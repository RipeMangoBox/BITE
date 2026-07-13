---
title: "Large-Scale 3D Generative Modeling using Sparse Voxel Hierarchies"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/Large_Scale_3D_Generative_Modeling_using_Sparse_Voxel_Hierarchies.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/xcube/
code_link: null
aliases:
- XHVLDM
- LS3GMUSVH
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "采用层级化稀疏体素潜在扩散模型，通过从粗到细的生成方式，层层递进地构建高分辨率体素网格。"
primary_logic: "利用稀疏体素层次结构将复杂生成任务分解为多个条件更简单的子任务，每一层级仅需建模局部几何细节，同时得益于高效的VDB数据结构，得以在1024^3分辨率下实时生成。"
claims:
- "在ShapeNet数据集上，XCube在1-NNA CD/EMD指标上全面超越基线方法（如NFD、NWD、LION等）。"
- "层次化模型在消融实验中优于单层模型，验证了稀疏体素层级的重要性。"
- "在Objaverse文字到3D用户研究中，79.2%的比较倾向于XCube生成的形状，而非Shap·E。"
- "在Waymo场景生成用户研究中，66.3%的比较认为XCube生成的场景比真实数据更真实。"
---

# Large-Scale 3D Generative Modeling using Sparse Voxel Hierarchies

