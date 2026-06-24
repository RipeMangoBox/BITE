#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# GPU1 Master Execution Script
# Runs SA + CFG_SA across MotionCLR, MotionGPT, MotionStreamer, MoLingo
# CFG_SA blocked on MotionGPT (T5 LM lacks CFG).
# ============================================================================

export MODEBUG_DS_APPROVED_EXECUTE=1

MOTION_ROOT=/data/public/ripemangobox/Motion
EXP_ROOT="$MOTION_ROOT/experiments/MoDebug"
RUN_DATE=${RUN_DATE:-20260605}
GPU=1

LOG_FILE="$EXP_ROOT/logs/master_gpu1_${RUN_DATE}.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
  printf '[%(%F %T)T] [GPU1] %s\n' -1 "$*" | tee -a "$LOG_FILE"
}

run_cmd() {
  local label=$1
  shift
  log "START: $label"
  log "CMD: $*"
  if "$@" >> "$LOG_FILE" 2>&1; then
    log "OK: $label"
    return 0
  else
    local s=$?
    if [[ "$s" -eq 2 ]]; then
      log "BLOCKED: $label (exit 2 — expected gate)"
      return 0
    fi
    log "FAIL: $label (exit $s)"
    return "$s"
  fi
}

main() {
  log "=============================================="
  log "GPU1 MASTER EXECUTION START"
  log "=============================================="

  # ---- MotionCLR: SA (18 layers) + CFG_SA (18 layers) ----
  log ""
  log "=== PHASE 1/4: MotionCLR GPU1 SA + CFG_SA ==="
  run_cmd "MotionCLR GPU1" \
    env GPU=1 MODEBUG_DS_APPROVED_EXECUTE=1 RUN_DATE="$RUN_DATE" \
    bash "$EXP_ROOT/commands/trace1_full_eval_gpu1_sa_cfg_sa_command.sh" || true

  # ---- MotionGPT: SA (12 layers) ----
  log ""
  log "=== PHASE 2/4: MotionGPT GPU1 SA (12 layers) ==="
  log "CFG_SA blocked: T5 LM lacks classifier-free guidance"

  local mpt_cmd="$EXP_ROOT/motiongpt/commands/trace1_full_eval_gpu1_sa_command.sh"
  if [[ ! -f "$mpt_cmd" ]]; then
    log "BLOCKED: MotionGPT GPU1 command missing: $mpt_cmd"
  else
    local layer
    for layer in $(seq 0 11); do
      run_cmd "MotionGPT GPU1 SA layer $layer" \
        env GPU=1 FAMILY=sa LAYER="$layer" MODEBUG_DS_APPROVED_EXECUTE=1 DRY_RUN=0 \
        bash "$mpt_cmd" || true
    done
  fi

  # ---- MotionStreamer: SA (12 layers) + CFG_SA (12 layers) ----
  log ""
  log "=== PHASE 3/4: MotionStreamer GPU1 SA + CFG_SA (12 layers each) ==="

  local ms_cmd="$EXP_ROOT/motionstreamer/commands/trace1_full_eval_gpu1_sa_cfg_sa_command.sh"
  if [[ ! -f "$ms_cmd" ]]; then
    log "BLOCKED: MotionStreamer GPU1 command missing: $ms_cmd"
  else
    run_cmd "MotionStreamer GPU1" \
      env GPU=1 MODEBUG_DS_APPROVED_EXECUTE=1 MODE=--execute \
      bash "$ms_cmd" || true
  fi

  # ---- MoLingo: SA (16 layers) + CFG_SA (16 layers) ----
  log ""
  log "=== PHASE 4/4: MoLingo GPU1 SA + CFG_SA ==="

  local ml_cmd="$EXP_ROOT/molingo/commands/trace1_full_eval_gpu1_sa_cfg_sa_command.sh"
  if [[ ! -f "$ml_cmd" ]]; then
    log "BLOCKED: MoLingo GPU1 command missing: $ml_cmd"
    log "Run MoLingo evaluator fix agent first."
  else
    run_cmd "MoLingo GPU1" \
      env GPU=1 MODEBUG_DS_APPROVED_EXECUTE=1 RUN_DATE="$RUN_DATE" \
      bash "$ml_cmd" || true
  fi

  log ""
  log "=============================================="
  log "GPU1 MASTER EXECUTION COMPLETE"
  log "=============================================="
}

main "$@"
