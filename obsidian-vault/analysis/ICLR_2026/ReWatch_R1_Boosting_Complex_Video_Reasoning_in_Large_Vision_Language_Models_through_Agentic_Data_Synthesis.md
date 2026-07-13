---
title: "ReWatch-R1: Boosting Complex Video Reasoning in Large Vision-Language Models through Agentic Data Synthesis"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ReWatch_R1_Boosting_Complex_Video_Reasoning_in_Large_Vision_Language_Models_through_Agentic_Data_Synthesis.pdf
project_link: https://rewatch-r1.github.io
code_link: null
openreview_forum_id: xindJJLSr1
aliases:
- RR
- ReWatch-R1
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "通过模拟人类“重新观看”过程的多智能体ReAct框架合成的视频思维链数据，以及评估中间步骤事实正确性和推理充分性的观察与推理奖励机制。"
primary_logic: "将智能体数据合成（生成高质量、视频基于的思维链）与过程奖励（评估观察准确性和推理充分性）相结合，可以打破复杂视频推理的数据瓶颈，使大模型通过RLVR学习真正基于视频证据的推理，有效抑制幻觉。"
claims:
- "ReWatch-R1在五项视频推理基准上达到最先进水平，7B模型192帧平均准确率35.51%，超过Video-R1（31.00%）和Qwen2.5-VL-7B基础模型（30.71%）"
- "观察与推理奖励机制进一步提升性能：ReWatch-R1 + O&R平均35.78% vs 无O&R 35.51%（192帧）"
- "SFT是RL的前提条件：未进行SFT直接RL导致灾难性性能崩溃"
- "ReWatch-QA数据集具有更高复杂度和视频依赖性，推理步骤数约为Video-R1的两倍（3.31 vs 1.82），纯文本回答准确率仅29.4%（接近随机猜测基线25%）"
---

# ReWatch-R1: Boosting Complex Video Reasoning in Large Vision-Language Models through Agentic Data Synthesis

