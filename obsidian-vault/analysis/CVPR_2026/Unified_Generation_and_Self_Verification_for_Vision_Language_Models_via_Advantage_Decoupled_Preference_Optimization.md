---
title: Unified Generation and Self-Verification for Vision-Language Models via Advantage Decoupled Preference Optimization
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Unified_Generation_and_Self_Verification_for_Vision_Language_Models_via_Advantage_Decoupled_Preference_Optimization.pdf
project_link: null
code_link: null
aliases:
- ADPOA
- UGSVVLMADPO
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过偏好验证奖励将验证转化为排序问题以解决类别不平衡，并采用优势解耦优化分离生成和验证的梯度，实现单一策略下的协同训练。
primary_logic: 偏好验证奖励利用对比集中的相对排序信号替代固定阈值，避免因答案正确率升高导致的分数崩塌；优势解耦优化通过独立计算答案优势和偏好优势，并施加token掩码，消除奖励黑客和梯度干扰，使统一模型在保持生成质量的同时输出可靠的自我验证分数。
claims:
- 二元验证奖励在训练后期因类别不平衡导致验证分数几乎全部收敛到1，梯度消失。
- 偏好验证奖励相较于二元奖励，将验证AUC/AP提升最高0.19。
- 优势解耦优化在GUI agent任务上best@8指标提升2.8%，且在所有域中均优于纠缠优势。
- MathVista 上 Accuracy = ADPO (best-of-8) 65.0%
---

# Unified Generation and Self-Verification for Vision-Language Models via Advantage Decoupled Preference Optimization

> [!tip] 核心洞察
> 偏好验证奖励利用对比集中的相对排序信号替代固定阈值，避免因答案正确率升高导致的分数崩塌；优势解耦优化通过独立计算答案优势和偏好优势，并施加token掩码，消除奖励黑客和梯度干扰，使统一模型在保持生成质量的同时输出可靠的自我验证分数。

| 字段 | 内容 |
|------|------|
| 中文题名 | 优势解耦偏好优化：统一视觉语言模型生成与自我验证 |
| 英文题名 | Unified Generation and Self-Verification for Vision-Language Models via Advantage Decoupled Preference Optimization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.01483) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Advantage Decoupled Preference Optimization (ADPO) |
| Dataset | MathVista, MMMU, ReasonSeg, AndroidControl |

> [!tip] 效果简介
> - MathVista 上，Accuracy ADPO (best-of-8) 65.0% vs GRPO + majority voting 62.9% (+2.1%)。
> - MMMU 上，Accuracy ADPO (best-of-8) 52.1% vs GRPO + majority voting 51.1% (+1.0%)。
> - ReasonSeg 上，cIoU (overall) ADPO (best-of-8) 61.2 vs GRPO + majority voting 59.6 (+1.6)。

## 概要

视觉语言模型（VLM）在测试时通过生成多个候选答案并从中择优，可以显著提升性能。然而，现有的并行测试时扩展方案通常需要分别训练生成器和验证器，导致训练成本高昂且推理资源消耗大；若仅训练单一组件，性能提升又十分有限。本文提出 **优势解耦偏好优化（Advantage Decoupled Preference Optimization, ADPO）**，在一个统一的强化学习框架内协同训练答案生成与自我验证，使单一策略模型既能产出高质量答案，又能输出可靠的自我验证分数。

ADPO 的核心洞察在于两点。第一，传统的二元验证奖励在训练后期因答案正确率升高而遭遇严重的类别不平衡——验证分数几乎全部收敛到 1，梯度消失，验证能力不再提升（Figure 2）。为此，ADPO 引入 **偏好验证奖励**，将验证重构为排序问题：在对比集内衡量验证分数与答案质量排序的一致性，从而利用相对排序信号替代固定阈值，避免分数崩塌。第二，将答案奖励与验证奖励聚合为单一优势会导致奖励黑客和梯度干扰。ADPO 通过 **优势解耦优化**，分别计算答案优势 $\hat{A}^{(a)}$ 和偏好优势 $\hat{A}^{(p)}$，并施加 token 掩码隔离梯度，使生成与验证两个目标在统一策略下协同优化。

实验覆盖多模态数学推理、图像定位和 GUI 智能体三个领域。结果表明，ADPO 在 MathVista 上 best-of-8 准确率达到 65.0%，较 GRPO + 多数投票的 62.9% 提升 2.1 个百分点；在 MMMU 上提升 1.0 个百分点；在 ReasonSeg 上 cIoU 提升 1.6；在 AndroidControl 上步成功率提升 1.9 个百分点。消融实验证实，偏好验证奖励将验证 AUC/AP 最高提升 0.19（Figure 4），优势解耦优化在所有领域均优于纠缠优势，且在 GUI agent 任务上 best@8 指标提升 2.8%（Figure 6）。ADPO 以单一统一模型实现了生成质量与验证可靠性的双重提升，为视觉语言模型的测试时扩展提供了高效的解决方案。



