---
title: "Sculpt4D: Generating 4D Shapes via Sparse-Attention Diffusion Transformers"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Sculpt4D_Generating_4D_Shapes_via_Sparse_Attention_Diffusion_Transformers.pdf
project_link: "https://visual-ai.github.io/sculpt4d"
code_link: "https://github.com/mit-han-lab/Block-Sparse-Attention"
aliases:
- Sculpt4D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 块稀疏注意力机制（Block Sparse Attention），通过将首帧作为全局锚点并施加随时间衰减的稀疏掩码，在大幅降低计算量的同时捕捉运动动态。
primary_logic: 在注意力矩阵中引入对角稀疏模式，使步长随帧间距离增大，强制保留空间对应关系，同时以首帧锚点防止语义漂移，从而在计算效率与生成质量之间取得最佳平衡。
claims:
- Sculpt4D 在所有几何指标上显著优于现有方法（如 L4GM、V2M4、DreamMesh4D 等）。
- 稀疏注意力在 Chamfer 距离、IoU 和 F-Score 上与全注意力高度接近（Chamfer 0.0972 vs 0.0958），但计算量仅为全注意力的 43.8%（186.3 PFLOPs vs 425.7 PFLOPs）。
- 移除首帧锚点导致所有几何指标退化，证实全局锚点对维持几何保真度的必要性。
- 延迟指数衰减策略（Delayed Exponential schedule）在几何质量与效率之间取得最佳权衡，优于固定步长、激进衰减和保守衰减。
---

# Sculpt4D: Generating 4D Shapes via Sparse-Attention Diffusion Transformers

