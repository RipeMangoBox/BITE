---
title: "Reasoning Palette: Modulating Reasoning via Latent Contextualization for Controllable Exploration for (V)LMs"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Reasoning_Palette_Modulating_Reasoning_via_Latent_Contextualization_for_Controllable_Exploration_for_V_LMs.pdf
project_link: null
code_link: null
aliases:
- RP
- RPMRLCCEVL
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 一个由VAE学习的随机潜在变量，其采样值被解码为可学习的token前缀并前置插入到输入提示中，从而在生成开始前调节模型的内部推理策略，将探索从token级别转向策略级别。
primary_logic: 通过潜在情境化将探索从token级随机性转化为策略级结构化采样，即在生成前对推理策略空间进行采样，使RL训练能够访问到更丰富的高层级推理行为，从而显著提升探索效率与最终性能。
claims:
- 直接向Qwen-4B-Base的提示前注入一个高斯噪声token嵌入，仅在潜变量空间采样即大幅提升pass@k准确率，验证了策略级采样的潜力。
- VAE学习的潜在空间和生成的前缀嵌入在PCA与t‑SNE投影中按推理领域形成清晰聚类，证明潜变量成功解耦了高层推理策略。
- 在数学推理基准上，带有潜在引导的RL训练（结合双阶段或线性衰减调度）一致且显著地超越标准GRPO基线；在Qwen3‑8B‑Base + RLOO设置下平均性能提升+3.09点。
- 在指代表达理解（RefCOCO系列）上，仅使用贪心解码的潜在引导即超过使用随机采样的基线，且潜在引导与采样结合取得最优结果。
---

# Reasoning Palette: Modulating Reasoning via Latent Contextualization for Controllable Exploration for (V)LMs

> [!tip] 核心洞察
> 通过潜在情境化将探索从token级随机性转化为策略级结构化采样，即在生成前对推理策略空间进行采样，使RL训练能够访问到更丰富的高层级推理行为，从而显著提升探索效率与最终性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 推理调色板：通过潜在情境化调节推理以实现可控探索的(V)LMs方法 |
| 英文题名 | Reasoning Palette: Modulating Reasoning via Latent Contextualization for Controllable Exploration for (V)LMs |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.17206) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Reasoning Palette |
| Dataset | RefCOCO, RefCOCOg, Math Reasoning Suite, AMC23 |

> [!tip] 效果简介
> - RefCOCO (referring expression comprehension) 上，Pass@32 Latent-guided + sampling 87.53 vs Baseline (greedy) 2.0 / Baseline + sampling 65.07 (+85.53 / +22.46)。
> - RefCOCO+ 上，Pass@32 Latent-guided + sampling 86.03 vs Baseline (greedy) 2.0 / Baseline + sampling 62.57 (+84.03 / +23.46)。
> - RefCOCOg 上，Pass@32 Latent-guided + sampling 85.7 vs Baseline (greedy) 4.67 / Baseline + sampling 72.0 (+81.03 / +13.7)。

## 概述

大型语言模型与视觉语言模型的推理能力在强化学习（RL）训练中面临一个关键瓶颈：标准随机采样策略（如温度采样、核采样）虽在token层面产生多样性，但往往生成策略相近的推理路径，导致高层推理策略的探索不足，限制了RL训练的探索效率与学习持续性。

**Reasoning Palette** 针对这一瓶颈提出了一种潜在情境化框架。其核心思路是将探索从token级别的随机性转化为策略级别的结构化采样——在生成开始之前，通过对一个由变分自编码器（VAE）学习的随机潜在变量进行采样，将其解码为可学习的token前缀并前置插入到输入提示中，从而在生成前调节模型的内部推理策略。这一设计使RL训练能够访问到更丰富的高层级推理行为，显著提升探索效率与最终性能。

