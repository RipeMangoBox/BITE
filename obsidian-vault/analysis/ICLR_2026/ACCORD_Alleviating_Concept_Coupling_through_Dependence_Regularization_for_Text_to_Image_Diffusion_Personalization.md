---
title: "ACCORD: Alleviating Concept Coupling through Dependence Regularization for Text-to-Image Diffusion Personalization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ACCORD_Alleviating_Concept_Coupling_through_Dependence_Regularization_for_Text_to_Image_Diffusion_Personalization.pdf
project_link: null
code_link: https://github.com/antgroup/ACCORD
aliases:
- ACCORD
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "两个可量化的依赖偏差：1）去噪依赖偏差（Denoising Dependence Discrepancy），即去噪过程中逐步引入的条件依赖变化；2）先验依赖偏差（Prior Dependence Discrepancy），即个性化概念与其超类之间的先验关系偏离。"
primary_logic: "首次将概念耦合形式化为统计依赖问题，并提出一种即插即用的框架ACCORD，通过两个针对性正则化损失直接最小化上述依赖偏差：DDLoss利用扩散模型作为隐式分类器约束相邻时间步的依赖变化；PDLoss在CLIP语义空间中对齐个性化概念与超类的先验依赖关系。"
claims:
- "定理1将总依赖偏差分解为去噪依赖偏差和先验依赖偏差两个可计算项，证明概念耦合源于这两个来源。"
- "DDLoss将去噪依赖偏差上界松弛为相邻时间步依赖变化的加权和，并利用扩散模型的隐式分类特性给出闭式梯度。"
- "PDLoss通过CLIP投影头的缩放余弦相似度近似条件密度比，进而最小化个性化概念与超类的先验依赖差异。"
- "在DreamBench上，将ACCORD集成到CustomDiffusion后，CLIP-I提升+8.4，DINO-I提升+8.3，且人类偏好胜率显著优于基线。"
---

# ACCORD: Alleviating Concept Coupling through Dependence Regularization for Text-to-Image Diffusion Personalization

