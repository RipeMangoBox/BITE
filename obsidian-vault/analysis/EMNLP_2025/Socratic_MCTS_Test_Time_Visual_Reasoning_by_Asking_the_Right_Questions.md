---
title: "Socratic-MCTS: Test-Time Visual Reasoning by Asking the Right Questions"
type: paper
paper_level: A
venue: EMNLP
year: 2025
pdf_ref: paperPDFs/EMNLP_2025/Socratic_MCTS_Test_Time_Visual_Reasoning_by_Asking_the_Right_Questions.pdf
aliases:
- SM
- Socratic-MCTS
tags:
- EMNLP_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "在蒙特卡洛树搜索（MCTS）中显式定义子问题作为动作，利用子问题-子答案对构建推理节点，并通过组合式展开和内部一致性估计值函数，完全无外部监督地引导搜索。"
primary_logic: "将推理形式化为对子问题序列的搜索，每个子问题作为潜在决策，组合先前的推理轨迹来引导模型，并借助内部一致性作为奖励信号，在测试时从非推理VLM中提取长链推理，显著提升非符号类任务性能。"
claims:
- "Socratic-MCTS将推理形式化为以子问题为潜在决策的搜索过程。"
- "方法采用MCTS框架，子问题-子答案对作为节点，并通过内部一致性而非外部监督估计值。"
- "Socratic-MCTS在MMMU-PRO上整体提升2%，在Liberal Arts类别上提升9%。"
- "通过简单提示进行的分解（Least-to-Most）在所有基准上均不如直接回答和CoT，突显了非推理VLM与LLM的根本差异。"
---

# Socratic-MCTS: Test-Time Visual Reasoning by Asking the Right Questions

