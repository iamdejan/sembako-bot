resource "google_project_iam_policy" "project" {
  project     = var.project
  policy_data = data.google_iam_policy.admin.policy_data
}

data "google_iam_policy" "admin" {
  binding {
    role = "roles/run.admin"

    members = [
      "serviceAccount:${google_service_account.sembako_account.email}"
    ]
  }
}
