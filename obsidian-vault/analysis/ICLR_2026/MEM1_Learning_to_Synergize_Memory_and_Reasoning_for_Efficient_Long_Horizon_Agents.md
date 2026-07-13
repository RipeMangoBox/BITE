---
title: "MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MEM1_Learning_to_Synergize_Memory_and_Reasoning_for_Efficient_Long_Horizon_Agents.pdf
project_link: null
code_link: https://github.com/MIT-MI/MEM1
openreview_forum_id: XY8AaxDSLb
aliases:
- MEM1
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过在每一轮交互中生成一个紧凑的内部状态 S_i，该状态联合完成对历史信息的记忆巩固和面向当前及未来查询的推理，并在下一轮之前丢弃旧的观察与中间产物，从而将内存使用量约束在近乎恒定的水平。"
primary_logic: "推理时生成的语言本身就兼具两种功能：为当前查询提供推理，同时提取并编码对未来任务至关重要的关键信息；将记忆巩固无缝融入这一推理过程，无需设计额外的外部模块或架构改动，即可使智能体在追求任务成功的同时自发习得高效的内存管理策略。"
claims:
- "MEM1-7B在16目标复合QA任务上准确率（EM=1.97）比Qwen2.5-14B-Instruct（EM=0.567）高出3.5倍，且峰值令牌仅为后者的27%，推理时间仅为29%。"
- "MEM1的RL训练显著优于SFT，SFT在6目标任务上分数仅0.088，而RL达到1.630；在8目标上SFT坍缩至0.027，RL继续提升至1.870。"
- "消融实验表明，将记忆与推理集成在统一内部状态中，相比使用单独的<summary>和<reasoning>标签，EM更高（2-obj: 0.709 vs 0.686），峰值令牌减少46%。"
- "Multi-Objective QA (16-Objective) 上 Exact Match (EM) = 1.97 (MEM1-QA)"
---

# MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents

