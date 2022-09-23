terraform {
  required_version = ">= 1.2.7"
}

locals {
  function_name = "pdf-generator"
}

module "ecr" {
  source = "./modules/ecr"

  repository_name = local.function_name
}

module "lambda" {
  source = "./modules/lambda"

  function_name  = local.function_name
  repository_url = module.ecr.repository_url
}

module "api_gateway" {
  source = "./modules/api_gateway"

  lambda_invoke_arn    = module.lambda.invoke_arn
  lambda_function_name = local.function_name
}

