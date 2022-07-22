terraform {
  required_version = "~>1.2.5"

  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~>4.23.0"
    }
  }

  backend "s3" {
    region = "us-east-1"
    bucket = "levendredi.backend"
    key = "terraform.tfstate"
  }

}

provider "aws" {
      region = "us-east-1"
      default_tags {
        tags = {
          Projet = "levendredi"
          version = "0.1"
        }
      }
    }
