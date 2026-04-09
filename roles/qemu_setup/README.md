# qemu_setup Ansible Role

## Overview

This role sets up a target for QEMU and libvirt. This enables
emulation and hypervisor accelerated system and user emulation. It
adds the target user to the necessary groups for permission to run
QEMU and libvirt.

This role also checks out the HEAD of [qemu-minimal][ref-qm], a lightweight
tool for running VMs and creating libvirt DOMs. To create a VM, you can
either use the instructions below or use the [vm_create][vm-create] role.

## Creating a libvirt VM

Once this task has been run on a given target machine you can create a
libvirt-enabled VM on that machine using the following steps:

1. ssh into the target.
2. cd <user>/Projects/qemu-minimal/libvirt
3. NAME=<vm-name> RELEASE=<noble|resolute> ./virt-install-ubuntu

This creates a NAT-connected VM named <vm-name> based on either Ubuntu
"Noble" (24.04) or "Resolute" (26.04). Use RELEASE=noble for Ubuntu
24.04 and RELEASE=resolute for Ubuntu 26.04. Alter RELEASE for other
versions (not all supported yet). You can then run
```virsh --edit <vm-name>``` to alter the domain for this VM, such as
changing vCPUs, memory, or adding NVMe passthrough devices. See the
virt-install-ubuntu script for additional options.

<!-- References -->

[ref-qm]: https://github.com/sbates130272/qemu-minimal
[vm-create]: ../roles/vm_create
