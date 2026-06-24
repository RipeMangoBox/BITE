#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import random
import subprocess
import sys
import time
from pathlib import Path

UNSUPPORTED_CA_MESSAGE = (
    "MotionStreamer has no cross-attention module on the official T2M path. "
    "Trace1 ca/cfg_ca are schema-incompatible and must not be reported as "
    "MotionCLR-style CA diagnostics."
)


def sha256(path: str | Path) -> str | None:
    p = Path(path)
    if not p.is_file():
        return None
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_record(path: str | Path) -> dict:
    p = Path(path).expanduser()
    return {"path": str(p.resolve()), "sha256": sha256(p)}


def run_text(cmd: list[str], cwd: Path) -> str:
    if not cwd.is_dir():
        return ""
    try:
        return subprocess.run(
            cmd, cwd=str(cwd), text=True, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).stdout.strip()
    except OSError:
        return ""


def prerequisite_records(args) -> dict:
    repo_dir = Path(args.repo_dir).expanduser()
    records = {
        "repo_dir": {"path": str(repo_dir), "ok": repo_dir.is_dir()},
        "official_eval_t2m": {"path": str(repo_dir / "eval_t2m.py"), "ok": (repo_dir / "eval_t2m.py").is_file()},
        "llama_model": {
            "path": str(repo_dir / "models" / "llama_model.py"),
            "ok": (repo_dir / "models" / "llama_model.py").is_file(),
        },
        "official_eval_trans": {
            "path": str(repo_dir / "utils" / "eval_trans.py"),
            "ok": (repo_dir / "utils" / "eval_trans.py").is_file(),
        },
        "dataset_eval_t2m": {
            "path": str(repo_dir / "humanml3d_272" / "dataset_eval_t2m.py"),
            "ok": (repo_dir / "humanml3d_272" / "dataset_eval_t2m.py").is_file(),
        },
        "sentence_t5": {"path": str(repo_dir / "sentencet5-xxl"), "ok": (repo_dir / "sentencet5-xxl").is_dir()},
        "evaluator_checkpoint": {
            "path": str(repo_dir / "Evaluator_272" / "epoch=99.ckpt"),
            "ok": (repo_dir / "Evaluator_272" / "epoch=99.ckpt").is_file(),
        },
        "tae_checkpoint": {"path": str(Path(args.resume_pth)), "ok": Path(args.resume_pth).is_file()},
        "transformer_checkpoint": {"path": str(Path(args.resume_trans)), "ok": Path(args.resume_trans).is_file()},
    }
    records["blocking"] = [name for name, record in records.items() if isinstance(record, dict) and not record["ok"]]
    return records


def parse_layers(value: str, num_layers: int, allow_multi_layer: bool) -> list[int]:
    if value == "all":
        layers = list(range(num_layers))
    else:
        layers = []
        for part in value.split(","):
            part = part.strip()
            if part:
                layers.append(int(part))
    for layer in layers:
        if layer < 0 or layer >= num_layers:
            raise ValueError(f"Layer {layer} outside valid range 0..{num_layers - 1}")
    if not allow_multi_layer and len(layers) != 1:
        raise ValueError("Formal layer sweep requires exactly one layer; pass --allow_multi_layer for controls.")
    return layers


def seed_everything(seed: int) -> None:
    import numpy as np
    import torch

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def require_file(path: Path, label: str) -> None:
    if not path.is_file():
        raise RuntimeError(f"Missing {label}: {path}")


def require_dir(path: Path, label: str) -> None:
    if not path.is_dir():
        raise RuntimeError(f"Missing {label}: {path}")


def layer_map(trans_encoder) -> list[dict]:
    layers = []
    for i, block in enumerate(trans_encoder.transformer.h):
        attn = getattr(block, "attn", None)
        layers.append(
            {
                "layer_id": i,
                "module": f"transformer.h.{i}",
                "self_attention_module": f"transformer.h.{i}.attn",
                "block_class": block.__class__.__name__,
                "self_attention_class": attn.__class__.__name__ if attn is not None else None,
                "attention_type": "causal_self_attention",
                "has_cross_attention": False,
            }
        )
    return layers


