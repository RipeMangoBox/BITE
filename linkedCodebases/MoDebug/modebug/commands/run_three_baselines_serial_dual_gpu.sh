#!/usr/bin/env bash
set -euo pipefail

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT=${EXP_ROOT:-$MOTION_ROOT/experiments/MoDebug}
BASELINES=${BASELINES:-motiongpt,molingo}
RUN_DATE=${RUN_DATE:-20260605}
LAYERS_12=${LAYERS_12:-3,7,11}
LAYERS_16=${LAYERS_16:-5,10,15}
LOG_FILE=${LOG_FILE:-$EXP_ROOT/logs/three_baselines_serial_dual_gpu_$(date +%Y%m%d_%H%M%S).log}
LOCK=${LOCK:-/tmp/modebug_three_baselines_serial_dual_gpu.lock}

export MODEBUG_DS_APPROVED_EXECUTE=1

log() {
  mkdir -p "$(dirname "$LOG_FILE")"
  printf '[%(%F %T)T] [MODEBUG-SERIAL-DUAL] %s\n' -1 "$*" | tee -a "$LOG_FILE"
}

split_csv() {
  local value=$1
  IFS=',' read -r -a _split_csv_out <<< "$value"
}

completed_manifest_is_valid() {
  local out_dir=$1
  python3 - "$out_dir" <<'PY'
import json
import math
import sys
from pathlib import Path

out_dir = Path(sys.argv[1])
manifest_path = out_dir / "manifest.json"
if not manifest_path.is_file():
    raise SystemExit(1)
try:
    manifest = json.loads(manifest_path.read_text())
except Exception:
    raise SystemExit(1)
status = manifest.get("paper_level_status") or manifest.get("status")
if status not in {"full_evaluator_metrics_computed", "completed"}:
    raise SystemExit(1)
metrics_path = out_dir / "metrics_summary.json"
if not metrics_path.is_file():
    raise SystemExit(0)
try:
    metrics = json.loads(metrics_path.read_text())
except Exception:
    raise SystemExit(1)
for value in metrics.values():
    if isinstance(value, (int, float)) and not math.isfinite(float(value)):
        raise SystemExit(1)
PY
}

unsupported_manifest_exists() {
  local path=$1
  [[ -f "$path" ]]
}

run_blockable() {
  local label=$1
  shift
  log "RUN $label"
  set +e
  "$@"
  local status=$?
  set -e
  if [[ "$status" -eq 0 ]]; then
    log "OK $label"
    return 0
  fi
  if [[ "$status" -eq 2 ]]; then
    log "BLOCKED $label (exit 2; accepted architecture/preflight guard)"
    return 0
  fi
  log "FAIL $label (exit $status)"
  return "$status"
}

run_motiongpt_one() {
  local gpu=$1
  local family=$2
  local layer=$3
  local command
  local out_dir

  if [[ "$gpu" == "0" ]]; then
    command="$EXP_ROOT/motiongpt/commands/trace1_full_eval_gpu0_ca_command.sh"
  else
    command="$EXP_ROOT/motiongpt/commands/trace1_full_eval_gpu1_sa_command.sh"
  fi
  if [[ "$family" == "baseline" ]]; then
    out_dir="$EXP_ROOT/motiongpt/formal_candidates/trace1_full_eval_baseline_${RUN_DATE}_gpu${gpu}"
  else
    out_dir="$EXP_ROOT/motiongpt/formal_candidates/trace1_full_eval_${family}_layer_${layer}_${RUN_DATE}_gpu${gpu}"
  fi
  if completed_manifest_is_valid "$out_dir"; then
    log "SKIP MotionGPT gpu${gpu} ${family} layer=${layer}: completed"
    return 0
  fi
  run_blockable "MotionGPT gpu${gpu} ${family} layer=${layer}" \
    env GPU="$gpu" FAMILY="$family" LAYER="$layer" RUN_DATE="$RUN_DATE" DRY_RUN=0 MODEBUG_DS_APPROVED_EXECUTE=1 \
    bash "$command"
}