> [!tip] 核心洞察
> 推理时生成的语言本身就兼具两种功能：为当前查询提供推理，同时提取并编码对未来任务至关重要的关键信息；将记忆巩固无缝融入这一推理过程，无需设计额外的外部模块或架构改动，即可使智能体在追求任务成功的同时自发习得高效的内存管理策略。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MEM1：学习记忆与推理协同以实现高效长程智能体 |
| 英文题名 | MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=XY8AaxDSLb) · [GitHub](https://github.com/MIT-MI/MEM1) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | MEM1 |
| Dataset | Multi-Objective QA (16-Objective), WebShop |

> [!tip] 效果简介
> - Multi-Objective QA (16-Objective) 上，Exact Match (EM) 为 1.97 (MEM1-QA)，对比 0.567 (Qwen2.5-14B-Instruct)，变化 1.403 (3.48x)。
> - Multi-Objective QA (16-Objective) 上，Peak Token Usage (×10²) 为 10.4 ± 0.09 (MEM1-QA)，对比 38.4 ± 0.71 (Qwen2.5-14B-Instruct)，变化 减少72.9%。
> - WebShop 上，Avg Final Reward 为 70.87 (MEM1-WebShop)，对比 70.80 (AgentLM-13B)，变化 +0.07 (并显著降低资源消耗)。

## 概要

### 问题瓶颈

长程多轮交互任务中，主流LLM智能体普遍采用全历史上下文提示策略，导致上下文长度随交互轮次无界增长，引发三重关键挑战：

1. **计算与内存开销线性扩张**：每轮推理需处理所有历史交互，推理计算量和峰值内存随轮次递增。
2. **上下文分布偏移引发性能崩塌**：当上下文超出模型训练长度时，分布偏移导致模型性能断崖式下降。
3. **冗余信息稀释注意力**：历史中大量无关信息占据注意力预算，加剧长程遗忘——即使关键信息仍存于上下文中，模型也难以有效利用。

### 核心方法

**MEM1** 是一个端到端的强化学习框架，其核心调控机制是：在每一轮交互中生成一个紧凑的内部状态 $S_i$，该状态联合完成对历史信息的记忆巩固和面向当前及未来查询的推理，并在下一轮之前丢弃旧的观察与中间产物，从而将内存使用量约束在近乎恒定的水平。

关键洞察在于：推理时生成的语言本身就兼具两种功能——为当前查询提供推理，同时提取并编码对未来任务至关重要的关键信息。将记忆巩固无缝融入这一推理过程，无需设计额外的外部模块或架构改动，即可使智能体在追求任务成功的同时自发习得高效的内存管理策略。

### 方法定位

MEM1 在方法谱系中占据独特位置：

- **相对于ReAct范式智能体**（如Search-R1, Jin et al., 2025）：MEM1 不保留全历史上下文，而是通过内部状态压缩实现恒定内存，从根本上解决了上下文膨胀问题。
- **相对于外部记忆模块方法**（如A-MEM, Xu et al., 2025）：MEM1 将记忆与推理统一在同一语言生成空间中，无需额外的向量数据库或摘要器，系统复杂度显著降低。
- **相对于监督微调智能体**（如Agent-FLAN, Chen et al., 2024）：MEM1 完全通过RL（PPO）端到端训练，仅使用任务完成的可验证奖励信号，未引入显式的内存效率奖励，却自发涌现出高效的内存管理行为。

### 主要结果

在16目标复合QA任务上，MEM1-7B 实现了 **Exact Match = 1.97**，相比 Qwen2.5-14B-Instruct（EM = 0.567）提升 **3.5倍**，同时峰值令牌消耗仅为后者的 **27%**，推理时间仅为 **29%**（Table 1）。在WebShop环境中，MEM1-WebShop 以 **70.87** 的最终奖励与 AgentLM-13B 持平，但峰值令牌消耗降低约 **2.8倍**（Table 2）。

消融实验揭示了三项决定性证据：(1) RL训练在所有多目标设置下均显著优于SFT，SFT在6目标以上性能崩塌（Table 5）；(2) 将记忆与推理集成在统一内部状态中，相比使用独立标签分离二者，在提升准确率的同时峰值令牌减少 **46%**（Table 6）；(3) 引入格式奖励虽能加速收敛，却阻碍了对有效推理策略的探索，最终EM从0.709降至0.466（Figure 6）。

### 局限与开放问题

MEM1 依赖可验证的规则化奖励函数，在奖励信号稀疏或隐含的开放性任务中难以直接迁移。模型在长程推理中仍存在幻觉（占失败案例的47.9%）和实体歧义（20.1%）等问题。未来的关键开放问题包括：如何将统一记忆-推理框架扩展到多模态输入和持续学习场景，以及如何在RL训练中显式引入内存效率约束以进一步提升性能。



### 长程交互中的上下文膨胀困境

在大语言模型（LLM）驱动的智能体执行多轮交互任务时，一种被广泛采用的范式是将所有历史交互——包括环境观察、模型动作和中间推理——全部追加到提示上下文中。这一做法虽然直观，却带来了一个根本性的瓶颈：**上下文长度随交互轮次无界增长**，进而引发三重连锁挑战。

首先，**推理计算与内存开销线性扩张**。每一轮交互都需要对不断增长的上下文执行自注意力计算，使得计算复杂度与内存占用随轮次递增，在长程任务中迅速变得不可承受。

其次，**超出训练长度的上下文分布偏移**导致模型性能断崖式下降。当上下文长度超出模型预训练或指令微调时所见的最大长度时，模型进入分布外区域，其注意力机制和位置编码均面临严重退化，表现为准确率急剧坍缩。

最后，**冗余信息稀释注意力，加剧长程遗忘**。即使关键信息仍存在于上下文中，模型也难以在大量无关历史中有效定位并利用这些信息。这一现象在多目标复杂任务中尤为突出——智能体需要在数轮甚至数十轮交互后，仍能准确回忆早期获取的事实以完成当前查询。

### 现有方法的局限

针对上述瓶颈，现有解决方案大致分为两类，但均存在显著不足。

一类是**基于外部模块的记忆管理方法**，如结合向量数据库的上下文压缩基线 **A-MEM**（Xu et al., 2025）。这类方法在策略网络之外引入独立的记忆模块（摘要器、检索器或压缩器），增加了系统复杂度，且记忆模块与策略网络的训练目标往往相互独立，难以形成协同优化。

另一类是**基于截断的被动遗忘策略**，即简单地丢弃超出窗口的早期上下文。这种做法虽然控制了内存开销，但会不可逆地丢失可能对后续任务至关重要的信息，在需要跨轮次信息整合的长程任务中表现不佳。

更深层的问题在于，**大多数现有智能体的训练范式并未将上下文管理纳入优化目标**。无论是基于行为克隆的监督微调（SFT），还是有限的强化学习对齐，模型都没有被激励去自主习得高效的内存使用策略。这使得智能体在长程任务中要么消耗过多资源，要么因信息丢失而失败，缺乏一种内生的、与任务求解协同进化的记忆管理能力。

### 本文动机：将记忆管理融入策略学习

本文的核心动机源于一个关键洞察：**推理时生成的语言本身就兼具两种功能——为当前查询提供推理，同时提取并编码对未来任务至关重要的关键信息**。如果能够将记忆巩固无缝融入推理过程，无需设计额外的外部模块或架构改动，就可以使智能体在追求任务成功的同时，自发习得高效的内存管理策略。

基于这一洞察，本文提出 **MEM1**——一个端到端的强化学习框架，其设计目标是在不引入额外模块的前提下，使智能体能够在近乎恒定的上下文大小下运行，同时保持甚至提升长程任务的求解能力。通过将记忆巩固与推理统一在同一语言生成空间中，MEM1 将上下文管理从一种工程层面的被动应对，转变为一个可被策略网络主动优化的行为维度。



## 核心方法与创新机理

MEM1 的核心创新在于将长程智能体的**记忆管理从架构负担转化为策略学习的内在产物**，通过三个相互耦合的机制实现近乎恒定的上下文开销。

### 统一记忆-推理空间：以语言生成为媒介的隐式记忆巩固

传统智能体将推理与记忆视为分离的子系统——推理链用于当前决策，记忆模块（摘要器、检索器或外部向量库）独立维护历史信息，二者通过显式接口交互，增加了系统复杂度和训练难度。MEM1 取消了这一分离：每一轮交互中，模型生成一个紧凑的内部状态 $S_i$，该状态**同时**承载对历史信息的记忆巩固和对当前及未来查询的推理。旧轮次的内部状态 $S_{i-1}$、动作 $A_{i-1}$ 和外部观察 $O_{i-1}$ 在下一轮开始前被从上下文中移除，仅保留 $S_i$ 作为智能体的唯一持久记忆。

这一设计的因果杠杆在于：推理时生成的自然语言本身就具备双重功能——为当前查询提供推理，同时提取并编码对未来任务至关重要的关键信息。记忆巩固被无缝融入推理过程，无需额外的外部模块或架构改动。消融实验证实了这一设计的有效性：将记忆与推理集成在统一内部状态中，相比使用独立的 `<summary>` 和 `<reasoning>` 标签，在 2 目标任务上 EM 从 0.686 提升至 0.709，峰值令牌消耗减少 46%（Table 6）。进一步分析表明，MEM1 的内部状态长度不随交互轮次显著增长，智能体能够自发丢弃无用信息并仅保留必要内容（Figure 5）。

### 端到端 RL 训练：以任务成功为唯一信号驱动记忆策略涌现

大多数智能体通过行为克隆（SFT）或结合少量 RL 进行对齐，上下文管理未被纳入优化目标。MEM1 完全通过强化学习（PPO）端到端训练，奖励信号仅为任务完成的最终结果（可验证奖励，如 Exact Match 或环境奖励），**未使用任何显式的内存效率奖励**。然而，智能体在追求任务成功的过程中，自发习得了高效的内存管理策略。

RL 训练相对于 SFT 的优势在递增多目标实验中表现得极为显著：SFT 在 6 目标任务上分数仅 0.088，而 RL 达到 1.630；在 8 目标上 SFT 坍缩至 0.027，RL 继续提升至 1.870（Table 5）。这表明 SFT 仅能模仿表面行为模式，无法应对长程场景中记忆管理所需的策略性权衡；RL 则通过探索与试错，使智能体学会在何时保留、何时丢弃信息，从而获得随任务复杂度增长的泛化鲁棒性。

### 掩码轨迹技术：在内存受限执行下实现正确的策略梯度计算

将各轮子轨迹直接拼接为全轨迹进行 RL 训练会导致策略梯度计算偏差，因为实际执行时各轮之间的上下文已被修剪。MEM1 引入掩码轨迹技术解决这一问题：将各轮子轨迹缝合为全轨迹 $\tau_{full}$，并施加二维注意力掩码，限制每个 token 在自注意力计算中只能看到所在轮及前一轮已保留的状态与观察，以及自身之前的 token：

$$\mathrm{Attn}_t = \mathbf{1}_{a \in \{ S_{i-1}, A_{i-1}, O_{i-1}, S_i, A_i, O_i \}} \times \mathbf{1}_{a \in \{ a_k | k \in \{1, 2, \ldots, t\} \}}$$

通过这一掩码，在压缩的全轨迹上计算出的策略概率与内存受限执行下的真实策略一致，从而支持正确的 PPO 梯度更新。该技术使得 MEM1 能够在不修改模型架构的前提下，将上下文管理策略端到端地纳入 RL 优化。

### 与基线方法的关键差异

| 改进维度 | 基线方法 | MEM1 |
|---------|---------|------|
| 上下文管理策略 | 全历史追加，上下文线性增长 | 每轮生成新内部状态后丢弃旧信息，上下文近乎恒定 |
| 记忆与推理耦合 | 分离的模块（摘要器/检索器 + 策略网络） | 统一在同一语言生成空间中，无额外模块 |
| 训练目标与算法 | 以 SFT 为主，上下文管理未被优化 | 完全 RL 端到端训练，仅以任务成功为信号 |

在 16 目标复合 QA 任务上，MEM1-7B 的 EM 达到 1.97，比 Qwen2.5-14B-Instruct（EM=0.567）高出 3.5 倍，且峰值令牌仅为后者的 27%，推理时间仅为 29%（Table 1）。在 WebShop 环境中，MEM1-WebShop 以最低的峰值令牌（0.81×10³）和依赖度（0.15×10⁶）达到最优平均奖励 70.87（Table 2）。这些结果表明，将记忆管理从显式设计转向策略学习的涌现产物，是实现长程高效智能体的有效路径。



![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_XY8AaxDSLb/figures/001_Figure_1.jpg]]
*Figure 1: (Top): the RL pipeline used to train MEM1. (Bottom left): The evolution of context in MEM1–old internal states (S), query/answer (A), and external information (O) are cleared as new states enter the context during rollout. (Bottom right): the 2D attention mask used during the objective computation stage. The mask is applied during the forward pass to compute action log-probabilities for the actor model and state value estimates for the critic model. During policy update, an information mask is then applied to mask out O tokens not generated by the model itself*

