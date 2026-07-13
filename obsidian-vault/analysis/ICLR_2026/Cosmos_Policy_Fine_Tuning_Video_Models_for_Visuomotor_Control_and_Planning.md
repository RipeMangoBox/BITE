---
title: "Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Cosmos_Policy_Fine_Tuning_Video_Models_for_Visuomotor_Control_and_Planning.pdf
project_link: https://research.nvidia.com/labs/dir/cosmos-policy/
code_link: null
openreview_forum_id: wPEIStHxYH
aliases:
- CP
- CPFTVMVCP
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将机器人动作、未来状态和价值统一编码为潜在帧，注入预训练视频扩散模型的潜在序列中，通过统一的去噪学习目标联合训练策略、世界模型和价值函数，无需架构改动。"
primary_logic: "预训练视频扩散模型的去噪得分匹配机制天然适合捕捉复杂高维动作分布；通过潜在帧注入实现多模态统一建模，使同一模型同时作为策略、世界模型和价值函数，并支持基于模型的规划来进一步提升任务成功率。"
claims:
- "Cosmos Policy 在 LIBERO 和 RoboCasa 模拟基准上分别取得 98.5% 和 67.1% 的平均成功率，达到最先进水平，且 RoboCasa 仅使用 50 条演示，远超其他方法所需的数据量。"
- "在真实世界 ALOHA 双臂操作任务中，Cosmos Policy 的平均任务完成得分为 93.6%，优于所有对比方法（含 π0.5 的 88.6%）。"
- "移除辅助损失（仅训练策略预测动作、世界模型预测下一状态）导致 LIBERO 平均成功率从 98.5% 降至 97.0%（-1.5 点），而从随机初始化训练下降至 94.6%（-3.9 点），证实联合预测与预训练至关重要。"
- "在两项挑战性任务上，基于模型的规划（V(s') 方案）相比基础无规划策略平均提高 12.5 分。"
---

# Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning

