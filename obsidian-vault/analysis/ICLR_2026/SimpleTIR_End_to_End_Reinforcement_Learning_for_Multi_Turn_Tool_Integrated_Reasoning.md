---
title: "SimpleTIR: End-to-End Reinforcement Learning for Multi-Turn Tool-Integrated Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SimpleTIR_End_to_End_Reinforcement_Learning_for_Multi_Turn_Tool_Integrated_Reasoning.pdf
project_link: null
code_link: null
openreview_forum_id: EplNy91Xqh
aliases:
- SimpleTIR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过检测并过滤包含“空轮次”（void turn，指未生成完整代码块或最终答案的轮次）的完整轨迹，阻止这些病理轨迹参与策略更新，直接消除有害的大梯度并修正信用分配，从而实现稳定的多轮 TIR 零 RL 训练。"
primary_logic: "空轮次是低概率 token 累积和高生成随机性的可靠信号，可作为简单而有效的轨迹级过滤指标，从根本上抑制梯度爆炸并保留有价值的多轮推理行为。"
claims:
- "单轮 TIR 训练平稳且性能较高，而多轮 TIR 训练则出现性能崩溃和频发的梯度尖峰。"
- "工具反馈 token 的概率极低（OOD），且这种漂移污染后续轮次的模型自身文本，导致多轮轨迹中 token 概率崩溃，最终产生空轮次。"
- "低概率 token 会通过未裁剪的重要性比率和概率相关项导致策略梯度范数爆炸。"
- "SimpleTIR 过滤含有空轮次的轨迹后，梯度范数几乎无尖峰，最终性能显著优于朴素多轮训练及基于概率/比率的 token 级过滤方法。"
---

# SimpleTIR: End-to-End Reinforcement Learning for Multi-Turn Tool-Integrated Reasoning

> [!tip] 核心洞察
> 空轮次是低概率 token 累积和高生成随机性的可靠信号，可作为简单而有效的轨迹级过滤指标，从根本上抑制梯度爆炸并保留有价值的多轮推理行为。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SimpleTIR：面向多轮工具集成推理的端到端强化学习 |
| 英文题名 | SimpleTIR: End-to-End Reinforcement Learning for Multi-Turn Tool-Integrated Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=EplNy91Xqh) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | SimpleTIR |
| Dataset | AIME24, MATH500, AIME25 |

> [!tip] 效果简介
> - AIME24 上，Accuracy (pass@32) 为 50.5 (SimpleTIR-7B)，对比 39.6 (ZeroTIR-7B)，变化 +10.9。
> - MATH500 上，Accuracy (pass@32) 为 88.4 (SimpleTIR-7B)，对比 80.2 (ZeroTIR-7B)，变化 +8.2。
> - AIME25 上，Accuracy (pass@32) 为 30.9 (SimpleTIR-7B)，对比 25.0 (ZeroTIR-7B)，变化 +5.9。

## 概要

**问题瓶颈**：多轮工具集成推理（TIR）训练中，来自外部工具（如代码解释器）的反馈分布与模型预训练数据分布严重不一致，引发分布漂移。这种漂移在后续轮次中不断累积，导致模型生成 token 的概率极低，进而诱发策略梯度爆炸和信用分配错乱，使训练稳定性崩溃、性能骤降。

**核心洞察**：空轮次（void turn）——即模型响应中既无完整代码块也无最终答案的轮次——是低概率 token 累积与高生成随机性的可靠信号。将其作为轨迹级过滤指标，可以从根本上抑制梯度爆炸，同时保留有价值的多轮推理行为。

**方法定位**：SimpleTIR 是一种即插即用的轨迹过滤算法，在 GRPO 策略更新前检测并滤除包含空轮次的完整轨迹，阻止病理轨迹参与策略优化。该方法在 feedback masking 的基础上，将含空轮次轨迹的损失掩码设为零，完全排除其对参数更新的贡献。

**主要结果**：在 Qwen2.5-7B 基座上，SimpleTIR 将 AIME24 得分从朴素多轮训练的 20.8 提升至 50.5，MATH500 从 73.1 提升至 88.4。在 Qwen2.5-32B 上，AIME24 得分达到 59.9。训练过程中梯度范数几乎无尖峰，显著优于基于低概率 token 或高重要性比率的 token 级过滤方法（后者均出现 NaN 梯度或训练崩溃）。



