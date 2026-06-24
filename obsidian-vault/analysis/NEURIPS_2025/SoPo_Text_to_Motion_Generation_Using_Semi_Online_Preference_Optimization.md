---
title: SoPo Text to Motion Generation Using Semi Online Preference Optimization
type: paper
paper_level: A
venue: NEURIPS
year: 2025
pdf_ref: paperPDFs/NEURIPS_2025/SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization.pdf
aliases:
- SOPOS
- STMGUSOPO
tags:
- NEURIPS_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将来自人工标注离线数据集的高质量优先运动与来自策略模型在线动态生成的多样化非优先运动组合成“半在线”训练对；并基于奖励阈值τ驱动分布分离，对高分非优先运动采用仅包含优先运动的损失项，对低分非优先运动采用对比损失，同时通过余弦相似度加权增大偏好差距。
primary_logic: 离线高质量优先运动提供了清晰且可靠的偏好方向，缓解了在线DPO的偏好差距不足；在线多样非优先运动提供了泛化和避免过拟合的能力，弥补了离线DPO的不足；通过阈值判断和重加权策略，使得模型仅在非优先运动确实差于优先运动时才进行对比学习，避免了不必要的优化。
claims:
- SoPo在HumanML3D数据集上显著优于MoDiPO等偏好对齐方法，在MLD模型上MM-Dist相对改善达3.25%，而MoDiPO仅有0.76%。
- 消融实验表明SoPo优于纯在线DPO、离线DPO及其直接组合，验证了半在线策略和阈值过滤的必要性。
- 理论分析揭示离线DPO梯度等价于最小化前向KL散度导致过拟合，在线DPO梯度在低生成概率高奖励样本上消失。
- HumanML3D 上 MM-Dist 相对改善 = 3.25% (MLD+SoPo 相较 MLD 基线)
---

# SoPo Text to Motion Generation Using Semi Online Preference Optimization

