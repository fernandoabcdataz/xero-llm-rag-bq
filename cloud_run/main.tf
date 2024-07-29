provider "google" {
  project     = var.project
  region      = var.region
  credentials = file("service-account.json")
}

resource "google_storage_bucket" "xero_data_bucket" {
  name          = "${var.project}-${var.client_name}-xero-data"
  location      = var.region
  force_destroy = true
}

resource "google_secret_manager_secret" "client_id" {
  secret_id = "xero-client-id"
  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "client_id_version" {
  secret      = google_secret_manager_secret.client_id.id
  secret_data = var.xero_client_id
}

resource "google_secret_manager_secret" "client_secret" {
  secret_id = "xero-client-secret"
  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "client_secret_version" {
  secret      = google_secret_manager_secret.client_secret.id
  secret_data = var.xero_client_secret
}

resource "google_cloud_run_service" "xero_api" {
  name     = "${var.project}-${var.client_name}-xero-api"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project}/xero-api"
        env {
          name  = "CLIENT_NAME"
          value = var.client_name
        }
        env {
          name = "GOOGLE_CLOUD_PROJECT"
          value = var.project
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