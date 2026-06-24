---
title: "Agent4FaceForgery: Multi-Agent LLM Framework for Realistic Face Forgery Detection"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Agent4FaceForgery_Multi_Agent_LLM_Framework_for_Realistic_Face_Forgery_Detection.pdf
project_link: null
code_link: null
aliases:
- Agent4FaceForgery
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过LLM驱动的多智能体系统模拟从伪造创作到社交传播的完整生命周期，生成富含意图、过程和社交上下文的多模态训练数据（特别是图文不一致样本），从而提升检测器的泛化性。
primary_logic: 将数据生成过程解耦为“伪造蓝图”生成（Phase 1）和社会模拟（Phase 2）两个阶段，先保证伪造任务的结构正确性，再填充自然的多轮对话细节，以克服单步错误累积和复杂依赖维护的难题。
claims:
- LLaVA模型在使用Agent4FaceForgery数据微调后，在Celeb-DF上的AUC从基线51.8%大幅提升至92.2%，证明了生成数据的有效性。
- 跨数据集泛化能力显著增强，在WildDeepfake和Celeb-DF上分别取得86.50%和87.10%的AUC，优于仅使用静态数据集训练的检测器。
- 在DF40协议下，面对六种先进伪造技术仍保持高鲁棒性，平均AUC达93.9%。
- 社会模拟与正负样本构造（PNS）使得检测器能有效识别图文不一致攻击，HighCritic环境下不一致检测准确率约88.7%。
---

# Agent4FaceForgery: Multi-Agent LLM Framework for Realistic Face Forgery Detection

> [!tip] 核心洞察
> 将数据生成过程解耦为“伪造蓝图”生成（Phase 1）和社会模拟（Phase 2）两个阶段，先保证伪造任务的结构正确性，再填充自然的多轮对话细节，以克服单步错误累积和复杂依赖维护的难题。

| 字段 | 内容 |
|------|------|
| 中文题名 | Agent4FaceForgery：面向逼真面部伪造检测的多智能体大语言模型框架 |
| 英文题名 | Agent4FaceForgery: Multi-Agent LLM Framework for Realistic Face Forgery Detection |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.12546) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Agent4FaceForgery |
| Dataset | Celeb-DF, WildDeepfake, DF40 |

> [!tip] 效果简介
> - Celeb-DF (CDF) 上，AUC (%) 92.2 vs 51.8 (+40.4)。
> - WildDeepfake (WDF) 上，AUC (%) 86.50。
> - DF40 (FF++ six advanced techniques) 上，Average AUC (%) 93.9。

## 概述

### 问题与瓶颈

深度伪造检测领域面临一个根本性瓶颈：**训练数据的生态无效性**。现有方法依赖静态基准数据集（如FF++），这些数据集由人工策划，无法捕捉真实世界中伪造创作的多样化意图、迭代过程以及社交媒体中的多模态交互。这导致检测器在实验室环境表现良好，但在真实部署场景中泛化能力急剧下降——例如，仅用FF++训练的LLaVA基线模型在Celeb-DF上AUC仅为51.8%，几乎等同于随机猜测。

### 核心思路

Agent4FaceForgery 提出了一种范式转变：**不再从数据中学习检测，而是让检测器从模拟的伪造生命周期中学习**。该框架利用大语言模型（LLM）驱动的多智能体系统，完整模拟从伪造创作到社交传播的全过程，生成富含意图、过程和社交上下文的多模态训练数据。

核心创新在于将数据生成过程**解耦为两个阶段**（Figure 2）：

- **Phase 1（伪造蓝图生成）**：智能体根据从FF++数据集中初始化的Profile（量化特质与风格品味），通过Memory模块进行迭代学习，经由Action模块执行视觉编辑操作链，生成结构正确的伪造样本。Adaptive Rejection Sampling（ARS）机制作为动态质量过滤器，融合LLM自评与外部判别器评分，自适应地筛选高挑战性样本。

- **Phase 2（社会模拟与正负样本构造）**：引入五种不同用户角色（Watcher、Explorer、Critic、Chatter、Poster），模拟多用户围绕伪造图像的交互行为。通过构造图文不一致的负样本（δ标签），使检测器学会识别社交媒体中常见的“图像伪造但文本声称真实”等对抗性场景。

### 关键结论

实验验证了该方法的有效性，主要结果如下：

- **域内性能跃升**：使用Agent4FaceForgery数据微调后，LLaVA模型在Celeb-DF上的AUC从51.8%提升至92.2%（+40.4个百分点），在WildDeepfake上达到86.50%。

- **跨操纵技术鲁棒性**：在DF40协议下，面对六种先进伪造技术（包括换脸、面部重演等），平均AUC达到93.9%，展现了极强的泛化能力（Table 2）。

