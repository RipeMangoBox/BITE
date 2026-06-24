#!/usr/bin/env bash
set -euo pipefail

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT=${EXP_ROOT:-$MOTION_ROOT/experiments/MoDebug}
REPO=${REPO:-$MOTION_ROOT/MoLingo}
RUN_DATE=${RUN_DATE:-20260605}
GPU=${GPU:-1}
CONDA_BIN=${CONDA_BIN:-/home/ripemangobox/miniconda3/bin/conda}
CONDA_ENV=${CONDA_ENV:-event-t2m}

SCRIPT="$EXP_ROOT/molingo/scripts/trace1_full_eval_attention_intervention.py"
OUT_ROOT="$EXP_ROOT/molingo/formal_candidates/trace1_full_eval_sa_cfg_sa_ds_review_${RUN_DATE}_gpu1"
COMMAND_SCRIPT="$EXP_ROOT/molingo/commands/trace1_full_eval_gpu1_sa_cfg_sa_command.sh"

if [[ "$GPU" != "1" ]]; then
  echo "ERROR: this command is GPU1-only; got GPU=$GPU" >&2
  exit 1
fi

export MODEBUG_COMMAND_SCRIPT="$COMMAND_SCRIPT"
export MODEBUG_DEPLOYED_FROM="${MODEBUG_DEPLOYED_FROM:-BITE_Process/obsidian-vault/ideas/MoDebug/experiments/molingo}"
export CUDA_VISIBLE_DEVICES="$GPU"
export TRANSFORMERS_OFFLINE=1
export HF_HUB_OFFLINE=1
export MOLINGO_T5_PATH="${MOLINGO_T5_PATH:-$MOTION_ROOT/Text-encoder/t5-large}"

mkdir -p "$OUT_ROOT"

"$CONDA_BIN" run --no-capture-output -n "$CONDA_ENV" python "$SCRIPT" \
  --repo_dir "$REPO" \
  --out_dir "$OUT_ROOT/schema_preflight" \
  --schema_preflight \
  --families sa,cfg_sa \
  --expected_layers 18 \
  --gpu_id "$GPU" \
  --conda_bin "$CONDA_BIN" \
  --conda_env "$CONDA_ENV"

echo "MoLingo GPU1 strict sa+cfg_sa schema preflight passed. No long run is defined in this script."