MEM1 的整体设计围绕一个核心因果机制展开：**在每一轮交互中生成一个紧凑的内部状态 $S_i$，该状态同时完成对历史信息的记忆巩固和面向当前及未来查询的推理，并在下一轮之前丢弃旧的观察与中间产物**，从而将内存使用量约束在近乎恒定的水平。这一机制通过端到端的强化学习训练习得，无需引入额外的外部记忆模块或架构改动。

### 核心流水线

MEM1 的推理与训练流水线由四个紧密耦合的模块构成，其整体结构如 Figure 1 所示：

**1. 内部状态巩固（$S_i$ 生成）**
在每一轮 $i$ 开始时，模型基于上一轮的内部状态 $S_{i-1}$、动作 $A_{i-1}$ 和环境观察 $O_{i-1}$，生成新的压缩内部状态 $S_i$。$S_i$ 同时承载两项功能：对历史关键信息的记忆编码，以及面向当前查询的推理链。这种“记忆即推理”的统一表征是整个框架的核心创新——推理时生成的语言本身就兼具提取关键信息与进行逻辑推导的双重能力。

**2. 动作生成（$A_i$ 生成）**
基于当前内部状态 $S_i$，模型产生查询（query）或最终答案（answer），并执行相应的工具调用（如搜索引擎查询）。动作的类型取决于任务设定：在多目标 QA 任务中，$A_i$ 可以是子问题的搜索查询或最终答案；在 WebShop 环境中，$A_i$ 对应网页导航操作。

