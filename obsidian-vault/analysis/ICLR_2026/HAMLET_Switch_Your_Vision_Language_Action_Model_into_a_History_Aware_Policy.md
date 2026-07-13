---
title: "HAMLET: Switch Your Vision-Language-Action Model into a History-Aware Policy"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/HAMLET_Switch_Your_Vision_Language_Action_Model_into_a_History_Aware_Policy.pdf
project_link: https://myungkyukoo.github.io/hamlet/
code_link: null
openreview_forum_id: KcJ9U0x6kO
aliases:
- HAMLET
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过引入可学习的 moment tokens 和轻量级记忆模块，将历史信息压缩为紧凑特征并选择性聚合到动作预测中，以极小的计算代价将预训练的单帧 VLA 转化为历史感知策略，从而显著提升历史依赖任务的成功率。"
primary_logic: "时间对比学习初始化的 moment tokens 能够捕获时间区分性任务相关特征，抑制静态背景冗余；浅层 Transformer 记忆模块可以动态关注关键历史时刻，避免同等对待所有时间步带来的干扰，使历史信息有效融入单帧 VLA 而不破坏其泛化能力。"
claims:
- "HAMLET 在三个真实世界长视距任务上平均成功率达到 76.4%，相比 GR00T N1.5 基线提升 47.2%。"
- "在 LIBERO 基准上，HAMLET 将先前最佳结果从 95.6% 提升至 97.6%，证明历史感知对于接近饱和性能仍有增益。"
- "多帧基线在仿真任务中导致性能下降（RoboCasa 下降 3.3%，LIBERO 下降 8.8%），而 HAMLET 通过记忆模块仅引入单帧输入同时利用历史，兼顾了性能与泛化。"
- "时间对比学习初始化使 moment tokens 关注任务相关区域，移除 TCL 导致性能持续下降。"
---

# HAMLET: Switch Your Vision-Language-Action Model into a History-Aware Policy

