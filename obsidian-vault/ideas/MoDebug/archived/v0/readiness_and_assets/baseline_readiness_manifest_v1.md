---
title: "MoDebug P0 Baseline Readiness Manifest v1"
created: 2026-04-23T01:35
updated: 2026-04-26T02:31
status: archived
tags:
  - Motion_Generation
  - MoDebug
  - p0
  - readiness
related_exec:
  - '[[paperIDEAs/MoDebug/2026-04-22_modebug-exec-plan-alignment-first|MoDebug Exec]]'
---

# MoDebug P0 Baseline Readiness Manifest v1

## 状态定义

- `runnable`
- `partial`
- `blocked`
- `paper-only`

## Baseline 状态

### Event-T2M

- status: `runnable`
- canonical repo: `[[linkedCodebases/EventT2M-codes-main]]`
- evidence:
  - `environment.yml` 与 `requirements.txt` 已在 repo 内。
  - pretrained checkpoint 已在位：
    - `[[linkedCodebases/EventT2M-codes-main/checkpoints/pretrained/HumanML3D/hml3d.ckpt]]`
    - `[[linkedCodebases/EventT2M-codes-main/checkpoints/pretrained/KIT-ML/kit.ckpt]]`
  - 2026-04-23 当前环境 smoke 已成功：
    - command:
      - `conda run --no-capture-output -n event-t2m python src/sample_motion.py repeats=1 device=0 sample_name=taskb_smoke ckpt_path=checkpoints/pretrained/HumanML3D/hml3d.ckpt save_path=./logs/task_b_smoke_sample/ hydra.run.dir=./logs/task_b_smoke_hydra/2026-04-23_run01`
    - artifacts:
      - `[[linkedCodebases/EventT2M-codes-main/logs/task_b_smoke_sample/gen_joints/generated/taskb_smoke_0.npz]]`
      - `[[linkedCodebases/EventT2M-codes-main/logs/task_b_smoke_hydra/2026-04-23_run01/visual.log]]`
  - 历史 eval 痕迹仍在：
    - `[[linkedCodebases/EventT2M-codes-main/logs/eval/runs/2026-04-04_20-43-20/metrics.json]]`
    - `[[linkedCodebases/EventT2M-codes-main/logs/eval/runs/2026-04-04_20-43-20/eval.log]]`
- note:
  - 当前已验证最小单次 sample smoke；retrieval-only 路径本轮没有单独重跑。

### ActionPlan

- status: `runnable`
- canonical repo: `[[linkedCodebases/ActionPlan-Code]]`
- evidence:
  - `README.md`、`requirements.txt`、`prepare/download_dependencies.py` 已在位。
  - canonical registry 已补入。
  - `actionplan_deps.zip` 已解压完成，关键目录已在位：
    - `[[linkedCodebases/ActionPlan-Code/deps]]`
    - `[[linkedCodebases/ActionPlan-Code/datasets]]`
    - `[[linkedCodebases/ActionPlan-Code/models]]`
    - `[[linkedCodebases/ActionPlan-Code/outputs]]`
  - 关键权重已在位：
    - `[[linkedCodebases/ActionPlan-Code/outputs/actionplan/logs/checkpoints/latest-epoch=9999.ckpt]]`
    - `[[linkedCodebases/ActionPlan-Code/models/Causal_TAE/net_last.pth]]`
    - `[[linkedCodebases/ActionPlan-Code/deps/smplh/SMPLH_NEUTRAL.npz]]`
  - 2026-04-23 最小 inference smoke 已成功：
    - prompt: `a person walks forward`
    - settings: `seconds=2.0`, `steps_per_block=1`, `render=False`
    - artifacts:
      - `[[linkedCodebases/ActionPlan-Code/outputs/actionplan/generations/modebug_smoke/walk_forward_smoke_latents.npy]]`
      - `[[linkedCodebases/ActionPlan-Code/outputs/actionplan/generations/modebug_smoke/walk_forward_smoke_decoded272.npy]]`
      - `[[linkedCodebases/ActionPlan-Code/outputs/actionplan/generations/modebug_smoke/walk_forward_smoke_latent_meta.txt]]`
- residual risk:
  - 本轮只验证了 sample + decode，不含 mp4 render 链路。

### ReAlign-MLD

- status: `partial`
- canonical repo: `[[linkedCodebases/ReAlign]]`
- evidence:
  - `environment.yaml`、`requirements.txt` 已在位。
  - `mld/` host 子树已存在。
  - 训练与评测入口已在位：
    - `[[linkedCodebases/ReAlign/ReAlignModule/train_spm.py]]`
    - `[[linkedCodebases/ReAlign/ReAlignModule/eval_tmr.py]]`
  - 下载入口已确认：
    - official:
      - README OneDrive / BaiduNetDisk share
    - fallback:
      - MotionLCM `download_glove.sh` / `download_t2m_evaluators.sh` / `download_smpl_models.sh` / `download_pretrained_models.sh`
    - HF text encoders:
      - `sentence-transformers/sentence-t5-large`
      - `openai/clip-vit-large-patch14`
      - `distilbert/distilbert-base-uncased`
  - 2026-04-26 当前本地依赖已 materialize：
    - `[[linkedCodebases/ReAlign/deps/sentence-t5-large]]`
    - `[[linkedCodebases/ReAlign/deps/clip-vit-large-patch14]]`
    - `[[linkedCodebases/ReAlign/deps/distilbert-base-uncased]]`
    - `[[linkedCodebases/ReAlign/deps/glove]]`
    - `[[linkedCodebases/ReAlign/deps/t2m]]`
    - `[[linkedCodebases/ReAlign/deps/smpl]]`
    - `[[linkedCodebases/ReAlign/deps/smpl_models]]`
    - `[[linkedCodebases/ReAlign/datasets/humanml3d]]`
