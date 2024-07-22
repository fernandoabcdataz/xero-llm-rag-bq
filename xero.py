import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests
import json

# REPLACE THESE WITH YOUR CLIENT ID AND CLIENT SECRET
CLIENT_ID = 'EAE32EE6A8514754AADF4BC8551CDFAA'
CLIENT_SECRET = '42rkPKJFTtcVFpWQd1hrRVuOfeG-kSC2QElL3p_VdeIAyTBt'
TOKEN_URL = 'https://identity.xero.com/connect/token'

# DEFINE YOUR ENDPOINTS
ENDPOINTS = {
    'bank_transactions': 'https://api.xero.com/api.xro/2.0/BankTransactions',
    'invoices': 'https://api.xero.com/api.xro/2.0/Invoices',
}

def fetch_token():
    client = BackendApplicationClient(client_id=CLIENT_ID)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=TOKEN_URL, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    return token

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

class WriteJSONFile(beam.DoFn):
    def __init__(self, directory):
        self.directory = directory

    def process(self, element):
        file_name = f"{element['endpoint_name']}.json"
        file_path = f"{self.directory}/{file_name}"
        with open(file_path, 'w') as f:
            f.write(element['file_content'])
        yield f"saved {file_name} to {self.directory}"

def run_pipeline():
    # Uncomment the following lines to use DataflowRunner and GCS
    # options = PipelineOptions(
    #     project='your-gcp-project-id',
    #     runner='DataflowRunner',
    #     temp_location='gs://your-temp-bucket/temp',
    #     region='your-region',
    # )
    options = PipelineOptions()
    options.view_as(StandardOptions).runner = 'DirectRunner'

    p = beam.Pipeline(options=options)

    results = (
        p
        | 'Start' >> beam.Create([None])
        | 'FetchDataFromEndpoints' >> beam.ParDo(FetchDataFromEndpoints(ENDPOINTS))
    )

    # Save to Local Storage
    results | 'WriteToLocal' >> beam.ParDo(WriteJSONFile('./data'))

    p.run().wait_until_finish()

if __name__ == '__main__':
    run_pipeline()