---
title: "X-MoGen: Unified Motion Generation across Humans and Animals"
type: paper
paper_level: A
venue: AAAI
year: 2026
pdf_ref: paperPDFs/AAAI_2026/X_MoGen_Unified_Motion_Generation_across_Humans_and_Animals.pdf
aliases:
- XM
- X-MoGen
tags:
- AAAI_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "通过条件图变分自编码器（CGAE）为每个物种生成物种特定的规范T-pose骨骼长度先验，并在运动自编码器（AE）与生成过程中引入针对骨骼长度的形态一致性模块（MCM）和形态损失，使模型显式感知并适应不同的身体比例。"
primary_logic: "将物种特定的形态学先验（T-pose骨骼长度）融入文本条件运动生成的两阶段框架，辅以统一的骨骼拓扑和形态学正则化，是实现统一跨物种运动生成的核心机制。"
claims:
- "在UniMo4D主测试集上，X-MoGen在所有文本-运动生成指标上显著超越先前最优方法，FID从0.189（MARDM）降至0.050。"
- "消融实验证明CGAE生成的T-pose先验和形态一致性模块（MCM）对降低形态误差（MME）至关重要，移除后MME分别升至0.228和0.238。"
- "在未见物种测试集上，X-MoGen仍能生成连贯且形态一致的运动，而对比方法产生明显伪影。"
- "UniMo4D test set (seen species) 上 FID↓ = 0.050 ± .001"
---

# X-MoGen: Unified Motion Generation across Humans and Animals

