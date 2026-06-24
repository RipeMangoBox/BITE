---
title: "CLaD: Planning with Grounded Foresight via Cross-Modal Latent Dynamics"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CLaD_Planning_with_Grounded_Foresight_via_Cross_Modal_Latent_Dynamics.pdf
project_link: "https://andrewwwj.github.io/clad"
code_link: null
aliases:
- CCMLD
- CLaD
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 非对称交叉注意力（asymmetric cross-attention）：以本体感觉转移作为查询、语义转移作为键值，使模型能够通过运动学上下文解读场景变化，从而提取任务相关的跨模态动态。
primary_logic: 一致性约束应从静态状态对齐转向动态转移一致性：通过建模本体感觉和语义状态在动作下的联合演化，利用 EMA 目标编码器和辅助重构损失预测“有基础的潜在远见”（grounded latent foresight），避免显式语义生成的计算开销，同时指导扩散策略生成动作。
claims:
- CLaD 以仅 0.66B 参数在 LIBERO-LONG 上达到 94.7% 成功率，与 7B 的 OpenVLA（93.8%）和 3.3B 的 π0.5（93.2%）竞争。
- 使用非对称交叉注意力（本体感觉查询语义）达到 94.7%，优于反向配置（93.8%）和对称自注意力（86.7%）。
- 移除辅助重构损失 L_recon 导致成功率从 94.7% 降至 86.1%（-8.6%），证明 grounded 机制至关重要。
- 模态消融显示完整跨模态远见（94.7%）远优于仅本体感觉远见（50.4%），表明运动学预测必须依赖语义上下文。
---

# CLaD: Planning with Grounded Foresight via Cross-Modal Latent Dynamics

> [!tip] 核心洞察
> 一致性约束应从静态状态对齐转向动态转移一致性：通过建模本体感觉和语义状态在动作下的联合演化，利用 EMA 目标编码器和辅助重构损失预测“有基础的潜在远见”（grounded latent foresight），避免显式语义生成的计算开销，同时指导扩散策略生成动作。