> [!tip] 核心洞察
> 时间对比学习初始化的 moment tokens 能够捕获时间区分性任务相关特征，抑制静态背景冗余；浅层 Transformer 记忆模块可以动态关注关键历史时刻，避免同等对待所有时间步带来的干扰，使历史信息有效融入单帧 VLA 而不破坏其泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | HAMLET：将视觉-语言-动作模型切换为历史感知策略 |
| 英文题名 | HAMLET: Switch Your Vision-Language-Action Model into a History-Aware Policy |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=KcJ9U0x6kO) · [Project](https://myungkyukoo.github.io/hamlet/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | HAMLET |
| Dataset | Real-world (3 Long-Horizon Tasks), RoboCasa Kitchen (100 demos), LIBERO (Average), SimplerEnv-Bridge (CogACT) |

> [!tip] 效果简介
> - Real-world (3 Long-Horizon Tasks) 上，Avg. Success Rate (%) 为 76.4，对比 29.2 (GR00T N1.5)，变化 +47.2%。
> - RoboCasa Kitchen (100 demos) 上，Success Rate (%) 为 65.4，对比 62.6 (GR00T N1.5)，变化 +2.8%。
> - LIBERO (Average) 上，Success Rate (%) 为 97.6，对比 95.6 (GR00T N1.5)，变化 +2.0%。

## 概要

**核心问题**：当前视觉-语言-动作模型（VLA）在机器人操控中仅依赖单帧观测进行决策，缺乏对历史上下文的利用。在需要多步推理或存在遮挡的非马尔可夫任务中，这种设计导致模型无法从当前观测推断正确动作，直接追加多帧历史又会显著增加计算开销并损害泛化能力。

**方法定位**：HAMLET 是一种面向预训练 VLA 的微调框架，通过引入可学习的 moment tokens 和轻量级记忆模块，将单帧 VLA 转化为历史感知策略。其核心设计包括两个互补组件：moment tokens 在每个时间步压缩视觉语义，经时间对比学习初始化以捕获时间区分性特征；浅层 Transformer 记忆模块选择性聚合历史 moment token 表示，为动作预测提供时间增强特征。该方法以极小的计算代价赋予 VLA 历史感知能力，同时保持单帧模型的泛化优势。

**核心结论**：在三个真实世界长视距任务上，HAMLET 平均成功率达到 76.4%，相比 GR00T N1.5 基线提升 47.2%；在 LIBERO 基准上将先前最佳结果从 95.6% 提升至 97.6%；在 SimplerEnv-Bridge 上基于 CogACT 骨干网络提升 11.4%。消融实验表明，记忆模块是核心增益来源，时间对比学习初始化对性能有持续贡献。该方法在扩散型和自回归型 VLA 上均展现出有效性。

### 视觉-语言-动作模型的单帧瓶颈

视觉-语言-动作模型（VLA）通过将预训练视觉-语言模型（VLM）与机器人动作预测相结合，在通用机器人操控任务中取得了显著进展。然而，当前主流 VLA 模型（如 **GR00T N1.5**、**π0**、**OpenVLA** 等）在决策时仅依赖当前时刻的单帧观测和任务指令，其核心范式可概括为：

$$\mathbf{h}_t = \mathcal{F}_\theta(\mathbf{o}_t, \mathbf{c})$$

$$[\mathbf{a}_t, \mathbf{a}_{t+1}, \ldots, \mathbf{a}_{t+k-1}] = \mathcal{A}_\psi(\mathbf{h}_t, \mathbf{s}_t)$$

其中 $\mathbf{o}_t$ 为当前观测，$\mathbf{c}$ 为指令，$\mathbf{s}_t$ 为本体感知状态。这种设计隐含地假设任务满足马尔可夫性质——当前观测足以确定最优动作。但在真实世界的长视距操控任务中，这一假设经常被打破。

### 非马尔可夫任务中的失败模式

三类典型场景暴露了单帧 VLA 的根本局限：

1. **物体遮挡**：目标物体被暂时遮挡后重新出现，单帧模型无法判断该物体是之前操作过的目标还是新出现的物体，导致重复操作或遗漏。
2. **多步推理**：任务需要根据先前步骤的结果决定后续动作（如“将蓝色方块与绿色方块交换位置”），单帧观测无法提供已完成步骤的信息。
3. **状态跟踪**：需要记忆已完成的子任务数量（如连续三次抓取-放置），单帧模型无法区分当前处于第几次循环。

在真实世界评估中，**GR00T N1.5** 在这类历史依赖任务上的平均成功率仅为 29.2%（Table 1），说明现有 VLA 在此类场景中几乎失效。

### 朴素多帧方案的代价

一个直接的解决方案是将多帧历史图像直接拼接到 VLM 输入中。然而，实验表明这一策略存在严重缺陷：

- **性能退化**：在 RoboCasa Kitchen 仿真基准上，多帧基线导致成功率下降 3.3%；在 LIBERO 基准上更是下降 8.8%（Table 2, Table 3）。原因在于额外帧引入了无关背景噪声，干扰了 VLM 的视觉理解。
- **计算开销激增**：多帧输入使延迟和显存占用成倍增长。以 4 帧历史为例，延迟增加 3.6 倍，峰值显存增加 7 倍（Table 4），严重损害实时控制效率。
- **泛化能力受损**：预训练 VLA 在单帧数据上微调获得的能力，在多帧输入下难以保持，导致跨任务泛化性能下降。

### 核心矛盾与 HAMLET 的切入点

上述分析揭示了一个核心矛盾：**历史信息对非马尔可夫任务至关重要，但直接将多帧图像注入 VLA 会破坏其单帧预训练获得的泛化能力并引入不可接受的计算开销。** 因此，关键问题在于：如何以最小的修改代价，让预训练的单帧 VLA 具备有效利用历史上下文的能力？

HAMLET 的核心洞察是：历史信息的利用不应以牺牲 VLA 的单帧处理效率为代价，而应通过**紧凑的时间表示**和**轻量级的记忆聚合机制**来实现。具体而言，HAMLET 引入两个互补组件：

- **Moment Tokens**：可学习的 token，在每个时间步与观测一起输入 VLM，将视觉语义压缩为紧凑的时间步表示，并通过时间对比学习（TCL）初始化以捕获时间区分性特征。
- **Memory Module**：浅层 Transformer，动态聚合过去时刻的 moment token 表示，选择性关注关键历史时刻，生成历史增强特征用于动作预测。

这一设计使 HAMLET 在保持单帧输入效率的同时，有效利用了历史上下文，将预训练 VLA 切换为历史感知策略。

## 核心方法与创新机理

HAMLET 的核心创新在于将预训练的单帧视觉-语言-动作模型（VLA）切换为历史感知策略，而无需修改原始 VLA 的骨干网络。其关键洞察是：通过引入可学习的 **moment tokens** 和轻量级 **记忆模块**，以极小的计算代价将历史信息压缩为紧凑特征并选择性聚合到动作预测中，从而突破当前 VLA 仅依赖单帧观测的根本瓶颈。

### 问题瓶颈与因果机制

当前 VLA（如 **GR00T N1.5**，Bjorck et al., 2025a）仅基于当前观测 $\mathbf{o}_t$ 和任务指令 $\mathbf{c}$ 进行动作预测，缺乏对历史上下文的利用。在需要多步推理或存在遮挡的非马尔可夫任务中，单帧信息不足以确定正确动作——例如，机械臂需要“记住”之前是否已将蓝色方块放下，才能决定下一步是抓取绿色方块还是执行其他操作。直接追加多帧输入虽能提供历史信息，但会显著增加计算开销（延迟和内存增长 3.6–7 倍，见 Table 4），并损害模型的泛化能力——在 RoboCasa 和 LIBERO 上，多帧基线分别导致性能下降 3.3% 和 8.8%（Table 2, Table 3）。

HAMLET 的因果机制可概括为：**时间对比学习初始化的 moment tokens 捕获时间区分性任务相关特征，抑制静态背景冗余；浅层 Transformer 记忆模块动态关注关键历史时刻，避免同等对待所有时间步带来的干扰**。这两者协同，使历史信息有效融入单帧 VLA 而不破坏其泛化能力。

### 相对于基线的关键变更（Changed Slots）

HAMLET 在三个关键维度上对标准 VLA 进行了改造：

**1. 输入构建：从单帧观测到“观测 + 可学习 moment tokens”**

基线 VLA 仅将当前观测 $\mathbf{o}_t$ 和指令 $\mathbf{c}$ 输入 VLM 骨干。HAMLET 在此基础上追加一组可学习的 moment tokens $\mathbf{m}_t$，使 VLM 的输入变为 $[\mathbf{o}_t, \mathbf{c}; \mathbf{m}_t]$，并输出更新后的 moment token 表示 $\mathbf{m}_t'$（Eq. 3）。这些 tokens 在每个时间步压缩视觉语义，提供紧凑的时间步表示，长度仅为 4（默认设置），几乎不增加 VLM 的计算负担。

**2. 时间特征学习：从无初始化到时间对比学习（TCL）初始化**

基线 VLA 不对输入 tokens 进行专门的时间特征学习。HAMLET 通过时间对比学习对 moment tokens 进行初始化：拉近同一时间步不同增强视图的表示 $\mathbf{z}_t$ 和 $\mathbf{z}_t^+$，推开不同时间步的表示 $\mathbf{z}_t$ 和 $\mathbf{z}_t^-$（Eq. 4）。这一初始化使 moment tokens 学会关注任务相关区域（如待抓取物体）而非静态背景，为后续记忆模块提供高质量的时间步特征。消融实验表明，移除 TCL 初始化会导致性能持续下降（RoboCasa 上从 65.4% 降至 64.8%，Table 5a），注意力可视化也证实 TCL 使 moment tokens 更集中于任务相关区域（Figure 8）。

**3. 历史信息整合：从无历史利用到 Transformer 记忆模块**

基线 VLA 完全忽略历史信息。HAMLET 引入一个浅层 Transformer 记忆模块 $\mathcal{M}_\phi$，将过去 $T$ 个时间步的 moment token 表示堆叠为历史矩阵 $\mathbf{M}'$（Eq. 5），通过因果自注意力计算历史增强特征 $\tilde{\mathbf{m}}'$（Eq. 6），最终与 VLM 隐藏状态 $\mathbf{h}_t$ 拼接后输入动作专家预测动作块（Eq. 7）。这一设计使模型能够动态关注关键历史时刻——例如在“交换方块”任务中，记忆模块在需要回忆蓝色方块是否已被放下时，会明显关注相关的历史时间步（Figure 4b, Figure 9）。消融实验确认记忆模块是核心组件：移除它导致最大性能下降（65.4% → 63.4%，Table 5a）；在多种记忆架构（RNN、LSTM、GRU、Transformer）中，Transformer 实现最高平均成功率（65.4%，Table 5c）。

### 核心洞察与证据强度

HAMLET 的决定性优势在于**以极低成本赋予单帧 VLA 历史感知能力**。在三个真实世界长视距任务上，HAMLET 平均成功率达到 76.4%，相比 GR00T N1.5 基线提升 47.2%（Table 1, Figure 1）——这一提升幅度在机器人操作领域极为显著。即使在接近饱和的 LIBERO 基准上（先前最佳 95.6%），HAMLET 仍将其提升至 97.6%（Table 2），证明历史感知对性能上限仍有增益。效率分析显示，HAMLET 的延迟仅为基线的 1.02–1.07 倍，内存开销约 2 倍，远优于多帧基线的 3.6–7 倍（Table 4）。此外，在 LIBERO 上预训练的记忆模块迁移至 RoboCasa 仍能取得 64.5% 成功率，接近在源域训练的效果（65.4%），表明记忆表示可跨数据集泛化（Table 6）。

**需注意的局限**：尽管 HAMLET 在扩散型 VLA（GR00T N1.5、CogACT）上验证良好，其在自回归式 VLA（如 OpenVLA 或 π0-FAST 的原始架构）上的直接适用性尚需进一步验证；时间对比学习初始化引入了额外训练成本；记忆模块在大规模多任务数据上的可扩展性尚未充分探索。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_KcJ9U0x6kO/figures/002_Figure_2.jpg]]
*Figure 2: An overview of HAMLET. Building on a pre-trained VLA, HAMLET adds two key components: moment tokens, appended to the VLM input and initialized with time-contrastive learning to capture task-relevant representations at each timestep, and a lightweight memory module that aggregates these tokens across timesteps for history-aware action prediction*

