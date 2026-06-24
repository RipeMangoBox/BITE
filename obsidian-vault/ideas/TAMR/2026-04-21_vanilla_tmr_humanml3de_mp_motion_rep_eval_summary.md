---
created: 2026-04-21
updated: 2026-04-21
status: active
title: "Vanilla TMR HumanML3D-E-MP Motion Rep Eval Summary"
tags:
  - TAMR
  - motion_rep
  - motion_retrieval
  - status/active
---

# 2026-04-21 Vanilla TMR on HumanML3D-E-MP: 6-way Motion Rep Eval Summary

> [!abstract] TL;DR
> 在同一 `vanilla TMR + HumanML3D-E-MP` 设定下，`kimodo261` 明显最好；`pos66 / hml272 / hy201` 构成非常接近的第二梯队；`guo263` 只是内部 baseline，不是最优；`smpl135` 基本崩掉，当前不应继续作为候选 motion rep。

## 设定

- 模型族：`vanilla TMR`
- 数据：`HumanML3D-E-MP`
- 训练目录：`outputs/humanml3d_e_mp_motion_repr_server/tmr/{guo263,pos66,kimodo261,smpl135,hy201,hml272}`
- 统一评测协议：`normal`、`threshold_0.95`、`nsim`、`guo`
- 主排序分数：`PrimaryScore = mean(normal/nsim x {t2m,m2t} x {R@1,R@5})`
- 同集内部 baseline：`guo263`
- 跨数据集参考 only：原始 `HumanML3D` 预训练 `models/tmr_humanml3d_guoh3dfeats`
- 结构化产物：[[vanilla_tmr_humanml3de_mp_motion_rep_eval_summary.json|summary JSON]]

> [!warning] 口径提醒
> 这 6 个 `HumanML3D-E-MP` run 才是 fair same-dataset 对照。
> `models/tmr_humanml3d_guoh3dfeats` 只能做 cross-dataset reference，不能和这 6 个 run 直接下结论式横比。

## 主表


| Rank | Schema      | Motion rep        | PrimaryScore | vs `guo263` | `normal` R@1 (`t2m/m2t`) | `nsim` R@1 (`t2m/m2t`) | `guo` R@1 (`t2m/m2t`) | 判读                              |
| ---- | ----------- | ----------------- | ------------ | ----------- | ------------------------ | ---------------------- | --------------------- | ------------------------------- |
| 1    | `kimodo261` | `kimodo_like_261` | `40.58`      | `+4.09`     | `5.57 / 8.61`            | `50.52 / 51.55`        | `65.06 / 66.23`       | clear winner                    |
| 2    | `pos66`     | `pos66`           | `37.45`      | `+0.96`     | `4.61 / 7.32`            | `48.45 / 45.36`        | `64.44 / 65.37`       | 第二梯队上沿，且最接近 MP 原生表示             |
| 3    | `hml272`    | `hml272`          | `37.38`      | `+0.89`     | `4.43 / 7.28`            | `38.14 / 46.39`        | `63.56 / 64.25`       | second tier，偏均衡                 |
| 4    | `hy201`     | `hy201_recon`     | `37.35`      | `+0.86`     | `5.40 / 8.85`            | `46.39 / 43.30`        | `64.61 / 65.06`       | second tier，`normal m2t/R@1` 最强 |
| 5    | `guo263`    | `guo263`          | `36.49`      | `0`         | `4.67 / 7.81`            | `42.27 / 49.48`        | `62.63 / 63.25`       | 内部 baseline，不再是最优               |
| 6    | `smpl135`   | `smpl_d135_recon` | `3.86`       | `-32.63`    | `0.09 / 0.11`            | `4.12 / 4.12`          | `6.90 / 5.17`         | collapse，当前应排除                  |


## 关键观察

### 1. `kimodo261` 是唯一的明显领先者

- 它在 `PrimaryScore` 上比 `guo263` 高 `+4.09`
- 同时拿到：
  - `normal t2m/R@1` 第一
  - `nsim t2m/R@1` 第一
  - `nsim m2t/R@1` 第一
  - `guo t2m/R@1` 第一
- 因而如果后续还要继续扩 vanilla TMR 这条线，`kimodo261` 应该是首选 motion rep

### 2. `pos66 / hml272 / hy201` 是很紧的第二梯队

- 三者 `PrimaryScore` 只差 `0.10`
- `pos66` 的优势是：
  - `nsim t2m/R@1` 第二
  - 表示最简单，也最接近 MotionPatches 当前默认输入习惯
- `hy201` 的优势是：
  - `normal m2t/R@1` 全部 run 第一
- `hml272` 的特点是：
  - 没有单项特别突出，但整体较稳，没有明显短板

### 3. `guo263` 只能保留为内部 baseline

- 它在这 6 个 same-dataset run 里只优于 `smpl135`
- 因而后续若继续做 vanilla TMR / HumanML3D-E-MP 的 same-family 对照，不能再只报 `guo263`
- 最少应同时保留：
  - `kimodo261`
  - `pos66`
  - `guo263`

### 4. `smpl135` 不是“偏弱”，而是“异常”

- 本地补跑 eval 时，dataset loader 明确提示：
  - `tiny std detected -> disable scaling for 1 dims (motion_rep=smpl_d135_recon)`
- 最终结果也表现为全面 collapse：
  - `normal t2m/R@1 = 0.09`
  - `normal m2t/R@1 = 0.11`
- 当前更合理的解释是：
  - `smpl135` 的 representation / normalization 仍有问题
  - 它不应继续作为公平候选，除非先做数据统计与归一化审计
- 补充审计提醒：
  - 本地补跑 eval 使用的 `Mean.npy / Std.npy` 假定与服务器训练时一致
  - 当前未做 checksum 级交叉验证
  - 但鉴于它已表现为明显 collapse，这个未校验前提大概率不影响“先排除该 rep”的结论

## 对当前路线的影响

1. 这组结果完成了 **TMR 侧** 的 6-way motion rep sanity check。
2. 但它**不自动推翻** [[ideas/TAMR/ROADMAP|ROADMAP]] 里 `R1 用 pos66 + DistilBERT` 的决定。
3. 原因不是 `pos66` 在 vanilla TMR 下最优，而是：
  - `R1` 的目标是最小化变量，先验证 structured rerank
  - `pos66` 更贴近当前 MotionPatches 主线的 MP-native 表示
4. 因此更稳妥的表述是：
  - 若继续扩 **vanilla TMR** 线，首选 `kimodo261`
  - 若保持 **MotionPatches R1** 的最小变量设定，`pos66 + DistilBERT` 仍然合理

## 外部参考

- 原始 `HumanML3D` 预训练 TMR 的 cross-dataset reference `PrimaryScore = 39.76`
- 当前 `HumanML3D-E-MP` 里最好的 `kimodo261 = 40.58`
- 但这两者：
  - test gallery 大小不同
  - 数据分布不同
  - motion feature 来源也不同
- 所以只能说：
  - best E-MP vanilla TMR 已经进入与原始 TMR baseline 相近的量级
  - **不能**据此声称“超过原始 HumanML3D baseline”

## 文档同步

- 本 note 替代了以下已过时记录：
  - `2026-04-20_r1_verification_vanilla_tmr_humanml3de_mp.md`
  - `2026-04-20_tamr_landscape_integration.md`
  - `2026-04-20_vanilla_tmr_humanml3d_ceiling_stats.md`
- 活跃索引与结论同步见：
  - [[ideas/TAMR/README|README]]
  - [[EXPERIMENTS|EXPERIMENTS]]
  - [[ideas/TAMR/ROADMAP|ROADMAP]]
