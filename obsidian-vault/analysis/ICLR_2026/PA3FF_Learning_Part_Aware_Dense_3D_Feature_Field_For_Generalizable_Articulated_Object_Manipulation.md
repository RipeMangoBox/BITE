---
title: "PA3FF:Learning Part-Aware Dense 3D Feature Field For Generalizable Articulated Object Manipulation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/PA3FF_Learning_Part_Aware_Dense_3D_Feature_Field_For_Generalizable_Articulated_O_591e4e474026.pdf
project_link: "https://pa3ff.github.io/"
code_link: null
aliases:
- PA3FFPPADPP
- PA3FF
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 部件感知的3D特征场（PA3FF），通过在大规模标注数据集上使用对比学习（几何损失和语义损失）训练，直接为点云生成稠密、连续、功能部件敏感的3D特征，特征距离直接反映部件归属关系。
primary_logic: 利用3D原生骨干（Sonata）提供几何先验，并结合对比学习引入部件级语义一致性，使得3D特征场能够区分和定位功能部件（如把手、旋钮），从而为模仿学习策略提供强泛化性的感知基础。
claims:
- PA3FF预测的连续3D特征场中，特征距离直接反映部件归属：相似部件的点具有相似特征。
- PADP在PartInstruct基准上取得了9.4%的绝对性能提升，达到SOTA。
- 在8个真实世界任务上，PADP显著超越最强基线GenDP，相对提升18.75%。
- 消融研究表明，移除对比学习导致的部件感知细化会使成功率从62%下降到46%，证明其至关重要。
---

# PA3FF:Learning Part-Aware Dense 3D Feature Field For Generalizable Articulated Object Manipulation

> [!tip] 核心洞察
> 利用3D原生骨干（Sonata）提供几何先验，并结合对比学习引入部件级语义一致性，使得3D特征场能够区分和定位功能部件（如把手、旋钮），从而为模仿学习策略提供强泛化性的感知基础。

