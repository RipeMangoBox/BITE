---
title: "Self-Swap Guidance: Guiding a Diffusion Model by Swapping Its Tokens"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/arxiv_2026/Self_Swap_Guidance_Guiding_a_Diffusion_Model_by_Swapping_Its_Tokens.pdf
aliases:
- SSGS
- SSGGDMBSIT
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过选择性地在空间和通道维度上交换语义最不相似的令牌（token latents），在精细粒度上引入局部扰动，从而控制弱化模型分支的强度，驱动采样远离低质量区域。
primary_logic: 在令牌级别进行选择性交换能以更可控的方式生成弱化模型，相比全局噪声能更精细地平衡扰动与保留，从而在更宽的引导尺度范围内稳定提升保真度。
claims:
- SSG在SDXL无条件生成上FID从119.04降至70.91，IS从9.082升至16.44，大幅领先其他方法。
- SSG在SDXL条件生成上FID从45.09降至21.73，CLIP Score从0.281升至0.313，所有指标均最佳。
- SSG在更宽的引导尺度范围内保持高保真度，而现有方法在低尺度下细节差，高尺度下噪声/过饱和。
- MS-COCO 2014 (无条件生成, SDXL) 上 FID↓ = 70.91
---

# Self-Swap Guidance: Guiding a Diffusion Model by Swapping Its Tokens

> [!tip] 核心洞察
> 在令牌级别进行选择性交换能以更可控的方式生成弱化模型，相比全局噪声能更精细地平衡扰动与保留，从而在更宽的引导尺度范围内稳定提升保真度。