- **模块贡献清晰**：消融实验表明，社会模拟与正负样本构造（PNS）模块贡献最大（单独使用可达91.0% AUC），伪造树模拟（FT）模块单独使用为83.2%，ARS的增量过滤进一步将完整系统推至92.2%（Table 6）。

- **对抗鲁棒性**：在HighCritic社会环境下训练的检测器，对图文不一致攻击的识别准确率约88.7%，验证了框架生成的对抗性数据对提升检测器鲁棒性的关键作用（Figure 3b）。

### 方法谱系与知识库定位

Agent4FaceForgery 在方法谱系中占据独特位置：它不同于传统的基于CNN的检测器（如**Xception**，Chollet 2017）或频域方法（如**SPSL**，Liu et al., CVPR 2021），也不仅仅是多模态检测器（如**M2TR**，Wang et al., 2022）的改进，而是从根本上重新定义了训练数据的生成范式。与CLIP-ViT（Radford et al., 2021）和LLaVA（Liu et al., 2024）等视觉-语言模型的关系是互补的——Agent4FaceForgery为这些模型提供高质量、上下文化的微调数据，而非替代其架构。

该工作可定位于**数据中心AI**与**多智能体模拟**的交叉领域，其核心贡献在于证明了：通过LLM驱动的生成式模拟构建的训练数据，能够有效弥补静态数据集与真实世界部署之间的生态鸿沟。

## 背景与动机

### 面部伪造检测的现实困境

深度伪造（Deepfake）技术的快速演进使得逼真面部伪造的检测成为计算机视觉与多媒体安全领域的核心挑战。现有检测方法——无论是基于CNN的**Xception**（Chollet, 2017）、频域方法**SPSL**（Liu et al., CVPR 2021）、多模态Transformer **M2TR**（Wang et al., 2022），还是视觉-语言模型**CLIP-ViT**（Radford et al., 2021）与多模态大语言模型**LLaVA**（Liu et al., 2024）——在静态基准数据集上已取得可观性能，但在真实场景中的泛化能力始终是瓶颈。

这一瓶颈的根源在于训练数据的**生态无效性**：现有数据集（如FF++）由人工策划生成，采用固定的伪造算法和单一的生成逻辑，未能捕捉真实世界中面部伪造创作的核心特征——多样化的伪造意图、迭代优化的制作过程，以及社交媒体中伪造图像与用户评论之间的多模态交互。换言之，检测器在实验室中学会识别的是“数据集中的伪造模式”，而非“真实世界中的伪造行为模式”。

### 从数据驱动到行为驱动的范式转变

Agent4FaceForgery的核心洞察在于：**要提升检测器的真实场景泛化性，必须让训练数据反映伪造行为的完整生命周期**——从伪造者的创作意图与迭代编辑，到社交媒体中多角色围绕图像真实性的自然讨论。这需要将数据生成从“静态样本收集”转变为“动态行为模拟”。

然而，端到端地模拟这一完整生命周期面临两个关键难题：
- **复杂依赖维护**：伪造创作涉及意图、工具选择、编辑序列之间的因果链，单步生成容易累积错误；
- **多模态一致性**：社交媒体中的图文交互要求文本描述与视觉内容高度对齐，否则会产生误导性训练信号。

### 本文的解决思路

针对上述挑战，Agent4FaceForgery提出将数据生成过程解耦为两个阶段：

1. **伪造蓝图生成（Phase 1）**：由LLM驱动的生成智能体（Generative Agent）基于可量化的特质画像（Profile）与迭代记忆（Memory），生成结构正确的“伪造蓝图”——包括目标选择、编辑算子序列和文本描述，确保伪造任务的结构正确性；
2. **社会模拟（Phase 2）**：多角色智能体（Watcher、Explorer、Critic、Chatter、Poster）在模拟社交媒体环境中与伪造图像交互，填充自然的多轮对话细节，并构造图文不一致样本以训练检测器识别对抗性文本攻击。

通过自适应拒绝采样（Adaptive Rejection Sampling, ARS）机制动态筛选高质量挑战样本，以及正负样本构造（Positive-Negative Sample construction, PNS）策略显式建模图文一致性标签，框架生成的多模态训练数据使检测器不仅能识别视觉伪造痕迹，还能捕捉文本-图像之间的语义矛盾——这是现有方法普遍缺失的能力。

## 核心创新

Agent4FaceForgery 的核心创新在于将面部伪造检测的数据生成范式从“静态标注”转变为“动态模拟”。传统方法依赖人工策划的基准数据集（如 FF++），其标签仅为图像级的二元真实性标签，无法反映真实世界中伪造创作的多样化意图、迭代过程以及社交媒体中的多模态交互。Agent4FaceForgery 通过以下四个关键维度的创新，系统性地解决了这一瓶颈。

