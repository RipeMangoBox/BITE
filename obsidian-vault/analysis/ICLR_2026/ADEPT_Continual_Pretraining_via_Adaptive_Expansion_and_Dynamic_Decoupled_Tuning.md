---
title: "ADEPT: Continual Pretraining via Adaptive Expansion and Dynamic Decoupled Tuning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ADEPT_Continual_Pretraining_via_Adaptive_Expansion_and_Dynamic_Decoupled_Tuning.pdf
project_link: null
code_link: https://github.com/PuppyKnightUniversity/ADEPT.git
openreview_forum_id: vcWDDfA4Ev
aliases:
- ADEPT
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "选择哪些层进行扩展以及如何为不同的参数单元分配学习率，基于它们对通用能力的重要性。"
primary_logic: "有效的CPT应该通过重要性引导选择性扩展对通用能力影响最小的层，并在这些扩展层内对单元进行解耦优化，以保护通用关键参数，同时允许适应性参数充分吸收领域知识。"
claims:
- "LLM中存在功能专门化，不同层和单元对通用能力的贡献不同（观察I和II）。"
- "扩展对通用能力影响最小的层可以理论上最小化遗忘的上界（附录F.1）。"
- "根据单元重要性逆比例分配学习率可以最小化通用领域遗忘的上界（附录F.2）。"
- "GSM8K (Mathematics domain) 上 Accuracy = 70.51"
---

# ADEPT: Continual Pretraining via Adaptive Expansion and Dynamic Decoupled Tuning

