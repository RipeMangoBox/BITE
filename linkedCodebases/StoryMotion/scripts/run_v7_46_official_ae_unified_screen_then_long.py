#!/usr/bin/env python3
"""Run the frozen official-Pulp-AE matched Unified screen and gated long continuation."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import torch


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.storymotion_run_layout import init_run, run_paths, update_manifest

TRAIN_SCRIPT = ROOT / "scripts/train_stage2_condmdi_pulp.py"
EVAL_SCRIPT = ROOT / "scripts/storymotion_official_full_eval.py"
MODEL_DIR = Path("/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models")
CACHE_DIR = ROOT / "runs/legacy/train/stage2/v7_17_corrected_cache_20260712/official_ae_paired"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def event(name: str, **fields: Any) -> None:
    print(json.dumps({"event": name, "time": time.strftime("%Y-%m-%dT%H:%M:%S%z"), **fields}, sort_keys=True), flush=True)


def run_logged(command: list[str], log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"command": command}, sort_keys=True) + "\n")
        handle.flush()
        subprocess.run(command, cwd=ROOT, stdout=handle, stderr=subprocess.STDOUT, check=True)


def checkpoint_step(path: Path) -> int:
    if not path.is_file():
        return 0
    return int(torch.load(path, map_location="cpu").get("step", 0))


def train_command(args: argparse.Namespace, target_steps: int, lr: float, resume: Path | None) -> list[str]:
    stats = run_paths("stage2", args.run_id)["cache"] / "train_latent_fullcov.pt"
    command = [
        sys.executable,
        str(TRAIN_SCRIPT),
        "train",
        "--run-id", args.run_id,
        "--device", args.device,
        "--seed", "17",
        "--steps", str(target_steps),
        "--batch-size", "512",
        "--num-workers", "0",
        "--width", "416",
        "--dim-mults", "1", "2", "2",
        "--cond-mask-prob", "0.1",
        "--cond-mask-prob-cam", "0.0",
        "--cond-mask-prob-hum", "0.0",
        "--generative-process", "diffusion",
        "--diffusion-steps", "1000",
        "--diffusion-prediction-type", "START_X",
        "--noise-schedule", "cosine",
        "--lr", str(lr),
        "--weight-decay", "0.01",
        "--adam-beta2", "0.999",
        "--grad-clip", "1.0",
        "--log-every", "100",
        "--eval-every", "1000" if target_steps <= 30000 else "1000000000",
        "--eval-batches", "4" if target_steps <= 30000 else "1",
        "--eval-samples", "256",
        "--test-every", "3000" if target_steps <= 30000 else "1000000000",
        "--test-batches", "4" if target_steps <= 30000 else "1",
        "--test-samples", "256",
        "--task-probs", "1", "1", "1", "0",
        "--joint-loss-mode", "element_mean",
        "--joint-human-branch-weight", "1.0",
        "--joint-camera-branch-weight", "1.0",
        "--joint-loss-weight", "1.0",
        "--task-routing", "human_first",
        "--joint-human-camera-input-mode", "normal",
        "--joint-coupling-scale", "0.0",
        "--joint-coupling-mode", "c_to_h_blocked",
        "--selection-metric", "loss",
        "--snapshot-steps", "1000", "3000", "10000", "30000", "105000",
        "--obs-self-condition-prob", "0.0",
        "--obs-self-condition-mode", "clean",
        "--obs-self-condition-noise-std", "0.0",
        "--v72-text-role-router",
        "--v72-aux-text-scale", "0.0",
        "--znorm",
        "--full-cov",
        "--znorm-stats-path", str(stats),
        "--cov-ridge", "0.0001",
        "--cache-dir", str(CACHE_DIR),
        "--official-pulp-ae-control",
    ]
    if resume is not None:
        command.extend(["--resume", str(resume)])
    return command


def eval_command(args: argparse.Namespace, task: str, samples: int, output: Path) -> list[str]:
    run_train = run_paths("stage2", args.run_id)["train"]
    return [
        sys.executable,
        str(EVAL_SCRIPT),
        "--story-root", str(ROOT),
        "--run-dir", str(run_train),
        "--cache-dir", str(CACHE_DIR),
        "--cache-file", "val.pt",
        "--official-pulp-ae-control",
        "--eval-source", "stage2",
        "--output", str(output),
        "--task", task,
        "--device", args.device,
        "--split", "test",
        "--set-name", "pure_",
        "--config-name", "config_dit_xy",
        "--model-dir", str(MODEL_DIR),
        "--pulp-root", str(ROOT / "linked/PulpMotion"),
        "--data-root", str(ROOT / "linked/pulpmotion-data"),
        "--samples", str(samples),
        "--start", "0",
        "--batch-size", "32",
        "--decode-batch-size", "16",
        "--workers", "0",
        "--seed", "17",
        "--num-steps", "50",
        "--cfg-scale", "1.0",
        "--eta", "0.0",
        "--joint-human-camera-input-mode", "normal",
        "--joint-coupling-scale", "0.0" if task == "joint" else "1.0",
        "--joint-coupling-mode", "c_to_h_blocked" if task == "joint" else "symmetric",
        "--progress-every", "10",
    ]


def screen_gate(paths: dict[str, Path]) -> dict[str, Any]:
    payloads = {name: json.loads(path.read_text(encoding="utf-8")) for name, path in paths.items()}
    reasons: list[str] = []
    for name, payload in payloads.items():
        if int(payload.get("evaluated_samples", 0)) != 64:
            reasons.append(f"{name}: evaluated_samples != 64")
        owning = payload.get("owning_decoder", {})
        if owning.get("kind") != "pulp_official_autoencoder" or not owning.get("checkpoint_sha256"):
            reasons.append(f"{name}: owning official decoder was not verified")
        metrics = payload.get("metrics", {})
        if not metrics or any(not math.isfinite(float(value)) for value in metrics.values()):
            reasons.append(f"{name}: metrics are empty or non-finite")
    thresholds = {
        "human": {"test/tmr/coverage": 0.20},
        "camera": {"test/clatr/coverage": 0.20},
        "joint": {"test/tmr/coverage": 0.20, "test/clatr/coverage": 0.20},
    }
    for name, required in thresholds.items():
        metrics = payloads[name].get("metrics", {})
        for metric, minimum in required.items():
            if float(metrics.get(metric, -math.inf)) < minimum:
                reasons.append(f"{name}: {metric} < {minimum}")
        if name == "joint":
            outscreen = metrics.get("test/proj/outscreen")
            if not isinstance(outscreen, (int, float)) or not math.isfinite(float(outscreen)):
                reasons.append("joint: test/proj/outscreen is missing or non-finite")
            elif float(outscreen) > 0.70:
                reasons.append("joint: test/proj/outscreen > 0.70")
    return {
        "schema_version": 1,
        "decision": "continue_to_105k" if not reasons else "stop_after_10k",
        "gate_type": "pre_registered_structural_learnability_screen",
        "screen_samples": 64,
        "checkpoint_step": 10000,
        "thresholds": thresholds,
        "max_outscreen": {"joint": 0.70},
        "metric_applicability": {
            "human": ["test/tmr/coverage"],
            "camera": ["test/clatr/coverage"],
            "joint": ["test/tmr/coverage", "test/clatr/coverage", "test/proj/outscreen"],
        },
        "reasons": reasons,
        "artifacts": {name: str(path) for name, path in paths.items()},
        "metrics": {name: payload["metrics"] for name, payload in payloads.items()},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default="v7_46_official_ae_unified_matched_seed17_5090g3_20260717")
    parser.add_argument("--version", default="v7.46")
    parser.add_argument("--device", default="cuda:0")
    args = parser.parse_args()
    paths = run_paths("stage2", args.run_id)
    run_root = paths["root"]
    if not run_root.exists():
        init_run(
            "stage2",
            args.run_id,
            runs_root=ROOT / "runs",
            description="Frozen official Pulp AE x matched asymmetric Unified-3 representation control",
        )
        paths = run_paths("stage2", args.run_id)
        run_root = paths["root"]
    update_manifest("stage2", args.run_id, runs_root=ROOT / "runs", status="training")
    train_dir = paths["train"]
    eval_dir = paths["eval"]
    checkpoint = train_dir / "last.pt"
    if not (CACHE_DIR / "train.pt").is_file() or not (CACHE_DIR / "val.pt").is_file():
        raise FileNotFoundError(f"missing matched official cache: {CACHE_DIR}")
    contract = {
        "schema_version": 1,
        "run_id": args.run_id,
        "version": args.version,
        "purpose": "frozen official Pulp AE x same asymmetric Unified-3 representation isolation",
        "cache": {
            "train": str(CACHE_DIR / "train.pt"),
            "train_sha256": sha256_file(CACHE_DIR / "train.pt"),
            "val": str(CACHE_DIR / "val.pt"),
            "val_sha256": sha256_file(CACHE_DIR / "val.pt"),
            "train_samples": 162760,
            "val_samples": 4053,
        },
        "representation": {
            "kind": "pulp_official_aemmardm",
            "is_causal": False,
            "owning_decoder_required": True,
        },
        "matched_stage2": {
            "architecture": "width416 asymmetric Unified-3 human-first",
            "task_probs": [1, 1, 1, 0],
            "batch_size": 512,
            "phase_1": {"steps": 30000, "lr": 1.0e-4},
            "phase_2": {"steps": 105000, "lr": 3.0e-5},
            "sample_exposures": 53760000,
        },
        "screen": {
            "step": 10000,
            "samples_per_profile": 64,
            "profiles": ["human", "camera", "joint"],
            "role": "structural learnability and owning-decoder gate; not a promoted comparison",
        },
    }
    write_json(run_root / "experiment_contract.json", contract)
    step = checkpoint_step(checkpoint)
    if step < 10000:
        event("train_short_start", current_step=step, target_step=10000)
        run_logged(
            train_command(args, 10000, 1.0e-4, checkpoint if step > 0 else None),
            run_root / "driver/train_to_10k.log",
        )
    screen_paths = {task: eval_dir / f"screen10k_n64/{task}.json" for task in ("human", "camera", "joint")}
    gate_path = eval_dir / "screen10k_n64/gate.json"
    if gate_path.is_file():
        gate = json.loads(gate_path.read_text(encoding="utf-8"))
    else:
        if checkpoint_step(checkpoint) != 10000:
            raise RuntimeError("a new short screen must use the immutable step-10000 boundary")
        for task, output in screen_paths.items():
            if not output.is_file():
                event("screen_eval_start", task=task)
                run_logged(eval_command(args, task, 64, output), run_root / f"driver/screen_{task}.log")
        gate = screen_gate(screen_paths)
        write_json(gate_path, gate)
    event("screen_gate", decision=gate["decision"], reasons=gate["reasons"])
    if gate["decision"] != "continue_to_105k":
        update_manifest(
            "stage2",
            args.run_id,
            runs_root=ROOT / "runs",
            status="screen_stopped",
            artifacts={"screen_gate": str(gate_path.relative_to(ROOT / "runs"))},
        )
        return
    if checkpoint_step(checkpoint) < 30000:
        event("train_phase1_continue", target_step=30000)
        run_logged(train_command(args, 30000, 1.0e-4, checkpoint), run_root / "driver/train_to_30k.log")
    if checkpoint_step(checkpoint) < 105000:
        event("train_phase2_start", target_step=105000)
        run_logged(train_command(args, 105000, 3.0e-5, checkpoint), run_root / "driver/train_to_105k.log")
    if checkpoint_step(checkpoint) != 105000:
        raise RuntimeError("long endpoint did not reach step 105000")
    for task in ("human", "camera", "joint"):
        output = eval_dir / f"official_pure4053/{task}.json"
        if not output.is_file():
            event("formal_eval_start", task=task)
            run_logged(eval_command(args, task, 4053, output), run_root / f"driver/formal_{task}.log")
    write_json(
        run_root / "driver_complete.json",
        {
            "status": "complete",
            "checkpoint": str(checkpoint),
            "checkpoint_sha256": sha256_file(checkpoint),
            "step": 105000,
            "formal_profiles": ["human", "camera", "joint"],
        },
    )
    update_manifest(
        "stage2",
        args.run_id,
        runs_root=ROOT / "runs",
        status="complete",
        artifacts={
            "checkpoint": str(checkpoint.relative_to(ROOT / "runs")),
            "screen_gate": str(gate_path.relative_to(ROOT / "runs")),
            "formal_eval": str((eval_dir / "official_pure4053").relative_to(ROOT / "runs")),
        },
    )
    event("driver_complete", step=105000)


if __name__ == "__main__":
    main()
