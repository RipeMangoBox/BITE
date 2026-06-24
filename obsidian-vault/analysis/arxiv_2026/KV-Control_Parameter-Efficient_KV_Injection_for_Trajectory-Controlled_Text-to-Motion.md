---
title: "KV-Control: Parameter-Efficient K/V Injection for Trajectory-Controlled Text-to-Motion"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/KV-Control_Parameter-Efficient_KV_Injection_for_Trajectory-Controlled_Text-to-Motion.pdf
project_link: null
code_link: null
aliases:
- KC
- KV-Control
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 在冻结骨干的每一层自注意力中，将轨迹信号作为附加的键/值记忆（K/V injection）注入，而非修改运动令牌查询流或仅作用于输出侧。
primary_logic: 将连续几何约束编码为部位‑时间索引的键/值记忆，在自注意力内部实现记忆检索式控制；通过PartVQ解剖部位化编码和T‑Concat序列展开，使每个（帧,部位）令牌成为注意力可寻址的显式站点，从而让低秩K/V注入能在不干扰文本交叉注意力和冻结骨干的前提下精确调制相关自由度。
claims:
- KV-Control在1.5M机制参数下，骨盆轨迹误差达0.40 cm，多关节误差0.71 cm，约为相同骨干的ControlNet式分支参数量的1/26。
- 将控制信号注入键/值侧而非查询侧，保持运动令牌查询序列逐点不变，从而保护文本交叉注意力。
- 移除K/V注入仅采用精炼循环时，FID恶化至~104，证明适配器而非精炼循环本身提供了维持运动流形的结构条件。
- HumanML3D 上 Avg. Pos. Err. (cm) 骨盆单关节 = 0.40 (M3)
---

# KV-Control: Parameter-Efficient K/V Injection for Trajectory-Controlled Text-to-Motion

> [!tip] 核心洞察
> 将连续几何约束编码为部位‑时间索引的键/值记忆，在自注意力内部实现记忆检索式控制；通过PartVQ解剖部位化编码和T‑Concat序列展开，使每个（帧,部位）令牌成为注意力可寻址的显式站点，从而让低秩K/V注入能在不干扰文本交叉注意力和冻结骨干的前提下精确调制相关自由度。

| 字段 | 内容 |
|------|------|
| 中文题名 | KV-Control：面向轨迹控制的文本到动作生成的参数高效K/V注入方法 |
| 英文题名 | KV-Control: Parameter-Efficient K/V Injection for Trajectory-Controlled Text-to-Motion |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2606.05624) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | KV-Control |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，Avg. Pos. Err. (cm) 骨盆单关节 0.40 (M3) vs 0.72 (MaskControl) (-0.32)；Avg. Pos. Err. (cm) 多关节 0.71 (M3) vs 0.72 (MaskControl) (-0.01)；FID (骨盆 M3) 0.065 vs 0.064 (MaskControl M2? see Table 4) (+0.001)。

## 概述

文本到动作生成中，为用户提供精确的空间轨迹控制是使生成结果可用的关键需求。现有轨迹控制器面临一个根本性瓶颈：**参数开销与推理成本之间的失衡**。以 **OmniControl**（Xie et al., ICLR 2024）和 **InterControl**（Wang et al., NeurIPS 2024）为代表的 ControlNet 式方法复制骨干网络以恢复逐层注意力，导致参数冗余（通常占骨干的 40–100%）；而 **MaskControl**（Pinyoanuntapong et al., ICCV 2025）将控制负担转移至测试时优化，使每样本推理成本急剧上升。两类方法均未能在极小参数占比下实现高精度、保持文本先验的逐层控制。

KV-Control 的核心洞察在于：**将连续几何约束编码为部位‑时间索引的键/值记忆，在自注意力内部实现记忆检索式控制**。具体而言，该方法在冻结骨干的每一层自注意力中，将轨迹信号作为附加的键/值伪令牌（K/V injection）注入，而非修改运动令牌的查询流或仅在输出侧施加约束。这一设计使得控制适配器的角色从“重建注意力通路”缩减为“学习每层应附加何种控制记忆”，从而将可训练的轨迹控制机制参数量压缩至 **1.5M**——约为相同骨干下 ControlNet 式复制分支参数量的 **1/26**。

为实现这一注入机制，KV-Control 协同设计了两个基底组件：**PartVQ** 将人体运动分解为 Q 个解剖部位的离散码本（Q=6），使每个部位获得独立的潜在表示；**T‑Concat** 将 Q 个部位码本沿序列轴展开，令每个（帧, 部位）令牌成为注意力可寻址的显式站点。这一令牌布局为低秩 K/V 注入提供了精确的解剖自由度调制能力，同时保持文本交叉注意力和骨干权重完全冻结。

在 HumanML3D 基准上，采用 MaskControl 评估协议，KV-Control 以 1.5M 机制参数实现**骨盆单关节轨迹误差 0.40 cm、多关节误差 0.71 cm** 的亚厘米级精度，与 MaskControl 的最优配置持平或更优，同时保持与无条件生成相当的 FID（0.065）和文本匹配分数（Top-3 0.799）。消融实验揭示了两个关键因果机制：（1）T‑Concat 布局是精度的必要条件——相同骨干下 C‑Concat 布局的骨盆误差高达 0.90 cm；（2）K/V 适配器提供了维持运动流形的结构条件——移除适配器仅依赖精炼循环时，位置误差可降至 ~0.01 cm，但 FID 崩塌至 103.86，表明精炼本身无法替代适配器提供的生成先验约束。

在方法谱系中，KV-Control 区别于三类现有轨迹控制范式：（1）ControlNet 式复制分支（OmniControl、InterControl），其参数开销与骨干规模线性相关；（2）测试时优化（MaskControl），其将计算成本转移至推理阶段；（3）分部位 VQ 码字优化（**TLControl**，Wan et al., ECCV 2024），其控制发生在潜在空间而非注意力内部。KV-Control 通过“冻结骨干 + 低秩 K/V 注入”的设计，在参数效率、推理速度和精度之间取得了新的平衡点，同时保持了文本先验的完整性——因为运动令牌查询序列逐点不变，文本交叉注意力完全不受干扰。