> [!tip] 核心洞察
> 将推理形式化为对子问题序列的搜索，每个子问题作为潜在决策，组合先前的推理轨迹来引导模型，并借助内部一致性作为奖励信号，在测试时从非推理VLM中提取长链推理，显著提升非符号类任务性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Socratic-MCTS：通过提出正确的问题进行测试时视觉推理 |
| 英文题名 | Socratic-MCTS: Test-Time Visual Reasoning by Asking the Right Questions |
| 会议/期刊 | EMNLP 2025 |
| Links | [paper](https://arxiv.org/abs/2506.08927) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Socratic-MCTS |
| Dataset | MMMU-Pro Liberal Arts, MMMU-Pro STEM+B, MMMU-Pro Overall, MMStar |

> [!tip] 效果简介
> - MMMU-Pro Liberal Arts 上，Accuracy 为 0.628，对比 0.538 (Direct)，变化 +9.0%。
> - MMMU-Pro STEM+B 上，Accuracy 为 0.492，对比 0.507 (Direct)，变化 -1.5%。
> - MMMU-Pro Overall 上，Accuracy 为 0.537，对比 0.517 (Direct)，变化 +2.0%。

## 概述

**问题瓶颈**：非推理视觉语言模型（VLM）在测试时难以通过常规思维链（CoT）提示激活其零散知识，缺乏结构化推理能力，无法自发产生长推理轨迹。实验显示，简单的分解式提示（如Least-to-Most）在所有基准上均不如直接回答和CoT，突显了非推理VLM与大型语言模型（LLM）的根本差异。

**核心方法**：Socratic-MCTS将视觉推理形式化为对子问题序列的搜索过程——每个子问题作为蒙特卡洛树搜索（MCTS）中的显式结构化动作，子问题-子答案对构成推理节点。搜索通过组合式展开和内部一致性加权投票来估计值函数，完全无需外部监督，在测试时从冻结的非推理VLM中提取长链推理。

**方法定位**：Socratic-MCTS属于测试时推理增强方法，通过MCTS框架将“提问”作为可搜索的潜在决策空间，区别于依赖外部监督或对数概率奖励的传统方法。其关键创新在于：显式定义子问题为动作、解耦答案策略以防止多模态错误传播、以及基于内部一致性的无监督值估计。

**主要结果**：在InternVL-78B上，Socratic-MCTS在MMMU-Pro整体准确率上提升2%（0.537 vs. Direct 0.517），其中Liberal Arts类别提升9%（0.628 vs. 0.538）；在MMStar上超越CoT基线2.2%（0.711 vs. 0.689）；在MathVista mini（英文多选题）上达到0.782，较CoT提升1.9%。方法在非符号类推理任务上优势显著，但在STEM+B等符号密集型任务上略有下降（-1.5%），揭示了结构化搜索在不同推理类型上的差异化效果。

## 背景与动机

### 问题背景：非推理视觉语言模型的推理瓶颈

视觉语言模型（VLM）在需要结构化多步推理的任务中面临根本性困难。与纯文本大语言模型（LLM）不同，非推理VLM的零散知识无法通过常规思维链（Chain-of-Thought, CoT）提示有效激活。核心瓶颈在于：**冻结的非推理VLM缺乏生成连贯长推理轨迹的能力**，即使提供CoT提示，模型也倾向于跳过关键推理步骤或产生不忠实的中间结论。

这一现象在非符号类视觉推理任务（如艺术史、音乐理论、文化分析等）中尤为突出。此类任务要求模型整合视觉感知、领域知识和逻辑推断，而非推理VLM的“一步到位”式回答往往无法建立正确的推理链路。

### 现有方法缺口：提示分解策略在VLM中的失效

在LLM领域，将复杂问题递归分解为子问题并自底向上求解的**Least-to-Most（LtM）**策略（Zhou et al., 2022）已被证明有效。然而，Socratic-MCTS的实验揭示了一个关键发现：**在VLM中，通过简单提示进行的分解（LtM）在所有基准上均不如直接回答和CoT**。这一结果突显了非推理VLM与LLM之间的根本差异——VLM无法像LLM那样可靠地执行提示引导的递归分解，因为其输出缺乏足够的忠实度和一致性。

现有的测试时推理增强方法（如CoT提示）仅产生单步推理链，无法系统性地探索多个可能的推理路径，也难以在无外部监督的情况下评估中间推理步骤的质量。

### 本文动机：将推理形式化为子问题搜索

Socratic-MCTS的出发点是：**将视觉推理重新定义为对子问题序列的搜索过程**。其核心洞察在于，每个子问题可以视为推理轨迹中的潜在决策节点，而通过组合先前的推理轨迹来引导模型，并借助内部一致性作为奖励信号，可以在测试时从冻结的非推理VLM中提取出长链推理能力。

这一思路借鉴了蒙特卡洛树搜索（MCTS）的结构化探索机制，但将其适配到“苏格拉底式”提问场景：**动作被显式定义为子问题**，而非隐式的词元采样；**节点状态由子问题-子答案对构成**，形成可组合的推理积木；**值估计完全依赖模型自身的内部一致性**，无需任何外部监督信号。这种设计使得方法能够在无额外训练的条件下，显著提升非符号类视觉推理任务的性能。

## 核心创新

### 瓶颈洞察：非推理VLM的“碎片化知识”困境

传统视觉语言模型（VLM）在未经专门推理训练的情况下，其内部知识呈现高度碎片化状态。常规思维链（Chain-of-Thought, CoT）提示无法有效激活这些零散知识，导致模型难以自发产生长推理轨迹。这一现象的根本原因在于：非推理VLM缺乏将孤立知识点“串联”为连贯推理链条的结构化能力。

实验证据直接支持了这一判断：在MMMU-Pro基准上，通过简单提示进行问题分解的Least-to-Most（LtM）方法在所有类别上均不如直接回答（Direct）和CoT，这与LtM在大语言模型（LLM）上的成功形成鲜明对比，突显了VLM与纯文本LLM在推理机制上的根本差异。

### 核心机制创新：将推理形式化为子问题搜索

Socratic-MCTS的核心洞察在于**将推理重新定义为对子问题序列的搜索过程**。具体而言，每个子问题被视为推理轨迹中的潜在决策（latent decision），通过组合先前的推理轨迹来引导模型，并借助内部一致性作为奖励信号，在测试时从冻结的非推理VLM中提取长链推理。

这一形式化带来了三个关键的结构性转变：

1. **动作定义的显式化**：不同于以往MCTS方法将隐式生成的词元或思考步骤作为动作，Socratic-MCTS将子问题（subquestion）显式定义为结构化的动态动作。这使搜索空间从连续的词元空间压缩到语义上有意义的“提问”空间，大幅降低了搜索复杂度。

2. **答案策略的解耦**：子问题的回答通过独立的答案策略 $\mathcal{M}_a(\cdot \mid I, s_{\tau+1})$ 完成，与推理轨迹的构建过程解耦。经验表明，这一解耦在多模态模型中至关重要——它能有效防止错误在子问题间传播，避免前序错误“污染”后续答案。

3. **无外部监督的值估计**：通过组合式展开（compositional rollouts）和内部一致性加权投票来估计节点价值，完全摆脱对外部监督或对数概率奖励的依赖。具体而言，从叶节点出发，使用 $K=8$ 种不同的总结短语（wrap-up phrases）进行展开，通过加权多数投票 $\arg\max_{a \in \mathcal{A}} \sum_{k=1}^{K} \mathbf{1}[\hat{a}^{(k)} = a] \cdot w^{(k)}$ 计算值估计。

### 方法谱系与知识库定位

Socratic-MCTS处于**测试时推理增强**与**结构化搜索**的交叉点，其方法谱系可沿以下维度定位：

| 维度 | 传统方法 | Socratic-MCTS |
|------|---------|---------------|
| 推理机制 | 单步思维链（无树搜索） | 基于MCTS的子问题-子答案对搜索 |
| 动作定义 | 隐式生成下一个词元或想法 | 显式将子问题定义为结构化动态动作 |
| 值估计 | 外部监督或基于对数概率的奖励 | 组合式展开的内部一致性加权投票（无外部监督） |
| 展开策略 | 标准自回归采样 | 在组合部分轨迹上使用多样化总结短语进行高效展开 |
| 早期退出 | 无 | 基于模型置信度的阈值（0.9）跳过搜索 |

与现有工作的关系：
- **相对于CoT提示**：Socratic-MCTS不依赖模型自发产生推理链，而是通过树搜索主动探索子问题空间，克服了非推理VLM在CoT下的“推理惰性”。
- **相对于Least-to-Most**：LtM通过递归分解问题并自底向上求解，但在VLM上因缺乏结构化搜索而表现不佳；Socratic-MCTS通过MCTS的探索-利用平衡机制弥补了这一缺陷。
- **相对于基于LLM的MCTS方法**：传统MCTS方法通常将词元或思考步骤作为动作，Socratic-MCTS首次将子问题显式定义为动作，并针对多模态场景设计了答案解耦和组合式展开机制。

### 效率机制：选择性搜索与早期退出

为控制计算开销，Socratic-MCTS引入了两个实用的效率机制：

- **置信度阈值早期退出**：在搜索开始前，先估计模型对直接答案的置信度。若置信度超过阈值（设为0.9），则跳过树搜索，直接输出答案。这在高置信度问题上显著减少了不必要的计算。
- **分层子问题生成**：第一层生成 $k_q=6$ 个子问题以充分探索，更深层仅生成 $k_q=3$ 个，平衡了探索广度与计算成本。

### 已知局限与开放问题

尽管Socratic-MCTS在非符号类任务上表现突出，其设计仍存在明确局限：

1. **计算效率瓶颈**：非自回归推理在GPU上效率较低，MCTS等结构化搜索方法在实践中比标准CoT更慢。如何提高此类方法在GPU上的效率是重要的工程挑战。
2. **VLM的过度自信问题**：冻结的VLM往往过度自信，即使有思维链提示也常常忽略推理线索，这限制了内部一致性信号的质量。
3. **符号推理的边界**：在MMMU-Pro的STEM+B类别上，Socratic-MCTS相比Direct略有下降（-1.5%），暗示该方法在更符号化的推理任务上可能不具有普适优势。

开放问题包括：超参数调优（$k_q$、$K$、探索常数$c$）和多智能体设置能否带来进一步增益；该方法在其他非推理VLM（如LLaVA-OneVision、Qwen2-VL）上的泛化表现如何；以及如何鼓励冻结VLM中思维链的忠实度和输出多样性。

## 整体框架

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2506_08927/figures/001_Figure_1.jpg]]
*Figure 1: Socratic-MCTS Overview. In Socratic-MCTS, actions are defined as subquestions, and each node state consists of a subquestion–subanswer pair. During search, rollouts are performed by preconditioning the model on the accumulated reasoning trajectory in a compositional manner. To structure this trajectory and enable faster rollouts, we use transition phrases (e.g., “First, I need to consider...”) and conclude with a wrapup phrase (e.g., “Summarizing, we have:”), which cue the model to complete the reasoning and produce a final answer. We estimate value through internal agreement and incorporate early-exit and selective search mechanisms to adaptively reduce computational overhead—all without e...*

