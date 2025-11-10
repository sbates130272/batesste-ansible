# github_runner

Install and configure GitHub self-hosted runners on Linux systems. This role automates the deployment of GitHub Actions runners that can execute workflows on your own infrastructure.

## Features

- Downloads and installs the latest GitHub Actions runner
- Configures runner with repository or organization
- Registers runner with GitHub using authentication token
- Sets up runner as a systemd service
- Supports ephemeral runners (removed after each job)
- Customizable runner labels and groups
- Handles runner updates and replacements
- Secure token handling with `no_log`

## Requirements

- Ubuntu 22.04 (Jammy) or 24.04 (Noble)
- `ansible-galaxy collection install community.general`
- GitHub Personal Access Token or GitHub App token with appropriate permissions

### GitHub Token Permissions

For **repository runners**, your token needs:
- `repo` (Full control of private repositories)

For **organization runners**, your token needs:
- `admin:org` (Full control of orgs and teams)

## Role Variables

### Required Variables

```yaml
# Repository or organization URL
github_runner_url: "https://github.com/myorg/myrepo"
# or
github_runner_url: "https://github.com/myorg"

# GitHub Personal Access Token (store in vault!)
github_runner_token: ""
```

### Optional Variables

```yaml
# Runner version (default: "latest")
github_runner_version: "latest"

# Runner name (default: hostname)
github_runner_name: "{{ ansible_hostname }}"

# Runner labels (default: "self-hosted,linux,x64")
github_runner_labels: "self-hosted,linux,x64,gpu"

# Runner group for enterprise/org runners (default: "Default")
github_runner_group: "Default"

# Work directory (default: "_work")
github_runner_work_directory: "_work"

# Installation directory (default: "/opt/github-runner")
github_runner_install_dir: "/opt/github-runner"

# Service user (default: "github-runner")
github_runner_user: "github-runner"

# Replace existing runner (default: false)
github_runner_replace: false

# Ephemeral mode - runner removed after each job (default: false)
github_runner_ephemeral: false

# Disable automatic updates (default: false)
github_runner_disable_auto_update: false

# Additional config.sh options (default: "")
github_runner_extra_options: ""
```

## Creating a GitHub Token

### For Repository Runners

1. Go to your repository Settings → Settings → Actions → Runners
2. Click "New self-hosted runner" to see registration instructions
3. Create a Personal Access Token:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate new token with `repo` scope
4. Store the token securely in Ansible Vault

### For Organization Runners

1. Go to Organization Settings → Actions → Runners
2. Click "New runner"
3. Create a Personal Access Token with `admin:org` scope
4. Store the token in Ansible Vault

## Securing Tokens with Ansible Vault

**IMPORTANT**: Always store `github_runner_token` in Ansible Vault, never in plaintext!

### Create Vault File

```bash
ansible-vault create group_vars/all/vault.yml
```

Add content:

```yaml
---
vault_github_runner_token: "ghp_your_actual_token_here"
```

### Reference in Playbook

```yaml
---
- name: Setup GitHub runner
  hosts: runners
  vars:
    github_runner_url: "https://github.com/myorg/myrepo"
    github_runner_token: "{{ vault_github_runner_token }}"
  roles:
    - github_runner
```

### Run with Vault

```bash
ansible-playbook -i inventory setup.yml --ask-vault-pass
```

## Example Playbooks

### Basic Repository Runner

```yaml
---
- name: Deploy GitHub runner for repository
  hosts: runners
  vars:
    github_runner_url: "https://github.com/myorg/myrepo"
    github_runner_token: "{{ vault_github_runner_token }}"
  roles:
    - github_runner
```

### Organization Runner with Custom Labels

```yaml
---
- name: Deploy GPU-enabled runners for organization
  hosts: gpu_servers
  vars:
    github_runner_url: "https://github.com/myorg"
    github_runner_token: "{{ vault_github_runner_token }}"
    github_runner_labels: "self-hosted,linux,x64,gpu,cuda"
    github_runner_name: "gpu-runner-{{ ansible_hostname }}"
  roles:
    - github_runner
```

