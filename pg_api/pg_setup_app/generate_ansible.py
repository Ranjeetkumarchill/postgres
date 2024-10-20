def generate_ansible_playbook(data):
    primary_ip = data.get("primary_ip")
    replica_ips = data.get("replica_ips", [])
    postgres_version = data.get("postgres_version", "14")  
    max_connections = data.get("max_connections", 200) 
    shared_buffers = data.get("shared_buffers", "256MB")

    # Generate Ansible playbook
    ansible_playbook = f"""
---
- name: Configure PostgreSQL
  hosts: all
  become: true
  tasks:
    - name: Install PostgreSQL
      apt:
        name: "postgresql-{postgres_version}, postgresql-contrib, python3-psycopg2"
        state: present
        update_cache: yes

    - name: Configure PostgreSQL to allow replication
      lineinfile:
        path: /etc/postgresql/{postgres_version}/main/postgresql.conf
        regexp: '^{{ item.key }}'
        line: '{{ item.key }} = {{ item.value }}'
      loop:
        - {{ key: "listen_addresses", value: "*" }}
        - {{ key: "wal_level", value: "replica" }}
        - {{ key: "max_wal_senders", value: "10" }}
        - {{ key: "wal_keep_segments", value: "64" }}
        - {{ key: "max_connections", value: "{max_connections}" }}
        - {{ key: "shared_buffers", value: "{shared_buffers}" }}

    - name: Configure authentication for replication
      lineinfile:
        path: /etc/postgresql/{postgres_version}/main/pg_hba.conf
        line: "host    replication     replicator    {primary_ip}/32    md5"
        state: present

    - name: Configure replicas
      lineinfile:
        path: /etc/postgresql/{postgres_version}/main/pg_hba.conf
        line: "host    replication     replicator    {{ item }}/32    md5"
        with_items: {replica_ips}
        state: present

    - name: Reload PostgreSQL configuration
      service:
        name: postgresql
        state: reloaded
"""

    # Write to Ansible playbook file
    with open('ansible/setup_postgres.yml', 'w') as f:
        f.write(ansible_playbook.strip())