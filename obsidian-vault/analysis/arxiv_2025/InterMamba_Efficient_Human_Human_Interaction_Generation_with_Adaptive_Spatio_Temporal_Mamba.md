---
title: "InterMamba: Efficient Human-Human Interaction Generation with Adaptive Spatio-Temporal Mamba"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/InterMamba_Efficient_Human_Human_Interaction_Generation_with_Adaptive_Spatio_Temporal_Mamba.pdf
aliases:
- InterMamba
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将Transformer骨干替换为选择性状态空间模型（Mamba），并设计解耦的自适应时空SSM分支与交叉交互建模，以线性复杂度捕获长程依赖。
primary_logic: 将运动序列建模分解为并行空间SSM（帧内关节结构）和时间SSM（帧间运动连续性），通过可学习权重自适应融合；同时利用交叉Mamba和局部交互聚合模块显式建模双人互动，在提升生成质量的同时大幅降低参数量和推理时间。
claims:
- Transformer架构的平方复杂度限制了长序列处理的可扩展性和效率。
- InterMamba仅使用66M参数（InterGen的36%），平均推理时间0.57秒（InterGen的46%），同时提高了生成精度。
- 自适应时空Mamba框架（ASTM）通过两个并行SSM分支与自适应机制有效整合时空特征。
- 消融实验表明，Self-ASTM + Cross-ASTM + LIIA组合取得最高R-Precision（0.705）和竞争力的FID（5.945）。
---

# InterMamba: Efficient Human-Human Interaction Generation with Adaptive Spatio-Temporal Mamba

> [!tip] 核心洞察
> 将运动序列建模分解为并行空间SSM（帧内关节结构）和时间SSM（帧间运动连续性），通过可学习权重自适应融合；同时利用交叉Mamba和局部交互聚合模块显式建模双人互动，在提升生成质量的同时大幅降低参数量和推理时间。

| 字段 | 内容 |
|------|------|
| 中文题名 | InterMamba：自适应时空Mamba的高效人际交互生成 |
| 英文题名 | InterMamba: Efficient Human-Human Interaction Generation with Adaptive Spatio-Temporal Mamba |
| 会议/期刊 | arXiv 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | InterMamba |
| Dataset | InterHuman, InterX, Efficiency |

> [!tip] 效果简介
> - InterHuman 上，R-Precision Top-1 ↑ 0.475 vs 0.371 (InterGen) (+0.104)；FID ↓ 5.945 vs 5.918 (InterGen) (+0.027 (worse))；MMDist ↓ 3.785 vs 5.108 (InterGen) (-1.323)。
> - InterX 上，R-Precision Top-1 ↑ 0.4573 vs 0.4403 (in2IN) (+0.017)；FID ↓ 0.517 vs 0.239 (in2IN) (+0.278 (worse))；Diversity → 9.194 vs 8.450 (InterGen) (+0.744 (closer to real))。
> - Efficiency 上，Inference Time (s) ↓ 0.567 (InterMamba) vs 1.233 (InterGen) (-0.666 (2.2× faster))。

## 概述

人际交互运动生成旨在根据文本描述合成逼真的双人互动动作，在虚拟现实、游戏、影视制作等领域具有广泛应用前景。然而，现有主流方法——基于 Transformer 的自注意力扩散模型——在处理长序列时，其平方复杂度严重制约了可扩展性与推理效率，难以满足实时交互式应用的需求。

针对这一瓶颈，本文提出 **InterMamba**，首次将选择性状态空间模型（Mamba）引入人际交互运动生成范式。核心思路是将 Transformer 骨干替换为线性复杂度的 Mamba，并设计解耦的自适应时空 SSM 分支与交叉交互建模机制，以捕获长程依赖。

具体而言，InterMamba 包含三个关键模块：**自适应时空 Mamba（ASTM）** 将运动序列建模分解为并行的空间 SSM（帧内关节结构）和时间 SSM（帧间运动连续性），通过可学习权重动态融合；**局部交互信息聚合（LIIA）** 利用自适应层归一化和卷积提取双人局部交互特征；**交叉自适应时空 Mamba（Cross-ASTM）** 基于混合状态空间模型显式建模角色间的交互关系。

实验表明，InterMamba 在 InterHuman 和 InterX 数据集上取得了领先性能。与代表性基线 **InterGen**（Liang et al., IJCV 2024）相比，InterMamba 仅使用 66M 参数（InterGen 的 36%），平均推理时间 0.57 秒（InterGen 的 46%），同时在 R-Precision 和 MMDist 等关键指标上显著提升。消融实验验证了自适应时空融合对各模块协同的必要性：移除自适应参数导致模型无法收敛，而 Self-ASTM + Cross-ASTM + LIIA 的组合取得了最高的 R-Precision（0.705）和竞争力的 FID（5.945）。

