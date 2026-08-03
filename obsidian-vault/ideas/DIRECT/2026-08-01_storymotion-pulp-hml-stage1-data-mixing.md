---
title: "StoryMotion Pulp–HumanML3D Stage1 数据混合合同"
status: historical_closed_specification
hypothesis: |
  HumanML3D can expand Human support only through explicit missing-modality
  supervision and matched Pulp replay; it cannot be treated as a synthetic
  Human–Camera pair source by filling absent Camera or pose channels.
tags:
  - StoryMotion
  - DIRECT
  - paper/B
  - stage1
  - data_mixing
  - HumanML3D
  - status/historical_closed
aliases:
  - StoryMotion-Pulp-HML-Mixing
source_notes:
  - "[[2026-07-27_storymotion-stage1-human-anchor-residual-control]]"
  - "[[archived/superseded-design/2026-07-22_storymotion-humanml3d-fixed-camera-augmentation-plan]]"
  - "[[DIRECT/2026-08-01_storymotion-multipair-data-training-plan]]"
  - "[[StoryMotion/version_family]]"
created: 2026-08-01T14:04:35+08:00
updated: 2026-08-03T14:30:39+08:00
---

# StoryMotion Pulp–HumanML3D Stage1 数据混合合同

> [!abstract] 一句话结论
> 历史 Pulp+HML 实验不是把 HML Human 与 Pulp Camera 配成联合 positive，而是在同一个 fresh redesigned non-causal Stage1 中按固定周期交替送入两类 batch：HML batch 只有 Human root/local supervision，Pulp batch 才有完整 Human199、Camera14 与 framing supervision。该配方产生跨域 trade-off，且 HML 缺失 rot6D 曾被均值填充为伪观测，因此只保留诊断身份；v11 继续使用 exact v9 Pulp-only Stage1，v10 后续不再执行。

## 1. “混入”实际指什么

历史 mixed arm 与 Pulp-only control 都从 seed17 fresh 训练相同的 `human128 + interaction16 + camera48` Stage1。它们不是 dataset concatenation 后随机采样，也没有构造 HML–Camera pair；数据源由 optimizer step 所在 phase 的固定 cycle 决定。

| phase | optimizer steps | mixed arm source cycle | mixed arm 实际更新 | matched Pulp-only control |
| --- | ---: | --- | --- | --- |
| A：Human anchor | `210K` | `HML,HML,HML,HML,Pulp` | 所有 batch 都只更新 Human encoder/decoder；Camera 模块冻结 | 用 Pulp Human-only batch 替换 HML，保持相同 role exposure |
| B：Camera | `210K` | `Pulp` | Human 模块冻结；更新 interaction、Camera 与 framing 模块 | 完全相同 |
| C：joint replay | `216K` | `HML×3 + Pulp×7` | HML step 仍为 Human-only；Pulp step 才有 joint objective；Human LR 为主 LR 的 `0.1×` | 用 matched Pulp replay 替换 HML |

总预算为 `636K` optimizer steps，batch size `128`。packed-I/O 版本只改变数据运输；`r3` 把 TensorBoard cadence 从 `10` 改为 `11`，避免日志周期与长度 `5/10` 的 source cycle 混叠，不改变训练样本或损失。

source cycle与phase freeze来自`experiments/stage1_human_anchor_residual/train.py`；Human-only／joint forward、supervision profile与decoder ownership来自同目录的`model.py`。packed transport与日志修订分别由`stage1_human_anchor_residual_packedio/`和`stage1_human_anchor_residual_packedio_r3/`持有。

## 2. HML 预处理

1. 从 HumanML3D canonical RIC263、`20 fps` 恢复 world joints，再转换为 StoryMotion/Pulp Human199。
2. 插值 world joints 与 pose6D 到 `30 fps`；重采样后重新计算 root planar velocity 与 yaw delta，禁止重复帧。
3. 长序列按最多 `300` 帧、stride `240` 做确定性滑窗，并强制加入 tail-aligned window；不是只取首窗。
4. 每个 crop 把起始 root `xy` 平移到零、把首帧 yaw delta 改为源窗口 absolute yaw，并清除末帧未使用的 planar velocity。
5. derived cache 保存 raw Human199；训练时只使用 Pulp train statistics 做归一化，不拟合 HML statistics。【怀疑合理性】

