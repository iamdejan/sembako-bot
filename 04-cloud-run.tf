resource "google_cloud_run_service" "sembako" {
  name     = "sembako-bot"
  location = var.region

  template {
    spec {
      containers {
        image = "" # TODO dejan: upload dlu ke Artifact Registry / Docker Hub
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

data "google_iam_policy" "admin" {
  binding {
    role = "roles/viewer"
    members = [
      "serviceAccount:${google_service_account.sembako_account.email}"
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "policy" {
  location = google_cloud_run_service.default.location
  project = google_cloud_run_service.default.project
  service = google_cloud_run_service.default.name
  policy_data = data.google_iam_policy.admin.policy_data
}