> [!tip] 核心洞察
> 有效的CPT应该通过重要性引导选择性扩展对通用能力影响最小的层，并在这些扩展层内对单元进行解耦优化，以保护通用关键参数，同时允许适应性参数充分吸收领域知识。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ADEPT：通过自适应扩展和动态解耦调优实现持续预训练 |
| 英文题名 | ADEPT: Continual Pretraining via Adaptive Expansion and Dynamic Decoupled Tuning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=vcWDDfA4Ev) · [GitHub](https://github.com/PuppyKnightUniversity/ADEPT.git) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | ADEPT |
| Dataset | GSM8K (Mathematics domain), CMB (Medical domain), MedQA (Medical domain) |

> [!tip] 效果简介
> - GSM8K (Mathematics domain) 上，Accuracy 为 70.51，对比 51.86 (PT-Full Qwen3-1.7B-Base)，变化 +18.65。
> - GSM8K (Mathematics domain) 上，Accuracy 为 76.19，对比 60.96 (PT-Full Qwen3-4B-Base)，变化 +15.23。
> - CMB (Medical domain) 上，Accuracy 为 65.43，对比 62.77 (PT-Full Qwen3-1.7B-Base)，变化 +2.66。

## 概要

大语言模型（LLM）在特定领域的持续预训练（Continual Pretraining, CPT）面临一个核心瓶颈：**通用知识与领域知识在参数空间中高度纠缠**，导致模型在学习新领域能力时不可避免地遗忘原有通用能力（灾难性遗忘），同时有限的模型容量难以充分吸收领域知识。现有方法或采用统一扩展架构（如均匀插入新层），或对所有参数施加统一学习率更新，忽略了LLM内部不同层和参数单元对通用能力的功能专门化差异。

本文提出 **ADEPT**（Adaptive Expansion and Dynamic Decoupled Tuning），核心思路是**基于参数对通用能力的重要性，自适应地选择扩展目标并解耦优化策略**。该方法包含两个阶段：

1. **通用能力引导的选择性层扩展**：通过探测每层对通用能力的贡献，识别并复制对通用能力影响最小的层，从理论上最小化遗忘上界（附录F.1）。
2. **自适应单元级解耦调优**：在扩展层内部，根据各参数单元对通用领域的重要性分配不对称学习率——关键单元以小学习率保护，适应性单元以大学习率充分吸收领域知识，理论上可最小化通用领域遗忘的上界（附录F.2）。

在数学和医疗两个领域的持续预训练实验中，ADEPT仅调优约15%的参数，在目标领域基准上相比全参数微调（PT-Full）提升最高达5.58%，在通用基准上提升最高达5.76%，同时显著缩短训练时间。消融实验证实，选择性层扩展和动态解耦调优两个阶段均对性能有实质性贡献，且重要性引导的选择策略优于均匀扩展策略。



大规模语言模型（LLM）的领域适应通常通过持续预训练（Continual Pretraining, CPT）实现，即在通用基座模型上利用领域语料进行二次训练。然而，CPT面临一个根本性瓶颈：**通用知识与领域知识在模型参数中高度纠缠**，导致领域学习过程中不可避免地损害模型的通用能力，即灾难性遗忘。

### 功能专门化：被忽视的结构性事实

现有CPT方法普遍采用“统一扩展、统一更新”的策略——要么对全部参数施加相同的学习率进行全参数微调（PT-Full），要么通过低秩适应（如**PT-LoRA**，Hu et al., 2022）或架构扩展（如**Llama-Pro**，Wu et al., 2024b）对所有层进行均匀处理。这些方法隐含地假设LLM中各层和各参数单元对通用能力的贡献是同质的。

然而，实证观察揭示了相反的事实。ADEPT通过对Qwen3系列模型的系统探测，发现了两个层次的功能专门化现象（Figure 2）：

- **层间异质性（Observation I）**：不同Transformer层对通用能力的贡献存在显著差异。某些层被掩蔽后，模型在通用基准上的损失几乎不变，表明这些层对通用知识的保持并非关键；而另一些层的掩蔽则导致损失急剧上升，说明它们承载了大量通用知识。
- **单元内异质性（Observation II）**：即使在单层内部，不同的参数单元（如注意力层的Q/K/V/O投影、MLP的上/下投影、LayerNorm参数等）对通用能力的贡献也高度分化。这意味着，在领域训练中对所有参数施加统一的学习率，将不可避免地扰动那些对通用能力至关重要的参数，从而引发遗忘。

### 现有方法的缺口

基于上述观察，现有方法存在两个结构性缺陷：

1. **容量分配的盲目性**：Llama-Pro等架构扩展方法在所有层之间均匀插入新层，忽视了层间功能专门化。这导致部分扩展层被放置在通用关键区域，扰动了原有的通用知识流；而真正需要额外容量来吸收领域知识的层却未被充分扩展。
2. **参数更新的粗粒度性**：无论是全参数微调还是LoRA类方法，都对可训练参数施加统一的学习率。这迫使模型在“保护通用参数”和“更新领域参数”之间做出全局妥协，无法实现对不同功能单元的精细控制。基于重播的方法（如Replay，Que et al., 2024）试图通过混合通用数据来缓解遗忘，但这增加了训练成本，且未能从根本上解决知识纠缠问题。

### ADEPT的核心动机

ADEPT的核心洞察是：**有效的持续预训练应当遵循LLM内在的功能专门化结构**——在通用能力影响最小的区域进行容量扩展，并在扩展区域内对不同功能单元实施差异化的知识注入。具体而言：

- **选择性扩展**：通过量化每层对通用能力的贡献，将扩展精确地引导至重要性最低的层，从而在理论上最小化遗忘的上界（附录F.1给出了形式化证明）。
- **解耦调优**：在扩展层内部，根据各参数单元对通用领域的重要性分配不对称的学习率——对通用关键单元施加低学习率以保护已有知识，对通用非关键单元施加高学习率以充分吸收领域知识。附录F.2进一步证明，按单元重要性逆比例分配学习率可以最小化通用领域遗忘的上界。

这一思路将CPT从“全局妥协”转变为“结构化适应”：通用知识在冻结的关键层和低学习率单元中得到保护，领域知识则通过扩展层的高学习率单元进行定向注入，两者在结构上实现解耦。



## 核心方法与创新机理

ADEPT 的核心创新在于将“在哪里扩展容量”与“如何分配学习强度”这两个持续预训练（CPT）中的关键决策，统一为对**通用能力重要性**的显式建模与利用。传统 CPT 方法（如 **PT-Full** 全参数微调、**Llama-Pro** 统一插入新层）采用“一刀切”的扩展与更新策略，忽略了 LLM 内部不同层和参数单元对通用能力的功能专门化，导致领域知识与通用知识高度纠缠，引发灾难性遗忘与容量不足。

ADEPT 通过两个相互衔接的阶段，从根本上改变了这一范式：

### 1. 基于通用能力重要性的选择性层扩展

传统架构扩展方法（如 Llama-Pro）在模型中**均匀插入**新层，不区分各层对通用能力的贡献差异。ADEPT 的先导实验揭示了关键事实：LLM 中不同层对通用能力的贡献高度异质——浅层通常承载更多通用知识，重要性向深层递减（Figure 2）。基于此，ADEPT 提出**选择性层扩展**：构建通用能力检测语料，通过掩蔽每层输出并测量损失增量来量化层重要性 $I_{\mathrm{layer}}^{(l)}$，然后选择重要性之和最小的 $k$ 层进行恒等复制并零初始化输出投影（Function Preserving Initialization）：

$$S_k = \arg \min_{S \subseteq \{1,\ldots,L\}} \sum_{l \in S} I_{\mathrm{layer}}^{(l)}$$

这一策略具有理论保证：扩展对通用能力影响最小的层，可证明性地最小化遗忘的上界（附录 F.1）。消融实验证实，移除该阶段导致通用和领域性能均大幅下降，且其影响大于移除第二阶段。

### 2. 自适应单元解耦调优

传统微调对所有参数施加**统一学习率**，迫使通用关键参数与领域适应性参数以相同强度更新。ADEPT 的第二个关键创新是将扩展层内的参数按功能划分为独立单元（Attention、MLP、LayerNorm 等），基于一阶泰勒近似计算每个单元的通用能力重要性 $I_{\mathrm{unit}}$，并据此分配**不对称学习率**：

$$\mathrm{lr}_{U} = 2 \cdot (1 - I_{\mathrm{unit}}) \cdot \mathrm{lr}_{\mathrm{base}}$$

通用重要性越高的单元，学习率越低，从而保护其不受领域训练侵蚀；通用重要性越低的单元，学习率越高，使其充分吸收领域知识。该分配策略同样具有理论支撑：学习率与单元重要性成反比，可最小化通用领域遗忘的上界（附录 F.2）。训练过程中，重要性每 500 步重新计算并动态调整学习率，实现自适应解耦。

### 创新本质

ADEPT 的 changed slots 揭示了其方法论跃迁：**层扩展策略**从“均匀插入”变为“重要性引导的选择性复制”，**参数更新粒度**从“统一学习率”变为“单元级不对称学习率”，**训练动态**从“静态更新”变为“周期性重要性探测与学习率自适应”。这三个维度的协同，使 ADEPT 在仅调优约 15% 参数的情况下，在数学和医疗领域的领域基准上平均超越全参数 CPT 最高 5.58%，同时在通用基准上最高提升 5.76%，实现了领域吸收与通用保持的有效平衡。



ADEPT 的整体流程围绕一个核心洞察展开：大语言模型的不同层和参数单元对通用能力的贡献存在显著异质性，因此有效的持续预训练应当**选择性扩展通用关键度最低的层**，并在扩展层内**对参数单元进行解耦优化**，从而在吸收领域知识的同时保护通用能力。

### 两阶段流水线

ADEPT 包含两个顺序执行的核心阶段，其整体架构如 Figure 3 所示：

**阶段一：通用能力引导的选择性层扩展（General-Competence Guided Selective Layer Expansion）**

该阶段的目标是为领域适应分配额外的模型容量，同时从理论上最小化灾难性遗忘的风险。具体步骤为：

1. **构建通用能力检测语料**（General Competence Detection Corpus）：从通用预训练数据中采样代表性样本，用于后续探测模型各层对通用能力的贡献。
2. **层重要性探测**：对模型的每一层 $l$，通过残差旁路掩蔽该层的输出，计算掩蔽前后在检测语料上的损失增量，作为该层的通用能力重要性分数：
   $$I_{\mathrm{layer}}^{(l)} = \hat{\mathcal{L}}^{(l)} - \mathcal{L}_{\mathrm{base}}$$
3. **选择性扩展**：按重要性升序排列所有层，选择重要性之和最小的 $k$ 层构成可扩展集合 $S_k$：
   $$S_k = \arg \min_{S \subseteq \{1,\ldots,L\}} \sum_{l \in S} I_{\mathrm{layer}}^{(l)}$$
   对选中的每一层，通过恒等复制创建平行层，并采用功能保持初始化（Function Preserving Initialization）将输出投影矩阵置零，确保扩展后模型输出与原始模型完全一致。

附录 F.1 从理论上证明，扩展通用能力重要性最低的层可以最小化遗忘的上界。

**阶段二：自适应单元级解耦调优（Adaptive Unit-Wise Decoupled Tuning）**

该阶段在扩展层内部实现参数单元级别的差异化学习，使通用关键参数得到保护，而适应性参数充分吸收领域知识。具体步骤为：

1. **单元划分**：将扩展层内的参数按功能划分为结构单元（如 Attention 的 Q/K/V/O 投影、MLP 的各线性层、LayerNorm 等）。
2. **单元重要性量化**：使用一阶泰勒近似计算单个参数的重要性 $I_j = \theta_j \cdot \nabla_{\theta_j} \mathcal{L}$，然后聚合成单元重要性：
   $$I_{\mathrm{unit}} = \frac{1}{|U|} \sum_{j \in U} I_j$$
3. **自适应学习率分配**：根据单元重要性反比例分配学习率，重要性越高的单元学习率越低：
   $$\mathrm{lr}_{U} = 2 \cdot (1 - I_{\mathrm{unit}}) \cdot \mathrm{lr}_{\mathrm{base}}$$
   其中系数 2 用于归一化，使整体学习率大致保持不变。
4. **动态更新**：在训练过程中每 500 步重新计算单元重要性并调整学习率，以适应训练动态。

附录 F.2 证明，按单元重要性逆比例分配学习率可以最小化通用领域遗忘的上界。

### 模块关系与数据流

整个框架的输入输出流如下：

1. **输入**：预训练基座模型 $M_0$ + 通用能力检测语料 $\mathcal{D}_{\mathrm{probe}}$ + 目标领域训练语料 $\mathcal{D}_{\mathrm{target}}$
2. **探测阶段**：在 $\mathcal{D}_{\mathrm{probe}}$ 上计算各层重要性 $I_{\mathrm{layer}}^{(l)}$ 和各单元重要性 $I_{\mathrm{unit}}$
3. **扩展阶段**：根据层重要性选择 $k$ 层进行恒等复制，得到扩展模型 $M_{\mathrm{exp}}$
4. **调优阶段**：在 $\mathcal{D}_{\mathrm{target}}$ 上训练 $M_{\mathrm{exp}}$，仅更新扩展层参数，且各单元使用自适应学习率 $\mathrm{lr}_U$
5. **输出**：领域增强模型，保持通用能力的同时获得目标领域专长

训练目标为标准自回归语言建模损失：
$$\mathcal{L} = -\sum_{t=1}^{T} \log P(x_t \mid x_{<t}; \Theta)$$

### 与基线方法的根本差异

| 设计维度 | 全参数微调 (PT-Full) | 架构扩展 (LLaMA-Pro) | 参数高效微调 (PT-LoRA) | **ADEPT** |
|---------|---------------------|---------------------|----------------------|-----------|
| 层扩展策略 | 不做扩展 | 均匀插入新层 | 不做扩展 | **重要性引导选择性扩展** |
| 参数更新粒度 | 统一学习率 | 冻结原始权重 | 低秩适配器 | **单元级解耦自适应学习率** |
| 重要性探测 | 无 | 无 | 无 | **周期性在线评估** |

ADEPT 的关键创新在于将**容量分配**（选择性层扩展）与**学习动态**（单元级解耦调优）统一在一个重要性驱动的框架下，使两者协同工作：扩展阶段从结构上隔离通用关键区域，调优阶段从优化上保护通用关键参数。消融实验（Table 2）证实，移除任一阶段均会导致性能显著下降，且移除阶段一的影响更大，验证了自适应容量分配的核心地位。



### 3.1 通用能力引导的选择性层扩展（Stage 1）

ADEPT 的第一阶段解决**在何处扩展模型容量**的问题。其核心操作流程如下：

**步骤一：层重要性探测。** 构建一个通用能力检测语料（General Competence Detection Corpus），通过掩蔽每层输出的残差连接，测量该层缺失时模型在通用语料上的损失增量。层重要性的形式化定义如下：

$$I_{\mathrm{layer}}^{(l)} = \hat{\mathcal{L}}^{(l)} - \mathcal{L}_{\mathrm{base}}$$

其中，$\mathcal{L}_{\mathrm{base}}$ 是原始模型在探测语料上的基准损失，$\hat{\mathcal{L}}^{(l)}$ 是掩蔽第 $l$ 层输出后的损失。$I_{\mathrm{layer}}^{(l)}$ 越大，表明该层对保持通用能力越关键。

**步骤二：选择性扩展。** 基于探测到的重要性分数，选择对通用能力影响最小的 $k$ 层进行扩展：

$$S_k = \arg \min_{S \subseteq \{1,\ldots,L\}} \sum_{l \in S} I_{\mathrm{layer}}^{(l)}$$

该公式从所有 $L$ 层中选出 $k$ 层，使得其重要性之和最小。论文在附录 F.1 中给出了理论保证：扩展通用能力重要性最低的层，可以从理论上最小化灾难性遗忘的上界。

**步骤三：恒等复制与函数保持初始化。** 对选中的每一层 $l \in S_k$，直接复制其参数（$\tilde{\Theta}^{(l)} = \Theta^{(l)}$），并采用函数保持初始化（Function Preserving Initialization）将输出投影矩阵置零，确保扩展后的模型在初始状态下输出与原模型完全一致。

### 3.2 自适应单元级解耦调优（Stage 2）

第二阶段解决**如何差异化更新扩展层内不同参数**的问题。其核心机制是将扩展层内的参数按功能划分为若干单元（如 Attention 的 Q/K/V/O 投影、MLP 的上/下投影、LayerNorm 参数等），并为每个单元分配不对称的学习率。

**单元重要性度量。** 首先在单个参数层面，使用一阶泰勒近似估计每个参数对通用领域损失的重要性：

$$I_j = \theta_j \cdot \nabla_{\theta_j} \mathcal{L}$$

然后对单元 $U$ 内的所有参数重要性取平均，得到单元重要性：

$$I_{\mathrm{unit}} = \frac{1}{|U|} \sum_{j \in U} I_j$$

**自适应学习率分配。** 学习率与单元重要性呈负相关——对通用能力越重要的单元，学习率越低，以保护其不被领域训练过度改写：

$$\mathrm{lr}_{U} = 2 \cdot (1 - I_{\mathrm{unit}}) \cdot \mathrm{lr}_{\mathrm{base}}$$

其中系数 2 用于归一化，使整体学习率规模大致保持不变。论文在附录 F.2 中证明，按单元重要性的反比分配学习率可以最小化通用领域遗忘的上界。

**动态更新机制。** 单元重要性并非静态不变。训练过程中，ADEPT 每 500 步重新计算一次 $I_{\mathrm{unit}}$ 并相应调整学习率，以适应参数重要性随训练进程的演化。

**训练目标。** 整个扩展模型在领域语料上使用标准的自回归语言建模损失进行优化：

$$\mathcal{L} = -\sum_{t=1}^{T} \log P(x_t \mid x_{<t}; \Theta)$$

### 3.3 关键设计决策与证据强度

| 设计决策 | 理论依据 | 证据强度 |
|---------|---------|---------|
| 选择重要性最低的层扩展 | 附录 F.1 证明可最小化遗忘上界 | 强（理论证明 + 消融实验验证） |
| 按单元重要性反比分配学习率 | 附录 F.2 证明可最小化遗忘上界 | 强（理论证明 + 消融实验验证） |
| 每 500 步动态重算重要性 | 应对训练中重要性漂移 | 中等（实验验证有效，但未对比不同更新频率） |
| 线性学习率映射 $2(1-I)$ | 简洁归一化 | 中等（论文承认未探索更精细的非线性策略） |

消融实验（Table 2）进一步验证了上述设计的必要性：移除 Stage-1（选择性层扩展）导致通用和领域性能均大幅下降，其影响程度大于移除 Stage-2（动态解耦调优）；将重要性引导的选择替换为均匀扩展（等同于 LLaMA-Pro 策略）同样导致性能显著降低。



## 实验与关键发现

### 主实验结果

ADEPT 在数学和医疗两个领域、Qwen3 系列多个模型规模上均展现出对持续预训练（CPT）基线的显著优势。Table 1 汇总了核心对比结果（最佳值加粗，次优值加下划线）：

**数学领域**：在 Qwen3-1.7B-Base 上，ADEPT 在 GSM8K 上达到 70.51%，相较全参数微调 PT-Full（51.86%）提升 **+18.65 个百分点**；在 Qwen3-4B-Base 上，GSM8K 从 60.96% 提升至 76.19%（+15.23 pp）。在通用能力指标上，ADEPT 同样保持甚至超越原始基座模型——例如 Qwen3-4B-Base 的 MMLU 从 65.71% 提升至 66.53%，CMMLU 从 77.92% 提升至 78.77%，表明其有效抑制了灾难性遗忘。

**医疗领域**：在 Qwen3-1.7B-Base 上，ADEPT 在 CMB 上达到 65.43%（PT-Full 为 62.77%，+2.66 pp）；在 Qwen3-8B-Base 上，MedQA 达到 69.24%（PT-Full 为 67.24%，+2.00 pp）。整体而言，ADEPT 在目标领域平均精度上最高超越 PT-Full **5.58%**，在通用基准上最高超越 **5.76%**，且仅需调优约 15% 的参数并缩短训练时间。

与代表性基线方法的横向对比显示：基于重播的 Replay（Que et al., 2024）虽可缓解遗忘，但在领域知识注入效率上不及 ADEPT；架构扩展方法 Llama-Pro（Wu et al., 2024b）采用均匀插入新层策略，缺乏对层重要性的差异化考量；参数高效方法 PT-LoRA（Hu et al., 2022）和 TaSL（Feng et al., 2024a）在领域适应性上受限于低秩假设。ADEPT 通过重要性引导的选择性扩展与单元级解耦调优，在领域性能与通用能力保留之间取得了更优的帕累托前沿。

### 消融实验

Table 2 在医疗领域对 ADEPT 的两个核心阶段进行了消融（Qwen3-1.7B-Base）：

- **移除 Stage-1（选择性层扩展）**：即不进行层扩展，仅做解耦调优。通用指标 MMLU 从 ADEPT 的 62.80 骤降至 57.31，CMMLU 从 66.89 降至 59.68；领域指标 MedQA 从 50.75 降至 47.29，CMB 从 65.43 降至 57.60。这是所有消融中性能下降最剧烈的配置，验证了自适应容量分配对同时维持通用能力与吸收领域知识的关键作用。
- **移除 Stage-2（动态解耦调优）**：即保留选择性扩展但使用统一学习率。性能同样下降，但幅度小于移除 Stage-1，表明解耦调优在扩展层内部进一步精细化知识注入，但容量扩展本身是更根本的瓶颈。
- **均匀扩展（Uniform Expansion）**：将重要性引导的选择替换为固定间隔均匀插入层（等价于 Llama-Pro 策略）。其性能显著低于 ADEPT，证实了“选择哪些层扩展”比“扩展多少层”更为关键——理论分析（附录 F.1）表明，扩展通用能力重要性最低的层可证明性地最小化遗忘上界。

### 机制分析

**参数解耦的激活分布证据**：Figure 4 和 Figure 6 展示了扩展层的激活分布核密度估计。在 Qwen3-1.7B 和 Qwen3-8B 上，ADEPT 的扩展策略使新层与原层在激活空间上形成清晰的功能分化——扩展层主要响应领域特定模式，而原层保持通用表征。相比之下，全参数 CPT 导致激活分布整体漂移，解释了其严重的遗忘现象。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_vcWDDfA4Ev/figures/007_Figure_4.jpg]]
*Figure 4: Activation distribution analysis of Qwen3-8B*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_vcWDDfA4Ev/figures/016_Figure_6.jpg]]
*Figure 6: Kernel Density Estimation of activations for Qwen3-1.7B-Base under different configurations. Our layer extension strategy enables effective parameter decoupling. Expanded layers: 22, 23, 25, and 27*