尽管如此，该方法仍依赖扩散迭代过程，在细节交互表现、物理真实感和实时用户控制方面存在局限，为后续研究留下了开放问题。

## 背景与动机

### 问题背景

生成逼真且多样化的人际交互运动是计算机视觉与图形学领域的核心挑战，在虚拟现实、人机交互、游戏角色动画和机器人学习等应用中具有广泛需求。与单人运动生成不同，人际交互生成要求模型同时理解两个个体的运动动力学及其复杂的时空耦合关系——例如握手、拥抱或舞蹈中的协调动作——这对序列建模能力提出了更高要求。

近年来，基于扩散模型（Diffusion Models）的生成范式在该领域取得了显著进展。典型工作如 **InterGen**（Liang et al., IJCV 2024）采用基于Transformer骨干的扩散框架，通过交叉注意力机制建模双人交互，在InterHuman和InterX等基准上建立了较强的性能基线。然而，这一技术路线面临一个根本性瓶颈。

### 现有方法的瓶颈：平方复杂度制约可扩展性

基于Transformer的交互生成方法继承了自注意力机制的固有缺陷——计算复杂度与序列长度呈平方关系。在人际运动生成场景中，序列通常包含两个角色的多帧关节运动数据，序列长度随帧数线性增长，导致自注意力的计算开销急剧膨胀。正如原文所述：

> While Transformer-based approaches effectively model intricate contextual relationships, benefiting from their powerful attention mechanism, they also inherit the drawback of quadratic complexity, which limits their scalability and efficiency for long sequences.

这一瓶颈在三个维度上制约了实际应用：

1. **推理效率低**：以InterGen为例，其平均推理时间达1.233秒（DDIM 50步采样），难以满足实时交互场景（如VR/AR）的毫秒级响应要求。
2. **参数规模大**：InterGen参数量达182M，对部署资源（尤其是移动端或嵌入式设备）构成显著压力。
3. **长序列扩展性差**：当需要生成更长时域的运动序列时，平方复杂度导致计算资源需求非线性增长，限制了模型在复杂交互场景中的适用性。

### 本文动机

针对上述瓶颈，本文提出核心问题：**能否在不牺牲生成质量的前提下，以线性复杂度架构替代Transformer，实现高效、可扩展的人际交互运动生成？**

这一动机催生了三个关键设计方向：

1. **架构替换**：将Transformer骨干替换为选择性状态空间模型（Mamba），利用其线性/近线性复杂度的序列建模能力，从根本上解决平方复杂度问题。
2. **时空解耦建模**：将运动序列分解为空间维度（帧内关节结构）和时间维度（帧间运动连续性），通过并行SSM分支分别捕获，再以可学习权重自适应融合，避免维度耦合带来的冗余计算。
3. **显式交互建模**：在高效个体建模的基础上，设计交叉Mamba机制和局部交互聚合模块，以线性复杂度显式捕获双人协调关系，填补Mamba在交互建模中的空白。

这一设计理念首次将Mamba引入人际交互运动生成范式，旨在实现“更少参数、更快推理、更优质量”的三角平衡——最终InterMamba仅使用66M参数（InterGen的36%），平均推理时间降至0.57秒（InterGen的46%），同时在文本-运动对齐精度（R-Precision）和分布匹配度（MMDist）上实现显著提升。

## 核心创新

InterMamba 的核心创新在于**用线性复杂度的选择性状态空间模型（Mamba）替代传统 Transformer 骨干**，从根本上解决了人际交互生成中长序列建模的可扩展性瓶颈。其创新点可归纳为三个层次的“changed slots”：

### 1. 骨干架构替换：从平方复杂度到线性复杂度

现有基于 Transformer 的方法（如 InterGen，Liang et al., IJCV 2024）虽然能通过交叉注意力有效建模双人交互，但自注意力机制的平方复杂度限制了其在长序列上的可扩展性和推理效率。InterMamba 首次将 Mamba 引入人际交互生成范式，以线性或近线性复杂度捕获长程依赖，在保持甚至提升生成质量的同时，大幅降低计算开销。这一替换带来的直接收益是：InterMamba 仅用 **66M 参数**（InterGen 的 36%），平均推理时间 **0.57 秒**（InterGen 的 46%），实现了 **2.2 倍**的推理加速。

### 2. 解耦的自适应时空状态空间模型（ASTM）

将运动序列建模分解为两个并行的 SSM 分支，是 InterMamba 在建模粒度上的关键创新：

- **空间 SSM（Spatial SSM）**：沿关节维度扫描，捕获帧内关节间的结构关系。
- **时间 SSM（Temporal SSM）**：沿时间维度扫描，建模帧间的运动连续性。

两个分支的输出通过**可学习权重** $w_\alpha$ 和 $w_\beta$ 进行自适应融合（$z = w_{\alpha} h_t + w_{\beta} h_s$），使模型能够动态平衡空间结构与时间动态的贡献。消融实验证实了这一设计的必要性：**移除自适应参数后模型无法收敛**，而移除时间或空间分支均导致 R-Precision 和 FID 显著恶化（Table 4）。

