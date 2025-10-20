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

See the [defaults file](./defaults/main.yml) for more information on
the variables associated with this file. Note there is also a
[rocm-latest](./files/rocm-latest) script that can be used to detect
the latest version of the `rocm` and `amdgpu` packages.

Note that `rocm_setup_version` and `rocm_setup_amdgpu_version` can be
set to `latest`. In this case the [rocm-latest](./files/rocm-latest)
script will be used to set the versions to install. If you do want to
install an older version then set the version variables and also set
`rocm_setup_force_version` to `true`.

# Dependencies

# Example Playbook

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
