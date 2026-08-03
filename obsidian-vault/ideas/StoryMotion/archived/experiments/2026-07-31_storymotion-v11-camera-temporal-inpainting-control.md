---
title: "StoryMotion v11 Camera Temporal Inpainting Control"
hypothesis: |
  A fixed-H v11 Camera flow can expose a practical camera-only temporal
  inpainting interface while preserving Human exactly and retaining the
  unedited Camera context. A training-free clamp probe first tests whether the
  non-causal Stage1 decoder permits localized edits; mask-aware training is
  authorized only if that representation gate passes.
status: stopped_representation_gate
archived: 2026-08-03
tags:
  - StoryMotion
  - version/v11
  - control/camera_inpainting
  - status/active
source_papers:
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
  - "[[analysis/CVPR_2026/ProjFlow_Projection_Sampling_with_Flow_Matching_for_Zero_Shot_Exact_Spatial_Motion_Control]]"
  - "[[analysis/ICCV_2025/MaskControl_Spatio_Temporal_Control_for_Masked_Motion_Synthesis]]"
  - "[[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI]]"
created: 2026-07-31T23:50:00+08:00
updated: 2026-08-01T03:05:00+08:00
---

# StoryMotion v11 Camera Temporal Inpainting Control

> [!important] Causal question
> 在 exact v11 C0-GEO／C0-LAT Camera endpoint、固定 GT Human、固定 Camera
> caption 下，给定 Camera 序列 mask 外的原始上下文，仅重生成一个内部连续时段，
> 能否同时满足 mask 内补全质量、mask 外保真与边界连续性？

本页是 Camera temporal inpainting 这一独立 control 轴的唯一计划与 screen
裁决所有者。训练过程、step、ETA 与 checkpoint 只写 `runs/` 下的 contract、manifest
和日志；正式通过审计的数字才进入 [[StoryMotion-valid-metric-ledger]]。

相关方法边界见
[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm|MotionLab]]、
[[analysis/CVPR_2026/ProjFlow_Projection_Sampling_with_Flow_Matching_for_Zero_Shot_Exact_Spatial_Motion_Control|ProjFlow]]、
[[analysis/ICCV_2025/MaskControl_Spatio_Temporal_Control_for_Masked_Motion_Synthesis|MaskControl]] 与
[[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI|CondMDI]]。

## 1. 固定边界

- Stage1、owning decoder、cache、train-only statistics 与 sample identity 均继承
  v11 C0 co-mainline 的 exact v9 owner，不改 representation。
- Human teacher 与输入 Human 全部冻结；Human 输出逐元素不变。
- temporal tokenizer 仍为 `is_causal=false`；本实验不是 causality ablation。
- 只测试 Direct-C 条件下的 Camera temporal completion；不训练、不评估
  joint-parallel，也不把它包装为 joint edit。
- 首轮 caption 不变，任务是 held-out interval reconstruction。替换 caption 的
  semantic edit 没有 paired ground truth，只有本任务闭合后才可另立 screen。

## 2. 最小 probe

在 ordered first-64 上对中心 `25%` 与 `50%` 两种 latent gap 使用相同初始噪声，
比较三个候选：

1. 原 C0 Camera full generation；
2. Camera64 线性补间；
3. training-free shifted-flow clamp，每个 ODE step 将 mask 外写回同一
   clean-to-noise path，终点精确写回已知 Camera64。

报告 masked Camera-center ADE、masked rotation geodesic error、边界速度误差、
mask 外 decoded drift，以及排除两侧两个 latent token guard band 后的 far-context
drift。所有 reference 都是同一 Human 与原 Camera latent 经 exact owning decoder
得到的重建，避免把 Stage1 reconstruction floor 混入 control 误差。

## 3. Continue／stop gate

| gate | continue | stop／转向 |
| --- | --- | --- |
| Contract | checkpoint、decoder、cache、stats、ordered IDs、seed、sampler 与代码 hash 全部可审计 | 任一 identity 不闭合即停止 |
| Exact preservation | mask 外 Camera64 max-abs 为 `0.0`；Human 未进入可训练图 | 任一非零即停止 |
| Decoder locality | far-context center 与 rotation drift 各不超过对应 masked change 的 `10%`，或处于数值 floor | 任一明显越界则停止 latent inpainting，转向 decoded Camera14 约束 |
| Inpainting signal | flow-clamp 相对 full generation 在 masked center／rotation 至少形成非劣 Pareto；相对线性补间无灾难性边界抖动 | 两种 gap 均被线性补间全面支配且视觉失真时不长训 |
| Stability | 无 non-finite；两种 gap 均完成；固定样本可解码 | 任一结构性失败即停止 |

## 4. 有条件长训

### 4.1 Camera center 非局部时的 endpoint-closure oracle

若 training-free probe 仅因 Camera center far-context leakage 失败，而 Camera64
保真与 rotation locality 通过，则先在 ordered first-8 上优化 mask 内 Camera64
delta，模型参数全部冻结。目标只读取 mask 外 decoded Camera center／rotation 与原
上下文的一致性，并用小权重锚定原 flow-clamp proposal；不读取 mask 内 GT，因此
不是用答案反推答案。

`25%` 与 `50%` gap 都必须满足：mask 外 Camera64 max-abs `0.0`；guard-band 后
center／rotation drift 各不超过 mask 内变化的 `10%`；mask 内 center／rotation 相对
优化前不得恶化超过 `2×`。两种 gap 同时通过才授权 amortized mask-aware Camera
训练；失败则认定当前 Camera14 累积中心表示不适合 endpoint-locked latent edit，
本轴停止。

### 4.2 训练边界

若 probe 通过，则从 co-mainline Camera EMA 显式转移权重，新增 mask-aware Camera
condition，仅训练 Camera 分支；Stage1、Human 与 decoder 永久冻结。训练 batch 同时
包含标准 Direct-C replay 与随机内部连续 mask，防止新增 control 以损害原生成能力为
代价。长训前先用短 screen 验证：

- 无 mask 路径与父 endpoint forward exact；
- mask-aware 路径能够读取已知 Camera 与 mask；
- Direct-H max-abs `0.0`；
- held-out masked geometry 改善且 Direct-C replay 不发生明显回退。

只有上述 screen 通过才部署完整预算；否则保留 training-free 工具或停止该路线，
不以 seed 补强冒充新能力。

## 5. Screen 裁决

> [!failure] 结论：停止 latent temporal inpainting 长训
> ordered first-64 training-free probe 中，两个 gap 的 mask 外 Camera64 均逐元素
> `0.0` 保留，far-context rotation／masked rotation 比值仅为 `0.0020` 与
> `0.0010`；但 Camera center 比值为 `0.8466` 与 `1.0540`，未通过 `0.10`
> locality gate。Camera14 translation velocity 从第二帧起反归一化并累积，因此
> 局部 Camera64 改动会传播到后续 world Camera center。

随后执行的 ordered first-8 endpoint-closure latent optimizer oracle 把两个 gap 的
far-context Camera-center ADE 从 `0.0988 / 0.4488` 降到 `0.0149 / 0.0345`，同时
masked Camera-center ADE 也下降；但 far／masked 比值仍为 `0.2835 / 0.3164`，未
通过预注册 `0.10` gate。rotation 与已知 latent 继续通过，无法修复 center 的表示
边界。因而不部署 mask-aware latent 长训，不事后放宽 threshold。

以上均为 `screen`／oracle，不进入正式 metric ledger。下一增强轴转向与现有
framing4 语义一致的显式 screen-space composition control。
