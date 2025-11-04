# RDMA Setup

## Overview

This Ansible role configures RDMA/InfiniBand support on Ubuntu systems. It installs the necessary kernel modules, RDMA packages, and provides comprehensive detection and reporting of RDMA-capable devices.

## Features

- Installs and configures RDMA/InfiniBand software stack
- Updates PCI ID database for latest device support
- Deploys and executes `rdma-detect` script for comprehensive device detection
- Reports device information including:
  - Vendor and device IDs
  - Driver name and version
  - Firmware version
  - Link status and speed
  - Network interface mappings
  - MAC addresses
- Saves detection report to configurable location
- Optionally displays RDMA/InfiniBand devices in Message of the Day

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
# Timeout for system reboot (in seconds)
rdma_setup_reboot_timeout: 60

# Location where rdma-detect script outputs its status report
rdma_detect_output_file: /tmp/rdma-detect.status

# Installation location for the rdma-detect script
rdma_detect_script_dest: /usr/local/bin/rdma-detect

# Enable MOTD showing RDMA/InfiniBand devices (Ubuntu 24.04+)
rdma_setup_motd: false
```

## RDMA/InfiniBand Devices MOTD

When `rdma_setup_motd` is set to `true`, the role will:
- Deploy a script to `/etc/update-motd.d/` that displays RDMA devices
- Show device names, vendors, drivers, link states, and speeds
- Automatically detect devices from `/sys/class/infiniband`

This is useful for systems with RDMA or InfiniBand capable network
adapters to see device status at login.

Example output:
```
==========================================
RDMA/InfiniBand Devices
==========================================
Device:  mlx5_0
  Vendor:  Mellanox Technologies
  Driver:  mlx5_core
  Link:    ACTIVE
  Speed:   100 Gb/s

==========================================
```

## Dependencies

- Role: `check_platform` - Validates platform compatibility

## Example Playbook

```yaml
---
- name: Setup RDMA on hosts with MOTD
  hosts: rdma_hosts
  roles:
    - role: rdma_setup
      become: true
      vars:
        rdma_detect_output_file: /var/log/rdma-status.txt
        rdma_setup_motd: true
```

## Accessing RDMA Detection Report

After the role runs, you can access the RDMA detection information:

```yaml
- name: Show RDMA detection report
  ansible.builtin.debug:
    var: rdma_detection_report
```

The report is also saved on the target host at the location specified by `rdma_detect_output_file`.

## Testing

Run the following from the folder this README resides in:

```bash
ANSIBLE_ROLES_PATH=../ ansible-playbook -i <host_file> ./tests/test.yml
```

There is an [example hosts file](./hosts-rdma-setup) that users can use as a template for their testing.

## Installed Packages

The role installs the following packages:
- RDMA core utilities: `rdma-core`, `rdmacm-utils`
- InfiniBand utilities: `ibutils`, `ibverbs-utils`, `infiniband-diags`
- Development libraries: `librdmacm-dev`, `libibverbs-dev`
- Network libraries: `libnl-3-dev`, `libnl-route-3-dev`
- NUMA support: `libnuma-dev`, `numactl`
- Performance testing: `perftest`
- PCI utilities: `pciutils`
- Kernel modules: `linux-modules-extra-{{ ansible_kernel }}`

## Author and License Information

See the [meta file](./meta/main.yml) for more information on the author, licensing and other details.
