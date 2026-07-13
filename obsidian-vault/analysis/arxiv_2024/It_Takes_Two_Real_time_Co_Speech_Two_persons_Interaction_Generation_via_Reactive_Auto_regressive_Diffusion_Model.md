---
title: "It Takes Two: Real-time Co-Speech Two-person’s Interaction Generation via Reactive Auto-regressive Diffusion Model"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/It_Takes_Two_Real_time_Co_Speech_Two_persons_Interaction_Generation_via_Reactive_Auto_regressive_Diffusion_Model.pdf
project_link: null
code_link: null
aliases:
- RARDM
tags:
- arxiv_2024
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 自回归扩散框架结合分离式多条件输入（自身历史动作、未来轨迹、伙伴动作与语音），并通过分类器自由引导（随机掩码）机制，使得系统能够实时响应伙伴动作并生成协调的互动。
primary_logic: 将伙伴的过去动作与未来语音作为条件，并利用独立预测的轨迹作为空间引导，通过自回归滑动窗口和轨迹混合策略，首次实现了从语音到双人全身实时交互运动的在线生成。
claims:
- 在单人协同语音任务（BEAT数据集）上，本方法以FPD 12.85显著优于最佳基线EMAGE的18.80，同时推理时间仅4ms。
- 在双人语音驱动运动任务（InterACT++）上，FPD 47.74远低于Audio2Photoreal的130.63和LDA的89.42，且FDD 117.88表明互动质量最高。
- 用户研究中，本方法在语音-动作对齐（75.2%）、动画质量（62.4%）和交互性（82.5%）上均获最高偏好。
- BEAT (单人协同语音) 上 FPD↓ = 12.85
---

# It Takes Two: Real-time Co-Speech Two-person’s Interaction Generation via Reactive Auto-regressive Diffusion Model

> [!tip] 核心洞察
> 将伙伴的过去动作与未来语音作为条件，并利用独立预测的轨迹作为空间引导，通过自回归滑动窗口和轨迹混合策略，首次实现了从语音到双人全身实时交互运动的在线生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 两人配合：基于反应式自回归扩散模型的实时协同语音双人交互生成 |
| 英文题名 | It Takes Two: Real-time Co-Speech Two-person’s Interaction Generation via Reactive Auto-regressive Diffusion Model |
| 会议/期刊 | arXiv 2024 |
| Links |  |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Reactive Auto-regressive Diffusion Model (反应式自回归扩散模型) |
| Dataset | BEAT, InterACT++ |

> [!tip] 效果简介
> - BEAT (单人协同语音) 上，FPD↓ 12.85 vs 18.80 (EMAGE) (5.95)；Beat Align↑ 0.79 vs 0.79 (AMUSE/EMAGE) (0.00 (持平最佳))。
> - InterACT++ (双人语音到运动) 上，FPD↓ 47.74 vs 89.42 (LDA) (41.68)；FDD↓ 117.88 vs 563.27 (Audio2Photoreal) (445.39)。
> - InterACT++ (交互运动生成) 上，FPD↓ 103.19 vs N/A (其他方法未提供音频条件，不直接可比) (N/A)。

## 概要

**问题瓶颈**：现有协同语音动作生成方法聚焦单人场景，无法建模对话双方的实时互动关系；且多为离线序列模型，需完整语音输入，不具备对伙伴动作与语音变化的在线反应能力。同时，已有数据集缺乏握手、拥抱等动态双人交互行为，进一步限制了模型学习。

**核心洞察**：将伙伴的过去动作与未来语音作为条件，并利用独立预测的地面轨迹作为空间引导，通过自回归滑动窗口与轨迹混合策略，首次实现了从语音到双人全身实时交互运动的在线生成。

**方法定位**：提出**反应式自回归扩散模型**（Reactive Auto-regressive Diffusion Model），属于扩散生成 + 自回归滑动窗口范式。系统由语音分词、轨迹预测、双流运动扩散生成器、自回归滑动窗口控制器四个模块构成。与现有方法的关键差异在于：① 生成范式从离线序列到序列转为在线滑动窗口（仅需历史帧，推理约 4 ms/剪辑，>100 fps）；② 运动范围从上肢姿势扩展至全身运动（含根位移、脚接触）；③ 条件输入从单人语音/历史动作扩展至分离式多条件令牌（自身历史动作、未来轨迹、伙伴动作与语音）；④ 训练策略引入随机掩码伙伴动作的分类器自由引导，可融合单人数据集。

