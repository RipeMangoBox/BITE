---
title: "Adaptive Moments are Surprisingly Effective for Plug-and-Play Diffusion Sampling"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Adaptive_Moments_are_Surprisingly_Effective_for_Plug-and-Play_Diffusion_Sampling.pdf
aliases:
- AMGAA
- AMASEPPDS
acceptance: accepted
openreview_forum_id: qYDObsHldZ
tags:
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在采样过程中对似然分数的梯度应用自适应矩估计（Adam风格的动量与自适应缩放），从而稳定梯度方向与尺度。
primary_logic: 将随机优化中成熟的Adam自适应矩思想注入到扩散模型的引导采样中，通过跨时间步维持梯度的一阶与二阶指数移动平均，有效抑制引导信号中的噪声，使采样轨迹更一致地朝目标条件收敛，且几乎不增加计算开销。
claims:
- AdamDPS在所有重建任务（超分辨16×、高斯去模糊强度12、90%随机掩码修复）的LPIPS和FID上均超越全部对比方法。
- 在ImageNet类别条件生成中，AdamDPS获得10.49%的top-10准确率，其余方法均接近1%。
- 合成实验表明，AdamDPS对引导噪声的鲁棒性远优于DPS，KL散度随噪声幅度增长更慢。
- AdamDPS相邻步的引导梯度余弦相似度始终为正，而DPS频繁出现负相似度，证明梯度方向被稳定化。
paradigm: 将随机优化中成熟的Adam自适应矩思想注入到扩散模型的引导采样中，通过跨时间步维持梯度的一阶与二阶指数移动平均，有效抑制引导信号中的噪声，使采样轨迹更一致地朝目标条件收敛，且几乎不增加计算开销。
---

# Adaptive Moments are Surprisingly Effective for Plug-and-Play Diffusion Sampling

> [!tip] 核心洞察
> 将随机优化中成熟的Adam自适应矩思想注入到扩散模型的引导采样中，通过跨时间步维持梯度的一阶与二阶指数移动平均，有效抑制引导信号中的噪声，使采样轨迹更一致地朝目标条件收敛，且几乎不增加计算开销。

| 字段      | 内容                                                                                                                                         |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| 中文题名    | 自适应矩对于即插即用扩散采样出奇地有效                                                                                                                        |
| 英文题名    | Adaptive Moments are Surprisingly Effective for Plug-and-Play Diffusion Sampling                                                           |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=qYDObsHldZ) |
| Topic   | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video                                                |
| Method  | Adaptive Moment Guidance (AdamDPS / AdamCG)                                                                                                |
| Dataset | ImageNet Super Resolution 16×, ImageNet Gaussian Deblur 12, ImageNet Inpainting 90% mask, CIFAR-10 Class-Conditional (standard classifier) |

> [!tip] 效果简介
> - ImageNet Super Resolution 16× 上，LPIPS (↓) 为 0.27 (AdamDPS)，对比 0.30 (DPS) / 0.32 (TFG N_iter=4)，变化 -0.03 / -0.05。
> - ImageNet Gaussian Deblur 12 上，LPIPS (↓) 为 0.33 (AdamDPS)，对比 0.35 (DPS) / 0.36 (TFG N_iter=4)，变化 -0.02 / -0.03。
> - ImageNet Inpainting 90% mask 上，LPIPS (↓) 为 0.12 (AdamDPS)，对比 0.16 (DPS) / 0.13 (TFG N_iter=4)，变化 -0.04 / -0.01。

## 概述

扩散模型在即插即用（plug-and-play）条件采样中面临一个关键瓶颈：似然分数的近似含有大量噪声，导致采样轨迹不稳定。这一问题在条件信息稀疏时尤为严重——例如高倍超分辨（16×）、强高斯模糊（强度12）或大面积随机掩码修复（90%）——此时基础的扩散后验采样（DPS）方法往往失效，生成的样本偏离目标条件。

本文的核心发现是：**将随机优化中成熟的Adam自适应矩估计思想注入扩散模型的引导采样过程，能够有效抑制引导信号中的噪声**。具体而言，在采样过程中对似然分数的梯度维持一阶矩和二阶矩的指数移动平均（EMA），经偏置校正后替代原始梯度作为引导项。一阶矩（动量）平滑了跨步的梯度方向，二阶矩（自适应缩放）根据历史梯度方差调整更新幅度，二者协同使采样轨迹更一致地向目标条件收敛，且几乎不增加计算开销。

该方法被命名为**自适应矩引导（Adaptive Moment Guidance）**，可分别应用于DPS和分类器引导（CG）两种主流范式，得到AdamDPS和AdamCG两种具体实现。

实验证据表明该方法在多个维度上具有显著优势：

