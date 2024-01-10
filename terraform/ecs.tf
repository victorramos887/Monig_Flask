# # create the ECS cluster
# resource "aws_ecs_cluster" "fp-ecs-cluster" {
#   name = "flask-app"
  
#   tags = {
#     Name = "flask-app"
#   }
# }


# resource "aws_ecs_cluster_capacity_providers" "capacidade_provider" {
#   cluster_name = aws_ecs_cluster.fp-ecs-cluster.name

#   capacity_providers = ["FARGATE"]

#   default_capacity_provider_strategy {
#     base              = 2
#     weight            = 100
#     capacity_provider = "FARGATE"
#   }
# }