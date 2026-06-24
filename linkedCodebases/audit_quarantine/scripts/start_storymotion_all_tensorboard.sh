#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  start_storymotion_all_tensorboard.sh [START_PORT]

Starts one TensorBoard for StoryMotion Stage1 + Stage2 logs on this machine.
Run it on 4090 and 5090 separately; both expose the same run groups when present.

Environment:
  STORYMOTION_ROOT    default /data/public/ripemangobox/Motion/StoryMotion
  STORYMOTION_PYTHON  Python executable with tensorboard installed
  STORYMOTION_CONDA_ENV default storymotion-director-cu128
  TENSORBOARD_HOST    default 0.0.0.0
  TENSORBOARD_EXTRA   extra args appended to tensorboard
USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

root="${STORYMOTION_ROOT:-/data/public/ripemangobox/Motion/StoryMotion}"
port="${1:-6019}"
host="${TENSORBOARD_HOST:-0.0.0.0}"
conda_env="${STORYMOTION_CONDA_ENV:-storymotion-director-cu128}"
python_bin="${STORYMOTION_PYTHON:-}"

if [[ -z "$python_bin" ]]; then
  if [[ -x "$HOME/miniconda3/envs/$conda_env/bin/python" ]]; then
    python_bin="$HOME/miniconda3/envs/$conda_env/bin/python"
  elif [[ -x "$HOME/miniconda3/envs/director/bin/python" ]]; then
    python_bin="$HOME/miniconda3/envs/director/bin/python"
  elif [[ -x "/data/public/ripemangobox/Motion/conda-envs/director/bin/python" ]]; then
    python_bin="/data/public/ripemangobox/Motion/conda-envs/director/bin/python"
  else
    python_bin="$(command -v python3 || true)"
  fi
fi

if [[ -z "$python_bin" || ! -x "$python_bin" ]]; then
  echo "Python executable not found. Set STORYMOTION_PYTHON." >&2
  exit 127
fi

if ! "$python_bin" -c 'import tensorboard' >/dev/null 2>&1; then
  echo "TensorBoard is not installed in: $python_bin" >&2
  exit 127
fi

port_in_use() {
  local candidate="$1"
  if command -v ss >/dev/null 2>&1; then
    ss -ltn "sport = :$candidate" | awk 'NR > 1 {found=1} END {exit !found}'
    return
  fi
  if command -v lsof >/dev/null 2>&1; then
    lsof -iTCP:"$candidate" -sTCP:LISTEN >/dev/null 2>&1
    return
  fi
  return 1
}

start_port="$port"
while port_in_use "$port"; do
  port=$((port + 1))
  if (( port - start_port > 100 )); then
    echo "No free TensorBoard port found after 100 attempts." >&2
    exit 3
  fi
done

declare -a logdirs=()
add_logdir() {
  local name="$1"
  local path="$2"
  if [[ -d "$path" ]]; then
    logdirs+=("$name:$path")
  fi
}

add_logdir "stage1_pulp192" "$root/runs/train/stage1/joint/v5_pulp192_20260621"
add_logdir "stage1_hfsq_coupling" "$root/runs/train/stage1/joint/v5_coupling_source_pulp192_20260621"
add_logdir "stage2_source_hfsq" "$root/runs/train/stage2/v5_stage1_to_stage2_20260622"
add_logdir "stage2_task_ratio" "$root/runs/train/stage2/v5_task_ratio_20260621"
add_logdir "stage2_main" "$root/runs/train/stage2"

if (( ${#logdirs[@]} == 0 )); then
  echo "No StoryMotion TensorBoard logdirs found under: $root" >&2
  exit 2
fi

joined="$(IFS=,; echo "${logdirs[*]}")"
host_ip="$(hostname -I 2>/dev/null | awk '{print $1}')"
echo "Starting StoryMotion TensorBoard"
echo "  root:   $root"
echo "  python: $python_bin"
echo "  logdir: $joined"
echo "  bind:   $host:$port"
echo "  url:    http://${host_ip:-127.0.0.1}:$port/"

exec "$python_bin" -m tensorboard.main --logdir "$joined" --host "$host" --port "$port" ${TENSORBOARD_EXTRA:-}
