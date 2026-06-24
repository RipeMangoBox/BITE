---
title: "InterHandGen: Two-Hand Interaction Generation via Cascaded Reverse Diffusion"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/InterHandGen_Two_Hand_Interaction_Generation_via_Cascaded_Reverse_Diffusion.pdf
aliases:
- InterHandGen
tags:
- CVPR_2024
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将联合分布分解为无条件单手分布 p(x_l) 和条件单手分布 p(x_r|x_l)，并利用左右手对称性在共享的 MANO 参数空间中通过条件 dropout 训练单一扩散模型。
primary_logic: 通过分布分解降低单个生成目标的自由度，使扩散模型更容易捕获合理的交互模式；利用手部对称性和多任务学习思想，用一个网络高效建模无条件与条件生成，并通过抗穿透引导和分类器自由引导进一步提升合理性与多样性。
claims:
- 分解建模（Ours）在 FHID、KHID、多样性和精确率-召回率上显著优于直接建模联合分布的 BUDDI* 和不分解的变体（Ours w/o Decomposition）。
- 使用单一共享网络（Ours）在大多数指标上明显优于分别训练无条件/条件网络的变体（Ours w/o Shared Network），尤其在召回率和多样性上。
- 抗穿透引导大幅降低穿透体积，同时保持手的近距离比率不显著变化。
- 级联生成（Ours）在 FHID、精确率、多样性上全面优于并行生成（ComMDM）。
---

# InterHandGen: Two-Hand Interaction Generation via Cascaded Reverse Diffusion

> [!tip] 核心洞察
> 通过分布分解降低单个生成目标的自由度，使扩散模型更容易捕获合理的交互模式；利用手部对称性和多任务学习思想，用一个网络高效建模无条件与条件生成，并通过抗穿透引导和分类器自由引导进一步提升合理性与多样性。

