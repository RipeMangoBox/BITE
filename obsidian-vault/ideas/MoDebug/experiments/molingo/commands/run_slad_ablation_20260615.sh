#!/usr/bin/env bash
set -euo pipefail
# SLAD Ablation: 5 conditions × 2 seeds on a parameterized prompt set
# Usage: GPU=0 PROMPT_SET=action bash run_slad_ablation_20260615.sh
#        GPU=1 PROMPT_SET=attribute bash run_slad_ablation_20260615.sh

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT="$MOTION_ROOT/experiments/MoDebug"
REPO="$MOTION_ROOT/MoLingo"
SCRIPT="$EXP_ROOT/molingo/scripts/modebug_slad.py"

GPU=${GPU:-0}
CONDA_ENV=${CONDA_ENV:-event-t2m}
CONDA_BIN=${CONDA_BIN:-/home/ripemangobox/miniconda3/bin/conda}
T5_PATH=${T5_PATH:-/data/public/ripemangobox/Motion/Text-encoder/t5-large}

# Shared settings
SEEDS=${SEEDS:-3407,2026}
DIRECTIONS=${DIRECTIONS:-a_to_b,b_to_a}
SWAP_ITERATIONS=${SWAP_ITERATIONS:-all}
CFG=${CFG:-5.5}
SAMPLE_STEPS=${SAMPLE_STEPS:-32}
ACC=${ACC:-3}
TRACE_DETAIL=${TRACE_DETAIL:-aggregate}

# SLAD settings
LOCK_THRESHOLD=${LOCK_THRESHOLD:-0.95}
LOCK_PATIENCE=${LOCK_PATIENCE:-3}
OMEGA_SEM=${OMEGA_SEM:-3.0}
OMEGA_QUAL=${OMEGA_QUAL:-1.0}

# Ablation settings
ABLATION_FIXED_STEP=${ABLATION_FIXED_STEP:-25}
ABLATION_OMEGA_POST=${ABLATION_OMEGA_POST:-1.5}

PROMPT_SET=${PROMPT_SET:-action}
SKIP_UNTIL=${SKIP_UNTIL:-0}
RUN_STAMP=${RUN_STAMP:-20260615_ablation_${PROMPT_SET}_gpu${GPU}}

if [[ "$PROMPT_SET" == "action" ]]; then
    PROMPT_PAIR_FILE="$EXP_ROOT/molingo/prompt_sets/slad_m0_gpu0_action_control_20260613.tsv"
    DIM_LABEL="action_control"
else
    PROMPT_PAIR_FILE="$EXP_ROOT/molingo/prompt_sets/slad_m0_gpu1_attribute_direction_20260613.tsv"
    DIM_LABEL="attribute_direction"
fi

ABLATION_ROOT="$EXP_ROOT/molingo/slad/slad_ablation_${DIM_LABEL}_${RUN_STAMP}"

log() {
    printf '[%(%F %T)T] %s\n' -1 "$*"
}

run_condition() {
    local cond_name="$1"; shift
    local out_dir="$ABLATION_ROOT/$cond_name"

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
        --cfg_schedule constant \
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

    log "=== GPU$GPU SLAD Ablation Queue: $DIM_LABEL, 5 conditions × 2 seeds ==="
    log "prompt_set=$PROMPT_PAIR_FILE"
    log "root=$ABLATION_ROOT"
    log "seeds=$SEEDS"

    # Condition 1: CFG baseline (uniform ω=5.5)
    if [[ "$SKIP_UNTIL" -le 1 ]]; then
        run_condition "01_cfg_baseline" \
            --guidance_mode cfg
    else
        log "=== SKIP 01_cfg_baseline (SKIP_UNTIL=$SKIP_UNTIL) ==="
    fi

    # Condition 2: SLAD full (adaptive detection + decoupling + projection)
    if [[ "$SKIP_UNTIL" -le 2 ]]; then
        run_condition "02_slad_full" \
            --guidance_mode slad \
            --lock_threshold "$LOCK_THRESHOLD" \
            --lock_patience "$LOCK_PATIENCE" \
            --omega_sem "$OMEGA_SEM" \
            --omega_qual "$OMEGA_QUAL"
    else
        log "=== SKIP 02_slad_full (SKIP_UNTIL=$SKIP_UNTIL) ==="
    fi

    # Condition 3: SLAD − adaptive detection (fixed step=25)
    if [[ "$SKIP_UNTIL" -le 3 ]]; then
        run_condition "03_no_adaptive" \
            --guidance_mode slad \
            --ablation fixed_step \
            --ablation_fixed_step "$ABLATION_FIXED_STEP" \
            --omega_sem "$OMEGA_SEM" \
            --omega_qual "$OMEGA_QUAL"
    else
        log "=== SKIP 03_no_adaptive (SKIP_UNTIL=$SKIP_UNTIL) ==="
    fi

    # Condition 4: SLAD − direction decoupling (post-lock simple ω scaling)
    if [[ "$SKIP_UNTIL" -le 4 ]]; then
        run_condition "04_no_decouple" \
            --guidance_mode slad \
            --ablation no_decouple \
            --ablation_omega_post "$ABLATION_OMEGA_POST" \
            --lock_threshold "$LOCK_THRESHOLD" \
            --lock_patience "$LOCK_PATIENCE"
    else
        log "=== SKIP 04_no_decouple (SKIP_UNTIL=$SKIP_UNTIL) ==="
    fi

    # Condition 5: SLAD − semantic projection (post-lock scale Δv)
    if [[ "$SKIP_UNTIL" -le 5 ]]; then
        run_condition "05_no_project" \
            --guidance_mode slad \
            --ablation no_project \
            --omega_sem "$OMEGA_SEM" \
            --lock_threshold "$LOCK_THRESHOLD" \
            --lock_patience "$LOCK_PATIENCE"
    else
        log "=== SKIP 05_no_project (SKIP_UNTIL=$SKIP_UNTIL) ==="
    fi

    log "=== GPU$GPU SLAD Ablation Queue FINISHED ==="
    log "results: $ABLATION_ROOT/{01_cfg_baseline,02_slad_full,03_no_adaptive,04_no_decouple,05_no_project}/"
}

main "$@"
