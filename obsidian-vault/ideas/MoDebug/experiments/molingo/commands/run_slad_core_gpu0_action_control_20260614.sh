#!/usr/bin/env bash
set -euo pipefail

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT="$MOTION_ROOT/experiments/MoDebug"
REPO="$MOTION_ROOT/MoLingo"
SCRIPT="$EXP_ROOT/molingo/scripts/modebug_slad.py"
ANALYZE_SCRIPT="$EXP_ROOT/molingo/scripts/analyze_slad_core_results.py"
PROMPT_PAIR_FILE=${PROMPT_PAIR_FILE:-"$EXP_ROOT/molingo/prompt_sets/slad_m0_gpu0_action_control_20260613.tsv"}

GPU=${GPU:-0}
CONDA_ENV=${CONDA_ENV:-event-t2m}
CONDA_BIN=${CONDA_BIN:-/home/ripemangobox/miniconda3/bin/conda}
T5_PATH=${T5_PATH:-/data/public/ripemangobox/Motion/Text-encoder/t5-large}
SEEDS=${SEEDS:-3407,2026,1337}
DIRECTIONS=${DIRECTIONS:-a_to_b,b_to_a}
SWAP_ITERATIONS=${SWAP_ITERATIONS:-all}
CFG=${CFG:-5.5}
SAMPLE_STEPS=${SAMPLE_STEPS:-32}
ACC=${ACC:-3}
TRACE_DETAIL=${TRACE_DETAIL:-aggregate}
GDC_THRESHOLDS=${GDC_THRESHOLDS:-0.85,0.90,0.95}
RUN_STAMP=${RUN_STAMP:-20260614_core_seed3_mvp_gpu0}

M0_RUN_ID=${M0_RUN_ID:-slad_m0_multiseed_action_control_${RUN_STAMP}}
GDC_RUN_ID=${GDC_RUN_ID:-slad_gdc_probe_action_control_${RUN_STAMP}}
M0_RUN_ROOT="$EXP_ROOT/molingo/slad/$M0_RUN_ID"
GDC_RUN_ROOT="$EXP_ROOT/molingo/slad/$GDC_RUN_ID"
ANALYSIS_ROOT="$EXP_ROOT/molingo/slad/slad_core_calibration_action_control_${RUN_STAMP}"

log() {
    printf '[%(%F %T)T] %s\n' -1 "$*"
}

run_m0() {
    mkdir -p "$M0_RUN_ROOT"
    log "=== GPU0 M0 multiseed action/control ==="
    log "RUN_ROOT=$M0_RUN_ROOT"
    log "seeds=$SEEDS directions=$DIRECTIONS swap_iterations=$SWAP_ITERATIONS"
    log "settings cfg=$CFG sample_steps=$SAMPLE_STEPS acc=$ACC"

    cd "$REPO"
    MODEBUG_DS_REVIEW_SESSION="ebc47ee1d44b" \
    CUDA_VISIBLE_DEVICES="$GPU" \
    TRANSFORMERS_OFFLINE=1 \
    HF_HUB_OFFLINE=1 \
    MOLINGO_T5_PATH="$T5_PATH" \
    MODEBUG_DEPLOYED_FROM="BITE_Process/obsidian-vault/ideas/MoDebug/experiments/molingo" \
    MODEBUG_COMMAND_SCRIPT="${BASH_SOURCE[0]}" \
    "$CONDA_BIN" run -n "$CONDA_ENV" --no-capture-output python "$SCRIPT" \
        --experiment m0_swap \
        --repo_dir "$REPO" \
        --out_dir "$M0_RUN_ROOT" \
        --prompt_pair_file "$PROMPT_PAIR_FILE" \
        --seeds "$SEEDS" \
        --directions "$DIRECTIONS" \
        --swap_iterations "$SWAP_ITERATIONS" \
        --cfg "$CFG" \
        --cfg_schedule constant \
        --sample_steps "$SAMPLE_STEPS" \
        --acc "$ACC" \
        --t5_path "$T5_PATH" \
        --guidance_mode cfg \
        --trace_detail "$TRACE_DETAIL" \
        --gdc_thresholds "$GDC_THRESHOLDS" \
        --validate_cfg_equivalence \
        --save_arrays \
        --overwrite 2>&1 | tee "$M0_RUN_ROOT/stdout_stderr.log"
}