视觉语言模型（VLMs）在数学推理、视觉定位、GUI智能体等多模态任务中取得了显著进展。然而，单一前向生成的答案往往存在不确定性，尤其在复杂场景下，模型的首次输出未必是最优解。为提升可靠性，测试时扩展（test-time scaling）策略——如多数投票（majority voting）或最优N选（best-of-N）——被广泛采用，其核心在于生成多个候选答案并从中筛选最佳结果。

这一范式催生了对**验证器（verifier）**的需求：一个能够评估候选答案质量并为筛选提供可靠信号的模型。现有方案通常遵循两条路径：一是训练独立于生成器的专用验证器（如判别式奖励模型）；二是直接利用生成器自身的输出置信度进行自验证。然而，这两类方法均面临显著瓶颈。

**并行测试时扩展的资源困境。** 独立训练生成器和验证器意味着需要分别维护两套模型参数、两套训练流程和两套推理管线，导致训练成本与推理延迟成倍增长。即便仅对生成器进行强化学习优化（如GRPO），再搭配多数投票作为验证，性能提升依然有限——生成器并未学会评估自身输出的可靠性，验证信号粗糙且缺乏校准。

**二元验证奖励的类别不平衡陷阱。** 若尝试在统一策略内同时学习生成与自我验证，最直接的做法是引入二元验证奖励：当验证分数与答案正确性方向一致时给予正奖励。然而，随着训练推进，生成器的答案正确率逐步上升，导致验证分数几乎全部收敛到1（即模型倾向于对所有答案赋予高分）。如Figure 2所示，这种类别不平衡使得二元验证奖励在训练后期几乎丧失区分能力，梯度消失，验证模块无法提供有效的排序信号。本质上，固定阈值下的二元奖励无法适应答案质量分布的动态变化，导致**分数崩塌（score collapse）**。

**奖励黑客与梯度干扰。** 将答案生成奖励与验证奖励简单聚合为单一优势函数进行优化时，模型可能通过操纵验证分数来“欺骗”奖励信号（例如，无论答案质量如何都输出极端分数以最大化聚合奖励），而非真正提升验证能力。同时，生成目标与验证目标的梯度在共享参数空间中相互干扰，导致两个子任务的优化彼此掣肘。

上述瓶颈共同指向一个核心矛盾：**如何在单一策略内实现生成与验证的协同训练，既避免验证信号退化，又防止优化目标间的负向干涉？** 本文的动机正是打破这一僵局——通过重新设计验证奖励的形式与优势解耦机制，使统一模型在保持生成质量的同时，输出可靠、可校准的自我验证分数，从而以极低的额外成本实现高效的测试时扩展。



## 核心方法与创新机理

ADPO 的核心创新在于解决了统一视觉语言模型在强化学习中同时优化**答案生成**与**自我验证**时面临的两个瓶颈：验证奖励信号的退化，以及生成与验证目标间的梯度干扰。其关键创新点体现在以下两个“changed slots”上。

### 从二元验证奖励到偏好验证奖励

传统的验证奖励通常采用二元形式，即判断验证分数与答案正确性是否一致：

$$R^{b} = \mathbb{1}\{(s - \tau_s)(R^{a} - \tau_a) > 0\}$$

然而，随着训练的进行，模型生成正确答案的比例显著上升，导致类别严重不平衡。如 Figure 2 所示，在训练后期，获得二元验证奖励为 1 的样本中，正确答案的比例超过 80%。这导致验证分数几乎全部收敛到 1，奖励信号丧失信息量，梯度消失，验证器无法进一步优化。

ADPO 提出**偏好验证奖励**（Preference Verification Reward），将验证重新定义为排序问题，而非绝对阈值的比较。对于批次内构造的对比集 $\mathcal{C}_i$，该奖励衡量验证分数与答案质量排序的一致性：

$$R_{i}^{p} = \frac{1}{\max(|\mathcal{C}_{i}|, 1)} \sum_{j \in \mathcal{C}_{i}} \mathbb{1}\{(s_i - s_j)(R_i^{a} - R_j^{a}) > 0\}$$

这一设计的核心洞察在于：利用对比集中答案质量的**相对排序信号**来监督验证分数，即使大部分答案本身都是正确的，模型仍需学会区分“好答案”与“更好答案”的细微差异。这从根本上避免了因答案正确率升高而导致的分数崩塌问题。消融实验证实，偏好验证奖励相较于二元奖励，将验证 AUC/AP 最高提升 0.19（Figure 4），且模型输出的分数分布更加多样化（Figure 8），不再集中于两端。