- **重建任务全面领先**：在ImageNet超分辨16×、高斯去模糊12、90%随机掩码修复三项任务上，AdamDPS的LPIPS和FID均超越所有对比方法（Figure 3, Table 1）。
- **类别条件生成大幅提升**：在ImageNet类别条件生成中，AdamDPS获得10.49%的top-10准确率，而其余方法均接近1%（Figure 4, Table 8）；使用时间感知分类器的AdamCG将引导分类器准确率从61.0%提升至82.5%（Table 9）。
- **对引导噪声高度鲁棒**：合成实验表明，AdamDPS的KL散度随噪声幅度增长远慢于DPS（Figure 1），相邻步的引导梯度余弦相似度始终为正，而DPS频繁出现负相似度（Figure 9），证明梯度方向被有效稳定化。
- **消融确认双组件必要性**：动量项（β₁）与自适应缩放项（β₂）对性能提升均不可或缺（Figure 7左）。
- **计算开销可忽略**：AdamDPS比DPS仅增加极少的墙钟时间，且远快于需要多次迭代的TFG等方案（Figure 7右）。

该方法将扩散采样中的引导问题重新框定为随机优化问题，以极简的工程改动（仅需维护两组EMA变量）实现了对多种即插即用方法的显著提升，为扩散模型的条件采样提供了新的视角。

## 背景与动机

### 扩散模型与即插即用条件采样

扩散模型通过逐步向数据添加噪声并学习逆转该过程来生成样本。其核心能力在于：训练好的噪声预测网络 $\epsilon_{\theta}(x_t, t)$ 可以给出数据分布对数概率的梯度近似，即先验分数：

$$s_{\theta}(x_t, t) = -\frac{\epsilon_{\theta}(x_t, t)}{\sigma_t} \approx \nabla_{x_t} \log p(x_t)$$

在条件生成场景中，目标是采样自后验分布 $p(x | y)$。根据贝叶斯公式，后验分数可分解为：

$$\nabla_{x_t} \log p(x_t | y) = \nabla_{x_t} \log p(x_t) + \nabla_{x_t} \log p(y | x_t)$$

其中第一项由扩散模型提供，第二项是似然分数。即插即用（plug-and-play）方法的核心思路是：**无需针对特定条件 $y$ 重新训练扩散模型**，只需在采样过程中注入一个外部的引导信号来近似似然分数。

### 现有近似方法的瓶颈

当前主流的即插即用方法采用两种策略来近似似然分数。DPS（Diffusion Posterior Sampling）利用Tweedie公式从噪声 $x_t$ 预测干净样本 $x_{0|t} = x_t - \sigma_t \epsilon_{\theta}(x_t, t)$，然后计算：

$$\nabla_{x_t} \log p(y | x_t) \approx -\nabla_{x_t} \mathcal{L}(f_{\phi}(x_{0|t}), y)$$

CG（Classifier Guidance）则使用时间感知模型直接作用于 $x_t$：

$$\nabla_{x_t} \log p(y | x_t) \approx -\nabla_{x_t} \mathcal{L}(f_{\phi}(x_t, t), y)$$

这些近似存在一个根本性瓶颈：**似然分数估计含有大量噪声**。在条件信息稀疏时（如16×超分辨、强模糊去卷积、90%随机掩码修复），梯度方向不稳定，导致采样轨迹偏离目标分布。合成实验（Figure 1）证实了这一判断：随着引导噪声系数 $\zeta$ 增大，DPS的KL散度迅速上升，而本方法保持显著更低的散度。

### 动机：从随机优化视角稳定引导信号

上述问题的本质是：每步采样中的似然分数梯度 $g_t$ 是一个高噪声的随机估计，直接使用它来更新采样方向等价于在噪声梯度上执行随机优化。这自然引出一个问题——**能否借鉴随机优化中成熟的动量与自适应步长技术来稳定扩散采样的引导过程？**

Adam优化器在深度学习训练中广泛有效，其核心机制是维护梯度的一阶矩（动量）和二阶矩（自适应缩放）的指数移动平均。将这一思想注入扩散采样，意味着跨时间步累积引导梯度的历史信息，从而：

- **一阶矩平滑方向**：抑制单步梯度的随机抖动，保持引导方向的一致性
- **二阶矩自适应缩放**：根据梯度各维度的历史波动幅度调整步长，防止大噪声维度主导更新

这一设计几乎不增加计算开销（仅需维护两组EMA状态），且可作为几行代码的修改直接嵌入现有DPS或CG实现。由此得到的变体分别称为 **AdamDPS** 和 **AdamCG**。

## 核心创新

### 瓶颈：即插即用引导中的噪声梯度

扩散后验采样（DPS）等即插即用方法的核心近似是将不可计算的似然分数 $\nabla_{x_t} \log p(y|x_t)$ 替换为对预测干净样本 $x_{0|t}$ 的损失梯度：

$$\nabla_{x_t} \log p(y|x_t) \approx -\nabla_{x_t} \mathcal{L}(f_\phi(x_{0|t}), y)$$

这一近似虽然实现了即插即用的灵活性，却引入了一个根本性问题：**似然分数的近似含有大量噪声**。当条件信息稀疏时（如16×超分辨、高强度模糊、大面积修复），$x_{0|t}$ 本身的不确定性被放大，导致引导梯度方向剧烈震荡。合成实验（Figure 1）定量验证了这一点：随着引导噪声系数 $\zeta$ 增大，DPS 的经验分布与目标分布之间的 KL 散度迅速攀升，而 AdamDPS 的增长显著更缓。

### 核心机制：将 Adam 注入扩散采样