> [!tip] 核心洞察
> 将物种特定的形态学先验（T-pose骨骼长度）融入文本条件运动生成的两阶段框架，辅以统一的骨骼拓扑和形态学正则化，是实现统一跨物种运动生成的核心机制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | X-MoGen：跨物种统一运动生成模型 |
| 英文题名 | X-MoGen: Unified Motion Generation across Humans and Animals |
| 会议/期刊 | AAAI 2026 |
| Links | [paper](https://arxiv.org/abs/2508.05162) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | X-MoGen |
| Dataset | UniMo4D test set (seen species) |

> [!tip] 效果简介
> - UniMo4D test set (seen species) 上，FID↓ 为 0.050 ± .001，对比 0.189 ± .002 (MARDM)，变化 -0.139。
> - UniMo4D test set (seen species) 上，R-Precision Top-1 ↑ 为 0.848 ± .001，对比 0.823 ± .001 (MARDM)，变化 +0.025。
> - UniMo4D test set (seen species) 上，MM-Dist↓ 为 0.742 ± .002，对比 0.874 ± .001 (MARDM)，变化 -0.132。

## 概述

**问题与瓶颈。** 文本驱动的人体运动生成近年来取得了显著进展，但现有方法普遍将人类与动物动作分开建模，难以应对跨物种场景。其根本瓶颈在于，不同物种的骨骼拓扑与形态参数——尤其是骨骼长度与身体比例——差异极大，导致在统一框架下生成形态合理、动作真实的跨物种运动极具挑战。

**核心方法。** 本文提出 **X-MoGen**，首个面向跨物种文本驱动运动生成的统一框架。该方法的核心机制是：通过条件图变分自编码器（CGAE）为每个物种生成物种特定的规范T-pose骨骼长度先验，并将此形态学先验融入运动自编码器与生成过程，辅以形态一致性模块（MCM）与形态损失，使模型显式感知并适应不同的身体比例。整体采用两阶段架构：第一阶段由CGAE与运动自编码器（AE）联合学习紧凑的连续运动潜在空间及形态约束；第二阶段以掩码Transformer（M-Trans）结合流匹配扩散头，在文本条件与T-pose先验的共同引导下生成运动序列。

**关键结论。** 在UniMo4D主测试集上，X-MoGen在所有文本-运动生成指标上显著超越先前最优方法：FID从MARDM的0.189降至**0.050**，R-Precision Top-1从0.823提升至**0.848**，MM-Dist从0.874降至**0.742**，形态误差MME从0.251降至**0.201**（Table 1）。消融实验证实，CGAE生成的T-pose先验与形态一致性模块对维持骨骼合理性至关重要——移除后MME分别恶化至0.228与0.238（Table 4）。在未见物种测试集上，X-MoGen仍能生成连贯且形态一致的运动，而对比方法出现明显伪影（Figure 4, Table 2），验证了框架的跨物种泛化能力。

**方法定位。** 相较于MDM（Tevet et al., ICLR 2023）、T2M-GPT（Zhang et al., CVPR 2023）、MoMask（Guo et al., CVPR 2024）等仅支持单物种的方法，以及MARDM（Meng et al., CVPR 2025）和AniMo（Wang et al., CVPR 2025）等动物专用方法，X-MoGen首次实现了覆盖115个物种的统一生成，其关键在于将物种特定的形态学先验与连续潜在空间建模相结合，突破了固定骨骼长度的限制。

## 背景与动机

文本驱动的三维人体运动生成近年来取得了显著进展，涌现出**MDM**（Tevet et al., ICLR 2023）、**T2M-GPT**（Zhang et al., CVPR 2023）、**MoMask**（Guo et al., CVPR 2024）等一系列代表性工作。这些方法在人体运动生成上展现出令人印象深刻的文本-运动对齐能力和运动自然度。然而，当视线转向动物运动生成时，现有范式面临根本性挑战。

核心瓶颈在于**跨物种形态差异**。不同物种之间的骨骼拓扑结构和形态参数——尤其是骨骼长度与身体比例——差异悬殊。人类的直立双足结构与四足动物的水平躯干结构在运动学上几乎无法直接兼容。现有方法（如**MARDM**，Meng et al., CVPR 2025；**AniMo**，Wang et al., CVPR 2025）将人类与动物动作分开建模，需要为每个物种训练独立模型，这不仅造成计算资源浪费，更从根本上丧失了跨物种运动理解和生成的能力。对于训练数据中未出现的物种，这些方法完全无法生成形态合理、动作真实的运动序列。

X-MoGen的提出正是为了填补这一空白：**构建一个统一的跨物种文本驱动运动生成框架**，使其能够同时处理人类和动物运动，并在未见物种上保持形态一致性与动作连贯性。这一目标的实现需要解决两个关键问题：其一，如何让模型感知并适应不同物种的骨骼形态差异；其二，如何在生成过程中显式约束骨骼长度的合理性，避免产生形态扭曲的运动伪影。

## 核心创新

X-MoGen 的核心创新在于首次将**物种特定的形态学先验**显式注入文本驱动的运动生成流程，从而突破现有方法只能分别建模人类与动物运动的根本局限。这一突破通过以下三个关键机制实现：

### 1. 物种条件T-pose骨骼长度先验（CGAE）

现有方法（如 **MDM** (Tevet et al., ICLR 2023)、**MoMask** (Guo et al., CVPR 2024)、**MARDM** (Meng et al., CVPR 2025) 等）均假设固定的骨骼长度，无法适应不同物种间巨大的形态差异。X-MoGen 引入**条件图变分自编码器（CGAE）**，以物种标签为条件，为每个物种生成其专属的规范T-pose骨骼长度向量 $\mathbf{b}$。该模块通过平衡骨骼重建精度与潜在空间KL正则化进行训练：

$$\mathcal{L}_{\mathrm{CGAE}} = \left\| \hat{\mathbf{b}} - \mathbf{b} \right\|_2^2 + \beta D_{\mathrm{KL}} \left( q_{\phi}(\mathbf{z}_{\mathrm{pose}} \mid \mathbf{b}, \mathbf{c}) \| p(\mathbf{z}_{\mathrm{pose}}) \right)$$

这一设计使模型在推理时能根据输入文本中隐含的物种信息（如“a dog is running”），动态生成与之匹配的骨骼比例先验，为后续运动生成提供形态学“锚点”。消融实验证实，移除CGAE先验后，形态误差（MME）从 0.201 急剧上升至 0.228（Table 4），表明该模块对维持骨骼合理性至关重要。

### 2. 形态一致性模块与形态损失（MCM）

仅有T-pose先验不足以保证生成运动过程中骨骼长度的时序一致性。X-MoGen 在运动自编码器（AE）和掩码生成阶段分别施加形态监督：

- **AE阶段**：在标准运动重建MSE损失之外，引入**形态重建损失** $\mathcal{L}_{\mathrm{morph}}^{\mathrm{recon}}$，逐帧比较重建运动与真实运动的骨骼长度，迫使潜在空间编码保留形态信息：

$$\mathcal{L}_{\mathrm{morph}}^{\mathrm{recon}} = \frac{1}{L} \sum_{t=1}^{L} \left\| \mathcal{B}(\hat{\mathbf{x}}_t) - \mathcal{B}(\mathbf{x}_t) \right\|_2^2$$

- **生成阶段**：**形态一致性模块（MCM）** 从生成的潜在运动序列 $\hat{\mathbf{Z}}$ 中预测骨骼长度，并通过**形态引导损失** $\mathcal{L}_{\mathrm{morph}}^{\mathrm{guide}}$ 惩罚其与CGAE先验的偏差：

$$\mathcal{L}_{\mathrm{morph}}^{\mathrm{guide}} = \left\| f_{\mathrm{MCM}}(\hat{\mathbf{Z}}) - \mathbf{b} \right\|_2^2$$

消融实验表明，移除MCM后MME恶化至 0.238（Table 4），证实该模块是维持跨物种运动形态合理性的关键瓶颈。

### 3. 连续潜在空间建模替代离散量化

现有方法（如 T2M-GPT、MoMask）普遍采用 VQ/RVQ 等离散量化压缩运动，但离散编码在跨物种场景下难以保留精细的骨骼长度信息。X-MoGen 改用**连续潜在空间的自编码器**，配合形态损失进行重建。Table 3 的对比显示，连续AE在重建精度和形态保持上均显著优于量化方法，为后续生成阶段提供了更高质量的形态感知表示。

### 4. 掩码建模与流匹配扩散的生成范式

在第二阶段，X-MoGen 采用**掩码Transformer（M-Trans）** 融合文本特征与T-pose先验，生成上下文表示，再通过**基于流匹配的扩散头**从噪声中预测被掩码的运动潜在令牌。流匹配损失定义为：

$$\mathcal{L}_{\mathrm{flow}} = \frac{1}{\lvert \mathcal{M} \rvert} \sum_{i \in \mathcal{M}} \mathbb{E}_{\tau, \hat{\mathbf{z}}_i, \mathbf{z}_i} \left[ \lVert \mathbf{v}_{\boldsymbol{\theta}} ( \mathbf{z}_{\tau, i}, \tau, \mathbf{h}_i ) - ( \mathbf{z}_i - \hat{\mathbf{z}}_i ) \rVert_2^2 \right]$$

推理时结合**分类器无关引导**增强文本对齐：

$$\mathbf{v}_{\mathrm{guided}, i}^{(n)} = \mathbf{v}_{\mathrm{uncond}, i}^{(n)} + \omega \cdot \left( \mathbf{v}_{\mathrm{cond}, i}^{(n)} - \mathbf{v}_{\mathrm{uncond}, i}^{(n)} \right)$$

这一混合范式兼具掩码建模的效率与扩散模型的生成质量，同时通过形态引导损失实现端到端的形态约束。

### 创新总结

上述四个机制形成闭环：CGAE提供物种级形态先验 → 连续AE在形态损失监督下压缩运动 → M-Trans融合先验与文本生成上下文 → 扩散头在流匹配与形态引导下预测运动。这一设计使X-MoGen成为首个在统一框架下支持115个物种运动生成的模型，在UniMo4D已见物种测试集上将FID从MARDM的 0.189 降至 0.050，并在未见物种上展现出显著的泛化能力（Table 2）。

## 整体框架

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2508_05162/figures/001_Figure_1.jpg]]
*Figure 1: X-MoGen achieves a wide range of capabilities within a single unified framework, including generating both human and animal motions from text descriptions and enabling smooth cross-species motion transitions*