| 字段 | 内容 |
|------|------|
| 中文题名 | InterHandGen：通过级联反向扩散生成双手交互 |
| 英文题名 | InterHandGen: Two-Hand Interaction Generation via Cascaded Reverse Diffusion |
| 会议/期刊 | CVPR 2024 |
| Links | [Project](https://jyunlee.github.io/projects/interhandgen) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | InterHandGen |
| Dataset | InterHand2.6M, ARCTIC, HIC |

> [!tip] 效果简介
> - InterHand2.6M (two‑hand synthesis) 上，FHID (↓) 1.00 vs Not directly reported (best baseline see Table 1a) (Significant improvement over baselines)；KHID (↓) 0.15 vs Not directly reported (see Table 1a) (Significant improvement)；Diversity (↑) 3.59 vs 2.68 (Parallel ComMDM) (+0.91)。
> - ARCTIC (object‑conditioned two‑hand synthesis) 上，FHID (↓) 12.91 vs Not directly reported (see Table 1b) (Significant improvement over baselines)。
> - InterHand2.6M (monocular reconstruction) 上，MPVPE (mm) ↓ 12.10 vs Not directly reported (see Table 2a) (New state‑of‑the‑art)。

## 概述

### 问题与瓶颈

生成逼真且多样的双手交互是 3D 人体建模中的一项关键挑战。双手交互的联合分布具有极高的组合复杂度：每只手包含姿态、形状、根旋转和根平移等高自由度参数，而双手之间的接触、遮挡与协调关系进一步放大了学习难度。直接建模联合分布
$p(\mathbf{x}_l, \mathbf{x}_r)$ 的方法往往面临生成质量不佳或模式崩溃的问题。

### 核心思路

InterHandGen 提出一种**级联反向扩散**框架，将双手交互的联合分布分解为两个更易学习的子问题：

$$
p_{\phi}(\mathbf{x}_l, \mathbf{x}_r) = p_{\phi}(\mathbf{x}_l) \; p_{\phi}(\mathbf{x}_r \mid \mathbf{x}_l)
$$

即先无条件地生成一只锚点手（左手），再以该手为条件生成与之交互的另一只手（右手）。这一分解显著降低了单次生成目标的自由度，使扩散模型更容易捕获合理的交互模式。

为高效实现这一分解，InterHandGen 利用左右手的镜像对称性，将左手样本通过镜像变换映射到右手 MANO 参数空间，从而统一训练域；同时引入**条件 dropout** 机制，仅用**单个扩散网络**同时参数化无条件分布 $p_{\phi}(\mathbf{x}_l)$ 和条件分布 $p_{\phi}(\mathbf{x}_r \mid \mathbf{x}_l)$。在推理阶段，通过**分类器自由引导**平衡生成保真度与多样性，并施加**抗穿透梯度引导**在反向扩散的每一步中最小化双手之间的穿透体积。

### 方法定位

InterHandGen 属于**基于扩散模型的分解式生成方法**。与直接建模联合分布的 BUDDI\* 等基线不同，它通过分布分解将高维组合生成问题转化为两个级联的低维条件生成步骤。与并行生成方法（如 ComMDM）相比，级联策略使条件手能够观察到已去噪的洁净锚点手，从而获得更准确的交互约束。该方法还展示了作为**扩散先验正则化项**在下游任务中的通用性——将冻结的扩散模型作为判别器，约束单目双手重建的输出位于合理交互流形上。

### 主要结果

在 InterHand2.6M 和 ARCTIC 数据集上，InterHandGen 在双手交互生成任务中显著优于现有基线：

- **生成质量**：在 FHID、KHID 等逼真度指标上全面超越 BUDDI\* 和不分解的消融变体（Table 1a）。
- **多样性与精确率**：相比并行生成方法 ComMDM，多样性从 2.68 提升至 3.59，精确率从 0.75 提升至 0.86（Table S1）。
- **物理合理性**：抗穿透引导将穿透体积从 4.23 cm³ 大幅降至 0.76 cm³，同时保持手部近距离比率基本不变（Table 3b）。
- **下游任务**：作为扩散先验正则化项应用于单目双手重建，在 InterHand2.6M 上达到 12.10 mm MPVPE，在 HIC 上达到 15.04 mm MPVPE，均创下新的最优结果（Table 2a, 2b）。

消融实验进一步验证了各设计选择的必要性：移除分布分解或共享网络均导致生成质量显著下降；去除自注意力或分类器自由引导分别损害保真度和多样性；联合训练多数据集的通用先验可将多样性从 3.59 进一步提升至 4.39，但逼真度指标未同步改善，提示现有数据集仅捕获了真实分布的子集（Figure S1）。

## 背景与动机

### 问题背景：双手交互生成的组合复杂性

生成自然、物理合理的双手交互是计算机视觉与图形学中的核心挑战之一。双手交互涉及高维的关节运动自由度——每只手通常由数十个姿态参数、形状参数和全局变换参数共同描述（例如基于 MANO 模型的 64 维表示 $\mathbf{x}_s = [\theta_s, \beta_s, \omega_s, \tau_s]$），而双手联合空间的高维度和交互模式的多样性使得直接建模其联合分布 $p(\mathbf{x}_l, \mathbf{x}_r)$ 面临极高的组合复杂性。这种复杂性在扩散生成框架中表现为学习困难：网络需要同时捕获双手各自的合理姿态以及双手之间微妙的空间关系（如接触、交叉、协同运动），导致生成质量不佳或出现模式崩溃。

### 现有方法缺口：直接联合建模的困境

现有双手生成方法通常采用直接建模联合分布的策略。例如，**BUDDI\*** 使用 Transformer 扩散模型直接对双手的联合参数分布进行建模，而基于 VAE 的方法（如 **Zuo et al., ICCV 2023**）则将双手编码到统一的潜在空间中进行生成。这些方法的共同局限在于：将双手视为一个整体进行生成，忽略了左右手之间天然存在的条件依赖关系与对称性，迫使模型在极高维空间中同时解决手部姿态合理性与交互合理性的双重问题。实验证据表明，这种直接联合建模的方式在保真度指标（FHID、KHID）和多样性指标上均显著劣于分解建模策略（Table 1a）。

此外，现有方法普遍缺乏对双手穿透问题的显式处理。在生成过程中，左右手模型容易出现相互穿透的物理不合理现象，而仅依赖训练数据中的隐式约束难以有效避免这一问题。

### 本文动机：分解建模与级联生成

针对上述困境，本文提出 **InterHandGen**，其核心动机源于一个关键洞察：**双手交互的联合分布可以自然地分解为无条件单手分布与条件单手分布的乘积**：

$$p_{\phi}(\mathbf{x}_l, \mathbf{x}_r) = p_{\phi}(\mathbf{x}_l) \, p_{\phi}(\mathbf{x}_r | \mathbf{x}_l)$$

这一分解将高维联合生成问题转化为两个更低维度的子问题——先生成一只“锚点”手（左手），再以该手为条件生成与之交互的右手。通过降低每个生成目标的自由度，扩散模型能够更容易地捕获合理的交互模式。同时，左右手在解剖结构上的对称性使得可以通过镜像变换将左手样本映射到右手参数空间，从而统一训练域并增广数据，进一步简化学习过程。

在此基础上，InterHandGen 引入三个关键机制以提升生成质量：(1) 通过**条件 dropout** 使用单一共享网络同时参数化无条件分布与条件分布，实现高效的多任务学习；(2) 在反向扩散的每一步施加**抗穿透梯度引导**，显式最小化穿透顶点对之间的距离；(3) 融合**分类器自由引导（CFG）** 以平衡生成保真度与多样性。这些设计共同构成了一个从分布分解出发、以级联反向扩散为核心的双手交互生成框架。

## 核心创新

InterHandGen 的核心创新在于将双手交互生成的高维联合分布建模问题，**分解为两个低维子问题**：无条件左手分布 $p_\phi(\mathbf{x}_l)$ 与以左手为条件的右手分布 $p_\phi(\mathbf{x}_r|\mathbf{x}_l)$。这一分解直接回应了本领域的核心瓶颈——直接建模 $p(\mathbf{x}_l, \mathbf{x}_r)$ 面临极高的组合复杂度和学习困难，容易导致生成质量低下或模式崩溃。通过将自由度从双手联合空间降至单手空间，扩散模型得以更稳定地捕获合理的交互模式。

围绕这一核心分解，InterHandGen 引入了三个紧密耦合的技术槽位（changed slots），构成完整的方法创新链：

**1. 分布建模方式：从联合分布到级联分解（Equation 6）**

基线方法（如 **BUDDI***）直接建模双手联合分布 $p(\mathbf{x}_l, \mathbf{x}_r)$，而 InterHandGen 将其因子化为 $p_\phi(\mathbf{x}_l, \mathbf{x}_r) = p_\phi(\mathbf{x}_l) p_\phi(\mathbf{x}_r|\mathbf{x}_l)$。推理时采用级联采样：先从纯噪声无条件生成锚点左手，再以该左手为条件生成与之交互的右手。消融实验（Table 1a）表明，移除分解的变体（Ours w/o Decomposition）在 FHID、KHID 和多样性上均大幅劣化，证实分解是高质量生成的关键前提。与并行生成方法 **ComMDM**（Shafir et al., ICCV 2023）的对比（Table S1）进一步显示，级联生成在 FHID、精确率（0.86 vs. 0.75）和多样性（3.59 vs. 2.68）上全面占优。

**2. 手部侧空间统一：镜像变换与共享网络（Section 3.3）**

利用左右手在解剖结构上的对称性，InterHandGen 通过镜像变换矩阵 $\mathbf{T} = \begin{bmatrix} -1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}$ 将左手样本映射到右手 MANO 参数空间，统一训练域并实现数据增广。在此基础上，通过**条件 dropout** 机制，使用单一扩散网络同时参数化无条件分布 $p_\phi(\mathbf{x}_l)$ 和条件分布 $p_\phi(\mathbf{x}_r|\mathbf{x}_l)$——当以概率 $p_\text{uncond}$ 将条件手 $\mathbf{x}_l$ 置为空时，网络即退化为无条件模型。这种“多任务”共享设计不仅减少了参数量，更重要的是让网络在统一特征空间中学习单手先验与双手交互依赖。消融实验（Table 1a）证实，共享网络（Ours）在召回率和多样性上显著优于分别训练两个独立网络的变体（Ours w/o Shared Network），同时保持竞争力的精确率。

