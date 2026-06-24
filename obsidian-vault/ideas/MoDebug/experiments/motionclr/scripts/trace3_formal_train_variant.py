#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
from collections import OrderedDict
from os.path import join as pjoin

import torch
import torch.nn.functional as F
import yaml
from accelerate import Accelerator
from accelerate.utils import set_seed
from box import Box


VARIANTS = {"baseline", "aug", "disploss", "aug_disploss"}


def run(cmd: list[str], cwd: str) -> str:
    return subprocess.run(
        cmd, cwd=cwd, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).stdout.strip()


def sha256(path: str) -> str | None:
    if not path or not os.path.exists(path) or not os.path.isfile(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_record(path: str) -> dict:
    return {
        "path": path,
        "exists": os.path.exists(path),
        "size_bytes": os.path.getsize(path) if os.path.exists(path) and os.path.isfile(path) else None,
        "sha256": sha256(path),
    }


def yaml_to_box(path: str) -> Box:
    with open(path, "r") as f:
        return Box(yaml.safe_load(f))


def split_line_count(path: str) -> int | None:
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return sum(1 for line in f if line.strip())


def parse_train_options(args: argparse.Namespace, accelerator: Accelerator):
    sys.path.insert(0, args.repo_dir)
    from options.train_options import TrainOptions

    old_argv = sys.argv[:]
    try:
        sys.argv = [
            "trace3_formal_train_variant.py",
            "--name",
            args.name,
            "--dataset_name",
            "t2m",
            "--dropout",
            str(args.dropout),
            "--lr",
            str(args.lr),
            "--batch_size",
            str(args.batch_size),
            "--num_train_steps",
            str(args.target_steps),
            "--log_every",
            str(args.log_every),
            "--save_interval",
            str(args.save_interval),
            "--checkpoints_dir",
            pjoin(args.out_dir, "checkpoints"),
            "--seed",
            str(args.seed),
        ]
        if args.no_eff:
            sys.argv.append("--no_eff")
        if args.self_attention:
            sys.argv.append("--self_attention")
        if args.edit_mode:
            sys.argv.append("--edit_mode")
        if args.model_ema:
            sys.argv.append("--model-ema")
        opt = TrainOptions().parse(accelerator)
        return opt
    finally:
        sys.argv = old_argv


def get_module(root: torch.nn.Module, dotted_path: str) -> torch.nn.Module:
    module = root
    for part in dotted_path.split("."):
        if not hasattr(module, part):
            raise RuntimeError(f"Module path '{dotted_path}' not found at '{part}'")
        module = getattr(module, part)
    return module


class TemporalScaleAugmenter:
    def __init__(
        self,
        prob: float,
        min_scale: float,
        max_scale: float,
        min_len: int,
        skip_keywords: str,
        seed: int,
    ) -> None:
        self.prob = prob
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.min_len = min_len
        self.skip_keywords = [item.strip().lower() for item in skip_keywords.split(",") if item.strip()]
        self.generator = torch.Generator()
        self.generator.manual_seed(seed)
        self.total_seen = 0
        self.total_augmented = 0
        self.total_skipped_keyword = 0

    def is_safe_caption(self, caption: str) -> bool:
        lower = caption.lower()
        return not any(keyword in lower for keyword in self.skip_keywords)

    def apply(self, captions, motions: torch.Tensor, m_lens: torch.Tensor):
        if self.prob <= 0:
            return captions, motions, m_lens
        new_motions = motions.clone()
        new_lens = torch.as_tensor(m_lens, device=motions.device).clone()
        max_len = motions.shape[1]
        for idx, caption in enumerate(captions):
            self.total_seen += 1
            if not self.is_safe_caption(str(caption)):
                self.total_skipped_keyword += 1
                continue
            if torch.rand((), generator=self.generator).item() >= self.prob:
                continue
            old_len = int(min(max_len, int(new_lens[idx].item())))
            if old_len <= self.min_len:
                continue
            scale = torch.empty(()).uniform_(self.min_scale, self.max_scale, generator=self.generator).item()
            new_len = int(round(old_len * scale))
            new_len = max(self.min_len, min(max_len, new_len))
            seq = new_motions[idx, :old_len].transpose(0, 1).unsqueeze(0)
            seq = F.interpolate(seq, size=new_len, mode="linear", align_corners=True)
            seq = seq.squeeze(0).transpose(0, 1)
            new_motions[idx].zero_()
            new_motions[idx, :new_len] = seq
            new_lens[idx] = new_len
            self.total_augmented += 1
        return captions, new_motions, new_lens

    def state_dict(self) -> dict:
        return {
            "policy": "feature_space_temporal_scale",
            "prob": self.prob,
            "min_scale": self.min_scale,
            "max_scale": self.max_scale,
            "min_len": self.min_len,
            "skip_keywords": self.skip_keywords,
            "total_seen": self.total_seen,
            "total_augmented": self.total_augmented,
            "total_skipped_keyword": self.total_skipped_keyword,
        }


class FormalVariantTrainer:
    def __init__(self, base_trainer, args: argparse.Namespace):
        self.base = base_trainer
        self.args = args
        self.use_aug = args.variant in {"aug", "aug_disploss"}
        self.use_disploss = args.variant in {"disploss", "aug_disploss"}
        if self.use_disploss and args.batch_size < 2:
            raise RuntimeError("DispLoss variants require batch_size >= 2 to form non-self feature pairs.")
        self.augmenter = TemporalScaleAugmenter(
            args.aug_prob,
            args.aug_min_scale,
            args.aug_max_scale,
            args.aug_min_len,
            args.aug_skip_keywords,
            args.seed + 17,
        )
        self.disp_feature = None
        self.disp_hook_handle = None
        self.disp_hook_calls = 0

    def __getattr__(self, name):
        return getattr(self.base, name)

    def attach_disp_hook(self) -> None:
        if not self.use_disploss:
            return
        model = self.base.accelerator.unwrap_model(self.base.model)
        module = get_module(model, self.args.disp_layer)

        def hook(_module, _inputs, output):
            self.disp_hook_calls += 1
            self.disp_feature = output

        self.disp_hook_handle = module.register_forward_hook(hook)

    def close(self) -> None:
        if self.disp_hook_handle is not None:
            self.disp_hook_handle.remove()
            self.disp_hook_handle = None

    def train_mode(self):
        self.base.train_mode()

    def forward(self, batch_data):
        if self.use_aug:
            caption, motions, m_lens = batch_data
            batch_data = self.augmenter.apply(caption, motions, m_lens)
        self.disp_feature = None
        return self.base.forward(batch_data)

    def update(self):
        self.base.zero_grad([self.base.optimizer])
        loss_logs = self.backward_G()
        self.base.accelerator.backward(self.base.loss)
        self.base.clip_norm([self.base.model])
        self.base.step([self.base.optimizer])
        return loss_logs

    def backward_G(self):
        loss_logs = self.base.backward_G()
        loss_logs["loss_total"] = self.base.loss
        if self.use_disploss:
            if self.disp_feature is None:
                raise RuntimeError(f"DispLoss hook did not capture layer '{self.args.disp_layer}'")
            disp = self.dispersion_loss(self.disp_feature)
            loss_logs["loss_disp"] = disp
            loss_logs["loss_total"] = loss_logs["loss_mot_rec"] + self.args.disp_lambda * disp
            self.base.loss = loss_logs["loss_total"]
        return loss_logs

    def dispersion_loss(self, feature: torch.Tensor) -> torch.Tensor:
        feature = feature.float()
        if feature.ndim == 3:
            pooled = feature.mean(dim=-1)
        elif feature.ndim == 2:
            pooled = feature
        else:
            pooled = feature.reshape(feature.shape[0], -1)
        pooled = F.normalize(pooled, dim=-1)
        sim = pooled @ pooled.t()
        eye = torch.eye(sim.shape[0], dtype=torch.bool, device=sim.device)
        off_diag = sim.masked_select(~eye)
        if off_diag.numel() == 0:
            return sim.sum() * 0.0
        return F.relu(off_diag - self.args.disp_margin).mean()

    def variant_state(self) -> dict:
        return {
            "variant": self.args.variant,
            "augmentation_enabled": self.use_aug,
            "augmentation": self.augmenter.state_dict(),
            "disploss_enabled": self.use_disploss,
            "disploss": {
                "layer": self.args.disp_layer,
                "lambda": self.args.disp_lambda,
                "margin": self.args.disp_margin,
                "feature_source": "real MotionCLR denoiser module forward hook",
                "hook_calls": self.disp_hook_calls,
            },
        }


def scalarize_logs(accelerator: Accelerator, log_dict: OrderedDict) -> dict:
    row = {}
    for key, value in log_dict.items():
        if torch.is_tensor(value):
            gathered = accelerator.gather(value.detach())
            row[key] = float(gathered.float().mean().item())
        else:
            row[key] = float(value)
    return row


def save_checkpoint(trainer, path: str, step: int) -> dict:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    trainer.save(path, step)
    return file_record(path)


def base_trainer(trainer):
    return trainer.base if isinstance(trainer, FormalVariantTrainer) else trainer


def evaluate_val_loss(trainer, val_loader, args: argparse.Namespace, accelerator: Accelerator, max_batches: int):
    base = base_trainer(trainer)
    was_training = base.model.training
    base.eval_mode()
    rows = []
    with torch.no_grad():
        for batch_idx, batch_data in enumerate(val_loader):
            if batch_idx >= max_batches:
                break
            base.forward(batch_data)
            log_dict = base.backward_G()
            log_dict["loss_total"] = base.loss
            row = {"val_batch": batch_idx}
            row.update(scalarize_logs(accelerator, log_dict))
            rows.append(row)
    if was_training:
        base.train_mode()
    if not rows:
        return {}
    keys = [key for key in rows[0] if key.startswith("loss")]
    return {f"val_{key}": sum(row[key] for row in rows) / len(rows) for key in keys}


def run_lite_eval(args: argparse.Namespace, opt, step: int) -> dict:
    if args.eval_interval <= 0:
        return {}
    if args.max_eval_fraction > 0 and args._train_elapsed_for_eval > 0:
        used = args._eval_elapsed_total
        budget = args._train_elapsed_for_eval * args.max_eval_fraction
        if used >= budget:
            return {"step": step, "status": "skipped_budget_exhausted", "used_sec": used, "budget_sec": budget}

    log_path = pjoin(args.out_dir, "eval_monitoring", f"step_{step:08d}.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    ckpt_path = pjoin(opt.model_dir, "latest.tar")
    command = [
        sys.executable,
        pjoin(os.path.dirname(__file__), "trace3_lite_eval.py"),
        "--repo_dir",
        args.repo_dir,
        "--opt_path",
        pjoin(opt.save_root, "opt.txt"),
        "--which_ckpt",
        "latest",
        "--gpu_id",
        str(args.eval_gpu_id),
        "--batch_size",
        str(args.eval_batch_size),
        "--num_inference_steps",
        str(args.eval_num_inference_steps),
        "--sample_limit",
        str(args.eval_sample_limit),
        "--log_path",
        log_path,
    ]
    if args.no_eff:
        command.append("--no_eff")
    if args.self_attention:
        command.append("--self_attention")
    command.append("--no_fp16")
    started = time.time()
    proc = subprocess.run(
        command,
        cwd=args.repo_dir,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=args.eval_timeout_sec,
    )
    elapsed = time.time() - started
    args._eval_elapsed_total += elapsed
    out_path = pjoin(args.out_dir, "eval_monitoring", f"step_{step:08d}_stdout.log")
    with open(out_path, "w") as f:
        f.write(proc.stdout)
    record = {
        "step": step,
        "status": "ok" if proc.returncode == 0 else "failed",
        "returncode": proc.returncode,
        "elapsed_sec": elapsed,
        "command": command,
        "log_file": file_record(log_path),
        "stdout_file": file_record(out_path),
        "checkpoint": file_record(ckpt_path),
    }
    metrics = parse_lite_eval_metrics(log_path)
    record.update(metrics)
    return record


def parse_lite_eval_metrics(path: str) -> dict:
    metrics = {}
    if not os.path.exists(path):
        return metrics
    patterns = {
        "eval_matching_score_text2motion": r"\[text2motion\] Matching Score:\s*([0-9.eE+-]+)",
        "eval_fid_text2motion": r"\[text2motion\] FID:\s*([0-9.eE+-]+)",
        "eval_diversity_text2motion": r"\[text2motion\] Diversity:\s*([0-9.eE+-]+)",
    }
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    for key, pat in patterns.items():
        found = re.findall(pat, text)
        if found:
            metrics[key] = float(found[-1])
    return metrics


def run_exact_train_loop(trainer, train_loader, val_loader, args: argparse.Namespace, opt, accelerator: Accelerator):
    started = time.time()
    logs = []
    val_logs = []
    eval_logs = []
    checkpoints = []
    base = base_trainer(trainer)
    base.model, base.mse_criterion, base.optimizer, train_loader, val_loader, base.model_ema = accelerator.prepare(
        base.model,
        base.mse_criterion,
        base.optimizer,
        train_loader,
        val_loader,
        base.model_ema,
    )
    if hasattr(trainer, "attach_disp_hook"):
        trainer.attach_disp_hook()

    step = 0
    epoch = 0
    try:
        while step < args.target_steps:
            trainer.train_mode()
            for inner_iter, batch_data in enumerate(train_loader):
                if step >= args.target_steps:
                    break
                trainer.forward(batch_data)
                log_dict = trainer.update()
                step += 1
                row = {"step": step, "epoch": epoch, "inner_iter": inner_iter}
                row.update(scalarize_logs(accelerator, log_dict))
                if any(not torch.isfinite(torch.tensor(value)) for key, value in row.items() if key.startswith("loss")):
                    raise RuntimeError(f"Non-finite loss at step {step}: {row}")
                logs.append(row)

                if trainer.model_ema and step % opt.model_ema_steps == 0:
                    accelerator.unwrap_model(trainer.model_ema).update_parameters(trainer.model)

                if accelerator.is_main_process and hasattr(trainer, "writer"):
                    trainer.writer.add_scalar("train/loss_total", row.get("loss_total", row["loss_mot_rec"]), step)
                    trainer.writer.add_scalar("train/loss_mot_rec", row["loss_mot_rec"], step)
                    if "loss_disp" in row:
                        trainer.writer.add_scalar("train/loss_disp", row["loss_disp"], step)

                if args.val_interval > 0 and step % args.val_interval == 0:
                    val_row = {"step": step}
                    val_row.update(evaluate_val_loss(trainer, val_loader, args, accelerator, args.val_batches))
                    val_logs.append(val_row)
                    if accelerator.is_main_process and hasattr(trainer, "writer"):
                        for key, value in val_row.items():
                            if key.startswith("val_loss"):
                                trainer.writer.add_scalar("val/" + key.replace("val_", ""), value, step)

                if args.eval_interval > 0 and step % args.eval_interval == 0 and accelerator.is_main_process:
                    checkpoints.append(save_checkpoint(trainer, pjoin(opt.model_dir, "latest.tar"), step))
                    args._train_elapsed_for_eval = time.time() - started
                    eval_row = run_lite_eval(args, opt, step)
                    eval_logs.append(eval_row)
                    if hasattr(trainer, "writer"):
                        for key, value in eval_row.items():
                            if key.startswith("eval_") and isinstance(value, (float, int)):
                                trainer.writer.add_scalar("eval/" + key.replace("eval_", ""), value, step)

                if args.save_interval > 0 and step % args.save_interval == 0 and accelerator.is_main_process:
                    checkpoints.append(save_checkpoint(trainer, pjoin(opt.model_dir, f"step_{step:08d}.tar"), step))
                    checkpoints.append(save_checkpoint(trainer, pjoin(opt.model_dir, "latest.tar"), step))

                if trainer.scheduler is not None and step % opt.update_lr_steps == 0:
                    trainer.scheduler.step()
                accelerator.wait_for_everyone()
            epoch += 1

        if accelerator.is_main_process:
            checkpoints.append(save_checkpoint(trainer, pjoin(opt.model_dir, "latest.tar"), step))
            checkpoints.append(save_checkpoint(trainer, pjoin(opt.model_dir, f"final_step_{step:08d}.tar"), step))
        accelerator.wait_for_everyone()
    finally:
        if hasattr(trainer, "close"):
            trainer.close()

    return logs, val_logs, eval_logs, checkpoints, time.time() - started, step


def write_git_diff(repo_dir: str, out_dir: str) -> dict:
    diff_path = pjoin(out_dir, "git_diff.patch")
    diff = subprocess.run(["git", "diff"], cwd=repo_dir, check=False, text=True, stdout=subprocess.PIPE).stdout
    with open(diff_path, "w") as f:
        f.write(diff)
    return file_record(diff_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo_dir", default="/data/public/ripemangobox/Motion/MotionCLR")
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--variant", required=True, choices=sorted(VARIANTS))
    parser.add_argument(
        "--run_scope",
        default="formal_training_candidate",
        choices=["formal_training_candidate", "dev_validation_only"],
    )
    parser.add_argument("--target_steps", type=int, required=True)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--dropout", type=float, default=0.1)
    parser.add_argument("--log_every", type=int, default=50)
    parser.add_argument("--save_interval", type=int, default=5000)
    parser.add_argument("--val_interval", type=int, default=1000)
    parser.add_argument("--val_batches", type=int, default=8)
    parser.add_argument("--eval_interval", type=int, default=5000)
    parser.add_argument("--eval_sample_limit", type=int, default=64)
    parser.add_argument("--eval_batch_size", type=int, default=32)
    parser.add_argument("--eval_num_inference_steps", type=int, default=10)
    parser.add_argument("--eval_gpu_id", type=int, default=0)
    parser.add_argument("--eval_timeout_sec", type=int, default=1800)
    parser.add_argument("--max_eval_fraction", type=float, default=0.1)
    parser.add_argument("--model_ema", action="store_true")
    parser.add_argument("--no_eff", action="store_true")
    parser.add_argument("--self_attention", action="store_true")
    parser.add_argument("--edit_mode", action="store_true")
    parser.add_argument("--aug_prob", type=float, default=0.5)
    parser.add_argument("--aug_min_scale", type=float, default=0.875)
    parser.add_argument("--aug_max_scale", type=float, default=1.125)
    parser.add_argument("--aug_min_len", type=int, default=40)
    parser.add_argument(
        "--aug_skip_keywords",
        default="left,right,clockwise,counterclockwise,anticlockwise,slow,slowly,fast,quick,quickly",
    )
    parser.add_argument("--disp_layer", default="unet.mid_block2")
    parser.add_argument("--disp_lambda", type=float, default=0.02)
    parser.add_argument("--disp_margin", type=float, default=0.2)
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    os.chdir(args.repo_dir)
    sys.path.insert(0, args.repo_dir)
    set_seed(args.seed)
    args._eval_elapsed_total = 0.0
    args._train_elapsed_for_eval = 0.0

    from models import build_models
    from motion_loader import get_dataset_loader
    from trainers import DDPMTrainer
    from utils.ema import ExponentialMovingAverage

    accelerator = Accelerator()
    opt = parse_train_options(args, accelerator)
    opt.save_root = pjoin(opt.checkpoints_dir, opt.dataset_name, opt.name)
    opt.model_dir = pjoin(opt.save_root, "model")
    opt.meta_dir = pjoin(opt.save_root, "meta")
    if accelerator.is_main_process:
        os.makedirs(opt.model_dir, exist_ok=True)
        os.makedirs(opt.meta_dir, exist_ok=True)

    edit_config = yaml_to_box("options/edit.yaml" if opt.edit_mode else "options/noedit.yaml")
    train_loader = get_dataset_loader(opt, batch_size=opt.batch_size, split="train", accelerator=accelerator, mode="train")
    val_loader = get_dataset_loader(opt, batch_size=opt.batch_size, split="val", accelerator=accelerator, mode="eval")
    model = build_models(opt, edit_config=edit_config)
    model_ema = None
    if opt.model_ema:
        adjust = 106_667 * opt.model_ema_steps / max(1, opt.num_train_steps)
        alpha = min(1.0, (1.0 - opt.model_ema_decay) * adjust)
        model_ema = ExponentialMovingAverage(model, decay=1.0 - alpha)

    base_trainer = DDPMTrainer(opt, model, accelerator, model_ema)
    trainer = base_trainer if args.variant == "baseline" else FormalVariantTrainer(base_trainer, args)
    loss_rows, val_rows, eval_rows, checkpoints, elapsed_sec, actual_steps = run_exact_train_loop(
        trainer, train_loader, val_loader, args, opt, accelerator
    )

    if accelerator.is_main_process:
        loss_path = pjoin(args.out_dir, "loss_steps.json")
        with open(loss_path, "w") as f:
            json.dump(loss_rows, f, indent=2)
        val_path = pjoin(args.out_dir, "val_steps.json")
        with open(val_path, "w") as f:
            json.dump(val_rows, f, indent=2)
        eval_path = pjoin(args.out_dir, "eval_steps.json")
        with open(eval_path, "w") as f:
            json.dump(eval_rows, f, indent=2)
        git_diff = write_git_diff(args.repo_dir, args.out_dir)
        data_root = pjoin(args.repo_dir, "data", "HumanML3D")
        manifest = {
            "trace": "Trace 3",
            "line": "Line 3",
            "old_name": "Track A",
            "variant": args.variant,
            "experiment_scope": args.run_scope,
            "paper_level_status": "not_final_until_official_evaluator_metrics",
            "repo_dir": args.repo_dir,
            "git_head": run(["git", "rev-parse", "HEAD"], args.repo_dir),
            "git_branch": run(["git", "branch", "--show-current"], args.repo_dir),
            "git_status_short": run(["git", "status", "--short"], args.repo_dir).splitlines(),
            "git_diff_stat": run(["git", "diff", "--stat"], args.repo_dir).splitlines(),
            "git_diff_file": git_diff,
            "command": " ".join(sys.argv),
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
            "python": sys.version,
            "platform": platform.platform(),
            "torch_version": torch.__version__,
            "cuda_version": torch.version.cuda,
            "device": str(accelerator.device),
            "dataset": {
                "name": "HumanML3D",
                "repo_path": data_root,
                "split": "train",
                "debug": bool(getattr(opt, "debug", False)),
                "train_rows": split_line_count(pjoin(data_root, "train.txt")),
                "val_rows": split_line_count(pjoin(data_root, "val.txt")),
                "test_rows": split_line_count(pjoin(data_root, "test.txt")),
                "train_split": file_record(pjoin(data_root, "train.txt")),
                "val_split": file_record(pjoin(data_root, "val.txt")),
                "test_split": file_record(pjoin(data_root, "test.txt")),
                "mean": file_record(pjoin(data_root, "Mean.npy")),
                "std": file_record(pjoin(data_root, "Std.npy")),
            },
            "training": {
                "target_steps": args.target_steps,
                "actual_steps": actual_steps,
                "batch_size": args.batch_size,
                "seed": args.seed,
                "lr": args.lr,
                "dropout": args.dropout,
                "save_interval": args.save_interval,
                "val_interval": args.val_interval,
                "val_batches": args.val_batches,
                "eval_interval": args.eval_interval,
                "eval_sample_limit": args.eval_sample_limit,
                "eval_num_inference_steps": args.eval_num_inference_steps,
                "eval_time_budget_fraction": args.max_eval_fraction,
                "eval_elapsed_total_sec": args._eval_elapsed_total,
                "model_ema": bool(opt.model_ema),
                "no_eff": bool(opt.no_eff),
                "self_attention": bool(opt.self_attention),
                "exact_stop_enforced": actual_steps == args.target_steps,
            },
            "variant_config": (
                {"variant": "baseline", "augmentation_enabled": False, "disploss_enabled": False}
                if args.variant == "baseline"
                else trainer.variant_state()
            ),
            "checkpoints": checkpoints,
            "loss_steps_file": file_record(loss_path),
            "val_steps_file": file_record(val_path),
            "eval_steps_file": file_record(eval_path),
            "elapsed_sec": elapsed_sec,
            "official_eval_required_after_training": True,
            "limitations": [
                "This script performs true MotionCLR/HumanML3D training updates and checkpointing.",
                "It does not compute final FID/R-Precision/Matching Score; official evaluation must run after training.",
                "Feature-space temporal scaling and denoiser-feature DispLoss are candidate policies pending DS approval.",
            ],
        }
        with open(pjoin(args.out_dir, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=2)
        with open(pjoin(args.out_dir, "PENDING_EVAL_NOTICE.txt"), "w") as f:
            f.write(f"EXPERIMENT_SCOPE={args.run_scope}\n")
            if args.run_scope == "dev_validation_only":
                f.write("DEV_VALIDATION_ONLY=true\n")
            f.write("PAPER_LEVEL_STATUS=not_final_until_official_evaluator_metrics\n")
            f.write("OFFICIAL_EVAL_REQUIRED=true\n")
        print(json.dumps({"manifest": pjoin(args.out_dir, "manifest.json"), "actual_steps": actual_steps}, indent=2))


if __name__ == "__main__":
    main()