HAMLET 是一个面向预训练视觉-语言-动作模型（VLA）的微调框架，其核心目标是以极小的计算代价将单帧决策策略转化为历史感知策略。框架由两个互补组件构成：**Moment Tokens** 和 **记忆模块**，二者协同工作，使 VLA 能够在不需要多帧图像输入的前提下利用历史上下文进行动作预测。

### Pipeline 总览

整个推理流程可概括为以下步骤：

1. **当前观测与指令编码**：VLA 的 VLM 主干 $\mathcal{F}_\theta$ 接收当前观测 $\mathbf{o}_t$ 和任务指令 $\mathbf{c}$，生成隐藏表示 $\mathbf{h}_t$（式 1）。
2. **Moment Token 提取**：将可学习的 moment tokens $\mathbf{m}_t$ 与 $\mathbf{o}_t, \mathbf{c}$ 一同送入 VLM，得到更新后的 moment token 表示 $\mathbf{m}_t'$（式 3）。这些 token 在每个时间步将视觉语义压缩为紧凑的特征向量。
3. **历史聚合**：记忆模块 $\mathcal{M}_\phi$ 收集最近 $T$ 个时间步的 moment token 表示 $\mathbf{m}_{t-k(T-1)}', \ldots, \mathbf{m}_t'$，通过因果自注意力机制选择性聚合关键历史信息，输出历史增强特征 $\tilde{\mathbf{m}}'$（式 5-6）。
4. **动作预测**：将 VLM 隐藏状态 $\mathbf{h}_t$ 与历史增强特征 $\tilde{\mathbf{m}}'$ 拼接，连同本体感知状态 $\mathbf{s}_t$ 送入动作专家 $\mathcal{A}_\psi$，预测未来 $k$ 步动作块 $[\mathbf{a}_t, \ldots, \mathbf{a}_{t+k-1}]$（式 7）。

