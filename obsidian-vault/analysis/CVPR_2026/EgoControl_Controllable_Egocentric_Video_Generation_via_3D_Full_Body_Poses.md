---
title: "EgoControl: Controllable Egocentric Video Generation via 3D Full-Body Poses"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EgoControl_Controllable_Egocentric_Video_Generation_via_3D_Full_Body_Poses.pdf
project_link: "https://cvg-bonn.github.io/EgoControl"
code_link: null
aliases:
- EgoControl
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用差分头部运动、骨盆相对运动和关节相对骨盆的组合姿态表示，并通过AdaLN调制与交叉注意力双路径将其注入扩散过程。
primary_logic: 将3D全身运动分解为相对变化，结合全局调制与帧级注意力，是实现身体姿态与生成视频精确对齐的关键。
claims:
- 与仅使用头部姿态控制相比，全身姿态控制的mIoU提升约55%，手臂可见性一致性超过96%。
- 差分姿态表示相比累积表示大幅降低了平移误差（12.31 → 6.75）。
- 骨盆相对关节表示相比每帧相对运动提升了mIoU（31.85 → 37.40）。
- Nymeria (2 seconds ahead) 上 LPIPS (×100) ↓ = 24.3
---

# EgoControl: Controllable Egocentric Video Generation via 3D Full-Body Poses

> [!tip] 核心洞察
> 将3D全身运动分解为相对变化，结合全局调制与帧级注意力，是实现身体姿态与生成视频精确对齐的关键。

