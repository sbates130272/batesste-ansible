# Example: Creating Additional Grafana User

This example shows how to create an additional user `stebates` alongside the default `admin` user.

## Update your inventory file

Edit `hosts-grafana-setup`:

```yaml
monitoring_servers:
  hosts:
    localhost:
      ansible_connection: local
      vault_grafana_setup_password: changeme
      # Enable additional user creation
      grafana_setup_create_user: true
      vault_grafana_setup_user_password: my_user_password_123
  vars:
    ansible_user: stebates
    # Customize the additional user (these use ansible_user by default)
    grafana_setup_user_login: stebates
    grafana_setup_user_name: Stephen Bates
    grafana_setup_user_email: stebates@example.com
    grafana_setup_user_role: Admin  # Can be: Admin, Editor, or Viewer
```

## Run the playbook

```bash
cd /home/stebates/Projects/batesste-ansible/roles/grafana_setup
ANSIBLE_ROLES_PATH=../ ansible-playbook -i hosts-grafana-setup ./tests/test.yml
```

## Login credentials

After running, you'll have two users:

1. **Default admin account:**
   - Username: `admin`
   - Password: `changeme` (value of `vault_grafana_setup_password`)

2. **Your custom user:**
   - Username: `stebates` (value of `grafana_setup_user_login`)
   - Password: `my_user_password_123` (value of `vault_grafana_setup_user_password`)
   - Role: `Admin`

Both users have full admin access (if role is set to Admin).

## Benefits

- **Password management**: Both passwords are automatically synchronized on every playbook run
- **Idempotent**: Safe to run multiple times - updates passwords if they change
- **Flexible roles**: Set the additional user as Admin, Editor, or Viewer
- **Personal account**: Use your own username instead of the generic "admin"

## Security Best Practice

In production, store passwords in Ansible Vault:

```bash
# Create a vault file
ansible-vault create group_vars/monitoring_servers/vault.yml

# Add your passwords:
vault_grafana_setup_password: your_secure_admin_password
vault_grafana_setup_user_password: your_secure_user_password
```

Then remove the passwords from the inventory file and run with:

```bash
ansible-playbook -i hosts-grafana-setup ./tests/test.yml --ask-vault-pass
```

