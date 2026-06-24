---
title: "STMC: Multi-Track Timeline Control for Text-Driven 3D Human Motion Generation"
type: paper
paper_level: A
venue: CVPRW
year: 2024
pdf_ref: paperPDFs/CVPR_2024/STMC_Multi_Track_Timeline_Control_for_Text_Driven_3D_Human_Motion_Generation.pdf
project_link: https://mathis.petrovich.fr/stmc/
aliases:
  - SSTMC
  - STMC
tags:
- CVPRW_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: 在测试时，通过在去噪的每一步独立处理每个时间区间的文本提示，并依据身体部位标签和时序重叠进行空间与时间上的动态拼接，使预训练扩散模型能够生成符合复杂多轨时间线的组合动作。
primary_logic: 将大型语言模型的语义理解/代码生成、Blender的物理仿真能力与预训练的文本到图像扩散模型相结合，构成无需额外训练（training-free）的框架，使生成的视频既符合文本语义又满足物理定律。
claims:
  - "STMC在自建的多轨时间线（MTT）数据集上，在语义正确性（R@1: 30.5 vs 22.6, TMR-Score M2T: 0.675 vs 0.633）和运动真实感（FID: 0.459 vs 0.532, 转换距离: 0.9 vs 4.6）上显著优于DiffCollage基线。"
  - 人类感知研究证实STMC在运动真实感和语义准确性上均被评估者显著偏好于SINC with Lerp（真实感66%偏好）和DiffCollage（真实感68%偏好）。
  - STMC可无缝集成多种预训练运动扩散模型（MDM, MotionDiffuse, MDM-SMPL），且MDM-SMPL通过SMPL骨骼表示和改进的扩散调度将采样速度提升10倍，同时维持生成质量。
  - 消融实验表明，较短的时序重叠提高语义准确性但增加过渡距离，反之亦然，验证了时空拼接策略的有效性与权衡。
---

# STMC: Multi-Track Timeline Control for Text-Driven 3D Human Motion Generation

> [!tip] 核心洞察
> 将多动作组合问题分解为多个单动作去噪子任务，再通过迭代的身体部位拼接和基于因子图的时序缝合（DiffCollage）聚合，无需额外训练即可实现忠实于时间线语义和时序的复杂运动生成。

