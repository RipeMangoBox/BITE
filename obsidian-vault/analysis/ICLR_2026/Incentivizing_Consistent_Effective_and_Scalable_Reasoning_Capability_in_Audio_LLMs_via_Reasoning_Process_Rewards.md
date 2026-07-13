---
title: "Incentivizing Consistent, Effective and Scalable Reasoning Capability in Audio LLMs via Reasoning Process Rewards"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Incentivizing_Consistent_Effective_and_Scalable_Reasoning_Capability_in_Audio_LLMs_via_Reasoning_Process_Rewards.pdf
project_link: null
code_link: null
openreview_forum_id: DUr48hxO2h
aliases:
- ICESRCALRPR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将训练奖励从结果正确性扩展为多维度过程奖励（一致性、结构化关键词、领域知识、长度惩罚），直接塑造推理过程的质量。这一过程奖励的设计是逆转测试时逆规模、实现可控推理规模化的关键控制变量。"
primary_logic: "真正的推理能力不能仅靠结果奖励自发涌现，而需要显式地对推理过程进行多维度激励。通过奖励推理与答案/问题的一致性、结构化分析模式、领域知识运用以及适当深度，可以将推理从不可靠的副产品转变为可控、可测的技能，并能发现模型特定的“推理甜点”（reasoning sweet spot）以实现最优测试时性能。"
claims:
- "基础模型启动推理后性能不升反降，从68.60%降至65.20%，出现测试时逆规模。"
- "CESAR 扭转逆规模，启用推理后总准确率达到77.10%，显著超越所有基线。"
- "线性回归分析显示，基础模型的规模斜率 β=−0.51，CESAR 为 β=+0.038，实现从负向到正向的完全逆转。"
- "消融实验证实：取消过程奖励（一致性、关键词）导致准确率显著下降；取消过度思考惩罚使推理与非推理模式差距缩小，表明各组件均为必要。"
---

# Incentivizing Consistent, Effective and Scalable Reasoning Capability in Audio LLMs via Reasoning Process Rewards

> [!tip] 核心洞察
> 真正的推理能力不能仅靠结果奖励自发涌现，而需要显式地对推理过程进行多维度激励。通过奖励推理与答案/问题的一致性、结构化分析模式、领域知识运用以及适当深度，可以将推理从不可靠的副产品转变为可控、可测的技能，并能发现模型特定的“推理甜点”（reasoning sweet spot）以实现最优测试时性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过推理过程奖励激励音频LLM的一致、有效且可扩展推理能力 |
| 英文题名 | Incentivizing Consistent, Effective and Scalable Reasoning Capability in Audio LLMs via Reasoning Process Rewards |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=DUr48hxO2h) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | CESAR |
| Dataset | MMAU Test-mini, MMSU, MMAU-Pro, MMAR |

> [!tip] 效果简介
> - MMAU Test-mini 上，Overall Accuracy (%) 为 77.10，对比 74.60 (Ke-Omni-R)，变化 +2.5。
> - MMSU 上，Overall Accuracy (%) 为 64.24，对比 62.08 (Ke-Omni-R)，变化 +2.16。
> - MMAU-Pro 上，Average Accuracy (%) 为 56.4，对比 54.5 (Ke-Omni-R)，变化 +1.9。

## 概要

音频大语言模型（Audio LLM）在推理时面临一个根本性瓶颈：当模型被要求生成显式推理链时，性能不升反降——推理链越长，准确率越差。这一现象被称为**测试时逆规模**（test-time inverse scaling）。在 **Qwen2.5-Omni-7B**（Xu et al., 2025）基础模型上，启用推理后准确率从 68.60% 降至 65.20%，规模斜率 β = −0.51，表明模型学习的推理模式存在幻觉、推理-答案不一致和逻辑混乱等系统性问题。其根本原因在于，现有基于结果奖励的强化学习（RLVR）仅以最终答案正确性为监督信号，无法塑造推理过程的质量。

**CESAR** 的核心洞察是：真正的推理能力不能仅靠结果奖励自发涌现，而需要对推理过程进行显式的多维度激励。该方法将训练奖励从单一的结果正确性扩展为**多面过程奖励**——包括推理-答案一致性、结构化关键词（模式、逻辑、领域知识）和过度思考惩罚——从而将推理从不可靠的副产品转变为可控、可测的技能。

在方法定位上，CESAR 以 **Group Relative Policy Optimization (GRPO)** 为训练框架，在 **Ke-Omni-R**（Zhao et al., 2025）的结果奖励 RL 基线上，将奖励函数从仅含准确性与格式的二元信号，改造为包含过程质量的多维奖励。这一设计直接逆转了测试时逆规模：CESAR 的规模斜率变为 β = +0.038，推理启用后总准确率达到 77.10%，超越所有基线。

主要实验结果如下：

