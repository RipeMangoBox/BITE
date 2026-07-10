#!/usr/bin/env bash
set -euo pipefail
source /home/ripemangobox/miniconda3/etc/profile.d/conda.sh
conda activate director-pulp-cu128
cd /data/public/ripemangobox/Motion/baselines/DIRECTOR_storymotion_20260626
HYDRA_FULL_ERROR=1 CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-0,1} python src/train.py \
  compnode.num_gpus=2 \
  compnode.num_workers=8 \
  dataset=traj+caption_cam \
  dataset.trajectory.set_name=mixed \
  data_dir=/data/public/ripemangobox/Motion/baselines/data/director_pulp_mixed \
  diffuser/network/module=ca_director \
  batch_size=64 \
  log_wandb=false \
  num_train_epochs=4001 \
  results_dir=/data/public/ripemangobox/Motion/baselines/runs/director_pulp_fromscratch
