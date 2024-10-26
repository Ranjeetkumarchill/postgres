# your_app/generate_terraform.py
import os
# import json
def generate_terraform_code(data):
    if not os.path.exists('terraform'):
        os.makedirs('terraform')

    aws_region = data.get("aws_region", "ap-south-1")
    vpc_cidr = data.get("vpc_cidr","10.0.0.0/16") 
    postgres_version = data.get("postgres_version", "14.0")
    instance_type = data.get("instance_type", "db.t3.micro")
    number_of_replicas = data.get("number_of_replicas", 1)
    subnet1_cidr = data.get("subnet1_cidr", "10.0.1.0/24")
    subnet2_cidr = data.get("subnet2_cidr", "10.0.2.0/24")
    master_username = data.get("master_username", "postgres")
    master_password = data.get("master_password", "your_secure_password")
    max_connections = data.get("max_connections", 200)
    shared_buffers = data.get("shared_buffers", "256MB")
    allocated_storage = data.get("allocated_storage", 20)
    backup_retention_period = data.get("backup_retention_period", 7)
    multi_az = data.get("multi_az", False)
    encryption = data.get("encryption", False)
    # tags = data.get("tags", {})

    # Generate main.tf
    main_tf = f"""
provider "aws" {{
  region = "{aws_region}"
  profile= "terraform"
}}

resource "aws_vpc" "main" {{
  cidr_block = "{vpc_cidr}"
}}

resource "aws_subnet" "subnet1" {{
  vpc_id            = aws_vpc.main.id
  cidr_block        = "{subnet1_cidr}"
  availability_zone = "ap-south-1a"
}}

resource "aws_subnet" "subnet2" {{
  vpc_id            = aws_vpc.main.id
  cidr_block        = "{subnet2_cidr}"
  availability_zone = "ap-south-1b"
}}

resource "aws_security_group" "postgres_sg" {{
  vpc_id = aws_vpc.main.id

  ingress {{
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["{subnet1_cidr}","{subnet2_cidr}"] 
  }}

  egress {{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }}
}}

resource "aws_db_subnet_group" "default" {{
  name       = "db_subnet_gp"
  subnet_ids = [aws_subnet.subnet1.id, aws_subnet.subnet2.id]
}}

resource "aws_db_parameter_group" "default" {{
  name   = "my-postgres-parameter-group"
  family = "postgres{postgres_version}"

  parameter {{
    name  = "max_connections"
    value = "{max_connections}"
    apply_method = "pending-reboot"
  }}

  parameter {{
    name  = "shared_buffers"
    value = "{shared_buffers}"
    apply_method = "pending-reboot"
  }}
}}

resource "aws_db_instance" "primary" {{
  identifier              = "primary-db"
  engine                  = "postgres"
  engine_version         = "{postgres_version}"
  instance_class         = "{instance_type}"
  allocated_storage       = {allocated_storage}
  username               = "{master_username}"
  password               = "{master_password}"  
  db_subnet_group_name    = aws_db_subnet_group.default.name
  vpc_security_group_ids   = [aws_security_group.postgres_sg.id]
  multi_az                = false
  storage_encrypted      = {str(encryption).lower()}
  skip_final_snapshot     = true
  backup_retention_period = "{backup_retention_period}"
  backup_window           = "10:00-12:00" 
}}

resource "aws_db_instance" "replica" {{
  identifier              = "replica-db"
  engine                  = "postgres"
  engine_version         = "{postgres_version}"
  instance_class         = "{instance_type}"
  vpc_security_group_ids   = [aws_security_group.postgres_sg.id]
  replicate_source_db     = aws_db_instance.primary.identifier
  skip_final_snapshot     = true
}}

output "primary_db_ip" {{
  value = aws_db_instance.primary.address
}}

output "replica_db_ips" {{
  value = aws_db_instance.replica.address
}}

"""

    # Write to main.tf
    with open('terraform/main.tf', 'w') as f:
        f.write(main_tf.strip())


    variables_tf = """
variable "aws_region" {
description = "AWS region for the DB instances"
type        = string
}

variable "aws_access_key" {
description = "AWS region for the DB instances"
type        = string
}

variable "aws_secret_key" {
description = "AWS region for the DB instances"
type        = string
}

variable "postgres_version" {
description = "PostgreSQL version"
type        = string
}

variable "instance_type" {
description = "DB instance type"
type        = string
}

variable "vpc_cidr" {
description = "vpc cidr"
type        = string
}

variable "number_of_replicas" {
description = "Number of read replicas"
type        = number
}

variable "subnet1_cidr" {
description = "List of subnet ID for DB instances"
type        = string
}

variable "subnet2_cidr" {
description = "List of subnet ID for DB instances"
type        = string
}

variable "master_username" {
description = "Master username for PostgreSQL"
type        = string
}

variable "master_password" {
description = "Master password for PostgreSQL"
type        = string
}

variable "max_connections" {
description = "Maximum number of connections"
type        = number
default     = 200
}

variable "shared_buffers" {
description = "Amount of shared memory"
type        = string
default     = "256MB"
}

variable "allocated_storage" {
description = "Allocated storage in GB"
type        = number
default     = 20
}


variable "backup_retention_period" {
description = "Backup retention period in days"
type        = number
default     = 7
}

variable "multi_az" {
description = "Enable Multi-AZ deployment"
type        = bool
default     = false
}

variable "encryption" {
description = "Enable storage encryption"
type        = bool
default     = false
}

# variable "tags" {
# description = "Tags for the resources"
# type        = map(string)
# }
"""
    with open('terraform/variables.tf', 'w') as f:
        f.write(variables_tf.strip())


    tfvars = f"""
aws_region              = "{data.get('aws_region', 'ap-south-1')}"
aws_access_key          = "{data.get("aws_access_key","dksjalald")}"
aws_secret_key          = "{data.get("aws_secret_key","dksjalalddnks")}"
vpc_cidr                = "{data.get("vpc_cidr","10.0.0.0/16")}"
postgres_version        = "{data.get('postgres_version', '14.0')}"
instance_type           = "{data.get('instance_type', 'db.t3.micro')}"
number_of_replicas      = "{data.get('number_of_replicas', 1)}"
subnet1_cidr             = "{data.get("subnet1_cidr", "10.0.1.0/24")}"
subnet2_cidr             = "{data.get("subnet2_cidr", "10.0.1.0/24")}"
master_username         = "{data.get('master_username', 'postgres')}"
master_password         = "{data.get('master_password', 'your_secure_password')}"
max_connections         = "{data.get('max_connections', 200)}"
shared_buffers          = "{data.get('shared_buffers', '256MB')}"
allocated_storage       = "{data.get('allocated_storage', 20)}"
backup_retention_period = "{data.get('backup_retention_period', 7)}"
multi_az                = "{str(data.get('multi_az', False)).lower()}"
encryption              = "{str(data.get('encryption', False)).lower()}"
# tags                  = "{data.get("tags", {})}
"""
    with open('terraform/terraform.tfvars', 'w') as f:
        f.write(tfvars.strip())