**3. 抗穿透策略：测试时梯度引导（Section 3.4, Algorithm 2）**

在反向扩散的每一步，InterHandGen 对估计的去噪样本 $\mathbf{x}_{t-1}$ 施加抗穿透梯度引导：首先通过最近邻搜索和法线投影判定穿透顶点对集合 $\mathcal{P}(\mathbf{x}_{t-1}, \mathbf{x}_l) = \{ (i, j) \mid -\mathbf{n}_j^{\mathrm{T}} \cdot (\mathbf{V}_{t-1}^i - \mathbf{V}_l^j) > 0 \}$，然后最小化这些顶点对之间的欧氏距离 $\mathcal{L}_{pen}$。这一测试时引导机制无需重新训练网络，即可大幅降低双手穿透。Table 3b 显示，抗穿透引导将穿透体积从 4.23 cm³ 降至 0.76 cm³，同时保持手的近距离比率（ProxRatio）基本不变，证明其在提升物理合理性的同时未损害交互紧密度。

此外，InterHandGen 在条件采样中引入**分类器自由引导（CFG）**，混合条件与无条件噪声估计 $\tilde{f}_\phi(\mathbf{z}_t, t, \mathbf{c}) = (1+w) f_\phi(\mathbf{z}_t, t, \mathbf{c}) - w f_\phi(\mathbf{z}_t, t, \emptyset)$，以 $w_\text{cfg}=0.1$ 平衡生成保真度与多样性。消融实验（Table 3a）表明，移除 CFG 会导致精确率显著下降。

**创新总结**：InterHandGen 的方法创新并非孤立技术的堆砌，而是以“分布分解”为轴心，通过镜像统一、共享网络、抗穿透引导和 CFG 形成闭环——降低建模难度的同时，保证了交互的物理合理性与样本多样性。这一设计思想具有较强的可推广性，可为其他多实例交互生成任务提供参考范式。

## 整体框架

InterHandGen 的整体框架围绕一个核心思想构建：**将双手交互的联合分布建模分解为两个更简单的子问题**，并通过级联扩散采样实现高质量生成。整个 pipeline 可分为训练与推理两大阶段，共享同一网络架构。

### 问题形式化

给定一对交互的左右手，每只手 $s \in \{l, r\}$ 用一个 64 维向量参数化：
$$\mathbf{x}_s = [\theta_s, \beta_s, \omega_s, \tau_s]$$
其中 $\theta_s$ 为 MANO 姿态参数，$\beta_s$ 为形状参数，$\omega_s$ 为根旋转，$\tau_s$ 为根平移。双手交互的联合分布被分解为：
$$p_{\phi}(\mathbf{x}_l, \mathbf{x}_r) = p_{\phi}(\mathbf{x}_l) \, p_{\phi}(\mathbf{x}_r \mid \mathbf{x}_l)$$
这一分解将原本高自由度的联合生成问题降维为两个低自由度子问题——无条件左手生成和以左手为条件的右手生成，从而显著降低扩散模型的学习难度。

### 级联采样流程（推理）

推理阶段采用**级联反向扩散**，分两步顺序执行：

1. **锚点左手采样**：从纯噪声出发，通过无条件扩散反向过程生成一只左手 $\mathbf{x}_l$。此步骤不依赖任何手部条件，仅利用扩散模型学到的 $p_{\phi}(\mathbf{x}_l)$。
2. **交互右手采样**：以已生成的左手 $\mathbf{x}_l$ 为条件，通过条件扩散反向过程生成与之交互的右手 $\mathbf{x}_r$。此步骤利用扩散模型学到的 $p_{\phi}(\mathbf{x}_r \mid \mathbf{x}_l)$。

在条件采样过程中，融合了两项关键引导机制：
- **分类器自由引导（CFG）**：混合条件与无条件噪声估计，以平衡生成保真度与多样性，引导权重 $w_{\text{cfg}} = 0.1$。
- **抗穿透引导（APG）**：在每一步反向扩散中，对估计的去噪手参数施加梯度下降，最小化穿透顶点对之间的距离，从而避免双手网格发生物理不合理的穿透。

当存在物体条件时，物体点云通过 PointNet++ 编码器提取特征 $\text{emb}_O$，与手部嵌入一同输入网络，使生成过程受物体几何约束。

### 训练流程

训练阶段的核心挑战在于：**如何用一个网络同时学习无条件分布 $p_{\phi}(\mathbf{x}_l)$ 和条件分布 $p_{\phi}(\mathbf{x}_r \mid \mathbf{x}_l)$**。InterHandGen 采用**条件 dropout** 策略解决这一问题：

