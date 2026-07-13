---
title: StickMotion Generating 3D Human Motions by Drawing a Stickman
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/StickMotion_Generating_3D_Human_Motions_by_Drawing_a_Stickman.pdf
project_link: null
code_link: null
aliases:
- SG3HMBDS
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 引入用户绘制的火柴人条件，结合多条件融合模块（MCM）和动态监督，使用户能够用简笔画和简短文本快速指导生成精细的可控动作。
primary_logic: 火柴人草图作为一种直观的空间约束，可以补充文本语义，通过多条件融合和动态位置调整，在保持自然度的同时显著降低用户交互成本，提高生成精度。
claims:
- 使用火柴人可节省用户约51.5%的交互时间（与详细文本描述相比）
- Multi-Condition Module (MCM) 相比传统自注意力融合方案将FID从0.38降至0.14
- 新提出的StiSim指标显示火柴人相似度达到41.5%（HumanML3D），证明模型有效捕捉了火柴人约束
- "HumanML3D (Ablation: MCM vs Self-Attention) 上 FID = 0.14"
---

# StickMotion Generating 3D Human Motions by Drawing a Stickman

> [!tip] 核心洞察
> 火柴人草图作为一种直观的空间约束，可以补充文本语义，通过多条件融合和动态位置调整，在保持自然度的同时显著降低用户交互成本，提高生成精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | StickMotion：通过绘制火柴人生成三维人体动作 |
| 英文题名 | StickMotion Generating 3D Human Motions by Drawing a Stickman |
| 会议/期刊 | CVPR 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | StickMotion |
| Dataset | HumanML3D, User Study |

> [!tip] 效果简介
> - HumanML3D (Ablation: MCM vs Self-Attention) 上，FID 0.14 vs 0.38 (-0.24)。
> - User Study (Table 6) 上，Total Time (min) 16.4 vs 33.8 (ReMoDiffuse) (-51.5%)；User Score 8.5 vs 7.3 (ReMoDiffuse) (+1.2)。

## 概要

### 问题瓶颈

文本到动作生成任务中，用户面临一个根本性矛盾：简单的文本描述无法充分捕捉复杂动作的细节想象，而撰写详细描述又极为耗时且难以精确表达空间姿态。这一瓶颈导致现有方法难以高效生成与用户意图高度一致的动作。

### 核心方案

StickMotion 引入**用户绘制的火柴人草图**作为额外的空间约束条件，使用户能够用简笔画配合简短文本快速指导生成精细的可控动作。其核心机制包括三个关键设计：

1. **多条件融合模块 (Multi-Condition Module, MCM)**：通过批次分段和专门的 Condition Fusion 模块，高效融合文本与火柴人两种模态的条件信息，替代传统自注意力融合方案，在降低计算量的同时显著提升生成质量。

2. **动态监督策略**：允许网络在指定位置附近动态调整火柴人的帧索引，而非将其刚性固定在预设帧，从而在施加空间约束的同时保持动作的自然流畅性。

3. **灵活的条件组合**：支持开始、中间、结束三处火柴人与文本描述的任意组合输入，用户可根据需求灵活控制动作细节。

### 方法定位

StickMotion 属于**多条件扩散生成模型**，以 DDPM 为基础框架，在反向去噪过程中同时接受文本编码（CLIP ViT-B/32）和火柴人编码（预训练 Transformer）的条件引导。与 ReMoDiffuse（Zhang et al., ICCV 2023）、MotionDiffuse（Zhang et al., arXiv 2022）、MDM（Tevet et al., 2022）等纯文本驱动方法相比，StickMotion 通过引入视觉草图模态，在交互效率和生成精度之间取得了新的平衡。

### 核心结果

- **交互效率**：用户研究中，使用火柴人配合简短描述的总交互时间为 16.4 分钟，相比 ReMoDiffuse 使用详细文本描述的 33.8 分钟，节省约 **51.5%** 的时间（Table 6）。

- **生成质量**：消融实验表明，MCM 相比传统自注意力融合方案将 FID 从 0.38 降至 **0.14**（Table 3，HumanML3D 数据集）。

- **约束有效性**：新提出的 StiSim 指标显示，火柴人相似度在 HumanML3D 上达到 **41.5%**，在 KIT-ML 上达到 42.6%，验证了模型有效捕捉火柴人空间约束的能力。

