#!/usr/bin/env bash
set -euo pipefail

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT=${EXP_ROOT:-$MOTION_ROOT/experiments/MoDebug}
RUN_DATE=${RUN_DATE:-20260605}
GPU=${GPU:-0}

BASELINES=(motiongpt motionstreamer molingo)
FAILURES=()
BLOCKED=()

declare -A REPO=(
  [motiongpt]="$MOTION_ROOT/MotionGPT"
  [motionstreamer]="$MOTION_ROOT/MotionStreamer"
  [molingo]="$MOTION_ROOT/MoLingo"
)

declare -A COMMAND=(
  [motiongpt]="$EXP_ROOT/motiongpt/commands/trace1_full_eval_gpu0_ca_command.sh"
  [motionstreamer]="$EXP_ROOT/motionstreamer/commands/trace1_full_eval_gpu0_ca_cfg_ca_command.sh"
  [molingo]="$EXP_ROOT/molingo/commands/trace1_full_eval_gpu0_ca_cfg_ca_command.sh"
)

log() {
  printf '[%(%F %T)T] %s\n' -1 "$*"
}

run_expected_blockable() {
  "$@"
  local status=$?
  if [[ "$status" -eq 2 ]]; then
    return 2
  fi
  return "$status"
}

check_motionclr_baseline_policy() {
  local gpu0="$EXP_ROOT/motionclr/formal_candidates/trace1_full_eval_ca_cfg_ca_ds_review_20260604_gpu0/baseline/manifest.json"
  local gpu1="$EXP_ROOT/motionclr/formal_candidates/trace1_full_eval_sa_cfg_sa_ds_review_20260604_gpu1/baseline/manifest.json"

  if [[ ! -f "$gpu0" ]]; then
    log "ERROR: required MotionCLR GPU0 baseline is missing: $gpu0"
    return 1
  fi

  log "MotionCLR baseline policy: keep GPU0 baseline only."
  log "MotionCLR GPU0 baseline: $gpu0"
  if [[ -f "$gpu1" ]]; then
    log "MotionCLR GPU1 duplicate baseline exists and is ignored for 73-task accounting: $gpu1"
  fi
}

require_repo() {
  local baseline=$1
  if [[ ! -d "${REPO[$baseline]}" ]]; then
    log "ERROR: missing repo for $baseline: ${REPO[$baseline]}"
    return 1
  fi
}

run_baseline_preflight() {
  local baseline=$1
  local command="${COMMAND[$baseline]}"

  require_repo "$baseline"

  if [[ ! -f "$command" ]]; then
    log "BLOCK $baseline GPU$GPU baseline+ca+cfg_ca"
    log "Missing baseline-specific command script: $command"
    return 2
  fi

  log "Running $baseline GPU$GPU baseline+ca+cfg_ca preflight via $command"
  case "$baseline" in
    motiongpt)
      GPU="$GPU" RUN_DATE="$RUN_DATE" DRY_RUN=1 FAMILY=baseline bash "$command" || return $?
      GPU="$GPU" RUN_DATE="$RUN_DATE" DRY_RUN=1 FAMILY=ca LAYER=0 bash "$command" || return $?
      run_expected_blockable env GPU="$GPU" RUN_DATE="$RUN_DATE" DRY_RUN=1 FAMILY=cfg_ca bash "$command" || return $?
      ;;
    *)
      run_expected_blockable env GPU="$GPU" RUN_DATE="$RUN_DATE" bash "$command" || return $?
      ;;
  esac
}

main() {
  if [[ "$GPU" != "0" ]]; then
    log "ERROR: this script is GPU0-only; got GPU=$GPU"
    return 1
  fi

  check_motionclr_baseline_policy

  local baseline
  for baseline in "${BASELINES[@]}"; do
    set +e
    run_baseline_preflight "$baseline"
    status=$?
    set -e
    if [[ "$status" -eq 0 ]]; then
      log "OK $baseline GPU$GPU preflight"
    elif [[ "$status" -eq 2 ]]; then
      log "BLOCKED $baseline GPU$GPU preflight with expected DS/schema gate exit 2"
      BLOCKED+=("$baseline")
    else
      log "ERROR $baseline GPU$GPU preflight exited $status"
      FAILURES+=("$baseline:$status")
    fi
  done

  log "GPU0 preflight summary: blocked=${BLOCKED[*]:-none} failures=${FAILURES[*]:-none}"
  if [[ "${#FAILURES[@]}" -gt 0 ]]; then
    return 1
  fi
}

main "$@"
