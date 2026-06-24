---
title: "SALAD KIT Denoiser Runtime Smoke"
created: 2026-05-15T20:36:00+08:00
updated: 2026-05-15T20:36:00+08:00
status: active
tags:
  - MoDebug
  - SALAD
  - runtime-smoke
  - status/diagnostic
role: diagnostic
used_for: observation
---

# SALAD KIT Denoiser Runtime Smoke

## Summary

2026-05-15 在 4090 上继续补齐 SALAD / EventT2M runtime，目标是验证 SALAD official `train_denoiser.py` 能否从依赖、VAE checkpoint、CLIP、KIT data、official evaluator、1-epoch train、validation、epoch eval 走到正常退出。

结论：`event-t2m` 环境已能完成 SALAD KIT denoiser official smoke。最终成功 run 为 `modebug_smoke_kit_denoiser_20260515g`，`exit_code: 0`，生成 denoiser checkpoint、TensorBoard event 和 8 个 mp4 animation。

## Provenance

Remote host / repo:

```text
host: user-SYS-7049GP-TRT
repo: /data/public/ripemangobox/Motion/SALAD
controller repo: /data/public/ripemangobox/Motion/EventT2M-codes
env: event-t2m
date: 2026-05-15
```

Fetched local logs:

```text
artifacts/remote4090/remote4090_logs_20260515_salad_denoiser/modebug_salad_event_env_repair_0515c.log
artifacts/remote4090/remote4090_logs_20260515_salad_denoiser/modebug_sklearn_fix_0515c.log
artifacts/remote4090/remote4090_logs_20260515_salad_denoiser/modebug_salad_import_wrapper_probe_0515f.log
artifacts/remote4090/remote4090_logs_20260515_salad_denoiser/modebug_salad_denoiser_train_wrapper_0515f.log
artifacts/remote4090/remote4090_logs_20260515_salad_denoiser/modebug_salad_denoiser_train_plotfix_0515g.log
```

Remote git provenance was archived through `remote4090` before the continuation run:

```text
logs/remote4090/git_archive/continue_019e2a83_salad_env_smoke_20260515_$(date +%Y%m%d_%H%M%S)
```

## Environment Repairs

Completed environment gates:

- Installed `tensorboard`, `joblib`, and related dependencies into `event-t2m`.
- Reinstalled `scikit-learn==1.3.2` from a Python 3.10 wheel; this fixed the stale `sklearn.__check_build` issue.
- Verified `openai/clip-vit-base-patch32` loads through HuggingFace mirror.
- Added a temporary `ffmpeg` symlink from `imageio_ffmpeg` into `PATH` for smoke commands.

Temporary overlays used only for smoke:

- `sitecustomize.py` restores old NumPy aliases needed by SALAD legacy code: `np.float`, `np.int`.
- `visualization.joints2bvh` is stubbed because denoiser train/test with `save_motion=False` does not need BVH export, while the original module imports old `numpy.core.umath_tests`.
- `utils.plot_script` is shadowed only in the final successful run to replace `ax.lines = []` / `ax.collections = []` with artist removal, fixing a matplotlib API incompatibility.

These overlays were under `/tmp/modebug_salad_overlay_0515*` and did not modify the SALAD repo source.

## Successful Smoke

Command role: `diagnostic`

Protocol:

```text
official train_denoiser.py via runpy wrapper
dataset_name: kit
name: modebug_smoke_kit_denoiser_20260515g
vae_name: modebug_smoke_kit_vae_ffmpeg_20260515
max_epoch: 1
batch_size: 256
num_workers: 0
num_inference_timesteps: 2
eval_every_e: 1
timeout: 900s
```

Runtime path:

```text
VAE checkpoint load -> CLIP text encoder load -> KIT evaluator load -> KIT data load -> initial official eval -> 17 train iterations -> validation -> epoch 1 official eval -> animation export -> exit_code 0
```

Remote outputs:

```text
checkpoints/kit/modebug_smoke_kit_denoiser_20260515g/model/latest.tar
checkpoints/kit/modebug_smoke_kit_denoiser_20260515g/model/net_best_fid.tar
checkpoints/kit/modebug_smoke_kit_denoiser_20260515g/model/net_best_matching.tar
checkpoints/kit/modebug_smoke_kit_denoiser_20260515g/opt.txt
log/kit/modebug_smoke_kit_denoiser_20260515g/events.out.tfevents.1778848248.user-SYS-7049GP-TRT.2689734.0
checkpoints/kit/modebug_smoke_kit_denoiser_20260515g/animation/E0001/00.mp4
checkpoints/kit/modebug_smoke_kit_denoiser_20260515g/animation/E0001/01.mp4
checkpoints/kit/modebug_smoke_kit_denoiser_20260515g/animation/E0001/02.mp4
checkpoints/kit/modebug_smoke_kit_denoiser_20260515g/animation/E0001/03.mp4
checkpoints/kit/modebug_smoke_kit_denoiser_20260515g/animation/E0001/04.mp4
checkpoints/kit/modebug_smoke_kit_denoiser_20260515g/animation/E0001/05.mp4
checkpoints/kit/modebug_smoke_kit_denoiser_20260515g/animation/E0001/06.mp4
checkpoints/kit/modebug_smoke_kit_denoiser_20260515g/animation/E0001/07.mp4
```

## Metric Role

The official SALAD evaluator printed KIT smoke metrics during epoch 0 and epoch 1. These are runtime diagnostics only.

Metric provenance:

- date: 2026-05-15
- artifact_path: `artifacts/remote4090/remote4090_logs_20260515_salad_denoiser/modebug_salad_denoiser_train_plotfix_0515g.log`
- evaluator: SALAD official KIT evaluator wrapper from `checkpoints/kit/Comp_v6_KLD005/opt.txt`
- protocol: 1-epoch KIT denoiser smoke, `num_inference_timesteps=2`
- motion_source: SALAD smoke-generated KIT denoiser outputs
- condition_pair: not a MoDebug counterfactual pair
- n/evaluable: 9 official eval batches in log
- coverage: runtime/evaluator path coverage only
- role: `diagnostic`
- used_for: observation
- limitations: not a held-out final evaluator, not a MoDebug method result, not evidence for event completion or cross-generator generality

Do not cite these printed metrics as final model quality evidence.

## Remaining Notes

This closes the SALAD KIT denoiser runtime-smoke gate for environment readiness. It does not establish MoDebug intervention quality, event completion quality, or cross-generator generality.

Potential cleanup later:

- Replace temporary overlay fixes with a minimal reproducible launch script if SALAD becomes an active P0 generator.
- Decide whether to patch SALAD `utils/plot_script.py` locally in a linked codebase fork, rather than relying on `/tmp` overlay.
- Run `test_denoiser.py` separately if a post-train official test smoke is needed; it uses `save_motion=False` and should avoid BVH export.
