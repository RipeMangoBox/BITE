#!/usr/bin/env bash
set -euo pipefail

ROOT=${ROOT:-/data/public/ripemangobox/Motion/StoryMotion}
PY=${PY:-/home/ripemangobox/miniconda3/envs/storymotion-director-cu128/bin/python}
OUT=${OUT:-runs/eval/storymotion_official_full_eval_20260613}
CACHE=${CACHE:-runs/train/stage2/pulp_official_full_mixed_20260611/cache_mixed_full_nw0_20260611_2110}
BATCH_SIZE=${BATCH_SIZE:-64}
NUM_STEPS=${NUM_STEPS:-50}
SEED=${SEED:-20260613}

cd "$ROOT"
mkdir -p "$OUT/logs"

run_job() {
  local name=$1
  local gpu=$2
  local task=$3
  local run_dir=$4
  local log="$OUT/logs/${name}.log"
  local marker="$OUT/logs/${name}.marker"
  local output="$OUT/${name}.json"

  {
    echo "started_at=$(date -Is)"
    echo "name=$name gpu=$gpu task=$task run_dir=$run_dir"
    CUDA_VISIBLE_DEVICES="$gpu" "$PY" scripts/storymotion_official_full_eval.py \
      --run-dir "$run_dir" \
      --cache-dir "$CACHE" \
      --task "$task" \
      --samples 0 \
      --batch-size "$BATCH_SIZE" \
      --workers 0 \
      --num-steps "$NUM_STEPS" \
      --seed "$SEED" \
      --output "$output"
    status=$?
    echo "finished_at=$(date -Is)"
    echo "exit:$status" > "$marker"
    return "$status"
  } > "$log" 2>&1
}

if (( $# % 4 != 0 || $# == 0 )); then
  echo "usage: $0 NAME GPU TASK RUN_DIR [NAME GPU TASK RUN_DIR ...]" >&2
  exit 2
fi

while (( $# > 0 )); do
  run_job "$1" "$2" "$3" "$4"
  shift 4
done
