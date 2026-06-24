#!/usr/bin/env bash
set -euo pipefail

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT=${EXP_ROOT:-$MOTION_ROOT/experiments/MoDebug}
REPO_DIR=${REPO_DIR:-$MOTION_ROOT/MotionCLR}
RUN_DATE=${RUN_DATE:-20260605}
GPU=${GPU:-1}
ALPHA=${ALPHA:-0.5}
CFG_SCALE=${CFG_SCALE:-2.5}
SEED=${SEED:-42}
CONDA_ENV=${CONDA_ENV:-event-t2m}
CONDA_SH=${CONDA_SH:-$HOME/miniconda3/etc/profile.d/conda.sh}

SCRIPT="$EXP_ROOT/scripts/trace1_full_eval_attention_intervention.py"
OUT_ROOT="$EXP_ROOT/motionclr/formal_candidates/trace1_full_eval_sa_cfg_sa_${RUN_DATE}_gpu${GPU}"

log() {
  printf '[%(%F %T)T] %s\n' -1 "$*"
}

if [[ -f "$CONDA_SH" ]]; then
  source "$CONDA_SH"
elif ! command -v conda >/dev/null 2>&1; then
  echo "ERROR: conda is unavailable" >&2
  exit 2
fi

if [[ "$GPU" != "1" ]]; then
  log "ERROR: this command is GPU1-only; got GPU=$GPU"
  exit 1
fi

if [[ "${MODEBUG_DS_APPROVED_EXECUTE:-0}" != "1" ]]; then
  log "ERROR: MotionCLR GPU1 formal eval requires MODEBUG_DS_APPROVED_EXECUTE=1"
  exit 2
fi

if [[ ! -f "$SCRIPT" ]]; then
  log "ERROR: missing evaluator script: $SCRIPT"
  exit 2
fi

mkdir -p "$OUT_ROOT"

run_one() {
  local family=$1
  local layer=$2
  local out_dir="$OUT_ROOT/${family}/layer_${layer}"

  log "START MotionCLR GPU1 $family layer $layer"

  local -a args=(
    "$SCRIPT"
    --repo_dir "$REPO_DIR"
    --out_dir "$out_dir"
    --family "$family"
    --layers "$layer"
    --alpha "$ALPHA"
    --cfg_scale "$CFG_SCALE"
    --seed "$SEED"
    --gpu_id "$GPU"
    --batch_size 32
    --replication_times 1
    --num_inference_steps 10
    --no_eff --self_attention --no_fp16
  )

  export CUDA_VISIBLE_DEVICES="$GPU"
  export MODEBUG_COMMAND_SCRIPT="${BASH_SOURCE[0]}"
  cd "$REPO_DIR"
  conda run -n "$CONDA_ENV" python "${args[@]}"
  local status=$?

  if [[ "$status" -eq 0 ]]; then
    log "OK MotionCLR GPU1 $family layer $layer"
  elif [[ "$status" -eq 2 ]]; then
    log "BLOCKED MotionCLR GPU1 $family layer $layer (exit 2)"
  else
    log "FAIL MotionCLR GPU1 $family layer $layer (exit $status)"
    return "$status"
  fi
}

main() {
  log "=== MotionCLR GPU1: SA (18 layers) + CFG_SA (18 layers) ==="

  local layer
  for layer in $(seq 0 17); do
    run_one sa "$layer"
  done

  for layer in $(seq 0 17); do
    run_one cfg_sa "$layer"
  done

  log "=== MotionCLR GPU1 sweep complete ==="
}

main "$@"
