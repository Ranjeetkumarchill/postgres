# PostgreSQL Primary-Read Replica Setup

This project automates the setup of a PostgreSQL primary-read-replica architecture using Terraform and Ansible.
Follow the instructions below to get started.

Prerequisites

1. Set AWS Credentials
    
    Create an IAM user in your AWS account and download the Access Key ID and Secret Access Key.

    Set these AWS credentials in ~/.aws/credentials:
    
        [default]
        aws_access_key_id = YOUR_ACCESS_KEY_ID
        aws_secret_access_key = YOUR_SECRET_ACCESS_KEY

2. Install Terraform

    Install Terraform using the following command:
    
        pip install terraform

3. Install Ansible
    Install Ansible using the command:

        pip install ansible

4. Start the Server
    Run the Django development server with the following command (port is optional):

        python manage.py runserver 8001


# API Usage

1. Generate Terraform Code
 
    Use the following curl command to generate Terraform code:

        curl -X POST http://localhost:8001/api/generate/ \
        -H "Content-Type: application/json" \
        -d '{
            "aws_region": "us-east-1",
            "postgres_version": "14.0",
            "instance_type": "db.t3.micro",
            "number_of_replicas": 2,
            "subnet_ids": ["subnet-xxxxxxxxx"],
            "master_username": "postgres",
            "master_password": "your_secure_password",
            "max_connections": 300,
            "shared_buffers": "512MB",
            "allocated_storage": 20,
            "vpc_security_group_ids": ["sg-xxxxxxxx"],
            "backup_retention_period": 7,
            "multi_az": false,
            "encryption": false,
            "tags": {
                "Environment": "Production"
            }
        }'

2. Plan Terraform

    Run the following command to create a Terraform plan:
    
        curl -X POST http://localhost:8001/api/plan/ -H "Content-Type: application/json" -d '{}'

3. Apply Terraform

    To apply the Terraform configuration, use:
    
        curl -X POST http://localhost:8001/api/apply/ -H "Content-Type: application/json" -d '{}'

4. Generate Ansible Playbook

    To provide data to this you need to get primary_ip and replica_ips from output of terraform apply.
    Generate the Ansible playbook with the following command:
    
        curl -X POST http://localhost:8001/api/ansible-generate/ -H "Content-Type: application/json" -d '{
            "primary_ip": "YOUR_PRIMARY_IP",
            "replica_ips": ["YOUR_REPLICA_IP_1", "YOUR_REPLICA_IP_2"],
            "postgres_version": "14.0",
            "max_connections": 300,
            "shared_buffers": "512MB"
        }'
    
5. Apply Ansible Playbook

    To run the Ansible playbook, execute:
    
        curl -X POST http://localhost:8001/api/run-ansible/ -H "Content-Type: application/json" -d '{}'



