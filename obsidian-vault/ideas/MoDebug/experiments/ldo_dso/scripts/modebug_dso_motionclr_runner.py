#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from os.path import join as pjoin

import torch


def import_motionclr_trace_helpers() -> object:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidate_roots = [
        os.path.abspath(os.path.join(script_dir, "..", "..")),
        os.path.abspath(os.path.join(script_dir, "..", "..", "..")),
    ]
    helper_dirs = []
    for modebug_root in candidate_roots:
        helper_dirs.extend(
            [
                os.path.join(modebug_root, "scripts"),
                os.path.join(modebug_root, "motionclr", "scripts"),
            ]
        )
    for helper_dir in helper_dirs:
        helper_path = os.path.join(helper_dir, "trace1_full_eval_attention_intervention.py")
        if os.path.isfile(helper_path):
            sys.path.insert(0, helper_dir)
            import trace1_full_eval_attention_intervention as helpers

            return helpers
    raise ModuleNotFoundError(
        "Could not find trace1_full_eval_attention_intervention.py in: " + ", ".join(helper_dirs)
    )


class DSOPipeline:
    def __init__(self, base_pipeline, seed: int, cutoff_step: int) -> None:
        self.base = base_pipeline
        self.seed = seed
        self.cutoff_step = cutoff_step
        self.model = base_pipeline.model
        self.opt = base_pipeline.opt
        self.device = base_pipeline.device
        self.torch_dtype = base_pipeline.torch_dtype
        self.num_inference_steps = base_pipeline.num_inference_steps
        self.cfg_scale = base_pipeline.cfg_scale
        self.scheduler = base_pipeline.scheduler

    def generate_batch(self, caption, m_lens):
        helpers = import_motionclr_trace_helpers()
        batch_size = len(caption)
        max_len = m_lens.max()
        sample = torch.randn((batch_size, max_len, self.model.input_feats), device=self.device, dtype=self.torch_dtype)

        self.scheduler.set_timesteps(self.num_inference_steps, self.device)
        timesteps = [torch.tensor([t] * batch_size, device=self.device).long() for t in self.scheduler.timesteps]
        enc_text = self.model.encode_text(caption, self.device)

        effective_cutoff = min(max(1, int(self.cutoff_step)), len(timesteps))
        for step_idx, t in enumerate(timesteps, start=1):
            with torch.no_grad():
                if getattr(self.model, "cond_mask_prob", 0) > 0:
                    predict = self.model.forward_with_cfg(sample, t, enc_text=enc_text, cfg_scale=self.cfg_scale)
                else:
                    predict = self.model(sample, t, enc_text=enc_text)
            sample = self.scheduler.step(predict, t[0], sample).prev_sample
            if step_idx >= effective_cutoff:
                break
        return sample

    def generate(self, caption, m_lens, batch_size=32):
        import math
        import tqdm

        helpers = import_motionclr_trace_helpers()
        helpers.seed_everything(self.seed)
        count = len(caption)
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
            elapsed_sum += now_time - start_time
            timed_batches += 1
            for i in range(output.shape[0]):
                outputs.append(output[i, : batch_m_lens[i]])
            cur_idx += batch_size

        t_eval = elapsed_sum / max(1, timed_batches)
        print(
            "DSO cutoff_step=%d/%d average batch generation time (bs=%d): %f seconds"
            % (self.cutoff_step, self.num_inference_steps, batch_size, t_eval)
        )
        return outputs, t_eval