- **用户满意度**：用户评分从 ReMoDiffuse 的 7.3 分提升至 **8.5 分**（Table 6）。

三维人体动作生成是计算机视觉与图形学领域的核心问题之一，其应用涵盖动画制作、虚拟现实、游戏开发与人机交互等场景。近年来，基于扩散模型的文本到动作生成方法取得了显著进展，如 **MDM**（Tevet et al., 2022）、**MotionDiffuse**（Zhang et al., arXiv 2022）和 **ReMoDiffuse**（Zhang et al., ICCV 2023）等，这些方法能够根据自然语言描述生成多样化的人体动作序列。

然而，现有方法面临一个根本性瓶颈：**文本描述与用户意图之间的语义鸿沟**。简单的文本描述（如"一个人向前走"）难以捕捉用户对复杂动作细节的想象，例如特定关节角度、肢体空间位置或动作节奏变化。而详细的文本描述虽然能提供更多约束，却耗时且难以精确表达空间关系——用户往往"心里清楚但说不出来"。这一矛盾导致现有文本到动作方法无法高效地生成与用户意图高度一致的动作。

StickMotion 的核心洞察在于：**火柴人草图作为一种直观的空间约束，可以高效补充文本语义的不足**。绘制一个简单的火柴人仅需几秒钟，却能直接传达肢体的空间位置、朝向和姿态信息，这些正是纯文本难以精确描述的内容。通过将用户绘制的火柴人与简短文本描述相结合，StickMotion 在保持动作自然度的同时，显著降低了用户的交互成本——实验表明，使用火柴人相比详细文本描述可节省约 **51.5%** 的交互时间（Table 6），同时获得更高的用户满意度评分（8.5 vs 7.3）。

这一动机驱动了 StickMotion 的三个关键设计：**多条件融合模块（MCM）** 用于高效整合火柴人与文本两种异构条件；**动态监督策略** 使网络能在指定位置附近灵活调整火柴人的精确帧索引，避免刚性约束导致动作不自然；以及**火柴人生成算法（SGA）** 用于自动生成多样化风格的火柴人训练数据。这些设计共同指向一个目标：让用户以最低的交互成本，获得最符合想象的动作生成结果。

## 核心方法与创新机理

StickMotion 的核心创新在于将**用户绘制的火柴人草图**作为一种全新的空间条件引入文本到动作生成任务，从根本上改变了人机交互的范式。与现有纯文本驱动方法（如 **ReMoDiffuse**，Zhang et al., ICCV 2023；**MDM**，Tevet et al., 2022）要求用户撰写冗长详细的自然语言描述不同，StickMotion 允许用户通过简单勾勒火柴人的肢体姿态，直观地表达对动作序列中关键帧的精确空间约束。这种多模态条件输入机制直接回应了文本到动作生成领域的核心瓶颈：简单文本描述无法充分捕捉用户对复杂动作细节的想象，而详细描述又耗时且难以表达。

围绕这一范式转变，StickMotion 在三个关键维度上实现了相对于 baseline 的实质性改进：

### 1. 条件输入：从纯文本到“文本+火柴人”的多模态融合

现有方法仅依赖文本描述作为唯一的条件信号，用户若想控制动作细节，必须撰写高度详细的描述（如“先抬起右手至肩高，掌心向下，然后缓慢下蹲……”），这不仅耗时，而且难以精确传达空间姿态信息。StickMotion 将输入空间扩展为**四种可任意组合的条件**：开始位置火柴人、中间位置火柴人、结束位置火柴人以及文本描述。用户可以根据需要提供其中的任意组合，模型自动处理缺失条件。用户研究（Table 6）表明，这一设计使用户交互总时间从 ReMoDiffuse 的 33.8 分钟降至 16.4 分钟，**节省约 51.5% 的时间**，同时用户评分从 7.3 提升至 8.5。

### 2. 多条件融合：Multi-Condition Module (MCM) 替代传统自注意力融合

处理四种条件的任意组合是一个非平凡的技术挑战。传统方案通常采用自注意力模块并对输入进行掩码操作来实现条件组合，这不仅引入额外计算量，而且在条件缺失时性能下降明显。StickMotion 提出了 **Multi-Condition Module (MCM)**，其核心设计包括两个关键组件：

