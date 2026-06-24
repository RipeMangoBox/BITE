---
title: "ReAlign: Text-to-Motion Generation via Step-Aware Reward-Guided Alignment"
type: paper
paper_level: A
venue: AAAI
year: 2026
pdf_ref: paperPDFs/arxiv_2025/ReAlign_Text_to_Motion_Generation_via_Step_Aware_Reward_Guided_Alignment.pdf
aliases:
- RRGSA
- ReAlign
tags:
- AAAI_2026
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: 在扩散逆过程中注入由步长感知奖励模型产生的奖励梯度（∇R(xt,c)），该奖励由文本对齐模块（语义一致性）和动作对齐模块（真实性）联合构成，能够在不同时间步适应噪声水平，引导采样轨迹同时兼顾概率密度和文本-动作对齐。
primary_logic: 无需对扩散模型进行微调，而是通过单独训练一个步长感知的奖励模型，在推理时将其奖励梯度直接融入逆向SDE/DDPM采样过程，实现即插即用的文本-动作对齐增强。
claims:
- ReAlign将文本-动作对齐奖励梯度引入逆向扩散采样，理论上推导出奖励引导的逆向SDE，能够动态调整采样方向。
- ReAlign即插即用，可无缝集成到多种扩散式文本-动作生成模型，在没有额外微调的情况下显著提升生成质量和对齐度。
- 步长感知训练对处理不同噪声水平至关重要，缺少步长感知的奖励模型在去噪步骤增多时性能远逊于完整ReAlign。
- "HumanML3D 上 R@1 (Top-1 R Precision) = MLD+ReAlign: 0.567"
---

# ReAlign: Text-to-Motion Generation via Step-Aware Reward-Guided Alignment

