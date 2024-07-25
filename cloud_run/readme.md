docker buildx build --platform linux/amd64 -t gcr.io/abcdataz/xero-api --push .

gcloud run deploy xero-api --image gcr.io/abcdataz/xero-api --platform managed --region australia-southeast1 --allow-unauthenticated

curl -X POST https://xero-api-pnyecjivxq-ts.a.run.app/run