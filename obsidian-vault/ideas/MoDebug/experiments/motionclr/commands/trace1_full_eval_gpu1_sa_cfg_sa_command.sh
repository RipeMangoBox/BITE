#!/usr/bin/env bash
set -euo pipefail

source ~/miniconda3/etc/profile.d/conda.sh
conda activate event-t2m

MOTION_ROOT=/data/public/ripemangobox/Motion
EXP_ROOT="$MOTION_ROOT/experiments/MoDebug"
REPO="$MOTION_ROOT/MotionCLR"
SCRIPT="$EXP_ROOT/scripts/trace1_full_eval_attention_intervention.py"
RUN_ID=${RUN_ID:-trace1_full_eval_sa_cfg_sa_ds_review_20260604_gpu1}
RUN_ROOT="$EXP_ROOT/motionclr/formal_candidates/$RUN_ID"

ALPHA=${ALPHA:-0.5}
CFG_SCALE=${CFG_SCALE:-2.5}
SEED=${SEED:-42}
REPLICATION_TIMES=${REPLICATION_TIMES:-1}
NUM_INFERENCE_STEPS=${NUM_INFERENCE_STEPS:-10}
BATCH_SIZE=${BATCH_SIZE:-32}
START_LAYER=${START_LAYER:-0}
END_LAYER=${END_LAYER:-17}

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
  if [[ -f "$out_dir/manifest.json" ]]; then
    echo "skip existing $out_dir"
    return 0
  fi
  mkdir -p "$out_dir"
  local layers_arg=0
  if [[ "$family" != "baseline" ]]; then
    layers_arg=$layer
  fi
  CUDA_VISIBLE_DEVICES=1 python "$SCRIPT" \
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
    --replication_times "$REPLICATION_TIMES" \
    --num_inference_steps "$NUM_INFERENCE_STEPS" \
    --evaluator_dir ./data/pretrained_models \
    --eval_meta_dir ./data \
    --glove_dir ./data/glove \
    --no_eff \
    --self_attention \
    --no_fp16 \
    2>&1 | tee "$out_dir/stdout_stderr.log"
}

run_variant baseline 0

for layer in $(seq "$START_LAYER" "$END_LAYER"); do
  run_variant sa "$layer"
  run_variant cfg_sa "$layer"
done

date -Is > "$RUN_ROOT/gpu1_done.marker"
