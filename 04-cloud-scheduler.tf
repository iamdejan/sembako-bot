resource "google_cloud_scheduler_job" "sembako" {
  name             = "sembako-job"
  description      = "Sembako job"
  schedule         = "* * * * *"
  time_zone        = var.time_zone
  attempt_deadline = "320s"

  http_target {
    http_method = "POST"
    uri         = "https://sembako-bot-tmnmmjo4aq-et.a.run.app/execute"

    oidc_token {
      service_account_email = google_service_account.sembako_account.email
    }
  }
}

