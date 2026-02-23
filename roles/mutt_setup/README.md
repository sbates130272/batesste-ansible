# mutt_setup Ansible Role

## Overview

This Ansible Role sets up [mutt][mutt] for two of my email accounts
(sbates@raithlin.com and sbates130272@gmail.com). It uses OAuth2
authentication so nothing in this repo is a plain-text secret. The
setup of OAuth2 is not trivial (see [this][oauth2] for Outlook
setup).

## Pre-requisites

This role assumes mutt is already installed. It also assumes you have
already setup [OAuth2][oauth2] for Microsoft and Google. You will have
had to already install the [add_batesste][add_batesste] role
which insures my PGP keys are installed.

## References

For some more good information on how to setup mutt for Gmail and
Office365 see [this][moreinfo] and [this][evenmoreinfo]. But to be
honest I found the instructions [here][oauth2] the best.

## Compatibility

Note that OAuth2 support was only added in [mutt 2.0][mutt2.0] so
while the script runs on Ubuntu 20.04 (which includes mutt 1.13.2) it
will not allow you to access email. Use Ubuntu 24.04 (noble) or
later.

## Role Variables

This role uses the following variable from the vault:

```yaml
# Google OAuth2 client secret (encrypted with ansible-vault)
mutt_setup_google_oauth2_client_secret: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  ...
```

## Dependencies

- Role: `check_platform` - Validates platform compatibility
- Role: `add_batesste` - Ensures PGP keys are installed

## Example Playbook

```yaml
---
- name: Setup mutt on target hosts
  hosts: mutt_servers
  roles:
    - role: mutt_setup
      become: false
```

## Testing

Run the following from the folder this README resides in:

```bash
ANSIBLE_ROLES_PATH=../ ansible-playbook -i <host_file> \
  --vault-password-file <vault-password-file> ./tests/test.yml
```

There is an [example hosts file](./hosts-mutt-setup) that users can
use as a template for their testing.

Note: The test requires a valid vault password file that can decrypt
the `mutt_setup_google_oauth2_client_secret` variable.

## Installed Components

The role deploys the following to the target system:

- Mutt configuration file (`~/.mutt/muttrc`)
- Email account configurations (raithlin.com and gmail.com)
- OAuth2 authentication script (`mutt_oauth2.py`)
- OAuth2 tokens (encrypted)
- Email signature file
- Language configuration (en_CA)
- Directory structure for mutt cache and temporary files

## Author and License Information

See the [meta file](./meta/main.yml) for more information on the
author, licensing and other details.

[mutt]: http://www.mutt.org/
[oauth2]: https://gitlab.com/muttmua/mutt/-/blob/master/contrib/mutt_oauth2.py.README
[add_batesste]: ../roles/add_batesste
[moreinfo]: https://kinsta.com/knowledgebase/office-365-smtp/
[evenmoreinfo]: https://github.com/ork/mutt-office365
[mutt2.0]: http://www.mutt.org/relnotes/2.0/
