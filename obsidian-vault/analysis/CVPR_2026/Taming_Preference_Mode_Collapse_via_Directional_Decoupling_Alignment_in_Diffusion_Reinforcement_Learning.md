---
title: Taming Preference Mode Collapse via Directional Decoupling Alignment in Diffusion Reinforcement Learning
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Taming_Preference_Mode_Collapse_via_Directional_Decoupling_Alignment_in_Diffusion_Reinforcement_Learning.pdf
project_link: null
code_link: null
aliases:
- DDADA
- TPMCDDADRL
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在奖励模型的文本嵌入空间中学习一个方向修正向量，在连续空间中系统性调整奖励信号，抵消奖励模型的固有偏差，从而阻止模型向特定模式坍塌。
primary_logic: 通过两阶段框架（阶段1冻结生成器学习方向修正向量，阶段2利用该向量构造引导文本嵌入并计算修正奖励）实现奖励信号的方向性解耦，使优化目标更贴合真实人类偏好，同时保持生成多样性。
claims:
- D2-Align在DivGenBench上取得了最高的多样性分数，有效缓解了PMC。
- D2-Align在训练效率上显著优于基线，在更少步数内达到更高奖励分数。
- 学习的方向向量b_v在多种指标上一致优于手动选择的离散词汇基线。
- HPDv2 (Table 1, HPS-v2.1 reward) 上 ImageReward = 1.771
---

# Taming Preference Mode Collapse via Directional Decoupling Alignment in Diffusion Reinforcement Learning

> [!tip] 核心洞察
> 通过两阶段框架（阶段1冻结生成器学习方向修正向量，阶段2利用该向量构造引导文本嵌入并计算修正奖励）实现奖励信号的方向性解耦，使优化目标更贴合真实人类偏好，同时保持生成多样性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过方向解耦对齐抑制扩散强化学习中的偏好模式坍塌 |
| 英文题名 | Taming Preference Mode Collapse via Directional Decoupling Alignment in Diffusion Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.24146) |
| Topic | #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | Directional Decoupling Alignment (D2-Align) |
| Dataset | HPDv2, DivGenBench, HPDv2 User Study, DivGenBench User Study |

> [!tip] 效果简介
> - HPDv2 (Table 1, HPS-v2.1 reward) 上，ImageReward 1.771 vs 1.703 (Flow-GRPO) (+0.068)；Pick Score 0.246 vs 0.241 (DanceGRPO / SRPO) (+0.005)；CLIP Score 0.323 vs 0.302 (SRPO) (+0.021)。
> - DivGenBench (Table 2, HPS-v2.1 reward) 上，IDS (↓) 0.251 vs 0.259 (SRPO) (-0.008)。
> - HPDv2 User Study (Figure 8) 上，Detail Preservation Preference 61.7% vs 16.5% (SRPO) (+45.2%)。

## 概要

**问题**：当前基于人类反馈强化学习的文本到图像扩散模型对齐方法（如DanceGRPO、Flow-GRPO、SRPO）在最大化预定义奖励信号时，普遍忽视生成多样性，导致模型过拟合奖励模型的固有偏好，收敛到单一高奖励模式（如过度光滑、油亮渲染风格），产生**偏好模式坍塌**。这一问题在身份、风格、布局、影调四个维度上均严重损害生成多样性，形成偏好与多样性之间的尖锐权衡。

**核心方法**：本文提出**方向解耦对齐**——一种两阶段框架，在奖励模型的文本嵌入空间中学习一个连续的方向修正向量，系统性抵消奖励模型的固有偏差，实现奖励信号的方向性解耦。阶段一冻结生成器，仅优化方向向量以最小化引导奖励的负值；阶段二冻结学习到的方向向量，利用修正后的奖励信号引导生成器远离模式坍塌。该方法无需修改模型架构或引入额外正则化项，通过在嵌入空间中连续搜索最优修正方向，使优化目标更贴合真实人类偏好。

**关键发现**：
- **打破权衡**：D2-Align在DivGenBench多样性基准上取得最高分（IDS 0.251，ASC 0.205等），同时在HPDv2人类偏好基准上达到最优ImageReward（1.771）和CLIP Score（0.323），在偏好-多样性平面上占据帕累托前沿位置。
- **训练高效**：相比DanceGRPO和Flow-GRPO需要超过250步才能达到相似性能，D2-Align在更少步数内实现更高奖励分数，训练效率显著提升。
- **人类评估验证**：用户研究中，D2-Align在细节保持（61.7%偏好率）和图文对齐（52.2%）上大幅领先基线；在风格多样性（37.3%）和身份多样性（35.2%）上也获得最高偏好率，而Flow-GRPO在影调多样性上仅获7.7%偏好率，严重坍塌。
- **方向向量的可迁移性**：学习到的方向修正向量可作为即插即用组件嵌入DanceGRPO等现有方法，在人类偏好和多样性指标上均带来一致提升，验证了方法的通用性。



### 扩散强化学习中的偏好模式坍塌

文本到图像扩散模型（如FLUX）在生成高质量图像方面取得了显著进展，但如何使生成结果与人类偏好对齐仍是一个核心挑战。基于强化学习的微调方法（RLHF）通过最大化预定义奖励模型的分数来优化生成器，已成为对齐的主流范式。然而，这一范式暴露了一个关键瓶颈：**奖励模型本身存在固有偏好偏差**，当生成器过度优化该奖励信号时，会收敛到单一的高奖励模式，严重损害生成多样性。