- **Condition Fusion 模块**：沿批次维度将数据划分为四个段，分别对应四种条件组合（文本+火柴人、仅火柴人、仅文本、无条件），实现高效的条件注入，避免了对缺失条件进行掩码操作的冗余计算。
- **Latent Encoder 模块**：对融合后的特征进行再编码，进一步提炼多模态信息。

消融实验（Table 3）提供了决定性证据：联合使用 Condition Fusion 和 Latent Encoder 的 MCM 方案将 FID 从自注意力方案的 0.38 **降至 0.14**，降幅达 63.2%。单独使用任一模块均无法达到此效果，验证了二者协同设计的必要性。

### 3. 火柴人位置监督：从刚性指定到动态调整

在序列生成中，火柴人应放置在哪些帧是一个关键问题。若刚性指定火柴人必须出现在固定的帧索引（如第 0 帧、第 N/2 帧、第 N 帧），会导致生成的动作僵硬不自然，因为真实动作的节奏和相位存在固有变化。StickMotion 引入了**动态监督策略**：网络在推理时输出一个帧索引分数（index score），在指定位置（开始/中间/结束）附近动态选择与火柴人姿态最匹配的帧。训练时，通过专门的索引损失函数进行监督：

$$\mathcal{L}_{\mathrm{index}} = M \cdot \sum_{l=0}^{L} \mathrm{softmax}(\hat{I}_l) \cdot ||\hat{x}_l(\mathrm{stick},*) - x_i||^2$$

该损失通过 softmax 加权机制，使网络预测的最高分数帧尽可能接近真实火柴人姿态，同时允许一定范围的动态偏移。总损失由三处火柴人位置的索引损失和动作重建损失共同构成：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{index}}^{\mathrm{start}} + \mathcal{L}_{\mathrm{index}}^{\mathrm{middle}} + \mathcal{L}_{\mathrm{index}}^{\mathrm{end}} + \mathcal{L}_{\mathrm{motion}}$$

这一设计使模型能够在保持动作自然度的前提下，灵活地将火柴人约束嵌入到最合适的时间位置。

### 创新总结

StickMotion 的三个核心创新形成了一个完整的因果链条：**火柴人草图**作为直观的空间约束降低了用户交互成本；**MCM 多条件融合模块**高效处理条件组合并显著提升生成质量；**动态监督策略**确保火柴人约束在时间维度上被灵活且自然地满足。新提出的 StiSim 指标（火柴人相似度）在 HumanML3D 上达到 41.5%，为量化评估火柴人约束的满足程度提供了工具。这一系列创新使 StickMotion 在保持与纯文本方法可比的自动指标（HumanML3D 上 FID 0.107）的同时，大幅提升了用户对生成结果的控制精度和交互效率。

StickMotion 的整体框架以条件扩散模型为核心，将用户交互从纯文本描述扩展为“火柴人草图 + 简短文本”的多模态输入，从而在降低交互成本的同时提升动作细节的可控性。框架由两条对称的流程构成：**训练时的前向扩散与条件预测**，以及**推理时的反向去噪与条件混合**。

### 输入模态与编码

系统接受四类可任意组合的输入：位于动作序列**开始、中间、结束**位置的火柴人草图，以及一段简短的文本描述（Section 3）。三类输入分别通过独立的编码器映射到统一的高维空间：

- **Stickman Encoder**：采用预训练的 6 层标准 Transformer 编码器，将火柴人草图编码为特征嵌入。实验表明，**预训练并冻结该编码器的权重**对 StickMotion 的整体性能有显著提升（Section 3.3）。
- **Text Encoder**：使用冻结的 CLIP ViT-B/32 模型将文本描述编码为语义向量。
- **Motion Encoder**：通过一个简单的线性层将带噪声的运动序列映射到高维空间，作为扩散过程的输入。

三种编码后的特征分别形如 $[L^m, E]$、$[L^s, E]$、$[L^t, E]$，随后送入核心的条件融合模块。

### 扩散过程

StickMotion 遵循标准的去噪扩散概率模型（DDPM）范式。前向过程逐步向真实运动 $x_0$ 添加高斯噪声，单步转移核为：

$$q(\mathbf{x}_t | \mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{\alpha_t} \mathbf{x}_{t-1}, (1-\alpha_t) \mathbf{I})$$

