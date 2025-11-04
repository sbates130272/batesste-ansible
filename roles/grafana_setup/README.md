# Grafana Setup

## Overview

This Ansible role installs and configures Grafana, Prometheus, and Node Exporter on Ubuntu systems, creating a complete monitoring stack.

## Features

- Installs Grafana from official apt repository
- Installs Prometheus for metrics collection
- Installs Node Exporter for system metrics
- Configures Grafana with custom user credentials from Vault
- Disables default admin password requirement
- Configures Prometheus to scrape local Node Exporter
- Enables and starts all services via systemd
- Automatic service restarts on configuration changes

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
# Grafana configuration
grafana_setup_user: "{{ ansible_user }}"
grafana_setup_password: "{{ vault_grafana_setup_password }}"
grafana_setup_port: 3000
grafana_setup_domain: localhost

# Prometheus configuration
grafana_setup_prometheus_port: 9090
grafana_setup_prometheus_data_dir: /var/lib/prometheus

# Node exporter configuration
grafana_setup_node_exporter_port: 9100

# Enable/disable components
grafana_setup_install_prometheus: true
grafana_setup_install_node_exporter: true
```

### Required Vault Variables

You must define `vault_grafana_setup_password` in your Ansible Vault:

```yaml
vault_grafana_setup_password: your_secure_password_here
```

## Dependencies

- Role: `check_platform` - Validates platform compatibility

## Example Playbook

```yaml
---
- name: Setup Grafana monitoring stack
  hosts: monitoring_servers
  roles:
    - role: grafana_setup
      vars:
        grafana_setup_user: "{{ ansible_user }}"
        grafana_setup_password: "{{ vault_grafana_setup_password }}"
```

## Accessing Grafana

After the role runs:
- Grafana: `http://localhost:3000`
  - Username: Value of `grafana_setup_user` (defaults to `ansible_user`)
  - Password: Value from `vault_grafana_setup_password`
- Prometheus: `http://localhost:9090`
- Node Exporter: `http://localhost:9100/metrics`

## Prometheus Data Sources

The role automatically configures Prometheus to scrape:
1. **Prometheus itself** - Self-monitoring metrics
2. **Node Exporter** - System metrics (CPU, memory, disk, network)
3. **Grafana** - Grafana's own metrics

To add Prometheus as a data source in Grafana:
1. Login to Grafana
2. Go to Configuration → Data Sources
3. Add Prometheus data source
4. URL: `http://localhost:9090`
5. Save & Test

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

