---
title: Reward Sharpness-Aware Fine-Tuning for Diffusion Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Reward_Sharpness_Aware_Fine_Tuning_for_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- RFRSAFT
- RSAFTDM
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 因果调节变量是奖励函数在生成图像和模型参数上的局部锐度；通过最小化奖励的局部锐度（即平坦化奖励），可以消除对抗性方向，引导模型沿着与真实偏好一致的方向更新。具体操作是同时施加输入空间对抗扰动（AT）和参数空间锐度感知扰动（SAM）。
primary_logic: 奖励黑客本质上是奖励模型的对抗脆弱性，类似于分类器的对抗攻击；研究发现奖励锐度与人类偏好质量呈强负相关，因此通过平坦化奖励景观可以减轻奖励黑客。结合 Sharpness-Aware Minimization (SAM) 的权重扰动和 Adversarial Training (AT) 的输入扰动，在不重新训练奖励模型的前提下获得鲁棒化的奖励梯度，为扩散模型对齐提供了一种简单通用的插件式方案。
claims:
- 奖励锐度与 PickScore、ImageReward 的人类偏好代理呈强负相关（Pearson r_corr=-0.802 和 -0.669）
- 在 SD1.5、SDXL、SD3 等多个骨干网络上，RSA-FT 均一致提高了所有 RDRL 基线（ReFL, DRaFT-K, AlignProp, DRTune）的 HPSv2.1、PickScore 和 ImageReward 得分，并缓解了奖励黑客行为
- 消融研究表明，联合图像空间扰动和参数空间扰动比单一扰动带来更大的性能提升，验证了两者的协同作用
- "RSA-FT 对扰动半径超参数不敏感（ρ 和 ρ_w 在 {0.1,0.01,0.001} 中均有效，0.01 最优），训练稳定"
---

# Reward Sharpness-Aware Fine-Tuning for Diffusion Models

> [!tip] 核心洞察
> 奖励黑客本质上是奖励模型的对抗脆弱性，类似于分类器的对抗攻击；研究发现奖励锐度与人类偏好质量呈强负相关，因此通过平坦化奖励景观可以减轻奖励黑客。结合 Sharpness-Aware Minimization (SAM) 的权重扰动和 Adversarial Training (AT) 的输入扰动，在不重新训练奖励模型的前提下获得鲁棒化的奖励梯度，为扩散模型对齐提供了一种简单通用的插件式方案。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向扩散模型的奖励锐度感知微调 |
| 英文题名 | Reward Sharpness-Aware Fine-Tuning for Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.21175) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | RSA-FT (Reward Sharpness-Aware Fine-Tuning) |
| Dataset | DrawBench, HPD, Flux.1-dev |

> [!tip] 效果简介
> - DrawBench 上，HPSv2.1 31.67 (ReFL+Ours, SD1.5) vs 31.08 (ReFL, SD1.5) (+0.59)；HPSv2.1 (SDXL) 31.58 (DRTune+Ours) vs 30.04 (DRTune) (+1.54)；PickScore (SD3) 22.61 (DRTune+Ours) vs 22.41 (DRTune) (+0.20)。
> - HPD 上，ImageReward 0.903 (DRTune+Ours, SD1.5) vs 0.842 (DRTune, SD1.5) (+0.061)。
> - Flux.1-dev 上，ImageReward 0.961 (DRTune+Ours) vs 0.926 (DRTune) (+0.035)。

## 概要

扩散模型在奖励驱动的强化学习（RDRL）中面临一个根本性瓶颈：奖励模型对输入扰动高度非鲁棒，导致策略沿对抗方向过优化奖励，产生“奖励黑客”现象——生成图像在目标奖励模型上得分虚高，但视觉质量和与人类偏好的真实对齐度反而下降。本文揭示，这一问题的本质在于奖励函数在图像输入空间和模型参数空间中存在尖锐的局部极大值（高奖励锐度），而奖励锐度与人类偏好质量呈强负相关（PickScore 的 Pearson $r_{\text{corr}}=-0.802$，ImageReward 的 $r_{\text{corr}}=-0.669$，见 **Figure 4**）。

基于这一洞察，本文提出 **RSA-FT**（Reward Sharpness-Aware Fine-Tuning），一种无需重新训练奖励模型的通用插件式方案。其核心思想是平坦化奖励景观：同时施加输入空间对抗扰动（Adversarial Training, AT）和参数空间锐度感知扰动（Sharpness-Aware Minimization, SAM），迫使模型在奖励函数的平坦区域进行优化，从而消除对抗性梯度方向，引导更新与真实人类偏好一致。如 **Figure 3** 所示，传统方法直接沿尖锐奖励的梯度最大化奖励，易陷入奖励黑客；RSA-FT 则从平坦化后的奖励模型获取梯度，在图像空间和参数空间双重平坦化。

实验覆盖 SD1.5、SDXL、SD3 和 Flux.1-dev 四个骨干网络，以及 ReFL、DRaFT-K、AlignProp、DRTune 四种主流 RDRL 基线。结果表明，RSA-FT 在所有组合上一致提升 HPSv2.1、PickScore 和 ImageReward 得分（例如 SD1.5 上 DRTune+Ours 的 ImageReward 从 0.842 提升至 0.903，SDXL 上 DRTune+Ours 的 HPSv2.1 从 30.04 提升至 31.58），并有效缓解奖励黑客行为。消融实验证实，联合使用图像空间和参数空间扰动比单独使用任一扰动带来更大增益，验证了两者的协同效应。此外，RSA-FT 对扰动半径超参数不敏感，训练稳定，且未引入显著的分布发散（FID/KID 评估），展现出良好的实用性和安全性。

