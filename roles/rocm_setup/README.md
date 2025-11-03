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
rocm_setup_force_version: false

# Add new ROCm version alongside existing installations
# When true: uses version-specific package names (e.g., rocm6.3.0)
#            and adds new repository without replacing old one
# When false: replaces existing ROCm installation with new version
rocm_setup_add_new: false

# User to configure for ROCm access (adds to render group)
rocm_setup_user: rocm_user

# Reboot timeout in seconds
rocm_setup_reboot_timeout: 300

# Windows Subsystem for Linux installation
rocm_setup_wsl_install: false
```

## Version Management

The `rocm_setup_rocm_version` and `rocm_setup_amdgpu_version` variables can be set to:
- `latest` - Uses the [rocm-latest](./files/rocm-latest) script to automatically detect the latest version
- Specific version (e.g., `6.3.0`) - Installs that exact version. Set `rocm_setup_force_version: true` to install an older version.

## Adding vs Replacing ROCm Versions

By default (`rocm_setup_add_new: false`), installing a new ROCm version replaces the existing installation. This is the standard behavior for most systems.

When `rocm_setup_add_new: true`, the role:
- Adds a new repository with a version-specific name (e.g., `rocm-6.3.0`)
- Installs version-specific packages (e.g., `rocm6.3.0` instead of `rocm`)
- Preserves existing ROCm installations
- Allows multiple ROCm versions to coexist on the same system

This is useful for:
- Testing compatibility across different ROCm versions
- Maintaining older applications while developing with newer versions
- Gradual migration from one ROCm version to another

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

## Add New ROCm Version Alongside Existing

```yaml
---
- name: Add ROCm 6.3.0 alongside existing installation
  hosts: amd_hosts
  roles:
    - role: rocm_setup
      vars:
        rocm_setup_rocm_version: "6.3.0"
        rocm_setup_amdgpu_version: "6.3"
        rocm_setup_add_new: true
        rocm_setup_user: myuser
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
