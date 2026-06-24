#!/usr/bin/env bash
set -euo pipefail

EXP_ROOT=${EXP_ROOT:-/data/public/ripemangobox/Motion/experiments/MoDebug}
COMMAND_DIR=${COMMAND_DIR:-$EXP_ROOT/motionstreamer/commands}
LAYERS=${LAYERS:-3,7,11}
SA_SESSION=${SA_SESSION:-ms_resume_sa_gpu0_20260609}
CFGSA_SESSION=${CFGSA_SESSION:-ms_resume_cfgsa_gpu1_20260609}
SA_LOG=${SA_LOG:-/tmp/ms_resume_sa_gpu0_20260609.log}
CFGSA_LOG=${CFGSA_LOG:-/tmp/ms_resume_cfgsa_gpu1_20260609.log}
SA_TMUX_LOG=${SA_TMUX_LOG:-/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/ms_resume_sa_gpu0_20260609.tmux.log}
CFGSA_TMUX_LOG=${CFGSA_TMUX_LOG:-/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/ms_resume_cfgsa_gpu1_20260609.tmux.log}
WAIT_FOR_GPUS=${WAIT_FOR_GPUS:-1}
GPU_POLL_SECONDS=${GPU_POLL_SECONDS:-300}
GPU_IDLE_CONFIRMATIONS=${GPU_IDLE_CONFIRMATIONS:-6}
BLOCKING_TMUX_PATTERN=${BLOCKING_TMUX_PATTERN:-storymotion}

log() {
  printf '[%(%F %T)T] [MS-DUAL-REMAINING] %s\n' -1 "$*"
}

tmux_has_session() {
  tmux has-session -t "$1" 2>/dev/null
}

blocking_tmux_active() {
  if [[ -z "$BLOCKING_TMUX_PATTERN" ]]; then
    return 1
  fi
  tmux ls 2>/dev/null | grep -E "$BLOCKING_TMUX_PATTERN"
}

gpu_busy() {
  python3 <<'PY'
import subprocess

result = subprocess.run(
    ["nvidia-smi", "--query-compute-apps=gpu_uuid,pid,process_name,used_memory", "--format=csv,noheader,nounits"],
    check=False,
    text=True,
    stdout=subprocess.PIPE,
)
if result.returncode != 0:
    raise SystemExit(1)
busy = [line.strip() for line in result.stdout.splitlines() if line.strip()]
if busy:
    print("; ".join(busy))
    raise SystemExit(0)
raise SystemExit(1)
PY
}

gpu_memory_busy() {
  python3 <<'PY'
import subprocess

result = subprocess.run(
    ["nvidia-smi", "--query-gpu=index,memory.used", "--format=csv,noheader,nounits"],
    check=False,
    text=True,
    stdout=subprocess.PIPE,
)
if result.returncode != 0:
    raise SystemExit(1)
busy = []
for line in result.stdout.splitlines():
    if not line.strip():
        continue
    idx, mem = [part.strip() for part in line.split(",", 1)]
    if int(mem) > 512:
        busy.append(f"gpu{idx}:{mem}MiB")
if busy:
    print(" ".join(busy))
    raise SystemExit(0)
raise SystemExit(1)
PY
}