run_motiongpt_unsupported_guard() {
  local gpu=$1
  local family=$2
  local preflight="$EXP_ROOT/motiongpt/preflight/failfast_${family}_${RUN_DATE}_v3/manifest.json"
  if unsupported_manifest_exists "$preflight"; then
    log "SKIP MotionGPT gpu${gpu} ${family}: unsupported manifest exists"
    return 0
  fi
  run_motiongpt_one "$gpu" "$family" 0
}

run_motiongpt_gpu0() {
  local -a layers=()
  split_csv "$LAYERS_12"; layers=("${_split_csv_out[@]}")
  run_motiongpt_one 0 baseline 0
  local layer
  for layer in "${layers[@]}"; do
    run_motiongpt_one 0 ca "$layer"
  done
  run_motiongpt_unsupported_guard 0 cfg_ca
}

run_motiongpt_gpu1() {
  local -a layers=()
  split_csv "$LAYERS_12"; layers=("${_split_csv_out[@]}")
  local layer
  for layer in "${layers[@]}"; do
    run_motiongpt_one 1 sa "$layer"
  done
  run_motiongpt_unsupported_guard 1 cfg_sa
}

run_motionstreamer_gpu0() {
  local log_file="$EXP_ROOT/logs/motionstreamer_sa_gpu0_${RUN_DATE}_$(date +%Y%m%d_%H%M%S).log"
  run_blockable "MotionStreamer gpu0 SA representative + baseline/guards" \
    env MODEBUG_DS_APPROVED_EXECUTE=1 GPU=0 LAYERS="$LAYERS_12" RUN_BASELINE_AND_GUARDS=1 LOG_FILE="$log_file" \
    bash "$EXP_ROOT/motionstreamer/commands/resume_encodecache_sa_gpu0.sh" --execute
}

run_motionstreamer_gpu1() {
  local log_file="$EXP_ROOT/logs/motionstreamer_cfgsa_gpu1_${RUN_DATE}_$(date +%Y%m%d_%H%M%S).log"
  run_blockable "MotionStreamer gpu1 CFG_SA representative" \
    env MODEBUG_DS_APPROVED_EXECUTE=1 GPU=1 LAYERS="$LAYERS_12" LOG_FILE="$log_file" \
    bash "$EXP_ROOT/motionstreamer/commands/resume_encodecache_cfgsa_gpu1.sh" --execute
}

run_molingo_one() {
  local gpu=$1
  local family=$2
  local layer=$3
  local repo="$MOTION_ROOT/MoLingo"
  local script="$EXP_ROOT/molingo/scripts/trace1_full_eval_attention_intervention.py"
  local run_id
  local out_dir
  if [[ "$gpu" == "0" ]]; then
    run_id=trace1_full_eval_ca_cfg_ca_official_${RUN_DATE}_gpu0
  else
    run_id=trace1_full_eval_sa_cfg_sa_official_${RUN_DATE}_gpu1
  fi
  local run_root="$EXP_ROOT/molingo/formal_candidates/$run_id"
  if [[ "$family" == "baseline" ]]; then
    out_dir="$run_root/baseline"
  else
    out_dir="$run_root/$family/layer_${layer}"
  fi
  if completed_manifest_is_valid "$out_dir"; then
    log "SKIP MoLingo gpu${gpu} ${family} layer=${layer}: completed"
    return 0
  fi
  mkdir -p "$out_dir"
  local -a cmd=(
    /home/ripemangobox/miniconda3/bin/conda run -n event-t2m --no-capture-output python "$script"
    --repo_dir "$repo"
    --out_dir "$out_dir"
    --family "$family"
    --gpu_id "$gpu"
    --dim_pose 272
    --cfg 5.5
    --sample_steps 32
    --acc 3
    --repeat 1
    --data_src "$MOTION_ROOT/datasets/272-dim-HumanML3D"
    --t5_path "$MOTION_ROOT/Text-encoder/t5-large"
  )
  if [[ "$family" != "baseline" ]]; then
    cmd+=(--layer "$layer")
    case "$family" in
      sa|ca) cmd+=(--alpha 0.5) ;;
      cfg_sa|cfg_ca) cmd+=(--cfg_scale 5.5) ;;
    esac
  fi
  log "RUN MoLingo gpu${gpu} ${family} layer=${layer}"
  set +e
  (
    cd "$repo"
    MODEBUG_DS_APPROVED_EXECUTE=1 \
      CUDA_VISIBLE_DEVICES="$gpu" \
      TRANSFORMERS_OFFLINE=1 \
      HF_HUB_OFFLINE=1 \
      MOLINGO_T5_PATH="$MOTION_ROOT/Text-encoder/t5-large" \
      MODEBUG_COMMAND_SCRIPT="${BASH_SOURCE[0]}" \
      "${cmd[@]}"
  ) 2>&1 | tee "$out_dir/eval_stdout_stderr.log"
  local status=${PIPESTATUS[0]}
  set -e
  if [[ "$status" -eq 0 ]]; then
    log "OK MoLingo gpu${gpu} ${family} layer=${layer}"
    return 0
  fi
  if [[ "$status" -eq 2 ]]; then
    log "BLOCKED MoLingo gpu${gpu} ${family} layer=${layer} (exit 2)"
    return 0
  fi
  log "FAIL MoLingo gpu${gpu} ${family} layer=${layer} (exit $status)"
  return "$status"
}

