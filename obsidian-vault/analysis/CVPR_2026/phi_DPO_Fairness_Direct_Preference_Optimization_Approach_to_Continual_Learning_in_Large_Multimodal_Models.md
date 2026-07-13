---
title: "$\\phi$-DPO: Fairness Direct Preference Optimization Approach to Continual Learning in Large Multimodal Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/phi_DPO_Fairness_Direct_Preference_Optimization_Approach_to_Continual_Learning_in_Large_Multimodal_Models.pdf
project_link: "http://uark-cviu.github.io/projects/Fai-DPO"
code_link: null
aliases:
- DF
- PDFDPOACLLMM
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过引入带有聚焦参数γ的Fair DPO损失函数，动态调制不同数据子组的梯度贡献，使得梯度更新在组间趋于平衡，从而解决数据不平衡带来的偏见问题。
primary_logic: 将持续学习形式化为带KL约束的RLHF问题，通过直接偏好优化 (DPO) 隐式实现遗忘抑制，并进一步提出Fair DPO损失，利用类似Focal Loss的调制因子（(1-p)^γ）对DPO梯度进行重加权，以使各数据组的梯度贡献均衡化，理论上保证在γ足够大时不平衡偏差趋近于零。
claims:
- DPO损失可以同时提供KL散度的下界和上界，从而在理论上保证遗忘抑制优于知识蒸馏。
- 在严重数据不平衡条件下，Fair DPO损失能够使梯度更新在各组间达到平衡，不平衡偏差B_γ(θ)随γ增大而趋近于零。
- 在三个多模态持续学习基准（CoIN, MLLM-CL Domain, MLLM-CL Ability）上，ϕ-DPO在所有指标上均达到最优，并在MLLM-CL Domain上实现近零遗忘（BWT=-0.37%）。
- MLLM-CL Domain 上 MFT↑ = 74.29
---

# $\phi$-DPO: Fairness Direct Preference Optimization Approach to Continual Learning in Large Multimodal Models

> [!tip] 核心洞察
> 将持续学习形式化为带KL约束的RLHF问题，通过直接偏好优化 (DPO) 隐式实现遗忘抑制，并进一步提出Fair DPO损失，利用类似Focal Loss的调制因子（(1-p)^γ）对DPO梯度进行重加权，以使各数据组的梯度贡献均衡化，理论上保证在γ足够大时不平衡偏差趋近于零。

