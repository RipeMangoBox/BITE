---
title: Content-Aware Dynamic Patchification for Efficient Video Diffusion
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Content_Aware_Dynamic_Patchification_for_Efficient_Video_Diffusion.pdf
project_link: "https://shengli99.github.io/DynaPatch/"
code_link: null
aliases:
- CADPEVD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 内容感知的动态块划分机制：根据潜在特征的内容复杂度，自适应选择每个时空区域的块大小（(1,2,2)/(2,2,2)/(1,4,4)），通过可训练路由器与扩散模型联合优化。
primary_logic: 与扩散目标联合优化路由器，而非依赖启发式熵或文本复杂度，使分块决策直接服务于生成质量；通过扩散损失、注意力引导损失和token预算正则化，实现计算资源的高效分配。
claims:
- DynaPatch在30% token减少下达到VBench Total Score 83.42（基线83.61），同时获得1.5倍加速。
- DynaPatch在所有token减少率下均显著优于先前的块划分方法（FlexiDiT、D²iT）和token剪枝方法（SPViT）。
- 注意力图引导训练一致提升生成质量；30% token减少下，有引导的Total Score为83.42，无引导下降至82.05。
- VBench 上 Total Score (20% token reduction) = 83.56
---

# Content-Aware Dynamic Patchification for Efficient Video Diffusion

> [!tip] 核心洞察
> 与扩散目标联合优化路由器，而非依赖启发式熵或文本复杂度，使分块决策直接服务于生成质量；通过扩散损失、注意力引导损失和token预算正则化，实现计算资源的高效分配。