- **MMAU Test-mini**：CESAR 达到 77.10%，较 Ke-Omni-R（74.60%）提升 +2.5 个百分点，超越 **GPT-4o Audio**（Hurst et al., 2024）和 **Gemini 2.5 Pro**（Comanici & et al., 2025）。
- **MMSU**：总准确率 64.24%，较 Ke-Omni-R（62.08%）提升 +2.16 个百分点，推理任务接近人类水平。
- **MMAU-Pro**：平均准确率 56.4%，较 Ke-Omni-R（54.5%）提升 +1.9 个百分点。
- **MMAR**：总准确率 62.70%，较 Ke-Omni-R（60.90%）提升 +1.80 个百分点。

消融实验证实，过程奖励的每个组件均为必要：移除一致性奖励导致准确率下降 0.9%，移除关键词奖励进一步下降 1.0%，移除过度思考惩罚则使推理与非推理模式的性能差距从 3.4 点缩小至 1.5 点。此外，CESAR 能够发现模型特定的“推理甜点”（reasoning sweet spot），在该点实现最优测试时性能，推理延迟仅增加 0.08 秒（1.8% 开销）。

方法的局限性包括：GRPO 在线训练计算开销大（8×H200 GPU 上需 61.44 小时）；感知能力仍是瓶颈（MMSU 感知任务平均 48.45%，远低于人类的 91.24%）；以及多面过程奖励框架的跨模态泛化性尚未验证。

音频大语言模型（Audio LLM）在声音理解、音乐分析和语音交互等任务上取得了显著进展，但其推理能力仍停留在基础水平。一个核心矛盾在于：当模型被要求显式地“思考”——即生成推理链后再作答时，其性能不仅没有提升，反而出现系统性的退化。这种**测试时逆规模现象**（test-time inverse scaling）表明，推理链越长，模型的准确率越低：基础模型 Qwen2.5-Omni-7B 在不启用推理时准确率为 68.60%，而启用推理后骤降至 65.20%（Table 1 / Table 18）。换言之，推理过程本身成为了性能的拖累，而非助力。

这一现象的根本原因在于当前主流的训练范式。现有的音频推理模型训练方法——无论是监督微调（SFT）还是基于结果验证的强化学习（RLVR）——都仅以最终答案的正确性和格式合规性作为监督信号。以 **Ke-Omni-R**（Zhao et al., 2025）为代表的 RLVR 方法，其奖励函数仅包含两项：

$$R_{\mathrm{RLVR}}(s_i) = \mathbb{I}[\hat{y}_i = y_i] + \mathbb{I}[\mathrm{ValidFormat}(s_i)]$$

这种**结果导向的奖励机制**存在一个致命缺陷：它不关心模型“如何”得到答案。模型可以通过随机猜测、模式匹配或表面语言线索碰巧答对，从而获得正向奖励，但其推理过程可能充满幻觉、逻辑断裂或与最终答案完全脱节。久而久之，模型学会了“答对即可”的策略，而非真正的分析能力。当推理链被强制生成时，这些虚假的推理模式就会暴露出来，导致性能崩溃。

因此，问题的瓶颈不在于模型是否“能够”推理，而在于**缺乏对推理过程本身的显式监督与塑造**。仅靠结果奖励，真正的推理能力无法自发涌现。这构成了本文的核心动机：能否设计一种训练机制，将推理从一个不可靠的副产品转变为一个可控、可测、可优化的技能？

## 核心方法与创新机理

### 问题诊断：从结果奖励到过程奖励的范式转移

音频LLM在引入推理链后普遍面临一个反直觉的瓶颈：**测试时逆规模现象**（test-time inverse scaling）。基础模型 Qwen2.5-Omni-7B 在启用推理后，准确率从 68.60% 降至 65.20%（Table 1 / Table 18），线性回归分析进一步量化了这一退化——其规模斜率 $\beta = -0.51$（Figure 8 / Appendix D.12），意味着推理链越长，性能越差。根因在于，现有 RL 训练范式（如 **Ke-Omni-R**，Zhao et al., 2025）仅以最终答案正确性与格式合规为监督信号（即结果奖励），模型在缺乏过程约束时学到了表面正确但逻辑混乱的推理模式，表现为推理-答案脱节、幻觉滋生、关键分析步骤缺失。

CESAR 的核心洞察是：**真正的推理能力需要显式地对推理过程进行多维度激励，而非依赖结果奖励的自发涌现**。这一洞察直接塑造了方法设计的全部 changed slots。

### 关键创新一：多面过程奖励函数

CESAR 将训练奖励从单一的结果正确性扩展为**五维加权组合**，直接塑造推理过程的质量：

$$R_{\mathrm{total}}(s_i) = \alpha_1 R_{\mathrm{acc}}(s_i) + \alpha_2 R_{\mathrm{format}}(s_i) + \alpha_3 R_{\mathrm{consistency}}(s_i) + \alpha_4 R_{\mathrm{keywords}}(s_i) + \alpha_5 R_{\mathrm{overthinking\ penalty}}(s_i)$$

其中前三项继承自结果奖励范式，后三项是 CESAR 的过程奖励创新：

