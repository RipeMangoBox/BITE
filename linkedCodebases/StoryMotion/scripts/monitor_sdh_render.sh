#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "usage: $0 TMUX_SESSION OUTPUT_DIR LOG_FILE" >&2
  exit 2
fi

session=$1
output_dir=$2
log_file=$3
tmux_socket=${TMUX_SOCKET:-/tmp/tmux-1002/default}
errors_file=${SDH_ERRORS_FILE:-/sys/fs/ext4/sdh1/errors_count}
stop_file="$output_dir/STOP_DISK_ERROR"
pattern='sd .*\[sdh\].*(FAILED|Sense Key|error|reset|timeout)|critical medium error, dev sdh|EXT4-fs (error|warning).*sdh'

count_dmesg() {
  { dmesg | grep -Ei "$pattern" || true; } | wc -l
}

mkdir -p "$(dirname "$log_file")" "$output_dir"
rm -f "$stop_file"
base_ext4=$(<"$errors_file")
base_dmesg=$(count_dmesg)
echo "guard_started=$(date -Is) session=$session base_ext4=$base_ext4 base_dmesg=$base_dmesg" >"$log_file"

while tmux -S "$tmux_socket" has-session -t "$session" 2>/dev/null; do
  ext4=$(<"$errors_file")
  current_dmesg=$(count_dmesg)
  if (( ext4 > base_ext4 || current_dmesg > base_dmesg )); then
    echo "FATAL_DISK_ERROR=$(date -Is) ext4=$ext4 dmesg_matches=$current_dmesg" >>"$log_file"
    dmesg -T | grep -Ei "$pattern" | tail -80 >>"$log_file" || true
    touch "$stop_file"
    tmux -S "$tmux_socket" kill-session -t "$session" 2>/dev/null || true
    exit 90
  fi
  sleep 2
done

echo "guard_finished=$(date -Is) ext4=$(<"$errors_file") dmesg_matches=$(count_dmesg)" >>"$log_file"
