# hashicorp_repo

Shared utility role that adds the HashiCorp APT repository and GPG key.

Used by `consul_setup` and `fave_packages` via `include_role` to avoid
duplicating the five-task GPG key + apt repo setup block.

## Variables

None — the role uses no configurable defaults; all paths and URLs are
fixed to HashiCorp's official distribution channel.
