#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import re
import subprocess
import sys
import time
from contextlib import contextmanager, nullcontext
from os.path import join as pjoin

import numpy as np
import torch
import tqdm
import yaml
from accelerate.utils import set_seed
from box import Box


FLOAT = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
SIMPLE_PATTERNS = {
    "matching_score": re.compile(rf"---> \[(?P<model>[^\]]+)\] Matching Score: (?P<value>{FLOAT})"),
    "fid": re.compile(rf"---> \[(?P<model>[^\]]+)\] FID: (?P<value>{FLOAT})"),
    "diversity": re.compile(rf"---> \[(?P<model>[^\]]+)\] Diversity: (?P<value>{FLOAT})"),
    "multimodality": re.compile(rf"---> \[(?P<model>[^\]]+)\] Multimodality: (?P<value>{FLOAT})"),
}
R_PRECISION = re.compile(r"---> \[(?P<model>[^\]]+)\] R_precision:(?P<body>.*)")
TOP = re.compile(rf"\(top\s*(?P<top>\d+)\):\s*(?P<value>{FLOAT})")


def run(cmd: list[str], cwd: str) -> str:
    return subprocess.run(
        cmd, cwd=cwd, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).stdout.strip()


def sha256(path: str) -> str | None:
    if not path or not os.path.isfile(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_record(path: str) -> dict:
    abs_path = os.path.abspath(path) if path else ""
    return {"path": abs_path, "sha256": sha256(abs_path)}


def infer_command_script(out_dir: str) -> str:
    explicit = os.environ.get("MODEBUG_COMMAND_SCRIPT", "")
    if explicit:
        return explicit
    run_hint = os.path.abspath(out_dir)
    if "sa_cfg_sa" in run_hint:
        name = "trace1_full_eval_gpu1_sa_cfg_sa_command.sh"
    elif "ca_cfg_ca" in run_hint:
        name = "trace1_full_eval_gpu0_ca_cfg_ca_command.sh"
    else:
        return ""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "commands", name)


def yaml_to_box(path: str) -> Box:
    with open(path, "r") as f:
        return Box(yaml.safe_load(f))


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    set_seed(seed)


def parse_eval_log(path: str) -> dict:
    metrics_by_model: dict[str, dict[str, list[float]]] = {}
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            for key, pattern in SIMPLE_PATTERNS.items():
                match = pattern.search(line)
                if match:
                    model = match.group("model")
                    metrics_by_model.setdefault(model, {}).setdefault(key, []).append(float(match.group("value")))
            match = R_PRECISION.search(line)
            if match:
                model = match.group("model")
                for top_match in TOP.finditer(match.group("body")):
                    top = top_match.group("top")
                    metrics_by_model.setdefault(model, {}).setdefault(f"r_precision_top{top}", []).append(
                        float(top_match.group("value"))
                    )
    return {
        model: {
            key: {
                "values": values,
                "last": values[-1] if values else None,
                "mean": float(np.mean(values)) if values else None,
                "std": float(np.std(values)) if values else None,
            }
            for key, values in metrics.items()
        }
        for model, metrics in metrics_by_model.items()
    }


def parse_test_options(args: argparse.Namespace):
    from options.evaluate_options import TestOptions

    old_argv = sys.argv[:]
    try:
        sys.argv = [
            "trace1_full_eval_attention_intervention.py",
            "--opt_path",
            args.opt_path,
            "--gpu_id",
            str(args.gpu_id),
            "--which_ckpt",
            args.which_ckpt,
            "--batch_size",
            str(args.batch_size),
            "--replication_times",
            "1",
            "--num_inference_steps",
            str(args.num_inference_steps),
            "--evaluator_dir",
            args.evaluator_dir,
            "--eval_meta_dir",
            args.eval_meta_dir,
            "--glove_dir",
            args.glove_dir,
        ]
        if args.no_eff:
            sys.argv.append("--no_eff")
        if args.self_attention:
            sys.argv.append("--self_attention")
        if args.no_fp16:
            sys.argv.append("--no_fp16")
        if args.no_ema:
            sys.argv.append("--no_ema")
        if args.edit_mode:
            sys.argv.append("--edit_mode")
        return TestOptions().parse()
    finally:
        sys.argv = old_argv


