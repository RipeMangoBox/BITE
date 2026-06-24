---
title: "PoseScript: 3D Human Poses from Natural Language"
type: paper
paper_level: A
venue: ECCV
year: 2022
pdf_ref: paperPDFs/ECCV_2022/PoseScript_3D_Human_Poses_from_Natural_Language.pdf
aliases:
- PoseScript
tags:
- ECCV_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过从归一化3D关键点自动提取多类posecodes（角度、距离、相对位置、俯仰/滚转、地面接触），并引导性地选择、聚合与转换为自然语言，可以大规模生成多样化且语义丰富的姿态描述，从而为下游检索和生成模型提供充足的训练数据。
primary_logic: 3D人体姿态的语义可被分解为一系列可计算的半结构化属性（posecodes），并借助随机化与聚合规则自动合成自然语言描述；利用这些合成描述进行预训练，再在人工标注上微调，能够显著提升文本-姿态跨模态检索与生成的性能。
claims:
- 自动描述生成管线建立在低层posecodes和高层概念之上，posecodes是对posebits的细粒度扩展。
- posecode提取涵盖五类基本关系：角度、距离、相对位置、俯仰/滚转和地面接触。
- 在自动描述上训练的检索模型达到69.1%的平均召回率，微调后在人工描述上将平均召回率从12.4%提升至30.4%。
- 文本条件姿态生成中，添加额外正则化损失改善全部指标；在自动描述上预训练后微调进一步大幅提升所有生成指标（FID、ELBO、mRecall）。
---

# PoseScript: 3D Human Poses from Natural Language