### 模块关系与数据流

两个核心组件的分工明确且互补：

- **Moment Tokens** 负责在每个时间步将丰富的视觉观测压缩为低维、任务相关的紧凑表示。其关键设计在于通过**时间对比学习**进行初始化，鼓励同一时间步的不同增强视图对齐、不同时间步的表示推开，从而使 token 倾向于关注随时间变化的任务相关区域（如被操作的物体、夹爪状态），同时抑制静态背景的冗余信息。
- **记忆模块** 是一个轻量级的浅层 Transformer，它在时间维度上操作，以 moment token 序列为输入。模块通过因果自注意力机制动态评估各历史时刻对当前决策的重要性，而非同等对待所有时间步。这使得模型能够在需要时精准回溯关键历史帧（例如遮挡发生前的物体位置），在不需要时忽略无关时刻，避免信息过载。

### 输入输出规范

- **输入**：当前观测 $\mathbf{o}_t$（单帧图像）、任务指令 $\mathbf{c}$、本体感知状态 $\mathbf{s}_t$，以及可学习的 moment tokens $\mathbf{m}_t$。历史信息通过记忆模块内部维护的 moment token 队列隐式引入，无需额外图像输入。
- **输出**：未来 $k$ 步的动作序列 $[\mathbf{a}_t, \ldots, \mathbf{a}_{t+k-1}]$，与原始 VLA 的动作空间完全一致。

### 与朴素多帧方案的对比

区别于直接将多帧图像拼接输入 VLA 的朴素方案，HAMLET 通过 moment tokens 和记忆模块实现了“单帧输入、多帧利用”的效果。多帧基线需要成倍增加 VLM 的推理计算量，且可能引入分布外视觉特征损害泛化能力；而 HAMLET 的记忆模块仅在轻量级 Transformer 中处理紧凑的 token 序列，推理延迟和显存开销极低（历史长度 4 时仅增加 1.02 倍延迟），同时保持了原始 VLA 的泛化特性。

> **注意**：HAMLET 的 moment tokens 长度、记忆模块层数、历史长度等超参数默认设置为 4、2 层 Transformer 和 4，这些取值在实验中表现稳定，但更彻底的架构搜索是否为最优解仍属开放问题。

HAMLET 在预训练 VLA 的基础上引入两个互补组件：**moment tokens** 和**记忆模块**，二者协同实现从单帧到历史感知策略的切换。

### Moment Tokens：时间步压缩表示

给定当前观测 $\mathbf{o}_t$ 和任务指令 $\mathbf{c}$，标准 VLA 的 VLM 主干生成隐藏表示：

$$\mathbf{h}_t = \mathcal{F}_\theta(\mathbf{o}_t, \mathbf{c}) \tag{1}$$

