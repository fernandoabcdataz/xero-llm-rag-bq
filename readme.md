gcloud projects add-iam-policy-binding abcdataz \                      
--member="serviceAccount:terraform-sa@abcdataz.iam.gserviceaccount.com" \
--role="roles/bigquery.user"

https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/use-cases/retrieval-augmented-generation/rag_qna_with_bq_and_featurestore.ipynb