本文的核心创新是将随机优化中成熟的 **Adam 自适应矩估计** 迁移到扩散模型的引导采样过程中。具体而言，不再直接使用当前步的似然分数梯度 $g_t$，而是跨采样步维护梯度的一阶矩和二阶矩的指数移动平均：

$$m_k = \beta_1 m_{k-1} + (1-\beta_1) g_t, \quad v_k = \beta_2 v_{k-1} + (1-\beta_2) g_t^2$$

经偏置校正后，输出稳定化的引导梯度：

$$\hat{g}_t = \frac{\hat{m}_k}{\sqrt{\hat{v}_k} + \delta}, \quad \hat{m}_k = m_k / (1-\beta_1^k), \; \hat{v}_k = v_k / (1-\beta_2^k)$$

这一设计从两个层面抑制噪声：

- **一阶矩（动量，$\beta_1$）**：累积历史梯度信息，平滑引导方向，使采样轨迹朝目标条件一致收敛。Figure 9 的证据直接支持这一点——AdamDPS 相邻步引导梯度的余弦相似度始终为正，而 DPS 频繁出现负相似度，表明其梯度方向在步间反复翻转。
- **二阶矩（自适应缩放，$\beta_2$）**：根据梯度幅度的历史方差对当前更新进行归一化，抑制异常大的噪声尖峰，同时保留有意义的信号成分。

### Changed Slot：从原始梯度到自适应矩估计

相对于基线方法，AdamDPS/AdamCG 仅改变了一个关键模块——**似然分数梯度的计算方式**：

| 组件 | 基线（DPS/CG） | AdamDPS/AdamCG |
|------|---------------|----------------|
| 引导梯度 | $g_t = -\nabla_{x_t} \mathcal{L}(\cdot)$ | $\hat{g}_t = \hat{m}_k / (\sqrt{\hat{v}_k} + \delta)$ |
| 状态维护 | 无状态 | 维护 $m_k, v_k$ 跨步 EMA |
| 计算开销 | 基础 | 可忽略的额外标量运算 |

这一修改是"几行代码"级别的改动（Algorithm 1-2），不改变扩散模型本身、引导模型架构或采样器的核心逻辑，因此具有极强的即插即用性。Figure 7 右侧的墙钟时间对比证实，AdamDPS 相比 DPS 几乎不增加计算开销，且远快于 TFG 等需要多次迭代的复合方法。

### 消融验证：动量与自适应缩放缺一不可

Figure 7 左侧的消融实验表明，单独移除动量项（$\beta_1=0$）或自适应缩放项（$\beta_2=0$）均导致性能显著下降，在 Cats 数据集的超分辨16×、高斯去模糊12和90%掩码修复三个任务上均如此。这证明 **一阶平滑与二阶归一化对噪声抑制具有互补作用**，二者共同构成了稳定化的充分条件。

### 隐式收益：减轻引导强度调度的依赖

基线方法通常需要针对不同任务精细调整引导强度 $\rho$ 的衰减调度。自适应矩估计的归一化特性隐式地提供了随采样步数变化的尺度调整，减轻了对复杂调度的依赖。实验中的超参数搜索（150次贝叶斯优化）在所有方法上统一进行，AdamDPS 并未获得额外的调参优势，但其性能优势在不同任务难度（Figure 5）和采样步数（Figure 6）下均保持稳健，暗示自适应矩本身提供了一定程度的自调度能力。

## 整体框架

本文提出的自适应矩引导（Adaptive Moment Guidance）方法是一个即插即用（plug-and-play）的扩散采样增强模块，其核心思想是将随机优化中成熟的Adam自适应矩估计注入到扩散模型的引导采样过程中。整个pipeline由三个功能模块构成，按数据流向依次为：

**1. 无条件扩散去噪器（Unconditional Diffusion Denoiser）**

该模块为预训练的扩散模型 $\\epsilon_{\\theta}$，提供两项关键输出：一是先验分数近似 $s_{\\theta}(x_t, t) = -\\epsilon_{\\theta}(x_t, t) / \\sigma_t \\approx \\nabla_{x_t} \\log p(x_t)$，二是通过Tweedie公式从当前噪声样本 $x_t$ 预测的干净数据估计 $\\boldsymbol{x}_{0 \\mid t} = \\boldsymbol{x}_t - \\sigma_t \\boldsymbol{\\epsilon}_{\\theta}(\\boldsymbol{x}_t, t)$。该模块在整个采样过程中保持冻结，不参与任何微调。

**2. 引导模型（Guidance Model）**

引导模型 $f_{\\phi}$ 负责计算条件 $y$ 与去噪估计之间的损失 $\\mathcal{L}$，为似然分数近似提供基础。根据具体任务和近似策略的不同，引导模型可以作用于预测的干净样本 $x_{0|t}$（DPS范式）或直接作用于噪声潜在变量 $x_t$（CG范式）。前者对应近似 $\\nabla_{x_t} \\log p(y | x_t) \\approx -\\nabla_{x_t} \\mathcal{L}(f_{\\phi}(x_{0|t}), y)$，后者对应 $\\nabla_{x_t} \\log p(y | x_t) \\approx -\\nabla_{x_t} \\mathcal{L}(f_{\\phi}(x_t, t), y)$。该模块同样冻结，不参与训练。

