---
title: "MG-MotionLLM: A Unified Framework for Motion Comprehension and Generation across Multiple Granularities"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities.pdf
project_link: null
code_link: https://github.com/CVI-SZU/MG-MotionLLM
aliases:
- MM
- MG-MotionLLM
tags:
- CVPR_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "Granularity-Synergy Pre-training（多粒度协同预训练）阶段，通过引入时间边界定位、片段描述生成等28个跨粒度的辅助任务，逐步建立运动与细粒度文本的映射，并实现粗-细任务间的相互增强。"
primary_logic: "在统一语言模型框架中同时训练粗粒度（如整体动作描述）和细粒度（如身体部位随时间变化的详细脚本）的运动-语言任务，多任务间的知识迁移和互相促进能显著提升模型在各粒度上的理解和生成能力，使得单一模型即可胜任多种新老任务。"
claims:
- "直接使用粗粒度+详细文本指令调优时，运动生成Top-3检索精度从仅用粗粒度文本的77.3%下降至75.0%，说明长详细文本干扰了全局语义学习。"
- "采用Granularity-Synergy Pre-training后的模型在所有四个测试任务上均优于直接指令微调的模型，且在此基础上进行任务特定的指令微调可获得进一步显著提升（例如Text-to-Motion Top-3精度从0.767提升至0.802）。"
- "预训练阶段的所有28个任务都是必要的，缺失任何一个任务都会导致平均Top-1检索精度下降。"
- "HumanML3D (Text-to-Motion) 上 FID ↓ = 0.303"
---

# MG-MotionLLM: A Unified Framework for Motion Comprehension and Generation across Multiple Granularities

> [!tip] 核心洞察
> 在统一语言模型框架中同时训练粗粒度（如整体动作描述）和细粒度（如身体部位随时间变化的详细脚本）的运动-语言任务，多任务间的知识迁移和互相促进能显著提升模型在各粒度上的理解和生成能力，使得单一模型即可胜任多种新老任务。

