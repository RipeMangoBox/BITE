---
title: "Is Ego Status All You Need for Open-Loop End-to-End Autonomous Driving?"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/Is_Ego_Status_All_You_Need_for_Open_Loop_End_to_End_Autonomous_Driving.pdf
project_link: null
code_link: https://github.com/NVlabs/BEV-Planner
aliases:
- BPBPBPBPM
- IESAYNOLEEAD
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "自车状态是否被引入模型，以及其在 BEV 编码器或规划器中的使用方式，是决定规划性能的关键因果旋钮。"
primary_logic: "在现有基准下，端到端自动驾驶模型对自车状态过度依赖，感知信息并未有效贡献于规划；引入新的路缘碰撞率（CCR）能揭示这种缺陷，并且即使不使用任何感知标注也能达到与现有复杂方法相当甚至更好的开环规划性能，但这并不反映真实驾驶能力。"
claims:
- "Ego-MLP 仅使用自车状态，在 L2 距离和碰撞率上与 UniAD、VAD 等复杂方法持平甚至更优。"
- "nuScenes 中 73.9% 的场景为直行，自车状态足以应对大部分情况。"
- "使用空白图像作为输入时，感知完全失效，但规划性能几乎不受影响，而当自车速度被扰动时规划剧烈变化。"
- "现有的纯直行策略（GoStraight）以及 Ego-MLP 在路缘碰撞率（CCR）上显著高于利用地图感知的方法，揭示传统度量无法捕捉偏离道路的危险。"
---

# Is Ego Status All You Need for Open-Loop End-to-End Autonomous Driving?