> [!tip] 核心洞察
> 3D人体姿态的语义可被分解为一系列可计算的半结构化属性（posecodes），并借助随机化与聚合规则自动合成自然语言描述；利用这些合成描述进行预训练，再在人工标注上微调，能够显著提升文本-姿态跨模态检索与生成的性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | PoseScript：基于自然语言的3D人体姿态 |
| 英文题名 | PoseScript: 3D Human Poses from Natural Language |
| 会议/期刊 | ECCV 2022 |
| Links | [paper](https://www.ecva.net/papers/eccv_2022/papers_ECCV/html/2069_ECCV_2022_paper.php) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PoseScript (自动描述生成流水线 + 跨模态检索/生成模型) |
| Dataset | PoseScript-H |

> [!tip] 效果简介
> - PoseScript-H (检索) 上，mRecall 30.4 (预训练+微调) vs 12.4 (仅人类描述训练) (+18.0)。
> - PoseScript-H (生成) 上，FID 0.11 (预训练) vs 0.14 (无预训练) (-0.03)；mRecall G/R 16.2 (预训练) vs 2.7 (无预训练) (+13.5)。

## 概述

**问题瓶颈**：当前缺乏将静态3D人体姿态与细粒度、结构化的自然语言描述直接配对的数据集，这从根本上限制了模型根据文本理解并生成复杂人体姿态的能力。

**核心洞察**：3D人体姿态的语义可被分解为一系列可计算的半结构化属性——posecodes（涵盖角度、距离、相对位置、俯仰/滚转、地面接触五类基本关系），并借助随机化选择与聚合规则自动合成自然语言描述。利用这些合成描述进行预训练，再在人工标注上微调，能够显著提升文本-姿态跨模态检索与生成的性能。

**方法定位**：PoseScript 提出了一套自动描述生成流水线（posecode提取 → 选择与聚合 → 句子转换），并在此基础上构建了文本-姿态跨模态检索模型（bi-GRU文本编码器 + VPoser姿态编码器，联合嵌入空间，BBC损失训练）和文本条件VAE生成模型（文本条件先验 + 额外KL正则化项）。该方法属于数据驱动与跨模态表示学习的技术路线，在方法谱系中填补了“大规模文本-3D姿态配对数据自动生成”这一关键空白。

**主要结果**：
- **检索**：在自动描述上训练的检索模型在PoseScript-A测试集上达到69.1%的平均召回率；在人工描述（PoseScript-H）上，预训练后微调将平均召回率从12.4%提升至30.4%（+18.0个百分点）。
- **生成**：在文本条件VAE中添加与标准高斯的额外KL散度正则化项改善了全部评估指标（FID、ELBO、mRecall）；在自动描述上预训练后微调，将PoseScript-H上的mRecall G/R从2.7提升至16.2，FID从0.14降至0.11。

**局限性**：自动生成的描述在自然多样性上仍逊于人类语言，当前工作仅处理静态姿态而未扩展到运动序列，且数据集仅包含英语描述，存在文化和主观偏见引入的风险。

## 背景与动机

### 问题背景：3D人体姿态理解中的语义鸿沟

3D人体姿态估计与理解是计算机视觉领域的核心问题之一，在动画制作、运动分析、人机交互和虚拟现实等应用中具有广泛需求。然而，当前的研究主要聚焦于从图像或视频中重建3D姿态的几何精度，对于姿态的**语义层面理解**——即用自然语言描述和检索复杂的人体姿态——关注甚少。

这一语义鸿沟带来了两个关键挑战：其一，如何建立细粒度的文本描述与3D姿态之间的直接映射，使得用户可以通过自然语言查询来检索特定的姿态；其二，如何根据文本描述生成符合语义约束的3D人体姿态。这两项任务——**文本到姿态检索**与**文本条件姿态生成**——构成了PoseScript工作的核心应用场景（Figure 1）。

### 现有方法的缺口：缺乏文本-姿态配对数据

实现上述目标的首要障碍是**数据的缺失**。与图像-文本领域拥有大规模配对数据集（如MS COCO、Visual Genome）不同，3D人体姿态领域长期缺乏将静态姿态与细粒度、结构化的自然语言描述直接配对的数据集。现有的姿态数据集（如AMASS、Human3.6M）仅提供3D关键点或SMPL参数标注，不包含语义描述；而现有的文本-运动数据集（如KIT Motion-Language Dataset）则聚焦于时序动作序列，并不适用于静态姿态的细粒度语义理解。

这一数据缺口导致了两方面的困境：
1. **检索任务**无法训练跨模态嵌入模型，使得“一个膝盖弯曲、双臂举过头顶”这样的自然语言查询无法直接映射到3D姿态数据库。
2. **生成任务**缺乏文本条件的监督信号，难以从自然语言描述中生成语义一致的3D姿态。

### 本文动机：构建文本-姿态跨模态理解的桥梁

针对上述缺口，PoseScript提出了一个系统性的解决方案，其核心动机体现在三个层面：

**第一，构建大规模文本-姿态配对数据集。** 作者从AMASS数据集中采样了20,000个人体姿态，通过两种方式获取对应的自然语言描述：(a) 通过Amazon Mechanical Turk收集人工撰写的判别性描述（PoseScript-H），平均长度为55.1个token；(b) 设计自动描述生成流水线，从归一化的3D关键点自动提取语义信息并合成结构化描述（PoseScript-A）。这种双轨数据构建策略兼顾了描述的语义质量和规模可扩展性。

**第二，提出基于posecode的自动描述生成流水线。** 这是本文的方法论核心。作者将3D姿态的语义分解为一系列可计算的半结构化属性——**posecodes**，涵盖五类基本关系：角度（angles）、距离（distances）、相对位置（relative positions）、俯仰/滚转（pitch/roll）以及地面接触（ground contacts）。这些posecodes是对Posebits（Pons-Moll et al., 2014）的细粒度扩展，能够捕捉诸如“膝盖轻微弯曲”或“左手高于头部”等精细语义。通过随机选择、聚合和模板转换，该流水线可以大规模生成多样化且语义丰富的姿态描述（Figure 4），为下游任务提供充足的训练数据。

**第三，验证自动描述在跨模态任务中的有效性。** 作者假设：利用自动合成的描述进行预训练，再在人工标注上微调，能够显著提升文本-姿态跨模态检索与生成的性能。这一假设在实验中得到了验证——在自动描述上预训练的检索模型在PoseScript-A测试集上达到69.1%的平均召回率，微调后在人工描述上将平均召回率从12.4%大幅提升至30.4%（Table 1）；在文本条件姿态生成中，预训练同样显著改善了所有生成指标，包括FID、ELBO和mRecall（Table 2）。

### 工作定位与贡献

PoseScript是首个将静态3D人体姿态与自然语言描述进行系统性关联的工作，其贡献不仅在于数据集本身，更在于提出了一套从姿态语义提取到跨模态应用的完整技术链路。该工作为后续的文本驱动人体姿态理解、图像中的文本条件姿态拟合（Figure 10）等应用奠定了基础，同时揭示了自动描述合成作为跨模态预训练手段的巨大潜力。

## 核心创新

PoseScript 的核心创新并非提出全新的检索或生成架构，而是构建了一条从 **3D 关键点自动合成细粒度自然语言描述的数据流水线**，并证明利用该合成数据（PoseScript-A）进行预训练，再在人工标注数据（PoseScript-H）上微调，能够系统性地提升下游跨模态检索与文本条件姿态生成的性能。这一策略直接回应了当前领域缺少大规模、高质量文本-姿态配对数据的关键瓶颈。

### 创新一：基于 Posecode 的自动描述生成流水线

该工作的首要贡献是设计了一套从归一化 3D 人体关键点到结构化自然语言描述的全自动流水线（Figure 4），其核心机制是将人体姿态的语义信息分解为可计算、可组合的 **posecode** 单元。

流水线由三个关键模块串联构成：

1.  **Posecode 提取器**：从 3D 关键点坐标中自动提取五类基本关系——角度、距离、相对位置、俯仰/滚转、地面接触。这五类关系是对 Pons-Moll 等人提出的 posebits 的细粒度扩展，覆盖了描述人体姿态所需的主要语义维度。
2.  **Posecode 选择与聚合器**：通过规则化策略筛选有判别力的 posecode 子集，去除平凡信息，并应用四类聚合规则（基于实体、基于对称性、基于关键点、基于解释性）将多个 posecode 合并为更高层的语义表达。这些聚合规则在条件满足时随机触发，从而增加描述的多样性。
3.  **Posecode 到句子转换器**：通过主语选择、模板填充与随机排序，将选中的 posecode 集合转化为流畅的自然语言描述。

这一流水线的本质创新在于，它将姿态描述从依赖昂贵人工标注的瓶颈中解放出来，转而利用 3D 姿态本身蕴含的可计算语义，实现了大规模、多样化的描述自动生成。

### 创新二：合成数据预训练 + 人工数据微调的迁移策略

PoseScript 的第二个关键创新在于训练范式的改变——将自动描述（PoseScript-A）作为大规模预训练资源，再将模型迁移到人工描述（PoseScript-H）上进行微调。这一策略在两个下游任务上均展现出显著增益：

-   **文本-姿态检索**：仅在人工描述上训练的模型平均召回率（mRecall）仅为 12.4%，而先使用自动描述预训练再微调的模型达到了 30.4%，提升幅度达 +18.0 个百分点（Table 1）。
-   **文本条件姿态生成**：无预训练的生成模型在人工描述上的 mRecall G/R 仅为 2.7，预训练后跃升至 16.2（Table 2）；同时 FID 从 0.14 降至 0.11，表明生成姿态的逼真度和多样性均得到显著改善。

这一结果揭示了自动描述与人工描述之间存在可迁移的底层语义结构，而自动描述提供的丰富监督信号能够有效缓解人工标注数据稀缺带来的过拟合问题。

### 创新三：文本条件 VAE 的正则化增强

在文本条件姿态生成任务中，PoseScript 在标准 VAE 框架上引入了一项关键的正则化改进：在原有的后验分布与文本条件先验之间的 KL 散度之外，额外添加后验分布与标准高斯分布之间的 KL 散度项：

$$
\mathcal{L}_{\text{extra}} = \mathcal{L}_{KL}(\mathcal{N}_p, \mathcal{N}(0, I))
$$

消融实验表明，添加该正则化项改善了全部评估指标，包括 FID、ELBO 和 mRecall（Table 2 顶部）。这一改进的机理在于，额外的标准高斯正则化约束了潜在空间的全局结构，避免文本条件先验过度坍缩到特定模式，从而提升了生成样本的多样性与质量。

### 方法定位

与依赖纯人工标注的传统文本-姿态对齐方法相比，PoseScript 的核心差异化在于**以自动合成描述为桥梁，将数据稀缺问题转化为迁移学习问题**。其 posecode 流水线提供了一种结构化、可扩展的姿态语义编码方式，而预训练-微调范式则为小样本人工标注场景下的跨模态学习提供了有效路径。这一方法论框架不仅适用于静态 3D 姿态，也为后续向人体运动生成等时序任务的扩展提供了基础。

## 整体框架

PoseScript（ECCV 2022）的核心贡献是构建了一条从3D人体姿态到自然语言描述的自动生成流水线，并以此为基础支撑文本-姿态跨模态检索与文本条件姿态生成两大应用（图1）。该流水线的关键洞察在于：3D人体姿态的语义可被分解为一系列可计算的半结构化属性，即**posecodes**，进而通过规则化的选择、聚合与语言转换，自动合成多样化的语义描述。利用这些自动描述进行预训练，再在人工标注上微调，能够显著提升下游任务的性能。

### 自动描述生成流水线

自动描述生成流水线（图4）包含三个核心模块，依次对归一化后的3D关键点坐标进行处理：

1. **Posecode提取器**：从归一化3D关键点中自动提取五类基本语义关系——角度、距离、相对位置、俯仰/滚转以及地面接触。Posecode是对Posebits（Pons-Moll et al., CVPR 2014）的细粒度扩展，将身体各部位的连续关系离散化为类别化描述单元（如“膝盖微曲/相对弯曲/完全弯曲”）。

2. **Posecode选择与聚合器**：为避免生成冗长且无判别力的描述，该模块首先去除平凡posecodes，并随机跳过部分非必要posecodes。随后应用四类聚合规则——基于实体、基于对称性、基于关键点、基于解释性——在条件满足时随机触发，将相关posecodes合并为更紧凑的语义单元。

3. **Posecode到句子转换器**：分两步完成——首先为每个posecode选择主语（如具体身体部位），然后通过模板填充将所有posecodes组合为自然语言句子，并引入随机排序以增加描述多样性。

图2展示了人工标注与自动生成描述的对比示例：人工描述更注重整体姿态的判别性特征，而自动描述则呈现结构化的身体部位关系。

### 下游应用模块

在自动描述生成流水线的基础上，PoseScript构建了两个下游应用模块：

- **文本-姿态嵌入模型（检索）**：采用双向GRU作为文本编码器（输入为预训练GloVe词嵌入），VPoser编码器作为姿态编码器，将两模态映射到L2归一化的联合嵌入空间。训练使用基于批次的分类损失（BBC loss），公式为：

  $$\mathcal{L}_{\mathrm{BBC}} = -\frac{1}{B} \sum_{i=1}^{B} \log \frac{\exp(\gamma \sigma(x_i, y_i))}{\sum_j \exp(\gamma \sigma(x_i, y_j))}$$

  其中 $\sigma(x, y) = \frac{x^{\top} y}{\|x\|_2 \times \|y\|_2}$ 为余弦相似度，$\gamma$ 为可学习温度参数。该损失鼓励匹配的文本-姿态对在嵌入空间中靠近，同时推开同一批次中的其他样本（图5）。

- **文本条件VAE（生成）**：基于变分自编码器框架，包含姿态编码器、姿态解码器，并以文本编码器输出作为条件先验 $\mathcal{N}_c$。训练损失为：

  $$\mathcal{L} = \mathcal{L}_{R}(p, \hat{p}) + \mathcal{L}_{KL}(\mathcal{N}_{p}, \mathcal{N}_{c})$$

  即重建损失与后验分布 $\mathcal{N}_p$ 和文本条件先验之间的KL散度之和。测试时从 $\mathcal{N}_c$ 采样潜在变量 $z$，经解码器生成姿态（图8）。此外，引入额外的正则化项 $\mathcal{L}_{KL}(\mathcal{N}_p, \mathcal{N}(0,I))$（后验与标准高斯的KL散度）可进一步改善生成质量。

### 训练策略

整个框架的核心训练策略是**预训练-微调范式**：先在自动描述集（PoseScript-A）上预训练模型，再在人工描述集（PoseScript-H）上微调。实验表明，该策略在检索任务上将平均召回率从12.4%提升至30.4%，在生成任务上将FID从0.14降至0.11，mRecall G/R从2.7提升至16.2，充分验证了自动描述预训练的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_www_ecva_net_papers_eccv_2022_papers_ECCV_html_2069_ECCV_2022_pape/figures/002_Figure_2.jpg]]
*Figure 2: Examples of pose descriptions from PoseScript, produced by human annotators (left) and by our automatic captioning pipeline (right)*

