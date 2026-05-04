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

The unified entry point is [setup.yml](./playbooks/setup.yml). It contains
every former `setup-*.yml` flow; select one with a **recipe** tag
`--tags recipe_<name>` (see the comments at the top of `setup.yml` for the
list). You can add role tags to limit work inside that recipe, e.g.
`--tags recipe_amd,rocm_setup`. Do not run `setup.yml` without tags unless you
intend to execute every play. Example inventory: [hosts.yml](./playbooks/hosts.yml)
(gitignored `playbooks/hosts` also works for private lists). For a new host you
may use [qemu-minimal][1] to build an image first.

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
ansible-playbook -i hosts setup.yml --tags recipe_newmachine --ask-vault-pass
```

You can then enter your ansible-vault password at the prompt and things should
work from there.

### AMD / ROCm Example

For AMD machines (ROCm, RDMA, uProf) use `setup.yml` with
`--tags recipe_amd`. It runs `user_setup`, `fave_packages`, `git_setup`,
`rdma_setup`, `rocm_setup`, and `uprof_setup`. The `uprof_setup` role
requires the AMD uProf `.deb` from
[amd.com](https://www.amd.com/en/developer/uprof.html) after accepting the
EULA, and its path via `uprof_setup_deb_path`. Example:

```
ansible-playbook -i <host-file> setup.yml -e targets=<group> --tags recipe_amd
```

Or with `run-ansible` (defaults to `recipe_newmachine`; override `TAGS`):

```
TAGS=recipe_amd HOSTS=<host-file> TARGETS=<target-group> playbooks/run-ansible
```

### AWS g4ad + ROCm XIO (automated EC2)

Use [setup.yml](./playbooks/setup.yml) with `--tags recipe_aws_rocm_xio` to
launch a **g4ad** instance (Ubuntu 24.04 noble, one GPU / one NVMe target)
with `amazon.aws`, then run `user_setup`, ROCm, `cloud_setup`, `aws_grub`,
`rocm_hipfile_setup`, and `rocm_xio_setup`.

1. `ansible-galaxy collection install -r requirements.yml` (pulls **amazon.aws**).
   Install the collection from this repo if you use FQCN roles (see **Local
   Collection Install** above).
2. Optional: put EC2 API keys in a YAML file (for example
   `playbooks/vars/vault.yml`) and encrypt with `ansible-vault encrypt`, then
   pass `-e @playbooks/vars/vault.yml` along with `--vault-password-file`, or
   rely on AWS credentials on the control node (env / `~/.aws/config`).
   Example contents:

```yaml
vault_aws_ec2_access_key_id: AKIA…
vault_aws_ec2_secret_access_key: …
```

3. Set account-specific values by editing [hosts.yml](./playbooks/hosts.yml)
   (`all.vars`, `aws_ec2_launch.vars`, `aws_rocm_bootstrap.vars`), or create a
   gitignored `playbooks/vars/local.yml` and merge it at runtime with
   `-e @playbooks/vars/local.yml`. Example `local.yml`:

```yaml
aws_ec2_vpc_subnet_id: "subnet-…"
aws_ec2_key_name: "your-ec2-key-name"
aws_ec2_security_group_ids: ["sg-…"]
aws_ec2_profile: "your-aws-cli-profile"
username: "yourlogin"
aws_ec2_owner_tag: "your-owner-id"
aws_ec2_bootstrap_ansible_host: "203.0.113.10"
aws_ec2_ssh_private_key_file: "{{ lookup('env', 'HOME') }}/.ssh/your-key.pem"
rocm_xio_setup_perf_nvme_controllers: ["/dev/nvme1n1"]
# For Play 2 only (no EC2 API): aws_rocm_skip_ec2_launch: true
```

4. `rocm_setup` reboots after AMDGPU DKMS (`hosts.yml`
   `aws_rocm_bootstrap.vars` sets `rocm_setup_skip_reboot: false`). Shared
   inventory [hosts.yml](./playbooks/hosts.yml) lists `aws_ec2_launch`
   (localhost), `aws_rocm_bootstrap`, and `awsmachines` so `aws_grub` runs
   (same group layout as Play 1 `add_host`), alongside other example groups.
   For YAML inventory, the file must start with `---` as the first line (no
   comment lines above it) or Ansible may fail to parse it.
5. To configure an existing instance without calling the EC2 API, set
   `aws_rocm_skip_ec2_launch: true` in `hosts.yml`, `local.yml`, or pass
   `-e aws_rocm_skip_ec2_launch=true`, or run with `--skip-tags ec2_launch`
   (same inventory).
6. Run from the `playbooks/` directory (see
   [ansible.cfg](./playbooks/ansible.cfg)):

```
ansible-playbook -i hosts.yml setup.yml --tags recipe_aws_rocm_xio \
  --vault-password-file vault-password --become-password-file sudo-password
```

   Add `-e @playbooks/vars/local.yml` (and optional `-e @…/vault.yml`) when you
   keep overrides outside `hosts.yml`.

With `run-ansible`, set `HOSTS=hosts.yml`, `TAGS=recipe_aws_rocm_xio`, and
leave `PLAYBOOK` at the default `setup.yml`; `TARGETS` is unused for this
recipe. For runs that do not need vault or a sudo password file on disk, set
`RUN_ANSIBLE_NO_VAULT=1` and/or `RUN_ANSIBLE_NO_SUDO_PASS=1` (see below).

### run-ansible

There is a simple bash script at `playbooks/run-ansible` that can call
`ansible-playbook` for you. By default it expects `vault-password` and
`sudo-password` in the `playbooks/` directory. To omit the vault file (for
example when no vault is used), set `RUN_ANSIBLE_NO_VAULT=1`. To omit the
become password file (for example when sudo is passwordless), set
`RUN_ANSIBLE_NO_SUDO_PASS=1`.

Otherwise you typically create:

1. A hosts file, call this what you like. The repository ships
   [hosts.yml](./playbooks/hosts.yml) as a combined example inventory (lab
   groups plus AWS ROCm XIO groups).
2. `sudo-password`, a file with the sudo password for the remote user. Not all
   modes of execution need this.
3. `vault-password`, a file with the ansible-vault password in it. Never check
   this in! Only some roles need this.

You can then invoke the unified playbook with the following (defaults shown):

```
TAGS=recipe_newmachine PLAYBOOK=setup.yml HOSTS=<host-file> TARGETS=<target-group> playbooks/run-ansible [<extra-args>]
```

`TAGS` is a comma-separated list passed to `ansible-playbook --tags`. The
optional `extra-args` are appended to the `ansible-playbook` command.

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
