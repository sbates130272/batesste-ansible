# tmux_scripts

Install tmux plugins and personal tmux configuration
by cloning the
[tmux-scripts](https://github.com/sbates130272/tmux-scripts)
repository.

## Features

- Adds the tmux-resurrect plugin to `~/.tmux.conf`
- Clones the tmux-scripts repository into `~/.tmux` at a
  pinned SHA

## Role Variables

```yaml
# Force a fresh checkout (default: false)
tmux_scripts_force: false

# Git SHA to checkout
tmux_scripts_sha: a4e649c...
```

## Example Playbook

```yaml
---
- name: Install tmux configuration
  hosts: workstations
  roles:
    - sbates130272.batesste.tmux_scripts
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
