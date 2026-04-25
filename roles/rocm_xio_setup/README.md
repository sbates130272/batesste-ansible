# ROCm XIO Setup

An Ansible role to build and validate [ROCm XIO][ref-rocm-xio] for
GPU-initiated IO workflows on Ubuntu noble and resolute hosts.

## Overview

This role clones and builds `ROCm/rocm-xio`, runs baseline checks, and can
run a practical endpoint performance path using `xio-tester`. It is intended
for hosts that already support ROCm, and it declares a dependency on
`rocm_setup` so ROCm prerequisites are installed first.

The role currently supports:

- Build and optional install of `rocm-xio`
- Basic checks (`rocminfo`, endpoint listing, unit tests, test endpoint)
- Endpoint performance testing (`nvme-ep` or `rdma-ep`)

## Requirements

- Ubuntu noble (24.04) or resolute (26.04)
- ROCm-capable GPU and driver stack
- Sudo access for package installation and endpoint runs
- Optional endpoint hardware:
  - NVMe SSD for `nvme-ep`
  - RDMA NIC for `rdma-ep`

## Role Variables

Available variables are listed below, with defaults from
`defaults/main.yml`.

```yaml
# Source location
rocm_xio_setup_repo_url: "https://github.com/ROCm/rocm-xio.git"
rocm_xio_setup_repo_version: "main"
rocm_xio_setup_source_dir: "{{ ansible_env.HOME }}/Projects/rocm-xio"
rocm_xio_setup_force_clone: false

# Build/install controls
rocm_xio_setup_install_dependencies: true
rocm_xio_setup_build_type: "Release"
rocm_xio_setup_build_clients: true
rocm_xio_setup_build_testing: true
rocm_xio_setup_install: false
rocm_xio_setup_install_prefix: "/opt/rocm"
rocm_xio_setup_parallel_jobs: "{{ ansible_processor_vcpus | default(4) }}"

# Basic checks
rocm_xio_setup_run_basic_checks: true
rocm_xio_setup_check_rocminfo: true
rocm_xio_setup_run_unit_tests: true
rocm_xio_setup_run_test_endpoint: true
rocm_xio_setup_test_endpoint_emulate: true

# Performance path
rocm_xio_setup_run_perf_tests: true
rocm_xio_setup_perf_endpoint: "nvme-ep"   # nvme-ep | rdma-ep
rocm_xio_setup_perf_provider: "bnxt"      # bnxt | mlx5 | ionic | ernic
rocm_xio_setup_perf_rdma_device: ""       # defaults to rocm-rdma-<provider>0
rocm_xio_setup_perf_iterations: 128        # used by rdma-ep
rocm_xio_setup_perf_transfer_size: 4096    # used by rdma-ep
rocm_xio_setup_perf_nvme_controller: "/dev/nvme0"  # used by nvme-ep
rocm_xio_setup_perf_read_io: 128           # used by nvme-ep
rocm_xio_setup_perf_batch_size: 1          # used by nvme-ep
rocm_xio_setup_perf_extra_args: ""

# Environment control
rocm_xio_setup_force_fine_grain_pcie: true
```

## Dependencies

This role depends on:

- `rocm_setup` (declared in `meta/main.yml`)

The role also runs `check_platform` directly to fail fast on unsupported
hosts.

## Example Playbook

```yaml
---
- name: Build and validate rocm-xio
  hosts: amd
  roles:
    - role: sbates130272.batesste.rocm_xio_setup
      vars:
        rocm_setup_user: "{{ username }}"
        rocm_xio_setup_source_dir: "~/Projects/rocm-xio"
        rocm_xio_setup_perf_endpoint: nvme-ep
        rocm_xio_setup_perf_nvme_controller: /dev/nvme0
```

## Suggested Flow with AWS G4

Use the dedicated [aws_ec2_setup role][ref-aws-ec2-role] to generate EC2
launch and inventory templates.

Recommended flow:

1. Generate templates:

```bash
PLAYBOOK=setup-aws-ec2-templates.yml \
HOSTS=playbooks/hosts-example.yml \
TARGETS=local \
playbooks/run-ansible
```

2. Edit generated launch YAML and replace all `REPLACE_WITH_*`
   placeholders. The default output path is:
   `~/Projects/aws-ec2-templates/g4ad-rocm-xio-instance.yaml`.
3. Launch the instance:

```bash
aws ec2 run-instances \
  --region us-east-1 \
  --cli-input-yaml \
  file://~/Projects/aws-ec2-templates/g4ad-rocm-xio-instance.yaml
```

4. Update generated inventory host value:
   `~/Projects/aws-ec2-templates/hosts-g4ad-rocm-xio.yml`.
5. Run the ROCm XIO playbook against the `aws_g4` target group:

```bash
PLAYBOOK=setup-rocm-xio.yml \
HOSTS=~/Projects/aws-ec2-templates/hosts-g4ad-rocm-xio.yml \
TARGETS=aws_g4 \
playbooks/run-ansible
```

6. The role dependency chain runs `rocm_setup` first, then
   `rocm_xio_setup`.

## Testing

Run from this role directory:

```bash
ANSIBLE_ROLES_PATH=../ ansible-playbook \
  -i ./hosts-rocm-xio-setup \
  ./tests/test.yml
```

## Notes

- `nvme-ep` performance checks are skipped automatically when the configured
  NVMe controller path does not exist.
- `rdma-ep` performance checks require a supported RDMA environment and may
  need endpoint-specific extra arguments.
- When using provider `ernic`, set `rocm_xio_setup_perf_rdma_device` explicitly
  so `xio-tester` uses the correct emulated device name.
- This role is meant for functional and baseline performance validation, not
  exhaustive benchmark automation.


<!-- References -->

[ref-rocm-xio]: https://github.com/ROCm/rocm-xio
[ref-aws-ec2-role]: ../aws_ec2_setup/README.md