### 从纠缠优势到解耦优势优化

在统一策略中同时优化生成和验证时，若将答案奖励 $R^a$ 和偏好验证奖励 $R^p$ 聚合后计算单一优势，会导致两个问题：一是**奖励黑客**——模型可能通过操纵验证分数来最大化聚合奖励，而非真正提升验证能力；二是**梯度干扰**——生成任务和验证任务的优化方向相互冲突。

ADPO 提出**优势解耦优化**（Advantage Decoupled Optimization），分别计算答案优势 $\hat{A}^{(a)}$ 和偏好优势 $\hat{A}^{(p)}$，并通过 token 掩码实现梯度隔离：

$$\mathcal{I}(\theta) = M^{a} \odot \mathcal{I}_{\theta}(\hat{A}^{(a)}) + M^{p} \odot \mathcal{I}_{\theta}(\hat{A}^{(p)})$$

其中 $M^{a}$ 和 $M^{p}$ 是互斥的 token 掩码，分别对应答案生成部分和验证评分部分。这一设计确保：
- 答案生成的优化仅受答案奖励驱动，不受验证奖励干扰；
- 验证评分的优化仅受偏好验证奖励驱动，防止模型通过牺牲生成质量来获取更高的验证奖励。

消融实验表明，优势解耦优化在 GUI agent 任务上 best@8 指标提升 2.8%，且在所有域（数学推理、视觉定位、GUI 代理）中均优于纠缠优势（Figure 6, Table 10），证明了解耦策略在防止奖励黑客和梯度干扰方面的关键作用。



ADPO 构建了一个统一的强化学习框架，在单一策略模型内联合学习**答案生成**与**自我验证**。其核心设计目标是在不牺牲生成质量的前提下，使模型输出的验证分数具备可靠的排序能力，从而支持高效的测试时扩展（best-of-N 选择）。

### 框架流程

给定多模态输入（图像与文本指令），统一策略模型并行采样 $G$ 个候选输出，每个输出包含两部分：

1. **答案序列** $o_i$：可包含思维链推理过程，最终给出任务答案 $y_i$。
2. **自我验证分数** $s_i \in [0,1]$：模型对自身答案正确性的连续置信度评分。

框架围绕这两类输出构建了三个关键模块：

**答案生成模块** 负责逐 token 生成候选答案。答案质量由答案奖励 $R^a$ 衡量：对于离散任务（如数学选择题）采用完全匹配的二元奖励 $R_{\mathrm{discrete}}^{a} = \mathrm{match}(y, y^{\ast}) \in \{0, 1\}$；对于连续任务（如视觉定位）采用相似度指标（如 IoU）作为连续奖励 $R_{\mathrm{continuous}}^{a} = \sin(y, y^{\ast}) \in [0, 1]$。

**自我验证评分模块** 为每个生成的答案输出一个标量分数 $s_i$，用于在测试时对候选答案进行排序和选择。该模块与答案生成共享同一策略网络，通过特殊 token 标记区分生成内容与验证分数。

**偏好验证奖励计算** 是 ADPO 区别于传统二元验证奖励的核心创新。传统方法将验证分数与答案正确性进行逐样本对齐（$R^{b} = \mathbb{1}\{(s - \tau_s)(R^{a} - \tau_a) > 0\}$），在训练后期因答案正确率升高导致类别严重不平衡——超过 80% 的样本验证奖励为 1，梯度信号消失（Figure 2）。ADPO 将验证重构为**排序问题**：在批次内为每个样本构造对比集 $\mathcal{C}_i$，计算其验证分数与答案质量排序一致的比例作为偏好验证奖励：

$$R_{i}^{p} = \frac{1}{\max(|\mathcal{C}_{i}|, 1)} \sum_{j \in \mathcal{C}_{i}} \mathbb{1}\{(s_i - s_j)(R_i^{a} - R_j^{a}) > 0\}$$

该设计利用相对排序信号替代固定阈值，即使答案正确率升高，只要验证分数的排序与答案质量排序保持一致，奖励信号仍保持有效。

**优势解耦优化器** 将答案奖励 $R^a$ 和偏好验证奖励 $R^p$ 分别计算组归一化优势 $\hat{A}^{(a)}$ 和 $\hat{A}^{(p)}$，并通过 token 掩码 $M^a$ 和 $M^p$ 将两类梯度隔离：

$$\mathcal{I}(\theta) = M^{a} \odot \mathcal{I}_{\theta}(\hat{A}^{(a)}) + M^{p} \odot \mathcal{I}_{\theta}(\hat{A}^{(p)})$$