> [!tip] 核心洞察
> 预训练视频扩散模型的去噪得分匹配机制天然适合捕捉复杂高维动作分布；通过潜在帧注入实现多模态统一建模，使同一模型同时作为策略、世界模型和价值函数，并支持基于模型的规划来进一步提升任务成功率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Cosmos Policy：微调视频模型用于视动控制与规划 |
| 英文题名 | Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=wPEIStHxYH) · [Project](https://research.nvidia.com/labs/dir/cosmos-policy/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Cosmos Policy |
| Dataset | LIBERO (4 suites), RoboCasa (24 tasks), Real-world ALOHA (4 tasks), Real-world ALOHA (planning subset: put candies in bowl, put candy in ziploc bag) |

> [!tip] 效果简介
> - LIBERO (4 suites) 上，平均成功率 (%) 为 98.5，对比 97.4 (CogVLA)，变化 +1.1。
> - RoboCasa (24 tasks) 上，平均成功率 (%) 为 67.1，对比 66.4 (FLARE / GR00T-N1.5+HAMLET)，变化 +0.7。
> - Real-world ALOHA (4 tasks) 上，平均任务完成得分 (0-100) 为 93.6，对比 88.6 (π0.5)，变化 +5.0。

## 概要

### 问题瓶颈

现有视频生成模型具备强大的时空先验，但将其转化为机器人策略通常需要多阶段训练与额外的架构组件（如独立的动作生成头或逆动力学模型），无法直接复用预训练视频模型的核心能力。这一瓶颈导致训练流程复杂、数据效率低下，且难以充分利用视频扩散模型在捕捉高维复杂动作分布上的天然优势。

### 核心方法

Cosmos Policy 提出一种**零架构改动的单阶段后训练范式**：将机器人动作、未来状态与价值函数统一编码为**潜在帧**，直接注入预训练视频扩散模型的潜在序列中，通过统一的去噪学习目标联合训练策略、世界模型和价值函数。该方法无需引入任何额外模块，使同一视频扩散模型同时承担策略、世界模型和价值函数三重角色，并支持基于模型的规划以进一步提升任务成功率。

### 方法定位

Cosmos Policy 在方法谱系中处于**统一视频-动作建模**与**扩散策略**的交汇点。与现有工作形成鲜明对比：

- **扩散策略类**（如 Diffusion Policy, Chi et al., 2023；Dita, Hou et al., 2025）：需从头训练独立的动作扩散头，无法利用预训练视频先验。
- **VLA 模型类**（如 π0, Black et al., 2024；π0.5, Intelligence et al., 2025；OpenVLA-OFT, Kim et al., 2025）：依赖额外的视觉-语言对齐与动作解码模块，架构复杂。
- **统一视频-动作模型类**（如 UVA, Li et al., 2025a；UWM, Zhu et al., 2025）：虽尝试联合建模，但仍需定制化架构或分阶段训练。

Cosmos Policy 的核心差异在于：**以潜在帧注入实现多模态统一建模，在预训练视频模型上以单阶段微调同时获得策略、世界模型和价值函数，无需任何架构修改**。

### 主要结果

- **LIBERO 模拟基准**：平均成功率 **98.5%**，超越所有对比方法（次优 CogVLA 为 97.4%），在四个子套件（Spatial、Object、Goal、Long）上均取得领先。
- **RoboCasa 模拟基准**（24 项厨房操作任务）：平均成功率 **67.1%**，达到最先进水平，且仅使用 **50 条演示**，远少于其他方法所需的 300+ 条。
- **真实世界 ALOHA 双臂操作**（四项任务）：平均任务完成得分 **93.6%**，优于所有对比方法（含 π0.5 的 88.6%），在四项任务中的三项取得最高分。
- **基于模型的规划增益**：在两项挑战性任务上，基于模型的 V(s') 规划方案相比基础无规划策略平均提高 **12.5 分**。

### 关键消融发现

联合训练辅助目标（同时预测动作、未来状态与价值）与预训练视频模型初始化是性能的核心支柱：
- 移除辅助损失使 LIBERO 平均成功率从 98.5% 降至 97.0%（-1.5 点）；
- 从随机初始化训练则进一步降至 94.6%（-3.9 点），证实预训练视频先验的关键作用。

机器人操作策略学习长期面临一个核心矛盾：**如何有效利用大规模预训练模型中的先验知识，同时保持策略架构的简洁性与通用性**。近年来，视频生成模型在捕捉复杂物理世界动态和时空先验方面展现出强大能力，但将其转化为机器人策略的过程仍然繁琐且割裂。

### 现有方法的瓶颈

当前将视频模型用于机器人策略的主流范式存在一个显著瓶颈：**多阶段训练与额外架构组件的依赖**。典型流程通常分为两步——首先在视频数据上微调预训练模型以适配机器人观测，然后训练独立的动作生成模块（如扩散策略的 U-Net/Transformer 动作头，或用于从生成视频帧反推动作的逆动力学模型）。这种设计带来了三个根本性问题：

1. **架构碎片化**：策略、世界模型和价值函数通常作为独立模块分别训练，彼此不共享骨干网络，导致整体系统复杂且难以协同优化。
2. **先验利用不充分**：额外的动作模块从头训练，无法直接继承预训练视频模型在去噪得分匹配过程中学到的复杂高维分布建模能力。
3. **多模态适配成本高**：处理多相机视图、机器人本体感受等异构输入时，往往需要定制化的编码器或特征融合模块，缺乏统一的表示框架。

### 本文动机

针对上述问题，Cosmos Policy 提出一个根本性的简化思路：**将机器人动作、未来状态和价值统一编码为潜在帧，直接注入预训练视频扩散模型的潜在序列中，通过单一的去噪学习目标实现策略、世界模型和价值函数的联合训练，无需任何架构改动**。

这一设计基于一个核心洞察：预训练视频扩散模型的去噪得分匹配机制天然适合捕捉复杂高维动作分布——这正是机器人操作中多模态动作建模所需要的。通过潜在帧注入实现多模态统一建模，同一模型可以同时充当策略（生成动作）、世界模型（预测未来状态）和价值函数（评估状态价值），并支持基于模型的规划来进一步提升任务成功率。

## 核心方法与创新机理

Cosmos Policy 的核心创新在于**零架构改动的统一视频扩散建模范式**：将机器人策略、世界模型和价值函数全部融入预训练视频扩散模型的潜在帧序列中，通过单阶段后训练实现多模态联合学习。相比现有方法，这一范式在三个关键维度上实现了突破。

### 从多阶段训练到单阶段后训练

现有视频模型策略通常采用多阶段训练流程：先微调视频生成模型，再训练独立的动作生成模块（如动作扩散头或逆动力学模型）。例如 **Video Policy**（Liang et al., 2025）需要额外的动作预测架构，**UVA**（Li et al., 2025a）和 **UWM**（Zhu et al., 2025）依赖独立的逆动力学模型从生成帧反推动作。这种分离设计使预训练视频模型的核心能力——时空建模与去噪得分匹配——无法直接作用于动作分布学习。

Cosmos Policy 将整个流程压缩为**单阶段后训练**：在机器人演示数据上直接微调预训练视频模型（Cosmos-Predict2-2B-Video2World），无需任何额外模块。消融实验证实了这一设计的必要性：从随机初始化训练（无预训练视频先验）使 LIBERO 平均成功率从 98.5% 降至 94.6%（-3.9 点），证明预训练视频模型的时空先验是性能的关键瓶颈（Table 4）。

### 从独立动作头到潜在帧注入

传统扩散策略（如 **Diffusion Policy**（Chi et al., 2023）、**Dita**（Hou et al., 2025））和 VLA 模型（如 **π0.5**（Intelligence et al., 2025）、**OpenVLA-OFT**（Kim et al., 2025））依赖独立的动作预测头来生成动作。这些方法无法直接利用视频扩散模型的去噪网络来捕捉复杂高维动作分布。

Cosmos Policy 提出**潜在帧注入（Latent Frame Injection）** 机制（Figure 2, Figure 8）：将机器人本体感受、动作块、状态价值等非图像模态编码为潜在帧，直接插入视频扩散序列中。具体实现为：在输入图像序列中插入空白图像，经 VAE 编码后在对应潜在帧位置覆盖编码后的模态向量。对于多相机视图，则在图像序列层面直接插入额外相机图像。这一设计使去噪网络在统一目标下同时预测动作、未来状态和价值，无需任何架构改动。

### 从独立模块到统一联合建模

现有方法将世界模型和价值函数作为独立模块训练，与策略不共享骨干网络。Cosmos Policy 通过**联合训练方案**（Figure 12）使同一视频扩散模型同时充当策略、世界模型和价值函数。训练时采用 50% 策略 / 25% 世界模型 / 25% 价值函数的批次划分，通过不同条件掩码使模型学习三个条件分布：

- 策略：$p(a, s', V(s') \mid s)$
- 世界模型：$p(s', V(s') \mid s, a)$
- 价值函数：$p(V(s') \mid s, a, s')$

关键洞察在于**辅助监督的因果作用**：策略不仅学习 $p(a \mid s)$，还联合预测未来状态和价值，迫使模型学习更丰富的状态-动作关联。移除辅助损失（仅训练策略预测动作、世界模型预测下一状态）导致 LIBERO 平均成功率下降 1.5 点（Table 4），在 RoboCasa 上逐步去除未来状态和价值监督更使成功率从 67.1% 骤降至 44.4%（-22.7 点，Table 5），其中预测未来状态的影响最大。这表明联合预测未来状态是提升策略性能的核心因果杠杆。

### 从独立规划到内置模型基规划

统一建模使 Cosmos Policy 天然支持**基于模型的规划**：利用策略生成 N 个候选动作块，通过世界模型预测每个候选的未来状态，再由价值函数评估并选择最高价值状态对应的动作执行。在两项目标性 ALOHA 任务上，模型基规划（$V(s')$ 方案）相比基础无规划策略平均提高 12.5 分（Figure 7），验证了联合建模为规划提供的直接支撑能力。

### 创新边界与局限

当前创新存在以下边界：模型仅预测单个未来时间步的状态和价值，未探索多步预测与更深层次规划；基于模型的规划推理延迟较高（N=8 搜索约 4.9 秒），难以直接用于高频动态任务；世界模型和价值函数的精炼依赖策略 rollout 数据，外推能力有限。这些局限指向了未来优化的方向——推理加速、多步预测扩展和更高效的探索策略。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_wPEIStHxYH/figures/002_Figure_2.jpg]]
*Figure 2: The latent diffusion sequence of Cosmos Policy. We illustrate latent frame injection—the primary mechanism for adapting the pretrained Cosmos-Predict2 into a policy that can predict robot actions, future states, and values without architectural changes. First, raw images are tokenized into latent frames (first row). Then, additional modalities are inserted directly into the latent frame sequence of the video diffusion model (second row). The model is then tasked to denoise the noised latent frames conditioned on the clean frames (third row). See Section 4.1 for more details. (Note: For simplicity, this figure does not depict certain implementation details; see Figure 8 for a more detailed v...*

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_wPEIStHxYH/figures/023_Figure_12.jpg]]
*Figure 12: Cosmos Policy balanced batches training scheme. We illustrate the joint objectives training scheme discussed in Section 4.2. While each batch of training samples is split 50/25/25 for policy, world model, and value function training, respectively, the full latent diffusion sequence remains fixed, and the conditioning scheme determines which of the three functions is being optimized. During training, the model is tasked to denoise the target noised latent frames conditioned on the clean latent frames. Note that the above depicts the initial base policy training scheme. When optionally refining the world model and value function on policy rollouts (in preparation for model-based planning), we...*