| 字段 | 内容 |
|------|------|
| 中文题名 | PA3FF：学习部件感知的稠密3D特征场以实现可泛化的铰接物体操控 |
| 英文题名 | PA3FF:Learning Part-Aware Dense 3D Feature Field For Generalizable Articulated Object Manipulation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=qXfRXfAHOK) · [Project](https://pa3ff.github.io/) · [arXiv](https://arxiv.org/abs/2410) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | Part-Aware 3D Feature Field (PA3FF) with Part-Aware Diffusion Policy (PADP) |
| Dataset | PartInstruct, 8 real-world tasks, Real-world Open Bottle test, RLBench |

> [!tip] 效果简介
> - PartInstruct (simulated, average over 5 test sets) 上，Success Rate (%) 28.79 ± 2.5 vs 19.36 ± 2.7 (GenDP) (+9.43)。
> - PartInstruct (as reported in paper) 上，Absolute gain over SOTA PADP vs previous SOTA (+9.4% absolute)。
> - 8 real-world tasks (unseen objects, mean) 上，Success Rate (%) 58.75 vs 35 (GenDP, highest baseline) (+23.75 (23.75 percentage points, 18.75% relative improvement reported))。

## 概述

铰接物体的通用操控是机器人学习中的核心挑战。其瓶颈在于：现有方法大多依赖2D基础视觉特征（如CLIP、DINOv2）并将其提升到3D空间，但这些特征面临**多视图不一致、空间分辨率低、难以捕捉细小功能部件**等问题，导致在未见物体上的泛化能力严重不足。

针对上述瓶颈，本文的核心洞见是：**直接利用3D原生骨干提供几何先验，并结合对比学习引入部件级语义一致性**，使得3D特征场能够区分和定位功能部件（如把手、旋钮），从而为模仿学习策略提供强泛化性的感知基础。具体而言，本文提出**部件感知的3D特征场（PA3FF）**，通过在大规模标注数据集上使用几何损失和语义损失进行对比学习训练，直接为点云生成稠密、连续、功能部件敏感的3D特征，使得特征距离直接反映部件归属关系——相似部件的点具有相似特征。在此基础上，本文进一步提出**部件感知扩散策略（PADP）**，将PA3FF特征与扩散动作生成相结合，实现高效且可泛化的操控。

实验结果表明，PADP在PartInstruct仿真基准上取得了**9.4%的绝对性能提升**，达到SOTA；在8个真实世界任务上，PADP显著超越最强基线GenDP，相对提升**18.75%**。消融研究进一步验证了部件感知对比学习的关键作用：移除特征细化组件后，成功率从62%骤降至46%。

**方法定位**：PA3FF属于3D原生特征表征学习范式，与依赖2D基础模型提升的方法（如GenDP）形成对比。其核心创新在于将3D几何预训练（Sonata骨干）与部件级对比学习相结合，在特征空间中显式编码了功能部件的归属关系，而非仅依赖语义相似性。PADP则将该特征场与扩散策略（Diffusion Policy, DP3）无缝集成，形成从感知到动作的端到端可泛化操控框架。

## 背景与动机

### 铰接物体操控的泛化困境

机器人操控正从刚性物体推向更复杂的铰接物体（如带把手的抽屉、旋钮式瓶盖），这类物体由多个功能部件构成，操控策略必须精确绑定到特定部件（如“抓住把手拉开抽屉”）。然而，现有方法在泛化到未见过的物体时面临根本性瓶颈：感知表示无法稳定地识别和定位功能部件。

### 2D基础特征提升到3D的固有缺陷

当前主流范式依赖2D视觉基础模型（如CLIP、DINOv2、Grounded-SAM）提取语义特征，再通过多视图投影将其“提升”到3D空间。这一路径存在三重结构性缺陷：

1. **多视图不一致**：不同视角下同一3D点的2D特征可能剧烈变化，导致融合后的3D表示在空间上不连续、不可靠。
2. **低空间分辨率**：2D特征图的分辨率限制使得细小功能部件（如旋钮、把手边缘）在投影过程中被模糊或丢失。
3. **部件感知缺失**：2D模型训练目标与部件级功能语义无关，提升后的3D特征缺乏对“哪些点属于同一功能部件”的感知能力。

这些缺陷直接导致下游操控策略在面对新物体时泛化失败——策略无法可靠地定位操作目标部件。

### 3D原生表示的机会与未利用的潜力

3D原生骨干网络（如基于Point Transformer的Sonata）直接从点云提取几何特征，天然避免了多视图不一致问题。但现有3D表示方法存在两个关键缺口：

- **缺乏部件级语义监督**：3D骨干通常仅在几何重建或分类任务上预训练，输出特征虽能捕捉形状信息，却无法区分功能部件（如瓶盖与瓶身）的语义边界。
- **特征密度与抽象能力的权衡**：标准3D骨干使用大量下采样层以扩大感受野，但这牺牲了对小部件的空间分辨率，导致细节丢失。

### 本文动机

本文的核心判断是：**铰接物体操控的泛化瓶颈在于感知表示本身，而非策略架构**。为此，需要一种同时满足以下四个条件的3D特征表示：

- **部件感知（Part-Aware）**：特征距离直接反映部件归属关系——同一部件的点特征相似，不同部件的点特征可区分。
- **3D原生（3D-Native）**：直接从点云生成，避免2D提升带来的不一致性。
- **稠密（Dense）**：为点云中每个点赋予连续特征向量，保留细粒度空间信息。
- **语义对齐（Semantically Grounded）**：特征与功能部件语义（如“handle”“knob”）对齐，支持跨物体的泛化。

基于此，本文提出PA3FF（Part-Aware 3D Feature Field），一种前馈式部件感知3D特征场，通过对比学习在大规模标注数据集上训练，使特征场具备上述四个属性。在此基础上构建的PADP（Part-Aware Diffusion Policy）策略，将PA3FF作为感知基础，实现对新物体的高效泛化操控。

## 核心创新

PA3FF 的核心创新在于将**部件感知的对比学习**引入到**3D原生特征场**中，从而系统性地解决了2D基础模型（如CLIP、DINOv2）在提升到3D空间时面临的多视图不一致、低空间分辨率、难以捕捉细小功能部件等瓶颈。与现有方法直接使用通用2D/3D特征作为感知输入不同，PA3FF通过两个关键的**changed slots**实现了突破。

**Slot 1：3D特征骨干的深度改造。** 基线方法通常采用原始的Sonata（基于PTv3）或2D基础模型提升到3D，这些骨干包含大量下采样层，虽然能捕获全局几何结构，但会丢失对功能部件至关重要的细节信息。PA3FF对PTv3架构进行了针对性修改：**移除大部分下采样层，并通过堆叠额外的Transformer块来加深网络**。这一改动在保留高分辨率空间信息的同时，增强了特征抽象能力，为后续的部件级区分提供了几何先验基础。消融实验证实，仅此架构修改即可带来4个百分点的性能提升（从58%到62%，Table 6）。

**Slot 2：部件感知的对比学习框架。** 这是PA3FF最核心的创新，也是性能提升的主要来源。单纯的Sonata输出缺乏显式的部件语义，无法保证同一部件的点具有相似特征。PA3FF引入了一个双损失对比学习框架：

- **几何损失** $\mathcal{L}_{Geo}$：有监督对比损失，在特征空间中**拉近同一部件的点特征，推远不同部件的点特征**，直接强化部件内一致性和部件间区别性。
- **语义损失** $\mathcal{L}_{Sem}$：InfoNCE损失，将点特征与SigLIP编码的部件名语义向量进行对齐，使特征场不仅知道“哪些点属于同一部件”，还理解“这个部件是什么”。

两个损失联合优化（$\mathcal{L}_{total} = \mathcal{L}_{Geo} + \mathcal{L}_{Sem}$），使得PA3FF预测的连续3D特征场中，特征距离直接反映部件归属关系——相似特征的更可能属于同一功能部件。消融实验表明，**移除语义损失导致成功率从62%骤降至46%**，移除几何损失降至54%，而完全移除对比学习细化（仅Sonata + DP3）仅达39%，接近DP3基线的37%，证明对比学习是性能提升的决定性因素。

**因果机制：** 这一创新设计形成了一条清晰的因果链：3D原生骨干提供几何先验 → 对比学习引入部件级语义一致性 → 特征场能够区分和定位功能部件（如把手、旋钮）→ 扩散策略获得强泛化性的感知基础 → 在新物体和新场景上实现高效操控。与GenDP等基于密集语义场的方法相比，PA3FF的部件感知是**3D原生的、连续的、功能导向的**，而非对2D特征的简单提升，这解释了其在PartInstruct上9.4%的绝对性能提升和在8个真实世界任务上相对GenDP 18.75%的提升。

## 整体框架

PA3FF 的整体框架围绕一个核心问题展开：**如何为铰接物体操控提供一个部件感知的、可泛化的 3D 表示**。其瓶颈在于，现有 2D 基础模型（如 CLIP、DINOv2）在提升到 3D 空间时面临多视图不一致、空间分辨率低、难以捕捉细小功能部件（如把手、旋钮）等挑战。PA3FF 的因果调节变量是**部件感知的 3D 特征场**——通过在大规模标注数据集上使用对比学习直接为点云生成稠密、连续、功能部件敏感的 3D 特征，使得特征距离直接反映部件归属关系。

框架由三个顺序衔接的模块组成，形成从感知到动作的端到端流水线：

### 模块一：3D 特征提取（Sonata 主干）

输入为场景的 **3D 点云**，首先通过修改版的 **Sonata**（基于 Point Transformer V3 的自监督预训练骨干）提取多尺度稠密 3D 几何特征。关键改动在于：移除了 PTv3 中的大部分下采样层，转而堆叠额外的 Transformer 块来加深网络。这一设计的因果逻辑是——下采样虽然提升计算效率，但会丢失对细小功能部件至关重要的空间细节；通过保留更高分辨率的特征图并增强特征抽象能力，Sonata 为后续的部件感知学习提供了更丰富的几何先验。

### 模块二：部件感知特征细化（对比学习）

Sonata 输出的原始 3D 特征尚不具备明确的部件语义。细化阶段引入**对比学习框架**，通过两个互补的损失函数为特征注入部件感知能力：

- **几何损失** $\mathcal{L}_{Geo}$：有监督对比损失，拉近同一部件内点的特征，推远不同部件点的特征，确保部件内一致性和部件间可区分性。
- **语义损失** $\mathcal{L}_{Sem}$：InfoNCE 损失，将点特征与 SigLIP 编码的部件名语义向量对齐，使特征空间获得语言锚定的语义含义。

总损失 $\mathcal{L}_{total} = \mathcal{L}_{Geo} + \mathcal{L}_{Sem}$ 联合优化，输出一个**连续的 3D 特征场** $f: \mathbb{R}^3 \to \mathbb{R}^n$，其中特征距离直接反映部件归属——相似部件上的点具有相似特征。该特征场以 feedforward 方式预测，无需对每个新物体重新优化。

### 模块三：部件感知扩散策略（PADP）

细化后的 3D 特征场与机器人状态（如关节角度、末端执行器位姿）拼接，送入**部件感知扩散策略（PADP）**。PADP 由 Transformer 编码器和扩散动作头组成：编码器融合 3D 感知特征与机器人状态，扩散头通过 DDIM 去噪过程生成未来动作序列。训练时，向真实动作 $\mathbf{a}_t$ 添加噪声得到 $\tilde{\mathbf{a}}_t$，以 MSE 损失 $\mathcal{L}(\phi) := \mathrm{MSE}(\mathbf{a}_t, D_\theta(\mathbf{o}_t, \tilde{\mathbf{a}}_t, k))$ 训练扩散模型预测去噪动作。

### 输入输出流

- **输入**：场景点云 + 机器人状态 + 语言任务指令
- **中间表示**：Sonata 提取的多尺度几何特征 → 对比学习细化的部件感知 3D 特征场
- **输出**：未来 $T$ 步的动作序列（末端执行器位姿或关节目标）

消融实验揭示了各模块的因果贡献：移除对比学习细化（无几何损失和语义损失）导致成功率从 62% 骤降至 46%；直接组合 Sonata 与 DP3（无任何架构修改或细化）仅达 39%，接近 DP3 基线 37%，表明单纯替换骨干获益有限。语义损失比几何损失更为关键——移除语义损失性能下降更多（46% vs 54%），说明语言锚定的语义对齐对部件感知能力的形成具有主导作用。

### 补充图表

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_qXfRXfAHOK/figures/001_Figure_1.jpg]]
*Figure 1: (1) We propose PA3FF, a feedforward model that predicts part-aware 3D feature fields for 3d shapes. (2) We propose a part-aware diffusion policy, which leverages PA3FF, that can efficiently generalize to unseen objects. (3) PA3FF exhibits consistency across shapes, enabling various downstream applications such as correspondence and segmentation*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_qXfRXfAHOK/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our Learning Framework. (1) Pretraining the PTv3 backbone to extract part-aware 3D features. (2) Feature refinement via contrastive learning across objects to enhance part-level consistency and distinctiveness. (3) Downstream usage by integrating the refined features into a diffusion policy for action generation*