其中 $M^a$ 仅覆盖答案生成部分的 token，$M^p$ 仅覆盖验证分数输出部分的 token。这种解耦设计防止了奖励黑客（模型通过操纵验证分数来获取高奖励而不提升答案质量），并消除生成与验证目标之间的梯度干扰，使统一模型在保持 pass@1 生成质量与 GRPO 基线相当的前提下，输出可靠的自我验证分数。

### 输入输出关系

- **输入**：多模态数据（图像 + 文本指令）。
- **训练阶段输出**：每个样本生成 $G$ 个候选答案及对应验证分数，通过答案奖励和偏好验证奖励联合优化统一策略。
- **推理阶段输出**：采样 $N$ 个候选答案，利用模型自身的验证分数进行 best-of-N 选择，无需额外验证器。

### 补充图表

![[assets/figures/papers/paper_list_l2196_https_arxiv_org_abs_2601_01483/figures/003_Figure_3.jpg]]
*Figure 3: The framework of ADPO. Given a multimodal input, our unified policy produces an answer and a self-verification score to rank answer candidates. We design a preference verification reward to improve verification capability and a decoupled optimization mechanism to enable synergistic optimization of generation and verification. Preference verification reward aligns verification scores with answer correctness by providing relative ranking supervision. Advantage decoupled optimization computes separate advantages for generation and verification, and applies token masks to isolate gradients, thereby preventing reward hacking and reducing gradient interference between the two objectives*



ADPO 在统一策略中同时完成答案生成与自我验证，其核心由四个模块串联构成：**答案生成模块**、**自我验证评分模块**、**偏好验证奖励计算**和**优势解耦优化器**。以下逐一给出其关键公式与变量含义。

### 3.1 答案生成与GRPO基础

给定多模态输入，统一策略逐 token 生成候选答案（可选含思维链），并以分组相对策略优化（GRPO）为训练基础。GRPO 的目标函数为：

$$ \mathcal{L}_{\mathrm{GRPO}}(\theta) = \mathbb{E}\Bigg[ \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|o_i|} \sum_{t=1}^{|o_i|} \Big( \min\big(r_{i,t}(\theta) \hat{A}_{i,t}, \mathrm{clip}(r_{i,t}(\theta), 1-\varepsilon, 1+\varepsilon) \hat{A}_{i,t}\big) - \beta D_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}}) \Big) \Bigg] $$

其中 $G$ 为每组采样数，$|o_i|$ 为第 $i$ 条响应的 token 长度，$r_{i,t}(\theta)$ 为当前策略与旧策略的概率比，$\hat{A}_{i,t}$ 为组归一化优势，$\varepsilon$ 为裁剪阈值，$\beta D_{\mathrm{KL}}$ 为与参考策略的 KL 正则项。

答案奖励 $R^a$ 根据任务类型分为两种形式：

- **离散任务**（如数学推理）：采用完全匹配的二元奖励

  $$ R_{\mathrm{discrete}}^{a} = \mathrm{match}(y, y^{\ast}) \in \{0, 1\} $$

- **连续任务**（如视觉定位）：采用相似度（如 IoU）作为连续奖励

  $$ R_{\mathrm{continuous}}^{a} = \sin(y, y^{\ast}) \in [0, 1] $$

其中 $y$ 为模型输出，$y^{\ast}$ 为参考答案。

### 3.2 偏好验证奖励：从二元到排序

传统二元验证奖励定义为验证分数 $s$ 与答案正确性 $R^a$ 的一致性指示：

$$ R^{b} = \mathbb{1}\{(s - \tau_s)(R^{a} - \tau_a) > 0\} $$

其中 $\tau_s$ 和 $\tau_a$ 分别为验证分数和答案奖励的阈值。该设计的核心瓶颈在于：当答案正确率升高时，类别严重不平衡导致 $R^b$ 几乎全部收敛到 1，梯度消失（见 Figure 2 的实证分析）。

![[assets/figures/papers/paper_list_l2196_https_arxiv_org_abs_2601_01483/figures/002_Figure_2.jpg]]
*Figure 2: Effect of class imbalance on the Binary Verification Reward. The Blue line shows the proportion of correct answers among responses with binary verification reward = 1. The Orange line shows the proportion of answers with verification score = 1*

ADPO 提出**偏好验证奖励**，将验证重构为排序问题：在批次内构造对比集 $\mathcal{C}_i$，衡量验证分数与答案质量排序一致的比例：

$$ R_{i}^{p} = \frac{1}{\max(|\mathcal{C}_{i}|, 1)} \sum_{j \in \mathcal{C}_{i}} \mathbb{1}\{(s_i - s_j)(R_i^{a} - R_j^{a}) > 0\} $$

其中 $s_i$ 为第 $i$ 条响应的验证分数，$R_i^a$ 为其答案奖励。该奖励利用**相对排序信号**替代固定阈值，即使整体正确率上升，只要验证分数的相对排序与答案质量一致，梯度信号仍可保持。消融实验表明，偏好验证奖励相较于二元奖励将验证 AUC/AP 提升最高 0.19（Figure 4）。

