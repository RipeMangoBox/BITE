#!/usr/bin/env bash
set -euo pipefail

RUN_DIR=/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/track_b_ca_perturbation/20260602_gpu1_track_b_ca_cfg_sweep_mvp
REPO_DIR=/data/public/ripemangobox/Motion/MotionCLR

mkdir -p "$RUN_DIR"
cd "$REPO_DIR"
source /home/ripemangobox/miniconda3/etc/profile.d/conda.sh

{
  echo "start_time=$(date --iso-8601=seconds)"
  echo "host=$(hostname)"
  echo "CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-}"
  nvidia-smi
} > "$RUN_DIR/nvidia_smi_start_end.txt"

CUDA_VISIBLE_DEVICES=1 conda run -n event-t2m python "$RUN_DIR/track_b_ca_cfg_sweep.py" \
  --repo_dir "$REPO_DIR" \
  --out_dir "$RUN_DIR" \
  --opt_path ./checkpoints/t2m/release/opt.txt \
  --prompt_limit 1 \
  --num_inference_steps 2 \
  --seed 0 \
  --gpu_id 0 \
  --batch_size 1 \
  --layers all \
  --no_fp16

{
  echo "end_time=$(date --iso-8601=seconds)"
  CUDA_VISIBLE_DEVICES=1 nvidia-smi
} >> "$RUN_DIR/nvidia_smi_start_end.txt"
