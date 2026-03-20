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

# SSH key filename stem (e.g. id_rsa, id_ed25519)
user_setup_ssh_key_name: id_rsa

# Controller-side directory containing the SSH keys
user_setup_ssh_key_src_dir: "{{ lookup('env', 'HOME') }}/.ssh"
```

### Driver Overrides MOTD

When `user_setup_motd` is set to `true`, the role will:
- Install `driverctl` utility
- Deploy a script to `/etc/update-motd.d/` that displays all driver overrides
- Show PCI device addresses, device names (from lspci), and assigned drivers

This is useful for systems where specific drivers have been manually
bound to devices using `driverctl`.

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

By default the role reads SSH keys from `$HOME/.ssh/id_rsa`
(and `.pub`) on the Ansible controller. Override the variables
`user_setup_ssh_key_name` and `user_setup_ssh_key_src_dir` to
use a different key or source directory. For example, to use an
Ed25519 key stored in a custom location:

```yaml
user_setup_ssh_key_name: id_ed25519
user_setup_ssh_key_src_dir: /opt/keys
```

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
