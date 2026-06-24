---
title: "Object-Centric World Models from Few-Shot Annotations for Sample-Efficient Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Object_Centric_World_Models_from_Few_Shot_Annotations_for_Sample_Efficient_Reinforcement_Learning.pdf
openreview_forum_id: qmEyJadwHA
aliases:
- OS
- OCWMFFSASERL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将预训练分割模型提取的紧凑物体特征向量作为世界模型的额外输入，使其能够对物体动态和物体间交互进行显式建模。"
primary_logic: "利用少样本标注的冻结视频分割模型获取语义丰富的物体表示，将其与下采样像素融合，引导世界模型关注任务关键实体，从而在不依赖大量标注或内部状态的情况下显著提升样本效率。"
claims:
- "OC-STORM 在 Atari 100k 基准测试上的 HNS 均值达到 134.8%，显著优于 STORM 基线的 114.2%。"
- "在 Hollow Knight 的多个 Boss 战中，OC-STORM 比 STORM 收敛更快，最终性能更高。"
- "基于向量的物体特征能完整保留物体的状态和位置信息，如图 3a 所示，通过两个物体特征向量即可重建观察。"
- "在可检测到物体的游戏中，OC 方法性能大幅提升（HNS 均值 186.2% vs 基线 147.7%），而在无法检测到物体的游戏中仍与基线相当。"
---

# Object-Centric World Models from Few-Shot Annotations for Sample-Efficient Reinforcement Learning

