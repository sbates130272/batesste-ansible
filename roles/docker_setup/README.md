# docker_setup

Install and configure Docker CE on Ubuntu. This role
replaces the standalone `geerlingguy.docker` dependency
with a simpler Ubuntu-only implementation.

## Features

- Removes obsolete Docker packages (`docker.io`,
  `podman-docker`, etc.)
- Adds the official Docker apt repository with GPG key
  verification
- Installs Docker CE, CLI, containerd, buildx, and
  compose plugins
- Enables and starts the Docker service
- Optionally adds users to the `docker` group

## Role Variables

```yaml
# Docker edition to install (default: ce)
docker_setup_edition: 'ce'

# List of users to add to the docker group (default: [])
docker_setup_users: []
```

## Example Playbook

```yaml
---
- name: Install Docker
  hosts: all
  roles:
    - role: sbates130272.batesste.docker_setup
      vars:
        docker_setup_users:
          - myuser
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
