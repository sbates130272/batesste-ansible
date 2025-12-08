
# nvmeof_setup Ansible Role

## Overview

This Ansible role configures NVMe over Fabrics (NVMe-oF) targets and
hosts/initiators on Ubuntu systems. It supports multiple transport types
(RDMA, TCP) and can manage multiple subsystems, namespaces, and ports.

## Features

- **Target Mode**: Configure NVMe-oF targets (storage exporters)
  - Create multiple subsystems with custom NQNs
  - Configure multiple namespaces per subsystem
  - Map namespaces to block devices
  - Support for RDMA and TCP transports
  - Persistent configuration via systemd service

- **Host Mode**: Configure NVMe-oF initiators (storage consumers)
  - Connect to multiple NVMe-oF targets
  - Support for RDMA and TCP transports
  - Automatic module loading

- **General Features**:
  - Automatic kernel module loading and persistence
  - Cleanup of existing configurations
  - Support for both IPv4 and IPv6
  - Configfs-based configuration

## Requirements

- Ubuntu 22.04 (Jammy) or 24.04 (Noble)
- Kernel with NVMe-oF support (linux-modules-extra)
- For RDMA: Working RDMA network stack (see rdma_setup role)
- nvme-cli package

## Role Variables

### Mode Selection

```yaml
# Role mode: 'target' or 'host'
nvmeof_setup_mode: target
```

### Transport Configuration

```yaml
# Transport type: rdma, tcp, fc, loop
nvmeof_setup_transport: rdma

# IP address for target
nvmeof_setup_target_ip: 192.168.2.2

# Port/service ID
nvmeof_setup_port: 4420

# Address family: ipv4, ipv6
nvmeof_setup_addr_family: ipv4
```

### Target Configuration

```yaml
# Subsystems to create
nvmeof_setup_subsystems:
  - name: nvmet-test
    allow_any_host: true
    namespaces:
      - nsid: 1
        device_path: /dev/nvme0n1
        enable: true
      - nsid: 2
        device_path: /dev/nvme1n1
        enable: true

# Ports to create
nvmeof_setup_ports:
  - port_id: 1
    trtype: rdma
    adrfam: ipv4
    traddr: 192.168.2.2
    trsvcid: 4420
    subsystems:
      - nvmet-test
```

### Host Configuration

```yaml
# Connections to establish (host mode)
nvmeof_setup_connections:
  - transport: rdma
    traddr: 192.168.2.2
    trsvcid: 4420
    nqn: nvmet-test
```

### Other Options

```yaml
# Install NVMe CLI tools
nvmeof_setup_install_tools: true

# Load kernel modules
nvmeof_setup_load_modules: true

# Persist modules across reboots
nvmeof_setup_persist_modules: true

# Create systemd service (target mode only)
nvmeof_setup_create_service: true

# Cleanup existing config before applying
nvmeof_setup_cleanup: false
```

## Dependencies

- Role: `check_platform` - Validates platform compatibility
- Role: `rdma_setup` - Required if using RDMA transport

## Example Playbooks

### NVMe-oF Target Setup

```yaml
---
- name: Setup NVMe-oF Target with RDMA
  hosts: nvme_targets
  become: true
  roles:
    - role: nvmeof_setup
      vars:
        nvmeof_setup_mode: target
        nvmeof_setup_transport: rdma
        nvmeof_setup_target_ip: 192.168.2.2
        nvmeof_setup_subsystems:
          - name: nvmet-storage
            allow_any_host: true
            namespaces:
              - nsid: 1
                device_path: /dev/nvme0n1
                enable: true
        nvmeof_setup_ports:
          - port_id: 1
            trtype: rdma
            adrfam: ipv4
            traddr: 192.168.2.2
            trsvcid: 4420
            subsystems:
              - nvmet-storage
```

### NVMe-oF Host/Initiator Setup

```yaml
---
- name: Setup NVMe-oF Host/Initiator
  hosts: nvme_hosts
  become: true
  roles:
    - role: nvmeof_setup
      vars:
        nvmeof_setup_mode: host
        nvmeof_setup_connections:
          - transport: rdma
            traddr: 192.168.2.2
            trsvcid: 4420
            nqn: nvmet-storage
```

### TCP Transport Example

```yaml
---
- name: Setup NVMe-oF Target with TCP
  hosts: nvme_targets
  become: true
  roles:
    - role: nvmeof_setup
      vars:
        nvmeof_setup_mode: target
        nvmeof_setup_transport: tcp
        nvmeof_setup_target_ip: 10.0.0.10
        nvmeof_setup_port: 4420
```

## Testing

Run the following from the folder this README resides in:

```bash
ANSIBLE_ROLES_PATH=../ ansible-playbook -i <host_file> \
  ./tests/test.yml
```

There is an [example hosts file](./hosts-nvmeof-setup) that users can
use as a template for their testing.

## Usage Notes

### Target Mode

1. The role creates a persistent systemd service that will recreate the
   NVMe-oF target configuration on boot
2. Block devices must exist before running the role
3. Use `nvmeof_setup_cleanup: true` to remove existing configuration
4. The configfs hierarchy is: subsystems → namespaces → ports

### Host Mode

1. Ensure RDMA or TCP network connectivity to target
2. The nvme-cli package provides the `nvme` command
3. Use `nvme list` to see connected NVMe-oF devices
4. Use `nvme disconnect -n <nqn>` to manually disconnect

### Cleanup

To remove all NVMe-oF configuration:

```yaml
nvmeof_setup_cleanup: true
```

This will:
- Disconnect all host connections (host mode)
- Remove all subsystems, namespaces, and ports (target mode)
- Leave kernel modules loaded

## Troubleshooting

### Target Issues

```bash
# Check if modules are loaded
lsmod | grep nvmet

# Check configfs structure
ls -la /sys/kernel/config/nvmet/

# View systemd service status
systemctl status nvmeof-target

# Check service logs
journalctl -u nvmeof-target
```

### Host Issues

```bash
# Check if modules are loaded
lsmod | grep nvme

# List NVMe devices
nvme list

# Try manual connection
nvme connect -t rdma --traddr 192.168.2.2 --trsvcid 4420 --nqn nvmet-test

# Check dmesg for errors
dmesg | grep nvme
```

## Author and License Information

See the [meta file](./meta/main.yml) for more information on the
author, licensing and other details.

## References

- [NVMe-oF Documentation](https://nvmexpress.org/developers/nvme-of-specification/)
- [Linux NVMe-oF Target](https://www.kernel.org/doc/html/latest/nvme/nvme-target.html)
- [nvme-cli](https://github.com/linux-nvme/nvme-cli)

