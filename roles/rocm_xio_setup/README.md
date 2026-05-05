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

The role relies on `rocm_setup` for the ROCm stack and avoids installing Ubuntu
distro HSA packages that can conflict with ROCm repository packages.

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
rocm_xio_setup_repo_version: "v0.1.0"
rocm_xio_setup_source_dir: "{{ ansible_env.HOME }}/Projects/rocm-xio"
rocm_xio_setup_force_clone: false

# Build/install controls
rocm_xio_setup_install_dependencies: true
rocm_xio_setup_remove_distro_hsa_runtime_dev: true
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

# Performance path (opt-in; can issue I/O to configured devices)
rocm_xio_setup_run_perf_tests: false
rocm_xio_setup_perf_endpoint: "nvme-ep"   # nvme-ep | rdma-ep
rocm_xio_setup_perf_provider: "bnxt"      # bnxt | mlx5 | ionic | ernic
rocm_xio_setup_perf_rdma_device: ""       # defaults to rocm-rdma-<provider>0
rocm_xio_setup_perf_iterations: 128        # used by rdma-ep
rocm_xio_setup_perf_transfer_size: 4096    # used by rdma-ep
rocm_xio_setup_gpu_count: 1                # baseline target for validation
rocm_xio_setup_perf_nvme_controllers: []   # set explicitly for nvme-ep perf
rocm_xio_setup_perf_read_io: 128           # used by nvme-ep
rocm_xio_setup_perf_batch_size: ""         # optional nvme-ep --batch-size
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
```

## Suggested Flow with AWS G4

Use the top-level setup playbook when you want the standard g4ad launch and
ROCm XIO configuration path. The EC2 play launches or discovers the instance,
then the shared recipe dispatcher runs the host setup roles.

Recommended flow:

1. Set the EC2 variables in `playbooks/hosts.yml`, a gitignored local vars
   file, or extra vars passed to Ansible.
2. Run the AWS ROCm XIO recipe from the repository root:

```bash
PLAYBOOK=setup-ec2.yml HOSTS=playbooks/hosts.yml playbooks/run-ansible
```

3. Enable performance tests only when you have explicitly configured safe test
   devices in `rocm_xio_setup_perf_nvme_controllers`.

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
- `rocm_xio_setup_run_perf_tests` defaults to `false`; do not enable it on a
  host unless the configured NVMe controller is safe for endpoint test I/O.
- `rocm_xio_setup_perf_batch_size` is empty by default because not every
  `xio-tester nvme-ep` build accepts `--batch-size`.
- `rdma-ep` performance checks require a supported RDMA environment and may
  need endpoint-specific extra arguments.
- When using provider `ernic`, set `rocm_xio_setup_perf_rdma_device` explicitly
  so `xio-tester` uses the correct emulated device name.
- This role is meant for functional and baseline performance validation, not
  exhaustive benchmark automation.


<!-- References -->

[ref-rocm-xio]: https://github.com/ROCm/rocm-xio