**主要结果**：在单人协同语音任务（BEAT 数据集）上，本方法以 FPD 12.85 显著优于最佳基线 EMAGE 的 18.80（Table 2）。在双人语音驱动运动任务（InterACT++）上，FPD 47.74 远低于 Audio2Photoreal 的 130.63 和 LDA 的 89.42，且 FDD 117.88 表明互动质量最高（Table 3）。用户研究中，本方法在语音-动作对齐（75.2%）、动画质量（62.4%）和交互性（82.5%）上均获最高偏好（Table 6）。消融实验证实伙伴动作/语音条件与轨迹控制信号的必要性（Table 5）。

**局限与开放问题**：模型缺乏对近距离身体交互的显式物理约束，可能导致穿透或不自然接触；现有数据集无法覆盖所有交互场景；系统假设已知伙伴的未来语音特征，实际应用需额外预测模块；当前未集成面部表情。未来方向包括：不依赖未来信息的在线反应预测、融入显式物理约束、扩展至多方对话、面部与身体协同生成。

**任务背景** 语音驱动的虚拟人动作生成旨在根据语音输入合成自然的人体姿态与手势。该技术是构建沉浸式虚拟现实、数字人助手和社交交互代理的核心环节。现有方法主要聚焦于**单人协同语音动作生成**，即在给定单段语音的条件下，生成对应的上半身或全身动作。然而，真实的人类交流场景多为**多人对话**，对话者的动作不仅受自身语音驱动，还持续受到对方动作与语音的实时影响——例如点头回应、手势交替、身体朝向调整等。这种动态的、双向的交互关系，是单人模型无法捕捉的。

**现有方法缺口** 当前面向多人交互的动作生成研究存在三个关键瓶颈。其一，**生成范式离线化**：主流方法采用序列到序列架构，需要完整的语音输入才能生成完整动作序列，无法在对话进行中实时响应对方的行为变化。其二，**运动范围受限**：多数协同语音方法仅生成站立姿态下的上半身动作，忽略了对话中的空间移动、身体朝向和脚部接触等全身行为，而这些恰恰是交互自然度的核心要素。其三，**数据支撑不足**：现有双人动作数据集（如Inter-Act）虽然包含语音与运动，但场景以静态站立对话为主，缺乏握手、拥抱、共同行走等动态交互行为，限制了模型对丰富交互模式的学习。

**本文动机** 针对上述缺口，本文提出**反应式自回归扩散模型**，旨在实现从双人语音到全身交互运动的**实时在线生成**。核心思路是将伙伴的过去动作与未来语音作为条件，并引入独立预测的地面轨迹作为空间引导，通过自回归滑动窗口机制，使系统能够在仅依赖历史帧的条件下，持续产出协调、动态的双人互动。同时，为弥补数据多样性的不足，本文还构建了**InterAct++数据集**，新增402段涵盖日常对话与动态交互的双人动作序列，为模型训练与评估提供更丰富的场景覆盖。

## 核心方法与创新机理

本工作针对现有语音驱动动作生成的两大瓶颈——**无法建模对话互动关系**与**离线序列生成无法实时响应**——提出了一套从数据到模型再到推理范式的系统性创新方案。

### 1. 问题驱动的范式转变：从离线单人序列到在线双人反应式生成

现有方法（如 **CaMN**、**EMAGE**、**AMUSE**）将协同语音动作生成视为“单人-单语音”到“单人-单动作”的序列到序列映射，需要完整语音输入，且仅生成站立状态的上半身姿势。这一范式在本质上忽略了对话场景中**伙伴动作与语音对自身行为的实时影响**。

本工作将任务重新定义为**反应式自回归生成**：系统在每一时刻仅依赖历史帧信息，同时接收**自身历史动作、自身未来语音、伙伴过去动作与伙伴未来语音**作为条件，在线预测双人全身运动（含根位移与脚接触）。这一转变使得生成结果能够对伙伴的突发动作（如挥手、靠近）做出即时响应，首次实现了从语音到双人全身交互运动的实时合成。