## 背景与动机

### 文本到动作生成中的轨迹控制困境

文本到动作生成（Text-to-Motion）旨在从自然语言描述合成逼真的三维人体运动序列。近年来，基于离散潜在空间（如VQ-VAE）的掩码Transformer骨干在这一任务上取得了显著进展，能够在保持文本-运动语义对齐的同时生成多样化的运动。然而，纯文本接口缺乏对空间轨迹的精确约束能力——用户无法指定“绕圈行走”的半径、无法控制手腕在特定时刻的位置——这严重限制了生成式运动模型在动画制作、游戏开发和交互式角色控制等实际场景中的应用。

为解决这一问题，近年来涌现了一批轨迹控制器。它们的基本思路是在预训练运动生成骨干之上附加控制模块，使模型在采样过程中接收用户指定的关键点三维轨迹（如骨盆路径、手腕位置序列），并生成满足这些空间约束的运动序列。然而，现有方案在**参数开销与推理成本之间陷入了系统性权衡**。

### 现有方法的两种路径及其瓶颈

当前轨迹控制方法可归为两类技术路线，二者均存在根本性局限：

**复制分支路线**（ControlNet式）：以 **OmniControl**（Xie et al., ICLR 2024）、**InterControl**（Wang et al., NeurIPS 2024）为代表，这类方法复制预训练运动骨干的全部或大部分Transformer层，在复制分支中注入控制信号，通过零初始化卷积/注意力层逐步将控制信息融合到主干。这一策略的代价是参数冗余——复制分支的参数量通常达到骨干的40%–100%，对于118M参数的T-Concat骨干而言意味着数十兆的额外可训练参数。**MaskControl**（Pinyoanuntapong et al., ICCV 2025）同样采用复制分支架构，虽然在推理时引入了精炼循环以提升控制精度，但参数开销问题并未缓解。

**测试时优化路线**：以 **TLControl**（Wan et al., ECCV 2024）为代表，这类方法在推理阶段对运动令牌的VQ码字进行逐样本优化，将轨迹误差作为目标函数反向传播更新离散令牌。虽然避免了大规模可训练参数的存储，但将计算成本完全转移到了推理端——每生成一个样本都需要运行数十步梯度优化，导致单样本延迟显著增加，难以满足实时交互需求。

上述两条路线的共同缺陷在于：**它们均未能在极小参数占比（如骨干的1%量级）下实现高精度、保持文本先验的逐层控制**。复制分支路线在参数效率上存在根本浪费——为每一层复制整个自注意力模块，而实际需要的可能仅是向注意力机制注入少量控制记忆；测试时优化路线则在推理效率上不可持续。

### 核心洞察：记忆检索式控制

KV-Control的核心洞察源于对自注意力机制中**查询（Query）与键/值（Key/Value）角色不对称性**的重新审视。在冻结的预训练运动Transformer中，运动令牌的查询流承载着“当前令牌需要从上下文中检索什么信息”的语义，而键/值侧则构成了“可供检索的记忆库”。如果控制信号被注入查询侧，将改变运动令牌的检索意图，进而干扰文本交叉注意力中已经建立的运动-语义对齐；但如果将控制信号作为附加的键/值记忆注入，则相当于在记忆库中增加了“轨迹约束锚点”，运动令牌可以在不改变自身查询意图的前提下，自然地关注这些约束站点。

基于此，KV-Control提出了一种**参数高效的K/V注入**策略：在冻结骨干的每一层自注意力中，将连续几何约束编码为部位-时间索引的键/值伪令牌，附加到原有的键/值序列中，同时保持运动令牌查询流、文本交叉注意力和前馈网络完全冻结。这一设计将控制适配器的角色从“学习如何修改骨干行为”简化为“学习在每层添加什么控制记忆”，使机制参数量压缩至1.5M——约为相同骨干下ControlNet式复制分支参数量的1/26。

### 令牌布局的结构性支撑

K/V注入的高效性依赖于一个关键的结构性前提：**每个受控自由度必须在注意力机制中具有可寻址的显式站点**。为此，KV-Control协同设计了两个基底组件：

- **PartVQ**（§3.1）：将人体运动按解剖部位分解为Q个独立的离散码本（Q=6，对应躯干、左臂、右臂、左腿、右腿及根关节），使每个部位的局部运动模式在潜在空间中形成紧凑的表示。
- **T-Concat**（§3.2）：将Q个部位码本沿序列轴展开，使每个（帧, 部位）组合成为一个独立的注意力令牌。这意味着一帧运动不再被压缩为单个令牌，而是展开为Q个部位令牌，每个令牌在自注意力中都是可独立寻址的站点。

T-Concat布局是K/V注入得以精确控制的关键：当轨迹约束仅涉及骨盆时，注入的键/值伪令牌可以自然地与骨盆对应的令牌子集交互，而不会干扰其他部位令牌的注意力模式。实验表明，若将T-Concat替换为传统的通道拼接布局（C-Concat，每帧一个令牌），相同20层骨干下骨盆轨迹误差从0.40 cm急剧上升至0.90 cm（Table 2），验证了令牌布局对控制精度的结构性影响。

### 研究目标与核心贡献

KV-Control旨在回答一个核心问题：**能否在保持预训练运动先验完整性的前提下，以极小的参数增量实现高精度的逐层轨迹控制？** 其核心贡献可归纳为三点：

1. **K/V注入范式**：将控制信号作为附加键/值记忆注入每层自注意力，而非修改查询流或复制骨干层，在1.5M机制参数下实现骨盆误差0.40 cm、多关节误差0.71 cm的亚厘米级控制精度。
2. **PartVQ + T-Concat协同基底**：通过解剖部位化编码和序列展开令牌布局，为K/V注入提供可寻址的控制站点，使低秩投影能够精确调制相关自由度而不干扰无关部位。
3. **保持文本先验的结构性保障**：冻结文本交叉注意力和全部骨干权重，确保控制适配器不会破坏预训练阶段建立的文本-运动语义对齐——实验表明，KV-Control在实现精确轨迹跟踪的同时，文本匹配分数（Match.）和运动多样性（Div.）与无条件生成基线保持一致（Table 5）。