| 字段      | 内容                                                                                                |
| ------- | ------------------------------------------------------------------------------------------------- |
| 中文题名    | STMC：面向文本驱动3D人体运动生成的多轨时间线控制                                                                       |
| 英文题名    | STMC: Multi-Track Timeline Control for Text-Driven 3D Human Motion Generation                     |
| 会议/期刊   | CVPRW 2024                                                                                        |
| Links   | [paper](https://arxiv.org/abs/2401.08559); [Project](https://mathis.petrovich.fr/stmc/)           |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method  | STMC (Spatio-Temporal Motion Collage)                                                             |
| Dataset | MTT (Multi-Track Timeline dataset), MTT                                                           |

> [!tip] 效果简介
> - MTT (Multi-Track Timeline dataset) 上，R@1 (motion-to-text retrieval accuracy) 为 30.5 (STMC with MDM-SMPL)，对比 22.6 (DiffCollage)，变化 +7.9。
> - MTT 上，R@3 为 50.9，对比 43.3 (DiffCollage)，变化 +7.6。
> - MTT 上，TMR-Score M2T 为 0.675，对比 0.633 (DiffCollage)，变化 +0.042。

## 概述

文本驱动三维人体运动生成近年来取得了显著进展，但现有方法普遍存在一个关键瓶颈：它们仅支持单一文本提示作为输入，缺乏对动作时序和空间组合的细粒度控制。具体而言，用户无法精确指定多个动作的**时机**、**持续时间**以及**身体部位协调**——例如，“前5秒用左手挥手，同时从第3秒开始下蹲并持续到结束”。这种多轨时间线（Multi-Track Timeline）控制能力的缺失，严重限制了运动生成在动画制作、游戏开发等创意场景中的实用性。

针对上述问题，本文提出 **STMC（Spatio-Temporal Motion Collage）**，一种无需额外训练、可在测试时与任意预训练运动扩散模型集成的多轨时间线控制方法。其核心洞见在于：将多动作组合问题分解为多个单动作去噪子任务，再通过迭代的**身体部位空间拼接**和基于因子图的**时序缝合**（DiffCollage）进行聚合，从而生成忠实于时间线语义和时序的复杂组合运动。

在自建的**多轨时间线（MTT）数据集**上，STMC在语义正确性和运动真实感方面均显著优于现有基线。以MDM-SMPL为底层去噪模型时，STMC在运动到文本检索准确率（R@1: 30.5 vs DiffCollage的22.6）和过渡真实感（FID: 0.459 vs 0.532）上取得大幅领先。人类感知研究进一步证实，评估者在运动真实感上对STMC的偏好率达66%–68%，显著优于SINC with Lerp和DiffCollage基线。此外，STMC可无缝集成多种预训练模型（MDM、MotionDiffuse、MDM-SMPL），其中MDM-SMPL通过SMPL骨骼表示和改进的扩散调度将采样速度提升10倍，同时维持生成质量。

## 背景与动机

文本驱动的人体运动生成旨在根据自然语言描述合成逼真的三维人体动作序列。近年来，基于扩散模型的方法在该领域取得了显著进展，但现有工作普遍存在一个根本性局限：它们仅支持单一文本提示作为输入，缺乏对动作时序和空间组合的细粒度控制。具体而言，用户无法精确指定多个动作的发生时机、持续时长以及涉及的身体部位协调关系。

这一局限与真实创作需求之间存在显著鸿沟。在动画制作、游戏开发和虚拟现实等应用场景中，创作者往往需要描述一段包含多个动作的复杂序列——例如“先走向桌子，同时用右手拿起杯子，然后转身离开”。传统方法要么将多个动作描述折叠为单一文本提示，导致语义丢失；要么仅支持非重叠区间的时序组合，无法处理并行发生的动作（Figure 2）。

**现有方法的缺口**主要体现在三个层面：

1. **输入格式受限**：预训练运动扩散模型（如MDM、MotionDiffuse）仅在单文本-单动作数据上训练，无法原生接受多轨多区间的时间线输入，其中每个区间独立绑定一个文本提示，且区间可以重叠。

2. **空间组合能力缺失**：现有时序组合方法（如**DiffCollage**，Zhang et al., CVPR 2023）将多轨时间线压缩为单轨时间序列后处理，忽略了不同动作可能涉及不同身体部位这一关键特性。**SINC**（Athanasiou et al., arXiv 2023）虽然支持独立生成各动作后再进行身体部位拼接，但其一次性拼接策略缺乏过渡平滑处理，导致动作衔接处出现突变伪影。

3. **时序过渡生硬**：简单拼接或线性插值无法生成符合物理规律和运动学约束的自然过渡。如何在保证各段动作语义准确性的同时，实现平滑的时序衔接，是一个未被充分解决的问题。

**本文动机**：针对上述缺口，本文提出STMC（Spatio-Temporal Motion Collage），一种无需额外训练的测试时组合方法。其核心思想是将多动作组合问题分解为多个单动作去噪子任务，在扩散模型的每一步去噪过程中独立处理每个时间区间的文本提示，并依据身体部位标签和时序重叠进行空间与时间上的动态拼接。该方法可无缝集成任何预训练运动扩散模型，使其具备忠实于复杂多轨时间线语义和时序的生成能力。

## 核心创新

### 问题瓶颈：从单文本到多轨时间线的控制鸿沟

现有文本驱动三维人体运动生成方法（如MDM、MotionDiffuse等）均围绕**单一文本提示**设计，仅能生成单一动作或简单时序序列。当用户需要精确控制多个动作的**时机、持续时间和身体部位协调**时——例如“前2秒抬左手，同时后1.5秒向右走”——这些方法面临根本性局限：将多轨时间线折叠为单一文本会丢失时序和空间信息，导致语义忠实度急剧下降。

STMC的核心创新在于**将多动作组合问题分解为多个单动作去噪子任务**，通过在预训练扩散模型的去噪过程中进行动态的时空拼接，无需任何额外训练即可实现复杂多轨时间线的忠实生成。

### 关键改变槽位（Changed Slots）

STMC相对现有基线在四个关键维度上实现了根本性改变：

**1. 输入格式：从单一文本到多轨多区间时间线**

基线方法仅接受单个文本描述或简单的时间序列文本列表。STMC引入了**多轨多区间时间线**（Figure 1），允许用户定义多个时间区间 $[a_j, b_j]$，每个区间独立绑定一个文本提示 $C_j$，且区间可以任意重叠。这一输入格式将时序组合、空间组合和传统文本到动作生成统一为同一框架的特例（Figure 2）。

**2. 空间组合策略：从一次性拼接到迭代身体部位拼接**

SINC等基线在生成完整动作后进行一次性身体部位拼接，无法在去噪过程中协调不同动作的空间关系。STMC在**去噪的每一步**都执行身体部位拼接：首先利用GPT-3自动标注每个文本涉及的身体部位（如“抬左手”仅涉及左臂），构建每个身体部位独立的时间线（Figure 3a）；然后在每步去噪后，依据身体部位时间线将各裁剪预测拆分为身体部位运动并重新组合（Figure 3c）。这种迭代拼接确保生成过程中各部位运动的持续协调。

**3. 时序过渡处理：从简单拼接到基于因子图的DiffCollage缝合**

SINC的直接拼接导致动作过渡处出现突变和不自然。STMC借鉴DiffCollage（Zhang et al., CVPR 2023）的因子图思想，但将其推广到**每个身体部位独立进行时序缝合**：对重叠或相邻区间，扩展区间边界（扩展长度 $l$），分别进行条件去噪和无条件去噪，然后通过加减运算合成平滑过渡：

$$\hat{\pmb{x}}_0 = \overset{-}{\pmb{x}}_0^{a_j - l : b_j + l} + \overset{-}{\pmb{x}}_0^{a_k - l : b_k + l} - \hat{\pmb{x}}_0^{\mathrm{uncond}}$$

该公式将两个条件去噪的扩展区间裁剪与无条件去噪的过渡区间裁剪相加减，在保持各区间语义的同时消除边界伪影（Figure 3b-c）。

**4. 底层运动表示：从263维位姿到SMPL参数化**

为更好地支持身体部位拼接，STMC将底层运动表示从Guo et al.的263维关节旋转特征替换为**SMPL pose参数（6D旋转表示）结合局部关节位置**。这一改变使得身体部位的运动可以独立表示和组合，同时通过改进的扩散调度将采样速度提升10倍（MDM-SMPL），在HumanML3D基准（数据集统计见[[../../references/T2M_Common_Datasets#HumanML3D|HumanML3D]]）上达到FID 0.38、R@3 0.74的竞争力性能。

### 核心洞察：测试时组合的无训练范式

STMC的根本洞察是：预训练扩散模型已经学会了单个动作的分布，多动作组合的挑战在于如何在去噪过程中协调多个条件信号。通过将去噪过程结构化为“独立预测-空间拼接-时序缝合-重噪声化”的迭代循环，STMC将组合问题转化为一系列单动作去噪子任务，利用扩散模型的后验均值公式（Eq. 3）保证合成运动的数学一致性。这一范式**无需任何训练或微调**，可无缝集成MDM、MotionDiffuse、MDM-SMPL等多种预训练模型，为文本驱动运动生成提供了首个实用的多轨时间线控制方案。

## 整体框架

STMC（Spatio-Temporal Motion Collage）是一种纯测试时的去噪组合方法，其核心设计理念是将多动作组合问题分解为多个单动作去噪子任务，再通过迭代的身体部位拼接和时序缝合聚合为完整运动。该方法可无缝集成任何预训练的运动扩散模型（如MDM、MotionDiffuse、MDM-SMPL），无需额外训练或微调。

### 输入输出流

**输入**：多轨时间线（Multi-Track Timeline），由若干时间区间 $[a_j, b_j]$ 构成，每个区间独立绑定一个自然语言提示 $C_j$，描述该时段内应执行的动作。区间可在时间上重叠，允许同时发生多个动作。

**输出**：一段完整的人体运动序列 $\hat{\mathbf{x}}_0$，忠实反映时间线中所有提示的语义内容、时序安排和身体部位协调。

### 核心流水线

STMC在去噪过程的每一步执行以下模块化操作（参见Figure 3）：

1. **身体部位标注与时间线构建**：利用GPT-3自动标注每个文本提示涉及的身体部位（如“左手”“双腿”等），据此将多轨时间线拆分为每个身体部位独立的时间线。未分配动作的区间通过SINC启发式方法填充。

2. **独立去噪**：将当前嘈杂运动 $\mathbf{x}_t$ 按各提示的时间区间裁剪，对每个裁剪片段以对应文本 $C_j$ 为条件，独立进行去噪预测，生成各区间内的干净运动裁剪 $\overset{-}{\mathbf{x}}_0^{a_j:b_j}$。

3. **空间拼接（身体部位组合）**：依据身体部位时间线，将各裁剪预测拆分为身体部位级运动片段，再重新组合成完整的人体运动。这一操作确保每个身体部位在任意时刻只执行其对应时间线规定的动作。

4. **时序拼接（DiffCollage过渡）**：对相邻或重叠的区间，将区间向两侧扩展 $l$ 秒形成过渡带。在过渡带内，对两个条件去噪的扩展裁剪和无条件去噪的过渡裁剪进行加减运算：
   $$\hat{\mathbf{x}}_0 = \overset{-}{\mathbf{x}}_0^{a_j - l : b_j + l} + \overset{-}{\mathbf{x}}_0^{a_k - l : b_k + l} - \hat{\mathbf{x}}_0^{\mathrm{uncond}}$$
   该公式源自DiffCollage（Zhang et al., CVPR 2023），通过有条件与无条件去噪信号的差分实现平滑的动作过渡。

5. **重噪声化与迭代**：将合成的干净运动 $\hat{\mathbf{x}}_0$ 按扩散逆过程的后验均值公式重新注入噪声，得到下一步的嘈杂运动 $\mathbf{x}_{t-1}$：
   $$\mu_t(\mathbf{x}_t, \hat{\mathbf{x}}_0) = \frac{\sqrt{\alpha_t}(1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t}\mathbf{x}_t + \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1-\bar{\alpha}_t}\hat{\mathbf{x}}_0$$
   随后采样 $\mathbf{x}_{t-1} \sim \mathcal{N}(\mu_t, \mathbf{\Sigma}_t)$，继续迭代直至去噪完成。

### 底层运动表示

为更好地支持身体部位拼接，STMC引入了MDM-SMPL变体：将原有263维关节旋转特征替换为SMPL姿态参数（6D旋转表示），并结合局部关节位置。该表示天然按身体部位组织，使空间拼接操作更直接。同时，改进的扩散调度使采样速度提升约10倍，且生成质量不受损（在HumanML3D基准上FID达0.38，优于原MDM）。

### 与现有任务的关系

如图Figure 2所示，STMC框架统一并推广了三类文本驱动运动合成任务：
- **传统文本到动作**：单文本、单区间（Figure 2a）
- **时序组合**：非重叠区间序列（Figure 2b）
- **空间组合**：单区间内多个文本（Figure 2c）
- **多轨时间线控制**：任意重叠区间的多文本集合（Figure 2d），是前三者的泛化形式

### 补充图表

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2401_08559/figures/002_Figure_2.jpg]]
*Figure 2: Text-driven motion synthesis tasks: Our framework generalizes (a) traditional text-to-motion synthesis given one text and one duration, (b) temporal composition given a sequence of texts for non-overlapping intervals, and (c) spatial composition given a set of texts for a single interval. (d) Multi-track timeline control uses a set of texts for arbitrary intervals, allowing fine-grained control over the timings of several complex actions*

## 核心模块与公式推导

STMC的核心思想是将多动作组合生成问题分解为多个单动作去噪子任务，再通过迭代的身体部位拼接和基于因子图的时序缝合进行聚合，无需额外训练即可实现复杂运动生成。该方法在测试时运作，可无缝集成任何预训练的运动扩散模型。

### 多轨时间线定义

给定一个持续时间为 $T$ 的运动序列，多轨时间线由 $N$ 个文本提示组成，每个提示 $C_j$ 绑定一个时间区间 $[a_j, b_j]$，其中 $a_j$ 和 $b_j$ 分别表示该动作的起始和结束时刻。区间之间允许重叠，从而支持多个动作在时间上的并行执行。

### 扩散模型基础

STMC建立在预训练的运动扩散模型之上，该模型学习从噪声中恢复干净运动。前向扩散过程逐步向运动数据 $\pmb{x}_0$ 添加高斯噪声：

$$q(\pmb{x}_t | \pmb{x}_{t-1}) = \mathcal{N}(\pmb{x}_t; \sqrt{1-\beta_t}\pmb{x}_{t-1}, \beta_t\mathbf{I})$$

其中 $\beta_t$ 为噪声调度参数。逆过程以干净运动 $\pmb{x}_0$ 和当前嘈杂运动 $\pmb{x}_t$ 为条件：

$$q(\pmb{x}_{t-1} | \pmb{x}_t, \pmb{x}_0) = \mathcal{N}(\pmb{x}_{t-1}; \mu_t(\pmb{x}_t, \pmb{x}_0), \pmb{\Sigma}_t)$$

后验均值 $\mu_t$ 的具体形式为：

$$\mu_t(\pmb{x}_t, \pmb{x}_0) = \frac{\sqrt{\alpha_t}(1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t}\pmb{x}_t + \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1-\bar{\alpha}_t}\pmb{x}_0$$

去噪模型 $\hat{\pmb{x}}_\theta$ 通过预测原始运动 $\pmb{x}_0$ 进行训练，损失函数为简化均方误差：

$$\mathcal{L} = \mathbb{E}_{\epsilon, t, \pmb{x}_0, C} \|\hat{\pmb{x}}_\theta(\pmb{x}_t, t, C) - \pmb{x}_0\|_2^2$$

该模型仅在单文本提示数据上训练，不涉及多轨时间线的组合学习。

### 核心模块一：身体部位标注与时间线构建

STMC首先将多轨时间线分解为各身体部位的独立时间线。具体而言，利用GPT-3自动标注每个文本提示所涉及的身体部位，为每个身体部位构建独立的时间线。对于未分配文本的时间区间，采用SINC启发式方法进行填充，确保每个身体部位在全时间线上都有对应的文本指派。

### 核心模块二：独立去噪与运动裁剪

在去噪的每一步，STMC接收封装整个时间线的当前嘈杂运动 $\pmb{x}_t$，将其按各提示的时间区间 $[a_j, b_j]$ 裁剪为多个运动片段。每个片段独立通过预训练去噪模型，以对应的文本提示 $C_j$ 为条件，预测该区间的干净运动裁剪 $\overset{-}{\pmb{x}}_0^{a_j:b_j}$。

### 核心模块三：空间拼接（身体部位组合）

依据身体部位时间线，将各裁剪预测拆分为身体部位级别的运动表示，再按部位重新组合成完整的运动帧。这一过程在去噪的每一步迭代执行，确保不同动作在空间维度上的协调组合。

### 核心模块四：时序拼接（DiffCollage过渡）

为处理区间之间的时序过渡，STMC引入基于因子图的时序缝合机制。对于相邻或重叠的区间 $j$ 和 $k$，将区间向两侧扩展长度 $l$ 形成过渡区间，分别进行条件去噪和无条件去噪，然后通过加减运算合成平滑过渡：

$$\hat{\pmb{x}}_0 = \overset{-}{\pmb{x}}_0^{a_j - l : b_j + l} + \overset{-}{\pmb{x}}_0^{a_k - l : b_k + l} - \hat{\pmb{x}}_0^{\mathrm{uncond}}$$

其中 $\overset{-}{\pmb{x}}_0^{a_j - l : b_j + l}$ 和 $\overset{-}{\pmb{x}}_0^{a_k - l : b_k + l}$ 分别为以提示 $C_j$ 和 $C_k$ 为条件的扩展区间去噪结果，$\hat{\pmb{x}}_0^{\mathrm{uncond}}$ 为无条件去噪的过渡区间裁剪。该公式在每个身体部位上独立应用，实现部位级别的平滑时序过渡。

### 核心模块五：重噪声化与迭代

完成时空拼接后，将合成的干净运动 $\hat{\pmb{x}}_0$ 按扩散逆过程公式重新注入噪声，得到下一步的嘈杂运动 $\pmb{x}_{t-1}$，继续迭代去噪直至完成全部扩散步数。重噪声化采样基于后验分布：

$$\pmb{x}_{t-1} \sim \mathcal{N}(\mu_t(\pmb{x}_t, \hat{\pmb{x}}_0), \pmb{\Sigma}_t)$$

### 运动表示改进（MDM-SMPL）

为更好地支持身体部位拼接，STMC引入基于SMPL的运动表示。与原始MDM使用的263维关节旋转特征不同，MDM-SMPL采用SMPL pose参数（6D旋转表示）结合局部关节位置。该表示天然按身体部位组织，便于空间拼接时的部位拆分与重组，同时通过改进的扩散调度将采样速度提升约10倍。

## 实验与分析

### 实验设置

为评估STMC在多轨时间线控制任务上的表现，作者构建了**MTT（Multi-Track Timeline）数据集**，包含500条多轨时间线，每条时间线包含3个文本提示，分布在两条轨道上。评估限制为3个提示，目的是降低感知研究中用户的认知负荷，提高结果可靠性（Section 4.1）。所有方法均使用相同的预训练运动扩散模型权重进行评估，保证了比较的公平性。

评价指标分为两类：
- **语义正确性**：采用TMR-Score的M2T（motion-to-text）和M2M（motion-to-motion）指标，以及检索指标R@1、R@3，衡量生成动作在指定时间区间内与文本描述的语义对齐程度。
- **运动真实感**：使用FID⁺评估整体运动质量，以及**过渡距离（Transition Distance）**衡量动作过渡的平滑性——该指标计算相邻区间边界处局部关节位置的差异，值越小表示过渡越自然。

### 基线方法

实验对比了以下基线：
- **Single-text input**：将多轨时间线折叠为单一文本提示，直接输入预训练扩散模型。
- **DiffCollage**（Zhang et al., CVPR 2023）：将多轨时间线转换为单轨时间序列，利用DiffCollage进行时序动作组合，但缺乏空间组合能力。
- **SINC w/o Lerp**（Athanasiou et al., arXiv 2023）：独立生成各动作后进行一次性身体部位拼接，无过渡平滑处理。
- **SINC w/ Lerp**：在SINC一次性拼接后应用线性插值平滑过渡。

### 主要定量结果

Table 1展示了STMC与各基线在三种去噪模型（MDM、MotionDiffuse、MDM-SMPL）下的对比结果。核心发现如下：

**语义正确性方面**，STMC在所有指标上均显著优于基线。以MDM-SMPL为去噪模型时，STMC的R@1达到**30.5**，相比DiffCollage的22.6提升了**+7.9**；R@3达到**50.9**，提升**+7.6**；TMR-Score M2T达到**0.675**，相比DiffCollage的0.633提升**+0.042**。Single-text基线表现最差，说明将多轨时间线简单折叠为单一提示会严重损害语义保真度。SINC系列方法虽然通过独立去噪获得了较好的语义准确性，但其过渡质量存在明显缺陷。

**运动真实感方面**，STMC的FID⁺达到**0.459**，优于DiffCollage的0.532（降低**-0.073**）。更关键的是过渡距离指标：STMC仅为**0.9 cm**，而DiffCollage高达**4.6 cm**，SINC w/o Lerp更是达到**6.5 cm**。这验证了STMC的时空拼接策略——特别是基于DiffCollage的时序过渡机制——在生成平滑自然动作过渡方面的核心优势。SINC w/ Lerp虽然通过线性插值降低了过渡距离（3.0 cm），但仍远不及STMC的0.9 cm，说明简单的后处理插值无法替代在去噪过程中进行的结构化时序拼接。

### 感知研究

Figure 4展示的人类感知研究结果进一步验证了定量指标的趋势。在与SINC with Lerp的对比中，评估者在**运动真实感上66%偏好STMC**；在与DiffCollage的对比中，**真实感偏好达到68%**。语义准确性方面，STMC同样获得了显著偏好。该研究通过预热问题和金丝雀问题严格筛选参与者，确保了评估质量。

### 消融实验

**时序重叠长度的影响**（Table A.1）：通过调整总重叠长度（2\*l）从0.25s到1.25s，实验揭示了语义准确性与过渡平滑性之间的权衡。较短的重叠导致过渡距离升高，但每个裁剪片段与描述的匹配更好（per-crop语义指标更优）；较长的重叠使过渡更平滑，但语义准确性略有下降。这一发现验证了STMC时空拼接策略中重叠长度作为关键控制参数的有效性，并为实际应用中的参数选择提供了指导。

**子动作质量保持**：与独立生成（无需重叠和拼接）相比，STMC生成的每段子动作在FID上接近独立生成水平（MDM上STMC的FID为0.579，独立生成为0.582），表明组合过程未显著损害单动作的生成质量。

### 底层表示的影响

MDM-SMPL作为STMC的推荐去噪模型，采用SMPL pose参数（6D旋转表示）结合局部关节位置，替代了Guo et al.的263维位姿表示。在标准HumanML3D基准上，MDM-SMPL达到FID 0.38、R@3 0.74，优于原MDM和MotionDiffuse，验证了SMPL表示和改进训练的有效性。更重要的是，SMPL骨骼表示天然适合身体部位拼接操作，且改进的扩散调度将采样速度提升了**10倍**，同时维持生成质量。

### 失败模式与局限性

尽管STMC在整体指标上表现优异，分析揭示了以下失败模式：

1. **冲突动作处理失败**：STMC无法处理对同一身体部位具有冲突描述的重叠动作（例如同时“抬左手”和“挥左手”），这是因为身体部位时间线机制假设每个部位在同一时刻只执行一个动作。

2. **微观时序控制不足**：时序控制精度受限于预训练模型对单动作时长的生成能力，难以精确控制动作在指定区间内的微观时序分布。

3. **LLM标注依赖**：身体部位标注依赖外部GPT-3，标注错误可能传播至拼接过程，影响生成质量。

4. **轨道扩展瓶颈**：现有验证主要限于两轨时间线，扩展到更多轨道时组合复杂度急剧上升，当前方法尚未在该场景下充分验证。

5. **长时序泛化未验证**：实验仅在较短时长（<20秒）和3个提示的简单时间线上进行，长时序和密集组合场景的泛化性仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2401_08559/figures/007_Figure.jpg]]
*Figure: Resolving unassigned timeframes SINC heuristic*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2401_08559/figures/009_Figure.jpg]]
*Figure: A.1. Additional details of STMC: To create the final body parts timeline, we need to “fill the holes” by assigning a text to all locations of the body parts timeline (left). This is done by first splitting the timelines such that there is no intersection with other intervals, and then applying the SINC heuristic for each cut (right). Finally, we regroup the intervals by removing the cuts to obtain full body part timelines*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2401_08559/figures/004_Table_1.jpg]]
*Table 1: Quantitative baseline comparison: Our method STMC is compared to several strong baselines when using three different denoising models. The single-text and DiffCollage baselines struggle to handle complex compositional prompts that results from collapsing the timeline down to a single track. The SINC baselines produce reasonable semantic accuracy by denoising prompts independently as in STMC, but cause abrupt or unnatural transitions with higher transition distance (underlined) or FID*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2401_08559/figures/008_Table.jpg]]

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2401_08559/figures/011_Table.jpg]]
*Table: A.1. Influence of the overlap size: We report the performance of STMC (with MDM-SMPL) while varying the total overlap size (2 ∗ l). We observe that a smaller overlap size leads to a higher transition distance but each crop matches the description better (higher per-crop semantic correctness metrics). We observe the opposite for a larger overlap size*


 
## 方法谱系与知识库定位

