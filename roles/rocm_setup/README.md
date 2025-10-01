# AMD ROCm Setup

An Ansible role to install and setup a complete [AMD ROCm][ref-rocm]
environment compatible with AMD [Radeon][ref-radeon] and
[Instinct][ref-instinct] accelerators.

## Overview

This role installs ROCm using [these instructions][ref-install] as a guide.

## Requirements

# Role Variables

See the [defaults file](./defaults/main.yml) for more information on
the variables associated with this file. Note there is also a
[rocm-latest](./files/rocm-latest) script that can be used to detect
the latest version of the `rocm` and `amdgpu` packages.

# Dependencies

# Example Playbook

# Testing

Run the following from the folder this README resides in.
```
ANSIBLE_ROLES_PATH=../ ansible-playbook -i <host_file> ./tests/test.yml
```
There is an [example hosts file](./tests/hosts-example) that users can
use as a template for their testing.

# Author and License Information

See the [meta file](./meta/main.yml) for more information on the
author, licensing and other details.

[ref-rocm]: https://www.amd.com/en/products/software/rocm.html
[ref-radeon]: https://www.amd.com/en/products/graphics/desktops/radeon.html
[ref-instinct]: https://www.amd.com/en/products/accelerators/instinct.html
[ref-install]: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/index.html