| 字段 | 内容 |
|------|------|
| 中文题名 | EgoControl：基于3D全身姿态的可控第一人称视频生成 |
| 英文题名 | EgoControl: Controllable Egocentric Video Generation via 3D Full-Body Poses |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.18173) · [Project](https://cvg-bonn.github.io/EgoControl) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | EgoControl |
| Dataset | Nymeria |

> [!tip] 效果简介
> - Nymeria (2 seconds ahead) 上，LPIPS (×100) ↓ 24.3 vs 29.8 (PEVA XXL) (-5.5)；DreamSim (×100) ↓ 11.3 vs 18.6 (PEVA XXL) (-7.3)。
> - Nymeria 上，TransError (cm) ↓ 6.75 vs 12.31 (Cumulative repr.) (-5.56)；mIoU ↑ 37.40 vs 31.85 (Δj repr.) (+5.55)。

## 概述

### 问题与瓶颈

第一人称（egocentric）视频生成在具身智能、增强现实等领域有重要应用，但现有方法普遍缺少对相机佩戴者**3D全身姿态的精细控制**。具体而言，仅依赖头部姿态或过去帧的视频预测模型无法同时建模**全局相机运动**与**局部肢体交互**，导致生成的手臂位置、手部动作与真实身体运动严重失配。**EgoControl** 正是针对这一瓶颈提出：如何在给定少量历史观测帧的条件下，让生成的未来帧严格遵循指定的3D全身姿态序列。

### 核心思路

EgoControl 的核心洞察在于：将3D全身运动分解为**相对变化**，并通过**全局调制与帧级注意力**两条互补路径注入扩散模型，是实现身体姿态与生成视频精确对齐的关键。为此，方法设计了三个紧密耦合的机制：

1. **差分姿态表示**：将头部运动表达为相邻帧间的相对变换（$\Delta \mathbf{h}$），骨盆运动同理（$\Delta \mathbf{r}$），而关节位置则表达为相对于当前帧骨盆的坐标（$\mathbf{J}$）。这一表示天然适配第一人称视角下相机与肢体的运动特性。
2. **双路径控制注入**：扁平化的姿态嵌入通过 **AdaLN 调制**（紫色分支）为 DiT 去噪网络的每个 Transformer 块预测偏移、缩放与门控参数，提供全局级姿态条件；同时，保留时间结构的帧级姿态令牌通过**交叉注意力**（蓝色分支）注入局部、时序敏感的控制信号。
3. **端到端扩散训练**：在潜空间中对未来帧进行连续噪声扰动与去噪预测，训练目标为直接预测干净潜变量的加权均方误差。

### 方法定位

EgoControl 属于**可控视频扩散模型**在**第一人称视角**下的延伸。与仅使用过去帧的微调基线（如 Cosmos finetuning）和仅控制头部姿态的消融变体相比，EgoControl 首次将完整的3D全身姿态作为显式条件引入视频扩散过程。与并发工作 **PEVA**（仅使用3D上半身姿态生成单帧）相比，EgoControl 同时建模全身运动并生成连续视频序列，在控制粒度和时序一致性上均有本质提升。

### 主要结果

在 Nymeria 数据集上，EgoControl 在多项指标上显著超越基线：

- **与 PEVA XXL 对比**：在 2 秒后的未来帧生成中，LPIPS 从 29.8 降至 **24.3**（↓5.5），DreamSim 从 18.6 降至 **11.3**（↓7.3），视觉质量与结构相似度均有大幅提升（Table 2）。
- **姿态控制精度**：与仅使用头部姿态控制相比，全身姿态控制使手臂分割的 mIoU 提升约 **55%**，手臂可见性一致性超过 **96%**（Table 1）。
- **表示消融**：差分头部表示相比累积绝对表示，平移误差从 12.31 cm 降至 **6.75 cm**（↓5.56）；骨盆相对关节表示相比每帧相对运动，mIoU 从 31.85 提升至 **37.40**（↑5.55）（Table 4）。
- **控制机制消融**：AdaLN 与交叉注意力联合使用，在视觉质量和运动精度上均优于单独任一路径（Table 3）。

定性结果（Figure 5、Figure 8、Figure 9）进一步表明，EgoControl 能够在相同初始上下文中跟随不同的身体运动，或在相同姿态序列下适应不同的场景上下文，展现出良好的**解耦控制能力**。

### 局限与开放问题

当前方法仅在 Nymeria 数据集上训练和评估，对其他第一人称场景的泛化能力尚未验证；生成视频长度受限于训练片段（32 帧），自回归扩展可能引入误差累积；对手部姿态和精细物体交互的控制仍需提升。开放问题包括：如何引入显式手部姿态标注以实现精细手指关节控制，以及如何提升对日常视角、衣着和传感器配置的分布外泛化能力。

## 背景与动机

第一人称（egocentric）视频生成在增强现实、具身智能和沉浸式内容创作中具有重要价值。其核心挑战在于：生成过程不仅需要保持场景的视觉真实性和时间一致性，还必须精确地反映相机佩戴者的运动意图。相机佩戴者的行为——包括头部的全局移动和肢体的局部动作——共同决定了第一人称视角下的视觉内容。然而，现有方法在这一问题上存在显著的能力缺口。

**现有方法的局限。** 当前的第一人称视频生成模型主要依赖过去帧的视觉上下文进行未来帧预测，缺乏对相机佩戴者身体姿态的显式控制。例如，直接微调预训练视频生成模型（如 Cosmos）虽然能够生成视觉质量尚可的帧，但无法保证生成内容与佩戴者的实际身体运动对齐。部分方法尝试仅使用头部姿态进行控制，但这忽略了肢体的局部运动——尤其是手臂与场景物体的交互——导致生成的肢体位置与目标姿态严重偏离。定量证据显示，仅使用头部控制的方案在手臂分割 mIoU 指标上比全身控制低约 55%，手臂可见性一致性不足 96%。并发工作 PEVA 虽然引入了 3D 上半身姿态，但仅支持单帧生成，且分辨率受限（224×224），无法满足连续视频生成的需求。

**核心瓶颈。** 第一人称视频生成的根本瓶颈在于：缺少一种能够同时编码全局相机运动和局部肢体动力学的姿态表示，以及将其有效注入扩散生成过程的控制机制。全局运动（头部姿态）决定相机视角的变化，局部运动（关节姿态）决定肢体在画面中的位置和形态，二者必须被联合建模并精确地作用于每一帧的生成。若姿态表示设计不当（如使用累积绝对变换而非帧间差分），会导致平移误差显著增大（从 6.75 cm 升至 12.31 cm）；若控制注入路径不完善（如仅使用单一调制而缺少帧级交叉注意力），则无法实现精细的时空对齐。

**本文动机。** 针对上述缺口，EgoControl 旨在构建一个可控的第一人称视频生成框架，其核心思路是：设计一种紧凑且信息充分的 3D 全身姿态表示，将全局与局部运动解耦为差分头部变换、骨盆相对运动和关节相对骨盆位置三个分量；同时，通过 AdaLN 全局调制和交叉注意力帧级注入的双路径控制机制，将姿态信息深度嵌入扩散去噪过程。这一设计使得模型能够根据相同的过去视觉上下文，生成跟随不同身体运动序列的视频，从而实现真正可控的第一人称视频合成。

## 核心创新

EgoControl 的核心创新在于首次将 **3D 全身姿态** 作为显式控制信号引入第一人称视频扩散模型，解决了现有方法仅依赖头部姿态或无条件生成时无法精细控制相机佩戴者肢体交互的瓶颈。这一创新通过三个关键设计实现：

### 1. 差分-骨盆相对姿态表示

传统姿态控制通常直接使用关节的绝对坐标或累积变换，但这在第一人称场景下会导致全局相机运动与局部肢体运动的耦合混乱。EgoControl 将姿态表示分解为三个互补分量（Eq. 4）：

- **帧间差分头部运动** (Δh)：编码相邻帧间头部姿态的 **相对变换**，使模型学习相机运动的动态变化而非绝对位置。消融实验证实，差分表示相比累积表示将平移误差从 12.31 cm 降至 6.75 cm（Table 4），说明相对运动建模对相机轨迹控制至关重要。
- **骨盆相对运动** (Δr)：捕获身体相对于骨盆的全局位移。
- **关节相对骨盆位置** (J)：将 23 个关节表示为 **当前帧相对于骨盆的坐标**，而非每帧相对于上一帧的差分运动 (Δj)。消融显示，骨盆中心表示将 mIoU 从 31.85 提升至 37.40（Table 4），表明以骨盆为锚点的关节表示更有利于模型学习稳定的肢体-场景空间关系。

这种分解的核心洞察在于：**将 3D 全身运动解耦为相对变化，使模型能够分别学习相机运动动力学和身体姿态几何，从而实现精确对齐**。

### 2. 双路径姿态控制注入

EgoControl 设计了 **AdaLN 调制** 与 **交叉注意力** 两条互补路径将姿态表示注入扩散去噪过程（Figure 2）：

- **AdaLN 调制路径**（紫色分支）：将扁平化的完整姿态序列通过 MLP 编码为全局嵌入，预测每个 Transformer 块的偏移 (β)、缩放 (γ) 和门控 (g) 参数，对自注意力、交叉注意力和 MLP 层进行条件调制（Eq. 6-7）。这提供了 **全局、粗粒度的运动风格控制**。
- **交叉注意力路径**（蓝色分支）：保留姿态序列的时间结构，将每帧姿态投影为令牌后与视觉特征进行交叉注意力计算（Eq. 13）。这提供了 **帧级、细粒度的局部对齐能力**。

消融实验（Table 3）表明，单独使用任一路径均无法达到最优效果：仅 AdaLN 缺乏帧级对齐精度，仅交叉注意力缺少全局运动一致性。**双路径联合使用在所有指标上均取得最佳结果**（SSIM 52.60, mIoU 37.40, TransError 5.59），验证了全局调制与局部注意力协同的必要性。

### 3. 全身控制 vs. 仅头部控制

与仅使用头部姿态控制的消融基线相比，EgoControl 的全身姿态控制使 mIoU 提升约 55%，手臂可见性一致性超过 96%（Table 1）。这直接证明了 **引入全身关节信息是实现精细肢体交互生成的因果开关**——头部姿态仅能约束相机视角，而手臂与物体的合理交互需要显式的关节级控制。

### 与并发工作的差异

并发工作 **PEVA** 使用 3D 上半身姿态生成单帧，而 EgoControl 生成完整的 **视频序列** 并控制 **全身** 姿态。在 2 秒后的未来帧生成对比中，EgoControl 的 LPIPS（24.3 vs 29.8）和 DreamSim（11.3 vs 18.6）均显著优于 PEVA XXL（Table 2），表明时序建模与全身控制的联合设计对第一人称视频生成质量至关重要。

## 整体框架

EgoControl 是一个基于连续时间潜空间扩散模型的可控第一人称视频生成框架。其核心任务可形式化为：给定一段包含 13 帧的过去视觉上下文 $x$ 以及未来 $M=32$ 帧的目标 3D 全身姿态序列 $P$，生成与之时空对齐的未来 2 秒第一人称视频。框架的设计围绕一个核心瓶颈展开——现有方法无法同时建模相机佩戴者的全局头部运动与局部肢体交互，导致生成视频中身体姿态与视觉内容严重脱节。

### Pipeline 总览

整个 pipeline 由三个关键阶段串联构成，如图 Figure 2 所示：

![[assets/figures/papers/paper_list_l964_https_arxiv_org_abs_2511_18173/figures/002_Figure_2.jpg]]
*Figure 2: EgoControl generates future egocentric frames conditioned on the past frames and sequence of human poses. We condition the model on the human poses in two ways. The purple branch uses the networks*

1. **潜空间编解码**：使用一个预训练的 tokenizer $E$ 将每一帧映射到紧凑的连续潜变量 $z_0 = E(x)$，生成完成后通过解码器 $D$ 恢复为像素空间帧。这一压缩步骤使扩散过程在低维流形上进行，显著降低了计算开销。

2. **姿态表示构造**（详见第 3.1 节）：将原始 3D 全身姿态序列转化为一种差分、骨盆相对的组合表示 $P = [\Delta h, \Delta r, J]$，其中 $\Delta h$ 为相邻帧间的头部相对平移变换，$\Delta r$ 为头部相对旋转变换，$J$ 为各关节相对于骨盆的当前位置。这种分解将全局相机运动与局部肢体动态解耦，是实现精确姿态控制的关键设计。

3. **条件扩散生成**：以过去帧的潜变量和构造好的姿态序列 $P$ 为条件，在 DiT（Diffusion Transformer）去噪主干中通过两条互补路径注入姿态控制信号：
   - **AdaLN 调制分支（紫色路径）**：将整个姿态序列展平后通过 MLP 编码为全局嵌入 $e_P$，进而预测每个 Transformer 块的偏移 $\beta$、缩放 $\gamma$ 和门控 $g$ 参数，对自注意力、交叉注意力和 MLP 层的归一化特征进行条件调制。
   - **交叉注意力分支（蓝色路径）**：保留姿态序列的时间结构，将每帧姿态向量投影为帧级姿态令牌 $P'_m$，与编码后的视觉令牌进行交叉注意力计算，提供帧粒度的局部控制。

两条路径的协同是框架设计的核心因果调节旋钮：AdaLN 提供全局风格级调制，交叉注意力提供时序对齐的细粒度控制。消融实验（Table 3）证实，单独使用任一路径均会导致视觉质量或运动精度的显著下降，二者联合才能实现最优的生成质量与姿态对齐。

### 输入输出流

- **输入**：
  - 过去视觉上下文：$N=13$ 帧 RGB 第一人称视频帧，提供场景几何与外观的先验。
  - 目标姿态序列：$M=32$ 帧的 3D 全身姿态，包含头部 6-DoF 变换和 23 个关节的 3D 位置。

- **输出**：$M=32$ 帧的未来第一人称视频，相机视角跟随目标头部姿态，可见肢体与场景物体产生合理交互。

- **训练信号**：采用连续时间扩散的 v-prediction 范式。前向过程对干净潜变量 $z_0$ 施加高斯噪声 $z = z_0 + \sigma \varepsilon$，去噪网络 $z_\theta$ 直接预测原始干净潜变量，损失函数为加权均方误差：
  $$\mathcal{L}(\theta) = \mathbb{E}_{z_0,\varepsilon,\sigma,c} \big[ w(\sigma) \big\lVert z_\theta(z,\sigma,c) - z_0 \big\rVert_2^2 \big]$$
  其中条件 $c$ 同时包含过去视觉上下文和姿态序列 $P$，权重 $w(\sigma)$ 随噪声水平自适应调整。

### 关键设计决策

框架中有两个改变游戏规则的表示选择，其因果效应在消融实验中得到严格验证：

- **差分 vs. 累积头部表示**：累积绝对变换表示将平移误差（TransError）推高至 12.31 cm，而差分相对变换将其降至 6.75 cm（Table 4）。原因在于差分表示直接编码帧间运动增量，与扩散模型学习残差变化的归纳偏置高度契合。

- **骨盆相对 vs. 每帧相对关节表示**：将关节位置表示为相对于骨盆的当前帧坐标（$J$），相比每帧关节相对上一帧的差分运动（$\Delta j$），使手臂分割 mIoU 从 31.85 提升至 37.40（Table 4）。骨盆相对表示提供了稳定的身体中心参照系，避免了误差在关节链上的累积传播。

### 推理配置

推理时采用 classifier-free guidance，引导权重设为 2，以增强姿态条件对生成过程的约束力。训练期间以 0.2 的概率随机丢弃上下文帧，提升模型对不完整观测的鲁棒性。所有实验均基于 Cosmos 预训练权重进行微调，并移除其默认的安全过滤模块以确保评估公平性。

## 核心模块与公式推导

EgoControl 的核心架构建立在连续时间潜变量扩散模型之上，其关键创新在于设计了一种紧凑且信息丰富的3D全身姿态表示，并通过双路径控制机制将其注入去噪过程。

### 3.1 扩散模型基础

EgoControl 采用连续时间扩散框架。给定一段第一人称视频，首先通过预训练的潜空间编码器 $E$ 将每一帧映射到紧凑的连续潜变量 $z_0 = E(x)$。前向扩散过程通过向干净潜变量注入高斯噪声进行扰动：

$$
z = z_0 + \sigma \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, I)
$$

