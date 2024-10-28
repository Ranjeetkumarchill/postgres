provider "aws" {
  region = "ap-south-1"
  profile= "terraform"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "subnet1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "ap-south-1a"
}

resource "aws_subnet" "subnet2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "ap-south-1b"
}

resource "aws_security_group" "postgres_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.1.0/24","10.0.2.0/24"] 
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_subnet_group" "default" {
  name       = "db_subnet_gp"
  subnet_ids = [aws_subnet.subnet1.id, aws_subnet.subnet2.id]
}

resource "aws_db_parameter_group" "default" {
  name   = "my-postgres-parameter-group"
  family = "postgres14"

  parameter {
    name  = "max_connections"
    value = "30"
    apply_method = "pending-reboot"
  }

  parameter {
    name  = "shared_buffers"
    value = "67108864"
    apply_method = "pending-reboot"
  }
}

resource "aws_db_instance" "primary" {
  identifier              = "primary-db"
  engine                  = "postgres"
  engine_version         = "14"
  instance_class         = "db.t3.micro"
  allocated_storage       = 20
  username               = "postgres"
  password               = "your_secure_password"  
  db_subnet_group_name    = aws_db_subnet_group.default.name
  vpc_security_group_ids   = [aws_security_group.postgres_sg.id]
  multi_az                = false
  storage_encrypted      = false
  skip_final_snapshot     = true
  backup_retention_period = "7"
  backup_window           = "10:00-12:00" 
}

resource "aws_db_instance" "replica" {
  identifier              = "replica-db"
  engine                  = "postgres"
  engine_version         = "14"
  instance_class         = "db.t3.micro"
  vpc_security_group_ids   = [aws_security_group.postgres_sg.id]
  replicate_source_db     = aws_db_instance.primary.identifier
  skip_final_snapshot     = true
}

output "primary_db_ip" {
  value = aws_db_instance.primary.address
}

output "replica_db_ips" {
  value = aws_db_instance.replica.address
}