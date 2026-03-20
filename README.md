# batesste-ansible: An Ansible collection of roles.

## Introduction

This repo contains an Ansible collection (`sbates130272.batesste`) of
roles used to setup bare-metal and VM servers the way that I like them.
This includes setting up ssh and GnuPG keys, installing packages and
copying in preferred configuration settings. The repo also ships
example playbooks in `playbooks/` but these are not included in the
published Galaxy collection artifact.

This repo supports Ubuntu 24.04 LTS (noble) and 26.04 LTS (resolute), and we
fail gracefully if we detect any hosts that do not meet this criteria.

## Installing the Collection

To use these roles in another project, install the collection from Ansible
Galaxy:

```
ansible-galaxy collection install sbates130272.batesste
```

Then reference roles using the fully qualified collection name (FQCN):

```yaml
- hosts: servers
  roles:
    - role: sbates130272.batesste.grafana_setup
    - role: sbates130272.batesste.docker_setup
      docker_setup_users:
        - myuser
```

Or add it to your project's `requirements.yml`:

```yaml
collections:
  - name: sbates130272.batesste
    version: ">=1.0.0"
```

## Development Setup

### MacOS

Use Homebrew you fools!

```
brew install ansible
```

### Ubuntu 24.04 / 26.04

Use the packaged version:

```
sudo apt install ansible
```

Or install via pip in the top-level folder for this repo:

```
python3 -m pip install -r requirements.txt
```

### Common

Install Python dependencies (Ansible, ansible-lint, etc.) and then install the
necessary collections:

```
python3 -m pip install -r requirements.txt
ansible-galaxy collection install -r requirements.yml
```

### Local Collection Install

To install the collection from your local checkout (needed for playbooks that
use FQCN role references):

```
ansible-galaxy collection build --force
ansible-galaxy collection install sbates130272-batesste-*.tar.gz --force
```

## Example Usage

The playbooks live in the `playbooks/` directory. Assuming a remote server has
been set up (and you may want to use [qemu-minimal][1] to do that) you can enter
the target(s) IP address or hostname and port in `playbooks/hosts` and run
something like:

```
ansible-playbook -i hosts <playbook-name>.yml
```

### AWS Example

Assuming you have set up a basic Ubuntu 24.04 or 26.04 EC2 instance on AWS you
can create a hosts file like this:

```
[awsmachines]
52.11.127.216
[awsmachines:vars]
root_user=ubuntu
username=batesste
```

and then run:

```
ansible-playbook -i hosts setup-newmachine.yml --ask-vault-pass
```

You can then enter your ansible-vault password at the prompt and things should
work from there.

### AMD / ROCm Example

For AMD machines (ROCm, RDMA, uProf) use the
[setup-amd.yml](./playbooks/setup-amd.yml) playbook. It runs the
`user_setup`, `fave_packages`, `git_setup`, `rdma_setup`,
`rocm_setup`, and `uprof_setup` roles. The `uprof_setup` role
requires the user to download the AMD uProf `.deb` from
[amd.com](https://www.amd.com/en/developer/uprof.html) after
accepting the EULA, and pass its path via the
`uprof_setup_deb_path` variable. Use the same inventory and
`run-ansible` pattern:

```
PLAYBOOK=setup-amd.yml HOSTS=<host-file> TARGETS=<target-group> playbooks/run-ansible
```

### run-ansible

There is a simple bash script at `playbooks/run-ansible` that can call
`ansible-playbook` for you. You do not have to use this but if you do you need
to create three local files:

1. A hosts file, call this what you like. Note there is a
   [hosts-example.yml](./playbooks/hosts-example.yml) file to give you an idea
   of what works.
2. `sudo-password`, a file with the sudo password for the remote user. Not all
   modes of execution need this.
3. `vault-password`, a file with the ansible-vault password in it. Never check
   this in! Only some roles need this.

You can then invoke a given playbook with the following:

```
PLAYBOOK=<playbook-file> HOSTS=<host-file> TARGETS=<target-group> playbooks/run-ansible [<extra-args>]
```

The optional `extra-args` will be appended to the call to `ansible-playbook`.

## Roles Information

Some of the more involved roles have their own README.md. Please refer to them
for more information about a specific role.

## Playbook and Role Testing

Role and playbook testing is done via GitHub Actions. See
[.github/README.md](.github/README.md) for how workflows are generated and
how to run role tests in CI.

## Useful Ansible Commands

As this repository has developed we have come across some very useful Ansible
commands that we include here for reference.

```
ansible -m ansible.builtin.setup --tree /tmp/facts -i hosts localmachines
```

This parses a local inventory file called `hosts` and gathers facts on all the
machines in the `localmachines` section. It then records those facts in a JSON
structure in `/tmp/facts/` indexed by target machine name.

[1]: https://github.com/sbates130272/qemu-minimal/blob/master/scripts/gen-image