动作专家基于该隐藏状态和本体感知 $\mathbf{s}_t$ 预测未来 $k$ 步动作块：

$$[\mathbf{a}_t, \mathbf{a}_{t+1}, \ldots, \mathbf{a}_{t+k-1}] = \mathcal{A}_\psi(\mathbf{h}_t, \mathbf{s}_t) \tag{2}$$

HAMLET 将一组可学习的 moment tokens $\mathbf{m}_t$ 追加到 VLM 输入序列中，与观测和指令共同前向传播，提取压缩后的时间步表示：

$$[\mathbf{h}_t; \mathbf{m}_t'] = \mathcal{F}_{\boldsymbol{\theta}}([\mathbf{o}_t, \mathbf{c}; \mathbf{m}_t]) \tag{3}$$

其中 $\mathbf{m}_t'$ 是经 VLM 编码后的 moment token 表示，捕获了当前时间步的视觉语义信息。

**时间对比学习初始化（TCL）**：为避免 moment tokens 退化或关注静态背景冗余，HAMLET 采用时间对比学习对 moment tokens 进行初始化。对同一时间步施加不同数据增强得到正样本对 $\mathbf{z}_t, \mathbf{z}_t^+$，不同时间步构成负样本对，损失函数为：

$$\mathcal{L}_{\mathrm{TCL}}(\mathbf{z}_t, \mathbf{z}_t^+) = -\sum_{t=1}^{B} \log \frac{\exp(\mathrm{sim}(\mathbf{z}_t, \mathbf{z}_t^+)/\tau)}{\exp(\mathrm{sim}(\mathbf{z}_t, \mathbf{z}_t^+)/\tau) + \exp(\mathrm{sim}(\mathbf{z}_t, \mathbf{z}_t^-)/\tau)} \tag{4}$$

该损失拉近同一时间步的不同增强视图，推开不同时间步的表示，使 moment tokens 学会捕获时间区分性、任务相关的特征，抑制静态背景冗余。消融实验表明，移除 TCL 初始化会导致性能持续下降（Table 5a），注意力可视化也证实 TCL 初始化后的 moment tokens 更集中于任务相关区域（Figure 4a, Figure 8）。

### 记忆模块：历史信息选择性聚合

为利用历史上下文，HAMLET 引入一个轻量级 Transformer 记忆模块 $\mathcal{M}_\phi$。首先按动作块步长 $k$ 间隔采样最近 $T$ 个时间步的 moment token 表示，构建历史矩阵：

$$\mathbf{M}' = [\mathbf{m}_{t-k(T-1)}'; \ldots; \mathbf{m}_{t-k}'; \mathbf{m}_t'] \in \mathbb{R}^{L \times d} \tag{5}$$

记忆模块对历史矩阵执行因果自注意力计算，选择性关注关键历史时刻：

$$\mathbf{Q} = \mathbf{M}' \mathbf{W}_q, \quad \mathbf{K} = \mathbf{M}' \mathbf{W}_k, \quad \mathbf{V} = \mathbf{M}' \mathbf{W}_v, \quad \mathbf{H} = \mathrm{softmax}\left(\frac{\mathbf{Q} \mathbf{K}^\top}{\sqrt{d}} + \mathbf{C}\right) \mathbf{V} \tag{6}$$

其中 $\mathbf{C}$ 为因果掩码，确保只关注当前及过去时间步。记忆模块输出历史增强特征 $\tilde{\mathbf{m}}'$，与原始 VLM 隐藏状态 $\mathbf{h}_t$ 拼接后输入动作专家：

