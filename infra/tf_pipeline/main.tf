terraform {
  backend "s3" {
    region = "eu-west-1"
    bucket = "jwnwilson-registry-tf"
    key = "terraform-pipeline.tfstate"
  }
}

provider "aws" {
  region  = var.aws_region
}

module "docker_images" {
  source = "github.com/jwnwilson/terraform-aws-modules/modules/ecr"

  project         = var.project
  access_key      = var.aws_access_key
  secret_key      = var.aws_secret_key
  region          = var.aws_region
}