> [!tip] 核心洞察
> 无需对扩散模型进行微调，而是通过单独训练一个步长感知的奖励模型，在推理时将其奖励梯度直接融入逆向SDE/DDPM采样过程，实现即插即用的文本-动作对齐增强。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReAlign：基于步长感知奖励引导对齐的文本到动作生成 |
| 英文题名 | ReAlign: Text-to-Motion Generation via Step-Aware Reward-Guided Alignment |
| 会议/期刊 | AAAI 2026 |
| Links | [paper](https://arxiv.org/abs/2511.19217) · [Project](https://wengwanjiang.github.io/ReAlign-page) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | ReAlign (Reward-guided sampling Alignment) |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，R@1 (Top-1 R Precision) MLD+ReAlign: 0.567 vs MLD: 0.481 (+17.9% (相对提升))；FID MLD+ReAlign: 0.195 vs MLD: 0.473 (-58.8% (相对降低))；MM Dist MLD+ReAlign: 2.704 vs MLD: 2.913 (-7.2% (相对降低))。
> - KIT-ML 上，R@3 (Top-3 R Precision) MDM+ReAlign: 0.784 vs MDM: 0.731 (+7.3% (相对提升))。
> - HumanML3D (文本-动作检索) 上，R@1 ReAlign: 67.59 vs TMR: 63.04 (as cited in text) (+4.55 百分点)。

## 概述

文本到动作生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的三维人体运动序列。近年来，扩散模型（Diffusion Models）已成为该领域的主流范式，涌现出 **MDM**（Tevet et al., ICLR 2023）、**MLD**（Chen et al., CVPR 2023）、**Mo.Diffuse**（Zhang et al., TPAMI 2024）等一系列代表性工作。然而，这些方法面临一个根本性瓶颈：扩散模型的采样过程优先追求高概率密度区域，却无法保证生成动作与文本描述之间的语义一致性。其深层原因在于，现有方法普遍依赖基于文本-图像对训练的 CLIP 编码器来桥接文本与动作模态，这种跨模态迁移难以精确捕捉文本-动作之间的细粒度语义对齐关系。

针对上述问题，本文提出 **ReAlign（Reward-guided sampling Alignment）**，一种即插即用的奖励引导采样对齐框架。其核心思路是：在扩散模型的逆向去噪过程中，注入由步长感知奖励模型产生的奖励梯度，引导采样轨迹同时兼顾概率密度和文本-动作对齐质量。具体而言，ReAlign 包含两个关键设计：

1. **步长感知奖励模型**：通过在训练时向动作注入不同时间步的扩散噪声，并引入时间步令牌，使奖励模型能够适应去噪过程中不同噪声水平的动作输入，从而在任意去噪步上准确评估文本-动作语义对齐度。
2. **双对齐奖励机制**：将文本-动作语义对齐奖励与基于训练集参考动作的运动-运动真实性奖励相结合，共同构造奖励分布，以梯度形式介入逆向 SDE/DDPM 采样过程，实现分布偏移。

ReAlign 的最大优势在于**无需对底层扩散模型进行任何微调**，可无缝集成到各类扩散式文本-动作生成模型中。实验结果表明，在 HumanML3D 数据集上，将 ReAlign 应用于 MLD 后，Top-1 R Precision 相对提升 17.9%，FID 相对降低 58.8%；在 MDiff、MotionLCM、MoMask 等多种模型上均观察到一致的性能增益，验证了其作为通用对齐增强模块的有效性。

## 背景与动机

### 问题背景：文本到动作生成的语义对齐困境

文本到动作生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的三维人体动作序列。近年来，扩散模型（Diffusion Models）在该领域取得了显著进展，代表性工作包括直接在原始运动数据上建模的**MDM**（Tevet et al., ICLR 2023）、在潜空间中进行扩散的**MLD**（Chen et al., CVPR 2023）、以及**Mo.Diffuse**（Zhang et al., TPAMI 2024）和**MotionLCM**（Dai et al., ECCV 2025）等。这些方法通过逐步去噪从高斯噪声中恢复运动数据，在生成多样性和逼真度上表现优异。

然而，扩散式文本-动作生成面临一个核心瓶颈：**采样过程与语义对齐之间存在内在张力**。扩散模型在逆向采样时，其评分函数 $\nabla \log p_t(\mathbf{x}|c)$ 天然倾向于引导样本进入高概率密度区域——这保证了生成动作的统计真实性和模式覆盖，但并不能保证这些动作与给定的文本条件 $c$ 在语义上精确匹配。换言之，模型可能生成一个“看起来像真实动作”但“与文本描述不符”的序列。

### 现有方法的缺口

这一瓶颈的根源可归结为三个层面的不足：

**第一，文本编码器的语义偏差。** 现有方法普遍采用基于文本-图像对预训练的CLIP编码器来编码文本条件。由于CLIP的训练目标并非文本-动作对齐，其在运动语义空间中的表征能力有限，无法准确捕捉细粒度的文本-动作对应关系。这导致扩散模型在条件生成时缺乏可靠的语义指导信号。

**第二，对齐校正的滞后性。** 现有对齐方法（如基于强化学习的**ReinDiffuse**（Han et al., arXiv 2024）和**MotionRL**（Liu et al., arXiv 2024），以及偏好优化方法**SoPo**（Tan et al., NeurIPS 2025））通常在最终动作生成完成后才进行校正或反馈。这些事后对齐策略无法干预扩散过程中的中间状态——而扩散去噪恰恰是一个逐步细化的过程，早期步骤的语义偏差会累积并放大，最终导致不可逆的对齐失败。

**第三，噪声鲁棒性的缺失。** 扩散去噪过程中，中间状态 $\mathbf{x}_t$ 是带有不同程度噪声的运动表示。现有的文本-动作检索或评估模型（如**TMR**（Petrovich et al., ICCV 2023）、**LaMP**（Li et al., ICLR 2025））均假设输入为无噪声的干净动作，无法在噪声环境下准确评估语义对齐度。这使得在去噪过程中进行实时对齐引导变得极为困难。

### 核心动机：将奖励引导注入扩散采样

上述分析揭示了一个清晰的研究动机：**能否在不重新训练扩散模型的前提下，在推理时动态地将文本-动作对齐信号注入逆向扩散过程？**

ReAlign的核心洞察在于：将扩散采样视为一个可引导的轨迹优化问题。如Figure 2所示，扩散模型学习的采样分布 $p_t(\cdot)$（蓝色区域）覆盖了高概率密度区域，但其中仅有部分区域与文本条件高度对齐。理想情况下，采样应发生在兼顾概率密度和语义对齐的分布 $p_t^I(\cdot)$（绿色区域）上。ReAlign通过引入一个**步长感知的奖励模型**（Step-Aware Reward Model），在逆向SDE/DDPM的每一步计算当前带噪运动 $\mathbf{x}_t$ 与文本条件 $c$ 的对齐奖励 $R(\mathbf{x}_t, c)$，并将其梯度 $\nabla R(\mathbf{x}_t, c)$ 注入采样步骤，从而将采样轨迹从纯高概率区域“牵引”至高对齐区域。

这一设计的关键优势在于**即插即用**（Plug-and-Play）：奖励模型独立于扩散模型进行训练，推理时无需对底层生成模型进行任何微调，可无缝集成到MDM、MLD、Mo.Diffuse、MotionLCM等多种扩散式文本-动作生成框架中。

## 核心创新

ReAlign 的核心创新在于将文本-动作对齐问题从“事后评估”前置到“生成过程内部”，通过一个**即插即用、无需微调扩散模型**的奖励引导机制，在逆向扩散采样的每一步动态调整采样轨迹。其关键创新点可归纳为三个紧密耦合的“changed slots”：

### 1. 逆向扩散采样步：从纯概率密度驱动到奖励梯度联合驱动

基线扩散式文本-动作生成方法（如 **MDM**，Tevet et al., ICLR 2023；**MLD**，Chen et al., CVPR 2023）的采样过程仅依赖扩散模型自身学到的评分函数 $\nabla \log p_t(\mathbf{x}|c)$，优先保证生成动作处于高概率密度区域，却无法显式保证动作与文本描述的语义一致性。

ReAlign 将这一机制改造为**奖励梯度联合驱动**的采样步。具体而言，在 DDPM 逆向链的每一步，去噪后的样本上直接叠加由步长感知奖励模型产生的奖励梯度：

$$
\mathbf{x}_{t-1} = \frac{1}{\sqrt{\alpha_t}} \big( \bar{\mathbf{x}}_{t-1} + \sqrt{\beta_t} \boldsymbol{\epsilon} \big) + \nabla R(\mathbf{x}_t, c)
$$

其中 $\nabla R(\mathbf{x}_t, c)$ 是双对齐奖励的梯度。为保证采样稳定性，论文去除了原始推导中奖励项上的权重 $\beta_t / \sqrt{\alpha_t}$（见 Algorithm 2 及 Eq. (13)）。这一改造的理论基础是奖励引导的逆向 SDE（Eq. (11)），它将理想采样分布 $p_t^I \propto p_t \cdot p_t^r$ 的梯度融入采样过程，使采样点从纯高概率区域移向**兼顾概率密度与文本-动作语义对齐**的区域（见 Figure 2 示意）。

**因果机制**：奖励梯度充当了采样轨迹的“语义校正力”——当带噪动作 $\mathbf{x}_t$ 与文本条件 $c$ 对齐较差时，$\nabla R$ 将采样推向对齐更优的方向；当对齐已足够好时，梯度项自然减弱，扩散模型自身的概率密度约束仍占主导。

### 2. 文本-动作对齐机制：从无外部信号到双对齐奖励分布

基线方法的生成过程完全依赖扩散模型内部隐式学到的文本-动作关联，缺乏显式的对齐评估与反馈。现有对齐方法（如基于检索的评估器）通常假设输入为干净动作，无法适应去噪过程中的噪声动作输入。

ReAlign 构建了一个**双对齐奖励分布** $p_t^r \propto \exp(R)$，由两个互补的奖励分量加权组合：

- **文本-动作奖励 $R_\varphi$**：由步长感知奖励模型计算带噪运动 $\mathbf{x}_t$ 与文本条件 $c$ 的嵌入余弦相似度 $R_\varphi = \cos(\mathbf{z_x}, \mathbf{z}_c)$，直接量化语义对齐程度（Eq. (6)）。
- **运动-运动奖励 $R_m$**：从训练集中检索与文本最匹配的参考动作 $\mathbf{x}^c$（Eq. (7)），计算生成动作与参考动作嵌入的余弦相似度 $R_m = \cos(\mathbf{z_x}, \mathbf{z}_{\mathbf{x}^c})$（Eq. (8)），激励动作真实性和模式跟随。

最终双对齐奖励为 $R = \mu R_\varphi + \eta R_m$（Eq. (9)），通过 Softmax 映射为奖励分布 $p_t^r$（Eq. (10)）。消融实验（Table 5）证实：仅使用 T2M 奖励即可显著降低 FID，叠加 M2M 奖励后进一步提升指标——在 HumanML3D 上，MLD+ReAlign 的 FID 从 0.473 降至 0.195（相对降低 58.8%），R@1 从 0.481 提升至 0.567（相对提升 17.9%）。

**因果机制**：$R_\varphi$ 提供语义锚定，$R_m$ 提供运动先验约束。两者协同使奖励分布 $p_t^r$ 在语义相关且运动合理的区域赋予更高概率，引导采样远离“高概率但语义错误”的陷阱。

### 3. 噪声鲁棒性处理：从噪声盲区到步长感知

这是支撑上述两个创新的关键使能技术。现有文本-动作检索/评估模型（如 **TMR**，Petrovich et al., ICCV 2023）假设输入为无噪声的干净动作，无法在扩散中间步骤的噪声动作上可靠工作。

ReAlign 通过**步长感知训练**（Step-Aware Training）赋予奖励模型噪声适应能力：训练时以一定概率向动作注入扩散噪声（随机时间步 $t$），并在运动表征中注入时间步令牌 $[e_t]$，使模型显式感知当前噪声水平（见 Algorithm 1 及 Figure 3）。奖励模型由对比损失 $\mathcal{L}_C$ 和表示损失 $\mathcal{L}_R$ 联合优化（Eq. (5)），学习在不同噪声程度下评估文本-动作对齐。

Figure 4 的消融实验直接验证了这一创新的必要性：缺少步长感知的奖励模型（w/o Step-Aware）在去噪步数变化时性能显著下降，甚至出现“奖励黑客”效应（过度优化奖励指标而损害生成质量），而完整 ReAlign 在所有去噪步数下均保持最优，且能稳定兼容无分类器引导（CFG），两者叠加达到最佳性能（Table 6：MLD+CFG+ReAlign 在 HumanML3D 上 FID=0.195，MM Dist=2.704）。

**因果机制**：时间步令牌 $[e_t]$ 为奖励模型提供了“噪声程度”的上下文信息，使其学到的对齐评估函数 $R_\varphi(\mathbf{x}_t, c)$ 对噪声水平具有不变性——在不同 $t$ 下，模型知道如何从不同程度的噪声动作中提取可靠的语义特征，从而在整个去噪链上提供一致的引导信号。

### 创新协同效应

三个 changed slots 形成闭环：步长感知训练使奖励模型能可靠评估噪声动作（Slot 3），可靠的对齐评估支撑双对齐奖励分布 $p_t^r$ 的构建（Slot 2），奖励分布以梯度形式注入逆向采样步（Slot 1），最终实现无需微调扩散模型的即插即用对齐增强。Table 4 的跨模型验证（MDiff、MLD、MDM、MotionLCM、MoMask 等均稳定获益）证实了这一协同设计的泛化能力。

## 整体框架

ReAlign 的整体框架以**即插即用**为设计原则，在不修改任何扩散式文本-动作生成模型参数的前提下，通过外挂一个**步长感知奖励模型**（Step-Aware Reward Model），在逆向扩散采样的每一步注入奖励梯度，引导采样轨迹从单纯的高概率密度区域转向兼顾文本-动作语义对齐的区域。

### 核心思路：理想采样分布

现有扩散模型在去噪过程中仅依据学习到的评分函数 $\nabla \log p_t(\mathbf{x}|c)$ 进行采样，其生成结果倾向于分布的高概率区域，但未必与文本条件 $c$ 在语义上高度一致。ReAlign 的核心洞察是引入一个**理想采样分布** $p_t^I$，将原始采样分布 $p_t$ 与一个反映文本-动作对齐程度的**奖励分布** $p_t^r$ 相融合：

$$p_t^I(\mathbf{x}|c) = p_t(\mathbf{x}|c) \, p_t^r(\mathbf{x}|c) \, / \, Z(c) \quad \text{(Eq. 3)}$$

其中 $Z(c)$ 为归一化常数。这一设计的本质是**在保持动作本身概率合理性的同时，显式提升文本-动作语义一致性**（Figure 2 以蓝/绿区域直观示意了这一分布偏移）。

### 奖励引导的逆向扩散

将理想分布代入逆向 SDE，得到**奖励引导的逆向 SDE**（Theorem 2）：

$$\mathbf{dx} = \Big[ \mathbf{f}(\mathbf{x}, t) - g(t)^2 \nabla \big( \log p_t(\mathbf{x}|c) + R(\mathbf{x}_t, c) \big) \Big] \mathrm{d}t + g(t) \mathrm{d}\mathbf{w} \quad \text{(Eq. 11)}$$

其中 $R(\mathbf{x}_t, c)$ 为双对齐奖励函数。在 DDPM 采样框架下，为保证采样稳定性，进一步移除奖励项上的权重系数 $\beta_t/\sqrt{\alpha_t}$，得到实用的**奖励引导去噪步**：

$$\mathbf{x}_{t-1} = \frac{1}{\sqrt{\alpha_t}} \big( \bar{\mathbf{x}}_{t-1} + \sqrt{\beta_t} \boldsymbol{\epsilon} \big) + \nabla R(\mathbf{x}_t, c) \quad \text{(Eq. 13, Algorithm 2)}$$

即在标准 DDPM 去噪结果 $\bar{\mathbf{x}}_{t-1}$ 之上，直接叠加奖励梯度 $\nabla R(\mathbf{x}_t, c)$，实现分布偏移。

### Pipeline 模块组成与数据流

ReAlign 的完整 pipeline 由以下四个模块串联构成：

1. **步长感知奖励模型 $R_\varphi$（Figure 3）**  
   - **输入**：带噪运动 $\mathbf{x}_t$（来自扩散过程的任意时间步 $t$）、文本条件 $c$  
   - **处理**：将时间步嵌入 $t$ 与运动嵌入 $\mathbf{x}_t^k$ 拼接为时间感知令牌，与文本嵌入 $c$ 在潜空间中通过对比损失 $\mathcal{L}_C$ 和表示损失 $\mathcal{L}_R$ 联合训练对齐（Eq. 5）  
   - **输出**：文本-动作语义对齐得分 $R_\varphi(\mathbf{x}_t, c) = \cos(\mathbf{z_x}, \mathbf{z}_c)$（Eq. 6）  
   - **关键特性**：训练时以一定概率向干净动作注入不同时间步的扩散噪声，使奖励模型具备**步长感知的噪声适应能力**（Algorithm 1），这是区别于现有文本-动作检索模型（如 TMR）的核心创新

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2511_19217/figures/003_Figure_3.jpg]]
*Figure 3: Framework of step-aware reward model. During this process, time-aware tokens, consisting of timestep embedding t and motion embeddings $\boldsymbol { x } _ { t } ^ { k }$ , are aligned with text embedding c in the latent space and reconstructed via the decoder, with the encoder and decoder jointly optimized by contrastive loss $\mathcal { L } _ { C }$ and representation loss $\mathcal { L } _ { R }$ (Petrovich, Black, and Varol 2022)

