---
title: "AVATAR: Reinforcement Learning to See, Hear, and Reason Over Video"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/AVATAR_Reinforcement_Learning_to_See_Hear_and_Reason_Over_Video.pdf
project_link: "https://people-robots.github.io/AVATAR/"
code_link: null
aliases:
- AAVAAR
- AVATAR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: AVATAR 的两大关键杠杆：(1) 引入离轨训练架构，通过分层重放缓冲区复用过去的成功与失败经验，并确保每个训练组内奖励多样性，从而同时解决数据低效和消失优势问题；(2) 引入时序优势塑造 (TAS)，利用与位置相关的抛物线加权函数，将学习信号集中在序列开头的规划令牌和末尾的综合令牌上，从而纠正统一信用分配问题。
primary_logic: 通过难度分层重放缓冲区，使训练组始终包含高奖励和低奖励样本，强制维持非零优势，将消失优势的死区转化为稳定的双峰分布；同时利用 Transformer 中注意力汇聚效应（早期令牌作为规划锚点，晚期令牌合成答案），以极简单的无评判器 U 形加权在长视频推理中显著提升关键步骤的学习效率。
claims:
- 在 Qwen2.5-Omni 基线上，AVATAR 在 OmniBench 上取得 +4.9 的绝对提升，而标准 GRPO 仅 +1.2，AVATAR 的增益约为 GRPO 的 4 倍。
- 组件消融实验表明，分层重放缓冲区单独使用即可将 OmniBench 提升 +3.6；进一步加入 TAS 后达到 +4.9，验证了两个组件的互补性。
- AVATAR 相比标准 GRPO 实现约 5 倍样本效率，仅需约 20% 的生成完成数即可达到目标性能。
- OmniBench 上 Accuracy = 49.1
---

# AVATAR: Reinforcement Learning to See, Hear, and Reason Over Video

> [!tip] 核心洞察
> 通过难度分层重放缓冲区，使训练组始终包含高奖励和低奖励样本，强制维持非零优势，将消失优势的死区转化为稳定的双峰分布；同时利用 Transformer 中注意力汇聚效应（早期令牌作为规划锚点，晚期令牌合成答案），以极简单的无评判器 U 形加权在长视频推理中显著提升关键步骤的学习效率。

