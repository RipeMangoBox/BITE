#!/usr/bin/env bash
set -euo pipefail

REPO=/data/public/ripemangobox/Motion/MoLingo
EXP_ROOT=/data/public/ripemangobox/Motion/experiments/MoDebug/molingo
SCRIPT=/data/public/ripemangobox/Motion/experiments/MoDebug/scripts/molingo_trace1_formal_layer_sweep.py
FORMAL_PROMPTS="$EXP_ROOT/prompt_sets/molingo_trace1_formal_test64_20260603.txt"

cd "$REPO"

conda run -n event-t2m python -V

DEV_OUT="$EXP_ROOT/dev_validation/molingo_trace1_formal_layer_sweep_dev_20260603_gpu1_v4"
CUDA_VISIBLE_DEVICES=1 conda run -n event-t2m python "$SCRIPT" \
  --repo_dir "$REPO" \
  --data_root /data/public/ripemangobox/Motion/datasets \
  --out_dir "$DEV_OUT" \
  --prompt_file "$REPO/assets/example.txt" \
  --prompt_limit 4 \
  --seeds 0 \
  --cfg 4.0 \
  --sample_steps 32 \
  --acc 1 \
  --run_scope dev_validation_only \
  --dev_layers 0,15

# Current formal tmux:
#   session: modebug_molingo_trace1_formal_test64_20260603
#   log: /data/public/ripemangobox/Motion/EventT2M-codes/artifacts/molingo_trace1_formal_test64_20260603_gpu1.log
FORMAL_OUT="$EXP_ROOT/formal_candidates/molingo_trace1_formal_layer_sweep_test64_ds_review_20260603_gpu1"
CUDA_VISIBLE_DEVICES=1 conda run -n event-t2m python "$SCRIPT" \
  --repo_dir "$REPO" \
  --data_root /data/public/ripemangobox/Motion/datasets \
  --out_dir "$FORMAL_OUT" \
  --prompt_file "$FORMAL_PROMPTS" \
  --prompt_limit 64 \
  --prompt_count_min 64 \
  --seeds 0,1,2 \
  --cfg 4.0 \
  --sample_steps 32 \
  --acc 1 \
  --run_scope formal_diagnostic_layer_sweep