$$[\mathbf{a}_t, \mathbf{a}_{t+1}, \ldots, \mathbf{a}_{t+k-1}] = \mathcal{A}_\psi([\mathbf{h}_t; \tilde{\mathbf{m}}'], \mathbf{s}_t) \tag{7}$$

### 关键设计要点

- **Moment tokens 长度**：默认 4 个 token，在计算开销与表示能力之间取得平衡。
- **记忆模块架构**：默认 2 层 Transformer，消融实验表明 Transformer 实现最高平均成功率（65.4%），优于 RNN、LSTM、GRU 等替代架构（Table 5c）。
- **历史长度**：默认 $T=4$，按动作块步长 $k$ 间隔采样，覆盖足够长的有效历史窗口。
- **因果注意力**：记忆模块的因果掩码确保预测仅依赖当前及历史信息，符合在线部署需求。

移除记忆模块导致最大性能下降（65.4% → 63.4%），证明记忆模块是 HAMLET 的核心组件（Table 5a）。注意力可视化进一步揭示：记忆模块在需要回忆特定历史时刻（如遮挡物体曾出现的位置）时，会显著提高对该时间步的注意力权重（Figure 4b, Figure 9），验证了选择性聚合机制的有效性。

## 实验与关键发现

### 4.1 核心瓶颈验证：历史依赖性任务

当前视觉-语言-动作模型（VLA）的致命瓶颈在于其马尔可夫假设——仅依赖当前单帧观测进行决策。在真实世界中，大量操作任务本质上是非马尔可夫的：物体遮挡、多步推理、状态记忆等场景要求智能体必须回溯历史信息才能做出正确动作。Figure 1 展示了两个典型失败模式：(a) 遮挡场景中，机械臂抓取方块后被遮挡，基线模型无法判断应抬起还是释放；(b) 多步推理场景中，模型无法识别哪个杯子下方有方块，因为关键信息存在于过去帧中。

HAMLET 的核心因果杠杆在于：通过极低计算代价将预训练的单帧 VLA 转化为历史感知策略，直接解决上述瓶颈。在三个真实世界长视距任务上，HAMLET 的平均成功率达到 **76.4%**，相比 GR00T N1.5 基线（29.2%）提升 **47.2%**（Table 1）。值得注意的是，朴素多帧基线（Multi-frame baseline）仅取得 31.9%，与单帧基线几乎持平，说明简单堆叠历史帧不仅无法有效利用时序信息，反而可能引入干扰。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_KcJ9U0x6kO/figures/004_Table_1.jpg]]
*Table 1: Real-world evaluation results. We report the success rate (%, over 24 trials per task) on three real-world tasks: partial success rates for columns (PnP Once, Cover Cube, Stage Cube), and ‘Success’ for full completion. Bold and underline indicate the best and runner-up results, respectively*

### 4.2 仿真基准主结果

**RoboCasa Kitchen 与 LIBERO。** Table 2 展示了基于 GR00T N1.5 骨干网络的全面对比。在 RoboCasa Kitchen 上，HAMLET 在三种数据规模（30/100/300 demonstrations）下均取得最优或次优结果，其中 100-demo 设置下达到 **65.4%**，相比基线提升 2.8%。在 LIBERO 基准上，HAMLET 将先前最佳结果从 95.6% 推升至 **97.6%**。这一结果尤其值得关注：LIBERO 任务已接近性能饱和，但历史感知能力仍能带来显著增益，证明即使在看似马尔可夫的任务中，微妙的时序依赖依然存在。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_KcJ9U0x6kO/figures/005_Table_2.jpg]]
*Table 2: Simulation benchmark results on GR00T N1.5. We compare HAMLET with baseline methods on RoboCasa Kitchen and LIBERO. For RoboCasa Kitchen, we report the average success rate (%) across 24 tasks with models trained using 30, 100, or 300 demonstrations per task. For LIBERO, each metric is the average success rate (%) across 10 tasks per suite, with training performed jointly on all suites. All the results are reproduced by us, except for those of GR00T N1 on RoboCasa Kitchen. Bold and underline indicate best and runner-up results, respectively*

**SimplerEnv-Bridge 与骨干网络通用性。** Table 3 展示了 HAMLET 在 CogACT 骨干上的迁移效果。HAMLET 将 CogACT 的平均完全成功率从 52.1% 提升至 **63.5%**（+11.4%），在所有四个 WidowX 任务上均取得最优。这验证了 HAMLET 的设计不依赖于特定 VLA 架构——无论是扩散策略（GR00T N1.5、CogACT）还是自回归模型（OpenVLA、π₀-FAST，见 Table 14），均可通过即插即用的方式获得历史感知能力。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_KcJ9U0x6kO/figures/006_Table_3.jpg]]
*Table 3: Simulation benchmark results on CogACT. We compare HAMLET with baseline methods on the SimplerEnv-Bridge benchmark. Each metric reports the success rate (%) on four WidowX tasks in SimplerEnv, with separate reporting for grasp success and full success. ‘Avg.’ denotes the average full success rate (%) across the four tasks, and all CogACT results are faithfully reproduced by us. Bold and underline indicate best and runner-up results, respectively. default, we use moment tokens of length 4, a 2-layer Transformer as the memory module, and a history length of 4. Full hyperparameters and implementation details are provided in Section A.3*

### 4.3 消融实验与机制分析

**组件贡献。** Table 5 的消融实验揭示了各组件的因果贡献。移除记忆模块导致最大性能下降（65.4% → 63.4%），证明记忆模块是核心组件。移除时间对比学习（TCL）初始化持续降低性能（65.4% → 64.8%），而将 moment tokens 简单拼接而不经过记忆模块（Moment Concat.）仅取得 62.7%，甚至低于无记忆的基线变体（63.1%），说明无选择性的历史聚合反而有害。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_KcJ9U0x6kO/figures/010_Table_5.jpg]]
*Table 5: Ablation study. Average success rate (%) on RoboCasa (100 demos) when selectively enabling different components of HAMLET. Moment Concat. concatenates all moment tokens without a memory module, whereas the Transformer-based memory yields the best overall performance. (a) Component analysis*