def layer_map(model) -> list[dict]:
    layers = []
    for name, module in model.unet.named_modules():
        if module.__class__.__name__ == "CLRBlock":
            item = {
                "layer_id": len(layers),
                "module": "unet." + name,
                "attention_module": "unet." + name + ".clr_attn",
                "cross_attention_module": "unet." + name + ".clr_attn.cross_attention",
                "cross_attention_class": module.clr_attn.cross_attention.__class__.__name__,
                "has_self_attention": bool(getattr(module.clr_attn, "self_attn_use", False)),
            }
            if item["has_self_attention"]:
                item["self_attention_module"] = "unet." + name + ".clr_attn.self_attention"
            layers.append(item)
    return layers


def modules_by_unet_name(model) -> dict:
    return dict(model.unet.named_modules())


def parse_layers(value: str, mapping: list[dict], allow_multi_layer: bool) -> list[int]:
    max_layer = len(mapping) - 1
    if value == "all":
        layers = [item["layer_id"] for item in mapping]
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
        raise ValueError("Formal full eval requires exactly one layer; pass --allow_multi_layer to override.")
    return layers


def parse_float_list(value: str) -> list[float]:
    if not value.strip():
        return []
    return [float(item.strip()) for item in value.split(",") if item.strip()]


def cfg_step_alpha(
    schedule: str,
    step_index: int,
    total_steps: int,
    decay: float,
    interval: tuple[float, float],
    table: list[float],
) -> float:
    progress = 0.0 if total_steps <= 1 else step_index / float(total_steps - 1)
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


def scheduled_cfg_scale(
    base_cfg: float,
    schedule: str,
    step_index: int,
    total_steps: int,
    decay: float,
    interval: tuple[float, float],
    table: list[float],
    alpha_scale: float,
) -> tuple[float, float]:
    alpha_t = cfg_step_alpha(schedule, step_index, total_steps, decay, interval, table)
    return 1.0 + (base_cfg - 1.0) * alpha_scale * alpha_t, alpha_t


