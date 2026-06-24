---
title: "Beyond Global Alignment: Fine-Grained Motion-Language Retrieval via Pyramidal Shapley-Taylor Learning"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval_via_Pyramidal_Shapley_Taylor_Learning.pdf
aliases:
- PSTPLF
- BGAFGMLRPSTL
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 引入Shapley-Taylor Interaction (STI) 量化跨模态元素对的交互强度，并结合金字塔式建模方案，从关节级、片段级到整体级逐步建立细粒度对齐。
primary_logic: 受人类运动感知的金字塔过程启发，通过STI捕捉随着上下文增加时元素对的边际贡献，并在不同语义层次间施加自蒸馏，实现从局部细节到整体语义的连贯跨模态对齐。
claims:
- 在HumanML3D数据集上，Small batches协议下文本到动作R@1达到71.61%，远超现有最佳方法（MotionPatch为10.80%，Lyu et al.为11.80%）。
- 在KIT-ML数据集上，Small batches协议下文本到动作R@1为56.83%，动作到文本R@1为57.14%，均显著优于对比方法。
- 消融实验中，加入STI蒸馏损失和自蒸馏损失均一致提升召回率，验证了细粒度交互建模与层级自蒸馏的必要性。
- HumanML3D 上 R@1 (文本→动作) = 12.45 (All) / 71.61 (Small)
---

# Beyond Global Alignment: Fine-Grained Motion-Language Retrieval via Pyramidal Shapley-Taylor Learning

> [!tip] 核心洞察
> 受人类运动感知的金字塔过程启发，通过STI捕捉随着上下文增加时元素对的边际贡献，并在不同语义层次间施加自蒸馏，实现从局部细节到整体语义的连贯跨模态对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | 超越全局对齐：基于金字塔Shapley-Taylor学习的细粒度动作-语言检索 |
| 英文题名 | Beyond Global Alignment: Fine-Grained Motion-Language Retrieval via Pyramidal Shapley-Taylor Learning |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2601.21904) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | Pyramidal Shapley-Taylor (PST) Learning Framework |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，R@1 (文本→动作) 12.45 (All) / 71.61 (Small) vs MotionPatch: 10.80 (All) / -- (Small) (+1.65 (All))；R@1 (动作→文本) 13.59 (All) / 75.12 (Small) vs MotionPatch: 11.25 (All) / -- (Small) (+2.34 (All))。
> - KIT-ML 上，R@1 (文本→动作) 16.01 (All) / 56.83 (Small) vs Lyu et al. 2025: 15.13 (All) / 53.55 (Small) (+0.88 (All) / +3.28 (Small))；MedR (文本→动作) 7.00 (All) / 1.28 (Small) vs Lyu et al. 2025: 8.00 (All) / 1.36 (Small) (-1.00 (All) / -0.08 (Small))。

## 概述

### 问题瓶颈

现有动作-语言检索方法普遍依赖**全局对齐**策略，即将整段动作序列与完整文本描述映射到共享空间后计算余弦相似度。这类方法忽略了动作序列内部丰富的局部结构——包括不同**时间片段**的语义差异以及不同**身体关节**与文本词元之间的细粒度对应关系。当查询涉及“先慢跑、再停下、然后摆出侧身格斗姿势”这类多阶段动作时，全局表示难以捕捉各子动作与对应文本片段之间的精确关联，导致检索性能处于次优水平。

### 核心方法

本文提出**金字塔式Shapley-Taylor学习框架（Pyramidal Shapley-Taylor, PST）**，受人类运动感知的金字塔过程启发，从三个语义层次逐步建立跨模态细粒度对齐：

- **关节级对齐**：在空间维度上，将人体运动分解为各身体关节的独立运动标记，与文本词元进行逐对交互建模。
- **片段级对齐**：在时间维度上，通过注意力引导的标记压缩模块将关节级标记聚合为语义更完整的运动片段标记。
- **整体级对齐**：在全局层面保留序列级表示，确保整体语义一致性。

框架的核心机制是**Shapley-Taylor交互（STI）**，用于量化任意文本-动作标记对在随机上下文子集中的**边际贡献**——即当一对标记被加入某个随机前缀子集时，模型预测分数的期望增量。STI值越高，表示该标记对在跨模态语义关联中越关键。为高效估计STI，框架引入一个轻量级**STI估计头**，并通过KL散度将标准STI分布蒸馏到估计分布中。同时，框架施加**层级自蒸馏损失**，用关节级的相似度分布指导片段级分布，确保从局部细节到整体语义的连贯对齐。

### 方法谱系与知识库定位

在动作-语言检索领域，现有方法可大致分为两类：

- **基于全局对齐的方法**：如**TEMOS**（Petrovich et al., ECCV 2022）、**T2M**（Guo et al., 2022）和**TMR**（Petrovich et al., ICCV 2023），它们使用对比损失将整个动作序列与文本描述对齐，但缺乏对局部结构的显式建模。
- **引入局部结构的方法**：如**MotionPatch**（Yu et al., CVPR 2024）使用ViT将人体划分为身体部位补丁进行处理，以及**Lyu et al.（2025）**采用词法化表示增强动作编码。这些方法开始关注局部信息，但尚未建立系统化的多层次对齐机制。

