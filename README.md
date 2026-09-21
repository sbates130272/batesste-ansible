# batesste-ansible: An Ansible collection of roles.

[![Collection CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/batesste-ansible-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/batesste-ansible-ci.yml) [![rocm_setup CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/rocm_setup-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/rocm_setup-ci.yml) [![rocm_xio_setup CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/rocm_xio_setup-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/rocm_xio_setup-ci.yml) [![lemonade_setup CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/lemonade_setup-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/lemonade_setup-ci.yml) [![claude_setup CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/claude_setup-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/claude_setup-ci.yml) [![uprof_setup CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/uprof_setup-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/uprof_setup-ci.yml) [![grafana_setup CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/grafana_setup-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/grafana_setup-ci.yml) [![rdma_setup CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/rdma_setup-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/rdma_setup-ci.yml) [![nvmeof_setup CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/nvmeof_setup-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/nvmeof_setup-ci.yml) [![nfs_rdma_setup CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/nfs_rdma_setup-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/nfs_rdma_setup-ci.yml) [![fio_devel CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/fio_devel-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/fio_devel-ci.yml)

[![user_setup CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/user_setup-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/user_setup-ci.yml) [![git_setup CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/git_setup-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/git_setup-ci.yml) [![dotfiles CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/dotfiles-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/dotfiles-ci.yml) [![fave_packages CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/fave_packages-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/fave_packages-ci.yml) [![docker_setup CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/docker_setup-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/docker_setup-ci.yml) [![kernel_setup CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/kernel_setup-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/kernel_setup-ci.yml) [![qemu_setup CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/qemu_setup-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/qemu_setup-ci.yml) [![cloud_setup CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/cloud_setup-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/cloud_setup-ci.yml) [![aws_ec2_setup CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/aws_ec2_setup-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/aws_ec2_setup-ci.yml) [![consul_setup CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/consul_setup-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/consul_setup-ci.yml) [![github_runner CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/github_runner-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/github_runner-ci.yml) [![check_platform CI](https://github.com/sbates130272/batesste-ansible/actions/workflows/check_platform-ci.yml/badge.svg)](https://github.com/sbates130272/batesste-ansible/actions/workflows/check_platform-ci.yml)

[![Ansible Galaxy](https://img.shields.io/badge/galaxy-sbates130272.batesste-blue?logo=ansible)](https://galaxy.ansible.com/ui/repo/published/sbates130272/batesste/) [![GitHub Release](https://img.shields.io/github/v/release/sbates130272/batesste-ansible)](https://github.com/sbates130272/batesste-ansible/releases) [![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

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

The `ansible` package in the Ubuntu 24.04 apt repos is outdated. Use
[pipx](https://pipx.pypa.io/) to install a recent `ansible-core` into an
isolated environment (pipx itself is installed by the `fave_packages` role):

```
sudo apt install pipx
pipx install ansible-core
pipx inject ansible-core ansible-lint
pipx ensurepath
```

Or install via pip in the top-level folder for this repo (suitable for CI
and virtualenvs where system-package isolation is not needed):

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

Roles included from playbooks use short names from `roles/`, but internal
`include_role` calls use the collection FQCN (for example
`sbates130272.batesste.check_platform`). Install collection dependencies
before running any playbook:

```
ansible-galaxy collection install -r requirements.yml
```

To build and install the collection from your checkout:

```
ansible-galaxy collection build --force
ansible-galaxy collection install sbates130272-batesste-*.tar.gz --force -p collections
```

## Example Usage

The unified entry point is [setup.yml](./playbooks/setup/setup.yml). Select a recipe
with `-e setup_recipe=<name>`. Tags are optional filters inside the selected recipe,
for example `--tags rocm_setup`. Example inventory:
[hosts.yml](./inventory/hosts.yml) (a gitignored local override also works for
private lists). For a new host you may use [qemu-minimal][qemu-minimal] to build
an image first.

### User Setup Example

The `newmachine` recipe bootstraps a fresh host: creates the user account,
installs preferred packages, configures git, tmux, mutt, Docker, QEMU, and
more. `user_setup` runs as `root_user` (typically `root` or `ubuntu`); all
subsequent roles run as `username`.

Create a minimal hosts file:

```ini
[mymachines]
192.168.1.10
[mymachines:vars]
root_user=ubuntu
username=batesste
```

Then run:

```
ansible-playbook -i hosts playbooks/setup/setup.yml \
  -e setup_recipe=newmachine \
  -e targets=mymachines \
  --ask-vault-pass
```

Dotfiles are deployed by default. To skip them, pass
`-e user_setup_dotfiles_enable=false`.

See [roles/user_setup/README.md](roles/user_setup/README.md) for the full
variable reference.

### AMD ROCm Example

For AMD machines (ROCm, RDMA, ROCm XIO, uProf, Claude Code) use `setup/setup.yml` with
`-e setup_recipe=amd`. It runs `user_setup`, `fave_packages`,
`nvme_exporter_setup`, `git_setup`, `rdma_setup`, `rocm_setup`,
`rocm_xio_setup`, `uprof_setup`, and `claude_setup`. The `uprof_setup`
role requires the AMD uProf `.deb` from [amd.com][amd-uprof] after accepting the
EULA, and its path via `uprof_setup_deb_path`. Example:

```bash
ansible-playbook playbooks/setup/setup.yml \
  -e setup_recipe=amd \
  -e targets=<group> \
  -e @playbooks/secrets.yml
```

### Other Recipes

`setup/setup.yml` also ships these focused recipes:

| Recipe | Roles run |
| ------ | --------- |
| `nfs_rdma` | `nfs_rdma_setup` |
| `nvmeof` | `nvmeof_setup` |
| `rocm_xio` | `rocm_xio_setup` |

Select them with `-e setup_recipe=<name>` like any other recipe.

### Dotfiles Deployment

[`playbooks/dotfiles/`](playbooks/dotfiles/) is a standalone playbook that
clones and installs [batesste-dotfiles](https://github.com/sbates130272/batesste-dotfiles)
on any SSH-reachable host. It resolves the latest release tag via the GitHub
API by default, optionally unlocks git-crypt secrets, and runs `install.sh`.

Run from `playbooks/dotfiles/`:

```bash
ansible-playbook deploy.yml \
  -e targets=<host> \
  -e @../secrets.yml \
  --vault-password-file ../vault-password
```

Key variables (all in `group_vars/all.yml`):

| Variable | Default | Purpose |
| -------- | ------- | ------- |
| `dotfiles_version` | `latest` | Tag to deploy; `latest` resolves via GitHub API |
| `dotfiles_packages` | `bash git gh` | Space-separated stow packages passed to `install.sh` |
| `dotfiles_bootstrap` | `""` | Passed as `--bootstrap <mode>` to `install.sh`; `proxy` group sets this automatically |
| `dotfiles_force` | `false` | Pass `--force` to `install.sh` |
| `dotfiles_install_prereqs` | `false` | Install git/stow/git-crypt/gnupg via package manager (requires sudo) |

git-crypt unlock requires `vault_git_crypt_key_b64` in `secrets.yml` — export
it from a host where the repo is already unlocked:

```bash
cd ~/.batesste-dotfiles && git-crypt export-key - | base64 -w0
```

### Credential files

Place these in `playbooks/`; never commit them:

- `vault-password` — ansible-vault password; read automatically via `ansible.cfg`
- `sudo-password` — become password; read automatically via `ansible.cfg`
- `secrets.yml` — vault-encrypted extra vars; pass explicitly with `-e @playbooks/secrets.yml`

### Running playbooks

All playbooks are invoked directly with `ansible-playbook` from the repo root.
`ansible.cfg` wires up the inventory, roles path, collections path, vault
password file, and become password file automatically.

```bash
# Bootstrap a new machine
ansible-playbook playbooks/setup/setup.yml \
  -e targets=<host-or-group> \
  -e setup_recipe=newmachine \
  -e @playbooks/secrets.yml

# Weekly maintenance
ansible-playbook playbooks/maintain/homelan-maintain.yml -e @playbooks/secrets.yml
ansible-playbook playbooks/maintain/amd-maintain.yml -e @playbooks/secrets.yml
```

Pass `-e targets=<group>` to override the default target for maintenance
playbooks, or `--limit <host>` to restrict to a single host within the group.

## Roles

Each role ships a `README.md` with variables, requirements, and usage notes.

| Role | Description |
| ---- | ----------- |
| [aws_ec2_setup](roles/aws_ec2_setup/README.md) | AWS EC2 instance configuration helpers |
| [aws_grub](roles/aws_grub/README.md) | GRUB configuration for AWS instances |
| [check_platform](roles/check_platform/README.md) | Assert supported Ubuntu release |
| [claude_setup](roles/claude_setup/README.md) | Install and configure Claude Code via a local proxy |
| [cloud_setup](roles/cloud_setup/README.md) | Cloud provider tools and configuration |
| [consul_setup](roles/consul_setup/README.md) | HashiCorp Consul agent install and configuration |
| [docker_setup](roles/docker_setup/README.md) | Docker engine install and user configuration |
| [eideticom_scripts](roles/eideticom_scripts/README.md) | Eideticom-specific utility scripts |
| [fave_packages](roles/fave_packages/README.md) | Install preferred apt/pip packages |
| [fio_devel](roles/fio_devel/README.md) | Build fio from source for storage benchmarking |
| [git_setup](roles/git_setup/README.md) | Git global config, signing, and dotfiles |
| [github_runner](roles/github_runner/README.md) | GitHub Actions self-hosted runner setup |
| [grafana_setup](roles/grafana_setup/README.md) | Grafana, Prometheus, and Node Exporter stack |
| [hashicorp_repo](roles/hashicorp_repo/README.md) | Add HashiCorp APT repository and GPG key (shared utility role) |
| [kernel_setup](roles/kernel_setup/README.md) | Custom kernel build and install |
| [lemonade_setup](roles/lemonade_setup/README.md) | Lemonade clipboard tool setup |
| [mutt_setup](roles/mutt_setup/README.md) | Mutt email client configuration |
| [nfs_rdma_setup](roles/nfs_rdma_setup/README.md) | NFS over RDMA configuration |
| [nvme_exporter_setup](roles/nvme_exporter_setup/README.md) | NVMe Prometheus exporter |
| [nvmeof_setup](roles/nvmeof_setup/README.md) | NVMe-oF target and initiator setup |
| [qemu_setup](roles/qemu_setup/README.md) | QEMU/KVM hypervisor install and configuration |
| [rdma_interfaces](roles/rdma_interfaces/README.md) | Discover RDMA-capable interfaces and IPv4 addresses (shared utility role) |
| [rdma_setup](roles/rdma_setup/README.md) | RDMA/InfiniBand drivers and tools |
| [rocm_hipfile_setup](roles/rocm_hipfile_setup/README.md) | ROCm hipFile package install |
| [rocm_setup](roles/rocm_setup/README.md) | AMD ROCm stack install and DKMS configuration |
| [rocm_xio_setup](roles/rocm_xio_setup/README.md) | ROCm XIO storage backend setup |
| [tmux_scripts](roles/tmux_scripts/README.md) | tmux configuration and helper scripts |
| [uprof_setup](roles/uprof_setup/README.md) | AMD uProf profiler install |
| [user_setup](roles/user_setup/README.md) | User account, SSH keys, and dotfiles bootstrap |
| [vm_create](roles/vm_create/README.md) | Create and configure local VMs via libvirt |

## Playbook and Role Testing

Role and playbook testing is done via GitHub Actions. See
[.github/README.md](.github/README.md) for how workflows are generated and
how to run role tests in CI.

<!-- References -->

[amd-uprof]: https://www.amd.com/en/developer/uprof.html
[qemu-minimal]: https://github.com/sbates130272/qemu-minimal/blob/master/scripts/gen-image