X-MoGen 采用两阶段流水线架构，将文本到运动的生成问题分解为“特征建模”与“条件生成”两个解耦的阶段，从而在统一框架内处理跨物种的形态差异。

**第一阶段：特征建模。** 该阶段由两个并行的编码器构成。条件图变分自编码器（CGAE）以物种标签为条件，从训练数据中学习各物种的规范 T‑pose 骨骼长度先验，输出一个物种特定的骨骼长度向量 $\hat{\mathbf{b}}$；其训练目标为重建误差与 KL 正则项的加权和：

$$
\mathcal{L}_{\mathrm{CGAE}} = \left\| \hat{\mathbf{b}} - \mathbf{b} \right\|_2^2 + \beta D_{\mathrm{KL}} \left( q_{\phi}(\mathbf{z}_{\mathrm{pose}} \mid \mathbf{b}, \mathbf{c}) \| p(\mathbf{z}_{\mathrm{pose}}) \right)
$$

同时，运动自编码器（AE）将原始运动序列 $\mathbf{x}$ 压缩到一个连续的潜在空间，并通过解码器重建运动 $\hat{\mathbf{x}}$。为维护骨骼结构的合理性，AE 的训练损失在逐帧均方误差 $\mathcal{L}_{\mathrm{MSE}}^{\mathrm{recon}}$ 之外，额外引入形态重建损失 $\mathcal{L}_{\mathrm{morph}}^{\mathrm{recon}}$，该损失比较重建运动与真实运动的骨骼长度 $\mathcal{B}(\cdot)$：