### 工具集成推理的零 RL 训练瓶颈

工具集成推理（Tool-Integrated Reasoning, TIR）赋予大语言模型在推理过程中调用外部工具（如代码解释器）的能力，从而显著提升其在数学、编程等复杂任务上的表现。近年来，基于强化学习的零 RL（Zero RL）范式——即从基座模型出发，不经过监督微调，直接使用强化学习进行训练——在纯文本推理上取得了令人瞩目的进展。然而，当这一范式被扩展到多轮 TIR 场景时，训练稳定性面临严峻挑战。

**核心瓶颈在于分布漂移引发的低概率 token 累积。** 在多轮 TIR 中，来自外部工具（如代码执行结果）的反馈分布与模型的预训练数据分布存在显著差异。这种分布漂移使得模型在接收到工具反馈后的后续轮次中，生成 token 的概率急剧下降，出现大量极低概率 token。这些低概率 token 在回合间持续累积，通过未裁剪的重要性采样比率和概率相关项，导致策略梯度范数爆炸，信用分配错乱，最终使训练陷入不稳定甚至崩溃。

这一现象在实验中有清晰的证据链：

- **单轮与多轮的稳定性鸿沟**：Figure 2 显示，单轮 TIR 训练过程平滑且能达到较高性能，而多轮 TIR 训练则出现剧烈波动和性能崩溃。
- **token 概率的逐轮崩溃**：Figure 3 可视化了多轮轨迹中 token 概率的演变——早期轮次的工具反馈引入分布漂移后，后续轮次中模型自身生成文本的 token 概率呈现对数级下降，最终导致整个轨迹的概率崩溃。
- **梯度爆炸的数学根源**：Proposition 1 对策略梯度范数进行了分解，揭示了低概率 token 如何通过重要性比率 $\rho_{i,t}(\theta)$ 和概率分布项 $\sqrt{1 - 2P(c) + \sum_{j \in A} P(j)^2}$ 导致梯度范数爆炸。

### 现有方法的缺口

现有的多轮 TIR 训练方法主要沿两条路径展开：一类从指令微调模型出发进行 RL 训练（如 ToRL、ARPO），另一类则遵循零 RL 范式（如 ZeroTIR）。尽管这些方法在特定设置下取得了进展，但它们在根本上**未能直接应对多轮 TIR 中特有的分布漂移和低概率 token 累积问题**。

具体而言，现有方法存在以下不足：

- **缺乏针对性的轨迹级过滤**：朴素的多轮训练仅对工具执行输出的 token 进行掩码（feedback masking），而不对轨迹本身的质量进行筛选。这使得包含病理行为的轨迹——特别是那些因概率崩溃而产生的“空轮次”轨迹——仍然参与策略更新，持续注入有害梯度。
- **token 级过滤的局限性**：基于低概率 token 或高重要性比率的 token 级过滤虽然直观，但实验表明它们无法稳定训练。Table 2 和 Figure 7 显示，这些方法在训练过程中出现 NaN 梯度，AIME24 分数分别仅为 23.3 和 26.3，远低于 SimpleTIR 的 50.5。
- **“空轮次”作为关键信号被忽视**：在多轮 TIR 中，当模型因概率崩溃而无法生成完整代码块或最终答案时，会产生所谓的“空轮次”（void turn）。这一现象既是分布漂移的直接后果，也是训练即将崩溃的可靠前兆，但此前的方法并未将其作为轨迹过滤的指标。

### 本文动机

基于上述观察，本文的核心动机是：**设计一种简单、即插即用的轨迹级过滤策略，通过检测并排除包含空轮次的完整轨迹，从根本上阻断低概率 token 对策略更新的污染，从而实现多轮 TIR 零 RL 训练的稳定化。** 这一策略无需修改奖励函数、无需调整优化器，也无需引入额外的正则化项，仅通过改变训练数据的构成即可达成目标。



## 核心方法与创新机理

