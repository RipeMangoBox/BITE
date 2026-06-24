---
title: "Vid2World: Crafting Video Diffusion Models to Interactive World Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Vid2World_Crafting_Video_Diffusion_Models_to_Interactive_World_Models.pdf
openreview_forum_id: pFyzqbUiF9
aliases:
- Vid2World
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过两个关键操作实现范式转换：(1) 视频扩散因果化——利用外推权重转移(Extrapolative Weight Transfer)将双向注意力/卷积改造为因果版本，并配合Diffusion Forcing训练目标，使模型能进行严格因果生成；(2) 因果动作引导——在每帧注入动作嵌入，并引入动作屏蔽训练和分类器自由引导，实现帧级动作调控。"
primary_logic: "利用互联网规模无动作视频数据蕴含的丰富物理先验，通过架构因果化和动作引导机制，以极低的域内交互数据成本将庞大的视频扩散模型重铸为高保真、动作响应的通用世界模型，突破了动作标注数据稀缺和预测真实感不足的根本瓶颈。"
claims:
- "在机器人操作、3D游戏和开放导航三个领域，Vid2World在FVD、FID等指标上全面超越已有转换方法和先进世界模型。"
- "外推权重转移 + 动作引导在RT-1上取得最佳FVD (22.4) 和FID (6.16)，消融实验证明两组件的互补增益。"
- "从随机初始化训练相同架构的世界模型，FVD高达1768.8（vs 22.4），实证预训练视觉先验是不可或缺的。"
- "定理4.1证明因果动作引导等价于对后验分布的概率调控，为方法提供了严格的理论基础。"
---

# Vid2World: Crafting Video Diffusion Models to Interactive World Models