![[assets/figures/papers/paper_list_l2196_https_arxiv_org_abs_2601_01483/figures/008_Figure_4.jpg]]
*Figure 4: Ablation of binary verification reward and preference verification reward*

### 3.3 优势解耦优化：隔离生成与验证梯度

传统 GRPO 将答案奖励与验证奖励聚合为单一总奖励 $R_{\mathrm{total}} = R^{a} + R^{p}$，并据此计算统一的组归一化优势，导致两个目标的梯度相互干扰，甚至引发奖励黑客（模型通过输出极端验证分数而非提升生成质量来最大化奖励）。

ADPO 的**优势解耦优化**分别计算两组优势：

- **答案优势** $\hat{A}^{(a)}$：仅基于 $R^a$ 进行组归一化
- **偏好优势** $\hat{A}^{(p)}$：仅基于 $R^p$ 进行组归一化

随后施加**token 掩码**实现梯度隔离。令 $M^a$ 为答案 token 的掩码矩阵（答案区域为 1，验证区域为 0），$M^p$ 为验证 token 的掩码矩阵（验证区域为 1，答案区域为 0），最终解耦训练目标为：

$$ \mathcal{I}(\theta) = M^{a} \odot \mathcal{I}_{\theta}(\hat{A}^{(a)}) + M^{p} \odot \mathcal{I}_{\theta}(\hat{A}^{(p)}) $$

其中 $\odot$ 表示逐元素乘法，$\mathcal{I}_{\theta}(\cdot)$ 为 GRPO 的裁剪目标函数。该设计确保：
- 答案生成的梯度仅由答案奖励驱动，不受验证评分干扰
- 验证评分的梯度仅由偏好奖励驱动，防止模型通过操控答案区域来提升验证奖励

消融实验证实，优势解耦优化在所有域（数学、定位、GUI 代理）中均优于纠缠优势，且在 GUI agent 任务上 best@8 指标提升 2.8%（Table 10, Figure 6）。

### 补充图表

![[assets/figures/papers/paper_list_l2196_https_arxiv_org_abs_2601_01483/figures/012_Figure_5.jpg]]
*Figure 5: Ablation of entangled and decoupled advantage. Entangled and decoupled correspond to models trained with entangled advantage in Eq. (8) and decoupled advantage in Eq. (9)*



## 实验与关键发现

### 主要结果：统一生成与自验证的协同收益

ADPO 的核心主张是：**单一策略模型可以同时作为生成器和验证器，在保持生成质量的前提下提供可靠的自我验证分数，从而在测试时通过 best-of-N 选择实现性能缩放**。实验在三个不同模态领域——多模态数学推理、图像定位和 GUI 代理——验证了这一主张。

**多模态数学推理**：在 MathVista 和 MMMU 上，ADPO 作为统一生成器-验证器的 best-of-8 性能分别达到 65.0% 和 52.1%，相较 GRPO + majority voting 的 62.9% 和 51.1% 分别提升 +2.1% 和 +1.0%（Table 2）。更重要的是，ADPO 的 pass@1 生成质量与 GRPO 相当，表明验证能力的增强并未牺牲生成性能。随着采样数增加，ADPO best-of-N 性能持续提升（N=4→8→12 在 MathVista 上分别为 64.8%→65.0%→65.3%），验证了自我验证分数对候选答案排序的有效性。

**图像定位**：在 ReasonSeg 上，ADPO 的 best-of-8 cIoU 达到 61.2，较 GRPO + majority voting 的 59.6 提升 +1.6（Table 3）。该任务使用 Qwen2.5-VL-7B 作为基座模型，训练数据为 RefCOCO，测试域为 out-of-domain 的 ReasonSeg，表明 ADPO 的验证能力具有一定的泛化性。

**GUI 代理**：在 AndroidControl 上，ADPO 的 best-of-8 步成功率（Step Success Rate）达到 72.7%，较 GRPO + majority voting 的 70.8% 提升 +1.9%（Table 4）。在 GUI Odyssey 上同样观察到一致的提升趋势。

**跨生成器-验证器组合实验**（Table 5）进一步揭示了一个关键现象：将 ADPO 作为验证器与 GRPO 生成器组合（GRPO + ADPO），其性能始终优于 GRPO 与自身验证器组合（GRPO + GRPO-Judge），且接近 ADPO 自生成自验证的完整方案。这表明 ADPO 习得的验证能力是可迁移的——即使面对来自不同策略的生成答案，ADPO 的验证分数仍然比 GRPO 自身的验证分数更可靠。

### 消融研究：偏好验证奖励 vs 二元验证奖励

