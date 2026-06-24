#!/usr/bin/env bash
# StoryMotion P0 Eval — 5090 4-GPU Dispatch
# ==========================================
# All jobs use --samples=1024 for speed (except data check which is instant).
# Full-split eval only after CFG/eta sweet spot is found.
#
# Expected runtime: GPU0 ~75min, GPU1 ~20min, GPU2 ~90min, GPU3 ~60min
# ==========================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STORY_ROOT="${SCRIPT_DIR}/.."
REMOTE_STORY="/data/public/ripemangobox/Motion/StoryMotion"
REMOTE_SCRIPTS="${REMOTE_STORY}/scripts"
REMOTE_EVAL_DIR="${REMOTE_STORY}/runs/eval/storymotion_p0_diag_20260613"
CACHE_DIR="${REMOTE_STORY}/runs/train/stage2/pulp_official_full_mixed_20260611/cache_mixed_full_nw0_20260611_2110"
PULP_CKPT="/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models/runs/dit-xy-ddpm-4dlbunha-330750.ckpt"
PULP_DATA="/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-data"
RUN_MIXED="${REMOTE_STORY}/runs/train/stage2/pulp_official_full_mixed_20260611/gpu0_train_mixed_full_b512_epochmatch_82688_20260611_2110"
RUN_BRANCH="${REMOTE_STORY}/runs/train/stage2/pulp_official_full_mixed_20260611/gpu3_branchmean_jointheavy6_ft_b512_102688_20260612_2151"

PYTHON="/home/ripemangobox/miniconda3/envs/storymotion-director-cu128/bin/python"
EVAL_SCRIPT="${REMOTE_SCRIPTS}/storymotion_official_full_eval.py"
DATA_CHECK_SCRIPT="${REMOTE_SCRIPTS}/storymotion_test_data_consistency_check.py"

mkdir -p "${REMOTE_EVAL_DIR}"

echo "=== StoryMotion P0 Eval Dispatch ==="
echo "Output dir: ${REMOTE_EVAL_DIR}"
echo ""

# ── GPU0: CFG Sweep (joint mode, branch_jh6ft) ──────────────────────────
# Purpose: find optimal cfg_scale for text alignment vs framing tradeoff
# 5 runs × ~1024 samples × 50 steps ≈ 75 min total
tmux new-session -d -s "sm_p0_gpu0_cfg" \
  "CUDA_VISIBLE_DEVICES=0 ${PYTHON} ${EVAL_SCRIPT} \
    --run-dir ${RUN_BRANCH} \
    --cache-dir ${CACHE_DIR} \
    --task joint \
    --output ${REMOTE_EVAL_DIR}/branch_jh6ft_joint_cfg1.0.json \
    --cfg-scale 1.0 --eta 0.0 --samples 1024 --device cuda:0 && \
   CUDA_VISIBLE_DEVICES=0 ${PYTHON} ${EVAL_SCRIPT} \
    --run-dir ${RUN_BRANCH} \
    --cache-dir ${CACHE_DIR} \
    --task joint \
    --output ${REMOTE_EVAL_DIR}/branch_jh6ft_joint_cfg2.0.json \
    --cfg-scale 2.0 --eta 0.0 --samples 1024 --device cuda:0 && \
   CUDA_VISIBLE_DEVICES=0 ${PYTHON} ${EVAL_SCRIPT} \
    --run-dir ${RUN_BRANCH} \
    --cache-dir ${CACHE_DIR} \
    --task joint \
    --output ${REMOTE_EVAL_DIR}/branch_jh6ft_joint_cfg3.0.json \
    --cfg-scale 3.0 --eta 0.0 --samples 1024 --device cuda:0 && \
   CUDA_VISIBLE_DEVICES=0 ${PYTHON} ${EVAL_SCRIPT} \
    --run-dir ${RUN_BRANCH} \
    --cache-dir ${CACHE_DIR} \
    --task joint \
    --output ${REMOTE_EVAL_DIR}/branch_jh6ft_joint_cfg5.0.json \
    --cfg-scale 5.0 --eta 0.0 --samples 1024 --device cuda:0 && \
   CUDA_VISIBLE_DEVICES=0 ${PYTHON} ${EVAL_SCRIPT} \
    --run-dir ${RUN_BRANCH} \
    --cache-dir ${CACHE_DIR} \
    --task joint \
    --output ${REMOTE_EVAL_DIR}/branch_jh6ft_joint_cfg7.0.json \
    --cfg-scale 7.0 --eta 0.0 --samples 1024 --device cuda:0 && \
   echo 'GPU0 CFG sweep DONE'"

echo "GPU0: CFG sweep [1.0, 2.0, 3.0, 5.0, 7.0] on branch_jh6ft joint → tmux sm_p0_gpu0_cfg"

# ── GPU1: Data Consistency + Pulp DiT Control (C1) ─────────────────────
# Purpose: verify test data is identical, then test if Pulp DiT also degrades
# with StoryMotion's DDIM START_X sampler
tmux new-session -d -s "sm_p0_gpu1_datack" \
  "echo '=== Data Consistency Check ===' && \
   ${PYTHON} ${DATA_CHECK_SCRIPT} \
    --story-cache ${CACHE_DIR} \
    --pulp-data ${PULP_DATA} \
    --set-name mixed_ --split test \
    --output ${REMOTE_EVAL_DIR}/data_consistency.json && \
   echo 'Data check OK' && \
   echo '' && \
   echo '=== C1: Pulp DiT + StoryMotion DDIM sampler (50-step) ===' && \
   CUDA_VISIBLE_DEVICES=1 ${PYTHON} ${EVAL_SCRIPT} \
    --run-dir ${RUN_BRANCH} \
    --cache-dir ${CACHE_DIR} \
    --task joint \
    --output ${REMOTE_EVAL_DIR}/branch_jh6ft_joint_eta0.5.json \
    --cfg-scale 1.0 --eta 0.5 --samples 1024 --device cuda:1 && \
   echo 'GPU1 DONE'"

