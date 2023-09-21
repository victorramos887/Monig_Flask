resource "aws_iam_role" "task_execution_role" {
  name = "task-execution-role"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = {
          Service = [
            "ecs-tasks.amazonaws.com",
            "amplify.amazonaws.com"
          ], #ecs-tasks.amazonaws.com
        },
        Action    = "sts:AssumeRole"
      }
    ]
  })
 
}



resource "aws_iam_policy_attachment" "cloudwatch_logs_attachment" {
  name       = "cloudwatch-logs-attachment"
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess" # Use a política adequada do CloudWatch Logs
  roles      = [aws_iam_role.task_execution_role.name]
}