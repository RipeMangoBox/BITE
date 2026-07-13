---
title: "VA-p: Variational Policy Alignment for Pixel-Aware Autoregressive Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VA_p_Variational_Policy_Alignment_for_Pixel_Aware_Autoregressive_Generation.pdf
project_link: null
code_link: "https://github.com/Lil-Shake/VA-Pi"
aliases:
- VA-p
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 采用变分下界（ELBO）将像素重建质量（MSE + LPIPS）作为内在奖励信号，通过GRPO策略梯度直接优化AR生成器，同时利用基于噪声上下文和下一token预测的交叉熵先验正则化保持令牌分布一致性，从而在不使用外部奖励模型和昂贵自由运行采样的前提下实现像素空间对齐。
primary_logic: 将AR生成器与tokenizer的对齐表述为变分优化问题：将离散令牌序列视为图像生成的潜变量，推导出包含像素重建项和令牌先验正则化项的ELBO；其中重建项通过teacher forcing下的解码损失转化为RL奖励，KL正则化近似为可微的噪声上下文下一token预测损失，实现在离散令牌空间中的像素感知对齐。
claims:
- 在LlamaGen-XXL上仅用1% ImageNet-1K数据和25分钟训练，FID从14.36降至7.65，IS从86.55提升至116.70（无CFG）
- 在GenEval文本到图像基准上，LlamaGen-XL整体得分从0.306提升至0.339，Janus-Pro 1B从0.725提升至0.744
- VA-π无需外部奖励模型，在文本-图像对齐指标CLIP（0.291 vs 0.274）和HPS v2（0.211 vs 0.208）上均优于使用外部奖励的AR-GRPO
- 消融研究证实像素重建奖励（MSE+LPIPS）与令牌先验正则化（交叉熵）的组合至关重要，中等噪声比（ξ=0.5）和适度正则化强度（β=0.1）性能最优
---

# VA-p: Variational Policy Alignment for Pixel-Aware Autoregressive Generation