| 字段 | 内容 |
|------|------|
| 中文题名 | CLaD：跨模态潜在动态驱动的具身远见规划 |
| 英文题名 | CLaD: Planning with Grounded Foresight via Cross-Modal Latent Dynamics |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.29409) · [Project](https://andrewwwj.github.io/clad) |
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | CLaD (Cross-modal Latent Dynamics) |
| Dataset | LIBERO-LONG |

> [!tip] 效果简介
> - LIBERO-LONG (Avg. Success Rate) 上，成功率 (%) 94.7 vs 93.8 (OpenVLA, 7B) (+0.9)；成功率 (%) 94.7 vs 93.2 (π0.5, 3.3B) (+1.5)；成功率 (%) 94.7 vs 88.6 (LBP, 0.19B) (+6.1)。

## 概述

### 问题瓶颈

现有机器人规划方法在利用多模态信息时存在一个根本性缺陷：它们要么生成显式的语义产物（如子目标图像或文本），引入高昂的计算开销；要么在单一模态的潜在空间中进行规划，缺乏对语义与本体感觉之间动态关联的理解。这种跨模态对齐的缺失导致潜在表示在 rollout 过程中逐渐解耦，产生物理上或逻辑上不一致的轨迹。核心瓶颈在于，现有方法关注的是**静态状态**的对齐，而非**动态转移**的一致性——即语义状态和本体感觉状态在动作作用下的**联合演化**规律。

### 核心洞见

CLaD 提出了一种范式转换：**将一致性约束从静态状态对齐转向动态转移一致性**。其核心思想是通过建模本体感觉和语义状态在动作下的联合演化，利用非对称交叉注意力（asymmetric cross-attention）让运动学转移作为查询去解读语义转移，从而提取任务相关的跨模态动态。在此基础上，通过 EMA 目标编码器和辅助重构损失进行自监督学习，预测“有基础的潜在远见”（grounded latent foresight）——既避免了显式语义生成的计算负担，又能为下游策略提供富含物理与语义一致性的规划条件。

### 方法定位

CLaD 是一种两阶段的**潜在空间规划框架**：

- **Stage 1（跨模态潜在动态）**：学习本体感觉与语义状态在动作下的联合转移规律，通过非对称交叉注意力和可学习池化提取紧凑的跨模态动态表示 $\mathbf{z}_{\mathrm{dyn}}$，并预测未来的潜在嵌入（latent foresights）。训练采用 EMA 目标编码器防止表示坍缩，辅以重构损失将潜在预测锚定回可观测状态。
- **Stage 2（扩散策略）**：以当前观察和预测远见为条件，通过 FiLM 调制自适应融合，驱动 DDPM 扩散模型生成动作序列。

相较于现有方法，CLaD 的关键差异在于：规划表示从当前观察嵌入升级为**预测的跨模态远见**；跨模态对齐从无或静态对比转向**基于转移的非对称交叉注意力**；训练目标从单一动作预测损失扩展为**潜在预测损失 + 辅助重构损失**。

### 主要结果

在 LIBERO-LONG 长视距操作基准上，CLaD 以仅 **0.66B 参数**达到 **94.7% 的平均成功率**，与 7B 的 OpenVLA（93.8%）和 3.3B 的 π0.5（93.2%）竞争，同时显著优于同类的潜在规划方法如 LBP（88.6%，0.19B）。在推理效率方面，CLaD 达到 **25 Hz**，显存占用仅 **4 GB**，远优于 OpenVLA（6 Hz / 15 GB）和 π0.5（10 Hz / 19 GB）。

消融实验验证了三个核心设计选择：
- **跨模态远见不可或缺**：仅使用本体感觉远见（CLaDp）成功率骤降至 50.4%，而全模态 CLaD 达 94.7%，说明运动学预测必须依赖语义上下文。
- **Grounding 机制至关重要**：移除辅助重构损失 $\mathcal{L}_{\mathrm{recon}}$ 导致成功率从 94.7% 降至 86.1%（-8.6%），UMAP 可视化进一步显示潜在嵌入的聚类结构明显退化。
- **非对称交叉注意力是最优归纳偏置**：本体感觉查询语义的配置（94.7%）优于反向配置（93.8%）和对称自注意力（86.7%）。

### 局限与展望

CLaD 在短视距泛化任务（如 LIBERO-Spatial、Object、Goal）上表现落后于大规模 VLA 模型，且训练依赖动作标注，尚未在大规模异质数据上验证动态预训练的摊销能力。此外，所有实验均在仿真环境中进行，真实机器人部署有待探索。

## 背景与动机

### 具身规划中的远见困境

在长视距机器人操作任务中，智能体必须在连续动作空间中进行序贯决策，而每一步决策都依赖于对未来的准确预期。现有规划方法大致分为两类，但各自存在根本性局限：

**显式语义规划**（如 **SuSIE**（Black et al., ICLR 2024））通过生成子目标图像或文本来引导低层策略。这类方法虽然可解释性强，但在生成过程中引入昂贵的解码开销，且显式生成的目标往往缺乏与本体感觉状态（关节角度、末端位姿等）的精确对应，导致生成的子目标在物理上不可执行。

**单模态潜在规划**（如 **LBP**（Liu et al., ICML 2025）、**Seer**（Tian et al., ICLR 2025））将规划压缩到紧凑的潜在空间中进行，避免了显式生成的代价。然而，这些方法仅在单一模态（纯视觉或纯本体感觉）的潜在空间中建模，**忽略了语义状态与本体感觉状态在动作执行下的联合演化**。其后果是：潜在表示在 rollout 过程中逐渐解耦，生成物理或逻辑不一致的轨迹。

### 核心瓶颈：跨模态转移的对齐缺失

两类方法的共同盲点在于：**它们未显式对齐语义与本体感觉的跨模态转移**。具体而言：

- 语义状态（场景中的物体位置、关系）描述“发生了什么”；
- 本体感觉状态（机械臂的运动学配置）描述“如何执行”；
- 两者在动作作用下**协同演化**——机械臂的运动改变了场景，而场景的变化又约束了后续动作。

现有方法要么将这种协同演化视为黑箱（端到端模仿学习），要么仅在静态状态层面进行对齐（如视觉-本体感觉对比学习），**从未在转移层面建模跨模态动态**。这导致规划缺乏“有基础的远见”（grounded foresight）：模型可以预测未来的潜在表示，但这些表示与可观测的物理状态之间的联系是脆弱的。

### 大规模 VLA 的替代路径及其代价

另一条技术路线是大规模视觉-语言-动作模型（VLA），如 **OpenVLA**（Kim et al., arXiv 2024, 7B 参数）和 **π0.5**（Physical Intelligence et al., arXiv 2025, 3.3B 参数）。这些模型通过海量预训练获得了强大的语义理解和泛化能力，在 LIBERO-LONG 上分别达到 93.8% 和 93.2% 的成功率。然而，它们的代价同样显著：

- **推理效率低下**：OpenVLA 仅 6 Hz，π0.5 为 10 Hz，难以满足实时控制需求；
- **显存占用巨大**：OpenVLA 需 15 GB，π0.5 需 19 GB，限制了在边缘设备上的部署。

这引出了一个关键问题：**能否在不依赖大规模预训练的前提下，通过显式建模跨模态动态来获得与 VLA 竞争的性能，同时保持轻量高效？**

### CLaD 的动机与设计直觉

CLaD 的核心直觉是：**一致性约束应从静态状态对齐转向动态转移一致性**。与其让模型学习“当前看到什么”，不如让它学习“在动作执行后，本体感觉和语义状态将如何联合变化”。这种转移层面的对齐天然地捕捉了跨模态的因果结构：本体感觉转移（运动学变化）作为查询，去解读语义转移（场景变化），从而提取任务相关的跨模态动态。

在此基础上，CLaD 通过自监督目标预测“有基础的潜在远见”——既包含对未来潜在状态的预测，又通过辅助重构损失将这些预测锚定到可观测的物理量上。这种设计避免了显式语义生成的计算开销，同时为下游扩散策略提供了富含跨模态上下文的条件信号，使动作生成既具有远见性，又扎根于物理现实。

## 核心创新

CLaD 的核心创新在于将具身规划中的一致性约束从**静态状态对齐**转向**动态转移一致性**。现有方法（如 SuSIE、Seer、LBP）或生成显式语义子目标，或在单一模态的潜在空间中进行规划，未能显式建模本体感觉与语义状态在动作作用下的联合演化，导致潜在表示在 rollout 过程中逐渐解耦，生成物理或逻辑不一致的轨迹。

CLaD 通过以下四个关键 changed slot 解决了该瓶颈：

### 1. 规划表示：从当前观察到潜在远见

传统扩散策略（Diffusion Policy）仅以当前观察 $o_t$ 为条件生成动作序列。CLaD 将规划条件扩展为**预测的未来潜在状态（latent foresights）** $\hat{\mathbf{e}}^{t+\tau}$，由跨模态动态模型生成。这些远见嵌入编码了本体感觉和语义状态在动作下的预期演化，使策略能够“预见”动作后果，而非仅依赖当前瞬时观察。在 LIBERO-LONG 上，仅使用策略而不加远见条件时，成功率远低于完整 CLaD（见 Figure 3 中 Policy only 基线）。

### 2. 跨模态对齐：非对称交叉注意力

现有方法或缺乏跨模态对齐，或仅进行静态状态对齐（如视觉-本体感觉对比学习）。CLaD 引入**基于转移的非对称交叉注意力**（Equation 9）：

$$\mathbf{z}_{p \to s} = \text{CrossAttn}(\mathbf{z}_p, \mathbf{z}_s) \in \mathbb{R}^{N_p \times H}$$

其中本体感觉转移 $\mathbf{z}_p$ 作为查询（query），语义转移 $\mathbf{z}_s$ 作为键值（key-value）。这一设计使模型能够**通过运动学上下文解读场景变化**：本体感觉编码了“机械臂如何移动”的信息，语义编码了“场景中发生了什么”，前者查询后者以提取任务相关的跨模态动态。消融实验（Table 5）证实：该配置达到 94.7% 成功率，优于反向配置（语义查询本体，93.8%）和对称自注意力（86.7%），验证了“以运动学为锚点理解语义变化”这一归纳偏置的有效性。

### 3. 训练目标：潜在预测损失 + 辅助重构损失

传统扩散策略仅使用动作预测损失（DDPM 噪声预测）。CLaD 在 Stage 1 的训练中引入双重自监督目标：

- **潜在预测损失** $\mathcal{L}_{\text{latent}}$（Equation 17）：在 L2 归一化嵌入上最小化预测远见与 EMA 目标编码器输出之间的 MSE，防止表示坍缩。
- **辅助重构损失** $\mathcal{L}_{\text{recon}}$（Equation 18）：将预测的潜在嵌入解码回原始本体感觉和语义状态，作为 **grounding 机制**，确保潜在空间不漂移。

总损失为 $\mathcal{L} = \mathcal{L}_{\text{latent}} + \lambda_{\text{recon}} \mathcal{L}_{\text{recon}}$，其中 $\lambda_{\text{recon}}=0.1$。消融实验（Table 4）显示，移除 $\mathcal{L}_{\text{recon}}$ 导致成功率从 94.7% 骤降至 86.1%（-8.6%），UMAP 可视化（Figure 4）进一步表明无重构约束时潜在嵌入的聚类结构变得分散重叠，证实 grounding 对稳定潜在空间至关重要。

### 4. 策略条件化：FiLM 自适应融合

CLaD 不直接将远见嵌入传入策略，而是通过 **FiLM 调制**（Equation 21）以当前观察对预测远见进行自适应调制，将预测锚定到当前上下文。这使策略同时感知“当前状态”和“预期未来”，在保持远见指导的同时避免预测误差累积。最终策略损失（Equation 22）为以调制后远见为条件的 DDPM 噪声预测损失。

### 创新总结

CLaD 的方法论贡献可概括为：**通过建模本体感觉和语义状态在动作下的联合演化，以非对称交叉注意力提取跨模态动态，并利用 EMA 目标编码器和辅助重构损失预测“有基础的潜在远见”，避免显式语义生成的计算开销，同时为扩散策略提供富含任务上下文的条件信号。** 该设计以 0.66B 参数在 LIBERO-LONG 上达到 94.7% 成功率，与 7B 的 OpenVLA（93.8%）和 3.3B 的 π0.5（93.2%）竞争，同时推理速度达 25 Hz、显存仅 4 GB（Table 2），在参数效率与计算效率上均展现出显著优势。

## 整体框架

CLaD 采用**两阶段解耦架构**，将跨模态动态学习与动作生成分离，从而在不生成显式语义中间产物（如子目标图像或文本）的前提下获得有基础的潜在远见。

### 阶段一：跨模态潜在动态（Cross-Modal Latent Dynamics）

该阶段是整个框架的核心创新，目标是学习本体感觉（proprioceptive）和语义（semantic）状态在动作作用下的**联合演化规律**。

**输入**：当前时刻的本体感觉状态 $p^t$、语义状态 $s^t$（由视觉-语言特征经 FiLM 融合得到）以及执行的动作 $a^t$。

**处理流程**（参见 Figure 2 左侧）：

1. **模态编码**：$f_p$ 和 $f_s$ 分别将 $p^t$ 和 $s^t$ 编码为令牌序列 $\mathbf{p}^t \in \mathbb{R}^{N_p \times H}$ 和 $\mathbf{s}^t \in \mathbb{R}^{N_s \times H}$（$H=1024$, $N_p=N_s=4$）。

2. **转移提取**：通过模态特定的交叉注意力模块，从状态-动作对中提取转移表示 $\mathbf{z}_p$ 和 $\mathbf{z}_s$，捕获每种模态在动作下的变化模式。

3. **非对称跨模态交叉注意力**：这是 CLaD 的关键设计——以本体感觉转移 $\mathbf{z}_p$ 作为查询（query）、语义转移 $\mathbf{z}_s$ 作为键值（key/value），通过交叉注意力得到跨模态动态 $\mathbf{z}_{p \to s}$。这一非对称设计使得运动学上下文能够“解读”场景语义变化，而非机械地对齐静态状态。

4. **可学习池化**：将跨模态特征压缩为紧凑的动态表示 $\mathbf{z}_{\mathrm{dyn}} \in \mathbb{R}^{H}$。

5. **远见预测**：轻量级 MLP 解码器 $g_p$ 和 $g_s$ 从 $\mathbf{z}_{\mathrm{dyn}}$ 预测未来 $t+\tau$ 时刻的潜在嵌入 $\hat{\mathbf{z}}_p^{t+\tau}$ 和 $\hat{\mathbf{z}}_s^{t+\tau}$。

**训练目标**：阶段一通过两项自监督损失进行优化——

- **潜在预测损失** $\mathcal{L}_{\mathrm{latent}}$：在 L2 归一化嵌入上最小化预测与 EMA 目标编码器输出的 MSE，防止表示坍缩。
- **辅助重构损失** $\mathcal{L}_{\mathrm{recon}}$：将预测嵌入通过 $h_p$、$h_s$ 解码回原始状态空间，以 L1 损失约束潜在表示与可观测量的联系，作为关键的 **grounding 机制**。

总损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{latent}} + \lambda_{\mathrm{recon}} \mathcal{L}_{\mathrm{recon}}$（$\lambda_{\mathrm{recon}}=0.1$）。

