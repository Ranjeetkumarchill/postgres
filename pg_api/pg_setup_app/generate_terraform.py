# your_app/generate_terraform.py
import os
import json
def generate_terraform_code(data):
    if not os.path.exists('terraform'):
        os.makedirs('terraform')

    aws_region = data.get("aws_region", "us-west-2")
    postgres_version = data.get("postgres_version", "14.0")
    instance_type = data.get("instance_type", "db.t3.micro")
    number_of_replicas = data.get("number_of_replicas", 1)
    subnet_ids = data.get("subnet_ids", [])
    master_username = data.get("master_username", "postgres")
    master_password = data.get("master_password", "your_secure_password")
    max_connections = data.get("max_connections", 200)
    shared_buffers = data.get("shared_buffers", "256MB")
    allocated_storage = data.get("allocated_storage", 20)
    vpc_security_group_ids = data.get("vpc_security_group_ids", [])
    backup_retention_period = data.get("backup_retention_period", 7)
    multi_az = data.get("multi_az", False)
    encryption = data.get("encryption", False)
    tags = data.get("tags", {})

    # Convert subnet_ids and vpc_security_group_ids to Terraform-compatible strings
    subnet_ids_str = ', '.join([f'"{subnet_id}"' for subnet_id in subnet_ids])
    vpc_security_group_ids_str = ', '.join([f'"{sg_id}"' for sg_id in vpc_security_group_ids])
    
    # Generate main.tf
    main_tf = f"""
provider "aws" {{
  region = "{aws_region}"
}}

resource "aws_db_subnet_group" "default" {{
  name       = "my-db-subnet-group"
  subnet_ids = [{subnet_ids_str}]
}}

resource "aws_security_group" "default" {{
  name        = "my-db-security-group"
  description = "Allow access to PostgreSQL"
}}

resource "aws_db_parameter_group" "default" {{
  name   = "my-postgres-parameter-group"
  family = "postgres{postgres_version}"

  parameter {{
    name  = "max_connections"
    value = "{max_connections}"
  }}

  parameter {{
    name  = "shared_buffers"
    value = "{shared_buffers}"
  }}
}}

resource "aws_db_instance" "primary" {{
  identifier              = "my-primary-db"
  engine                 = "postgres"
  engine_version         = "{postgres_version}"
  instance_class         = "{instance_type}"
  allocated_storage       = {allocated_storage}
  db_subnet_group_name   = aws_db_subnet_group.default.name
  vpc_security_group_ids  = [{vpc_security_group_ids_str}]
  username               = "{master_username}"
  password               = "{master_password}"  # Handle securely
  skip_final_snapshot    = true
  parameter_group_name   = aws_db_parameter_group.default.name
  backup_retention_period = {backup_retention_period}
  multi_az               = {str(multi_az).lower()}
  storage_encrypted      = {str(encryption).lower()}
  tags                   = {json.dumps(tags)}
}}

resource "aws_db_instance" "replica" {{
  count                   = {number_of_replicas}
  identifier              = "my-replica-db-${{count.index + 1}}"
  engine                 = "postgres"
  engine_version         = "{postgres_version}"
  instance_class         = "{instance_type}"
  allocated_storage       = {allocated_storage}
  db_subnet_group_name   = aws_db_subnet_group.default.name
  vpc_security_group_ids  = [{vpc_security_group_ids_str}]
  replicate_source_db     = aws_db_instance.primary.id
  skip_final_snapshot    = true
}}

output "primary_db_ip" {{
  value = aws_db_instance.primary.address
}}

output "replica_db_ips" {{
  value = [for r in aws_db_instance.replica : r.address]
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

variable "postgres_version" {
description = "PostgreSQL version"
type        = string
}

variable "instance_type" {
description = "DB instance type"
type        = string
}

variable "number_of_replicas" {
description = "Number of read replicas"
type        = number
}

variable "subnet_ids" {
description = "List of subnet IDs for DB instances"
type        = list(string)
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

variable "vpc_security_group_ids" {
description = "List of security group IDs"
type        = list(string)
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

variable "tags" {
description = "Tags for the resources"
type        = map(string)
}
"""
    with open('terraform/variables.tf', 'w') as f:
        f.write(variables_tf.strip())


    tfvars = f"""
aws_region              = "{data.get('aws_region', 'us-west-2')}"
postgres_version        = "{data.get('postgres_version', '14.0')}"
instance_type           = "{data.get('instance_type', 'db.t3.micro')}"
number_of_replicas      = {data.get('number_of_replicas', 1)}
subnet_ids              = {json.dumps(data.get('subnet_ids', []))}
master_username         = "{data.get('master_username', 'postgres')}"
master_password         = "{data.get('master_password', 'your_secure_password')}"
max_connections         = {data.get('max_connections', 200)}
shared_buffers          = "{data.get('shared_buffers', '256MB')}"
allocated_storage       = {data.get('allocated_storage', 20)}
vpc_security_group_ids  = {json.dumps(data.get('vpc_security_group_ids', []))}
backup_retention_period  = {data.get('backup_retention_period', 7)}
multi_az               = {str(data.get('multi_az', False)).lower()}
encryption             = {str(data.get('encryption', False)).lower()}
tags                   = {json.dumps(data.get('tags', {}))}
"""
    with open('terraform/terraform.tfvars', 'w') as f:
        f.write(tfvars.strip())