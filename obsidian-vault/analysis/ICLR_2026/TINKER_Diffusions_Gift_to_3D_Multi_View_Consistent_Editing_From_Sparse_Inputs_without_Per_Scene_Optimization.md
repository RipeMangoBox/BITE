---
title: "TINKER: Diffusion's Gift to 3D--Multi-View Consistent Editing From Sparse Inputs without Per-Scene Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/TINKER_Diffusions_Gift_to_3D_Multi_View_Consistent_Editing_From_Sparse_Inputs_without_Per_Scene_Optimization.pdf
openreview_forum_id: j7Vt2lp2jX
aliases:
- TINKER
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过自构建多视角一致编辑数据集对基础模型进行LoRA微调，使其支持跨视角参考编辑；同时利用深度图作为强约束训练场景补全模型，将稀疏编辑视图传播至稠密视图。"
primary_logic: "大规模图像编辑基础模型（如Flux Kontext）通过简单图像拼接即可展现多视角一致的编辑能力；将编辑任务转化为重建任务，利用深度引导的视频扩散模型实现从稀疏视图高效补全场景，从而彻底消除逐场景优化。"
claims:
- "TINKER在few-shot和one-shot设置下均无需逐场景优化，在3D编辑质量上超过现有方法。"
- "多视角一致编辑微调显著提升跨视角一致性（DINO相似度从0.862提升至0.943）。"
- "深度条件比射线图条件产生更优的几何一致性和细节保留，优于现有深度引导视频生成方法VACE。"
- "Mip-NeRF-360 / IN2N 上 CLIP-dir = 0.157 (few-shot)"
---

# TINKER: Diffusion's Gift to 3D--Multi-View Consistent Editing From Sparse Inputs without Per-Scene Optimization

> [!tip] 核心洞察
> 大规模图像编辑基础模型（如Flux Kontext）通过简单图像拼接即可展现多视角一致的编辑能力；将编辑任务转化为重建任务，利用深度引导的视频扩散模型实现从稀疏视图高效补全场景，从而彻底消除逐场景优化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | TINKER：扩散模型赋能3D编辑——从稀疏输入实现无需逐场景优化的多视角一致编辑 |
| 英文题名 | TINKER: Diffusion's Gift to 3D--Multi-View Consistent Editing From Sparse Inputs without Per-Scene Optimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=j7Vt2lp2jX) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | TINKER |
| Dataset | Mip-NeRF-360 / IN2N, OpenVid-1M (1000 videos) |

> [!tip] 效果简介
> - Mip-NeRF-360 / IN2N 上，CLIP-dir 为 0.157 (few-shot)，对比 0.123 (GaussCtrl)，变化 +0.034。
> - Mip-NeRF-360 / IN2N 上，DINO 为 0.959 (few-shot)，对比 0.957 (GaussCtrl)，变化 +0.002。
> - Mip-NeRF-360 / IN2N 上，Aesthetic 为 6.338 (few-shot)，对比 5.661 (EditSplat)，变化 +0.677。

## 概述

**核心问题**：现有3D场景编辑方法普遍依赖逐场景优化（per-scene finetuning）来维持多视角一致性，这不仅带来高昂的计算开销，也未能充分利用最新大规模2D基础模型的生成能力。同时，直接从稀疏编辑视图重建完整3D场景面临“局部一致但全局不一致”的困境——即使通过图像拼接实现相邻视图的一致编辑，不同拼接对之间仍存在显著差异（Figure 2）。

**核心洞察与因果机制**：TINKER 发现大规模图像编辑基础模型（如 Flux Kontext）通过简单的双图水平拼接即可展现跨视角一致编辑的潜力，但缺乏“参考编辑”能力——即根据已编辑视图来编辑另一视图。基于此，TINKER 将3D编辑重构为两个子问题：（1）通过自构建数据集和 LoRA 微调，赋予基础模型跨视角参考编辑能力；（2）利用深度图作为强几何约束，将稀疏编辑视图传播为稠密、多视角一致的视频帧，从而将编辑转化为重建任务，彻底消除逐场景优化。

