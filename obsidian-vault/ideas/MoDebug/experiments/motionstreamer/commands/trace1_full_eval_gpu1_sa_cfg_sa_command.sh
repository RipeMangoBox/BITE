#!/usr/bin/env bash
set -euo pipefail

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT=${EXP_ROOT:-$MOTION_ROOT/experiments/MoDebug}
REPO_DIR=${REPO_DIR:-$MOTION_ROOT/MotionStreamer}
SCRIPT=${SCRIPT:-$EXP_ROOT/motionstreamer/scripts/trace1_full_eval_attention_intervention.py}
OUT_ROOT=${OUT_ROOT:-$EXP_ROOT/motionstreamer/formal_candidates/trace1_full_eval_sa_cfg_sa_ds_review_20260605_gpu1}
GPU=${GPU:-1}
PYTHON=${PYTHON:-python3}
CFG_SCALE=${CFG_SCALE:-4.0}
ALPHA=${ALPHA:-0.5}
SEED=${SEED:-42}
RESUME_PTH=${RESUME_PTH:-$REPO_DIR/Causal_TAE/net_last.pth}
RESUME_TRANS=${RESUME_TRANS:-/cpfs03/shared/IDC/wangjingbo_group/motionstreamer/Open_source_Train_AR_16_1024_fps_30_111M_9/latest.pth}
MODE=${1:-dry-run}

log() {
  printf '[%(%F %T)T] %s\n' -1 "$*"
}

run_one() {
  local family=$1
  local layer=$2
  local out_dir="$OUT_ROOT/$family/layer_${layer}"
  local -a cmd=(
    "$PYTHON" "$SCRIPT"
    --repo_dir "$REPO_DIR"
    --out_dir "$out_dir"
    --family "$family"
    --layers "$layer"
    --alpha "$ALPHA"
    --cfg_scale "$CFG_SCALE"
    --seed "$SEED"
    --gpu_id "$GPU"
    --resume-pth "$RESUME_PTH"
    --resume-trans "$RESUME_TRANS"
  )
  if [[ "$MODE" == "--execute" ]]; then
    cmd+=(--execute)
  fi
  MODEBUG_COMMAND_SCRIPT="${BASH_SOURCE[0]}" "${cmd[@]}"
}

main() {
  if [[ "$GPU" != "1" ]]; then
    log "ERROR: this command is GPU1-only; got GPU=$GPU"
    return 1
  fi
  if [[ "$MODE" == "--execute" && "${MODEBUG_DS_APPROVED_EXECUTE:-0}" != "1" ]]; then
    log "ERROR: formal MotionStreamer GPU1 eval requires MODEBUG_DS_APPROVED_EXECUTE=1 after DS approval."
    return 2
  fi
  log "MotionStreamer SA protocol: 12 causal self-attention layers, not 18 MotionCLR CLRBlocks."
  log "Default mode is DS-review dry-run. Pass --execute only after DS approval and checkpoint provenance approval."

  local layer
  for layer in $(seq 0 11); do
    run_one sa "$layer"
  done
  for layer in $(seq 0 11); do
    run_one cfg_sa "$layer"
  done
  log "Completed MotionStreamer GPU1 sa/cfg_sa ${MODE} sweep."
}

main "$@"
