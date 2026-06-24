---
title: "Video-STAR: Reinforcing Open-Vocabulary Action Recognition with Tools"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Video_STAR_Reinforcing_Open_Vocabulary_Action_Recognition_with_Tools.pdf
aliases:
- VS
- Video-STAR
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "上下文子动作分解（将整体动作拆解为具有区分性的子动作原语）与工具增强的强化学习（动态调用姿态估计、人体检测等工具）协同作用，强制模型将推理建立在外部工具提取的视觉事实上，从而纠正文本驱动的推理偏差。"
primary_logic: "将动作识别重新定义为顺序决策过程：先分解动作，再匹配候选，最后通过层次化奖励加权子动作重要性进行评分，使模型从以文本为中心转向以视觉为基础的推理。"
claims:
- "Video-STAR-7B 在 base-to-novel 设置下的 Kinetics-400 上取得了 96.7% 的谐波均值（HM），超过先前最佳方法 26.3 个百分点。"
- "移除强化学习组件后，UCF-101 准确率从 96.7% 骤降至 76.8%，降幅高达 19.9 个百分点，证明强化学习是驱动工具使用和性能提升的核心因素。"
- "与静态调用全部工具的流水线相比，Video-STAR 的智能体系统在保持相近准确率（96.7% vs 97.2%）的同时，总推理时间减少 22%，工具调用时间减少 36%，实现了更优的成本效益。"
- "当将 YOLO 11 换为 OpenPose 或 Qwen 换为 Gemini‑1.5‑Pro 后，UCF 准确率依然高达 96.1% 与 97.4%，揭示了核心创新在于智能体逻辑而非特定工具栈。"
---

# Video-STAR: Reinforcing Open-Vocabulary Action Recognition with Tools

