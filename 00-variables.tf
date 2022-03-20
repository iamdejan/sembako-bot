variable "project" {
  description = "Project ID on where these resources are located."
  default     = "scheduled-chat-bot"
}

variable "region" {
  description = "Project's region."
  default     = "asia-southeast2"
}

variable "zone" {
  description = "Zone inside chosen region."
  default     = "asia-southeast2-a"
}

variable "api_key" {
  description = "API key for Telegram bot."
}

variable "time_zone" {
  description = "Time zone for scheduler."
  default = "Asia/Jakarta"
}

variable "tag_version" {
  description = "Tag version of the Docker image."
}

variable "db_string" {
  description = "Connection sring for CockroachDB."
}