$$
\mathcal{L}_{\mathrm{AE}} = \mathcal{L}_{\mathrm{MSE}}^{\mathrm{recon}} + \lambda_{\mathrm{morph}}^{\mathrm{recon}} \cdot \mathcal{L}_{\mathrm{morph}}^{\mathrm{recon}}
$$

这一阶段为后续生成提供了两个关键组件：物种特定的 T‑pose 先验，以及一个形态感知的连续运动潜在空间。

**第二阶段：掩码运动生成。** 该阶段以文本描述和物种信息为输入，通过掩码 Transformer（M‑Trans）与扩散补全头协作生成运动潜在序列。具体流程为：CLIP 文本编码器提取句子级和词级文本特征；CGAE 根据物种条件生成对应的 T‑pose 骨骼先验；M‑Trans 将文本特征与 T‑pose 先验融合，对部分被掩码的运动潜在令牌进行上下文建模，输出条件表示 $\mathbf{h}$。随后，基于流匹配的扩散头从噪声中预测被掩码位置的运动潜在表示，其训练目标为流匹配损失 $\mathcal{L}_{\mathrm{flow}}$。同时，形态一致性模块（MCM）从生成的潜在序列中预测骨骼长度，并通过形态引导损失 $\mathcal{L}_{\mathrm{morph}}^{\mathrm{guide}}$ 惩罚与参考骨骼长度的偏差：

$$
\mathcal{L}_{\mathrm{gen}} = \mathcal{L}_{\mathrm{flow}} + \lambda_{\mathrm{morph}}^{\mathrm{guide}} \cdot \mathcal{L}_{\mathrm{morph}}^{\mathrm{guide}}
$$

**推理阶段。** 推理时，扩散头从纯噪声开始迭代去噪，生成完整的运动潜在序列，再由 AE 解码器重建为运动数据。为增强文本对齐，推理过程采用分类器无关引导，在每一步将条件速度 $\mathbf{v}_{\mathrm{cond}}$ 与无条件速度 $\mathbf{v}_{\mathrm{uncond}}$ 按引导强度 $\omega$ 进行插值：

$$
\mathbf{v}_{\mathrm{guided}, i}^{(n)} = \mathbf{v}_{\mathrm{uncond}, i}^{(n)} + \omega \cdot \left( \mathbf{v}_{\mathrm{cond}, i}^{(n)} - \mathbf{v}_{\mathrm{uncond}, i}^{(n)} \right)
$$