## 核心模块与公式推导

PA3FF 的核心设计围绕一个关键瓶颈展开：**2D 基础视觉特征（如 CLIP、DINOv2）在提升到 3D 空间时，面临多视图不一致、低空间分辨率、难以捕捉细小功能部件等挑战**，导致铰接物体操控的泛化能力不足。为此，PA3FF 构建了一个**部件感知的稠密 3D 特征场**，通过对比学习直接为点云生成功能部件敏感的连续特征，使特征距离直接反映部件归属关系。

整个学习框架（Figure 2）分为三个核心模块：

### 1. 3D 特征提取骨干（Sonata 主干）

PA3FF 采用 **Sonata**——一种自监督预训练的 Point Transformer V3（PTv3）——作为 3D 特征提取基础。为适配部件感知任务，对原始 PTv3 架构进行了关键修改：

- **移除大部分下采样层**：原始 PTv3 包含大量下采样操作，会丢失细小功能部件（如把手、旋钮）的几何细节。
- **堆叠额外 Transformer 块**：通过加深网络提升特征抽象能力，在保留空间分辨率的同时增强语义表达能力。

这一修改使骨干网络能够从点云中提取**多尺度密集 3D 几何特征**，为后续部件感知细化提供高质量的几何先验。

### 2. 部件感知特征细化（对比学习框架）