**Token 分布偏移的聚焦性**：Figure 5 的 token 分布偏移分析显示，在医疗领域，ADEPT 仅引起 2.18% 的 token 分布变化，而全参数预训练引发 5.61% 的偏移；数学领域 ADEPT 的偏移仅为 1.24%。词云可视化进一步表明，ADEPT 的变化高度集中在领域特定术语上（如医学术语、数学符号），而非对通用词汇的广泛扰动。这直接印证了动态解耦调优中“通用关键参数受保护、适应性参数充分学习”的设计意图。

**层重要性分布的先验验证**：Figure 2 的先导研究揭示，Qwen3 系列中通用知识关键层集中于浅层，重要性向深层递减。ADEPT 据此自动选择深层（通用重要性最低的层）进行扩展，与这一先验分布一致。Table 11-12 进一步对比了不同层选择策略（如扩展浅层 vs 深层、均匀 vs 重要性引导），证实重要性引导策略在各模型规模下均最优。

### 效率分析

Table 6 对比了医疗领域各方法的训练时间：ADEPT 在保持最优性能的同时，训练时间显著低于全参数 PT-Full，也优于 Llama-Pro。Table 7 报告了重要性探测的墙钟时间开销——层掩蔽和单元级梯度探测的总反向传播时间在训练总时长中占比很小（单 GPU 和 8-GPU 设置下均如此），验证了周期性重计算重要性（每 500 步）的实用性。Table 8 展示了不同扩展层数对训练时间的影响，表明 ADEPT 的效率优势在合理扩展范围内保持稳健。