**方法定位**：TINKER 是一种无需逐场景优化的3D编辑框架，由两个核心模块构成——多视角一致编辑器（基于 Flux Kontext 的 LoRA 微调）和场景补全模型（基于 Wan2.1 的深度条件视频扩散模型）。它接收1-2张稀疏输入视图，输出可直接用于3DGS优化的稠密编辑视图，在方法谱系中属于“零样本编辑+重建”范式，区别于 DGE、GaussCtrl、TIP-Editor 等需要逐场景训练或超参数调优的方法。

**主要结果**：在 Mip-NeRF-360 / IN2N 基准上，TINKER 的 few-shot 设置在 CLIP-dir（0.157 vs GaussCtrl 0.123）、DINO（0.959 vs GaussCtrl 0.957）和 Aesthetic（6.338 vs EditSplat 5.661）指标上均取得最优，且支持消费级 GPU（24G）上的15分钟快速编辑。消融实验证实：LoRA 微调使跨视角 DINO 相似度从 0.862 提升至 0.943（Table 2）；深度条件显著优于射线图条件（Text-Image Similarity 0.821 vs 0.783，Table S1）；双图拼接在一致性与保真度间达到最佳平衡（Figure 8）。用户研究进一步表明 TINKER 在文本相似度、编辑质量和多视角一致性三个维度上更符合主观偏好（Table S4）。

**局限性**：当前方法依赖深度约束，无法处理涉及大幅几何变形的编辑；合成训练数据中个别样本的细节一致性有待提升。

## 背景与动机

3D场景编辑是计算机视觉与图形学中的核心任务，其目标是在保持多视角几何一致性的前提下，根据用户指令对三维场景进行语义修改。近年来，基于3D高斯泼溅（3D Gaussian Splatting, 3DGS）的显式表示方法因其高效的渲染能力和灵活的可编辑性，已成为该领域的主流范式。

然而，现有3D编辑方法面临一个根本性的瓶颈：**多视角一致性与计算效率之间的尖锐矛盾**。以**TIP-Editor**（基于SDS优化）、**GaussCtrl**（基于注意力对齐）、**DGE**（基于多视图特征对齐）和**EditSplat**（基于3DGS编辑）为代表的现有方法，普遍依赖逐场景微调（per-scene finetuning）来维持编辑后的多视角一致性——要么在生成编辑视图阶段进行场景特定的训练，要么在3DGS优化过程中反复调参。这种逐场景优化的策略带来了两个严重问题：其一，计算开销巨大，部分方法在消费级GPU上甚至无法运行；其二，编辑效果受限于优化过程的稳定性，难以充分利用最新的大规模2D基础模型所蕴含的生成能力。

与此同时，2D图像编辑领域经历了范式级跃迁。以**Flux Kontext**为代表的DiT架构（Diffusion Transformer）流匹配模型，展现出远超传统U-Net扩散模型（如InstructPix2Pix）的编辑质量和指令遵循能力。一个关键的观察是：当将两个不同视角的图像水平拼接后输入此类大模型，模型能够产生局部高度一致的编辑结果。这一现象暗示，**大规模图像编辑基础模型内部可能已经蕴含了隐式的3D感知能力**，只是尚未被系统性挖掘。

但这一潜力存在两个关键缺口（如Figure 2所示）：
1. **局部一致，全局断裂**：拼接两视图编辑虽能保证该对之间的一致性，但不同拼接对之间仍存在显著差异，无法形成全局统一的三维编辑。
2. **缺乏参考编辑能力**：现有基础模型无法以已编辑视图为参考来编辑另一视图——即缺乏跨视角的“参考引导编辑”（reference-based editing）能力，而这正是实现多视角一致编辑的关键。

