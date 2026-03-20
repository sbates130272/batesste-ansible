====================================
sbates130272.batesste Release Notes
====================================

.. contents:: Topics

v1.0.0
======

Release Summary
----------------
Initial release of the batesste Ansible collection. All
roles previously published as standalone roles are now
bundled into a single collection. The geerlingguy.docker
and mrlesmithjr.netplan dependencies have been inlined.

Major Changes
--------------
- Published 20 roles as the ``sbates130272.batesste``
  collection.
- Added ``docker_setup`` role replacing the standalone
  ``geerlingguy.docker`` role.
- Inlined netplan bridge configuration into
  ``qemu_setup``, removing the ``mrlesmithjr.netplan``
  dependency.
- Standardised all role metadata to use Apache-2.0
  license.
- All inter-role references now use fully qualified
  collection names (FQCN).