def parse_endpoints(value: str, total_steps: int) -> list[int]:
    if value == "thirds":
        raw = [max(1, round(total_steps / 3)), max(1, round(2 * total_steps / 3)), total_steps]
    elif value == "ac3d":
        raw = [max(1, round(total_steps * 0.1)), max(1, round(total_steps * 0.4)), max(1, round(total_steps * 0.7)), total_steps]
    else:
        raw = [int(part.strip()) for part in value.split(",") if part.strip()]
    endpoints = []
    for item in raw:
        item = min(max(1, int(item)), total_steps)
        if item not in endpoints:
            endpoints.append(item)
    return endpoints


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo_dir", default="/data/public/ripemangobox/Motion/MotionCLR")
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--gpu_id", type=int, default=1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--opt_path", default="./checkpoints/t2m/release/opt.txt")
    parser.add_argument("--which_ckpt", default="latest")
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--replication_times", type=int, default=1)
    parser.add_argument("--num_inference_steps", type=int, default=10)
    parser.add_argument("--dso_endpoints", default="ac3d")
    parser.add_argument("--cfg_scale", type=float, default=2.5)
    parser.add_argument("--evaluator_dir", default="./data/pretrained_models")
    parser.add_argument("--eval_meta_dir", default="./data")
    parser.add_argument("--glove_dir", default="./data/glove")
    parser.add_argument("--no_eff", action="store_true", default=True)
    parser.add_argument("--self_attention", action="store_true", default=True)
    parser.add_argument("--no_fp16", action="store_true", default=True)
    parser.add_argument("--no_ema", action="store_true")
    parser.add_argument("--edit_mode", action="store_true")
    args = parser.parse_args()

    started = time.time()
    os.makedirs(args.out_dir, exist_ok=True)
    os.chdir(args.repo_dir)
    sys.path.insert(0, args.repo_dir)
    helpers = import_motionclr_trace_helpers()

    from datasets import get_dataset
    from eval import EvaluatorModelWrapper, evaluation
    from models import build_models
    from motion_loader import get_dataset_loader, get_motion_loader
    from utils.model_load import load_model_weights

    helpers.seed_everything(args.seed)
    opt = helpers.parse_test_options(args)
    opt.save_root = args.out_dir
    device = torch.device(f"cuda:{args.gpu_id}" if torch.cuda.is_available() else "cpu")
    if torch.cuda.is_available():
        torch.cuda.set_device(device)
    opt.device = device

    edit_config = helpers.yaml_to_box("options/edit.yaml" if opt.edit_mode else "options/noedit.yaml")
    eval_wrapper = EvaluatorModelWrapper(opt)
    gt_loader = get_dataset_loader(opt, opt.batch_size, mode="gt_eval", split="test")
    gen_dataset = get_dataset(opt, mode="eval", split="test")

    model = build_models(opt, edit_config=edit_config)
    ckpt_path = pjoin(opt.model_dir, opt.which_ckpt + ".tar")
    evaluator_ckpt = helpers.evaluator_checkpoint(args.evaluator_dir)
    if not os.path.isfile(ckpt_path):
        raise RuntimeError(f"Missing checkpoint: {ckpt_path}")
    if not os.path.isfile(evaluator_ckpt):
        raise RuntimeError(f"Missing evaluator checkpoint: {evaluator_ckpt}")
    total_it = load_model_weights(model, ckpt_path, use_ema=not opt.no_ema, device=device)

    base_pipeline = helpers.LocalInterventionPipeline(
        opt=opt,
        model=model,
        diffuser_name=opt.diffuser_name,
        device=device,
        num_inference_steps=opt.num_inference_steps,
        torch_dtype=torch.float32 if opt.no_fp16 else torch.float16,
        cfg_scale=args.cfg_scale,
    )
    model = base_pipeline.model
    model.eval()

    endpoints = parse_endpoints(args.dso_endpoints, args.num_inference_steps)
    log_file = pjoin(args.out_dir, "eval_stdout_stderr.log")
    with open(log_file, "w") as f:
        f.write("------------ MoDebug MotionCLR DSO official evaluator -------------\n")
        f.write(f"endpoints: {endpoints}\n")
        f.write(f"num_inference_steps: {args.num_inference_steps}\n")
        f.write(f"seed: {args.seed}\n")
        f.write("-------------- End ----------------\n")

    eval_motion_loaders = {}
    for endpoint in endpoints:
        name = f"text2motion_dso_step_{endpoint:02d}_of_{args.num_inference_steps:02d}"

        def make_loader(step: int):
            return lambda: get_motion_loader(
                opt,
                opt.batch_size,
                DSOPipeline(base_pipeline, seed=args.seed, cutoff_step=step),
                gen_dataset,
                opt.mm_num_samples,
                opt.mm_num_repeats,
            )

        eval_motion_loaders[name] = make_loader(endpoint)

    for rep_idx in range(args.replication_times):
        helpers.seed_everything(args.seed + rep_idx)
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

    metrics = helpers.parse_eval_log(log_file)
    summary_path = pjoin(args.out_dir, "metrics_summary.json")
    with open(summary_path, "w") as f:
        json.dump(metrics, f, indent=2)

    manifest = {
        "trace": "LDO/DSO",
        "scope": "motionclr_diffusion_step_output_official_evaluator",
        "paper_level_status": "full_evaluator_metrics_computed",
        "baseline": "MotionCLR",
        "diagnostic": "DSO",
        "repo_dir": args.repo_dir,
        "git_head": helpers.run(["git", "rev-parse", "HEAD"], args.repo_dir),
        "git_branch": helpers.run(["git", "branch", "--show-current"], args.repo_dir),
        "git_status_short": helpers.run(["git", "status", "--short"], args.repo_dir).splitlines(),
        "command": " ".join(sys.argv),
        "wrapper_script": helpers.file_record(os.path.abspath(__file__)),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        "device": str(device),
        "seed": args.seed,
        "replication_times": args.replication_times,
        "num_inference_steps": args.num_inference_steps,
        "dso_endpoints": endpoints,
        "endpoint_policy": args.dso_endpoints,
        "cfg_scale": args.cfg_scale,
        "batch_size": args.batch_size,
        "checkpoint_path": ckpt_path,
        "checkpoint_sha256": helpers.sha256(ckpt_path),
        "evaluator_checkpoint": evaluator_ckpt,
        "evaluator_checkpoint_sha256": helpers.sha256(evaluator_ckpt),
        "log_file": log_file,
        "metrics_summary_file": summary_path,
        "metrics_summary_sha256": helpers.sha256(summary_path),
        "metrics": metrics,
        "limitations": [
            "DSO evaluates noisy intermediate scheduler samples as motion outputs; early endpoints are diagnostic, not normal generation quality claims.",
            "All endpoints reset the same seed before generation so comparisons share the same initial noise as much as the official loader permits.",
            "This DSO implementation is valid for MotionCLR diffusion sampling only; MoLingo flow/masked iterative steps are not counted as diffusion DSO here.",
        ],
        "failures": [],
        "elapsed_sec": time.time() - started,
        "total_it": total_it,
    }
    manifest_path = pjoin(args.out_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(json.dumps({"manifest": manifest_path, "metrics_summary": summary_path}, indent=2))


if __name__ == "__main__":
    main()