> [!tip] 核心洞察
> 利用稀疏体素层次结构将复杂生成任务分解为多个条件更简单的子任务，每一层级仅需建模局部几何细节，同时得益于高效的VDB数据结构，得以在1024^3分辨率下实时生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | XCube: 基于稀疏体素层级的大规模三维生成建模 |
| 英文题名 | Large-Scale 3D Generative Modeling using Sparse Voxel Hierarchies |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2312.03806) · [Project](https://research.nvidia.com/labs/toronto-ai/xcube/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | XCube (Hierarchical Voxel Latent Diffusion Model) |
| Dataset | ShapeNet Airplane, ShapeNet Chair, ShapeNet Car, Objaverse (Text-to-3D) |

> [!tip] 效果简介
> - ShapeNet Airplane 上，1-NNA CD 为 52.85，对比 57.55 (NFD)，变化 -4.70。
> - ShapeNet Chair 上，1-NNA EMD 为 48.60，对比 54.06 (NFD)，变化 -5.46。
> - ShapeNet Car 上，1-NNA CD 为 57.96，对比 60.61 (LION)，变化 -2.65。

## 概要

现有三维生成模型的核心瓶颈在于**先验表示的分辨率受限**：基于密集体素、点云或三平面（Triplane）的方法难以有效扩展到大规模室外场景（如自动驾驶数据），无法在可接受的计算开销下捕捉高分辨率几何细节。XCube 针对这一瓶颈，提出**层级化稀疏体素潜在扩散模型**，将复杂的三维生成任务分解为由粗到细的多级条件子任务——每一层级仅需建模局部几何细节，从而在高达 $1024^3$ 的有效分辨率下实现实时生成。

### 方法定位

XCube 属于**稀疏体素层级生成模型**，其核心设计包含三个关键组件：

- **稀疏体素层级结构**：将三维形状表示为 $L$ 层由粗到细的稀疏体素网格 $\mathcal{G} = \{ \mathbf{G}_1, \dots, \mathbf{G}_L \}$ 及逐体素属性 $\mathcal{A}$，细网格严格嵌套于粗网格内。
- **稀疏结构 VAE**：对每一层级的体素网格和属性进行紧凑潜在编码，解码器通过渐进式修剪与细分（progressive pruning and subdividing）从潜在变量逐步恢复高分辨率结构。
- **层级潜在扩散模型**：在潜在空间中对每一层执行扩散/去噪过程，以上一层级的生成结果作为条件（式 1–2），形成马尔可夫链式的级联生成。

在底层计算上，XCube 构建了基于 NanoVDB 的自定义稀疏三维深度学习框架，相比通用稀疏卷积库 TorchSparse，在 $1024^3$ 网格上内存占用降低约 92%（8.4 MB vs 104.6 MB），前向时间缩短约 66.5%（149.6 ms vs 446.0 ms），为高分辨率实时生成提供了工程基础。

### 主要结果摘要

- **ShapeNet 无条件生成**：在 Airplane、Chair、Car 三个类别上，XCube 在 1-NNA CD/EMD 指标上全面超越 NFD、LION、NWD、LAS-Diffusion 等基线方法（Table 1），其中 Airplane 1-NNA CD 降至 52.85（NFD 为 57.55）。
- **Objaverse 文字到三维**：用户研究中 79.2% 的比较倾向于 XCube 生成的形状，显著优于 Shap·E（§4.2）。
- **Waymo 场景生成**：用户研究中 66.3% 的比较认为 XCube 生成的场景比真实数据更真实（§4.3），验证了其在大规模室外场景上的生成能力。
- **消融实验**：层级化模型（2 层或 3 层）在 1-NNA 指标上均优于单层基线；渐进式修剪将网格 IoU 从 89.68% 提升至 92.88% 并节省约 3 倍 GPU 内存（§4.4）。

### 局限与开放问题

当前三维数据集规模仍远不及二维图像数据集，导致文字到三维模型难以处理复杂提示词；层级式建模存在误差累积问题，粗层级误差会向下传播。未来方向包括将纯三维先验与二维图像先验有效结合以提升纹理和语义生成质量，以及将 XCube 迁移到图像条件重建、多模态感知等下游任务。

三维生成建模是计算机视觉与图形学领域的核心挑战之一，其目标是从无到有地合成逼真且多样化的三维形状与场景。近年来，扩散模型在二维图像生成领域取得了革命性突破，这一成功也推动了三维生成模型的快速发展。然而，将扩散模型从二维迁移至三维面临着根本性的维度诅咒——三维数据的计算与存储需求随分辨率呈立方增长，使得现有方法普遍受困于低分辨率先验。

**核心瓶颈在于三维表示的选择与生成架构的可扩展性。** 现有三维生成模型主要采用以下表示方式：

- **点云方法**（如 **PVD**、**LION**）直接对非结构化点集进行扩散，虽具备表示灵活性，但缺乏拓扑信息且难以保证表面质量，在复杂几何结构上表现受限。
- **三平面方法**（如 **NFD**）将三维几何压缩至三个正交特征平面，通过二维扩散间接生成三维内容。这类方法虽受益于二维扩散的成熟技术，但三平面表示的容量有限，难以捕捉精细的局部几何细节。
- **密集体素方法**（如 **NWD**）直接对规则体素网格进行建模，但内存消耗随分辨率立方增长，实际可处理的分辨率通常不超过128³，远不足以表示大规模室外场景（如自动驾驶数据中常见的1024³级别）。
- **稀疏体素方法**（如 **LAS-Diffusion**）通过仅存储占用体素来缓解内存压力，但现有工作仍采用单层生成架构，未能充分利用稀疏结构在多尺度建模中的潜力。

上述方法的共同缺陷在于：**生成架构均为单层扩散模型，试图在单一尺度上一次性完成高分辨率生成。** 这种“一步到位”的策略在面对大规模场景时，不仅计算成本高昂，更难以同时捕捉全局布局与局部细节。以自动驾驶场景为例，一个典型的Waymo场景在1024³分辨率下包含数万个体素，需要同时建模道路、车辆、行人、建筑等多类物体的几何形状与语义属性，单层模型在此任务上几乎不可行。

**XCube的核心动机正是突破这一可扩展性瓶颈。** 论文提出将复杂的三维生成任务分解为一系列条件更简单的子任务——通过层级化稀疏体素潜在扩散模型，以由粗到细的方式逐层构建高分辨率体素网格。这一设计的直觉在于：粗层级负责全局结构与拓扑，细层级仅需在上层基础上补充局部几何细节，每层模型的条件空间被显著简化。同时，通过引入基于NanoVDB的自定义稀疏三维深度学习框架，XCube得以在毫秒级时间内处理1024³分辨率的稀疏网格，使大规模场景的实时生成成为可能。

此外，当前三维生成模型在**属性建模**方面也存在明显缺口。大多数方法仅生成几何形状，忽略了法线、语义标签、TSDF等对下游应用至关重要的表面属性。XCube通过在体素层级中统一编码几何与属性信息，实现了多属性联合生成，为场景理解、仿真模拟等任务提供了更丰富的输出形式。

综上，XCube的提出旨在回答一个关键问题：**能否设计一种三维生成模型，使其先验表示既能支持高分辨率（1024³级别）的大规模场景，又能在生成质量上超越现有方法？** 这一问题的解答不仅关乎生成模型本身的性能边界，更决定了三维生成技术能否真正应用于自动驾驶、机器人仿真等真实世界场景。

## 核心方法与创新机理

XCube 的核心创新在于通过**稀疏体素层级结构（Sparse Voxel Hierarchy）**将高分辨率 3D 生成这一复杂任务分解为一系列条件更简单的子任务，从而突破了现有方法在分辨率与场景规模上的瓶颈。以下从五个关键维度展开其相对于 baseline 的差异化设计。

### 1. 由粗到细的层级化生成架构

现有 3D 生成模型（如 **NFD**、**LION**、**NWD**）普遍采用单层潜在扩散模型，一次性地从噪声中生成整个 3D 表示，这导致模型容量与分辨率之间存在尖锐矛盾——要提升分辨率就必须成倍增加计算开销。XCube 将这一过程重构为 $L$ 层级联结构，每一层以上一层生成的几何与属性为条件，逐步细化体素网格。联合分布被显式分解为：

$$p ( \mathcal{G}, \mathcal{A}, \mathcal{X} ) = \prod_{l=1}^{L} p_{\psi_l} ( \mathbf{G}_l, \mathbf{A}_l | \mathbf{X}_l ) \, p_{\theta_l} ( \mathbf{X}_l | \mathbf{C}_{l-1} )$$

其中条件 $\mathbf{C}_{l-1}$ 在 $l>1$ 时融合了上一层的几何 $\mathbf{G}_{l-1}$、属性 $\mathbf{A}_{l-1}$ 与全局条件 $c$，形成了马尔可夫式的层级依赖。消融实验（Table 2）直接验证了这一设计的必要性：2 层或 3 层模型在 1-NNA 指标上均显著优于单层模型，且 2 层与 3 层性能相当，说明层级分解本身是增益来源，而非单纯的容量增加。

### 2. 稀疏体素层级表示：突破分辨率上限

Baseline 方法受限于密集体素（如 **NWD**）、点云（如 **PVD**、**LION**）或三平面（如 **NFD**）表示，有效分辨率通常不超过 $256^3$。XCube 采用稀疏体素层级结构，每层仅存储被占据的体素及其潜在特征，使得有效分辨率可达 $1024^3$，同时保持存储和计算的高度稀疏性。Finer grids $\mathbf{G}_{l+1}$ 严格包含于 coarser grids $\mathbf{G}_l$ 内，这一约束不仅保证了层级间的几何一致性，还使得模型能够集中容量于物体表面区域，而非在空白空间中浪费计算。

### 3. 稀疏结构 VAE：从体素到紧凑潜在空间

不同于直接对几何表示进行扩散或使用非稀疏 VAE 的 baseline 方案，XCube 为每一层级单独设计了**稀疏结构 VAE**。其编码器将体素网格 $\mathbf{G}_l$ 及关联属性 $\mathbf{A}_l$ 压缩为低维潜在变量 $\mathbf{X}_l$，解码器则通过**渐进式修剪与细分（progressive pruning and subdividing）**从潜在变量逐步恢复高分辨率结构：从 $\mathbf{X}_l$ 出发，迭代地对现有体素进行八叉细分（subdividing）并剪除多余体素（pruning），基于 subdivision mask 的预测来决定每个体素的去留。消融实验表明，移除渐进式修剪会导致网格 IoU 从 92.88% 降至 89.68%，同时 GPU 内存占用增加约 3 倍，验证了该设计在精度与效率上的双重价值。

### 4. 自定义稀疏计算框架：底层效率跃升

通用稀疏卷积库（如 **TorchSparse**）在设计上未针对体素层级结构进行优化，导致在处理 $1024^3$ 网格时内存和速度均成为瓶颈。XCube 基于 NanoVDB 构建了自定义的稀疏 3D 深度学习框架，完全在 GPU 端完成网格构建、卷积与池化等操作。在 $1024^3$ 分辨率下的基准测试（Table 3）中，该框架仅需 **8.4 MB** 内存（TorchSparse 为 104.6 MB），单次卷积前向时间仅 **149.6 ms**（TorchSparse 为 446.0 ms），内存和速度分别降低了约 92% 和 66%。这一效率优势是 XCube 能够在 30 秒内生成完整 $1024^3$ 场景的工程基础。

### 5. 层级条件机制与错误累积缓解

层级式建模的固有风险在于粗层级的误差会向细层级传播并放大。XCube 在两方面应对这一问题：其一，每层扩散模型以 $v$-参数化训练，最小化预测 $v_{\theta_l}$ 与参考 $v_{\mathrm{ref}}$ 之间的 L2 误差，提供更稳定的去噪梯度；其二，引入**细化网络（Refinement Network）**对解码后的体素网格进行后处理，修正因子分解建模导致的累积误差。尽管该网络无法完全消除错误传播（这仍是论文明确指出的局限之一），但在实践中已使层级模型在 1-NNA 指标上稳定超越单层 baseline。

### 小结

XCube 的创新并非单一技术点的突破，而是从**表示（稀疏体素层级）、架构（层级扩散）、编码（稀疏结构 VAE）、解码（渐进修剪细分）到底层计算框架**的系统性重构。这五个维度的协同使得模型首次能够在 $1024^3$ 分辨率下实时生成大规模室外场景，并在 ShapeNet、Objaverse 和 Waymo 等多个基准上取得 state-of-the-art 的生成质量。

XCube 的核心是一个**层级化稀疏体素潜在扩散模型**（Hierarchical Voxel Latent Diffusion Model），它将大规模三维生成任务分解为由粗到细（coarse-to-fine）的级联过程。整个 pipeline 围绕一个核心数据结构——**稀疏体素层级**（Sparse Voxel Hierarchy）——展开，该层级由 $L$ 层分辨率递增的稀疏体素网格 $\mathcal{G} = \{ \mathbf{G}_1, ..., \mathbf{G}_L \}$ 及其关联的逐体素属性 $\mathcal{A} = \{ \mathbf{A}_1, ..., \mathbf{A}_L \}$ 组成。细网格 $\mathbf{G}_{l+1}$ 被严格约束在粗网格 $\mathbf{G}_l$ 的几何范围内，形成空间上的嵌套关系。

### 模块拓扑与数据流

整体框架由三个核心模块串联而成，数据流严格遵循“编码→生成→解码”的层级递进逻辑：

1. **稀疏结构 VAE 编码器**（Sparse Structure VAE Encoder）：负责将每一层级的体素网格 $\mathbf{G}_l$ 及其属性 $\mathbf{A}_l$ 压缩为紧凑的潜在表示 $\mathbf{X}_l$。编码器独立作用于每个层级，产出低维潜在变量，为后续扩散模型提供高效的操作空间。

2. **层级化潜在扩散模型**（Hierarchical Voxel Latent Diffusion Model）：在潜在空间中逐层执行扩散与去噪过程。该模块的核心机制是将联合分布按层级因式分解为马尔可夫条件链：
   $$p ( \mathcal { G } , \mathcal { A } , \mathcal { X } ) = \prod _ { l = 1 } ^ { L } p _ { \psi _ { l } } ( \mathbf { G } _ { l } , \mathbf { A } _ { l } | \mathbf { X } _ { l } ) p _ { \theta _ { l } } ( \mathbf { X } _ { l } | \mathbf { C } _ { l - 1 } )$$
   其中每一层的扩散模型 $p_{\theta_l}$ 以上一层级条件 $\mathbf{C}_{l-1}$ 为输入，生成当前层的潜在变量 $\mathbf{X}_l$。条件 $\mathbf{C}_l$ 定义为：
   $$\mathbf { C } _ { l } = \left\{ \begin{array} { l l } { c , } & { l = 0 } \\ { \{ \mathbf { G } _ { l } , \mathbf { A } _ { l } , c \} , } & { l > 0 } \end{array} \right.$$
   最粗层级（$l=1$）仅依赖全局条件 $c$（如类别标签或文本嵌入），后续层级则将上一层的几何 $\mathbf{G}_l$、属性 $\mathbf{A}_l$ 与全局条件融合，逐步注入更精细的结构信息。扩散过程采用 **v-参数化**，训练目标为最小化预测速度 $\pmb{v}_{\theta_l}$ 与参考速度 $\pmb{v}_{\mathrm{ref}}$ 之间的 L2 误差：
   $$\mathcal { L } _ { l } ^ { \mathrm { D M } } = \mathbb { E } _ { t , \mathbf { X } _ { l } , \epsilon \sim \mathcal { N } ( \mathbf { 0 } , \mathbf { I } ) } \left[ \| \pmb { v } _ { \theta _ { l } } ( \mathbf { X } _ { l , t } , t ) - \pmb { v } _ { \mathrm { r e f } } \| _ { 2 } ^ { 2 } \right]$$

3. **稀疏结构 VAE 解码器**（含渐进式修剪与细分）：从潜在变量 $\mathbf{X}_l$ 出发，通过**渐进式修剪**（progressive pruning）和**细分**（subdividing）操作，逐层恢复高分辨率体素网格 $\tilde{\mathbf{G}}_l$ 及属性 $\tilde{\mathbf{A}}_l$。解码器以粗网格为骨架，迭代地将现有体素细分为八分体（octants），并基于细分掩码（subdivision mask）的预测剪除多余体素，从而在保持稀疏性的同时捕捉局部几何细节。

4. **细化网络**（Refinement Network）：作为后处理模块，修正层级因式分解导致的误差累积，提升最终重建质量。

### 底层计算支撑

整个框架构建在基于 **NanoVDB** 的自定义稀疏三维深度学习框架之上。该框架在 GPU 端实现了高效的稀疏卷积、池化等常用神经操作，使得处理 $1024^3$ 分辨率的场景仅需 **8.4 MB** 显存和 **149.6 ms** 的前向时间，相较于 TorchSparse（104.6 MB, 446.0 ms）有数量级的效率优势（Table 3）。这一计算瓶颈的突破，是 XCube 能够将生成分辨率推至 $1024^3$ 并保持实时性的关键使能因素。

### 训练策略

VAE 与扩散模型采用**逐层级独立训练**（level-by-level independent training）策略。每层的 VAE 损失由网格重建二值交叉熵、属性损失和 KL 正则项加权组成：
$$\mathcal { L } _ { l } ^ { \mathrm { v A E } } = \mathbb { E } _ { \{ { \mathbf { G } _ { l } } , { \mathbf { A } _ { l } } \} } [ \mathbb { E } _ { { \mathbf { X } } _ { l } \sim q _ { \phi } } [ { \mathrm { B C E } } ( { \mathbf { G } _ { l } } , \tilde { \mathbf { G } } _ { l } ) + \mathcal { L } _ { l } ^ { \mathrm { A t t r } } ( { \mathbf { A } _ { l } } , \tilde { \mathbf { A } } _ { l } ) ] + \lambda \mathbb { K L } ( q _ { \phi } ( { \mathbf { X } _ { l } } ) \parallel p ( { \mathbf { X } _ { l } } ) ) ]$$
这种解耦训练方式降低了优化难度，使得每一层级只需专注于建模其分辨率尺度下的几何细节。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2312_03806/figures/002_Figure_2.jpg]]
*Figure 2: Method. Sparse voxel grids within the hierarchy are first encoded into compact latent representations using a sparse structure VAE. The hierarchical latent diffusion model then learns to generate each level of the latent representation conditioned on the coarser level in a cascaded fashion. The generated high-resolution voxel grids contain various attributes for different applications. Note that technically X1 is a dense latent grid, but illustrated as a sparse one for clarity. G G1+1*

