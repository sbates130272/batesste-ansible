# consul_setup

## Overview

This role installs consul on a Linux server using (by default) the
configuration files needed to connect to my homelab consul server.

## Note on prometheus-node-exporter

This role installs `prometheus-node-exporter` alongside Consul. The
`fave_packages` and `grafana_setup` roles also install it independently so each
role remains usable standalone. Running more than one of these roles on the same
host is safe (idempotent).
