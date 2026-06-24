---
title: Training-Free Motion-Guided Video Generation with Enhanced Temporal Consistency Using Motion Consistency Loss
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Training_Free_Motion_Guided_Video_Generation_with_Enhanced_Temporal_Consistency_Using_Motion_Consistency_Loss.pdf
aliases:
- INMCLMVG
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 通过显式定义并优化帧间特征相关性模式的一致性损失（运动一致性损失），可以将参考视频的运动模式更有效地迁移到生成视频，从而在不更新模型参数的前提下提高时间一致性和运动精度。
primary_logic: 利用扩散模型时间注意力中间层的特征相关性模式作为软运动轨迹的表示，并通过梯度引导的方式施加一致性约束，能够与初始噪声隐含运动引导形成互补，仅需少量稀疏关键点即可达到良好的运动控制效果。
claims:
- 仅使用初始噪声引导而不加运动一致性损失时，视频细节出现时间不一致现象（如狮子尾巴和爪子丢失）。
- 相比于FreeTraj，所提方法在轨迹控制任务的mIoU和CLIP-SIM-GTBox指标上均有提升，且人类评估大幅领先。
- 与需要训练的MotionDirector相比，所提方法在时间一致性（TC）和视频质量上获得更优的人类偏好分数。
- 消融实验表明，运动一致性损失和初始噪声共同作用才能实现最优性能，单点引导已足够。
---

# Training-Free Motion-Guided Video Generation with Enhanced Temporal Consistency Using Motion Consistency Loss

> [!tip] 核心洞察
> 利用扩散模型时间注意力中间层的特征相关性模式作为软运动轨迹的表示，并通过梯度引导的方式施加一致性约束，能够与初始噪声隐含运动引导形成互补，仅需少量稀疏关键点即可达到良好的运动控制效果。