PST框架在以下维度实现了差异化定位：

| 设计维度 | 基线方法 | PST框架 |
|---------|---------|---------|
| 对齐粒度 | 全局对齐（整个序列与文本） | 金字塔式三层对齐：关节级、片段级、整体级 |
| 跨模态交互建模 | 余弦相似度/对比损失 | 基于STI的边际贡献衡量与蒸馏 |
| 训练目标 | 仅全局对比损失（InfoNCE） | 三层对比损失 + STI蒸馏损失 + 层级自蒸馏损失 |

### 主要结果概览

在两个公开基准数据集上的实验验证了PST框架的有效性：

- **HumanML3D数据集**（Table 1）：在Small batches协议下，文本到动作的R@1达到**71.61%**，远超现有最佳方法MotionPatch的10.80%和Lyu et al.的11.80%；在All batches协议下，文本到动作R@1为12.45%，动作到文本R@1为13.59%，分别比MotionPatch提升1.65和2.34个百分点。
- **KIT-ML数据集**（Table 2）：在Small batches协议下，文本到动作R@1为**56.83%**，动作到文本R@1为57.14%，均显著优于对比方法；MedR指标同样取得领先。
- **消融实验**（Table 3, Table 4）：加入STI蒸馏损失和自蒸馏损失均一致提升召回率，验证了细粒度交互建模与层级语义约束的必要性。压缩比设为0.25时性能最优。

### 局限与开放问题

当前方法面临的主要局限包括：（1）数据集文本描述多为整体性动作，缺乏细粒度部位描述，导致文本与动作模态间存在结构性不对齐；（2）模型对复杂或罕见动作的细粒度对齐仍存在局部偏差；（3）STI估计头依赖特定数据集训练，迁移到全新领域时可能需要额外微调。

值得进一步探索的开放问题包括：如何设计更优的文本模态结构先验以弥合模态差距；能否将金字塔式对齐框架推广到开放词汇或大规模动作-语言理解任务；以及如何通过改进的注意力或正则化技术缓解局部偏差问题。

## 背景与动机

### 任务定义与现有范式

动作-语言检索旨在根据自然语言描述从数据库中检索相应的三维人体动作序列，反之亦然。该任务的核心挑战在于弥合视觉运动模态与文本语义模态之间的异质性鸿沟。现有主流方法——包括 **TEMOS**（Petrovich et al., ECCV 2022）、**T2M**（Guo et al., 2022）以及 **TMR**（Petrovich et al., ICCV 2023）——普遍采用全局对齐范式：将整个动作序列编码为单一嵌入，将文本描述编码为单一嵌入，然后通过余弦相似度或InfoNCE对比损失在嵌入空间中对齐二者。

近年来，研究者开始尝试引入更细粒度的表示以突破全局对齐的局限。**MotionPatch**（Yu et al., CVPR 2024）将人体划分为多个身体部位补丁，利用ViT架构提取部位级特征；Lyu et al.（2025）则提出词法化动作表示。然而，这些方法在建模跨模态元素之间的交互时，仍主要依赖全局相似度度量，未能系统性地捕捉局部动作片段、身体关节与文本标记之间的细粒度对应关系。

### 核心瓶颈：全局对齐的局限性

经验证据表明，全局对齐范式存在根本性缺陷。在HumanML3D数据集上的Small batches协议下，现有最强方法的文本到动作R@1仅约11%（MotionPatch为10.80%，Lyu et al.为11.80%），而本文方法达到71.61%（Table 1）。这一巨大差距揭示了核心瓶颈：**现有方法忽略了动作序列与文本描述在局部粒度上的交互结构**。

具体而言，一个动作描述如“一个人慢跑向前，停下，然后摆出侧向格斗姿势”包含多个时序阶段和空间部位信息，但全局对齐将其压缩为单一向量，丢失了“慢跑”与腿部运动、“格斗姿势”与上肢姿态之间的细粒度关联。这种信息压缩导致两个关键问题：

1. **局部语义错配**：全局嵌入可能因主导性动作片段而掩盖细节动作，造成检索结果在局部动作上不准确。
2. **模态间结构不对齐**：文本天然具有时序和语义结构，而动作序列具有时空结构，全局对齐无法利用这些结构先验进行约束。

### 动机：金字塔式感知与交互建模

人类对动作的感知遵循金字塔式过程：先感知整体动作类型，再关注时序片段，最后聚焦于具体身体关节的运动细节。受此启发，本文提出**金字塔式Shapley-Taylor（Pyramidal Shapley-Taylor, PST）学习框架**，在两个关键维度上突破全局对齐的局限：

