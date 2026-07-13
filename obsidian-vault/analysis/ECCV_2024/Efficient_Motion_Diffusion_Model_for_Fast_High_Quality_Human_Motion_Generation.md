---
title: Efficient Motion Diffusion Model for Fast High Quality Human Motion Generation
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ICLR_2026/EasyTune_Efficient_Step_Aware_Fine_Tuning_for_Diffusion_Based_Motion_Generation.pdf
project_link: null
code_link: https://github.com/black-forest-labs/flux
aliases:
- EMDMFHQHMG
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 逐步感知的微调策略（Step-aware fine-tuning）：在每个去噪步骤独立计算奖励并优化，通过停止梯度（stop-gradient）操作切断递归依赖，使内存复杂度从 O(T) 降至 O(1)，同时实现密集细粒度优化。
primary_logic: 通过解耦去噪轨迹的递归梯度计算，在每一去噪步骤直接最大化中间状态的奖励，配合自改进偏好学习（SPL）训练的噪声感知奖励模型，无需人工标注即可高效微调文本驱动运动生成扩散模型。
claims:
- EasyTune 在 HumanML3D 上 FID 达到 0.132（较 MLD 的 0.473 降低 72.1%），R-Precision Top-1 提升 20.8%，MM-Dist 降低 17.5%，且仅需 DRaFT-50 约 31% 的额外内存，训练速度提升 7.3 倍。
- 理论分析（Corollary 1）和实验（Fig.3）证实现有方法的梯度中包含乘积项，随 t 增大而趋近于零，导致早期步骤优化不足；而 EasyTune 的 Corollary 2 显示 step-aware 优化消除了这种递归依赖性。
- 消融实验表明 SPL 训练的奖励模型在微调中胜率显著高于基线，且强调早期步骤的奖励重加权策略取得最佳性能，验证了早期步骤优化的重要性。
- 噪声感知奖励（Noise-Aware）比单步预测奖励（One-Step）在 ODE 模型上表现更优，进一步支持 step-aware 设计。
---

# Efficient Motion Diffusion Model for Fast High Quality Human Motion Generation

