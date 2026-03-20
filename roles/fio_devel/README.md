# fio_devel

Clone the upstream [fio](https://github.com/axboe/fio)
repository, install build dependencies, and build fio
from source. Also clones the companion
[fio-stuff](https://github.com/sbates130272/fio-stuff)
repository with additional tooling.

## Features

- Installs fio build dependencies (libaio-dev,
  liburing-dev, libnuma-dev, libpci-dev, etc.)
- Installs linux perf tools (and AWS-specific kernel
  tools when running on AWS)
- Clones upstream fio at a pinned SHA
- Builds and installs fio into a configurable prefix
- Clones the fio-stuff helper repository

## Role Variables

```yaml
# Force a fresh fio checkout (default: false)
fio_devel_fio_force: false

# Git SHA or tag to checkout for fio
fio_devel_fio_sha: db7fc8d...

# Installation prefix for fio (default: /opt/fio)
fio_devel_fio_install_dir: /opt/fio

# Force a fresh fio-stuff checkout (default: false)
fio_devel_fio_stuff_force: false

# Git SHA or tag to checkout for fio-stuff
fio_devel_fio_stuff_sha: a0e9fcd...
```

## Example Playbook

```yaml
---
- name: Build fio from source
  hosts: dev
  roles:
    - role: sbates130272.batesste.fio_devel
      vars:
        fio_devel_fio_sha: fio-3.38
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
