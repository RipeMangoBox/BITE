---
title: "SocialNav: Training Human-Inspired Foundation Model for Socially-Aware Embodied Navigation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SocialNav_Training_Human_Inspired_Foundation_Model_for_Socially_Aware_Embodied_Navigation.pdf
project_link: "https://amap-eai.github.io/SocialNav/"
code_link: "https://github.com/isaacsim/IsaacSim"
aliases:
- SocialNav
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过分层脑-行动架构中VLM语义推理、条件流匹配轨迹生成及社交合规奖励的强化学习，将社交规范注入导航策略。
primary_logic: 模仿学习无法内在化社会规范；通过结合VLM认知先验与流式RL的社交合规奖励（SAFE-GRPO），智能体能够习得社会行为的因果原则而非表面模仿。
claims:
- SocialNav achieves +38% success rate and +46% social compliance rate compared to state-of-the-art.
- SAFE-GRPO with cognitive priors yields best social compliance; without cognitive priors, RL worsens social metrics.
- CityWalker Open-Loop Benchmark 上 MAOE (Mean across scenarios) = 10.2
- SocNav Closed-Loop Benchmark 上 Success Rate (SR) = 86.1
---

# SocialNav: Training Human-Inspired Foundation Model for Socially-Aware Embodied Navigation

> [!tip] 核心洞察
> 模仿学习无法内在化社会规范；通过结合VLM认知先验与流式RL的社交合规奖励（SAFE-GRPO），智能体能够习得社会行为的因果原则而非表面模仿。

