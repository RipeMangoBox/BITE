#!/usr/bin/env bash
set -euo pipefail
cd "/data/public/ripemangobox/Motion/MoLingo"
RUN_ID="modebug_molingo272_eval_diagnostic_20260602-170502_86e21b2_cfg4_g1"
RUN_DIR="/data/public/ripemangobox/Motion/MoLingo/artifacts/modebug_real_runs/modebug_molingo272_eval_diagnostic_20260602-170502_86e21b2_cfg4_g1"
CFG="4.0"
STEP="32"
ACC="5"
REPEAT="1"
GPU="1"
ROLE="diagnostic"
DATA_SRC="/data/public/ripemangobox/Motion/datasets/272-dim-HumanML3D"
DATA_ROOT="$RUN_DIR/data_root"
OFFICIAL_OUT="mogen/checkpoints/ms/pretrained_model_272/eval_cfg_4.0_step_32_acc_5/eval_res.txt"
export CUDA_VISIBLE_DEVICES="$GPU"
export TRANSFORMERS_OFFLINE=1
export HF_HUB_OFFLINE=1
export MOLINGO_T5_PATH="/data/public/ripemangobox/Motion/Text-encoder/t5-large"
mkdir -p "$DATA_ROOT"
ln -sfn "$DATA_SRC" "$DATA_ROOT/HumanML3D_272"
echo "run_id=$RUN_ID" > "$RUN_DIR/runtime_status.txt"
echo "start_time=$(date --iso-8601=seconds)" >> "$RUN_DIR/runtime_status.txt"
echo "pid=$$" >> "$RUN_DIR/runtime_status.txt"
nvidia-smi > "$RUN_DIR/nvidia_smi_start_end.txt"
if [ -e "$OFFICIAL_OUT" ]; then
  echo "ERROR: official output already exists: $OFFICIAL_OUT" | tee -a "$RUN_DIR/stdout_stderr.log"
  exit 20
fi
set +e
/home/ripemangobox/miniconda3/bin/conda run --no-capture-output -n "event-t2m" python mogen/eval_mogen.py -d 272 -dr "$DATA_ROOT" -s "$STEP" -c "$CFG" -a "$ACC" -r "$REPEAT" 2>&1 | tee "$RUN_DIR/stdout_stderr.log"
STATUS=${PIPESTATUS[0]}
set -e
{
  echo "end_time=$(date --iso-8601=seconds)"
  echo "exit_code=$STATUS"
} >> "$RUN_DIR/runtime_status.txt"
{
  echo
  echo "===== END ====="
  date --iso-8601=seconds
  nvidia-smi
} >> "$RUN_DIR/nvidia_smi_start_end.txt"
if [ -f "$OFFICIAL_OUT" ]; then
  cp "$OFFICIAL_OUT" "$RUN_DIR/metrics_eval_res.txt"
else
  echo "missing_official_output=$OFFICIAL_OUT" >> "$RUN_DIR/runtime_status.txt"
fi
exit "$STATUS"