- **一致性奖励**（$R_{\mathrm{consistency}}$）：通过语义相似度 $R_{\mathrm{consistency}}(s_i) = \mathrm{Sim}_{\mathrm{semantic}}(t_i, \hat{y}_i) + \mathrm{Sim}_{\mathrm{semantic}}(t_i, Q_i)$，强制推理过程与预测答案和问题上下文对齐。消融实验证实，移除该奖励导致总准确率从 77.10% 降至 76.20%，并引发推理-答案脱节（Table 6 / Table 21）。

- **关键词奖励**（$R_{\mathrm{keywords}}$）：三组件设计 $R_{\mathrm{keywords}}(s_i) = R_{\mathrm{pattern}}(s_i) + R_{\mathrm{logic}}(s_i) + R_{\mathrm{domain}}(s_i)$，分别激励结构化分析模式（如“首先/其次/因此”）、逻辑严谨与因果推理（如“因为/导致/如果…则”）、领域知识整合（如“频率/音高/音色”）。移除该奖励进一步将准确率降至 75.20%，表明显式的结构化推理激励对培养有效分析策略至关重要。

- **过度思考惩罚**（$R_{\mathrm{overthinking\ penalty}}$）：线性惩罚 $R_{\mathrm{overthinking\ penalty}}(s_i) = 1 - \frac{|t_i|}{L_{\mathrm{max\_output}}}$，鼓励模型在适当深度停止推理。移除该惩罚使推理与非推理模式的性能差距从 3.4 点缩小至 1.5 点，说明该组件帮助模型识别何时需要深度推理，避免冗余和幻觉。

### 关键创新二：GRPO 结合过程奖励的在线训练

CESAR 采用 **Group Relative Policy Optimization (GRPO)** 作为训练算法，但将其从单纯的结果验证器转变为**过程塑造引擎**。训练循环中，每个样本采样 $K=8$ 个回复，通过多面奖励计算器（Algorithm 2）计算相对优势，更新策略并加入 KL 正则化：

$$\mathcal{L}_{\mathrm{GRPO}} = \mathcal{L}_{PG}^{\mathrm{multi-faceted}} + \beta \cdot \mathcal{L}_{KL}$$

与仅使用结果奖励的 RLVR 基线相比，GRPO 的过程奖励信号在在线采样中持续校准推理质量，使得模型在训练过程中逐步内化结构化分析模式、逻辑推导和领域知识运用。

### 关键创新三：推理可控化与“推理甜点”

CESAR 将推理从不可靠的副产品转变为可控技能。通过测试时规模分析 $P(L_{\mathrm{max.think}}) = \mathbb{E}[\mathbb{I}[\hat{y} = y] \mid |t| \leq L_{\mathrm{max.think}}]$，模型能够发现**推理甜点** $L_{\mathrm{sweet}} = \arg\max_L P(L)$——即最优推理深度。CESAR 在约 35-40 tokens 的推理链长度上达到 77.10% 的峰值准确率（Figure 3 左），而基础模型的规模斜率从 $\beta=-0.51$ 反转为 $\beta=+0.038$（Figure 8），实现了从负向到正向的完全逆转。这一可控性使得推理深度可以根据任务难度动态调整，而非盲目延长推理链。

### 关键创新四：答案不变的数据增强

为提升训练数据的多样性与泛化性，CESAR 引入**答案不变的模板变换**：对每个训练问题应用变换模板 $T = \{T_1, ..., T_M\}$，生成多种语言变体 $q'_{i,k} = T_k(q_i, C_i)$，保持答案不变。这一增强策略在单一 AVQA 数据集上扩展了训练规模，配合 GRPO 在线采样，缓解了过程奖励训练对数据覆盖的依赖。

### 创新总结：changed slots 与因果机制

| 变更槽位 | 基线值 | CESAR 方案 | 因果作用 |
|---------|--------|-----------|---------|
| 奖励函数 | 仅结果奖励（答案正确+格式） | 五维过程奖励（一致性、关键词、过度思考惩罚） | 直接塑造推理过程质量，逆转测试时逆规模 |
| 训练算法 | 结果验证的 RLVR | GRPO + 多面奖励 | 在线采样中持续校准推理模式 |
| 推理控制 | 自发涌现 | 关键词奖励激励结构化分析；过度思考惩罚校准深度 | 将推理变为可控技能，发现推理甜点 |
| 数据增强 | 原始 AVQA 数据 | 答案不变的模板变换 | 扩展训练覆盖，提升泛化性 |

消融实验的渐进式验证（Table 6 / Table 21）确认了各组件的必要性：移除 RL 后训练导致准确率骤降 11.9 点（74.60% → 65.20%），移除一致性奖励降 0.9 点，移除关键词奖励再降 1.0 点，移除过度思考惩罚使推理优势缩水。这一因果链证实了过程奖励是逆转逆规模、实现可控推理规模化的关键控制变量。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_DUr48hxO2h/figures/001_Figure_1.jpg]]
*Figure 1: General Framework of Different Training Methods for Audio Reasoning Models*

CESAR 的核心设计理念是将音频LLM的推理能力从不可控的副产品转化为可训练、可校准的技能。其整体框架由三个关键模块串联构成，形成从数据准备到策略优化的闭环。

