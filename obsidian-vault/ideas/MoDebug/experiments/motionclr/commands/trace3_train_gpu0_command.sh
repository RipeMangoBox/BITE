#!/usr/bin/env bash
set -euo pipefail
source ~/miniconda3/etc/profile.d/conda.sh
conda activate event-t2m

OUT_DIR=/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/dual_trace_validation/20260602_trace1_trace3_ds_pending/trace3_train_gpu0
cd /data/public/ripemangobox/Motion/MotionCLR

CUDA_VISIBLE_DEVICES=0 python /data/public/ripemangobox/Motion/experiments/MoDebug/scripts/trace3_training_path_validation.py \
  --repo_dir /data/public/ripemangobox/Motion/MotionCLR \
  --out_dir "$OUT_DIR" \
  --name trace3_training_path_validation_seed0_steps3 \
  --batch_size 1 \
  --max_steps 3 \
  --seed 0
