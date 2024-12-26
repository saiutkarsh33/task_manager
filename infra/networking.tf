resource "aws_vpc" "task_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
}

resource "aws_subnet" "private_subnet" {
  vpc_id                  = aws_vpc.task_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.task_vpc.id
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.task_vpc.id
}

resource "aws_route" "default_public_route" {
  route_table_id         = aws_route_table.public_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

resource "aws_route_table_association" "public_association" {
  route_table_id = aws_route_table.public_rt.id
  subnet_id      = aws_subnet.private_subnet.id
}

resource "aws_security_group" "db_sg" {
  vpc_id = aws_vpc.task_vpc.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.task_vpc.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