![[assets/figures/papers/paper_list_l2_https_www_ecva_net_papers_eccv_2022_papers_ECCV_html_2069_ECCV_2022_pape/figures/004_Figure_4.jpg]]
*Figure 4: Overview of our captioning pipeline. Given a normalized 3D pose, we use posecodes to extract semantic pose information. These posecodes are then selected, merged or combined (when relevant) before being converted into a structural pose description in natural language. Letters ‘L’ and ‘R’ stand for ‘left’ and ‘right’ respectively*

## 核心模块与公式推导

PoseScript的方法体系由三个核心模块构成：自动描述生成流水线、文本-姿态跨模态检索模型，以及文本条件姿态生成模型。前者的输出为后两者提供训练数据，形成“合成数据预训练+人工标注微调”的闭环。

### 3.1 自动描述生成流水线

该流水线将归一化的3D人体关键点坐标转化为结构化的自然语言描述，包含三个子模块（图4）：

**Posecode提取器**：从归一化3D关键点自动提取五类基本关系——角度、距离、相对位置、俯仰/滚转、地面接触。这些posecodes是对posebits的细粒度扩展，将不同身体部位的关系量化为类别值（如“膝盖轻微/相当/完全弯曲”）。

**Posecode选择与聚合器**：首先去除平凡posecodes，随机跳过非判别性posecodes以增加多样性；随后应用四类聚合规则——基于实体的聚合、基于对称性的聚合、基于关键点的聚合、基于解释的聚合。聚合规则在条件满足时随机触发。