**3. 上下文修剪**
每一轮结束后，系统从上下文窗口中移除不再需要的旧状态 $S_{i-1}$、旧动作 $A_{i-1}$ 和外部观察 $O_{i-1}$，仅保留最新状态 $S_i$ 作为下一轮的输入。这一修剪操作确保上下文长度不随交互轮次线性增长，是实现近乎恒定内存占用的关键工程手段。

**4. 掩码轨迹构建（用于 RL 训练）**
在训练阶段，各轮子轨迹 $\tau_1, \tau_2, \dots, \tau_n$ 被缝合为一条完整轨迹 $\tau_{full}$，并施加二维注意力掩码。该掩码限制每个 token 在自注意力计算中只能看到所在轮及前一轮已保留的状态与观察，以及自身之前的 token，从而在内存受限执行下仍能正确计算策略梯度，支持 PPO 训练。

### 训练范式

MEM1 完全通过强化学习（PPO）端到端训练，优化目标为最大化任务完成的累积奖励期望值：

$$\operatorname*{argmax}_{\theta} \mathbb{E}_{Q \in \mathcal{Q}, \tau \sim \pi_{\theta, Q}} \Big[ \sum_{(a_t, s_t) \in \tau} r(s_t) \Big]$$

奖励信号 $r(s_t)$ 仅来自任务完成的最终结果（如 QA 任务中的 Exact Match、WebShop 中的环境奖励），不包含任何显式的内存效率奖励。然而，智能体在追求任务成功的过程中自发习得了高效的内存管理策略——这正是将记忆巩固与推理统一在同一语言生成空间中所带来的涌现效应。

### 与基线方法的根本差异

相较于现有智能体框架，MEM1 在三个关键维度上做出了根本性改变：

| 维度 | 基线方法 | MEM1 |
|------|---------|------|
| 上下文管理 | 全历史上下文追加，长度随轮次线性增长 | 每轮生成新状态后丢弃旧信息，上下文近乎恒定 |
| 记忆-推理耦合 | 记忆模块（摘要器、检索器）独立于策略网络 | 统一在同一语言生成空间中，无需额外模块 |
| 训练目标 | 以行为克隆（SFT）为主，上下文管理未被纳入优化 | 完全通过 RL 端到端训练，记忆管理作为策略的一部分被隐式优化 |