| 字段 | 内容 |
|------|------|
| 中文题名 | AVATAR：通过强化学习实现视频的听、看与推理 |
| 英文题名 | AVATAR: Reinforcement Learning to See, Hear, and Reason Over Video |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2508.03100) · [Project](https://people-robots.github.io/AVATAR/) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | AVATAR (Audio-Video Agent for Alignment and Reasoning) |
| Dataset | OmniBench, Video-Holmes, MMVU |

> [!tip] 效果简介
> - OmniBench 上，Accuracy 49.1 vs 44.2 (+4.9)。
> - Video-Holmes 上，Accuracy 45.1 vs 40.6 (+4.5)。
> - MMVU 上，Accuracy 65.6 vs 60.2 (+5.4)。

## 概要

视频理解与推理要求模型同时处理视觉、听觉和时序信息，并在长推理链中整合多模态证据。当前主流方法采用 **Group Relative Policy Optimization (GRPO)** 对多模态大语言模型进行强化学习微调，但其在轨（on-policy）设计面临三个相互强化的瓶颈：**数据利用效率低**（每次更新后丢弃历史样本）、**消失优势问题**（组内奖励同质化导致优势值退化为零，模型停止学习）、以及**统一信用分配**（对推理链中所有令牌分配相同的标量优势，忽视规划、中间步骤与综合阶段的重要程度差异）。

AVATAR（**A**udio-**V**ideo **A**gent for **A**lignment and **R**easoning）针对上述瓶颈提出了两个关键杠杆：

1.  **离轨训练架构与分层重放缓冲区**：将训练策略从纯在轨切换为在轨-离轨混合模式。通过维护一个按难度分层的重放缓冲区（Easy/Medium/Hard），复用过去的高难度成功与失败样本，强制每个训练组内维持奖励多样性，从而同时解决数据低效和消失优势问题。离轨样本通过重要性采样修正策略偏移，并引入 Video-Context Reference Score（VCRS）作为稳定的优势基线。

2.  **时序优势塑造（Temporal Advantage Shaping, TAS）**：利用 Transformer 中注意力汇聚效应（早期令牌作为规划锚点，晚期令牌合成答案），以极简单的无评判器 U 形抛物线加权函数 $w_t = 1.0 + \lambda_{\mathrm{TAS}} \cdot (2\tilde{t} - 1)^2$ 调制每个令牌的优势信号，将学习信号集中在序列开头的规划令牌和末尾的综合令牌上，纠正统一信用分配问题。

在 Qwen2.5-Omni-7B 基线上，AVATAR 在 OmniBench 音视频理解基准上取得 **+4.9** 的绝对提升（标准 GRPO 仅 +1.2），在 Video-Holmes 和 MMVU 推理基准上分别提升 **+4.5** 和 **+5.4**。组件消融表明，分层重放缓冲区单独使用即可贡献 +3.6 的提升，TAS 在此基础上进一步带来增益，验证了两者的互补性。AVATAR 相比标准 GRPO 实现约 **5 倍样本效率**，仅需约 20% 的生成完成数即可达到目标性能。

### 多模态视频推理的强化学习瓶颈

大语言模型（LLM）在文本推理上的成功，推动了多模态大语言模型（MLLM）向音视频理解领域的快速扩展。然而，视频推理面临独特的挑战：模型需要同时处理长时序的视觉信号与音频信号，并在冗长的推理链中完成规划、中间步骤执行和最终答案综合。以 GRPO（Group Relative Policy Optimization）为代表的在轨强化学习方法，虽然在纯语言推理中取得了显著成效，但在迁移到多模态视频推理时暴露出三个结构性缺陷。

**第一，数据效率低下。** 标准 GRPO 采用严格的在轨策略设计——模型仅使用当前策略即时生成的样本进行训练，完成后立即丢弃。这种“用完即弃”的模式意味着，每一次昂贵的视频前向推理（涉及长上下文的多模态编码与自回归生成）所产生的经验无法被复用。当训练预算有限时，大量计算资源被浪费在重复探索已知区域上。

**第二，消失优势问题。** GRPO 的核心学习信号来自组内相对优势：将同一提示下多个响应的奖励标准化后，作为策略更新的方向。然而，当组内所有响应获得相同奖励时（例如全部正确或全部错误），标准化后的优势值退化为零，模型停止学习。在视频推理场景中，由于任务难度两极分化——简单样本组内全对、困难样本组内全错——这种“死区”现象尤为频繁，导致训练信号频繁中断。

**第三，统一信用分配缺陷。** GRPO 将整个输出序列的所有令牌分配相同的标量优势值，完全忽视了推理链中不同阶段的重要性差异。在长视频推理中，序列开头的令牌负责理解任务并制定推理规划（planning），末尾的令牌负责整合信息并生成最终答案（synthesis），而中间令牌执行逐步推理。将学习信号均匀洒在所有令牌上，意味着模型无法将奖励信号精准归因到真正关键的推理步骤。

### 现有方法的缺口

已有的 RL 训练框架（如标准 GRPO）在多模态视频推理中面临一个根本性的权衡：要么维持严格的在轨策略以保证策略梯度无偏，但承受数据低效和消失优势的代价；要么引入经验回放但缺乏有效的策略偏移修正和信用分配机制。此外，现有工作普遍忽略了 Transformer 架构中注意力汇聚的自然特性——早期令牌天然充当“规划锚点”，晚期令牌聚合信息以合成答案——这一结构先验尚未被系统性地用于引导强化学习的信用分配。

### 本文动机

针对上述三个瓶颈，AVATAR 提出两条核心改进路径：

1. **离轨训练架构 + 分层重放缓冲区**：打破在轨策略的限制，通过难度感知的分层缓冲区复用历史经验。缓冲区按提示的平均奖励动态分区（简单/中等/困难），优先保留高难度样本以维持训练组内的奖励多样性。这一设计同时解决了数据低效（复用昂贵的历史样本）和消失优势（强制组内奖励非零分布）两个问题，将 GRPO 的“死区”转化为稳定的双峰优势分布。

2. **时序优势塑造（Temporal Advantage Shaping, TAS）**：利用位置相关的抛物线加权函数，对推理链首尾令牌施加更强的学习信号，对中间令牌保持基准权重。这一设计以极简的无评判器方式，将 Transformer 的注意力汇聚效应转化为结构化的信用分配，使模型更高效地学习“规划”与“综合”这两个关键推理阶段。

## 核心方法与创新机理

AVATAR 的核心创新源于对标准 GRPO 三个根本性局限的系统性诊断与解决：

**1. 数据效率瓶颈与消失优势问题**

标准 GRPO 采用在轨（on-policy）策略设计，每个训练批次仅使用当前策略生成的新样本，训练完成后立即丢弃。这导致两个连锁问题：(a) 昂贵的历史样本无法复用，数据利用效率极低；(b) 当组内所有响应的奖励相同时，优势值退化为零——即**消失优势（vanishing advantages）**问题，模型停止学习。

AVATAR 通过引入**离轨训练架构**（off-policy architecture）同时解决这两个问题。其核心机制是**分层重放缓冲区**（Stratified Replay Buffer）：根据提示的平均奖励将历史样本动态分区为 Easy/Medium/Hard 三类，优先保留高难度样本。训练时，每个批次从缓冲区的不同分区采样离轨样本，与当前在轨样本混合，强制维持组内奖励多样性。这一设计将消失优势的“死区”转化为稳定的双峰优势分布（Figure 4），使训练信号持续有效。

**2. 统一信用分配缺陷**

GRPO 对整个输出序列的所有令牌分配相同的标量优势 $A_i$，忽视了推理链中不同阶段的重要程度差异：序列开头的**规划阶段**（planning）和末尾的**综合阶段**（synthesis）对推理质量的影响远大于中间步骤。

AVATAR 提出**时序优势塑造**（Temporal Advantage Shaping, TAS），通过位置相关的抛物线加权函数调制每个令牌的优势信号：

$$w_t = 1.0 + \lambda_{\mathrm{TAS}} \cdot (2\tilde{t} - 1)^2$$

其中 $\tilde{t}$ 是归一化后的令牌位置，$\lambda_{\mathrm{TAS}}$ 控制波幅。该函数在序列两端赋予最大权重 $1+\lambda_{\mathrm{TAS}}$，中间令牌权重为 $1$，形成 U 形曲线（Figure 2）。形塑后的优势 $A_{i,t}^{\mathrm{TAS}} = w_{i,t} \cdot A_i$ 将学习信号集中在规划锚点和答案合成阶段，利用 Transformer 中注意力汇聚效应（早期令牌作为规划锚点，晚期令牌合成答案），以极简单的无评判器加权显著提升长视频推理中关键步骤的学习效率。

**3. 离轨优势估计的不稳定性**

离轨样本的策略分布与当前策略存在偏移，直接使用组平均奖励 $\mu_R$ 作为基线会因批次噪声导致训练震荡。AVATAR 引入**视频上下文参考分数**（Video-Context Reference Score, VCRS）：对每个提示 $q$，维护其最近 20 个在轨实例的移动平均奖励 $\overline{R}(q)$，作为离轨优势估计的稳定基线：

$$A_{i,\mathrm{off}} = \frac{R(o_i) - \overline{R}(q)}{\sigma_{R,\mathrm{off}}}$$

VCRS 替代了嘈杂的组均值，使离轨训练信号更加稳定可靠。

**4. 探索停滞的辅助机制**

当特定提示长期处于高难度分区且策略探索停滞时，AVATAR 的**提示生成机制**（Hinting Mechanism）触发外部教师模型（Qwen2.5-VL-72B）生成高层提示，帮助策略逃离局部最优。该机制作为辅助组件，与核心的离轨架构和 TAS 形成互补。

**关键杠杆总结**：AVATAR 的两大关键杠杆——离轨训练架构（解决数据低效与消失优势）和时序优势塑造（纠正统一信用分配）——并非简单叠加，而是产生协同效应。组件消融实验（Table 4）表明，分层重放缓冲区单独使用即可在 OmniBench 上提升 +3.6，加入 TAS 后达到 +4.9，验证了两者的互补性。

AVATAR 的核心设计围绕标准 GRPO 的三个结构性缺陷展开：**在轨策略导致的数据低效**、**奖励同质引发的消失优势**，以及**统一信用分配对推理链不同阶段重要性的忽视**。为解决这些问题，AVATAR 构建了一个离轨训练架构，并引入时序优势塑造机制，形成从数据采样到梯度更新的完整闭环。

### 训练架构：离轨学习与分层重放缓冲区

标准 GRPO 采用严格的在轨策略：每个训练步仅使用当前策略即时生成的样本，完成后立即丢弃。这一设计导致两个后果——昂贵的历史经验被浪费，且当组内所有响应的奖励相同时，优势值退化为零，模型停止学习。

AVATAR 将训练目标扩展为在轨损失与离轨损失的加权和：

$$\mathcal{T}_{\mathrm{AVATAR}}(\theta) = \mathcal{T}_{\mathrm{on-policy}}(\theta) + \alpha \cdot \mathcal{T}_{\mathrm{off-policy}}(\theta)$$

其中 $\alpha$ 控制离轨样本的贡献权重，离轨样本通过重要性采样比 $r_i^{\mathrm{off}}(\theta) = \frac{\pi_{\theta}(o_i | q)}{\pi_{\theta_{\mathrm{off}}}(o_i | q)}$ 修正策略偏移。

离轨样本来源于**分层重放缓冲区**。该缓冲区根据每个提示的历史平均奖励将样本动态划分为 Easy / Medium / Hard 三个难度层级，优先保留高难度样本。这一分层的核心作用在于：强制每个训练组内同时包含高奖励和低奖励样本，从而维持奖励多样性，将 GRPO 中优势值集中于零的“死区”转化为稳定的双峰分布，从根本上解决消失优势问题。

此外，缓冲区还集成了**提示生成机制**：当某个提示长期处于高难度区且策略探索停滞时，系统触发外部教师模型生成高层提示，帮助策略逃离局部最优。

### 信用分配：时序优势塑造

GRPO 对整个输出序列的所有令牌分配相同的标量优势 $A_i$，忽略了推理链中不同阶段的重要程度差异。AVATAR 提出**时序优势塑造**，通过位置相关的抛物线权重函数调制每个令牌的优势值：

$$A_{i,t}^{\mathrm{TAS}} = w_{i,t} \cdot A_i$$

其中权重函数 $w_t = 1.0 + \lambda_{\mathrm{TAS}} \cdot (2\tilde{t} - 1)^2$ 呈 U 形分布：序列两端的令牌（对应规划与综合阶段）获得 $1 + \lambda_{\mathrm{TAS}}$ 的放大权重，中间令牌保持基准权重 1。这一设计的直觉来源于 Transformer 的注意力汇聚效应——早期令牌作为规划锚点建立推理框架，晚期令牌合成最终答案，两者对推理质量的影响远大于中间步骤。

### 训练流水线：四阶段递进

AVATAR 的训练采用四阶段递进式流水线，逐步提升任务复杂度和模态融合深度：

1. **Stage 0（冷启动 SFT）**：在基础多模态大语言模型上进行监督微调，建立初步的视觉推理和格式遵循能力。
2. **Stage 1（视觉推理）**：仅使用视觉模态数据进行 RL 训练，奖励函数为 $0.5 \times R_{\mathrm{format}} + 0.5 \times R_{\mathrm{acc}}$，专注于格式合规与答案准确性。
3. **Stage 2（音视频推理）**：引入音频模态，奖励组合扩展为 $0.2 \times R_{\mathrm{format}} + 0.4 \times R_{\mathrm{acc}} + 0.4 \times R_{\mathrm{self}}$，其中 $R_{\mathrm{self}}$ 为多数投票一致性奖励，用于在没有标准答案时提供自监督信号。
4. **Stage 3（音频-物体定位）**：进一步加入逐步评判奖励 $R_{\mathrm{judge}}$，由外部 VLM 对推理步骤进行逐级评估，提供细粒度的过程反馈。

### 稳定化机制：视频上下文参考分数

在离轨优势估计中，标准 GRPO 使用的组均值 $\mu_R$ 受批次噪声影响严重。AVATAR 引入**视频上下文参考分数**，以每个提示最近 20 个在轨实例的移动平均奖励 $\overline{R}(q)$ 替代组均值：

$$A_{i,\mathrm{off}} = \frac{R(o_i) - \overline{R}(q)}{\sigma_{R,\mathrm{off}}}$$

这一设计为离轨优势提供了稳定的基线，防止因批次内奖励波动导致的训练震荡。

### 整体数据流

每个训练步的数据流如下：从当前策略生成在轨样本，同时从分层重放缓冲区采样离轨样本，按 4:4 的平衡比例混合；在轨优势使用组标准化计算，离轨优势使用 VCRS 基线计算；所有令牌的原始优势经 TAS 抛物线加权调制成形优势；最终通过裁剪的重要性采样目标与 KL 散度正则项更新策略参数。

![[assets/figures/papers/paper_list_l1041_https_arxiv_org_abs_2508_03100/figures/001_Figure_1.jpg]]
*Figure 1: Standard GRPO (top) vs. AVATAR (bottom). AVATAR enhances GRPO with two key components: (1) an off-policy architecture using a stratified replay buffer to improve data efficiency, and (2) Temporal Advantage Shaping (TAS), a novel credit assignment strategy that focuses learning on critical reasoning steps*

AVATAR 在标准 GRPO 框架上引入两个关键模块，分别解决数据效率与信用分配两大瓶颈。以下逐一拆解其设计动机、公式化定义与变量含义。

### 4.1 离轨训练架构与分层重放缓冲区

**动机**：标准 GRPO 采用在轨（on-policy）策略，每次训练仅使用当前策略生成的新样本，生成后立即丢弃。这导致两个问题——(1) 昂贵的视频推理样本无法复用，数据效率极低；(2) 当组内所有响应的奖励相同时，优势值 $A_i$ 退化为零（消失优势问题），模型停止学习。

**解决方案**：AVATAR 引入离轨（off-policy）训练架构，通过分层重放缓冲区（Stratified Replay Buffer）保留并复用历史样本。缓冲区根据提示的平均奖励动态分区为 Easy / Medium / Hard 三个层级，优先保留高难度样本以维持训练组内的奖励多样性，从而强制维持非零优势。

**总体损失函数**：AVATAR 的优化目标为在轨损失与离轨损失的加权和：

$$
\mathcal{T}_{\mathrm{AVATAR}}(\theta) = \mathcal{T}_{\mathrm{on-policy}}(\theta) + \alpha \cdot \mathcal{T}_{\mathrm{off-policy}}(\theta)
$$

其中 $\alpha$ 控制离轨样本的贡献权重。离轨损失中的重要性采样比用于修正策略偏移：

$$
r_i^{\mathrm{off}}(\theta) = \frac{\pi_{\theta}(o_i \mid q)}{\pi_{\theta_{\mathrm{off}}}(o_i \mid q)}
$$

$\pi_{\theta}$ 为当前策略，$\pi_{\theta_{\mathrm{off}}}$ 为生成该离轨样本时的旧策略。通过该比值，AVATAR 在复用历史经验的同时保持策略更新的无偏性。

**提示生成机制（Hinting Mechanism）**：当特定提示长期处于困难分区且策略探索停滞时，AVATAR 触发外部教师模型（Qwen2.5-VL-72B）生成高层提示，帮助策略逃离局部最优。

### 4.2 时序优势塑造（TAS）

**动机**：标准 GRPO 对整个输出序列的所有令牌分配相同的标量优势 $A_i$（均匀信用分配），忽视了推理链中不同阶段的重要程度差异——序列开头的规划令牌和末尾的综合令牌对最终答案质量的影响远大于中间步骤。

**解决方案**：TAS 引入位置相关的抛物线加权函数，对每个令牌 $t$ 计算权重 $w_t$，调制得到成形优势：

$$
A_{i,t}^{\mathrm{TAS}} = w_t \cdot A_i
$$

其中 $A_i$ 为原始组相对优势（见公式 1），权重函数定义为：

$$
w_t = 1.0 + \lambda_{\mathrm{TAS}} \cdot (2\tilde{t} - 1)^2
$$

$\tilde{t} \in [0, 1]$ 为令牌在序列中的归一化位置，$\lambda_{\mathrm{TAS}}$ 控制抛物线的波幅。该函数呈 U 形：序列中间令牌权重为 $1.0$（不增不减），两端令牌权重为 $1.0 + \lambda_{\mathrm{TAS}}$（放大学习信号）。这一设计利用了 Transformer 的注意力汇聚效应——早期令牌作为规划锚点，晚期令牌合成答案——以极简单的无评判器加权显著提升关键步骤的学习效率。

### 4.3 优势估计与 VCRS 基线

**动机**：标准 GRPO 使用组内平均奖励 $\mu_R$ 作为优势估计基线。当引入离轨样本时，组内样本来源混杂，$\mu_R$ 的噪声增大，导致训练震荡。

**解决方案**：AVATAR 引入视频上下文参考分数（Video-Context Reference Score, VCRS），针对每个提示 $q$ 维护其最近 20 个在轨实例的移动平均奖励 $\overline{R}(q)$，作为离轨优势估计的稳定基线：

$$
A_{i,\mathrm{off}} = \frac{R(o_i) - \overline{R}(q)}{\sigma_{R,\mathrm{off}}}
$$

其中 $\sigma_{R,\mathrm{off}}$ 为离轨批次奖励的标准差。VCRS 替换了嘈杂的组均值 $\mu_R$，有效防止因批次噪声导致的训练震荡。

### 4.4 奖励函数体系

AVATAR 采用多阶段奖励组合（详见 Table 1），核心奖励组件包括：

- **格式奖励 $R_{\mathrm{format}}$**：二元奖励，验证输出是否遵循预定义的推理格式模板。正确为 $+1$，否则为 $-1$。
- **准确率奖励 $R_{\mathrm{acc}}$**：基于答案匹配的二元或部分评分。
- **自一致性奖励 $R_{\mathrm{self}}$**：对同一提示生成多个响应，通过多数投票共识判断一致性，鼓励稳定输出。
- **逐步评判奖励 $R_{\mathrm{judge}}$**：由外部 VLM 对推理链的每一步进行评判，提供细粒度反馈。消融实验表明，该奖励对推理密集型基准（Video-Holmes +1.4, MMVU +1.2）贡献最大。

不同训练阶段采用不同的奖励权重组合：Stage 1（视觉推理）使用 $0.5 \times R_{\mathrm{format}} + 0.5 \times R_{\mathrm{acc}}$；Stage 2（音视频推理）引入 $R_{\mathrm{self}}$；Stage 3（音频物体定位）进一步加入 $R_{\mathrm{judge}}$，形成递进式奖励课程。

## 实验与关键发现

### 主实验：音视频理解与视频推理基准

AVATAR 在两类核心基准上对基础模型进行了 RL 后训练，并与标准 GRPO 基线进行严格对比。所有提升幅度均附带通过 bootstrap 计算的 95% 置信区间。

**音视频理解基准（Table 2）**：以 Qwen2.5-Omni-7B 为基座，AVATAR 在 OmniBench 上取得 49.1 的准确率，相比基线的 44.2 提升 **+4.9**；而标准 GRPO 仅提升 +1.2，AVATAR 的增益约为 GRPO 的 4 倍。在 Ola-7B 基线上，AVATAR 同样带来 +1.9 的显著提升（45.3 → 47.2）。值得注意的是，AVATAR 使 Qwen2.5-Omni 超越了多个参数量更大的专有模型，验证了 RL 后训练在弥补架构差距方面的有效性。

**视频理解与推理基准（Table 3）**：AVATAR 在 MMVU 上取得 **+5.4**（60.2 → 65.6），在 Video-Holmes 上取得 **+4.5**（40.6 → 45.1），在 Video-MME 上取得 **+4.5**（58.3 → 62.8）。这三项基准分别侧重多模态知识推理、幻觉检测与时间因果推断，AVATAR 的全面提升表明其推理能力的改善具有跨任务泛化性。

### 组件消融：两大杠杆的独立贡献与协同

Table 4 的组件消融揭示了 AVATAR 各组件的因果作用：

![[assets/figures/papers/paper_list_l1041_https_arxiv_org_abs_2508_03100/figures/007_Table_4.jpg]]
*Table 4: Component-wise ablation demonstrating how each component addresses specific GRPO limitations. The stratified replay buffer resolves data inefficiency and vanishing advantages, TAS improves credit assignment, and hinting helps escape local optima*

- **分层重放缓冲区单独使用**（配合均匀信用分配）：在 OmniBench 上相比基础 GRPO 提升 +2.4，验证了离轨架构通过维持奖励多样性有效缓解了消失优势问题。
- **TAS 单独使用**（保持 GRPO 在轨策略）：在推理密集型基准 Video-MMMU 上提升 +2.2（Table 5），证明位置相关信用分配对长链推理的关键步骤具有独立增益。
- **完整 AVATAR**（离轨缓冲区 + TAS）：在所有基准上均超越仅含单个组件的配置，OmniBench 上达到 +4.9，验证了两大杠杆的协同效应——缓冲区解决“学什么样本”的问题，TAS 解决“样本内学哪里”的问题。

![[assets/figures/papers/paper_list_l1041_https_arxiv_org_abs_2508_03100/figures/010_Table_5.jpg]]
*Table 5: Ablation studies on training curriculum and advantage shaping strategies. TAS significantly outperforms uniform weights and inverse parabolic weights, validating our hypothesis that early and late reasoning phases are most critical*

Figure 4 从优势分布角度提供了机制层面的证据：标准 GRPO 的优势值高度集中在零附近（消失优势），而 AVATAR 通过重放缓冲区维持了多样化的双峰优势分布，确保了持续的学习信号。

### TAS 权重策略与推理长度的交互

Table 5 对比了 TAS 的抛物线加权与逆抛物线加权（即放大中间令牌、抑制两端）。逆抛物线加权导致性能显著下降，直接验证了“规划与综合阶段才是推理链的关键学习区域”这一核心假设。

Figure 6 进一步揭示了 TAS 的效果与推理序列长度的关系：在音视频和视频推理基准上，TAS 的增益随着推理序列长度的增加而增大。这意味着长链推理中，首尾令牌的规划与综合作用更为突出，TAS 的 U 形加权恰好放大了这些关键位置的学习信号。

### 奖励策略的逐阶段贡献

Table 10 的奖励组件消融展示了三阶段训练中逐步引入的奖励信号各自的累积增益：

![[assets/figures/papers/paper_list_l1041_https_arxiv_org_abs_2508_03100/figures/019_Table_10.jpg]]
*Table 10: Ablation studies of the reward strategy across three training stages. Stage 1 uses*

- **Stage 1**（R_acc + R_format）：建立基础准确率与格式合规性。
- **Stage 2**（加入 R_self，即多数投票一致性奖励）：通过自洽性信号提升推理一致性。
- **Stage 3**（加入 R_judge，即逐步评判奖励）：在推理密集型基准上贡献最大——Video-Holmes +1.4，MMVU +1.2——表明细粒度的步骤级反馈对复杂推理至关重要。

VCRS（Video-Context Reference Score）作为离轨优势的稳定基线，通过最近 20 个在轨实例的移动平均奖励替代嘈杂的组均值，防止了因批次噪声导致的训练震荡。

### 样本效率与训练动态

Figure 5 对比了 GRPO 与 AVATAR 的训练曲线：GRPO 呈现明显的振荡和不稳定，而 AVATAR 展现出平滑、持续上升的学习轨迹。AVATAR 约需标准 GRPO 20% 的生成完成数即可达到目标性能，实现了约 **5 倍样本效率**。

Figure 8 分析了在轨/离轨样本比例对性能的影响：在 6 个基准上，4:4 的均衡分配（4 个在轨样本 + 4 个离轨样本）达到最优性能。过多离轨数据会导致策略漂移，纯在轨训练则样本效率低下，均衡混合实现了两者的最佳权衡。

![[assets/figures/papers/paper_list_l1041_https_arxiv_org_abs_2508_03100/figures/014_Figure_8.jpg]]
*Figure 8: Performance vs. on-policy/off-policy sample ratio across six benchmarks. AVATAR achieves optimal performance with 4-4 split (4 on-policy, 4 off-policy samples), demonstrating that balanced mixing prevents both policy drift from excessive off-policy data and sample inefficiency from pure on-policy training*

Figure 11 的完整训练曲线显示，AVATAR 在训练初期经历短暂下降后迅速恢复并超越基线，这一“先降后升”的模式验证了离轨架构和 TAS 在探索-利用平衡中的有效性——模型在初期探索更广泛的策略空间，随后通过信用塑造收敛到更优解。

![[assets/figures/papers/paper_list_l1041_https_arxiv_org_abs_2508_03100/figures/023_Figure_11.jpg]]
*Figure 11: Training curves across audio-visual and video reasoning benchmarks. AVATAR demonstrates superior sample efficiency and final performance, particularly on challenging reasoning tasks. AVATAR’s initial dip, followed by a strong recovery, validates the effectiveness of our off-policy architecture and TAS for credit assignment*

### 失败模式与局限

尽管 AVATAR 在离线视频基准上表现强劲，但其提示机制依赖外部教师模型（Qwen2.5-VL-72B）生成高层提示以帮助策略逃离局部最优，这增加了额外的计算开销。此外，当前验证仅限于离线场景，扩展到实时流式音视频推理仍是一个开放挑战。

## 定位与知识库关联

### 1. 基线关系与改进脉络

AVATAR 直接构建在 **GRPO**（Group Relative Policy Optimization）之上，后者是当前多模态大语言模型强化学习的主流在轨（on-policy）方法。AVATAR 并非提出新的策略优化器，而是针对 GRPO 在长视频推理场景中暴露的三个结构性缺陷进行定向修补：

- **数据效率瓶颈**：GRPO 严格遵循在轨策略，每次更新后丢弃所有生成样本，导致昂贵的音视频推理数据无法复用。AVATAR 将其改造为**离轨（off-policy）架构**，通过分层重放缓冲区保留历史经验，将数据利用率提升约 5 倍（见 **Figure 5** 训练动态对比）。
- **消失优势（vanishing advantage）**：当组内所有响应的奖励相同时，GRPO 的优势值退化为零，模型停止学习。AVATAR 通过缓冲区采样强制维持组内奖励多样性，将优势分布从零附近的单峰死区转化为稳定的双峰分布（见 **Figure 4**）。
- **统一信用分配（uniform credit assignment）**：GRPO 对整个输出序列的所有令牌分配相同的标量优势，忽视了推理链中规划阶段（序列开头）和综合阶段（序列末尾）的关键性差异。AVATAR 引入**时序优势塑造（TAS）**，通过抛物线加权函数放大两端的梯度信号。

在实验对比中，AVATAR 以两种基础多模态模型为基线：**Qwen2.5-Omni-7B** 和 **Ola-7B**。在 OmniBench 上，标准 GRPO 仅能为 Qwen2.5-Omni 带来 +1.2 的提升，而 AVATAR 实现了 +4.9 的绝对增益，约为 GRPO 的 4 倍。这一差距直接验证了离轨架构与 TAS 的协同作用并非简单的增量改进，而是对 GRPO 训练瓶颈的系统性修补。

### 2. 方法谱系中的定位

从强化学习训练范式来看，AVATAR 处于以下谱系的交叉点：

| 维度 | 传统 GRPO | AVATAR |
|------|-----------|--------|
| 策略模式 | 纯在轨（on-policy） | 在轨-离轨混合架构 |
| 经验复用 | 无（立即丢弃） | 分层重放缓冲区，按难度分区保留 |
| 信用分配 | 统一标量优势 | 时序优势塑造（TAS），U 形加权 |
| 优势基线 | 组平均奖励 μ_R | VCRS 移动平均 + 组标准化 |
| 训练稳定性 | 易振荡（见 Figure 5a） | 平滑上升（见 Figure 5b） |

AVATAR 的离轨架构借鉴了深度强化学习中经典的经验重放（experience replay）思想，但其核心创新在于**难度分层**的缓冲区管理策略：根据提示的平均奖励将样本动态分区为 Easy/Medium/Hard，优先保留高难度样本以维持奖励多样性。这一设计与课程学习（curriculum learning）形成互补——缓冲区提供“回顾”机制，而三阶段训练流水线（Stage 1: Visual Reasoning → Stage 2: Audio-Visual Reasoning → Stage 3: Audio-Object Localization）提供“渐进”机制。

TAS 的抛物线加权函数 $w_t = 1.0 + \lambda_{\mathrm{TAS}} \cdot (2\tilde{t} - 1)^2$ 在形式上极为简洁，但其设计动机源于对 Transformer 注意力机制的洞察：早期令牌作为规划锚点汇聚全局信息，晚期令牌直接决定答案质量。这一“无评判器”（critic-free）的信用塑造策略避免了额外训练价值网络的复杂性，与近期纯语言推理中基于过程奖励模型（PRM）的方法形成对比——TAS 以极低的计算开销实现了对关键推理步骤的差异化学习信号。

### 3. 适用边界与局限

**已验证的适用场景**：
- 离线视频理解与推理基准（OmniBench、Video-Holmes、MMVU、Video-MME 等）
- 需要长链推理的音视频多模态任务
- 基于 Qwen2.5-Omni 和 Ola 架构的 7B 级模型

**明确的局限**：
1. **实时流式推理未覆盖**：当前 AVATAR 仅在离线视频基准上验证，扩展到实时流式音视频推理是一个有前景但尚未探索的方向。流式场景下的缓冲区管理和 TAS 权重设计可能需要根本性调整。
2. **提示机制依赖外部教师**：当特定提示长期困难且策略探索停滞时，AVATAR 触发外部教师模型（Qwen2.5-VL-72B）生成高层提示。这一机制引入了额外的推理开销，且提示质量依赖于教师模型的能力上限。
3. **超参数敏感性**：TAS 系数 $\lambda_{\mathrm{TAS}}$ 的最优值约为 0.3（见 **Figure 10**），在轨/离轨样本的最佳比例为 4:4（见 **Figure 8**），这些配置可能需要针对不同任务规模进行调整。

### 4. 开放问题与未来方向

1. **自适应缓冲区管理**：当前分层重放缓冲区的容量和分区比例是固定的。是否可以设计自适应机制，根据训练过程中的奖励分布变化动态调整分区边界和采样权重，以进一步优化样本效率？

2. **可学习的时序信用分配**：TAS 的抛物线权重函数是手工设计的。是否可以将其替换为可学习的、任务自适应的加权机制（例如基于小型注意力网络预测每个令牌的重要性），以在更复杂的推理结构中自动发现关键步骤？

3. **跨领域泛化**：AVATAR 的核心思想——离轨缓冲区 + 位置信用塑造——是否能够推广到纯语言推理、代码生成、数学证明等其他需要长链推理的领域？这些领域中“规划”和“综合”阶段的定义可能需要重新校准。

4. **与过程奖励模型的结合**：TAS 提供了一种无评判器的信用分配方案，而近期工作表明过程奖励模型（PRM）在数学推理中有效。两者的结合——以 PRM 提供细粒度步骤奖励，TAS 提供位置先验——是否能在长视频推理中产生互补增益，是一个值得探索的方向。

5. **更大规模模型的验证**：当前实验集中在 7B 级模型。AVATAR 的增益是否随模型规模扩大而保持或衰减（即是否存在“规模不变性”），需要进一步验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/AVATAR_Reinforcement_Learning_to_See_Hear_and_Reason_Over_Video.pdf]]
