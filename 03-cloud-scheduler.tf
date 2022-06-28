resource "google_cloud_scheduler_job" "sembako" {
  name             = "sembako-job"
  description      = "Sembako job"
  schedule         = "0 0 * * *"
  time_zone        = var.time_zone
  attempt_deadline = "600s"

  retry_config {
    min_backoff_duration = "1s"
    max_retry_duration   = "60s"
    max_doublings        = 2
    retry_count          = 3
  }

  http_target {
    http_method = "POST"
    uri         = "${google_cloud_run_service.sembako.status[0].url}/prices"
  }
}