| 字段 | 内容 |
|------|------|
| 中文题名 | 自交换引导：通过交换令牌引导扩散模型 |
| 英文题名 | Self-Swap Guidance: Guiding a Diffusion Model by Swapping Its Tokens |
| 会议/期刊 | CVPR 2026 (Oral) |
| Links | [paper](https://arxiv.org/abs/2604.08048) · [Code](https://github.com/VISION-SJTU/SSG) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Self-Swap Guidance (SSG) |
| Dataset | MS-COCO 2014, ImageNet, MS-COCO 2017 |

> [!tip] 效果简介
> - MS-COCO 2014 (无条件生成, SDXL) 上，FID↓ 70.91 vs 119.04 (w/o guidance) (-48.13)。
> - ImageNet (无条件生成, SD1.5) 上，FID↓ 63.05 vs 74.11 (w/o guidance) (-11.06)。
> - MS-COCO 2014 (条件生成, SDXL) 上，FID↓ 21.73 vs 45.09 (w/o guidance) (-23.36)。

## 概述

扩散模型已成为视觉生成的主流范式，但现有无条件引导方法——如 **SAG** (Hong et al., ICCV 2023)、**SEG** (Hong, NeurIPS 2024) 和 **PAG** (Ahn et al., ECCV 2024)——普遍采用全局且不加区分的扰动策略（对输入图像或注意力图注入高斯噪声）。这类粗粒度扰动忽视了网络不同层和不同时间步中表征的多样性：扰动过弱则细节提升有限，过强则引入噪声、过饱和与过度简化，导致引导尺度（guidance scale）的有效适用范围狭窄。

本文提出 **Self-Swap Guidance (SSG)**，核心思想是将扰动从全局噪声注入转变为**令牌级别的选择性交换**。具体而言，SSG 在扩散模型中间表征空间内，沿空间维度和通道维度分别计算令牌（token latents）之间的语义相似度，并选择性地交换语义最不相似的令牌对。这一操作以精细粒度局部破坏模型表征，生成一个可控的“弱化”预测分支，进而通过外推原始预测与弱化预测的差值实现无条件引导。该方法无需重新训练或修改模型架构，作为即插即用的推理时插件直接集成到标准扩散流程中。

实验表明，SSG 在更宽的引导尺度范围内稳定提升生成保真度。在 SDXL 无条件生成任务上，SSG 将 FID 从 119.04 降至 70.91，IS 从 9.082 提升至 16.44（Table 1）；在条件生成任务上，FID 从 45.09 降至 21.73，CLIP Score 从 0.281 提升至 0.313（Table 3），所有指标均显著优于现有方法。此外，SSG 与 Classifier-Free Guidance (CFG) 兼容，联合使用可进一步改善图像质量与提示对齐。

## 背景与动机

扩散模型已成为视觉生成领域的核心范式，其采样过程可被统一描述为从噪声分布逐步去噪的随机微分方程（SDE）。前向过程由 $d x = - \frac { \beta ( t ) } { 2 } x d t + \sqrt { \beta ( t ) } d w$ 定义，反向采样则依赖分数函数 $\nabla_x \log p_t(x)$ 进行迭代去噪。实际应用中，分数网络 $s_\theta(x_t)$ 通过去噪分数匹配目标训练，但受限于模型容量和数据规模，学习到的分数函数在低密度区域往往存在估计偏差，导致生成样本偏离真实数据分布，出现细节模糊、结构失真等问题。

为缓解上述问题，**无分类器引导（CFG）** 通过外推条件预测与无条件预测的差值来增强条件信号，但其依赖条件标签，无法用于无条件生成场景。针对这一局限，近年来涌现出一类**无条件引导方法**，其核心思想是构造一个“弱化模型”作为负参照，利用原始预测与弱化预测的差异进行外推，从而在无外部条件的情况下提升生成保真度。代表性工作包括 **SAG**（Hong et al., ICCV 2023），通过在输入图像上添加高斯噪声来构建弱化分支；**SEG**（Hong, NeurIPS 2024）与 **PAG**（Ahn et al., ECCV 2024）则直接扰动自注意力图以实现类似效果。

然而，这些现有方法存在一个共同的**结构性缺陷**：它们采用全局且不加区分的扰动策略——无论是向输入图像注入高斯噪声，还是均匀扰动整个注意力特征图，都忽视了扩散模型中不同网络层和不同去噪时间步之间表示多样性的差异。这种粗粒度扰动导致一个根本性的两难困境：扰动过弱时，弱化模型与原始模型过于相似，引导信号不足，细节改善有限；扰动过强时，弱化模型崩塌，引导外推产生噪声、过饱和和过简化等伪影。如图1所示，现有方法在较低的引导尺度下细节表现差，而在较高尺度下则出现明显的噪声和过饱和现象，其有效引导尺度范围十分狭窄。

本文的核心动机正是突破这一瓶颈：**能否设计一种更精细、更可控的弱化机制，在令牌级别引入选择性扰动，从而在更宽的引导尺度范围内稳定提升生成保真度？** 这一思路的直觉在于，扩散模型中间层的令牌潜在表示（token latents）承载了丰富的语义信息，通过选择性地破坏其中语义最不相似的令牌对，可以以最小干预实现有效的模型弱化，避免全局扰动带来的过度退化。

## 核心创新

### 瓶颈发现：全局噪声扰动的粒度失配

现有无条件引导方法——包括 **SAG**（Hong et al., ICCV 2023）、**SEG**（Hong, NeurIPS 2024）和 **PAG**（Ahn et al., ECCV 2024）——共享一个根本性局限：它们采用**全局且不加区分的扰动策略**。SAG 在输入图像上添加高斯噪声，SEG 和 PAG 则在注意力图上施加扰动。这种粗粒度扰动忽视了扩散模型中不同网络层和去噪时序上表示多样性的差异，导致一个难以调和的矛盾：扰动过弱时细节改善不足，扰动过强时则引入噪声、过饱和和过简化伪影。其直接后果是这些方法的引导尺度适用范围狭窄，无法在宽参数区间内稳定提升生成质量（见 Figure 1）。

### 核心洞察：令牌级选择性交换

SSG 的核心洞察在于将扰动的控制粒度从全局下推到**令牌（token latent）级别**。扩散 Transformer 的中间表示由空间和通道维度上的令牌特征组成，不同令牌承载着差异化的语义信息。通过**选择性地交换语义最不相似的令牌对**，SSG 在精细粒度上引入局部语义破坏，从而生成一个“弱化”模型分支作为负参照。这种选择性扰动相比全局噪声注入具有两个关键优势：其一，扰动强度可通过交换比率精确控制；其二，由于仅扰动语义差异最大的局部区域，模型的整体结构得以保留，避免了全局扰动带来的过度退化。

### 方法实现：三个关键机制

**1. 对抗性令牌选择。** SSG 首先沿特征维度归一化所有令牌向量，计算令牌对之间的余弦相似度。与直觉相悖的是，SSG 刻意选择相似度**最低**的 N 对令牌进行交换——即语义最不相似的令牌对。消融实验（Table 5）证实，交换不相似令牌在所有指标上均优于随机交换和交换相似令牌，因为后者无法有效破坏局部结构，生成的图像与原始扩散模型输出趋同。

**2. 空间与通道双维度交换。** SSG 在空间维度和通道维度上分别执行令牌交换。空间交换（spatial self-swap）打乱不同空间位置的令牌，通道交换（channel self-swap）则重组同一空间位置的不同通道。消融实验（Table 6）表明，空间交换主要提升美学分数（AES），通道交换改善 PickScore 和 ImageReward，两者联合使用在所有指标上达到最优。

**3. 双分支架构与扰动注入位置。** SSG 在 Transformer 块开始前和残差连接前分别应用令牌交换操作，以最大化破坏效果。原始分支保持完整前向传播产生 $\epsilon_{\mathrm{ori}}$，扰动分支应用令牌交换后产生 $\epsilon_{\mathrm{pert}}$，最终通过外推公式 $\tilde{\epsilon}(x_t) = \epsilon_{\mathrm{ori}}(x_t) + \omega(\epsilon_{\mathrm{ori}}(x_t) - \epsilon_{\mathrm{pert}}(x_t))$ 实现引导。

### 与 baseline 的本质差异

| 维度 | 现有方法（SAG/SEG/PAG） | SSG |
|------|--------------------------|-----|
| 扰动类型 | 加性高斯噪声 | 令牌交换（置换映射） |
| 扰动粒度 | 全局/粗粒度 | 细粒度/逐令牌选择性 |
| 扰动维度 | 单一（输入或注意力图） | 空间与通道联合 |
| 控制精度 | 仅噪声尺度 | 交换比率 + 引导尺度双参数 |
| 适用范围 | 引导尺度窄 | 引导尺度宽（Figure 1） |

### 兼容性设计

SSG 作为即插即用的推理时方法，无需额外训练或修改模型架构。在条件生成场景下，SSG 与 Classifier-Free Guidance（CFG）完全兼容，可联合使用以在保真度、多样性和提示对齐之间取得更优权衡（Table 7 显示联合使用将 FID 从 31.41 进一步降至 30.82，CLIP Score 升至 0.319）。

## 整体框架

Self-Swap Guidance（SSG）是一种推理时即插即用的无条件引导方法，无需额外训练或修改模型架构。其核心思路是：在扩散模型的前向传播中维护两个并行分支——**原始分支**（保持未修改，产生 $\epsilon_{\mathrm{ori}}$）和**退化分支**（施加令牌交换扰动，产生 $\epsilon_{\mathrm{pert}}$），然后通过引导外推公式将两者差值作为校正信号，驱动采样远离低质量区域。

### 模块关系与数据流

SSG 的整体 pipeline 由以下关键模块串联构成：

**1. 令牌相似度计算**

在退化分支中，首先沿特征维度对所有令牌向量进行归一化，然后计算令牌对之间的余弦相似度。这一步骤在空间维度和通道维度上分别执行，用于识别语义最不相似的令牌对。

**2. 对抗性令牌交换**

选择相似度最低的 $N$ 对令牌，构造置换映射进行并行交换。交换操作在空间维度和通道维度上联合进行：空间交换打乱不同空间位置的特征，通道交换重组不同通道的语义信息。交换比率 $r$ 直接控制扰动强度——$r$ 越大，被交换的令牌/通道比例越高，退化分支的预测质量越低。

**3. 扰动分支集成**

令牌交换操作被施加在每个 Transformer 块开始前以及残差连接前，以最大化破坏效果。退化分支输出的噪声预测 $\epsilon_{\mathrm{pert}}$ 作为负参照，表征模型在局部语义被破坏后的“弱化”预测。

**4. 引导外推**

利用原始预测与扰动预测的差值进行线性外推，实现无条件引导：

$$\tilde{\epsilon}(x_t) = \epsilon_{\mathrm{ori}}(x_t) + \omega \big( \epsilon_{\mathrm{ori}}(x_t) - \epsilon_{\mathrm{pert}}(x_t) \big)$$

其中 $\omega$ 为引导尺度，控制校正信号的强度。在条件生成场景下，SSG 可与 Classifier-Free Guidance（CFG）联合使用，进一步叠加条件引导信号。

### 与现有方法的本质区别

现有无条件引导方法（如 **SAG**（Hong et al., ICCV 2023）、**SEG**（Hong, NeurIPS 2024）、**PAG**（Ahn et al., ECCV 2024））采用全局且不加区分的扰动策略——在输入图像或注意力图上添加高斯噪声。这种粗粒度扰动忽视了网络层和时序的表示多样性：扰动过弱则细节改善有限，过强则引入噪声、过饱和和过简化，导致引导尺度的有效范围狭窄。

SSG 的关键突破在于将扰动粒度从全局压缩到**令牌级**，并通过**选择性交换语义最不相似的令牌对**实现精细的局部语义破坏。相比全局加噪，这种策略能以更可控的方式生成弱化模型，在更宽的引导尺度范围内稳定提升保真度。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_08048/figures/012_Table_5.jpg]]
*Table 5: Importance of adversarial token swap. Swapping dissimilar tokens achieves the best generation quality overall. Random swap yields slightly worse results and swapping similar tokens perform worst, but they still substantially outperform. Figure 7. Visualising the effect of different token swap policies. Swapping dissimilar tokens further refines local details and global coherence compared to random swap. In contrast, swapping similar tokens leads to poor generation that resembles the vanilla diffusion model’s output*

