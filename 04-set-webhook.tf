resource "null_resource" "name" {
  provisioner "local-exec" {
    command = "curl --location --request POST 'https://api.telegram.org/bot${var.api_key}/setWebhook?url=${google_cloud_run_service.sembako.status[0].url}&max_connections=5&drop_pending_updates=true'"
  }
}
