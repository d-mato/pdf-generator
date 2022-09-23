variable "repository_name" {}

resource "aws_ecr_repository" "this" {
  name = var.repository_name
}

resource "aws_ecr_lifecycle_policy" "this" {
  repository = aws_ecr_repository.this.name
  policy     = file("${path.module}/lifecycle_policy.json")
}

output "repository_url" {
  value = aws_ecr_repository.this.repository_url
}