联合分布分解为 $\prod_{t=1}^T q(\mathbf{x}_t | \mathbf{x}_{t-1})$。训练时，网络以文本和火柴人为条件，预测所添加的噪声 $\epsilon_\theta$，损失函数为：

$$\mathbb{E}_{\epsilon_t, t, x_0}[ ||\epsilon_t - \epsilon_\theta(\mathbf{x}_t, t, L, C(stick), C(text))||^2 ]$$

推理时，反向过程从纯噪声出发，逐步去噪生成运动序列。为灵活控制火柴人约束与文本语义的混合程度，StickMotion 在推理阶段采用**条件混合策略**，将不同条件状态下的预测噪声加权组合：

$$\hat{\epsilon}_\theta = w_1 \cdot \epsilon_\theta(stick, text) + w_2 \cdot \epsilon_\theta(stick,) + w_3 \cdot \epsilon_\theta(text,) + w_4 \cdot \epsilon_\theta(,)$$

这一机制使用户可以在推理时调节生成结果更偏向火柴人形状还是文本语义。

### 多条件融合模块

框架的核心是 **Multi-Condition Module（MCM）**。与传统的自注意力融合方案（通过掩码实现条件组合，引入额外计算量）不同，MCM 内部包含两个关键子模块：

- **Feat Decoder**：负责将条件信息注入运动特征。
- **Latent Encoder**：对融合后的特征进行再编码，增强条件交互。

MCM 通过**沿批次维度将数据划分为四个分段**，分别对应四种条件组合（文本+火柴人、仅火柴人、仅文本、无条件），从而高效并行处理多条件输入。消融实验表明，联合使用 Condition Fusion 和 Latent Encoder 的 MCM，相比传统自注意力融合方案将 FID 从 **0.38 降至 0.14**（Table 3），同时降低了计算复杂度。

### 动态监督与输出

StickMotion 的输出包含两部分：**预测噪声**（用于去噪生成运动）和**索引分数**（用于确定火柴人在序列中的精确位置）。传统方法将火柴人刚性绑定在固定帧，容易导致动作不自然。StickMotion 引入**动态监督策略**：网络在用户指定的“开始/中间/结束”位置附近动态调整火柴人的最佳帧索引，并通过专门的索引损失进行监督：

$$\mathcal{L}_{\mathrm{index}} = M \cdot \sum_{l=0}^{L} \mathrm{softmax}(\hat{I}_l) \cdot ||\hat{x}_l(\mathrm{stick},*) - x_i||^2$$

该损失使网络预测的最高分数帧尽可能接近真实火柴人姿态。总损失由三处火柴人位置的索引损失与运动重建损失共同构成：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{index}}^{\mathrm{start}} + \mathcal{L}_{\mathrm{index}}^{\mathrm{middle}} + \mathcal{L}_{\mathrm{index}}^{\mathrm{end}} + \mathcal{L}_{\mathrm{motion}}$$

其中运动损失 $\mathcal{L}_{\mathrm{motion}} = \sum_{l=0}^{L} ||\hat{x}_l(*,*) - x_l||^2$ 驱动基础运动生成。

### 数据流总览

整个数据流可概括为：**用户输入（火柴人 + 文本）→ 冻结编码器提取特征 → MCM 多条件融合 → 扩散模型预测噪声与索引分数 → 动态监督优化位置 → 反向去噪生成最终运动序列**。训练时使用 Stickman Generation Algorithm（SGA）从真实运动数据自动生成多样风格的火柴人作为监督信号，推理时则直接接收用户绘制的草图。

![[assets/figures/papers/paper_list_l1866_StickMotion_Generating_3D_Human_Motions_by_Drawing_a_Stickman/figures/003_Figure_3.jpg]]
*Figure 3: The StickMotion framework consists of the diffusion process on the left and the network structure on the right. 1) The diffusion process is divided into two components: the forward process and the reverse process. In the forward process, original motions are artificially augmented with Gaussian noise and fed into StickMotion to facilitate its prediction of the added noise based on text from the dataset and stickman generated by actual motion through the Stickman Generation Algorithm (SGA). In the reverse process, the user’s textual descriptions and stickman figures are inputted into StickMotion, enabling the gradual generation of motion sequences with its predicted noise. 2) Regarding the s...*

