#!/usr/bin/env bash
set -uo pipefail

gpu="${1:-1}"
v82_run="${2:-v8_2_human200_joint_ae_yaw001_root003_seed17_4090g1_20260717}"
v81a_run="${3:-v8_1a_joint_ae_yaw001_root003_seed17_4090g0_20260717}"
v81b_run="${4:-v8_1b_residual_ae_yaw001_root003_seed17_4090g0_20260717}"
python_bin="/home/ripemangobox/miniconda3/envs/director/bin/python"

timestamp() {
  date '+%Y-%m-%d %H:%M:%S %Z'
}

wait_for_endpoint() {
  local run_id="$1"
  local contract="runs/stage1/${run_id}/experiment_contract.json"
  local checkpoint="runs/stage1/${run_id}/train/checkpoints/${run_id}_last.pt"

  while true; do
    if [[ -f "$contract" && -f "$checkpoint" ]] && "$python_bin" -c \
      'import json,sys; raise SystemExit(0 if json.load(open(sys.argv[1]))["status"] == "trained" else 1)' \
      "$contract"; then
      echo "$(timestamp) endpoint_ready run_id=${run_id}"
      return 0
    fi
    if ! pgrep -f -- "--run-id ${run_id}" >/dev/null; then
      echo "$(timestamp) endpoint_failed run_id=${run_id} reason=trainer_not_running" >&2
      return 1
    fi
    sleep 30
  done
}

run_eval() {
  local run_id="$1"
  shift
  if ! wait_for_endpoint "$run_id"; then
    return 1
  fi
  echo "$(timestamp) eval_start run_id=${run_id} gpu=${gpu}"
  "$@"
  local rc=$?
  echo "$(timestamp) eval_end run_id=${run_id} rc=${rc}"
  return "$rc"
}

failures=0
run_eval "$v82_run" bash scripts/eval_v8_2_stage1_human200_pure4053_4090.sh "$gpu" "$v82_run" || failures=$((failures + 1))
run_eval "$v81a_run" bash scripts/eval_v8_1_stage1_pure4053_4090.sh "$gpu" "$v81a_run" pulpmotion_joint_ae_official_199_14_pulp192 || failures=$((failures + 1))
run_eval "$v81b_run" bash scripts/eval_v8_1_stage1_pure4053_4090.sh "$gpu" "$v81b_run" storymotion_v8_1b_residual_joint_ae_199_14 || failures=$((failures + 1))

echo "$(timestamp) queue_end failures=${failures}"
exit "$failures"
