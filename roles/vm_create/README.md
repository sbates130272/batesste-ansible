# create_vm Ansible Role

## Overview

This role uses the [virt-install-ubuntu][ref1] script in the
[qemu-minimal][ref2] repo to either create a new VM on the target(s)
or start-up the VM if one with the requested name already exists. It
should auto-magically make sure the target users SSH key is installed
and that the VM in on the default network.

Once this role has executed you can use a command like
```
virsh list --all
```
to see if the VM is installed and if it is running. You can use
something like
```
virsh net-dhcp-leases default
```
to see what IPv4 address has been assigned to the VM. You can ssh into
the machine using something as simple as
```
ssh <vm_name>
```