### 扩散过程基础

StickMotion 基于条件扩散模型构建，其核心数学框架如下。

**前向过程**将原始运动序列 $\mathbf{x}_0$ 逐步添加高斯噪声，形成马尔可夫链：

$$q(\mathbf{x}_{1:T} | \mathbf{x}_0) = \prod_{t=1}^T q(\mathbf{x}_t | \mathbf{x}_{t-1})$$

单步转移核为：

$$q(\mathbf{x}_t | \mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{\alpha_t} \mathbf{x}_{t-1}, (1-\alpha_t) \mathbf{I})$$

其中 $\alpha_t \in [0.9800, 0.9999]$，总噪声步数 $T = 1000$。

**训练损失**以文本描述 $C(text)$ 和火柴人草图 $C(stick)$ 为联合条件，监督噪声预测：

$$\mathbb{E}_{\epsilon_t, t, x_0}[ ||\epsilon_t - \epsilon_\theta(\mathbf{x}_t, t, L, C(stick), C(text))||^2 ]$$

其中 $\epsilon_t$ 为真实添加的噪声，$\epsilon_\theta$ 为网络预测噪声，$L$ 为序列长度。

**反向过程**从纯噪声逐步去噪生成运动序列：

$$x_{t-1} = \frac{1}{\sqrt{\alpha_t}} (x_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon_\theta) + \sigma_t$$

### 条件混合策略

推理阶段采用无分类器引导，通过混合不同条件状态下的预测噪声，实现对火柴人约束与文本语义之间权衡的精细控制：

$$\hat{\epsilon}_\theta = w_1 \cdot \epsilon_\theta(stick, text) + w_2 \cdot \epsilon_\theta(stick,) + w_3 \cdot \epsilon_\theta(text,) + w_4 \cdot \epsilon_\theta(,)$$

其中 $w_1 = \tau w$，$w_4 = 1 - 2 \cdot w$，权重 $w$ 控制条件采样强度与输出分布。该策略允许用户调节生成结果偏向火柴人空间约束或文本语义描述的程度。

### 多条件模块（MCM）

MCM 是 StickMotion 的核心条件融合单元。与传统的自注意力融合方案（将所有条件拼接后统一处理，FID 为 0.38）不同，MCM 内部包含两个关键子模块：

- **Condition Fusion（条件融合）**：沿批次维度将数据划分为四个分段，分别对应四种条件组合（文本+火柴人、仅火柴人、仅文本、无条件），实现高效的条件注入，显著降低计算量。
- **Latent Encoder（隐空间编码器）**：对融合后的特征进行再编码，增强条件信息的表达力。

联合使用 Condition Fusion 和 Latent Encoder 将 FID 从 0.38 降至 0.14（Table 3），验证了该设计的有效性。

### 动态监督与损失函数

为解决火柴人刚性指定在固定帧导致动作不自然的问题，StickMotion 引入**动态监督策略**。网络输出一个额外的帧索引分数（Index Score），在指定位置附近动态调整火柴人对应的帧索引。

**总损失**由三处火柴人位置的索引损失和运动重建损失构成：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{index}}^{\mathrm{start}} + \mathcal{L}_{\mathrm{index}}^{\mathrm{middle}} + \mathcal{L}_{\mathrm{index}}^{\mathrm{end}} + \mathcal{L}_{\mathrm{motion}}$$

**索引损失**通过 softmax 加权姿态误差，使网络预测的最高分数帧逼近真实火柴人姿态：

$$\mathcal{L}_{\mathrm{index}} = M \cdot \sum_{l=0}^{L} \mathrm{softmax}(\hat{I}_l) \cdot ||\hat{x}_l(\mathrm{stick},*) - x_i||^2$$

其中 $\hat{I}_l$ 为帧 $l$ 的预测索引分数，$x_i$ 为真实火柴人姿态，$M$ 为缩放系数。

**运动损失**驱动所有条件组合下的基础运动生成：

$$\mathcal{L}_{\mathrm{motion}} = \sum_{l=0}^{L} ||\hat{x}_l(*,*) - x_l||^2$$

### 编码器设计

StickMotion 包含三个输入编码器：

