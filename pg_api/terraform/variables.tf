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