2. **参考动作检索与运动-运动奖励 $R_m$**  
   - **输入**：文本条件 $c$、训练集 $\mathcal{D}_{tr}$  
   - **处理**：利用步长感知奖励模型从训练集中检索与 $c$ 最匹配的无噪声参考动作 $\mathbf{x}^c = \arg\max_{\mathbf{x} \in \mathcal{D}_{tr}} R_\varphi(\mathbf{x}, c)$（Eq. 7）  
   - **输出**：运动-运动奖励 $R_m(\mathbf{x}_t, c) = \cos(\mathbf{z_x}, \mathbf{z}_{\mathbf{x}^c})$（Eq. 8），通过比较生成动作与参考动作的嵌入相似度，激励运动真实性和模式一致性

3. **双对齐奖励分布 $p_t^r$**  
   - **输入**：$R_\varphi$ 和 $R_m$  
   - **处理**：加权组合为双对齐奖励 $R(\mathbf{x}_t, c) = \mu R_\varphi(\mathbf{x}_t, c) + \eta R_m(\mathbf{x}_t, c)$（Eq. 9），再通过 Softmax 映射为概率分布 $p_t^r(\mathbf{x}_t|c) \propto \exp(R(\mathbf{x}_t, c))$（Eq. 10）  
   - **输出**：奖励分布 $p_t^r$，用于在逆向 SDE 中提供梯度信号

