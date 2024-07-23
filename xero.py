import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions, GoogleCloudOptions
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests
import json
from google.cloud import storage

# REPLACE THESE WITH YOUR CLIENT ID AND CLIENT SECRET
CLIENT_ID = 'EAE32EE6A8514754AADF4BC8551CDFAA'
CLIENT_SECRET = '42rkPKJFTtcVFpWQd1hrRVuOfeG-kSC2QElL3p_VdeIAyTBt'
TOKEN_URL = 'https://identity.xero.com/connect/token'

# DEFINE YOUR ENDPOINTS
ENDPOINTS = {
    'bank_transactions': 'https://api.xero.com/api.xro/2.0/BankTransactions',
    'invoices': 'https://api.xero.com/api.xro/2.0/Invoices',
}

# FETCH TOKEN
def fetch_token():
    client = BackendApplicationClient(client_id=CLIENT_ID)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=TOKEN_URL, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    return token

# PASS TOKEN AND ENDPOINTS
def fetch_data_from_endpoint(token, endpoint):
    headers = {'Authorization': f'Bearer {token["access_token"]}', 'Accept': 'application/json'}
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()

class FetchDataFromEndpoints(beam.DoFn):
    def __init__(self, endpoints):
        self.endpoints = endpoints

    def start_bundle(self):
        self.token = fetch_token()

    def process(self, element):
        for name, endpoint in self.endpoints.items():
            data = fetch_data_from_endpoint(self.token, endpoint)
            file_content = json.dumps(data, indent=2)
            yield {
                'endpoint_name': name,
                'file_content': file_content
            }

class WriteJSONToGCS(beam.DoFn):
    def __init__(self, bucket_name, client_name):
        self.bucket_name = bucket_name
        self.client_name = client_name

    def start_bundle(self):
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(self.bucket_name)

    def process(self, element):
        file_name = f"{self.client_name}/{element['endpoint_name']}.json"
        blob = self.bucket.blob(file_name)
        blob.upload_from_string(element['file_content'], content_type='application/json')
        yield f"saved {file_name} to gs://{self.bucket_name}/{file_name}"

def create_bucket_if_not_exists(bucket_name, project_id, location="australia-southeast1"):
    storage_client = storage.Client(project=project_id)
    
    try:
        bucket = storage_client.get_bucket(bucket_name)
        print(f"Bucket {bucket_name} already exists")
    except Exception:
        bucket = storage_client.create_bucket(bucket_name, location=location)
        print(f"Bucket {bucket_name} created")
    
    return bucket

class XeroOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument(
            '--client_name',
            required=True,
            help='NAME OF THE CLIENT, USED IN BUCKET NAMING AND AS A PREFIX FOR DATAFLOW JOB NAME'
        )

def run_pipeline():
    pipeline_options = XeroOptions()
    
    # ACCESS THE CLIENT_NAME FROM OUR CUSTOM OPTIONS
    client_name = pipeline_options.client_name
    
    # ACCESS THE PROJECT FROM THE GOOGLECLOUDOPTIONS
    google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
    project_id = google_cloud_options.project

    if not project_id:
        raise ValueError("Please provide a project ID using --project argument")

    # CONSTRUCT BUCKET NAME
    bucket_name = f"{project_id}--{client_name}--xero-data"

    # CREATE THE BUCKET IF IT DOESN'T EXIST
    create_bucket_if_not_exists(bucket_name, project_id)

    # SET UP THE PIPELINE OPTIONS
    options = pipeline_options.view_as(PipelineOptions)
    options.view_as(StandardOptions).runner = 'DataflowRunner'
    google_cloud_options.temp_location = f'gs://{bucket_name}/temp'
    google_cloud_options.job_name = f'{client_name}-xero-data-pipeline'

    p = beam.Pipeline(options=options)

    results = (
        p
        | 'Start' >> beam.Create([None])
        | 'FetchDataFromEndpoints' >> beam.ParDo(FetchDataFromEndpoints(ENDPOINTS))
    )

    # SAVE TO GOOGLE CLOUD STORAGE
    results | 'WriteToGCS' >> beam.ParDo(WriteJSONToGCS(bucket_name, client_name))

    p.run().wait_until_finish()

if __name__ == '__main__':
    run_pipeline()