去噪网络 $z_{\theta}$ 被训练为直接从带噪潜变量预测原始干净潜变量 $z_0$，其训练损失函数为加权均方误差：

$$
\mathcal{L}(\boldsymbol{\theta}) = \mathbb{E}_{z_0,\varepsilon,\sigma,c} \big[ w(\sigma) \big\lVert z_{\theta}(z,\sigma,c) - z_0 \big\rVert_2^2 \big]
$$

其中 $c$ 为条件上下文，包括过去帧的视觉信息 $x$ 和目标人体姿态序列 $\mathbf{P}$；$w(\sigma)$ 为噪声水平相关的权重函数。

### 3.2 3D全身姿态表示

姿态控制的核心在于如何表示相机佩戴者的运动意图。EgoControl 将3D全身姿态分解为三个互补分量，形成统一的姿态张量 $\mathbf{P} \in \mathbb{R}^{M \times 23 \times 6}$（$M$ 为帧数）：

**差分头部变换** $\Delta \mathbf{h}$：为精确控制第一人称相机的全局运动，采用相邻帧间的相对变换而非累积绝对位姿。对于帧 $i$，其相对头部变换定义为：

$$
\Delta \mathbf{H}_i = \mathbf{H}_i \mathbf{H}_{i-1}^{-1}, \quad \forall i \in [1, M]
$$