Socratic-MCTS 的核心思路是将视觉推理重新形式化为一个**以子问题为潜在决策的搜索过程**。与标准思维链（CoT）提示中模型隐式生成下一个词元不同，该方法显式地将“提出子问题”定义为蒙特卡洛树搜索（MCTS）的动作空间，从而在冻结的非推理视觉语言模型（VLM）中构建结构化的长链推理轨迹。

### 推理范式与模块关系

整个框架围绕一个中心洞察展开：非推理 VLM 的零散知识无法通过常规 CoT 提示被有效激活，因为它们缺乏结构化推理能力。Socratic-MCTS 通过以下模块化流程解决这一瓶颈：

1. **置信度估计与早期退出**：在搜索开始前，模型先对原始查询生成初始答案并估计其置信度。若置信度超过预设阈值（实验中设为 0.9），则直接跳过树搜索，以降低计算开销。
2. **子问题生成策略**：从当前节点出发，模型根据原始查询、已累积的推理轨迹和一个指示模型提问的提示，采样有限个子问题作为候选动作。
3. **解耦答案策略**：每个子问题被独立地送入模型，仅基于图像和该子问题本身产生子答案。这一解耦设计在实验中证明对多模态模型至关重要——它能防止错误在推理链中传播或污染后续答案。
4. **MCTS 树导航与扩展**：通过 UCT（树的上置信界）公式选择最有前景的子节点进行扩展，在第一层生成更多子问题以鼓励探索，在更深层则减少子问题数以控制计算量。
5. **组合式展开与值估计**：从叶节点出发，将已累积的推理轨迹与多样化的总结短语组合，进行多次展开。最终通过加权多数投票计算节点的值估计，整个过程**完全无需外部监督**。
6. **反向传播**：将展开得到的奖励沿搜索路径向上传播，更新各节点的访问次数和累积奖励。