## 核心模块与公式推导

### 无条件引导的统一外推框架

SSG 建立在无条件引导（condition-free guidance）的通用外推公式之上。给定原始模型预测 $\epsilon_{\mathrm{ori}}(x_t)$ 和一个弱化模型预测 $\epsilon_{\mathrm{pert}}(x_t)$，引导后的噪声估计为：

$$\tilde{\epsilon}(x_t) = \epsilon_{\mathrm{ori}}(x_t) + \omega \big( \epsilon_{\mathrm{ori}}(x_t) - \epsilon_{\mathrm{pert}}(x_t) \big)$$

其中 $\omega$ 为引导尺度，控制外推强度。该公式的核心思想是：弱化模型分支产生低质量预测，原始分支与弱化分支的差值指向高质量区域，沿此方向外推即可驱离低质量采样轨迹。SSG 的创新在于如何构造 $\epsilon_{\mathrm{pert}}$——通过令牌级别的选择性交换，而非全局噪声注入。

### 令牌自交换模块

SSG 的弱化分支通过在 Transformer 块的中间表示空间中对令牌特征进行对抗性交换来引入局部扰动。具体流程如下：

**令牌相似度计算**：首先沿特征维度对所有令牌向量进行归一化，然后计算令牌对之间的余弦相似度。对于空间自交换，计算不同空间位置令牌之间的相似度矩阵；对于通道自交换，计算不同通道令牌之间的相似度矩阵。