这种现象被称为**偏好模式坍塌（Preference Mode Collapse, PMC）**。具体而言，奖励模型倾向于给某些特定视觉风格（如过度光滑、油亮渲染）分配高分，即使这些风格与用户提示的意图并不匹配（见Figure 3）。当生成器被反复训练以最大化该奖励时，它会“钻空子”地生成奖励模型偏好的单一模式，而忽略提示中要求的多样性——例如，无论提示要求的是“极简主义”还是“油画风格”，模型都输出同质化的油亮图像。

### 现有方法的缺口

现有RL对齐方法在抑制PMC方面存在明显不足：

- **多奖励集成方法**（如**DanceGRPO**）试图通过集成多个奖励模型来避免单一奖励的偏差，但在实践中仍易出现PMC，且训练效率较低（需超过250步才能达到可比性能，见Figure 5）。
- **KL散度正则化方法**（如**Flow-GRPO**）利用KL散度约束防止过优化，但其系数高度敏感，调参困难，且训练开销大。
- **监督奖励策略优化**（**SRPO**）同样难以在保持高奖励分数的同时维持生成多样性。

这些方法的共同缺陷在于：它们在**最大化奖励与保持多样性之间存在根本性权衡**（见Figure 1右上角散点图），要么获得低多样性，要么获得低偏好分数，无法同时达到两者兼优的状态。

### 本文动机与核心思路

本文提出**方向解耦对齐（Directional Decoupling Alignment, D2-Align）**框架，核心洞察在于：与其被动约束生成器不过度优化，不如**主动修正奖励信号本身**，从源头消除奖励模型的固有偏差。

具体而言，D2-Align在奖励模型的文本嵌入空间中学习一个**方向修正向量** $b_v \in \mathbb{R}^d$，通过连续空间中的方向性扰动系统性调整奖励信号，抵消奖励模型对特定模式的偏好。该框架采用两阶段设计：

1. **阶段1（方向修正学习）**：冻结生成器，仅优化方向向量 $b_v$，使其最小化负引导奖励，从而在嵌入空间中学习能抵消奖励偏差的修正方向。
2. **阶段2（引导对齐）**：冻结学习到的 $b_v^*$，利用该向量构造引导文本嵌入并计算修正后的奖励信号，优化生成器使其远离模式坍塌，同时保持高生成质量。

通过这种奖励信号的**方向性解耦**，D2-Align使优化目标更贴合真实人类偏好，打破了偏好与多样性之间的固有权衡，在保持甚至提升人类偏好分数的同时，显著增强了生成多样性。



## 核心方法与创新机理

### 问题瓶颈：偏好模式坍塌（PMC）

现有基于强化学习的人类反馈对齐方法（RLHF）在最大化预定义奖励时，忽视了对生成多样性的保持。由于奖励模型本身存在固有偏好——例如对“油亮渲染风格”或特定色调的过度奖励——生成器在优化过程中会逐步收敛到这些单一的高奖励模式，产生**偏好模式坍塌（Preference Mode Collapse, PMC）**。其直接后果是：模型对不同的提示输入产生高度同质化的输出，在身份、风格、布局、影调等维度上丧失多样性，形成“高奖励但低多样性”的困境。

### 因果调控：奖励信号的方向解耦

D2-Align的核心创新在于**不从生成器优化策略入手约束多样性，而是直接修正奖励信号本身**。其因果调控机制如下：

1. **在奖励模型的文本嵌入空间中学习一个方向修正向量** $b_v \in \mathbb{R}^d$，该向量编码了奖励模型偏差的“反方向”。
2. 利用该向量对原始文本提示嵌入进行双向扰动，构造正向嵌入 $e_+$ 与负向嵌入 $e_-$：
   $$e_+ = \mathrm{normalize}(e_{\mathrm{text}} + b_v), \quad e_- = \mathrm{normalize}(e_{\mathrm{text}} - b_v)$$
3. 通过引导尺度 $\omega > 1$ 从负方向向正方向外推，生成**引导文本嵌入** $\tilde{e}_{\mathrm{text}}$：
   $$\tilde{e}_{\mathrm{text}} = e_- + \omega \cdot (e_+ - e_-)$$
4. 以该引导嵌入替代原始文本嵌入计算修正后的奖励信号：
   $$R_{\mathrm{guided}}(x_0, c; b_v) = \mathrm{score}(e_{\mathrm{img}}, \tilde{e}_{\mathrm{text}})$$

这一设计的本质是**在连续嵌入空间中进行方向性奖励解耦**：通过系统性地偏移奖励模型的文本条件输入，抵消其固有偏差，使优化目标更贴合真实人类偏好，从而阻止生成器向特定模式坍塌。

### 关键结构变更：两阶段解耦框架

D2-Align将奖励修正与生成器优化解耦为两个独立阶段，这是其相对于现有RL对齐方法最重要的结构创新：

| 阶段 | 核心操作 | 优化目标 | 冻结/更新 |
|------|----------|----------|-----------|
| **Stage 1: 方向修正学习** | 学习方向向量 $b_v$ | $\mathcal{L}_{\mathrm{stage1}}(b_v) = \mathbb{E}[-R_{\mathrm{guided}}]$ | 冻结生成器 $G_\theta$，仅优化 $b_v$ |
| **Stage 2: 引导对齐** | 利用冻结的 $b_v^*$ 优化生成器 | $\mathcal{L}_{\mathrm{stage2}}(\theta) = \mathbb{E}[-R_{\mathrm{guided}}(x_0, c; b_v^*)]$ | 冻结 $b_v^*$，仅优化 $G_\theta$ |

与现有方法的关键差异：