| 字段 | 内容 |
|------|------|
| 中文题名 | 内容感知的动态块划分用于高效视频扩散 |
| 英文题名 | Content-Aware Dynamic Patchification for Efficient Video Diffusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_Content-Aware_Dynamic_Patchification_for_Efficient_Video_Diffusion_CVPR_2026_paper.html) · [Project](https://shengli99.github.io/DynaPatch/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DynaPatch |
| Dataset | VBench |

> [!tip] 效果简介
> - VBench 上，Total Score (20% token reduction) 83.56 vs 83.61 (uniform finest, 0% reduction) (1.3x speedup, Score -0.05)；Total Score (30% token reduction) 83.42 vs 83.61 (uniform finest, 0% reduction) (1.5x speedup, Score -0.19)；Total Score (40% token reduction) 82.19 vs 83.61 (uniform finest, 0% reduction) (1.8x speedup, Score -1.42)。

## 概述

视频扩散模型近年来在生成质量上取得了显著进展，但其核心架构——扩散Transformer（DiT）——通常采用固定均匀的块划分策略，对所有时空区域使用相同的细粒度分块。这一设计忽略了视频内容在空间和时间上的高度异质性：视觉简单或静止的背景区域与复杂运动的前景区域被分配了相同数量的token，导致大量冗余计算，严重制约了推理效率。

针对这一瓶颈，本文提出 **DynaPatch**，一种内容感知的动态块划分框架。其核心思想是让模型根据潜在特征的内容复杂度，自适应地为每个时空区域选择合适的块大小，从而在保持生成质量的前提下大幅减少token数量。DynaPatch 的核心机制包括三个层面：

1. **可训练路由器**：一个轻量级三层MLP，直接处理3D VAE编码的潜在特征，为每个时空区域从三种候选块大小 `(1,2,2)`、`(2,2,2)`、`(1,4,4)` 中做出离散选择。路由器不显式依赖扩散时间步，而是从噪声潜在特征中隐式感知去噪阶段。
2. **联合优化目标**：路由器的训练与扩散模型端到端联合进行，损失函数由三部分组成——扩散去噪损失、注意力图引导损失和token预算正则化损失。注意力引导损失将路由器的软概率与DiT内部的区域注意力图对齐，使分块决策直接服务于生成质量；预算损失则灵活控制整体token数量。
3. **跨粒度位置编码**：粗粒度块的位置编码由其内部细粒度块位置编码的平均得到，保证不同粒度token在统一位置空间中保留相对时空关系。

实验结果表明，DynaPatch 在 VBench 基准上实现了显著的速度提升与质量保持。在30% token减少率下，DynaPatch 达到 VBench Total Score 83.42（基线83.61），同时获得1.5倍加速；在40%减少率下仍保持82.19分，加速达1.8倍。与先前的块划分方法（**FlexiDiT** (Anagnostidis et al., CVPR 2025)、**D²iT** (Jia et al., CVPR 2025)）和token剪枝方法（**SPViT** (Kong et al., ECCV 2022)）相比，DynaPatch 在所有token减少率下均显著优于这些方法。消融实验进一步证实，注意力图引导训练是性能的关键保障——去除该引导后，30%减少率下的Total Score从83.42降至82.05。

DynaPatch 的方法定位处于视频扩散模型效率优化的前沿：它不同于依赖启发式规则或时间步调度的粗粒度方案，也不同于事后剪枝的token选择策略，而是通过与扩散目标的联合优化，学习内容感知的、细粒度的块划分决策，实现了计算资源的高效分配。

## 背景与动机

### 视频扩散模型的效率瓶颈

视频扩散模型近年来取得了显著进展，但高昂的计算开销始终制约其实际部署。当前主流架构——扩散Transformer（DiT）——将视频编码为潜在空间中的时空token序列，并通过大规模Transformer进行迭代去噪。在这一流程中，**块划分（patchification）** 是将连续潜在特征离散化为token的关键步骤：它将3D VAE编码器输出的潜在表示按固定时空尺寸切分为不重叠的块，每个块被线性投影为一个token嵌入。

几乎所有现有视频DiT模型（包括Open-Sora、CogVideoX、HunyuanVideo等）都采用**固定均匀的块划分策略**——对所有时空区域使用相同的最细粒度块大小（如(1,2,2)，即时间维度1帧、空间维度2×2像素的潜在块）。这种"一刀切"的做法忽略了视频内容的天然异质性：一段视频中往往同时存在快速运动的复杂区域和近乎静止的简单背景。固定细粒度分块意味着**视觉简单或静止区域产生与复杂区域等量的token**，造成大量冗余计算。

从token数量角度看，一个(1,2,2)的块仅覆盖极小的时空体积，一段数秒的视频即可产生数万乃至数十万个token。考虑到DiT中自注意力的计算复杂度与token数量的平方成正比，冗余token对推理延迟和显存占用的影响是超线性的。这一效率瓶颈在长视频生成和高分辨率场景下尤为突出。

### 现有加速方法的局限

针对视频扩散模型的效率问题，学术界已提出多种加速策略，大致可分为两类：

**（1）token剪枝与合并。** 这类方法在token进入DiT骨干网络后，依据某种重要性准则丢弃或合并部分token。代表性工作如**SPViT**（Kong et al., ECCV 2022）基于注意力图或token范数进行剪枝。然而，剪枝操作发生在token已被完整生成之后，这意味着块划分和线性投影的计算开销已经付出；更重要的是，剪枝丢弃的信息不可恢复，可能导致细粒度视觉细节的永久丢失。

**（2）粗粒度块划分调度。** 这类方法直接改变块大小以减少token总数。**FlexiDiT**（Anagnostidis et al., CVPR 2025）提出基于扩散时间步的块大小调度——在去噪早期使用粗粒度块、后期切换为细粒度块。其局限在于：决策仅依赖时间步，完全忽略了**不同空间区域的内容差异**。一个静态背景区域即使在去噪后期也不需要最细粒度分块，而一个快速运动的前景区域在早期可能就需要较高分辨率。

**D²iT**（Jia et al., CVPR 2025）向前迈进了一步，引入可训练路由器实现区域级块大小选择。但其路由器训练依赖**熵启发式标签**——以各区域的信息熵作为监督信号，而非直接与扩散模型的生成质量对齐。这种间接监督使得路由决策可能与实际生成需求脱节：低熵区域未必不重要（例如平坦的人脸区域对感知质量至关重要），高熵区域未必需要最细粒度（例如噪声纹理）。

### 核心动机与研究问题

上述分析揭示了当前方法的一个共同盲区：**分块决策与扩散模型的生成目标之间缺乏直接耦合**。无论是基于启发式规则（时间步、熵）还是后验剪枝，都没有让路由器"理解"不同区域对最终生成质量的差异化贡献。

这引出了本文的核心研究问题：**能否设计一种内容感知的动态分块机制，通过与扩散模型联合优化，使每个时空区域的分块粒度直接服务于生成质量？**

实现这一目标面临三个关键技术挑战：

1. **离散决策的可微优化。** 块大小选择是离散的（从有限候选集中选取），而扩散模型训练依赖梯度反向传播。如何在保持端到端可训练的前提下实现离散路由？

2. **生成感知的路由信号。** 扩散损失是全局的标量信号，难以提供空间细粒度的路由指导。如何让路由器感知不同区域对生成质量的相对重要性？

3. **效率与质量的灵活权衡。** 不同应用场景对推理速度和生成质量有不同的偏好。如何在不重新训练的情况下灵活控制token减少率？

## 核心创新

DynaPatch 的核心创新在于将视频扩散Transformer中**固定均匀的块划分（patchification）替换为内容感知的动态机制**，通过一个与扩散模型联合优化的轻量路由器，为每个时空区域自适应选择最合适的块大小。这一设计的本质是将“在哪里分配计算资源”的决策权交给生成模型自身，而非依赖人工预设的启发式规则。

### 从固定分块到动态三选一

基线方法采用固定均匀的 `(1,2,2)` 分块，对所有时空区域一视同仁。然而，视频中大量区域（如静止背景、低纹理表面）并不需要如此细粒度的token化，这造成了严重的计算冗余。DynaPatch 将分块策略扩展为**基于内容的自适应三选一**：路由器为每个时空区域从 `(1,2,2)`、`(2,2,2)` 和 `(1,4,4)` 三种候选块大小中做出离散选择。这三种尺寸在时间维度和空间维度上各有侧重，使模型能够根据内容的运动速度和纹理复杂度灵活调配token密度——快速运动或纹理丰富区域保留细粒度，静态或简单区域合并为粗粒度。

### 可训练路由器：让扩散损失驱动分块决策

与先前工作采用扩散时间步调度（如 **FlexiDiT** (Anagnostidis et al., CVPR 2025)）或熵启发式标签训练（如 **D²iT** (Jia et al., CVPR 2025)）不同，DynaPatch 的路由器是一个**轻量级三层MLP**（隐藏维度1024），直接处理3D VAE编码器输出的潜在特征，不显式依赖时间步作为输入。噪声水平信息已蕴含在带噪潜在特征中，路由器无需额外的时间步信号即可感知去噪阶段的内容复杂度。

更关键的是，路由器**与扩散模型通过扩散损失端到端联合优化**。这意味着分块决策不是基于某个代理指标（如熵、文本复杂度）的“猜测”，而是直接服务于最终的生成质量目标。路由器的离散选择通过 **Straight-Through Gumbel-Softmax** 实现可微训练：前向传播使用硬选择的独热向量，反向传播则通过未脱钩的软概率传播梯度。Gumbel-Softmax 的温度从初始值1.0线性衰减至0.2，使路由决策从早期探索逐步收敛为确定性选择。

### 注意力引导：让路由器“看见”生成模型关注什么

DynaPatch 引入了一项独特的训练信号——**注意力图引导损失**。其核心思想是：DiT 内部的注意力图揭示了生成模型认为哪些区域对去噪最为关键，这些区域理应获得更细粒度的token化。具体而言，该损失将路由器对最细块大小 `(1,2,2)` 的软概率与 DiT 内部经层-头筛选的归一化区域注意力图进行余弦相似度对齐。实验表明，仅当去噪步数较低（如 $t<500$，总步数 $T=1000$）时启用该损失，此时注意力图已趋于稳定且具有语义意义。

这一设计的消融证据极为有力：在30% token减少率下，有注意力引导的 VBench Total Score 为83.42，无引导则骤降至82.05（见表2），证实了注意力信号对路由器训练的关键作用。

### 位置编码的跨粒度一致性

动态分块带来的一个技术挑战是：不同粒度的token如何在同一位置空间中保持空间一致性？DynaPatch 的解决方案简洁而有效——粗粒度块的位置编码由其内部 $N$ 个最细粒度块位置编码的平均得到：

$$P E _ { \mathrm { c o a r s e } } = \frac { 1 } { N } \sum _ { i = 1 } ^ { N } P E _ { \mathrm { f i n e } , i }$$

这一设计保证了不同粒度token在统一位置空间中保留相对时空关系，无需为每种块大小学习独立的位置编码表。

### 预算正则化：灵活而非强制的token控制

Token预算损失鼓励所有区域平均的软token代价接近目标预算比，但采用软约束而非硬性强制。这使路由器在整体效率目标下仍保留根据内容灵活调配的自由度——某些区域可以“超预算”使用细粒度token，只要其他区域相应节省即可。总训练目标为三者加权和：

$$\mathcal { L } _ { \mathrm { t o t a l } } = \mathcal { L } _ { \mathrm { d i f f u s i o n } } + \lambda _ { \mathrm { a t t n } } \mathcal { L } _ { \mathrm { a t t n - g u i d e d } } + \lambda _ { \mathrm { b u d g e t } } \mathcal { L } _ { \mathrm { b u d g e t } }$$

### 与先前方法的本质差异

相较于 **FlexiDiT** 的全局时间步级调度和 **D²iT** 的熵启发式训练，DynaPatch 的关键跃升在于：分块决策是**区域级、内容自适应且由扩散损失直接驱动**的，而非依赖外部启发式信号或粗粒度时间步调度。相较于 **SPViT** (Kong et al., ECCV 2022) 等token剪枝方法直接丢弃token可能造成的信息丢失，DynaPatch 通过合并相邻token保留完整信息，仅在空间粒度上做权衡。

## 整体框架

DynaPatch 的整体推理流程围绕一个核心思想展开：**让扩散模型根据视频内容复杂度，自适应地为不同时空区域选择不同的块划分粒度**。图 2 展示了完整的推理流水线。

### 管线模块与数据流

整个框架由六个核心模块串联构成：

1. **3D VAE Encoder**：将输入视频编码到低维潜在空间，产生时空压缩的潜在特征。这些特征既作为后续去噪的输入，也作为路由器的内容感知信号源。

2. **Patch-size Router（MLP）**：一个轻量级的三层 MLP（隐藏维度 1024），直接接收 3D VAE 编码后的潜在特征，为每个时空区域预测分块大小的离散选择。路由器不显式依赖扩散时间步——噪声强度已隐含在加噪后的潜在特征中。

3. **Learnable Patchify Layers**：根据路由器的硬决策（通过 Straight-Through Gumbel-Softmax 获得），将每个区域的潜在特征映射为对应粒度的 token 嵌入。候选块大小包括三种：`(1, 2, 2)`（最细）、`(2, 2, 2)` 和 `(1, 4, 4)`（最粗），分别对应 1×、2× 和 2× 的 token 压缩比。

4. **DiT Backbone**：处理混合粒度的 token 序列，执行扩散去噪。不同大小的 token 通过统一的粗粒度位置编码方案保持空间一致性——粗粒度块的位置编码由其内部 $N$ 个最细粒度块位置编码的平均得到：

   $$PE _ { \mathrm { c o a r s e } } = \frac { 1 } { N } \sum _ { i = 1 } ^ { N } P E _ { \mathrm { f i n e } , i }$$

5. **Learnable Unpatchify Layers**：将 DiT 输出的 token 序列恢复为原始时空分辨率的潜在特征，与 Patchify Layers 形成对称结构。

6. **3D VAE Decoder**：从去噪后的潜在特征重建最终视频。

### 训练时的联合优化

图 4 展示了路由器训练的三个目标。与推理时使用硬决策不同，训练阶段通过 **Straight-Through Gumbel-Softmax** 实现离散路由的可微优化。具体而言，对路由器输出的 logits $S$ 加入 Gumbel 噪声 $g$，以温度 $\tau$ 缩放后得到软概率分布：

$$y _ { \mathrm { s o f t } } = \mathrm { S o f t m a x } \left( \frac { S + g } { \tau } \right)$$

前向传播使用硬选择的独热向量 $y_{\mathrm{hard}}$，反向传播则通过未脱钩的软概率 $y_{\mathrm{soft}}$ 传递梯度，即直通估计器（STE）：

$$y _ { \mathrm { S T E } } = y _ { \mathrm { h a r d } } - \left( y _ { \mathrm { s o f t } } \right) _ { \mathrm { d e t a c h e d } } + y _ { \mathrm { s o f t } }$$

温度 $\tau$ 随训练步数线性衰减，使路由决策从探索逐步收敛为确定性选择：

$$\tau _ { \mathrm { c u r r e n t } } = m a x ( \tau _ { \mathrm { m i n } } , \tau _ { \mathrm { i n i t i a l } } \times \left( 1 - \frac { s t e p } { t o t a l \_ s t e p s } \right) )$$

总训练损失由三项加权构成：

$$\mathcal { L } _ { \mathrm { t o t a l } } = \mathcal { L } _ { \mathrm { d i f f u s i o n } } + \lambda _ { \mathrm { a t t n } } \mathcal { L } _ { \mathrm { a t t n - g u i d e d } } + \lambda _ { \mathrm { b u d g e t } } \mathcal { L } _ { \mathrm { b u d g e t } }$$

- **扩散损失** $\mathcal{L}_{\mathrm{diffusion}}$：标准的视频扩散去噪目标，确保生成质量。
- **注意力图引导损失** $\mathcal{L}_{\mathrm{attn-guided}}$：将路由器对最细块大小 `(1,2,2)` 的软概率与 DiT 内部经层-头筛选的归一化区域注意力图进行余弦相似度对齐，引导路由器关注生成模型认为重要的区域：

  $$\mathcal { L } _ { \mathrm { a t t n - g u i d e d } } = 1 - \mathrm { C o s i n e } ( y _ { \mathrm { s o f t } } ^ { ( 1 , 2 , 2 ) } , \; \mathrm { a t t e n t i o n . m a p } )$$

  该损失仅在较低扩散时间步（如 $t < 500$，总步数 $T=1000$）启用，因为此时注意力图更具语义意义。

- **Token 预算损失** $\mathcal{L}_{\mathrm{budget}}$：以软约束方式鼓励所有区域的平均 token 代价接近目标预算比 $r_{\mathrm{target}}$，避免刚性强制固定选择比例：

  $$\mathcal { L } _ { \mathrm { b u d g e t } } = \left( \frac { 1 } { M } \sum _ { j = 1 } ^ { M } \sum _ { k } y _ { \mathrm { s o f t } , j } ^ { ( k ) } \cdot C _ { k } - r _ { \mathrm { t a r g e t } } \right) ^ { 2 }$$

  其中 $C_k$ 为第 $k$ 种块大小相对于最细粒度的 token 倍数。

### 关键设计决策

- **路由器输入粒度**：路由器以候选块大小中最粗粒度的形状 `(2, 4, 4)` 作为输入区域单元，确保每个区域都能被映射到任意候选块大小。
- **不依赖时间步**：路由器不接收扩散时间步作为显式输入，噪声强度信息已编码在加噪潜在特征中，简化了路由器设计并使其完全由内容驱动。
- **位置编码一致性**：粗粒度块的位置编码由其内部细粒度块位置编码的平均得到，保证不同粒度 token 在统一位置空间中保留相对时空关系，使 DiT 骨干无需修改即可处理混合粒度序列。

### 补充图表

![[assets/figures/papers/paper_list_l849_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Content_Aware_Dynam/figures/002_Figure_2.jpg]]
*Figure 2: Overall workflow of our DynaPatch design during inference. Each small square in the latent representation indicates a (1, 2, 2) latent patch, which is the by-default patch size in baseline model*

## 核心模块与公式推导

### 动态块划分框架概述

DynaPatch 的核心设计是在视频扩散 Transformer（DiT）中引入**内容感知的动态块划分机制**：根据 3D VAE 编码器输出的潜在特征的内容复杂度，为每个时空区域自适应选择分块大小。系统由四个关键模块串联构成：**分块大小路由器（Patch-size Router）**、**可学习块化层（Learnable Patchify Layers）**、**DiT 骨干网络**和**可学习反块化层（Learnable Unpatchify Layers）**。

推理流程如 Figure 2 所示：3D VAE 编码器将视频压缩为潜在表示后，路由器预测每个区域的分块大小，块化层据此将潜在特征映射为不同粒度的 token 嵌入，经 DiT 去噪处理后由反块化层恢复为原始时空分辨率，最终由 3D VAE 解码器重建视频。

### 分块大小路由器

路由器是一个**轻量级三层 MLP**，隐藏维度为 1024。其输入区域的形状由候选块大小中最粗的粒度决定——在默认配置（候选块大小为 (1,2,2)、(2,2,2)、(1,4,4)）下，输入区域形状为 (2,4,4)。值得注意的是，路由器**不显式接收扩散时间步作为输入**；噪声水平信息已蕴含在加噪后的潜在特征中，这使得路由器能够根据内容本身而非去噪阶段做出决策。

路由器的输出是每个区域的离散三选一决策，对应三种块大小。不同块大小产生的 token 数量关系如 Figure 1 所示：以最细粒度 (1,2,2) 为基准（1× token），(2,2,2) 产生 0.5× token，(1,4,4) 产生 0.25× token。

![[assets/figures/papers/paper_list_l849_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Content_Aware_Dynam/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of different patch sizes*

### 位置编码策略

为处理混合粒度 token 序列，DynaPatch 采用**粗粒度位置编码的平均化策略**：

$$P E _ { \mathrm { c o a r s e } } = \frac { 1 } { N } \sum _ { i = 1 } ^ { N } P E _ { \mathrm { f i n e } , i }$$

其中 $N$ 为一个粗块内包含的最细粒度块数量。一个粗块的位置编码等于其覆盖的 $N$ 个 (1,2,2) 细粒度块位置编码的平均值。该设计保证了不同粒度 token 在统一位置空间中保留相对时空关系，使 DiT 能够无缝处理混合粒度的 token 序列。

### 训练目标

路由器与扩散模型通过**端到端联合优化**训练，总损失函数为三项的加权和：

$$\mathcal { L } _ { \mathrm { t o t a l } } = \mathcal { L } _ { \mathrm { d i f f u s i o n } } + \lambda _ { \mathrm { a t t n } } \mathcal { L } _ { \mathrm { a t t n - g u i d e d } } + \lambda _ { \mathrm { b u d g e t } } \mathcal { L } _ { \mathrm { b u d g e t } }$$

三项损失分别对应 Figure 4 所示的三个训练目标：
- **扩散损失** $\mathcal{L}_{\mathrm{diffusion}}$：标准的视频扩散去噪损失，保证生成质量；
- **注意力图引导损失** $\mathcal{L}_{\mathrm{attn-guided}}$：将路由器决策与 DiT 内部的显著性区域对齐；
- **Token 预算正则化损失** $\mathcal{L}_{\mathrm{budget}}$：控制整体 token 数量接近目标预算。

![[assets/figures/papers/paper_list_l849_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Content_Aware_Dynam/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of router training objectives, including ➀ Diffusion loss, ➁ Attention Guidance Loss, and ➂ Budget Loss. The fire icon indicates that the router, patchify layers, and DiT blocks are actively being trained*

### 可微路由：Straight-Through Gumbel-Softmax

路由器的离散选择本质上不可微。为实现端到端训练，DynaPatch 采用 **Straight-Through Gumbel-Softmax** 技术。对路由器输出的 logits $S$，加入 Gumbel 噪声 $g$ 并以温度 $\tau$ 缩放，得到连续近似的软概率分布：

$$y _ { \mathrm { s o f t } } = \mathrm { S o f t m a x } \left( \frac { S + g } { \tau } \right)$$

前向传播中使用硬选择的独热向量 $y_{\mathrm{hard}}$，反向传播中通过未脱钩的软概率 $y_{\mathrm{soft}}$ 传播梯度，梯度更新公式为：

$$y _ { \mathrm { S T E } } = y _ { \mathrm { h a r d } } - \left( y _ { \mathrm { s o f t } } \right) _ { \mathrm { d e t a c h e d } } + y _ { \mathrm { s o f t } }$$

温度 $\tau$ 随训练进程线性衰减，使路由决策从探索逐步收敛为确定性选择：

$$\tau _ { \mathrm { c u r r e n t } } = m a x ( \tau _ { \mathrm { m i n } } , \tau _ { \mathrm { i n i t i a l } } \times \left( 1 - \frac { s t e p } { t o t a l \_ s t e p s } \right) )$$

其中 $\tau_{\mathrm{initial}} = 1$，$\tau_{\mathrm{min}} = 0.2$。

### 注意力图引导损失

该损失将路由器对最细块大小 (1,2,2) 的软概率与 DiT 内部的区域注意力图进行对齐，引导路由器关注生成模型认为重要的区域：

$$\mathcal { L } _ { \mathrm { a t t n - g u i d e d } } = 1 - \mathrm { C o s i n e } ( y _ { \mathrm { s o f t } } ^ { ( 1 , 2 , 2 ) } , \; \mathrm { a t t e n t i o n . m a p } )$$

注意力图并非简单平均所有层和头，而是从 DiT 的特定层-头对中筛选（如 Figure 5 所示，精选层-头对产生的注意力图比全层全头平均更具判别性）。此外，该损失仅在较低时间步（例如 $t < 500$，总步数 $T=1000$）启用，因为高噪声阶段的注意力图尚不可靠。

### Token 预算正则化损失

该损失鼓励所有区域的平均软 token 代价接近目标预算比，实现灵活而非强制的 token 数量控制：

$$\mathcal { L } _ { \mathrm { b u d g e t } } = \left( \frac { 1 } { M } \sum _ { j = 1 } ^ { M } \sum _ { k } y _ { \mathrm { s o f t } , j } ^ { ( k ) } \cdot C _ { k } - r _ { \mathrm { t a r g e t } } \right) ^ { 2 }$$

其中 $M$ 为区域总数，$k$ 遍历候选块大小，$C_k$ 为该块大小相对于最细粒度的 token 倍数（如 (1,2,2) 对应 $C=1$，(2,2,2) 对应 $C=0.5$，(1,4,4) 对应 $C=0.25$），$r_{\mathrm{target}}$ 为目标 token 保留比。该设计允许路由器在不同区域间灵活分配计算资源，而非强制每个区域达到相同的减少率。

## 实验与分析

### 主实验：VBench 基准上的性能与效率权衡

DynaPatch 的核心验证在 VBench 视频生成基准上进行，统一使用最细粒度 (1,2,2) 固定分块的 DiT 作为基线（Baseline），对比方法包括基于时间步调度的 **FlexiDiT**（Anagnostidis et al., CVPR 2025）、基于熵启发式路由的 **D²iT**（Jia et al., CVPR 2025）以及 token 剪枝方法 **SPViT**（Kong et al., ECCV 2022）。所有方法使用相同的 DiT 骨干和 3D VAE，在相同 token 减少率下比较。

**Table 1** 汇总了不同 token 减少率下的 VBench Total Score 与加速比：

- **20% token 减少**：DynaPatch 取得 Total Score **83.56**，相比基线（83.61，0% 减少）仅下降 0.05，同时获得 **1.3× 加速**。
- **30% token 减少**：Total Score 为 **83.42**（基线 83.61），下降 0.19，加速 **1.5×**。
- **40% token 减少**：Total Score 为 **82.19**，下降 1.42，加速 **1.8×**。

在所有 token 减少率下，DynaPatch 的 VBench 得分均显著高于 FlexiDiT、D²iT 和 SPViT，验证了内容感知动态分块相比时间步级调度、熵启发式路由和 token 剪枝的优越性。值得注意的是，DynaPatch 在 30% token 减少时几乎保持与基线相同的生成质量，而其他方法在同等减少率下已出现明显退化。

### 消融实验：注意力图引导的关键作用

**Table 2** 报告了注意力图引导损失对路由训练的影响。在 30% token 减少条件下：

- 启用注意力图引导（w/ Attn-guide）：Total Score **83.42**
- 去除注意力图引导（w/o Attn-guide）：Total Score 降至 **82.05**

这一 1.37 分的差距表明，仅依赖扩散损失和预算正则化不足以让路由器学到最优的块大小分配——路由器可能将粗粒度块错误地分配给生成模型关注的关键区域。注意力图引导通过将路由器的最细粒度软概率与 DiT 内部注意力图对齐，为路由器提供了明确的“哪些区域对生成质量重要”的信号，使分块决策直接服务于扩散目标的优化。

### 路由器行为分析：去噪过程中的动态 token 分配

**Figure 3** 展示了不同去噪时间步下的 token 减少率变化。路由器并非在整个去噪过程中保持固定的减少率，而是呈现出动态调整行为：在去噪早期（高噪声阶段），token 减少率相对较高，因为此时潜在特征中的细粒度结构尚未显现；随着去噪进行，路由器逐步为内容复杂的区域分配更细的块大小，token 减少率相应降低。这一行为表明路由器确实学到了内容感知的分块策略，而非简单的均匀降采样。

### 层-头筛选对注意力引导的影响

**Figure 5** 对比了两种区域注意力图构建方式：(a) 对所有层和头的注意力取平均；(b) 使用精选的层-头对。结果表明，筛选后的层-头对产生的注意力图更能聚焦于语义关键区域，避免了全层平均带来的噪声和注意力弥散问题。这一设计是注意力引导损失有效的关键前提——如果引导信号本身不可靠，对齐训练将适得其反。

### 公平性与开销说明

速度测量基于实际推理时间，包含路由器前向计算的额外开销。路由器为轻量级三层 MLP（隐藏维度 1024），其计算量相比 DiT 骨干可忽略不计，因此加速比主要来自 token 数量减少带来的自注意力计算量下降。所有对比方法在相同 VAE 和 DiT 骨干下评估，确保比较的公平性。

### 补充图表

![[assets/figures/papers/paper_list_l849_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Content_Aware_Dynam/figures/006_Table_1.jpg]]
*Table 1: Evaluation of different patchification and token pruning approaches on VBench. The full results on all evaluation dimensions of VBench are in the supplementary material (Section 11)*

![[assets/figures/papers/paper_list_l849_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Content_Aware_Dynam/figures/008_Table_2.jpg]]
*Table 2: Ablation study on attention map guidance router training*

![[assets/figures/papers/paper_list_l849_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Content_Aware_Dynam/figures/003_Figure_3.jpg]]
*Figure 3: Token reduction rate across denoising steps. Results are averaged over sampled videos*

![[assets/figures/papers/paper_list_l849_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Content_Aware_Dynam/figures/005_Figure_5.jpg]]
*Figure 5: (a) Video sample with the regional attention map from averaging all layers and heads. (b) Regional attention map using the selected layer–head pairs*

![[assets/figures/papers/paper_list_l849_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Content_Aware_Dynam/figures/007_Figure.jpg]]

## 方法谱系与知识库定位

### 问题定位与核心瓶颈

视频扩散Transformer（DiT）在生成高质量视频时，通常采用固定均匀的块划分（patchification）策略，对所有时空区域使用相同的最细粒度（如 (1,2,2)）进行token化。这种“一刀切”的策略忽视了视频内容的天然异质性——视觉简单的背景和静止区域与复杂运动区域被分配了相同的计算资源，导致大量冗余token和计算开销，严重制约推理效率。

DynaPatch的核心洞察在于：**块划分的粒度决策应当与扩散模型的生成目标联合优化，而非依赖启发式规则**。通过让路由器直接感知潜在特征的内容复杂度，并以扩散损失、注意力引导损失和token预算正则化进行端到端训练，分块决策能够真正服务于生成质量，实现计算资源的高效分配。

### 与现有方法的谱系关系

#### 1. 固定分块基线

最直接的基线是使用**Uniform Finest Patch**的标准DiT，即对所有时空区域统一采用 (1,2,2) 的最细粒度分块。该方法无任何动态机制，代表了质量上限但效率最低的极端。DynaPatch在保持该基线83.61的VBench Total Score几乎不变的前提下（83.42，-0.19），实现了1.5倍加速。

#### 2. 时间步级路由：FlexiDiT

**FlexiDiT**（Anagnostidis et al., CVPR 2025）提出了基于扩散时间步的粗粒度块大小调度策略。其核心假设是：去噪早期阶段噪声较大，可使用较粗粒度；后期阶段需要精细细节，切换为细粒度。这是一种**时间维度的粗粒度动态调整**，但忽略了同一时间步内不同空间区域的内容差异。

DynaPatch超越了这一范式：路由器直接处理3D VAE潜在特征，不显式依赖时间步作为输入（噪声水平已编码在noisy latent中），实现了**时空区域级的细粒度动态选择**。实验表明，在相同的token减少率下，DynaPatch显著优于FlexiDiT。

#### 3. 启发式标签训练的路由器：D²iT

**D²iT**（Jia et al., CVPR 2025）首次引入可学习路由器实现区域级块大小选择，但其训练依赖**熵启发式标签**——即用潜在特征的熵值作为“内容复杂度”的代理标签来监督路由器。这种方法存在根本性局限：熵高并不等同于对生成质量重要，两者之间存在语义鸿沟。

DynaPatch的关键突破在于**抛弃启发式标签，直接与扩散目标联合优化路由器**。通过Straight-Through Gumbel-Softmax实现离散决策的可微训练，路由器的梯度直接来自扩散损失，使其学会选择对去噪生成真正重要的区域使用细粒度分块。这一设计变更从根本上解决了启发式标签与生成目标不一致的问题。

#### 4. Token剪枝方法：SPViT

**SPViT**（Kong et al., ECCV 2022）代表另一类加速思路——先使用固定分块生成全部token，再基于重要性评分剪枝冗余token。这种方法存在先天不足：剪枝操作破坏了token序列的空间结构一致性，且重要性评分的准确性高度依赖启发式设计。

DynaPatch的**动态块划分**本质上优于token剪枝：通过在token化阶段就自适应选择粒度，避免了“先膨胀再剪枝”的计算浪费，同时保持了潜在空间的结构完整性。实验一致表明，DynaPatch在所有token减少率下均显著优于SPViT。

### 方法谱系图

从方法演进的角度，视频扩散模型的效率优化可归纳为以下路径：

1. **固定均匀分块** → 所有区域等粒度，效率最低
2. **时间步调度**（FlexiDiT, CVPR 2025）→ 时间维度粗粒度动态，忽略空间差异
3. **启发式路由器**（D²iT, CVPR 2025）→ 区域级动态，但依赖熵标签，与生成目标脱节
4. **端到端联合优化路由器**（DynaPatch, CVPR 2026）→ 区域级动态，直接由扩散损失+注意力引导+预算正则化驱动

DynaPatch处于这一谱系的当前最前沿：它继承了D²iT的区域级动态路由器思想，但通过联合优化机制和注意力图引导，从根本上解决了启发式标签与生成质量之间的不一致问题。

### 知识库定位与适用边界

#### 核心贡献定位

DynaPatch为视频扩散模型领域贡献了以下可迁移的知识组件：

- **内容感知的动态分块范式**：证明在token化阶段进行自适应粒度选择是可行的，且优于后验剪枝
- **联合优化路由器的训练框架**：Straight-Through Gumbel-Softmax + 扩散损失直接驱动的路由器训练方案
- **注意力图引导损失**：利用DiT内部注意力图作为“免费”的重要性信号，实现无外部监督的路由器引导
- **跨粒度位置编码方案**：粗粒度块位置编码由其内部细粒度块编码的平均得到，保证空间一致性

#### 适用边界

1. **架构依赖**：方法假设使用DiT架构和3D VAE进行视频潜在编码，直接迁移到其他生成架构（如UNet-based扩散模型）需要适配
2. **候选块大小的限制**：当前仅支持三种候选块大小 (1,2,2)/(2,2,2)/(1,4,4)，决策空间有限
3. **训练开销**：路由器需要与扩散模型联合训练，无法直接即插即用到预训练好的DiT模型上

### 局限与开放问题

#### 已验证的局限

论文未明确报告失败案例或局限性分析，以下局限需要手动验证：

- 路由器前向计算的额外开销在端侧或低功耗设备上的实际影响未量化
- 该方法在更长视频（分钟级）或更高分辨率（1080p+）下的可扩展性未经实验验证

#### 开放问题

1. **跨模态泛化**：动态块划分机制是否可推广到图像扩散模型或其他模态（如音频、3D生成）？图像模型的空间-only分块与视频的时空分块存在差异，路由器的设计需要相应调整。

2. **决策空间扩展**：若增加更多候选块大小（如 (2,4,4)、(1,8,8) 等），扩大路由器的离散决策空间，是否会进一步提升效率与质量的帕累托前沿？这需要在路由器容量和训练难度之间权衡。

3. **注意力引导的鲁棒性**：注意力图引导损失的设计是否对不同的DiT架构变体（不同层数、头数、注意力机制）保持鲁棒？层-头筛选策略的泛化性需要进一步验证。

4. **推理时自适应**：当前路由器在推理时执行确定性选择（argmax），是否可以利用软概率进行推理时的随机采样或集成，以进一步提升生成多样性或质量？

5. **与量化/蒸馏的协同**：动态分块与模型量化、知识蒸馏等正交加速技术的组合效果如何？是否存在协同或冲突效应？

6. **实时视频生成**：该方法在实时或交互式视频生成场景下的延迟表现和用户体验影响需要进一步研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/Content_Aware_Dynamic_Patchification_for_Efficient_Video_Diffusion.pdf]]