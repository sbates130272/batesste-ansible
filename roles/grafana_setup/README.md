# Grafana Setup

## Overview

This Ansible role installs and configures Grafana, Prometheus, and Node Exporter on Ubuntu systems, creating a complete monitoring stack.

## Features

- Installs Grafana from official apt repository
- Installs Prometheus for metrics collection
- Installs Node Exporter for system metrics
- Configures Grafana with admin credentials from Vault
- Automatically synchronizes admin password on every run
- Optional creation of additional users with custom roles
- Automatically configures Prometheus as a datasource in Grafana
- Network discovery for Node Exporters and AMD Device Metrics exporters
- Automatic dashboard provisioning (Node Exporter and AMD GPU)
- Disables default admin password requirement
- Configures Prometheus to scrape local Node Exporter
- Enables and starts all services via systemd
- Automatic service restarts on configuration changes

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
# Grafana configuration
# Note: Grafana's default admin username is always 'admin'
# The password is automatically synchronized after installation
grafana_setup_password: "{{ vault_grafana_setup_password }}"
grafana_setup_port: 3000
grafana_setup_domain: localhost
grafana_setup_root_url: "http://{{ grafana_setup_domain }}:{{ grafana_setup_port }}/"

# Additional user configuration (optional)
grafana_setup_create_user: false
grafana_setup_user_name: "{{ ansible_user }}"
grafana_setup_user_email: "{{ ansible_user }}@localhost"
grafana_setup_user_login: "{{ ansible_user }}"
grafana_setup_user_password: "{{ vault_grafana_setup_user_password | default('') }}"
grafana_setup_user_role: Admin  # Can be: Admin, Editor, or Viewer

# GitHub OAuth configuration (optional)
grafana_setup_github_auth_enabled: false
grafana_setup_github_client_id: "{{ vault_grafana_setup_github_client_id | default('') }}"
grafana_setup_github_client_secret: "{{ vault_grafana_setup_github_client_secret | default('') }}"
grafana_setup_github_allowed_orgs: []
grafana_setup_github_allow_sign_up: true
grafana_setup_github_auto_assign_org_role: Editor

# Prometheus configuration
grafana_setup_prometheus_port: 9090
grafana_setup_prometheus_data_dir: /var/lib/prometheus

# Node exporter configuration
grafana_setup_node_exporter_port: 9100

# AMD Device Metrics Exporter configuration
# https://github.com/ROCm/device-metrics-exporter
grafana_setup_amd_gpu_exporter_port: 2021

# Network discovery configuration
grafana_setup_discover_node_exporters: false
grafana_setup_discover_amd_gpu_exporters: false
grafana_setup_discovery_network: "{{ ansible_default_ipv4.network }}/{{ ansible_default_ipv4.netmask }}"
grafana_setup_discovery_timeout: 2  # HTTP request timeout for verification
grafana_setup_discovery_scan_timeout: 60  # Maximum nmap scan time

# Dashboard provisioning
grafana_setup_provision_node_exporter_dashboard: true
grafana_setup_node_exporter_dashboard_id: 1860
grafana_setup_provision_amd_gpu_dashboard: true
grafana_setup_amd_gpu_dashboard_id: 23434  # AMD Instinct Single Node Dashboard

# Enable/disable components
grafana_setup_install_prometheus: true
grafana_setup_install_node_exporter: true
```

### Required Vault Variables

**For password authentication (default):**

You must define `vault_grafana_setup_password` in your Ansible Vault:

```yaml
vault_grafana_setup_password: your_secure_admin_password
```

**For additional user creation (optional):**

If you enable `grafana_setup_create_user`, define the user's password:

```yaml
vault_grafana_setup_user_password: your_secure_user_password
```

**For GitHub OAuth authentication (optional):**

If you enable GitHub OAuth, define these in your Ansible Vault:

```yaml
vault_grafana_setup_github_client_id: your_github_oauth_client_id
vault_grafana_setup_github_client_secret: your_github_oauth_client_secret
```

## GitHub OAuth Setup

To enable GitHub OAuth authentication:

### 1. Create a GitHub OAuth Application

1. Go to GitHub Settings → Developer settings → OAuth Apps
2. Click "New OAuth App"
3. Fill in the application details:
   - **Application name**: Grafana (or your preferred name)
   - **Homepage URL**: `http://your-server:3000`
   - **Authorization callback URL**: `http://your-server:3000/login/github`
4. Click "Register application"
5. Copy the **Client ID** and **Client Secret**

### 2. Configure Ansible Variables

Add to your inventory or playbook:

```yaml
grafana_setup_github_auth_enabled: true
grafana_setup_root_url: "http://your-server.example.com:3000/"
grafana_setup_github_allowed_orgs:
  - your-github-org
```

Add to your Ansible Vault:

```yaml
vault_grafana_setup_github_client_id: your_client_id_here
vault_grafana_setup_github_client_secret: your_client_secret_here
```

### 3. Run the Playbook

After deployment, users can log in using "Sign in with GitHub".

**Note**: If you restrict access to specific organizations using
`grafana_setup_github_allowed_orgs`, only members of those orgs
can authenticate.

## Dependencies

- Role: `check_platform` - Validates platform compatibility

## Example Playbook

**Basic setup with password authentication:**

```yaml
---
- name: Setup Grafana monitoring stack
  hosts: monitoring_servers
  roles:
    - role: grafana_setup
      vars:
        grafana_setup_password: "{{ vault_grafana_setup_password }}"
```

**Setup with GitHub OAuth authentication:**

