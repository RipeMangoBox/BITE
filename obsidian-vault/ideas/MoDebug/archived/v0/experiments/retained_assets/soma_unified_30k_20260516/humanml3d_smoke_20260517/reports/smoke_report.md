---
title: "SOMA/KIMODO 到 HumanML3D 转换 Smoke 报告"
created: 2026-05-17T17:45:51+08:00
updated: 2026-05-17T17:45:51+08:00
type: conversion_smoke_report
tags:
  - MoDebug
  - SOMA
  - KIMODO
  - HumanML3D
---

# SOMA/KIMODO 到 HumanML3D 转换 Smoke 报告

## 目标

验证官方 KIMODO SOMA BVH 到 Kimodo NPZ 转换能否接上 MoMask/MoGenTS 使用的 HumanML3D 263D 表征，并用 recover/可视化/loader smoke 闭环检查。

## 数据对象

- 输入 manifest：`/data/public/ripemangobox/Motion/datasets/soma_unified_30k_20260516/input/manifests/selected_30k_manifest.tsv`
- smoke rows：`6`
- 成功转换：`6`
- 输出 dataset：`/data/public/ripemangobox/Motion/datasets/soma_unified_30k_20260516/humanml3d_smoke_20260517/hml3d_dataset`

## 计算方式

1. 使用 KIMODO 官方 `convert_motion_files` 执行 SOMA BVH -> Kimodo NPZ。
2. 从 Kimodo NPZ 的 `posed_joints [T,77,3]` 按名称映射到 HumanML3D 22 关节。
3. 使用 MoMask/MoGenTS 同源 `process_file` 生成 `new_joint_vecs/*.npy` 263D 特征。
4. 使用 `recover_from_ric` 还原 22 关节，生成静态可视化面板。
5. 检查 motion/text/Mean/Std 是否可被 HumanML3D-style loader 消费。

## 结论

- n/evaluable：`6/6 converted rows; loader_smoke=pass`
- loader smoke：`pass`
- 这是 small smoke，不是全量 30k 转换完成声明。

## 限制

- role: `diagnostic`
- used_for: `conversion_smoke`
- limitations: SOMA77 到 HumanML3D22 是基于拓扑/名称的 smoke 映射，仍需人工检查可视化和更多样本后才能作为全量训练转换。