- **DanceGRPO** 通过集成多个奖励模型来避免单一奖励偏差，但集成本身无法消除各模型共有的系统性偏差，仍会出现PMC。
- **Flow-GRPO** 利用KL散度正则化防止过优化，但正则化系数高度敏感，且额外的前向/反向传播显著增加了训练开销。
- **SRPO** 基于监督奖励策略优化，同样缺乏对奖励信号偏差的显式建模。

D2-Align的**changed slot**在于将奖励信号计算从原始的余弦相似度：
$$R(x_0, c) = \mathrm{score}(\Phi_{\mathrm{img}}(x_0), \Phi_{\mathrm{text}}(c))$$
替换为方向引导的修正奖励：
$$R_{\mathrm{guided}}(x_0, c; b_v^*) = \mathrm{score}(e_{\mathrm{img}}, \tilde{e}_{\mathrm{text}})$$

### 创新有效性证据

1. **方向向量的学习优于离散词汇基线**：消融实验（Figure 7右）表明，学习到的方向向量 $b_v$ 在所有评估指标上一致优于手动选择离散词汇（如“realistic”）的基线方法，且全面优于未修正的奖励信号。这验证了连续空间方向修正相较于离散提示工程的本质优势。

2. **训练效率显著提升**：D2-Align在更少的训练步数内达到更高的奖励分数（Figure 5），而DanceGRPO和Flow-GRPO需要超过250步才能达到相近性能。这表明奖励信号修正使优化路径更加直接高效。

3. **方向向量收敛迅速且稳定**：$b_v$ 在约2000步训练后其修正效果即变得显著且鲁棒，此后模型性能大幅提升（Figure 7左），验证了两阶段解耦设计的收敛特性。

4. **通用可迁移性**：将学习到的 $b_v$ 嵌入DanceGRPO框架后，其在人类偏好与多样性指标上均获得提升（Table 6, Table 7），表明方向修正向量可作为即插即用的模块迁移至其他RL对齐方法。



D2-Align 采用**两阶段解耦框架**，核心思想是在奖励模型的连续文本嵌入空间中学习一个方向修正向量 $\mathbf{b}_v \in \mathbb{R}^d$，通过系统性调整奖励信号来抵消奖励模型的固有偏差，从而在不牺牲生成质量的前提下保持生成多样性。

### 框架总览

整个 pipeline 由三个关键模块串联构成：**一步去噪重建** → **阶段1：方向修正学习** → **阶段2：引导对齐**。

#### 模块一：一步去噪重建

在计算奖励信号之前，需要从扩散模型的噪声隐变量中恢复干净的图像估计。给定时间步 $t$ 的噪声隐变量 $\mathbf{x}_t$ 和预测噪声 $\epsilon_\theta(\mathbf{x}_t, t)$，利用 ground-truth 噪声先验进行一步重建：

$$\hat{\mathbf{x}}_0 = \frac{\mathbf{x}_t - \sigma_t \epsilon_\theta(\mathbf{x}_t, t)}{\alpha_t}$$

该模块为后续奖励计算提供**稳定且可微分的图像输入**，是整个框架的感知基础。

#### 模块二：阶段1 — 方向修正学习

此阶段**冻结生成器参数 $\theta$**，仅优化可学习的方向量 $\mathbf{b}_v$。给定文本提示的嵌入 $\mathbf{e}_{\text{text}}$，通过加减 $\mathbf{b}_v$ 构造正/负扰动嵌入：

$$e_+ = \text{normalize}(\mathbf{e}_{\text{text}} + \mathbf{b}_v), \quad e_- = \text{normalize}(\mathbf{e}_{\text{text}} - \mathbf{b}_v)$$

然后从负方向向正方向外推，得到引导文本嵌入：

$$\tilde{\mathbf{e}}_{\text{text}} = e_- + \omega \cdot (e_+ - e_-)$$

其中 $\omega > 1$ 为引导尺度。利用该嵌入计算**引导奖励**：

$$R_{\text{guided}}(\mathbf{x}_0, c; \mathbf{b}_v) = \text{score}(\mathbf{e}_{\text{img}}, \tilde{\mathbf{e}}_{\text{text}})$$

阶段1通过最小化负引导奖励 $\mathcal{L}_{\text{stage1}}(\mathbf{b}_v) = \mathbb{E}[-R_{\text{guided}}]$ 来学习能抵消奖励偏差的修正方向 $\mathbf{b}_v^*$。其核心机制在于：奖励模型对某些模式（如“油亮”、“过度渲染”）存在系统性高估，而 $\mathbf{b}_v$ 在嵌入空间中向相反方向修正文本表征，使修正后的奖励信号更贴合真实人类偏好（参见 Figure 3）。

#### 模块三：阶段2 — 引导对齐

此阶段**冻结已学到的方向向量 $\mathbf{b}_v^*$**，优化生成器参数 $\theta$：

$$\mathcal{L}_{\text{stage2}}(\theta) = \mathbb{E}_{c \sim \mathcal{D}, \mathbf{x}_0 \sim G_\theta(c)} [-R_{\text{guided}}(\mathbf{x}_0, c; \mathbf{b}_v^*)]$$

利用修正后的奖励信号引导生成器远离模式坍塌区域。与直接优化原始奖励 $R(\mathbf{x}_0, c)$ 不同，$R_{\text{guided}}$ 通过方向性解耦抑制了奖励模型对特定模式的过度偏好，使得优化路径指向一个**同时兼顾质量与多样性的更优解**（Figure 2 右图示意了该机制）。

![[assets/figures/papers/paper_list_l2705_https_arxiv_org_abs_2512_24146/figures/002_Figure_2.jpg]]
*Figure 2: Overview of*

### 关键设计决策

