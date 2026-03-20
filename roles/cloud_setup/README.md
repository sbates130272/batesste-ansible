# cloud_setup

Install and configure cloud CLI tools and credentials.
Currently supports AWS CLI and GitHub CLI.

## Features

- Installs GitHub CLI (`gh`) and pip
- Installs AWS CLI via pip (required for Ubuntu 24.04+
  where the `awscli` deb package was removed)
- Creates `~/.aws/config` from a bundled defaults file
- Templates `~/.aws/credentials` from vault-encrypted
  variables

## Role Variables

### Required Variables (vault-encrypted)

```yaml
cloud_setup_raithlin_access_key_id: !vault |
  ...
cloud_setup_raithin_secret_access_key: !vault |
  ...
```

These should be stored in an Ansible Vault file and
referenced from your inventory or playbook vars.

## Example Playbook

```yaml
---
- name: Configure cloud CLI tools
  hosts: workstations
  roles:
    - sbates130272.batesste.cloud_setup
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