### 3. 从个体建模到交互建模的层次化设计

InterMamba 通过三个模块的递进组合，实现了从独立运动到协同交互的完整建模链路：

- **Self-ASTM**：对每个角色单独处理，提取个体运动最显著的时空特征，建立基础运动先验。
- **LIIA（Local Interaction Information Aggregation）**：通过拼接个体特征、自适应层归一化（AdaLN）和两层卷积（$1\times1$ 和 $3\times3$），显式聚合双人局部交互信息。
- **Cross-ASTM**：基于混合状态空间模型（MSSM），利用 LIIA 生成的交互特征来动态计算 SSM 参数 $\mathbf{B}$、$\mathbf{C}$ 和 $\Delta$，使每个个体能感知对方的运动状态，实现交互关系的显式建模。

消融实验（Table 5）揭示了这一递进设计的因果机制：单独使用 Self-ASTM 可建立基础个体建模能力（R-Precision 0.371），但缺乏交互理解；加入 Cross-ASTM 后语义对齐提升（R-Precision 0.409），但运动质量下降（FID 增至 8.524）；进一步集成 LIIA 后，局部交互聚合有效平衡了生成质量与语义一致性，达到最优组合（R-Precision 0.705, FID 5.945）。

## 整体框架

InterMamba 的整体 pipeline 围绕 **基于扩散的运动生成框架** 与 **自适应时空 Mamba 骨干网络** 构建，将双人交互运动生成分解为个体运动建模、局部交互聚合与交叉交互建模三个递进阶段。图 4 展示了完整的架构概览。

**输入与条件编码。** 系统接收文本描述作为条件信号，首先通过冻结的 CLIP-ViT-L/14 编码器将文本提示转化为语义特征嵌入，作为后续扩散去噪过程的条件 $c$。运动数据初始化为高斯噪声 $x_t$，与文本条件、时间步 $t$ 一同输入去噪网络。

**扩散框架。** InterMamba 采用前向-反向扩散范式。前向过程按式 (1) 逐步向原始运动 $x_0$ 添加噪声，直至近似标准正态分布：
$$q ( x _ { t } \mid x _ { 0 } ) = \mathcal { N } \left( \sqrt { \bar { \alpha } _ { t } } x _ { 0 } , ( 1 - \bar { \alpha } _ { t } ) \mathbf { I } \right)$$
反向过程则通过去噪网络 $f_\theta$ 直接预测干净运动 $\hat{x}_0$，而非预测噪声，训练目标为式 (2) 所示的均方误差损失：
$$\mathcal { L } _ { \mathrm { t } } = \mathbb { E } _ { x _ { 0 } , t } \left[ \| x _ { 0 } - f _ { \theta } ( x _ { t } , t , c ) \| _ { 2 } ^ { 2 } \right]$$

**核心模块管线。** 去噪网络内部由三个关键模块串联构成：

1. **Self-ASTM Block（个体自适应时空建模）。** 对两个角色的运动序列分别处理。每个个体的运动特征经过层归一化后进入 ASTM（自适应时空 Mamba）单元，该单元将运动建模分解为并行的空间 SSM 分支和时间 SSM 分支——空间 SSM 捕获帧内关节结构关系，时间 SSM 建模帧间运动连续性——再通过可学习权重 $w_\alpha$、$w_\beta$ 自适应融合两分支输出（式 9）。随后经门控机制与残差连接得到个体特征 $h_p^S$（式 10）。此阶段为每个角色建立独立的运动表征基础。

2. **LIIA（局部交互信息聚合）。** 将两个个体的 Self-ASTM 输出 $h_a^S$ 与 $h_b^S$ 沿通道维度拼接，经自适应层归一化（AdaLN）以时间步条件进行归一化，再通过 $1\times1$ 和 $3\times3$ 两层卷积提取局部交互特征 $h_{inter}$（式 11）。该模块以轻量卷积操作显式捕获双人之间局部的空间-运动关联。

3. **Cross-ASTM Block（交叉交互建模）。** 基于混合状态空间模型（MSSM）架构，利用 LIIA 产生的交互特征 $h_{inter}$ 指导个体特征的进一步演化。具体而言，ASTM$_{cross}$ 内部包含时间 MSSM 分支和空间 MSSM 分支，二者分别将个体特征与交互特征融合处理，再通过可学习标量 $\alpha_c$、$\beta_c$ 融合得到交叉增强特征（式 13）。随后经门控与残差连接输出最终特征 $h_{out}$（式 12），使每个个体的运动表征显式感知另一方的交互影响。

