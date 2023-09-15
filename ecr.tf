# provider "aws" {
#   region = "us-east-1" # Substitua pela região desejada
# }
resource "aws_caller_identity" "current" {}

resource "aws_ecr_repository" "repositorio-ecr-monig" {
  name = "monig" # Nome do seu repositório ECR
}

# Configure a política para permitir o acesso ao repositório ECR
data "aws_iam_policy_document" "ecr_policy" {
  statement {
    actions   = ["ecr:GetDownloadUrlForLayer", "ecr:GetRepositoryPolicy", "ecr:ListImages", "ecr:BatchCheckLayerAvailability", "ecr:GetAuthorizationToken", "ecr:GetManifest", "ecr:PutImage"]
    resources = [aws_ecr_repository.repositorio-ecr-monig.arn]
  }
}

resource "aws_ecr_repository_policy" "my_ecr_policy" {
  name        = "my-ecr-policy"
  repository  = aws_ecr_repository.repositorio-ecr-monig.name
  policy      = data.aws_iam_policy_document.ecr_policy.json
}

# Use the AWS CLI to authenticate Docker to your ECR registry
resource "null_resource" "docker_auth" {
  provisioner "local-exec" {
    command = "aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin ${aws_account_id}.dkr.ecr.us-east-2.amazonaws.com"
  }
  triggers = {
    aws_account_id = aws_caller_identity.current.account_id
  }
}

# Push your Docker image to the ECR repository
resource "null_resource" "docker_push" {
  depends_on = [null_resource.docker_auth]

  provisioner "local-exec" {
    command = "docker tag repositorio-ecr-monig:test ${aws_account_id}.dkr.ecr.us-east-2.amazonaws.com/repositorio-ecr-monig:test"
  }
}

resource "null_resource" "docker_push_2" {
  depends_on = [null_resource.docker_push]

  provisioner "local-exec" {
    command = "docker push ${aws_account_id}.dkr.ecr.us-east-2.amazonaws.com/repositorio-ecr-monig:test"
  }
}

# # Output the ECR repository URL for later use
# output "ecr_repository_url" {
#   value = "${aws_account_id}.dkr.ecr.us-east-1.amazonaws.com/repositorio-ecr-monig"
# }

output "ecr_repository_url" {
  value = aws_ecr_repository.repositorio-ecr-monig.repository_url
}
