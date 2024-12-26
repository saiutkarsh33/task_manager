resource "aws_db_subnet_group" "db_subnet_group" {
  name       = "task-manager-db-subnet-group"
  subnet_ids = [aws_subnet.private_subnet.id]
}

resource "aws_db_instance" "postgres_db" {
  allocated_storage       = 20
  engine                  = "postgres"
  engine_version          = "14"
  instance_class          = "db.t3.micro"
  name                    = "auth_db"
  username                = var.db_username
  password                = var.db_password
  skip_final_snapshot     = true
  db_subnet_group_name    = aws_db_subnet_group.db_subnet_group.name
  vpc_security_group_ids  = [aws_security_group.db_sg.id]
}