其中，与 **A-MEM**（Xu et al., 2025）的对比尤为关键：A-MEM 结合外部向量数据库进行上下文压缩，而 MEM1 完全摒弃了外部记忆模块，仅依靠模型自身生成的内部状态完成记忆管理。消融实验表明，这种集成设计在 2 目标任务上不仅 EM 更高（0.709 vs 0.686），峰值令牌消耗更减少了 46%。



### 3.1 内部状态巩固模块 (Internal State Consolidation)

MEM1 的核心机制是在每一轮交互中生成一个紧凑的**内部状态** $S_i$，该状态同时承担两项功能：对历史信息进行记忆巩固，以及为当前及未来的查询提供推理链。具体而言，在第 $i$ 轮起始时，模型基于上一轮的内部状态 $S_{i-1}$、上一轮的动作 $A_{i-1}$ 以及环境返回的观察 $O_{i-1}$，生成新的内部状态 $S_i$。随后，模型根据 $S_i$ 生成当前轮的动作 $A_i$（查询或最终答案）。在进入下一轮之前，旧的 $(S_{i-1}, A_{i-1}, O_{i-1})$ 被从上下文窗口中移除，仅保留 $S_i$ 作为智能体的唯一记忆。

这一设计的因果机制在于：推理时生成的语言本身就兼具“为当前查询提供推理”和“提取并编码对未来任务至关重要的关键信息”两种功能。将记忆巩固无缝融入推理过程，无需设计额外的外部模块或架构改动，即可使智能体在追求任务成功的同时自发习得高效的内存管理策略。消融实验证实，将记忆与推理集成在统一内部状态中，相比使用独立的 `<summary>` 与 `<reasoning>` 标签，在 2 目标任务上 Exact Match 更高（0.709 vs 0.686），且峰值令牌消耗减少 46%（Table 6, Appendix F.3）。

### 3.2 掩码轨迹构建模块 (Masked Trajectory Construction)

由于 MEM1 在 rollout 时每轮仅保留有限的上下文窗口，若直接将各轮子轨迹拼接为全轨迹进行训练，会导致策略梯度计算与内存受限执行时的条件概率分布不一致。为此，MEM1 引入**掩码轨迹**技术：将各轮子轨迹 $\tau_1, \tau_2, \dots, \tau_n$ 缝合为全轨迹 $\tau_{full}$，并施加二维注意力掩码，使得每个 token 在自注意力计算中只能看到所在轮及前一轮已保留的状态与观察，以及自身之前的 token。

具体地，第 $i$ 轮第 $t$ 个 token 的注意力掩码定义为：

$$
\mathrm{Attn}_t = \mathbf{1}_{a \in \{ S_{i-1}, A_{i-1}, O_{i-1}, S_i, A_i, O_i \}} \times \mathbf{1}_{a \in \{ a_k \mid k \in \{1, 2, \ldots, t\} \}}
$$

其中第一项限制 token 只能关注当前轮和前一轮保留的上下文元素，第二项限制只能关注自身及之前的 token。基于此掩码，第 $i$ 轮的策略概率通过在全轨迹上应用掩码计算得到：

$$
\pi_{\theta, Q, \tau_i}(a_t, s_t) = \pi_{\theta, Q, \tau_{full}}(a_t, s_t \times \mathrm{Attn}_t)
$$

完整的掩码序列为 $\mathbf{Mask} = (\mathrm{Attn}_1, \dots, \mathrm{Attn}_T)$，在 PPO 训练的前向传播中用于计算 actor 模型的动作对数概率和 critic 模型的状态价值估计。需注意，由于实现中未对每个断点位置复制 `<IS>` 标记并调整位置 ID，因此未能完全恢复原始拆分子轨迹时的注意力模式，但实验表明这种近似影响很小。

### 3.3 RL 优化目标

MEM1 完全通过强化学习端到端训练，优化目标为最大化在任务集 $\mathcal{Q}$ 上采样轨迹的累积奖励期望：

$$
\operatorname*{argmax}_{\theta} \mathbb{E}_{Q \in \mathcal{Q}, \tau \sim \pi_{\theta, Q}} \Big[ \sum_{(a_t, s_t) \in \tau} r(s_t) \Big]
$$

其中奖励 $r(s_t)$ 仅取决于状态 $s_t$，在 QA 任务中使用 Exact Match 作为可验证奖励，在 WebShop 中使用环境奖励。训练仅在 2 目标复合任务上进行，未使用显式的内存效率奖励，但智能体在 RL 过程中自发习得了近乎恒定的内存使用策略。消融实验表明，RL 训练在所有多目标设置下均显著优于 SFT：6 目标时 RL 的 EM 为 1.630，而 SFT 仅为 0.088；8 目标时 SFT 坍缩至 0.027，RL 继续提升至 1.870（Table 5, Appendix F.1）。