### 扩散模型对齐中的奖励黑客困境

扩散模型在文本到图像生成中取得了显著进展，但预训练模型往往无法完全对齐人类偏好。奖励驱动的强化学习（Reward-Driven Reinforcement Learning, RDRL）通过引入奖励模型作为偏好代理，直接最大化生成图像的期望奖励，已成为扩散模型对齐的主流范式。典型方法包括 **ReFL**（步跳过与 x₀ 估计）、**DRaFT-K**（仅反向传播最后 K 步）、**AlignProp**（随机化 K）和 **DRTune**（在 1/10 步上计算梯度）。

然而，RDRL 面临一个核心瓶颈：奖励黑客（reward hacking）。如图 2 所示，当以 HPSv2 作为奖励模型微调时，HPSv2.1 分数确实上升，但其他指标（如 ImageReward、PickScore）和视觉质量反而下降。这表明模型学会了利用奖励函数的漏洞来“刷分”，而非真正提升生成质量。

### 奖励锐度：奖励黑客的根源

本文揭示了奖励黑客的本质原因：**奖励模型在图像输入空间中存在尖锐的局部极大值，对输入扰动高度非鲁棒**。这种尖锐性使得奖励景观中充斥着对抗性方向——策略沿这些方向更新时，奖励分数上升，但真实人类偏好并未改善。

为量化这一现象，本文定义了奖励锐度指标 $S_{1}$：

$$S_{1}=\mathbb{E}_{\mathbf{x}\sim\mathcal{D}}\Big[r(\mathbf{x})-\min_{\|\epsilon\|<\rho}r(\mathbf{x}+\epsilon)\Big]$$

该指标衡量奖励模型在局部邻域内的平均奖励下降程度——值越大，奖励景观越尖锐。实验表明，奖励锐度与人类偏好质量呈**强负相关**：在 PickScore 上 Pearson 相关系数为 -0.802，在 ImageReward 上为 -0.669（Fig. 4）。这为“平坦化奖励景观可以缓解奖励黑客”提供了直接证据。

### 现有方法的缺口

现有缓解奖励黑客的策略主要包括：重新训练更鲁棒的奖励模型、使用奖励集成（reward ensemble）、或引入 KL 正则化约束。这些方法要么计算成本高昂，要么需要额外的训练阶段，缺乏一种**无需重新训练奖励模型、即插即用的通用方案**。

从对抗鲁棒性视角来看，奖励黑客与分类器对抗攻击具有本质相似性：奖励模型对输入扰动的脆弱性导致梯度信号被对抗性方向污染。这暗示着，将对抗训练（Adversarial Training, AT）和锐度感知最小化（Sharpness-Aware Minimization, SAM）的思想引入扩散模型对齐，可能是一条有效的路径——前者在输入空间施加扰动以平坦化奖励，后者在参数空间施加扰动以寻找平坦极小值。然而，在 RDRL 框架下将二者有机结合的工作尚属空白。

### 本文动机

基于上述观察，本文提出 **RSA-FT（Reward Sharpness-Aware Fine-Tuning）**：一种通过联合输入空间和参数空间扰动来平坦化奖励景观的微调方法。核心思想是将原始奖励 $r(\mathbf{x}_0, \mathbf{c})$ 替换为平坦化奖励 $r(\mathbf{x}_0 + \delta_{\mathbf{x}_0}, \mathbf{c}; \theta + \epsilon_{\theta})$，其中 $\delta_{\mathbf{x}_0}$ 为输入对抗扰动，$\epsilon_{\theta}$ 为参数 SAM 扰动。该方法无需重新训练奖励模型，可作为插件无缝集成到现有 RDRL 框架中，引导模型沿着与真实偏好一致的方向更新。

## 核心方法与创新机理

### 问题定位：奖励黑客的对抗脆弱性根源

扩散模型在奖励驱动的强化学习（RDRL）中面临的核心瓶颈是**奖励黑客**（reward hacking）——模型沿奖励函数的对抗方向过优化，产生高奖励分数但偏离人类真实偏好的生成结果。本文揭示了这一现象的本质根源：奖励模型在图像输入空间中存在**尖锐的局部极大值**，对输入扰动高度非鲁棒，类似于分类器面对对抗攻击时的脆弱性。当扩散策略沿着这些尖锐区域的梯度方向更新时，极易陷入奖励模型的“捷径”，导致生成质量与文本对齐度的退化（Figure 2 以 Draft-LV 为例展示了这一现象：原始奖励模型可提升 HPS v2.1 分数，却损害了其他指标和视觉质量）。

### 因果机制：奖励锐度与人类偏好的强负相关

本文建立了一个关键因果联系：**奖励函数的局部锐度**与**人类偏好质量**之间存在强负相关。通过定义奖励锐度指标 $S_{1}=\mathbb{E}_{\mathbf{x}\sim\mathcal{D}}\Big[r(\mathbf{x})-\min_{\|\epsilon\|<\rho}r(\mathbf{x}+\epsilon)\Big]$（Eq. 10），即局部邻域内奖励的平均下降幅度，实验证实该指标与 PickScore 和 ImageReward 的 Pearson 相关系数分别达到 **-0.802** 和 **-0.669**（Figure 4）。这一发现提供了明确的因果调节变量：**平坦化奖励景观**可以消除对抗性方向，引导模型沿与真实偏好一致的梯度更新。