| 字段 | 内容 |
|------|------|
| 中文题名 | SocialNav：训练面向社交感知的具身导航基础模型 |
| 英文题名 | SocialNav: Training Human-Inspired Foundation Model for Socially-Aware Embodied Navigation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.21135) · [Project](https://amap-eai.github.io/SocialNav/) · [Code](https://github.com/isaacsim/IsaacSim) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SocialNav |
| Dataset | CityWalker Open-Loop Benchmark, SocNav Closed-Loop Benchmark, Real-World Deployment |

> [!tip] 效果简介
> - CityWalker Open-Loop Benchmark 上，MAOE (Mean across scenarios) 10.2 vs 15.2 (CityWalker) (-5.0)。
> - SocNav Closed-Loop Benchmark 上，Success Rate (SR) 86.1 vs 47.8 (CityWalker) (+38.3)；Distance Compliance Rate (DCR) 82.5 vs 36.1 (CityWalker) (+46.4)。
> - Real-World Deployment (3 environments) 上，Average Success Rate 85.0 vs 62.5 (CityWalker) (+22.5)。

## 概要

现有具身导航模型大多以几何最短路径为唯一优化目标，缺乏对社会规范的显式建模，导致机器人在真实环境中频繁出现闯红灯、穿越禁行区、踩踏草坪等不符合人类预期的行为。这一瓶颈的根源在于，纯模仿学习只能复现训练分布中的表面动作模式，无法内在化社会规范的因果原则。

SocialNav 提出了一套分层脑-行动基础模型架构，将社交规范注入导航策略。其核心洞察是：通过视觉语言模型（VLM）提供高层语义推理与认知先验，再结合条件流匹配（Conditional Flow Matching）扩散 Transformer 生成多模态轨迹，最后以社交合规奖励驱动的强化学习（SAFE-GRPO）进行对齐，智能体能够习得社会行为的因果原则而非表面模仿。

实验结果表明，SocialNav 在闭环 SocNav 基准上相较 SOTA 方法 CityWalker 成功率提升 **+38%**（86.1 vs 47.8），社交合规率提升 **+46%**（DCR 82.5 vs 36.1）；在真实世界部署中平均成功率亦领先 **+22.5%**（85.0 vs 62.5）。消融研究进一步证实，认知先验与 SAFE-GRPO 的组合是实现高社交合规性的关键——移除认知先验后，强化学习反而会恶化社交指标。



### 问题背景：具身导航中的社会规范盲区

具身导航（Embodied Navigation）是机器人自主性的核心能力之一，要求智能体在真实环境中从当前位置安全、高效地抵达目标点。近年来，基于模仿学习（Imitation Learning, IL）的点目标导航（Point-Goal Navigation）方法取得了显著进展，代表性工作包括 **GNM**、**ViNT**、**NoMaD** 和 **CityWalker** 等。这些方法通过从大规模专家轨迹中学习映射函数，能够在多样化的室内外场景中生成几何意义上最短或最优的路径。

然而，几何最优并不等同于行为合理。真实世界中的导航远不止避障和路径规划——它深深嵌入在人类社会的规范体系之中。一个在几何上完美的路径可能穿过草坪、闯入车道、横穿马路或在人行道上逆行，这些行为虽然在物理上可行，却严重违反了社会公约。现有导航模型的核心瓶颈正在于此：**它们仅追求几何最优路径，缺乏对社会规范的遵守能力，易产生闯红灯、穿越禁行区等不合理行为**。这种“社会盲视”使得当前最先进的导航策略难以直接部署到与人共存的真实环境中。

### 现有方法的根本缺口：模仿学习无法内化社会规范

当前主流的导航模型几乎全部采用行为克隆（Behavior Cloning）范式，即通过回归专家轨迹来学习导航策略。这一范式存在一个根本性的局限：**模仿学习只能复现训练数据中出现的表面行为模式，而无法理解驱动这些行为背后的因果原则**。在社会导航场景中，这意味着模型可能在某些情况下恰好走在人行道上（因为训练数据中专家如此），但一旦遇到分布外场景——例如人行道被临时占用、路口没有明确标识——模型就会退化为纯粹的几何规划器，选择最短而非最合规的路径。

更深层的问题在于，社会规范本身具有高度的上下文依赖性。在斑马线前等待、为行人让路、避开私人领地等行为，需要智能体具备对场景语义的理解能力——识别“这是人行道”、“那是车道”、“前方是交叉路口”——以及基于这些理解做出因果推理的能力。纯端到端的行为克隆架构缺乏这种语义理解和推理机制，因此无法将社会规范真正“内化”为策略的一部分。

### 本文动机：注入社会认知的导航基础模型

针对上述缺口，本文提出 **SocialNav**——一个面向社交感知的具身导航基础模型。其核心动机是：**通过将视觉语言模型（VLM）的语义推理能力与可流式强化学习的社交合规奖励相结合，使导航智能体能够习得社会行为的因果原则，而非停留在表面模仿**。

SocialNav 的设计围绕三个关键认知展开：

1. **高层语义推理是社交导航的前提**：智能体首先需要“理解”场景中的社会结构——哪里是可通行的公共区域，哪里是禁入的私人空间，哪里是安全的过街位置。这一能力通过 VLM 脑模块（Brain Module）实现，该模块能够生成社交可穿越区域（socially traversable zones）和导航思维链（Chain-of-Thought）解释。

2. **轨迹生成需要多模态性**：社会合规的导航路径往往不是唯一的，智能体需要在多个可接受的行为选项中进行选择。为此，SocialNav 采用条件流匹配（Conditional Flow Matching）扩散 Transformer 作为动作专家（Action Expert），生成多样化且符合语义条件的轨迹。

3. **社交规范必须通过奖励驱动的方式对齐**：模仿学习提供了基础导航能力，但要真正习得社会规范，需要引入社交合规奖励信号。SocialNav 提出 **SAFE-GRPO**（Socially-Aligned Flow Exploration with GRPO）流式强化学习阶段，通过将确定性 ODE 转化为随机微分方程（SDE）实现可控探索，并结合基于距离变换图的社交合规奖励函数，使智能体在保持导航效率的同时最大化社会合规性。

### 关键证据预览

SocialNav 在多个维度上验证了上述动机的有效性。在闭环 SocNav Benchmark 上，SocialNav 相比 SOTA 方法 **CityWalker** 实现了 **+38% 的成功率提升**和 **+46% 的社交合规率提升**（DCR 从 36.1 提升至 82.5）。消融实验进一步揭示了核心洞察：**在缺乏认知先验（Cognitive Activation Dataset, D_cog）的情况下直接应用 SAFE-GRPO 强化学习，反而会损害社交指标**（DCR 下降 1.7，TCR 下降 1.3）；只有当 VLM 提供的认知先验与社交合规奖励共同作用时，才能获得最佳的社交合规表现。这有力地证明了“理解场景语义”与“奖励驱动对齐”两者缺一不可——正是这一组合机制使 SocialNav 超越了模仿学习的表面复现，实现了对社会规范的因果性内化。



## 核心方法与创新机理

SocialNav 的核心创新在于**将社交规范从“表面模仿”提升为“因果对齐”**。现有导航方法（如 GNM、ViNT、NoMaD、CityWalker）仅通过行为克隆追求几何最优路径，缺乏对社会规范的语义理解，导致闯红灯、穿越禁行区等不合理行为。SocialNav 通过三个关键的 **changed slots** 系统性地解决了这一瓶颈。

### 1. 高层语义推理：VLM 脑模块注入社交认知先验

传统方法无显式社交推理，仅依赖观测-动作的端到端映射。SocialNav 引入基于视觉语言模型（VLM）的 **Brain Module**，将社交规范编码为可操作的语义先验。该模块以 Qwen2.5-VL (3B) 为核心，接收历史观测 $\mathcal{O}_{t-n:t}$、位置序列 $P_{t-n:t}$ 和目标 $g$，输出两个关键信息：

- **社交可穿越区域**：识别人行道、斑马线等符合社会规范的通行区域，排除车道、草坪等禁行区；
- **导航思维链（CoT）**：生成结构化的推理过程，显式权衡安全性（如“不横穿马路”）与效率，为下游动作生成提供可解释的语义条件。

这一设计使得模型不再盲从轨迹数据的表面统计规律，而是具备了对场景社交属性的语义判别能力。

### 2. 动作生成模型：条件流匹配替代确定性回归

传统方法采用直接回归或确定性策略生成轨迹，输出单一且缺乏对多模态社交约束的适应能力。SocialNav 的 **Action Expert** 采用条件流匹配（Conditional Flow Matching）构建扩散 Transformer（12 层、12 注意力头、隐藏维度 1536），将动作生成形式化为从简单分布到目标轨迹分布的概率流：

$$\mathbf{A}_{t+1:t+m} = \pi_{\mathrm{flow}}(\mathbf{x}_t, t; \mathbf{Z}_{\mathrm{VLM}})$$

其中 $\mathbf{Z}_{\mathrm{VLM}}$ 为 VLM 提取的潜在语义特征。流匹配使模型能够生成覆盖多种合规路径的多模态轨迹分布，而非单一“平均”路径，从而在复杂社交场景中保持灵活性。

### 3. 训练策略：SAFE-GRPO 实现社交规范的因果对齐

这是 SocialNav 最关键的范式转变。传统方法仅依赖模仿学习（IL）拟合专家轨迹，但消融实验（Table 4）揭示了一个核心发现：**纯 IL 无法内在化社交规范**——当在 IL 基础上直接施加 RL（不含认知先验）时，社交指标反而恶化（DCR -1.7, TCR -1.3）。

SocialNav 的三阶段训练策略解决了这一矛盾：

- **Stage 1（预训练）**：在大规模轨迹与认知数据上激活基础导航能力；
- **Stage 2（微调）**：使用高质量真实机器人数据缩小仿真-真实差距；
- **Stage 3（SAFE-GRPO）**：通过将确定性 ODE 转为随机微分方程实现可控探索：
  $$d\mathbf{x}_t = \mathbf{v}_{\mathrm{flow}}(\mathbf{x}_t, t; \mathbf{Z}_{\mathrm{VLM}}) dt + \sigma_t d\mathbf{w}_t$$
  并引入社交合规奖励 $\mathcal{R}_{\mathrm{social}}$（基于距离变换图，sigmoid 缩放），使智能体习得社交行为的**因果原则**而非表面模仿。

消融实验（Table 4）证实：仅当认知激活数据集（$D_{\mathrm{cog}}$）与 SAFE-GRPO 结合时，社交合规性达到最优（DCR 82.5, TCR 82.9），而单独使用 RL 或单独使用认知数据均无法达到此效果。这表明 **VLM 认知先验为 RL 提供了必要的语义约束，RL 则将先验转化为可执行的因果行为**。

### 创新总结

SocialNav 的三个 changed slots 形成了一条因果链：VLM 提供社交语义理解（**知道什么是对的**），流匹配生成多模态候选（**能够做到对的**），SAFE-GRPO 通过奖励机制将对的行为固化为策略（**愿意做对的**）。这一设计使得 SocialNav 在 SocNav 闭环基准上相比 CityWalker 实现成功率 +38.3%、社交合规率 +46.4% 的跃升，并在真实世界部署中保持 85% 的平均成功率。



SocialNav 采用**分层脑-行动架构（hierarchical brain-action architecture）**，将高层语义推理与底层轨迹生成解耦，如图 Figure 3 所示。该架构由两个核心模块串联构成：

![[assets/figures/papers/paper_list_l2095_https_arxiv_org_abs_2511_21135/figures/003_Figure_3.jpg]]
*Figure 3: SocialNav Architecture and Training Pipeline. SocialNav adopts a hierarchical architecture, with a VLM-based Brain for high-level semantic reasoning and an action expert for generating socially compliant trajectories. We adopt a three-stage training strategy: Pre-training, Fine-tuning, and SAFE-GRPO*

1. **Brain Module（脑模块）**：基于视觉语言模型（VLM）构建，负责从历史观测中提取社交导航先验。输入为过去 $n$ 帧的视觉观测 $\mathcal{O}_{t-n:t}$ 与位置序列 $P_{t-n:t}$，以及目标 $g$，输出为潜在语义特征 $\mathbf{Z}_{\mathrm{VLM}}$ 和社交可穿越区域的思维链（CoT）解释。该模块赋予模型“理解社交规范”的能力，而非仅追求几何最短路径。

2. **Action Expert（行动专家）**：基于条件流匹配（Conditional Flow Matching）的扩散 Transformer，以脑模块输出的语义特征 $\mathbf{Z}_{\mathrm{VLM}}$ 为条件，从当前状态 $\mathbf{x}_t$ 出发，生成未来 $m$ 步的动作序列 $\mathbf{A}_{t+1:t+m}$。该模块将高层语义意图转化为符合社交规范的多模态轨迹。

整体信息流可概括为：

$$\mathbf{Z}_{\mathrm{VLM}} = \pi_{\mathrm{VLM}}(\mathcal{O}_{t-n:t}, P_{t-n:t}, g) \quad \rightarrow \quad \mathbf{A}_{t+1:t+m} = \pi_{\mathrm{flow}}(\mathbf{x}_t, t; \mathbf{Z}_{\mathrm{VLM}})$$

**输入**：历史观测序列、历史位置序列、导航目标。
**输出**：未来动作序列（含线速度和角速度），以及可选的思维链解释。

这种设计的关键因果机制在于：VLM 提供的语义条件并非简单的特征拼接，而是将“何处可走”与“何处应走”的社交认知先验注入轨迹生成过程，使模型从纯几何导航转向社交感知导航。消融实验证实，移除 VLM 认知先验后，即使使用强化学习训练，社交合规指标反而下降（DCR $-1.7$，TCR $-1.3$），验证了脑模块作为社交规范注入瓶颈的不可替代性。

模型的具体参数配置见 Table 5：脑模块采用 **Qwen2.5-VL (3B)**，行动专家为 12 层、12 注意力头、隐藏维度 1536 的扩散 Transformer。部署时整体推理频率超过 5 Hz，满足实时导航需求。

![[assets/figures/papers/paper_list_l2095_https_arxiv_org_abs_2511_21135/figures/013_Table_5.jpg]]
*Table 5: Model Architecture and Parameters*

### 补充图表

![[assets/figures/papers/paper_list_l2095_https_arxiv_org_abs_2511_21135/figures/001_Figure_1.jpg]]
*Figure 1: Socially-Aware Navigation in Real-World Environments. SocialNav combines high-level semantic reasoning with low-level trajectory generation. It identifies socially traversable zones and generates CoT explanations, planning routes that respect social norms*



### 问题形式化

SocialNav 将社交感知导航建模为从历史观测到未来动作的映射。给定过去 $n$ 步的观测 $\mathcal{O}_{t-n:t}$ 与位置 $P_{t-n:t}$，以及导航目标 $g$，策略 $\pi_\theta$ 预测未来 $m$ 步的动作序列：

$$A_{t+1:t+m} = \pi_{\theta}(\mathcal{O}_{t-n:t}, P_{t-n:t}, g) \tag{1}$$

该形式化的核心挑战在于：动作序列不仅需要满足几何可达性，还必须遵守场景中的社交规范（如不穿越草坪、不闯红灯、沿人行道行进）。SocialNav 通过分层架构将这一映射分解为语义推理与轨迹生成两个耦合阶段。

### 脑模块（Brain Module）：VLM 语义推理

脑模块是整个架构的认知核心，基于视觉语言模型（VLM）构建。其功能是将原始观测转化为富含社交语义的潜在表征。具体而言，VLM 接收历史观测帧 $\mathcal{O}_{t-n:t}$、位置序列 $P_{t-n:t}$ 和目标 $g$，输出潜在语义特征 $\mathbf{Z}_{\mathrm{VLM}}$：

$$\mathbf{Z}_{\mathrm{VLM}} = \pi_{\mathrm{VLM}}(\mathcal{O}_{t-n:t}, P_{t-n:t}, g) \tag{2}$$

这些特征编码了场景中的社交可穿越区域（socially traversable zones）、障碍物语义类型，以及符合社会规范的路径选择倾向。与直接输出控制指令的端到端模型不同，脑模块还生成结构化的导航思维链（Chain-of-Thought），显式地推理安全约束与社交规范之间的优先级——例如在路口场景中优先选择人行横道而非直接穿越马路。

### 行动专家（Action Expert）：条件流匹配扩散 Transformer

行动专家负责将脑模块的语义先验转化为可执行的多模态轨迹。其核心生成机制采用条件流匹配（Conditional Flow Matching），以扩散 Transformer 为骨干网络。

给定当前状态 $\mathbf{x}_t$ 和扩散时间步 $t$，模型在 VLM 语义特征 $\mathbf{Z}_{\mathrm{VLM}}$ 的条件下预测未来动作序列：

$$\mathbf{A}_{t+1:t+m} = \pi_{\mathrm{flow}}(\mathbf{x}_t, t; \mathbf{Z}_{\mathrm{VLM}}) \tag{3}$$

条件流匹配的本质是学习一个从简单先验分布到目标轨迹分布的连续归一化流。在推理时，模型从噪声出发，通过求解常微分方程逐步去噪，生成符合语义条件约束的动作序列。扩散 Transformer 采用 12 层结构，每层 12 个注意力头，隐藏维度为 1536，为多模态轨迹分布建模提供了足够容量。

### SAFE-GRPO：流式探索与社交合规对齐

第三阶段的对齐训练是 SocialNav 区别于纯模仿学习方法的关键。SAFE-GRPO 将确定性流匹配的 ODE 扩展为随机微分方程（SDE），引入可控的探索噪声：

$$d\mathbf{x}_t = \mathbf{v}_{\mathrm{flow}}(\mathbf{x}_t, t; \mathbf{Z}_{\mathrm{VLM}}) dt + \sigma_t d\mathbf{w}_t \tag{4}$$

其中 $\sigma_t$ 控制探索强度，$d\mathbf{w}_t$ 为标准维纳过程。这一设计使得智能体能够在轨迹空间中进行结构化探索，而非在动作空间中盲目随机采样。

探索产生的轨迹由复合奖励函数评估：

$$\mathcal{R} = \mathcal{R}_{\mathrm{social}} + \lambda_{\mathrm{expert}} \mathcal{R}_{\mathrm{expert}} + \lambda_{\mathrm{smooth}} \mathcal{R}_{\mathrm{smooth}} + \lambda_{\mathrm{eff}} \mathcal{R}_{\mathrm{eff}} \tag{5}$$

其中 $\mathcal{R}_{\mathrm{social}}$ 是社交合规奖励，基于距离变换图（distance transform map）量化轨迹与社交可穿越区域的偏离程度；$\mathcal{R}_{\mathrm{expert}}$ 鼓励与专家轨迹的一致性；$\mathcal{R}_{\mathrm{smooth}}$ 惩罚动作序列的不平滑；$\mathcal{R}_{\mathrm{eff}}$ 奖励路径效率。消融实验（Table 8）表明，移除 $\mathcal{R}_{\mathrm{social}}$ 会导致社交合规指标显著下降，验证了该奖励项的核心作用。

### 社交合规度量：DCR 与 TCR

为量化评估社交合规性，SocialNav 引入了两个关键度量。距离合规率（Distance Compliance Rate, DCR）定义为成功完成的任务中，在社交可穿越区域内行进距离的比例：

$$\mathrm{DCR} = \begin{cases} \frac{d_{\mathrm{compliant}}}{d_{\mathrm{actual}}}, & \text{if } s = 1 \\ 0, & \text{otherwise} \end{cases} \tag{6}$$

其中 $s=1$ 表示任务成功，$d_{\mathrm{compliant}}$ 为合规区域内的行进距离，$d_{\mathrm{actual}}$ 为实际总行进距离。类似地，时间合规率（TCR）从时间维度度量社交规范的遵守程度。这两个度量共同构成了 SocNav 基准的社交合规评估体系，与传统的成功率（SR）和路径长度加权成功率（SPL）形成互补。

### 补充图表

![[assets/figures/papers/paper_list_l2095_https_arxiv_org_abs_2511_21135/figures/012_Figure_8.jpg]]
*Figure 8: Example of a navigation chain-of-thought (CoT) in an unseen crossing scenario. Given the historical observations (left) and a goal in the forward-right direction, the Brain Module generates a structured CoT (right). The CoT demonstrates hierarchical decisionmaking, prioritizing Safety (no jaywalking) and Social Compliance (using the crosswalk) over direct path efficiency*

![[assets/figures/papers/paper_list_l2095_https_arxiv_org_abs_2511_21135/figures/010_Figure_6.jpg]]
*Figure 6: Predicted socially traversable regions on unseen scenes. Green polygons denote predicted socially traversable regions, and red arrows highlight areas incorrectly classified as traversable. SocialNav yields more semantically aligned polygons in both domains*



## 实验与关键发现

### 核心实验设置

SocialNav 的脑模块采用 **Qwen2.5-VL (3B)**，行动专家为 12 层、12 注意力头、隐藏维度 1536 的扩散 Transformer，通过条件流匹配生成多模态轨迹。训练分三阶段：大规模预训练、真实数据微调、SAFE-GRPO 强化学习对齐。推理时系统以超过 5 Hz 运行，满足实时部署需求。

### 开环评估：CityWalker 基准

在 CityWalker 开环基准上，SocialNav (Full) 在所有方法中取得最低的平均角误差（MAOE），场景均值 10.2，全样本均值 7.8，较 CityWalker 基线（均值 15.2）降低 5.0（Table 1）。该基准涵盖六种关键场景，SocialNav 在狭窄通道、路口等社交约束密集的场景中优势尤为显著。

![[assets/figures/papers/paper_list_l2095_https_arxiv_org_abs_2511_21135/figures/004_Table_1.jpg]]
*Table 1: Open-Loop Evaluation on CityWalker Benchmark [24]. We evaluate MAOE metric in each critical scenario for all methods. Percentages under scenarios indicate their data proportions. The ”Mean” column shows scenario means averaged over six scenarios; ”All” shows sample means over all data samples*

### 闭环评估：SocNav 基准

闭环 SocNav 基准综合评估导航性能与社交合规性。SocialNav (Full) 取得 **86.1% 成功率（SR）** 和 **91.2% 路线完成率（RC）**，较 CityWalker 的 47.8% SR 提升 +38.3 个百分点（Table 2）。在社交合规指标上，SocialNav 的距离合规率（DCR）达 82.5%，轨迹合规率（TCR）达 82.9%，均超过 CityWalker（DCR 36.1%）的两倍以上。SPL 为 77.4%，表明路径效率与社交规范遵守之间存在可接受的权衡。

![[assets/figures/papers/paper_list_l2095_https_arxiv_org_abs_2511_21135/figures/005_Table_2.jpg]]
*Table 2: Performance Comparison on the Closed-Loop SocNav Benchmark*

定性对比（Figure 4）直观展示了这一差异：在路口、公园、校园三个场景中，SocialNav（绿色轨迹）始终保持在人行道和步道上，而 CityWalker（红色轨迹）频繁穿越车道、干涸河床、草坪等禁行区域，甚至撞向玻璃幕墙或树木。

![[assets/figures/papers/paper_list_l2095_https_arxiv_org_abs_2511_21135/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison on the SocNav Benchmark. We visualize representative trajectories in three scenes (Crossing, Park, Campus). The left column shows top-down path views with our method (green) and the CityWalker baseline (red), where warning signs mark unsafe or socially improper behaviors. The right columns depict corresponding egocentric views: SocialNav remains on sidewalks and walkways, while the baseline often takes shorter but socially risky routes through restricted regions (such as driveways, dry streambeds, lawns, and green belts) or crashes into obstacles like glass walls and trees*

### 真实世界部署

在街道、公园、校园三类真实环境中部署于 Unitree Go2 机器人，SocialNav 平均成功率达 **85.0%**，较 CityWalker 的 62.5% 提升 +22.5 个百分点（Table 3）。机器人成功遵循人行道、避让草坪和车道、尊重行人流向，验证了仿真到真实的有效迁移。

![[assets/figures/papers/paper_list_l2095_https_arxiv_org_abs_2511_21135/figures/007_Table_3.jpg]]
*Table 3: Real-world Results. Comparison of success rates across different real-world environments*

### 消融研究：数据组成与训练阶段

Table 4 揭示了各组件对性能的因果贡献：

![[assets/figures/papers/paper_list_l2095_https_arxiv_org_abs_2511_21135/figures/008_Table_4.jpg]]
*Table 4: Ablation Study on Data Composition and Training Stages. IL: Imitation Learning (Stages 1–2); RL: SAFE-GRPO (Stage 3). SocialNav* is trained with IL only on*

1. **认知激活数据集（D_cog）的作用**：在纯模仿学习（IL）设置下，加入 D_cog 使 DCR 提升 +8.4、TCR 提升 +10.2（No.4 vs No.3），证明 VLM 生成的思维链先验对社交推理具有独立价值。
2. **RL 与认知先验的耦合**：仅用 D_real 进行 SAFE-GRPO 而不引入 D_cog（No.5），社交指标反而下降（DCR -1.7, TCR -1.3），说明**缺乏认知先验的 RL 会破坏社交行为**。同时引入 D_cog 与 SAFE-GRPO（No.6）则取得最佳社交合规（DCR 82.5, TCR 82.9）和导航性能（SR 86.1）。
3. **数据金字塔的贡献**：从仅用 D_real（No.1）逐步扩展至完整 ETP 金字塔（No.3），SR 从 54.8 提升至 75.4，RC 从 70.2 提升至 88.6，验证了大规模多样化轨迹预训练的基础作用。

### 奖励函数消融

Table 8 对 SAFE-GRPO 的四个奖励项逐一消融。社交合规奖励 $\mathcal{R}_{\mathrm{social}}$ 的移除导致 DCR 和 TCR 出现最大幅度下降，确认其是社交行为对齐的核心驱动项。专家一致性奖励 $\mathcal{R}_{\mathrm{expert}}$ 主要影响 SR 和 RC，平滑性奖励 $\mathcal{R}_{\mathrm{smooth}}$ 和效率奖励 $\mathcal{R}_{\mathrm{eff}}$ 的移除则主要影响 SPL 和轨迹质量。

![[assets/figures/papers/paper_list_l2095_https_arxiv_org_abs_2511_21135/figures/016_Table_8.jpg]]
*Table 8: Ablation on SAFE-GRPO reward components on the SocNav Benchmark. We deactivate each reward term in turn by setting its weight to zero. Checkmarks indicate that the reward is used*

### 失败模式与局限

强化学习阶段在提升社交合规性的同时轻微牺牲路径效率（SPL 从 79.4 降至 77.4），体现了直接性与社交规范遵守之间的固有张力。在高度动态、多人交互场景中，当前 VLM 推理的上下文窗口有限，可能导致对行人意图的误判。此外，RL 奖励信号依赖预定义的社交可穿越区域图，对未建模的社会约定（如礼仪性避让）泛化能力不足。

### 补充图表

![[assets/figures/papers/paper_list_l2095_https_arxiv_org_abs_2511_21135/figures/018_Figure_9.jpg]]
*Figure 9: Real-world deployment visualizations. Third-person views of the Unitree Go2 robot navigating in street, park, and campus environments. SocialNav successfully follows sidewalks, avoids stepping onto lawns or driveways, respects pedestrian flows*



## 定位与知识库关联

### 与基线方法的关系

SocialNav 的核心目标是将**社交规范**注入具身导航策略，这与现有端到端导航模型形成根本性差异。基线方法 **GNM**、**ViNT**、**NoMaD** 和 **CityWalker**（具体作者/会议信息需手动核实）均采用纯模仿学习（行为克隆）范式，其策略仅追求几何最优路径，缺乏对社会规范的推理能力。实验证据表明，这些基线在 SocNav 闭环基准上的成功率（SR）仅为 47.8%（CityWalker），社交合规率（DCR 36.1%、TCR 36.0%）严重不足，常产生穿越草坪、闯入车道等违规行为（见 Figure 4 定性对比）。

SocialNav 通过三个关键设计突破这一瓶颈：

1. **高层语义推理**：引入基于 VLM 的 Brain Module（Qwen2.5-VL 3B），将社交可穿越区域预测与思维链（CoT）推理作为动作生成的条件先验，而基线方法无显式社交推理。
2. **动作生成模型**：采用条件流匹配（Conditional Flow Matching）扩散 Transformer 替代直接回归策略，生成多模态、社交合规的轨迹分布。
3. **训练策略**：以三阶段训练（预训练→微调→SAFE-GRPO 流式 RL）取代纯模仿学习，其中 SAFE-GRPO 阶段通过社交合规奖励函数实现规范对齐。

消融实验（Table 4）揭示了方法谱系中的关键因果机制：**模仿学习无法内在化社会规范**。当仅在真实数据上使用 IL 训练时（SocialNav*），DCR 为 74.1%；若在无认知先验（D_cog）的条件下直接施加 SAFE-GRPO，社交指标反而恶化（DCR -1.7、TCR -1.3）。唯有结合 VLM 认知先验与 SAFE-GRPO 时，社交合规率达到最优（DCR 82.5、TCR 82.9）。这表明 RL 本身不是充分条件，认知先验为奖励信号提供了语义锚定，使智能体能够习得社会行为的因果原则而非表面模仿。

### 适用边界与局限

SocialNav 的适用边界受以下因素制约：

- **场景依赖性**：模型在 SocNav 基准覆盖的街道、公园、校园等结构化室外场景表现优异（真实世界平均 SR 85.0%），但其在高度动态、密集人群交互场景中的泛化能力未经充分验证。
- **效率-合规权衡**：RL 阶段在提升社交合规性的同时会轻微牺牲路径效率，SPL 从 79.4 降至 77.4（Table 4 No.3 vs No.6），体现了直接性与规范遵守之间的内在张力。
- **VLM 依赖性**：Brain Module 的推理质量受限于底层 VLM 的能力边界，在语义模糊或未见过的场景布局中，社交可穿越区域预测可能出现误判（见 Figure 6 红色箭头标注的错误分类区域）。
- **计算约束**：系统部署时运行频率超过 5 Hz，满足实时性要求，但 VLM 推理与扩散 Transformer 采样的联合计算负载可能限制其在资源受限平台上的应用。

### 开放问题与后续方向

论文明确指出了两个开放问题，为后续工作提供了方向：

1. **更广泛社会约定的泛化**：如何将 SAFE-GRPO 范式扩展到行人优先、礼仪性避让等上下文相关的人类约定？当前奖励函数主要依赖距离变换图（sigmoid 缩放）编码空间合规性，对时序性、交互性的社会规范建模不足。
2. **VLM 驱动的自适应奖励**：如何整合视觉语言模型以提供更丰富、自适应的奖励信号？现有社交合规奖励 $\mathcal{R}_{\mathrm{social}}$ 基于预定义的距离变换图，若能利用 VLM 在线评估轨迹的社会合理性，可实现更强的以人为本对齐。

此外，从方法谱系角度看，SocialNav 开创了“VLM 认知先验 + 流式 RL 对齐”的范式，后续工作可沿以下路径延伸：（1）将 Brain Module 升级为更强的 VLM 或引入多模态社会线索（如行人意图预测）；（2）设计更细粒度的社交奖励组件，解耦不同类型的规范违反；（3）探索离线 RL 或偏好对齐方法以降低在线探索的安全风险。



## 原文 PDF

![[paperPDFs/CVPR_2026/SocialNav_Training_Human_Inspired_Foundation_Model_for_Socially_Aware_Embodied_Navigation.pdf]]