1. **细粒度交互量化**：引入Shapley-Taylor Interaction（STI），一种源于合作博弈论的边际贡献度量。STI通过计算在随机上下文前缀下文本-动作标记对的预期边际贡献，量化跨模态元素对之间的交互强度。相比简单的余弦相似度，STI能够捕捉到随着上下文增加时元素对交互的非线性变化，从而识别出真正具有语义耦合的细粒度配对。

2. **金字塔式多层对齐**：将动作序列分解为三个语义层次——关节级（joint-wise）、片段级（segment-wise）和整体级（holistic）——并在每一层建立跨模态对齐。关节级对齐捕捉身体部位与文本词的细粒度对应；片段级对齐通过注意力引导的标记压缩模块将关节级信息聚合为时序片段表示；整体级对齐保留全局语义。三层之间通过自蒸馏损失保持语义一致性，形成从局部细节到整体语义的连贯对齐链路。

这一设计使得模型不仅能够进行传统的全局检索，还能在关节和片段粒度上提供可解释的对齐证据，为细粒度动作理解奠定了基础。

## 核心创新

### 问题瓶颈：从全局对齐到细粒度交互缺失

现有动作-语言检索方法的核心范式是将整段动作序列与整句文本描述映射到共享嵌入空间，通过全局余弦相似度或对比损失进行对齐。这一范式忽略了两个关键事实：(1) 人体动作天然具有时空层次结构——从身体关节、动作片段到整体序列；(2) 文本描述中不同词汇往往对应动作的不同时空局部。因此，全局对齐无法捕捉“关节-词汇”“片段-短语”层级的细粒度对应关系，导致检索性能次优，尤其在需要区分局部细节的场景下表现乏力。

### 因果调控变量：Shapley-Taylor Interaction (STI)

针对上述瓶颈，本文引入**Shapley-Taylor Interaction (STI)** 作为核心因果调控变量。STI 是合作博弈论中 Shapley 值的推广，用于量化多个输入单元之间的交互强度。在本任务中，STI 被设定为二阶交互（k=2），用于计算任意文本标记 $t_i$ 与动作标记 $m_j$ 组成的元素对 $(e_i^{\mathrm{t}}, e_j^{\mathrm{m}})$ 的**预期边际贡献**：

$$\phi(e_i^{\mathrm{t}}, e_j^{\mathrm{m}}) = \mathbb{E}_{\boldsymbol\pi} \Big[ F(S_{\boldsymbol\pi} \cup \{e_i^{\mathrm{t}}, e_j^{\mathrm{m}}\}) - F(S_{\boldsymbol\pi} \cup \{e_i^{\mathrm{t}}\}) - F(S_{\boldsymbol\pi} \cup \{e_j^{\mathrm{m}}\}) + F(S_{\boldsymbol\pi}) \Big]$$

其中 $S_{\boldsymbol\pi}$ 为随机排列 $\boldsymbol\pi$ 下的前缀子集，$F$ 为相似度评分函数。该公式的直觉含义是：在随机上下文子集上，同时加入文本标记和动作标记所带来的边际增益，减去分别单独加入的增益，即二者独有的协同交互强度。为突出短上下文中的局部交互，前缀长度 $\ell$ 的概率分布设计为偏向短前缀：

$$\mathbb{P}(L = \ell) = \frac{2(K - \ell - 1)}{K(K - 1)}, \quad \ell = 0, 1, \dots, K-2$$

这一设计使得 STI 能够捕捉随着上下文逐渐丰富时元素对交互强度的变化，从而为细粒度对齐提供精确的量化信号。

### 核心洞察：金字塔式建模与自蒸馏

受人类运动感知的金字塔过程启发——从局部关节运动到整体动作语义的逐步抽象——本文提出**金字塔式建模方案**，将动作和文本分别组织为三个语义层次：

| 层次 | 动作侧 | 文本侧 | 对齐粒度 |
|------|--------|--------|----------|
| 关节级 (joint-wise) | 身体关节点/部位标记 | 词级标记 | 细粒度局部 |
| 片段级 (segment-wise) | 时间片段标记 | 短语级标记 | 中等粒度 |
| 整体级 (holistic) | 全局动作嵌入 | 全局文本嵌入 | 粗粒度全局 |

关键创新在于**层级自蒸馏机制**：利用关节级的细粒度相似度分布作为教师信号，通过 KL 散度蒸馏指导片段级的相似度分布：

$$\mathcal{L}_{\mathrm{D}} = \mathrm{KL}(\mathcal{D}_{\mathrm{m2t}}^{\mathrm{sgm}} \parallel \mathcal{D}_{\mathrm{m2t}}^{\mathrm{jnt}}) + \mathrm{KL}(\mathcal{D}_{\mathrm{t2m}}^{\mathrm{sgm}} \parallel \mathcal{D}_{\mathrm{t2m}}^{\mathrm{jnt}})$$

这一约束确保从局部细节到中层语义的连贯性，避免片段级对齐丢失关节级的精细信息。同时，标准 STI 分布与轻量级 STI 估计头预测分布之间的 KL 散度构成 STI 蒸馏损失 $\mathcal{L}_{\mathrm{SD}}$，使得网络无需在推理时计算昂贵的 STI 精确值，即可保持细粒度交互建模能力。

