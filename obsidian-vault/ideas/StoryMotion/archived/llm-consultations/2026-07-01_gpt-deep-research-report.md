---
title: "StoryMotion GPT 深度研究报告清洗版"
status: cleaned
tags:
  - StoryMotion
  - Motion_Generation
  - architecture
  - status/cleaned
aliases:
  - StoryMotion-GPT-Cleaned
hypothesis: |
  GPT 报告中有价值的部分是“统一三模式不能再用对称 branch-mask 硬凑”，而不是替换 Stage1 或退化成单一 camera completion。清洗后的结论是：Stage1 继续固定 Pulp official checkpoint/cache 作为当前 latent contract；v7 只聚焦 Stage2，采用统一接口、非对称路由、source reliability、relation token 和可选 task-text CLIP latent 插件。
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions]]"
  - "[[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI]]"
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
created: 2026-07-01T23:08:48+0800
updated: 2026-07-01T23:08:48+0800
---
# StoryMotion GPT 深度研究报告清洗版

## 0. 清洗裁决

原 GPT 报告的主线是可用的：StoryMotion 应保留 unified three-mode framework，但内部不能继续把 human/camera 当成 CondMDI 式可交换缺失分支。真正需要修的是 Stage2 的任务路由、observed source 可信度、screen-framing relation 和 camera text 控制。

需要明确修正的一点：**不丢弃 Pulp official Stage1 checkpoint/cache**。当前本地 tokenizer 还不能训练到更好的 official metric contract，因此 v7 不把“重训或替换 Stage1 tokenizer”作为目标。Stage1 在 v7 中只作为固定 latent contract 和评估桥，不作为新增贡献。

清洗后的有效结论：

- 保留三模式统一目标：`JOINT`、`H2C camera completion`、`C2H human completion`。
- 三模式是异构任务，不是同一个 symmetric mask completion 的三个 mask pattern。
- `H2C` 是强条件方向，容易形成 GT-human shortcut；必须 source-aware。
- `C2H` 是弱约束方向，camera 更像 view/framing constraint，不能和 `H2C` 同权同结构。
- `JOINT` 没有 clean observed branch，不能靠 completion shortcut 学 relation。
- Stage2 先修 architecture 和 training protocol，不换 Stage1，不换大 backbone。
- MotionLab 的启发应降落为 task instruction / task latent / curriculum，而不是照搬其完整范式。

## 1. 保留的高价值意见

### 1.1 统一接口，非对称内部

最重要的判断是：

```text
unified task interface != symmetric internal denoising
```

StoryMotion 可以仍然对外宣称一个模型支持三种任务，但模型内部应承认三种任务的信息方向不同：

```text
JOINT:
  human text + camera text -> H_hat, C_hat

H2C:
  camera text + H_source -> C_hat

C2H:
  human text + C_source -> H_hat
```

其中 `H2C` 不是 `C2H` 的镜像。human motion 携带 action/root/timing，camera motion 更多提供 view、framing、shot intent 和 visibility constraint。

### 1.2 CondMDI-style 对称 mask 的问题诊断

GPT 报告对当前失败链的判断可以保留：

```text
三模式统一目标
  -> 对称 branch-mask 实现
  -> observed branch hard inject as clean x0
  -> camera 学会依赖 GT human/root shortcut
  -> camera text 与 relation control 变弱
  -> clean H_gt -> C 通过
  -> noisy/generated H -> C collapse
```

这与 v6.4 的现象一致：clean camera completion 能过，但 noise `0.15/0.30` 崩，camera text shuffle/zero 几乎不破坏 clean output。

### 1.3 Source reliability 是 Stage2 主矛盾

有效建议是：observed branch 不应再只用二值 `obs_mask` 表示。Stage2 需要显式知道 observed source 的类型与可信度：

```text
source_type:
  gt
  noisy_gt
  generated
  missing

source_quality:
  sigma
  root_drift
  mask_ratio
  source_confidence
```

但要修正 GPT 报告里过于乐观的一点：v6.4 的 P2b 结果已经说明“只加 source/noise augmentation”不够。v7 需要把 reliability 变成真正的 trust gate，而不是只作为额外 conditioning 向量。

### 1.4 Relation token 是必要桥接面

保留 GPT 对 Pulp Motion 的核心抽象：human-camera 的关键不是 raw latent concat，而是 screen-framing relation。v7 应加入 `R` token：

```text
R = screen relation / framing token
  e.g. projected bbox center, scale, visibility, relative camera-human layout
```

第一版可以用 Pulp `W` row-space 或 projected skeleton surrogate，不需要重训 Stage1。

### 1.5 Camera text 需要反 shortcut 机制

