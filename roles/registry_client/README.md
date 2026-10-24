# registry_client

Register a private container registry with Docker (and optionally
Podman/containerd) on Ubuntu homelan nodes.

Configures `snoc-strix.fold-leaffish.ts.net:8080` (the homelan zot
registry) as an insecure registry in `/etc/docker/daemon.json` and
writes `/etc/buildkit/buildkitd.toml` for use with `docker-container`
BuildKit builders. Uses a daemon reload (SIGHUP) rather than a restart.

## Role Variables

```yaml
# Registry endpoint — one canonical name used in every image reference.
registry_client_endpoint: snoc-strix.fold-leaffish.ts.net:8080
registry_client_insecure: true

# Non-empty: add this IP to /etc/hosts for the endpoint hostname.
# Use on hosts without MagicDNS (e.g. amd-laptop with ZScaler).
registry_client_hosts_entry_ip: ""

registry_client_configure_docker: true
registry_client_configure_podman: false
registry_client_configure_containerd: false
registry_client_reload_docker: true
```

## Opt-in

Hosts must be in the `registry_clients` inventory group (or set
`registry_client_enabled: true`) to apply this role. Most off-LAN
hosts (AWS, OCI, etc.) cannot reach the registry and must not be
targeted.

## BuildKit

The role writes `/etc/buildkit/buildkitd.toml` with an insecure
registry stanza. There is no automatic pickup — pass
`--config /etc/buildkit/buildkitd.toml` to `docker buildx create`
to use it.
