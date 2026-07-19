#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 7 ]]; then
  echo "usage: $0 ACTIVE_PID GPU RUN_ID PYTHON EXPECTED_STEPS VAL_HUMAN_MANIFEST VAL_CAMERA_MANIFEST" >&2
  exit 2
fi

ACTIVE_PID="$1"
GPU="$2"
RUN_ID="$3"
PYTHON_BIN="$4"
EXPECTED_STEPS="$5"
VAL_HUMAN_MANIFEST="$6"
VAL_CAMERA_MANIFEST="$7"

ROOT=/data/public/ripemangobox/Motion/StoryMotion
PRESET=pulpmotion_joint_ae_official_199_14_pulp192
FEATURE_CONTRACT=pulpmotion_official_normalized_human199_joint_camera14
RUN_ROOT="runs/train/stage1/${RUN_ID}"
CHECKPOINT="${RUN_ROOT}/checkpoints/${RUN_ID}_last.pt"
EVAL_ROOT="runs/eval/stage1/${RUN_ID}"
LOG="runs/ops/stage1_parallel_20260719/${RUN_ID}.posteval.log"

cd "${ROOT}"
exec >>"${LOG}" 2>&1
echo "[$(date '+%F %T %Z')] waiting_for_training_process pid=${ACTIVE_PID} run_id=${RUN_ID}"

while [[ -r "/proc/${ACTIVE_PID}/cmdline" ]] && tr '\0' ' ' <"/proc/${ACTIVE_PID}/cmdline" | grep -Fq "${RUN_ID}"; do
  sleep 60
done

"${PYTHON_BIN}" - "${RUN_ROOT}/experiment_contract.json" "${EXPECTED_STEPS}" <<'PY'
import json
import sys

contract_path, expected_steps = sys.argv[1], int(sys.argv[2])
payload = json.load(open(contract_path, encoding="utf-8"))
assert payload["stage"] == "stage1"
assert payload["status"] == "trained"
assert payload["model"]["is_causal"] is False
assert payload["train"]["optimizer_steps"] == expected_steps
assert payload["train"]["sample_exposures"] == payload["train"]["epochs"] * 162760
print({"status": "endpoint_contract_precheck_passed"})
PY

"${PYTHON_BIN}" scripts/storymotion_experiment_harness.py audit-contract \
  "${RUN_ROOT}/experiment_contract.json" --verify-files
"${PYTHON_BIN}" scripts/storymotion_stage1_contract_harness.py \
  --story-root "${ROOT}" \
  --checkpoint "${CHECKPOINT}" \
  --preset "${PRESET}" \
  --tokenizer joint_ae \
  --feature-contract "${FEATURE_CONTRACT}" \
  --expected-is-causal false \
  --human-dim 199 \
  --camera-dim 14 \
  --human-latent-dim 128 \
  --camera-latent-dim 64 \
  --hidden-dim 256 \
  --downsample 4 \
  --device "cuda:${GPU}" \
  --output "${RUN_ROOT}/stage1_checkpoint_preflight_posteval.json"

mkdir -p "${EVAL_ROOT}"
CUDA_VISIBLE_DEVICES="${GPU}" "${PYTHON_BIN}" scripts/eval_stage1_long_sequence_geometry.py \
  --pulp-root linked/PulpMotion \
  --data-root linked/pulpmotion-data \
  --human-manifest "${VAL_HUMAN_MANIFEST}" \
  --camera-manifest "${VAL_CAMERA_MANIFEST}" \
  --local-model "${RUN_ID}:${PRESET}:${CHECKPOINT}" \
  --set-name pure_ \
  --split test \
  --expected-samples 4053 \
  --batch-size 8 \
  --workers 4 \
  --fixed-max-frames 300 \
  --device cuda \
  --output "${EVAL_ROOT}/pure4053_long_geometry.json"

"${PYTHON_BIN}" scripts/storymotion_run_layout.py update \
  --stage stage1 \
  --run-id "${RUN_ID}" \
  --status evaluated_stage1_geometry_nonpromotion \
  --artifact "pure4053_long_geometry=${EVAL_ROOT}/pure4053_long_geometry.json" >/dev/null
echo "[$(date '+%F %T %Z')] completed_and_evaluated run_id=${RUN_ID}"