XCube 的核心生成框架由三个关键模块串联构成：**稀疏结构 VAE** 负责将各层级体素网格压缩至紧凑潜在空间；**层次化潜在扩散模型** 在潜在空间中逐层执行去噪生成；**渐进式修剪与细分解码器** 从潜在变量重建高分辨率体素网格。三者协同实现从粗到细的层级式生成。

### 3.1 稀疏结构 VAE

稀疏结构 VAE 的设计目标是学习每一层级体素网格 $\mathbf{G}_l$ 及其关联属性 $\mathbf{A}_l$ 的紧凑潜在表示 $\mathbf{X}_l$。其编码器 $q_\phi$ 将稀疏体素网格映射到低维潜在空间，解码器 $p_\psi$ 则从潜在变量重建网格与属性。解码器采用独特的**渐进式修剪与细分**机制：从潜在变量 $\mathbf{X}_l$ 出发，通过预测细分掩码（subdivision mask）迭代地将现有体素细分为八分体（octants），同时剪除冗余体素，逐步恢复从粗到细的体素结构（Figure 3）。这一设计将三维归纳偏置直接注入解码过程，是保留表面细节的关键。

### 3.2 层次化潜在扩散模型

层次化潜在扩散模型将联合分布 $p(\mathcal{G}, \mathcal{A}, \mathcal{X})$ 分解为各级条件模型的乘积，体现层级马尔科夫结构：