SimpleTIR 的核心创新在于**通过轨迹级过滤解决多轮工具集成推理（TIR）中由分布漂移引发的训练崩溃问题**。与现有方法在 token 级别进行干预不同，SimpleTIR 直接识别并移除包含“空轮次”（void turn）的完整轨迹，从根本上消除导致梯度爆炸的病理信号。

### 问题根因：分布漂移 → 低概率 token → 梯度爆炸

多轮 TIR 训练的不稳定性源于一个因果链条。外部工具（如代码解释器）的输出 token 分布与模型预训练数据分布存在显著差异，这种**分布漂移**（distributional drift）使工具反馈成为相对于模型策略的离群（OOD）输入（Figure 3）。当模型在后续轮次中基于这些 OOD 输入继续生成时，其自身文本的 token 概率也会崩溃至极低水平。

这些低概率 token 通过两条路径破坏训练稳定性。首先，在 PPO 的裁剪替代损失中，重要性采样比率 $\rho_{i,t}(\theta)$ 对于负优势轨迹是**无上界的**——旧策略下极低概率的 token 在策略更新后即使概率略有提升，也会导致该比率爆炸。其次，策略梯度 L2 范数中的概率相关项 $\sqrt{1 - 2P(c) + \sum_j P(j)^2}$ 在策略对采样 token 分配极低概率且分布尖锐时，会**持续维持大梯度**。两者叠加，使得梯度范数出现灾难性尖峰，训练迅速崩溃（Figure 2）。

### 创新方案：空轮次作为轨迹级过滤信号

SimpleTIR 的关键洞察是：**空轮次是低概率 token 累积和高生成随机性的可靠、可检测信号**。空轮次定义为模型响应中既未包含完整代码块、也未给出最终答案（如 `\boxed{}` 或 `final_answer` 调用）的轮次。这类轮次通常表现为不完整的代码块、无意义的文本序列或完全崩溃的生成。

基于此，SimpleTIR 在每次 GRPO 策略更新前执行两步操作：
1. **检测**：逐轮检查每条采样轨迹，标记是否包含空轮次；
2. **过滤**：将包含至少一个空轮次的完整轨迹从当前批次中移除，将其损失掩码设为 0，使其完全不参与策略损失计算。

这一设计直接切断了低概率 token 向梯度计算传播的路径。与 token 级过滤方法（如基于最低概率或最高重要性比率的掩码）不同，轨迹级过滤**不依赖概率阈值调参**，且能一次性消除空轮次中所有受污染 token 的累积效应，而非仅掩盖其中部分 token。

### 与 baseline 的关键差异（changed slots）

| 维度 | Naive Multi-Turn 基线 | SimpleTIR |
|------|----------------------|-----------|
| **轨迹过滤策略** | 不对轨迹进行额外过滤，或仅采用基于低概率 token / 高重要性比率的 token 级过滤 | 检测并完全滤除包含至少一个空轮次的整个轨迹 |
| **GRPO 更新中的掩码对象** | 仅对工具执行输出 token 进行掩码（feedback masking），不实施轨迹级别掩码 | 在 feedback masking 基础上，将含空轮次的完整轨迹损失掩码设为 0 |

消融实验直接验证了这一创新的有效性：移除空轮次过滤后（Naive Multi-Turn），AIME24 得分从 50.5 暴跌至 20.8，MATH500 从 88.4 降至 73.1，且出现频繁的梯度爆炸（Table 2）。基于低概率 token 或高重要性比率的 token 级过滤方法则因 NaN 梯度而提前停止训练，AIME24 分数分别仅为 23.3 和 26.3（Figure 7）。这些结果表明，空轮次过滤是稳定多轮 TIR 零 RL 训练的充分且必要条件。



![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EplNy91Xqh/figures/008_Figure_4.jpg]]
*Figure 4: An overview of SIMPLETIR. During the policy update, SIMPLETIR identifies and filters out entire Emergent Multi-Turn Reasoning Patternstrajectories that contain a void turn—an LLM response that fails to produce either a complete code block or a final answer*

SimpleTIR 是一个**即插即用的轨迹级过滤算法**，嵌入在基于 GRPO 的多轮工具集成推理（TIR）训练流程中。其核心 pipeline 由四个串行模块构成：多轮交互 rollout 采样、空轮次检测器、轨迹过滤器、以及带反馈掩码的 GRPO 更新。