> [!tip] 核心洞察
> 利用少样本标注的冻结视频分割模型获取语义丰富的物体表示，将其与下采样像素融合，引导世界模型关注任务关键实体，从而在不依赖大量标注或内部状态的情况下显著提升样本效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于少样本标注的以对象为中心的世界模型用于样本高效强化学习 |
| 英文题名 | Object-Centric World Models from Few-Shot Annotations for Sample-Efficient Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=qmEyJadwHA); [Project](https://oc-storm.weipuzhang.com) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | OC-STORM |
| Dataset | Atari 100k (26 games), Atari 100k (13 object-detectable games), Hollow Knight boss: God Tamer, Atari Boxing |

> [!tip] 效果简介
> - Atari 100k (26 games) 上，Human Normalized Score (HNS) mean 为 134.8% (Cutie-OC STORM)，对比 114.2% (STORM)，变化 +20.6 percentage points。
> - Atari 100k (13 object-detectable games) 上，HNS mean 为 186.2% (Cutie-OC STORM)，对比 147.7% (STORM)，变化 +38.5 percentage points。
> - Hollow Knight boss: God Tamer 上，Episode return 为 41.7 (OC-STORM)，对比 35.0 (STORM)，变化 +6.7。

## 概述

标准基于模型强化学习（MBRL）的世界模型通常依赖像素级重建损失进行训练。然而，这类损失天然偏向于占据画面大面积区域的静态背景，导致模型在预测动力学时忽略小而关键的决策相关物体（如游戏中的玩家角色、Boss等），最终拖累策略学习的样本效率与最终性能。**OC-STORM** 正是为解决这一瓶颈而提出：它利用一个冻结的、预训练的视频分割模型，从仅需数帧人工标注的掩码中提取紧凑的物体特征向量，并将这些向量与下采样后的像素观测融合，作为世界模型的输入。这一设计使得世界模型能够显式地捕捉物体的动态及其与场景的交互，从而引导策略关注任务关键实体。

在 Atari 100k 基准测试上，OC-STORM 的人类标准化得分（HNS）均值达到 **134.8%**，显著优于其基础架构 STORM 的 **114.2%**（Table 1）。在可检测到物体的 13 款游戏中，提升更为显著（HNS 均值 **186.2%** vs. 基线 **147.7%**）；而在无法检测到物体的游戏中，OC-STORM 的性能与基线基本持平，表明其不会因引入物体信息而产生负面影响。在 Hollow Knight 的多个 Boss 战中，OC-STORM 同样展现出更快的收敛速度和更高的最终回报（Figure 2）。

从方法定位来看，OC-STORM 属于**以对象为中心的世界模型**范畴，其核心创新在于将冻结分割模型提取的向量化物体表示与基于 Transformer 的时空序列模型相结合。与基于掩码的同类方法（如 **FOCUS**，Ferraro et al., 2023）相比，向量表示在低分辨率下计算效率更高且表现更优。消融实验进一步表明，仅使用物体模块（无视觉输入）已能获得可竞争的性能，但将物体模块与视觉模块结合使用效果最佳。该方法对分割失败具有较强的鲁棒性：即便在物体特征被随机置零的概率高达 50% 时，智能体仍能保持正回报（Figure 3b）。

综上，OC-STORM 通过少量人工标注和冻结分割模型，以较低的计算开销为世界模型注入了语义丰富的物体感知能力，在保持对非物体场景兼容性的同时，大幅提升了样本效率。

## 背景与动机

基于模型的强化学习（MBRL）通过学习环境的世界模型，使智能体能够在想象的轨迹上进行规划与策略优化，从而大幅提升样本效率。近年来，以 **DreamerV3**（Hafner et al., 2023）和 **STORM**（Zhang et al., 2023）为代表的世界模型方法在 Atari 等视觉控制基准上取得了显著进展。这些方法的核心思路是：将高维像素观察压缩为紧凑的潜在表示，在潜在空间中学习动力学模型，并基于模型生成的想象轨迹训练策略。

然而，标准的世界模型存在一个关键瓶颈：**基于像素重建的损失函数天然偏向大面积、静态的背景区域，而忽视了小而关键的决策相关物体**。如图 1 所示，STORM 能够精确重建背景（蓝色区域），却遗漏了对任务至关重要的玩家角色和 Boss 角色（橙色区域）。这种偏差直接导致两个后果：（1）世界模型未能学习到物体的运动动态和交互关系，动力学预测不准确；（2）基于不完整世界模型的策略学习受到阻碍，尤其在需要精细操控物体的场景中表现不佳。

解决这一问题的一种直观思路是引入以对象为中心的表示（object-centric representations），让世界模型显式地关注任务关键实体。现有方法大致分为两类：一类依赖无监督的对象发现（如 slot attention），但在复杂视觉环境中泛化能力有限；另一类利用预训练的检测或分割模型提取对象信息，但通常需要大量标注数据或引入高计算开销的掩码表示。

本文的核心动机在于：**能否以极低的标注成本，将预训练视觉模型的语义理解能力注入世界模型，使其在不牺牲计算效率的前提下，显式建模物体动态与交互？** 为此，作者提出了一种务实的方案——利用冻结的少样本视频分割模型（如 Cutie）从仅需少量标注帧中提取紧凑的物体特征向量，将这些向量与下采样像素融合后共同训练世界模型。这种设计的独特优势在于：

- **低标注成本**：仅需对少数帧进行物体标注，分割模型即可在时间维度上持续跟踪物体；
- **信息完整性**：基于向量的物体表示（而非掩码）能够完整保留物体的状态、位置和外观信息，如图 3a 所示，仅用两个物体特征向量即可重建出包含玩家和对手的完整观察；
- **计算效率**：向量表示比掩码表示更紧凑，避免了高分辨率掩码带来的计算开销。

通过这种设计，世界模型能够同时利用像素级视觉细节（来自下采样图像）和语义级物体信息（来自分割模型），从而在保持对背景建模能力的同时，获得对关键实体动态的显式理解。

## 核心创新

### 瓶颈定位：像素重建损失的决策盲区

基于模型的强化学习（MBRL）中，世界模型通常通过像素级重建损失进行训练。然而，这一标准范式存在一个被忽视的决策瓶颈：重建损失天然偏向于占据画面大面积的低频静态背景，而忽略了面积虽小但决策关键的动态物体。**STORM**（Zhang et al., 2023）等基于 Transformer 的世界模型在 Hollow Knight 等高分辨率环境中，能高精度重建背景区域，却完全遗漏了玩家角色和 Boss 等核心实体（Figure 1 左），导致动力学预测失真，策略学习受阻。因果链条可归纳为：

$$
\text{大面积背景主导重建梯度} \;\rightarrow\; \text{小物体信息被隐式丢弃} \;\rightarrow\; \text{物体动态与交互建模失败} \;\rightarrow\; \text{策略性能退化}
$$

### 核心洞察：冻结分割模型驱动的物体感知世界模型

OC-STORM 的核心洞察在于**将物体感知从世界模型的学习目标中解耦**：不再期望世界模型从像素中自行“发现”关键实体，而是借助一个冻结的、预训练的视频分割模型（Cutie/SAM2）显式注入物体信息。具体而言，仅需在首帧提供少量标注掩码，分割模型即可在后续帧中持续追踪物体，并输出紧凑的物体特征向量。这些向量与下采样至 $64\times64$ 的像素输入融合后，共同训练世界模型，使其能够对物体动态和物体-场景交互进行显式建模。

这一设计的决定性优势在于**语义保真度与样本效率的协同**：
- **语义保真度**：物体特征向量完整保留了物体的状态和位置信息。实验表明，仅凭两个物体特征向量即可重建出包含玩家和对手的完整观察（Figure 3a），证明向量表示未丢失决策关键信息。
- **样本效率**：在仅 100k 环境帧的 Atari 100k 基准上，Cutie-OC STORM 的 Human Normalized Score（HNS）均值达到 134.8%，较 STORM 基线的 114.2% 提升 20.6 个百分点（Table 1）。在可检测到物体的 13 款游戏中，提升更为显著（186.2% vs 147.7%，+38.5 个百分点）。

### 关键架构变更：三个 Changed Slots

相较于基线 STORM，OC-STORM 在以下三个关键维度进行了系统性改造：

**1. 世界模型输入：从单一像素到“像素+物体向量”双流融合**

| 维度 | STORM 基线 | OC-STORM |
|------|-----------|----------|
| 输入组成 | 仅 $64\times64$ 下采样像素 $s_t^{\mathrm{vis}}$ | $s_t^{\mathrm{vis}}$ + $K$ 个物体特征向量 $s_t^{\mathrm{obj}} \in \mathbb{R}^{K \times \mathrm{obj\_dim}}$ |
| 物体来源 | 无 | 冻结的 Cutie/SAM2 分割模型，仅需少样本标注 |
| 证据锚点 | Section 3.1, Equation (1) | 同左 |

融合后的输入同时保留了场景上下文（像素流）和实体语义（物体流），使世界模型无需从零学习物体概念。

**2. 动力学架构：引入空间注意力实现物体-场景交互**

| 维度 | STORM 基线 | OC-STORM |
|------|-----------|----------|
| 注意力模式 | 仅时间注意力 | 交替空间注意力 + 时间注意力 |
| 空间注意力范围 | 无 | 在 $K$ 个物体标记和 1 个视觉标记间进行注意力计算 |
| 交互建模 | 隐式 | 显式建模物体-物体、物体-场景交互 |
| 证据锚点 | Section 3.3 | 同左 |

空间注意力模块使物体标记能够“关注”视觉标记中的场景信息，反之亦然，从而捕捉物体与背景之间的因果交互（如角色与地形的碰撞）。

**3. 物体潜在编解码：独立的离散表示管道**

| 维度 | STORM 基线 | OC-STORM |
|------|-----------|----------|
| 物体编码器 | 无 | MLP 编码器，将 $s_t^{\mathrm{obj}}$ 映射为离散潜在变量 |
| 离散化方式 | 无 | 分类 VAE（16 个分类分布，各 16 类） |
| 解码器 | 无 | 从物体潜在变量重建物体特征 |
| 证据锚点 | Section 3.2, Appendix A | 同左 |

独立的物体潜在管道确保物体信息在离散化过程中不被像素信息稀释，同时分类 VAE 的离散瓶颈有效防止了复合预测误差在想象推演中的累积。

### 设计选择的经验支撑

消融实验（Figure 4a）验证了双流设计的必要性：仅使用物体模块（无视觉输入）已能获得可竞争的性能，但组合两者效果最优。此外，基于掩码的物体表示（FOCUS, Ferraro et al., 2023）在低分辨率下表现不如向量表示，且计算效率更低，进一步支持了向量表示作为物体信息载体的优越性。

对分割失败的鲁棒性分析（Figure 3b）表明，即使在 Atari Pong 中以 50% 概率将物体特征归零，智能体仍能保持正回报，说明世界模型学会了对物体信息的适度依赖而非机械记忆。

## 整体框架

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_qmEyJadwHA/figures/003_Figure_1.jpg]]
*Figure 1: (c) The proposed OC-STORM framework. A frozen, pretrained segmentation model extracts object feature vectors from a few annotated frames. These features are combined with downsampled pixels to train an OC world model, which is then used for policy learning via imagined trajectories. Figure 1: Left: STORM (Zhang et al., 2023) accurately reconstructs large background areas (blue) but overlooks the small, critical player and boss characters (orange), hindering policy learning. Right: Overview of the proposed OC-STORM framework. See Appendix A for network details*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_qmEyJadwHA/figures/010_Figure_5.jpg]]
*Figure 5: The model structure of our proposed OC-STORM. The tuples in square brackets represent the shapes of the corresponding tensors, where L denotes the batch length or sequence length, K is the number of objects, and H and W are the image height and width, respectively. The object module constitutes the proposed object-centric component, while the visual module processes resized raw observations. K ^ { * } equals K when only object module is used, equals 1 when only visual module is used, and equals K + 1 when both modules are used. The trainable token and positional embeddings are broadcast to match the shapes of the corresponding tensors. The reward logit is 255-dimensional and used for the sy...*

