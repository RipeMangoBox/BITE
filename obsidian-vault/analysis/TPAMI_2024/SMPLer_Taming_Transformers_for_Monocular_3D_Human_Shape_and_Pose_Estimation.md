---
title: "SMPLer: Taming Transformers for Monocular 3D Human Shape and Pose Estimation"
type: paper
paper_level: A
venue: TPAMI
year: 2024
pdf_ref: paperPDFs/TPAMI_2024/SMPLer_Taming_Transformers_for_Monocular_3D_Human_Shape_and_Pose_Estimation.pdf
project_link: null
code_link: https://github.com/xuxy09/SMPLer
aliases:
- SMPLer
tags:
- TPAMI_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 解耦注意力操作（去除特征-特征交互，仅保留目标-特征交叉注意力和目标-目标自注意力）和基于SMPL的紧凑目标表示（仅需少量参数表达姿态和形状），将复杂度降为线性，大幅降低计算量。
primary_logic: 通过解耦注意力实现线性复杂度，并利用SMPL参数化表达使得Transformer能高效利用高分辨率、多尺度特征，再结合多尺度注意力与关节感知注意力，在高效的前提下显著提升单目三维人体重建精度。
claims:
- SMPLer在Human3.6M上MPJPE为45.2mm，比Mesh Graphormer改善超过10%，参数量不到三分之一。
- 解耦注意力+SMPL表示（Table 2(d)）显著降低GPU内存和计算量，并实现47.0 MPJPE。
- 多尺度注意力优于单尺度特征；使用全部四个尺度获得最佳性能（47.0 MPJPE）。
- 去除关节感知注意力导致MPJPE从47.0增加到51.4，PA-MPJPE从32.8上升到34.5。
---

# SMPLer: Taming Transformers for Monocular 3D Human Shape and Pose Estimation

