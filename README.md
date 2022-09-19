# batesste-ansible: A collection of useful Ansible roles and playbooks.

## Introduction

This repo contains a bunch of useful Ansible roles and playbooks used
to setup bare-metal and VM servers the way that I like them. This
includes setting up ssh and gnupgp keys, installing packages and
copying in preferred configuration settings.

This repo assumes Ubuntu based distros (though I may add a check for
this in due course) and is currently tested on Ubuntu 22.04 LTS (and
may fail on other versions).

## Example Usage

Assuming a remote server has been setup (and you may want to use
[qemu-minimal][1] to do that) you can enter the target(s) IP address
or hostname and port in playbooks/hosts and run something like:
```
ansible-playbook -i hosts <playbook-name>.yml
```

[1]: https://github.com/sbates130272/qemu-minimal/blob/master/scripts/gen-image