**Posecode到句子转换器**：分两步执行。第一步为每个posecode选择主语（如“左臂”“右膝”）；第二步将所有posecodes组合为最终描述，通过模板填充与随机排序生成人可读的自然语言句子。

### 3.2 文本-姿态检索模型

检索模型将文本和姿态映射到联合嵌入空间，通过BBC损失训练（图5）。文本编码器采用bi-GRU，输入为预训练的GloVe词嵌入；姿态编码器选用VPoser编码器。两编码器输出经L2归一化后得到嵌入向量$x = \theta(c) \in \mathbb{R}^d$和$y = \phi(p) \in \mathbb{R}^d$。

核心损失函数为批次分类损失（BBC loss）：

$$\mathcal{L}_{\mathrm{BBC}} = -\frac{1}{B} \sum_{i=1}^{B} \log \frac{\exp(\gamma \sigma(x_i, y_i))}{\sum_j \exp(\gamma \sigma(x_i, y_j))}$$

其中$\gamma$为可学习温度参数，$\sigma$为余弦相似度：

$$\sigma(x, y) = \frac{x^{\top} y}{\|x\|_2 \times \|y\|_2}$$

该损失鼓励匹配的文本-姿态对在嵌入空间中靠近，同时将非匹配对推开。

### 3.3 文本条件姿态生成模型

