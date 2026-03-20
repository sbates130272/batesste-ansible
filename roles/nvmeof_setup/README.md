# nvmeof_setup

Configure NVMe over Fabrics (NVMe-oF) targets and
host/initiator connections using kernel configfs.

## Features

- Supports RDMA, TCP, FC, and loop transports
- Configures NVMe-oF targets with subsystems, namespaces,
  and ports via configfs
- Connects NVMe-oF host/initiators to remote targets
- Loads and optionally persists required kernel modules
- Creates a systemd service for target persistence across
  reboots
- Optional RDMA DHCP server/client for direct-connected
  links
- Automatic target IP resolution from interface names
- Cleanup tasks for tearing down existing configuration

## Role Variables

Key variables (see `defaults/main.yml` for full list):

```yaml
# Role mode: 'target' or 'host'
nvmeof_setup_mode: target

# Transport type: rdma, tcp, fc, loop
nvmeof_setup_transport: rdma

# Target IP (used when target_interface is not set)
nvmeof_setup_target_ip: 192.168.2.1

# Network interface on the target host
nvmeof_setup_target_interface: ""

# Port / service ID
nvmeof_setup_port: 4420

# Subsystem definitions (target mode)
nvmeof_setup_subsystems:
  - name: nvmet-test
    allow_any_host: true
    namespaces:
      - nsid: 1
        device_path: /dev/nvme0n1
        enable: true

# Host connections (host mode)
nvmeof_setup_connections:
  - transport: "{{ nvmeof_setup_transport }}"
    traddr: 192.168.2.2
    trsvcid: 4420
    nqn: nvmet-test

# Cleanup before applying (default: false)
nvmeof_setup_cleanup: false

# Create systemd service (default: true)
nvmeof_setup_create_service: true
```

## Example Playbook

```yaml
---
- name: Configure NVMe-oF target
  hosts: targets
  roles:
    - role: sbates130272.batesste.nvmeof_setup
      vars:
        nvmeof_setup_mode: target
        nvmeof_setup_transport: tcp
        nvmeof_setup_target_ip: 10.0.0.1

- name: Connect NVMe-oF hosts
  hosts: initiators
  roles:
    - role: sbates130272.batesste.nvmeof_setup
      vars:
        nvmeof_setup_mode: host
        nvmeof_setup_transport: tcp
        nvmeof_setup_connections:
          - transport: tcp
            traddr: 10.0.0.1
            trsvcid: 4420
            nqn: nvmet-test
```

## Dependencies

Includes `check_platform` automatically.

## Supported Platforms

- Ubuntu noble (24.04)
- Ubuntu resolute (26.04)

## License

Apache-2.0

## Author

Stephen Bates (sbates@raithlin.com)
