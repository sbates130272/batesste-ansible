# tmux_scripts

Clone [sbates130272/tmux-scripts](https://github.com/sbates130272/tmux-scripts)
into `~/.tmux` and optionally install
[TPM (Tmux Plugin Manager)](https://github.com/tmux-plugins/tpm) so that
plugins declared in `.tmux.conf` can be installed via `prefix+I`.

## Role Variables

```yaml
# Pin to a specific commit SHA for reproducibility.
tmux_scripts_sha: a4e649c5896fddad87d584b8e34c9b9549bcc659

# Pass --force to git clone (overwrites local modifications).
tmux_scripts_force: false

# Clone TPM to ~/.tmux/plugins/tpm.
tmux_scripts_tpm_enable: true
```

## Usage

The role runs as the target user (no `become` required). Include it in
a playbook or via the `maintain` / `setup` recipes:

```yaml
- hosts: all
  roles:
    - sbates130272.batesste.tmux_scripts
```