**记忆架构选择。** Table 5c 对比了多种记忆架构：Transformer 实现最高平均成功率（65.4%），优于 RNN（64.5%）、LSTM（65.0%）和 GRU（64.3%）。Transformer 的自注意力机制能够动态关注关键历史时刻，避免 RNN 类模型对时序位置的归纳偏置带来的次优聚合。

**TCL 初始化方法。** Table 11 对比了不同对比学习初始化策略。HAMLET 的 TCL 方法（同一时间步的不同增强视图互为正样本，不同时间步互为负样本）在所有方法中取得最高平均成功率，验证了时间区分性特征对于历史感知的核心作用。Figure 8 的可视化进一步证实：经 TCL 初始化的 moment tokens 更集中于任务相关区域（如待抓取物体），而随机初始化则分散于静态背景。

**记忆模块的注意力行为。** Figure 4 提供了关键的机制解释：(a) moment tokens 在 VLM 内部的自注意力集中于夹爪和与任务成功相关的物体区域，抑制静态背景冗余；(b) 记忆模块的跨时间步注意力权重表明，模型能根据当前上下文选择性回溯关键历史时刻——例如在 Swap Cubes 任务中，当需要移动绿色方块时，记忆模块会高亮蓝色方块被放置的那个历史时间步（Figure 9）。

### 4.4 效率分析

HAMLET 的核心设计原则之一是以极小计算代价换取历史感知能力。Table 4 的效率分析表明：在历史长度 4 的设置下，HAMLET 的推理延迟仅为基线的 **1.02 倍**，峰值内存为 **1.07 倍**；而朴素多帧基线在相同历史长度下延迟达 3.58 倍，内存达 3.61 倍。当历史长度扩展至 8 时，HAMLET 仍保持 1.07 倍延迟和 1.17 倍内存，多帧基线则飙升至 7.06 倍和 7.14 倍。这一效率优势源于 moment tokens 的紧凑表示——仅需 4 个 token 即可压缩单帧信息，而非处理完整的多帧视觉序列。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_KcJ9U0x6kO/figures/009_Table_4.jpg]]
*Table 4: Efficiency analysis. Average latency and peak memory usage measured on RoboCasa datasets. Both metrics are computed at each timestep within an episode and then averaged. For fair comparison, memory for original VLA parameters is excluded, except for the memory module in HAMLET. All measurements were on an NVIDIA A100 GPU. ↓ indicates lower values are better*

### 4.5 跨数据集泛化

Table 6 验证了记忆模块的表示可迁移性。在 LIBERO 上预训练的记忆模块迁移至 RoboCasa 后，仍能取得 **64.5%** 的成功率，接近在 RoboCasa 源域训练的 65.4%。这一结果表明，记忆模块学习到的历史聚合策略具有跨 embodiment 和跨任务场景的泛化能力，而非过拟合于特定数据分布。

### 4.6 失败模式与局限性

尽管 HAMLET 在多数场景下表现优异，分析揭示了以下边界情况：

1. **极长视距任务。** Table 13 的 Pick-and-Place Three Times 任务（需连续完成三次抓放循环）中，HAMLET 的成功率（54.2%）虽显著优于基线（25.0%），但绝对性能仍有限，表明当前历史长度（T=4）可能不足以覆盖超长时序依赖。
2. **TCL 训练成本。** Table 8 显示，HAMLET 需额外的 TCL 预训练阶段，增加了训练时间开销（尽管推理效率几乎不受影响）。

3. **自回归 VLA 的适配。** Table 14 显示 HAMLET 在 OpenVLA 和 π₀-FAST 上同样有效，但作者指出当前设计主要针对扩散型 VLA 优化，自回归模型的 token 序列结构可能需要更精细的适配策略。

## 定位与知识库关联

### 1. 方法谱系：从单帧 VLA 到历史感知策略

HAMLET 的核心定位是**预训练 VLA 的历史感知微调框架**，其设计动机源于对当前 VLA 范式根本瓶颈的诊断：主流 VLA 模型仅基于单帧观测进行决策，缺乏对历史上下文的利用，导致在需要多步推理或存在遮挡的非马尔可夫任务中系统性失败。直接追加多帧输入虽能引入历史信息，但会显著增加计算开销并损害模型在分布外场景的泛化能力。

HAMLET 在方法谱系中占据以下位置：

- **上游基础模型**：HAMLET 构建于预训练 VLA 之上，主要验证的骨干网络包括 **GR00T N1.5**（Bjorck et al., 2025a）、**GR00T N1**（Bjorck et al., 2025b）、**CogACT**（Li et al., 2024a）、**OpenVLA**（Kim et al., 2024）、**π0**（Black et al., 2025）和 **π0-FAST**（Pertsch et al., 2025）。这些模型覆盖了扩散型与自回归型两大 VLA 类别，HAMLET 通过统一的输入扩展和记忆模块设计，在不修改 VLM 主干的前提下实现历史感知能力的注入。