### 方法设计：联合输入-参数空间平坦化

基于上述洞察，本文提出 **RSA-FT（Reward Sharpness-Aware Fine-Tuning）**，其核心创新在于**同时从输入空间和参数空间对奖励函数进行平坦化**，无需重新训练奖励模型，作为一个即插即用的通用模块嵌入现有 RDRL 框架。具体而言，RSA-FT 改变了两个关键训练槽位：

| 训练槽位 | 基线做法 | RSA-FT 做法 |
|----------|----------|-------------|
| **训练奖励函数** | 原始奖励模型 $r(\mathbf{x}_0, \mathbf{c})$ | 平坦化奖励 $r(\mathbf{x}_0 + \delta_{\mathbf{x}_0}, \mathbf{c}; \theta + \epsilon_\theta)$，其中 $\delta_{\mathbf{x}_0}$ 为输入对抗扰动，$\epsilon_\theta$ 为参数 SAM 扰动（Eq. 19, Algorithm 1） |
| **奖励求导空间** | 仅对生成图像 $\mathbf{x}_0$ 求导 | 同时对输入图像和模型参数进行扰动后再评估奖励，实现输入-参数双空间平坦化（Eq. 15-17） |

方法由三个协同模块构成：

1. **输入空间扰动模块**：沿奖励对图像的梯度负方向施加单步最差情况扰动 $\delta_{\mathbf{x}_0}=-\rho\frac{\nabla_{\mathbf{x}_0}r}{\|\nabla_{\mathbf{x}_0}r\|}$（Eq. 15），生成对抗样本以消除输入端尖锐区域。

2. **参数空间扰动模块**：借鉴 Sharpness-Aware Minimization（SAM），沿奖励对参数的梯度负方向施加扰动 $\epsilon_{\theta}=-\rho_{\omega}\frac{\nabla_{\theta}r}{\|\nabla_{\theta}r\|}$（Eq. 17），从参数端平坦化奖励景观。

3. **联合平坦化奖励最大化**：最终训练目标为 $\max_{\theta}\mathbb{E}_{\mathbf{c},\mathbf{x}_T}\big[r(\mathbf{x}_0(\mathbf{x}_T,\mathbf{c};\theta+\epsilon_{\theta})+\delta_{\mathbf{x}_0},\mathbf{c})\big]$（Eq. 19），同时包含参数扰动和输入扰动。

### 与现有工作的本质区别

RSA-FT 与现有 RDRL 方法的根本差异在于**反馈信号的来源**：ReFL、DRaFT-K、AlignProp、DRTune 等基线方法直接最大化原始奖励模型的输出，而 RSA-FT 最大化的是经过输入-参数双重平坦化后的奖励。这一设计使得模型不再沿着奖励模型的尖锐对抗方向更新，而是沿着与人类偏好一致的平坦方向优化（Figure 3 提供了几何解释）。消融实验证实，单独使用输入空间扰动（AT）或参数空间扰动（SAM）均能带来性能提升，但**联合使用两者取得了最大增益**，验证了两种平坦化机制的协同效应（Table 6, Appendix）。

RSA‑FT 的整体设计遵循一个简洁的逻辑：**奖励黑客行为的根源在于奖励模型在图像空间和参数空间中存在尖锐的局部极大值，因此通过同时平坦化这两个空间中的奖励景观，可以消除对抗性梯度，使策略沿着与真实人类偏好一致的方向更新**。图 3 从几何角度直观展示了这一思想：传统 RDRL 方法直接沿尖锐奖励表面的梯度方向最大化奖励，容易陷入对抗性区域；RSA‑FT 则从平坦化后的奖励模型中获取梯度，从而缓解奖励黑客。

基于上述洞察，RSA‑FT 的 pipeline 由三个紧密协作的模块构成，其输入‑输出流如下：

1.  **输入空间扰动模块（Adversarial Training, AT）**
    对于当前采样的生成图像 $\mathbf{x}_0(\mathbf{x}_T,\mathbf{c};\theta)$，该模块计算奖励函数 $r$ 对图像输入的最差情况扰动方向，生成对抗样本 $\mathbf{x}_0 + \delta_{\mathbf{x}_0}$，其中
    $$\delta_{\mathbf{x}_0}=-\rho\frac{\nabla_{\mathbf{x}_0}r(\mathbf{x}_0(\mathbf{x}_T,\mathbf{c};\theta),\mathbf{c})}{\|\nabla_{\mathbf{x}_0}r(\mathbf{x}_0(\mathbf{x}_T,\mathbf{c};\theta),\mathbf{c})\|}$$
    其作用是从输入端平坦化奖励景观，使模型在局部邻域内面对的是最小化后的奖励值，而非可能被高估的峰值。

2.  **参数空间扰动模块（Sharpness‑Aware Minimization, SAM）**
    在参数端，该模块计算奖励函数对当前模型参数 $\theta$ 的最差情况扰动方向，生成扰动后的参数 $\theta + \epsilon_{\theta}$，其中
    $$\epsilon_{\theta}=-\rho_{\omega}\frac{\nabla_{\theta}r(\mathbf{x}_0(\mathbf{x}_T,\mathbf{c};\theta),\mathbf{c})}{\|\nabla_{\theta}r(\mathbf{x}_0(\mathbf{x}_T,\mathbf{c};\theta),\mathbf{c})\|}$$
    这等价于在参数空间中最小化奖励的局部锐度，迫使模型收敛到平坦的奖励区域。