$$p ( \mathcal { G } , \mathcal { A } , \mathcal { X } ) = \prod _ { l = 1 } ^ { L } p _ { \psi _ { l } } ( \mathbf { G } _ { l } , \mathbf { A } _ { l } | \mathbf { X } _ { l } ) p _ { \theta _ { l } } ( \mathbf { X } _ { l } | \mathbf { C } _ { l - 1 } )$$

其中 $p_{\psi_l}$ 为第 $l$ 级 VAE 解码器，$p_{\theta_l}$ 为第 $l$ 级潜在扩散模型。条件 $\mathbf{C}_l$ 的定义如下：

$$\mathbf { C } _ { l } = \left\{ \begin{array} { l l } { c , } & { l = 0 } \\ { \{ \mathbf { G } _ { l } , \mathbf { A } _ { l } , c \} , } & { l > 0 } \end{array} \right.$$

最粗层级（$l=0$）仅使用全局条件 $c$（如类别标签或文本嵌入），后续层级则融合上一级的几何 $\mathbf{G}_l$、属性 $\mathbf{A}_l$ 与全局条件 $c$。这种分解将复杂的高分辨率生成任务拆解为多个条件更简单的子任务：每一层级仅需建模当前分辨率下的局部几何细节，以上一层输出为条件。

### 3.3 训练目标

VAE 与扩散模型采用**逐层独立训练**策略。第 $l$ 级 VAE 的损失函数为：

$$\mathcal { L } _ { l } ^ { \mathrm { v A E } } = \mathbb { E } _ { \{ { \mathbf { G } _ { l } } , { \mathbf { A } _ { l } } \} } [ \mathbb { E } _ { { \mathbf { X } } _ { l } \sim q _ { \phi } } [ { \mathrm { B C E } } ( { \mathbf { G } _ { l } } , \tilde { \mathbf { G } } _ { l } ) + \mathcal { L } _ { l } ^ { \mathrm { A t t r } } ( { \mathbf { A } _ { l } } , \tilde { \mathbf { A } } _ { l } ) ] + \lambda \mathbb { K L } ( q _ { \phi } ( { \mathbf { X } _ { l } } ) \parallel p ( { \mathbf { X } _ { l } } ) ) ]$$

该损失由三部分组成：网格重建的二值交叉熵 $\mathrm{BCE}$、属性重建损失 $\mathcal{L}_l^{\mathrm{Attr}}$，以及潜在分布与先验分布之间的 KL 散度正则项（权重 $\lambda$）。

第 $l$ 级扩散模型采用 **v-参数化**，训练目标为最小化预测速度 $\pmb{v}_{\theta_l}$ 与参考速度 $\pmb{v}_{\mathrm{ref}}$ 之间的 L2 误差：

$$\mathcal { L } _ { l } ^ { \mathrm { D M } } = \mathbb { E } _ { t , \mathbf { X } _ { l } , \epsilon \sim \mathcal { N } ( \mathbf { 0 } , \mathbf { I } ) } \left[ \| \pmb { v } _ { \theta _ { l } } ( \mathbf { X } _ { l , t } , t ) - \pmb { v } _ { \mathrm { r e f } } \| _ { 2 } ^ { 2 } \right]$$

属性损失 $\mathcal{L}^{\mathrm{Attr}}$ 由三项加权组合构成（详见附录 Eq. 8）：

$$\mathcal { L } ^ { \mathrm { A t r } } = \lambda _ { 1 } \underbrace { | | n - n _ { \mathrm { G T } } | | _ { 2 } ^ { 2 } } _ { \mathrm { n o r m a l ~ l o s s } } + \lambda _ { 2 } \underbrace { \mathrm { B C E } ( s , s _ { \mathrm { G T } } ) } _ { \mathrm { s e m a n t i c ~ l o s s } } + \lambda _ { 3 } \underbrace { \mathbb { E } _ { { \mathbf x } \in \mathbb { R } ^ { 3 } } | | f ( x ) - \mathrm { T S D F } ( x , X _ { \mathrm { G T } } ) | | _ { 1 } } _ { \mathrm { s u r f a c e ~ l o s s } }$$

其中法线损失与语义损失直接监督体素属性，表面损失通过神经核函数 $f(\pmb{x})$ 拟合连续 TSDF 值，实现任意位置的表面查询（Eq. 9）。

### 3.4 细化网络与计算框架

层级式分解虽降低了建模难度，但存在**错误累积**问题：高层级的重建误差会向下传播，影响最终细节。为此，XCube 引入一个轻量级**细化网络**（Refinement Network），在各级解码后对潜在变量进行修正，缓解因子分解建模导致的误差传播。

在底层计算方面，XCube 基于 NanoVDB 构建了自定义稀疏 3D 深度学习框架，实现了高效的稀疏卷积、池化等操作。与通用稀疏卷积库 TorchSparse 相比，该框架在处理 $1024^3$ 网格时内存占用仅 8.4 MB（TorchSparse 为 104.6 MB），前向卷积时间 149.6 ms（TorchSparse 为 446.0 ms），速度提升约 3 倍，内存节省约 92%（Table 3），为高分辨率实时生成提供了关键支撑。

> **⚠️ 手动验证提示**：以上公式均来自原论文（Eq. 1, 2, 6, 7, 8），变量含义与模块功能描述基于 §3.1–§3.4 的文本证据。细化网络的具体架构细节（层数、参数量）在已验证分析中未提供，需要查阅原论文补充。

## 实验与关键发现

### 核心定量结果

**ShapeNet 无条件生成。** XCube 在 ShapeNet 三个代表性类别（飞机、椅子、汽车）上均取得最优 1-NNA 分数（Table 1）。以 1-NNA CD 为例，飞机类别达到 **52.85**，相较此前最优的 NFD（57.55）降低 4.70；椅子类别 CD 为 53.99，EMD 为 **48.60**（NFD 为 54.06）；汽车类别 CD 为 **57.96**（LION 为 60.61）。1-NNA 越低表示生成分布与真实分布越接近，50% 为理论最优。XCube 在所有六个指标（三类 × CD/EMD）上均超越包括点云方法（PVD、LION）、三平面方法（NFD）、密集体素方法（NWD）、稀疏体素方法（LAS-Diffusion）及非结构化潜在方法（3DShape2VecSet）在内的全部基线。

**文字到 3D 生成（Objaverse）。** 在用户偏好研究中，79.2% 的比较倾向于 XCube 生成的形状，而非 Shap·E（无纹理版本），优势幅度达 +29.2%（§4.2 Evaluation）。定性结果（Figure 7、Figure 8）显示 XCube 能生成与提示词更匹配的高质量形状，且对同一提示词可产生多样化输出（Figure 9）。

**大规模场景生成（Waymo）。** 在无条件场景生成的用户研究中，66.3% 的比较认为 XCube 生成的场景比真实数据更真实（§4.3 Evaluation），即生成质量在感知上超越 ground truth。Figure 10 展示了无条件生成样本，Figure 11 展示了单帧 LiDAR 条件生成结果——给定左侧输入扫描，XCube 能补全出合理的三维语义网格。

### 消融实验

**层次化结构的关键性。** Table 2 的消融对比了不同分辨率和层级深度的配置。结果表明，层次化模型（2 层或 3 层）在 1-NNA 指标上均显著优于单层模型，且 2 层与 3 层性能相当。这验证了稀疏体素层级将复杂生成任务分解为条件更简单的子任务这一核心设计动机。

**渐进式修剪的作用。** 移除渐进式修剪（progressive pruning）后，网格重建 IoU 从 **92.88% 降至 89.68%**，同时 GPU 内存消耗增加约 3 倍（§4.4 Progressive Pruning）。这表明渐进式修剪不仅对保留形状细节和注入 3D 归纳偏置至关重要，也是维持高分辨率下内存效率的关键机制。

### 底层框架效率

Table 3 报告了自定义稀疏框架与 TorchSparse 的性能对比。在处理 $1024^3$ 网格时，自定义框架的内存占用仅为 **8.4 MB**（TorchSparse 为 104.6 MB），稀疏卷积前向时间仅需 **149.6 ms**（TorchSparse 为 446.0 ms），内存节省约 92%，速度提升约 3 倍。这一效率优势源于基于 NanoVDB 的自定义 VDB 稀疏操作库，使得在消费级 GPU 上实时生成 $1024^3$ 分辨率场景成为可能。

### 关键定性发现

**细节生成能力。** Figure 5 的近距离视图展示了 XCube 生成的体素网格（按预测法线着色）能捕捉汽车内饰、飞机螺旋桨等精细结构，验证了稀疏体素层级在高分辨率下保留表面细节的能力。

**用户交互编辑。** Figure 6 展示了通过添加（绿色）或删除（红色）粗层级体素来控制细粒度形状的交互编辑能力——粗层级的稀疏编辑可传播至更精细层级，产生符合直觉的全局形状变化。

**形状新颖性。** Figure 15 的新颖性分析表明，从生成形状出发，在训练集中按倒角距离检索的最相似样本仍存在明显差异，说明模型并非简单记忆训练数据。

### 失败模式与局限

尽管整体性能优异，论文明确指出以下局限：层级式建模存在**错误累积**问题——即使使用了细化网络（Refinement Network），粗层级的误差仍会向下传播，可能影响最终细节质量（§3.4）。此外，当前 3D 数据集规模远不及 2D 图像数据集，导致文字到 3D 模型在处理复杂提示词时能力受限。生成速度与显存消耗虽已显著优化，但在极大规模场景或多层级交互式应用中仍有提升空间。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2312_03806/figures/004_Figure.jpg]]

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2312_03806/figures/017_Figure.jpg]]

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2312_03806/figures/020_Figure_16.jpg]]
*Figure 16: More qualitative results on text-to-3D*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2312_03806/figures/005_Table_1.jpg]]
*Table 1: 1-NNA Comparison on ShapeNet [5]. The lower the better. Best scores highlighted in bold*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2312_03806/figures/012_Table.jpg]]