> [!tip] 核心洞察
> 在注意力矩阵中引入对角稀疏模式，使步长随帧间距离增大，强制保留空间对应关系，同时以首帧锚点防止语义漂移，从而在计算效率与生成质量之间取得最佳平衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | Sculpt4D：基于稀疏注意力扩散 Transformer 的 4D 形状生成 |
| 英文题名 | Sculpt4D: Generating 4D Shapes via Sparse-Attention Diffusion Transformers |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.21592) · [Project](https://visual-ai.github.io/sculpt4d) · [Code](https://github.com/mit-han-lab/Block-Sparse-Attention) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Sculpt4D |
| Dataset | Video Quality Assessment, Computational Efficiency |

> [!tip] 效果简介
> - Video Quality Assessment 上，LPIPS↓ 0.098 (Ours) vs 0.131 (Hunyuan3D, best baseline) (-0.033)；CLIP↑ 0.916 (Ours) vs 0.835 (DreamMesh4D, best baseline) (+0.081)；FVD↓ 483.1 (Ours) vs 914.9 (DreamMesh4D, best baseline) (-431.8)。
> - Computational Efficiency (16 frames) 上，PFLOPs 186.3 (Sparse attention) vs 425.7 (Full attention) (-239.4 (43.8% of baseline))。

## 概要

**问题瓶颈：** 从视频或多视图输入生成时间连贯的 4D 网格序列，面临全时空自注意力 $O((T \times P)^2)$ 的二次计算复杂度瓶颈。当帧数 $T$ 和空间令牌数 $P$ 增大时，计算开销急剧膨胀，迫使现有方法在时间一致性与对象身份保持之间做出妥协。

**核心方法：** Sculpt4D 提出一种原生 4D 生成框架，将高效时间建模无缝注入预训练的 3D Diffusion Transformer（Hunyuan3D 2.1）。其关键创新是**块稀疏注意力机制**（Block Sparse Attention）：将首帧作为全局锚点防止语义漂移，同时施加随时间距离衰减的稀疏掩码捕捉运动动态。这一设计在注意力矩阵中形成对角稀疏模式，步长随帧间距离增大，强制保留空间对应关系，从而在计算效率与生成质量之间取得最优平衡。

**主要结果：**
- 与全注意力相比，稀疏注意力将计算量从 425.7 PFLOPs 降至 186.3 PFLOPs（仅占 43.8%），而几何指标高度接近（Chamfer 距离 0.0972 vs 0.0958）。
- 在视频质量评估中，Sculpt4D 显著优于所有基线方法：LPIPS↓ 0.098（最佳基线 Hunyuan3D 为 0.131），CLIP↑ 0.916（最佳基线 DreamMesh4D 为 0.835），FVD↓ 483.1（最佳基线 DreamMesh4D 为 914.9）。
- 消融实验证实，移除首帧锚点导致所有几何指标退化，而提出的延迟指数衰减策略在几何质量与效率之间达到最优权衡。

### 4D 内容生成的现实需求

从单目视频中重建动态三维世界是计算机视觉与图形学的长期目标。近年来，3D 生成模型取得了显著进展，能够从文本或图像生成高质量的静态网格。然而，现实世界中的对象是动态的——它们移动、变形、改变拓扑结构。将这种时间维度引入生成过程，即 **4D 生成**（三维空间 + 一维时间），成为通向沉浸式数字内容创作的关键一步。

Sculpt4D 的目标是：给定一段输入视频，直接生成时间连贯的 4D 网格序列，同时处理复杂的非刚性运动和拓扑变化（如 Figure 1 所示）。

### 现有方法的瓶颈：全时空注意力的二次复杂度

将 3D 生成模型扩展到 4D 面临一个核心计算瓶颈。最自然的做法是在预训练的 3D Diffusion Transformer（DiT）中插入时间注意力层，使所有时空令牌之间进行全连接交互。然而，这种全时空自注意力的计算复杂度为：

$$\mathcal{O}((T \times P)^2)$$

其中 $T$ 为帧数，$P$ 为每帧的空间令牌数。随着帧数增加，计算开销呈二次增长，使得长序列 4D 生成在实践上难以承受。

### 现有 4D 生成方法的局限性

在 Sculpt4D 之前，已有若干方法尝试解决 4D 生成问题，但各自存在明显短板：

- **逐帧独立生成**（如直接使用 **Hunyuan3D** 逐帧生成静态网格）：完全缺乏时间一致性约束，导致帧间几何抖动和对象身份漂移。
- **基于 Score Distillation Sampling (SDS) 的方法**（如 **DreamMesh4D**）：通过蒸馏预训练的视频扩散模型注入运动先验，但优化过程缓慢，且难以保证精确的几何保真度。
- **后处理优化方法**（如 **V2M4**）：先生成各帧网格，再通过后处理步骤优化顺序一致性，本质上仍是两阶段方案，无法端到端学习时空耦合表示。
- **前馈式快速方法**（如 **L4GM**）：基于图像表示进行快速生成，但在几何精度上有所妥协。
- **变形场预测方法**（如 **GVFD**）：从规范形状预测变形场，对复杂拓扑变化的建模能力有限。

这些方法的共同缺口在于：**缺乏一种既高效又能同时维持时间一致性与对象身份稳定性的原生 4D 生成架构**。全注意力虽能建模完整的时空依赖，但计算代价过高；而简化时间建模则会导致运动质量或几何保真度的损失。

### 本文动机与核心思路

Sculpt4D 的提出正是为了填补这一缺口。其核心动机是：**能否设计一种注意力机制，在显著降低计算量的同时，仍然捕捉到足够的运动动态并保持对象身份一致性？**

为此，Sculpt4D 将高效的时空建模无缝集成到预训练的 3D Diffusion Transformer（**Hunyuan3D 2.1**）中，核心创新是一种 **块稀疏注意力机制（Block Sparse Attention）**。该机制通过两个关键设计实现效率与质量的平衡：

1. **首帧全局锚点**：所有后续帧始终可以关注第一帧，以此作为对象身份的稳定参照，防止语义漂移。
2. **时间衰减稀疏掩码**：帧间注意力步长随时间距离增大而增加，强制保留空间对应关系，同时大幅减少冗余计算。

通过这种设计，Sculpt4D 将计算量降低约 56%，同时在几何质量上接近全注意力水平，实现了 4D 生成中效率与保真度的最佳权衡。

## 核心方法与创新机理

Sculpt4D 的核心创新并非简单的模块堆叠，而是在充分继承 3D 生成先验的前提下，通过**三个相互耦合的 changed slots** 系统性地解决了 4D 生成中“计算可行性—时间一致性—身份稳定性”的不可能三角。

### 瓶颈洞察：全时空注意力的二次复杂度陷阱

现有 4D 生成方法面临一个根本性的计算瓶颈：若将 $T$ 帧、每帧 $P$ 个空间令牌直接送入全时空自注意力，计算复杂度为 $\mathcal{O}((T \times P)^2)$。这意味着随着帧数增加，计算开销呈二次增长，迫使现有方法要么牺牲时间分辨率，要么采用逐帧独立生成后拼接的后处理策略（如 **V2M4**、**Hunyuan3D** 的逐帧生成模式），导致时间一致性和对象身份稳定性难以同时保证。

Sculpt4D 的因果调节旋钮在于：**注意力矩阵的结构化稀疏性**。论文发现，并非所有时空令牌对之间的交互都具有同等重要性——帧间运动信息主要蕴含在空间对应关系附近，而对象身份的全局一致性可以通过少数锚点维持。这一洞察直接催生了三个 changed slots 的设计。

### Changed Slot 1：从“无时间建模”到“分解式时空 4D-DiT 块”

**Baseline 状态**：Hunyuan3D 等 3D 生成模型仅包含空间自注意力和交叉注意力，逐帧独立生成静态网格，缺乏显式的时间建模能力（`Section 3.2`）。

**Proposed 方案**：在预训练的 3D DiT 块中插入专门的时间自注意力模块，形成“空间注意力 → 时间注意力 → 交叉注意力”的分解式架构。空间注意力负责单帧内的几何结构建模，时间注意力负责跨帧运动动态捕捉，两者解耦后分别优化，避免时空耦合带来的冗余计算。

**设计意图**：这种分解式设计使得模型可以充分利用 Hunyuan3D 2.1 的预训练权重作为强先验，仅在时间维度上进行增量学习，大幅降低了 4D 生成的训练成本（约 3 天，8 张 96GB GPU）。

### Changed Slot 2：从“逐帧独立噪声”到“序列共享噪声重参数化”

**Baseline 状态**：VAE 重参数化中，每帧独立采样高斯噪声 $\epsilon_t$，引入帧间随机性，破坏了潜在空间的时间连续性（`Section 3.1`）。

**Proposed 方案**：整个序列共享同一噪声向量 $\epsilon_{\mathrm{seq}}$，重参数化公式变为 $z_t = \mu_t + \sigma_t \cdot \epsilon_{\mathrm{seq}}$。这一看似简单的修改具有深层含义：它强制 VAE 编码器将所有帧的时间变化信息压缩到均值 $\mu_t$ 中，而共享的随机分量则保证了潜在序列的平滑性。

**证据强度**：该设计的必要性在消融实验中通过对比实验间接验证——移除时间一致性约束（如无锚点变体）会导致几何指标全面退化（Table A1），而共享噪声正是维持时间一致性的第一道防线。

### Changed Slot 3：从“全注意力”到“锚点引导的块稀疏注意力”——核心创新

这是 Sculpt4D 最关键的 changed slot，也是计算效率与生成质量平衡的核心机制。

**Baseline 状态**：全时空自注意力计算所有令牌对之间的交互，复杂度为 $\mathcal{O}((T \times P)^2)$。

**Proposed 方案**：块稀疏注意力（Block Sparse Attention）由两个互补的掩码组成：

1. **首帧全局锚点**：所有帧的所有令牌块都可以无条件地关注第一帧的对应块。这借鉴了 Radial Attention 的 “attention sink” 思想，将首帧作为对象身份的全局参考系，防止长序列生成中的语义漂移。消融实验证实，移除该锚点（Model A）导致 Chamfer 距离从 0.0972 升至 0.0986，IoU 从 0.3451 降至 0.3442（Table A1），证明锚点对维持几何保真度具有统计显著但幅度较小的贡献。

2. **时间衰减稀疏掩码**：帧间注意力步长 $s(d)$ 随时间距离 $d$ 增大而增加，遵循 $s(d) = \mathcal{S}[\min(d, \operatorname{len}(\mathcal{S})-1)]$ 的查表映射。注意力掩码定义为：
   $$M_{i \cdot N_B + u, \, j \cdot N_B + v} = \begin{cases} 1, & \text{if } j=0 \\ 1, & \text{if } (u \bmod s_d) = (v \bmod s_d) \\ 0, & \text{otherwise} \end{cases}$$
   其物理意义是：查询块 $u$ 与键块 $v$ 在距离为 $d$ 的帧间允许注意力当且仅当 $u \bmod s = v \bmod s$，这确保了空间对应关系在稀疏模式下的保持。步长随帧间距离增大意味着：近邻帧保留细粒度交互（小步长），远距离帧仅保留粗粒度对应（大步长），符合运动信息随时间的衰减特性。

**步长策略的消融洞察**：Table A1 系统比较了五种步长策略，揭示了精度—效率权衡的连续谱：
- **固定步长**（Model B, stride=4）：性能最差（Chamfer 0.1124, IoU 0.3298），表明均匀稀疏无法捕捉局部运动的细粒度细节。
- **激进衰减**（Model C）：计算量最低（145.0 PFLOPs），但几何精度受损（Chamfer 0.0991）。
- **保守衰减**（Model D）：几何质量接近全注意力，但计算量高达 233.6 PFLOPs，效率优势有限。
- **延迟指数衰减**（Model F, 即 Sculpt4D 最终方案）：在几何质量（IoU 0.3451, F-Score 0.3383）与效率（186.3 PFLOPs，仅为全注意力的 43.8%）之间达到最优平衡。

### 创新的协同效应

三个 changed slots 并非孤立运作。共享噪声重参数化提供了平滑的潜在空间基础，分解式 4D-DiT 块为稀疏注意力提供了结构化的操作舞台，而块稀疏注意力则在前两者的基础上实现了计算效率的质变。这种“先验继承—结构解耦—计算稀疏”的三层递进设计，使得 Sculpt4D 在仅需 3 天训练的条件下，在 Chamfer 距离（0.0972 vs 全注意力的 0.0958）上与全注意力高度接近，同时将计算量削减 56.2%。

Sculpt4D 的整体框架围绕一个核心设计展开：将高效的时间建模注入预训练的 3D 扩散 Transformer，从而将静态生成能力扩展为端到端的 4D 生成能力。该框架以图像序列为条件输入，通过四个级联模块完成从像素到动态网格的转换，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2590_https_arxiv_org_abs_2604_21592/figures/002_Figure_2.jpg]]
*Figure 2: An overview of our 4D generation framework. Conditioned on an image sequence, we use Consistent Surface Sampling (Sec. 3.1) to acquire both sharp edge points and random surface points, which a vector set VAE [13, 58] encodes into shape latents. These latents are processed by 4D DiT blocks, which use cross-attention for image conditioning and our novel Block Sparse Attention (Sec. 3.3). This sparse attention, guided by a composite mask (Temporal Sparse and First-Frame Anchor), efficiently captures motion while ensuring identity consistency. Finally, a decoder produces the final mesh sequence from the denoised latents*