> [!tip] 核心洞察
> 在现有基准下，端到端自动驾驶模型对自车状态过度依赖，感知信息并未有效贡献于规划；引入新的路缘碰撞率（CCR）能揭示这种缺陷，并且即使不使用任何感知标注也能达到与现有复杂方法相当甚至更好的开环规划性能，但这并不反映真实驾驶能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 自车状态是否为开环端到端自动驾驶的全部所需？ |
| 英文题名 | Is Ego Status All You Need for Open-Loop End-to-End Autonomous Driving? |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2312.03031) · [GitHub](https://github.com/NVlabs/BEV-Planner) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | BEV-Planner (含变体 BEV-Planner+，BEV-Planner++, BEV-Planner+Map) |
| Dataset | nuScenes val (开环规划) |

> [!tip] 效果简介
> - nuScenes val (开环规划) 上，L2 距离 (m) ↓ 均值 为 BEV-Planner++ (0.35)，对比 UniAD (official, 0.66)，变化 -0.31。
> - nuScenes val (开环规划) 上，碰撞率 (%) ↓ 均值 为 BEV-Planner++ (0.34)，对比 UniAD (official, 0.62)，变化 -0.28。
> - nuScenes val (开环规划) 上，路缘碰撞率 (%) ↓ 均值 为 BEV-Planner++ (3.16)，对比 UniAD (official, 1.72)，变化 +1.44。

## 概要

端到端自动驾驶旨在直接从传感器输入映射到规划轨迹，但当前开环评测体系存在一个被忽视的致命缺陷：**模型可以通过过度依赖自车状态（ego status）这一简单捷径来“刷榜”，而无需真正利用感知信息理解场景**。本文通过系统性分析揭示，在广泛使用的 nuScenes 数据集上，高达 73.9% 的场景为简单直行（Figure 2），且传统的 L2 距离与碰撞率指标无法有效惩罚偏离道路边界的危险行为，使得仅使用自车速度、加速度、偏航角和驾驶指令的 **Ego-MLP** 模型，在不使用任何感知模块的情况下，竟能达到与 UniAD、VAD 等复杂端到端方法相当甚至更优的开环规划性能（Table 1）。

这一发现的核心因果旋钮在于**自车状态是否被引入模型，以及其在 BEV 编码器或规划器中的使用方式**。当自车状态被注入规划流程时，感知信息的贡献被严重稀释——即使将相机输入替换为空白图像，导致检测和地图感知完全失效，规划性能几乎不受影响；然而一旦对自车速度施加扰动（如设为零或 100 m/s），轨迹预测则剧烈恶化并产生不合常理的结果（Table 2, Figure 4）。这直接证明现有方法在基准测试中并未真正学会“看路”，而是学会了“记车速”。

为揭示这一隐藏缺陷，本文提出了新的**路缘碰撞率（CCR）**指标，量化预测轨迹与道路边界的交互频率。实验表明，纯直行策略（GoStraight）和 Ego-MLP 在传统指标上表现尚可，但在 CCR 上显著恶化；而 UniAD 的后处理优化虽降低了车辆间碰撞率，却大幅增加了冲出道路边界的风险（Table 6, Appendix Figure 3）。这说明传统度量体系存在根本性盲区。

在方法层面，本文设计了极简基线 **BEV-Planner** 及其变体，通过可学习的 ego query 与 BEV 特征做交叉注意力后直接回归轨迹，无需任何人工标注（检测框、跟踪 ID、高精地图等）。该系列方法的定位是**分析性工具而非可部署系统**，旨在剥离复杂模块以精确量化自车状态的影响。主要发现包括：引入自车状态后模型收敛极快（Figure 5），BEV 特征仅关注自车附近区域（Figure 6）；添加地图感知任务虽能改善 CCR，但会牺牲 L2 和碰撞率（Table 3），暴露出多目标权衡的困境。

综上，本文的核心结论是：**在当前开环基准下，自车状态几乎就是规划性能的全部所需，但这恰恰反映了评测体系而非模型能力的缺陷**。这一发现对端到端自动驾驶领域的基准设计、公平比较和模型评估提出了根本性质疑。



端到端自动驾驶旨在将感知、预测与规划统一于一个可学习的框架中，从而避免传统模块化架构中的信息损失与误差累积。近年来，以 **UniAD** (Hu et al., CVPR 2023) 为代表的方法在 nuScenes 开环规划基准上取得了显著进展，通过引入检测、跟踪、建图与轨迹预测等多重辅助任务，逐步提升了规划性能。然而，这一研究范式的评估体系存在一个被长期忽视的致命缺陷：**开环评测中的规划性能究竟来自模型对场景的感知理解，还是仅仅来自对自车状态（ego status）的过拟合？**

本文通过系统性的分析揭示，当前开环端到端自动驾驶评测存在三个相互关联的瓶颈：

**1. 数据集分布严重失衡。** 对 nuScenes 数据集的自车轨迹热力图分析显示，73.9% 的场景为简单直行工况（Figure 2）。在这种分布下，模型仅凭自车当前速度与偏航角即可推断出合理的未来轨迹，而无需真正理解周围的道路结构、交通参与者或交互意图。

**2. 评估度量存在盲区。** 现有主流的 L2 距离与碰撞率（Collision Rate）两项指标无法全面评估轨迹的安全性。具体而言，碰撞率仅检测自车与其他车辆或障碍物的冲突，但完全忽略了对道路边界（路缘）的侵犯。这意味着一条冲出道路、驶入人行道或绿化带的轨迹，只要未与其他车辆发生碰撞，仍可在现有度量下获得高分。此外，已有方法的碰撞检测实现还存在忽略自车偏航角变化的缺陷，导致误检（附录 Figure 1）。

**3. 自车状态捷径的隐蔽性。** 许多现有方法在 BEV 特征生成阶段通过 BEVFormer 等模块隐式引入了自车状态信息（附录 Figure 4），但未在论文中明确讨论这一设计对规划性能的决定性影响。这导致不同方法之间的比较缺乏公平性——使用自车状态的方法天然具有巨大优势，而这一优势与感知能力无关。

基于上述分析，本文提出核心洞察：**在现有基准下，端到端自动驾驶模型对自车状态存在过度依赖，感知信息并未有效贡献于规划决策。** 这一现象并非某个特定模型的缺陷，而是当前评测范式系统性失效的体现。为验证这一假设，本文设计了 Ego-MLP（仅使用自车速度、加速度、偏航角和驾驶指令的简单 MLP）和 BEV-Planner 系列基线，并通过引入路缘碰撞率（Curb Collision Rate, CCR）作为补充度量，试图揭示被传统指标掩盖的安全隐患，推动社区重新审视开环评测的可靠性与公平性。



## 核心方法与创新机理

本文的核心创新并非提出一种性能更强的端到端自动驾驶模型，而是通过系统性的因果分析，揭示当前开环评测范式下模型对**自车状态（ego status）**的过度依赖，并据此设计极简基线以暴露基准缺陷。其关键“因果旋钮”在于**自车状态是否被引入模型，以及其在 BEV 编码器或规划器中的使用方式**。

### 1. 自车状态作为因果旋钮的显式操控

通过对现有 SOTA 方法的复现与消融，本文识别出两个决定规划性能的关键设计槽位（changed slots）：

- **BEV 编码器中的自车状态注入**：官方 UniAD（Hu et al., CVPR 2023）在 BEV 模块中隐式使用了自车状态（Table 1, ID-2），而许多后续工作未意识到这一细节。本文通过将 `use can bus flag` 设为 `False`，显式移除了该信息（UniAD ID-1），发现 L2 距离从 0.66m 急剧恶化至 1.03m，碰撞率从 0.62% 升至 0.77%（Table 1）。
- **规划器中的自车状态注入**：在 VAD-Base 和 BEV-Planner 的规划器中，通过将自车状态向量与 query 特征拼接（遵循 VAD 的设计），可进一步引入 ego status 捷径（Table 1, ID-6, ID-12）。

这种对因果旋钮的显式操控，使得本文能够精确量化自车状态在不同模块中对最终规划性能的贡献。

### 2. 极简基线的构建：剥离感知以暴露捷径

为证明感知信息在现有基准下并非规划的必要条件，本文构建了**Ego-MLP**——一个仅使用自车速度、加速度、偏航角和驾驶指令的 MLP 模型，完全摒弃了相机输入与感知模块。决定性证据显示：

> Ego-MLP 在 L2 距离（均值 0.35m）和碰撞率（均值 0.29%）上与 UniAD、VAD 等复杂方法持平甚至更优（Table 1, ID-8 vs ID-2/ID-4）。

这一结果与 nuScenes 数据集的分布偏斜高度相关——**73.9% 的场景为简单直行**（Figure 2），自车状态足以应对大部分情况。

### 3. 鲁棒性测试：因果方向的强验证

通过干预实验，本文验证了因果方向：

- **移除相机输入（空白图像）**：感知模块完全失效（Det. NDS=0.0, Map mAP=0.0），但规划性能几乎不受影响（L2 均值 0.46m，碰撞率 0.54%）（Table 2）。
- **扰动自车速度**：将速度设为零导致模型预测静止轨迹（L2 均值 6.16m）；设为 100 m/s 则产生不合常理的轨迹（L2 均值 208m）（Table 2, Figure 4）。

这表明规划输出对自车状态高度敏感，而对感知信息近乎免疫——感知与规划之间存在严重的因果断裂。

### 4. 新度量揭示隐藏缺陷：路缘碰撞率（CCR）

传统 L2 距离和碰撞率无法捕捉轨迹偏离道路边界的危险。本文引入**路缘碰撞率（Curb Collision Rate, CCR）**，揭示了被旧度量掩盖的问题：

- **GoStraight**（按当前速度直行的朴素策略）在 L2 和碰撞率上表现尚可，但频繁与道路边界相交（CCR 显著偏高）。
- **Ego-MLP** 的 CCR（3.16%）比 UniAD（1.72%）高出近一倍（Table 1）。
- **UniAD 的后处理优化**虽然将碰撞率从 0.62% 降至 0.51%，却使 CCR 从 1.72% 飙升至 7.83%（Table 6, Appendix），因为优化后的轨迹为避开车辆而冲出道路边界（Figure 3, Appendix）。

### 5. 方法谱系与知识库定位

本文的 BEV-Planner 系列并非旨在提出可部署的驾驶系统，而是作为**分析性基线**，定位于端到端自动驾驶的评测批判与基准反思：

- **BEV-Planner**：使用 R50 骨干提取多视图特征生成 BEV，沿通道拼接过去 4 帧历史 BEV（无对齐），通过可学习的 ego query 与融合 BEV 特征做交叉注意力，再经 MLP 直接回归未来轨迹。不使用任何感知标注（3D 框、跟踪 ID、高精地图），仅以 L1 损失监督轨迹。其公式为：
  $$\tau = \mathbf{MLP}(\mathbf{attn}(q=Q, k=B, v=B))$$
  其中 $Q$ 为可学习 ego query，$B$ 为融合历史后的 BEV 特征（Eq. 1, Section 3）。

- **BEV-Planner++**：在规划器中引入自车状态，与 ego query 特征拼接后预测轨迹。该变体收敛极快（Figure 5），但 BEV 特征激活范围仅局限于自车附近（Figure 6），表明模型几乎不利用场景上下文。

- **BEV-Planner+Map**：向 BEV 特征添加地图分割头（遵循 UniAD 设计），引入道路边界信息。虽然 L2 距离和碰撞率变差（0.55→0.96, 0.59→0.89），但 CCR 显著改善（4.26→2.60）（Table 3），验证了地图感知对道路边界安全的必要性。

与现有方法的本质区别在于：**BEV-Planner 系列不依赖任何人类标注数据**，其设计目标不是追求 SOTA 性能，而是通过最小化感知依赖来暴露 ego status 捷径的严重性。这一方法论贡献对社区重新审视开环评测基准具有警示意义——在数据集分布偏斜和度量缺陷的双重作用下，复杂的感知-预测-规划流水线可能只是在学习一个精致的自车状态插值器。



![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2312_03031/figures/001_Figure_1.jpg]]
*Figure 1: (a) AD-MLP uses both ego status and past trajectory GTs as input. Our reproduced version (Ego-MLP) drops the past trajectories. (b) The existing end-to-end autonomous driving pipeline consists of perception, prediction, and planning modules. Ego status can be integrated into the bird’s-eye view (BEV) generation module or within the planning module. (c) We design a simple baseline for comparison with existing methods. The simple baseline does not leverage the perception or prediction module and directly predicts the final trajectories based on BEV features*