> [!tip] 核心洞察
> 通过解耦去噪轨迹的递归梯度计算，在每一去噪步骤直接最大化中间状态的奖励，配合自改进偏好学习（SPL）训练的噪声感知奖励模型，无需人工标注即可高效微调文本驱动运动生成扩散模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | 高效运动扩散模型用于快速高质量人体运动生成 |
| 英文题名 | Efficient Motion Diffusion Model for Fast High Quality Human Motion Generation |
| 会议/期刊 | ECCV 2024 |
| Links | [Code](https://github.com/black-forest-labs/flux) · [paper](https://arxiv.org/abs/2511.18927) · [paper](https://arxiv.org/abs/2602.07967) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | EasyTune |
| Dataset | HumanML3D, KIT-ML, Training Efficiency, Training Speed |

> [!tip] 效果简介
> - HumanML3D 上，FID (↓) 0.132 (EasyTune step + noise-aware) vs 0.473 (MLD pretrained) (-72.1%)；R-Precision Top-1 (↑) 0.581 (EasyTune) vs 0.481 (MLD) (+20.8%)；MM-Dist (↓) 2.637 (EasyTune noise-aware) vs 3.196 (MLD) (-17.5%)。
> - KIT-ML 上，FID (↓) 0.284 (MDM + EasyTune) vs 0.497 (MDM) (-42.9%)。
> - Training Efficiency (vs DRaFT-50) 上，Additional Memory Overhead 31.16% of DRaFT vs 100% (DRaFT-50) (-68.84%)。

## 概要

文本驱动的人体运动生成旨在根据自然语言描述合成逼真的三维人体动作序列。扩散模型在该领域取得了显著进展，但现有可微奖励微调方法面临三个根本性瓶颈：**高内存占用**（需存储完整去噪轨迹的计算图）、**稀疏粗粒度优化**（仅在轨迹末端更新一次）、以及**早期步骤梯度消失**（梯度中的乘积系数随步骤数增大而趋近于零）。这些问题严重制约了微调效率与最终生成质量。

针对上述瓶颈，本文提出 **EasyTune**，一种高效的运动扩散模型微调框架。其核心思路是**逐步感知的微调策略**（Step-aware fine-tuning）：在每个去噪步骤独立计算奖励并优化，通过停止梯度（stop-gradient）操作切断步骤间的递归依赖，使内存复杂度从 $O(T)$ 降至 $O(1)$，同时实现密集细粒度优化。配合**自改进偏好学习**（Self-refinement Preference Learning, SPL）训练的噪声感知奖励模型，EasyTune 无需人工标注即可高效微调文本驱动运动生成扩散模型。

在 HumanML3D 基准上，EasyTune 取得了 **FID 0.132**（较预训练 MLD 降低 72.1%）、**R-Precision Top-1 0.581**（提升 20.8%）、**MM-Dist 2.637**（降低 17.5%）的领先性能。同时，其额外内存开销仅为 DRaFT-50 的约 31%，训练速度提升 7.3 倍。该方法在六个不同的预训练扩散模型上均展现出良好的泛化能力，验证了逐步微调范式的普适性。

### 任务背景：文本驱动的人体运动生成

文本驱动的人体运动生成（Text-to-Motion Generation）旨在根据自然语言描述生成逼真、多样且语义对齐的 3D 人体运动序列。近年来，扩散模型（Diffusion Models）凭借其强大的生成能力成为该领域的主流范式。预训练的运动扩散模型（如 **MLD**，Chen et al., 2023）能够生成物理上合理的运动，但其语义对齐质量——即生成的运动是否准确反映文本描述的语义——仍有显著提升空间。

### 现有微调方法及其瓶颈

为提升预训练模型的语义对齐能力，研究者提出基于可微奖励的微调方法（Differentiable Reward Fine-tuning），如 **DRaFT**（Clark et al., 2024）和 **DRTune**（Wu et al., 2025）。这类方法的核心思路是：在去噪轨迹的末端（即生成干净运动 $\mathbf{x}_0^\theta$ 后）计算奖励模型 $\mathcal{R}_\phi$ 的评分，并通过整个 $T$ 步去噪过程反向传播梯度来更新模型参数。其优化目标为：

$$\mathcal{L}(\theta) = -\mathbb{E}_{c\sim\mathcal{D}_{\mathrm{T}}, \mathbf{x}_0^{\theta}\sim\pi_{\theta}(\cdot|c)}[\mathcal{R}_{\phi}(\mathbf{x}_0^{\theta}, c)]$$

然而，这种**轨迹级优化（Trajectory-level Optimization）** 策略存在三个根本性瓶颈：

**1. 高内存占用（Excessive Memory）**
去噪过程各步骤间存在递归依赖：$\mathbf{x}_{t-1}^\theta = \pi_\theta(\mathbf{x}_t^\theta, t, c)$。反向传播时，必须存储从 $t=T$ 到 $t=0$ 的完整计算图及所有中间 Jacobian，导致内存复杂度为 $O(T)$。对于典型的 50 步去噪过程，这带来了极高的 GPU 内存开销。

**2. 稀疏粗粒度优化（Sparse, Coarse-Grained Optimization）**
梯度仅在轨迹末端计算一次，模型参数的更新信号需要穿越整个去噪链才能到达早期步骤。这种“末端驱动”的优化方式使得每一步的监督信号极为稀疏，优化效率低下。

**3. 早期步骤梯度消失（Vanishing Gradient for Early Steps）**
理论分析（Corollary 1）和实验（Figure 3）均揭示了一个关键问题：现有方法的完整梯度中包含乘积项 $\prod_{s=1}^{t-1} \frac{\partial \pi_\theta}{\partial \mathbf{x}_s^\theta}$。由于每个去噪步骤的 Jacobian 矩阵 $\frac{\partial \pi_\theta(\mathbf{x}_s^\theta, s, c)}{\partial \mathbf{x}_s^\theta}$ 趋近于零，该乘积项随 $t$ 增大而急剧衰减。这意味着**早期去噪步骤（$t$ 接近 $T$）几乎接收不到有效的优化信号**——而这些步骤恰恰决定了运动的全局结构和语义布局。Figure 3 的实验数据直接证实了这一点：梯度范数在早期步骤几乎为零，优化实际上只作用于轨迹末端的少数步骤。

### 本文动机

上述分析表明，现有方法的瓶颈根源于**去噪轨迹的递归梯度依赖**。要突破这一瓶颈，需要从根本上改变优化范式：

- **解耦递归依赖**：切断步骤间的梯度传播链，使每个去噪步骤可以独立优化。
- **实现密集细粒度优化**：在每一步直接注入奖励信号，而非仅在末端进行一次粗粒度更新。
- **保持计算可行性**：在实现上述目标的同时，将内存复杂度从 $O(T)$ 降至 $O(1)$，使微调在消费级 GPU 上也可行。

此外，现有方法直接使用预训练的文本-运动检索模型（如 **ReAlign**，Weng et al., 2025；**TMR**，Petrovich et al., 2023）作为奖励模型。这些模型针对干净运动设计，无法有效评估去噪过程中的**噪声中间状态**，且缺乏对运动偏好的精细感知能力，进一步限制了微调效果。

基于以上动机，本文提出 **EasyTune**，通过**逐步感知的微调策略（Step-aware Fine-tuning）** 和**自改进偏好学习（Self-refinement Preference Learning, SPL）** 两大核心设计，系统性地解决上述问题。

## 核心方法与创新机理

EasyTune 的核心创新在于**将扩散模型的奖励微调从轨迹级（trajectory-level）重构为步骤级（step-level）**，从根本上解除了现有方法中“递归梯度依赖”这一结构性瓶颈。这一重构在两个关键维度上改变了优化范式：

### 1. 优化粒度：从轨迹级到步骤级

现有可微奖励微调方法（如 **DRaFT**，Clark et al., 2024）在整个 T 步去噪轨迹完成后，仅在末端干净运动 $\mathbf{x}_0^\theta$ 上计算一次奖励并反向传播。其损失函数为：

$$\mathcal{L}(\theta) = -\mathbb{E}_{c\sim\mathcal{D}_{\mathrm{T}}, \mathbf{x}_0^{\theta}\sim\pi_{\theta}(\cdot|c)}[\mathcal{R}_{\phi}(\mathbf{x}_0^{\theta}, c)]$$

这种设计的因果瓶颈在于：**优化信号稀疏且粗粒度**——模型仅在轨迹终点获得一次反馈，早期去噪步骤的贡献被严重稀释。

EasyTune 将优化目标重新定义为在每个去噪步骤 $t$ 上直接最大化奖励：

$$\mathcal{L}_{\mathrm{EasyTune}}(\theta) = -\mathbb{E}_{c,\mathbf{x}_t^{\theta},t}[\mathcal{R}_{\phi}(\mathbf{x}_t^{\theta}, t, c)]$$

这一改动实现了**密集的、细粒度的逐步骤优化**，使每个去噪步骤都能独立获得梯度信号。

### 2. 梯度依赖：解除递归依赖

现有方法的根本缺陷在于梯度计算中的递归依赖。完整梯度可分解为：

$$\frac{\partial\mathcal{L}(\theta)}{\partial\theta} = -\mathbb{E}[\frac{\partial\mathcal{R}_{\phi}}{\partial\mathbf{x}_0^{\theta}}\cdot\sum_{t=1}^{T}(\prod_{s=1}^{t-1}\frac{\partial\pi_{\theta}}{\partial\mathbf{x}_s^{\theta}})\frac{\partial\pi_{\theta}}{\partial\theta}]$$

其中乘积项 $\prod_{s=1}^{t-1}\frac{\partial\pi_{\theta}}{\partial\mathbf{x}_s^{\theta}}$ 随 $t$ 增大而趋近于零（**Corollary 1**，Fig.3 提供了梯度范数随步骤衰减的实验证据），导致早期步骤梯度消失。同时，计算该乘积需要存储整个 T 步的计算图，内存复杂度为 $O(T)$。

EasyTune 通过 **stop-gradient 操作**（$\mathrm{sg}(\cdot)$）切断递归依赖：

$$\mathbf{x}_{t-1}^{\theta} = \pi_{\theta}(\mathrm{sg}(\mathbf{x}_t^{\theta}), t, c)$$

这使得每一步的梯度计算仅依赖当前步骤，**内存复杂度从 $O(T)$ 降至 $O(1)$**（**Corollary 2**），同时消除了梯度消失的结构性根源。

### 3. 奖励模型：从静态检索到噪声感知偏好学习

现有方法直接使用预训练文本-运动检索模型（如 **ReAlign**，Weng et al., 2025；**TMR**，Petrovich et al., 2023）作为奖励函数，这些模型仅针对干净运动训练，无法有效评估去噪过程中的噪声中间状态。

EasyTune 引入 **自改进偏好学习（Self-refinement Preference Learning, SPL）** 机制：
- **无需人工标注**：从检索数据集的失败检索结果中动态挖掘偏好对；
- **噪声感知**：奖励模型 $\mathcal{R}_{\phi}(\mathbf{x}_t, t, c)$ 直接接受噪声运动输入，能够评估任意去噪步骤的中间状态质量；
- **偏好微调**：通过 KL 散度优化偏好预测 $\mathcal{L}_{\mathrm{SPL}}(\phi) = \mathrm{D}_{\mathrm{KL}}(\mathcal{Q}\parallel\mathcal{P})$，使奖励模型学会区分运动质量。

消融实验证实：SPL 训练的奖励模型在微调中胜率显著高于未进行偏好学习的预训练模型（Fig.8），噪声感知奖励在 ODE 模型上显著优于单步预测奖励（Tab.S11），且强调早期步骤的奖励重加权策略取得最佳性能（Tab.S4），验证了早期步骤优化的关键作用。

### 创新总结

EasyTune 的三项 changed slots 构成一个**因果闭环**：步骤级优化（slot 1）提出需求 → stop-gradient 解除递归依赖（slot 2）提供实现基础 → SPL 噪声感知奖励（slot 3）为中间步骤提供有效评估信号。三者协同使得 EasyTune 在 HumanML3D 上以 **DRaFT-50 约 31% 的额外内存**实现 **FID 降低 72.1%**（0.132 vs 0.473），训练速度提升 **7.3 倍**。

EasyTune 的整体框架围绕一个核心洞察展开：将扩散模型去噪轨迹的递归梯度依赖解耦为逐步独立的优化问题。图 Figure 2 对比了现有可微奖励微调方法与 EasyTune 的架构差异。

![[assets/figures/papers/paper_list_l1873_Efficient_Motion_Diffusion_Model_for_Fast_High_Quality_Human_Motion_Gene/figures/002_Figure_2.jpg]]
*Figure 2: The framework of existing differentiable reward-based methods (left) and our proposed EasyTune (right). Existing methods backpropagate the gradients of the reward model through the overall denoising process, resulting in (1) excessive memory, (2) inefficient, and (3) coarse-grained optimization. In contrast, EasyTune optimizes the diffusion model by directly backpropagating the gradients at each denoising step, overcoming these issues*

### 现有方法的瓶颈

现有可微奖励微调方法（如 **DRaFT** (Clark et al., 2024)、**DRTune** (Wu et al., 2025)）遵循统一的范式：在完整的 T 步去噪轨迹末端，对最终生成的干净运动 $\mathbf{x}_0^\theta$ 计算奖励值，然后通过整个轨迹反向传播梯度来更新模型参数 $\theta$。其优化目标为：

$$\mathcal{L}(\theta) = -\mathbb{E}_{c\sim\mathcal{D}_{\mathrm{T}}, \mathbf{x}_0^{\theta}\sim\pi_{\theta}(\cdot|c)}[\mathcal{R}_{\phi}(\mathbf{x}_0^{\theta}, c)]$$

这一设计导致三个关键瓶颈：

1. **高内存占用**：需要存储完整 T 步的计算图，内存复杂度为 $O(T)$。
2. **稀疏粗粒度优化**：仅在轨迹末端更新一次参数，中间步骤缺乏直接监督信号。
3. **早期步骤梯度消失**：梯度中包含乘积项 $\prod_{s=1}^{t-1} \frac{\partial \pi_{\theta}}{\partial \mathbf{x}_s^{\theta}}$，随着 $t$ 增大，该系数趋近于零，导致早期去噪步骤几乎得不到有效优化（理论分析见 Corollary 1，实验证据见 Figure 3）。

### EasyTune 的逐步感知微调

EasyTune 的核心创新在于将优化粒度从轨迹级（trajectory-level）下沉到步骤级（step-level）。其训练目标直接在每个去噪步骤 $t$ 最大化中间噪声状态 $\mathbf{x}_t^\theta$ 的奖励：

$$\mathcal{L}_{\mathrm{EasyTune}}(\theta) = -\mathbb{E}_{c,\mathbf{x}_t^{\theta},t}[\mathcal{R}_{\phi}(\mathbf{x}_t^{\theta}, t, c)]$$

为实现这一目标，EasyTune 在单步去噪中引入 stop-gradient 操作，切断步骤间的递归依赖：

$$\mathbf{x}_{t-1}^{\theta} = \pi_{\theta}(\mathrm{sg}(\mathbf{x}_t^{\theta}), t, c)$$

这一操作使得每一步的梯度计算仅依赖当前步的状态，无需回溯整个轨迹，从而将内存复杂度从 $O(T)$ 降至 $O(1)$（Corollary 2 理论保证，Figure 6 实验验证），同时实现了密集细粒度的逐步优化。

### 模块化 Pipeline

EasyTune 的完整 pipeline 由以下四个核心模块串联构成：

**1. 扩散去噪器（$\epsilon_\theta$）**
基于预训练文本到运动扩散模型（如 **MLD** (Chen et al., 2023)），根据当前噪声运动 $\mathbf{x}_t^\theta$ 和文本条件 $c$ 预测去噪方向。该模块是微调的目标对象。

**2. 逐步感知微调循环（Step-aware fine-tuning loop）**
在每个去噪步骤独立计算奖励梯度并更新模型参数。具体流程遵循 Algorithm 1：从随机时间步 $t$ 采样噪声运动，计算该步奖励，通过 stop-gradient 单步去噪后反向传播，循环迭代。

**3. 奖励模型（$\mathcal{R}_\phi$）**
评估运动-文本对齐质量，支持噪声输入。基础形式为运动特征与文本特征的余弦相似度：

$$\mathcal{R}_{\phi}(\mathbf{x}, c) = \mathcal{E}_{\mathrm{M}}(\mathbf{x}) \cdot \mathcal{E}_{\mathrm{T}}(c) \cdot \tau$$

针对不同扩散范式，噪声感知奖励的计算方式有所区分：ODE 模型可选用基于单步预测干净运动 $\hat{\mathbf{x}}_0$ 的奖励，SDE 和 ODE 模型均可直接评估噪声状态 $\mathbf{x}_t$ 的奖励（Eq. 12）。

**4. SPL 偏好挖掘器（SPL preference miner）**
从检索失败样本中自动挖掘偏好对，无需人工标注。具体而言，SPL 利用预训练文本-运动检索模型（如 **ReAlign** (Weng et al., 2025)）的检索结果，将正确匹配与检索失败样本构成偏好对，通过 KL 散度优化奖励模型的偏好预测能力：

$$\mathcal{L}_{\mathrm{SPL}}(\phi) = \mathrm{D}_{\mathrm{KL}}(\mathcal{Q}\parallel\mathcal{P})$$

SPL 微调后的奖励模型能够更准确地捕捉隐式偏好，且具备处理噪声运动的能力（Table 4 验证了其噪声感知优势）。

### 输入输出流

整个框架的输入为文本描述 $c$ 和随机噪声，输出为与文本语义对齐的高质量运动序列。数据流如下：文本条件 $c$ 输入扩散去噪器，在逐步感知微调循环中，每一步的噪声运动 $\mathbf{x}_t^\theta$ 同时送入奖励模型评估对齐质量，梯度信号直接用于更新去噪器参数。SPL 偏好挖掘器在独立阶段训练奖励模型，为微调循环提供高质量的奖励信号。

### 模块一：扩散去噪器 ε_θ

EasyTune 建立在预训练文本到运动扩散模型之上，核心组件为去噪网络 ε_θ。给定噪声运动 x_t、时间步 t 和文本条件 c，去噪器预测噪声方向，并通过单步去噪操作 π_θ 得到 x_{t-1}：

$$
\mathbf{x}_{t-1}^{\theta} = \pi_{\theta}(\mathbf{x}_t^{\theta}, t, c) := \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t^{\theta} - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon_{\theta}(\mathbf{x}_t^{\theta}, t, c) \right)
$$

