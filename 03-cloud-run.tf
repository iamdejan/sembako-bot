resource "random_string" "random" {
  length  = 4
  special = false
  upper   = false
  number  = false
}

resource "google_cloud_run_service" "sembako" {
  name     = "sembako-bot-${random_string.random.result}"
  location = var.region

  template {
    spec {
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
