---
title: "CME-CAD: Heterogeneous Collaborative Multi-Expert Reinforcement Learning for CAD Code Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CME_CAD_Heterogeneous_Collaborative_Multi_Expert_Reinforcement_Learning_for_CAD_Code_Generation.pdf
project_link: null
code_link: null
aliases:
- CCHCMERL
- CME-CAD
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过异构多专家协作学习框架，引入多个具有不同系统提示（推理风格）的专家模型，结合专家内部优势估计（EIAE）来选择最适合任务的专家，利用KL散度惩罚强制弱专家向强专家学习，并通过硬负样本缓冲机制（HSB）持续利用困难样本进行监督微调，从而打破单一模型认知限制，促进对多样化推理路径的探索。
primary_logic: 借鉴“取长补短”的思想，融合多个异构预训练模型的互补优势：不同专家的差异化推理路径为模型提供了更丰富的探索空间，跨专家协作学习使得每个专家都能从其他专家处获取改进信号，突破了单一专家模型固有的推理上限，显著提升了CAD代码生成的几何精度、可执行性和坐标一致性。
claims:
- 提出CME-CAD范式，将多专家微调与多专家强化学习结合，用于CAD代码生成。
- MEFT阶段利用多个异构专家生成不同风格的推理路径，增强了推理多样性。
- MERL阶段通过专家内部优势估计和多专家协作学习，实现跨专家知识迁移与探索增强。
- 在CADExpert基准上，CME-CAD取得80.71%的IoU，相比最强基线CAD-RL的71.84%提升了8.87个百分点。
---

# CME-CAD: Heterogeneous Collaborative Multi-Expert Reinforcement Learning for CAD Code Generation

> [!tip] 核心洞察
> 借鉴“取长补短”的思想，融合多个异构预训练模型的互补优势：不同专家的差异化推理路径为模型提供了更丰富的探索空间，跨专家协作学习使得每个专家都能从其他专家处获取改进信号，突破了单一专家模型固有的推理上限，显著提升了CAD代码生成的几何精度、可执行性和坐标一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | CME-CAD：面向CAD代码生成的异构协作多专家强化学习 |
| 英文题名 | CME-CAD: Heterogeneous Collaborative Multi-Expert Reinforcement Learning for CAD Code Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.23333) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | CME-CAD (Heterogeneous Collaborative Multi-Expert Reinforcement Learning) |
| Dataset | CADExpert |

> [!tip] 效果简介
> - CADExpert 上，IoU (%) 80.71 vs 71.84 (CAD-RL) (+8.87)；Executability (%) 98.25 vs 97.60 (CAD-RL) (+0.65)；Mean CD 1.00 vs 1.22 (CAD-RL) (-0.22)。

## 概要

从二维工程图自动生成精确、可执行的CAD代码是工业设计自动化的核心挑战。现有基于可验证奖励的强化学习方法（RLVR）本质上是on-policy的，倾向于沿已有奖励丰富的推理路径优化，难以主动探索新的知识与推理路径。同时，CAD代码生成任务要求高几何精度、约束兼容性和可编辑性，单一专家模型的推理路径受限，在复杂场景中性能难以突破。

针对上述瓶颈，本文提出**CME-CAD**（Heterogeneous Collaborative Multi-Expert Reinforcement Learning）范式。其核心思路是借鉴“取长补短”的思想：引入多个具有不同系统提示（推理风格）的异构专家模型，通过专家内部优势估计（EIAE）为每个任务选择最合适的专家，利用KL散度惩罚强制弱专家向强专家学习，并通过硬负样本缓冲机制（HSB）持续利用困难样本进行监督微调。这一跨专家协作学习框架打破了单一模型的认知限制，显著拓展了对多样化推理路径的探索空间。

在工业级数据集CADExpert上，CME-CAD取得了**80.71%的IoU**，相比当前最强基线CAD-RL的71.84%提升了**8.87个百分点**，可执行性达到98.25%，平均Chamfer距离降至1.00。消融实验表明，硬负样本缓冲机制对整体性能影响最大，而EIAE与多专家协作学习（MECL）联合使用可充分激活框架潜力。