## 实验与关键发现

### 核心性能与效率结果

MEM1在多目标复合QA任务上展现出显著的性能与效率双重优势。在最具挑战性的16目标设定下，MEM1-7B的精确匹配得分（EM=1.97）达到Qwen2.5-14B-Instruct（EM=0.567）的3.5倍，而峰值令牌消耗仅为后者的27%（10.4×10² vs 38.4×10²），推理时间仅为其29%。这一结果的核心驱动力在于MEM1的上下文管理策略：基线模型将全部历史交互追加至提示中，导致上下文长度随轮次线性膨胀，不仅引发计算开销剧增，更因超出训练长度的分布偏移而性能坍缩——Search-R1、DeepResearcher等基线在16目标下EM已趋近于零。相比之下，MEM1通过每轮生成压缩内部状态S_i并丢弃旧观察，将内存使用约束在近乎恒定水平，从而在长程任务中同时获得准确率提升与资源节省（Table 1, Figure 2）。


![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_XY8AaxDSLb/figures/003_Table_1.jpg]]
*Table 1: Comparison of models on multi-objective multi-turn QA tasks. Arrows indicate the desired directions. Numbers in red indicate collapsed model behavior (extremely low performance). (truncate) means using MEM1’s prompt and rollout pipeline. (A-MEM) means using MEM1’s prompt and rollout pipeline with A-Mem’s external memory module (Xu et al., 2025). MEM1-QA means MEM1 trained on 2-objective QA task. Dependency scores are presented in due to limited space*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_XY8AaxDSLb/figures/002_Figure_2.jpg]]
*Figure 2: Performance and efficiency scaling of MEM1 (trained on 2-objective QA) with the number of objectives in multi-objective tasks. MEM1 outperforms the other models and baselines while having an almost constant scaling in memory usage. Note that at 16-objective, the context of baseline models does not increase anymore since their model performance has degraded (some collapsed)*

在WebShop环境中，MEM1-WebShop以平均最终奖励70.87达到与AgentLM-13B（70.80）相当的水平，但峰值令牌消耗（0.81×10³）仅为AgentLM-7B（2.24×10³）的约36%，推理时间（2.61s）也显著低于同类模型。值得注意的是，Agent-R虽报告了更高的奖励分数，但其为闭源模型，推理效率指标无法直接对比（Table 2）。


![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_XY8AaxDSLb/figures/004_Table_2.jpg]]
*Table 2: The experimental results for WebShop. For a fair comparison, we do not report GPT’s inference time. For Agent-R, scores are taken from the original paper, as the model is closed source. MEM1-WebShop means MEM1 trained on WebShop environment*

### 跨环境迁移泛化

MEM1在分布外单目标任务上的迁移能力进一步验证了其学习到的记忆管理策略的通用性。在Wiki RAG任务上，MEM1-QA以最低的峰值令牌（5.63×10²）和依赖度（0.76×10）实现了与专门针对该任务训练的Search-R1可比的准确率。在在线Web QA任务上，MEM1-QA同样展现出效率优势（峰值令牌5.79×10²），尽管DeepResearcher专门针对该任务以F1为目标进行训练，MEM1的迁移性能仍具竞争力。这一泛化能力源于RL训练赋予智能体的策略灵活性——模型学会了在内部状态中自主决定保留何种信息，而非依赖任务特定的记忆模板（Table 3）。

### 消融实验与关键设计验证

**RL vs SFT训练范式。** 在递增多目标数的消融实验中，RL训练的MEM1在所有设定下均显著优于SFT基线，且优势随目标数增加而急剧扩大：在6目标时RL的EM为1.630，而SFT仅0.088（差距17.5倍）；在8目标时SFT进一步坍缩至0.027，RL则继续提升至1.870。SFT在6目标以上的性能崩塌表明，行为克隆无法赋予智能体在长程上下文中自主管理记忆的能力——它只能模仿训练轨迹的表面模式，而无法习得压缩与推理之间的深层协同策略（Table 5, Appendix F.1）。


![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_XY8AaxDSLb/figures/014_Table_5.jpg]]
*Table 5: Comparison of RL and SFT on increasing number of multi-turn questions. Exact match scores ↑ is better. Gap shows absolute difference. Red numbers show collapsed SFT behavior*

**格式奖励的影响。** 引入格式奖励（强制使用`<IS>`等标签）虽能加速训练初期的收敛，但最终阻碍了对有效推理策略的探索：EM从0.709降至0.466，且模型生成的响应更短。这表明格式约束限制了智能体在内部状态中自由组织推理链的空间，削弱了记忆巩固与推理融合的核心优势（Figure 6, Appendix F.2）。

