resource "aws_mq_broker" "rabbitmq_broker" {
  broker_name        = "task-manager-rabbitmq"
  engine_type        = "RABBITMQ"
  engine_version     = "3.8.22"
  host_instance_type = "mq.t3.micro"

  publicly_accessible = false

  user {
    username = "admin"
    password = var.db_password
  }
}
