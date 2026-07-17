#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import torch


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.storymotion_run_layout import init_run, run_paths

PARENT_RUN_ID = "v7_36_p0a_asym_unified3_joint30k_seed17_4090g0_20260714"
PARENT_PATHS = run_paths("stage2", PARENT_RUN_ID)
PARENT_ROOT = PARENT_PATHS["root"]
PARENT_TRAIN = PARENT_PATHS["train"]
PARENT_CHECKPOINT = PARENT_TRAIN / "last.pt"
PARENT_CHECKPOINT_SHA256 = "7dcf3b1911af144ea9ef2b30017dd07472d62f655fd04c1dc9263581e3382c0b"
CACHE_DIR = ROOT / "runs/legacy/train/stage2/v7_17_corrected_cache_20260712/joint_ae_noncausal"
CANONICAL_STATS = ROOT / "runs/train/stage2/shared/contracts/v7_36_p0_matched_20260714/train_latent_fullcov.pt"
CANONICAL_STATS_SHA256 = "c7353d25b15d66071eb286c400d099c454705c568a643c5f0c895a98c39f71d8"
CALIBRATION_META = ROOT / "runs/train/stage2/shared/contracts/v7_37_p0e_purefull_20260715/train_human_replay_calib4096/meta.json"
CALIBRATION_SAMPLE_IDS_SHA256 = "a3fce0d9d5c5d4047ee3ec37c4fde53efdfd5b9201ba4bd5b5ffe9372e8bdcaa"
MODEL_DIR = Path("/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models")
PULP_ROOT = ROOT / "linked/PulpMotion"
DATA_ROOT = ROOT / "linked/pulpmotion-data"
TRAIN_SCRIPT = ROOT / "scripts/train_stage2_condmdi_pulp.py"
EVAL_SCRIPT = ROOT / "scripts/storymotion_official_full_eval.py"
HARNESS_SCRIPT = ROOT / "scripts/storymotion_experiment_harness.py"


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


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def common_train_command(args: argparse.Namespace, stats_path: Path) -> list[str]:
    return [
        sys.executable,
        str(TRAIN_SCRIPT),
        "train",
        "--run-id",
        args.run_id,
        "--device",
        args.device,
        "--seed",
        "17",
        "--steps",
        "33000",
        "--batch-size",
        "512",
        "--num-workers",
        "0",
        "--width",
        "416",
        "--dim-mults",
        "1",
        "2",
        "2",
        "--cond-mask-prob",
        "0.1",
        "--cond-mask-prob-cam",
        "0.0",
        "--cond-mask-prob-hum",
        "0.0",
        "--generative-process",
        "diffusion",
        "--diffusion-steps",
        "1000",
        "--diffusion-prediction-type",
        "START_X",
        "--noise-schedule",
        "cosine",
        "--lr",
        "0.0001",
        "--weight-decay",
        "0.01",
        "--adam-beta2",
        "0.999",
        "--grad-clip",
        "1.0",
        "--log-every",
        "100",
        "--eval-every",
        "1000",
        "--eval-batches",
        "4",
        "--eval-samples",
        "256",
        "--test-every",
        "3000",
        "--test-batches",
        "4",
        "--test-samples",
        "256",
        "--task-probs",
        *(str(value) for value in args.task_probs),
        "--joint-loss-mode",
        "element_mean",
        "--joint-human-branch-weight",
        "1.0",
        "--joint-camera-branch-weight",
        "1.0",
        "--joint-loss-weight",
        "1.0",
        "--task-routing",
        "human_first",
        "--joint-human-camera-input-mode",
        "normal",
        "--joint-coupling-scale",
        "0.0",
        "--joint-coupling-mode",
        "c_to_h_blocked",
        "--selection-metric",
        "loss",
        "--snapshot-steps",
        "33000",
        "--obs-self-condition-prob",
        str(args.obs_prob),
        "--obs-self-condition-mode",
        args.obs_mode,
        "--obs-self-condition-noise-std",
        str(args.noise_std),
        "--v72-text-role-router",
        "--v72-aux-text-scale",
        "0.0",
        "--znorm",
        "--full-cov",
        "--znorm-stats-path",
        str(stats_path),
        "--cov-ridge",
        "0.0001",
        "--cache-dir",
        str(CACHE_DIR),
        "--resume",
        str(PARENT_CHECKPOINT),
    ]


