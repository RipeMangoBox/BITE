#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import random
import subprocess
import sys
import time
from collections import OrderedDict
from contextlib import contextmanager
from os.path import join as pjoin

import numpy as np
import torch


DEFAULT_BLOCKS = {
    "motionclr": [
        {"block": "early", "layers": [0, 1, 2, 3, 4, 5], "endpoint_layer": 5},
        {"block": "middle_sensitive", "layers": [6, 7, 8, 9, 10, 11, 12, 13, 14, 15], "endpoint_layer": 15},
        {"block": "late", "layers": [16, 17], "endpoint_layer": 17},
    ],
    "motiongpt": [
        {"block": "early", "layers": [0, 1, 2, 3], "endpoint_layer": 3},
        {"block": "middle", "layers": [4, 5, 6, 7], "endpoint_layer": 7},
        {"block": "late", "layers": [8, 9, 10, 11], "endpoint_layer": 11},
    ],
    "molingo": [
        {"block": "early", "layers": [0, 1, 2, 3, 4], "endpoint_layer": 4},
        {"block": "middle", "layers": [5, 6, 7, 8, 9, 10], "endpoint_layer": 10},
        {"block": "late", "layers": [11, 12, 13, 14, 15], "endpoint_layer": 15},
    ],
}


def now() -> str:
    import datetime as dt

    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def run(cmd: list[str], cwd: str) -> str:
    try:
        return subprocess.check_output(cmd, cwd=cwd, text=True, stderr=subprocess.STDOUT).strip()
    except Exception as exc:
        return f"ERROR: {exc}"


