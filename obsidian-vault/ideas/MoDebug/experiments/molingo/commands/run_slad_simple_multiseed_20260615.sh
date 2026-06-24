#!/usr/bin/env bash
set -euo pipefail
# Simplified SLAD Multi-Seed Validation (2026-06-15)
# Implements: two-phase ω scheduling only (no GDC/decouple/project)
#   Pre-split (step < 25/50): ω = 5.5 (standard CFG)
#   Post-split (step >= 25/50): ω = 1.5 (weak guidance)
#
# Usage: GPU=0 PROMPT_SET=action bash run_slad_simple_multiseed_20260615.sh
#        GPU=1 PROMPT_SET=attribute bash run_slad_simple_multiseed_20260615.sh

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT="$MOTION_ROOT/experiments/MoDebug"
REPO="$MOTION_ROOT/MoLingo"
SCRIPT="$EXP_ROOT/molingo/scripts/modebug_slad.py"

GPU=${GPU:-0}
CONDA_ENV=${CONDA_ENV:-event-t2m}
CONDA_BIN=${CONDA_BIN:-/home/ripemangobox/miniconda3/bin/conda}
T5_PATH=${T5_PATH:-/data/public/ripemangobox/Motion/Text-encoder/t5-large}

# Shared settings
SEEDS=${SEEDS:-3407,2026,42}
DIRECTIONS=${DIRECTIONS:-a_to_b,b_to_a}
SWAP_ITERATIONS=${SWAP_ITERATIONS:-all}
CFG=${CFG:-5.5}
SAMPLE_STEPS=${SAMPLE_STEPS:-32}
ACC=${ACC:-3}
TRACE_DETAIL=${TRACE_DETAIL:-aggregate}

# Simplified SLAD settings
SLAD_SPLIT=${SLAD_SPLIT:-0.5}        # timestep fraction → outer step ~25/50
SLAD_OMEGA_POST=${SLAD_OMEGA_POST:-1.5}  # post-split ω

PROMPT_SET=${PROMPT_SET:-action}
SKIP_UNTIL=${SKIP_UNTIL:-0}
RUN_STAMP=${RUN_STAMP:-20260615_simple_multiseed_${PROMPT_SET}_gpu${GPU}}

if [[ "$PROMPT_SET" == "action" ]]; then
    PROMPT_PAIR_FILE="$EXP_ROOT/molingo/prompt_sets/slad_m0_gpu0_action_control_20260613.tsv"
    DIM_LABEL="action_control"
else
    PROMPT_PAIR_FILE="$EXP_ROOT/molingo/prompt_sets/slad_m0_gpu1_attribute_direction_20260613.tsv"
    DIM_LABEL="attribute_direction"
fi

SLAD_ROOT="$EXP_ROOT/molingo/slad/slad_simple_${DIM_LABEL}_${RUN_STAMP}"

log() {
    printf '[%(%F %T)T] %s\n' -1 "$*"
}

run_condition() {
    local cond_name="$1"; shift
    local out_dir="$SLAD_ROOT/$cond_name"

    mkdir -p "$out_dir"
    log "=== GPU$GPU $cond_name ==="
    log "OUT_DIR=$out_dir"

    cd "$REPO"
    CUDA_VISIBLE_DEVICES="$GPU" \
    TRANSFORMERS_OFFLINE=1 \
    HF_HUB_OFFLINE=1 \
    MOLINGO_T5_PATH="$T5_PATH" \
    MODEBUG_DEPLOYED_FROM="BITE_Process/obsidian-vault/ideas/MoDebug/experiments/molingo" \
    MODEBUG_COMMAND_SCRIPT="${BASH_SOURCE[0]}" \
    "$CONDA_BIN" run -n "$CONDA_ENV" --no-capture-output python "$SCRIPT" \
        --experiment m0_swap \
        --repo_dir "$REPO" \
        --out_dir "$out_dir" \
        --prompt_pair_file "$PROMPT_PAIR_FILE" \
        --seeds "$SEEDS" \
        --directions "$DIRECTIONS" \
        --swap_iterations "$SWAP_ITERATIONS" \
        --cfg "$CFG" \
        --cfg_schedule slad_simple \
        --slad_split "$SLAD_SPLIT" \
        --slad_omega_post "$SLAD_OMEGA_POST" \
        --sample_steps "$SAMPLE_STEPS" \
        --acc "$ACC" \
        --t5_path "$T5_PATH" \
        --trace_detail "$TRACE_DETAIL" \
        --validate_cfg_equivalence \
        --overwrite \
        "$@" 2>&1 | tee "$out_dir/stdout_stderr.log"

    log "=== GPU$GPU $cond_name DONE ==="
}

main() {
    [[ -f "$SCRIPT" ]] || { log "ERROR: missing $SCRIPT"; return 1; }
    [[ -f "$PROMPT_PAIR_FILE" ]] || { log "ERROR: missing $PROMPT_PAIR_FILE"; return 1; }

    log "=== GPU$GPU Simplified SLAD Multi-Seed: $DIM_LABEL, 3 seeds × 8 pairs ==="
    log "prompt_set=$PROMPT_PAIR_FILE"
    log "root=$SLAD_ROOT"
    log "seeds=$SEEDS"
    log "slad_split=$SLAD_SPLIT (step ~$(awk "BEGIN {printf \"%d\", $SLAD_SPLIT * 50}")/50)"
    log "slad_omega_post=$SLAD_OMEGA_POST"
    log ""

    # Condition 1: CFG baseline (uniform ω=5.5)
    if [[ "$SKIP_UNTIL" -le 1 ]]; then
        run_condition "01_cfg_baseline" \
            --cfg_schedule constant \
            --guidance_mode cfg
    else
        log "=== SKIP 01_cfg_baseline (SKIP_UNTIL=$SKIP_UNTIL) ==="
    fi

    # Condition 2: Simplified SLAD (two-phase ω, no GDC/decouple/project)
    if [[ "$SKIP_UNTIL" -le 2 ]]; then
        run_condition "02_slad_simple" \
            --cfg_schedule slad_simple \
            --slad_split "$SLAD_SPLIT" \
            --slad_omega_post "$SLAD_OMEGA_POST" \
            --guidance_mode cfg
    else
        log "=== SKIP 02_slad_simple (SKIP_UNTIL=$SKIP_UNTIL) ==="
    fi

    # Condition 3: SLAD full (original) — for comparison against simplified
    if [[ "$SKIP_UNTIL" -le 3 ]]; then
        run_condition "03_slad_full" \
            --cfg_schedule constant \
            --guidance_mode slad \
            --lock_threshold 0.95 \
            --lock_patience 3 \
            --omega_sem 3.0 \
            --omega_qual 1.0
    else
        log "=== SKIP 03_slad_full (SKIP_UNTIL=$SKIP_UNTIL) ==="
    fi

    log "=== GPU$GPU Simplified SLAD Multi-Seed FINISHED ==="
    log "results: $SLAD_ROOT/{01_cfg_baseline,02_slad_simple,03_slad_full}/"
}

main "$@"
