terraform {
  backend "etcdv3" {
    endpoints = ["34.101.107.21:2379"]
    lock      = true
    prefix    = "/sembako-bot"
  }
}

provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
}