- 在训练时，以概率 $p_{\text{uncond}}$ 将条件手 $\mathbf{x}_l$ 替换为空条件 $\emptyset$，使网络既能处理条件输入，也能处理无条件输入。
- 训练损失为预测去噪手参数与真实手参数之间的均方误差：$\nabla_{\phi} \| \mathbf{x}_r - D_{\phi}(\mathbf{x}_t, \mathbf{x}_l, t) \|^2$。

此外，利用左右手的对称性，通过镜像变换矩阵 $\mathbf{T} = \text{diag}(-1, 1, 1)$ 将左手样本映射到右手 MANO 参数空间，统一训练域并实现数据增广。

### 网络架构

推理和训练共享同一网络架构（Figure 2），由以下模块串联组成：

![[assets/figures/papers/paper_list_l1719_InterHandGen_Two_Hand_Interaction_Generation_via_Cascaded_Reverse_Diffus/figures/002_Figure_2.jpg]]
*Figure 2: Our network architecture. We use self-attention between the embeddings of the inputs*

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| 手部嵌入 | 将含噪手参数和条件手参数分别映射到隐空间 | $\mathbf{x}_t$, $\mathbf{x}_l$ | 手部特征向量 |
| 时间嵌入 | 对扩散时间步 $t$ 进行 Sinusoidal 位置编码并通过 MLP | $t$ | 时间特征向量 |
| 物体嵌入（可选） | 通过 PointNet++ 提取物体点云特征 | 物体点云 $O$ | $\text{emb}_O$ |
| Transformer 编码器 | 两层自注意力融合所有嵌入，捕获交互依赖 | 手部、时间、物体特征拼接 | 全局上下文特征 |
| 输出解码器 | 多层全连接网络从全局特征估计去噪手参数 | 全局特征 | $\hat{\mathbf{x}}_r$ |

### 扩散先验正则化（下游任务扩展）

对于单目双手重建等下游任务，InterHandGen 将预训练的扩散模型作为**冻结判别器**，通过单步前向-反向扩散构造正则化损失：
$$\mathcal{L}_{reg} = \| \mathcal{S}(D_{\phi}, \mathbf{x}_l, \mathbf{x}_r) - (\mathbf{x}_l, \mathbf{x}_r) \|_2$$
该损失约束当前双手交互状态与扩散先验认为合理的交互状态一致，从而在优化过程中抑制不合理的双手配置。

### 关键设计决策的证据

消融实验（Table 1a, Table 3）为上述设计提供了强有力支持：
- **分布分解**：移除分解（Ours w/o Decomposition）导致 FHID、KHID 和多样性大幅下降，验证了分解对降低学习难度的核心作用。
- **共享网络**：使用单一共享网络（Ours）在召回率和多样性上明显优于分别训练两个独立网络的变体（Ours w/o Shared Network）。
- **级联 vs. 并行**：级联生成在 FHID、精确率和多样性上全面优于并行生成（ComMDM），证实了顺序建模的优势（Table S1）。
- **抗穿透引导**：移除 APG 使穿透体积从 0.76 cm³ 飙升至 4.23 cm³，而手部近距离比率未显著变化（Table 3b）。

## 核心模块与公式推导

### 核心设计思想：分布分解与级联生成

直接建模双手交互的联合分布 $p(\mathbf{x}_l, \mathbf{x}_r)$ 面临极高的组合自由度——每只手的 MANO 参数空间高达 64 维，双手共 128 维，导致扩散模型难以捕获合理的交互模式，容易出现生成质量下降或模式崩溃。InterHandGen 的核心洞察是将这一高维联合分布分解为两个低维条件分布：

$$p_{\phi}(\mathbf{x}_l, \mathbf{x}_r) = p_{\phi}(\mathbf{x}_l) \; p_{\phi}(\mathbf{x}_r \mid \mathbf{x}_l)$$

其中 $\mathbf{x}_l$ 为左手参数，$\mathbf{x}_r$ 为右手参数。这一分解将生成任务从“同时生成两只手”转化为“先无条件生成锚点左手，再以左手为条件生成交互右手”的级联过程。每步只需建模单只手的分布，自由度减半，使扩散模型能更有效地学习交互约束。

### 手部参数化

每只手由 MANO 模型参数化，表示为 64 维向量：

$$\mathbf{x}_s = [\theta_s, \beta_s, \omega_s, \tau_s]$$

其中 $\theta_s \in \mathbb{R}^{45}$ 为手部姿态参数（15 个关节的轴角表示），$\beta_s \in \mathbb{R}^{10}$ 为形状参数，$\omega_s \in \mathbb{R}^{6}$ 为根旋转（连续 6D 表示），$\tau_s \in \mathbb{R}^{3}$ 为根平移。该参数化完整定义了手部在三维空间中的姿态、形状和全局位置。

### 扩散模型基础

InterHandGen 基于方差保持（Variance-Preserving）扩散框架。前向过程将干净的右手参数 $\mathbf{x}_r$ 逐步加噪：

$$\mathbf{x}_t = \sqrt{\alpha_t} \, \mathbf{x}_r + \sqrt{1 - \alpha_t} \, \epsilon, \quad \epsilon \sim \mathcal{N}(0, \mathbf{I})$$

其中 $\alpha_t$ 为噪声调度参数，$t \in [1, T]$ 为扩散时间步。反向过程从纯噪声 $\mathbf{x}_T \sim \mathcal{N}(0, \mathbf{I})$ 开始，通过训练好的去噪网络 $D_\phi$ 逐步恢复干净样本：

$$p_{\phi}(\mathbf{x}_{0:T}) := p(\mathbf{x}_T) \prod_{t=1}^{T} p_{\phi}(\mathbf{x}_{t-1} \mid \mathbf{x}_t)$$

