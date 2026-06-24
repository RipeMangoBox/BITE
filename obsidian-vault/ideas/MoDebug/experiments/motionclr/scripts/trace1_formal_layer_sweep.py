#!/usr/bin/env python
import argparse
import hashlib
import json
import os
import random
import subprocess
import sys
import time
from contextlib import contextmanager
from os.path import join as pjoin

import numpy as np
import torch
import yaml
from accelerate.utils import set_seed
from box import Box


def run(cmd, cwd):
    return subprocess.run(
        cmd, cwd=cwd, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).stdout.strip()


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def yaml_to_box(path):
    with open(path, "r") as f:
        return Box(yaml.safe_load(f))


def parse_options(repo_dir, opt_path, gpu_id, steps, seed, no_fp16):
    sys.path.insert(0, repo_dir)
    from options.generate_options import GenerateOptions

    old_argv = sys.argv[:]
    try:
        sys.argv = [
            "trace1_formal_layer_sweep.py",
            "--opt_path",
            opt_path,
            "--gpu_id",
            str(gpu_id),
            "--num_inference_steps",
            str(steps),
            "--seed",
            str(seed),
            "--no_eff",
            "--self_attention",
        ]
        if no_fp16:
            sys.argv.append("--no_fp16")
        return GenerateOptions().parse()
    finally:
        sys.argv = old_argv


def layer_map(model):
    layers = []
    for name, module in model.unet.named_modules():
        if module.__class__.__name__ == "CLRBlock":
            layers.append(
                {
                    "layer_id": len(layers),
                    "module": "unet." + name,
                    "cross_attention_module": "unet." + name + ".clr_attn.cross_attention",
                    "cross_attention_class": module.clr_attn.cross_attention.__class__.__name__,
                    "has_self_attention": bool(getattr(module.clr_attn, "self_attn_use", False)),
                }
            )
    return layers


def modules_by_unet_name(model):
    return dict(model.unet.named_modules())


@contextmanager
def scaled_ca_outputs(model, layer_ids, alpha):
    modules = modules_by_unet_name(model)
    mapping = layer_map(model)
    patched = []
    call_counts = {str(layer_id): 0 for layer_id in layer_ids}
    for item in mapping:
        layer_id = item["layer_id"]
        if layer_id not in layer_ids:
            continue
        clr_name = item["module"].replace("unet.", "", 1)
        ca = modules[clr_name].clr_attn.cross_attention
        old_forward = ca.forward

        def make_forward(forward_fn, lid):
            def forward_scaled(x, xf):
                call_counts[str(lid)] += 1
                return forward_fn(x, xf) * alpha

            return forward_scaled

        ca.forward = make_forward(old_forward, layer_id)
        patched.append((ca, old_forward))
    try:
        yield call_counts
    finally:
        for ca, old_forward in patched:
            ca.forward = old_forward


@contextmanager
def replace_cond_half_with_uncond_hidden(model, layer_ids, enabled=True):
    modules = modules_by_unet_name(model)
    mapping = layer_map(model)
    patched = []
    call_counts = {str(layer_id): 0 for layer_id in layer_ids}
    replacement_checks = []
    for item in mapping:
        layer_id = item["layer_id"]
        if layer_id not in layer_ids:
            continue
        clr_name = item["module"].replace("unet.", "", 1)
        block = modules[clr_name]
        old_forward = block.forward

        def make_forward(forward_fn, lid):
            def forward_replaced(x, t, cond, cond_indices=None):
                out = forward_fn(x, t, cond, cond_indices)
                call_counts[str(lid)] += 1
                if not enabled:
                    return out
                if out.shape[0] % 2 != 0:
                    raise RuntimeError(f"Layer {lid} output batch is not even: {tuple(out.shape)}")
                half = out.shape[0] // 2
                before = (out[:half] - out[half:]).detach().abs().max().item()
                new_out = out.clone()
                new_out[:half] = out[half:].clone()
                after = (new_out[:half] - new_out[half:]).detach().abs().max().item()
                replacement_checks.append(
                    {"layer_id": lid, "shape": list(out.shape), "max_abs_before": before, "max_abs_after": after}
                )
                return new_out

            return forward_replaced

        block.forward = make_forward(old_forward, layer_id)
        patched.append((block, old_forward))
    try:
        yield call_counts, replacement_checks
    finally:
        for block, old_forward in patched:
            block.forward = old_forward