class LocalInterventionPipeline:
    def __init__(
        self,
        opt,
        model,
        diffuser_name,
        num_inference_steps,
        device,
        torch_dtype=torch.float16,
        cfg_scale=2.5,
        cfg_schedule="constant",
        cfg_schedule_decay=1.0,
        cfg_schedule_interval=(0.25, 0.75),
        cfg_schedule_table=None,
        cfg_alpha_scale=1.0,
    ) -> None:
        from diffusers import (
            DDIMScheduler,
            DDPMScheduler,
            DEISMultistepScheduler,
            DPMSolverMultistepScheduler,
            PNDMScheduler,
        )

        self.device = device
        self.torch_dtype = torch_dtype
        self.diffuser_name = diffuser_name
        self.num_inference_steps = num_inference_steps
        self.cfg_scale = cfg_scale
        self.cfg_schedule = cfg_schedule
        self.cfg_schedule_decay = cfg_schedule_decay
        self.cfg_schedule_interval = cfg_schedule_interval
        self.cfg_schedule_table = cfg_schedule_table or []
        self.cfg_alpha_scale = cfg_alpha_scale
        self.cfg_schedule_audit = {
            "call_count": 0,
            "min_cfg": None,
            "max_cfg": None,
            "trace": [],
        }
        if self.torch_dtype == torch.float16:
            model = model.half()
        self.model = model.to(device)
        self.opt = opt

        scheduler_classes = {
            "DDIMScheduler": DDIMScheduler,
            "DDPMScheduler": DDPMScheduler,
            "DEISMultistepScheduler": DEISMultistepScheduler,
            "DPMSolverMultistepScheduler": DPMSolverMultistepScheduler,
            "PNDMScheduler": PNDMScheduler,
        }
        with open("config/diffuser_params.yaml", "r") as f:
            diffuser_params = yaml.safe_load(f)
        if diffuser_name not in diffuser_params:
            raise ValueError(f"Unsupported diffuser_name: {diffuser_name}")
        params = diffuser_params[diffuser_name]
        additional_params = dict(params["additional_params"])
        additional_params["num_train_timesteps"] = opt.diffusion_steps
        additional_params["beta_schedule"] = opt.beta_schedule
        additional_params["prediction_type"] = opt.prediction_type
        scheduler_class = scheduler_classes[params["scheduler_class"]]
        self.scheduler = scheduler_class(**additional_params)

    def generate_batch(self, caption, m_lens):
        batch_size = len(caption)
        max_len = m_lens.max()
        sample = torch.randn((batch_size, max_len, self.model.input_feats), device=self.device, dtype=self.torch_dtype)

        self.scheduler.set_timesteps(self.num_inference_steps, self.device)
        timesteps = [torch.tensor([t] * batch_size, device=self.device).long() for t in self.scheduler.timesteps]
        enc_text = self.model.encode_text(caption, self.device)

        for step_index, t in enumerate(timesteps):
            cfg_value, alpha_t = scheduled_cfg_scale(
                self.cfg_scale,
                self.cfg_schedule,
                step_index,
                len(timesteps),
                self.cfg_schedule_decay,
                self.cfg_schedule_interval,
                self.cfg_schedule_table,
                self.cfg_alpha_scale,
            )
            self._record_cfg_schedule(step_index, int(t[0].item()), len(timesteps), cfg_value, alpha_t)
            with torch.no_grad():
                if getattr(self.model, "cond_mask_prob", 0) > 0:
                    predict = self.model.forward_with_cfg(sample, t, enc_text=enc_text, cfg_scale=cfg_value)
                else:
                    predict = self.model(sample, t, enc_text=enc_text)
            sample = self.scheduler.step(predict, t[0], sample).prev_sample
        return sample

    def _record_cfg_schedule(self, step_index, raw_t, total_steps, cfg_value, alpha_t):
        audit = self.cfg_schedule_audit
        audit["call_count"] += 1
        audit["min_cfg"] = cfg_value if audit["min_cfg"] is None else min(audit["min_cfg"], cfg_value)
        audit["max_cfg"] = cfg_value if audit["max_cfg"] is None else max(audit["max_cfg"], cfg_value)
        if len(audit["trace"]) < 200:
            progress = 0.0 if total_steps <= 1 else step_index / float(total_steps - 1)
            audit["trace"].append(
                {
                    "step_index": int(step_index),
                    "total_steps": int(total_steps),
                    "progress": float(progress),
                    "raw_timestep": int(raw_t),
                    "alpha_t": float(alpha_t),
                    "cfg_scale": float(cfg_value),
                }
            )

    def generate(self, caption, m_lens, batch_size=32):
        count = len(caption)
        infer_mode = ""
        if getattr(self.model, "cond_mask_prob", 0) > 0:
            infer_mode = "classifier-free-guidance"
        print(
            f"\nUsing {self.diffuser_name} diffusion scheduler to {infer_mode} generate "
            f"{count} motions, sampling {self.num_inference_steps} steps, cfg_scale={self.cfg_scale}."
        )
        self.model.eval()

        outputs = []
        elapsed_sum = 0.0
        timed_batches = 0
        cur_idx = 0
        for batch_idx in tqdm.tqdm(range(math.ceil(count / batch_size))):
            batch_caption = caption[cur_idx : cur_idx + batch_size]
            batch_m_lens = m_lens[cur_idx : cur_idx + batch_size]
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            start_time = time.time()
            output = self.generate_batch(batch_caption, batch_m_lens)
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            now_time = time.time()
            if (batch_idx + 1) * self.num_inference_steps >= 50:
                elapsed_sum += now_time - start_time
                timed_batches += 1
            for i in range(output.shape[0]):
                outputs.append(output[i, : batch_m_lens[i]])
            cur_idx += batch_size

        t_eval = elapsed_sum / max(1, timed_batches)
        print("The average generation time of a batch motion (bs=%d) is %f seconds" % (batch_size, t_eval))
        return outputs, t_eval


@contextmanager
def scale_cross_attention_outputs(model, layer_ids: list[int], alpha: float):
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
        yield {"call_counts": call_counts, "replacement_checks": []}
    finally:
        for module, old_forward in patched:
            module.forward = old_forward