### 训练策略：条件 Dropout 与镜像增广

**条件 Dropout**（Conditioning Dropout）：为使用单一网络同时建模无条件分布 $p_{\phi}(\mathbf{x}_r)$ 和条件分布 $p_{\phi}(\mathbf{x}_r \mid \mathbf{x}_l)$，训练时以概率 $p_{\text{uncond}}$ 将条件左手 $\mathbf{x}_l$ 替换为空条件 $\emptyset$。这使得网络既能学习无条件生成（用于第一步采样锚点左手），又能学习条件生成（用于第二步生成交互右手）。训练损失为预测干净手参数与真实值的均方误差：

$$\nabla_{\phi} \left\| \mathbf{x}_r - D_{\phi}(\mathbf{x}_t, \mathbf{x}_l, t) \right\|^2$$

**镜像变换与空间统一**：利用左右手的几何对称性，通过镜像矩阵 $\mathbf{T} = \begin{bmatrix} -1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}$ 将左手样本映射到右手 MANO 参数空间，统一训练域。这不仅实现了数据增广，还使网络能共享左右手的结构先验，提升建模效率。

### 推理策略：级联采样与双重引导

**级联采样**：推理分为两步——首先从无条件分布采样锚点左手 $\mathbf{x}_l \sim p_{\phi}(\mathbf{x}_l)$，然后以 $\mathbf{x}_l$ 为条件从条件分布采样交互右手 $\mathbf{x}_r \sim p_{\phi}(\mathbf{x}_r \mid \mathbf{x}_l)$。

**分类器自由引导（CFG）**：在条件采样阶段，通过混合条件与无条件噪声估计来平衡保真度与多样性：

$$\tilde{f}_{\phi}(\mathbf{x}_t, t, \mathbf{c}) = (1 + w) f_{\phi}(\mathbf{x}_t, t, \mathbf{c}) - w \, f_{\phi}(\mathbf{x}_t, t, \emptyset)$$

其中 $w$ 为引导强度（本文取 $w=0.1$），$\mathbf{c} = \mathbf{x}_l$ 为条件左手。较小的 $w$ 值在维持条件约束的同时保留生成多样性。

**抗穿透引导（APG）**：在反向扩散的每一步，对预测的 $\mathbf{x}_{t-1}$ 施加梯度引导以消除双手穿透。首先通过最近邻搜索和法线投影判定穿透顶点对：

$$\mathcal{P}(\mathbf{x}_{t-1}, \mathbf{x}_l) = \left\{ (i, j) \;\middle|\; -\mathbf{n}_j^{\mathrm{T}} \cdot (\mathbf{V}_{t-1}^i - \mathbf{V}_l^j) > 0 \right\}$$

其中 $\mathbf{V}_{t-1}^i$ 为右手顶点，$\mathbf{V}_l^j$ 为左手表面最近顶点，$\mathbf{n}_j$ 为该顶点的外法线。条件 $-\mathbf{n}_j^{\mathrm{T}} \cdot (\mathbf{V}_{t-1}^i - \mathbf{V}_l^j) > 0$ 表示右手顶点位于左手表面内侧。穿透损失定义为所有穿透顶点对的欧氏距离之和：

$$\mathcal{L}_{pen}(\mathbf{x}_{t-1}, \mathbf{x}_l) = \sum_{i,j \in \mathcal{P}(\mathbf{x}_{t-1}, \mathbf{x}_l)} \left\| \mathbf{V}_{t-1}^i - \mathbf{V}_l^j \right\|_2$$

在去噪步中沿 $-\nabla_{\mathbf{x}_{t-1}} \mathcal{L}_{pen}$ 方向调整 $\mathbf{x}_{t-1}$，有效减少穿透体积（表 3b 显示穿透体积从 4.23 cm³ 降至 0.76 cm³），同时保持手部近距离比率基本不变。

### 网络架构

去噪网络 $D_\phi$ 采用 Transformer 编码器架构（Figure 2）。输入包括含噪手参数 $\mathbf{x}_t$、条件左手 $\mathbf{x}_l$、扩散时间步 $t$ 和可选的物体点云嵌入 $\text{emb}_O$。各输入通过独立 MLP 嵌入后，经两层自注意力模块融合交互依赖关系，最终由 MLP 解码器输出去噪后的右手参数。自注意力机制使网络能捕获双手间的全局交互约束，消融实验显示移除自注意力会同时损害保真度（FHID）和多样性（Table 3a）。

### 扩散先验正则化

预训练的扩散模型可作为冻结判别器用于下游任务。给定任意双手交互状态 $(\mathbf{x}_l, \mathbf{x}_r)$，正则化损失定义为单步前向-反向扩散后的重建误差：

$$\mathcal{L}_{reg} = \left\| \mathcal{S}(D_{\phi}, \mathbf{x}_l, \mathbf{x}_r) - (\mathbf{x}_l, \mathbf{x}_r) \right\|_2$$

其中 $\mathcal{S}$ 表示对 $\mathbf{x}_r$ 施加一步加噪后由 $D_\phi$ 去噪的操作。该损失约束双手状态保持在扩散模型学习的合理流形上，在单目双手重建任务中将 MPVPE 降至 12.10 mm（InterHand2.6M）和 15.04 mm（HIC），达到新 state-of-the-art（Table 2）。

## 实验与分析

### 核心实验设置与评估指标

InterHandGen 在两个主要任务上进行评估：**无条件双手交互生成**（InterHand2.6M 数据集）和**物体条件双手交互生成**（ARCTIC 数据集）。评估指标覆盖生成质量、多样性和物理合理性三个维度：