### 阶段二：以远见为条件的扩散策略

阶段二将阶段一预测的潜在远见注入低层动作生成（参见 Figure 2 右侧）。

**输入**：当前观察 $o_t$（由 $e_p$ 和 $e_s$ 编码得到）以及阶段一输出的预测远见 $\hat{\mathbf{z}}_p^{t+\tau}$ 和 $\hat{\mathbf{z}}_s^{t+\tau}$。

**处理流程**：

1. **FiLM 自适应调制**：以当前观察为条件对远见嵌入进行 FiLM 调制，将预测的未来状态锚定到当前上下文，避免预测漂移。

2. **DDPM 动作生成**：以调制后的条件信号为输入，扩散策略通过去噪过程生成动作序列 $\mathbf{a}_t$，训练目标为标准噪声预测损失 $\mathcal{L}_{\mathrm{policy}}$。

### 端到端部署

推理时，阶段一（CLaD 动态模型）以冻结的 VLM 编码器（0.1B）提取语义特征，经跨模态动态预测远见；阶段二（扩散策略，0.23B）据此生成动作。整个流程达到 **25 Hz 推理频率，显存占用仅 4 GB**，远优于 OpenVLA（6 Hz / 15 GB）和 π0.5（10 Hz / 19 GB）。模型总参数量 0.66B，但推理时 VLM 冻结，实际运行时开销更低。

