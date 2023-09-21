resource "aws_cloudwatch_log_group" "log" {
    name = "log-cluster-flask"
    retention_in_days = 7
}