**输出与推理。** 经多层 Self-ASTM、LIIA 与 Cross-ASTM 的交替堆叠处理后，去噪网络输出预测的干净运动 $\hat{x}_0$。推理时采用 DDIM 50 步采样，从纯噪声逐步去噪生成最终的双人运动序列。轻量版本 InterMamba (UltraLight) 以 66M 参数（仅为 InterGen 的 36%）实现平均 0.57 秒的推理速度，较 InterGen 加速约 2.2 倍。

**数据流总结：** 文本 → CLIP 编码器 → 条件嵌入 $c$；噪声 $x_t$ + $c$ + $t$ → Self-ASTM（个体特征提取）→ LIIA（局部交互聚合）→ Cross-ASTM（交叉交互建模）→ 预测 $\hat{x}_0$ → 迭代去噪 → 最终双人运动序列。

### 补充图表

![[assets/figures/papers/paper_list_l1687_InterMamba_Efficient_Human_Human_Interaction_Generation_with_Adaptive_Sp/figures/004_Figure_4.jpg]]
*Figure 4: The framework of InterMamba. The key components include Self Adaptive Spatio-Temporal Mamba module (Self-ASTM), Cross Adaptive Spatio-Temporal Mamba module (Cross-ASTM), and Local Interaction Information Aggregation module (LIIA)*

![[assets/figures/papers/paper_list_l1687_InterMamba_Efficient_Human_Human_Interaction_Generation_with_Adaptive_Sp/figures/001_Figure_1.jpg]]
*Figure 1: In this paper, we introduce an efficient human-to-human interaction generation method based on the Mamba framework, designed to achieve real-time, high-fidelity motion synthesis*

## 核心模块与公式推导

InterMamba 的核心架构由三个关键模块构成：**自适应时空Mamba（ASTM）** 作为基础算子，**Self-ASTM** 与 **Cross-ASTM** 分别负责个体运动建模与交互关系建模，**局部交互信息聚合（LIIA）** 桥接二者。以下逐一推导各模块的核心公式与变量含义。

### 4.1 自适应时空Mamba（ASTM）

ASTM 将运动序列建模分解为两个并行的选择性状态空间模型（SSM）分支：时间SSM捕获帧间运动连续性，空间SSM捕获帧内关节结构关系。

**时间分支** 沿时间维度扫描序列：

$$h_t = \text{LayerNorm}(\text{SSM}_{\text{temp}}(\text{Conv}_{\text{temp}}(\text{Linear}(h))))$$

其中 $h$ 为输入特征，$\text{Linear}$ 为线性投影，$\text{Conv}_{\text{temp}}$ 为时序卷积，$\text{SSM}_{\text{temp}}$ 为沿时间维度的选择性SSM算子，$\text{LayerNorm}$ 为层归一化。

**空间分支** 沿关节维度扫描：

$$h_s = \text{LayerNorm}(\text{SSM}_{\text{spat}}(\text{Conv}_{\text{spat}}(\text{Linear}(h))))$$

其中 $\text{SSM}_{\text{spat}}$ 沿空间（关节）维度操作，$\text{Conv}_{\text{spat}}$ 为空间卷积。

**自适应融合** 通过可学习权重动态平衡两分支贡献：

$$z = w_{\alpha} h_t + w_{\beta} h_s$$

其中 $w_{\alpha}, w_{\beta}$ 为可学习的标量权重，训练中自适应调整（见 Figure 8）。消融实验（Table 4）证实：移除自适应参数后模型无法收敛，验证了该机制对训练稳定性的必要性。

**SSM算子内部** 基于Mamba的选择机制，参数 $\mathbf{B}, \mathbf{C}, \Delta$ 均依赖输入：

$$\mathbf{B} = \text{Linear}_N(x), \quad \mathbf{C} = \text{Linear}_N(x), \quad \Delta = \tau_{\Delta}(P + \text{LayerNorm}(\text{Linear}_1(x)))$$

离散化后的状态空间递推为：

$$h_t = \bar{\mathbf{A}}_t h_{t-1} + \bar{\mathbf{B}}_t x_t, \quad y_t = \mathbf{C}_t h_t$$

其中 $\bar{\mathbf{A}}, \bar{\mathbf{B}}$ 通过零阶保持法从连续参数 $\mathbf{A}, \mathbf{B}$ 和步长 $\Delta$ 离散化得到：

$$\bar{\mathbf{A}} = \exp(\Delta \mathbf{A}), \quad \bar{\mathbf{B}} = (\Delta \mathbf{A})^{-1} (\exp(\Delta \mathbf{A}) - \mathbf{I}) \cdot \Delta \mathbf{B}$$

### 4.2 Self-ASTM模块

Self-ASTM 对每个角色单独建模，提取个体运动的长程依赖。给定角色 $p$ 的运动特征 $h_p$，其输出计算为：

$$\begin{array}{l}
\bar{h}_p = \text{LayerNorm}(h_p), \\
\hat{h}_p = \text{ASTM}(\bar{h}_p), \\
q = \sigma(\text{Linear}(\bar{h}_p)), \\
\widetilde{h}_p = \hat{h}_p \odot q, \\
h_p^S = h_p + \text{Linear}(\widetilde{h}_p)
\end{array}$$