### 输入输出流

- **输入**：一张图像和一个自然语言查询。
- **输出**：经过结构化搜索后产生的最终答案，伴随一条由子问题-子答案对构成的显式推理轨迹。
- **中间状态**：每个 MCTS 节点在深度 τ 处的状态包含原始查询、当前推理轨迹、访问次数、累积奖励和经验值估计。

### 与传统方法的根本差异

在 VLM 场景下，简单的提示分解策略（如 Least-to-Most）在所有基准上均不如直接回答和 CoT，这揭示了非推理 VLM 与 LLM 之间的本质区别。Socratic-MCTS 通过将推理形式化为对子问题序列的搜索，并借助内部一致性作为奖励信号，成功从冻结的非推理 VLM 中提取出长链推理能力，尤其显著提升了非符号类任务的性能。

## 核心模块与公式推导

### 3.1 总体框架：将推理形式化为子问题搜索

Socratic-MCTS 的核心洞察在于：**将长链推理形式化为对子问题序列的搜索过程**，其中每个子问题作为潜在决策，组合先前的推理轨迹来引导模型，并借助内部一致性作为奖励信号。该方法完全在测试时运行，无需任何外部监督或微调。

框架将问题空间定义为一棵蒙特卡洛树，其中每个节点 $\mathbf{n}_\tau$ 在深度 $\tau$ 处的状态包含原始查询 $q$、当前推理轨迹 $T_\tau$、访问次数 $N$、累积奖励 $W$ 和经验值估计 $Q$：

$$\mathbf{n}_\tau := q, T_\tau, N, W, Q$$

### 3.2 动作定义：子问题作为结构化动态动作

与先前 MCTS 方法隐式采样词元或步骤作为动作不同，Socratic-MCTS **显式地将子问题定义为结构化动态动作**。在深度 $\tau$ 处，动作是从子问题策略 $\mathcal{M}_s$ 中采样的自包含子问题：

$$k_q \colon \{ s_{\tau+1}, \ldots, s_{\tau+k_q} \} \sim \mathcal{M}_s(\cdot \mid q, T_\tau, \mathfrak{p}_{\mathrm{sub}})$$

其中：
- $k_q$ 为每层采样的子问题数量（第一层 $k_q=6$，更深层 $k_q=3$）
- $\mathfrak{p}_{\mathrm{sub}}$ 是指示模型提问的提示模板
- $T_\tau$ 为当前累积的推理轨迹