### Ephemeral Runner (Clean Slate for Each Job)

```yaml
---
- name: Deploy ephemeral runners
  hosts: ephemeral_runners
  vars:
    github_runner_url: "https://github.com/myorg/myrepo"
    github_runner_token: "{{ vault_github_runner_token }}"
    github_runner_ephemeral: true
    github_runner_labels: "self-hosted,linux,x64,ephemeral"
  roles:
    - github_runner
```

### Specific Runner Version

```yaml
---
- name: Deploy specific runner version
  hosts: stable_runners
  vars:
    github_runner_url: "https://github.com/myorg/myrepo"
    github_runner_token: "{{ vault_github_runner_token }}"
    github_runner_version: "2.311.0"
  roles:
    - github_runner
```

## Runner Management

### Checking Runner Status

```bash
# Check service status
sudo systemctl status github-runner

# View logs
sudo journalctl -u github-runner -f
```

### Manually Stopping/Starting Runner

```bash
# Stop runner
sudo systemctl stop github-runner

# Start runner
sudo systemctl start github-runner

# Restart runner
sudo systemctl restart github-runner
```

### Removing a Runner

To unregister and remove a runner:

```yaml
---
- name: Remove GitHub runner
  hosts: runner_to_remove
  tasks:
    - name: Stop runner service
      ansible.builtin.systemd:
        name: github-runner
        state: stopped
      become: true

    - name: Remove runner configuration
      ansible.builtin.command:
        cmd: "{{ github_runner_install_dir }}/config.sh remove --token {{ github_runner_token }}"
        chdir: "{{ github_runner_install_dir }}"
      become: true
      become_user: "{{ github_runner_user }}"

    - name: Remove runner installation
      ansible.builtin.file:
        path: "{{ github_runner_install_dir }}"
        state: absent
      become: true

    - name: Remove systemd service
      ansible.builtin.file:
        path: /etc/systemd/system/github-runner.service
        state: absent
      become: true
```

## Using Runners in Workflows

Once deployed, reference your runner in GitHub Actions workflows:

```yaml
name: Build on Self-Hosted Runner
on: [push]

jobs:
  build:
    runs-on: self-hosted
    # Or use specific labels:
    # runs-on: [self-hosted, linux, x64, gpu]
    
    steps:
      - uses: actions/checkout@v4
      - name: Build project
        run: make build
```

## Security Considerations

1. **Token Security**
   - Always use Ansible Vault for tokens
   - Rotate tokens regularly
   - Use least-privilege tokens (repository-scoped when possible)

2. **Runner Security**
   - Self-hosted runners execute arbitrary code from workflows
   - Only use with **private repositories** you trust
   - Consider ephemeral runners for better isolation
   - Review workflow permissions carefully

3. **Network Security**
   - Runners connect outbound to GitHub (no inbound ports needed)
   - Ensure firewall allows HTTPS (443) outbound
   - Consider using runner groups to restrict access

4. **System Security**
   - Runner runs as dedicated `github-runner` user
   - Service includes `NoNewPrivileges=true` hardening
   - Review and harden based on your security requirements

## Troubleshooting

### Runner Not Appearing in GitHub

1. Check service status: `sudo systemctl status github-runner`
2. View logs: `sudo journalctl -u github-runner -f`
3. Verify token has correct permissions
4. Check runner configuration: `cat {{ github_runner_install_dir }}/.runner`

### Runner Offline

1. Check network connectivity to GitHub
2. Restart service: `sudo systemctl restart github-runner`
3. Check for version mismatches
4. Review logs for authentication errors

### Permission Errors

1. Verify `github_runner_user` has correct permissions
2. Check directory ownership: `ls -la {{ github_runner_install_dir }}`
3. Ensure token has required scopes

## Dependencies

This role depends on the `check_platform` role to verify platform compatibility.

## License

Copyright (c) Stephen Bates, 2025

## Author

Stephen Bates (sbates@raithlin.com)

## References

- [GitHub Actions Runner Documentation](https://docs.github.com/en/actions/hosting-your-own-runners)
- [Self-hosted Runner Security](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners#self-hosted-runner-security)