**输入**为一个自然语言数学问题 $q$。在 rollout 阶段，当前策略 $\pi_{\theta_{\text{old}}}$ 针对 $q$ 生成 $G$ 条多轮交互轨迹。每条轨迹中，模型依次生成响应、执行代码块，并接收来自外部代码解释器的执行反馈，形成“模型文本—工具反馈—模型文本”交替的序列。为保持与基模型（如 Qwen2.5-7B）的分布一致性，系统不使用聊天模板，而是在工具输出前添加简单前缀 `Code Execution Result:`；同时，在模型生成完整代码块后立即停止解码，强制追加真实的外部工具反馈，防止模型幻觉工具输出。

**空轮次检测器**随后逐轮扫描每条轨迹中的模型响应。空轮次定义为：该轮次的模型响应中既不包含完整的代码块，也不包含最终答案（如 `\boxed{}` 格式或 `final_answer` 函数调用）。这一检测完全基于结构化模式匹配，不依赖 token 概率或重要性比率等信号。

**轨迹过滤器**以整条轨迹为粒度进行决策：若一条轨迹包含至少一个空轮次，则该轨迹被完全标记为无效，其损失掩码在后续 GRPO 更新中置为零，从而被彻底排除出策略损失计算。这一设计的因果逻辑在于：空轮次是低概率 token 累积和高生成随机性的可靠信号（见 Figure 3），滤除这些病理轨迹可直接消除由未裁剪重要性比率 $\rho_{i,t}(\theta)$ 和概率分布项 $\sqrt{1 - 2P(c) + \sum_{j \in A} P(j)^2}$ 引发的梯度爆炸（Proposition 1），同时保留包含有效多轮推理行为（如交叉验证、渐进推理、自我纠错）的轨迹。

**带反馈掩码的 GRPO 更新**在过滤后的轨迹集合上执行。损失函数仅累积模型生成 token 上的裁剪替代损失 $L_{\text{CLIP}}$，工具执行输出的 token 以及被滤除轨迹的所有 token 均通过二元掩码 $m_{i,t}$ 排除。最终训练目标为：

$$\mathcal{J}_{\text{TIR}}(\theta) = \mathbb{E}_{\{o_i\}_{i=1}^G \sim \pi_{\theta_{\text{old}}}(\cdot|q)} \left[ \frac{1}{G} \sum_{i=1}^G \frac{1}{\sum_t m_{i,t}} \sum_{t=1}^{|o_i|} m_{i,t} \cdot L_{\text{CLIP}}(\theta, i, t) \right]$$

其中 $L_{\text{CLIP}}(\theta, i, t) = \min\left(\rho_{i,t}(\theta) \hat{A}_i, \text{clip}(\rho_{i,t}(\theta), 1-\varepsilon, 1+\varepsilon) \hat{A}_i\right)$，$\rho_{i,t}(\theta) = \frac{\pi_\theta(o_{i,t} \vert o_{i,<t})}{\pi_{\theta_{\text{old}}}(o_{i,t} \vert o_{i,<t})}$。

整个框架的模块关系如 **Figure 4** 所示：rollout 生成轨迹 → 空轮次检测 → 轨迹级过滤 → 掩码 GRPO 更新。这一流程无需修改底层 RL 算法或奖励模型，仅通过在策略更新前插入一个轻量级过滤步骤，即可将多轮 TIR 训练从梯度爆炸和性能崩溃中挽救出来。



### 多轮 TIR 的形式化建模

SimpleTIR 将多轮工具集成推理建模为分层马尔可夫决策过程，将决策分为两个层级：高层策略控制对话轮次的序列，底层策略则在每一轮内生成具体的响应 token。训练采用统一的策略 $\pi_{\theta}$，通过 GRPO（Group Relative Policy Optimization）进行优化。

### 核心训练目标

多轮 TIR 的最终训练目标函数为：

$$\mathcal{J}_{\mathrm{TIR}}(\theta) = \mathbb{E}_{\{o_i\}_{i=1}^{G} \sim \pi_{\theta_{\mathrm{old}}}(\cdot | q)} \left[ \frac{1}{G} \sum_{i=1}^{G} \frac{1}{\sum_t m_{i,t}} \sum_{t=1}^{|o_i|} m_{i,t} \cdot L_{\mathrm{CLIP}}(\theta, i, t) \right]$$