### 1. 训练数据来源：从静态基准到多智能体动态模拟

传统检测器仅在 FF++ 等静态数据集上训练，数据生态缺乏多样性和上下文信息。Agent4FaceForgery 引入了一个由 LLM 驱动的多智能体系统，完整模拟从伪造创作到社交传播的生命周期。该系统包含两个核心阶段：**Phase 1** 生成结构正确的“伪造蓝图”，**Phase 2** 在此基础上进行多用户角色的社会模拟。这种动态生成机制使得训练数据能够覆盖更广泛的伪造痕迹和社交上下文，从根本上提升了检测器的泛化能力。

### 2. 数据标签类型：从图像真实性到图文一致性

传统方法仅提供图像级的真实/伪造标签，无法应对社交媒体中常见的图文不一致攻击（例如，真实图像被配上误导性文字描述）。Agent4FaceForgery 引入了一个新的标签维度 $\delta$，用于标记图文是否匹配。负样本（$\delta=1$）定义为：真实图像被描述为“伪造”或伪造图像被描述为“真实”的情况。这一设计使得检测器不仅学习判断图像真伪，还能识别文本描述与视觉证据之间的矛盾，从而更贴近真实应用场景。

### 3. 数据生成机制：从人工策划到智能体自主迭代

传统数据增强依赖预设规则，缺乏对伪造创作中意图和迭代过程的建模。Agent4FaceForgery 为每个智能体配备了三个核心模块：
- **Profile Module**：定义智能体的量化特质和风格品味，初始化其行为偏好；
- **Memory Module**：存储事实性和评价性记忆，支持回顾与 LLM 驱动的反思，驱动迭代学习；
- **Action Module**：将意图转化为具体的视觉编辑操作和文本描述，形式为 $(\mathrm{Edit}(\cdot), \mathrm{Desc}(\cdot))$ 对。

配合 **Adaptive Rejection Sampling (ARS)** 机制——通过融合 LLM 自评分数 $s_i^{\mathrm{LLM}}$ 与外部判别器分数 $s_i^{\mathrm{disc}}$ 的加权和 $s_i = \lambda s_i^{\mathrm{LLM}} + (1 - \lambda) s_i^{\mathrm{disc}}$，并采用自适应阈值 $\tau = \mathrm{Quantile}(\{\text{Accepted Samples}\}, q)$ 进行动态筛选——系统能够自动过滤低质量样本，保留高挑战性的训练数据。

### 4. 社交上下文建模：从无到多角色社会模拟

传统检测器完全忽略了图像在社交媒体中的传播和讨论动态。Agent4FaceForgery 在 Phase 2 中引入了五种由 MLLM 驱动的用户角色（Watcher、Explorer、Critic、Chatter、Poster），模拟多用户对伪造图像的查看、评论、分享和标记行为。特别地，**Gemini Auditor** 角色会故意生成具有欺骗性的陈述，制造图文不一致的对抗性样本。这种社会模拟使得训练数据天然包含正负样本对，显著增强了检测器对社交上下文中伪造信息的识别能力。

### 创新有效性验证

消融实验直接验证了上述创新的贡献。在 Celeb-DF 数据集上，基线 LLaVA 模型（仅在 FF++ 上训练）的 AUC 仅为 51.8%。逐步引入各模块后：**FT 模块**（伪造树模拟）单独使用将 AUC 提升至 83.2%；**PNS 模块**（正负样本构造）单独使用可达 91.0%；完整框架（FT+ARS+PNS）最终达到 92.2% AUC，各模块均展现出增量贡献。跨数据集泛化实验进一步表明，该方法在 WildDeepfake（86.50%）和 Celeb-DF（87.10%）上均显著优于传统静态数据训练的检测器。

## 整体框架

Agent4FaceForgery 的核心设计理念是将逼真面部伪造检测的数据生成过程解耦为两个阶段，以克服单步错误累积和复杂依赖维护的难题。整体框架由 **LLM赋能的生成式智能体（Generative Agents）** 和 **媒体展示环境（Media Presentation Environment）** 两大核心部分组成，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2370_https_arxiv_org_abs_2509_12546/figures/002_Figure_2.jpg]]
*Figure 2: The overall framework of Agent4FaceForgery. Our simulator consists of two core facets: LLM-empowered Generative Agents and a Media Presentation Environment. Agent profiles are initialized using datasets characterizing real media. Agents, enhanced with specialized memory and action modules tailored for media evaluation and authenticity assessment scenarios, simulate a wide range of behaviors including viewing content, evaluating authenticity, flagging suspicious items, sharing media, ignoring content, and potentially participating in discussion*