- missing:
  - `checkpoints/mld_humanml/mld_humanml_v1.ckpt`
  - default SPM checkpoint:
    - `SPM_H3D_Thr50.0_Temp1000_SAM1T0_E100.pth`
  - host + reward model 联合 smoke log
- note:
  - README 写 `deps/smpl`，但当前代码路径实际访问的是 `deps/smpl_models`。
  - 当前环境访问其官方 `OneDrive` share 会返回 `The request is blocked`，因此剩余 checkpoint 缺口不是来源未知，而是外部下载通道受阻。

### FineXtrol

- status: `paper-only`
- current finding:
  - 本地 repo 已在位：`[[linkedCodebases/FineXtrol]]`
  - 当前未发现本地权重。
  - README 明确写明 `Environment setup / Inference / Training / Evaluation` 均 `Coming Soon`。
- implication:
  - 缺口已从“repo 缺失”转为“官方 runnable code 与 weights 尚未公开”。
  - 自 2026-04-26 起不再把它当作 baseline readiness 的执行依赖，只保留为 paper-only related work。

### MotionFix

- status: `runnable`
- canonical repo: `[[linkedCodebases/motionfix]]`
- evidence:
  - requirements 与下载脚本已在位：
    - `[[linkedCodebases/motionfix/requirements.txt]]`
    - `[[linkedCodebases/motionfix/scripts/download_data.sh]]`
  - evaluator 与权重已在位：
    - `[[linkedCodebases/motionfix/eval-deps/tmr-evaluator/logs/checkpoints/last.ckpt]]`
    - `[[linkedCodebases/motionfix/eval-deps/tmr-evaluator/last_weights/motion_encoder.pt]]`
  - dataset 与 body models 已在位：
    - `[[linkedCodebases/motionfix/data/motionfix-dataset/motionfix.pth.tar]]`
    - `[[linkedCodebases/motionfix/data/body_models/smplh/SMPLH_NEUTRAL.npz]]`
  - sample outputs 已在位：
    - `[[linkedCodebases/motionfix/experiments/tmed]]`
- note:
  - 2026-04-24 当前真实 blocker 不在 MotionFix 本地资产，而在跨 repo bridge：`Event-T2M canonical_22j -> MotionFix pose(135)` 仍未闭合
  - 已确认 native `pose(135) -> 22j` forward probe 可跑，因此当前应把 `MotionFix` 继续记为 `runnable`，但不能误写成“主线接口已贯通”

### MotionReFit

- status: `partial`
- canonical repo: `[[linkedCodebases/motionReFit]]`
- evidence:
  - repo index 已修复：
    - executed:
      - `git reset HEAD`
      - `git checkout -- .`
    - current state:
      - `git status` 返回 clean working tree
  - `README.md`、`requirements.txt`、`data/norm_scaled.npy` 已在位。
  - `git-lfs` 文件已 materialize 到工作树：
    - `[[linkedCodebases/motionReFit/data/norm_scaled.npy]]`
    - `[[linkedCodebases/motionReFit/deps/Checkpoints/model_joints_to_smpl_wrist.pth]]`
  - 2026-04-26 从 Hugging Face model repo 自动补齐：
    - `[[linkedCodebases/motionReFit/models/regen/model_h3d_epoch3400.pth]]`
    - `[[linkedCodebases/motionReFit/models/style_transfer/model_h3d_epoch4403.pth]]`
    - `[[linkedCodebases/motionReFit/models/adjustment/model_h3d_epoch3300.pth]]`
    - `[[linkedCodebases/motionReFit/models/disc/regen/model_h3d_step68000.pth]]`
    - `[[linkedCodebases/motionReFit/models/disc/style_transfer/model_h3d_step55000.pth]]`
    - `[[linkedCodebases/motionReFit/models/disc/adjustment/model_h3d_step68000.pth]]`
    - `[[linkedCodebases/motionReFit/deps/smplx/models/smplx/SMPLX_MALE.npz]]`
- missing:
  - smoke 产物
  - STANCE dataset 本地根
- blocker:
  - 当前阻塞点已从“缺 demo weights / SMPL-X model assets”降为“缺 smoke 验证与 STANCE dataset”。

## 结论

- 当前可直接进入 runnable roster 的 baseline:
  - `Event-T2M`
  - `ActionPlan`
  - `MotionFix`
- 当前需要继续补资产的 baseline:
  - `ReAlign-MLD`
  - `MotionReFit`
- 当前 paper-only 参考仓库:
  - `FineXtrol`
