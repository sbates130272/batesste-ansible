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
```

**How it works:**
1. Uses `nmap` to scan the specified network for port 9100
2. Verifies each discovered host responds with valid node exporter metrics
3. Adds verified exporters to Prometheus scrape configuration
4. Labels them with `discovered: 'true'` for filtering in Grafana

### 2. AMD GPU / ROCm Exporter Discovery

Automatically finds AMD GPU exporters on your network:

```yaml
grafana_setup_discover_amd_gpu_exporters: true
grafana_setup_amd_gpu_exporter_port: 9400
```

**How it works:**
1. Scans the network for the specified GPU exporter port (default: 9400)
2. Verifies each host is responding with GPU metrics
3. Creates a dedicated `amd_gpu` job in Prometheus
4. Labels targets with `group: 'gpus'` and `discovered: 'true'`

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
        grafana_setup_amd_gpu_exporter_port: 9400
        
        # Dashboard provisioning (enabled by default)
        grafana_setup_provision_node_exporter_dashboard: true
        grafana_setup_provision_amd_gpu_dashboard: true
```

## Requirements

- `nmap` package (automatically installed when discovery is enabled)
- Network access to target hosts
- Exporters must be accessible without authentication

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
  
  # AMD GPU Exporters
  - job_name: 'amd_gpu'
    static_configs:
      - targets: ['192.168.1.20:9400']
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

