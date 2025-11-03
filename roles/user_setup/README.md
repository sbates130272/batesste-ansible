# user_setup Ansible Role

## Overview

This [Ansible][ansible] role adds a new user (defined in
[defaults][defaultsfile]) to the target system(s) and also sets them up as a
passwordless sudo-er. It also copies over their SSH public-key to
allow for remote login *and* copies their SSH private key to allow
access to things like [GitHub][github].

## Features

- Creates user account with passwordless sudo access
- Configures SSH keys for authentication
- Sets up timezone configuration
- Configures emacs editor
- Optionally displays driver overrides in Message of the Day (MOTD)

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
# Username to create
username: batesste

# System timezone
user_setup_timezone: America/Edmonton

# Enable VM shared filesystem mounting
user_setup_vm_fstab: false

# Enable MOTD showing driver overrides (Ubuntu 24.04+)
user_setup_motd: false
```

### Driver Overrides MOTD

When `user_setup_motd` is set to `true`, the role will:
- Install `driverctl` utility
- Deploy a script to `/etc/update-motd.d/` that displays all driver overrides
- Show PCI device addresses, device names (from lspci), and assigned drivers

This is useful for systems where specific drivers have been manually bound to devices using `driverctl`.

Example output:
```
==========================================
Driver Overrides (driverctl)
==========================================

Device:  0000:01:00.0
  Name:    NVIDIA Corporation GA102 [GeForce RTX 3080]
  Driver:  vfio-pci

Device:  0000:02:00.0
  Name:    Mellanox Technologies MT27800 ConnectX-5
  Driver:  mlx5_core

==========================================
```

## Usage

This role assumes your public SSH key is in ~/.ssh/id_rsa.pub and your
private SSH key is in ~/.ssh/id_rsa. There is an [open issue][oi] to make
this more robust.

## Example Playbook

```yaml
---
- name: Setup user with driver overrides MOTD
  hosts: servers
  roles:
    - role: user_setup
      vars:
        username: myuser
        user_setup_motd: true
```

[ansible]: https://www.ansible.com/
[defaultsfile]: ./defaults/main.yml
[github]: https://github.com/
[oi]: https://github.com/sbates130272/batesste-ansible/issues/18