3.  **联合平坦化奖励最大化**
    将上述两个模块的输出合并：使用扰动后的参数 $\theta+\epsilon_{\theta}$ 生成图像，再对该图像施加输入扰动 $\delta_{\mathbf{x}_0}$，最后将扰动后的图像送入奖励模型计算奖励。RSA‑FT 的训练目标即为最大化这一平坦化后的期望奖励：
    $$\operatorname*{max}_{\theta}\mathbb{E}_{\mathbf{c},\mathbf{x}_T\sim\mathcal{N}(0,\mathbf{I})}\big[r(\mathbf{x}_0(\mathbf{x}_T,\mathbf{c};\theta+\epsilon_{\theta})+\delta_{\mathbf{x}_0},\mathbf{c})\big]$$

整个流程以即插即用的方式嵌入到现有的 RDRL 框架（ReFL、DRaFT‑K、AlignProp、DRTune）中，不改变去噪骨干网络的结构，也不要求重新训练或修改奖励模型本身。Algorithm 1 给出了完整的训练伪代码：在每次迭代中，先采样噪声和文本条件，通过去噪过程得到 $\mathbf{x}_0$；随后依次计算参数扰动 $\epsilon_{\theta}$ 和输入扰动 $\delta_{\mathbf{x}_0}$；最后用扰动后的参数和图像计算奖励，并通过梯度上升更新模型参数。

消融实验证实了双空间协同的必要性：单独使用图像空间扰动或参数空间扰动均能带来性能提升，但联合使用（即完整的 RSA‑FT）在所有 RDRL 基线和骨干网络上取得了最大增益（附录 Table 6），验证了两种平坦化机制的互补效应。

![[assets/figures/papers/paper_list_l2700_https_arxiv_org_abs_2603_21175/figures/010_Figure_7.jpg]]
*Figure 7: Conceptual illustration of the RDRL framework*

### 动机：奖励景观的局部尖锐性

扩散模型在奖励驱动的强化学习（RDRL）中面临的核心瓶颈是奖励黑客现象：奖励模型在生成图像空间中存在尖锐的局部极大值，导致策略沿对抗方向过优化奖励而偏离真实人类偏好。为量化这一现象，本文引入奖励锐度指标 $S_1$，衡量奖励模型在局部邻域内的平均奖励下降程度：

$$S_{1}=\mathbb{E}_{\mathbf{x}\sim\mathcal{D}}\Big[r(\mathbf{x})-\min_{\|\epsilon\|<\rho}r(\mathbf{x}+\epsilon)\Big] \tag{Eq.10}$$

其中 $r(\mathbf{x})$ 为奖励模型对图像 $\mathbf{x}$ 的输出，$\rho$ 为扰动半径。$S_1$ 值越大，表明奖励景观在局部越尖锐，模型越容易沿对抗梯度方向过优化。实验证实，奖励锐度与人类偏好质量呈强负相关（PickScore 的 Pearson $r_{\text{corr}}=-0.802$，ImageReward 的 $r_{\text{corr}}=-0.669$；Fig. 4），为后续平坦化策略提供了实证基础。

### 核心思想：平坦化奖励函数

为消除奖励景观中的尖锐区域，本文定义平坦化奖励 $\tilde{r}^{d}(\mathbf{x},\mathbf{c})$ 为在距离度量 $d$ 约束下奖励的最低取值：

