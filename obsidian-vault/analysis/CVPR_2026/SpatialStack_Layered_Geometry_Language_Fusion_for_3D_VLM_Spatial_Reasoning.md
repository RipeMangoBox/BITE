---
title: "SpatialStack: Layered Geometry-Language Fusion for 3D VLM Spatial Reasoning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SpatialStack_Layered_Geometry_Language_Fusion_for_3D_VLM_Spatial_Reasoning.pdf
project_link: "https://spatial-stack.github.io/"
code_link: null
aliases:
- SpatialStack
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 在LLM解码器的不同层中渐进式注入来自几何编码器多个深度的特征（浅层捕捉局部细节，深层编码全局结构），形成层次化的几何-语言融合。
primary_logic: 几何编码器的浅层特征保留尖锐的局部结构和几何边界，有利于基础空间感知；深层特征编码全局结构关系，适合复杂空间推理。通过将浅层几何特征注入LLM浅层、深层几何特征注入LLM深层，可同时强化局部几何精度和全局语义理解。
claims:
- 浅层几何特征保留清晰局部结构，深层特征趋于平滑均匀，表明单层融合丢失了关键的细粒度空间信息。
- 几何特征注入层越深，高层次任务性能提升但低层次任务性能下降，证明单层融合存在层级功能的互补性。
- 简单的多层级几何-视觉融合（GVF multi-layer）导致特征干扰，性能甚至弱于最佳单层融合，说明融合策略至关重要。
- SpatialStack的渐进式几何-语言对齐（L11→LLM-L0, L17→LLM-L1, L23→LLM-L2）在跨基准消融中取得最高综合得分，优于逆序融合和纯视觉融合。
---

# SpatialStack: Layered Geometry-Language Fusion for 3D VLM Spatial Reasoning

> [!tip] 核心洞察
> 几何编码器的浅层特征保留尖锐的局部结构和几何边界，有利于基础空间感知；深层特征编码全局结构关系，适合复杂空间推理。通过将浅层几何特征注入LLM浅层、深层几何特征注入LLM深层，可同时强化局部几何精度和全局语义理解。

