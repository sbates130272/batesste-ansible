# lemonade_setup

Install and configure [Lemonade Server][lemonade] on Ubuntu
hosts. Lemonade provides an OpenAI-compatible HTTP API for
running LLMs locally on CPU, GPU (ROCm/Vulkan), or NPU
hardware.

This role creates three systemd services that mirror a
production deployment:

- **lemonade-server** -- the main inference server
  (`lemonade-server serve --no-tray`).
- **lemonade-preload** -- a oneshot unit that waits for the
  server to become healthy and then pre-loads a configurable
  list of models via the `/api/v1/load` endpoint.
- **lemonade-exporter** -- an optional Prometheus exporter
  that scrapes `/api/v1/stats` and `/api/v1/health` and
  exposes metrics on a configurable port.

## Supported Platforms

- Ubuntu 24.04 (Noble)
- Ubuntu 26.04 (Resolute)

## Installation Methods

The role supports three installation methods, controlled by
the `lemonade_setup_install_method` variable:

| Value    | Description                          |
|----------|--------------------------------------|
| `deb`    | Install from the official PPA        |
| `source` | Clone and build with CMake           |
| `snap`   | Install the snap package             |

The default is `deb`.

## Role Variables

All variables live in `defaults/main.yml` and can be
overridden per host or group.

### General

| Variable                            | Default                             |
|-------------------------------------|-------------------------------------|
| `lemonade_setup_install_method`     | `"deb"`                             |
| `lemonade_setup_host`              | `"0.0.0.0"`                         |
| `lemonade_setup_port`              | `8000`                              |
| `lemonade_setup_log_level`         | `"info"`                            |
| `lemonade_setup_max_loaded_models` | `3`                                 |
| `lemonade_setup_ctx_size`          | `131072`                            |
| `lemonade_setup_api_key`           | `"{{ vault_lemonade_setup_api_key }}"` |
| `lemonade_setup_llamacpp_backend`  | `"rocm"`                            |
| `lemonade_setup_run_rocm_setup`    | `true`                              |
| `lemonade_setup_user`              | `"{{ ansible_user }}"`              |
| `lemonade_setup_group`             | `"{{ ansible_user }}"`              |
| `lemonade_setup_start_service`     | `true`                              |

### Source Build

| Variable                          | Default                                            |
|-----------------------------------|----------------------------------------------------|
| `lemonade_setup_source_repo`     | `"https://github.com/lemonade-sdk/lemonade.git"`  |
| `lemonade_setup_source_version`  | `"v10.2.0"`                                        |
| `lemonade_setup_source_dir`      | `"~/Projects/lemonade"`                            |
| `lemonade_setup_source_force`    | `false`                                            |

### Model Preload

| Variable                          | Default                                 |
|------------------------------------|-----------------------------------------|
| `lemonade_setup_preload_enabled`  | `true`                                  |
| `lemonade_setup_preload_timeout`  | `600`                                   |
| `lemonade_setup_preload_models`   | See `defaults/main.yml`                 |

### Prometheus Exporter

| Variable                            | Default  |
|--------------------------------------|----------|
| `lemonade_setup_exporter_enabled`   | `true`   |
| `lemonade_setup_exporter_port`      | `9091`   |

### llama.cpp Backend

The `lemonade_setup_llamacpp_backend` variable selects which
llama.cpp backend binary lemonade downloads and uses at
runtime. Valid values are `rocm`, `vulkan`, `cpu`, and
`metal`. The default is `rocm`, which requires a working
AMD ROCm installation on the target host.

When set to `rocm` the role will automatically run the
`rocm_setup` role first unless
`lemonade_setup_run_rocm_setup` is `false`.

## Example Playbook

```yaml
- hosts: llm_servers
  roles:
    - role: sbates130272.batesste.lemonade_setup
      vars:
        lemonade_setup_install_method: deb
        lemonade_setup_llamacpp_backend: rocm
        lemonade_setup_preload_models:
          - "Qwen3.5-35B-A3B-GGUF"
```

## Dependencies

When `lemonade_setup_llamacpp_backend` is set to `"rocm"`
(the default) and `lemonade_setup_run_rocm_setup` is `true`,
this role automatically includes
`sbates130272.batesste.rocm_setup` to ensure the AMD ROCm
stack is present. Set `lemonade_setup_run_rocm_setup` to
`false` if ROCm is already installed or managed separately.

## License

Apache-2.0

<!-- References -->

[lemonade]: https://github.com/lemonade-sdk/lemonade
