# Configure the AWS provider
provider "aws" {
  region = var.aws_region
}

# --- 1. Container Registry (ECR) ---
# Where the Docker image will be stored
resource "aws_ecr_repository" "app_repo" {
  name                 = "${var.project_name}-ingestion-api"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# --- 2. Networking (VPC and Subnets for ECS/Fargate) ---
# A basic VPC structure is required for almost all cloud deployments
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0" # Use a stable version

  name = "${var.project_name}-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
  enable_nat_gateway = false
  enable_vpn_gateway = false
}

# --- 3. IAM Role for ECS Task Execution ---
# This role gives the deployed container permission to run and log
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${var.project_name}-task-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_exec_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}