**3. 自适应矩估计器（Adaptive Moment Estimator）**

这是本文的核心创新模块，插入在引导模型输出原始梯度 $g_t = -\\nabla \\mathcal{L}(\\cdot)$ 之后、采样更新之前。该模块跨采样时间步维护梯度的一阶矩 $m_k$ 和二阶矩 $v_k$ 的指数移动平均（EMA）：

$$m_k = \\beta_1 m_{k-1} + (1-\\beta_1) g_t, \\quad v_k = \\beta_2 v_{k-1} + (1-\\beta_2) g_t^2$$

经偏置校正后，输出稳定化的引导梯度：

$$\\hat{g}_t = \\frac{\\hat{m}_k}{\\sqrt{\\hat{v}_k} + \\delta}, \\quad \\hat{m}_k = m_k / (1-\\beta_1^k), \\; \\hat{v}_k = v_k / (1-\\beta_2^k)$$

该稳定化梯度 $\\hat{g}_t$ 替代原始梯度 $g_t$ 参与采样更新：

$$x_s = x_t + (\\sigma_t^2 - \\sigma_s^2)\\Big(s_{\\theta}(x_t, t) + \\hat{g}_t\\Big) + \\sqrt{\\sigma_t^2 - \\sigma_s^2} \\frac{\\sigma_s}{\\sigma_t} \\epsilon$$

**输入输出流**

整个pipeline的输入为初始噪声 $x_T \\sim \\mathcal{N}(0, \\sigma_T^2 I)$ 和条件信号 $y$（如低分辨率图像、类别标签等），输出为符合条件约束的干净样本 $x_0$。在每个采样步 $t \\to s$ 中，数据依次流经：扩散去噪器（提供 $x_{0|t}$ 和先验分数）$\\to$ 引导模型（计算损失梯度 $g_t$）$\\to$ 自适应矩估计器（输出 $\\hat{g}_t$）$\\to$ 采样更新（生成 $x_s$）。自适应矩估计器内部维护跨步状态（$m_{k-1}, v_{k-1}$），使得当前步的引导方向受历史梯度信息的平滑与缩放调控。

**两种实例化**

根据底层引导策略的不同，该方法有两种实例化：AdamDPS（Algorithm 1）将自适应矩估计应用于DPS的 $x_{0|t}$ 近似，AdamCG（Algorithm 2）将其应用于CG的时间感知分类器近似。两者的自适应矩估计逻辑完全一致，仅引导梯度的来源不同。论文强调，添加自适应矩通常只需对现有引导实现做几行代码的修改，几乎不增加计算开销（Figure 7右侧墙钟时间对比证实了这一点）。

## 核心模块与公式推导

### 问题背景：即插即用扩散采样中的后验分数分解

扩散模型从纯噪声中生成样本的过程，本质上是在近似数据分布的分数函数（score function），即对数概率密度对输入的梯度 $\nabla_{x_t} \log p(x_t)$。当需要生成满足特定条件 $y$ 的样本时，目标变为从后验分布 $p(x_t \mid y)$ 中采样。根据贝叶斯公式，后验分数可分解为先验分数与似然分数之和：

$$\nabla_{x_t} \log p(x_t \mid y) = \nabla_{x_t} \log p(x_t) + \nabla_{x_t} \log p(y \mid x_t)$$

其中，先验分数 $\nabla_{x_t} \log p(x_t)$ 由预训练的扩散模型提供——通过噪声预测网络 $\epsilon_\theta(x_t, t)$ 与噪声标准差 $\sigma_t$ 的关系直接给出：

$$s_{\theta}(x_t, t) = -\frac{\epsilon_{\theta}(x_t, t)}{\sigma_t} \approx \nabla_{x_t} \log p(x_t)$$

真正棘手的是似然分数 $\nabla_{x_t} \log p(y \mid x_t)$。由于 $x_t$ 是加噪后的潜在变量，其与观测 $y$ 的关系需要通过边缘化所有可能的干净数据 $x_0$ 来刻画：

$$p(y \mid x_t) = \int p(y \mid x_0) \, p(x_0 \mid x_t) \, dx_0$$

这个积分在一般情况下不可解，因此即插即用方法的核心挑战在于：**如何在无需额外训练的前提下，给出一个可计算且足够准确的似然分数近似**。

### 现有方法的近似策略

现有即插即用方法的核心分歧，在于用“什么”来替代似然分数中的 $x_t$。

**DPS（Diffusion Posterior Sampling）** 的思路最为直接：利用 Tweedie 公式从 $x_t$ 预测干净样本的条件期望 $\boldsymbol{x}_{0 \mid t}$，然后将似然分数近似为对该预测干净样本的损失在 $x_t$ 上的梯度：

$$\boldsymbol{x}_{0 \mid t} = \mathbb{E}[\boldsymbol{x}_0 \mid \boldsymbol{x}_t] = \boldsymbol{x}_t - \sigma_t \boldsymbol{\epsilon}_{\theta}(\boldsymbol{x}_t, t)$$

$$\nabla_{x_t} \log p(y \mid x_t) \approx -\nabla_{x_t} \mathcal{L}(f_{\phi}(\boldsymbol{x}_{0 \mid t}), y)$$