其中 $\text{ASTM}(\cdot)$ 为第4.1节的自适应时空Mamba算子，$\sigma$ 为Sigmoid门控函数，$\odot$ 为逐元素乘法，最后通过残差连接保留原始信息。$h_p^S$ 为角色 $p$ 的个体运动表征。

### 4.3 局部交互信息聚合（LIIA）

LIIA 将两个角色的个体特征融合为交互特征，作为 Cross-ASTM 的条件输入：

$$\begin{array}{rl}
h_{ab} &= \text{concat}(h_a^S, h_b^S), \\
h_{ab} &= \text{AdaLN}(h_{ab}, \text{cond}_t), \\
h_{\text{inter}} &= \text{conv}_{3 \times 3}(\text{conv}_{1 \times 1}(h_{ab}))
\end{array}$$

其中 $\text{concat}$ 为通道拼接，$\text{AdaLN}$ 为自适应层归一化（以时间步条件 $\text{cond}_t$ 调制），$\text{conv}_{1 \times 1}$ 和 $\text{conv}_{3 \times 3}$ 分别为 $1 \times 1$ 和 $3 \times 3$ 卷积，通过残差连接聚合局部交互信息。$h_{\text{inter}}$ 为输出的交互特征。

### 4.4 Cross-ASTM模块

Cross-ASTM 基于混合状态空间模型（MSSM）显式建模角色间交互。其核心在于利用 LIIA 生成的交互特征 $h_{\text{inter}}$ 动态调制 SSM 参数，使每个角色感知对方信息。

**Cross-ASTM输出** 计算为：

$$\begin{array}{rl}
\widetilde{h}_p &= \text{LayerNorm}(h_p^S), \\
\widehat{h}_p &= \text{ASTM}_{\text{cross}}(\widetilde{h}_p, h_{\text{inter}}), \\
q &= \sigma(\text{Linear}(\widetilde{h}_p)), \\
\widetilde{h}_p &= \widehat{h}_p \odot q, \\
h_{\text{out}} &= h_p^S + \text{Linear}(\widetilde{h}_p)
\end{array}$$

其中 $\text{ASTM}_{\text{cross}}$ 为交互感知的ASTM变体，其内部计算（Eq. 13）展开为：

$$\begin{array}{l}
c_s = \text{LayerNorm}(\text{MSSM}_{\text{temp}}(\text{Conv}_{\text{temp}}(\text{Linear}(h_p^S), h_{\text{inter}}))), \\
c_t = \text{LayerNorm}(\text{MSSM}_{\text{spat}}(\text{Conv}_{\text{spat}}(\text{Linear}(h_p^{S'}), h_{\text{inter}}'))), \\
\hat{h}_p = \alpha_c \odot c_s + \beta_c \odot c_t
\end{array}$$

其中 $\text{MSSM}_{\text{temp}}$ 和 $\text{MSSM}_{\text{spat}}$ 分别为时间和空间维度的混合SSM，其参数 $\mathbf{B}, \mathbf{C}, \Delta$ 由交互特征 $h_{\text{inter}}$ 计算得到，使得SSM的选择机制能够感知对方角色的运动信息。$\alpha_c, \beta_c$ 为可学习标量，动态融合时空分支输出。

**因果机制总结**：Self-ASTM 建立个体运动基线（单独使用R-Precision 0.371, FID 5.918），LIIA 提取双人局部交互特征，Cross-ASTM 利用该交互特征通过MSSM调制SSM参数，使角色感知对方运动。消融实验（Table 5）表明：三者组合使R-Precision从0.371提升至0.705，同时维持竞争力FID 5.945，验证了模块间协同的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l1687_InterMamba_Efficient_Human_Human_Interaction_Generation_with_Adaptive_Sp/figures/003_Figure_3.jpg]]
*Figure 3: The spatial and temporal scanning process, where the spatial SSM captures intra-frame joint relationships and the temporal SSM models inter-frame relationships*

![[assets/figures/papers/paper_list_l1687_InterMamba_Efficient_Human_Human_Interaction_Generation_with_Adaptive_Sp/figures/005_Figure_5.jpg]]
*Figure 5: (a) This figure illustrates the core module of the ASTM in Section 4.1 — — State Space Model (SSM). Given an input sequence*

![[assets/figures/papers/paper_list_l1687_InterMamba_Efficient_Human_Human_Interaction_Generation_with_Adaptive_Sp/figures/006_Figure_6.jpg]]
*Figure 6: The structure of Local Interaction Information Aggregation (LIIA) consists of AdaLN for adaptive normalization, followed by 1×1 and 3×3 convolutions for feature refinement and local interaction modeling*

## 实验与分析

### 核心性能对比