其中 $\mathbf{H}_i \in SE(3)$ 为第 $i$ 帧的头部6自由度位姿。该差分表示使模型学习帧间运动增量，显著降低了平移误差（TransError 从累积表示的 12.31 cm 降至 6.75 cm，Table 4）。

**骨盆相对位移** $\Delta \mathbf{r}$：编码骨盆在相邻帧间的相对变换，捕捉身体躯干的全局运动。

**关节相对骨盆位置** $\mathbf{J}$：将每一帧的23个身体关节坐标表示为相对于骨盆坐标系的位置，而非每帧关节相对上一帧的差分运动 $\Delta j$。消融实验表明，这种骨盆中心表示将 mIoU 从 31.85 提升至 37.40（Table 4），因为其为模型提供了关节在空间中的绝对构型信息，更有利于学习肢体与场景的交互对齐。

最终姿态表示由上述三分量拼接而成：

$$
\mathbf{P} = [ \Delta \mathbf{h}, \Delta \mathbf{r}, \mathbf{J} ] \in \mathbb{R}^{M \times 23 \times 6}
$$

### 3.3 双路径姿态控制机制

EgoControl 采用两条互补路径将姿态信息注入 DiT 去噪主干网络（如图 Figure 2 所示）：

**AdaLN 调制分支（紫色路径）**：将完整的姿态序列 $\mathbf{P}$ 扁平化后，通过两个 MLP 网络 $g_e$ 和 $g_m$ 分别提取全局姿态嵌入 $\mathbf{e}_P$ 和调制向量 $\mathbf{m}_P^{\beta\gamma g}$。在每个 Transformer 块 $k$ 中，从姿态嵌入预测偏移 $\boldsymbol{\beta}_P^{(k)}$、缩放 $\boldsymbol{\gamma}_P^{(k)}$ 和门控 $\mathbf{g}_P^{(k)}$ 参数：