这里 $f_\phi$ 是引导模型（如分类器、下采样算子等），$\mathcal{L}$ 是衡量其输出与条件 $y$ 之间差异的损失函数。梯度通过 $\boldsymbol{x}_{0 \mid t}$ 反向传播至 $x_t$，形成引导信号。

**Classifier Guidance（CG）** 则采用另一种策略：训练一个时间感知的模型 $f_\phi(x_t, t)$，使其能直接作用于噪声潜在变量 $x_t$，从而避免通过 Tweedie 估计的间接路径：

$$\nabla_{x_t} \log p(y \mid x_t) \approx -\nabla_{x_t} \mathcal{L}(f_{\phi}(x_t, t), y)$$

两种方法各有优劣：DPS 无需额外训练但近似噪声较大，CG 需要时间感知模型但梯度路径更直接。论文提出的自适应矩方法对两者均适用，分别称为 AdamDPS 和 AdamCG。

### 采样更新与引导注入

无论采用哪种近似，即插即用扩散采样的每一步更新都遵循统一形式。从当前噪声水平 $\sigma_t$ 的样本 $x_t$ 过渡到下一噪声水平 $\sigma_s$（$s < t$）的样本 $x_s$，更新公式为：

$$x_s = x_t + (\sigma_t^2 - \sigma_s^2)\Big(s_{\theta}(x_t, t) - \nabla \mathcal{L}(\cdot)\Big) + \sqrt{\sigma_t^2 - \sigma_s^2} \frac{\sigma_s}{\sigma_t} \epsilon$$

其中 $\epsilon \sim \mathcal{N}(0, I)$ 是随机噪声项。括号内的两项分别对应先验分数（推动样本向数据流形靠拢）和似然分数近似（推动样本向条件 $y$ 靠拢）。核心瓶颈在于：**$\nabla \mathcal{L}(\cdot)$ 这一项含有大量噪声**，尤其在条件信息稀疏时（如 16 倍超分辨），其方向与尺度在相邻采样步之间剧烈波动，导致采样轨迹不稳定。

### 核心创新：自适应矩引导

论文的核心洞察是：扩散采样中似然分数的逐步估计，与随机优化中梯度的逐批估计面临相同的噪声问题。因此，可以将 Adam 优化器中成熟的自适应矩估计直接注入到采样循环中。

具体而言，设第 $t$ 步的原始似然分数梯度为 $g_t = -\nabla_{x_t} \mathcal{L}(\cdot)$。自适应矩估计器跨采样步维护两个指数移动平均（EMA）：

$$m_k = \beta_1 m_{k-1} + (1 - \beta_1) g_t, \quad v_k = \beta_2 v_{k-1} + (1 - \beta_2) g_t^2$$

其中 $k$ 是采样步的索引（从 $T$ 递减至 $0$），$\beta_1, \beta_2 \in [0, 1)$ 分别控制一阶矩和二阶矩的衰减速率。一阶矩 $m_k$ 累积历史梯度方向，起到动量平滑作用；二阶矩 $v_k$ 累积历史梯度平方，用于自适应缩放。

为纠正 EMA 初始值偏向零的偏差，对两个矩进行偏置校正：

$$\hat{m}_k = \frac{m_k}{1 - \beta_1^k}, \quad \hat{v}_k = \frac{v_k}{1 - \beta_2^k}$$

最终，用校正后的一阶矩除以二阶矩的平方根（加小常数 $\delta$ 防止除零），得到自适应缩放后的稳定化梯度：

$$\hat{g}_t = \frac{\hat{m}_k}{\sqrt{\hat{v}_k} + \delta}$$

用 $\hat{g}_t$ 替代原始 $g_t$ 注入采样更新，即构成 AdamDPS（Algorithm 1）或 AdamCG（Algorithm 2）的完整流程。

### 自适应矩的双重作用

这一设计的有效性源于两个互补机制：

1. **动量（一阶矩）**：通过 $\beta_1$ 加权累积历史梯度方向，平滑了相邻步之间的方向跳变。实验证据（Figure 9）显示，AdamDPS 相邻步引导梯度的余弦相似度始终为正，而 DPS 频繁出现负相似度，证明梯度方向被显著稳定化。

2. **自适应缩放（二阶矩）**：通过 $\beta_2$ 累积梯度平方，对每个梯度分量进行独立缩放——历史上波动大的分量被抑制，稳定的分量被保留。这隐式地提供了随采样进程变化的归一化，减轻了对精细调度引导强度 $\rho_t$ 的依赖。

消融实验（Figure 7 左）证实，移除动量项（$\beta_1 = 0$）或自适应缩放项（$\beta_2 = 0$）均导致性能显著下降，表明两者缺一不可。同时，该修改仅增加可忽略的墙钟时间（Figure 7 右），且对现有引导实现通常只需数行代码改动。

## 实验与分析

![[obsidian-vault/assets/figures/papers/paper_list_l8_Adaptive_Moments_are_Surprisingly_Effective_for_Plug_and_Play_Diffusion/figures/003_Figure_1.jpg]]
*Figure 1: Left: The KL divergence between each method’s empirical distribution and the target distribution as a function of the guidance noise coefficient ζ. Right: Visualization of the empirical and target distributions at ζ = 0.175. Figure 2: Qualitative comparison of AdamDPS, DPS, and TFG on Cats dataset for super resolution at 12x downsampling and Gaussian deblurring at blur intensity 9*