在 Sonata 输出的初始 3D 特征之上，PA3FF 引入一个**对比学习框架**，通过联合优化几何损失和语义损失，强制实现部件内特征一致性和部件间特征区别性。

#### 几何损失（Geometric Loss）—— 部件内聚、部件间分离

几何损失采用有监督对比学习范式，直接作用于 3D 特征空间：

$$
\mathcal { L } _ { G e o } = \sum _ { i = 1 } ^ { N } \frac { - 1 } { N _ { a _ { i } } - 1 } \sum _ { j = 1 } ^ { N } \mathbf { 1 } _ { i \neq j } \cdot \mathbf { 1 } _ { a _ { i } = a _ { j } } \cdot \log \frac { \exp { ( f _ { i } \cdot f _ { j } / \tau ) } } { \sum _ { k = 1 } ^ { N } \mathbf { 1 } _ { i \neq k } \cdot \exp { ( f _ { i } \cdot f _ { k } / \tau ) } }
$$

**变量含义**：
- $N$：点云中的总点数
- $f_i$：点 $i$ 的特征向量
- $a_i$：点 $i$ 所属的部件标签
- $N_{a_i}$：与点 $i$ 属于同一部件的点数
- $\tau$：温度系数，控制特征空间的分布锐度
- $\mathbf{1}_{i \neq j}$：指示函数，排除自身对比
- $\mathbf{1}_{a_i = a_j}$：指示函数，筛选同部件正样本对

