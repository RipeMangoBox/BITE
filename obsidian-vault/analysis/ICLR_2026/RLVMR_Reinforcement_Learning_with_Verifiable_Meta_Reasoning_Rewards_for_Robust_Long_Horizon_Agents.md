---
title: "RLVMR: Reinforcement Learning with Verifiable Meta-Reasoning Rewards for Robust Long-Horizon Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RLVMR_Reinforcement_Learning_with_Verifiable_Meta_Reasoning_Rewards_for_Robust_Long_Horizon_Agents.pdf
project_link: null
code_link: null
openreview_forum_id: cTbAevdwBE
aliases:
- RLVMR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入基于可验证元推理行为的过程级密集奖励（如规划、探索、反思/监控），并采用冷启动有监督微调与带标签组归一化的群组相对策略优化（GRPO-MR），组合最终结果奖励与推理过程奖励，直接塑造更稳健的推理过程。"
primary_logic: "通过将元认知理论中的“规划-探索-反思-监控”等高层认知技能操作化为可验证的推理标签，并提供程序化规则奖励，RLVMR 指导智能体学习“如何推理”，而非仅学习“如何成功”，从而同时提升任务成功率和推理质量，缓解无效探索问题。"
claims:
- "GRPO虽然提升泛化成功率，但带来了严重的推理低效：在ALFWorld L2任务上，7B GRPO的重复动作率高达31.2%，而SFT模型的效率则很脆弱。"
- "RLVMR在ALFWorld最难的未被见任务分割(L2)上取得83.6%成功率(7B)，远超最强基线GiGPO(67.2%)和GRPO(52.3%)，且重复动作率和无效动作率大幅下降。"
- "消融实验表明，移除元推理奖励(A^MC)导致ALFWorld L2成功率从56.3%降至45.3%，而移除结果奖励(A^T)则使成功率崩溃至12.5%，证实过程奖励不可或缺且需与结果奖励协同。"
- "ALFWorld 上 Success Rate (%) = 83.6"
---

# RLVMR: Reinforcement Learning with Verifiable Meta-Reasoning Rewards for Robust Long-Horizon Agents

> [!tip] 核心洞察
> 通过将元认知理论中的“规划-探索-反思-监控”等高层认知技能操作化为可验证的推理标签，并提供程序化规则奖励，RLVMR 指导智能体学习“如何推理”，而非仅学习“如何成功”，从而同时提升任务成功率和推理质量，缓解无效探索问题。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | RLVMR：基于可验证元推理奖励的强化学习，用于构建鲁棒的长周期智能体 |
| 英文题名 | RLVMR: Reinforcement Learning with Verifiable Meta-Reasoning Rewards for Robust Long-Horizon Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=cTbAevdwBE) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | RLVMR |
| Dataset | ALFWorld, ScienceWorld |

> [!tip] 效果简介
> - ALFWorld 上，Success Rate (%) 为 83.6，对比 67.2，变化 +16.4。
> - ALFWorld 上，Success Rate (%) 为 83.6，对比 52.3，变化 +31.3。
> - ScienceWorld 上，Success Rate (%) 为 32.2，对比 26.6，变化 +5.6。

## 概要

### 问题核心

在长周期（long-horizon）文本交互任务中，当前主流的**端到端强化学习范式**（如 GRPO）仅以稀疏的最终任务成功信号作为奖励。这种方式虽然能提升策略在未见任务上的泛化成功率，却带来了严重的**“无效探索”**问题：智能体的推理路径充斥着冗余、低效甚至逻辑矛盾的中间步骤。实验表明，在 ALFWorld L2 任务上，7B 模型的 GRPO 策略重复动作率高达 31.2%，且增大模型规模并不能缓解这一推理低效。与之相对，监督微调（SFT）策略虽然动作效率较高，但其泛化能力极为脆弱——在 L2 未见任务上的成功率从 L0 的 63.3% 骤降至 37.5%。这一“高效但脆弱”与“泛化但低效”之间的根本性权衡，构成了长周期智能体推理能力提升的核心瓶颈。

### 核心方法

**RLVMR**（Reinforcement Learning with Verifiable Meta-Reasoning Rewards）的核心思路是：将元认知理论中的高层认知技能——**规划、探索、反思、监控**——操作化为可验证的推理标签，并通过程序化规则提供过程级密集奖励，直接塑造智能体的推理过程质量。具体而言，RLVMR 在标准 ReAct 框架中引入四类元推理标签（`<planning>`、`<explore>`、`<reflection>`、`<monitor>`），并设计了一套**复合优势函数**：将基于最终结果的轨迹级优势与在同一标签组内归一化的元推理级优势进行加权组合。训练采用两阶段范式——先利用约 200 条教师模型标注的成功轨迹进行冷启动 SFT，再通过带标签组归一化的群组相对策略优化（GRPO-MR）进行端到端强化学习。

### 核心结论