本文的核心目标是诊断开环端到端自动驾驶中自车状态（ego status）对规划性能的支配性影响，而非提出一个全新的 SOTA 模型。为此，作者构建了一个极简的分析性基线——**BEV-Planner** 及其变体，以剥离感知、预测等复杂模块，直接检验“BEV 特征 + 自车状态”的最小规划回路。

**整体流水线**

BEV-Planner 的流水线刻意省略了传统端到端驾驶框架中的显式感知（检测、跟踪、建图）和预测模块，仅保留三个核心环节：

1. **BEV 特征生成与历史融合**  
   使用 R50 骨干网络从多视图图像中提取特征，生成分辨率为 128×128（感知范围约 50 米）的 BEV 特征。随后，将过去 4 帧的历史 BEV 特征沿通道维度直接拼接至当前帧，**不进行任何对齐操作**。

2. **Ego Query 交叉注意力**  
   引入一个可学习的 ego query 嵌入，与融合后的 BEV 特征进行交叉注意力，以聚合全局上下文信息。这一设计使得模型无需依赖检测框、跟踪 ID 或高精地图等人工标注。

3. **MLP 轨迹预测头**  
   将精炼后的 ego query 通过 MLP 直接回归未来轨迹点 $\tau$，仅使用 L1 损失进行监督。整个过程可形式化为：
   $$\tau = \mathbf{MLP}(\mathbf{attn}(q=Q, k=B, v=B))$$
   其中 $Q$ 为 ego query，$B$ 为融合后的 BEV 特征。