def eval_command(args: argparse.Namespace, run_train: Path, output: Path, profile: str) -> list[str]:
    task = "joint" if profile.startswith("joint_") else profile
    command = [
        sys.executable,
        str(EVAL_SCRIPT),
        "--story-root",
        str(ROOT),
        "--run-dir",
        str(run_train),
        "--cache-dir",
        str(CACHE_DIR),
        "--cache-file",
        "val.pt",
        "--eval-source",
        "stage2",
        "--output",
        str(output),
        "--task",
        task,
        "--device",
        args.device,
        "--split",
        "test",
        "--set-name",
        "pure_",
        "--config-name",
        "config_dit_xy",
        "--model-dir",
        str(MODEL_DIR),
        "--pulp-root",
        str(PULP_ROOT),
        "--data-root",
        str(DATA_ROOT),
        "--samples",
        "4053",
        "--start",
        "0",
        "--batch-size",
        "32",
        "--decode-batch-size",
        "16",
        "--workers",
        "0",
        "--seed",
        "17",
        "--num-steps",
        "50",
        "--cfg-scale",
        "1.0",
        "--eta",
        "0.0",
        "--text-intervention",
        "none",
        "--observed-latent-intervention",
        "none",
        "--joint-camera-latent-intervention",
        "none",
        "--joint-human-camera-input-mode",
        "normal",
        "--joint-coupling-scale",
        str(getattr(args, "joint_coupling_scale", 0.0)),
        "--joint-coupling-mode",
        getattr(args, "joint_coupling_mode", "c_to_h_blocked"),
        "--progress-every",
        "10",
    ]
    if profile == "joint_cascade":
        command.extend(
            [
                "--joint-compose-camera-run-dir",
                str(run_train),
                "--joint-compose-human-task",
                "human",
                "--joint-compose-human-source",
                "generated",
                "--joint-compose-h2c-source",
                "replay",
            ]
        )
    return command


def build_contract(
    args: argparse.Namespace,
    stats_path: Path,
    checkpoint_sha256: str,
) -> dict[str, Any]:
    run_train = run_paths("stage2", args.run_id)["train"]
    contract = json.loads((PARENT_ROOT / "experiment_contract.json").read_text(encoding="utf-8"))
    contract["version"] = "v7.37"
    contract["run_id"] = args.run_id
    contract["generation_modes"] = ["completion", "parallel", "cascade"]
    contract["cache"]["z_norm_stats_path"] = str(stats_path.relative_to(ROOT))
    contract["cache"]["z_norm_stats_sha256"] = sha256_file(stats_path)
    contract["train"] = {
        "seed": 17,
        "batch_size": 512,
        "steps": 33000,
        "resume_step": 30000,
        "added_steps": 3000,
        "parent_run_id": PARENT_RUN_ID,
        "parent_checkpoint": str(PARENT_CHECKPOINT.relative_to(ROOT)),
        "parent_checkpoint_sha256": PARENT_CHECKPOINT_SHA256,
        "checkpoint": str((run_train / "last.pt").relative_to(ROOT)),
        "checkpoint_sha256": checkpoint_sha256,
        "task_probs": list(args.task_probs),
        "task_routing": "human_first",
        "joint_loss_weight": 1.0,
        "joint_coupling_scale": 0.0,
        "joint_coupling_mode": "c_to_h_blocked",
        "human_text_only": True,
        "camera_condition": "observed_human_latent_plus_camera_text",
        "obs_self_condition": {
            "scope": "observed human branch of camera-completion samples only under human_first routing",
            "probability": args.obs_prob,
            "mode": args.obs_mode,
            "noise_std_znorm": args.noise_std,
            "joint_pred_semantics": "same-timestep detached proxy; not DDIM50 replay",
        },
    }
    if args.noise_std > 0.0:
        contract["train"]["obs_self_condition"]["calibration"] = {
            "split": "train",
            "samples": 4096,
            "sample_ids_sha256": CALIBRATION_SAMPLE_IDS_SHA256,
            "human_task": "human",
            "sampler": {"steps": 50, "eta": 0.0, "cfg_scale": 1.0, "seed": 17},
            "statistic": "per-sample valid-value residual std in full-covariance-whitened human latent; p50",
        }
    contract["eval"] = {
        "protocol": "pure_full_ddim50",
        "seed": 17,
        "batch_size": 32,
        "decode_batch_size": 16,
        "sample_count": 4053,
        "sampler": {"steps": 50, "eta": 0.0, "cfg_scale": 1.0},
        "profiles": ["human", "camera", "joint_parallel", "joint_cascade"],
    }
    return contract