1. **连续嵌入空间中的方向学习 vs. 离散词汇扰动**：消融实验（Figure 7 右）表明，学习到的连续向量 $\mathbf{b}_v$ 在所有评估指标上一致优于手动选择的离散词汇（如“realistic”），且全面优于未修正的奖励信号。连续空间的优化使修正方向更精准地捕捉奖励偏差的几何结构。

2. **两阶段解耦的必要性**：若将方向学习与生成器优化耦合进行，奖励信号在训练过程中持续变化，会导致优化目标漂移。冻结生成器先学习稳定的修正方向，再用于引导对齐，保证了训练的信号一致性。

3. **引导尺度 $\omega$ 的调节作用**：$\omega$ 控制从负方向向正方向的外推程度。实验表明 $\omega = 1.5$ 时在 HPS-v2.1 和 Pickscore 上均达到最优，过小的 $\omega$ 修正不足，过大的 $\omega$ 则可能过度扭曲奖励信号（Figure 7 中）。

### 输入输出流总结

- **输入**：文本提示 $c$，预训练扩散生成器 $G_\theta$（基于 **FLUX.1.Dev**），预训练奖励模型（**HPS-v2.1** 或 HPS-v2.1 + CLIP）。
- **阶段1 输出**：冻结的方向量 $\mathbf{b}_v^*$。
- **阶段2 输出**：优化后的生成器参数 $\theta^*$，在给定提示下生成高保真且多样化的图像。
- **推理**：仅使用阶段2优化后的生成器，无需额外的方向修正计算，推理开销与标准扩散生成一致。

### 补充图表

![[assets/figures/papers/paper_list_l2705_https_arxiv_org_abs_2512_24146/figures/001_Figure_1.jpg]]
*Figure 1: D2-Align breaks the trade-off between human preference and generative diversity, mitigating Preference Mode Collapse (PMC). The top-right plot shows that while baselines struggle with a trade-off—either achieving low diversity or low preference—D2- Align, achieves a state of both higher diversity and higher human preference. The qualitative examples below illustrate this phenomenon. For the same set of varied prompts, baseline methods exhibit severe PMC, generating homogeneous outputs for identity, style, layout, and tone. D2-Align successfully preserves diversity, generating distinct and high-quality images that align with each individual prompt. See Supp. for detail prompts*



### 2.1 问题建模与奖励信号

D²-Align 建立在基于扩散的文本到图像生成框架之上。给定文本提示 $c$，生成器 $G_\theta$ 从随机噪声出发，通过逆向扩散过程生成图像 $\pmb{x}_0$。扩散模型的正向加噪过程定义为：

$$\pmb{x}_t = \alpha_t \pmb{x}_0 + \sigma_t \pmb{\epsilon}, \quad \epsilon \sim \mathcal{N}(0, \mathbf{I})$$

其中 $\alpha_t$ 和 $\sigma_t$ 为噪声调度参数，控制信噪比。模型通过 Flow Matching 损失学习时间依赖的向量场 $\pmb{v}_\theta$：

$$\mathbb{E}_{t,\pmb{x}_0,\epsilon} \left[ w(t) \| \pmb{v}_\theta(\alpha_t \pmb{x}_0 + \sigma_t \epsilon, t) - (\dot{\alpha}_t \pmb{x}_0 + \dot{\sigma}_t \epsilon) \|_2^2 \right]$$

生成过程由概率流 ODE 控制：$\frac{\mathrm{d}\pmb{x}_t}{\mathrm{d}t} = \pmb{v}_\theta(\pmb{x}_t, t)$。

**核心瓶颈**在于，现有 RL 对齐方法直接使用预训练奖励模型（如 HPS-v2.1）计算奖励信号：

$$R(\pmb{x}_0, c) = \mathrm{score}(\Phi_{\mathrm{img}}(\pmb{x}_0), \Phi_{\mathrm{text}}(c))$$

该奖励本质上是图像嵌入 $\Phi_{\mathrm{img}}(\pmb{x}_0)$ 与文本嵌入 $\Phi_{\mathrm{text}}(c)$ 的余弦相似度。然而，奖励模型本身存在固有偏差——它倾向于给某些特定视觉模式（如过度光滑、油亮风格）分配高分，即使这些模式与提示语义不匹配。当生成器被反复优化以最大化该奖励时，会收敛到这些高奖励但单一的模式，导致**偏好模式坍塌（PMC）**，严重损害生成多样性。

### 2.2 一步去噪重建模块

为在扩散生成过程中高效计算奖励，D²-Align 引入一步去噪重建模块。给定当前噪声隐变量 $\pmb{x}_t$ 和预测噪声 $\pmb{\epsilon}_\theta(\pmb{x}_t, t)$，利用已知的噪声先验直接重建干净的图像估计：

$$\hat{\pmb{x}}_0 = \frac{\pmb{x}_t - \sigma_t \pmb{\epsilon}_\theta(\pmb{x}_t, t)}{\alpha_t}$$

该模块的关键作用在于：为奖励模型提供高保真且可微分的干净图像估计，避免了在完整逆向链上采样带来的计算开销，使端到端优化成为可能。

### 2.3 方向修正学习模块（Stage 1）

D²-Align 的核心创新在于**方向解耦**策略。在阶段一中，生成器 $G_\theta$ 被冻结，引入一个可学习的方向向量 $\pmb{b}_v \in \mathbb{R}^d$，该向量位于奖励模型的文本嵌入空间中。通过在该连续空间中进行搜索，学习一个能够抵消奖励模型固有偏差的修正方向。

具体而言，对原始文本嵌入 $\pmb{e}_{\mathrm{text}} = \Phi_{\mathrm{text}}(c)$ 施加正负两个方向的扰动：

$$\pmb{e}_+ = \mathrm{normalize}(\pmb{e}_{\mathrm{text}} + \pmb{b}_v)$$

