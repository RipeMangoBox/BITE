---
title: "PartDiffuser: Part-wise 3D Mesh Generation via Discrete Diffusion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PartDiffuser_Part_wise_3D_Mesh_Generation_via_Discrete_Diffusion.pdf
project_link: null
code_link: null
aliases:
- PartDiffuser
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将网格生成解耦为部件间自回归（保证全局拓扑）与部件内并行离散扩散（保留局部细节），通过层次化几何条件动态控制生成。
primary_logic: 语义部件分割使全局拓扑可由部件级自回归依赖建模，而部件内并行扩散可精细重建高频几何特征，从而化解长序列生成中的全局-局部冲突与误差传播。
claims:
- 在Objaverse数据集上，PartDiffuser的Chamfer距离（CD×10³）为17.813，相比MeshAnythingV2改进约27%
- 消融实验中，仅用全局特征（w/ Global only）CD升至29.125，仅用局部特征（w/ Parts only）CD升至54.728，表明层次条件缺一不可
- Objaverse 上 Chamfer Distance (CD×10³)↓ = 17.813
- Objaverse 上 F1-Score↑ = 0.343
---

# PartDiffuser: Part-wise 3D Mesh Generation via Discrete Diffusion

> [!tip] 核心洞察
> 语义部件分割使全局拓扑可由部件级自回归依赖建模，而部件内并行扩散可精细重建高频几何特征，从而化解长序列生成中的全局-局部冲突与误差传播。

| 字段 | 内容 |
|------|------|
| 中文题名 | PartDiffuser：基于离散扩散的部件级三维网格生成 |
| 英文题名 | PartDiffuser: Part-wise 3D Mesh Generation via Discrete Diffusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.18801) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | PartDiffuser |
| Dataset | Objaverse, 3DFront |

> [!tip] 效果简介
> - Objaverse 上，Chamfer Distance (CD×10³)↓ 17.813 vs ~24.4 (MeshAnythingV2) (-27%)；F1-Score↑ 0.343 vs MeshAnythingV2 (second best) (+~20%)。
> - 3DFront 上，CD×10³↓ 6.461 vs 其他最佳基线 (最佳)；HD↓ 0.147 vs 其他最佳基线 (最佳)；EMD↓ 0.068 vs 其他最佳基线 (最佳)。

## 概要

从点云重建三维网格是计算机视觉与图形学中的基础任务。现有主流方法采用令牌级自回归生成，将网格面片序列化为离散令牌后逐令牌预测。然而，这类方法面临一个根本性瓶颈：**长序列自回归生成难以同时兼顾全局拓扑一致性与高频局部细节，且存在误差累积问题**，导致生成的网格在精细结构处出现断裂或扭曲。

针对上述挑战，本文提出 **PartDiffuser**，一种面向点云到网格生成的半自回归离散扩散框架。其核心思路是将网格生成解耦为两个层次：**部件间自回归**（保证全局拓扑）与**部件内并行离散扩散**（保留局部细节），通过层次化几何条件动态控制生成过程。这一设计的关键洞察在于：语义部件分割使全局拓扑可由部件级自回归依赖建模，而部件内并行扩散可精细重建高频几何特征，从而化解长序列生成中的全局-局部冲突与误差传播。

在 Objaverse 数据集上，PartDiffuser 的 Chamfer Distance（CD×10³）达到 17.813，相比 **MeshAnythingV2** 改进约 27%；F1-Score 达到 0.343，领先次优方法约 20%。消融实验进一步验证了层次几何条件的关键作用：仅使用全局特征时 CD 升至 29.125，仅使用局部特征时 CD 恶化至 54.728，表明全局形状先验与部件级细节引导缺一不可。

在方法谱系上，PartDiffuser 相较于现有工作做出了以下关键改变：

| 设计维度 | 基线方法（令牌级自回归） | PartDiffuser |
|---------|----------------------|--------------|
| **生成范式** | 令牌级自回归生成 | 部件级半自回归离散扩散（部件间自回归，部件内并行扩散） |
| **几何条件注入** | 通常使用全局点云特征或无分级条件 | 层次化几何条件（全局形状特征 + 部件局部特征），通过交叉注意力动态注入每个去噪块 |
| **注意力掩码** | 标准因果掩码 | 复合材料掩码（块扩散掩码 + 块感知填充掩码），块内双向注意力、块间自回归注意力 |
| **训练策略** | 因果语言建模 | 掩码离散扩散并行训练（两阶段课程：裁剪噪声调度与全线性调度） |