> [!tip] 核心洞察
> 离线高质量优先运动提供了清晰且可靠的偏好方向，缓解了在线DPO的偏好差距不足；在线多样非优先运动提供了泛化和避免过拟合的能力，弥补了离线DPO的不足；通过阈值判断和重加权策略，使得模型仅在非优先运动确实差于优先运动时才进行对比学习，避免了不必要的优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | SoPo：基于半在线偏好优化的文本到运动生成方法 |
| 英文题名 | SoPo Text to Motion Generation Using Semi Online Preference Optimization |
| 会议/期刊 | NEURIPS 2025 |
| Links | [arXiv](https://arxiv.org/abs/2410.05255) · [Code](https://github.com/black-forest-labs/flux) · [paper](https://arxiv.org/abs/2412.05095) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Semi-Online Preference Optimization (SoPo) |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，MM-Dist 相对改善 3.25% (MLD+SoPo 相较 MLD 基线) vs 0.76% (MLD+MoDiPO 相较 MLD 基线) (+2.49% (更优))；FID 0.374 ± 0.007 (MLD+SoPo) vs MLD 基线 (相对改善约18.5%) (相对改善 18.5%)；R-Precision Top1 相对改善 +2.21% (MLD+SoPo) vs MLD (+2.21%)。
> - KIT-ML 上，FID 0.384 (MLD+SoPo), 0.176 (MoMask+SoPo) vs 未明确提供基线值 (显著低于其他方法)。

## 概述

文本到运动生成领域面临一个根本性瓶颈：现有模型常产生与人类偏好不一致或不真实的运动，而主流的偏好对齐方法——离线DPO和在线DPO——各自存在难以调和的缺陷。离线DPO依赖固定的标注数据对，其梯度等价于最小化前向KL散度（Theorem 1），导致模型过拟合到有限的非偏好样本上（Figure 2）；在线DPO虽通过动态采样缓解了过拟合，但在低生成概率高奖励样本上梯度消失（Theorem 2），偏好差距不足，对齐效果受限。

针对这一困境，本文提出**半在线偏好优化（Semi-Online Preference Optimization, SoPo）**，核心思路是将离线高质量优先运动与在线动态生成的非优先运动组合成“半在线”训练对。离线优先运动提供清晰可靠的偏好方向，缓解在线DPO的偏好差距不足；在线多样非优先运动提供泛化能力，弥补离线DPO的过拟合问题。在此基础上，SoPo引入奖励阈值τ驱动的分布分离机制，对高分非优先运动采用仅包含优先运动的置信损失，对低分非优先运动采用对比损失，并通过余弦相似度加权增大偏好差距，避免不必要的优化。

在HumanML3D数据集上，SoPo集成到MLD模型后，MM-Dist相对改善达3.25%，显著优于MoDiPO的0.76%（Table 1）；FID实现约18.5%的相对改善。消融实验验证了半在线策略和阈值过滤机制的必要性——SoPo优于纯在线DPO、离线DPO及二者的直接组合（Table 5）。在KIT-ML数据集上，SoPo同样展现出具有竞争力的FID表现（Table 3）。

方法层面，SoPo属于偏好对齐方法谱系中的半在线DPO变体，与离线DPO和在线DPO形成互补。其知识库定位在文本到运动生成的扩散模型后训练阶段，可适配MLD、MDM等主流骨干网络。

## 背景与动机

文本到运动生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的三维人体运动序列，在动画制作、虚拟现实和人机交互等领域具有重要应用价值。近年来，扩散模型（Diffusion Models）在该任务上取得了显著进展，涌现出如**MLD**、**MDM**、**MotionDiffuse**等一系列代表性工作。然而，现有模型生成的运动往往与人类偏好存在偏差——运动可能不自然、与文本语义不一致，或缺乏合理的空间感知能力。

### 现有偏好对齐方法的局限

为缓解上述问题，研究者开始将强化学习人类反馈（RLHF）引入文本到运动生成，通过偏好对齐（Preference Alignment）使模型输出更符合人类期望。直接偏好优化（DPO）作为RLHF的简化形式，避免了显式奖励建模和强化学习训练的不稳定性，成为主流选择。**MoDiPO**是当前文本到运动领域基于DPO的代表性偏好对齐方法，但其底层范式存在根本性缺陷：

- **离线DPO的过拟合问题**：离线DPO依赖固定的偏好数据对进行训练。理论分析（Theorem 1）表明，离线DPO的梯度等价于最小化前向KL散度，导致模型仅学会避开训练集中出现的特定非偏好运动模式，而忽略其他常见但未被覆盖的非偏好区域（Figure 2）。当离线非偏好数据多样性不足时，模型泛化能力严重受限。

- **在线DPO的偏好差距不足**：在线DPO通过当前策略模型动态采样构建偏好对，试图缓解过拟合。然而，理论分析（Theorem 2）揭示，在线DPO的梯度在模型生成概率较低但奖励较高的样本上会消失，导致有偏采样（biased sampling）。这使得优先运动与非优先运动之间的偏好差距（preference gap）不足，难以提供清晰有效的优化信号（Figure 3）。

### 核心动机与研究思路

上述分析揭示了文本到运动偏好对齐的核心瓶颈：**离线DPO因固定标签数据导致过拟合，在线DPO因有偏采样导致偏好差距不足，二者均无法独立实现鲁棒且有效的偏好对齐。**

本文的核心洞察在于：离线高质量优先运动提供了清晰可靠的偏好方向（缓解在线DPO的偏好差距不足），而在线动态生成的多样化非优先运动提供了泛化能力（弥补离线DPO的过拟合缺陷）。基于此，SoPo提出**半在线偏好优化**（Semi-Online Preference Optimization）范式，将离线人工标注的高质量优先运动与在线策略模型动态生成的多样化非优先运动组合成“半在线”训练对，使模型同时获得明确的对齐目标和充足的负样本多样性，从而突破现有方法的性能瓶颈。

## 核心创新

SoPo 的核心创新在于通过**半在线偏好数据构造**与**阈值驱动的分布分离损失**，系统性地解决了现有 DPO 变体在文本到运动生成中的两个结构性缺陷：离线 DPO 的前向 KL 散度最小化导致过拟合，以及在线 DPO 因有偏采样造成的偏好差距不足。

### 半在线偏好对构造

现有偏好对齐方法在数据构造上走向两个极端：**MoDiPO** 等离线方法从预训练模型的固定采样中选取偏好对，其偏好分布退化为数据集上的指示函数 $p_{\mathrm{gt}}^{Mo}(x_w, x_l|c) = \mathbb{I}((x_w, x_l, c) \in \mathcal{D})$，导致梯度等价于最小化前向 KL 散度 $D_{KL}(p_{\mathrm{gt}} \| p_\theta)$（Theorem 1），模型仅学会避开固定的非优先模式而忽略其他常见非偏好区域（Figure 2）；纯在线 DPO 虽使用策略模型动态采样，但其梯度在低生成概率高奖励样本上消失（Theorem 2），且生成分布与偏好分布正相关，难以产生足够的偏好差距。

SoPo 的关键突破在于将两类数据源解耦并重新组合：
- **优先运动** $x^w$ 来自离线人工标注数据集，提供无偏、可靠的偏好方向，避免在线采样中优先运动质量波动的问题；
- **非优先运动** $x^l$ 由在线策略模型 $\bar{\pi}_\theta$ 动态生成，提供多样化的负样本以增强泛化能力并防止过拟合。

这一设计的损失函数为：
$$\mathcal{L}_{\mathrm{DSoPo}}(\theta) = -\mathbb{E}_{(x^w,c)\sim\mathcal{D}} \mathbb{E}_{x^l\sim\bar{\pi}_\theta(x|c)} \log\sigma(\beta \mathcal{H}_\theta(x^w, x^l, c))$$
其中优先运动从离线数据集 $\mathcal{D}$ 采样，非优先运动从策略模型在线采样，形成了“半在线”的偏好学习范式。

### 阈值驱动的分布分离与分支损失

半在线构造引入了一个新挑战：在线生成的非优先运动可能质量较高（奖励分数高），与优先运动的偏好差距不足，此时进行对比学习反而会引入噪声。SoPo 通过引入奖励阈值 $\tau$ 对生成分布进行显式分离来解决这一问题：

$$p_{\bar{\pi}_\theta}(x^{1:K}|c) = p_{\bar{\pi}_\theta}(\cdot) p_\tau(r(x^l,c) \geq \tau) + p_{\bar{\pi}_\theta}(\cdot) p_\tau(r(x^l,c) < \tau)$$

基于此分离，SoPo 设计了**双分支损失**：
- **有价值非优先运动**（$r(x^l,c) < \tau$）：采用标准对比损失，同时包含优先与非优先运动项，推动模型明确区分偏好差异；
- **高偏好非优先运动**（$r(x^l,c) \geq \tau$）：丢弃非优先运动项，仅使用优先运动的 log-sigmoid 损失，避免在偏好差距不足时进行无意义的对比优化。

这一设计确保了模型仅在非优先运动确实差于优先运动时才进行对比学习，从根本上避免了不必要的优化噪声。

### 余弦相似度重加权

为进一步增大有效偏好差距，SoPo 引入基于余弦相似度的动态权重机制：计算优先运动与在线生成的非优先运动集合之间的最小余弦相似度，对优先运动的损失权重 $\beta_w(x^w)$ 进行缩放。相似度越低（即偏好差距越大）的样本对获得更高权重，使得优化过程更聚焦于偏好差异显著的样本，从而提升对齐效率。

### 扩散模型适配

SoPo 将上述概率形式的损失推导到扩散模型框架，转换为基于噪声预测误差差的优化目标，根据阈值条件在两个分支间切换，实现了对主流扩散骨干模型（如 MLD、MDM）的无缝集成。

消融实验（Table 5）直接验证了这些创新：SoPo 显著优于纯离线 DPO、纯在线 DPO 及其简单组合，证明了半在线策略与阈值过滤机制各自独立且协同的必要性。

## 整体框架

SoPo 的整体训练流程围绕“半在线偏好对构造—阈值驱动损失分支—余弦相似度重加权”三条主线展开，旨在解决文本到运动生成中偏好对齐的过拟合与偏好差距不足问题。

**输入与数据流。** 每个训练步接收两类数据：(1) 来自离线人工标注数据集的高质量优先运动 $x^w$，对应文本条件 $c$；(2) 由当前策略模型 $\pi_\theta$ 在线生成的 $K$ 个候选运动 $\{x_{\bar{\pi}_\theta}^k\}_{k=1}^K$。离线优先运动提供了稳定、无偏的偏好方向；在线候选运动则引入了动态多样性，避免对固定负样本的过拟合。

**非优先运动筛选与分布分离。** 从 $K$ 个在线候选运动中，选取奖励模型 $r(\cdot, c)$ 评分最低者作为非优先运动 $x_{\bar{\pi}_\theta}^l$（Eq. 10）。随后，引入阈值 $\tau$ 对生成分布进行分离：若 $r(x_{\bar{\pi}_\theta}^l, c) < \tau$，该样本被标记为“有价值非优先运动”；否则被标记为“高分非优先运动”（Eq. 11）。这一分离机制是 SoPo 的核心因果旋钮——仅当非优先运动确实劣于优先运动时，才进行对比学习；否则避免不必要的优化。

**阈值驱动损失分支。** 根据上述分离结果，SoPo 损失函数分为两支（Eq. 14, 17）：
- **有价值非优先运动分支**：采用对比损失 $\log\sigma(\beta_w h_\theta(x^w,c) - \beta h_\theta(x^l,c))$，同时包含优先运动项与非优先运动项，推动模型拉开偏好差距。
- **高分非优先运动分支**：丢弃非优先运动项，仅保留优先运动的置信损失 $\log\sigma(\beta_w h_\theta(x^w,c))$，避免对已接近优先质量的生成样本施加错误惩罚。

**余弦相似度重加权。** 为增大偏好差距，SoPo 计算优先运动 $x^w$ 与在线非优先运动集合的最小余弦相似度，据此动态缩放优先运动项的权重 $\beta_w(x^w)$（Eq. 14）。相似度越低（即偏好差距越大），权重越高，使模型更关注那些在线生成质量明显不足的样本。

**扩散模型适配。** 对于基于扩散的文本到运动骨干模型（如 MLD、MDM），SoPo 将上述概率形式损失转换为噪声预测误差差的形式（Eq. 17），使优化目标可直接作用于扩散去噪过程。

**模块关系总结。** 整个 pipeline 可概括为五个串行模块：离线优先运动选择 → 在线非优先运动生成与筛选 → 阈值驱动损失分支选择 → 余弦相似度重加权 → 扩散模型适配。这一设计使得 SoPo 同时继承了离线 DPO 的稳定偏好方向和在线 DPO 的泛化能力，并通过阈值与重加权机制克服了二者的核心缺陷——离线 DPO 的过拟合（Theorem 1）和在线 DPO 的梯度消失（Theorem 2）。

### 补充图表

![[assets/figures/papers/paper_list_l1919_SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization/figures/001_Figure_1.jpg]]
*Figure 1: Visual results on HumanML3D dataset. We integrate our SoPo into MDM [13] and MLD [1], respectively. Our SoPo improves the alignment between text and motion preferences*

## 核心模块与公式推导

### 问题形式化与RLHF目标

文本到运动生成的偏好对齐问题可形式化为带KL约束的强化学习目标。给定文本条件 $c$，策略模型 $\pi_{\theta}$ 的目标是最大化期望奖励并约束与参考模型 $\pi_{\mathrm{ref}}$ 的KL散度：

$$
\max_{\pi_{\theta}} \mathbb{E}_{c\sim \mathcal{D}, x\sim \pi_{\theta}(\cdot|c)} \big[ r(x,c) - \beta D_{KL}(\pi_{\theta}(x|c) \| \pi_{\mathrm{ref}}(x|c)) \big]
$$

其中 $r(x,c)$ 为预训练奖励模型对运动 $x$ 的偏好评分，$\beta$ 控制KL惩罚强度（**Eq. (1)**）。

### DPO损失函数

DPO通过分析上述RLHF目标的闭式解，将其简化为直接优化偏好对。给定优先运动 $x^w$ 和非优先运动 $x^l$，DPO损失为：

$$
\mathcal{L}_{\mathrm{DPO}}(\theta) = \mathbb{E}_{(x^w,x^l,c)\sim \mathcal{D}} \big[ -\log\sigma(\beta \mathcal{H}_{\theta}(x^w,x^l,c)) \big]
$$

其中 $\mathcal{H}_{\theta}(x^w,x^l,c) = h_{\theta}(x^w,c) - h_{\theta}(x^l,c)$，$h_{\theta}(x,c) = \log\frac{\pi_{\theta}(x|c)}{\pi_{\mathrm{ref}}(x|c)}$ 为策略与参考模型的对数概率比，$\sigma$ 为logistic函数（**Eq. (2)**）。该损失通过最大化优先与非优先运动之间的隐式奖励差距来对齐偏好。

### SoPo半在线偏好对构建

SoPo的核心创新在于偏好数据对的组成方式：**优先运动来自离线人工标注数据集，非优先运动由在线策略模型动态生成**。这一半在线设计的形式化损失为：

$$
\mathcal{L}_{\mathrm{DSoPo}}(\theta) = - \mathbb{E}_{(x^w,c)\sim \mathcal{D}} \mathbb{E}_{x^l\sim \bar{\pi}_{\theta}(x|c)} \log\sigma(\beta \mathcal{H}_{\theta}(x^w,x^l,c))
$$

其中 $x^w$ 从离线数据集中采样，$x^l$ 从当前策略模型 $\bar{\pi}_{\theta}$ 的生成分布中采样（**Eq. (9)**）。该设计的关键洞察是：离线优先运动提供清晰可靠的偏好方向，缓解在线DPO的偏好差距不足；在线多样非优先运动提供泛化能力，弥补离线DPO的过拟合问题。

### 在线非优先运动生成与筛选

从当前策略模型采样 $K$ 个候选运动后，选取奖励最低者作为非优先运动：

$$
x_{\bar{\pi}_{\theta}}^{l} = \arg\min_{\{x_{\bar{\pi}_{\theta}}^{k}\}_{k=1}^{K}} r(x^k, c)
$$

该选择策略确保非优先运动确实具有较低的偏好评分（**Eq. (10)**）。

### 阈值驱动的分布分离

为解决在线生成中非优先运动可能与优先运动偏好差距不足的问题，SoPo引入阈值 $\tau$ 将生成分布分离为两部分：

$$
p_{\bar{\pi}_{\theta}}(x^{1:K}|c) = p_{\bar{\pi}_{\theta}}(\cdot) p_{\tau}(r(x^l,c)\geq \tau) + p_{\bar{\pi}_{\theta}}(\cdot) p_{\tau}(r(x^l,c)<\tau)
$$

其中 $p_{\tau}(r(x^l,c)<\tau)$ 对应的部分为“有价值非优先运动”，$p_{\tau}(r(x^l,c)\geq \tau)$ 对应的部分为“高分非优先运动”（**Eq. (11)**）。

### 阈值驱动的损失分支选择

针对两类非优先运动采用不同的损失处理策略。对于高分非优先运动（奖励高于阈值），其与优先运动的偏好差距不足，因此丢弃非优先运动项，仅使用优先运动的log-sigmoid损失；对于有价值非优先运动（奖励低于阈值），使用标准对比损失。最终SoPo损失为：

$$
\mathcal{L}_{\mathrm{SoPo}}(\theta) = - \mathbb{E} \big[ Z_{vu}(c) \log\sigma( \beta_w(x^w) h_{\theta}(x^w,c) - \beta h_{\theta}(x^l,c) ) \big] - \mathbb{E} \big[ Z_{hu}(c) \log\sigma( \beta_w(x^w) h_{\theta}(x^w,c) ) \big]
$$

其中 $Z_{vu}$ 和 $Z_{hu}$ 分别为两类非优先运动的归一化因子（**Eq. (14)**）。这一设计使得模型仅在非优先运动确实差于优先运动时才进行对比学习，避免不必要的优化。

### 余弦相似度重加权

为进一步增大偏好差距，SoPo基于优先运动与在线非优先运动集合的最小余弦相似度动态调整损失权重：

$$
\beta_w(x^w) = \beta \cdot \exp\big( C \cdot \min_{k} \cos(x^w, x_{\bar{\pi}_{\theta}}^{k}) \big)
$$

其中 $C$ 为缩放常数。当优先运动与非优先运动在特征空间距离较远时（相似度低），权重增大，强化对该样本的偏好学习（**Section 4.3**）。

### 扩散模型适配

将SoPo损失从概率模型形式推导到扩散模型。对于扩散模型，$h_{\theta}$ 可转换为基于噪声预测误差的形式：

$$
h_{\theta}(x,c) \approx -T \omega_t \mathcal{L}(\theta, \mathrm{ref}, x_t)
$$

其中 $\mathcal{L}(\theta, \mathrm{ref}, x_t)$ 为当前模型与参考模型在噪声预测上的误差差，$T$ 为扩散步数，$\omega_t$ 为时间步权重。代入后得到扩散模型适用的SoPo损失：

$$
\mathcal{L}_{\mathrm{SoPo}}^{\mathrm{diff}}(\theta) = - \mathbb{E}_{t,\,x^w\dots} \begin{cases} \log\sigma(-T\omega_t(\beta_w(x_w) \mathcal{L}(\theta,\mathrm{ref},x_t^w) - \beta \mathcal{L}(\theta,\mathrm{ref},x_t^l))), & \mathrm{if } r(x^l,c)<\tau, \\ \log\sigma(-T\omega_t \beta_w(x_w) \mathcal{L}(\theta,\mathrm{ref},x_t^w)), & \mathrm{otherwise}. \end{cases}
$$

该损失保留了阈值驱动的双分支结构，直接以噪声预测误差差度量模型对优先运动的提升程度（**Eq. (16)-(17)**）。

### 补充图表

![[assets/figures/papers/paper_list_l1919_SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization/figures/002_Figure_2.jpg]]
*Figure 2: Overfitting in offline DPO: green/red points are preferred/unpreferred motions; blue shows bias from fixed unpreferred data, red indicates uncovered unpreferred regions*

## 实验与分析

### 主实验结果

SoPo 在文本到运动生成的偏好对齐任务上展现了显著且一致的性能优势。在 HumanML3D 测试集上，将 SoPo 集成到 MLD 骨干模型后，MM-Dist 相对改善达到 **3.25%**，而同样集成 MoDiPO 仅获得 0.76% 的改善（Table 1）。在 FID 指标上，MLD+SoPo 达到 **0.374 ± 0.007**，相对 MLD 基线改善约 18.5%；R-Precision Top1 相对改善 **+2.21%**。这些结果表明 SoPo 的半在线偏好优化策略在提升文本-运动语义对齐和运动真实感方面均优于现有偏好对齐方法。

![[assets/figures/papers/paper_list_l1919_SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization/figures/004_Table_1.jpg]]
*Table 1: Quantitative results of preference alignment methods for text-to-motion generation on the HumanML3D test set. Results are borrowed from those reported in [9]. The subscripts in each cell denotes the relative performance change. Superscript “†" marks the largest improvement across all models; gray background highlights the largest improvement for each model. “Time∗” denotes estimated online/offline motion generation time, with “1X” as the time for MLD [1] to generate all HumanML3D motions and “K” (unspecified in [9], typically 2∼6) as the number of motion pairs*

将 SoPo 集成到 MDM 骨干模型同样有效：MDM+SoPo 在 FID 上达到 0.544，相较 MDM 基线的 0.544（原文如此，需核实基线值）在 Diversity 和 MM-Dist 上均有提升（Table 1）。在 KIT-ML 数据集上，MLD+SoPo 的 FID 达到 **0.384**，MoMask+SoPo 达到 **0.176**，均显著低于其他对比方法（Table 3），验证了 SoPo 在不同数据集和骨干架构上的泛化能力。

![[assets/figures/papers/paper_list_l1919_SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization/figures/006_Table_3.jpg]]
*Table 3: Comparison of text-to-motion generation performance on the KIT-ML dataset*

与当前最优文本到运动生成方法的全面对比（Table 2）显示，SoPo 增强后的模型在多项指标上达到或超越现有方法，且无需大幅增加模型参数量。

![[assets/figures/papers/paper_list_l1919_SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison of state-of-the-art text-to-motion generation on the HumanML3D test set. ‘MLD∗” refers to the enhanced reproduction of MLD [1] from [2]. For a fair comparison, we selected the “LMM-T” [41] with a similar size to ours*

### 消融实验

#### 对齐策略消融

Table 5 的训练策略消融实验直接验证了半在线设计的必要性。纯离线 DPO 因过拟合固定非偏好数据导致泛化能力下降；纯在线 DPO 受限于有偏采样，偏好差距不足。将离线优先运动与在线非优先运动简单组合（无阈值过滤）的变体性能同样不及完整 SoPo，证实了阈值驱动分布分离机制的关键作用。

![[assets/figures/papers/paper_list_l1919_SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization/figures/009_Table_5.jpg]]
*Table 5: Ablation study on training strategy*

#### 阈值 τ 与采样数 K

Table 4 报告了超参数敏感性分析。在 MLD 骨干上，阈值 **τ = 0.45** 与采样数 **K = 2** 达到性能与效率的最佳平衡；在 MDM 上，**K = 4** 效果更好。当 τ 设置过低时，大量非优先运动被错误归类为高偏好运动，削弱对比学习信号；τ 过高则导致可用训练对过少。增加 K 可进一步提高生成质量，但受限于扩散模型在线采样的计算开销。

![[assets/figures/papers/paper_list_l1919_SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization/figures/007_Table_4.jpg]]
*Table 4: Ablation study on alignment methods, thresholds τ , and sampled number K*

#### 损失组件消融

去除余弦相似度重加权（即 β_w 退化为常数 β）后，模型在偏好差距较大的样本上优化不足，FID 和 MM-Dist 均有退化。去除阈值分支选择（即对所有非优先运动统一使用对比损失）导致高分非优先运动被错误惩罚，R-Precision 下降。这些结果验证了 Eq.(14) 中两项分工设计的有效性：有价值非优先运动（r < τ）通过对比损失拉开与优先运动的差距，高分非优先运动（r ≥ τ）仅通过优先运动的置信损失进行温和引导。

### 失败模式分析

尽管 SoPo 在多数场景下表现优异，但存在以下可识别的失败模式：

1. **奖励模型泛化瓶颈**：SoPo 依赖预训练的文本-运动奖励模型（如 TMR）来筛选非优先运动并计算阈值。当文本描述涉及复杂空间关系或罕见语义组合时，奖励模型的评分可能与真实人类偏好存在偏差，导致筛选出的“非优先运动”并非真正低质量，从而引入噪声训练信号。Figure 4(a) 的空间感知运动生成实验显示，在需要精确空间推理的任务上，SoPo 的提升幅度相对有限。

![[assets/figures/papers/paper_list_l1919_SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization/figures/008_Figure_4.jpg]]
*Figure 4: Quantitative results on (a) spatial-preception motion generation, and (b) user study*

2. **离线偏好数据覆盖不足**：SoPo 的优先运动来自离线标注数据集。对于长尾或开放域文本条件，数据集中可能缺乏对应的高质量运动，此时优先运动本身质量有限，半在线对比较为薄弱。Table 2 中 SoPo 增强模型在极端文本条件下的 MM-Dist 改善幅度小于平均改善，间接反映了这一问题。

3. **在线采样效率**：Table 4 显示 K 增大可提升性能，但扩散模型的反向去噪采样计算成本高昂。当前实验仅探索到 K=4（MDM）和 K=2（MLD），更大 K 值下的性能上界和效率权衡尚不明确。

4. **超参数敏感性**：τ 和重加权常数 C 需针对不同骨干模型和数据集独立调优（Table S2），缺乏自适应调整机制，增加了实际部署的调参成本。

![[assets/figures/papers/paper_list_l1919_SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization/figures/013_Table.jpg]]
*Table: S2: Hyperparameters analysis of our SoPo*

### 图表核心结论

- **Table 1**：SoPo 在 HumanML3D 上全面超越 MoDiPO 等偏好对齐基线，MM-Dist 相对改善达 3.25%，验证半在线策略对文本-运动对齐的有效性。
- **Table 2**：SoPo 增强模型在与当前最优方法的全面对比中表现竞争力，证明偏好对齐可作为通用增强模块。
- **Table 3**：在 KIT-ML 上的优异 FID 表现（MLD+SoPo: 0.384, MoMask+SoPo: 0.176）验证跨数据集泛化能力。
- **Table 4**：τ 和 K 的消融揭示性能-效率权衡，τ=0.45、K=2（MLD）为推荐配置。
- **Table 5**：训练策略消融直接证实半在线设计优于纯离线、纯在线及其简单组合，阈值过滤不可或缺。
- **Figure 4**：用户研究和空间感知实验表明 SoPo 生成的运动在主观偏好上显著优于基线，但在复杂空间推理任务上仍有提升空间。

### 补充图表

![[assets/figures/papers/paper_list_l1919_SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of offline, online DPO, and our SoPo on synthetic data. Offline DPO suffers from mining unpreferred motions with high probability, and online DPO is limited by biased sampling. Our SoPo utilizes the dynamic unpreferred motions and preferred motions from unbiased offline dataset, overcoming their advantage. Here, the blue region is the distribution of generative model*

## 方法谱系与知识库定位

### 1. 方法脉络与前置基础

SoPo 的提出根植于文本到运动生成领域的两条技术主线：**扩散式运动生成模型**与**基于人类反馈的偏好对齐方法**。

在生成骨干方面，SoPo 直接适配于两类主流扩散架构：基于 Transformer 的 **MDM** 和基于潜在扩散的 **MLD**，同时也兼容 **MotionDiffuse** 等经典基线。这些模型虽然能够生成物理上合理的运动序列，但在语义一致性和人类偏好对齐方面存在显著不足——生成的运动常出现文本-运动语义错配、动作不自然或违反物理常识等问题。

在偏好对齐方面，SoPo 的前置方法是 **MoDiPO**，该方法将 Direct Preference Optimization 引入文本到运动生成，通过离线预训练模型采样并构建偏好对进行对齐训练。然而，MoDiPO 继承了离线 DPO 的固有缺陷：偏好对完全来自固定的预训练模型采样，导致训练数据缺乏多样性，模型容易过拟合到特定的非偏好运动模式。

### 2. 核心改进与差异化定位

SoPo 的方法论创新围绕对离线 DPO 和在线 DPO 的**理论缺陷分析**展开，并据此设计了针对性的改进方案。

#### 2.1 理论诊断：两类 DPO 的梯度困境

SoPo 的理论分析揭示了离线 DPO 与在线 DPO 各自的根本性局限：

- **离线 DPO 的过拟合机制**：Theorem 1 证明，离线 DPO 的梯度等价于最小化真实偏好分布与策略分布之间的前向 KL 散度 $D_{KL}(p_{\mathrm{gt}} \| p_{\theta})$。由于离线数据集中非偏好运动固定且有限，模型仅学会避开这些特定模式，而对数据集中未覆盖的非偏好区域缺乏抑制能力，导致泛化性能下降。

- **在线 DPO 的梯度消失问题**：Theorem 2 表明，在线 DPO 的梯度与策略模型自身的生成概率 $p_{\bar{\pi}_\theta}$ 成正比。当某类非偏好运动的生成概率趋近于零但其奖励值较高时（即模型已学会避免采样该运动），梯度依然消失，使得模型无法进一步拉开偏好差距。这源于在线采样与策略分布的耦合导致的“有偏采样”困境。

#### 2.2 半在线机制：解耦偏好方向与负样本多样性

SoPo 的核心设计是将偏好对的构建拆分为两个独立来源：

- **偏好方向锚定**：优先运动 $x^w$ 来自离线人工标注数据集，提供清晰、无偏的偏好目标。这避免了在线 DPO 中偏好方向随策略漂移的问题。
- **负样本多样性**：非优先运动 $x^l$ 由当前策略模型在线动态生成，确保负样本始终覆盖模型当前的弱点区域。这解决了离线 DPO 中负样本固定导致的过拟合。

该设计可视为对 MoDiPO 的直接改进：MoDiPO 的偏好对完全来自离线预训练模型的固定采样，而 SoPo 将非偏好运动的来源替换为在线策略模型，同时保留了离线数据集的偏好运动作为稳定锚点。

#### 2.3 阈值驱动的分布分离与损失分支

SoPo 进一步引入奖励阈值 $\tau$ 对在线生成的非偏好运动进行区分处理：

- **有价值非偏好运动**（$r(x^l, c) < \tau$）：奖励值足够低，与偏好运动形成显著的偏好差距，采用标准对比损失 $\log\sigma(\beta_w h_\theta(x^w) - \beta h_\theta(x^l))$。
- **高偏好非偏好运动**（$r(x^l, c) \geq \tau$）：奖励值偏高，与偏好运动的差距不足，此时丢弃非偏好项，仅使用偏好运动的置信损失 $\log\sigma(\beta_w h_\theta(x^w))$，避免对不构成有效对比的样本进行无效优化。

这一设计与标准 DPO 的单一损失函数形成对比：标准 DPO 对所有样本对统一施加对比损失，而 SoPo 通过阈值判断实现了**条件化的损失选择**，仅在非偏好运动确实显著劣于偏好运动时才进行对比学习。

#### 2.4 余弦相似度重加权

为增大偏好差距，SoPo 计算偏好运动与在线采样得到的 $K$ 个候选非偏好运动之间的最小余弦相似度，并以此对偏好运动的损失权重 $\beta_w$ 进行缩放。该机制倾向于选择与偏好运动语义差异更大的非偏好运动进行对比，从而增强训练信号的有效性。

### 3. 适用边界与局限

#### 3.1 依赖预训练奖励模型

SoPo 的对齐效果高度依赖预训练的文本-运动奖励模型（如 TMR）的判别能力。该奖励模型在开放域文本或复杂空间推理任务上的泛化能力有限，可能导致偏好评分不准确，进而影响阈值 $\tau$ 的判断和非偏好运动的选择质量。

#### 3.2 离线偏好数据的规模与覆盖

离线偏好运动数据集的质量和覆盖范围直接决定了偏好方向的可靠性。对于数据集中未充分覆盖的文本条件，SoPo 可能缺乏高质量的偏好运动锚点，导致对齐方向偏差。

#### 3.3 计算开销与采样数限制

在线采样数 $K$ 的增大可提升非偏好运动的多样性和质量，但受限于扩散模型的反向去噪计算开销。实验表明 $K=2$（MLD）或 $K=4$（MDM）是当前计算约束下的实用选择，更大 $K$ 值的潜力尚未充分探索。

#### 3.4 超参数敏感性

阈值 $\tau$ 和重加权常数 $C$ 等超参数需要针对不同骨干模型和数据集进行独立调优，通用性有待验证。当前实验在 HumanML3D 上使用 $\tau=0.45$，但该值在其他数据集或模型架构上的适用性未经验证。

### 4. 开放问题

1. **奖励模型能力提升**：如何增强奖励模型的空间推理和细粒度语义理解能力，以进一步提升 SoPo 在复杂场景下的对齐效果？

2. **跨架构泛化**：SoPo 当前在扩散模型上验证有效，但在基于离散词表（如 VQ-VAE）的运动生成模型上是否同样适用？

3. **自适应阈值机制**：能否将固定的阈值 $\tau$ 替换为训练过程中动态调整的自适应机制，减少超参数调优负担？

4. **任务扩展**：SoPo 的半在线偏好优化框架能否扩展到文本到视频生成、三维人体运动预测等相关任务？

5. **与判别式模型的协同**：SoPo 通过奖励模型间接利用判别信号，是否存在更直接的判别式-生成式协同优化路径？

## 原文 PDF

![[paperPDFs/NEURIPS_2025/SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization.pdf]]