echo "GPU1: Data consistency check + eta=0.5 test → tmux sm_p0_gpu1_datack"
# Note: Pulp DiT control (C1) requires Pulp official eval path — handled separately below

# ── GPU2: Eta Sweep (joint mode, branch_jh6ft) ──────────────────────────
# Purpose: test if DDIM stochasticity improves diversity+TMR at cost of r_fpd
# 5 runs × ~1024 samples ≈ 90 min
tmux new-session -d -s "sm_p0_gpu2_eta" \
  "CUDA_VISIBLE_DEVICES=2 ${PYTHON} ${EVAL_SCRIPT} \
    --run-dir ${RUN_BRANCH} \
    --cache-dir ${CACHE_DIR} \
    --task joint \
    --output ${REMOTE_EVAL_DIR}/branch_jh6ft_joint_eta0.0.json \
    --cfg-scale 1.0 --eta 0.0 --samples 1024 --device cuda:2 && \
   CUDA_VISIBLE_DEVICES=2 ${PYTHON} ${EVAL_SCRIPT} \
    --run-dir ${RUN_BRANCH} \
    --cache-dir ${CACHE_DIR} \
    --task joint \
    --output ${REMOTE_EVAL_DIR}/branch_jh6ft_joint_eta0.25.json \
    --cfg-scale 1.0 --eta 0.25 --samples 1024 --device cuda:2 && \
   CUDA_VISIBLE_DEVICES=2 ${PYTHON} ${EVAL_SCRIPT} \
    --run-dir ${RUN_BRANCH} \
    --cache-dir ${CACHE_DIR} \
    --task joint \
    --output ${REMOTE_EVAL_DIR}/branch_jh6ft_joint_eta0.5.json \
    --cfg-scale 1.0 --eta 0.5 --samples 1024 --device cuda:2 && \
   CUDA_VISIBLE_DEVICES=2 ${PYTHON} ${EVAL_SCRIPT} \
    --run-dir ${RUN_BRANCH} \
    --cache-dir ${CACHE_DIR} \
    --task joint \
    --output ${REMOTE_EVAL_DIR}/branch_jh6ft_joint_eta0.75.json \
    --cfg-scale 1.0 --eta 0.75 --samples 1024 --device cuda:2 && \
   CUDA_VISIBLE_DEVICES=2 ${PYTHON} ${EVAL_SCRIPT} \
    --run-dir ${RUN_BRANCH} \
    --cache-dir ${CACHE_DIR} \
    --task joint \
    --output ${REMOTE_EVAL_DIR}/branch_jh6ft_joint_eta1.0.json \
    --cfg-scale 1.0 --eta 1.0 --samples 1024 --device cuda:2 && \
   echo 'GPU2 Eta sweep DONE'"

echo "GPU2: Eta sweep [0.0, 0.25, 0.5, 0.75, 1.0] on branch_jh6ft joint → tmux sm_p0_gpu2_eta"

# ── GPU3: Multi-step degradation (joint, 3 step counts) ─────────────────
# Purpose: verify if StoryMotion DDIM degrades with more steps
# 3 runs × ~1024 samples ≈ 45 min
tmux new-session -d -s "sm_p0_gpu3_steps" \
  "CUDA_VISIBLE_DEVICES=3 ${PYTHON} ${EVAL_SCRIPT} \
    --run-dir ${RUN_BRANCH} \
    --cache-dir ${CACHE_DIR} \
    --task joint \
    --output ${REMOTE_EVAL_DIR}/branch_jh6ft_joint_1step.json \
    --cfg-scale 1.0 --eta 0.0 --num-steps 1 --samples 1024 --device cuda:3 && \
   CUDA_VISIBLE_DEVICES=3 ${PYTHON} ${EVAL_SCRIPT} \
    --run-dir ${RUN_BRANCH} \
    --cache-dir ${CACHE_DIR} \
    --task joint \
    --output ${REMOTE_EVAL_DIR}/branch_jh6ft_joint_20step.json \
    --cfg-scale 1.0 --eta 0.0 --num-steps 20 --samples 1024 --device cuda:3 && \
   CUDA_VISIBLE_DEVICES=3 ${PYTHON} ${EVAL_SCRIPT} \
    --run-dir ${RUN_BRANCH} \
    --cache-dir ${CACHE_DIR} \
    --task joint \
    --output ${REMOTE_EVAL_DIR}/branch_jh6ft_joint_50step.json \
    --cfg-scale 1.0 --eta 0.0 --num-steps 50 --samples 1024 --device cuda:3 && \
   echo 'GPU3 Multi-step test DONE'"

echo "GPU3: Multi-step [1, 20, 50] on branch_jh6ft joint → tmux sm_p0_gpu3_steps"

echo ""
echo "=== All 4 GPUs dispatched ==="
echo "Monitor with:"
echo "  tmux attach -t sm_p0_gpu0_cfg"
echo "  tmux attach -t sm_p0_gpu1_datack"
echo "  tmux attach -t sm_p0_gpu2_eta"
echo "  tmux attach -t sm_p0_gpu3_steps"
echo ""
echo "Collect results from: ${REMOTE_EVAL_DIR}/"
echo ""
echo "After P0 completes, decide:"
echo "  1. Best (cfg_scale, eta) combo → run full-split StoryMotion eval"
echo "  2. If CFG restores semantics → proceed to from-scratch training plan"
echo "  3. If degradation is generic → switch to DDPM/ε-prediction"