其中 α_t、β_t、\bar{α}_t 为标准 DDPM 噪声调度参数。该模块在 EasyTune 中保持不变，仅作为被微调的基础组件。

### 模块二：Step-aware 微调循环

这是 EasyTune 的核心创新模块。现有方法在完整 T 步去噪轨迹末端计算奖励，梯度需通过整个轨迹反向传播，其完整梯度形式为：

$$
\frac{\partial\mathcal{L}(\theta)}{\partial\theta} = -\mathbb{E}\left[\frac{\partial\mathcal{R}_{\phi}}{\partial\mathbf{x}_0^{\theta}} \cdot \sum_{t=1}^{T} \left( \prod_{s=1}^{t-1} \frac{\partial\pi_{\theta}}{\partial\mathbf{x}_s^{\theta}} \right) \frac{\partial\pi_{\theta}}{\partial\theta} \right]
$$

该梯度存在三个关键瓶颈：**（1）高内存**——需存储完整 T 步计算图，内存复杂度 O(T)；**（2）稀疏优化**——仅在轨迹末端更新一次参数；**（3）梯度消失**——乘积项 ∏ ∂π_θ/∂x_s^θ 随 t 增大趋近于零（见 Figure 3 实证），导致早期步骤优化不足。

![[assets/figures/papers/paper_list_l1873_Efficient_Motion_Diffusion_Model_for_Fast_High_Quality_Human_Motion_Gene/figures/003_Figure_3.jpg]]
*Figure 3: Gradient norm with respect to denoising steps. Here, dim(·) denotes the gradient dimension. Detailed settings are provided in App. B.1*