### 2. 核心机制创新：双流分离条件与分类器自由引导

模型架构的核心创新在于**双流分离式多条件输入**与**随机掩码训练策略**，二者共同解决了“如何让模型学会响应伙伴”这一关键问题。

**双流分离条件**（Figure 3, Equation 2）将五个条件源——自身运动 $\mathbf{m}$、预测轨迹 $\mathbf{p}$、自身语音 $\mathbf{s}$、伙伴运动 $\mathbf{m}_{refer}$、伙伴语音 $\mathbf{s}_{refer}$——分别进行令牌化后拼接，送入基于 Transformer 的扩散模型 $\mathcal{G}_m$：

$$\hat{\mathbf{x}}_0 = \mathcal{G}_m(\mathbf{x}_t, t; [\mathbf{m}, \mathbf{p}, \mathbf{s}, \mathbf{m}_{refer}, \mathbf{s}_{refer}])$$

与基线方法（如 **LDA** 仅将双人语音合并为单一输入）不同，分离式设计使模型能够显式区分自身与伙伴的信息流，从而学习到“伙伴动作变化 → 自身动作调整”的因果映射。

**分类器自由引导**（Equation 3）通过训练时随机将伙伴条件 $\mathbf{m}_{refer}$ 和 $\mathbf{s}_{refer}$ 置为空 $\emptyset$，使模型同时学会条件生成与无条件生成。推理时通过引导系数 $\gamma$ 调节两者的混合比例：

$$\mathcal{G}(\mathbf{x}_t, t; c) = \mathcal{G}_m(...\emptyset...) + \gamma( \mathcal{G}_m(...) - \mathcal{G}_m(...\emptyset...) )$$

这一策略带来两个关键收益：(1) 增强模型对伙伴条件的依赖强度，提升互动质量；(2) 允许在缺少伙伴信息时退化为单人生成，使得模型可以**在单人数据集（BEAT）和双人数据集（InterACT++）上联合训练**，缓解双人数据稀缺问题。

### 3. 控制信号创新：轨迹预测作为空间引导

现有方法缺乏对人物空间位置的有效控制，生成的运动往往出现不合理的滑动或位置漂移。本工作引入**独立的轨迹预测模块**，自回归地预测双人的地面轨迹（位置与朝向），作为扩散模型的空间引导信号 $\mathbf{p}$。

消融实验（Table 5）表明，去除轨迹控制后，运动质量（FPD）和脚部稳定性（Foot Sliding）均显著下降，验证了轨迹引导对于全身运动生成的必要性。

### 4. 推理范式创新：自回归滑动窗口与混合策略

为实现实时在线生成，系统采用**自回归滑动窗口**机制：每次预测一个短时运动片段，仅将选定帧作为下一轮的历史条件。配合**轨迹混合**与**死区混合**策略（Sec. 3.3），有效抑制了自回归累积误差导致的长时漂移与抖动问题。最终系统以 8 步扩散实现每片段 4ms 的推理速度（>100fps），满足实时交互需求。

### 5. 数据层面创新：InterACT++ 数据集

现有数据集（如 BEAT）仅包含单人站立讲话动作，**Inter-Act** 虽含双人动作但缺乏动态交互行为（如握手、拥抱）。本工作采集了 **InterACT++** 数据集（402 个片段，1.7 小时，平均 15 秒/片段），覆盖多种日常对话场景中的动态双人交互，为模型学习互动行为提供了必要的数据基础（Table 1）。

本工作提出了**反应式自回归扩散模型（Reactive Auto-regressive Diffusion Model）**，首次实现了从双人语音到全身实时交互运动的在线生成。系统接收两个对话者的语音输入 $[\mathbf{S}^A, \mathbf{S}^B]$，实时输出两人的全身运动序列 $[\mathbf{M}^A, \mathbf{M}^B]$，其中运动表示包含 $N$ 帧、$J$ 个关节的旋转特征 $Q$、根节点全局位移 $\mathbb{R}^3$ 以及双脚接触标签 $\mathbb{R}^2$（Sec. 3）。

### 核心瓶颈与设计动机