def verify_training(args: argparse.Namespace, run_train: Path) -> tuple[str, dict[str, int]]:
    records = load_jsonl(run_train / "train_log.jsonl")
    resume_records = [record for record in records if record.get("split") == "resume"]
    if len(resume_records) != 1:
        raise RuntimeError(f"expected exactly one resume record, found {len(resume_records)}")
    resume = resume_records[0]
    if resume.get("step") != 30000 or resume.get("target_steps") != 33000:
        raise RuntimeError(f"unexpected resume boundary: {resume}")
    if not resume.get("resume_strict") or not resume.get("optimizer_loaded"):
        raise RuntimeError(f"resume was not strict with optimizer state: {resume}")
    if resume.get("resume_missing_keys") or resume.get("resume_unexpected_keys"):
        raise RuntimeError(f"resume key mismatch: {resume}")
    train_records = [record for record in records if record.get("split") == "train"]
    final_train = max(train_records, key=lambda record: int(record["step"]))
    if final_train.get("step") != 33000:
        raise RuntimeError(f"training did not reach step 33000: {final_train.get('step')}")
    if args.obs_prob > 0.0 and final_train.get("obs_self_condition_sample_frac", 0.0) <= 0.0:
        raise RuntimeError("configured observed-source treatment had zero measured exposure")
    checkpoint_path = run_train / "last.pt"
    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    if int(checkpoint.get("step", -1)) != 33000:
        raise RuntimeError(f"last.pt step is {checkpoint.get('step')}, expected 33000")
    counts = {
        key: int(value)
        for key, value in checkpoint.get("meta", {}).get("task_exposure_counts", {}).items()
    }
    parent_meta = json.loads((PARENT_TRAIN / "meta.json").read_text(encoding="utf-8"))
    parent_counts = {key: int(value) for key, value in parent_meta["task_exposure_counts"].items()}
    exposure_delta = {key: counts.get(key, 0) - parent_counts.get(key, 0) for key in parent_counts}
    if sum(exposure_delta.values()) != 3000 * 512:
        raise RuntimeError(f"unexpected exposure delta: {exposure_delta}")
    return sha256_file(checkpoint_path), exposure_delta


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one v7.37 3k short arm and all matched pure4053 DDIM50 profiles.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--task-probs", nargs=4, type=float, required=True)
    parser.add_argument("--obs-mode", choices=["clean", "noisy", "joint_pred", "mixed"], required=True)
    parser.add_argument("--obs-prob", type=float, required=True)
    parser.add_argument("--noise-std", type=float, required=True)
    parser.add_argument("--description", required=True)
    args = parser.parse_args()
    if not 0.0 <= args.obs_prob <= 1.0:
        parser.error("--obs-prob must be in [0,1]")
    if args.noise_std < 0.0:
        parser.error("--noise-std must be non-negative")

    paths = run_paths("stage2", args.run_id)
    run_root = paths["root"]
    run_train = paths["train"]
    eval_dir = paths["eval"] / "official_pure4053_matched"
    if run_root.exists():
        raise FileExistsError(f"refusing to reuse run root: {run_root}")
    init_run("stage2", args.run_id, description=args.description)
    eval_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = run_root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update({
        "status": "preflight",
        "description": args.description,
        "driver_pid": os.getpid(),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    })
    write_json(manifest_path, manifest)
    try:
        for path in (PARENT_CHECKPOINT, CANONICAL_STATS, CACHE_DIR / "train.pt", CACHE_DIR / "val.pt"):
            if not path.is_file():
                raise FileNotFoundError(path)
        if sha256_file(PARENT_CHECKPOINT) != PARENT_CHECKPOINT_SHA256:
            raise RuntimeError("parent A-30k checkpoint hash mismatch")
        if sha256_file(CANONICAL_STATS) != CANONICAL_STATS_SHA256:
            raise RuntimeError("canonical full-covariance stats hash mismatch")
        if args.noise_std > 0.0:
            calibration = json.loads(CALIBRATION_META.read_text(encoding="utf-8"))
            train_calibration = calibration["files"]["train.pt"]
            if train_calibration["sample_ids_sha256"] != CALIBRATION_SAMPLE_IDS_SHA256:
                raise RuntimeError("train-only calibration sample IDs changed")
            if train_calibration["human_task"] != "human" or train_calibration["num_steps"] != 50:
                raise RuntimeError("train-only calibration is not human DDIM50")
        stats_path = paths["cache"] / "train_latent_fullcov.pt"
        stats_path.parent.mkdir(parents=True)
        shutil.copy2(CANONICAL_STATS, stats_path)
        if sha256_file(stats_path) != CANONICAL_STATS_SHA256:
            raise RuntimeError("per-run stats copy hash mismatch")
        command = common_train_command(args, stats_path)
        check_command = command.copy()
        check_command[2] = "check"
        event("preflight_start", run_id=args.run_id)
        run_logged(check_command, run_root / "preflight.log")
        manifest["status"] = "training"
        write_json(manifest_path, manifest)
        event("training_start", run_id=args.run_id)
        run_logged(command, run_train / "launcher.log")
        checkpoint_sha256, exposure_delta = verify_training(args, run_train)
        contract_path = run_root / "experiment_contract.json"
        contract = build_contract(args, stats_path, checkpoint_sha256)
        write_json(contract_path, contract)
        subprocess.run(
            [sys.executable, str(HARNESS_SCRIPT), "audit-contract", str(contract_path)],
            cwd=ROOT,
            check=True,
        )
        manifest["status"] = "evaluating_pure_full"
        manifest["checkpoint_sha256"] = checkpoint_sha256
        manifest["exposure_delta"] = exposure_delta
        write_json(manifest_path, manifest)
        outputs: dict[str, str] = {}
        for profile in ("human", "camera", "joint_parallel", "joint_cascade"):
            output = eval_dir / f"{profile}.json"
            event("pure_full_start", run_id=args.run_id, profile=profile)
            run_logged(eval_command(args, run_train, output, profile), eval_dir / f"{profile}.log")
            subprocess.run(
                [
                    sys.executable,
                    str(HARNESS_SCRIPT),
                    "audit-eval",
                    str(contract_path),
                    str(output),
                    "--require-pure-full",
                ],
                cwd=ROOT,
                check=True,
            )
            outputs[profile] = str(output.relative_to(ROOT))
            event("pure_full_complete", run_id=args.run_id, profile=profile)
        manifest["status"] = "complete"
        manifest["completed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        manifest["artifacts"] = outputs
        write_json(manifest_path, manifest)
        write_json(
            run_root / "driver_complete.json",
            {
                "run_id": args.run_id,
                "checkpoint_sha256": checkpoint_sha256,
                "exposure_delta": exposure_delta,
                "pure_full_artifacts": outputs,
                "completed_at": manifest["completed_at"],
            },
        )
        event("driver_complete", run_id=args.run_id)
    except Exception as exc:
        manifest["status"] = "failed"
        manifest["error"] = f"{type(exc).__name__}: {exc}"
        manifest["failed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        write_json(manifest_path, manifest)
        event("driver_failed", run_id=args.run_id, error=manifest["error"])
        raise


if __name__ == "__main__":
    main()
