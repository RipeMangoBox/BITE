---
title: "Cosmos-Transfer1: Conditional World Generation with Adaptive Multimodal Control"
type: paper
paper_level: A
venue: Whitepaper
year: 2025
pdf_ref: paperPDFs/WHITEPAPER_2025/Cosmos_Transfer1_Conditional_World_Generation_with_Adaptive_Multimodal_Control.pdf
code_link: https://github.com/nvidia-cosmos/cosmos-transfer1
project_link: https://research.nvidia.com/labs/dir/cosmos-transfer1/
aliases:
- CT
- Cosmos-Transfer1
tags:
- WHITEPAPER_2025
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning
core_operator: "引入的时空控制图 (spatiotemporal control map) 允许对不同空间位置和时间分配不同模态的控制权重，从而精确调节每个区域的生成自由度。"
primary_logic: "通过为不同模态构建独立且可零初始化的ControlNet分支，在推理时融合并通过可调的空间控制图加权，模型能够灵活整合多种互补的模态信息，在保持整体生成质量的同时实现区域级可控性。"
claims:
- "多模态均匀权重模型 (Cosmos-Transfer1-7B Uniform Weights) 在TransferBench上取得了最高的整体质量评分 (Quality Score 8.54)，优于所有单模态控制模型（最高6.51）。"
- "通过调整前景Vis权重，前景模糊结构相似度 (Blur SSIM) 从0.43提升至0.81，皮尔逊相关系数为0.93，表明时空控制图能精确调节对应区域的对齐度。"
- "在排除Blur visual或Edge控制的情况下，模型多样性 (Diversity-LPIPS) 显著提高（0.37和0.31），而排除Depth或Segmentation时多样性降低（0.25和0.23），验证了密集结构信息限制多样性、稀疏信息提升多样性的假设。"
- "TransferBench 上 Quality Score (DOVER-technical, 越高越好) = 8.54 (Cosmos-Transfer1-7B Uniform Weights)"
---

# Cosmos-Transfer1: Conditional World Generation with Adaptive Multimodal Control