**关键设计意图。** 整个框架的核心在于将物种形态学先验显式地注入生成过程：CGAE 提供骨骼长度基准，AE 在压缩阶段施加形态正则化，MCM 在生成阶段持续约束骨骼合理性。三者协同，使模型在统一的骨骼拓扑下，能够自适应地生成形态合理、动作真实的跨物种运动。

## 核心模块与公式推导

X-MoGen 采用两阶段框架解决跨物种运动生成问题。第一阶段负责运动特征建模，第二阶段完成文本条件生成。

### 第一阶段：运动特征建模

第一阶段包含两个并行的自编码器。

**条件图变分自编码器（CGAE）** 接收物种条件 $\mathbf{c}$ 和参考 T-pose 骨骼长度向量 $\mathbf{b}$，通过图编码器 $q_{\phi}$ 编码为潜在变量 $\mathbf{z}_{\mathrm{pose}}$，再由解码器重建骨骼长度。其训练目标为：

$$
\mathcal{L}_{\mathrm{CGAE}} = \left\| \hat{\mathbf{b}} - \mathbf{b} \right\|_2^2 + \beta D_{\mathrm{KL}} \left( q_{\phi}(\mathbf{z}_{\mathrm{pose}} \mid \mathbf{b}, \mathbf{c}) \| p(\mathbf{z}_{\mathrm{pose}}) \right)
$$

其中 $\hat{\mathbf{b}}$ 为重建的骨骼长度，$\beta$ 控制 KL 正则化强度，$p(\mathbf{z}_{\mathrm{pose}})$ 为标准高斯先验。CGAE 的核心作用是学习物种特定的规范 T-pose 骨骼长度先验，为后续生成提供形态学锚点。

**运动自编码器（AE）** 将运动序列 $\mathbf{x}$ 压缩到连续潜在空间 $\mathbf{Z}$ 并重建。其总损失为重建损失与形态损失的加权和：

$$
\mathcal{L}_{\mathrm{AE}} = \mathcal{L}_{\mathrm{MSE}}^{\mathrm{recon}} + \lambda_{\mathrm{morph}}^{\mathrm{recon}} \cdot \mathcal{L}_{\mathrm{morph}}^{\mathrm{recon}}
$$

逐帧均方误差衡量运动重建精度：

$$
\mathcal{L}_{\mathrm{MSE}}^{\mathrm{recon}} = \frac{1}{L} \sum_{t=1}^{L} \left\| \hat{\mathbf{x}}_t - \mathbf{x}_t \right\|_2^2
$$

形态重建损失通过比较骨骼长度维护结构一致性，$\mathcal{B}(\cdot)$ 为骨骼长度提取函数：

$$
\mathcal{L}_{\mathrm{morph}}^{\mathrm{recon}} = \frac{1}{L} \sum_{t=1}^{L} \left\| \mathcal{B}(\hat{\mathbf{x}}_t) - \mathcal{B}(\mathbf{x}_t) \right\|_2^2
$$

### 第二阶段：掩码运动生成

第二阶段以掩码 Transformer（M-Trans）和扩散完成头为核心。M-Trans 接收文本特征（来自 CLIP 编码器）、CGAE 生成的 T-pose 先验以及部分掩码的运动潜在序列，输出上下文表示 $\mathbf{h}_i$。扩散头基于流匹配范式，从噪声 $\hat{\mathbf{z}}_i$ 预测被掩码位置的目标速度场：

$$
\mathcal{L}_{\mathrm{flow}} = \frac{1}{\lvert \mathcal{M} \rvert} \sum_{i \in \mathcal{M}} \mathbb{E}_{\tau, \hat{\mathbf{z}}_i, \mathbf{z}_i} \left[ \lVert \mathbf{v}_{\boldsymbol{\theta}} ( \mathbf{z}_{\tau, i}, \tau, \mathbf{h}_i ) - ( \mathbf{z}_i - \hat{\mathbf{z}}_i ) \rVert_2^2 \right]
$$