在 ALFWorld 和 ScienceWorld 两个长周期文本交互基准上，RLVMR 在所有模型规模和任务难度下均取得了最优结果。在 ALFWorld 最难的 L2 未见任务分割上，7B 模型的成功率达到 **83.6%**，较最强基线 GiGPO 提升 16.4 个百分点，较标准 GRPO 提升 31.3 个百分点；同时重复动作率从 27.1% 大幅降至 5.7%。消融实验证实，元推理过程奖励与最终结果奖励缺一不可——移除元推理奖励导致成功率下降 11 个百分点，移除结果奖励则使成功率崩溃至 12.5%。反思和探索标签对错误恢复与搜索效率的贡献尤为关键。

### 方法谱系与知识库定位

RLVMR 定位于**基于文本交互的 LLM 智能体强化学习**领域，其方法谱系可沿以下维度展开：

| 维度 | 基线方法 | RLVMR 的改进 |
|------|----------|-------------|
| **奖励信号** | 仅稀疏最终结果奖励（GRPO, Shao et al., 2024） | 结果奖励 + 密集可验证元推理奖励（规划/探索/反思/监控） |
| **优势函数构造** | 基于整条轨迹结果的组内归一化（GRPO） | 轨迹级优势与标签内归一化元推理优势的加权组合 |
| **训练范式** | 直接从环境交互进行端到端 RL（GRPO, GiGPO） | 冷启动 SFT（~200 条标注轨迹）+ 端到端 RL |
| **策略优化** | 标准 GRPO（Shao et al., 2024） | GRPO-MR：标签内分组归一化 + 复合优势 + KL 正则化 |

与离线 RL 方法（如 **ETO**, Song et al., 2024；**GLIDER**, Hu et al., 2025）相比，RLVMR 通过在线交互与过程级奖励塑形实现了更强的泛化能力；与端到端在线 RL 方法（如 **GiGPO**, Feng et al., 2025）相比，RLVMR 通过显式的元推理结构引导，在提升成功率的同时大幅降低了推理低效行为。



### 长周期智能体中的推理困境

基于大语言模型（LLM）的智能体在长周期交互任务（如具身导航、科学实验模拟）中面临一个核心挑战：如何学习稳健的推理过程，而不仅仅是达成最终目标。现有范式主要分为两条技术路线，但各自暴露出根本性缺陷。

**监督微调（SFT）的脆弱效率。** 通过模仿专家轨迹进行微调，SFT 模型在已见任务（ALFWorld L0）上可取得 63.3% 的成功率，表现出较高的执行效率。然而，这种效率极为脆弱——当任务分布发生偏移时，成功率骤降至 37.5%（L2 分割），暴露出严重的泛化不足问题（Figure 2）。SFT 学到的是表层的行为模式，而非可迁移的推理能力。

**端到端强化学习的低效泛化。** 以 GRPO（Shao et al., 2024）为代表的在线 RL 方法通过环境交互直接优化任务成功率，在未见任务上展现出更强的泛化能力。然而，这种泛化是以显著的推理低效为代价的：在 ALFWorld L2 任务上，7B 模型的 GRPO 重复动作率高达 31.2%（Figure 2(f)）。更值得警惕的是，增大模型规模非但不能缓解这一问题，反而使重复动作率从 1.5B 的 27.1% 升至 7B 的 31.2%，表明单纯扩大模型容量无法自动修复底层推理缺陷。

### 根本瓶颈：结果导向奖励的无效探索

上述困境的根源在于，仅依赖稀疏的最终结果奖励 $R(\tau)$ 进行优化的 RL 范式，其优化目标为：

$$\operatorname*{max}_{\theta} \operatorname{\mathbb{E}}_{\tau \sim \pi_{\theta}} \left[ R(\tau) \right]$$

该目标只关心轨迹的最终成败，对中间推理步骤的质量完全无感知。这导致了一个关键的“无效探索”（inefficient exploration）问题：智能体虽然最终成功完成任务，但其推理路径充斥着冗余、低效甚至自相矛盾的步骤。这些有缺陷的推理模式在结果奖励的掩护下被强化学习算法错误地强化，使得策略在未见任务上的泛化能力严重受损，并伴随高重复动作率和无效动作率。

**因果机制**可概括为：结果奖励信号过于稀疏，无法区分“高效推理的成功”与“低效试错的侥幸成功”，导致策略优化陷入局部最优——学习到的是“如何碰巧成功”，而非“如何有效推理”。

### 本文动机：从“学习成功”到“学习推理”

为打破这一僵局，本文提出核心洞察：**将元认知理论中的高层认知技能（规划、探索、反思、监控）操作化为可验证的推理标签，并通过程序化规则提供过程级密集奖励，直接塑造智能体的推理过程质量**。这意味着将优化范式从“仅学习如何成功”转向“同时学习如何成功和如何推理”，从而在提升任务成功率的同时，从根本上缓解无效探索问题。