**关键设计决策**：两阶段分离使得动态学习可以专注于跨模态转移一致性，而策略学习可以专注于将预测远见转化为精确动作，避免了端到端联合训练中表示解耦的风险。消融实验证实，移除辅助重构损失 $L_{\mathrm{recon}}$ 会导致成功率从 94.7% 降至 86.1%（-8.6%），验证了 grounding 机制对稳定潜在空间的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l2452_https_arxiv_org_abs_2603_29409/figures/001_Figure_1.jpg]]
*Figure 1: Overview of CLaD. (a) Conventional approaches either generate semantic artifacts (e.g., subgoal images or texts), or plan in unimodal latent spaces that lack cross-modal understanding. (b) CLaD learns cross-modal latent dynamics to predict grounded latent foresights, which condition a diffusion policy for action generation. CLaD achieves 94.7% with only 0.66B parameters, competitive with OpenVLA (7B) and π0.5 (3.3B)*

## 核心模块与公式推导

CLaD 是一个两阶段框架：Stage 1 学习跨模态潜在动态并预测“有基础的潜在远见”（grounded latent foresight），Stage 2 以当前观察和预测远见为条件，通过扩散策略生成动作序列。以下按管道模块拆解其关键设计与公式。

### 模态编码器

本体感觉状态 $p^t$ 和语义状态 $s^t$ 分别通过 MLP 编码为令牌序列：

$$ \mathbf{p}^t = f_p(p^t) \in \mathbb{R}^{N_p \times H}, \quad \mathbf{s}^t = f_s(s^t) \in \mathbb{R}^{N_s \times H} $$

其中 $H=1024$ 为隐藏维度，可学习令牌数 $N_p = N_s = 4$。语义状态 $s^t$ 由冻结 VLM 提取的视觉特征经 FiLM 融合语言指令得到。

### 模态特定转移提取器

为建模“转移”而非静态状态，给定状态-动作对 $(p^t, a^t)$ 和 $(s^t, a^t)$，通过交叉注意力提取转移表示：