![[obsidian-vault/assets/figures/papers/paper_list_l8_Adaptive_Moments_are_Surprisingly_Effective_for_Plug_and_Play_Diffusion/figures/009_Figure_3.jpg]]
*Figure 3: Reconstruction performance measured in LPIPS and FID, where lower is better for both. Comparison on ImageNet and Cats dataset for super resolution at 16x downsampling, Gaussian deblurring at blur intensity 12, and inpainting with a 90% random mask*

![[obsidian-vault/assets/figures/papers/paper_list_l8_Adaptive_Moments_are_Surprisingly_Effective_for_Plug_and_Play_Diffusion/figures/012_Figure_4.jpg]]
*Figure 4: Class-conditional sampling performance measured in classification accuracy and FID, where higher accuracy and lower FID is better. Accuracy is computed as the harmonic mean across three held-out classifiers. Left & Center: Comparison of plug-and-play methods with a standard classifier on CIFAR-10 and ImageNet, respectively. Right: Comparison of plug-and-play methods with a time-aware classifier on ImageNet*

![[obsidian-vault/assets/figures/papers/paper_list_l8_Adaptive_Moments_are_Surprisingly_Effective_for_Plug_and_Play_Diffusion/figures/016_Figure_7.jpg]]
*Figure 7: Left: Ablation of Adam \beta _ { 1 } , \beta _ { 2 } for super resolution at 16x downsampling, Gaussian deblurring at blur intensity 12, and inpainting at 90% random mask on the Cats dataset. Right: Wall clock comparison on a single H100 GPU of 100 step class-conditional sampling with a standard classifier on ImageNet for a batch of 8 256x256 images*

![[obsidian-vault/assets/figures/papers/paper_list_l8_Adaptive_Moments_are_Surprisingly_Effective_for_Plug_and_Play_Diffusion/figures/020_Figure_8.jpg]]
*Figure 8: Sampling trajectories for DPS and AdamDPS projected onto two dimensions for super resolution at 16x downsampling on ImageNet. The y-axis is defined by the difference between the initial noise and the target, and the x-axis by the difference between the AdamDPS and DPS solutions. Contours depict the MSE loss surface with respect to the target. Figure 9: Cosine similarity between sequential guidance terms g _ { t } and g _ { t + 1 } throughout sampling for DPS and AdamDPS. Guidance terms collected from 16x super resolution task on ImageNet. Shading denotes the 25th to 75th percentile*

![[obsidian-vault/assets/figures/papers/paper_list_l8_Adaptive_Moments_are_Surprisingly_Effective_for_Plug_and_Play_Diffusion/figures/026_Table_1.jpg]]
*Table 1: Reconstruction on ImageNet*

### 核心瓶颈：似然分数近似的噪声问题

即插即用扩散采样的核心挑战在于似然分数 $\nabla_{x_t} \log p(y|x_t)$ 的近似质量。DPS将这一梯度近似为对预测干净样本 $x_{0|t}$ 的损失在 $x_t$ 上的梯度，但该近似天然含有大量噪声，尤其在条件信息稀疏时（如16×超分辨、强模糊）表现尤为突出。Figure 1的合成实验定量揭示了这一问题的严重性：当向引导梯度注入噪声（噪声系数 $\zeta$）时，DPS的经验分布与目标分布之间的KL散度随 $\zeta$ 增大而急剧上升，而AdamDPS的KL散度增长显著更平缓，表明其对引导噪声具有强鲁棒性。

### 主实验结果

#### 图像重建任务

Table 1和Figure 3汇总了ImageNet上三项高难度重建任务的定量结果。AdamDPS在所有任务的LPIPS和FID上均超越全部对比方法：

- **超分辨16×**：AdamDPS的LPIPS为0.27，相比DPS（0.30）降低0.03，相比TFG（N_iter=4, 0.32）降低0.05。FID同样最优。
- **高斯去模糊（强度12）**：AdamDPS的LPIPS为0.33，DPS为0.35，TFG为0.36。
- **90%随机掩码修复**：AdamDPS的LPIPS为0.12，DPS为0.16，TFG为0.13。

Cats数据集上的结果（Table 3）进一步验证了这一优势：16×超分辨任务上AdamDPS的FID为27.62，DPS为30.68，TFG（N_iter=4）为38.83，差距显著扩大。Figure 2的定性对比显示，AdamDPS在12×超分辨和模糊强度9的去模糊任务上生成的图像细节更清晰、伪影更少。

**关键观察**：随着任务难度增加（更高倍数的超分辨或更强模糊），TFG的性能迅速退化，甚至在某些设置下跌落至DPS之下，而AdamDPS始终保持对DPS的稳定正增益（Figure 5）。这表明自适应矩估计在极端条件下的鲁棒性远超基于蒙特卡洛平滑或迭代优化的现有方案。

#### 类别条件生成

类别条件生成是即插即用方法最具挑战性的测试场景之一，因为条件信号仅为一个类别标签，信息极度稀疏。