计算机辅助设计（CAD）是现代工业制造的基石，而将二维工程图自动转化为可执行的CAD脚本代码是提升设计效率的关键环节。近年来，视觉语言模型（VLM）在CAD代码生成领域展现出巨大潜力，研究者先后提出了**CAD-MLLM**（Xu et al., arXiv 2024）、**GenCAD**（Alam et al., arXiv 2024）以及基于思维链推理的**CAD-Coder**（Guan et al., arXiv 2025）等方法，逐步推进了这一任务的性能边界。然而，该任务天然面临三大核心挑战：生成代码必须具备**高几何精度**、**约束兼容性**和**可编辑性**——任何一个维度的偏差都可能导致生成的3D模型无法实际使用。

当前最先进的方法，如**CAD-RL**（Niu et al., arXiv 2025），采用基于可验证奖励的强化学习（RLVR）来优化代码生成质量。这类方法虽然有效，但存在一个根本性的认知瓶颈：**RLVR本质上是on-policy的优化过程，倾向于强化模型已有且奖励丰富的推理路径，而难以主动探索新的知识与推理方式**。当面对CADExpert这类包含复杂工业设计特征的数据集时，单一专家模型的推理空间受限，即使经过充分训练，其性能仍会触及认知上限。

这一瓶颈的深层原因在于，**单一专家模型受限于其固有的推理风格和知识边界**。不同预训练VLM由于架构、训练数据和提示策略的差异，各自形成了独特的推理路径偏好——有的擅长精细的几何推理，有的更关注代码结构完整性。但现有方法将模型视为同质个体进行优化，未能利用这些互补性优势。

受“取长补短”思想的启发，本文提出**异构协作多专家强化学习（CME-CAD）范式**。其核心洞见在于：通过融合多个异构预训练模型的差异化推理能力，为强化学习提供更丰富的探索空间；同时，跨专家协作学习机制使得每个专家都能从其他专家处获取改进信号，从而突破单一模型固有的推理上限。这一范式将多专家微调（MEFT）与多专家强化学习（MERL）有机结合，为CAD代码生成任务开辟了新的优化路径。

## 核心方法与创新机理

### 问题瓶颈：从单一路径优化到多路径探索的范式跃迁

现有基于可验证奖励的强化学习（RLVR）方法，如 **CAD-RL**（Niu et al., arXiv 2025），在CAD代码生成任务上取得了显著进展，但其本质上的on-policy特性构成了性能天花板：模型倾向于沿着奖励丰富的已知推理路径进行优化，而难以主动探索新的知识与推理路径。这一固有限制在CAD代码生成这一高精度、强约束场景中被进一步放大——从二维工程图直接生成精确的CADQuery代码，不仅要求几何精度（IoU），还需同时满足可执行性、坐标平面一致性等多重约束。单一专家模型的推理路径受限，导致在复杂工业设计任务中性能难以突破。

CME-CAD的核心创新在于，它并非在单一模型架构或奖励函数设计上做增量改进，而是从**训练范式**层面进行了根本性重构：将“单专家优化”转变为“异构多专家协作学习”，通过引入具有不同推理风格的多个专家模型，打破了单一模型的认知边界。

### Changed Slots：四个维度的范式重构

与以CAD-RL为代表的SOTA基线相比，CME-CAD在以下四个关键维度上实现了系统性创新：

#### 1. 训练范式：从单专家RL到多专家微调+多专家强化学习

基线方法（CAD-RL等）采用标准的单专家监督微调（SFT）后接RLVR/GRPO的训练流程。CME-CAD将其重构为两阶段框架：

- **Multi-Expert Fine-Tuning (MEFT)**：利用多个异构专家模型（通过不同的系统提示赋予差异化的推理风格）生成多样化的思维链（CoT）数据，并进行联合监督微调。其训练目标为最大化在给定系统提示和输入条件下生成拼接推理过程与答案的概率：

$$\mathcal { L } = - \sum _ { n = 1 } ^ { N } \sum _ { i = 1 } ^ { I } \log \left( p ( \mathbf{\mathrm{Concat}} ( C _ { i } ^ { ( n ) } , A _ { i } ^ { ( n ) } ) \mid P _ { n } , I _ { i } ) \right)$$