## 核心创新

现有轨迹控制方法在参数效率与推理成本之间陷入两难：**MaskControl**（Pinyoanuntapong et al., ICCV 2025）通过复制骨干网络恢复逐层注意力实现控制，但引入大量参数冗余；**OmniControl**（Xie et al., ICLR 2024）和 **InterControl**（Wang et al., NeurIPS 2024）采用 ControlNet 式零初始化复制分支，参数开销通常占骨干的 40–100%；**TLControl**（Wan et al., ECCV 2024）则将成本转移至测试时优化，使每样本推理延迟显著增加。这些方法均未能在极小参数占比下同时实现高精度轨迹跟踪与文本先验保持。

KV-Control 的核心创新在于将控制范式从“复制骨干逐层调制”转变为“记忆检索式注入”，通过三个相互耦合的 changed slots 实现突破：

### 1. 自注意力键/值注入：从查询侧干预到记忆侧附加

传统控制适配器通常修改运动令牌的查询流或仅在输出侧施加条件，这不可避免地干扰文本交叉注意力中已对齐的查询语义。KV-Control 将控制信号作为附加的键/值记忆（K/V injection）注入冻结骨干的每一层自注意力中，而非修改运动令牌查询流。具体而言，每层自注意力的键/值序列由原始运动令牌特征扩展为拼接了控制条件伪令牌 $\mathbf{C}_i^{\mathrm{K}}, \mathbf{C}_i^{\mathrm{V}}$ 的增强序列：

$$\widetilde{\mathbf{K}}_i^{\mathrm{in}} = [\mathbf{X}_i; \bar{\mathbf{C}}_i^{\mathrm{K}}], \quad \widetilde{\mathbf{V}}_i^{\mathrm{in}} = [\mathbf{X}_i; \bar{\mathbf{C}}_i^{\mathrm{V}}]$$

增强后的注意力计算引入可学习的控制列偏置 $\mathbf{B}_i$（初始化为 $b_i = -5$），在控制令牌列上施加单标量偏置，运动令牌列保持零偏置：

$$\mathrm{Attn}_i = \mathrm{softmax}\Big(\frac{\mathbf{Q}_i \widetilde{\mathbf{K}}_i^{\top}}{\sqrt{d_h}} + \mathbf{B}_i\Big) \widetilde{\mathbf{V}}_i$$

这一设计的因果机制在于：**查询侧保持逐点不变，运动令牌查询序列与冻结骨干中的文本交叉注意力完全不受扰动**，从而保护了预训练的文本-运动对齐；控制信号通过键/值侧的附加记忆站点参与注意力竞争，使每个运动令牌查询能够选择性关注相关控制信息，而非被强制改写。

### 2. 令牌布局：从通道拼接（C-Concat）到序列展开（T-Concat）

传统 VQ-VAE 运动表示通常将多部位码本沿通道维度拼接（C-Concat），每帧仅产生一个令牌，导致控制信号无法精确寻址单个解剖部位。KV-Control 提出 T-Concat 布局：将 PartVQ 的 $Q=6$ 个数据驱动部位码本沿序列轴展开，使每个（帧, 部位）成为独立的注意力可寻址令牌。对于 $T_{\mathrm{tok}}=49$ 帧的序列，T-Concat 产生 $S = T_{\mathrm{tok}} \cdot Q = 294$ 个令牌，而 C-Concat 仅产生 49 个。

这一布局转变是 K/V 注入实现高精度控制的结构前提：低秩 K/V 残差可在查询位置选择性调制单个解剖子令牌，而 C-Concat 布局下控制信号被迫作用于整个帧令牌，缺乏部位级精度。消融实验（Table 2）证实了这一点——同一 20 层骨干下，T-Concat 布局的骨盆轨迹误差为 0.40 cm，而 C-Concat 布局高达 0.90 cm。

### 3. 控制适配器类型：从复制分支到低秩 K/V 注入

KV-Control 将适配器的角色从“学习逐层特征变换”简化为“学习每层应添加何种控制记忆”。控制编码器利用当前令牌状态的解码姿态与目标轨迹的残差生成共享控制特征 $\mathbf{f}_{\mathrm{ctrl}}$，随后通过每层的零初始化低秩投影生成键/值伪令牌：

$$\mathbf{h}_i = \mathbf{f}_{\mathrm{ctrl}} \mathbf{W}_i^{\mathrm{down}}, \quad \mathbf{C}_i^{\mathrm{K}} = \mathbf{h}_i \mathbf{W}_i^{\mathrm{K}}, \quad \mathbf{C}_i^{\mathrm{V}} = \mathbf{h}_i \mathbf{W}_i^{\mathrm{V}}$$

参数账本（Table 3）显示，KV-Control 的机制参数仅 1.5M，而相同骨干的 ControlNet 式复制分支（M2 设置）需 39.3M——**参数效率提升约 26 倍**。更关键的是，1.5M 的 K/V 注入在骨盆轨迹误差上达到 0.40 cm，显著优于 39.3M 复制分支的 1.24 cm（Table 2），证明参数效率与精度并非权衡关系，而是通过正确的注入位置和令牌布局实现了协同增益。

### 决定性证据

移除 K/V 适配器仅保留精炼循环的消融实验（Table 5）提供了因果性证据：冻结 T-Concat 骨干配合精炼循环可将位置误差降至 ~0.01 cm，但 FID 崩塌至 103.86。这表明适配器并非仅仅提供轨迹约束，而是**维持了运动流形的结构条件**——K/V 注入在自注意力内部创造了条件化的记忆检索路径，使精炼循环能够在保持生成质量的前提下优化轨迹精度。

