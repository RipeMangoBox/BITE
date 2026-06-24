#!/usr/bin/env python3
"""MoLingo Trace 1 Full Evaluation with Attention Intervention.

Supports families: baseline, ca, cfg_ca, sa, cfg_sa
Model: MoLingo (nn.TransformerDecoder, 16 layers)
Intervention targets: self_attn (SA) / multihead_attn (CA) per layer
Official eval: mogen.core.eval.eval_molingo_ms (FID, R-Precision, Matching Score)
CFG: separate force_mask=True/False forward_z calls, not paired batch
CFG residual mixers: replace, residual_gate, apg_orthogonal, stat_match, discrepancy_gate
Gate: MODEBUG_DS_APPROVED_EXECUTE=1
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import os
import subprocess
import sys
import time
from collections import OrderedDict
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader
from argparse import Namespace

# Add MoLingo to path
_MOLINGO_REPO = "/data/public/ripemangobox/Motion/MoLingo"
if _MOLINGO_REPO not in sys.path:
    sys.path.insert(0, _MOLINGO_REPO)

from mogen.utils.fixseed import fixseed
from mogen.utils.get_opt import get_opt
from mogen.utils.eval_utils import load_ms_evaluators
from mogen.data.ms_dataset import Text2MotionDatasetMS
from mogen.models.vae.vae import VAE
import mogen.models.molingo.molingo as molingo_models
from mogen.core.eval import eval_molingo_ms

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BASELINE_NAME = "MoLingo"
TRACE = "Trace 1"
NATIVE_DECODER_LAYERS = 16
FAMILIES = ("baseline", "ca", "cfg_ca", "sa", "cfg_sa")

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")

def run_git(args, cwd):
    try:
        return subprocess.check_output(args, cwd=str(cwd), text=True, stderr=subprocess.STDOUT).strip()
    except Exception as exc:
        return f"ERROR: {exc}"

def sha256(path):
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def file_record(p):
    p = Path(p).expanduser().resolve()
    return {"path": str(p), "sha256": sha256(p)}

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def parse_layer(value):
    return int(value.strip())


def parse_float_list(value: str) -> list[float]:
    if not value.strip():
        return []
    return [float(item.strip()) for item in value.split(",") if item.strip()]


def cfg_step_alpha(schedule, timestep, decay, interval, table):
    progress = float(timestep.detach().item()) if hasattr(timestep, "detach") else float(timestep)
    if schedule == "constant":
        return 1.0
    if schedule == "linear_increase":
        return progress
    if schedule == "linear_decay":
        return 1.0 - progress
    if schedule == "c2fg_decay":
        return math.exp(-decay * progress)
    if schedule == "inverse_decay":
        return math.exp(-decay * (1.0 - progress))
    if schedule == "interval":
        start, end = interval
        return 1.0 if start <= progress <= end else 0.0
    if schedule == "scalar_table":
        if not table:
            raise ValueError("--cfg_schedule_table is required for scalar_table schedule")
        idx = min(len(table) - 1, int(round(progress * (len(table) - 1))))
        return table[idx]
    raise ValueError(f"Unsupported cfg schedule: {schedule}")


def scheduled_cfg_scale(base_cfg, schedule, timestep, decay, interval, table, alpha_scale):
    alpha_t = cfg_step_alpha(schedule, timestep, decay, interval, table)
    return 1.0 + (base_cfg - 1.0) * alpha_scale * alpha_t, alpha_t

# ---------------------------------------------------------------------------
# Model loading (replicating eval_mogen.py protocol)
# ---------------------------------------------------------------------------

def load_vae_model(vae_opt, ckpt_path, dim_pose, device):
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
        new_key = k[len("module."):] if k.startswith("module.") else k
        new_state_dict[new_key] = v
    vae_model.load_state_dict(state_dict=new_state_dict)
    for param in vae_model.parameters():
        param.requires_grad = False
    return vae_model


def load_molingo_model(repo_dir, dim_pose, device, step, t5_path):
    """Load MoLingo with EMA weights, following eval_mogen.py protocol."""
    dataset = "ms" if dim_pose == 272 else "t2m"
    model_dir = Path(repo_dir) / "mogen" / "checkpoints" / dataset / f"pretrained_model_{dim_pose}"
    opt_path = model_dir / "opt.txt"
    model_opt = get_opt(str(opt_path), device)

    # VAE
    vae_opt_path = Path(repo_dir) / "mogen" / "checkpoints" / dataset / model_opt.vae / "opt.txt"
    vae_ckpt_path = Path(repo_dir) / "mogen" / "checkpoints" / dataset / model_opt.vae / "model" / "net_best_fid.ckpt"
    vae_opt = get_opt(str(vae_opt_path), device=device)
    vae_model = load_vae_model(vae_opt, str(vae_ckpt_path), dim_pose, device)

    vae_embed_dim = vae_opt.output_emb_width
    ds_rate = int(math.pow(2, vae_opt.down_t))
    unit_length = ds_rate

    # MoLingo model
    model_func_name = f"molingo_{model_opt.model_size}"
    molingo_func = getattr(molingo_models, model_func_name)
    partial_molingo = molingo_func()

    molingo_model = partial_molingo(
        vae_embed_dim=vae_embed_dim,
        token_size=model_opt.max_motion_length // ds_rate,
        unit_length=unit_length,
        sample_steps=step,
        t5_max_len=model_opt.t5_max_len,
        adapter_layers=model_opt.aligner_layers,
        ae=vae_opt.ae,
    )
    molingo_model.to(device)

    ckpt_path = model_dir / "net_best_fid.pth"
    checkpoint = torch.load(str(ckpt_path), map_location="cpu")
    molingo_model.load_state_dict(checkpoint["model"], strict=False)

    # EMA weights
    ema_params = [checkpoint["model_ema"][name].cuda()
                  for name, _ in molingo_model.named_parameters()]
    ema_state_dict = OrderedDict()
    for i, (name, _value) in enumerate(molingo_model.named_parameters()):
        assert name in checkpoint["model_ema"]
        ema_state_dict[name] = ema_params[i]
    molingo_model.load_state_dict(ema_state_dict, strict=False)
    del checkpoint, ema_state_dict
    molingo_model.eval()

    actual_layers = len(molingo_model.seqTransDecoder.layers)
    print(f"[MoLingo] Loaded model_size={model_opt.model_size}, "
          f"decoder_layers={actual_layers}, vae_embed_dim={vae_embed_dim}")

    return molingo_model, vae_model, model_opt, vae_opt, unit_length


def load_dataset(repo_dir, dim_pose, data_root, model_opt, unit_length):
    """Load MS-272 test dataset and dataloader."""
    opt = Namespace()
    opt.dataset_name = "ms"
    opt.joints_num = 22
    opt.data_root = data_root
    opt.motion_dir = os.path.join(opt.data_root, "motion_data")
    opt.text_dir = os.path.join(opt.data_root, "texts")
    opt.max_motion_length = 300
    opt.unit_length = unit_length

    mean = np.load(os.path.join(opt.data_root, "mean_std", "Mean.npy"))
    std = np.load(os.path.join(opt.data_root, "mean_std", "Std.npy"))
    test_split_file = os.path.join(opt.data_root, "split", "test.txt")

    test_dataset = Text2MotionDatasetMS(opt, mean, std, test_split_file)
    test_loader = DataLoader(
        test_dataset, batch_size=32, drop_last=True,
        shuffle=True, num_workers=4, pin_memory=True
    )
    return test_dataset, test_loader

# ---------------------------------------------------------------------------
# Attention intervention
# ---------------------------------------------------------------------------

def _get_attn_module(model, family, layer_idx):
    """Get the target attention module for the given family and layer."""
    layer = model.seqTransDecoder.layers[layer_idx]
    if family in ("sa", "cfg_sa"):
        return layer.self_attn
    elif family in ("ca", "cfg_ca"):
        return layer.multihead_attn
    else:
        raise ValueError(f"Unknown family: {family}")


def _shape_of(value):
    if isinstance(value, tuple):
        value = value[0]
    if hasattr(value, "shape"):
        return list(value.shape)
    return None


def _mean_float(value):
    if value is None:
        return None
    return float(value.detach().float().mean().item())


def _residual_norm_stats(cond, uncond, mixed):
    delta_in = cond - uncond
    delta_out = mixed - uncond
    in_norm = torch.linalg.vector_norm(delta_in.detach().float(), dim=-1)
    out_norm = torch.linalg.vector_norm(delta_out.detach().float(), dim=-1)
    cond_norm = torch.linalg.vector_norm(cond.detach().float(), dim=-1)
    uncond_norm = torch.linalg.vector_norm(uncond.detach().float(), dim=-1)
    return {
        "input_residual_norm": float(in_norm.mean().item()),
        "output_residual_norm": float(out_norm.mean().item()),
        "cond_norm": float(cond_norm.mean().item()),
        "uncond_norm": float(uncond_norm.mean().item()),
    }


def _update_mixer_audit(audit, mixer, cond, uncond, mixed, gate=None):
    stats = audit["mixer_checks"]
    stats["applied"] += 1
    stats["last_mixer"] = mixer
    norm_stats = _residual_norm_stats(cond, uncond, mixed)
    stats["last_stats"] = norm_stats
    if gate is not None:
        stats["last_gate_mean"] = _mean_float(gate)
    if len(stats["trace"]) < 200:
        record = {"mixer": mixer, **norm_stats}
        if gate is not None:
            record["gate_mean"] = _mean_float(gate)
        stats["trace"].append(record)


def _project_parallel(delta, reference, eps=1e-6):
    ref_f = reference.float()
    delta_f = delta.float()
    denom = (ref_f * ref_f).sum(dim=-1, keepdim=True).clamp_min(eps)
    coeff = (delta_f * ref_f).sum(dim=-1, keepdim=True) / denom
    return coeff.to(delta.dtype) * reference


def _cosine_gate(cond, uncond, threshold, slope, eps=1e-6):
    cond_f = cond.float()
    uncond_f = uncond.float()
    numerator = (cond_f * uncond_f).sum(dim=-1, keepdim=True)
    denom = torch.linalg.vector_norm(cond_f, dim=-1, keepdim=True)
    denom = denom * torch.linalg.vector_norm(uncond_f, dim=-1, keepdim=True)
    cosine = numerator / denom.clamp_min(eps)
    return torch.sigmoid(slope * (cosine - threshold)).to(cond.dtype)


def _mix_cfg_attention_residual(cond, uncond, config):
    mixer = config["mixer"]
    alpha = config["alpha"]
    delta = cond - uncond
    gate = None

    if mixer == "replace":
        return uncond, gate
    if mixer == "residual_gate":
        return uncond + alpha * delta, gate
    if mixer == "apg_orthogonal":
        parallel = _project_parallel(delta, uncond)
        orthogonal = delta - parallel
        repaired = (
            config["orthogonal_scale"] * orthogonal
            + config["parallel_scale"] * parallel
        )
        return uncond + alpha * repaired, gate
    if mixer == "norm_clamp":
        delta_norm = torch.linalg.vector_norm(delta.float(), dim=-1, keepdim=True).clamp_min(1e-6)
        ref_norm = torch.linalg.vector_norm(uncond.float(), dim=-1, keepdim=True).clamp_min(1e-6)
        max_norm = config["norm_ratio"] * ref_norm
        scale = torch.minimum(torch.ones_like(delta_norm), max_norm / delta_norm).to(delta.dtype)
        return uncond + alpha * delta * scale, scale
    if mixer == "stat_match":
        cond_mean = cond.mean(dim=-1, keepdim=True)
        cond_std = cond.std(dim=-1, keepdim=True, unbiased=False).clamp_min(1e-6)
        uncond_mean = uncond.mean(dim=-1, keepdim=True)
        uncond_std = uncond.std(dim=-1, keepdim=True, unbiased=False).clamp_min(1e-6)
        matched = (cond - cond_mean) / cond_std * uncond_std + uncond_mean
        return uncond + alpha * (matched - uncond), gate
    if mixer == "discrepancy_gate":
        gate = _cosine_gate(
            cond,
            uncond,
            config["discrepancy_threshold"],
            config["discrepancy_slope"],
        )
        return uncond + alpha * gate * delta, gate
    raise ValueError(f"Unsupported cfg residual mixer: {mixer}")


def _build_cfg_mixer_config(args):
    return {
        "mixer": args.cfg_residual_mixer,
        "alpha": args.cfg_residual_alpha,
        "parallel_scale": args.cfg_residual_parallel_scale,
        "orthogonal_scale": args.cfg_residual_orthogonal_scale,
        "norm_ratio": args.cfg_residual_norm_ratio,
        "discrepancy_threshold": args.cfg_residual_discrepancy_threshold,
        "discrepancy_slope": args.cfg_residual_discrepancy_slope,
    }


def _apply_cfg_intervention(model, family, layer_idx, audit, mixer_config):
    """
    Patch model.forward_with_cfg to mix cond/uncond attention outputs.
    
    For cfg_ca: mix cond cross-attention output with uncond cross-attention output.
    For cfg_sa: mix cond self-attention output with uncond self-attention output.
    """
    attn_module = _get_attn_module(model, family, layer_idx)
    orig_forward_with_cfg = model.forward_with_cfg

    # Mutable container for captured uncond attention output
    uncond_output = [None]

    def capture_hook(module, input, output):
        audit["hook_call_counts"]["capture_hook"] += 1
        if isinstance(output, tuple):
            uncond_output[0] = output[0].detach().clone()
        else:
            uncond_output[0] = output.detach().clone()
        audit["replacement_checks"]["captured_uncond"] += 1
        audit["replacement_checks"]["last_uncond_shape"] = _shape_of(output)

    def replace_hook(module, input, output):
        audit["hook_call_counts"]["replace_hook"] += 1
        if uncond_output[0] is not None:
            audit["replacement_checks"]["replaced_cond"] += 1
            cond_shape = _shape_of(output)
            cond_output = output[0] if isinstance(output, tuple) else output
            uncond = uncond_output[0].to(device=cond_output.device, dtype=cond_output.dtype)
            uncond_shape = list(uncond.shape)
            audit["replacement_checks"]["last_cond_shape"] = cond_shape
            if cond_shape != uncond_shape:
                audit["replacement_checks"]["shape_mismatch"] += 1
            mixed_output, gate = _mix_cfg_attention_residual(cond_output, uncond, mixer_config)
            _update_mixer_audit(
                audit,
                mixer_config["mixer"],
                cond_output,
                uncond,
                mixed_output,
                gate=gate,
            )
            if isinstance(output, tuple):
                return (mixed_output,) + output[1:]
            return mixed_output
        audit["replacement_checks"]["missed_replacement"] += 1
        return output

    def intervened_forward_with_cfg(x, y, mask, key_padding_mask, cfg=4.0, temperature=1.0):
        audit["hook_call_counts"]["forward_with_cfg"] += 1
        # Step 1: Uncond forward_z -- capture attention output at target layer
        cap_handle = attn_module.register_forward_hook(capture_hook)
        aux_z = model.forward_z(x, y, key_padding_mask, force_mask=True)
        cap_handle.remove()

        # Step 2: Cond forward_z -- replace attention output with uncond version
        rep_handle = attn_module.register_forward_hook(replace_hook)
        z = model.forward_z(x, y, key_padding_mask, force_mask=False)
        rep_handle.remove()

        # Step 3: Flow-space CFG mixing (from original forward_with_cfg)
        mixed_z = torch.cat([z, aux_z], dim=0)
        bsz, seq_len, embed_dim = mixed_z.size()
        mask_cat = torch.cat([mask, mask], dim=0).reshape(bsz * seq_len)
        mixed_z = mixed_z.reshape(bsz * seq_len, embed_dim)
        mixed_z = mixed_z[mask_cat]

        sampled_token_latent = model.flow_loss.sample(mixed_z, cfg)
        sampled_token_latent, _ = sampled_token_latent.chunk(2, dim=0)
        mask_half, _ = mask_cat.chunk(2, dim=0)
        x_out = x.reshape(bsz // 2 * seq_len, model.token_embed_dim)
        x_out[mask_half.reshape(bsz // 2 * seq_len)] = sampled_token_latent
        sampled_token_latent = x_out.reshape(bsz // 2, seq_len, model.token_embed_dim)

        uncond_output[0] = None  # reset for next call
        return sampled_token_latent

    model.forward_with_cfg = intervened_forward_with_cfg
    return orig_forward_with_cfg  # return for restoration


def build_intervention_audit(family):
    audit = {
        "family": family,
        "hook_call_counts": {},
        "replacement_checks": {},
    }
    if family in ("ca", "sa"):
        audit["hook_call_counts"] = {"scale_hook": 0}
        audit["replacement_checks"] = {"not_applicable": True}
    elif family in ("cfg_ca", "cfg_sa"):
        audit["hook_call_counts"] = {
            "forward_with_cfg": 0,
            "capture_hook": 0,
            "replace_hook": 0,
        }
        audit["replacement_checks"] = {
            "captured_uncond": 0,
            "replaced_cond": 0,
            "missed_replacement": 0,
            "shape_mismatch": 0,
            "last_uncond_shape": None,
            "last_cond_shape": None,
        }
        audit["mixer_checks"] = {
            "applied": 0,
            "last_mixer": None,
            "last_gate_mean": None,
            "last_stats": {},
            "trace": [],
        }
    return audit


def validate_intervention_audit(family, audit):
    failures = []
    if family in ("ca", "sa"):
        if audit["hook_call_counts"].get("scale_hook", 0) <= 0:
            failures.append("Intervention hook did not run: scale_hook count is zero")
    elif family in ("cfg_ca", "cfg_sa"):
        checks = audit["replacement_checks"]
        if audit["hook_call_counts"].get("forward_with_cfg", 0) <= 0:
            failures.append("CFG intervention did not run: forward_with_cfg count is zero")
        if checks.get("captured_uncond", 0) <= 0:
            failures.append("CFG intervention did not capture unconditional attention output")
        if checks.get("replaced_cond", 0) <= 0:
            failures.append("CFG intervention did not replace conditional attention output")
        if checks.get("shape_mismatch", 0) > 0:
            failures.append("CFG replacement shape mismatch occurred")
        if audit.get("mixer_checks", {}).get("applied", 0) <= 0:
            failures.append("CFG residual mixer did not run")
    return failures


def apply_intervention(model, family, layer_idx, alpha, args, audit):
    """
    Apply attention intervention to the model.
    
    Returns:
        handles: list of hook handles or original functions for restoration.
    """
    if family == "baseline":
        return []

    if family in ("ca", "sa"):
        attn_module = _get_attn_module(model, family, layer_idx)

        def scale_hook(module, input, output):
            audit["hook_call_counts"]["scale_hook"] += 1
            if isinstance(output, tuple):
                return (output[0] * alpha,) + output[1:]
            return output * alpha

        handle = attn_module.register_forward_hook(scale_hook)
        return [handle]

    elif family in ("cfg_ca", "cfg_sa"):
        # Note: cfg_scale is NOT used for the attention replacement itself --
        # it replaces the --cfg argument passed to sample_tokens (flow mixing).
        orig_fwd = _apply_cfg_intervention(
            model,
            family,
            layer_idx,
            audit,
            _build_cfg_mixer_config(args),
        )
        return [orig_fwd]

    else:
        raise ValueError(f"Unknown family: {family}")


def remove_intervention(model, family, handles):
    """Remove intervention hooks and restore model state."""
    if family == "baseline" or not handles:
        return
    if family in ("ca", "sa"):
        for h in handles:
            h.remove()
    elif family in ("cfg_ca", "cfg_sa"):
        # handles[0] is the original forward_with_cfg
        model.forward_with_cfg = handles[0]


def patch_sample_tokens_cfg_schedule(model, args, audit):
    audit["active"] = True
    original_sample_tokens = model.sample_tokens
    interval = args._cfg_schedule_interval
    table = args._cfg_schedule_table

    def sample_tokens_scheduled(bsz, m_lens, cfg=1.0, cfg_schedule="linear", labels=None, temperature=1.0, device="cuda", acc_ratio=1):
        m_lens = m_lens // model.unit_length
        seq_len = model.seq_len
        steps = int(seq_len // acc_ratio)
        key_padding_mask = ~model.__class__.__dict__["sample_tokens"].__globals__["lengths_to_mask"](m_lens, seq_len).to(device)
        latents = torch.where(
            key_padding_mask.unsqueeze(-1),
            torch.zeros(bsz, seq_len, model.token_embed_dim).to(device),
            model.mask_token.repeat(bsz, seq_len, 1),
        )
        masked_rand_schedule = torch.where(key_padding_mask, 1e5, torch.rand_like(key_padding_mask, dtype=torch.float))

        for timestep in torch.linspace(0, 1, steps, device=device):
            rand_mask_prob = torch.cos(timestep * math.pi * 0.5)
            num_masked = torch.round(rand_mask_prob * m_lens).clamp(min=1)
            sorted_indices = masked_rand_schedule.argsort(dim=1)
            ranks = sorted_indices.argsort(dim=1)
            is_mask = ranks < num_masked.unsqueeze(-1)
            latents_masked = torch.where(is_mask.unsqueeze(-1), model.mask_token.repeat(bsz, seq_len, 1), latents)

            cfg_iter, alpha_t = scheduled_cfg_scale(
                cfg,
                args.cfg_schedule,
                timestep,
                args.cfg_schedule_decay,
                interval,
                table,
                args.cfg_alpha_scale,
            )
            audit["call_count"] += 1
            audit["min_cfg"] = cfg_iter if audit["min_cfg"] is None else min(audit["min_cfg"], cfg_iter)
            audit["max_cfg"] = cfg_iter if audit["max_cfg"] is None else max(audit["max_cfg"], cfg_iter)
            if len(audit["trace"]) < 200:
                audit["trace"].append(
                    {
                        "progress": float(timestep.detach().item()),
                        "alpha_t": float(alpha_t),
                        "cfg_scale": float(cfg_iter),
                    }
                )

            sampled_tokens = model.forward_with_cfg(
                latents_masked,
                labels,
                is_mask,
                key_padding_mask=key_padding_mask,
                cfg=cfg_iter,
                temperature=temperature,
            )
            latents = torch.where(is_mask.unsqueeze(-1), sampled_tokens, latents_masked)
            masked_rand_schedule = masked_rand_schedule.masked_fill(~is_mask, 1e5)

        return torch.where(key_padding_mask.unsqueeze(-1), torch.zeros_like(latents), latents)

    model.sample_tokens = sample_tokens_scheduled
    return original_sample_tokens


def restore_sample_tokens_cfg_schedule(model, original_sample_tokens):
    if original_sample_tokens is not None:
        model.sample_tokens = original_sample_tokens


# ---------------------------------------------------------------------------
# Evaluation runner
# ---------------------------------------------------------------------------

def run_eval(args):
    """Run official eval_molingo_ms with attention intervention applied."""
    started = time.time()
    repo_dir = Path(args.repo_dir).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    family = args.family
    layer_idx = parse_layer(args.layer) if family != "baseline" else -1
    alpha = args.alpha
    cfg_eval = (args.cfg_scale if args.cfg_scale is not None else args.cfg) if family in ("cfg_ca", "cfg_sa") else args.cfg
    interval_values = parse_float_list(args.cfg_schedule_interval)
    if len(interval_values) != 2:
        raise ValueError("--cfg_schedule_interval must contain exactly two comma-separated floats")
    args._cfg_schedule_interval = (interval_values[0], interval_values[1])
    args._cfg_schedule_table = parse_float_list(args.cfg_schedule_table)

    device = "cuda"
    fixseed(args.seed)

    failures = []
    metrics = {}
    log_file = out_dir / "eval_stdout_stderr.log"

    # ---- Load everything ----
    try:
        print(f"[Eval] Loading MoLingo model from {repo_dir}...")
        model, vae_model, model_opt, vae_opt, unit_length = load_molingo_model(
            repo_dir, args.dim_pose, device, args.sample_steps, args.t5_path
        )

        actual_layers = len(model.seqTransDecoder.layers)
        if family != "baseline" and layer_idx >= actual_layers:
            raise ValueError(f"Layer {layer_idx} out of range (0-{actual_layers-1})")

        print(f"[Eval] Loading dataset from {args.data_src}...")
        test_dataset, test_loader = load_dataset(
            repo_dir, args.dim_pose, args.data_src, model_opt, unit_length
        )

        print(f"[Eval] Loading MS evaluators...")
        textencoder, motionencoder = load_ms_evaluators(device=device)
    except Exception as exc:
        import traceback
        traceback.print_exc()
        failures.append(f"Setup failed: {exc}")
        _write_failure_manifest(args, out_dir, failures, time.time() - started)
        return 2

    # ---- Apply intervention ----
    handles = []
    intervention_audit = build_intervention_audit(family)
    cfg_schedule_audit = {"active": None, "call_count": 0, "min_cfg": None, "max_cfg": None, "trace": []}
    original_sample_tokens = None
    if family != "baseline":
        print(f"[Eval] Applying {family} intervention at layer {layer_idx}, alpha={alpha}, cfg_eval={cfg_eval}")
        handles = apply_intervention(model, family, layer_idx, alpha, args, intervention_audit)
    original_sample_tokens = patch_sample_tokens_cfg_schedule(model, args, cfg_schedule_audit)

    # ---- Run evaluation ----
    try:
        print(f"[Eval] Running eval_molingo_ms (cfg={cfg_eval}, acc={args.acc}, repeat={args.repeat})...")

        fid_list, top1_list, top2_list, top3_list, ms_list = [], [], [], [], []

        for rt in range(args.repeat):
            tmp_fid, tmp_top1, tmp_top2, tmp_top3, tmp_ms = eval_molingo_ms(
                test_loader, model, vae_model,
                ep=rt, cfg=cfg_eval,
                motionencoder=motionencoder, textencoder=textencoder,
                std_factor=model_opt.std_factor, acc_ratio=args.acc
            )
            fid_list.append(tmp_fid)
            top1_list.append(tmp_top1)
            top2_list.append(tmp_top2)
            top3_list.append(tmp_top3)
            ms_list.append(tmp_ms)

        fid_arr = np.array(fid_list)
        top1_arr = np.array(top1_list)
        top2_arr = np.array(top2_list)
        top3_arr = np.array(top3_list)
        ms_arr = np.array(ms_list)

        metrics = {
            "fid_tmr": float(np.mean(fid_arr)),
            "fid_tmr_std": float(np.std(fid_arr)),
            "top1": float(np.mean(top1_arr)),
            "top2": float(np.mean(top2_arr)),
            "top3": float(np.mean(top3_arr)),
            "matching_score": float(np.mean(ms_arr)),
            "repeat": args.repeat,
        }
        print(f"[Eval] Metrics: {json.dumps(metrics)}")
    except Exception as exc:
        failures.append(f"Eval failed: {exc}")
        import traceback
        traceback.print_exc()
    finally:
        remove_intervention(model, family, handles)
        restore_sample_tokens_cfg_schedule(model, original_sample_tokens)

    failures.extend(validate_intervention_audit(family, intervention_audit))

    # ---- Write outputs ----
    metrics_file = out_dir / "metrics_summary.json"
    write_json(metrics_file, metrics)

    elapsed = time.time() - started

    manifest = _build_manifest(args, repo_dir, out_dir, family, layer_idx,
                               alpha, cfg_eval, metrics, failures, elapsed,
                               actual_layers, model_opt, vae_opt,
                               unit_length, intervention_audit, cfg_schedule_audit)
    manifest_path = out_dir / "manifest.json"
    write_json(manifest_path, manifest)

    print(json.dumps({"manifest": str(manifest_path), "metrics_summary": str(metrics_file),
                      "metrics": metrics, "failures": failures, "elapsed_sec": elapsed},
                     indent=2))

    return 2 if failures else 0


def _build_manifest(args, repo_dir, out_dir, family, layer_idx, alpha, cfg_eval,
                    metrics, failures, elapsed, actual_layers, model_opt,
                    vae_opt, unit_length, intervention_audit, cfg_schedule_audit):
    command_script = os.environ.get("MODEBUG_COMMAND_SCRIPT", "")
    dataset = "ms" if args.dim_pose == 272 else "t2m"
    model_dir = repo_dir / "mogen" / "checkpoints" / dataset / f"pretrained_model_{args.dim_pose}"
    model_ckpt = model_dir / "net_best_fid.pth"
    vae_opt_path = repo_dir / "mogen" / "checkpoints" / dataset / model_opt.vae / "opt.txt"
    vae_ckpt = repo_dir / "mogen" / "checkpoints" / dataset / model_opt.vae / "model" / "net_best_fid.ckpt"
    manifest = {
        "baseline": BASELINE_NAME,
        "trace": TRACE,
        "scope": f"full_official_evaluator_{family}" + (f"_layer_{layer_idx}" if family != "baseline" else ""),
        "paper_level_status": "full_evaluator_metrics_computed" if not failures else "failed",
        "created_at": now_iso(),
        "repo_dir": str(repo_dir),
        "git_head": run_git(["git", "rev-parse", "HEAD"], repo_dir),
        "git_branch": run_git(["git", "branch", "--show-current"], repo_dir),
        "git_status_short": run_git(["git", "status", "--short"], repo_dir).splitlines(),
        "command": " ".join(sys.argv),
        "wrapper_script": file_record(Path(__file__)),
        "command_script": file_record(command_script) if command_script else {"path": "", "sha256": None},
        "deployed_from": os.environ.get("MODEBUG_DEPLOYED_FROM", ""),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        "gpu_id": args.gpu_id,
        "environment": os.environ.get("CONDA_DEFAULT_ENV", "unknown"),
        "family": family,
        "layer": layer_idx if family != "baseline" else None,
        "native_decoder_layers": actual_layers,
        "intervention": {},
        "hook_call_counts": intervention_audit["hook_call_counts"],
        "replacement_checks": intervention_audit["replacement_checks"],
        "mixer_checks": intervention_audit.get("mixer_checks", {}),
        "cfg_schedule": {
            "status": "diagnostic_run_level_schedule",
            "schedule": args.cfg_schedule,
            "base_cfg_scale": cfg_eval,
            "decay": args.cfg_schedule_decay,
            "interval": list(args._cfg_schedule_interval),
            "table": args._cfg_schedule_table,
            "alpha_scale": args.cfg_alpha_scale,
            "deprecated_cfg_layer_alpha_alias": args.cfg_layer_alpha,
            "definition": "effective_cfg = 1 + (base_cfg - 1) * alpha_scale * alpha_t(step)",
            "limitation": "MoLingo applies CFG in flow_loss.sample after forward_z; this is a denoising-step schedule for selected-layer diagnostic runs, not a true layer-local CFG mixer.",
            "runtime_audit": cfg_schedule_audit,
        },
        "eval_settings": {
            "dim_pose": args.dim_pose,
            "cfg": cfg_eval,
            "sample_steps": args.sample_steps,
            "acc": args.acc,
            "repeat": args.repeat,
            "seed": args.seed,
            "unit_length": unit_length,
            "unit_length_source": "int(2 ** vae_opt.down_t), matching MoLingo/mogen/eval_mogen.py",
            "vae_down_t": vae_opt.down_t,
        },
        "official_protocol": {
            "source": "MoLingo/mogen/eval_mogen.py",
            "dataset_class": "Text2MotionDatasetMS",
            "evaluator": "mogen.core.eval.eval_molingo_ms",
            "batch_size": 32,
            "drop_last": True,
            "shuffle": True,
            "num_workers": 4,
        },
        "artifacts": {
            "model_opt": file_record(model_dir / "opt.txt"),
            "model_checkpoint": file_record(model_ckpt),
            "vae_opt": file_record(vae_opt_path),
            "vae_checkpoint": file_record(vae_ckpt),
        },
        "data_src": args.data_src,
        "t5_path": args.t5_path,
        "log_file": str(out_dir / "eval_stdout_stderr.log"),
        "metrics_file": str(out_dir / "metrics_summary.json"),
        "metrics_summary_sha256": sha256(out_dir / "metrics_summary.json"),
        "metrics": metrics,
        "failures": failures,
        "elapsed_sec": elapsed,
    }

    if family in ("ca", "sa"):
        manifest["intervention"] = {
            "type": "attention_output_scaling",
            "target": "self_attn" if family == "sa" else "multihead_attn",
            "layer_idx": layer_idx,
            "alpha": alpha,
        }
    elif family in ("cfg_ca", "cfg_sa"):
        manifest["intervention"] = {
            "type": "cfg_attention_residual_mixer",
            "target": "self_attn" if family == "cfg_sa" else "multihead_attn",
            "layer_idx": layer_idx,
            "mechanism": args.cfg_residual_mixer,
            "mechanism_description": "mix cond/uncond target-layer attention outputs before MoLingo flow-space CFG sampling",
            "residual_alpha": args.cfg_residual_alpha,
            "parallel_scale": args.cfg_residual_parallel_scale,
            "orthogonal_scale": args.cfg_residual_orthogonal_scale,
            "norm_ratio": args.cfg_residual_norm_ratio,
            "discrepancy_threshold": args.cfg_residual_discrepancy_threshold,
            "discrepancy_slope": args.cfg_residual_discrepancy_slope,
            "training_free": True,
            "cfg_scale": args.cfg_scale if args.cfg_scale is not None else args.cfg,
        }

    return manifest


def _write_failure_manifest(args, out_dir, failures, elapsed):
    manifest = {
        "baseline": BASELINE_NAME,
        "trace": TRACE,
        "paper_level_status": "failed",
        "created_at": now_iso(),
        "family": args.family,
        "failures": failures,
        "elapsed_sec": elapsed,
        "command": " ".join(sys.argv),
        "gpu_id": args.gpu_id,
    }
    write_json(out_dir / "manifest.json", manifest)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="MoLingo Trace 1 Full Eval with Attention Intervention")
    parser.add_argument("--repo_dir", default="/data/public/ripemangobox/Motion/MoLingo")
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--family", required=True, choices=FAMILIES)
    parser.add_argument("--layer", default="0", help="Layer index (0-15), ignored for baseline")
    parser.add_argument("--alpha", type=float, default=0.5, help="Scaling factor for ca/sa interventions")
    parser.add_argument("--cfg_scale", type=float, default=None, help="CFG scale for cfg_ca/cfg_sa (defaults to --cfg)")
    parser.add_argument(
        "--cfg_residual_mixer",
        default="replace",
        choices=["replace", "residual_gate", "apg_orthogonal", "norm_clamp", "stat_match", "discrepancy_gate"],
        help="Training-free cond/uncond attention residual mixer for cfg_ca/cfg_sa.",
    )
    parser.add_argument("--cfg_residual_alpha", type=float, default=1.0)
    parser.add_argument("--cfg_residual_parallel_scale", type=float, default=1.0)
    parser.add_argument("--cfg_residual_orthogonal_scale", type=float, default=0.0)
    parser.add_argument("--cfg_residual_norm_ratio", type=float, default=1.0)
    parser.add_argument("--cfg_residual_discrepancy_threshold", type=float, default=0.0)
    parser.add_argument("--cfg_residual_discrepancy_slope", type=float, default=8.0)
    parser.add_argument(
        "--cfg_schedule",
        default="constant",
        choices=["constant", "linear_increase", "linear_decay", "c2fg_decay", "inverse_decay", "interval", "scalar_table"],
    )
    parser.add_argument("--cfg_schedule_decay", type=float, default=1.0)
    parser.add_argument("--cfg_schedule_interval", default="0.25,0.75")
    parser.add_argument("--cfg_schedule_table", default="")
    parser.add_argument("--cfg_alpha_scale", type=float, default=1.0)
    parser.add_argument("--cfg_layer_alpha", type=float, default=None, help="Deprecated alias for --cfg_alpha_scale.")
    parser.add_argument("--gpu_id", type=int, default=0)
    parser.add_argument("--data_src", default="/data/public/ripemangobox/Motion/datasets/272-dim-HumanML3D")
    parser.add_argument("--dim_pose", type=int, default=272)
    parser.add_argument("--cfg", type=float, default=5.5, help="Base CFG scale for flow mixing")
    parser.add_argument("--sample_steps", type=int, default=32)
    parser.add_argument("--acc", type=int, default=3)
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--seed", type=int, default=3407)
    parser.add_argument("--t5_path", default="/data/public/ripemangobox/Motion/Text-encoder/t5-large")
    args = parser.parse_args()
    if args.cfg_layer_alpha is not None:
        args.cfg_alpha_scale = args.cfg_layer_alpha

    # Gate check
    if os.environ.get("MODEBUG_DS_APPROVED_EXECUTE") != "1":
        out_dir = Path(args.out_dir).expanduser().resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        failures = [
            "Formal MoLingo evaluator blocked: MODEBUG_DS_APPROVED_EXECUTE=1 is required."
        ]
        _write_failure_manifest(args, out_dir, failures, 0.0)
        print(json.dumps({"manifest": str(out_dir / "manifest.json"), "failures": failures}, indent=2))
        return 2

    # Validate layer
    if args.family != "baseline":
        layer_idx = parse_layer(args.layer)
        if layer_idx < 0 or layer_idx >= NATIVE_DECODER_LAYERS:
            out_dir = Path(args.out_dir).expanduser().resolve()
            out_dir.mkdir(parents=True, exist_ok=True)
            failures = [f"Layer {layer_idx} out of range [0, {NATIVE_DECODER_LAYERS - 1}]"]
            _write_failure_manifest(args, out_dir, failures, 0.0)
            print(json.dumps({"manifest": str(out_dir / "manifest.json"), "failures": failures}, indent=2))
            return 2

    # Skip if manifest exists (idempotent)
    out_dir = Path(args.out_dir).expanduser().resolve()
    manifest_path = out_dir / "manifest.json"
    if manifest_path.exists():
        existing = json.loads(manifest_path.read_text())
        if existing.get("paper_level_status") == "full_evaluator_metrics_computed":
            print(f"[Eval] Skipping existing completed run: {manifest_path}")
            return 0

    return run_eval(args)


if __name__ == "__main__":
    raise SystemExit(main())