**输入与表面采样。** 给定一段图像序列，框架首先执行一致性表面采样（Consistent Surface Sampling），从变形网格序列中提取时间对齐的点云。采样策略兼顾两类点：锐边点用于保留几何细节，随机表面点用于覆盖整体形状。这一步为后续的隐变量编码提供了时间一致的几何基础。

**VAE 隐变量编码。** 采样得到的点序列随后送入 Vector Set VAE（基于 Hunyuan3D-v2.1），被压缩为紧凑的隐变量序列。框架在此引入了一个关键设计：**共享噪声重参数化**。传统做法是对每一帧独立采样高斯噪声，这会在隐空间中引入随机的时间扰动。Sculpt4D 改为让整个序列共享同一个噪声向量 $\epsilon_{\mathrm{seq}}$，即 $z_t = \mu_t + \sigma_t \cdot \epsilon_{\mathrm{seq}}$。这一改动消除了逐帧噪声的随机性差异，从编码阶段就强制执行时间连续性。

**4D DiT 块。** 编码后的隐变量序列进入核心生成模块——4D DiT 块。每个 4D DiT 块由三个注意力子模块串联而成：
1. **空间自注意力**：对每一帧独立操作，建模单帧内部的几何结构。
2. **交叉注意力**：以图像序列为条件，将视觉信息注入隐变量。
3. **时间自注意力**：跨帧操作，建模帧间的运动动态。该模块采用 RoPE（旋转位置编码）提供时间位置信息。