**数据增强模块**是训练管线的入口。针对音频视觉问答（AVQA）数据集中的每个样本，该模块应用一组答案不变的变换模板 $\mathcal{T} = \{T_1, ..., T_M\}$，对原始问题 $q_i$ 和选项 $\mathcal{C}_i$ 进行词句层面的改写，生成多个语言变体 $q'_{i,k} = T_k(q_i, \mathcal{C}_i)$。这一步骤在不改变音频输入和正确答案的前提下，有效扩充了训练规模，为后续的在线强化学习提供了更丰富的探索空间。

**GRPO 在线训练循环**是框架的引擎。模型 $\pi_\theta$ 对每个增强后的训练样本采样 $K=8$ 个回复，每个回复遵循结构化输出格式：

$$\pi_\theta(a_i, q_i, \mathcal{C}_i) = \langle\text{think}\rangle\, t_i \,\langle/\text{think}\rangle \langle\text{answer}\rangle\, \hat{y}_i \,\langle/\text{answer}\rangle$$

其中 $t_i$ 为推理链，$\hat{y}_i$ 为最终预测答案。GRPO 基于组内相对优势计算策略梯度，并加入 KL 正则化项以稳定训练：

$$\mathcal{L}_{\mathrm{GRPO}} = \mathcal{L}_{PG}^{\mathrm{multi\text{-}faceted}} + \beta \cdot \mathcal{L}_{KL}$$

训练目标是最大化期望奖励 $\pi^* = \arg\max_\pi \mathbb{E}[R(s_i)]$，其中 $s_i$ 为完整的模型输出序列。

**多面奖励计算器**是框架的核心创新，它将传统的结果导向奖励扩展为五维加权组合：

$$R_{\mathrm{total}}(s_i) = \alpha_1 R_{\mathrm{acc}}(s_i) + \alpha_2 R_{\mathrm{format}}(s_i) + \alpha_3 R_{\mathrm{consistency}}(s_i) + \alpha_4 R_{\mathrm{keywords}}(s_i) + \alpha_5 R_{\mathrm{overthinking\ penalty}}(s_i)$$

- **准确性奖励** $R_{\mathrm{acc}}$：二元信号 $\mathbb{I}[\hat{y}_i = y_i]$，保证答案正确性。
- **格式奖励** $R_{\mathrm{format}}$：验证输出是否符合 XML 标签结构。
- **一致性奖励** $R_{\mathrm{consistency}}$：通过语义相似度确保推理过程与预测答案及问题上下文对齐，防止推理-答案脱节。
- **关键词奖励** $R_{\mathrm{keywords}}$：三组件设计，分别激励结构化分析模式、逻辑推导和领域知识运用。
- **过度思考惩罚** $R_{\mathrm{overthinking\ penalty}} = 1 - |t_i| / L_{\mathrm{max\_output}}$：对推理长度进行线性惩罚，引导模型在适当深度停止。

这三个模块协同运作：数据增强提供多样化的训练样本，GRPO 在线采样多个回复并计算相对优势，多面奖励计算器为每个回复提供细粒度的过程信号。这一闭环设计使得模型不仅被训练为给出正确答案，更被显式塑造为具备一致、结构化、深度可控的推理能力。

### 3.1 问题形式化与训练范式

音频LLM接收三元组输入 $(a_i, q_i, \mathcal{C}_i)$，其中 $a_i$ 为音频信号，$q_i$ 为问题文本，$\mathcal{C}_i$ 为候选选项集。模型输出遵循结构化格式：

$$\pi_{\theta}(a_i, q_i, \mathcal{C}_i) = \langle\text{think}\rangle\ t_i\ \langle/\text{think}\rangle\ \langle\text{answer}\rangle\ \hat{y}_i\ \langle/\text{answer}\rangle$$

其中 $t_i$ 为推理过程，$\hat{y}_i$ 为最终预测答案。强化学习微调的目标是最大化期望奖励：

$$\pi^* = \arg\max_{\pi}\ \mathbb{E}[R(s_i)]$$

现有方法（如 **Ke-Omni-R**，Zhao et al., 2025）采用仅结果导向的奖励：

$$R_{\mathrm{RLVR}}(s_i) = \mathbb{I}[\hat{y}_i = y_i] + \mathbb{I}[\mathrm{ValidFormat}(s_i)]$$

核心洞察在于：真正的推理能力需要显式的过程导向激励，而非仅依赖结果信号的自发涌现。CESAR 将奖励函数从结果正确性扩展为多维度过程奖励，直接塑造推理过程的质量。

### 3.2 多面过程奖励设计

总奖励由可验证奖励（准确性、格式）和推理过程奖励（一致性、关键词、过度思考惩罚）加权组合：

$$R_{\mathrm{total}}(s_i) = \alpha_1 R_{\mathrm{acc}}(s_i) + \alpha_2 R_{\mathrm{format}}(s_i) + \alpha_3 R_{\mathrm{consistency}}(s_i) + \alpha_4 R_{\mathrm{keywords}}(s_i) + \alpha_5 R_{\mathrm{overthinking\ penalty}}(s_i)$$