$$\pmb{e}_- = \mathrm{normalize}(\pmb{e}_{\mathrm{text}} - \pmb{b}_v)$$

随后，通过引导尺度 $\omega > 1$ 从负方向向正方向外推，构造引导文本嵌入：

$$\tilde{\pmb{e}}_{\mathrm{text}} = \pmb{e}_- + \omega \cdot (\pmb{e}_+ - \pmb{e}_-)$$

该外推机制类似于分类器自由引导的思想：通过放大正负方向之间的差异，强化修正信号。基于引导文本嵌入计算修正后的奖励：

$$R_{\mathrm{guided}}(\pmb{x}_0, c; \pmb{b}_v) = \mathrm{score}(\pmb{e}_{\mathrm{img}}, \tilde{\pmb{e}}_{\mathrm{text}})$$

阶段一的优化目标是最小化负引导奖励，使 $\pmb{b}_v$ 学习到能够系统性抑制奖励偏差的方向。消融实验证实，$\pmb{b}_v$ 经过约 2000 步训练后修正效果显著且稳定，此后模型性能大幅提升（Figure 7 左）。

### 2.4 引导对齐模块（Stage 2）

在阶段二中，冻结学习到的方向向量 $\pmb{b}_v^*$，仅优化生成器参数 $\theta$。优化目标为最小化负引导奖励：

$$\mathcal{L}_{\mathrm{stage2}}(\theta) = \mathbb{E}_{c \sim \mathcal{D}, \pmb{x}_0 \sim G_\theta(c)} [-R_{\mathrm{guided}}(\pmb{x}_0, c; \pmb{b}_v^*)]$$

此时，修正后的奖励信号引导生成器远离奖励模型偏好的单一模式，在保持高奖励的同时维持生成多样性。Figure 2（右）直观展示了这一效果：基线方法收敛到狭窄的高奖励峰值（低多样性），而 D²-Align 找到了兼顾质量与多样性的更优解。

### 2.5 关键超参数：引导尺度 $\omega$

引导尺度 $\omega$ 控制修正信号的强度。消融实验（Figure 7 中）表明，$\omega = 1.5$ 时达到最优性能，在 HPS-v2.1 和 PickScore 上均取得最佳结果。过小的 $\omega$ 不足以抵消奖励偏差，而过大的 $\omega$ 可能导致过度修正，损害生成质量。

### 2.6 与手动离散词汇基线的对比

一个自然的问题是：能否通过手动选择离散词汇（如 “realistic”）来替代学习连续方向向量？D²-Align 的消融实验（Figure 7 右）明确回答了这一问题：学习到的方向向量 $\pmb{b}_v$ 在所有评估指标上一致优于手动选择的离散词汇基线，且全面优于未修正的原始奖励信号。这验证了在连续嵌入空间中学习修正方向的必要性——离散词汇的语义空间过于粗糙，无法精确抵消奖励模型的细微偏差。

### 补充图表

![[assets/figures/papers/paper_list_l2705_https_arxiv_org_abs_2512_24146/figures/003_Figure_3.jpg]]
*Figure 3: Correcting the Reward Signal via Prompt Perturbation. An image generated for a minimalism prompt is instead oily and overly-rendered. This style mismatch is identified by a human (low score), but the reward model assigns a high score due to its intrinsic bias. We counteract this by perturbing the prompt with descriptors like ”Realistic” to produce a more accurate reward signal aligned with human preference*



## 实验与关键发现

### 主实验结果：人类偏好对齐与语义一致性

D2-Align 在人类偏好对齐、语义一致性和准确性三个维度上均表现出显著优势。Table 1 报告了在 HPDv2 基准上以 HPS-v2.1 和 HPS-v2.1+CLIP 两种奖励配置下的综合定量评估结果。

![[assets/figures/papers/paper_list_l2705_https_arxiv_org_abs_2512_24146/figures/007_Table_1.jpg]]
*Table 1: Comprehensive Quantitative Evaluation. We compare FLUX and advanced methods from the combined perspectives of human preference alignmen, semantic consistency and accuracy, showcasing performance under two distinct reward configurations: HPS-v2.1 and HPS-v2.1 + CLIP. Ranking is performed independently for each reward configuration among the RL-based methods. The highest score is shown in bold, and the second-highest score is underlined*

在 HPS-v2.1 单一奖励配置下，D2-Align 在 ImageReward 指标上达到 **1.771**，超出最强基线 Flow-GRPO（1.703）约 0.068 分；在 Pick Score 上达到 0.246，与 DanceGRPO 和 SRPO（均为 0.241）相比提升 0.005；CLIP Score 达到 0.323，较 SRPO（0.302）提升 0.021。这一结果的关键驱动在于：D2-Align 通过方向向量 $b_v$ 修正奖励信号，使优化目标更贴合真实人类偏好，而非像基线方法那样过拟合奖励模型的固有偏差。

在 HPS-v2.1+CLIP 双奖励配置下，D2-Align 同样保持了领先地位。值得注意的是，**DanceGRPO** 通过集成多个奖励模型来避免单一奖励偏差，但在该配置下仍出现偏好模式坍塌（PMC），说明简单的奖励集成并不能从根本上解决奖励偏差问题。**Flow-GRPO** 依赖 KL 散度正则化防止过优化，但其系数高度敏感，训练开销大，且最终性能仍不及 D2-Align。

### 主实验结果：生成多样性

Table 2 展示了在 DivGenBench 基准上四种多样性指标的定量评估。D2-Align 在身份多样性（IDS）上取得 **0.251** 的最低分数（越低表示多样性越高），优于 SRPO 的 0.259。在艺术风格覆盖（ASC）、空间分布指数（SDI）和影调方差得分（PVS）上，D2-Align 同样保持领先。

