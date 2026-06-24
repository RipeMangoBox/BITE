---
title: "Mind the Generative Details: Direct Localized Detail Preference Optimization for Video Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Mind_the_Generative_Details_Direct_Localized_Detail_Preference_Optimization_for_Video_Diffusion_Models.pdf
code_link: "https://github.com/1170300714/Local-DPO"
aliases:
- MGDDLDPOVDM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/benchmarks_datasets_evaluation
core_operator: 通过局部破坏真实视频生成负样本，并引入掩码引导的区域感知 DPO 损失，将偏好优化严格限制在损坏区域，从而直接驱动模型学习局部细节偏好。
primary_logic: 以真实视频为锚点，利用模型自身生成能力构造局部退化的对比对，可在零标注成本下获得高置信度、区域级的偏好信号；结合归一化的区域感知 DPO 损失，能让模型高效地聚焦于局部生成细节的改善，同时避免全局结构漂移。
claims:
- LocalDPO 使用真实视频作为正样本，并通过局部破坏生成负样本，单次推理即可构造偏好对，无需额外评判模型或人工标注。
- 区域感知 DPO 损失在所有质量维度均带来显著提升，尤其是视觉质量和图像质量。
- 在 CogVideoX-2B/5B 和 Wan2.1-1.3B 三个基座上，LocalDPO 在 VBench 和 VideoJAM 的审美质量、成像质量、人类偏好分数及 VideoAlign 总分上均超越 SFT、Vanilla DPO 和 DenseDPO。
- VBench (aesthetic & imaging quality dimensions) 上 Aesthetic Quality / Imaging Quality / VideoAlign Overall = 0.6499 / 0.7080 / 7.8568 (CogVideoX-2B); 0.6274 / 0.7107 /...
---

# Mind the Generative Details: Direct Localized Detail Preference Optimization for Video Diffusion Models

> [!tip] 核心洞察
> 以真实视频为锚点，利用模型自身生成能力构造局部退化的对比对，可在零标注成本下获得高置信度、区域级的偏好信号；结合归一化的区域感知 DPO 损失，能让模型高效地聚焦于局部生成细节的改善，同时避免全局结构漂移。

