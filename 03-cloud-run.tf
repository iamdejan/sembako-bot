resource "google_cloud_run_service" "sembako" {
  name     = "sembako-bot"
  location = var.region

  template {
    spec {
      containers {
        image = "asia.gcr.io/scheduled-chat-bot/sembako-bot:${var.tag_version}"
        env {
          name  = "API_KEY"
          value = var.api_key
        }
        env {
          name = "DB_STRING"
          value = var.db_string
        }
        ports {
          container_port = 8000
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

data "google_iam_policy" "runner" {
  binding {
    role = "roles/run.invoker"
    members = [
      "serviceAccount:${google_service_account.sembako_account.email}"
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "runner" {
  location    = google_cloud_run_service.sembako.location
  project     = google_cloud_run_service.sembako.project
  service     = google_cloud_run_service.sembako.name
  policy_data = data.google_iam_policy.runner.policy_data
}
