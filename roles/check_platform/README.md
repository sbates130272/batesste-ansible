# check_platform

Validate that the target host is running a supported
distribution and release before executing a role. This is
a helper role included by all other roles in the
collection.

## How It Works

The role reads the calling role's `meta/main.yml` to
extract its `platforms` list. It then compares the target
host's `ansible_distribution` and
`ansible_distribution_release` against that list. If the
host is not supported, it calls `meta: end_host` to
gracefully skip the rest of the play on that host.

## Role Variables

### Required Variables

```yaml
# Path to the calling role (set automatically by the
# calling role before including check_platform)
calling_role_path: "{{ role_path }}"
```

## Usage

This role is not intended to be used directly in
playbooks. Each role in the collection includes it
automatically:

```yaml
- name: Set a fact containing the current roles' path
  ansible.builtin.set_fact:
    calling_role_path_fact: "{{ role_path }}"

- name: Test the host platform
  ansible.builtin.include_role:
    name: sbates130272.batesste.check_platform
  vars:
    calling_role_path: "{{ calling_role_path_fact }}"
```

## Supported Platforms

- Ubuntu noble (24.04)
- Ubuntu resolute (26.04)

## License

Apache-2.0

## Author

Stephen Bates (sbates@raithlin.com)