$$\tilde{r}^{d}(\mathbf{x},\mathbf{c}):=\min_{d(\mathbf{x},\mathbf{x}')<\rho}r(\mathbf{x}',\mathbf{c}) \tag{Eq.12}$$

该定义的核心思路是：用局部邻域内的最差情况奖励替代原始奖励，迫使模型避开奖励景观的尖锐峰，转而沿平坦方向更新。RSA-FT 的训练目标即最大化该平坦化奖励：

$$\mathcal{I}(\theta)=\max_{\theta}\mathbb{E}_{\mathbf{c},\mathbf{x}_T\sim\mathcal{N}(0,\mathbf{I})}\left[\tilde{r}^d\big(\mathbf{x}_0(\mathbf{x}_T,\mathbf{c};\theta),\mathbf{c}\big)\right] \tag{Eq.4 扩展}$$

### 三大模块：联合输入空间与参数空间的平坦化

RSA-FT 通过三个模块实现上述平坦化目标，分别从输入空间和参数空间两个维度消除对抗性方向。

#### 模块一：输入空间扰动（对抗训练视角）

对于生成图像 $\mathbf{x}_0$，直接求解 $\min_{\|\epsilon\|<\rho} r(\mathbf{x}_0+\epsilon)$ 在计算上不可行。本文采用单步梯度近似，计算最差情况输入扰动 $\delta_{\mathbf{x}_0}$：

$$\delta_{\mathbf{x}_0}=-\rho\frac{\nabla_{\mathbf{x}_0}r(\mathbf{x}_0(\mathbf{x}_T,\mathbf{c};\theta),\mathbf{c})}{\|\nabla_{\mathbf{x}_0}r(\mathbf{x}_0(\mathbf{x}_T,\mathbf{c};\theta),\mathbf{c})\|} \tag{Eq.15}$$

该扰动沿奖励对图像梯度的负方向移动 $\rho$ 距离，生成对抗样本 $\mathbf{x}_0+\delta_{\mathbf{x}_0}$。其物理含义是：在输入空间中，奖励下降最快的方向即为对抗方向，通过向该方向施加扰动，可暴露并惩罚奖励模型的局部脆弱性。此模块本质上将对抗训练（Adversarial Training, AT）引入 RDRL 框架，从输入端平坦化奖励景观。

#### 模块二：参数空间扰动（锐度感知最小化视角）

类似地，在模型参数 $\theta$ 上施加最差情况扰动 $\epsilon_{\theta}$，以平坦化参数空间的奖励景观：

$$\epsilon_{\theta}=-\rho_{\omega}\frac{\nabla_{\theta}r(\mathbf{x}_0(\mathbf{x}_T,\mathbf{c};\theta),\mathbf{c})}{\|\nabla_{\theta}r(\mathbf{x}_0(\mathbf{x}_T,\mathbf{c};\theta),\mathbf{c})\|} \tag{Eq.17}$$

其中 $\rho_{\omega}$ 为参数扰动半径。该扰动沿奖励对参数梯度的负方向移动，源自 Sharpness-Aware Minimization (SAM) 的思想：最小化参数邻域内的最差情况损失，使模型收敛到平坦的损失区域。在 RDRL 语境下，SAM 的原始目标

$$\min_{\theta}\mathbb{E}_{\mathbf{x}\sim\mathcal{D}}\Big[\max_{\|\epsilon\|\leq\rho}\ \ell(\theta+\epsilon;\mathbf{x})\Big]$$

被重新解释为：在参数空间中寻找奖励景观平坦的区域，从而避免模型参数沿尖锐梯度方向更新。

#### 模块三：联合平坦化奖励最大化

将上述两个扰动同时作用于奖励评估，得到 RSA-FT 的最终目标：

$$\max_{\theta}\mathbb{E}_{\mathbf{c},\mathbf{x}_T\sim\mathcal{N}(0,\mathbf{I})}\big[r(\mathbf{x}_0(\mathbf{x}_T,\mathbf{c};\theta+\epsilon_{\theta})+\delta_{\mathbf{x}_0},\mathbf{c})\big] \tag{Eq.19}$$

该目标的因果机制如下：
- **参数扰动 $\epsilon_{\theta}$** 使奖励评估发生在参数空间的局部最差情况，迫使模型参数远离奖励景观的尖锐峰；
- **输入扰动 $\delta_{\mathbf{x}_0}$** 使奖励评估发生在图像空间的局部最差情况，消除输入端的对抗性方向；
- **联合最大化** 同时平坦化两个空间，产生协同效应：参数空间的平坦化使模型对输入扰动不敏感，输入空间的平坦化则进一步缩小奖励黑客的可行方向。

### 关键公式汇总

| 公式编号 | 角色 | 变量含义 |
|---------|------|---------|
| Eq.(10) | 奖励锐度指标 $S_1$ | $\mathbf{x}$：生成图像；$\rho$：扰动半径；$r(\cdot)$：奖励模型 |
| Eq.(12) | 平坦化奖励定义 | $d(\cdot,\cdot)$：距离度量；$\tilde{r}^d$：平坦化奖励 |
| Eq.(15) | 图像空间扰动 $\delta_{\mathbf{x}_0}$ | $\mathbf{x}_0$：生成图像；$\rho$：输入扰动半径 |
| Eq.(17) | 参数空间扰动 $\epsilon_{\theta}$ | $\theta$：模型参数；$\rho_{\omega}$：参数扰动半径 |
| Eq.(19) | RSA-FT 联合目标 | $\mathbf{c}$：文本条件；$\mathbf{x}_T$：初始噪声 |

### 与基线方法的差异本质

现有 RDRL 方法（**ReFL**、**DRaFT-K**、**AlignProp**、**DRTune**）均直接最大化原始奖励模型 $r(\mathbf{x}_0,\mathbf{c})$ 对生成图像的评分，其梯度方向完全由奖励模型的局部景观决定。当奖励景观存在尖锐峰时，这些方法会沿对抗方向过优化，导致奖励黑客。RSA-FT 的核心改动在于**训练时对奖励函数的求导空间**：将原始的单点奖励评估替换为同时包含输入扰动和参数扰动的平坦化评估，从而获得鲁棒化的奖励梯度信号。该改动不涉及奖励模型的重新训练，仅改变微调时奖励的调用方式，因此可作为插件式模块与任意 RDRL 框架兼容。

### 扰动半径的鲁棒性

消融实验表明，RSA-FT 对扰动半径超参数不敏感：$\rho$ 和 $\rho_{\omega}$ 在 $\{0.1, 0.01, 0.001\}$ 范围内均有效，其中 $0.01$ 在 HPSv2.1、PickScore 和 ImageReward 上取得最佳综合表现（Table 7, Table 8）。单独使用图像空间扰动或参数空间扰动均能提升性能，但联合使用取得最大增益，验证了两种平坦化的协同效应（Table 6）。

## 实验与关键发现

### 核心假设验证：奖励锐度与人类偏好的负相关

RSA-FT 的设计基于一个核心假设：奖励模型的局部锐度是奖励黑客行为的根源。为验证这一点，作者在 **Figure 4** 中测量了奖励锐度指标 $S_{1}$ 与人类偏好代理指标之间的相关性。结果显示，奖励锐度与 PickScore 的 Pearson 相关系数为 **-0.802**，与 ImageReward 的相关系数为 **-0.669**，均呈现强负相关。这意味着奖励景观越尖锐，其评分与真实人类偏好的一致性越差。这一发现从因果层面确立了“平坦化奖励景观”作为解决奖励黑客问题的有效调节变量。

### 主要定量结果

RSA-FT 作为一种即插即用的模块，被集成到四种主流的奖励驱动扩散强化学习基线中：**ReFL**、**DRaFT-K**、**AlignProp** 和 **DRTune**。所有实验均使用 HPSv2 作为训练奖励模型，并在 DrawBench 和 HPD 两个基准上评估 HPSv2.1、PickScore 和 ImageReward 三项指标。

**SD 1.5 骨干网络（Table 1）**：RSA-FT 在所有基线上均带来一致且显著的提升。以 ReFL 为例，RSA-FT 将 HPSv2.1 从 31.08 提升至 **31.67**（+0.59），ImageReward 从 0.671 提升至 0.719（+0.048）。在 DRTune 上，ImageReward 从 0.842 跃升至 **0.903**（+0.061），提升幅度最大。AlignProp 在集成 RSA-FT 后，PickScore 从 20.74 提升至 **21.51**（+0.77），ImageReward 从 -0.132 大幅回升至 0.268，表明该方法有效抑制了该基线原本严重的奖励黑客问题。

**SDXL 骨干网络（Table 2）**：在 1024×1024 分辨率下，RSA-FT 的增益更为突出。DRTune 基线的 HPSv2.1 从 30.04 提升至 **31.58**（+1.54），ImageReward 从 0.844 提升至 **0.944**（+0.100）。ReFL 基线的 PickScore 从 22.22 提升至 **22.60**（+0.38）。这表明 RSA-FT 的平坦化策略在不同规模的 U-Net 架构上均有效，且对大分辨率生成场景的奖励黑客抑制效果更强。

**SD3 骨干网络（Table 3）**：在基于 MMDiT 架构的 SD3 上，RSA-FT 同样表现出一致的提升。在 DrawBench 上，DRTune + RSA-FT 的 ImageReward 达到 **0.979**，较基线的 0.937 提升 +0.042；在 HPD 上，HPSv2.1 达到 **31.86**，较基线的 31.68 提升 +0.18。这表明该方法对 DiT 类架构同样具有良好的泛化性。

**Flux.1-dev 骨干网络**：在附录实验中，DRTune + RSA-FT 将 ImageReward 从 0.926 提升至 **0.961**（+0.035），进一步验证了该方法在更大规模模型上的有效性。

### 消融实验：双空间扰动的协同效应

**Table 6** 的消融实验系统解耦了 RSA-FT 的两个核心组件：图像空间对抗扰动（AT）和参数空间锐度感知扰动（SAM）。在 SD 1.5 上，单独使用图像空间扰动或参数空间扰动均能带来性能提升，但联合使用两者（即完整的 RSA-FT）在所有基线和指标上均取得最大增益。以 DRTune 为例：仅用 AT 时 ImageReward 为 0.887，仅用 SAM 时为 0.889，而 RSA-FT 达到 **0.903**。这验证了输入空间平坦化与参数空间平坦化之间存在协同效应——前者消除奖励模型对输入像素的对抗脆弱性，后者防止模型参数落入奖励景观的尖锐局部最优。

### 超参数敏感性分析

RSA-FT 引入了两个关键超参数：图像空间扰动半径 $\rho$ 和参数空间扰动半径 $\rho_w$。**Table 7** 显示，$\rho$ 在 {0.1, 0.01, 0.001} 范围内均有效，其中 **0.01** 在 HPSv2.1、ImageReward 和 PickScore 上取得最佳综合表现。**Table 8** 显示，$\rho_w$ 同样在 **0.01** 时所有指标均优于 0.1 和 0.001 的设置。两个扰动半径在数个数量级范围内均能稳定工作，表明 RSA-FT 对超参数选择不敏感，降低了实际部署中的调参成本。

![[assets/figures/papers/paper_list_l2700_https_arxiv_org_abs_2603_21175/figures/015_Table_7.jpg]]
*Table 7: Ablation study on the hyper-parameter ρ*

![[assets/figures/papers/paper_list_l2700_https_arxiv_org_abs_2603_21175/figures/017_Table_8.jpg]]
*Table 8: Ablation study on the hyper-parameter ρ*

### 多奖励组合与分布发散分析

**Table 9** 展示了 RSA-FT 在多重奖励组合场景下的表现。当训练奖励为 HPS+Pick 或 HPS+Pick+Aes 的混合时，RSA-FT 仍能一致提升各项指标，且对扰动范围保持不敏感。这初步表明该方法可扩展到更复杂的奖励聚合场景。

在分布发散方面，**Table 10** 通过 FID 和 KID 测量了 RSA-FT 增强模型与 Vanilla 模型的差异。ReFL + RSA-FT 的 FID 为 48.70，KID 为 0.0006；DRTune + RSA-FT 的 FID 为 92.92，KID 为 0.0099。与基线方法相比，RSA-FT 未引入额外的分布偏移，表明其在提升奖励得分的同时未牺牲生成多样性或引入新的偏差。

![[assets/figures/papers/paper_list_l2700_https_arxiv_org_abs_2603_21175/figures/016_Table_10.jpg]]
*Table 10: Divergence from Vanilla sampling*

### 人类偏好研究

**Figure 5** 的人类偏好研究进一步验证了自动指标的结果。评估者被要求比较基线方法与 RSA-FT 增强版本的生成图像。虚线标记 50% 的等偏好线，RSA-FT 在所有对比中均显著越过该线，表明人类评估者严格偏好 RSA-FT 的输出。这为奖励锐度平坦化策略的有效性提供了最直接的证据。

### 失败模式与局限性

尽管 RSA-FT 在多个维度上表现出一致性，仍需注意以下边界：

1. **偏好优化方法的未验证性**：所有实验均限于基于显式奖励模型的 RDRL 框架。RSA-FT 在基于偏好优化的方法（如 DPO 类扩散对齐）上的有效性尚未得到验证，需要进一步研究。
2. **单一训练奖励**：所有主实验均使用 HPSv2 作为训练信号。虽然附录中的多奖励实验给出了积极信号，但更系统的多目标权衡研究仍有待深入。
3. **扰动半径的固定性**：当前 $\rho$ 和 $\rho_w$ 通过有限网格搜索确定，缺乏自适应调节机制。在训练动态变化或不同任务分布下，固定扰动半径可能次优。
4. **大规模边界**：尽管已覆盖到 Flux.1-dev 规模，但未在更大规模模型或更高分辨率场景下评估，极端规模下的行为尚不可知。
5. **公平性细粒度评估**：仅通过 FID/KID 测量分布发散，缺少针对特定人群、敏感内容或安全维度的细粒度偏差分析。

![[assets/figures/papers/paper_list_l2700_https_arxiv_org_abs_2603_21175/figures/005_Table_1.jpg]]
*Table 1: Quantitative results of various RDRL methods on SD 1.5*

![[assets/figures/papers/paper_list_l2700_https_arxiv_org_abs_2603_21175/figures/006_Table_2.jpg]]
*Table 2: Quantitative results of various RDRL on SDXL (1024 × 1024). Bold text indicates the best performance for each metric*

## 定位与知识库关联

### 核心贡献定位

RSA-FT 的提出直指奖励驱动的扩散强化学习（RDRL）中一个被长期忽视的结构性瓶颈：**奖励模型的对抗脆弱性**。现有的 RDRL 方法——包括 **ReFL**、**DRaFT-K**、**AlignProp** 和 **DRTune**——均直接最大化原始奖励模型 $r(\mathbf{x}_0, \mathbf{c})$ 的输出，却未考虑奖励函数在生成图像空间中的局部几何性质。当奖励景观存在尖锐的局部极大值时，策略梯度会沿对抗方向过度优化，导致生成图像在训练奖励指标上虚高，而在其他人类偏好代理上退化——这正是经典的奖励黑客（reward hacking）现象。

RSA-FT 的因果洞察在于：**奖励黑客的本质是奖励模型对输入扰动的非鲁棒性**，而非优化算法本身的设计缺陷。这一洞察将问题从“如何约束策略更新”重新表述为“如何获得更鲁棒的奖励信号”，从而将对抗训练（Adversarial Training, AT）和锐度感知最小化（Sharpness-Aware Minimization, SAM）这两条原本独立发展的技术线，首次在扩散模型对齐的语境下统一为一个协同框架。

### 与现有技术的关系

**相对于 RDRL 基线方法**，RSA-FT 不改变底层优化器的结构，而是作为一个**即插即用的奖励平坦化模块**嵌入。具体而言：

- **ReFL** 通过跳步和 $\mathbf{x}_0$ 估计来降低反向传播成本，但仍使用原始奖励梯度。
- **DRaFT-K** 仅通过最后 $K$ 步反向传播，同样暴露于尖锐奖励的风险中。
- **AlignProp** 随机化 $K$ 以稳定训练，但未从根本上解决奖励景观的局部尖锐性。
- **DRTune** 在 1/10 步上计算梯度以提升效率，同样继承了对奖励函数局部几何的敏感性。

RSA-FT 在这些方法上的统一增益（Table 1–3）表明，**奖励平坦化是一个正交于梯度估计策略的改进维度**——无论底层 RDRL 方法如何近似去噪过程的梯度，获得平坦化后的奖励信号都能一致地缓解奖励黑客。

**相对于对抗训练和 SAM 的原始语境**，RSA-FT 进行了关键的适应性改造：

- **经典对抗训练**（如 Madry et al., ICLR 2018）在分类任务中对输入施加扰动以提升模型鲁棒性；RSA-FT 将其迁移到**奖励模型的输入空间**，通过对生成图像 $\mathbf{x}_0$ 施加最差情况扰动 $\delta_{\mathbf{x}_0}$ 来平坦化奖励对输入的敏感度。
- **SAM**（Foret et al., ICLR 2021）在参数空间中寻找损失最陡峭的方向进行惩罚以提升泛化能力；RSA-FT 将其重新定向为**对奖励函数的参数锐度进行惩罚**，通过对扩散模型参数 $\theta$ 施加扰动 $\epsilon_\theta$ 来平坦化奖励对模型参数的敏感度。

这种双重平坦化的设计并非简单的技术堆叠。消融实验（Table 6, Appendix）证实：单独使用图像空间扰动或参数空间扰动均能带来性能提升，但**联合使用产生显著的协同增益**——这表明奖励黑客同时存在于输入流形和参数流形两个维度，单一维度的平坦化无法完全消除对抗性梯度。

### 适用边界与约束条件

RSA-FT 的有效性建立在以下前提之上，这些前提同时定义了其适用边界：

1. **奖励模型的可微分性**：RSA-FT 需要计算奖励对生成图像 $\mathbf{x}_0$ 和模型参数 $\theta$ 的梯度，因此仅适用于基于可微分奖励模型的 RDRL 框架。对于使用非可微分奖励信号（如离散的人类反馈排序）的方法，需要额外的近似策略。

2. **扰动半径的合理范围**：实验表明 $\rho$ 和 $\rho_w$ 在 $\{0.1, 0.01, 0.001\}$ 范围内均有效（Table 7–8, Appendix），以 $0.01$ 为最优。但这一范围是针对所测试的奖励模型（HPSv2）和扩散骨干（SD1.5/SDXL/SD3/Flux.1-dev）的经验结果。对于不同尺度的奖励模型或不同模态的生成任务，最优扰动半径可能需要重新校准。

3. **奖励模型的训练分布**：RSA-FT 的平坦化操作在奖励模型的输入空间中进行，其有效性依赖于奖励模型在其训练分布附近具有一定的泛化能力。如果生成图像在微调过程中大幅偏离奖励模型的训练分布，平坦化操作本身可能引入新的偏差。

4. **未验证的扩展场景**：论文明确指出 RSA-FT 尚未在以下场景中得到验证：
   - 基于偏好优化的方法（如 DPO 及其变体），这些方法不直接使用标量奖励模型；
   - PPO 类扩散模型对齐框架，其奖励信号的使用方式与 RDRL 存在差异；
   - 极大规模模型（超过 Flux.1-dev 规模）或更高分辨率的生成任务。

### 局限与开放问题

**已识别的局限**：

1. **单一训练奖励模型**：所有实验均使用 HPSv2 作为训练信号。尽管附录中的多奖励混合实验（Table 9, Appendix）显示了初步的兼容性，但如何在多目标权衡中系统地应用 RSA-FT 仍是一个开放问题。不同奖励模型可能具有不同的锐度特性，联合平坦化的策略需要更深入的理论指导。

2. **扰动半径的手动设定**：当前的 $\rho$ 和 $\rho_w$ 通过有限的网格搜索确定。对于新的任务、骨干网络或奖励模型，手动调参可能成为实际部署的障碍。自适应或学习式的扰动调节机制（如基于奖励景观局部曲率的动态调整）是一个自然的改进方向。

3. **公平性评估的粒度**：论文仅通过 FID 和 KID 测量分布发散来论证 RSA-FT 未引入额外偏差（ReFL+Ours 的 FID 48.70，KID 0.0006；DRTune+Ours 的 FID 92.92，KID 0.0099）。但缺少针对特定人群、敏感概念或危险内容的细粒度偏差分析，这使得安全性声明需要进一步验证。

4. **理论分析的深度**：虽然 Fig. 4 建立了奖励锐度与人类偏好质量之间的强负相关（PickScore 的 Pearson $r_{\text{corr}}=-0.802$，ImageReward 的 $r_{\text{corr}}=-0.669$），但 RSA-FT 的收敛性质、平坦化操作对优化轨迹的影响、以及为什么联合扰动产生协同效应的理论机制，尚未得到严格的形式化分析。

**值得追踪的开放问题**：

- **自适应扰动调节**：能否基于奖励函数在局部邻域内的 Hessian 信息动态调整 $\rho$ 和 $\rho_w$，使得扰动半径与局部曲率相匹配？
- **与 Reward Ensemble 的结合**：RSA-FT 的平坦化操作与 reward ensemble 技术（通过多个奖励模型的集成来缓解过度优化）是否互补？两者的结合能否在更广泛的奖励黑客场景中提供更强的鲁棒性？
- **向偏好优化的迁移**：在 DPO 或 Diffusion-DPO 框架中，奖励信号隐含在偏好对中而非显式的标量输出。RSA-FT 的平坦化思想能否通过对比损失的对抗扰动形式得到保留？
- **最优扰动比例的理论指导**：图像空间扰动和参数空间扰动在平坦化奖励景观时各自扮演什么角色？是否存在一个理论上的最优分配比例，使得在给定的计算预算下最大化平坦化效果？
- **与扩散模型安全对齐的关系**：RSA-FT 通过平坦化奖励减少了奖励黑客，但这是否也意味着模型对某些合法的奖励信号变化变得不敏感？在安全对齐的语境下，这种“平坦化”是否可能掩盖重要的安全信号？

### 在知识库中的位置

RSA-FT 在扩散模型对齐的知识谱系中占据了一个独特的位置：它既不修改底层 RDRL 优化器的结构，也不重新训练或集成奖励模型，而是通过对**奖励信号的局部几何进行主动塑造**来实现对齐改进。这一思路将扩散模型对齐问题从“优化策略设计”层面向“奖励信号预处理”层面进行了有益的转移，为后续研究开辟了一个新的干预维度——奖励景观工程（reward landscape engineering）。

## 原文 PDF

![[paperPDFs/CVPR_2026/Reward_Sharpness_Aware_Fine_Tuning_for_Diffusion_Models.pdf]]
