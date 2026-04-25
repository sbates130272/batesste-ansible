# rocm_hipfile_setup

Build and install hipFile and hipFile-enabled fio from source on Ubuntu
hosts where `rocm_setup` has already been run.

This role follows upstream guidance from [ROCm/hipFile][rocm-hipfile] and
[ROCm/fio][rocm-fio]:

- hipFile is built with CMake against an existing ROCm install.
- fio is built from ROCm/fio `hipFile` branch with `--enable-libhipfile`.
- Runtime link paths include both ROCm and AIS library directories.

## Requirements

- `rocm_setup` has completed successfully on the target host.
- ROCm toolchain is available at `/opt/rocm` (or override with variables).
- Ubuntu noble (24.04) or resolute (26.04).

## Role Variables

```yaml
# Master toggles
rocm_hipfile_setup_install: true
rocm_hipfile_setup_run_checks: true

# Source and install paths
rocm_hipfile_setup_projects_dir: "~/Projects"
rocm_hipfile_setup_hipfile_src_dir: "{{ rocm_hipfile_setup_projects_dir }}/hipFile"
rocm_hipfile_setup_hipfile_build_dir: "{{ rocm_hipfile_setup_hipfile_src_dir }}/build"
rocm_hipfile_setup_fio_src_dir: "{{ rocm_hipfile_setup_projects_dir }}/fio-hipfile"
rocm_hipfile_setup_fio_install_dir: "/opt/fio-hipfile"

# Repositories and pinned refs
rocm_hipfile_setup_hipfile_repo: "https://github.com/ROCm/hipFile.git"
rocm_hipfile_setup_hipfile_version: "9b0b6a1ce01d2cbb655151e69bbfe3bea4e493ae"
rocm_hipfile_setup_fio_repo: "https://github.com/ROCm/fio.git"
rocm_hipfile_setup_fio_version: "ee6ea2ebcc266f766c69df9d7990f1255e9f59f9"

# ROCm and AIS paths
rocm_hipfile_setup_rocm_path: "/opt/rocm"
rocm_hipfile_setup_ais_lib_path: "/opt/rocs-ais/lib"
rocm_hipfile_setup_ais_include_path: "/opt/rocs-ais/include"
```

## Example Playbook

```yaml
---
- name: Build hipFile and hipFile fio
  hosts: amd_hosts
  roles:
    - role: sbates130272.batesste.rocm_hipfile_setup
      vars:
        rocm_hipfile_setup_run_checks: true
```

## What the Role Does

1. Validates supported Ubuntu release via `check_platform`.
2. Verifies ROCm exists (`/opt/rocm/bin/hipcc`) and fails otherwise.
3. Installs build dependencies for hipFile and fio.
4. Clones and builds ROCm/hipFile from a pinned commit.
5. Installs hipFile to the ROCm path.
6. Clones and builds ROCm/fio from the `hipFile` branch commit with
   `--enable-libhipfile`.
7. Installs fio to `/opt/fio-hipfile` by default.
8. Optionally runs `ais-check` and `fio --enghelp=libhipfile`.

## Notes

- Upstream hipFile is now marked as deprecated in favor of
  [ROCm/rocm-systems][rocm-systems], but this role tracks the requested
  ROCm/hipFile project and current ROCm/fio `hipFile` integration branch.
- This role assumes `rocm_setup` is already applied and does not install
  ROCm itself.

## Dependencies

Includes `check_platform` automatically.

## Supported Platforms

- Ubuntu noble (24.04)
- Ubuntu resolute (26.04)

## License

Apache-2.0

<!-- References -->

[rocm-fio]: https://github.com/ROCm/fio/tree/hipFile
[rocm-hipfile]: https://github.com/ROCm/hipFile
[rocm-systems]: https://github.com/ROCm/rocm-systems