- **FHID / KHID**：基于专门训练的 PointNet++ 特征提取骨干网络（在 InterHand2.6M 上测试 MPJPE 为 1.49 mm）计算的特征空间 Frechet / Kernel Inception Distance，衡量生成分布与真实分布的逼真度。
- **Diversity**：生成样本在特征空间中的平均成对距离，反映生成多样性。
- **Precision / Recall**：基于特征空间最近邻的精确率与召回率，分别衡量生成样本的逼真度和覆盖度。
- **PenVol / PenDist / ProxRatio**：穿透体积、穿透距离和近距离比率，衡量双手交互的物理合理性。

为公平比较，所有基线均进行了针对性增强：将 VAE 基线（Zuo et al., ICCV 2023）的特征维度从 128 增至 256、编码器层数从 4 增至 5；将 BUDDI* 的注意力特征维度从 152 增至 184。物体条件生成中，所有基线均以相同的 PointNet++ 嵌入接收物体条件。

### 双手交互生成主结果

在 InterHand2.6M 上的无条件双手生成实验中（Table 1a），InterHandGen 在 FHID（1.00）和 KHID（0.15）上均取得最优结果，显著超越直接建模联合分布的 BUDDI* 和不分解的消融变体（Ours w/o Decomposition）。这一差距的核心来源是 **分布分解策略**：将高维联合分布 $p(\mathbf{x}_l, \mathbf{x}_r)$ 分解为 $p(\mathbf{x}_l) p(\mathbf{x}_r | \mathbf{x}_l)$ 的级联形式，将单个生成目标的自由度减半，使扩散模型更容易捕获合理的交互模式。

与并行生成方法 **ComMDM**（Shafir et al., ICCV 2023）的对比（Table S1）进一步验证了级联采样的优势：InterHandGen 在 Precision 上从 0.75 提升至 0.86，Diversity 从 2.68 提升至 3.59，同时 FHID 也明显更优。这表明先确定锚点左手、再条件生成右手的顺序策略，比同时生成双手更能保证交互的一致性和多样性。

![[assets/figures/papers/paper_list_l1719_InterHandGen_Two_Hand_Interaction_Generation_via_Cascaded_Reverse_Diffus/figures/013_Table.jpg]]
*Table: S1. Comparisons between the parallel and cascaded generation approaches*

### 物体条件双手生成

在 ARCTIC 数据集上的物体条件双手生成实验中（Table 1b），InterHandGen 的 FHID 达到 12.91，显著优于扩展自单手‑物体交互方法 **ContactGen** 的基线。这证明分布分解策略在引入物体条件时同样有效——物体点云通过 PointNet++ 编码器嵌入后，与手部特征在 Transformer 自注意力模块中融合，模型能够学习物体几何对双手交互的约束关系。

### 消融实验分析

#### 分布分解与共享网络

Table 1a 的消融对比揭示了两个关键设计的作用：

1. **移除分布分解（Ours w/o Decomposition）**：直接建模联合分布的变体在 FHID、KHID 和 Diversity 上均大幅下降。这证实了核心瓶颈——双手关节运动自由度高、交互模式多样，直接学习联合分布面临高组合复杂度和模式崩溃风险，而分解建模有效降低了学习难度。

2. **移除共享网络（Ours w/o Shared Network）**：使用两个独立网络分别训练无条件分布 $p(\mathbf{x}_l)$ 和条件分布 $p(\mathbf{x}_r | \mathbf{x}_l)$ 的变体，在 Recall 和 Diversity 上明显劣于共享网络方案。共享网络通过条件 dropout 同时学习两个分布，利用左右手对称性和多任务学习思想，使条件生成能够受益于无条件分布中学习到的手部先验，从而提升生成覆盖度。

#### 架构组件与采样策略

Table 3a 的消融进一步揭示了架构细节的影响：

- **移除自注意力（Ours w/o SelfAtt）** 同时损害 FHID 和 Diversity，说明 Transformer 自注意力层对于捕获含噪手参数、条件手参数和时间步嵌入之间的交互依赖至关重要。
- **移除分类器自由引导（Ours w/o CFG）** 导致 Precision 显著下降，而 Diversity 上升。CFG 通过混合条件与无条件噪声估计（$w_{cfg}=0.1$）平衡保真度与多样性，防止条件采样过度偏向训练分布的模式而丧失多样性。

#### 抗穿透引导

Table 3b 的穿透指标消融直接量化了抗穿透引导（APG）的效果：

- **移除 APG（Ours w/o APG）** 导致 PenVol 从 0.76 cm³ 飙升至 4.23 cm³，PenDist 也大幅增加，而 ProxRatio 未显著变化。这表明 APG 在反向扩散的每一步通过最小化穿透顶点对距离（Equation 7-8），有效消除了双手网格的相互穿透，同时保持了手的近距离交互比率，实现了物理合理性与交互紧密性的良好平衡。

### 下游任务：单目双手重建

将预训练的 InterHandGen 扩散模型作为冻结先验，通过扩散先验正则化损失 $\mathcal{L}_{reg}$（Equation 9）约束重建网络的双手交互状态，在 InterHand2.6M 和 HIC 两个数据集上均取得了新的最优结果（Table 2）：

![[assets/figures/papers/paper_list_l1719_InterHandGen_Two_Hand_Interaction_Generation_via_Cascaded_Reverse_Diffus/figures/008_Table_2.jpg]]
*Table 2: Quantitative comparisons of interacting two-hand reconstruction from in-the-wild images. Utilizing our generative prior can boost the two-hand reconstruction accuracy*