### 3.3 答案生成：解耦答案策略防止错误传播

为每个子问题 $s_{\tau+1}$ 生成答案时，采用**解耦的答案策略** $\mathcal{M}_a$，在给定图像和子问题的条件下独立回答：

$$a_{s\tau+1} \sim \mathcal{M}_a(\cdot \mid I, s_{\tau+1})$$

这一解耦设计在多模态模型中至关重要——经验表明，若将子问题答案的生成与完整推理轨迹耦合，会导致错误传播或答案污染。实验中将子问题策略与答案策略统一为同一基础模型（$\mathcal{M}_s = \mathcal{M}_a = \mathcal{M}$）。

### 3.4 树导航与节点选择：UCT 引导搜索

搜索过程中，使用 UCT（Upper Confidence Bound for Trees） 分数选择子节点，平衡探索与利用：

$$\mathrm{UCT}(\mathbf{n}_{\tau+1}) = Q + c \sqrt{\frac{\ln N_{\mathrm{parent}}}{N_{\tau+1}}}$$

其中探索常数 $c=1.4$，$N_{\mathrm{parent}}$ 为父节点访问次数，$N_{\tau+1}$ 为当前子节点访问次数。

### 3.5 组合式展开与值估计：内部一致性作为奖励信号

从叶节点出发，采用**组合式展开**策略进行 $K=8$ 次独立展开：将模型条件化于累积推理轨迹 $T_{\tau+1}$，随后追加 $K$ 个不同的总结短语（wrap-up phrases），引导模型完成推理并产生最终答案。值估计通过加权多数投票实现：

$$V := \arg\max_{a \in \mathcal{A}} \sum_{k=1}^{K} \mathbf{1}[\hat{a}^{(k)} = a] \cdot w^{(k)}$$

其中 $\hat{a}^{(k)}$ 为第 $k$ 次展开产生的答案，$w^{(k)}$ 为基于答案有效性的权重。这一机制完全依赖内部一致性，无需外部监督信号。

### 3.6 选择性搜索与早期退出

为自适应降低计算开销，引入**基于模型置信度的早期退出机制**：在搜索开始前估计初始答案的置信度，若超过阈值（实验中设为 0.9），则跳过树搜索直接输出答案。这一机制使得高置信度问题无需承担完整的 MCTS 计算成本。

## 实验与分析

### 主结果

Socratic-MCTS 在多个多模态推理基准上一致优于直接回答（Direct）、思维链（CoT）和 Least-to-Most（LtM）基线。表 1 汇总了在 MMMU-Pro 和 MMStar 上的核心结果。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2506_08927/figures/003_Table_1.jpg]]
*Table 1: Performance across different reasoning benchmarks. Socratic MCTS consistently outperforms direct, CoT and LtM baselines across all benchmarks. We evaluate InternVL-78B Direct, CoT, LtM. Others results are for reference, unknown entries represented as*

**MMMU-Pro**：Socratic-MCTS 在整体准确率上达到 53.7%，较 Direct 基线的 51.7% 提升 2.0 个百分点。提升主要来自非符号类任务——在人文学科（Liberal Arts）子集上，方法取得 62.8% 的准确率，较 Direct 的 53.8% 大幅提升 9.0 个百分点。然而，在 STEM+B 子集上，Socratic-MCTS 为 49.2%，略低于 Direct 的 50.7%（-1.5%），提示该方法在需要符号操作的任务上可能不具优势。

**MMStar**：Socratic-MCTS 达到 71.1%，较 CoT 基线的 68.9% 提升 2.2 个百分点。

**MathVista**：在仅包含英文选择题的 MathVista mini 子集上（表 2），Socratic-MCTS 达到 78.2%，高于 Direct 的 74.0%、CoT 的 76.3% 和 LtM 的 47.1%，进一步验证了方法的跨基准泛化能力。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2506_08927/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative comparison on MMMU-PRO. We show Socratic-MCTS responses on non-symbolic tasks comparing qualitatively against the best-performing baseline in this benchmark (direct prompting). Table 2: Performance on MathVista mini further filtered to include only multiple-choice questions in English*

值得注意的是，LtM（Least-to-Most）分解策略在所有基准上均大幅落后于 Direct 和 CoT，甚至低于直接回答。这一现象突显了非推理 VLM 与 LLM 的根本差异：在 VLM 中，通过简单提示进行问题分解无法激活结构化推理，反而可能引入干扰。