其中权重经调优设为 $\alpha_1 = 5.0$，$\alpha_2 = \alpha_3 = \alpha_4 = \alpha_5 = 1.0$（详见 Table 23 敏感性分析）。

#### 3.2.1 可验证奖励

- **准确性奖励**：$R_{\mathrm{acc}}(s_i) = \mathbb{I}[\hat{y}_i = y_i]$，二元信号，判断答案是否正确。
- **格式奖励**：$R_{\mathrm{format}}(s_i) = \mathbb{I}[\mathrm{ValidFormat}(s_i)]$，强制要求输出符合 `<think>...</think><answer>...</answer>` 的 XML 标签结构。

#### 3.2.2 推理-答案一致性奖励

该组件是逆转推理-答案脱节的关键控制变量。通过语义相似度确保推理过程同时与预测答案和问题上下文对齐：

$$R_{\mathrm{consistency}}(s_i) = \mathrm{Sim}_{\mathrm{semantic}}(t_i, \hat{y}_i) + \mathrm{Sim}_{\mathrm{semantic}}(t_i, Q_i)$$

语义相似度基于概念重叠实现，归一化至 $[0,1]$：

$$\mathrm{Sim}_{\mathrm{semantic}}(x, y) = \frac{\mathrm{ConceptOverlap}(x, y)}{\max(|\mathrm{Concepts}(x)|, |\mathrm{Concepts}(y)|)}$$

消融实验证实：移除一致性奖励使总准确率从 77.10% 降至 76.20%，并导致推理与答案脱节（Table 6/Table 21）。

#### 3.2.3 结构化关键词与过度思考惩罚

**关键词奖励**采用三分量设计，显式激励结构化分析模式、逻辑推导和领域知识运用：

$$R_{\mathrm{keywords}}(s_i) = R_{\mathrm{pattern}}(s_i) + R_{\mathrm{logic}}(s_i) + R_{\mathrm{domain}}(s_i)$$

- $R_{\mathrm{pattern}}$：奖励结构化分析模式关键词（如 "first", "then", "therefore"，完整列表见 Table 7）
- $R_{\mathrm{logic}}$：奖励逻辑严谨与因果推理关键词（如 "because", "leads to", "if-then"，完整列表见 Table 8）
- $R_{\mathrm{domain}}$：奖励领域知识整合关键词（如 "frequency", "pitch", "tempo"，完整列表见 Table 9）

消融实验表明：移除关键词奖励使准确率进一步降至 75.20%，表明结构化逻辑和领域术语激励对有效分析策略至关重要。

**过度思考惩罚**对推理长度施加线性惩罚，鼓励模型在适当深度停止，避免冗余和幻觉：

$$R_{\mathrm{overthinking\ penalty}}(s_i) = 1 - \frac{|t_i|}{L_{\mathrm{max\_output}}}$$

其中最大输出长度 $L_{\mathrm{max\_output}} = 256$。该惩罚是发现“推理甜点”（reasoning sweet spot）的核心机制——移除后推理与非推理模式的性能差距从 3.4 个百分点缩小至 1.5 个百分点，表明模型失去了对推理深度必要性的校准能力（Table 6/Table 21）。

### 3.3 在线强化学习训练

CESAR 采用 Group Relative Policy Optimization (GRPO) 结合多面过程奖励进行在线训练。对每个训练样本采样 $K=8$ 个回复，计算相对优势后更新策略，并加入 KL 正则化以稳定训练：

$$\mathcal{L}_{\mathrm{GRPO}} = \mathcal{L}_{PG}^{\mathrm{multi\text{-}faceted}} + \beta \cdot \mathcal{L}_{KL}$$

训练流程（Algorithm 1）包含三个关键模块：

1. **数据增强模块**：对训练问题进行答案不变的模板变换，生成多种语言变体以扩展训练集（详见 Appendix B.3）
2. **GRPO 在线训练循环**：采样每个样本的多个回复，计算相对优势，更新策略
3. **多面奖励计算器**（Algorithm 2）：计算准确性、格式、一致性、关键词和过度思考惩罚的加权总奖励

训练在 AVQA 增强数据集上进行，使用 8×H200 GPU，耗时 61.44 小时。

### 3.4 测试时规模控制

CESAR 通过控制最大思考长度 $L_{\mathrm{max.think}}$ 实现测试时推理深度的可控调节。定义性能函数：

$$P(L_{\mathrm{max.think}}) = \mathbb{E}[\mathbb{I}[\hat{y} = y] \mid |t| \leq L_{\mathrm{max.think}}]$$

推理甜点定义为使性能最大化的最优思考长度：

$$L_{\mathrm{sweet}} = \arg\max_L P(L)$$

线性回归模型 $P(L) = P(0) + \beta \cdot L$ 量化推理对性能的影响方向与程度。基础模型呈现 $\beta = -0.51$ 的负斜率（测试时逆规模），而 CESAR 实现 $\beta = +0.038$ 的正斜率，完成从负向到正向的完全逆转（Figure 8/Appendix D.12）。