run_molingo_gpu0() {
  local -a layers=()
  split_csv "$LAYERS_16"; layers=("${_split_csv_out[@]}")
  run_molingo_one 0 baseline 0
  local layer
  for layer in "${layers[@]}"; do
    run_molingo_one 0 ca "$layer"
  done
  for layer in "${layers[@]}"; do
    run_molingo_one 0 cfg_ca "$layer"
  done
}

run_molingo_gpu1() {
  local -a layers=()
  split_csv "$LAYERS_16"; layers=("${_split_csv_out[@]}")
  local layer
  for layer in "${layers[@]}"; do
    run_molingo_one 1 sa "$layer"
  done
  for layer in "${layers[@]}"; do
    run_molingo_one 1 cfg_sa "$layer"
  done
}

run_group() {
  local baseline=$1
  local gpu=$2
  case "$baseline:$gpu" in
    motiongpt:0) run_motiongpt_gpu0 ;;
    motiongpt:1) run_motiongpt_gpu1 ;;
    motionstreamer:0) run_motionstreamer_gpu0 ;;
    motionstreamer:1) run_motionstreamer_gpu1 ;;
    molingo:0) run_molingo_gpu0 ;;
    molingo:1) run_molingo_gpu1 ;;
    *)
      log "ERROR: unsupported baseline/gpu pair: $baseline gpu$gpu"
      return 2
      ;;
  esac
}

run_baseline_stage() {
  local baseline=$1
  local stage_dir="$EXP_ROOT/logs/serial_dual_${RUN_DATE}/$baseline"
  mkdir -p "$stage_dir"
  log "===== START baseline stage: $baseline ====="
  run_group "$baseline" 0 > "$stage_dir/gpu0.log" 2>&1 &
  local pid0=$!
  run_group "$baseline" 1 > "$stage_dir/gpu1.log" 2>&1 &
  local pid1=$!

  set +e
  wait "$pid0"
  local status0=$?
  wait "$pid1"
  local status1=$?
  set -e

  log "baseline=$baseline gpu0_status=$status0 log=$stage_dir/gpu0.log"
  log "baseline=$baseline gpu1_status=$status1 log=$stage_dir/gpu1.log"
  if [[ "$status0" -ne 0 || "$status1" -ne 0 ]]; then
    log "FAIL baseline stage: $baseline"
    return 1
  fi
  log "===== DONE baseline stage: $baseline ====="
}

main() {
  exec 9>"$LOCK"
  if ! flock -n 9; then
    log "ERROR: another MoDebug serial dual-GPU run appears active: $LOCK"
    return 2
  fi
  log "BASELINES=$BASELINES"
  log "RUN_DATE=$RUN_DATE LAYERS_12=$LAYERS_12 LAYERS_16=$LAYERS_16"
  local -a baselines=()
  split_csv "$BASELINES"; baselines=("${_split_csv_out[@]}")
  local baseline
  for baseline in "${baselines[@]}"; do
    run_baseline_stage "$baseline"
  done
  log "ALL REQUESTED BASELINE STAGES COMPLETE"
}

main "$@"