InterMamba 在 InterHuman 和 Inter-X 两个主流人际交互数据集上均展现出具有竞争力的生成性能，同时实现了显著的效率优势。

**InterHuman 数据集（Table 1）**：与当前最强基线 **InterGen**（Liang et al., IJCV 2024）相比，InterMamba 在文本-运动对齐的关键指标上取得大幅领先。R-Precision Top-1 达到 **0.475**，较 InterGen 的 0.371 提升 0.104；MMDist 降至 **3.785**，较 InterGen 的 5.108 降低 1.323，表明生成运动的分布更接近真实数据。Diversity 为 7.963，同样更接近真实值。值得注意的是，FID 为 **5.945**，略逊于 InterGen 的 5.918（+0.027），但综合 R-Precision 和 MMDist 的显著优势，整体生成质量仍处于领先水平。

**Inter-X 数据集（Table 2）**：InterMamba 在 R-Precision Top-1 上达到 **0.4573**，优于 **in2IN**（Ruiz-Ponce et al., CVPRW 2024）的 0.4403，取得最佳文本对齐性能。Diversity 为 9.194，在所有方法中最接近真实数据分布。然而，FID 为 **0.517**，远高于 InterGen 的 0.238 和 in2IN 的 0.239，存在明显劣势。这一差异可能源于数据集分布特性或评价指标的局限性，需在具体应用中审慎评估。

**效率对比（Table 3）**：InterMamba 的轻量版本仅使用 **66M 参数**，为 InterGen（182M）的 36%；平均推理时间 **0.567 秒**，约为 InterGen（1.233 秒）的 46%，实现 2.2 倍加速。这一效率提升源于 Mamba 骨干的线性复杂度特性，验证了核心瓶颈的突破——将平方复杂度的自注意力替换为选择性状态空间模型，使长序列人际交互生成具备实时推理潜力。

### 消融实验分析

消融实验系统验证了 InterMamba 各组件的贡献与交互效应（Table 4, Table 5）。

![[assets/figures/papers/paper_list_l1687_InterMamba_Efficient_Human_Human_Interaction_Generation_with_Adaptive_Sp/figures/010_Table_4.jpg]]
*Table 4: The effectiveness of adaptive Spatio-Temporal SSM on the InterHuman dataset. Bold font highlights the best performance in each category*

![[assets/figures/papers/paper_list_l1687_InterMamba_Efficient_Human_Human_Interaction_Generation_with_Adaptive_Sp/figures/013_Table_5.jpg]]
*Table 5: The effectiveness of each module in InterMamba on the InterHuman dataset is presented. The Self-ASTM refers to the Self-ASTM Block in Section 4.2, Cross-ASTM denotes the Cross-ASTM Block in Section 4.4, and LIIA stands for the Local Interaction Information Aggregation module in Section 4.3. Bold font highlights the best performance in each category*

**自适应时空融合的必要性（Table 4）**：移除时间 Mamba 分支后，FID 升至 5.539，R-Precision 降至 0.679；移除空间 Mamba 分支同样导致性能下降。若进一步移除自适应参数（可学习权重 $w_\alpha$、$w_\beta$），模型**无法收敛**，证明自适应机制不仅是性能优化手段，更是训练稳定性的关键保障。自适应参数在训练过程中动态调整时空分支的贡献比例（Figure 8），使模型能根据运动序列特性灵活分配建模资源。

**模块递增效应（Table 5）**：单独使用 Self-ASTM 建立了个体运动建模的基线能力（R-Precision 0.371, FID 5.918），但缺乏交互理解导致文本-运动对齐欠佳。加入 Cross-ASTM 后，R-Precision 提升至 0.409，证明交叉 Mamba 模块有效捕获了角色间交互关系；然而 FID 显著恶化至 8.524，暗示增强协调性的同时可能引入了运动不一致性。进一步集成 LIIA 后，R-Precision 跃升至 **0.705**（所有配置中最高），FID 回落至 **5.945** 的竞争力水平。这一结果表明，局部交互信息聚合模块是平衡生成质量与语义一致性的关键——通过卷积操作在局部感受野内融合双人特征，有效抑制了 Cross-ASTM 引入的运动伪影。

### 失败模式与局限性

尽管 InterMamba 在多项指标上取得领先，仍存在若干值得关注的局限：

1. **FID 指标的波动性**：在 InterHuman 上 FID 略逊于 InterGen，在 Inter-X 上差距更为显著。这提示 Mamba 架构在捕捉运动细节的统计分布上可能不如注意力机制精细，尤其在数据分布复杂或样本量有限的情况下。
2. **扩散采样的效率-质量权衡**：当前推理基于 DDIM 50 步采样，减少步数可进一步加速，但可能损害运动质量。如何在更少采样步数下保持生成精度，仍是开放问题。
3. **交互细节的缺失**：生成的运动在微妙交互表现（如情感传递、接触点精度）和物理真实感方面仍有不足，需引入接触建模和生物力学约束加以强化。
4. **实际部署差距**：当前方法缺乏灵活的用户控制和实时适应性，与交互式应用需求之间存在鸿沟，需进一步探索多任务优化和在线适应机制。

