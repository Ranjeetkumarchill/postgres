from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import json
import os
from .generate_terraform import generate_terraform_code
from .generate_ansible import generate_ansible_playbook

@csrf_exempt
def generate_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
    
        try:
            generate_terraform_code(data)
            # generate_ansible_playbook(data)

            return JsonResponse({"message": "Terraform code generated successfully."}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def plan_infrastructure(request):
    if request.method == 'POST':
        try:
            init_command = "terraform init"
            subprocess.run(init_command.split(), cwd='terraform', check=True)

            terraform_command = "terraform plan"
            subprocess.run(terraform_command.split(), cwd='terraform', check=True)

            return JsonResponse({"message": "Terraform plan executed successfully."}, status=200)
        except subprocess.CalledProcessError as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def apply_infrastructure(request):
    if request.method == 'POST':
        try:
            terraform_apply_command = "terraform apply -auto-approve"
            subprocess.run(terraform_apply_command.split(), cwd='terraform', check=True)
            result = subprocess.run(
                ["terraform", "output", "-json"],
                cwd='terraform',
                capture_output=True,
                text=True,
                check=True
            )

            return JsonResponse({"message": "Infrastructure created successfully.",
                                 }, status=200)
        except subprocess.CalledProcessError as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def ansible_generate_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
    
        try:
            generate_ansible_playbook(data)

            return JsonResponse({"message": "Ansible code generated successfully."}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def run_ansible_playbook(request):
    inventory_file = "inventory.ini"
    if request.method == 'POST':
        try:
            subprocess.run(["ansible-playbook", "-i", inventory_file,"setup_postgres.yml"], cwd='ansible', check=True)

            return JsonResponse({"message": "Ansible playbook executed successfully."}, status=200)
        except subprocess.CalledProcessError as e:
            return JsonResponse({"error": str(e)}, status=500)

