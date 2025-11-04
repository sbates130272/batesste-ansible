# CI Workflow Improvements

This document describes the improvements made to the CI/CD system for the batesste-ansible repository.

## Overview

The CI system has been enhanced with an automated workflow generation system that creates individual test workflows for each Ansible role. This provides better isolation, faster feedback, and easier maintenance.

## Key Improvements

### 1. Automated Workflow Generation

**Script:** `.github/generate-workflows.py`

A Python script that automatically scans the `roles/` directory and generates GitHub Actions workflows for each role that has a `tests/` directory.

**Benefits:**
- Consistent workflow structure across all roles
- Easy to add CI for new roles
- Centralized configuration management
- Reduces manual workflow maintenance

### 2. Individual Role Workflows

Each role with tests now has its own workflow file:
- `grafana_setup-ci.yml`
- `rdma_setup-ci.yml`
- `rocm_setup-ci.yml`

**Benefits:**
- Tests run independently (parallel execution)
- Failures are isolated to specific roles
- Faster feedback for role-specific changes
- Only triggers when relevant files change

### 3. Smart Path Filtering

Workflows only trigger when relevant files are modified:
```yaml
paths:
  - roles/{role_name}/**
  - .github/workflows/**
  - requirements.txt
  - requirements.yml
```

**Benefits:**
- Reduces unnecessary CI runs
- Saves GitHub Actions minutes
- Faster PR checks for focused changes

### 4. GitHub Runner Compatibility

Role configurations specify which features to disable in CI environments:

```python
"grafana_setup": {
    "extra_vars": {
        "grafana_setup_discover_node_exporters": False,  # No network scanning
        "grafana_setup_discover_amd_gpu_exporters": False,  # No GPU hardware
    }
}
```

**Benefits:**
- Tests work reliably in CI without hardware
- No manual configuration needed
- Consistent behavior across runs

### 5. Multi-Version Testing

Roles can be tested against multiple Ubuntu versions:

```python
"ubuntu_versions": ["22.04", "24.04"]
```

**Benefits:**
- Ensures compatibility across LTS versions
- Catches version-specific issues early
- Uses GitHub Actions matrix strategy

## Workflow Architecture

### Main Workflow
**File:** `batesste-ansible-ci.yml`

Runs on all PRs and handles:
- Spelling checks
- Ansible linting
- Core playbook tests
- Repository-wide validations

### Role Workflows
**Files:** `{role_name}-ci.yml` (auto-generated)

Run when role-specific files change:
- Role installation
- Test playbook execution
- Installation verification
- Service health checks

## Configuration

### Role-Specific Settings

Defined in `generate-workflows.py`:

```python
ROLE_CONFIGS = {
    "role_name": {
        "ubuntu_versions": ["22.04", "24.04"],  # Test on these Ubuntu versions
        "free_disk_space": False,                # Clean up disk before test
        "extra_vars": {},                        # Ansible variables for CI
        "verification_commands": [],             # Commands to verify success
        "needs_vault": False,                    # Requires vault password
    }
}
```

### Default Configuration

Roles without specific configuration use defaults:
- Ubuntu 22.04 and 24.04
- No disk cleanup
- No vault password
- Basic verification

## Usage

### For Role Developers

#### Adding Tests to a New Role

1. Create `roles/{role_name}/tests/test.yml`:
```yaml
---
- name: Test playbook for my_role
  hosts: all
  roles:
    - role: my_role
      become: true
```

2. (Optional) Add role config to `generate-workflows.py`

3. Generate the workflow:
```bash
python3 .github/generate-workflows.py
```

4. Commit:
```bash
git add roles/{role_name}/tests/
git add .github/workflows/{role_name}-ci.yml
git commit -m "Add CI tests for {role_name}"
```

#### Updating Workflow Configuration

1. Edit `ROLE_CONFIGS` in `.github/generate-workflows.py`
2. Regenerate workflows: `python3 .github/generate-workflows.py`
3. Commit the changes

### For CI Maintainers

#### Regenerating All Workflows

```bash
cd .github
python3 generate-workflows.py
```

#### Adding Support for New Ubuntu Version

Update the default config or role-specific config:
```python
"ubuntu_versions": ["22.04", "24.04", "25.04"]
```

Then regenerate workflows.

## Current Role Tests

### grafana_setup
- **Tests on:** Ubuntu 22.04, 24.04
- **Features disabled in CI:**
  - Node Exporter network discovery
  - AMD SMI Exporter network discovery
- **Verification:**
  - Grafana service status
  - Prometheus service status
  - Node Exporter service status
  - Health endpoint checks

### rocm_setup  
- **Tests on:** Ubuntu 24.04
- **Special requirements:**
  - Disk space cleanup (large packages)
- **Features disabled in CI:**
  - Hardware checks (no AMD GPUs)
  - WSL installation paths
- **Verification:**
  - ROCm package installation
  - AMDGPU driver status

### rdma_setup
- **Tests on:** Ubuntu 22.04, 24.04
- **Verification:**
  - RDMA package installation
  - InfiniBand tools availability

## Benefits Summary

1. **Faster Feedback**
   - Parallel test execution
   - Smart path filtering
   - Only relevant tests run

2. **Better Isolation**
   - Independent workflows per role
   - Failures don't block unrelated roles
   - Clear test results

3. **Easier Maintenance**
   - Auto-generated workflows
   - Centralized configuration
   - Consistent structure

4. **Cost Efficient**
   - Reduced unnecessary runs
   - Optimized for GitHub Actions
   - Smart triggering

5. **Developer Friendly**
   - Simple test setup
   - Clear documentation
   - Easy to extend

## Future Enhancements

Potential improvements for the CI system:

1. **Test Coverage Reports**
   - Track which roles have tests
   - Measure test execution time
   - Generate coverage badges

2. **Integration Tests**
   - Multi-role scenarios
   - Full playbook tests
   - Inter-role dependencies

3. **Performance Benchmarks**
   - Track role execution time
   - Identify slow operations
   - Historical performance data

4. **Artifact Management**
   - Save test logs
   - Store configuration snapshots
   - Debug failed runs

5. **Notification System**
   - Role-specific alerts
   - Failed test summaries
   - Slack/Discord integration

## Migration Notes

### Before
- All role tests in single workflow
- Manual workflow creation
- All tests run on every change
- No role-specific configuration

### After
- Individual workflows per role
- Auto-generated workflows
- Smart path filtering
- Centralized role configuration

### Backwards Compatibility
- Existing `batesste-ansible-ci.yml` workflow unchanged
- All current tests preserved
- No breaking changes to roles
- Additive improvements only

## Documentation

- **Workflow System:** `.github/README.md`
- **This Document:** `CI_WORKFLOW_IMPROVEMENTS.md`
- **Script Source:** `.github/generate-workflows.py`
- **Generated Workflows:** `.github/workflows/{role}-ci.yml`

## Questions & Support

For questions about the CI system:
1. Check `.github/README.md` for usage docs
2. Review `generate-workflows.py` for configuration options
3. Examine existing role configs for examples
4. Open an issue for CI-related problems

## Credits

Created as part of the batesste-ansible repository improvements to provide better CI/CD infrastructure for Ansible role development and testing.