> [!tip] 核心洞察
> 将智能体数据合成（生成高质量、视频基于的思维链）与过程奖励（评估观察准确性和推理充分性）相结合，可以打破复杂视频推理的数据瓶颈，使大模型通过RLVR学习真正基于视频证据的推理，有效抑制幻觉。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ReWatch-R1：通过智能体数据合成增强大视觉语言模型的复杂视频推理 |
| 英文题名 | ReWatch-R1: Boosting Complex Video Reasoning in Large Vision-Language Models through Agentic Data Synthesis |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=xindJJLSr1) · [Project](https://rewatch-r1.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ReWatch-R1 |
| Dataset | Average of 5 Video Reasoning Benchmarks (192 frames), VCR-Bench (192 frames), Average of 4 Video Understanding Benchmarks (192 frames) |

> [!tip] 效果简介
> - Average of 5 Video Reasoning Benchmarks (192 frames) 上，accuracy 为 35.51% (ReWatch-R1)，对比 31.00% (Video-R1)，变化 +4.51%。
> - Average of 5 Video Reasoning Benchmarks (192 frames) 上，accuracy 为 35.51% (ReWatch-R1)，对比 30.71% (Qwen2.5-VL-7B non-thinking)，变化 +4.80%。
> - VCR-Bench (192 frames) 上，accuracy 为 40.14% (ReWatch-R1)，对比 32.69% (Video-R1)，变化 +7.45%。

## 概要

**核心问题**：现有视频推理数据集普遍缺乏高质量、挑战性的多跳问题以及基于视频内容的思维链（CoT），导致基于强化学习的视频推理（RLVR）方法难以引导模型进行真正基于证据的推理，模型容易依赖语言先验而产生幻觉。

**核心方法**：ReWatch-R1 通过两条路径打破上述数据瓶颈。其一，提出**多智能体 ReAct 数据合成框架**，模拟人类“重新观看”过程，显式生成包含信息检索与验证步骤的视频思维链数据（ReWatch-CoT）；同时通过对比生成与三重过滤机制构建高难度、视频依赖的问答数据（ReWatch-QA）。其二，设计**观察与推理（O&R）奖励机制**，在 GRPO 强化学习过程中不仅评估最终答案正确性，还额外评估中间观察的事实准确性与推理的充分性，直接惩罚幻觉。

**核心结论**：
- 在五项视频推理基准上，ReWatch-R1（7B，192帧）平均准确率达到 **35.51%**，超过 Video-R1（31.00%）和 Qwen2.5-VL-7B 基础模型（30.71%）。配合 O&R 奖励后进一步提升至 **35.78%**。
- SFT 是 RL 的必要前提：跳过 SFT 直接进行 RL 会导致灾难性性能崩溃。
- ReWatch-QA 数据集具有显著更高的复杂度和视频依赖性，其推理步骤数约为 Video-R1 的两倍（3.31 vs 1.82），纯文本回答准确率仅 29.4%，接近随机猜测基线（25%），有效抑制了语言捷径。

**方法定位**：ReWatch-R1 属于“智能体数据合成 + 过程奖励引导的 RLVR”范式。与 Video-R1 等仅依赖最终答案奖励的方法不同，ReWatch-R1 将视频推理建模为“观察→推理→答案”的序列过程，通过合成高质量的视频基于思维链数据初始化策略，再利用 O&R 奖励在 RL 阶段强化推理的忠实性与逻辑一致性。该方法在 7B 和 32B 模型规模上均验证了有效性，且对视频理解任务亦有正向迁移（平均提升 1.95%）。



视频推理要求模型从长时序视觉流中提取关键证据、建立因果联系并进行多跳逻辑推导，是当前大视觉语言模型（LVLM）面临的核心挑战之一。尽管基于强化学习的视觉推理训练（RLVR）在图像领域已展现出通过过程奖励引导模型进行可验证推理的潜力，但将其直接迁移至视频领域时，面临一个根本性的瓶颈：**现有视频推理数据集缺乏高质量、挑战性的多跳问题以及基于视频内容的思维链（CoT）**。

具体而言，现有用于RLVR的视频数据集存在两个结构性缺陷。其一，问答对的质量不足：大量问题可通过文本先验或简单感知回答，形成“快捷推理”（shortcut reasoning），使模型无需真正理解视频内容即可获得正确答案。其二，思维链数据不可靠：许多CoT是由纯文本语言模型基于问题生成的，缺乏对视频内容的实际检索与验证，导致推理轨迹充满语言偏见和事实幻觉。这两个缺陷共同导致RLVR方法无法有效引导模型进行基于证据的推理——模型学到的不是“观看-推理”的能力，而是利用数据偏差进行猜测的策略。

ReWatch-R1针对上述缺口，提出了一条从数据合成到训练机制的完整路径。其核心洞察在于：**将智能体数据合成（生成高质量、视频基于的思维链）与过程奖励（评估观察准确性和推理充分性）相结合，可以打破复杂视频推理的数据瓶颈，使大模型通过RLVR学习真正基于视频证据的推理，有效抑制幻觉。**

这一洞察建立在以下因果链条之上：首先，通过模拟人类“重新观看”过程的多智能体ReAct框架，合成显式记录信息检索与验证步骤的视频思维链数据，为模型提供可靠的推理模板；其次，设计观察与推理（O&R）奖励机制，在RL阶段不仅评估最终答案正确性，还直接评估中间观察的事实正确性和推理的逻辑充分性，从而将奖励信号从“答对”延伸到“如何答对”。两者协同作用，使模型从SFT阶段习得“如何看”，在RL阶段通过过程奖励被强化为“必须看”。



## 核心方法与创新机理

ReWatch-R1的核心创新在于将**智能体数据合成**与**过程奖励机制**深度耦合，系统性地解决了当前视频推理RLVR范式的两大瓶颈：高质量视频思维链数据的缺失，以及仅依赖最终答案正确性的稀疏奖励无法有效引导基于视频证据的推理。

### 1. 因果调控杠杆：从数据瓶颈到奖励瓶颈的联合突破

现有视频推理方法（如Video-R1）面临双重困境：其一，基于文本语言模型生成的思维链数据存在严重的语言偏见和事实不准确性，导致模型在RLVR过程中无法学习到真正基于视频的推理模式；其二，仅使用答案正确性奖励（$r_{acc}$）无法区分模型是基于视频证据还是基于语言先验得出正确答案，因而无法有效抑制幻觉。

ReWatch-R1通过两个相互增强的机制打破这一僵局：

- **数据侧**：多智能体ReAct框架合成的视频思维链数据（ReWatch-CoT），显式模拟人类“重新观看”的信息检索与验证过程，为模型提供了高质量的视频基于推理示范。
- **奖励侧**：观察与推理（O&R）奖励机制，在答案正确性基础上额外评估中间步骤的观察真实性（$r_{obs}$）和推理充分性（$r_{rea}$），直接惩罚与视频内容不一致的幻觉推理。

两者的耦合关系体现在：高质量CoT数据为RL提供了有效的初始策略（证据表明，跳过SFT直接进行RL会导致灾难性性能崩溃，见Figure 5a），而O&R奖励则进一步引导RL优化过程，使模型在保持高准确率的同时减少冗余推理步骤（Figure 6b）。

### 2. 关键Changed Slots分析

#### Slot 1：思维链数据合成方法——从文本驱动到视频基于的ReAct框架

**基线方法**（Video-R1等）：基于简单视频问答数据集，通过文本语言模型生成思维链。这类数据存在根本性缺陷——语言模型无法访问视频内容，生成的推理过程往往基于语言先验而非视频证据。证据显示，Video-R1-QA的纯文本回答准确率高达68.9%，表明其问题存在严重的文本快捷路径（Figure 6a）。

**ReWatch-R1方案**：引入多智能体ReAct框架，定义Reasoner和Observer两个智能体：
- Reasoner（$\mathcal{A}_R$）基于历史上下文生成思考（$T_t$）和行动（$Act_t$）
- Observer（$\mathcal{A}_O$）在视频详细描述（$C_{detail}$）上执行行动，返回观察结果（$Obs_t$）

这一框架显式记录了“重新观看”的完整推理轨迹，包括信息检索步骤和验证过程。效果对比：ReWatch-QA的推理步骤数约为Video-R1的两倍（3.31 vs 1.82），纯文本回答准确率仅29.4%，接近随机猜测基线25%（Figure 6a），证明其问题必须依赖视频内容才能正确回答。

#### Slot 2：问答数据质量与过滤——从简单感知到对比生成加三重过滤

**基线方法**：简单感知问答，存在大量可被文本先验回答的快捷问题。

**ReWatch-R1方案**：采用对比生成策略，基于详细描述（$C_{detail}$）和摘要（$C_{sum}$）生成仅能从详细描述回答的问题：
$$(Q, A)_{raw} = \mathcal{M}_{qa}(C_{detail}, C_{sum})$$

随后通过三重过滤机制净化数据：
1. **答案验证**：确保生成答案的正确性
2. **文本偏见消除**：验证问题无法仅凭文本先验回答
3. **摘要偏见消除**：验证问题无法仅凭视频摘要回答

消融实验（Figure 5b）表明，仅使用基线QA数据（Video-R1-QA和LongVideoReason-QA）进行RL得分最低，而使用ReWatch-QA数据带来显著提升，证实了高质量QA数据对RL最终性能的决定性作用。

#### Slot 3：强化学习奖励机制——从稀疏答案奖励到过程奖励

**基线方法**：仅使用最终答案正确性作为奖励（$r_{acc}$）。

**ReWatch-R1方案**：设计O&R奖励机制，将视频推理QA过程建模为“视频+问题→观察+推理→答案”的序列流，并引入两个过程奖励：

- **观察奖励**（$r_{obs}$）：评估思维链中行动-观察对与详细视频描述的符合程度
$$r_{obs} = \mathrm{mean}(\{\mathcal{M}_{judge}(C_{detail}, \{Act_i, Obs_i\})\}_{i=1}^{N})$$

- **推理奖励**（$r_{rea}$）：基于从提取的行动-观察中推理得出的答案正确性
$$r_{rea} = \mathcal{M}_{judge}(A_{ao}, A_{gt})$$

最终组合奖励为：
$$r_{O\&R} = r_{acc} \times (1 + r_{obs} + r_{rea}) + r_{fmt}$$

这一设计的核心洞察在于：通过乘法形式将过程奖励与答案奖励耦合，使得仅当答案正确且推理过程基于真实视频观察时，模型才能获得最高奖励。实验结果（Table 1）验证了其有效性：ReWatch-R1 + O&R在192帧下平均准确率35.78%，优于无O&R的35.51%。

#### Slot 4：视频描述粒度——从整体描述到分层动态帧率的时间戳精确描述

**基线方法**：整体性、无时间戳的视频描述。

**ReWatch-R1方案**：采用分层动态帧率策略：
- 对长视频（>10分钟）先进行语义分割，使用低帧率LVLM（$\mathcal{M}_{seg}$）将视频划分为$k$个语义连贯的片段
- 对每个片段使用高帧率LVLM（$\mathcal{M}_{cap}$）生成带相对时间戳的详细描述
- 通过时间戳重对齐（$t_{ij} = t_i^{start} + \tau_{ij}$）将相对时间戳转换为绝对时间戳

这一设计为后续的QA生成和CoT合成提供了精确的时间定位能力，是多智能体ReAct框架中Observer能够执行定向信息检索的基础。

### 3. 创新点的协同效应

上述四个changed slots并非独立运作，而是形成了层层递进的协同体系：**分层描述**为**对比QA生成**提供信息基础，**三重过滤**确保QA的高质量和高视频依赖性，**ReAct CoT合成**在此基础上生成视频基于的推理轨迹，最终**O&R奖励**在RL阶段引导模型内化这一推理模式。消融实验（Figure 5a）证实了这一协同效应的必要性：将ReWatch-CoT替换为Video-R1的CoT数据会显著降低性能，说明高质量数据与奖励机制缺一不可。



![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_xindJJLSr1/figures/003_Figure_3.jpg]]
*Figure 3: The data construction pipeline. (a) Caption Construction. Long videos are semantically segmented to produce detailed, temporally-aware captions. (b) QA Pair Generation. A contrastive method using detailed and summary captions generates complex questions, which are then purified by a three-layer filtering mechanism. (c) CoT Synthesis. A ReAct framework with a Reasoner Agent and an Observer Agent simulates a "re-watching" process by performing targeted queries on the video caption to generate video-grounded reasoning traces*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_xindJJLSr1/figures/004_Figure_4.jpg]]
*Figure 4: Our two-stage Post-Training framework. (a) A Base Model is first fine-tuned (SFT) on all ReWatch datasets, (b) then further refined as a policy via Reinforcement Learning (RL) using the ReWatch-QA dataset. (c) The "Rollout" panel illustrates the generative process of the policy: producing a purely textual chain-of-thought that simulates a Thought-Action-Observation reasoning loop through self-generated text segments. (d) We employ four verifiable reward mechanisms*

