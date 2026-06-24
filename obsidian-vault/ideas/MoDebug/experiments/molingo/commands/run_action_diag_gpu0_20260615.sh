#!/usr/bin/env bash
set -euo pipefail
# GPU0: Action Dimension Diagnostic
# Goal: understand why GDC stability_score maps weakly (Pearson 0.61) to action swap k50
# Strategy: inner-trace CFG + SLAD test on action prompt set

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT="$MOTION_ROOT/experiments/MoDebug"
REPO="$MOTION_ROOT/MoLingo"
SCRIPT="$EXP_ROOT/molingo/scripts/modebug_slad.py"
PROMPT_PAIR_FILE=${PROMPT_PAIR_FILE:-"$EXP_ROOT/molingo/prompt_sets/slad_m0_gpu0_action_control_20260613.tsv"}

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
RUN_STAMP=${RUN_STAMP:-20260615_action_diag_gpu0}

# SLAD settings
LOCK_THRESHOLD=${LOCK_THRESHOLD:-0.95}
LOCK_PATIENCE=${LOCK_PATIENCE:-3}
OMEGA_SEM=${OMEGA_SEM:-3.0}
OMEGA_QUAL=${OMEGA_QUAL:-1.0}

DIAG_ROOT="$EXP_ROOT/molingo/slad/slad_action_diagnostic_${RUN_STAMP}"

log() {
    printf '[%(%F %T)T] %s\n' -1 "$*"
}

run_condition() {
    local cond_name="$1"; shift
    local out_dir="$DIAG_ROOT/$cond_name"

    mkdir -p "$out_dir"
    log "=== GPU0 $cond_name ==="
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
        --sample_steps "$SAMPLE_STEPS" \
        --acc "$ACC" \
        --t5_path "$T5_PATH" \
        --validate_cfg_equivalence \
        --save_arrays \
        --overwrite \
        "$@" 2>&1 | tee "$out_dir/stdout_stderr.log"

    log "=== GPU0 $cond_name DONE ==="
}

main() {
    [[ "$GPU" != "0" ]] && { log "ERROR: requires GPU=0, got GPU=$GPU"; return 1; }
    [[ -f "$SCRIPT" ]] || { log "ERROR: missing $SCRIPT"; return 1; }
    [[ -f "$PROMPT_PAIR_FILE" ]] || { log "ERROR: missing $PROMPT_PAIR_FILE"; return 1; }

    log "=== GPU0 Action Diagnostic Queue ==="
    log "prompt_set=$PROMPT_PAIR_FILE"
    log "root=$DIAG_ROOT"

    # Task 1: CFG inner-trace — full per-step GDC/stability data for action pairs
    # This gives us the raw signal to diagnose why Pearson is only 0.61
    run_condition "cfg_inner_trace" \
        --guidance_mode cfg \
        --cfg_schedule constant \
        --trace_detail inner

    # Task 2: SLAD on action pairs — test SLAD despite weak calibration
    # Even if detector triggers suboptimally, the decoupled guidance might still help
    run_condition "slad_test" \
        --guidance_mode slad \
        --cfg_schedule constant \
        --lock_threshold "$LOCK_THRESHOLD" \
        --lock_patience "$LOCK_PATIENCE" \
        --omega_sem "$OMEGA_SEM" \
        --omega_qual "$OMEGA_QUAL" \
        --trace_detail aggregate

    log "=== GPU0 Action Diagnostic Queue FINISHED ==="
    log "results: $DIAG_ROOT/{cfg_inner_trace,slad_test}/"
}

main "$@"
