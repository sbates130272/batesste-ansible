# amd_llm_exporter

Install and run a Prometheus exporter for AMD LLM API (Anthropic) token
usage statistics. The exporter polls `https://llm-api.amd.com/api/UsageStats`
on a configurable rolling window and exposes per-provider/model metrics
(requests, prompt tokens, completion tokens, total tokens, approximate USD
charge) on port 9876.

## Requirements

`vault_amd_llm_exporter_custom_header` must be set in the vault. Its value
is the full `Ocp-Apim-Subscription-Key: <token>` header string (matching
the `ANTHROPIC_CUSTOM_HEADER` environment variable convention).

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `amd_llm_exporter_port` | `9876` | Prometheus metrics port |
| `amd_llm_exporter_window_days` | `30` | Rolling window for usage stats |
| `amd_llm_exporter_refresh_seconds` | `300` | API poll interval |
| `amd_llm_exporter_endpoint` | `https://llm-api.amd.com/api/UsageStats` | AMD LLM API endpoint |
| `amd_llm_exporter_install_dir` | `/opt/amd_llm_exporter` | Installation directory |
| `amd_llm_exporter_user` | `amd-llm-exporter` | Dedicated system user |
| `amd_llm_exporter_custom_header` | `{{ vault_amd_llm_exporter_custom_header }}` | Auth header |

## Exposed Metrics

- `amd_llm_total_requests` — total API requests in window
- `amd_llm_total_tokens` — total tokens in window
- `amd_llm_approx_charge_usd` — approximate USD charge in window
- `amd_llm_model_requests{provider, model}` — requests per model
- `amd_llm_model_prompt_tokens{provider, model}` — prompt tokens per model
- `amd_llm_model_completion_tokens{provider, model}` — completion tokens per model
- `amd_llm_model_total_tokens{provider, model}` — total tokens per model
- `amd_llm_model_approx_charge_usd{provider, model}` — USD charge per model
