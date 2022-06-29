resource "google_cloud_run_service" "sembako" {
  name     = "sembako-bot"
  location = var.region

  template {
    spec {
      timeout_seconds = 1200
      containers {
        image = var.docker_image
        env {
          name  = "API_KEY"
          value = var.api_key
        }
        env {
          name  = "DB_STRING"
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
      "allUsers"
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "runner" {
  location    = google_cloud_run_service.sembako.location
  project     = google_cloud_run_service.sembako.project
  service     = google_cloud_run_service.sembako.name
  policy_data = data.google_iam_policy.runner.policy_data
}