现有语音驱动动作生成方法面临三重瓶颈：
1. **范式局限**：主流方法采用序列到序列架构，需完整语音输入，无法实时响应；
2. **范围受限**：仅生成站立状态的上半身姿势，缺乏全身运动（根位移、脚步接触）；
3. **交互缺失**：无法建模对话双方的动态互动关系，且现有数据集缺乏握手、拥抱等动态双人交互行为。

本框架的核心洞察在于：将**伙伴的过去动作与未来语音**作为条件，并利用**独立预测的轨迹**作为空间引导，通过自回归滑动窗口和轨迹混合策略，首次实现了从语音到双人全身实时交互运动的在线生成。

### Pipeline 模块与数据流

系统由四个核心模块串联构成，数据流如图 2 所示：

**1. 语音分词（Speech Tokenization）**
利用预训练的大规模语音模型（LSM）从原始语音中提取离散语义令牌，替代传统 Mel 频谱特征，以获得更鲁棒的语义表征。分析表明，语音分词空间中的训练-测试分布对齐优于 BERT 特征空间（Figure 7）。

**2. 轨迹预测（Trajectory Prediction）**
一个独立的预测模块，根据语音、高层活动标签及位置信号，自回归地预测两人的地面轨迹（位置与朝向），作为后续运动生成的空间引导信号。该模块将抽象的空间意图显式化，显著提升了运动质量与稳定性（消融实验证实去除轨迹后 FPD 和脚滑动指标恶化）。

**3. 双流运动扩散生成器（Dual-streaming Motion Diffusion Generator）**
这是系统的核心生成引擎，基于 Transformer 的扩散模型，在每一预测步接收**分离式多条件令牌**（自身历史运动 $\mathbf{m}$、预测轨迹 $\mathbf{p}$、自身语音特征 $\mathbf{s}$、伙伴运动 $\mathbf{m}_{refer}$、伙伴语音 $\mathbf{s}_{refer}$），通过去噪过程预测未来运动 $\hat{\mathbf{x}}_0$：

$$\hat{\mathbf{x}}_0 = \mathcal{G}_m(\mathbf{x}_t, t; [\mathbf{m}, \mathbf{p}, \mathbf{s}, \mathbf{m}_{refer}, \mathbf{s}_{refer}])$$

训练时采用**随机掩码伙伴动作**的策略，使模型同时学习条件生成与无条件生成，推理时通过分类器自由引导（Classifier-Free Guidance）调节对伙伴条件的依赖强度：

$$\mathcal{G}(\mathbf{x}_t, t; c) = \mathcal{G}_m(...\emptyset... ) + \gamma( \mathcal{G}_m(...) - \mathcal{G}_m(...\emptyset...) )$$

这种设计使系统能够**实时响应伙伴的动作变化**，同时允许融合单人数据集进行训练。

**4. 自回归滑动窗口控制器（Autoregressive Sliding Window Controller）**
为保证长时生成的稳定性与平滑过渡，系统采用滑动窗口机制：每次预测一段未来运动后，仅选取部分帧作为下一窗口的历史条件。配合轨迹混合与死区混合策略，有效抑制了自回归累积误差导致的漂移问题（Sec. 3.3, D.4）。

### 关键设计选择

| 设计维度 | 传统方法 | 本方法 |
|---------|---------|--------|
| 生成范式 | 序列到序列（需完整语音） | 自回归滑动窗口（仅需历史帧，4ms/剪辑，>100fps） |
| 运动范围 | 仅上肢姿势 | 全身运动（含根位移、脚接触） |
| 条件输入 | 单人语音/自身历史 | 增加伙伴动作、伙伴语音、预测轨迹 |
| 训练策略 | 单向依赖 | 随机掩码实现 CFG，可融合单人数据 |

这一框架从根本上改变了语音驱动动作生成的范式：从离线、单人、局部姿势的合成，转向在线、双人、全身交互的实时生成，为虚拟人对话系统提供了可行的技术路径。

### 3.1 运动表示与语音编码

