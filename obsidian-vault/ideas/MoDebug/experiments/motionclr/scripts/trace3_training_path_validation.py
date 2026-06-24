#!/usr/bin/env python
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from collections import OrderedDict
from os.path import join as pjoin

import torch
import yaml
from accelerate import Accelerator
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


def parse_train_options(repo_dir, out_dir, name, batch_size, max_steps, seed, save_checkpoint, accelerator):
    sys.path.insert(0, repo_dir)
    from options.train_options import TrainOptions

    old_argv = sys.argv[:]
    try:
        sys.argv = [
            "trace3_training_path_validation.py",
            "--name",
            name,
            "--dataset_name",
            "t2m",
            "--dropout",
            "0.1",
            "--lr",
            "1e-4",
            "--no_eff",
            "--self_attention",
            "--edit_mode",
            "--debug",
            "--batch_size",
            str(batch_size),
            "--num_train_steps",
            str(max_steps),
            "--log_every",
            "1",
            "--save_interval",
            "100000000",
            "--checkpoints_dir",
            pjoin(out_dir, "checkpoints"),
            "--seed",
            str(seed),
        ]
        if save_checkpoint:
            sys.argv.extend(["--model-ema"])
        opt = TrainOptions().parse(accelerator)
        return opt
    finally:
        sys.argv = old_argv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo_dir", default="/data/public/ripemangobox/Motion/MotionCLR")
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--name", default="trace3_training_path_validation")
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--max_steps", type=int, default=3)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--save_checkpoint", action="store_true")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    os.chdir(args.repo_dir)
    sys.path.insert(0, args.repo_dir)
    set_seed(args.seed)

    from models import build_models
    from motion_loader import get_dataset_loader
    from trainers import DDPMTrainer
    from utils.ema import ExponentialMovingAverage

    accelerator = Accelerator()
    opt = parse_train_options(args.repo_dir, args.out_dir, args.name, args.batch_size, args.max_steps, args.seed, args.save_checkpoint, accelerator)
    opt.save_root = pjoin(opt.checkpoints_dir, opt.dataset_name, opt.name)
    opt.model_dir = pjoin(opt.save_root, "model")
    opt.meta_dir = pjoin(opt.save_root, "meta")
    if accelerator.is_main_process:
        os.makedirs(opt.model_dir, exist_ok=True)
        os.makedirs(opt.meta_dir, exist_ok=True)

    edit_config = yaml_to_box("options/edit.yaml")
    train_loader = get_dataset_loader(opt, batch_size=opt.batch_size, split="train", accelerator=accelerator, mode="train")
    model = build_models(opt, edit_config=edit_config)
    model_ema = None
    if opt.model_ema:
        adjust = 106_667 * opt.model_ema_steps / max(1, opt.num_train_steps)
        alpha = min(1.0, (1.0 - opt.model_ema_decay) * adjust)
        model_ema = ExponentialMovingAverage(model, decay=1.0 - alpha)

    trainer = DDPMTrainer(opt, model, accelerator, model_ema)
    trainer.model, trainer.mse_criterion, trainer.optimizer, train_loader, trainer.model_ema = accelerator.prepare(
        trainer.model,
        trainer.mse_criterion,
        trainer.optimizer,
        train_loader,
        trainer.model_ema,
    )

    started = time.time()
    loss_rows = []
    it = 0
    trainer.train_mode()
    for batch_data in train_loader:
        trainer.forward(batch_data)
        log_dict = trainer.update()
        it += 1
        row = {"step": it}
        for key, value in log_dict.items():
            row[key] = float(accelerator.gather(value.detach()).mean().item())
        loss_rows.append(row)
        if trainer.model_ema and it % opt.model_ema_steps == 0:
            accelerator.unwrap_model(trainer.model_ema).update_parameters(trainer.model)
        if it >= args.max_steps:
            break

    checkpoint_info = None
    if args.save_checkpoint and accelerator.is_main_process:
        ckpt_path = pjoin(opt.model_dir, "validation_latest.tar")
        trainer.save(ckpt_path, it)
        checkpoint_info = {"path": ckpt_path, "sha256": sha256(ckpt_path), "size_bytes": os.path.getsize(ckpt_path)}

    accelerator.wait_for_everyone()
    if accelerator.is_main_process:
        loss_path = pjoin(args.out_dir, "loss_steps.json")
        with open(loss_path, "w") as f:
            json.dump(loss_rows, f, indent=2)
        manifest = {
            "trace": "Trace 3",
            "old_name": "Track A",
            "formal_data_status": "engineering_validation_only",
            "purpose": "Bounded validation of real HumanML3D MotionCLR training path with exact step stop.",
            "repo_dir": args.repo_dir,
            "git_head": run(["git", "rev-parse", "HEAD"], args.repo_dir),
            "git_branch": run(["git", "branch", "--show-current"], args.repo_dir),
            "git_status_short": run(["git", "status", "--short"], args.repo_dir).splitlines(),
            "git_diff_stat": run(["git", "diff", "--stat"], args.repo_dir).splitlines(),
            "command": " ".join(sys.argv),
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
            "device": str(accelerator.device),
            "dataset": {
                "name": "HumanML3D",
                "repo_path": "/data/public/ripemangobox/Motion/MotionCLR/data/HumanML3D",
                "split": "train",
                "debug": True,
            },
            "seed": args.seed,
            "batch_size": args.batch_size,
            "requested_max_steps": args.max_steps,
            "actual_steps": it,
            "loss_steps_file": loss_path,
            "loss_steps_sha256": sha256(loss_path),
            "checkpoint": checkpoint_info,
            "elapsed_sec": time.time() - started,
            "limitations": [
                "Bounded validation only; not formal training evidence.",
                "No DispLoss or augmentation is implemented in this script.",
                "No formal evaluator metrics are computed.",
            ],
        }
        with open(pjoin(args.out_dir, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=2)
        with open(pjoin(args.out_dir, "NONFORMAL_NOTICE.txt"), "w") as f:
            f.write("FORMAL_DATA_STATUS=engineering_validation_only\nDO_NOT_USE_FOR_FORMAL_CLAIMS=true\n")
        print(json.dumps({"manifest": pjoin(args.out_dir, "manifest.json"), "loss_steps": loss_rows}, indent=2))


if __name__ == "__main__":
    main()
