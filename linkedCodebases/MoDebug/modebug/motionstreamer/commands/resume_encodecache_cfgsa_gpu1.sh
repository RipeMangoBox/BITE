#!/usr/bin/env bash
set -euo pipefail

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT=${EXP_ROOT:-$MOTION_ROOT/experiments/MoDebug}
REPO_DIR=${REPO_DIR:-$MOTION_ROOT/MotionStreamer}
SCRIPT=${SCRIPT:-$EXP_ROOT/motionstreamer/scripts/trace1_full_eval_attention_intervention.py}
OUT_ROOT=${OUT_ROOT:-$EXP_ROOT/motionstreamer/formal_candidates/trace1_full_eval_sa_cfg_sa_ds_review_20260605_gpu1}
GPU=${GPU:-1}
PYTHON=${PYTHON:-/home/ripemangobox/miniconda3/envs/event-t2m/bin/python}
TEXT_ENCODER_PATH=${TEXT_ENCODER_PATH:-/data/public/ripemangobox/Motion/Text-encoder/t5-base}
RESUME_PTH=${RESUME_PTH:-$REPO_DIR/Causal_TAE_t2m_babel/net_last.pth}
RESUME_TRANS=${RESUME_TRANS:-$REPO_DIR/Experiments/t2m_model/latest.pth}
ALPHA=${ALPHA:-0.5}
CFG_SCALE=${CFG_SCALE:-4.0}
SEED=${SEED:-42}
START_LAYER=${START_LAYER:-1}
END_LAYER=${END_LAYER:-11}
LAYERS=${LAYERS:-3,7,11}
MODE=${1:-dry-run}
LOCK=${LOCK:-/tmp/modebug_motionstreamer_resume_cfgsa_gpu1.lock}
LOG_FILE=${LOG_FILE:-/tmp/modebug_motionstreamer_resume_cfgsa_gpu1_$(date +%Y%m%d_%H%M%S).log}
CURRENT_OUT_DIR=""
CURRENT_LABEL=""
CURRENT_ACTIVE=0

log() {
  printf '[%(%F %T)T] [MS-RESUME-CFGSA-GPU1] %s\n' -1 "$*" | tee -a "$LOG_FILE"
}

completed_manifest_is_valid() {
  local out_dir=$1
  "$PYTHON" - "$out_dir" <<'PY'
import json
import math
import sys
from pathlib import Path

out_dir = Path(sys.argv[1])
manifest_path = out_dir / "manifest.json"
metrics_path = out_dir / "metrics_summary.json"
if not manifest_path.is_file() or not metrics_path.is_file() or metrics_path.stat().st_size <= 2:
    raise SystemExit(1)
try:
    manifest = json.loads(manifest_path.read_text())
    metrics = json.loads(metrics_path.read_text())
except Exception:
    raise SystemExit(1)
status = manifest.get("paper_level_status") or manifest.get("status")
keys = (
    "fid",
    "diversity",
    "r_precision_top1",
    "r_precision_top2",
    "r_precision_top3",
    "matching_score",
)
if status not in {"full_evaluator_metrics_computed", "completed"}:
    raise SystemExit(1)
for key in keys:
    try:
        value = float(metrics[key])
    except Exception:
        raise SystemExit(1)
    if not math.isfinite(value):
        raise SystemExit(1)
PY
}

