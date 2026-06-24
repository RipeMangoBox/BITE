#!/usr/bin/env bash
set -euo pipefail

MOTION_ROOT=${MOTION_ROOT:-/data/public/ripemangobox/Motion}
EXP_ROOT="$MOTION_ROOT/experiments/MoDebug"
REPO="$MOTION_ROOT/MoLingo"
SCRIPT="$EXP_ROOT/molingo/scripts/trace1_full_eval_attention_intervention.py"
RUN_ID=${RUN_ID:-p1_molingo_l15_pareto_gap_gpu0_20260612}
RUN_ROOT="$EXP_ROOT/molingo/mechanism_candidates/$RUN_ID"

GPU=${GPU:-0}
CONDA_ENV=${CONDA_ENV:-event-t2m}
CONDA_BIN=${CONDA_BIN:-/home/ripemangobox/miniconda3/bin/conda}
DATA_SRC=${DATA_SRC:-/data/public/ripemangobox/Motion/datasets/272-dim-HumanML3D}
T5_PATH=${T5_PATH:-/data/public/ripemangobox/Motion/Text-encoder/t5-large}
DIM_POSE=${DIM_POSE:-272}
CFG_BASE=${CFG_BASE:-5.5}
CFG_SCALE=${CFG_SCALE:-5.5}
SAMPLE_STEPS=${SAMPLE_STEPS:-32}
ACC=${ACC:-3}
REPEAT=${REPEAT:-1}
LAYER=${LAYER:-15}
SEED=${SEED:-3407}
SERVICE=${SERVICE:-4090}

mkdir -p "$RUN_ROOT"

log() {
    printf '[%(%F %T)T] %s\n' -1 "$*"
}

is_completed() {
    local manifest=$1
    [[ -f "$manifest" ]] || return 1
    python3 - "$manifest" <<'PY'
import json
import sys
try:
    data = json.load(open(sys.argv[1]))
except Exception:
    raise SystemExit(1)
raise SystemExit(0 if data.get("paper_level_status") == "full_evaluator_metrics_computed" else 1)
PY
}

run_one() {
    local name=$1
    local mixer=$2
    local alpha=$3
    local out_dir="$RUN_ROOT/$name"
    local manifest="$out_dir/manifest.json"

    if is_completed "$manifest"; then
        log "skip existing completed $name -> $out_dir"
        return 0
    fi

    mkdir -p "$out_dir"
    local -a cmd=(
        "$CONDA_BIN" run -n "$CONDA_ENV" --no-capture-output python "$SCRIPT"
        --repo_dir "$REPO"
        --out_dir "$out_dir"
        --family cfg_ca
        --layer "$LAYER"
        --gpu_id "$GPU"
        --dim_pose "$DIM_POSE"
        --cfg "$CFG_BASE"
        --cfg_scale "$CFG_SCALE"
        --cfg_schedule constant
        --cfg_residual_mixer "$mixer"
        --cfg_residual_alpha "$alpha"
        --cfg_residual_discrepancy_threshold 0.0
        --cfg_residual_discrepancy_slope 8.0
        --sample_steps "$SAMPLE_STEPS"
        --acc "$ACC"
        --repeat "$REPEAT"
        --seed "$SEED"
        --data_src "$DATA_SRC"
        --t5_path "$T5_PATH"
    )

    log "RUN $name: service=$SERVICE path=$out_dir layer=$LAYER mixer=$mixer alpha=$alpha seed=$SEED"
    cd "$REPO"
    set +e
    MODEBUG_DS_APPROVED_EXECUTE=1 \
        CUDA_VISIBLE_DEVICES="$GPU" \
        TRANSFORMERS_OFFLINE=1 \
        HF_HUB_OFFLINE=1 \
        MOLINGO_T5_PATH="$T5_PATH" \
        MODEBUG_SERVICE="$SERVICE" \
        MODEBUG_DEPLOYED_FROM="ResearchFlow_Process/linkedCodebases/MoDebug/modebug/molingo" \
        MODEBUG_COMMAND_SCRIPT="${BASH_SOURCE[0]}" \
        "${cmd[@]}" 2>&1 | tee "$out_dir/eval_stdout_stderr.log"
    local ret=${PIPESTATUS[0]}
    set -e

    if [[ $ret -ne 0 ]]; then
        log "FAILED ($ret): $name -> $out_dir"
    else
        log "OK: $name -> $out_dir"
    fi
    return 0
}

summarize() {
    python3 - "$RUN_ROOT" "$SERVICE" "${BASH_SOURCE[0]}" <<'PY'
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
service = sys.argv[2]
command_script = sys.argv[3]
rows = []
for manifest in sorted(root.glob("*/manifest.json")):
    data = json.load(open(manifest))
    metrics = data.get("metrics", {})
    intervention = data.get("intervention", {})
    rows.append({
        "name": manifest.parent.name,
        "status": data.get("paper_level_status"),
        "service": service,
        "remote_path": str(manifest.parent),
        "command_script": command_script,
        "layer": intervention.get("layer_idx"),
        "mechanism": intervention.get("mechanism"),
        "residual_alpha": intervention.get("residual_alpha"),
        "threshold": intervention.get("discrepancy_threshold"),
        "slope": intervention.get("discrepancy_slope"),
        "seed": data.get("eval_settings", {}).get("seed"),
        "fid_tmr": metrics.get("fid_tmr"),
        "top1": metrics.get("top1"),
        "top2": metrics.get("top2"),
        "top3": metrics.get("top3"),
        "matching_score": metrics.get("matching_score"),
        "failures": data.get("failures", []),
    })
summary = root / "queue_summary.jsonl"
with open(summary, "w", encoding="utf-8") as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
print(f"[summary] {summary}")
for row in rows:
    print(json.dumps(row, ensure_ascii=False))
PY
}

main() {
    if [[ "$GPU" != "0" ]]; then
        log "ERROR: L15 Pareto gap queue requires GPU=0, got GPU=$GPU"
        return 1
    fi

    log "=== MoLingo L15 Pareto gap GPU0 ==="
    log "RUN_ROOT=$RUN_ROOT"
    log "official_eval layer=$LAYER cfg=$CFG_SCALE sample_steps=$SAMPLE_STEPS acc=$ACC repeat=$REPEAT seed=$SEED"

    run_one discrepancy_gate_a070 discrepancy_gate 0.7
    run_one discrepancy_gate_a080 discrepancy_gate 0.8
    run_one discrepancy_gate_a090 discrepancy_gate 0.9
    run_one residual_gate_a070 residual_gate 0.7
    run_one residual_gate_a090 residual_gate 0.9
    run_one residual_gate_a100 residual_gate 1.0

    summarize
    date -Is > "$RUN_ROOT/gpu0_done.marker"
    log "=== GPU0 L15 Pareto gap complete ==="
}

main "$@"
