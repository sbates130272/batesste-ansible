# claude_setup

Install the [Claude CLI][claude-code] and configure it to
route API requests through a local LLM reverse proxy on
AMD systems (e.g. a [Lemonade][lemonade] server instance).

The role installs the `@anthropic-ai/claude-code` npm package,
writes a `~/.claude/settings.json` file that points the CLI at
the configured reverse proxy, and stores the LLM API key in a
mode-`0600` secrets file that is sourced from `~/.bashrc`.

## Supported Platforms

- Ubuntu 24.04 (Noble)
- Ubuntu 26.04 (Resolute)

## Role Variables

All variables live in `defaults/main.yml` and can be overridden
per host or group.

| Variable                       | Default                              | Description                                     |
|-------------------------------|--------------------------------------|-------------------------------------------------|
| `claude_setup_install_nodejs` | `true`                               | Install Node.js and npm before the CLI install  |
| `claude_setup_api_base_url`   | `"http://localhost:8000"`            | Base URL of the LLM reverse proxy               |
| `claude_setup_api_key`        | `"{{ vault_claude_setup_api_key }}"` | API key for the LLM serving backend (secret)    |

### `claude_setup_api_key`

This variable must be set to the API key accepted by the local
LLM serving backend (e.g. the value of `lemonade_setup_api_key`
on the same host). It should **always** be sourced from an
Ansible Vault-encrypted variable:

```yaml
# group_vars/amd_hosts/vault.yml  (vault-encrypted)
vault_claude_setup_api_key: "<your-api-key>"
```

### `claude_setup_api_base_url`

Set this to the URL of the reverse proxy that the Claude CLI
should send API requests to. On a host running Lemonade, the
default value (`http://localhost:8000`) is correct. Override
it when the proxy runs on a different host or port:

```yaml
claude_setup_api_base_url: "http://llm-server.example.com:8000"
```

## What the Role Does

1. Validates the host platform via `check_platform`.
2. Installs Node.js and npm (when `claude_setup_install_nodejs`
   is `true`).
3. Installs `@anthropic-ai/claude-code` globally via npm.
4. Creates `~/.claude/` and writes `settings.json` containing
   the `ANTHROPIC_BASE_URL` that routes traffic to the proxy.
5. Writes `~/.claude/secrets.sh` (mode `0600`) containing the
   `ANTHROPIC_API_KEY` export for the LLM backend.
6. Adds a `source ~/.claude/secrets.sh` block to `~/.bashrc`
   so that new shells pick up the API key automatically.

## Example Playbook

```yaml
---
- name: Set up Claude CLI on AMD LLM hosts
  hosts: amd_hosts
  roles:
    - role: sbates130272.batesste.claude_setup
      vars:
        claude_setup_api_base_url: "http://localhost:8000"
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
