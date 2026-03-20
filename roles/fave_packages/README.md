# fave_packages

Install a curated set of development and systems packages
on Ubuntu.

## Packages Installed

The role installs the following packages on all supported
platforms:

aspell, bmon, build-essential, cmake, driverctl,
emacs-nox, expect, fio, git, gnuplot, gpg-agent,
libaio-dev, liburing-dev, linux-generic,
prometheus-node-exporter,
prometheus-node-exporter-collectors, python-is-python3,
python3, python3-pip, python3-venv, mutt, sysstat, tmux,
tree, xfsprogs.

On Ubuntu noble and resolute the role also installs:
elpa-cmake-mode, elpa-rust-mode, virtiofsd, and
conditionally git-email (when git < 2.43).

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

## License

Apache-2.0

## Author

Stephen Bates (sbates@raithlin.com)
