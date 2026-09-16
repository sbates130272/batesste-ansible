# rdma_interfaces

Shared utility role that discovers RDMA-capable network interfaces and their
IPv4 addresses on the target host.

Used by `nfs_rdma_setup` and `nvmeof_setup` via `include_role`. The result
is written to `rdma_interfaces_result` (a list of `{name, address}` dicts)
which callers alias to their own role-prefixed variable immediately after the
include.

## Variables

### Output

| Variable | Description |
|----------|-------------|
| `rdma_interfaces_result` | List of dicts `{name: str, address: str}` for each RDMA interface with an IPv4 address |
