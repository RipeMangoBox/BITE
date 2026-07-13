---
title: "MotionVerse: A Unified Multimodal Framework for Motion Comprehension, Generation and Editing"
type: paper
paper_level: A
venue: PAMI
year: 2025
pdf_ref: paperPDFs/PAMI_2025/MotionVerse_A_Unified_Multimodal_Framework_for_Motion_Comprehension_Generation_and_Editing.pdf
project_link: null
code_link: null
aliases:
- MotionVerse
tags:
- PAMI_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入残差向量量化（RVQ）生成多流运动令牌，采用延迟并行建模策略有效捕获流间依赖，并设计模态隔离的双塔架构分离运动和文本表示。
primary_logic: 通过多流离散表示和模态隔离，大语言模型可以在不互相干扰的前提下统一处理多种运动相关任务，实现端到端的理解、生成和编辑。
claims:
- 延迟并行建模在文本到运动任务上相比扁平和并行策略显著提升了Top-1准确率和MM距离（表10）。
- 模态隔离架构（MoE/MIS）相比共享参数的Prototype和LoRA有效降低了模态干扰，在多任务训练下性能提升明显（表11）。
- 残差向量量化（L=6）相比普通VQ在运动重建和生成质量上均有大幅改善（表9）。
- 任务特定的运动塔（TMT）在多任务指令微调中缓解了任务间干扰，各子任务性能一致提升（表12-14）。
---

# MotionVerse: A Unified Multimodal Framework for Motion Comprehension, Generation and Editing