- **Multi-Expert Reinforcement Learning (MERL)**：在强化学习阶段引入跨专家协作机制，使各专家不仅从自身经验中学习，还能从其他专家的成功推理中获取改进信号。

这一范式转变的核心价值在于：多专家SFT阶段即能扩展模型的知识边界（消融实验Table 2证实，仅使用多专家数据进行SFT即可在所有评估指标上超越单专家SFT），而完整的MERL方法则在此基础上进一步突破单一专家的性能上限。

#### 2. 推理路径多样性：从单一风格到异构融合

基线方法受限于单一模型的推理风格，探索空间有限。CME-CAD通过以下机制实现推理路径的多样化与有效融合：

- **异构专家设计**：在MEFT阶段，不同专家被赋予差异化的系统提示，从而生成具有本质区别的推理路径。这些路径的差异性为后续强化学习提供了更丰富的探索空间。
- **Expert-Internal Advantage Estimation (EIAE)**：在每个专家内部计算相对优势，利用GRPO损失进行策略优化。关键创新在于采用非负优势截断（$\max(A, 0)$），避免对探索行为的过度惩罚：

$$\mathcal { L } _ { \mathrm { G R P O } } ^ { ( n ) } = - \mathbb { E } _ { A _ { g } ^ { n } \sim \pi _ { \theta } } \left[ \log \pi _ { \theta } ( A _ { g } ^ { n } | P _ { n } , I _ { i } ) \cdot \operatorname* { m a x } ( A _ { g } ^ { n } , 0 ) \right]$$

消融实验证实，EIAE的引入显著提高了代码可执行性，这是因为它帮助模型为每个任务选择最合适的专家进行推理。

#### 3. 跨专家知识迁移：Multi-Expert Collaborative Learning (MECL)

这是CME-CAD最具原创性的机制之一。传统RLVR方法中，各样本独立优化，不存在模型间的知识流动。CME-CAD通过KL散度惩罚项，强制表现较差的专家（$E^-$）学习最佳专家（$E^+$）的输出分布：

$$\mathcal { L } _ { \mathrm { K L } } = \mathrm { K L } \left( \pi _ { \theta } ( A ^ { + } | P _ { E ^ { - } } , I _ { i } ) || \pi _ { \theta } \big ( A _ { \mathrm { c o r r e c t } } | P _ { E ^ { + } } , I _ { i } \big ) \right)$$

这一设计的精妙之处在于：弱专家并非简单复制强专家的输出，而是在保持自身提示风格的前提下，将其输出分布向强专家的正确答案分布靠拢，实现“取长补短”式的知识迁移。消融实验（Table 3）表明，EIAE与MECL联合使用方能充分激活框架潜力。

#### 4. 奖励函数设计：门控机制与困难样本利用

基线方法通常仅依赖可执行性或几何一致性奖励。CME-CAD引入了更精细的奖励结构：

- **门控总奖励**：格式正确性和可执行性作为必要门控条件，仅当两者均满足时，才结合几何IoU奖励和坐标平面一致性奖励：

$$R = \lambda _ { \mathrm { f o r m a t } } R _ { \mathrm { f o r m a t } } \cdot \lambda _ { \mathrm { e x e c } } R _ { \mathrm { e x e c } } \cdot \left( \lambda _ { \mathrm { I o U } } R _ { \mathrm { I o U } } + \lambda _ { \mathrm { p l a n e } } R _ { \mathrm { p l a n e } } \right)$$

- **Hard Negative Sample Buffering Mechanism (HSB)**：维护困难样本缓冲区，当所有专家均无法生成正确输出时，对缓冲区数据施加监督微调，缓解奖励稀疏问题：

$$\mathcal { L } _ { \mathrm { S F T } } = - \sum _ { B } \log p _ { \theta } ( A _ { \mathrm { c o r r e c t } } | P _ { n } , I _ { i } )$$

消融实验明确指出，HSB对整体性能影响最大——在CADExpert这一高复杂度数据集上，困难样本的有效利用是性能突破的关键。

### 创新有效性验证