Cosmos Policy 的核心设计理念是：**将机器人策略学习完全嵌入预训练视频扩散模型的去噪框架中，无需任何架构改动**。其整体 pipeline 围绕一个统一的 Cosmos-Predict2-2B-Video2World 潜在视频扩散模型展开，该模型同时充当策略、世界模型和价值函数三重角色。

### 输入输出流

**输入侧**，模型接收多模态观测：多相机 RGB 图像、机器人本体感受状态（如关节角度、末端位姿）以及可选的 T5-XXL 文本嵌入作为全局条件。**输出侧**，模型在统一的去噪生成过程中并行预测三个量：动作块（action chunk）、未来状态（由本体感受和图像观测表示）以及未来状态的价值 $V(s')$。

### 核心模块与数据流

pipeline 由四个关键模块串联，数据流贯穿始终：

1. **潜在帧注入（Latent Frame Injection）**：这是适配预训练视频模型的首要机制。机器人本体感受、动作块、状态价值等非图像模态被编码为与视频潜在帧相同维度的“潜在帧”，直接插入到视频扩散序列中。多相机视图则通过插入额外的图像潜在帧实现。整个过程等价于在原始视频序列中插入新的“通道”，无需修改模型架构（见图 Figure 2、Figure 8）。

2. **联合训练（Joint Training）**：训练批次按 50%/25%/25% 划分——50% 来自演示数据用于训练策略，25% 来自 rollout 数据训练世界模型，剩余 25% 训练价值函数。通过不同的条件掩码（conditioning mask）切换训练目标：
   - 策略学习 $p(a, s', V(s') \mid s)$
   - 世界模型学习 $p(s', V(s') \mid s, a)$
   - 价值函数学习 $p(V(s') \mid s, a, s')$
   
   这种联合训练使同一模型在统一的去噪得分匹配损失下获得辅助监督信号，实验证明移除辅助损失会导致性能显著下降（Table 4）。

3. **并行/自回归解码**：推理时，直接策略模式采用并行生成动作、未来状态和价值，以降低延迟；当需要高质量未来预测进行规划时，切换为自回归模式——先生成动作块，再以动作为条件生成未来状态，最后预测价值。

4. **基于模型的规划（Model-Based Planning）**：利用策略模型采样 $N$ 个候选动作块，通过精炼后的世界模型预测每个候选的未来状态，再由价值函数评分，选择最高价值状态对应的动作执行。为应对价值预测的双峰分布，采用“多数平均”（majority mean）聚合策略：先判断多数预测成功还是失败，再对多数组内的价值取均值。该模块在两项挑战性真实任务上带来平均 12.5 分的提升（Figure 7）。

### 关键设计决策

- **单阶段后训练**：与多阶段方法（先微调视频模型再训练独立动作模块）不同，Cosmos Policy 仅在机器人演示数据上做单阶段微调，直接产出可部署的策略。
- **零架构改动**：所有模态适配通过潜在帧注入完成，原始 Cosmos-Predict2 的 Transformer 去噪网络和 VAE 编解码器保持不变。
- **预训练至关重要**：从随机初始化训练（无视频模型先验）导致 LIBERO 平均成功率下降 3.9 个百分点（Table 4），验证了预训练时空先验的核心作用。

### 潜在帧注入：零架构改动的多模态适配

Cosmos Policy 的核心适配机制是**潜在帧注入**（Latent Frame Injection），其设计目标是无需修改预训练视频扩散模型（Cosmos-Predict2-2B-Video2World）的任何架构组件，即可将机器人策略所需的多模态输入和输出统一到视频扩散序列中。

具体实现流程如下（Figure 2, Figure 8）：
1. **输入侧**：在原始相机图像序列中插入空白（全零）图像，经 VAE 编码后在潜在空间中产生对应的空白潜在帧。
2. **模态编码**：将机器人本体感受（proprioception）、动作块（action chunk）、状态价值（state values）等非图像模态，以及额外的相机视图，分别编码为与图像潜在帧相同空间维度的潜在帧。对于向量形式的模态（如动作），通过重复填充因子 $\frac{H' \times W' \times C'}{K \times d_{act}}$ 将扁平化向量复制填充至潜在帧体积。
3. **交错注入**：将编码后的新模态潜在帧覆盖到空白潜在帧的位置，与原始图像潜在帧交错排列，形成统一的潜在扩散序列。

这一机制的灵活性体现在：可根据具体机器人配置自由增减潜在帧——例如，对于仅有一个第三视角相机的机器人，可移除额外相机视图对应的潜在帧。整个过程对预训练视频模型的去噪网络 $D_{\theta}$ 完全透明，实现了**零架构改动**的策略适配。

### 联合训练：策略、世界模型与价值函数的统一优化

Cosmos Policy 通过统一的去噪得分匹配损失同时训练三个功能模块，而非分别训练独立网络。核心训练损失沿用视频扩散模型的标准形式：

$$\mathcal{L}(D_{\theta}, \sigma) = \mathbb{E}_{\mathbf{x}_0, \mathbf{c}, \mathbf{n}} \left[ \| D_{\theta}(\mathbf{x}_0 + \mathbf{n}; \sigma, \mathbf{c}) - \mathbf{x}_0 \|_2^2 \right]$$

其中 $D_{\theta}$ 为去噪网络，$\sigma$ 为噪声水平（采用混合对数-均匀分布以增加高噪声权重，Figure 9），$\mathbf{c}$ 为 T5-XXL 文本嵌入条件。

三个功能模块通过**条件掩码**（conditioning mask）在潜在扩散序列中区分（Figure 12）：
- **策略**（Policy）：以当前观测 $s$ 为条件，联合预测动作块、未来状态和未来状态价值：
  $$p(a, s', V(s') \mid s)$$
- **世界模型**（World Model）：以当前状态和动作为条件，预测未来状态和价值：
  $$p(s', V(s') \mid s, a)$$
