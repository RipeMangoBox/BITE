#!/usr/bin/env python3
"""Add fixed held-out eval/test records to completed StoryMotion snapshots."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import torch
from torch.utils.data import DataLoader, Subset

import train_stage2_condmdi_pulp as base
from storymotion.experiment_invariants import assert_default_cache_meta
from storymotion.stage2.processes import build_stage2_process
from storymotion_run_layout import run_paths


ROOT = Path(__file__).resolve().parents[1]


def value(raw: dict[str, str], name: str, kind: type, default: Any = None) -> Any:
    text = raw.get(name)
    if text is None or text == "None":
        return default
    if kind is bool:
        return text == "True"
    return kind(text)


def list_value(raw: dict[str, str], name: str) -> list[Any]:
    return json.loads(raw[name])


def build_model(raw: dict[str, str], device: torch.device) -> torch.nn.Module:
    instruction_path = value(raw, "task_instruction_embeddings", Path)
    embeddings, _ = base.load_task_instruction_embeddings(instruction_path)
    model = base.TemporalObsUNet(
        value(raw, "width", int),
        tuple(int(item) for item in list_value(raw, "dim_mults")),
        value(raw, "cond_mask_prob", float),
        value(raw, "zero_final", bool),
        value(raw, "cond_mask_prob_cam", float),
        value(raw, "cond_mask_prob_hum", float),
        v72_text_role_router=value(raw, "v72_text_role_router", bool),
        v72_aux_text_scale=value(raw, "v72_aux_text_scale", float),
        v72_soft_source=value(raw, "v72_soft_source", bool),
        v72_trust_gate=value(raw, "v72_trust_gate", bool),
        v72_relation_surrogate=value(raw, "v72_relation_surrogate", bool),
        v72_gate_bias=value(raw, "v72_gate_bias", float),
        task_instruction_embeddings=embeddings,
        task_instruction_scale=value(raw, "task_instruction_scale", float),
        num_task_embeddings=max(3, len(list_value(raw, "task_probs"))),
    ).to(device)
    return model


def fixed_evaluate(
    model: torch.nn.Module,
    process: Any,
    loader: DataLoader,
    device: torch.device,
    raw: dict[str, str],
    split: str,
    seed: int,
) -> dict[str, float]:
    with torch.random.fork_rng(devices=[device.index]):
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        return base.evaluate(
            model,
            process,
            loader,
            device,
            max_batches=1,
            split=split,
            joint_loss_mode=raw["joint_loss_mode"],
            joint_human_branch_weight=value(raw, "joint_human_branch_weight", float),
            joint_camera_branch_weight=value(raw, "joint_camera_branch_weight", float),
            joint_loss_weight=value(raw, "joint_loss_weight", float),
            task_routing=raw["task_routing"],
            joint_human_camera_input_mode=raw["joint_human_camera_input_mode"],
            joint_coupling_scale=value(raw, "joint_coupling_scale", float),
            joint_coupling_mode=raw["joint_coupling_mode"],
            znorm_stats=None,
        )


def annotate_active_task_loss(
    metrics: dict[str, float], raw: dict[str, str]
) -> tuple[dict[str, float], list[str]]:
    task_probs = list_value(raw, "task_probs")
    active_tasks = [
        base.TASK_NAMES[task_id]
        for task_id, probability in enumerate(task_probs)
        if float(probability) > 0.0
    ]
    if not active_tasks:
        raise RuntimeError("task_probs has no active tasks")
    annotated = dict(metrics)
    annotated["loss_all_task_embeddings"] = float(metrics["loss"])
    annotated["loss_active_tasks"] = sum(
        float(metrics[f"{task_name}_loss"]) for task_name in active_tasks
    ) / len(active_tasks)
    return annotated, active_tasks


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--eval-seed", type=int, default=1017)
    parser.add_argument("--test-seed", type=int, default=2017)
    parser.add_argument("--allow-non-resume", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    paths = run_paths("stage2", args.run_id)
    train_root = paths["train"]
    meta = json.loads((train_root / "meta.json").read_text(encoding="utf-8"))
    raw = meta["args"]
    is_resume = value(raw, "resume", Path) is not None
    if not is_resume and not args.allow_non_resume:
        raise RuntimeError("snapshot audit requires a resume run")
    device = torch.device(args.device)
    base.set_seed(value(raw, "seed", int))
    stats_path = value(raw, "znorm_stats_path", Path)
    stats = base.load_latent_znorm_stats(stats_path)
    cache_dir = value(raw, "cache_dir", Path)
    heldout = base.PulpLatentCache(cache_dir / "val.pt", znorm_stats=stats)
    assert_default_cache_meta(heldout.meta)
    eval_count = min(256, len(heldout))
    test_count = min(256, len(heldout) - eval_count)
    if eval_count != 256 or test_count != 256:
        raise RuntimeError(f"expected disjoint 256/256 held-out subsets, got {eval_count}/{test_count}")
    eval_loader = DataLoader(Subset(heldout, range(eval_count)), batch_size=eval_count, shuffle=False)
    test_loader = DataLoader(
        Subset(heldout, range(eval_count, eval_count + test_count)),
        batch_size=test_count,
        shuffle=False,
    )
    model = build_model(raw, device)
    process = build_stage2_process(
        raw["generative_process"],
        value(raw, "diffusion_steps", int),
        raw["noise_schedule"],
        device,
        raw["diffusion_prediction_type"],
    )

    output_dir = paths["eval"] / "posthoc_tracking"
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "eval_test.jsonl"
    existing_steps: set[int] = set()
    if log_path.is_file() and not args.overwrite:
        existing_steps = {
            int(json.loads(line)["step"])
            for line in log_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
    if args.overwrite:
        log_path.unlink(missing_ok=True)
    writer = base.SummaryWriter(str(output_dir / "tensorboard"))
    rows: list[dict[str, Any]] = []
    checkpoints = sorted(
        train_root.glob("step_*.pt"), key=lambda path: int(path.stem.removeprefix("step_"))
    )
    for checkpoint_path in checkpoints:
        step = int(checkpoint_path.stem.removeprefix("step_"))
        if step in existing_steps:
            continue
        checkpoint = torch.load(checkpoint_path, map_location="cpu")
        checkpoint_step = int(checkpoint.get("step", -1))
        if checkpoint_step != step:
            raise RuntimeError(f"checkpoint step mismatch: {checkpoint_path} contains {checkpoint_step}")
        state = checkpoint["raw_model"] if "raw_model" in checkpoint else checkpoint["model"]
        model.load_state_dict(state, strict=not value(raw, "v72_relation_surrogate", bool))
        del checkpoint, state
        model.to(device).eval()
        eval_metrics, active_tasks = annotate_active_task_loss(
            fixed_evaluate(model, process, eval_loader, device, raw, "eval", args.eval_seed),
            raw,
        )
        test_metrics, test_active_tasks = annotate_active_task_loss(
            fixed_evaluate(model, process, test_loader, device, raw, "test", args.test_seed),
            raw,
        )
        if test_active_tasks != active_tasks:
            raise RuntimeError("eval/test active task sets differ")
        row = {
            "run_id": args.run_id,
            "step": step,
            "checkpoint": str(checkpoint_path.relative_to(ROOT)),
            "checkpoint_sha256": base.sha256_file(checkpoint_path),
            "eval_seed": args.eval_seed,
            "test_seed": args.test_seed,
            "eval_samples": eval_count,
            "test_samples": test_count,
            "eval_sample_ids_sha256": base.sha256_sample_ids(
                [str(item) for item in heldout.sample_id[:eval_count]]
            ),
            "test_sample_ids_sha256": base.sha256_sample_ids(
                [str(item) for item in heldout.sample_id[eval_count : eval_count + test_count]]
            ),
            "active_tasks": active_tasks,
            "eval": eval_metrics,
            "test": test_metrics,
        }
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
        base.write_scalars(writer, "eval", eval_metrics, step)
        base.write_scalars(writer, "test", test_metrics, step)
        writer.flush()
        rows.append(row)
        print(
            json.dumps(
                {
                    "run_id": args.run_id,
                    "step": step,
                    "active_tasks": active_tasks,
                    "eval_loss_active_tasks": eval_metrics["loss_active_tasks"],
                    "test_loss_active_tasks": test_metrics["loss_active_tasks"],
                }
            ),
            flush=True,
        )

    all_rows = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    best = min(all_rows, key=lambda row: float(row["eval"]["loss_active_tasks"]))
    summary = {
        "schema_version": 2,
        "kind": "fixed_posthoc_snapshot_tracking",
        "run_id": args.run_id,
        "historical_gap": (
            "periodic eval/test was disabled during resume training; these are posthoc snapshot diagnostics"
            if is_resume
            else "periodic eval/test was disabled during training; only saved snapshots can be diagnosed posthoc"
        ),
        "selection_metric": "eval.loss_active_tasks",
        "selection_boundary": "teacher-forced latent loss over trained task embeddings only monitors stability and overfit; formal checkpoint promotion remains pure4053 decoded evaluation",
        "fixed_eval_seed": args.eval_seed,
        "fixed_test_seed": args.test_seed,
        "eval_samples": eval_count,
        "test_samples": test_count,
        "snapshot_steps": [int(row["step"]) for row in all_rows],
        "best_eval": best,
        "tensorboard": str((output_dir / "tensorboard").relative_to(ROOT)),
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    writer.close()
    print(json.dumps({"output": str(output_dir), "new_rows": len(rows), "best_step": best["step"]}, sort_keys=True))


if __name__ == "__main__":
    main()