> [!tip] 核心洞察
> 通过为不同模态构建独立且可零初始化的ControlNet分支，在推理时融合并通过可调的空间控制图加权，模型能够灵活整合多种互补的模态信息，在保持整体生成质量的同时实现区域级可控性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Cosmos-Transfer1: 基于自适应多模态控制的条件世界生成 |
| 英文题名 | Cosmos-Transfer1: Conditional World Generation with Adaptive Multimodal Control |
| 会议/期刊 | Whitepaper 2025 |
| Links | [paper](https://arxiv.org/abs/2503.14492) · [GitHub](https://github.com/nvidia-cosmos/cosmos-transfer1) · [Project](https://research.nvidia.com/labs/dir/cosmos-transfer1/) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning |
| Method | Cosmos-Transfer1 |
| Dataset | TransferBench, 自建机器人Sim2Real数据 |

> [!tip] 效果简介
> - TransferBench 上，Quality Score (DOVER-technical, 越高越好) 为 8.54 (Cosmos-Transfer1-7B Uniform Weights)，对比 6.51 (Cosmos-Transfer1-7B [Depth]), 5.94 (Cosmos-Transfer1-7B [Vis])，变化 +2.03 / +2.60。
> - TransferBench 上，Depth Alignment (si-RMSE, 越低越好) 为 0.47 (Uniform Weights)，对比 0.49 (Cosmos-Transfer1-7B [Depth])，变化 -0.02。
> - 自建机器人Sim2Real数据 上，Quality Score 为 模型with spatiotemporal control map 取得前三名，对比 单模态分割控制模型，变化 未给出具体数值。

## 概要

可控世界生成旨在根据给定的控制信号（如深度图、分割掩码、边缘图等）合成视觉逼真的视频，在自动驾驶仿真、机器人数据增强等领域具有关键应用价值。然而，现有方法面临一个核心瓶颈：**单一模态控制难以同时满足场景中不同区域对生成保真度与多样性的矛盾需求**。例如，前景物体需要高保真结构约束以保留可辨识的几何与纹理细节，而背景区域则期望更高的多样性以产生合理的场景变化。传统方案通常对整帧施加全局统一的控制信号，无法在空间维度上灵活调节不同模态的控制强度，导致生成结果要么整体过于僵硬（多样性不足），要么关键结构丢失（保真度不足）。

针对上述问题，本文提出 **Cosmos-Transfer1**，一个基于扩散模型的自适应多模态条件世界生成框架。其核心创新在于引入**时空控制图（spatiotemporal control map）** 机制：通过为视觉模糊、Canny边缘、深度、语义分割等多种模态分别构建独立的 ControlNet 分支，并在推理时使用可调的空间-时间权重图对各分支输出进行逐元素加权融合，模型能够在不同空间位置和时间步长上自主选择最相关的控制模态，从而精确调节每个区域的生成自由度。这一设计使得模型可以灵活整合互补的模态信息——密集模态（如视觉模糊、边缘）提供强结构约束，稀疏模态（如深度、分割）提供高层语义引导——在保持整体生成质量的同时实现区域级可控性。

实验结果表明，Cosmos-Transfer1 在多项任务上显著优于单模态控制基线。在 TransferBench 基准上，多模态均匀权重模型取得了 **8.54 的整体质量评分**，较最优单模态模型（Depth，6.51）提升逾 2 分（Table 1）。消融实验进一步揭示了模态特性与生成行为之间的因果关联：**排除密集视觉/边缘控制后，生成多样性（Diversity-LPIPS）显著提高**（0.37 和 0.31），而排除深度或分割控制则多样性降低（0.25 和 0.23），验证了“密集结构信息限制多样性、稀疏语义信息提升多样性”的假设。更关键的是，通过调节前景区域的视觉权重，前景模糊结构相似度（Blur SSIM）可从 0.43 线性提升至 0.81（皮尔逊相关系数 r=0.93），证实了时空控制图对区域对齐度的精确调控能力（Figure 7）。在自动驾驶视频生成任务中，融合 HDMap 与 LiDAR 的多模态控制相比单一 LiDAR 控制，在保持动态物体检测精度（3D-Bbox mAP 44.66）的同时，将车道线分割 IoU 从 46.41 提升至 51.55（Table 4），展示了多模态互补的实际收益。

从方法谱系来看，Cosmos-Transfer1 属于**基于 ControlNet 的多模态条件扩散模型**，其关键设计决策包括：（1）各控制分支**独立训练、推理时融合**，避免了联合训练的组合爆炸与模态冲突；（2）引入**零初始化线性层**将控制特征注入主分支，确保训练初期不干扰预训练权重；（3）通过**时空控制图**实现推理阶段的动态加权，无需重新训练即可适应不同下游任务的控制需求。与现有可控生成方法相比，该工作首次系统性地解决了多模态控制在空间维度上的自适应分配问题，为条件世界生成提供了更灵活、更高效的范式。



### 条件世界生成与可控视频合成

世界模型旨在根据给定的输入条件生成逼真、多样且物理一致的视觉场景，是通向物理人工智能的关键技术。当前，基于扩散模型的条件世界生成已取得显著进展，能够根据文本、图像、深度图、语义分割等多种模态的控制信号生成高质量视频。这类模型通常采用 ControlNet 架构，在主去噪分支之外增加控制分支，将条件信息注入生成过程。

### 现有方法的模态单一瓶颈

现有可控世界生成方法普遍面临一个核心瓶颈：**它们通常仅支持单一模态的控制信号**。例如，一个基于模糊视觉特征（blur visual）的模型只能保持颜色和整体构图，而基于深度图的模型只能保持场景几何。然而，真实世界的应用场景往往需要同时满足多种、甚至相互冲突的约束——例如，在机器人数据增强中，前景机器人需要高保真度以保持精确的视觉外观，而背景环境则需要高多样性以覆盖更多域迁移场景。

单一模态控制无法同时满足这些差异化需求：密集模态（如模糊视觉、边缘）虽然能提供强结构约束以保证保真度，但会严重限制生成多样性；稀疏模态（如深度、分割）能保留更多生成自由度以提升多样性，但结构对齐度显著下降。这种**保真度与多样性之间的根本矛盾**，在单一模态控制下无法得到灵活调节。

### 多模态融合的缺失与空间自适应需求

尽管多模态信息在理论上可以互补——密集模态提供结构保真，稀疏模态释放生成自由度——但如何将多种模态有效融合并实现区域级可控，仍是一个开放问题。简单的全局均匀融合策略无法区分不同空间区域的需求：前景物体需要强结构约束，而背景区域则希望保留更多变化空间。这要求控制机制不仅支持多模态输入，还必须具备**空间自适应的权重分配能力**，使得模型能够在不同区域灵活选择最相关的模态信息。

### 本文动机与核心思路

针对上述缺口，Cosmos-Transfer1 提出了一种**自适应多模态控制的条件世界生成框架**。其核心思路是：

1. **多控制分支独立训练**：为每种模态（模糊视觉、边缘、深度、分割等）构建独立的 ControlNet 分支，分别训练后于推理时融合，避免联合训练的高昂成本和模态冲突。
2. **时空控制图**：引入一个可调的空间-时间权重图，允许用户或算法为不同空间位置和时间分配不同模态的控制权重，从而精确调节每个区域的生成自由度。
3. **区域级保真度-多样性权衡**：通过在前景区域施加密集模态（视觉、边缘）的高权重以保证结构保真，在背景区域施加稀疏模态（深度、分割）的高权重以释放多样性，实现灵活的区域级控制。

这种方法首次将多模态条件生成的“融合”问题提升为“空间自适应的选择性融合”问题，为可控世界生成提供了更精细的调控维度。



## 核心方法与创新机理

Cosmos-Transfer1 的核心创新在于引入了一套**自适应多模态控制框架**，使条件世界生成模型首次能够在统一的架构下，对不同空间区域和时间步灵活组合多种控制模态，从而精确调节各区域的生成自由度。这一设计直接回应了现有方法的瓶颈：单一模态控制无法同时满足不同区域对保真度与多样性的差异化需求。

### 关键创新点分解

**1. 多模态独立控制分支与零初始化融合**

与以往仅支持单一模态或需联合训练所有模态的方法不同，Cosmos-Transfer1 为每种控制模态（视觉模糊、Canny边缘、深度、分割等）构建**独立的 ControlNet 分支**，各分支分别训练，仅在推理时融合。每个控制分支的输出通过零初始化线性层注入主去噪分支（Figure 1），确保训练初期不干扰预训练权重。这种设计使得模型可以灵活地开关任意模态组合，而不需要针对每种组合重新训练。

**2. 时空控制图实现区域级自由度调节**

这是方法最具区分度的创新。Cosmos-Transfer1 引入**时空控制图** $\mathbf{w} \in \mathbb{R}^{N \times X \times Y \times T}$，对每个控制分支的输出进行逐元素加权后再注入主分支：

$$\mathbf{w}_i \cdot \mathbf{h}_i^j$$

其中 $\mathbf{h}_i^j$ 为第 $j$ 个控制分支第 $i$ 个块的输出，$\mathbf{w}_i$ 为对应的时空权重。通过在不同空间位置分配不同的模态权重，模型可以在前景区域施加密集约束（如视觉模糊+边缘）以保证结构保真度，同时在背景区域施加稀疏约束（如深度+分割）以释放生成多样性。

**3. 推理时动态权重调节**

时空控制图支持在推理阶段动态调整，无需重新训练。论文通过 SalientObject 算法（利用 VLM 进行前后景分类）自动生成权重掩码，也支持手动设计。实验表明，当前景 Vis 权重增加时，前景 Blur SSIM 从 0.43 线性提升至 0.81（Pearson $r=0.93$）；当背景 Depth 权重增加时，背景 Depth si-RMSE 线性下降（Pearson $r=-0.92$）（Figure 7）。这验证了控制图对区域生成行为的精确调节能力。

### 与基线方法的差异对照

| 维度 | 基线方法 | Cosmos-Transfer1 |
|------|---------|-----------------|
| 控制模态数量 | 单一模态（如仅 Vis 或仅 Depth） | 多模态（Vis、Edge、Depth、Seg 等），可独立开关 |
| 控制权重分布 | 全局统一或无权重 | 时空控制图，支持区域定制加权 |
| 控制分支训练 | 联合训练所有模态 | 各模态独立训练，推理时融合 |
| 推理灵活性 | 固定模态组合 | 推理时动态调整权重，无需重训练 |

### 创新背后的核心洞察

论文通过系统的消融实验揭示了一个关键规律：**密集结构信息（如视觉模糊、边缘）限制多样性但提升保真度，稀疏语义信息（如深度、分割）释放多样性但降低结构对齐**。在 TransferBench 上，排除 Vis 或 Edge 控制时多样性 LPIPS 显著提高（0.37 和 0.31），而排除 Depth 或 Segmentation 时多样性降低（0.25 和 0.23）（Table 1）。这一发现为时空控制图的设计提供了理论依据——通过在不同区域分配不同密集度的控制信号，可以在保真度与多样性之间取得区域级的最优权衡。

多模态均匀权重模型（Cosmos-Transfer1-7B Uniform Weights）在 TransferBench 上取得了最高的整体质量评分（Quality Score 8.54），优于所有单模态控制模型的最高分（6.51），证明了多模态信息互补的有效性。然而，均匀权重在单项对齐指标上（如 Blur SSIM 0.87 vs. 单模态最优 0.96）并非最优，这恰恰凸显了时空控制图的必要性——全局统一权重无法满足区域级差异化需求。



Cosmos-Transfer1 是一个基于扩散模型的条件世界生成器，其核心架构可解构为三条并行的功能流：**条件提取流**、**主生成流**与**多模态融合流**。系统接受多模态控制信号与文本提示，输出可控的长视频。

**主生成流**建立在 Cosmos-Predict1-7B-Video2World 的预训练 DiT 基础之上。该主干由一系列 Transformer 块堆叠而成，接受含噪视频令牌 $\mathbf{x}_{\sigma}$ 与噪声级别 $\sigma$，预测添加的噪声 $\mathbf{n} = D(\mathbf{x}_{\sigma}, \sigma)$。基础模型权重在后续所有控制分支训练中保持冻结（Figure 1a）。

**条件提取流**由多个独立的 ControlNet 分支构成，每个分支对应一种控制模态——视觉模糊 (Blur Visual)、Canny 边缘 (Edge)、深度 (Depth)、分割 (Segmentation)、HDMap 或 LiDAR。每个控制分支包含若干 Transformer 块，从对应模态的条件令牌 $\mathbf{c}$ 中提取层次化特征。分支的输出通过零初始化线性层注入主分支，确保训练初期不干扰预训练权重（Figure 1b）。

**多模态融合流**是 Cosmos-Transfer1 区别于单模态 ControlNet 的关键创新。设第 $j$ 个控制分支在第 $i$ 个 Transformer 块的输出为 $\mathbf{h}_i^j$，时空控制图 $\mathbf{w} = \{\mathbf{w}_1, \mathbf{w}_2, \dots, \mathbf{w}_N\}$ 为每个时空位置 $(x, y, t)$ 分配各模态的权重。最终注入主分支的激活为逐元素乘积 $\mathbf{w}_i \cdot \mathbf{h}_i^j$（Figure 2）。当某位置各模态权重之和超过 1 时，系统执行和为一归一化：$w_k^{xyt} \leftarrow w_k^{xyt} / \sum_{k'} w_{k'}^{xyt}$。

**输入输出流与辅助模块**。文本提示首先经过基于 Pixtral-12B 微调的提示上采样器，将简短用户描述扩展为符合训练分布的长提示。多模态控制信号（如深度图、分割掩码、边缘图）经各自分支编码后，与文本条件一同注入主生成流。模型输出为 5 秒 1280×704p 24fps 视频（约 56K 令牌）。对于 4K 分辨率需求，系统后接一个专用升频 ControlNet：该模块接受经 Real-ESRGAN 退化技术处理的低质视频块作为输入，通过 3×3 重叠网格的逐块生成与重叠区域平均，将 720p 视频提升至 4K，同时添加真实反射与纹理细节（Figure 5）。

**训练策略**。各模态控制分支**分别独立训练**，推理时融合。每个分支使用 1024 块 NVIDIA H100 GPU 训练 2 至 4 周。这种分离训练策略使得新增模态无需重训已有分支，实现了模态层面的即插即用。



Cosmos-Transfer1 的核心架构围绕三个关键设计展开：**独立可零初始化的多模态控制分支**、**时空控制图加权融合机制**，以及**基础扩散去噪主分支**。以下按模块拆解其公式与变量含义。

### 基础扩散去噪器

模型主干基于 DiT（Diffusion Transformer）架构，其基础去噪函数接受含噪令牌 $\mathbf{x}_{\sigma}$ 和噪声级别 $\sigma$，预测添加的噪声 $\mathbf{n}$：

$$\mathbf{n} = D(\mathbf{x}_{\sigma}, \sigma)$$

其中 $\mathbf{x}_{\sigma}$ 为加噪后的视频令牌序列，$\sigma$ 控制噪声强度。此模块在 ControlNet 训练阶段**权重完全冻结**，仅作为主生成分支提供预训练先验（Figure 1(a)）。

### 条件去噪器（ControlNet 扩展）

为引入外部控制信号，基础去噪器被扩展为条件形式：

$$\mathbf{n} = D(\mathbf{x}_{\sigma}, \sigma, \mathbf{c})$$

其中 $\mathbf{c}$ 为条件令牌，由控制分支从各类模态输入（如视觉模糊、边缘、深度、分割）中提取。该公式定义了单模态 ControlNet 的基本范式（Eq. 2），也是 Cosmos-Transfer1 多模态融合的原子单元。

### 控制分支与零初始化注入

每个控制分支 $j$ 包含若干 Transformer 块，其第 $i$ 个块的输出 $\mathbf{h}_i^j$ 通过**零初始化线性层**后注入主分支对应块。零初始化确保训练初期控制分支不干扰预训练权重，使模型从无条件生成平滑过渡到条件生成（Figure 1(b)）。

### 时空控制图加权融合

这是 Cosmos-Transfer1 区别于标准 ControlNet 的核心机制。对于 $N$ 个控制分支，定义时空控制图 $\mathbf{w} = \{\mathbf{w}_1, \mathbf{w}_2, ..., \mathbf{w}_N\}$，其中 $\mathbf{w}_j \in \mathbb{R}^{X \times Y \times T}$ 对第 $j$ 个模态在空间位置 $(x,y)$ 和时间 $t$ 上分配权重。第 $j$ 个控制分支第 $i$ 个块的最终激活注入主分支前，进行逐元素加权：

$$\mathbf{w}_i \cdot \mathbf{h}_i^j$$

其中 $\cdot$ 表示逐元素乘积。这意味着模型可以在**不同空间区域对不同模态赋予不同控制强度**——例如前景区域增大视觉模糊权重以提升结构保真度，背景区域增大深度权重以保持几何一致性（Sec. 3）。

### 权重归一化约束

为避免多模态权重叠加导致信号过强，在每个时空位置 $(x,y,t)$ 上施加和为一的归一化约束：若各模态权重之和超过 1，则进行缩放：

$$\text{if } \sum_k w_k^{xyt} > 1 \text{, then } w_k^{xyt} \leftarrow \frac{w_k^{xyt}}{\sum_{k'} w_{k'}^{xyt}}$$

此约束确保控制信号的注入强度在合理范围内，防止生成过程被过度约束（Sec. 3 末段）。

### 模块间因果链路

上述模块的协作逻辑可总结为：**独立训练的控制分支**各自从不同模态提取互补特征 → **零初始化线性层**保证训练稳定性 → **时空控制图**在推理时对不同区域选择性加权 → **归一化约束**防止信号过载 → 加权后的多模态特征注入**冻结的主分支**，最终引导扩散去噪过程生成符合区域约束的视频。这一设计使得模型无需联合训练所有模态组合，即可在推理时灵活融合任意模态子集，并实现区域级可控性。



## 实验与关键发现

### 核心定量结果：多模态控制统一优于单模态

在自建的**TransferBench**（600个视频）上，Cosmos-Transfer1-7B的多模态均匀权重变体（各控制模态权重均为0.25）取得了**最高的整体质量评分**（Quality Score 8.54），显著优于所有单模态控制模型。作为对比，最优的单模态模型Cosmos-Transfer1-7B [Depth]仅获得6.51，而[Vis]模型仅为5.94（Table 1）。这一结果直接验证了多模态信息融合对提升生成质量的关键作用——不同模态提供了互补的结构与语义线索，单一模态无法同时满足场景重建的多样需求。

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2503_14492/figures/006_Table_1.jpg]]
*Table 1: Quantitative evaluation on TransferBench for various Cosmos-Transfer1 configurations. We compare single control models (each conditioned on a single modality) with multimodal variants that use spatially uniform weights. For the multimodal cases, “Cosmos-Transfer1-7B, Uniform Weights” denotes the full model that integrates all four control modalities (each weighted at 0.25), while variants such as “Cosmos-Transfer1-7B, Uniform Weights, No Vis” exclude a specific modality (here, the blur visual control), with the remaining modalities retaining equal weights. Best results are in bold; second-best are underlined*

