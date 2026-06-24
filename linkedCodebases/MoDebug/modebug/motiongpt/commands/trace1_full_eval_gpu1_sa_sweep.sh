#!/usr/bin/env bash
set -euo pipefail

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT=${EXP_ROOT:-$MOTION_ROOT/experiments/MoDebug}
REPO_DIR=${REPO_DIR:-$MOTION_ROOT/MotionGPT}
RUN_DATE=${RUN_DATE:-20260605}
GPU=${GPU:-1}
ALPHA=${ALPHA:-0.5}
SEED=${SEED:-42}
CONDA_ENV=${CONDA_ENV:-event-t2m}
CONDA_SH=${CONDA_SH:-$HOME/miniconda3/etc/profile.d/conda.sh}

SCRIPT="$EXP_ROOT/motiongpt/scripts/trace1_full_eval_attention_intervention.py"
OUT_ROOT="$EXP_ROOT/motiongpt/formal_candidates/trace1_full_eval_sa_cfg_sa_${RUN_DATE}_gpu${GPU}"

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
  log "ERROR: MotionGPT GPU1 formal eval requires MODEBUG_DS_APPROVED_EXECUTE=1"
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

  log "START MotionGPT GPU1 $family layer $layer"

  local -a args=(
    "$SCRIPT"
    --repo_dir "$REPO_DIR"
    --out_dir "$out_dir"
    --family "$family"
    --layers "$layer"
    --alpha "$ALPHA"
    --seed "$SEED"
    --gpu_id "$GPU"
    --batch_size 32
    --replication_times 1
    --expected_layers 12
  )

  export CUDA_VISIBLE_DEVICES="$GPU"
  export MODEBUG_COMMAND_SCRIPT="${BASH_SOURCE[0]}"
  cd "$REPO_DIR"
  conda run -n "$CONDA_ENV" python "${args[@]}"
  local status=$?

  if [[ "$status" -eq 0 ]]; then
    log "OK MotionGPT GPU1 $family layer $layer"
  elif [[ "$status" -eq 2 ]]; then
    log "BLOCKED MotionGPT GPU1 $family layer $layer (exit 2)"
  else
    log "FAIL MotionGPT GPU1 $family layer $layer (exit $status)"
    return "$status"
  fi
}

main() {
  log "=== MotionGPT GPU1: SA (12 layers); CFG_SA blocked by architecture ==="

  # SA: 12-layer sweep
  local layer
  for layer in $(seq 0 11); do
    run_one sa "$layer"
  done

  # CFG_SA: expected block (T5 LM has no CFG)
  log "MotionGPT CFG_SA intentionally blocked: T5 LM lacks classifier-free guidance"
  run_one cfg_sa 0 || log "CFG_SA blocked as expected (exit 2)"

  log "=== MotionGPT GPU1 sweep complete ==="
}

main "$@"