在CADExpert基准上，CME-CAD以**80.71%的IoU**显著超越SOTA方法CAD-RL的71.84%（提升8.87个百分点），同时可执行性达到98.25%，Mean CD降至1.00。消融实验的系统性验证（Table 3）表明：从基础模型（IoU 64.45%）开始，逐步添加EIAE、HSB和MECL后性能持续提升，三者共同使用达到最优。这一递进式验证有力地支撑了各创新组件的独立贡献与协同效应。

CME-CAD 采用**两阶段异构多专家训练范式**，将 CAD 代码生成建模为从二维工程图到可执行 CADQuery 代码的序列生成任务。其核心设计思路是：通过引入多个具有差异化推理风格的专家模型，打破单一模型在复杂推理场景中的认知上限，实现跨专家的知识迁移与探索增强。

### 两阶段训练流程

整个框架由以下两个阶段串联构成：

1.  **多专家微调（Multi-Expert Fine-Tuning, MEFT）**：第一阶段，利用多个异构预训练模型（专家）为同一输入生成不同风格的思维链（Chain-of-Thought, CoT）数据。每个专家被赋予独特的系统提示（system prompt），从而诱导出差异化的推理路径。这些数据随后用于对基础模型进行监督微调，使模型初步习得多样化的推理风格。训练目标为最大化在给定系统提示和输入条件下，生成拼接推理过程与答案的概率：
    $$
    \mathcal { L } = - \sum _ { n = 1 } ^ { N } \sum _ { i = 1 } ^ { I } \log \left( p ( \mathbf{\mathrm{Concat}} ( C _ { i } ^ { ( n ) } , A _ { i } ^ { ( n ) } ) \mid P _ { n } , I _ { i } ) \right)
    $$

2.  **多专家强化学习（Multi-Expert Reinforcement Learning, MERL）**：第二阶段，在 MEFT 基础上引入强化学习，通过可验证奖励信号进一步优化模型。MERL 阶段包含三个关键机制：
    -   **专家内部优势估计（Expert-Internal Advantage Estimation, EIAE）**：在每个专家内部独立计算相对优势，利用 GRPO 损失进行策略优化，并采用非负截断 $\max(A, 0)$ 保护模型的探索能力。
    -   **多专家协作学习（Multi-Expert Collaborative Learning, MECL）**：通过 KL 散度惩罚项，强制表现较差的专家（弱专家）的输出分布向最佳专家（强专家）的正确答案分布靠拢，实现跨专家知识迁移，同时保持各自的提示风格。
    -   **硬负样本缓冲机制（Hard Negative Sample Buffering, HSB）**：维护一个困难样本缓冲区，当所有专家均无法为某样本生成正确输出时，将该样本存入缓冲区，并定期对其进行监督微调，以缓解奖励稀疏问题，持续利用困难样本提升模型能力。

### 模块关系与数据流

框架的模块关系与数据流可概括为：

-   **输入**：二维工程图（三视图图像）及对应的系统提示。
-   **MEFT 阶段**：多个异构专家 → 生成差异化 CoT 数据 → 监督微调基础模型 → 输出具备多风格推理能力的初始策略模型。
-   **MERL 阶段**：初始策略模型在多个专家提示下采样生成代码 → 执行代码并计算门控总奖励（格式 + 可执行性作为门控条件，内部为 IoU 与坐标平面一致性奖励的加权和）→ EIAE 计算组内优势并更新策略 → MECL 通过 KL 散度实现跨专家知识迁移 → HSB 收集并回放困难样本。
-   **输出**：可执行的 CADQuery 代码，经解析后生成对应的三维模型。

### 奖励函数设计

