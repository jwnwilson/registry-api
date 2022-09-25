terraform {
  backend "s3" {
    region = "eu-west-1"
    bucket = "jwnwilson-registry-tf"
    key = "terraform.tfstate"
  }
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region  = var.aws_region
}
