terraform {
  backend "s3" {
    bucket = "my-terraform-state-bucket"
    key    = "task-manager/terraform.tfstate"
    region = "us-east-1"
  }
}
