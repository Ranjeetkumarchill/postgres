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