其中 $G$ 为采样轨迹数，$o_i$ 为第 $i$ 条轨迹的完整 token 序列，$m_{i,t} \in \{0, 1\}$ 是二元掩码——仅在模型自身生成的 token 上取值为 1，在外部工具执行输出的 token 上取值为 0。这一反馈掩码机制确保了信用分配仅作用于模型的决策 token，而非环境反馈。

每条轨迹的裁剪替代损失为：

$$L_{\mathrm{CLIP}}(\theta, i, t) = \min\Big(\rho_{i,t}(\theta) \hat{A}_i, \mathrm{clip}(\rho_{i,t}(\theta), 1 - \varepsilon, 1 + \varepsilon) \hat{A}_i\Big)$$

其中 $\hat{A}_i$ 为轨迹 $i$ 的组内相对优势估计，$\varepsilon$ 为裁剪阈值。重要性采样比率定义为：

$$\rho_{i,t}(\theta) = \frac{\pi_{\theta}(o_{i,t} \vert o_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(o_{i,t} \vert o_{i,<t})}$$

该比率度量了当前策略与旧策略在给定 token 上的概率偏差，是 PPO 风格更新的核心控制量。

### 梯度爆炸的数学机理

作者推导了策略梯度对 logits $\mathbf{z}_t$ 的 L2 范数分解：

$$\|\nabla_{\mathbf{z}_t} \mathcal{J}_{TIR}\|_2 = \frac{m_{i,t}}{\sum_j m_{i,j}} \cdot \rho_{i,t}(\theta) \cdot g_{i,t} \cdot |\hat{A}_i| \cdot \sqrt{1 - 2P(c) + \sum_{j \in A} P(j)^2}$$

该分解揭示了梯度范数的三个关键依赖项：

- **$\rho_{i,t}(\theta)$（重要性比率）**：对于低概率 token，旧策略下的概率极低，导致该比率无上界。即使策略仅发生微小更新，$\rho_{i,t}(\theta)$ 也可急剧膨胀，直接驱动梯度爆炸。
- **$\sqrt{1 - 2P(c) + \sum_{j} P(j)^2}$（概率分布项）**：当策略对采样 token $c$ 分配极低概率，且分布高度尖锐时，该项保持较大值，持续放大梯度范数。
- **$g_{i,t}$（梯度系数）**：与 token 在词汇表上的梯度结构相关。

低概率 token 同时通过无界比率和持续高概率分布项两个渠道放大梯度范数，这正是多轮 TIR 训练不稳定的数学根源。

### SimpleTIR 的轨迹过滤模块

针对上述机理，SimpleTIR 引入了空轮次检测与轨迹过滤两个关键模块：

1. **空轮次检测器**：逐轮检查模型响应是否包含完整的代码块（``````...`````` 结构）或最终答案（`\boxed{}` 或 `final_answer` 调用）。若某轮二者皆无，则标记为空轮次。
2. **轨迹过滤器**：扫描每条完整轨迹，若包含至少一个空轮次，则将该轨迹的损失掩码全部置零，完全排除其对 GRPO 策略更新的贡献。

这一设计直接切断了低概率 token 通过梯度范数传导的路径——含空轮次的轨迹通常对应着 token 概率已崩溃的病理序列，将其从更新中移除，等价于从根源上消除了无界比率和持续高概率分布项的破坏性影响。



## 实验与关键发现

### 主实验结果

SimpleTIR 在多个数学推理基准上展现出显著且一致的性能优势，其核心增益源于对多轮 TIR 训练稳定性的根本性修复。表 1 汇总了各方法在 AIME24、AIME25、MATH500 等基准上的 pass@32 准确率。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EplNy91Xqh/figures/009_Table_1.jpg]]
*Table 1: Performance comparison on various math benchmarks. Check and cross marks in the “TIR” column refers to whether the method involves TIR during training and evaluation. The “From” column indicates the type of base models we train the model from. We fill the scores with - if they are not provided in respective reports*