EasyTune 通过两步设计破解上述瓶颈：

**第一步：Step-level 目标函数。** 将优化目标从轨迹末端奖励改为每个去噪步骤的奖励期望：

$$
\mathcal{L}_{\mathrm{EasyTune}}(\theta) = -\mathbb{E}_{c \sim \mathcal{D}_{\mathrm{T}}, \mathbf{x}_t^{\theta} \sim \pi_{\theta}(\cdot|c), t \sim \mathcal{U}(0,T)} \left[ \mathcal{R}_{\phi}(\mathbf{x}_t^{\theta}, t, c) \right]
$$

**第二步：Stop-gradient 解耦递归依赖。** 在每步去噪中对输入 x_t^θ 施加 stop-gradient 操作，切断与前序步骤的梯度连接：

$$
\mathbf{x}_{t-1}^{\theta} = \pi_{\theta}(\mathrm{sg}(\mathbf{x}_t^{\theta}), t, c)
$$

其中 sg(·) 表示 stop-gradient。这一操作使每步优化独立进行，内存复杂度从 O(T) 降至 O(1)（Figure 6 验证），同时实现密集细粒度更新——每个去噪步骤均产生一次参数更新。理论分析（Corollary 2）证明该设计消除了递归梯度依赖，避免了早期步骤的梯度消失问题。