@contextlib.contextmanager
def scale_self_attention_outputs(trans_encoder, layer_ids: list[int], alpha: float):
    patched = []
    call_counts = {str(layer): 0 for layer in layer_ids}
    replacement_checks: list[dict] = []
    for layer in layer_ids:
        attn = trans_encoder.transformer.h[layer].attn
        old_forward = attn.forward

        def make_forward(forward_fn, lid):
            def forward_scaled(*args, **kwargs):
                out = forward_fn(*args, **kwargs)
                call_counts[str(lid)] += 1
                if isinstance(out, tuple):
                    y = out[0] * alpha
                    return (y, *out[1:])
                return out * alpha

            return forward_scaled

        attn.forward = make_forward(old_forward, layer)
        patched.append((attn, old_forward))
    try:
        yield {"call_counts": call_counts, "replacement_checks": replacement_checks}
    finally:
        for module, old_forward in patched:
            module.forward = old_forward


@contextlib.contextmanager
def replace_block_output_cond_with_uncond(trans_encoder, layer_ids: list[int]):
    patched = []
    call_counts = {str(layer): 0 for layer in layer_ids}
    replacement_checks: list[dict] = []
    for layer in layer_ids:
        block = trans_encoder.transformer.h[layer]
        old_forward = block.forward
        cache: dict[tuple[int, str], object] = {}

        def make_forward(forward_fn, lid):
            def forward_replaced(x, *args, **kwargs):
                y = forward_fn(x, *args, **kwargs)
                tensor = y[0] if isinstance(y, tuple) else y
                call_counts[str(lid)] += 1

                seq_len = int(tensor.shape[1])
                key = (seq_len, str(tensor.device))
                is_uncond = bool(getattr(trans_encoder, "_modebug_cfg_uncond_pass", False))
                if is_uncond:
                    cache[key] = tensor.detach()
                    return y

                if key not in cache:
                    raise RuntimeError(
                        f"CFG_SA layer {lid} missing cached uncond block output for sequence length {seq_len}"
                    )
                uncond = cache.pop(key)
                before = (tensor - uncond).detach().abs().max().item()
                new_tensor = uncond.to(device=tensor.device, dtype=tensor.dtype).clone()
                after = (new_tensor - uncond.to(device=tensor.device, dtype=tensor.dtype)).detach().abs().max().item()
                replacement_checks.append(
                    {
                        "layer_id": lid,
                        "shape": list(tensor.shape),
                        "sequence_length": seq_len,
                        "max_abs_cond_vs_uncond_before": before,
                        "max_abs_cond_vs_uncond_after": after,
                        "definition": "conditional post-block hidden is replaced by same-prefix empty-text post-block hidden",
                    }
                )
                if isinstance(y, tuple):
                    return (new_tensor, *y[1:])
                return new_tensor

            return forward_replaced

        block.forward = make_forward(old_forward, layer)
        patched.append((block, old_forward))
    try:
        yield {"call_counts": call_counts, "replacement_checks": replacement_checks}
    finally:
        for module, old_forward in patched:
            module.forward = old_forward
        if hasattr(trans_encoder, "_modebug_cfg_uncond_pass"):
            delattr(trans_encoder, "_modebug_cfg_uncond_pass")


def intervention_context(trans_encoder, family: str, layer_ids: list[int], alpha: float):
    if family == "baseline":
        return contextlib.nullcontext({"call_counts": {}, "replacement_checks": []})
    if family == "sa":
        return scale_self_attention_outputs(trans_encoder, layer_ids, alpha)
    if family == "cfg_sa":
        return replace_block_output_cond_with_uncond(trans_encoder, layer_ids)
    raise ValueError(UNSUPPORTED_CA_MESSAGE)


def patch_cfg_sampling(trans_encoder):
    import torch

    def sample_for_eval_cfg_modebug(text, length=196, tokenize_model=None, device=torch.device("cuda"), unit_length=4, cfg=4.0):
        max_token_len = length // unit_length
        for k in range(max_token_len):
            x = [] if k == 0 else xs
            empty_feat_text = torch.from_numpy(tokenize_model.encode("")).float().unsqueeze(0).to(device)
            trans_encoder._modebug_cfg_uncond_pass = True
            empty_conditions = trans_encoder.forward(x, empty_feat_text)[:, -1, :]

            feat_text = torch.from_numpy(tokenize_model.encode(text)).float().to(device)
            trans_encoder._modebug_cfg_uncond_pass = False
            conditions = trans_encoder.forward(x, feat_text)[:, -1, :]

            if cfg != 1:
                mix_conditions = torch.cat([conditions, empty_conditions], dim=0)
                sampled_token_latent = trans_encoder.diff_loss.sample(mix_conditions, temperature=1.0, cfg=cfg)
                scaled_logits, _ = sampled_token_latent.chunk(2, dim=0)
            else:
                scaled_logits = trans_encoder.diff_loss.sample(conditions, temperature=1.0, cfg=1)

            scaled_logits = scaled_logits.unsqueeze(0)
            xs = scaled_logits if k == 0 else torch.cat((xs, scaled_logits), dim=1)
        return xs

    trans_encoder.sample_for_eval_CFG = sample_for_eval_cfg_modebug