$$ \mathbf{z}_p = \text{CrossAttn}(\mathbf{p}^t, [\mathbf{p}^t; \mathbf{a}^t]) \in \mathbb{R}^{N_p \times H} $$

$$ \mathbf{z}_s = \text{CrossAttn}(\mathbf{s}^t, [\mathbf{s}^t; \mathbf{a}^t]) \in \mathbb{R}^{N_s \times H} $$

其中 $\mathbf{a}^t$ 为动作嵌入，$[\cdot;\cdot]$ 表示拼接。$\mathbf{z}_p$ 捕获本体感觉转移，$\mathbf{z}_s$ 捕获语义转移。

### 非对称交叉注意力：跨模态动态核心

核心创新在于以**本体感觉转移查询语义转移**，使模型通过运动学上下文解读场景变化：

$$ \mathbf{z}_{p \to s} = \text{CrossAttn}(\mathbf{z}_p, \mathbf{z}_s) \in \mathbb{R}^{N_p \times H} $$

随后通过可学习池化压缩为紧凑动态表示：

$$ \mathbf{z}_{\mathrm{dyn}} = \text{Pool}(\mathbf{q}_{\mathrm{out}}, \mathbf{z}_{p\to s}) \in \mathbb{R}^{H} $$

其中 $\mathbf{q}_{\mathrm{out}}$ 为可学习查询令牌。这一非对称设计是性能关键——消融实验（Table 5）显示，本体查询语义的配置（94.7%）优于反向配置（93.8%）和对称自注意力（86.7%）。

### 远见解码器与 EMA 目标编码器

从 $\mathbf{z}_{\mathrm{dyn}}$ 出发，轻量 MLP 预测未来 $\tau$ 步的潜在嵌入：

$$ \hat{\mathbf{z}}_p^{t+\tau} = g_p(\mathbf{z}_{\mathrm{dyn}}) \in \mathbb{R}^{H}, \quad \hat{\mathbf{z}}_s^{t+\tau} = g_s(\mathbf{z}_{\mathrm{dyn}}) \in \mathbb{R}^{H} $$

为提供稳定的自监督学习目标，使用指数移动平均（EMA，动量 $m=0.995$）的目标编码器 $\bar{f}_p, \bar{f}_s$ 编码真实未来状态，得到目标嵌入 $\bar{\mathbf{z}}_p^{t+\tau}, \bar{\mathbf{z}}_s^{t+\tau}$。

### 潜在预测损失

在 L2 归一化嵌入上最小化 MSE，防止表示坍缩：

$$ \mathcal{L}_{\mathrm{latent}} = \left\| \hat{\mathbf{z}}_p^{t+\tau} - \frac{\bar{\mathbf{z}}_p^{t+\tau}}{\|\bar{\mathbf{z}}_p^{t+\tau}\|} \right\|_2^2 + \left\| \hat{\mathbf{z}}_s^{t+\tau} - \frac{\bar{\mathbf{z}}_s^{t+\tau}}{\|\bar{\mathbf{z}}_s^{t+\tau}\|} \right\|_2^2 $$

### 辅助重构损失：Grounding 机制

为防止潜在表示漂移，将预测嵌入通过重构解码器 $h_p, h_s$ 映射回原始状态空间，以 L1 损失约束：

$$ \mathcal{L}_{\mathrm{recon}} = \| h_p(\hat{\mathbf{z}}_p^{t+\tau}) - p^{t+\tau} \|_1 + \| h_s(\hat{\mathbf{z}}_s^{t+\tau}) - s_v^{t+\tau} \|_1 $$

总训练损失为：

$$ \mathcal{L} = \mathcal{L}_{\mathrm{latent}} + \lambda_{\mathrm{recon}} \mathcal{L}_{\mathrm{recon}}, \quad \lambda_{\mathrm{recon}} = 0.1 $$

消融实验（Table 4）显示，移除 $\mathcal{L}_{\mathrm{recon}}$ 导致成功率从 94.7% 骤降至 86.1%（-8.6%），UMAP 可视化（Figure 4）进一步证实无重构损失时潜在嵌入聚类变得弥散重叠，验证了 grounding 对稳定潜在空间的关键作用。

### FiLM 调制与扩散策略条件化

在 Stage 2，预测远见 $\hat{\mathbf{z}}^{t+\tau} = [\hat{\mathbf{z}}_p^{t+\tau}; \hat{\mathbf{z}}_s^{t+\tau}]$ 需锚定到当前上下文。通过 FiLM 层以当前观察嵌入 $\mathbf{o}^t$ 进行自适应调制：

$$ \mathbf{g} = \text{FiLM}(\hat{\mathbf{z}}^{t+\tau}, \mathbf{o}^t) $$

其中 $\mathbf{o}^t = [e_p(p^t); e_s(s_v^t, s_l)]$ 融合当前本体感觉和语义观察。调制后的表示 $\mathbf{g} = [\mathbf{g}_p; \mathbf{g}_s]$ 作为扩散策略的条件，DDPM 噪声预测损失为：

$$ \mathcal{L}_{\mathrm{policy}} = \mathbb{E}_{\mathbf{a}_0, k, \epsilon} \left[ \| \epsilon - \hat{\epsilon}_{\theta}(\mathbf{a}_k, k, \mathbf{g}_p, \mathbf{g}_s) \|_2^2 \right] $$