OC-STORM 的整体框架围绕一个核心设计展开：将冻结的预训练视频分割模型提取的紧凑物体特征向量，与下采样后的像素观测融合，共同馈入世界模型，使其显式建模关键实体的动态与交互。图 1 给出了该流程的概览。

**输入流**。在时间步 $t$，系统接收原始观测 $o_t \in \mathbb{R}^{3 \times H \times W}$。该观测同时流向两条路径：
1. **物体路径**：冻结的分割模型（Cutie 或 SAM2）基于少量人工标注的掩码帧，输出 $K$ 个物体的特征向量 $s_t^{\mathrm{obj}} \in \mathbb{R}^{K \times \mathrm{obj\_dim}}$。这些向量通过掩码池化（masked pooling）从分割模型的对象注意力输出中聚合得到，保留了物体的语义、状态和位置信息。
2. **视觉路径**：原始观测被下采样至 $64 \times 64$ 分辨率，得到视觉输入 $s_t^{\mathrm{vis}} \in \mathbb{R}^{3 \times 64 \times 64}$。

**编码与离散化**。物体特征和视觉输入分别通过各自的 MLP/CNN 编码器，进入一个分类 VAE（categorical VAE），将连续输入映射为离散潜在变量 $z_t$，以防止自回归预测中的复合误差。具体而言，物体路径使用 16 个分类分布、每分布 16 类的离散表示；视觉路径采用类似的离散化策略。解码器则从潜在变量重建原始输入，用于重建损失。