**关键变体与因果旋钮**

为系统性地控制“自车状态”这一因果旋钮，作者设计了以下变体：

- **BEV-Planner（ID-10）**：基础版本，不使用自车状态，也不使用地图感知。
- **BEV-Planner++（ID-12）**：在规划器中显式引入自车状态（速度、加速度、偏航角、驾驶指令），与 query 特征拼接后输入 MLP。
- **BEV-Planner+Map**：在 BEV-Planner 基础上添加地图感知分支（主要遵循 UniAD 的设计），以引入道路边界信息，用于改善路缘碰撞率（CCR）。

此外，作者还构建了 **Ego-MLP**（ID-8）作为极端基线——完全移除视觉感知模块，仅以自车状态为输入，通过 MLP 直接预测轨迹。

**输入输出流与模块关系**

- **输入**：多视图图像（可选） + 自车状态（可选） + 历史 BEV 特征。
- **输出**：未来 3 秒的预测轨迹点序列。
- **模块关系**：BEV 编码器与规划器之间通过 ego query 交叉注意力连接，形成端到端的可微分通路。自车状态可在 BEV 编码阶段或规划阶段注入，这两种注入方式对最终性能的影响是本文消融实验的核心关注点。

值得注意的是，BEV-Planner 系列**不需要任何人工标注数据**（如 3D 检测框、跟踪 ID、高精地图），仅依赖自车轨迹的真值进行监督，这使其成为检验感知信息是否真正贡献于规划的“最小可行基线”。



### 3.1 BEV-Planner 整体架构

BEV-Planner 是一个极简的分析性基线，其设计目标是剥离感知与预测模块，直接检验 BEV 特征对规划的贡献。流水线仅包含三个核心模块：

1. **BEV 特征生成与历史融合**：使用 R50 骨干网络提取多视图图像特征并生成 BEV 特征，随后将过去 4 帧的历史 BEV 特征沿通道维度直接拼接（无显式对齐），形成融合后的 BEV 特征 $B$。
2. **Ego Query 交叉注意力**：通过一个可学习的 ego query $Q$ 与融合后的 BEV 特征 $B$ 进行交叉注意力操作，聚合全局空间上下文。
3. **MLP 轨迹预测头**：将精化后的 ego query 通过 MLP 直接回归未来轨迹点。

整个模型仅使用 L1 损失对轨迹进行监督，不依赖任何人工标注数据（如边界框、跟踪 ID、高精地图等）。

### 3.2 核心公式

BEV-Planner 的轨迹预测过程可形式化为：

$$\tau = \mathbf{MLP}(\mathbf{attn}(q=Q, k=B, v=B))$$

其中：
- $Q$ 为可学习的 ego query 嵌入向量，作为交叉注意力的查询（query）；
- $B$ 为融合了历史帧的 BEV 特征，同时作为键（key）和值（value）；
- $\mathbf{attn}(\cdot)$ 表示交叉注意力操作，将 ego query 与 BEV 特征进行交互，输出精化后的查询表示；
- $\mathbf{MLP}(\cdot)$ 为多层感知机，将精化后的查询映射为未来轨迹 $\tau$。