### 两阶段生成管线

**Phase 1：伪造蓝图生成（Forged Blueprint Generation）**
此阶段负责生成结构正确、语义合理的伪造任务描述。智能体首先通过分析 FF++ 基准数据集进行 Profile 初始化，获取量化特质向量和风格品味描述。随后，智能体利用 Memory 模块存储事实性和评价性记忆，并通过 LLM 驱动的反思机制进行迭代学习。Action 模块将智能体的意图转化为具体的视觉编辑操作和文本描述对 `(Edit(·), Desc(·))`，其中视觉编辑通过顺序应用伪造算子链实现：

$$\operatorname{Edit}(\mathbf{x}; \mathbf{p}_k, \mathcal{M}_k) = O_n \big( \cdots O_1(\mathbf{x}; \theta_1) \cdots ; \theta_n \big)$$

生成的候选蓝图经过 **自适应拒绝采样（Adaptive Rejection Sampling, ARS）** 进行质量控制。ARS 采用融合评分机制筛选高质量样本：

$$s_i = \lambda s_i^{\mathrm{LLM}} + (1 - \lambda) s_i^{\mathrm{disc}}$$

其中 $s_i^{\mathrm{LLM}}$ 为 LLM 自评质量分，$s_i^{\mathrm{disc}}$ 为外部判别器评分。在热身阶段后，接受阈值动态更新为已接受样本分数的分位数：

$$\tau = \mathrm{Quantile}(\{ s_j \mid j \in \mathrm{Accepted~Samples} \}, q)$$

通过筛选的伪造样本与真实面部样本合并，形成多模态数据集 $\mathcal{D}$。

**Phase 2：社会模拟与交互轨迹收集（Social Interaction Trajectory Collection）**
此阶段将 Phase 1 生成的伪造蓝图置于模拟的社交媒体环境中。框架引入五种由 MLLM 驱动的用户角色——**Watcher**（观察者）、**Explorer**（探索者）、**Critic**（批评者）、**Chatter**（闲聊者）和 **Poster**（发布者）——模拟多样化的用户交互行为，包括查看、评论、分享和标注等。其中，**Gemini Auditor** 专门生成具有意图欺骗性的陈述，以构造对抗性文本样本。

### 正负样本构造（PNS）与标签机制

社会模拟的关键输出是图文一致性标签。负样本的判定函数定义为：

$$\delta ( x', \check{c'} ) = \begin{cases} 1, & \text{if } y = 1 \text{ and } c' \text{ claims ``perfectly real''}, \\ 1, & \text{if } y = 0 \text{ and } c' \text{ claims ``obvious forgery''}, \\ 0, & \text{otherwise} \end{cases}$$

其中 $\delta=1$ 表示负样本（图文不匹配），$\delta=0$ 表示对齐或已纠正的正样本。这一机制使得训练数据不仅包含图像级别的真实性标签，还包含图文一致性的细粒度监督信号，这是本框架区别于传统静态数据集的关键创新点。

### 数据流总结

整个管线的数据流为：**FF++ 基准数据 → Profile 初始化 → 伪造蓝图生成（Phase 1）→ ARS 质量过滤 → 社会模拟交互（Phase 2）→ PNS 正负样本标注 → 多模态训练数据集**。该数据集随后用于微调多模态大语言模型（如 LLaVA）或视觉-语言模型（如 CLIP-ViT），以提升其在真实社交媒体环境中对逼真伪造的检测能力。

## 核心模块与公式推导

### 两阶段解耦生成范式

Agent4FaceForgery 的核心设计洞察在于将数据生成过程解耦为两个独立阶段：**Phase 1** 负责生成结构正确的“伪造蓝图”（forged blueprint），**Phase 2** 则基于该蓝图进行多角色社交模拟，填充自然的多轮对话细节。这一分离策略有效规避了单步生成中常见的错误累积和复杂依赖维护问题。

### Phase 1：伪造蓝图生成

#### 智能体 Profile 模块

每个生成智能体的行为由其 **Profile** 定义，该 Profile 从 FF++ 基准数据集中初始化，包含两个组成部分：

- **可量化特质向量** $v_k$：刻画智能体的行为倾向性
- **风格品味描述**：自然语言形式，定义智能体的美学偏好和伪造风格

Profile 是智能体所有后续决策的基础，决定了其选择何种伪造目标、采用何种操纵技术以及生成何种风格的视觉输出。

#### 智能体 Memory 模块

Memory 模块维护两类记忆以支持迭代学习：

- **事实性记忆**：记录历史操作序列和对应的视觉编辑结果
- **评价性记忆**：存储对过往生成质量的自我评估和外部反馈