方法的有效性通过多维度实验得到验证：
- 在指代表达理解任务（RefCOCO系列）上，仅使用贪心解码的潜在引导即大幅超越随机采样基线，潜在引导与采样结合取得最优结果（如RefCOCO上Pass@32达87.53，相较基线贪心解码的2.0提升+85.53）。
- 在数学推理基准上，带有调度策略的潜在引导RL训练一致且显著地超越标准GRPO基线；在Qwen3-8B-Base + RLOO设置下，平均性能提升+3.09点，在复杂领域（如AMC23、MinervaMath）增益尤为突出（分别+4.38和+4.29）。
- VAE学习的潜在空间在PCA与t-SNE投影中按推理领域形成清晰聚类，证实潜变量成功解耦了高层推理策略。

Reasoning Palette的方法定位在于：将推理策略多样性建模为可学习的连续潜在空间，并通过轻量监督微调（SFT）适配与调度驱动的RL训练，实现从探索到利用的平滑过渡，为(V)LMs的可控推理探索提供了新的范式。

## 背景与动机

大语言模型与视觉语言模型在复杂推理任务上的突破，很大程度上依赖于强化学习（RL）训练中的探索质量。然而，当前主流的探索手段——如温度采样（temperature sampling）、核采样（nucleus sampling）等token级随机解码策略——存在一个根本性瓶颈：**这些方法产生的推理路径虽然在表层token序列上呈现差异，但其高层次的推理策略往往高度相似**。换言之，token级的随机性并未有效转化为策略级的多样性，导致RL训练在探索阶段难以接触到足够广泛的高层推理行为，进而限制了学习效率与最终性能的持续提升。

这一瓶颈在标准GRPO（Group Relative Policy Optimization，Shao et al., 2024）等RL基线上表现得尤为明显：模型在训练早期快速收敛于某些局部最优的推理模式，后续训练难以突破，性能曲线趋于平缓。

本文的**核心动机**来源于一个关键观察：若能在生成开始之前，对模型的**内部推理策略进行结构化采样**，而非依赖生成过程中的token级随机扰动，是否能从根本上提升探索的广度与效率？Figure 1 提供了一个有力的初步验证——仅向Qwen-4B-Base的输入提示前注入一个高斯噪声token嵌入，并在每个候选回答中仅使用贪心解码，即可在pass@k准确率上获得大幅提升。这一现象表明，**在嵌入空间中对推理上下文进行微小的结构性扰动，足以激发模型产生截然不同的推理路径**，从而验证了“策略级采样”的巨大潜力。

基于上述洞察，本文提出**Reasoning Palette**框架，其核心思想是：**通过潜在情境化（latent contextualization），将探索从token级随机性转化为生成前的策略级结构化采样**。具体而言，Reasoning Palette引入一个由变分自编码器（VAE）学习的随机潜在变量，该变量的采样值被解码为可学习的token前缀并前置插入到输入提示中，从而在生成开始前即调节模型的内部推理策略。这一设计使得RL训练能够访问到更丰富的高层级推理行为，在探索阶段覆盖更广泛的策略空间，并在训练后期平滑过渡到利用阶段，最终显著提升探索效率与收敛性能。

## 核心创新

**Reasoning Palette** 的核心贡献在于将推理探索的随机性从 token 级解码提升到**策略级结构化采样**，通过一个由 VAE 学习的潜在变量在生成开始前对模型的内部推理策略进行调节。这一设计从根本上改变了 RL 训练中探索的粒度与效率。

### 1. 瓶颈洞察：Token 级随机性的策略同质化

标准随机采样（温度采样、核采样等）虽然能在 token 层面产生不同的输出序列，但其背后所调用的高层推理策略往往高度相似。这种“表层多样、内核实同质”的现象限制了 RL 训练中真正的探索广度，导致模型在复杂推理任务上难以持续发现更优的解题路径。

方法的核心动机来自一个简洁而有力的验证实验（Figure 1）：**仅向 Qwen-4B-Base 的提示嵌入前注入一个服从高斯噪声的 token 嵌入**，在贪心解码下即可大幅提升 pass@k 准确率。这一现象表明，在 token 生成之前对模型内部状态进行扰动，能够触发显著不同的推理行为——即存在一个可被“调制”的策略空间。

### 2. 核心机制：潜在情境化（Latent Contextualization）