### 与基线方法的差异维度

相较于现有方法，本文在三个关键维度上实现了根本性改变：

1. **对齐粒度**：从单一全局对齐（**TEMOS** (Petrovich et al., ECCV 2022)、**T2M** (Guo et al., 2022)、**TMR** (Petrovich et al., ICCV 2023)）扩展为关节-片段-整体三层金字塔对齐。即使是最新的 **MotionPatch** (Yu et al., CVPR 2024) 虽然使用 ViT 处理身体部位补丁，仍停留在全局对齐层面。

2. **跨模态交互建模**：从简单的余弦相似度/对比损失升级为基于 STI 的边际贡献量化与蒸馏。STI 不仅衡量“是否相似”，更衡量“在给定上下文中，这对元素带来了多少额外的语义匹配增益”。

3. **训练目标**：从仅使用全局 InfoNCE 对比损失扩展为三层对比损失 + STI 蒸馏损失 + 层级自蒸馏损失的复合目标：

$$\mathcal{L} = \mathcal{L}_{\mathrm{C}}^{\mathrm{jnt}} + \mathcal{L}_{\mathrm{C}}^{\mathrm{sgm}} + \mathcal{L}_{\mathrm{C}}^{\mathrm{hl}t} + \lambda_{\mathrm{S}}(\mathcal{L}_{\mathrm{SD}}^{\mathrm{jnt}} + \mathcal{L}_{\mathrm{SD}}^{\mathrm{sgm}}) + \lambda_{\mathrm{D}}\mathcal{L}_{\mathrm{D}}$$

其中 $\mathcal{L}_{\mathrm{C}}^{*}$ 为各层级的对比损失，$\lambda_{\mathrm{S}}$ 和 $\lambda_{\mathrm{D}}$ 为平衡超参数。

### 证据强度与边界

**决定性证据**：在 HumanML3D 数据集 Small batches 协议下，文本到动作 R@1 达到 71.61%，远超同期最佳方法（MotionPatch 为 10.80%，Lyu et al. 为 11.80%），动作到文本 R@1 达到 75.12%（Table 1）。在 KIT-ML 上同样取得一致领先（Table 2）。消融实验（Table 3, Table 4）证实，加入 $\mathcal{L}_{\mathrm{SD}}$ 和 $\mathcal{L}_{\mathrm{D}}$ 均一致提升召回率，验证了 STI 蒸馏和自蒸馏的必要性。

**需注意的边界**：(1) 数据集文本描述多为整体性动作，缺乏细粒度部位描述，导致文本与动作模态间存在结构性不对齐，限制了细粒度对齐潜力的充分发挥；(2) 在复杂或罕见动作上，关节级和片段级对齐可视化仍观察到局部偏差；(3) STI 估计头依赖特定数据集训练，迁移到全新领域时可能需要额外微调。这些边界条件提示，方法的细粒度优势在当前数据生态下尚未完全释放，未来需结合更丰富的文本标注或 LLM 驱动的文本增强来弥合模态差距。

## 整体框架

Pyramidal Shapley-Taylor (PST) 学习框架旨在建立动作与语言之间的细粒度跨模态对齐。如图 1 所示，框架由两条并行的编码支路和三层金字塔对齐结构组成。

**输入与编码。** 文本端采用 **DistilBERT** 作为文本编码器，将自然语言描述转化为文本标记嵌入序列 $\boldsymbol{\mathcal{E}}_T(t_i)$。动作端受 **MotionPatch**（Yu et al., CVPR 2024）启发，使用基于 ViT 的动作编码器处理空间结构化的运动输入，提取关节级运动标记嵌入 $\boldsymbol{\mathcal{E}}_M(m_j)$。两个编码器输出的标记嵌入构成后续所有对齐操作的基础。

**金字塔三层对齐。** 框架的核心是自底向上的三层对齐结构，模拟人类运动感知从局部到整体的金字塔过程：

1. **关节级对齐（Joint-wise Alignment）：** 在原始标记粒度上，对每个文本标记与每个动作关节标记计算跨模态交互强度。这一层捕捉最细粒度的语义对应关系，例如“jog”与腿部关节运动的关联。

2. **片段级对齐（Segment-wise Alignment）：** 通过 **Token Compressor**（注意力引导的标记压缩模块，见图 6b）将关节级标记压缩为更高语义层次的片段级标记。压缩模块使用卷积、自注意力和 KNN-DPC 聚类，压缩比 $\rho_* = N_*^{\text{sgm}} / N_*^{\text{jnt}}$ 设为 0.25。片段级对齐在压缩后的表示上进行，捕捉动作子序列与文本短语之间的中层语义对应。

3. **整体级对齐（Holistic Alignment）：** 在全局池化后的序列级表示上执行标准的跨模态对比学习，保持与现有方法兼容的全局语义对齐。