## 实验与关键发现

### 核心瓶颈：测试时逆规模现象

我们在MMAU Test-mini基准上首先验证了基础模型 **Qwen2.5-Omni-7B**（Xu et al., 2025）的推理行为。关键发现是：当该模型被要求生成显式推理链时，其性能**不升反降**——从无推理模式下的68.60%骤降至推理模式下的65.20%（Table 1 / Table 18）。这一现象即为**测试时逆规模（test-time inverse scaling）**：推理链越长，准确率越低。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_DUr48hxO2h/figures/002_Table_1.jpg]]
*Table 1: MMAU Test-Mini benchmark results. Blue indicates best performance, green indicates second-best. Accuracy (%) is reported across audio modalities. OP means overthinking penalty. See App. D.4 for details*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_DUr48hxO2h/figures/022_Table_18.jpg]]
*Table 18: MMAU Test-mini Benchmark Results. We evaluate our method against state-of-the-art proprietary and open-source audio models. Best scores are highlighted in blue , second-best scores in green . Accuracy (%) is reported. We report the performance of Qwen2.5-Omni-7B (Xu et al., 2025) and Ke-Omni-R (Zhao et al., 2025) from our own reproductions under the same protocol; all other baseline results are taken from the MMAU paper (Sakshi et al., 2025)*

线性回归分析（Figure 8 / Appendix D.12）量化了这一退化趋势：基础模型的规模斜率 $\beta = -0.51$，表明每增加一个推理token，准确率平均下降0.51个百分点。这揭示了一个根本性瓶颈：仅以最终答案正确性为监督信号（如RLVR），模型学到的是“为推理而推理”的表面模式，而非真正的分析能力——推理过程充斥着幻觉、逻辑断裂、推理-答案不一致等问题。

### 主实验结果

#### MMAU Test-mini

CESAR在启用推理后达到 **77.10%** 的总准确率（Table 1 / Table 18），显著超越所有对比方法：基于结果奖励的RL基线 **Ke-Omni-R**（Zhao et al., 2025）为74.60%（+2.5点），领先商业模型 **GPT-4o Audio**（Hurst et al., 2024）和 **Gemini 2.5 Pro**（Comanici & et al., 2025）。更重要的是，CESAR完全逆转了测试时逆规模——其规模斜率变为 $\beta = +0.038$（Figure 8），实现了从负向到正向的推理规模化。

任务级雷达图（Figure 2）进一步显示，CESAR在大多数子任务上实现了归一化性能的全面领先，尤其在需要深层推理的复杂任务上优势更为明显。

#### MMSU

在MMSU基准上（Table 2 / Table 19），CESAR以 **64.24%** 的总准确率超越Ke-Omni-R（62.08%），并在推理子任务上逼近人类水平。然而，感知任务的平均准确率仅为48.45%，远低于人类的91.24%，暴露出**感知瓶颈**——模型的基础听觉理解能力仍是制约整体性能的短板。

#### MMAU-Pro

在更具挑战性的MMAU-Pro基准上（Table 3 / Table 10），CESAR以 **56.4%** 的平均准确率位居7B参数规模模型之首，超过Ke-Omni-R（54.5%）和基础模型（49.1%）。在12个音频理解类别中，CESAR在多数类别上取得最佳或次佳成绩，进一步验证了过程奖励在复杂推理场景下的泛化能力。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_DUr48hxO2h/figures/005_Table_3.jpg]]
*Table 3: Performance on the MMAU-Pro Benchmark (Kumar et al., 2025). We compare CESAR against key baselines and SOTA models. Best scores are highlighted in blue , second-best scores in green . All values are accuracy (%) and rounded to one decimal place (same as MMAU Pro paper). See App. D.1 for more results*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_DUr48hxO2h/figures/014_Table_10.jpg]]
*Table 10: Performance on the MMAU-Pro Benchmark. Best scores are highlighted in blue , second-best scores in green . All values are accuracy (%). All results show accuracy (%). Human performance is included as an upper bound reference. We report the performance of Ke-Omni-R (Zhao et al., 2025) and Qwen2.5-Omni-7B (Xu et al., 2025) from our own reproductions under the same protocol; all other baseline results are taken from the MMAU Pro paper (Kumar et al., 2025)*

#### MMAR

在混合音频推理基准MMAR上（Table 22），CESAR达到 **62.70%** 的总准确率，超越Ke-Omni-R（60.90%）。值得注意的是，在涉及多声源混合的场景（如Sound+Music+Speech），所有模型的表现均显著下降，表明对重叠声源的组合理解仍是开放难题。

### 测试时规模分析：推理甜点的发现

Figure 3（左）展示了通过扫描最大思考长度（0到250 tokens，步长25）获得的测试时规模曲线。基础模型呈现灾难性的性能崩溃——推理链越长，准确率越低。相比之下，所有经过RL训练的模型均保持鲁棒。

