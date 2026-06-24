#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  start_stage2_tensorboard.sh [LOGDIR] [START_PORT]

Defaults:
  LOGDIR      ${STORYMOTION_ROOT:-/data/public/ripemangobox/Motion/StoryMotion}/runs/train/stage2
  START_PORT 6006

Environment:
  STORYMOTION_ROOT  StoryMotion checkout root when LOGDIR is omitted.
  STORYMOTION_PYTHON Python executable used to run TensorBoard.
  STORYMOTION_CONDA_ENV
                    Conda env name used when STORYMOTION_PYTHON is omitted,
                    default storymotion-director-cu128.
  CONDA_PREFIX      Used to infer STORYMOTION_PYTHON when it matches the env.
  TENSORBOARD_HOST  Bind host, default 0.0.0.0.
  TENSORBOARD_BIN   TensorBoard executable; overrides STORYMOTION_PYTHON.
  TENSORBOARD_EXTRA Extra arguments appended to tensorboard.

The script increments the port until it finds a free one.
USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

storymotion_root="${STORYMOTION_ROOT:-/data/public/ripemangobox/Motion/StoryMotion}"
logdir="${1:-$storymotion_root/runs/train/stage2}"
port="${2:-6006}"
host="${TENSORBOARD_HOST:-0.0.0.0}"
conda_env="${STORYMOTION_CONDA_ENV:-storymotion-director-cu128}"
python_bin="${STORYMOTION_PYTHON:-}"
tensorboard_bin="${TENSORBOARD_BIN:-}"
max_tries="${TENSORBOARD_PORT_TRIES:-100}"

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
  if command -v nc >/dev/null 2>&1; then
    nc -z 127.0.0.1 "$candidate" >/dev/null 2>&1
    return
  fi
  return 1
}

if [[ ! -d "$logdir" ]]; then
  echo "Logdir does not exist: $logdir" >&2
  exit 2
fi

if [[ -z "$tensorboard_bin" ]]; then
  if [[ -n "$python_bin" ]]; then
    :
  elif [[ -n "${CONDA_PREFIX:-}" && -x "$CONDA_PREFIX/bin/python" ]]; then
    python_bin="$CONDA_PREFIX/bin/python"
  elif [[ -x "$HOME/miniconda3/envs/$conda_env/bin/python" ]]; then
    python_bin="$HOME/miniconda3/envs/$conda_env/bin/python"
  elif [[ -x "$HOME/anaconda3/envs/$conda_env/bin/python" ]]; then
    python_bin="$HOME/anaconda3/envs/$conda_env/bin/python"
  fi

  if [[ -z "$python_bin" || ! -x "$python_bin" ]]; then
    echo "Python executable for TensorBoard not found." >&2
    echo "Set STORYMOTION_PYTHON, TENSORBOARD_BIN, or activate the training environment." >&2
    exit 127
  fi
  if ! "$python_bin" -c 'import tensorboard' >/dev/null 2>&1; then
    echo "TensorBoard is not installed in: $python_bin" >&2
    echo "Install it with: $python_bin -m pip install tensorboard" >&2
    exit 127
  fi
else
  if ! command -v "$tensorboard_bin" >/dev/null 2>&1; then
    echo "TensorBoard executable not found: $tensorboard_bin" >&2
    echo "Set TENSORBOARD_BIN, STORYMOTION_PYTHON, or activate the training environment." >&2
    exit 127
  fi
fi

tries=0
while port_in_use "$port"; do
  port=$((port + 1))
  tries=$((tries + 1))
  if (( tries >= max_tries )); then
    echo "No free port found after $max_tries attempts." >&2
    exit 3
  fi
done

echo "Starting TensorBoard"
echo "  logdir: $logdir"
echo "  bind:   $host:$port"
echo "  url:    http://$(hostname -I 2>/dev/null | awk '{print $1}'):$port/"

if [[ -n "$tensorboard_bin" ]]; then
  exec "$tensorboard_bin" --logdir "$logdir" --host "$host" --port "$port" ${TENSORBOARD_EXTRA:-}
fi
exec "$python_bin" -m tensorboard.main --logdir "$logdir" --host "$host" --port "$port" ${TENSORBOARD_EXTRA:-}
