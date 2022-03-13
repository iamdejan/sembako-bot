resource "google_service_account" "sembako_account" {
  account_id   = "sembako-scheduler"
  display_name = "Service Account for Cloud Scheduler"
}

output "sembako_email" {
  value = google_service_account.sembako_account.email
}