### 1. 问题定位与基线关系

STMC解决的是一个在现有文本驱动三维人体运动生成文献中尚未被明确定义的任务：**多轨时间线控制**。传统方法仅支持单一文本提示生成一段完整运动，后续工作分别探索了**时序组合**（在非重叠区间上依次执行多个动作）和**空间组合**（在同一时间段内协调不同身体部位执行不同动作），但均无法同时精确控制多个动作的**时机、持续时间和身体部位协调**（Figure 2）。STMC将这一任务形式化为：给定一组可重叠的时间区间，每个区间绑定一个自然语言提示，要求生成的运动在每个区间内忠实反映对应提示的语义，并在区间边界处保持平滑过渡。

与STMC形成对比的基线方法可分为三类：

- **单文本折叠基线**：将多轨时间线折叠为单一文本描述，直接输入预训练扩散模型（如MDM、MotionDiffuse）。该方法完全丧失了细粒度时序控制能力，在语义正确性上表现最差（Table 1）。
- **时序组合基线**：**DiffCollage**（Zhang et al., CVPR 2023）将多轨时间线转换为单轨时间序列后进行时序动作组合，但缺乏空间组合能力，无法处理同一时刻不同身体部位执行不同动作的场景，导致过渡距离高达4.6 cm，远差于STMC的0.9 cm（Table 1）。
- **空间组合基线**：**SINC**（Athanasiou et al., arXiv 2023）独立生成各动作后一次性进行身体部位拼接，其无平滑版本（SINC w/o Lerp）产生突变过渡，而线性插值版本（SINC w/ Lerp）虽改善了平滑度，但语义准确性仍不及STMC。人类感知研究显示，评估者在运动真实感上以68%的比例偏好STMC优于DiffCollage，以66%的比例偏好STMC优于SINC with Lerp（Figure 4）。

