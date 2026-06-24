#!/usr/bin/env bash
set -euo pipefail

source ~/miniconda3/etc/profile.d/conda.sh
conda activate event-t2m

ROOT=/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/formal_candidates/trace3_formal_train_ds_review_20260603_gpu0
TRAIN_STEPS=${TRAIN_STEPS:-50000}
BATCH_SIZE=${BATCH_SIZE:-32}
mkdir -p "$ROOT"

cd /data/public/ripemangobox/Motion/MotionCLR

for VARIANT in baseline aug disploss aug_disploss; do
  OUT_DIR="$ROOT/$VARIANT"
  mkdir -p "$OUT_DIR"
  CUDA_VISIBLE_DEVICES=0 python /data/public/ripemangobox/Motion/experiments/MoDebug/scripts/trace3_formal_train_variant.py \
    --repo_dir /data/public/ripemangobox/Motion/MotionCLR \
    --out_dir "$OUT_DIR" \
    --name "trace3_${VARIANT}_seed0_steps${TRAIN_STEPS}" \
    --variant "$VARIANT" \
    --target_steps "$TRAIN_STEPS" \
    --batch_size "$BATCH_SIZE" \
    --seed 0 \
    --lr 2e-4 \
    --dropout 0.1 \
    --log_every 50 \
    --save_interval 5000 \
    --model_ema \
    --no_eff \
    --self_attention \
    --aug_prob 0.5 \
    --aug_min_scale 0.875 \
    --aug_max_scale 1.125 \
    --disp_layer unet.mid_block2 \
    --disp_lambda 0.02 \
    --disp_margin 0.2 \
    2>&1 | tee "$OUT_DIR/stdout_stderr.log"
done