### 失败模式与局限

1. **重要性估计的敏感性**：一阶泰勒近似 $I_j = \theta_j \cdot \nabla_{\theta_j} \mathcal{L}$ 对随机波动敏感，尤其在训练初期梯度不稳定时。Table 14 对比了基于 benchmark 和基于预训练语料的重要性估计，显示不同探测语料选择会影响最终性能，需根据领域谨慎构建通用能力检测语料（General Competence Detection Corpus）。
2. **学习率映射的线性假设**：自适应学习率采用简单线性映射 $\mathrm{lr}_U = 2 \cdot (1 - I_{\mathrm{unit}}) \cdot \mathrm{lr}_{\mathrm{base}}$，未探索非线性策略。在重要性分布高度偏斜时，线性映射可能导致部分单元学习率过激或过保守。
3. **领域泛化未充分验证**：当前实验仅覆盖数学和医疗两个领域，在代码、多语言等差异更大的领域上，层重要性分布和最优扩展策略可能不同，需进一步研究。
4. **多领域合并的简单化**：多个领域特定扩展层合并时仅使用简单加权平均，尚未探索更优的融合方法以构建统一的领域增强模型。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_vcWDDfA4Ev/figures/002_Figure.jpg]]

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_vcWDDfA4Ev/figures/021_Figure_8.jpg]]
*Figure 8: Kernel Density Estimation of activations for Qwen3-8B-Base, showing that our layer extension strategy enables clear parameter decoupling. We expand layers 26, 28, 29, and 30*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_vcWDDfA4Ev/figures/046_Figure_16.jpg]]
*Figure 16: Importance visualization for Llama3-8B-Base across Math and Medical domains, with and without calibration*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_vcWDDfA4Ev/figures/047_Figure.jpg]]
*Figure: (a) Llama3-8B-Base on Math (raw importance) (c) Llama3-8B-Base on Medical (raw importance)*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_vcWDDfA4Ev/figures/048_Figure.jpg]]
*Figure: (a) Qwen3-1.7B-Base on Math (raw importance) (c) Qwen3-1.7B-Base on Medical (raw importance)*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_vcWDDfA4Ev/figures/049_Figure_17.jpg]]
*Figure 17: Importance visualization for Qwen3-1.7B-Base across Math and Medical domains, with and without calibration*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_vcWDDfA4Ev/figures/050_Figure_18.jpg]]
*Figure 18: Importance visualization for Qwen3-4B-Base across Math and Medical domains, with and without calibration*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_vcWDDfA4Ev/figures/051_Figure.jpg]]
*Figure: (a) Qwen3-4B-Base on Math (raw importance) (c) Qwen3-4B-Base on Medical (raw importance)*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_vcWDDfA4Ev/figures/052_Figure_19.jpg]]
*Figure 19: Importance visualization for Qwen3-8B-Base across Math and Medical domains, with and without calibration*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_vcWDDfA4Ev/figures/053_Figure.jpg]]
*Figure: (a) Qwen3-8B-Base on Math (raw importance) (c) Qwen3-8B-Base on Medical (raw importance)*