> [!tip] 核心洞察
> 利用互联网规模无动作视频数据蕴含的丰富物理先验，通过架构因果化和动作引导机制，以极低的域内交互数据成本将庞大的视频扩散模型重铸为高保真、动作响应的通用世界模型，突破了动作标注数据稀缺和预测真实感不足的根本瓶颈。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Vid2World：将视频扩散模型打造为交互式世界模型 |
| 英文题名 | Vid2World: Crafting Video Diffusion Models to Interactive World Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=pFyzqbUiF9); [Project](https://knightnemo.github.io/vid2world/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Vid2World |
| Dataset | Robot Manipulation (RT-1), 3D Game Simulation (CS:GO), Open-World Navigation (RECON) |

> [!tip] 效果简介
> - Robot Manipulation (RT-1) 上，FVD 为 18.5 (Vid2World autoregressive)，对比 24.2 (Action-Conditioned FT)，变化 -23.6%。
> - 3D Game Simulation (CS:GO) 上，FVD 为 106.6，对比 368.5 (DIAMOND-HQ)，变化 -71.1%。
> - 3D Game Simulation (CS:GO) 上，FID 为 17.5，对比 87.2 (DIAMOND-HQ)，变化 -79.9%。

## 概述

### 问题瓶颈

构建能模拟物理世界、支持动作反事实推理的交互式世界模型，是具身智能与强化学习的核心追求。然而，现有方法面临双重瓶颈：**数据瓶颈**——高质量动作标注数据极度稀缺且采集昂贵，而互联网上存在海量的无动作视频数据却蕴含丰富的物理先验；**架构瓶颈**——预训练视频扩散模型（如DynamiCrafter）虽能生成高保真视频，但其双向注意力与对称卷积核天然允许未来帧信息泄露，且缺乏帧级动作可控性，无法直接用于需要严格因果生成和细粒度动作响应的世界模型。

### 核心思路

Vid2World 提出了一条系统性的范式转换路径：**以极低的域内交互数据成本，将互联网规模预训练的视频扩散模型重铸为高保真、动作响应的通用世界模型**。其核心洞察在于——预训练模型已内化丰富的视觉物理先验，只需通过架构因果化和动作引导机制即可“解锁”其作为世界模型的潜力，而非从零训练。

### 方法定位

Vid2World 的方法谱系可定位于**预训练视频扩散模型的后训练适配（post-training adaptation）**，区别于两类现有路线：

- **从零训练的世界模型**（如 DIAMOND、NWM）：完全依赖域内数据学习，缺乏大规模视觉先验，预测真实感不足。
- **直接微调视频扩散模型**（如 Action-Conditioned Fine-tuning、AVID、ControlNet 适配）：仅添加动作条件或简单因果掩码，未系统解决架构因果化与动作引导的耦合问题。

Vid2World 通过两个关键操作实现突破：

1. **视频扩散因果化**：提出外推权重转移（Extrapolative Weight Transfer），将双向注意力改为因果掩码，将对称卷积核通过局部线性外推重分配为因果核，配合 Diffusion Forcing 训练目标，使模型能进行严格的自回归因果生成。
2. **因果动作引导**：在每帧注入动作嵌入，并引入动作屏蔽训练与分类器自由引导（Causal Action Guidance），实现帧级动作调控。定理 4.1 从贝叶斯后验角度证明该引导等价于对生成分布的概率调控。

### 主要结果

在机器人操作（RT-1）、3D 游戏仿真（CS:GO）和开放世界导航（RECON）三个领域的实验表明：

- **全面超越现有方法**：Vid2World 在 FVD、FID 等指标上显著优于 DIAMOND、NWM 等先进世界模型及各类微调基线。例如，CS:GO 场景下 FVD 降低 71.1%（106.6 vs 368.5），FID 降低 79.9%（17.5 vs 87.2）。
- **组件互补增益**：消融实验证实，外推权重转移在三种权重转移策略中表现最优，且动作引导带来一致的额外提升（RT-1 上 FVD 从 28.6 降至 22.4）。
- **预训练先验不可或缺**：从随机初始化训练相同架构的模型，FVD 高达 1768.8（vs 22.4），实证预训练视觉先验是性能的根基。

### 局限性

推理速度较慢（每帧约 20 秒），训练成本高（100k 步需 7 天 × 4 A100 GPU），长时域 rollout 存在错误累积，且交互性评估指标可能被模型“利用”——这些问题构成了后续优化的关键方向。

## 背景与动机

### 世界模型的根本瓶颈：交互数据稀缺与预测真实感不足

构建能够模拟物理环境、预测未来状态并与智能体交互的世界模型，是具身智能和强化学习的核心目标之一。然而，当前世界模型面临两个根本性瓶颈：

**瓶颈一：细粒度动作标注数据的极度稀缺。** 高质量的世界模型训练需要大量带有帧级动作标签的交互视频数据。这类数据的采集成本极高——在机器人操作中需要真实硬件部署，在3D游戏中需要专业玩家操控，在开放世界导航中需要精确的里程计记录。互联网上海量的无动作视频数据（如YouTube视频）蕴含丰富的物理先验和视觉知识，却因缺乏动作标注而无法被传统世界模型直接利用。这一数据金字塔的倒置——域内交互数据极少，通用视频数据极多——构成了世界模型泛化能力的根本制约。

**瓶颈二：预测真实感与物理一致性的不足。** 现有世界模型多从零开始训练，受限于域内数据的规模和多样性，其生成的未来帧往往存在模糊、细节丢失和物理不合理等问题。例如，在CS:GO游戏环境中，DIAMOND模型的帧在长时rollout中逐渐模糊退化；在机器人操作场景中，从随机初始化训练的世界模型FVD高达1768.8，远无法满足实际应用对视觉保真度的要求（见Table 5）。

### 视频扩散模型的潜力与结构性缺陷

预训练视频扩散模型（如DynamiCrafter）在互联网规模的无动作视频数据上训练，展现出惊人的高保真视频生成能力。这一能力天然契合世界模型对预测真实感的需求。然而，将视频扩散模型直接用于交互式世界模型面临两个结构性障碍：

1. **非因果架构**：视频扩散模型采用双向时间注意力机制和对称时间卷积核，在生成某帧时可以“窥视”未来帧的信息。这种全序列生成范式违背了世界模型逐帧自回归预测的因果约束——智能体在时刻$t$只能基于历史观测$\mathcal{H}_t$预测未来，而非已知完整序列。

2. **缺乏动作条件化**：视频扩散模型通常以文本提示或初始帧为条件，不具备接收和响应帧级动作指令的机制。世界模型需要根据智能体的动作$\mathbf{a}_t$生成相应的下一帧，这要求模型能够理解动作对视觉状态的因果影响，并支持反事实推理（“如果执行另一个动作会怎样”）。

### 现有转换方法的不足

已有工作尝试将视频扩散模型适配为世界模型，但均存在明显局限：

- **动作条件微调**直接对基模型添加动作条件进行训练，但未解决非因果架构问题，模型仍可利用未来信息“作弊”，导致自回归rollout时性能退化。
- **ControlNet**（Zhang et al., 2023）类方法注入动作条件，但同样未处理因果性问题。
- **AVID**（Rigter et al., 2024）冻结基模型仅训练动作感知适配器，虽降低了训练成本，但因果架构缺失的根本问题依旧。
- **DIAMOND**和**NWM**等专用世界模型从零训练，受限于域内数据规模，预测质量远不及预训练视频扩散模型。

### Vid2World的动机与核心思路

Vid2World的核心洞察在于：**互联网规模的无动作视频数据已经编码了丰富的物理先验和视觉知识，关键在于如何通过架构改造和条件注入，将这些“被动”的视频扩散模型重铸为“主动”的因果世界模型，而非从零训练或简单微调。**

这一范式的优势在于：以极低的域内交互数据成本（仅需少量动作标注视频进行微调），撬动海量预训练知识，同时解决预测真实感和动作响应性两大难题。具体而言，Vid2World通过两条技术路径实现这一范式转换（如Figure 2所示）：

- **视频扩散因果化**：将双向时间注意力和对称时间卷积改造为严格的因果版本，使模型仅依赖历史帧进行预测，配合Diffusion Forcing训练目标适应自回归生成。
- **因果动作引导**：在每帧注入动作嵌入，并通过动作屏蔽训练和分类器自由引导机制，实现帧级动作调控，使生成分布向指定动作偏移。

这一设计使得Vid2World在机器人操作（RT-1）、3D游戏仿真（CS:GO）和开放世界导航（RECON）三个领域，均以显著优势超越现有转换方法和先进世界模型，验证了“预训练先验+因果化改造”路线的有效性。

## 核心创新

Vid2World的核心创新在于通过**架构因果化**与**因果动作引导**两大模块，将预训练的非因果视频扩散模型重铸为可自回归生成、帧级动作可控的交互式世界模型。其本质是对模型的时间建模机制和条件化范式进行根本性改造，而非简单的微调适配。

### 1. 视频扩散因果化：从双向到因果的时间建模

预训练视频扩散模型（如DynamiCrafter）的时间注意力层和卷积层天然具有双向性，允许未来帧信息泄露到当前帧的生成中，这使其无法直接用于需要严格逐帧自回归预测的世界模型。Vid2World通过两个关键操作实现因果化：

**（1）外推权重转移（Extrapolative Weight Transfer）**
时间卷积层的对称核会聚合过去和未来帧的信息。Vid2World提出基于局部线性外推的权重重分配策略：将原本作用于未来帧的权重，按照外推系数精确重新分配到过去位置，形成因果核。具体更新规则为：

$$w_{j}^{\prime} = \mathbf{1}_{[j \geq -m]} \cdot w_{j} + \mathbf{1}_{[-p+1 \leq j \leq 0]} \cdot \sum_{i=1}^{m} \gamma_{i,-j} w_{i}, \quad \mathbf{b}^{\prime} = \mathbf{b} + \sum_{i=1}^{m} w_{i} \beta_{i}$$

其中$\gamma_{i,-j}$和$\beta_i$通过局部线性关系$\mathbf{z}_{t+k} \approx \sum_{j=0}^{p-1} \gamma_{k,j} \mathbf{z}_{t-j} + \beta_k$估计得到。该方法在所有权重转移策略中最大程度保留了预训练表示结构（特征余弦相似度最高，达0.7113），为后续微调提供了最优初始化。消融实验证实，外推权重转移在RT-1上取得FVD 28.6（无动作引导），显著优于Shift WT（FVD 29.9）和Masked WT（FVD 33.2）（Table 2）。

对于时间注意力层，因果化更为直接——仅需施加因果掩码，无需参数修改。

**（2）Diffusion Forcing训练目标**
传统扩散模型对所有帧施加统一的噪声水平，而Vid2World采用Diffusion Forcing策略：每帧独立采样均匀噪声级别$k_t \sim U(0, K)$。这迫使模型学习在任意历史帧干净、未来帧带噪的组合下进行去噪，从而在推理时能够稳定地进行因果自回归生成。该设计是连接“视频扩散”与“世界模型”两个范式的关键训练协议转换。

### 2. 因果动作引导：帧级动作注入与概率调控

仅实现因果生成不足以构建交互式世界模型——模型还需响应外部动作输入。Vid2World的动作条件化包含三个协同机制：

**（1）帧级动作嵌入注入**
在预测第$t$帧时，将动作$\mathbf{a}_{t-1}$通过轻量MLP编码后注入到对应时间位置的潜在表示中，实现细粒度动作调控。

**（2）动作屏蔽训练**
训练时以固定概率$p$随机将动作替换为空标记$\varnothing$：

$$\mathcal{L}(\theta) = \mathbb{E}_{[k_{\tau}], \epsilon, [\mathbf{x}_{\tau}^{0}], [\widetilde{\mathbf{a}}_{\tau}]} \left[ \sum_{t=0}^{T} || \epsilon_{t} - \epsilon_{\theta}( [\mathbf{x}_{\tau}^{k_{\tau}}]_{\leq t}, [\widetilde{\mathbf{a}}_{\tau}]_{< t}, [k_{\tau}]_{\leq t} ) ||^{2} \right]$$

其中$\widetilde{\mathbf{a}}_{t} = \varnothing$以概率$p$出现。这迫使模型同时学习条件分数$\epsilon_{\mathrm{cond}}$和无条件分数$\epsilon_{\mathrm{ucond}}$。

**（3）分类器自由动作引导**
推理时通过引导尺度$\lambda$组合两个分数：

$$\epsilon_{\mathrm{guided}} = (1 + \lambda) \cdot \epsilon_{\mathrm{cond}} - \lambda \cdot \epsilon_{\mathrm{ucond}}$$

**定理4.1**为该方法提供了严格的理论基础，证明该组合等价于从如下调控后验分布中采样：

$$\tilde{p}(\mathbf{x}_t \mid \mathbf{a}_{t-1}, \mathcal{H}_t) \propto p(\mathbf{x}_t \mid \mathcal{H}_t) \cdot p(\mathbf{a}_{t-1} \mid \mathbf{x}_t, \mathcal{H}_t)^{\omega}$$

即生成过程由历史一致先验与动作对齐项共同决定。实验表明$\lambda$在中间值（如3.0）达到最优DreamSim，过高则导致过锐化伪影（Figure 8），验证了引导强度的可调性。

### 3. 创新点的协同效应

消融实验揭示了两个创新模块的互补增益（Table 2）：外推权重转移将FVD从1768.8（从头训练）降至28.6，而动作引导进一步降至22.4；FID从6.93降至6.16。**完全从头训练相同架构的世界模型FVD高达1768.8（vs 22.4），实证预训练视觉先验是不可或缺的**（Table 5）。这表明Vid2World的创新本质在于：以极低的域内交互数据成本（RT-1上仅100k梯度步），通过架构因果化和动作引导机制，将互联网规模无动作视频数据中蕴含的丰富物理先验重铸为高保真、动作响应的通用世界模型。

## 整体框架

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_pFyzqbUiF9/figures/004_Figure_4.jpg]]
*Figure 4: Training and sampling of Vid2World, initialized by architecture causalization. (a) During training, we add independently sampled noise levels to each frame, as well as randomly drop out each action with a fixed probability. (b) For autoregressive rollout, we denoise the latest frame while setting history clean. Action guidance is added for the current action. See Appendix B for details*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_pFyzqbUiF9/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of weight transfer mechanisms for temporal convolution layers: (1) Shift: shifts all weights into the past. (2) Masked: retains only past weights. (3) Extrapolative: leverages local linear feature relationships more in principle(example shown with m = 1 , p = 2 )*