### 2. 核心机制对比与创新

STMC的方法论创新在于将**多动作组合问题分解为多个单动作去噪子任务**，再通过迭代的时空拼接聚合结果。这一设计与上述基线存在本质差异：

| 方法 | 空间策略 | 时序策略 | 是否需要训练 |
|------|---------|---------|------------|
| Single-text | 无 | 无 | 否 |
| DiffCollage | 无 | 单轨内DiffCollage拼接 | 否 |
| SINC | 生成后一次性身体部位拼接 | 无/线性插值 | 否 |
| **STMC** | **去噪每一步动态身体部位拼接** | **每部位独立DiffCollage过渡** | **否** |

STMC的关键操作发生在**去噪过程的每一步**：首先利用LLM（GPT-3）自动标注每个文本提示涉及的身体部位，构建每个身体部位独立的时间线；然后在每一步去噪中，将当前嘈杂运动按提示区间裁剪，独立进行去噪预测；最后依据身体部位时间线进行空间拼接，并对重叠或相邻区间使用扩展的无条件去噪和条件去噪的加减运算（即 $\hat{\pmb{x}}_0 = \overset{-}{\pmb{x}}_0^{a_j - l : b_j + l} + \overset{-}{\pmb{x}}_0^{a_k - l : b_k + l} - \hat{\pmb{x}}_0^{\mathrm{uncond}}$）实现平滑时序过渡。这种迭代式的“去噪-拼接-重噪声化”循环使得每一步的预测都能感知到全局时间线约束，而非仅在生成后做一次性的后处理缝合。