- **价值函数**（Value Function）：接收完整转移三元组，学习预测未来状态价值：
  $$p(V(s') \mid s, a, s')$$

其中价值函数在稀疏奖励设定下的定义为：
$$V^{\pi}(s) = \mathbb{E}_{\tau \sim \pi} \left[ \gamma^{H-t} R(s_H, a_H) \mid s_t = s \right]$$

即策略 $\pi$ 在状态 $s$ 的期望折现终止奖励，通过 Monte Carlo 回报 $\gamma^{H-t} R(s_H, a_H)$ 沿轨迹反向传播计算。

**批次划分策略**（Figure 12）：训练时采用 50% 演示数据 + 50% 策略 rollout 数据的混合批次：
- 50% 批次来自演示数据集，用于训练策略 $p(a, s', V(s') \mid s)$；
- 剩余 50% 来自策略 rollout 数据集，平分为两部分：一半训练世界模型 $p(s', V(s') \mid s, a)$，另一半训练价值函数 $p(V(s') \mid s, a, s')$。

这种联合训练设计的关键优势在于：策略不仅学习 $p(a \mid s)$，还通过辅助目标 $p(s', V(s') \mid s)$ 获得关于动作后果的额外监督信号，从而提升动作预测精度。消融实验证实，移除这些辅助损失导致 LIBERO 平均成功率从 98.5% 降至 97.0%（-1.5 点），而完全从随机初始化训练则进一步降至 94.6%（-3.9 点），验证了联合预测目标与预训练视频先验的双重重要性（Table 4）。

