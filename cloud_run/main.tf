provider "google" {
  project     = "abcdataz"
  region      = "australia-southeast1"
  credentials = file("service-account.json")
}

resource "google_storage_bucket" "xero_data_bucket" {
  name          = "abcdataz-xero-data"
  location      = "australia-southeast1"
  force_destroy = true
}

resource "google_secret_manager_secret" "client_id" {
  secret_id = "client-id"
  replication {
    user_managed {
      replicas {
        location = "australia-southeast1"
      }
    }
  }
}

resource "google_secret_manager_secret_version" "client_id_version" {
  secret      = google_secret_manager_secret.client_id.id
  secret_data = "EAE32EE6A8514754AADF4BC8551CDFAA"
}

resource "google_secret_manager_secret" "client_secret" {
  secret_id = "client-secret"
  replication {
    user_managed {
      replicas {
        location = "australia-southeast1"
      }
    }
  }
}

resource "google_secret_manager_secret_version" "client_secret_version" {
  secret      = google_secret_manager_secret.client_secret.id
  secret_data = "42rkPKJFTtcVFpWQd1hrRVuOfeG-kSC2QElL3p_VdeIAyTBt"
}

resource "google_cloud_run_service" "xero_api" {
  name     = "xero-api"
  location = "australia-southeast1"

  template {
    spec {
      containers {
        image = "gcr.io/abcdataz/xero-api"
        env {
          name  = "CLIENT_NAME"
          value = "demo"
        }
        env {
          name = "GOOGLE_CLOUD_PROJECT"
          value = "abcdataz"
        }
        env {
          name = "CLIENT_ID"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.client_id.secret_id
              key  = "latest"
            }
          }
        }
        env {
          name = "CLIENT_SECRET"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.client_secret.secret_id
              key  = "latest"
            }
          }
        }
        ports {
          container_port = 8080
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_service.xero_api.location
  project     = google_cloud_run_service.xero_api.project
  service     = google_cloud_run_service.xero_api.name

  policy_data = data.google_iam_policy.noauth.policy_data
}

data "google_iam_policy" "noauth" {
  binding {
    role    = "roles/run.invoker"
    members = ["allUsers"]
  }
}