在具体对齐指标上，多模态均匀权重模型展现了均衡的性能：深度对齐（Depth si-RMSE）达到0.47，甚至略优于纯深度控制的0.49；分割对齐（Mask mIoU）为0.48，接近纯分割控制的0.62。然而，这种全局均匀加权策略也暴露了局限性——Blur SSIM（0.87）和Edge F1（0.20）分别低于单模态最优的0.96和0.28，说明**全局权衡无法在每项约束上达到极致**。

### 模态稀疏性与多样性的因果机制

Table 1的消融实验揭示了一个清晰的因果链条：**密集结构信息限制多样性，稀疏语义信息提升多样性**。当从多模态均匀权重模型中排除Blur visual或Edge控制时，多样性指标（Diversity-LPIPS）分别跃升至0.37和0.31；相反，排除Depth或Segmentation时，多样性降至0.25和0.23。这一发现支持了核心假设——深度图和分割图作为稀疏控制信号（如远处背景区域的同质化深度、SAM2分割的大面积色块），为模型保留了更大的生成自由度，从而产生更丰富的纹理和细节变化。

同时，密集控制信号对结构保真度至关重要：排除Vis控制导致Blur SSIM从0.87骤降至0.68，排除Edge控制使Edge F1从0.20降至0.11。这证实了**视觉模糊和边缘信息是维持空间结构对齐的瓶颈模态**，其缺失无法被其他模态补偿。