## 整体框架

KV-Control 的整体设计围绕一个核心原则展开：**在冻结的运动生成骨干中，通过极低秩的键/值记忆注入实现轨迹控制，而不修改骨干的任何权重或文本交叉注意力**。图 2 给出了单次前向的完整流程，可划分为三个逻辑块。

### 冻结基底：PartVQ + T‑Concat

控制适配器建立在预训练且严格冻结的离散潜在运动基底之上。该基底由两个协同设计的模块构成：

- **PartVQ（§3.1）** 将人体运动分解为 $Q$ 个数据驱动的解剖部位码本（论文取 $Q=6$）。每个码本独立学习对应部位的运动模式，输出部位化的离散令牌。
- **T‑Concat（§3.2）** 将 $Q$ 个部位的码本沿序列轴展开，使每个 $(\text{帧}, \text{部位})$ 成为注意力可寻址的独立令牌。具体而言，若每个部位码本长度为 $T_{\text{tok}}$，则展开后序列长度 $S = T_{\text{tok}} \cdot Q$，形成显式的解剖‑时间网格。

这一令牌布局是整个方法的关键结构条件：它使得后续的低秩 K/V 注入能够**精确调制特定部位在特定帧上的注意力响应**，而不会通过通道混合干扰其他部位。

### 控制侧模块：轨迹编码器与逐层 K/V 注入

控制信号的处理流程如下：

1. **控制编码器** 接收当前令牌状态解码出的姿态与控制目标轨迹之间的残差，输出共享控制特征 $\mathbf{f}_{\text{ctrl}}$。
2. **逐层低秩投影** 将 $\mathbf{f}_{\text{ctrl}}$ 通过零初始化的下投影 $\mathbf{W}_i^{\text{down}}$ 压缩至秩 $r$，再分别上投影为第 $i$ 层的控制键伪令牌 $\mathbf{C}_i^{\text{K}}$ 和控制值伪令牌 $\mathbf{C}_i^{\text{V}}$：

$$
\mathbf{h}_i = \mathbf{f}_{\text{ctrl}} \mathbf{W}_i^{\text{down}}, \quad
\mathbf{C}_i^{\text{K}} = \mathbf{h}_i \mathbf{W}_i^{\text{K}}, \quad
\mathbf{C}_i^{\text{V}} = \mathbf{h}_i \mathbf{W}_i^{\text{V}}
$$

3. **增强自注意力** 将控制伪令牌拼接到原始键/值序列的末端，并引入可学习的控制列偏置 $\mathbf{B}_i$（初始化为 $b_i = -5$，仅作用于控制令牌列）：

$$
\text{Attn}_i = \text{softmax}\!\left(\frac{\mathbf{Q}_i \widetilde{\mathbf{K}}_i^{\top}}{\sqrt{d_h}} + \mathbf{B}_i\right) \widetilde{\mathbf{V}}_i
$$

其中 $\widetilde{\mathbf{K}}_i, \widetilde{\mathbf{V}}_i$ 为拼接了控制令牌的增强键/值序列。

### 冻结路径：查询流与文本交叉注意力

KV-Control 的关键设计选择是**将控制信号注入键/值侧，而非查询侧**。运动令牌的查询序列 $\mathbf{Q}_i$ 保持逐点不变，文本门控交叉注意力模块和 FFN 子层也完全冻结。这意味着：

- 文本‑运动对齐能力得到完整保留，不受控制适配器干扰；
- 骨干网络的所有 118M 权重在控制适配阶段严格冻结，仅训练控制侧的 10.5M 参数（其中 K/V 注入机制本身仅 1.5M）。

### 输出重建

增强后的自注意力输出经冻结的 FFN 和输出头处理后，由 PartVQ 解码器重建为最终的人体运动序列。训练时采用掩码交叉熵损失与 L1 轨迹损失的联合目标：

$$
\mathcal{L}_{\text{KV}} = \lambda_{\text{CE}} \mathcal{L}_{\text{CE}} + \lambda_{\text{traj}} \mathcal{L}_{\text{traj}}
$$

其中轨迹损失计算预测干净令牌的正向运动学结果与目标位置在掩码指示范围内的 L1 误差：

$$
\mathcal{L}_{\text{traj}} = \| \mathbf{m} \odot (\text{FK}(\hat{\mathbf{x}}_0^{\text{out}}) - \mathbf{p}^{\text{tgt}}) \|_1
$$

### 推理工作点

推理时可选择不同强度的测试时优化策略（Table 1），从纯前馈（M0）到动态采样阶段优化（M3），在精度与延迟之间灵活权衡。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_05624/figures/002_Figure_2.jpg]]
*Figure 2: KV-Control method overview. Single-pass left-to-right schematic; full equations and dimensions in §3.1–§3.3. Left: frozen co-designed PartVQ+T-Concat substrate (Q = 6 data-driven body-part codebooks unpacked along the sequence axis) into which motion tokens flow. Middle: per self-attention layer, the motion query stream Q is unchanged and the keys/values K, V are augmented with control-conditioned pseudo-tokens*

## 核心模块与公式推导

### 3.1 PartVQ：解剖部位感知的分区码本

KV‑Control 的控制精度依赖于一个关键设计选择——**令牌布局**必须使每个（帧，部位）成为注意力可寻址的显式站点。为此，方法首先构建 PartVQ，将人体运动分解为 $Q$ 个数据驱动的解剖部位码本。

分区过程基于两个统计量：**逐关节激活度** $a_j(t)$ 定义为关节 $j$ 在时刻 $t$ 相对其父关节的 HumanML3D 特征的 $\ell_2$ 范数，并在整个语料库上标准化；**逐对关节相似度** $s_{jk}$ 定义为小滞后窗口内的绝对最大归一化互相关。算法 1 以这两个量为基础，自底向上合并语义相近且运动耦合度高的关节，最终将 22 关节的 HumanML3D 骨骼划分为 $Q = 6$ 个部位（如躯干、左臂、右臂、左腿、右腿等），每个部位对应一个独立的 VQ 码本。