**记忆与推理的集成vs分离。** 将记忆巩固与推理统一在单一内部状态中，相比使用独立的`<summary>`和`<reasoning>`标签，在2目标任务上EM更高（0.709 vs 0.686），峰值令牌减少46%（6.40×10² vs 11.80×10²）。在8目标和16目标设定下，集成设计的准确率与效率优势持续保持。这一结果验证了核心设计洞察：推理时生成的语言本身即可兼具提取关键信息与辅助当前决策的双重功能，强行分离二者反而引入冗余并削弱协同效应（Table 6, Appendix F.3）。


![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_XY8AaxDSLb/figures/016_Table_6.jpg]]
*Table 6: Ablation study comparing integrated versus separated memory and reasoning. Peak token counts are reported in units of ×102, with standard deviations in parentheses*

**内部状态长度稳定性。** 对MEM1在2目标和8目标任务中内部状态长度的分析显示，平均状态长度不随交互轮次显著增长，表明智能体有效习得了丢弃无用信息、仅保留必要内容的自发压缩行为。这一涌现特性是RL训练的直接产物——奖励信号仅针对任务完成，内存效率作为策略优化的副产品自然产生（Figure 5, Appendix E.2）。

### 失败模式分析

在2目标QA设定下的失败案例统计揭示了MEM1的主要局限性。**幻觉替代搜索**（Hallucination Instead of Search）是最主要的失败模式，占比47.9%：当外部信息源不包含答案时，模型倾向于基于内部知识编造答案，而非继续搜索或明确表示无法回答。**实体歧义**（Entity Ambiguity）占20.1%，出现在需要精细区分同名实体或理解上下文指代的场景。其余失败模式包括过早终止搜索、信息整合错误等。这些失败模式表明，尽管MEM1在内存效率上取得了突破，但在长程推理中的事实可靠性仍有提升空间，尤其在信息源不完整或存在歧义时（Table 7, Appendix F.4）。

### 实验公平性说明

所有推理效率指标（推理时间、峰值令牌）均在相同硬件环境（单个H200 GPU，10并发线程，vLLM推理框架）下测量。在16目标实验中，部分基线模型已性能坍缩（EM接近0），此时其上下文增长停止，效率对比需结合这一因素解读。MEM1训练仅使用2目标复合任务，与Search-R1等专门针对单目标训练的基线相比，在小目标数上可比肩，在大目标数上大幅超越，凸显了泛化能力而非训练数据优势。



## 定位与知识库关联

### 1. 方法谱系：从全上下文提示到统一记忆-推理框架

MEM1 的核心定位在于对长程智能体**上下文管理策略**的根本性重构。传统 LLM 智能体（包括基于 ReAct 范式的 **Search-R1**（Jin et al., 2025）和 **DeepResearcher**（Zheng et al., 2025））普遍采用“全历史追加”策略：将每一轮交互的观察、动作和思考产物全部追加到提示中，导致上下文长度随交互轮次线性增长。这一策略带来三重连锁瓶颈：（1）推理计算与内存开销线性扩张；（2）超出训练长度的上下文分布偏移引发模型性能断崖式下降；（3）冗余信息稀释注意力，加剧长程遗忘——即使关键信息仍存于上下文中也难以有效利用。

在这条技术路线上，已有工作尝试通过**外部记忆模块**缓解上下文膨胀问题。**A-MEM**（Xu et al., 2025）结合外部向量数据库进行上下文压缩，属于“推理-记忆分离”范式：记忆模块（摘要器、检索器）独立于策略网络设计和训练。然而，这类方法引入了额外的系统复杂度，且记忆压缩与推理过程缺乏协同优化。

MEM1 的突破在于将**记忆巩固无缝融入推理过程**，形成统一的内部状态生成机制。其关键设计决策体现在三个维度：

- **上下文管理策略**：从“全历史追加”转变为“每回合生成新内部状态 S_i 后丢弃旧状态”。S_i 联合完成对历史信息的记忆巩固和面向当前及未来查询的推理，使上下文始终保持近乎恒定（Section 3.1, Figure 1 bottom left）。

- **记忆与推理的耦合方式**：从“模块分离”转变为“统一语言生成空间”。内部状态 S_i 同时承载工作记忆与推理链，无需额外的摘要器或检索器模块。消融实验确证了这一设计的优势：相比使用独立 `<summary>` 与 `<reasoning>` 标签的分离方案，集成设计在 2 目标任务上 EM 更高（0.709 vs 0.686），峰值令牌减少 46%（Table 6, Appendix F.3）。

- **训练目标与算法**：从“行为克隆（SFT）为主”转变为“完全端到端 RL（PPO）训练”。奖励信号仅为任务完成的最终结果（可验证奖励），未使用显式的内存效率奖励；模型在追求任务成功的过程中自发习得高效的内存管理策略（Section 3.2, Section 4.1）。

### 2. 与具体基线工作的关系

