resource "google_cloud_scheduler_job" "sembako" {
  name             = "sembako-job"
  description      = "Sembako job"
  schedule         = "0 0 * * *"
  time_zone        = var.time_zone
  attempt_deadline = "600s"

  http_target {
    http_method = "POST"
    uri         = "${google_cloud_run_service.sembako.status[0].url}/prices"

    oidc_token {
      service_account_email = google_service_account.sembako_account.email
    }
  }
}