### 消融分析

论文未提供独立的消融实验表格，但方法设计中的若干关键选择构成了隐含的消融证据：

- **解耦答案策略**：子问题的答案通过独立的答案策略 $\mathcal{M}_a(\cdot \mid I, s_{\tau+1})$ 生成，而非将子问题嵌入完整推理轨迹后让模型自回归回答。论文明确指出，这一解耦在多模态模型中至关重要，可防止错误传播或答案污染（Section 3.1）。若缺少此设计，子问题答案可能被前序推理中的幻觉或偏差所污染。

- **组合式展开与内部一致性**：值估计不依赖外部监督，而是通过对叶节点进行 $K=8$ 次组合式展开，并采用加权多数投票计算内部一致性。论文指出，使用多样化的总结短语（wrap-up phrases）可产生足够的响应变异性以支撑一致性计算（Section 3.2）。若 $K$ 过小或短语缺乏多样性，值估计的可靠性将下降。

- **子问题数量配置**：第一层树展开时生成 $k_q=6$ 个子问题，更深层则降至 $k_q=3$。这一设置平衡了搜索的广度与计算开销（Section 3.2）。

- **早期退出机制**：当模型对初始答案的置信度超过阈值 0.9 时，跳过树搜索直接输出答案。该机制可减少高置信度问题的计算开销，但论文未量化其节省的计算量或对准确率的影响，需手动验证。

### 失败模式

图 4 展示了 Socratic-MCTS 在 MMStar 和 MMMU-Pro 上的失败案例。结合论文讨论，主要失败模式包括：

1. **冻结 VLM 的过度自信**：即使提供思维链提示，冻结的 VLM 往往忽略推理线索，直接输出看似合理但错误的答案。Socratic-MCTS 的子问题机制虽能部分缓解此问题，但无法从根本上改变模型的置信度校准。

2. **符号类任务的退化**：在 MMMU-Pro 的 STEM+B 子集上，Socratic-MCTS 准确率低于 Direct 基线，表明该方法在需要精确符号操作的任务上可能引入噪声，子问题分解未能有效激活相关数学知识。

3. **搜索效率瓶颈**：非自回归的结构化搜索方法（如 MCTS）在 GPU 上效率较低，实践中更慢。论文未报告具体推理延迟或计算开销对比，这是评估方法实用性的关键缺失。

### 重要图表结论

- **图 1（方法总览）**：展示了 Socratic-MCTS 的完整流程——子问题作为动作、子问题-子答案对作为节点状态、组合式展开进行值估计、以及早期退出和选择性搜索机制。该图是理解方法架构的核心参考。

- **图 2（MMStar 定性比较）**：通过两个多模态问题的对比案例，展示了 Socratic-MCTS 如何帮助模型发掘相关知识、验证中间步骤并连贯地合成最终答案，而 CoT 基线则产生表面化或错误的推理。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2506_08927/figures/002_Figure_2.jpg]]
*Figure 2: Qualitative comparison on MMStar. We show Socratic-MCTS responses on two multimodal questions from the benchmark, comparing qualitatively against the CoT prompting baseline. Socratic-MCTS allows the model to uncover relevant knowledge, verify intermediate steps, and synthesize final answers coherently*

- **图 3（MMMU-Pro 定性比较）**：在非符号任务上，Socratic-MCTS 相较于 Direct 基线展现出更深入的知识关联和推理链条。

- **表 1（主结果表）**：全面对比了 InternVL-78B 在 Direct、CoT、LtM 和 Socratic-MCTS 下的性能，是论文实验部分的核心证据。表中还引用了其他方法的参考结果，但未知条目以“-”表示。

- **表 2（MathVista 补充结果）**：在英文选择题子集上进一步验证了方法的有效性，同时再次确认 LtM 在 VLM 上的严重退化。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2506_08927/figures/004_Figure.jpg]]
*Figure: (a) Socratic-MCTS on a multimodal color theory question. (b) Socratic-MCTS on a music question*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

Socratic-MCTS 的核心贡献在于将推理形式化为**以子问题为显式动作的树搜索过程**，这与现有提示策略构成了根本性差异。