**Shapley-Taylor 交互建模。** 在关节级和片段级，框架引入 **Shapley-Taylor Interaction (STI)** 量化跨模态元素对的交互强度。STI 通过计算文本-动作标记对在不同上下文前缀下的预期边际贡献（见 Eq. 2），生成标准 STI 分布 $\mathcal{D}^{\phi}$。为降低计算开销，框架使用轻量级 **STI Estimation Head**（图 6a）近似估计 STI 值，并通过 KL 散度将估计分布 $\mathcal{D}^{\mathcal{H}}$ 向标准分布蒸馏（STI 蒸馏损失 $\mathcal{L}_{\text{SD}}$，见 Eq. 6）。

**层级自蒸馏。** 为保持金字塔各层之间的语义一致性，框架引入自蒸馏损失 $\mathcal{L}_{\text{D}}$（见 Eq. 9），用关节级的相似度分布指导片段级分布，防止压缩过程中细粒度语义信息的丢失。

**训练目标。** 总损失函数（见 Eq. 10）联合优化三层对比损失、STI 蒸馏损失和层级自蒸馏损失：
$$\mathcal{L} = \mathcal{L}_{\text{C}}^{\text{jnt}} + \mathcal{L}_{\text{C}}^{\text{sgm}} + \mathcal{L}_{\text{C}}^{\text{hlt}} + \lambda_{\text{S}} (\mathcal{L}_{\text{SD}}^{\text{jnt}} + \mathcal{L}_{\text{SD}}^{\text{sgm}}) + \lambda_{\text{D}} \mathcal{L}_{\text{D}}$$

其中 $\mathcal{L}_{\text{C}}$ 为基于 InfoNCE 的对比损失，$\lambda_{\text{S}}$ 和 $\lambda_{\text{D}}$ 为平衡超参数。

### 补充图表

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2601_21904/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our Pyramidal Shapley-Taylor (PST) learning framework. Our PST learning framework consists of Shapley-Taylor Interaction (STI), described in Sec. 3.2, and pyramidal modeling scheme, described in Sec. 3.3. As illustrated in the middle cube, each cell represents the interaction strength between a motion token and a text token within a batch, where darker colors indicate stronger semantic correlations, and lighter colors represent weaker ones*

## 核心模块与公式推导

### 3.1 跨模态标记相似度基础

给定文本标记 $t_i$ 和动作标记 $m_j$，其编码器输出嵌入分别为 $\boldsymbol{\mathcal{E}}_T(t_i)$ 和 $\boldsymbol{\mathcal{E}}_M(m_j)$。基础相似度函数采用余弦相似度：

$$s(t_i, m_j) = \frac{\boldsymbol{\mathcal{E}}_T(t_i) \cdot \boldsymbol{\mathcal{E}}_M(m_j)}{\|\boldsymbol{\mathcal{E}}_T(t_i)\| \|\boldsymbol{\mathcal{E}}_M(m_j)\|}$$

该相似度作为后续 Shapley-Taylor 交互值计算和对比损失的基础度量。

### 3.2 Shapley-Taylor 交互模块

**核心思想**：将跨模态元素对的交互强度量化为其在不同上下文子集下的边际贡献期望。框架采用 $k=2$ 的 Shapley-Taylor Interaction (STI)，衡量文本标记 $e_i^{\mathrm{t}}$ 与动作标记 $e_j^{\mathrm{m}}$ 的成对交互值：

$$\phi(e_i^{\mathrm{t}}, e_j^{\mathrm{m}}) = \mathbb{E}_{\boldsymbol{\pi}} \Big[ F(S_{\boldsymbol{\pi}} \cup \{e_i^{\mathrm{t}}, e_j^{\mathrm{m}}\}) - F(S_{\boldsymbol{\pi}} \cup \{e_i^{\mathrm{t}}\}) - F(S_{\boldsymbol{\pi}} \cup \{e_j^{\mathrm{m}}\}) + F(S_{\boldsymbol{\pi}}) \Big]$$

其中 $\boldsymbol{\pi}$ 为随机排列，$S_{\boldsymbol{\pi}}$ 为排列中位于该对之前的元素子集（前缀），$F(\cdot)$ 为基于相似度的集合价值函数。前缀长度 $\ell$ 的采样分布为：

$$\mathbb{P}(L = \ell) = \frac{2(K - \ell - 1)}{K(K - 1)}, \quad \ell = 0, 1, \dots, K - 2$$

该分布赋予较短前缀更大权重，使模型更关注局部上下文下的交互贡献。

**STI 估计头**：由于精确计算 STI 值需要枚举所有排列，计算代价高昂，框架引入轻量级 STI Estimation Head $\mathcal{H}$（结构见 Figure 6a）。该模块以动作标记 $m_j$ 和文本标记 $t_i$ 为输入，通过卷积和自注意力操作输出估计值 $p_{i,j}^{\mathcal{H}}$ 和 $\hat{p}_{i,j}^{\mathcal{H}}$，分别构成动作→文本分布 $\mathcal{D}_{\mathrm{m2t}}^{\mathcal{H}}$ 和文本→动作分布 $\mathcal{D}_{\mathrm{t2m}}^{\mathcal{H}}$。标准 STI 分布 $\mathcal{D}^{\phi}$ 与估计分布之间的 KL 散度构成 STI 蒸馏损失：

