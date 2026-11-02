====================================
sbates130272.batesste Release Notes
====================================

.. contents:: Topics

v3.2.1
======

Release Summary
----------------
Patch release to fix Galaxy publish failure: add missing README.md
for the tmux_scripts role.

Bugfixes
---------
- ``tmux_scripts`` — add missing ``README.md`` required by Ansible Galaxy.

v3.2.0
======

Release Summary
----------------
Snap removal, tmux_scripts and registry_client roles, native
gpuagent-wsl binary for ROCm WSL2, uv-based fave_packages installs,
dotfiles proxy rework, and CI hardening.

Minor Changes
--------------
- ``user_setup`` — add ``user_setup_disable_snap`` (default true) to
  remove snapd, mask its units, and purge snap data directories.
- ``tmux_scripts`` — new role to clone and install tmux helper scripts;
  wired into maintain and setup recipes.
- ``registry_client`` — new role for homelan Zot registry client with
  pull-through cache, buildkit/containerd config, and WSL2 fixes.
- ``rocm_setup`` — replace LD_PRELOAD shim with native gpuagent-wsl
  binary for WSL2 ROCm support.
- ``fave_packages`` — install uv and ansible via GitHub releases and
  uv tool instead of pip.
- ``dotfiles`` — adopt install.sh v1.16.0 argument changes; rework
  ``--proxy`` and ``--zscaler`` flags.

Bugfixes
---------
- ``ci`` — fix secret handling for setup-amd recipe; pass boolean
  extra-vars as YAML dicts; disable tailscale in lemonade CI.
- ``rocm_setup`` — use ``--force-depends`` for gpuagent-wsl deb
  install; add ``pipefail`` to shell pipe tasks.
- ``fave_packages`` — remove spurious ``v`` prefix from uv download URL.
- ``rdma_setup`` — tolerate rdmatop PPA 503 and rdma-detect non-zero
  exit in CI.
- ``docs`` — use absolute Galaxy URLs for all role links.

v3.1.0
======

Release Summary
----------------
ROCm 10.x support, rocjitsu GPU CI lanes for LLM inference
and ROCm validation, lemonade_setup improvements, and
shields.io badges throughout.

Minor Changes
--------------
- ``rocm_setup`` — add ROCm 10.x minimal package set and
  therock stream version discovery.
- ``lemonade_setup`` — add ``amd-laptop`` to
  ``lemonade_servers`` on port 13306.
- ``ci`` — add rocjitsu vfio-pci GPU CI lane for
  ``rocm_setup``.
- ``ci`` — add rocjitsu LLM inference CI lane for
  ``lemonade_setup`` using the llamacpp:vulkan backend and
  the ``/v1/chat/completions`` endpoint.
- ``docs`` — convert all GitHub Actions CI badges to
  shields.io format.

Bugfixes
---------
- ``lemonade_setup`` — fix backends install skip condition
  and word-boundary regex in backend presence check.
- ``dotfiles`` — fix ansible-lint violations in
  ``deploy.yml`` build tasks.
- ``ci`` — numerous rocjitsu lane stabilisation fixes:
  health check timing, become_user pipelining, vault/sudo
  password stubs, inference endpoint and timeout tuning.

v1.5.0
======

Release Summary
----------------
Auto-install the local collection from
``playbooks/run-ansible`` and fix AMD uProf CLI discovery
after ``.deb`` install.

Minor Changes
--------------
- ``playbooks/run-ansible`` — auto-install the local
  ``sbates130272.batesste`` collection when missing. Set
  ``FORCE_LOCAL=1`` to rebuild and reinstall from the
  checkout before each run.

Bugfixes
---------
- ``uprof_setup`` — resolve ``AMDuProfCLI`` from the
  ``amduprof`` package under ``/opt/AMDuProf_*`` and add
  a symbolic link in ``/usr/local/bin``; the ``.deb`` does
  not add the CLI to PATH.

v1.0.0
======

Release Summary
----------------
Initial release of the batesste Ansible collection. All
roles previously published as standalone roles are now
bundled into a single collection. The geerlingguy.docker
and mrlesmithjr.netplan dependencies have been inlined.

Major Changes
--------------
- Published 20 roles as the ``sbates130272.batesste``
  collection.
- Added ``docker_setup`` role replacing the standalone
  ``geerlingguy.docker`` role.
- Inlined netplan bridge configuration into
  ``qemu_setup``, removing the ``mrlesmithjr.netplan``
  dependency.
- Standardised all role metadata to use Apache-2.0
  license.
- All inter-role references now use fully qualified
  collection names (FQCN).