> [!tip] 核心洞察
> 将AR生成器与tokenizer的对齐表述为变分优化问题：将离散令牌序列视为图像生成的潜变量，推导出包含像素重建项和令牌先验正则化项的ELBO；其中重建项通过teacher forcing下的解码损失转化为RL奖励，KL正则化近似为可微的噪声上下文下一token预测损失，实现在离散令牌空间中的像素感知对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | VA-π：面向像素感知自回归生成的变分策略对齐 |
| 英文题名 | VA-p: Variational Policy Alignment for Pixel-Aware Autoregressive Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Liao_VA-p_Variational_Policy_Alignment_for_Pixel-Aware_Autoregressive_Generation_CVPR_2026_paper.html) · [Code](https://github.com/Lil-Shake/VA-Pi) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VA-π |
| Dataset | ImageNet-1K class-conditional, ImageNet-1K, GenEval, Text-to-image alignment |

> [!tip] 效果简介
> - ImageNet-1K class-conditional (256×256, w/o CFG) 上，FID↓ 7.65 vs 14.36 (-6.71)。
> - ImageNet-1K (w/o CFG) 上，IS↑ 116.70 vs 86.55 (+30.15)。
> - ImageNet-1K (with CFG) 上，FID↓ 2.28 vs 2.62 (LlamaGen-XXL) (-0.34)。

## 概要

### 问题瓶颈

标准两阶段自回归（Autoregressive, AR）视觉生成管线存在一个根本性的不一致：tokenizer（编码器-量化器-解码器）的训练目标仅为像素重建，而下游AR生成器仅优化令牌序列的对数似然。这导致生成器可能产生在令牌空间高似然、但在像素空间偏离真实图像流形的“off-manifold tokens”，解码后出现伪影和视觉质量退化。这一**生成器-分词器不一致**构成了当前自回归视觉生成的核心瓶颈。

### 核心方法

VA-π（Variational Policy Alignment）将上述对齐问题形式化为一个**变分优化**框架。其核心洞察是：将离散令牌序列视为从图像生成潜变量，推导出包含像素重建项和令牌先验正则化项的**证据下界（ELBO）**。具体而言：

- **像素重建奖励**：将teacher forcing下采样的令牌序列通过冻结的解码器重建图像，以像素级MSE和LPIPS损失的负值作为内在奖励信号；
- **先验正则化**：向ground-truth令牌序列注入随机上下文噪声，通过下一token预测交叉熵损失近似KL正则化，保持令牌分布一致性；
- **策略优化**：采用GRPO（Group Relative Policy Optimization）策略梯度，基于组归一化优势和裁剪目标，在无需外部奖励模型和昂贵自由运行采样的前提下完成像素空间对齐。

### 主要结果

VA-π展现出极高的数据效率与训练效率：

- **类条件生成（ImageNet-1K 256×256）**：在LlamaGen-XXL上，仅使用**1%数据**（约1280张图像）和**25分钟训练**，无分类器引导（CFG）下FID从14.36降至**7.65**，IS从86.55提升至**116.70**；启用CFG后FID进一步降至2.28。
- **文本到图像生成（GenEval）**：LlamaGen-XL整体得分从0.306提升至**0.339**；统一多模态模型Janus-Pro 1B从0.725提升至**0.744**。
- **文本-图像对齐**：在无外部奖励模型的情况下，VA-π的CLIP得分（0.291）和HPS v2得分（0.211）均优于使用外部奖励模型优化的AR-GRPO（0.274 / 0.208），且训练计算成本节省**86.6%**。

### 方法谱系与知识库定位

VA-π处于**自回归视觉生成**与**强化学习微调**的交叉点：

- **基座模型**：以**LlamaGen**（Sun et al., 2024）作为类条件生成基线，以**Janus-Pro**作为统一多模态基线；
- **对比方法**：与**AR-GRPO**（基于外部奖励模型的GRPO微调）直接对比，验证内在像素奖励的优越性；与**STE**（Van Den Oord et al., 2017，直通估计器）对比，验证变分下界优化路径的有效性；
- **正则化灵感**：令牌先验正则化部分借鉴**reAR**（He et al., 2025）的噪声上下文鲁棒训练思想，但将其融入ELBO框架并赋予明确的KL近似角色。

VA-π的关键创新在于**将像素空间监督内化为无需外部模型的RL奖励**，并通过变分下界将重建目标与令牌建模统一为单一优化框架，为自回归视觉生成的后训练对齐提供了原则性方案。



### 两阶段自回归视觉生成的范式与隐忧

当前主流的自回归（Autoregressive, AR）视觉生成模型普遍采用两阶段范式：首先训练一个离散分词器（tokenizer），将连续图像映射为离散令牌序列；随后训练一个自回归生成器，在令牌空间中最大化序列的对数似然。这一范式在语言建模中取得了巨大成功，但在视觉生成中暴露出一个深层矛盾——**生成器与分词器之间的不一致性**。

具体而言，分词器仅基于像素重建目标（MSE + LPIPS）进行训练，其解码器被优化为从“真实图像编码得到的令牌序列”中恢复图像。然而，自回归生成器仅优化令牌似然，缺乏像素空间的直接监督。这导致一个关键问题：生成器可能产生具有高似然值、但偏离真实图像令牌分布的序列（即“离流形令牌”，off-manifold tokens）。当这些令牌被送入分词器的解码器时，解码器会将其映射到像素空间中的异常区域，产生伪影、结构失真和视觉质量退化。

Figure 1 通过核密度估计和 t-SNE 可视化直观地揭示了这一现象：基线 AR 模型生成的图像在像素空间中与真实图像分布存在显著偏移，而 VA-π 能够将生成分布重新对齐到真实图像流形附近。

### 现有对齐方案的局限性

针对上述不一致性问题，现有工作主要沿两条路径展开：

**基于强化学习的外部奖励微调（如 AR-GRPO）** 引入预训练的美学模型或图文匹配模型（如 CLIP、HPS v2）作为外部奖励信号，通过策略梯度（GRPO）对生成器进行微调。然而，这类方法存在三个根本性缺陷：（1）外部奖励模型本身可能与像素质量不完全对齐，优化其得分并不保证视觉质量的提升；（2）需要昂贵的自由运行采样（free-running rollout）来生成完整序列以计算奖励，训练计算开销巨大；（3）需额外维护一个参考模型以施加 KL 正则化，增加了存储成本。

**基于直通估计器（Straight-Through Estimator, STE）的端到端优化** 试图直接通过离散量化步骤回传梯度，但 STE 引入的偏置梯度在深层 AR 模型中会导致训练不稳定和收敛困难。

### VA-π 的核心动机：像素感知的内在对齐

VA-π 的核心洞察在于：**分词器本身已经编码了像素空间的先验知识——其解码器能够将令牌序列映射回像素空间，并计算重建质量。这一能力可以直接作为生成器的内在监督信号，无需依赖任何外部模型。**

基于这一洞察，VA-π 将生成器-分词器对齐问题形式化为一个变分优化问题：将离散令牌序列视为图像生成的潜变量，推导出包含像素重建项和令牌先验正则化项的证据下界（ELBO）。其中，像素重建项通过 teacher forcing 下的解码损失转化为内在 RL 奖励，KL 正则化项被近似为可微的噪声上下文下一令牌预测损失。这一框架在离散令牌空间中实现了像素感知的对齐，同时避免了外部奖励模型和自由运行采样的需求。

Figure 2 展示了 VA-π 的整体框架：给定参考图像及其真实令牌序列，VA-π 注入上下文噪声，让 AR 模型在 teacher forcing 下采样目标令牌，通过解码器重建图像并计算重建奖励，最后在 GRPO 框架下进行策略更新，同时保留令牌先验正则化以维持生成器的原始预测能力。



## 核心方法与创新机理

### 瓶颈洞察：生成器-分词器不一致

标准两阶段自回归视觉生成存在一个根本性瓶颈：tokenizer 仅基于像素重建目标训练（MSE + LPIPS + VQ损失），而 AR 生成器仅优化令牌序列的对数似然（MLE）。这种训练目标的割裂导致生成器可能产生高似然但偏离真实图像分布的令牌序列（off-manifold tokens），解码后出现伪影和视觉质量下降。VA-π 的核心洞察在于，**将生成器与分词器的对齐表述为变分优化问题**：将离散令牌序列视为图像生成的潜变量，推导出包含像素重建项和令牌先验正则化项的 ELBO，从而在离散令牌空间中实现像素感知对齐。

### 关键创新机制

VA-π 相对于基线方法的核心创新体现在以下五个关键维度：

**1. 训练目标：从令牌似然最大化到像素空间 ELBO 最大化**

基线方法（如 **LlamaGen**，Sun et al., 2024）仅最大化令牌序列的对数似然：

$$\theta = \underset{\theta}{\arg\max} \sum_{i=1}^{N} \log \pi_{\theta}(\mathbf{x}_i \mid \mathbf{x}_{1:i-1}) \tag{3}$$

VA-π 将其替换为最大化像素空间似然的变分下界：

$$\log p(\mathbf{I}; \theta, \psi, \phi) \geq \mathbb{E}_{q_{\phi,\theta}(\mathbf{x} \mid \mathbf{I})}\left[\log p_{\psi}(\mathbf{I} \mid \mathbf{x})\right] - \mathrm{KL}\big(q_{\phi,\theta}(\mathbf{x} \mid \mathbf{I}) \mid\mid \pi_{\theta}(\mathbf{x})\big) \tag{Eq.8}$$

这一 ELBO 将像素重建质量（期望对数似然项）和令牌分布一致性（KL 正则化项）统一在一个优化框架内，从理论上保证了生成器优化方向与像素空间真实分布对齐。

**2. 优化信号：从令牌级交叉熵到像素重建内在奖励**

基线方法仅使用令牌级交叉熵损失作为优化信号，缺乏像素空间的直接监督。VA-π 引入像素重建奖励作为内在 RL 信号：

$$R(\mathbf{x}, \mathbf{x}^*) = -\big(\mathcal{L}_{\mathrm{MSE}}(\hat{\mathbf{I}}, \mathbf{I}) + \lambda_{\mathrm{p}} \mathcal{L}_{\mathrm{p}}(\hat{\mathbf{I}}, \mathbf{I})\big) \tag{Eq.10}$$

该奖励直接度量采样令牌序列经解码器重建后与原始图像的像素级 MSE 和 LPIPS 损失，为生成器提供了与视觉质量直接相关的梯度信号。同时，令牌级先验正则化损失（交叉熵）作为约束项保留，防止策略偏离原始令牌分布：

$$\mathcal{L}_{\mathrm{prior}}(\pi_{\theta}, \mathbf{x}^*, \tilde{\mathbf{x}}^*) = -\frac{1}{N}\sum_{t=1}^{N} \log \pi_{\theta}(\mathbf{x}_t^* \mid \tilde{\mathbf{x}}_{<t}^*) \tag{Eq.9}$$

**3. 策略更新机制：从标准反向传播到 GRPO 策略梯度**

VA-π 采用 GRPO 策略梯度替代标准梯度下降。具体而言，基于 teacher forcing 采样的多个令牌序列（组大小 G）计算组归一化优势：

$$\hat{A}_i = \frac{r_i - \mathrm{mean}(\{r_j\}_{j=1}^{G})}{\mathrm{std}(\{r_j\}_{j=1}^{G})}$$

然后应用裁剪更新目标并结合先验正则化惩罚：

$$\mathcal{T}_{\mathbf{VA}\cdot\boldsymbol{\pi}}(\theta) = \mathbb{E}\left[\frac{1}{G}\sum_{i=1}^{G} \min\Bigl(\rho_i A_i, \mathrm{clip}(\rho_i, 1-\epsilon, 1+\epsilon) A_i\Bigr) - \beta \mathcal{L}_{\mathrm{prior}}(\boldsymbol{\pi}_{\theta}, \mathbf{x}^*, \tilde{\mathbf{x}}^*)\right] \tag{Eq.11}$$

这一机制的关键优势在于：通过组归一化降低奖励方差，通过裁剪防止策略突变，通过先验正则化保持令牌分布稳定性。

**4. 采样策略：消除自由运行采样的计算开销**

**AR-GRPO** 等 RL 微调方法需要昂贵的自由运行采样（free-running rollout）来生成完整令牌序列以计算奖励。VA-π 的关键简化在于：**所有奖励计算和策略更新均基于 teacher forcing 轨迹**，无需自由运行采样。这源于 ELBO 推导中变分后验 $q_{\phi,\theta}(\mathbf{x} \mid \mathbf{I})$ 的自然定义——它使用 ground-truth 前缀进行 teacher forcing 采样。这一设计使训练计算成本降低 86.6%，且无需维持独立的参考模型，无额外存储开销。

**5. 正则化：噪声上下文下一令牌预测缓解曝光偏差**

VA-π 的先验正则化采用独特的噪声上下文机制：以概率 $\xi$ 用随机令牌替换 ground-truth 序列中的令牌产生噪声上下文，然后训练下一令牌预测交叉熵损失。这一设计受 **reAR**（He et al., 2025）启发，同时近似 KL 正则化并缓解 teacher forcing 训练与自回归推理之间的曝光偏差。消融实验证实，交叉熵正则化始终优于 KL 散度，中等噪声比（$\xi=0.5$）和适度正则化强度（$\beta=0.1$）性能最优。

### 与相关方法的本质差异

| 维度 | LlamaGen（基线） | AR-GRPO | VA-π（本文） |
|------|------------------|---------|-------------|
| 优化目标 | 令牌 MLE | 外部奖励最大化 | 像素空间 ELBO |
| 奖励来源 | 无 | 外部奖励模型（CLIP/HPS） | 内在像素重建损失 |
| 采样方式 | Teacher forcing | 自由运行 rollout | 仅 Teacher forcing |
| 正则化 | 无特殊机制 | KL 参考模型约束 | 噪声上下文 CE 先验 |
| 额外开销 | 无 | 参考模型 + rollout | 无 |

VA-π 在无需外部奖励模型的前提下，在文本-图像对齐指标上仍优于使用外部奖励的 AR-GRPO（CLIP: 0.291 vs 0.274; HPS v2: 0.211 vs 0.208），验证了像素内在奖励的有效性和充分性。



VA-π 的整体设计围绕一个核心问题展开：**如何在不依赖外部奖励模型、不引入昂贵自由运行采样的前提下，将自回归（AR）生成器的输出分布与冻结分词器（tokenizer）的像素重建能力对齐**。框架将这一对齐问题形式化为变分优化，通过策略梯度方法在离散令牌空间中直接优化像素空间似然的证据下界（ELBO）。

### 模块构成与数据流

VA-π 由五个相互协作的模块组成，数据流严格限定在 teacher forcing 轨迹内，避免了传统 RL 微调中昂贵的 rollout 采样：

1. **冻结的视觉分词器（Encoder → Quantizer → Decoder）**  
   分词器在训练前已完成预训练并保持冻结。其作用是将参考图像 $\mathbf{I}$ 编码为离散令牌序列 $\mathbf{x}^* = \mathcal{Q}(\mathcal{E}(\mathbf{I}))$，同时将 AR 生成器采样得到的令牌序列 $\mathbf{x}$ 解码回像素空间 $\hat{\mathbf{I}} = \mathcal{D}(\mathbf{x})$，为奖励计算提供桥梁。

2. **AR 生成器（策略 $\pi_\theta$）**  
   生成器以 teacher forcing 模式运行：给定真实令牌前缀 $\mathbf{x}^*_{1:i-1}$（可能被噪声污染），输出下一令牌的条件分布 $\pi_\theta(\mathbf{x}_i \mid \tilde{\mathbf{x}}^*_{<i})$，并从中采样得到完整序列 $\mathbf{x}$。该序列同时用于奖励评估和策略更新，无需额外的自由运行采样。

3. **重建奖励模块**  
   将 teacher forcing 下采样得到的令牌序列 $\mathbf{x}$ 通过解码器重建为图像 $\hat{\mathbf{I}}$，计算与原始图像 $\mathbf{I}$ 的像素级 MSE 损失和感知损失 LPIPS，取负值作为内在奖励：
   $$R(\mathbf{x}, \mathbf{x}^*) = -\big(\mathcal{L}_{\mathrm{MSE}}(\hat{\mathbf{I}}, \mathbf{I}) + \lambda_{\mathrm{p}} \mathcal{L}_{\mathrm{p}}(\hat{\mathbf{I}}, \mathbf{I})\big)$$
   该奖励直接度量生成令牌序列在像素空间的重建质量，是驱动对齐的核心信号。

4. **先验正则化模块**  
   以概率 $\xi$ 将真实令牌序列 $\mathbf{x}^*$ 中的部分令牌替换为随机令牌，构造噪声上下文 $\tilde{\mathbf{x}}^*$。在此噪声上下文中计算下一令牌预测的交叉熵损失：
   $$\mathcal{L}_{\mathrm{prior}}(\pi_\theta, \mathbf{x}^*, \tilde{\mathbf{x}}^*) = -\frac{1}{N}\sum_{t=1}^{N} \log \pi_\theta(\mathbf{x}_t^* \mid \tilde{\mathbf{x}}^*_{<t})$$
   该损失近似 ELBO 中的 KL 正则化项，约束更新后的策略不偏离基础 AR 模型的令牌分布，同时缓解 teacher forcing 带来的曝光偏差。

5. **GRPO 策略更新模块**  
   对同一输入采样 $G$ 个令牌序列，计算组归一化优势 $\hat{A}_i$，应用裁剪目标更新生成器参数，同时加权先验正则化损失：
   $$\mathcal{T}_{\mathbf{VA}\cdot\boldsymbol{\pi}}(\theta) = \mathbb{E}\left[\frac{1}{G}\sum_{i=1}^{G} \min\Bigl(\rho_i A_i, \mathrm{clip}(\rho_i, 1-\epsilon, 1+\epsilon) A_i\Bigr) - \beta \mathcal{L}_{\mathrm{prior}}(\pi_\theta, \mathbf{x}^*, \tilde{\mathbf{x}}^*)\right]$$
   其中 $\rho_i = \pi_\theta(\mathbf{x}^{(i)} \mid \tilde{\mathbf{x}}^*) / \pi_{\theta_{\mathrm{old}}}(\mathbf{x}^{(i)} \mid \tilde{\mathbf{x}}^*)$ 为重要性采样比，$\beta$ 控制正则化强度。

### 关键设计选择

- **仅使用 teacher forcing 轨迹**：与 AR-GRPO 需要额外自由运行采样进行 rollout 不同，VA-π 的所有奖励和损失项均从 teacher forcing 轨迹中导出。这使训练计算成本降低约 86.6%，且无需维持独立的参考模型，无额外存储开销。
- **内在奖励替代外部奖励**：重建奖励直接来自冻结分词器的解码损失，无需训练或调用外部奖励模型。实验表明，VA-π 在文本-图像对齐指标 CLIP（0.291 vs 0.274）和 HPS v2（0.211 vs 0.208）上均优于使用外部奖励的 AR-GRPO。
- **噪声上下文正则化**：向真实令牌序列注入随机噪声构造上下文，使生成器在训练中暴露于不完美的前缀条件，从而提升推理时的鲁棒性。消融实验证实，中等噪声比 $\xi=0.5$ 和适度正则化强度 $\beta=0.1$ 性能最优。

### 与基线方法的差异

| 设计维度 | 标准 AR 训练 | AR-GRPO | VA-π |
|---------|-------------|---------|------|
| 优化目标 | 令牌级 MLE | 外部奖励最大化 | 像素空间 ELBO |
| 奖励信号 | 无 | 外部奖励模型 | 内在像素重建奖励 |
| 采样策略 | Teacher forcing | 自由运行 rollout | Teacher forcing |
| 正则化 | 无特殊正则化 | KL 参考模型约束 | 噪声上下文 CE 先验正则化 |
| 额外存储 | 无 | 需维持参考模型 | 无 |

整体而言，VA-π 通过变分下界将像素重建质量与令牌分布一致性统一在单一优化框架内，以极低的训练成本实现了生成器与分词器的像素感知对齐。

### 补充图表

![[assets/figures/papers/paper_list_l2623_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_VA_p_Variational/figures/001_Figure_1.jpg]]
*Figure 1: Pixel-Aware Alignment via VA-π. VA-π enables efficient post-training via variational policy optimization, aligning the pixel-space distribution of AR generated images with that of ground-truth images*

![[assets/figures/papers/paper_list_l2623_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_VA_p_Variational/figures/002_Figure_2.jpg]]
*Figure 2: Overview of VA-π. VA-π aligns the visual AR model with tokenizer via variational optimization. Given a reference image and its ground-truth tokens, VA-π adds context noise and lets the AR model compute logits under teacher forcing and samples target tokens. These sampled tokens are decoded back into an image, and the reconstruction reward is defined against the reference image. This reward is then used for policy updates within an RL framework such as GRPO [1]. Additionally, a likelihood regularization using cross-entropy loss between the logits and ground-truth tokens is retained to preserve the model’s original next-token prediction ability*



### 问题形式化：从令牌似然到像素似然

标准自回归图像生成器 $\pi_\theta$ 的训练目标为最大化令牌序列的对数似然：

$$ \theta = \underset{\theta}{\arg\max} \sum_{i=1}^{N} \log \pi_\theta(\mathbf{x}_i \mid \mathbf{x}_{1:i-1}) \tag{3} $$

该目标仅关注令牌级分布匹配，缺乏对解码后像素空间质量的直接监督，导致生成器可能产生高似然但偏离真实图像流形的令牌序列（off-manifold tokens），解码后出现伪影。VA-π 将对齐目标重新表述为最大化像素空间似然：

$$ \underset{\theta}{\mathrm{max}} ~ \mathbb{E}_{\mathbf{I} \sim p_{\mathrm{data}}} \left[ \log p(\mathbf{I}; \theta, \phi) \right] $$

其中 $p(\mathbf{I}; \theta, \phi)$ 表示在AR生成器参数 $\theta$ 和冻结的tokenizer解码器参数 $\phi$ 下，图像 $\mathbf{I}$ 的似然。由于直接优化该目标需要对所有令牌序列进行边缘化，计算不可行，VA-π 引入变分后验 $q_{\psi,\theta}(\mathbf{x} \mid \mathbf{I})$ 来近似真实后验 $p(\mathbf{x} \mid \mathbf{I})$：

$$ q_{\psi,\theta}(\mathbf{x} \mid \mathbf{I}) = \prod_{i=1}^{N} \pi_\theta(\mathbf{x}_i \mid \mathbf{x}^*_{1:i-1}), \quad \mathbf{x}^* = \mathcal{Q}(\mathcal{E}(\mathbf{I})) $$

该变分后验采用teacher forcing机制：以ground-truth令牌序列 $\mathbf{x}^*$ 的前缀为条件，逐token采样生成令牌序列 $\mathbf{x}$。

### 核心ELBO推导

基于上述变分后验，像素空间似然的证据下界（ELBO）可推导为：

$$ \log p(\mathbf{I}; \theta, \psi, \phi) \geq \mathbb{E}_{q_{\phi,\theta}(\mathbf{x} \mid \mathbf{I})} \left[ \log p_{\psi}(\mathbf{I} \mid \mathbf{x}) \right] - \mathrm{KL} \big( q_{\phi,\theta}(\mathbf{x} \mid \mathbf{I}) \mid\mid \pi_\theta(\mathbf{x}) \big) \tag{8} $$

该ELBO由两项构成：
- **像素重建项** $\mathbb{E}_{q_{\phi,\theta}(\mathbf{x} \mid \mathbf{I})} [\log p_{\psi}(\mathbf{I} \mid \mathbf{x})]$：衡量从采样的令牌序列解码后重建图像与原始图像的像素级保真度，直接提供像素空间监督信号。
- **令牌先验正则化项** $\mathrm{KL}(q_{\phi,\theta}(\mathbf{x} \mid \mathbf{I}) \mid\mid \pi_\theta(\mathbf{x}))$：约束更新后的策略分布不偏离原始AR生成器的令牌分布，防止灾难性遗忘。

### 先验正则化模块：噪声上下文下一token预测

直接计算KL散度在离散令牌空间上不可微，VA-π 将其近似为可微的交叉熵损失。具体而言，以概率 $\xi$ 随机替换ground-truth序列中的令牌，生成噪声上下文 $\tilde{\mathbf{x}}^*$，然后计算下一token预测的交叉熵损失：

$$ \mathcal{L}_{\mathrm{prior}}(\pi_\theta, \mathbf{x}^*, \tilde{\mathbf{x}}^*) = -\frac{1}{N} \sum_{t=1}^{N} \log \pi_\theta(\mathbf{x}_t^* \mid \tilde{\mathbf{x}}_{<t}^*) \tag{9} $$

该设计的核心机制：噪声上下文模拟了推理时的曝光偏差（exposure bias），强制生成器在部分错误的前缀条件下仍能预测正确的下一token，从而保持令牌分布的一致性。消融实验证实，交叉熵正则化在FID和IS上始终优于KL散度（Figure 4），中等正则化强度 $\beta=0.1$ 效果最优。

![[assets/figures/papers/paper_list_l2623_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_VA_p_Variational/figures/007_Figure_4.jpg]]
*Figure 4: Ablation on regularization weight (w/o cfg). CE regularization consistently outperforms KL regularization on FID and IS. Moderate CE regularization (0.1) provides the best results*

### 重建奖励模块：像素级内在奖励

ELBO中的像素重建项通过teacher forcing下的解码损失转化为RL奖励。对于采样的令牌序列 $\mathbf{x}$，冻结的tokenizer解码器将其重建为图像 $\hat{\mathbf{I}} = \mathcal{D}(\mathbf{x})$，计算与原始图像 $\mathbf{I}$ 的MSE和LPIPS损失，取负作为内在奖励：

$$ R(\mathbf{x}, \mathbf{x}^*) = -\big( \mathcal{L}_{\mathrm{MSE}}(\hat{\mathbf{I}}, \mathbf{I}) + \lambda_{\mathrm{p}} \mathcal{L}_{\mathrm{p}}(\hat{\mathbf{I}}, \mathbf{I}) \big) \tag{10} $$

该奖励直接度量像素空间重建质量，无需外部奖励模型。消融实验（Table 4）表明，同时使用MSE和LPIPS作为奖励成分对FID-IS平衡至关重要，仅使用视觉-语言奖励（无像素重建奖励）会导致生成质量和多样性显著下降。

### GRPO策略更新模块

VA-π 采用GRPO（Group Relative Policy Optimization）进行策略更新。对于每个ground-truth令牌序列，在teacher forcing下采样 $G$ 个令牌序列 $\{\mathbf{x}^{(i)}\}_{i=1}^{G}$，计算组归一化优势：

$$ \hat{A}_i = \frac{r_i - \mathrm{mean}(\{r_j\}_{j=1}^{G})}{\mathrm{std}(\{r_j\}_{j=1}^{G})} $$

其中 $r_i = R(\mathbf{x}^{(i)}, \mathbf{x}^*)$ 为各序列的重建奖励。完整的VA-π优化目标为：

$$ \mathcal{T}_{\mathbf{VA}\cdot\boldsymbol{\pi}}(\theta) = \mathbb{E} \left[ \frac{1}{G} \sum_{i=1}^{G} \min \Bigl( \rho_i A_i, \mathrm{clip}(\rho_i, 1-\epsilon, 1+\epsilon) A_i \Bigr) - \beta \mathcal{L}_{\mathrm{prior}}(\pi_\theta, \mathbf{x}^*, \tilde{\mathbf{x}}^*) \right] \tag{11} $$

其中 $\rho_i$ 为重要性采样比率，第一项为裁剪后的优势策略梯度（最大化重建奖励），第二项为加权的先验正则化损失（最小化下一token预测误差）。该设计的关键优势在于：所有项均基于teacher forcing轨迹计算，无需AR-GRPO所需的昂贵自由运行采样（rollout），节省86.6%的训练计算成本，且无需维持独立的参考模型，无额外存储开销。



## 实验与关键发现

### 核心定量结果

VA-π在类条件生成和文本到图像生成两个核心场景下均展现出显著的性能增益，且训练成本极低。

**类条件生成（ImageNet-1K 256×256）**：在无分类器引导（w/o CFG）的设置下，VA-π对LlamaGen-XXL进行仅25分钟的微调（使用约1%的ImageNet-1K数据），将FID从14.36大幅降至7.65，IS从86.55提升至116.70（Table 2）。引入CFG后，VA-π同样带来进一步提升，FID从2.62降至2.28，IS从约253提升至273.53。这一结果验证了像素空间对齐对生成图像多样性和感知质量的直接改善。

**文本到图像生成（GenEval基准）**：VA-π在LlamaGen-XL上将整体得分从0.306提升至0.339，在统一多模态模型Janus-Pro 1B上从0.725提升至0.744（Table 3）。更重要的是，VA-π在文本-图像对齐指标CLIP（0.291 vs 0.274）和HPS v2（0.211 vs 0.208）上均优于使用外部奖励模型的AR-GRPO（Table 1），而VA-π完全无需外部奖励模型，且训练计算成本节省86.6%，无额外存储开销。

### 消融分析：奖励组成与正则化机制

**像素重建奖励与令牌先验正则化的协同**：Table 4的奖励组成消融表明，同时使用像素级重建奖励（MSE+LPIPS）和令牌级先验正则化（交叉熵损失）可获得最佳的FID-IS平衡。仅使用像素奖励而缺失先验正则化，或仅使用视觉语言奖励（VL reward）替代像素奖励，均导致性能显著下降——后者直接验证了像素空间内在奖励的不可替代性。

**先验正则化的形式与强度**：Figure 4对比了交叉熵（CE）和KL散度两种正则化形式在不同权重β下的表现。CE正则化在FID和IS上一致优于KL正则化，中等强度β=0.1性能最优。这一结果支持了论文的理论设计：通过噪声上下文下的下一token预测交叉熵损失近似KL正则化，既能保持令牌分布一致性，又比直接KL散度更稳定有效。

**训练噪声比例的选择**：Table 5展示了上下文噪声比ξ在GenEval各子任务上的消融结果。中等噪声比ξ=0.5在整体得分上最佳；无噪声（ξ=0）或过高噪声均导致性能下降。这一现象揭示了先验正则化的平衡机制：适度噪声迫使生成器学习从扰动上下文中恢复正确令牌，从而缓解曝光偏差；但过高噪声会破坏有效的条件信息，损害生成质量。

### 定性分析与分布对齐

Figure 1通过核密度估计和t-SNE可视化展示了VA-π将生成图像的分布向真实图像流形对齐的效果。Figure 3的定性对比进一步显示，在类条件生成中，VA-π产生的物体结构（如汽车后视镜）比LlamaGen-XL和AR-GRPO更清晰；在文本到图像生成中，VA-π在物体组合和计数准确性上表现更强。这些定性结果与定量指标相互印证，验证了像素空间对齐对生成真实性和组合能力的系统提升。

### 补充图表

![[assets/figures/papers/paper_list_l2623_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_VA_p_Variational/figures/003_Table_1.jpg]]
*Table 1: Comparison on text–image alignment metrics. VA-π without reward model attains higher scores than AR-GRPO, even on the alignment reward that AR-GRPO itself is optimized for*

![[assets/figures/papers/paper_list_l2623_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_VA_p_Variational/figures/004_Table_2.jpg]]
*Table 2: Quantitative results on class-conditional ImageNet-1k [19]. We compare both LlamaGen-XL (775M) and LlamaGen-XXL (1.4B) models. All models are evaluated both with and without classifier-free guidance (CFG). Generated 384 × 384 images are resized to 256 × 256 for evaluation. Metrics include Frechet Inception Distance (FID), Inception Score (IS), Precision (Pre.) and Recall (Rec.). ´ “Ext. Rwd” denotes the use of external reward during reinforcement learning fine-tuning. Our proposed VA-π achieves competitive diversity (FID) and perceptual quality (IS) with substantially lower training cost. Best FID and IS results are highlighted in blue*

![[assets/figures/papers/paper_list_l2623_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_VA_p_Variational/figures/005_Table_3.jpg]]
*Table 3: Quantitative results on the GenEval benchmark. The upper block reports performance of LlamaGen-XL (T2I visual generation model), and the lower block reports Janus Pro-1B (unified multi-modal model). The abbreviation ”Ext. Rwd” denotes ”External Reward”, ”Attr. Bind.” denotes ”Attribute Binding”, ”obj.” denotes ”Object”. VA-π improves over both LlamaGen-XL [20] and AR-GRPO [1], achieving the highest overall GenEval [55] score. When applied to the unified multimodal model Janus-Pro 1B [5], VA-π further enhances fine-grained attributes, demonstrating its generalization across model architectures. Best results are highlighted in blue*

![[assets/figures/papers/paper_list_l2623_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_VA_p_Variational/figures/006_Figure_3.jpg]]
*Figure 3: Left: Qualitative comparison of C2I generation among LlamaGen-XL [20] (top), AR-GRPO [1] (middle) and VA-π (bottom) on the ImageNet-1k [19] classes. Both models use a CFG scale of 2.0. VA-π produces clearer object structures (like the car mirror) than LlamaGen-XL (top) and AR-GRPO (middle), demonstrating that pixel-space alignment encourages realistic generations. Right: Qualitative comparison of T2I generation between Janus-Pro 1B [48] and VA-π on the GenEval Benchmark [55]. Both models use a CFG scale of 5.0. VA-π produces better object combination and counting accuracy, demonstrating stronger capability*

![[assets/figures/papers/paper_list_l2623_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_VA_p_Variational/figures/008_Table_4.jpg]]
*Table 4: Ablation on reward composition (w/o CFG). We analyze the contribution of each reward component*

![[assets/figures/papers/paper_list_l2623_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_VA_p_Variational/figures/009_Table_5.jpg]]
*Table 5: Ablation on noise ratio (ξ) during training. Moderate noise ratio (0.5) achieves the best overall performance on GenEval. Abbreviations: PT (Position), CL (Color), AB (Attribute Binding), CT (Counting), SO (Single Object), TO (Two objects)*



## 定位与知识库关联

### 1. 问题定位：两阶段自回归视觉生成的核心瓶颈

VA-π 瞄准的是当前两阶段自回归（AR）视觉生成范式中的一个结构性不一致问题。该范式的标准流程为：先训练一个离散 tokenizer（如 VQ-VAE 或 VQGAN）将图像压缩为离散令牌序列，再训练一个 AR 生成器（如 LlamaGen）在令牌空间中进行下一令牌预测。然而，tokenizer 的训练目标仅为像素重建质量（MSE + LPIPS + 量化损失），而 AR 生成器的训练目标仅为最大化令牌序列的对数似然（MLE）。这种**目标函数解耦**导致了一个关键瓶颈：生成器可能产生在令牌空间具有高似然、但解码后在像素空间偏离真实图像分布的令牌序列（即 off-manifold tokens），表现为伪影、结构模糊和视觉质量退化。

VA-π 的核心洞察在于：**将生成器与 tokenizer 的对齐问题形式化为变分优化问题**，通过在像素空间直接监督 AR 生成器来弥合这一目标函数鸿沟。

### 2. 与基线方法的差异化关系

#### 2.1 相对于标准 AR 生成器（LlamaGen）

**LlamaGen**（Sun et al., 2024）是 VA-π 的直接改造对象。该模型采用标准的下一令牌预测 MLE 训练（Eq.3），仅优化令牌级交叉熵损失，完全缺乏像素空间的反馈信号。VA-π 在以下关键维度进行了根本性改造：

| 维度 | LlamaGen（基线） | VA-π（本文） |
|------|-----------------|-------------|
| 训练目标 | 最大化令牌似然（MLE） | 最大化像素空间似然的变分下界（ELBO） |
| 优化信号 | 仅令牌级交叉熵 | 像素重建奖励（MSE + LPIPS）+ 令牌先验正则化 |
| 策略更新 | 标准梯度下降 | GRPO 策略梯度 + 裁剪优势更新 |
| 正则化 | 无特殊机制 | 噪声上下文下一令牌预测交叉熵正则化 |

实验证据表明，在 **LlamaGen-XXL**（1.4B 参数）上仅使用 1% 的 ImageNet-1K 数据训练 25 分钟，VA-π 将 FID 从 14.36 降至 7.65（降幅 46.7%），IS 从 86.55 提升至 116.70（增幅 34.8%），且无需 CFG（Table 2）。在启用 CFG 的设置下，FID 进一步优化至 2.28（基线 2.62），IS 达到 273.53。

#### 2.2 相对于 AR-GRPO（基于外部奖励的 RL 微调）

**AR-GRPO** 是近期将 GRPO 策略优化应用于 AR 视觉生成的代表性方法，其核心思路是使用外部奖励模型（如 CLIP、HPS v2）来引导生成器改进文本-图像对齐。VA-π 与 AR-GRPO 的关键差异体现在三个层面：

**（1）奖励信号来源**：AR-GRPO 依赖外部预训练奖励模型，这些模型本身可能与生成任务的目标不完全一致，且引入额外的推理开销。VA-π 将 tokenizer 的 teacher-forcing 重建损失（MSE + LPIPS）直接转化为**内在奖励**，无需任何外部模型。Table 1 的结果具有决定性：VA-π 在无外部奖励模型的情况下，在文本-图像对齐指标 CLIP（0.291 vs 0.274）和 HPS v2（0.211 vs 0.208）上均优于使用外部奖励的 AR-GRPO——即在 AR-GRPO 自身优化的对齐指标上也被 VA-π 超越。

**（2）采样策略与计算效率**：AR-GRPO 需要昂贵的自由运行采样（free-running rollout）来生成完整的令牌序列以计算奖励，这导致训练计算开销巨大。VA-π 的所有项均从 teacher-forcing 轨迹中导出，完全避免了自由运行采样。论文报告 VA-π 相比 AR-GRPO **节省 86.6% 的训练计算成本**（Section 5.2）。

**（3）存储开销**：AR-GRPO 需要维持一个独立的参考模型用于 KL 正则化，VA-π 的先验正则化通过交叉熵损失直接实现，**无额外存储开销**。

#### 2.3 相对于 reAR（鲁棒性正则化）

**reAR**（He et al., 2025）提出了基于噪声上下文的 AR 生成器鲁棒性正则化方法，为 VA-π 的正则化部分提供了直接灵感。VA-π 的先验正则化模块（Eq.9）继承了 reAR 的核心思路：以概率 ξ 用随机令牌替换 ground-truth 序列中的令牌产生噪声上下文，训练下一令牌预测交叉熵损失。但 VA-π 的创新在于将该正则化嵌入到完整的变分优化框架中——它作为 ELBO 中 KL 散度项的近似，与像素重建奖励形成互补约束，而非孤立的鲁棒性训练技巧。

#### 2.4 相对于 Straight-through Estimator（STE）

**STE**（Van Den Oord et al., 2017）是处理离散潜变量梯度传播的经典方法，通过在前向传播中执行量化操作、反向传播中直接传递梯度来近似优化。论文将 STE 作为直接优化 ELBO 上限的对比方案。实验表明，VA-π 的 RL 策略梯度方法在稳定性和最终性能上均优于 STE 方案（Table 4 相关消融），这归因于 GRPO 的组归一化优势估计和裁剪更新机制能更好地处理离散令牌空间中的高方差梯度。

### 3. 方法谱系中的定位

VA-π 在方法论上处于以下研究脉络的交汇点：

- **变分自编码器（VAE）传统**：将离散令牌序列视为图像生成的潜变量，推导 ELBO 作为优化目标，继承了 VAE 的证据下界优化范式。
- **强化学习微调（RL Fine-tuning）**：采用 GRPO 策略梯度方法，将生成器视为策略，像素重建质量作为奖励，属于 RL 微调大模型的当代技术路线。
- **自回归视觉生成**：直接作用于 LlamaGen 等两阶段 AR 生成框架，解决 tokenizer-生成器不一致的特有问题。

### 4. 适用边界与局限

**（1）数据效率与泛化边界**：VA-π 在 1% 数据量（约 1280 张图像）和 25 分钟训练下取得了显著改进，但这一极低数据设置同时也意味着其改进可能主要来自对预训练模型已有能力的"解锁"而非学习新的视觉概念。在分布外类别或全新视觉概念上的泛化能力需要进一步验证。

**（2）对 tokenizer 质量的依赖**：VA-π 的像素重建奖励完全依赖于冻结的 tokenizer 解码器。若 tokenizer 本身的重建质量存在系统性缺陷（如对特定纹理或细粒度结构的表达能力不足），VA-π 无法超越 tokenizer 的信息瓶颈。

**（3）正则化强度的敏感性**：消融实验（Figure 4, Table 5）显示，先验正则化权重 β 和噪声比 ξ 的最优值分别为 0.1 和 0.5，偏离这些值会导致性能下降。这表明在实际部署中可能需要针对不同模型规模和数据分布进行调参。

**（4）多模态模型的适配**：虽然在 Janus-Pro 1B 统一多模态模型上验证了有效性（GenEval 从 0.725 提升至 0.744），但该模型本身已包含视觉理解能力，VA-π 在纯文本到图像生成模型上的改进幅度（LlamaGen-XL: 0.306→0.339）相对更显著，暗示该方法可能更适用于缓解视觉生成特有的 tokenizer-生成器不一致问题。

### 5. 开放问题

1. **更大规模模型的缩放行为**：当前实验覆盖 LlamaGen-XL（775M）和 XXL（1.4B），在更大规模（如 7B+）AR 视觉生成模型上，VA-π 的改进幅度和计算效率优势是否会保持或变化？

2. **与端到端像素生成方法的比较**：VA-π 本质上是在两阶段框架内进行对齐优化，与直接端到端像素生成方法（如扩散模型、连续自回归模型）在效率-质量权衡上的系统比较尚待开展。

3. **多轮对齐的可能性**：VA-π 当前为单轮后训练对齐，是否可以通过迭代式对齐（多次应用 VA-π 或与 tokenizer 交替微调）获得进一步改进？

4. **奖励函数的可扩展性**：当前内在奖励仅包含 MSE 和 LPIPS，是否可以整合更多像素空间质量指标（如 FID 感知损失、SSIM 等）而不破坏训练的稳定性？



## 原文 PDF

![[paperPDFs/CVPR_2026/VA_p_Variational_Policy_Alignment_for_Pixel_Aware_Autoregressive_Generation.pdf]]