def parse_metrics_from_log(log_path: Path) -> dict:
    if not log_path.is_file():
        return {}
    metrics = {}
    text = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    for line in text:
        if "Eval. :" not in line:
            continue
        metrics["raw_eval_line"] = line.strip()
    for line in text:
        stripped = line.strip()
        for key, out_key in [
            ("fid:", "fid"),
            ("div:", "diversity"),
            ("top1:", "r_precision_top1"),
            ("top2:", "r_precision_top2"),
            ("top3:", "r_precision_top3"),
            ("MM-dist (matching score) :", "matching_score"),
        ]:
            if stripped.startswith(key):
                metrics[out_key] = stripped.split(":", 1)[1].strip()
    return metrics


def write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def build_manifest(args, mapping: list[dict], layer_ids: list[int], started: float, status: str, hook_state=None, metrics=None, error=None) -> dict:
    repo_dir = Path(args.repo_dir)
    command_script = os.environ.get("MODEBUG_COMMAND_SCRIPT", "")
    manifest = {
        "baseline": "MotionStreamer",
        "status": status,
        "family": args.family,
        "layers": layer_ids,
        "architecture": {
            "text_conditioning": "sentence-t5 embedding prepended as a causal transformer token",
            "attention_path": "causal self-attention only",
            "num_trace_layers": len(mapping),
            "ca_supported": False,
            "cfg_ca_supported": False,
            "sa_supported": True,
            "cfg_sa_supported": True,
            "cfg_sa_definition": "same-prefix empty-text branch post-block hidden replacement",
        },
        "official_protocol": {
            "entrypoint_reference": "eval_t2m.py",
            "metrics_function": "utils.eval_trans.evaluation_transformer_272_single",
            "cfg_scale": args.cfg_scale,
            "unit_length": args.unit_length,
            "dataset": args.dataname,
        },
        "provenance": {
            "repo_dir": str(repo_dir.resolve()),
            "repo_head": run_text(["git", "rev-parse", "HEAD"], repo_dir),
            "repo_branch": run_text(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo_dir),
            "wrapper_script": file_record(Path(__file__)),
            "command_script": file_record(command_script) if command_script else None,
            "tae_checkpoint": file_record(args.resume_pth),
            "transformer_checkpoint": file_record(args.resume_trans),
            "evaluator_checkpoint": file_record(repo_dir / "Evaluator_272" / "epoch=99.ckpt"),
        },
        "args": vars(args),
        "prerequisites": prerequisite_records(args),
        "elapsed_sec": time.time() - started,
        "hook_state": hook_state or {"call_counts": {}, "replacement_checks": []},
        "metrics": metrics or {},
        "error": error,
    }
    return manifest


