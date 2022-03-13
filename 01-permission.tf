resource "google_service_account" "sembako_account" {
  account_id   = "sembako-scheduler"
  display_name = "Service Account for Terraform scheduler"
}

data "google_iam_policy" "admin" {
  depends_on = [
    google_service_Account.sembako_account.id
  ]

  binding {
    role = "roles/cloudfunctions.admin"

    members = [
      google_service_Account.sembako_account.email
    ]
  }

  binding {
    role = "roles/cloudscheduler.admin"

    members = [
      google_service_Account.sembako_account.email
    ]
  }
}
