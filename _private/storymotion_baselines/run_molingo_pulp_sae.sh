#!/usr/bin/env bash
set -euo pipefail

echo "MoLingo SAE adaptation is disabled for PulpMotion." >&2
echo "Reason: PulpMotion human text is sequence-level and lacks frame-level labels required by MoLingo SAE." >&2
exit 2
