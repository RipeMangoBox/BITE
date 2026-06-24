#!/usr/bin/env bash
set -euo pipefail
source ~/miniconda3/etc/profile.d/conda.sh
conda activate event-t2m

OUT_DIR=/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/dual_trace_validation/20260602_trace1_trace3_ds_pending/trace1_ca_gpu1
cd /data/public/ripemangobox/Motion/MotionCLR

CUDA_VISIBLE_DEVICES=1 python /data/public/ripemangobox/Motion/experiments/MoDebug/scripts/trace1_ca_output_scale_validation.py \
  --repo_dir /data/public/ripemangobox/Motion/MotionCLR \
  --out_dir "$OUT_DIR" \
  --opt_path ./checkpoints/t2m/release/opt.txt \
  --prompt_limit 2 \
  --num_inference_steps 10 \
  --seed 0 \
  --gpu_id 0 \
  --batch_size 1 \
  --layers 0,8,17 \
  --alpha_values 1,0.5,0 \
  --no_fp16
