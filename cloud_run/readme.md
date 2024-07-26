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
export GOOGLE_APPLICATION_CREDENTIALS="service-account.json"
```

5. Rebuild and push the Docker image to GCR:
```
docker buildx build --platform linux/amd64 -t gcr.io/abcdataz/xero-api --push .
```

6. Initialize Terraform:
```
terraform init
```

7. Apply Terraform Configuration:
```
terraform apply
```

8. Trigger Cloud Run
CURL -X POST https://xero-api-pnyecjivxq-ts.a.run.app/run