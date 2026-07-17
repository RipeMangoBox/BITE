#!/usr/bin/env python3
"""Plan or run the v7.38 same-implementation specialist queue on one GPU.

The primary comparison resumes the exact shared A30 checkpoint and allocates
one-hot continuation updates so each specialist matches the corresponding L0
Phase-II task exposure.  The three primary continuations also sum to the L0
Phase-II update budget.  An optional, separately labelled sensitivity gives
each specialist the full L0 Phase-II update count; its ensemble costs 3x.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

import storymotion_v737_short_arm_driver as short
from storymotion_run_layout import run_paths


ROOT = Path(__file__).resolve().parents[1]
LONG_DRIVER = ROOT / "scripts/storymotion_v738_long_arm_driver.py"
HARNESS = ROOT / "scripts/storymotion_experiment_harness.py"
TRAINER = ROOT / "scripts/train_stage2_condmdi_pulp.py"
EVALUATOR = ROOT / "scripts/storymotion_official_full_eval.py"

DEFAULT_PARENT = "v7_36_p0a_asym_unified3_joint30k_seed17_4090g0_20260714"
DEFAULT_REFERENCE = "v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715"
DEFAULT_PARENT_SHA256 = "7dcf3b1911af144ea9ef2b30017dd07472d62f655fd04c1dc9263581e3382c0b"
DEFAULT_REFERENCE_SHA256 = "ab474d353a29a4ee707c8ed4e37599fcc47ea79c124452ebdd366d5bdafdaf35"
DEFAULT_STAGE1_SHA256 = "91248bf440a4a5493a0f8b4994d6d36479fcaa221d331f6995a91ed1af8e7ce1"
DEFAULT_TRAIN_CACHE_SHA256 = "f7a00a483395fc993faae304e5b63b64f12163033b2f96fd073f4f7e3a3a5983"
DEFAULT_EVAL_CACHE_SHA256 = "6f13816cb8705f0aea239c1a8f62e6fdd730654a78b83124af90fd581efb9b25"
DEFAULT_STATS_SHA256 = "c7353d25b15d66071eb286c400d099c454705c568a643c5f0c895a98c39f71d8"
BATCH_SIZE = 512

TASKS = (
    {"name": "human", "index": 1, "task_probs": [0.0, 1.0, 0.0, 0.0], "profile": "human"},
    {"name": "camera", "index": 0, "task_probs": [1.0, 0.0, 0.0, 0.0], "profile": "camera"},
    {"name": "joint", "index": 2, "task_probs": [0.0, 0.0, 1.0, 0.0], "profile": "joint_parallel"},
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_root(run_id: str) -> Path:
    return run_paths("stage2", run_id)["root"]


def largest_remainder_steps(
    exposure_delta: dict[str, int], total_steps: int, batch_size: int = BATCH_SIZE
) -> dict[str, int]:
    """Allocate integer steps while preserving the ensemble update total."""
    exact = {name: exposure_delta[name] / batch_size for name in exposure_delta}
    result = {name: math.floor(value) for name, value in exact.items()}
    remaining = total_steps - sum(result.values())
    if remaining < 0 or remaining > len(result):
        raise RuntimeError(
            f"exposure deltas cannot be reconciled with {total_steps} steps: {exact}"
        )
    order = sorted(exact, key=lambda name: (exact[name] - result[name], name), reverse=True)
    for name in order[:remaining]:
        result[name] += 1
    if sum(result.values()) != total_steps:
        raise AssertionError(result)
    return result


def validate_source(parent_id: str, reference_id: str) -> dict[str, Any]:
    parent = run_root(parent_id)
    reference = run_root(reference_id)
    required = (
        parent / "experiment_contract.json",
        parent / "train/meta.json",
        parent / "train/last.pt",
        reference / "experiment_contract.json",
        reference / "train/meta.json",
        reference / "train/last.pt",
    )
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)
    parent_contract = read_json(parent / "experiment_contract.json")
    reference_contract = read_json(reference / "experiment_contract.json")
    parent_meta = read_json(parent / "train/meta.json")
    reference_meta = read_json(reference / "train/meta.json")

    if reference_contract["train"]["parent_run_id"] != parent_id:
        raise RuntimeError("reference L0 does not resume the declared common parent")
    if reference_contract["train"]["parent_checkpoint_sha256"] != DEFAULT_PARENT_SHA256:
        raise RuntimeError("reference L0 parent checkpoint hash changed")
    if reference_contract["train"]["checkpoint_sha256"] != DEFAULT_REFERENCE_SHA256:
        raise RuntimeError("reference L0 checkpoint hash changed")
    if reference_contract["train"]["task_probs"] != [1.0, 1.0, 1.0, 0.0]:
        raise RuntimeError("reference L0 is not the registered balanced Unified-3 run")
    if reference_contract["train"]["task_routing"] != "human_first":
        raise RuntimeError("reference L0 does not use human-first routing")
    if reference_contract["train"]["obs_self_condition"]["probability"] != 0.0:
        raise RuntimeError("reference L0 is not the clean arm")
    if reference_contract["train"]["temporal_mask"]["probability"] != 0.0:
        raise RuntimeError("reference L0 unexpectedly enables temporal completion")
    for contract in (parent_contract, reference_contract):
        if contract["tasks"] != ["human", "camera", "joint"]:
            raise RuntimeError("source contract is not Unified-3")
        if contract["parent_stage1"]["checkpoint_sha256"] != DEFAULT_STAGE1_SHA256:
            raise RuntimeError("source does not use corrected v7.14 Stage1")
        if contract["parent_stage1"]["owning_decoder_sha256"] != DEFAULT_STAGE1_SHA256:
            raise RuntimeError("source owning decoder changed")
        if contract["cache"]["tokenizer_checkpoint_sha256"] != DEFAULT_STAGE1_SHA256:
            raise RuntimeError("source cache tokenizer changed")
        if contract["cache"]["train_sha256"] != DEFAULT_TRAIN_CACHE_SHA256:
            raise RuntimeError("source train cache changed")
        if contract["cache"]["eval_sha256"] != DEFAULT_EVAL_CACHE_SHA256:
            raise RuntimeError("source eval cache changed")
        if contract["cache"]["z_norm_source_train_sha256"] != DEFAULT_TRAIN_CACHE_SHA256:
            raise RuntimeError("source z-normalization is not train-cache-only")
    if reference_contract["cache"]["z_norm_stats_sha256"] != DEFAULT_STATS_SHA256:
        raise RuntimeError("reference full-covariance statistics changed")

    parent_step = int(reference_contract["train"]["resume_step"])
    reference_step = int(reference_contract["train"]["steps"])
    reference_added_steps = int(reference_contract["train"]["added_steps"])
    if parent_step != 30000 or reference_step != 105000 or reference_added_steps != 75000:
        raise RuntimeError("source curriculum is not the registered 30k -> 105k L0 schedule")
    parent_counts = {key: int(value) for key, value in parent_meta["task_exposure_counts"].items()}
    reference_counts = {
        key: int(value) for key, value in reference_meta["task_exposure_counts"].items()
    }
    exposure_delta = {
        name: reference_counts[name] - parent_counts[name]
        for name in ("camera", "human", "joint")
    }
    if sum(exposure_delta.values()) != reference_added_steps * BATCH_SIZE:
        raise RuntimeError(f"reference exposure ledger does not close: {exposure_delta}")
    allocated_steps = largest_remainder_steps(exposure_delta, reference_added_steps)
    return {
        "parent_id": parent_id,
        "reference_id": reference_id,
        "parent_step": parent_step,
        "reference_step": reference_step,
        "reference_added_steps": reference_added_steps,
        "parent_counts": parent_counts,
        "reference_counts": reference_counts,
        "exposure_delta": exposure_delta,
        "allocated_steps": allocated_steps,
    }


def driver_command(
    *,
    version: str,
    run_id: str,
    parent_id: str,
    parent_sha256: str,
    target_step: int,
    task: dict[str, Any],
    device: str,
    description: str,
) -> list[str]:
    return [
        sys.executable,
        str(LONG_DRIVER),
        "--version",
        version,
        "--run-id",
        run_id,
        "--parent-run-id",
        parent_id,
        "--parent-checkpoint-sha256",
        parent_sha256,
        "--device",
        device,
        "--seed",
        "17",
        "--steps",
        str(target_step),
        "--lr",
        "3e-5",
        "--snapshot-steps",
        str(target_step),
        "--task-probs",
        *(str(value) for value in task["task_probs"]),
        "--obs-mode",
        "clean",
        "--obs-prob",
        "0",
        "--noise-std",
        "0",
        "--temporal-mask-probability",
        "0",
        "--formal-profiles",
        task["profile"],
        "--tracking-mode",
        "posthoc",
        "--description",
        description,
    ]


def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    source = validate_source(args.parent_run_id, args.reference_run_id)
    code_hashes = {
        "trainer_sha256": short.sha256_file(TRAINER),
        "evaluator_sha256": short.sha256_file(EVALUATOR),
        "long_driver_sha256": short.sha256_file(LONG_DRIVER),
        "queue_driver_sha256": short.sha256_file(Path(__file__)),
    }
    primary = []
    sensitivity = []
    for task in TASKS:
        name = task["name"]
        added_steps = source["allocated_steps"][name]
        target_step = source["parent_step"] + added_steps
        run_id = f"{args.run_prefix}_{name}_exposure_matched"
        mismatch = added_steps * BATCH_SIZE - source["exposure_delta"][name]
        primary.append(
            {
                "task": name,
                "run_id": run_id,
                "parent_run_id": args.parent_run_id,
                "parent_checkpoint_sha256": DEFAULT_PARENT_SHA256,
                "added_steps": added_steps,
                "target_step": target_step,
                "task_probs": task["task_probs"],
                "formal_profile": task["profile"],
                "reference_task_exposure_samples": source["exposure_delta"][name],
                "planned_task_exposure_samples": added_steps * BATCH_SIZE,
                "rounding_error_samples": mismatch,
                "command": driver_command(
                    version=args.version,
                    run_id=run_id,
                    parent_id=args.parent_run_id,
                    parent_sha256=DEFAULT_PARENT_SHA256,
                    target_step=target_step,
                    task=task,
                    device=args.device,
                    description=(
                        f"same-implementation {name} specialist; per-task exposure and "
                        "ensemble-total-compute matched to v7.38 L0 Phase II"
                    ),
                ),
            }
        )
        sensitivity.append(
            {
                "task": name,
                "run_id": f"{args.run_prefix}_{name}_per_model_compute",
                "parent_run_id": run_id,
                "parent_checkpoint_sha256": "<read from completed primary contract>",
                "target_step": source["reference_step"],
                "total_added_steps_from_A30": source["reference_added_steps"],
                "formal_profile": task["profile"],
            }
        )
    return {
        "schema_version": 1,
        "status": "planned_not_started",
        "winner_source": "v7.38 L0 formal mainline",
        "v7_40_boundary": (
            "not eligible as specialist source until 30k, four-mode formal gate, complete "
            "checkpoint contract, and a hashable common initialization are available"
        ),
        "device": args.device,
        "source": source,
        "fixed_contract": {
            "stage1_and_owning_decoder_sha256": DEFAULT_STAGE1_SHA256,
            "train_cache_sha256": DEFAULT_TRAIN_CACHE_SHA256,
            "eval_cache_sha256": DEFAULT_EVAL_CACHE_SHA256,
            "z_norm_stats_sha256": DEFAULT_STATS_SHA256,
            "task_routing": "human_first",
            "human_condition": "human_text_only",
            "camera_condition": "observed_human_latent_plus_camera_text",
            "joint_condition": "parallel text_to_human_camera",
            "tracking": "train/100 plus fixed posthoc eval256/test256 at terminal snapshot",
            "formal_eval": "corresponding H/C/joint pure4053 DDIM50 CFG1 eta0 seed17",
            **code_hashes,
        },
        "primary_fairness": {
            "name": "per_task_exposure_and_ensemble_total_compute_matched",
            "definition": (
                "each one-hot specialist matches its L0 Phase-II task assignments after "
                "integer-step rounding; the three added-step counts sum exactly to 75000"
            ),
            "queue": primary,
            "estimated_wall_clock": "~9h40m train + ~30m formal eval = ~10h10m on one RTX 4090",
        },
        "optional_sensitivity": {
            "name": "per_model_update_matched_not_ensemble_compute_matched",
            "definition": (
                "each specialist receives all 75000 L0 Phase-II updates; the three-model "
                "ensemble therefore costs 3x the Unified continuation"
            ),
            "enabled": bool(args.include_per_model_sensitivity),
            "queue": sensitivity,
            "additional_wall_clock": "~19h20m train + ~30m formal eval",
        },
    }


def verify_files(plan: dict[str, Any]) -> dict[str, Any]:
    parent_checkpoint = run_root(plan["source"]["parent_id"]) / "train/last.pt"
    reference_checkpoint = run_root(plan["source"]["reference_id"]) / "train/last.pt"
    actual = {
        "parent_checkpoint_sha256": short.sha256_file(parent_checkpoint),
        "reference_checkpoint_sha256": short.sha256_file(reference_checkpoint),
        "train_cache_sha256": short.sha256_file(short.CACHE_DIR / "train.pt"),
        "eval_cache_sha256": short.sha256_file(short.CACHE_DIR / "val.pt"),
        "z_norm_stats_sha256": short.sha256_file(short.CANONICAL_STATS),
    }
    expected = {
        "parent_checkpoint_sha256": DEFAULT_PARENT_SHA256,
        "reference_checkpoint_sha256": DEFAULT_REFERENCE_SHA256,
        "train_cache_sha256": DEFAULT_TRAIN_CACHE_SHA256,
        "eval_cache_sha256": DEFAULT_EVAL_CACHE_SHA256,
        "z_norm_stats_sha256": DEFAULT_STATS_SHA256,
    }
    if actual != expected:
        raise RuntimeError(f"source file hash mismatch: actual={actual}, expected={expected}")
    target_ids = [item["run_id"] for item in plan["primary_fairness"]["queue"]]
    if plan["optional_sensitivity"]["enabled"]:
        target_ids.extend(item["run_id"] for item in plan["optional_sensitivity"]["queue"])
    collisions = [run_id for run_id in target_ids if run_root(run_id).exists()]
    if collisions:
        raise FileExistsError(f"refusing to reuse specialist run roots: {collisions}")
    return {"status": "passed", "verified_hashes": actual, "target_run_ids": target_ids}


def annotate_contract(
    item: dict[str, Any], plan: dict[str, Any], budget_name: str
) -> None:
    root = run_root(item["run_id"])
    contract_path = root / "experiment_contract.json"
    contract = read_json(contract_path)
    complete = read_json(root / "driver_complete.json")
    task = item["task"]
    contract["train"]["specialist"] = {
        "task": task,
        "same_implementation": True,
        "initialization_source_run": item["parent_run_id"],
        "initialization_checkpoint_sha256": item["parent_checkpoint_sha256"],
        "reference_unified_run": plan["source"]["reference_id"],
        "budget_basis": budget_name,
        "task_probs": contract["train"]["task_probs"],
        "actual_exposure_delta": complete["exposure_delta"],
        "trainer_sha256": plan["fixed_contract"]["trainer_sha256"],
        "evaluator_sha256": plan["fixed_contract"]["evaluator_sha256"],
    }
    if budget_name == "per_task_exposure_and_ensemble_total_compute_matched":
        contract["train"]["specialist"].update(
            {
                "reference_task_exposure_samples": item["reference_task_exposure_samples"],
                "planned_task_exposure_samples": item["planned_task_exposure_samples"],
                "rounding_error_samples": item["rounding_error_samples"],
            }
        )
    short.write_json(contract_path, contract)
    subprocess.run(
        [sys.executable, str(HARNESS), "audit-contract", str(contract_path)],
        cwd=ROOT,
        check=True,
    )


def execute(plan: dict[str, Any], args: argparse.Namespace) -> None:
    for item in plan["primary_fairness"]["queue"]:
        subprocess.run(item["command"], cwd=ROOT, check=True)
        annotate_contract(
            item, plan, "per_task_exposure_and_ensemble_total_compute_matched"
        )
    if not plan["optional_sensitivity"]["enabled"]:
        return
    task_by_name = {task["name"]: task for task in TASKS}
    primary_by_task = {
        item["task"]: item for item in plan["primary_fairness"]["queue"]
    }
    for item in plan["optional_sensitivity"]["queue"]:
        primary = primary_by_task[item["task"]]
        parent_contract = read_json(run_root(primary["run_id"]) / "experiment_contract.json")
        parent_sha = parent_contract["train"]["checkpoint_sha256"]
        item["parent_checkpoint_sha256"] = parent_sha
        item["command"] = driver_command(
            version=args.version,
            run_id=item["run_id"],
            parent_id=primary["run_id"],
            parent_sha256=parent_sha,
            target_step=item["target_step"],
            task=task_by_name[item["task"]],
            device=args.device,
            description=(
                f"same-implementation {item['task']} specialist; per-model full L0 "
                "Phase-II update sensitivity (ensemble cost 3x)"
            ),
        )
        subprocess.run(item["command"], cwd=ROOT, check=True)
        annotate_contract(item, plan, "per_model_update_matched_not_ensemble_compute_matched")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["plan", "check", "run"])
    parser.add_argument("--parent-run-id", default=DEFAULT_PARENT)
    parser.add_argument("--reference-run-id", default=DEFAULT_REFERENCE)
    parser.add_argument("--run-prefix", default="v7_42_l0_sameimpl_specialist_seed17")
    parser.add_argument("--version", default="v7.42")
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--include-per-model-sensitivity", action="store_true")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Required with mode=run. This guard prevents an accidental GPU launch.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    plan = build_plan(args)
    if args.mode == "plan":
        print(json.dumps(plan, indent=2, sort_keys=True))
        return
    check = verify_files(plan)
    print(json.dumps(check, indent=2, sort_keys=True), flush=True)
    if args.mode == "check":
        return
    if not args.execute:
        raise RuntimeError("mode=run requires the explicit --execute guard")
    execute(plan, args)


if __name__ == "__main__":
    main()
