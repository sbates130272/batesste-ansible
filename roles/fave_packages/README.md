# fave_packages

Install a curated set of development and systems packages
on Ubuntu.

## Packages Installed

The role installs the following packages on all supported
platforms:

aspell, bmon, build-essential, cmake, driverctl,
expect, fio, git, gettext-base, git-crypt,
git-extras, gpg-agent, libaio-dev, liburing-dev,
pipx, prometheus-node-exporter,
prometheus-node-exporter-collectors, python-is-python3,
python3, python3-pip, python3-venv, ripgrep, stow,
sysstat, tmux, tree, xfsprogs.

The role installs `uv` and `uvx` from the latest
[astral-sh/uv](https://github.com/astral-sh/uv) GitHub
release into `/usr/local/bin/`. The installed version is
tracked in `/usr/local/bin/.uv_version` and updated
automatically when a newer release is available.

When `fave_packages_ansible_enable` is true (the default),
`ansible` and `ansible-lint` are installed per-user via
`uv tool install`, giving a current version isolated from
system Python. This requires the uv block to have run first.

When `fave_packages_ptop_enable` is true (the default),
`ptop` is installed from the latest
[trentas/ptop](https://github.com/trentas/ptop) GitHub
release into `/usr/local/bin/`. The installed version is
tracked in `/usr/local/bin/.ptop_version` and updated
automatically when a newer release is available.

On Ubuntu noble and resolute the role also installs:
elpa-cmake-mode, elpa-rust-mode, virtiofsd, and
conditionally git-email (when git < 2.43).

## Node Exporter Configuration

After installing `prometheus-node-exporter` the role
deploys `/etc/default/prometheus-node-exporter` with
extra flags controlled by
`fave_packages_node_exporter_extra_args`. By default
this enables the WiFi collector (`--collector.wifi`)
which is disabled upstream.

Override the variable to add more collectors or disable
the WiFi collector:

```yaml
# Enable WiFi and thermal zone collectors
fave_packages_node_exporter_extra_args: >-
  --collector.wifi --collector.thermal_zone

# Disable all extra collectors (use upstream defaults)
fave_packages_node_exporter_extra_args: ""
```

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `fave_packages_ansible_enable` | `true` | Install `ansible` and `ansible-lint` via `uv tool install` |
| `fave_packages_desktop_enable` | `true` | Install `emacs-nox`, `gnuplot`, `mutt` |
| `fave_packages_linux_generic_enable` | `false` | Install `linux-generic` meta-package |
| `fave_packages_node_exporter_enable` | `true` | Install and configure `prometheus-node-exporter` |
| `fave_packages_node_exporter_extra_args` | `--collector.wifi` | Extra CLI flags for `prometheus-node-exporter` |
| `fave_packages_ptop_enable` | `true` | Install `ptop` from GitHub releases |
| `fave_packages_uv_enable` | `true` | Install `uv` and `uvx` from GitHub releases |
| `fave_packages_github_api_token` | `$GITHUB_TOKEN` env | Bearer token for GitHub API release lookups (uv, ptop) |

## Example Playbook

```yaml
---
- name: Install favourite packages
  hosts: all
  roles:
    - sbates130272.batesste.fave_packages
```

## Dependencies

Includes `check_platform` automatically.

## Supported Platforms

- Ubuntu noble (24.04)
- Ubuntu resolute (26.04)

## Note on prometheus-node-exporter

This role installs `prometheus-node-exporter` as part of its default package
list. The `grafana_setup` and `consul_setup` roles also install it independently
so each role remains usable standalone. Running more than one of these roles on
the same host is safe (idempotent), but if you want to manage node-exporter
exclusively through one role, set `grafana_setup_install_node_exporter: false`
and/or remove the package from `fave_packages_packages` as needed.

## License

Apache-2.0

## Author

Stephen Bates (sbates@raithlin.com)