系统将双人运动输出形式化为 $\mathbf{M} \in \mathbb{R}^{N \times (J \times Q + 3 + 2)}$，其中 $N$ 为帧数，$J$ 为关节数，$Q$ 为旋转特征维度，额外维度分别对应根节点全局位移（$\mathbb{R}^3$）和脚部接触标签（$\mathbb{R}^2$）。所有动作数据统一重定向至 Mixamo 骨架（65 个关节），以保证骨架一致性。

语音处理采用多尺度特征提取策略：
- **声学特征**：通过 librosa 库将语音信号转换为梅尔频谱图 $\mathbf{s}^{\mathrm{mel}} \in \mathbb{R}^{27}$，并提取基于起始振幅的节奏曲线。
- **语义特征**：利用预训练的大规模语音语言模型（Large-Speech-Model, LSM）提取离散语音语义令牌，作为高层语义条件。Figure 7 的 t-SNE 可视化表明，相比 BERT 特征，语音令牌在训练集与测试集间的分布对齐更优。

### 3.2 双流运动扩散生成器

生成器以 Transformer 为骨干网络，采用分离式令牌化策略处理多模态条件输入。核心反向扩散过程为：

$$\hat{\mathbf{x}}_0 = \mathcal{G}_m(\mathbf{x}_t, t; [\mathbf{m}, \mathbf{p}, \mathbf{s}, \mathbf{m}_{refer}, \mathbf{s}_{refer}]) \tag{2}$$

其中各变量含义如下：
- $\mathbf{x}_t$：当前噪声状态下的运动表示
- $t$：扩散时间步
- $\mathbf{m}$：自身历史运动令牌
- $\mathbf{p}$：预测的轨迹控制信号（位置与朝向）
- $\mathbf{s}$：自身语音特征令牌
- $\mathbf{m}_{refer}$：伙伴的过去运动令牌
- $\mathbf{s}_{refer}$：伙伴的未来语音特征令牌

上述条件令牌各自独立编码后，与时间步嵌入逐一拼接，送入去噪 Transformer 进行预测。Figure 3 展示了该双流架构：两人运动同时生成，每一步预测的未来运动经筛选后作为下一步的历史条件。

![[assets/figures/papers/paper_list_l1671_It_Takes_Two_Real_time_Co_Speech_Two_person_s_Interaction_Generation_via/figures/003_Figure_3.jpg]]
*Figure 3: The overview of our autoregressive motion generator. Through a dual streaming design, the motion of two persons are generated simultaneously. For each prediction step, the generative diffusion model receives a separated token as a condition to predict plausible future motion, and then the selected frames from the predicted motion are utilized as the conditions for the next step generation. Unlike other sequential generation methods, which often struggle to quickly adapt to changes in another person’s motion, our autoregressive manner can react to the partner’s motion effectively, ensuring a more realistic interaction*

### 3.3 分类器自由引导与随机掩码策略

为增强模型对伙伴条件的依赖控制，训练阶段对伙伴动作令牌 $\mathbf{m}_{refer}$ 和伙伴语音令牌 $\mathbf{s}_{refer}$ 进行随机掩码（设为 $\emptyset$），实现分类器自由引导（Classifier-Free Guidance）。推理时通过超参数 $\gamma$ 平衡条件与无条件生成：

$$\mathcal{G}(\mathbf{x}_t, t; c) = \mathcal{G}_m(\ldots \emptyset \ldots) + \gamma \left( \mathcal{G}_m(\ldots) - \mathcal{G}_m(\ldots \emptyset \ldots) \right) \tag{3}$$

该策略同时使模型能够融合单人数据集（如 BEAT）进行联合训练，缓解双人交互数据稀缺问题。

### 3.4 训练损失函数

总运动损失由五项加权组合构成：

$$\mathcal{L}_{motion} = \mathcal{L}_{samp.} + \lambda_{pos}\mathcal{L}_{pos} + \lambda_{vel}\mathcal{L}_{vel} + \mathcal{L}_{smo} + \mathcal{L}_{foot} \tag{4}$$

- $\mathcal{L}_{samp.}$：扩散样本重建损失
- $\mathcal{L}_{pos}$：关节点位置损失（权重 $\lambda_{pos}$）
- $\mathcal{L}_{vel}$：速度一致性损失（权重 $\lambda_{vel}$）
- $\mathcal{L}_{smo}$：运动平滑正则项
- $\mathcal{L}_{foot}$：脚部接触损失，约束足部滑动

