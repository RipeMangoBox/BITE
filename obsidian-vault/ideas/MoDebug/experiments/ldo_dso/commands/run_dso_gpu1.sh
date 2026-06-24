#!/usr/bin/env bash
set -euo pipefail

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT=${EXP_ROOT:-$MOTION_ROOT/experiments/MoDebug}
SCRIPT=${SCRIPT:-$EXP_ROOT/ldo_dso/scripts/modebug_dso_motionclr_runner.py}
OUT_DIR=${OUT_DIR:-$EXP_ROOT/ldo_dso/formal_20260608/dso_gpu1_motionclr}

source /home/ripemangobox/miniconda3/etc/profile.d/conda.sh
conda activate event-t2m

CUDA_VISIBLE_DEVICES=1 python "$SCRIPT" \
  --repo_dir "$MOTION_ROOT/MotionCLR" \
  --out_dir "$OUT_DIR" \
  --gpu_id 0 \
  --seed "${SEED:-42}" \
  --batch_size "${BATCH_SIZE:-32}" \
  --replication_times "${REPLICATION_TIMES:-1}" \
  --num_inference_steps "${NUM_INFERENCE_STEPS:-10}" \
  --dso_endpoints "${DSO_ENDPOINTS:-ac3d}" \
  --cfg_scale "${CFG_SCALE:-2.5}" \
  --evaluator_dir ./data/pretrained_models \
  --eval_meta_dir ./data \
  --glove_dir ./data/glove \
  --no_eff \
  --self_attention \
  --no_fp16