ReWatch-R1 的整体框架由**数据合成管线**与**两阶段后训练流程**两部分串联构成，核心目标是通过高质量、视频基于的思维链数据打破复杂视频推理的数据瓶颈。

### 数据合成管线

如图 Figure 3 所示，数据构建分为三个级联模块：

1.  **分层视频描述 (Hierarchical Video Captioning)**：对长视频进行语义分段，仅对时长超过 10 分钟的视频执行此操作以保持长期上下文完整性。每个片段以高帧率生成带相对时间戳的详细描述，再通过时间戳重对齐转换为绝对时间戳，最终形成具有时间粒度的视频描述 $C_{\mathrm{detail}}$。

2.  **对比式问答生成与三重过滤 (Contrastive QA Generation & Three-Layer Filtering)**：同时输入详细描述 $C_{\mathrm{detail}}$ 与摘要 $C_{\mathrm{sum}}$，生成仅能从详细描述回答的高难度多选题。随后经过答案验证、文本偏见消除、摘要偏见消除三层过滤，剔除可被纯文本先验或摘要“快捷回答”的问题，确保问题必须依赖视频细节。

3.  **多智能体 ReAct 思维链合成 (Multi-Agent ReAct CoT Synthesis)**：引入 **Reasoner** 与 **Observer** 两个智能体模拟人类“重新观看”过程。Reasoner 基于历史 $H_{t-1}$ 生成思考 $T_t$ 与动作 $Act_t$，Observer 在视频描述 $C_{\mathrm{detail}}$ 上执行动作并返回观察 $Obs_t$，循环迭代生成显式记录信息检索与验证步骤的视频基于思维链轨迹。