## 定位与知识库关联

### 问题定位与核心瓶颈

持续预训练（Continual Pretraining, CPT）的核心挑战在于**灾难性遗忘**与**容量不足**之间的根本性冲突。传统CPT方法采用统一的参数扩展和统一的学习率更新，忽视了LLM内部不同层和参数单元对通用能力的功能专门化——这种粗粒度策略导致通用知识与领域知识高度纠缠，使得模型在吸收新领域知识时不可避免地损害其原有的通用能力。

ADEPT的出发点是两个关键观察：**观察I**——不同层对通用能力的贡献存在显著异质性，早期层对通用知识保留更为关键，而后期层的重要性逐渐降低（Figure 2）；**观察II**——同一层内的不同参数单元（如Attention、MLP、LayerNorm等）对通用能力的贡献同样高度不均匀。这两个观察共同指向一个核心洞察：有效的CPT应该**精确识别并保护通用关键参数，同时仅对通用影响最小的结构进行定向扩展和适应性更新**。

### 方法谱系中的位置

ADEPT处于**架构扩展**（Architecture Expansion）与**参数高效微调**（Parameter-Efficient Tuning）两条技术路线的交汇点，但通过引入**重要性引导的自适应机制**实现了对两者的超越。

**与架构扩展方法的对比。** **Llama-Pro**（Wu et al., 2024b）是架构扩展路线的代表，通过在Transformer层间均匀插入新层并冻结原始权重来实现领域适应。ADEPT与Llama-Pro的关键差异在于层选择策略：Llama-Pro采用均匀扩展，而ADEPT基于层重要性探测（Equation 3）选择对通用能力影响最小的层进行扩展。消融实验（Table 2）直接验证了这一差异——均匀扩展（Uniform Expansion）的性能显著低于ADEPT的重要性引导选择，表明**“在哪里扩展”比“是否扩展”更为关键**。理论上，附录F.1证明了扩展通用重要性最低的层可以最小化遗忘风险的上界。