**对抗性令牌交换**：选择相似度最低的 $N$ 对令牌，构造置换映射进行成对交换。交换语义最不相似的令牌对能够最大化局部结构的破坏效果——将语义无关的特征强行置换，迫使弱化分支产生显著偏离原始语义的表示。交换比率 $r$ 定义为被交换令牌数占总令牌数的比例，直接控制扰动强度。

**双分支架构**：在前向传播中维护两个并行分支。原始分支不做任何修改，产生 $\epsilon_{\mathrm{ori}}$；弱化分支在每个 Transformer 块开始前和残差连接前应用令牌交换操作，产生 $\epsilon_{\mathrm{pert}}$。交换操作选择在残差连接前施加，是为了最大化扰动在后续层中的传播效应，从而充分弱化模型输出。

### 空间交换与通道交换

SSG 支持两种互补的令牌交换维度：

- **空间自交换（Spatial Self-Swap）**：在空间维度上交换不同位置的令牌。这破坏了图像的空间结构一致性，迫使模型修复被扰乱的空间布局，从而提升全局结构和细节保真度。
- **通道自交换（Channel Self-Swap）**：在通道维度上交换不同通道的令牌。这扰乱了特征的语义组合，迫使模型重建更合理的特征表达，从而改善语义对齐和美学质量。

