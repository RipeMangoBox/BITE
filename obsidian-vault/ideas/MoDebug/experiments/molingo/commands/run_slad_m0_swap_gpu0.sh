#!/usr/bin/env bash
set -euo pipefail

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT="$MOTION_ROOT/experiments/MoDebug"
REPO="$MOTION_ROOT/MoLingo"
SCRIPT="$EXP_ROOT/molingo/scripts/modebug_slad.py"
RUN_ID=${RUN_ID:-slad_m0_swap_walk_run_seed3407_20260613_gpu0}
RUN_ROOT="$EXP_ROOT/molingo/slad/$RUN_ID"

GPU=${GPU:-0}
CONDA_ENV=${CONDA_ENV:-event-t2m}
CONDA_BIN=${CONDA_BIN:-/home/ripemangobox/miniconda3/bin/conda}
T5_PATH=${T5_PATH:-/data/public/ripemangobox/Motion/Text-encoder/t5-large}
PROMPT_A=${PROMPT_A:-"a person walks forward"}
PROMPT_B=${PROMPT_B:-"a person runs forward"}
MOTION_SECONDS=${MOTION_SECONDS:-6.0}
SEEDS=${SEEDS:-3407}
DIRECTIONS=${DIRECTIONS:-a_to_b}
SWAP_ITERATIONS=${SWAP_ITERATIONS:-all}
CFG=${CFG:-5.5}
SAMPLE_STEPS=${SAMPLE_STEPS:-32}
ACC=${ACC:-3}
TRACE_DETAIL=${TRACE_DETAIL:-aggregate}

mkdir -p "$RUN_ROOT"

log() {
    printf '[%(%F %T)T] %s\n' -1 "$*"
}

main() {
    if [[ "$GPU" != "0" ]]; then
        log "ERROR: M0 GPU0 command requires GPU=0, got GPU=$GPU"
        return 1
    fi
    if [[ ! -f "$SCRIPT" ]]; then
        log "ERROR: missing deployed script: $SCRIPT"
        return 1
    fi

    log "=== MoDebug SLAD M0 token-swap run ==="
    log "RUN_ROOT=$RUN_ROOT"
    log "prompt A=$PROMPT_A"
    log "prompt B=$PROMPT_B"
    log "seconds=$MOTION_SECONDS"
    log "seeds=$SEEDS directions=$DIRECTIONS swap_iterations=$SWAP_ITERATIONS"
    log "cfg=$CFG sample_steps=$SAMPLE_STEPS acc=$ACC trace_detail=$TRACE_DETAIL"

    cd "$REPO"
    MODEBUG_DS_APPROVED_EXECUTE=1 \
    CUDA_VISIBLE_DEVICES="$GPU" \
    TRANSFORMERS_OFFLINE=1 \
    HF_HUB_OFFLINE=1 \
    MOLINGO_T5_PATH="$T5_PATH" \
    MODEBUG_DEPLOYED_FROM="BITE_Process/obsidian-vault/ideas/MoDebug/experiments/molingo" \
    MODEBUG_COMMAND_SCRIPT="${BASH_SOURCE[0]}" \
    "$CONDA_BIN" run -n "$CONDA_ENV" --no-capture-output python "$SCRIPT" \
        --repo_dir "$REPO" \
        --out_dir "$RUN_ROOT" \
        --prompt_a "$PROMPT_A" \
        --prompt_b "$PROMPT_B" \
        --seconds "$MOTION_SECONDS" \
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
        --validate_cfg_equivalence \
        --save_arrays \
        --overwrite 2>&1 | tee "$RUN_ROOT/stdout_stderr.log"

    log "=== M0 run finished ==="
}

main "$@"