## 定位与知识库关联

### 1. 方法对比与关键差异

XCube 的核心突破在于将大规模3D生成任务分解为**层级化稀疏体素潜在扩散模型**，这与现有方法在三个维度上形成显著差异。

**生成架构：从单层到层级。** 现有主流3D生成模型（如 PVD、LION、NFD、NWD、LAS-Diffusion、3DShape2VecSet）均采用单层潜在扩散架构，直接对完整形状的潜在表示进行去噪生成。XCube 则将联合分布因子分解为 $L$ 层条件模型（Eq. 1），每一层仅需建模当前分辨率的局部几何细节，以上一层输出为条件（Eq. 2）。消融实验直接验证了这一设计的必要性：层次化模型在1-NNA指标上全面优于单层模型，且2层与3层性能相当（Table 2），表明层级分解有效降低了单层建模的难度。

**3D表示：从密集到稀疏层级。** 基于密集体素的方法（如 NWD）受限于 $64^3$ 或 $128^3$ 分辨率，基于点云的方法（PVD、LION）虽不受网格约束但缺乏结构化先验，三平面方法（NFD）则在压缩与细节保留间存在权衡。XCube 采用稀疏体素层级结构，有效分辨率可达 $1024^3$，同时通过 VDB 数据结构实现高效存储与计算。自定义稀疏框架在处理 $1024^3$ 网格时，内存仅需 8.4MB（对比 TorchSparse 的 104.6MB），前向时间 149.6ms（对比 446.0ms），效率提升约 3 倍（Table 3）。