**时空序列模型**。潜在变量序列 $z_{1:L}^{\mathrm{obj}}$ 和 $z_{1:L}^{\mathrm{vis}}$ 与动作序列 $a_{1:L}$ 一同输入序列模型 $f_\phi$（基于 Transformer 或 RNN）。其核心创新在于交替应用空间注意力和时间注意力：
- **空间注意力**在每个时间步横跨 $K$ 个物体标记和 1 个视觉标记，实现物体-场景间的信息交互；
- **时间注意力**沿时间维度建模各标记的动态演化。

序列模型输出隐藏状态 $h_{1:L} \in \mathbb{R}^{(K+1) \times L \times d_h}$，其中 $K+1$ 对应物体标记加视觉标记的合并维度。

**预测头**。从隐藏状态 $h_t$ 出发，三个预测头分别负责：
- 动力学预测器 $g_\phi^{\mathrm{dyn}}$：预测下一时间步的潜在分布 $\hat{z}_{t+1}$；
- 奖励预测器 $g_\phi^{\mathrm{rew}}$：利用自注意力聚合所有标记信息，预测即时奖励 $\hat{r}_t$；
- 终止预测器 $g_\phi^{\mathrm{term}}$：预测 episode 终止概率 $\hat{\tau}_t$。

**策略学习**。世界模型训练完成后，Actor-Critic 策略网络（采用 DreamerV3 的算法）在世界模型生成的想象轨迹上进行训练。Actor 基于潜在变量和隐藏状态采样动作 $a_t \sim \pi_\theta(a_t | z_t, h_t)$，Critic 估计状态值 $V_\psi(z_t, h_t)$，使用 λ-回报作为目标。

**关键设计选择**。整个框架中，分割模型保持冻结，仅需对每个游戏提供少量（1–6 个）人工标注的掩码帧即可运行，无需在线标注或内部状态访问。物体特征以向量形式（而非掩码形式）表示，实验表明这一选择在低分辨率场景下既保留了充分的物体信息（图 3a 显示仅用两个物体特征向量即可重建观测），又比基于掩码的表示（如 FOCUS）计算效率更高。

## 核心模块与公式推导

### 整体框架

OC-STORM 在标准世界模型的基础上引入了一个**冻结的预训练分割模型**作为物体特征提取器，将物体感知与动力学学习解耦。框架包含以下核心模块：

1. **冻结分割模型**（Cutie 或 SAM2）：从少样本标注中提取 K 个物体的紧凑特征向量，保持时间一致性。
2. **物体特征编码器**（MLP）：将物体特征编码为离散潜在变量。
3. **视觉编码器**（CNN）：将下采样至 64×64 的像素图像编码为离散潜在变量。
4. **分类 VAE**：将连续输入离散化为 16 个分类分布（各 16 类），防止复合预测误差。
5. **时空序列模型**：交替应用空间注意力和时间注意力，建模物体动态、视觉动态及物体-场景交互。
6. **预测头**：从隐藏状态预测下一时刻的潜在分布、即时奖励和终止概率。
7. **解码器**：从潜在变量重建输入，用于重建损失。
8. **Actor-Critic 策略网络**：在想象轨迹上训练策略和价值函数。

### 关键公式与变量含义

