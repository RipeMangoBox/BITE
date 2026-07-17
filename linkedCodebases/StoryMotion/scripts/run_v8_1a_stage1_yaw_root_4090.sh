#!/usr/bin/env bash
set -euo pipefail

gpu="${1:-0}"
run_id="${2:-v8_1a_joint_ae_yaw001_root003_seed17_4090g0_20260717}"

export CUDA_VISIBLE_DEVICES="$gpu"
exec /home/ripemangobox/miniconda3/envs/director/bin/python scripts/train_storymotion_joint_tokenizer.py \
  --preset pulpmotion_joint_ae_official_199_14_pulp192 \
  --feature-contract pulpmotion_official_normalized_human199_joint_camera14 \
  --pulp-root linked/PulpMotion \
  --human-manifest runs/train/stage1/manifests/ae_train_split_20260708/human_train.jsonl \
  --camera-manifest runs/train/stage1/manifests/ae_train_split_20260708/camera_train.jsonl \
  --val-human-manifest runs/train/stage1/manifests/ae_train_split_20260708/human_pure_test.jsonl \
  --val-camera-manifest runs/train/stage1/manifests/ae_train_split_20260708/camera_pure_test.jsonl \
  --loss-config configs/stage1_loss/storymotion_stage1_v8_1_yaw_root_final.yaml \
  --non-causal \
  --batch-size 128 --epochs 500 --lr 5e-5 \
  --num-workers 8 --pin-memory --device cuda \
  --val-every-steps 2000 --eval-every-steps 5000 --save-every-steps 25000 \
  --run-id "$run_id" --runs-root runs \
  --checkpoint-prefix "$run_id" \
  --keep-best-checkpoints 3 --keep-step-checkpoints 3