$$
[\boldsymbol{\beta}_P^{(k)}, \boldsymbol{\gamma}_P^{(k)}, \mathbf{g}_P^{(k)}] = \mathbf{W}_{m1}^k \mathbf{W}_{m2}^k \mathrm{SiLU}(\mathbf{e}_P) + \mathbf{m}_P^{\beta\gamma g}
$$

这些参数通过自适应层归一化（AdaLN）对自注意力、交叉注意力和 MLP 模块的特征进行条件调制：

$$
\mathrm{AdaLN}^{(k)}(\mathbf{u}; \boldsymbol{\beta}_P^{(k)}, \boldsymbol{\gamma}_P^{(k)}) = \mathbf{LN}(\mathbf{u}) \odot (1 + \boldsymbol{\gamma}_P^{(k)}) + \boldsymbol{\beta}_P^{(k)}
$$

调制分支提供全局、粗粒度的姿态控制信号。

**交叉注意力分支（蓝色路径）**：为保留姿态序列的时间结构，将每帧的姿态向量 $\mathbf{P}_m$ 通过线性投影和激活函数映射为姿态令牌：

$$
\mathbf{P}_m^{'} = \mathrm{LayerNorm}(\mathrm{GELU}(\mathbf{W}_p \mathbf{P}_m))
$$

这些帧级姿态令牌通过交叉注意力机制与编码后的视觉令牌交互，提供局部、细粒度的帧级控制。两条路径的时间步嵌入与姿态嵌入相加后共同调制网络：$\mathbf{e}_P = \mathbf{e}_t + \mathbf{e}_P$，$\mathbf{m}_P^{\beta\gamma g} = \mathbf{m}_t^{\beta\gamma g} + \mathbf{m}_P^{\beta\gamma g}$。

消融实验（Table 3）证实，单独使用 AdaLN 或交叉注意力均无法达到最优效果，双路径联合设计在视觉质量（SSIM 52.60, LPIPS 36.79）和运动精度（mIoU 37.40, TransError 5.59 cm）上均取得最佳性能。

## 实验与分析

### 实验设置

**数据集与预处理。** 实验基于Nymeria数据集，包含超过1,100段高分辨率第一人称视频，每段均与3D全身姿态同步标注。从中选取186段视频，统一重采样至16 FPS并缩放至480×480分辨率。模型以45帧的视频片段训练，使用前13帧作为过去视觉上下文，生成未来32帧（对应2秒），并以完整3D全身姿态序列作为控制条件。

**基线方法。** 实验设置三类对比基线：（1）**Cosmos微调基线**，仅使用过去帧进行视频预测，不注入姿态控制；（2）**仅头部控制**，仅使用头部姿态信息进行条件生成；（3）并发工作**PEVA**，使用3D上半身姿态生成单帧未来图像，输入为15帧过去帧（4 FPS，224×224）。

**评估指标。** 从四个维度系统评估生成质量：
- **帧保真度**：SSIM、LPIPS、DreamSim；
- **视频质量**：FVD；
- **运动控制精度**：平移误差（TransError，cm）、旋转误差（RotError，度），通过估计生成帧的相机运动并与真值头部轨迹比较得到；
- **身体姿态对齐**：mIoU与手臂可见性一致性（Acc%）。具体而言，使用SAM2对生成帧与真值帧中的可见手臂进行分割与跟踪（Figure 3），计算分割掩码的mIoU，并统计手臂可见性一致的帧比例。

![[assets/figures/papers/paper_list_l964_https_arxiv_org_abs_2511_18173/figures/003_Figure_3.jpg]]
*Figure 3: SAM2 [40] is used to segment and track the visible arms in both ground truth (first row) and the generated frames (second row). The extracted segmentation masks (highlighted in red) are then used to assess the quality of body pose control with mIoU and Acc%*

**公平性说明。** 所有方法采用相同的13帧过去帧条件，并移除Cosmos默认的安全过滤模块以确保评估公平。推理时使用classifier-free guidance，权重为2；训练时随机丢弃上下文帧的概率为0.2。

---

### 主要结果

**Table 1** 汇总了EgoControl与各基线在四个维度上的定量对比。EgoControl在所有指标上均显著优于微调基线和仅头部控制基线。核心发现包括：

- **身体姿态对齐大幅提升**：与仅使用头部姿态控制相比，EgoControl的mIoU提升约55%，手臂可见性一致性超过96%。这表明引入全身姿态控制后，生成帧中手臂的位置与姿态序列高度吻合。
- **运动控制精度改善**：在平移误差和旋转误差上，EgoControl均取得最低值，验证了差分头部表示与骨盆相对关节表示对相机运动建模的有效性。
- **帧保真度与视频质量**：SSIM、LPIPS、DreamSim和FVD四项指标全面领先，说明全身姿态控制不仅提升了运动对齐，也改善了生成帧的视觉真实感。

**Table 2** 展示了与并发工作PEVA XXL的对比。在生成未来2秒的单帧时，EgoControl的LPIPS（×100）为24.3，显著优于PEVA的29.8；DreamSim（×100）为11.3，远低于PEVA的18.6。需注意PEVA使用15帧4 FPS的低分辨率输入且仅生成单帧，而EgoControl以13帧16 FPS的高分辨率输入生成连续32帧，两者设置不完全对等，但EgoControl在更丰富的输出要求下仍展现出明显优势。

---

### 消融实验

**控制机制消融（Table 3）。** 为验证AdaLN调制与交叉注意力双路径设计的必要性，实验对比了三种变体：仅AdaLN、仅交叉注意力、以及二者联合（完整EgoControl）。结果表明，联合使用两条路径在所有指标上均取得最优性能——SSIM达52.60，LPIPS为36.79，DreamSim为10.94，FVD为27.51，mIoU为37.40，TransError为5.59 cm，RotError为5.23°。单独使用任一路径均导致性能下降，证实了全局调制与帧级局部注意力的互补性：AdaLN提供全局姿态风格调制，交叉注意力保留帧间时间结构以提供精细的空间对齐。

**姿态表示消融（Table 4）。** 针对姿态表示的设计选择，实验从两个关键维度进行消融：

1. **头部运动表示**：对比累积绝对变换与帧间差分相对变换（Δh）。差分表示将平移误差从12.31 cm降至6.75 cm，降幅约45%，验证了相对运动编码对相机轨迹建模的优越性。
2. **关节表示**：对比每帧关节相对于上一帧的差分运动（Δj）与关节相对于骨盆的当前位置（J）。骨盆相对表示将mIoU从31.85提升至37.40，提升约17%，表明以骨盆为中心的关节表示更有利于身体姿态与生成帧的空间对齐。

完整姿态表示 **P = [Δh, Δr, J]** 在各项指标上均取得最优结果，验证了差分头部运动、骨盆相对运动和关节相对骨盆位置这一组合表示的有效性。

---

### 失败模式与局限性

尽管EgoControl在定量指标和定性可视化中表现优异，论文仍明确指出以下局限：

1. **数据域泛化**：模型仅在Nymeria数据集上训练和评估，对其他第一人称数据集（如日常场景、不同相机佩戴方式）的泛化能力尚未验证。实际部署中可能面临域偏移问题。
2. **姿态输入依赖**：方法依赖于完整的3D全身姿态输入，包括23个关节的精确位置。在实际应用中，获取如此精确的3D姿态可能存在困难，尤其是手部等精细部位。
3. **生成长度受限**：训练片段固定为32帧（2秒），自回归式扩展可能引入误差累积，导致长视频的视觉质量下降和姿态漂移。
4. **精细交互控制不足**：对手部姿态和精细物体交互的控制仍需提升。当前主要通过手臂分割间接评估身体控制质量，缺乏对手指动作和物体操纵的直接建模与评估。

这些局限指向了未来工作的方向：引入显式手部姿态标注以提升精细关节控制，以及改进对日常场景、不同衣着和传感器配置的域外泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l964_https_arxiv_org_abs_2511_18173/figures/004_Table_1.jpg]]
*Table 1: EgoControl (row 4) shows notable improvements across all dimensions over the baseline and the head only control*