- **Stickman Encoder**：6 层标准 Transformer 编码器，将火柴人草图编码为特征嵌入。实验表明，预训练并冻结该编码器可显著提升整体性能。
- **Text Encoder**：冻结的 CLIP ViT-B/32，将文本描述编码为特征向量。
- **Motion Encoder**：简单线性层，将噪声运动序列映射到高维空间。

三类输入分别编码为形状 $[L^m, E]$、$[L^s, E]$、$[L^t, E]$ 的特征向量，供后续 MCM 处理。

## 实验与关键发现

### 主实验结果

StickMotion 在 HumanML3D 和 KIT-ML 两个标准基准上进行了定量评估，采用 R Precision、FID、MM Dist、Diversity 和 Multimodality 五项指标。Table 1 和 Table 2 分别展示了两个数据集上的完整对比结果，最佳结果以红色标注，次优以蓝色标注。在 HumanML3D 上，StickMotion 取得了 Top1 R Precision 0.518、FID 0.107、MM Dist 2.953、Diversity 9.239、MultiModality 2.256；在 KIT-ML 上，对应指标为 Top1 R Precision 0.430、FID 0.141、MM Dist 2.763、Diversity 10.94、MultiModality 1.457。

![[assets/figures/papers/paper_list_l1866_StickMotion_Generating_3D_Human_Motions_by_Drawing_a_Stickman/figures/004_Table_1.jpg]]
*Table 1: Comparison on the HumanML3D test set. We mark the best result as red and the second best one as blue*

![[assets/figures/papers/paper_list_l1866_StickMotion_Generating_3D_Human_Motions_by_Drawing_a_Stickman/figures/005_Table_2.jpg]]
*Table 2: Comparison on the KIT-ML test set*

需要指出的是，论文仅提供了定性排名而未给出所有对比方法的具体数值，因此无法在此报告中直接计算所有指标的 delta 值。此外，对比基线未涵盖同期最强方法（如 MotionGPT），公平性可能受限。

### 用户研究：效率与质量

用户研究（Table 6）是验证 StickMotion 实际可用性的关键证据。与基于详细文本描述的 **ReMoDiffuse**（Zhang et al., ICCV 2023）相比，StickMotion 将用户交互总时间从 33.8 分钟降至 16.4 分钟，节省约 51.5%。同时，用户评分从 7.3 提升至 8.5（满分 10），表明火柴人草图不仅提高了效率，也提升了用户对生成结果的满意度。这一结果直接支撑了论文的核心主张：火柴人作为一种直观的空间约束，能以更低交互成本实现更精确的动作生成。

### 多条件融合模块（MCM）消融

MCM 是 StickMotion 的核心技术创新，其消融实验（Table 3）揭示了关键设计选择的有效性：

![[assets/figures/papers/paper_list_l1866_StickMotion_Generating_3D_Human_Motions_by_Drawing_a_Stickman/figures/006_Table_3.jpg]]
*Table 3: Ablation study on Condition Fusion and Latent Encoder for the training / forward process*

- **传统自注意力融合**作为基线方案，FID 为 0.38。
- **单独引入 Condition Fusion 模块**将 FID 降至 0.19。
- **单独引入 Latent Encoder** 将 FID 降至 0.17。
- **联合使用 Condition Fusion 和 Latent Encoder（即完整 MCM）** 将 FID 进一步降至 0.14。

这一消融链表明，MCM 的两个子模块存在互补效应：Condition Fusion 负责高效注入多模态条件，Latent Encoder 则对融合后的特征进行再编码以提取更优表示。相比自注意力方案，MCM 在降低计算量的同时实现了显著的性能提升（FID 降低 0.24）。

### 推理阶段条件混合策略

推理过程中，StickMotion 通过混合四种条件状态（文本+火柴人、仅火柴人、仅文本、无条件）的预测噪声来控制生成偏向，其权重由参数 $w$ 调节（见公式 $w_1 = \tau w, w_4 = 1 - 2 \cdot w$）。Table 4 的消融表明，初始扩散步骤的条件混合对最终生成质量至关重要——在早期步骤中同时注入文本和火柴人条件，能有效引导生成方向；若仅在后期引入条件，则难以纠正已形成的运动轨迹。

![[assets/figures/papers/paper_list_l1866_StickMotion_Generating_3D_Human_Motions_by_Drawing_a_Stickman/figures/007_Table_4.jpg]]
*Table 4: Ablation study on the condition mixture for the inference / reverse process*