**与参数高效微调方法的对比。** **PT-LoRA**（Hu et al., 2022）通过低秩适应矩阵实现参数高效微调，**TaSL**（Feng et al., 2024a）进一步通过解耦LoRA矩阵跨层实现多任务扩展。ADEPT与这些方法的核心差异体现在两个层面：（1）ADEPT通过物理扩展层容量来提供额外的领域知识吸收空间，而非仅在低秩子空间内调整；（2）ADEPT的单元级解耦调优（Equation 7）根据参数对通用能力的重要性分配不对称学习率，而非对所有可调参数施加统一的学习率约束。附录F.2进一步证明，按单元重要性逆比例分配学习率可以最小化通用领域遗忘的上界。

**与数据层面方法的互补性。** **Replay**（Que et al., 2024）通过在训练中混合通用领域数据来缓解遗忘，属于数据层面的防御策略。ADEPT的架构和优化层面设计可以与Replay正交互补——两者分别从模型结构和训练数据两个维度对抗灾难性遗忘，理论上可以叠加使用以获得更强的遗忘抑制效果。

### 方法适用边界

**已验证的领域范围。** 当前实验验证集中在**数学推理**（GSM8K、MMLU-Math等）和**医疗知识**（MedQA、CMB、MMCU-Medical等）两个领域，覆盖Qwen3系列的1.7B、4B和8B三个模型规模。在数学领域，ADEPT相比全参数CPT（PT-Full）在GSM8K上分别获得+18.65%（1.7B）和+15.23%（4B）的显著提升；在医疗领域，提升幅度相对温和（+2.66%至+2.00%），但仍稳定超越所有基线方法。