4. **奖励引导的 DDPM 采样（Algorithm 2）**  
   - **输入**：预训练扩散模型的去噪网络、步长感知奖励模型 $R_\varphi$、训练集 $\mathcal{D}_{tr}$（用于检索参考动作）、文本条件 $c$  
   - **处理**：在逆向扩散的每一步 $t$ 中，(a) 执行标准 DDPM 去噪得到 $\bar{\mathbf{x}}_{t-1}$；(b) 计算当前带噪样本 $\mathbf{x}_t$ 的奖励梯度 $\nabla R(\mathbf{x}_t, c)$；(c) 将二者相加得到 $\mathbf{x}_{t-1}$（Eq. 13）  
   - **输出**：最终去噪完成的干净动作 $\mathbf{x}_0$

### 即插即用集成方式

ReAlign 完全独立于扩散模型的训练过程，**无需对底层生成模型进行任何微调**。集成时只需：
- 加载预训练好的步长感知奖励模型权重
- 在推理循环中，将标准 DDPM/DDIM 采样步替换为 Algorithm 2 中的奖励引导去噪步
- 调整超参数 $\mu$、$\eta$ 控制文本对齐与运动真实性的平衡

该设计已在 **MDM**（Tevet et al., ICLR 2023）、**MLD**（Chen et al., CVPR 2023）、**Mo.Diffuse**（Zhang et al., TPAMI 2024）、**MotionLCM**（Dai et al., ECCV 2025）、**MoMask**（Guo et al., CVPR 2024）等多种扩散式及离散式动作生成模型上验证了即插即用能力（Table 1, Table 4），均稳定带来生成质量和对齐度的显著提升。

