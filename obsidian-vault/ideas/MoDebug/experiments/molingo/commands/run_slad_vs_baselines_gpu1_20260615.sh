#!/usr/bin/env bash
set -euo pipefail
# GPU1: SLAD vs Baselines on Attribute/Direction Prompt Set
# 4 guidance modes × 1 seed each = quick comparison to identify winning conditions
# After this: scale to multi-seed on the best conditions

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT="$MOTION_ROOT/experiments/MoDebug"
REPO="$MOTION_ROOT/MoLingo"
SCRIPT="$EXP_ROOT/molingo/scripts/modebug_slad.py"
ANALYZE_SCRIPT="$EXP_ROOT/molingo/scripts/analyze_slad_core_results.py"
PROMPT_PAIR_FILE=${PROMPT_PAIR_FILE:-"$EXP_ROOT/molingo/prompt_sets/slad_m0_gpu1_attribute_direction_20260613.tsv"}

GPU=${GPU:-1}
CONDA_ENV=${CONDA_ENV:-event-t2m}
CONDA_BIN=${CONDA_BIN:-/home/ripemangobox/miniconda3/bin/conda}
T5_PATH=${T5_PATH:-/data/public/ripemangobox/Motion/Text-encoder/t5-large}

# Shared settings
SEEDS=${SEEDS:-3407}
DIRECTIONS=${DIRECTIONS:-a_to_b,b_to_a}
SWAP_ITERATIONS=${SWAP_ITERATIONS:-all}
CFG=${CFG:-5.5}
SAMPLE_STEPS=${SAMPLE_STEPS:-32}
ACC=${ACC:-3}
TRACE_DETAIL=${TRACE_DETAIL:-aggregate}
RUN_STAMP=${RUN_STAMP:-20260615_slad_vs_baselines_gpu1}

# SLAD settings (calibrated on attribute dimension)
LOCK_THRESHOLD=${LOCK_THRESHOLD:-0.95}
LOCK_PATIENCE=${LOCK_PATIENCE:-3}
OMEGA_SEM=${OMEGA_SEM:-3.0}
OMEGA_QUAL=${OMEGA_QUAL:-1.0}

# C2FG settings
C2FG_LAMBDA=${C2FG_LAMBDA:-2.0}

# ANT settings
ANT_SPLIT=${ANT_SPLIT:-0.6}
ANT_OMEGA_HIGH=${ANT_OMEGA_HIGH:-7.5}
ANT_OMEGA_LOW=${ANT_OMEGA_LOW:-1.5}

SLAD_VS_ROOT="$EXP_ROOT/molingo/slad/slad_vs_baselines_attribute_${RUN_STAMP}"

log() {
    printf '[%(%F %T)T] %s\n' -1 "$*"
}

run_condition() {
    local cond_name="$1"; shift
    local out_dir="$SLAD_VS_ROOT/$cond_name"

    mkdir -p "$out_dir"
    log "=== GPU1 $cond_name ==="
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
        --trace_detail "$TRACE_DETAIL" \
        --validate_cfg_equivalence \
        --save_arrays \
        --overwrite \
        "$@" 2>&1 | tee "$out_dir/stdout_stderr.log"

    log "=== GPU1 $cond_name DONE ==="
}

main() {
    [[ "$GPU" != "1" ]] && { log "ERROR: requires GPU=1, got GPU=$GPU"; return 1; }
    [[ -f "$SCRIPT" ]] || { log "ERROR: missing $SCRIPT"; return 1; }
    [[ -f "$PROMPT_PAIR_FILE" ]] || { log "ERROR: missing $PROMPT_PAIR_FILE"; return 1; }

    log "=== GPU1 SLAD vs Baselines Queue: 4 conditions × 1 seed ==="
    log "prompt_set=$PROMPT_PAIR_FILE"
    log "root=$SLAD_VS_ROOT"

    # Condition 1: CFG baseline (constant ω=5.5)
    run_condition "cfg_baseline" \
        --guidance_mode cfg \
        --cfg_schedule constant

    # Condition 2: SLAD (adaptive, calibrated)
    run_condition "slad" \
        --guidance_mode slad \
        --cfg_schedule constant \
        --lock_threshold "$LOCK_THRESHOLD" \
        --lock_patience "$LOCK_PATIENCE" \
        --omega_sem "$OMEGA_SEM" \
        --omega_qual "$OMEGA_QUAL"

    # Condition 3: C2FG exponential schedule
    run_condition "c2fg_exponential" \
        --guidance_mode cfg \
        --cfg_schedule exponential \
        --c2fg_lambda "$C2FG_LAMBDA"

    # Condition 4: ANT-style two-phase DCFG
    run_condition "ant_two_phase" \
        --guidance_mode cfg \
        --cfg_schedule two_phase \
        --ant_split "$ANT_SPLIT" \
        --ant_omega_high "$ANT_OMEGA_HIGH" \
        --ant_omega_low "$ANT_OMEGA_LOW"

    log "=== GPU1 SLAD vs Baselines Queue FINISHED ==="
    log "results: $SLAD_VS_ROOT/{cfg_baseline,slad,c2fg_exponential,ant_two_phase}/"
}

main "$@"
