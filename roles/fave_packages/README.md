# fave_packages

Install a curated set of development and systems packages
on Ubuntu.

## Packages Installed

The role installs the following packages in a single apt
transaction:

aspell, bmon, build-essential, cmake, driverctl,
elpa-cmake-mode, elpa-rust-mode, expect, fio, gettext-base,
gh, git, git-crypt, git-extras, gpg-agent, jq, libaio-dev,
liburing-dev, python-is-python3, python3, python3-jinja2,
python3-pip, python3-pytest, python3-venv, ripgrep, shellcheck, stow, sysstat, tmux,
tree, virtiofsd, xfsprogs.

The enable flags below add emacs-nox, gnuplot, mutt,
prometheus-node-exporter, prometheus-node-exporter-collectors,
tmuxinator and linux-generic. `fave_packages_extra_packages`
adds host-specific packages to the same transaction.

The role installs `uv` and `uvx` from the latest
[astral-sh/uv](https://github.com/astral-sh/uv) GitHub
release into `/usr/local/bin/`, and replaces them when
`uv --version` differs from the latest release.

When `fave_packages_ansible_enable` is true (the default),
`ansible`, `ansible-core` and `ansible-lint` (plus `jmespath`)
are installed into one `uv tool` environment for the login user, never
root, even when the caller or the inventory (`ansible_become`)
applies `become` to the role.
This requires `fave_packages_uv_enable`.

uv replaces pipx: the role removes the links pipx left in
`~/.local/bin`, removes `~/.local/share/pipx`, and removes the apt `pipx`, `ansible`,
`ansible-core` and `ansible-lint` packages. On the controller
(`ansible_connection: local`) those removals are skipped while
the play itself runs from a non-uv ansible; the uv install
takes over `~/.local/bin` on that run and the next run
finishes the cleanup.

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
| `fave_packages_ansible_enable` | `true` | Install `ansible`, `ansible-core` and `ansible-lint` via `uv tool install` |
| `fave_packages_desktop_enable` | `true` | Install `emacs-nox`, `gnuplot`, `mutt` |
| `fave_packages_extra_packages` | `[]` | Host-specific apt packages, set in `host_vars` or `group_vars` |
| `fave_packages_linux_generic_enable` | `false` | Install `linux-generic` meta-package |
| `fave_packages_node_exporter_enable` | `true` | Install and configure `prometheus-node-exporter` |
| `fave_packages_node_exporter_extra_args` | `--collector.wifi` | Extra CLI flags for `prometheus-node-exporter` |
| `fave_packages_tmuxinator_enable` | `true` | Install `tmuxinator` |
| `fave_packages_uv_enable` | `true` | Install `uv` and `uvx` from GitHub releases |
| `fave_packages_uv_system_certs` | `false` | Set `system-certs = true` in the login user's `~/.config/uv/uv.toml`, for hosts behind a TLS-inspecting proxy such as ZScaler |
| `fave_packages_github_api_token` | `$GITHUB_TOKEN` env | Bearer token for GitHub API release lookups (uv) |
| `fave_packages_apt_sources_cleanup_enable` | `false` | Remove editor backups and package-manager leftovers from `/etc/apt/sources.list.d` and print a warning listing any `*.disabled` source lists, which are kept (the maintain playbook enables it) |
| `fave_packages_apt_sources_cleanup_patterns` | `*~`, `*.bak`, `*.save`, `*.orig`, `*.distUpgrade`, `*.dpkg-*`, `*.ucf-*` | Glob patterns to remove; `*.list` and `*.sources` files are never removed |

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
and/or set `fave_packages_node_exporter_enable: false` as needed.

## License

Apache-2.0

## Author

Stephen Bates (sbates@raithlin.com)