run_gdc() {
    mkdir -p "$GDC_RUN_ROOT"
    log "=== GPU0 GDC probe action/control ==="
    log "RUN_ROOT=$GDC_RUN_ROOT"
    log "seeds=$SEEDS thresholds=$GDC_THRESHOLDS"

    cd "$REPO"
    MODEBUG_DS_REVIEW_SESSION="ebc47ee1d44b" \
    CUDA_VISIBLE_DEVICES="$GPU" \
    TRANSFORMERS_OFFLINE=1 \
    HF_HUB_OFFLINE=1 \
    MOLINGO_T5_PATH="$T5_PATH" \
    MODEBUG_DEPLOYED_FROM="BITE_Process/obsidian-vault/ideas/MoDebug/experiments/molingo" \
    MODEBUG_COMMAND_SCRIPT="${BASH_SOURCE[0]}" \
    "$CONDA_BIN" run -n "$CONDA_ENV" --no-capture-output python "$SCRIPT" \
        --experiment gdc_probe \
        --repo_dir "$REPO" \
        --out_dir "$GDC_RUN_ROOT" \
        --prompt_pair_file "$PROMPT_PAIR_FILE" \
        --seeds "$SEEDS" \
        --cfg "$CFG" \
        --cfg_schedule constant \
        --sample_steps "$SAMPLE_STEPS" \
        --acc "$ACC" \
        --t5_path "$T5_PATH" \
        --guidance_mode cfg \
        --trace_detail "$TRACE_DETAIL" \
        --gdc_thresholds "$GDC_THRESHOLDS" \
        --overwrite 2>&1 | tee "$GDC_RUN_ROOT/stdout_stderr.log"
}

run_analysis() {
    mkdir -p "$ANALYSIS_ROOT"
    log "=== GPU0 CPU calibration summary ==="
    "$CONDA_BIN" run -n "$CONDA_ENV" --no-capture-output python "$ANALYZE_SCRIPT" \
        --m0_metrics "$M0_RUN_ROOT/swap_metrics.jsonl" \
        --gdc_metrics "$GDC_RUN_ROOT/gdc_metrics.jsonl" \
        --out_dir "$ANALYSIS_ROOT" \
        --gdc_thresholds "$GDC_THRESHOLDS" 2>&1 | tee "$ANALYSIS_ROOT/stdout_stderr.log"
}

main() {
    if [[ "$GPU" != "0" ]]; then
        log "ERROR: GPU0 action/control core suite requires GPU=0, got GPU=$GPU"
        return 1
    fi
    [[ -f "$SCRIPT" ]] || { log "ERROR: missing script: $SCRIPT"; return 1; }
    [[ -f "$ANALYZE_SCRIPT" ]] || { log "ERROR: missing analyze script: $ANALYZE_SCRIPT"; return 1; }
    [[ -f "$PROMPT_PAIR_FILE" ]] || { log "ERROR: missing prompt file: $PROMPT_PAIR_FILE"; return 1; }

    log "=== MoDebug SLAD core GPU0 action/control queue ==="
    log "prompt_pair_file=$PROMPT_PAIR_FILE"
    log "m0_run=$M0_RUN_ROOT"
    log "gdc_run=$GDC_RUN_ROOT"
    log "analysis=$ANALYSIS_ROOT"
    run_m0
    run_gdc
    run_analysis
    log "=== GPU0 action/control core queue finished ==="
}

main "$@"