**核心消融**（Table 9, Figure 4）对比了二元验证奖励（Eq.4）与偏好验证奖励（Eq.5）对验证能力和 best-of-N 性能的影响。在数学推理、图像定位和 GUI 代理三个领域，偏好验证奖励一致地提升了验证 AUC/AP（例如数学域 AUC 从 0.609 提升至 0.727）和 best-of-N 性能。二元验证奖励在训练后期因类别不平衡导致验证分数几乎全部收敛到 1（Figure 2），梯度消失，验证器失去判别力。偏好验证奖励通过构造对比集内的相对排序一致性信号，避免了这一问题——即使答案正确率升高，验证器仍需学习区分答案质量的细微差异。

**边际 γ 的消融**（Table 6）在 ReasonSeg 上考察了偏好验证奖励中边际参数 γ 的影响。当 γ=0.1 时取得最优整体 ACC 73.5%，表明适度的边际可以稳定排序学习；过大的 γ 会过度惩罚接近的候选对，反而损害性能。

**训练过程中的奖励信号分布分析**（Figure 7）显示，偏好验证奖励在整个训练过程中始终保持有意义的梯度信号（蓝色线代表的正确答案比例在偏好奖励=1 的响应中保持稳定），而二元验证奖励的信号质量随训练迅速退化（橙色线代表的正确答案比例在二元奖励=1 的响应中持续攀升）。

**分数分布对比**（Figure 8）表明，二元奖励训练的模型倾向于输出离散的极端分数（0 或 1），而偏好奖励训练的模型产生更多样化的连续分数分布，这为 best-of-N 选择提供了更细粒度的排序依据。

### 消融研究：优势解耦优化 vs 纠缠优势

**核心消融**（Table 10, Figure 5）对比了纠缠优势（Eq.8，将答案奖励和偏好奖励聚合后计算单一优势）与解耦优势（Eq.9，分别计算答案优势 $\hat{A}^{(a)}$ 和偏好优势 $\hat{A}^{(p)}$，并用 token 掩码隔离梯度）。在所有三个领域中，解耦优势均优于纠缠优势。在 GUI 代理任务上，解耦优势的 best@8 指标提升最为显著（+2.8%）。

**奖励黑客的预防**：纠缠优势下，模型可能通过输出极端的验证分数来操纵聚合奖励，而非真正提升答案质量或验证准确性。解耦优化通过独立的组归一化优势和 token 掩码，切断了这一梯度捷径——验证 token 的梯度仅受偏好奖励影响，答案 token 的梯度仅受答案奖励影响。

**组合消融**（Figure 6）展示了偏好验证奖励与优势解耦优化的叠加效果。仅使用偏好奖励（Binary→Preference）即可带来显著提升，再叠加解耦优化（Entangled→Decoupled）进一步增益。两者联合使用（ADPO 完整方案）在所有 k 值下均取得最优 best@k 性能。

### 统一验证 vs 分离验证

Table 7 对比了统一验证（ADPO 同时作为生成器和验证器）与分离验证（GRPO 作为生成器，GRPO 自身或多数投票作为验证器）的效率与性能。统一验证在保持或提升性能的同时，显著降低了推理开销——无需维护独立的验证模型，也无需额外的训练流程。这一结果直接回应了并行测试时扩展的核心瓶颈：分别训练生成器和验证器的高成本问题。

![[assets/figures/papers/paper_list_l2196_https_arxiv_org_abs_2601_01483/figures/011_Table_7.jpg]]
*Table 7: Comparison of unified and separate verification. GRPO: GRPO post-trained model as generator. +Major: majority voting as verifier. +Judge: GRPO post-trained model as verifier*

### 实验设置说明

训练超参数详见 Table 8。基座模型为 Qwen2-VL-7B（数学推理）和 Qwen2.5-VL-7B（定位与 GUI 代理）。答案奖励形式根据任务类型自适应选择：离散任务使用精确匹配二元奖励 $R_{\text{discrete}}^{a} = \text{match}(y, y^{*}) \in \{0, 1\}$，连续任务使用相似度连续奖励 $R_{\text{continuous}}^{a} = \text{sim}(y, y^{*}) \in [0, 1]$。所有 best-of-N 实验均使用 ADPO 自身输出的验证分数进行候选排序和选择。

### 补充图表

![[assets/figures/papers/paper_list_l2196_https_arxiv_org_abs_2601_01483/figures/004_Table_2.jpg]]
*Table 2: Performance on MathVista [22] and MMMU [45]. We adopt Qwen2-VL-7B [35] as the base model and use majority voting for both the base and GRPO models. We report accuracy (%) and highlight the best results in bold*