**适用条件与限制。** ADEPT的有效性依赖于两个前提：（1）存在可用的通用能力检测语料（General Competence Detection Corpus）用于重要性探测——论文使用MMLU、CMMLU、ARC等通用基准的示例构建该语料（Table 5），其质量和覆盖范围直接影响重要性估计的准确性；（2）领域语料与通用语料之间存在足够的分布差异，使得参数重要性呈现出可利用的异质性——如果新领域与通用领域高度重叠，选择性扩展和差异化学习率带来的收益可能有限。

**未充分验证的边界。** 以下场景需要进一步研究：（1）代码生成、多语言等与数学/医疗性质差异较大的领域；（2）超大规模模型（70B+）上扩展策略的效率和效果；（3）多个领域同时扩展时的层选择冲突和模型合并策略——当前仅使用简单加权平均合并多领域扩展层，可能不是最优方案。

### 局限性与开放问题

**重要性估计的局限性。** 当前采用一阶泰勒近似（$I_j = \theta_j \cdot \nabla_{\theta_j} \mathcal{L}$）估计参数重要性，该方法对随机波动敏感，且依赖于探测语料的质量。虽然论文证明周期性重计算（每500步）的额外开销较小（Table 7），但更鲁棒的实时重要性度量方法仍有待探索。

**学习率映射的简化设计。** 动态学习率分配采用简单的线性映射 $\mathrm{lr}_{U} = 2 \cdot (1 - I_{\mathrm{unit}}) \cdot \mathrm{lr}_{\mathrm{base}}$，系数2用于保持整体学习率大致不变。这种线性策略可能无法充分利用重要性信息的细粒度差异——重要性极高和极低的单元之间可能存在非线性的最优学习率关系，更精细的映射函数设计是一个开放方向。

**多领域扩展的合并策略。** 当需要为多个领域分别训练扩展层时，如何科学地组合这些领域特定的扩展层以获得统一的领域增强模型，目前仅采用简单加权平均，尚未探索更优的融合方法（如基于任务相关性的动态路由或门控机制）。

**理论保证的实践差距。** 虽然附录F.1和F.2提供了选择性扩展和逆比例学习率分配的最小化遗忘上界的理论证明，但这些上界依赖于重要性估计的准确性——当重要性估计存在偏差时，理论保证的有效性会相应减弱。



## 原文 PDF

![[paperPDFs/ICLR_2026/ADEPT_Continual_Pretraining_via_Adaptive_Expansion_and_Dynamic_Decoupled_Tuning.pdf]]