这三个子模块形成“空间-条件-时间”的分解式建模结构，将原本耦合的时空建模解耦为可分别优化的组件。

**块稀疏注意力机制。** 时间自注意力模块的核心是块稀疏注意力（Block Sparse Attention），它通过复合掩码 $M$ 定义注意力模式：
$$M_{i \cdot N_B + u, \, j \cdot N_B + v} = \begin{cases} 1, & \text{if } j=0 \\ 1, & \text{if } (u \bmod s_d) = (v \bmod s_d) \\ 0, & \text{otherwise} \end{cases}$$

该掩码包含两个互补部分：
- **首帧全局锚点**：所有帧的令牌块均可关注首帧（$j=0$），首帧充当“注意力汇”，为整个序列提供稳定的身份参照，防止语义漂移。
- **时间衰减稀疏模式**：对于非首帧的帧间注意力，根据时间距离 $d$ 从预定义步长表 $\mathcal{S}$ 中查找步长 $s_d = \mathcal{S}[\min(d, \text{len}(\mathcal{S})-1)]$，仅当查询块 $u$ 与键块 $v$ 满足 $u \bmod s_d = v \bmod s_d$ 时才允许注意力。这在对角线附近形成稀疏模式，且步长随帧间距离增大而增大，强制保留空间对应关系的同时大幅降低计算量。