该管线产出三类数据集：ReWatch-Cap（视频描述）、ReWatch-QA（高难度问答）和 ReWatch-CoT（思维链），共同构成 ReWatch 数据集。

### 两阶段后训练流程

如 Figure 4 所示，训练分为两个阶段：

1.  **监督微调 (SFT)**：基础模型在全部 ReWatch 数据集上进行多任务学习，包含视频描述、直接问答和思维链推理三项任务，总损失为三部分之和：
    $$\mathcal{L}_{\mathrm{SFT}}(\theta) = \mathcal{L}_{\mathrm{Cap}} + \mathcal{L}_{\mathrm{QA}} + \mathcal{L}_{\mathrm{CoT}}$$
    SFT 为后续强化学习提供强初始策略——消融实验证实，跳过 SFT 直接进行 RL 会导致灾难性性能崩溃。

2.  **GRPO 强化学习 (RL)**：以 SFT 模型为策略，仅使用 ReWatch-QA 数据进行优化。策略在推理时通过自生成文本片段模拟 Thought-Action-Observation 循环。奖励机制除最终答案正确性奖励 $r_{acc}$ 外，引入**观察与推理 (O&R) 奖励**：
    - **观察奖励 $r_{obs}$**：评估思维链中行动-观察对与详细视频描述的符合程度，直接惩罚幻觉。
    - **推理奖励 $r_{rea}$**：基于提取的行动-观察重新推理，评估其答案正确性。
    
    最终组合奖励为：
    $$r_{O\&R} = r_{acc} \times \left(1 + r_{obs} + r_{rea}\right) + r_{fmt}$$
    其中 $r_{fmt}$ 为格式奖励。该机制引导模型在准确理解视频内容的基础上进行适当推理，而非依赖语言偏见生成幻觉。

