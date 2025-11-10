variable "aws_region" {
  description = "The AWS region to deploy resources into."
  default     = "us-east-1"
}

variable "project_name" {
  description = "A prefix used for all resources."
  default     = "quant-pipeline"
}