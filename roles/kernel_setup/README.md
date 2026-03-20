# kernel_setup

Install Linux kernel build prerequisites and set up a
local kernel source tree with upstream remotes (Linus and
stable).

## Features

- Installs kernel build tools: bison, flex, libelf-dev,
  libssl-dev, libncurses-dev, nasm, pahole, libdw-dev
- Clones the
  [kernel-tools](https://github.com/sbates130272/kernel-tools)
  repository into `~/Projects/kernel`
- Initialises a bare git repository in
  `~/Projects/kernel/src`
- Adds Linus and stable remotes (does not fetch; the
  user can do this later)

## Role Variables

```yaml
# Git SHA for kernel-tools checkout
kernel_setup_tools_sha: d707fb9...

# Force a fresh kernel-tools checkout (default: false)
kernel_setup_tools_force: false

# Force removal and re-init of the src directory
kernel_setup_force: false

# Linus tree remote URL
kernel_setup_linus_remote: >-
  https://git.kernel.org/.../torvalds/linux.git

# Stable tree remote URL
kernel_setup_stable_remote: >-
  https://git.kernel.org/.../stable/linux.git
```

## Example Playbook

```yaml
---
- name: Set up kernel development environment
  hosts: dev
  roles:
    - sbates130272.batesste.kernel_setup
```

## Dependencies

Includes `check_platform` automatically. Requires
`community.general` for `git_config`.

## Supported Platforms

- Ubuntu noble (24.04)
- Ubuntu resolute (26.04)

## License

Apache-2.0

## Author

Stephen Bates (sbates@raithlin.com)
