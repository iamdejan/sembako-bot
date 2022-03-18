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

variable "chat_ids" {
  description = "List of Telegram chat IDs that want to be sent automatic message."
  default = "1661005444,1380613892,1637396348"
}