### 时空控制图的精确调节能力

为突破全局均匀加权的局限，Cosmos-Transfer1引入了**时空控制图**（spatiotemporal control map），允许在不同空间区域分配差异化的模态权重。基于VLM的**SalientObject算法**自动将场景划分为前景与背景：前景分配Vis和Edge权重（各0.5），以降低生成自由度、提升结构保真度；背景分配Depth和Seg权重（各0.5），以增加多样性。

Figure 7的消融分析定量验证了控制图的精确调节能力：
- **前景Vis权重与Blur SSIM呈强正相关**（Pearson r=0.93），权重从0增加至1时，Blur SSIM从0.43线性提升至0.81。
- **背景Depth权重与Depth si-RMSE呈强负相关**（Pearson r=-0.92），权重增加显著降低深度重建误差。

Table 2进一步展示了权重空间分配对区域级保真度与多样性的直接控制：将密集约束（Vis+Edge）从前景移至背景时，前景Blur SSIM从0.86降至0.44，同时前景多样性LPIPS从0.01跃升至0.12；背景则呈现相反趋势（Blur SSIM从0.56升至0.75，多样性LPIPS从0.03升至0.33）。这证明**时空控制图能够在同一场景的不同区域实现保真度与多样性的解耦控制**。

### 下游任务验证：机器人Sim2Real与自动驾驶