该模块支持记忆检索、写入以及基于 LLM 的反思过程，使智能体能够从历史经验中学习并逐步优化其伪造策略。

#### Action 模块与视觉编辑算子链

智能体的行动被形式化为一个二元组 $(\operatorname{Edit}(\cdot), \operatorname{Desc}(\cdot))$，分别对应视觉编辑操作和文本描述。视觉编辑通过算子链实现：

$$\operatorname{Edit}(\mathbf{x}; \mathbf{p}_k, \mathcal{M}_k) = O_n \big( \cdots O_1(\mathbf{x}; \theta_1) \cdots ; \theta_n \big)$$

其中 $\mathbf{x}$ 为输入图像，$\mathbf{p}_k$ 为智能体 $k$ 的 Profile，$\mathcal{M}_k$ 为其 Memory。算子 $O_1, \ldots, O_n$ 从预定义的工具包中顺序选取，参数 $\theta_i$ 由智能体的 Profile 和 Memory 共同决定。这种链式结构使得智能体能够组合多种伪造技术，生成复杂的、多层次的伪造痕迹。

#### 智能体生产力度量

为量化智能体的行为特征，框架定义了三个核心度量指标：

- **伪造频次**：$T_{k}^{\mathrm{freq}} = |\mathrm{forgeries}_k|$，衡量智能体的总产出量
- **方法多样性**：$T_{k}^{\mathrm{div}} = \bigcup_{i \in \mathrm{forgeries}_k} \{ \mathrm{method}_i \}$，统计智能体使用的唯一操纵技术数量
- **目标流行度一致性**：$T_{k}^{\mathrm{conf}} = \frac{1}{|\mathrm{forgeries}_k|} \sum_{i \in \mathrm{forgeries}_k} \mathrm{Pop}(\mathrm{target}_i)$，衡量智能体选择热门伪造目标的倾向性

#### 自适应拒绝采样（ARS）

ARS 作为动态质量过滤器，筛选高质量的伪造蓝图。候选蓝图的评分采用融合度量：

$$s_i = \lambda s_i^{\mathrm{LLM}} + (1 - \lambda) s_i^{\mathrm{disc}}$$

其中 $s_i^{\mathrm{LLM}}$ 为 LLM 自评质量分，$s_i^{\mathrm{disc}}$ 为外部判别器的评分，$\lambda$ 为加权系数。在热身阶段后，接受阈值根据已接受样本的分数分布自适应更新：

$$\tau = \mathrm{Quantile}(\{ s_j \mid j \in \mathrm{Accepted~Samples} \}, q)$$

即阈值设为所有已接受样本分数的 $q$ 分位数，随着高质量样本的积累，阈值逐步收紧，确保只有最具挑战性的样本被保留。

### Phase 2：多角色社交模拟与正负样本构造

#### 五类用户角色

社交模拟阶段引入五种由多模态大语言模型（MLLM）驱动的用户角色：

- **Watcher**：浏览内容但不主动互动
- **Explorer**：深入分析图像真实性
- **Critic**：对图像提出质疑和批评
- **Chatter**：参与随意讨论
- **Poster**：主动分享和传播内容

这些角色围绕 Phase 1 生成的伪造图像进行多轮交互，模拟社交媒体中真实用户对伪造内容的多样化反应。

#### 正负样本标注函数

社交模拟的核心输出是图文一致性标签 $\delta$，用于区分正样本（图文匹配）和负样本（图文不一致）：

$$\delta ( x', \check{c'} ) = \begin{cases} 1, & \text{if } y = 1 \text{ and } c' \text{ claims ``perfectly real''}, \\ 1, & \text{if } y = 0 \text{ and } c' \text{ claims ``obvious forgery''}, \\ 0, & \text{otherwise} \end{cases}$$

其中 $y=1$ 表示真实图像，$y=0$ 表示伪造图像，$c'$ 为生成的评论文本。$\delta=1$ 标识负样本——即文本描述与图像真实状态存在矛盾的情形（如对真实图像声称“完美无瑕”，或对伪造图像声称“明显造假”）；$\delta=0$ 则表示图文对齐或已被纠正的正样本。这一标注机制使检测器能够学习识别图文不一致攻击，而非仅依赖图像本身的伪造痕迹。

#### 对抗性文本生成

在社交模拟中，**Gemini Auditor** 角色专门生成具有故意欺骗性的陈述，例如将明显伪造的图像描述为“绝对真实”，或将真实图像标记为“可疑”。这些对抗性文本与 HighCritic 环境配置相结合，训练出的检测器在图文不一致识别上表现出最强鲁棒性（约 88.7% 不一致检测准确率）。

### 补充图表

