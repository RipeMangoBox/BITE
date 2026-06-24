#!/usr/bin/env bash
set -euo pipefail

source ~/miniconda3/etc/profile.d/conda.sh
conda activate event-t2m

RUN_ID=trace1_formal_layer_sweep_ds_review_20260603_gpu1
OUT_DIR=/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/formal_candidates/${RUN_ID}
mkdir -p "$OUT_DIR"

cd /data/public/ripemangobox/Motion/MotionCLR

CUDA_VISIBLE_DEVICES=1 python /data/public/ripemangobox/Motion/experiments/MoDebug/scripts/trace1_formal_layer_sweep.py \
  --repo_dir /data/public/ripemangobox/Motion/MotionCLR \
  --out_dir "$OUT_DIR" \
  --opt_path ./checkpoints/t2m/release/opt.txt \
  --split test \
  --prompt_limit 64 \
  --prompt_seed 0 \
  --seeds 0,1,2 \
  --num_inference_steps 10 \
  --gpu_id 0 \
  --batch_size 8 \
  --cfg_scale 2.5 \
  --ca_alpha 0.0 \
  --no_fp16 \
  2>&1 | tee "$OUT_DIR/stdout_stderr.log"