![[assets/figures/papers/paper_list_l2705_https_arxiv_org_abs_2512_24146/figures/009_Table_2.jpg]]
*Table 2: Quantitative Evaluation of Generative Diversity on DivGenBench. We compare the FLUX and other advanced methods, showcasing performance under two distinct reward configurations and four metrics, i.e., Identity Divergence Score (IDS), Artistic Style Coverage (ASC), Spatial Dispersion Index (SDI), and Photographic Variance Score (PVS). Ranking is performed independently for each reward configuration among the RLbased methods. The best score is shown in bold, and the secondbest score is underlined*

这一优势的因果机制在于两阶段框架的解耦设计：阶段1在冻结生成器的条件下学习方向修正向量 $b_v$，该向量在连续嵌入空间中系统性抵消奖励模型对特定风格（如过度光滑、油亮渲染）的固有偏好；阶段2利用修正后的引导奖励 $R_{\mathrm{guided}}$ 优化生成器，使其远离单一高奖励模式，从而在保持高奖励的同时维持生成多样性。

Figure 5 的训练效率对比曲线进一步印证了这一机制的有效性：D2-Align 在更少的训练步数内达到更高的奖励分数，而 DanceGRPO 和 Flow-GRPO 需要超过 250 步才能达到类似性能水平。这表明方向修正不仅提升了最终效果，还显著加速了收敛过程。

![[assets/figures/papers/paper_list_l2705_https_arxiv_org_abs_2512_24146/figures/005_Figure_5.jpg]]
*Figure 5: Training Efficiency and Effectiveness Comparison. D2-Align outperforms baselines by being both more effective and more efficient. It achieves a higher score in fewer steps, whereas methods like DanceGRPO and Flow-GRPO require over 250 steps to attain a similar level of performance*

### 人类偏好评估

Figure 8 展示了 HPDv2 上的人类偏好评估结果。D2-Align 在细节保留（Detail Preservation）维度上以 **61.7%** 的压倒性优势领先，而 SRPO 仅为 16.5%，差距高达 45.2 个百分点。这一巨大差异揭示了 PMC 的核心表现：基线方法在追求高奖励分数时牺牲了图像细节，产生过度渲染或概念遗忘等问题。D2-Align 通过修正奖励信号的方向性偏差，使生成器不再向损害细节的“捷径”模式坍塌。

![[assets/figures/papers/paper_list_l2705_https_arxiv_org_abs_2512_24146/figures/014_Figure_8.jpg]]
*Figure 8: Human Preference Evaluation on HPDv2. We conducted a user study comparing*

在图文对齐（Image-Text Alignment）维度上，D2-Align 获得 52.2% 的偏好率，同样位居第一。综合偏好（Overall Preference）达到 48.2%，显著优于所有基线。

Figure 9 的多样性人类偏好评估进一步验证了 D2-Align 在打破偏好-多样性权衡方面的能力。在风格多样性（Style Diversity）上，D2-Align 获得 **37.3%** 的偏好率，而 SRPO 仅约 23%；在身份多样性（Identity Diversity）上，D2-Align 获得 35.2%，同样大幅领先。值得注意的是，DanceGRPO 和 Flow-GRPO 在某些多样性维度上的评分甚至低于基座模型 FLUX，这直接证明了现有 RL 对齐方法存在严重的 PMC 问题——优化过程不仅未能提升多样性，反而使其恶化。

![[assets/figures/papers/paper_list_l2705_https_arxiv_org_abs_2512_24146/figures/015_Figure_9.jpg]]
*Figure 9: Human Preference on Diversity (DivGenBench). We evaluated user preferences across four key diversity dimensions: Identity, Style, Layout, and Tonal. The results reveal a severe PMC in existing RL baselines (DanceGRPO, Flow-GRPO), which often score lower than the Base Model (FLUX), particularly in Tonal and Style diversity. In contrast*

### 消融实验

Figure 7 系统消融了 D2-Align 的关键组件和超参数。

![[assets/figures/papers/paper_list_l2705_https_arxiv_org_abs_2512_24146/figures/008_Figure_7.jpg]]
*Figure 7: Ablation Studies on the Key Components and Hyperparameters of*

**方向向量收敛性**（Figure 7 左）：方向向量 $b_v$ 在经过约 2000 步训练后，其修正效果变得显著且稳定，此后模型性能大幅提升。这表明 $b_v$ 确实在连续嵌入空间中学习到了能够抵消奖励偏差的稳定方向，而非随机扰动。

**引导尺度敏感性**（Figure 7 中）：引导尺度 $\omega$ 在 1.5 时达到最优性能，在 HPS-v2.1 和 Pickscore 上均取得最佳结果。过小的 $\omega$ 无法充分抵消奖励偏差，过大的 $\omega$ 则可能导致过度修正，损害对齐质量。

**学习向量 vs. 手动词汇**（Figure 7 右）：雷达图对比了三种配置：使用学习到的 $b_v$（完整方法）、使用手动离散词汇（如“realistic”）作为修正方向、以及不使用任何方向修正。结果显示，学习到的方向向量在所有评估指标上一致优于手动词汇基线，且全面优于未修正的奖励信号。这一消融实验的关键结论是：奖励模型的偏差存在于连续嵌入空间的特定方向上，离散词汇只能提供粗糙的近似，而可学习向量能够精确捕获并抵消这一偏差。

### 通用性验证