- InterHand2.6M：MPVPE 12.10 mm，MPJPE 14.53 mm
- HIC：MPVPE 15.04 mm

这验证了所学习的双手交互先验不仅能够生成合理的交互，还能有效正则化下游重建任务，防止产生物理上不合理的双手姿态。

### 失败模式与局限性

尽管整体性能优越，InterHandGen 仍存在以下局限：

1. **通用先验的逼真度瓶颈**：联合训练多数据集（双手 + 单手）的通用先验可将 Diversity 从 3.59 提升至 4.39（Figure S1），但 FHID/KHID 等逼真度指标并未同步改善。这说明现有数据集仅捕获了真实双手交互分布的子集，简单联合训练难以实现协同改进。

![[assets/figures/papers/paper_list_l1719_InterHandGen_Two_Hand_Interaction_Generation_via_Cascaded_Reverse_Diffus/figures/009_Figure.jpg]]
*Figure: (c) False positive samples with respect to the manifold modeled by the prior trained on InterHand2.6M only. Figure S1. Hands sampled by our prior trained on two-hand dataset and additional single-hand datasets [16, 71, 74, 75]*

2. **级联采样速度**：级联生成需要顺序执行两次完整的扩散反向采样（先左手后右手），相比并行方法推理速度较慢。

3. **抗穿透引导的局限性**：APG 仅在测试时通过梯度下降附加，缺乏与其他扩散引导方法（如重建引导、物理约束引导）的深入结合分析，且早期去噪步中引导权重的调度策略未充分优化。

4. **静态生成范围**：当前方法专注于静态双手姿势生成，未涉及时间维度的交互动作序列，无法建模动态的双手协调运动。

5. **物体条件的封闭性**：物体条件生成仍依赖预定义的对象类别，未实现开放世界的任意物体条件生成。

### 补充图表