## 核心模块与公式推导

### 3.1 理想采样分布与奖励引导的逆向SDE

ReAlign 的核心动机源于一个观察：标准扩散模型在逆向采样时优先探索高概率密度区域，但高概率密度并不保证文本-动作语义对齐。为此，ReAlign 定义了一个**理想采样分布** $p_t^I(\mathbf{x}|c)$，将原始扩散模型的采样分布 $p_t(\mathbf{x}|c)$ 与一个奖励分布 $p_t^r(\mathbf{x}|c)$ 相乘：

$$p_t^I(\mathbf{x}|c) = p_t(\mathbf{x}|c) \, p_t^r(\mathbf{x}|c) \, / \, Z(c) \tag{3}$$

其中 $Z(c)$ 为归一化常数。奖励分布 $p_t^r$ 编码了文本-动作语义对齐的偏好，使采样轨迹从纯概率密度最大化转向概率密度与语义对齐的联合优化（Figure 2 示意了这一偏移）。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2511_19217/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of the sampling process in diffusion-based motion generation frameworks. The blue region represents the sampling distribution $p _ { t } ( \cdot$ ) learned by the diffusion model, while the green region depicts the ideal sampling distribution $p _ { t } ^ { I } ( \cdot$ ) achieved by incorporating our proposed reward-guided sampling strategy with the sampling distribution $p _ { t } ( \cdot$ )

基于此理想分布，ReAlign 将标准逆向SDE

$$\mathrm{d}\mathbf{x} = [\mathbf{f}(\mathbf{x}, t) - g(t)^2 \nabla \log p_t(\mathbf{x}|c)] \mathrm{d}t + g(t) \mathrm{d}\mathbf{w} \tag{2}$$

修改为**奖励引导的逆向SDE**：

$$\mathbf{dx} = \Big[ \mathbf{f}(\mathbf{x}, t) - g(t)^2 \nabla \big( \log p_t(\mathbf{x}|c) + \log p_t^r(\mathbf{x}|c) \big) \Big] \mathrm{d}t + g(t) \mathrm{d}\mathbf{w} \tag{4}$$

进一步，由于奖励分布 $p_t^r \propto \exp(R(\mathbf{x}_t, c))$，其对数梯度可直接替换为奖励梯度，得到简化形式：

$$\mathbf{dx} = \Bigl[ \mathbf{f}(\mathbf{x}, t) - g(t)^2 \nabla \big( \log p_t(\mathbf{x}|c) + R(\mathbf{x}_t, c) \big) \Bigr] \mathbf{d}t + g(t) \mathbf{d w} \tag{11}$$

这一推导（Theorem 2）将奖励信号以梯度形式注入逆向过程，是即插即用推理阶段引导的理论基础。

### 3.2 步长感知奖励模型

奖励模型 $R_\varphi$ 需要评估**带噪运动** $\mathbf{x}_t$ 与文本条件 $c$ 的语义对齐度，而现有文本-动作检索模型（如 TMR）假设输入为干净动作，无法适应扩散过程中不同时间步的噪声水平。ReAlign 通过**步长感知训练**解决这一问题。

**架构**：如图 Figure 3 所示，奖励模型由编码器-解码器构成。输入包含：
- 时间步嵌入 $t$ 与运动嵌入 $\mathbf{x}_t^k$ 拼接的**时间感知令牌**（step-aware tokens）
- 文本嵌入 $c$

编码器将二者映射到共享潜空间，解码器重建运动表征。模型通过联合优化对比损失 $\mathcal{L}_C$ 和表示损失 $\mathcal{L}_R$ 训练：

$$\mathcal{L}_{RM}(\boldsymbol{\varphi}; \mathbf{x}_t, c) = \mathcal{L}_C(\boldsymbol{\varphi}; \mathbf{x}_t, c) + \mathcal{L}_R(\boldsymbol{\varphi}; \mathbf{x}_t, c) \tag{5}$$

**步长感知策略**：训练时以一定概率向运动数据注入随机时间步的扩散噪声，使奖励模型学会在不同噪声水平下评估对齐度。这一设计的关键性在消融实验中得到了验证：缺少步长感知的奖励模型在多步去噪时性能显著下降，甚至出现奖励黑客效应（Figure 4）。

**文本-动作对齐得分**：奖励模型输出运动嵌入 $\mathbf{z_x}$ 与文本嵌入 $\mathbf{z}_c$ 的余弦相似度：

$$R_{\varphi}(\mathbf{x}, c) = \cos(\mathbf{z_x}, \mathbf{z}_c) \tag{6}$$

### 3.3 运动-运动奖励与双对齐奖励

仅靠文本-动作对齐可能不足以约束生成运动的真实性和模式一致性。ReAlign 引入**运动-运动奖励** $R_m$，以训练集中与文本最匹配的干净动作为锚点：

$$\mathbf{x}^c = \arg \max_{\mathbf{x} \in \mathcal{D}_{tr}} R_{\varphi}(\mathbf{x}, c) \tag{7}$$