Vid2World 的整体 pipeline 围绕一个核心范式转换展开：将互联网规模预训练的全序列、非因果、被动视频扩散模型，改造为自回归、交互式、动作条件驱动的世界模型。这一转换通过两个互补的模块级操作实现——**视频扩散因果化（Video Diffusion Causalization）** 与 **因果动作引导（Causal Action Guidance）**，二者以串行方式衔接，共享统一的 Diffusion Forcing 训练目标。

### 阶段一：视频扩散因果化

该阶段解决预训练模型“允许未来帧信息泄露”的根本性架构缺陷，将双向时序建模改造为严格因果的自回归生成结构。具体包含三个子操作：

1. **时序注意力因果掩码**：对时间注意力层施加因果掩码，使当前帧仅能关注历史帧，无需参数修改即可完成因果化。
2. **时序卷积核外推权重转移**：针对时间卷积层，通过**外推权重转移（Extrapolative Weight Transfer）**将原本作用于未来帧的卷积权重，依据局部线性外推关系重新分配到过去位置，形成因果卷积核。这一操作最大限度地保留了预训练表示结构（特征余弦相似度达 0.7113，为所有策略中最高）。
3. **Diffusion Forcing 训练目标**：每帧独立采样均匀噪声级别 $k_t \sim U(0, K)$，使模型适应任意“历史干净帧 + 未来带噪帧”的组合模式，为后续自回归 rollout 奠定基础。