### 并行/自回归解码与基于模型的规划

推理时，Cosmos Policy 支持两种解码模式：
- **并行解码**：直接策略模式下，同时生成动作块、未来状态和价值，以降低推理延迟。
- **自回归解码**：当需要高质量未来预测进行规划时，依次生成 动作 $\rightarrow$ 未来状态 $\rightarrow$ 价值。

**基于模型的规划**（Model-Based Planning）利用世界模型和价值函数进行最佳动作搜索：策略首先生成 $N$ 个候选动作块，世界模型预测每个候选动作对应的未来状态，价值函数评估这些未来状态的价值，最终选择最高价值状态对应的动作执行。为提高鲁棒性，采用“多数平均”（majority mean）聚合策略——先通过固定阈值判断多数预测是否成功，再对多数组内的价值取平均。

在两项挑战性真实世界 ALOHA 任务上，基于模型的规划（$V(s')$ 方案）相比基础无规划策略平均提高 12.5 分（Figure 7），验证了统一世界模型和价值函数对规划的有效支撑。

### 关键训练细节

- **噪声分布调整**：将基础 Cosmos-Predict2 的对数正态分布改为混合对数-均匀分布：
  $$\sigma \sim 0.7 \cdot \text{LogNormal}(P_{\text{mean}}, P_{\text{std}}^2) + 0.3 \cdot \text{Uniform}(1.0, 85.0)$$
  增加高噪声水平的采样权重，以提升动作预测精度（Figure 9）。
- **单步去噪**：仅使用 1 步去噪推理时，RoboCasa 平均成功率仍达 66.4%，推理延迟从 0.61 秒降至 0.16 秒（约 4× 加速），验证了模型在低步数下的鲁棒性（Table 5）。

## 实验与关键发现

Cosmos Policy 在三个层级上进行了系统验证：两个模拟基准（LIBERO、RoboCasa）、一个真实世界双臂操作基准（ALOHA），以及基于模型的规划消融。所有实验均在固定初始条件下评估，并使用相同数量的真人演示进行微调（RoboCasa 仅 50 条，远低于对比方法的 300+ 条），确保数据公平。

### 模拟基准结果

**LIBERO 基准**（Table 1）涵盖四个任务套件（Spatial、Object、Goal、Long），Cosmos Policy 取得 **98.5%** 的平均成功率，超过所有对比方法，包括微调后的 VLA 模型 CogVLA（97.4%）和 FLARE（97.2%）。在 Object 套件上达到 100% 成功率，在最具挑战性的 Long 套件上以 97.6% 领先第二名 2.2 个百分点。结果基于每套件 500 次试验 × 3 个随机种子，共 6000 次试验。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_wPEIStHxYH/figures/004_Table_1.jpg]]
*Table 1: LIBERO simulation benchmark results. Success rates (SR) across four LIBERO benchmark task suites (Liu et al., 2024). Cosmos Policy success rates are averaged over 500 trials for each suite (10 tasks × 50 episodes) and three random seeds (6000 trials total). Our method achieves highest performance overall, even outperforming fine-tuned state-of-the-art vision-language-action (VLA) models. Table 2: RoboCasa simulation benchmark results. Success rates (SR) across 24 kitchen manipulation tasks (Nasiriany et al., 2024). Cosmos Policy success rates are averaged over 50 trials for each task and three random seeds (3600 trials total). Our method achieves a state-of-the-art average success rate of 6...*

