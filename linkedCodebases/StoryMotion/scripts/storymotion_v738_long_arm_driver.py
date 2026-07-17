#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import torch

import storymotion_v737_short_arm_driver as short
from storymotion_run_layout import init_run, run_paths


ROOT = short.ROOT
TRAIN_SCRIPT = short.TRAIN_SCRIPT
HARNESS_SCRIPT = short.HARNESS_SCRIPT
POSTHOC_TRACKING_SCRIPT = ROOT / "scripts/eval_v738_resume_snapshots.py"
CANONICAL_STATS = short.CANONICAL_STATS
CANONICAL_STATS_SHA256 = short.CANONICAL_STATS_SHA256
CACHE_DIR = short.CACHE_DIR
FORMAL_PROFILES = ("human", "camera", "joint_parallel", "joint_cascade")
TEMPORAL_PATTERN_NAMES = ("span", "prefix", "suffix", "sparse", "mixed")


def train_command(
    args: argparse.Namespace,
    parent_checkpoint: Path,
    stats_path: Path,
) -> list[str]:
    periodic = args.tracking_mode == "periodic"
    return [
        sys.executable,
        str(TRAIN_SCRIPT),
        "train",
        "--run-id",
        args.run_id,
        "--device",
        args.device,
        "--seed",
        str(args.seed),
        "--steps",
        str(args.steps),
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
        str(args.lr),
        "--weight-decay",
        "0.01",
        "--adam-beta2",
        "0.999",
        "--grad-clip",
        "1.0",
        "--log-every",
        "100",
        "--eval-every",
        "1000" if periodic else "1000000000",
        "--eval-batches",
        "4" if periodic else "1",
        "--eval-samples",
        "256",
        "--test-every",
        "3000" if periodic else "1000000000",
        "--test-batches",
        "4" if periodic else "1",
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
        str(args.joint_loss_weight),
        "--task-routing",
        args.task_routing,
        "--joint-human-camera-input-mode",
        "normal",
        "--joint-coupling-scale",
        str(args.joint_coupling_scale),
        "--joint-coupling-mode",
        args.joint_coupling_mode,
        "--selection-metric",
        "auto",
        "--snapshot-steps",
        *(str(value) for value in args.snapshot_steps),
        "--obs-self-condition-prob",
        str(args.obs_prob),
        "--obs-self-condition-mode",
        args.obs_mode,
        "--obs-self-condition-noise-std",
        str(args.noise_std),
        "--temporal-mask-probability",
        str(args.temporal_mask_probability),
        "--temporal-mask-task-weights",
        *(str(value) for value in args.temporal_mask_task_weights),
        "--v72-text-role-router",
        "--v72-aux-text-scale",
        "0.0",
        "--znorm",
        "--znorm-stats-path",
        str(stats_path),
        "--cov-ridge",
        "0.0001",
        "--cache-dir",
        str(CACHE_DIR),
        "--resume",
        str(parent_checkpoint),
    ]


