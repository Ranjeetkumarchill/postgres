def generate_ansible_playbook(data):
    ansible_playbook = f"""
---
- hosts: localhost
  vars_files:
    - secrets.yml

  tasks:
    - name: Connect to PostgreSQL
      postgresql_db:
        name: mydb
        state: present
        login_user: "{{{{ db_user }}}}"
        login_password: "{{{{ db_password }}}}"
        login_host: "{{{{ primary_host }}}}"
        login_port: 5432
        
    - name: Install PostgreSQL
      homebrew:
        name: postgresql@14
        state: present

    - name: Initialize PostgreSQL database
      command: /usr/bin/postgresql14-setup initdb
      when: ansible_hostname == "{{{{primary_host}}}}"

    - name: Start PostgreSQL service
      command: brew services restart postgresql@14
      changed_when: false

    - name: Initialize PostgreSQL database (only on primary)
      command: /usr/local/opt/postgresql@14/bin/initdb /usr/local/var/postgresql@14
      when: inventory_hostname == "primary"
      args:
        creates: /usr/local/var/postgresql@14/PG_VERSION 

    - name: Check replication status on primary
      postgresql_query:
        login_host: "{{{{ primary_host }}}}"
        login_user: "{{{{ db_user }}}}"
        login_password: "{{{{ db_password }}}}"
        db: "{{{{ db_name }}}}"
        query: "SELECT pid, usename, application_name, client_addr, state FROM pg_stat_replication;"
      register: primary_replication_status

    - name: Output primary replication status
      debug:
        var: primary_replication_status

    - name: Check replication lag on primary
      postgresql_query:
        login_host: "{{{{ primary_host }}}}"
        login_user: "{{{{ db_user }}}}"
        login_password: "{{{{ db_password }}}}"
        db: "{{{{ db_name }}}}"
        query: SELECT application_name, client_addr,pg_current_wal_lsn() - replay_lsn AS replication_lag FROM pg_stat_replication;
      register: replication_lag

    - name: Output replication lag
      debug:
        var: replication_lag
    
    - name: Create employees table
      postgresql_query:
        query: >
          CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            position VARCHAR(50)
          );
        db: "{{{{ db_name }}}}"
        login_user: "{{{{ db_user }}}}"
        login_host: "{{{{ primary_host }}}}"
        login_password: "{{{{ db_password }}}}" 
        port: 5432
        autocommit: yes 

    - name: Insert sample data
      postgresql_query:
        query: >
          INSERT INTO employees (name, position)
          SELECT 'Alice', 'Developer'
          WHERE NOT EXISTS (SELECT 1 FROM employees WHERE name = 'Alice')
          UNION ALL
          SELECT 'Bob', 'Designer'
          WHERE NOT EXISTS (SELECT 1 FROM employees WHERE name = 'Bob')
          UNION ALL
          SELECT 'Charlie', 'Manager'
          WHERE NOT EXISTS (SELECT 1 FROM employees WHERE name = 'Charlie');
        db: "{{{{ db_name }}}}"
        login_user: "{{{{ db_user }}}}"
        login_host: "{{{{ primary_host }}}}"
        login_password: "{{{{ db_password }}}}"
        port: 5432
        autocommit: yes

    - name: Verify data consistency between primary and replica
      postgresql_query:
        login_host: "{{{{ replica_host }}}}"
        login_user: "{{{{ db_user }}}}"
        login_password: "{{{{ db_password }}}}"
        db: "{{{{ db_name }}}}"
        query: "SELECT COUNT(*) FROM employees;"
      register: replica_count

    - name: Verify data consistency between primary and replica
      postgresql_query:
        login_host: "{{{{ primary_host }}}}"
        login_user: "{{{{ db_user }}}}"
        login_password: "{{{{ db_password }}}}"
        db: "{{{{ db_name }}}}"
        query: "SELECT COUNT(*) FROM employees;"
      register: primary_count

    - name: Check data consistency
      debug:
        msg: "Primary count: {{{{ primary_count }}}}, Replica count: {{{{ replica_count }}}}"
      when: primary_count != replica_count

    - name: Verify if primary and replica counts match
      fail:
        msg: "Data inconsistency detected: primary count is not equal to replica count."
      when: primary_count != replica_count
"""

    # Write to Ansible playbook file
    with open('ansible/setup_postgres.yml', 'w') as f:
        f.write(ansible_playbook.strip())