wait_for_gpus() {
  if [[ "$WAIT_FOR_GPUS" != "1" ]]; then
    log "WAIT_FOR_GPUS=0; launching without GPU idle wait"
    return 0
  fi
  while busy=$(blocking_tmux_active 2>&1); do
    log "Blocking tmux active ($BLOCKING_TMUX_PATTERN): $busy; retry in ${GPU_POLL_SECONDS}s"
    sleep "$GPU_POLL_SECONDS"
  done
  local idle_count=0
  while busy=$(gpu_busy 2>&1); do
    idle_count=0
    log "GPU compute apps active: $busy; retry in ${GPU_POLL_SECONDS}s"
    sleep "$GPU_POLL_SECONDS"
  done
  while busy=$(gpu_memory_busy 2>&1); do
    idle_count=0
    log "GPU memory still above idle threshold: $busy; retry in ${GPU_POLL_SECONDS}s"
    sleep "$GPU_POLL_SECONDS"
  done
  idle_count=1
  while [[ "$idle_count" -lt "$GPU_IDLE_CONFIRMATIONS" ]]; do
    log "GPUs idle confirmation ${idle_count}/${GPU_IDLE_CONFIRMATIONS}; recheck in ${GPU_POLL_SECONDS}s"
    sleep "$GPU_POLL_SECONDS"
    if busy=$(blocking_tmux_active 2>&1); then
      log "Blocking tmux became active ($BLOCKING_TMUX_PATTERN): $busy"
      idle_count=0
      while busy=$(blocking_tmux_active 2>&1); do
        log "Blocking tmux active ($BLOCKING_TMUX_PATTERN): $busy; retry in ${GPU_POLL_SECONDS}s"
        sleep "$GPU_POLL_SECONDS"
      done
      continue
    fi
    if busy=$(gpu_busy 2>&1); then
      log "GPU compute apps became active during confirmation: $busy"
    elif busy=$(gpu_memory_busy 2>&1); then
      log "GPU memory became busy during confirmation: $busy"
    else
      idle_count=$((idle_count + 1))
      continue
    fi
    idle_count=0
    while busy=$(gpu_busy 2>&1); do
      log "GPU compute apps active: $busy; retry in ${GPU_POLL_SECONDS}s"
      sleep "$GPU_POLL_SECONDS"
    done
    while busy=$(gpu_memory_busy 2>&1); do
      log "GPU memory still above idle threshold: $busy; retry in ${GPU_POLL_SECONDS}s"
      sleep "$GPU_POLL_SECONDS"
    done
    idle_count=1
  done
  log "GPUs idle confirmed ${GPU_IDLE_CONFIRMATIONS}/${GPU_IDLE_CONFIRMATIONS}; launching representative-layer jobs"
}

start_session() {
  local session=$1
  local tmux_log=$2
  shift 2
  if tmux_has_session "$session"; then
    log "SKIP existing tmux session: $session"
    return 0
  fi
  mkdir -p "$(dirname "$tmux_log")"
  log "START tmux session: $session"
  tmux new-session -d -s "$session" "set -o pipefail; $* 2>&1 | tee -a '$tmux_log'"
}

main() {
  if [[ "${MODEBUG_DS_APPROVED_EXECUTE:-0}" != "1" ]]; then
    log "ERROR: set MODEBUG_DS_APPROVED_EXECUTE=1 before launching formal resume."
    return 2
  fi
  local -a layer_list=()
  IFS=',' read -r -a layer_list <<< "$LAYERS"
  local layer
  for layer in "${layer_list[@]}"; do
    if [[ ! "$layer" =~ ^[0-9]+$ || "$layer" -lt 0 || "$layer" -gt 11 ]]; then
      log "ERROR: invalid representative layer in LAYERS=$LAYERS"
      return 2
    fi
  done

  if ! tmux_has_session "$SA_SESSION" || ! tmux_has_session "$CFGSA_SESSION"; then
    wait_for_gpus
  fi

  start_session "$SA_SESSION" "$SA_TMUX_LOG" \
    "MODEBUG_DS_APPROVED_EXECUTE=1 LAYERS='$LAYERS' RUN_BASELINE_AND_GUARDS=1 LOG_FILE='$SA_LOG' bash '$COMMAND_DIR/resume_encodecache_sa_gpu0.sh' --execute"

  start_session "$CFGSA_SESSION" "$CFGSA_TMUX_LOG" \
    "MODEBUG_DS_APPROVED_EXECUTE=1 LAYERS='$LAYERS' LOG_FILE='$CFGSA_LOG' bash '$COMMAND_DIR/resume_encodecache_cfgsa_gpu1.sh' --execute"

  log "Active sessions:"
  tmux ls | grep -E "$SA_SESSION|$CFGSA_SESSION" || true
  log "Logs:"
  log "  SA:     $SA_LOG"
  log "  CFG_SA: $CFGSA_LOG"
}

main "$@"