**作用机制**：该损失拉近同一部件内点的特征距离（分子），同时推远不同部件点的特征距离（分母），直接在几何层面建立部件归属的判别性表示。

#### 语义损失（Semantic Loss）—— 跨物体语义对齐

语义损失通过 InfoNCE 形式，将点特征与部件名称的语义向量对齐：

$$
\mathcal { L } _ { S e m } = \sum _ { i = 1 } ^ { N } - \log \frac { \exp { ( \pmb { f } _ { i } \cdot \pmb { x } _ { a _ { i } } / \tau ) } } { \sum _ { k = 1 } ^ { m } \exp { ( \pmb { f } _ { i } \cdot \pmb { x } _ { k } / \tau ) } }
$$

**变量含义**：
- $\pmb{f}_i$：点 $i$ 的特征向量
- $\pmb{x}_{a_i}$：部件名 $a_i$ 经 SigLIP 编码得到的语义向量
- $m$：数据集中所有可能的部件类别数
- $\tau$：温度系数

**作用机制**：该损失使 3D 点特征与其对应部件名称的语义嵌入对齐，实现**跨物体的功能部件语义一致性**。例如，不同微波炉的“把手”点在特征空间中会被拉向相同的语义方向，从而支持泛化操作。

#### 总损失

两部分损失直接相加，构成联合优化目标：

$$
\mathcal { L } _ { t o t a l } = \mathcal { L } _ { G e o } + \mathcal { L } _ { S e m }
$$

消融实验（Table 6）揭示了两个损失的重要性差异：**语义损失比几何损失更为关键**——移除语义损失导致成功率从 62% 降至 46%，而仅移除几何损失降至 54%。这表明跨物体的语义对齐是部件感知泛化的核心驱动力。

### 3. 部件感知扩散策略（PADP）

PADP 接收 PA3FF 细化后的 3D 特征和机器人状态，通过 Transformer 编码器和扩散头生成动作序列。

**扩散训练损失**采用标准均方误差形式：

$$
\mathcal { L } ( \phi ) : = \mathrm { M S E } \left( \mathbf { a } _ { t } , D _ { \theta } \left( \mathbf { o } _ { t } , \tilde { \mathbf { a } } _ { t } , k \right) \right)
$$

其中 $\mathbf{a}_t$ 为真实动作序列，$D_\theta$ 为去噪网络，$\mathbf{o}_t$ 为观测（包含 PA3FF 特征），$\tilde{\mathbf{a}}_t$ 为加噪动作。