上述观察揭示了一个清晰的研究机会：**能否通过重新激活预训练扩散模型的隐式3D意识，构建一个无需任何逐场景优化的3D编辑框架？** 这需要同时解决两个子问题：（1）如何赋予基础模型跨视角参考编辑的能力；（2）如何从稀疏的编辑视图高效传播至稠密视图，完成场景级重建。

## 核心创新

TINKER 的核心创新在于通过**两个关键设计**彻底消除了现有3D编辑方法对逐场景优化（per-scene finetuning）的依赖，同时实现了从稀疏输入到多视角一致编辑的高质量输出。

### 关键改进槽位

#### 1. 逐场景优化 → 零样本编辑

现有方法（如 **TIP-Editor**、**GaussCtrl**）需要在每个场景上执行训练或超参数调优，计算开销大且在消费级GPU上可能不可行。TINKER 通过将编辑任务分解为“多视角一致编辑”和“深度引导场景补全”两个独立模块，使得整个编辑流程无需任何逐场景微调（Section 3.1）。在 few-shot 设置下，TINKER 以 CLIP-dir 0.157 显著优于最强基线 GaussCtrl 的 0.123（Table 1），同时保持 15 分钟左右的平均编辑时间。

#### 2. U-Net 架构 → DiT 流匹配架构

以往方法多基于 U-Net 扩散模型（如 InstructPix2Pix），其注意力设计紧密耦合于 U-Net 结构。TINKER 直接采用 DiT-based 的流匹配基础模型 **Flux Kontext**，并通过 LoRA 微调赋予其参考编辑能力。实验表明，将 U-Net 编辑器简单替换为 FLUX 会导致严重性能退化甚至失败（Table S3, Figure S7），而 TINKER 的设计充分利用了 DiT 架构对大规模拼接输入的兼容性。

#### 3. 射线图条件 → 深度图条件

场景补全阶段，TINKER 采用**深度图作为几何约束**，而非现有视频生成方法常用的射线图（ray-map）条件。深度图由 Video Depth Anything 从原始 3DGS 渲染视频中估计获得，提供像素级几何先验。在 DL3DV/Re10k 等多数据集测试中，深度条件在 Text-Image Similarity（0.821 vs 0.783）、DINO（0.978 vs 0.916）和 Aesthetic（6.586 vs 5.833）上全面优于射线图条件（Table S1），且比现有深度引导视频生成方法 VACE 更严格遵循深度约束，产生更好的几何一致性和细节保留（Figure S4）。

#### 4. 独立编辑 → 参考引导的多视角一致编辑

基础模型通过简单拼接两张图像即可实现局部一致编辑，但不同拼接对之间存在显著不一致（Figure 2a），且模型缺乏参考编辑能力（Figure 2b）。TINKER 通过**自构建数据集**：利用基础模型生成大量拼接编辑对，经 DINOv2 编辑强度过滤和跨视角一致性筛选后，构建“原始图像-参考编辑图像”配对数据，再以 LoRA 微调基础模型本身，使其学会根据参考视图执行编辑。微调后 DINO 跨视角相似度从 0.862 提升至 0.943，同时保持文本-图像对齐和美学质量（Table 2, Figure 7）。

### 因果机制

核心洞察在于：大规模图像编辑基础模型通过简单图像拼接已展现**潜在的3D感知能力**。TINKER 通过两个互补的微调阶段激活并强化了这一能力——多视角一致编辑器确保稀疏编辑视图的全局一致性，深度引导的场景补全模型将稀疏编辑传播至稠密视图，从而将3D编辑转化为“参考编辑+几何约束重建”的复合任务，彻底绕过逐场景优化。

## 整体框架

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_j7Vt2lp2jX/figures/004_Figure_3.jpg]]
*Figure 3: Overview of our editing process. We first apply our multi-view consistent editing model to obtain coherent sparse views. Leveraging depth constraints from the rendered results, we generate a large number of consistent edited images. The edited images are used to optimize the 3DGS to achieve high-quality 3D editing*

