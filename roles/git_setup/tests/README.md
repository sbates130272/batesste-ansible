# git_setup Role Tests

## Overview

This directory contains tests for the `git_setup` role that run in CI and can be executed locally.

## Test Coverage

The test playbook (`test.yml`) verifies:
- Git installation and configuration
- GitHub CLI (`gh`) installation
- GitHub CLI authentication with token
- Git config settings (editor, name, email, branch defaults)

## Running Tests Locally

### Prerequisites

- Ansible installed
- Ubuntu (22.04 or 24.04)
- GitHub token (optional, for authentication tests)

### Basic Test (without GitHub authentication)

```bash
cd roles/git_setup
ansible-playbook -i localhost, -c local tests/test.yml \
  -e "git_setup_gh_authenticate=false"
```

### Test with GitHub Authentication

```bash
cd roles/git_setup
export GITHUB_TOKEN="your_github_token_here"
ansible-playbook -i localhost, -c local tests/test.yml
```

## CI Execution

In GitHub Actions CI, the test uses the built-in `GITHUB_TOKEN` that is automatically available to all workflows. This token:
- Is automatically provided by GitHub
- Has repository-scoped permissions
- Requires no manual secret configuration
- Is refreshed for each workflow run

### CI Configuration

The workflow:
1. Checks out the code
2. Installs Ansible and dependencies
3. Sets up SSH keys and GPG directories
4. Passes `GITHUB_TOKEN` as an environment variable
5. Runs the test playbook
6. Verifies git and gh are configured correctly

## Manual Verification

After running the role, verify the setup:

### Check Git Configuration

```bash
git config --global --list
```

Expected output should include:
```
core.editor=emacs
user.name=Stephen Bates
user.email=sbates@raithlin.com
pull.rebase=false
init.defaultBranch=main
```

### Check GitHub CLI Installation

```bash
gh --version
```

### Check GitHub CLI Authentication

```bash
gh auth status
```

Expected output:
```
github.com
  ✓ Logged in to github.com as <username> (<auth_method>)
  ✓ Git operations for github.com configured to use https protocol.
  ✓ Token: *******************
```

### Test GitHub CLI Functionality

```bash
# View your repositories
gh repo list

# Check your profile
gh api user

# View current authentication token info
gh auth status -t
```

## Troubleshooting

### GPG Signing Errors

In CI environments without GPG keys, GPG signing is disabled via:
```yaml
git_setup_enable_gpg_signing: false
```

### Authentication Failures

If `gh auth status` fails:
1. Check token is valid: `echo $GITHUB_TOKEN | wc -c` (should be > 40)
2. Check token has correct permissions
3. Verify network connectivity to github.com
4. Check `gh` version: `gh --version`

### Missing Dependencies

If packages are missing, install manually:
```bash
sudo apt-get update
sudo apt-get install -y gh git gpg-agent
```

## Security Notes

- Tokens are passed via environment variables (not command line)
- `no_log: true` prevents token exposure in Ansible output
- CI uses repository-scoped GitHub token automatically
- Local testing requires your own Personal Access Token
- Never commit tokens to version control

## CI Token Permissions

The GitHub Actions `GITHUB_TOKEN` has these default permissions:
- `contents: read` - Read repository contents
- `metadata: read` - Read repository metadata

These are sufficient for testing authentication but may have limited functionality compared to a full Personal Access Token.