实现入口为 `experiments/stage1_human_anchor_residual/prepare_humanml3d.py` 与 `data.py`。parent manifest、source split、window、转换与文件 hash 均保留，坏样本进入带 reason code 的 quarantine，不删除源 motion。

## 3. 通道与梯度边界

| source | 输入通道 | 有监督 Human 通道 | 缺失模态 | Camera／interaction 梯度 |
| --- | --- | --- | --- | --- |
| Pulp | 完整 Human199 + Camera14 | `0:199` 全部 | 无 | 有，仅 Phase B/C |
| HML | converted Human199 | root/yaw `0:4` + 21 个 root-relative joints `136:199`，合计 `67D` | Camera、framing、同源 TRAM/SMPL rot6D | 无；模型以 `camera=None` 走 Human-only path |

HML 经 joints+IK 得到的 rotation 不等于 Pulp TRAM/SMPL 的同源 rot6D。历史 loader 把归一化后的 `4:136` 写成零，即 Pulp mean，并在 HML loss 中排除；这虽阻止极端数值进入 loss，却没有 availability mask，仍把“未知”伪装成可见的平均姿态。该做法现已禁止。

历史 objective 为：Human `SmoothL1 + first difference + 0.001 integrated yaw + 0.003 integrated root`；Camera `SmoothL1 + first difference`；framing 权重 `0.1`；interaction residual energy 权重 `1e-4`。HML 从未获得 Camera、framing 或 interaction target。

## 4. 为什么没有晋升

正式 paired reconstruction closure 由 [[2026-07-27_storymotion-stage1-human-anchor-residual-control]] 唯一持有：mixed arm 改善 converted HML validation 的 root/local reconstruction，但 Pulp-only arm 在 Pulp pure test 的 Human root、heading、global geometry 与 Human–Camera projective geometry 上更好。结果是 domain trade-off，不是 Pareto improvement；mixed checkpoint 禁止 Stage2 cache、Stage2 training 与 promotion。

这不证明“HML 数据无效”，只否定了当时的 partial-supervision policy、replay ratio、architecture 与 schedule 组合。它也不属于 Rect augmentation：没有同一 Human 的多个 Camera program，更没有跨 Human 重新求解的 Camera target。

## 5. 未来若重新使用 HML

- motionstreamer272 虽然只包含 HML 的子集，但不强求完整性。直接将它作为 HML 来源进行适配，可解决 rot6d 的 IK 精度不足相关问题。【更新】
- 缺失通道必须有 availability mask 或独立 root/local encoder；禁止 mean Camera、static Camera、零 Camera 或 mean rot6D 充当观测。
- HML batch 只更新 Human/provider；Pulp factual 与合格 Rect batch 更新 Director，并持续 replay Pulp Human。
- data-mixing、Stage1 observation、Stage2 text injection 必须分 run／contract，不能在一个训练中同时改变。
- matched control 保持相同 optimizer steps、source-role exposure、batch、seed、sampler、train-only statistics 与评价 IDs；结果表每行写明 `version / run`。

## 6. 缩写

| 缩写 | 全称与语义 |
| --- | --- |
| HML | HumanML3D；这里只是 Human-only motion/text source |
| H199 | Pulp Human199：root/yaw `4D` + rot6D `132D` + root-relative joints `63D` |
| RL67 | HML 实际受监督的 root/local `67D`，不是完整 Human199 |
| C14 | Pulp Camera14 motion representation |
| S1／S2 | Stage1 representation autoencoder／Stage2 conditional generator |
| Pulp-full | Pulp batch同时提供完整 Human、Camera 与 framing supervision |