在**多目标复合 QA** 场景中，MEM1-7B 与以下工作形成直接对比：

- **Qwen2.5-14B-Instruct**（Yang et al., 2024）：作为大规模指令微调模型的强基准，在 16 目标复合 QA 任务上 EM 仅为 0.567，而 MEM1-7B 达到 1.97（3.5× 提升），且峰值令牌仅为后者的 27%，推理时间仅为 29%（Table 1, Section 4.2）。这一对比凸显了 MEM1 在参数规模减半的条件下仍能实现压倒性的性能与效率优势。

- **Search-R1**（Jin et al., 2025）：专门针对单目标 QA 训练的 RL 智能体。在 16 目标任务上，Search-R1 原始版性能已崩溃（EM 接近 0），而 MEM1（仅用 2 目标训练）仍保持高性能，凸显了泛化能力的质变（Table 1, Figure 2）。

- **DeepResearcher**（Zheng et al., 2025）：使用 RL 训练的深度搜索智能体，专门优化单目标在线 Web-QA。在迁移实验中，MEM1-QA 在分布外的单目标 Wiki RAG 和在线 Web QA 任务上均展现出显著的效率优势，同时保持可比的有效性（Table 3）。

在 **WebShop** 环境中：

- **AgentLM-13B**（Zeng et al., 2023）和 **Agent-FLAN**（Chen et al., 2024）：分别代表针对 WebShop 微调的中等规模智能体和指令微调智能体。MEM1-WebShop 以最低的峰值令牌（0.81×10³）和依赖度（0.15×10⁶）达到最优平均最终奖励 70.87，而 AgentLM-7B 的峰值令牌为 2.24×10³（Table 2）。

- **Agent-R**（Yuan et al., 2025）：基于 RL 的 WebShop 智能体，但为闭源模型，其奖励分数取自原论文，推理时间与峰值令牌无法直接对比（Table 2 注释）。

### 3. 适用边界与关键局限

MEM1 的有效性建立在以下前提之上，其适用边界也由此界定：

**奖励信号的可验证性**。MEM1 完全依赖可验证的规则化奖励函数（如 EM、环境奖励）进行 RL 训练。在奖励信号稀疏、延迟或隐含的开放性任务中，当前训练方法难以直接迁移。这是方法泛化面临的核心瓶颈。

**训练-测试的目标数分布偏移**。MEM1 仅在 2 目标复合任务上进行训练，虽然泛化至 16 目标效果优异（EM 从 0.709 增至 1.97），但在更长目标序列、更强分布偏移下的鲁棒性未经系统验证。SFT 基线在 6 目标以上性能崩塌（EM 从 0.088 降至 0.027）的现象（Table 5, Appendix F.1）暗示，RL 训练的泛化能力虽显著优于 SFT，但其上限尚未探明。

**长程推理中的幻觉与实体歧义**。失败案例分析显示，在 2 目标设置下，47.9% 的失败源于“幻觉替代搜索”（模型虚构答案而非执行检索），20.1% 源于实体歧义（Table 7）。这表明 MEM1 在信息源不包含答案或需要精细区分同名实体时仍存在脆弱性。

**掩码注意力的近似实现**。由于未对每个断点位置复制 `<IS>` 标记并调整位置 ID，掩码注意力未能完全恢复原始拆分子轨迹时的注意力模式，但实验表明这种近似的影响很小（Section 3.2 讨论）。

### 4. 开放问题与未来方向

基于上述局限，以下开放问题值得进一步探索：

1. **稀疏奖励环境的训练方法**：如何在奖励信号稀疏、延迟或隐含的开放性环境中训练 MEM1 智能体，使其自主进行记忆管理？这可能需要引入内在激励或课程学习机制。

2. **多模态与持续学习扩展**：能否将 MEM1 的统一记忆-推理框架扩展到多模态输入（如图像、网页截图）或需要持续学习与知识更新的场景？当前框架仅处理文本输入，多模态场景下的压缩与推理协同机制有待设计。

3. **超长周期的内存优化**：是否可以结合动态缓存及压缩策略，进一步降低内部状态的长度以适应超长周期（如数百轮）的交互？Figure 5 显示内部状态长度在 2 目标和 8 目标下均保持稳定，但其在极端长程下的行为未经验证。

4. **显式内存效率约束**：如何在当前 RL 训练中显式引入对内存效率的约束或奖励，从而在不牺牲任务性能的前提下进一步提升效率？格式奖励实验（Figure 6, Appendix F.2）表明，不当的显式约束可能阻碍有效推理策略的探索，这提示需要设计更精细的效率引导机制。



## 原文 PDF

![[paperPDFs/ICLR_2026/MEM1_Learning_to_Synergize_Memory_and_Reasoning_for_Efficient_Long_Horizon_Agents.pdf]]