def verify_training(
    args: argparse.Namespace,
    parent_checkpoint: dict[str, Any],
    run_train: Path,
    run_eval: Path,
) -> tuple[str, dict[str, int], dict[str, int]]:
    records = short.load_jsonl(run_train / "train_log.jsonl")
    resume_records = [record for record in records if record.get("split") == "resume"]
    if len(resume_records) != 1:
        raise RuntimeError(f"expected one resume record, found {len(resume_records)}")
    parent_step = int(parent_checkpoint["step"])
    resume = resume_records[0]
    if resume.get("step") != parent_step or resume.get("target_steps") != args.steps:
        raise RuntimeError(f"unexpected resume boundary: {resume}")
    if not resume.get("resume_strict") or not resume.get("optimizer_loaded"):
        raise RuntimeError(f"resume was not strict with optimizer state: {resume}")
    if resume.get("resume_missing_keys") or resume.get("resume_unexpected_keys"):
        raise RuntimeError(f"resume key mismatch: {resume}")
    eval_steps = [int(record["step"]) for record in records if record.get("split") == "eval"]
    test_steps = [int(record["step"]) for record in records if record.get("split") == "test"]
    if args.tracking_mode == "periodic":
        expected_eval = [
            step for step in range(parent_step + 1, args.steps + 1) if step % 1000 == 0
        ]
        expected_test = [
            step for step in range(parent_step + 1, args.steps + 1) if step % 3000 == 0
        ]
    else:
        expected_eval = []
        expected_test = []
    if eval_steps != expected_eval or test_steps != expected_test:
        raise RuntimeError(
            f"training diagnostic cadence mismatch: eval={eval_steps}, test={test_steps}"
        )
    if not (run_train / "tensorboard").is_dir():
        raise RuntimeError("resume run is missing TensorBoard tracking")
    if args.tracking_mode == "periodic" and not (run_train / "best_eval.pt").is_file():
        raise RuntimeError("periodic tracking is missing best_eval.pt")
    if args.tracking_mode == "posthoc" and not (run_eval / "posthoc_tracking/summary.json").is_file():
        raise RuntimeError("posthoc tracking summary is missing")
    train_records = [record for record in records if record.get("split") == "train"]
    last_logged_step = max((int(record["step"]) for record in train_records), default=-1)
    if last_logged_step > args.steps or args.steps - last_logged_step >= 100:
        raise RuntimeError(
            f"train log does not reach the final log interval: {last_logged_step} -> {args.steps}"
        )
    if args.obs_prob > 0.0 and not any(record.get("obs_self_condition_sample_frac", 0.0) > 0.0 for record in train_records):
        raise RuntimeError("configured observed-source treatment had zero measured exposure")

    checkpoint_path = run_train / "last.pt"
    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    if int(checkpoint.get("step", -1)) != args.steps:
        raise RuntimeError(f"last.pt step is {checkpoint.get('step')}, expected {args.steps}")
    parent_counts = parent_checkpoint.get("meta", {}).get("task_exposure_counts", {})
    final_counts = checkpoint.get("meta", {}).get("task_exposure_counts", {})
    exposure_delta = {
        name: int(final_counts.get(name, 0)) - int(parent_counts.get(name, 0))
        for name in final_counts
    }
    expected_samples = (args.steps - parent_step) * 512
    if sum(exposure_delta.values()) != expected_samples:
        raise RuntimeError(f"unexpected task exposure delta: {exposure_delta}")

    parent_temporal = parent_checkpoint.get("meta", {}).get("temporal_mask_exposure_counts", {})
    final_temporal = checkpoint.get("meta", {}).get("temporal_mask_exposure_counts", {})
    temporal_delta = {
        name: int(final_temporal.get(name, 0)) - int(parent_temporal.get(name, 0))
        for name in final_temporal
    }
    if args.temporal_mask_probability > 0.0:
        for index, name in enumerate(("camera", "human", "joint")):
            if (
                args.task_probs[index] > 0.0
                and args.temporal_mask_task_weights[index] > 0.0
                and temporal_delta.get(f"task_{name}", 0) <= 0
            ):
                raise RuntimeError(f"temporal task {name} had zero exposure")
    return short.sha256_file(checkpoint_path), exposure_delta, temporal_delta