在 7B 规模，SimpleTIR-7B 在 AIME24 上达到 **50.5**，较 ZeroTIR-7B（39.6）提升 **+10.9**，较 ToRL-7B（40.2）提升 **+10.3**；在 MATH500 上达到 **88.4**，较 ZeroTIR-7B（80.2）提升 **+8.2**。值得注意的是，SimpleTIR-7B 的性能甚至显著超越了基于更大基模型（32B）的若干基线方法。

在 32B 规模，SimpleTIR-32B 在 AIME24 上达到 **59.9**，较 ZeroTIR-32B（48.0）提升 **+11.9**，较 DAPO（50.0）提升 **+9.9**，确立了新的性能高点。

在更小的 4B 规模，SimpleTIR-4B 从 Qwen3-4B-Base 的 4.9 分提升至 **48.1**（+43.2），验证了该方法在不同模型容量下的鲁棒性。所有评估均在统一的 pass@32 协议（温度 1、top-p 0.95）下进行，训练数据均为 Math3-5 与 Deepscaler 数据集，基模型均为 Qwen 系列，确保了对比的公平性。

### 训练稳定性分析

图 1 揭示了 SimpleTIR 与朴素多轮训练在训练动态上的本质差异。SimpleTIR 的梯度范数曲线几乎无尖峰，始终维持在低水平，训练过程高度平稳；而朴素多轮训练（Naive Multi-turn）则出现灾难性的梯度范数爆炸（峰值超过 40），并伴随性能崩溃，最终表现甚至不及不使用 TIR 的 DAPO 基线。这直接证明了多轮 TIR 的不稳定性是制约性能的核心瓶颈，而非 TIR 本身缺乏潜力。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EplNy91Xqh/figures/002_Figure_1.jpg]]
*Figure 1: Starting from Qwen2.5-7B base model, The training dynamics of SimpleTIR are highly stable, and it clearly outperforms the baseline method without TIR (DAPO). The gradient norm remains well-behaved with almost no spikes. In contrast, Naive Multi-turn Training not only suffers from unstable dynamics and catastrophic gradient norm explosions, but also fails to match the performance of the baseline without TIR*

图 2 进一步将问题定位于“多轮”特性：单轮 TIR 训练过程平滑且性能较高，而多轮 TIR 训练则出现剧烈波动和性能衰退。这表明不稳定性的根源在于跨轮次的误差累积与分布漂移，而非工具交互本身。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EplNy91Xqh/figures/006_Figure_2.jpg]]
*Figure 2: Training statistics comparing naive single-turn and multi-turn TIR. Single-turn training proceeds smoothly and achieves higher performance, while multi-turn training is unstable*

### 消融实验与失败模式

表 2 的消融实验严格验证了空洞轮次过滤的不可替代性：

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EplNy91Xqh/figures/018_Table_2.jpg]]
*Table 2: Results of ablation studies. Considering the unstable training of ablated methods, we report the highest scores within 1000 gradient steps. “Naive Multi-Turn” directly applies RLVR in multi-turn TIR. “Low Prob” and “High Ratio” filtering refers to masking the policy loss on tokens with lowest probabilities or highest importance ratio*

- **移除空洞轮次过滤（Naive Multi-Turn）**：AIME24 得分从 50.5 骤降至 **20.8**，MATH500 从 88.4 降至 73.1，且训练过程中梯度范数频繁爆炸（图 5 底部）。
- **基于低概率 token 的过滤（Low Prob Filtering）**：AIME24 仅 **23.3**，训练仍不稳定，最终因梯度出现 NaN 而提前停止（图 7）。
- **基于高重要性比率的过滤（High Ratio Filtering）**：AIME24 为 **26.3**，同样因 NaN 梯度提前终止，无法完成完整训练。
- **仅截断后缀的过滤（Filter Suffix）**：训练过程虽相对稳定，但最终性能仍显著低于 SimpleTIR（图 8 底部），表明仅移除空洞轮次之后的生成而不对整个轨迹进行掩码，无法充分消除有害梯度的影响。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EplNy91Xqh/figures/017_Figure_5.jpg]]
*Figure 5: Top: Training curves for SimpleTIR with different maximum number of turns. SimpleTIR with maximum 10 turns is resumed at 200 steps from SimpleTIR with maximum 5 turns. SimpleTIR clearly benefits from scaling interaction turns from 1 to 5. Bottom: The training curves for ablation studies in the first 320 steps. Trajectory filtering with high importance ratios or low probability tokens cannot resolve the challenge of training instability, while SimpleTIR suffers less from low probability tokens and gradient explosion*