```yaml
---
- name: Setup Grafana with GitHub OAuth
  hosts: monitoring_servers
  roles:
    - role: grafana_setup
      vars:
        grafana_setup_domain: grafana.example.com
        grafana_setup_root_url: "https://grafana.example.com/"
        grafana_setup_github_auth_enabled: true
        grafana_setup_github_allowed_orgs:
          - my-company
        grafana_setup_github_auto_assign_org_role: Viewer
```

## Accessing Grafana

After the role runs:
- Grafana: `http://localhost:3000`
  - **With password auth**: Username is `admin` and password is the value
    from `vault_grafana_setup_password`
  - **With GitHub OAuth**: Click "Sign in with GitHub" button
- Prometheus: `http://localhost:9090`
- Node Exporter: `http://localhost:9100/metrics`

### Important: Admin Password Management

Grafana's admin password is automatically synchronized with your configuration:
- On **first install**: Grafana creates the admin user with the configured password
- On **subsequent runs**: The role uses `grafana-cli` to reset the password to match
  your configuration, ensuring consistency

This means you can update `vault_grafana_setup_password` and re-run the playbook
to change the admin password without manual intervention.

## Creating Additional Users

You can create an additional user (besides the default `admin` user) by enabling 
`grafana_setup_create_user`:

```yaml
---
- name: Setup Grafana with additional user
  hosts: monitoring_servers
  roles:
    - role: grafana_setup
      vars:
        grafana_setup_create_user: true
        grafana_setup_user_login: stebates
        grafana_setup_user_name: Stephen Bates
        grafana_setup_user_email: stebates@example.com
        grafana_setup_user_role: Admin  # Can be: Admin, Editor, or Viewer
        grafana_setup_user_password: "{{ vault_grafana_setup_user_password }}"
```

The role will:
- Create the user if it doesn't exist
- Update the password if the user already exists
- Set the appropriate role (Admin, Editor, or Viewer)

This allows you to have both:
- **admin** account (default Grafana admin)
- **Your custom user** (e.g., `stebates`) with a configurable role

Both passwords are managed automatically and can be updated by re-running the playbook.

## Prometheus Data Sources

The role automatically:
1. Configures Prometheus to scrape:
   - **Prometheus itself** - Self-monitoring metrics
   - **Node Exporter** - System metrics (CPU, memory, disk, network)
   - **Grafana** - Grafana's own metrics

2. Adds Prometheus as a datasource in Grafana:
   - Creates the datasource if it doesn't exist
   - Updates the datasource URL if it already exists
   - Sets it as the default datasource
   - Verifies the connection is working

After the role runs, the Prometheus datasource is immediately available for creating dashboards.
No manual configuration needed!

## Network Discovery

The role can automatically discover exporters on your local network:

### Node Exporter Discovery

Enable automatic discovery of Node Exporters:

```yaml
grafana_setup_discover_node_exporters: true
grafana_setup_discovery_network: "192.168.1.0/24"  # Your network CIDR
```

The role will:
- Scan the specified network for hosts with port 9100 open
- Verify each host is responding with valid node exporter metrics
- Add discovered exporters to Prometheus scrape configuration
- Label them with `discovered: 'true'` for easy filtering

### AMD Device Metrics Exporter Discovery

Enable automatic discovery of AMD Device Metrics exporters ([official ROCm exporter](https://github.com/ROCm/device-metrics-exporter)):

```yaml
grafana_setup_discover_amd_gpu_exporters: true
grafana_setup_amd_gpu_exporter_port: 2021
```

The role will:
- Scan the network for hosts with port 2021 open (AMD Device Metrics Exporter default)
- Verify each host is responding with AMD GPU metrics
- Add discovered AMD Device Metrics exporters to Prometheus scrape configuration
- Create a separate `amd_gpu` job in Prometheus

**Note:** The AMD Device Metrics Exporter supports AMD MI100/MI200/MI300 series GPUs

### Requirements for Discovery

- `nmap` package (automatically installed when discovery is enabled)
- Network access to the target hosts
- Exporters must be accessible without authentication

## Dashboard Provisioning

The role automatically provisions dashboards from Grafana.com:

### Node Exporter Dashboard

- **Dashboard ID**: 1860 (Node Exporter Full)
- **URL**: http://localhost:3000/d/node-exporter-full
- Shows: CPU, memory, disk, network metrics for all discovered nodes

### AMD GPU Dashboard

- **Dashboard ID**: 23434 (AMD Instinct Single Node Dashboard)
- **URL**: http://localhost:3000/d/amd-gpu-metrics
- Shows: GPU utilization, temperature, memory, power consumption
- Designed for AMD Device Metrics Exporter metrics

Both dashboards are automatically configured to use the Prometheus datasource
and are ready to use immediately after role execution.

## Security Notes

- The Grafana admin password is stored in Ansible Vault
- Anonymous access is disabled by default
- User signup is disabled
- Basic authentication is enabled
- Consider using HTTPS in production (requires additional configuration)

## Testing

Run the following from the folder this README resides in:

```bash
ANSIBLE_ROLES_PATH=../ ansible-playbook -i hosts-grafana-setup ./tests/test.yml
```

Or to test with your own user:

```bash
ANSIBLE_ROLES_PATH=../ ansible-playbook -i hosts-grafana-setup ./tests/test.yml -e ansible_user=$(whoami)
```

**Note**: Update `vault_grafana_setup_password` in `hosts-grafana-setup` before running.

## Author and License Information

See the [meta file](./meta/main.yml) for more information on the author, licensing and other details.