在**机器人Sim2Real数据生成**任务中，结合时空控制图（Seg+Edge+Vis）的模型在质量评分上取得前三名（Table 3），且前景机器人的结构保真度显著优于纯分割控制（Figure 8）。这表明多模态区域加权有效缓解了单模态控制下前景物体形变或纹理丢失的问题。

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2503_14492/figures/010_Table_3.jpg]]
*Table 3: Quantitative evaluation of Cosmos-Transfer1 on robotics Sim2Real data generation task, including single-control models and two multimodal control variants with different spatiotemporal control maps. Best results are in bold; second-best are underlined*

在**自动驾驶视频生成**任务中，单独使用LiDAR控制在3D边界框检测（mAP）和重投影误差上最优，但对车道线保持较差（Lane mIoU 46.41）；集成HDMap后，车道线IoU提升至51.55，同时保持了动态物体检测精度（3D-Bbox mAP 44.66）（Table 4）。这验证了**不同模态对场景元素的敏感性存在互补性**——LiDAR擅长保留动态物体的几何结构，HDMap则提供稳定的道路拓扑约束。

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2503_14492/figures/016_Table_4.jpg]]
*Table 4: Quantitative evaluation of Cosmos-Transfer1-7B-Sample-AV on the autonomous driving video generation task. We compare the results of both single-control models and multimodal control variant over various metrics. Best results are in bold*