RLVMR 框架正是基于这一动机，通过引入可验证元推理奖励与复合优势函数，为长周期智能体的稳健推理能力训练提供了新的技术路径。



## 核心方法与创新机理

RLVMR 的核心创新在于，它直面了当前长周期 LLM 智能体强化学习中一个被忽视的根本矛盾：**仅优化最终任务成功（稀疏结果奖励）的范式，会系统性地奖励那些推理过程充斥着冗余、低效甚至矛盾步骤的“成功”轨迹，导致策略泛化能力脆弱且动作效率低下**。针对这一瓶颈，RLVMR 将元认知理论中的高层认知技能（规划、探索、反思、监控）操作化为可验证的推理标签，并以此构建过程级密集奖励，直接塑造智能体“如何推理”，而非仅仅“如何成功”。

这一核心思路通过以下四个关键机制实现，构成了相对于现有端到端强化学习基线的本质性改变：

### 1. 奖励信号：从稀疏结果奖励到密集可验证的过程奖励

标准在线强化学习方法（如 **GRPO** (Shao et al., 2024; Wang et al., 2025)）仅依赖轨迹最终的成功与否提供稀疏奖励 $R(\tau)$。这种信号无法区分一条高效推理的成功轨迹与一条充满无效探索和重复动作的成功轨迹，从而在优化过程中无形地强化了低质量推理模式。

RLVMR 将奖励信号从单一的最终结果扩展为**结果奖励与密集可验证的元推理奖励的组合**。具体而言，每一步的奖励由两部分构成：基于规则程序化计算的元推理奖励 $r_t^{\mathrm{MR}}$（涵盖规划、探索、反思等行为的正向激励）以及格式合规性惩罚。这使得智能体在每一步都能获得关于其推理行为质量的即时反馈，从根本上改变了优化的信用分配机制。

### 2. 优势函数构造：从轨迹级归一化到标签内归一化的复合优势

传统 GRPO 通过在同一提示词的多个采样轨迹之间进行组内归一化来构造轨迹级优势 $A_k^{\mathrm{traj}} = \frac{R(\tau_k) - \mu_R}{\sigma_R}$，这本质上是将整条轨迹视为一个不可分割的评估单元。

RLVMR 提出了一种**复合优势函数**，将轨迹级优势与标签级元推理优势进行加权融合：

$$A_t = \alpha \cdot A_k^{\mathrm{traj}} + (1 - \alpha) \cdot A_{t,\mathrm{tag}}^{\mathrm{MR}}$$

其中，标签级优势 $A_{t,\mathrm{tag}}^{\mathrm{MR}} = \frac{r_{t,\mathrm{tag}}^{\mathrm{MR}} - \mu_{\mathrm{tag}}}{\sigma_{\mathrm{tag}}}$ 的关键创新在于**在同一元推理标签组内进行归一化**——即，将某一步的“规划”质量仅与其他轨迹中的“规划”步骤进行比较，而非与“探索”或“反思”步骤混为一谈。这一设计使得优势估计能够精确捕捉同类推理行为的相对质量，避免了跨类型比较引入的噪声。

### 3. 训练范式：冷启动有监督微调注入结构化推理先验

端到端强化学习基线（如 GRPO、**GiGPO** (Feng et al., 2025)）通常直接从环境交互开始训练，智能体需要在巨大的动作-推理空间中从零开始探索，极易陷入无效循环。

RLVMR 引入了一个**基于约 200 条教师标注轨迹的冷启动有监督微调阶段**。该阶段利用更强的教师模型（如 GPT-4）在成功轨迹中自动标注元推理标签（`<planning>`、`<explore>`、`<reflection>`、`<monitor>`），使基础 LLM 在进入强化学习之前，就已经初步掌握了生成结构化标签和合法动作的能力。这一轻量级初始化（数据量远少于完整 SFT 基线）为后续的强化学习提供了一个非平凡的起点，显著降低了探索难度。

### 4. 策略优化算法：GRPO-MR 实现过程与结果的协同优化

RLVMR 在标准 GRPO 的基础上提出了 **GRPO-MR**（Group Relative Policy Optimization with Meta-Reasoning）。其核心改动在于：在组内进一步按元推理标签类型分组计算相对优势，并将该标签级优势与全局轨迹级优势通过超参数 $\alpha$ 进行加权融合，最终通过带裁剪的目标函数和 KL 正则化项更新策略：

$$\mathcal{L}_{\mathrm{final}} = \mathbb{E}_t \left[ \min \left( r_t(\theta) A_t, \mathrm{clip}(r_t(\theta), 1 - \epsilon, 1 + \epsilon) A_t \right) \right] - \lambda_{\mathrm{KL}} D_{\mathrm{KL}}(\pi_{\theta} || \pi_{\mathrm{ref}})$$