### 输入输出流

- **输入**：原始视频 → 语义分段 → 分层描述 → 对比式问答生成与过滤 → 多智能体 ReAct 合成 → 结构化数据集。
- **训练流**：基础模型 → SFT（多任务学习）→ 策略初始化 → GRPO RL（O&R 奖励优化）→ ReWatch-R1 模型。
- **推理流**：视频 + 问题 → 策略生成 Thought-Action-Observation 推理轨迹 → 最终答案。



ReWatch-R1 的核心技术路线围绕“高质量视频推理数据合成”与“过程奖励引导的强化学习”两条主线展开。其关键模块与公式如下。

### 1. 分层视频描述生成

对于长视频，首先通过低帧率 LVLM $\mathcal{M}_{\mathrm{seg}}$ 进行语义分割，将视频 $V$ 划分为 $k$ 个语义连贯的片段 $S$：

$$ S = \{ s_1, \dots, s_k \} = \mathcal{M}_{\mathrm{seg}}(V) $$

随后，使用高帧率 LVLM $\mathcal{M}_{\mathrm{cap}}$ 对每个片段 $s_i$ 生成带相对时间戳 $\tau_{ij}$ 的详细描述 $D_i^{\mathrm{rel}}$：

$$ D_i^{\mathrm{rel}} = \{ (c_{ij}, \tau_{ij}) \}_{j=1}^{m_i} = \mathcal{M}_{\mathrm{cap}}(s_i) $$

最后，通过时间戳重对齐将相对时间转换为绝对时间 $t_{ij}$：

$$ t_{ij} = \mathcal{P}(\tau_{ij}, t_i^{\mathrm{start}}) = t_i^{\mathrm{start}} + \tau_{ij} $$

这一模块为后续所有合成步骤提供了细粒度、时间精确的视频文本基础。

### 2. 对比式问答生成与三重过滤

为避免模型依赖文本先验“走捷径”，ReWatch-QA 采用对比生成策略。QA 生成器 $\mathcal{M}_{qa}$ 同时输入详细描述 $C_{detail}$ 和摘要 $C_{sum}$，生成仅能从详细描述回答的问题：

$$ (Q, A)_{\mathrm{raw}} = \mathcal{M}_{qa}(C_{detail}, C_{sum}) $$

生成的 QA 对随后经过三重过滤机制净化：
- **文本线索泄漏过滤**：排除问题本身包含答案线索的样本。
- **答案验证过滤**：确保生成的答案与视频内容一致。
- **摘要偏见消除过滤** $\mathcal{F}_3$：确保问题无法仅凭摘要 $C_{sum}$ 回答，强制模型依赖视频细节。

### 3. 多智能体 ReAct 思维链合成

ReWatch-CoT 的核心是模拟人类“重新观看”过程的双智能体 ReAct 框架：
- **推理者（Reasoner）** $\mathcal{A}_R$：基于历史 $H_{t-1}$ 生成思考 $T_t$ 和检索动作 $Act_t$：
  $$ (T_t, Act_t) = \mathcal{A}_R(H_{t-1}) $$
- **观察者（Observer）** $\mathcal{A}_O$：在视频描述 $C_{detail}$ 上执行动作，返回观察结果 $Obs_t$：
  $$ Obs_t = \mathcal{A}_O(Act_t, C_{detail}) $$

通过多轮交互，框架生成包含 Thought-Action-Observation 循环的完整推理轨迹。