@contextmanager
def scale_self_attention_outputs(model, layer_ids: list[int], alpha: float):
    modules = modules_by_unet_name(model)
    mapping = layer_map(model)
    patched = []
    call_counts = {str(layer_id): 0 for layer_id in layer_ids}
    for item in mapping:
        layer_id = item["layer_id"]
        if layer_id not in layer_ids:
            continue
        if not item["has_self_attention"]:
            raise RuntimeError(f"Layer {layer_id} has no self_attention module")
        clr_name = item["module"].replace("unet.", "", 1)
        sa = modules[clr_name].clr_attn.self_attention
        old_forward = sa.forward

        def make_forward(forward_fn, lid):
            def forward_scaled(x):
                call_counts[str(lid)] += 1
                return forward_fn(x) * alpha

            return forward_scaled

        sa.forward = make_forward(old_forward, layer_id)
        patched.append((sa, old_forward))
    try:
        yield {"call_counts": call_counts, "replacement_checks": []}
    finally:
        for module, old_forward in patched:
            module.forward = old_forward


@contextmanager
def replace_self_attention_cond_with_uncond(model, layer_ids: list[int]):
    modules = modules_by_unet_name(model)
    mapping = layer_map(model)
    patched = []
    call_counts = {str(layer_id): 0 for layer_id in layer_ids}
    replacement_checks = []
    for item in mapping:
        layer_id = item["layer_id"]
        if layer_id not in layer_ids:
            continue
        if not item["has_self_attention"]:
            raise RuntimeError(f"Layer {layer_id} has no self_attention module")
        clr_name = item["module"].replace("unet.", "", 1)
        sa = modules[clr_name].clr_attn.self_attention
        old_forward = sa.forward

        def make_forward(forward_fn, lid):
            def forward_replaced(x):
                y = forward_fn(x)
                call_counts[str(lid)] += 1
                if y.shape[0] % 2 != 0:
                    raise RuntimeError(f"CFG_SA layer {lid} expected even batch, got {tuple(y.shape)}")
                half = y.shape[0] // 2
                before = (y[:half] - y[half:]).detach().abs().max().item()
                new_y = y.clone()
                new_y[:half] = y[half:].clone()
                after = (new_y[:half] - new_y[half:]).detach().abs().max().item()
                replacement_checks.append(
                    {
                        "layer_id": lid,
                        "shape": list(y.shape),
                        "max_abs_before": before,
                        "max_abs_after": after,
                    }
                )
                return new_y

            return forward_replaced

        sa.forward = make_forward(old_forward, layer_id)
        patched.append((sa, old_forward))
    try:
        yield {"call_counts": call_counts, "replacement_checks": replacement_checks}
    finally:
        for module, old_forward in patched:
            module.forward = old_forward


@contextmanager
def replace_ca_boundary_cond_with_uncond(model, layer_ids: list[int]):
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
        attn = modules[clr_name].clr_attn
        old_forward = attn.forward

        def make_forward(attn_module, lid):
            def forward_replaced(input_tensor, condition_tensor, cond_indices):
                if cond_indices.numel() == 0:
                    return input_tensor

                if attn_module.self_attn_use:
                    sa_out = input_tensor.permute(0, 2, 1)
                    sa_out = attn_module.self_attention(sa_out)
                    sa_out = sa_out.permute(0, 2, 1)
                    input_tensor = input_tensor + sa_out

                pre_ca = input_tensor.clone()
                x = input_tensor[cond_indices].permute(0, 2, 1)
                x = attn_module.cross_attention(x, condition_tensor[cond_indices])
                x = x.permute(0, 2, 1)

                output = input_tensor.clone()
                output[cond_indices] = output[cond_indices] + x
                call_counts[str(lid)] += 1

                if output.shape[0] % 2 != 0:
                    raise RuntimeError(f"CFG_CA layer {lid} expected even batch, got {tuple(output.shape)}")
                half = output.shape[0] // 2
                expected = torch.arange(half, device=cond_indices.device)
                if cond_indices.shape[0] != half or not torch.equal(cond_indices.to(expected.device), expected):
                    raise RuntimeError(
                        f"CFG_CA layer {lid} expected cond_indices arange({half}), got {cond_indices.detach().cpu().tolist()}"
                    )
                before = (output[:half] - pre_ca[half:]).detach().abs().max().item()
                new_output = output.clone()
                new_output[:half] = pre_ca[half:].clone()
                after = (new_output[:half] - new_output[half:]).detach().abs().max().item()
                replacement_checks.append(
                    {
                        "layer_id": lid,
                        "shape": list(output.shape),
                        "max_abs_cond_post_ca_vs_uncond_pre_ca_before": before,
                        "max_abs_cond_vs_uncond_after": after,
                        "definition": "cond post-CA hidden is replaced with uncond post-self-attention/pre-CA hidden",
                    }
                )
                return new_output

            return forward_replaced

        attn.forward = make_forward(attn, layer_id)
        patched.append((attn, old_forward))
    try:
        yield {"call_counts": call_counts, "replacement_checks": replacement_checks}
    finally:
        for module, old_forward in patched:
            module.forward = old_forward


