---
title: "$\\alpha$-DPO: Robust Preference Alignment for Diffusion Models via $\\alpha$ Divergence"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/alpha_DPO_Robust_Preference_Alignment_for_Diffusion_Models_via_alpha_Divergence.pdf
project_link: null
code_link: https://github.com/yangli-lab/Diffusion_alpha-DPO_ICLR2026/
aliases:
- ADRPADMAD
- "α-DPO"
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "将DPO的优化目标从前向KL散度替换为α散度，并通过动态α调度机制根据样本置信度自适应调整α值。"
primary_logic: "α散度在α<1时具有模式寻求特性，能够抑制离群点的影响，从而在噪声偏好数据下学习到更接近无噪声情况的目标分布。"
claims:
- "DPO的优化目标等价于最小化前向KL散度，这使其对噪声敏感"
- "α散度在噪声数据下学习到的分布更接近无噪声情况"
- "α-DPO在标签翻转率20%时在SDXL上HPSv2达到30.38，显著优于DPO的29.12"
- "α-DPO在Pick-a-Pic V2真实数据集上SDXL的HPSv2达到30.86，优于所有基线"
---

# $\alpha$-DPO: Robust Preference Alignment for Diffusion Models via $\alpha$ Divergence

> [!tip] 核心洞察
> α散度在α<1时具有模式寻求特性，能够抑制离群点的影响，从而在噪声偏好数据下学习到更接近无噪声情况的目标分布。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | α-DPO：基于α散度的扩散模型鲁棒偏好对齐方法 |
| 英文题名 | $\alpha$-DPO: Robust Preference Alignment for Diffusion Models via $\alpha$ Divergence |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=wqbnA6PcKr) · [GitHub](https://github.com/yangli-lab/Diffusion_alpha-DPO_ICLR2026/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | α-DPO |
| Dataset | Pick-a-Pic Test (SDXL, 标签翻转率20%), 无翻转) |

> [!tip] 效果简介
> - Pick-a-Pic Test (SDXL, 标签翻转率20%) 上，HPSv2↑ 为 30.38，对比 29.12 (DPO)，变化 +1.26。
> - Pick-a-Pic Test (SDXL, 标签翻转率20%) 上，IR↑ 为 1.001，对比 0.9424 (DPO)，变化 +0.0586。
> - Pick-a-Pic Test (SDXL, 无翻转) 上，HPSv2↑ 为 30.86，对比 29.43 (DPO)，变化 +1.43。

## 概要

该论文针对扩散模型偏好对齐中的噪声鲁棒性问题，提出了 $\alpha$-DPO 方法。其核心洞察在于：现有 Diffusion-DPO 的优化目标等价于最小化前向KL散度（Forward Kullback–Leibler divergence, FKL），而FKL的质量覆盖（mass-covering）特性使其对偏好数据中的标签翻转噪声（包括误标注和个体偏好差异）高度敏感。论文通过将优化目标替换为 $\alpha$ 散度（$\alpha$-divergence），利用其在 $\alpha < 1$ 时的模式寻求（mode-seeking）特性来抑制离群噪声样本的影响。此外，论文设计了动态 $\alpha$ 调度机制（$\alpha = \mu f(\mathbf{x}^w, \mathbf{x}^l, \mathbf{c})$），通过隐式偏好分类器 $f$ 根据样本置信度自适应调整 $\alpha$ 值。

在实验验证上，$\alpha$-DPO 在多个基准和模型骨干上均取得显著优势。在标签翻转率20%的合成噪声场景下（SDXL骨干），$\alpha$-DPO 的 HPSv2 达到 30.38，ImageReward 达到 1.001，显著优于 DPO 的 29.12 和 0.9424。在无噪声的 Pick-a-Pic V2 真实数据集上，$\alpha$-DPO 同样表现最佳（SDXL，HPSv2: 30.86，ImageReward: 1.054），且在所有基线方法中保持领先。消融实验证实了动态 $\alpha$ 调度机制的必要性（禁用后性能显著下降）。该方法与现有 DPO 变体（如 SPO）兼容，可作为即插即用模块提升其性能。人类评估（$p < 0.001$）进一步验证了 $\alpha$-DPO 在文本对齐、视觉吸引力和整体偏好上的优越性。



扩散模型在文本到图像生成领域取得了突破性进展，但如何使其生成结果与人类偏好对齐仍是核心挑战。现有的主流方法——直接偏好优化（DPO）——通过将奖励函数隐式参数化为策略比率，避免了传统RLHF中训练独立奖励模型的复杂流程。然而，DPO在真实场景中面临一个关键瓶颈：**偏好数据中普遍存在的噪声导致其性能严重退化**。

