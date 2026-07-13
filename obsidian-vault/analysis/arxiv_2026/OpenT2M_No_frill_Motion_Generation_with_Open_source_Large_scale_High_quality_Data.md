---
title: "OpenT2M: No-frill Motion Generation with Open-source, Large-scale, High-quality Data"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/OpenT2M_No_frill_Motion_Generation_with_Open_source_Large_scale_High_quality_Data.pdf
project_link: null
code_link: null
aliases:
- M2PMTAL
- OpenT2M
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 构建大规模、物理可行的开源运动数据集OpenT2M（百万级序列，包含长时序数据与秒级标注），并设计2D-PRQ运动分词器，通过身体分块与2D卷积捕捉时空依赖，显著提升数据编码效率和模型泛化能力。
primary_logic: 大规模、高质量的运动数据是T2M模型泛化性的决定性因素；合理设计运动分词器（如利用2D卷积建模身体部位间的时空依赖性）能够有效释放大数据潜力。同时，消除基准数据泄漏是获得可靠性能评估的前提。
claims:
- HumanML3D和Motion-X验证集中分别有10.62%和16.97%的文本描述与训练集完全一致，清理后模型性能大幅下降，表明现有基准评估不准。
- OpenT2M包含100万条运动序列、超过2800小时数据，平均长度10.1秒，支持物理可行性验证和长时序，规模和多样性远超先前数据集。
- 在2D-PRQ运动分词器下，OpenT2M零样本泛化性能显著优于HumanML3D和Motion-X训练的模型（如表2所示），证明数据规模与质量是关键。
- 2D-PRQ在运动重建任务（Motion-X MPJPE 54.493 vs PRQ 73.989）和零样本标记器迁移（HumanML3D MPJPE 77.695 vs VQ-VAE 237.702）上均显著优于此前方法。
---

# OpenT2M: No-frill Motion Generation with Open-source, Large-scale, High-quality Data

> [!tip] 核心洞察
> 大规模、高质量的运动数据是T2M模型泛化性的决定性因素；合理设计运动分词器（如利用2D卷积建模身体部位间的时空依赖性）能够有效释放大数据潜力。同时，消除基准数据泄漏是获得可靠性能评估的前提。

| 字段 | 内容 |
|------|------|
| 中文题名 | OpenT2M：基于开源大规模高质量数据的无冗余运动生成 |
| 英文题名 | OpenT2M: No-frill Motion Generation with Open-source, Large-scale, High-quality Data |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.18623v1) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MonoFrill (2D-PRQ motion tokenizer + autoregressive LLM) |
| Dataset | Motion-X, HumanML3D |

> [!tip] 效果简介
> - Motion-X (运动重建) 上，MPJPE ↓ 54.493 (2D-PRQ_4) vs 73.989 (PRQ_4) (-19.496 (-26.3%))。
> - HumanML3D (零样本标记器迁移) 上，MPJPE ↓ 77.695 (2D-PRQ_4) vs 237.702 (VQ-VAE) (-160.007 (-67.3%))。
> - HumanML3D (文本精炼) 上，R@1 ↑ 0.533 (with refinement) vs 0.520 (without refinement) (+0.013)。

## 概要

**问题瓶颈**：当前文本到运动（Text-to-Motion, T2M）生成模型的泛化能力普遍不足，其根本原因并非模型架构复杂度的欠缺，而是训练数据的规模与质量存在根本性缺陷。主流基准数据集（如HumanML3D、Motion-X）规模过小且多样性有限，更严重的是，其训练集与验证集之间存在显著的文本重叠——HumanML3D中10.62%、Motion-X中16.97%的验证文本与训练集完全一致（Figure 1）。这种数据泄漏导致现有性能指标虚高，掩盖了模型在分布外数据上泛化能力的真实水平：清理重叠后，模型性能大幅下降。

**核心洞察**：大规模、高质量的运动数据是决定T2M模型泛化性的核心因素；同时，合理设计运动分词器以有效捕捉身体部位间的时空依赖关系，是释放大数据潜力的关键前提。

**方法与定位**：本文提出了**MonoFrill**，一个极简的自回归离散T2M框架，包含两个核心组件：

1. **OpenT2M数据集**：当前最大规模的开源人体运动数据集，包含100万条运动序列、超过2800小时数据，平均序列长度10.1秒。数据经过物理可行性验证（基于强化学习的物理仿真过滤）与多粒度质量筛选，并采用两阶段秒级细粒度文本标注管道（Figure 2），在规模、时长、物理可信度和标注精度上全面超越此前数据集（Table 1）。