### 模块三：噪声感知奖励模型 R_φ

奖励模型用于评估运动-文本对齐质量，其基础形式为运动特征与文本特征的余弦相似度：

$$
\mathcal{R}_{\phi}(\mathbf{x}, c) = \mathcal{E}_{\mathrm{M}}(\mathbf{x}) \cdot \mathcal{E}_{\mathrm{T}}(c) \cdot \tau
$$

其中 E_M 和 E_T 分别为运动和文本编码器（基于预训练检索模型 ReAlign，Weng et al., 2025），τ 为可训练温度参数。关键设计在于**噪声感知**能力——奖励模型需能评估中间噪声状态的运动质量，而非仅评估最终干净运动。针对不同采样器类型，噪声感知奖励的计算策略为：

$$
\mathcal{R}_{\phi}(\mathbf{x}_t, t, c) = \begin{cases}
\mathcal{R}_{\phi}(\hat{\mathbf{x}}_0, 0, c), & \text{仅 ODE 设定} \\
\mathcal{R}_{\phi}(\mathbf{x}_t, t, c), & \text{SDE 和 ODE 设定}
\end{cases}
$$

其中 \hat{x}_0 为从 x_t 单步预测的干净运动。消融实验（Table S11）表明，噪声感知奖励在 ODE 模型上显著优于仅评估预测干净运动的单步奖励（One-Step），验证了 step-aware 设计的必要性。

### 模块四：SPL 偏好挖掘器