其中 $\mathbf{a}_0$ 为真实动作序列，$k$ 为扩散时间步，$\epsilon$ 为高斯噪声。动作预测范围 $\tau=6$，推理时从噪声出发经 $T$ 步去噪生成动作序列。

### 补充图表

![[assets/figures/papers/paper_list_l2452_https_arxiv_org_abs_2603_29409/figures/002_Figure_2.jpg]]
*Figure 2: Detailed architecture of CLaD’s two-stage framework. Stage 1 (Left) - Semantic state*

## 实验与分析

### 主结果：LIBERO-LONG 性能对比

CLaD 在 LIBERO-LONG 的 10 个长视距任务上取得 **94.7%** 的平均成功率（Table 1），以仅 **0.66B** 参数与大规模 VLA 模型竞争：超越 **OpenVLA**（7B, 93.8%）和 **π0.5**（3.3B, 93.2%），并显著领先同类潜在规划方法 **LBP**（0.19B, 88.6%）、**Seer**（0.32B, 87.7%）和 **SuSIE**（0.86B, 76.3%）。

![[assets/figures/papers/paper_list_l2452_https_arxiv_org_abs_2603_29409/figures/003_Table_1.jpg]]
*Table 1: Performance comparison on LIBERO-LONG benchmark. CLaD achieves competitive performance with significantly fewer parameters (0.66B) compared to baselines. LIBERO-LONG tasks include: (1) put soup and sauce in basket; (2) put box and butter in basket; (3) turn on stove and put pot; (4) put bowl in drawer and close it; (5) put mugs on left and right plates; (6) pick book and place it in back; (7) put mug on plate and put pudding to right; (8) put soup and box in basket; (9) put both pots on stove; (10) put mug in microwave and close it*

参数效率优势突出：CLaD 总参数量 0.66B（包含冻结 VLM 0.1B、CLaD 动态模型 0.33B、扩散策略 0.23B），而 **OpenVLA** 和 **π0.5** 分别需要 7B 和 3.3B。推理效率同样显著（Table 2）：CLaD 达到 **25 Hz** 推理频率、仅 **4 GB** 显存占用，远优于 OpenVLA（6 Hz / 15 GB）和 π0.5（10 Hz / 19 GB）。

![[assets/figures/papers/paper_list_l2452_https_arxiv_org_abs_2603_29409/figures/005_Table_2.jpg]]
*Table 2: Comparison on computational requirements. CLaD achieves faster inference and lower resource consumption compared to large-scale VLA models, while maintaining competitive task performance on LIBERO-LONG*

> ⚠️ **公平性说明**：Table 1 中标记 † 的方法（SuSIE、Seer、LBP、Ours†）为 top-3 检查点的 20 次 rollout 平均；标记 ‡ 的方法（OpenVLA、π0、π0.5、Ours‡）为单检查点的 50 次 rollout 平均。评估协议差异可能影响直接数值比较。此外，正文声称 CLaD 在 Task 9 上优于 LBP，但 Table 1 显示 LBP 为 82.0%、CLaD（Ours†）为 81.3%，存在矛盾，需人工核实是否为笔误或不同检查点。

### 跨模态远见的关键作用

模态消融实验（Figure 3）直接验证了跨模态远见的核心贡献：
- **仅本体感觉远见（CLaDp）**：成功率骤降至 50.4%，表明单纯运动学预测无法支撑长视距规划；
- **仅语义远见（CLaDs）**：成功率 91.5%，说明语义上下文对规划不可或缺；
- **完整跨模态远见（CLaD）**：94.7%，证明本体感觉与语义的联合演化建模带来显著增益。

![[assets/figures/papers/paper_list_l2452_https_arxiv_org_abs_2603_29409/figures/004_Figure_3.jpg]]
*Figure 3: Modality contribution analysis on LIBERO-LONG tasks. We compare diffusion policy without foresight conditioning (Policy only), conditioning on proprioceptive foresight only (CLaDp), semantic foresight only (CLaDs), and full cross-modal foresight (CLaD). Results demonstrate that cross-modal foresight provides substantial gains over single-modality predictions, though semantic foresight alone achieves reasonable performance. Notably, proprioceptive foresight alone severely degrades performance, suggesting that kinematic predictions require semantic context for effective planning*

这一结果表明，运动学预测必须依赖语义上下文——本体感觉转移通过非对称交叉注意力查询语义转移，提取任务相关的跨模态动态，而非简单的模态拼接。

### 消融实验：架构设计的因果验证

**辅助重构损失 L_recon 的 grounding 作用**（Table 4）：移除 L_recon 导致成功率从 94.7% 降至 **86.1%**（-8.6%），是单项消融中降幅最大的操作。UMAP 可视化（Figure 4）进一步揭示：有 L_recon 时，潜在动态表示 z_dyn 形成清晰的任务特定簇；无 L_recon 时，簇边界模糊重叠，表明潜在空间发生漂移。这证实了 L_recon 通过将预测嵌入解码回原始状态，锚定了潜在表示与可观测量的联系。