2. **2D-PRQ运动分词器**：将人体划分为五个部位，利用2D卷积同时捕捉空间（部位间）和时间维度的依赖关系，并采用残差量化（Residual Quantization）生成离散部位-时间二维标记。相较于此前基于1D卷积的VQ-VAE（Zhang et al., CVPR 2023）和整体残差量化PRQ，2D-PRQ在运动重建和零样本泛化上均展现出显著优势。

在方法谱系中，MonoFrill继承了自回归语言模型驱动的运动生成范式，但通过数据与分词器的双重革新，跳出了对复杂模型设计的依赖，以“无冗余”（no-frill）路线实现了竞争力的突破。

**主要结果**：

- **数据规模驱动泛化**：在OpenT2M上训练的模型，零样本泛化性能显著优于使用HumanML3D或Motion-X训练的模型（Table 2）。
- **预训练增益显著**：以LLaMA3-8B为骨干，OpenT2M预训练使HumanML3D微调后的FID从0.546降至0.238（↓56.4%，Table 3），验证了大规模预训练的决定性作用。
- **分词器性能领先**：2D-PRQ在Motion-X上的运动重建MPJPE达54.493，较PRQ（73.989）降低26.3%（Table 6）；在HumanML3D上的零样本标记器迁移MPJPE为77.695，远优于VQ-VAE的237.702（↓67.3%，Table 8）。
- **文本精炼有效**：通过Gemini-2.5对原始描述进行运动无关内容滤除后，HumanML3D上的文本-运动对齐度R@1从0.520提升至0.533（Table 5）。

**局限与开放问题**：基于视频提取的原始运动可能残留少量伪影；文本精炼提示设计的具体影响机制、最优身体分块方案、以及更大规模LLM收益递减的破解策略，仍有待进一步探索。



文本到运动（Text-to-Motion, T2M）生成旨在根据自然语言描述合成逼真的三维人体运动序列，在动画制作、虚拟人交互、游戏开发等领域具有广泛应用前景。近年来，基于自回归模型和扩散模型的方法在该任务上取得了显著进展，但现有工作的性能评估和泛化能力仍面临根本性挑战。

### 数据瓶颈：规模、多样性与物理可行性

当前T2M模型的训练严重依赖有限的运动捕捉数据集。主流基准如**HumanML3D**仅包含约15,000条序列，**Motion-X**虽扩展至约81,000条，但其运动来源多为视频提取，缺乏物理可行性验证。这一数据瓶颈直接导致模型泛化能力不足——在训练分布之外的新文本输入上，生成质量急剧下降。

OpenT2M数据集（Table 1）的统计对比揭示了这一缺口的量级：该数据集包含**100万条运动序列**、超过**2,800小时**数据，平均序列长度**10.1秒**，同时支持物理可行性验证和长时序运动生成。相较之下，此前最大的开源数据集在规模和功能覆盖上均存在数量级差距。

### 基准污染：被掩盖的泛化危机

更隐蔽的问题在于现有基准的**数据泄漏**。如Figure 1所示，对HumanML3D和Motion-X的训练-验证集文本嵌入进行可视化分析后发现，HumanML3D验证集中有**10.62%** 的文本描述与训练集完全一致，Motion-X的这一比例高达**16.97%**。这种训练-验证集重叠意味着模型在验证集上的“高性能”很大程度上源于对训练文本的记忆，而非真正的语义理解与泛化。

当对基准进行重新划分、消除重叠后，现有方法的性能出现**大幅下降**。这一发现从根本上动摇了此前T2M研究中的性能评估可信度，也揭示了当前模型在面对分布外（Out-of-Distribution, OOD）数据时泛化能力的真实局限。

### 方法缺口：运动分词器的时空建模不足

在模型架构层面，现有运动分词器普遍采用**1D卷积**对整体身体特征进行编码（如**VQ-VAE**在T2M-GPT中的应用，Zhang et al., CVPR 2023），或对整体运动进行残差量化。这种设计忽略了人体运动的本质结构——不同身体部位之间存在复杂的时空依赖关系，单一维度的编码难以有效捕捉这种层次化特征。运动重建误差居高不下（如VQ-VAE在HumanML3D上的零样本迁移MPJPE高达237.702），直接制约了下游生成任务的质量上限。

### 本文动机