Self-refinement Preference Learning (SPL) 机制用于微调奖励模型，使其具备偏好感知能力，无需人工标注。其核心流程为：从检索数据集中动态构建偏好对——将正确检索结果作为正样本（偏好），检索失败结果作为负样本（非偏好），并通过 KL 散度优化奖励模型的偏好预测：

$$
\mathcal{L}_{\mathrm{SPL}}(\phi) = \mathrm{D}_{\mathrm{KL}}(\mathcal{Q} \parallel \mathcal{P})
$$

其中 Q 为模型预测的偏好分布，P 为目标偏好分布。SPL 使奖励模型能够捕捉隐式偏好信号，在微调中的胜率显著高于未进行偏好学习的预训练模型（Figure 8），且文本-运动检索 R@1 提升 2.5%（HumanML3D，Table 4）。该模块的性能依赖于预训练检索模型质量——若初始检索模型较差，可能挖掘到错误偏好对，影响后续微调效果。

## 实验与关键发现

### 核心性能验证

EasyTune 在 HumanML3D 和 KIT-ML 两个标准基准上均实现了显著的性能提升，同时大幅降低了训练开销。

**HumanML3D 主结果**（Table 1, Table 3）：以 MLD（Chen et al., 2023）为预训练基础模型，EasyTune 将 FID 从 0.473 降至 **0.132**（降幅 72.1%），R-Precision Top-1 从 0.481 提升至 **0.581**（增幅 20.8%），MM-Dist 从 3.196 降至 **2.637**（降幅 17.5%）。与现有可微微调方法 DRaFT（Clark et al., 2024）和 DRTune（Wu et al., 2025）相比，EasyTune 在所有指标上均取得最优或次优结果，验证了 step-level 优化策略的有效性。

**KIT-ML 跨数据集泛化**（Table S3）：将 EasyTune 应用于 MDM 基础模型时，FID 从 0.497 降至 **0.284**（降幅 42.9%），表明该微调范式对不同扩散架构具有良好的泛化能力。

**训练效率**（Figure S5, Table S9）：EasyTune 的内存复杂度从现有方法的 O(T) 降至 **O(1)**，额外内存开销仅为 DRaFT-50 的 **31.16%**。在达到相同奖励水平时，训练速度提升 **7.3 倍**。Figure 6 进一步证实，EasyTune 的内存占用在去噪过程中保持恒定，而现有方法随步数线性增长。

### 消融实验

**Step-aware 优化粒度**（Table S4）：对 step-level 奖励应用线性递减权重（强调早期去噪步骤）取得最佳性能，验证了 Corollary 1 的理论分析——现有方法因乘积系数趋近于零而导致早期步骤优化不足，而 EasyTune 的 Corollary 2 消除了这种递归依赖。

**SPL 偏好学习**（Figure 8, Table 4）：使用 SPL 微调的奖励模型在微调中胜率显著高于未进行偏好学习的预训练模型，且文本-运动检索 R@1 在 HumanML3D 上提升 2.5%。Table 4 显示，SPL 训练的噪声感知奖励模型能够有效处理去噪过程中的噪声运动输入。

**噪声感知奖励**（Table S11）：噪声感知奖励（直接评估噪声状态）在 ODE-based 模型上显著优于基于单步预测的干净运动奖励，进一步支撑 step-aware 设计。

**KL 正则化**（Table S2）：添加 KL 正则化可缓解过拟合并提高多样性，但会轻微降低生成质量（FID 略有上升），表明需要在对齐精度和多样性之间权衡。

### 失败模式与局限

**Reward Hacking**：奖励模型主要侧重于语义对齐，对物理合理性感知较弱，可能导致生成语义匹配但运动不真实的序列。这是可微奖励微调方法的共性问题，需要设计兼顾语义和物理合理性的统一奖励模型。

**SPL 对初始检索模型的依赖**：SPL 的偏好对挖掘质量依赖于预训练检索模型的性能。若初始检索模型（如 ReAlign, Weng et al., 2025）质量较差，可能挖掘到错误的偏好对，影响微调效果。Table S5 显示 SPL 可提升 TMR（Petrovich et al., 2023）的检索性能，但提升幅度受限于基础模型能力。

**跨模态扩展未验证**：EasyTune 目前仅在文本到运动生成任务上验证，其逐步微调范式能否推广到图像或视频等其他扩散生成任务仍是开放问题。

### 公平性说明

所有实验均在同一硬件（NVIDIA RTX A6000 48GB）和相同的预训练基础模型上进行。奖励模型与微调目标保持一致：EasyTune 使用 SPL 训练的奖励，对比方法使用相同预训练检索模型的未微调版本。训练步数和优化器设置统一（Table S1）。

![[assets/figures/papers/paper_list_l1873_Efficient_Motion_Diffusion_Model_for_Fast_High_Quality_Human_Motion_Gene/figures/013_Table.jpg]]
*Table: S1: Hyperparameters for EasyTune and baseline methods*

### 补充图表