### 3.3 自车状态引入方式

本文系统性地考察了自车状态在模型中的两种注入位置：

- **BEV 编码器注入**：在 BEV 特征生成阶段引入自车状态（如速度、加速度、偏航角、驾驶指令）。以 UniAD 官方实现（**UniAD**，Hu et al., CVPR 2023）为例，其 BEV 模块通过 BEVFormer 初始化查询时隐式使用了自车状态信息，但许多后续工作未在消融中明确讨论这一细节。
- **规划器注入**：在规划阶段将自车状态向量与查询特征拼接。例如 VAD 方法在规划器中将自车状态与 query 特征拼接后输入轨迹预测头。BEV-Planner++ 即采用此方式。

### 3.4 度量公式

本文对碰撞率计算进行了修正。原始碰撞率定义为在评估时间窗口内每 0.5 秒评估一次碰撞，取平均值：

$$CR(t) = \frac{\sum_{i=0}^{N} \mathbb{I}_i}{N}, \quad N = t/0.5$$

其中 $\mathbb{I}_i$ 为第 $i$ 个时间步是否发生碰撞的指示函数。此定义可能低估碰撞风险，因为短暂碰撞被平均化。

修正后的碰撞率采用“任意碰撞”定义，即 $t$ 秒内任一时刻发生碰撞即视为碰撞：

$$CR(t) = \left(\sum_{i=0}^{N} \mathbb{I}_i\right) > 0, \quad N = t/0.5$$

此外，本文引入路缘碰撞率（Curb Collision Rate, CCR），用于衡量预测轨迹与道路边界（路缘）的交互率，以揭示传统 L2 距离和碰撞率无法捕捉的偏离道路危险。

### 3.5 BEV-Planner 变体

为分析不同组件对规划的贡献，本文设计了多个 BEV-Planner 变体：

- **BEV-Planner**：基础版本，不在规划器中使用自车状态。
- **BEV-Planner++**：在规划器中引入自车状态，将其与 ego query 特征拼接后输入 MLP 预测头。
- **BEV-Planner+Map**：在 BEV-Planner 基础上引入地图感知任务（主要遵循 UniAD 的设计），向 BEV 特征添加地图分割头，以引入道路边界等信息。



## 实验与关键发现

### 核心发现：自车状态对开环规划的支配性影响

本文通过一系列受控实验揭示了一个关键瓶颈：在当前 nuScenes 开环评测体系下，**自车状态（ego status）对最终规划性能具有压倒性影响，感知信息的贡献几乎可以忽略**。这一发现动摇了现有端到端自动驾驶方法在开环基准上性能比较的有效性。

#### 主结果：简单基线即可匹敌 SOTA

**Table 1** 汇总了各方法在 L2 距离、碰撞率（Collision Rate）和新提出的路缘碰撞率（CCR）上的对比。最引人注目的结果是：


![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2312_03031/figures/004_Table_1.jpg]]
*Table 1: Open-loop planning performance. †: The official implementation of ST-P3 (ID-0) utilized partial erroneous ground truth trajectories, with details provided in the appendix. The official UniAD (ID-2) utilized ego status in its BEV module. It is of particular note that the performance of the officially open-sourced model exceeds the results reported in the original paper [13]. We implemented minor modifications to the official codebases of UniAD and VAD to investigate the variations in results arising from different applications of ego status (ID-1, 3 & 4). A naive strategy (ID-7) of proceeding at the current speed also yields satisfactory results. Without the perception module, Ego-MLP (ID-8)...*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2312_03031/figures/015_Table_1.jpg]]
*Table 1: The smoothness $\sigma _ { w d }$ of predicted trajectories*

- **Ego-MLP**（ID-8）：仅使用自车速度、加速度、偏航角和驾驶指令，完全移除感知模块，在 L2 距离均值（0.35m）和碰撞率均值（0.29%）上与 UniAD（0.66m, 0.62%）和 VAD 等复杂方法持平甚至更优。
- **BEV-Planner++**（ID-12）：在 BEV 编码器和规划器中均引入自车状态后，L2 均值降至 0.35m，碰撞率均值降至 0.34%，显著优于官方 UniAD（ID-2）。
- **GoStraight** 策略（ID-7）：仅按当前速度直行，也能获得可接受的 L2 和碰撞率结果，但在 CCR 上表现极差（频繁与道路边界相交），暴露了传统度量的盲区。

**因果机制**：nuScenes 数据集中 73.9% 的场景为直行（Figure 2），自车状态本身已编码了足够的运动先验来应对这些简单场景。模型学会了利用这一捷径，而非真正理解场景语义。