轨迹预测模块独立优化均方误差：

$$\mathcal{L}_{traj} = \mathrm{mse}(\mathbf{P}^A, \hat{\mathbf{P}}^A) + \mathrm{mse}(\mathbf{P}^B, \hat{\mathbf{P}}^B) \tag{5}$$

其中 $\mathbf{P}^A$、$\mathbf{P}^B$ 分别为两人物的真实地面轨迹（位置与朝向），轨迹预测器以语音、高层活动值和位置信号为输入（Figure 9），自回归输出未来轨迹作为空间引导。

### 3.5 自回归滑动窗口与实时推理

系统采用自回归滑动窗口机制实现长时生成：每步预测一个运动片段，选取部分帧作为下一窗口的历史条件。轨迹混合与死区混合策略保证窗口边界处的运动平滑过渡。推理阶段使用 8 步扩散采样，运动预测模块为 4 层 Transformer（4 注意力头），单片段推理耗时约 4ms，帧率超过 100fps，满足实时交互需求。

## 实验与关键发现

### 数据集与评估基准

本研究在两个核心基准上验证方法有效性：**BEAT** 用于单人协同语音动作生成，**InterACT++** 用于双人语音驱动交互运动生成。InterACT++ 是本文在 Inter-Act 基础上扩展的新数据集，新增 402 个片段（约 1.7 小时，平均片段长度 15 秒），覆盖握手、拥抱等动态双人交互场景（Table 1）。所有方法均使用统一重定向到 Mixamo 骨架（65 个关节）的动作数据进行训练与评估，确保骨架一致性。

![[assets/figures/papers/paper_list_l1671_It_Takes_Two_Real_time_Co_Speech_Two_person_s_Interaction_Generation_via/figures/004_Table_1.jpg]]
*Table 1: Comparison of existing body-centric dataset. Inter-Act [29] is the only dataset that contains two-person motion and audio sequences. We enrich it with InterAct++ by including 402 clips about dynamic and common two-person interactions*

### 单人协同语音动作生成

在 BEAT 数据集上，本方法与 **CaMN**、**Habibie et al.**、**EMAGE**、**AMUSE**、**LDA** 等基线进行全面对比（Table 2）。核心发现：

![[assets/figures/papers/paper_list_l1671_It_Takes_Two_Real_time_Co_Speech_Two_person_s_Interaction_Generation_via/figures/005_Table_2.jpg]]
*Table 2: Comparison on the single person Speech2Motion Task. All the methods are trained on the BEAT dataset unless specified. The top three are feed-forward methods and the bottom two are diffusion methods*

- **运动质量（FPD）**：本方法以 **FPD 12.85** 显著优于最佳基线 EMAGE 的 18.80，降幅达 31.6%，表明生成动作的分布与真实数据最为接近。
- **节拍对齐（Beat Align）**：达到 0.79，与 AMUSE/EMAGE 持平，证明语音节奏与动作的同步性未因加入双人交互能力而受损。
- **推理效率**：推理时间仅 **4ms/片段**，远超实时要求（>100fps），这得益于 8 步扩散模型与 4 层 Transformer（4 个注意力头）的轻量设计。
- **脚部滑动（Foot Sliding）**：仅 0.0032，表明全身运动（含根位移与脚接触）的物理合理性。

### 双人语音驱动交互运动生成

在 InterACT++ 数据集上的双人语音到运动任务（Table 3）中，本方法与 **Audio2Photoreal**、**LDA**、**LDAdual** 等对比：

![[assets/figures/papers/paper_list_l1671_It_Takes_Two_Real_time_Co_Speech_Two_person_s_Interaction_Generation_via/figures/007_Table_3.jpg]]
*Table 3: The benchmark on the InterACT++ dataset for twoperson speech-to-motion task. All the methods are trained on the train split, and the evaluation is conducted on the test split. LDAdual is the dual-person version of LDA [3] that takes two-person audio as one input and generates two-person motion together*