**加噪过程**：

$$
\tilde { \mathbf { a } } _ { t } : = \sqrt { \bar { \beta } ^ { k } } \mathbf { a } _ { t } + \sqrt { 1 - \bar { \beta } ^ { k } } \epsilon , \quad \epsilon \sim { \mathcal { N } } ( \mathbf { 0 } , \mathbf { I } ) , \quad k \sim \mathrm { U n i f o r m } ( \{ 1 , \dots , K \} )
$$

其中 $\bar{\beta}^k$ 为累积噪声调度参数，$k$ 为随机采样的扩散步数。

**推理时采用 DDIM 加速采样**，单步去噪迭代公式为：

$$
\mathbf { a } _ { t } ^ { k - 1 } = \frac { \sqrt { \bar { \beta } ^ { k - 1 } } \gamma ^ { k } } { 1 - \bar { \beta } ^ { k } } \mathbf { a } _ { t } ^ { 0 } + \frac { \sqrt { \beta ^ { k } } ( 1 - \bar { \beta } ^ { k - 1 } ) } { 1 - \bar { \beta } ^ { k } } \mathbf { a } _ { t } ^ { k } + \tau ^ { k } \mathbf { v }
$$

其中 $\mathbf{a}_t^0$ 为预测的干净动作，$\gamma^k$ 和 $\tau^k$ 为 DDIM 特定参数，$\mathbf{v}$ 为随机噪声项。

### 模块间的因果链路

整个框架的因果链路清晰：**Sonata 骨干提供几何先验 → 对比学习（几何损失 + 语义损失）注入部件级语义一致性 → PADP 利用部件感知特征生成泛化动作**。消融实验证实了这一链路的关键性：直接组合 Sonata 与 DP3（无任何架构修改或细化）仅达 39%，接近 DP3 基线 37%，表明单纯替换骨干获益有限；而移除对比学习细化则使成功率从 62% 骤降至 46%，证明部件感知特征场是泛化能力的决定性因素。

### 补充图表

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_qXfRXfAHOK/figures/011_Figure_7.jpg]]
*Figure 7: Flaws of lifting up method*

## 实验与分析

### 核心性能：仿真与真实世界

PA3FF 驱动的部件感知扩散策略（PADP）在仿真和真实世界两大平台上均取得了显著领先的性能。在仿真基准 **PartInstruct** 的五类测试集上，PADP 的平均成功率达到 **28.79% ± 2.5**，较此前最强的基线 **GenDP**（19.36% ± 2.7）实现了 **+9.43 个百分点**的绝对提升（Table 1）。这一结果直接验证了部件感知 3D 特征场对于泛化操控的核心价值。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_qXfRXfAHOK/figures/004_Table_1.jpg]]
*Table 1: Simulated results across five test sets. The best-performing results are highlighted in bold*

在真实世界实验中，这一优势被进一步放大。针对 8 项未见物体的操控任务，PADP 的平均成功率达到 **58.75%**，而最强基线 GenDP 仅为 35%，相对提升高达 **18.75%**（Table 2）。值得注意的是，PADP 在“打开瓶子”任务的原始设置中成功率为 80%，即便在物体扰动（60%）、空间扰动（70%）和环境扰动（60%）等泛化测试条件下，仍大幅领先 GenDP（Table 3）。这表明 PA3FF 学到的部件级特征——例如把手、旋钮等——能够在物体外观、位姿和环境发生显著变化时保持语义一致性，从而为策略提供鲁棒的感知锚点。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_qXfRXfAHOK/figures/006_Table_2.jpg]]
*Table 2: Real-world task success rates across different methods (train/test). Each task is evaluated with 10 trials under randomized initial conditions. The best-performing results are highlighted in bold*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_qXfRXfAHOK/figures/007_Table_3.jpg]]
*Table 3: Generalization evaluation of the Open Bottle task (10 trials)*

### 基础特征对比：3D 原生优于 2D 提升