每个部位码本将对应关节的运动特征量化为离散令牌序列，从而形成 $Q$ 路并行的令牌表示。这一分区方案是后续 T‑Concat 展开和逐部位 K/V 注入的结构基础。

### 3.2 T‑Concat：沿序列轴展开部位令牌

传统运动 VQ‑VAE 通常将 $Q$ 个部位码本沿通道维度拼接（C‑Concat），每帧产生一个复合令牌，序列长度保持为 $T_{\text{tok}}$。T‑Concat 则**沿序列轴展开**：将 $Q$ 个长度为 $T_{\text{tok}}$ 的部位码本首尾相接，形成 $S = T_{\text{tok}} \cdot Q$ 个维度为 $d_{\text{model}}$ 的独立令牌。

这一布局转变的核心因果机制在于：每个（帧，部位）令牌成为自注意力可独立寻址的单元。当后续 K/V 注入在某一部位对应的令牌位置附加控制记忆时，注意力机制可以**选择性调制该解剖部位的自由度**，而不会通过通道混合污染其他部位的信息。消融实验（Table 2）直接验证了这一点：同一 20 层骨干下，C‑Concat 布局的骨盆轨迹误差为 0.90 cm，而 T‑Concat 降至 0.40 cm。

冻结的 T‑Concat 骨干包含掩码运动 Transformer 的所有自注意力层、文本门控交叉注意力层和前馈网络，总参数量 118 M，在控制适配器训练期间保持严格冻结。

### 3.3 KV‑Control：逐层键/值注入机制

KV‑Control 的核心操作是在冻结骨干的**每一层自注意力中**，将轨迹控制信号作为附加的键/值伪令牌注入，而非修改运动令牌的查询流。

**控制编码器**首先计算控制特征。给定当前令牌状态解码出的姿态，通过正向运动学获得各关节的当前位置，与目标轨迹 $\mathbf{p}^{\text{tgt}}$ 计算残差，经共享的 1D 卷积编码器得到控制特征 $\mathbf{f}_{\text{ctrl}} \in \mathbb{R}^{T_{\text{tok}} \times d_{\text{model}}}$。

**逐层低秩投影**将共享控制特征映射为第 $i$ 层的键/值控制令牌：

$$\mathbf{h}_i = \mathbf{f}_{\text{ctrl}} \mathbf{W}_i^{\text{down}}, \quad \mathbf{C}_i^{\text{K}} = \mathbf{h}_i \mathbf{W}_i^{\text{K}}, \quad \mathbf{C}_i^{\text{V}} = \mathbf{h}_i \mathbf{W}_i^{\text{V}}$$

其中 $\mathbf{W}_i^{\text{down}} \in \mathbb{R}^{d_{\text{model}} \times r}$ 将特征降至秩 $r$，$\mathbf{W}_i^{\text{K}}, \mathbf{W}_i^{\text{V}} \in \mathbb{R}^{r \times d_{\text{model}}}$ 分别上投影为键和值伪令牌。所有投影矩阵均采用零初始化，确保训练初期适配器不干扰冻结骨干的原始行为。

**增强自注意力**将控制令牌拼接到原始键/值序列：

$$\widetilde{\mathbf{K}}_i = [\mathbf{K}_i; \mathbf{C}_i^{\text{K}}], \quad \widetilde{\mathbf{V}}_i = [\mathbf{V}_i; \mathbf{C}_i^{\text{V}}]$$

同时引入可学习的**控制列偏置** $\mathbf{B}_i \in \mathbb{R}^{S \times (S + T_{\text{tok}})}$：运动令牌列偏置为零，控制令牌列偏置为单一可学习标量 $b_i$（初始化为 $-5$，使控制令牌在训练初期近似被抑制）。最终注意力输出为：

$$\text{Attn}_i = \text{softmax}\left(\frac{\mathbf{Q}_i \widetilde{\mathbf{K}}_i^{\top}}{\sqrt{d_h}} + \mathbf{B}_i\right) \widetilde{\mathbf{V}}_i$$

**查询流保护**是该方法的关键安全特性：运动令牌的查询序列 $\mathbf{Q}_i$ 在注入前后逐点保持不变。这意味着文本交叉注意力（以运动令牌为查询、文本嵌入为键/值）的输入完全不受控制信号干扰，从而保护了预训练的文本‑运动对齐。消融实验（Table 5）从反面证明了这一设计的必要性：移除 K/V 适配器仅保留精炼循环时，位置误差虽降至约 0.01 cm，但 FID 崩塌至 103.86，说明适配器提供了维持运动流形的结构条件。

### 3.4 训练目标

KV‑Control 适配器通过联合损失端到端训练：

$$\mathcal{L}_{\text{KV}} = \lambda_{\text{CE}} \mathcal{L}_{\text{CE}} + \lambda_{\text{traj}} \mathcal{L}_{\text{traj}}$$

其中 $\mathcal{L}_{\text{CE}}$ 为标准掩码交叉熵损失，作用于被掩码的运动令牌预测。$\mathcal{L}_{\text{traj}}$ 为轨迹损失：

$$\mathcal{L}_{\text{traj}} = \| \mathbf{m} \odot (\text{FK}(\hat{\mathbf{x}}_0^{\text{out}}) - \mathbf{p}^{\text{tgt}}) \|_1$$

$\hat{\mathbf{x}}_0^{\text{out}}$ 为预测的干净令牌，FK 为正向运动学函数，$\mathbf{p}^{\text{tgt}}$ 为目标位置，$\mathbf{m}$ 为指示哪些帧‑关节受控的掩码。该损失仅在受控部位上计算 L1 误差，引导 K/V 注入学习精确的几何约束调制。

### 参数效率