### 4. 监督微调复合损失

SFT 阶段使用多任务学习，总损失为描述、直接问答、思维链推理三部分之和：

$$ \mathcal{L}_{\mathrm{SFT}}(\theta) = \mathcal{L}_{\mathrm{Cap}} + \mathcal{L}_{\mathrm{QA}} + \mathcal{L}_{\mathrm{CoT}} $$

这为后续 RL 阶段提供了强初始策略——消融实验证实，跳过 SFT 直接进行 RL 会导致灾难性性能崩溃。

### 5. 观察与推理奖励机制

O&R 奖励是该方法的核心创新，直接针对视频推理中的幻觉问题。它将推理过程建模为“视频+问题 → 观察+推理 → 答案”的序贯流程，并设计四个可验证奖励：

- **准确率奖励** $r_{acc}$：基于最终答案与真实答案的一致性：
  $$ r_{acc} = \mathcal{M}_{judge}(A, A_{gt}) $$

- **观察奖励** $r_{obs}$：评估思维链中所有行动-观察对与详细视频描述的符合程度：
  $$ r_{obs} = \mathrm{mean}\left(\{\mathcal{M}_{judge}(C_{detail}, \{Act_i, Obs_i\})\}_{i=1}^{N}\right) $$

- **推理奖励** $r_{rea}$：从提取的行动-观察中重新推理，评估推理路径本身的正确性：
  $$ r_{rea} = \mathcal{M}_{judge}(A_{ao}, A_{gt}) $$

- **组合 O&R 奖励** $r_{O\&R}$：答案正确性乘以观察与推理的加权和，再加上格式奖励 $r_{fmt}$：
  $$ r_{O\&R} = r_{acc} \times \left(1 + r_{obs} + r_{rea}\right) + r_{fmt} $$

这一设计的因果逻辑是：仅当模型正确理解视频内容（$r_{obs}$ 高）且逻辑推理充分（$r_{rea}$ 高）时，才能获得最大奖励。它直接惩罚了脱离视频证据的幻觉推理。实验表明，加入 O&R 奖励后，ReWatch-R1 在五项推理基准上的平均准确率从 35.51% 进一步提升至 35.78%（192 帧）。



## 实验与关键发现

### 主要结果：视频推理基准

ReWatch-R1在五项视频推理基准上取得最先进性能。在192帧设置下，7B模型平均准确率达到35.51%，显著超越Video-R1（31.00%）和Qwen2.5-VL-7B基础模型（30.71%），提升幅度分别为+4.51和+4.80个百分点。引入观察与推理奖励机制（O&R）后，平均准确率进一步提升至35.78%（Table 1）。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_xindJJLSr1/figures/005_Table_1.jpg]]
*Table 1: Performance comparison on Video Reasoning tasks. ∗ indicates that we reproduced the model using a training configuration with 192 frames. † indicates that reinforcement learning is conducted using exactly the same data as ReWatch-R1. The best results among models of the same size are indicated in bold*

在VCR-Bench上，ReWatch-R1达到40.14%，相比Video-R1的32.69%提升+7.45个百分点，是该基准上最显著的单项增益。在384帧设置下，ReWatch-R1平均准确率为35.59%，O&R版本达到35.89%，表明方法对帧数增加具有鲁棒性。

扩展到32B模型规模，ReWatch-R1-32B+O&R在192帧下平均准确率38.08%，超越Qwen2.5-VL-32B非思考模式基线（35.71%）+2.37个百分点（Table 2）。在视频理解基准上，ReWatch-R1同样保持竞争力，7B模型平均54.15%，相比基础模型提升+1.95%（Table 4）。

### SFT是RL的必要前提

消融实验揭示了SFT阶段的不可替代性。Figure 5a显示，跳过SFT直接进行RL会导致灾难性性能崩溃，验证了RL需要一个足够强的初始策略才能有效探索。仅使用SFT的ReWatch-R1-SFT（33.25%）已经超越大多数竞争方法的SFT版本，包括Video-R1-SFT（29.74%）和LongVideoReason-SFT（26.31%），证明了ReWatch合成数据的质量优势。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_xindJJLSr1/figures/006_Figure_5.jpg]]
*Figure 5: (a) Ablation results using different CoT data*

### 思维链数据质量的关键作用