该噪声主要来源于两类：一是**误标注**，即标注者的判断错误；二是**个体偏好差异**，即不同用户对同一图像对存在截然相反的偏好。如图1所示，这两类噪声可以统一建模为**标签翻转噪声**，即偏好标签以一定概率被随机反转。当这种噪声存在时，DPO的优化目标——等价于最小化前向KL散度（Forward KL divergence）——由于其质量覆盖（mass-covering）特性，会倾向于拟合噪声数据的整体分布，而非真实偏好分布。图3的模拟实验直观展示了这一点：前向KL散度学习到的分布（蓝色）紧密贴合含噪数据，而α散度学习到的分布则更接近无噪声的真实情况。

这一缺憾的根本原因在于DPO的数学形式。原始DPO损失函数为：
$$
\mathcal{L}_{\mathrm{DPO}}(\theta) = -\mathbb{E}_{(\boldsymbol{x}_0^w, \boldsymbol{x}_0^l, c) \sim \mathcal{D}} \left[ \log \sigma \left( \beta \log \frac{p_\theta(\boldsymbol{x}_0^w|\boldsymbol{c})}{p_{\mathrm{ref}}(\boldsymbol{x}_0^w|\boldsymbol{c})} - \beta \log \frac{p_\theta(\boldsymbol{x}_0^l|\boldsymbol{c})}{p_{\mathrm{ref}}(\boldsymbol{x}_0^l|\boldsymbol{c})} \right) \right]
$$
该损失函数在扩散模型上的扩展（Diffusion-DPO）已被证明等价于最小化前向KL散度：
$$
\mathcal{L}_{\mathrm{DPO-Diffusion}} = \mathbb{E}_{\pmb{x} \sim \mathcal{D}} [ \mathbb{D}_{\mathrm{KL}} [ \bar{p}^*(\pmb{x}_{0:T}|\pmb{c}) ) || \bar{p}_\theta(\pmb{x}_{0:T}|\pmb{c}) ] ]
$$
前向KL散度的这一特性使其在应对标签翻转噪声时显得脆弱——一个被错误翻转的偏好对会以与正确对同等的权重影响优化方向，导致模型学习到偏离真实偏好的分布。

现有的一些改进方法，如Conservative DPO（cDPO，使用标签平滑）、Robust DPO（rDPO，基于噪声鲁棒损失设计）和Holder-DPO（H-DPO，利用redescending性质评估鲁棒性），虽然在一定程度上缓解了噪声问题，但都未能从根本上解决前向KL散度对噪声敏感的结构性缺陷。这些方法要么引入了额外的正则化项，要么修改了损失函数的尾部行为，但均未改变优化目标的基本散度类型。

针对这一瓶颈，本文提出了一种基于α散度的偏好对齐方法——**α-DPO**。核心洞察在于：α散度在α<1时具有**模式寻求**（mode-seeking）特性，能够有选择地忽略离群点的影响，从而在噪声偏好数据下学习到更接近无噪声情况的目标分布。具体而言，α-DPO将DPO的优化目标从前向KL散度替换为α散度：
$$
\mathcal{D}_\alpha(P||Q) = \frac{1}{\alpha(\alpha-1)} \mathbb{E}_{x \sim Q} \left[ \left( \frac{P(x)}{Q(x)} \right)^{1-\alpha} - (1-\alpha) \frac{P(x)}{Q(x)} - \alpha \right]
$$
并进一步引入了**动态α调度**机制，根据样本置信度自适应调整α值：α = μ f(x^w, x^l, c)，其中f作为一个隐式偏好分类器，其输出与样本的置信度单调相关（如图4所示）。这种设计使得模型对高置信度（低噪声）样本赋予更大的α值，利用α散度的质量覆盖特性学习更丰富的分布；对低置信度（高噪声）样本赋予更小的α值，利用模式寻求特性抑制其负面影响。



## 核心方法与创新机理

α-DPO 的核心创新在于将扩散模型偏好对齐的优化目标从**前向KL散度**替换为**α散度**，并引入**动态α调度机制**来适应数据质量。这一改变的根源在于，现有 Diffusion-DPO 的优化目标等价于最小化前向KL散度（Eq. 8: $\mathcal{L}_{\mathrm{DPO-Diffusion}} = \mathbb{E}_{\pmb{x} \sim \mathcal{D}} [ \mathbb{D}_{\mathrm{KL}} [ \bar{p}^*(\pmb{x}_{0:T}|\pmb{c}) ) || \bar{p}_\theta(\pmb{x}_{0:T}|\pmb{c}) ] ]$），而前向KL散度的“质量覆盖”特性使其对偏好数据中的标签翻转噪声（包括误标注和个体偏好差异）极其敏感。如图3所示，前向KL散度倾向于紧密拟合噪声分布，而α散度学习到的分布更接近无噪声情况。