这一设计使得策略更新同时受到“是否最终成功”和“推理过程是否高质量”的双重约束，从根本上缓解了标准 GRPO 中“泛化但低效”的困境。

**消融实验为上述创新提供了决定性证据**：移除元推理奖励（$A^{\mathrm{MC}}$）导致 ALFWorld L2 成功率从 56.3% 降至 45.3%；而移除结果奖励（$A^{T}$）则使成功率崩溃至 12.5%，证实了过程奖励与结果奖励必须协同工作，缺一不可。超参数 $\alpha$ 的灵敏度分析进一步表明，当 $\alpha = 0.5$ 时性能最为稳健，过小或过大均会破坏两种信号的平衡。



![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_cTbAevdwBE/figures/009_Figure_3.jpg]]
*Figure 3: A schematic diagram of the RLVMR framework, which consists of two training phases: cold start and reinforcement learning. Our method provides rule-verifiable feedback signals based on the final outcome and the relative advantages of different types of meta-reasoning behaviors*

RLVMR 采用**两阶段训练范式**，将可验证的元推理过程监督注入端到端强化学习，其整体架构如 Figure 3 所示。

### 阶段一：冷启动有监督微调（Cold Start SFT）

该阶段的目标是让基础 LLM 初步学会生成结构化的元推理标签和合法动作，而非直接从零开始进行在线探索。具体流程为：

1. **轨迹采集**：在目标环境中运行教师模型（如 GPT-4），收集约 200 条成功完成任务的交互轨迹。
2. **元推理标注**：教师模型对每条轨迹中的每个动作步骤进行回溯标注，推断出该动作前最可能的认知步骤类型，将其映射为四类元推理标签：`<planning>`、`<explore>`、`<reflection>`、`<monitor>`。
3. **有监督微调**：使用标注后的轨迹数据对基础 LLM 进行 SFT，使其学会在 ReAct 范式的基础上输出带有元推理标签的结构化响应。

值得注意的是，冷启动仅需约 200 条轨迹，数据量远小于典型 SFT 基线所需的完整专家轨迹集，但消融实验表明该阶段对小模型尤为关键——移除冷启动使 ALFWorld L2 成功率从 56.3% 骤降至 40.6%（Table 5）。

### 阶段二：带元推理奖励的强化学习（GRPO-MR）

在冷启动策略的基础上，RLVMR 进入在线强化学习阶段。该阶段的核心创新在于**奖励信号的双重构造**和**优势函数的标签内归一化**：

**奖励信号**由两部分组成（Section 3.2, Algorithm 3）：
- **结果奖励** $R(\tau)$：轨迹结束时根据任务完成情况给出的稀疏信号。
- **过程级元推理奖励** $r_t^{\mathrm{MR}}$：每步根据规则程序化计算的密集奖励，包括规划奖励（验证子目标是否在后续被实现）、探索奖励（鼓励尝试新动作组合）、反思奖励（检测并纠正错误后给予正向反馈），以及格式惩罚（对不符合 XML 标签格式的输出施加 -0.1 的惩罚）。

**优势函数构造**采用复合设计（Section 3.3, Eq. 2-4）：
- **轨迹级优势** $A_k^{\mathrm{traj}}$：在同一批次内基于最终结果奖励进行组归一化。
- **标签级元推理优势** $A_{t,\mathrm{tag}}^{\mathrm{MR}}$：在相同标签类型（如所有 `<planning>` 步骤）的步骤内进行归一化，衡量该步推理质量相对于同类步骤的优势。
- **组合步级优势** $A_t = \alpha \cdot A_k^{\mathrm{traj}} + (1-\alpha) \cdot A_{t,\mathrm{tag}}^{\mathrm{MR}}$，其中 $\alpha$ 控制全局结果信号与局部推理信号之间的平衡，默认设为 0.5。

**策略优化**采用 GRPO-MR（Algorithm 1-2），在标准 GRPO 的裁剪替代目标函数基础上，使用上述复合优势 $A_t$ 替代单一的轨迹级优势，并加入 KL 散度正则化项 $-\lambda_{\mathrm{KL}} D_{\mathrm{KL}}(\pi_\theta || \pi_{\mathrm{ref}})$（$\lambda_{\mathrm{KL}}=0.01$），防止策略偏离参考模型过远。

### 模块间数据流

整个框架的数据流可概括为：环境交互产生的观察-动作序列 → 元推理标签框架对其进行结构化标注 → 奖励塑形模块计算每步的过程奖励与最终结果奖励 → GRPO-MR 优化器利用标签内归一化的复合优势更新策略参数。两阶段训练确保了策略在具备基本推理能力的基础上，通过在线探索进一步强化推理质量和泛化能力。



### 冷启动有监督微调（Cold Start SFT）