综上所述，T2M领域面临三重核心挑战：
1. **数据层面**：缺乏大规模、物理可行、标注精细的开源运动数据集；
2. **评估层面**：现有基准存在严重数据泄漏，性能指标虚高，无法反映真实泛化能力；
3. **方法层面**：运动分词器的时空建模能力不足，限制了数据潜力的释放。

本文的核心动机在于：通过构建**OpenT2M**——一个百万级、物理可行的开源运动数据集，并设计**2D-PRQ**运动分词器以充分建模身体部位间的时空依赖，从根本上解决上述瓶颈，推动T2M模型向真正的零样本泛化迈进。



## 核心方法与创新机理

本工作围绕“数据是泛化瓶颈”这一核心诊断，从数据与分词器两个维度对文本到运动（T2M）生成进行了系统性改造。其关键创新可归纳为三个 **changed slots**。

### 1. 运动数据：从“小样本+泄漏”到“百万级+物理可行”

现有T2M模型长期依赖 **HumanML3D**（约15K序列）或 **Motion-X**（约81K序列）进行训练与评估。本文首先揭示了一个被忽视的基准缺陷：HumanML3D与Motion-X的验证集中分别有 **10.62%** 和 **16.97%** 的文本描述与训练集完全一致（Figure 1），这种训练-验证集文字重叠导致性能指标虚高，掩盖了模型真实的泛化能力不足。清理重叠后，现有模型性能大幅下降，暴露出严重的数据泄漏问题。

为解决规模与多样性的根本瓶颈，作者构建了 **OpenT2M** 数据集，包含 **100万条** 运动序列、超过 **2800小时** 数据，平均序列长度 **10.1秒**，且支持物理可行性验证与长时序生成（Table 1）。与先前数据集相比，OpenT2M在规模、时长和物理可信度上均形成数量级优势。

在文本标注层面，OpenT2M采用 **两阶段秒级细粒度标注管道**：先用Gemini-2.5-pro对运动视频逐秒生成时序对齐的描述，再合成为连贯的语义丰富摘要。后续训练中，还引入 **文本精炼模块**（Text Refinement），通过Gemini-2.5将原始粗描述转化为去除运动无关细节的精确用户指令（Figure 7），进一步提升了文本-运动对齐度。

### 2. 运动分词器：从“1D整体编码”到“2D身体分块残差量化”

此前主流运动分词器采用 **VQ-VAE**（1D卷积，整体身体编码；Zhang et al., CVPR 2023）或 **PRQ**（整体残差量化），将运动序列压缩为一维离散标记序列，忽略了人体各部位之间的时空依赖关系。

本文提出的 **2D-PRQ** 运动分词器进行了两个关键设计变更：

- **身体分块**：将人体划分为5个部位，对每个部位独立编码，形成“部位×时间”的二维标记网格。
- **2D卷积建模**：在编码器-解码器中采用2D卷积，同时捕捉空间维度（部位间依赖）和时间维度的关联，从而更高效地建模运动动力学。

该设计在运动重建任务上展现出显著优势：在Motion-X基准上，2D-PRQ的MPJPE达到 **54.493**，较PRQ（73.989）降低 **26.3%**（Table 6）。更关键的是零样本泛化能力：在HumanML3D上做跨数据集标记器迁移时，2D-PRQ的MPJPE为 **77.695**，而VQ-VAE高达 **237.702**，降幅达 **67.3%**（Table 8）。这验证了身体分块与2D卷积设计在释放大数据潜力方面的因果作用。

### 3. 训练范式：大规模预训练释放数据红利

基于上述数据与分词器，作者设计了简洁的两阶段训练流程：

1. **预训练阶段**：在OpenT2M上训练自回归LLM（GPT2/LlaMA系列），以文本为条件预测2D-PRQ运动标记序列，损失函数为负对数似然：
   $$\mathcal{L}(\Theta) = -\sum_{j=1}^{L} \log P_{\Theta}(y_j | desc, \hat{y}_{1:j-1})$$

2. **微调阶段**：在目标基准（如HumanML3D）上仅进行有限步数微调（50个epoch），避免过拟合，使预训练增益明确可测。

消融实验表明，OpenT2M预训练带来一致且显著的提升：以LlaMA3-8B为例，预训练后FID从0.546降至 **0.238**（降低 **56.4%**），R@1从0.503提升至0.518（Table 3）。在零样本泛化基准OpenT2M zero上，以OpenT2M训练的模型全面超越以HumanML3D或Motion-X训练的模型（Table 2），直接证明了数据规模与质量是泛化能力的决定性因素。