| 字段 | 内容 |
|------|------|
| 中文题名 | ϕ-DPO：面向大型多模态模型持续学习的公平性直接偏好优化方法 |
| 英文题名 | $\phi$-DPO: Fairness Direct Preference Optimization Approach to Continual Learning in Large Multimodal Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Truong_phi-DPO_Fairness_Direct_Preference_Optimization_Approach_to_Continual_Learning_in_CVPR_2026_paper.html) · [Project](http://uark-cviu.github.io/projects/Fai-DPO) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | ϕ-DPO (FaiDPO) |
| Dataset | MLLM-CL Domain, MLLM-CL Ability, CoIN |

> [!tip] 效果简介
> - MLLM-CL Domain 上，MFT↑ 74.29 vs 73.85 (HiDe*) (+0.44)。
> - MLLM-CL Ability 上，MFN↑ 45.31 vs 43.81 (HiDe*) (+1.50)。
> - CoIN 上，MAA↑ 74.94 vs 74.89 (CoIN*) (+0.05)。

## 概要

大型多模态模型（LMM）在持续学习中面临一个核心瓶颈：不平衡的数据分布导致梯度更新向多数类倾斜，损害先前知识的保持与新任务的适应能力。现有方法如知识蒸馏（KD）和LoRA系列技术未能有效缓解这种数据偏见，在多模态持续学习基准上仍出现显著的灾难性遗忘与组间性能差异。

本文提出 **ϕ-DPO（FaiDPO）** 框架，其核心洞察是将持续学习形式化为带KL约束的RLHF问题，通过直接偏好优化（DPO）隐式实现遗忘抑制，并进一步引入**Fair DPO损失**——利用类似Focal Loss的调制因子 $(1-p)^\gamma$ 对DPO梯度进行重加权，使各数据组的梯度贡献趋于均衡。理论上，当聚焦参数 $\gamma$ 足够大时，不平衡偏差 $B_\gamma(\theta)$ 趋近于零（Lemma 3）。

在三个多模态持续学习基准（CoIN、MLLM-CL Domain、MLLM-CL Ability）上，ϕ-DPO在所有指标上均达到最优：在MLLM-CL Domain上实现近零遗忘（BWT=-0.37%），在MLLM-CL Ability上MFN指标达到45.31（较HiDe*提升+1.50），在CoIN上MAA指标达到74.94。消融实验证实Fair DPO损失相比标准DPO和KD在所有指标上均有一致提升，且该方法在LLaVA-13B等更大规模模型上展现出良好的可扩展性。

大型多模态模型（LMMs）在持续学习场景中面临一个核心瓶颈：**数据分布的不平衡导致梯度更新系统性偏向多数类**，从而损害先前知识的保持和对新任务的适应能力。这一问题在多模态持续学习中尤为突出——不同任务或领域之间的样本数量、视觉分布和模态对齐目标存在显著漂移。

具体而言，现有持续学习基准中的数据不平衡体现在两个层面。**类内不平衡**：以ScienceQA为例，各主题的样本分布高度倾斜，生物学、物理等主题拥有丰富训练数据，而语法、语音意识等主题样本稀缺，导致少数类准确率显著偏低。**跨任务模态漂移**：ScienceQA、Grounding、OCR-VQA等任务依次引入差异化的视觉分布和对齐目标，形成任务间的模态不平衡。在这两种不平衡的叠加下，传统持续学习方法面临严峻挑战。

现有方法在应对上述问题时存在明显缺口：

- **基于知识蒸馏的方法**（如LwF等）通过最小化当前模型与旧模型之间的KL散度来保持旧知识，但其仅提供单向的遗忘约束，无法主动引导模型在新旧任务之间取得平衡，且在不平衡数据下蒸馏信号本身即带有偏见。
- **基于参数隔离的方法**（如**O-LoRA** (Wang et al., arXiv 2023)、**MoELoRA** (Chen et al., NeurIPS 2024)、**CL-MoE** (Jang et al., arXiv 2024)、**HiDe** (Guo et al., arXiv 2025)）通过正交子空间、混合专家或层级分解来隔离不同任务的知识，但未显式处理数据不平衡带来的公平性问题，少数类性能仍然受限。
- **直接偏好优化（DPO）** 在标准场景下虽能通过偏好对对齐来隐式约束遗忘，但在不平衡数据下，其梯度更新仍受多数类主导，偏见未能消除。

本文的动机正是填补这一空白：**将持续学习形式化为带KL约束的RLHF问题，并进一步引入公平性调制机制，使梯度更新在各数据子组之间趋于平衡**。通过将遗忘抑制与公平性处理统一于DPO框架内，ϕ-DPO旨在同时实现灾难性遗忘的缓解、新任务的持续适应以及不平衡数据下的鲁棒性保持。

## 核心方法与创新机理

ϕ-DPO 的核心创新在于将**持续学习中的遗忘抑制与数据不平衡下的公平性**两个关键挑战统一到一个基于**直接偏好优化 (Direct Preference Optimization, DPO)** 的理论框架中，并通过一个可调制的**公平性焦点损失 (Fair DPO Loss)** 实现梯度层面的组间平衡。

### 1. 范式创新：从知识蒸馏到 DPO 隐式约束

传统持续学习方法（如 **O-LoRA** (Wang et al., arXiv 2023)、**MoELoRA** (Chen et al., NeurIPS 2024)）依赖知识蒸馏 (KL 散度) 来约束当前模型与历史模型之间的分布偏移，以防止灾难性遗忘。ϕ-DPO 则将持续学习形式化为一个带 KL 约束的 RLHF 问题（Eqn. 2），并采用 DPO 损失替代显式的 KL 散度计算。

这一转变的理论优势在于：**DPO 损失同时提供了 KL 散度的下界和上界**（Lemma 1 与 Lemma 2，第 3.1.2 节）。具体而言：

- **下界**：$D_{\mathrm{KL}}(\pi_{t-1} \| \pi_t) \geq \frac{1}{C_{\mathrm{lower}}} (\log 2 - \mathcal{L}_{\mathrm{DPO}}(\pi_t; \pi_{t-1}))^2$，保证最小化 DPO 损失时，KL 散度不会任意缩小，从而保留一定的模型可塑性。
- **上界**：$D_{\mathrm{KL}}(\pi_{t-1} \| \pi_t) \leq C_{\mathrm{upper}} \mathcal{L}_{\mathrm{DPO}}(\pi_t; \pi_{t-1})$，保证 DPO 损失下降时，遗忘程度（KL 散度）被线性上界控制。

这种双向约束机制使得 DPO 在理论上优于仅提供单向正则化的知识蒸馏：DPO 在抑制遗忘的同时，**通过偏好对 (preference pairs) 的选择性放大/抑制机制，保留了模型对新任务的适应能力**。

### 2. 机制创新：Fair DPO 损失与梯度公平调制

多模态持续学习中的数据不平衡存在于两个层面：**任务间样本量差异**（如 ScienceQA 中 Biology 与 Grammar 的样本量悬殊，见 Figure 2）以及**跨任务模态分布漂移**（如 ScienceQA→Grounding→OCR-VQA 的视觉分布变化，见 Figure 3）。这种不平衡导致标准 DPO 的梯度更新偏向多数类或主导模态，损害少数类的性能保持。

ϕ-DPO 的核心机制创新是引入**Fair DPO 损失**（Eqn. 14），受 Focal Loss 启发，对 DPO 损失施加聚焦参数 $\gamma$ 的调制：

$$\mathcal{L}_{\mathrm{DPO}}^{\gamma}(\theta; \mu) = -\mathbb{E}_{z \sim \mu}\Big[(1-p(z))^{\gamma} \log p(z)\Big]$$

其中 $p(z)$ 为偏好对 $z$ 被正确排序的概率。该调制因子 $(1-p)^{\gamma}$ 的作用机制如下：

- 当某数据子组的偏好对**容易被正确分类**（$p \to 1$）时，调制因子趋近于 0，降低该组的梯度贡献；
- 当某数据子组的偏好对**难以分类**（$p \to 0$）时，调制因子趋近于 1，保持其梯度贡献。

这一机制的理论保证由 **Lemma 3**（第 3.2 节）给出：将 DPO 梯度按数据子组分解为 $\nabla_{\theta} \mathcal{L}_{\mathrm{DPO}}(\theta; \mu) = \sum_{k=1}^{K} \mu_k m_k(\theta)$，在引入 Fair DPO 后，**不平衡偏差 $B_{\gamma}(\theta)$ 随 $\gamma$ 增大而趋近于零**，即梯度更新在各组间趋于平衡。

### 3. 数据构造创新：遗忘感知的偏好对设计

为支持 DPO 训练，ϕ-DPO 需要构建偏好对 $(y^+, y^-)$，其中 $y^+$ 为保留记忆的正确回答，$y^-$ 为精心设计的“遗忘回答”。这一数据构造（第 3.3 节，示例见 Figure 5）是方法可行的关键前提，也是相对于仅使用 $(图像, 指令, 答案)$ 三元组的传统持续学习方法的显著差异点。

### 创新点总结

| 创新维度 | 基线方法 | ϕ-DPO 方案 | 理论/实证支撑 |
|---------|---------|-----------|-------------|
| 遗忘缓解 | 知识蒸馏 (KL 散度) 或无显式机制 | DPO 隐式 KL 约束，双向界保证 | Lemma 1, 2; Eqn. (7) |
| 公平性处理 | 无显式公平机制 | Fair DPO 损失 + 聚焦参数 $\gamma$ 梯度调制 | Lemma 3; Eqn. (14)-(16) |
| 训练数据 | $(x, 指令, y)$ 三元组 | 额外构建 $(y^+, y^-)$ 偏好对 | 第 3.3 节; Figure 5 |

**需人工验证**：公平性度量（如组间准确度方差）在实验中未直接报告，仅通过整体指标提升间接体现；Lemma 3 的不平衡偏差趋零性依赖于 $\gamma$ 足够大的假设，而实验中 $\gamma=2.0$ 为最优，过大的 $\gamma$ 会导致梯度消失，理论边界与实验最优值之间的精确关系需进一步确认。

ϕ‑DPO（FaiDPO）将持续学习重新形式化为一个带 KL 约束的 RLHF 问题，并通过**直接偏好优化（DPO）**隐式实现遗忘抑制，避免显式奖励建模与 PPO 训练的复杂性。整体框架由三个核心模块串联构成：监督微调模块、DPO 偏好对齐模块与公平调制模块，三者协同工作，使大型多模态模型（LMM）在增量学习过程中既能适应新任务，又能保持对旧知识的记忆，同时抑制数据不平衡引入的梯度偏见。

### 问题形式化

设第 $t$ 个学习步骤的当前策略为 $\pi_t$，前一策略为 $\pi_{t-1}$。持续学习的核心目标是在最大化当前任务对数似然的同时，约束 $\pi_t$ 与 $\pi_{t-1}$ 之间的 KL 散度不超过阈值 $\delta$：

$$
\pi_t^* = \arg\max_{\pi_t} \mathbb{E}_{x,y \in \mathcal{D}_t} \log p(y|x) + D_{\mathrm{Forget}}(\pi_t \| \pi_{t-1})
$$

其中 $D_{\mathrm{Forget}}$ 是遗忘缓解项。ϕ‑DPO 的关键创新在于：将上述约束优化问题转化为 RLHF 框架下的奖励最大化问题，并通过 DPO 损失直接优化策略，无需显式奖励函数。

### 模块一：监督微调模块

该模块使用标准交叉熵损失在增量任务数据 $\mathcal{D}_t$ 上训练当前步骤的模型，确保模型获得新任务的基本能力。其输出作为后续 DPO 对齐的初始策略。

### 模块二：DPO 偏好对齐模块

该模块通过构造偏好对 $(y^+, y^-)$ 来引导策略更新：$y^+$ 为保留记忆的回答，$y^-$ 为精心设计的遗忘回答。DPO 损失直接最大化当前策略与前一策略在偏好对上的对数比率差异：

$$
\mathcal{L}_{\mathrm{DPO}}(\pi_t, \pi_{t-1}) = -\mathbb{E}_{x,y^+,y^-}\log\sigma\Big[\beta\big[\log\pi_t(y^+|x) - \log\pi_t(y^-|x) - \log\pi_{t-1}(y^+|x) + \log\pi_{t-1}(y^-|x)\big]\Big]
$$

其中 $\beta$ 控制发散惩罚强度。理论上，DPO 损失同时提供了 KL 散度的下界与上界（Lemma 1, 2，第 3.1.2 节），使得遗忘程度受到严格约束，且约束效果优于传统知识蒸馏。

### 模块三：公平调制模块

在多模态持续学习中，数据分布高度不平衡（如 ScienceQA 各主题样本量差异可达数十倍），导致 DPO 梯度更新偏向多数类。公平调制模块引入聚焦参数 $\gamma$，对 DPO 损失进行重加权：

$$
\mathcal{L}_{\mathrm{DPO}}^{\gamma}(\theta; \mu) = -\mathbb{E}_{z \sim \mu}\Big[(1-p(z))^{\gamma} \log p(z)\Big]
$$

其中 $p(z)$ 为偏好对的分类概率，调制因子 $(1-p)^{\gamma}$ 类似 Focal Loss，降低易分类样本的权重，迫使模型关注难例和少数类。理论分析（Lemma 3，第 3.2 节）表明，当 $\gamma$ 足够大时，各组梯度贡献的不平衡偏差 $B_\gamma(\theta)$ 趋近于零。

### 最终学习目标

每个增量步骤的联合损失为：

$$
\pi_t^* = \arg\min_{\pi_t} \mathbb{E}_{x,y \in \mathcal{D}_t} -\log p(y|x) + \mathcal{L}_{\mathrm{DPO}}^{\gamma}(\pi_t \| \pi_{t-1})
$$

第一项为标准监督损失，第二项为带公平调制的 DPO 正则项。整个 pipeline 的输入为当前任务数据与前一策略，输出为更新后的策略 $\pi_t$，其数据流为：**监督微调 → DPO 偏好对齐 → 公平调制 → 参数更新**。

![[assets/figures/papers/paper_list_l2282_https_openaccess_thecvf_com_content_CVPR2026_html_Truong_phi_DPO_Fairnes/figures/004_Figure_4.jpg]]
*Figure 4: Our Proposed Continual Learning Approach via Fairness DPO for Large Multimodal Models. Traditional reinforcement learning with human feedback (RLHF) method optimize models through explicit reward maximization. Our framework instead reformulates RLHF as Direct Preference Optimization (DPO). The Fairness DPO loss mitigate the gradient biased under the imbalanced data*

### 3.1 持续学习的RLHF形式化与DPO重构

ϕ-DPO将多模态持续学习重新形式化为带KL约束的强化学习问题。在增量步骤 $t$，模型需要在新任务上最大化期望奖励，同时保持与上一步策略 $\pi_{t-1}$ 的接近度，以避免灾难性遗忘：

$$\pi_t^* = \max_{\pi_t} \mathbb{E}_{x,y \sim \pi_t}[r(x,y)] - \beta D_{\mathrm{KL}}(\pi_t(\cdot|x) \parallel \pi_{t-1}(\cdot|x)) \tag{3}$$

其中 $\beta$ 为发散参数，控制遗忘抑制的强度。该优化问题存在闭式最优解，揭示了奖励函数与策略之间的隐式关系：

$$\pi_t^*(y|x) = \frac{\pi_{t-1}(y|x) \exp\left(\frac{1}{\beta} r(x,y)\right)}{Z(x)}, \quad r(x,y) = \beta \log \frac{\pi_t^*(y|x)}{\pi_{t-1}(y|x)} + \beta \log Z(x) \tag{4}$$

基于此，ϕ-DPO摒弃了显式奖励建模和PPO优化，转而采用**直接偏好优化（DPO）**，通过构建偏好对 $(y^+, y^-)$ 直接对齐策略：

$$\mathcal{L}_{\mathrm{DPO}}(\pi_t, \pi_{t-1}) = -\mathbb{E}_{x,y^+,y^-} \log \sigma \Big[\beta \big[\log \pi_t(y^+|x) - \log \pi_t(y^-|x) - \log \pi_{t-1}(y^+|x) + \log \pi_{t-1}(y^-|x) \big]\Big] \tag{7}$$

其中 $y^+$ 为保留记忆的回答，$y^-$ 为精心设计的遗忘回答（见Figure 5）。DPO通过对比当前策略与前一策略在偏好对上的对数比率，鼓励模型提升保留回答的相对概率，从而**隐式实现遗忘抑制**。

### 3.2 DPO对遗忘抑制的理论保证

ϕ-DPO的核心理论贡献在于证明了DPO损失对KL散度的双向约束，为遗忘抑制提供了严格保证。

**Lemma 1（KL下界）**：DPO损失提供KL散度的下界控制：
$$D_{\mathrm{KL}}(\pi_{t-1} \parallel \pi_t) \geq \frac{1}{C_{\mathrm{lower}}} (\log 2 - \mathcal{L}_{\mathrm{DPO}}(\pi_t; \pi_{t-1}))^2 \tag{式见原文3.1.2节}$$

这意味着最小化DPO损失会**强制增大KL散度的下界**，防止当前策略过度偏离前一策略。

**Lemma 2（KL上界）**：DPO损失同时提供KL散度的上界控制：
$$D_{\mathrm{KL}}(\pi_{t-1} \parallel \pi_t) \leq C_{\mathrm{upper}} \mathcal{L}_{\mathrm{DPO}}(\pi_t; \pi_{t-1}) \tag{式见原文3.1.2节}$$

这表明KL散度由DPO损失线性上界约束，**遗忘程度受DPO损失直接控制**。相比之下，传统的知识蒸馏仅最小化KL散度本身：

$$\mathcal{L}_{\mathrm{KD}}(\pi_t, \pi_{t-1}) = D_{\mathrm{KL}}(\pi_{t-1} \parallel \pi_t) = \mathbb{E}_{x,y \sim \pi_{t-1}} \left[\log \frac{\pi_{t-1}(y|x)}{\pi_t(y|x)}\right] \tag{8}$$

DPO的双向约束使其在理论上优于知识蒸馏——不仅抑制遗忘，还通过偏好信号选择性放大高奖励回答，抑制低奖励回答。

### 3.3 Fair DPO损失：梯度公平调制

上述DPO损失在数据不平衡时仍会产生**梯度偏见**：多数类子组的梯度贡献主导了整体更新方向。为分析这一问题，将DPO梯度按 $K$ 个数据子组分解：

$$\nabla_{\theta} \mathcal{L}_{\mathrm{DPO}}(\theta; \mu) = \sum_{k=1}^{K} \mu_k m_k(\theta) \tag{式见原文3.2节}$$

其中 $\mu_k$ 为第 $k$ 组的样本权重，$m_k(\theta)$ 为该组的平均梯度。当 $\mu_k$ 高度不平衡时，梯度更新偏向多数类。

受Focal Loss启发，ϕ-DPO引入**聚焦参数 $\gamma \geq 0$**，对DPO损失进行重加权，得到**Fair DPO损失**：

$$\mathcal{L}_{\mathrm{DPO}}^{\gamma}(\theta; \mu) = -\mathbb{E}_{z \sim \mu} \Big[(1-p(z))^{\gamma} \log p(z)\Big] \tag{14}$$

其中 $p(z) = \sigma(\beta[\log \pi_t(y^+|x) - \log \pi_t(y^-|x) - \log \pi_{t-1}(y^+|x) + \log \pi_{t-1}(y^-|x)])$ 为偏好对的预测概率，$(1-p(z))^{\gamma}$ 为调制因子。其作用机制为：
- 对于**易分类的多数类样本**，$p(z) \to 1$，调制因子趋近于0，梯度贡献被大幅削弱；
- 对于**难分类的少数类样本**，$p(z)$ 较小，调制因子接近1，梯度贡献得以保留。

**Lemma 3（梯度平衡）**：在Fair DPO下，各组梯度贡献的不平衡偏差 $B_{\gamma}(\theta)$ 随 $\gamma$ 增大而减小，当 $\gamma \to \infty$ 时，$B_{\gamma}(\theta) \to 0$（证明见原文3.2节）。这从理论上保证了Fair DPO能够在严重数据不平衡条件下实现**组间梯度更新的均衡化**。

### 3.4 最终学习目标

每个增量步骤的最终优化目标将标准监督微调与Fair DPO正则项结合：

$$\pi_t^* = \arg\min_{\pi_t} \mathbb{E}_{x,y \in \mathcal{D}_t} -\log p(y|x) + \mathcal{L}_{\mathrm{DPO}}^{\gamma}(\pi_t \parallel \pi_{t-1}) \tag{17}$$

其中第一项为当前任务的标准交叉熵损失，第二项为带公平调制的DPO正则项。该组合使得模型在适应新任务的同时，通过DPO隐式约束保持旧知识，并通过 $\gamma$ 调制抵消不平衡数据带来的梯度偏见。

![[assets/figures/papers/paper_list_l2282_https_openaccess_thecvf_com_content_CVPR2026_html_Truong_phi_DPO_Fairnes/figures/005_Figure_5.jpg]]
*Figure 5: Example of Our DPO Data in the Continual Learning Benchmark. Best viewed in color*

![[assets/figures/papers/paper_list_l2282_https_openaccess_thecvf_com_content_CVPR2026_html_Truong_phi_DPO_Fairnes/figures/003_Figure_2.jpg]]
*Figure 2: The Imbalanced Distribution of Multimodal Continual Learning Benchmarks. The distribution of samples across ScienceQA topics is highly skewed, i.e. categories with fewer training examples (e.g. Grammar, Phonological Awareness, Word Study) exhibit significantly lower accuracy, while topics with richer data (e.g. Biology, Physics) achieve stronger performance*

## 实验与关键发现

### 主实验结果

ϕ-DPO 在三个多模态持续学习基准上进行了全面验证：**MLLM-CL Domain**（跨领域迁移）、**MLLM-CL Ability**（跨能力迁移）和 **CoIN**（通用多模态持续学习）。所有实验均以 LLaVA-1.5-7B 为基础模型，采用序列微调范式，评估指标包括平均最终性能（MFT）、平均遗忘率（MFN）和平均累积准确率（MAA）等。

**MLLM-CL Domain 基准**（Table 1）涵盖遥感、医学、自动驾驶、ScienceQA 和金融五个领域。ϕ-DPO 在 MFT 指标上达到 **74.29%**，超过最强基线 HiDe* 的 73.85%（+0.44%），且在近零遗忘方面表现突出——后向迁移（BWT）仅为 **-0.37%**，意味着模型在学习新领域时几乎完全保留了先前知识。相比之下，序列微调基线 LoRA-FT 的 BWT 为 -3.14%，知识蒸馏方法虽有缓解但仍存在明显遗忘。

**MLLM-CL Ability 基准**（Table 2）测试模型在数学逻辑与视觉感知能力间的迁移。ϕ-DPO 在 MFN 指标上取得 **45.31%**，优于 HiDe* 的 43.81%（+1.50%），证明公平调制机制在能力维度迁移中同样有效。值得注意的是，该基准中数据不平衡问题尤为突出——不同能力类别的训练样本量差异可达数倍，而 ϕ-DPO 在各子类别上均维持了更均衡的准确率分布。

**CoIN 基准**（Table 3）包含 ScienceQA、ImageNet、VizWiz、Grounding、TextVQA 和 VQAv2 六个任务。ϕ-DPO 在 MAA 指标上达到 **74.94%**，略高于 CoIN* 的 74.89%（+0.05%）。虽然绝对提升较小，但考虑到 CoIN 基准上各方法性能已趋于饱和，ϕ-DPO 仍在最严格的公平性条件下保持了竞争力。

### 消融实验

**公平调制模块的有效性**（Table 4）通过对比三种变体得到验证：纯监督微调（SFT）、SFT + 标准 DPO 和 SFT + Fair DPO。结果表明，标准 DPO 相比 SFT 已显著降低遗忘率，但引入 Fair DPO 后所有指标进一步提升，证实了聚焦参数 γ 对不平衡梯度的校正作用独立于 DPO 的遗忘抑制机制。

**发散参数 β 的影响**（Table 5）揭示了一个关键权衡：β 控制当前策略与前一策略的 KL 散度约束强度。实验扫描 β ∈ {0.05, 0.10, 0.50, 1.00}，发现 **β = 0.10 是最优设置**。过小的 β（0.05）导致约束过弱，遗忘率上升；过大的 β（1.00）则过度限制模型适应性，新任务性能下降。这一现象与理论分析一致——Lemma 2 表明 KL 散度受 DPO 损失线性上界控制，β 直接调节该上界的紧度。

**聚焦参数 γ 的影响**（Table 6）验证了公平调制的核心机制。γ ∈ {0.50, 1.00, 2.00, 5.00} 的扫描显示 **γ = 2.00 达到最佳平衡**。当 γ = 0.50 时，调制效应不足，少数类梯度仍被淹没；当 γ = 5.00 时，梯度消失问题显现，模型整体性能下降。这与 Focal Loss 的理论性质一致——过大的 γ 使得易分类样本的梯度趋近于零，反而损害了学习过程。

**模型规模可扩展性**（Table 7）在 LLaVA-13B 上得到验证。ϕ-DPO 在大规模模型上仍一致优于标准 DPO，表明公平调制机制不依赖于特定模型容量，具有良好的泛化性。

### 失败模式与局限性

尽管 ϕ-DPO 在多数场景下表现优异，实验分析揭示了若干值得关注的边界条件：

1. **超参数敏感性**：β 和 γ 的最优值依赖于具体基准和数据分布。在 CoIN 基准上，由于任务间差异更大，β 的最优值可能偏离 0.10。论文未提供自适应调节机制，实际部署时需要针对新场景重新搜索。

2. **极端不平衡下的退化**：当某些数据组的样本量趋近于零时，即使 γ 足够大，Lemma 3 保证的不平衡偏差 B_γ(θ) → 0 在有限样本下仍可能存在较大方差。实验未系统测试样本量低于 10 的极端情况。

3. **偏好对构造质量依赖**：DPO 训练依赖于精心构造的偏好对（y⁺, y⁻），其中负样本 y⁻ 需模拟遗忘回答。Figure 5 展示了构造示例，但该过程依赖 LLM 生成，可能引入噪声或偏差。论文未消融不同构造策略对最终性能的影响。

4. **公平性度量的直接报告缺失**：虽然 ϕ-DPO 的设计目标是对抗数据不平衡，实验仅通过整体指标和子类别准确率间接反映公平性改善，未直接报告组间准确率方差或最大-最小差距等标准公平性度量。这一缺失使得公平性声称的量化强度有所折扣。

### 核心图表结论

- **Figure 2** 直观展示了 ScienceQA 各主题的样本分布与性能差异：语法、语音意识等少数类主题准确率显著低于生物、物理等多数类，验证了数据不平衡是导致性能差异的直接原因。
- **Table 1-3** 共同确立了 ϕ-DPO 在三个基准上的最优地位，尤其在 MLLM-CL Domain 上实现了近零遗忘（BWT = -0.37%），这是现有方法未能达到的。
- **Table 4-6** 的消融链从组件有效性、约束强度和公平调制力度三个维度，完整验证了 ϕ-DPO 设计空间的合理性。
- **Table 7** 排除了方法仅适用于特定模型规模的疑虑，为后续扩展到更大规模 LMM 提供了初步证据。

![[assets/figures/papers/paper_list_l2282_https_openaccess_thecvf_com_content_CVPR2026_html_Truong_phi_DPO_Fairnes/figures/007_Table_1.jpg]]
*Table 1: Results on MLLM-CL Domain (* denote the method using relay data). RS: Remote Sensing, Med: Medical, AD: Autonmous Driving, Sci: ScienceQA, Fin: Finance*

![[assets/figures/papers/paper_list_l2282_https_openaccess_thecvf_com_content_CVPR2026_html_Truong_phi_DPO_Fairnes/figures/009_Table_4.jpg]]
*Table 4: Effectiveness of Our Fairness DPO*

![[assets/figures/papers/paper_list_l2282_https_openaccess_thecvf_com_content_CVPR2026_html_Truong_phi_DPO_Fairnes/figures/011_Table_7.jpg]]
*Table 7: Effectiveness of Different LMM Framework*

## 定位与知识库关联

### 1. 与基线方法的关系

ϕ-DPO 的提出立足于对现有多模态持续学习方法的两个核心缺陷的回应：**灾难性遗忘的抑制机制不足**，以及**数据不平衡下梯度更新的系统性偏见**。以下从遗忘缓解和公平性两个维度，梳理 ϕ-DPO 与代表性基线的演进关系。

#### 1.1 遗忘缓解机制的演进

现有的多模态持续学习方法在遗忘缓解上主要依赖三类策略：

- **基于 LoRA 的序列微调**：以 **LoRA-FT**（Hu et al., arXiv 2021）为代表，通过低秩适配器隔离参数更新，但缺乏显式的遗忘抑制机制，在任务序列较长时遗忘严重。
- **基于正交子空间的方法**：**O-LoRA**（Wang et al., arXiv 2023）通过将不同任务的 LoRA 参数约束在正交子空间中来减少干扰，但子空间容量有限，难以扩展到多任务场景。
- **基于混合专家（MoE）的方法**：**MoELoRA**（Chen et al., CoIN, NeurIPS 2024）和 **CL-MoE**（Jang et al., arXiv 2024）利用多专家路由为不同任务激活不同子网络，通过结构稀疏化缓解干扰，但路由机制本身可能受到不平衡数据的影响。
- **基于层级分解的方法**：**HiDe**（Guo et al., arXiv 2025）通过层级化模块分解实现跨模态持续学习，在多个基准上取得领先结果，但其遗忘抑制仍依赖结构隔离，缺乏对梯度层面的动态调控。

ϕ-DPO 的遗忘缓解机制（第3.1节）与上述方法存在本质差异：它将持续学习形式化为带 KL 约束的 RLHF 问题，通过 DPO 损失**隐式地**实现遗忘抑制。理论分析（Lemma 1, Lemma 2）表明，DPO 损失同时提供了 KL 散度（即遗忘程度）的下界和上界：

$$D_{\mathrm{KL}}(\pi_{t-1}\|\pi_t) \geq \frac{1}{C_{\mathrm{lower}}}(\log 2 - \mathcal{L}_{\mathrm{DPO}}(\pi_t;\pi_{t-1}))^2$$

$$D_{\mathrm{KL}}(\pi_{t-1}\|\pi_t) \leq C_{\mathrm{upper}} \mathcal{L}_{\mathrm{DPO}}(\pi_t;\pi_{t-1})$$

这意味着 DPO 损失对遗忘的约束比传统的知识蒸馏（KD）更为严格——KD 仅最小化 KL 散度，而 DPO 通过偏好对的对比信号，在保持旧知识的同时**选择性放大高奖励（保留良好）响应、抑制低奖励（遗忘）响应**。实验结果表明，ϕ-DPO 在 MLLM-CL Domain 基准上实现了接近零遗忘（BWT=-0.37%），显著优于 HiDe 等最强基线。

#### 1.2 公平性机制的缺失与填补

上述所有基线方法均**未显式处理数据不平衡问题**。在多模态持续学习基准中，数据分布的不平衡体现在两个层面：

- **类别不平衡**：如 ScienceQA 中各主题样本数差异悬殊（Figure 2），少数类（如 Grammar、Phonological Awareness）的准确率显著低于多数类（如 Biology、Physics）。
- **模态不平衡**：不同任务（ScienceQA、Grounding、OCR-VQA）之间的视觉分布和对齐目标逐渐漂移（Figure 3），形成跨任务的模态偏见。

ϕ-DPO 的核心创新在于引入 **Fair DPO 损失**（第3.2节），受 Focal Loss 启发，通过聚焦参数 γ 对 DPO 梯度进行动态调制：

$$\mathcal{L}_{\mathrm{DPO}}^{\gamma}(\theta;\mu) = -\mathbb{E}_{z\sim\mu}\Big[(1-p(z))^{\gamma}\log p(z)\Big]$$

其梯度可分解为各组梯度贡献的加权和：

$$\nabla_{\theta}\mathcal{L}_{\mathrm{DPO}}(\theta;\mu) = \sum_{k=1}^{K} \mu_k m_k(\theta)$$

调制因子 $(1-p(z))^{\gamma}$ 降低了易分类样本（多数类）的梯度权重，迫使模型更关注难例和少数类。理论分析（Lemma 3）证明，当 γ 足够大时，不平衡偏差 $B_{\gamma}(\theta)$ 趋近于零，即梯度更新在各组间趋于平衡。这一机制是 ϕ-DPO 区别于所有基线方法的独特贡献。

### 2. 适用边界

ϕ-DPO 的设计适用于以下场景：

- **多模态大模型的持续微调**：方法在 LLaVA-1.5/1.6 系列上验证，理论上可推广到其他自回归 LMM 架构，但尚未在非自回归或编码器-解码器架构上验证。
- **数据分布不平衡的增量学习**：Fair DPO 的调制机制专门针对类别/模态不平衡设计，在 ScienceQA 等高度偏斜的数据集上效果显著。
- **任务序列明确的持续学习**：方法假设任务边界清晰，依赖前一时刻的模型参数 $\pi_{t-1}$ 作为参考策略，不直接适用于无任务边界的在线持续学习。

不适用或需谨慎使用的场景包括：

- **极大规模任务序列**：DPO 偏好数据的构建依赖人工或 LLM 生成，成本随任务数线性增长。
- **严格的内存限制**：方法需保留前一时刻模型副本用于 DPO 损失计算，内存开销高于纯 LoRA 方法。
- **非偏好可形式化的任务**：DPO 框架假设任务可构造有意义的偏好对 $(y^+, y^-)$，对于开放式生成任务，偏好信号的定义可能模糊。

### 3. 局限与开放问题

#### 3.1 已验证的局限

1. **超参数敏感性**：聚焦参数 γ 需要仔细调节——过小则无法有效抑制偏见，过大则导致梯度消失，妨碍模型适应性（Table 6 验证了 γ=2.00 为最优折中）。类似地，发散参数 β 在稳定性与可塑性之间存在敏感平衡（Table 5，β=0.10 最优）。
2. **偏好数据构建成本**：DPO 训练需要构造偏好对，其中 $y^-$ 为精心设计的遗忘回答（Figure 5 示例），依赖人工或 LLM 生成并验证，成本较高且可能引入噪声。
3. **模型架构覆盖有限**：实验仅在 LLaVA 系列上进行（Table 7 验证了 LLaVA-13B 上的可扩展性），尚未在 InstructBLIP、Qwen-VL 等其他主流 LMM 上验证。
4. **公平性度量不完整**：论文通过实验证实了 ϕ-DPO 在不平衡数据上维持较高且更均衡的准确度，但**未直接报告组间准确度方差等标准公平性度量**，公平性评估的全面性需要手动验证。

#### 3.2 开放问题

1. **自适应超参数调节**：能否设计自适应的 β 和 γ 调整策略（如基于梯度统计或任务难度），以减少对超参数搜索的依赖？
2. **跨模态泛化**：该方法在更多模态（如视频、音频）和跨模态持续学习中的效果如何？Fair DPO 的调制机制是否适用于非视觉-语言的对齐任务？
3. **偏好数据自动化**：DPO 偏好数据构造如何进一步自动化并保证质量和多样性？能否利用模型自身的置信度或集成信号生成偏好对？
4. **理论界的紧化**：Fair DPO 是否存在更紧的泛化误差界？能否结合其他公平性约束（如 demographic parity 或 equalized odds）形成更全面的公平性保证？
5. **与结构方法的融合**：Fair DPO 的梯度调制与 MoE、正交子空间等结构隔离方法是否互补？两者的结合能否进一步提升极端不平衡下的持续学习性能？

## 原文 PDF

![[paperPDFs/CVPR_2026/phi_DPO_Fairness_Direct_Preference_Optimization_Approach_to_Continual_Learning_in_Large_Multimodal_Models.pdf]]