**非对称交叉注意力的归纳偏置**（Table 5）：
- 本体感觉查询语义（CLaD 默认）：**94.7%**
- 语义查询本体感觉（反向配置）：93.8%
- 对称自注意力：86.7%

非对称设计让运动学上下文“解读”场景变化，优于对称融合和反向查询，验证了该归纳偏置的有效性。

**动作条件与掩码策略**（Table 7）：随机掩码率 r=0.3 的 CLaD（94.7%）优于重度掩码（Heavy Mask, 88.2%）、无动作训练（Action-free, 90.8%）和课程掩码（Curriculum, 85.1%）。无动作训练引入多模态歧义，降低了预测确定性，确认动作条件对跨模态动态学习的必要性。

### 全 LIBERO 套件泛化表现

Table 6 展示了 CLaD 在所有 LIBERO 套件上的 50 次 rollout 平均成功率。CLaD 在 LIBERO-LONG 上表现最强，但在 **LIBERO-Spatial、Object、Goal** 等短视距泛化任务上落后于 OpenVLA 和 π0.5。这暴露了 CLaD 的核心局限：缺乏大规模预训练带来的 in-distribution 泛化优势，跨模态动态预训练目前仅在单任务 LIBERO-LONG 上进行，尚未在多任务异质数据上摊销。

![[assets/figures/papers/paper_list_l2452_https_arxiv_org_abs_2603_29409/figures/011_Table_6.jpg]]
*Table 6: Average success rates (%) over 50 rollouts on all suites in LIBERO benchmark. Color intensity is proportional to the performance level (thicker = higher)*

### 失败模式分析

在需要精细操作和感知模糊的任务上，CLaD 表现相对薄弱。例如 Task 9（put both pots on stove）成功率仅约 81%，反映出对视觉歧义的敏感性——当场景中物体相似或遮挡严重时，语义编码器可能产生模糊表示，导致跨模态动态预测偏差。此外，所有实验均在 LIBERO 仿真环境中进行，未在真实机器人上验证，sim-to-real 转移能力尚不明确。

### 补充图表

![[assets/figures/papers/paper_list_l2452_https_arxiv_org_abs_2603_29409/figures/006_Table_3.jpg]]
*Table 3: Performance and efficiency of latent planning methods on LIBERO-LONG. Although CLaD requires more parameters than LBP (0.19B) and UVA (0.5B), it yields higher average success rate, respectively, suggesting a competitive trade-off between model capacity and task performance within the latent planning paradigm*

![[assets/figures/papers/paper_list_l2452_https_arxiv_org_abs_2603_29409/figures/007_Table_4.jpg]]
*Table 4: Ablation of the auxiliary reconstruction loss*

![[assets/figures/papers/paper_list_l2452_https_arxiv_org_abs_2603_29409/figures/008_Figure_4.jpg]]
*Figure 4: UMAP of latent embedding*

![[assets/figures/papers/paper_list_l2452_https_arxiv_org_abs_2603_29409/figures/009_Table_5.jpg]]
*Table 5: Ablation of cross-attention configurations. Using proprioceptive transitions as queries over semantic transitions (94.7%) outperforms both the reverse configuration (93.8%) and symmetric self-attention (86.7%), confirming that directing kinematic context to attend over semantic transitions is a beneficial inductive bias for extracting cross-modal dynamics*

![[assets/figures/papers/paper_list_l2452_https_arxiv_org_abs_2603_29409/figures/010_Figure_5.jpg]]
*Figure 5: Pixel attribution for predicted latent foresight via Integrated Gradients. Heatmaps show pixel-level contributions toward the alignment between predicted foresight zˆt+τ and target embedding. Brighter regions indicate higher attribution scores. While not yielding precise object boundaries, attributions consistently highlight task-relevant objects, suggesting that the model leverages semantic features for future state prediction*

![[assets/figures/papers/paper_list_l2452_https_arxiv_org_abs_2603_29409/figures/012_Table_7.jpg]]
*Table 7: Ablation with action-free training variants*

## 方法谱系与知识库定位

### 1. 方法谱系：从静态对齐到动态转移一致性

CLaD 的核心推进在于将跨模态对齐的焦点从**静态状态**转向**动态转移**。传统方法或显式生成语义中间表示（子目标图像/文本），或在单一模态的潜在空间中规划，均未显式建模本体感觉与语义状态在动作下的联合演化。CLaD 直接学习“本体感觉转移如何查询语义转移”，从而提取任务相关的跨模态动态。