write_exit_record() {
  local out_dir=$1
  local status=$2
  local label=$3
  "$PYTHON" - "$out_dir" "$status" "$label" "$LOG_FILE" <<'PY'
import json
import sys
import time
from pathlib import Path

out_dir = Path(sys.argv[1])
status = int(sys.argv[2])
label = sys.argv[3]
log_file = sys.argv[4]
out_dir.mkdir(parents=True, exist_ok=True)
payload = {
    "label": label,
    "exit_status": status,
    "timestamp_unix": time.time(),
    "log_file": log_file,
    "note": "Written by resume wrapper after the per-layer process returned.",
}
(out_dir / "wrapper_exit_status.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
PY
}

write_interrupt_record() {
  local signal=$1
  if [[ "$CURRENT_ACTIVE" != "1" || -z "$CURRENT_OUT_DIR" ]]; then
    return 0
  fi
  "$PYTHON" - "$CURRENT_OUT_DIR" "$CURRENT_LABEL" "$signal" "$LOG_FILE" <<'PY'
import json
import sys
import time
from pathlib import Path

out_dir = Path(sys.argv[1])
label = sys.argv[2]
signal = sys.argv[3]
log_file = sys.argv[4]
out_dir.mkdir(parents=True, exist_ok=True)
payload = {
    "label": label,
    "signal": signal,
    "timestamp_unix": time.time(),
    "log_file": log_file,
    "note": "Written by resume wrapper trap before the active layer completed.",
}
(out_dir / "wrapper_interrupt_status.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
PY
}

on_interrupt() {
  local signal=$1
  log "INTERRUPTED signal=$signal active=$CURRENT_LABEL"
  write_interrupt_record "$signal"
  exit 130
}

run_one() {
  local layer=$1
  local out_dir="$OUT_ROOT/cfg_sa/layer_${layer}"

  if completed_manifest_is_valid "$out_dir"; then
    log "SKIP completed CFG_SA layer=$layer out=$out_dir"
    return 0
  fi

  log "RUN CFG_SA layer=$layer out=$out_dir mode=$MODE"
  CURRENT_OUT_DIR="$out_dir"
  CURRENT_LABEL="cfg_sa:$layer"
  CURRENT_ACTIVE=1
  local -a execute_arg=()
  if [[ "$MODE" == "--execute" ]]; then
    execute_arg=(--execute)
  fi
  set +e
  MODEBUG_COMMAND_SCRIPT="${BASH_SOURCE[0]}" \
  MODEBUG_DS_APPROVED_EXECUTE=1 \
  CUDA_VISIBLE_DEVICES="$GPU" \
  TRANSFORMERS_OFFLINE=1 \
  HF_HUB_OFFLINE=1 \
  "$PYTHON" "$SCRIPT" \
    --repo_dir "$REPO_DIR" \
    --out_dir "$out_dir" \
    --family cfg_sa \
    --layers "$layer" \
    --alpha "$ALPHA" \
    --cfg_scale "$CFG_SCALE" \
    --seed "$SEED" \
    --gpu_id 0 \
    --text-encoder-path "$TEXT_ENCODER_PATH" \
    --resume-pth "$RESUME_PTH" \
    --resume-trans "$RESUME_TRANS" \
    "${execute_arg[@]}" 2>&1 | tee -a "$LOG_FILE"
  local status=${PIPESTATUS[0]}
  set -e
  CURRENT_ACTIVE=0

  write_exit_record "$out_dir" "$status" "cfg_sa:$layer"
  if [[ "$status" -eq 0 ]]; then
    log "OK CFG_SA layer=$layer"
    return 0
  fi
  log "FAIL CFG_SA layer=$layer (exit $status)"
  return "$status"
}

main() {
  trap 'on_interrupt HUP' HUP
  trap 'on_interrupt INT' INT
  trap 'on_interrupt TERM' TERM

  if [[ "$GPU" != "1" ]]; then
    log "ERROR: this command is GPU1-only; got GPU=$GPU"
    return 1
  fi
  if [[ "$MODE" == "--execute" && "${MODEBUG_DS_APPROVED_EXECUTE:-0}" != "1" ]]; then
    log "ERROR: formal MotionStreamer resume requires MODEBUG_DS_APPROVED_EXECUTE=1"
    return 2
  fi
  local -a layer_list=()
  if [[ -n "$LAYERS" ]]; then
    IFS=',' read -r -a layer_list <<< "$LAYERS"
  else
    if [[ "$START_LAYER" -lt 0 || "$END_LAYER" -gt 11 || "$START_LAYER" -gt "$END_LAYER" ]]; then
      log "ERROR: invalid layer range START_LAYER=$START_LAYER END_LAYER=$END_LAYER"
      return 2
    fi
    mapfile -t layer_list < <(seq "$START_LAYER" "$END_LAYER")
  fi
  local layer
  for layer in "${layer_list[@]}"; do
    if [[ ! "$layer" =~ ^[0-9]+$ || "$layer" -lt 0 || "$layer" -gt 11 ]]; then
      log "ERROR: invalid layer in LAYERS/range: $layer"
      return 2
    fi
  done

  exec 9>"$LOCK"
  if ! flock -n 9; then
    log "ERROR: another MotionStreamer CFG_SA resume appears active: $LOCK"
    return 2
  fi

  log "START MotionStreamer CFG_SA resume GPU1 layers=${layer_list[*]} mode=$MODE"
  for layer in "${layer_list[@]}"; do
    run_one "$layer"
  done
  log "DONE MotionStreamer CFG_SA resume GPU1"
}

main "$@"
