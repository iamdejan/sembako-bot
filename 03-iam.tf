resource "google_project_iam_binding" "cloud_functions" {
  project = var.project
  role    = "roles/cloudfunctions.admin"

  members = [
    "serviceAccount:${google_service_account.sembako_account.email}"
  ]
}

resource "google_project_iam_binding" "cloud_scheduler" {
  project = var.project
  role    = "roles/cloudscheduler.admin"

  members = [
    "serviceAccount:${google_service_account.sembako_account.email}"
  ]
}