$$R_m(\mathbf{x}_t, c) = \cos(\mathbf{z_x}, \mathbf{z}_{\mathbf{x}^c}) \tag{8}$$

其中 $\mathbf{z}_{\mathbf{x}^c}$ 为检索到的参考动作嵌入。该奖励鼓励生成运动在表征空间中靠近真实运动模式。

最终，**双对齐奖励**将文本-动作奖励与运动-运动奖励加权组合：

$$R(\mathbf{x}_t, c) = \mu R_{\varphi}(\mathbf{x}_t, c) + \eta R_m(\mathbf{x}_t, c) \tag{9}$$

并通过 Softmax 映射为奖励分布：

$$p_t^r(\mathbf{x}_t|c) = \exp(R(\mathbf{x}_t, c)) \, / \, Z^r(c) \tag{10}$$

### 3.4 奖励引导的DDPM采样

将奖励梯度直接应用于DDPM逆向链，得到**奖励引导的去噪步**。为保证采样稳定性，ReAlign 移除了原始推导中的权重系数 $\beta_t / \sqrt{\alpha_t}$，得到去权重版本：

$$\mathbf{x}_{t-1} = \frac{1}{\sqrt{\alpha_t}} \big( \bar{\mathbf{x}}_{t-1} + \sqrt{\beta_t} \boldsymbol{\epsilon} \big) + \nabla R(\mathbf{x}_t, c) \tag{13}$$

其中 $\bar{\mathbf{x}}_{t-1}$ 为DDPM标准去噪输出，$\boldsymbol{\epsilon}$ 为噪声项，$\nabla R(\mathbf{x}_t, c)$ 是步长感知双对齐奖励在 $\mathbf{x}_t$ 处的梯度。该步骤在每一轮去噪后施加奖励引导，逐步将采样轨迹推向高对齐区域（Algorithm 2 给出了完整伪代码）。

**关键设计决策**：奖励模型在推理时需对每个时间步的 $\mathbf{x}_t$ 进行前向和反向传播以计算梯度，同时需从训练集检索参考动作。这引入了额外计算开销，但换来了无需微调扩散模型的即插即用能力。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2511_19217/figures/005_Table_2.jpg]]
*Table 2: Comparison of text-to-motion generation performance on the KIT-ML dataset. Bold highlights the best results. Figure 4: Comparison of motion generation quality across denoising steps for the MLD w/o ReAlign, MLD w/o Step-Aware, and MLD w/ Step-Aware (ReAlign). ReAlign consistently outperforms the others, highlighting the necessity of explicit noise handling during denoising*

## 实验与分析

### 主实验结果

ReAlign作为一种即插即用的奖励引导对齐策略，在HumanML3D和KIT-ML两个标准数据集上展现出显著且一致的性能增益。

在HumanML3D数据集上，以MLD（Chen et al., CVPR 2023）为基线模型集成ReAlign后，文本-动作对齐指标R@1从0.481提升至0.567，相对提升17.9%；生成质量指标FID从0.473降至0.195，相对降低58.8%；多模态距离MM Dist从2.913降至2.704，相对降低7.2%（Table 1）。当进一步结合无分类器引导（CFG）时，MLD+CFG+ReAlign达到了FID=0.195、MM Dist=2.704的最优结果，验证了ReAlign与CFG的兼容互补性（Table 6）。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2511_19217/figures/004_Table_1.jpg]]
*Table 1: Comparison of text-to-motion generation performance on the HumanML3D dataset. These metrics are evaluated by the evaluator from TM2T (Guo et al. 2022b). The arrows ↑, ↓, and → indicate higher, lower, and closer-to-real-motion values are better, respectively. Bold highlights the best results. Percentages in bracket indicate improvements over respective baselines*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2511_19217/figures/008_Table_6.jpg]]
*Table 6: Ablation study of the guidance strategy. Evaluation conducted on the HumanML3D with MLD (2023b) as the baseline. “CFG” and “ReAlign” denote the classifierfree guidance and our ReAlign, respectively*

在KIT-ML数据集上，MDM（Tevet et al., ICLR 2023）集成ReAlign后，R@3从0.731提升至0.784，相对提升7.3%（Table 2）。

ReAlign的即插即用能力在多种扩散式文本-动作生成模型上得到系统验证（Table 4）。在HumanML3D上，MDiff（Zhang et al., TPAMI 2024）集成ReAlign后R@1从0.491提升至0.534（+8.8%）；MotionLCM（Dai et al., ECCV 2025）、MoMask（Guo et al., CVPR 2024）等方法在集成后同样获得稳定提升。这些结果表明，ReAlign无需对底层扩散模型进行任何微调，即可有效改善生成动作与文本描述之间的语义对齐度。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2511_19217/figures/009_Table_4.jpg]]
*Table 4: Performance improvement of motion generation methods with our step-aware reward guidance. Results are reported on the HumanML3D dataset, showing improvements over baseline methods*

在文本-动作检索任务上，ReAlign同样表现突出（Table 3）。在HumanML3D上，ReAlign的T2M检索R@1达到67.59%，超越TMR（Petrovich et al., ICCV 2023）的63.04%以及LaMP（Li et al., ICLR 2025）等基线方法。值得注意的是，Table 3中的“Noise”列表明ReAlign是少数能处理去噪过程中含噪动作输入的方法，这得益于其步长感知训练策略。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2511_19217/figures/007_Table_3.jpg]]
*Table 3: Comparison of Text-to-motion (left) and motion-to-text (right) retrieval methods on the HumanML3D and KIT-ML datasets. The column “Noise” indicates whether the method can handle noisy motion from the denoised process*