> [!tip] 核心洞察
> 通过多流离散表示和模态隔离，大语言模型可以在不互相干扰的前提下统一处理多种运动相关任务，实现端到端的理解、生成和编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionVerse：一个统一的面向运动理解、生成和编辑的多模态框架 |
| 英文题名 | MotionVerse: A Unified Multimodal Framework for Motion Comprehension, Generation and Editing |
| 会议/期刊 | PAMI 2025 |
| Links |  [paper](https://arxiv.org/abs/2509.23635)|
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MotionVerse |
| Dataset | InterX, MotionX, InterHuman |

> [!tip] 效果简介
> - InterX (Interactive Text-to-Motion) 上，R-Precision Top-1 70.2 vs 66.0 (TM2T) (+4.2)。
> - MotionX (Text-to-Motion) 上，FID 0.010 vs N/A (优于多数基线，FID略高于MoMask) (N/A)。
> - MotionX (Motion-to-Text) 上，BLEU@4 15.8 vs N/A (最优) (N/A)。

## 概要

### 问题背景

人类运动理解与生成是计算机视觉的核心课题，涵盖文本到运动（T2M）、运动到文本（M2T）、运动预测、运动编辑、交互式双人运动生成与反应等多种子任务。然而，现有方法面临两个根本性瓶颈：

1. **任务碎片化**：单人和交互式运动任务被分别处理，缺乏统一的建模框架。大多数方法仅覆盖少数几项任务（参见Table 1），难以实现跨任务的泛化与协同。
2. **模态干扰与信息丢失**：早期统一尝试（如**MotionGPT**，Jiang et al., NeurIPS 2023）采用简单的向量量化（VQ）将运动压缩为单层离散令牌，导致细粒度运动细节丢失；同时，共享参数的Transformer架构使运动与文本模态在表示空间中相互干扰，限制了多任务学习的性能上限。

### 核心方法

**MotionVerse** 提出了一套系统性的解决方案，核心思路是“多流离散表示 + 模态隔离架构”：

- **残差向量量化（RVQ）**：摒弃单层VQ，采用L层残差码本将连续运动序列转化为多流离散令牌（见Figure 4）。每一层码本编码上一层的量化残差，从而以层级方式保留从粗到细的运动动态信息。消融实验（TABLE 9）表明，RVQ（L=6）相比VQ在运动重建和生成质量上均有大幅改善——T2M任务的FID从0.036降至0.012，Top-1准确率从25.3跃升至41.7。

- **延迟并行建模**：针对多流令牌的依赖关系建模，提出延迟并行策略（见Figure 1(c)）。与扁平化（将所有流拼接为单一长序列）和并行预测（各流独立建模）不同，延迟并行通过为各流引入时间偏移，使LLM的自回归注意力机制能同时捕获流内时序依赖和流间层级残差依赖，且计算复杂度仅为 $O(T^2)$ 而非 $O((T \times L)^2)$（见Table 2）。消融实验（TABLE 10）证实，延迟并行在T2M任务上的Top-1准确率（79.5）显著优于并行（75.2）和扁平化（68.9）。

- **模态隔离的双塔架构（Motion-Fusion）**：为消除运动与文本的模态干扰，设计运动塔和文本塔分离的架构。探索了三种实现变体：LoRA（低秩适配）、MoE（混合专家，为运动模态复制FFN层）和MIS（模态隔离架构，为运动模态复制完整Transformer块），如Figure 2所示。消融实验（TABLE 11）表明，MoE变体在InterX交互式T2M任务上的Top-1准确率（71.9）比共享参数的Prototype基线（63.8）高出约8个百分点。

- **任务特定运动塔（TMT）与三阶段训练**：在多任务指令微调阶段引入任务特定的运动塔，缓解不同子任务间的干扰。三阶段训练流水线依次为：令牌器训练、运动-文本对齐预训练、多任务指令微调。消融实验（TABLES 12-14）表明，移除TMT会导致各子任务性能普遍下降，尤其在运动反应和编辑任务上损失显著。

### 主要结果

MotionVerse在8项运动相关任务上进行了统一评估，覆盖单人和双人场景：

- **文本到运动生成（T2M）**：在MotionX数据集上，FID达到0.010，与专门优化的**MoMask**（Guo et al., CVPR 2024）可比，同时显著优于**MotionGPT**等统一框架（TABLE 3）。
- **交互式文本到运动（I-T2M）**：在InterX数据集上，R-Precision Top-1达到70.2，超越**TM2T**（66.0）等基线（TABLE 4）。
- **运动到文本（M2T）**：在MotionX上，BLEU@4达到15.8，取得最优结果（TABLE 5）。
- **运动反应生成**：在InterHuman数据集上，Top-1 R-Precision达到50.3，优于**MDM**（Tevet et al., arXiv 2022）和**ReGenNet**（Xu et al., CVPR 2024）（TABLE 7）。
- **运动编辑**：在MotionFix数据集上，各项指标均优于专用编辑方法**TMED**（Athanasiou et al., SIGGRAPH 2024）（TABLE 8）。

### 方法定位

MotionVerse属于“统一多模态运动框架”这一新兴范式。与**MotionGPT**等早期工作相比，其关键区分点在于：通过RVQ实现多流离散表示以保留运动细节，通过模态隔离架构化解模态干扰，并通过延迟并行建模高效捕获流间依赖。在方法谱系上，它融合了残差量化的表示优势、LLM的序列建模能力，以及多任务指令微调的灵活性，为“任意到运动”的统一生成奠定了基础。

### 局限与开放问题

尽管MotionVerse在统一性上取得突破，仍需注意以下局限：统一架构在个别指标（如T2M的FID）上略逊于单任务专用模型（如MoMask），多任务学习与单任务专精之间仍需权衡；T5-Large相比T5-Base未带来显著增益，表明当前任务规模可能已饱和；评估限于公开数据集，未在真实交互或机器人场景中验证。开放问题包括：延迟并行策略能否自适应调整延迟量、模态隔离效果能否用梯度冲突等量化指标进一步验证、框架能否扩展至音频和场景上下文等更多模态。

### 问题背景

人类运动理解与生成是计算机视觉和图形学中的核心问题，涉及文本到运动生成、运动到文本描述、运动预测、运动编辑、运动反应生成等多样化任务。这些任务在电影制作、游戏开发、虚拟现实和人机交互等领域具有广泛的应用前景。近年来，大语言模型（LLM）的兴起为统一处理多种运动相关任务提供了新的范式——将连续运动序列离散化为运动令牌，使其能够像自然语言一样被LLM理解和生成。

然而，现有方法面临两个根本性瓶颈。**第一，单人运动与交互式多人运动被分别处理**。如表1所示，**MoMask**（Guo et al., CVPR 2024）专注于文本到运动生成，**InterGen**（Liang et al., IJCV 2024）针对交互式文本到运动生成，**ReGenNet**（Xu et al., CVPR 2024）则面向运动反应生成，各方法任务覆盖范围碎片化，缺乏统一的框架。**第二，简单向量量化导致信息丢失，共享参数架构引发模态干扰**。早期统一模型如**MotionGPT**（Jiang et al., NeurIPS 2023）采用单层向量量化（VQ）将运动压缩为单一令牌流，但VQ的信息瓶颈使得精细运动动态难以完整保留；同时，运动与文本模态共享同一Transformer参数空间，导致两类异质信号相互干扰，限制了多任务联合学习的性能上限。

### 现有方法缺口

当前方法的缺口可归纳为三个层面：

1. **表示层面**：单层VQ或单流令牌无法充分保留运动序列的层次化结构信息。运动本质上具有多尺度时序依赖，粗糙的离散化会导致重建质量下降和生成保真度不足。

2. **建模层面**：多流运动令牌的建模策略尚未被系统探索。当运动被分解为多个残差令牌流时，如何在LLM的自回归框架内高效捕获流内时序依赖与流间层次依赖，是一个待解决的关键问题。简单的扁平化策略丢失了流结构信息，而朴素的并行预测则无法有效建模流间依赖。

3. **架构层面**：共享参数的LLM微调策略（如直接全参数微调或通用LoRA）无法解决运动与文本模态间的干扰问题。在多任务指令微调场景下，不同任务对模态表征的需求各异，缺乏模态隔离机制会导致任务间负迁移，尤其损害运动理解与编辑等依赖精细运动表征的子任务。

### 本文动机

针对上述缺口，本文提出**MotionVerse**——一个统一的多模态框架，旨在以端到端的方式同时处理单人和交互式场景下的运动理解、生成与编辑任务。核心动机是：**通过多流离散表示与模态隔离架构，使LLM能够在不互相干扰的前提下统一处理多种运动相关任务**。

具体而言，MotionVerse引入了三个关键设计：采用**残差向量量化（RVQ）**生成多流运动令牌，以层次化方式保留运动细节；设计**延迟并行建模策略**，在控制计算复杂度的同时有效捕获流间依赖；构建**模态隔离的双塔架构**，为运动和文本分别分配独立的参数空间，从根本上缓解模态干扰。这一设计使得单一模型能够覆盖8类运动任务，在多个基准上取得有竞争力的结果，为通用运动智能提供了新的技术路径。

## 核心方法与创新机理

MotionVerse 的核心创新在于通过三个关键设计，首次将单人运动与交互式运动的理解、生成与编辑统一到一个框架中，并有效抑制了多任务与多模态带来的干扰。

### 1. 多流离散运动表示：从单层量化到残差向量量化

传统方法（如 **MotionGPT**，Jiang et al., NeurIPS 2023）采用单层向量量化（VQ）将运动序列压缩为单一流令牌，这会导致细粒度运动动态的严重信息丢失。MotionVerse 引入了**残差向量量化（RVQ）**，将连续运动序列离散化为 $L$ 层多流令牌：

$$\mathcal{RQ}(z; \mathcal{B}^1, \ldots, \mathcal{B}^L) = (k^1, \ldots, k^L)$$

其递归过程为：

$$k^l = \mathcal{Q}(r^l; \mathcal{B}^l), \quad r^{l+1} = r^l - \mathbf{e}^l(k^l)$$

每一层对上一层的量化残差进行编码，从而分层保留从粗到细的运动信息。消融实验（**Table 9**）证实，RVQ（$L=6$）相比普通 VQ 在文本到运动任务上 FID 从 0.036 降至 0.012，Top-1 准确率从 25.3 跃升至 41.7，重建与生成质量均有决定性提升。

### 2. 延迟并行建模：平衡流内与流间依赖

多流令牌的建模存在一个核心矛盾：扁平化策略（将所有流拼接为单一长序列）虽能捕获流间依赖，但自注意力复杂度为 $O(T^2 L^2)$，计算代价高昂；并行策略（各流独立建模）复杂度仅 $O(T^2 L)$，却完全忽略了跨流依赖。

MotionVerse 提出的**延迟并行建模**策略在二者之间取得了突破性平衡。通过对第 $l$ 流引入 $l-1$ 个前导填充令牌：

$$\widetilde{m}^l = [\underbrace{-1}_{l-1}, m^l, \underbrace{-1}_{L-l}]$$

使得因果注意力能够以 $O(T^2 L)$ 的复杂度同时捕获流内时序依赖和流间层次化残差依赖。其条件概率建模目标为：

$$p(m_t^1, m_{t-1}^2, \ldots, m_{t-L+1}^L | m_{<t}^1, m_{<t-1}^2, \ldots, m_{<t-L+1}^L)$$

消融实验（**Table 10**）表明，延迟并行在文本到运动任务上 Top-1 准确率达 79.5，显著优于并行策略（75.2）和扁平化策略（68.9），同时保持与并行策略相当的计算效率。

### 3. 模态隔离架构：化解运动与文本的模态干扰

现有统一模型（如 **MotionGPT**）采用共享 Transformer 参数同时处理运动和文本令牌，导致严重的模态干扰。MotionVerse 设计了 **Motion-Fusion 模块**，采用双塔架构将运动与文本的表示空间分离。

论文探索了三种实现变体（**Figure 2**）：
- **LoRA**：在自注意力层注入低秩适配矩阵；
- **MoE**：为运动模态复制前馈网络（FFN）作为独立专家；
- **MIS（模态隔离架构）**：为运动模态完整复制 Transformer 块，参数完全独立：

$$h = x + \mathrm{MHSA}(\mathrm{LN}(x, \theta_{\mathrm{ln1}}^{\mathrm{u}}); \theta_{\mathrm{attn}}^{\mathrm{u}})$$
$$x' = h + \mathrm{FFN}(\mathrm{LN}(x, \theta_{\mathrm{ln2}}^{\mathrm{u}}); \theta_{\mathrm{ffn}}^{\mathrm{u}}), \; \mathrm{u} \in \{\mathrm{m}, \mathrm{t}\}$$

消融实验（**Table 11**）证实，MoE 变体在交互式文本到运动任务上 Top-1 准确率（71.9）相比共享参数的 Prototype 基线（63.8）提升约 8 个百分点，MIS 变体进一步提升至最优水平，有力证明了模态隔离对抑制干扰的关键作用。

### 4. 任务特定运动塔：缓解多任务间干扰

在多任务指令微调阶段，MotionVerse 引入了**任务特定的运动塔（TMT）**，为每个子任务（文本到运动、运动到文本、运动预测、运动编辑等）分配独立的输出头。消融实验（**Tables 12-14**）显示，移除 TMT（wo-TMT）会导致各子任务性能一致下降，尤其在运动反应和编辑任务上退化最为明显，验证了任务隔离对统一多任务框架的必要性。

MotionVerse 是一个以多流离散运动令牌和模态隔离架构为核心的统一框架，旨在让大语言模型（LLM）在单人和多人场景下同时胜任运动理解、生成和编辑等多类任务。框架由三个关键组件构成，并通过三阶段训练流水线完成端到端学习。

### 核心设计思路

现有方法将单人和交互式运动任务分别处理，且普遍采用简单向量量化（VQ）将运动压缩为单层离散令牌。这种做法导致两个瓶颈：其一，单层量化丢失了大量细粒度运动动态信息；其二，共享参数架构在同时处理运动和文本两种模态时产生严重的模态干扰，限制了多任务统一建模的能力。MotionVerse 的核心洞察在于：**通过多流离散表示和模态隔离，LLM 可以在不互相干扰的前提下统一处理多种运动相关任务**。

### 三大组件

**1. 运动标记器（RVQ-VAE）**——多流离散化

框架第一级是一个基于残差向量量化（Residual Vector Quantization, RVQ）的 3D 变分自编码器（RVQ-VAE）。给定一段连续运动序列 $\mathbf{X}$，编码器 $\mathcal{E}$ 将其映射为潜在特征 $\mathbf{Z}$，随后通过 $L$ 层码本 $\mathcal{B}^1, \ldots, \mathcal{B}^L$ 进行逐层残差量化：

$$\mathcal{RQ}(z; \mathcal{B}^1, \ldots, \mathcal{B}^L) = (k^1, \ldots, k^L)$$

$$k^l = \mathcal{Q}(r^l; \mathcal{B}^l), \quad r^{l+1} = r^l - \mathbf{e}^l(k^l)$$

对每个时间步 $t$ 的潜在向量 $\mathbf{Z}[t]$ 执行上述量化，运动序列最终被表示为 $L$ 条离散令牌序列 $\dot{\mathbf{M}} = [m^1, \dots, m^L]$。与单层 VQ 相比，RVQ 通过多层残差结构保留了更丰富的运动细节，消融实验证实 $L=6$ 时重建与生成质量均大幅优于普通 VQ（TABLE 9）。

**2. 并行流感知 LLM 骨干（带延迟编码）**——多流令牌建模

获得 $L$ 条运动令牌流后，如何将其输入 LLM 进行自回归建模是关键设计选择。框架对比了三种策略（Figure 1, TABLE 2）：

- **扁平化（Flattening）**：将所有流按时间步交错拼接为单一长序列 $U = [m_1^1, m_1^2, \ldots, m_T^L]$，能同时捕获流内和流间依赖，但序列长度膨胀为 $T \times L$，注意力复杂度为 $\mathcal{O}(T^2 L^2)$。
- **并行建模（Parallel）**：各流独立预测，仅条件于各自的历史令牌，复杂度降为 $\mathcal{O}(T^2 L)$，但完全忽略了流间（跨残差层）的层次依赖。
- **延迟并行建模（Delay Parallel）**：为每条残差流引入时间偏移，例如第 $l$ 流前补 $l-1$ 个空位令牌 $-1$，使同一时间步的多层令牌在序列中错位排列。LLM 在因果注意力下自回归地建模：

$$p(m_t^1, m_{t-1}^2, \ldots, m_{t-L+1}^L \mid m_{<t}^1, m_{<t-1}^2, \ldots, m_{<t-L+1}^L)$$

该策略同时捕获流内时序依赖和流间残差依赖，且复杂度保持 $\mathcal{O}(T^2 L)$。消融实验表明，延迟并行在文本到运动任务上的 Top-1 准确率（79.5）远超并行（75.2）和扁平化（68.9）（TABLE 10）。

**3. Motion-Fusion 模块**——模态隔离的双塔架构

为将预训练 LLM 适配到运动模态，MotionVerse 设计了 Motion-Fusion 模块，采用双塔架构分离运动和文本的表示处理（Figure 2）。具体探索了三种实现变体：

- **LoRA（低秩适配）**：在自注意力层注入低秩矩阵，参数增量小。
- **MoE（混合专家）**：为运动模态复制前馈网络（FFN），形成模态特定的专家子层。
- **MIS（模态隔离架构）**：为运动模态复制完整的 Transformer 块，运动和文本以完全独立的参数通过自注意力和前馈子层：

$$h = x + \mathrm{MHSA}(\mathrm{LN}(x, \theta_{\mathrm{ln1}}^{\mathrm{u}}); \theta_{\mathrm{attn}}^{\mathrm{u}}), \quad x' = h + \mathrm{FFN}(\mathrm{LN}(x, \theta_{\mathrm{ln2}}^{\mathrm{u}}); \theta_{\mathrm{ffn}}^{\mathrm{u}}), \quad \mathrm{u} \in \{\mathrm{m}, \mathrm{t}\}$$

消融实验显示，MoE 变体在多任务训练下的交互式文本到运动 Top-1 准确率（71.9）比共享参数的 Prototype 架构（63.8）高出约 6%（TABLE 11），验证了模态隔离对缓解模态干扰的有效性。

### 三阶段训练流水线

整个框架分三个阶段训练：

1. **令牌器训练**：仅训练 RVQ-VAE，优化目标为 L1 重建损失与承诺损失之和：
   $$\mathcal{L}_{\mathrm{rvq}} = \|\mathbf{X} - \widehat{\mathbf{X}}\|_1 + \beta \sum_{l=1}^L \|\mathbf{R}^l - \mathrm{sg}[\widehat{\mathbf{R}}^l]\|_2^2$$
2. **运动-文本对齐预训练**：固定令牌器，以文本-运动对数据训练 LLM 骨干和 Motion-Fusion 模块，建立跨模态对齐。
3. **多任务指令微调**：引入任务特定的运动塔（Task-specific Motion Tower, TMT），在多种运动任务（文本到运动、运动到文本、运动预测、插值、反应生成、编辑等）上联合微调。移除 TMT 会导致各子任务性能一致下降，尤其在反应和编辑任务上退化明显（TABLES 12–14）。

### 输入输出流

框架以文本指令和/或运动序列作为输入。运动序列经 RVQ-VAE 标记化为 $L$ 条离散令牌流，文本经语言编码器（T5）转换为连续嵌入。两者通过 Motion-Fusion 双塔分别处理后，在 LLM 骨干中由延迟并行注意力联合建模。输出端根据任务类型由对应的预测头解码：生成任务自回归地产出运动令牌流，理解任务则输出文本序列。Figure 3 以三流示例展示了完整的架构流程。

![[assets/figures/papers/paper_list_l1801_MotionVerse_A_Unified_Multimodal_Framework_for_Motion_Comprehension_Gene/figures/004_Figure_3.jpg]]
*Figure 3: Architecture of the proposed MotionVerse framework: Integrating Textural and Multi-stream Motion Tokens via Modality-Aware Autoregressive Transformers (Three-Stream Example)*

MotionVerse 由三个核心模块构成：残差向量量化运动标记器、延迟并行LLM骨干网络、以及模态隔离的Motion-Fusion模块。以下逐一展开其设计逻辑与关键公式。

### 3.1 残差向量量化运动标记器（RVQ-VAE）

**设计动机**：传统向量量化（VQ）将连续运动序列映射为单层离散令牌，在压缩过程中丢失大量细粒度运动细节，导致重建质量下降。残差向量量化（RVQ）通过多层递进式量化，逐层捕获上一层的残差信息，从而以多流令牌形式保留更丰富的运动动态。

**模块结构**：标记器采用3D RVQ-VAE架构，包含运动编码器 $E$、运动解码器 $D$ 以及 $L$ 个分层码本 $\mathcal{B}^1, \ldots, \mathcal{B}^L$。编码器将运动序列 $\mathbf{X}$ 映射为潜在特征 $\mathbf{Z}$，随后对每个时间步的潜在向量进行 $L$ 层残差量化。

**核心公式**：

给定向量 $z$，RVQ将其表示为 $L$ 个离散代码的有序序列：
$$\mathcal{RQ}(z; \mathcal{B}^1, \ldots, \mathcal{B}^L) = (k^1, \ldots, k^L) \tag{1}$$

每一层的递归量化过程为：
$$k^l = \mathcal{Q}(r^l; \mathcal{B}^l), \quad r^{l+1} = r^l - \mathbf{e}^l(k^l), \quad \text{for } l=1,\ldots,L \tag{2}$$
其中 $r^1 = z$ 为初始残差，$\mathbf{e}^l(k^l)$ 为第 $l$ 层码本中索引 $k^l$ 对应的嵌入向量，$\mathcal{Q}$ 为最近邻查找算子。每层量化后，残差减去该层嵌入，传递至下一层继续量化。

将上述操作应用于潜在特征 $\mathbf{Z}$ 的每个时间步 $t$，运动序列被离散化为 $L$ 条令牌流：
$$\mathbf{M}[t] = \mathcal{RQ}(\mathbf{Z}[t]; \mathcal{B}^1, \ldots, \mathcal{B}^L) \tag{3}$$
最终得到多流运动令牌表示 $\dot{\mathbf{M}} = [m^1, \ldots, m^L]$，其中 $m^l = (m_1^l, \ldots, m_T^l)$ 为第 $l$ 层的令牌序列。

**训练目标**：RVQ-VAE的训练损失由L1重建损失和承诺损失组成：
$$\mathcal{L}_{\mathrm{rvq}} = \|\mathbf{X} - \widehat{\mathbf{X}}\|_1 + \beta \sum_{l=1}^L \|\mathbf{R}^l - \mathrm{sg}[\widehat{\mathbf{R}}^l]\|_2^2 \tag{4}$$
其中 $\widehat{\mathbf{X}}$ 为解码器重建的运动，$\mathbf{R}^l$ 为第 $l$ 层的残差，$\widehat{\mathbf{R}}^l$ 为量化后的残差估计，$\mathrm{sg}[\cdot]$ 表示stop-gradient操作，$\beta$ 为承诺损失权重。承诺损失鼓励编码器输出靠近码本嵌入，从而稳定训练。

> **消融证据**：Table 9表明，RVQ（$L=6$）相比普通VQ在MotionX数据集上的文本到运动生成任务中，FID从0.036降至0.012，Top-1准确率从25.3升至41.7，验证了多层残差量化对运动重建和生成质量的关键作用。

### 3.2 延迟并行LLM骨干网络

**设计动机**：RVQ产生的 $L$ 条运动令牌流之间存在层级依赖关系——深层流编码的是浅层流的残差信息。如何在自回归LLM框架中高效建模流内时序依赖和流间残差依赖，是核心挑战。

**三种建模策略对比**（Fig. 1, Table 2）：

1. **扁平化（Flattening）**：将 $L$ 条流按时间步交错拼接为单一长序列：
   $$U = [m_1^1, m_1^2, \ldots, m_1^L, \ldots, m_T^1, m_T^2, \ldots, m_T^L] \tag{5}$$
   优点是可利用标准因果注意力捕获所有依赖，但序列长度膨胀为 $L \times T$，注意力复杂度为 $O(L^2 T^2)$，计算代价高。

2. **并行建模（Parallel）**：$L$ 条流独立自回归，共享LLM骨干但使用独立的预测头：
   $$\widehat{\pmb{m}}^l = g^l(\mathrm{Z}_{\mathrm{dec}}), \quad \text{for } l=1,\ldots,L \tag{8}$$
   条件概率为：
   $$p(m_t^1, m_t^2, \ldots, m_t^L | m_{<t}^1, m_{<t}^2, \ldots, m_{<t}^L) \tag{9}$$
   该方法有效捕获流内时序依赖，但同时间步的各流令牌在注意力机制中相互独立，**无法建模流间残差依赖**。

3. **延迟并行建模（Delay Parallel）**：在并行建模基础上，对第 $l$ 条流引入 $l-1$ 个时间步的前导填充，使深层流在时间轴上滞后于浅层流：
   $$\widetilde{m}^l = [\underbrace{-1}_{l-1}, m^l, \underbrace{-1}_{L-l}] \tag{10}$$
   其中 $-1$ 表示空位令牌。由此，LLM在时间步 $t$ 的条件概率变为：
   $$p(m_t^1, m_{t-1}^2, \ldots, m_{t-L+1}^L | m_{<t}^1, m_{<t-1}^2, \ldots, m_{<t-L+1}^L) \tag{11}$$
   因果注意力机制下，深层流的当前令牌可以关注浅层流的历史令牌，从而**以 $O(T^2)$ 的复杂度同时捕获流内和流间依赖**。

> **消融证据**：Table 10显示，延迟并行在文本到运动任务上的Top-1准确率达到79.5，显著优于并行策略（75.2）和扁平化策略（68.9），验证了其对流间依赖的有效建模。

### 3.3 模态隔离的Motion-Fusion模块

**设计动机**：将运动令牌注入预训练LLM时，运动模态与文本模态共享参数会导致**模态干扰**——两个模态的特征分布差异使共享的注意力层和前馈层难以同时优化，损害多任务学习效果。

**标准Transformer块**（Prototype基线）：
$$\begin{array}{rl}
h &= x + \mathrm{MHSA}(\mathrm{LN}(x, \theta_{\mathrm{ln1}}); \theta_{\mathrm{attn}}), \\
x' &= h + \mathrm{FFN}(\mathrm{LN}(x, \theta_{\mathrm{ln2}}); \theta_{\mathrm{ffn}})
\end{array} \tag{12}$$
运动和文本令牌通过同一组参数 $\theta$，模态干扰不可避免。

**三种模态隔离变体**（Fig. 2）：

- **LoRA**：在自注意力层注入低秩适配矩阵，以极小参数量实现模态偏置，但前馈层仍共享。
- **MoE**：为运动模态复制独立的前馈网络（FFN），以专家混合形式路由运动令牌，注意力层仍共享。
- **MIS（模态隔离架构）**：为运动模态复制完整的Transformer块，运动和文本以完全独立的参数通过各自塔：
  $$\begin{array}{ll}
  h &= x + \mathrm{MHSA}(\mathrm{LN}(x, \theta_{\mathrm{ln1}}^{\mathrm{u}}); \theta_{\mathrm{attn}}^{\mathrm{u}}), \\
  x' &= h + \mathrm{FFN}(\mathrm{LN}(x, \theta_{\mathrm{ln2}}^{\mathrm{u}}); \theta_{\mathrm{ffn}}^{\mathrm{u}}), \quad \mathrm{u} \in \{\mathrm{m}, \mathrm{t}\}
  \end{array} \tag{19}$$
  其中 $\mathrm{u}=\mathrm{m}$ 表示运动塔参数，$\mathrm{u}=\mathrm{t}$ 表示文本塔参数。双塔在顶层通过交叉注意力或简单拼接进行融合。

> **消融证据**：Table 11表明，MoE变体在InterX交互式文本到运动任务上的Top-1准确率（71.9）比Prototype基线（63.8）高出约8个百分点，MIS进一步带来增益，验证了模态隔离对缓解模态干扰的有效性。

### 3.4 三阶段训练流水线

MotionVerse采用三阶段渐进训练策略：

1. **阶段一：令牌器训练**。仅训练RVQ-VAE，优化目标为公式(4)的重建损失和承诺损失，使运动标记器获得高质量的多流离散表示。
2. **阶段二：运动-文本对齐预训练**。冻结令牌器，在大规模运动-文本对上训练LLM骨干和Motion-Fusion模块，使模型学习运动令牌与自然语言的联合分布。
3. **阶段三：多任务指令微调**。引入任务特定的运动塔（Task-specific Motion Tower, TMT），在多种运动任务（生成、理解、编辑、预测、反应等）的指令数据上进行微调，以统一格式处理所有任务。

> **消融证据**：Tables 12-14显示，移除任务特定运动塔（wo-TMT）导致各子任务性能一致下降，尤其在运动反应和编辑任务上退化明显，表明TMT有效缓解了多任务间的干扰。

![[assets/figures/papers/paper_list_l1801_MotionVerse_A_Unified_Multimodal_Framework_for_Motion_Comprehension_Gene/figures/001_Figure_1.jpg]]
*Figure 1: Multi-stream motion token modeling strategies. We illustrate 3 quantization levels as an example. Here, mlt denotes the t-th token in the l-th motion stream. These motion tokens can be flattened or interleaved in various ways, resulting in a new sequence with either 1 or 4 parallel streams and steps s1, s2, . . . , sm. The special token −1 denotes empty positions within the pattern*

![[assets/figures/papers/paper_list_l1801_MotionVerse_A_Unified_Multimodal_Framework_for_Motion_Comprehension_Gene/figures/002_Figure_2.jpg]]
*Figure 2: Potential architecture variants of the Motion-Fusion module. (a) Prototype: Direct fine-tuning of a pretrained LLM. (b) Low-Rank Adaptation (LoRA): injecting low-rank matrices into multi-head self-attention layers. (c) Mixture-of-Experts (MoE): Duplicating each Feed-Forward Network (FFN) for the motion modality. (d) Modality-Isolated Architecture (MIS): Duplicating each transformer block for the motion modality*

## 实验与关键发现

### 核心实验设计

MotionVerse 在 **8 类运动任务** 上进行统一评估，覆盖单人/双人场景的理解、生成与编辑。实验采用三阶段训练流水线：令牌器训练、运动-文本对齐预训练、多任务指令微调。评估时为每个子任务使用专门训练的检索模型，保证公平性（fairness notes）。主要对比基线包括：**MoMask**（Guo et al., CVPR 2024）用于文本到运动生成，**MotionGPT**（Jiang et al., NeurIPS 2023）作为统一运动语言模型，**InterGen**（Liang et al., IJCV 2024）用于交互式生成，**ReGenNet**（Xu et al., CVPR 2024）用于运动反应生成，**TMED**（Athanasiou et al., SIGGRAPH 2024）用于运动编辑。

### 主实验结果

**文本到运动生成（T2M）。** 在 MotionX 数据集上，MotionVerse 取得 FID 0.010（Table 3），与专用模型 MoMask 接近但略高；R-Precision Top-1 达到 79.5，处于领先水平。这体现了统一架构在多任务训练下仍能保持有竞争力的生成质量。

**交互式文本到运动生成（I-T2M）。** 在 InterX 数据集上，MotionVerse 的 R-Precision Top-1 达到 70.2，显著优于 TM2T 的 66.0（+4.2，Table 4）。在 InterHuman 数据集上同样保持优势，验证了多流令牌表示对双人交互建模的有效性。

**运动到文本（M2T）。** 在 MotionX 数据集上，BLEU@4 达到 15.8（Table 5），为所有对比方法中最优。交互式运动到文本（I-M2T）在 InterHuman 和 InterX 上也取得领先结果，表明模态隔离架构有效保留了运动语义信息。

**运动反应生成（React）。** 在 InterHuman 数据集上，Top-1 R-Precision 达到 50.3（Table 7），优于 MDM 和 ReGenNet。延迟并行建模策略使模型能同时捕获单人运动时序和双人间交互依赖。

**运动预测与插值（M2M）。** 在 MotionX、InterHuman、InterX 三个数据集上均取得有竞争力的结果（Table 6），证明统一框架对运动补全任务的泛化能力。

**运动编辑（Edit）。** 在 MotionFix 数据集上表现优异（Table 8），任务特定运动塔（TMT）有效缓解了编辑任务与其他任务间的干扰。

### 消融实验：关键设计的因果验证

#### 残差向量量化（RVQ）的有效性

Table 9 对比了 RVQ 与普通 VQ 在运动重建和生成上的表现。当量化层数 L=6 时，RVQ 在 T2M 任务上 FID 从 VQ 的 0.036 降至 0.012，Top-1 R-Precision 从 25.3 升至 41.7。这直接验证了 **核心洞察**：多流离散表示能更完整地保留运动细节，避免单层 VQ 的信息丢失瓶颈。随着 L 从 2 增至 6，重建质量和生成质量均单调提升，但 L=8 时收益递减。

![[assets/figures/papers/paper_list_l1801_MotionVerse_A_Unified_Multimodal_Framework_for_Motion_Comprehension_Gene/figures/016_Table_9.jpg]]
*Table 9: Reconstruction and Generation Performance of Residual Vector Quantization (RVQ) vs. Vanilla Vector Quantization (VQ) on MotionX. We evaluate the Generation Performance on the single-task Text-to-Motion (T2M). L denotes the number of quantization layers in RVQ, and MPJPE is reported in millimeters*

#### 多流令牌建模策略对比

Table 10 系统比较了三种建模策略。延迟并行（Delay Parallel）在 T2M 任务上 Top-1 达到 79.5，远高于并行策略的 75.2 和扁平化策略的 68.9；MM-Dist 也显著降低。这证实了 **因果机制**：延迟并行能同时捕获流内时序依赖和流间残差依赖，而并行策略忽略了流间关系，扁平化策略则破坏了流内时序结构。Table 2 进一步从理论复杂度角度说明，延迟并行在保持 $O(T^2)$ 注意力的同时实现了流间依赖建模，优于扁平化的 $O((LT)^2)$。

![[assets/figures/papers/paper_list_l1801_MotionVerse_A_Unified_Multimodal_Framework_for_Motion_Comprehension_Gene/figures/017_Table_10.jpg]]
*Table 10: Ablation study on multi-stream motion token modeling strategies, evaluating all models after training on the single Text-to-Motion task on MotionX*

#### 模态隔离架构消融

Table 11 对比了 Motion-Fusion 模块的四种变体。在多任务训练下，**MoE 变体**在 InterX T2M 的 Top-1 上达到 71.9，比共享参数的 Prototype 架构（63.8）高出约 8 个百分点。MIS（完全隔离）变体进一步将 Top-1 提升至 72.3。这直接验证了 **核心洞察**：共享参数架构引发严重的模态干扰，而模态隔离设计能有效化解运动与文本表示间的冲突。值得注意的是，单任务 Prototype 在 T2M 上表现尚可（Top-1 76.5），但多任务训练后性能骤降，进一步证实了模态干扰的存在。

![[assets/figures/papers/paper_list_l1801_MotionVerse_A_Unified_Multimodal_Framework_for_Motion_Comprehension_Gene/figures/015_Table_11.jpg]]
*Table 11: Ablation study on architectural variants for modality-specific towers in Motion-Fusion. The Single-Task adopts the Prototype architecture and is trained solely on the Text-to-Motion (T2M) task. Other models are trained on all tasks. All models are evaluated on T2M task*

#### 任务特定运动塔（TMT）的作用

Tables 12-14 消融了 TMT 组件。移除 TMT（wo-TMT）后，各子任务性能一致下降：在运动反应任务上 FID 从 0.296 升至 0.351，编辑任务上 FID 从 0.208 升至 0.254（Table 14）。这表明 TMT 通过为每个任务提供独立的运动塔参数，有效缓解了多任务指令微调中的任务间干扰。

#### LLM 主干规模影响

Tables 12-14 同时对比了 T5-Base 和 T5-Large 作为 LLM 主干。T5-Large 相比 T5-Base 未带来显著性能增益，部分指标甚至略有下降。这被论文列为 **已知局限**：当前任务规模可能已使 T5-Base 饱和，更大的语言模型在该设定下收益有限。

### 失败模式与局限性

1. **专用模型在单一指标上的优势。** 在 T2M 的 FID 指标上，MotionVerse（0.010）略逊于 MoMask（0.008）。这是统一架构多任务学习的固有权衡：通用性提升可能以牺牲单任务极致性能为代价。
2. **延迟并行的序列长度依赖。** 延迟并行策略的效果依赖于 $L \ll T$ 的假设（即量化层数远小于序列长度）。对于极短运动序列，流间延迟带来的优势减小，扁平化或并行策略可能更合适。
3. **LLM 规模扩展瓶颈。** T5-Large 未带来显著增益，暗示当前训练数据规模和任务复杂度可能不足以驱动更大模型的能力涌现。
4. **评估场景局限。** 所有实验基于现有公开数据集（MotionX、InterHuman、InterX、MotionFix），未在真实交互场景或机器人应用中验证。

### 重要图表结论

- **Figure 1** 与 **Table 2** 联合说明了三种建模策略的理论特性：延迟并行是唯一同时具备流内建模、流间建模和 $O(T^2)$ 复杂度的方案。
- **Figure 2** 展示的四种 Motion-Fusion 变体中，MIS 提供最强的模态隔离，LoRA 在参数效率与性能间取得折中。
- **Figure 3** 的架构全景图揭示了从 RVQ-VAE 令牌化到延迟并行 LLM 再到双塔输出的完整数据流，是理解整个框架的关键。
- **Table 1** 的任务覆盖对比表明，MotionVerse 是首个同时支持 8 类单人/双人运动任务的统一框架，而此前方法最多覆盖 3-4 类。

## 定位与知识库关联

### 核心瓶颈与因果机制

现有运动理解与生成方法面临两个结构性瓶颈。其一，**单人运动与交互式运动长期被分而治之**：文本到运动生成（如 **MoMask** Guo et al., CVPR 2024）、运动反应生成（如 **ReGenNet** Xu et al., CVPR 2024）、运动编辑（如 **TMED** Athanasiou et al., SIGGRAPH 2024）等任务各自发展专用架构，缺乏统一框架。其二，**早期统一尝试受限于信息丢失与模态干扰**：**MotionGPT**（Jiang et al., NeurIPS 2023）虽率先将运动语言模型化，但其采用的单层向量量化（VQ）造成细粒度运动动态的信息丢失，且共享参数的Transformer架构导致文本与运动模态在联合训练时产生严重干扰。

MotionVerse的因果调控旋钮可归结为三点。**残差向量量化（RVQ）** 将连续运动序列转化为多层离散令牌流，通过逐层量化残差的方式保留从粗到细的运动层次结构，从根本上缓解了VQ的信息瓶颈。**延迟并行建模策略**在保持线性注意力复杂度的前提下，通过在残差流之间引入时间偏移，使LLM能够自回归地同时捕获流内时序依赖和流间层次依赖。**模态隔离的双塔架构**（Motion-Fusion模块）为运动和文本分别分配独立的Transformer参数，从架构层面消除模态干扰，使多任务联合训练成为可能。

### 方法谱系中的坐标定位

MotionVerse处于“统一运动基础模型”这一新兴技术路线的关键节点，其上下游关系如下：

| 维度 | 上游基础 | MotionVerse贡献 | 下游延伸方向 |
|------|----------|-----------------|-------------|
| **运动令牌化** | VQ-VAE单层量化（MotionGPT） | RVQ-VAE多层残差量化（L=6），多流令牌 | 可推广至面部动画、手势等其他时序数据的统一离散化 |
| **多流建模** | 扁平化序列或并行独立预测 | 延迟并行（Delay Parallel），同时捕获流内与流间依赖 | 自适应延迟量调整；超长序列的分块延迟建模 |
| **模态融合** | 共享Transformer全参数微调（Prototype） | 模态隔离架构（MIS变体），运动/文本独立参数 | 扩展至音频、场景上下文等更多模态的隔离融合 |
| **任务统一** | 单任务专用模型（MDM, InterGen, TMED等） | 三阶段训练+任务特定运动塔（TMT），统一8类任务 | 真正的“任意到运动”（any-to-motion）生成 |

具体而言，**MDM**（Tevet et al., arXiv 2022）以扩散模型独立处理文本到运动生成，**InterGen**（Liang et al., IJCV 2024）专攻双人交互运动生成，二者均无法跨任务迁移。MotionVerse通过统一的运动令牌语言和LLM骨干，首次在单一框架内覆盖单人/双人的理解、生成、预测、插值、反应和编辑共八类任务（Table 1），在方法论层面实现了从“任务专用”到“基础模型”的范式跃迁。

### 适用边界与局限

**架构假设的边界**。延迟并行策略的有效性依赖于量化层数L远小于运动序列长度T的假设（Table 2中复杂度为$\mathcal{O}(T^2)$，与L无关）。当面对极短运动序列（T接近L）时，延迟机制带来的流间依赖增益将被削弱，该点需在特定应用场景下手动验证。

**统一性与专精性的权衡**。尽管MotionVerse在绝大多数任务上取得最优或次优结果，但在文本到运动生成的FID指标上（Table 3，FID=0.010），仍略逊于专门优化的**MoMask**。这反映了基础模型路线的固有张力：多任务联合训练带来的任务间迁移收益，需以单一指标上的微小退让为代价。论文同时指出，T5-Large相比T5-Base未带来显著性能增益，暗示当前任务规模可能已触及该架构的收益天花板。

**评估生态的局限**。所有定量评估基于现有公开数据集（MotionX、InterHuman、InterX、MotionFix），未在真实交互场景或机器人应用中验证。交互式任务的评估依赖专门训练的检索模型，虽保证了公平性，但检索模型的偏差可能影响结论的泛化性。

### 开放问题

1. **延迟并行的自适应机制**：当前延迟量固定为$l-1$步，能否根据运动序列的局部动态复杂度自适应调整延迟量，在流间依赖与计算成本之间实现更细粒度的权衡？

2. **模态干扰的量化度量**：模态隔离架构对干扰的缓解目前仅通过下游任务性能间接验证（Table 11中MoE/MIS相比Prototype提升约6% Top-1准确率）。能否引入梯度冲突度量或互信息分析，从优化动力学层面直接量化模态干扰的减轻程度？

3. **多模态扩展路径**：论文提出的多流令牌化和模态隔离架构能否平滑扩展至音频、场景上下文等模态，实现“任意到运动”生成？新增模态是否需要独立的令牌化器和隔离塔，还是可以共享部分表示空间？

4. **超长序列扩展性**：当生成时间跨度极大的运动序列时，延迟并行策略的线性注意力假设是否仍然成立？是否需要引入记忆压缩或分块自回归机制？

5. **三阶段训练的最优配比**：令牌器训练、对齐预训练、指令微调三个阶段的数据比例和任务采样策略是否存在最优设计？论文未对此进行系统消融，该方向可能蕴含进一步的性能提升空间。

## 原文 PDF

![[paperPDFs/PAMI_2025/MotionVerse_A_Unified_Multimodal_Framework_for_Motion_Comprehension_Generation_and_Editing.pdf]]