### 阶段二：因果动作引导

在因果化架构之上，引入帧级动作可控性，使模型能够响应外部动作信号进行条件生成。该阶段同样包含三个子操作：

1. **因果动作注入（Causal Action Injection）**：通过轻量 MLP 将动作 $\mathbf{a}_{t-1}$ 的嵌入注入到时间位置 $t$ 的潜在表示中，实现帧级动作条件化。
2. **动作屏蔽训练**：训练时以固定概率 $p$ 将动作随机替换为空标记 $\varnothing$，迫使模型同时学习条件分数 $\epsilon_{\text{cond}}$ 与无条件分数 $\epsilon_{\text{ucond}}$，为推理时的引导提供基础。
3. **分类器自由动作引导**：推理时通过组合公式 $\epsilon_{\text{guided}} = (1 + \lambda) \cdot \epsilon_{\text{cond}} - \lambda \cdot \epsilon_{\text{ucond}}$ 放大当前动作的影响。定理 4.1 证明该操作等价于从调控后验分布 $\tilde{p}(\mathbf{x}_t \mid \mathbf{a}_{t-1}, \mathcal{H}_t) \propto p(\mathbf{x}_t \mid \mathcal{H}_t) \cdot p(\mathbf{a}_{t-1} \mid \mathbf{x}_t, \mathcal{H}_t)^{\omega}$ 中采样，其中历史一致先验与动作对齐项共同决定生成过程。

### 输入输出流

- **输入**：历史观测帧序列 $\mathbf{o}_{<t}$（可为带噪或干净状态）与对应动作序列 $\mathbf{a}_{<t}$。
- **处理**：因果化架构逐帧处理，每帧仅访问历史信息；动作嵌入在对应时间步注入潜在空间；Diffusion Forcing 噪声调度使模型能处理任意干净/带噪帧组合。
- **输出**：下一帧预测 $\hat{\mathbf{o}}_t$，在自回归 rollout 中该预测被反馈为下一时间步的历史输入。

### 训练与推理流程

如图 4 所示，训练时模型接收完整视频序列，每帧被独立赋予不同噪声级别，动作以概率 $p$ 随机屏蔽；推理时采用自回归 rollout，每步预测的干净帧被拼接回历史，与当前动作一起驱动下一帧生成。因果动作引导的强度由超参数 $\lambda$ 控制，在动作对齐与保真度之间进行权衡——实验表明 $\lambda$ 在中间值（如 3.0）达到最优 DreamSim，过高则导致过锐化伪影。

### 关键设计决策

- **预训练先验保留**：完全从随机初始化训练相同架构的世界模型，FVD 高达 1768.8（vs Vid2World 的 22.4），实证互联网视频预训练的视觉先验是不可或缺的核心要素。
- **外推权重转移 vs 其他策略**：相比简单的 Shift WT（直接平移权重）和 Masked WT（直接丢弃未来权重），外推方法通过线性外推系数 $\gamma_{i,-j}$ 将未来权重信息精确重分配到过去位置，在所有权重转移策略中取得最佳 FVD/FID，且动作引导一致带来额外增益（如 Extrapolative WT: FVD 28.6 → 22.4）。

## 核心模块与公式推导

Vid2World 将预训练视频扩散模型转化为交互式世界模型，依赖四个关键模块协同工作。以下逐一阐述其设计原理与核心公式。

### 模块一：视频扩散因果化 (Video Diffusion Causalization)

预训练视频扩散模型（如 DynamiCrafter）的时间注意力层和时间卷积层天然是非因果的——它们允许未来帧的信息泄露到当前帧的预测中。因果化改造分两步进行：

**时间注意力因果化**：直接施加因果掩码，使时间位置 $t$ 只能关注 $\leq t$ 的帧。此操作不涉及参数修改，属于纯架构层面的约束。

**时间卷积因果化——外推权重转移 (Extrapolative Weight Transfer)**：这是因果化的核心难点。原始卷积核包含作用于未来帧的权重 $\{w_i\}_{i>0}$，简单丢弃会损失预训练表示。外推权重转移基于局部线性外推假设：未来帧特征可由过去 $p$ 帧线性近似：