def forward_cfg(model, x, timesteps, enc_text, cfg_scale):
    if model.training:
        raise RuntimeError("Trace 1 formal CFG sweep requires eval mode; dropout/cond masking must be disabled.")
    bsz, frames, _ = x.shape
    x_in = x.transpose(1, 2)
    cond_indices = torch.arange(bsz, device=x_in.device)
    padding_needed = (16 - (frames % 16)) % 16
    x_in = torch.nn.functional.pad(x_in, (0, padding_needed), value=0)
    combined_x = torch.cat([x_in, x_in], dim=0)
    combined_t = torch.cat([timesteps, timesteps], dim=0)
    unet_out = model.unet(x=combined_x, t=combined_t, cond=enc_text, cond_indices=cond_indices)
    unet_out = unet_out[:, :, :frames].transpose(1, 2)
    out_cond, out_uncond = torch.split(unet_out, len(unet_out) // 2, dim=0)
    pre_cfg_max_abs = (out_cond - out_uncond).detach().abs().max().item()
    cfg_out = out_uncond + cfg_scale * (out_cond - out_uncond)
    return cfg_out, {"pre_cfg_max_abs_cond_minus_uncond": pre_cfg_max_abs}


def generate_batch(model, scheduler, device, dtype, captions, motion_lens, steps, cfg_scale):
    bsz = len(captions)
    max_frames = int(max(motion_lens))
    sample = torch.randn((bsz, max_frames, model.input_feats), device=device, dtype=dtype)
    scheduler.set_timesteps(steps, device)
    enc_text = model.encode_text(captions, device)
    step_stats = []
    for raw_t in scheduler.timesteps:
        t = torch.tensor([raw_t] * bsz, device=device).long()
        with torch.no_grad():
            pred, stats = forward_cfg(model, sample, t, enc_text, cfg_scale)
        step_stats.append(stats)
        sample = scheduler.step(pred, t[0], sample).prev_sample
    return [sample[i, : int(motion_lens[i])].detach().cpu().numpy() for i in range(bsz)], step_stats


def generate_variant(model, scheduler, device, dtype, texts, lens, batch_size, seed, steps, cfg_scale):
    set_seed(seed)
    arrays = []
    all_step_stats = []
    for start in range(0, len(texts), batch_size):
        batch_texts = texts[start : start + batch_size]
        batch_lens = lens[start : start + batch_size]
        batch_arrays, step_stats = generate_batch(
            model, scheduler, device, dtype, batch_texts, batch_lens, steps, cfg_scale
        )
        arrays.extend(batch_arrays)
        all_step_stats.extend(step_stats)
    return arrays, all_step_stats


def read_caption(text_path):
    fallback = None
    with open(text_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            parts = line.strip().split("#")
            if not parts or not parts[0]:
                continue
            fallback = fallback or parts[0]
            if len(parts) >= 4:
                try:
                    start = float(parts[2])
                    end = float(parts[3])
                except ValueError:
                    continue
                if start == 0.0 and end == 0.0:
                    return parts[0]
    return fallback


def motion_unit_length(opt):
    return int(getattr(opt, "unit_length", 4))


def max_motion_length(opt):
    return int(getattr(opt, "max_motion_length", 196))


def load_prompts(args, opt):
    if args.prompt_file:
        with open(args.prompt_file, "r") as f:
            texts = [line.strip() for line in f if line.strip()]
        if args.lens_file:
            with open(args.lens_file, "r") as f:
                lens = [int(line.strip()) for line in f if line.strip()]
        else:
            lens = [max_motion_length(opt) for _ in texts]
        rows = [{"source": args.prompt_file, "caption": t, "motion_len": int(l)} for t, l in zip(texts, lens)]
        return rows[: args.prompt_limit]

    data_root = pjoin(args.repo_dir, "data", "HumanML3D")
    with open(pjoin(data_root, args.split + ".txt"), "r") as f:
        ids = [line.strip() for line in f if line.strip()]
    rng = random.Random(args.prompt_seed)
    rng.shuffle(ids)
    rows = []
    unit_length = motion_unit_length(opt)
    min_len = 10 * unit_length
    max_len = max_motion_length(opt)
    for sample_id in ids:
        motion_path = pjoin(data_root, "new_joint_vecs", sample_id + ".npy")
        text_path = pjoin(data_root, "texts", sample_id + ".txt")
        if not os.path.exists(motion_path) or not os.path.exists(text_path):
            continue
        motion = np.load(motion_path)
        if len(motion) < min_len or len(motion) >= 200:
            continue
        caption = read_caption(text_path)
        if not caption:
            continue
        motion_len = (len(motion) // unit_length) * unit_length
        motion_len = max(min_len, min(motion_len, max_len))
        rows.append(
            {
                "source": "HumanML3D/" + args.split,
                "sample_id": sample_id,
                "caption": caption,
                "motion_len": int(motion_len),
                "raw_motion_len": int(len(motion)),
            }
        )
        if len(rows) >= args.prompt_limit:
            break
    if len(rows) < args.prompt_limit:
        raise RuntimeError(f"Only found {len(rows)} valid prompts, requested {args.prompt_limit}")
    return rows


def save_arrays(out_dir, seed, variant, arrays):
    variant_dir = pjoin(out_dir, "outputs", f"seed_{seed}", variant)
    os.makedirs(variant_dir, exist_ok=True)
    files = []
    for idx, arr in enumerate(arrays):
        path = pjoin(variant_dir, f"raw_{idx:03}.npy")
        np.save(path, arr)
        files.append({"path": path, "sha256": sha256(path), "shape": list(arr.shape)})
    return files


def diff_stats(arrays, baseline):
    diffs = [a - b for a, b in zip(arrays, baseline)]
    flat = np.concatenate([d.reshape(-1) for d in diffs])
    return {
        "l2_vs_baseline": float(np.linalg.norm(flat)),
        "max_abs_vs_baseline": float(np.abs(flat).max()),
        "mean_abs_vs_baseline": float(np.abs(flat).mean()),
        "allclose_vs_baseline": bool(all(np.allclose(a, b, rtol=0, atol=0) for a, b in zip(arrays, baseline))),
    }


def max_pre_cfg_delta(step_stats):
    if not step_stats:
        return None
    return float(max(item["pre_cfg_max_abs_cond_minus_uncond"] for item in step_stats))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo_dir", default="/data/public/ripemangobox/Motion/MotionCLR")
    parser.add_argument("--out_dir", required=True)
    parser.add_argument(
        "--run_scope",
        default="formal_diagnostic_layer_sweep",
        choices=["formal_diagnostic_layer_sweep", "dev_validation_only"],
    )
    parser.add_argument("--opt_path", default="./checkpoints/t2m/release/opt.txt")
    parser.add_argument("--prompt_file", default="")
    parser.add_argument("--lens_file", default="")
    parser.add_argument("--split", default="test")
    parser.add_argument("--prompt_limit", type=int, default=5)
    parser.add_argument("--prompt_seed", type=int, default=0)
    parser.add_argument("--seeds", default="0,1,2")
    parser.add_argument("--num_inference_steps", type=int, default=10)
    parser.add_argument("--gpu_id", type=int, default=0)
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--cfg_scale", type=float, default=2.5)
    parser.add_argument("--ca_alpha", type=float, default=0.0)
    parser.add_argument("--no_fp16", action="store_true")
    parser.add_argument("--all_layer_tol", type=float, default=1e-5)
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    os.chdir(args.repo_dir)
    sys.path.insert(0, args.repo_dir)

    from models import build_models
    from models.gaussian_diffusion import DiffusePipeline
    from utils.model_load import load_model_weights

    seeds = [int(item) for item in args.seeds.split(",") if item.strip()]
    first_seed = seeds[0]
    device = torch.device(f"cuda:{args.gpu_id}" if torch.cuda.is_available() else "cpu")
    opt = parse_options(args.repo_dir, args.opt_path, args.gpu_id, args.num_inference_steps, first_seed, args.no_fp16)
    opt.device = device
    edit_config = yaml_to_box("options/noedit.yaml")
    set_seed(first_seed)
    model = build_models(opt, edit_config=edit_config, out_path=args.out_dir)
    ckpt_path = pjoin(opt.model_dir, opt.which_ckpt + ".tar")
    total_it = load_model_weights(model, ckpt_path, use_ema=not opt.no_ema)
    pipeline = DiffusePipeline(
        opt=opt,
        model=model,
        diffuser_name=opt.diffuser_name,
        device=device,
        num_inference_steps=args.num_inference_steps,
        torch_dtype=torch.float32 if args.no_fp16 else torch.float16,
    )
    model = pipeline.model
    dtype = pipeline.torch_dtype
    model.eval()

    mapping = layer_map(model)
    if len(mapping) != 18:
        raise RuntimeError(f"Expected exactly 18 CLRBlock layers, found {len(mapping)}")
    with open(pjoin(args.out_dir, "layer_mapping.json"), "w") as f:
        json.dump(mapping, f, indent=2)

    prompt_rows = load_prompts(args, opt)
    texts = [row["caption"] for row in prompt_rows]
    lens = [row["motion_len"] for row in prompt_rows]
    with open(pjoin(args.out_dir, "prompt_set.json"), "w") as f:
        json.dump(prompt_rows, f, indent=2)

    started = time.time()
    summary = []
    outputs = {}
    failures = []
    all_layers = [item["layer_id"] for item in mapping]

    for seed in seeds:
        seed_key = f"seed_{seed}"
        outputs[seed_key] = {}
        baseline, baseline_step_stats = generate_variant(
            model, pipeline.scheduler, device, dtype, texts, lens, args.batch_size, seed, args.num_inference_steps, args.cfg_scale
        )
        outputs[seed_key]["baseline"] = save_arrays(args.out_dir, seed, "baseline", baseline)
        summary.append(
            {
                "seed": seed,
                "family": "baseline",
                "variant": "baseline",
                "num_outputs": len(baseline),
                "max_pre_cfg_delta": max_pre_cfg_delta(baseline_step_stats),
            }
        )

        with scaled_ca_outputs(model, all_layers, 1.0) as counts:
            arrays, step_stats = generate_variant(
                model, pipeline.scheduler, device, dtype, texts, lens, args.batch_size, seed, args.num_inference_steps, args.cfg_scale
            )
        variant = "noop_ca_all_layers_alpha_1"
        outputs[seed_key][variant] = save_arrays(args.out_dir, seed, variant, arrays)
        stats = diff_stats(arrays, baseline)
        summary.append(
            {
                "seed": seed,
                "family": "noop",
                "variant": variant,
                "layers": all_layers,
                "hook_call_counts": counts,
                "max_pre_cfg_delta": max_pre_cfg_delta(step_stats),
                **stats,
            }
        )
        if not stats["allclose_vs_baseline"]:
            failures.append(f"{variant} seed {seed} is not exactly equal to baseline")

        with replace_cond_half_with_uncond_hidden(model, all_layers, enabled=False) as (counts, checks):
            arrays, step_stats = generate_variant(
                model, pipeline.scheduler, device, dtype, texts, lens, args.batch_size, seed, args.num_inference_steps, args.cfg_scale
            )
        variant = "noop_hidden_hook_all_layers_disabled"
        outputs[seed_key][variant] = save_arrays(args.out_dir, seed, variant, arrays)
        stats = diff_stats(arrays, baseline)
        summary.append(
            {
                "seed": seed,
                "family": "noop",
                "variant": variant,
                "layers": all_layers,
                "hook_call_counts": counts,
                "replacement_checks": checks,
                "max_pre_cfg_delta": max_pre_cfg_delta(step_stats),
                **stats,
            }
        )
        if not stats["allclose_vs_baseline"]:
            failures.append(f"{variant} seed {seed} is not exactly equal to baseline")

        with scaled_ca_outputs(model, all_layers, args.ca_alpha) as counts:
            arrays, step_stats = generate_variant(
                model, pipeline.scheduler, device, dtype, texts, lens, args.batch_size, seed, args.num_inference_steps, args.cfg_scale
            )
        variant = "positive_control_ca_all_layers_alpha_" + str(args.ca_alpha).replace(".", "p")
        outputs[seed_key][variant] = save_arrays(args.out_dir, seed, variant, arrays)
        summary.append(
            {
                "seed": seed,
                "family": "positive_control",
                "variant": variant,
                "layers": all_layers,
                "alpha": args.ca_alpha,
                "hook_call_counts": counts,
                "max_pre_cfg_delta": max_pre_cfg_delta(step_stats),
                **diff_stats(arrays, baseline),
            }
        )

        with replace_cond_half_with_uncond_hidden(model, all_layers, enabled=True) as (counts, checks):
            arrays, step_stats = generate_variant(
                model, pipeline.scheduler, device, dtype, texts, lens, args.batch_size, seed, args.num_inference_steps, args.cfg_scale
            )
        variant = "positive_control_hidden_replace_all_layers"
        outputs[seed_key][variant] = save_arrays(args.out_dir, seed, variant, arrays)
        max_delta = max_pre_cfg_delta(step_stats)
        summary.append(
            {
                "seed": seed,
                "family": "positive_control",
                "variant": variant,
                "layers": all_layers,
                "hook_call_counts": counts,
                "replacement_checks_tail": checks[-len(all_layers) :],
                "max_pre_cfg_delta": max_delta,
                **diff_stats(arrays, baseline),
            }
        )
        if max_delta is None or max_delta > args.all_layer_tol:
            failures.append(f"{variant} seed {seed} pre-CFG cond/uncond delta {max_delta} exceeds {args.all_layer_tol}")

        for layer_id in all_layers:
            with scaled_ca_outputs(model, [layer_id], args.ca_alpha) as counts:
                arrays, step_stats = generate_variant(
                    model,
                    pipeline.scheduler,
                    device,
                    dtype,
                    texts,
                    lens,
                    args.batch_size,
                    seed,
                    args.num_inference_steps,
                    args.cfg_scale,
                )
            variant = f"layer_{layer_id:02d}_ca_alpha_" + str(args.ca_alpha).replace(".", "p")
            outputs[seed_key][variant] = save_arrays(args.out_dir, seed, variant, arrays)
            summary.append(
                {
                    "seed": seed,
                    "family": "ca_output_perturbation",
                    "variant": variant,
                    "layer": layer_id,
                    "alpha": args.ca_alpha,
                    "hook_call_counts": counts,
                    "max_pre_cfg_delta": max_pre_cfg_delta(step_stats),
                    **diff_stats(arrays, baseline),
                }
            )

        for layer_id in all_layers:
            with replace_cond_half_with_uncond_hidden(model, [layer_id], enabled=True) as (counts, checks):
                arrays, step_stats = generate_variant(
                    model,
                    pipeline.scheduler,
                    device,
                    dtype,
                    texts,
                    lens,
                    args.batch_size,
                    seed,
                    args.num_inference_steps,
                    args.cfg_scale,
                )
            variant = f"layer_{layer_id:02d}_hidden_cond_to_uncond"
            outputs[seed_key][variant] = save_arrays(args.out_dir, seed, variant, arrays)
            summary.append(
                {
                    "seed": seed,
                    "family": "cfg_hidden_replacement",
                    "variant": variant,
                    "layer": layer_id,
                    "hook_call_counts": counts,
                    "replacement_checks_tail": checks[-1:],
                    "max_pre_cfg_delta": max_pre_cfg_delta(step_stats),
                    **diff_stats(arrays, baseline),
                }
            )

    summary_path = pjoin(args.out_dir, "summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    manifest = {
        "trace": "Trace 1",
        "line": "Line 1",
        "old_name": "Track B",
        "experiment_scope": args.run_scope,
        "paper_level_status": "not_final_full_evaluator_result",
        "ds_method_status": "METHOD_APPROVED_TO_IMPLEMENT",
        "repo_dir": args.repo_dir,
        "git_head": run(["git", "rev-parse", "HEAD"], args.repo_dir),
        "git_branch": run(["git", "branch", "--show-current"], args.repo_dir),
        "git_status_short": run(["git", "status", "--short"], args.repo_dir).splitlines(),
        "git_diff_stat": run(["git", "diff", "--stat"], args.repo_dir).splitlines(),
        "command": " ".join(sys.argv),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        "device": str(device),
        "torch_dtype": str(dtype),
        "model_training": bool(model.training),
        "cfg_cond_indices_policy": "explicit torch.arange(B), matching MotionCLR forward_with_cfg in eval mode",
        "checkpoint_path": ckpt_path,
        "checkpoint_sha256": sha256(ckpt_path),
        "opt_path": opt.opt_path,
        "opt_sha256": sha256(opt.opt_path),
        "layer_mapping_file": pjoin(args.out_dir, "layer_mapping.json"),
        "prompt_set_file": pjoin(args.out_dir, "prompt_set.json"),
        "num_layers": len(mapping),
        "motion_length_policy": {
            "unit_length": motion_unit_length(opt),
            "max_motion_length": max_motion_length(opt),
            "fallback_source": "MotionCLR Text2MotionDataset defaults when opt.txt omits unit_length",
        },
        "required_layer_groups": {
            "ca_output_perturbation": len(all_layers),
            "cfg_hidden_replacement": len(all_layers),
            "minimum_user_required_groups": 36,
        },
        "seeds": seeds,
        "prompt_limit": args.prompt_limit,
        "num_prompts": len(prompt_rows),
        "num_inference_steps": args.num_inference_steps,
        "batch_size": args.batch_size,
        "cfg_scale": args.cfg_scale,
        "ca_alpha": args.ca_alpha,
        "outputs": outputs,
        "summary_file": summary_path,
        "summary_sha256": sha256(summary_path),
        "failures": failures,
        "elapsed_sec": time.time() - started,
        "total_it": total_it,
        "limitations": [
            "This is the DS-approved implementation target for a formal diagnostic sweep.",
            "It is not a full benchmark evaluator result until official FID/R-Precision/Matching Score are computed.",
        ],
    }
    manifest_path = pjoin(args.out_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    with open(pjoin(args.out_dir, "NONFINAL_NOTICE.txt"), "w") as f:
        f.write(f"EXPERIMENT_SCOPE={args.run_scope}\n")
        if args.run_scope == "dev_validation_only":
            f.write("DEV_VALIDATION_ONLY=true\n")
        f.write("PAPER_LEVEL_STATUS=not_final_full_evaluator_result\n")
        f.write("DO_NOT_REPORT_AS_FULL_FORMAL_BENCHMARK=true\n")
    if failures:
        print(json.dumps({"manifest": manifest_path, "summary": summary_path, "failures": failures}, indent=2))
        raise SystemExit(2)
    print(json.dumps({"manifest": manifest_path, "summary": summary_path, "num_summary_rows": len(summary)}, indent=2))


if __name__ == "__main__":
    main()