$$\mathcal{L}_{\mathrm{SD}} = \mathrm{KL}\left( \mathcal{D}_{\mathrm{m2t}}^{\phi} \parallel \mathcal{D}_{\mathrm{m2t}}^{\mathcal{H}} \right) + \mathrm{KL}\left( \mathcal{D}_{\mathrm{t2m}}^{\phi} \parallel \mathcal{D}_{\mathrm{t2m}}^{\mathcal{H}} \right)$$

该损失将精确 STI 的细粒度交互知识蒸馏到可高效计算的估计头中。

### 3.3 金字塔式建模方案

框架模拟人类运动感知的层次化过程，建立三层对齐结构：

- **关节级**：保留原始动作标记，捕捉身体关节与文本标记的细粒度对应。
- **片段级**：通过 Token Compressor（结构见 Figure 6b）将关节级标记压缩为片段级标记。压缩器使用卷积、自注意力和 KNN-DPC 聚类，压缩比 $\rho_* = N_*^{\mathrm{sgm}} / N_*^{\mathrm{jnt}}$ 设为 0.25（$* \in \{m, t\}$）。
- **整体级**：对片段级标记进行平均池化，获得全局表示。

### 3.4 训练目标

**投影头与相似度**：在计算对比损失前，使用投影头 $\mathrm{PH}(\cdot)$（两层前馈网络，含 GeLU 激活）将嵌入映射为标量分数，修正相似度函数：

$$s(t_i, m_j) = \frac{\mathrm{PH}(\boldsymbol{\mathcal{E}}_T(t_i)) \cdot \mathrm{PH}(\boldsymbol{\mathcal{E}}_M(m_j))}{\|\mathrm{PH}(\boldsymbol{\mathcal{E}}_T(t_i))\| \|\mathrm{PH}(\boldsymbol{\mathcal{E}}_M(m_j))\|}$$

**三层对比损失**：在关节级、片段级和整体级分别应用 InfoNCE 对比损失 $\mathcal{L}_{\mathrm{C}}^{\mathrm{jnt}}$、$\mathcal{L}_{\mathrm{C}}^{\mathrm{sgm}}$、$\mathcal{L}_{\mathrm{C}}^{\mathrm{hlt}}$，每层包含文本→动作和动作→文本两个方向。

**自蒸馏损失**：为保持层级间语义一致性，用关节级相似度分布指导片段级分布：

$$\mathcal{L}_{\mathrm{D}} = \mathrm{KL}( \mathcal{D}_{\mathrm{m2t}}^{\mathrm{sgm}} \parallel \mathcal{D}_{\mathrm{m2t}}^{\mathrm{jnt}} ) + \mathrm{KL}( \mathcal{D}_{\mathrm{t2m}}^{\mathrm{sgm}} \parallel \mathcal{D}_{\mathrm{t2m}}^{\mathrm{jnt}} )$$

**总损失**：

$$\mathcal{L} = \mathcal{L}_{\mathrm{C}}^{\mathrm{jnt}} + \mathcal{L}_{\mathrm{C}}^{\mathrm{sgm}} + \mathcal{L}_{\mathrm{C}}^{\mathrm{hlt}} + \lambda_{\mathrm{S}} (\mathcal{L}_{\mathrm{SD}}^{\mathrm{jnt}} + \mathcal{L}_{\mathrm{SD}}^{\mathrm{sgm}}) + \lambda_{\mathrm{D}} \mathcal{L}_{\mathrm{D}}$$

其中 $\lambda_{\mathrm{S}}$ 和 $\lambda_{\mathrm{D}}$ 为损失权重。消融实验（Table 3, Table 4）表明，加入 STI 蒸馏损失和自蒸馏损失均一致提升召回率，但过高权重会导致过拟合。

### 补充图表

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2601_21904/figures/002_Figure_2.jpg]]
*Figure 2: An intuitive illustration of the STI*

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2601_21904/figures/010_Figure_6.jpg]]
*Figure 6: Detailed architecture. (a) Structure of the STI Estimation Head. (b) Structure of the Token Compressor*

## 实验与分析

### 主要结果

在 HumanML3D 和 KIT-ML 两个公开基准数据集上，PST 学习框架在 All batches 和 Small batches 两种评估协议下均取得了领先的检索性能。

**HumanML3D 数据集**（Table 1）。在文本到动作检索任务上，PST 在 All 协议下 R@1 达到 12.45%，较最强基线 MotionPatch（Yu et al., CVPR 2024）的 10.80% 提升 1.65 个百分点；在 Small batches 协议下，R@1 跃升至 71.61%，远超 Lyu et al.（2025）的 11.80%。在动作到文本检索任务上，PST 同样保持优势，All 协议 R@1 为 13.59%（MotionPatch 为 11.25%），Small batches 协议 R@1 达到 75.12%。值得注意的是，Small batches 协议下 PST 的 MedR 降至 1.00，意味着检索结果几乎总在第一位命中，验证了细粒度对齐对缩小候选空间的关键作用。