$$\mathbf{z}_{t+k} \approx \sum_{j=0}^{p-1} \gamma_{k,j} \mathbf{z}_{t-j} + \beta_k$$

其中 $\gamma_{k,j}$ 和 $\beta_k$ 通过最小二乘拟合从预训练特征中估计。据此，因果卷积核的权重 $w'_j$ 和偏置 $\mathbf{b}'$ 更新为：

$$w_{j}^{\prime} = \mathbf{1}_{[j \geq -m]} \cdot w_{j} + \mathbf{1}_{[-p+1 \leq j \leq 0]} \cdot \sum_{i=1}^{m} \gamma_{i,-j} w_{i}, \quad \mathbf{b}^{\prime} = \mathbf{b} + \sum_{i=1}^{m} w_{i} \beta_{i}$$

该公式将原始作用于未来 $i$ 帧的权重 $w_i$，按外推系数 $\gamma_{i,-j}$ 精确重分配到过去位置 $j$，同时修正偏置以补偿外推偏移。消融实验证实，外推权重转移在所有权重转移策略中保留预训练表示的程度最高（特征余弦相似度 0.7113），且最终性能最优（Table 2）。

**训练目标——Diffusion Forcing**：因果架构需要配套的训练范式。传统扩散模型对所有帧施加相同噪声水平，而 Diffusion Forcing 为每帧独立采样噪声级别 $k_t \sim U(0, K)$。这使得模型必须学会在任意“历史干净、未来带噪”的组合下进行去噪，从而在推理时支持严格的自回归生成。

### 模块二：因果动作注入 (Causal Action Injection)

为实现帧级动作可控性，Vid2World 在每帧的潜在表示中注入动作嵌入。具体而言，当预测第 $t$ 帧观测 $o_t$ 时，将前一时刻动作 $\mathbf{a}_{t-1}$ 通过轻量 MLP 编码后，直接加到时间位置 $t$ 的潜在特征上。这种设计保证了因果性：当前帧的生成仅依赖历史动作序列，不访问未来动作信息。

### 模块三：因果动作引导 (Causal Action Guidance)

单纯的动作注入可能不足以让模型充分响应动作信号。为此引入分类器自由引导机制：

**训练阶段**：以概率 $p$ 随机将动作 $\mathbf{a}_t$ 替换为空标记 $\varnothing$，迫使模型同时学习条件分布和无条件分布。训练损失为：

$$\mathcal{L}(\theta) = \mathbb{E}_{[k_{\tau}], \epsilon, [\mathbf{x}_{\tau}^{0}], [\widetilde{\mathbf{a}}_{\tau}]} \left[ \sum_{t=0}^{T} || \epsilon_{t} - \epsilon_{\theta}( [\mathbf{x}_{\tau}^{k_{\tau}}]_{\leq t}, [\widetilde{\mathbf{a}}_{\tau}]_{< t}, [k_{\tau}]_{\leq t} ) ||^{2} \right]$$

其中 $\widetilde{\mathbf{a}}_{t}$ 以概率 $p$ 取 $\varnothing$，否则取真实动作 $\mathbf{a}_{t}$。

**推理阶段**：通过超参数 $\lambda$ 组合条件与无条件噪声预测：

$$\epsilon_{\mathrm{guided}} = (1 + \lambda) \cdot \epsilon_{\mathrm{cond}} - \lambda \cdot \epsilon_{\mathrm{ucond}}$$

该操作有严格的理论基础。定理 4.1 证明，上述引导等价于从如下调控后验分布中采样：

$$\tilde { p } ( \mathbf { x } _ { t } \mid \mathbf { a } _ { t - 1 } , \mathcal { H } _ { t } ) \propto p ( \mathbf { x } _ { t } \mid \mathcal { H } _ { t } ) \cdot p ( \mathbf { a } _ { t - 1 } \mid \mathbf { x } _ { t } , \mathcal { H } _ { t } ) ^ { \omega }$$

其中 $\mathcal{H}_t$ 为历史上下文，$\omega$ 与 $\lambda$ 存在确定映射关系。该式揭示：生成过程由“历史一致性先验” $p(\mathbf{x}_t \mid \mathcal{H}_t)$ 与“动作对齐项” $p(\mathbf{a}_{t-1} \mid \mathbf{x}_t, \mathcal{H}_t)^\omega$ 共同决定，引导项本质上充当隐式分类器，将生成推向与当前动作对齐的区域。

实验表明，$\lambda$ 在中间值（如 3.0）达到最优 DreamSim 指标，过高则引发过锐化伪影（Figure 8），验证了引导强度的可调性。

### 模块间协同关系

四个模块形成清晰的因果链：架构因果化（模块一）消除未来信息泄露，为自回归生成奠定基础；Diffusion Forcing 训练目标使模型适应因果生成范式；动作注入（模块二）建立动作到观测的映射通道；动作引导（模块三）进一步强化该映射的响应灵敏度。消融实验（Table 2）证实，外推权重转移与动作引导的组合取得最佳 FVD (22.4) 和 FID (6.16)，且两者贡献互补——移除任一组件均导致性能显著下降。

## 实验与分析

### 核心实验设置

