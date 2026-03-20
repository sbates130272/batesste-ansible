# eideticom_scripts

Clone the
[eideticom-scripts](https://github.com/Eideticom/eideticom-scripts)
repository into `~/.local/bin/eideticom-scripts` and add
it to the user's `PATH` via `.bashrc`.

## Features

- Creates `~/.local/bin` if it does not exist
- Clones the eideticom-scripts repo at a pinned SHA
- Adds `~/.local/bin` and the scripts directory to
  `PATH` in `.bashrc`

## Role Variables

```yaml
# Force a fresh checkout (default: false)
eideticom_scripts_force: false

# Git SHA to checkout
eideticom_scripts_sha: b39c2d7...
```

## Example Playbook

```yaml
---
- name: Install Eideticom scripts
  hosts: workstations
  roles:
    - sbates130272.batesste.eideticom_scripts
```

## Notes

The clone step is gated on `username == 'batesste'`
because the repository uses SSH authentication. Override
or remove this condition if you have access to the repo.

## Dependencies

Includes `check_platform` automatically.

## Supported Platforms

- Ubuntu noble (24.04)
- Ubuntu resolute (26.04)

## License

Apache-2.0

## Author

Stephen Bates (sbates@raithlin.com)