![[assets/figures/papers/paper_list_l1873_Efficient_Motion_Diffusion_Model_for_Fast_High_Quality_Human_Motion_Gene/figures/007_Table_1.jpg]]
*Table 1: Comparison of fine-tuning methods on HumanML3D. Arrows , , and indicate that higher, lower, and closer to real values are better. Bold and underline denote the best and second-best results. MLD baseline follows the implementation of (Dai et al., 2024)*

![[assets/figures/papers/paper_list_l1873_Efficient_Motion_Diffusion_Model_for_Fast_High_Quality_Human_Motion_Gene/figures/009_Table_3.jpg]]
*Table 3: Comparison of text-to-motion generation performance on the HumanML3D dataset*

![[assets/figures/papers/paper_list_l1873_Efficient_Motion_Diffusion_Model_for_Fast_High_Quality_Human_Motion_Gene/figures/010_Table_4.jpg]]
*Table 4: Evaluation on text-motion retrieval benchmark, HumanML3D and KIT-ML. The column “Noise” indicates whether the method can handle noisy motion from the denoised process*

![[assets/figures/papers/paper_list_l1873_Efficient_Motion_Diffusion_Model_for_Fast_High_Quality_Human_Motion_Gene/figures/011_Figure_8.jpg]]
*Figure 8: Comparison of models fine-tuned with and without SPL*

![[assets/figures/papers/paper_list_l1873_Efficient_Motion_Diffusion_Model_for_Fast_High_Quality_Human_Motion_Gene/figures/018_Table.jpg]]
*Table: S4: Ablation study on step-level reward reweighting strategies for EasyTune. The baseline is MLD*

![[assets/figures/papers/paper_list_l1873_Efficient_Motion_Diffusion_Model_for_Fast_High_Quality_Human_Motion_Gene/figures/024_Figure.jpg]]
*Figure: (a) Memory Usage for Key Stages (b) Memory Growth per Denoising Step Figure S5: Comprehensive memory analysis of EasyTune and existing fine-tuning methods. We report the memory usage of key stages (model loading, prompt encoding, denoising, VAEbased motion decoding, and reward computation with backpropagation), as well as the full memory trajectory during optimization. EasyTune achieves lower peak memory while maintaining high utilization, benefiting from the O(1) memory growth of the denoising process*

![[assets/figures/papers/paper_list_l1873_Efficient_Motion_Diffusion_Model_for_Fast_High_Quality_Human_Motion_Gene/figures/025_Table.jpg]]
*Table: S9: Computational overhead comparison. We report the training time and TFLOPs required to reach different reward scores. Total time is measured in seconds on a single NVIDIA RTX A6000 GPU. “-” indicates the method could not reach that reward level within a reasonable training budget*

![[assets/figures/papers/paper_list_l1873_Efficient_Motion_Diffusion_Model_for_Fast_High_Quality_Human_Motion_Gene/figures/014_Table.jpg]]
*Table: S2: Performance comparison between EasyTune with and without KL-regularized*

## 定位与知识库关联

### 1. 与现有微调范式的谱系关系

EasyTune 的核心贡献在于对“基于可微奖励的扩散模型微调”这一范式的梯度计算路径进行了结构性重构，而非引入全新的优化目标。其与现有工作的关系可通过三个维度定位：

**（1）从轨迹级优化到步骤级优化的粒度跃迁**

现有可微奖励微调方法，如 **DRaFT**（Clark et al., 2024）和 **DRTune**（Wu et al., 2025），均采用轨迹级（trajectory-level）优化策略：在完整的 $T$ 步去噪轨迹末端计算奖励值 $\mathcal{R}_\phi(\mathbf{x}_0^\theta, c)$，然后通过整条轨迹反向传播梯度。这一设计的根本缺陷在于，去噪步骤之间存在递归依赖（式 5 中的乘积项 $\prod_{s=1}^{t-1} \frac{\partial \pi_\theta}{\partial \mathbf{x}_s^\theta}$），导致三个连锁问题：

- **内存爆炸**：需存储完整 $T$ 步的计算图，内存复杂度为 $O(T)$；
- **优化稀疏**：仅在轨迹末端更新一次参数，中间步骤缺乏直接监督信号；
- **早期步骤梯度消失**：乘积系数随 $t$ 增大而趋近于零（见 Corollary 1 及 Figure 3 的实验验证），使得早期去噪步骤几乎无法被优化。

EasyTune 通过在每个去噪步骤独立计算奖励并优化，将优化粒度从轨迹级提升至步骤级（step-level）。关键操作是在单步去噪中引入 stop-gradient 操作（式 7：$\mathbf{x}_{t-1}^\theta = \pi_\theta(\mathrm{sg}(\mathbf{x}_t^\theta), t, c)$），切断递归依赖，使每一步的梯度计算仅依赖当前步骤的状态，内存复杂度降至 $O(1)$（Figure 6 提供了实证对比）。

**（2）与强化学习微调路线的差异**

另一类微调方法将去噪过程建模为马尔可夫决策过程（MDP），采用强化学习进行优化，代表工作包括 **DDPO**（Black et al., 2023）和 **DPOK**（Fan et al., 2023a）。这类方法避免了全轨迹反向传播的内存问题，但引入了策略梯度估计的高方差和样本效率低下的问题。EasyTune 保留了可微奖励的直接梯度优化路径，在保持低内存的同时避免了 RL 的估计方差问题，本质上是在“可微优化”与“RL 优化”之间找到了一条更高效的中间路径。