Vid2World 在三个截然不同的领域验证其作为交互式世界模型的能力：**机器人操作**（RT-1，基于 CLIPort 的 7 自由度真实机器人数据）、**3D 游戏仿真**（CS:GO，基于 DIAMOND 的 Atari-Head 风格环境）和**开放世界导航**（RECON，基于 Ego4D 的 1B 参数导航世界模型 NWM 数据集）。所有对比方法均基于相同的基模型 **DynamiCrafter 1.1B** 和统一的训练协议（RT-1 上 100k 梯度步，4×A100 GPU），视频生成指标（FVD、FID、SSIM、LPIPS、PSN、DreamSim）遵循标准实现和数据集划分，确保可比性。对于无法自回归生成的基线，额外报告非自回归或单步预测结果以进行公平对比。完整超参数见 Table 3。

### 主结果：跨领域全面领先

Table 1 汇总了 Vid2World 在三个领域与世界模型基线的对比。核心结论如下：

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_pFyzqbUiF9/figures/005_Table_1.jpg]]
*Table 1: World modeling performance across various domains. Best performances are in bold, second best are underlined. Dash (-) indicates the metric was not originally evaluated for that dataset. ∗Autoregressive prediction. †Non-autoregressive prediction. ‡One-step prediction*

**机器人操作（RT-1）**：在自回归预测设定下，Vid2World 取得 FVD 18.5，显著优于 Action-Conditioned Fine-tuning 的 24.2（相对提升 23.6%），在 FID、SSIM、LPIPS 等指标上同样全面领先。非自回归设定下，Vid2World 亦以 FVD 22.4 超越 ControlNet（Zhang et al., 2023）和 AVID（Rigter et al., 2024）等专用适配方案。

**3D 游戏仿真（CS:GO）**：这是验证方法通用性的关键战场。Vid2World 在自回归设定下取得 FVD 106.6、FID 17.5，相较最强基线 DIAMOND-HQ 的 FVD 368.5 和 FID 87.2，分别实现 **71.1%** 和 **79.9%** 的惊人降幅。这意味着 Vid2World 生成的游戏画面在时序一致性和视觉保真度上远超现有扩散世界模型。

**开放世界导航（RECON）**：在自回归多步预测中，Vid2World 的 SSIM 达 0.481，优于 NWM 1B 的 0.389（提升 23.7%），DreamSim 亦更优（0.175 vs 0.203）。在单步预测中，Vid2World 在 6 项指标中的 4 项超越 NWM（+Ego4D）。值得注意的是，NWM 专门针对导航任务设计且使用了 Ego4D 域内预训练，而 Vid2World 仅凭通用视频扩散先验的迁移即达此水平，凸显了预训练视觉先验的跨域迁移效率。

### 消融实验：两大组件的互补增益

Table 2 在 RT-1 上系统解耦了**权重转移策略**与**动作引导**的贡献，揭示了三层递进结论：

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_pFyzqbUiF9/figures/010_Table_2.jpg]]
*Table 2: Ablation study on two components of our proposed method: the choice of Weight Transfer (WT) mechanisms and the use of Action Guidance (AG)*

**权重转移策略的阶梯效应**：Shift WT 仅简单平移权重，FVD 29.9；Masked WT 保留过去权重，FVD 降至 28.4；Extrapolative WT 通过局部线性外推将未来权重精确重分配到过去位置，FVD 进一步降至 28.6。三者均显著优于无因果化的基线，但外推方法在保留预训练表示结构方面最优——Table 6 显示其与原始模型的特征余弦相似度最高（0.7113），验证了“最大限度保留预训练表示”的设计初衷。

**动作引导的普适增益**：在三种权重转移策略上叠加 Causal Action Guidance 后，FVD 分别从 29.9→24.6、28.4→23.0、28.6→**22.4**，FID 从 7.82→6.68、7.50→6.37、7.34→**6.16**。动作引导的增益在 Extrapolative WT 上最为显著（FVD 降低 21.7%），说明更好的因果化基础能更有效地响应动作调控。

**预训练先验的不可替代性**：Table 5 的对比极具说服力——从随机初始化训练相同架构的世界模型，FVD 高达 **1768.8**，而 Vid2World（Extrapolative WT + AG）仅为 22.4，差距近 80 倍。这实证了互联网规模无动作视频数据蕴含的丰富物理先验是 Vid2World 成功的核心要素，仅靠域内交互数据（RT-1 仅约 100k 帧）无法习得可用的世界模型。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_pFyzqbUiF9/figures/036_Table_5.jpg]]
*Table 5: Ablation study on the role of video pretraining: To validate Vid2World truly transfers priors from the pretrained video diffusion model, we train an additional model from scratch in the RT-1 environment, maintaining the exact architecture as Vid2World but randomly initializing the parameters. Best results in bold, worst in italics*

### 因果动作引导的尺度敏感性

Figure 8 在 CS:GO 上揭示了引导强度 λ 的 U 形效应：DreamSim 从 λ=1.0 时的约 0.143 降至 λ=3.0 时的最优值约 0.134，随后在 λ=4.0 时反弹至约 0.137。低 λ 时动作对齐不足，高 λ 时过锐化伪影损害保真度，中等 λ 取得最佳平衡。这与 Theorem 4.1 的理论预测一致——引导项 $p(\mathbf{a}_{t-1} \mid \mathbf{x}_t, \mathcal{H}_t)^\omega$ 的指数放大必须在动作对齐与分布保真之间权衡。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_pFyzqbUiF9/figures/015_Figure_8.jpg]]
*Figure 8: Video Prediction Metrics as a function of Causal Action Guidance Scale (λ) in the CS:GO environment. While increasing λ initially improves performance by enforcing action alignment, excessive guidance leads to degradation due to over-sharpening artifacts*

