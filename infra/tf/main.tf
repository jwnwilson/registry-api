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

module "registry_api" {
  source = "github.com/jwnwilson/terraform-aws-modules/modules/lambda-api"

  environment       = var.environment
  project           = "registry"
  ecr_url           = var.ecr_url
  docker_tag        = var.docker_tag
}

module "api_gateway" {
  source = "github.com/jwnwilson/terraform-aws-modules/modules/apigateway"

  environment       = var.environment
  lambda_invoke_arn = module.registry_api.lambda_function_invoke_arn
  lambda_name       = module.registry_api.lambda_function_name
  domain            = "jwnwilson.co.uk"
  api_subdomain     = "registry-${var.environment}"
  project           = "registry"
}