RLVMR 的训练分为两个阶段。第一阶段是冷启动 SFT，其核心目的是让基础 LLM 初步习得结构化元推理标签的生成能力和合法动作空间。具体做法是：利用一个更强的教师模型（如 GPT-4）对约 200 条成功轨迹进行标注，推断每个动作前最可能的认知步骤，并插入 `<planning>`、`<explore>`、`<reflection>`、`<monitor>` 四类 XML 风格标签。这些标注后的轨迹构成 SFT 数据集，使策略模型在进入强化学习阶段前已具备基本的元推理行为模式，从而避免从零开始的无效探索。

### 元推理标签框架

RLVMR 在 ReAct 范式的基础上扩展了四类结构化元推理标签，将智能体的内部认知过程显式化：

- **`<planning>`**：表示智能体正在制定高层计划或分解子目标。
- **`<explore>`**：表示智能体正在执行信息收集或环境探索动作。
- **`<reflection>`**：表示智能体正在对先前动作的结果进行评估、纠错或调整策略。
- **`<monitor>`**：表示智能体正在检查当前状态是否满足任务终止条件。

所有环境交互动作均置于 `<action>` 标签内，与推理标签在结构上分离。这一设计使得后续的奖励塑形能够针对不同类型的推理行为施加差异化反馈。

### 可验证元推理奖励塑形

RLVMR 的核心创新在于提供过程级密集奖励信号，而非仅依赖最终任务成功与否的稀疏结果奖励。每步的即时奖励由两部分组成：

$$r_t = r_t^{\mathrm{MR}} + r_t^{\mathrm{format}}$$

其中 $r_t^{\mathrm{MR}}$ 是根据预定义规则计算的可验证元推理奖励，涵盖规划、探索、反思三类正向激励（如规划是否合理、探索是否产生新信息、反思是否准确识别错误等），以及格式违规时的惩罚项 $r_t^{\mathrm{format}}$（如输出未遵循 XML 标签结构时给予 -0.1 的固定惩罚）。所有奖励信号均由程序化规则自动验证，无需人工标注或学习判别器。

### GRPO-MR 优化目标

RLVMR 采用一种名为 GRPO-MR（Group Relative Policy Optimization with Meta-Reasoning）的策略优化算法，其关键创新在于构造了融合全局结果信号与局部推理信号的复合优势函数。

#### 轨迹级相对优势

对于同一 prompt 采样得到的 $K$ 条轨迹，第 $k$ 条轨迹的轨迹级优势基于最终结果奖励 $R(\tau_k)$ 在批次内归一化：

$$A_k^{\mathrm{traj}} = \frac{R(\tau_k) - \mu_R}{\sigma_R}$$

其中 $\mu_R$ 和 $\sigma_R$ 分别为批次内所有轨迹结果奖励的均值和标准差。

#### 元推理级相对优势

对于第 $t$ 步的元推理奖励 $r_{t,\mathrm{tag}}^{\mathrm{MR}}$，其优势在同一标签类型（如所有 `<planning>` 步骤）的组内进行归一化：

$$A_{t,\mathrm{tag}}^{\mathrm{MR}} = \frac{r_{t,\mathrm{tag}}^{\mathrm{MR}} - \mu_{\mathrm{tag}}}{\sigma_{\mathrm{tag}}}$$

其中 $\mu_{\mathrm{tag}}$ 和 $\sigma_{\mathrm{tag}}$ 分别为该标签组内所有步骤元推理奖励的均值和标准差。这种标签内归一化的设计确保了不同推理类型（如探索与反思）的优势在各自语义范畴内可比。

#### 组合步级优势

将上述两级优势通过超参数 $\alpha$ 加权融合，得到每步的复合优势：

$$A_t = \alpha \cdot A_k^{\mathrm{traj}} + (1 - \alpha) \cdot A_{t,\mathrm{tag}}^{\mathrm{MR}}$$

$\alpha$ 控制全局结果信号与局部推理信号的平衡。消融实验表明，$\alpha = 0.5$ 时性能最稳健：$\alpha$ 过小（接近 0）会剥夺成功信号导致性能崩溃，$\alpha$ 过大（接近 1）则削弱元推理奖励的塑形效果。

#### 最终策略损失

基于复合优势 $A_t$，策略更新采用带裁剪的替代目标函数，并加入 KL 散度正则化以约束策略偏离参考模型：

$$\mathcal{L}_{\mathrm{final}} = \mathbb{E}_t \left[ \min \left( r_t(\theta) A_t, \ \mathrm{clip}(r_t(\theta), 1 - \epsilon, 1 + \epsilon) A_t \right) \right] - \lambda_{\mathrm{KL}} D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}})$$

其中 $r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\mathrm{old}}(a_t|s_t)}$ 为概率比，$\epsilon$ 为裁剪阈值，$\lambda_{\mathrm{KL}}$ 为 KL 惩罚系数（默认 0.01）。该目标函数在保持训练稳定性的同时，通过复合优势函数同时优化任务成功率与推理过程质量。



## 实验与关键发现

### 核心瓶颈：从“无效探索”到“高效推理”的量化证据