TINKER的核心设计理念是将3D编辑任务分解为两个解耦的子问题——**稀疏视图的多视角一致编辑**与**从稀疏到稠密的场景补全**——从而彻底消除传统方法中必需的逐场景优化（per-scene finetuning）。整个pipeline由四个模块串联构成，数据流呈线性推进。

### 编辑流程总览

给定一个预重建的3D高斯泼溅（3DGS）场景表示 $\mathbf{G}$，编辑流程起始于从 $\mathbf{G}$ 渲染若干视频序列，并从中随机选取少量稀疏视图（few-shot设置下通常为2-4个视图）。这些稀疏视图首先经过**多视角一致编辑器**（Multi-view Consistent Editor）获得编辑后的参考视图；同时，原始渲染视频通过**视频深度估计器**（Video Depth Anything）提取深度图序列作为几何先验。随后，**场景补全模型**（Scene Completion Model）以深度图和参考编辑视图为条件，从稀疏编辑视图生成稠密的多视角一致编辑图像。最终，这些生成的编辑图像用于优化3DGS，得到编辑后的3D场景。

对于**one-shot**设置，TINKER采用渐进式传播策略：将唯一的编辑视图作为初始参考，由场景补全模型生成第一批编辑视图；这些新生成的视图再作为后续参考视图，迭代扩展覆盖范围，直至生成足够稠密的编辑视图用于3DGS优化。

### 模块间关系

Figure 3清晰展示了四个模块的串联关系与数据依赖：

1. **多视角一致编辑器**（Section 3.2）：基于Flux Kontext DiT架构，通过LoRA在自构建的参考编辑数据集上微调，使模型学会根据参考视图对目标视图进行一致性编辑。该模块接受稀疏原始视图和文本提示，输出编辑后的参考视图，为后续场景补全提供编辑语义锚点。

2. **视频深度估计器**（Section 3.1）：利用Video Depth Anything从原始3DGS渲染视频中估计深度图。深度图作为强几何约束，在场景补全阶段指导模型保持正确的空间结构和遮挡关系。

3. **场景补全模型**（Section 3.3）：基于Wan2.1视频扩散模型微调，以深度图和参考编辑视图为条件，将稀疏编辑视图传播至整个视频序列。其核心输入构造为 $\mathbf{X}_{input}^t = \operatorname{Concat}(\mathbf{Z}^t, \mathbf{D}, \mathbf{V})$，其中 $\mathbf{Z}^t$ 为噪声隐变量，$\mathbf{D}$ 为深度图token，$\mathbf{V}$ 为参考视图token。关键设计在于参考视图、深度图与目标帧共享相同的位置嵌入 $\operatorname{PE}(\mathbf{V}) = \operatorname{PE}(\mathbf{D}_j) = \operatorname{PE}(\mathbf{X}_j)$，使模型能够建立跨帧的空间对应关系。

4. **3DGS优化**（Section 3.1）：使用NeRFStudio框架，以场景补全模型生成的稠密编辑图像作为监督信号优化3DGS，得到最终的编辑后3D场景。

### 关键设计决策

整个框架的两个核心因果节点是：**(1) 多视角一致编辑微调**使基础模型获得参考编辑能力，将成对拼接的一致性扩展为全局一致性（DINO相似度从0.862提升至0.943，Table 2）；**(2) 深度图条件**替代传统射线图条件，为场景补全提供更强的几何约束，在Text-Image Similarity上从0.783提升至0.821，并显著优于同期深度引导视频生成方法VACE（Table S1）。

这两个设计共同实现了“编辑即重建”的范式转换——将编辑任务转化为以深度为约束、参考视图为条件的场景重建问题，从而彻底绕过了逐场景优化的计算瓶颈。

## 核心模块与公式推导