该稀疏注意力机制通过 Block Sparse Attention 库高效实现，将全时空自注意力的 $\mathcal{O}((T \times P)^2)$ 二次复杂度压缩至可控范围。

**SDF 解码与网格重建。** 去噪后的隐变量序列最终由 SDF 解码器逐帧重建为水密网格，得到完整的 4D 网格序列。

**训练配置。** 模型在包含约 13k 个 4D 动画对象的数据集上训练，训练配置为 8 张 96GB GPU、约 3 天、24K 次迭代、批次大小 32（每序列 16 帧）。损失计算使用通过最远点采样（FPS）选取的 4,096 个查询点。

### 4D 潜在编码：共享噪声重参数化

Sculpt4D 的时间一致性从 VAE 潜在编码阶段就开始构建。给定一个变形网格序列，模型通过 Consistent Surface Sampling 从每一帧采样时间对齐的点云（包含锐边点和随机表面点），随后利用预训练的 Vector Set VAE（基于 Hunyuan3D-v2.1）将其编码为紧凑的隐变量序列。

常规 VAE 对每一帧独立采样高斯噪声会引入随机的时间抖动。为解决这一问题，Sculpt4D 采用**共享噪声重参数化**策略——整个序列共享同一个噪声向量 $\epsilon_{\mathrm{seq}}$，所有帧的隐变量由统一的随机源驱动：

$$z_t = \mu_t + \sigma_t \cdot \epsilon_{\mathrm{seq}}$$

其中 $z_t$ 为第 $t$ 帧的隐变量，$\mu_t$ 和 $\sigma_t$ 分别为 VAE 编码器输出的均值和标准差。这一设计消除了逐帧独立采样带来的时间随机性，使得潜在空间中的帧间变化完全由内容差异驱动，而非噪声扰动，从而为后续的时间注意力模块提供了稳定的初始条件。

### 4D-DiT 块：分解式时空建模

Sculpt4D 的核心架构创新在于将时间建模无缝注入预训练的 3D Diffusion Transformer（Hunyuan3D 2.1），形成**分解式的 4D-DiT 块**。每个 4D-DiT 块包含三个顺序执行的注意力模块：

1. **空间自注意力**：在每帧内部独立运行，建模单帧的几何结构；
2. **空间交叉注意力**：以输入图像序列为条件，将视觉信息注入每帧的隐变量；
3. **时间自注意力**：跨帧运行，捕捉运动动态和时间一致性。

这种“先空间、后时间”的分解设计将原本需要联合处理的时空令牌序列拆分为两个阶段，避免了全时空自注意力的二次复杂度瓶颈。时间自注意力模块采用 Rotary Position Embedding（RoPE）为每帧提供时间位置编码，使模型能够感知帧间顺序关系。

### 块稀疏注意力：核心效率机制

全时空自注意力的计算复杂度为 $\mathcal{O}((T \times P)^2)$，其中 $T$ 为帧数，$P$ 为每帧的空间令牌数。当 $T$ 增长时，计算开销急剧膨胀。Sculpt4D 的**块稀疏注意力（Block Sparse Attention）**通过两个关键设计在大幅降低计算量的同时保持生成质量：

#### 首帧全局锚点

所有后续帧的令牌块均可无条件关注首帧（$j=0$）的对应空间位置。这一设计借鉴了 Radial Attention 中的“attention sink”概念——首帧作为全局锚点，为整个序列提供稳定的身份参照，防止长序列生成中的语义漂移。