### 消融实验

**奖励组件消融**（Table 5）：在HumanML3D上以MLD为基线，逐步添加奖励组件以评估各自贡献。仅加入文本-动作对齐奖励（T2M）时，FID从2.932降至2.750，MM Dist从2.913降至2.754；进一步加入运动-运动对齐奖励（M2M）后，FID降至2.704。这表明T2M奖励是语义对齐的核心驱动力，而M2M奖励通过引入训练集参考动作的锚定效应，进一步改善了运动真实性和模式一致性。

**步长感知训练消融**（Figure 4与Table 5）：步长感知策略（SA）是ReAlign的关键设计。在缺少步长感知的版本中，奖励模型无法适应不同噪声水平下的运动输入，导致在去噪步数变化时性能显著下降，甚至出现“奖励黑客”效应——即奖励模型被高噪声输入欺骗而给出错误引导。完整ReAlign（含SA）在所有去噪步数下均保持最优，且FID进一步降至0.195，验证了显式建模噪声水平的必要性。

**引导策略消融**（Table 6）：对比仅MLD、MLD+CFG、MLD+ReAlign、MLD+CFG+ReAlign四种配置。ReAlign单独使用时FID从0.473降至0.195，MM Dist从2.913降至2.704；CFG单独使用时FID降至0.217，MM Dist降至2.726；两者结合达到FID=0.195、MM Dist=2.704的最优结果，证明奖励引导与无分类器引导在机制上互补，可叠加增效。

### 失败模式与局限性

尽管ReAlign在多个基准上表现优异，仍存在以下局限：

1. **推理计算开销**：奖励引导采样在每一步去噪中需运行步长感知奖励模型的前向/反向传播以计算梯度，并从训练集中检索参考动作。论文未提供详细的推理延迟对比数据，实际部署中可能影响实时性。

2. **奖励设计的单一性**：当前工作仅关注文本-动作语义对齐和运动真实性，尚未探索物理合理性奖励、轨迹约束奖励或风格一致性奖励等更丰富的引导信号。

3. **数据集泛化性**：实验聚焦于HumanML3D和KIT-ML两个标准数据集，未在更大规模或更多样化的数据集（如FineMotion）上进行验证。

4. **奖励权重调度不透明**：论文未给出步长感知策略中奖励权重μ和η在不同时间步的具体调度方案或变化曲线，其最优配置可能依赖于经验调参。

5. **高维空间中的梯度效应**：奖励引导在高维动作空间中的梯度注入是否会导致模式坍塌或样本多样性损失，文中未进行深入讨论。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2511_19217/figures/006_Table.jpg]]

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2511_19217/figures/010_Table_5.jpg]]
*Table 5: Effectiveness of Reward Sampling. We assess the Re-Align, including T2M and M2M alignment rewards, along with the step-aware strategy in text-to-motion generation on Table 5: Ablation study of the text-to-motion on HumanML3D dataset. “T2M”, “M2M” and “SA” denote the text-to-motion reward, motion-to-motion reward and stepaware training, respectively*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2511_19217/figures/001_Figure_1.jpg]]
*Figure 1: Visual comparison of text-to-motion generation. This figure presents motions generated by existing methods, such as Mo.Diffuse (2024), MDM (2023), MLD (2023b), and MotionLCM (2025). Our ReAlign enhances these models to produce motions that align more closely with text inputs*

## 方法谱系与知识库定位

### 1. 问题定位：扩散式文本-动作生成的对齐鸿沟

现有扩散式文本-动作生成方法（如 **MDM** (Tevet et al., ICLR 2023)、**MLD** (Chen et al., CVPR 2023)、**Mo.Diffuse** (Zhang et al., TPAMI 2024)）的核心瓶颈在于：它们依赖的文本编码器（通常为CLIP）基于文本-图像对训练，无法准确捕捉文本与动作之间的细粒度语义对应关系。扩散模型的采样过程本质上是追求高概率密度区域，而非语义对齐最优区域，这导致生成的动作在物理上合理但语义上偏离文本描述。

现有的后处理对齐方案（如 **ReinDiffuse** (Han et al., arXiv 2024)、**MotionRL** (Liu et al., arXiv 2024)）试图在最终动作生成后进行校正，但面临一个根本性困难：它们假设输入为无噪声的干净动作，无法处理扩散去噪过程中的中间噪声状态。这种“事后对齐”范式无法在采样轨迹的早期阶段干预语义方向。

ReAlign 的方法论定位是：**将对齐问题从“事后校正”迁移到“过程中引导”**，在不修改底层扩散模型的前提下，通过一个独立训练的步长感知奖励模型，在推理时以梯度形式介入逆向扩散的每一步。

### 2. 方法谱系中的位置

#### 2.1 与扩散式文本-动作生成基线的关系

ReAlign 并非一个独立的生成模型，而是一个**即插即用的推理时对齐增强模块**。它可以无缝集成到以下扩散式生成框架中：

| 基线方法 | 核心机制 | ReAlign 的集成方式 |
|---------|---------|------------------|
| **MDM** (Tevet et al., ICLR 2023) | 在原始运动数据空间进行扩散 | 在DDPM逆向步中加入奖励梯度 ∇R(x_t, c) |
| **MLD** (Chen et al., CVPR 2023) | 在VAE潜空间进行扩散 | 在潜空间去噪步中加入奖励梯度 |
| **Mo.Diffuse** (Zhang et al., TPAMI 2024) | 基于Transformer的扩散架构 | 奖励梯度注入其去噪过程 |
| **MotionLCM** (Dai et al., ECCV 2025) | 潜一致性模型快速采样 | 在一致性映射步中加入对齐引导 |
| **MoMask** (Guo et al., CVPR 2024) | 离散掩码建模 | 可集成至其生成流程 |