**关键改变的Slot：**

1. **散度类型**：从**前向KL散度**（Forward KL divergence）变为**α散度**（α-divergence）。α散度在α<1时具有模式寻求特性，能够抑制离群点（噪声样本）的影响，从而在噪声偏好数据下学习到更鲁棒的分布。其损失函数形式为：
   $\mathcal{L}_{\alpha\cdot\mathrm{DPO}} = \mathbb{E}_{c \sim \mathcal{D}} \mathbb{E}_{\{x_0^w, x_0^l\} \sim p_{\mathrm{ref}}} \left[ \frac{1}{\alpha(\alpha-1)} u \cdot \left( u^{\alpha-1} - (1-\alpha) u^{-1} - \alpha \right) \right]$
   其中 $u_t(\theta)$ 定义了偏好样本与拒绝样本的对数几率差。

2. **α调度策略**：从**固定α或无α参数**变为**动态α调度**。α根据样本置信度自适应调整：$\alpha = \mu f(\mathbf{x}^w, \mathbf{x}^l, \mathbf{c})$，其中 $\mu$ 是控制α尺度的超参数，$f$ 是一个隐式偏好分类器。如图4所示，$f$ 与 $\Delta \mathrm{HPSv2}$ 分数呈现强单调相关性，因此可作为有效的内部置信度信号：当样本置信度高（即噪声较小）时分配较大的α值，反之分配较小的α值。消融实验（Table 4）表明，禁用动态α调度会导致性能显著下降（PS从22.51降至22.45，IR从1.054降至1.019）。

**证据强度说明**：上述两点改变均有明确的公式推导（Eq. 8, 9, 13）和实验验证（Figure 3, 4; Table 4）。关于α散度在α<1时的模式寻求特性是理论已知性质，论文通过图3的可视化实验验证了其在噪声数据下的有效性。动态α调度中$f$作为隐式分类器的有效性通过图4的单调相关性得到验证。



![[assets/figures/papers/iclr26_0001_wqbnA6PcKr_alpha-DPO_Robust_Preference_Alignment_for_Diffus/figures/009_Figure_5.jpg]]
*Figure 5: Top, human evaluations, our method shows superior performance over DPO on SDXL. Bottom, qualitative comparison with other baselines with models trained on Pick-a-Pic V2 Dataset*

α-DPO的整体pipeline建立在Diffusion-DPO的框架之上，核心改动是将优化目标从最小化前向KL散度替换为最小化α散度，并引入动态α调度机制。整个系统由四个关键模块构成：

**扩散模型前向/反向过程**是整个生成的基础。给定文本条件 $c$，模型通过马尔可夫链从噪声逐步生成图像 $x_0$。该过程为后续的偏好对齐提供了采样轨迹。

**α散度损失计算模块**是核心改动所在。原始Diffusion-DPO的损失函数（Eq. 7）等价于最小化前向KL散度（Eq. 8），即 $\mathcal{L}_{\mathrm{DPO-Diffusion}} = \mathbb{E}_{\mathbf{x} \sim \mathcal{D}} [ \mathbb{D}_{\mathrm{KL}} [ \bar{p}^*(\mathbf{x}_{0:T}|\mathbf{c}) || \bar{p}_\theta(\mathbf{x}_{0:T}|\mathbf{c}) ] ]$。α-DPO将其替换为α散度（Eq. 9），得到新的损失函数（Eq. 13）：

$$
\mathcal{L}_{\alpha\mathrm{-DPO}} = \mathbb{E}_{c \sim \mathcal{D}} \mathbb{E}_{\{x_0^w, x_0^l\} \sim p_{\mathrm{ref}}} \left[ \frac{1}{\alpha(\alpha-1)} u \cdot \left( u^{\alpha-1} - (1-\alpha) u^{-1} - \alpha \right) \right]
$$

其中 $u$ 是偏好样本与拒绝样本的对数几率差（Eq. 12），包含了扩散轨迹上每个时间步的噪声预测误差差异。

**动态α调度模块**根据样本置信度自适应调整α值。其机制为 $\alpha = \mu f(\mathbf{x}^w, \mathbf{x}^l, \mathbf{c})$，其中 $\mu$ 是控制α尺度的超参数，$f$ 是隐式偏好分类器。该分类器评估样本对的置信度——当样本对更可靠（噪声更少）时，$f$ 输出更高值，从而分配更大的α；反之则分配较小的α。这种自适应机制使得模型在高质量数据上更接近前向KL散度的质量覆盖特性，而在噪声数据上切换到α<1时的模式寻求特性。