**输入定义**（公式 1）：
$$o_t \in \mathbb{R}^{3 \times H \times W}, \quad s_t^{\mathrm{obj}} = \mathrm{SegModel}(o_t) \in \mathbb{R}^{K \times \mathrm{obj\_dim}}, \quad s_t^{\mathrm{vis}} = \mathrm{Resize}(o_t) \in \mathbb{R}^{3 \times 64 \times 64}$$
其中 $o_t$ 为时间步 $t$ 的原始高分辨率观察，$s_t^{\mathrm{obj}}$ 为分割模型提取的 $K$ 个物体特征向量，$s_t^{\mathrm{vis}}$ 为下采样至 64×64 的视觉输入。

**分类 VAE 编码与解码**（公式 2）：
$$z_t \sim q_{\phi}(z_t | s_t), \quad \hat{s}_t = p_{\phi}(z_t)$$
编码器 $q_{\phi}$ 将输入状态 $s_t$ 映射为离散潜在变量 $z_t$，解码器 $p_{\phi}$ 从潜在变量重建输入 $\hat{s}_t$。物体特征和视觉输入分别使用独立的分类 VAE。

**时空序列模型**（公式 3）：
$$h_{1:L} = f_{\phi}(z_{1:L}^{\mathrm{obj}}, z_{1:L}^{\mathrm{vis}}, a_{1:L}) \in \mathbb{R}^{(K+1) \times L \times d_h}$$
序列模型 $f_{\phi}$ 接收长度为 $L$ 的物体潜在变量序列、视觉潜在变量序列和动作序列，输出隐藏状态序列。空间注意力在每一时间步横跨 $K$ 个物体标记和 1 个视觉标记（共 $K+1$ 个标记），时间注意力沿序列维度传播信息。

**预测头**（公式 4）：
$$\hat{z}_{t+1} \sim g_{\phi}^{\mathrm{dyn}}(\hat{z}_{t+1} | h_t), \quad \hat{r}_t = g_{\phi}^{\mathrm{rew}}(h_t), \quad \hat{\tau}_t = g_{\phi}^{\mathrm{term}}(h_t)$$
动力学预测器 $g_{\phi}^{\mathrm{dyn}}$ 从隐藏状态 $h_t$ 预测下一时刻潜在分布 $\hat{z}_{t+1}$；奖励预测器 $g_{\phi}^{\mathrm{rew}}$ 利用自注意力聚合所有标记信息预测即时奖励 $\hat{r}_t$；终止预测器 $g_{\phi}^{\mathrm{term}}$ 预测终止概率 $\hat{\tau}_t$。

**世界模型总损失**（公式 7）：
$$\mathcal{L}(\phi) = \mathbb{E}_{\mathcal{D}}\left[ \mathcal{L}_{\mathrm{pred}}(\phi) + \mathcal{L}_{\mathrm{dyn}}(\phi) + 0.5\,\mathcal{L}_{\mathrm{rep}}(\phi) \right]$$
其中 $\mathcal{L}_{\mathrm{pred}}$ 为预测损失（重建 MSE + 奖励 symlog 损失 + 终止交叉熵），$\mathcal{L}_{\mathrm{dyn}}$ 为动态损失（KL 散度，以 1 为下界），$\mathcal{L}_{\mathrm{rep}}$ 为表示损失。系数 0.5 用于防止后验崩塌。

**Actor-Critic**（公式 8）：
$$\begin{array}{rll} \text{Critic: } & V_{\psi}(z_t, h_t) \approx \mathbb{E}_{\pi_{\theta},\phi} \left[ \sum_{k=0}^{T} \gamma^k r_{t+k} \right], \\ \text{Actor: } & a_t \sim \pi_{\theta}(a_t | z_t, h_t). \end{array}$$
Critic 网络 $V_{\psi}$ 基于潜在变量 $z_t$ 和隐藏状态 $h_t$ 估计状态值，Actor 网络 $\pi_{\theta}$ 采样动作 $a_t$。两者均使用世界模型生成的想象轨迹进行训练，采用 DreamerV3 的 λ-回报目标。

### 核心设计要点

**物体-视觉融合机制**：空间注意力在物体标记和视觉标记之间建立信息交换通道，使模型能够显式建模物体与场景的交互。消融实验表明，仅使用物体模块（无视觉输入）仍可获得可竞争的性能，但组合两者效果最优（Figure 4a）。

**向量表示优于掩码表示**：与基于掩码的对象表示（FOCUS）相比，基于向量的表示在低分辨率下表现更好且计算效率更高。掩码表示需要在高分辨率下操作才能保留空间细节，而向量表示通过压缩特征隐式保留了物体的状态和位置信息——仅用两个物体特征向量即可重建 Atari Boxing 的完整观察（Figure 3a）。