CESAR完整方法（含过度思考惩罚）展现出卓越的校准能力：它在推理链约35-40 tokens处发现了一个**推理甜点（reasoning sweet spot）**，以更短的推理链达到77.1%的峰值准确率。而去除过度思考惩罚的变体虽然也能维持正向规模，但其性能峰值更低且需要更长的推理链。这证明过度思考惩罚不仅抑制了冗余推理，更帮助模型学会了**何时需要深度推理、何时可以简洁作答**的元认知能力。

### 推理质量评估：AI-as-Judge与人工评估

仅凭准确率无法完全刻画推理质量。我们采用两种补充评估：

**AI-as-Judge**（Figure 3右 / Figure 7）：以GPT-4o Audio作为评判者，对推理过程进行头对头比较。CESAR对基础模型的胜率占据压倒性优势，对Ke-Omni-R也取得显著胜率。这提供了超越准确率的定量证据，表明过程奖励培养的推理质量在一致性、逻辑性和信息量上均优于结果奖励。

**人工评估**（Table 4 / Table 11 / Table 12）：基于MMAU Test-mini的1000个样本，3位专家标注者进行超过3000次独立判断（多数投票协议）。CESAR对基础模型的总体胜率为 **88.60%**，对Ke-Omni-R为 **63.10%**。后者尤为关键——它提供了人类背书的确凿证据：过程导向奖励相比仅奖励最终结果，确实培养了更优质、更可信的推理能力。在音乐、声音、语音三个音频领域，CESAR均保持一致的胜率优势。

### 消融实验：各组件的因果贡献

渐进消融研究（Table 6 / Table 21）从完整CESAR出发，逐步移除各组件以量化其独立贡献：

1. **移除RL后训练**：推理准确率从74.60%骤降至65.20%，确认了GRPO训练的核心作用。
2. **移除一致性奖励**：总准确率从77.10%降至76.20%（-0.9点），且定性分析显示推理与答案脱节现象重新出现。
3. **移除关键词奖励**：进一步降至75.20%（累计-1.9点），表明结构化分析模式、逻辑推导和领域术语的显式激励对培养有效推理策略不可或缺。
4. **移除过度思考惩罚**：推理与非推理模式的性能差距从3.4点缩小至1.5点，证实该惩罚是模型识别推理必要性的关键信号。

每个组件的移除均导致统计显著的性能退化，验证了多面过程奖励中**各维度均为必要且互补**。

### 定性分析：推理过程的质变

Table 5展示了CESAR与基线模型在推理过程上的定性对比。基础模型的推理常出现逻辑跳跃、与答案矛盾、或包含无关信息。Ke-Omni-R虽然有所改善，但仍存在推理-答案不一致的案例。CESAR的推理过程则展现出**一致、结构化**的特征：推理内容与最终答案和问题上下文保持语义对齐，呈现出清晰的分析模式（如“首先分析...然后比较...因此选择...”），且推理深度与问题复杂度相匹配。

### 训练稳定性

训练曲线（Figure 9）显示，CESAR的训练准确率随步数呈现稳定上升趋势，未出现明显的性能震荡或退化。GRPO的KL正则化机制和在线采样策略共同保障了训练的稳定性。

### 公平性说明

需注意以下限定条件：
- 训练计算开销较大：在AVQA增强数据集上使用8×H200 GPU训练需61.44小时。
- 奖励权重经过调优（$\alpha_1=5.0$，$\alpha_2$至$\alpha_5=1.0$），不同配置会带来性能变化，但整体框架具有一定鲁棒性（Table 23）。
- 部分商业模型（如GPT-4o Audio、Gemini 2.5 Pro）的内部推理细节不完全公开，比较存在一定不确定性。
- 所有报告分数均使用固定协议和自复现基线，但MMAU-Pro等基准的官方评估协议与本文可能存在细微差异。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_DUr48hxO2h/figures/027_Figure_6.jpg]]
*Figure 6: Test-Time Scaling Curves of Reasoning. Accuracy is plotted against the average length of the reasoning chain (in used tokens). (Top Row) The full comparison reveals a catastrophic performance collapse of the base Qwen2.5-Omni-7B model as it generates longer reasoning chains, empirically demonstrating the test-time inverse scaling problem. In contrast, all RL-trained models remain robust. (Bottom Row) A zoomed-in view of the RL models highlights the performance peak of our full method (i.e., CESAR (Ours)), which discovers a “reasoning sweet spot”. It consistently outperforms both the version without the Overthinking Penalty reward (i.e., CESAR (Ours w/o Overthinking Penalty)) and the Ke-Omni...*

## 定位与知识库关联

### 1. 与基线方法的关系

**CESAR** 的核心定位是对现有音频LLM推理训练范式的系统性补全，而非颠覆性重构。其与关键基线的关系可从三个维度理解：

**基础模型层：Qwen2.5-Omni-7B**（Xu et al., 2025）
该模型作为所有RL训练的起点，其原始行为揭示了本文的核心问题——**测试时逆规模现象**（test-time inverse scaling）。当直接要求该模型生成推理链时，准确率反而从68.60%降至65.20%（Table 1），推理链越长性能越差。线性回归分析给出负向规模斜率 $\beta = -0.51$（Figure 8），表明该模型学到的推理模式存在系统性缺陷：推理过程与答案脱节、逻辑混乱、幻觉频发。CESAR 将这一现象诊断为“仅以最终答案为监督信号”的必然结果——模型学会了生成看似合理的推理文本，却未习得真正的分析能力。