- **CIFAR-10（标准分类器）**：AdamDPS的引导分类器准确率达到52.6%，DPS为42.8%，提升9.8个百分点（Table 7）。
- **ImageNet（标准分类器）**：AdamDPS获得10.49%的top-10准确率，而DPS及其他方法均接近1%（Table 8, Figure 4左/中）。这一差距极为显著——在1000类分类任务中，10.49%意味着模型确实捕捉到了类别信息，而1%则接近随机猜测。
- **ImageNet（时间感知分类器）**：AdamCG的准确率达到82.5%，CG为61.0%，提升21.5个百分点（Table 9, Figure 4右）。

### 消融实验

#### 自适应矩的双组件必要性

Figure 7（左）的消融表明，动量项（$\beta_1$）与自适应缩放项（$\beta_2$）二者对性能提升均不可或缺。单独移除任一项（设 $\beta_1=0$ 或 $\beta_2=0$）均导致Cats数据集上三项重建任务的LPIPS显著恶化，证明一阶平滑与二阶归一化存在互补效应。

#### 采样步数鲁棒性

Figure 6和Tables 5-6展示了不同采样步数下的性能对比。AdamDPS在低至12步的DDPM采样下仍对DPS保持显著优势，而TFG虽然在极低步数时相对提升较大，但高步数时性能跌落至DPS之下。这一模式在DDPM和DDIM两种采样器上均成立，表明自适应矩估计对不同采样范式具有良好的泛化性。

#### 计算开销

Figure 7（右）的墙钟时间对比显示，AdamDPS相比DPS仅增加可忽略的计算开销（在单张H100 GPU上，100步ImageNet 256×256类别条件采样，批量大小为8），且远快于TFG的多次迭代方案。这与方法设计一致——自适应矩估计仅需维护两个额外的指数移动平均变量，不涉及额外的模型前向/反向传播。

### 机制分析

#### 梯度方向稳定化

Figure 9揭示了AdamDPS性能提升的关键机制：相邻采样步之间引导梯度 $g_t$ 与 $g_{t+1}$ 的余弦相似度。DPS的余弦相似度频繁出现负值，表明引导方向在相邻步之间剧烈振荡；而AdamDPS的余弦相似度始终为正，证明动量累积有效平滑了梯度方向，使采样轨迹更一致地朝目标条件收敛。

#### 采样轨迹可视化

Figure 8将采样轨迹投影到二维空间：纵轴为初始噪声到目标的差异方向，横轴为AdamDPS与DPS解之间的差异方向，等值线描绘相对于目标的MSE损失曲面。可视化显示，DPS的轨迹在损失曲面上剧烈摆动，而AdamDPS的轨迹更平滑、更直接地逼近目标区域。

#### 引导损失动态

Figure 10展示了采样过程中引导损失的变化。对于16×超分辨任务，TFG虽然最终达到更低的引导损失，但这并未转化为更好的重建质量——这一“过度优化”现象说明TFG的损失下降可能以牺牲图像真实性为代价。对于类别条件生成任务，仅AdamDPS能有效降低引导损失，DPS和TFG均无法产生有意义的损失下降，这解释了类别条件任务上AdamDPS的巨大优势。

### 公平性保障

所有方法的超参数均通过贝叶斯优化（150次试验，50次Sobol初始化+100次Log Noisy EI）在验证集（32张图像）上针对各自的主指标独立调优，测试集统一使用2048张图像。重建任务采用LPIPS和FID双指标，类别条件生成采用三个保持分类器的调和平均准确率与FID。这一协议确保了对比的公平性。

### 局限与待验证点

1. **任务域局限**：实验仅在CIFAR-10、ImageNet 256×256和Cats数据集上进行，未验证大规模文本到图像或更高分辨率场景下的有效性。
2. **超参调度**：$\beta_1$、$\beta_2$沿用标准Adam默认值或简单搜索，缺乏针对不同任务或采样阶段的自适应调度策略。
3. **采样器兼容性**：实验以100步DDPM为主，虽在DDIM上进行了步数消融，但未与DPM-Solver等更高效的快速采样器结合评估。
4. **动态场景未知**：在视频帧间引导等动态变化条件下，自适应矩的长期记忆是否会引入滞后效应，尚需进一步研究。

## 方法谱系与知识库定位

### 基线方法关系网络

AdamDPS/AdamCG 的核心贡献在于**注入自适应矩估计**，而非重新设计似然分数近似本身。因此，该方法与现有即插即用方法形成"叠加式改进"关系：

**DPS（直接基础）**：AdamDPS 直接建立在 DPS 的似然分数近似之上——将不可处理的 $\nabla_{x_t} \log p(y|x_t)$ 替换为对预测干净样本 $x_{0|t}$ 损失的梯度 $\nabla_{x_t} \mathcal{L}(f_\phi(x_{0|t}), y)$。DPS 的瓶颈在于该近似本身含有大量噪声，尤其在条件信息稀疏时（如 16× 超分辨）导致采样轨迹不稳定。AdamDPS 不改变近似形式，而是对 DPS 输出的原始梯度 $g_t$ 施加跨时间步的自适应矩归一化，将 $g_t$ 替换为 $\hat{g}_t = \hat{m}_k / (\sqrt{\hat{v}_k} + \delta)$。