**KIT-ML 数据集**（Table 2）。PST 在文本到动作检索上 All 协议 R@1 为 16.01%，MedR 为 7.00，均优于 Lyu et al.（2025）的 15.13% 和 8.00。Small batches 协议下优势更为明显，文本到动作 R@1 达 56.83%（对比 53.55%），动作到文本 R@1 达 57.14%（对比 54.09%）。KIT-ML 数据集规模较小且描述相对简单，PST 在 MedR 上的增益（All 协议从 8.00 降至 7.00）表明细粒度建模在数据稀疏场景下仍能稳定贡献。

**公平性说明**。所有对比均采用与先前工作一致的评估协议、数据集划分和评价指标（R@k、MedR）。动作编码器沿用 MotionPatch 的 ViT 架构，文本编码器采用 DistilBERT，确保性能增益归因于 PST 学习框架本身而非编码器差异。

### 消融实验

为验证各模块的独立贡献，论文在 HumanML3D（Table 3）和 KIT-ML（Table 4）上进行了系统消融。

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2601_21904/figures/005_Table_3.jpg]]
*Table 3: Ablation on HumanML3D*

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2601_21904/figures/006_Table_4.jpg]]
*Table 4: Ablation on KIT-ML*

**STI 蒸馏损失（L_SD）的有效性**。移除 L_SD 后，两个数据集上所有检索指标均出现一致下降。在 HumanML3D Small batches 协议下，文本到动作 R@1 从 71.61% 降至约 69%，动作到文本 R@1 从 75.12% 降至约 72%。这一结果表明，基于 Shapley-Taylor 相互作用的细粒度跨模态交互建模是性能提升的核心驱动力，单纯依赖全局对比损失无法捕捉关节级和片段级的语义对应。

**自蒸馏损失（L_D）的必要性**。进一步移除层级自蒸馏损失 L_D 后，性能继续下降。L_D 的作用是强制关节级相似度分布指导片段级分布，维持金字塔层级间的语义一致性。消融结果验证了该约束的有效性：缺乏自蒸馏时，片段级对齐可能偏离关节级已建立的细粒度对应，导致整体检索精度受损。

**超参数敏感性**。损失权重 λ_S 和 λ_D 的扫描实验表明，过高的权重会导致过拟合，性能反而下降。压缩比 ρ 设为 0.25 时性能最优——该值在关节级和片段级标记数量之间取得平衡：压缩比过低会导致片段级表示丢失关键信息，过高则退化为粗粒度对齐，无法发挥金字塔建模优势。

### LLM 驱动的文本增强

针对数据集中文本描述多为整体性动作、缺乏细粒度部位描述的结构性不对齐问题，论文探索了利用大语言模型（LLM）对文本进行增强的策略。Table 5 的结果显示，在 HumanML3D 上引入 LLM 生成的部位级描述后，PST 的检索性能进一步提升，表明更丰富的文本模态先验有助于释放细粒度对齐框架的潜力。然而，该方法在 KIT-ML 等描述更简单的数据集上的可扩展性仍需进一步验证。

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2601_21904/figures/015_Table_5.jpg]]
*Table 5: Motion-to-text and text-to-motion retrieval results on HumanML3D with LLM-driven text enhancement*

### 可视化分析

定性可视化（Figure 3-5, Figure 7-10）展示了 PST 在片段级和关节级的对齐能力。片段级可视化（Figure 3）显示，模型能够将文本中的动作短语（如“jogs forward”、“stops”）与动作序列的对应时间片段准确关联。关节级可视化（Figure 4）通过相似度热力图揭示了身体部位与文本标记之间的细粒度对应关系。但在复杂或罕见动作上，可视化结果仍存在局部偏差，表明模型对长尾动作的细粒度对齐能力尚有提升空间。

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2601_21904/figures/007_Figure_3.jpg]]
*Figure 3: Visualization results of segment-wise alignment. We omit \<EOS> for clarity and use commas to separate each individual word*

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2601_21904/figures/009_Figure_4.jpg]]
*Figure 4: Visualization results of joint-wise alignment. Darker colors indicate higher similarity scores*

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2601_21904/figures/011_Figure_7.jpg]]
*Figure 7: Visualization results for text description “a person jogs forward, stops and gets into a sideways fighting stance.”*

### 补充图表

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2601_21904/figures/003_Table_1.jpg]]
*Table 1: Motion-to-text and text-to-motion retrieval results on HumanML3D*

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2601_21904/figures/004_Table_2.jpg]]
*Table 2: Motion-to-text and text-to-motion retrieval results on KIT-ML*

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2601_21904/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative results of text-to-motion retrieval*

## 方法谱系与知识库定位

### 与现有工作的关系