### 交互性评估与失败模式

Table 4 报告了 CS:GO 上的归一化 delta 交互指标（$\Delta_N$-$\mathcal{M}$），该指标衡量模型对动作变化的敏感度：Vid2World 在 FVD（-77.06）和 FID（-6.83）上表现最强，但 DIAMOND-HQ 在 SSIM（47.04）和 DreamSim（-53.35）上占优。作者坦承该指标存在被“利用”的风险——模型可能通过降低 OOD 动作下的生成质量来虚增分数，评估体系有待完善。

Figure 14 的定性对比展示了 Vid2World 的动作响应能力：从同一初始帧出发，Forward、Left、Backward、Right 等 8 种不同动作序列在 14 帧内产生显著分化的轨迹，验证了帧级动作调控的有效性。但在长程 rollout（>100 帧）中仍存在错误累积，可能偏离物理一致性；对于稀有动作或细粒度操控（如 RT-1 中的特定抓取），模型可能退化为常见模式，存在模式坍塌现象。

### 实际应用验证：Real2Sim 策略评估

Figure 5 展示了 Vid2World 在真实机器人策略评估中的应用价值：遵循 SIMPLER（Li et al., 2025）的范式，Vid2World 作为世界模型对不同策略的模拟评估结果，与真实世界执行的成功率趋势高度一致。这意味着 Vid2World 可作为策略筛选的廉价代理，大幅降低真实机器人实验成本。

### 推理效率与资源开销

当前 Vid2World 的推理速度为每帧约 20 秒（50 步 DDIM），训练需 7 天 × 4 A100 GPUs，尚无法满足实时交互需求。作者指出减少采样步数、KV 缓存、模型蒸馏等加速方向，但尚未实现。这构成了从研究原型到实际部署的关键工程瓶颈。

## 方法谱系与知识库定位

### 1. 基线谱系与差异化定位

Vid2World 的核心贡献在于将预训练视频扩散模型系统性地转换为交互式世界模型，这一范式与现有基线方法在路径上存在根本差异。我们将相关基线分为三类，逐层对比其与 Vid2World 的边界。

#### 1.1 直接动作条件化微调方法

最直接的基线是将动作条件直接注入预训练视频扩散模型进行微调，具体包括：

- **Action-Conditioned Fine-tuning**：在基模型（DynamiCrafter 1.1B）上添加帧级动作嵌入进行端到端微调。该方法保留了原始模型的双向注意力架构，导致未来帧信息可泄露至当前帧预测，无法支持严格的自回归因果生成。在 RT-1 机器人操作场景中，其自回归 FVD 为 24.2，显著弱于 Vid2World 的 18.5（Table 1）。

- **Language-Conditioned Fine-tuning**：以语言指令替代动作信号作为条件。该方法在需要细粒度空间操控的任务（如 RT-1 的精确抓取）中存在信息瓶颈——语言描述无法编码连续控制量的精确数值。

- **ControlNet**（Zhang et al., 2023）：通过冻结基模型、仅训练并行的条件注入分支来引入控制信号。ControlNet 的设计初衷是处理空间条件（如边缘图、深度图），其条件注入机制未针对时序因果性进行适配，无法解决未来帧信息泄露问题。

- **Classifier Guidance**：利用额外训练的分类器在扩散采样过程中引导生成偏向指定动作。该方法需额外训练分类器，且引导强度与生成质量之间存在难以调和的权衡，缺乏 Vid2World 中 Causal Action Guidance 的概率论基础（Theorem 4.1）。

- **AVID**（Rigter et al., 2024）：冻结基模型，仅训练轻量动作感知适配器。AVID 的适配器设计避免了全模型微调的高成本，但其基模型仍保持非因果架构，无法实现真正的自回归预测。

Vid2World 与上述方法的本质区别在于：**它同时解决了架构因果化与动作引导两个问题**。消融实验（Table 2）表明，仅添加动作引导而不进行因果化（即 Shift WT + AG），FVD 为 29.9；而 Vid2World 的 Extrapolative WT + AG 组合将 FVD 降至 22.4，降幅达 25.1%。这证明了两组件的互补增益。

#### 1.2 专用世界模型

在特定应用领域，存在从零训练或基于域内数据微调的专用世界模型：

- **DIAMOND (Fast/HQ)**：基于扩散模型的游戏世界模型，专为 3D 游戏环境（如 CS:GO）设计。DIAMOND 完全依赖域内游戏数据进行训练，缺乏互联网规模视频数据的视觉先验。在 CS:GO 场景中，Vid2World 的 FVD 为 106.6，较 DIAMOND-HQ 的 368.5 降低 71.1%；FID 为 17.5，较 DIAMOND-HQ 的 87.2 降低 79.9%（Table 1）。这一悬殊差距直接验证了 Vid2World 的核心洞察：**互联网规模无动作视频数据蕴含的物理先验远优于有限域内数据**。

- **NWM (Navigation World Model)**：导航世界模型，同样利用预训练视频模型（Ego4D），但在架构设计上与 Vid2World 存在差异。在开放世界导航（RECON）的自回归预测中，Vid2World 的 SSIM 为 0.481，优于 NWM 1B 的 0.389（提升 23.7%）；但在单步预测中，NWM 在部分指标上仍占优。这说明 Vid2World 在长程自回归一致性上具有优势，但在高度复杂的开放场景中，域内专用模型的精细调优仍有其价值。

#### 1.3 从零训练的世界模型