def build_contract(
    args: argparse.Namespace,
    parent_root: Path,
    parent_checkpoint_path: Path,
    parent_checkpoint_sha256: str,
    parent_step: int,
    stats_path: Path,
    checkpoint_sha256: str,
) -> dict[str, Any]:
    run_train = run_paths("stage2", args.run_id)["train"]
    contract = json.loads((parent_root / "experiment_contract.json").read_text(encoding="utf-8"))
    contract["version"] = args.version
    contract["run_id"] = args.run_id
    generation_modes = []
    if {"human", "camera"}.intersection(args.formal_profiles):
        generation_modes.append("completion")
    if "joint_parallel" in args.formal_profiles:
        generation_modes.append("parallel")
    if "joint_cascade" in args.formal_profiles:
        generation_modes.append("cascade")
    contract["generation_modes"] = generation_modes
    if args.temporal_mask_probability > 0.0:
        contract["generation_modes"].append("temporal_completion")
    contract["cache"]["z_norm_stats_path"] = str(stats_path.relative_to(ROOT))
    contract["cache"]["z_norm_stats_sha256"] = short.sha256_file(stats_path)
    contract["train"] = {
        "seed": args.seed,
        "batch_size": 512,
        "steps": args.steps,
        "resume_step": parent_step,
        "added_steps": args.steps - parent_step,
        "parent_run_id": args.parent_run_id,
        "parent_checkpoint": str(parent_checkpoint_path.relative_to(ROOT)),
        "parent_checkpoint_sha256": parent_checkpoint_sha256,
        "checkpoint": str((run_train / "last.pt").relative_to(ROOT)),
        "checkpoint_sha256": checkpoint_sha256,
        "task_probs": list(args.task_probs),
        "task_routing": args.task_routing,
        "joint_loss_weight": args.joint_loss_weight,
        "joint_coupling_scale": args.joint_coupling_scale,
        "joint_coupling_mode": args.joint_coupling_mode,
        "human_text_only": args.task_routing == "human_first",
        "camera_condition": "observed_human_latent_plus_camera_text",
        "learning_rate": args.lr,
        "snapshot_steps": list(args.snapshot_steps),
        "training_diagnostics": {
            "log_every": 100,
            "tracking_mode": args.tracking_mode,
            "eval_every": 1000 if args.tracking_mode == "periodic" else None,
            "test_every": 3000 if args.tracking_mode == "periodic" else None,
            "eval_samples": 256,
            "test_samples": 256,
            "selection_scope": "latent teacher-forced diagnostics only; formal ranking remains pure4053 DDIM50",
        },
        "obs_self_condition": {
            "scope": "observed human branch of camera-completion samples only",
            "probability": args.obs_prob,
            "mode": args.obs_mode,
            "noise_std_znorm": args.noise_std,
            "joint_pred_semantics": "same-timestep detached proxy; not DDIM50 replay",
        },
        "temporal_mask": {
            "probability": args.temporal_mask_probability,
            "task_weights": list(args.temporal_mask_task_weights),
            "patterns": list(TEMPORAL_PATTERN_NAMES),
            "whole_branch_replay": True,
            "fixed_batch_denominator": True,
        },
    }
    if args.noise_std > 0.0:
        contract["train"]["obs_self_condition"]["calibration"] = {
            "split": "train",
            "samples": 4096,
            "sample_ids_sha256": short.CALIBRATION_SAMPLE_IDS_SHA256,
            "human_task": "human",
            "sampler": {"steps": 50, "eta": 0.0, "cfg_scale": 1.0, "seed": 17},
            "statistic": "p50 valid-value residual std in full-covariance-whitened human latent",
        }
    contract["eval"] = {
        "protocol": "pure_full_ddim50",
        "seed": 17,
        "batch_size": 32,
        "decode_batch_size": 16,
        "sample_count": 4053,
        "sampler": {"steps": 50, "eta": 0.0, "cfg_scale": 1.0},
        "profiles": list(args.formal_profiles),
        "selection_rule": "only audited pure4053 full reverse-sampling artifacts may rank checkpoints",
    }
    return contract


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one v7.38 long continuation and final matched pure4053 evaluation.")
    parser.add_argument("--version", default="v7.38")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--parent-run-id", required=True)
    parser.add_argument("--parent-checkpoint-sha256", required=True)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--steps", type=int, default=120000)
    parser.add_argument("--lr", type=float, default=3.0e-5)
    parser.add_argument("--snapshot-steps", type=int, nargs="+", required=True)
    parser.add_argument("--task-probs", nargs=4, type=float, required=True)
    parser.add_argument("--task-routing", choices=["symmetric", "human_first"], default="human_first")
    parser.add_argument("--joint-loss-weight", type=float, default=1.0)
    parser.add_argument("--joint-coupling-scale", type=float, default=0.0)
    parser.add_argument(
        "--joint-coupling-mode",
        choices=["symmetric", "c_to_h_blocked"],
        default="c_to_h_blocked",
    )
    parser.add_argument("--obs-mode", choices=["clean", "noisy", "joint_pred", "mixed"], required=True)
    parser.add_argument("--obs-prob", type=float, required=True)
    parser.add_argument("--noise-std", type=float, required=True)
    parser.add_argument("--temporal-mask-probability", type=float, default=0.0)
    parser.add_argument("--temporal-mask-task-weights", nargs=3, type=float, default=[1.0, 1.0, 1.0])
    parser.add_argument("--description", required=True)
    parser.add_argument(
        "--formal-profiles",
        nargs="+",
        choices=FORMAL_PROFILES,
        default=list(FORMAL_PROFILES),
    )
    parser.add_argument("--tracking-mode", choices=["periodic", "posthoc"], default="periodic")
    args = parser.parse_args()
    if args.steps <= 0 or args.lr <= 0.0:
        parser.error("--steps and --lr must be positive")
    if args.joint_loss_weight < 0.0:
        parser.error("--joint-loss-weight must be non-negative")
    if not 0.0 <= args.joint_coupling_scale <= 1.0:
        parser.error("--joint-coupling-scale must be in [0,1]")
    if args.task_routing == "human_first" and (
        args.joint_coupling_scale != 0.0 or args.joint_coupling_mode != "c_to_h_blocked"
    ):
        parser.error("human_first requires coupling scale 0 and c_to_h_blocked mode")
    if not 0.0 <= args.obs_prob <= 1.0 or args.noise_std < 0.0:
        parser.error("invalid observed-source treatment")
    if not 0.0 <= args.temporal_mask_probability <= 1.0:
        parser.error("--temporal-mask-probability must be in [0,1]")
    if any(value < 0.0 for value in args.temporal_mask_task_weights):
        parser.error("temporal task weights must be non-negative")
    if sorted(set(args.snapshot_steps)) != args.snapshot_steps or args.snapshot_steps[-1] > args.steps:
        parser.error("snapshot steps must be sorted, unique, and no greater than --steps")
    profile_requirements = {
        "camera": (0,),
        "human": (1,),
        "joint_parallel": (2,),
        "joint_cascade": (0, 1),
    }
    for profile in args.formal_profiles:
        if any(args.task_probs[index] <= 0.0 for index in profile_requirements[profile]):
            parser.error(f"formal profile {profile} requires trained task probabilities")
    if "joint_parallel" in args.formal_profiles and args.joint_loss_weight <= 0.0:
        parser.error("joint_parallel formal evaluation requires positive joint loss weight")
    if "joint_cascade" in args.formal_profiles and args.task_routing != "human_first":
        parser.error("joint_cascade formal evaluation requires human_first routing")

    parent_paths = run_paths("stage2", args.parent_run_id)
    parent_root = parent_paths["root"]
    parent_checkpoint_path = parent_paths["train"] / "last.pt"
    paths = run_paths("stage2", args.run_id)
    run_root = paths["root"]
    run_train = paths["train"]
    eval_dir = paths["eval"] / "official_pure4053_matched"
    if run_root.exists():
        raise FileExistsError(f"refusing to reuse run root: {run_root}")
    parent_contract = json.loads((parent_root / "experiment_contract.json").read_text(encoding="utf-8"))
    init_run(
        "stage2",
        args.run_id,
        parent_stage1_run=parent_contract["parent_stage1"]["run_id"],
        description=args.description,
    )
    eval_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = run_root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update({
        "version": args.version,
        "status": "preflight",
        "driver_pid": os.getpid(),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    })
    short.write_json(manifest_path, manifest)
    try:
        for path in (parent_checkpoint_path, parent_root / "experiment_contract.json", CANONICAL_STATS, CACHE_DIR / "train.pt", CACHE_DIR / "val.pt"):
            if not path.is_file():
                raise FileNotFoundError(path)
        if short.sha256_file(parent_checkpoint_path) != args.parent_checkpoint_sha256:
            raise RuntimeError("parent checkpoint hash mismatch")
        if short.sha256_file(CANONICAL_STATS) != CANONICAL_STATS_SHA256:
            raise RuntimeError("canonical full-covariance stats hash mismatch")
        if args.noise_std > 0.0:
            calibration = json.loads(short.CALIBRATION_META.read_text(encoding="utf-8"))
            train_calibration = calibration["files"]["train.pt"]
            if train_calibration["sample_ids_sha256"] != short.CALIBRATION_SAMPLE_IDS_SHA256:
                raise RuntimeError("train-only calibration sample IDs changed")
            if train_calibration["human_task"] != "human" or train_calibration["num_steps"] != 50:
                raise RuntimeError("train-only calibration is not human DDIM50")
        loaded_parent_checkpoint = torch.load(parent_checkpoint_path, map_location="cpu")
        parent_checkpoint = {
            "step": int(loaded_parent_checkpoint.get("step", -1)),
            "meta": loaded_parent_checkpoint.get("meta", {}),
        }
        del loaded_parent_checkpoint
        parent_step = int(parent_checkpoint["step"])
        if not 0 < parent_step < args.steps:
            raise RuntimeError(f"invalid parent/target steps: {parent_step} -> {args.steps}")
        if any(step <= parent_step for step in args.snapshot_steps):
            raise RuntimeError("snapshot steps must be greater than the parent step")

        stats_path = paths["cache"] / "train_latent_fullcov.pt"
        stats_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(CANONICAL_STATS, stats_path)
        launch_contract = {
            "run_id": args.run_id,
            "parent_run_id": args.parent_run_id,
            "parent_checkpoint_sha256": args.parent_checkpoint_sha256,
            "parent_step": parent_step,
            "target_step": args.steps,
            "stats_sha256": short.sha256_file(stats_path),
            "train_cache_sha256": short.sha256_file(CACHE_DIR / "train.pt"),
            "eval_cache_sha256": short.sha256_file(CACHE_DIR / "val.pt"),
            "seed": args.seed,
            "batch_size": 512,
            "task_probs": list(args.task_probs),
            "task_routing": args.task_routing,
            "joint_loss_weight": args.joint_loss_weight,
            "joint_coupling_scale": args.joint_coupling_scale,
            "joint_coupling_mode": args.joint_coupling_mode,
            "obs_mode": args.obs_mode,
            "obs_prob": args.obs_prob,
            "noise_std": args.noise_std,
            "temporal_mask_probability": args.temporal_mask_probability,
            "temporal_mask_task_weights": list(args.temporal_mask_task_weights),
            "tracking_mode": args.tracking_mode,
            "single_step_eval_test_disabled": args.tracking_mode == "posthoc",
            "formal_profiles": list(args.formal_profiles),
            "formal_eval_protocol": "pure4053_ddim50_cfg1_eta0_seed17",
            "script_hashes": {
                Path(__file__).name: short.sha256_file(Path(__file__)),
                Path(short.__file__).name: short.sha256_file(Path(short.__file__)),
                TRAIN_SCRIPT.name: short.sha256_file(TRAIN_SCRIPT),
                short.EVAL_SCRIPT.name: short.sha256_file(short.EVAL_SCRIPT),
                HARNESS_SCRIPT.name: short.sha256_file(HARNESS_SCRIPT),
                POSTHOC_TRACKING_SCRIPT.name: short.sha256_file(POSTHOC_TRACKING_SCRIPT),
            },
        }
        short.write_json(run_root / "launch_contract.json", launch_contract)
        command = train_command(args, parent_checkpoint_path, stats_path)
        check_command = command.copy()
        check_command[2] = "check"
        short.event("preflight_start", run_id=args.run_id)
        short.run_logged(check_command, run_root / "preflight.log")
        if short.sha256_file(stats_path) != CANONICAL_STATS_SHA256:
            raise RuntimeError("preflight changed the canonical stats copy")
        manifest["status"] = "training"
        manifest["parent_step"] = parent_step
        manifest["target_step"] = args.steps
        short.write_json(manifest_path, manifest)
        short.event("training_start", run_id=args.run_id)
        short.run_logged(command, run_train / "launcher.log")
        if args.tracking_mode == "posthoc":
            short.event("posthoc_tracking_start", run_id=args.run_id)
            short.run_logged(
                [
                    sys.executable,
                    str(POSTHOC_TRACKING_SCRIPT),
                    "--run-id",
                    args.run_id,
                    "--device",
                    args.device,
                ],
                eval_dir / "posthoc_tracking/launcher.log",
            )
        checkpoint_sha256, exposure_delta, temporal_delta = verify_training(
            args, parent_checkpoint, run_train, paths["eval"]
        )
        if short.sha256_file(stats_path) != CANONICAL_STATS_SHA256:
            raise RuntimeError("training changed the canonical stats copy")

        contract_path = run_root / "experiment_contract.json"
        contract = build_contract(
            args,
            parent_root,
            parent_checkpoint_path,
            args.parent_checkpoint_sha256,
            parent_step,
            stats_path,
            checkpoint_sha256,
        )
        short.write_json(contract_path, contract)
        subprocess.run([sys.executable, str(HARNESS_SCRIPT), "audit-contract", str(contract_path)], cwd=ROOT, check=True)
        manifest["status"] = "evaluating_pure_full"
        manifest["checkpoint_sha256"] = checkpoint_sha256
        manifest["exposure_delta"] = exposure_delta
        manifest["temporal_exposure_delta"] = temporal_delta
        short.write_json(manifest_path, manifest)
        outputs: dict[str, str] = {}
        for profile in args.formal_profiles:
            output = eval_dir / f"{profile}.json"
            short.event("pure_full_start", run_id=args.run_id, profile=profile)
            short.run_logged(short.eval_command(args, run_train, output, profile), eval_dir / f"{profile}.log")
            subprocess.run(
                [sys.executable, str(HARNESS_SCRIPT), "audit-eval", str(contract_path), str(output), "--require-pure-full"],
                cwd=ROOT,
                check=True,
            )
            outputs[profile] = str(output.relative_to(ROOT))
            short.event("pure_full_complete", run_id=args.run_id, profile=profile)
        manifest["status"] = "complete"
        manifest["completed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        manifest["artifacts"] = outputs
        short.write_json(manifest_path, manifest)
        short.write_json(
            run_root / "driver_complete.json",
            {
                "run_id": args.run_id,
                "checkpoint_sha256": checkpoint_sha256,
                "exposure_delta": exposure_delta,
                "temporal_exposure_delta": temporal_delta,
                "pure_full_artifacts": outputs,
                "completed_at": manifest["completed_at"],
            },
        )
        short.event("driver_complete", run_id=args.run_id)
    except Exception as exc:
        manifest["status"] = "failed"
        manifest["error"] = f"{type(exc).__name__}: {exc}"
        manifest["failed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        short.write_json(manifest_path, manifest)
        short.event("driver_failed", run_id=args.run_id, error=manifest["error"])
        raise


if __name__ == "__main__":
    main()