其中 $\mathcal{M}$ 为被掩码位置的索引集，$\tau$ 为流匹配时间步，$\mathbf{v}_{\boldsymbol{\theta}}$ 为速度预测网络。

**形态一致性模块（MCM）** 从生成的潜在序列 $\hat{\mathbf{Z}}$ 预测骨骼长度，并通过形态引导损失惩罚与参考骨骼长度 $\mathbf{b}$ 的偏差：

$$
\mathcal{L}_{\mathrm{morph}}^{\mathrm{guide}} = \left\| f_{\mathrm{MCM}}(\hat{\mathbf{Z}}) - \mathbf{b} \right\|_2^2
$$

第二阶段总损失为：

$$
\mathcal{L}_{\mathrm{gen}} = \mathcal{L}_{\mathrm{flow}} + \lambda_{\mathrm{morph}}^{\mathrm{guide}} \cdot \mathcal{L}_{\mathrm{morph}}^{\mathrm{guide}}
$$

### 推理：分类器无关引导

推理时采用分类器无关引导增强文本对齐，引导速度由无条件与条件速度的插值得到：

$$
\mathbf{v}_{\mathrm{guided}, i}^{(n)} = \mathbf{v}_{\mathrm{uncond}, i}^{(n)} + \omega \cdot \left( \mathbf{v}_{\mathrm{cond}, i}^{(n)} - \mathbf{v}_{\mathrm{uncond}, i}^{(n)} \right)
$$

其中 $\omega$ 为引导尺度，$n$ 为去噪步索引。

## 实验与分析

### 数据集与评估协议

实验基于 **UniMo4D** 数据集，该数据集涵盖人类及多种动物（四足类为主）的文本-运动对。图3展示了数据集的物种分布与关键骨骼长度分布，凸显了跨物种形态差异带来的挑战。评估分为两个测试集：**已见物种（seen species）** 和 **未见物种（unseen species）**，后者用于检验模型的泛化能力。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2508_05162/figures/003_Figure_3.jpg]]
*Figure 3: Statistics of the UniMo4D dataset. (a) Species distribution. (b) Length distribution of key bones*

评价指标包括：
- **R-Precision**（Top-1/2/3）：衡量生成运动与文本的语义对齐程度，值越高越好。
- **FID**：衡量生成运动分布与真实运动分布的距离，值越低越好。
- **MM-Dist**：多模态距离，衡量生成运动与对应文本在特征空间中的匹配度，值越低越好。
- **MME**（Mean Morphological Error）：自建指标，定义为生成运动序列中各帧骨骼长度与参考T-pose骨骼长度的平均L1偏差：

$$
\mathbf{MME} = \frac{1}{L \cdot N_b} \sum_{t=1}^{L} \| \hat{\mathbf{b}}_t - \mathbf{b} \|_1
$$

其中 $L$ 为帧数，$N_b$ 为骨骼数量。MME直接量化生成运动的形态合理性。

### 主实验结果

**Table 1** 展示了在已见物种测试集上的定量对比。X-MoGen在所有指标上均显著超越先前最优方法：

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2508_05162/figures/004_Table_1.jpg]]
*Table 1: Comparison of text-driven motion generation on the UniMo4D dataset. The right arrow (→) indicates that values closer to the ground truth motion are better. The best results for each metric are shown in bold*

| 指标 | X-MoGen | MARDM（最优基线） | 提升幅度 |
|------|---------|-------------------|----------|
| FID↓ | **0.050** | 0.189 | -73.5% |
| R-Precision Top-1↑ | **0.848** | 0.823 | +3.0% |
| MM-Dist↓ | **0.742** | 0.874 | -15.1% |
| MME↓ | **0.201** | 0.251 | -19.9% |