**证据强度**：以上三个changed slots均有强证据支撑（置信度0.95–0.98），来自多表消融与跨基准对比。需注意的局限是，基于视频提取的运动虽经物理可行性验证（通过率>63%），仍可能残留少量运动伪影，对极高精度任务或构成影响。



OpenT2M 的整体框架围绕一个核心洞察构建：**当前文本到运动（T2M）模型的泛化瓶颈根源于数据规模与质量的双重不足，而非模型架构的复杂性**。为此，作者提出了一套“无冗余”（no-frill）的技术方案，由两条并行但深度耦合的流水线组成：大规模高质量运动-文本数据集 **OpenT2M** 的构建，以及简洁的自回归运动生成模型 **MonoFrill**。

### 数据与模型的双轮驱动

整个系统的运作逻辑遵循“数据先行、模型跟随”的范式。首先，通过一套多阶段数据整理管道（Figure 2）从互联网视频中提取并验证百万级运动序列，并配以秒级细粒度文本标注，形成 OpenT2M 数据集。随后，MonoFrill 模型在该数据集上进行预训练，习得鲁棒的文本-运动对齐能力，再在下游基准上微调，实现强泛化性能。

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2603_18623v1/figures/002_Figure_2.jpg]]
*Figure 2: Data Curation pipeline. (a) We adopt a two-stage pipeline, including physically feasible validation and multi-granularity filter. (b) We adapt the interpolation-based method for motion curation and introduce an RL-policy for refinement. (c) For text annotation, we generate temporally aligned labels for each second of video, using them to synthesize a precise, semantic-rich description*

### MonoFrill 模型流水线

MonoFrill 的架构极简，由三个核心模块串联构成（Figure 3）：

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2603_18623v1/figures/004_Figure_3.jpg]]
*Figure 3: Model Overview. We propose an extendable, autoregressive (AR) and discrete T2M model with no frills. (left) Our core design 2D-PRQ divides the entire body into five parts, encoding and quantizing motion into a sequence of discrete part-level tokens. (right) The AR model takes text as input and predicts part-level motion tokens. We call this model “MonoFrill” to show its simplicity*

1. **2D-PRQ 运动分词器（Encoder + Quantizer）**：将原始运动序列编码为离散的部位-时间二维标记。其关键设计是将人体划分为 5 个部位，利用 2D 卷积同时捕捉空间（部位间）和时间（帧间）依赖关系，再通过残差量化（Residual Quantization）将连续特征压缩为离散标记序列。
2. **LLM 骨架（GPT2/LLaMA 系列）**：以自回归方式工作，接收文本描述作为条件输入，逐 token 预测运动标记序列。训练目标为标准的负对数似然损失：
   $$\mathcal{L}(\Theta) = -\sum_{j=1}^{L} \log P_{\Theta}(y_j | desc, \hat{y}_{1:j-1})$$
3. **2D-PRQ 解码器**：将 LLM 预测的离散标记序列解码回连续运动表示，完成从文本到运动的生成闭环。

### 数据整理管道

OpenT2M 的数据生产流程（Figure 2）包含三个关键阶段：

- **物理可行性验证与多粒度过滤**：从网络视频中提取 2D 关键点后，首先施加质量准则（最低关键点数、人体边界框比例下界、最短时序长度）。随后引入基于强化学习的鲁棒性策略 $\pi_{\text{refine}}$，在 AMASS 上训练后用于追踪和精修运动，确保符合物理规律——超过 63% 的提取运动通过了该验证。
- **秒级文本标注**：采用 Gemini-2.5-pro 进行两阶段标注——首先生成逐秒的时间对齐描述，再综合为语义丰富的连贯摘要。
- **文本精炼**：在训练前，利用 Gemini-2.5 将原始标注转化为精确的用户指令，移除与运动无关的细节（如外观、背景描述），提升文本-运动对齐度。

### 输入输出流

- **训练阶段**：输入为运动序列及其精炼文本描述。运动序列经 2D-PRQ 编码器编码并量化为离散标记，文本经 LLM 的文本编码器处理为条件表示。LLM 以文本为条件，自回归地预测运动标记，通过最小化负对数似然进行优化。2D-PRQ 分词器则通过包含整体 L1 损失、部位级 L1 损失和承诺损失的重构目标端到端训练：
  $$\mathcal{L} = ||\boldsymbol{m} - \hat{\boldsymbol{m}}||_1 + \sum_{i=0}^{p} ||\boldsymbol{m}_i - \hat{\boldsymbol{m}}_i||_1 + \beta \sum_{k=1}^{K} \sum_{i=1}^{p} ||\boldsymbol{r}_i^k - sg[b_i^k]||_2^2$$
