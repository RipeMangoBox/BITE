#!/usr/bin/env python3
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


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def repo_status(repo_dir):
    def run(args):
        try:
            return subprocess.check_output(args, cwd=repo_dir, text=True, stderr=subprocess.STDOUT).strip()
        except Exception as exc:
            return f"ERROR: {exc}"

    return {
        "head": run(["git", "rev-parse", "HEAD"]),
        "branch": run(["git", "rev-parse", "--abbrev-ref", "HEAD"]),
        "status_short": run(["git", "status", "--short"]),
    }


def fixseed(seed):
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


def resolve_mean_std_paths(data_root, dim_pose):
    if dim_pose == 272:
        candidate_dirs = [
            pjoin(data_root, "HumanML3D_272", "mean_std"),
            pjoin(data_root, "272-dim-HumanML3D", "mean_std"),
            pjoin(data_root, "mean_std"),
            pjoin(data_root, "HumanML3D-E-MP", "motion_format_stats", "hml272"),
        ]
    else:
        candidate_dirs = [
            pjoin(data_root, "HumanML3D", "HumanML3D"),
            pjoin(data_root, "HumanML3D"),
            data_root,
        ]
    checked = []
    for candidate_dir in candidate_dirs:
        mean_path = pjoin(candidate_dir, "Mean.npy")
        std_path = pjoin(candidate_dir, "Std.npy")
        checked.append({"mean": mean_path, "std": std_path})
        if os.path.exists(mean_path) and os.path.exists(std_path):
            return mean_path, std_path, checked
    raise FileNotFoundError("Could not resolve Mean.npy/Std.npy from candidates: " + json.dumps(checked, indent=2))


def load_molingo(repo_dir, data_root, dim_pose, sample_steps, device):
    sys.path.insert(0, repo_dir)
    import mogen.models.molingo.molingo as molingo_models
    from argparse import Namespace
    from mogen.eval_mogen import load_vae_model as _unused  # noqa: F401
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

    mean_path, std_path, mean_std_candidates = resolve_mean_std_paths(data_root, dim_pose)
    mean = np.load(mean_path)
    std = np.load(std_path)

    return {
        "model": molingo_model,
        "vae": vae_model,
        "model_opt": model_opt,
        "vae_opt": vae_opt,
        "model_dir": model_dir,
        "model_opt_path": opt_path,
        "vae_opt_path": vae_opt_path,
        "checkpoint_path": checkpoint_path,
        "vae_checkpoint_path": vae_ckpt_path,
        "std_factor": model_opt.std_factor,
        "unit_length": ds_rate,
        "max_motion_length": max_motion_length,
        "mean_path": mean_path,
        "std_path": std_path,
        "mean_std_candidates": mean_std_candidates,
        "mean": mean,
        "std": std,
    }