**隐式偏好分类器** $f(\mathbf{x}^w, \mathbf{x}^l, \mathbf{c})$ 是动态调度的依据。实验验证（Figure 4）显示，$f$ 的输出与ΔHPSv2分数呈现强单调相关性，表明它能有效反映样本对的偏好对齐质量，从而为α的动态调整提供可靠的内部置信信号。

整个pipeline的数据流为：输入文本条件 $c$ 和偏好对 $(x^w, x^l)$ → 扩散模型采样生成轨迹 → α调度模块根据样本置信度确定当前α值 → α散度损失计算模块计算对齐损失 → 梯度更新模型参数。值得注意的是，α-DPO不引入额外计算开销，与原始DPO和其他基线方法具有相同的时间和GPU消耗（证据来自附录A.3.4）。



α-DPO 的核心改动是将扩散模型偏好对齐的优化目标从**前向KL散度**替换为 **α散度**，并引入**动态α调度**机制以自适应地处理噪声数据。以下从原始DPO的瓶颈出发，逐步推导α-DPO的损失函数与梯度形式。

### 1. 原始DPO的瓶颈：等价于前向KL散度

扩散模型的DPO（Diffusion-DPO）目标函数为：

$$\mathcal{L}_{\mathrm{DPO-Diffusion}}(\theta) = -\mathbb{E}_{(\mathbf{x}^w, \mathbf{x}^l) \sim \mathcal{D}} \log \sigma \bigg( \beta \mathbb{E}_{\mathbf{x}_{1:T}^w \sim \mathcal{P}_\theta(\mathbf{x}_{1:T}^w \mid \mathbf{x}_0^w)} \left[ \log \frac{p_\theta(\mathbf{x}_{0:T}^w)}{p_{\mathrm{ref}}(\mathbf{x}_{0:T}^w)} - \log \frac{p_\theta(\mathbf{x}_{0:T}^l)}{p_{\mathrm{ref}}(\mathbf{x}_{0:T}^l)} \right] \bigg)$$

该目标等价于最小化前向KL散度（Forward KL divergence）：

$$\mathcal{L}_{\mathrm{DPO-Diffusion}} = \mathbb{E}_{\pmb{x} \sim \mathcal{D}} [ \mathbb{D}_{\mathrm{KL}} [ \bar{p}^*(\pmb{x}_{0:T}|\pmb{c}) ) || \bar{p}_\theta(\pmb{x}_{0:T}|\pmb{c}) ] ]$$

其中 $\bar{p}^*$ 是隐含的最优分布，$\bar{p}_\theta$ 是模型分布。前向KL散度的**质量覆盖**（mass-covering）特性使其对离群点（如标签翻转噪声）极其敏感——它会努力拟合所有数据点，包括错误标注的偏好对，从而导致模型在噪声数据下性能严重下降。

### 2. α散度：鲁棒性来源

α散度是一种参数化散度族，定义如下：

$$\mathcal{D}_\alpha(P||Q) = \frac{1}{\alpha(\alpha-1)} \mathbb{E}_{x \sim Q} \left[ \left( \frac{P(x)}{Q(x)} \right)^{1-\alpha} - (1-\alpha) \frac{P(x)}{Q(x)} - \alpha \right]$$

关键性质：当 $\alpha < 1$ 时，α散度呈现**模式寻求**（mode-seeking）特性，即它会忽略低概率区域（如噪声离群点），只拟合高概率模式。这与前向KL散度的质量覆盖特性形成互补，使得α散度在噪声数据下学习到的分布更接近无噪声情况。

### 3. α-DPO损失函数

将α散度代入偏好对齐框架，得到α-DPO损失：

$$\mathcal{L}_{\alpha\text{-DPO}} = \mathbb{E}_{c \sim \mathcal{D}} \mathbb{E}_{\{x_0^w, x_0^l\} \sim p_{\mathrm{ref}}} \left[ \frac{1}{\alpha(\alpha-1)} u \cdot \left( u^{\alpha-1} - (1-\alpha) u^{-1} - \alpha \right) \right]$$

其中 $u_t(\theta)$ 是扩散轨迹中偏好样本与拒绝样本的对数几率差：

$$u_t(\theta) = \sigma \left( -\beta T \omega(\lambda_t) \left[ \|\epsilon^w - \epsilon_\theta(\mathbf{x}_t^w, t)\|_2^2 - \|\epsilon^w - \epsilon_{\mathrm{ref}}(\mathbf{x}_t^w, t)\|_2^2 - \left( \|\epsilon^l - \epsilon_\theta(\mathbf{x}_t^l, t)\|_2^2 - \|\epsilon^l - \epsilon_{\mathrm{ref}}(\mathbf{x}_t^l, t)\|_2^2 \right) \right] \right)$$