这些结果揭示了一个关键洞见：token 级的概率或比率阈值过滤无法有效抑制梯度爆炸，因为低概率 token 的累积效应已污染整个轨迹的信用分配。SimpleTIR 的轨迹级过滤通过一次性排除病理轨迹，从根本上切断了梯度爆炸的传导路径。

### 推理行为分析

SimpleTIR 的训练稳定性不仅带来了性能提升，还催生了更丰富的推理行为。图 6 展示了三种典型的多轮推理模式：**交叉验证**（Cross Validation）、**逐步推理**（Progressive Reasoning）和**自我纠错**（Error Correction）。表 3 的定量分析显示，SimpleTIR-32B 在逐步推理（46.5% vs. 18.9%）和自我纠错（38.0% vs. 25.8%）上的频率显著高于 ReTool，表明稳定的训练环境使模型能够习得更复杂、更主动的推理策略。

### 交互轮次的可扩展性

图 5（顶部）展示了 SimpleTIR 在不同最大交互轮次下的训练曲线。从 1 轮到 5 轮，模型性能持续提升，验证了多轮交互的价值。当从 5 轮恢复训练扩展至 10 轮时，性能仍有进一步增益，表明 SimpleTIR 的稳定机制能够支撑轮次扩展，而不会重新引入训练崩溃的风险。

### 关键图表汇总

- **图 1**：训练动态全景对比——SimpleTIR 的梯度范数稳定在低位，朴素多轮训练则爆炸至 40+。
- **图 2**：单轮 vs. 多轮 TIR 训练对比——多轮训练的不稳定性是核心瓶颈。
- **表 1**：全基准性能对比——SimpleTIR 在各模型规模上均取得最优结果。
- **表 2**：消融实验——空洞轮次过滤的移除导致性能崩溃，token 级过滤方法均失败。
- **图 5**：轮次扩展与消融训练曲线——SimpleTIR 从 1 轮扩展至 10 轮持续受益，消融方法均出现梯度爆炸或 NaN。
- **表 3**：推理模式频率对比——SimpleTIR 展现出更强的逐步推理和自我纠错能力。



## 定位与知识库关联

### 核心瓶颈与因果机制

SimpleTIR 所解决的核心问题在于多轮工具集成推理（TIR）的**零强化学习（Zero RL）训练不稳定性**。其根本瓶颈是：外部工具（如代码解释器）的反馈分布与预训练数据分布不一致，引发**分布漂移**。这一漂移使模型在后续轮次中生成 token 的概率极低（OOD token），这些低概率 token 在回合间累积，导致**策略梯度爆炸**和**信用分配错乱**，最终使训练崩溃。

因果调控旋钮是**轨迹级过滤**：通过检测并过滤包含“空轮次”（void turn，指未生成完整代码块或最终答案的轮次）的完整轨迹，阻止这些病理轨迹参与策略更新，直接消除有害的大梯度并修正信用分配。空轮次作为低概率 token 累积和高生成随机性的可靠信号，成为简单而有效的轨迹级过滤指标。

### 在 TIR 与 Zero RL 谱系中的定位

SimpleTIR 处于 **Zero RL 范式下的多轮 TIR 训练**这一交叉点。其方法谱系可沿两个维度展开：

**维度一：是否采用工具集成推理（TIR）。** 非 TIR 的纯文本 Zero RL 基线包括 **DAPO**（Yu et al., 2025）和 **SimpleRL-Zoo**（Zeng et al., 2025），它们在数学推理上已展现强性能，但未利用外部工具进行多轮验证与修正。SimpleTIR 在引入 TIR 后，不仅未因训练不稳定而性能倒退，反而显著超越了这些纯文本基线（Figure 1）。

**维度二：TIR 训练中采用何种 RL 策略与稳定化手段。** 现有 TIR 方法可大致分为两类：