两种交换联合使用可进一步提升所有指标。消融实验表明，空间交换主要提升 AES 分数，通道交换主要改善 PickScore 和 ImageReward，两者互补地覆盖了保真度与语义对齐的不同方面。

### 与 CFG 的兼容性

SSG 的引导公式与 CFG 自然兼容。在条件生成场景下，可将 SSG 的引导项叠加到 CFG 之上：

$$\tilde{\epsilon}_{\mathrm{combined}}(x_t, y) = \epsilon_{\mathrm{cond}}(x_t, y) + \omega_{\mathrm{cfg}} \big( \epsilon_{\mathrm{cond}}(x_t, y) - \epsilon_{\mathrm{uncond}}(x_t, \emptyset) \big) + \omega_{\mathrm{ssg}} \big( \epsilon_{\mathrm{ori}}(x_t) - \epsilon_{\mathrm{pert}}(x_t) \big)$$

实验表明，联合使用可进一步将 FID 从 31.41 降至 30.82，CLIP Score 升至 0.319，验证了 SSG 提供的局部结构引导与 CFG 提供的语义条件引导是正交且互补的信号。

### 关键设计选择

消融实验揭示了两项关键设计决策的因果作用：

1. **对抗性选择 vs 随机选择**：交换语义最不相似的令牌对显著优于随机交换，而交换相似令牌对效果最差。这验证了“最大化语义破坏”原则——只有充分扰乱局部结构，才能产生有效的负参照信号。
2. **交换位置**：在 Transformer 块开始前和残差连接前施加交换，确保扰动能在注意力计算和残差传播中充分扩散，而非被残差连接绕过。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_08048/figures/009_Figure_5.jpg]]
*Figure 5: Effect of varying guidance scale and swap ratio on image quality and prompt alignment*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_08048/figures/001_Figure_1.jpg]]
*Figure 1: Self-Swap Guidance (SSG) generates higher-fidelity images over a wider range of guidance scale. In contrast, existing methods [1, 18, 19] suffer from poor details at lower guidance scale, or noise, oversaturation, and oversimplified details at higher guidance scale*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_08048/figures/002_Figure_2.jpg]]
*Figure 2: Visualisations of guidance patterns and the iteratively denoised images across different timesteps. The text prompt used is “A loft bed with a dresser underneath it”*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_08048/figures/011_Figure_6.jpg]]
*Figure 6: Visualising the effect of using different swap ratio and guidance scale values on generated images*

## 实验与分析

### 核心瓶颈与设计动机验证

现有无条件引导方法（SAG、SEG、PAG）的根本缺陷在于采用**全局且不加区分的扰动策略**——在输入图像或注意力图上注入高斯噪声，忽视了扩散模型不同层和时序步中表示多样性的差异。这种粗粒度扰动导致一个不可调和的矛盾：扰动过弱则细节提升有限，扰动过强则引入噪声、过饱和和过简化伪影，使得引导尺度 $\omega$ 的有效范围极为狭窄（见 Figure 1）。

SSG 通过**令牌级别的选择性交换**从根本上解决了这一瓶颈：在空间和通道维度上识别并交换语义最不相似的令牌对，在细粒度上引入局部扰动，从而以更可控的方式构建弱化模型分支。这一设计的核心因果机制在于：交换语义差异最大的令牌能最大化对局部结构的破坏效果，同时保留全局语义的完整性，使得外推引导能在更宽的 $\omega$ 范围内稳定提升保真度。

### 无条件生成主结果

Table 1 展示了 SDXL 在 MS-COCO 2014 上的无条件生成结果。SSG 在所有指标上均大幅领先现有方法：

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_08048/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of unconditional image generation by SDXL on MS COCO-2014*

- **FID 从 119.04 降至 70.91**（降幅 48.13），远超 SAG（93.80）、SEG（90.72）和 PAG（85.17）。
- **IS 从 9.082 升至 16.44**，相比第二名 PAG（14.36）仍有显著提升。
- Precision 和 Recall 同步改善（Precision 0.643→0.712，Recall 0.484→0.536），表明 SSG 在提升保真度的同时未牺牲多样性。
- AES 美学评分从 5.460 升至 5.744，验证了视觉质量的实质性提升。