公式中的变量含义：
- $c$：文本条件（prompt）
- $x_0^w, x_0^l$：偏好对中的获胜样本和失败样本
- $p_{\mathrm{ref}}$：参考策略（通常是预训练扩散模型）
- $\beta$：KL正则化系数，控制策略偏离参考策略的程度
- $T$：扩散步数
- $\omega(\lambda_t)$：噪声水平相关的权重函数
- $\epsilon$：扩散过程中添加的高斯噪声
- $\epsilon_\theta$：模型预测的噪声
- $\epsilon_{\mathrm{ref}}$：参考模型预测的噪声

### 4. α-DPO梯度分析

α-DPO关于 $u_t$ 的梯度为：

$$\nabla_{u_t} \mathcal{L}_{\alpha\text{-DPO}} = \frac{1}{(\alpha-1)} (u_t^{\alpha-1} - 1) = \frac{1}{(1-\alpha)} \left(1 - \frac{1}{u_t^{1-\alpha}}\right)$$

梯度特性分析：
- 当 $0 < \alpha < 1$ 时，梯度关于 $u_t$ 单调递减
- 对于低置信度样本（$u_t$ 接近0.5），梯度较小，模型更新幅度小
- 对于高置信度样本（$u_t$ 接近1），梯度较大，模型更新幅度大
- 这种自适应梯度机制自动抑制噪声样本的影响，同时强化干净样本的学习

### 5. 动态α调度机制

α-DPO进一步引入动态α调度，使α值根据样本置信度自适应调整：

$$\alpha = \mu f(\mathbf{x}^w, \mathbf{x}^l, \mathbf{c})$$

其中：
- $\mu$：超参数，控制α的总体尺度
- $f(\mathbf{x}^w, \mathbf{x}^l, \mathbf{c})$：隐式偏好分类器，评估样本对的置信度

$f$ 的实际计算方式为：

$$f(\mathbf{x}^w, \mathbf{x}^l, \mathbf{c}) = \sigma \left( \beta \log \frac{p_\theta(\mathbf{x}^w|\mathbf{c})}{p_{\mathrm{ref}}(\mathbf{x}^w|\mathbf{c})} - \beta \log \frac{p_\theta(\mathbf{x}^l|\mathbf{c})}{p_{\mathrm{ref}}(\mathbf{x}^l|\mathbf{c})} \right)$$

即当前模型对偏好对的置信度分数。$f$ 与人工评分差异 $\Delta\text{HPSv2}$ 呈现强单调相关性，可作为有效的内部置信度信号。当样本置信度高（$f$ 大）时，$\alpha$ 较大，模型更倾向于模式寻求；当样本置信度低（$f$ 小）时，$\alpha$ 较小，模型更保守。

### 6. 与加权前向KL散度的区别

需要明确的是，α散度**不等价于**加权的前向KL散度。两者的生成函数不同：
- 加权前向KL散度的生成函数：$f_{\mathrm{FKL}}(u) \propto -w \cdot \log u$
- α散度的生成函数：$f_\alpha(u) \propto (u^{1-\alpha} - (1-\alpha)u - \alpha) / (\alpha(\alpha-1))$

这意味着α-DPO引入了**本质上不同的正则化机制**，而非简单的样本重加权。这种差异在高噪声条件下尤为显著。

### 7. 关键公式总结

| 公式 | 含义 | 关键变量 |
|------|------|----------|
| $\mathcal{L}_{\mathrm{DPO-Diffusion}} = \mathbb{E}[\mathbb{D}_{\mathrm{KL}}[\bar{p}^* \| \bar{p}_\theta]]$ | DPO等价于前向KL散度 | 质量覆盖 → 噪声敏感 |
| $\mathcal{D}_\alpha(P\|Q) = \frac{1}{\alpha(\alpha-1)} \mathbb{E}_Q[(\frac{P}{Q})^{1-\alpha} - (1-\alpha)\frac{P}{Q} - \alpha]$ | α散度定义 | $\alpha<1$ → 模式寻求 |
| $\mathcal{L}_{\alpha\text{-DPO}} = \mathbb{E}[\frac{1}{\alpha(\alpha-1)} u \cdot (u^{\alpha-1} - (1-\alpha)u^{-1} - \alpha)]$ | α-DPO损失 | $u$：对数几率差 |
| $\nabla_{u_t} \mathcal{L}_{\alpha\text{-DPO}} = \frac{1}{(1-\alpha)}(1 - \frac{1}{u_t^{1-\alpha}})$ | 梯度形式 | 单调递减 → 自动抑制噪声 |
| $\alpha = \mu f(\mathbf{x}^w, \mathbf{x}^l, \mathbf{c})$ | 动态α调度 | $\mu$：尺度超参；$f$：隐式分类器 |