**对分割失败的鲁棒性**：通过随机将物体特征向量置零模拟分割失败，实验表明 OC-STORM 具有较强的容错能力：在 Atari Pong 中，即使零化概率达 50%，智能体仍能保持正回报（Figure 3b）。

## 实验与分析

### 核心瓶颈与因果机制

标准基于像素重建的世界模型（如 STORM, Zhang et al., 2023）在训练时，其重建损失天然偏向占据画面大面积的低频静态背景，而忽略了小而关键的任务相关物体（如玩家角色、敌人、球等）。这一偏差导致世界模型学到的动力学表征中，决策关键实体的状态和交互信息被严重稀释，进而阻碍策略学习。**Figure 1 (左)** 直观展示了这一现象：STORM 准确重建了背景区域（蓝色），却遗漏了关键的玩家和 Boss 角色（橙色）。

OC-STORM 的因果调节变量是：**将冻结的预训练视频分割模型（Cutie/SAM2）提取的紧凑物体特征向量，作为世界模型的额外结构化输入**。这些物体特征向量完整编码了物体的语义、外观和空间位置信息（**Figure 3a** 证实仅用两个物体特征向量即可重建观察），迫使世界模型的动力学模块显式建模物体动态及物体-场景交互。当物体可被检测到时，这一机制大幅提升样本效率；当无法检测到物体时，模型退化为基线，不会引入负面干扰。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_qmEyJadwHA/figures/007_Figure_3.jpg]]
*Figure 3: Analysis of the object feature. (a) Observation reconstructions on Atari Boxing with two object feature vectors as inputs. The object mask row highlights the relevant objects. (see Section 5.1 for details). (b) Training episode returns for Atari Boxing and Pong with 4 different zeroing probabilities (see Section 5.2)*

### Atari 100k 基准主要结果

**Table 1** 报告了 Atari 100k 基准（26 款游戏，100k 环境帧）上的核心结果。以人类归一化得分（HNS）均值衡量：

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_qmEyJadwHA/figures/004_Table_1.jpg]]
*Table 1: Game scores and overall human-normalized scores on the Atari 100k benchmark. We compare OC approaches (vector-based OC and mask-based FOCUS (Ferraro et al., 2023)) against baseline world models. Bold indicates scores within 5% of best. The highlighting is computed separately with respect to the Dreamer and STORM baselines, shown in blue and red, respectively. The last column ‘#obj’ denotes manually annotated objects per game. All experiments use identical lightweight configurations suitable for high-resolution environments. STORM serves as the primary baseline due to its computational efficiency*

- **Cutie-OC STORM** 达到 **134.8%**，显著优于 STORM 基线的 **114.2%**（提升 20.6 个百分点）。
- **SAM2-OC STORM** 达到 **124.6%**，也明显超过 STORM 基线。
- 基于掩码的对象表示方法 **FOCUS**（Ferraro et al., 2023）在低分辨率下表现不如向量表示，且计算效率更低。

按游戏类别分解后，因果效应更加显著：

- 在 **13 款可检测到物体的游戏**中，Cutie-OC STORM 的 HNS 均值高达 **186.2%**，远超 STORM 基线的 **147.7%**（提升 38.5 个百分点）。
- 在 **13 款无法检测到物体的游戏**中，OC 方法仍保持与基线相当的性能（HNS 均值 69.2%–83.4% vs 基线 74.5%），说明物体模块的引入不会损害原有能力。

与外部 MBRL 方法的比较（**Table 2**）显示，OC-STORM 的 HNS 均值（134.8%）与 DIAMOND（145.9%, Alonso et al., 2024）、Δ-IRIS（136.7%, Micheli et al., 2024）等基于 Transformer 或扩散模型的方法具有竞争力，但 OC-STORM 的计算开销显著更低。

### Hollow Knight 上的样本效率

在 Hollow Knight 的多场 Boss 战中，OC-STORM 展现出更高的样本效率和最终性能。**Figure 2** 的训练曲线表明，OC-STORM 在大多数 Boss（尤其是 Mage Lord 和 Pure Vessel）上收敛更快，最终回报更高。**Table 4** 的数值结果显示：

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_qmEyJadwHA/figures/005_Figure_2.jpg]]
*Figure 2: The training episode returns on Hollow Knight. We use a solid line to represent the mean of 3 seeds and use a semi-transparent background to represent the standard deviation*

- **God Tamer**：OC-STORM 回合回报 **41.7** vs STORM **35.0**（提升 6.7）。
- 多个 Boss 的胜率（Win Rate）指标上，OC-STORM 同样优于 STORM。

### 模块消融分析

**Figure 4a** 的模块消融实验揭示了各输入模块的贡献：

