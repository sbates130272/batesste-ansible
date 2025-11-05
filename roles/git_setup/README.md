# git_setup

Configure git and GitHub CLI (gh) with personal preferences, GPG signing, and authentication.

## Features

- Installs GitHub CLI (`gh`)
- Configures git editor (emacs)
- Sets up user name and email
- Enables GPG commit signing
- Configures GPG agent in `.bashrc`
- Sets default merge behavior (no rebase)
- Sets default branch to "main"
- Syncs GPG keys to remote hosts
- **Optional**: Authenticates GitHub CLI with vault-stored token

## Requirements

- `ansible-galaxy collection install community.general`
- `ansible-galaxy collection install ansible.posix`

## Role Variables

### Required Variables

```yaml
# GPG signing key ID
git_setup_signingkey: CB05CB5CFA5DFD9850BB814DE0C020C1975548AE
```

### Optional Variables

```yaml
# Install GitHub CLI (default: true)
git_setup_install_gh: true

# Enable GitHub CLI authentication (default: false)
git_setup_gh_authenticate: false

# GitHub authentication token (store in vault)
git_setup_gh_token: ""
```

## GitHub CLI Authentication with Vault

To securely authenticate the GitHub CLI using a token stored in Ansible Vault:

### 1. Create a Vault File

Create a vault file to store your GitHub token:

```bash
ansible-vault create group_vars/all/vault.yml
```

Add the following content (when prompted for the vault password):

```yaml
---
vault_github_token: "ghp_your_actual_github_token_here"
```

### 2. Configure Your Playbook

Reference the vaulted token in your playbook or inventory:

```yaml
---
- name: Setup git and GitHub CLI
  hosts: all
  vars:
    git_setup_gh_authenticate: true
    git_setup_gh_token: "{{ vault_github_token }}"
  roles:
    - git_setup
```

### 3. Run with Vault Password

Execute the playbook with the vault password:

```bash
ansible-playbook -i inventory setup.yml --ask-vault-pass
```

Or use a password file:

```bash
ansible-playbook -i inventory setup.yml --vault-password-file ~/.vault_pass.txt
```

### 4. Verification

The role will:
1. Authenticate `gh` with the provided token
2. Verify authentication succeeded with `gh auth status`
3. Display the authentication status
4. Fail the playbook if authentication fails

## Creating a GitHub Token

To create a GitHub Personal Access Token for CLI authentication:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes based on your needs:
   - `repo` - Full control of private repositories
   - `workflow` - Update GitHub Action workflows
   - `admin:org` - Full control of orgs and teams (if needed)
   - `admin:public_key` - Manage public keys (if needed)
4. Generate and copy the token
5. Store it securely in your Ansible vault

## Example Playbook

### Basic Usage (without GitHub CLI auth)

```yaml
---
- name: Configure git
  hosts: all
  roles:
    - git_setup
```

### With GitHub CLI Authentication

```yaml
---
- name: Configure git with GitHub CLI authentication
  hosts: workstations
  vars:
    git_setup_gh_authenticate: true
    git_setup_gh_token: "{{ vault_github_token }}"
  roles:
    - git_setup
```

### Skip GitHub CLI Installation

```yaml
---
- name: Configure git without GitHub CLI
  hosts: servers
  vars:
    git_setup_install_gh: false
  roles:
    - git_setup
```

## Security Notes

- The `git_setup_gh_token` variable should **always** be stored in Ansible Vault
- The authentication task uses `no_log: true` to prevent token exposure in logs
- Never commit the vault file with a plaintext token to version control
- Rotate tokens regularly following security best practices
- Use least-privilege principle when selecting token scopes

## Dependencies

This role depends on the `check_platform` role to verify platform compatibility.

## License

Copyright (c) Stephen Bates, 2022

## Author

Stephen Bates (sbates@raithlin.com)

