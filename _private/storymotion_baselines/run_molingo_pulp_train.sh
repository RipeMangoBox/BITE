#!/usr/bin/env bash
set -euo pipefail

cat >&2 <<'MSG'
This legacy MoLingo Pulp train entry is disabled.

Reason: it trains/evaluates the deprecated pulp199pad272 route, which pads
Pulp smpl_rifke 199-D features into HumanML3D_272 and contaminates the
StoryMotion baseline contract.

Required replacement: retrain a MoLingo VAE-style human baseline directly on
Pulp 199-D input/output data, without HumanML272 checkpoints or 199->272
padding.
MSG
exit 2