### 条件组合的影响

Table 5 分析了不同火柴人位置（开始、中间、结束）与文本描述的组合效果。使用新提出的 StiSim 指标（StickmanSimilarity）评估火柴人约束的满足程度，结果显示：

- 提供更多火柴人条件（如同时提供开始、中间、结束三个位置的火柴人）可逐步提高 StiSim 值，在 HumanML3D 上达到 41.5%，KIT-ML 上达到 42.6%。
- 仅提供文本描述时 StiSim 最低，验证了火柴人草图对精确空间控制的必要性。
- 开始位置的火柴人对整体序列的约束作用最为显著，这与运动生成的因果结构一致——初始姿态决定了后续运动的演化方向。

### 预训练火柴人编码器的作用

实验发现，预训练并冻结火柴人编码器（6 层标准 Transformer）对整体性能有显著提升。若编码器参与训练或不进行预训练，模型在 FID 和 StiSim 上均出现退化。这表明，在训练数据通过 Stickman Generation Algorithm（SGA）自动生成的火柴人上预训练编码器，能使其获得稳定的姿态特征提取能力，避免与扩散模型的联合训练带来的优化冲突。

### 新指标 StickmanSimilarity（StiSim）

StiSim 定义为 $1 - (\text{StickmanDistance} / \text{MeanDistance})$，用于量化生成动作中特定帧的姿态与输入火柴人之间的相似度。该指标填补了现有文本到动作评估体系缺乏空间约束度量的问题。在 HumanML3D 上达到 41.5%，KIT-ML 上达到 42.6%，表明模型能有效捕捉火柴人约束。但该指标与人类主观评判的一致性尚未经过大规模用户研究验证，需进一步确认。

### 公平性与局限性

1. **基线覆盖不全**：仅与部分文本到动作方法比较（如 ReMoDiffuse、MotionDiffuse、MDM），未涵盖 MotionGPT 等同期方法。
2. **数据集局限**：仅在 KIT-ML 和 HumanML3D 上测试，未在舞蹈、手势交互等更广泛动作类型上验证泛化能力。
3. **用户研究样本量**：论文未明确说明用户研究的参与者数量，统计显著性未经验证。
4. **火柴人位置受限**：当前仅支持开始、中间、结束三个粗略位置，无法精确指定任意帧。
5. **文本与火柴人冲突**：当文本描述与火柴人形状产生语义冲突时，模型的鲁棒性未深入探讨。

![[assets/figures/papers/paper_list_l1866_StickMotion_Generating_3D_Human_Motions_by_Drawing_a_Stickman/figures/009_Figure_4.jpg]]
*Figure 4: Visualization with various input combinations*

## 定位与知识库关联

### 任务定位与核心突破

StickMotion 面向**文本到三维人体动作生成**任务，其核心切入点是解决该领域长期存在的“表达瓶颈”：简单的文本描述（如“一个人走路”）无法捕捉用户对动作细节的想象，而撰写足以控制动作细节的详细描述又极其耗时。现有条件生成方法的交互效率与生成精度之间存在根本性张力。

StickMotion 的解决方案是引入**火柴人草图**作为第二种条件模态，与简短文本描述协同工作。这一设计的因果机制在于：火柴人提供直观的**空间约束**（关键帧的人体姿态），文本提供**语义上下文**（动作类别与风格），二者通过多条件融合模块（MCM）与动态监督策略实现互补。从交互成本看，用户研究（Table 6）表明，绘制火柴人配合简短描述的总耗时（16.4分钟）相比撰写详细文本描述（33.8分钟）节省约51.5%，同时用户评分从7.3提升至8.5。

### 与基线方法的关系

StickMotion 建立在扩散式动作生成的工作线上，其直接可比的基线包括：

- **MDM**（Tevet et al., 2022）：基于扩散模型的人体动作生成框架，使用纯文本条件。StickMotion 沿用了其扩散范式，但在条件输入和融合机制上做了根本性扩展。
- **MotionDiffuse**（Zhang et al., arXiv 2022）：文本驱动的扩散动作生成模型。StickMotion 与其共享扩散建模的基本思路，但 MotionDiffuse 仅支持文本条件。
- **ReMoDiffuse**（Zhang et al., ICCV 2023）：检索增强的文本到动作扩散模型，是 StickMotion 在用户研究中直接对比的基线。ReMoDiffuse 通过检索相似动作来增强文本条件，但仍依赖用户提供足够详细的描述才能生成符合意图的动作。