![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2312_03031/figures/002_Figure_2.jpg]]
*Figure 2: (a) The ego car trajectory heatmap on nuScenes dataset. (b) The majority of the scenes within the nuScenes dataset consist of straightforward driving situations*

#### 鲁棒性分析：感知崩溃不影响规划

**Table 2** 和 **Figure 3**（正文）展示了 VAD-Base 模型对图像腐败和自车状态噪声的敏感性：


![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2312_03031/figures/005_Table_2.jpg]]
*Table 2: The VAD-base model’s robustness to images and ego status. To ascertain the impact of perceptual information and ego status on the ultimate planning performance, we systematically introduced noise into each component separately. We utilize the official VAD-Base checkpoint that uses ego status in its planner module. *: the results of VAD-Base without ego status in its planner. We can observe that introducing corruption to images markedly affects the perception results, especially in the case of using blank images; nonetheless, this does not markedly disrupt the ultimate planning results. In contrast to the minor impact of image corruption on planning, modifications to the ego vehicle’s veloci...*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2312_03031/figures/007_Figure_3.jpg]]
*Figure 3: We exhibit the predicted trajectories of the VAD model (incorporating ego status in its planner) under various image corruptions. All trajectories within a given scene (spanning 20 seconds) are presented in the global coordinate system. Each triangular marker signifies a ground truth trajectory point of the ego vehicle, with different colors representing distinct timesteps. Notably, the model’s predicted trajectory maintains plausibility, even when blank images serve as input. The trajectories within the red boxes, however, are suboptimal, as further elucidated in Appendix. While corruptions were applied to all surround-view images, for the sake of visualization, only the corresponding fron...*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2312_03031/figures/018_Table_2.jpg]]
*Table 2: The integration of ego status within BEVFormer exerts only a marginal effect on the perception performance*

- **图像腐败**（雪、雾、眩光、雨）显著降低感知性能（检测 NDS 和地图 mAP 下降），但对规划结果影响甚微。
- **空白图像输入**：感知完全失效（Det. NDS=0.0, Map mAP=0.0），但 L2 均值仅 0.46m，碰撞率均值仅 0.54%——规划几乎不受影响。
- **自车速度扰动**：将速度设为零，模型预测静止轨迹（L2 6.16m, 碰撞率 7.98%）；设为 100 m/s，则产生完全不合常理的轨迹（L2 208m, 碰撞率 9.38%），如 **Figure 4**（正文）所示。

**结论**：模型对自车状态的依赖远超对视觉感知的依赖。当自车状态被扰动时，规划剧烈恶化；而当视觉输入完全移除时，规划几乎不变。这直接证明了感知信息在现有框架中并未有效贡献于规划决策。

#### 消融实验：自车状态的使用方式

通过在 UniAD、VAD-Base 和 BEV-Planner 上系统性地开关自车状态在 BEV 编码器和规划器中的使用（Table 1, ID-1 至 ID-12），可得出以下因果旋钮效应：

- **在 BEV 编码器中引入自车状态**（如 UniAD official ID-2 vs ID-1）：L2 从 1.03m 降至 0.46m，碰撞率从 0.77% 降至 0.37%，提升幅度巨大。
- **在规划器中引入自车状态**（如 VAD-Base ID-6 vs ID-4, BEV-Planner++ ID-12 vs BEV-Planner ID-10）：同样带来显著的 L2 和碰撞率改善。
- **收敛速度**：引入自车状态后，BEV-Planner++ 极速收敛（Figure 5 正文），进一步说明模型主要拟合的是自车状态与轨迹之间的简单映射。

#### 地图感知的悖论：改善 CCR 但牺牲 L2 和碰撞率

**Table 3**（正文）展示了向 BEV-Planner 添加地图感知任务（BEV-Planner+Map）后的效果：


![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2312_03031/figures/019_Table_3.jpg]]
*Table 3: Omitting camera inputs in the VAD model, when it does not utilize ego status, results in a marked reduction in performance, as evidenced by the metrics for L2 distance and collision rate*

- L2 均值从 0.55m 恶化至 0.96m，碰撞率从 0.59% 恶化至 0.89%。
- 但 CCR 从 4.26% 显著改善至 2.60%。

按驾驶指令拆分（Table 4, Table 5）进一步揭示：地图信息在直行场景下增加了 L2 误差和碰撞率，但在转弯场景下降低了碰撞率。这表明地图感知确实提供了道路边界信息以减少偏离道路的风险，但同时也干扰了模型对自车状态捷径的利用，导致整体 L2 和碰撞率指标变差。