**RoboCasa 基准**（Table 2）包含 24 个厨房操作任务。Cosmos Policy 以 **67.1%** 的平均成功率取得最优，略高于 FLARE（66.4%）和 GR00T-N1.5+HAMLET（66.4%）。关键优势在于数据效率：Cosmos Policy 仅使用 **50 条演示** 进行训练，而 FLARE 需要 300 条，GR00T-N1.5 需要 500 条，Diffusion Policy 需要 3000 条。结果基于每任务 50 次试验 × 3 个随机种子，共 3600 次试验。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_wPEIStHxYH/figures/005_Table_2.jpg]]

### 真实世界 ALOHA 双臂操作

真实世界评估包含四项高精度双臂操作任务（Figure 3）：将物品放到盘子上、将糖果放入碗中、将糖果放入自封袋、折叠衬衫。评估涵盖分布内（in-distribution）和分布外（OOD）初始条件（Figure 10、Figure 11），每方法每任务共 101 次试验，按统一评分细则打分（0-100 分）。

Cosmos Policy 取得 **93.6%** 的平均综合得分（Table 3），优于所有对比方法，包括 π0.5（88.6%）、π0（83.1%）、OpenVLA-OFT+（80.1%）和 Diffusion Policy（62.7%）。在四项任务中的三项（put on plate、put candies in bowl、fold shirt）获得最高分，在 OOD 条件下同样保持领先（91.0% vs. π0.5 的 84.5%）。

**定性失败模式分析**（Figure 5）揭示了 Cosmos Policy 相对于 VLA 方法的优势来源：π0.5 在自封袋任务中难以执行高精度抓取，导致滑块脱手；OpenVLA-OFT+ 在糖果任务中伸手到两颗糖果之间而非瞄准其中一颗，表明其对高度多模态动作分布的建模能力不足。Cosmos Policy 通过扩散模型天然的多模态分布捕捉能力克服了这些问题。

### 消融实验

