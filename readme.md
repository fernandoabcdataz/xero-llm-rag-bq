gcloud projects add-iam-policy-binding abcdataz \                      
--member="serviceAccount:terraform-sa@abcdataz.iam.gserviceaccount.com" \
--role="roles/bigquery.user"