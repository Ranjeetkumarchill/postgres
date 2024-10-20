from django.urls import path
from .views import generate_code, plan_infrastructure, apply_infrastructure, ansible_generate_code, run_ansible_playbook

urlpatterns = [
    path('generate/', generate_code, name='generate_code'),
    path('plan/', plan_infrastructure, name='plan_infrastructure'),
    path('apply/', apply_infrastructure, name='apply_infrastructure'),
    path('ansible-generate/', ansible_generate_code, name='ansible_generate_code'),
    path('run-ansible/', run_ansible_playbook, name='run_ansible_playbook'),
]