在长周期具身智能任务中，仅以最终任务成功为奖励信号的强化学习范式，会导致一种被本文称为“无效探索”（inefficient exploration）的系统性缺陷。**Figure 2** 在 ALFWorld 基准上清晰地刻画了这一现象：监督微调（SFT）模型在已见任务（L0）上表现高效，但其泛化能力脆弱——7B SFT 模型在未见任务（L2）上的成功率从 63.3% 骤降至 37.5%。相反，端到端强化学习（GRPO）虽然将 L2 泛化成功率提升至 52.3%，却付出了严重的推理效率代价：7B GRPO 的重复动作率高达 31.2%，无效动作率同样居高不下。更值得注意的是，将模型规模从 1.5B 扩展至 7B 不仅未能缓解这一问题，反而使重复动作率从 27.1% 升至 31.2%（Figure 2(f)），表明单纯扩大模型容量无法自动习得稳健的推理过程。


![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_cTbAevdwBE/figures/008_Figure_2.jpg]]
*Figure 2: Performance on ALFWorld. While SFT excels on seen tasks (L0) but fails to generalize, GRPO achieves better generalization at the cost of significant inefficiency. This highlights a fundamental trade-off between brittle efficiency and inefficient generalization*

这一“高效但脆弱 vs. 泛化但低效”的根本性权衡，构成了本文方法设计的直接动机：需要一种能够在强化学习过程中**直接塑造推理质量**的奖励机制，而非仅奖励最终结果。

### 主实验结果：成功率与推理效率的双重突破

**Table 1** 汇总了 RLVMR 在 ALFWorld 和 ScienceWorld 两个长周期基准上的全面对比。在最具挑战性的 ALFWorld L2 分割（完全未见的任务变体和类别）上，RLVMR 以 Qwen2.5-7B 为基座取得了 **83.6%** 的成功率，远超最强端到端 RL 基线 GiGPO（67.2%）和 GRPO（52.3%），相对提升分别达 +16.4 和 +31.3 个百分点。在 Qwen2.5-1.5B 小模型上，RLVMR 同样取得 56.3% 的 L2 成功率，而 GRPO 仅为 31.3%。在 ScienceWorld 基准上，RLVMR 以 32.2% 的成功率超越 GRPO 的 26.6%（+5.6 个百分点），且在平均累积奖励（score）指标上也保持领先。


![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_cTbAevdwBE/figures/010_Table_1.jpg]]
*Table 1: Performance comparison on the benchmarks. We report the success rate (%) on seen (L0: seen task variants and categories) and unseen (L1: unseen task variants but seen task categories; L2: unseen task variants and categories) task variations. We also report the average cumulative reward (score) on the ScienceWorld benchmark*

值得注意的是，RLVMR 在已见任务（L0）上同样保持竞争力：Qwen2.5-7B 达到 91.4%，Llama3.1-8B 达到 92.2%，证明过程奖励的引入并未牺牲对已知任务的拟合能力。

**Figure 4** 从推理效率维度揭示了更关键的提升。在 ALFWorld L2 分割上，RLVMR（1.5B）将重复动作率从 GRPO 的 27.1% 压缩至 **5.7%**（降幅达 21.4 个百分点），无效动作率从 18.4% 降至 12.5%。这意味着 RLVMR 学到的策略不仅更成功，而且更“聪明”——它懂得避免无意义的循环和非法操作，将有限的交互步数用于有效探索。


![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_cTbAevdwBE/figures/014_Figure_4.jpg]]
*Figure 4: Exploration efficiency of RLVMR compared to SFT and GRPO baselines on ALFWorld*

**Figure 5** 和 **Figure 6** 进一步展示了训练效率优势：RLVMR 在 ALFWorld 上的成功率曲线收敛更快，且平均完成步数持续低于 GRPO，表明过程级奖励信号有效引导了策略搜索方向，减少了试错成本。

### 消融实验：元推理奖励与结果奖励的协同必要性

**Table 5** 的核心消融结果直接验证了本文的核心主张——过程级元推理奖励不可或缺，且必须与结果奖励协同工作。以 Qwen2.5-1.5B 在 ALFWorld L2 上的完整 RLVMR（成功率 56.3%）为基准：


![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_cTbAevdwBE/figures/024_Table_5.jpg]]
*Table 5: Ablation results on ALFWorld and ScienceWorld (success rates (%) on L2 variant)*

- **移除元推理奖励（A^MC）**：成功率降至 45.3%（-11.0 个百分点），ScienceWorld 上从 26.5% 降至 20.3%。这证明即使保留了最终结果信号，缺乏对规划、探索、反思等中间推理步骤的显式奖励，策略仍难以在复杂未见任务中习得有效推理模式。
- **移除结果奖励（A^T）**：成功率崩溃至 12.5%（ALFWorld）和 7.8%（ScienceWorld）。这一极端退化表明，纯过程奖励无法独立驱动任务完成——智能体需要最终成功信号来锚定推理行为的最终目的。
- **移除冷启动 SFT 阶段**：成功率下降 15.7 个百分点至 40.6%。仅 200 条教师标注轨迹的初始化对后续 RL 收敛至关重要，尤其对小模型而言，它提供了基本的元推理标签生成能力和合法动作空间。