StickMotion 相对于上述基线的**关键改动槽位**有三处：

1. **条件输入扩展**：从纯文本扩展为“文本 + 火柴人”双模态，支持开始/中间/结束三个位置的火柴人与文本的任意组合输入，使用户能以极低成本指定关键帧姿态。
2. **多条件融合机制重构**：基线方法通常采用自注意力模块并通过输入掩码实现条件组合，这会引入额外计算量。StickMotion 提出 Multi-Condition Module (MCM)，通过批次维度划分和专门的 Condition Fusion 模块高效处理四种条件组合（纯文本、纯火柴人、两者皆有、两者皆无），消融实验（Table 3）显示 FID 从自注意力方案的 0.38 降至 0.14。
3. **火柴人位置动态监督**：基线方法缺乏对条件时间位置的灵活处理。StickMotion 引入动态监督策略，允许网络在指定位置附近动态调整火柴人对应的帧索引，并通过专门的索引损失（Index Loss）进行监督，避免刚性指定导致的动作不自然。

### 适用边界

StickMotion 的适用场景和约束可从以下几个维度界定：

- **输入模态要求**：需要用户具备绘制火柴人的能力或设备。论文未探讨绘图质量对生成效果的系统性影响，但可以合理推断，严重偏离人体结构的火柴人可能导致生成失败或动作畸变。
- **时间控制粒度**：当前仅支持将火柴人放置在开始、中间、结束三个粗略位置，无法精确指定任意帧的姿态。对于需要密集关键帧控制的场景（如复杂舞蹈编排），该方法的能力受限。
- **数据分布范围**：训练和评估仅在 KIT-ML 和 HumanML3D 两个数据集上进行，这两个数据集以日常动作和简单运动为主。模型在舞蹈、体育动作、手势交互等分布外动作类型上的泛化能力未经检验。
- **多人物与场景交互**：模型设计为单人生成，未涉及多人交互或与场景物体的物理交互，这些是动作生成领域的重要扩展方向。
- **语义冲突处理**：当文本描述与火柴人形状产生语义冲突时（例如文本说“举手”但火柴人画的是“叉腰”），模型的鲁棒性未得到系统分析。推理阶段的条件混合权重（Equation 4）提供了控制文本与火柴人相对影响力的机制，但极端冲突下的行为仍是开放的。

### 局限与开放问题

基于论文自身的讨论和实验证据的缺口，可识别以下局限与开放问题：

**已确认的局限**：
- 火柴人位置仅支持三个粗略锚点，无法实现任意帧的精确时间控制。
- 需要用户手动绘制火柴人，对无绘图设备或绘画能力较弱的用户不友好。
- 仅在两个标准数据集上验证，泛化至其他动作域的能力未知。
- 模型参数规模（43M/62M）和推理速度未与最轻量的文本到动作方法充分对比。

**开放研究问题**：
- **精细时间控制**：如何使模型支持任意数量、任意位置的火柴人条件，实现帧级别的精确姿态控制？
- **绘图鲁棒性量化**：不同绘图风格、精度和歧义性对生成质量的影响能否系统量化？是否存在一个“最低绘图质量阈值”？
- **多智能体扩展**：能否将火柴人条件扩展到多人物交互或场景感知的动作生成？这需要解决多人空间关系建模和碰撞避免等问题。
- **自动火柴人提取**：是否可以通过自监督学习从视频中自动提取火柴人表示，以减少人工绘制需求？这将显著降低使用门槛。
- **评估指标验证**：新提出的 StiSim 指标（火柴人相似度）与人类主观评判的一致性，需要在更大规模用户研究中验证其可靠性。
- **局部姿态精细控制**：如何在保持整体动作自然性的同时，进一步增强对特定肢体部位（如手腕角度、脚掌方向）的精确控制？当前的火柴人表示可能过于粗糙，无法捕捉这些细节。

## 原文 PDF

![[paperPDFs/CVPR_2025/StickMotion_Generating_3D_Human_Motions_by_Drawing_a_Stickman.pdf]]