Table 2 在 SD1.5 + ImageNet 上的跨模型验证进一步确认了 SSG 的泛化能力：FID 从 74.11 降至 63.05，IS 从 19.57 升至 22.94，在所有方法中均为最优。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_08048/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison of unconditional image generation by SD1.5 on ImageNet*

### 条件生成主结果

Table 3（MS-COCO 2014）和 Table 4（MS-COCO 2017）展示了 SDXL 条件生成场景下的定量对比。SSG 在六项指标上全面领先：

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_08048/figures/007_Table_3.jpg]]
*Table 3: Quantitative comparison of conditional image generation by SDXL on MS-COCO 2014*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_08048/figures/008_Table_4.jpg]]
*Table 4: Quantitative comparison of conditional image generation by SDXL on MS-COCO 2017*

- **FID 从 45.09 降至 21.73**（MS-COCO 2014），降幅达 23.36，远超 PAG（25.98）和 SEG（28.21）。
- **CLIP Score 从 0.281 升至 0.313**，表明提示对齐能力显著增强。
- IS 从 26.97 升至 34.15，AES 从 5.694 升至 5.890。
- PickScore（22.14）和 ImageReward（0.253）的人类偏好指标同样最优。

值得注意的是，SSG 在条件生成场景下与 CFG 兼容（Table 7），联合使用时 FID 进一步从 31.41 降至 30.82，CLIP Score 升至 0.319，IS 升至 36.37，验证了两种引导机制的互补性。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_08048/figures/015_Table_7.jpg]]
*Table 7: Compatibility of SSG with CFG*

### 消融实验

**对抗性交换策略的关键性**（Table 5 & Figure 7）：对比三种令牌交换策略——交换语义最不相似的令牌（SSG 默认）、随机交换、交换相似令牌——结果表明，交换不相似令牌在所有指标上达到最优（FID 31.41, CLIP 0.313, PickScore 22.18, IR 0.297）。随机交换性能略降但仍大幅优于无引导基准，而交换相似令牌则退化为接近原始扩散模型的低质量生成。这证实了**语义破坏程度与引导效果之间的正相关关系**。

**空间与通道交换的互补性**（Table 6）：单独使用空间交换可提升 AES 美学分数，单独使用通道交换则改善 PickScore 和 ImageReward 等人类偏好指标。两者联合使用在所有指标上均取得进一步提升，表明空间结构破坏和通道语义破坏对图像质量的不同维度具有互补贡献。

**参数鲁棒性**（Figure 5 & Figure 6）：增加交换比率 $r$ 和引导尺度 $\omega$ 能单调改善 FID 和 CLIP Score，且 SSG 对参数变化表现出显著优于 SAG、SEG、PAG 的鲁棒性——在更宽的参数范围内保持高保真度，而对比方法在高尺度下迅速劣化。

### 方法局限与待验证问题

尽管 SSG 在定量和定性评估中均表现优异，以下局限需要在解读结论时注意：

1. **计算开销**：维护双分支前向传播和令牌相似度计算引入额外推理成本，论文未提供与基准方法的推理时间定量对比，该点需要手动验证。
2. **任务泛化性**：当前验证仅限于 SD1.5/SDXL 的图像生成任务，对视频生成、3D 生成等其他模态的可扩展性尚未探索。
3. **架构依赖性**：SSG 的令牌交换操作依赖 Transformer 块的中间表示结构，在非 Transformer 架构（如纯卷积 UNet）或 DiT 等不同设计下的有效性有待验证。
4. **超参数自适应**：$\omega$ 和 $r$ 的最优值依赖人工选择，缺乏自动或自适应的参数确定策略。

### 公平性说明

所有对比方法均采用 50 步 Euler 离散调度器采样（SAG 因方法限制使用 DDIM），SSG 作为即插即用的推理时方法，无需额外训练或模型架构修改。定量评估覆盖 FID、IS、Precision、Recall、AES、CLIP Score、PickScore、ImageReward 等多维度指标，并在 MS-COCO 2014/2017 和 ImageNet 三个数据集上进行了跨模型验证。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_08048/figures/010_Table.jpg]]

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_08048/figures/014_Table_6.jpg]]
*Table 6: Ablation on two types of token swap*

## 方法谱系与知识库定位