- **运动质量（FPD）**：本方法 **47.74**，远低于 LDA 的 89.42（降幅 46.6%）和 Audio2Photoreal 的 130.63（降幅 63.5%）。
- **交互质量（FDD）**：**117.88**，相比 Audio2Photoreal 的 563.27 降幅达 79.1%，表明双人动作的协调性与互动真实感大幅提升。
- **交互多样性（Interaction Div.）**：12.54，显著高于 LDAdual 的 5.73，证明生成的动作模式更为丰富。

定性对比（Figure 5）进一步揭示：单人方法（如 Audio2Photoreal、EMAGE、AMUSE）无法捕捉交互关系，生成的动作缺乏动态性；基于轨迹的 LDA 虽能产生动态运动，但因缺乏反应式生成机制，互动真实感受到限制。

![[assets/figures/papers/paper_list_l1671_It_Takes_Two_Real_time_Co_Speech_Two_person_s_Interaction_Generation_via/figures/008_Figure_5.jpg]]
*Figure 5: The qualitative comparison among various co-speech methods. We use a consistent SMPL-X representation for the mesh rendering, except for Audio2Photoreal [41] which provides its own mesh template. Single-person co-speech methods, such as Audio2Photoreal, EMAGE [46] and AMUSE [13], fall short in capturing interaction and producing dynamic motion. While the trajectory-based method LDA [3] succeeds in creating dynamic motion, its lack of a reactive generation mechanism hampers realism*

### 交互运动生成

在给定一方真实动作、生成另一方动作的交互运动生成任务中（Table 4），本方法 FPD 为 103.19，脚部滑动仅 0.0074，在运动质量与物理合理性上均表现最优。需注意该任务下其他方法未提供音频条件，直接可比性有限。

### 消融实验

消融实验（Table 5）系统验证了各模块的贡献：

![[assets/figures/papers/paper_list_l1671_It_Takes_Two_Real_time_Co_Speech_Two_person_s_Interaction_Generation_via/figures/009_Table_5.jpg]]
*Table 5: Ablation study of different system module*

- **伙伴动作条件（m_refer）移除**：FPD 与 FDD 显著恶化，证明实时响应伙伴动作对交互真实感至关重要。
- **伙伴语音条件（s_refer）移除**：运动质量与交互多样性下降，说明语音信息为预测伙伴意图提供了关键上下文。
- **轨迹控制信号（p）移除**：运动质量（FPD）与稳定性（Foot Sliding）均明显变差，验证了独立预测的地面轨迹作为空间引导的必要性。
- **完整系统**在所有指标上均优于各消融版本，确认多模态交互条件的协同作用。

### 用户研究

用户偏好研究（Table 6）中，本方法在三个关键维度上均获最高偏好：
- **语音-动作对齐**：75.2%
- **动画质量**：62.4%
- **交互性**：82.5%

交互性维度的高偏好率（82.5%）尤其突出，印证了反应式自回归生成框架在塑造真实互动感知方面的核心优势。

### 失败模式与局限性

尽管整体性能优异，系统仍存在以下局限：
- **近距离身体交互**：缺乏对握手、拥抱等场景的显式物理约束（如接触点建模、穿透避免），可能导致不自然的穿透或接触。
- **数据集覆盖**：InterACT++ 虽已扩展，但仍无法覆盖所有可能的交互场景，尤其手指级精细交互。
- **未来信息依赖**：系统假设已知伙伴的未来语音特征，实际部署中需额外预测模块，这可能引入级联误差。
- **面部表情缺失**：当前仅生成身体运动，未集成面部动画，限制了完整虚拟人对话系统的构建。

### 关键图表指引

- **Table 2**：单人任务量化对比，核心证据为 FPD 12.85 vs. EMAGE 18.80。
- **Table 3**：双人任务量化对比，核心证据为 FPD 47.74 vs. LDA 89.42，FDD 117.88 vs. Audio2Photoreal 563.27。
- **Table 5**：消融实验，验证伙伴条件与轨迹控制的必要性。
- **Table 6**：用户研究，交互性偏好 82.5% 为关键优势。
- **Figure 5**：定性对比，直观展示本方法在交互性与动态性上的优势。

## 定位与知识库关联

### 1. 方法谱系：从单人语音驱动到双人实时交互

本文提出的**反应式自回归扩散模型**位于协同语音动作生成与多人交互运动生成两条技术路线的交汇点。其直接前驱可划分为两个阵营：