**辅助损失与预训练的重要性**（Table 4，LIBERO）：去除辅助联合预测目标（策略仅学习 $p(a|s)$，世界模型仅学习 $p(s'|s,a)$）使平均成功率从 98.5% 降至 **97.0%**（-1.5 个百分点）。从随机初始化训练（无预训练视频模型先验）进一步降至 **94.6%**（-3.9 个百分点）。在 ALOHA 折叠衬衫任务上，从随机初始化训练的版本得分仅 80.8，比完整 Cosmos Policy 低 18.7 分，证实预训练视频模型的时空先验对数据效率至关重要。

**联合训练组件逐步消融**（Table 5，RoboCasa）：完整模型 67.1% → 去除价值函数训练样本 66.6%（-0.5）→ 进一步去除世界模型训练样本 64.0%（-3.1）→ 进一步去除辅助未来状态和价值监督 **44.4%**（-22.7）。预测未来状态的辅助监督贡献最大，表明联合建模未来状态对策略学习有强正则化作用。

**推理效率**（Table 5 底部）：仅使用 1 步去噪推理（而非默认的 4 步），RoboCasa 平均成功率仍达 **66.4%**（仅下降 0.7 个百分点），推理延迟从 0.61 秒降至 **0.16 秒**（约 4× 加速），验证了方法在低延迟场景下的实用性。

### 基于模型的规划

在两项最具挑战性的 ALOHA 任务（put candies in bowl、put candy in ziploc bag）的困难初始状态下，基于模型的规划（$V(s')$ 方案）相比基础无规划策略平均提高 **12.5 分**（Figure 7）。规划流程为：策略生成 N 个候选动作块 → 世界模型预测每个候选的未来状态 → 价值函数评估未来状态价值 → 选择最高价值状态对应的动作执行，并采用"多数平均"聚合提高鲁棒性。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_wPEIStHxYH/figures/009_Figure_7.jpg]]
*Figure 7: Model-based planning results. We evaluate the base Cosmos Policy on challenging initial states for the last two ALOHA robot tasks, and compare it with two planning variants (model-based and model-free). We find that the model-based variant ( V ( $s ^ { \prime }$ ) ) leads to highest overall performance*

世界模型的精炼对规划效果至关重要（Figure 6）：基础 Cosmos Policy 的世界模型仅用演示数据训练，可能无法预测错误（如自封袋滑块脱手）；利用策略 rollout 数据精炼后，世界模型能更准确地预测失败结果，从而使规划器能够规避这些失败。当前规划推理延迟较高（8×H100 GPU 上 N=8 搜索约 4.9 秒），限制了其在高频动态任务中的应用。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_wPEIStHxYH/figures/006_Figure_4.jpg]]
*Figure 4: Real-world ALOHA robot evaluation results. We evaluate state-of-the-art policies on a suite of four tasks and measure the score, which represents average percent completion of each task. Cosmos Policy achieves highest overall score, outperforming all other methods in three of four tasks*

## 定位与知识库关联

### 1. 核心瓶颈与设计动机

当前机器人策略学习面临一个关键瓶颈：**现有视频生成模型虽然具备强大的时空先验，但将其转化为机器人策略通常需要多阶段训练和额外的架构组件**（如单独的动作模块、逆动力学模型或定制化特征融合模块），无法直接利用预训练视频模型的核心去噪能力。这导致训练流程复杂、数据效率低下，且难以充分发挥视频模型对复杂高维动作分布的建模优势。

Cosmos Policy 的核心洞察在于：**预训练视频扩散模型的去噪得分匹配机制天然适合捕捉复杂高维动作分布**。通过将机器人动作、未来状态和价值统一编码为潜在帧，注入预训练视频扩散模型的潜在序列中，实现多模态统一建模——同一模型同时作为策略、世界模型和价值函数，无需任何架构改动。

### 2. 方法谱系定位

#### 2.1 与扩散策略方法的对比

**Diffusion Policy**（Chi et al., 2023）和 **Dita**（Hou et al., 2025）等扩散策略方法通常从随机初始化训练，使用独立的动作扩散头（U-Net 或 Transformer）生成动作，缺乏预训练视频模型提供的时空先验。Cosmos Policy 的核心区别在于：
- **训练流程**：从单阶段后训练（在机器人演示数据上直接微调预训练视频模型）替代多阶段训练（先微调视频模型，再训练独立动作生成模块）；
- **动作生成机制**：将动作块编码为潜在帧直接注入视频扩散序列，由去噪网络在统一目标下预测，而非使用单独的动作预测头。

消融实验证实了这一设计的关键性：从随机初始化训练（无预训练视频模型）使 LIBERO 平均成功率从 98.5% 降至 94.6%（-3.9 点），验证了预训练视频先验的不可替代性。

#### 2.2 与统一视频-动作模型的对比

**UVA**（Li et al., 2025a）和 **UWM**（Zhu et al., 2025）等统一视频-动作模型尝试将动作生成与视频预测结合，但其世界模型和价值函数通常作为独立模块训练，不与策略共享骨干。Cosmos Policy 的关键突破在于：
- **多模态信息整合**：通过潜在帧注入灵活整合多相机视图、本体感受和状态价值，无需引入额外编码器或特征融合模块；
- **世界建模与价值预测**：同一视频扩散模型同时充当策略、世界模型和价值函数，通过训练批次划分（50% 策略/25% 世界模型/25% 价值函数）和条件掩码统一优化。