| 字段 | 内容 |
|------|------|
| 中文题名 | 免训练运动引导视频生成：通过运动一致性损失增强时间一致性 |
| 英文题名 | Training-Free Motion-Guided Video Generation with Enhanced Temporal Consistency Using Motion Consistency Loss |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2501.07563) · [Project](https://zhangxinyu-xyz.github.io/SimulateMotion.github.io/) · [Code](https://github.com/AILab-CVC/VideoCrafter) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | Initial-Noise + Motion Consistency Loss (MCL) Video Generation |
| Dataset | Trajectory Control, Reference Video Control |

> [!tip] 效果简介
> - Trajectory Control (56 prompts, 8 trajectories, 2 random noises) 上，mIoU 0.272 vs 0.268 (FreeTraj) (+0.004 (+1.5%))。
> - Trajectory Control 上，CLIP-SIM-GTBox 0.889 vs 0.886 (FreeTraj) (+0.003 (+0.34%))；Human preference (Trajectory Align) 52.12% vs 47.88% (FreeTraj) (+4.24%)。
> - Reference Video Control (76 videos, 4 prompts) 上，TC (Temporal Consistency) 93.3 vs 93.1 (MotionDirector) (+0.2)。

## 概述

现有免训练运动引导视频生成方法（如基于轨迹的 **FreeTraj** 和基于参考视频的 **MotionDirector**）主要依赖初始噪声反演或注意力掩码等隐式手段进行运动控制。这类方法难以同时保持精确的运动轨迹跟随和帧间外观一致性，导致生成视频中出现目标物体变形、细节丢失等时间不连贯问题（Figure 1）。

本工作提出一种简单而有效的解决方案：将初始噪声引导与一种新颖的**运动一致性损失（Motion Consistency Loss, MCL）**相结合。核心思路是利用视频扩散模型中时间注意力模块的帧间特征相关性模式作为软运动轨迹的表征，并在去噪过程中通过分类器引导的方式施加显式一致性约束。该方法无需更新模型参数，仅需少量稀疏关键点即可将参考视频的运动模式迁移到生成视频中。

主要结果：
- 在轨迹控制任务上，mIoU 达到 0.272（FreeTraj 为 0.268），CLIP-SIM-GTBox 达到 0.889，人类偏好评估中轨迹对齐度领先 FreeTraj 4.24 个百分点（Table 1）。
- 在参考视频控制任务上，时间一致性（TC）达到 93.3，视频质量人类偏好分数领先需训练的 **MotionDirector**（Zhao et al., ECCV 2025）10.52 个百分点（Table 2）。
- 消融实验证实，初始噪声反演与运动一致性损失二者缺一不可，且单点引导已足够实现有效控制（Figure 5, Figure 10）。

方法在目标文本与参考视频内容差异过大时仍存在一定局限（Figure 12）。代码与项目页面已公开。

## 背景与动机

### 免训练运动引导视频生成的现状与瓶颈

扩散模型在视频生成领域已展现出强大的能力，但如何在不进行额外训练的前提下，精确控制生成视频中的运动轨迹和时间一致性，仍是一个开放挑战。现有的免训练运动引导方法主要依赖两类隐式机制：一是通过精心设计的初始噪声（如DDIM反演噪声或轨迹特定噪声）隐含地注入运动先验；二是通过注意力掩码约束空间-时间注意力范围。然而，这些手段难以同时兼顾**精确的运动轨迹跟随**和**帧间外观一致性**，导致生成视频中出现目标物体变形、细节丢失等时间不连贯现象。

Figure 1 直观地展示了这一瓶颈：在参考视频控制场景下，现有方法**MotionDirector**（Zhao et al., ECCV 2025）尽管使用了反演噪声初始化，但在狮子奔跑的案例中，尾巴和爪子在后续帧中逐渐模糊甚至消失（红色圆圈区域）；在轨迹控制场景下，当前最优的免训练方法**FreeTraj**同样存在类似的细节退化问题。这些现象表明，仅靠初始噪声的隐式引导不足以在去噪过程中持续约束运动模式的时间一致性。

### 核心洞察：从隐式引导到显式运动一致性约束

上述瓶颈的根源在于，现有方法缺乏一个**显式的、可优化的运动表示**来约束生成过程。本文的核心洞察是：扩散模型的时间注意力中间层特征包含了丰富的帧间对应关系信息——这些特征的相关性模式本质上构成了目标点的“软运动轨迹”。如果能够从参考视频中提取这种运动模式，并在去噪过程中以损失函数的形式显式地要求生成视频复现相同的模式，就有望在不更新模型参数的前提下，显著提升运动精度和时间一致性。

这一思路的关键优势在于**互补性**：初始噪声提供了粗粒度的运动先验和外观基调，而运动一致性损失则在去噪的每一步施加细粒度的帧间约束，两者协同作用。消融实验（Figure 5）证实了这一点：单独使用反演噪声会导致细节丢失，单独使用运动一致性引导则无法模拟大幅度的外观变化，仅当两者结合时才能实现最优的时间一致性。

### 方法定位与贡献

基于上述洞察，本文提出了一种**免训练的运动引导视频生成方法**，其核心是**运动一致性损失（Motion Consistency Loss, MCL）**。该方法通过以下三个步骤实现运动控制：

1. **初始噪声反演**：利用DDIM反演将参考视频转换为初始潜变量 $z_T$，隐含地携带运动信息。
2. **运动模式提取**：从扩散模型时间注意力模块中提取目标关键点的帧间特征相关性模式 $\mathcal{M}$，作为软运动轨迹的显式表示。
3. **梯度引导去噪**：在去噪过程中计算生成视频与参考视频运动模式之间的L2距离 $\mathcal{L}_c$，并以分类器引导的方式将梯度注入噪声估计，实现无须微调的运动约束。

该方法在轨迹控制和参考视频控制两个任务上均取得了有竞争力的结果：在轨迹控制任务中，相比FreeTraj，mIoU提升1.5%（0.268→0.272），CLIP-SIM-GTBox提升0.34%（0.886→0.889），人类偏好评估中轨迹对齐得分领先4.24个百分点（Table 1）；在参考视频控制任务中，相比需要训练的MotionDirector，时间一致性得分（TC）达到93.3，视频质量人类偏好得分领先10.52个百分点（Table 2）。值得注意的是，该方法仅需**单个稀疏关键点**即可达到良好的运动控制效果，增加点数并未进一步提升性能（Figure 10），体现了其高效性。

## 核心创新

本工作针对现有免训练运动引导视频生成方法中“隐式引导不足导致时间一致性差”的瓶颈，提出了**初始噪声反演 + 运动一致性损失（Motion Consistency Loss, MCL）** 的互补式显式引导方案。其关键创新体现在两个 changed slots 上：

### 从隐式引导到显式运动模式约束

现有免训练方法（如 **Peekaboo**、**FreeTraj**）主要依赖精心设计的初始噪声和注意力掩码来隐式地注入运动信息。这种方式缺乏对生成过程中帧间运动关系的直接监督，导致视频中出现目标物体变形、细节丢失等时间不连贯现象（Figure 5, confidence 0.9）。

本方法的核心突破在于引入了一个**显式的帧间运动一致性损失函数**：

$$
\mathcal { L } _ { c } = \sum _ { f = 1 } ^ { F } \sum _ { i = f + 1 } ^ { F } | | \mathbf { M } _ { i } ^ { ' } - \mathbf { M } _ { i } | | _ { 2 } ^ { 2 }
$$

该损失直接度量生成视频与参考视频之间运动模式的偏差。其中运动模式 $\mathbf{M}_i$ 定义为关键点特征在后续帧上的 Softmax 归一化余弦相似度分布（Eq. 3），本质上是一种**软运动轨迹表示**。通过将 $\mathcal{L}_c$ 的梯度以分类器引导的方式注入去噪过程：

$$
\hat { \epsilon } _ { \boldsymbol { \theta } } ( \mathbf { z } _ { t } , t , y ) : = \epsilon _ { \boldsymbol { \theta } } ( \mathbf { z } _ { t } , t , y ) + \sigma _ { t } \nabla _ { \mathbf { z } _ { t } } \mathcal { L } _ { e } ( \mathbf { z } _ { t } )
$$

方法在不更新模型参数的前提下实现了对运动轨迹的精确控制。

### 初始噪声反演与显式损失的互补机制

消融实验（Figure 5, confidence 0.9）揭示了两个 changed slots 的互补关系：

- **仅使用初始噪声反演**：能够隐式提供运动轨迹信息，但缺乏显式约束时，时间一致性变差，细节出现伪影（如狮子尾巴和爪子丢失）。
- **仅使用运动一致性损失**：在没有反演噪声初始化的情况下，模型无法模拟带有外观变化的大幅度运动。
- **两者结合**：初始噪声提供运动先验，运动一致性损失在去噪过程中持续校正帧间关系，二者共同作用才能实现最优性能。

### 稀疏关键点的高效引导

与需要密集轨迹标注或复杂训练的方法不同，本方法仅需在参考视频上指定**少量稀疏关键点**即可提取运动模式。消融实验（Figure 10, confidence 0.9）表明，增加稀疏点数量并未进一步提升性能，单点引导已足够。这大幅降低了用户交互成本，同时保持了运动控制的精度。

### 与需训练方法的差异化优势

相比于需要训练的 **MotionDirector**（Zhao et al., ECCV 2025），本方法在保持免训练优势的同时，在时间一致性（TC: 93.3 vs 93.1）和人类偏好的视频质量评估（55.26% vs 44.74%）上均取得了更优结果（Table 2, confidence 0.95）。这表明显式运动一致性约束在免训练框架下能够有效替代甚至超越训练式方法的运动定制能力。

## 整体框架

该方法构建了一条**免训练的运动引导视频生成管线**，核心思路是将初始噪声隐含的运动先验与显式的帧间运动一致性损失相结合，在不更新扩散模型参数的前提下实现精确的运动控制与时间连贯性。

### 管线总览

整个流程分为三个主要阶段，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l41_https_arxiv_org_abs_2501_07563/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method. We first conduct (a) inversion noise initialization on the reference video to obtain the initial noise zT (Section 3.2). Then we (b) extract the motion pattern M from the reference video for each tracked point p (Section 3.3). During the (c) denoising process, we use the proposed frame-to-frame motion consistency loss*

1. **DDIM 反演初始噪声生成**：将参考视频通过 DDIM 反演转换为初始潜变量 $\mathbf{z}_T$，使初始噪声中隐含参考视频的运动信息。
2. **运动模式提取**：从参考视频中提取用户指定的稀疏关键点 $\mathbf{p}$ 的帧间特征相关性模式 $\mathcal{M}$，作为软运动轨迹的表示。
3. **梯度引导去噪**：在去噪过程中，同步提取生成视频的运动模式 $\mathcal{M}'$，计算与参考运动模式之间的运动一致性损失 $\mathcal{L}_c$，并将其梯度注入噪声估计，实现训练免微调的运动引导。

### 模块关系与数据流

各模块之间的输入输出关系如下：

- **输入**：参考视频 $\mathbf{z}_0$、用户点击的稀疏关键点 $\mathbf{p}$、目标文本提示 $y$。
- **DDIM 反演模块**：以参考视频为输入，输出初始噪声 $\mathbf{z}_T$，为后续去噪提供起点。
- **运动模式提取模块**：以参考视频经 $t'=1$ 步加噪后的潜变量 $\mathbf{z}_{t'}$ 为输入，从扩散模型所有时间注意力模块中提取特征图 $\{\mathbf{F}_l\}$，计算关键点 $\mathbf{p}$ 在后续各帧上的 Softmax 归一化余弦相似度分布 $\mathbf{M}_i$（Eq. 3），构成运动模式 $\mathcal{M} = \{\mathbf{M}_{f+1}, \mathbf{M}_{f+2}, ..., \mathbf{M}_F\}$。
- **去噪循环**：从 $\mathbf{z}_T$ 开始逐步去噪。在每一步 $t$，使用当前潜变量 $\mathbf{z}_t$ 同步提取生成视频的运动模式 $\mathcal{M}'$，计算帧间运动一致性损失 $\mathcal{L}_c = \sum_{f=1}^{F} \sum_{i=f+1}^{F} ||\mathbf{M}_i' - \mathbf{M}_i||_2^2$（Eq. 4），然后按照分类器引导范式修正噪声估计：$\hat{\epsilon}_{\boldsymbol{\theta}}(\mathbf{z}_t, t, y) := \epsilon_{\boldsymbol{\theta}}(\mathbf{z}_t, t, y) + \sigma_t \nabla_{\mathbf{z}_t} \mathcal{L}_c(\mathbf{z}_t)$（Eq. 2），其中权重调度 $\sigma_t = 10000.0$。
- **输出**：去噪完成后的生成视频 $\mathbf{z}_0$。

### 关键设计选择

- **稀疏关键点**：仅需用户在参考视频首帧点击一个或多个稀疏点即可定义运动轨迹，消融实验表明单点引导已足够（Figure 10）。
- **局部帧范围**：运动关联模式的计算范围限定在后续 8 帧内，可有效提升运动相似性，继续增大范围后性能趋于稳定（Figure 9）。
- **温度参数**：Eq. 3 中 Softmax 的温度 $\tau$ 设为 10.0，控制运动模式的软硬程度。

整个管线的伪代码见 Algorithm 1，完整实现了从初始噪声反演到梯度引导去噪的训练免微调运动控制流程。

## 核心模块与公式推导

本节聚焦所提方法中三个核心模块的数学定义与推导：运动模式的提取与表示、运动一致性损失函数的构建，以及分类器引导下的梯度注入机制。所有公式均来自原文，不进行额外推导。

### 运动模式提取：帧间特征相关性模式

方法的核心思想是利用视频扩散模型时间注意力模块的中间特征，构建可迁移的运动模式表示。给定参考视频，首先通过1步加噪得到 $z_{t'}$（经验选取 $t'=1$），将其输入扩散模型，从所有时间注意力模块提取特征图 $\{F_l\}$。对于用户指定的关键点 $p$，在第一帧特征图中定位其对应特征向量 $\mathbf{f}$。

运动模式 $\mathcal{M}$ 定义为该关键点在后续帧上的空间注意力分布集合：

$$
\mathcal{M} = \{ \mathbf{M}_{f+1}, \mathbf{M}_{f+2}, \dots, \mathbf{M}_{F} \}
$$

其中每一帧 $i$ 上的相关性分布 $\mathbf{M}_i$ 通过余弦相似度与Softmax归一化计算：

$$
\mathbf{M}_i(j,k) = \frac{\exp(\mathrm{sim}(\mathbf{f}, \mathbf{f}_{(i,j,k)}) / \tau)}{\sum_{h=1}^{H} \sum_{w=1}^{W} \exp(\mathrm{sim}(\mathbf{f}, \mathbf{f}_{(i,h,w)}) / \tau)}
$$

这里 $\mathbf{f}_{(i,j,k)}$ 表示第 $i$ 帧空间位置 $(j,k)$ 处的特征向量，$\mathrm{sim}(\cdot,\cdot)$ 为余弦相似度，$\tau$ 为温度系数（实验中设为10.0）。该分布实质上构成了一种“软运动轨迹”——高响应区域指示关键点在后续帧中的可能位置，无需显式坐标回归。

### 运动一致性损失：帧间约束

在去噪过程的每一步 $t$，从当前噪声潜变量 $z_t$ 中同样提取运动模式 $\mathcal{M}'$。运动一致性损失定义为生成视频与参考视频运动模式在所有帧对上的L2距离之和：

$$
\mathcal{L}_c = \sum_{f=1}^{F} \sum_{i=f+1}^{F} \|\mathbf{M}_i' - \mathbf{M}_i\|_2^2
$$

该损失函数的变量含义明确：$F$ 为总帧数，$f$ 为起始帧索引，$i$ 为后续帧索引；$\mathbf{M}_i'$ 与 $\mathbf{M}_i$ 分别为生成过程与参考视频在第 $i$ 帧上的运动相关性分布。通过最小化该损失，生成视频的帧间特征相关性模式被强制逼近参考视频的模式，从而在无需更新模型参数的前提下实现运动迁移。

### 梯度引导去噪：分类器引导范式

为实现免训练的运动控制，方法采用分类器引导范式将运动一致性损失的梯度注入噪声估计。标准扩散模型的噪声估计 $\epsilon_{\theta}(z_t, t, y)$ 被修正为：

$$
\hat{\epsilon}_{\theta}(z_t, t, y) := \epsilon_{\theta}(z_t, t, y) + \sigma_t \nabla_{z_t} \mathcal{L}_c(z_t)
$$

其中 $\sigma_t$ 为权重调度参数（实验中设为10000.0），控制运动一致性引导的强度。该修正噪声估计随后用于标准的DDIM去噪更新步骤，形成完整的免训练运动引导生成流程（详见Algorithm 1）。

### 初始噪声初始化：隐式运动先验

除显式的运动一致性损失外，方法还利用DDIM反演将参考视频转换为初始噪声 $z_T$，为生成过程提供隐式的运动先验。消融实验（Figure 5）表明，仅使用初始噪声引导而不加运动一致性损失时，视频细节会出现时间不一致现象（如狮子尾巴和爪子丢失）；反之，仅使用运动一致性损失而不用反演初始化，则模型难以模拟带有外观变化的大幅度运动。两者协同作用才能实现最优性能。

## 实验与分析

### 核心实验设置

方法在两种运动控制场景下进行验证：**轨迹控制**（trajectory control）与**参考视频控制**（reference video control）。轨迹控制实验沿用 FreeTraj 的评测框架，包含 56 条文本提示、8 条预定义轨迹、2 种初始噪声，共生成 896 个视频。参考视频控制实验使用 LOVEU-TGVE 数据集，包含 76 个参考视频，每个视频搭配 4 条编辑提示，共生成 304 个视频。实现层面，权重调度参数 $\sigma_t$ 设为 10000.0，运动模式提取中的温度系数 $\tau$ 设为 10.0。所有基线方法（Peekaboo、FreeTraj、MotionDirector）均使用官方代码重新实现，保持相同的提示、轨迹和随机种子以确保公平比较。

### 轨迹控制任务：运动精度与时间一致性的双重提升

在轨迹控制的自动评估中，所提方法在两项核心指标上均超越当前最优的免训练方法 FreeTraj。如 Table 1 所示，mIoU 从 FreeTraj 的 0.268 提升至 0.272（+1.5%），CLIP-SIM-GTBox 从 0.886 提升至 0.889（+0.34%）。这两个指标的提升幅度虽然有限，但结合人类评估来看，优势更为显著：在轨迹对齐偏好上，所提方法以 52.12% 对 47.88% 领先 FreeTraj，表明运动一致性损失有效增强了生成视频对指定轨迹的跟随能力。

![[assets/figures/papers/paper_list_l41_https_arxiv_org_abs_2501_07563/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison of trajectory control. Automatic and human evaluations results with the trajectory based videos. We re-implement Peekaboo [26] and FreeTraj [47] using their official code with the same prompts as ours. Our method achieves competitive performance in metrics about video quality and gains the best scores in metrics that are related to trajectory control*

定性结果（Figure 3）进一步印证了这一结论。在“Direct”基线（纯随机噪声无引导）中，生成视频的运动轨迹完全不可控；Peekaboo 和 FreeTraj 虽能大致跟随轨迹，但在目标物体外观的时序一致性上存在明显瑕疵。所提方法在保持轨迹精度的同时，显著减少了帧间抖动和物体变形现象。

![[assets/figures/papers/paper_list_l41_https_arxiv_org_abs_2501_07563/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison of trajectory control. We evaluate our method and other trajectory based approaches, i.e., Peekaboo [26] and FreeTraj [47]. The “Direct” means the direct inference with random noise and no other guidance. We use the same initial noises as in [47] for better visual comparison. Our method shows better ability on trajectory follow and temporal coherent consistency*

### 参考视频控制任务：与需训练方法的正面竞争

在参考视频控制场景下，所提方法与需要训练的 MotionDirector（Zhao et al., ECCV 2025）进行了全面对比。自动评估指标 TC（Temporal Consistency）上，所提方法以 93.3 对 93.1 略优于 MotionDirector（Table 2）。更具说服力的是人类评估结果：在视频质量偏好上，所提方法获得了 55.26% 的支持率，大幅领先 MotionDirector 的 44.74%（+10.52%）。这一结果表明，即使在无需任何模型微调的前提下，显式的运动一致性损失约束也能产生比训练式方法更优的感知质量。

Figure 4 的定性对比展示了具体的优势场景。红色圆圈标注的用户点击关键点，所提方法生成的视频中目标物体的运动轨迹更稳定，红色和绿色矩形高亮区域的时序连贯性明显优于 MotionDirector，后者在某些帧中出现了目标外观的突变或漂移。

![[assets/figures/papers/paper_list_l41_https_arxiv_org_abs_2501_07563/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison of reference video control. We evaluate our method and MotionDirector [93]. The red circle represents the given point clicked by users. The red and green rectangle are highlight areas to show the temporal coherent clearly. We keep the initial noises same in [47] and our method for fair comparison*

### 消融实验：初始噪声与运动一致性损失的协同机制

消融实验系统解耦了方法中两个核心组件的贡献（Figure 5）。当仅使用随机噪声而不使用 DDIM 反演初始噪声时，模型无法模拟包含显著外观变化的大幅度运动（如狮子奔跑时尾巴和爪子的时序变形）。当仅使用反演初始噪声但去掉运动一致性引导时，时间一致性显著恶化，细节区域出现伪影和丢失。只有当两者协同作用时，才能同时实现精确的运动轨迹跟随和稳定的帧间外观保持。这一发现验证了核心洞察：反演噪声隐式提供了运动轨迹的“粗粒度”先验，而运动一致性损失则通过显式梯度引导进行“细粒度”修正。

![[assets/figures/papers/paper_list_l41_https_arxiv_org_abs_2501_07563/figures/007_Figure_5.jpg]]
*Figure 5: Ablation study on each component in our method, including the inversion noise initialization and frame-to-frame consistency guidance*

进一步的参数消融揭示了几个关键特性：

- **局部帧范围**（Figure 9）：将运动关联模式的计算范围从相邻帧逐步扩展至 8 帧时，运动相似性持续提升，超过 8 帧后趋于稳定，表明适度的时序感受野对捕捉运动模式至关重要。
- **稀疏点数量**（Figure 10）：增加稀疏关键点数量并未带来性能增益，单点引导已足以实现有效运动控制。这与直觉相悖——更多运动线索反而可能引入优化冲突。
- **权重调度 $\sigma_t$**（Figure 11）：在 10000.0 附近达到运动一致性与外观质量的最佳平衡，过高或过低都会导致某一方面的退化。

![[assets/figures/papers/paper_list_l41_https_arxiv_org_abs_2501_07563/figures/011_Figure_9.jpg]]
*Figure 9: The local range for the calculation of the motion correlation pattern. The text prompt is “A lion is running on the road.”*

![[assets/figures/papers/paper_list_l41_https_arxiv_org_abs_2501_07563/figures/014_Figure_10.jpg]]
*Figure 10: The number of sparse points selected for the calculation of the motion correlation consistency. The text prompt is “A panda is lifting weights”*

![[assets/figures/papers/paper_list_l41_https_arxiv_org_abs_2501_07563/figures/012_Figure_11.jpg]]
*Figure 11: The impact on the weight schedule*

### 失败模式与适用范围边界

方法存在明确的适用边界。当目标文本提示与参考视频内容差异过大时，生成质量显著下降（Figure 12）。例如，要求汽车执行“V”形轨迹或海豚进行举重动作，由于扩散模型的语义先验与运动约束产生冲突，生成结果无法同时满足内容合理性和运动精度。此外，增加稀疏点数未能提升性能的现象暗示，当前的运动模式提取策略可能对关键点的选择和跟踪质量较为敏感，需要人工干预来确保引导信号的可靠性。

![[assets/figures/papers/paper_list_l41_https_arxiv_org_abs_2501_07563/figures/013_Figure_12.jpg]]
*Figure 12: Failure case. The results are suboptimal when the target prompt deviates significantly from the reference video*

### 手势模拟：运动迁移的直观验证

Figure 6 展示了方法的一个有趣应用：将摄像头捕捉的手势运动迁移到动物视频生成中。这一实验以直观的方式验证了运动一致性损失对不同来源运动信号的泛化能力——即使参考运动来自完全不同的域（人手姿态），方法仍能将其转化为目标物体（动物）的合理运动轨迹。

![[assets/figures/papers/paper_list_l41_https_arxiv_org_abs_2501_07563/figures/008_Figure_6.jpg]]
*Figure 6: Gesture simulation. We use two gestures captured from the camera to simulate animal’s movement. Our method can successfully generate the video with accurate ear moving of rabbit and body moving of snake when the given point is on the finger and ball. (Best view in video in the project link.)*

### 补充图表

![[assets/figures/papers/paper_list_l41_https_arxiv_org_abs_2501_07563/figures/005_Figure.jpg]]

![[assets/figures/papers/paper_list_l41_https_arxiv_org_abs_2501_07563/figures/001_Figure_1.jpg]]
*Figure 1: Visualization comparisons on our method and two existing motion customization methods, including the reference video based Motiondirector [93], and the bounding box trajectory based FreeTraj [47]. Methods in the upper part use the inversion noise from the reference video, while methods in the lower part use the well-designed noise as initialization. The red circle regions represent the inconsistent temporal coherent, while the green circle regions represent the correct one*

## 方法谱系与知识库定位

### 1. 方法定位与核心差异

本文提出的 **Initial-Noise + Motion Consistency Loss (MCL)** 方法属于**免训练运动引导视频生成**范式。其核心定位在于：**在不更新扩散模型参数的前提下，通过显式优化帧间特征相关性模式的一致性，将参考视频的运动模式迁移到生成视频中**，从而同时提升时间一致性和运动轨迹精度。

与现有工作的关键差异体现在两个维度：

| 对比维度 | 现有免训练方法（Peekaboo、FreeTraj） | 需训练方法（MotionDirector） | 本文方法 |
|----------|--------------------------------------|------------------------------|----------|
| 运动引导方式 | 隐式：仅依赖初始噪声和注意力掩码 | 显式：通过微调模型参数学习运动模式 | 显式：通过运动一致性损失函数梯度引导，但不更新参数 |
| 时间一致性保障 | 弱：目标物体易出现变形、细节丢失 | 中：受限于训练数据的泛化能力 | 强：帧间特征相关性模式约束直接作用于去噪过程 |
| 计算开销 | 低 | 高（需训练） | 中（需在去噪过程中提取特征并计算损失） |

**因果机制**：现有免训练方法的根本瓶颈在于，初始噪声和注意力掩码只能提供**隐式**的运动线索，无法对帧间外观一致性施加直接约束。本文通过引入**运动一致性损失**（$L_c$），将参考视频中关键点的帧间特征相关性模式 $\mathcal{M}$ 作为“软运动轨迹”的显式监督信号，以分类器引导的方式注入去噪过程。这一机制与初始噪声的隐式运动引导形成**互补**：初始噪声提供了运动的大致方向，而 $L_c$ 则精细地约束了帧间细节的一致性。

### 2. 方法谱系中的位置

在免训练可控视频生成的演进脉络中，本文方法可以视为从“隐式引导”到“显式约束”的关键转折点：

- **Peekaboo**（基于轨迹的免训练方法）：通过初始噪声设计实现轨迹控制，但缺乏对帧间一致性的显式建模。
- **FreeTraj**（基于轨迹的免训练方法，当前最优）：改进了初始噪声和注意力掩码策略，但仍未解决隐式引导的根本局限——在复杂运动下目标物体易出现变形。
- **本文方法**：在 FreeTraj 的基础上，引入基于时间注意力特征相关性模式的运动一致性损失，首次在免训练框架下实现了对帧间外观一致性的显式约束。

与需要训练的 **MotionDirector**（Zhao et al., ECCV 2025）相比，本文方法在**不更新模型参数**的条件下，在参考视频控制任务上取得了更优的时间一致性（TC: 93.3 vs. 93.1）和大幅领先的人类偏好分数（视频质量: 55.26% vs. 44.74%），证明了显式运动约束在免训练范式下的有效性。

### 3. 适用边界

**有效场景**：
- 目标文本与参考视频内容高度相关时（如“狮子奔跑”匹配狮子参考视频），方法能精确迁移运动模式并保持外观一致性。
- 稀疏关键点引导（甚至单点）已足够实现良好的运动控制效果——消融实验表明增加点数未进一步提升性能（Figure 10）。
- 支持两种输入模式：参考视频的 DDIM 反演噪声（运动定制）和轨迹特定的初始噪声（轨迹控制）。

**失效场景**：
- 当目标文本与参考视频内容**差异过大**时，生成结果不理想（Figure 12）。例如：汽车执行“V”形轨迹、海豚举重等场景——扩散模型的先验知识无法弥合文本语义与运动模式之间的鸿沟。
- 运动关联模式的计算范围在扩展到 8 帧后性能趋于稳定（Figure 9），暗示方法对**长程运动依赖**的建模能力存在上限。

### 4. 局限与开放问题

**已知局限**：
1. **跨域泛化弱**：目标文本与参考视频的语义鸿沟限制了方法的适用范围。
2. **稀疏点冗余**：增加稀疏关键点数量并未带来性能增益，甚至可能引入不确定性。
3. **长视频扩展未验证**：当前实验基于固定帧数，方法在更长视频或高度动态场景下的表现未知。

**开放问题**：
1. **多主体交互**：如何将方法推广到多对象、多运动轨迹的复杂交互场景？
2. **关键点自动选择**：能否自动确定最优的稀疏关键点及其跟踪策略，减少人工干预？
3. **多模态运动信号融合**：能否将骨骼点、物理模拟等其他形式的运动控制信号与当前框架结合？
4. **计算效率优化**：去噪过程中每步提取特征并计算运动一致性损失引入了额外开销，是否存在轻量化的替代方案？

## 原文 PDF

![[paperPDFs/arxiv_2025/Training_Free_Motion_Guided_Video_Generation_with_Enhanced_Temporal_Consistency_Using_Motion_Consistency_Loss.pdf]]