基于上述洞察，方法引入了一个**随机潜在变量 z**，其采样值通过 VAE 解码器映射为可学习的 token 前缀序列，并前置拼接到输入提示中：

$$\mathbf{p_z} = (D_\psi(\mathbf{z}^{(1)}), D_\psi(\mathbf{z}^{(2)}), \dots, D_\psi(\mathbf{z}^{(L)})) \in \mathbb{R}^{L \times d}$$

$$\tilde{\mathbf{q}} = [\mathbf{p_z}; \mathcal{E}(\mathbf{q})], \quad \mathbf{o} \sim \pi_\theta(\cdot \mid \tilde{\mathbf{q}})$$

这种设计将探索从 token 级随机性转化为**生成前的策略级采样**：每次从先验 $p(\mathbf{z}) = \mathcal{N}(0, I)$ 采样一个潜变量，即对应选择一种不同的推理策略模式，再由前缀引导整个生成过程。

VAE 在问答对数据集上训练，其损失函数平衡了重建精度与先验正则：

$$\mathcal{L}^{\mathrm{vAE}} = \mathbb{E}_{\mathbf{z} \sim q_\phi(\mathbf{z}|\mathbf{h})} [\|\mathbf{h} - \hat{\mathbf{h}}\|^2] + \beta \cdot \mathrm{KL}(q_\phi(\mathbf{z}\mid\mathbf{h}) \| p(\mathbf{z}))$$

其中 $\mathbf{h}$ 是问答对拼接后的平均池化嵌入，编码了该问答对所蕴含的推理策略信息。

### 3. 关键验证：潜在空间的策略解耦

PCA 与 t‑SNE 可视化（Figure 3）提供了强有力的结构证据：**生成的前缀嵌入与对应的潜变量在投影空间中按推理领域（数学、代码、QA）形成清晰聚类**。这说明 VAE 成功将高层推理策略解耦到潜在空间的不同区域，使得潜变量采样具有语义意义而非纯粹的噪声扰动。

进一步的领域干预实验（Table 1）验证了这一解耦的可控性：在数学推理任务上，使用数学领域数据训练的潜变量（MetaMathQA）始终优于代码或 QA 领域的潜变量（如 MATH500 上达 72.4），证明潜在空间确实编码了领域相关的推理策略。

### 4. 调度机制：RL 训练中的探索-利用控制

在 RL 训练阶段，方法引入**调度策略**来控制潜变量注入的比例与强度，实现从早期广泛探索到后期精细利用的平滑过渡：

$$\mathcal{I}_{\mathrm{sched}}(\theta) = \mathbb{E}_\tau \mathbb{E}_{\mathbf{q} \sim Q} [\rho(\tau) \cdot \mathcal{L}_{\mathrm{PPO}}(\theta; \mathbf{q}, \mathbf{z}) + (1-\rho(\tau)) \cdot \mathcal{L}_{\mathrm{PPO}}(\theta; \mathbf{q})]$$

其中 $\rho(\tau)$ 按训练进度 $\tau$ 动态调节潜在引导响应与标准响应的混合比例。实验表明，线性衰减调度相比双阶段调度在最终平均性能上有 +0.75 点的额外提升，暗示平滑过渡更有利于收敛。

### 5. Changed Slots 总结

| 变更维度 | 基线方案 | 本方法方案 |
|---------|---------|-----------|
| **输入表示** | 仅由提示 token 嵌入构成 | 前置由 VAE 解码器从潜变量 z 生成的可学习前缀嵌入序列 |
| **推理策略采样** | token 级随机解码（温度/核采样） | 生成前对潜变量 z ∼ N(0,I) 采样，选择不同策略模式 |
| **RL 探索控制** | 固定解码策略（仅熵正则化） | 双阶段/线性衰减调度，动态调节潜变量注入比例 |

这种从 token 级到策略级的探索范式转换，使得 RL 训练能够访问到更丰富的高层推理行为。训练曲线（Figure 6）清晰地展示了这一机制的效果：潜在引导变体在训练早期因探索更广泛的策略空间而准确率增长较慢，但在后期逐渐超越 GRPO 基线，体现了“先广泛探索、后精准利用”的学习动态。