奖励函数采用**门控总奖励**结构，仅当格式奖励 $R_{\mathrm{format}}$ 和可执行性奖励 $R_{\mathrm{exec}}$ 均满足时，总奖励才为正，内部为几何 IoU 奖励与坐标平面一致性奖励的加权和：
$$
R = \lambda _ { \mathrm { f o r m a t } } R _ { \mathrm { f o r m a t } } \cdot \lambda _ { \mathrm { e x e c } } R _ { \mathrm { e x e c } } \cdot \left( \lambda _ { \mathrm { I o U } } R _ { \mathrm { I o U } } + \lambda _ { \mathrm { p l a n e } } R _ { \mathrm { p l a n e } } \right)
$$
其中几何 IoU 奖励基于 Jaccard 指数衡量生成模型与真实模型的三维几何精度：
$$
R _ { \mathrm { I o U } } ( M _ { \mathrm { g e n } } , M _ { \mathrm { g t } } ) = J ( M _ { \mathrm { g e n } } , M _ { \mathrm { g t } } ) = { \frac { | M _ { \mathrm { g e n } } \cap M _ { \mathrm { g t } } | } { | M _ { \mathrm { g e n } } \cup M _ { \mathrm { g t } } | } }
$$

整体框架的架构示意可参考 Figure 2，其中 $O$ 表示模型输出，$O^N$ 表示第 $N$ 个专家的思维链与答案的拼接，$O_G^N$ 表示第 $N$ 个专家生成的 $G$ 个输出组。

![[assets/figures/papers/paper_list_l2669_https_arxiv_org_abs_2512_23333/figures/002_Figure_2.jpg]]
*Figure 2: Overall architecture of our method CME-CAD framework. O represents the model output*

![[assets/figures/papers/paper_list_l2669_https_arxiv_org_abs_2512_23333/figures/001_Figure_1.jpg]]
*Figure 1: The workflow of our method for CAD code generation*

CME-CAD 的训练流程由两个阶段构成：**多专家监督微调（MEFT）** 与 **多专家强化学习（MERL）**。MEFT 阶段负责构建多样化的推理路径数据并进行监督微调，MERL 阶段则在强化学习框架下通过三个核心机制实现跨专家知识迁移与探索增强：专家内部优势估计（EIAE）、多专家协作学习（MECL）和硬负样本缓冲机制（HSB）。

### 多专家监督微调（MEFT）

MEFT 的核心目标是利用多个异构专家模型生成风格各异的思维链（CoT）推理路径，从而扩展模型的知识边界。对于第 $n$ 个专家，给定系统提示 $P_n$ 和输入工程图 $I_i$，构造专家专属样本：

$$S_n = (P_n, I_i, C_i^{(n)}, A_i^{(n)})$$

其中 $C_i^{(n)}$ 为该专家的推理过程，$A_i^{(n)}$ 为对应的 CADQuery 代码答案。训练时，将推理过程与答案拼接后，通过负对数似然损失最大化联合生成概率：

$$\mathcal{L} = -\sum_{n=1}^{N}\sum_{i=1}^{I} \log\left(p(\mathbf{Concat}(C_i^{(n)}, A_i^{(n)}) \mid P_n, I_i)\right)$$

这一设计使得模型在单一参数空间内同时学习多个专家的差异化推理风格，为后续 MERL 阶段的协作学习奠定基础。

### 多专家强化学习（MERL）

MERL 阶段在 MEFT 初始化权重的基础上，通过可验证奖励驱动策略优化。其奖励函数采用**门控总奖励**设计，将格式正确性和代码可执行性作为必要条件：

$$R = \lambda_{\mathrm{format}} R_{\mathrm{format}} \cdot \lambda_{\mathrm{exec}} R_{\mathrm{exec}} \cdot (\lambda_{\mathrm{IoU}} R_{\mathrm{IoU}} + \lambda_{\mathrm{plane}} R_{\mathrm{plane}})$$

仅当格式奖励 $R_{\mathrm{format}}$ 和可执行性奖励 $R_{\mathrm{exec}}$ 均为正时，门控开启，内部几何 IoU 奖励与坐标平面一致性奖励的加权和才生效。其中几何 IoU 奖励基于 Jaccard 指数衡量生成 3D 模型与真实模型的体素重合度：

$$R_{\mathrm{IoU}}(M_{\mathrm{gen}}, M_{\mathrm{gt}}) = J(M_{\mathrm{gen}}, M_{\mathrm{gt}}) = \frac{|M_{\mathrm{gen}} \cap M_{\mathrm{gt}}|}{|M_{\mathrm{gen}} \cup M_{\mathrm{gt}}|}$$

#### 专家内部优势估计（EIAE）

