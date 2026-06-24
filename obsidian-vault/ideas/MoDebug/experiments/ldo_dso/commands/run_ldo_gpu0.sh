#!/usr/bin/env bash
set -euo pipefail

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT=${EXP_ROOT:-$MOTION_ROOT/experiments/MoDebug}
SCRIPT=${SCRIPT:-$EXP_ROOT/ldo_dso/scripts/modebug_ldo_audit_runner.py}
OUT_DIR=${OUT_DIR:-$EXP_ROOT/ldo_dso/formal_20260608/ldo_gpu0}
PROMPTS=${PROMPTS:-$EXP_ROOT/molingo/prompt_sets/molingo_trace1_formal_test64_20260603.txt}

source /home/ripemangobox/miniconda3/etc/profile.d/conda.sh
conda activate event-t2m

CUDA_VISIBLE_DEVICES=0 python "$SCRIPT" \
  --out_dir "$OUT_DIR" \
  --mode all \
  --gpu_id 0 \
  --motionclr_repo "$MOTION_ROOT/MotionCLR" \
  --motiongpt_repo "$MOTION_ROOT/MotionGPT" \
  --molingo_repo "$MOTION_ROOT/MoLingo" \
  --data_root "$MOTION_ROOT/datasets" \
  --prompt_file "$PROMPTS" \
  --prompt_limit "${PROMPT_LIMIT:-64}" \
  --prompt_count_min "${PROMPT_COUNT_MIN:-64}" \
  --seeds "${SEEDS:-0,1,2}" \
  --dim_pose "${DIM_POSE:-272}" \
  --cfg "${CFG:-4.0}" \
  --sample_steps "${SAMPLE_STEPS:-32}" \
  --acc "${ACC:-1}"