**（3）奖励模型的噪声感知能力**

现有方法大多直接使用预训练的文本-运动检索模型（如 **ReAlign**（Weng et al., 2025）或 **TMR**（Petrovich et al., 2023））作为奖励模型，这些模型仅在干净运动上训练，无法有效评估去噪过程中的噪声中间状态。EasyTune 提出的 SPL（Self-refinement Preference Learning）机制从检索失败中自动挖掘偏好对（无需人工标注），将预训练检索模型微调为噪声感知的奖励模型（式 12），使其能直接评估任意去噪步骤 $\mathbf{x}_t$ 的运动-文本对齐程度。Table 4 和 Table S11 的消融实验证实，噪声感知奖励在 ODE-based 模型上显著优于单步预测奖励。

### 2. 适用边界与前提条件

EasyTune 的有效性依赖于以下前提条件，这些条件同时界定了其适用边界：

- **预训练扩散模型的可用性**：EasyTune 是一种微调方法，需要已预训练好的文本到运动扩散模型作为基础。论文中验证的基础模型包括 **MLD**（Chen et al., 2023）和 MDM，跨模型泛化实验（Figure 1b）显示其在六种预训练模型上均有效，但性能提升幅度因基础模型质量而异。

- **预训练检索模型的质量**：SPL 机制的性能依赖于预训练文本-运动检索模型（如 ReAlign）的初始质量。若初始检索模型较差，可能挖掘到错误的偏好对，导致奖励模型训练偏差。论文未对此进行系统的质量阈值分析，这一依赖关系需要进一步验证。

- **奖励模型侧重于语义对齐**：当前奖励模型主要评估运动与文本的语义对齐，对物理合理性（如关节角度约束、足部滑动等）感知较弱。这导致 reward hacking 风险：模型可能生成语义匹配但物理上不合理的运动序列。论文在 Limitations 部分明确承认了这一局限。

- **任务模态限制**：EasyTune 目前仅在文本到运动生成任务上验证，尚未扩展到图像、视频等其他扩散生成任务。其 step-aware 微调范式在更高维数据上的可扩展性仍是开放问题。

### 3. 局限性与未解决问题

**（1）reward hacking 与物理合理性缺失**

如论文 Limitations 部分所述，奖励模型主要关注语义对齐，对物理合理性感知不足。这是当前可微奖励微调方法的共性瓶颈，而非 EasyTune 特有。解决方向可能包括：设计多目标奖励模型（同时评估语义对齐和物理约束），或在优化过程中引入物理仿真器的反馈。

**（2）stop-gradient 操作的优化偏差**

stop-gradient 操作切断了递归依赖，但也引入了优化偏差：每一步的梯度仅反映当前步骤的局部奖励，忽略了步骤间的长期依赖关系。论文的 Corollary 2 证明了这种解耦在数学上的合理性，但未讨论其在更复杂生成架构（如级联扩散模型、非马尔可夫去噪过程）中的收敛性保证。这一理论问题需要进一步分析。

**（3）SPL 的扩展性与在线学习**

SPL 目前采用离线方式从检索数据集中挖掘偏好对。在大规模多模态数据场景下，如何设计在线偏好对挖掘机制，以及如何避免偏好对质量随模型更新而退化，是尚未解决的问题。

**（4）跨任务泛化**

EasyTune 的 step-aware 微调范式在理论上不限于运动生成，但其在图像、视频、音频等模态的扩散模型上的适用性尚未验证。不同模态的去噪动态特性（如噪声调度、去噪步数）可能影响 step-aware 优化的效果。

### 4. 开放研究问题

基于上述分析，EasyTune 开启或未能解决的开放问题包括：

1. **统一奖励模型设计**：如何设计同时兼顾语义对齐和物理合理性的统一奖励模型？多目标优化或约束优化的引入是否会破坏 step-aware 微调的内存效率优势？

2. **跨模态范式迁移**：EasyTune 的逐步微调范式能否推广到其他基于扩散的生成任务（如图像、视频、3D 生成）？不同模态的去噪轨迹特性对 step-aware 优化有何影响？

3. **SPL 的在线扩展**：SPL 的偏好对挖掘机制能否从离线扩展到在线，实现微调过程中奖励模型的持续自改进？在线学习中如何保证偏好对的质量稳定性？

4. **stop-gradient 的理论收敛性**：stop-gradient 操作在更复杂的扩散架构（如非马尔可夫过程、级联模型）中的收敛性保证如何？是否存在更优的递归解耦策略？

5. **奖励模型与生成模型的协同进化**：当前 SPL 在微调前独立训练奖励模型，微调过程中奖励模型固定。是否可能实现奖励模型与生成模型的协同在线进化，以缓解 reward hacking 问题？

## 原文 PDF

![[paperPDFs/ICLR_2026/EasyTune_Efficient_Step_Aware_Fine_Tuning_for_Diffusion_Based_Motion_Generation.pdf]]