为了剥离 PA3FF 相对于现有基础特征的增益，作者在 PartInstruct 上进行了系统的特征替换实验（Table 4）。将 PA3FF 替换为 2D 基础模型（如 CLIP、DINOv2）或 3D 基础模型（如 ULIP-2、OpenShape）提升到 3D 的特征，性能均出现明显下降。这一对比揭示了一个关键瓶颈：**2D 基础视觉特征在提升到 3D 空间时面临多视图不一致与空间分辨率不足的问题，难以捕捉细小的功能部件**。相比之下，PA3FF 作为 3D 原生表示，直接在点云上生成稠密、连续的部件感知场，从根本上规避了 2D-to-3D 提升带来的信息损失。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_qXfRXfAHOK/figures/010_Table_4.jpg]]
*Table 4: Comparisons with Other Foundation Features*

### 消融实验：对比学习是性能核心

Table 6 的消融实验揭示了各模块的贡献权重。最关键的发现是：**移除对比学习带来的部件感知细化（即同时去掉几何损失和语义损失），成功率从 62% 骤降至 46%**。进一步分解来看，语义损失比几何损失更为重要——单独移除语义损失后性能降至 46%，而单独移除几何损失后为 54%。这说明将点特征与部件名语义向量对齐（语义损失）对于建立功能部件的语义认知至关重要。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_qXfRXfAHOK/figures/014_Table_6.jpg]]
*Table 6: Ablation study results showing the impact of different components on task performance across diverse tasks*

相比之下，对 Sonata 骨干的架构修改（移除下采样层并堆叠额外 Transformer 块）贡献相对温和：还原该修改后成功率从 62% 小幅降至 58%。而直接将未修改的 Sonata 与 DP3 组合（Sonata + DP3）仅获得 39%，与 DP3 基线（37%）相差无几，证明**单纯替换 3D 骨干而不引入部件感知细化，收益极为有限**。这进一步坐实了对比学习框架才是性能提升的核心因果杠杆。

### 部件分割：感知能力的独立验证

在 **PartNetE** 数据集上的部件分割实验（Table 5）独立验证了 PA3FF 的部件感知质量。PA3FF 在多个物体类别上取得了最高的类别平均精度（mAP50），表明其学到的特征不仅服务于操控策略，本身即具备良好的部件判别能力。Figure 4 的特征场可视化进一步从定性角度展示了 PA3FF 相较于其他基础特征的优越性：PA3FF 能够清晰地区分功能部件（如把手与壶身），而其他方法往往将整个物体编码为模糊的全局特征。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_qXfRXfAHOK/figures/005_Figure_4.jpg]]
*Figure 4: The feature field visualizations of PA3FF and other foundation features*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_qXfRXfAHOK/figures/013_Table_5.jpg]]
*Table 5: Segmentation Results on the PartNetE Dataset. Category mAP50s (%) are shown for different object categories. Higher values indicate better performance*

### 样本效率与跨任务泛化

在 **RLBench** 的 6 项任务上，PADP（约 64.5% 平均成功率）同样大幅超越 GenDP（约 48.3%）（Table 8），表明该方法在非铰接物体的常规操作任务上也具有迁移能力。此外，在仅使用 5 个演示的极低数据条件下，PADP 仍能保持可观的性能，展现出优异的样本效率。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_qXfRXfAHOK/figures/028_Table_8.jpg]]
*Table 8: Simulated results with different numbers of demonstrations. Here we use the two seen objects in the training phase to test the success rate, and conduct five trials for each object with random initialization in each task*

### 失败模式与局限性

尽管 PADP 在铰接物体操控上表现突出，其核心依赖的 Sonata 骨干主要针对刚体几何设计。论文明确指出，该方法**对于复杂变形物体（如绳子、布料）的处理能力有限**，因为此类物体的结构变化超出了当前 3D 特征骨干的建模范围。此外，PA3FF 的训练依赖于大规模部件标注数据，其在完全未见物体类别上的零样本泛化能力仍需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_qXfRXfAHOK/figures/008_Figure_5.jpg]]
*Figure 5: Generalization test set of the Open Bottle task*

## 方法谱系与知识库定位

### 核心思路的继承与突破