整个 K/V 注入机制（包括所有层的低秩投影和偏置）仅产生 **1.5 M 可训练参数**。相比之下，同一 T‑Concat 骨干上的 ControlNet 式复制分支需 39.3 M 参数（Table 2），且骨盆误差高达 1.24 cm。完整控制侧训练预算（含共享轨迹编码器的 9 M）为 10.5 M，而骨干 118 M 保持冻结。

## 实验与分析

### 评估协议与工作点配置

为确保公平对比，所有主要结果均采用 **MaskControl**（Pinyoanuntapong et al., ICCV 2025）的评估协议——相同控制目标、指标和测试集。实验在 HumanML3D 数据集上展开，覆盖骨盆单关节轨迹控制和全关节多关节轨迹控制两类任务。核心指标为 **Avg. Pos. Err. (cm)**，即生成位置与目标位置在所有受控关节‑帧对上的平均欧氏距离；辅以 FID、Top‑3 匹配精度、Skate（脚滑动比）、轨迹/位置失败率（>50 cm 占比）以及运动‑文本匹配分数和多样性指标。

论文定义了四个工作点配置（Table 1），以控制推理时的精炼强度与计算量：

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_05624/figures/003_Table_1.jpg]]
*Table 1: Operating points used in evaluation. Stage 1 optimizes motion-token logits during sampling; Stage 2 refines token embeddings after sampling. Dynamic Stage 1 uses*

- **M0**：纯前馈，无测试时优化。
- **M1**：静态 Stage‑1 精炼（每步固定迭代次数）。
- **M2**：与 MaskControl 计算量对齐的动态 Stage‑1 精炼（$n_{\text{iter}}^{(s)} = (s+1) \cdot 35$）。
- **M3**：最强精炼设置，在 M2 基础上追加 Stage‑2 令牌嵌入精炼。

M2 设置下计算量与 MaskControl 对齐，是参数效率对比的主战场；M3 则用于展示方法在最强精炼下的精度上限。所有延迟数据在单张 H100 上测量。

### 主结果：轨迹控制精度与参数效率

Table 4 汇总了 HumanML3D 上单关节与多关节轨迹控制的定量对比。KV‑Control 在 M3 设置下实现骨盆单关节误差 **0.40 cm**，多关节误差 **0.71 cm**，同时仅需 **1.5M** 机制参数——约为同骨干 ControlNet 式复制分支（39.3M）的 1/26。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_05624/figures/006_Table_4.jpg]]
*Table 4: Trajectory control on HumanML3D under the MaskControl evaluation protocol. Upper/lower blocks: single-joint pelvis / all-joints multi-joint. Avg. Pos. Err. (cm) = mean Euclidean distance between generated and target positions over controlled joint-frame targets (shared across all rows); Skate = Foot-Skating Ratio; Traj. E, Loc. E = > 50 cm failure rates (%); MC = MaskControl-matched compute*

| 方法 | 骨盆 Avg. Pos. Err. (cm) | 多关节 Avg. Pos. Err. (cm) | 机制参数量 |
|------|--------------------------|----------------------------|------------|
| KV‑Control (M3, T‑Concat) | **0.40** | **0.71** | 1.5M |
| MaskControl (M2) | 0.72 | 0.72 | — |
| OmniControl | — | — | 复制分支 ≈ 骨干 |
| TLControl | — | — | 部位 VQ 码字优化 |

在 M2 对齐计算量设置下，KV‑Control 同样保持优势：骨盆误差 0.59 cm，显著低于 MaskControl 的 0.72 cm。FID 和 Top‑3 指标上，KV‑Control 与 MaskControl 基本持平（骨盆 M3：FID 0.065 vs. 0.064，Top‑3 0.799 vs. 0.805），表明精度提升并非以牺牲运动质量为代价。

**关键洞察**：KV‑Control 在极小参数占比下实现了高精度轨迹跟踪，其核心机制——将控制信号注入键/值侧而非查询侧——保持了运动令牌查询序列的逐点不变性，从而保护了文本交叉注意力，使文本‑运动对齐不受控制信号干扰。

### 消融实验：骨干布局与适配器机制

Table 2 报告了在同一 20 层 Transformer 骨干上的布局与机制消融，揭示了两个决定性设计选择：

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_05624/figures/004_Table_2.jpg]]
*Table 2: Backbone-layout and mechanism ablations on the same 20-layer trunk. KV-Control is evaluated on T-Concat and C-Concat layouts; the bottom block is a same-substrate duplicated-branch sanity check at the MaskControl-matched M2 protocol. Bold indicates the main configuration*

**T‑Concat vs. C‑Concat 布局**。C‑Concat 将 Q=6 个部位码本沿通道拼接为每帧一个 768 维令牌（S=49），而 T‑Concat 沿序列轴展开为 S=294 个独立令牌，使每个（帧, 部位）成为注意力可寻址的显式站点。在相同 M3 设置下，C‑Concat 的骨盆误差高达 **0.90 cm**，是 T‑Concat（0.40 cm）的 2.25 倍。这说明部位粒度的令牌化是精确空间控制的必要条件：低秩 K/V 注入只有在可寻址到具体解剖部位时，才能选择性调制相关自由度。

**K/V 注入 vs. ControlNet 式复制分支**。在 T‑Concat 骨架上，ControlNet 式零初始化复制分支（M2 协议）需 39.3M 参数，骨盆误差达 **1.24 cm**；而 KV‑Control 仅用 1.5M 机制参数即达 0.59 cm（M2）。这一对比直接验证了“注入优于复制”的核心主张——复制整个骨干的逐层注意力不仅参数冗余，且控制精度反而更差。

**适配器必要性**。Table 5 的纯精炼基线（frozen T‑Concat，移除 K/V 适配器，仅运行 Stage‑1 + Stage‑2 精炼循环）提供了最有力的因果证据：位置误差降至 ~0.01 cm，但 FID 崩塌至 **103.86**（正常水平约 0.06–0.08）。这表明精炼循环本身可以强行拟合目标位置，但会破坏运动流形结构；K/V 适配器提供了保持流形约束的结构条件，使精炼在流形附近搜索而非跳出分布。

