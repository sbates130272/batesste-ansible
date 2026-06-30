# claude_setup

Install the [Claude CLI][claude-code] and configure it to
route API requests through a local nginx reverse proxy on
AMD systems. The nginx proxy forwards Claude CLI requests to
the configured LLM serving backend (e.g. a
[Lemonade][lemonade] server on this host or a remote proxy
node).

The role installs the `@anthropic-ai/claude-code` npm package,
deploys an nginx reverse proxy site that tunnels requests to
the upstream LLM backend, writes a `~/.claude/settings.json`
file that points the CLI at the local proxy, and stores the
LLM API key in a mode-`0600` secrets file that is sourced
from `~/.bashrc`.

## Supported Platforms

- Ubuntu 24.04 (Noble)
- Ubuntu 26.04 (Resolute)

## Role Variables

All variables live in `defaults/main.yml` and can be overridden
per host or group.

| Variable                         | Default                                          | Description                                       |
|---------------------------------|--------------------------------------------------|---------------------------------------------------|
| `claude_setup_install_nodejs`   | `true`                                           | Install Node.js and npm before the CLI install    |
| `claude_setup_proxy_port`       | `8888`                                           | Port the local nginx reverse proxy listens on     |
| `claude_setup_proxy_upstream`   | `"http://localhost:8000"`                        | Upstream LLM backend URL nginx forwards to        |
| `claude_setup_api_base_url`     | `"http://localhost:{{ claude_setup_proxy_port }}"` | ANTHROPIC_BASE_URL written into Claude settings  |
| `claude_setup_api_key`          | `"{{ vault_claude_setup_api_key }}"`             | API key for the LLM serving backend (secret)      |

### `claude_setup_api_key`

This variable must be set to the API key accepted by the local
LLM serving backend (e.g. the value of `lemonade_setup_api_key`
on the same host). It should **always** be sourced from an
Ansible Vault-encrypted variable:

```yaml
# group_vars/amd_hosts/vault.yml  (vault-encrypted)
vault_claude_setup_api_key: "<your-api-key>"
```

### `claude_setup_proxy_upstream`

Set this to the URL of the LLM serving backend. When Lemonade
runs on the same host the default (`http://localhost:8000`) is
correct. Set it to a remote address when the LLM proxy runs on
a different node:

```yaml
claude_setup_proxy_upstream: "http://llm-server.example.com:8000"
```

## What the Role Does

1. Validates the host platform via `check_platform`.
2. Installs Node.js and npm (when `claude_setup_install_nodejs`
   is `true`).
3. Installs `@anthropic-ai/claude-code` globally via npm.
4. Installs nginx and deploys an nginx site at
   `/etc/nginx/sites-available/claude-proxy` that listens on
   `claude_setup_proxy_port` and proxies all requests to
   `claude_setup_proxy_upstream`.
5. Creates `~/.claude/` and writes `settings.json` containing
   the `ANTHROPIC_BASE_URL` that points Claude CLI at the local
   nginx proxy.
6. Writes `~/.claude/secrets.sh` (mode `0600`) containing the
   `ANTHROPIC_API_KEY` export for the LLM backend.
7. Adds a `source ~/.claude/secrets.sh` block to `~/.bashrc`
   so that new shells pick up the API key automatically.

## Example Playbook

```yaml
---
- name: Set up Claude CLI on AMD LLM hosts
  hosts: amd_hosts
  roles:
    - role: sbates130272.batesste.claude_setup
      vars:
        claude_setup_proxy_upstream: "http://localhost:8000"
        claude_setup_api_key: "{{ vault_claude_setup_api_key }}"
```

## Dependencies

- Role: `check_platform` — validates platform compatibility.
- `community.general` collection (for `community.general.npm`).

## License

Apache-2.0

<!-- References -->

[claude-code]: https://github.com/anthropics/claude-code
[lemonade]: https://github.com/lemonade-sdk/lemonade
