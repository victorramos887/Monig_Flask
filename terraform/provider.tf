provider "aws" {
  region = var.region
  version = "~> 4.16"
}

resource "random_string" "flask-secret-key" {
  length = 16
  special = true
  override_special = "/@\" "
}

