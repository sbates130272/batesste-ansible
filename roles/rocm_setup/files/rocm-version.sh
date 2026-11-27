#!/usr/bin/env bash
# Copyright (c) Advanced Micro Devices, Inc. All rights reserved.
#
# SPDX-License-Identifier: MIT

# Publish the host's ROCm release, its HIP runtime version, and
# the amdgpu driver package version as node-exporter textfile
# metrics, for the ROCm and DKMS columns on the LAN Overview
# dashboard's GPU Inventory table.
#
# This exists as its own collector rather than reusing
# rocm_aic_rocm_version_info, which used to report a version on
# snoc-thinkstation. That metric came from the rocm-aic-exporter
# timer -- a large bespoke LMCache/NIXL/AIS instrumentation
# package tied to that host's vLLM work, which had no business
# being installed on the other three GPU boxes just to read one
# version string. It ran on snoc-thinkstation alone, and has
# since been removed from there too, so nothing emits that series
# on this fleet any more.

set -euo pipefail

TEXTFILE_DIR="${TEXTFILE_DIR:-/var/lib/prometheus/node-exporter}"
OUT="${TEXTFILE_DIR}/rocm-version.prom"

# PATH first, then the ROCm prefixes. systemd's default PATH does
# include /usr/bin, which is where the apt-packaged hipconfig
# lives on all four hosts, so the bare lookup is not the fragile
# one -- /opt/rocm/bin is, since it is on nobody's default PATH.
#
# The order is load-bearing, not cosmetic. amd-laptop has two ROCm
# installs, and probing /opt/rocm first reports the older one,
# which is not what anything on that host actually builds or runs
# against.
find_hipconfig() {
    local c
    c="$(command -v hipconfig 2>/dev/null)" && { echo "$c"; return 0; }
    for c in /opt/rocm/bin/hipconfig /opt/rocm/hip/bin/hipconfig; do
        [[ -x "$c" ]] && { echo "$c"; return 0; }
    done
    # A minimal therock install has neither of the above. The
    # /opt/rocm/bin and /opt/rocm/core alternatives links come from
    # the amdrocm-core<ver>-gfx* packages, which a minimal install
    # leaves out, so the only hipconfig is under the versioned
    # prefix. Take the newest one. `|| true` because compgen exits
    # non-zero on no match, which pipefail would turn into an abort.
    c="$(compgen -G '/opt/rocm/core-*/bin/hipconfig' | sort -V | tail -1 || true)"
    [[ -n "$c" && -x "$c" ]] && { echo "$c"; return 0; }
    return 1
}

# The ROCm release -- which is NOT the HIP runtime version, and
# does not track it. snoc-thinkstation and snoc-strix are both on
# release 10.1.0 while HIP reports 7.16.26385-0000000. This
# collector originally published `hipconfig --version` as
# rocm_version_info, so a column headed ROCm showed 7.16 on hosts
# running ROCm 10.1. That was simply the wrong number.
#
# `hipconfig --path` resolves the active core through
# /etc/alternatives, so it follows an alternatives switch that a
# hardcoded /opt/rocm would miss. That matters here: both hosts
# carry /opt/rocm/core-7.14 (7.14.1) alongside core-10.1, and
# snoc-strix a core-10.0 as well, with /opt/rocm/core pointing at
# whichever is selected.
rocm_release_version() {
    local p
    p="$("$1" --path 2>/dev/null)" || return 0
    [[ -n "$p" && -r "${p}/.info/version" ]] || return 0
    tr -d '[:space:]' < "${p}/.info/version"
    return 0
}

# Fallback for an install whose hipconfig cannot resolve a path
# but which still lays down a version file. Checked in prefix
# order, most specific first.
rocm_release_fallback() {
    local f
    for f in /opt/rocm/core/.info/version /opt/rocm/.info/version; do
        [[ -r "$f" ]] && { tr -d '[:space:]' < "$f"; return 0; }
    done
    f="$(compgen -G '/opt/rocm/core-*/.info/version' | sort -V | tail -1 || true)"
    [[ -n "$f" && -r "$f" ]] && tr -d '[:space:]' < "$f"
    return 0
}

# Report the ROCm prefix separately when it disagrees with PATH.
# Without this, amd-laptop's stale alternatives link is invisible
# -- the column just shows a plausible version and nothing hints
# that /opt/rocm points somewhere else entirely.
alt_version() {
    local alt
    [[ -x /opt/rocm/bin/hipconfig ]] || return 0
    alt="$(rocm_release_version /opt/rocm/bin/hipconfig)"
    # The explicit `return 0` is required under `set -e`. Without
    # it the function's exit status is that of the failed test on
    # every host where the two versions agree, which is three of
    # the four, and the whole collector aborts before writing.
    [[ -n "$alt" && "$alt" != "$1" ]] && echo "$alt"
    return 0
}

