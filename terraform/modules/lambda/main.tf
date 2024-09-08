variable "function_name" {}
variable "repository_url" {}

resource "aws_iam_role" "this" {
  assume_role_policy = file("${path.module}/assume_policy.json")
}

resource "aws_iam_role_policy_attachment" "this" {
  role       = aws_iam_role.this.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "this" {
  function_name = var.function_name
  role          = aws_iam_role.this.arn
  package_type  = "Image"
  image_uri     = "${var.repository_url}:latest"

  timeout     = 30
  memory_size = 1024
}

resource "aws_lambda_function_url" "this" {
  function_name = aws_lambda_function.this.function_name
  authorization_type = "NONE"
}

output "invoke_arn" {
  value = aws_lambda_function.this.invoke_arn
}
