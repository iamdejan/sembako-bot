resource "google_cloud_run_service" "sembako" {
  name     = "sembako-bot"
  location = var.region

  template {
    spec {
      containers {
        image = "asia.gcr.io/scheduled-chat-bot/sembako-bot:latest"
        env {
          name  = "API_KEY"
          value = var.api_key
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

resource "google_cloud_run_service_iam_policy" "policy" {
  location = google_cloud_run_service.sembako.location
  project  = google_cloud_run_service.sembako.project
  service  = google_cloud_run_service.sembako.name
  role     = "roles/run.admin"
  members = [
    "serviceAccount:${google_service_account.sembako_account.email}"
  ]
}