**核心因果链**：前向KL散度的质量覆盖特性 → 噪声敏感 → 替换为α散度（$\alpha<1$的模式寻求特性） → 自动抑制离群点 → 动态α调度进一步增强自适应能力 → 在噪声偏好数据下学习到更接近无噪声情况的目标分布。



## 实验与关键发现

### 核心结果：噪声偏好下的鲁棒性

α-DPO 的核心动机是解决 DPO 在偏好数据存在噪声时性能严重下降的问题。论文通过引入标签翻转噪声（Label Flipping）来模拟真实场景中的误标注和个体偏好差异，并系统评估了方法的鲁棒性。

**合成噪声实验（标签翻转率 20%）** 是验证鲁棒性的核心基准。在 SDXL 骨干网络上，α-DPO 在 Pick-a-Pic Test 数据集上的 HPSv2 得分达到 **30.38**，显著优于 DPO 的 29.12（+1.26）；ImageReward (IR) 得分从 0.9424 提升至 1.001（+0.0586）。该优势在所有对比基线中均保持领先，包括鲁棒性变体 rDPO、cDPO 和 Holder-DPO。在 SD1.5 骨干上同样观察到一致趋势：α-DPO 的 HPSv2 为 26.69，IR 为 0.4512，均优于 DPO 的 26.02 和 0.3206。这一结果直接验证了将优化目标从前向 KL 散度替换为 α 散度的因果有效性——当 α<1 时，散度的模式寻求特性能够抑制噪声离群点对梯度更新的影响。

**真实数据集实验（Pick-a-Pic V2，无人工翻转）** 进一步验证了方法在自然分布上的泛化能力。在 SDXL 上，α-DPO 的 HPSv2 达到 **30.86**，IR 为 1.054，相比 DPO（29.43 / 0.9424）提升显著。在 PartiPrompt 和 HPSv2 基准上，α-DPO 分别达到 29.87 和 30.99，同样全面超越所有基线。值得注意的是，即使在无噪声的真实数据上，α-DPO 仍然优于 DPO，说明 α 散度引入的平衡机制（质量覆盖与模式寻求之间的权衡）在干净数据上也不会带来性能退化。

**人类评估** 提供了比自动指标更可靠的验证。Figure 5 和 Figure 7 的用户研究表明，α-DPO 在“文本对齐”、“视觉吸引力”和“整体偏好”三个维度上均显著优于 DPO 和 SDXL。统计显著性分析（Table 6）显示，α-DPO 相比 DPO 和 SDXL 的 p 值均小于 0.001，表明结果具有强统计稳健性。

### 消融研究：动态 α 调度与超参数敏感性

**动态 α 调度策略** 是方法的关键组件。Table 4 的消融实验表明，禁用动态 α 调度（即使用固定 α）会导致性能显著下降：PS 从 22.51 降至 22.45，IR 从 1.054 降至 1.019。这验证了根据样本置信度自适应调整 α 的必要性——高置信度样本获得较大 α（接近前向 KL），低置信度样本获得较小 α（模式寻求），从而在噪声抑制与信息利用之间取得平衡。


![[assets/figures/papers/iclr26_0001_wqbnA6PcKr_alpha-DPO_Robust_Preference_Alignment_for_Diffus/figures/011_Table_4.jpg]]
*Table 4: Ablation on hyperparameters µ and $\beta$ and the Dynamic α Strategy, evaluated on the Pick-a-Pic Test dataset with the fine-tuned SDXL model. (1) Effect of µ: As µ grows, model performance first increases then decreases. (2) Effect of the Dynamic α Strategy (Fixed-α): Without dynamic allocation of the α, the model performance degrades significantly. (3) Effect of dynamic α start step: the increasing of starting step slightly decrease the performance. (4) Effect of β: As β increases, model performance first increases and then decreases*

**超参数 µ 和 β 的敏感性** 呈现倒 U 型曲线。随着 µ 增大（控制 α 的尺度），模型性能先升后降；β（KL 正则化强度）同样存在最优区间。这一模式符合预期：过小的 µ 无法充分激活模式寻求特性，过大的 µ 则可能导致过度抑制有效信息。最优 µ 值需要根据数据集调整，这是方法当前的主要局限性。

**即插即用能力** 是 α-DPO 的重要设计特性。Table 5 显示，将 α-DPO 的损失函数替换 SPO 中的原始损失后，SPO 的性能得到显著提升（HPSv2 从 29.93 提升至 30.18，IR 从 0.994 提升至 1.028）。这表明 α 散度优化可以作为一种通用增强模块，独立于具体的偏好对齐框架。


