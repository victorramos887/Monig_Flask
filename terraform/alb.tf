# create the ALB
resource "aws_alb" "alb" {
  load_balancer_type = "application"
  name = "application-load-balancer"
  subnets = aws_subnet.public_subnets.*.id
  security_groups = [aws_security_group.alb_sg.id]
}

# point redirected traffic to the app
resource "aws_alb_target_group" "target_group" {
  name = "ecs-target-group"
  port = 80
  protocol = "HTTP"
  vpc_id = aws_vpc.vpc.id
  target_type = "ip"
}

# direct traffic through the ALB
resource "aws_alb_listener" "fp-alb-listener" {
  load_balancer_arn = aws_alb.alb.arn
  port = 80
  protocol = "HTTP"
  default_action {
    target_group_arn = aws_alb_target_group.target_group.arn
    type = "forward"
  }
}

resource "aws_lb_listener" "lb_api_https" {
    load_balancer_arn   =   "${aws_alb.alb.arn}"
    port            =   "443"
    protocol        =   "HTTPS"
    ssl_policy      =   "ELBSecurityPolicy-TLS-1-2-Ext-2018-06"
    certificate_arn     =   aws_acm_certificate.acm_certificate.arn
    default_action {
        target_group_arn    =   "${aws_alb_target_group.target_group.arn}"
        type            =   "forward"
    }
}

resource "aws_lb_listener_certificate" "ssl_certificate" {
  listener_arn=aws_lb_listener.lb_api_https.arn
  certificate_arn = aws_acm_certificate.acm_certificate.arn
}