| 字段 | 内容 |
|------|------|
| 中文题名 | SpatialStack：面向3D视觉语言模型空间推理的分层几何-语言融合 |
| 英文题名 | SpatialStack: Layered Geometry-Language Fusion for 3D VLM Spatial Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.27437) · [Project](https://spatial-stack.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SpatialStack |
| Dataset | VSI-Bench, CV-Bench |

> [!tip] 效果简介
> - VSI-Bench 上，Avg. 67.5 (SpatialStack-5B, Qwen3.5-4B) vs 60.9 (Cambrian-S-3B, 最佳先前开源模型) (+6.6)。
> - CV-Bench (Table C) 上，Overall 86.5 vs 72.7 (SpatialRGPT) (+13.8)。
> - 跨基准综合 (VSI/SPAR/CV-Bench) 上，Overall average SpatialStack 最高 vs GVF-L23 / Qwen3.5 基线 (显著领先（具体数值因基准而异）)。

## 概要

**解决的问题。** 现有3D视觉语言模型（VLM）仅将几何编码器的单层（通常为最后一层）深度特征与视觉分支融合。该设计丢弃了编码器中间层蕴含的丰富层次化几何线索——浅层保留尖锐的局部结构与几何边界，深层编码全局空间关系——导致VLM在细粒度空间感知与高层空间推理两方面均存在性能瓶颈。

**核心思路。** SpatialStack提出一种通用的分层几何-语言融合框架，其核心控制变量是：在LLM解码器的不同层中渐进式注入来自几何编码器多个深度的特征。具体而言，浅层几何特征（VGGT层11）注入LLM浅层以强化局部几何精度，深层几何特征（VGGT层17、23）注入LLM更深层以支持全局语义推理，从而形成跨模型层级的视觉-几何-语言渐进对齐。融合采用掩码加性残差注入，仅更新视觉token位置，避免干扰语言token。

**关键证据。** 相似度热力图显示，几何编码器浅层特征保留清晰的局部结构，深层特征趋于平滑均匀，证实单层融合丢失了关键的细粒度空间信息（Fig. 2）。注入层消融实验表明，深层注入有利于高层任务，但低层任务在层11达到峰值后随注入深度增加而下降，揭示层级功能的互补性（Figure 4）。简单的多层级几何-视觉融合（GVF multi-layer）导致特征干扰，整体性能（64.92）甚至弱于最佳单层融合（65.35），说明融合策略至关重要（Table 1）。最终，渐进式几何-语言对齐（L11→LLM-L0, L17→LLM-L1, L23→LLM-L2）在跨基准消融中取得最高综合得分（69.14），优于逆序融合和纯视觉融合（Table 7）。

**主要结果。** SpatialStack在多个3D空间推理基准上达到领先水平：VSI-Bench上SpatialStack-5B取得67.5，较最佳先前开源模型Cambrian-S-3B（60.9）提升+6.6（Table 3）；CV-Bench上取得86.5，较SpatialRGPT（72.7）提升+13.8（Table C）；跨基准综合消融中整体平均分最高（Table 2）。模型在通用能力评测中未出现灾难性遗忘（Table 5）。

**方法谱系与知识库定位。** 该工作属于“几何增强的3D VLM”方向，与以下路线形成对比：(1) 单层几何-视觉融合路线，如GVF-L23（VG-LLM）仅用最后一层几何特征注入视觉编码器；(2) 双编码器架构，如Spatial-MLLM将几何特征融合到视觉分支；(3) 基于RGB-D的空间推理VLM，如SpatialRGPT、Spatialbot；(4) 大规模空间指令微调模型，如Cambrian-S。SpatialStack的独特贡献在于将融合目标从视觉侧迁移到语言侧，并以渐进式分层策略替代单层或简单堆叠，从而系统性地利用几何编码器的层次化表征能力。训练仅更新融合模块与LLM解码器，视觉塔与VGGT保持冻结，约200k样本指令微调，保证了比较的公平性。

**局限与开放问题。** 论文未明确讨论方法在计算开销、对VGGT预训练权重的依赖、极端动态场景泛化等方面的局限性。开放问题包括：层次化几何特征应如何以及在何处融合才能最大化VLM的空间推理能力？该多级融合策略能否推广到更复杂的动态场景（4D世界模型）与具身交互任务？



### 3D空间推理的视觉语言模型现状

3D空间推理要求模型不仅理解场景中“有什么”，还要精确感知物体间的几何关系——相对距离、方位排序、跨物体空间布局等。近年来，视觉语言模型（VLM）在通用多模态理解上取得了显著进展，但在细粒度空间感知和高层空间推理方面仍存在明显短板。现有方案通常采用双编码器架构：一个视觉编码器提取外观特征，一个几何编码器（如基于多视图的VGGT）捕获深度与结构信息。然而，**几何特征的融合方式构成了当前方法的核心瓶颈**。

### 单层融合的局限：层次化几何线索的丢弃

主流VLM在融合几何信息时，仅使用几何编码器的**最后一层输出特征**（如GVF-L23方案），将其注入视觉分支或LLM输入端。这一做法隐含假设：深层特征已充分编码所有空间信息。但实证分析揭示了相反的事实。

**浅层几何特征保留清晰的局部结构**。如Figure 2左侧相似度热力图所示，VGGT浅层（如第11层）的patch特征呈现出尖锐的局部激活模式，能够精确刻画物体边界和细粒度几何差异；而随着层数加深，特征逐渐趋于平滑均匀，深层（如第23层）的激活呈现过度同质化。这意味着，仅依赖单层深层特征会**系统性地丢失中间层蕴含的细粒度空间线索**，形成“信息瓶颈”。

**不同层级的几何特征服务于不同粒度的空间任务**。Figure 4的层级注入实验揭示了清晰的权衡关系：将几何特征注入LLM解码器的浅层时，低层次任务（如相对深度判断——判断两点中哪一点更靠近相机）性能达到峰值；而注入层越深，高层次任务（如跨物体距离估计——计算两个物体最近点之间的3D距离）性能持续提升，但低层次任务性能在深层出现下降。这证明了几何编码器的中间层与深层之间存在**功能互补性**：浅层特征擅长局部几何精度，深层特征编码全局结构关系。

### 多层级融合的失败：简单堆叠并非答案

直观的改进思路是将多个几何层的特征同时融合。然而，Table 1的消融实验给出了反直觉的结果：将多层几何特征简单融合到视觉分支（GVF multi-layer），其综合性能（64.92）甚至**弱于最佳单层融合**（65.35，使用第23层）。这表明不同层级的几何特征之间存在**特征干扰**——浅层的局部细节与深层的全局语义在缺乏对齐机制的情况下直接混合，反而损害了表征质量。融合策略本身比特征数量更为关键。

### SpatialStack的动机：渐进式几何-语言对齐

上述发现共同指向一个核心洞察：**几何编码器的浅层特征保留尖锐的局部结构和几何边界，有利于基础空间感知；深层特征编码全局结构关系，适合复杂空间推理。** 因此，理想的融合框架应当让不同层级的几何特征在语言模型的**对应层级**发挥作用——浅层几何特征注入LLM浅层以强化局部几何精度，深层几何特征注入LLM深层以增强全局语义理解。

基于此，SpatialStack提出了一种**分层几何-语言融合框架**：从VGGT的多个深度（第11、17、23层）提取patch级几何特征，经过层特定投影器对齐后，以加性残差方式**渐进式注入LLM解码器的前几层**（L11→LLM-L0, L17→LLM-L1, L23→LLM-L2）。这一设计将融合目标从传统的“几何→视觉”转向“几何→语言”，使得层次化几何线索能够直接参与语言模型的多层推理过程，同时避免了简单堆叠带来的特征干扰。



## 核心方法与创新机理

SpatialStack 的核心创新在于将几何编码器与语言解码器之间从“单层几何-视觉融合”重构为“分层几何-语言融合”，以层次化方式保留并利用几何编码器中间层蕴含的丰富空间线索。具体而言，其创新体现在以下四个关键维度。

### 1. 从单层到多层：解锁几何编码器的层次化表征

现有方法（如 VG-LLM）仅提取几何编码器（VGGT）的最后一层特征进行融合，丢弃了中间层保留的细粒度几何结构。SpatialStack 则同时利用 VGGT 的多个层 `{11, 17, 23}` 的 patch token 输出，形成层次化的几何特征集合。**关键证据**：相似度热力图（Figure 2）显示，浅层几何特征保留清晰的局部结构和几何边界，而深层特征趋于平滑均匀——单层融合必然丢失这类关键的细粒度空间信息。

### 2. 融合目标迁移：从几何-视觉融合到几何-语言融合

传统方案将几何特征注入视觉编码器特征（Geometry-Vision Fusion），SpatialStack 则将几何特征直接注入 LLM 解码器的前几层（Geometry-Language Fusion）。这一迁移使得几何信息能够直接参与语言模型的多层推理过程，而非仅在视觉表示阶段进行一次性的特征混合。**关键证据**：Table 7 消融显示，SpatialStack 的几何-语言融合（Overall 69.14）优于纯视觉融合方案（Vision Fusion 68.38）。

### 3. 渐进式层级对齐：浅层几何→浅层语言，深层几何→深层语言

SpatialStack 的核心设计是渐进式映射：`Geo-L11 → LLM-L0, Geo-L17 → LLM-L1, Geo-L23 → LLM-L2`。这一映射的因果逻辑在于：浅层几何特征擅长捕捉局部细节和几何边界，适合注入 LLM 浅层以强化基础空间感知；深层几何特征编码全局结构关系，适合注入 LLM 深层以支持复杂空间推理。**关键证据**：Figure 4 揭示了明确的层级功能互补——注入层越深，高层次任务性能提升但低层次任务性能下降（L11 最适合低层感知，L23 最适合高层推理）；Table 7 进一步证实，渐进式对齐（69.14）显著优于逆序融合（Reverse 68.52）。

### 4. 掩码加性残差注入：精准更新视觉 token

SpatialStack 采用掩码加性残差注入策略，通过 scatter 操作仅对视觉 token 位置施加几何加性残差，非视觉 token 保持不变（见 Eq. (16)）。该设计避免了简单堆叠多层几何特征导致的特征干扰——**关键证据**：Table 1 显示，简单的多层几何-视觉融合（GVF multi-layer）整体性能（64.92）甚至弱于最佳单层融合（65.35），说明融合策略的精细设计至关重要。

### 方法谱系与知识库定位

SpatialStack 在以下维度与现有工作形成差异化：

- **vs. 单层几何融合（VG-LLM / GVF-L23）**：仅用最后一层几何特征，丢失中间层细粒度几何线索。
- **vs. 双编码器架构（Spatial-MLLM）**：融合几何特征到视觉分支，而非直接注入语言解码器。
- **vs. 大规模空间指令微调（Cambrian-S）**：依赖数据规模驱动，未显式建模几何特征的层级结构。
- **vs. RGB-D 空间推理（SpatialRGPT / Spatialbot）**：基于深度输入，与基于多视图几何编码器的融合范式不同。

SpatialStack 的层级融合框架具有通用性——其核心思想（从编码器多层提取特征并渐进注入解码器）可推广至其他多模态架构，为 3D VLM 的空间推理能力提升提供了新的设计范式。



SpatialStack 的核心设计是将多层级几何特征渐进式注入语言解码器，形成一条贯穿视觉、几何与语言表征的层次化融合通道。整个框架由五个关键模块构成，数据流沿“视觉编码→几何编码→几何对齐→加性注入→语言解码”方向单向推进，各模块分工如下：

### 视觉编码器

多视图图像首先经过视觉编码器提取视觉 token，再将多视图 token 合并为统一的视觉表示 $\tilde{\mathbf{V}}$。该表示与文本 token $\mathbf{T}$ 拼接，构成 LLM 解码器的初始输入序列 $\mathbf{H}_0 = [\tilde{\mathbf{V}}; \mathbf{T}]$。视觉编码器在指令微调阶段保持冻结，仅作为固定特征提取器。

### 几何编码器（VGGT）

同一组多视图图像并行送入 VGGT 几何编码器。VGGT 的每一层都会产生包含相机 token、寄存器 token 和 patch token 的中间表示，其中浅层（如第 11 层）保留尖锐的局部几何边界，深层（如第 23 层）编码全局结构关系。SpatialStack 从 VGGT 的 **第 11、17、23 层** 分别提取 patch token 输出，作为三个不同抽象层级的几何特征源。

### 几何 Token 合并器

不同层的几何特征在空间分辨率和语义维度上存在差异，无法直接注入 LLM。为此，每一层配备独立的 **层特定 MLP 投影器**，将对应层的几何 token 对齐到语言空间的目标维度和 token 数量，得到对齐后的几何特征 $\mathbf{G}_{l_i}$。

### 掩码加性融合

对齐后的几何特征以 **加性残差** 形式注入 LLM 解码器的对应层。具体映射关系为：

- $\mathbf{G}_{11}$（浅层局部几何）→ LLM 第 0 层
- $\mathbf{G}_{17}$（中层过渡几何）→ LLM 第 1 层
- $\mathbf{G}_{23}$（深层全局几何）→ LLM 第 2 层

注入操作通过 **scatter 掩码机制** 实现：仅对视觉 token 位置施加几何残差，非视觉 token 位置保持不变。这一设计避免了几何特征对文本语义空间的干扰，同时确保空间信息精准作用于视觉区域。

### LLM 解码器

注入几何残差后，LLM 解码器（基于 Qwen2.5/3.5 系列）逐层处理融合后的多模态序列，最终生成空间推理答案。整个模型在约 200k 样本的混合数据集上以标准交叉熵损失进行指令微调，训练时仅更新融合模块和 LLM 解码器参数，视觉编码器与几何编码器均保持冻结。

### 框架的因果逻辑

该框架的因果逻辑可概括为：**浅层几何特征注入 LLM 浅层，强化细粒度局部感知；深层几何特征注入 LLM 深层，增强全局语义推理**。这一渐进式对齐策略在消融实验中得到了直接验证——注入层越深，高层次任务性能提升但低层次任务性能下降，说明不同层级的几何特征在功能上确实存在互补性。简单地将所有层级几何特征同时融合到视觉侧（GVF multi-layer）反而导致特征干扰，整体性能（64.92）甚至弱于最佳单层融合（65.35），进一步证明了分层、分阶段的注入策略对融合质量的决定性作用。

### 补充图表

![[assets/figures/papers/paper_list_l2420_https_arxiv_org_abs_2603_27437/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of SpatialStack. A standard VLM backbone is coupled with a multi-view geometry encoder whose layer-wise features are processed by layer-specific projectors and sequentially injected into the LLM decoder, progressively integrating geometric cues. Explanation of the similarity heatmaps on the left is provided in Sec. 3. This multi-level injection preserves both fine-grained geometric structure and high-level spatial context, supporting more reliable low-level understanding and high-level reasoning*

![[assets/figures/papers/paper_list_l2420_https_arxiv_org_abs_2603_27437/figures/001_Figure_1.jpg]]
*Figure 1: SpatialStack: Layered Geometry-Language Fusion. Conventional VLMs (a) fuse only a single deep geometry feature with vision tokens, which limits both fine-grained spatial understanding and high-level spatial reasoning. SpatialStack (b) instead stacks multilevel geometry features and injects them hierarchically into successive LLM decoder layers, yielding stronger 3D spatial understanding across benchmarks*



SpatialStack 的核心架构由五个模块串联构成：**Vision Encoder** 提取多视图视觉 token 并合并为统一视觉表示；**Geometry Encoder (VGGT)** 从多视图图像中提取多层级几何特征；**Geometry Token Merger** 通过层特定 MLP 将不同层的几何特征对齐到语言空间的维度和分辨率；**Masked Additive Fusion** 将投影后的几何特征以加性残差方式注入 LLM 解码器的对应层；**LLM Decoder** 接收融合后的多模态序列，执行空间推理与答案生成。

### 多模态输入序列构建

LLM 解码器的初始输入序列由视觉 token 和文本 token 拼接而成：

$$
\mathbf{H}_0 = [\tilde{\mathbf{V}}; \mathbf{T}]
$$

其中 $\tilde{\mathbf{V}}$ 为视觉编码器提取并合并后的视觉 token，$\mathbf{T}$ 为文本指令的 token 嵌入。

### 几何编码器前向传播

VGGT 几何编码器对多视图图像逐层提取几何特征。对于第 $k$ 个视图，初始 token 序列包含相机 token $\mathbf{c}_k$、寄存器 token $\mathbf{r}_k$ 和 patch token $\mathbf{p}_k$：

$$
\mathbf{Z}_0^{(k)} = [\mathbf{c}_k; \mathbf{r}_k; \mathbf{p}_k] \in \mathbb{R}^{(1+R+N) \times D_{\mathrm{geo}}}
$$

所有 $K$ 个视图的初始序列拼接后，经过 $L$ 层 Transformer 逐层处理：

$$
\mathbf{Z}_L = f_L^{\mathrm{geo}} \big( f_{L-1}^{\mathrm{geo}} ( \cdots f_1^{\mathrm{geo}} ( [\mathbf{Z}_0^{(1)}; \cdots; \mathbf{Z}_0^{(K)}] ) ) \big)
$$

### 几何 Token 合并与投影

从 VGGT 的指定层 $\{l_1, l_2, l_3\} = \{11, 17, 23\}$ 提取 patch token 输出，通过层特定的几何 token 合并器 $\mathcal{M}_{\mathrm{geo}}^{(l_i)}$ 对齐空间分辨率和嵌入维度：

$$
\mathbf{G}_{l_i} = \mathcal{M}_{\mathrm{geo}}^{(l_i)}(\mathbf{Z}_{l_i}), \quad \mathbf{G}_{l_i} \in \mathbb{R}^{N' \times D_{\mathrm{lang}}}
$$

其中 $D_{\mathrm{lang}}$ 为 LLM 的隐藏层维度，$N'$ 为对齐后的 token 数量。合并器由层特定的 MLP 实现，将几何编码器的输出维度 $D_{\mathrm{geo}}$ 投影到语言空间维度，同时调整空间分辨率以匹配视觉 token 的数量。

### 掩码加性残差注入

投影后的几何特征以加性残差方式注入 LLM 解码器的对应层，形成渐进式几何-语言对齐：Geo-L11 → LLM-L0，Geo-L17 → LLM-L1，Geo-L23 → LLM-L2：

$$
\mathbf{H}^{(j)'} = \mathbf{H}^{(j)} + \mathbf{G}_{l_j}, \quad j \in \{0, 1, 2\}
$$

其中 $\mathbf{H}^{(j)}$ 为 LLM 第 $j$ 层的隐藏状态。注入操作通过 scatter 机制实现，仅更新视觉 token 位置，非视觉 token 保持不变：

$$
\mathbf{H}_l[i] \gets \begin{cases} \mathbf{H}_l[i] + \mathbf{G}_l[k], & \text{if } M_{\mathrm{vis}}[i] = 1, \\ \mathbf{H}_l[i], & \text{if } M_{\mathrm{vis}}[i] = 0 \end{cases}
$$

$M_{\mathrm{vis}}$ 为视觉 token 位置的二值掩码。这种掩码加性融合策略确保几何信息仅增强视觉 token 的表示，避免对文本 token 引入噪声。

### LLM 解码器前向传播与优化目标

融合后的多模态序列经过 LLM 的堆叠 Transformer 层逐层处理：

$$
\mathbf{H}_L^{\mathrm{llm}} = f_L^{\mathrm{llm}} \big( f_{L-1}^{\mathrm{llm}} ( \cdots f_1^{\mathrm{llm}} ( \mathbf{H}_0 ) ) \big)
$$

整个模型以标准的下一 token 负对数似然（交叉熵）损失进行指令微调：

$$
\mathcal{L}_{\mathrm{ce}}(\theta) = -\sum_{i=1}^{|o|} \log P_{\theta}\big(o^{(i)} \mid o^{(<i)}, q, \mathcal{C}\big)
$$

其中 $q$ 为问题，$\mathcal{C}$ 为多视图上下文，$o$ 为答案 token 序列。训练时冻结视觉编码器和几何编码器（VGGT），仅更新融合模块和 LLM 解码器参数。

### 补充图表

![[assets/figures/papers/paper_list_l2420_https_arxiv_org_abs_2603_27437/figures/005_Figure_4.jpg]]
*Figure 4: Effect of Geometry Injection Layers on Spatial Tasks. Deeper layers improve high-level tasks, while low-level tasks peak at layer 11 and decline at deeper layers, suggesting a trade-off between fine-grained perception and higher-level reasoning*



## 实验与关键发现

### 实验设置

SpatialStack的训练采用统一的下一token交叉熵损失进行指令微调：

$$\mathcal{L}_{\mathrm{ce}}(\theta) = -\sum_{i=1}^{|o|} \log P_{\theta}\big(o^{(i)} \mid o^{(<i)}, q, \mathcal{C}\big)$$

训练期间，视觉编码器和几何编码器（VGGT）均保持冻结，仅更新多模态融合模块和LLM解码器。训练使用AdamW优化器，学习率 $1 \times 10^{-5}$，warmup比例0.03，余弦学习率调度，batch size为64。训练数据混合约200k样本，从SPAR-234k、LLaVA-Hound-64k和VLM-3R的ScanNet子集中采样60%，并额外加入约2k的VSI-590k外观顺序样本以补充排序监督信号（Table A）。

### 主要结果

**VSI-Bench.** SpatialStack-5B（基于Qwen3.5-4B）在VSI-Bench上取得Avg. 67.5，相较于此前最佳开源模型Cambrian-S-3B的60.9，提升+6.6个百分点（Table 3）。在多个细粒度子指标上，SpatialStack-5B均取得开源模型中的最优或次优结果，证明了分层几何-语言融合对空间推理的显著增益。

**CV-Bench.** 基于Qwen2.5构建的SpatialStack-4B在CV-Bench上取得Overall 86.5，大幅超越SpatialRGPT的72.7（+13.8，Table C），同时优于VG-LLM和Cambrian-S（Table 4）。扩展到Qwen3.5后，SpatialStack-5B进一步提升基准表现，在2D和3D空间感知上均达到新的最优水平。

**跨基准综合.** 在VSI-Bench、SPAR-Bench、CV-Bench三个核心空间推理基准的跨基准消融中，SpatialStack取得最高的综合平均分，显著优于GVF-L23和Qwen3.5基线（Table 2）。值得注意的是，Qwen3.5基线在BLINK-Spatial上仍保持最强，提示该基准可能更依赖纯语言能力而非几何增强。

**通用能力保持.** SpatialStack-5B在通用多模态和时空推理评测中保持鲁棒表现，未出现灾难性遗忘（Table 5），说明几何增强并未损害模型的基础能力。

### 消融实验

#### 1. 几何token融合深度（Table 1）

![[assets/figures/papers/paper_list_l2420_https_arxiv_org_abs_2603_27437/figures/004_Table_1.jpg]]
*Table 1: Ablation Results on Geometry Token Fusion Depth. Simply fusing multi-layer geometry features to the visual features yields suboptimal performance, while selecting an appropriate single geometry encoder layer achieves better task-specific trade-offs*

简单地将多层几何特征同时融合到视觉特征（GVF multi-layer）导致整体性能（64.92）甚至弱于最佳单层融合（geo enc: 23, 65.35）。这表明**朴素的多层堆叠会造成特征干扰**，而非简单的信息增益。选择适当的单一几何编码器层可以在特定任务上取得更好的权衡。

#### 2. 注入层深度与任务层级权衡（Figure 4）

几何特征注入层越深，高层次空间推理任务性能持续提升，但低层次空间感知任务在LLM第11层达到峰值后随注入深度增加而下降。这一现象直接验证了核心洞察：**浅层几何特征保留局部结构细节，适合细粒度感知；深层几何特征编码全局关系，适合复杂推理**。单层融合无法同时兼顾两者，构成了根本瓶颈。

#### 3. 深层几何层选择（Table 6）

![[assets/figures/papers/paper_list_l2420_https_arxiv_org_abs_2603_27437/figures/009_Table_6.jpg]]
*Table 6: Layer Selection Ablation. Performance comparison of extracting geometry features from different deep VGGT layers (L21, L22, L23) and their multi-layer combinations*

将深层几何特征从VGGT的L23替换为L21或L22，对最终性能影响不显著。这说明深层几何特征具有一定容差，SpatialStack对具体层选择不敏感，框架具有良好的鲁棒性。

#### 4. 几何-语言融合顺序（Table 7）

![[assets/figures/papers/paper_list_l2420_https_arxiv_org_abs_2603_27437/figures/011_Table_7.jpg]]
*Table 7: Geometry-Language Fusion Order Ablation. Comparison of our progressive hierarchical alignment against a reverse fusion strategy and baseline models*

渐进式几何-语言对齐策略（Geo-L11→LLM-L0, Geo-L17→LLM-L1, Geo-L23→LLM-L2）在跨基准消融中取得最高综合得分（69.14），优于逆序融合（68.52）和纯视觉融合（68.38）。这证实了**浅层几何特征应注入LLM浅层以强化基础空间感知，深层几何特征应注入LLM深层以增强高层推理**的设计原则。逆序融合破坏了这种层级对应关系，导致性能下降。

### 失败模式与局限性

论文未明确讨论方法的局限性。根据实验证据推断，以下方面需要关注：

- **BLINK-Spatial上的相对弱势**：Qwen3.5基线在该基准上优于SpatialStack（Table 2），可能表明当前几何注入策略对某些纯语言空间推理任务的增益有限。
- **朴素多层融合的失败**（Table 1）：直接堆叠多层几何特征会产生特征干扰，说明融合策略的设计至关重要，简单扩展无法带来收益。
- **对VGGT预训练权重的依赖**：几何编码器在训练中保持冻结，方法的有效性依赖于VGGT提供的层次化几何表征质量。在VGGT未覆盖的场景或域外数据上的泛化能力未经验证。
- **动态场景与具身交互**：当前评估集中在静态3D场景的空间推理，方法能否推广到4D动态世界模型和具身交互任务仍是开放问题。

![[assets/figures/papers/paper_list_l2420_https_arxiv_org_abs_2603_27437/figures/006_Table_2.jpg]]
*Table 2: Cross-benchmark Ablation. SpatialStack achieves the best cross-task transfer ability, obtaining the highest scores on VSI-Bench, SPAR-Bench, CV-Bench, and the overall average, while the Qwen3.5 baseline remains strongest on BLINK-Spatial. Gray cells denote the highest value in each column*

### 小结

SpatialStack通过分层几何-语言融合框架，系统性地解决了现有VLM仅使用单层几何特征的瓶颈。消融实验一致表明：**浅层几何特征→LLM浅层、深层几何特征→LLM深层的渐进式映射是实现细粒度感知与高层推理兼顾的关键**，而朴素的多层堆叠或逆序融合均会损害性能。在VSI-Bench和CV-Bench上，SpatialStack均取得开源模型中最优结果，同时保持了通用能力不退化。

### 补充图表

![[assets/figures/papers/paper_list_l2420_https_arxiv_org_abs_2603_27437/figures/008_Table_3.jpg]]
*Table 3: Evaluation on VSI-Bench. Dark orange cells denote the best open-source result in each column, while light orange cells denote the second-best open-source result. Group-wise ranks within proprietary and open-source model blocks are highlighted in purple, with dark purple , medium purple , and light purple indicating 1st, 2nd, and 3rd place, respectively*

![[assets/figures/papers/paper_list_l2420_https_arxiv_org_abs_2603_27437/figures/010_Table_4.jpg]]
*Table 4: Comparison on CV-Bench. Built on Qwen2.5, SpatialStack-4B outperforms its base model alongside VG-LLM and Cambrian-S. Scaling to Qwen3.5, SpatialStack-5B further improves upon its baseline to set a new state-of-the-art*

![[assets/figures/papers/paper_list_l2420_https_arxiv_org_abs_2603_27437/figures/012_Table_5.jpg]]
*Table 5: General Capabilities Evaluation. Our SpatialStack-5B maintains robust general multimodal and spatial-temporal reasoning capabilities, demonstrating no catastrophic forgetting*

![[assets/figures/papers/paper_list_l2420_https_arxiv_org_abs_2603_27437/figures/003_Figure_3.jpg]]
*Figure 3: Examples of spatial tasks at different levels. The left example (Low-Level Task) targets fine-grained geometric perception, such as determining which of two points is closer to the camera. The right example (High-Level Task) requires higher-level spatial reasoning, where the model must estimate the distance between two objects by comparing their closest points in 3D space*

![[assets/figures/papers/paper_list_l2420_https_arxiv_org_abs_2603_27437/figures/018_Table.jpg]]
*Table: C. Additional Baseline Comparison on CV-Bench*



## 定位与知识库关联

### 1. 与现有工作的关系

#### 1.1 通用视觉语言模型基线

SpatialStack 构建于通用视觉语言模型（VLM）之上，其直接基线是 **Qwen2.5-VL** 和 **Qwen3.5** 系列。这些通用 VLM 不具备显式的几何增强模块，仅通过视觉编码器处理图像输入后交由 LLM 解码器进行多模态推理。SpatialStack 在冻结视觉编码器和几何编码器的前提下，仅在 LLM 解码器的前几层注入多层级几何特征，从而在保持通用能力不衰退（Table 5）的同时获得空间推理增益。

#### 1.2 几何增强 VLM 谱系

**单层几何-视觉融合范式（GVF / VG-LLM）** 是此前的主流方案。该类方法将几何编码器（如 VGGT）的**仅最后一层**特征投影后注入视觉分支，形成几何-视觉融合（Geometry-Vision Fusion, GVF）。SpatialStack 的消融实验（Table 1）直接验证了这一范式的瓶颈：GVF-L23（仅用第 23 层几何特征）取得 65.35 的整体平均分，而简单堆叠多个几何层进行视觉融合（Multi-Layer Fusion）反降至 64.92，表明**不加区分的多层级融合会产生特征干扰**，性能甚至弱于最佳单层融合。

**双编码器架构（Spatial-MLLM）** 同样尝试融合几何特征，但其注入目标仍是视觉分支，未触及几何-语言直接对齐的核心问题。

**RGB-D 空间推理 VLM（SpatialRGPT / Spatialbot）** 依赖深度传感器输入进行空间感知。SpatialStack 在 CV-Bench 上相较 SpatialRGPT 取得了 +13.8 的整体提升（86.5 vs 72.7，Table C），表明从多视图图像中提取的层次化几何线索可以超越直接深度输入的效用。

**大规模空间指令微调模型（Cambrian-S）** 是此前 VSI-Bench 上最强的开源模型（Avg. 60.9）。SpatialStack-5B 以 67.5 的 Avg. 超越其 +6.6（Table 3），确立了新的开源最优。

#### 1.3 核心差异：几何-语言融合 vs. 几何-视觉融合

SpatialStack 与上述所有工作的根本分水岭在于**融合目标从视觉侧迁移到语言侧**（Figure 2）。这一设计转变由两个关键发现驱动：

1. **几何编码器的层次化特性**（Figure 4）：浅层（L11）保留尖锐的局部结构和几何边界，有利于基础空间感知任务（如相对深度判断）；深层（L23）编码全局结构关系，适合复杂空间推理任务（如跨物体距离估计）。单层融合必然丢失其中一类信息。

2. **融合策略的敏感性**（Table 1）：即便获取了多层级特征，简单地堆叠注入仍会导致干扰。SpatialStack 的渐进式映射策略——Geo-L11→LLM-L0, Geo-L17→LLM-L1, Geo-L23→LLM-L2——在跨基准消融中取得 69.14 的综合得分，优于逆序融合（68.52）和纯视觉融合（68.38）（Table 7），验证了“浅层几何对齐浅层语言、深层几何对齐深层语言”的因果逻辑。

### 2. 适用边界

#### 2.1 适用场景

- **多视图静态场景的 3D 空间推理**：SpatialStack 在 VSI-Bench、SPAR-Bench、CV-Bench 三个空间推理基准上均取得最优或领先结果（Table 2），覆盖相对深度、距离估计、空间关系判断等任务。
- **通用多模态能力的保持**：Table 5 表明空间增强后无灾难性遗忘，模型在通用视觉问答和时空推理基准上保持稳健。
- **参数高效扩展**：SpatialStack-4B（基于 Qwen2.5）和 SpatialStack-5B（基于 Qwen3.5）均表现出随基座模型升级而持续增益的特性（Table 4），说明框架具有良好的可扩展性。

#### 2.2 已知局限

论文未明确讨论方法的局限性，以下边界需手动验证：

- **对 VGGT 预训练权重的依赖**：几何编码器在训练期间保持冻结，其层次化特征的质量完全取决于 VGGT 的预训练效果。若 VGGT 在特定域（如极端光照、稀疏纹理）退化，SpatialStack 的几何注入可能引入噪声而非增益。
- **动态场景泛化能力未知**：所有评测基准均为静态 3D 场景，方法在动态环境（如 4D 世界模型、具身交互中的时序空间推理）下的有效性未经检验。
- **计算开销**：引入额外的几何编码器和多层融合模块会增加推理延迟和显存占用，但论文未报告具体的效率对比数据。
- **深层几何层的容差范围**：Table 6 显示将 L23 替换为 L21 或 L22 对性能影响不大，表明深层特征具有一定冗余。但浅层（L11）的选择是否同样鲁棒，以及不同场景下最优层组合的自动化选择策略，均未探索。

### 3. 开放问题

论文明确提出的开放问题聚焦于融合策略的泛化性：

> 层次化几何特征应如何以及在何处融合，才能最大限度地增强 VLM 的空间推理能力？

SpatialStack 给出了一个有效的经验解（渐进式几何-语言对齐），但以下方向仍待探索：

1. **动态层选择机制**：当前层映射 {11, 17, 23} 是固定的。是否可以根据输入场景的复杂度动态选择注入层和融合强度？例如，简单场景仅需浅层几何，复杂场景激活深层全局推理。

2. **向 4D 世界模型和具身交互的扩展**：在时序空间推理任务中，几何特征的层次化特性是否仍然成立？运动信息应注入 LLM 的哪个深度？

3. **跨架构泛化**：SpatialStack 的渐进式对齐策略是否适用于其他几何编码器（非 VGGT）和其他 LLM 架构（非 Qwen 系列）？融合层数与 LLM 深度的最优比例关系是什么？

4. **训练数据配比的敏感性**：训练混合数据约 200k 样本（Table A），其中 60% 来自 SPAR-234k。不同数据配比对层次化融合效果的影响尚未消融分析。



## 原文 PDF

![[paperPDFs/CVPR_2026/SpatialStack_Layered_Geometry_Language_Fusion_for_3D_VLM_Spatial_Reasoning.pdf]]