在每个专家内部，采用组相对策略优化（GRPO）损失进行策略更新。关键创新在于**非负优势截断**，仅对正优势进行加权，避免负优势抑制模型的探索能力：

$$\mathcal{L}_{\mathrm{GRPO}}^{(n)} = -\mathbb{E}_{A_g^n \sim \pi_\theta}\left[\log \pi_\theta(A_g^n \mid P_n, I_i) \cdot \max(A_g^n, 0)\right]$$

其中 $A_g^n$ 为第 $n$ 个专家在第 $g$ 个输出上的相对优势。消融实验表明，EIAE 显著提升了代码可执行性，因为它帮助模型为每个任务选择最合适的专家（Tab. 3）。

#### 多专家协作学习（MECL）

MECL 通过 KL 散度惩罚实现跨专家知识迁移。在每个训练步中，识别表现最佳的专家 $E^+$ 和最差专家 $E^-$，强制 $E^-$ 在保持自身提示风格 $P_{E^-}$ 的条件下，使其输出分布向 $E^+$ 的正确答案分布靠拢：

$$\mathcal{L}_{\mathrm{KL}} = \mathrm{KL}\left(\pi_\theta(A^+ \mid P_{E^-}, I_i) \;\|\; \pi_\theta(A_{\mathrm{correct}} \mid P_{E^+}, I_i)\right)$$

这一设计实现了“取长补短”的协作效应：弱专家从强专家获取改进信号，同时保留各自的推理风格差异，维持了探索空间的多样性。

#### 硬负样本缓冲机制（HSB）

针对奖励稀疏问题——当所有专家均无法生成正确输出时，强化学习无法获得有效训练信号——HSB 维护一个困难样本缓冲区。当某样本的所有专家输出均未通过门控奖励时，将其加入缓冲区；随后对缓冲区数据执行监督微调：

$$\mathcal{L}_{\mathrm{SFT}} = -\sum_{B} \log p_\theta(A_{\mathrm{correct}} \mid P_n, I_i)$$

消融实验证实，HSB 对整体性能影响最大（Tab. 3），这与 CADExpert 数据集的高复杂性直接相关——困难样本的持续利用是突破性能瓶颈的关键。

## 实验与关键发现

### 主要结果

CME-CAD 在 CADExpert 基准上取得了显著优于现有方法的性能。Table 1 展示了与多个基线方法的全面对比，包括预训练 VLM 的零样本推理结果以及经过微调的方法。在几何精度指标 IoU 上，CME-CAD 达到 **80.71%**，相比此前最强的 CAD-RL（71.84%）提升了 **8.87 个百分点**。在可执行性方面，CME-CAD 达到 **98.25%**，较 CAD-RL 的 97.60% 进一步提升，表明门控奖励机制有效保障了代码的正确执行。在衡量生成模型与真实模型之间距离的 Mean CD 指标上，CME-CAD 取得 **1.00**，优于 CAD-RL 的 1.22，降幅达 0.22，说明生成的 3D 几何形状与真实值更为接近。

![[assets/figures/papers/paper_list_l2669_https_arxiv_org_abs_2512_23333/figures/004_Table_1.jpg]]
*Table 1: The comparison on CADExpert is presented in two sections. The upper block reports results using pretrained SOTA VLMs without any fine-tuning, while the lower block displays results after fine-tuning. ∗ denote our re-implementation trained on the same benchmark*

值得注意的是，所有带 ∗ 标记的基线方法均在相同基准上进行了重新实现与训练，确保了比较的公平性。预训练 VLM 的零样本推理性能普遍较低，进一步凸显了该任务对专用训练范式的高度依赖。

### 消融实验

为验证 CME-CAD 各核心组件的贡献，论文进行了系统的消融研究（Table 3）。

![[assets/figures/papers/paper_list_l2669_https_arxiv_org_abs_2512_23333/figures/006_Table_3.jpg]]
*Table 3: Ablation studies on each component of CME-CAD, with results reported for the best-performing experts for brevity. “EIAE” refers to Expert-Internal Advantage Estimation, “HSB” stands for Hard Negative Sample Buffering Mechanism, and “MECL” denotes Multi-Expert Collaborative Learning*