整体而言，PartDiffuser 通过“分而治之”的部件级建模策略，在点云条件网格生成任务上实现了对现有自回归方法的显著超越，同时为离散扩散模型在三维生成领域的应用提供了新的范式。

三维网格（3D Mesh）是计算机图形学、增强现实与机器人等领域的基础表示形式。然而，从原始点云自动生成高质量、结构规整的网格仍是一项开放挑战。现有方法主要分为两类：一类依赖于复杂的优化与后处理管线，难以端到端扩展；另一类将网格生成建模为令牌级（token-level）的自回归序列生成任务，虽能捕捉拓扑结构，却面临**全局拓扑一致性与高频局部细节之间的根本冲突**。

自回归生成范式存在两个结构性缺陷。其一，长序列生成中的**误差累积**——早期令牌的预测偏差会沿序列传播，导致后续几何结构失真。其二，标准因果注意力掩码强制单向依赖，使得模型在生成局部细节时无法充分利用全局上下文，反之亦然。尽管近期工作如 **MeshAnythingV2**、**BPT** 和 **TreeMeshGPT** 在点云条件网格生成上取得了进展，它们本质上仍受限于令牌级自回归框架，难以同时保证整体形状的拓扑合理性与局部曲面的精细度。

PartDiffuser 的核心洞察在于：**语义部件分割**为化解这一冲突提供了天然的结构先验。三维物体的全局拓扑可由部件间的自回归依赖关系有效建模，而每个部件内部的高频几何特征则可通过并行扩散过程精细重建。这种“部件间自回归、部件内并行扩散”的半自回归范式，将长序列生成问题解耦为多个短序列的并行去噪任务，从根本上缓解了误差传播，并允许模型在部件级别动态融合全局形状条件与局部几何条件。

本文据此提出 PartDiffuser——一个面向点云到网格生成的半自回归离散扩散框架。该方法首先对输入点云与目标网格进行语义分割，将网格序列化为定长的部件令牌块；随后，通过层次化几何条件编码器提取全局形状特征与部件级局部特征，并在扩散去噪过程中以交叉注意力动态注入。这一设计使 PartDiffuser 在 Objaverse 等大规模数据集上显著超越了现有最优基线，Chamfer 距离（CD×10³）降至 17.813，相较 MeshAnythingV2 改进约 27%，验证了部件级半自回归扩散范式的有效性。

## 核心方法与创新机理

PartDiffuser 的核心创新在于**将网格生成解耦为部件间自回归与部件内并行离散扩散**，从而化解长序列生成中全局拓扑一致性与高频局部细节之间的根本冲突。这一设计通过三个紧密耦合的 changed slots 实现：生成范式、几何条件注入与注意力机制。

### 1. 部件级半自回归生成范式

现有方法（如 MeshAnythingV2、BPT、TreeMeshGPT）采用令牌级自回归生成，将整个网格序列化为单一长序列逐令牌预测。这类方法面临两个固有问题：**误差累积**——早期令牌的预测偏差沿序列传播放大；**全局-局部冲突**——长距离依赖难以建模，导致拓扑一致性差或局部细节模糊。

PartDiffuser 将网格生成重新表述为**部件级半自回归过程**：首先对输入点云和网格进行语义分割，将网格序列化为多个部件令牌块；然后在部件间采用自回归顺序保证全局拓扑依赖，而在每个部件内部采用并行离散扩散精细重建高频几何特征。这一范式转换的形式化表达为：

$$p_{\theta}(X|C_{\mathrm{pc}}) = \prod_{i=1}^{N} p_{\theta}(X_i | X_{<i}, C_{\mathrm{pc}})$$

其中 $X_i$ 为第 $i$ 个部件的令牌块，$X_{<i}$ 为已生成的部件上下文。训练目标为每个部件的掩码扩散损失：

$$\mathcal{L}_i = \mathbb{E}_{t, X_i^t \sim q(\cdot|X_i^0)} [ w(t)(-\log p_{\theta}(X_i^0|X_i^t, X_{<i}, C_{\mathrm{dyn},i})) ]$$

