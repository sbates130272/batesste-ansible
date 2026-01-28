# AMD ROCm Setup

An Ansible role to install and setup a complete [AMD ROCm][ref-rocm]
environment compatible with AMD [Radeon][ref-radeon] and
[Instinct][ref-instinct] accelerators.

## Overview

This role installs ROCm using [these instructions][ref-install] as a
guide. Note that it is targeted at pure Linux but can also be used to
install on [WSL-based systems][ref-wsl]. Pure Windows installs are not
currently supported.

## Requirements

# Role Variables

Available variables are listed below, along with default values (see [defaults/main.yml](./defaults/main.yml)):

```yaml
# ROCm version to install (use 'latest' for automatic detection)
rocm_setup_rocm_version: latest
rocm_setup_amdgpu_version: latest

# Single file for ROCm APT sources (deb822 format)
rocm_setup_sources_file: /etc/apt/sources.list.d/rocm.sources

# User to configure for ROCm access (adds to render group)
rocm_setup_user: rocm_user

# Reboot timeout in seconds
rocm_setup_reboot_timeout: 300

# Skip reboot steps (useful for CI, containers, or manual control)
rocm_setup_skip_reboot: true

# Windows Subsystem for Linux installation
rocm_setup_wsl_install: false

# Run ROCm checks (rocminfo and HIP compilation)
# Set to false in CI or when no AMD GPUs are present
rocm_setup_run_checks: true

# AMD Device Metrics Exporter for Prometheus
rocm_setup_install_metrics_exporter: true
rocm_setup_metrics_exporter_version: latest
rocm_setup_metrics_exporter_repo_uri: https://repo.radeon.com/device-metrics-exporter/apt/VERSION
rocm_setup_metrics_exporter_port: 5000
rocm_setup_metrics_exporter_config_path: /etc/metrics/config.json
rocm_setup_metrics_exporter_open_firewall: true
```

## Version Management

The `rocm_setup_rocm_version` and `rocm_setup_amdgpu_version` variables can be set to:
- `latest` - Uses the [rocm-latest](./files/rocm-latest) script to automatically detect the latest version
- Specific version (e.g., `6.3.0`) - Installs that exact version.

## Replacing ROCm Versions

Installing a new ROCm version replaces the existing installation. This
is the standard behavior for most systems.

## AMD Device Metrics Exporter

This role can optionally install and configure the [AMD Device Metrics Exporter](https://github.com/ROCm/device-metrics-exporter), which exposes AMD GPU and CPU metrics in Prometheus format. The exporter runs as a systemd service and listens on port 2021 by default.

Features:
- Automatic build from source (latest release or specific version)
- Systemd service configuration with automatic restart
- Health checks to verify the exporter is responding
- Configurable port and installation path
- Automatic installation of Go compiler if needed

To enable:
```yaml
rocm_setup_install_metrics_exporter: true
```

To disable (useful in CI or on systems without AMD hardware):
```yaml
rocm_setup_install_metrics_exporter: false
```

### Network Access for VMs

By default, the exporter binds to `0.0.0.0` (all interfaces), making it accessible from other machines on the LAN. This is particularly useful when:
- The target host is a VM and you want to scrape metrics from the host machine
- You have a centralized Prometheus server monitoring multiple systems
- You want to access metrics from Grafana running on a different machine

The role automatically:
- Configures the exporter to listen on all network interfaces
- Opens the firewall port (2021) if UFW is enabled
- Displays the LAN-accessible URL after installation

To restrict to localhost only:
```yaml
rocm_setup_metrics_exporter_bind_address: 127.0.0.1
rocm_setup_metrics_exporter_open_firewall: false
```

**Important Note for VMs and Systems Without GPUs:**

The AMD Device Metrics Exporter handles missing hardware gracefully:

**Behavior:**
- **With AMD GPUs detected**: Exports full GPU metrics (power, temperature, utilization, etc.)
- **Without GPUs (VM without passthrough)**: Exporter still runs and responds to `/metrics` requests
  - Version 1.3.1+: Omits unsupported/unavailable fields
  - Older versions: Reports unavailable metrics as `0`
  - Logs indicate which fields are unsupported

**Hardware Access:**
- Requires `/dev/kfd` and `/dev/dri` device access for full functionality
- In VMs with GPU passthrough, these devices should be available
- Without passthrough, the exporter runs but reports minimal/no GPU data

**Troubleshooting:**
- Check service status: `systemctl status device-metrics-exporter`
- View logs: `journalctl -u device-metrics-exporter -n 50`
- Verify devices: `ls -la /dev/kfd /dev/dri/`
- Test metrics: `curl http://localhost:2021/metrics`

# Dependencies

This role depends on the `check_platform` role for platform compatibility verification.

# Example Playbook

## Standard Installation (Replace existing ROCm)

```yaml
---
- name: Install ROCm on AMD systems
  hosts: amd_hosts
  roles:
    - role: rocm_setup
      vars:
        rocm_setup_rocm_version: "6.3.0"
        rocm_setup_user: myuser
```

## VM Setup with LAN-Accessible Metrics

```yaml
---
- name: Install ROCm on VM with metrics accessible from host machine
  hosts: amd_vm
  roles:
    - role: rocm_setup
      vars:
        rocm_setup_rocm_version: "6.3.0"
        rocm_setup_user: myuser
        # Enable metrics exporter with LAN access (default)
        rocm_setup_install_metrics_exporter: true
        rocm_setup_metrics_exporter_bind_address: 0.0.0.0
        rocm_setup_metrics_exporter_open_firewall: true
```

After installation, you can access metrics from the host machine or any LAN device:
```bash
# From host machine (replace VM_IP with your VM's IP address)
curl http://VM_IP:2021/metrics

# Example output (when AMD hardware is detected):
# amd_num_gpus 1
# amd_gpu_power_avg{gpu="0"} 150.5
# amd_gpu_current_temperature{gpu="0"} 65.0
```

**Note:** The exporter gracefully handles systems without GPUs:
```bash
# Check if exporter is running and responding
curl http://VM_IP:2021/metrics

# View detailed logs to see what hardware was detected
journalctl -u device-metrics-exporter -n 50

# Example: System without GPUs will show minimal metrics
# The /metrics endpoint will still respond, just with limited data
```

If you prefer not to install the exporter on systems without AMD hardware:
```yaml
rocm_setup_install_metrics_exporter: false
```

# Testing

Run the following from the folder this README resides in.
```
ANSIBLE_ROLES_PATH=../ ansible-playbook -i <host_file> ./tests/test.yml
```
There is an [example hosts file](./hosts-rocm-setup) that users can
use as a template for their testing.

# Author and License Information

See the [meta file](./meta/main.yml) for more information on the
author, licensing and other details.

[ref-rocm]: https://www.amd.com/en/products/software/rocm.html
[ref-radeon]: https://www.amd.com/en/products/graphics/desktops/radeon.html
[ref-instinct]: https://www.amd.com/en/products/accelerators/instinct.html
[ref-install]: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/index.html
[ref-wsl]: https://learn.microsoft.com/en-us/windows/wsl/install
