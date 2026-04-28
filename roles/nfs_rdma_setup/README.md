# nfs_rdma_setup

Configure NFS over RDMA (nfsrdma): Linux NFS server exports with `nfs.conf`
RDMA support and optional firewall rules, and NFS clients mounting over RDMA.
Patterns mirror `nvmeof_setup` (target vs host mode, optional inventory-based
server discovery).

## Features

- Target mode: install `nfs-kernel-server`, load `rpcrdma`, `/etc/exports`,
  `[nfsd]` rdma in `/etc/nfs.conf`, `RPCNFSDOPTS` for `--rdma=` port
- Sets `nfs_rdma_setup_server_address_resolved` on the server (RDMA IPv4 if
  discovered, else default IPv4) for clients resolving `nfs_rdma_setup_target_host`
- Host mode: install `nfs-common`, mount with RDMA transport; options are
  built from `nfs_rdma_setup_nfs_minor_version` and
  `nfs_rdma_setup_enable_pnfs` unless you override
  `nfs_rdma_setup_mount_options`
- Optional parallel NFS (pNFS): enable `nfs_rdma_setup_enable_pnfs` for
  NFSv4.1+ client mounts; target mode can set `[nfsd] vers4` when pNFS is
  enabled or when `nfs_rdma_setup_nfsd_vers4` is set
- Optional UFW rules for NFS ports on chosen interfaces (disabled by default)

## Role Variables

Key variables (see `defaults/main.yml` for the full list):

```yaml
nfs_rdma_setup_mode: target   # or host

nfs_rdma_setup_enable_rdma: true
nfs_rdma_setup_rdma_port: 20049

nfs_rdma_setup_export_path: /storage/home
nfs_rdma_setup_export_clients: "*"
nfs_rdma_setup_export_options: >-
  rw,no_subtree_check,no_root_squash,async,crossmnt,insecure

# NFSv4 minor version on client (0 = v4.0; 1 = v4.1 for pNFS)
nfs_rdma_setup_nfs_minor_version: 0

# Parallel NFS: bumps client to at least nfsvers=4.1; on server sets vers4
nfs_rdma_setup_enable_pnfs: false

# Optional explicit [nfsd] vers4 in nfs.conf (e.g. "4.1-4.2"); when empty and
# enable_pnfs is true, the role sets vers4 to "y"
nfs_rdma_setup_nfsd_vers4: ""

# Host mode: leave empty for auto options, or set full mount(8) string
nfs_rdma_setup_mount_options: ""

# Appended to auto-built options when mount_options is empty
nfs_rdma_setup_mount_options_extra: ""

# Host mode
nfs_rdma_setup_nfs_server: ""           # or set nfs_rdma_setup_target_host
nfs_rdma_setup_target_host: ""
nfs_rdma_setup_mount_path: /mnt/nfs-rdma

nfs_rdma_setup_configure_firewall: false
nfs_rdma_setup_ufw_rules: []
```

## Example Playbook

```yaml
---
- name: NFS server over RDMA
  hosts: nfs_servers
  roles:
    - role: sbates130272.batesste.nfs_rdma_setup
      vars:
        nfs_rdma_setup_mode: target
        nfs_rdma_setup_enable_pnfs: true

- name: NFS clients
  hosts: nfs_clients
  roles:
    - role: sbates130272.batesste.nfs_rdma_setup
      vars:
        nfs_rdma_setup_mode: host
        nfs_rdma_setup_target_host: nfs_servers_host_group_or_hostname
        nfs_rdma_setup_enable_pnfs: true
```

Use `nfs_rdma_setup_nfs_server: "192.168.1.10"` on clients instead of
`nfs_rdma_setup_target_host` when you prefer a fixed address.

## Dependencies

Uses `community.general` (`modprobe`, `ini_file`, optional `ufw`) and
`ansible.posix` (`mount`). Includes `check_platform` automatically.

## Supported Platforms

- Ubuntu noble (24.04)
- Ubuntu resolute (26.04)

## License

Apache-2.0

## Author

Stephen Bates (sbates@raithlin.com)
