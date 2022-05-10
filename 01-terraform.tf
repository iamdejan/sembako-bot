terraform {
  backend "gcs" {
    bucket = "sembako-terraform-state"
    prefix = "/sembako-bot"
  }
}

provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
}