### 关键图表结论

- **Figure 2**：气泡图直观展示了 InterMamba 系列在 R-Precision 与推理时间构成的帕累托前沿上占据优势位置，以更小参数量（气泡尺寸）实现更高文本对齐精度和更快推理速度。
- **Table 4**：自适应参数的移除导致训练崩溃，确立了自适应时空融合作为方法核心机制的地位。
- **Table 5**：Self-ASTM + Cross-ASTM + LIIA 的组合取得最优 R-Precision，揭示了三个模块的协同效应：个体建模 → 交互感知 → 局部精炼的级联架构是有效的设计范式。
- **Figure 8**：自适应参数随训练进程的动态变化，验证了模型自主学习时空贡献比例的能力。

![[assets/figures/papers/paper_list_l1687_InterMamba_Efficient_Human_Human_Interaction_Generation_with_Adaptive_Sp/figures/002_Figure_2.jpg]]
*Figure 2: This figure presents a comparative analysis of different methods on the Interhuman dataset in terms of R-Precision (Top-1) and inference time, with the bubble size indicating the number of model parameters. From the figure, our InterMamba and InterMamba (UltraLight), which are highlighted in a red dashed box, achieve superior performance compared to other methods*

![[assets/figures/papers/paper_list_l1687_InterMamba_Efficient_Human_Human_Interaction_Generation_with_Adaptive_Sp/figures/012_Figure_8.jpg]]
*Figure 8: As the training progresses, the variation process of the adaptive parameters α and β*

### 补充图表

![[assets/figures/papers/paper_list_l1687_InterMamba_Efficient_Human_Human_Interaction_Generation_with_Adaptive_Sp/figures/007_Table_1.jpg]]
*Table 1: The quantitative comparisons on the InterHuman [24] test set. We run all the evaluations 20 times. ± indicates a 95% confidence interval. ↑ (↓) indicates that a higher (lower) result corresponds to better performance, and → means the closer to ground-truth the better. Bold indicates the best result, and underline refers to the second best*

![[assets/figures/papers/paper_list_l1687_InterMamba_Efficient_Human_Human_Interaction_Generation_with_Adaptive_Sp/figures/008_Table_2.jpg]]
*Table 2: The quantitative comparisons on the Inter-X [52] test set. We run all the evaluations 20 times. ± indicates a 95% confidence interval. Bold indicates the best result, and underline refers to the second best*

![[assets/figures/papers/paper_list_l1687_InterMamba_Efficient_Human_Human_Interaction_Generation_with_Adaptive_Sp/figures/011_Table_3.jpg]]
*Table 3: This table compares the computational complexity of our method with that of other approaches, based on three indicators: average inference time, parameters, and FLOPs. As shown in the table, our Inter-Mamba achieves the highest overall efficiency across all metrics*

## 方法谱系与知识库定位

### 1. 方法脉络与核心差异

InterMamba 处于**基于扩散模型的文本驱动双人交互运动生成**这一任务线上。该任务的核心瓶颈在于：Transformer 架构的自注意力机制在处理长序列时具有平方复杂度，导致模型在捕捉长程时空依赖时计算开销巨大，难以满足实时交互应用的可扩展性需求。InterMamba 的因果调节旋钮是将骨干网络从 Transformer 替换为**选择性状态空间模型（Mamba）**，并设计解耦的自适应时空 SSM 分支与交叉交互建模，以线性或近线性复杂度捕获长程依赖。

与现有工作的关键差异体现在以下维度：

- **架构范式转换**：主流方法普遍采用 Transformer 作为扩散模型的去噪骨干。**InterGen** (Liang et al., IJCV 2024) 使用交叉注意力机制建模双人交互，是 InterMamba 的直接对标基线。**ComMDM** (Shafir et al., arXiv 2023) 同样基于 Transformer 扩散框架。InterMamba 首次将 Mamba 引入人际交互运动生成范式，将计算复杂度从平方级降至线性/近线性。

- **时空建模策略**：InterMamba 提出**自适应时空 Mamba（ASTM）**，将运动序列建模分解为并行的时间 SSM 分支（帧间运动连续性）和空间 SSM 分支（帧内关节结构），并通过可学习权重 $w_\alpha, w_\beta$ 自适应融合：
  $$z = w_{\alpha} h_t + w_{\beta} h_s$$
  消融实验证实，移除任一分支均导致性能显著下降（仅时间分支：FID 5.539, R-Precision 0.679；仅空间分支：FID 6.775, R-Precision 0.625；完整 ASTM：FID 5.945, R-Precision 0.705），验证了时空解耦建模的必要性。

