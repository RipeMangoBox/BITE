#!/usr/bin/env python
import argparse
import json
import os
import subprocess
import sys
from contextlib import contextmanager
from os.path import join as pjoin
from types import MethodType

import numpy as np
import torch
import yaml
from accelerate.utils import set_seed
from box import Box


def run(cmd, cwd):
    return subprocess.run(
        cmd,
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout.strip()


def sha256(path):
    out = run(["sha256sum", path], cwd=os.getcwd())
    return out.split()[0] if out else None


def yaml_to_box(path):
    with open(path, "r") as f:
        return Box(yaml.safe_load(f))


def read_opt_bool(opt_path, key):
    with open(opt_path, "r") as f:
        for line in f:
            prefix = key + ": "
            if line.startswith(prefix):
                return line.strip().split(": ", 1)[1] == "True"
    return False


def parse_motionclr_options(repo_dir, opt_path, gpu_id, steps, seed, no_fp16):
    sys.path.insert(0, repo_dir)
    from options.generate_options import GenerateOptions

    old_argv = sys.argv[:]
    try:
        sys.argv = [
            "track_b_ca_cfg_sweep.py",
            "--opt_path",
            opt_path,
            "--gpu_id",
            str(gpu_id),
            "--num_inference_steps",
            str(steps),
            "--seed",
            str(seed),
        ]
        if no_fp16:
            sys.argv.append("--no_fp16")
        if read_opt_bool(opt_path, "no_eff"):
            sys.argv.append("--no_eff")
        if read_opt_bool(opt_path, "self_attention"):
            sys.argv.append("--self_attention")
        return GenerateOptions().parse()
    finally:
        sys.argv = old_argv


def layer_map(model):
    layers = []
    for name, module in model.unet.named_modules():
        if module.__class__.__name__ == "CLRBlock":
            cross = module.clr_attn.cross_attention.__class__.__name__
            layers.append(
                {
                    "layer_id": len(layers),
                    "module": "unet." + name,
                    "clr_attn_module": "unet." + name + ".clr_attn",
                    "cross_attention_class": cross,
                    "has_self_attention": bool(getattr(module.clr_attn, "self_attn_use", False)),
                }
            )
    return layers


def patch_clr_layers(model, disabled_layer_ids):
    disabled = set(disabled_layer_ids)
    patched = []

    for layer in layer_map(model):
        if layer["layer_id"] not in disabled:
            continue
        module = dict(model.unet.named_modules())[layer["module"].replace("unet.", "", 1)]
        original_forward = module.forward

        def make_forward(mod, old_forward):
            def forward_layer_cond_off(self, x, t, cond, cond_indices=None):
                device = x.device if cond_indices is None else cond_indices.device
                empty = torch.empty(0, dtype=torch.long, device=device)
                return old_forward(x, t, cond, empty)

            return MethodType(forward_layer_cond_off, mod), old_forward

        module.forward, original_forward = make_forward(module, original_forward)
        module._track_b_original_forward = original_forward
        patched.append(module)
    return patched


def restore_patches(patched):
    for module in patched:
        module.forward = module._track_b_original_forward
        delattr(module, "_track_b_original_forward")


@contextmanager
def ca_disabled(model, layer_ids):
    patched = patch_clr_layers(model, layer_ids)
    try:
        yield
    finally:
        restore_patches(patched)


def generate_raw(pipeline, texts, motion_lens, batch_size):
    output, _ = pipeline.generate(texts, torch.LongTensor(motion_lens), batch_size=batch_size)
    return [x.detach().cpu().numpy() for x in output]


def summarize_variant(name, arrays, baseline_arrays):
    flat = np.concatenate([x.reshape(-1) for x in arrays])
    item = {
        "variant": name,
        "num_outputs": len(arrays),
        "mean": float(flat.mean()),
        "std": float(flat.std()),
        "l2_vs_baseline": None,
        "mean_abs_vs_baseline": None,
        "max_abs_vs_baseline": None,
    }
    if baseline_arrays is not None:
        diffs = [a - b for a, b in zip(arrays, baseline_arrays)]
        dflat = np.concatenate([d.reshape(-1) for d in diffs])
        item["l2_vs_baseline"] = float(np.linalg.norm(dflat))
        item["mean_abs_vs_baseline"] = float(np.abs(dflat).mean())
        item["max_abs_vs_baseline"] = float(np.abs(dflat).max())
    return item


def save_outputs(out_dir, variant, arrays):
    variant_dir = pjoin(out_dir, "outputs", variant)
    os.makedirs(variant_dir, exist_ok=True)
    files = []
    for i, arr in enumerate(arrays):
        path = pjoin(variant_dir, f"raw_{i:02}.npy")
        np.save(path, arr)
        files.append(path)
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo_dir", default="/data/public/ripemangobox/Motion/MotionCLR")
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--opt_path", default="./checkpoints/t2m/release/opt.txt")
    parser.add_argument("--prompt_file", default="")
    parser.add_argument("--lens_file", default="")
    parser.add_argument("--prompt_limit", type=int, default=1)
    parser.add_argument("--num_inference_steps", type=int, default=2)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--gpu_id", type=int, default=0)
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--layers", default="all")
    parser.add_argument("--no_fp16", action="store_true")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    os.chdir(args.repo_dir)
    sys.path.insert(0, args.repo_dir)

    from models import build_models
    from models.gaussian_diffusion import DiffusePipeline
    from utils.model_load import load_model_weights

    set_seed(args.seed)
    device = torch.device(f"cuda:{args.gpu_id}" if torch.cuda.is_available() else "cpu")

    opt = parse_motionclr_options(
        repo_dir=args.repo_dir,
        opt_path=args.opt_path,
        gpu_id=args.gpu_id,
        steps=args.num_inference_steps,
        seed=args.seed,
        no_fp16=args.no_fp16,
    )
    opt.device = device
    opt.output_dir = args.out_dir
    edit_config = yaml_to_box("options/noedit.yaml")
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

    default_prompt_file = pjoin(args.repo_dir, "assets/prompts.txt")
    default_lens_file = pjoin(args.repo_dir, "assets/motion_lens.txt")
    prompt_file = args.prompt_file or default_prompt_file
    lens_file = args.lens_file or default_lens_file
    with open(prompt_file, "r") as f:
        texts = [line.strip() for line in f if line.strip()][: args.prompt_limit]
    with open(lens_file, "r") as f:
        motion_lens = [int(line.strip()) for line in f if line.strip()][: len(texts)]
    if len(texts) != len(motion_lens):
        raise ValueError("prompt and motion length counts do not match")

    mapping = layer_map(pipeline.model)
    if args.layers == "all":
        selected_layers = [x["layer_id"] for x in mapping]
    else:
        selected_layers = [int(x) for x in args.layers.split(",") if x.strip()]

    with open(pjoin(args.out_dir, "layer_mapping.json"), "w") as f:
        json.dump(mapping, f, indent=2)
    with open(pjoin(args.out_dir, "prompts.json"), "w") as f:
        json.dump(
            [{"index": i, "text": text, "motion_len": motion_lens[i]} for i, text in enumerate(texts)],
            f,
            indent=2,
        )

    output_files = {}
    summaries = []

    baseline = generate_raw(pipeline, texts, motion_lens, args.batch_size)
    output_files["baseline"] = save_outputs(args.out_dir, "baseline", baseline)
    summaries.append(summarize_variant("baseline", baseline, None))

    for layer_id in selected_layers:
        variant = f"ca_off_layer_{layer_id:02d}"
        with ca_disabled(pipeline.model, [layer_id]):
            arrays = generate_raw(pipeline, texts, motion_lens, args.batch_size)
        output_files[variant] = save_outputs(args.out_dir, variant, arrays)
        summaries.append(summarize_variant(variant, arrays, baseline))

    with ca_disabled(pipeline.model, selected_layers):
        all_off = generate_raw(pipeline, texts, motion_lens, args.batch_size)
    output_files["ca_off_all_layers"] = save_outputs(args.out_dir, "ca_off_all_layers", all_off)
    summaries.append(summarize_variant("ca_off_all_layers", all_off, baseline))

    with open(pjoin(args.out_dir, "summary.json"), "w") as f:
        json.dump(summaries, f, indent=2)

    git_status = run(["git", "status", "--short"], cwd=args.repo_dir).splitlines()
    git_diff_stat = run(["git", "diff", "--stat"], cwd=args.repo_dir).splitlines()
    manifest = {
        "track": "B",
        "run_name": os.path.basename(args.out_dir),
        "repo_dir": args.repo_dir,
        "git_branch": run(["git", "branch", "--show-current"], cwd=args.repo_dir),
        "git_head": run(["git", "rev-parse", "HEAD"], cwd=args.repo_dir),
        "git_status_short": git_status,
        "dirty_diff_summary": git_diff_stat,
        "device": str(device),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        "gpu_role": "GPU1 host device, remapped to cuda:0 when CUDA_VISIBLE_DEVICES=1",
        "command": " ".join(sys.argv),
        "checkpoint_path": ckpt_path,
        "checkpoint_sha256": sha256(ckpt_path),
        "opt_path": opt.opt_path,
        "opt_sha256": sha256(opt.opt_path),
        "prompt_file": prompt_file,
        "prompt_file_sha256": sha256(prompt_file),
        "prompt_set": [{"index": i, "text": text, "motion_len": motion_lens[i]} for i, text in enumerate(texts)],
        "num_inference_steps": args.num_inference_steps,
        "seed": args.seed,
        "batch_size": args.batch_size,
        "torch_dtype": "float32" if args.no_fp16 else "float16",
        "cfg_source_location": "models/unet.py:941 MotionCLR.forward_with_cfg returns out_uncond + cfg_scale * (out_cond - out_uncond)",
        "perturbation": {
            "method": "run-local monkey patch of selected CLRBlock.forward",
            "target": "call the original CLRBlock.forward with empty cond_indices for the selected layer only",
            "selected_layer_ids": selected_layers,
            "positive_control": "ca_off_all_layers",
        },
        "layer_mapping": mapping,
        "output_files": output_files,
        "summary_file": pjoin(args.out_dir, "summary.json"),
        "limitations": [
            "MVP smoke sweep only: 1 prompt by default and 2 diffusion inference steps.",
            "No evaluator metrics or rendered videos; outputs are raw normalized motion tensors and numeric deltas.",
            "In MotionCLR, ResidualCLRAttentionLayer.forward returns before both self-attention and cross-attention when cond_indices is empty; this MVP disables the implemented clr_attn block path, not only key/value text attention internals.",
            "In MotionCLR forward_with_cfg, cond_indices covers the original batch indices, so non-disabled layers still apply conditioning only to the conditional half used in CFG.",
        ],
        "total_it": total_it,
    }
    with open(pjoin(args.out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print(json.dumps({"manifest": pjoin(args.out_dir, "manifest.json"), "summary": summaries}, indent=2))


if __name__ == "__main__":
    main()