def run_eval(args, mapping: list[dict], layer_ids: list[int]) -> tuple[dict, dict]:
    import torch
    from torch.utils.tensorboard import SummaryWriter

    repo_dir = Path(args.repo_dir).resolve()
    os.chdir(repo_dir)
    sys.path.insert(0, str(repo_dir))
    sys.path.insert(0, str(repo_dir / "Evaluator_272"))

    from humanml3d_272 import dataset_eval_t2m
    from mld.models.architectures.temos.motionencoder.actor import ActorAgnosticEncoder
    from mld.models.architectures.temos.textencoder.distillbert_actor import DistilbertActorAgnosticEncoder
    from models.llama_model import LLaMAHF, LLaMAHFConfig
    import models.tae as tae
    from sentence_transformers import SentenceTransformer
    import utils.eval_trans as eval_trans
    import utils.utils_model as utils_model

    device = torch.device(f"cuda:{args.gpu_id}" if torch.cuda.is_available() else "cpu")
    if torch.cuda.is_available():
        torch.cuda.set_device(device)
    seed_everything(args.seed)

    out_dir = Path(args.out_dir).resolve()
    run_log_dir = out_dir / "official_eval_log"
    run_log_dir.mkdir(parents=True, exist_ok=True)
    logger = utils_model.get_logger(str(run_log_dir))
    writer = SummaryWriter(str(run_log_dir))

    val_loader = dataset_eval_t2m.DATALoader(args.dataname, True, args.eval_batch_size)

    t5_model = SentenceTransformer(str(repo_dir / "sentencet5-xxl"))
    t5_model.eval()
    for p in t5_model.parameters():
        p.requires_grad = False

    net = tae.Causal_HumanTAE(
        hidden_size=args.hidden_size,
        down_t=args.down_t,
        stride_t=args.stride_t,
        depth=args.depth,
        dilation_growth_rate=args.dilation_growth_rate,
        activation="relu",
        latent_dim=args.latent_dim,
        clip_range=[-30, 20],
    )
    ckpt = torch.load(args.resume_pth, map_location="cpu")
    net.load_state_dict(ckpt["net"], strict=True)
    net.eval().to(device)

    config = LLaMAHFConfig.from_name("Normal_size")
    config.block_size = args.block_size
    trans_encoder = LLaMAHF(config, args.num_diffusion_head_layers, args.latent_dim, device)
    ckpt = torch.load(args.resume_trans, map_location="cpu")
    new_ckpt_trans = {}
    for key, value in ckpt["trans"].items():
        new_key = ".".join(key.split(".")[1:]) if key.split(".")[0] == "module" else key
        new_ckpt_trans[new_key] = value
    trans_encoder.load_state_dict(new_ckpt_trans, strict=True)
    trans_encoder.eval().to(device)
    actual_mapping = layer_map(trans_encoder)
    if len(actual_mapping) != len(mapping):
        raise RuntimeError(f"Expected {len(mapping)} MotionStreamer causal self-attention layers, found {len(actual_mapping)}")

    textencoder = DistilbertActorAgnosticEncoder("distilbert-base-uncased", num_layers=4, latent_dim=256)
    motionencoder = ActorAgnosticEncoder(nfeats=272, vae=True, num_layers=4, latent_dim=256, max_len=300)
    evaluator_ckpt = torch.load(repo_dir / "Evaluator_272" / "epoch=99.ckpt", map_location="cpu")
    textencoder.load_state_dict(
        {k.replace("textencoder.", ""): v for k, v in evaluator_ckpt["state_dict"].items() if k.startswith("textencoder.")},
        strict=True,
    )
    motionencoder.load_state_dict(
        {k.replace("motionencoder.", ""): v for k, v in evaluator_ckpt["state_dict"].items() if k.startswith("motionencoder.")},
        strict=True,
    )
    textencoder.eval().to(device)
    motionencoder.eval().to(device)

    if args.family == "cfg_sa":
        patch_cfg_sampling(trans_encoder)

    with intervention_context(trans_encoder, args.family, layer_ids, args.alpha) as hook_state:
        fid, div, top1, top2, top3, matching, logger = eval_trans.evaluation_transformer_272_single(
            val_loader,
            net,
            trans_encoder,
            t5_model,
            logger,
            [textencoder, motionencoder],
            args.cfg_scale,
            device=device,
            unit_length=args.unit_length,
        )

    metrics = {
        "fid": float(fid),
        "diversity": float(div),
        "r_precision_top1": float(top1),
        "r_precision_top2": float(top2),
        "r_precision_top3": float(top3),
        "matching_score": float(matching),
        "log_parse": parse_metrics_from_log(run_log_dir / "log.txt"),
    }
    writer.close()
    return hook_state, metrics