![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2312_03031/figures/008_Table_4.jpg]]
*Table 4: L2-ST is the L2 distance with going straight driving commands. L2-LR is the L2 distance with turning left/right commands. Table 5. Collision-ST is the collision rate with going straight driving commands. Collision-LR is the collision rate with turning left/right commands*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2312_03031/figures/020_Table_4.jpg]]
*Table 4: CCR-ST is the CCR rate with going straight driving commands. CCR-LR is the CCR rate with turning left/right commands*

#### UniAD 后处理的隐性风险

UniAD 的后处理优化模块旨在通过非线性优化避免与占用网格的碰撞。然而，**Table 6**（附录）显示：

- 后处理确实降低了碰撞率（0.62% → 0.51%）。
- 但 CCR 从 1.72% 急剧上升至 7.83%，意味着优化后的轨迹更频繁地冲出道路边界。

**Figure 3**（附录）展示了典型失败案例：为避开对向车道车辆，UniAD 的优化轨迹冲向了道路边界，实际上制造了另一种事故风险。这说明单一指标的优化可能引发指标间的恶性权衡。

#### BEV 特征可视化：模型真正学到了什么？

**Figure 6**（正文）对比了 BEV-Planner 和 BEV-Planner++ 的 BEV 特征激活范围：

- BEV-Planner（无自车状态）的激活范围更广，覆盖了道路区域。
- BEV-Planner++（有自车状态）的激活范围主要集中于自车附近，甚至经常出现在车辆后方，与驾驶场景的语义无关。

这进一步证实：当自车状态可用时，模型几乎完全依赖它进行规划，BEV 特征提取被边缘化。

### 新度量：路缘碰撞率（CCR）

为弥补传统 L2 距离和碰撞率无法评估轨迹偏离道路风险的缺陷，本文引入了路缘碰撞率（CCR），计算预测轨迹与道路边界相交的频率。实验表明：

- Ego-MLP 和 GoStraight 在 CCR 上显著劣于利用地图感知的方法（UniAD, BEV-Planner+Map），揭示了它们虽然 L2 和碰撞率优秀，但存在严重的安全隐患。
- 当自车速度为零时，CCR 会产生过于乐观的结果（静止轨迹不会碰撞路缘），这是该度量的已知局限。

### 公平性说明

- ST-P3 官方实现使用了部分错误的未来轨迹标签，导致其性能不可与其他方法公平比较（详见附录 A）。
- 官方 UniAD 和 VAD 版本在 BEV 模块中隐式引入了自车状态信息，而许多工作未在规划器中显式讨论此影响，导致消融不一致。
- 现有碰撞率计算常忽略自车的偏航角变化，产生错误碰撞判定；本文采用了改进的碰撞检测方法（附录 Figure 1）以提升公平性。

### 失败模式与局限

- **连续转弯场景**：附录 Figure 6 显示，所有方法在需要连续转弯的场景下均产生次优轨迹，说明当前模型对复杂机动仍缺乏鲁棒性。
- **无自车状态时移除相机**：附录 Table 3 和 Figure 5 显示，当模型不使用自车状态时，移除相机输入导致 L2 和碰撞率急剧恶化，说明此时模型确实需要感知信息，但其规划能力远弱于使用自车状态时。
- **CCR 的零速度奖励问题**：当自车速度为零时，CCR 无法区分安全静止与危险静止，可能奖励不合理的静止策略。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2312_03031/figures/003_Table.jpg]]

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2312_03031/figures/011_Table.jpg]]




## 定位与知识库关联

### 1. 核心因果旋钮：自车状态的引入方式

本文的核心发现是，**自车状态（ego status）是否被引入模型，以及其在 BEV 编码器或规划器中的使用方式，是决定开环规划性能的关键因果旋钮**。这一发现将现有端到端自动驾驶方法置于一个统一的因果框架下审视：

- **BEV 编码器中的隐式注入**：官方 **UniAD**（Hu et al., CVPR 2023）在 BEV 特征生成阶段通过 BEVFormer 的 query 初始化隐式引入了自车状态信息，这一细节被多数后续工作忽略（附录 Figure 4）。当显式关闭此标志后，UniAD 的 L2 距离从 0.66 m 恶化至 1.03 m，碰撞率从 0.62% 升至 0.77%（Table 1, ID-1 vs ID-2）。

- **规划器中的显式拼接**：**VAD-Base** 在其规划器中将自车状态向量与 query 特征拼接，本文遵循相同方法为 BEV-Planner++ 引入自车状态。该操作使 BEV-Planner 的 L2 距离从 0.55 m 降至 0.35 m（Table 1, ID-10 vs ID-12）。

- **完全无感知的极限**：**Ego-MLP** 仅使用自车速度、加速度、偏航角和驾驶指令，完全不使用任何相机输入或感知模块，却在 L2 距离（0.35 m）和碰撞率（0.29%）上与 UniAD、VAD 等复杂方法持平甚至更优（Table 1, ID-8）。