**Table 6** 进一步消融了四类元推理标签的各自贡献。移除反思（reflection）标签造成的损害最大：成功率从 56.3% 降至 46.2%（-10.1 个百分点），重复动作率从 5.7% 飙升至 14.5%，无效动作率从 12.5% 升至 20.2%。这与直觉一致——反思机制是智能体识别错误、避免陷入循环的关键认知技能。移除探索（explore）标签导致平均轨迹长度从 15.4 步增至 17.2 步，且重复/无效动作均有增加，说明结构化探索引导能提升搜索效率。规划（planning）和监控（monitor）标签的移除也分别造成 5-7 个百分点的成功率下降，证实每一类元认知技能都对稳健的长周期行为有独立贡献。


![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_cTbAevdwBE/figures/025_Table_6.jpg]]
*Table 6: Overall, these ablations demonstrate that each meta-reasoning type contributes meaningfully to robust long-horizon behavior. The meta-reasoning patterns operationalized from metacognitive theory are therefore essential for improving both effectiveness and reliability of the agent. Table 6: Ablation of meta-reasoning tag types on ALFWorld L2 with Qwen2.5-1.5B-Instruct*

### 超参数灵敏度与折扣因子分析

**Figure 7** 展示了组合优势函数中权重系数 α 的灵敏度。α 控制轨迹级结果优势与标签级元推理优势的平衡：

$$A_t = \alpha \cdot A_k^{\mathrm{traj}} + (1 - \alpha) \cdot A_{t,\mathrm{tag}}^{\mathrm{MR}}$$

实验表明 α = 0.5 时性能最稳健。当 α 过小（0~0.05）时，结果信号几乎被完全剥夺，性能急剧恶化；当 α 接近 1.0 时，元推理奖励被削弱，性能同样下降。这进一步印证了两类信号需要均衡协同的结论。

**Figure 8(b)** 考察了在 RLVMR 中引入时间折扣因子 γ 的影响。结果表明折扣因子的引入对性能影响微乎其微，说明显式的元推理奖励已为每个时间步提供了足够的结构化指导，无需额外的时序衰减来区分步骤重要性。

### 公平性说明

所有对比方法使用相同的环境最大步数限制（30 步）、相同的模型基座和相同的评估分割，确保了比较的公平性。RLVMR 的冷启动阶段仅使用约 200 条教师标注轨迹，与基线 SFT 方法使用完整专家轨迹的数据量相比并不占优，排除了数据量优势的混淆解释。



## 定位与知识库关联

### 1. 与基线方法的谱系关系

RLVMR 的方法学位置处于**端到端在线强化学习（online end-to-end RL）**与**过程监督（process supervision）**的交叉地带。其直接对话的基线方法可按训练范式分为四类：

**零样本提示基线**：**ReAct**（Yao et al., 2023）通过交错推理与行动轨迹实现零样本任务执行，是本文元推理标签框架的语法基础。RLVMR 在 ReAct 的 `<thought>`/`<action>` 结构上扩展了 `<planning>`、`<explore>`、`<reflection>`、`<monitor>` 四类结构化标签，将隐式推理显式化为可验证的认知步骤，从而为过程级奖励提供了“锚点”。

**监督微调基线**：标准 SFT 在已见任务上表现高效但泛化能力脆弱——ALFWorld L0 上成功率 63.3%，L2 骤降至 37.5%（Qwen2.5-7B）。RLVMR 的冷启动阶段同样使用 SFT，但仅需约 200 条教师标注轨迹（远少于完整专家轨迹），且其目的不是“学会成功”，而是使模型初步习得生成结构化标签和合法动作的格式能力，为后续 RL 阶段提供稳定的初始策略分布。

**离线强化学习基线**：**ETO**（Song et al., 2024）和 **GLIDER**（Hu et al., 2025）利用离线数据进行策略优化，避免了在线交互成本，但受限于数据覆盖范围，在未见任务上的泛化能力有限。RLVMR 采用在线 RL 范式，通过与环境实时交互探索新策略，同时以过程奖励引导探索方向，在 ALFWorld L2 上显著超越离线方法。

