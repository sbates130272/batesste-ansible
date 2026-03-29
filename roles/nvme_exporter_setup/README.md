# nvme_exporter_setup

Install and configure the
[Prometheus NVMe exporter](https://github.com/E4-Computer-Engineering/nvme-exporter)
on Ubuntu. The exporter exposes NVMe SMART log and OCP SMART
log metrics for Prometheus scraping.

## Requirements

- `nvme-cli` version 2.3 or later (installed automatically
  by this role).
- Root access is required for reading NVMe device data; the
  systemd unit runs as root.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `nvme_exporter_setup_install` | `false` | Set to `true` to install the exporter |
| `nvme_exporter_version` | `latest` | Version to install; `latest` queries GitHub |
| `nvme_exporter_install_dir` | `/usr/local/bin` | Binary install directory |
| `nvme_exporter_listen_address` | `:9998` | Listen address (`host:port`) |
| `nvme_exporter_metrics_path` | `/metrics` | HTTP metrics endpoint path |

## Example Playbook

```yaml
---
- name: Install NVMe exporter
  hosts: storage_nodes
  roles:
    - role: sbates130272.batesste.nvme_exporter_setup
      nvme_exporter_setup_install: true
```

## Example Inventory

```yaml
storage_nodes:
  hosts:
    nvme-host-01:
      nvme_exporter_setup_install: true
      nvme_exporter_version: "2.2.0"
```

## VM Port Forwarding

When the target is a user-mode networked VM (QEMU SLIRP),
forward the exporter port from the host so a remote
Prometheus can scrape it:

```
-netdev user,id=net0,\
  hostfwd=tcp::2222-:22,\
  hostfwd=tcp::9998-:9998
```

Then configure Prometheus to scrape
`<host-ip>:9998/metrics`.

## Dependencies

Includes `check_platform` automatically.

## Supported Platforms

- Ubuntu jammy (22.04)
- Ubuntu noble (24.04)
- Ubuntu resolute (26.04)

## License

Apache-2.0

## Author

Stephen Bates (sbates@raithlin.com)