**解码策略：从一次性上采样到渐进式修剪与细分。** 传统 VAE 解码器通常使用反卷积或插值一次性恢复高分辨率结构。XCube 的解码器采用迭代的“细分-修剪”机制（Figure 3）：从潜在变量出发，逐步将现有体素细分为八分体，同时基于细分掩码预测修剪冗余体素。消融实验表明，移除渐进式修剪后，网格 IoU 从 92.88% 降至 89.68%，且 GPU 内存消耗增加约 3 倍（§4.4），证明该设计同时提升了重建精度与计算效率。

### 2. 在知识谱系中的位置

XCube 处于**稀疏表示学习**与**层级生成模型**的交叉点。

在稀疏表示方面，XCube 继承了 VDB 数据结构的工业级效率，但将其首次引入深度学习生成管线。与 LAS-Diffusion 等早期稀疏体素扩散方法相比，XCube 的稀疏操作完全在 GPU 上执行（包括网格构建），避免了 CPU-GPU 数据传输瓶颈。

在层级生成方面，XCube 延续了级联扩散模型（cascaded diffusion）的思想，但将其从 2D 像素空间迁移至 3D 体素空间，并通过稀疏性解决了直接在高分辨率下建模的计算不可行性。与 Shape·E 等基于 NeRF 或隐式表示的文字到3D方法相比，XCube 生成的显式稀疏体素层级天然支持用户交互编辑（Figure 6）和后续纹理合成（Figure 14）。