### 参数账本与计算效率

Table 3 给出了完整的参数账本。KV‑Control 的轨迹控制机制（K/V 投影 + 控制偏置）仅占 **1,474,560** 参数；完整控制侧可训练预算为 **10.5M**，其中 9M 为共享的轨迹编码器（1D‑Conv）。底层 118M 的 PartVQ + T‑Concat 骨干在控制适配阶段严格冻结。这一参数结构意味着：部署多个控制目标（如不同关节组合）时，只需切换轻量的 K/V 投影权重，骨干和轨迹编码器均可复用。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_05624/figures/001_Figure_1.jpg]]
*Figure 1: KV-Control on PartVQ+T-Concat. Left: pelvis-trajectory error versus trainable trajectory-control mechanism parameters under the MaskControl-matched M2 setting; K/V injection uses mechanism parameters (including the shared trajectory encoder; see Table 3). Right: four out-of-distribution demos from the same trained adapter—walk wave, circle arms high, forward hop wall, and walk heart both hands; markers denote user-supplied targets, mannequin meshes denote generated motion*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_05624/figures/005_Table_3.jpg]]
*Table 3: Parameter accounting on the same frozen 118 M T-Concat masked-transformer motion backbone. Mechanism column = trajectory-control mechanism (Fig. 1 x-axis); Full = Mechanism + shared trajectory encoder*

### 单关节控制能力分析

Table 6 展示了多关节适配器在单关节控制场景下的泛化能力。将受控关节集固定为单一解剖关节（骨盆、左/右腕、左/右踝、头），各关节平均位置误差为 **0.41 cm**，与全关节多关节设置（0.71 cm）相比更低——这符合预期，因为约束更稀疏。值得注意的是，各关节误差分布均匀（0.34–0.48 cm），未出现特定关节退化，说明多关节训练学到的 K/V 记忆具有部位选择性，可在推理时灵活激活。

### 定性结果与分布外泛化

Figure 3 展示了 OOD 轨迹控制的定性结果：同一骨盆单关节 K/V 控制检查点在八个字母形目标轨迹（S, I, G, G, R, A, P, H）上生成连贯运动，无需逐字母微调。Figure 4 对比了无条件生成与多关节轨迹控制合成——冻结骨干在动态文本提示下合成多阶段运动（如华尔兹侧步、空手道型），而 K/V 控制检查点可驱动 OOD 约束模式（圆形行走、之字行走、弧线举手行走）。Figure 5 进一步展示了 S 曲线行走、螺旋行走、8 字形闭环路径等多样控制模式，验证了适配器的鲁棒泛化能力。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_05624/figures/009_Figure_3.jpg]]
*Figure 3: Qualitative trajectory control on out-of-distribution targets. Eight user-specified letter-shaped pelvis-trajectory targets (S, I, G, G, R, A, P, H) for our single-joint pelvis K/V-Control checkpoint, oblique 3/4 view; each cell overlays input waypoints as red 3D markers on the floor along 8 translucent body keyframes sampled from the L = 196 motion. The same trained adapter is applied to all eight letters with no per-letter tuning; the duplicate G panel is for visual readability of the SIGGRAPH word. 20 fps per-letter videos are in the supplementary*

### 失败模式与局限性

尽管 KV‑Control 在参数效率和控制精度上表现优异，论文坦承以下局限：

1. **密集约束退化**：当约束极为密集（如逐帧接触 + 多关节目标）时，Stage‑2 精炼可能过度拟合，导致非控制部位的运动质量退化。这需要更强的正则化以拓宽有效工作范围。
2. **跨骨骼迁移**：PartVQ 的分区方案基于 HumanML3D 的 22 关节骨骼，目前不支持直接迁移至其他骨骼拓扑。分区感知的骨骼重定向是适配其他角色的必要条件。
3. **长序列效率**：T‑Concat 将序列长度扩大 Q 倍，在极长序列生成场景下计算效率受限，尚未探索稀疏注意力等加速手段。
4. **骨干依赖性**：当前控制适配器依赖预训练的 PartVQ + T‑Concat 基底，未验证在其他离散潜在运动骨干（如扩散模型或自回归模型）上的即插即用能力。

> **注意**：以上局限均来自论文自述，其中跨骨骼迁移和骨干依赖性两点缺乏实验验证，需在实际部署中手动评估。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_05624/figures/007_Table_5.jpg]]
*Table 5: Extended diagnostics under the MaskControl protocol; means unless noted. Match. is the motion-text matching score of Guo et al. (2022); Div. is intra-set feature variance with real-data Diversity ∼ 9.5*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_05624/figures/008_Figure.jpg]]
*Figure: KV-Controlon User-Specified Out-of-Distribution Trajectories (oblique 3/4 view,8 keyframes)*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_05624/figures/010_Figure.jpg]]

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_05624/figures/011_Figure.jpg]]

## 方法谱系与知识库定位

### 轨迹控制方法谱系

文本到动作生成中的轨迹控制任务，核心瓶颈在于**如何在极小参数开销下实现高精度、保持文本先验的逐层控制**。现有方法可依控制信号的注入策略分为三条技术路线：

**复制分支（ControlNet式）路线**。**OmniControl**（Xie et al., ICLR 2024）和 **InterControl**（Wang et al., NeurIPS 2024）均采用复制骨干网络全部自注意力层的策略，以零初始化分支将轨迹条件逐层注入。这一方案虽然提供了逐层控制能力，但参数开销巨大——在118M冻结骨干上，复制分支的可训练参数量达39.3M（约骨干的33%），且精度并不占优（Table 2中复制分支M2骨盆误差达1.24 cm）。参数冗余的根源在于：复制分支必须恢复完整的自注意力计算图，而轨迹控制任务实际只需调制与受控关节相关的少数自由度。

