# create security group
resource "aws_security_group" "public-sg" {
  name = "public-group-default"
  description = "access to public instances"
  vpc_id = aws_vpc.vpc.id
}

# create security group for ALB
resource "aws_security_group" "alb_sg" {
  name = "alb-group"
  description = "control access to the application load balancer"
  vpc_id = aws_vpc.vpc.id

  ingress {
    from_port = 80
    to_port = 80
    protocol = "TCP"
    cidr_blocks = [
      "0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = [
      "0.0.0.0/0"]
  }
}

# create security group to access the ecs cluster (traffic to ecs cluster should only come from the ALB)
resource "aws_security_group" "ecs_sg" {
  name = "ecs-from-alb-group"
  description = "control access to the ecs cluster"
  vpc_id = aws_vpc.vpc.id

  ingress {
    from_port = var.flask_app_port
    to_port = var.flask_app_port
    protocol = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
    security_groups = [aws_security_group.alb_sg.id]
  }

  egress {
    protocol = "-1"
    from_port = 0
    to_port = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# create security group for RDS
resource "aws_security_group" "rds_sg" {
  name = "postgres-public-group"
  description = "access to public rds instances"
  vpc_id = aws_vpc.vpc.id

  ingress {
    protocol = "TCP"
    from_port = var.postgres_db_port
    to_port = var.postgres_db_port
    cidr_blocks = ["0.0.0.0/0"]
    security_groups = [aws_security_group.alb_sg.id]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

#ALTERAÇÃO: Acrecentado Security Group

resource "aws_security_group" "allow_tls" {
  name        = "allow_tls"
  description = "Allow TLS inbound traffic"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    description      = "TLS from VPC"
    from_port        = 443
    to_port          = 443
    protocol         = "TCP"
    cidr_blocks      = [aws_vpc.vpc.cidr_block]
    # ipv6_cidr_blocks = [aws_vpc.vpc.ipv6_cidr_block] #Removido cidr ipv6
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "allow_tls"
  }
}