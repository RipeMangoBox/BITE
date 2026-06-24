#!/usr/bin/env bash
set -euo pipefail

source ~/miniconda3/etc/profile.d/conda.sh
conda activate event-t2m

MOTION_ROOT=/data/public/ripemangobox/Motion
EXP_ROOT="$MOTION_ROOT/experiments/MoDebug"
REPO="$MOTION_ROOT/MotionCLR"
SCRIPT="$EXP_ROOT/scripts/trace1_full_eval_attention_intervention.py"
RUN_ID=${RUN_ID:-trace1_full_eval_preflight_ds_review_20260604_gpu0}
RUN_ROOT="$EXP_ROOT/motionclr/preflight/$RUN_ID"

LAYER=${LAYER:-0}
ALPHA=${ALPHA:-0.5}
CFG_SCALE=${CFG_SCALE:-2.5}
SEED=${SEED:-42}
BATCH_SIZE=${BATCH_SIZE:-8}
NUM_INFERENCE_STEPS=${NUM_INFERENCE_STEPS:-1}

mkdir -p "$RUN_ROOT"
cd "$REPO"

run_variant() {
  local family=$1
  local layer=$2
  local out_dir
  if [[ "$family" == "baseline" ]]; then
    out_dir="$RUN_ROOT/baseline"
  else
    out_dir="$RUN_ROOT/$family/layer_${layer}"
  fi
  rm -rf "$out_dir"
  mkdir -p "$out_dir"
  local layers_arg=0
  if [[ "$family" != "baseline" ]]; then
    layers_arg=$layer
  fi
  CUDA_VISIBLE_DEVICES=0 python "$SCRIPT" \
    --repo_dir "$REPO" \
    --out_dir "$out_dir" \
    --family "$family" \
    --layers "$layers_arg" \
    --alpha "$ALPHA" \
    --cfg_scale "$CFG_SCALE" \
    --seed "$SEED" \
    --opt_path ./checkpoints/t2m/release/opt.txt \
    --which_ckpt latest \
    --gpu_id 0 \
    --batch_size "$BATCH_SIZE" \
    --replication_times 1 \
    --num_inference_steps "$NUM_INFERENCE_STEPS" \
    --evaluator_dir ./data/pretrained_models \
    --eval_meta_dir ./data \
    --glove_dir ./data/glove \
    --no_eff \
    --self_attention \
    --no_fp16 \
    2>&1 | tee "$out_dir/stdout_stderr.log"
}

run_variant baseline "$LAYER"
run_variant ca "$LAYER"
run_variant sa "$LAYER"
run_variant cfg_ca "$LAYER"
run_variant cfg_sa "$LAYER"

python - "$RUN_ROOT" "$LAYER" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
layer = sys.argv[2]
paths = {
    "baseline": root / "baseline" / "manifest.json",
    "ca": root / "ca" / f"layer_{layer}" / "manifest.json",
    "sa": root / "sa" / f"layer_{layer}" / "manifest.json",
    "cfg_ca": root / "cfg_ca" / f"layer_{layer}" / "manifest.json",
    "cfg_sa": root / "cfg_sa" / f"layer_{layer}" / "manifest.json",
}
report = {}
failures = []
for family, path in paths.items():
    if not path.exists():
        failures.append(f"missing manifest: {path}")
        continue
    data = json.loads(path.read_text())
    report[family] = {
        "manifest": str(path),
        "failures": data.get("failures", []),
        "hook_call_counts": data.get("hook_call_counts", {}),
        "replacement_checks": len(data.get("replacement_checks", [])),
    }
    if data.get("failures"):
        failures.append(f"{family} failures: {data['failures']}")
    if family != "baseline":
        count = data.get("hook_call_counts", {}).get(str(layer), 0)
        if count <= 0:
            failures.append(f"{family} hook call count is {count}")
    if family in {"cfg_ca", "cfg_sa"} and not data.get("replacement_checks"):
        failures.append(f"{family} has no replacement checks")

summary = {"root": str(root), "layer": int(layer), "report": report, "failures": failures}
(root / "preflight_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
if failures:
    raise SystemExit(2)
PY

date -Is > "$RUN_ROOT/preflight_done.marker"