v6.4 中 camera text shuffle/zero 影响很小，说明 camera text 被 GT human shortcut 掩盖。GPT 报告建议做 camera text sensitivity gate 是有效的。v7 应把它变成硬 gate：

```text
如果 camera text shuffle/zero 对 CLaTr、FDCLaTr、SRE 几乎无影响，
则不能宣称 text-driven camera control 已经成立。
```

## 2. 修正或丢弃的内容

### 2.1 丢弃“替换 / 放弃 Pulp official Stage1”的路线

当前不做：

- 不丢弃 Pulp official Stage1 checkpoint/cache。
- 不把自训练 tokenizer 作为 v7 前置条件。
- 不用 Stage1 重训失败来否定 Stage2 方案。

正确表述：

```text
v7 assumes a fixed official-equivalent Stage1 latent contract.
Stage2 ablation uses Pulp official cache first.
Self-trained Stage1 can be a future independent milestone, not v7 dependency.
```

原因很直接：目前本地 tokenizer 还无法稳定超过或复现 official contract，强行换 tokenizer 会把 Stage2 架构诊断污染掉。

### 2.2 修正“三模式定义”

原 GPT 报告中有时把三模式写成 `human-only generation`、`camera-only completion`、`joint`。这不完全符合当前 StoryMotion 的统一目标。

v7 采用三种异构任务：

- `JOINT`: human text + camera text -> human + camera。
- `H2C`: camera text + human source -> camera。
- `C2H`: human text + camera source -> human。

`human-only` 可以作为 `JOINT` 的内部 first pass 或 human prior warmup，但不是替代 `C2H` 的外部三模式定义。

### 2.3 降级“camera-to-human 只是辅助任务”的说法

GPT 报告建议把 `C2H` 降为 auxiliary。这个判断需要改成更精确的版本：

```text
C2H 仍是三模式之一，
但它是弱约束 / actor blocking 任务，
不能被当成 H2C 的严格对称镜像。
```

也就是说，保留 `C2H` 的任务入口和 loss，但采用更低权重、更弱 condition gate、更强 human text prior，避免 camera branch 噪声反向污染 human。

### 2.4 降级“camera latent 重新拆维度”的说法

GPT 报告中给了 `d_s=512, d_h=256, d_cg=128, d_cr=128` 这类维度建议。它们不应作为 v7 设计要求。

v7 的现实做法：

```text
不改 Stage1 latent shape。
在 Stage2 head / adapter 层做 camera global/residual 的功能分解。
```

换句话说，`C_global` 和 `C_residual` 是 Stage2 内部预测路径，不要求改 tokenizer 或重建 cache。

### 2.5 丢弃无来源的具体阈值

GPT 报告中的一些阈值如 “noise `0.15` FDCLaTr 降 30%” 可以作为直觉目标，但不能直接写成理论结论。v7 gate 应优先继承已有内部基线：

- clean 不能显著差于 v6.4 clean `FDCLaTr 15.00 / F1 0.629`。
- noise 必须显著好于 v6.4 `FDCLaTr 530.27 / 493.82`。
- 第一阶段最好先回到或优于旧 P2a noise 量级，再追求强鲁棒。
- text shuffle/zero 不能继续近似无影响。

## 3. 清洗后的设计方向

### 3.1 v7 的一句话定位

```text
StoryMotion v7 is a unified three-task Stage2 policy with asymmetric routing,
source-aware trust gates, explicit relation tokens, and optional task-text CLIP latent.
```

### 3.2 v7 的边界

v7 做：

- 固定 Pulp official Stage1 cache / checkpoint。
- 重写 Stage2 任务组织与条件注入。
- 引入 `mode router`、`trust gate`、`R token`、分离的 human/camera heads。
- 保留三模式，但三模式不同权、不同 condition path。
- 加入 optional task-text CLIP latent 插件，默认关闭。

v7 不做：

- 不训练新 tokenizer。
- 不改 Pulp official evaluator。
- 不把 v6.4 camera specialist 当最终模型。
- 不把 `H2C` 与 `C2H` 当完全对称任务。
- 不靠扩大 backbone 掩盖 routing 问题。

### 3.3 对 v7 最关键的实验问题

v7 不是只问 clean camera completion 是否强，而是问四件事：

1. clean `H_gt -> C` 是否保持 v6.4 水平。
2. noisy/generated `H_source -> C` 是否不再 collapse。
3. camera text shuffle/zero 是否真的会影响 camera output。
4. `JOINT / H2C / C2H` 三任务是否能共存，而不是一个任务挤掉另外两个任务。

## 4. 连接到 v7 设计文档

清洗后的 v7 方案见 [[ideas/StoryMotion/2026-07-01_storymotion-v7-stage2-architecture]]。