**结果奖励基线：Ke-Omni-R**（Zhao et al., 2025）
Ke-Omni-R 采用基于结果验证的RLVR范式，仅奖励答案正确性与格式合规，代表了当前音频推理训练的主流思路。其在MMAU Test-mini上达到74.60%的准确率，显著优于基础模型，证明RL训练本身确有价值。然而，CESAR 在此基础上进一步提升了2.5个百分点至77.10%（Table 1），且人工评估中以63.10%的胜率显著优于Ke-Omni-R（Table 4）。这一差距的关键在于：结果奖励能纠正部分错误，但无法阻止模型习得“推理-答案不一致”的捷径——即推理过程指向错误结论却恰好猜对答案。CESAR 通过一致性奖励 $R_{\mathrm{consistency}}$ 显式约束推理与答案的对齐关系，从机制上阻断了这一漏洞。

**商业闭源模型：GPT-4o Audio**（Hurst et al., 2024）与 **Gemini 2.5 Pro**（Comanici & et al., 2025）
CESAR 在MMAU Test-mini上以77.10%超越GPT-4o Audio（76.40%）和Gemini 2.5 Pro（75.30%），在MMAU-Pro上也以56.4%的平均准确率位居所有7B模型之首（Table 3）。但需注意，这些商业模型的内部推理机制不完全公开，且可能受益于更大规模的训练数据和模型参数量，比较存在一定的不确定性。

### 2. 方法适用边界

**已验证的适用范围：**
- **任务类型**：音频理解与推理，涵盖声音事件分析、音乐理解、语音内容推理等多模态音频任务。在MMAU Test-mini、MMSU、MMAU-Pro、MMAR四个基准上均取得一致提升。
- **模型架构**：基于Qwen2.5-Omni-7B的音频LLM架构，使用GRPO在线训练框架。
- **推理模式**：同时提升“带推理”和“不带推理”两种模式的性能，表明过程奖励训练具有跨推理模式的泛化增益。

**已知局限与未验证边界：**
1. **感知能力瓶颈**：MMSU感知任务中模型平均准确率仅为48.45%，远低于人类的91.24%。过程奖励主要塑造推理质量，对底层声学感知能力的提升有限。这暗示该方法需要与感知能力的专项训练结合，才能实现全面的类人音频理解。
2. **混合音频流的组合理解**：多个重叠声源（如背景音乐+前景语音+环境音效）的推理仍是开放难题，论文未报告在此类场景上的专门评估。
3. **跨模态迁移**：方法论局限于音频领域，尚未在视觉、文本或机器人等任务上验证其通用性。过程奖励的核心思想——显式激励推理过程的一致性、结构化和适当深度——在理论上具有跨模态可迁移性，但实际效果需进一步验证。
4. **训练数据依赖**：所有RL训练仅基于AVQA数据集（经模板增强），模型在分布外音频场景（如长对话、实时交互、开放域问答）中的推理鲁棒性尚未评估。

### 3. 核心局限与开放问题

**计算开销：**
GRPO在线训练需为每个样本采样 $K=8$ 个回复，在8×H200 GPU上训练增强后的AVQA数据集耗时61.44小时。这一计算负担限制了方法在更大规模数据或更大模型上的快速迭代。可能的缓解方向包括：采样策略优化（减少 $K$ 值）、模型蒸馏、或离线过程奖励预训练。

**奖励权重的敏感性：**
准确性奖励权重 $\alpha_1$ 对性能有明显影响（Table 23），各权重需归一化至 $[0,1]$ 范围才能稳定工作。虽然整体框架对权重配置具有一定鲁棒性，但最优配置可能因数据集和模型规模而异，需要额外的调优成本。

**推理甜点的稳定性：**
论文发现模型存在“推理甜点”（reasoning sweet spot）——即最优的推理链长度。CESAR通过过度思考惩罚 $R_{\mathrm{overthinking\ penalty}}$ 帮助模型发现这一甜点，但该甜点是否在不同数据集、模型规模或训练阶段保持稳定，能否通过理论推导预测，仍是开放问题。

**开放研究方向：**
- 如何设计类似的过程导向奖励来突破感知能力瓶颈？感知任务可能需要不同于推理任务的奖励结构。
- 本文的多面过程奖励框架能否迁移至视觉、文本等领域的推理训练？跨模态的奖励设计空间有何异同？
- 能否通过理论分析预测最优推理深度，而非依赖经验性的测试时规模扫描？
- 模型在真实开放场景（如长对话、实时交互）中的推理鲁棒性如何？过程奖励训练是否会引入新的失败模式？

## 原文 PDF

![[paperPDFs/ICLR_2026/Incentivizing_Consistent_Effective_and_Scalable_Reasoning_Capability_in_Audio_LLMs_via_Reasoning_Process_Rewards.pdf]]