TINKER 由两个核心模块串联构成：**多视角一致编辑器**（Multi-view Consistent Editor）和**场景补全模型**（Scene Completion Model）。两个模块均基于流匹配（Flow Matching）框架训练，共享 DiT（Diffusion Transformer）架构，但承担不同的功能角色。

---

### 模块一：多视角一致编辑器

该模块解决的核心问题是：给定一个已编辑的参考视图，如何对其他视角的原始视图施加一致的编辑。直接使用现成的大规模图像编辑基础模型（如 Flux Kontext）无法完成“参考式编辑”——即将未编辑图像与已编辑图像拼接后，模型不会自动以已编辑图像为参考来编辑未编辑图像（见 Figure 2b）。TINKER 通过自构建数据集 + LoRA 微调赋予模型这一能力。

**数据生成**：利用基础编辑模型 $\mathcal{E}$ 对水平拼接的两张视图进行联合编辑，生成大量编辑对。设原始视图为 $\mathbf{I}_a, \mathbf{I}_b$，编辑提示为 $P$，则编辑过程为：

$$
\mathbf{I}_a', \mathbf{I}_b' = \mathcal{E}(\operatorname{Concat}(\mathbf{I}_a, \mathbf{I}_b), P) \tag{1}
$$

随后通过两道过滤筛选高质量训练样本：
- **编辑强度过滤**：用 DINOv2 特征相似度衡量编辑前后的变化幅度，相似度过高表示编辑不足，直接丢弃：

$$
s_{\text{noedit}} = \max\big(\sin(f_{\text{dino}}(\mathbf{I}_a), f_{\text{dino}}(\mathbf{I}_a')),\; \sin(f_{\text{dino}}(\mathbf{I}_b), f_{\text{dino}}(\mathbf{I}_b'))\big) \tag{2}
$$

- **跨视角一致性过滤**：丢弃两视图间 DINO 相似度低于阈值的样本，确保训练数据本身具有多视角一致性。

**训练目标**：将原始图像与另一视角的已编辑图像水平拼接，训练模型学会以参考图像为引导进行编辑。训练采用流匹配损失，在潜空间最小化预测速度与真值速度的差异：