| 范式 | 代表工作 | 核心机制 | 与 CLaD 的关系 |
|------|----------|----------|----------------|
| 语义子目标生成 + 低层策略 | **SuSIE** (Black et al., ICLR 2024, 0.86B) | 生成语义子目标图像，再以子目标为条件执行低层策略 | CLaD 不生成显式语义产物，而是在潜在空间中预测“有基础的远见”，避免了显式生成的计算开销与累积误差 |
| 预测性逆向动力学 | **Seer** (Tian et al., ICLR 2025, 0.32B) | 学习逆向动力学模型预测未来状态 | CLaD 同时建模前向跨模态动态与潜在远见预测，并通过 EMA 目标编码器防止表示坍缩 |
| 潜在空间反向规划 | **LBP** (Liu et al., ICML 2025, 0.19B) | 在潜在空间中执行反向规划 | CLaD 以 0.66B 参数在 LIBERO-LONG 上达到 94.7%，较 LBP 的 88.6% 提升 6.1 个百分点（Table 1/Table 3），表明前向跨模态动态建模比纯潜在规划更有效 |
| 大规模 VLA 微调 | **OpenVLA** (Kim et al., arXiv 2024, 7B) | 大规模 VLM 微调为通用 VLA | CLaD 以 1/10 参数量达到 94.7%（vs. 93.8%），推理速度 25 Hz vs. 6 Hz，显存 4 GB vs. 15 GB（Table 2） |
| VLM + 流匹配动作输出 | **π0** / **π0.5** (Black et al., arXiv 2024 / Physical Intelligence et al., arXiv 2025, 3.3B) | VLM 与流匹配结合生成动作 | CLaD 以 1/5 参数量达到 94.7%（vs. π0.5 的 93.2%），推理效率显著占优 |
| 统一视频动作模型 | **UVA** (Li et al., arXiv 2025, 0.5B) | 统一视频与动作建模 | CLaD 参数量略高（0.66B vs. 0.5B），但成功率更高（Table 3），体现跨模态动态建模的收益 |

### 2. 关键设计决策的消融证据

CLaD 的性能优势来自三个相互耦合的设计选择，消融实验给出了清晰的因果证据：

- **非对称交叉注意力（本体查询语义）**：该配置达到 94.7%，优于反向配置（语义查询本体，93.8%）和对称自注意力（86.7%）（Table 5）。这验证了“以运动学上下文解读场景变化”的归纳偏置——本体感觉转移作为查询，迫使模型从语义转移中检索与当前运动状态相关的场景信息。

- **辅助重构损失 L_recon**：移除该损失导致成功率从 94.7% 骤降至 86.1%（-8.6%）（Table 4）。UMAP 可视化（Figure 4）进一步揭示：有 L_recon 时潜在嵌入形成清晰的任务特定簇，无 L_recon 时簇边界模糊重叠。这表明 L_recon 通过将潜在预测锚定回可观测状态，防止了潜在空间的语义漂移。

- **全模态远见 vs. 单模态远见**：仅本体感觉远见（CLaDp）成功率仅 50.4%，语义远见（CLaDs）为 91.5%，全模态 CLaD 达 94.7%（Figure 3）。本体感觉远见的极低成功率证明：运动学预测必须依赖语义上下文，单纯的关节状态外推无法应对长视距任务的场景变化。

### 3. 适用边界与局限

**适用场景**：CLaD 在需要跨模态协调的长视距操作任务（LIBERO-LONG，平均 10 个动作序列）上表现突出，参数效率与推理速度使其适合资源受限的部署环境。

**已知局限**：

1. **短视距泛化不足**：在 LIBERO-Spatial、Object、Goal 等短视距泛化任务上，CLaD 落后于大规模 VLA 模型（如 OpenVLA、π0.5）。这表明跨模态动态建模无法替代大规模预训练带来的分布内泛化能力——CLaD 的 Stage 1 动态预训练目前仅在单任务 LIBERO-LONG 上进行，尚未在多任务异质数据上摊销。

2. **精细操作与感知歧义**：在需要精细操作和感知模糊的任务（如 Task 9: put both pots on stove）上成功率仅约 81%，显示出对视觉歧义的敏感性。此外，Table 1 中 LBP 在 Task 9 上为 82.0%、CLaD 为 81.3%，与正文声称“CLaD 优于 LBP”存在矛盾，可能为不同评估协议或笔误，需人工核实。

3. **动作标注依赖**：训练依赖动作标注。无动作或纯掩码训练变体（Heavy Mask 88.2%, Action-free 90.8%, Curriculum 85.1%）均低于完整 CLaD（Table 7），表明动作条件对消除多模态歧义至关重要。

4. **仿真验证局限**：所有实验均在 LIBERO 仿真环境中进行，未在真实机器人上验证跨模态动态建模对传感器噪声和物理交互不确定性的鲁棒性。

### 4. 开放问题

1. **跨任务摊销**：Stage 1 动态预训练能否在多任务、大规模异质机器人数据集上摊销，从而同时获得参数效率和泛化性？这是 CLaD 追赶大规模 VLA 的关键路径。

2. **多模态扩展**：跨模态动态建模范式能否推广至其他多模态具身任务（如移动操作中融合视觉、力觉、触觉反馈）？非对称交叉注意力的“本体查询语义”归纳偏置在更多模态下是否仍然成立？

3. **精细操作改进**：在需要精确操作和感知易混淆物体的任务上，grounding 机制（L_recon）能否通过更强的重构目标（如感知损失）或外部记忆增强来进一步提高成功率？

4. **评估一致性**：Table 1 与正文关于 Task 9 性能的矛盾需澄清——是不同检查点、不同评估协议还是笔误？这影响对 CLaD 在精细操作任务上表现的准确判断。

5. **语言增强**：能否结合外部记忆或更大规模语言模型来增强任务理解和重规划能力，同时保持 CLaD 的参数效率优势？

## 原文 PDF

![[paperPDFs/CVPR_2026/CLaD_Planning_with_Grounded_Foresight_via_Cross_Modal_Latent_Dynamics.pdf]]