![[assets/figures/papers/iclr26_0001_wqbnA6PcKr_alpha-DPO_Robust_Preference_Alignment_for_Diffus/figures/012_Table_5.jpg]]
*Table 5: Combining our α-DPO with other DPO variants. SPO∗ denotes our reimplementation results. Our α-DPO acts as a complementary component, which successfully integrates with SPO and significantly boosts its efficacy*

### 噪声鲁棒性的梯度机制分析

α-DPO 的鲁棒性来源可以通过梯度形式直接理解。其梯度为：
$$\nabla_{u_t} \mathcal{L}_{\alpha\text{-DPO}} = \frac{1}{(\alpha-1)} (u_t^{\alpha-1} - 1) = \frac{1}{(1-\alpha)} \left(1 - \frac{1}{u_t^{1-\alpha}}\right)$$
当 $0<\alpha<1$ 时，该梯度关于 $u_t$ 单调递减。这意味着对于噪声翻转样本（$u_t$ 很小），梯度幅值被有效抑制；而对于高质量偏好样本（$u_t$ 很大），梯度保持较大。这种自适应的梯度缩放机制是 DPO（梯度恒为 $1-u_t$）所不具备的，也是 α-DPO 在噪声环境下性能稳健的根本原因。

### 失败模式与局限性

尽管 α-DPO 在标签翻转率从 10% 到 40% 的范围内始终优于所有基线（Figure 6），但存在以下限制：

1. **超参数 µ 的调优成本**：最优 µ 值依赖数据集噪声特性，目前缺乏自动化的自适应机制。在附录 A.4.3 中，作者明确承认这是未来工作方向。
2. **隐式分类器 f(x^w, x^l, c) 的可靠性边界**：动态 α 调度依赖于该分类器对样本置信度的评估。在极端噪声条件下（如翻转率 > 40%），分类器本身的判别能力可能退化，导致 α 分配失效。当前实验仅覆盖到 40% 翻转率，更高噪声水平下的表现需要验证。
3. **模态泛化**：当前验证仅限扩散模型的图像生成任务。α 散度优化在文本生成或其他模态上的有效性尚未探索。

### 关键图表结论

- **Figure 3** 提供了最直观的理论验证：在前向 KL 散度下，模型倾向于覆盖噪声分布（质量覆盖特性），而 α 散度学习到的分布更接近无噪声情况。这是方法设计的核心直觉支撑。
- **Table 2 和 Table 9** 提供了最有力的定量证据，分别覆盖合成噪声和真实数据场景。α-DPO 在所有指标上均取得最优或次优结果。

