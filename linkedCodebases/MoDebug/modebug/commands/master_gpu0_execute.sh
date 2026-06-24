#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# GPU0 Master Execution Script
# Runs CA + CFG_CA across MotionCLR, MotionGPT, MotionStreamer, MoLingo
# MotionCLR baseline already done on GPU0. CFG blocked on MotionGPT (T5 LM).
# MotionStreamer CA/CFG_CA blocked (no cross-attention).
# ============================================================================

export MODEBUG_DS_APPROVED_EXECUTE=1

MOTION_ROOT=/data/public/ripemangobox/Motion
EXP_ROOT="$MOTION_ROOT/experiments/MoDebug"
RUN_DATE=${RUN_DATE:-20260605}
GPU=0

LOG_FILE="$EXP_ROOT/logs/master_gpu0_${RUN_DATE}.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
  printf '[%(%F %T)T] [GPU0] %s\n' -1 "$*" | tee -a "$LOG_FILE"
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
  log "GPU0 MASTER EXECUTION START"
  log "=============================================="

  # ---- MotionCLR: CA (18 layers) + CFG_CA (18 layers) ----
  log ""
  log "=== PHASE 1/4: MotionCLR GPU0 CA + CFG_CA ==="
  run_cmd "MotionCLR GPU0" \
    env GPU=0 MODEBUG_DS_APPROVED_EXECUTE=1 RUN_DATE="$RUN_DATE" \
    bash "$EXP_ROOT/commands/trace1_full_eval_gpu0_ca_cfg_ca_command.sh" || true

  # ---- MotionGPT: baseline + CA (12 layers) ----
  log ""
  log "=== PHASE 2/4: MotionGPT GPU0 baseline + CA (12 layers) ==="
  log "CFG_CA blocked: T5 LM lacks classifier-free guidance"

  local mpt_cmd="$EXP_ROOT/motiongpt/commands/trace1_full_eval_gpu0_ca_command.sh"
  if [[ ! -f "$mpt_cmd" ]]; then
    log "BLOCKED: MotionGPT command missing: $mpt_cmd"
  else
    run_cmd "MotionGPT GPU0 baseline" \
      env GPU=0 FAMILY=baseline MODEBUG_DS_APPROVED_EXECUTE=1 DRY_RUN=0 \
      bash "$mpt_cmd" || true

    local layer
    for layer in $(seq 0 11); do
      run_cmd "MotionGPT GPU0 CA layer $layer" \
        env GPU=0 FAMILY=ca LAYER="$layer" MODEBUG_DS_APPROVED_EXECUTE=1 DRY_RUN=0 \
        bash "$mpt_cmd" || true
    done
  fi

  # ---- MotionStreamer: baseline only (CA/CFG_CA blocked) ----
  log ""
  log "=== PHASE 3/4: MotionStreamer GPU0 (baseline only) ==="
  log "CA/CFG_CA blocked: MotionStreamer has no cross-attention"

  local ms_cmd="$EXP_ROOT/motionstreamer/commands/trace1_full_eval_gpu0_ca_cfg_ca_command.sh"
  if [[ ! -f "$ms_cmd" ]]; then
    log "BLOCKED: MotionStreamer command missing: $ms_cmd"
  else
    run_cmd "MotionStreamer GPU0" \
      env GPU=0 MODEBUG_DS_APPROVED_EXECUTE=1 MODE=--execute \
      bash "$ms_cmd" || true
  fi

  # ---- MoLingo: baseline + CA (16 layers) + CFG_CA (16 layers) ----
  log ""
  log "=== PHASE 4/4: MoLingo GPU0 baseline + CA + CFG_CA ==="

  local ml_cmd="$EXP_ROOT/molingo/commands/trace1_full_eval_gpu0_ca_cfg_ca_command.sh"
  if [[ ! -f "$ml_cmd" ]]; then
    log "BLOCKED: MoLingo GPU0 command missing: $ml_cmd"
    log "Run MoLingo evaluator fix agent first."
  else
    run_cmd "MoLingo GPU0" \
      env GPU=0 MODEBUG_DS_APPROVED_EXECUTE=1 RUN_DATE="$RUN_DATE" \
      bash "$ml_cmd" || true
  fi

  log ""
  log "=============================================="
  log "GPU0 MASTER EXECUTION COMPLETE"
  log "=============================================="
}

main "$@"
