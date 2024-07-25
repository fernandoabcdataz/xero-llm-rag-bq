command 1:
gcloud init

command 2:
gcloud projects create abcdataz

command 3:
gcloud config set project abcdataz

command 4:
gcloud services enable dataflow compute_component logging storage_component storage_api bigquery pubsub datastore.googleapis.com cloudresourcemanager.googleapis.com

command 5:
gcloud auth application-default login

command 6:
gcloud projects add-iam-policy-binding abcdataz --member="user:fernando@abcdataz.com" --role="roles/iam.serviceAccountUser"
gcloud projects add-iam-policy-binding abcdataz --member="user:fernando@abcdataz.com" --role="roles/dataflow.admin"
gcloud projects add-iam-policy-binding abcdataz --member="user:fernando@abcdataz.com" --role="roles/storage.admin"
gcloud projects add-iam-policy-binding abcdataz --member="user:fernando@abcdataz.com" --role="roles/storage.objectViewer"

command 7:
gcloud projects add-iam-policy-binding abcdataz --member="serviceAccount:215301014952-compute@developer.gserviceaccount.com" --role="roles/dataflow.admin"
gcloud projects add-iam-policy-binding abcdataz --member="serviceAccount:215301014952-compute@developer.gserviceaccount.com" --role="roles/dataflow.worker"
gcloud projects add-iam-policy-binding abcdataz --member="serviceAccount:215301014952-compute@developer.gserviceaccount.com" --role="roles/storage.objectAdmin"

command 8:
python3 -m venv beam-env

command 9:
source beam-env/bin/activate

command 10:
pip3 install -r requirements.txt

command 11:
python3 xero.py \
    --project=abcdataz \
    --client_name=demo \
    --dataflow_region=australia-southeast1 \
    --dataflow_zone=australia-southeast1-c \
    --runner=DataflowRunner \
    --worker_machine_type=n1-standard-4