| 字段 | 内容 |
|------|------|
| 中文题名 | 关注生成细节：面向视频扩散模型的直接局部细节偏好优化 |
| 英文题名 | Mind the Generative Details: Direct Localized Detail Preference Optimization for Video Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.04068) · [Code](https://github.com/1170300714/Local-DPO) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/benchmarks_datasets_evaluation |
| Method | LocalDPO |
| Dataset | VBench, VideoJAM, Human Evaluation |

> [!tip] 效果简介
> - VBench (aesthetic & imaging quality dimensions) 上，Aesthetic Quality / Imaging Quality / VideoAlign Overall 0.6499 / 0.7080 / 7.8568 (CogVideoX-2B); 0.6274 / 0.7107 / 10.2930 (CogVideoX-5... vs 参见 Table 1 和 Table 2 中 Baseline/SFT/Vanilla DPO/DenseDPO 行的对应数值 (例如 Aesthetic Quality 相比 Baseline 提升 0.022 (CogVideoX-2B)，Imaging Quality 提升 0.0...)。
> - VideoJAM 上，Aesthetic Quality / Imaging Quality / VideoAlign Overall 0.5604 / 0.7001 / 7.5397 (CogVideoX-2B); 0.5782 / 0.6727 / 7.6424 (CogVideoX-5B... vs 参见 Table 2 (例如 Imaging Quality 相比 Baseline 提升 0.0674 (CogVideoX-2B))。
> - Human Evaluation 上，Win rate against Vanilla DPO (General) 88.86% average win rate (Fig.4); Fig.7 shows LocalDPO wins on all dimensions vs... vs Vanilla DPO (约 33.4% direct wins + 58.7% ties in Fig.4 General dimension)。

## 概述

**核心问题**：现有的视频扩散模型偏好优化方法（如 Vanilla DPO）依赖对同一提示多次采样、再借助评判模型或人工进行全局排序来构造偏好对。这一范式存在三重瓶颈：① 多轮采样与标注成本高昂；② 全局偏好信号可能模糊甚至自相矛盾；③ 最关键的是，它完全忽略了视频中局部区域的细粒度质量差异——同一视频的不同空间位置、不同帧之间，其生成质量往往存在显著波动（图 2），而全局评分无法捕捉这些局部退化。

**核心方法**：本文提出 **LocalDPO**，一种面向视频扩散模型的直接局部细节偏好优化框架。其核心思路是以高质量真实视频为锚点，通过随机时空掩码对真实视频进行局部破坏，再利用冻结的预训练模型仅修复被破坏区域，从而在单次推理内获得“正样本（真实视频）—负样本（局部退化视频）”的偏好对。在此基础上，引入掩码引导的**区域感知 DPO 损失**，将偏好优化严格限制在损坏区域，驱动模型聚焦于局部生成细节的改善，同时通过混合全局 DPO 和 SFT 损失保持整体结构稳定性。

**方法定位**：LocalDPO 属于视频扩散模型的后训练（post-training）偏好对齐方法。与依赖多采样排序的 **Vanilla DPO**（Liu et al., NeurIPS 2025）和以帧为粒度的 **DenseDPO**（Wu et al., NeurIPS 2025）相比，LocalDPO 的创新在于将偏好信号的构造从“全局采样—排序”转变为“真实视频锚定—局部破坏”，并将优化目标从全局潜变量重建误差差升级为掩码归一化的区域重建误差差。

**主要结果**：在 CogVideoX-2B、CogVideoX-5B 和 Wan2.1-1.3B 三个基座模型上，LocalDPO 在 VBench 和 VideoJAM 基准的审美质量、成像质量及 VideoAlign 总分上一致超越 Baseline、SFT、Vanilla DPO 和 DenseDPO（表 1、表 2）。消融实验证实，区域感知 DPO 损失是性能提升的关键驱动因素（表 3），而“真实视频 + 区域感知破坏”的偏好对构造策略显著优于其他替代方案（表 4）。人类评估中，LocalDPO 在所有维度上均取得最高胜率（图 4、图 7）。

## 背景与动机

### 视频扩散模型的后训练瓶颈

大规模视频扩散模型（VDM）在文本到视频生成任务中取得了显著进展，但预训练模型生成的视频在局部区域仍频繁出现目标闪烁、纹理缺失、细节模糊等细粒度质量问题。为弥补这一缺陷，现有后训练方法通常采用偏好对齐策略：对同一提示多次采样生成多个视频，借助评判模型或人工标注进行全局质量排序，再通过扩散DPO（Direct Preference Optimization）损失驱动模型向“胜出”样本靠拢（**Vanilla DPO**, Liu et al., NeurIPS 2025）。然而，这一范式存在三个关键瓶颈：

1. **标注成本高昂**：多轮采样与评判模型推理消耗大量计算资源，人工标注则进一步推高成本。
2. **全局偏好信号模糊甚至矛盾**：同一提示下不同种子的视频在全局层面可能各有优劣，但在局部区域（如人物面部、物体纹理）的质量差异显著，且这种局部优劣关系可能随帧变化而反转（见 Figure 2）。全局排序无法捕捉这些细粒度、区域级的偏好差异，导致优化信号被稀释或误导。
3. **局部退化被忽略**：现有方法以整帧或整个视频为单位计算偏好损失，模型难以聚焦于真正需要改善的局部区域，尤其当全局结构已较为合理时，局部细节的退化往往被全局损失平均化。

### 从全局偏好到区域感知偏好

Figure 2 揭示了问题的本质：同一提示生成的两个视频，在全局审美上可能难分高下，但在特定时空区域（如人物手部、背景纹理）存在明显质量差异，且这种差异在不同帧之间并不一致。这意味着，**真正影响人类偏好判断的往往是局部细节的生成质量**，而非全局平均质量。然而，Vanilla DPO 和以帧为粒度的 **DenseDPO**（Wu et al., NeurIPS 2025）均无法针对这些区域级退化提供精准的优化信号。

### 核心洞察与本文动机

本文提出一个关键洞察：**以真实视频为锚点，利用模型自身生成能力构造局部退化的对比对，可在零标注成本下获得高置信度、区域级的偏好信号**。具体而言，真实视频天然具备高质量的局部细节，只需在其上引入可控的局部破坏，即可自动生成“正样本（原始真实视频）vs. 负样本（局部退化版本）”的偏好对，无需任何外部评判模型或人工干预。基于此，本文设计了 **LocalDPO** 框架，通过掩码引导的区域感知 DPO 损失，将偏好优化严格限制在损坏区域，从而直接驱动模型学习局部细节偏好，同时避免全局结构漂移。

## 核心创新

LocalDPO 的核心创新在于**以真实视频为锚点，将视频扩散模型的偏好优化从全局、模糊的信号精确地聚焦到局部、细粒度的生成细节上**。这一转变通过两个紧密耦合的“changed slots”实现，直击现有方法的瓶颈。

### 瓶颈分析：全局偏好信号的局限

现有视频扩散模型的偏好优化方法（如 Vanilla DPO、DenseDPO）存在两个根本性缺陷：

1.  **高昂的标注成本与模糊的信号**：它们依赖对同一提示进行多轮采样，再由评判模型或人工对生成视频进行全局排序来构建偏好对。这不仅计算开销巨大，更关键的是，全局评分可能模糊甚至矛盾——一个视频可能在主体运动上胜出，却在局部纹理上落败，而全局信号无法捕捉这种细粒度的偏好差异（见 Figure 2 的动机说明）。
2.  **对局部退化的忽视**：视频生成中常见的瑕疵，如目标闪烁、细节丢失、纹理失真，往往发生在局部时空区域。全局偏好优化无法针对性地修正这些区域级退化，导致模型缺乏对局部细节的精细控制。

### 创新一：零成本、区域级的偏好对构造

LocalDPO 彻底改变了偏好对的构造范式，从“多采样-全局排序”转变为“单样本-局部破坏”。其核心机制是**以真实视频为锚点的局部退化生成**，流程如下（见 Figure 3）：

1.  **正样本**：直接使用高质量的真实视频作为正样本（win sample），无需生成。
2.  **负样本构造**：对正样本视频进行局部破坏以生成负样本（lose sample）。具体步骤为：
    -   **生成3D时空掩码**：通过在视频帧上随机绘制贝塞尔曲线形成不规则闭合形状，并将其沿时间轴广播，生成一个时空二值掩码 $M$。此掩码定义了需要进行局部退化的区域。
    -   **局部修复与潜变量融合**：首先向真实视频的潜变量添加一定程度的噪声。然后，利用冻结的预训练视频扩散模型进行逐步去噪。关键在于，在每一步去噪后，通过一个区域感知的潜变量融合机制来维持掩码外区域的原始内容不变：
        $$\mathbf{z}_{t-1} = \mathbf{M} \odot \hat{\mathbf{z}}_{t-1} + (1 - \mathbf{M}) \odot \mathbf{z}_{t-1}^{\mathrm{orig}}$$
        其中，$\hat{\mathbf{z}}_{t-1}$ 是去噪后的潜变量，$\mathbf{z}_{t-1}^{\mathrm{orig}}$ 是重新加噪至对应时间步的原始视频潜变量。该操作确保了模型仅在掩码 $M$ 指示的区域内进行“修复”，而背景区域被完美保留。由于预训练模型的修复能力有限，修复区域的视觉质量会低于原始真实视频，从而自然地构成了一个仅在局部区域退化的负样本。

这种构造方式的优势在于：**单次推理即可获得高置信度的对比对，完全避免了多轮采样、额外评判模型和人工标注的成本与歧义**。

### 创新二：掩码引导的区域感知偏好优化

拥有了区域级的偏好对后，LocalDPO 进一步设计了与之匹配的优化目标，确保模型的学习严格聚焦于局部退化区域，避免全局结构漂移。

1.  **区域感知的DPO损失 ($\mathcal{L}_{\mathrm{RA-DPO}}$)**：该损失是核心驱动。它修改了标准扩散DPO损失，使其仅在掩码 $M$ 指示的区域内计算正负样本的重建误差改进量 $\Delta'$：
    $$\Delta_*' = \frac{N_M}{\|\mathbf{M}\|_1} \left( \| \mathbf{M} \odot (\mathbf{y}^* - f_{\theta}(\mathbf{z}_t^*, t, \mathbf{c})) \|^2 - \| \mathbf{M} \odot (\mathbf{y}^* - f_{\widetilde{\theta}}(\mathbf{z}_t^*, t, \mathbf{c})) \|^2 \right)$$
    其中 $f_{\theta}$ 和 $f_{\widetilde{\theta}}$ 分别为当前模型和参考模型。该公式通过 $\mathbf{M} \odot$ 运算将误差计算限制在损坏区域，并通过 $\|\mathbf{M}\|_1$ 进行归一化，使得损失对不同大小的掩码区域不敏感。
    最终的 $\mathcal{L}_{\mathrm{RA-DPO}}$ 损失形式为：
    $$\mathcal{L}_{\mathrm{RA-DPO}} = -\mathbb{E}_{d \sim \hat{\mathcal{D}}} \left[ \log \sigma \left( -\beta \cdot (1 + \eta(\alpha)) \cdot \mathbb{E}_t [\Delta_w' - \Delta_l'] \right) \right]$$
    其中，$(1 + \eta(\alpha))$ 是一个基于噪声水平 $\alpha$ 的动态惩罚因子。当破坏程度高（$\alpha$ 大）时，惩罚力度更强，引导模型更关注修复明显的退化区域。

2.  **混合训练目标**：为防止模型过度聚焦于局部修复而丧失全局生成能力，LocalDPO 采用了一个混合损失函数进行训练：
    $$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{RA-DPO}} \mathcal{L}_{\mathrm{RA-DPO}} + \lambda_{\mathrm{DPO}} \mathcal{L}_{\mathrm{DPO}} + \lambda_{\mathrm{SFT}} \mathcal{L}_{\mathrm{SFT}}$$
    其中，$\mathcal{L}_{\mathrm{DPO}}$ 是标准的全局DPO损失，用于维持整体偏好对齐；$\mathcal{L}_{\mathrm{SFT}}$ 是监督微调损失，用于稳定训练并保留基座模型的先验知识。实验设定权重为 $\lambda_{\mathrm{RA-DPO}}=1.0, \lambda_{\mathrm{DPO}}=1.0, \lambda_{\mathrm{SFT}}=0.1$。

### 消融实验验证

消融实验（Table 3）有力地证明了上述两个创新的关键作用。当在训练中加入 $\mathcal{L}_{\mathrm{RA-DPO}}$ 后，模型在审美质量、成像质量等几乎所有指标上均获得显著提升。此外，Table 4 的消融研究表明，采用“真实视频 + 区域感知破坏”的偏好对构造策略，其效果远超使用Vanilla DPO的全局win/lose样本或以生成视频作为正样本的策略，证实了以真实视频为锚点的局部退化构造是获得高质量偏好信号的核心。

## 整体框架

LocalDPO 的整体框架围绕一个核心洞察展开：**以真实视频为锚点，利用模型自身的生成能力构造局部退化的对比对，从而在零标注成本下获得高置信度、区域级的偏好信号**。该框架包含三个紧密耦合的模块，形成一条从偏好数据构造到区域感知优化的完整链路。

### 数据流与模块关系

如图 3 所示，整个 pipeline 的输入为高质量真实视频 $\mathbf{x}^w$ 及其对应的文本提示 $\mathbf{c}$，输出为经过区域偏好优化的扩散模型。数据依次流经以下三个核心模块：

1.  **3D 掩码生成**：在视频空间中随机生成不规则的时空二值掩码 $\mathbf{M}$，用于指定后续需要破坏的局部区域。
2.  **时空局部破坏**：以真实视频为正样本，在掩码区域内通过“加噪-去噪”过程生成局部退化的负样本 $\mathbf{x}^l$，同时利用区域感知潜变量融合保持背景区域不变。
3.  **区域感知偏好优化**：基于构造的偏好对 $(\mathbf{c}, \mathbf{x}^w, \mathbf{x}^l, \mathbf{M})$，计算仅作用于掩码区域的重建误差改进量，并通过混合损失函数驱动模型学习局部细节偏好。

### 模块一：3D 掩码生成

该模块负责在视频中定义待优化的局部区域。具体而言，算法在空间域随机生成若干条贝塞尔曲线，并确保这些曲线构成闭合形状；闭合形状的内部区域即为破坏目标。随后，该空间掩码沿时间轴广播，形成覆盖特定时空范围的 3D 二值掩码 $\mathbf{M}$。这种基于随机贝塞尔曲线的策略无需语义先验，计算代价极低，且能产生多样化的不规则区域，避免模型过拟合到固定掩码模式。

### 模块二：时空局部破坏

给定真实视频 $\mathbf{x}^w$ 和掩码 $\mathbf{M}$，本模块的目标是生成仅在掩码区域内存在质量退化的负样本 $\mathbf{x}^l$。核心流程如下：

1.  向真实视频的潜变量 $\mathbf{z}^{\text{orig}}$ 添加受控噪声，达到预设的噪声水平 $\alpha$。
2.  在掩码区域内逐步去噪，得到重建潜变量 $\hat{\mathbf{z}}_{t-1}$。
3.  在每一步去噪中，通过区域感知潜变量融合将掩码内外的潜变量进行组合：
    $$\mathbf{z}_{t-1} = \mathbf{M} \odot \hat{\mathbf{z}}_{t-1} + (1 - \mathbf{M}) \odot \mathbf{z}_{t-1}^{\text{orig}}$$
    其中 $\mathbf{z}_{t-1}^{\text{orig}}$ 是原始潜变量在对应噪声水平下的重加噪版本。这一融合机制确保了掩码区域外的原始内容得以完整保留，避免了分布不匹配问题。

由于负样本由预训练模型自身修复生成，其退化模式与模型的能力边界高度一致，因此偏好信号具有高置信度。整个过程仅需单次推理，无需多轮采样或外部评判模型。

### 模块三：区域感知偏好优化

获得偏好对后，LocalDPO 通过区域感知 DPO 损失 $\mathcal{L}_{\mathrm{RA-DPO}}$ 驱动模型学习局部细节偏好。该损失的核心改进在于：仅计算掩码 $\mathbf{M}$ 指示区域内的重建误差改进量，并进行掩码面积归一化：
$$\Delta_*' = \frac{N_M}{\|\mathbf{M}\|_1} \left( \| \mathbf{M} \odot (\mathbf{y}^* - f_{\theta}(\mathbf{z}_t^*, t, \mathbf{c})) \|^2 - \| \mathbf{M} \odot (\mathbf{y}^* - f_{\widetilde{\theta}}(\mathbf{z}_t^*, t, \mathbf{c})) \|^2 \right)$$
其中 $f_{\theta}$ 为当前模型，$f_{\widetilde{\theta}}$ 为冻结的参考模型。此外，损失函数引入噪声水平相关的权重因子 $(1 + \eta(\alpha))$，对高噪声水平下的重建误差施以更强惩罚，引导模型更关注严重退化区域的修复。

为防止模型在局部优化中丧失全局生成能力，最终训练目标采用混合损失：
$$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{RA-DPO}} \mathcal{L}_{\mathrm{RA-DPO}} + \lambda_{\mathrm{DPO}} \mathcal{L}_{\mathrm{DPO}} + \lambda_{\mathrm{SFT}} \mathcal{L}_{\mathrm{SFT}}$$
其中全局 DPO 损失 $\mathcal{L}_{\mathrm{DPO}}$ 维持整体偏好对齐，SFT 损失 $\mathcal{L}_{\mathrm{SFT}}$ 防止模型偏离真实视频分布。权重配置为 $\lambda_{\mathrm{RA-DPO}}=1.0$，$\lambda_{\mathrm{DPO}}=1.0$，$\lambda_{\mathrm{SFT}}=0.1$。

### 与基线方法的本质区别

与 Vanilla DPO（**Jie Liu et al., NeurIPS 2025**）和 DenseDPO（**Ziyi Wu et al., NeurIPS 2025**）相比，LocalDPO 在偏好对构造和优化目标两个维度上实现了根本性转变：

-   **偏好对构造**：基线方法依赖对同一提示生成多个视频并进行全局排序，标注成本高且偏好信号粗糙；LocalDPO 以真实视频为正样本，通过局部破坏生成负样本，单次推理即可完成构造，且偏好信号天然定位于局部区域。
-   **优化目标**：基线方法使用全局 DPO 损失，可能因全局信号的模糊性（如不同区域质量此消彼长）导致优化矛盾；LocalDPO 的掩码引导区域感知损失将优化严格限制在损坏区域，避免了全局结构漂移，实现了对局部生成细节的精准驱动。

## 核心模块与公式推导

LocalDPO 的核心设计围绕三个递进模块展开：**偏好对构造**、**区域感知优化目标** 和 **混合训练策略**。其根本逻辑是：以真实视频为锚点，利用预训练模型自身的生成能力在局部区域制造退化，进而通过掩码引导的 DPO 损失将偏好信号精确注入退化区域。

### 局部破坏式偏好对构造

传统视频 DPO 依赖对同一提示多次采样、再由评判模型进行全局排序，成本高且偏好信号粗糙。LocalDPO 将正样本固定为高质量真实视频 $\mathbf{x}^w$，负样本 $\mathbf{x}^l$ 则通过对 $\mathbf{x}^w$ 进行**时空局部破坏**获得，形成区域感知的偏好元组 $(\mathbf{c}, \mathbf{x}^w, \mathbf{x}^l, \mathbf{M})$。

构造过程分为两步：

**3D 掩码生成**：在视频空间域上，基于贝塞尔曲线随机生成不规则闭合形状，并将其沿时间轴广播，形成时空二值掩码 $\mathbf{M}$。掩码内部即为待破坏区域。

**时空局部破坏**：给定真实视频的潜变量 $\mathbf{z}^{\text{orig}}$，先添加受控噪声至噪声水平 $\alpha$，然后在掩码区域内逐步去噪。为保证区域内外潜变量分布一致，每一步去噪后执行**区域感知潜变量融合**：

$$ \mathbf{z}_{t-1} = \mathbf{M} \odot \hat{\mathbf{z}}_{t-1} + (1 - \mathbf{M}) \odot \mathbf{z}_{t-1}^{\text{orig}} \tag{3} $$

其中 $\hat{\mathbf{z}}_{t-1}$ 为去噪后的潜变量，$\mathbf{z}_{t-1}^{\text{orig}}$ 为原始视频在当前时间步重加噪后的潜变量。该融合确保掩码区域外保持原始内容不变，仅掩码内产生局部退化。整个过程仅需单次推理，无需额外评判模型或人工标注。

### 区域感知偏好优化

标准扩散 DPO 损失基于全局潜变量计算重建误差差，无法区分退化的空间位置。LocalDPO 引入**区域感知 DPO 损失**，将优化严格限制在掩码区域内。

首先定义区域感知的重建误差改进量 $\Delta'_*$，仅计算掩码 $\mathbf{M}$ 内的重建误差差，并按掩码面积归一化：

$$ \Delta'_* = \frac{N_M}{\|\mathbf{M}\|_1} \left( \| \mathbf{M} \odot (\mathbf{y}^* - f_{\theta}(\mathbf{z}_t^*, t, \mathbf{c})) \|^2 - \| \mathbf{M} \odot (\mathbf{y}^* - f_{\widetilde{\theta}}(\mathbf{z}_t^*, t, \mathbf{c})) \|^2 \right) \tag{5} $$

其中 $f_{\theta}$ 为当前模型，$f_{\widetilde{\theta}}$ 为参考模型（冻结的预训练基座），$\mathbf{y}^*$ 为目标噪声，$N_M$ 为视频总像素数，$\|\mathbf{M}\|_1$ 为掩码区域像素数。归一化使得不同大小的掩码区域对损失的贡献可比。

在此基础上，区域感知 DPO 损失定义为：

$$ \mathcal{L}_{\mathrm{RA-DPO}} = -\mathbb{E}_{d \sim \hat{\mathcal{D}}} \left[ \log \sigma \left( -\beta \cdot (1 + \eta(\alpha)) \cdot \mathbb{E}_t [\Delta'_w - \Delta'_l] \right) \right] \tag{4} $$

关键设计在于**噪声水平自适应惩罚因子** $(1 + \eta(\alpha))$：当局部破坏的噪声水平 $\alpha$ 较高时，退化更严重，正负样本差异更大，应施加更强的偏好惩罚；$\eta(\alpha)$ 将 $\alpha$ 线性归一化至 $[0,1]$，使损失强度与退化程度自适应匹配。

### 混合训练目标

仅使用区域感知 DPO 损失可能导致模型过度聚焦局部而忽略全局结构。为此，LocalDPO 采用混合训练目标：

$$ \mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{RA-DPO}} \mathcal{L}_{\mathrm{RA-DPO}} + \lambda_{\mathrm{DPO}} \mathcal{L}_{\mathrm{DPO}} + \lambda_{\mathrm{SFT}} \mathcal{L}_{\mathrm{SFT}} \tag{6} $$

