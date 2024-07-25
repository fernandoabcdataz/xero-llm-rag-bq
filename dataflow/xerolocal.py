import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests
import json
import logging
import os

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
        self.processed_all_endpoints = False  # FLAG TO TRACK ENDPOINT PROCESSING

    def fetch_token(self):
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=self.token_url, client_id=self.client_id, client_secret=self.client_secret)
        return token

    def start_bundle(self):
        self.token = self.fetch_token()
        self.processed_all_endpoints = False

    def process(self, element):
        for name, endpoint in self.endpoints.items():
            if self.processed_all_endpoints:
                # NO NEED TO PROCESS FURTHER ENDPOINTS IF ALL ARE DONE
                break
            data = fetch_data_from_endpoint(self.token, endpoint)
            if not data:
                # CHECK FOR EMPTY DATA TO POTENTIALLY SIGNAL TERMINATION (IF APPLICABLE)
                logging.info(f"No data received for endpoint: {name}. Assuming termination.")
                self.processed_all_endpoints = True  # SET FLAG TO STOP FURTHER PROCESSING
                break
            file_content = json.dumps(data, indent=2)
            yield {
                'endpoint_name': name,
                'file_content': file_content
            }

class WriteJSONToLocal(beam.DoFn):
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def process(self, element):
        file_name = os.path.join(self.output_dir, f"{element['endpoint_name']}.json")
        with open(file_name, 'w') as f:
            f.write(element['file_content'])
        yield f"saved {file_name} locally"

def run_pipeline():
    pipeline_options = PipelineOptions()
    
    client_name = 'demo'  # Directly setting client_name since we're running locally

    p = beam.Pipeline(options=pipeline_options)

    results = (
        p
        | 'Start' >> beam.Create([None])
        | 'FetchDataFromEndpoints' >> beam.ParDo(FetchDataFromEndpoints(ENDPOINTS, CLIENT_ID, CLIENT_SECRET, TOKEN_URL))
    )

    # SAVE LOCALLY
    output_dir = 'output'  # Specify your local output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    results | 'WriteToLocal' >> beam.ParDo(WriteJSONToLocal(output_dir))

    p.run().wait_until_finish()

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run_pipeline()