![[assets/figures/papers/paper_list_l2196_https_arxiv_org_abs_2601_01483/figures/005_Table_3.jpg]]
*Table 3: Performance on ReasonSeg [11]. We use Qwen2.5-VL-7B [1] as the base model*

![[assets/figures/papers/paper_list_l2196_https_arxiv_org_abs_2601_01483/figures/007_Table_4.jpg]]
*Table 4: Performance on AndroidControl [13] and GUI Odyssey [23]. We adopt Qwen2.5-VL-7B as base model and report type accuracy, grounding accuracy and step success rate (SR)*

![[assets/figures/papers/paper_list_l2196_https_arxiv_org_abs_2601_01483/figures/006_Table_5.jpg]]
*Table 5: Performance of different generator–verifier settings on MathVista [22], ReasonSeg [11] and AndroidControl [13]*

![[assets/figures/papers/paper_list_l2196_https_arxiv_org_abs_2601_01483/figures/018_Table_9.jpg]]
*Table 9: Ablation of Preference reward. Replacing the binary answer reward with our preference reward consistently strengthens self-verification (↑AUC/AP) and improves best of N selection performance on Math, Grounding, and GUI Agent*

![[assets/figures/papers/paper_list_l2196_https_arxiv_org_abs_2601_01483/figures/017_Table_10.jpg]]
*Table 10: Ablation study on decoupled advantages. Our advantage decoupled optimization consistently outperforms entangled advantage in both task performance and solution verification across mathematical reasoning, grounding, and GUI agent tasks*

![[assets/figures/papers/paper_list_l2196_https_arxiv_org_abs_2601_01483/figures/010_Table_6.jpg]]
*Table 6: Ablation of the margin γ for preference verification reward on ReasonSeg*



## 定位与知识库关联

### 1. 与现有基线的结构性关系

ADPO 的核心贡献在于将**生成**与**自我验证**统一到单一策略的强化学习框架中，其设计直接回应了现有并行测试时扩展（parallel test-time scaling）范式的两个关键瓶颈：训练与推理的资源冗余，以及单一组件训练时的性能天花板。

#### 1.1 相对于分离式生成-验证范式的改进

传统的测试时扩展通常采用“生成器 + 验证器”的分离架构。在此范式下，生成器（如 GRPO 微调后的策略模型）负责产生候选答案，验证器（如专门的验证模型或多数投票机制）负责从中择优。这种分离带来了两个问题：

1.  **资源成本高**：需要分别训练和部署两个模型，导致训练算力和推理显存的双重开销。
2.  **协同效应缺失**：仅优化生成器时，验证器无法从生成能力的提升中获益；反之亦然。论文通过交叉评估实验（Table 5）揭示了这一现象：当使用 GRPO 后训练模型作为生成器，并搭配另一个 GRPO 后训练模型作为独立验证器时，其性能（MathVista 63.5%）不仅低于 ADPO 的统一方案（65.0%），甚至低于简单的“GRPO 生成器 + 多数投票”（62.9%）。这表明，未经协同训练的独立验证器无法有效利用生成器的输出分布，反而可能引入噪声。

ADPO 通过**优势解耦优化**解决了这一协同问题。它在单一策略内分别计算答案优势 $\hat{A}^{(a)}$ 和偏好优势 $\hat{A}^{(p)}$，并通过 token 掩码 $M^{a}$ 和 $M^{p}$ 将两者的梯度隔离（Eq. 9）。这使得生成和验证两个目标可以在不互相干扰的前提下共享底层表征，从而在保持 pass@1 生成质量与 GRPO 持平的同时，输出可靠的自我验证分数。

#### 1.2 相对于强化学习基线的改进

在生成器的优化层面，ADPO 建立在 **GRPO**（分组相对策略优化）的基础之上。GRPO 通过组内归一化的优势估计来优化答案生成，但其奖励信号仅来自答案正确性 $R^{a}$。ADPO 在此基础上引入了**偏好验证奖励** $R^{p}$，将验证任务转化为一个排序问题。这一设计直接回应了二元验证奖励在训练后期因类别不平衡导致的**分数崩塌**问题：当答案正确率升高时，二元奖励 $R^{b} = \mathbb{1}\{(s - \tau_s)(R^{a} - \tau_a) > 0\}$ 会因正样本泛滥而几乎全部收敛到 1，导致梯度消失（Figure 2 证实，训练后期超过 80% 的正确答案其二元验证奖励为 1）。偏好验证奖励通过对比集内的相对排序一致性来提供监督信号，天然地避开了对绝对阈值的依赖，从而在整个训练过程中保持信息的有效性。

#### 1.3 相对于专门验证器的优势

