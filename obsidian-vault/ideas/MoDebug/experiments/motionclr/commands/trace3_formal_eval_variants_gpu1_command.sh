#!/usr/bin/env bash
set -euo pipefail

source ~/miniconda3/etc/profile.d/conda.sh
conda activate event-t2m

ROOT=/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/formal_candidates/trace3_formal_train_ds_review_20260603_gpu0
cd /data/public/ripemangobox/Motion/MotionCLR

for VARIANT in baseline aug disploss aug_disploss; do
  OPT_PATH="$ROOT/$VARIANT/checkpoints/t2m/trace3_${VARIANT}_seed0_steps${TRAIN_STEPS:-50000}/opt.txt"
  CUDA_VISIBLE_DEVICES=1 python scripts/evaluation.py \
    --opt_path "$OPT_PATH" \
    --which_ckpt latest \
    --gpu_id 0 \
    --batch_size 32 \
    --replication_times 1 \
    --num_inference_steps 10 \
    --no_eff \
    --self_attention \
    --no_fp16 \
    2>&1 | tee "$ROOT/$VARIANT/eval_stdout_stderr.log"
done