### 失败模式与局限性

尽管Cosmos-Transfer1在多模态控制上取得了显著进展，仍存在以下关键失败模式：

1. **稀疏模态的结构保真度不足**：当仅使用深度或分割等稀疏控制信号时，生成视频的Blur SSIM和Edge F1显著低于密集模态，可能导致物体边界模糊或几何失真（Table 1）。

2. **全局均匀加权的次优性**：多模态均匀权重模型虽在整体质量上最优，但在单项对齐指标上均弱于对应的单模态最优模型，表明**全局统一权重是一种折中方案，无法在局部区域实现极致控制**。

3. **时空控制图的启发式局限**：当前控制图依赖VLM驱动的SalientObject算法进行前景-背景二分类，无法处理更细粒度的区域划分（如多物体交互场景）。此外，该算法需要额外的VLM推理开销，且未经过端到端优化。

4. **物理一致性未量化**：生成视频中对象间的物理交互（如机器人抓取时的接触动力学）未进行定量评估，这可能影响在物理AI应用中的可靠性。

5. **评估覆盖有限**：TransferBench仅含600个视频，未在完全真实的长尾场景（如极端天气、罕见驾驶行为）中充分验证模型的鲁棒性。

### 推理效率与可扩展性

Table 5展示了Cosmos-Transfer1-7B在不同GPU配置下的端到端推理延迟。生成5秒视频（1280×704p，24fps，约56K tokens）时，从1块到64块NVIDIA B200 GPU实现了近40倍的加速，最终延迟低于5秒，达到实时生成吞吐量。这表明独立控制分支的融合策略在推理时具有高度可并行性，为实际部署提供了可行性。