**在线端到端 RL 基线**：这是 RLVMR 最核心的对比对象。**GRPO**（Shao et al., 2024; Wang et al., 2025）和 **GiGPO**（Feng et al., 2025）均使用仅基于最终结果的稀疏奖励进行端到端策略优化。GRPO 虽提升了泛化成功率（ALFWorld L2 达 52.3%），但带来了严重的推理低效——重复动作率高达 31.2%（7B 模型），且增大模型规模并不能缓解该问题（1.5B 为 27.1%，7B 反升至 31.2%）。RLVMR 的核心创新在于**在 GRPO 的优化框架内注入了过程级密集奖励**：将元推理行为的规则化奖励与最终结果奖励结合，并在优势函数层面通过标签内归一化（tag-level normalization）实现细粒度的信用分配，使策略优化直接塑造“如何推理”而非仅“如何成功”。

### 2. 关键设计差异与因果机制

RLVMR 与上述基线的方法论差异可归结为三个“变化槽”（changed slots）：

| 变化槽 | 基线值 | RLVMR 值 | 因果作用 |
|--------|--------|----------|----------|
| 奖励信号 | 仅稀疏结果奖励 $R(\tau)$ | 结果奖励 + 密集可验证元推理奖励 $r_t^{\text{MR}}$（规划、探索、反思奖励及格式惩罚） | 缓解无效探索：过程奖励为每一步提供即时反馈，避免策略在冗余或矛盾步骤上浪费信用 |
| 优势函数构造 | 轨迹级组归一化优势 $A_k^{\text{traj}}$ | 复合优势 $A_t = \alpha A_k^{\text{traj}} + (1-\alpha) A_{t,\text{tag}}^{\text{MR}}$，元推理优势在同一标签组内归一化 | 平衡全局成功信号与局部推理质量信号；标签内归一化消除了不同标签类型间奖励尺度差异带来的偏差 |
| 训练范式 | 直接从环境交互开始端到端 RL | 冷启动 SFT（~200 条标注轨迹）→ 端到端 RL | 提供结构化推理的初始能力，避免 RL 早期在巨大的标签-动作联合空间中盲目探索 |

消融实验直接验证了这些差异的因果贡献：移除元推理奖励 $A^{\text{MC}}$ 导致 ALFWorld L2 成功率从 56.3% 降至 45.3%（下降 11 个百分点）；移除结果奖励 $A^T$ 则使成功率崩溃至 12.5%；移除冷启动阶段使成功率降至 40.6%（下降 15.7 个百分点）。三者协同方才构成完整方法。

### 3. 适用边界与局限

**已验证的适用场景**：RLVMR 在两类文本交互式具身智能基准上得到验证——ALFWorld（家庭环境文本游戏）和 ScienceWorld（科学实验文本模拟）。其核心假设是：任务的可验证推理行为可以被预定义为有限类别的规则化标签。在此前提下，方法在已见和未见任务上均取得最优，且推理效率（重复动作率、无效动作率）显著优于所有基线。

**已知局限**：

1. **标签空间的封闭性**：当前四类元推理标签（规划、探索、反思、监控）是人工预定义的，可能无法覆盖所有有益的推理模式。对于需要创造性问题求解或非常规推理路径的任务，预定义标签可能成为约束而非引导。
2. **环境模态限制**：实验仅在纯文本环境中进行。在多模态环境（如视觉导航、物理机器人操作）中，如何将元推理标签与图像观察对齐，以及如何定义基于视觉状态的可验证奖励规则，均未验证。
3. **冷启动对教师模型的依赖**：冷启动阶段依赖更强的教师模型（如 GPT-4）生成标注。虽然实验表明对教师模型选择不敏感，但若教师能力极弱，标注质量可能限制初始化上限。
4. **奖励规则的手工设计**：元推理奖励的计算依赖人工编写的规则（如规划奖励基于后续动作是否与规划一致），这限制了方法向全新领域的迁移速度。

### 4. 开放问题与后续方向

论文明确指出了四个开放方向：

1. **多模态扩展**：将 RLVMR 框架扩展到视觉-语言环境，处理图像观察中的元推理行为定义与验证。
2. **自适应奖励机制**：设计能根据任务复杂度和智能体熟练度动态调整元推理奖励权重的机制，替代当前固定的 $\alpha=0.5$ 超参数。
3. **标签空间的自动发现**：探索元推理标签的自动发现或在线扩展方法，突破当前四类预定义标签的限制。
4. **真实世界应用**：在机器人操作、代码调试等真实场景中，定义和验证过程级奖励，同时确保安全性和价值对齐。

从方法谱系角度看，RLVMR 为“将认知过程结构化并纳入强化学习优化”提供了可操作的范式，其核心思想——通过可验证的中间行为标签实现过程监督——可被视为连接符号化推理规则与神经网络策略优化的桥梁。后续工作可能沿两个方向延伸：一是向下游，将标签空间从认知行为扩展至工具使用、多智能体协作等更复杂的交互模式；二是向上游，探索自动发现或学习最优标签结构的方法，减少人工设计依赖。



## 原文 PDF

![[paperPDFs/ICLR_2026/RLVMR_Reinforcement_Learning_with_Verifiable_Meta_Reasoning_Rewards_for_Robust_Long_Horizon_Agents.pdf]]
