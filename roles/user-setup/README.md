# user-setup

## Overview

This [Ansible][ansible] role adds a new user (defined in
[defaults][defaultsfile]) to the target system(s) and also sets them up as a
passwordless sudo-er. It also copies over their SSH public-key to
allow for remote login *and* copies their SSH private key to allow
access to things like [GitHub][github].

## Usage

This role assumes your public SSH key is in ~/.ssh/id_rsa.pub and your
private SSH key is in ~/.ssh/id_rsa. There is an [open issue][oi] to make
this more robust.

[ansible]: https://www.ansible.com/
[defaultsfile]: ./defaults/main.yml
[github]: https://github.com/
[oi]: https://github.com/sbates130272/batesste-ansible/issues/18