**核心瓶颈与因果杠杆**。现有无条件引导方法——包括 **SAG** (Hong et al., ICCV 2023)、**SEG** (Hong, NeurIPS 2024) 和 **PAG** (Ahn et al., ECCV 2024)——共享一个根本性局限：它们采用全局且不加区分的扰动策略。SAG 在输入图像上添加高斯噪声，SEG 和 PAG 则扰动注意力图。这类全局噪声注入忽视了两个关键的结构性信息：其一，扩散模型中不同网络层在不同时间步上的表示具有高度异质性；其二，同一特征图内部不同空间位置或通道的语义重要性差异显著。其直接后果是：当扰动强度不足时，弱化模型分支与原始分支差异过小，引导信号微弱，细节质量差；当扰动强度增大时，全局扰动破坏过多结构信息，导致生成图像出现噪声、过饱和或过简化等伪影。这从根本上限制了引导尺度的有效范围。

**SSG 的方法定位**。Self-Swap Guidance (SSG) 通过将扰动操作从“全局加噪”重构为“选择性令牌交换”，实现了精细粒度的扰动控制。其核心操作是在 Transformer 块的中间表示空间中，沿空间维度或通道维度计算令牌对之间的余弦相似度，并选择语义最不相似的 N 对令牌进行交换。这一设计在三个维度上区别于现有方法：(1) **扰动类型**从加性噪声变为令牌特征置换，避免了引入外部随机噪声；(2) **扰动粒度**从全局粗粒度变为逐令牌的选择性操作，仅扰动语义最不相似的部分，保留其余令牌的原始表示；(3) **扰动维度**支持空间与通道维度的联合交换——空间交换破坏局部结构，通道交换扰动全局语义属性，两者互补。此外，SSG 维护原始分支与扰动分支两个并行前向通路，在 Transformer 块开始前和残差连接前应用交换操作，以最大化扰动效果。

**方法谱系中的位置**。SSG 属于推理时引导方法的谱系，与 CFG (Classifier-Free Guidance) 和各类无条件引导方法共享“通过外推两个分支的预测差异来实现引导”的数学框架。其引导公式 $\tilde{\epsilon}(x_t) = \epsilon_{\text{ori}}(x_t) + \omega(\epsilon_{\text{ori}}(x_t) - \epsilon_{\text{pert}}(x_t))$ 与 CFG 的 $\tilde{\epsilon}_{\text{CFG}}(x_t, y) = \epsilon_{\text{cond}}(x_t, y) + \omega(\epsilon_{\text{cond}}(x_t, y) - \epsilon_{\text{uncond}}(x_t, \mathcal{O}))$ 在形式上完全对应，区别仅在于负参照分支的来源：CFG 使用无条件模型输出，SSG 使用令牌交换扰动后的模型输出。这一对应关系使得 SSG 天然兼容 CFG——实验证明两者联合使用可进一步将 FID 从 31.41 降至 30.82，CLIP Score 升至 0.319（Table 7）。

**适用边界**。SSG 作为即插即用的推理时方法，无需额外训练或修改模型架构，可直接集成到标准扩散流水线中。当前验证范围覆盖 SD1.5 和 SDXL 在 MS-COCO 2014、MS-COCO 2017 和 ImageNet 上的无条件与条件生成任务。方法对超参数（引导尺度 $\omega$ 和交换比率 $r$）的敏感性较低，在更宽的参数范围内保持稳定性能（Figure 5），这显著优于 SAG、SEG 和 PAG 在高低尺度下的性能退化。然而，SSG 引入的额外计算开销（维护双分支前向传播及令牌相似度计算）的定量分析尚未充分展开。

**开放问题**。以下方向有待进一步探索：(1) SSG 对其他生成任务（如视频生成、3D 生成）的可扩展性尚未验证；(2) 在非 U-Net 架构的扩散模型（如 DiT）上的表现有待检验；(3) 超参数 $\omega$ 和 $r$ 的自适应选择策略尚未提出，当前依赖手动调节；(4) 令牌交换的计算复杂度优化（如近似最近邻搜索）可进一步降低额外开销。

## 原文 PDF

![[paperPDFs/arxiv_2026/Self_Swap_Guidance_Guiding_a_Diffusion_Model_by_Swapping_Its_Tokens.pdf]]