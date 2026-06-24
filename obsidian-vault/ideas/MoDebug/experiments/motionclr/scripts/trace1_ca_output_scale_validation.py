#!/usr/bin/env python
import argparse
import hashlib
import json
import os
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
    return subprocess.run(cmd, cwd=cwd, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip()


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
            "trace1_ca_output_scale_validation.py",
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
            "--edit_mode",
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


@contextmanager
def scaled_ca_outputs(model, layer_ids, alpha):
    modules = dict(model.unet.named_modules())
    mapping = layer_map(model)
    patched = []
    for item in mapping:
        if item["layer_id"] not in layer_ids:
            continue
        clr_name = item["module"].replace("unet.", "", 1)
        ca = modules[clr_name].clr_attn.cross_attention
        old_forward = ca.forward

        def make_forward(forward_fn):
            def forward_scaled(x, xf):
                return forward_fn(x, xf) * alpha

            return forward_scaled

        ca.forward = make_forward(old_forward)
        patched.append((ca, old_forward))
    try:
        yield
    finally:
        for ca, old_forward in patched:
            ca.forward = old_forward


def generate_raw(pipeline, texts, motion_lens, batch_size):
    output, _ = pipeline.generate(texts, torch.LongTensor(motion_lens), batch_size=batch_size)
    return [x.detach().cpu().numpy() for x in output]


def generate_seeded(pipeline, texts, motion_lens, batch_size, seed):
    set_seed(seed)
    return generate_raw(pipeline, texts, motion_lens, batch_size)


def save_arrays(out_dir, variant, arrays):
    variant_dir = pjoin(out_dir, "outputs", variant)
    os.makedirs(variant_dir, exist_ok=True)
    files = []
    for i, arr in enumerate(arrays):
        path = pjoin(variant_dir, f"raw_{i:02}.npy")
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo_dir", default="/data/public/ripemangobox/Motion/MotionCLR")
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--opt_path", default="./checkpoints/t2m/release/opt.txt")
    parser.add_argument("--prompt_file", default="")
    parser.add_argument("--lens_file", default="")
    parser.add_argument("--prompt_limit", type=int, default=2)
    parser.add_argument("--num_inference_steps", type=int, default=10)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--gpu_id", type=int, default=0)
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--layers", default="0,8,17")
    parser.add_argument("--alpha_values", default="1,0")
    parser.add_argument("--no_fp16", action="store_true")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    os.chdir(args.repo_dir)
    sys.path.insert(0, args.repo_dir)
    set_seed(args.seed)

    from models import build_models
    from models.gaussian_diffusion import DiffusePipeline
    from utils.model_load import load_model_weights

    device = torch.device(f"cuda:{args.gpu_id}" if torch.cuda.is_available() else "cpu")
    opt = parse_options(args.repo_dir, args.opt_path, args.gpu_id, args.num_inference_steps, args.seed, args.no_fp16)
    opt.device = device
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

    prompt_file = args.prompt_file or pjoin(args.repo_dir, "assets/prompts.txt")
    lens_file = args.lens_file or pjoin(args.repo_dir, "assets/motion_lens.txt")
    with open(prompt_file, "r") as f:
        texts = [line.strip() for line in f if line.strip()][: args.prompt_limit]
    with open(lens_file, "r") as f:
        motion_lens = [int(line.strip()) for line in f if line.strip()][: len(texts)]
    selected_layers = [int(x) for x in args.layers.split(",") if x.strip()]
    alpha_values = [float(x) for x in args.alpha_values.split(",") if x.strip()]

    mapping = layer_map(pipeline.model)
    with open(pjoin(args.out_dir, "layer_mapping.json"), "w") as f:
        json.dump(mapping, f, indent=2)

    started = time.time()
    baseline = generate_seeded(pipeline, texts, motion_lens, args.batch_size, args.seed)
    outputs = {"baseline": save_arrays(args.out_dir, "baseline", baseline)}
    summary = [{"variant": "baseline", "num_outputs": len(baseline)}]

    with scaled_ca_outputs(pipeline.model, selected_layers, 1.0):
        noop = generate_seeded(pipeline, texts, motion_lens, args.batch_size, args.seed)
    outputs["noop_alpha_1_selected"] = save_arrays(args.out_dir, "noop_alpha_1_selected", noop)
    summary.append({"variant": "noop_alpha_1_selected", **diff_stats(noop, baseline)})

    for alpha in alpha_values:
        if alpha == 1.0:
            continue
        variant = "selected_layers_alpha_" + str(alpha).replace(".", "p")
        with scaled_ca_outputs(pipeline.model, selected_layers, alpha):
            arrays = generate_seeded(pipeline, texts, motion_lens, args.batch_size, args.seed)
        outputs[variant] = save_arrays(args.out_dir, variant, arrays)
        summary.append({"variant": variant, "layers": selected_layers, "alpha": alpha, **diff_stats(arrays, baseline)})

    all_layers = [item["layer_id"] for item in mapping]
    with scaled_ca_outputs(pipeline.model, all_layers, 0.0):
        all_zero = generate_seeded(pipeline, texts, motion_lens, args.batch_size, args.seed)
    outputs["all_layers_alpha_0"] = save_arrays(args.out_dir, "all_layers_alpha_0", all_zero)
    summary.append({"variant": "all_layers_alpha_0", "layers": all_layers, "alpha": 0.0, **diff_stats(all_zero, baseline)})

    with open(pjoin(args.out_dir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    manifest = {
        "trace": "Trace 1",
        "old_name": "Track B",
        "formal_data_status": "engineering_validation_only",
        "purpose": "Bounded validation of CA output scaling hook with real MotionCLR checkpoint and real prompts.",
        "repo_dir": args.repo_dir,
        "git_head": run(["git", "rev-parse", "HEAD"], args.repo_dir),
        "git_branch": run(["git", "branch", "--show-current"], args.repo_dir),
        "git_status_short": run(["git", "status", "--short"], args.repo_dir).splitlines(),
        "git_diff_stat": run(["git", "diff", "--stat"], args.repo_dir).splitlines(),
        "command": " ".join(sys.argv),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        "device": str(device),
        "checkpoint_path": ckpt_path,
        "checkpoint_sha256": sha256(ckpt_path),
        "opt_path": opt.opt_path,
        "opt_sha256": sha256(opt.opt_path),
        "prompt_file": prompt_file,
        "prompt_file_sha256": sha256(prompt_file),
        "texts": texts,
        "motion_lens": motion_lens,
        "seed": args.seed,
        "num_inference_steps": args.num_inference_steps,
        "selected_layers": selected_layers,
        "alpha_values": alpha_values,
        "outputs": outputs,
        "summary_file": pjoin(args.out_dir, "summary.json"),
        "elapsed_sec": time.time() - started,
        "total_it": total_it,
        "limitations": [
            "Bounded validation only; not formal layer criticality evidence.",
            "No formal evaluator metrics are computed.",
            "Formal sweep requires DS approval after this hook validation.",
        ],
    }
    with open(pjoin(args.out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    with open(pjoin(args.out_dir, "NONFORMAL_NOTICE.txt"), "w") as f:
        f.write("FORMAL_DATA_STATUS=engineering_validation_only\nDO_NOT_USE_FOR_FORMAL_CLAIMS=true\n")
    print(json.dumps({"manifest": pjoin(args.out_dir, "manifest.json"), "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