def load_prompt_rows(prompt_file, prompt_limit):
    rows = []
    with open(prompt_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("#")
            text = parts[0].strip()
            if len(parts) >= 2 and parts[1].strip():
                seconds = float(parts[1].strip())
            else:
                seconds = 9.8
            rows.append({"text": text, "seconds": seconds})
            if prompt_limit and len(rows) >= prompt_limit:
                break
    return rows


def require_prompt_count(rows, prompt_count_min, prompt_file):
    if prompt_count_min and len(rows) < prompt_count_min:
        raise RuntimeError(f"Prompt file {prompt_file} has {len(rows)} prompts, below required minimum {prompt_count_min}")


def lengths_from_seconds(rows, unit_length, device):
    # MoLingo demo uses: token_lens = seconds * 20 // 4; m_length = token_lens * 4 * 1.5.
    token_lens = torch.LongTensor([int(row["seconds"] * 20 // 4) for row in rows]).to(device)
    lengths = (token_lens * 4 * 1.5).int()
    return lengths


def diff_stats(arrays, baseline):
    diff = arrays - baseline
    return {
        "l2_vs_baseline": float(np.linalg.norm(diff.reshape(-1))),
        "mean_abs_vs_baseline": float(np.mean(np.abs(diff))),
        "max_abs_vs_baseline": float(np.max(np.abs(diff))),
        "allclose_vs_baseline": bool(np.allclose(arrays, baseline, atol=1e-6, rtol=1e-6)),
    }


@contextmanager
def scaled_ca_outputs(model, layer_ids, alpha):
    layers = list(model.seqTransDecoder.layers)
    patched = []
    call_counts = {str(layer_id): 0 for layer_id in layer_ids}
    for layer_id in layer_ids:
        layer = layers[layer_id]
        old_forward = layer.multihead_attn.forward

        def make_forward(forward_fn, lid):
            def forward_scaled(*args, **kwargs):
                out = forward_fn(*args, **kwargs)
                call_counts[str(lid)] += 1
                if isinstance(out, tuple):
                    attn_out = out[0] * alpha
                    return (attn_out,) + out[1:]
                return out * alpha

            return forward_scaled

        layer.multihead_attn.forward = make_forward(old_forward, layer_id)
        patched.append((layer.multihead_attn, old_forward))
    try:
        yield call_counts
    finally:
        for module, old_forward in patched:
            module.forward = old_forward


@contextmanager
def replace_decoder_hidden_with_uncond(model, layer_ids, enabled=True):
    layers = list(model.seqTransDecoder.layers)
    patched = []
    call_counts = {str(layer_id): 0 for layer_id in layer_ids}
    replacement_checks = []
    for layer_id in layer_ids:
        layer = layers[layer_id]
        old_forward = layer.forward

        def make_forward(forward_fn, lid):
            def forward_replaced(tgt, memory, *args, **kwargs):
                out = forward_fn(tgt, memory, *args, **kwargs)
                call_counts[str(lid)] += 1
                if not enabled:
                    return out
                if out.shape[0] % 2 != 0:
                    raise RuntimeError(f"Layer {lid} batch is not even: {tuple(out.shape)}")
                half = out.shape[0] // 2
                before = (out[:half] - out[half:]).detach().abs().max().item()
                new_out = out.clone()
                new_out[:half] = out[half:].clone()
                after = (new_out[:half] - new_out[half:]).detach().abs().max().item()
                replacement_checks.append({"layer_id": lid, "shape": list(out.shape), "max_abs_before": before, "max_abs_after": after})
                return new_out

            return forward_replaced

        layer.forward = make_forward(old_forward, layer_id)
        patched.append((layer, old_forward))
    try:
        yield call_counts, replacement_checks
    finally:
        for layer, old_forward in patched:
            layer.forward = old_forward


def sample_tokens_pair_cfg(model, rows, lengths, cfg, acc, seed, device):
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


@contextmanager
def cache_decoder_layer_outputs(model, layer_ids):
    layers = list(model.seqTransDecoder.layers)
    patched = []
    cache = {}
    call_counts = {str(layer_id): 0 for layer_id in layer_ids}
    for layer_id in layer_ids:
        layer = layers[layer_id]
        old_forward = layer.forward

        def make_forward(forward_fn, lid):
            def forward_cached(*args, **kwargs):
                out = forward_fn(*args, **kwargs)
                call_counts[str(lid)] += 1
                cache[str(lid)] = out.detach().clone()
                return out

            return forward_cached

        layer.forward = make_forward(old_forward, layer_id)
        patched.append((layer, old_forward))
    try:
        yield cache, call_counts
    finally:
        for layer, old_forward in patched:
            layer.forward = old_forward


@contextmanager
def replace_decoder_layer_outputs_from_cache(model, layer_ids, cache):
    layers = list(model.seqTransDecoder.layers)
    patched = []
    call_counts = {str(layer_id): 0 for layer_id in layer_ids}
    replacement_checks = []
    for layer_id in layer_ids:
        layer = layers[layer_id]
        old_forward = layer.forward

        def make_forward(forward_fn, lid):
            def forward_replaced(*args, **kwargs):
                out = forward_fn(*args, **kwargs)
                call_counts[str(lid)] += 1
                key = str(lid)
                if key not in cache:
                    raise RuntimeError(f"Missing cached uncond hidden for layer {lid}")
                replacement = cache[key]
                if tuple(out.shape) != tuple(replacement.shape):
                    raise RuntimeError(f"Layer {lid} replacement shape mismatch: {tuple(out.shape)} vs {tuple(replacement.shape)}")
                before = (out - replacement).detach().abs().max().item()
                new_out = replacement.clone()
                after = (new_out - replacement).detach().abs().max().item()
                replacement_checks.append({"layer_id": lid, "shape": list(out.shape), "max_abs_before": before, "max_abs_after": after})
                return new_out

            return forward_replaced

        layer.forward = make_forward(old_forward, layer_id)
        patched.append((layer, old_forward))
    try:
        yield call_counts, replacement_checks
    finally:
        for layer, old_forward in patched:
            layer.forward = old_forward


def sample_tokens_hidden_replace(model, rows, lengths, cfg, acc, seed, device, layer_ids):
    fixseed(seed)
    texts = [row["text"] for row in rows]
    bsz = len(rows)
    m_lens = lengths // model.unit_length
    seq_len = model.seq_len
    key_padding_mask = ~model.__class__.__dict__["sample_tokens"].__globals__["lengths_to_mask"](m_lens, seq_len).to(device)
    latents = torch.where(
        key_padding_mask.unsqueeze(-1),
        torch.zeros(bsz, seq_len, model.token_embed_dim).to(device),
        model.mask_token.repeat(bsz, seq_len, 1),
    )
    masked_rand_schedule = torch.where(key_padding_mask, 1e5, torch.rand_like(key_padding_mask, dtype=torch.float))
    steps = int(seq_len // acc)
    replace_counts_total = {str(layer_id): 0 for layer_id in layer_ids}
    cache_counts_total = {str(layer_id): 0 for layer_id in layer_ids}
    replacement_checks = []
    for timestep in torch.linspace(0, 1, steps, device=device):
        with torch.no_grad():
            rand_mask_prob = torch.cos(timestep * math.pi * 0.5)
            num_masked = torch.round(rand_mask_prob * m_lens).clamp(min=1)
            sorted_indices = masked_rand_schedule.argsort(dim=1)
            ranks = sorted_indices.argsort(dim=1)
            is_mask = ranks < num_masked.unsqueeze(-1)
            latents_masked = torch.where(is_mask.unsqueeze(-1), model.mask_token.repeat(bsz, seq_len, 1), latents)
            cfg_iter = cfg

            with cache_decoder_layer_outputs(model, layer_ids) as (cache, cache_counts):
                aux_z = model.forward_z(latents_masked, texts, key_padding_mask, force_mask=True)
            with replace_decoder_layer_outputs_from_cache(model, layer_ids, cache) as (replace_counts, checks):
                z = model.forward_z(latents_masked, texts, key_padding_mask, force_mask=False)
            for key, value in cache_counts.items():
                cache_counts_total[key] += value
            for key, value in replace_counts.items():
                replace_counts_total[key] += value
            replacement_checks.extend(checks)

            mixed_z = torch.cat([z, aux_z], dim=0)
            mb, sl, embed_dim = mixed_z.size()
            mask = torch.cat([is_mask, is_mask], dim=0).reshape(mb * sl)
            mixed_z = mixed_z.reshape(mb * sl, embed_dim)[mask]
            sampled_token_latent = model.flow_loss.sample(mixed_z, cfg_iter)
            sampled_token_latent, _ = sampled_token_latent.chunk(2, dim=0)
            mask_half, _ = mask.chunk(2, dim=0)
            x_flat = latents_masked.reshape(bsz * seq_len, model.token_embed_dim)
            x_flat[mask_half.reshape(bsz * seq_len)] = sampled_token_latent
            sampled_tokens = x_flat.reshape(bsz, seq_len, model.token_embed_dim)

            latents = torch.where(is_mask.unsqueeze(-1), sampled_tokens, latents_masked)
            masked_rand_schedule = masked_rand_schedule.masked_fill(~is_mask, 1e5)
    latents = torch.where(key_padding_mask.unsqueeze(-1), torch.zeros_like(latents), latents)
    return latents, replace_counts_total, cache_counts_total, replacement_checks


def decode_features(vae, tokens, std_factor):
    with torch.no_grad():
        return vae.decode(tokens / std_factor).detach().cpu().numpy()


def save_arrays(out_dir, seed, variant, arrays):
    seed_dir = pjoin(out_dir, f"seed_{seed}")
    os.makedirs(seed_dir, exist_ok=True)
    path = pjoin(seed_dir, f"{variant}.npy")
    np.save(path, arrays)
    return path


def save_variant(out_dir, seed, variant, arrays, started):
    path = save_arrays(out_dir, seed, variant, arrays)
    print(f"[{time.time() - started:.1f}s] seed={seed} saved {variant} shape={list(arrays.shape)} path={path}", flush=True)
    return path


def run_variant(model, vae, rows, lengths, cfg, acc, seed, device, std_factor, hidden_replace=False):
    if hidden_replace:
        tokens, _replace_counts, _cache_counts, _checks = sample_tokens_hidden_replace(model, rows, lengths, cfg, acc, seed, device, [])
    else:
        tokens = sample_tokens_pair_cfg(model, rows, lengths, cfg, acc, seed, device)
    return decode_features(vae, tokens, std_factor)


def run_hidden_replace_variant(model, vae, rows, lengths, cfg, acc, seed, device, std_factor, layer_ids):
    tokens, replace_counts, cache_counts, checks = sample_tokens_hidden_replace(model, rows, lengths, cfg, acc, seed, device, layer_ids)
    return decode_features(vae, tokens, std_factor), replace_counts, cache_counts, checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo_dir", default="/data/public/ripemangobox/Motion/MoLingo")
    parser.add_argument("--data_root", default="/data/public/ripemangobox/Motion/datasets/272-dim-HumanML3D/..")
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--prompt_file", default="/data/public/ripemangobox/Motion/MoLingo/assets/example.txt")
    parser.add_argument("--prompt_limit", type=int, default=64)
    parser.add_argument("--prompt_count_min", type=int, default=0)
    parser.add_argument("--seeds", default="0,1,2")
    parser.add_argument("--dim_pose", type=int, default=272)
    parser.add_argument("--cfg", type=float, default=4.0)
    parser.add_argument("--sample_steps", type=int, default=32)
    parser.add_argument("--acc", type=int, default=1)
    parser.add_argument("--ca_alpha", type=float, default=0.0)
    parser.add_argument("--run_scope", default="formal_diagnostic_layer_sweep", choices=["formal_diagnostic_layer_sweep", "dev_validation_only"])
    parser.add_argument("--dev_layers", default="0,15")
    args = parser.parse_args()

    started = time.time()
    os.makedirs(args.out_dir, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type != "cuda":
        raise RuntimeError("MoLingo diagnostic requires CUDA")
    os.chdir(args.repo_dir)

    rows = load_prompt_rows(args.prompt_file, args.prompt_limit)
    require_prompt_count(rows, args.prompt_count_min, args.prompt_file)
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    bundle = load_molingo(args.repo_dir, args.data_root, args.dim_pose, args.sample_steps, device)
    model = bundle["model"]
    vae = bundle["vae"]
    lengths = lengths_from_seconds(rows, bundle["unit_length"], device)
    num_layers = len(list(model.seqTransDecoder.layers))
    all_layers = list(range(num_layers))
    if args.run_scope == "dev_validation_only":
        layer_ids = [int(x) for x in args.dev_layers.split(",") if x.strip()]
    else:
        layer_ids = all_layers

    prompt_path = pjoin(args.out_dir, "prompt_set.json")
    with open(prompt_path, "w") as f:
        json.dump({"rows": rows, "lengths": [int(x) for x in lengths.detach().cpu().tolist()]}, f, indent=2)

    summary = []
    outputs = {}
    failures = []
    for seed in seeds:
        seed_key = str(seed)
        outputs[seed_key] = {}
        baseline = run_variant(model, vae, rows, lengths, args.cfg, args.acc, seed, device, bundle["std_factor"])
        variant = "baseline"
        outputs[seed_key][variant] = save_variant(args.out_dir, seed, variant, baseline, started)
        summary.append({"seed": seed, "family": "baseline", "variant": variant, "num_outputs": int(baseline.shape[0])})

        with scaled_ca_outputs(model, all_layers, 1.0) as counts:
            arrays = run_variant(model, vae, rows, lengths, args.cfg, args.acc, seed, device, bundle["std_factor"])
        variant = "noop_ca_all_layers_alpha_1"
        outputs[seed_key][variant] = save_variant(args.out_dir, seed, variant, arrays, started)
        row = {"seed": seed, "family": "noop", "variant": variant, "layers": all_layers, "hook_call_counts": counts, **diff_stats(arrays, baseline)}
        summary.append(row)
        if not row["allclose_vs_baseline"]:
            failures.append(f"{variant} seed {seed} not allclose")

        with replace_decoder_hidden_with_uncond(model, all_layers, enabled=False) as (counts, checks):
            arrays = run_variant(model, vae, rows, lengths, args.cfg, args.acc, seed, device, bundle["std_factor"])
        variant = "noop_hidden_hook_all_layers_disabled"
        outputs[seed_key][variant] = save_variant(args.out_dir, seed, variant, arrays, started)
        row = {
            "seed": seed,
            "family": "noop",
            "variant": variant,
            "layers": all_layers,
            "hook_call_counts": counts,
            "replacement_checks_tail": checks[-len(all_layers) :],
            **diff_stats(arrays, baseline),
        }
        summary.append(row)
        if not row["allclose_vs_baseline"]:
            failures.append(f"{variant} seed {seed} not allclose")

        with scaled_ca_outputs(model, all_layers, args.ca_alpha) as counts:
            arrays = run_variant(model, vae, rows, lengths, args.cfg, args.acc, seed, device, bundle["std_factor"])
        variant = "positive_control_ca_all_layers_alpha_" + str(args.ca_alpha).replace(".", "p")
        outputs[seed_key][variant] = save_variant(args.out_dir, seed, variant, arrays, started)
        row = {"seed": seed, "family": "positive_control", "variant": variant, "layers": all_layers, "hook_call_counts": counts, **diff_stats(arrays, baseline)}
        summary.append(row)
        if row["allclose_vs_baseline"]:
            failures.append(f"{variant} seed {seed} unexpectedly allclose")

        arrays, counts, cache_counts, checks = run_hidden_replace_variant(
            model, vae, rows, lengths, args.cfg, args.acc, seed, device, bundle["std_factor"], all_layers
        )
        variant = "positive_control_hidden_replace_all_layers"
        outputs[seed_key][variant] = save_variant(args.out_dir, seed, variant, arrays, started)
        row = {
            "seed": seed,
            "family": "positive_control",
            "variant": variant,
            "layers": all_layers,
            "hook_call_counts": counts,
            "uncond_cache_call_counts": cache_counts,
            "replacement_checks_tail": checks[-len(all_layers) :],
            **diff_stats(arrays, baseline),
        }
        summary.append(row)
        if row["allclose_vs_baseline"]:
            failures.append(f"{variant} seed {seed} unexpectedly allclose")

        for layer_id in layer_ids:
            with scaled_ca_outputs(model, [layer_id], args.ca_alpha) as counts:
                arrays = run_variant(model, vae, rows, lengths, args.cfg, args.acc, seed, device, bundle["std_factor"])
            variant = f"layer_{layer_id:02d}_ca_alpha_" + str(args.ca_alpha).replace(".", "p")
            outputs[seed_key][variant] = save_variant(args.out_dir, seed, variant, arrays, started)
            summary.append({
                "seed": seed,
                "family": "ca_output_perturbation",
                "variant": variant,
                "layer": layer_id,
                "alpha": args.ca_alpha,
                "hook_call_counts": counts,
                **diff_stats(arrays, baseline),
            })

        for layer_id in layer_ids:
            arrays, counts, cache_counts, checks = run_hidden_replace_variant(
                model, vae, rows, lengths, args.cfg, args.acc, seed, device, bundle["std_factor"], [layer_id]
            )
            variant = f"layer_{layer_id:02d}_hidden_cond_to_uncond"
            outputs[seed_key][variant] = save_variant(args.out_dir, seed, variant, arrays, started)
            summary.append({
                "seed": seed,
                "family": "cfg_hidden_replacement",
                "variant": variant,
                "layer": layer_id,
                "hook_call_counts": counts,
                "uncond_cache_call_counts": cache_counts,
                "replacement_checks_tail": checks[-1:],
                **diff_stats(arrays, baseline),
            })

    summary_path = pjoin(args.out_dir, "summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    manifest = {
        "baseline": "MoLingo",
        "trace": "Trace 1",
        "experiment_scope": args.run_scope,
        "paper_level_status": "not_final_full_evaluator_result",
        "repo_dir": args.repo_dir,
        "repo_status": repo_status(args.repo_dir),
        "command": " ".join(sys.argv),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        "device": str(device),
        "environment": os.environ.get("CONDA_DEFAULT_ENV", "unknown"),
        "prompt_file": args.prompt_file,
        "prompt_set_file": prompt_path,
        "num_prompts": len(rows),
        "seeds": seeds,
        "num_layers": num_layers,
        "tested_layers": layer_ids,
        "required_layer_groups": {
            "ca_output_perturbation": len(layer_ids),
            "cfg_hidden_replacement": len(layer_ids),
            "minimum_user_required_groups_for_formal": 32 if num_layers == 16 else num_layers * 2,
        },
        "official_settings": {
            "source": "MoLingo README demo plus argparse/model opt defaults",
            "cfg": args.cfg,
            "sample_steps": args.sample_steps,
            "acc": args.acc,
            "cfg_schedule": "constant",
            "temperature": 1.0,
        },
        "paths": {
            "model_opt": bundle["model_opt_path"],
            "model_checkpoint": bundle["checkpoint_path"],
            "vae_opt": bundle["vae_opt_path"],
            "vae_checkpoint": bundle["vae_checkpoint_path"],
            "mean": bundle["mean_path"],
            "std": bundle["std_path"],
            "mean_std_candidates": bundle["mean_std_candidates"],
            "summary": summary_path,
        },
        "sha256": {
            "model_opt": sha256(bundle["model_opt_path"]),
            "model_checkpoint": sha256(bundle["checkpoint_path"]),
            "vae_opt": sha256(bundle["vae_opt_path"]),
            "vae_checkpoint": sha256(bundle["vae_checkpoint_path"]),
            "summary": sha256(summary_path),
        },
        "outputs": outputs,
        "failures": failures,
        "elapsed_sec": time.time() - started,
    }
    manifest_path = pjoin(args.out_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"[{time.time() - started:.1f}s] wrote summary={summary_path} manifest={manifest_path} failures={failures}", flush=True)
    if failures:
        raise RuntimeError("Failures: " + "; ".join(failures))


if __name__ == "__main__":
    main()