$$
\text{Loss} = \mathbb{E}_{\mathbf{z}_0, t} \left\| \mathcal{E}_\theta(\mathbf{z}_t, t, P) - u(\mathbf{z}_t') \right\|_2^2 \tag{3}
$$

其中 $\mathbf{z}_t$ 为加噪后的潜变量，$\mathcal{E}_\theta$ 为待训练的编辑模型，$u(\mathbf{z}_t')$ 为从干净潜变量 $\mathbf{z}_0$ 到 $\mathbf{z}_t'$ 的真实速度场。通过 LoRA 微调，模型学会在保持文本-图像对齐的前提下，使编辑结果与参考视图保持一致。

**效果**：微调后 DINO 跨视角相似度从 0.862 提升至 0.943，同时 CLIP-dir 和 Aesthetic 分数基本持平（Table 2），验证了该模块在不牺牲编辑质量的前提下显著提升全局一致性。

---

### 模块二：场景补全模型

该模块将稀疏编辑视图传播至稠密视图，本质上是将编辑任务转化为**深度引导的图像到视频生成任务**。输入由三部分拼接而成：噪声潜变量 $\mathbf{Z}^t$、深度图序列 $\mathbf{D}$、参考编辑视图 $\mathbf{V}$：

$$
\mathbf{X}_{\text{input}}^t = \operatorname{Concat}(\mathbf{Z}^t, \mathbf{D}, \mathbf{V}) \tag{4}
$$

**关键设计——位置嵌入共享**：参考视图、深度图与目标帧共享相同的位置嵌入（Positional Embedding），使模型理解它们对应同一相机位姿：

$$
\operatorname{PE}(\mathbf{V}) = \operatorname{PE}(\mathbf{D}_j) = \operatorname{PE}(\mathbf{X}_j) \tag{5}
$$

这一设计是深度约束得以生效的核心机制：模型通过位置嵌入将深度几何信息与目标帧像素位置对齐，从而在生成过程中严格遵循场景几何结构。

**训练目标**：同样采用流匹配损失，但仅对噪声潜变量对应位置的输出计算损失，条件 token（深度图、参考视图）对应的输出被丢弃，不参与梯度回传（见 Figure 5）：

$$
\text{Loss} = \mathbb{E}_{\mathbf{z}_0, t} \left\| \Phi_\theta(\mathbf{X}_{\text{input}}^t, t) - u(\mathbf{Z}^t) \right\|_2^2 \tag{6}
$$

其中 $\Phi_\theta$ 为场景补全模型，文本嵌入被固定为常量嵌入，迫使模型完全依赖深度图和参考视图进行生成，而非依赖文本提示。

**深度条件的优势**：与射线图（Ray-Map）条件相比，深度图条件产生更准确的几何结构和细节保留（Table S1: Text-Image Similarity 0.821 vs 0.783）；与现有深度引导视频生成方法 VACE 相比，本方法更严格遵循深度约束，多视角一致性更好（DINO 0.978 vs 0.916），且美学质量更高（6.586 vs 5.833）。

---

### 模块协同与推理流程

两个模块在推理时串联工作（见 Figure 3）：首先从原始 3DGS 渲染视频中随机选取稀疏视图，经多视角一致编辑器生成参考编辑视图；同时利用 Video Depth Anything 从渲染视频中估计深度图序列；最后将深度图与参考视图输入场景补全模型，生成稠密的多视角一致编辑图像，用于优化 3DGS 得到最终编辑场景。整个过程无需任何逐场景微调。

## 实验与分析

### 主要结果

TINKER在Mip-NeRF-360/IN2N基准上，无论few-shot还是one-shot设置，均无需任何逐场景微调即可取得最优3D编辑质量。Table 1显示，TINKER-few-shot的CLIP-dir达到0.157，显著优于最强基线GaussCtrl的0.123（提升27.6%）；DINO一致性指标为0.959，与GaussCtrl的0.957持平；美学质量（Aesthetic）达6.338，远超EditSplat的5.661。在计算开销方面，TINKER仅需约15分钟即可完成编辑，且可在24G显存消费级GPU上运行，而部分基线方法因逐场景优化需求，在相同硬件上可能不可行。


![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_j7Vt2lp2jX/figures/008_Table_1.jpg]]
*Table 1: Quantitative comparisons of different methods. TINKER achieves superior results with acceptable computational cost*

定性对比（Figure 6）进一步验证了TINKER在新视角下的视觉质量优势和编辑多样性。用户主观研究（Table S4）从文本相似度、编辑质量和多视角一致性三个维度评估，TINKER-few-shot分别获得4.52、4.61、4.55分（满分5分），在所有方法中排名第一，TINKER-one-shot紧随其后，表明方法更符合用户主观偏好。

### 消融实验

**多视角一致编辑微调**。Table 2和Figure 7展示了LoRA微调前后的关键变化：跨视角DINO相似度从0.862跃升至0.943，验证了微调显著提升了全局一致性；同时CLIP-dir（0.277→0.281）和美学质量（7.058→6.973）基本保持稳定，说明一致性提升并未以牺牲文本对齐或视觉保真度为代价。微调后模型能够根据参考视图精确执行编辑，有效消除了拼接编辑中的跨视角不一致问题。


![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_j7Vt2lp2jX/figures/012_Table_2.jpg]]
*Table 2: After multi-view consistent image editing fine-tuning, the edited images exhibit substantially improved multi-view consistency, while maintaining comparable text–image alignment and aesthetic quality to the nonfinetuned results*

**拼接图像数量**。Figure 8分析了水平拼接图像数量对编辑质量的影响：拼接2张图像在一致性与保真度之间取得最佳平衡；拼接过多图像会导致严重的视觉质量退化，美学评分显著下降。