消融实验表明，逐步去除价值函数训练样本、世界模型训练样本、辅助未来状态和价值监督，RoboCasa 平均成功率从 67.1% 逐步降至 44.4%（-22.7 点），证实了联合训练的显著增益。

#### 2.3 与 VLA 模型的对比

**π0**（Black et al., 2024）、**π0.5**（Intelligence et al., 2025）、**OpenVLA-OFT**（Kim et al., 2025）、**CogVLA**（Li et al., 2025b）、**DP-VLA**（Han et al., 2024）、**UniVLA**（Bu et al., 2025）和 **GR00T-N1.5**（Bjorck et al., 2025）等 VLA 模型通常依赖大规模语言模型或多模态 Transformer 架构，需要定制化设计来处理视觉-语言-动作的对齐。Cosmos Policy 的优势体现在：
- **数据效率**：在 RoboCasa 基准上仅使用 50 条演示达到 67.1% 平均成功率，远超其他方法所需的数据量（>300 条）；
- **真实世界性能**：在 ALOHA 双臂操作任务中取得 93.6% 平均任务完成得分，优于 π0.5 的 88.6%（+5.0 点）。

**FLARE**（Zheng et al., 2025）作为带有未来标记的扩散 Transformer 策略，在 RoboCasa 上达到 66.4% 的成功率，与 Cosmos Policy 的 67.1% 接近，但后者在数据效率和模型统一性上更具优势。

#### 2.4 与 Video Policy 的对比

**Video Policy**（Liang et al., 2025）同样利用视频模型进行策略学习，但 Cosmos Policy 的独特贡献在于：通过潜在帧注入实现零架构改动的多模态适配，并通过联合训练使同一模型同时具备策略执行、世界建模和价值评估能力，进而支持基于模型的规划——这在 Video Policy 中未被探索。

### 3. 适用边界与局限

尽管 Cosmos Policy 在模拟和真实世界基准上取得了领先性能，其当前设计存在以下边界约束：

1. **推理延迟与动态任务适配**：基于模型的规划推理延迟较高（在 8 块 H100 GPU 上 N=8 搜索约 4.9 秒），难以直接用于高频动态任务。虽然 1 步去噪推理可将延迟从 0.61 秒降至 0.16 秒（约 4× 加速）且 RoboCasa 成功率仅降至 66.4%，但规划模式下的延迟瓶颈仍未根本解决。

2. **世界模型精炼的数据依赖**：世界模型和价值函数的精炼依赖策略 rollout 数据，若数据覆盖有限，其外推能力不足，可能影响规划效果。在真实世界 ALOHA 实验中，基础 Cosmos Policy 的世界模型在“拉链袋抓取”任务上无法准确预测抓取失败的未来状态，需要额外微调才能实现有效规划。

3. **预测范围限制**：当前仅预测单个未来时间步的状态和价值，未探索多步预测与更深层次的规划（如模型预测控制），可能限制其在长时域任务上的表现。

4. **鲁棒性验证不足**：模型未经环境扰动、光照变化等鲁棒性专门训练，在复杂现实条件下的稳定性仍需验证。

### 4. 开放问题

1. 如何优化推理速度和搜索过程，使基于模型的规划适用于动态操控或移动任务？是否可以通过模型蒸馏、投机解码或更高效的搜索策略（如 beam search 的近似变体）来降低延迟？

2. 能否通过更高效的探索策略或数据增强（如利用视频模型本身生成多样化 rollout 数据），用更少的真实 rollout 数据达到有效的世界模型精炼？

3. 将预测范围扩展至多步未来序列并引入更深层次的规划（如模型预测控制或蒙特卡洛树搜索）是否能进一步提升长期任务的成功率？这需要解决累积误差和计算成本的双重挑战。

4. Cosmos Policy 的联合建模范式能否扩展到更广泛的具身任务，如结合自然语言指令的复杂多步规划？当前模型使用 T5-XXL 文本嵌入作为条件，但尚未充分利用语言理解能力进行指令跟随。

5. 在更多样、更具挑战性的真实场景（包括人机交互、动态障碍物避碰）中，统一视频扩散模型作为策略、世界模型和价值函数的方法是否依然保持优势？这需要更大规模的真实世界评估和鲁棒性测试。

## 原文 PDF

![[paperPDFs/ICLR_2026/Cosmos_Policy_Fine_Tuning_Video_Models_for_Visuomotor_Control_and_Planning.pdf]]
