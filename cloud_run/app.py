from flask import Flask, request
import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests
import json
from google.cloud import storage
import time
import os
import traceback
from google.cloud import secretmanager

app = Flask(__name__)

def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')

CLIENT_ID = get_secret('xero-client-id')
CLIENT_SECRET = get_secret('xero-client-secret')

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("CLIENT_ID and CLIENT_SECRET are required")

TOKEN_URL = 'https://identity.xero.com/connect/token'

ENDPOINTS = {
    'bank_transactions': 'https://api.xero.com/api.xro/2.0/BankTransactions',
    'contacts': 'https://api.xero.com/api.xro/2.0/Contacts',
    'invoices': 'https://api.xero.com/api.xro/2.0/Invoices',
    'journals': 'https://api.xero.com/api.xro/2.0/Journals',
    'reports__balance_sheet': 'https://api.xero.com/api.xro/2.0/Reports/BalanceSheet',
    'reports__bank_summary': 'https://api.xero.com/api.xro/2.0/Reports/BankSummary',
    'reports__profit_and_loss': 'https://api.xero.com/api.xro/2.0/Reports/ProfitAndLoss',
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
    def __init__(self, endpoints, client_id, client_secret, token_url):
        self.endpoints = endpoints
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.processed_all_endpoints = False

    def fetch_token(self):
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=self.token_url, client_id=self.client_id, client_secret=self.client_secret)
        return token

    def start_bundle(self):
        self.token = self.fetch_token()
        self.processed_all_endpoints = False
        logging.info("Token fetched and bundle started.")

    def process(self, element):
        for name, endpoint in self.endpoints.items():
            if self.processed_all_endpoints:
                break
            logging.info(f"Fetching data from endpoint: {endpoint}")
            start_time = time.time()
            data = fetch_data_from_endpoint(self.token, endpoint)
            end_time = time.time()
            logging.info(f"Data fetched from {endpoint} in {end_time - start_time} seconds.")
            if not data:
                logging.info(f"No data received for endpoint: {name}. Assuming termination.")
                self.processed_all_endpoints = True
                break
            file_content = json.dumps(data, indent=2)
            yield {
                'endpoint_name': name,
                'file_content': file_content
            }
            logging.info(f"Data processed for endpoint: {name}")

class WriteJSONToGCS(beam.DoFn):
    def __init__(self, bucket_name, client_name):
        self.bucket_name = bucket_name
        self.client_name = client_name

    def start_bundle(self):
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.get_bucket(self.bucket_name)
        logging.info("GCS client initialized and bucket accessed.")

    def process(self, element):
        file_name = f"{element['endpoint_name']}.json"
        blob = self.bucket.blob(file_name)
        blob.upload_from_string(element['file_content'], content_type='application/json')
        yield f"saved {file_name} to gs://{self.bucket_name}/{file_name}"
        logging.info(f"File {file_name} saved to GCS.")

def run_pipeline():
    try:
        # read environment variables
        client_name = os.getenv('CLIENT_NAME')
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')

        if not client_name:
            raise ValueError("CLIENT_NAME environment variable is required")
        if not project_id:
            raise ValueError("PROJECT ID environment variable is required")

        logging.info(f"starting pipeline for client: {client_name}, project_id: {project_id}")

        bucket_name = f"{project_id}-{client_name}-xero-data"

        options = PipelineOptions()
        options.view_as(StandardOptions).runner = 'DirectRunner'

        p = beam.Pipeline(options=options)

        results = (
            p
            | 'Start' >> beam.Create([None])
            | 'FetchDataFromEndpoints' >> beam.ParDo(FetchDataFromEndpoints(ENDPOINTS, CLIENT_ID, CLIENT_SECRET, TOKEN_URL))
        )

        results | 'WriteToGCS' >> beam.ParDo(WriteJSONToGCS(bucket_name, client_name))
        p.run().wait_until_finish()

        logging.info("pipeline completed successfully")

    except Exception as e:
        logging.error(f"error running pipeline: {str(e)}")
        logging.error(traceback.format_exc())
        raise

@app.route('/run', methods=['POST'])
def trigger_pipeline():
    try:
        run_pipeline()
        return 'pipeline started', 200
    except Exception as e:
        logging.error(f"error triggering pipeline: {str(e)}")
        return 'internal server error', 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.getLogger().setLevel(logging.INFO)
    app.run(host='0.0.0.0', port=8080)