- **仅使用物体模块（No-visual）**：仍能获得可竞争的性能，证明物体特征向量自身包含足够的任务相关信息。
- **组合物体模块与视觉模块（OC-STORM）**：在所有任务上均取得最佳性能，表明两者互补——物体模块提供精确的实体动态，视觉模块补充场景上下文。
- **FOCUS 掩码表示**：在 Atari 和 Hollow Knight 任务上均不及向量表示，且计算效率更低，验证了向量表示在低分辨率世界模型中的优势。

### 分割失败鲁棒性

OC-STORM 对分割模型的失败具有较强鲁棒性。**Figure 3b** 通过随机将物体特征向量置零来模拟分割失败：

- 在 Atari Pong 中，即使零化概率高达 **50%**，智能体仍能保持正回报。
- 随着分割模型检测准确率的提升，智能体性能单调改善，表明方法能从更好的视觉模型中持续获益。

### 标注数量的影响

**Figure 9** 考察了标注掩码数量对性能的影响。将标注掩码数量从 1 增加到 6，提高了 Atari Boxing 和 Pong 上的性能鲁棒性。这表明更丰富的少样本标注有助于分割模型更稳定地跟踪物体，进而提升策略学习质量。

### 物体缺失的影响

消融实验（**Figure 15**）表明，移除直接受动作影响的物体会导致性能大幅下降，验证了物体特征对任务关键实体建模的必要性。但某些物体（如 Breakout 中的砖墙）的引入可能产生负面影响，提示物体选择需要任务相关性判断。

### Meta-world 连续控制任务

在 Meta-world 连续控制任务上（**Figure 4b**），OC-STORM 比 STORM 展现出更高的样本效率，且在某些任务上优于专门设计的 MWM（Seo et al., 2022）。这表明物体中心的方法不仅适用于离散控制的 Atari 游戏，也可泛化至连续控制场景。

### 计算开销

**Table 5** 和 **Table 6** 报告了 OC-STORM 的计算开销。在单张 NVIDIA RTX 4090 GPU 上，分割推理是主要的额外开销来源（Cutie 加载约 1500ms）。整体而言，引入物体模块后训练时间有所增加，但仍在可接受范围内，且换来了显著的样本效率提升。

### 已知失败模式

1. **重复实例跟踪失败**：**Figure 10** 展示了 Hollow Knight Mantis Lords 场景中 Cutie 对重复实例的跟踪丢失问题。当场景中存在多个外观相同的物体时，分割模型可能混淆或丢失其中一个实例。
2. **几何结构难以编码**：**Figure 11** 指出，当前物体特征向量难以编码隧道、墙壁等几何结构信息（如 Atari Gopher 中的地下隧道），这可能限制方法在需要空间推理的环境中的表现。

### 补充图表

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_qmEyJadwHA/figures/008_Figure_7.jpg]]
*Figure 7: (a) Module ablation training curves*

## 方法谱系与知识库定位

### 1. 方法贡献的因果逻辑链

OC-STORM 的核心贡献在于识别并解决了基于像素重建的世界模型中的一个关键瓶颈：标准重建损失（MSE）天然偏向大面积静态背景，导致模型忽略小而关键的决策相关物体（如 Atari 中的玩家角色、Hollow Knight 中的 Boss）。这一瓶颈直接限制了动力学预测的精度和策略学习的样本效率。

为解决该问题，OC-STORM 引入了一个因果调节旋钮：将冻结的预训练视频分割模型（Cutie/SAM2）提取的紧凑物体特征向量作为世界模型的额外输入。这一设计的因果机制是：

1. **信息完整性**：物体特征向量通过掩码池化保留了物体的状态和位置信息，如图 3a 所示，仅用两个物体特征向量即可重建 Atari Boxing 的完整观察。
2. **显式建模**：交替的空间-时间注意力架构使模型能够显式建模物体动态和物体-场景交互，而非依赖隐式的像素模式。
3. **少样本标注**：只需对每个游戏手动标注 1-6 个物体掩码，冻结的分割模型即可持续跟踪，无需大量标注或内部状态访问。

### 2. 与基线方法的关系

#### 2.1 主要基线：STORM（Zhang et al., 2023）

OC-STORM 直接建立在 STORM 之上，STORM 是一个基于 Transformer 的高效世界模型。OC-STORM 对 STORM 的改动集中在三个关键插槽：

| 插槽 | STORM 基线值 | OC-STORM 改进 |
|------|-------------|--------------|
| 世界模型输入 | 仅下采样 64×64 像素图像 | K 个物体特征向量 + 64×64 像素图像融合 |
| 空间注意力 | 仅时间注意力 | 交替空间注意力（跨物体标记和视觉标记）和时间注意力 |
| 物体编码器/解码器 | 无 | 针对物体特征向量的 MLP 编码器/解码器，配备独立分类 VAE |