> [!tip] 核心洞察
> 将动作识别重新定义为顺序决策过程：先分解动作，再匹配候选，最后通过层次化奖励加权子动作重要性进行评分，使模型从以文本为中心转向以视觉为基础的推理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Video-STAR: 通过工具增强开放词汇动作识别 |
| 英文题名 | Video-STAR: Reinforcing Open-Vocabulary Action Recognition with Tools |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=NBOHB6aYZh) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Video-STAR |
| Dataset | Kinetics-400 (base-to-novel), UCF-101 (full, cross-dataset), Kinetics-600 (split |

> [!tip] 效果简介
> - Kinetics-400 (base-to-novel) 上，Harmonic Mean (HM) 为 96.7，对比 70.4 (Open-MeDe)，变化 +26.3。
> - UCF-101 (full, cross-dataset) 上，Top1-Acc 为 99.4，对比 98.3 (Open-MeDe)，变化 +1.1。
> - Kinetics-600 (split, cross-dataset) 上，Top1-Acc 为 90.5，对比 71.3 (Open-MeDe)，变化 +19.2。

## 概述

现有多模态大语言模型（MLLM）在开放词汇动作识别中普遍采用以文本为中心的链式思维（CoT）推理，这一范式严重依赖语言先验，却忽视视频中的视觉事实，导致跨模态幻觉频发，并在语义相近或组成复杂的细粒度动作上表现出较差的区分能力。针对这一瓶颈，本文提出 **Video-STAR**，一种将动作识别重新构造为顺序决策过程的统一框架。其核心思想是：先对动作进行上下文化的子动作分解，获得具有判别力的运动原语；进而动态调用姿态估计、人体检测等外部工具，将推理锚定在工具提取的视觉/几何事实上；最后通过层次化奖励函数对工具使用效率、子动作相关性和推理结构一致性进行联合优化，迫使模型从文本驱动转向视觉基础的推理。

Video-STAR 在多个开放词汇动作识别基准上取得大幅领先：在 Kinetics‑400 的 base‑to‑novel 设置下，谐波均值（HM）达到 96.7%，超越此前最优方法 **26.3** 个百分点；在 UCF‑101 跨数据集评估中，Top‑1 准确率高达 99.4%。消融实验表明，移除强化学习模块后准确率骤降约 **20** 个百分点，验证了 RL 对驱动工具使用和性能提升的决定性作用；同时，工具互换实验证实，框架的核心创新在于智能体逻辑而非特定工具栈，模块化设计具有较强鲁棒性。在保持相近准确率的前提下，智能体系统相较静态调用全部工具的流水线降低了约 **22%** 的总推理时间，展现出良好的性能‑成本权衡。综上，Video‑STAR 通过 “分解‑增强‑优化” 的协同机制，为开放词汇动作识别提供了一种从文本幻觉中解脱、以视觉事实为根基的解决方案。

## 背景与动机

开放词汇动作识别要求模型在未见过的类别或跨数据集场景下准确识别视频动作，这对模型的视觉-语义对齐能力提出了极高要求。传统CLIP微调方法（如ActionCLIP、ViFi-CLIP、Open-VCLIP）依赖视觉编码器与文本编码器的联合适应，虽然在基类-新类别泛化上取得一定进展，但面对语义相似或细粒度动作时仍暴露出判别力不足的瓶颈。更关键的是，近期多模态大语言模型（MLLM）虽然凭借其广阔的世界知识展现出强大的视频理解潜力，但其推理范式存在一个被低估的结构性缺陷：**以文本为中心的链式思维（Chain-of-Thought, CoT）推理容易忽视视觉信号，导致跨模态幻觉**。即便MLLM能给出看似合理的文本解释，却可能完全误读视频中人物的实际动作（如将“转身”误判为“微笑”），这类错误在标准CoT模式下很难被自动纠正。

为缓解幻觉，现有工作尝试引入工具增强CoT——通过调用姿态估计、检测器等外部工具提取视觉证据来辅助推理。然而，这种策略尽管在一定程度上抑制了幻觉，却依然缺乏**类别特定的细粒度推理能力**。因为工具只是机械地提供额外信息，模型仍未学会如何针对具体动作类别分解出具有区分性的子步骤，导致在区分如“击高尔夫球”与“挥棒”这样的相似动作时仍表现不佳（Figure 1 a/b）。

因此，亟需一种能够**强制模型将推理建立在结构化视觉事实之上，并针对每个候选动作进行精细拆解对比**的新范式。本文的动机正是在此：通过引入**上下文子动作分解**，将整体动作解耦为按语义显著性排序的子运动原语（如从“转身”中识别出“肩部转动→头部转向→身体旋转”等关键子步骤），并动态调用人体检测、姿态估计、动作解释等工具，使模型在分解‑匹配‑评分的顺序决策过程中，必须基于工具返回的几何/语义证据进行逻辑推演，而非停留在表面的文本联想。进一步地，结合层次化强化学习优化工具调用效率与子动作权重，最终实现从以文本为中心到以视觉为基础的推理转变。一系列实验表明，这一思路能够显著提升开放词汇动作识别的精准度与跨场景鲁棒性，尤其在对细粒度动作的区分上，效果远超现有基线。

## 核心创新

现有开放词汇动作识别的核心瓶颈在于：多模态大语言模型（MLLMs）普遍依赖**文本中心的链式思维（CoT）**，推理时缺少来自视觉信号的结构化约束，因而对语义相似或运动模式相近的细粒度动作极易产生跨模态幻觉。Video‑STAR 通过三个连锁层面纠正这一偏差，将动作识别重新定义为**顺序决策过程**——先进行子动作分解，再动态调用外部工具获取视觉事实，最后在层次化奖励下完成候选匹配与评分，强迫模型将推理锚定在实际观测量上。

### 相对于基线的关键创新（Changed Slots）

| 设计维度 | 基线做法 | Video‑STAR 方案 | 证据 Anchor |
|----------|----------|-----------------|------------|
| **推理框架** | 文本 CoT 或简单的视觉特征匹配（如 ActionCLIP、ViFi‑CLIP、Open‑VCLIP 等 CLIP 变体） | **上下文子动作分解 + 工具增强视觉 CoT**，构成“分解 → 候选匹配 → 评分”的三段式推理链路 | Section 3.2, 3.4 |
| **工具集成与调用** | 不使用外部工具，或仅采用固定流水线式的帧缩放/裁剪 | **动态四类工具库**（人体检测、姿态估计、动作解释、视频描述），由策略模型根据查询内容按需调用，输出结构化视觉‑语义证据 | Section 3.1, Tool Library |
| **奖励机制** | 仅依据最终答案正确与否给出二元奖励 | **层次化奖励函数**：同时优化准确度、格式规范、工具调用效率以及按语义显著性排名的子动作权重；工具奖励与子动作奖励**仅在答案正确时激活**，防止策略作弊 | Section 3.4, Reward Design；Eq. (6) |

### 破解跨模态幻觉的因果机制

1. **子动作分解强制视觉锚定**  
   MLLMs 在 CoT 中容易忽略视频中的几何线索（例如将“转身”误判为“微笑”，Figure 4），原因是文本推理路径不受视觉事实约束。Video‑STAR 将整体动作解构为若干具有区分性的**子动作原语**（如“先下蹲，后曲臂，再跃起”），并在推理链中显式要求模型调用工具去验证这些原语。这一分解不仅为后续匹配提供了细粒度特征，而且将推理从开放文本生成转化为受控的视觉事实核对任务（Figure 1(c)）。

2. **工具增强 RL 纠正分布外推理**  
   仅靠监督微调（SFT）无法保证模型在测试时不变回文本中心的捷径推理。消融实验显示，**移除整个强化学习阶段会使 UCF‑101 准确率从 96.7% 骤降至 76.8%（‑19.9 pp）**（Table 3, w/o. RL），说明 RL 是迫使策略在推理时实际使用工具的核心推动器。GRPO 算法（Eq. 3）配合层次化奖励，既鼓励调用正确工具，又对生成格式和子动作质量施加结构化压力，从而将高维动作识别问题分解为可验证的步骤。

3. **智能体逻辑而非特定工具栈**  
   当把 YOLO 11 换为 OpenPose 或把 Qwen API 换成 Gemini‑1.5‑Pro 时，UCF 准确率依然维持在 96.1% 和 97.4%（Table 6），证明性能提升来源于**智能体决策逻辑**（何时调用哪类工具、如何整合输出、怎样加权子动作），而非某个孤立工具的能力。同时，与静态调用全部工具的流水线相比，Video‑STAR 在保持相近准确率（96.7% vs. 97.2%）的条件下，**总推理时间减少 22%，工具调用时间减少 36%**（Table 4），验证了动态工具选择的有效性。

### 创新点的协同效应：子动作权重与工具互补性

层次化奖励中对子动作使用排名权重 $w_k = n - k + 1$（越显著的子动作权重越高）并非孤立设计，它与工具输出形成互补。消融实验表明：  
- 将排名权重替换为等权重，UCF‑101 / HMDB‑51 / K‑600 分别下降 2.5 / 3.8 / 4.8 pp（Table 7, row d）；  
- 移除姿态估计工具，三数据集分别下跌 3.9 / 5.0 / 6.8 pp（Table 7, row h）；  
- 两处削弱叠加影响更大，说明**工具提供的几何事实是子动作权重合理分配的前提**，而子动作分解则为工具输出提供了语义解释框架。

Video‑STAR 的创新本质上是**将开放词汇动作识别的推理从“问-答”模式升级为“观察-分解-验证-决策”的自主式流程**，使 MLLM 从被动的文本联想者转变为主动的视觉事实整合者。这一转变在 base‑to‑novel 设置下带来了 Kinetics‑400 上 96.7% 的谐波均值，相较先前最佳方法提升 26.3 个百分点（Table 1），且模型仅在 HMDB‑51 子集上微调后即可零样本泛化至多个数据集（Table 2），佐证了框架对 visual grounding 能力的根本性修复。

## 整体框架

![[assets/figures/papers/iclr26_0016_NBOHB6aYZh_Video-STAR_Reinforcing_Open-Vocabulary_Action_Re/figures/002_Figure_1.jpg]]
*Figure 1: Key insight of Video-STAR. (a) MLLMs + CoT is prone to hallucinations due to overreliance on text-centric reasoning while ignoring visual cues. (b) MLLMs + Tool-Augmented CoT mitigates hallucinations by integrating domain-specific tools to extract visual information. However, both (a) and (b) lack category-specific reasoning capabilities and struggle to distinguish semantically similar or complex actions. (c) Video-STAR enhances reasoning capacity by introducing contextual sub-motion decomposition, which disentangles actions into discriminative motion primitives. This enables fine-grained action discrimination and robust performance in open-vocabulary scenarios*

![[assets/figures/papers/iclr26_0016_NBOHB6aYZh_Video-STAR_Reinforcing_Open-Vocabulary_Action_Re/figures/003_Figure_2.jpg]]
*Figure 2: Pipeline of Video-STAR. (i) Introduce a three-stage sub-motion logic chain to construct tool-augmented reasoning data that decomposes actions into discriminative sub-motions. (ii) Pretrain the MLLMs on structured reasoning chains and fine-tune it for domain-specific adaptation. (iii) Adopt the GRPO algorithm for reinforcement learning, which optimizes a hierarchical reward function considering both tool-usage and sub-motion to ensure robust and consistent inference*

Video-STAR 将开放词汇动作识别重塑为**工具增强的顺序决策过程**，其整体流水线围绕三个核心环节构建：上下文子动作分解、动态工具调用与集成，以及层次化奖励驱动的强化学习。系统输入为视频 $V$ 和包含候选动作的文本查询 $Q$，最终输出动作类别 $A$，中间的推理过程被显式建模为两阶段智能体行为。

### 训练数据构建

为了给模型提供结构化的工具使用和推理能力，Video-STAR 首先通过**三阶段子动作逻辑链**自动合成训练数据。该流程将每个动作拆解为一组具有区分性的子动作原语，并调用领域专用工具（人体检测、姿态估计、动作解释、视频描述）获取的多模态证据，形成⟨子动作分解→工具证据→最终判定⟩的思维链样本。生成的样本再经由专家模型进行质量过滤，剔除推理不一致的条目，确保数据可靠且逻辑连贯。

### 训练阶段

训练分为**智能体监督微调（Agentic SFT）**和**智能体强化学习（Agentic RL）**两个阶段。SFT 阶段在构造的多模态思维链数据上对基础 MLLM 进行冷启动微调，使其学会按预定模板生成工具调用命令和子动作分析步骤，损失函数为负对数似然：
$$\mathcal{L}_{\mathrm{SFT}} = - \mathbb{E}_{\mathcal{T} \sim \mathcal{D}} \left[ \sum_{t=1}^{T} \log p_{\theta}(s_{t} \mid \mathcal{X}, \mathcal{T}, s_{< t}) \right]$$

RL 阶段则采用**群组相对策略优化（GRPO）**进一步强化策略，目标函数为：
$$\mathcal{L}_{\mathrm{GRPO}}(\theta) = - \mathbb{E}_{q,\{o_i\}} \frac{1}{G} \sum_{i=1}^{G} \left( \min\left(\frac{\pi_{\theta}(o_i|q)}{\pi_{\theta_{old}}(o_i|q)} A_i, \operatorname{clip}\left(\frac{\pi_{\theta}(o_i|q)}{\pi_{\theta_{old}}(o_i|q)}, 1-\epsilon, 1+\epsilon\right) A_i \right) - \beta \mathbb{D}_{KL}(\pi_{\theta} || \pi_{ref}) \right)$$
其中优势 $A_i$ 由群组内奖励的标准化得到。优化信号由**层次化奖励函数**提供：
$$R(\tau) = R_{\mathrm{acc}}(\tau) + R_{\mathrm{format}}(\tau) + \mathbb{I}_{R_{\mathrm{acc}}(\tau) > 0} \cdot \left( R_{\mathrm{tool}}(\tau) + R_{\mathrm{sub}}(\tau) \right)$$
该奖励仅在答案正确时激活工具使用效率和子动作相关性项，迫使模型在得到正确答案的前提下，尽可能高效、精准地调用工具并关注语义最显著的子动作。子动作权重按语义重要性排序，第 $k$ 重要的子动作获得系数 $w_k = n - k + 1$，从而引导策略对区分性更强的运动原语分配更多注意力。

### 推理阶段与工具库

推理时，Video-STAR 以**两阶段智能体**方式运作。第一阶段根据当前视频的模态特性，从工具库 $\mathcal{T} = \{T_{\mathrm{p}}, T_{\mathrm{d}}, T_{\mathrm{a}}, T_{\mathrm{v}}\}$ 中动态选择最相关的工具。工具库封装了 YOLO 11 提供的人体检测与姿态估计，以及 Qwen API 提供的动作解释和视频描述，为智能体提供即插即用的结构化视觉-语义增强。第二阶段整合工具输出的视觉特征 $F$（以拼接形式）和文本解释 $E$（以追加形式），与原始视频和查询一起送入策略网络，输出最终动作预测：
$$A \sim \pi_{\theta}( \cdot | V \oplus F, Q \oplus E ; \mathcal{T} )$$

该两阶段机制相比传统静态流水线显著减少了冗余工具调用：实验表明，Video-STAR‑3B 在保持相近准确率（96.7% vs 97.2%）的同时，总时间降低 22%，工具调用时间降低 36%，实现了更优的推理效率。

### 模块协同关系

上下文子动作分解为两阶段推理提供了类别特定的区分性线索，工具库提供了可验证的视觉事实，层次化奖励则保障了 RL 阶段对工具使用效率与子动作重要性的联合优化。三者协同作用，将推理从文本中心转向视觉基础，从而有效抑制跨模态幻觉，并提升对语义相似或复杂动作的识别精度。SFT 步骤作为冷启动为 RL 提供了结构化先验，移除 RL 会致使 UCF‑101 准确率从 96.7% 骤降至 76.8%（降幅 19.9 个百分点），而 SFT 若不使用工具增强数据也会带来约 10 个百分点的性能损失，进一步印证了每个模块的不可替代性。

## 核心模块与公式推导

**整体推理流程**
Video‑STAR 将开放词汇动作识别形式化为顺序决策过程。给定输入视频 $V$ 和动作查询 $Q$，模型在工具集 $T = \{T_{\text{p}}, T_{\text{d}}, T_{\text{a}}, T_{\text{v}}\}$ 中动态选择工具，通过两阶段推理实现“子动作分解 → 候选匹配 → 加权评分”的视觉基础链式思维。最终动作预测由公式 (1) 给出：

$$
A \sim \pi_{\theta}(\cdot \mid V \oplus F, Q \oplus E ; T) \tag{1}
$$

**公式变量含义**：
- $V$：原始视频的视觉特征；
- $F$：工具调用后产生的视觉特征（如人体检测框、姿态关键点），以通道或空间维度与 $V$ 拼接（$\oplus$）；
- $Q$：文本形式的动作类别查询；
- $E$：工具生成的结构化文本解释（如动作语义描述、视频帧描述），以追加形式（$\oplus$）嵌入到查询中；
- $T$：可供模型选择的工具集合；
- $\pi_{\theta}$：参数化策略，输出动作类别 $A$。

**关键模块及其公式推导**

### 1. 工具库（Tool Library）

工具库封装了四个即插即用的工具，为智能体提供结构化的视觉‑语义证据：

- $T_{\text{d}}$（人体检测）：基于 YOLO 11，输出人员的边界框；
- $T_{\text{p}}$（姿态估计）：基于 YOLO 11，输出骨骼关键点；
- $T_{\text{a}}$（动作解释）：通过 Qwen API 在线检索动作类别的自然语言解释；
- $T_{\text{v}}$（视频描述）：通过 Qwen API 生成关键帧的密集自然语言描述。

工具的输出被编码为视觉特征 $F$（检测框、姿态）和文本解释 $E$（动作定义、帧描述），分别以拼接和追加的方式注入预测模型 (Eq. 1)。这种设计将模型的推理依据从文本先验转移到由外部工具提取的几何事实上，从而抑制跨模态幻觉。

### 2. 训练数据构建与智能体监督微调（Agentic SFT）

训练数据由三阶段子动作逻辑链合成：首先将动作分解为可区分的子动作原语，再为每个原语匹配候选，最后通过排序加权得到类别评分。该过程利用大型教师模型生成多模态思维链，并经过专家模型过滤剔除不一致的推理样本，确保逻辑一致性。

在构建的数据上，对基础多模态大语言模型进行冷启动监督微调，目标函数为负对数似然：

$$
\mathcal{L}_{\text{SFT}} = - \mathbb{E}_{\mathcal{T} \sim \mathcal{D}} \left[ \sum_{t=1}^{T} \log p_{\theta}(s_{t} \mid \mathcal{X}, \mathcal{T}, s_{< t}) \right] \tag{2}
$$

**公式变量含义**：
- $\mathcal{D}$：合成的工具增强推理数据分布；
- $\mathcal{T}$：从数据集中采样的一条完整推理轨迹；
- $T$：该轨迹的总步数（子动作分解、工具调用、候选匹配等步骤）；
- $\mathcal{X}$：输入的视频‑查询对；
- $s_t$：第 $t$ 步的输出 token；
- $s_{<t}$：前 $t-1$ 步的上下文。

SFT 阶段为后续强化学习提供了结构化的推理模板和初步的工具调用能力，防止 RL 探索阶段出现工具退化。

### 3. 智能体强化学习与层次化奖励（Agentic RL）

RL 阶段采用 **群组相对策略优化（GRPO）** 算法，目标函数为：

$$
\mathcal{L}_{\text{GRPO}}(\theta) = - \mathbb{E}_{q, \{o_i\}} \frac{1}{G} \sum_{i=1}^{G} \left( \min\left( \frac{\pi_{\theta}(o_i \mid q)}{\pi_{\theta_{\text{old}}}(o_i \mid q)} A_i,\; \operatorname{clip}\left( \frac{\pi_{\theta}(o_i \mid q)}{\pi_{\theta_{\text{old}}}(o_i \mid q)}, 1-\epsilon, 1+\epsilon \right) A_i \right) - \beta \, \mathbb{D}_{\text{KL}}(\pi_{\theta} \,\|\, \pi_{\text{ref}}) \right) \tag{3}
$$

**公式变量含义**：
- $q$：输入查询（视频和动作类别提示）；
- $\{o_i\}$：针对同一 $q$ 采样的 $G$ 条候选输出轨迹；
- $\pi_{\theta}$ / $\pi_{\theta_{\text{old}}}$：当前 / 旧策略；
- $A_i$：第 $i$ 条轨迹的优势估计（见 Eq. 5）；
- $\epsilon$：重要性采样比率裁剪阈值；
- $\beta$：KL 散度惩罚系数，防止策略偏离参考模型 $\pi_{\text{ref}}$。

优势估计量通过群组内归一化计算：

$$
A_i = \frac{r_i - \operatorname{mean}(\{r_1, \dots, r_G\})}{\operatorname{std}(\{r_1, \dots, r_G\})} \tag{5}
$$

其中 $r_i = R(\tau_i)$ 为轨迹 $\tau_i$ 的总奖励，由层次化奖励函数 (Eq. 6) 计算。

**层次化奖励函数**由四个分量组成，且工具和子动作奖励仅当最终动作分类正确时激活：

$$
R(\tau) = R_{\text{acc}}(\tau) + R_{\text{format}}(\tau) + \mathbb{I}_{R_{\text{acc}}(\tau) > 0} \cdot \big( R_{\text{tool}}(\tau) + R_{\text{sub}}(\tau) \big) \tag{6}
$$

**各项含义**：
- $R_{\text{acc}}$：分类准确度奖励（如匹配正确为 1，否则 0）；
- $R_{\text{format}}$：输出格式规范性奖励；
- $R_{\text{tool}}$：工具调用效率奖励，奖励合理、精简的调用行为；
- $R_{\text{sub}}$：子动作相关性奖励，基于分解的子动作与标准模板的语义匹配度计算；
- 指示函数 $\mathbb{I}_{R_{\text{acc}} > 0}$：确保工具和子动作奖励仅在答案正确时生效，防止模型投机优化表面特征。

**子动作权重** 进一步按照语义显著性加权，使模型优先关注最具区分性的运动原语：

$$
w_k = n - k + 1 \tag{权重定义}
$$

**变量含义**：
- $n$：分解出的子动作总数；
- $k \in \{1, \dots, n\}$：子动作按语义重要性从高到低的排序位置（$k=1$ 为最重要）；
- $w_k$：赋予第 $k$ 个子动作的奖励权重。最重要的子动作获得权重 $n$，最不重要的获得权重 $1$，从而在优化时放大关键运动原语的影响。

这组公式共同驱动模型在自主调用工具时兼顾准确度与效率，并以自动化方式聚焦于决定动作类别的关键视觉线索，而非依赖文本先验进行无差别的子动作处理。实验证据（Table 3）显示，移除整个 RL 阶段会导致 UCF‑101 准确率从 96.7% 骤降至 76.8%，验证了该强化学习框架是驱动工具使用和性能提升的核心因素。

## 实验与分析

Video-STAR 在两个标准的开放词汇动作识别设定下进行验证：(1) **base-to-novel** 泛化，评估模型识别训练集中未见过的新类别动作的能力；(2) **cross-dataset** 零样本迁移，检验模型在不同数据集间的泛化能力。所有模型 **仅在 HMDB-51 的高频动作子集上进行微调**，之后以零样本方式在 Kinetics-400 (K-400)、UCF-101 和 Something-Something V2 (SSv2) 等数据集上评估，充分反映了方法的实际泛化边界。

### 主结果与分析

在 **base-to-novel** 设定下（Table 1），Video-STAR-7B 取得了 **96.7% 的谐波均值（HM）**，比先前最优的 Open-MeDe（70.4%）高出 **26.3 个百分点**；在 UCF-101 上更是达到了 **99.7% 的 HM**。该结果验证了上下文子动作分解与工具增强推理的有效性——传统 CLIP 基方法在语义相似或细粒度动作上极易混淆，而 Video-STAR 通过动态调用姿态估计、人体检测等工具提取几何视觉证据，从根本上 **将推理锚定在视频内容而非文本先验**上，从而显著抑制了跨模态幻觉。
在 **cross-dataset** 设定（Table 2）中，Video-STAR-7B 在 UCF-101 上达到 **99.4% Top-1 准确率**（全验证集），在更具挑战性的 Kinetics-600 上提升至 **98.2%**，比 Open-MeDe 高出近 27 个百分点。即便是 3B 参数量的 Video-STAR-3B，也在 K-600 上取得 **90.5%** 的成绩，远超同参数量的通用视觉语言模型 Qwen2.5-VL-3B（37.7%）。这表明 Video-STAR 的核心增益并非单纯来自基础模型规模的扩大，而是来自 **推理范式的结构性改进**。

![[assets/figures/papers/iclr26_0016_NBOHB6aYZh_Video-STAR_Reinforcing_Open-Vocabulary_Action_Re/figures/005_Table_1.jpg]]
*Table 1: Performance comparison (Top1-Acc (%)) with the CLIP-based methods using ViT-B/16 under the base-to-novel setting. "HM" denotes the harmonic mean of the accuracy from the base and novel sets. Note that the best and second best performances are highlighted*

**定性案例**（Figure 4）显示，Qwen2.5-VL-3B 将 “turn” 误分类为 “smile”，而 Video-STAR-3B 借助姿态估计等工具的输出，准确捕捉到身体的旋转运动，从而做出正确判断。这直接印证了工具增强的视觉链式思维在抑制幻觉方面的作用。

### 关键组件消融

综合消融实验（Table 3, 7）揭示了各环节的因果贡献：

![[assets/figures/papers/iclr26_0016_NBOHB6aYZh_Video-STAR_Reinforcing_Open-Vocabulary_Action_Re/figures/008_Table_3.jpg]]
*Table 3: Ablation of key components in Video-STAR under cross-dataset setting. "Split" denotes evaluating across three validation splits. The best and second best performances are highlighted*

1. **强化学习（RL）是性能的核心推手**。移除整个 RL 阶段后，UCF-101 准确率从 **96.7% 骤降至 76.8%**（−19.9 个百分点），HMDB-51 和 K-600 也分别下跌 22.7 和 29.2 个百分点。GRPO 算法与层次化奖励函数（奖励工具调用效率、子动作语义权重，且仅在答案正确时激活）共同迫使模型学会何时以及如何高效调用工具，仅靠冷启动的监督微调（SFT）远不能实现这一能力。

2. **工具库与子动作分解相互补充**。移除工具使用（w/o. TOL）导致 UCF-101 下降约 9.6 个百分点；移除子动作分解（w/o. SUB）同样带来显著损失。二者同时去除，模型退化为近似纯文本推理基线。进一步，若 **用等权重替代按语义排序的子动作权重**（Table 7 row d），UCF-101、HMDB-51、K-600 分别下降 2.5、3.8、4.8 个百分点，证明对不同子动作赋予差异化重要性能够引导模型聚焦最判别的运动原语。

3. **姿态估计工具对细粒度动作分析不可或缺**。单独移除姿态估计工具（Table 7 row h）造成的损失最大（UCF-101: −3.9%，HMDB-51: −5.0%，K-600: −6.8%），说明位于动作识别中，人体的几何构型与关键点运动是最根本的视觉线索，缺失该信号会直接损害区分类似动作的能力。

4. **数据质量过滤至关重要**。去除数据评估步骤（Table 7 row c）导致三个数据集分别下降 1.9、3.0、3.9 个百分点，表明过滤不一致的思维链是保证工具增强推理逻辑一致性的必要条件。

### 效率与模块化分析

Video-STAR 的智能体系统通过动态选择工具实现了 **性能–效率** 的极佳平衡（Table 4）。相较于静态调用所有工具的流水线，智能体系统在 UCF-101 上保持相近准确率（**96.7% vs 97.2%**）的同时，总推理时间减少 **22%**（3.18 s vs 4.10 s），其中工具调用时间缩短 **36%**（1.43 s vs 2.24 s）。这说明智能体能够学习到哪些工具是冗余的，从而避免无效调用。计算开销方面（Table 5），Video-STAR-3B 相较于纯 Qwen2.5-VL-3B 仅增加 7,477 GFLOPS 和 2.39 秒延迟，却换来了近 **39 个百分点的准确率提升**，完全在可接受范围内。

![[assets/figures/papers/iclr26_0016_NBOHB6aYZh_Video-STAR_Reinforcing_Open-Vocabulary_Action_Re/figures/009_Table_4.jpg]]
*Table 4: Comparison between our agentic system and a static pipeline that adopts all tools*

框架的模块化通过工具互换实验得到验证（Table 6）。将 YOLO 11 替换为 OpenPose 后，UCF 准确率依然达到 **96.1%**；将 Qwen API 替换为 Gemini‑1.5‑Pro 则取得 **97.4%** 的更高成绩。这表明 **核心贡献在于智能体逻辑本身**，而非某一特定工具栈，系统具备良好的鲁棒性，可随工具技术迭代而获益。同时，用更强大的教师模型（Gemini‑1.5‑Pro）生成思维链数据（Table 8），还可额外带来约 **0.8 个百分点的提升**（UCF 97.5%），显示数据质量上界仍有提升空间。

![[assets/figures/papers/iclr26_0016_NBOHB6aYZh_Video-STAR_Reinforcing_Open-Vocabulary_Action_Re/figures/011_Table_6.jpg]]
*Table 6: Ablation on tool selection, demonstrating the framework’s modularity. Performance remains high when swapping core tools, proving the agentic logic is the key contribution*

### 局限性与未来方向

尽管 Video-STAR 取得了显著提升，但仍存在若干局限：(1) **工具调用引入额外延迟**，尤其是依赖大型 API 的动作解释和视频描述，工具时间约占端到端推理的 45%，对实时应用构成挑战；(2) **微调数据集覆盖有限**，仅在 HMDB-51 子集上训练，对于更长时序、多人交互或群体动作的泛化性尚未充分验证，可能在 Something-Something v2 等侧重时序因果的数据集上表现不如预期；(3) **外部工具依赖**，若姿态估计或检测模型在遮挡、暗光等困难场景下失效，其错误会传播至智能体的最终决策；(4) **工具库容量约束**，当前仅四类工具，未来可引入物体检测、场景图解析等更多视觉专家，但会进一步提升系统复杂性。后续工作可探索模型蒸馏与并行化以降低延迟，并验证该推理范式在视频问答、稠密视频描述等更广泛的视频理解任务上的适用性。

## 方法谱系与知识库定位

Video-STAR 处于基于 CLIP 的开放词汇动作识别方法与基于多模态大语言模型（MLLM）的通用视频理解路线之间，但通过**将动作识别重构为顺序决策过程**，开辟了一条“智能体 + 工具增强”的新范式。传统 CLIP 适应方法（如 ActionCLIP、ViFi-CLIP、ST-Adapter、Open-VCLIP）专注于视觉编码器的微调或权重插值，依赖静态特征匹配，缺乏对精细语义差异的显式推理能力（Table 1）。另一端的通用 MLLM（如 Qwen2.5-VL）虽能进行链式思维（CoT）推理，却普遍存在**以文本为中心的跨模态幻觉**，难以区分“转身”与“微笑”等语义相似或细粒度动作（Figure 1, Figure 4）。Video-STAR 通过三个关键设计突破了上述瓶颈：

* **推理框架升级**：将基线模型从“视觉特征匹配 + 文本 CoT”推至“上下文子动作分解→候选匹配→层次化评分”的三段推理流程。模型首先将整体动作解耦为一组具有区分性的子动作原语（如“投篮”分解为“起跳、抬手、压腕”），再动态调用外部工具提取视觉证据进行匹配与评分（Section 3.2, 3.4）。这一机制将推理根基从文本先验转移到视觉事实上，被论文明确指出能够“有效抑制跨模态幻觉”（Section C, confidence 0.9）。
* **工具集成与调用**：不同于基线模型的无工具或固定流水线操作（如简单的帧缩放/裁剪），Video-STAR 引入了一个动态工具库，包含人体检测、姿态估计、动作解释和视频描述四类工具（YOLO 11 与 Qwen API）。智能体根据输入内容**自主选择**最相关工具，而非全部调用，从而在保持性能的同时显著降低计算开销（Table 4：准确率 96.7% vs 97.2%，总时间减少 22%，工具时间减少 36%）。工具互换实验（YOLO→OpenPose，Qwen→Gemini‑1.5‑Pro）表明，性能仍高达 96.1% / 97.4%（Table 6），证明核心创新在于智能体的决策逻辑，而非具体工具栈。
* **奖励机制重设计**：将基线的二元答案奖励替换为**层次化奖励函数**：同时优化准确度、格式规范、工具使用效率和子动作重要性加权，且工具与子动作奖励仅在答案正确时激活（$R(\tau) = R_{\mathrm{acc}} + R_{\mathrm{format}} + \mathbb{I}_{R_{\mathrm{acc}}>0} (R_{\mathrm{tool}} + R_{\mathrm{sub}})$, Eq. 6）。这一设计通过 $w_k = n - k + 1$ 的排序权重显式激励模型优先关注语义突出的子动作，消融实验中用等权重替换后各数据集分别下跌 2.5 ~ 4.8 个百分点（Table 7）。

该方法在 **base-to-novel 和跨数据集设置**下均展现出对先行方法的压倒性优势：7B 版本在 Kinetics‑400 上谐波均值（HM）达到 96.7%，超过最佳 CLIP 方法（Open-MeDe）26.3 个百分点（Table 1）；在 Kinetics‑600 跨数据集评估中亦将 Top‑1 准确率从 71.3% 拉升至 90.5%（Table 2）。进一步地，GRPO 强化学习被证实为关键推手：**移除 RL 阶段后，UCF‑101 准确率从 96.7% 骤降至 76.8%**（Table 3），降幅远大于移除工具或子动作模块，说明 RL 不仅驱动了工具的高效调用，更从根本上塑造了模型的推理策略。

### 适用边界与局限

尽管 Video-STAR 展示了“微调 + 零快门迁移”的强大潜力（仅在 HMDB‑51 高频类别上微调，即泛化至 K‑400、UCF‑101 和 SSv2），其适用边界仍受以下因素制约：

* **工具延迟与实时性**：工具调用占总推理时间的约 45%（Table 4, Table 5），端到端延迟达到 3.18 s，难以直接部署于需要毫秒级响应的实时系统。工具时间主要来自外部 API（动作解释、视频描述），本地模型（YOLO）部分相对较轻。
* **外部工具质量依赖**：姿态估计或人体检测的错误会传播到后续推理链。尽管工具互换实验显示框架具有模块鲁棒性，但在极端遮挡、低光照等工具失效场景下，性能仍可能退化。当前工具库仅包含四类工具，进一步扩展（如物体检测、场景图）虽可提升能力，也意味着更高的系统复杂性与耦合风险。
* **动作复杂度与泛化上限**：训练仅基于 HMDB‑51 子集，虽然跨数据集结果优异，但论文自身指出“对于更长序列、更多样化或更复杂的动作（如群体交互）的泛化性尚未充分验证”（limitations）。子动作分解逻辑目前针对单人动作设计，当涉及多人协同或多对象交互时，分解粒度与权重分配机制可能需要根本性调整。
* **计算开销与精度权衡**：模型以适度的 GFLOPS 增加（+7,477）和内存占用（+0.86 GB）换取了近 39 个百分点的准确率提升（Table 5），性价比显著，但对于边缘设备或大批量离线处理，仍需通过蒸馏或量化等手段压缩开销。

### 开放问题

Video-STAR 将工具使用与强化学习引入开放词汇动作识别，为后续研究打开了多条高价值路径：

1. **跨任务迁移**：工具增强的子动作推理框架能否直接复用到视频问答、密集视频描述、时序动作定位等任务？其“分解‑匹配‑评分”流程在动作识别之外可能同样有效，但需验证对因果推理或长时依赖的支持能力。
2. **推理延迟压缩**：能否通过模型蒸馏、并行化工具调用、或缓存工具输出等工程手段，将总推理时间压缩至实时阈值以下？当前 45% 的工具开销为优化留出了可观空间。
3. **群组与交互动作扩展**：如何重新定义子动作分解逻辑，以处理多人体育比赛、舞蹈配合、对话交互等群体场景？可能需要从单人姿态扩展到多人时空图建模。
4. **子动作模式的自动发现**：现有分解依赖于人工设计的 trigger prompt 与教师模型生成，能否通过端到端学习从数据中自动涌现任务相关的子动作原语？这可能需要结合自监督表征与可微分工具选择。
5. **工具库的开放生态**：将工具调用抽象为标准接口，允许社区贡献新的视觉基础模型（如物体检测、深度估计）或知识库，能否持续提升 Video-STAR 的上界，并催生更通用的视频理解智能体？

总体上，Video-STAR 在方法论谱系中居于 CLIP 微调方法与通用 MLLM 的交汇地带，却凭借**智能体逻辑的引入**跃迁到一个新的坐标系——将感知与推理解耦，再通过工具调用与强化学习重新耦合。这一定位使其既具备强烈的实证优势（K‑400 HM 96.7%），也面临系统延迟、工具依赖和场景泛化等亟待解决的工程化难题。后续工作沿上述开放方向推进，有望将工具增强的视频智能体推向更广泛的真实世界应用。

## 原文 PDF

![[paperPDFs/ICLR_2026/Video_STAR_Reinforcing_Open_Vocabulary_Action_Recognition_with_Tools.pdf]]