Table 6 和 Table 7 展示了将学习到的方向向量 $b_v$ 嵌入 DanceGRPO 后的性能变化。结果表明，引入 $b_v$ 后 DanceGRPO 在人类偏好对齐、语义一致性和生成多样性上均获得了全面提升。这一通用性实验证明，$b_v$ 捕获的修正方向具有可迁移性，能够作为插件式组件增强其他 RL 对齐方法，进一步验证了方向解耦策略的有效性。

![[assets/figures/papers/paper_list_l2705_https_arxiv_org_abs_2512_24146/figures/016_Table_6.jpg]]
*Table 6: Comprehensive Quantitative Evaluation of Metrics for Human Preference Alignment and Semantic Consistency. We compare FLUX, DanceGRPO, and DanceGRPO incorporated with our learned*

![[assets/figures/papers/paper_list_l2705_https_arxiv_org_abs_2512_24146/figures/017_Table_7.jpg]]
*Table 7: Quantitative Evaluation of Generative Diversity on DivGenBench. We compare FLUX, DanceGRPO, and Dance-GRPO enhanced with our learned bv. All RL-based methods utilize HPS-v2.1 as the reward model. We report Identity Divergence Score (IDS), Artistic Style Coverage (ASC), Spatial Dispersion Index (SDI), and Photographic Variance Score (PVS). Ranking is performed between the RL-based methods. The best score is shown in bold*

### 失败模式与局限

定性对比（Figure 6、Figure 10-15）揭示了基线方法的典型失败模式：DanceGRPO 和 Flow-GRPO 在风格维度上倾向于生成油亮、过度渲染的“塑料感”图像，在身份维度上出现面部特征同质化，在布局维度上缺乏空间变化，在影调维度上饱和度和亮度分布集中。这些失败模式正是 PMC 的直接表现——模型收敛到奖励模型偏好的狭窄高奖励区域。

![[assets/figures/papers/paper_list_l2705_https_arxiv_org_abs_2512_24146/figures/006_Figure_6.jpg]]
*Figure 6: Qualitative Comparison of*

D2-Align 有效缓解了上述问题，但论文未报告方向向量 $b_v$ 在不同奖励模型（非 CLIP 基）上的迁移性实验，也未讨论当奖励偏差随时间动态变化时的适应策略。这些开放性问题的答案需要进一步研究验证。



## 定位与知识库关联

### 1. 问题定位：偏好模式坍塌（PMC）的成因与瓶颈

在扩散模型的强化学习人类反馈（RLHF）对齐中，现有方法普遍面临一个核心瓶颈：**偏好模式坍塌（Preference Mode Collapse, PMC）**。其因果链条如下：

- **奖励模型的固有偏差**：以 HPS-v2.1 为代表的预训练奖励模型在训练过程中习得了对特定视觉风格（如过度光滑、油亮渲染、高饱和度）的系统性偏好。当模型生成符合提示语义但风格不符的图像时，人类会给出低分，而奖励模型却因内在偏差给出高分（见 Figure 3 示例：极简主义提示生成了油亮过度渲染的图像）。
- **单一奖励信号驱动过优化**：现有 RL 对齐方法（如 **DanceGRPO**、**Flow-GRPO**、**SRPO**）以最大化单一预定义奖励为目标，缺乏对生成多样性的显式约束。模型在策略梯度优化过程中迅速收敛到奖励模型偏好的狭窄高峰，导致生成结果在身份、风格、布局、影调四个维度上高度同质化。
- **保真度与多样性的零和博弈**：如 Figure 1 右上方散点图所示，基线方法在偏好分数与多样性之间呈现明显的权衡——要么获得低多样性，要么获得低偏好分数。D2-Align 则打破了这一权衡，同时达到更高的多样性与人类偏好。

### 2. 核心机制：方向解耦对齐（D2-Align）

D2-Align 的核心创新在于**在连续嵌入空间中学习一个方向修正向量 $b_v$**，通过扰动奖励模型的文本嵌入来系统性抵消其固有偏差，而非直接修改生成器或引入额外的正则化项。其两阶段框架的因果机制如下：

**阶段 1：方向修正学习（Directional Correction Learning）**
- 冻结生成器 $G_\theta$，引入可学习向量 $b_v \in \mathbb{R}^d$。
- 通过扰动原始文本嵌入 $e_{\text{text}}$ 生成正/负扰动嵌入：$e_+ = \text{normalize}(e_{\text{text}} + b_v)$，$e_- = \text{normalize}(e_{\text{text}} - b_v)$。
- 构造引导文本嵌入 $\tilde{e}_{\text{text}} = e_- + \omega \cdot (e_+ - e_-)$，从负方向向正方向外推（$\omega > 1$）。
- 计算引导奖励 $R_{\text{guided}}(x_0, c; b_v) = \text{score}(e_{\text{img}}, \tilde{e}_{\text{text}})$，最小化负引导奖励 $\mathcal{L}_{\text{stage1}}(b_v) = \mathbb{E}[-R_{\text{guided}}]$ 来优化 $b_v$。
- **因果机制**：$b_v$ 在训练中自动发现奖励模型偏好方向的反方向，使得修正后的奖励信号更贴合真实人类偏好。

**阶段 2：引导策略对齐（Guided Policy Alignment）**
- 冻结学习到的 $b_v^*$，优化生成器参数 $\theta$，最小化 $\mathcal{L}_{\text{stage2}}(\theta) = \mathbb{E}_{c \sim \mathcal{D}, x_0 \sim G_\theta(c)} [-R_{\text{guided}}(x_0, c; b_v^*)]$。
- **因果机制**：修正后的奖励信号引导生成器远离奖励模型的偏好模式，在保持高奖励的同时维持生成多样性。

### 3. 与基线方法的关系与差异

