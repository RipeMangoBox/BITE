---
title: Trace 3 — Data Efficiency
created: 2026-06-02
updated: 2026-06-14T00:00:00+08:00
status: archived
---

# Trace 3: Data Efficiency

对应 Line 3，旧称 Track A。完整设计见 [[archived/v2/2026-06-02_modebug_reboot_plan#5 Trace 3 — 数据效率训练侧]]。

## Status

- MotionCLR code/data/evaluator symlink 和 release checkpoint 已配置。
- GPU0 `20260602_gpu0_track_a_minimal_real_ablation/` 已降级为 engineering path-validation；OOM/停止/不完整 checkpoint 不可引用。
- 2026-06-03 DS 已批准 formal candidate；`modebug_trace3_train_formal_20260603` 正在 GPU0 串行运行 baseline、aug、disploss、aug_disploss real training。
- 当前 50k step 来自 MotionCLR 官方 `TrainOptions --num_train_steps` 默认值，并在本次命令中显式设置；训练完成前不产生收益结论。

## Claim Boundary

- 不 claim motion-domain data augmentation 为空白或新颖。
- 只讨论具体 backbone、split、evaluator 和 augmentation policy 下的受控结果。
- DispLoss 仍需真实 ablation 后才能形成任何 claim。

## Valid Entry Criteria

- 使用真实 MotionCLR 或另一个声明 backbone。
- 使用真实 HumanML3D train/eval split。
- 训练循环能精确停在指定 step。
- 新增 flag 关闭时 baseline 路径不变。
- 所有正式代码和命令先经 DS 复核。

## Next

- [x] 提交 formal training 脚本、四 variant 命令和 official evaluator 命令给 DS。
- [x] 运行 `dev_validation_only` 入口检查：baseline、aug、disploss、aug_disploss 均真实更新 1 step 并精确停止。
- [ ] 等待 `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/formal_candidates/trace3_formal_train_ds_review_20260603_gpu0/` 四个训练 checkpoint 完成。
- [ ] 训练完成后运行 official evaluator；未完成前不得产生 paper-level metric claim。