- **交互建模机制**：InterMamba 设计了**交叉自适应时空 Mamba（Cross-ASTM）**和**局部交互信息聚合模块（LIIA）**。Cross-ASTM 基于混合状态空间模型（MSSM），利用交互特征 $h_{inter}$ 生成 SSM 参数，使每个角色能动态感知对方的运动状态。LIIA 通过自适应层归一化（AdaLN）和两层卷积（$1\times1$ 和 $3\times3$）聚合双人局部交互信息。消融实验表明，Self-ASTM + Cross-ASTM + LIIA 组合取得最高 R-Precision（0.705），而单独 Cross-ASTM 虽提升文本-运动对齐（R-Precision 0.409），却导致运动质量下降（FID 增至 8.524），说明交互建模需与局部信息聚合配合才能平衡语义一致性与生成质量。

### 2. 知识库定位

**上游依赖**：

- **扩散模型**：采用 DDIM 类扩散框架，直接预测 $\hat{x}_0$ 而非噪声（遵循 的做法），训练目标为：
  $$\mathcal{L}_t = \mathbb{E}_{x_0, t}\left[\|x_0 - f_\theta(x_t, t, c)\|_2^2\right]$$

- **状态空间模型**：继承 Mamba 的选择性扫描机制，参数 $\mathbf{B}, \mathbf{C}, \Delta$ 均由输入动态生成：
  $$\mathbf{B} = Linear_N(x), \quad \mathbf{C} = Linear_N(x), \quad \Delta = \tau_\Delta(P + LayerNorm(Linear_1(x)))$$
  离散化采用零阶保持法（ZOH）。

- **文本编码**：使用冻结的 CLIP-ViT-L/14 提取文本语义特征。

**下游适用边界**：

- **适用场景**：文本驱动的双人交互运动生成，支持实时或近实时推理（UltraLight 版本仅 0.325 秒推理时间）。在 InterHuman 和 InterX 数据集上验证了有效性。
- **不适用/需谨慎的场景**：
  - 需要精细物理接触建模和生物力学约束的场景（当前方法在微妙交互细节、情感表达上仍有不足）。
  - 需要强用户实时控制、多任务协同的交互式应用（方法尚缺乏灵活的在线适应能力）。
  - InterX 数据集上 FID 指标（0.517）明显劣于 InterGen（0.238），可能存在分布偏差或评价指标局限性，在该数据集上的运动质量需进一步验证。

### 3. 局限性与开放问题

**已确认的局限性**（论文明确提及或实验可验证）：

1. **扩散迭代开销**：仍依赖多步扩散去噪过程，减少采样步数可加速推理但可能损害运动质量。当前推理速度（0.567 秒）基于 DDIM 50 步采样，实际部署中需权衡速度与质量。
2. **交互细节不足**：生成的运动在微妙交互表现（如情感传递、接触点精度）和物理真实感上仍有欠缺，需加强接触建模和生物力学约束。
3. **实时适应性不足**：方法在交互式应用中缺乏灵活的用户控制、实时适应性和多任务优化能力。
4. **跨数据集泛化差异**：在 InterX 数据集上 FID 显著劣于部分基线，可能源于数据集分布差异或 FID 指标对 Mamba 生成运动的分布特性不敏感。该点需人工进一步验证。

**开放问题**：

1. 能否在不损害运动质量的前提下进一步减少扩散采样步数，实现真正的实时生成？
2. 如何增强细微交互细节（如情感、接触点）和物理真实感的建模，例如引入物理模拟器作为后处理或约束？
3. 如何实现更灵活的用户控制、实时适应性和多任务协同，以弥合算法与实际交互应用之间的鸿沟？
4. Mamba 的选择性扫描机制在双人交互场景下是否存在长程遗忘问题？如何设计更有效的状态记忆策略？

### 4. 证据强度评估

- **架构创新性**：强。首次将 Mamba 引入人际交互运动生成，时空解耦与自适应融合设计有清晰的消融支持（Table 4, Table 5）。
- **效率提升**：强。参数量（66M vs 182M）和推理时间（0.567s vs 1.233s）的对比数据确凿（Table 3），2.2 倍加速和 64% 参数缩减具有实际部署价值。
- **生成质量**：中等偏强。在 InterHuman 上 R-Precision（0.475）和 MMDist（3.785）显著领先，但 FID（5.945）略差于 InterGen（5.918）；在 InterX 上 R-Precision 最优但 FID 明显落后。整体呈现“语义对齐强、分布匹配有波动”的特征。
- **消融完整性**：强。对时空分支、自适应参数、各模块组合均进行了系统消融，且揭示了自适应参数对训练收敛的必要性（移除后模型无法收敛）。

## 原文 PDF

![[paperPDFs/arxiv_2025/InterMamba_Efficient_Human_Human_Interaction_Generation_with_Adaptive_Spatio_Temporal_Mamba.pdf]]
