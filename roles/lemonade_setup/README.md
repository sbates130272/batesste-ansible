# lemonade_setup

Install and configure [Lemonade Server][lemonade] (`lemond`) on Ubuntu
hosts. Lemonade provides an OpenAI-compatible HTTP API for running LLMs
locally on CPU, GPU (ROCm/Vulkan), or NPU hardware.

## Architecture

This role manages one systemd service — the package-shipped `lemond.service`
— and a drop-in that injects API keys:

```text
lemond (loopback only, :13305)
   └── systemd drop-in: /etc/systemd/system/lemond.service.d/10-auth.conf
          └── EnvironmentFile: /etc/lemonade/lemonade-auth.env
tailscaled  → reverse-proxy → lemond
   └── `tailscale serve --https=13305 http://127.0.0.1:13305`
Prometheus  → https://<host>.ts.net:13305/metrics  (Bearer auth required)
```

**lemond always binds loopback.** TLS termination and external exposure are
`tailscale serve`'s responsibility. Do not set a bind host/address on lemond.

Server settings are applied via `lemonade config set` (written to
`/var/lib/lemonade/config.json`, owned by the `lemonade` user). The role
does not template that file directly to avoid conflicts with lemond's own
upgrade-time rewrites.

Prometheus metrics are served at `/metrics` on the main API port.
No separate exporter process is required or wanted.

## Supported Platforms

- Ubuntu 24.04 (Noble)
- Ubuntu 26.04 (Resolute)

## Installation Methods

| Value    | Description                   |
|----------|-------------------------------|
| `deb`    | Install from the official PPA |
| `source` | Clone and build with CMake    |
| `snap`   | Install the snap package      |

The default is `deb`.

## Role Variables

### General

| Variable                              | Default                                |
|---------------------------------------|----------------------------------------|
| `lemonade_setup_install_method`       | `"deb"`                                |
| `lemonade_setup_port`                 | `13305`                                |
| `lemonade_setup_log_level`            | `"info"`                               |
| `lemonade_setup_max_loaded_models`    | `3`                                    |
| `lemonade_setup_ctx_size`             | `131072`                               |
| `lemonade_setup_no_broadcast`         | `true`                                 |
| `lemonade_setup_inhibit_suspend`      | `true`                                 |
| `lemonade_setup_llamacpp_backend`     | `"rocm"`                               |
| `lemonade_setup_run_rocm_setup`       | `true`                                 |
| `lemonade_setup_start_service`        | `true`                                 |

### Authentication

| Variable                           | Default                                          |
|------------------------------------|--------------------------------------------------|
| `lemonade_setup_api_key`           | `"{{ vault_lemonade_setup_api_key }}"`           |
| `lemonade_setup_admin_api_key`     | `"{{ vault_lemonade_setup_admin_api_key }}"`     |

Both keys are written to `/etc/lemonade/lemonade-auth.env` (mode `0600`,
`root:root`) and loaded into lemond via the systemd drop-in.
`LEMONADE_API_KEY` gates all inference and model-management endpoints.
`LEMONADE_ADMIN_API_KEY` additionally covers `/internal/*`.

### Tailscale serve

| Variable                              | Default   |
|---------------------------------------|-----------|
| `lemonade_setup_tailscale_serve`      | `true`    |
| `lemonade_setup_tailscale_https_port` | `13305`   |

Set `lemonade_setup_tailscale_serve: false` for hosts where `tailscale`
runs outside Linux (e.g. `snoc-gaming`, which runs WSL2 under Windows).
On those hosts run the equivalent command manually on Windows:

```powershell
tailscale serve --bg --https=13305 http://127.0.0.1:13305
```

### Source Build

| Variable                        | Default                                          |
|---------------------------------|--------------------------------------------------|
| `lemonade_setup_source_repo`    | `"https://github.com/lemonade-sdk/lemonade.git"` |
| `lemonade_setup_source_version` | `"HEAD"`                                         |
| `lemonade_setup_source_dir`     | `"~/Projects/lemonade"`                          |
| `lemonade_setup_source_force`   | `false`                                          |

### llama.cpp Backend

| Variable                            | Default    |
|-------------------------------------|------------|
| `lemonade_setup_llamacpp_backend`   | `"rocm"`   |
| `lemonade_setup_llamacpp_rocm_args` | `""`       |
| `lemonade_setup_llamacpp_rocm_bin`  | `"latest"` |

`lemonade_setup_llamacpp_backend` selects which backend lemond uses at
runtime. Valid values: `rocm`, `vulkan`, `cpu`, `metal`.

`lemonade_setup_llamacpp_rocm_args` passes extra flags to `llama-server`
for the ROCm backend. The current fleet-wide value is
`"-fa on -ctk q8_0 -ctv q8_0"`: enables flash attention and quantized KV
cache, cutting VRAM ~15% with negligible throughput impact.

`lemonade_setup_llamacpp_rocm_bin` controls which binary build lemond
uses: `"latest"` takes automatic fixes but risks regressions; a pinned
build ID gives reproducibility. Both hosts are currently on `"latest"`.

When `lemonade_setup_llamacpp_backend == "rocm"` the role runs
`rocm_setup` first unless `lemonade_setup_run_rocm_setup` is `false`.

### Backends

```yaml
lemonade_setup_backends:
  - llamacpp:rocm
  - llamacpp:vulkan
  - llamacpp:cpu   # omit on gfx1201 (gaming) — not supported
```

List of backends to assert are installed, as `lemonade backends install`
names. The role checks `lemonade backends` output before each install and
skips backends already present (`installed` in the output), avoiding the
~1.9 GB re-download on every play.

**The supported set is GPU-specific.** gfx1151 (strix) and gfx1201
(gaming) differ. Always set this in host_vars, not group_vars. An empty
list (the default) means no backend management — lemond uses whatever is
already present, which may silently be Vulkan even when ROCm is intended.

A host can be fully configured, healthy, scraping green, and serving
inference at 1/5th of its hardware's throughput if the right backend is
not installed. `lemonade_setup_backends` is the fix for that failure
mode.

## Vault variables required

Add to `playbooks/secrets.yml`:

```yaml
vault_lemonade_setup_api_key: <key>
vault_lemonade_setup_admin_api_key: <key>
```

Both must share the value used in the Prometheus scrape config
(`/etc/prometheus/secrets/lemonade-api-key` in batesste-homesetup).

## Example Playbook

```yaml
- hosts: lemonade_servers
  roles:
    - role: sbates130272.batesste.lemonade_setup
      vars:
        lemonade_setup_llamacpp_backend: rocm
        lemonade_setup_run_rocm_setup: false
```

## Verification

```bash
# Auth and reachability (on the host via SSH)
systemctl is-active lemond
curl -s -o /dev/null -w '%{http_code}\n' localhost:13305/metrics
# expect 401 (key enforced)

# From anywhere on the tailnet
curl -s -o /dev/null -w '%{http_code}\n' \
  -H "Authorization: Bearer $LEMONADE_API_KEY" \
  https://<host>.fold-leaffish.ts.net:13305/metrics
# expect 200 (unauthenticated should still be 401)

# Backends actually installed (run on the host as the lemonade user)
lemonade backends | grep -E 'llamacpp +(rocm|vulkan|cpu)'
# each line expected to contain "installed"

# Active backend matches config
lemonade config 2>/dev/null | grep backend

# Smoke test with a throughput number (run on demand, takes ~2 min)
lemonade bench Qwen3.5-4B-MTP-GGUF --scenarios chat --runs 1
# healthy: >100 tok/s on strix (rocm), >150 tok/s on gaming (rocm)
# if you see ~29 tok/s the backend fell back to vulkan — recheck backends
```

## Dependencies

When `lemonade_setup_llamacpp_backend == "rocm"` (the default) and
`lemonade_setup_run_rocm_setup == true`, the role automatically includes
`sbates130272.batesste.rocm_setup`.

## License

Apache-2.0

<!-- References -->

[lemonade]: https://github.com/lemonade-sdk/lemonade
