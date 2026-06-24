#!/usr/bin/env bash
set -euo pipefail

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT=${EXP_ROOT:-$MOTION_ROOT/experiments/MoDebug}
REPO_DIR=${REPO_DIR:-$MOTION_ROOT/MotionGPT}
RUN_DATE=${RUN_DATE:-20260605}
GPU=${GPU:-0}
FAMILY=${FAMILY:-baseline}
LAYER=${LAYER:-0}
ALPHA=${ALPHA:-0.5}
DRY_RUN=${DRY_RUN:-1}
CONDA_ENV=${CONDA_ENV:-event-t2m}
CONDA_SH=${CONDA_SH:-$HOME/miniconda3/etc/profile.d/conda.sh}

if [[ -f "$CONDA_SH" ]]; then
  # conda is not loaded in non-interactive ssh/tmux shells by default.
  source "$CONDA_SH"
elif ! command -v conda >/dev/null 2>&1; then
  echo "ERROR: conda is unavailable; set CONDA_SH or load conda before running." >&2
  exit 2
fi

if [[ "$GPU" != "0" ]]; then
  echo "ERROR: GPU0 command got GPU=$GPU" >&2
  exit 1
fi

if [[ "$DRY_RUN" != "1" && "${MODEBUG_DS_APPROVED_EXECUTE:-0}" != "1" ]]; then
  echo "ERROR: formal MotionGPT GPU0 eval requires MODEBUG_DS_APPROVED_EXECUTE=1 after DS approval." >&2
  exit 2
fi

case "$FAMILY" in
  baseline|ca|cfg_ca) ;;
  *)
    echo "ERROR: GPU0 MotionGPT command supports only baseline, ca, cfg_ca; got FAMILY=$FAMILY" >&2
    exit 1
    ;;
esac

SCRIPT="$EXP_ROOT/motiongpt/scripts/trace1_full_eval_attention_intervention.py"
if [[ ! -f "$SCRIPT" ]]; then
  echo "ERROR: missing MotionGPT evaluator: $SCRIPT" >&2
  exit 2
fi

OUT_DIR="$EXP_ROOT/motiongpt/formal_candidates/trace1_full_eval_${FAMILY}_layer_${LAYER}_${RUN_DATE}_gpu${GPU}"
if [[ "$FAMILY" == "baseline" ]]; then
  OUT_DIR="$EXP_ROOT/motiongpt/formal_candidates/trace1_full_eval_baseline_${RUN_DATE}_gpu${GPU}"
fi

ARGS=(
  "$SCRIPT"
  --repo_dir "$REPO_DIR"
  --out_dir "$OUT_DIR"
  --family "$FAMILY"
  --layers "$LAYER"
  --gpu_id "$GPU"
  --seed 42
  --batch_size 32
  --replication_times 1
  --num_workers 4
  --expected_layers 12
  --alpha "$ALPHA"
)

if [[ "$DRY_RUN" == "1" ]]; then
  ARGS+=(--dry_run)
fi

export CUDA_VISIBLE_DEVICES="$GPU"
export MODEBUG_COMMAND_SCRIPT="${BASH_SOURCE[0]}"
cd "$REPO_DIR"
conda run -n "$CONDA_ENV" python "${ARGS[@]}"
