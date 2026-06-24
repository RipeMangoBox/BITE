---
title: "DS 审查 SOMA Unified 30k"
created: 2026-05-16T23:48:36
updated: 2026-05-17T18:55:50+08:00
type: ds_review
---

# DS 审查 SOMA Unified 30k

## 目标

审查 30k 数据构造单位、split 策略、HumanML3D 对齐要求和训练前置 gate。

## 数据对象

- 30k unit: `caption-motion pair`，不是 event-level pair。
- primary pool: original SEED/KIMODO motions，mirror rows 排除。
- text: 保留 full natural-language caption。
- split: 80/10/10，按 source identity 去重。

## 计算方式

DS 审查先确认 30k 的单位是 caption-motion pair，再检查 split 泄漏策略、HumanML3D 表征兼容性、raw BVH 到训练特征的转换门槛，以及 remote4090 资产可见性。

## 审查结论

当前 manifest 可作为 metadata selection 结果，但不能直接启动真正训练。MoMask/MoGenTS 需要 HumanML3D-style feature arrays 和 text files，不是 raw BVH path。

## 训练前硬门槛

1. SOMA BVH 转换为 HumanML3D-compatible 263-dim `new_joint_vecs/*.npy` 和 `texts/*.txt`。
2. 转换记录 fps、skeleton mapping、coordinate normalization、mean/std provenance。
3. loader smoke 验证 selected samples 能在 MoMask/MoGenTS 中加载，数值 finite、shape 正确。
4. 小训练 smoke 无 NaN/loss explosion。

## 4090 状态

早期 remote probe 在 2026-05-16 发现 `/data/public/ripemangobox/Motion/mogents` 和 KIMODO code，但当时未确认 SOMA 解包数据和 MoMask repo 可见性。随后用户确认 4090 上已有 `/data/public/ripemangobox/Motion/datasets/soma_uniform`，并已按本地 manifest/split 构造 raw BVH + full text 数据集：`30000/30000` motion symlinks、`30000/30000` text files、missing motion 为 `0`。

随后在 2026-05-17 跑通 6 条 KIMODO/HumanML3D 转换 smoke：SOMA BVH 经 KIMODO 官方 `convert_motion_files` 转成 Kimodo NPZ，再由 `posed_joints [T,77,3]` 基于拓扑/名称映射到 HumanML3D 22 关节，并通过 MoMask/MoGenTS 同源 `process_file` 生成 263D `new_joint_vecs`。6/6 转换成功，loader smoke 为 pass，并已拉回 recover 静态可视化。

同日追加 20fps gate：KIMODO NPZ 默认转为 30Hz，但 HumanML3D/MoMask/MoGenTS loader 使用 20fps 时间单位。新增 `--target-fps 20` 后，6 条 smoke 与 12 条 regression 均通过；recover 后 Y 最小值为 0，最终帧数回到 manifest 的 20fps 长度范围。基于该 gate，4090 已启动 full 30k 20fps HumanML3D-263 转换，tmux session 为 `soma30k_hml3d_full20fps_0517`。

训练仍未启动。当前 blocker 已从“远程缺少 SOMA 原始动作/完全没有转换路径”收敛为：

- full 30k 20fps HumanML3D-263 转换正在运行，尚未完成。
- SOMA77->HumanML3D22 mapping 仍需更多可视化抽检和人工确认，当前 smoke 不是全量训练资格。
- 全量 skeleton/fps/coordinate normalization/mean/std provenance 需等 full conversion 完成后记录。
- MoMask repo 在 4090 上仍未确认可见。
- MoMask/MoGenTS 全量 loader smoke 和小训练 smoke 尚未完成。

## 元数据

- date: `2026-05-17`
- experiment_path: `paperIDEAs/MoDebug/experiments/soma_unified_30k_20260516`
- evaluator: `DS Max data-construction review`
- protocol: `SOMA/KIMODO 30k selection and MoMask/MoGenTS training gate review`
- data_source: local manifest/profile and remote4090 probes
- condition_pair: `not_applicable`
- n/evaluable: `30000/30000 manifest rows; 0/2 training jobs started`
- coverage: data construction plan and training preflight
- role: `diagnostic`
- used_for: `selection`
- limitations: 审查不是模型训练结果。