- **从指令微调模型出发的 TIR RL**：如 **ToRL**（Li et al., 2025b）从数学指令模型出发，**ARPO**（Dong et al., 2025）从指令微调模型出发。这些方法借助指令微调阶段的分布对齐，部分规避了 Zero RL 面临的分布漂移问题，但未从根本上解决从基模型直接训练 TIR 的稳定性挑战。

- **从基模型出发的 TIR RL**：如 **ZeroTIR**（Mai et al., 2025）遵循 Zero RL 范式进行多轮 TIR 训练，**Effective TIR**（Bai et al., 2025）和 **VT/VerlTool**（Jiang et al., 2025）基于数学专用基模型。这些方法直接面对分布漂移问题，但未提出针对性的稳定化机制。SimpleTIR 与 ZeroTIR 同属 Zero RL 范式，但 SimpleTIR 通过空轮次过滤直接解决了 ZeroTIR 中存在的训练不稳定问题，在 AIME24 上从 39.6 提升至 50.5（SimpleTIR-7B），在 MATH500 上从 80.2 提升至 88.4（Table 1）。

### 关键设计选择与消融证据

SimpleTIR 的轨迹过滤策略与两类替代方案形成对比（Table 2, Figure 5 Bottom, Figure 7）：

- **朴素多轮训练（Naive Multi-Turn）**：不实施额外过滤，仅对工具执行输出 token 进行掩码（feedback masking）。该方案导致性能崩溃（AIME24 从 50.5 降至 20.8，MATH500 从 88.4 降至 73.1），并伴随频繁的梯度范数尖峰。

- **Token 级过滤**：包括基于低概率 token 的过滤（Low Prob Filtering）和基于高重要性比率的过滤（High Ratio Filtering）。这两种方案均无法稳定训练，出现 NaN 梯度并提前停止，AIME24 分数分别仅为 23.3 和 26.3。

- **后缀过滤（Filter Suffix）**：仅终止空轮次之后的生成，而不对整个轨迹进行掩码。训练虽相对稳定，但性能仍低于 SimpleTIR（Figure 8 Bottom）。

这些消融实验表明：**轨迹级过滤是必要的**，仅对 token 级指标进行干预无法根除梯度爆炸；同时，**完全排除病理轨迹**（而非仅截断后缀）对于维持正确的信用分配至关重要。

### 适用边界与局限

SimpleTIR 的当前验证存在明确的适用边界：

1. **任务域局限**：仅在数学推理任务（AIME24/25、MATH500 等）上验证，尚未在搜索、数据库查询等其他需要多轮工具交互的领域上测试。

2. **交互轮次限制**：最大交互轮次限制为 10 轮。对于更长的多步自主智能体任务，可能需要进一步的序列长度扩展和训练效率优化。值得注意的是，从 5 轮扩展到 10 轮时，AIME24 得分未见明显提升，而 MATH500 持续受益（Figure 5 Top），这一现象的原因尚需进一步分析。

3. **工具形态依赖**：空轮次检测依赖于对代码块和最终答案（`\boxed{}` 或 `final_answer` 调用）的结构化模式匹配。对于多语言、多工具混合的复杂工具形态，需要针对性的指标设计。

4. **基础设施依赖**：训练与评估依赖外部代码执行沙盒，沙盒的延迟、稳定性及安全性可能影响方法的实际部署与规模扩展。

### 开放问题

SimpleTIR 开启了若干值得进一步探索的方向：

- **跨工具泛化**：如何将基于空轮次的过滤策略泛化到其他非代码工具（如搜索、LSP 服务）的多轮智能体任务？这需要定义与代码块/最终答案等价的“有效轮次”指标。

- **超长轮次扩展**：如何将训练扩展到 10 轮以上，同时保持高效且稳定的 rollout 与奖励计算？异步 rollout 和奖励计算解耦可能是一个有前景的方向。

- **更大规模验证**：在更大规模模型（>70B）和更多样化的预训练基座上，SimpleTIR 的稳定性和增益是否仍然保持？当前实验覆盖 Qwen2.5-7B/32B 和 Qwen3-4B，更大规模的验证仍是开放问题。



## 原文 PDF

![[paperPDFs/ICLR_2026/SimpleTIR_End_to_End_Reinforcement_Learning_for_Multi_Turn_Tool_Integrated_Reasoning.pdf]]