def intervention_context(model, family: str, layer_ids: list[int], alpha: float):
    if family == "baseline":
        return nullcontext({"call_counts": {}, "replacement_checks": []})
    if family == "ca":
        return scale_cross_attention_outputs(model, layer_ids, alpha)
    if family == "sa":
        return scale_self_attention_outputs(model, layer_ids, alpha)
    if family == "cfg_sa":
        return replace_self_attention_cond_with_uncond(model, layer_ids)
    if family == "cfg_ca":
        return replace_ca_boundary_cond_with_uncond(model, layer_ids)
    raise ValueError(f"Unsupported family: {family}")


def evaluator_checkpoint(evaluator_dir: str) -> str:
    return pjoin(evaluator_dir, "t2m", "text_mot_match", "model", "finest.tar")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo_dir", default="/data/public/ripemangobox/Motion/MotionCLR")
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--family", required=True, choices=["baseline", "ca", "sa", "cfg_ca", "cfg_sa"])
    parser.add_argument("--layers", default="0")
    parser.add_argument("--allow_multi_layer", action="store_true")
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--cfg_scale", type=float, default=2.5)
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
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--opt_path", default="./checkpoints/t2m/release/opt.txt")
    parser.add_argument("--which_ckpt", default="latest")
    parser.add_argument("--gpu_id", type=int, default=0)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--replication_times", type=int, default=1)
    parser.add_argument("--num_inference_steps", type=int, default=10)
    parser.add_argument("--evaluator_dir", default="./data/pretrained_models")
    parser.add_argument("--eval_meta_dir", default="./data")
    parser.add_argument("--glove_dir", default="./data/glove")
    parser.add_argument("--no_eff", action="store_true", default=True)
    parser.add_argument("--self_attention", action="store_true", default=True)
    parser.add_argument("--no_fp16", action="store_true", default=True)
    parser.add_argument("--no_ema", action="store_true")
    parser.add_argument("--edit_mode", action="store_true")
    args = parser.parse_args()
    if args.cfg_layer_alpha is not None:
        args.cfg_alpha_scale = args.cfg_layer_alpha

    started = time.time()
    os.makedirs(args.out_dir, exist_ok=True)
    os.chdir(args.repo_dir)
    sys.path.insert(0, args.repo_dir)
    interval_values = parse_float_list(args.cfg_schedule_interval)
    if len(interval_values) != 2:
        raise ValueError("--cfg_schedule_interval must contain exactly two comma-separated floats")
    cfg_schedule_interval = (interval_values[0], interval_values[1])
    cfg_schedule_table = parse_float_list(args.cfg_schedule_table)

    if args.family in {"cfg_ca", "cfg_sa"} and args.alpha != 0:
        print(f"WARNING: --alpha={args.alpha} is ignored for {args.family}; CFG families use hidden replacement only.")

    from datasets import get_dataset
    from eval import EvaluatorModelWrapper, evaluation
    from models import build_models
    from motion_loader import get_dataset_loader, get_motion_loader
    from utils.model_load import load_model_weights

    seed_everything(args.seed)
    opt = parse_test_options(args)
    opt.save_root = args.out_dir
    device = torch.device(f"cuda:{args.gpu_id}" if torch.cuda.is_available() else "cpu")
    if torch.cuda.is_available():
        torch.cuda.set_device(device)
    opt.device = device

    edit_config = yaml_to_box("options/edit.yaml" if opt.edit_mode else "options/noedit.yaml")
    eval_wrapper = EvaluatorModelWrapper(opt)
    gt_loader = get_dataset_loader(opt, opt.batch_size, mode="gt_eval", split="test")
    gen_dataset = get_dataset(opt, mode="eval", split="test")

    model = build_models(opt, edit_config=edit_config)
    ckpt_path = pjoin(opt.model_dir, opt.which_ckpt + ".tar")
    if not os.path.isfile(ckpt_path):
        raise RuntimeError(f"Missing checkpoint: {ckpt_path}")
    evaluator_ckpt = evaluator_checkpoint(args.evaluator_dir)
    if not os.path.isfile(evaluator_ckpt):
        raise RuntimeError(f"Missing evaluator checkpoint: {evaluator_ckpt}")
    total_it = load_model_weights(model, ckpt_path, use_ema=not opt.no_ema, device=device)

    pipeline = LocalInterventionPipeline(
        opt=opt,
        model=model,
        diffuser_name=opt.diffuser_name,
        device=device,
        num_inference_steps=opt.num_inference_steps,
        torch_dtype=torch.float32 if opt.no_fp16 else torch.float16,
        cfg_scale=args.cfg_scale,
        cfg_schedule=args.cfg_schedule,
        cfg_schedule_decay=args.cfg_schedule_decay,
        cfg_schedule_interval=cfg_schedule_interval,
        cfg_schedule_table=cfg_schedule_table,
        cfg_alpha_scale=args.cfg_alpha_scale,
    )
    model = pipeline.model
    model.eval()

    mapping = layer_map(model)
    if len(mapping) != 18:
        raise RuntimeError(f"Expected exactly 18 CLRBlock layers, found {len(mapping)}")
    layer_ids = [] if args.family == "baseline" else parse_layers(args.layers, mapping, args.allow_multi_layer)
    selected_mapping = [item for item in mapping if item["layer_id"] in layer_ids]

    layer_mapping_path = pjoin(args.out_dir, "layer_mapping.json")
    with open(layer_mapping_path, "w") as f:
        json.dump(mapping, f, indent=2)

    log_file = pjoin(args.out_dir, "eval_stdout_stderr.log")
    with open(log_file, "w") as f:
        f.write("------------ MoDebug MotionCLR full-eval attention intervention -------------\n")
        f.write(f"family: {args.family}\n")
        f.write(f"layers: {layer_ids}\n")
        f.write(f"alpha: {args.alpha}\n")
        f.write(f"cfg_scale: {args.cfg_scale}\n")
        f.write(f"cfg_schedule: {args.cfg_schedule}\n")
        f.write(f"cfg_alpha_scale: {args.cfg_alpha_scale}\n")
        f.write(f"seed: {args.seed}\n")
        f.write("-------------- End ----------------\n")

    failures = []
    with intervention_context(model, args.family, layer_ids, args.alpha) as hook_state:
        for rep_idx in range(args.replication_times):
            rep_seed = args.seed + rep_idx
            seed_everything(rep_seed)
            eval_motion_loaders = {
                f"text2motion_{args.family}": lambda: get_motion_loader(
                    opt,
                    opt.batch_size,
                    pipeline,
                    gen_dataset,
                    opt.mm_num_samples,
                    opt.mm_num_repeats,
                )
            }
            evaluation(
                eval_wrapper,
                gt_loader,
                eval_motion_loaders,
                log_file,
                1,
                opt.diversity_times,
                opt.mm_num_times,
                run_mm=True,
            )

    if args.family != "baseline":
        for layer_id in layer_ids:
            if hook_state["call_counts"].get(str(layer_id), 0) <= 0:
                failures.append(f"Layer {layer_id} hook was never called for family {args.family}")
        if args.family in {"cfg_ca", "cfg_sa"} and not hook_state["replacement_checks"]:
            failures.append(f"No replacement checks recorded for {args.family}")

    metrics = parse_eval_log(log_file)
    summary_path = pjoin(args.out_dir, "metrics_summary.json")
    with open(summary_path, "w") as f:
        json.dump(metrics, f, indent=2)

    limitations = []
    if args.family == "cfg_ca":
        limitations.extend(
            [
                "MotionCLR uncond branch does not call CrossAttention, so CFG_CA cannot replace a true uncond CA output.",
                "Implemented definition: after self-attention and after the selected CA sublayer, cond post-CA hidden is replaced with uncond post-self-attention/pre-CA hidden.",
                "This removes the selected layer CA contribution and aligns cond hidden at that CA boundary to the uncond branch; report this as cfg_ca_boundary_hidden_replacement.",
                "The implementation patches only the selected layer instance's ResidualCLRAttentionLayer.forward during CFG_CA runs; non-selected layers keep their original forward method.",
            ]
        )

    wrapper_script = os.path.abspath(__file__)
    command_script = infer_command_script(args.out_dir)
    edit_config_path = "options/edit.yaml" if opt.edit_mode else "options/noedit.yaml"
    diffuser_config_path = "config/diffuser_params.yaml"
    evaluator_config_path = "config/evaluator.yaml"
    manifest = {
        "trace": "Trace 1",
        "scope": "full_official_evaluator_attention_intervention",
        "paper_level_status": "full_evaluator_metrics_computed" if not failures else "failed",
        "repo_dir": args.repo_dir,
        "git_head": run(["git", "rev-parse", "HEAD"], args.repo_dir),
        "git_branch": run(["git", "branch", "--show-current"], args.repo_dir),
        "git_status_short": run(["git", "status", "--short"], args.repo_dir).splitlines(),
        "git_diff_stat": run(["git", "diff", "--stat"], args.repo_dir).splitlines(),
        "command": " ".join(sys.argv),
        "wrapper_script": file_record(wrapper_script),
        "command_script": file_record(command_script),
        "deployed_from": os.environ.get("MODEBUG_DEPLOYED_FROM", ""),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        "device": str(device),
        "torch_dtype": str(pipeline.torch_dtype),
        "family": args.family,
        "layers": layer_ids,
        "selected_layer_mapping": selected_mapping,
        "alpha": args.alpha if args.family in {"ca", "sa"} else None,
        "cfg_scale": args.cfg_scale,
        "cfg_schedule": {
            "status": "diagnostic_run_level_schedule",
            "schedule": args.cfg_schedule,
            "base_cfg_scale": args.cfg_scale,
            "decay": args.cfg_schedule_decay,
            "interval": list(cfg_schedule_interval),
            "table": cfg_schedule_table,
            "alpha_scale": args.cfg_alpha_scale,
            "deprecated_cfg_layer_alpha_alias": args.cfg_layer_alpha,
            "definition": "effective_cfg = 1 + (base_cfg - 1) * alpha_scale * alpha_t(step)",
            "limitation": "MotionCLR applies CFG after the full UNet cond/uncond pass; this is a denoising-step schedule for selected-layer diagnostic runs, not a true layer-local CFG mixer.",
            "runtime_audit": pipeline.cfg_schedule_audit,
        },
        "seed": args.seed,
        "replication_times": args.replication_times,
        "num_inference_steps": args.num_inference_steps,
        "batch_size": args.batch_size,
        "checkpoint_path": ckpt_path,
        "checkpoint_sha256": sha256(ckpt_path),
        "opt_path": opt.opt_path,
        "opt_sha256": sha256(opt.opt_path),
        "config_files": {
            "diffuser_params": file_record(diffuser_config_path),
            "edit_config": file_record(edit_config_path),
            "evaluator_config": file_record(evaluator_config_path),
        },
        "evaluator_dir": args.evaluator_dir,
        "evaluator_checkpoint": evaluator_ckpt,
        "evaluator_checkpoint_sha256": sha256(evaluator_ckpt),
        "eval_protocol": {
            "wrapper_replication_loop": args.replication_times,
            "official_evaluation_replication_times_per_call": 1,
            "mm_num_samples": getattr(opt, "mm_num_samples", None),
            "mm_num_repeats": getattr(opt, "mm_num_repeats", None),
            "mm_num_times": getattr(opt, "mm_num_times", None),
            "diversity_times": getattr(opt, "diversity_times", None),
            "run_mm": True,
            "no_eff": bool(opt.no_eff),
            "self_attention": bool(opt.self_attention),
            "no_fp16": bool(opt.no_fp16),
            "no_ema": bool(opt.no_ema),
        },
        "layer_mapping_file": layer_mapping_path,
        "log_file": log_file,
        "metrics_summary_file": summary_path,
        "metrics_summary_sha256": sha256(summary_path),
        "metrics": metrics,
        "hook_call_counts": hook_state["call_counts"],
        "replacement_checks": hook_state["replacement_checks"],
        "limitations": limitations,
        "failures": failures,
        "elapsed_sec": time.time() - started,
        "total_it": total_it,
    }
    manifest_path = pjoin(args.out_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    if failures:
        print(json.dumps({"manifest": manifest_path, "failures": failures}, indent=2))
        raise SystemExit(2)
    print(json.dumps({"manifest": manifest_path, "metrics_summary": summary_path}, indent=2))


if __name__ == "__main__":
    main()