### 3. 适用边界与局限

**数据规模约束。** 当前3D数据集（ShapeNet、Objaverse）的规模远不及2D图像数据集，导致文字到3D模型在处理复杂、组合式提示词时表现受限（§5 Limitations）。模型对训练分布外概念的泛化能力仍需更大规模数据的验证。

**错误累积问题。** 层级式建模的固有风险在于粗层级的误差会传播至细层级。尽管 XCube 引入了细化网络（Refinement Network）来缓解这一问题，但高层次的结构性错误（如错误的拓扑连接）仍可能在下游层级中表现为不可修复的细节失真。

**计算效率边界。** 尽管自定义稀疏框架已显著优化，在极大规模场景（如城市级重建）或需要多个层级交互式编辑的应用中，生成速度与内存消耗仍有提升空间。当前 $1024^3$ 分辨率下的 30 秒生成时间虽已实用，但实时交互场景仍需进一步压缩。

### 4. 开放问题

**多模态先验融合。** 如何将 XCube 的纯3D先验与2D图像先验（如 Stable Diffusion）有效结合，以提升纹理质量和语义一致性，是一个自然的研究方向。当前纹理合成依赖后处理管线（TEXTure），端到端的多模态联合生成可能带来更协调的结果。

**下游任务迁移。** XCube 作为基础生成模型，其在图像条件重建、多模态感知（如激光雷达补全、语义场景补全）等任务上的迁移能力尚未充分探索。微条件机制（micro-conditioning，Figure 13）已展示了控制生成的潜力，但针对更复杂的条件信号（如多视角图像、文本描述）的设计空间仍待开拓。

**稀疏结构的设计空间。** 针对真实世界数据中稀疏性分布不均的特点（如自动驾驶场景中近处密集、远处稀疏），层级深度、体素分辨率分配策略以及微条件机制的设计空间值得进一步探索。自适应层级结构可能比固定层数配置更适应多样化场景。

## 原文 PDF

![[paperPDFs/CVPR_2024/Large_Scale_3D_Generative_Modeling_using_Sparse_Voxel_Hierarchies.pdf]]
