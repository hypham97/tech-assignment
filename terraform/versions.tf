terraform {
  required_version = ">= 0.13"
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.36.0"
    }
  }

  backend "gcs" {
    bucket  = "tf-state-tech-assignment-362812"
    prefix  = "terraform/state"
  }
}