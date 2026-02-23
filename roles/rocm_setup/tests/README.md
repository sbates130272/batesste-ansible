# Testing AMD Device Metrics Exporter

This directory contains tests for the `rocm_setup` role, specifically for the AMD Device Metrics Exporter functionality.

## Manual Testing (Recommended)

The AMD Device Metrics Exporter is hardware-dependent and requires AMD EPYC CPUs or MI-series GPUs. Manual testing on real hardware or VMs with GPU passthrough is recommended.

### Prerequisites

- AMD EPYC CPU or AMD MI200/MI300 GPU
- Ubuntu 24.04
- ROCm installed (or will be installed by the role)

### Basic Test

```bash
cd roles/rocm_setup
ansible-playbook -i hosts-rocm-setup ./tests/test.yml
```

### Verify Installation

```bash
# Check service status
systemctl status device-metrics-exporter

# View logs
journalctl -u device-metrics-exporter -n 50

# Test metrics endpoint
curl http://localhost:2021/metrics

# Test from another machine (LAN access)
curl http://VM_IP:2021/metrics
```

### Expected Results

**With AMD Hardware:**
- Service starts successfully
- Metrics endpoint returns GPU/CPU data
- Accessible from other machines on the network (if firewall allows)

**Without AMD Hardware:**
- Service may fail to start (expected)
- Binary is installed and ready
- Will start automatically if hardware becomes available

## Docker Test (Experimental - Not Recommended)

A Docker-based test exists but is **not recommended** because:
- systemd in Docker requires complex configuration
- No AMD hardware available in containers
- Only tests the "no GPU" scenario
- Manual testing on real hardware is more valuable

The Docker test files are kept for reference but may not work reliably.

## Ansible Test (Standard)

For testing without GPU hardware:

```bash
cd roles/rocm_setup
ansible-playbook -i hosts-rocm-setup ./tests/test.yml -e "rocm_setup_install_metrics_exporter=false"
```

## CI/CD Testing

The GitHub Actions workflow automatically tests this role with:
- `rocm_setup_install_metrics_exporter: false` (no hardware in CI)
- `rocm_setup_run_checks: false` (skip GPU-dependent checks)

See `.github/workflows/rocm_setup-ci.yml` for details.

## Test Scenarios

### Scenario 1: Full Installation with GPU
```yaml
---
- hosts: amd_gpu_server
  roles:
    - role: rocm_setup
      vars:
        rocm_setup_rocm_version: "6.3.0"
        rocm_setup_user: myuser
        rocm_setup_install_metrics_exporter: true
```

**Expected:**
- ROCm installed
- Metrics exporter running
- GPU metrics available at `http://IP:2021/metrics`

### Scenario 2: VM Without GPU Passthrough
```yaml
---
- hosts: amd_vm_no_gpu
  roles:
    - role: rocm_setup
      vars:
        rocm_setup_rocm_version: "6.3.0"
        rocm_setup_user: myuser
        rocm_setup_install_metrics_exporter: true
```

**Expected:**
- ROCm installed
- Metrics exporter binary installed
- Service fails to start (no hardware)
- No errors in playbook execution

### Scenario 3: Skip Metrics Exporter
```yaml
---
- hosts: any_host
  roles:
    - role: rocm_setup
      vars:
        rocm_setup_install_metrics_exporter: false
```

**Expected:**
- ROCm installed
- No metrics exporter installed

## Manual Verification Commands

```bash
# Check if exporter binary exists
ls -la /usr/local/bin/amd-metrics-exporter

# Check systemd service file
cat /etc/systemd/system/device-metrics-exporter.service

# Check service status
systemctl status device-metrics-exporter

# Try to start service manually
sudo systemctl start device-metrics-exporter

# Check for AMD devices
ls -la /dev/kfd /dev/dri

# Test metrics (if service is running)
curl http://localhost:2021/metrics | head -20
```

## Network Access Testing

From another machine on the LAN:

```bash
# Replace VM_IP with your target IP
curl http://VM_IP:2021/metrics

# Test with timeout
curl --max-time 5 http://VM_IP:2021/metrics

# Check if port is open
nc -zv VM_IP 2021
```

## Troubleshooting

### Service won't start
```bash
# Check logs
journalctl -u device-metrics-exporter -n 100 --no-pager

# Check for AMD devices
ls -la /dev/kfd /dev/dri

# Verify ROCm installation
rocminfo

# Try running manually
sudo /usr/local/bin/amd-metrics-exporter --port=2021 --address=0.0.0.0
```

### Can't access from LAN
```bash
# Check if service is listening on all interfaces
sudo netstat -tulpn | grep 2021

# Check firewall
sudo ufw status

# Manually allow port
sudo ufw allow 2021/tcp
```

## Documentation

- Main README: [../README.md](../README.md)
- AMD Device Metrics Exporter: https://github.com/ROCm/device-metrics-exporter
- ROCm Documentation: https://rocm.docs.amd.com/
