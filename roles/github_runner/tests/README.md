# github_runner Role Tests

This directory contains tests for the `github_runner` role.

## Overview

The test playbook configures an ephemeral GitHub Actions runner on the test host. Because GitHub runner tokens are sensitive and repository-specific, this test requires a valid registration token to run.

## Local Testing

### Prerequisites

1. Generate a runner registration token from GitHub:
   - For repository runners: Go to repository Settings → Actions → Runners → New self-hosted runner
   - For organization runners: Go to Organization Settings → Actions → Runners → New runner
   - Copy the registration token (valid for 1 hour)

2. Export the token as an environment variable:

```bash
export GITHUB_RUNNER_TOKEN="your_registration_token_here"
export GITHUB_REPOSITORY_URL="https://github.com/yourusername/yourrepo"
```

### Running the Test

```bash
cd roles/github_runner
ansible-playbook -i tests/hosts tests/test.yml
```

### Test Behavior

The test will:
1. Install the GitHub runner software
2. Register an ephemeral runner with your repository/organization
3. Start the runner as a systemd service
4. The runner will appear in your GitHub repository/organization Settings → Actions → Runners

**Note**: Ephemeral runners are automatically removed after completing one job, so they're ideal for testing.

### Verification Commands

```bash
# Check runner service status
sudo systemctl status github-runner

# View runner logs
sudo journalctl -u github-runner -f

# Check runner configuration
cat /opt/github-runner/.runner

# Verify runner is connected
sudo systemctl is-active github-runner
```

### Cleanup

The ephemeral runner will automatically remove itself after running one job. To manually clean up:

```bash
# Stop the service
sudo systemctl stop github-runner

# Remove runner configuration (requires token)
cd /opt/github-runner
sudo -u github-runner ./config.sh remove --token YOUR_TOKEN

# Remove service and files
sudo systemctl disable github-runner
sudo rm /etc/systemd/system/github-runner.service
sudo rm -rf /opt/github-runner
sudo userdel github-runner
```

## CI Testing

The CI workflow for this role requires a GitHub runner registration token. There are two approaches:

### Approach 1: Skip Runner Registration in CI (Current)

The test checks if `GITHUB_RUNNER_TOKEN` is available and gracefully skips the runner registration if not. This allows the CI to validate:
- Package installation
- User creation
- Directory setup
- Service file creation
- Basic Ansible syntax and linting

### Approach 2: Use GitHub Secrets for Full CI Testing

To enable full testing in CI:

1. Generate a long-lived Personal Access Token with `repo` or `admin:org` scope
2. Add it as a GitHub secret: `GITHUB_RUNNER_TOKEN`
3. Update the CI workflow to pass the secret to the test

**Security Warning**: Using PATs for runner registration in CI can be risky. Consider:
- Using short-lived tokens
- Limiting token scope to test repositories only
- Using ephemeral runners (auto-removed after job)
- Implementing proper secret rotation

## Test Scenarios

### Scenario 1: Standard Repository Runner

```yaml
github_runner_url: "https://github.com/myorg/myrepo"
github_runner_ephemeral: false
```

### Scenario 2: Ephemeral Runner (CI-friendly)

```yaml
github_runner_url: "https://github.com/myorg/myrepo"
github_runner_ephemeral: true
```

### Scenario 3: Organization Runner with Custom Labels

```yaml
github_runner_url: "https://github.com/myorg"
github_runner_labels: "self-hosted,linux,x64,gpu,cuda"
```

### Scenario 4: Replace Existing Runner

```yaml
github_runner_url: "https://github.com/myorg/myrepo"
github_runner_name: "test-runner"
github_runner_replace: true
```

## Known Issues

1. **Token Expiration**: Registration tokens expire after 1 hour. Generate a fresh token before testing.

2. **Runner Already Exists**: If a runner with the same name already exists, set `github_runner_replace: true` or use a unique name.

3. **Systemd in Docker**: Testing in Docker containers requires special systemd setup. Consider using `molecule` for container-based testing.

4. **Token Permissions**: Ensure your token has the correct permissions:
   - Repository runners: `repo` scope
   - Organization runners: `admin:org` scope

## Troubleshooting

### Test Fails with "Token validation failed"

- Token may have expired (1-hour validity)
- Token may not have correct permissions
- Repository URL may be incorrect

### Runner Doesn't Appear in GitHub UI

- Check service status: `sudo systemctl status github-runner`
- View logs: `sudo journalctl -u github-runner -f`
- Verify network connectivity to `github.com`
- Check firewall allows outbound HTTPS (port 443)

### Permission Denied Errors

- Ensure test is run with sufficient privileges (become: true)
- Check the `github-runner` user exists and has correct permissions
- Verify installation directory ownership

## Additional Resources

- [GitHub Actions Runner Documentation](https://docs.github.com/en/actions/hosting-your-own-runners)
- [Runner Registration API](https://docs.github.com/en/rest/actions/self-hosted-runners)
- [Self-hosted Runner Security](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners#self-hosted-runner-security)

