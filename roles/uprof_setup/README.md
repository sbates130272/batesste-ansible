# AMD uProf Setup

## Overview

This Ansible role installs the [AMD uProf][uprof] performance analysis
tool on Ubuntu systems. Because AMD uProf requires accepting a EULA
before download, the user must download the `.deb` package ahead of
time and provide its path to the role.

## Features

- Validates the target host has an AMD CPU (can be skipped for CI)
- Copies the user-supplied `.deb` from the Ansible controller to
  the target host
- Installs the package and cleans up the staged file
- Verifies the installation by running `AMDuProfCLI --version`

## Requirements

Download the AMD uProf `.deb` installer from the [AMD uProf download
page][uprof] and set `uprof_setup_deb_path` to the local path of the
file on the Ansible controller.

## Role Variables

Available variables are listed below (defaults in `defaults/main.yml`):

```yaml
# Path to the AMD uProf .deb on the Ansible controller (required).
# uprof_setup_deb_path:

# Remote directory used to stage the .deb before install.
uprof_setup_install_dir: /tmp

# Skip the AMD CPU vendor check (useful for CI or non-AMD hosts).
uprof_setup_skip_amd_check: false
```

## Dependencies

- Role: `check_platform` -- validates platform compatibility

## Example Playbook

```yaml
---
- name: Install AMD uProf on profiling hosts
  hosts: profiling_hosts
  roles:
    - role: uprof_setup
      become: true
      vars:
        uprof_setup_deb_path: /path/to/amduprof_x.y.z_amd64.deb
```

## Testing

Run the following from the folder this README resides in:

```bash
ANSIBLE_ROLES_PATH=../ ansible-playbook -i <host_file> ./tests/test.yml
```

The test playbook builds a dummy `.deb` and stub `AMDuProfCLI` script
so the role can execute end-to-end without a real AMD uProf installer.

## Author and License Information

See the [meta file](./meta/main.yml) for author, licensing and other
details.

<!-- References -->

[uprof]: https://www.amd.com/en/developer/uprof.html
