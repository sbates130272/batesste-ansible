# batesste-ansible: A collection of useful Ansible roles and playbooks.

## Introduction

This repo contains a bunch of useful Ansible roles and playbooks used
to setup bare-metal and VM servers the way that I like them. This
includes setting up ssh and gnupgp keys, installing packages and
copying in preferred configuration settings.

This repo assumes Ubuntu 22.04 LTS (jammy) or Ubuntu 24.04 LTS (noble)
and we fail gracefully if we detect any hosts that do not meet this
criteria.

## Setup

### MacOS

Use Homebrew you fools!
```
brew install ansible
```

### Ubuntu 24.04

Use the packaged version:
```
sudo apt install ansible
```

### Ubuntu 22.04

Note that the Ansible that comes as standard in Ubuntu 22.04 is pretty
old (2.10.8). You can either us a [ppa][ref-ansible-ppa] to install a
more recent version or install via pip.
```
python3 -m pip install ansible
```
or in the top-level folder for this repo
```
python3 -m pip install -r requirements.txt
```
We do not support older versions of Ubuntu at this time.

### Common

Install the necessary collections and roles.
```
ansible-galaxy install -r requirements.yml
```

## Example Usage

Assuming a remote server has been setup (and you may want to use
[qemu-minimal][1] to do that) you can enter the target(s) IP address
or hostname and port in playbooks/hosts and run something like:
```
ansible-playbook -i hosts <playbook-name>.yml
```
### AWS Example

Assuming you have setup a basic Ubuntu 22.04 or 24.04 EC2 instance on
AWS you can create a hosts file like this:
```
[awsmachines]
52.11.127.216
[awsmachines:vars]
root_user=ubuntu
username=batesste
```
and then run
```
ansible-playbook -i hosts setup-newmachine.yml --ask-vault-pass
```
You can then enter your ansible-vault password at the prompt and
things should work from there...

### run-ansible

There is also a simple bash script that can call ansible-playbook for
you. You do not have to use this but if you do want to use it you need
to create three local files.

1. A hosts file, call this what you like.
1. sudo-password, a file with the sudo password for the remote user in
it. Not all modes of execution need this.
1. vault-password, a file with the ansible-vault password in it. Never
check this in! Only some roles need this.

You can then invoke a given playbook with the following
```
PLAYBOOK=<playbook-file> HOSTS=<host-file> TARGETS=<target-group> ./run-ansible [<extra-args>]
```
The optional ```extra-args``` will be appended to the call to
ansible-playbook.

## Roles Information

Some of the more involved roles have their own README.md. Please refer
to them for more information about a specific role.

## Playbook and Role Testing

This project contains a [docker](./docker) directory that contains a
Dockerfile and a bash script that allows simple testing of these
playbooks and roles. This is based on [this tutorial][ref-docker-tut]
with some of my own modifications.

You can run a test for any of the roles in this repo by calling the
following from the top-level directory of a given role.
```
MAC_MODE=no CLEAN_UP=yes ../../docker/test-playbook tests/test.yml
```
This runs the test playbook in the ```tests/test.yml``` file using a
docker container based on Ubuntu Noble. You can change to
```MAC_MODE=yes``` when running on Mac OS X and ```CLEAN_UP=no``` if
you want to leave the container running for debug purposes.

## Useful Ansible Commands

As this repository has developed we have come across some very useful
Ansible commands that we include here for reference.

```
ansible -m ansible.builtin.setup --tree /tmp/facts -i hosts localmachines
```
This parses a local inventory file called ```hosts``` and gathers
facts on all the machines in the localmachines section. It then
records those facts in a JSON structure in ```/tmp/facts/``` indexed
by target machine name.

[1]: https://github.com/sbates130272/qemu-minimal/blob/master/scripts/gen-image
[ref-ansible-ppa]: https://launchpad.net/~ansible/+archive/ubuntu/ansible
[ref-docker-tut]: https://dev.to/pencillr/test-ansible-playbooks-using-docker-ci0