- **朴素多帧基线**：最直接的对比点是直接将多帧图像拼接输入 VLA 的朴素方案。该基线在 RoboCasa 上导致性能下降 3.3%，在 LIBERO 上下降 8.8%，暴露了简单堆叠历史帧会引入冗余视觉信息、干扰 VLM 特征提取的缺陷。HAMLET 通过 moment tokens 的压缩机制和记忆模块的选择性聚合，以单帧输入的计算代价获得历史感知能力，在效率上实现了数量级优势（历史长度 4 时延迟仅 1.02×，内存约 2×；而多帧基线分别为 1.5× 延迟和 3.6× 内存）。

- **时间对比学习的继承与发展**：Moment tokens 的初始化借鉴了时间对比学习（Time-Contrastive Learning, Sermanet et al., 2018）的思想，但将其从独立的表示学习阶段嵌入到 VLA 微调流程中。与原始 TCL 用于学习解耦的时间不变特征不同，HAMLET 利用 TCL 鼓励 moment tokens 捕获时间区分性特征——同一时间步的不同增强视图对齐，不同时间步推开——从而抑制静态背景冗余，聚焦于任务相关的动态区域。

- **记忆架构的选择**：在记忆模块设计上，HAMLET 对比了多种序列建模架构（RNN、LSTM、GRU、直接拼接），最终选择浅层因果 Transformer。消融实验表明 Transformer 实现最高平均成功率（65.4%），优于 LSTM（65.0%）和 GRU（64.3%），这归因于自注意力机制能够动态关注关键历史时刻，避免循环架构中信息衰减或同等对待所有时间步带来的干扰。

### 2. 适用边界

HAMLET 的适用边界由以下因素界定：

- **VLA 架构兼容性**：HAMLET 在扩散型 VLA（GR00T N1/N1.5、π0、π0-FAST、CogACT）上得到了充分验证，并在自回归 VLA（OpenVLA、π0-FAST 的自回归变体）上展示了初步可行性。但论文明确指出，该方法可能无法直接扩展到某些自回归 VLA 的原始架构，需要针对具体模型进行适配。

- **任务类型**：HAMLET 的核心增益集中在**历史依赖的长视距操作任务**，包括存在遮挡的抓取、多步推理的物体交换、以及需要记忆先前动作的连续操作。在接近饱和性能的基准（如 LIBERO 平均成功率 95.6%→97.6%）上仍能带来提升，证明历史感知即使在简单任务中也有边际增益。但对于纯马尔可夫任务，HAMLET 的优势可能有限。

- **数据规模**：实验覆盖了 30 到 300 个演示的数据规模。记忆模块的跨数据集泛化实验（LIBERO→RoboCasa 迁移后成功率 64.5%，接近源域训练的 65.4%）表明学习到的记忆表示具有一定泛化性，但未在大规模多任务数据上验证可扩展性。

- **计算开销**：HAMLET 保持了单帧 VLA 的推理效率优势，但需要额外的时间对比学习初始化阶段和记忆模块的训练。修改成本（参数量、训练时间）在不同 VLA 类型间存在差异，但整体轻量。

### 3. 局限与开放问题

**已识别的局限**：

1. **额外训练成本**：尽管 HAMLET 通过高效设计保持了单帧 VLA 的推理效率，但仍需时间对比学习的预初始化阶段，增加了训练流程的复杂度。

2. **自回归 VLA 的扩展性**：HAMLET 在扩散型 VLA 上验证良好，但对自回归式 VLA 的原始架构适配尚不完整，需要针对 token 化动作空间的特性进行额外设计。

3. **大规模数据验证缺失**：记忆模块的跨数据集泛化仅在两个仿真环境间验证，未在更大规模、更多样化的机器人操作数据集上测试其可扩展性。

**开放问题**：

1. **大规模扩展**：如何在大规模机器人操作数据集上扩展 HAMLET，使其在更广泛的任务分布中保持历史感知能力？

2. **记忆架构的进一步优化**：对记忆模块的架构参数进行更彻底的搜索（如混合模型、Mamba 等状态空间模型）是否能获得更高性能？

3. **统一 VLA 适配方案**：能否设计统一方案同时适用于扩散型和自回归型 VLA，减少对特定架构的适配成本？

4. **更长时间跨度任务**：HAMLET 在更长时间跨度、更复杂场景（如整个家庭环境中的连贯操作）中的表现如何？当前的历史窗口长度为 4 个动作块，更长的依赖关系是否仍能被有效捕获？

## 原文 PDF

![[paperPDFs/ICLR_2026/HAMLET_Switch_Your_Vision_Language_Action_Model_into_a_History_Aware_Policy.pdf]]