**多专家学习 vs. 单专家学习。** Table 2 的对比揭示了多专家框架的根本性优势。仅使用单一专家进行监督微调（SFT）时，模型的知识边界受限于该专家的推理风格。当采用多专家数据（MEFT）进行 SFT 时，模型性能即获得全面提升，表明异构推理路径的引入本身就能扩展模型的知识覆盖。在此基础上，应用完整的多专家强化学习（MERL）方法后，性能进一步突破单专家上限，验证了跨专家协作学习的核心价值。

**组件级消融。** 移除所有组件时，基础模型仅取得 64.45% IoU 和 96.99% 可执行性。逐步添加各组件后，性能持续提升：

- **专家内部优势估计（EIAE）** 的引入显著提高了代码可执行性。其核心机制在于帮助模型为每个任务选择最合适的专家，避免不匹配的推理风格导致生成失败。
- **硬负样本缓冲机制（HSB）** 对整体性能影响最大。CADExpert 数据集包含大量高复杂度的工业设计样本，奖励稀疏问题严重——当所有专家均无法生成正确输出时，标准 RL 无法提供有效学习信号。HSB 通过持续利用这些困难样本进行监督微调，弥补了这一关键缺口。
- **多专家协作学习（MECL）** 通过 KL 散度惩罚强制弱专家向强专家学习，实现了跨专家的知识迁移。

当 EIAE、HSB 和 MECL 三者联合使用时，框架潜力被充分激活，达到最佳性能：IoU 80.71%、Mean CD 1.00、可执行性 98.25%。这一结果表明，三个组件之间存在协同效应——EIAE 选择合适专家、HSB 攻克困难样本、MECL 传播改进信号，共同构成了完整的多专家学习闭环。

### 失败模式与局限性

尽管 CME-CAD 取得了显著性能提升，论文未系统报告具体的失败案例。结合方法设计和数据集特性，可推断以下潜在局限：

1. **硬负样本缓冲的依赖性问题。** HSB 机制依赖预先收集的困难样本缓冲区。当所有专家持续无法生成正确输出时，该方法能否持续改进缺乏理论保证，可能陷入局部最优。
2. **多专家训练的资源开销。** 论文提到训练时间仅增加 20–30%，但多专家训练仍需额外内存和计算资源。在更轻量的模型上能否有效应用，尚待验证。
3. **泛化边界不明确。** 当前方法仅在 CADExpert 数据集上验证，对于手绘工程图或部分标注的工业图纸等质量参差不齐的输入，泛化能力未作讨论。
4. **任务范围受限。** 方法针对 CADQuery 代码生成设计，能否扩展到其他 CAD 脚本语言（如 OpenSCAD）或直接生成参数化特征树，仍需进一步研究。对于涉及装配体或运动学仿真的复杂产品，精度和可编辑性亦无实验支撑。

### 关键图表结论

- **Table 1**：CME-CAD 在 IoU、Mean CD、可执行性三项核心指标上全面超越所有基线，IoU 提升 8.87 个百分点，确立了新的 SOTA。
- **Table 2**：多专家 SFT 数据即可超越单专家上限，完整 MERL 方法带来进一步的显著增益，证实了异构协作学习的根本优势。
- **Table 3**：HSB 是影响最大的单一组件，EIAE 与 MECL 联合使用才能充分释放框架潜力，三者缺一不可。

![[assets/figures/papers/paper_list_l2669_https_arxiv_org_abs_2512_23333/figures/005_Table_2.jpg]]
*Table 2: Results of Multi-Expert learning compared to individual Expert learning.The table shows four sections: performance of a single expert with SFT, performance with multi-expert data in SFT, performance of a single expert with both SFT and GRPO, and the final results of our approach*

## 定位与知识库关联

### 任务定位与核心瓶颈

CME-CAD 面向从二维工程图（三视图）生成精确可执行的 CADQuery 代码这一高难度任务。该任务的核心挑战在于：生成的代码不仅需要语法正确、可执行，还必须满足严格的几何精度、约束兼容性和可编辑性要求。现有的基于可验证奖励的强化学习方法（如 **CAD-RL** (Niu et al., arXiv 2025)）本质上是 on-policy 的，倾向于沿着奖励丰富的现有推理路径进行优化，难以主动探索新的知识与推理路径。单一专家模型的推理路径受限，导致在复杂推理场景中性能难以突破。