![[assets/figures/papers/paper_list_l2370_https_arxiv_org_abs_2509_12546/figures/001_Figure_1.jpg]]
*Figure 1: The illustrative example of our proposed agentbased social simulation. Diverse agents engage in a humanlike deliberation on the image’s authenticity*

## 实验与分析

### 核心实验结果

Agent4FaceForgery 框架的核心验证围绕生成数据的有效性与检测器泛化能力展开。实验采用 LLaVA（Liu et al., 2024）作为基础多模态大语言模型检测器，基线模型仅在 FF++ 数据集上训练，在 Celeb-DF（CDF）上的 AUC 仅为 51.8%。完整框架（FT+ARS+PNS）在相同条件下将 AUC 提升至 **92.2%**，增幅达 40.4 个百分点（Table 6）。这一跃升直接验证了核心洞察：模拟完整伪造生命周期所生成的数据，能够填补静态数据集与真实检测需求之间的生态鸿沟。

![[assets/figures/papers/paper_list_l2370_https_arxiv_org_abs_2509_12546/figures/006_Table_6.jpg]]
*Table 6: Ablation study regarding the effectiveness of each proposed module via cross-dataset evaluation. The results show an incremental benefit in each module*

跨数据集泛化评估（Table 1）进一步支撑该结论。在 WildDeepfake 和 Celeb-DF 两个分布外数据集上，Agent4FaceForgery 增强的检测器分别取得 **86.50%** 和 **87.10%** 的 AUC，优于仅使用静态数据集训练的对比方法。这表明生成数据中嵌入的多样化伪造意图与社交上下文，有效提升了检测器对未知伪造模式的适应能力。

![[assets/figures/papers/paper_list_l2370_https_arxiv_org_abs_2509_12546/figures/003_Table_1.jpg]]
*Table 1: Frame-level cross-database evaluation from FF++(HQ) to DFD, DFDC-P, Wild Deepfake, and Celeb-DF in terms of AUC (%) and EER (%). The FF++ results represent intra-domain performance, while others represent generalization to unseen domains. The best results are indicated in bold, and the second-best results are underlined*

鲁棒性测试采用 DF40 协议（Table 2），评估检测器面对六种先进伪造技术（如 uniface、e4s、simswap 等）时的表现。Agent4FaceForgery 增强模型取得平均 **93.9%** 的 AUC，证明 ARS 机制筛选的高难度样本与多样化智能体 Profile 所覆盖的广泛伪造痕迹谱系，显著增强了检测器对各类操纵算法的鲁棒性。

![[assets/figures/papers/paper_list_l2370_https_arxiv_org_abs_2509_12546/figures/004_Table_2.jpg]]
*Table 2: Assessing detector robustness to diverse manipulation algorithms within the FF++ dataset. We report frame-level AUC (%) against six techniques specified in DF40 (Yan et al. 2024b)*

### 消融研究

消融实验（Table 6）逐模块拆解了各组件对最终性能的贡献。以 LLaVA 在 Celeb-DF 上的 AUC 为指标：

- **FT 模块**（Forgery Tree 模拟）单独使用将 AUC 从基线 51.8% 提升至 **83.2%**，证明结构化伪造蓝图生成本身已具备显著的数据增强价值。
- **PNS 模块**（正负样本构造）贡献最为突出，单独使用可达 **91.0%** AUC，表明图文不一致样本的引入是性能跃升的关键杠杆。
- **ARS 模块**（自适应拒绝采样）与 FT 协同使用时进一步推高至 92.2%，验证了动态质量过滤对样本难度的精准调控作用。

智能体数量消融（Table 7）揭示了收益递减规律：将社会模拟中的智能体从 6 个增至 12 个时，Celeb-DF AUC 仅从 85.3% 微升至 **85.8%**。这一发现为计算成本与性能之间的权衡提供了实证依据——6 个智能体已能捕捉足够的社交交互多样性。

![[assets/figures/papers/paper_list_l2370_https_arxiv_org_abs_2509_12546/figures/009_Table_7.jpg]]
*Table 7: Ablation on the number of agents in the social simulation. Performance is evaluated on the DFD and Celeb-DF datasets. The results show diminishing returns as the number of agents increases, with 12 agents providing only marginal gains over 6, which justifies our agent count configuration and balances performance with computational cost*

顺序训练策略消融（Table 4）表明，先以 FF++ 预训练再以 Agent4FaceForgery 数据微调的策略，在 Xception、CLIP-ViT、LLaVA 等多个骨干网络上均带来显著提升，验证了生成数据作为增强源的通用适配性。

![[assets/figures/papers/paper_list_l2370_https_arxiv_org_abs_2509_12546/figures/007_Table_4.jpg]]
*Table 4: Ablation on the sequential training strategy. Models are first pre-trained on a base dataset and then fine-tuned with data generated by Agent4FaceForgery (A4FF). The results demonstrate significant performance improvements across multiple backbone models, confirming the effectiveness of our generated data for augmentation*

