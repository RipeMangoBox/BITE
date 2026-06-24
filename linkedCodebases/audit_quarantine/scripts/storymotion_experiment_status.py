#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNS = [
    ("stage1_vae_pure", ROOT / "runs/train/stage1/joint/v5_pulp192_20260621/gpu0_joint_vae_pulp192_pure_500ep", "stage1", 36572 * 500),
    ("stage1_vae_mixed", ROOT / "runs/train/stage1/joint/v5_pulp192_20260621/gpu0_joint_vae_pulp192_mixed_500ep", "stage1", 29779 * 500),
    ("stage1_grfsq_pure", ROOT / "runs/train/stage1/joint/v5_pulp192_20260621/gpu1_joint_grfsq_pulp192_pure_500ep", "stage1", 36572 * 500),
    ("stage1_grfsq_mixed", ROOT / "runs/train/stage1/joint/v5_pulp192_20260621/gpu1_joint_grfsq_pulp192_mixed_500ep", "stage1", 29779 * 500),
    ("stage2_hfsq_with_z_mixed", ROOT / "runs/train/stage2/v5_stage1_to_stage2_20260622/hfsq_with_z_mixed_ratio112_b512", "stage2", 82688),
    ("stage2_hfsq_no_z_mixed", ROOT / "runs/train/stage2/v5_stage1_to_stage2_20260622/hfsq_no_z_mixed_ratio112_b512", "stage2", 82688),
    ("stage2_hfsq_with_z_pure", ROOT / "runs/train/stage2/v5_stage1_to_stage2_20260622/hfsq_with_z_pure_ratio112_b512", "stage2", 82688),
    ("stage2_hfsq_no_z_pure", ROOT / "runs/train/stage2/v5_stage1_to_stage2_20260622/hfsq_no_z_pure_ratio112_b512", "stage2", 82688),
    ("stage2_vae_mixed", ROOT / "runs/train/stage2/v5_stage1_to_stage2_20260622/vae_mixed_ratio112_b512", "stage2", 82688),
]


def read_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def latest_stage2_step(run_dir: Path) -> tuple[int | None, float | None]:
    records = [r for r in read_records(run_dir / "train_log.jsonl") if r.get("split") == "train"]
    if not records:
        return None, None
    last = records[-1]
    return int(last["step"]), float(last.get("loss", math.nan))


def latest_stage1_from_log(run_dir: Path) -> tuple[int | None, float | None, bool]:
    log = run_dir / "training.log"
    complete = False
    if log.exists():
        text = log.read_text(encoding="utf-8", errors="ignore")
        complete = "[end]" in text
    if complete:
        return None, None, True
    last_ckpt = sorted((run_dir / "checkpoints").glob("*_last.pt"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not last_ckpt:
        return None, None, False
    return None, last_ckpt[0].stat().st_mtime, False


def mtime(path: Path) -> float | None:
    return path.stat().st_mtime if path.exists() else None


def fmt_eta(seconds: float | None) -> str:
    if seconds is None or not math.isfinite(seconds) or seconds < 0:
        return "unknown"
    ts = time.time() + seconds
    return time.strftime("%Y-%m-%d %H:%M:%S %z", time.localtime(ts))


def tmux_sessions() -> list[str]:
    try:
        output = subprocess.check_output(["tmux", "list-sessions"], text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return []
    return [line.split(":", 1)[0] for line in output.splitlines()]


def main() -> None:
    sessions = tmux_sessions()
    now = time.time()
    print(f"root: {ROOT}")
    print(f"time: {time.strftime('%Y-%m-%d %H:%M:%S %z', time.localtime(now))}")
    print()
    print("| run | kind | status | step | target | loss_or_mtime | eta |")
    print("| --- | --- | --- | ---: | ---: | --- | --- |")
    for name, run_dir, kind, target in RUNS:
        if kind == "stage2":
            step, loss = latest_stage2_step(run_dir)
            done = (run_dir / "last.pt").exists() and step is not None and step >= target
            eta = None
            if step is not None and not done:
                log_m = mtime(run_dir / "train_log.jsonl")
                # Conservative: estimate only from current recent wall-clock if records are active.
                records = [r for r in read_records(run_dir / "train_log.jsonl") if r.get("split") == "train"]
                if len(records) >= 10:
                    recent = records[-10:]
                    delta_steps = recent[-1]["step"] - recent[0]["step"]
                    # Logs are written every fixed step but do not contain wall time; use file mtime as activity only.
                    # Avoid pretending precision we do not have.
                    eta = None if log_m and now - log_m < 900 else None
            status = "done" if done else ("running" if any(name.replace("stage2_", "") in s for s in sessions) else "present")
            value = "" if loss is None else f"{loss:.6g}"
            print(f"| {name} | {kind} | {status} | {step or ''} | {target} | {value} | {fmt_eta(eta)} |")
        else:
            _, value, complete = latest_stage1_from_log(run_dir)
            status = "done" if complete and (run_dir / "last.pt").exists() else ("running" if name.endswith("mixed") and "grfsq" in name else "present")
            value_text = "" if value is None else time.strftime("%Y-%m-%d %H:%M:%S %z", time.localtime(value))
            print(f"| {name} | {kind} | {status} |  | {target} | {value_text} | unknown |")


if __name__ == "__main__":
    main()