## 整体框架

Reasoning Palette 的核心思想是将推理过程中的探索从 **token 级随机性** 提升为 **策略级结构化采样**。框架通过一个随机潜在变量在生成开始前调节模型的内部推理策略，使模型能够访问更丰富的高层级推理行为，而非仅依赖温度采样或核采样产生的表层差异。

### 框架总览

整个框架由四个关键模块串联构成，形成“潜在空间学习 → 模型适应 → 潜在引导推理 → 调度驱动的强化学习训练”的完整流水线。Figure 2 给出了框架的宏观示意：(a) 通过变分自编码器（VAE）在问答对数据上学习推理策略的潜在空间；(b) 在推理时从该潜在空间采样，解码为可学习的 token 前缀并前置插入到输入提示中，从而在生成开始前引导模型的内部规划。

![[assets/figures/papers/paper_list_l2577_https_arxiv_org_abs_2512_17206/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the Reasoning Palette framework: a latent-modulation system that enables strategic, diverse reasoning in LLMs/VLMs by sampling and decoding contextual latent variables to guide internal planning before token generation*

### 模块关系与数据流

1. **变分自编码器（VAE）训练模块**  
   在多样化的问答对数据集上训练 VAE，将问题-答案对的上下文嵌入映射到一个结构化的潜在空间。该空间的每个采样点编码了一种高层推理策略模式（如探索性推理、保守推理等），为后续的策略级采样提供基础。

2. **监督微调（SFT）适应模块**  
   采用极轻量的 SFT（仅 10 步迭代，前缀长度固定为 $L=1$），使用从先验分布 $p(\mathbf{z}) = \mathcal{N}(0, I)$ 采样的潜变量生成前缀，使基础模型适配潜在条件输入。这一步骤使模型“感知”到前缀的存在及其对生成行为的调节作用。

3. **潜在引导推理模块**  
   在推理阶段，从先验分布随机采样潜变量 $\mathbf{z}$，通过 VAE 解码器 $D_\psi$ 生成 $L$ 个前缀嵌入 $\mathbf{p_z} \in \mathbb{R}^{L \times d}$，并将其与原始提示嵌入拼接：$\tilde{\mathbf{q}} = [\mathbf{p_z}; \mathcal{E}(\mathbf{q})]$。随后，模型基于拼接后的输入进行自回归生成。该模块的关键特性在于：即使每个候选响应均采用贪心解码，仅通过潜变量空间的随机采样即可获得策略层面的多样性。

4. **调度驱动的潜在 RL 训练模块**  
   在强化学习训练（如 GRPO 或 RLOO）中，根据训练进度 $\tau$ 动态调节潜变量注入的比例 $\rho(\tau)$。具体而言，采用“双阶段”或“线性衰减”调度策略：训练早期以较高比例注入潜在前缀以促进探索，后期逐步减少注入比例以转向利用。调度目标函数为：
   $$\mathcal{I}_{\mathrm{sched}}(\theta) = \mathbb{E}_\tau \mathbb{E}_{\mathbf{q} \sim Q} [\rho(\tau) \cdot \mathcal{L}_{\mathrm{PPO}}(\theta; \mathbf{q}, \mathbf{z}) + (1-\rho(\tau)) \cdot \mathcal{L}_{\mathrm{PPO}}(\theta; \mathbf{q})]$$
   该设计实现了探索-利用的平滑过渡，使模型在训练初期充分探索多样化的推理路径，在后期收敛到高性能策略。

### 输入输出流总结

- **输入**：原始问题 $\mathbf{q}$（对于 VLM 任务，视觉输入 $\mathbf{v}$ 经视觉编码器 $f_v$ 编码后与文本提示拼接）。
- **潜在采样**：从标准高斯先验 $p(\mathbf{z})$ 采样潜变量 $\mathbf{z}$。
- **前缀生成**：VAE 解码器将 $\mathbf{z}$ 解码为前缀嵌入序列 $\mathbf{p_z}$。
- **条件化生成**：前缀嵌入与提示嵌入拼接后送入策略模型 $\pi_\theta$，自回归生成输出 $\mathbf{o}$。
- **调度控制**：在 RL 训练中，调度器决定每条响应的生成是否注入潜在前缀，控制组内响应的策略多样性。

这一流水线将探索从 token 级随机性解耦出来，转化为生成前的策略空间采样，使得模型在 RL 训练中能够访问到更丰富的高层级推理行为，从而显著提升探索效率与最终性能。

## 核心模块与公式推导

Reasoning Palette 的核心由四个模块构成，分别负责潜在空间构建、模型适应、推理引导与RL探索控制。

### 变分自编码器（VAE）训练模块

该模块的目标是从问答对中学习一个结构化的推理策略潜在空间。给定问答对 $(q, o)$，首先通过均值池化获得上下文摘要向量：

$$h = \frac{1}{N} \sum_{i=1}^N \mathcal{E}([q; o]_i) \in \mathbb{R}^d$$

其中 $\mathcal{E}$ 为基础模型的嵌入层。VAE的编码器 $q_\phi(\mathbf{z}|\mathbf{h})$ 将 $h$ 映射为潜在变量 $\mathbf{z}$，解码器则从 $\mathbf{z}$ 重建 $h$。训练目标为证据下界（ELBO）：

$$\mathcal{L}^{\mathrm{vAE}} = \mathbb{E}_{\mathbf{z} \sim q_\phi(\mathbf{z}|\mathbf{h})} [\|\mathbf{h} - \hat{\mathbf{h}}\|^2] + \beta \cdot \mathrm{KL}(q_\phi(\mathbf{z}\mid\mathbf{h}) \| p(\mathbf{z}))$$

其中第一项为均方误差重建损失，第二项为编码分布与先验 $p(\mathbf{z}) = \mathcal{N}(0, I)$ 之间的KL散度，$\beta$ 控制正则化强度。训练完成后，从先验中采样即可获得编码不同推理策略的潜在变量。

### 前缀解码与潜在条件化输入

推理时，从先验采样 $L$ 个独立潜在变量，经解码器 $D_\psi$ 生成前缀嵌入序列：

$$\mathbf{p_z} = (D_\psi(\mathbf{z}^{(1)}), D_\psi(\mathbf{z}^{(2)}), \dots, D_\psi(\mathbf{z}^{(L)})) \in \mathbb{R}^{L \times d}$$

该前缀嵌入与原始提示嵌入拼接，形成潜在条件化输入：

$$\tilde{\mathbf{q}} = [\mathbf{p_z}; \mathcal{E}(\mathbf{q})], \quad \mathbf{o} \sim \pi_\theta(\cdot \mid \tilde{\mathbf{q}})$$

其中 $\pi_\theta$ 为自回归生成策略。在SFT适应阶段，前缀长度固定为 $L=1$，仅使用单个可学习token调节行为；推理与RL阶段则可自由增加至 $L=4$ 或 $L=8$，以提供更丰富的组合式引导。

### 监督微调（SFT）适应模块

该模块执行轻量级适应（10步迭代），使基础模型感知潜在条件信号。训练时从先验采样 $\mathbf{z}$，解码为前缀并拼接至提示前，模型学习在前缀引导下生成高质量回答。此步骤为后续RL训练中的潜在引导奠定基础。

### 调度驱动的潜在RL训练模块

在RL训练中，Reasoning Palette 通过调度策略控制潜在前缀的注入比例，实现探索-利用的平滑过渡。调度目标函数为：

$$\mathcal{I}_{\mathrm{sched}}(\theta) = \mathbb{E}_\tau \mathbb{E}_{\mathbf{q} \sim Q} [\rho(\tau) \cdot \mathcal{L}_{\mathrm{PPO}}(\theta; \mathbf{q}, \mathbf{z}) + (1-\rho(\tau)) \cdot \mathcal{L}_{\mathrm{PPO}}(\theta; \mathbf{q})]$$

其中 $\tau$ 为训练进度，$\rho(\tau)$ 为调度函数。在每个GRPO组内采样时，以概率 $\rho(\tau)$ 使用潜在前缀引导的响应，其余为标准响应。论文设计了两种调度策略：**双阶段调度**（前期高探索、后期高利用）与**线性衰减调度**（$\rho$ 随训练线性下降）。消融实验表明，线性衰减调度在最终平均性能上略优于双阶段调度（+0.75点），说明平滑过渡更有利于最终收敛。

### 公式变量汇总

| 符号 | 含义 |
|------|------|
| $h$ | 问答对的均值池化嵌入，作为VAE输入 |
| $\mathbf{z}$ | 潜在变量，从先验 $\mathcal{N}(0,I)$ 采样 |
| $q_\phi$ | VAE编码器，输出潜在分布参数 |
| $D_\psi$ | VAE解码器，将潜在变量映射为前缀嵌入 |
| $\beta$ | KL散度正则化系数 |
| $L$ | 前缀长度（token数量） |
| $\mathbf{p_z}$ | 解码后的前缀嵌入序列 |
| $\tilde{\mathbf{q}}$ | 拼接前缀后的潜在条件化输入 |
| $\rho(\tau)$ | 训练进度 $\tau$ 处的调度比例 |
| $\mathcal{L}_{\mathrm{PPO}}$ | PPO裁剪目标函数 |

### 补充图表

![[assets/figures/papers/paper_list_l2577_https_arxiv_org_abs_2512_17206/figures/001_Figure_1.jpg]]
*Figure 1: Motivation: Injecting a Gaussian noise token embedding before the prompt embeddings of Qwen-4B-Base enables substantial gains in pass@k accuracy by merely sampling in the Gaussian, despite using greedy decoding for each candidate*

![[assets/figures/papers/paper_list_l2577_https_arxiv_org_abs_2512_17206/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of the learned latent space and generated prefix embeddings via PCA and t-SNE. Left two panels: projections of decoded prefix embeddings*

## 实验与分析

### 核心发现：从token级随机到策略级采样的性能跃迁

Reasoning Palette 的核心主张是：将探索从 token 级随机性转化为生成前的策略级结构化采样，能够显著提升模型在复杂推理任务上的表现。实验从两个维度验证了这一主张——视觉语言模型（VLM）的指代表达理解，以及大语言模型（LLM）的数学推理强化学习训练。

在 VLM 指代表达理解任务上，潜在引导的效果尤为突出。仅使用贪心解码的潜在引导在 RefCOCO 上即达到 72.07 Pass@32，而依赖 token 级随机采样的基线仅为 65.07；当潜在引导与随机采样结合时，性能进一步提升至 87.53（Table 2）。这一差距在 RefCOCO+ 和 RefCOCOg 上同样稳定复现，表明结构化采样带来的增益独立于、且可叠加于 token 级随机性之上。值得注意的是，纯贪心解码基线的 Pass@32 仅为 2.0–4.67，说明该任务对探索策略高度敏感，而潜在引导恰好提供了一种高效的结构化探索机制。

![[assets/figures/papers/paper_list_l2577_https_arxiv_org_abs_2512_17206/figures/007_Table_2.jpg]]
*Table 2: Pass@32 on referring expression comprehension*

在数学推理的 RL 训练场景中，Reasoning Palette 展现出更为系统性的优势。以 Qwen3-8B-Base + RLOO 为基础配置，引入潜在引导后平均性能提升 +3.09 点（Table 3）。增益在复杂领域尤为显著：AMC23 提升 +4.38，MinervaMath 提升 +4.29。这一结果验证了分析中的核心洞见——当 RL 训练能够访问到更丰富的高层级推理行为时，探索效率与最终性能均获得实质性提升。

![[assets/figures/papers/paper_list_l2577_https_arxiv_org_abs_2512_17206/figures/008_Table_3.jpg]]
*Table 3: Results of Math reasoning over different model sizes. Bold denotes the best results*

### 调度策略：探索-利用的平滑过渡

Reasoning Palette 在 RL 训练中引入调度策略来控制潜在前缀的注入比例，实现从探索到利用的平滑过渡。实验对比了两种调度方案：双阶段调度与线性衰减调度。结果表明，线性衰减调度在最终平均性能上略优于双阶段调度（+0.75 点），暗示平滑过渡可能更有利于训练的最终收敛。

训练动态曲线（Figure 6）进一步揭示了潜在变体的行为特征：在训练早期，潜在引导变体的准确率增长慢于 GRPO 基线，这是因为模型需要花费更多步骤探索多样化、有时甚至是次优的推理路径；然而在训练后期，这些变体逐渐超越基线，体现了前期广泛探索所积累的策略多样性红利。这一“先慢后快”的模式与调度策略的设计初衷高度吻合。

![[assets/figures/papers/paper_list_l2577_https_arxiv_org_abs_2512_17206/figures/009_Figure_6.jpg]]
*Figure 6: Performance curves of the GRPO baseline and the proposed latent variants during training. Latent variants perform more thorough exploration in early stages of training and then shift toward exploitation in the latter stages, resulting in a performance curve that gradually overtakes baselines*

### 潜在空间的领域解耦与可控性

VAE 学习到的潜在空间是否真正编码了可区分的推理策略？Figure 3 通过 PCA 和 t-SNE 投影给出了肯定的答案：解码后的前缀嵌入与对应的潜变量均按推理领域（数学、代码、QA 等）形成清晰聚类。这表明 VAE 成功将高层推理策略解耦到潜在空间的不同区域。

这一解耦特性直接支撑了领域可控的推理干预。Table 1 展示了使用不同领域数据训练的潜变量在数学推理基准上的表现差异：数学领域潜变量（MetaMathQA）在 MATH500 上达到 72.4 Pass@8，始终优于代码或 QA 领域的潜变量。这一结果不仅验证了潜在空间的领域特异性，也为实际应用中的领域定制化推理提供了可行的操作路径。

![[assets/figures/papers/paper_list_l2577_https_arxiv_org_abs_2512_17206/figures/004_Table_1.jpg]]
*Table 1: Pass@8 results of latent-guided inference*

### 消融与公平性说明

所有 RL 训练均在统一条件下进行：每组生成 8 条响应用于优势估计，基础模型均为 Qwen3 系列架构，SFT 步骤统一为 10 步。VAE 训练数据来源公开且覆盖多样化领域，确保了实验的可比性与可复现性。潜在引导仅在贪心解码下即可大幅超越随机采样基线的消融结果，进一步排除了 token 级随机性对增益的混淆解释。

### 补充图表

![[assets/figures/papers/paper_list_l2577_https_arxiv_org_abs_2512_17206/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative results on RefCOCO dataset. From left to right: input image with the ground-truth bounding box, prediction from Qwen2.5VL-3B (greedy decoding), and prediction from our method, Qwen2.5VL-3B (greedy decoding) with a randomly sampled latent. The referring expressions for the top and bottom rows are train closest to the bottom and a zebra standing behind two other zebras, with only its mane and rear showing, respectively*

## 方法谱系与知识库定位

### 1. 方法本质与核心基线的关系

**Reasoning Palette** 的核心创新在于将大语言/视觉语言模型的推理探索从 token 级随机性转向策略级结构化采样。与之形成对比的是当前主流的推理时探索范式：

- **GRPO**（Shao et al., 2024）与 **RLOO**：这两种算法均属于组相对策略优化方法，通过在同一提示下生成多条响应并计算组内相对优势来训练策略。它们的探索完全依赖解码阶段的 token 级随机性（温度采样、核采样等），这往往产生表层不同但策略相近的推理路径，导致高层次推理策略多样性不足。Reasoning Palette 在 GRPO/RLOO 的基础上引入一个前置的潜在变量采样步骤，在生成开始前即确定推理策略模式，从而将探索从 token 级提升到策略级。

- **贪心解码基线** 与 **基于采样的解码基线**：在 VLM 指代表达理解任务中，标准贪心解码几乎无法产生正确结果（RefCOCO 上 Pass@32 仅为 2.0），而加入 token 级随机采样后虽有提升（65.07），但仍远低于潜在引导方案。Reasoning Palette 在仅使用贪心解码的情况下（即完全不依赖 token 级随机性）即可达到 72.07，验证了策略级结构化采样的独立增益。

### 2. 方法谱系定位

从方法论角度，Reasoning Palette 处于以下几条研究脉络的交汇点：

**（1）潜在变量引导生成**  
在文本生成中引入潜在变量以控制风格、内容或结构并非全新思路，但此前的工作多将潜在变量用于控制表层文本属性（如情感、主题），而 Reasoning Palette 首次将其用于调节深层推理策略。其 VAE 在问答对数据集上学习到的潜在空间，经 PCA 和 t-SNE 可视化证实按推理领域形成清晰聚类（Figure 3），表明潜变量成功解耦了高层推理策略，而非简单的表层特征。

**（2）前缀微调与软提示**  
在输入序列前拼接可学习的连续嵌入作为“软提示”是参数高效微调的常见做法。Reasoning Palette 的前缀机制在形式上与此类似，但关键区别在于：前缀并非静态学习，而是由 VAE 解码器从采样的潜在变量动态生成，从而实现了推理策略的可控采样。SFT 适应阶段仅需 10 步训练即可使基础模型适配潜在条件输入，体现了方法的轻量性。

**（3）强化学习中的探索-利用权衡**  
RL 训练中探索与利用的平衡是经典问题。Reasoning Palette 提出的双阶段调度和线性衰减调度策略，通过动态调节潜在前缀注入的比例 ρ(τ)，实现了从早期广泛探索到后期精细利用的平滑过渡。这种调度机制使潜在变体在训练早期虽因探索多样推理路径而准确率增长较慢，但后期持续超越 GRPO 基线（Figure 6）。

### 3. 适用边界与局限

基于现有证据，Reasoning Palette 的适用边界可归纳如下：

- **任务类型**：当前验证集中在数学推理（MATH500、GSM8K、Olympic、AMC23、MinervaMath 等）和视觉指代表达理解（RefCOCO 系列）两类任务。在更开放的推理任务（如常识推理、多跳问答）上的有效性尚未验证。

- **模型规模**：实验覆盖 Qwen-4B-Base、Qwen3-8B-Base 及 Qwen2.5VL-3B 等规模，在更大模型（如 70B+）上的扩展性需要进一步验证。

- **潜在空间质量依赖**：领域干预实验（Table 1）表明，使用数学领域数据训练的潜在空间在数学推理上显著优于代码或通用 QA 领域训练的潜在空间。这意味着方法的有效性依赖于 VAE 训练数据与目标任务领域的对齐程度——若缺乏高质量的目标领域问答对，潜在空间可能无法提供有效的策略多样性。

- **调度策略敏感度**：线性衰减调度相比双阶段调度在平均性能上有 +0.75 点的提升，说明最终性能对调度策略的选择存在一定敏感度，需要针对具体场景进行调优。

### 4. 开放问题

1. **潜在空间的可解释性**：虽然可视化显示按领域聚类，但每个潜在区域具体编码了何种推理策略（如“枚举法”、“逆向推理”、“类比推理”等）仍不明确。更深层的语义解耦分析有待开展。

2. **跨任务迁移**：VAE 学习到的潜在空间能否在不同推理任务间迁移？例如，数学推理的潜在空间是否对代码生成或逻辑推理有帮助？这涉及潜在空间的通用性边界。

3. **与推理时扩展方法的结合**：Reasoning Palette 在生成前进行策略采样，而诸如多数投票、最优-N 重排序等推理时扩展方法在生成后进行选择。两者如何协同以获得更大增益，是一个值得探索的方向。

4. **训练稳定性**：潜在引导 RL 训练在早期阶段准确率增长较慢（Figure 6），虽然最终超越基线，但训练过程中的不稳定性是否会在更大规模训练中被放大，需要更多实验证据。

## 原文 PDF

![[paperPDFs/CVPR_2026/Reasoning_Palette_Modulating_Reasoning_via_Latent_Contextualization_for_Controllable_Exploration_for_V_LMs.pdf]]
