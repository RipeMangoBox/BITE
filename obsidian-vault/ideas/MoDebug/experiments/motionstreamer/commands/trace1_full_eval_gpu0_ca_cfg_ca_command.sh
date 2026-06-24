#!/usr/bin/env bash
set -euo pipefail

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT=${EXP_ROOT:-$MOTION_ROOT/experiments/MoDebug}
REPO_DIR=${REPO_DIR:-$MOTION_ROOT/MotionStreamer}
SCRIPT=${SCRIPT:-$EXP_ROOT/motionstreamer/scripts/trace1_full_eval_attention_intervention.py}
OUT_ROOT=${OUT_ROOT:-$EXP_ROOT/motionstreamer/formal_candidates/trace1_full_eval_ca_cfg_ca_ds_review_20260605_gpu0}
GPU=${GPU:-0}
PYTHON=${PYTHON:-python3}
MODE=${1:-dry-run}

log() {
  printf '[%(%F %T)T] %s\n' -1 "$*"
}

run_family() {
  local family=$1
  local out_dir="$OUT_ROOT/$family"
  local -a cmd=(
    "$PYTHON" "$SCRIPT"
    --repo_dir "$REPO_DIR"
    --out_dir "$out_dir"
    --family "$family"
    --gpu_id "$GPU"
  )
  if [[ "$MODE" == "--execute" ]]; then
    cmd+=(--execute)
  fi
  MODEBUG_COMMAND_SCRIPT="${BASH_SOURCE[0]}" "${cmd[@]}"
}

main() {
  if [[ "$GPU" != "0" ]]; then
    log "ERROR: this command is GPU0-only; got GPU=$GPU"
    return 1
  fi
  if [[ "$MODE" == "--execute" && "${MODEBUG_DS_APPROVED_EXECUTE:-0}" != "1" ]]; then
    log "ERROR: formal MotionStreamer GPU0 eval requires MODEBUG_DS_APPROVED_EXECUTE=1 after DS approval."
    return 2
  fi
  log "MotionStreamer has no cross-attention on the official T2M path."
  log "GPU0 owns the single MotionStreamer baseline. ca/cfg_ca are expected to fail fast for DS review."
  run_family baseline
  run_family ca || [[ $? -eq 2 ]]
  run_family cfg_ca || [[ $? -eq 2 ]]
  log "Completed MotionStreamer GPU0 ca/cfg_ca schema guard."
}

main "$@"
