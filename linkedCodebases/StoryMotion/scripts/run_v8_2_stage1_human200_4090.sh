#!/usr/bin/env bash
set -euo pipefail

gpu="${1:-1}"
run_id="${2:-v8_2_human200_joint_ae_yaw001_root003_seed17_4090g1_20260717}"
python_bin="/home/ripemangobox/miniconda3/envs/director/bin/python"
train_human="runs/train/stage1/manifests/ae_train_split_20260708/human_train.jsonl"
train_camera="runs/train/stage1/manifests/ae_train_split_20260708/camera_train.jsonl"
eval_human="runs/train/stage1/manifests/ae_train_split_20260708/human_pure_test.jsonl"
eval_camera="runs/train/stage1/manifests/ae_train_split_20260708/camera_pure_test.jsonl"
stats="runs/train/stage1/stats/v8_2_human200_ae_train_split_20260708.json"

CUDA_VISIBLE_DEVICES="" "$python_bin" scripts/build_v8_2_human200_stats.py \
  --train-human-manifest "$train_human" \
  --output "$stats" \
  --expected-samples 162760 \
  --num-workers 8 --chunk-size 256 --reuse-existing

export CUDA_VISIBLE_DEVICES="$gpu"
exec "$python_bin" scripts/train_storymotion_joint_tokenizer.py \
  --preset storymotion_v8_2_joint_ae_human200_camera14 \
  --feature-contract storymotion_v8_2_normalized_human200_absolute_root_yaw_joint_camera14 \
  --human200-stats "$stats" \
  --pulp-root linked/PulpMotion \
  --human-manifest "$train_human" \
  --camera-manifest "$train_camera" \
  --val-human-manifest "$eval_human" \
  --val-camera-manifest "$eval_camera" \
  --loss-config configs/stage1_loss/storymotion_stage1_v8_1_yaw_root_final.yaml \
  --non-causal --expected-train-samples 162760 \
  --batch-size 128 --eval-batch-size 64 --epochs 500 --seed 17 --lr 5e-5 \
  --num-workers 8 --pin-memory --device cuda \
  --val-every-steps 2000 --eval-every-steps 5000 --save-every-steps 25000 \
  --run-id "$run_id" --runs-root runs \
  --checkpoint-prefix "$run_id" \
  --keep-best-checkpoints 3 --keep-step-checkpoints 3
