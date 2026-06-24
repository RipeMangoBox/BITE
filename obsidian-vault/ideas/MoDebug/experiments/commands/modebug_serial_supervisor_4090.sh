#!/usr/bin/env bash
set -euo pipefail

POLL_SEC=${POLL_SEC:-300}
TRAIN_STEPS=${TRAIN_STEPS:-50000}
EVAL_CUDA=${EVAL_CUDA:-1}

MOTION_ROOT=/data/public/ripemangobox/Motion
EXP_ROOT="$MOTION_ROOT/experiments/MoDebug"

MOLINGO_REPO="$MOTION_ROOT/MoLingo"
MOLINGO_SCRIPT="$EXP_ROOT/scripts/molingo_trace1_formal_layer_sweep.py"
MOLINGO_PROMPTS="$EXP_ROOT/molingo/prompt_sets/molingo_trace1_formal_test64_20260603.txt"
MOLINGO_OUT="$EXP_ROOT/molingo/formal_candidates/molingo_trace1_formal_layer_sweep_test64_ds_review_20260603_gpu1"
MOLINGO_SESSION=modebug_molingo_trace1_formal_test64_20260603

TRACE3_ROOT="$EXP_ROOT/motionclr/formal_candidates/trace3_formal_train_ds_review_20260603_gpu0"
TRACE3_SESSION=modebug_trace3_train_formal_20260603
MOTIONCLR_REPO="$MOTION_ROOT/MotionCLR"
TRACE3_VARIANTS=(baseline aug disploss aug_disploss)

log() {
  printf '[%(%F %T)T] %s\n' -1 "$*"
}

tmux_exists() {
  tmux has-session -t "$1" 2>/dev/null
}

require_file() {
  if [[ ! -f "$1" ]]; then
    log "ERROR: missing required file: $1"
    return 1
  fi
}

ensure_prompt_set() {
  if [[ -f "$MOLINGO_PROMPTS" ]]; then
    local count
    count=$(wc -l < "$MOLINGO_PROMPTS")
    if [[ "$count" -ge 64 ]]; then
      log "MoLingo prompt set exists: $MOLINGO_PROMPTS ($count lines)"
      return 0
    fi
    log "MoLingo prompt set has only $count lines; regenerating"
  fi

  python3 - <<'PY'
from pathlib import Path

root = Path("/data/public/ripemangobox/Motion/datasets/272-dim-HumanML3D")
out = Path("/data/public/ripemangobox/Motion/experiments/MoDebug/molingo/prompt_sets/molingo_trace1_formal_test64_20260603.txt")
out.parent.mkdir(parents=True, exist_ok=True)

ids = [line.strip() for line in (root / "split/test.txt").read_text().splitlines() if line.strip()]
rows = []
seen = set()
for mid in ids:
    text_path = root / "texts" / f"{mid}.txt"
    if not text_path.exists():
        continue
    for line in text_path.read_text().splitlines():
        parts = line.strip().split("#")
        if not parts or not parts[0].strip():
            continue
        text = parts[0].strip()
        if text in seen:
            continue
        seen.add(text)
        seconds = 9.8
        if len(parts) >= 4:
            try:
                start = float(parts[2])
                end = float(parts[3])
                if end > start:
                    seconds = max(1.0, min(9.8, (end - start) / 20.0))
            except Exception:
                pass
        rows.append(f"{text}#{seconds:g}")
        break
    if len(rows) >= 64:
        break

if len(rows) < 64:
    raise SystemExit(f"only built {len(rows)} prompts")
out.write_text("\n".join(rows) + "\n")
print(f"wrote {out} count={len(rows)}")
PY
}

check_manifest() {
  local manifest=$1
  local min_prompts=${2:-0}
  python3 - "$manifest" "$min_prompts" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
min_prompts = int(sys.argv[2])
m = json.loads(path.read_text())

failures = m.get("failures", [])
if failures:
    raise SystemExit(f"{path}: failures={failures}")

if min_prompts:
    num_prompts = int(m.get("num_prompts", 0))
    if num_prompts < min_prompts:
        raise SystemExit(f"{path}: num_prompts={num_prompts}, expected >= {min_prompts}")

print(f"manifest ok: {path}")
PY
}

wait_for_manifest_after_tmux() {
  local label=$1
  local session=$2
  local manifest=$3

  while true; do
    if [[ -f "$manifest" ]]; then
      if tmux_exists "$session"; then
        log "$label manifest exists; waiting for tmux session to exit: $session"
        sleep 30
        continue
      fi
      log "$label manifest ready: $manifest"
      return 0
    fi

    if tmux_exists "$session"; then
      log "$label still running in tmux session $session; waiting ${POLL_SEC}s"
      sleep "$POLL_SEC"
      continue
    fi

    log "ERROR: $label has no manifest and tmux session is not running"
    return 1
  done
}