![[assets/figures/papers/paper_list_l1719_InterHandGen_Two_Hand_Interaction_Generation_via_Cascaded_Reverse_Diffus/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparisons of two-hand interaction synthesis with and without an object. Bold indicates the best scores, and underline indicates the second best scores. In both experiments, ours significantly outperforms the baselines on most of the metrics. We conduct 20 evaluations and report the average scores, where 10K samples are used in two-hand synthesis and 30K samples (3K samples per object category) are used for two-hand-object synthesis in each evaluation*

![[assets/figures/papers/paper_list_l1719_InterHandGen_Two_Hand_Interaction_Generation_via_Cascaded_Reverse_Diffus/figures/006_Table_3.jpg]]
*Table 3: Ablation study results. We use the same setting as in the two-hand interaction generation experiments (Section 4.1)*

![[assets/figures/papers/paper_list_l1719_InterHandGen_Two_Hand_Interaction_Generation_via_Cascaded_Reverse_Diffus/figures/007_Table.jpg]]
*Table: (b) Comparisons on inter-penetration. We compare to our method variation where anti-penetration guidance is not used (Ours w/o APG). PenVol, PenDist, and ProxRatio denote penetration volume, penetration distance, and proximity ratio, respectively*

![[assets/figures/papers/paper_list_l1719_InterHandGen_Two_Hand_Interaction_Generation_via_Cascaded_Reverse_Diffus/figures/001_Figure.jpg]]
*Figure: (a) Generated two-hand interactions*

![[assets/figures/papers/paper_list_l1719_InterHandGen_Two_Hand_Interaction_Generation_via_Cascaded_Reverse_Diffus/figures/005_Figure_4.jpg]]
*Figure 4: Object-conditional two-hand interaction synthesized by InterHandGen. Ours can model plausible and diverse bimanual interactions*

![[assets/figures/papers/paper_list_l1719_InterHandGen_Two_Hand_Interaction_Generation_via_Cascaded_Reverse_Diffus/figures/010_Figure.jpg]]
*Figure: S2. Qualitative results of our monocular two-hand reconstruction experiment in Section 4.3. The top four rows show results from the HIC dataset, while the bottom four rows show results from the InterHand2.6M dataset. Brown boxes highlight areas where shape penetration occurs, and blue boxes denote regions with inaccurate hand interaction (e.g., contact is absent where it should occur). Utilizing our generative prior leads to more plausible reconstructions*

![[assets/figures/papers/paper_list_l1719_InterHandGen_Two_Hand_Interaction_Generation_via_Cascaded_Reverse_Diffus/figures/011_Figure.jpg]]
*Figure: S3. Qualitative results of two-hand interaction synthesis experiment in Section 4.1. Brown boxes denote regions with implausible two-hand interaction (e.g., where penetration or unnatural hand articulation occurs). Our method can produce more plausible two-hand interactions with less penetration*

![[assets/figures/papers/paper_list_l1719_InterHandGen_Two_Hand_Interaction_Generation_via_Cascaded_Reverse_Diffus/figures/012_Figure.jpg]]
*Figure: S4. Qualitative results of two-hand interaction synthesis experiment in Section 4.2. Brown boxes denote implausible regions with penetration or unnatural hand articulation. Our approach can generate more realistic bimanual interactions*

## 方法谱系与知识库定位

### 1. 核心瓶颈与因果机制

双手交互生成的根本挑战在于**高维联合分布的直接建模**。双手各自由 MANO 参数化（姿态、形状、根旋转、根平移共 64 维），联合空间自由度极高，且自然交互模式在数据中稀疏分布。直接学习 $p(\mathbf{x}_l, \mathbf{x}_r)$ 的扩散模型（如 BUDDI*）面临严重的模式崩溃和低质量生成问题——这一瓶颈在消融实验中得到了明确验证：移除分布分解后，FHID、KHID 和多样性指标均大幅恶化（Table 1a, Ours vs. Ours w/o Decomposition）。

InterHandGen 的**因果旋钮**是将联合分布分解为级联条件分布：

$$p_{\phi}(\mathbf{x}_l, \mathbf{x}_r) = p_{\phi}(\mathbf{x}_l) \, p_{\phi}(\mathbf{x}_r \mid \mathbf{x}_l)$$

这一分解将高维联合生成问题转化为两个低维子问题：先无条件采样锚点左手，再以其为条件采样交互右手。核心洞察在于：**降低单个生成目标的自由度，使扩散模型能够更有效地捕获合理的交互模式**。同时，利用左右手的几何对称性，通过镜像变换 $\Gamma$ 将左手样本映射到共享的右手 MANO 参数空间，并借助条件 dropout 使单一网络同时参数化 $p_{\phi}(\mathbf{x}_l)$ 和 $p_{\phi}(\mathbf{x}_r \mid \mathbf{x}_l)$，实现了高效的多任务学习。

### 2. 与基线方法的关系

**直接联合建模基线**

- **BUDDI\***（Transformer 扩散模型，直接建模 $p(\mathbf{x}_l, \mathbf{x}_r)$）：InterHandGen 的分解策略在 FHID、KHID、多样性和精确率-召回率上均显著优于该基线（Table 1a）。BUDDI* 的失败验证了联合空间建模的固有困难。
- **Ours w/o Decomposition**（消融变体，单扩散网络直接生成双手）：性能大幅下降，进一步确认分解的必要性。
- **Parallel ComMDM**（Shafir et al., ICCV 2023）：遵循多实例通信机制的并行生成方案。InterHandGen 的级联生成在 FHID、精确率和多样性上全面优于并行方案（Table S1），表明顺序条件生成比并行通信更适合双手交互的结构化依赖。

**单手建模基线**

- **VAE**（Zuo et al., ICCV 2023）：原为单目双手重建的 VAE 先验，扩展为无条件生成基线。扩散模型在生成质量上显著优于 VAE，这符合扩散模型在高维连续数据上的普遍优势。
- **ContactGen**：原为单手-物体交互的接触先验生成方法，扩展为双手-物体条件生成基线。InterHandGen 在 ARCTIC 数据集上显著优于该基线（Table 1b），表明级联扩散框架在物体条件场景下同样有效。

**共享网络的消融意义**

使用共享网络（Ours）相比分别训练两个独立网络（Ours w/o Shared Network）在召回率和多样性上明显更优（Table 1a）。这表明条件 dropout 机制使网络在无条件与条件生成任务之间形成了有益的参数共享，增强了泛化能力。

### 3. 适用边界

**有效范围**

- 静态双手交互姿势生成，包括无物体和有物体条件（给定物体点云）两种场景。
- 单目双手重建的下游任务，通过扩散先验正则化 $\mathcal{L}_{reg}$ 约束重建结果的交互合理性。
- 基于 MANO 参数化的人手表示，依赖该参数模型的表达能力和拓扑结构。

**边界限制**

1. **时序建模缺失**：当前方法仅生成静态姿势，无法处理连续交互动作序列。级联采样需要两次完整的反向扩散过程，推理速度低于并行方法。
2. **数据分布依赖**：联合训练多数据集（双手 + 单手）虽将多样性从 3.59 提升至 4.39，但 FHID 等逼真度指标未同步改善（Figure S1）。这表明现有数据集仅捕获了真实手部交互分布的子集，简单联合训练无法实现协同提升。
3. **物体条件封闭性**：物体条件生成依赖预定义的对象类别和 PointNet++ 嵌入，未实现开放世界的任意物体条件生成。
4. **抗穿透引导的局限性**：抗穿透引导仅在测试时通过梯度下降施加，缺乏与其他扩散引导方法（如约束优化、物理模拟）的深入结合分析。早期去噪步中引导权重的最优调度策略尚不明确。

### 4. 局限与开放问题

**已确认的局限**

- 通用先验联合训练虽提升多样性，但逼真度未改善——这指向数据层面的根本瓶颈，而非方法设计缺陷。
- 级联生成顺序执行两次扩散采样，推理效率低于并行方案。
- 抗穿透引导为后处理式修正，未嵌入训练过程，可能无法从根本上消除穿透。
- 分解策略依赖左右手的明确语义角色（锚点手 vs. 条件手），在对称交互场景中可能引入不必要的非对称偏置。

**开放问题**

1. **通用手部先验的协同训练**：如何构建训练策略，使联合训练多个异构数据集既能提升多样性又能提高逼真度？可能需要数据增强、域自适应或更精细的分布对齐技术。
2. **时序扩展**：如何将分解建模思想推广到时序域，生成连续、物理一致的双手交互动作序列？这需要处理时序依赖和运动平滑性。
3. **跨任务推广**：该分解建模框架能否应用于其他多实例交互生成任务，如人手-物体、人体-人体交互？核心挑战在于不同实例间的非对称条件依赖建模。
4. **穿透避免的深层机制**：抗穿透引导在早期去噪步中使用较低权重是否最优？是否存在更高效的穿透避免机制（如将穿透约束直接嵌入扩散训练或使用约束优化替代梯度引导）？
5. **扩散先验正则化的泛化**：$\mathcal{L}_{reg}$ 在其他下游任务（如双手跟踪、从视频生成、运动补全）中的适用性和性能表现尚待探索。
6. **开放世界物体条件**：如何突破预定义对象类别的限制，实现基于文本描述或任意物体几何的条件生成？

## 原文 PDF

![[paperPDFs/CVPR_2024/InterHandGen_Two_Hand_Interaction_Generation_via_Cascaded_Reverse_Diffusion.pdf]]