- **推理阶段**：输入为用户文本指令，LLM 自回归生成运动标记序列，再由 2D-PRQ 解码器解码为连续运动，输出可直接用于动画驱动的运动数据。



### 2D-PRQ 运动分词器

MonoFrill 的核心设计是 **2D-PRQ（2D Part-wise Residual Quantization）** 运动分词器，其关键创新在于将人体运动建模从整体序列编码转变为**分部位、时空联合**的二维离散表示。

**身体分块策略**：2D-PRQ 将人体骨骼划分为 5 个部位（`p=5`），每个部位的运动特征被独立编码。这种设计使得模型能够捕捉不同身体部位之间的协调关系，而非将整个人体视为单一整体。

**2D 卷积编码**：与先前方法采用的 1D 卷积（如 **VQ-VAE**，Zhang et al., CVPR 2023）不同，2D-PRQ 使用 2D 卷积架构，在空间维度（身体部位）和时间维度上同时建模依赖关系。这一设计的核心优势在于能够捕捉**跨部位的时间协同模式**，例如行走时手臂与腿部的节律性配合。

**残差量化机制**：编码后的连续特征通过残差量化（Residual Quantization, RQ）转换为离散标记序列。采用共享码本 `C`，经过 `K` 层残差量化后，每个部位在每个时间步产生 `K` 个离散标记，最终形成 `(p, n, K)` 的二维标记表示，其中 `n` 为时间步数。

### 核心损失函数

**自回归运动生成损失**

训练 LLM Backbone（GPT2/LlaMA）进行文本条件运动生成时，采用标准的负对数似然损失：

$$\mathcal{L}(\Theta) = -\sum_{j=1}^{L} \log P_{\Theta}(y_j \mid desc, \hat{y}_{1:j-1})$$

其中：
- `desc` 为输入的文本描述
- `y_j` 为目标运动标记序列的第 `j` 个标记
- `\hat{y}_{1:j-1}` 为前 `j-1` 步已预测的标记序列
- `L` 为标记序列总长度

该损失函数驱动模型在给定文本条件下，自回归地最大化正确运动标记序列的似然。

**2D-PRQ 重构损失**

2D-PRQ 分词器的端到端训练采用复合重构损失：

$$\mathcal{L} = \|\boldsymbol{m} - \hat{\boldsymbol{m}}\|_1 + \sum_{i=0}^{p} \|\boldsymbol{m}_i - \hat{\boldsymbol{m}}_i\|_1 + \beta \sum_{k=1}^{K} \sum_{i=1}^{p} \|\boldsymbol{r}_i^k - sg[b_i^k]\|_2^2$$

损失由三项构成：
- **整体运动 L1 损失**：`\|\boldsymbol{m} - \hat{\boldsymbol{m}}\|_1`，约束完整人体运动 `\boldsymbol{m}` 与重建运动 `\hat{\boldsymbol{m}}` 的逐帧一致性
- **分部位 L1 损失**：`\sum_{i=0}^{p} \|\boldsymbol{m}_i - \hat{\boldsymbol{m}}_i\|_1`，分别约束每个身体部位 `i` 的运动重建精度
- **承诺损失**：`\beta \sum_{k=1}^{K} \sum_{i=1}^{p} \|\boldsymbol{r}_i^k - sg[b_i^k]\|_2^2`，强制编码器输出 `\boldsymbol{r}_i^k` 接近量化后的离散编码 `b_i^k`，其中 `sg[·]` 为停止梯度算子，`\beta` 为承诺损失权重

### MonoFrill 生成流程

整体生成管线由三个模块串联构成：

1. **2D-PRQ Encoder + Quantizer**：将原始运动序列编码为部位-时间二维离散标记
2. **LLM Backbone**：以文本描述为条件，自回归预测运动标记序列
3. **2D-PRQ Decoder**：将预测的离散标记解码为连续运动表示

训练采用两阶段范式：首先在 OpenT2M 大规模数据集上预训练，随后在目标基准（如 HumanML3D）上进行有限步数的微调（50 epoch），以避免过拟合并凸显预训练的泛化增益。



## 实验与关键发现

### 1. 实验设置与公平性保障