# The driver release in AMD's own 30.x/31.x scheme, e.g.
# 31.60.0.0. This is the number the column shows, because it is
# the one AMD versions the driver by: the apt source on these
# hosts is repo.radeon.com/amdgpu/31.60/ubuntu, and AMD's driver
# documentation is published per 31.x line.
#
# amdgpu-dkms carries it only in packed form -- its version is
# 1:7.1.9.31600000-2407772.26.04, where 31600000 is 31.60.0.0
# with the dots removed. amdgpu-dkms-firmware spells it out:
# 1:31.60.0.0.31600000-2407772.26.04. Read it from there rather
# than unpacking the digits, which would be guessing at the
# grouping -- 31600000 could be split several defensible ways
# and only the firmware package says which is right.
amdgpu_driver_release() {
    local v
    command -v dpkg-query >/dev/null 2>&1 || return 0
    v="$(dpkg-query -W -f='${Status} ${Version}' amdgpu-dkms-firmware 2>/dev/null)" || return 0
    [[ "$v" == "install ok installed "* ]] || return 0
    v="${v##* }"
    v="${v#*:}"
    # Four components, not "everything before the packed field":
    # the release is 31.60.0.0 and the packed digits follow it as
    # a fifth, so a greedy split would swallow them.
    echo "$v" | awk -F. 'NF>=4 {print $1"."$2"."$3"."$4}'
    return 0
}

# The full amdgpu-dkms version as Debian records it. Kept as its
# own series rather than shown in the column: it is what
# `apt policy amdgpu-dkms` compares against, so it is the string
# to quote in a support ticket, but it buries the release the
# column is actually about.
dpkg_amdgpu_version() {
    local v
    command -v dpkg-query >/dev/null 2>&1 || return 0
    v="$(dpkg-query -W -f='${Status} ${Version}' amdgpu-dkms 2>/dev/null)" || return 0
    # Guard on the status field: dpkg-query also succeeds for a
    # package that is merely known, or removed-but-not-purged,
    # and reporting a version for a driver that is not installed
    # would be worse than reporting nothing.
    [[ "$v" == "install ok installed "* ]] || return 0
    echo "${v##* }"
    return 0
}