论文将 ADPO 与专门的数学验证器 **MM-Verifier** 进行了对比。MM-Verifier 作为独立的验证模型，需要额外的训练数据和模型参数。ADPO 的统一方案在 MathVista 上以 best-of-8 策略取得了 65.0% 的准确率，不仅超越了 GRPO + 多数投票（62.9%），也验证了其自我验证能力可以媲美甚至超越需要额外训练的专门验证器。更重要的是，ADPO 的验证能力是生成过程的“副产品”，无需额外的推理时间开销，这直接带来了论文宣称的“-53.5% 推理时间”的优势。

### 2. 方法适用边界

ADPO 的设计使其天然适用于那些**答案质量可以客观度量、且存在明确优劣排序**的多模态任务。论文在三个差异显著的领域验证了其有效性，同时也揭示了方法的一些边界条件：

*   **离散答案任务**（如 MathVista、MMMU）：答案奖励使用完全匹配 $R_{\text{discrete}}^{a} = \text{match}(y, y^{\ast}) \in \{0, 1\}$。这类任务中，偏好验证奖励的优势最为明显，因为它能在高正确率场景下维持验证信号的区分度。
*   **连续答案任务**（如 ReasonSeg）：答案奖励使用相似度度量 $R_{\text{continuous}}^{a} = \text{sim}(y, y^{\ast}) \in [0, 1]$（如 cIoU）。在此类任务中，偏好验证奖励需要引入**边际 $\gamma$** 来处理答案质量差异微小的情况。消融实验（Table 6）表明，$\gamma = 0.1$ 时取得最优，这说明当答案间的质量差异低于某个阈值时，强制模型进行排序可能引入噪声，需要适当的容差机制。
*   **序列决策任务**（如 AndroidControl、GUI Odyssey）：这类 GUI 代理任务涉及多步交互，其验证需要评估动作序列的整体正确性。ADPO 在此类任务上的成功（best-of-8 步成功率 +1.9%）表明，偏好验证奖励的排序机制能够有效处理具有时间依赖性的验证问题。

然而，ADPO 的适用性存在以下边界：
1.  **奖励信号依赖性**：方法的核心假设是存在一个可自动计算的、能反映答案质量的奖励函数 $R^{a}$。对于那些难以定义自动奖励的开放式生成任务（如创意写作、对话生成），ADPO 的直接应用受限。
2.  **对比集构建**：偏好验证奖励依赖批次内构建的对比集 $\mathcal{C}_i$。当批次内答案质量高度同质化时（例如，所有候选答案都正确或都错误），排序信号会变得稀疏，可能影响训练效率。论文未深入探讨对比集构建策略对性能的影响。

### 3. 局限与开放问题

尽管 ADPO 在多个基准上取得了显著提升，论文自身揭示了一些值得进一步探索的问题：

1.  **奖励黑客的残余风险**：优势解耦优化被设计用于防止奖励黑客（reward hacking），即模型通过操纵验证分数来获取高奖励而非真正提升答案质量。消融实验（Table 10, Figure 5）证实了解耦优势相较于纠缠优势的优越性，但论文并未提供关于解耦后奖励黑客是否被完全消除的严格证明或诊断实验。在更复杂的任务中，模型是否可能学会在 token 掩码的边界处进行微妙的奖励黑客，仍是一个开放问题。

2.  **对比集大小的敏感性**：偏好验证奖励的计算依赖于对比集的大小 $|\mathcal{C}_i|$。论文未对该参数进行消融研究。理论上，过小的对比集可能导致排序信号方差大，过大的对比集可能引入无关比较的噪声。这一参数如何影响验证的校准性和训练的稳定性，值得进一步探索。

3.  **跨领域泛化的验证能力**：论文在 Table 5 中展示了不同生成器-验证器组合的性能。一个有趣的发现是，ADPO 作为验证器搭配 GRPO 生成器时，其性能（MathVista 63.5%）不如 ADPO 自生成自验证（65.0%）。这表明 ADPO 习得的验证策略与自身的生成分布存在某种“共生适应”。这种验证器是否能在完全不同的生成模型上保持有效性，论文未给出答案。

4.  **计算开销与可扩展性**：ADPO 的优势解耦优化需要为每个样本维护两组优势估计和 token 掩码，这增加了训练时的计算图复杂度。论文未报告 ADPO 相对于 GRPO 的训练时间或显存开销。对于更大规模的模型（如 13B、34B 参数级别），这种额外开销是否仍然可接受，需要实际验证。

5.  **与推理时扩展策略的深度结合**：ADPO 当前仅探索了 best-of-N 选择这一种测试时扩展策略。其输出的连续验证分数是否可以与更复杂的搜索策略（如树搜索、束搜索）结合，以进一步推动性能边界，是一个具有潜力的开放方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/Unified_Generation_and_Self_Verification_for_Vision_Language_Models_via_Advantage_Decoupled_Preference_Optimization.pdf]]
