# qemu_setup Ansible Role

## Overview

This role sets up a target for QEMU and libvirt. This enables
emulation and hypervisor accelerated system and user emulation. It
adds the target user to the necessary groups for permission to run
libvirt.

This role also checks out the HEAD of [qemu-minimal][ref-qm] which is
a lightweight tool for running VMs and creating libvirt DOMs.

## Creating a libvirt VM

Once this task has been run on a given target machine you can create a
libvirt-enabled VM on that machine using the following steps:

1. ssh into the target.
2. cd <user>/Projects/qemu-minimal/libvirt
3. NAME=<vm-name> RELEASE=jammy ./virt-install-ubuntu

This will create a NAT connected VM with name <vm-name> based on the
Ubuntu "Jammy" (22.04) release. Alter RELEASE for other versions (not
all supported yet). Note you can then use ```virsh --edit <vm-name>```
to alter the DOM for this VM to change vCPUs, memory, add NVMe SSDs do
passthru etc.

[ref-qm]: https://github.com/sbates130272/qemu-minimal