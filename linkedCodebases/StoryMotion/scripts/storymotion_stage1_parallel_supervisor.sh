#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 12 ]]; then
  echo "usage: $0 GPU RUN_ID SEED EPOCHS EXPECTED_STEPS PYTHON LOSS_CONFIG HUMAN_MANIFEST CAMERA_MANIFEST VAL_HUMAN_MANIFEST VAL_CAMERA_MANIFEST SCOPE" >&2
  exit 2
fi

GPU="$1"
RUN_ID="$2"
SEED="$3"
EPOCHS="$4"
EXPECTED_STEPS="$5"
PYTHON_BIN="$6"
LOSS_CONFIG="$7"
HUMAN_MANIFEST="$8"
CAMERA_MANIFEST="$9"
VAL_HUMAN_MANIFEST="${10}"
VAL_CAMERA_MANIFEST="${11}"
SCOPE="${12}"

ROOT=/data/public/ripemangobox/Motion/StoryMotion
PRESET=pulpmotion_joint_ae_official_199_14_pulp192
FEATURE_CONTRACT=pulpmotion_official_normalized_human199_joint_camera14
RUN_ROOT="runs/train/stage1/${RUN_ID}"
CHECKPOINT="${RUN_ROOT}/checkpoints/${RUN_ID}_last.pt"
EVAL_ROOT="runs/eval/stage1/${RUN_ID}"
OPS_ROOT=runs/ops/stage1_parallel_20260719
LOG="${OPS_ROOT}/${RUN_ID}.log"

cd "${ROOT}"
mkdir -p "${OPS_ROOT}"

if [[ -e "${RUN_ROOT}" ]]; then
  echo "fresh-init violation: run root already exists: ${RUN_ROOT}" >&2
  exit 2
fi
for path in "${PYTHON_BIN}" "${LOSS_CONFIG}" "${HUMAN_MANIFEST}" "${CAMERA_MANIFEST}" "${VAL_HUMAN_MANIFEST}" "${VAL_CAMERA_MANIFEST}"; do
  if [[ ! -e "${path}" ]]; then
    echo "missing required path: ${path}" >&2
    exit 2
  fi
done

finish_failed() {
  status=$?
  echo "[$(date '+%F %T %Z')] failed status=${status}"
  if [[ -d "${RUN_ROOT}" ]]; then
    "${PYTHON_BIN}" scripts/storymotion_run_layout.py update --stage stage1 --run-id "${RUN_ID}" --status failed >/dev/null 2>&1 || true
  fi
  exit "${status}"
}
trap finish_failed ERR

exec >>"${LOG}" 2>&1
echo "[$(date '+%F %T %Z')] supervisor_start run_id=${RUN_ID} gpu=${GPU} seed=${SEED} epochs=${EPOCHS} expected_steps=${EXPECTED_STEPS}"
echo "scope=${SCOPE}"
echo "source_git_head=$(git rev-parse HEAD)"
echo "source_git_dirty_count=$(git status --porcelain | wc -l | tr -d ' ')"
echo "loss_config_sha256=$(sha256sum "${LOSS_CONFIG}" | awk '{print $1}')"
echo "trainer_sha256=$(sha256sum scripts/train_storymotion_joint_tokenizer.py | awk '{print $1}')"
echo "tokenizer_sha256=$(sha256sum storymotion/tokenizers/joint_human_camera.py | awk '{print $1}')"
echo "invariants_sha256=$(sha256sum storymotion/experiment_invariants.py | awk '{print $1}')"

"${PYTHON_BIN}" - "${LOSS_CONFIG}" "${SEED}" "${EPOCHS}" "${EXPECTED_STEPS}" <<'PY'
import math
import sys
import yaml

config_path, seed, epochs, expected_steps = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
payload = yaml.safe_load(open(config_path, encoding="utf-8"))
assert payload["stage1_model"]["is_causal"] is False
loss = payload["stage1_loss"]
assert math.isclose(float(loss["human_yaw_weight"]), 0.001, rel_tol=0.0, abs_tol=1e-15)
assert math.isclose(float(loss["human_root_weight"]), 0.003, rel_tol=0.0, abs_tol=1e-15)
assert float(loss.get("camera_center_weight", 0.0)) >= 0.0
camera_rotation_weight = float(loss.get("camera_rotation_weight", 0.0))
human_horizon_weight = float(loss.get("human_horizon_weight", 0.0))
human_multi_horizon_weight = float(loss.get("human_multi_horizon_weight", 0.0))
assert camera_rotation_weight >= 0.0 and human_horizon_weight >= 0.0 and human_multi_horizon_weight >= 0.0
assert sum(weight > 0.0 for weight in (camera_rotation_weight, human_horizon_weight, human_multi_horizon_weight)) <= 1
assert float(loss.get("camera_recon_weight", 1.0)) > 0.0
assert seed >= 0 and epochs > 0 and expected_steps == epochs * 1272
print({"status": "preflight_passed", "seed": seed, "epochs": epochs, "expected_steps": expected_steps})
PY

"${PYTHON_BIN}" scripts/train_storymotion_joint_tokenizer.py \
  --preset "${PRESET}" \
  --feature-contract "${FEATURE_CONTRACT}" \
  --pulp-root linked/PulpMotion \
  --human-manifest "${HUMAN_MANIFEST}" \
  --camera-manifest "${CAMERA_MANIFEST}" \
  --val-human-manifest "${VAL_HUMAN_MANIFEST}" \
  --val-camera-manifest "${VAL_CAMERA_MANIFEST}" \
  --loss-config "${LOSS_CONFIG}" \
  --non-causal \
  --batch-size 128 \
  --eval-batch-size 8 \
  --epochs "${EPOCHS}" \
  --expected-train-samples 162760 \
  --lr 5e-5 \
  --num-workers 8 \
  --pin-memory \
  --device "cuda:${GPU}" \
  --seed "${SEED}" \
  --val-every-steps 2000 \
  --eval-every-steps 5000 \
  --save-every-steps 25000 \
  --run-id "${RUN_ID}" \
  --runs-root runs \
  --checkpoint-prefix "${RUN_ID}" \
  --keep-best-checkpoints 3 \
  --keep-step-checkpoints 3

"${PYTHON_BIN}" - "${RUN_ROOT}/experiment_contract.json" "${EXPECTED_STEPS}" "${SEED}" "${EPOCHS}" <<'PY'
import json
import sys
import time

contract_path = sys.argv[1]
expected_steps, expected_seed, expected_epochs = map(int, sys.argv[2:5])
for attempt in range(10):
    payload = json.load(open(contract_path, encoding="utf-8"))
    checks = {
        "stage": payload["stage"] == "stage1",
        "status": payload["status"] == "trained",
        "non_causal": payload["model"]["is_causal"] is False,
        "seed": payload["train"]["seed"] == expected_seed,
        "optimizer_steps": payload["train"]["optimizer_steps"] == expected_steps,
        "sample_exposures": payload["train"]["sample_exposures"] == expected_epochs * 162760,
    }
    if all(checks.values()):
        print({"status": "endpoint_contract_precheck_passed", "attempt": attempt + 1})
        break
    time.sleep(1.0)
else:
    raise AssertionError(checks)
PY

"${PYTHON_BIN}" scripts/storymotion_experiment_harness.py audit-contract "${RUN_ROOT}/experiment_contract.json" --verify-files
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

echo "[$(date '+%F %T %Z')] endpoint_audited; pure4053_start"
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