### 3. 与底层运动表示的协同

STMC的另一个重要贡献在于证明了**方法可以无缝集成多种预训练运动扩散模型**，包括MDM、MotionDiffuse和MDM-SMPL。其中MDM-SMPL的改进尤为关键：将原始的263维关节旋转特征替换为SMPL姿态参数（6D旋转表示）并结合局部关节位置，不仅更适合身体部位拼接操作（因为SMPL的骨骼层级结构天然支持按部位分解），还通过改进的扩散调度将采样速度提升了10倍，同时在HumanML3D基准上达到FID 0.38、R@3 0.74，优于原MDM和MotionDiffuse（Appendix D）。这一结果表明，**表示层面的选择对测试时组合方法的有效性有显著影响**——更适合分解的表示可以降低拼接伪影的风险。

### 4. 适用边界与局限

尽管STMC展示了强大的组合能力，其适用边界受以下因素制约：

1. **身体部位冲突**：无法处理对同一身体部位具有冲突描述的重叠动作（例如同时“抬左手”和“挥左手”）。这是因为身体部位时间线要求每个部位在每个时刻只能被分配一个文本提示，冲突描述无法在因子图框架下得到一致解析。

2. **微观时序精度**：时序控制精度受限于预训练模型对单动作时长的生成能力。即使时间线指定了精确的起止时刻，模型生成的单动作可能无法完全填满或严格限制在指定区间内，导致实际动作与时间线存在偏差。