本文提出的**金字塔Shapley-Taylor（PST）学习框架**直接回应了动作-语言检索领域的一个核心瓶颈：现有方法主要依赖动作序列与文本的全局对齐，忽略了局部动作片段、身体关节与文本标记之间的细粒度交互。PST框架在以下三个关键维度上对现有方法进行了系统性改进：

**对齐粒度的跃升。** 传统方法如**TEMOS**（Petrovich et al., ECCV 2022）、**T2M**（Guo et al., 2022）和**TMR**（Petrovich et al., ICCV 2023）均采用“整个序列↔整句文本”的全局对齐策略，仅通过余弦相似度或InfoNCE对比损失优化跨模态匹配。PST框架则将对齐过程分解为三层金字塔结构：关节级（joint-wise）、片段级（segment-wise）和整体级（holistic），模拟人类运动感知从局部细节到全局语义的递进过程。这种设计使模型能够显式捕捉“手部动作↔抓取”“脚步↔行走方向”等细粒度对应关系，而无需依赖额外的部位标注。

**跨模态交互建模的深化。** 与**MotionPatch**（Yu et al., CVPR 2024）采用ViT处理身体部位补丁但仅维持全局对齐不同，PST框架引入Shapley-Taylor Interaction（STI）量化跨模态元素对的交互强度。STI通过计算文本标记与动作标记在随机上下文前缀下的预期边际贡献，捕捉二者之间的非线性交互效应——这是余弦相似度无法表征的。STI值随后通过蒸馏损失传递至轻量级估计头，使模型在推理时也能高效近似细粒度交互。

**训练目标的复合化。** 基线方法仅依赖全局对比损失（InfoNCE），PST框架则构建了三层对比损失 + STI蒸馏损失 + 层级自蒸馏损失的复合目标。其中自蒸馏损失以关节级相似度分布指导片段级分布，强制不同语义层次间保持一致性，避免金字塔建模中的语义漂移。

### 适用边界

PST框架的适用性受以下因素制约：

1. **文本描述的结构性不对齐。** 当前动作-语言数据集（如HumanML3D、KIT-ML）的文本描述多为整体性动作（如“一个人向前走并挥手”），缺乏对具体身体部位的细粒度描述。这导致STI建模的细粒度交互在文本侧缺乏对应锚点，限制了其潜力的充分发挥。论文在局限性中明确指出，这种模态间的结构性不对齐是当前方法面临的主要挑战。

2. **数据集规模与多样性。** 实验在HumanML3D和KIT-ML两个标准基准上验证，但二者均为受控环境下的动作捕捉数据。对于野外视频、非标准动作或跨文化动作表达，PST框架的泛化能力尚未得到验证。

3. **STI估计头的迁移成本。** STI估计头在特定数据集上训练，迁移到全新领域（如不同动作粒度或文本风格的数据集）时可能需要额外微调，否则估计精度可能下降。

4. **压缩比的敏感性。** 消融实验表明，片段级压缩比设为0.25时性能最优，过高或过低均会损害检索精度。这意味着在实际部署中，压缩比需要针对具体任务进行调优。

### 局限与开放问题

**已识别的局限：**

- **局部偏差问题。** 在关节级和片段级对齐可视化中，模型对复杂或罕见动作（如“侧向格斗姿态”“向后踉跄”）的细粒度对齐仍存在困难，部分关节或片段与文本标记的匹配出现系统性偏差。论文认为这可能源于训练数据中此类动作样本不足，或注意力机制在长序列上的聚焦能力有限。

- **LLM增强的适用范围有限。** 论文尝试使用LLM生成部位级描述以缓解文本不对齐问题（Table 5），但该方法在KIT-ML等描述更简单的数据集上效果未知，且增加了推理成本。

**值得探索的开放问题：**

1. **文本模态的结构先验设计。** 如何为文本侧引入更符合人体运动结构的先验（如部位-动作分解、时间顺序约束），以弥合模态差距并提升细粒度检索的鲁棒性？这是论文明确提出的核心开放问题。

2. **金字塔框架的推广能力。** 能否将关节-片段-整体的金字塔式对齐框架推广到开放词汇或大规模动作-语言理解任务？这需要解决STI计算在大规模标记空间中的效率问题。

3. **局部偏差的缓解策略。** 论文观察到的局部偏差问题是否可以通过改进的注意力机制（如局部-全局混合注意力）或对比正则化技术缓解？这需要进一步的理论和实验探索。

4. **多模态动作理解的统一框架。** PST框架目前专注于检索任务，但其细粒度对齐能力是否可迁移至动作生成、动作描述、动作问答等下游任务，尚待验证。若能将STI建模与生成式模型结合，可能催生更统一的动作-语言理解框架。

**证据强度说明：** 上述局限和开放问题主要基于论文自身的讨论和消融实验的间接证据。其中局部偏差问题有可视化结果支撑（Figure 4, 7-10），但缺乏定量指标；LLM增强的迁移性仅有初步实验（Table 5），需要手动验证其在更多数据集上的效果。

## 原文 PDF

![[paperPDFs/arxiv_2026/PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval_via_Pyramidal_Shapley_Taylor_Learning.pdf]]