### 智能体行为与社交环境影响

Figure 3a 展示了不同 Profile 配置下智能体伪造逃避能力的动态演变。**Stealthy** 配置的智能体生成最具对抗性的伪造，将检测 AUC 逐步压低至约 **48.5%**，几近随机猜测水平。这一定量证据表明，通过调节智能体的意图参数（Profile），可以系统性地生成从“易检测”到“高对抗”的连续难度样本。

Figure 3b 对比了不同社交环境下训练的 MLLM 检测准确率。**HighCritic** 环境（高比例质疑型用户）训练出的检测器在图文不一致识别上表现最强，不一致检测准确率约 **88.7%**，但同时 CDF 整体准确率降至约 78.6%。这一权衡揭示了社交环境的“质疑强度”与检测器“整体精度”之间的张力——过度强调质疑可能引入假阳性风险，需在实际部署中根据场景需求调节社交角色配比。

### 标注质量分析

Table 3 从标注质量角度评估了 Agent4FaceForgery 生成的文本描述。智能体生成的标注在精确率上达到 **94.41%**，F1 分数为 69.06%，优于直接使用 MLLM 生成的基线标注。高精确率表明智能体的 Memory 模块与 PNS 机制有效抑制了幻觉——生成的文本描述与视觉证据高度对齐，减少了“无中生有”的错误归因。F1 分数的提升空间则指向召回率的进一步优化方向。

![[assets/figures/papers/paper_list_l2370_https_arxiv_org_abs_2509_12546/figures/005_Table_3.jpg]]
*Table 3: Comparison of different annotation approaches. We report precision, recall and F1-score for annotation quality evaluation, AUC (%) and EER for CLIP-based forgery detection and ACC (%) and explanation quality (Precision/Recall) for MLLMs evaluation on FF++ and Celeb-DF (CDF) datasets*

### 补充图表

![[assets/figures/papers/paper_list_l2370_https_arxiv_org_abs_2509_12546/figures/010_Figure_3.jpg]]
*Figure 3: Left (a): Comparison of forgery evasion capability (AUC, lower is better) evolution over simulation time for Agents with different profiles. Right (b): Comparison of MLLM detection accuracy (Inconsistency vs. Overall) when trained on data generated under different Social Environment configurations*

![[assets/figures/papers/paper_list_l2370_https_arxiv_org_abs_2509_12546/figures/008_Table_5.jpg]]
*Table 5: Results of different backbone models with and without Agent4FaceForgery on different datasets*

![[assets/figures/papers/paper_list_l2370_https_arxiv_org_abs_2509_12546/figures/013_Figure_4.jpg]]
*Figure 4: Qualitative examples in challenge scenarios*

![[assets/figures/papers/paper_list_l2370_https_arxiv_org_abs_2509_12546/figures/014_Figure_5.jpg]]
*Figure 5: Qualitative examples of Agent-Generated Images*

## 方法谱系与知识库定位

### 1. 问题定位：从静态检测到生态模拟

现有面部伪造检测的研究主线长期围绕**静态基准数据集**展开，代表性工作包括基于CNN的**Xception**（Chollet, 2017）、视觉-语言模型**CLIP-ViT**（Radford et al., 2021）以及多模态大语言模型**LLaVA**（Liu et al., 2024）。这些方法的共同假设是：训练集与测试集的伪造分布足够相似，检测器可以通过在FF++等数据集上学习伪造痕迹来完成泛化。

然而，这一假设在真实环境中遭遇系统性失效。核心瓶颈在于**训练数据的生态无效性**——静态数据集无法捕捉人类伪造创作中的多样化意图、迭代优化过程以及社交媒体中的多模态交互链条。具体表现为三个断层：

- **意图断层**：真实伪造者具有特定的欺骗动机和风格偏好，而数据集中的伪造操作是机械化的、无上下文的；
- **过程断层**：实际伪造往往经过多次试错与迭代优化，而数据集仅提供单次操作的最终产物；
- **交互断层**：社交媒体中图像与文本评论之间存在复杂的图文不一致攻击（如伪造图像配以“绝对真实”的文字声明），而传统数据集仅提供图像级二元标签。

Agent4FaceForgery的核心洞察在于：**将数据生成过程解耦为“伪造蓝图”生成（Phase 1）和社会模拟（Phase 2）两个阶段**，先保证伪造任务的结构正确性，再填充自然的多轮对话细节，以克服单步错误累积和复杂依赖维护的难题。

### 2. 与现有数据增强方法的对比