生成模型基于变分自编码器（VAE）框架（图8）。训练时，姿态编码器输出后验分布$\mathcal{N}_p$，文本编码器输出条件先验分布$\mathcal{N}_c$。总损失为重建损失与KL散度之和：

$$\mathcal{L} = \mathcal{L}_{R}(p, \hat{p}) + \mathcal{L}_{KL}(\mathcal{N}_{p}, \mathcal{N}_{c})$$

其中$\mathcal{L}_{R}(p, \hat{p})$衡量原始姿态$p$与重建姿态$\hat{p}$之间的差异，$\mathcal{L}_{KL}$约束后验分布逼近文本条件先验。

**额外正则化项**：作者进一步引入后验分布与标准高斯分布之间的KL散度作为额外正则化：

$$\mathcal{L}_{KL}(\mathcal{N}_p, \mathcal{N}(0, I))$$

消融实验表明，添加该正则化项在自动描述上改善了全部评估指标（FID从0.10降至0.08，mRecall R/G从24.7升至29.2，mRecall G/R从14.4升至17.3）。推理时，从文本条件先验$\mathcal{N}_c$中采样隐变量$z$，经解码器生成姿态。

### 3.4 预训练-微调范式

两个下游任务均采用统一的训练策略：先在自动描述PoseScript-A上预训练，再在人工描述PoseScript-H上微调。检索任务中，微调使mRecall从12.4%提升至30.4%；生成任务中，预训练使FID从0.14降至0.11，mRecall G/R从2.7跃升至16.2。这一范式验证了合成数据预训练对缓解人工标注稀缺问题的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_www_ecva_net_papers_eccv_2022_papers_ECCV_html_2069_ECCV_2022_pape/figures/005_Figure_5.jpg]]
*Figure 5: Overview of the training scheme of the retrieval model. The input pose and caption are fed to a pose encoder and a text encoder respectively to map them into a joint embedding space. The loss encourages the pose embedding y _ { i } and its caption embedding x _ { i } to be close in this latent space, while being pulled apart from features of other poses in the same training batch (e.g. yk and yl)*

![[assets/figures/papers/paper_list_l2_https_www_ecva_net_papers_eccv_2022_papers_ECCV_html_2069_ECCV_2022_pape/figures/008_Figure_7.jpg]]
*Figure 7: Retrieval results in image databases. We use our text-to-pose retrieval model trained on human captions from PoseScript to retrieve 3D poses from SMPL fits on MS Coco, for some given text queries. We display the corresponding pictures for the top retrieved poses, along with the bounding boxes around the pose*

