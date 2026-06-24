#!/usr/bin/env bash
set -euo pipefail
#
# MoLingo Trace 1 Full Eval — GPU0: baseline + CA sweep + CFG_CA sweep
# 16 decoder layers (0-15), official eval pipeline, MODEBUG_DS_APPROVED_EXECUTE=1
#

MOTION_ROOT=/data/public/ripemangobox/Motion
EXP_ROOT="$MOTION_ROOT/experiments/MoDebug"
REPO="$MOTION_ROOT/MoLingo"
SCRIPT="$EXP_ROOT/molingo/scripts/trace1_full_eval_attention_intervention.py"
RUN_ID=${RUN_ID:-trace1_full_eval_ca_cfg_ca_official_20260609_gpu0}
RUN_ROOT="$EXP_ROOT/molingo/formal_candidates/$RUN_ID"

# Intervention params
ALPHA=${ALPHA:-0.5}
CFG_SCALE=${CFG_SCALE:-5.5}
CFG_BASE=${CFG_BASE:-5.5}
DIM_POSE=${DIM_POSE:-272}
SAMPLE_STEPS=${SAMPLE_STEPS:-32}
ACC=${ACC:-3}
REPEAT=${REPEAT:-1}
GPU=${GPU:-0}
CONDA_ENV=${CONDA_ENV:-event-t2m}
CONDA_BIN=${CONDA_BIN:-/home/ripemangobox/miniconda3/bin/conda}
DATA_SRC=${DATA_SRC:-/data/public/ripemangobox/Motion/datasets/272-dim-HumanML3D}
T5_PATH=${T5_PATH:-/data/public/ripemangobox/Motion/Text-encoder/t5-large}
LAYERS=${LAYERS:-5,10,15}

mkdir -p "$RUN_ROOT"

log() {
    printf '[%(%F %T)T] %s\n' -1 "$*"
}

run_one() {
    local family=$1
    local layer=$2
    local out_dir

    if [[ "$family" == "baseline" ]]; then
        out_dir="$RUN_ROOT/baseline"
    else
        out_dir="$RUN_ROOT/$family/layer_${layer}"
    fi

    if [[ -f "$out_dir/manifest.json" ]]; then
        # Check if already completed
        if python3 -c "
import json
try:
    d = json.load(open('$out_dir/manifest.json'))
    if d.get('paper_level_status') == 'full_evaluator_metrics_computed':
        exit(0)
except:
    pass
exit(1)
" 2>/dev/null; then
            log "skip existing completed $out_dir"
            return 0
        fi
    fi

    mkdir -p "$out_dir"

    local -a cmd=(
        "$CONDA_BIN" run -n "$CONDA_ENV" --no-capture-output python "$SCRIPT"
        --repo_dir "$REPO"
        --out_dir "$out_dir"
        --family "$family"
        --gpu_id "$GPU"
        --dim_pose "$DIM_POSE"
        --cfg "$CFG_BASE"
        --sample_steps "$SAMPLE_STEPS"
        --acc "$ACC"
        --repeat "$REPEAT"
        --data_src "$DATA_SRC"
        --t5_path "$T5_PATH"
    )

    if [[ "$family" != "baseline" ]]; then
        cmd+=(--layer "$layer")
        if [[ "$family" == "ca" ]]; then
            cmd+=(--alpha "$ALPHA")
        elif [[ "$family" == "cfg_ca" ]]; then
            cmd+=(--cfg_scale "$CFG_SCALE")
        fi
    fi

    log "RUN: ${cmd[*]}"
    cd "$REPO"
    MODEBUG_DS_APPROVED_EXECUTE=1 \
        CUDA_VISIBLE_DEVICES="$GPU" \
        TRANSFORMERS_OFFLINE=1 \
        HF_HUB_OFFLINE=1 \
        MOLINGO_T5_PATH="$T5_PATH" \
        MODEBUG_COMMAND_SCRIPT="${BASH_SOURCE[0]}" \
        "${cmd[@]}" 2>&1 | tee "$out_dir/eval_stdout_stderr.log"

    local ret=$?
    if [[ $ret -ne 0 ]]; then
        log "FAILED ($ret): $family layer=$layer -> $out_dir"
    else
        log "OK: $family layer=$layer -> $out_dir"
    fi
}

main() {
    if [[ "$GPU" != "0" ]]; then
        log "ERROR: this command is GPU0-only; got GPU=$GPU"
        return 1
    fi

    log "=== MoLingo Trace 1 GPU0: baseline + CA sweep + CFG_CA sweep ==="
    log "RUN_ROOT=$RUN_ROOT"
    log "ALPHA=$ALPHA  CFG_SCALE=$CFG_SCALE  CFG_BASE=$CFG_BASE"
    log "DIM_POSE=$DIM_POSE  SAMPLE_STEPS=$SAMPLE_STEPS  ACC=$ACC  REPEAT=$REPEAT"
    log "LAYERS=$LAYERS"

    # 1. Baseline
    run_one baseline 0

    # 2. CA representative layers
    IFS=',' read -r -a layer_list <<< "$LAYERS"
    for layer in "${layer_list[@]}"; do
        run_one ca "$layer"
    done

    # 3. CFG_CA representative layers
    for layer in "${layer_list[@]}"; do
        run_one cfg_ca "$layer"
    done

    date -Is > "$RUN_ROOT/gpu0_done.marker"
    log "=== GPU0 sweep complete ==="
}

main "$@"