**Classifier Guidance（时间感知分支）**：CG 使用时间条件模型 $f_\phi(x_t, t)$ 直接作用于噪声潜在变量，与 DPS 形成"近似策略"层面的平行选择。AdamCG 对 CG 施加相同的自适应矩机制，证明该改进不依赖于特定的似然近似形式。

**LGD（蒙特卡洛平滑）**：LGD 通过多次采样 $x_{0|t}$ 并取平均来稳定 DPS 近似，本质上是**空间维度的平滑**。AdamDPS 则通过跨时间步的指数移动平均实现**时间维度的平滑**。两者在机制上互补，但 AdamDPS 无需额外的前向传播开销。

**MPGD（流形保持）**：MPGD 在数据空间上优化 $x_{0|t}$ 而非在潜在空间反传，避免了通过扩散模型的梯度计算。这与 AdamDPS 的正交性体现在：MPGD 改变的是梯度**来源**（绕过扩散模型），AdamDPS 改变的是梯度**处理方式**（自适应矩归一化）。

**TFG / UGD（复合框架）**：TFG 综合了 DPS、MPGD、LGD 和 FreeDoM 的递归机制，通过多次迭代（$N_{iter}$）和多种策略组合来提升性能。然而，实验揭示了关键发现：TFG 的多次迭代策略在**高难度任务**上迅速退化至不如 DPS，而 AdamDPS 保持稳定的正增益（Figure 5）。在低采样步数下（12 步），TFG 相对提升较大，但高步数时跌落至 DPS 之下（Figure 6）。这表明复合策略的收益高度依赖于任务难度和采样预算，而自适应矩估计的收益更为**鲁棒**。

**RED-diff / ΠGDM**：RED-diff 基于分数先验的重建框架，ΠGDM 假设伪逆转化的存在。两者属于不同的问题设定，与 AdamDPS 的直接可比性有限，但在 ImageNet 重建主表中均被 AdamDPS 超越。

### 适用边界与失效模式

**已验证的适用场景**：
- 图像重建任务：超分辨（4×–16×）、高斯去模糊（强度 3–12）、随机掩码修复（90% 掩码），覆盖从轻度到极端的退化强度
- 类别条件生成：CIFAR-10（32×32）和 ImageNet（256×256），包括标准分类器和时间感知分类器两种引导模式
- 采样器兼容性：DDPM 和 DDIM 采样器均验证有效（Figure 6）

**已知局限**：
- 仅在有限分辨率的图像域（CIFAR-10、ImageNet 256×256、Cats）进行测试，未验证大规模文本到图像或更高分辨率场景
- 实验使用 100 步 DDPM 采样，未与更高效的快速采样器（如 DPM-Solver）结合评估
- 自适应矩的超参数 $\beta_1, \beta_2$ 沿用了标准 Adam 的默认值或简单搜索，缺乏针对不同任务的自适应调度

**需手动验证的边界**：论文未提供以下场景的实验证据——(a) 非高斯噪声退化（如 JPEG 压缩伪影、运动模糊）；(b) 多条件组合引导（如同时进行超分辨和类别条件）；(c) 潜在扩散模型（LDM）框架下的适配性。这些场景下自适应矩的有效性需要进一步验证。

### 开放问题

1. **跨方法组合**：自适应矩估计能否与其他类型的即插即用方法（如 FreeDoM 的重访机制、MPGD 的流形保持策略）叠加获益？消融实验已证明 $\beta_1$（动量）和 $\beta_2$（自适应缩放）缺一不可，但未探索与其他平滑/正则化策略的交互。

2. **采样器依赖**：扩散模型的不同采样器（DDIM、DPM-Solver、Heun 等）下，矩估计的最优衰减率是否一致？DDIM 的非马尔可夫性质可能改变相邻步梯度的相关性结构，从而影响指数移动平均的平滑效果。

3. **时序记忆的代价**：在动态变化的条件（如视频帧间引导、交互式编辑）中，自适应矩的长期记忆是否会引入滞后效应？Figure 9 显示 AdamDPS 的相邻步引导梯度余弦相似度始终为正，这证明了方向稳定性，但在条件快速切换时可能成为阻力。

4. **统一调度设计**：是否可以将 Adam 的步长自适应特性与扩散模型自身的噪声调度 $\sigma_t$ 统一设计，形成端到端的训练采样一体方案？当前两者是独立设计的，联合优化可能进一步提升效率。

## 原文 PDF

## 相关样本

- [[obsidian-vault/analysis/ICLR_2026/AC-Sampler_Accelerate_and_Correct_Diffusion_Sampling_with_Metropolis-Hastings_Algorithm.md|AC-Sampler]]：同属 diffusion sampling 样本，可对照梯度矩估计稳定化与 MCMC 校正。
- [[obsidian-vault/analysis/ICLR_2026/A_Noise_is_Worth_Diffusion_Guidance.md|A Noise is Worth Diffusion Guidance]]：同属 diffusion guidance 样本，可对照显式引导梯度处理与噪声先验细化。

![[obsidian-vault/paperPDFs/ICLR_2026/Adaptive_Moments_are_Surprisingly_Effective_for_Plug-and-Play_Diffusion_Sampling.pdf]]
