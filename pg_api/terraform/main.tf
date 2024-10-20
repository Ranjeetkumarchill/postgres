provider "aws" {
  region = "us-east-1"
}

resource "aws_db_subnet_group" "default" {
  name       = "my-db-subnet-group"
  subnet_ids = ["subnet-xxxxxxxxx"]
}

resource "aws_security_group" "default" {
  name        = "my-db-security-group"
  description = "Allow access to PostgreSQL"
}

resource "aws_db_parameter_group" "default" {
  name   = "my-postgres-parameter-group"
  family = "postgres14.0"

  parameter {
    name  = "max_connections"
    value = "300"
  }

  parameter {
    name  = "shared_buffers"
    value = "512MB"
  }
}

resource "aws_db_instance" "primary" {
  identifier              = "my-primary-db"
  engine                 = "postgres"
  engine_version         = "14.0"
  instance_class         = "db.t3.micro"
  allocated_storage       = 20
  db_subnet_group_name   = aws_db_subnet_group.default.name
  vpc_security_group_ids  = ["sg-xxxxxxxx"]
  username               = "postgres"
  password               = "your_secure_password"  # Handle securely
  skip_final_snapshot    = true
  parameter_group_name   = aws_db_parameter_group.default.name
  backup_retention_period = 7
  multi_az               = false
  storage_encrypted      = false
  tags                   = {"Environment": "Production"}
}

resource "aws_db_instance" "replica" {
  count                   = 2
  identifier              = "my-replica-db-${count.index + 1}"
  engine                 = "postgres"
  engine_version         = "14.0"
  instance_class         = "db.t3.micro"
  allocated_storage       = 20
  db_subnet_group_name   = aws_db_subnet_group.default.name
  vpc_security_group_ids  = ["sg-xxxxxxxx"]
  replicate_source_db     = aws_db_instance.primary.id
  skip_final_snapshot    = true
}

output "primary_db_ip" {
  value = aws_db_instance.primary.address
}

output "replica_db_ips" {
  value = [for r in aws_db_instance.replica : r.address]
}