**与 Chain-of-Thought (CoT) 的关系。** 标准 CoT 提示通过单步自回归采样生成推理轨迹，缺乏对推理路径的结构化探索。Socratic-MCTS 将 CoT 的线性生成替换为基于 MCTS 的树搜索，在测试时主动探索多条子问题-子答案路径，并通过内部一致性信号选择最优轨迹。实验表明，在 InternVL-78B 上，Socratic-MCTS 在 MMStar 上超越 CoT 基线 2.2%（0.711 vs 0.689），在 MathVista 上超越 1.9%（0.782 vs 0.763），验证了结构化搜索相对于单步采样的增益。

**与 Least-to-Most (LtM) 的关系。** LtM（Zhou et al., 2022）通过递归分解问题并自底向上求解来实现复杂推理。然而，论文发现了一个关键洞察：**在非推理 VLM 中，通过简单提示进行的问题分解（LtM）在所有基准上均不如直接回答和 CoT**（例如 MMMU-Pro 上 LtM 仅 0.280，远低于 Direct 的 0.517 和 CoT 的 0.506）。这揭示了 VLM 与 LLM 在推理行为上的根本差异——VLM 的碎片化知识无法通过常规提示分解有效激活。Socratic-MCTS 通过将分解过程嵌入到有引导的搜索框架中，以内部一致性作为奖励信号，克服了纯提示分解的局限。

**与基于 MCTS 的推理方法的关系。** 与以往在 LLM 中将隐式词元或推理步骤作为动作的 MCTS 方法不同，Socratic-MCTS 将动作显式定义为**结构化的动态子问题**（Section 3.1）。这一设计选择使得搜索空间更具可解释性，同时允许模型在组合先前推理轨迹的基础上进行条件化展开。此外，Socratic-MCTS 的值估计完全依赖内部一致性加权投票，无需外部监督或对数概率奖励，这与依赖外部奖励或过程监督的现有方法形成对比。

### 2. 适用边界与局限

**任务类型边界。** Socratic-MCTS 在非符号类推理任务上表现突出——MMMU-Pro 的 Liberal Arts 类别提升 9%（0.628 vs 0.538），但在符号化程度较高的 STEM+B 类别上反而下降 1.5%（0.492 vs 0.507）。这表明该方法更适用于需要知识整合和语义推理的任务，而在需要精确符号操作的领域可能引入不必要的搜索开销或错误累积。

**模型依赖性。** 当前实验主要在 InternVL-78B 上进行，该方法在其他非推理 VLM（如 LLaVA-OneVision、Qwen2-VL 等）上的泛化性尚未验证。此外，冻结 VLM 的过度自信倾向（即使有 CoT 提示也常忽略推理线索）构成了方法有效性的潜在瓶颈——当模型对子问题的回答质量较差时，搜索框架难以弥补基础能力的不足。

**计算效率局限。** 非自回归推理在 GPU 上效率较低，MCTS 等结构化搜索方法在实践中比标准 CoT 更慢。尽管论文引入了置信度阈值为 0.9 的早期退出机制来减少高置信度问题的计算开销，但搜索过程本身的计算成本（包括 k_q=6 的首层扩展和 K=8 次展开）仍然显著。超参数调优和多智能体设置等可能进一步提升性能的方向因计算成本未被探索。

### 3. 开放问题

1. **效率优化。** 如何提高结构化搜索方法（如 MCTS）在 GPU 上的推理效率，使其在计算成本上接近单步 CoT，是实际部署的关键挑战。

2. **VLM 推理忠实度。** 如何在冻结的 VLM 中鼓励思维链的忠实度和输出多样性，使模型不因过度自信而忽略关键推理线索，是该方法效果上限的决定性因素。

3. **跨模型泛化。** Socratic-MCTS 在其他非推理 VLM 上的表现如何，以及该方法是否可以从更强的推理模型中受益（如使用推理模型作为答案策略 M_a），有待系统验证。

4. **超参数与多智能体扩展。** 超参数调优（如子问题数量 k_q、展开次数 K、探索常数 c）以及多智能体设置（异构子问题策略和答案策略）能否带来进一步的性能提升，是值得探索的方向。

5. **符号推理的适应性。** 该方法在更符号化的推理任务（如数学符号计算）上是否能通过调整子问题策略和值估计机制来保持优势，仍需研究。

## 原文 PDF

![[paperPDFs/EMNLP_2025/Socratic_MCTS_Test_Time_Visual_Reasoning_by_Asking_the_Right_Questions.pdf]]