**测试时优化路线**。**MaskControl**（Pinyoanuntapong et al., ICCV 2025）将控制成本从训练侧转移至推理侧：在冻结骨干的输出端，通过两阶段精炼（Stage-1优化运动令牌logits，Stage-2精炼令牌嵌入）使生成运动逼近目标轨迹。该方案无需任何控制适配器参数，但每样本推理需数百步迭代优化，延迟显著增加（M3配置下约需35×扩散步数的优化迭代）。此外，Table 5的冻结T‑Concat纯精炼基线表明：移除K/V适配器仅依赖精炼循环时，骨盆位置误差虽可降至~0.01 cm，但FID崩塌至103.86，证明**精炼循环本身无法维持运动流形结构**——它需要适配器提供的结构条件作为搜索空间的正则化边界。

**分部位VQ优化路线**。**TLControl**（Wan et al., ECCV 2024）将控制建模为分部位VQ码字的优化问题，以部位感知的离散令牌操作实现轨迹跟随。该方法在参数效率上优于复制分支方案，但其控制精度受限于VQ码本的离散粒度，且缺乏对自注意力内部信息流的直接调制能力。

### KV-Control 的定位与核心差异

KV-Control 在上述谱系中占据一个独特位置：**以1.5M机制参数（约为复制分支方案的1/26）实现最高精度的逐层控制**，同时保持骨干完全冻结、文本交叉注意力不受干扰。其与各路线的本质差异体现在三个设计决策上：

**注入侧的选择：键/值 vs. 查询**。所有复制分支方案在概念上等同于修改运动令牌的查询流——复制分支的输出被加回主分支，改变了自注意力中查询的来源。KV-Control 明确将控制信号注入键/值侧，保持运动令牌查询序列逐点不变（§3.3原文：“A key/value-side intervention instead leaves the motion-token query sequence pointwise unchanged”）。这一选择的关键后果是：文本交叉注意力模块的输入（来自自注意力的查询输出）完全不受轨迹控制干扰，从而保护了文本‑运动对齐。

**令牌布局：T‑Concat vs. C‑Concat**。传统方案将运动表示为每帧一个令牌（通道拼接各部位信息），KV-Control 通过 T‑Concat 将 Q=6 个部位码本沿序列轴展开，使每个（帧, 部位）成为独立的注意力可寻址令牌（S = T_tok × Q = 294）。Table 2 的消融直接验证了这一布局的决定性作用：同一20层骨干下，C‑Concat 布局的 M3 骨盆误差为 0.90 cm，而 T‑Concat 降至 0.40 cm。其因果机制在于：T‑Concat 将解剖部位显式化为注意力站点，低秩 K/V 残差可在查询位置精确调制单一解剖子令牌，而 C‑Concat 的通道混合令牌使控制信号无法精确路由至特定关节。

**适配器形态：记忆检索式 vs. 计算复制式**。KV-Control 将轨迹约束编码为附加的键/值记忆（$C_i^K, C_i^V$），在自注意力内部实现记忆检索式控制——运动令牌通过注意力分数“检索”相关的控制记忆。这一设计将适配器的角色从“复制并修改骨干计算”缩减为“学习每层应添加何种控制记忆”，从而将可训练参数压缩至极低水平（每层仅需下投影 $W_i^{down}$ 和两路上投影 $W_i^K, W_i^V$，总计1.5M）。

### 适用边界与局限

**当前已验证的适用条件**：
- 基底模型为基于 PartVQ + T‑Concat 的掩码运动 Transformer（118M 参数，20层，Q=6 部位分区）；
- 控制目标为稀疏关节位置轨迹（单关节骨盆或多关节），评估基于 HumanML3D 数据集及其 22 关节骨骼拓扑；
- 推理采用 MaskControl 继承的两阶段精炼协议（M0–M3 工作点，Table 1），精炼强度可调。

**已识别的局限**：
1. **密集约束退化**：当轨迹约束过于密集（如逐帧接触目标、多关节全时域约束）时，Stage-2 精炼可能过度拟合控制目标，导致非控制部位的运动质量退化。原文指出需要更强的正则化以拓宽有效工作范围。
2. **骨骼拓扑绑定**：PartVQ 的 Q=6 部位分区基于 HumanML3D 的 22 关节骨骼通过数据驱动的激活相关性聚类得出（Algorithm 1），目前不支持跨骨骼迁移。分区感知的骨骼重定向是适配其他角色形态的必要前置工作。
3. **序列长度扩展**：T‑Concat 将序列长度扩大 Q 倍（S = T_tok × Q），在极长序列生成场景下自注意力的 $O(S^2)$ 复杂度成为瓶颈。原文尚未探索稀疏注意力等加速手段。
4. **基底模型依赖**：当前所有实验均基于 PartVQ + T‑Concat 这一特定离散潜在运动骨干，未验证 K/V 注入机制在其他运动生成范式（如扩散运动模型、自回归模型）上的即插即用能力。

### 开放问题

1. **跨架构迁移**：KV‑Control 的键/值注入机制能否以同样低的参数开销迁移至扩散运动模型（如 MDM 系列）或自回归运动模型？这需要验证不同骨干的自注意力结构是否都支持“附加控制记忆”的抽象。
2. **约束类型扩展**：当前仅支持位置轨迹约束。能否在不显著增加开销的前提下，将控制信号扩展至速度、加速度、关节旋转上限等运动学/动力学约束？这可能需要在控制编码器中引入时域差分特征。
3. **分区学习化**：PartVQ 的部位分区目前通过启发式聚类固定。是否可以让分区完全可学习（如通过注意力模式自动发现），同时保持解剖语义的可解释性？这涉及离散潜在空间的结构化学习问题。
4. **交互式细粒度控制**：在交互式动画编辑场景中，能否通过动态启用/禁用特定层的 K/V 注入实现更细粒度的实时控制（如仅调制手部轨迹而保持下肢自然摆动）？这需要研究不同层对控制信号的响应特性差异。

## 原文 PDF

![[paperPDFs/arxiv_2026/KV-Control_Parameter-Efficient_KV_Injection_for_Trajectory-Controlled_Text-to-Motion.pdf]]