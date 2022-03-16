output "sembako_email" {
  value = google_service_account.sembako_account.email
}

output "cloud_run_url" {
  value = google_cloud_run_service.sembako.status[0].url
}
