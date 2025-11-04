# Network Discovery and Dashboard Provisioning

## Overview

The `grafana_setup` role now includes automatic network discovery for exporters and dashboard provisioning from Grafana.com.

## Features

### 1. Node Exporter Discovery

Automatically finds Node Exporters on your network:

```yaml
grafana_setup_discover_node_exporters: true
grafana_setup_discovery_network: "192.168.1.0/24"
grafana_setup_node_exporter_port: 9100
grafana_setup_discovery_scan_timeout: 60  # Max scan time in seconds
```

**How it works:**
1. Uses `nmap` with optimized timing (`-T4`, `--host-timeout 2s`) to scan for port 9100
2. Scan is limited to maximum of 60 seconds (configurable)
3. Verifies each discovered host responds with valid node exporter metrics
4. Adds verified exporters to Prometheus scrape configuration
5. Labels them with `discovered: 'true'` for filtering in Grafana

**Performance:**
- Uses aggressive timing template (`-T4`) for faster scanning
- Per-host timeout of 2 seconds to avoid hanging on dead hosts
- Maximum retry count of 1 to reduce scan time
- Overall scan limited to 60 seconds (default, configurable)

### 2. AMD SMI Exporter Discovery

Automatically finds AMD SMI exporters on your network ([official AMD exporter](https://github.com/amd/amd_smi_exporter)):

```yaml
grafana_setup_discover_amd_gpu_exporters: true
grafana_setup_amd_gpu_exporter_port: 2021  # AMD SMI Exporter default port
grafana_setup_discovery_scan_timeout: 60  # Max scan time in seconds
```

**How it works:**
1. Uses optimized `nmap` to scan for the AMD SMI Exporter port (default: 2021)
2. Scan is limited to maximum of 60 seconds (same timeout as node exporters)
3. Verifies each host is responding with AMD EPYC CPU & GPU metrics
4. Creates a dedicated `amd_gpu` job in Prometheus
5. Labels targets with `group: 'gpus'` and `discovered: 'true'`

**What is AMD SMI Exporter?**
- Official AMD exporter for EPYC CPUs and Datacenter GPUs (MI200, MI300)
- Exports CPU metrics (core energy, socket power, boost limits, PROC_HOT status)
- Exports GPU metrics (power, temperature, clock speeds, utilization, memory)
- Written in Go with AMD SMI library bindings

**Performance:**
- Same optimizations as Node Exporter discovery
- Fast scanning with aggressive timing
- Prevents hanging on networks with many unresponsive hosts

### 3. Dashboard Provisioning

Automatically downloads and provisions dashboards:

**Node Exporter Dashboard:**
- Dashboard ID: 1860
- Name: Node Exporter Full
- URL: http://localhost:3000/d/node-exporter-full
- Metrics: CPU, memory, disk, network for all nodes

**AMD GPU Dashboard:**
- Dashboard ID: 12239
- Name: AMD GPU Metrics
- URL: http://localhost:3000/d/amd-gpu-metrics
- Metrics: GPU utilization, temperature, memory, power

## Configuration Example

```yaml
---
- name: Setup Grafana with discovery
  hosts: monitoring_servers
  roles:
    - role: grafana_setup
      vars:
        # Enable discoveries
        grafana_setup_discover_node_exporters: true
        grafana_setup_discover_amd_gpu_exporters: true
        
        # Configure network
        grafana_setup_discovery_network: "10.0.0.0/24"
        grafana_setup_discovery_timeout: 2
        
        # Custom ports (if needed)
        grafana_setup_node_exporter_port: 9100
        grafana_setup_amd_gpu_exporter_port: 2021  # AMD SMI Exporter default
        
        # Dashboard provisioning (enabled by default)
        grafana_setup_provision_node_exporter_dashboard: true
        grafana_setup_provision_amd_gpu_dashboard: true
```

## Requirements

- `nmap` package (automatically installed when discovery is enabled)
- Network access to target hosts
- Exporters must be accessible without authentication

## Performance Tuning

The default settings are optimized for typical home/lab networks:

```yaml
# Default settings (good for most use cases)
grafana_setup_discovery_scan_timeout: 60      # Total scan time limit
grafana_setup_discovery_timeout: 2            # HTTP verification timeout per host
grafana_setup_discovery_network: "192.168.1.0/24"
```

For **large networks** (e.g., /16 or /8), consider:
- Narrowing the discovery network range
- Increasing `grafana_setup_discovery_scan_timeout` to 120 or 180 seconds
- Running discovery during off-peak hours

For **fast networks** with few hosts, you can:
- Keep the default 60-second timeout
- The scan will complete faster if fewer hosts are present

**Scan behavior:**
- Nmap uses `-T4` (aggressive) timing template
- Each host has a 2-second timeout
- Maximum of 1 retry per port
- Entire scan terminates after `grafana_setup_discovery_scan_timeout` seconds
- Timeout exit (code 124) is treated as success (returns partial results)

## Prometheus Scrape Configuration

The role automatically generates Prometheus configuration with discovered targets:

```yaml
scrape_configs:
  # Node Exporters
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['localhost:9100']
        labels:
          instance: 'MKMSTEBATES01'
          group: 'nodes'
      - targets: ['192.168.1.10:9100']
        labels:
          instance: '192.168.1.10'
          group: 'nodes'
          discovered: 'true'
  
  # AMD SMI Exporters
  - job_name: 'amd_gpu'
    static_configs:
      - targets: ['192.168.1.20:2021']
        labels:
          instance: '192.168.1.20'
          group: 'gpus'
          discovered: 'true'
```

## Benefits

1. **Zero Configuration**: Dashboards are ready immediately after deployment
2. **Automatic Discovery**: No manual target management needed
3. **Idempotent**: Safe to run multiple times, updates existing configuration
4. **Flexible**: Discovery can be enabled/disabled per exporter type
5. **Observable**: Shows discovered targets in playbook output

## Security Considerations

- Network scanning may trigger security alerts on monitored networks
- Ensure your security policies allow `nmap` usage
- Consider restricting discovery to known safe networks
- Exporters should implement their own authentication if needed

