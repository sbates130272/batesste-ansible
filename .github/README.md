# GitHub Actions Workflows

This directory contains automated CI/CD workflows for the batesste-ansible repository.

## Overview

- **batesste-ansible-ci.yml**: Main CI workflow that runs linting, spelling, and core tests
- **Individual role workflows**: Auto-generated workflows for each role with tests
- **generate-workflows.py**: Python script that automatically generates role-specific workflows

## Automated Workflow Generation

Individual role workflows are automatically generated using `generate-workflows.py`. This ensures consistency across all role tests and makes it easy to add CI for new roles.

### How It Works

1. The script scans the `roles/` directory for any role that has a `tests/` subdirectory
2. For each role found, it generates a GitHub Actions workflow file
3. Role-specific configuration (Ubuntu versions, extra variables, etc.) is defined in `ROLE_CONFIGS`
4. Generated workflows are saved as `{role_name}-ci.yml`

### Generating Workflows

To regenerate all role workflows:

```bash
python3 .github/generate-workflows.py
```

**Note:** Generated workflow files have headers indicating they are auto-generated and should not be edited manually.

## Role Configuration

Role-specific configurations are defined in `generate-workflows.py` in the `ROLE_CONFIGS` dictionary:

```python
ROLE_CONFIGS = {
    "role_name": {
        "ubuntu_versions": ["22.04", "24.04"],  # Ubuntu versions to test
        "free_disk_space": False,                # Whether to free disk space first
        "extra_vars": {},                        # Additional Ansible variables
        "verification_commands": [],             # Commands to verify installation
        "needs_vault": False,                    # Whether role needs vault password
    }
}
```

### Adding CI for a New Role

1. Create a `tests/` directory in your role
2. Add a `test.yml` playbook in the `tests/` directory
3. (Optional) Add role-specific configuration to `ROLE_CONFIGS` in `generate-workflows.py`
4. Run `python3 .github/generate-workflows.py` to generate the workflow
5. Commit both the role and the generated workflow file

### Example Role Test Playbook

```yaml
---
- name: The test playbook for the my_role role
  hosts: all
  vars:
    my_var: test_value
  roles:
    - role: my_role
      become: true
```

## Role Configurations

### grafana_setup
- Tests on: Ubuntu 22.04, 24.04
- Disables network discovery for CI (no network scanning)
- Verifies Grafana, Prometheus, and Node Exporter services
- Checks service health endpoints

### rocm_setup  
- Tests on: Ubuntu 24.04
- Requires disk space cleanup (large packages)
- Skips hardware checks (no AMD GPUs in CI)
- Verifies ROCm package installation

### rdma_setup
- Tests on: Ubuntu 22.04, 24.04
- Verifies RDMA package installation
- Checks for InfiniBand tools

## GitHub Runner Limitations

Some features are automatically disabled or skipped in CI environments:

1. **Hardware-specific tests**: GPU checks, RDMA hardware tests
2. **Network scanning**: Discovery features that scan local networks
3. **Disk-intensive operations**: Some roles free disk space first
4. **WSL-specific features**: Windows Subsystem for Linux installations

These are configured via the `extra_vars` in each role's configuration.

## Workflow Triggers

Individual role workflows trigger on:
- Manual dispatch (`workflow_dispatch`)
- Pull requests to `main` branch (when role files change)
- Pushes to `main` branch (when role files change)

Path filters ensure workflows only run when relevant files are modified:
- `roles/{role_name}/**`
- `.github/workflows/**`
- `requirements.txt`
- `requirements.yml`

## Maintenance

### Updating Workflows

1. Modify `ROLE_CONFIGS` in `generate-workflows.py`
2. Run `python3 .github/generate-workflows.py`
3. Review the generated workflow files
4. Commit changes

### Adding New Ubuntu Versions

Update the `ubuntu_versions` list in the role's config:

```python
"role_name": {
    "ubuntu_versions": ["22.04", "24.04", "25.04"],
    ...
}
```

Then regenerate workflows.

## Best Practices

1. **Keep test playbooks simple**: Use `tests/test.yml` for straightforward role execution
2. **Add verification commands**: Include commands to verify the role worked correctly
3. **Skip non-CI features**: Use `extra_vars` to disable features that don't work in CI
4. **Test on multiple Ubuntu versions**: When possible, test on both LTS versions
5. **Free disk space when needed**: Large packages (ROCm, etc.) may need disk cleanup

## Troubleshooting

### Workflow not triggering
- Check that your role has a `tests/` directory with `test.yml`
- Verify the workflow file exists in `.github/workflows/`
- Check path filters match your changes

### Test failures
- Review verification commands in the workflow
- Check if hardware-specific features need to be disabled
- Verify required secrets are configured in GitHub repository settings

### Regenerating workflows
If workflows become out of sync:
```bash
cd .github
python3 generate-workflows.py
git add workflows/*.yml
git commit -m "Regenerate role CI workflows"
```