关键区别在于：上述基线方法的文本-动作对齐完全依赖扩散模型自身学到的条件分布 p_t(x|c)，而 ReAlign 通过引入外部奖励分布 p_t^r(x|c) 将采样目标修正为理想分布 p_t^I ∝ p_t · p_t^r。这种设计使得对齐信号与生成过程解耦，无需对任何底层模型进行微调。

#### 2.2 与后处理对齐方法的对比

| 方法 | 对齐时机 | 噪声适应性 | 核心机制 |
|------|---------|-----------|---------|
| **ReinDiffuse** (Han et al., arXiv 2024) | 生成完成后 | 无 | 强化学习细化 |
| **MotionRL** (Liu et al., arXiv 2024) | 生成完成后 | 无 | 多奖励RL对齐 |
| **SoPo** (Tan et al., NeurIPS 2025) | 训练时 | 无 | 半在线偏好优化 |
| **ReAlign** (本文) | 去噪过程中每一步 | 有（步长感知） | 奖励梯度引导逆向SDE |

后处理方法的共同局限在于：它们只能对最终输出进行修正，无法影响扩散模型在早期去噪步中的语义方向选择。ReAlign 通过步长感知训练使奖励模型能够理解不同噪声水平下的运动表征，从而在去噪全程提供有效的对齐信号。

#### 2.3 与文本-动作检索方法的关系

**TMR** (Petrovich et al., ICCV 2023) 和 **LaMP** (Li et al., ICLR 2025) 等方法专注于学习文本-动作联合嵌入空间以支持检索任务，但它们假设输入为干净动作，无法处理扩散过程中的噪声动作。ReAlign 的步长感知奖励模型在训练时以一定概率向动作注入扩散噪声（随机时间步），并在运动表征中注入时间步令牌 [e_t]，使其具备跨噪声水平的泛化能力。Table 3 的结果表明，ReAlign 在文本-动作检索任务上（R@1: 67.59%）显著优于 TMR（63.04%），且是少数能处理噪声动作的方法。

### 3. 适用边界与局限

#### 3.1 已验证的适用范围

- **数据集**：HumanML3D 和 KIT-ML 两个标准文本-动作数据集上进行了全面验证。
- **模型架构**：在基于原始运动空间的扩散模型（MDM）、潜空间扩散模型（MLD）、Transformer扩散模型（Mo.Diffuse）、一致性模型（MotionLCM）和离散掩码模型（MoMask）上均验证了即插即用能力。
- **评估指标**：R Precision、FID、MM Dist、Diversity，以及检索任务的 Recall@K。
- **与CFG的兼容性**：Table 6 表明 ReAlign 与无分类器引导（CFG）互补，两者叠加可达到最优性能（MLD+CFG+ReAlign 在 HumanML3D 上 FID=0.195）。

#### 3.2 已知局限

1. **奖励类型单一**：当前工作仅关注文本-动作语义对齐，尚未探索物理合理性奖励（如足部滑动惩罚）、轨迹约束奖励、风格一致性奖励等扩展方向。这限制了 ReAlign 在需要多重约束的场景（如物理仿真、交互式动画）中的直接应用。

2. **推理计算开销**：奖励引导采样在每一步去噪时需要：
   - 运行步长感知奖励模型进行前向传播以计算 R(x_t, c)
   - 对奖励模型进行反向传播以计算梯度 ∇R(x_t, c)
   - 从训练集中检索参考动作 x^c
   
   论文未提供详细的推理延迟对比数据，这一开销在实时应用场景中的可接受性需要进一步验证。

3. **数据集泛化性**：实验聚焦于 HumanML3D 和 KIT-ML，未在更大规模或更多样化的数据集（如 FineMotion、BABEL）上进行验证。当新任务的文本-动作分布与训练集有显著差异时，步长感知奖励模型是否依然有效尚不明确。

4. **多样性与模式坍塌风险**：奖励引导本质上是将采样分布向高奖励区域偏移，在高维动作空间中可能导致样本多样性损失。文中未深入讨论奖励引导强度（μ、η权重）与生成多样性之间的权衡关系。

### 4. 开放问题

1. **步长感知的调度机制**：步长感知策略如何在不同时间步实际调节奖励权重 μ 和 η？论文未给出具体的调度方案或曲线。在早期去噪步（高噪声）和后期去噪步（低噪声），T2M 奖励和 M2M 奖励的相对重要性可能不同，这一动态调节机制值得深入研究。

2. **计算效率优化**：能否通过奖励模型的轻量化设计（如知识蒸馏、量化）或梯度近似的免反向传播方法来降低推理开销？

3. **多模态条件扩展**：该方法能否扩展到音频-文本联合条件、动作预测、动作过渡等多模态可控生成任务？步长感知奖励模型的多条件泛化能力需要验证。

4. **奖励模型的迁移能力**：当目标域的动作风格或文本描述分布与训练集存在域偏移时，步长感知奖励模型是否需要微调？零样本迁移的性能边界在哪里？

5. **理论分析深度**：奖励引导采样对扩散模型原有概率密度保真度的影响缺乏定量分析。是否存在一个理论上的最优奖励强度，在不对抗原始分布的前提下最大化对齐增益？

## 原文 PDF

![[paperPDFs/arxiv_2025/ReAlign_Text_to_Motion_Generation_via_Step_Aware_Reward_Guided_Alignment.pdf]]