本文采用两阶段训练范式：首先在百万级OpenT2M数据集上进行预训练以建立鲁棒的文本-运动对齐，随后在下游基准（如HumanML3D）上进行有限步数的微调（仅50个epoch），以避免过拟合并凸显预训练增益。所有运动分词器统一采用时间降采样率α=4，确保重建与生成对比的公平性。评估指标涵盖运动重建质量（MPJPE）、生成质量（FID）、文本-运动对齐度（R@1、MMDist）及多样性（DIV）。

### 2. 数据规模与质量决定泛化能力

#### 2.1 零样本泛化：OpenT2M预训练的核心增益

Table 2展示了不同训练数据源在OpenT2M zero基准上的零样本泛化性能。以MonoFrill-2D-PRQ₄为统一分词器，当训练数据从HumanML3D（约15K序列）切换至Motion-X（约81K序列）再到OpenT2M（百万级序列）时，模型性能呈阶梯式跃升：OpenT2M训练的模型在R@1上达到0.240，FID降至1.475，MMDist降至4.281，显著优于HumanML3D和Motion-X训练的对应模型。这一结果直接验证了核心论断——**数据规模与多样性是T2M模型泛化性的决定性瓶颈**，而非模型架构的边际改进。

#### 2.2 运动指令微调：预训练带来一致且显著的提升

Table 3系统消融了OpenT2M预训练对不同LLM backbone在下游HumanML3D微调中的增益。以LLaMA3-8B为例，预训练后FID从0.546降至0.238（降幅56.4%），R@1从0.503提升至0.518。该增益在GPT2-medium、LLaMA2-7B等不同规模的backbone上一致存在，表明OpenT2M预训练学到的文本-运动对齐具有跨模型迁移能力。值得注意的是，所有微调均限制在50个epoch内，有效排除了过拟合对评估的干扰。

### 3. 运动分词器：2D-PRQ的架构优势

#### 3.1 运动重建精度对比

Table 6在Motion-X、HumanML3D和OpenT2M三个基准上对比了不同运动分词器的重建性能。2D-PRQ₄在Motion-X上取得MPJPE=54.493，相比PRQ₄的73.989降低26.3%；在HumanML3D上，2D-PRQ₄的MPJPE为77.695，而VQ-VAE高达237.702（降幅67.3%）。这一差距源于2D-PRQ的核心设计：将人体分为5个部位，利用2D卷积联合建模空间（部位间）与时间依赖性，而VQ-VAE的1D卷积只能处理整体身体特征的时序信息，PRQ虽采用残差量化但缺乏显式的空间建模。

#### 3.2 零样本分词器迁移能力

Table 8进一步考察了分词器的零样本泛化能力——即在未见数据集上的重建性能。2D-PRQ在所有量化层数配置下均显著优于VQ-VAE和PRQ。例如，在HumanML3D上，2D-PRQ₄的MPJPE为77.695，PRQ₄为89.410，VQ-VAE则高达237.702。这证明身体分块与2D卷积设计不仅提升了编码效率，更赋予分词器对分布外运动数据的鲁棒编码能力，为大规模预训练提供了可靠的基础。

### 4. 文本精炼与长时序消融

#### 4.1 文本精炼提升文本-运动对齐

Table 5在HumanML3D上消融了文本精炼模块的效果。使用Gemini-2.5对原始描述进行精炼（移除运动无关细节，转化为精确用户指令）后，R@1从0.520提升至0.533。增益虽看似微小，但考虑到HumanML3D本身规模有限且文本已相对干净，该提升仍验证了高质量文本标注对对齐度的正向作用。

#### 4.2 长时序运动生成

Table 4在OpenT2M long基准上进行了双因素消融：是否使用文本精炼、是否纳入长时序训练数据。同时启用两项的模型取得最优结果（FID=0.297，R@1=0.510），验证了长时序数据与精确文本标注对复杂运动生成的协同增益。该基准专门评估模型生成长时间运动序列的能力，OpenT2M中平均序列长度10.1秒为此提供了数据基础。

### 5. 模型规模与分词器的交互效应

Table 7在OpenT2M上考察了LLM backbone规模与分词器类型的组合效应。将backbone从GPT2-medium扩展到LLaMA2-7B带来显著生成质量提升，但进一步扩展到LLaMA3-8B时出现收益递减（R@1持平，FID改善有限）。同时，在相同backbone下，2D-PRQ始终优于PRQ，表明分词器质量与模型规模存在互补关系——更优的分词器可在一定程度上弥补模型容量的不足。

### 6. 数据泄漏：现有基准的可靠性危机