def sha256(path: str) -> str | None:
    if not path or not os.path.isfile(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: str, payload: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def blocked_manifest(args: argparse.Namespace, baseline: str, reason: str, extra: dict | None = None) -> dict:
    repo_dir = getattr(args, f"{baseline}_repo")
    payload = {
        "trace": "LDO/DSO",
        "scope": "layer_direct_output_audit",
        "paper_level_status": "blocked_incompatible_interface",
        "baseline": baseline,
        "diagnostic": "LDO",
        "created_at": now(),
        "repo_dir": repo_dir,
        "repo_status": {
            "head": run(["git", "rev-parse", "HEAD"], repo_dir) if os.path.isdir(repo_dir) else "missing_repo",
            "branch": run(["git", "branch", "--show-current"], repo_dir) if os.path.isdir(repo_dir) else "missing_repo",
            "status_short": run(["git", "status", "--short"], repo_dir).splitlines() if os.path.isdir(repo_dir) else ["missing_repo"],
        },
        "block_plan": DEFAULT_BLOCKS[baseline],
        "reason": reason,
        "failures": [reason],
        "limitations": [
            "LDO requires layer output to be legally decodable into motion before computing official metrics.",
            "This manifest intentionally blocks metric computation rather than treating arbitrary hidden states as motion outputs.",
        ],
    }
    if extra:
        payload.update(extra)
    return payload


def fixseed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def load_vae_model(vae_opt, ckpt_path, dim_pose, device):
    from mogen.models.vae.vae import VAE

    vae_model = VAE(
        input_width=dim_pose,
        output_emb_width=vae_opt.output_emb_width,
        down_t=vae_opt.down_t,
        stride_t=vae_opt.stride_t,
        width=vae_opt.width,
        depth=vae_opt.depth,
        dilation_growth_rate=vae_opt.dilation_growth_rate,
        activation=vae_opt.activation,
        norm=vae_opt.norm,
        pad_mode=vae_opt.pad_mode,
        ae=vae_opt.ae,
    )
    vae_model.to(device)
    state_dict = torch.load(ckpt_path, map_location="cpu")["state_dict"]
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        new_state_dict[k[len("module.") :] if k.startswith("module.") else k] = v
    vae_model.load_state_dict(state_dict=new_state_dict)
    vae_model.eval()
    for param in vae_model.parameters():
        param.requires_grad = False
    return vae_model


def resolve_mean_std_paths(data_root: str, dim_pose: int):
    if dim_pose == 272:
        candidate_dirs = [
            pjoin(data_root, "HumanML3D_272", "mean_std"),
            pjoin(data_root, "272-dim-HumanML3D", "mean_std"),
            pjoin(data_root, "mean_std"),
            pjoin(data_root, "HumanML3D-E-MP", "motion_format_stats", "hml272"),
        ]
    else:
        candidate_dirs = [pjoin(data_root, "HumanML3D", "HumanML3D"), pjoin(data_root, "HumanML3D"), data_root]
    for candidate_dir in candidate_dirs:
        mean_path = pjoin(candidate_dir, "Mean.npy")
        std_path = pjoin(candidate_dir, "Std.npy")
        if os.path.exists(mean_path) and os.path.exists(std_path):
            return mean_path, std_path
    raise FileNotFoundError("Could not resolve Mean.npy/Std.npy")


def load_molingo(repo_dir: str, data_root: str, dim_pose: int, sample_steps: int, device):
    sys.path.insert(0, repo_dir)
    import mogen.models.molingo.molingo as molingo_models
    from argparse import Namespace
    from mogen.utils.get_opt import get_opt

    opt = Namespace()
    opt.dataset_name = "t2m" if dim_pose == 263 else "ms"
    model_dir = pjoin(repo_dir, "mogen/checkpoints", opt.dataset_name, f"pretrained_model_{dim_pose}")
    opt_path = pjoin(model_dir, "opt.txt")
    model_opt = get_opt(opt_path, device)
    vae_opt_path = pjoin(repo_dir, "mogen/checkpoints", opt.dataset_name, model_opt.vae, "opt.txt")
    vae_ckpt_path = pjoin(repo_dir, "mogen/checkpoints", opt.dataset_name, model_opt.vae, "model", "net_best_fid.ckpt")
    vae_opt = get_opt(vae_opt_path, device=device)
    vae_model = load_vae_model(vae_opt, vae_ckpt_path, dim_pose, device=device)

    ds_rate = int(math.pow(2, vae_opt.down_t))
    max_motion_length = 300 if dim_pose == 272 else 196
    model_func = getattr(molingo_models, f"molingo_{model_opt.model_size}")
    molingo_model = model_func()(
        vae_embed_dim=vae_opt.output_emb_width,
        token_size=max_motion_length // ds_rate,
        unit_length=ds_rate,
        sample_steps=sample_steps,
        t5_max_len=model_opt.t5_max_len,
        adapter_layers=model_opt.aligner_layers,
        ae=vae_opt.ae,
    ).to(device)

    checkpoint_path = pjoin(model_dir, "net_best_fid.pth")
    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    molingo_model.load_state_dict(checkpoint["model"])
    ema_state_dict = checkpoint["model_ema"]
    ema_params = [ema_state_dict[name].to(device) for name, _ in molingo_model.named_parameters()]
    new_state = copy.deepcopy(molingo_model.state_dict())
    for i, (name, _value) in enumerate(molingo_model.named_parameters()):
        new_state[name] = ema_params[i]
    molingo_model.load_state_dict(new_state)
    molingo_model.eval()
    for param in molingo_model.parameters():
        param.requires_grad = False

    mean_path, std_path = resolve_mean_std_paths(data_root, dim_pose)
    return {
        "model": molingo_model,
        "vae": vae_model,
        "std_factor": model_opt.std_factor,
        "unit_length": ds_rate,
        "model_dir": model_dir,
        "model_opt_path": opt_path,
        "checkpoint_path": checkpoint_path,
        "vae_opt_path": vae_opt_path,
        "vae_checkpoint_path": vae_ckpt_path,
        "mean_path": mean_path,
        "std_path": std_path,
    }


def load_prompt_rows(prompt_file: str, prompt_limit: int):
    rows = []
    with open(prompt_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("#")
            text = parts[0].strip()
            seconds = float(parts[1].strip()) if len(parts) >= 2 and parts[1].strip() else 9.8
            rows.append({"text": text, "seconds": seconds})
            if prompt_limit and len(rows) >= prompt_limit:
                break
    return rows


def lengths_from_seconds(rows, unit_length, device):
    token_lens = torch.LongTensor([int(row["seconds"] * 20 // 4) for row in rows]).to(device)
    return (token_lens * 4 * 1.5).int()


@contextmanager
def molingo_early_exit(model, endpoint_layer: int):
    layers = list(model.seqTransDecoder.layers)
    original = list(layers)

    class DecoderBypass(torch.nn.Module):
        def forward(self, tgt, *args, **kwargs):
            return tgt

    model.seqTransDecoder.layers = torch.nn.ModuleList(
        [layer if idx <= endpoint_layer else DecoderBypass() for idx, layer in enumerate(original)]
    )
    try:
        yield
    finally:
        model.seqTransDecoder.layers = torch.nn.ModuleList(original)


def sample_molingo_tokens(model, rows, lengths, cfg, acc, seed, device):
    fixseed(seed)
    texts = [row["text"] for row in rows]
    with torch.no_grad():
        return model.sample_tokens(
            bsz=len(rows),
            m_lens=lengths,
            cfg=cfg,
            cfg_schedule="constant",
            labels=texts,
            temperature=1.0,
            acc_ratio=acc,
            device=device,
        )


def decode_molingo(vae, tokens, std_factor):
    with torch.no_grad():
        return vae.decode(tokens / std_factor).detach().cpu().numpy()


def run_molingo_ldo(args: argparse.Namespace) -> dict:
    started = time.time()
    os.chdir(args.molingo_repo)
    sys.path.insert(0, args.molingo_repo)
    device = torch.device(f"cuda:{args.gpu_id}" if torch.cuda.is_available() else "cpu")
    if device.type != "cuda":
        raise RuntimeError("MoLingo LDO requires CUDA")
    torch.cuda.set_device(device)
    fixseed(args.seed)

    rows = load_prompt_rows(args.prompt_file, args.prompt_limit)
    if args.prompt_count_min and len(rows) < args.prompt_count_min:
        raise RuntimeError(f"Prompt file has {len(rows)} prompts, below {args.prompt_count_min}")
    bundle = load_molingo(args.molingo_repo, args.data_root, args.dim_pose, args.sample_steps, device)
    model = bundle["model"]
    vae = bundle["vae"]
    lengths = lengths_from_seconds(rows, bundle["unit_length"], device)
    num_layers = len(list(model.seqTransDecoder.layers))
    blocks = DEFAULT_BLOCKS["molingo"]
    if num_layers != 16:
        raise RuntimeError(f"Expected MoLingo 16 decoder layers, got {num_layers}")

    output_index = {}
    summary = []
    for seed in [int(x) for x in args.seeds.split(",") if x.strip()]:
        seed_dir = pjoin(args.out_dir, "molingo", f"seed_{seed}")
        os.makedirs(seed_dir, exist_ok=True)
        with torch.no_grad():
            baseline_tokens = sample_molingo_tokens(model, rows, lengths, args.cfg, args.acc, seed, device)
            baseline = decode_molingo(vae, baseline_tokens, bundle["std_factor"])
        baseline_path = pjoin(seed_dir, "baseline.npy")
        np.save(baseline_path, baseline)
        output_index[f"seed_{seed}/baseline"] = baseline_path
        summary.append({"seed": seed, "variant": "baseline", "family": "baseline", "shape": list(baseline.shape)})

        for block in blocks:
            with molingo_early_exit(model, int(block["endpoint_layer"])):
                tokens = sample_molingo_tokens(model, rows, lengths, args.cfg, args.acc, seed, device)
                arrays = decode_molingo(vae, tokens, bundle["std_factor"])
            diff = arrays - baseline
            name = f"ldo_{block['block']}_endpoint_{block['endpoint_layer']:02d}"
            path = pjoin(seed_dir, name + ".npy")
            np.save(path, arrays)
            output_index[f"seed_{seed}/{name}"] = path
            summary.append(
                {
                    "seed": seed,
                    "variant": name,
                    "family": "ldo",
                    "block": block["block"],
                    "endpoint_layer": block["endpoint_layer"],
                    "layers": block["layers"],
                    "shape": list(arrays.shape),
                    "l2_vs_baseline": float(np.linalg.norm(diff.reshape(-1))),
                    "mean_abs_vs_baseline": float(np.mean(np.abs(diff))),
                    "max_abs_vs_baseline": float(np.max(np.abs(diff))),
                    "allclose_vs_baseline": bool(np.allclose(arrays, baseline, atol=1e-6, rtol=1e-6)),
                }
            )

    summary_path = pjoin(args.out_dir, "molingo", "ldo_summary.json")
    write_json(summary_path, {"rows": rows, "lengths": [int(x) for x in lengths.detach().cpu().tolist()], "summary": summary})
    return {
        "trace": "LDO/DSO",
        "scope": "molingo_layer_direct_output_early_exit_diagnostic",
        "paper_level_status": "diagnostic_arrays_computed_not_official_metrics",
        "baseline": "molingo",
        "diagnostic": "LDO",
        "created_at": now(),
        "repo_dir": args.molingo_repo,
        "repo_status": {
            "head": run(["git", "rev-parse", "HEAD"], args.molingo_repo),
            "branch": run(["git", "branch", "--show-current"], args.molingo_repo),
            "status_short": run(["git", "status", "--short"], args.molingo_repo).splitlines(),
        },
        "block_plan": blocks,
        "num_layers": num_layers,
        "prompt_file": args.prompt_file,
        "num_prompts": len(rows),
        "seeds": [int(x) for x in args.seeds.split(",") if x.strip()],
        "cfg": args.cfg,
        "sample_steps": args.sample_steps,
        "acc": args.acc,
        "summary_file": summary_path,
        "outputs": output_index,
        "model_checkpoint": bundle["checkpoint_path"],
        "model_checkpoint_sha256": sha256(bundle["checkpoint_path"]),
        "vae_checkpoint": bundle["vae_checkpoint_path"],
        "vae_checkpoint_sha256": sha256(bundle["vae_checkpoint_path"]),
        "limitations": [
            "MoLingo LDO is implemented as decoder early-exit by replacing later TransformerDecoder layers with Identity before flow sampling and VAE decode.",
            "This is a diagnostic direct-output proxy, not an official full evaluator result.",
            "Because flow sampling remains active after the endpoint, attribution is to decoder endpoint representation plus the unchanged flow decoder.",
        ],
        "failures": [],
        "elapsed_sec": time.time() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--mode", default="all", choices=["all", "audit_only", "molingo"])
    parser.add_argument("--gpu_id", type=int, default=0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--seeds", default="0")
    parser.add_argument("--motionclr_repo", default="/data/public/ripemangobox/Motion/MotionCLR")
    parser.add_argument("--motiongpt_repo", default="/data/public/ripemangobox/Motion/MotionGPT")
    parser.add_argument("--molingo_repo", default="/data/public/ripemangobox/Motion/MoLingo")
    parser.add_argument("--data_root", default="/data/public/ripemangobox/Motion/datasets")
    parser.add_argument("--prompt_file", default="/data/public/ripemangobox/Motion/experiments/MoDebug/molingo/prompt_sets/molingo_trace1_formal_test64_20260603.txt")
    parser.add_argument("--prompt_limit", type=int, default=64)
    parser.add_argument("--prompt_count_min", type=int, default=0)
    parser.add_argument("--dim_pose", type=int, default=272)
    parser.add_argument("--cfg", type=float, default=4.0)
    parser.add_argument("--sample_steps", type=int, default=32)
    parser.add_argument("--acc", type=int, default=1)
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    manifests = {}

    if args.mode in {"all", "audit_only"}:
        manifests["motionclr"] = blocked_manifest(
            args,
            "motionclr",
            "MotionCLR CLRBlock outputs have varying channel/time resolutions inside UNet; they are not directly decodable motion outputs. Use DSO for MotionCLR step outputs.",
            {"num_layers": 18},
        )
        manifests["motiongpt"] = blocked_manifest(
            args,
            "motiongpt",
            "MotionGPT T5 decoder hidden states are not motion tokens and official generate() does not expose a stable direct-output decoder interface. Early-exit generation needs separate validation before official metrics.",
            {"num_layers": 12},
        )
    if args.mode in {"all", "molingo"}:
        try:
            manifests["molingo"] = run_molingo_ldo(args)
        except Exception as exc:
            manifests["molingo"] = blocked_manifest(
                args,
                "molingo",
                f"MoLingo LDO execution failed: {exc}",
                {"paper_level_status": "failed", "num_layers": 16},
            )

    manifest_path = pjoin(args.out_dir, "manifest.json")
    write_json(manifest_path, {"created_at": now(), "scope": "ldo_audit_runner", "manifests": manifests})
    for key, payload in manifests.items():
        write_json(pjoin(args.out_dir, key, "manifest.json"), payload)
    print(json.dumps({"manifest": manifest_path, "baselines": sorted(manifests)}, indent=2))


if __name__ == "__main__":
    main()