### 补充图表

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2503_14492/figures/008_Figure_7.jpg]]
*Figure 7: Correlations of modality weights on foreground (FG) region (for Vis and Edge) or background (BG) region (for Depth and Segmentation) with ground truth modality*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2503_14492/figures/015_Figure_12.jpg]]
*Figure 12: 1st row: LiDAR simulated by NVIDIA Omniverse as the control signal to Cosmos-Transfer1-7B. 2nd-5th rows: Videos generated by different text prompts listed as following: The video showcases an urban driving scene during the golden hour...; The video portrays a nighttime driving scene in an urban environment...; The video captures an urban driving scene under heavy rainfall...; The video depicts a thrilling driving scene in a jungle-style urban environment*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2503_14492/figures/014_Figure_11.jpg]]
*Figure 11: 1st row: Control signals (left: HDMap + 3DBbox, right: LiDAR) to Cosmos-Transfer1-7B-Sample-AV. 2nd-5th rows: Video generated by different text prompts listed as following: The scene unfolds on a foggy morning, with a thick layer of mist reducing visibility...; The scene is bathed in the warm, golden hues of the late afternoon sun, casting long shadows on the road...; The street is blanketed in heavy snowfall, with large snowflakes continuously falling, partially obscuring visibility...; The scene unfolds in a chaotic and intense environment as a fire engulfs the houses on either side of the street*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2503_14492/figures/009_Table_2.jpg]]
*Table 2: Quantitative evaluation on TransferBench for Cosmos-Transfer1-7B with spatiotemporal weights derived from our SalientObject algorithm. The leftmost eight columns specify the weight design for the four modalities respectively. For each metric, “FG” denotes the result in that metric computed in the foreground region, and “BG” stands for background*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2503_14492/figures/017_Table_5.jpg]]
*Table 5: Computation time for generating a 5-second video with Cosmos-Transfer1-7B under different parallelism settings. End-to-end runtime dips below 5 seconds when scaled up to 64 B200 GPUs and reach real-time generation throughput*



## 定位与知识库关联

### 与基线方法的关系

Cosmos-Transfer1 建立在两条成熟技术路线的交汇点上：**扩散 Transformer (DiT)** 视频生成主干和 **ControlNet** 条件控制范式。

**主干继承。** 模型的主生成分支直接复用 **Cosmos-Predict1-7B-Video2World**（NVIDIA, 2025）的预训练 DiT 去噪网络，该网络接受含噪令牌 $\mathbf{x}_{\sigma}$ 和噪声级别 $\sigma$ 预测噪声 $\mathbf{n} = D(\mathbf{x}_{\sigma}, \sigma)$。Cosmos-Transfer1 冻结该主分支的全部权重，仅通过外挂控制分支注入条件信息——这与 ControlNet（Zhang et al., 2023）的“冻结主模型、训练可插拔编码器”策略一脉相承，但将其从单模态图像域扩展到了**多模态视频域**。

**控制分支的独立训练策略。** 与多数多模态条件生成方法（如 UniControl、ControlNet++ 等联合训练所有模态分支的做法）不同，Cosmos-Transfer1 的关键设计选择是**各模态控制分支完全独立训练，仅在推理时融合**。每个分支使用 1024 块 NVIDIA H100 GPU 训练 2 到 4 周，且均从相同的预训练主分支出发，通过零初始化线性层注入控制特征——这一技巧直接继承自 ControlNet 原始设计，确保训练初期不干扰预训练权重。独立训练带来了显著的工程优势：新增模态无需重新训练已有分支，只需训练新分支并与已有分支在推理时组合。