![[assets/figures/papers/paper_list_l2_https_www_ecva_net_papers_eccv_2022_papers_ECCV_html_2069_ECCV_2022_pape/figures/012_Figure_10.jpg]]
*Figure 10: Example of potential application to SMPL fitting in images. Using the text-conditional pose prior (right) yields a more accurate 3D pose than a generic pose prior (left) when running the optimization-based SMPL fitting method SMPLify*

## 实验与分析

### 核心实验设置与评估协议

PoseScript的实验设计围绕两个核心应用场景展开：**文本到姿态检索**（Section 4）与**文本条件姿态生成**（Section 5）。两项任务均以PoseScript数据集为基础，该数据集包含从AMASS中通过最远点采样获取的20,000个3D人体姿态，每个姿态配有5条人工撰写的判别性描述（PoseScript-H）以及由自动描述流水线生成的结构化描述（PoseScript-A）。评估指标因任务而异：检索任务采用**平均召回率（mRecall）**，即文本查询到姿态（T→P）与姿态查询到文本（P→T）两个方向Recall@K（K=1,5,10）的均值；生成任务则综合使用**FID**（评估生成姿态的真实性）、**ELBO**（分别针对关节位置、顶点和旋转矩阵）以及基于检索模型的**mRecall**（评估生成姿态与输入文本的语义一致性）。

### 文本到姿态检索：自动描述预训练的关键作用

检索模型的核心结果汇总于Table 1。当仅在自动描述（PoseScript-A）上训练时，模型在自动描述测试集上达到了**69.1%的mRecall**，表明自动描述流水线生成的数据具有高度的内部一致性和可学习性。然而，当直接在人工描述（PoseScript-H）上训练时，mRecall骤降至**12.4%**。这一巨大差距揭示了核心瓶颈：人工描述具有丰富的语言多样性和表达自由度，远非自动描述的结构化模板所能覆盖，导致模型难以从有限的人工标注中学习到鲁棒的跨模态映射。

关键的因果干预在于**预训练策略**：先在自动描述上预训练，再在人工描述上微调，将mRecall从12.4%大幅提升至**30.4%**（提升+18.0个百分点）。这一结果表明，自动描述为模型提供了关于姿态语义结构的强先验知识，使其在接触少量人工描述时能够更有效地泛化。定性结果（Figure 6）进一步验证了该结论：微调后的模型能够准确检索到与复杂文本查询（如"the person is kneeling on one knee with the other foot forward and arms bent"）语义匹配的姿态，即使查询中包含自动描述中不常见的词汇组合。

![[assets/figures/papers/paper_list_l2_https_www_ecva_net_papers_eccv_2022_papers_ECCV_html_2069_ECCV_2022_pape/figures/007_Figure_6.jpg]]
*Figure 6: Text-to-pose retrieval results for human-written captions from the Pose-Script dataset. Directions such as ‘left’ and ‘right’ are relative to the body*

模型在MS Coco图像数据库上的跨域检索实验（Figure 7）展示了其实际应用潜力：给定文本查询，模型能够从大规模图像的SMPL拟合结果中检索到语义相关的3D姿态，无需任何图像级别的训练。

### 文本条件姿态生成：双重正则化与预训练的协同效应

生成模型基于条件VAE架构（Figure 8），其训练损失为：

![[assets/figures/papers/paper_list_l2_https_www_ecva_net_papers_eccv_2022_papers_ECCV_html_2069_ECCV_2022_pape/figures/009_Figure_8.jpg]]
*Figure 8: Overview of the text-conditioned generative model. During training, it follows a VAE but where the latent distribution $\mathcal { N } _ { p }$ from the pose encoder has a KL divergence term with the prior distribution $\mathcal { N } _ { c }$ given by the text encoder. At test time, the sample z is drawn from the distribution $\mathcal { N } _ { c }$

$$\mathcal{L} = \mathcal{L}_{R}(p, \hat{p}) + \mathcal{L}_{KL}(\mathcal{N}_{p}, \mathcal{N}_{c})$$

其中$\mathcal{N}_{p}$为姿态编码器输出的后验分布，$\mathcal{N}_{c}$为文本编码器给出的条件先验分布。

消融实验揭示了两个关键设计选择的影响（Table 2上半部分）。在自动描述上训练时，**添加额外正则化项**$\mathcal{L}_{KL}(\mathcal{N}_{p}, \mathcal{N}(0,I))$——即强制后验分布同时靠近标准高斯先验——改善了所有评估指标：FID从0.10降至**0.08**，mRecall R/G从24.7提升至**29.2**，mRecall G/R从14.4提升至**17.3**。这一额外KL散度项的作用机制在于：它防止文本条件先验过度坍缩到特定模式，从而增强了生成样本的多样性，同时保持了与文本条件的语义对齐。