相较于传统的数据增强思路，Agent4FaceForgery在多个维度上实现了方法论的跃迁：

| 方法维度 | 基线方法 | Agent4FaceForgery |
|---------|---------|-------------------|
| **训练数据来源** | 静态基准数据集（如FF++） | 多智能体模拟生成的动态、多模态、上下文化数据集 |
| **数据标签类型** | 图像级二元真实性标签（真实/伪造） | 图文一致性标签（δ）与图像真实性标签结合 |
| **数据生成机制** | 人工策划或简单数据增强 | 基于LLM智能体的Profile、Memory、Action模块的自动迭代伪造生成，配合ARS质量控制 |
| **社交上下文建模** | 无或有限 | 多角色社会模拟（Watcher、Critic、Gemini Auditor等）生成多样化评论和对抗性文本 |

其中，**图文一致性标签（δ）** 的引入是一个关键的差异化设计。传统方法仅区分图像是否被篡改，而Agent4FaceForgery通过负样本标记函数δ区分“图文一致”与“图文不一致”样本——例如，当一张真实图像（y=1）被配以“明显是伪造的”评论时，该样本被标记为负样本（δ=1），迫使检测器学习跨模态的语义对齐关系。

### 3. 与频域/多模态检测方法的关系

在检测器层面，Agent4FaceForgery与**SPSL**（Liu et al., CVPR 2021）等频域方法以及**M2TR**（Wang et al., 2022）等多模态多尺度Transformer检测器形成互补而非替代关系。SPSL和M2TR关注的是**检测器架构层面的改进**——前者利用频域相位谱捕捉伪造痕迹，后者通过多模态多尺度注意力机制融合不同来源的特征。而Agent4FaceForgery的核心贡献在于**训练数据层面的革新**：通过LLM驱动的多智能体系统模拟从伪造创作到社交传播的完整生命周期，生成富含意图、过程和社交上下文的多模态训练数据。

实验证据表明，这种数据层面的革新对多种检测器架构均有效。在顺序训练策略下（先预训练FF++，再微调A4FF数据），包括Xception、CLIP-ViT、LLaVA在内的多个骨干网络均获得显著性能提升（Table 4），说明Agent4FaceForgery生成的数据具有**架构无关的通用增强能力**。

### 4. 适用边界与局限

尽管Agent4FaceForgery在跨数据集泛化和鲁棒性方面表现出色，其适用边界仍需审慎界定：

**（1）对LLM能力的依赖**：框架的核心机制——Profile初始化、Memory反思、ARS质量评分——均依赖LLM的推理和生成能力。在LLM对细粒度视觉伪造痕迹理解不足的场景下，生成数据的质量可能下降。当前分析中未提供针对不同LLM骨干的消融实验，这一点需要人工验证。

**（2）计算成本与收益递减**：消融实验表明，智能体数量从6增至12时，Celeb-DF AUC仅从85.3%提升至85.8%（Table 7），显示出明显的收益递减。这意味着框架的性能上限可能受限于模拟的边际信息增益，而非算力的持续投入。

**（3）社交模拟的生态效度**：虽然五种用户角色（Watcher、Explorer、Critic、Chatter、Poster）覆盖了主要的社交互动模式，但真实社交媒体中存在更复杂的动态——如信息级联、群体极化、对抗性水军等——这些在当前框架中尚未建模。

**（4）伪造技术的覆盖范围**：尽管在DF40协议下面对六种先进伪造技术取得了93.9%的平均AUC，但该评估仍局限于已知伪造技术类别。对于完全未知的、基于新范式的伪造方法（如神经辐射场生成的3D人脸），框架的泛化能力尚未得到验证。

### 5. 开放问题

Agent4FaceForgery的开源范式提出了若干值得后续探索的方向：

- **多模态智能体的自我进化**：当前智能体的Profile在初始化后保持相对固定，是否可以让智能体在模拟过程中根据反馈动态调整其伪造策略，形成“伪造者-检测器”的对抗性共同进化？
- **跨模态不一致的细粒度建模**：δ标签当前是二值的（一致/不一致），是否可以引入连续的不一致程度度量，捕捉从“微妙暗示”到“公然矛盾”的语义梯度？
- **社交传播动力学**：当前Phase 2模拟的是围绕单张图像的静态交互，是否可以扩展为包含转发、二次创作、信息衰减等传播动力学的时间序列模型？

这些问题指向一个更宏大的方向：将面部伪造检测从“静态分类任务”重新定义为“动态生态中的持续适应问题”，而Agent4FaceForgery为此提供了可行的技术基座。

## 原文 PDF

![[paperPDFs/CVPR_2026/Agent4FaceForgery_Multi_Agent_LLM_Framework_for_Realistic_Face_Forgery_Detection.pdf]]