Figure 1揭示了HumanML3D和Motion-X中严重的数据泄漏问题：验证集中分别有10.62%和16.97%的文本描述与训练集完全一致。清理重叠数据后，现有方法在重新划分的基准上性能大幅下降，表明此前文献中的高指标部分源于训练-验证集信息泄漏，而非真实的泛化能力。这一发现从根本上动摇了以HumanML3D为主要基准的T2M评估体系的可靠性，也解释了为何在OpenT2M zero基准上未经预训练的模型表现极差。

### 7. 局限与待验证问题

尽管OpenT2M通过物理可行性验证（超过63%的提取运动通过RL-based filter），基于视频提取的原始运动仍可能残留少量运动伪影，对极高精度任务构成潜在影响。此外，以下问题需进一步验证：
- 文本精炼提示的具体设计机制及其对不同风格文本的鲁棒性；
- OpenT2M长时序基准的详细子集组成与拼接管道；
- LLaMA3-8B收益递减的深层原因，是否存在更优的模型架构或训练策略；
- 2D-PRQ固定5部位分块的合理性，是否存在更优的身体划分方案以适应更多样化的运动类型。

### 补充图表

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2603_18623v1/figures/001_Figure_1.jpg]]
*Figure 1: (Left) Visualization of text embeddings for the training and validation sets of HumanML3D and Motion-X. A substantial overlap between the splits indicates data leakage. To avoid this risk, we remove the overlap via data repartition (version denoted as ∗). (Right) However, we observe a drastic performance drop when experimenting on this repartitioned benchmark, which reveals the limited generalization capability of current methods when faced with out-of-domain data*

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2603_18623v1/figures/003_Table_1.jpg]]
*Table 1: Comparison with existing human motion datasets, where “#physically-feasible” refers to the motion sequences that comply with physical laws and “#long-horizon” denotes the dataset that can serve as a long-horizon benchmark*

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2603_18623v1/figures/005_Table_2.jpg]]
*Table 2: Comparison of zero-shot performance on OpenT2M zero using different datasets for training. Models trained on OpenT2M consistently present significant OOD improvements*

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2603_18623v1/figures/006_Table_3.jpg]]
*Table 3: Comparison of motion instruction tuning on HumanML3D. We apply a limited number of training steps to avoid overfitting. Models with #pretrain consistently achieve significant improvements across diverse #LLM backbones*

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2603_18623v1/figures/010_Table_6.jpg]]
*Table 6: Comparison of motion reconstruction on three benchmarks. Subscripts denote the number of quantization layers*

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2603_18623v1/figures/012_Table_8.jpg]]
*Table 8: Zero-shot comparison of motion tokenizers*

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2603_18623v1/figures/007_Table_4.jpg]]
*Table 4: Comparison on OpenT2M long, where “#text refinement” refers to converting raw texts into cleaned user commands, "#long-horizon" denotes incorporating long-horizon motion data into OpenT2M*

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2603_18623v1/figures/009_Table_5.jpg]]
*Table 5: Ablation of text refinement on HumanML3D*

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2603_18623v1/figures/011_Table_7.jpg]]
*Table 7: Comparison of T2M on OpenT2M under different model parameters and motion tokenizers*

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2603_18623v1/figures/016_Figure_7.jpg]]
*Figure 7: Prompt template for generating second-wise text annotations utilizing Gemini-2.5*



## 定位与知识库关联

### 1. 核心瓶颈与设计动机

当前文本到运动（T2M）模型泛化能力差的根本原因并非模型设计复杂度的不足，而在于**现有运动数据集规模小、多样性不足，且常用基准（如HumanML3D、Motion-X）存在严重的训练-验证集文字重叠问题**。具体而言，HumanML3D和Motion-X验证集中分别有10.62%和16.97%的文本描述与训练集完全一致（Figure 1），这种数据泄漏导致性能指标虚高，掩盖了模型在分布外数据上的真实泛化能力不足。清理重叠后的基准上模型性能大幅下降，直接验证了这一判断。

基于此，OpenT2M工作的核心洞察是：**大规模、高质量的运动数据是T2M模型泛化性的决定性因素；合理设计运动分词器（如利用2D卷积建模身体部位间的时空依赖性）能够有效释放大数据潜力**。

### 2. 方法谱系：与基线工作的关系

#### 2.1 运动分词器谱系

MonoFrill的核心组件2D-PRQ（2D Part-based Residual Quantization）位于运动分词器设计的演进脉络中：