![[assets/figures/papers/iclr26_0001_wqbnA6PcKr_alpha-DPO_Robust_Preference_Alignment_for_Diffus/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison with other backbones on Label Flipping dataset. The Flip rate is 20%. For more results, please refer to the Appendix. A.4.2. The best results are in highlighted bold and the second-best ones are underlined (same in the following tables)*

- **Figure 6** 展示了不同翻转率下的胜率对比，α-DPO 的曲线始终位于其他方法之上，且优势随噪声增加而扩大，验证了鲁棒性的单调增益。
- **Table 4 和 Table 5** 分别验证了动态 α 调度和即插即用能力的必要性，为方法的工程实用性提供了支撑。

### 补充图表

![[assets/figures/papers/iclr26_0001_wqbnA6PcKr_alpha-DPO_Robust_Preference_Alignment_for_Diffus/figures/003_Figure_2.jpg]]
*Figure 2: Qualitative DPO results on SDXL with different label flipping. Table 1: DPO results with different label flipping*

![[assets/figures/papers/iclr26_0001_wqbnA6PcKr_alpha-DPO_Robust_Preference_Alignment_for_Diffus/figures/008_Table_3.jpg]]
*Table 3: Comparison with other baselines with models trained on the Pick-a-Pic V2 dataset*





## 定位与知识库关联

### 基线关系与核心差异

α-DPO 直接继承自 Diffusion-DPO 框架，其根本区别在于散度类型的选择。Diffusion-DPO 的优化目标已被严格证明等价于最小化前向 KL 散度（FKL），即 $\mathcal{L}_{\mathrm{DPO-Diffusion}} = \mathbb{E}_{\mathbf{x} \sim \mathcal{D}} [ \mathbb{D}_{\mathrm{KL}} [ \bar{p}^*(\mathbf{x}_{0:T}|\mathbf{c}) || \bar{p}_\theta(\mathbf{x}_{0:T}|\mathbf{c}) ] ]$。FKL 的质量覆盖（mass-covering）特性使其在偏好数据存在标签翻转噪声时，倾向于拟合噪声分布而非真实分布，这是性能退化的根本原因（Figure 3 左图）。

α-DPO 将散度替换为 α 散度，其定义为 $\mathcal{D}_\alpha(P||Q) = \frac{1}{\alpha(\alpha-1)} \mathbb{E}_{x \sim Q} \left[ \left( \frac{P(x)}{Q(x)} \right)^{1-\alpha} - (1-\alpha) \frac{P(x)}{Q(x)} - \alpha \right]$。当 $\alpha < 1$ 时，α 散度表现出模式寻求（mode-seeking）特性，能够抑制离群点的影响。Figure 3 的对比实验清晰地展示了这一机制：在噪声数据下，FKL 学习到的分布与噪声分布高度吻合，而 α 散度学习到的分布更接近无噪声情况。

与同期鲁棒性增强方法相比，α-DPO 的因果机制更为直接。Conservative DPO (cDPO) 通过标签平滑进行正则化，Robust DPO (rDPO) 基于噪声鲁棒损失设计，Holder-DPO (H-DPO) 利用 redescending 性质评估鲁棒性——这些方法均未触及 DPO 损失函数在散度层面的噪声敏感性根源。α-DPO 则直接替换了散度类型，并在附录 A.2.2 中严格论证了 α 散度不等价于加权 FKL，表明其引入的是质上不同的正则化结构。

### 关键机制：动态 α 调度

α-DPO 的第二个关键设计是动态 α 调度策略。其核心公式为 $\alpha = \mu f(\mathbf{x}^w, \mathbf{x}^l, \mathbf{c})$，其中 $f$ 是一个隐式偏好分类器，其输出与 $\Delta\mathrm{HPSv2}$ 分数呈强单调相关（Figure 4）。这一设计的因果逻辑是：当样本置信度高（$f$ 值大）时，分配较大的 $\alpha$，使优化更接近模式寻求模式；当样本可能被翻转时，$\alpha$ 自动减小，降低损失函数对噪声样本的敏感度。消融实验（Table 4）证实，禁用动态调度后，模型性能显著下降（PS 从 22.51 降至 22.45，IR 从 1.054 降至 1.019），证明该机制是 α-DPO 性能提升的必要条件。

### 适用边界与证据强度

α-DPO 的鲁棒性优势在标签翻转率 10%–40% 的范围内均得到验证（Tables 2, 10–12），且在无翻转的真实数据集（Pick-a-Pic V2）上同样优于所有基线（Table 9: SDXL HPSv2 30.86 vs. DPO 29.43）。其作为即插即用模块的能力在 Table 5 中得到初步验证：与 SPO 集成后显著提升了后者的效果。然而，该集成策略仍较为初步，缺乏理论化的融合框架。

### 局限与开放问题

**已知局限：**
1. 引入额外超参数 $\mu$，其最优值需根据数据集调整（Table 4 显示 $\mu$ 过大或过小均导致性能下降）。
2. 动态调度依赖隐式分类器 $f$ 的可靠性，在极端噪声条件下该分类器可能失效——这一边界条件在论文中未被量化分析。
3. 当前验证仅限于扩散模型的图像生成任务，在文本生成或其他模态上的泛化能力尚未验证。

**开放问题：**
1. 如何设计自动化或自适应机制来调整 $\mu$？当前 $\mu$ 的调优依赖人工网格搜索，限制了方法的易用性。
2. α 散度在 $\alpha < 1$ 时的模式寻求特性是否在所有噪声类型下都优于 FKL？论文仅验证了标签翻转噪声，对偏好标注中的其他噪声类型（如模糊偏好、标注者偏差）的鲁棒性尚不清楚。
3. 动态 α 调度能否推广到其他基于散度的优化框架（如 RLHF 中的 KL 正则化）？这一方向的理论潜力未被探索。
4. 与 SPO 的集成策略缺乏理论指导——需要更原则性的融合框架来解释为何 α 散度与 SPO 的优化目标互补。

> **需要人工验证的点：** 论文声称 α-DPO 不引入额外计算开销（附录 A.3.4），但动态调度机制中隐式分类器 $f$ 的计算成本未与基线方法进行详细的 FLOPs 对比。该结论依赖于实验设置中的显存和时间消耗统计，需确认是否在相同硬件和批大小下严格对齐。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/alpha_DPO_Robust_Preference_Alignment_for_Diffusion_Models_via_alpha_Divergence.pdf

![[paperPDFs/ICLR_2026/alpha_DPO_Robust_Preference_Alignment_for_Diffusion_Models_via_alpha_Divergence.pdf]]