FID从0.189降至0.050的幅差尤其显著，表明X-MoGen生成的跨物种运动分布与真实数据高度吻合。MME的降低则直接验证了CGAE与MCM在维持骨骼长度一致性方面的有效性。对比的基线方法包括 **MDM**（Tevet et al., ICLR 2023）、**T2M-GPT**（Zhang et al., CVPR 2023）、**AttT2M**（Zhong et al., ICCV 2023）、**MMM**（Pinyoanuntapong et al., CVPR 2024）、**MoMask**（Guo et al., CVPR 2024）、**MARDM**（Meng et al., CVPR 2025）和 **AniMo**（Wang et al., CVPR 2025）。所有基线均使用官方实现或统一配置在UniMo4D上公平训练。

**Table 2** 报告了未见物种测试集上的泛化性能。X-MoGen在全部指标上保持最优：FID为19.935，MME为0.229。图4的定性对比进一步印证了这一优势——基线方法在未见物种上产生明显的运动伪影（红框/箭头标出），而X-MoGen生成的序列连贯且形态一致。这归因于CGAE能够为任意新物种生成合理的T-pose骨骼先验，使模型无需额外训练即可适应新的身体比例。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2508_05162/figures/005_Table_2.jpg]]
*Table 2: Comparison of text-driven motion generation on the UniMo4D unseen species test dataset. The right arrow (→) indicates that values closer to the ground truth motion are better. The best results for each metric are shown in bold*

### 运动压缩方式对比

**Table 3** 对比了不同运动压缩方法的性能。X-MoGen采用的连续潜在空间自编码器（AE）在重建精度和形态保持上均显著优于基于VQ/RVQ的离散量化方法。这一结果确立了连续潜在建模在跨物种场景下的优势——离散量化在骨骼长度差异巨大的情况下难以保持重建精度，而AE配合形态损失 $\mathcal{L}_{\mathrm{morph}}^{\mathrm{recon}}$ 能有效约束结构一致性。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2508_05162/figures/007_Table_3.jpg]]
*Table 3: Quantitative results of different motion compressors on the UniMo4D test set*

### 消融实验

**Table 4** 系统拆解了各组件的贡献：

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2508_05162/figures/008_Table_4.jpg]]
*Table 4: Ablation study on the UniMo4D test set*

1. **移除词级文本特征（w/o W）**：FID轻微上升至0.053，说明句子级特征已提供足够语义指引，但词级特征对精细对齐仍有增益。

2. **移除CGAE的T-pose先验（w/o CGAE）**：MME从0.201升至0.228，FID亦有所恶化。这证明物种特定的骨骼长度先验是形态合理性的关键瓶颈——没有该先验，模型无法感知不同物种的身体比例差异。

3. **移除形态一致性模块MCM（w/o MCM）**：MME进一步恶化至0.238，是消融实验中形态退化最严重的情况。MCM在生成阶段直接惩罚骨骼长度偏差，与AE阶段的形态重建损失形成互补。

4. **移除AE中的形态重建损失 $\mathcal{L}_{\mathrm{morph}}^{\mathrm{recon}}$**：同样导致MME上升，表明在潜在空间学习阶段注入形态约束对后续生成质量至关重要。

### 失败模式与局限性

尽管X-MoGen在跨物种生成上取得突破，**未见物种测试集上的FID仍高达19.935**，与真实数据存在明显差距。这表明模型对完全未见的生物形态（尤其是极端身体比例）的生成真实感仍有不足。此外，当前框架主要针对四足动物与人类，向鸟类、鱼类等拓扑差异更大的物种推广时，统一骨骼拓扑的假设可能不再适用。

### 应用展示

X-MoGen支持**跨物种运动变换**：利用CGAE为不同物种生成各自的T-pose先验，可在保持运动语义的前提下，将一种物种的运动迁移至另一种物种的骨骼上，实现平滑的跨物种运动过渡（见Figure 1示意）。这一能力无需额外训练，仅通过替换CGAE的物种条件即可完成。

## 方法谱系与知识库定位

**问题定位与现有范式**