> [!tip] 核心洞察
> 通过解耦注意力实现线性复杂度，并利用SMPL参数化表达使得Transformer能高效利用高分辨率、多尺度特征，再结合多尺度注意力与关节感知注意力，在高效的前提下显著提升单目三维人体重建精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | SMPLer: 驯服Transformer用于单目三维人体形状与姿态估计 |
| 英文题名 | SMPLer: Taming Transformers for Monocular 3D Human Shape and Pose Estimation |
| 会议/期刊 | TPAMI 2024 |
| Links | [Code](https://github.com/xuxy09/SMPLer) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SMPLer |
| Dataset | Human3.6M, 3DPW, Speed/Compute |

> [!tip] 效果简介
> - Human3.6M 上，MPJPE ↓ 45.2 (SMPLer-L) vs 51.2 (Mesh Graphormer) (-11.7%)；PA-MPJPE ↓ 32.4 (SMPLer-L) vs 34.5 (Mesh Graphormer) (-6.1%)。
> - 3DPW 上，MPJPE ↓ 73.7 (SMPLer-L) vs 74.7 (Mesh Graphormer) (-1.3%)；PA-MPJPE ↓ 43.4 (SMPLer-L) vs 45.6 (Mesh Graphormer) (-4.8%)；MPVE ↓ 82.0 (SMPLer-L) vs 87.7 (Mesh Graphormer) (-6.5%)。
> - Speed/Compute 上，FPS ↑ / GFlops ↓ 96.0 / 8.7 (SMPLer) vs 34.6 / 45.4 (Mesh Graphormer) (+177% fps / -81% GFlops)。

## 概要

单目三维人体重建旨在从单张RGB图像中恢复人体的三维姿态与形状。近年来，基于Transformer的方法在该任务上取得了显著进展，但其固有的计算瓶颈限制了性能的进一步提升。现有工作（如**Mesh Graphormer**，Lin et al., ICCV 2021；**METRO**，Lin et al., CVPR 2021）普遍采用ViT式的全注意力操作，将目标嵌入与图像特征拼接后进行自注意力计算，导致计算与内存复杂度随特征长度呈二次增长——$\mathcal{O}((l_F + l_T)^2)$。这一瓶颈使得模型难以利用高分辨率的图像特征，而高分辨率特征恰恰对精确重建至关重要。

**核心瓶颈**：全注意力机制中特征-特征交互的计算冗余，以及基于顶点的目标表示（$l_T = 6890$个嵌入）带来的高维目标空间，二者叠加使得高效利用多尺度、高分辨率特征成为奢望。

**核心思路**：SMPLer通过两个关键设计驯服Transformer，使其能够高效利用高分辨率特征：
1. **解耦注意力**：将全注意力拆解为目标-特征交叉注意力与目标-目标自注意力的级联，去除特征-特征交互，将复杂度降为$\mathcal{O}(l_F l_T + l_T^2)$——即对特征长度线性。
2. **基于SMPL的紧凑目标表示**：用SMPL参数化模型的姿态、形状与相机参数替代顶点嵌入，将目标嵌入长度从6890压缩至仅$H+2=26$，大幅降低目标侧的计算开销。

在此基础上，SMPLer进一步引入**多尺度注意力**（融合不同分辨率特征以获取全局上下文）和**关节感知注意力**（在关节周围局部区域提取精细特征），在保持高效的前提下显著提升重建精度。

**核心结论**：
- 在Human3.6M上，SMPLer-L的MPJPE达到**45.2 mm**，相比Mesh Graphormer改善超过**10%**，参数量不到其三分之一。
- 在3DPW上，MPJPE为**73.7 mm**，PA-MPJPE为**43.4 mm**，MPVE为**82.0 mm**，均优于此前最优方法。
- 推理速度达到**96.0 fps**，计算量仅**8.7 GFlops**，比Mesh Graphormer快2.8倍且计算量低5.2倍。

**方法定位**：SMPLer属于基于SMPL参数回归的混合架构（CNN骨干+Transformer解码器），其Transformer部分采用解耦注意力与分层迭代优化，在方法谱系上介于纯CNN回归（如**SPIN**，Kolotouros et al., ICCV 2019）与顶点回归Transformer（如Mesh Graphormer）之间，兼具参数化模型的结构先验优势与Transformer的全局建模能力。



单目三维人体形状与姿态估计旨在从单张RGB图像中恢复人体的三维网格和关节位置，是计算机视觉领域的核心问题之一，在虚拟现实、人机交互、运动分析等应用中具有广泛价值。该任务的核心挑战在于从二维投影中推断深度信息，同时需要处理人体姿态的高度自由度、自遮挡、服装变化以及复杂背景等干扰因素。

近年来，基于参数化人体模型的方法取得了显著进展。以**SPIN**（Kolotouros et al., ICCV 2019）和**VIBE**（Kocabas et al., CVPR 2020）为代表的工作将三维人体重建转化为SMPL模型参数的回归问题，利用卷积神经网络（CNN）从图像中提取特征并预测姿态参数 $\theta$ 和形状参数 $\beta$，再通过SMPL模型生成网格顶点 $Y \in \mathbb{R}^{N \times 3} = f_{\mathrm{SMPL}}(\theta, \beta)$。这类方法受益于SMPL流形的强先验约束，能够保证输出结果始终位于合理的人体形状空间内，但CNN有限的感受野限制了其对全局空间关系的建模能力。

为克服CNN的局限，**METRO**（Lin et al., CVPR 2021）和**Mesh Graphormer**（Lin et al., ICCV 2021）将Transformer架构引入三维人体重建，直接回归6890个网格顶点坐标。这些方法采用ViT风格的全注意力机制，将图像特征 $F$ 与顶点嵌入 $T$ 拼接后进行自注意力操作：

$$h_{\mathrm{self}}(T \parallel F)$$

这种设计虽然能有效建模全局依赖关系，但存在一个根本性的效率瓶颈：全注意力的计算与内存复杂度随特征长度呈二次增长，即 $\mathcal{O}((l_F + l_T)^2)$。当使用高分辨率特征图（如HRNet输出的最高分辨率特征）时，特征令牌数量 $l_F$ 可达数千个，导致注意力计算的开销急剧膨胀。因此，现有Transformer方法被迫仅使用最低分辨率的特征图 $F_S$，牺牲了高分辨率特征中蕴含的精细空间信息，而这类信息对精确重建人体关节位置和肢体轮廓至关重要。

此外，现有Transformer方法直接回归顶点坐标，虽然表达灵活，但失去了SMPL参数化表示的结构化先验。这意味着模型可能输出不符合人体解剖结构的网格，偏离真实的SMPL流形，不仅影响重建精度，也给后续应用（如虚拟化身控制）带来不便——需要额外的迭代优化步骤将结果投影回SMPL空间，这一过程耗时且容易累积误差。

综上所述，现有方法面临一个两难困境：**全注意力机制的高计算开销限制了高分辨率特征的利用，而高分辨率特征恰恰是精确重建的关键**。这构成了该领域的核心瓶颈。本文的动机正是打破这一困境，通过重新设计注意力机制和目标表示，使Transformer能够在保持高效计算的前提下充分利用高分辨率、多尺度的图像特征，从而显著提升单目三维人体重建的精度与效率。



## 核心方法与创新机理

### 瓶颈诊断：全注意力与顶点表示的效率困境

现有基于Transformer的单目三维人体重建方法（如**Mesh Graphormer**（Lin et al., ICCV 2021）、**METRO**（Lin et al., CVPR 2021））普遍采用ViT风格的全注意力操作：将目标嵌入与图像特征拼接后进行自注意力计算，即 $h_{\mathrm{self}}(T \parallel F)$。该操作的复杂度为 $\mathcal{O}((l_F + l_T)^2)$，随特征长度呈二次增长，直接导致两个致命后果：

1. **高分辨率特征不可用**：当特征图尺寸稍大时，计算量与GPU显存需求急剧膨胀，迫使现有方法仅能使用CNN骨干输出的最低分辨率特征 $F_S$，丢弃了大量对精确重建至关重要的细粒度空间信息。
2. **顶点级表示的冗余**：现有方法以SMPL网格的6890个顶点作为目标表示（$l_T = 6890$），进一步加剧了复杂度负担。

这一瓶颈的因果链条清晰：全注意力的二次复杂度 → 高分辨率特征被舍弃 → 重建精度受限。SMPLer的核心创新正是围绕这一瓶颈展开，通过两个相互协同的“changed slots”从根本上打破僵局。

### 关键创新一：解耦注意力——从二次到线性

SMPLer提出**解耦注意力**（decoupled attention），将全注意力操作拆解为两个级联步骤：

$$h_{\mathrm{self}}(h_{\mathrm{cross}}(T, F))$$

其中第一步为目标-特征交叉注意力 $h_{\mathrm{cross}}(T, F)$，第二步为目标-目标自注意力 $h_{\mathrm{self}}(\cdot)$。这一拆解的核心价值在于**剪除了特征-特征之间的交互计算**——在三维人体重建任务中，特征像素之间的全局交互并非必需，真正重要的是目标（人体关节/形状参数）与图像特征之间的对应关系。

解耦后的复杂度降为 $\mathcal{O}(l_F l_T + l_T^2)$，对特征长度 $l_F$ 呈线性关系。这使得模型首次能够处理高分辨率特征图，为后续多尺度特征利用铺平了道路。

### 关键创新二：基于SMPL的紧凑目标表示——从6890到26

与解耦注意力配套，SMPLer将目标表示从基于顶点（6890个嵌入）替换为**基于SMPL参数化模型**的紧凑表示。具体而言，目标嵌入 $\mathcal{T} \in \mathbb{R}^{(H+2) \times d}$ 仅包含：

- $H$ 行（$H=24$）对应人体各部位的旋转姿态（以6D旋转表示）；
- 1行对应体型参数 $\beta$；
- 1行对应相机参数。

总计仅需26个嵌入（$l_T = 26$），相比顶点表示的6890个嵌入减少了两个数量级以上。这一设计的精妙之处在于：SMPL参数本身是人体形状与姿态的完备低维流形表达，通过SMPL函数 $f_{\mathrm{SMPL}}(\theta, \beta)$ 可以解析地恢复出6890个网格顶点，无需在Transformer内部维护高维顶点嵌入。

### 两个创新的协同效应

解耦注意力和SMPL目标表示并非孤立设计，二者形成强协同：

- **解耦注意力消除特征-特征交互**，使复杂度对特征长度线性化，为高分辨率特征利用提供可能；
- **SMPL紧凑表示大幅缩短目标嵌入长度**，进一步压低交叉注意力和自注意力的计算量。

消融实验（Table 2）清晰验证了这一协同效应：全注意力+顶点表示（配置a）因显存需求过大甚至无法正常训练；而解耦注意力+SMPL表示（配置d）不仅GPU显存和GFlops大幅降低，更实现了47.0 mm的MPJPE，在精度和效率上全面占优。

### 关键创新三：多尺度注意力——释放高分辨率特征的潜力

在解耦注意力使高分辨率特征可用之后，SMPLer进一步设计了**多尺度注意力**机制以充分利用CNN骨干（HRNet）输出的多分辨率特征金字塔 $\mathcal{F} = \{F_1, F_2, ..., F_S\}$：

$$h_{\mathrm{ms}}(\mathcal{T}, \mathcal{F}) = \frac{1}{S} \sum_{i=1}^{S} h_{\mathrm{cross}}(\mathcal{T}, F_i)$$

各尺度使用独立的投影权重 $W_q, W_k, W_v$，最终输出为所有尺度交叉注意力的均值。配合**池化生成的多尺度位置编码** $\phi_i = f_{\mathrm{pool}}^{(2^{i-1})}(\phi_1)$（仅学习最高分辨率编码，低分辨率编码通过平均池化获得），确保不同尺度间空间位置的一致性。

消融实验（Table 3）表明：使用全部4个尺度（$S=4$）相比仅使用单尺度（$S=1$）将MPJPE从48.4 mm降至47.0 mm，验证了高分辨率特征对精确重建的贡献。

### 关键创新四：关节感知注意力——全局与局部的互补

多尺度注意力捕获全局上下文，但对关节附近的局部细节敏感度不足。SMPLer引入**关节感知注意力**，将交叉注意力的键和值限制在每个关节周围 $r \times r$ 的局部图像块内：

$$h_{\mathrm{ja}}(\mathcal{T}_i, \mathcal{F}) = f_{\mathrm{soft}}\left(\frac{(\mathcal{T}_i W_q)(F_1^{\mathcal{N}(\mathcal{T}_i)} W_k)^\top}{\sqrt{d}} + \eta\right)(F_1^{\mathcal{N}(\mathcal{T}_i)} W_v)$$

其中 $\eta$ 为局部块内的相对位置编码。最终，姿态部分（前 $H$ 行）的注意力为全局多尺度注意力与局部关节感知注意力的均值，而形状和相机嵌入仅使用多尺度注意力：

$$h_{\mathrm{co}}(\mathcal{T}_i, \mathcal{F}) = \begin{cases} \frac{1}{2}(h_{\mathrm{ja}} + h_{\mathrm{ms}}), & i \le H \\ h_{\mathrm{ms}}, & i > H \end{cases}$$

消融实验（Table 5）显示：去除关节感知注意力导致MPJPE从47.0 mm退化至51.4 mm，PA-MPJPE从32.8 mm升至34.5 mm，验证了局部信息对关节定位精度的关键作用。

### 创新总结：changed slots 全景

| 设计维度 | 基线方法（Mesh Graphormer/METRO） | SMPLer | 核心收益 |
|---------|--------------------------------|--------|---------|
| 注意力操作 | 全注意力 $h_{\mathrm{self}}(T \parallel F)$ | 解耦注意力 $h_{\mathrm{self}}(h_{\mathrm{cross}}(T, F))$ | 复杂度从二次降为线性，支持高分辨率特征 |
| 目标表示 | 顶点级（$l_T=6890$） | SMPL参数化（$l_T=26$） | 嵌入长度减少两个数量级，保证输出在SMPL流形上 |
| 多尺度集成 | 仅使用最低分辨率特征 | 多尺度注意力（平均各尺度交叉注意力） | 融合全局上下文，MPJPE降低1.4 mm |
| 局部信息 | 无显式机制 | 关节感知注意力（局部 $r \times r$ 块） | 增强关节定位精度，MPJPE改善4.4 mm |
| 位置编码 | 每尺度独立学习 | 池化生成多尺度编码 | 保持跨尺度空间一致性，MPJPE改善1.5 mm |

这些创新共同实现了**精度与效率的双重突破**：SMPLer在Human3.6M上达到45.2 mm MPJPE（SMPLer-L），较Mesh Graphormer改善超过10%，参数量不到其三分之一；推理速度达96.0 fps，比Mesh Graphormer快2.8倍，计算量低5.2倍（Table 7）。



SMPLer 的整体框架遵循“CNN 骨干提取多尺度特征 + Transformer 迭代重建三维人体”的流水线设计。给定一张单目 RGB 输入图像，首先通过 CNN 骨干网络（HRNet）提取多尺度图像特征 $\mathcal{F} = \{F_1, F_2, \dots, F_S\}$，其中 $F_1$ 为最高分辨率特征图，$F_S$ 为最低分辨率特征图。这些多尺度特征随后被送入 Transformer 模块，用于重建三维人体姿态与形状。

框架的两大核心设计直接嵌入在 Transformer 内部：
1. **解耦注意力模块（Decoupled Attention）**：将传统 Transformer 中使用的全注意力 $h_{\mathrm{self}}(T \parallel F)$ 替换为“目标-特征交叉注意力 + 目标-目标自注意力”的级联形式 $h_{\mathrm{self}}(h_{\mathrm{cross}}(T, F))$，从而将计算与内存复杂度从 $\mathcal{O}((l_F + l_T)^2)$ 降至 $\mathcal{O}(l_F l_T + l_T^2)$，实现了相对于特征长度 $l_F$ 的线性复杂度。
2. **基于 SMPL 的紧凑目标表示（SMPL-based Target Representation）**：摒弃了以往基于顶点（6890 个嵌入）的目标表示，转而采用仅需 $H+2 = 26$ 个嵌入的紧凑表示 $\mathcal{T} \in \mathbb{R}^{(H+2) \times d}$，其中前 $H$ 行对应 $H$ 个身体部件的旋转姿态，剩余两行分别对应体型参数 $\beta$ 和弱透视相机参数 $C$。

Transformer 采用分层迭代架构，包含 $B$ 个 Transformer Block，每个 Block 又由 $U$ 个 Transformer Unit 组成。每个 Unit 的核心操作为组合注意力 $h_{\mathrm{co}}(\mathcal{T}_i, \mathcal{F})$ 后接目标自注意力，形成最终注意力模块 $h_{\mathrm{final}}(\mathcal{T}, \mathcal{F}) = h_{\mathrm{self}}(h_{\mathrm{co}}(\mathcal{T}, \mathcal{F}))$。其中，组合注意力对姿态部分（前 $H$ 行）平均融合全局多尺度注意力 $h_{\mathrm{ms}}$ 和局部关节感知注意力 $h_{\mathrm{ja}}$，而对形状和相机部分仅使用多尺度注意力。

迭代过程可形式化为：
$$\mathcal{T}^b = f_{\mathrm{TB}}^b(\mathcal{T}^{b-1}, P^{b-1}, \mathcal{F}), \quad P^b = f_{\mathrm{fusion}}(\mathcal{T}^b, P^{b-1})$$
其中 $P^{b-1}$ 为上一 Block 输出的 SMPL 参数估计，$f_{\mathrm{TB}}^b$ 为第 $b$ 个 Transformer Block，$f_{\mathrm{fusion}}$ 为融合层，通过残差加法将当前估计与历史估计结合。每个 Block 内部还包含一个 2D 关节回归模块（J-Reg），从三维估计结果通过 SMPL 模型和弱透视投影计算二维关节坐标，为下一轮迭代提供空间位置线索。默认配置为 $B=3, U=2$，输入图像尺寸统一为 $224 \times 224$。

整个流水线的数据流可以概括为：**输入图像 → HRNet 多尺度特征 → 初始 SMPL 参数 $P^0$ → 分层 Transformer 迭代更新目标嵌入与 SMPL 参数 → 最终三维网格与关节输出**。

### 补充图表

![[assets/figures/papers/paper_list_l1649_SMPLer_Taming_Transformers_for_Monocular_3D_Human_Shape_and_Pose_Estimat/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed framework. Given a monocular input image, we first use a CNN backbone [31] to extract image features F, which are fed into the Transformer to reconstruct the 3D human body. The main ingredients of this framework are 1) an efficient decoupled attention module in the Transformer (Section 3.1), and 2) a compact target representation T based on parametric human model (Section 3.2). More detailed descriptions of the Transformer architecture are provided in Figure 3*

![[assets/figures/papers/paper_list_l1649_SMPLer_Taming_Transformers_for_Monocular_3D_Human_Shape_and_Pose_Estimat/figures/014_Figure_12.jpg]]
*Figure 12: Output of Block 1, 2, and 3 of SMPLer. The reconstruction result is progressively refined in the hierarchical architecture*



### 3.1 标准注意力与全注意力瓶颈

Transformer 的核心操作为缩放点积注意力（Scaled Dot-Product Attention），给定查询 $\boldsymbol{Q}$、键 $K$、值 $V$，其形式为：

$$h(\boldsymbol{Q}, K, V) = f_{\mathrm{soft}}\left(\frac{(QW_q)(KW_k)^\top}{\sqrt{d}}\right)(VW_v) \tag{Eq. 1}$$

其中 $W_q, W_k, W_v$ 为可学习的投影矩阵，$d$ 为特征维度，$f_{\mathrm{soft}}$ 为 softmax 函数。

现有基于 Transformer 的三维人体重建方法（如 **Mesh Graphormer**（Lin et al., ICCV 2021）和 **METRO**（Lin et al., CVPR 2021））采用 ViT 风格的全注意力操作：将目标嵌入 $T \in \mathbb{R}^{l_T \times d}$ 与图像特征 $F \in \mathbb{R}^{l_F \times d}$ 沿序列维度拼接后进行自注意力：

$$h_{\mathrm{self}}(T \parallel F) \tag{Eq. 2}$$

该操作的计算与内存复杂度为 $\mathcal{O}((l_F + l_T)^2)$，与特征长度 $l_F$ 呈二次关系。当需要利用高分辨率特征（$l_F$ 较大）以提升重建精度时，全注意力会带来不可承受的计算开销。这一瓶颈构成了本工作的核心动因。

### 3.2 解耦注意力：线性复杂度的关键设计

为解决上述瓶颈，SMPLer 提出**解耦注意力**（Decoupled Attention），通过剪除特征-特征之间的交互，将全注意力拆分为两个级联操作：

$$h_{\mathrm{self}}(h_{\mathrm{cross}}(T, F)) \tag{Eq. 3}$$

具体而言，首先执行目标到特征的交叉注意力 $h_{\mathrm{cross}}(T, F)$，以目标嵌入 $T$ 为查询、图像特征 $F$ 为键和值，从特征中聚合信息；随后对更新后的目标嵌入执行目标-目标自注意力 $h_{\mathrm{self}}(\cdot)$，建模目标内部的依赖关系。该设计的复杂度降为 $\mathcal{O}(l_F l_T + l_T^2)$，与特征长度 $l_F$ 呈线性关系，从而使得利用高分辨率特征成为可能。

### 3.3 SMPL 目标表示：紧凑参数化

解耦注意力的效率优势需要与紧凑的目标表示配合才能充分发挥。现有方法使用基于顶点的表示，目标嵌入长度 $l_T = 6890$（对应 SMPL 网格的全部顶点），即使采用解耦注意力，$\mathcal{O}(l_F l_T)$ 项仍随顶点数线性增长。

SMPLer 引入基于 SMPL 参数化人体模型的紧凑目标表示 $T \in \mathbb{R}^{(H+2) \times d}$，其中 $H = 24$ 为人体关节数。前 $H$ 行对应 $H$ 个身体部件的旋转姿态嵌入，后两行分别对应形状参数嵌入和相机参数嵌入。该表示将 $l_T$ 从 $6890$ 压缩至 $26$，与解耦注意力协同作用，大幅降低计算量。

SMPL 网格顶点 $Y \in \mathbb{R}^{N \times 3}$（$N = 6890$）由姿态参数 $\theta$ 和形状参数 $\beta$ 通过 SMPL 函数生成：

$$Y = f_{\mathrm{SMPL}}(\theta, \beta) \tag{Eq. 4}$$

三维关节 $J \in \mathbb{R}^{H \times 3}$ 由顶点线性映射得到：

$$J = \mathcal{M} Y \tag{Eq. 5}$$

其中 $\mathcal{M}$ 为预定义的回归矩阵。二维关节通过弱透视投影获得：

$$\mathcal{I} \in \mathbb{R}^{H \times 2} = \Pi_C(J) \tag{Eq. 6}$$

### 3.4 多尺度注意力

为同时利用高分辨率特征的精细空间信息与低分辨率特征的语义上下文，SMPLer 提出多尺度注意力（Multi-Scale Attention）。给定 CNN 骨干（HRNet）提取的 $S$ 个尺度的特征图 $\mathcal{F} = \{F_1, F_2, \dots, F_S\}$（$F_1$ 分辨率最高），多尺度注意力定义为各尺度交叉注意力的平均：

$$h_{\mathrm{ms}}(\mathcal{T}, \mathcal{F}) = \frac{1}{S} \sum_{i=1}^{S} h_{\mathrm{cross}}(\mathcal{T}, F_i) \tag{Eq. 8}$$

每个尺度使用独立的投影权重 $W_q, W_k, W_v$，输出为所有尺度响应的均值。该设计使目标嵌入能同时感知全局语义和局部细节。

为保持不同尺度间的空间对应关系，多尺度位置编码采用池化策略：仅对最高分辨率特征学习位置编码 $\phi_1$，低尺度编码通过对 $\phi_1$ 进行步长为 $2^{i-1}$ 的平均池化获得：

$$\phi_i = f_{\mathrm{pool}}^{(2^{i-1})}(\phi_1) \tag{Eq. 9}$$

或等价地迭代执行步长为 2 的池化：$\phi_i = f_{\mathrm{pool}}^{(2)}(\phi_{i-1})$。这保证了相似空间位置在不同尺度上具有相似的位置嵌入。

### 3.5 关节感知注意力

多尺度注意力提供全局上下文，但对关节周围的局部细节不够敏感。SMPLer 引入关节感知注意力（Joint-Aware Attention），将每个关节嵌入 $\mathcal{T}_i$ 的交叉注意力限制在最高分辨率特征图 $F_1$ 上以该关节投影位置为中心的 $r \times r$ 局部块 $\mathcal{N}(\mathcal{T}_i)$ 内：

$$h_{\mathrm{ja}}(\mathcal{T}_i, \mathcal{F}) = f_{\mathrm{soft}}\left(\frac{(\mathcal{T}_i W_q)(F_1^{\mathcal{N}(\mathcal{T}_i)} W_k)^\top}{\sqrt{d}} + \eta\right)(F_1^{\mathcal{N}(\mathcal{T}_i)} W_v) \tag{Eq. 10}$$

其中 $\eta$ 为局部相对位置编码。该操作使模型能精确捕捉关节附近的纹理和几何线索。

### 3.6 组合注意力与最终模块

对于前 $H$ 个姿态嵌入，组合注意力取关节感知注意力与多尺度注意力的均值；对于形状和相机嵌入（$i > H$），仅使用多尺度注意力：

$$h_{\mathrm{co}}(\mathcal{T}_i, \mathcal{F}) = \begin{cases} \frac{1}{2}(h_{\mathrm{ja}}(\mathcal{T}_i, \mathcal{F}) + h_{\mathrm{ms}}(\mathcal{T}_i, \mathcal{F})), & i \le H \\ h_{\mathrm{ms}}(\mathcal{T}_i, \mathcal{F}), & i > H \end{cases} \tag{Eq. 11}$$

最终注意力模块将组合注意力与目标自注意力级联：

$$h_{\mathrm{final}}(\mathcal{T}, \mathcal{F}) = h_{\mathrm{self}}(h_{\mathrm{co}}(\mathcal{T}, \mathcal{F})) \tag{Eq. 12}$$

### 3.7 分层迭代架构

整个 Transformer 采用分层架构，包含 $B$ 个 Transformer Block，每个 Block 包含 $U$ 个 Transformer Unit（每个 Unit 对应 $h_{\mathrm{final}}$）。给定初始 SMPL 参数估计 $P^0$，第 $b$ 个 Block 的更新过程为：

$$\mathcal{T}^b = f_{\mathrm{TB}}^b(\mathcal{T}^{b-1}, P^{b-1}, \mathcal{F}), \quad P^b = f_{\mathrm{fusion}}(\mathcal{T}^b, P^{b-1}) \tag{Eq. 13}$$

其中 $f_{\mathrm{TB}}^b$ 为第 $b$ 个 Transformer Block，$f_{\mathrm{fusion}}$ 为融合层，通过残差加法将当前估计叠加到 SMPL 参数上，实现渐进式优化。每个 Block 内部通过二维关节回归模块（J-Reg）从三维估计计算二维关节位置，为后续迭代提供空间锚点。默认配置为 $B=3, U=2$。

### 3.8 损失函数

训练损失包含标准的三维关节误差、二维关节重投影误差及 SMPL 参数正则化。其中旋转正则化损失定义为预测旋转矩阵与真值之间的 L1 损失：

$$\ell_{\mathrm{rotation}} = w_R \cdot \frac{1}{H} \sum_{i=1}^{H} \| R_{\theta_i} - \hat{R}_{\theta_i} \|_1 \tag{Eq. 14}$$

权重 $w_R = 50$。该损失直接监督 SMPL 目标表示中的姿态嵌入，确保解耦注意力学习到有意义的身体部件旋转。

### 补充图表

![[assets/figures/papers/paper_list_l1649_SMPLer_Taming_Transformers_for_Monocular_3D_Human_Shape_and_Pose_Estimat/figures/003_Figure_3.jpg]]
*Figure 3: Hierarchical architecture of our Transformer. (a) shows an overview of the hierarchical architecture which corresponds to the “Transformer” in Figure 2. With the image features*

![[assets/figures/papers/paper_list_l1649_SMPLer_Taming_Transformers_for_Monocular_3D_Human_Shape_and_Pose_Estimat/figures/006_Figure_6.jpg]]
*Figure 6: Illustration of the joint-aware attention that aggregates local features around human joints. See more details in Sec. 3.4*

![[assets/figures/papers/paper_list_l1649_SMPLer_Taming_Transformers_for_Monocular_3D_Human_Shape_and_Pose_Estimat/figures/001_Figure_1.jpg]]
*Figure 1: Two key designs of the proposed Transformer. The sub-caption “A-B” denotes the attention form “A” and the target representation “B”, respectively. The vertical and horizontal lines around the rectangles represent query and key in the attention operation. Red indicates source image features, blue indicates target output representation, and the colors within the rectangles represent the interactions between them. (a) Existing Transformers for 3D human reconstruction [1], [2] typically adopt a ViT-style full attention operation and a vertex-based target representation, hindering the utilization of high-resolution image features. In contrast, we propose a decoupled attention (b) and an SMPL-bas...*

![[assets/figures/papers/paper_list_l1649_SMPLer_Taming_Transformers_for_Monocular_3D_Human_Shape_and_Pose_Estimat/figures/004_Figure_4.jpg]]
*Figure 4: Jointly exploiting multi-scale features in the attention operation (see Eq. 8 for more explanations)*

![[assets/figures/papers/paper_list_l1649_SMPLer_Taming_Transformers_for_Monocular_3D_Human_Shape_and_Pose_Estimat/figures/005_Figure_5.jpg]]
*Figure 5: Pooling-based multi-scale positional encoding. We learn the positional encoding only for the highest-resolution feature, and the encodings for other scales are generated by average pooling, such that similar spatial locations across different scales have similar positional embeddings*

![[assets/figures/papers/paper_list_l1649_SMPLer_Taming_Transformers_for_Monocular_3D_Human_Shape_and_Pose_Estimat/figures/007_Figure_7.jpg]]
*Figure 7: Combining the joint-aware and multi-scale attention. Note that only the first H rows of T are averaged in the “Average” operation (see Eq. 11 for more details)*



## 实验与关键发现

### 核心性能对比

SMPLer在单目三维人体重建的两个主流基准上均取得领先性能。在Human3.6M数据集上，基础版SMPLer的MPJPE为47.0 mm，PA-MPJPE为32.8 mm；大模型版SMPLer-L进一步将MPJPE降至**45.2 mm**，PA-MPJPE降至**32.4 mm**（Table 1）。与先前最优的基于Transformer的顶点回归方法**Mesh Graphormer**（Lin et al., ICCV 2021）相比，SMPLer-L的MPJPE改善超过10%（51.2→45.2 mm），参数量却不到其三分之一。在户外场景数据集3DPW上，SMPLer-L同样表现优异：MPJPE 73.7 mm，PA-MPJPE 43.4 mm，MPVE 82.0 mm，全面超越Mesh Graphormer（Table 1）。

![[assets/figures/papers/paper_list_l1649_SMPLer_Taming_Transformers_for_Monocular_3D_Human_Shape_and_Pose_Estimat/figures/008_Table_1.jpg]]

效率方面优势更为显著（Table 7）：SMPLer在NVIDIA Tesla M40 GPU上达到**96.0 fps**的推理速度，GFlops仅**8.7**；相比之下，Mesh Graphormer仅34.6 fps，GFlops高达45.4。SMPLer速度提升2.8倍，计算量降低5.2倍，验证了解耦注意力设计带来的线性复杂度优势。

### 关键设计消融

#### 解耦注意力与SMPL目标表示

Table 2系统比较了注意力操作与目标表示的不同组合。全注意力+顶点表示（a）是现有方法的标配，但GPU内存和计算量极高。全注意力+SMPL表示（b）和顶点表示+解耦注意力（c）因内存需求过大甚至无法以合理批量训练。**解耦注意力+SMPL表示**（d，即SMPLer默认配置）在GPU内存、GFlops和精度三个维度上全面占优，实现47.0 MPJPE。这一结果直接验证了论文的核心因果机制：去除特征-特征交互（解耦注意力）并将目标嵌入从6890个顶点压缩至26个SMPL参数嵌入，使Transformer能高效利用高分辨率特征，从而同时获得精度和效率收益。

#### 多尺度注意力

Table 3显示，仅使用单一尺度特征（S=1）时MPJPE为48.4 mm；逐步增加尺度数量，性能持续提升，使用全部四个尺度（S=4）时MPJPE降至**47.0 mm**，相对改善1.4 mm。这一结果表明，高分辨率特征提供精细空间定位，低分辨率特征提供全局上下文，两者互补。Figure 14通过KL散度分析进一步揭示：不同尺度的注意力分布差异显著，高尺度注意力更集中于细粒度特征，低尺度注意力更弥散，验证了多尺度融合的必要性。

#### 位置编码策略

Table 4比较了三种位置编码方案：无位置编码、各尺度独立学习编码、以及论文提出的**池化生成多尺度编码**。池化方案（φ_i = pool(φ_1)）使MPJPE相对降低约1.5 mm，优于其他方案。其原理在于：通过对最高分辨率编码进行平均池化获得低尺度编码，使得不同尺度下相同空间位置的嵌入保持相似，从而促进跨尺度注意力的一致性。

#### 关节感知注意力

Table 5的消融显示，移除关节感知注意力后MPJPE从47.0退化至**51.4 mm**（+4.4 mm），PA-MPJPE从32.8升至34.5（+1.7 mm）。这表明局部关节区域的特征对于精确姿态估计至关重要——全局多尺度注意力虽然覆盖广，但缺乏对关节邻域的精细感知。关节感知注意力通过在关节周围r×r局部块内进行交叉注意力，有效补充了这一局部信息。

#### 分层架构超参数

Table 6探索了Transformer块数B和每块单元数U的影响。默认配置B=3, U=2提供最佳性能（47.0 MPJPE）。增加块数或单元数收益递减，表明三层迭代已能充分渐进优化姿态估计，更深架构可能导致过拟合或优化困难。Figure 12可视化展示了三个Block的渐进优化过程：初始估计粗糙，经过三个Block逐步修正为精确的三维人体网格。

### 失败模式与局限性

尽管SMPLer在精度和效率上均表现优异，论文明确指出以下局限：

1. **混合架构依赖**：SMPLer仍采用CNN骨干（HRNet）+ Transformer的混合架构，尚未探索完全基于注意力的骨干网络（如Swin Transformer、HRFormer），这可能限制进一步的效率提升。
2. **任务泛化未验证**：方法仅针对人体重建设计，虽然理论上可通过替换SMPL为SMAL或MANO扩展到动物或手部重建，但缺乏实验验证。
3. **复杂场景鲁棒性未知**：训练依赖大量标注数据，对严重遮挡和多人交互场景的鲁棒性未进行深入评估。这些场景下关节感知注意力的局部块可能无法正确关联到对应人体部位。
4. **SMPL流形约束的边界**：Figure 10展示了SMPLer始终在SMPL流形上输出结果的优势，但这也意味着模型无法表达超出SMPL模型能力范围的细节（如衣物、头发），对需要精细几何的应用场景可能不足。

### 开放问题

论文提出了三个值得后续探索的方向：能否将解耦注意力和多尺度/多范围注意力推广到运动估计、图像复原等其他视觉任务？通过直接替换参数化模型，该方法能否零样本迁移到动物或手部重建？在SMPLer中用纯注意力骨干替换CNN能否进一步提升性能？这些问题目前尚无实验答案，需后续工作验证。

### 补充图表

![[assets/figures/papers/paper_list_l1649_SMPLer_Taming_Transformers_for_Monocular_3D_Human_Shape_and_Pose_Estimat/figures/016_Table_2.jpg]]

![[assets/figures/papers/paper_list_l1649_SMPLer_Taming_Transformers_for_Monocular_3D_Human_Shape_and_Pose_Estimat/figures/018_Table_5.jpg]]

![[assets/figures/papers/paper_list_l1649_SMPLer_Taming_Transformers_for_Monocular_3D_Human_Shape_and_Pose_Estimat/figures/021_Table.jpg]]



## 定位与知识库关联

### 1. 问题定位：Transformer在三维人体重建中的瓶颈

单目三维人体重建领域的方法可大致分为两类：基于卷积神经网络（CNN）的SMPL参数回归方法和基于Transformer的顶点回归方法。**SPIN**（Kolotouros et al., ICCV 2019）和**VIBE**（Kocabas et al., CVPR 2020）等CNN方法直接预测SMPL的姿态参数$\theta$和形状参数$\beta$，计算效率高但精度受限。近年，**METRO**（Lin et al., CVPR 2021）和**Mesh Graphormer**（Lin et al., ICCV 2021）等Transformer方法转向直接回归6890个网格顶点，取得了更高的重建精度，成为该领域的新基准。

然而，这些基于Transformer的方法继承了ViT式全注意力操作的一个根本性瓶颈：**计算与内存复杂度随特征长度呈二次增长**。在全注意力机制下，目标嵌入$T$与图像特征$F$被拼接后进行自注意力：

$$h_{\mathrm{self}}(T \parallel F)$$

其复杂度为$\mathcal{O}((l_F + l_T)^2)$。当$l_T = 6890$（顶点数）且$l_F$较大（高分辨率特征图的空间尺寸）时，计算开销变得难以承受。这迫使现有方法只能使用最低分辨率的特征图$F_S$，丢弃了高分辨率特征中对精确重建至关重要的细粒度空间信息。

SMPLer正是在这一瓶颈点上切入，通过两个协同设计从根本上改变了复杂度结构。

### 2. 核心改进：解耦注意力与SMPL目标表示

SMPLer的核心创新在于将**注意力操作**和**目标表示**两个维度同时重构，形成互补的降复杂度方案。

**注意力操作的重构**：将全注意力解耦为目标-特征交叉注意力和目标-目标自注意力的级联：

$$h_{\mathrm{self}}(h_{\mathrm{cross}}(T, F))$$

这一操作去除了特征-特征交互，复杂度降至$\mathcal{O}(l_F l_T + l_T^2)$，对特征长度$l_F$呈线性关系。这意味着即使使用高分辨率特征，计算量也仅线性增长而非二次爆炸。

**目标表示的重构**：将基于6890个顶点的表示替换为基于SMPL参数的紧凑表示，仅需$H+2 = 26$个嵌入（$H=24$个身体部件旋转嵌入 + 1个形状嵌入 + 1个相机嵌入）。这使得$l_T$从6890骤降至26，进一步压缩了交叉注意力项$l_F l_T$和自注意力项$l_T^2$。

Table 2的消融实验（Table 2(d)）验证了这一组合的效力：解耦注意力+SMPL表示在GPU内存、计算量（GFlops）和精度（47.0 MPJPE）三个维度上全面优于全注意力+顶点表示的基线配置。值得注意的是，全注意力+顶点表示（Table 2(a)）的GPU内存需求过大，甚至无法以合理的批量大小进行训练。

### 3. 多尺度与多范围信息利用

在降低复杂度以释放高分辨率特征使用能力之后，SMPLer进一步设计了两个互补的注意力机制来充分利用这些特征。

**多尺度注意力**（Section 3.3.1）：对$S$个不同分辨率的特征图分别执行交叉注意力，并对输出取平均：

$$h_{\mathrm{ms}}(\mathcal{T}, \mathcal{F}) = \frac{1}{S} \sum_{i=1}^{S} h_{\mathrm{cross}}(\mathcal{T}, F_i)$$

各尺度使用独立的投影权重，使模型能同时捕获全局语义和局部细节。Table 3显示，使用全部四个尺度（$S=4$）相比单尺度（$S=1$）将MPJPE从48.4降至47.0，验证了多尺度信息互补的价值。

**关节感知注意力**（Section 3.4）：针对姿态估计的局部敏感性需求，在最高分辨率特征图上以每个关节为中心取$r \times r$局部块进行交叉注意力：

$$h_{\mathrm{ja}}(\mathcal{T}_i, \mathcal{F}) = f_{\mathrm{soft}}\left(\frac{(\mathcal{T}_i W_q)(F_1^{\mathcal{N}(\mathcal{T}_i)} W_k)^\top}{\sqrt{d}} + \eta\right)(F_1^{\mathcal{N}(\mathcal{T}_i)} W_v)$$

其中引入相对位置编码$\eta$以增强空间感知。Table 5显示，去除关节感知注意力导致MPJPE从47.0退化至51.4（+4.4mm），PA-MPJPE从32.8升至34.5（+1.7mm），证实了局部精细特征对精确关节定位的关键作用。

最终的组合注意力对姿态部分（前$H$行）平均全局多尺度和局部关节注意力，对形状/相机部分（后2行）仅使用多尺度注意力：

$$h_{\mathrm{co}}(\mathcal{T}_i, \mathcal{F}) = \begin{cases} \frac{1}{2}(h_{\mathrm{ja}}(\mathcal{T}_i, \mathcal{F}) + h_{\mathrm{ms}}(\mathcal{T}_i, \mathcal{F})), & i \le H \\ h_{\mathrm{ms}}(\mathcal{T}_i, \mathcal{F}), & i > H \end{cases}$$

### 4. 与基线方法的关系定位

| 方法 | 范式 | 目标表示 | 注意力类型 | 特征使用 | 核心限制 |
|------|------|----------|------------|----------|----------|
| **SPIN** (Kolotouros et al., ICCV 2019) | CNN + 迭代优化 | SMPL参数 | 无 | 单尺度 | 精度受限 |
| **VIBE** (Kocabas et al., CVPR 2020) | CNN + 时序 | SMPL参数 | 无 | 单尺度 | 依赖视频输入 |
| **METRO** (Lin et al., CVPR 2021) | Transformer | 顶点（6890） | 全注意力 | 单尺度（低分辨率） | 二次复杂度 |
| **Mesh Graphormer** (Lin et al., ICCV 2021) | Transformer + 图卷积 | 顶点（6890） | 全注意力 | 单尺度（低分辨率） | 二次复杂度，参数多 |
| **SMPLer** (本文) | Transformer | SMPL参数（26） | 解耦注意力 | 多尺度（4层） | 混合架构，未验证跨任务泛化 |

**与Mesh Graphormer的直接对比**：SMPLer在Human3.6M上MPJPE为45.2mm，较Mesh Graphormer的51.2mm改善超过10%，参数量不到其三分之一。在推理效率上，SMPLer达到96.0 fps，GFlops仅8.7，比Mesh Graphormer快2.8倍且计算量低5.2倍（Table 7）。这一精度-效率的双重提升源于解耦注意力从根本上改变了复杂度结构，使高分辨率多尺度特征的使用成为可能。

**与SMPL参数回归方法的区别**：虽然SMPLer也输出SMPL参数，但其核心推理引擎是Transformer而非CNN，且通过迭代分层架构（$B=3$个块，每块$U=2$个单元）逐步优化估计，这与SPIN等CNN方法的一次性回归有本质区别。

### 5. 适用边界与局限

**已验证的适用场景**：
- 单目图像的三维人体姿态与形状重建
- 标准数据集（Human3.6M室内、3DPW室外）的受控评估
- 虚拟化身控制等下游应用（Figure 11展示了SMPL流形约束带来的直接可控性优势）

**已知局限**：

1. **混合架构依赖**：SMPLer仍采用CNN骨干（HRNet）+ Transformer的混合架构，未探索完全基于注意力的骨干网络。这留下了性能提升空间，但同时也意味着该方法可以即插即用地替换骨干网络。

2. **任务特化设计**：当前的解耦注意力、关节感知注意力等模块专为人体重建设计，尚未扩展到动物重建（如SMAL模型）或手部重建（如MANO模型）等其他铰接式物体重建任务。

3. **监督训练依赖**：方法需要大量标注数据（配对图像与三维真值）进行监督训练，对复杂遮挡和多人场景的鲁棒性未在论文中进行深入评估。

4. **超参数敏感性**：Table 6显示分层架构中$B=3, U=2$为最优配置，增加块数或单元数收益递减。这表明模型容量与性能之间存在饱和点，但不同数据集或场景下是否需要重新调优尚未验证。

### 6. 开放问题与后续方向

1. **跨任务泛化**：能否将解耦注意力和紧凑目标表示的设计范式推广到其他视觉任务？论文提出通过替换SMPL为SMAL或MANO可直接用于动物或手部重建，但这需要实验验证。

2. **纯注意力骨干**：用纯注意力骨干（如Swin Transformer、HRFormer）替换CNN骨干能否进一步提升性能？这涉及到完全统一的Transformer架构，可能进一步简化设计并提升特征质量。

3. **弱监督与自监督扩展**：当前方法依赖强监督，能否利用多视角一致性、时序约束或扩散模型先验减少标注依赖，是实际部署中的重要方向。

4. **多人场景与遮挡处理**：论文未评估多人交互和严重遮挡场景下的鲁棒性，这是从实验室走向实际应用必须解决的问题。



## 原文 PDF

![[paperPDFs/TPAMI_2024/SMPLer_Taming_Transformers_for_Monocular_3D_Human_Shape_and_Pose_Estimation.pdf]]