将ReWatch-CoT数据替换为Video-R1的CoT数据会显著降低性能（Figure 5a），表明高质量、视频基于的思维链是RL阶段性能增益的核心驱动力。ReWatch-CoT通过多智能体ReAct框架显式模拟“重新观看”过程，生成的信息检索和验证步骤为模型提供了更可靠的推理轨迹模板。

### QA数据质量决定RL上限

Figure 5b的比较分析表明，RL阶段使用的QA数据质量直接决定最终性能。仅使用基线QA数据（Video-R1-QA和LongVideoReason-QA）进行RL得分最低，而使用ReWatch-QA数据带来显著提升。这一结果与ReWatch-QA的数据特性一致：该数据集具有更高的复杂度和视频依赖性，推理步骤数约为Video-R1的两倍（3.31 vs 1.82），纯文本回答准确率仅29.4%，接近随机猜测基线25%（Figure 6a），证明三重过滤机制有效消除了文本快捷路径，迫使模型进行真正的视频理解。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_xindJJLSr1/figures/007_Figure_6.jpg]]
*Figure 6: (b) Ablation results using different QA data*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_xindJJLSr1/figures/010_Figure_6.jpg]]
*Figure 6: Analysis on QA complexity and Evolution of action count*

### RL优化推理过程效率

RL阶段不仅提升了准确率，还优化了推理效率。Figure 6b显示，经过RL训练后，模型的平均动作数减少，同时保持高准确率，表明策略学会了剪枝冗余步骤，聚焦于关键的信息检索和验证动作。这一现象说明GRPO算法成功引导模型在探索与利用之间找到更优平衡。

### 思考模式的演化轨迹

Figure 7揭示了思考模式在训练过程中的动态变化。在基础模型阶段，启用思考模式反而有害（27.54% vs 30.71%），因为未经训练的模型无法有效利用CoT格式。SFT阶段，思考模式性能逐步提升并最终超越非思考模式，RL阶段进一步拉大差距，虚线所示的最终性能表明思考模式成为性能优势的主要来源。这一演化轨迹验证了“先对齐格式、再优化推理”的两阶段策略的有效性。

### 跨视频时长泛化

Figure 9展示了ReWatch-R1在不同视频时长上的性能表现。在短（0-3分钟）、中（3-20分钟）、长（>20分钟）三类视频上，ReWatch-R1在推理和理解任务上均保持稳定优势，表明分层动态帧率的描述生成策略有效保留了长视频中的时序信息，避免了长视频场景下的性能退化。



## 定位与知识库关联

### 1. 方法沿革与基线关系

ReWatch-R1 针对的核心瓶颈是现有视频推理数据集中高质量、挑战性多跳问题与基于视频证据的思维链（CoT）的匮乏。这一瓶颈直接限制了基于强化学习的视频推理（RLVR）方法的有效性，因为模型缺乏引导其进行真正基于证据推理的训练信号。论文将这一问题的解决路径分解为两个相互耦合的维度：**数据质量**与**奖励信号**。

在数据维度上，ReWatch-R1 直接对标并改进了 **Video-R1** 的数据合成策略。Video-R1 的 CoT 数据依赖文本语言模型生成，存在语言偏见和不真实性，其问答数据也包含大量可被文本先验回答的“快捷问题”。ReWatch-R1 通过多智能体 ReAct 框架模拟人类“重新观看”过程，显式记录信息检索与验证步骤，生成视频基于的思维链轨迹（ReWatch-CoT）。同时，对比生成结合三重过滤（答案验证、文本偏见消除、摘要偏见消除）的问答数据（ReWatch-QA）确保了问题必须依赖视频细节才能回答。实验证据表明，ReWatch-QA 的推理步骤数约为 Video-R1 的两倍（3.31 vs. 1.82），纯文本回答准确率仅 29.4%，接近随机猜测基线 25%，而 Video-R1 的对应指标高达 68.9%，这直接证明了 ReWatch 数据集的更高复杂度和视频依赖性（Figure 6a, Section 4.2）。

在奖励维度上，ReWatch-R1 引入了观察与推理（O&R）奖励机制，超越了仅依赖最终答案正确性的传统奖励（r_acc）。O&R 奖励通过评估模型输出中观察的真实性（r_obs）和推理的充分性（r_rea），直接惩罚幻觉，引导模型学习基于视频证据的推理过程。这一机制与 **GRPO** 算法结合，构成了完整的 RLVR 优化框架。

