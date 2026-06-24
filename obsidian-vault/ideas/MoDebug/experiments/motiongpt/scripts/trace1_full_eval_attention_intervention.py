#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import subprocess
import sys
import time
from contextlib import contextmanager, nullcontext
from pathlib import Path
from typing import Any


SUPPORTED_FAMILIES = {"baseline", "ca", "sa"}
UNSUPPORTED_CFG_REASONS = {
    "cfg_ca": (
        "MotionGPT official text-to-motion path uses T5ForConditionalGeneration.generate "
        "without an unconditional/classifier-free branch. README --cfg is a config-file "
        "argument, not classifier-free guidance scale. There is no true uncond CA output "
        "to replace."
    ),
    "cfg_sa": (
        "MotionGPT official text-to-motion path uses T5ForConditionalGeneration.generate "
        "without paired conditional/unconditional batches. There is no true uncond decoder "
        "self-attention output to replace."
    ),
}


def run(cmd: list[str], cwd: str) -> str:
    try:
        return subprocess.run(
            cmd,
            cwd=cwd,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout.strip()
    except OSError:
        return ""


def sha256(path: str | Path | None) -> str | None:
    if not path:
        return None
    p = Path(path)
    if not p.is_file():
        return None
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_record(path: str | Path | None) -> dict[str, Any]:
    if not path:
        return {"path": "", "sha256": None}
    p = Path(path).expanduser().resolve()
    return {"path": str(p), "sha256": sha256(p)}


def seed_everything(seed: int) -> None:
    import numpy as np

    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
        import pytorch_lightning as pl

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        pl.seed_everything(seed, workers=True)
    except Exception:
        pass


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def parse_layers(value: str, mapping: list[dict[str, Any]], allow_multi_layer: bool) -> list[int]:
    max_layer = len(mapping) - 1
    if value == "all":
        layers = [int(item["layer_id"]) for item in mapping]
    else:
        layers = []
        for part in value.split(","):
            part = part.strip()
            if not part:
                continue
            layer_id = int(part)
            if layer_id < 0 or layer_id > max_layer:
                raise ValueError(f"Layer {layer_id} outside valid range 0..{max_layer}")
            layers.append(layer_id)
    if not allow_multi_layer and len(layers) != 1:
        raise ValueError("Formal Trace1 run expects exactly one layer; pass --allow_multi_layer to override.")
    return layers


def motiongpt_layer_map(model: Any, expected_layers: int | None) -> list[dict[str, Any]]:
    lm = model.lm.language_model
    decoder = getattr(lm, "decoder", None)
    blocks = getattr(decoder, "block", None)
    if blocks is None:
        raise RuntimeError("MotionGPT language model has no decoder.block stack to hook.")

    mapping: list[dict[str, Any]] = []
    for layer_id, block in enumerate(blocks):
        layer_modules = list(getattr(block, "layer", []))
        self_attn = None
        enc_dec_attn = None
        for sub_idx, submodule in enumerate(layer_modules):
            if hasattr(submodule, "SelfAttention"):
                self_attn = (sub_idx, submodule.SelfAttention)
            if hasattr(submodule, "EncDecAttention"):
                enc_dec_attn = (sub_idx, submodule.EncDecAttention)
        mapping.append(
            {
                "layer_id": layer_id,
                "module": f"lm.language_model.decoder.block.{layer_id}",
                "self_attention_module": (
                    f"lm.language_model.decoder.block.{layer_id}.layer.{self_attn[0]}.SelfAttention"
                    if self_attn
                    else None
                ),
                "cross_attention_module": (
                    f"lm.language_model.decoder.block.{layer_id}.layer.{enc_dec_attn[0]}.EncDecAttention"
                    if enc_dec_attn
                    else None
                ),
                "self_attention_class": self_attn[1].__class__.__name__ if self_attn else None,
                "cross_attention_class": enc_dec_attn[1].__class__.__name__ if enc_dec_attn else None,
                "has_self_attention": self_attn is not None,
                "has_cross_attention": enc_dec_attn is not None,
            }
        )

    if expected_layers is not None and len(mapping) != expected_layers:
        raise RuntimeError(f"Expected {expected_layers} MotionGPT decoder layers, found {len(mapping)}")
    return mapping


def modules_for_layers(model: Any, layer_ids: list[int]) -> dict[int, dict[str, Any]]:
    blocks = model.lm.language_model.decoder.block
    selected: dict[int, dict[str, Any]] = {}
    for layer_id in layer_ids:
        block = blocks[layer_id]
        layer_modules = list(block.layer)
        entry: dict[str, Any] = {}
        for submodule in layer_modules:
            if hasattr(submodule, "SelfAttention"):
                entry["sa"] = submodule.SelfAttention
            if hasattr(submodule, "EncDecAttention"):
                entry["ca"] = submodule.EncDecAttention
        selected[layer_id] = entry
    return selected


def scale_attention_output(output: Any, alpha: float) -> Any:
    if isinstance(output, tuple):
        items = list(output)
        if items:
            items[0] = items[0] * alpha
        return tuple(items)
    return output * alpha


@contextmanager
def scale_motiongpt_attention(model: Any, family: str, layer_ids: list[int], alpha: float):
    selected = modules_for_layers(model, layer_ids)
    patched: list[tuple[Any, Any]] = []
    call_counts = {str(layer_id): 0 for layer_id in layer_ids}
    key = "ca" if family == "ca" else "sa"

    for layer_id, modules in selected.items():
        module = modules.get(key)
        if module is None:
            raise RuntimeError(f"MotionGPT layer {layer_id} has no {family} module")
        old_forward = module.forward

        def make_forward(forward_fn: Any, lid: int):
            def forward_scaled(*args: Any, **kwargs: Any) -> Any:
                call_counts[str(lid)] += 1
                return scale_attention_output(forward_fn(*args, **kwargs), alpha)

            return forward_scaled

        module.forward = make_forward(old_forward, layer_id)
        patched.append((module, old_forward))

    try:
        yield {"call_counts": call_counts, "replacement_checks": []}
    finally:
        for module, old_forward in patched:
            module.forward = old_forward


def intervention_context(model: Any, family: str, layer_ids: list[int], alpha: float):
    if family == "baseline":
        return nullcontext({"call_counts": {}, "replacement_checks": []})
    if family in {"ca", "sa"}:
        return scale_motiongpt_attention(model, family, layer_ids, alpha)
    raise ValueError(f"Unsupported family: {family}")


def build_motiongpt(args: argparse.Namespace):
    import torch
    import pytorch_lightning as pl
    from omegaconf import OmegaConf
    from mGPT.callback import build_callbacks
    from mGPT.config import parse_args as parse_motiongpt_args
    from mGPT.data.build_data import build_data
    from mGPT.models.build_model import build_model
    from mGPT.utils.logger import create_logger
    from mGPT.utils.load_checkpoint import load_pretrained, load_pretrained_vae

    old_argv = sys.argv[:]
    try:
        sys.argv = [
            "trace1_full_eval_attention_intervention.py",
            "--cfg",
            args.cfg,
            "--nodebug",
        ]
        cfg = parse_motiongpt_args(phase="test")
    finally:
        sys.argv = old_argv

    cfg.FOLDER = args.out_dir
    cfg.TEST.FOLDER = args.out_dir
    cfg.DEVICE = [args.gpu_id]
    cfg.TEST.REPLICATION_TIMES = args.replication_times
    cfg.TEST.BATCH_SIZE = args.batch_size
    cfg.TRAIN.NUM_WORKERS = args.num_workers
    cfg.TEST.SAVE_PREDICTIONS = args.save_predictions
    if args.checkpoint:
        cfg.TEST.CHECKPOINTS = args.checkpoint
    if args.vae_checkpoint:
        cfg.TRAIN.PRETRAINED_VAE = args.vae_checkpoint

    pl.seed_everything(args.seed, workers=True)
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["CUDA_VISIBLE_DEVICES"] = str(args.gpu_id)

    logger = create_logger(cfg, phase="test")
    logger.info(OmegaConf.to_yaml(cfg))
    callbacks = build_callbacks(cfg, logger=logger, phase="test")
    datamodule = build_data(cfg)
    model = build_model(cfg, datamodule)
    if cfg.TRAIN.PRETRAINED_VAE:
        load_pretrained_vae(cfg, model, logger)
    if cfg.TEST.CHECKPOINTS:
        load_pretrained(cfg, model, logger, phase="test")
    else:
        raise RuntimeError("MotionGPT TEST.CHECKPOINTS is required for Trace1 evaluation.")

    trainer = pl.Trainer(
        benchmark=False,
        max_epochs=cfg.TRAIN.END_EPOCH,
        accelerator=cfg.ACCELERATOR,
        devices=list(range(len(cfg.DEVICE))),
        default_root_dir=cfg.FOLDER_EXP,
        reload_dataloaders_every_n_epochs=1,
        deterministic=False,
        detect_anomaly=False,
        enable_progress_bar=True,
        logger=None,
        callbacks=callbacks,
    )
    return cfg, logger, datamodule, model, trainer


def run_official_test(args: argparse.Namespace, cfg: Any, logger: Any, datamodule: Any, model: Any, trainer: Any) -> dict[str, Any]:
    import numpy as np

    metrics_by_rep: dict[str, list[Any]] = {}
    metrics_type = ", ".join(cfg.METRIC.TYPE)
    for rep_idx in range(args.replication_times):
        seed_everything(args.seed + rep_idx)
        logger.info(f"MoDebug Trace1 {args.family} replication {rep_idx}: {metrics_type}")
        metrics = trainer.test(model, datamodule=datamodule)[0]
        if "TM2TMetrics" in metrics_type and cfg.model.params.task == "t2m" and cfg.model.params.stage != "vae":
            logger.info(f"MoDebug Trace1 {args.family} multimodality replication {rep_idx}")
            datamodule.mm_mode(True)
            mm_metrics = trainer.test(model, datamodule=datamodule)[0]
            metrics.update(mm_metrics)
            datamodule.mm_mode(False)
        for key, item in metrics.items():
            value = item.item() if hasattr(item, "item") else item
            metrics_by_rep.setdefault(key, []).append(value)

    summary: dict[str, Any] = {}
    for key, values in metrics_by_rep.items():
        arr = np.asarray(values, dtype=float)
        summary[key] = {
            "values": values,
            "mean": float(arr.mean()) if arr.size else None,
            "std": float(arr.std()) if arr.size else None,
        }
    return summary


def unsupported_manifest(args: argparse.Namespace, started: float, reason: str) -> dict[str, Any]:
    repo_dir = Path(args.repo_dir).resolve()
    wrapper_script = Path(__file__).resolve()
    return {
        "trace": "Trace 1",
        "scope": "motiongpt_full_official_evaluator_attention_intervention",
        "paper_level_status": "unsupported_family_fail_fast",
        "baseline": "MotionGPT",
        "repo_dir": str(repo_dir),
        "git_head": run(["git", "rev-parse", "HEAD"], str(repo_dir)),
        "git_branch": run(["git", "branch", "--show-current"], str(repo_dir)),
        "git_status_short": run(["git", "status", "--short"], str(repo_dir)).splitlines(),
        "command": " ".join(sys.argv),
        "wrapper_script": file_record(wrapper_script),
        "command_script": file_record(os.environ.get("MODEBUG_COMMAND_SCRIPT", "")),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        "family": args.family,
        "layers": [],
        "alpha": None,
        "seed": args.seed,
        "replication_times": args.replication_times,
        "batch_size": args.batch_size,
        "cfg": args.cfg,
        "checkpoint_path": args.checkpoint,
        "checkpoint_sha256": sha256(Path(args.repo_dir) / args.checkpoint) if args.checkpoint else None,
        "supported_families": sorted(SUPPORTED_FAMILIES),
        "unsupported_reason": reason,
        "failures": [reason],
        "limitations": [
            "MotionGPT is a VQ motion-token + T5 encoder-decoder language-model baseline, not a diffusion CFG baseline.",
            "The 18-layer MotionCLR layer count is not supported. Layer mapping is read from the MotionGPT T5 decoder stack at runtime.",
        ],
        "elapsed_sec": time.time() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo_dir", default="/data/public/ripemangobox/Motion/MotionGPT")
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--family", required=True, choices=["baseline", "ca", "sa", "cfg_ca", "cfg_sa"])
    parser.add_argument("--layers", default="0")
    parser.add_argument("--allow_multi_layer", action="store_true")
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--cfg", default="configs/config_h3d_stage3.yaml")
    parser.add_argument("--checkpoint", default="")
    parser.add_argument("--vae_checkpoint", default="")
    parser.add_argument("--gpu_id", type=int, default=0)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--replication_times", type=int, default=1)
    parser.add_argument("--num_workers", type=int, default=4)
    parser.add_argument("--expected_layers", type=int, default=12)
    parser.add_argument("--save_predictions", action="store_true")
    parser.add_argument("--dry_run", action="store_true")
    args = parser.parse_args()

    started = time.time()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    repo_dir = Path(args.repo_dir).resolve()
    wrapper_script = Path(__file__).resolve()

    if args.family in UNSUPPORTED_CFG_REASONS:
        manifest = unsupported_manifest(args, started, UNSUPPORTED_CFG_REASONS[args.family])
        write_json(out_dir / "manifest.json", manifest)
        print(json.dumps({"manifest": str(out_dir / "manifest.json"), "failures": manifest["failures"]}, indent=2))
        raise SystemExit(2)

    if not args.dry_run and os.environ.get("MODEBUG_DS_APPROVED_EXECUTE") != "1":
        reason = (
            "Formal MotionGPT eval is blocked until DS approves this baseline-specific "
            "evaluator and MODEBUG_DS_APPROVED_EXECUTE=1 is set explicitly."
        )
        manifest = unsupported_manifest(args, started, reason)
        manifest["paper_level_status"] = "execution_not_ds_approved_fail_fast"
        manifest["failures"] = [reason]
        write_json(out_dir / "manifest.json", manifest)
        print(json.dumps({"manifest": str(out_dir / "manifest.json"), "failures": manifest["failures"]}, indent=2))
        raise SystemExit(2)

    os.chdir(repo_dir)
    sys.path.insert(0, str(repo_dir))

    cfg, _logger, datamodule, model, trainer = build_motiongpt(args)
    mapping = motiongpt_layer_map(model, args.expected_layers)
    layer_ids = [] if args.family == "baseline" else parse_layers(args.layers, mapping, args.allow_multi_layer)
    selected_mapping = [item for item in mapping if item["layer_id"] in layer_ids]
    write_json(out_dir / "layer_mapping.json", {"layers": mapping})

    failures: list[str] = []
    metrics: dict[str, Any] = {}
    hook_state = {"call_counts": {}, "replacement_checks": []}

    if args.dry_run:
        metrics = {"dry_run": {"repo_imported": True, "model_built": True, "official_test_skipped": True}}
    else:
        with intervention_context(model, args.family, layer_ids, args.alpha) as hook_state:
            metrics = run_official_test(args, cfg, _logger, datamodule, model, trainer)

        for layer_id in layer_ids:
            if hook_state["call_counts"].get(str(layer_id), 0) <= 0:
                failures.append(f"Layer {layer_id} hook was never called for family {args.family}")

    metrics_path = out_dir / "metrics_summary.json"
    write_json(metrics_path, metrics)

    cfg_path = repo_dir / args.cfg
    ckpt_path = repo_dir / (args.checkpoint or str(cfg.TEST.CHECKPOINTS))
    vae_path = repo_dir / (args.vae_checkpoint or str(cfg.TRAIN.PRETRAINED_VAE))
    manifest = {
        "trace": "Trace 1",
        "scope": "motiongpt_full_official_evaluator_attention_intervention",
        "paper_level_status": "dry_run_preflight" if args.dry_run else ("full_evaluator_metrics_computed" if not failures else "failed"),
        "baseline": "MotionGPT",
        "repo_dir": str(repo_dir),
        "git_head": run(["git", "rev-parse", "HEAD"], str(repo_dir)),
        "git_branch": run(["git", "branch", "--show-current"], str(repo_dir)),
        "git_status_short": run(["git", "status", "--short"], str(repo_dir)).splitlines(),
        "git_diff_stat": run(["git", "diff", "--stat"], str(repo_dir)).splitlines(),
        "command": " ".join(sys.argv),
        "wrapper_script": file_record(wrapper_script),
        "command_script": file_record(os.environ.get("MODEBUG_COMMAND_SCRIPT", "")),
        "deployed_from": os.environ.get("MODEBUG_DEPLOYED_FROM", ""),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        "family": args.family,
        "layers": layer_ids,
        "selected_layer_mapping": selected_mapping,
        "alpha": args.alpha if args.family in {"ca", "sa"} else None,
        "seed": args.seed,
        "replication_times": args.replication_times,
        "batch_size": args.batch_size,
        "num_workers": args.num_workers,
        "cfg": str(cfg_path),
        "cfg_sha256": sha256(cfg_path),
        "checkpoint_path": str(ckpt_path),
        "checkpoint_sha256": sha256(ckpt_path),
        "vae_checkpoint_path": str(vae_path),
        "vae_checkpoint_sha256": sha256(vae_path),
        "eval_protocol": {
            "official_entry_reference": "MotionGPT test.py Lightning Trainer.test",
            "task": str(cfg.model.params.task),
            "stage": str(cfg.model.params.stage),
            "metric_type": list(cfg.METRIC.TYPE),
            "mm_metrics": True,
            "dry_run": bool(args.dry_run),
            "cfg_families": "unsupported: no classifier-free/unconditional branch in official MotionGPT generation",
        },
        "layer_mapping_file": str(out_dir / "layer_mapping.json"),
        "metrics_summary_file": str(metrics_path),
        "metrics_summary_sha256": sha256(metrics_path),
        "metrics": metrics,
        "hook_call_counts": hook_state["call_counts"],
        "replacement_checks": hook_state["replacement_checks"],
        "supported_families": sorted(SUPPORTED_FAMILIES),
        "unsupported_families": UNSUPPORTED_CFG_REASONS,
        "limitations": [
            "MotionGPT layer ids refer to T5 decoder blocks, not MotionCLR CLRBlock layers.",
            "The deployed MotionGPT T5-base backbone has 12 decoder layers, so MotionCLR-style 18-layer accounting is not supported for this baseline.",
            "CA means T5 decoder EncDecAttention output scaling.",
            "SA means T5 decoder SelfAttention output scaling.",
            "cfg_ca and cfg_sa are intentionally fail-fast because MotionGPT has no official classifier-free guidance/unconditional branch.",
        ],
        "failures": failures,
        "elapsed_sec": time.time() - started,
    }
    manifest_path = out_dir / "manifest.json"
    write_json(manifest_path, manifest)

    if failures:
        print(json.dumps({"manifest": str(manifest_path), "failures": failures}, indent=2))
        raise SystemExit(2)
    print(json.dumps({"manifest": str(manifest_path), "metrics_summary": str(metrics_path)}, indent=2))


if __name__ == "__main__":
    main()