| 字段 | 内容 |
|------|------|
| 中文题名 | MG-MotionLLM：面向多粒度运动理解与生成的统一框架 |
| 英文题名 | MG-MotionLLM: A Unified Framework for Motion Comprehension and Generation across Multiple Granularities |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2504.02478) · [GitHub](https://github.com/CVI-SZU/MG-MotionLLM)  |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | MG-MotionLLM |
| Dataset | HumanML3D (Text-to-Motion), HumanML3D (Motion-to-Text) |

> [!tip] 效果简介
> - HumanML3D (Text-to-Motion) 上，FID ↓ 为 0.303，对比 0.567 (MotionGPT)，变化 −0.264。
> - HumanML3D (Text-to-Motion) 上，Top-1 R-Precision ↑ 为 0.516，对比 0.492 (MotionGPT)，变化 +0.024。
> - HumanML3D (Text-to-Motion) 上，Diversity ↑ 为 9.960，对比 9.528 (MotionGPT)，变化 +0.432。

## 概要

MG-MotionLLM 是一个面向多粒度运动理解与生成的统一框架。其核心动机源于一个关键瓶颈：**直接将人体运动序列与长篇幅的细粒度文本描述对齐存在根本性困难**。详细文本描述的长度常常超过 1000 个 token，而运动序列通常仅被压缩为约 50 个运动 token，信息密度差异巨大，导致模型难以捕捉运动的全局语义。实验证实，当直接将粗粒度和详细文本描述拼接用于指令微调时，运动生成的 Top-3 检索精度从仅使用粗粒度文本的 77.3% 下降至 75.0%，说明长文本反而干扰了全局语义学习。

为解决这一问题，MG-MotionLLM 提出了**两阶段多粒度训练方案**。第一阶段为 **Granularity-Synergy Pre-training（多粒度协同预训练）**，通过 28 个跨粒度的辅助任务（涵盖时间边界定位、片段描述生成等），逐步建立运动与细粒度文本之间的映射关系，并实现粗粒度与细粒度任务间的知识迁移和相互增强。第二阶段为 **Task-Specific Instruction Tuning（任务特定指令微调）**，针对特定下游任务进一步优化。实验表明，经过协同预训练的模型在所有四个测试任务上均优于直接指令微调的模型，且在此基础上进行第二阶段微调可获得进一步显著提升——例如 Text-to-Motion 的 Top-3 精度从 0.767 提升至 0.802。消融实验进一步揭示，预训练阶段的 28 个任务缺一不可，移除任意一个任务均会导致平均 Top-1 检索精度下降。

在方法定位上，MG-MotionLLM 延续了将运动离散化为 token 并与语言模型统一建模的路线（如 **MotionGPT**, NeurIPS 2023），但其核心创新在于**多粒度协同训练策略**，使得单一模型能够同时胜任粗粒度任务（如文本驱动运动生成、运动描述生成）和首次提出的细粒度任务（如运动到详细文本生成、运动时间定位）。在 HumanML3D 基准上，MG-MotionLLM 在文本驱动运动生成任务中取得了 FID 0.303（MotionGPT 为 0.567）、Top-1 R-Precision 0.516 的结果，在运动描述生成任务中取得了 Top-1 R-Precision 0.592 的结果，均优于现有统一框架方法。

### 问题背景

人体运动理解与生成是计算机视觉和图形学领域的核心问题，涵盖文本到运动生成（Text-to-Motion）、运动描述生成（Motion-to-Text）等经典任务。近年来，随着大规模语言模型（LLM）的兴起，研究者开始探索将运动数据离散化为运动token，从而在统一的语言模型框架中同时处理运动理解与生成任务。代表性工作如**MotionGPT**（NeurIPS 2023）基于T5架构，首次尝试将运动与文本统一建模，但其能力主要局限于粗粒度任务——即用简短的句子描述整体动作（如“一个人向前走并挥手”），而无法处理涉及身体部位随时间变化的细粒度描述。

### 现有方法的核心缺口

现有统一运动-语言模型面临一个根本性瓶颈：**运动与长详细文本之间的直接对齐极为困难**。细粒度运动描述（motion script）通常包含超过1000个token，详细刻画了身体各部位在每一时间片段的状态变化，而对应的运动token最多仅约50个。这种信息量的巨大不对称导致模型难以捕捉运动的全局语义。实验证据直接验证了这一问题：当作者尝试直接将粗粒度描述与详细描述拼接后对LLM进行指令微调时，模型在文本到运动生成任务上的Top-3检索精度从仅使用粗粒度描述的**77.3%下降至75.0%**。这表明，长详细文本非但未能提供有效补充信息，反而干扰了模型对全局运动语义的学习。

### 本文动机与核心思路

上述瓶颈揭示了一个关键洞察：**粗粒度与细粒度的运动-语言对齐不应被割裂处理，而应通过精心设计的跨粒度辅助任务实现知识迁移与相互增强**。基于此，本文提出MG-MotionLLM，核心思路是在统一语言模型框架中同时训练粗粒度任务（如整体动作描述生成）和细粒度任务（如运动片段的时间边界定位、片段级详细描述生成），通过多任务间的知识共享，使模型在各粒度上的理解与生成能力同步提升。

具体而言，MG-MotionLLM采用两阶段训练策略：第一阶段为**Granularity-Synergy Pre-training**（多粒度协同预训练），引入时间边界定位、片段描述生成等28个跨粒度辅助任务，逐步建立运动与细粒度文本的映射关系；第二阶段为**Task-Specific Instruction Tuning**（任务特定指令微调），针对具体下游任务进一步优化。这一设计使得单一模型能够胜任从粗粒度运动生成到细粒度运动定位等多种新旧任务，突破了现有统一框架仅能处理粗粒度描述的局限。

## 核心方法与创新机理

MG-MotionLLM的核心创新在于**通过多粒度协同预训练（Granularity-Synergy Pre-training）解决运动与长详细文本直接对齐的瓶颈**，并构建了一个真正统一的、覆盖粗粒度与细粒度任务的运动语言模型框架。

### 1. 核心瓶颈：长详细文本与运动token的信息量鸿沟

运动理解与生成的一个关键挑战是：**直接将运动与长详细文本对齐会导致性能退化**。详细运动描述（motion script）的长度通常超过1000个token，而一条运动序列经VQ-VAE离散化后最多仅约50个运动token。这种信息量的巨大不对称，使得模型在联合训练粗粒度和细粒度任务时，难以捕捉运动的全局语义。实验证据直接印证了这一点：当直接使用粗粒度描述加详细文本指令微调语言模型时，运动生成的Top-3检索精度从仅用粗粒度描述的**77.3%下降至75.0%**（Table 5消融实验）。这说明，简单地将长文本与运动token拼接送入模型，非但不能带来增益，反而会干扰模型对运动整体语义的学习。

### 2. 因果调节变量：28个跨粒度辅助任务的协同预训练

为突破上述瓶颈，MG-MotionLLM将训练过程重构为**两阶段方案**（changed slot: 训练方案），这是其相对于MotionGPT等单阶段指令微调方法的根本性改变：

- **第一阶段：Granularity-Synergy Pre-training（多粒度协同预训练）**。模型在28个涵盖粗粒度与细粒度的任务上进行联合预训练，包括12个经典粗粒度任务（如text-to-motion、motion captioning）和16个新提出的细粒度任务。这些任务按输入信息类型（文本、时间边界、运动token）的组合方式组织（Table 1），形成从单一信息类型到三种信息类型组合的递进结构。关键设计在于：**将长详细文本按运动片段拆分，设计（Motion Snippet, Snippet Motion Script）-to-Time等辅助任务，先学习局部时间边界与文本的对齐**，再通过多任务间的知识迁移实现粗-细粒度的相互增强（changed slot: 细粒度对齐策略）。

- **第二阶段：Task-Specific Instruction Tuning（任务特定指令微调）**。在协同预训练的基础上，针对特定下游任务进行额外微调，以达到最优性能。

消融实验（Table 5）严格验证了这一两阶段方案的有效性：**仅经过Granularity-Synergy Pre-training的模型（即使每个任务的训练迭代次数仅为直接指令微调的约1/30），在所有四个测试任务上均优于直接对特定任务进行指令微调的模型**；在此基础上进行第二阶段的特定任务微调，性能进一步提升——例如Text-to-Motion的Top-3精度从0.767提升至**0.802**。更进一步地，Figure 6显示，移除预训练阶段的任意一个任务，模型的平均Top-1检索精度均低于使用全部28个任务预训练的模型，证明**每个辅助任务对多粒度协同均有正向贡献**。

### 3. 核心洞察：统一框架下的多粒度知识迁移

MG-MotionLLM的核心洞察在于：**在统一语言模型框架中同时训练粗粒度（如整体动作描述）和细粒度（如身体部位随时间变化的详细脚本）的运动-语言任务，多任务间的知识迁移和互相促进能显著提升模型在各粒度上的理解和生成能力**。这使得单一模型无需针对每个任务分别设计架构，即可胜任文本到运动生成、运动描述生成、运动到详细文本生成、运动时间定位等多种新老任务（Figure 1, Figure 4）。

### 4. 方法定位：相对于基线的增量贡献

相较于已有的统一运动-语言方法**MotionGPT**（NeurIPS 2023），MG-MotionLLM的核心增量在于：

| 维度 | MotionGPT | MG-MotionLLM |
|------|-----------|--------------|
| 训练方案 | 单阶段指令微调（仅粗粒度任务） | 两阶段：28个跨粒度任务协同预训练 + 任务特定指令微调 |
| 细粒度对齐 | 未涉及 | 将长详细文本按片段拆分，通过时间边界定位等辅助任务建立局部对齐，再通过多任务协同实现粗-细知识融合 |
| 任务覆盖 | 仅粗粒度（text-to-motion, motion captioning等） | 粗粒度 + 新细粒度任务（motion-to-detailed text, motion localization等） |

在HumanML3D测试集上，MG-MotionLLM在统一方法中取得了最优的Text-to-Motion FID（0.303 vs MotionGPT的0.567，Table 2）和Motion-to-Text Top-1 R-Precision（0.592 vs MotionGPT的0.543，Table 3），验证了多粒度协同预训练带来的实质性提升。

MG-MotionLLM 的整体框架遵循“离散化-统一序列建模-两阶段训练”的流水线设计。其核心思路是将高维运动数据压缩为离散 token，与自然语言文本在同一序列空间中统一处理，再通过多粒度协同训练赋予模型跨任务的理解与生成能力。

### 流水线总览

整个系统由两大模块串联构成（Figure 2）：

![[assets/figures/papers/paper_list_l5_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our MG-MotionLLM. It consists of a motion VQ-VAE and a T5-based motion-aware language model*

1. **Motion VQ-VAE**：负责将原始运动序列编码为离散的运动 token 序列，并可从 token 序列逆向解码重建运动。
2. **Motion-Aware Language Model**：基于 T5 架构，在扩展词汇表后统一接收文本描述、运动 token 和特殊控制 token，以自回归方式执行所有多粒度任务。

### 模块间的数据流

- **输入侧**：一段人体运动序列 $M$ 首先进入 Motion VQ-VAE 的编码器 $E$，输出连续潜变量序列 $Z$。通过最近邻查找将每个潜变量 $\pmb{z}_i$ 量化为码本 $\pmb{B}$ 中距离最近的向量 $\pmb{b}_k$，得到离散运动 token 序列 $\pmb{c}_i$：
  
  $$\pmb{c}_i = \underset{\pmb{b}_k \in \pmb{B}}{\arg \min} \left\| \pmb{z}_i - \pmb{b}_k \right\|_2$$

- **统一序列空间**：扩展后的词汇表 $\mathcal{V} = \{\mathcal{V}_t, \mathcal{V}_m, \mathcal{V}_s\}$ 同时容纳文本 token（$\mathcal{V}_t$）、运动 token（$\mathcal{V}_m$）以及特殊 token（$\mathcal{V}_s$，如 `<Motion Tokens>`、`</Motion Tokens>`、`<SEP>`、`<Motionless>` 等）。这使得语言模型能够以统一的序列格式表示“文本-运动”多模态输入和输出，特殊 token 则用于标记运动片段的起止和模态边界。

- **输出侧**：Motion-Aware Language Model 以自回归方式逐 token 预测目标序列，损失函数为标准交叉熵：
  
  $$\mathcal{L}_{\mathrm{CE}} = - \sum_{i=1}^{N_{out}} \log P(v_{out}^i \mid X_{in}, v_{out}^j, \theta_{LLM}), \quad j < i$$
  
  当输出为运动 token 时，生成的 token 序列经 Motion VQ-VAE 的解码器 $D$ 重建为连续运动；当输出为文本时，直接解码为自然语言描述。

### 训练的两阶段设计

MG-MotionLLM 的训练分为两个阶段，这是其区别于直接指令微调方案的关键：

1. **第一阶段：Granularity-Synergy Pre-training（多粒度协同预训练）**  
   在 28 个涵盖粗粒度与细粒度的运动相关任务上对模型进行联合预训练（12 个经典粗粒度任务 + 16 个新提出的细粒度任务）。这些任务按输入信息类型（文本、时间、运动）的数量进行组织（Table 1），迫使模型在不同粒度间建立知识迁移——例如，通过“运动片段定位”任务学习局部时间边界与细粒度文本的对齐，再反哺粗粒度的整体运动理解。

2. **第二阶段：Task-Specific Instruction Tuning（任务特定指令微调）**  
   在预训练模型基础上，针对特定下游任务（如 Text-to-Motion、Motion-to-Text）进行额外的指令微调，使模型在该任务上达到最优性能。

### 设计动机：为什么要两阶段？

直接使用粗粒度描述与长详细文本拼接进行指令调优时，模型性能反而下降——Top-3 检索精度从仅用粗粒度描述的 77.3% 降至 75.0%。根本原因在于详细描述长度常超 1000 个 token，而运动 token 至多约 50 个，信息密度极度不对称，导致模型难以捕捉运动的全局语义。两阶段训练通过先让模型在 28 个辅助任务中逐步建立细粒度映射，再在第二阶段聚焦特定任务，有效规避了这一瓶颈。消融实验证实，移除预训练阶段任意一个任务均会导致平均 Top-1 检索精度下降（Figure 6），且经过协同预训练的模型在所有四个测试任务上均优于直接指令微调的模型（Table 5）。

### 3.1 运动离散化：Motion VQ-VAE

MG-MotionLLM 的运动理解与生成能力建立在将连续运动序列离散化为 token 序列的基础上。为此，方法采用了一个 **Motion VQ-VAE** 模块，其网络结构与训练策略遵循 **T2M-GPT**（CVPR 2023）的设计。该模块由编码器 $E$、解码器 $D$ 和一个可学习的码本 $\pmb{B} = \{\pmb{b}_k\}_{k=1}^K$ 组成。

给定一段运动序列 $M \in \mathbb{R}^{T \times D}$（$T$ 为帧数，$D$ 为每帧的关节表示维度），编码器 $E$ 将其映射为一组潜变量 $Z = \{\pmb{z}_i\}_{i=1}^{N}$。随后，每个潜向量 $\pmb{z}_i$ 通过最近邻查找被量化为码本中距离最近的码向量，得到对应的离散运动 token $\pmb{c}_i$：

$$
\pmb{c}_i = \underset{\pmb{b}_k \in \pmb{B}}{\arg \min} \left\| \pmb{z}_i - \pmb{b}_k \right\|_2
$$

解码器 $D$ 则根据量化后的 token 序列 $\hat{Z} = \{\pmb{c}_i\}$ 重建运动序列 $\hat{M}$。整个 VQ-VAE 的训练目标由三项损失加权组合而成：

$$
\mathcal{L}_{\mathrm{VQVAE}} = \Vert M - \hat{M} \Vert_2 + \Vert \mathcal{F}_{\mathrm{SG}}(Z) - \hat{Z} \Vert_2 + \beta \Vert Z - \mathcal{F}_{\mathrm{SG}}(\hat{Z}) \Vert_2
$$

其中，$\mathcal{F}_{\mathrm{SG}}$ 表示 stop-gradient 算子。第一项为运动重建损失，保证解码器能准确恢复原始运动；第二项为嵌入损失（embedding loss），推动码本向量向编码器输出靠拢；第三项为承诺损失（commitment loss），约束编码器输出不要偏离所选码向量过远，$\beta$ 为平衡系数。通过这一离散化过程，连续的运动信号被压缩为有限词汇表中的 token 序列，为后续语言模型的统一处理奠定了基础。

### 3.2 统一词汇表与运动感知语言模型

为使语言模型能够无缝处理文本描述与运动 token，MG-MotionLLM 构建了一个统一的词汇表 $\pmb{V} = \{\pmb{V}_t, \pmb{V}_m, \pmb{V}_s\}$，包含三类元素：

- **文本词汇 $\pmb{V}_t$**：继承自预训练 T5 模型的原始文本 token。
- **运动词汇 $\pmb{V}_m$**：由 Motion VQ-VAE 码本中所有码向量索引构成的运动 token 集合。
- **特殊词汇 $\pmb{V}_s$**：用于标记多模态序列边界与结构的控制 token，包括 `<Motion Tokens>`、`</Motion Tokens>`、`<SEP>` 以及 `<Motionless>` 等。

运动感知语言模型的核心是一个经过词汇表扩展的 **T5** 模型。该模型以自回归方式对输入序列 $X_{in}$（可包含文本、运动 token 及特殊 token 的任意组合）进行建模，并通过标准的交叉熵损失优化下一 token 预测能力：

$$
\mathcal{L}_{\mathrm{CE}} = - \sum_{i=1}^{N_{out}} \log \left( P(v_{out}^i \mid X_{in}, v_{out}^j, \theta_{LLM}) \right), \quad j < i
$$

其中 $v_{out}^i$ 为输出序列中的第 $i$ 个 token，$\theta_{LLM}$ 为语言模型参数。该损失函数统一驱动所有多粒度任务的训练——无论是从文本生成运动 token、从运动 token 生成描述文本，还是执行时间边界定位等细粒度任务，均被形式化为同一自回归序列建模问题。

## 实验与关键发现

### 核心瓶颈验证：粗-细粒度直接对齐的失效

MG-MotionLLM的设计起点来自一个关键实验发现：直接将运动与长详细文本对齐会导致性能退化。当研究者尝试用粗粒度描述和详细描述（长度常超1000 token）共同对语言模型进行指令微调以生成运动时，模型的Top-3检索精度从仅使用粗粒度描述的**77.3%下降至75.0%**。这一退化现象揭示了核心瓶颈——运动token最多约50个，而详细描述的信息量远超运动序列的承载能力，长文本的引入反而干扰了模型对运动全局语义的捕捉。

### 主实验结果

#### 文本驱动运动生成（Text-to-Motion）

在HumanML3D测试集上，MG-MotionLLM在统一运动理解与生成的方法中取得了最优性能（Table 2）。与同为统一框架的**MotionGPT**（NeurIPS 2023）相比：

![[assets/figures/papers/paper_list_l5_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation/figures/004_Table_2.jpg]]
*Table 2: Comparison of motion generation on the HumanML3D [6] test set. We group the existing methods into ones that solely focus on motion generation (Motion Gen. Only) and ones that unify motion understanding and generation tasks (Unified Motion Gen. and Und.). Bold results refer to the best ones in each block. Results showed that our MG-MotionLLM achieves state-of-the-art performance*

- **FID**：0.303 vs. 0.567（降低0.264），表明生成运动的分布更接近真实数据；
- **Top-1 R-Precision**：0.516 vs. 0.492（提升0.024），文本-运动匹配精度更高；
- **Diversity**：9.960 vs. 9.528（提升0.432），生成多样性更丰富。

值得注意的是，MG-MotionLLM的FID（0.303）已接近专门面向运动生成的强基线方法如**MoMask**（CVPR 2024，FID=0.204）和**T2M-GPT**（CVPR 2023，FID=0.116），但作为统一框架，其同时具备运动理解和细粒度生成能力，这是专用生成方法所不具备的。

#### 运动描述生成（Motion-to-Text）

在HumanML3D上的运动描述生成任务中（Table 3），MG-MotionLLM同样超越现有方法：

![[assets/figures/papers/paper_list_l5_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation/figures/005_Table_3.jpg]]
*Table 3: Motion captioning results on the HumanML3D [6] test set. We bold the best result and underline the second-best one. Our model exceeds the previous methods on most metrics*

- **Top-1 R-Precision**：0.592 vs. 0.543（MotionGPT），提升0.049；
- **MM-Dist**：2.581 vs. 2.821（MotionGPT），降低0.240，说明生成文本与真实描述的语义距离更小。

#### 运动到详细文本生成（Motion-to-Detailed Text）

这是本文首次提出的细粒度基准任务，在FineMotion测试集上进行评估（Table 4）。由于缺乏外部基线，实验仅在模型不同尺寸间进行比较，以BERTScore为评估指标。结果显示，更大的模型容量在大多数指标上带来更好性能，验证了该任务对模型表达能力的要求。

![[assets/figures/papers/paper_list_l5_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation/figures/006_Table_4.jpg]]
*Table 4: Results of Motion-to-Detailed Text at two levels on the FineMotion test set. Results show that the larger model size yields better performance on most metrics*

### 消融实验：训练策略的核心贡献

Table 5展示了训练策略消融的关键结论：

1. **Granularity-Synergy Pre-training的有效性**：经过多粒度协同预训练的模型在所有四个测试任务上均优于直接对特定任务进行指令微调的模型。值得注意的是，预训练阶段每个任务仅分配到约1/30的训练迭代，但跨粒度任务间的知识迁移仍带来了显著增益。

2. **任务特定微调的叠加收益**：在协同预训练基础上进行第二阶段的Task-Specific Instruction Tuning，性能进一步提升。例如，Text-to-Motion的Top-3精度从预训练后的0.767提升至0.802，验证了两阶段训练方案的互补性。

3. **28个预训练任务的必要性**：Figure 6展示了逐任务消融结果。移除预训练阶段任意一个任务，模型在三个代表性任务（Text-to-Motion、Motion-to-Text、(Text, Detailed Text)-to-Motion）上的平均Top-1检索精度均低于使用全部28个任务预训练的模型。这证明每个辅助任务——无论是粗粒度的经典任务还是细粒度的新任务——都对整体性能有正向贡献，多粒度任务间存在相互增强效应。

### 模型容量的影响

Table 6展示了不同T5模型尺寸（Small 60M、Base 220M、Large 770M）的消融结果。从Small到Base时性能提升明显，但从Base到Large时提升有限，甚至在部分任务上出现性能下降。这一现象与**MotionGPT**（NeurIPS 2023）的观察一致，推测受限于HumanML3D数据集仅包含约1.5万条运动序列的规模，更大模型可能面临过拟合风险。该结论提示，在更大规模运动数据集上验证模型容量的可扩展性是一个值得探索的方向。

### 局限性分析

1. **运动表征范围受限**：当前模型仅关注人体身体动作，未涉及面部表情和手部动作等更精细的运动维度。
2. **场景单一**：模型仅处理单人运动，尚未扩展到多人交互、动物运动以及人-物交互等更复杂场景。
3. **细粒度编辑的自动化不足**：细粒度运动编辑目前仍需用户手动修改运动脚本（motion script），尚未实现通过自然语言指令自动生成或修改脚本的功能。
4. **控制模态有限**：尚未整合音乐片段等其他时间序列模态作为控制信号。

![[assets/figures/papers/paper_list_l5_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation/figures/016_Table_9.jpg]]
*Table 9: Examples of prompt templates for tasks that utilize two types of information in the input*

![[assets/figures/papers/paper_list_l5_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation/figures/008_Table_5.jpg]]
*Table 5: Ablation of the proposed training scheme in four motion tasks on HumanML3D [6] dataset. Results show that the Granularity-Synergy Pre-trained model outperforms models that are directly instruction-tuned on specific tasks, even with relatively few training iterations per task (approximately 1/30). Pretraining the model with tasks spanning multiple granularities promotes mutual enhancement across tasks at each granularity. Further instruction tuning on specific tasks leads to significant performance gains*

## 定位与知识库关联

### 1. 方法脉络与基线关系

MG-MotionLLM 处于**统一运动理解与生成**这一研究脉络中，其直接对标的核心基线是 **MotionGPT**（NeurIPS 2023）。两者共享以下设计基因：(1) 均采用 Motion VQ-VAE 将连续运动序列离散化为 token；(2) 均基于 T5 语言模型架构构建运动感知语言模型；(3) 均试图在单一框架内同时处理运动理解（Motion-to-Text）与生成（Text-to-Motion）任务。然而，MG-MotionLLM 在以下关键维度上实现了对 MotionGPT 的超越：

- **粒度扩展**：MotionGPT 仅处理粗粒度任务（如整体动作描述与生成），MG-MotionLLM 首次将细粒度任务（如身体部位随时间变化的详细脚本生成、运动时间边界定位）纳入统一框架，定义了 16 个全新的细粒度任务。
- **训练策略革新**：MotionGPT 采用单阶段指令微调，而 MG-MotionLLM 提出了两阶段的 **Granularity-Synergy Pre-training + Task-Specific Instruction Tuning** 方案，通过 28 个跨粒度辅助任务的协同预训练，实现了粗-细任务间的知识迁移与相互增强。
- **性能优势**：在 HumanML3D 基准上，MG-MotionLLM 的 Text-to-Motion FID 降至 0.303（MotionGPT 为 0.567），Motion-to-Text Top-1 R-Precision 提升至 0.592（MotionGPT 为 0.543），在统一模型类别中达到最优。

在更广泛的文本驱动运动生成领域，MG-MotionLLM 与以下专用方法形成对比：

| 方法 | 定位 | 关键差异 |
|------|------|----------|
| **T2M-GPT** (CVPR 2023) | 专用运动生成 | 仅关注生成，不涉及理解任务；MG-MotionLLM 在统一框架下实现了可竞争的性能 |
| **MoMask** (CVPR 2024) | 专用运动生成强基线 | 同样仅专注生成；MG-MotionLLM 以统一模型身份在 FID 指标上接近专用方法水平 |
| **MotionDiffuse** (TPAMI 2024) | 扩散模型运动生成 | 基于扩散范式，与 MG-MotionLLM 的自回归语言模型范式不同 |
| **FineMoGen** (NeurIPS 2024) | 细粒度时空运动生成 | 关注细粒度生成但未涉及理解任务；MG-MotionLLM 同时覆盖细粒度的理解与生成 |
| **TM2T** (ECCV 2022) | 运动描述生成 | 仅处理 Motion-to-Text 单一任务；MG-MotionLLM 在统一框架下超越了其性能 |

### 2. 核心因果机制与设计瓶颈

**瓶颈识别**：论文通过关键消融实验揭示了一个反直觉的现象——直接将长详细文本（通常超过 1000 个 token）与运动（最多约 50 个 token）对齐进行指令微调时，模型性能反而下降。具体而言，同时使用粗粒度描述和详细描述进行训练时，Text-to-Motion 的 Top-3 检索精度从仅用粗粒度描述的 77.3% 降至 75.0%。这表明长详细文本的巨大信息量干扰了模型对运动全局语义的捕捉。

**因果调节变量**：Granularity-Synergy Pre-training 阶段是解决上述瓶颈的关键。该阶段通过以下机制建立有效的跨粒度映射：
1. **分解对齐**：将长详细文本按时间片段拆分，设计（Motion Snippet, Motion Script）-to-Time 等辅助任务，先学习局部时间边界与文本的对应关系。
2. **协同增强**：28 个任务涵盖粗粒度（12 个经典任务）和细粒度（16 个新任务），多任务联合训练使不同粒度的知识相互迁移和增强。
3. **证据强度**：消融实验（Table 5）表明，经过 Granularity-Synergy Pre-training 的模型在所有四个测试任务上均优于直接指令微调的模型；进一步的任务特定微调可将 Text-to-Motion Top-3 精度从 0.767 提升至 0.802。此外，Figure 6 显示移除预训练阶段的任意一个任务都会导致平均 Top-1 检索精度下降，证明每个辅助任务均有正向贡献。

### 3. 适用边界与局限

**已确认的适用范围**：
- 单人人体身体动作的理解与生成（不含面部表情和手部动作）
- 粗粒度任务：Text-to-Motion、Motion-to-Text（整体动作描述）
- 细粒度任务：Motion-to-Detailed Text（序列级和片段级）、运动时间边界定位、细粒度运动描述生成
- 基于 HumanML3D 和 FineMotion 数据集的运动类型

**明确局限**：
1. **运动范畴受限**：仅关注人体身体动作，未涉及面部表情和手部动作等更精细的运动维度。
2. **交互场景缺失**：当前模型只处理单人运动，尚未扩展到多人交互、动物运动以及人-物交互等更广泛场景。
3. **编辑能力有限**：细粒度运动编辑目前需要用户手动修改运动脚本（motion script），尚未实现通过自然语言指令自动生成或修改脚本的功能。
4. **控制模态单一**：尚未整合如音乐片段等其他时间序列模态作为精细粒度的控制信号。
5. **模型规模收益递减**：消融实验（Table 6）表明，模型容量从 Small（60M）增大到 Base（220M）时性能提升明显，但从 Base 到 Large（770M）提升有限甚至部分任务下降，疑似受限于 HumanML3D 数据规模。

### 4. 开放问题与未来方向

论文明确指出的开放问题包括：

1. **智能细粒度编辑**：如何利用大语言模型自动将用户的简洁自然语言指令映射为对应的运动脚本修改，实现更智能的细粒度运动编辑？
2. **场景扩展**：如何将 MG-MotionLLM 扩展到多人交互、动物运动等场景，并整合面部表情和手部动作？
3. **多模态控制融合**：能否将音乐等时间序列模态作为额外的控制信号，实现更丰富的运动生成？
4. **规模化效应**：在更大规模的数据集上，增加模型参数量是否会带来一致的性能提升？

此外，从方法谱系角度看，以下问题值得进一步探索：
- Granularity-Synergy Pre-training 中 28 个任务的必要性已在当前数据规模下验证，但任务间的冗余性和最优任务组合策略尚不明确。
- 细粒度任务“Motion-to-Detailed Text”为本文首次提出的基准，缺乏外部独立验证和标准化评估协议，其评估体系（BERTScore）的可靠性需要在更广泛的社区共识中确认。

## 原文 PDF

![[paperPDFs/CVPR_2025/MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities.pdf]]