| 方法 | 核心策略 | 与 D2-Align 的关键差异 | PMC 表现 |
|------|----------|------------------------|----------|
| **DanceGRPO** | 多奖励模型集成，通过组合多个奖励信号避免单一偏差 | 集成策略仅能部分缓解偏差，仍缺乏对多样性的显式保护；D2-Align 从信号源头进行方向性修正 | 严重 PMC（Figure 9 中身份/风格多样性偏好低于基座模型 FLUX） |
| **Flow-GRPO** | 引入 KL 散度正则化项防止策略过优化 | KL 系数高度敏感，调参困难且训练开销大；D2-Align 无需额外正则化，训练更高效（Figure 5） | 存在 PMC，需 250+ 步才能达到 D2-Align 的性能水平 |
| **SRPO** | 基于监督奖励策略优化的 RL 对齐 | 与 DanceGRPO 类似，缺乏对奖励偏差的结构性修正 | 多样性指标次优（Table 2 IDS: 0.259 vs D2-Align 0.251） |
| **手动离散词汇基线** | 在提示中附加“realistic”等离散词汇来抵消偏差 | 离散词汇的修正效果受限于词汇表覆盖范围，无法精细调整；D2-Align 在连续空间中学习的方向向量在所有指标上一致优于手动基线（Figure 7 right） | — |

**通用性验证**：将学习到的 $b_v^*$ 嵌入 DanceGRPO 后，该方法在人类偏好对齐（Table 6）和生成多样性（Table 7）上均获得一致提升，表明方向修正向量具有跨方法的可迁移性。

### 4. 关键公式与符号体系

D2-Align 的数学框架建立在以下公式链上：

- **一步去噪重建**（Eq. 4）：$\hat{\pmb{x}}_0 = \frac{\pmb{x}_t - \sigma_t \pmb{\epsilon}_\theta(\pmb{x}_t, t)}{\alpha_t}$ — 利用 ground-truth 噪声先验从噪声潜伏变量重建可微分的干净图像估计，为奖励模型提供稳定输入。
- **原始奖励**（Eq. 5）：$R(\pmb{x}_0, c) = \text{score}(\Phi_{\text{img}}(\pmb{x}_0), \Phi_{\text{text}}(c))$ — 基于图像嵌入与文本嵌入的余弦相似度。
- **引导奖励**（Eq. 6-9）：通过 $b_v$ 扰动文本嵌入构造 $\tilde{e}_{\text{text}}$，计算 $R_{\text{guided}}(x_0, c; b_v) = \text{score}(e_{\text{img}}, \tilde{e}_{\text{text}})$。
- **多样性评估指标**：IDS（Eq. 11, ArcFace 嵌入平均成对余弦相似度）、ASC（Eq. 15, 风格覆盖比率）、SDI（Eq. 18, 布局多样性）、PVS（Eq. 19, 影调标准差和）。

### 5. 适用边界与局限

**方法适用边界**：
- **基座模型**：以 **FLUX.1.Dev**（Black Forest Labs, 2024）为生成器，基于 Flow Matching 框架训练。理论上可推广至其他扩散/流模型架构，但需验证。
- **奖励模型**：当前验证基于 HPS-v2.1 及 HPS-v2.1 + CLIP 组合。$b_v$ 的学习依赖于奖励模型嵌入空间的结构，更换奖励模型需重新学习方向向量。
- **任务范围**：面向文本到图像生成的 RLHF 对齐场景，DivGenBench 基准覆盖身份、风格、布局、影调四个多样性维度。

**已知局限与开放问题**：
1. **跨奖励模型的迁移性未充分验证**：论文仅在 HPS-v2.1 和 CLIP 基奖励模型上验证了 $b_v^*$ 的有效性。当奖励模型架构或训练数据发生显著变化时，方向修正向量的鲁棒性需要进一步研究。
2. **偏差动态变化的适应性**：若奖励模型的偏差随时间或数据分布动态变化，当前静态的方向修正策略可能需要持续在线适应机制。
3. **DivGenBench 的跨任务推广**：提出的多样性评估基准目前仅针对图像生成任务设计，其在文本生成、音频生成等模态上的适用性尚待探索。
4. **计算开销**：阶段 1 需额外训练约 2000 步才能使 $b_v$ 的修正效果显著且稳定（Figure 7 left），但论文未详细报告该阶段的绝对训练时间与显存占用。

### 6. 在知识库中的定位

D2-Align 在扩散模型 RLHF 对齐方法谱系中占据了一个独特位置：

- **相对于奖励集成方法**（如 DanceGRPO）：D2-Align 不依赖多模型集成，而是从信号源头进行方向性修正，计算开销更低且修正效果更稳定。
- **相对于正则化方法**（如 Flow-GRPO 的 KL 散度约束）：D2-Align 无需敏感的超参数调优，通过解耦奖励修正与策略优化两个阶段，实现了更高效的训练（Figure 5 显示 D2-Align 在更少步数内达到更高分数）。
- **相对于提示工程方法**（手动添加离散词汇）：D2-Align 在连续嵌入空间中学习修正方向，突破了离散词汇表的表达能力上限，在所有评估指标上一致优于手动基线（Figure 7 right）。

该方法的核心贡献在于**首次将奖励偏差建模为嵌入空间中的可学习方向**，并通过两阶段解耦框架实现了偏好对齐与多样性保持的协同优化，为 RLHF 中的模式坍塌问题提供了结构化的解决方案。



## 原文 PDF

![[paperPDFs/CVPR_2026/Taming_Preference_Mode_Collapse_via_Directional_Decoupling_Alignment_in_Diffusion_Reinforcement_Learning.pdf]]