PA3FF/PADP 的核心突破在于将**部件感知（part-aware）**引入可泛化的铰接物体操控，其方法谱系可沿两条主线追溯：3D视觉表征学习与基于扩散的模仿学习。

**3D表征学习主线**：早期工作主要依赖2D基础模型（CLIP、DINOv2）提升至3D空间，但面临多视图不一致、空间分辨率低、难以捕捉细小功能部件等瓶颈。PA3FF的独特之处在于直接使用3D原生骨干**Sonata**（基于Point Transformer V3的预训练模型），并对其进行关键修改——移除大部分下采样层、堆叠额外Transformer块以保留细节并增强特征抽象能力。这一设计使得特征场能够编码稠密、连续、功能部件敏感的信息，而非简单的语义类别标签。

**扩散策略主线**：在模仿学习领域，**Diffusion Policy (DP)** (Chi et al., 2023) 建立了图像-动作的扩散生成范式；**DP3** (Ze et al., 2024) 将其扩展到点云输入；**GenDP** (Wang et al., 2024c) 进一步引入密集语义场。PADP在这一谱系中的定位是：将部件感知的3D特征场作为扩散策略的观测输入，使动作生成能够显式地依赖于功能部件的位置与归属关系，而非仅依赖全局几何或语义信息。

### 关键设计选择的因果机制

PA3FF的性能优势可归因于两个相互耦合的设计选择：

1. **对比学习双损失框架**：几何损失（$\mathcal{L}_{Geo}$）拉近同一部件点的特征、推远不同部件点的特征，提供部件内一致性与部件间区别性；语义损失（$\mathcal{L}_{Sem}$）通过InfoNCE将点特征与SigLIP编码的部件名语义向量对齐，引入跨物体的功能语义一致性。消融实验表明，语义损失比几何损失更为关键——移除语义损失导致成功率从62%降至46%，而移除几何损失降至54%（Table 6）。

2. **3D原生骨干的适配修改**：直接组合未修改的Sonata与DP3仅获得39%成功率，接近DP3基线的37%（Table 6），说明单纯替换骨干获益有限。移除额外Transformer块的修改（保留下采样层）仅小幅下降至58%，表明架构修改虽有贡献，但对比学习细化才是性能提升的主要驱动力。

### 适用边界与局限

**有效范围**：
- **物体类型**：刚体和铰接物体（如抽屉、门、瓶子、微波炉），这些物体具有明确的功能部件结构（把手、旋钮、盖子等）。
- **任务类型**：基于部件交互的操作任务（打开、关闭、旋转等），在仿真（PartInstruct）和真实世界（8项任务）均验证有效。
- **泛化能力**：对未见物体、空间位置变化、环境干扰均表现出鲁棒性（Table 3: Open Bottle任务在空间干扰下仍保持70%完成率）。

**已知局限**：
- **变形物体处理能力有限**：论文明确指出，对于复杂变形物体（如绳子、布料），基础模型Sonata难以应对复杂的结构变化，PA3FF在此类场景的适用性尚未验证。
- **部件标注依赖**：PA3FF的训练需要大规模部件标注数据集（如PartNetE），标注成本和对新类别的覆盖是潜在瓶颈。

### 开放问题与未来方向

1. **变形物体扩展**：如何将部件感知的3D特征场扩展到高度可变形的物体？这可能需要引入时序信息或物理先验来建模非刚性变换下的部件对应关系。

2. **语言与任务规划的融合**：当前PA3FF将部件名编码为语义向量，未来能否通过融合更高级的语言指令或任务规划来进一步增强跨任务的泛化能力？

3. **数据效率与标注需求**：PA3FF的训练是否可以通过自监督或弱监督方式减少对精细部件标注的依赖，以覆盖更多物体类别和更广泛的操控场景？

4. **与基础模型的深度整合**：PA3FF目前独立于2D基础模型，未来是否可以通过与CLIP、DINOv2等2D模型的跨模态对齐，进一步提升对未见物体的零样本泛化能力？

## 原文 PDF

![[paperPDFs/ICLR_2026/PA3FF_Learning_Part_Aware_Dense_3D_Feature_Field_For_Generalizable_Articulated_O_591e4e474026.pdf]]