### 2. 层次化几何条件注入

基线方法通常仅使用全局点云特征作为条件，缺乏对局部几何结构的精细引导。PartDiffuser 引入**层次化几何条件**：利用预训练编码器 Michelangelo 从输入点云中提取一个全局形状特征 $C_{\mathrm{global}}$ 和 $N$ 个部件级局部特征 $\{C_{\mathrm{part}_i}\}$。在生成第 $i$ 个部件时，动态拼接为 $[C_{\mathrm{global}}, C_{\mathrm{part}_i}]$，通过交叉注意力注入每个去噪块：

$$\hat Z = \mathrm{CrossAttn}(Q=\mathrm{LN}(Z'), K=C_{\mathrm{dyn}}, V=C_{\mathrm{dyn}}) + Z'$$

消融实验（Table 2）提供了决定性证据：完整模型（Full）CD 为 17.813；仅用全局特征（w/ Global only）CD 升至 29.125；仅用局部特征（w/ Parts only）CD 飙升至 54.728。这表明**全局特征提供拓扑骨架，局部特征注入精细几何，二者缺一不可**。

### 3. 复合材料注意力掩码

为支持部件间自回归、部件内双向扩散的混合注意力模式，PartDiffuser 设计了**复合材料注意力掩码**（Figure 7）。该掩码同时包含：
- **块扩散掩码**：允许部件内令牌双向交互，支持并行去噪；
- **块感知填充掩码**：约束部件间为自回归因果注意力，确保生成顺序依赖。

这一设计使模型在并行训练阶段即可同时学习部件内几何重建与部件间拓扑依赖，避免了标准因果掩码对并行扩散的限制。训练采用两阶段课程策略：先使用裁剪噪声调度训练扩散能力，再切换至全线性调度优化生成质量。

### 创新之间的因果耦合

上述三个 changed slots 形成**因果闭环**：语义分割（PartField）使部件级自回归成为可能；层次条件为每个部件提供差异化的几何引导；复合材料掩码则使混合注意力模式在训练和推理中保持一致。三者共同支撑了“部件间自回归保拓扑、部件内扩散保细节”的核心机制，最终在 Objaverse 数据集上实现 Chamfer Distance 17.813，相比 MeshAnythingV2 改进约 27%。

PartDiffuser 提出了一种**半自回归离散扩散框架**，将点云到网格的生成任务解耦为两个层次：部件间的自回归建模负责全局拓扑一致性，部件内的并行离散扩散负责局部几何细节的精细重建。整个 pipeline 由五个核心模块串联构成，形成从点云输入到结构化网格输出的端到端流程。

### Pipeline 总览

如 Figure 2 所示，框架的输入为原始点云，输出为具有语义部件结构的多边形网格。整体流程可概括为以下阶段：

![[assets/figures/papers/paper_list_l2562_https_arxiv_org_abs_2511_18801/figures/002_Figure_2.jpg]]
*Figure 2: An overview of our PartDiffuser framework. The process begins with semantic segmentation of the input point-cloud using PartField [23]. A pre-trained point cloud encoder, Michelangelo [46], extracts hierarchical geometric conditions. These conditions are dynamically injected via cross-attention into the Part-aware Diffusion Blocks, which guides the semi-autoregressive ”Part-wise Sampling” process of our Discrete Diffusion Model. to generate the final mesh*

1. **语义分割**：PartField 对点云进行语义分割，将全局形状分解为若干有意义的部件区域。
2. **网格标记化**：BPT（Block-wise Parallel Tokenizer）将每个分割后的部件序列化为定长离散令牌块。
3. **层次几何条件编码**：预训练的 Michelangelo 编码器从点云中提取全局形状特征和部件级局部特征向量，形成层次化条件表示。
4. **部件感知扩散块**：基于 DiT 架构的离散扩散模型，通过自注意力与动态交叉注意力融合层次条件，实现部件级令牌的并行去噪生成。
5. **半自回归采样器**：逐个部件执行完整去噪调度，部件间遵循 BFS 顺序的自回归依赖，部件内令牌并行生成。

### 模块关系与数据流

各模块之间的数据依赖关系决定了框架的半自回归特性。语义分割模块（PartField）产生部件划分后，每个部件独立经过 BPT 标记化，得到 $N$ 个令牌块 $\{X_1, X_2, \dots, X_N\}$。同时，Michelangelo 编码器从点云中提取条件表示 $C_{\mathrm{pc}} = \{C_{\mathrm{global}}, C_{\mathrm{part}_1}, \dots, C_{\mathrm{part}_N}\}$，其中 $C_{\mathrm{global}}$ 为全局形状特征，$C_{\mathrm{part}_i}$ 为第 $i$ 个部件的局部几何特征。

在生成阶段，部件感知扩散块以半自回归方式运作：当生成第 $i$ 个部件时，模型将已生成的干净部件块 $X_{<i}$ 作为上下文条件，同时对当前部件的噪声令牌块 $X_i^t$ 执行去噪。交叉注意力模块动态注入层次条件 $[C_{\mathrm{global}}, C_{\mathrm{part}_i}]$，使模型既能感知全局结构约束，又能聚焦当前部件的局部细节。这一设计的关键在于**复合材料注意力掩码**：块内采用双向注意力以充分捕捉部件内部几何关系，块间采用自回归因果掩码以保证拓扑依赖的有序传递。

### 训练与推理的差异化设计

训练阶段采用**并行掩码离散扩散**策略，所有部件的令牌块同时参与前向扩散与反向去噪，通过两阶段课程学习（裁剪噪声调度与全线性调度）逐步提升生成质量。推理阶段则切换为**半自回归采样**：按照 BFS 确定的部件顺序，逐个部件执行完整的 $T$ 步去噪过程，当前部件完全生成后再进入下一个部件。这种训练-推理的范式切换，使得模型在训练时能够高效并行学习部件间的联合分布，在推理时又能保证拓扑结构的层次化一致性。

### 关键设计要点

- **层次条件注入**：全局特征 $C_{\mathrm{global}}$ 提供整体形状约束，部件特征 $C_{\mathrm{part}_i}$ 提供局部几何引导，二者通过交叉注意力动态融合，缺一不可。消融实验表明，仅用全局特征时 CD 升至 29.125，仅用局部特征时 CD 升至 54.728，远差于完整模型的 17.813（Table 2）。
- **复合材料掩码**：块扩散掩码（块内双向注意力）与块感知填充掩码（块间自回归注意力）的组合，使得模型能够在保持部件间因果依赖的同时，充分利用部件内的双向上下文信息（Figure 7）。
- **加速因子 $k$**：通过调整去噪步长实现质量-速度权衡。当 $k$ 从 1 增至 4 时，推理时间从 63.8s 降至 34.6s，但 CD 从 17.813 恶化至 44.720（Table 3），表明该框架为实际部署提供了灵活的配置空间。

PartDiffuser 的核心设计是将网格生成解耦为**部件间自回归**与**部件内并行离散扩散**两个层次，并通过层次化几何条件动态控制生成过程。以下按流水线顺序阐述关键模块与核心公式。

### 语义分割与网格标记化

生成流水线始于对输入点云和网格的语义分割。模型采用 **PartField** 对网格进行部件级分割，将网格分解为 $N$ 个有语义意义的部件。分割的聚类数由网格面数 $F$ 动态决定：

$$K_{min} = \min\left(\left\lfloor \frac{F \times 0.5}{500} \right\rfloor, 4\right), \quad K_{max} = \min\left(\left\lfloor \frac{F \times 2.0}{500} \right\rfloor, 4\right)$$

分割完成后，每个部件通过 **BPT**（Block-wise Polygon Tokenization）序列化为定长离散令牌块 $X_i$，作为后续扩散模型的输入单元。

### 层次几何条件编码器

模型采用预训练点云编码器 **Michelangelo** 从输入点云 $C_{\mathrm{pc}}$ 中提取层次化条件表示。该编码器输出两类几何特征：

- **全局形状特征** $C_{\mathrm{global}}$：捕捉物体的整体拓扑与结构信息；
- **部件级局部特征** $\{C_{\mathrm{part}_i}\}_{i=1}^N$：对应每个语义部件的局部几何细节。

在推理阶段，交叉注意力的条件向量被动态设置为全局特征与当前生成部件的局部特征的拼接：

$$[C_{\mathrm{global}}, C_{\mathrm{part}_i}]$$

这种层次化条件注入机制是 PartDiffuser 区别于仅使用全局特征或无条件生成方法的关键设计。

### 部件感知扩散块

部件感知扩散块（Part-Aware Diffusion Block）在标准 DiT 块的基础上插入交叉注意力模块，使层次几何条件能够动态融入令牌特征。其核心计算流程为：

**自注意力残差连接：**

$$Z' = \mathrm{SelfAttn}(\mathrm{LN}(Z)) + Z$$

**交叉注意力条件注入：**

$$\hat{Z} = \mathrm{CrossAttn}(Q=\mathrm{LN}(Z'), K=C_{\mathrm{dyn}}, V=C_{\mathrm{dyn}}) + Z'$$

其中 $Z$ 为当前令牌序列，$C_{\mathrm{dyn}}$ 为动态条件向量（推理时 $C_{\mathrm{dyn}} = [C_{\mathrm{global}}, C_{\mathrm{part}_i}]$）。交叉注意力以令牌特征为 Query，以层次几何条件为 Key 和 Value，实现条件信息的高效融合。

### 半自回归分解与训练目标

PartDiffuser 将网格的似然函数按部件顺序进行半自回归分解：

$$p_{\theta}(X|C_{\mathrm{pc}}) = \prod_{i=1}^{N} p_{\theta}(X_i \mid X_{<i}, C_{\mathrm{pc}})$$

其中 $X_i$ 为第 $i$ 个部件的令牌块，$X_{<i}$ 表示已生成的前 $i-1$ 个部件。这种分解使得部件间保持自回归依赖以保证全局拓扑一致性，而每个部件内部则通过并行离散扩散精细重建局部几何。

第 $i$ 个部件的掩码扩散训练损失为：

$$\mathcal{L}_i = \mathbb{E}_{t, X_i^t \sim q(\cdot|X_i^0)} \left[ w(t) \left(-\log p_{\theta}(X_i^0 \mid X_i^t, X_{<i}, C_{\mathrm{dyn},i})\right) \right]$$

其中 $X_i^0$ 为干净令牌，$X_i^t$ 为时间步 $t$ 的噪声令牌，$w(t)$ 为时间步权重，$C_{\mathrm{dyn},i}$ 为第 $i$ 个部件对应的动态条件。

### 复合材料注意力掩码

训练阶段采用**复合材料掩码**（Composite Mask）控制令牌间的注意力模式。该掩码由两部分组成：

- **块扩散掩码**：允许同一部件块内的令牌双向注意力，实现并行去噪；
- **块感知填充掩码**：在部件间施加自回归注意力约束，确保当前部件只能关注已完成的先前部件。

这种设计使得模型在并行训练中同时学习部件内的双向依赖和部件间的因果依赖，为推理时的半自回归采样奠定基础。训练采用两阶段课程策略：先使用裁剪噪声调度，再切换至全线性调度，以稳定收敛。

![[assets/figures/papers/paper_list_l2562_https_arxiv_org_abs_2511_18801/figures/013_Figure_7.jpg]]
*Figure 7: Visualization of the composite attention mask during the parallel training phase, using N = 3 parts as an example. This mask governs the attention mask used in Section*

## 实验与关键发现

### 主实验：点云到网格生成性能对比

PartDiffuser 在 Objaverse、HSSD 与 3DFront 三个基准上与当前最优方法进行了定量比较，核心指标包括 Chamfer Distance（CD×10³↓）、F1-Score（↑）、Hausdorff Distance（HD↓）与 Earth Mover's Distance（EMD↓）。结果汇总于 Table 1。

![[assets/figures/papers/paper_list_l2562_https_arxiv_org_abs_2511_18801/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison for point cloud to mesh generation against state-of-the-art baselines. Datasets include Objaverse[8], HSSD[17], and 3DFront[10]. The Chamfer Distance (CD) metric is scaled by 103. The best results are highlighted in bold, and the second-best results are underlined*

在 Objaverse 数据集上，PartDiffuser 的 CD 降至 **17.813**，相比第二名 **MeshAnythingV2** 的约 24.4 提升了约 27%；F1-Score 达到 **0.343**，比第二名高出近 20%。在 3DFront 数据集上，PartDiffuser 在所有四项指标（CD 6.461、HD 0.147、EMD 0.068）上均取得最优，验证了方法在不同场景下的泛化能力。

定性结果（Figure 3）进一步显示，PartDiffuser 生成的网格在保持全局拓扑一致性的同时，能够重建出更丰富的高频局部几何细节，而基线方法常出现局部模糊或拓扑断裂。

![[assets/figures/papers/paper_list_l2562_https_arxiv_org_abs_2511_18801/figures/003_Figure_3.jpg]]
*Figure 3: Visual comparison of PartDiffuser with Baselines*

### 消融实验：层次几何条件的关键作用

为验证层次几何条件设计的有效性，作者在 Objaverse 测试集上进行了组件消融（Table 2）：

![[assets/figures/papers/paper_list_l2562_https_arxiv_org_abs_2511_18801/figures/004_Table_2.jpg]]
*Table 2: Ablation study on the components of our hierarchical geometric conditioning mechanism. All models are evaluated on the test set from Objaverse[8]*

- **Full model（全局 + 部件特征）**：CD 17.813，性能最优。
- **仅用全局特征（w/ Global only）**：移除部件级局部特征后，CD 急剧升至 **29.125**，表明缺乏局部条件会导致几何细节严重退化。
- **仅用部件特征（w/ Parts only）**：移除全局形状特征后，CD 进一步恶化至 **54.728**，说明全局拓扑约束对保持整体结构一致性不可或缺。

Figure 4 的可视化消融实例直观展示了上述退化：仅用部件特征时各部件间出现明显错位，仅用全局特征时则丢失了局部精细结构。这一组实验强有力地证明，**全局形状特征与部件级局部特征的层次化组合是 PartDiffuser 性能的关键因果机制**。

![[assets/figures/papers/paper_list_l2562_https_arxiv_org_abs_2511_18801/figures/006_Figure_4.jpg]]
*Figure 4: An example of the ablation study*

### 推理加速与质量权衡

PartDiffuser 默认推理步数 T=1024，单网格平均推理时间约 63.8 秒。通过引入加速因子 k（每 k 步执行一次去噪更新），可在推理速度与生成质量之间进行权衡（Table 3）：

| 加速因子 k | 采样步数 T | 推理时间（秒） | CD×10³↓ |
|:---:|:---:|:---:|:---:|
| 1 | 1024 | 63.8 | 17.813 |
| 2 | 512 | 46.0 | 22.697 |
| 4 | 256 | 34.6 | 44.720 |

当 k 从 1 增至 4 时，推理时间减少约 46%，但 CD 从 17.813 恶化至 44.720，几何精度显著下降。Figure 5 的可视化对比显示，高加速因子下网格表面出现明显噪声和细节丢失。这表明当前离散扩散采样步骤对高频几何重建至关重要，激进的跳跃采样会破坏去噪过程的渐进精化能力。

### 分割策略鲁棒性

PartDiffuser 对语义分割策略具有一定鲁棒性。在 PartField（默认）与 SAMPart3D 两种分割方案下，CD 分别为 17.81 与 19.11，差异不大（Figure 8）。这说明框架的性能增益主要来自层次条件与半自回归扩散范式，而非特定分割算法的选择。

### 局限性与失败模式

实验与论文分析揭示了以下局限性：

1. **序列长度瓶颈**：单个部件令牌块长度限制为 1024，模型最高序列长度为 4096。对于部件数量多或几何极度复杂的网格，这可能截断有效信息，导致生成质量下降。
2. **推理延迟**：默认 63.8 秒的推理时间不适合实时应用，且加速采样会显著牺牲几何精度。
3. **部件遍历顺序**：当前采用 BFS 确定部件生成顺序，未优化全局组装策略，可能在某些拓扑结构下产生次优的上下文利用。

这些失败模式提示，在极端复杂网格或对实时性要求高的场景中，PartDiffuser 的适用性需要进一步验证。

## 定位与知识库关联

### 1. 与现有工作的关系

PartDiffuser 的核心突破在于将**部件级半自回归离散扩散**范式引入点云到网格的生成任务，从而系统性地化解了现有令牌级自回归方法中全局拓扑一致性与高频局部细节之间的根本冲突。

**与令牌级自回归方法的对比。** 以 **MeshAnythingV2**、**BPT** 和 **TreeMeshGPT** 为代表的现有方法均采用令牌级自回归生成范式。这些方法将网格序列化为长令牌序列，通过标准因果掩码逐令牌预测。其瓶颈在于：长序列生成中的误差累积会破坏全局拓扑结构，而逐令牌的局部注意力窗口又难以捕获重建精细几何所需的高频信息。PartDiffuser 将生成解耦为两个层次——部件间自回归（保证全局拓扑）与部件内并行扩散（保留局部细节），从而在 Objaverse 数据集上将 Chamfer 距离（CD×10³）从 MeshAnythingV2 的约 24.4 降至 17.813（改进约 27%），F1-Score 从次优结果提升至 0.343（提升约 20%）。这一性能跃迁直接验证了“部件级解耦”对令牌级范式的结构性优势。

**与扩散模型的对比。** 标准离散扩散模型通常在整个序列上并行去噪，缺乏对结构化先验（如语义部件边界）的显式建模。PartDiffuser 通过引入**复合材料掩码**（块扩散掩码 + 块感知填充掩码），在训练阶段实现了块内双向注意力与块间自回归注意力的统一，使得模型能够同时学习部件内部的几何分布和部件间的拓扑依赖。这一设计使扩散模型首次具备了半自回归的结构化生成能力。

**与点云编码方法的对比。** 现有方法通常仅使用全局点云特征作为条件，缺乏对局部几何的精细引导。PartDiffuser 采用预训练的 **Michelangelo** 编码器提取层次化几何条件（全局形状特征 + 部件级局部特征），并通过交叉注意力动态注入每个去噪块。消融实验（Table 2）表明：仅用全局特征时 CD 升至 29.125，仅用局部特征时 CD 升至 54.728，而完整模型为 17.813，证明层次条件缺一不可。

### 2. 适用边界与局限

尽管 PartDiffuser 在多个基准上取得显著提升，其设计仍存在明确的适用边界：

- **序列长度限制。** 单个部件令牌块长度限制为 1024，模型最高序列长度为 4096。对于部件数量过多或单个部件面数极高的非结构化网格，该限制可能导致截断或信息丢失。Figure 6 展示了数据集中不同面数的网格分布，暗示模型在极端复杂形状上可能面临容量瓶颈。

- **推理效率。** 默认推理设置（k=1, T=1024）下，每网格平均推理时间约为 63.8 秒，不适合实时或交互式应用。虽然增加加速因子 k 可将时间压缩至 34.6 秒（k=4），但 CD 从 17.813 恶化至 44.720（Table 3），呈现明显的质量-速度权衡。

- **部件遍历策略。** 部件生成顺序由 BFS（广度优先搜索）决定，未针对全局组装策略进行优化。这意味着模型可能无法充分利用上下文信息来指导后续部件的生成，在部件间依赖关系复杂时可能产生次优结果。

- **分割策略依赖性。** 模型依赖外部语义分割模块（PartField）。虽然实验表明对不同分割策略具有一定鲁棒性（PartField vs SAMPart3D 的 CD 分别为 17.81 和 19.11，见 Figure 8），但分割质量仍可能成为整体性能的上限。

### 3. 开放问题与未来方向

论文明确指出了若干值得探索的方向：

- **模型规模扩展与长上下文。** 扩大模型规模并研究长上下文窗口策略，以突破当前 4096 的序列长度限制，从而支持更复杂、部件更多样的网格生成。

- **更并行的采样策略。** 当前半自回归采样在部件间仍为串行。探索更并行的采样策略，并量化采样步数与生成网格质量之间的精确关系，有望在保持质量的同时大幅提升推理速度。

- **端到端联合训练与多模态扩展。** 当前框架中分割、编码、扩散为独立模块。探索端到端联合训练可能进一步提升整体性能。此外，将 PartDiffuser 扩展至接受多模态输入（如图像、文本），可使其具备从更丰富的用户意图出发生成三维网格的能力。

- **部件遍历顺序优化。** 研究更优的部件生成顺序策略（如基于依赖图或注意力机制的自适应排序），可能进一步提升全局拓扑一致性和上下文利用效率。

## 原文 PDF

![[paperPDFs/CVPR_2026/PartDiffuser_Part_wise_3D_Mesh_Generation_via_Discrete_Diffusion.pdf]]
