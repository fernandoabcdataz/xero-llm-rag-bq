Prerequisites

Before you begin, ensure you have the following installed:
Git
Google Cloud SDK
Terraform
Getting Started

1. Clone the Repository:
```
git clone https://github.com/your-repo/your-project.git
cd your-project
```

2. Set Up Google Cloud SDK:
```
gcloud init
```

3. Create a Service Account and Grant Roles:
```
gcloud iam service-accounts create terraform-sa --display-name "Terraform Service Account"
gcloud projects add-iam-policy-binding abcdataz \
--member="serviceAccount:terraform-sa@abcdataz.iam.gserviceaccount.com" \
--role="roles/editor"
gcloud projects add-iam-policy-binding abcdataz \
--member="serviceAccount:terraform-sa@abcdataz.iam.gserviceaccount.com" \
--role="roles/secretmanager.admin"
gcloud projects add-iam-policy-binding abcdataz \
--member="serviceAccount:terraform-sa@abcdataz.iam.gserviceaccount.com" \
--role="roles/secretmanager.secretAccessor"
gcloud projects add-iam-policy-binding abcdataz \
--member="serviceAccount:terraform-sa@abcdataz.iam.gserviceaccount.com" \
--role="roles/cloudrun.admin"
gcloud projects add-iam-policy-binding abcdataz \
--member="serviceAccount:terraform-sa@abcdataz.iam.gserviceaccount.com" \
--role="roles/storage.admin"
gcloud iam service-accounts keys create service-account.json --iam-account terraform-sa@abcdataz.iam.gserviceaccount.com
```

4. Set Environment Variable for Service Account Key:
```
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
Note: Replace /path/to/service-account.json with the actual path to your downloaded service account key file.
```

5. Initialize Terraform:
```
terraform init
```

6. Import Existing Resources (Optional):
If you have existing resources you want to manage with Terraform, import them using the appropriate commands. For example:
```
terraform import google_storage_bucket.xero_data_bucket abcdataz-xero-data
terraform import google_secret_manager_secret.client_id projects/abcdataz/secrets/client-id
terraform import google_secret_manager_secret.client_secret projects/abcdataz/secrets/client-secret
```

7. Apply Terraform Configuration:
```
terraform apply
```
This command will review your Terraform code, show you the planned changes, and prompt you for confirmation before applying them to your Google Cloud environment.