**与单模态基线的性能对比。** 论文将四个单模态控制变体作为直接基线：**Cosmos-Transfer1-7B [Vis]**（模糊视觉控制）、**[Edge]**（Canny 边缘控制）、**[Depth]**（深度控制）和 **[Seg]**（分割控制）。在 TransferBench 上，单模态模型在各自对应的对齐指标上达到最优——例如 [Vis] 的 Blur SSIM 为 0.96，[Edge] 的 Edge F1 为 0.28——但整体质量评分（Quality Score）最高仅 6.51（[Depth]）。多模态均匀权重模型（每个模态权重 0.25）将 Quality Score 推至 8.54，提升幅度达 +2.03，但代价是部分对齐指标退化（Blur SSIM 降至 0.87，Edge F1 降至 0.20）。这揭示了多模态融合中固有的**全局权衡困境**：均匀融合无法在每个区域同时达到各模态的最优保真度。

### 适用边界

**优势场景。** 时空控制图机制在以下场景中展现出精确的区域级可控性：
- **前景高保真 + 背景高多样性**：通过 SalientObject 算法（基于 VLM 的前/背景分类）为前景分配密集约束模态（Vis + Edge 各 0.5 权重），背景分配稀疏约束模态（Depth + Seg 各 0.5 权重），前景 Blur SSIM 可达 0.81（Pearson r=0.93），同时背景多样性 LPIPS 可提升至 0.33。
- **自动驾驶多模态融合**：HDMap 保持车道布局（Lane mIoU 51.55），LiDAR 保持动态物体检测精度（3D-Bbox mAP 44.66），联合使用优于任一单模态。
- **机器人 Sim2Real 数据增强**：前景（机器人）使用 Seg+Edge+Vis 联合约束提升保真度，背景释放自由度以生成多样化环境。

**退化场景。** 以下情况中方法表现受限：
- **纯稀疏模态控制**：单独使用 Depth 或 Seg 时，结构保真度显著低于密集模态（Vis/Edge），因为深度图和分割掩码在远距离背景区域高度同质化，缺乏细粒度结构约束。
- **极端对齐需求**：当某一模态的对齐精度要求极高时（如 Blur SSIM > 0.95），多模态融合的全局权衡会稀释该模态的控制力，需通过大幅提高该模态的时空权重来补偿。
- **未见长尾场景**：TransferBench 仅含 600 个视频，模型在真实长尾分布中的泛化能力尚未充分验证。

### 局限与开放问题

**已明确的局限。**
1. **时空控制图的获取依赖启发式**：当前通过手工规则或 VLM 驱动的 SalientObject 算法生成权重图，远非最优。端到端学习时空控制图需要大量配对数据，目前尚不可行。
2. **训练开销巨大**：单模态分支需 1024 块 H100 GPU 训练 2–4 周；虽独立训练避免组合爆炸，但模态数量增长仍线性增加总资源消耗。
3. **物理一致性未量化**：生成视频中对象间的物理交互（如机器人抓取的接触动力学）未进行定量评估，这对物理 AI 应用的可靠性构成潜在风险。
4. **公平性与偏见未讨论**：论文未评估生成内容在人口统计学、地理、天气、驾驶习惯等维度上的潜在偏见，也未对训练数据的场景均衡性进行分析。

**开放问题。**
- 能否设计端到端学习框架自动预测最优时空控制图，替代当前的 VLM 启发式或手工设计？
- 当可用模态数量进一步增加（如法线、热成像、事件相机等）时，独立控制分支的训练与融合策略是否依然高效且可扩展？
- 如何量化生成视频中对象间物理交互的准确性？时空控制图是否有利于改善这些物理一致性？
- 生成的视觉内容是否存在与训练数据相关的系统性偏见？如何评测与缓解？
- 实时推理所采用的并行策略（64 块 B200 GPU 下 5 秒内生成 5 秒视频）能否推广到更大规模模型或更多模态融合场景，并维持低延迟？
- 将本方法应用于实际机器人 Sim2Real 迁移时，域间隙的量化指标与下游任务性能之间的因果关系如何建立？



## 原文 PDF

![[paperPDFs/WHITEPAPER_2025/Cosmos_Transfer1_Conditional_World_Generation_with_Adaptive_Multimodal_Control.pdf]]
