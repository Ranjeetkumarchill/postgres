# PostgreSQL Primary-Read Replica Setup

This project automates the setup of a PostgreSQL primary-read-replica architecture using Terraform and Ansible.
Follow the instructions below to get started.

Prerequisites

1. Use Virtual Environment

   use these commands:

       cd /path/to/your/project
       python3 -m venv venv
       source venv/bin/activate

2. Set AWS Credentials
    
    Create an IAM user in your AWS account and download the Access Key ID and Secret Access Key.

    Set these AWS credentials in ~/.aws/credentials:
    
        [default]
        aws_access_key_id = YOUR_ACCESS_KEY_ID
        aws_secret_access_key = YOUR_SECRET_ACCESS_KEY

3. Install Terraform

    Install Terraform using the following command:
    
        pip install terraform

4. Install Ansible
    Install Ansible using the command:

        pip install ansible

5. Start the Server
    Run the Django development server with the following command (port is optional):

        python manage.py runserver 8001


# API Usage

1. Generate Terraform Code
 
    Use the following curl command to generate Terraform code:

        curl -X POST http://localhost:8001/api/generate/ -H "Content-Type: application/json" -d '{            
            "aws_region": "ap-south-1","vpc_cidr": "10.0.0.0/16",
            "postgres_version": "14",
            "instance_type": "db.t3.micro",
            "number_of_replicas": 1,
            "subnet1_cidr": "10.0.1.0/24","subnet2_cidr": "10.0.2.0/24",
            "master_username": "postgres",
            "master_password": "your_secure_password",
            "max_connections": 30,
            "shared_buffers": "67108864",
            "allocated_storage": 20,
            "backup_retention_period": 7,
            "multi_az": false,
            "encryption": false
        }'

2. Plan Terraform

    Run the following command to create a Terraform plan:
    
        curl -X POST http://localhost:8001/api/plan/ -H "Content-Type: application/json" -d '{}'

3. Apply Terraform

    To apply the Terraform configuration, use:
    
        curl -X POST http://localhost:8001/api/apply/ -H "Content-Type: application/json" -d '{}'

   ![Uploading Screenshot 2024-10-29 at 9.51.04 PM.png…]()


5. Generate Ansible Playbook
    
        curl -X POST http://localhost:8001/api/ansible-generate/ -H "Content-Type: application/json" -d '{}'
    
6. Apply Ansible Playbook

    To run the Ansible playbook, execute:
    
        curl -X POST http://localhost:8001/api/run-ansible/ -H "Content-Type: application/json" -d '{}'

![Uploading Screenshot 2024-10-29 at 9.51.42 PM.png…]()