# The DKMS tree built for the kernel currently running. Used for
# the health signal rather than the version string: it answers
# "did the rebuild happen", which dpkg cannot.
#
# Scoped with -k because both GPU hosts have amdgpu built for two
# kernels at once, so an unscoped query has no single answer, and
# with -m because snoc-strix also carries AMDPowerProfiler and
# xrt trees.
#
# Two output formats are in the wild. dkms 3.x (3.2.2 on both
# hosts) prints the module and version as one slash-joined field,
# "amdgpu/7.1.9-2407772.26.04, 7.0.0-38-generic, x86_64:
# installed"; dkms 2.x prints them as separate comma-separated
# fields. Trimming at the colon and testing for the slash covers
# both without parsing the status text itself, which is
# translated on some systems.
dkms_amdgpu_version() {
    local line first
    command -v dkms >/dev/null 2>&1 || return 0
    line="$(dkms status -m amdgpu -k "$(uname -r)" 2>/dev/null | head -1)"
    [[ -n "$line" ]] || return 0
    line="${line%%:*}"
    first="${line%%,*}"
    if [[ "$first" == */* ]]; then
        echo "${first#*/}"
    else
        echo "$line" | awk -F', *' '{print $2}'
    fi
    return 0
}

# Fallback for a DKMS-built module on a host without the dkms
# CLI. The filename guard is the whole point: the inbox amdgpu
# also answers `modinfo -F version` on some kernels, and
# reporting that as a DKMS version would be quietly wrong.
# Anything DKMS built lands under /updates/dkms/.
modinfo_dkms_version() {
    local f v
    f="$(modinfo -F filename amdgpu 2>/dev/null)" || return 0
    [[ "$f" == */updates/dkms/* ]] || return 0
    v="$(modinfo -F version amdgpu 2>/dev/null | head -1 | tr -d '[:space:]')"
    [[ -n "$v" ]] && echo "$v"
    return 0
}

# True when DKMS knows about amdgpu for *some* kernel. Only
# consulted once the running-kernel lookup has already come back
# empty, which makes the pair of them a real diagnosis rather
# than a blank column: the rebuild after a kernel upgrade did not
# happen, so the kernel now running has no out-of-tree amdgpu.
dkms_has_amdgpu_tree() {
    command -v dkms >/dev/null 2>&1 || return 1
    dkms status -m amdgpu 2>/dev/null | grep -q .
}

VERSION=""
HIP_VERSION=""
if HIPCONFIG="$(find_hipconfig)"; then
    VERSION="$(rocm_release_version "$HIPCONFIG")"
    # Kept, but no longer as rocm_version_info. It is the right
    # answer to "will this kernel build and run here" and the
    # wrong answer to "what ROCm is this", so it gets its own
    # series instead of impersonating the release.
    HIP_VERSION="$("$HIPCONFIG" --version 2>/dev/null | tr -d '[:space:]')" || HIP_VERSION=""
fi
[[ -n "$VERSION" ]] || VERSION="$(rocm_release_fallback)"
ALT="$(alt_version "$VERSION")"

# Built-for-the-running-kernel first, since that is the health
# question; the reported version prefers dpkg, which is the
# number anyone would compare against a repo.
DKMS_BUILT="$(dkms_amdgpu_version | tr -d '[:space:]')"
[[ -n "$DKMS_BUILT" ]] || DKMS_BUILT="$(modinfo_dkms_version)"

# Preference order for the column: AMD's driver release, then the
# raw package version, then whatever DKMS has built. Each is a
# strictly worse answer to "which driver is this" than the one
# before it, but any of them beats a blank cell.
DKMS_PKG="$(dpkg_amdgpu_version)"
DKMS_VERSION="$(amdgpu_driver_release)"
[[ -n "$DKMS_VERSION" ]] || DKMS_VERSION="$DKMS_PKG"
[[ -n "$DKMS_VERSION" ]] || DKMS_VERSION="$DKMS_BUILT"

DKMS_MISMATCH=0
if [[ -z "$DKMS_BUILT" ]] && dkms_has_amdgpu_tree; then
    DKMS_MISMATCH=1
fi

TMP="$(mktemp "${OUT}.XXXXXX")"
trap 'rm -f "$TMP"' EXIT

{
    echo '# HELP rocm_version_present 1 if a ROCm stack was detected on this host.'
    echo '# TYPE rocm_version_present gauge'
    if [[ -n "$VERSION" || -n "$HIP_VERSION" ]]; then
        echo 'rocm_version_present 1'
        if [[ -n "$VERSION" ]]; then
            echo '# HELP rocm_version_info ROCm release version, from the active core prefix (gauge 1).'
            echo '# TYPE rocm_version_info gauge'
            printf 'rocm_version_info{version="%s"} 1\n' "$VERSION"
        fi
        if [[ -n "$HIP_VERSION" ]]; then
            echo '# HELP rocm_hip_version_info HIP runtime version from hipconfig --version (gauge 1).'
            echo '# TYPE rocm_hip_version_info gauge'
            printf 'rocm_hip_version_info{hip_version="%s"} 1\n' "$HIP_VERSION"
        fi
        if [[ -n "$ALT" ]]; then
            echo '# HELP rocm_version_prefix_mismatch /opt/rocm resolves to a different ROCm release than PATH (gauge 1).'
            echo '# TYPE rocm_version_prefix_mismatch gauge'
            printf 'rocm_version_prefix_mismatch{version="%s"} 1\n' "$ALT"
        fi
    else
        # Emit the "absent" case explicitly. A host with no ROCm
        # and a host whose collector never ran are otherwise
        # indistinguishable in the TSDB, and only one of those is
        # worth chasing.
        echo 'rocm_version_present 0'
    fi

    # The label is dkms_version rather than the version used
    # above, and that is not a style slip. GPU Inventory joins
    # its targets with a seriesToColumns transform; a second
    # frame carrying a `version` label collides with the ROCm
    # column's and one of the two gets dropped.
    echo '# HELP amdgpu_dkms_present 1 if an out-of-tree amdgpu DKMS module is built for the running kernel.'
    echo '# TYPE amdgpu_dkms_present gauge'
    if [[ -n "$DKMS_BUILT" ]]; then
        echo 'amdgpu_dkms_present 1'
    else
        # Absent covers three different hosts: the inbox amdgpu
        # driver, no AMD GPU at all, and WSL, where the GPU
        # arrives over /dev/dxg and there is no kernel module to
        # version. None of them is a fault, so none of them gets
        # a mismatch series.
        echo 'amdgpu_dkms_present 0'
        if (( DKMS_MISMATCH )); then
            echo '# HELP amdgpu_dkms_kernel_mismatch amdgpu is built by DKMS but not for the running kernel (gauge 1).'
            echo '# TYPE amdgpu_dkms_kernel_mismatch gauge'
            echo 'amdgpu_dkms_kernel_mismatch 1'
        fi
    fi
    # Emitted whenever a version is known at all, including the
    # mismatch case -- that is precisely when you want to see
    # which driver package is sitting there unbuilt.
    if [[ -n "$DKMS_VERSION" ]]; then
        echo '# HELP amdgpu_dkms_version_info amdgpu driver release, e.g. 31.60.0.0 (gauge 1).'
        echo '# TYPE amdgpu_dkms_version_info gauge'
        printf 'amdgpu_dkms_version_info{dkms_version="%s"} 1\n' "$DKMS_VERSION"
    fi
    if [[ -n "$DKMS_PKG" ]]; then
        echo '# HELP amdgpu_dkms_package_info amdgpu-dkms version as dpkg records it (gauge 1).'
        echo '# TYPE amdgpu_dkms_package_info gauge'
        printf 'amdgpu_dkms_package_info{package_version="%s"} 1\n' "$DKMS_PKG"
    fi
    if [[ -n "$DKMS_BUILT" ]]; then
        echo '# HELP amdgpu_dkms_module_info amdgpu DKMS tree version built for the running kernel (gauge 1).'
        echo '# TYPE amdgpu_dkms_module_info gauge'
        printf 'amdgpu_dkms_module_info{module_version="%s"} 1\n' "$DKMS_BUILT"
    fi
} > "$TMP"

chmod 0644 "$TMP"
mv "$TMP" "$OUT"
trap - EXIT