> [!tip] 核心洞察
> 首次将概念耦合形式化为统计依赖问题，并提出一种即插即用的框架ACCORD，通过两个针对性正则化损失直接最小化上述依赖偏差：DDLoss利用扩散模型作为隐式分类器约束相邻时间步的依赖变化；PDLoss在CLIP语义空间中对齐个性化概念与超类的先验依赖关系。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ACCORD：通过依赖性正则化缓解文本到图像扩散个性化中的概念耦合 |
| 英文题名 | ACCORD: Alleviating Concept Coupling through Dependence Regularization for Text-to-Image Diffusion Personalization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=CKYsYlRdCM) · [GitHub](https://github.com/antgroup/ACCORD) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ACCORD |
| Dataset | DreamBench, StyleBench, FFHQ |

> [!tip] 效果简介
> - DreamBench 上，CLIP-I 为 71.4 (CD w/ Ours*, per Table 1 visual)，对比 62.7 (CD)，变化 +8.7。
> - DreamBench 上，DINO-I 为 61.4 (CD w/ Ours*)，对比 52.7 (CD)，变化 +8.7。
> - StyleBench 上，CLIP-T 为 33.6 (LoRA SDXL w/ Ours*)，对比 31.9 (Omnigen, 3.8B模型)，变化 +1.7。

## 概要

文本到图像扩散模型的个性化微调中普遍存在**概念耦合**问题：训练图像中与目标概念频繁共现的一般概念（如人物、背景或属性）会被错误绑定，导致生成时不符合文本提示，例如出现不该有的物体或风格混淆。ACCORD 首次将这一问题形式化为统计依赖问题，揭示了其两个根本来源——**去噪依赖偏差**（去噪过程中逐步引入的虚假依赖）和**先验依赖偏差**（个性化概念与其超类之间先验关系的偏离），并通过定理 1 将总依赖偏差严格分解为这两个可量化的项。

基于此，ACCORD 提出一种**即插即用**的解耦框架，包含两个理论保证的正则化损失：**去噪解耦损失 DDLoss** 和 **先验解耦损失 PDLoss**。DDLoss 利用扩散模型作为隐式分类器，约束相邻时间步之间条件依赖系数的变化，抑制去噪过程中的依赖漂移；PDLoss 在 CLIP 语义空间中对齐个性化概念与超类的条件密度比，校正先验偏差。二者均不改变原有架构参数，可直接叠加到现有微调流程中。

在 DreamBench、StyleBench 和 FFHQ 等多个基准上的实验表明：将 ACCORD 集成到 CustomDiffusion 后，CLIP‑I 提升 +8.4，DINO‑I 提升 +8.3，且人类偏好胜率显著优于基线；集成到 DreamBooth、LoRA（SDXL）等方法后，同样在文本对齐和个性化保真度上获得一致性增益。消融研究进一步验证了 DDLoss 和 PDLoss 的协同作用以及对不同主干的普适性。这些结果确证了通过直接统计依赖解耦来缓解概念耦合的有效性。



文本到图像（T2I）扩散模型的个性化微调旨在让模型学会一个或几个特定概念（如一只独特的玩具、某个人的脸、一种风格），并根据自由文本提示生成这些概念在不同场景下的图像。主流范式（如DreamBooth、CustomDiffusion）通常使用少量参考图像，在标准扩散去噪损失下微调部分参数或文本嵌入。然而，这种简单的训练策略隐含着一个严重的缺陷：**概念耦合**。

概念耦合是指，当个性化目标概念 $c_p$ 在训练集中频繁与某个一般概念 $c_g$（譬如人物、背景、特定物体）共同出现时，模型容易错误地将两者绑定成统计依赖关系。结果，即使在生成时文本提示中完全没有 $c_g$，模型仍然会"固执地"生成它，导致生成图像违反提示要求。图1清楚展示了这一现象：目标概念"背包*"的训练图像总是与"女孩"共现，常规微调后模型只能在提示"一个背包在红色地毯上"时仍画出一个女孩。这表明，去噪过程本身不断放大了概念间虚假的统计依赖，而现有方法对此无能为力。

现有工作的本质缺口在于**缺乏对概念间统计依赖性的直接、可量化的约束**。DreamBooth、CustomDiffusion、LoRA（SDXL）、VisualEncoder等基线都只用原始扩散损失进行微调，并通过额外正则化数据（如保留原类别的样本）、权重衰减或区域掩码等间接方式来稳定训练，但这些手段并未触及依赖耦合的根源。因此，概念耦合问题一直得不到根本性的缓解，严重影响文本对齐度与个性化保真度。

本文的动机正是将概念耦合**首次形式化为显式的统计依赖问题**，并提出具有理论保证的解耦框架。我们通过定义条件依存系数

$$r(\mathbf{c}_p, \mathbf{c}_g | \mathbf{x}_{\theta, t}) = \frac{p(\mathbf{c}_p, \mathbf{c}_g | \mathbf{x}_{\theta, t})}{p(\mathbf{c}_p | \mathbf{x}_{\theta, t}) p(\mathbf{c}_g | \mathbf{x}_{\theta, t})}$$

来度量在去噪表示 $\mathbf{x}_{\theta, t}$ 下两个概念间的统计依赖程度（$r=1$ 时相互独立）。进而，我们发现概念耦合的主要来源可以精确分解为两类偏差——**去噪依赖偏差**（Denoising Dependence Discrepancy）与**先验依赖偏差**（Prior Dependence Discrepancy）。定理1严格证明了总依赖偏差正是这两项贡献之和，从而揭示了问题根因的双重性。

基于此，我们提出**ACCORD**——一个即插即用的正则化框架，通过两个针对性损失直接最小化上述偏差，而无需改变原有个性化方法的架构或参数。其中，**DDLoss** 在扩散时间步间约束依存系数的增长，利用模型作为隐式分类器的特性给出可计算的闭式梯度；**PDLoss** 则在CLIP语义空间中对齐个性化概念与超类概念的先验依赖关系，防止过度的先验耦合。这一设计使得ACCORD能够通用地集成到DreamBooth、CustomDiffusion、LoRA、VisualEncoder甚至零样本方法（如IP-Adapter）中，从统计根源上缓解概念耦合，期望在保持个性化保真度的同时，大幅提升文本-图像一致性。



## 核心方法与创新机理

**瓶颈形式化：概念耦合即统计依赖偏差**  
现有文本到图像扩散模型的个性化过程，常常将目标概念 $c_p$ 与训练集中频繁共现的一般概念 $c_g$（如背景人物、属性）虚假绑定，导致生成图像违背文本提示。ACCORD 首次将这一现象形式化为**统计依赖问题**：通过条件依存系数  

$$r(\mathbf{c}_p, \mathbf{c}_g | \mathbf{x}_{\theta, t}) = \frac{p(\mathbf{c}_p, \mathbf{c}_g | \mathbf{x}_{\theta, t})}{p(\mathbf{c}_p | \mathbf{x}_{\theta, t}) p(\mathbf{c}_g | \mathbf{x}_{\theta, t})}$$

度量给定去噪表示下概念的依赖强度，并定义概念耦合度量为  

$$\mathbb{E}_{\mathbf{x}_{\theta}} [ |\log r(\mathbf{c}_p, \mathbf{c}_g|\mathbf{x}_{\theta,0}) - \log r(\mathbf{c}_s, \mathbf{c}_g) | ] \gg 0,$$

即生成图像中 $c_p$ 与 $c_g$ 的依赖偏离超类先验的程度。进一步，**定理 1** 将总偏差分解为两个可计算项：  

$$\mathbb{E}_{\mathbf{x}_{\theta}} \Big[ \underbrace{\log r(\mathbf{c}_p,\mathbf{c}_g|\mathbf{x}_{\theta,0}) - \log r(\mathbf{c}_p,\mathbf{c}_g|\mathbf{x}_T)}_{\text{去噪依赖偏差}} + \underbrace{\log r(\mathbf{c}_p,\mathbf{c}_g) - \log r(\mathbf{c}_s,\mathbf{c}_g)}_{\text{先验依赖偏差}} \Big],$$

明确了概念耦合源于 1）去噪过程中逐步引入的依赖变化，2）个性化概念与其超类之间的先验关系偏移。这一分解为直接干预提供了理论杠杆。

**核心洞察：即插即用的直接依赖解耦框架**  
基于上述分解，ACCORD 提出一种与个性化基座无关的框架，通过两个针对性正则化损失直接最小化依赖偏差：

- **去噪解耦损失（DDLoss）**：利用扩散模型作为隐式分类器的特性，将去噪依赖偏差上界松弛为相邻时间步依赖变化的加权和（定理 2 给出闭式梯度），定义为  

  $$\mathcal{L}_{\mathrm{DD}} = \sum_{t=1}^{T} \frac{t}{T} \big| \log r(\mathbf{c}_p, \mathbf{c}_g|\mathbf{x}_{\theta, t-1}) - \log r(\mathbf{c}_p, \mathbf{c}_g|\mathbf{x}_{\theta, t}) \big|,$$

  在训练中约束 UNet 在四种条件 $(\mathbf{c}_p,\mathbf{c}_g), \mathbf{c}_p, \mathbf{c}_g, \varnothing$ 下的预测关系，防止时间步间依赖的剧烈增长。

- **先验解耦损失（PDLoss）**：在 CLIP 语义空间中对齐个性化概念与超类的先验依赖，通过投影头映射得到特征 $\mathbf{f}_p, \mathbf{f}_g, \mathbf{f}_s$，最小化余弦相似度差异  

  $$\mathcal{L}_{\mathrm{PD}} = \mathbb{E}_{\mathbf{c}_g} [ |\cos(\mathbf{f}_p, \mathbf{f}_g) - \cos(\mathbf{f}_s, \mathbf{f}_g) | ],$$

  从而将 $c_p$ 与任何 $c_g$ 的关联拉回超类与 $c_g$ 的关联水平（定理 3 从条件密度比给予支撑）。

**相对于 baselines 的 changed slots**

1. **正则化机制**  
   - **Baseline**：数据正则化（DreamBooth 的先验保留损失）、权重正则化（LoRA）、启发式损失或区域正则化（Break-A-Scene）等，仅能间接缓解概念耦合，无法显式建模依赖变化。  
   - **ACCORD**：引入 DDLoss + PDLoss 两个**直接依赖解耦损失**，在不修改原有个性化架构和参数的前提下，即插即用地强化解耦效果。证据锚点："Building on this decomposition, we propose ACCORD, a plug-and-play method comprising two loss functions: the Denoising Decouple Loss (DDLoss) and the Prior Decouple Loss (PDLoss)."

2. **损失函数**  
   - **Baseline**：仅使用扩散模型原始去噪损失（或其他基线的定制微调损失）。  
   - **ACCORD**：在原有损失上叠加 DDLoss 和 PDLoss，其中 DDLoss 权重通常设在 0.1–0.3，PDLoss 权重设在 0.001–0.003。对于不更新个性化嵌入的方法（如 DreamBooth、LoRA），仅使用 DDLoss；否则同时使用两种损失。证据锚点："Only DDLoss is used for methods that do not update the personalized embedding (e.g., DreamBooth, LoRA), while both losses are applied otherwise."

**实验证据强度**  
- 在 DreamBench 上，ACCORD 集成到 CustomDiffusion 使 CLIP-I 提升 +8.4，DINO-I 提升 +8.3（Table 1），人类偏好胜率显著优于基线。  
- 消融实验（Table 3）表明 DDLoss 和 PDLoss 协同作用，对 SD1.5、SDXL、FLUX 等不同主干具有普适性；权重消融（Table 6）显示对损失超参数不敏感。  
- 即使仅用 1 张参考图像，ACCORD 仍能提升主体相似度（VE+Ours 的 CLIP‑I 从 75.9 升至 78.9，Table 4）。

**可扩展性与局限性**  
该方法不依赖于特定个性化基座，但依赖基础 T2I 模型对条件依赖的建模质量；若基模型无法准确表示超类‑一般概念关联，DDLoss 的对齐可能失效。此外，对于训练提示中未显式出现但强纠缠的外部概念，现有损失无法显式消除关联，仍需依赖模型泛化。



![[assets/figures/papers/iclr26_0005_CKYsYlRdCM_ACCORD_Alleviating_Concept_Coupling_through_Depe/figures/002_Figure_2.jpg]]
*Figure 2: Denoising Decouple Loss $\mathcal{L}_{\mathrm{DD}}$. The UNet estimates $\mathbf{x}_{t-1}$ based on $\mathbf{x}_$t$ and four different conditions, then constrains the relationships between the four denoising results. The objective of $\mathcal{L}_{\mathrm{DD}}$ is to prevent the conditional dependence coefficient between the personalization target $\mathbf{c}_$p$ and the general text condition $\mathbf{c}_$g$ from varying significantly between adjacent timesteps.

![[assets/figures/papers/iclr26_0005_CKYsYlRdCM_ACCORD_Alleviating_Concept_Coupling_through_Depe/figures/003_Figure_3.jpg]]
*Figure 3: Prior Decouple Loss $\mathcal{L}_{\mathrm{PD}}$. Either the Image Encoder or the Text Encoder of CLIP can be used to generate $\mathbf{c}_$p$. The purpose of $\mathcal{L}_{\mathrm{PD}}$ is to prevent excessive prior dependence between $\mathbf{c}_$p$ and the general text condition $\mathbf{c}_$g$. We first use the CLIP projector to map $\mathbf{c}_$p$ and $\mathbf{c}_$g$ into $\mathbf{f}_$p$ and $\mathbf{f}_$g$ respectively, and then minimize the absolute difference between $\cos(\mathbf{f}_$p, $\mathbf{f}_$g)$ and $\cos(\mathbf{f}_$s, $\mathbf{f}_$g)$.

ACCORD 将文本到图像扩散模型个性化中普遍存在的**概念耦合**问题首次形式化为统计依赖问题，并给出一个即插即用的解耦框架。其核心思路是将个性化目标 $c_p$ 与训练集中频繁共现的一般概念 $c_g$ 之间产生的虚假统计依赖，分解为两个可直接优化的来源：

- **去噪依赖偏差**（Denoising Dependence Discrepancy）：去噪过程中逐步引入的条件依赖变化，即 $\log r(c_p, c_g|x_{\theta,0}) - \log r(c_p, c_g|x_T)$ 的期望；
- **先验依赖偏差**（Prior Dependence Discrepancy）：个性化概念与其超类 $c_s$ 之间先验关系的偏移，即 $\log r(c_p, c_g) - \log r(c_s, c_g)$。

基于该分解（定理 1），ACCORD 设计了两项即插即用的正则化损失，与原有个性化微调目标的优化同步进行：

**DDLoss（去噪解耦损失）** 作用于扩散模型的去噪训练过程。对每一个时间步 $t$，它使用 UNet 在四种条件 $(c_p, c_g), c_p, c_g, \varnothing$ 下的预测，计算相邻时间步之间条件依存系数 $r$ 的变化，并以 $t/T$ 为权重对所有步求和。该损失利用扩散模型作为隐式分类器的性质，将依赖变化转化为不同条件下去噪输出差异的闭式表达（定理 2），从而直接约束去噪过程不引入过度的概念耦合。

**PDLoss（先验解耦损失）** 不依赖去噪过程，独立运作。它通过 CLIP 的图文联合嵌入空间，将个性化概念的编码 $\mathbf{f}_p$、一般概念的编码 $\mathbf{f}_g$ 以及超类的编码 $\mathbf{f}_s$ 投影后，最小化 $|\cos(\mathbf{f}_p, \mathbf{f}_g) - \cos(\mathbf{f}_s, \mathbf{f}_g)|$。该损失背后的原理是：缩放余弦相似度能够近似条件密度比（定理 3），因而对齐余弦相似度等价于将个性化概念的先验依赖"拉回"到其超类的水平。

**输入‑输出与集成方式**：ACCORD 不改变任何基线的架构、参数或标准扩散去噪损失，仅在其上添加上述两项损失。对于不更新个性化文本嵌入的方法（如 DreamBooth、LoRA），**仅使用 DDLoss**；对于更新嵌入的方法（如 CustomDiffusion），**同时使用两个损失**。DDLoss 的典型权重为 0.1–0.3，PDLoss 的典型权重为 0.001–0.003，均在验证集上固定后不再对每个概念单独调优，保证了比较的公平性。

整体而言，ACCORD 通过 **DDLoss 抑制去噪阶段依赖的意外增长**，通过 **PDLoss 校正先验层面的依赖偏移**，二者协同在原有微调流水线上即插即用地缓解概念耦合，从而提升文图对齐与个性化保真度。



ACCORD 将概念耦合形式化为个性化目标 $c_p$ 与一般概念 $c_g$ 之间的统计依赖偏离，并通过定理 1 将总依赖偏差分解为两个可优化的来源：**去噪依赖偏差**（Denoising Dependence Discrepancy）与**先验依赖偏差**（Prior Dependence Discrepancy）。基于该分解，ACCORD 提出两个即插即用的正则化损失——**DDLoss**与**PDLoss**，分别在扩散模型的去噪轨迹和 CLIP 语义空间上直接抑制依赖偏差，不改变原有架构参数。

### 依赖偏差的量化与分解

在扩散模型的前向过程中，带噪表示 $\mathbf{x}_t = \sqrt{\alpha_t} \mathbf{x}_0 + \sqrt{1-\alpha_t} \epsilon$，其中 $\alpha_t$ 控制原始信号的保留比例。给定由 UNet $\mathcal{U}_\theta$ 参数化的去噪过程，在时间步 $t$ 学习到的表示 $\mathbf{x}_{\theta,t}$ 上，概念 $c_p$ 和 $c_g$ 的条件依存系数定义为

$$ r(\mathbf{c}_p, \mathbf{c}_g | \mathbf{x}_{\theta, t}) = \frac{p(\mathbf{c}_p, \mathbf{c}_g | \mathbf{x}_{\theta, t})}{p(\mathbf{c}_p | \mathbf{x}_{\theta, t}) \, p(\mathbf{c}_g | \mathbf{x}_{\theta, t})}, $$

其中 $r=1$ 表示条件独立，$r\gg 1$ 表示强依赖。概念耦合程度可由生成结果 $\mathbf{x}_{\theta,0}$ 与超类 $c_s$ 的先验依赖差异衡量：

$$ \mathbb{E}_{\mathbf{x}_{\theta}} \big[ |\log r(\mathbf{c}_p,\mathbf{c}_g|\mathbf{x}_{\theta,0}) - \log r(\mathbf{c}_s,\mathbf{c}_g) | \big] \gg 0. $$

**定理 1** 将此总偏差分解为两个可计算项：

$$ \mathbb{E}_{\mathbf{x}_{\theta}} \Big[ \underbrace{\log r(\mathbf{c}_p,\mathbf{c}_g|\mathbf{x}_{\theta,0}) - \log r(\mathbf{c}_p,\mathbf{c}_g|\mathbf{x}_T)}_{\text{Denoising Dependence Discrepancy}} + \underbrace{\log r(\mathbf{c}_p,\mathbf{c}_g) - \log r(\mathbf{c}_s,\mathbf{c}_g)}_{\text{Prior Dependence Discrepancy}} \Big]. $$

- **去噪依赖偏差**：从纯噪声 $\mathbf{x}_T$ 到清晰图像 $\mathbf{x}_{\theta,0}$ 的去噪过程中，条件依赖的累积变化，揭示了扩散过程本身引入的虚假耦合。
- **先验依赖偏差**：个性化概念 $c_p$ 与一般概念 $c_g$ 的先验依赖相比其超类 $c_s$ 的偏移，反映训练数据中先验共现关系的扭曲。

### 去噪解耦损失（DDLoss）

DDLoss 针对去噪依赖偏差，将其上界松弛为相邻时间步之间依赖变化的加权和，并利用扩散模型作为隐式分类器的性质给出闭式梯度。

首先，对相邻时间步 $t-1$ 与 $t$ 的依赖变化，定理 2 证明其可通过 UNet 在四种条件（$(c_p,c_g), c_p, c_g, \varnothing$）下的输出来计算：

$$ \begin{aligned} \log r(\mathbf{c}_p,\mathbf{c}_g|\mathbf{x}_{\theta,t-1}) - \log r(\mathbf{c}_p,\mathbf{c}_g|\mathbf{x}_{\theta,t}) = \frac{1}{2\sigma_t^2} \Big[ &\|\mathcal{U}_\theta(\mathbf{x}_t,(\mathbf{c}_p,\mathbf{c}_g),t) - \mathcal{U}_\theta(\mathbf{x}_{\theta,t},\mathbf{c}_p,t)\|^2 \\ + &\|\mathcal{U}_\theta(\mathbf{x}_t,(\mathbf{c}_p,\mathbf{c}_g),t) - \mathcal{U}_\theta(\mathbf{x}_{\theta,t},\mathbf{c}_g,t)\|^2 \\ - &\|\mathcal{U}_\theta(\mathbf{x}_t,(\mathbf{c}_p,\mathbf{c}_g),t) - \mathcal{U}_\theta(\mathbf{x}_{\theta,t},\varnothing,t)\|^2 \Big], \end{aligned} $$

其中 $\sigma_t$ 是时间步 $t$ 的噪声标准差。该式子将抽象的条件概率密度比转化为 UNet 去噪估计的欧氏距离，使得依赖变化可微可优。

最终，DDLoss 定义为所有相邻步依赖变化的加权累积：

$$ \mathcal{L}_{\mathrm{DD}} = \sum_{t=1}^{T} \frac{t}{T} \, \big| \log r(\mathbf{c}_p, \mathbf{c}_g | \mathbf{x}_{\theta, t-1}) - \log r(\mathbf{c}_p, \mathbf{c}_g | \mathbf{x}_{\theta, t}) \big|. $$

- $T$：总扩散步数；权重 $t/T$ 使得后期去噪步（更接近清晰图像）获得更大惩罚，以集中抑制概念耦合的形成。
- 该损失在训练时与原始扩散去噪损失共同优化，仅需额外传入 $c_g$ 条件即可计算，属于即插即用模块。

### 先验解耦损失（PDLoss）

PDLoss 校正先验依赖偏差，其核心思路是将个性化概念 $c_p$ 与一般概念 $c_g$ 的依赖关系，对齐到超类 $c_s$ 与 $c_g$ 的依赖关系。根据定理 3，先验依赖偏差等价于条件密度比的对数差：

$$ \log r(\mathbf{c}_p, \mathbf{c}_g) - \log r(\mathbf{c}_s, \mathbf{c}_g) = \log \frac{p(\mathbf{c}_g|\mathbf{c}_p)}{p(\mathbf{c}_g|\mathbf{c}_s)}. $$

为避免直接估计高维条件密度，利用 CLIP 投影头的缩放余弦相似度与密度比的对数近似性：

$$ \tau \cos(\mathbf{f}_p, \mathbf{f}_g) \propto \log \frac{p(\mathbf{c}_g|\mathbf{c}_p)}{p(\mathbf{c}_g)}, \quad \tau \cos(\mathbf{f}_s, \mathbf{f}_g) \propto \log \frac{p(\mathbf{c}_g|\mathbf{c}_s)}{p(\mathbf{c}_g)}, $$

其中 $\mathbf{f}_p, \mathbf{f}_s, \mathbf{f}_g$ 分别为个性化概念、超类和一般概念在 CLIP 联合嵌入空间中的表示。由此，PDLoss 直接最小化两者的余弦相似度差异：

$$ \mathcal{L}_{\mathrm{PD}} = \mathbb{E}_{\mathbf{c}_g} \big[ |\cos(\mathbf{f}_p, \mathbf{f}_g) - \cos(\mathbf{f}_s, \mathbf{f}_g)| \big]. $$

- $c_g$ 从训练提示或预定义词汇集中采样，以覆盖多样的一般概念。
- 若方法不更新个性化文本嵌入（如 DreamBooth、LoRA），$c_p$ 可直接使用参考图像的 CLIP 视觉编码；否则通过可学习的文本嵌入获得。
- 该损失独立于扩散过程，只在语义空间中对齐先验关系，防止过度的先验耦合，同时不损害个性化保真度。



## 实验与关键发现

ACCORD 在两个核心维度上系统性地验证了其去耦合能力：**主体、风格、人脸个性化任务的定量与定性主结果**，以及**消融研究揭示的损失函数与超参数的鲁棒性**。瓶颈洞察—概念耦合源于去噪依赖偏差与先验依赖偏差—在所有实验中保持一致，且 ACCORD 作为即插即用模块可无缝集成到 DreamBooth (DB)、CustomDiffusion (CD)、LoRA、VisualEncoder (VE) 甚至 Break‑A‑Scene (BAS) 等代表性基线中，不改变原始架构与训练超参数。

**主结果**  
- **DreamBench 主体个性化（表 1）**：集成 ACCORD 后，CD 的 CLIP‑I 从 62.7 提升至 71.4（+8.7），DINO‑I 从 52.7 提升至 61.4（+8.7）；同时 CLIP‑T、BLIP‑T 保持稳定甚至稍有改善。在人类偏好评估中，CD+ACCORD 相比原 CD 胜率显著占优，配对一致性 (PA) 超过 80%。该结果确证了直接优化依赖偏差比间接数据正则化更有效地同时提升文本对齐与保真度。  
- **StyleBench 风格个性化（表 2）**：在 SDXL 主干上，LoRA+ACCORD 的 CLIP‑T 达到 33.6，仅比 3.8B 参数的 Omnigen 高 1.7，且 Gram 矩阵距离 (Gram‑D) 明显优于多数基线。这表明 ACCORD 对大规模模型与风格迁移同样通用。  
- **FFHQ 零样本人脸个性化（表 5）**：将 DDLoss 与 PDLoss 同时引入 IP‑Adapter，Face‑Sim 从 14.8 升至 16.4，同时 CLIP‑T 保持不降。DDLoss 与 PDLoss 的协同作用在零样本设定下依然有效。  
- **定性可视化（图 4、5、7）**：ACCORD 生成的图像不仅保留了参考主体的身份特征（如背包、玩具），还准确执行了文本提示中的背景、动作和属性要求，避免了基线中常出现的无关人物、错误背景或属性污染。

![[assets/figures/papers/iclr26_0005_CKYsYlRdCM_ACCORD_Alleviating_Concept_Coupling_through_Depe/figures/004_Table_1.jpg]]

![[assets/figures/papers/iclr26_0005_CKYsYlRdCM_ACCORD_Alleviating_Concept_Coupling_through_Depe/figures/005_Table_2.jpg]]

**消融与分析**  
- **损失贡献（表 3，主干：SD1.5、SDXL、LoRA FLUX）**：DDLoss 主要提升文本对齐指标 (CLIP‑T, BLIP‑T)，PDLoss 主要提升保真度指标 (CLIP‑I, DINO‑I)；两者组合实现最佳的文本‑保真度平衡。在图 6 中，我们通过训练曲线直接观测到 DDLoss 抑制了去噪依赖偏差的增长，而 PDLoss 减小了 CLIP 空间中的余弦相似度偏差，从机制上验证了定理 1 的分解。  
- **损失权重（表 6）**：在 CD 上，DDLoss 权重 0.1‑0.3，PDLoss 权重 0.001‑0.003 的组合均有效，且性能对权重不敏感，无需针对每个主体精细调参。  
- **参考图像数量（表 4）**：当仅使用 1 张参考图时，VE+ACCORD 的 CLIP‑I 仍从 75.9 提升到 78.9，DINO‑I 从 71.0 提升到 73.9，证明依赖解耦即使在极度少样本条件下也能稳健工作。  
- **多主体个性化（表 9）**：将 ACCORD 集成到 Break‑A‑Scene，CLIP‑I 从 51.6 提升到 53.2，DINO‑I 从 36.1 到 38.7，且 CLIP‑T 几乎不变，说明解耦机制在区域正则化多主体设定中同样通用。  
- **PDLoss 设计选择（表 8）**：我们验证了使用超类余弦相似度作为锚点的方案优于仅最小化余弦差异或拉近至零的设置，在保持文本对齐的同时最大化保真度。  
- **按提示类别（表 11）**：ACCORD 在背景替换、场景放置、物体组合、属性编辑四类提示上均超越 CD，尤其在背景替换类别中 CLIP‑I 领先 10 点（75.2 vs 65.2），说明模型对训练集常见共现关系的过度依赖被有效打破。

![[assets/figures/papers/iclr26_0005_CKYsYlRdCM_ACCORD_Alleviating_Concept_Coupling_through_Depe/figures/064_Table_3.jpg]]

![[assets/figures/papers/iclr26_0005_CKYsYlRdCM_ACCORD_Alleviating_Concept_Coupling_through_Depe/figures/070_Figure_6.jpg]]

**失败模式与局限性**  
- **训练提示未覆盖的属性耦合（图 15）**：若训练提示未描述特定属性（如"立方体形状"太阳镜），DDLoss 和 PDLoss 无法显式解耦这些属性，此时 ACCORD 的有效性依赖于超类关系的外推。当基模型本身对超类‑属性关系建模存在系统性偏差时，解耦能力会下降。  
- **基模型依赖薄弱**：ACCORD 的前提是 T2I 模型能通过隐式分类（DDLoss 的梯度闭式）和 CLIP 嵌入空间（PDLoss）可靠估计概念依赖；若基模型在特定概念对上存在显著偏差，正则化效果将受限。  
- **不适用于非扩散模型**：由于去噪依赖偏差源于扩散概率路径，该框架无法直接迁移至自回归生成模型 (如 LlamaGen)。  
- **需手动验证的点**：部分极端共现模式下（如训练图像中目标对象从不单独出现），仅靠依赖解耦能否完全消除耦合风险，仍需进一步评估；当前实验未系统覆盖此类单样本‑完全共现的场景。

**重要图表结论**  
- **图 2/3**：分别展示了 DDLoss 和 PDLoss 的计算流程，突出其无需修改网络结构、仅通过损失函数施加依赖约束的即插即用特性。  
- **图 6**：直接量化了损失函数的期望效应——DDLoss 抑制了去噪过程中条件依存系数 $r$ 的变化幅值，PDLoss 将余弦相似度偏差向零压缩——为理论分解提供了训练动态证据。  
- **图 10**：展示了 ACCORD 在训练提示中故意加入无关属性（如"蓝色帽子"）时，能选择性地仅个性化目标主体而不耦合该属性，这超出了常规的共现依赖解耦，体现了超类先验对无关属性的泛化过滤能力。  
- **图 12**：分别启用 PDLoss 和 DDLoss 的可视化表明，PDLoss 使生成主体更接近参考，DDLoss 则使背景和场景更贴合文本，二者组合实现了最协调的生成效果。

以上实验证据一致性高（置信度≥0.95），共同支撑了"概念耦合可被统计依赖偏差分解所解释，且可通过 DDLoss 与 PDLoss 有效缓解"的核心 claim。失败模式指出了训练提示覆盖面和基模型能力两个关键约束，为后续改进指明了方向。



## 定位与知识库关联

### 与基线及后续工作的关系
现有测试时微调个性化方法（DreamBooth、CustomDiffusion、LoRA、VisualEncoder、Break‑A‑Scene 等）均以扩散模型原始去噪损失为基础，辅以数据正则化（如先验保留损失）、权重正则化或启发式区域正则化（Figure 1 示例）。这些技术**并未显式建模并最小化概念间的统计依赖**，因此对"概念耦合"的缓解是间接且不充分的。ACCORD 的核心差异在于将概念耦合形式化为一个**统计依赖问题**，并通过定理 1（Section 3.3）将总依赖偏差分解为两可计算项：
$$\underbrace{\log r(\mathbf{c}_p,\mathbf{c}_g|\mathbf{x}_{\theta,0}) - \log r(\mathbf{c}_p,\mathbf{c}_g|\mathbf{x}_T)}_{\text{去噪依赖偏差}} + \underbrace{\log r(\mathbf{c}_p,\mathbf{c}_g) - \log r(\mathbf{c}_s,\mathbf{c}_g)}_{\text{先验依赖偏差}}$$
在此基础上提出即插即用的两个正则化损失——**DDLoss** 与 **PDLoss**。这一因果性调控（causal knob）是以前工作所缺失的。

ACCORD 本身不是一种新的个性化架构，而是一个**可装配的损失模块**，其改动点明确：
- **正则化机制**：从数据/权重/启发式损失间接缓解，转变为直接最小化去噪过程中的条件依存系数变化（DDLoss, Eq. (8)）和在 CLIP 语义空间中对齐与超类的先验依赖（PDLoss, Eq. (11)）。
- **损失函数**：在基方法原有损失上加权叠加，仅 DDLoss 用于不更新个性化嵌入的方法（如 DreamBooth、LoRA），两者同时作用否则；典型权重为 0.1‑0.3（DD）与 0.001‑0.003（PD），对取值不敏感（Table 6）。

实验表明，该模块集成到 CustomDiffusion 后在 DreamBench 上带来 CLIP‑I **+8.7**、DINO‑I **+8.7** 的提升；集成到 LoRA (SDXL) 在 StyleBench 上 CLIP‑T 超越 3.8B 参数的 Omnigen（33.6 vs 31.9）；在零样本人脸个性化中（IP‑Adapter）同样提升 Face‑Sim 1.6 点（Table 5）。消融实验（Table 3）证实 DDLoss 和 PDLoss 均有正向贡献且协同工作，对 SD1.5、SDXL、FLUX 等不同骨架保持普适性（置信度 0.95）。

与区域正则化（Break‑A‑Scene）等后续工作相比，ACCORD 的**依赖解耦思想更为根本**，后续集成也证实了其可叠加性（Table 9：CLIP‑I 从 51.6 提升至 53.2）。因此，ACCORD 在方法谱系中定位为：**将个性化中的概念干扰首次提升到统计依赖因果层面，并为所有扩散微调范式提供一个理论自洽的解耦正则化框架**。

### 适用边界与局限
ACCORD 的设计建立在扩散模型的隐式分类器性质（Theorem 2）之上，因此**不适用于无扩散过程的自回归生成模型**（如 LlamaGen）。即便在扩散模型内，其解耦效果也受制于以下因素：

1. **基模型依赖假设**：DDLoss 依赖基 T2I 模型能够准确建模不同条件组合下的去噪差异。若基模型本身对超类与一般概念的依赖关系建模存在系统性偏差，跨时间步的依赖约束就会失效（置信度 0.95）。
2. **提示词覆盖不足**：训练提示中未显式提及的概念（例如背景物体、配饰）无法被 DDLoss/PDLoss 直接约束其依赖关系，解耦程度完全依赖模型的泛化能力（Limitations 原文）。
3. **隐式属性耦合**：当参考图像中与个性化目标协调出现的属性（如特定材质、颜色）在训练提示中未被描述时，两种损失**无法显式消除这类耦合**，仅能依靠超类关系的泛化来弱化（置信度 0.9）。图 4 的失败案例也显示，在背景与目标高度纠缠时改善有限。
4. **计算开销**：集成 ACCORD 会引入额外前向传播（四种条件），使训练显存与时间适度上升（如 LoRA SDXL 从 51.2 GB/780 s 增至 60.8 GB/916 s，Table 15）。这在资源受限场景下可能构成瓶颈。

因此，ACCORD 最适合基模型能力较强、训练提示能覆盖主要共现概念的场景；对于开放域强纠缠或超类定义模糊的任务，其效果会衰减。

### 开放问题
- **未提示强纠缠概念的解耦**：当外部概念与个性化目标强统计绑定、但从未在训练提示中出现时（如固某人自带标志性饰品），现有依赖分解无法定位该依赖源。是否需要引入外部知识或场景图来显式建模此类隐性关联？
- **基模型偏差下的鲁棒性**：若扩散模型对特定条件组合的预测本身存在偏差（例如对某些超类的去噪估计不准确），DDLoss 的闭式解（Theorem 2）会引入系统误差。如何设计自适应校准或元学习机制来增强损失在不同基模型/域下的鲁棒性，尚待探索。
- **超类模糊场景的扩展**：PDLoss 的对齐依赖一个语义明确的超类（如"背包"超类"包"）；对于抽象风格或缺乏清晰超类的概念，先验依赖偏差的锚定目标如何构建？可能的方向是在 CLIP 空间聚类或利用 VLM 自动生成分层概念关系。

这些开放点标志着概念耦合的因果调控仍处于"有提示的统计解耦"阶段，向完全无监督、跨模态依赖感知的个性化迈进是下一步需要突破的方向。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/ACCORD_Alleviating_Concept_Coupling_through_Dependence_Regularization_for_Text_to_Image_Diffusion_Personalization.pdf

![[paperPDFs/ICLR_2026/ACCORD_Alleviating_Concept_Coupling_through_Dependence_Regularization_for_Text_to_Image_Diffusion_Personalization.pdf]]