3. **LLM标注依赖**：身体部位标注依赖外部GPT-3，标注错误可能传播至拼接过程。例如，将“转身”错误地仅标注为下肢动作会导致上肢在转身过程中出现不协调。

4. **轨道数量扩展**：现有验证主要限于两轨时间线，扩展到更多并行轨道时，身体部位时间线的冲突概率和组合复杂度急剧上升，因子图的解算开销也随之增长。

5. **时长与复杂度泛化**：目前仅在较短时长（<20秒）和3个提示的简单时间线上验证，长时序和密集组合场景下的拼接质量退化风险尚未充分探索。

### 5. 开放问题

STMC的工作为后续研究开辟了若干方向：

- **端到端训练**：当前测试时组合方法虽无需额外训练，但每步去噪的计算开销较大。能否设计直接接受多轨时间线作为输入的端到端可训练模型，在训练阶段就学习组合能力，从而在推理时避免迭代拼接？

- **跨模态推广**：STMC的核心思想——将复合条件分解为独立去噪子任务再通过因子图聚合——是否可推广到其他模态的生成控制？例如文本到视频的时空组合、文本到场景的多物体协调等场景存在类似的“多条件并行控制”需求。

- **自适应重叠优化**：消融实验表明，时序重叠长度在语义正确性和过渡平滑性之间存在明确权衡（Table A.1：较短重叠提高语义准确性但增加过渡距离）。是否存在自动优化重叠长度的机制，使其根据动作类型和过渡难度自适应调节？

- **动态身体部位标注**：当前LLM标注是静态的——每个文本被分配固定的身体部位集。但在实际运动中，同一动作在不同阶段可能涉及不同的肢体（如“起跳”初期以腿部为主，后期手臂参与摆动）。动态标注策略可能进一步提升拼接的自然度。

- **交互式编辑**：STMC的迭代去噪框架天然支持在生成过程中介入修改。结合用户交互，允许对生成结果进行局部编辑或微调（如调整某个区间的动作强度、替换某个身体部位的运动），可进一步提高创作控制力，使该方法更适用于动画制作等实际应用场景。

## 原文 PDF

![[paperPDFs/CVPR_2024/STMC_Multi_Track_Timeline_Control_for_Text_Driven_3D_Human_Motion_Generation.pdf]]
