resource "aws_acm_certificate" "acm_certificate" {
  domain_name       = "moing.com.br"
  validation_method = "EMAIL"

  tags = {
    Environment = "flask_monig"
  }

  lifecycle {
    create_before_destroy = true
  }
}