在人工描述上的实验（Table 2下半部分）进一步证实了预训练的决定性作用。无预训练时，模型的mRecall G/R仅为**2.7**，表明生成的姿态几乎与输入文本无关。在自动描述上预训练后，mRecall G/R跃升至**16.2**（提升+13.5），FID从0.14改善至**0.11**。值得注意的是，即使经过微调，生成模型的mRecall（16.2）仍显著低于检索模型在相同数据上的表现（30.4），说明从文本直接生成精确的3D姿态比检索已有姿态更具挑战性。

### 失败模式与局限性分析

尽管预训练策略带来了显著提升，实验揭示了若干系统性的失败模式：

1. **语言多样性的覆盖不足**：自动描述基于模板生成，缺乏人类语言的自然变异性。当测试查询包含稀有词汇或非标准表达时，模型性能波动较大。这一点在人工描述测试集上mRecall仅为30.4%（远低于自动描述测试集的69.1%）中得到量化印证。

2. **复杂空间关系的歧义处理**：模型对涉及多肢体协调的复杂空间关系（如"arms crossed behind the back while leaning forward"）的理解能力有限。Figure 9的生成样本显示，部分生成姿态在局部关节角度上合理，但整体姿态结构可能与文本描述存在语义偏差。

3. **静态姿态的固有局限**：当前模型仅处理静态3D姿态，无法捕捉文本中隐含的动态信息（如"正在跑步"与"跑步姿势"的区分），这限制了其在动画生成等时序任务中的应用。

4. **数据集偏差**：人工描述由AMT标注者以英语撰写，可能引入文化和主观偏见。Figure 3的词云显示高频词汇集中在基本身体部位和方向词上，表明描述风格的集中化倾向。

### 开放问题与未来方向

实验结果为后续研究指明了若干方向：模型在完全未见过的描述上的泛化能力仍需系统评估；不同姿态表示（关节旋转、位置坐标、SMPL参数）对跨模态学习的影响尚待对比研究；将文本条件生成扩展到3D人体运动序列是自然的下一步；此外，利用生成的姿态作为中间表示来驱动文本到图像的3D可控生成，是一个具有应用价值但尚未探索的方向。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_www_ecva_net_papers_eccv_2022_papers_ECCV_html_2069_ECCV_2022_pape/figures/003_Figure_3.jpg]]
*Figure 3: Left: Interface presented to the AMT annotators in order to collect discriminative descriptions of the blue pose. Right: Wordcloud of the most frequent words in the human-written descriptions*

![[assets/figures/papers/paper_list_l2_https_www_ecva_net_papers_eccv_2022_papers_ECCV_html_2069_ECCV_2022_pape/figures/006_Table_1.jpg]]
*Table 1: Text-to-pose and pose-to-text retrieval results on the test split of the PoseScript dataset. For human-written captions (PoseScript-H), we evaluate models trained on each specific caption set alone, and one pretrained on automatic captions (PoseScript-A) then finetuned (FT) on human captions*

![[assets/figures/papers/paper_list_l2_https_www_ecva_net_papers_eccv_2022_papers_ECCV_html_2069_ECCV_2022_pape/figures/010_Table_2.jpg]]
*Table 2: Evaluation of the text-conditioned generative model on PoseScript-A for a model without or with $\mathcal { L } _ { K L } ( \mathcal { N } _ { p } , \mathcal { N } _ { 0 }$ ) (top) and on PoseScript-H without or with pretraining on PoseScript-A (bottom). For comparison, the mRecall when training and testing on real poses is 69.1 with PoseScript-A and 30.4 on PoseScript-H