**单人协同语音基线**：早期工作如 **CaMN**、**Habibie et al.**、**AMUSE** 以及 **EMAGE** 均聚焦于单人场景，输入单人语音生成上半身或全身动作。这些方法的核心局限在于：① 仅建模单人运动，无法捕捉对话中的互动关系；② 多为离线序列到序列模型，需要完整语音输入，不具备实时反应能力。**LDA**（Ao et al., 2023）虽引入了扩散生成框架并支持全身运动，但其设计本质上仍是单人的。

**双人语音到动作基线**：**Audio2Photoreal**（Ng et al., 2022）是少数直接处理双人语音到动作生成的工作，但其生成的运动缺乏动态交互性，且仅输出上半身姿势。**LDAdual** 作为 LDA 的双人变体，将两人音频合并为单一输入并联合生成两人运动，但由于缺乏分离式条件建模和反应式生成机制，互动真实感不足。

本方法的关键突破在于将**自回归滑动窗口**范式引入扩散生成框架，并设计了**分离式多条件输入**（自身历史动作、预测轨迹、伙伴动作与语音），使得系统能够实时响应伙伴的行为变化。这一设计从根本上改变了生成范式——从“一次性生成完整序列”转向“在线逐段预测并持续适应”。

### 2. 知识库定位：填补的空白与适用边界

**填补的核心空白**：
- **实时双人全身交互生成**：首次实现了从两人语音到全身动态交互运动的在线生成，推理速度达 4ms/片段（>100fps），远超实时要求。
- **反应式生成机制**：通过自回归窗口和分类器自由引导（随机掩码伙伴条件），模型既能利用伙伴信息增强互动质量，又可在伙伴信息缺失时退化为单人生成，实现了灵活的条件依赖。
- **轨迹引导的空间控制**：独立预测的双人地面轨迹作为空间引导信号，显著提升了运动稳定性（Foot Sliding 指标大幅降低）和可控性。

**适用边界**：
- **已知未来伙伴语音的假设**：系统在生成当前帧时需访问伙伴的未来语音特征（用于语义令牌提取），这在实际部署中需要额外的语音预测模块。该假设在离线场景或可容忍微小延迟的应用中成立，但在严格实时对话中是一个待解决的前提条件。
- **身体交互的物理合理性**：模型未嵌入显式物理约束（如接触点检测、穿透避免），对于握手、拥抱等近距离身体交互，可能出现穿透或不自然接触。当前系统更适合中等距离的对话场景。
- **数据集覆盖范围**：InterAct++ 数据集虽丰富了动态交互，但 402 个片段（1.7 小时）仍无法覆盖所有可能的交互类型，尤其缺乏手指级精细交互和极端身体接触场景。

### 3. 局限与开放问题

**已识别的局限**：
1. **物理约束缺失**：扩散模型生成的关节旋转和根位移未经过物理验证，可能导致脚部滑动（虽已通过损失函数缓解）或身体穿透。
2. **面部表情未集成**：当前系统专注于身体运动，未包含面部动画生成，距离完整的虚拟人对话系统仍有差距。
3. **数据集规模与多样性**：InterAct++ 虽较 Inter-Act 有所扩展，但相比单人数据集（如 BEAT）规模仍较小，可能限制模型对长尾交互模式的泛化能力。

**开放问题**：
1. **在线伙伴行为预测**：如何在不依赖未来信息的前提下，在线预测伙伴的反应性语音与动作，从而实现完全自主的双人实时交互？
2. **显式物理约束融合**：如何将接触点约束、穿透惩罚等物理先验融入扩散去噪过程，而不破坏生成多样性和实时性？
3. **多方对话扩展**：当前双流架构能否自然扩展到三人以上的多方对话场景？分离式条件设计在超过两个主体时如何避免组合爆炸？
4. **面部-身体协同生成**：如何将面部动画与身体运动在统一的扩散框架中协同生成，实现语义一致的全模态虚拟人交互？

## 原文 PDF

![[paperPDFs/arxiv_2024/It_Takes_Two_Real_time_Co_Speech_Two_persons_Interaction_Generation_via_Reactive_Auto_regressive_Diffusion_Model.pdf]]