这一因果链表明，在 nuScenes 开环设定下，**感知信息的贡献被自车状态捷径严重稀释**。

### 2. 与现有方法的谱系关系

本文的方法谱系可沿“感知-规划耦合度”和“自车状态依赖度”两个维度展开：

| 方法 | 感知模块 | 自车状态使用 | 核心特征 |
|------|---------|-------------|---------|
| **ST-P3**（官方实现） | 有 | 未知（存在标签泄漏） | 时空特征学习，但官方实现使用了部分未来轨迹真值，不可公平比较 |
| **UniAD**（Hu et al., CVPR 2023） | 检测/跟踪/建图/预测/规划 | BEV 编码器中隐式注入 | 多任务联合优化，含后处理碰撞优化 |
| **VAD-Base** | 矢量化场景表示 | 规划器中显式拼接 | 基于向量化的高效端到端框架 |
| **BEV-Planner**（本文） | 无（仅 BEV 特征） | 不使用 | 极简基线，仅用交叉注意力和 MLP |
| **BEV-Planner++**（本文） | 无（仅 BEV 特征） | 规划器中显式拼接 | 引入自车状态后性能跃升 |
| **Ego-MLP**（本文） | 无 | 仅使用自车状态 | 无任何视觉输入，性能与 SOTA 持平 |
| **GoStraight**（本文） | 无 | 仅当前速度 | 按当前速度直行的朴素策略 |

**关键定位**：BEV-Planner 系列并非旨在提出新的 SOTA 方法，而是作为**分析性基线**，用于揭示现有基准和度量的系统性缺陷。其极简设计（无检测、跟踪、建图标注，仅使用 L1 轨迹损失）使得因果分析成为可能。

### 3. 适用边界与局限

#### 3.1 数据集分布偏差

nuScenes 数据集中 **73.9% 的场景为直行**（Figure 2），自车状态（速度、加速度、偏航角）足以应对大部分情况。这一分布偏差是自车状态捷径得以存在的根本原因。在需要连续转弯的复杂场景中，所有方法均产生次优轨迹（附录 Figure 6）。

#### 3.2 度量体系缺陷

- **L2 距离与碰撞率**：无法捕捉偏离道路边界的危险。GoStraight 策略在 L2 和碰撞率上表现尚可，但频繁与路缘相交（Table 1）。
- **路缘碰撞率（CCR）**：本文提出的新度量揭示了 UniAD 后处理的副作用——碰撞率从 0.62% 降至 0.51%，但 CCR 从 1.72% 飙升至 7.83%（Table 6，附录）。CCR 本身也存在局限：当自车速度为零时，静止轨迹不会与路缘相交，可能奖励“不动”策略。
- **轨迹平滑度**（$σ_{wd}$）：附录 Table 1 表明该度量并不比 L2 距离提供更多额外信息。

#### 3.3 开环设定的根本局限

当前所有分析均局限于 nuScenes 的**开环评测**，无法反映闭环交互下的真实驾驶能力。在开环设定下，模型无需应对自身决策对环境的影响，自车状态捷径的风险被掩盖。**本文明确声明 BEV-Planner 系列不适合直接部署**，缺乏可解释性与安全约束。

### 4. 开放问题

1. **综合性规划度量设计**：如何设计一个既惩罚偏离道路（如 CCR），又能合理奖励安全轨迹，同时避免奖励静止策略的度量体系？

2. **消除自车状态捷径**：能否通过数据集重构（如移除自车状态信息、增加挑战性场景）或模型架构约束，迫使模型真正利用感知信息进行规划？

3. **数据集均衡性**：能否构建一个包含更多连续转弯、复杂交互、边缘场景的数据集来取代或补充 nuScenes，从而更公平地评估端到端驾驶模型？

4. **闭环安全性验证**：在闭环仿真或真实场景中，自车状态的过度依赖是否会直接导致安全事故？如何设计鲁棒的评测基准来捕捉这种风险？

5. **感知贡献的公平比较**：由于数据集分布和度量缺陷，目前尚不能完全消除自车状态的影响并公平比较各方法的感知贡献。如何设计实验协议来隔离感知模块的真实效用？

### 5. 方法定位总结

本文的方法贡献不在于提出新的 SOTA 模型，而在于**通过构造极简基线和引入新度量，系统性地揭示了当前开环端到端自动驾驶评测的危机**：现有基准下的“高性能”可能主要来自对自车状态的过拟合，而非感知能力的提升。这一发现对后续研究具有警示意义——任何未显式控制自车状态变量的性能声明，都可能是不公平比较的产物。



## 原文 PDF

![[paperPDFs/CVPR_2024/Is_Ego_Status_All_You_Need_for_Open_Loop_End_to_End_Autonomous_Driving.pdf]]