其中 $\mathcal{L}_{\mathrm{DPO}}$ 为标准全局 DPO 损失（式 (1)），维持整体生成质量；$\mathcal{L}_{\mathrm{SFT}}$ 为在 63K 高质量真实视频上的有监督微调损失，防止训练不稳定和过拟合。权重配置为 $\lambda_{\mathrm{RA-DPO}}=1.0$，$\lambda_{\mathrm{DPO}}=1.0$，$\lambda_{\mathrm{SFT}}=0.1$。消融实验（Table 3）证实，引入区域感知 DPO 损失后几乎所有质量指标均显著提升，而 SFT 和全局 DPO 损失的辅助作用则体现在训练稳定性和全局结构保持上。

### 补充图表

![[assets/figures/papers/paper_list_l2693_https_arxiv_org_abs_2601_04068/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of video pairs generated by CogVideoX-5B from the same prompt but different seeds reveals significant discrepancies in the visual quality of localized regions, with their relative quality varying across frames. These fine-grained, localized preference patterns are overlooked by the vanilla DPO annotation paradigm, motivating our LocalDPO approach*

![[assets/figures/papers/paper_list_l2693_https_arxiv_org_abs_2601_04068/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline of locally corrupted videos generation. We first randomly sample several Bezier curves on the original video and ´ ensure that these curves form closed shapes. The interior of each closed shape defines the region to be corrupted in subsequent steps. Then, the masked area of real video is inpainted by the pretrained VDM. Specifically, given the latent of input real video, the model first adds a controlled amount of noise to its latent representation and then denoises it step by step. During each denoising step, the original video latent is re-noised at the noise level corresponding to the next timestep and then fused with the denoised latent via a latent fusion mechanism by*

![[assets/figures/papers/paper_list_l2693_https_arxiv_org_abs_2601_04068/figures/014_Figure_9.jpg]]
*Figure 9: Visualization of generated locally corrupted videos*

## 实验与分析

### 主实验设置

为公平比较，所有方法（SFT、Vanilla DPO、DenseDPO 及 LocalDPO）均采用相同的 LoRA 配置（rank=64，仅微调 DiT 的注意力层）、相同的训练数据量（63K）和优化协议。Vanilla DPO 和 DenseDPO 的偏好排序均使用同一评判模型。实验覆盖三个基座模型：CogVideoX-2B、CogVideoX-5B 和 Wan2.1-1.3B，评估基准包括 VBench（审美质量与成像质量维度）、VideoJAM 以及人类偏好评估。

### 主实验结果

在 VBench 和 VideoJAM 两个基准上，LocalDPO 在审美质量、成像质量和 VideoAlign 总分上均一致地取得最优或次优结果，显著超越 Baseline（未微调）、SFT、Vanilla DPO 和 DenseDPO。

**VBench 基准**（Table 1）：以 CogVideoX-2B 为例，LocalDPO 的审美质量达到 0.6499，成像质量达到 0.7080，VideoAlign 总分为 7.8568。相比 Baseline，审美质量提升 0.022，成像质量提升 0.0491。在 CogVideoX-5B 上，审美质量为 0.6274，成像质量为 0.7107，VideoAlign 总分高达 10.2930。Wan2.1-1.3B 上审美质量与成像质量分别为 0.6416 和 0.6412，VideoAlign 总分 7.9588，同样保持领先。

**VideoJAM 基准**（Table 2）：在 CogVideoX-2B 上，LocalDPO 的成像质量达到 0.7001，相比 Baseline 提升 0.0674，审美质量 0.5604，VideoAlign 总分 7.5397。CogVideoX-5B 上审美质量 0.5782、成像质量 0.6727、VideoAlign 总分 7.6424；Wan2.1-1.3B 上分别为 0.5698、0.6467 和 7.4849。跨模型、跨基准的稳定优势表明 LocalDPO 的局部偏好优化策略具有良好的泛化性。

**人类评估**（Figure 4, Figure 7）：在通用维度上，LocalDPO 对 Vanilla DPO 的平均胜率达到 88.86%（直接胜出 33.4%，平局 58.7%）。在更细粒度的维度比较中（Figure 7），LocalDPO 对 Baseline、SFT 和 Vanilla DPO 在所有评估维度上均取得最佳结果，覆盖 CogVideoX-2B/5B 和 Wan2.1-1.3B 三个基座。

### 消融实验

**损失组件消融**（Table 3）：逐步引入区域感知 DPO 损失（$\mathcal{L}_{\mathrm{RA-DPO}}$）后，几乎所有指标均显著提升。仅使用全局 DPO 损失或 SFT 损失时，审美质量与成像质量明显低于加入 $\mathcal{L}_{\mathrm{RA-DPO}}$ 的配置。这验证了掩码引导的区域级偏好信号是性能提升的核心驱动因素，而非单纯增加训练数据或全局对齐。

**正负样本构造策略消融**（Table 4）：比较了四种构造策略——（1）使用 Vanilla DPO 的 win/lose 样本；（2）生成视频作为正样本 + 区域感知破坏负样本；（3）真实视频作为正样本 + Vanilla lose 负样本；（4）真实视频 + 区域感知破坏（LocalDPO 方案）。结果表明，方案（4）在审美质量和成像质量上均取得最高分。这证明了两个关键设计选择的有效性：以真实视频为锚点提供高保真正样本，以及通过局部破坏构造区域级退化负样本以提供精准的对比信号。

### 定性分析

Figure 5 和 Figure 10-12 展示了 LocalDPO 与 SFT、Vanilla DPO 在三个基座上的定性对比。LocalDPO 生成的视频展现出更丰富的纹理细节、更合理的运动、更高的美学质量和更少的伪影。相比之下，SFT 和 Vanilla DPO 在局部区域常出现细节丢失、纹理模糊或不自然的运动模式。这与 LocalDPO 的优化机制一致——通过在局部退化区域施加精确的偏好压力，模型学会了修复这些细粒度缺陷，同时保留全局结构的完整性。

![[assets/figures/papers/paper_list_l2693_https_arxiv_org_abs_2601_04068/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative Comparison between SFT, Vanilla DPO and LocalDPO for CogVideoX models. Our LocalDPO generates rich textural details, plausible motion, higher aesthetic and fewer artifacts*

### 训练动态

Figure 6 展示了不同训练迭代次数下审美质量和成像质量的收敛曲线。引入区域感知 DPO 损失后，模型在较少的迭代步数内即可达到更高的质量水平，且收敛更加稳定。这表明局部偏好信号不仅有效，而且提供了更高效的梯度方向，避免了全局 DPO 中可能出现的信号矛盾或优化震荡。

![[assets/figures/papers/paper_list_l2693_https_arxiv_org_abs_2601_04068/figures/010_Figure_6.jpg]]
*Figure 6: Convergence of the models on aesthetic and image quality under different training iterations*

### 失败模式与局限性

尽管 LocalDPO 在多项指标上表现优异，仍存在以下局限：

1. **掩码缺乏语义引导**：当前 3D 掩码基于随机贝塞尔曲线生成，未考虑视频中的语义对象分布。退化区域可能与关键语义对象不完全对齐，导致优化信号无法精准作用于最需要改善的局部细节。论文指出可引入视觉基础模型（如 Grounding DINO 和 SAM）来指导掩码放置。

2. **噪声水平需手动设定**：局部破坏的强度由噪声水平范围 $\alpha_l$ 和 $\alpha_h$ 控制，需针对不同内容和模型手动调整。过小的噪声水平可能导致退化不足、偏好信号过弱；过大则可能破坏过多内容，超出模型修复能力。自适应噪声水平策略是未来的改进方向。

3. **架构覆盖有限**：实验仅覆盖了 DiT 架构的 VDM（CogVideoX 系列和 Wan2.1），未在非 DiT 或更小规模模型上验证。方法的通用性边界尚待进一步探索。

4. **负样本生成的计算开销**：虽然 LocalDPO 仅需单次推理即可构造偏好对（相比 Vanilla DPO 的多轮采样大幅降低开销），但负样本生成仍依赖预训练模型的一次完整去噪过程。对于极长视频，这一步骤的计算成本仍不可忽略。

### 数据统计

Table 5 展示了训练数据的关键属性统计，Figure 8 给出了视频类别分布，Figure 9 可视化了生成的局部破坏视频示例。数据覆盖多样化的场景类别，局部破坏在视觉上表现为掩码区域内的纹理退化、细节丢失或轻微模糊，而背景区域保持真实视频的高质量，形成了清晰的区域级对比对。

![[assets/figures/papers/paper_list_l2693_https_arxiv_org_abs_2601_04068/figures/012_Table_5.jpg]]
*Table 5: Statistics of the curated data on key attributes*

### 补充图表

![[assets/figures/papers/paper_list_l2693_https_arxiv_org_abs_2601_04068/figures/004_Figure_4.jpg]]
*Figure 4: Human evaluation of LocalDPO vs. SFT and VanillaDPO. LocalDPO achieves the best results on all dimensions of human evaluation*

![[assets/figures/papers/paper_list_l2693_https_arxiv_org_abs_2601_04068/figures/005_Table_1.jpg]]
*Table 1: Quantitative Comparison on Vbench prompts from aesthetic and imaging quality dimensions. The best result is highlighted in bold and the second-best is underlined*

![[assets/figures/papers/paper_list_l2693_https_arxiv_org_abs_2601_04068/figures/006_Table_2.jpg]]
*Table 2: Quantitative Comparison on VideoJAM benchmark. The best result is highlighted in bold and the second-best is underlined*

![[assets/figures/papers/paper_list_l2693_https_arxiv_org_abs_2601_04068/figures/007_Table_3.jpg]]
*Table 3: Ablation on loss components. ✓indicates the used loss*

![[assets/figures/papers/paper_list_l2693_https_arxiv_org_abs_2601_04068/figures/008_Table_4.jpg]]
*Table 4: Ablation on positive and negative sample construction strategies. “Vanilla win” and “Vanilla lose” indicate the win and lose sample used in vanilla DPO. “RA corruption” represents the region-aware corruption in our method*

![[assets/figures/papers/paper_list_l2693_https_arxiv_org_abs_2601_04068/figures/011_Figure_7.jpg]]
*Figure 7: Human evaluation of LocalDPO vs. Baseline, SFT and Vanilla DPO on CogvideoX-2B [71], CogvideoX-5B [71] and Wan2.1- 1.3B [55]. LocalDPO achieves the best results on all dimensions of human evaluation*

## 方法谱系与知识库定位

### 1. 与现有方法的谱系关系

LocalDPO 位于视频生成模型后训练（post-training）中偏好对齐方法的分支上，其直接对话对象是扩散 DPO 家族，但通过构造范式和优化目标的协同改造，形成了独特的定位。

**上游继承：扩散 DPO 框架。** 方法直接继承扩散模型偏好优化的数学形式。标准扩散 DPO 损失（**Diffusion-DPO**，Liu et al., NeurIPS 2025）通过比较 win/lose 样本在潜空间上的重建误差差异来驱动偏好对齐：

$$ \mathcal{L}_{\mathrm{DPO}} = -\mathbb{E}_{(\mathbf{c}, \mathbf{z}^w, \mathbf{z}^l) \sim \mathcal{D}} \left[ \log \sigma \left( -\beta \cdot \mathbb{E}_t \left[ \Delta_w - \Delta_l \right] \right) \right] $$

其中 $\Delta(\mathbf{z}^*, t, \mathbf{c}, \mathbf{y}^*) = \| \mathbf{y}^* - f_{\theta}(\mathbf{z}_t^*, t, \mathbf{c}) \|^2 - \| \mathbf{y}^* - f_{\widetilde{\theta}}(\mathbf{z}_t^*, t, \mathbf{c}) \|^2$ 衡量当前模型相对于参考模型的重建误差改进量。LocalDPO 保留了这一核心机制，但将其作用域从全局潜变量收缩至局部掩码区域。

**关键分歧点：偏好对构造范式。** 标准 DPO（包括 Diffusion-DPO 和 **DenseDPO**，Wu et al., NeurIPS 2025）依赖“同一提示 → 多样本生成 → 评判模型/人工排序”的流水线来获取 win/lose 对。该范式存在三重瓶颈：
- **计算开销**：单偏好对需多次完整去噪推理；
- **标注歧义**：全局评分可能掩盖局部区域的矛盾偏好（同一视频中某区域质量高而另一区域差）；
- **信号粒度**：全局偏好信号无法定位到具体时空区域，模型难以学习细粒度改进。

LocalDPO 以“真实视频为锚点 + 局部破坏生成负样本”的策略完全绕开上述瓶颈。这一构造范式的核心洞察是：真实视频天然具备高置信度的正样本属性，而模型自身的局部修复能力可产生可控的退化负样本，两者结合无需任何外部评判模型或人工标注即可获得区域级偏好信号。

**与 DenseDPO 的粒度差异。** DenseDPO 虽然也关注细粒度偏好，但其粒度为帧级别（frame-level），即对同一视频的不同帧进行独立偏好评分。LocalDPO 进一步下沉至时空区域级（spatio-temporal region level），通过 3D 掩码在帧内划定任意形状的局部区域，实现了更精准的退化定位和偏好学习。

### 2. 方法适用边界

**架构适用性。** 当前验证覆盖 DiT（Diffusion Transformer）架构的视频扩散模型，包括 CogVideoX-2B、CogVideoX-5B 和 Wan2.1-1.3B。方法的核心组件（潜变量融合、掩码引导损失）在原理上不依赖于特定 backbone，但未在 UNet-based 或更小规模 VDM 上验证，跨架构迁移需谨慎评估。

**数据依赖性。** LocalDPO 的训练依赖于高质量真实视频数据集（论文使用 63K 精选视频）。真实视频的质量直接决定了正样本的上限，若数据集中存在伪影或低质量片段，可能削弱偏好信号的置信度。此外，文本-视频配对质量影响条件引导的有效性。

**退化模式的可控性。** 局部破坏强度由噪声水平范围 $[\alpha_l, \alpha_h]$ 控制，需手动设定。过低的噪声水平可能导致退化不明显，偏好信号过弱；过高的噪声水平可能产生非自然的严重伪影，超出“局部退化”的合理范围。该超参数对内容和模型的敏感性尚未系统研究。

**计算开销特征。** 虽然 LocalDPO 将偏好对构造从“多次完整生成”压缩为“单次局部修复”，但负样本生成仍需预训练模型的一次完整去噪过程。对于极长视频（高帧数），单次推理的时间/显存开销仍不可忽略。

### 3. 局限性与开放问题

**掩码生成的语义盲区。** 当前 3D 掩码基于随机贝塞尔曲线生成，完全不考虑视频内容的语义分布。这导致退化区域可能与关键语义对象（人脸、文字、小目标）错位，偏好优化的效果可能集中在背景或非关键区域。一个自然的改进方向是引入视觉基础模型（如 Grounding DINO + SAM）指导掩码放置，使其覆盖语义显著区域，提升偏好学习的有效性。

**噪声水平的自适应需求。** 固定范围的噪声水平忽略了视频内容的异质性——不同场景、不同区域的“可接受退化程度”不同。设计自适应噪声调度策略（例如基于局部纹理复杂度或运动幅度动态调整 $\alpha$）可能进一步提升退化样本的合理性和训练效率。

**权重因子的最优性未验证。** 区域感知 DPO 损失中的惩罚权重因子 $\eta(\alpha)$ 采用线性归一化设计，其最优性缺乏理论或实验支撑。是否存在更优的调度函数（如指数衰减、Sigmoid 型）以更好地匹配不同噪声水平下的偏好信号强度，是一个开放的设计空间。

**规模化训练的泛化瓶颈。** 论文使用 63K 数据进行验证，当真实视频数据量进一步增大时，LocalDPO 是否会因过度聚焦局部细节而损害全局一致性或产生过拟合，尚不明确。混合训练目标中的 $\lambda_{\mathrm{RA-DPO}}$、$\lambda_{\mathrm{DPO}}$、$\lambda_{\mathrm{SFT}}$ 权重可能需要随数据规模动态调整。

**跨模态与跨任务的扩展性。** LocalDPO 的核心思想——“以真实数据为锚点，通过局部破坏构造区域级偏好对”——在原理上可迁移至图像生成、3D 场景生成甚至文本生成任务。但不同模态的“局部破坏”定义和掩码生成策略需要重新设计，目前尚无相关验证。

**评估维度的覆盖缺口。** 现有评估集中在审美质量、成像质量和人类偏好分数，对运动一致性（motion coherence）、物理合理性（physical plausibility）等视频特有关注维度覆盖不足。局部细节的改善是否以牺牲运动平滑性为代价，需要更全面的评估体系来回答。

## 原文 PDF

![[paperPDFs/CVPR_2026/Mind_the_Generative_Details_Direct_Localized_Detail_Preference_Optimization_for_Video_Diffusion_Models.pdf]]