- **VQ-VAE基线**（Zhang et al., CVPR 2023，T2M-GPT所用）：采用1D卷积对整个身体特征进行单一向量量化编码。该设计将运动序列视为一维时间信号，忽略了人体不同部位间的空间依赖关系，导致重建精度有限，且零样本泛化能力差——在HumanML3D零样本标记器迁移实验中，MPJPE高达237.702（Table 8）。

- **PRQ基线**（Residual Quantization）：在VQ基础上引入残差量化机制，通过多层量化逐步逼近原始特征，提升了编码精度。但PRQ仍采用整体身体特征的1D编码策略，未能显式建模部位间的时空依赖性。在Motion-X运动重建任务上，PRQ_4的MPJPE为73.989（Table 6）。

- **2D-PRQ（本文提出）**：将人体划分为5个部位（身体分块），利用2D卷积同时捕捉空间（部位间）和时间维度的依赖关系，并结合残差量化。这一设计在运动重建任务上显著优于此前方法：Motion-X上MPJPE降至54.493（较PRQ_4降低26.3%）；零样本标记器迁移实验中，HumanML3D上MPJPE仅77.695，较VQ-VAE降低67.3%（Table 8）。2D卷积对时空依赖的联合建模是性能跃升的关键机制。

#### 2.2 数据规模与训练范式谱系

在数据层面，OpenT2M将T2M训练从“小规模标注数据微调”推向了“大规模预训练+指令微调”的范式：

- **先前范式**：模型直接在HumanML3D（约15K序列）或Motion-X（约81K序列）上训练或微调，数据规模限制了模型对运动多样性的覆盖，且上述数据泄漏问题使评估不可靠。

- **OpenT2M预训练范式**：构建百万级序列的OpenT2M数据集（1M clips，2815.6小时，平均长度10.1秒），支持物理可行性验证和长时序数据（Table 1）。采用两阶段训练：先在OpenT2M上预训练建立鲁棒的文本-运动对齐，再在下游基准（如HumanML3D）上仅微调50个epoch以避免过拟合。消融实验表明，预训练带来一致且显著的提升：以LLaMA3-8B为例，预训练后HumanML3D上FID从0.546降至0.238（降低56.4%），R@1从0.503升至0.518（Table 3）。

#### 2.3 文本标注管道谱系

文本标注质量直接影响文本-运动对齐精度：

- **先前范式**：单阶段粗粒度视频描述，缺乏时序对齐，且常包含与运动无关的细节。

- **OpenT2M两阶段标注**：首先生成秒级时序对齐的细粒度描述，再合成为语义丰富的摘要（Figure 2c）。此外引入文本精炼模块（基于Gemini-2.5），移除运动无关细节，将原始描述转化为精确的用户指令。在HumanML3D上，文本精炼使R@1从0.520提升至0.533（Table 5），验证了文本质量对对齐度的直接影响。

### 3. 适用边界与局限

尽管OpenT2M在规模和质量上取得显著突破，以下边界条件需注意：

1. **运动伪影残留**：基于视频提取的原始运动尽管经过RL-based物理可行性验证（超过63%通过率），仍可能残留少量运动伪影，对极高精度任务（如运动风格迁移、精细手势生成）可能构成影响。

2. **身体分块方案的固定性**：2D-PRQ固定将身体分为5个部位，该方案在通用运动生成上有效，但未探索是否存在更优的分块策略以适应更多样化的运动类型（如舞蹈、体育动作中的非典型姿态）。

3. **LLM规模收益递减**：将LLM backbone从GPT2-medium扩展到LLaMA2-7B带来显著生成质量提升，但进一步扩展到LLaMA3-8B时增益递减（R@1持平，Table 7），表明当前架构下模型容量可能已接近数据所能支撑的上限。

### 4. 开放问题

1. **文本精炼机制**：Gemini-2.5在文本精炼中所使用的提示设计（如何滤除运动无关细节）的具体影响机制尚未充分分析，该环节的鲁棒性和可迁移性有待验证。

2. **长时序基准组成**：OpenT2M long基准的详细组成（各子集混合比例）及拼接管道细节有待进一步披露，这影响对长时序生成能力的精确归因。

3. **架构优化方向**：LLM规模从7B到8B出现收益递减，是否存在更优的模型架构（如改进的注意力机制）或训练策略可进一步突破当前瓶颈？

4. **分块方案泛化性**：固定5部位分块在极端姿态或非典型运动上的适用性如何？是否存在自适应分块或动态部位划分的可能性？



## 原文 PDF

![[paperPDFs/arxiv_2026/OpenT2M_No_frill_Motion_Generation_with_Open_source_Large_scale_High_quality_Data.pdf]]