#### 时间衰减稀疏掩码

对于非首帧之间的注意力，Sculpt4D 根据帧间时间距离 $d$ 动态调整注意力密度。具体而言，预定义一个步长表 $\mathcal{S}$，通过距离-步长映射函数查找当前帧对的注意力步长：

$$s(d) = \mathcal{S}[\min(d, \operatorname{len}(\mathcal{S})-1)]$$

帧间距离越大，步长越大，注意力越稀疏。最终形成的块级注意力掩码定义为：

$$M_{i \cdot N_B + u, \, j \cdot N_B + v} = \begin{cases} 1, & \text{if } j=0 \\ 1, & \text{if } (u \bmod s_d) = (v \bmod s_d) \\ 0, & \text{otherwise} \end{cases}$$

其中 $N_B$ 为块大小，$u$ 和 $v$ 分别为查询帧 $i$ 和键帧 $j$ 内的块索引，$s_d$ 为帧间距离 $d = |i-j|$ 对应的步长。

该掩码的核心约束条件为 $u \bmod s = v \bmod s$，确保查询块 $u$ 仅关注键帧中与其空间位置对应的块 $v$。由于 $u \bmod s = u \bmod s$ 恒成立，每个令牌块总能关注到远距离帧中相同空间位置的对应块，从而在稀疏化注意力的同时严格保持空间对应关系。

#### 延迟指数衰减策略

步长表 $\mathcal{S}$ 的具体设计对几何质量与计算效率的权衡至关重要。Sculpt4D 提出**延迟指数衰减（Delayed Exponential schedule）**策略：近距离帧保持密集注意力以捕捉局部运动细节，随距离增大逐步稀疏化以控制计算量。消融实验表明，该策略在 IoU（0.3451）、F-Score（0.3383）和计算开销（186.3 PFLOPs）之间达到最优平衡——相比之下，固定步长策略因无法捕捉局部运动细节而几何质量最差，激进衰减策略虽将计算量降至 145.0 PFLOPs 但精度受损，保守衰减策略几何质量接近全注意力但计算开销高达 233.6 PFLOPs。

整个稀疏注意力机制通过 Block Sparse Attention 库高效实现，在 16 帧设定下仅消耗全注意力 43.8% 的计算量（186.3 vs 425.7 PFLOPs），而 Chamfer 距离几乎无损（0.0972 vs 0.0958）。

## 实验与关键发现

### 主要定量结果

Sculpt4D 在几何精度与视频感知质量两个维度上均显著超越现有方法。Table 1 报告了与五类代表性基线的几何指标对比：逐帧生成的 **Hunyuan3D**、基于 Score Distillation Sampling 的 **DreamMesh4D**、后处理优化的 **V2M4**、前馈式 **L4GM** 以及变形场预测方法 **GVFD**。Sculpt4D 在所有几何指标上取得最优结果，Chamfer 距离降至 0.1052，IoU 达到 0.3381（Table 1）。

