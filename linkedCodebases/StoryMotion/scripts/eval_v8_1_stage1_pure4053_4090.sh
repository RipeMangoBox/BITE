#!/usr/bin/env bash
set -euo pipefail

gpu="${1:-1}"
run_id="${2:?usage: $0 GPU RUN_ID PRESET [CHECKPOINT]}"
preset="${3:?usage: $0 GPU RUN_ID PRESET [CHECKPOINT]}"
checkpoint="${4:-runs/stage1/${run_id}/train/checkpoints/${run_id}_last.pt}"
python_bin="/home/ripemangobox/miniconda3/envs/director/bin/python"

case "$preset" in
  pulpmotion_joint_ae_official_199_14_pulp192|storymotion_v8_1b_residual_joint_ae_199_14)
    ;;
  *)
    echo "unsupported v8.1 preset: $preset" >&2
    exit 2
    ;;
esac

if [[ ! -f "$checkpoint" ]]; then
  echo "missing Stage1 endpoint checkpoint: $checkpoint" >&2
  exit 2
fi

export CUDA_VISIBLE_DEVICES="$gpu"
exec "$python_bin" scripts/eval_stage1_long_sequence_geometry.py \
  --pulp-root linked/PulpMotion \
  --data-root linked/pulpmotion-data \
  --human-manifest runs/train/stage1/manifests/ae_train_split_20260708/human_pure_test.jsonl \
  --camera-manifest runs/train/stage1/manifests/ae_train_split_20260708/camera_pure_test.jsonl \
  --local-model "${run_id}:${preset}:${checkpoint}" \
  --set-name pure_ --split test --expected-samples 4053 \
  --batch-size 8 --workers 4 --fixed-max-frames 300 \
  --device cuda \
  --output "runs/stage1/${run_id}/eval/pure4053_long_geometry.json"
