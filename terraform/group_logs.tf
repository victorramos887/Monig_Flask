resource "aws_cloudwatch_log_group" "logs_monig_api" {
  name = "Monig"

  tags = {
    Environment = "production"
    Application = "flask-app"
  }
}