Table 5 的消融实验提供了最具说服力的对比：使用与 Vid2World 完全相同的因果化架构，但从随机初始化开始训练，FVD 飙升至 1768.8（vs Vid2World 的 22.4），性能完全崩溃。这一结果实证了**预训练视觉先验是 Vid2World 成功的不可替代要素**，而非架构因果化或动作引导的单一贡献。

### 2. 方法适用边界

Vid2World 的设计在以下条件下表现最优：

- **基模型条件**：需要具备强时序建模能力的视频扩散模型作为初始化。论文使用 DynamiCrafter 1.1B 作为基座，其 U-Net 架构包含时序注意力层和时序卷积层，是权重转移机制的直接作用对象。对于纯空间扩散模型或基于 DiT（Diffusion Transformer）架构的模型，权重转移策略需重新设计。

- **动作空间特性**：Causal Action Injection 通过轻量 MLP 将动作嵌入注入潜在表示，适用于低维连续或离散动作空间（如 RT-1 的 7-DoF 末端执行器动作、CS:GO 的键盘/鼠标离散动作）。对于高维组合动作空间（如多指灵巧手关节角度），MLP 嵌入的表达能力可能不足。

- **数据需求**：尽管 Vid2World 大幅降低了域内交互数据需求，但仍需一定量的动作标注数据进行微调（RT-1 上 100k 梯度步）。在动作标注极度稀缺（如仅数十条轨迹）的场景下，微调可能不充分。

- **预测时域**：论文明确指出 long-horizon rollout（>100 帧）存在错误累积问题。虽然因果化架构避免了训练时的未来信息泄露，但自回归推理的误差传播是扩散模型固有的挑战，Vid2World 并未完全解决。

### 3. 局限性与已知失败模式

#### 3.1 推理效率瓶颈

当前 Vid2World 的推理速度约为每帧 20 秒（50 步 DDIM 采样），无法满足实时交互需求。论文在局限部分承认了这一问题，并指出多种加速潜力（减少采样步数、KV 缓存、模型蒸馏）尚未实现。这一瓶颈限制了 Vid2World 在实时策略评估和人在回路交互中的应用。

#### 3.2 训练资源需求

完整训练流程需 100k 梯度步 × 4 张 A100-40GB GPU，耗时约 7 天。对于资源有限的学术团队，这一成本门槛较高。论文提出的开放问题包括“能否以更少梯度步微调达到同等性能”，但尚未给出答案。

#### 3.3 稀有动作的模式坍塌

在 RT-1 等操作任务中，Vid2World 对于稀有动作（如特定角度的抓取、非典型轨迹）可能退化为常见模式。论文在失败案例分析中确认了这一现象，其根源在于：(1) 预训练数据中缺乏对应的视觉模式；(2) Causal Action Guidance 的引导强度 λ 在稀有动作上可能不足。Figure 8 显示 λ 存在最优值（CS:GO 中 λ=3.0 时 DreamSim 最优），过高则产生过锐化伪影，但该最优值是否适用于所有动作类型尚不明确。

#### 3.4 评估指标的潜在脆弱性

论文特别指出，交互能力评估中使用的归一化 delta 指标可能被模型“利用”——通过故意降低 OOD（分布外）动作下的生成质量来虚增归一化分数。这一评估体系缺陷意味着当前报告的交互性能可能被高估，需要更鲁棒的评估指标设计。

#### 3.5 复杂场景的预测保真度

在开放世界导航（RECON）中，Vid2World 的部分指标仍不及 NWM 等域内专用模型。这提示了一个根本性张力：互联网视频先验虽丰富，但可能包含与目标域分布偏移的视觉模式（如不同相机参数、光照条件、场景布局），在高度复杂场景中这种偏移可能主导预测误差。

### 4. 开放问题与后续方向

论文明确提出的开放问题及我们基于分析识别的潜在方向包括：

**加速推理**：如何通过减少采样步数（如蒸馏为少步模型）、KV 缓存复用（利用自回归生成中历史帧的中间表示）、或模型量化等手段，将推理速度从 20 秒/帧降至亚秒级，是实现实时交互的关键。

**权重转移的扩展性**：当前外推权重转移基于一阶线性外推（p=2），能否扩展至高阶外推（p>2）或非线性外推（如基于学习的偏移预测），以进一步降低因果化过程中的表示失真？Table 6 显示外推方法保持与原始模型的特征余弦相似度为 0.7113，仍有提升空间。

**更大基座模型的潜力**：Vid2World 目前基于 DynamiCrafter 1.1B，若能结合更大规模的视频扩散模型（如 Sora 类），能否释放更强的物理世界理解和泛化能力？这直接关系到 Vid2World 范式的可扩展性上限。

**更鲁棒的交互性评估**：如何设计不易被“黑客攻击”的交互性指标？可能的路径包括基于策略排序一致性的非参数检验、或引入对抗性动作采样来探测模型的真实响应边界。

**因果动作引导的理论推广**：Theorem 4.1 将 Causal Action Guidance 解释为后验概率调控，这一贝叶斯框架能否推广到更复杂的干预（do-calculus）和反事实推理场景？这将是 Vid2World 从“动作响应”迈向“因果推理”的理论基石。

**少步微调的可行性**：在从零训练完全不可行（FVD 1768.8）的前提下，能否以远少于 100k 步的梯度更新达到同等性能？这涉及预训练表示的可迁移性边界问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/Vid2World_Crafting_Video_Diffusion_Models_to_Interactive_World_Models.pdf]]