在 Atari 100k 基准上，OC-STORM（Cutie 版本）的 HNS 均值达到 134.8%，显著优于 STORM 基线的 114.2%（+20.6 个百分点）。在可检测到物体的 13 款游戏中，提升更为显著：OC-STORM 的 HNS 均值为 186.2%，而 STORM 为 147.7%（+38.5 个百分点）。

#### 2.2 其他世界模型基线：DreamerV3（Hafner et al., 2023）

DreamerV3 是基于 RNN 的世界模型，无空间注意力机制。OC 方法同样可应用于 DreamerV3 骨干，但论文选择 STORM 作为主要基线，因其计算效率更高且 Transformer 架构天然支持空间注意力扩展。

#### 2.3 基于掩码的对象表示：FOCUS（Ferraro et al., 2023）

FOCUS 使用基于掩码的对象表示（如 Slot Attention 风格的掩码重建），而 OC-STORM 使用紧凑的向量表示。实验表明，向量表示在低分辨率下表现优于掩码表示，且计算效率更高。在 Atari 100k 上，FOCUS 的 HNS 均值低于 OC-STORM 的向量方法。

#### 2.4 外部 MBRL 方法

在 Atari 100k 基准上，OC-STORM 与多种外部方法进行了比较（Table 2）：
- **SPR**（Schwarzer et al., 2021）：典型的样本高效无模型方法
- **IRIS**（Micheli et al., 2023）和 **TWM**（Robine et al., 2023）：基于 Transformer 的 MBRL 方法
- **Δ-IRIS**（Micheli et al., 2024）：IRIS 的升级版本
- **DIAMOND**（Alonso et al., 2024）：基于扩散模型的 MBRL 方法

OC-STORM 在可检测物体的游戏中表现优异，但在无法检测物体的游戏中与这些方法相当。

### 3. 适用边界与局限性

#### 3.1 已知适用场景

- **离散控制与像素观察**：Atari 100k 和 Hollow Knight Boss 战均属于此类。
- **连续控制**：在 Meta-world 任务上，OC-STORM 比 STORM 样本效率更高，且在某些任务上优于 MWM（Seo et al., 2022）。
- **可检测物体的环境**：当环境中存在可通过少样本标注分割的物体时，OC 方法带来显著增益。

#### 3.2 已知局限

1. **重复实例的跟踪失败**：当环境中存在多个相同外观的物体时（如 Hollow Knight 的 Mantis Lords），分割模型可能丢失对某个实例的跟踪（Figure 10）。这是视频分割模型的固有问题。

2. **几何结构难以编码**：物体特征向量难以编码墙壁、隧道等几何结构信息（Figure 11，Atari Gopher 中的地下隧道）。这些结构对导航至关重要，但无法被简单地表示为“物体”。

3. **物体选择的影响**：移除直接受动作影响的物体会导致性能大幅下降；而某些物体（如 Breakout 中的砖墙）甚至可能产生负面影响（Figure 15）。这表明物体标注的质量和选择策略对性能有显著影响。

4. **分割模型依赖**：OC-STORM 的性能依赖于分割模型的检测精度。如图 3b 所示，随着零化概率增加（模拟分割失败），智能体性能下降，但在 50% 零化概率下仍能保持正回报，表明一定鲁棒性。

5. **计算开销**：引入分割模型和物体特征处理增加了计算开销（Table 5），但论文声称相对于性能提升是可接受的。

### 4. 开放问题

1. **如何自动选择关键物体？** 当前方法依赖手动标注，如何自动识别对任务关键的物体仍是一个开放问题。错误的物体选择可能引入噪声甚至降低性能。

2. **如何处理重复实例？** 分割模型对相同外观物体的跟踪失败问题需要更鲁棒的解决方案，可能涉及实例级特征区分或时间一致性约束的改进。

3. **如何编码几何结构？** 将墙壁、边界等非物体几何结构纳入以对象为中心的表示是一个重要方向，可能需要混合表示（如结合向量和空间特征图）。

4. **物体表示的泛化性**：当前方法对每个游戏独立标注物体，如何实现跨游戏或跨任务的物体表示迁移尚待探索。

5. **与无监督物体发现的结合**：Table 3 综述了 Slot Attention、SAVi 等无监督物体发现方法。将这些方法与 OC-STORM 结合，可能消除对少样本标注的依赖，但需要解决无监督方法在复杂场景中的稳定性问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/Object_Centric_World_Models_from_Few_Shot_Annotations_for_Sample_Efficient_Reinforcement_Learning.pdf]]