**深度条件 vs. 射线图条件**。Table S1和Figure S3对比了场景补全模型中不同条件信号的效果。Ours-Depth在文本-图像相似度（0.821）、DINO一致性（0.978）和美学质量（6.586）三项指标上全面优于Ours-Ray-Map（0.783/0.968/6.170），证实深度图作为几何约束能产生更准确的几何结构和更好的细节保留。

**与VACE的对比**。Table S1同时显示，本方法在深度引导视频生成任务上显著优于VACE：文本-图像相似度0.821 vs 0.760，DINO 0.978 vs 0.916，美学质量6.586 vs 5.833。Figure S4进一步表明，本方法更严格遵循深度约束，多视角一致性更好，细节保留更优。在视频重建应用上（Table S2），仅使用第一帧和深度序列，TINKER的PSNR达31.869，SSIM达0.941，远超VACE的16.635和0.331。

### 失败模式与架构适配

**直接替换U-Net编辑器的失败**。Figure S7和Table S3揭示了将现有U-Net架构编辑方法（如DGE、GaussCtrl）直接适配到FLUX（DiT架构）的严重后果：注意力设计紧密耦合U-Net结构，直接替换导致严重性能退化甚至完全失败，编辑结果出现严重像素化和噪声伪影；即使勉强运行，计算开销也高达133分钟且需要超过24GB显存，不具备实用性。

**方法局限性**。合成数据集由基础模型生成，个别样本的细节可能存在不一致；场景补全模型基于深度约束，目前无法处理涉及大幅几何变形的编辑任务。

### 补充图表

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_j7Vt2lp2jX/figures/018_Table_3.jpg]]
*Table 3: Table S1: Quantitative comparisons of different conditions and different depth-guided video generation models. Our approach achieves the best overall performance*

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_j7Vt2lp2jX/figures/020_Table_4.jpg]]
*Table 4: Table S2: Quantitative comparisons of video reconstruction with first frame and depth as input*

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_j7Vt2lp2jX/figures/023_Table_5.jpg]]
*Table 5: Table S3: Quantitative comparisons of FLUX-adapted different methods. Simply replacing U-Net editors with FLUX is unviable, leading to prohibitive costs and even failed due to critical architectural mismatches*

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_j7Vt2lp2jX/figures/024_Table_6.jpg]]
*Table 6: Table S4: We conducted a user study across three dimensions: text similarity, editing quality, and multi-view consistency. The results indicate that our method better aligns with subjective user preferences*

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_j7Vt2lp2jX/figures/022_Figure_18.jpg]]
*Figure 18: Vincent van Gogh Fail Figure S7: Prior methods’ attention designs are tightly coupled with the U-Net architecture, causing severe performance degradation when the editing model is directly replaced*


## 方法谱系与知识库定位

### 1. 与现有3D编辑方法的关系

TINKER 的核心突破在于将3D编辑从“逐场景优化”范式解放出来，转而利用大规模2D基础模型的潜在3D感知能力。现有方法可大致分为三类，TINKER 在每一类上都做出了结构性改进：

**基于SDS优化的方法**（如 **TIP-Editor**）通过分数蒸馏采样（SDS）将2D扩散先验注入3D表示，但需要逐场景迭代训练，计算开销大且易产生模式坍塌。TINKER 完全避开了SDS路径，将编辑转化为“稀疏视图编辑+稠密视图补全”的重建任务，实现了zero-shot编辑。

**基于多视图特征/注意力对齐的方法**（如 **DGE**、**GaussCtrl**）通过对齐不同视图间的特征或注意力图来保持一致性，但这类方法通常需要逐场景调优超参数，且其注意力设计紧密耦合于U-Net架构。TINKER 的消融实验（Table S3）表明，直接将这类方法中的U-Net编辑器替换为FLUX会导致严重性能退化甚至失败，根本原因在于架构不匹配——DiT-based的FLUX与U-Net的注意力机制不可直接迁移。

