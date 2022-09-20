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

## Compatability

Note that OAuth2 support was only added in [mutt 2.0][mutt2.0] so
while the script runs on Ubuntu 20.04 (which includes mutt 1.13.2) it
will not allow you to access email. Instead use Ubuntu 22.04 (or
later).

[mutt]: http://www.mutt.org/
[oauth2]: https://gitlab.com/muttmua/mutt/-/blob/master/contrib/mutt_oauth2.py.README
[add_batesste]: ../roles/add_batesste
[moreinfo]: https://kinsta.com/knowledgebase/office-365-smtp/
[evenmoreinfo]: https://github.com/ork/mutt-office365
[mutt2.0]: http://www.mutt.org/relnotes/2.0/
