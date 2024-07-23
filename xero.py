import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions, GoogleCloudOptions, WorkerOptions, SetupOptions
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests
import json
from google.cloud import storage
import logging

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
    def __init__(self, endpoints, client_id, client_secret, token_url):
        self.endpoints = endpoints
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url

    def fetch_token(self):
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=self.token_url, client_id=self.client_id, client_secret=self.client_secret)
        return token

    def start_bundle(self):
        self.token = self.fetch_token()

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
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.get_bucket(self.bucket_name)

    def process(self, element):
        file_name = f"{self.client_name}/{element['endpoint_name']}.json"
        blob = self.bucket.blob(file_name)
        blob.upload_from_string(element['file_content'], content_type='application/json')
        yield f"saved {file_name} to gs://{self.bucket_name}/{file_name}"

def create_bucket_if_not_exists(bucket_name, project_id, location):
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
        parser.add_argument(
            '--dataflow_region',
            required=True,
            help='THE REGION TO RUN THE DATAFLOW JOB IN'
        )
        parser.add_argument(
            '--dataflow_zone',
            required=True,
            help='THE ZONE TO RUN THE DATAFLOW JOB IN'
        )

def run_pipeline():
    pipeline_options = XeroOptions()
    
    # ACCESS THE CLIENT_NAME FROM OUR CUSTOM OPTIONS
    client_name = pipeline_options.client_name
    
    # ACCESS THE PROJECT FROM THE GOOGLECLOUDOPTIONS
    google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
    project_id = google_cloud_options.project

    if not project_id:
        raise ValueError("please provide a PROJECT ID using --project argument")

    # ACCESS REGION AND ZONE FROM OUR CUSTOM OPTIONS
    region = pipeline_options.dataflow_region
    zone = pipeline_options.dataflow_zone

    # CONSTRUCT BUCKET NAME
    bucket_name = f"{project_id}--{client_name}--xero-data"

    # CREATE THE BUCKET IF IT DOESN'T EXIST
    create_bucket_if_not_exists(bucket_name, project_id, region)

    # SET UP THE PIPELINE OPTIONS
    options = pipeline_options.view_as(PipelineOptions)
    options.view_as(StandardOptions).runner = 'DataflowRunner'
    google_cloud_options.temp_location = f'gs://{bucket_name}/temp'
    google_cloud_options.job_name = f'{client_name}-xero-data-pipeline'
    google_cloud_options.region = region

    worker_options = pipeline_options.view_as(WorkerOptions)
    worker_options.zone = zone

    # Add this line to include the setup file
    pipeline_options.view_as(SetupOptions).setup_file = './setup.py'

    p = beam.Pipeline(options=pipeline_options)

    results = (
        p
        | 'Start' >> beam.Create([None])
        | 'FetchDataFromEndpoints' >> beam.ParDo(FetchDataFromEndpoints(ENDPOINTS, CLIENT_ID, CLIENT_SECRET, TOKEN_URL))
    )

    # SAVE TO GOOGLE CLOUD STORAGE
    results | 'WriteToGCS' >> beam.ParDo(WriteJSONToGCS(bucket_name, client_name))

    p.run().wait_until_finish()

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run_pipeline()