terraform {

  required_providers {
    google {
      source = "hashicorp/google"
    }
  }

  backend "gcs" {
    bucket = "sembako-terraform-state"
    prefix = "state"
  }
}

provider "google" {
  project = "scheduled-chat-bot"
  region = "asia-southeast2"
  zone = "asia-southeast2-a"
}