run_molingo_formal_if_needed() {
  local manifest="$MOLINGO_OUT/manifest.json"
  if [[ -f "$manifest" ]]; then
    log "MoLingo formal already has manifest"
    check_manifest "$manifest" 64
    return 0
  fi

  if tmux_exists "$MOLINGO_SESSION"; then
    wait_for_manifest_after_tmux "MoLingo formal" "$MOLINGO_SESSION" "$manifest"
    check_manifest "$manifest" 64
    return 0
  fi

  log "Starting MoLingo formal directly from supervisor"
  require_file "$MOLINGO_SCRIPT"
  ensure_prompt_set
  source /home/ripemangobox/miniconda3/etc/profile.d/conda.sh
  conda activate event-t2m
  cd "$MOLINGO_REPO"
  CUDA_VISIBLE_DEVICES=1 python "$MOLINGO_SCRIPT" \
    --repo_dir "$MOLINGO_REPO" \
    --data_root "$MOTION_ROOT/datasets" \
    --out_dir "$MOLINGO_OUT" \
    --prompt_file "$MOLINGO_PROMPTS" \
    --prompt_limit 64 \
    --prompt_count_min 64 \
    --seeds 0,1,2 \
    --cfg 4.0 \
    --sample_steps 32 \
    --acc 1 \
    --run_scope formal_diagnostic_layer_sweep
  check_manifest "$manifest" 64
}

trace3_all_manifests_ready() {
  local variant
  for variant in "${TRACE3_VARIANTS[@]}"; do
    [[ -f "$TRACE3_ROOT/$variant/manifest.json" ]] || return 1
  done
  return 0
}

check_trace3_manifests() {
  python3 - "$TRACE3_ROOT" "$TRAIN_STEPS" "${TRACE3_VARIANTS[@]}" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
target_steps = int(sys.argv[2])
variants = sys.argv[3:]

for variant in variants:
    path = root / variant / "manifest.json"
    m = json.loads(path.read_text())
    actual = int(m.get("actual_steps", -1))
    if actual != target_steps:
        raise SystemExit(f"{path}: actual_steps={actual}, expected {target_steps}")
    print(f"trace3 manifest ok: {variant} actual_steps={actual}")
PY
}

wait_for_trace3_training() {
  if trace3_all_manifests_ready; then
    check_trace3_manifests
    return 0
  fi

  while true; do
    if trace3_all_manifests_ready; then
      check_trace3_manifests
      return 0
    fi
    if tmux_exists "$TRACE3_SESSION"; then
      log "Trace3 training still running in tmux session $TRACE3_SESSION; waiting ${POLL_SEC}s"
      sleep "$POLL_SEC"
      continue
    fi
    log "ERROR: Trace3 training incomplete and tmux session is not running"
    return 1
  done
}

run_trace3_official_eval() {
  source /home/ripemangobox/miniconda3/etc/profile.d/conda.sh
  conda activate event-t2m
  cd "$MOTIONCLR_REPO"

  local variant
  for variant in "${TRACE3_VARIANTS[@]}"; do
    local out_dir="$TRACE3_ROOT/$variant"
    local marker="$out_dir/eval_done.marker"
    local opt_path="$out_dir/checkpoints/t2m/trace3_${variant}_seed0_steps${TRAIN_STEPS}/opt.txt"

    if [[ -f "$marker" ]]; then
      log "Trace3 eval already marked done: $variant"
      continue
    fi
    require_file "$opt_path"

    log "Running Trace3 official eval for $variant on CUDA_VISIBLE_DEVICES=$EVAL_CUDA"
    CUDA_VISIBLE_DEVICES="$EVAL_CUDA" python scripts/evaluation.py \
      --opt_path "$opt_path" \
      --which_ckpt latest \
      --gpu_id 0 \
      --batch_size 32 \
      --replication_times 1 \
      --num_inference_steps 10 \
      --no_eff \
      --self_attention \
      --no_fp16 \
      2>&1 | tee "$out_dir/eval_stdout_stderr.log"
    date -Is > "$marker"
  done
}

main() {
  log "MoDebug serial supervisor started"
  ensure_prompt_set
  run_molingo_formal_if_needed
  wait_for_trace3_training
  run_trace3_official_eval
  log "MoDebug serial supervisor completed"
}

main "$@"