![[assets/figures/papers/paper_list_l2_https_www_ecva_net_papers_eccv_2022_papers_ECCV_html_2069_ECCV_2022_pape/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of possible applications using PoseScript. The top figure illustrates text-to-pose retrieval where the goal is to retrieve poses in a large-scale database given a text query. This can be applied to databases of images with associated SMPL fits. The bottom figure shows an example of text-conditioned pose generation*

## 方法谱系与知识库定位

**PoseScript**（Delmas et al., ECCV 2022）的核心方法贡献在于一条从3D关键点到结构化自然语言描述的自动生成流水线，以及在此基础上的跨模态检索与文本条件姿态生成。其方法谱系可沿两条线索追溯：一是姿态语义的符号化表示，二是文本-姿态的跨模态学习。

### 姿态语义表示的演进

PoseScript的posecode体系直接继承自**posebits**（Pons-Moll et al., CVPR 2014）的语义姿态属性框架。posebits定义了角度、距离和相对位置三类基本关系，但粒度较粗，且未考虑俯仰/滚转和地面接触等对姿态理解至关重要的空间信息。PoseScript将posebits扩展为五类基本关系，并将连续值离散化为细粒度类别（如“膝盖轻微/相当/完全弯曲”），使得语义描述更接近人类语言的自然颗粒度。这种从“属性标签”到“可组合语义单元”的演进，使得自动描述生成成为可能。

在自动描述生成策略上，PoseScript采用了基于规则的聚合与转换方法，而非端到端的数据驱动生成。这一设计选择具有明确的适用边界：规则系统保证了描述的语义准确性和可控性，但牺牲了语言的自然多样性。与同期或后续基于大语言模型（LLM）的3D姿态描述方法相比，PoseScript的规则流水线不依赖外部语言模型，避免了幻觉问题，但也因此无法生成训练数据中未覆盖的词汇和表达方式。

### 跨模态检索与生成的方法定位

在文本-姿态检索任务上，PoseScript采用了经典的联合嵌入学习框架——文本编码器（bi-GRU + GloVe）与姿态编码器（VPoser）通过Batch-Based Classification（BBC）损失对齐。该架构与图像-文本检索中广泛使用的对比学习方法（如CLIP）处于同一谱系，但PoseScript的BBC损失引入了可学习温度参数γ，并在损失形式上更接近分类目标而非简单的InfoNCE。

在文本条件姿态生成上，PoseScript构建了一个条件VAE框架。其关键创新在于引入了双重KL正则化：后验分布不仅与文本条件先验对齐，还额外与标准高斯分布计算KL散度。这一设计（见Table 2顶部分）在自动描述上改善了所有指标（FID从0.10降至0.08，mRecall R/G从24.7升至29.2），表明额外的无信息先验正则化有助于防止后验坍缩，提升生成多样性。

### 预训练-微调范式的有效性

PoseScript最重要的方法论启示在于：**大规模自动生成数据预训练 + 少量人工标注数据微调**的两阶段策略显著提升了模型性能。在检索任务上，仅用人工描述训练时mRecall仅为12.4%，而在自动描述上预训练后微调提升至30.4%（Table 1）。在生成任务上，预训练将mRecall G/R从2.7提升至16.2，FID从0.14改善至0.11（Table 2底部）。这一结果表明，自动描述流水线虽然语言质量不及人工标注，但其覆盖的语义空间足够支撑有效的表征学习，为后续在高质量数据上的适配提供了良好的初始化。

### 适用边界与局限

1. **语言多样性的上限**：自动描述生成的随机性仅体现在posecode选择跳过的随机化和聚合规则的条件随机应用上，本质上仍是模板填充。对于稀有词汇和非常规表达，模型方差较大，泛化能力受限。

2. **静态姿态的限定**：当前工作仅处理单帧3D人体姿态，未扩展到运动序列。这使得方法无法直接应用于动作描述（如“从蹲姿站起”）或时序相关的文本-运动任务。

3. **语言与文化的单一性**：数据集仅包含英语描述，AMT标注过程可能引入英语母语者的文化和主观偏见，跨语言泛化能力未经验证。

4. **空间关系的理解深度**：posecode体系对“左/右”等方向性关系有良好覆盖，但对更复杂的空间关系（如“手臂在头部后方交叉”）和多义词的理解有限，这限制了模型在未见过的复杂描述上的表现。

### 开放问题

- 自动描述流水线能否适配其他人体模型（如SMPL-X）或非人形骨架？posecode的定义依赖于关节集合的语义分组，扩展到不同拓扑结构需要重新设计关系模板。
- 文本条件姿态生成能否扩展为文本条件运动生成？这需要处理时序依赖和动作过渡的语义建模。
- 生成的3D姿态能否作为条件信号驱动图像生成模型，实现文本到图像的可控3D人体合成？Figure 10展示了文本条件姿态先验在SMPLify优化中的初步应用，但端到端的生成式应用仍有待探索。
- 不同姿态表示（关节旋转、3D位置、SMPL参数）对跨模态检索性能的系统性影响尚未量化比较，这对下游任务中的表示选择具有实际指导意义。

## 原文 PDF

![[paperPDFs/ECCV_2022/PoseScript_3D_Human_Poses_from_Natural_Language.pdf]]