文本驱动运动生成领域长期面临一个根本性瓶颈：人类与动物动作被分别建模，难以在统一框架下处理。其深层原因在于不同物种间骨骼拓扑和形态参数（骨骼长度、身体比例）差异巨大，导致单一模型难以同时保证动作真实性与形态合理性。现有方法如 **MDM** (Tevet et al., ICLR 2023)、**T2M-GPT** (Zhang et al., CVPR 2023)、**AttT2M** (Zhong et al., ICCV 2023)、**MMM** (Pinyoanuntapong et al., CVPR 2024)、**MoMask** (Guo et al., CVPR 2024) 等均聚焦于单一人体的运动生成，而 **AniMo** (Wang et al., CVPR 2025) 虽面向动物，但仍限定于特定物种。**MARDM** (Meng et al., CVPR 2025) 是此前在 UniMo4D 数据集上表现最优的方法，其 FID 为 0.189，但同样不具备跨物种统一建模能力。

X-MoGen 的核心突破在于将物种特定的形态学先验（T-pose 骨骼长度）显式融入文本条件运动生成的两阶段框架，辅以统一的骨骼拓扑和形态学正则化，首次实现了覆盖 115 个物种的统一运动生成。这一设计直接回应了跨物种建模的核心矛盾：不同物种的身体比例差异不再是阻碍，而是被转化为可学习的条件先验。

**关键设计选择与对比**

在运动压缩方式上，X-MoGen 采用连续潜在空间的自编码器（AE）替代了主流方法中常见的 VQ/RVQ 离散量化策略。Table 3 的对比实验表明，连续 AE 在重建精度和形态保持上显著优于量化方法，这为后续生成阶段提供了更高质量的潜在表示。在生成范式上，X-MoGen 并未沿用纯扩散或纯掩码建模路线，而是设计了掩码 Transformer（M-Trans）结合流匹配扩散头的混合架构，并采用分类器无关引导增强文本对齐。

形态一致性模块（MCM）和条件图变分自编码器（CGAE）是 X-MoGen 区别于所有基线方法的两个独特组件。CGAE 根据物种条件生成规范 T-pose 骨骼长度先验，MCM 则在运动自编码器和生成过程中持续惩罚骨骼长度偏差。消融实验（Table 4）提供了决定性证据：移除 CGAE 后，形态误差 MME 从 0.201 升至 0.228；移除 MCM 后，MME 进一步恶化至 0.238。这表明两者对维持跨物种骨骼合理性均不可或缺，且作用机制互补——CGAE 提供全局形态先验，MCM 实施逐序列的局部约束。

**适用边界与局限**

尽管 X-MoGen 在已见物种上取得了显著优势（FID 从 MARDM 的 0.189 降至 0.050），其在未见物种上的表现仍存在明显差距。Table 2 显示，在 UniMo4D 未见物种测试集上，X-MoGen 的 FID 为 19.935，虽优于所有对比方法，但与真实数据之间的鸿沟表明跨物种泛化的真实感仍有较大提升空间。Figure 4 的定性对比也印证了这一点：X-MoGen 能生成连贯且形态一致的运动，而基线方法产生明显伪影，但生成质量与已见物种相比仍有退化。

当前框架的适用边界主要受限于四足动物范畴。论文中提出的开放问题直接指向这一局限：如何推广至鸟类、鱼类等更多样化的生物形态，以及能否借助互联网大规模视频数据改善未见物种的生成质量。此外，将运动生成与物理模拟相结合以进一步保证物理合理性，也是值得探索的方向。

**知识库定位**

X-MoGen 在文本驱动运动生成领域填补了“跨物种统一建模”这一空白。其贡献不在于提出全新的生成范式，而在于识别并解决了形态学差异这一阻碍统一建模的关键瓶颈。CGAE + MCM 的组合设计为后续研究提供了一个可复用的技术方案：当需要处理多形态、多尺度的运动数据时，显式建模形态学先验并施加一致性约束是一条经过验证的有效路径。该工作也为运动生成与生物力学、物理模拟的交叉研究打开了接口。

## 原文 PDF

![[paperPDFs/AAAI_2026/X_MoGen_Unified_Motion_Generation_across_Humans_and_Animals.pdf]]
