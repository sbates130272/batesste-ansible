#!/usr/bin/env bash
# Verify that every role in roles/ is linked in the top-level README.md.
set -euo pipefail

README="README.md"
ROLES_DIR="roles"
rc=0

while IFS= read -r -d '' role_dir; do
  role=$(basename "$role_dir")
  if ! grep -qF "roles/${role}/" "$README"; then
    echo "MISSING: '$role' is not linked in $README"
    rc=1
  fi
done < <(find "$ROLES_DIR" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)

if [ "$rc" -eq 0 ]; then
  echo "OK: all roles are referenced in $README"
fi
exit "$rc"