论文将 ReWatch-R1 与以下基线方法进行了系统比较：
- **基础模型基线**：**Qwen2.5-VL-7B**（Thinking/Non-Thinking）、**Qwen2.5-VL-32B**、**GLM4.1V-9B**、**InternVL3.5-8B**。
- **视频推理专用基线**：**Video-R1**、**Video-Chat-R1**、**VideoRFT**、**VersaVid-R1**、**TW-GRPO**、**GRPO-CARE**、**LongVideoReason**。
- **消融基线**：**Video-R1-SFT**、**LongVideoReason-SFT**（用于 SFT 阶段数据质量对比）；**Video-R1-RL**、**LongVideoReason-RL**（使用与 ReWatch-R1 完全相同的 40k RL 问答数据复现，用于 RL 阶段公平对比）。

### 2. 适用边界与局限

ReWatch-R1 的有效性建立在以下关键前提之上，这些前提也构成了其适用边界：

1.  **SFT 是 RL 的必要前提**：消融实验明确显示，去除 SFT 阶段直接进行 RL 会导致灾难性性能崩溃（Figure 5a, Section 4.2）。这意味着 ReWatch-R1 的方法不能跳过监督微调阶段，需要先通过多任务学习（视频文本对齐、直接问答、思维链推理）为策略模型提供良好的初始状态。

2.  **高质量 CoT 数据的不可替代性**：将 ReWatch-CoT 数据替换为 Video-R1 的 CoT 数据会显著降低性能（Figure 5a）。这表明 O&R 奖励机制和 RL 优化本身无法弥补初始思维链数据质量的缺陷，数据合成质量是性能上限的决定性因素。

3.  **QA 数据质量对 RL 阶段的决定性影响**：仅使用基线 QA 数据（Video-R1-QA 和 LongVideoReason-QA）进行 RL 得分最低，而使用 ReWatch-QA 数据带来显著提升（Figure 5b）。这进一步证实了 RL 阶段对高质量、视频依赖的问答数据的强依赖。

4.  **模型规模与帧数限制**：论文主要在 7B 和 32B 参数规模、192 帧和 384 帧设置下验证方法。方法在更大规模模型或更高帧数下的泛化性未经验证。此外，对于极长视频（>20分钟），虽然 Figure 9 显示了性能趋势，但具体瓶颈和优化策略仍需进一步探索。

5.  **数据合成成本**：多智能体 ReAct 框架和分层视频描述生成涉及多次大模型调用，计算成本较高。论文未报告数据合成的具体计算开销，这可能是实际应用中的一个限制因素。

### 3. 开放问题与未来方向

论文未明确列出开放问题，但从方法设计和实验结果中可以推断出以下值得进一步探索的方向：

1.  **“思考-观看”范式的深化**：当前 ReWatch-R1 的“思考”过程仍然是纯文本的，通过模拟 Thought-Action-Observation 循环来间接引用视频信息。一个自然的问题是：能否让模型在推理过程中直接与视觉编码器交互，实现真正的“thinking-with-video”，而非仅通过文本描述间接获取视觉证据？这涉及到模型架构层面的创新。

2.  **O&R 奖励的泛化与自动化**：当前 O&R 奖励依赖详细的视频描述（C_detail）作为评估依据，而 C_detail 本身由 LVLM 生成，存在信息损失和不准确的风险。如何设计更鲁棒、更自动化的过程奖励机制，减少对外部生成文本的依赖，是一个重要方向。

3.  **数据合成效率优化**：多智能体 ReAct 框架虽然有效，但合成效率可能成为大规模扩展的瓶颈。探索更高效的数据合成策略，例如通过蒸馏或自改进机制减少对多轮智能体交互的依赖，具有实用价值。

4.  **跨架构与跨模态泛化**：ReWatch-R1 基于 Qwen2.5-VL 架构，其数据合成与训练策略能否有效迁移到其他视觉语言模型架构，乃至扩展到其他视频理解任务（如时序定位、视频问答），值得系统研究。

5.  **推理效率与准确性的权衡**：RL 阶段使模型的平均动作数减少，同时保持高准确率（Figure 6b），这表明 RL 能够优化推理过程效率。然而，在计算资源受限的场景下，如何显式控制推理深度与准确性的权衡，仍是一个开放问题。



## 原文 PDF

![[paperPDFs/ICLR_2026/ReWatch_R1_Boosting_Complex_Video_Reasoning_in_Large_Vision_Language_Models_through_Agentic_Data_Synthesis.pdf]]