**基于3DGS编辑的方法**（如 **EditSplat**）直接在3D高斯表示上进行操作，但受限于3DGS的表达能力，编辑的多样性和质量有限。TINKER 在2D图像空间完成所有编辑操作，仅将3DGS作为最终渲染载体，从而充分利用了大规模图像编辑模型的能力。

### 2. 与基础模型生态的定位

TINKER 的方法设计深度绑定于两个关键基础模型的选择：

- **Flux Kontext**（DiT-based flow matching模型）作为多视角一致编辑器的基座。其通过简单图像拼接即可展现多视角一致编辑能力（Figure 2a），这是TINKER方法可行性的核心前提。论文通过LoRA微调赋予其“参考编辑”能力（Figure 2b → Figure 7），使模型从“被动保持拼接一致性”升级为“主动跟随参考视图编辑”。

- **Wan2.1**（视频扩散模型）作为场景补全模型的基座。TINKER 将其改造为深度条件驱动的图像到视频生成模型，关键设计在于：参考视图、深度图与目标帧共享相同的位置嵌入（Eq.5），使模型能够将稀疏编辑视图的语义信息传播到整个视频序列。

与现有深度引导视频生成方法 **VACE** 的对比（Table S1, Figure S4）表明，TINKER 的场景补全模型更严格地遵循深度约束，在多视角一致性（DINO: 0.978 vs 0.916）和美学质量（Aesthetic: 6.586 vs 5.833）上均有显著优势。视频重建实验（Table S2）进一步验证了深度条件的有效性：仅用第一帧和深度序列即可实现PSNR 31.869的高质量重建，远超VACE的16.635。

### 3. 适用边界与局限

**适用场景**：
- 物体级和场景级编辑（Figure 1, Figure 6）
- Few-shot（2-3个视图）和one-shot（1个视图）设置
- 静态3DGS场景及4D动态场景编辑（Figure S2）
- 消费级GPU（24G显存）可运行，编辑时间约15分钟（Table 1）

**已知局限**：
1. **无法处理大幅几何变形**：场景补全模型依赖深度图作为几何约束，当编辑涉及显著几何变化时（如物体形状改变），深度图与编辑后场景不匹配，模型无法正确补全。论文明确指出这是当前方法的限制。
2. **合成数据集的细节不一致**：多视角一致编辑器的训练数据由基础模型自动生成，尽管经过编辑强度过滤（Eq.2）和跨视角一致性筛选，个别样本仍可能存在细节不一致，这可能在边缘情况下影响编辑质量。
3. **拼接图像数量的权衡**：消融实验（Figure 8）表明，拼接2张图像可获得一致性与保真度的最佳平衡；拼接过多图像会导致图像质量严重下降。这意味着模型在单次前向传播中能处理的多视角数量有限。

### 4. 开放问题

1. **几何变形编辑的扩展**：如何在保持深度约束优势的同时，支持涉及大幅几何变形的编辑？可能的路径包括引入可变形深度图或结合3D感知的变形场。

2. **合成数据一致性的进一步提升**：当前数据生成依赖基础模型的拼接编辑能力，其跨视图一致性在“局部一致但全局不一致”的瓶颈（Figure 2a）。如何构建更高质量的多视角编辑数据集，是进一步提升模型性能的关键。

3. **架构迁移的通用性**：论文证明直接将U-Net方法迁移到DiT架构不可行（Figure S7, Table S3），但未探索是否存在通用的架构适配策略，使现有3D编辑方法能够利用DiT-based基础模型的能力。

## 原文 PDF

![[paperPDFs/ICLR_2026/TINKER_Diffusions_Gift_to_3D_Multi_View_Consistent_Editing_From_Sparse_Inputs_without_Per_Scene_Optimization.pdf]]