![[assets/figures/papers/paper_list_l964_https_arxiv_org_abs_2511_18173/figures/005_Table_2.jpg]]
*Table 2: Comparison with PEVA XXL. Note that PEVA uses 15 past frames at 4 FPS (224 × 224) as conditioning and generates a single frame in the future. The comparison is for a generated frame 2 seconds in the future*

![[assets/figures/papers/paper_list_l964_https_arxiv_org_abs_2511_18173/figures/007_Table_3.jpg]]
*Table 3: Ablation on the control mechanism*

![[assets/figures/papers/paper_list_l964_https_arxiv_org_abs_2511_18173/figures/006_Table_4.jpg]]
*Table 4: Ablation on the pose representation*

![[assets/figures/papers/paper_list_l964_https_arxiv_org_abs_2511_18173/figures/008_Figure_4.jpg]]
*Figure 4: Pose alignment (mIoU) and SSIM for each of the 32 generated frames. The green line denotes the fully trained model*

![[assets/figures/papers/paper_list_l964_https_arxiv_org_abs_2511_18173/figures/009_Figure_5.jpg]]
*Figure 5: Given the same initial context, EgoControl is capable of generating videos following different body movements. See videos in the supp. material for better visualization*

![[assets/figures/papers/paper_list_l964_https_arxiv_org_abs_2511_18173/figures/011_Figure_7.jpg]]
*Figure 7: Comparing EgoControl (fourth row) to ground truth (first row), finetuning (second row), and head only control (third row)*