### 与基线方法的差异化定位

**CAD-RL** (Niu et al., arXiv 2025) 是当前基于强化学习的可执行 CAD 代码生成方法的 SOTA，其核心思路是将 GRPO 应用于 CAD 代码生成，通过可执行性奖励和几何一致性奖励引导模型优化。然而，CAD-RL 仍采用单专家训练范式，推理路径多样性受限于单一模型的认知边界。CME-CAD 在 CAD-RL 的基础上，将单专家 GRPO 扩展为多专家协作学习框架，通过引入异构专家的差异化推理路径，从根本上扩大了探索空间。

**CAD-Coder** (Guan et al., arXiv 2025) 是 SOTA 的基于思维链与几何奖励的文本转 CAD 代码方法，侧重于通过精心设计的思维链提示和几何奖励函数提升生成质量。CME-CAD 同样利用思维链推理，但通过多专家微调（MEFT）阶段生成不同风格的推理路径，并在强化学习阶段实现跨专家知识迁移，从而在推理多样性上超越了单专家思维链方法的固有上限。

**CAD-MLLM** (Xu et al., arXiv 2024) 和 **GenCAD** (Alam et al., arXiv 2024) 分别代表了多模态大语言模型和图像条件 Transformer 在 CAD 生成中的早期探索。这些方法主要依赖监督微调或扩散先验，缺乏对可执行性和几何精度的显式强化学习优化。CME-CAD 的门控总奖励函数（格式 + 可执行性作为必要门控条件，结合 IoU 和坐标平面一致性奖励）为 CAD 代码生成提供了更全面的优化信号。

### 方法谱系中的关键创新点

| 维度 | 基线方法（单专家 RLVR） | CME-CAD |
|------|------------------------|---------|
| 训练范式 | 单专家 SFT + 标准 GRPO | 多专家微调（MEFT）+ 多专家强化学习（MERL） |
| 推理路径多样性 | 单一风格的推理路径 | 多个异构专家生成不同风格的推理路径，通过协作学习融合 |
| 奖励函数 | 通常仅依赖可执行性或几何一致性 | 门控总奖励：格式 + 可执行性门控 × (IoU + 平面一致性) |
| 探索能力 | 标准 GRPO 可能抑制探索 | 非负优势截断（max(A, 0)），硬负样本缓冲机制持续训练困难样本 |

### 适用边界与局限

1. **领域语言依赖**：当前方法仅针对 CADQuery 代码生成设计，是否能够扩展到其他 CAD 脚本语言（如 OpenSCAD）或直接生成参数化特征树尚待研究。

2. **输入质量假设**：论文未说明该方法在只有部分标注或手绘工程图上的泛化能力，实际工业应用中图纸质量参差不齐，可能影响模型性能。

3. **计算资源需求**：尽管训练时间仅增加 20–30%，但多专家训练仍需要额外内存和计算资源。能否在更轻量模型上有效应用需要验证。

4. **复杂产品场景未覆盖**：对于需要装配体或运动学仿真的复杂产品，该方法是否仍能保持精度和编辑性未作讨论。

5. **硬负样本机制的依赖性**：硬负样本缓冲机制（HSB）依赖预先收集的数据，如果所有专家都无法生成正确输出，该方法能否持续改进缺乏理论保证。

### 开放问题

- 该方法能否与参数化特征树生成方法结合，进一步提升 CAD 模型的可编辑性和结构化程度？
- 在工业级大规模数据集上，异构专家数量的最优选择策略是什么？专家间的互补性如何量化？
- 门控奖励函数中的权重系数（λ）对最终性能的敏感性如何？是否存在自适应调节机制的空间？

## 原文 PDF

![[paperPDFs/CVPR_2026/CME_CAD_Heterogeneous_Collaborative_Multi_Expert_Reinforcement_Learning_for_CAD_Code_Generation.pdf]]