![[assets/figures/papers/paper_list_l2590_https_arxiv_org_abs_2604_21592/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison*

视频质量评估进一步验证了时间一致性的优势。如 Table A3 所示，Sculpt4D 在 LPIPS 上达到 0.098，较最佳基线 Hunyuan3D（0.131）降低 0.033；CLIP 分数达到 0.916，超越 DreamMesh4D（0.835）达 0.081；FVD 降至 483.1，仅为 DreamMesh4D（914.9）的 52.8%。这些结果表明，稀疏注意力机制在维持对象身份稳定性的同时，有效捕捉了帧间运动动态。

![[assets/figures/papers/paper_list_l2590_https_arxiv_org_abs_2604_21592/figures/012_Table.jpg]]
*Table: A3. Results comparison*

### 消融实验：稀疏注意力设计的有效性

消融研究系统解耦了块稀疏注意力的两个核心设计——首帧锚点与时间衰减稀疏掩码——对几何质量与计算效率的影响（Table 2, Table A1）。

![[assets/figures/papers/paper_list_l2590_https_arxiv_org_abs_2604_21592/figures/007_Table_2.jpg]]
*Table 2: Ablation study*

![[assets/figures/papers/paper_list_l2590_https_arxiv_org_abs_2604_21592/figures/009_Table.jpg]]
*Table: A1. Ablation study*

**首帧锚点的必要性。** 移除首帧全局锚点（Model A）导致所有几何指标退化：Chamfer 距离从 0.0972 升至 0.0986，IoU 从 0.3451 降至 0.3442，F-Score 从 0.3383 降至 0.3375。这表明全局锚点对于在整个序列中维持语义锚定、防止几何漂移具有不可替代的作用。

**稀疏步长策略的权衡。** 固定步长策略（Model B, stride=4）在所有变体中表现最差（Chamfer 0.1124, IoU 0.3298, F-Score 0.3306），证明均匀稀疏无法捕捉局部运动细节。激进衰减策略（Model C）将计算量压缩至 145.0 PFLOPs，但几何精度受损（Chamfer 0.0991, IoU 0.3420）；保守衰减策略（Model D）几何质量接近全注意力，但计算开销高达 233.6 PFLOPs。所提出的延迟指数衰减策略（Model F）在几何质量（IoU 0.3451, F-Score 0.3383）与计算效率（186.3 PFLOPs）之间达到最优平衡。

**稀疏注意力与全注意力的对比。** 核心消融（Table 2）显示，稀疏注意力在 Chamfer 距离（0.0972 vs 0.0958）、IoU 和 F-Score 上与全注意力高度接近，但计算量仅为全注意力的 43.8%（186.3 PFLOPs vs 425.7 PFLOPs），实现了 56.2% 的计算削减。

### 计算扩展性分析

稀疏注意力的计算优势随帧数增加而愈发显著。Table A2 展示了不同帧数下的 PFLOPs 对比：在 16 帧配置下，核心时间注意力层的 FLOPs 比率（稀疏/全注意力）远低于整个网络比率，表明稀疏掩码主要降低了时间建模的计算瓶颈。Figure A1 进一步展示了该比率随帧数变化的扩展曲线，验证了稀疏注意力在长序列场景下的可扩展性。

Table A4 测试了模型在超出训练长度序列上的几何质量，结果表明 Sculpt4D 在扩展帧数下仍能保持稳定的几何保真度，未出现明显的质量衰减。

### 定性结果

Figure 4 展示了六组多样化的 4D 网格序列生成结果，每组包含六个时间帧的多视角渲染。Sculpt4D 能够处理复杂运动（如人物舞蹈、动物奔跑）和拓扑变化（如物体变形），同时保持时间一致的几何结构。Figure 5 展示了模型在野外数据上的泛化能力，Figure 6 进一步呈现了带纹理的网格序列生成效果，验证了框架对纹理信息的兼容性。

![[assets/figures/papers/paper_list_l2590_https_arxiv_org_abs_2604_21592/figures/006_Figure_5.jpg]]
*Figure 5: Mesh sequences generated from in the wild data*

### 实验设置与公平性说明

所有方法在同一 13k 4D 对象数据集上训练与评估，采用一致的几何度量（Chamfer Distance, IoU, F-Score）和视频质量度量（LPIPS, CLIP, FVD）。计算效率以 PyTorch 框架下的理论 FLOPs（PFLOPs）进行比较，硬件环境统一。Sculpt4D 训练约 3 天，使用 8 张 96GB GPU，batch size 为 32（每序列 16 帧），损失计算采用最远点采样选取 4,096 个查询点。

## 定位与知识库关联

### 问题定位：4D 生成的计算瓶颈

4D 形状生成的核心挑战在于同时维持时间一致性与对象身份稳定性，而全时空自注意力的二次计算复杂度 $\mathcal{O}((T \times P)^2)$（$T$ 帧、每帧 $P$ 个空间令牌）使得长序列生成的计算开销过大，现有方法难以在两者之间取得平衡。Sculpt4D 通过引入块稀疏注意力机制，在大幅降低计算量的同时捕捉运动动态，填补了效率与质量之间的鸿沟。

### 与现有方法的关系

**逐帧生成方法（无时间建模）**：Hunyuan3D 等 3D 生成模型直接逐帧生成静态网格，完全缺乏时间一致性约束，导致帧间几何抖动和身份漂移。Sculpt4D 在其预训练权重基础上注入时间自注意力模块，将独立帧生成升级为端到端 4D 学习，从根本上解决了这一问题。

**基于优化的 4D 方法**：DreamMesh4D 采用 Score Distillation Sampling (SDS) 进行 4D 生成，V2M4 则在逐帧生成网格后通过后处理优化顺序一致性。这些方法要么依赖耗时的迭代优化，要么将时间一致性作为后处理步骤，而非原生建模。Sculpt4D 的前馈式架构在推理效率上具有本质优势——Table A3 显示，其 FVD 为 483.1，远低于 DreamMesh4D 的 914.9。

**前馈式 4D 方法**：L4GM 基于图像表示实现快速 4D 生成，但其图像域操作限制了网格几何精度。GVFD 从规范形状预测变形场，依赖显式的变形假设，对拓扑变化（如物体分离、合并）的建模能力受限。Sculpt4D 直接在网格几何空间操作，可处理复杂拓扑变化（Figure 1 中展示的物体分离场景）。

**同期端到端方法**：ShapeGen4D 同样在 3D DiT 中注入时空注意力层进行端到端 4D 学习，但未采用稀疏注意力机制，其计算效率与长序列扩展性可能受限。Sculpt4D 的块稀疏注意力在此形成差异化优势——Table A2 显示，稀疏注意力仅需全注意力 43.8% 的计算量（186.3 vs 425.7 PFLOPs），而几何质量几乎无损失（Chamfer 0.0972 vs 0.0958）。

### 技术继承与创新

Sculpt4D 的核心设计借鉴了两项关键思想：**Radial Attention** 中的“注意力沉没”（attention sink）概念被改造为首帧全局锚点，确保对象身份在时间维度上的稳定性；**FramePack** 的时间衰减计算密度策略被泛化为距离相关的步长调度，使注意力密度随帧间距离增大而稀疏化。两者的结合——全局锚点防止语义漂移，对角稀疏模式保留空间对应关系——构成了 Sculpt4D 在计算效率与生成质量之间取得最佳平衡的因果机制。

在架构层面，Sculpt4D 继承了 Hunyuan3D-v2.1 的 Vector Set VAE 和 SDF Decoder，将 3D 生成能力直接迁移至 4D 域。其关键创新在于 4D-DiT 块的设计：空间自注意力/交叉注意力独立处理单帧内容，新增的时间自注意力模块采用块稀疏注意力进行帧间建模，RoPE 提供时间位置编码。这种分解式设计使模型既保留了预训练 3D 生成器的几何先验，又获得了高效的时间建模能力。

### 适用边界与局限

**训练数据依赖**：模型在约 13k 个 4D 动画对象上训练，数据规模相对有限。Figure 5 展示了在野外数据上的泛化能力，但缺乏系统性的分布外评估，对极端运动或罕见拓扑的鲁棒性需要手动验证。

**帧数扩展性**：Table A4 测试了超出训练长度（16 帧）的序列生成，但缺乏对更长序列（如 64 帧以上）的几何质量退化分析。Figure A1 的 FLOPs 比例曲线显示稀疏注意力的效率优势随帧数增加而扩大，但几何质量在超长序列上的保持情况未充分验证。

**纹理生成**：Figure 6 展示了带纹理的网格序列结果，但论文主要聚焦几何质量评估，纹理一致性的定量指标（如纹理 FVD 或时间纹理一致性度量）缺失，该维度需要进一步研究。

**与物理仿真的关系**：Sculpt4D 从视频输入学习运动模式，属于数据驱动的运动生成，不包含物理约束。对于需要物理真实性（如碰撞、重力）的场景，其生成结果可能违反物理规律，需结合物理仿真器进行后处理或约束。

### 开放问题

1. **稀疏模式的动态适应性**：当前步长调度 $s(d)$ 是预定义的静态函数，能否根据运动复杂度自适应调整稀疏模式，在简单运动场景下进一步降低计算量，在复杂运动场景下自动增加注意力密度？

2. **多对象场景扩展**：首帧锚点机制假设场景中存在单一主要对象，对于多对象交互场景（如双手操作、群体运动），单一全局锚点可能不足以维持所有对象的身份一致性，需要探索多锚点或对象级稀疏注意力。

3. **生成控制与编辑**：Sculpt4D 目前从视频输入生成完整 4D 序列，缺乏对特定帧或特定区域的精细控制能力。如何将稀疏注意力机制与可控生成（如运动编辑、局部变形）结合，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Sculpt4D_Generating_4D_Shapes_via_Sparse_Attention_Diffusion_Transformers.pdf]]