![[assets/figures/papers/paper_list_l964_https_arxiv_org_abs_2511_18173/figures/012_Figure_9.jpg]]
*Figure 9: Applying different sequences of human poses to the same context frames. EgoControl is capable of generating videos following the different body movements*

![[assets/figures/papers/paper_list_l964_https_arxiv_org_abs_2511_18173/figures/013_Figure_10.jpg]]
*Figure 10: Videos of 8 seconds generated by EgoControl*

![[assets/figures/papers/paper_list_l964_https_arxiv_org_abs_2511_18173/figures/010_Figure.jpg]]

## 方法谱系与知识库定位

### 与现有工作的关系

EgoControl 处于第一人称视频生成与人体运动控制两个方向的交叉点。其直接技术底座是 **Cosmos** 的潜空间条件视频扩散模型，EgoControl 将其作为去噪主干与微调基线。Cosmos 本身是一个面向通用视频预测的大规模扩散模型，但原始版本并不具备对相机佩戴者身体姿态的显式控制能力。

与该工作最接近的并发方法是 **PEVA**，它同样利用 3D 上半身姿态生成第一人称未来帧。但 PEVA 的设计存在两个关键差异：其一，它仅生成单帧未来图像（2 秒后），而非连续视频；其二，它使用 15 帧过去上下文在 4 FPS、224×224 分辨率下进行条件控制。EgoControl 在 Nymeria 数据集上对同一未来时刻（2 秒后）的生成质量显著优于 PEVA XXL：LPIPS 从 29.8 降至 24.3，DreamSim 从 18.6 降至 11.3（Table 2）。这一差距的核心原因在于 EgoControl 的差分姿态表示与双路径控制机制能够更精确地建模全局相机运动与局部肢体动态的耦合关系。

