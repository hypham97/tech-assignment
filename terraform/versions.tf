terraform {
  required_version = ">= 0.13"
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.36.0"
    }
  }

  backend "remote" {
    organization = "nc"
    workspaces {
        name = "tech-assignment"
    }
  }  
}