def main() -> int:
    parser = argparse.ArgumentParser(description="MoDebug MotionStreamer Trace1 causal-self-attention evaluator")
    parser.add_argument("--repo_dir", default="/data/public/ripemangobox/Motion/MotionStreamer")
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--family", required=True, choices=["baseline", "ca", "cfg_ca", "sa", "cfg_sa"])
    parser.add_argument("--layers", default="0")
    parser.add_argument("--allow_multi_layer", action="store_true")
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--cfg_scale", type=float, default=4.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--gpu_id", type=int, default=0)
    parser.add_argument("--dataname", default="t2m_272")
    parser.add_argument("--eval_batch_size", type=int, default=32)
    parser.add_argument("--unit_length", type=int, default=4)
    parser.add_argument("--block_size", type=int, default=78)
    parser.add_argument("--hidden_size", type=int, default=1024)
    parser.add_argument("--down-t", dest="down_t", type=int, default=2)
    parser.add_argument("--stride-t", dest="stride_t", type=int, default=2)
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--dilation-growth-rate", dest="dilation_growth_rate", type=int, default=3)
    parser.add_argument("--num_diffusion_head_layers", type=int, default=9)
    parser.add_argument("--latent_dim", type=int, default=16)
    parser.add_argument("--resume-pth", dest="resume_pth", default="/data/public/ripemangobox/Motion/MotionStreamer/Causal_TAE/net_last.pth")
    parser.add_argument(
        "--resume-trans",
        dest="resume_trans",
        default="/cpfs03/shared/IDC/wangjingbo_group/motionstreamer/Open_source_Train_AR_16_1024_fps_30_111M_9/latest.pth",
    )
    parser.add_argument("--execute", action="store_true", help="Run official eval. Omit for DS-review dry run only.")
    args = parser.parse_args()

    started = time.time()
    repo_dir = Path(args.repo_dir).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.family in {"ca", "cfg_ca"}:
        manifest = build_manifest(args, [], [], started, "blocked_schema_incompatible", error=UNSUPPORTED_CA_MESSAGE)
        write_json(out_dir / "manifest.json", manifest)
        print(UNSUPPORTED_CA_MESSAGE, file=sys.stderr)
        return 2

    mapping = [
        {
            "layer_id": i,
            "module": f"transformer.h.{i}",
            "self_attention_module": f"transformer.h.{i}.attn",
            "block_class": "Block",
            "self_attention_class": "CausalSelfAttention",
            "attention_type": "causal_self_attention",
            "has_cross_attention": False,
        }
        for i in range(12)
    ]
    layer_ids = [] if args.family == "baseline" else parse_layers(args.layers, len(mapping), args.allow_multi_layer)
    write_json(out_dir / "layer_mapping.json", mapping)

    if args.execute and os.environ.get("MODEBUG_DS_APPROVED_EXECUTE") != "1":
        reason = (
            "Formal MotionStreamer eval is blocked until DS approves this baseline-specific "
            "evaluator and MODEBUG_DS_APPROVED_EXECUTE=1 is set explicitly."
        )
        manifest = build_manifest(args, mapping, layer_ids, started, "execution_not_ds_approved_fail_fast", error=reason)
        write_json(out_dir / "manifest.json", manifest)
        print(reason, file=sys.stderr)
        return 2

    require_dir(repo_dir, "MotionStreamer repo")
    require_file(repo_dir / "eval_t2m.py", "official eval_t2m.py")
    require_file(repo_dir / "models" / "llama_model.py", "MotionStreamer llama_model.py")
    require_file(repo_dir / "utils" / "eval_trans.py", "official eval_trans.py")
    require_file(repo_dir / "Evaluator_272" / "epoch=99.ckpt", "272D evaluator checkpoint")
    require_dir(repo_dir / "sentencet5-xxl", "local sentence-t5 model")

    if not args.execute:
        prerequisites = prerequisite_records(args)
        status = "dry_run_ready" if not prerequisites["blocking"] else "dry_run_blocked"
        manifest = build_manifest(args, mapping, layer_ids, started, status)
        write_json(out_dir / "manifest.json", manifest)
        print(
            json.dumps(
                {
                    "status": status,
                    "family": args.family,
                    "layers": layer_ids,
                    "num_layers": len(mapping),
                    "blocking": prerequisites["blocking"],
                },
                indent=2,
            )
        )
        return 0

    require_file(Path(args.resume_pth), "Causal TAE checkpoint")
    require_file(Path(args.resume_trans), "MotionStreamer transformer checkpoint")
    require_file(repo_dir / "humanml3d_272" / "dataset_eval_t2m.py", "humanml3d_272 dataset_eval_t2m.py")

    hook_state: dict | None = None
    metrics: dict | None = None
    try:
        hook_state, metrics = run_eval(args, mapping, layer_ids)
        status = "completed"
        error = None
    except Exception as exc:
        status = "failed"
        error = repr(exc)
    manifest = build_manifest(args, mapping, layer_ids, started, status, hook_state=hook_state, metrics=metrics, error=error)
    write_json(out_dir / "manifest.json", manifest)
    write_json(out_dir / "metrics_summary.json", metrics or {})
    if status != "completed":
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