在仅使用头部姿态控制的消融基线上，EgoControl 的优势更为突出。头部控制变体仅能约束相机视角，无法显式控制手臂等身体部位的位置与可见性，导致生成的手臂与真值之间的 mIoU 极低。引入全身姿态控制后，mIoU 提升约 55%，手臂可见性一致性超过 96%（Table 1）。这表明，对于第一人称视频生成任务，单纯的相机运动控制不足以实现身体部位与场景的合理交互，完整的 3D 全身姿态信号是必要的信息增量。

### 适用边界

EgoControl 的有效性边界由以下因素共同界定：

**数据依赖性**：模型仅在 **Nymeria** 数据集上训练和评估。该数据集包含超过 1100 段高分辨率第一人称视频，与 3D 全身姿态同步标注，使用 Movella Xsens 动作捕捉系统采集（ Movella, 2021）。视频被重采样至 16 FPS、缩放至 480×480，最终使用 186 段视频的子集。Nymeria 的场景分布、相机佩戴方式与参与者的运动模式构成了模型已知的分布范围。对于其他第一人称数据集（如 Ego4D、EPIC-Kitchens）的泛化能力尚未验证，需要谨慎对待。

**姿态输入要求**：模型依赖完整的 3D 全身姿态序列作为控制信号，具体为 23 个关节相对于骨盆的 3D 位置、头部帧间差分平移与旋转、以及骨盆的帧间差分运动。在实际部署中，获取如此精确的 3D 姿态通常需要动作捕捉设备或多视角视觉系统，这限制了模型的即插即用能力。

**时序范围**：训练时使用 13 帧过去上下文（约 0.81 秒）生成 32 帧未来（2 秒）。推理时可通过自回归方式扩展至更长序列（如 Figure 10 展示的 8 秒生成），但自回归过程可能引入误差累积和视觉质量退化，论文未对此进行系统量化。

**控制粒度**：当前姿态控制主要通过手臂分割的 mIoU 和可见性一致性来间接评估。对于手部姿态和精细物体交互的直接控制能力仍然有限，这是一个明确的局限性。

### 局限与开放问题

论文明确指出的局限包括：仅在 Nymeria 数据集上验证；依赖完整 3D 全身姿态输入；生成长度受限于训练片段长度，自回归扩展存在质量退化风险；对手部姿态和精细物体交互的控制不足。

由此引出的开放问题有两个核心方向：

1. **细粒度手部控制**：如何将显式的手部姿态标注（如手指关节角度）融入当前的姿态表示与控制框架，以实现对手部与物体交互的精细控制？当前框架的关节表示仅覆盖 23 个身体关节，手部信息被高度压缩，需要设计专门的表示与注入路径。

2. **分布外泛化**：如何提升模型对日常视角、不同衣物、不同传感器佩戴方式的泛化能力？Nymeria 的采集环境与设备相对受控，向更自然的第一人称视频分布迁移时，域差异可能导致姿态控制精度和视觉质量同时下降。这可能需要域自适应训练策略或更大规模、更多样化的标注数据。

此外，一个隐含但值得关注的问题是：当前的双路径控制机制（AdaLN 调制 + 交叉注意力）虽然在消融实验中证明了两者联合使用的必要性（Table 3），但两种路径各自承担的功能分工——全局调制负责整体风格与相机运动，交叉注意力负责帧级局部对齐——是否在更复杂的场景中仍然有效，尚需进一步验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/EgoControl_Controllable_Egocentric_Video_Generation_via_3D_Full_Body_Poses.pdf]]