#!/usr/bin/env bash
set -euo pipefail

gpu="${1:-1}"
run_id="${2:-v8_2_human200_joint_ae_yaw001_root003_seed17_4090g1_20260717}"
python_bin="/home/ripemangobox/miniconda3/envs/director/bin/python"
stats="runs/train/stage1/stats/v8_2_human200_ae_train_split_20260708.json"
canonical_checkpoint="runs/train/stage1/${run_id}/checkpoints/${run_id}_last.pt"
legacy_checkpoint="runs/stage1/${run_id}/train/checkpoints/${run_id}_last.pt"
if [[ -f "$canonical_checkpoint" ]]; then
  checkpoint="${3:-$canonical_checkpoint}"
  eval_root="runs/eval/stage1/${run_id}"
else
  checkpoint="${3:-$legacy_checkpoint}"
  eval_root="runs/stage1/${run_id}/eval"
fi

export CUDA_VISIBLE_DEVICES="$gpu"
exec "$python_bin" scripts/eval_stage1_long_sequence_geometry.py \
  --pulp-root linked/PulpMotion \
  --data-root linked/pulpmotion-data \
  --human-manifest runs/train/stage1/manifests/ae_train_split_20260708/human_pure_test.jsonl \
  --camera-manifest runs/train/stage1/manifests/ae_train_split_20260708/camera_pure_test.jsonl \
  --local-model "${run_id}:storymotion_v8_2_joint_ae_human200_camera14:${checkpoint}" \
  --human200-stats "$stats" \
  --set-name pure_ --split test --expected-samples 4053 \
  --batch-size 8 --workers 4 --fixed-max-frames 300 \
  --device cuda \
  --output "${eval_root}/pure4053_long_geometry.json"
