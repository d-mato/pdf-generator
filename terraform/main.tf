terraform {
  required_version = ">= 1.2.7"
}

resource "aws_ecr_repository" "main" {
  name = "pdf-generator"
}

resource "aws_ecr_lifecycle_policy" "main" {
  repository = aws_ecr_repository.main.name
  policy     = file("docs/ecr_lifecycle_policy.json")
}

resource "aws_iam_role" "lambda" {
  assume_role_policy = file("docs/lambda_assume_policy.json")
}

resource "aws_iam_role_policy_attachment" "lambda" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "main" {
  function_name = "pdf-generator"
  role          = aws_iam_role.lambda.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.main.repository_url}:latest"

  timeout     = 30
  memory_size = 1024
}

resource "aws_apigatewayv2_api" "main" {
  name          = "pdf-generator"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "main" {
  api_id      = aws_apigatewayv2_api.main.id
  name        = "default"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway.arn
    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
    })
  }
}

resource "aws_apigatewayv2_integration" "main" {
  api_id = aws_apigatewayv2_api.main.id

  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.main.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "main" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.main.id}"
}

resource "aws_lambda_permission" "main" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

resource "aws_cloudwatch_log_group" "api_gateway" {
  name = "/aws/api_gateway/${aws_apigatewayv2_api.main.name}"

  retention_in_days = 7
}
