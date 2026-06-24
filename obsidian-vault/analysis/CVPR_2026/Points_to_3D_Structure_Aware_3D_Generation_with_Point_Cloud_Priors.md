---
title: "Points-to-3D: Structure-Aware 3D Generation with Point Cloud Priors"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Points_to_3D_Structure_Aware_3D_Generation_with_Point_Cloud_Priors.pdf
project_link: "https://jiatongxia.github.io/points2-3D/"
code_link: null
aliases:
- P3
- Points-to-3D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过将点云先验编码为稀疏结构潜变量并用掩码控制保留区域，同时设计修复网络替代原有结构生成网络，可以在潜空间中直接保留可见几何并补全不可见结构。
primary_logic: 将3D点云先验显式注入TRELLIS的稀疏结构潜变量空间，把3D生成重新定义为潜空间修复问题：编码可见区域为结构潜变量，用掩码保护这些区域，并训练一个修复网络从可见区域推断缺失几何，再通过分阶段采样保持边界一致性。
claims:
- 在Toys4K单物体生成上，使用真实点云先验的Points-to-3D在几何指标上远超所有基线，F-score达到0.963，显著优于TRELLIS的0.832。
- 在可见区域内，Points-to-3D的生成结果与真值几乎完全对齐，F-score达到0.998，Chamfer Distance仅为0.007。
- 即使使用VGGT估计的点云（无精确先验），Points-to-3D依然在渲染和几何质量上优于TRELLIS等现有方法。
- Toys4K 上 PSNR (Rendering) = 22.91
---

# Points-to-3D: Structure-Aware 3D Generation with Point Cloud Priors

> [!tip] 核心洞察
> 将3D点云先验显式注入TRELLIS的稀疏结构潜变量空间，把3D生成重新定义为潜空间修复问题：编码可见区域为结构潜变量，用掩码保护这些区域，并训练一个修复网络从可见区域推断缺失几何，再通过分阶段采样保持边界一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | Points-to-3D：基于点云先验的结构感知3D生成 |
| 英文题名 | Points-to-3D: Structure-Aware 3D Generation with Point Cloud Priors |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.18782) · [Project](https://jiatongxia.github.io/points2-3D/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Points-to-3D |
| Dataset | Toys4K, 3D-FRONT |

> [!tip] 效果简介
> - Toys4K 上，PSNR (Rendering) 22.91 vs 21.94 (TRELLIS) (+0.97)；SSIM (Rendering) 92.83 vs 91.46 (TRELLIS) (+1.37)；LPIPS (Rendering) 0.070 vs 0.105 (TRELLIS) (-0.035)。
> - 3D-FRONT 上，PSNR (Rendering) 21.63 vs 18.21 (TRELLIS) (+3.42)；F-Score (Geometry) 0.886 vs 0.478 (TRELLIS) (+0.408)。

## 概述

**问题瓶颈：** 当前领先的3D生成框架（如 **TRELLIS**，Xiang et al., CVPR 2025）在生成过程中，其稀疏结构潜变量（Sparse Structure latent）从纯高斯噪声初始化，缺乏将易于获取的可见区域点云先验作为硬几何约束直接注入生成过程的机制。这导致两个核心问题：生成结果无法忠实反映真实观测几何，且难以合理补全不可见区域。

**核心洞察：** Points-to-3D 将3D生成重新定义为**潜空间修复（latent inpainting）问题**。其因果机制在于：将可见点云体素化并编码为稀疏结构潜变量，用掩码保护已知区域，训练一个修复流Transformer从可见几何推断缺失结构，再通过两阶段采样保持修复边界的一致性。

**方法定位：** Points-to-3D 是对 TRELLIS 框架的定向改造——替换其结构潜变量的初始化方式与生成网络，而非从零构建新框架。该方法处于“3D先验驱动的可控生成”与“潜空间修复”的交叉点，与依赖图像条件间接整合点映射的方法（如 **SAM3D**）形成显式控制与隐式引导的对比。

**主要结果：** 在 Toys4K 单物体生成基准上，使用真实点云先验时，Points-to-3D 的几何 F-Score 达到 **0.963**（TRELLIS 为 0.832），Chamfer Distance 降至 **0.013**（TRELLIS 为 0.034）；在可见区域内，F-Score 高达 **0.998**，几乎与真值完全对齐。在 3D-FRONT 场景级生成中，F-Score 从 TRELLIS 的 0.478 提升至 **0.886**。即使使用 VGGT 估计的点云（无精确先验），渲染与几何质量仍优于所有不使用显式点云先验的基线方法。

## 背景与动机

3D内容生成正处于从“可生成”向“可控制”过渡的关键阶段。以**TRELLIS**（Xiang et al., CVPR 2025）为代表的3D原生扩散框架，通过在一个紧凑的稀疏结构（SS）潜空间与结构化潜空间（SLAT）中执行扩散过程，实现了高质量、多样化的3D资产生成。然而，这类方法存在一个根本性的结构瓶颈：**结构潜变量从纯高斯噪声初始化，缺乏任何机制将易于获取的可见区域几何先验作为硬约束直接注入生成过程**。

这一缺口的后果是双重的。一方面，当用户已经拥有部分3D信息（如深度传感器采集的点云、多视角重建的稀疏几何）时，现有方法无法利用这些信息来锚定生成结果，导致输出与真实几何之间缺乏忠实性。另一方面，纯噪声初始化使得模型在补全不可见区域时缺乏来自可见区域的几何线索，难以在保持全局一致性的前提下合理推断缺失结构。

从因果机制来看，问题的核心在于**先验信息的注入位置与形式**。现有方法要么完全依赖图像/文本条件进行隐式引导（如**LGM**, Tang et al., ECCV 2024），要么通过注意力机制间接整合点映射（如**SAM3D**），但这些途径都无法实现显式的、逐体素的几何控制。**VoxHammer**虽然使用了相同的3D先验进行编辑反演，但其依赖图像条件修复缺失区域，缺乏在潜空间中直接进行结构修复的机制，因而未能充分利用先验的几何约束力。

Points-to-3D的核心洞察在于：**将3D点云先验显式注入TRELLIS的稀疏结构潜变量空间，把3D生成重新定义为潜空间修复问题**。具体而言，该方法将可见区域的点云体素化并编码为结构潜变量，用掩码保护这些已知区域，其余区域填入噪声，然后训练一个修复网络从可见区域推断缺失几何。这一设计将“利用先验”从软约束升级为硬约束——已知区域的几何被强制保留，不可见区域的生成则被锚定在可见结构的边界条件之上。推理时，通过分阶段采样（先结构修复、后边界细化）进一步保证修复边界的一致性与平滑性。

## 核心创新

Points-to-3D的核心创新在于将3D生成问题重新定义为**稀疏结构潜空间中的条件修复问题**，通过显式注入点云先验作为硬几何约束，打破了现有方法从纯噪声初始化结构潜变量的范式。具体而言，该方法在**TRELLIS**（Xiang et al., CVPR 2025）框架上进行了四个关键改造：

### 1. 结构潜变量初始化：从纯噪声到点云先验引导

在原始TRELLIS中，稀疏结构（SS）潜变量从高斯噪声 $\boldsymbol{\epsilon}_{\mathrm{s}}$ 采样初始化，生成过程缺乏对真实几何的锚定。Points-to-3D将可见点云先验体素化为占据网格 $\mathbf{M}'$，通过VAE编码器 $\mathcal{E}_s$ 转化为结构潜变量 $\mathbf{q}_{\mathrm{vis}}$：

$$\mathbf{q}_{\mathrm{vis}} = \mathcal{E}_s(\mathbf{M}')$$

随后，利用可见区域的占据掩码 $\mathbf{m}_{\mathrm{s}}$ 将已知区域潜变量与噪声混合，形成修复的初始状态：

$$\mathbf{q}_{\mathrm{comb}} = \mathbf{m}_{\mathrm{s}} \odot \mathbf{q}_{\mathrm{vis}} + (1 - \mathbf{m}_{\mathrm{s}}) \odot \boldsymbol{\epsilon}_{\mathrm{s}}$$

这一设计使得生成过程从“无中生有”转变为“从已知推断未知”，在潜空间中直接保留了可见几何的硬约束。

### 2. 生成网络改造：修复流Transformer替代标准结构生成器

原始TRELLIS的稀疏结构流Transformer $G_s$ 仅接收条件嵌入，无法感知哪些区域已被先验占据。Points-to-3D将其改造为修复网络 $G_{\mathrm{inp}}$，通过扩展输入通道以拼接掩码信息：

$$\mathbf{x}_{\mathrm{inp}} = \operatorname{Concat}[\mathbf{q}_{\mathrm{comb}}, \mathbf{m}_{\mathrm{s}}], \quad \mathbf{x}_{\mathrm{inp}} \in \mathbb{R}^{r \times r \times r \times (c_{\mathrm{s}} + c_{\mathrm{m}})}$$

改造方式极为轻量：仅替换输入投影层，将通道维度从 $c_{\mathrm{s}}$ 扩展为 $c_{\mathrm{s}} + c_{\mathrm{m}}$，其余网络结构保持不变。训练目标采用条件流匹配损失，使网络学习从噪声到真实潜变量的方向向量。

### 3. 训练数据构造：可见性感知的配对数据生成

为了训练修复网络，需要构建“可见点云先验-完整结构潜变量”的配对数据。Points-to-3D从完整3D资产出发，通过多视角渲染与深度一致性检查，自动提取可见区域点云作为先验，同时保留完整结构潜变量作为真值。可见性判断基于投影深度与渲染深度的比较：

$$\mathbf{O}_{i}^{t} = \begin{cases} 1, & \text{if } |\mathbf{D}_{t}(\mathbf{u}_{i}) - w_{i}^{t}| < \tau \end{cases}$$

这一数据构造流程（Figure 3）使得修复网络能够在训练中学习从局部可见几何推断全局结构的映射。

### 4. 推理采样策略：两阶段修复-细化机制

推理阶段采用50步采样的两阶段策略（Figure 2）：
- **结构修复阶段**（前 $s=25$ 步）：保持掩码 $\mathbf{m}_{\mathrm{s}}$ 不变，在潜空间中修复缺失区域的全局结构；
- **边界细化阶段**（后 $t-s=25$ 步）：将掩码替换为全1掩码，将修复转化为标准去噪，平滑修复边界。

消融实验（Table 4）证实，纯修复（50步修复+0步细化）会导致边界区域产生几何空洞，而25+25的分配在Chamfer Distance（0.013）和F-Score（0.963）上达到最优。这一机制的关键在于：修复阶段建立了全局结构一致性，细化阶段通过少量噪声注入消除了修复边界的不连续性，同时不会破坏已知区域的几何保真度。

### 创新本质总结

上述四个改造共同构成了一个**因果干预链条**：点云先验 → 潜变量初始化 → 掩码保护 → 修复网络推断 → 边界细化。其核心洞察在于，通过将显式3D几何约束直接注入生成模型的潜空间，把不可控的随机生成转化为可控的条件补全，从而在可见区域实现接近完美的几何保真度（F-Score 0.998, Chamfer Distance 0.007, Table 3），同时在不可见区域生成合理且连贯的几何结构。

## 整体框架

Points-to-3D 的核心思想是将显式的3D点云先验注入到 TRELLIS（Xiang et al., CVPR 2025）的稀疏结构（SS）潜变量空间中，从而将3D生成重新定义为**潜空间修复问题**。其整体 pipeline 由五个关键模块串联而成，形成从点云先验到完整3D资产的端到端流程（Figure 2）。

![[assets/figures/papers/paper_list_l2572_https_arxiv_org_abs_2603_18782/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework. Given point cloud priors—either pre-existing or predicted by VGGT from input image—we first voxelize and VAE-encode it to obtain an SS latent, where the empty regions are filled with random noise and concatenated with an extracted mask to form the input paradigm for our model. During training, the input training data is fed into our inpainting flow transformer*

### 输入与预处理

框架接受两种形式的点云先验：**预先存在的点云**（如从多视角重建获得）或由 **VGGT** 从单张输入图像前馈预测的点云。点云先验首先经过体素化，转化为二值占据网格 $\mathbf{M}'$，随后通过 TRELLIS 预训练的 VAE 编码器 $\mathcal{E}_s$ 编码为初始 SS 潜变量：

$$\mathbf{q}_{\mathrm{vis}} = \mathcal{E}_s(\mathbf{M}')$$

### 修复输入构建

从可见点云中提取占据掩码 $\mathbf{m}_{\mathrm{s}}$（已知区域为1，未知区域为0），将可见区域的潜变量与高斯噪声 $\boldsymbol{\epsilon}_{\mathrm{s}}$ 按掩码混合，形成修复的初始状态：

$$\mathbf{q}_{\mathrm{comb}} = \mathbf{m}_{\mathrm{s}} \odot \mathbf{q}_{\mathrm{vis}} + (1 - \mathbf{m}_{\mathrm{s}}) \odot \boldsymbol{\epsilon}_{\mathrm{s}}$$

随后将混合潜变量与掩码沿通道维度拼接，构成修复网络的输入张量：

$$\mathbf{x}_{\mathrm{inp}} = \operatorname{Concat}[\mathbf{q}_{\mathrm{comb}}, \mathbf{m}_{\mathrm{s}}], \quad \mathbf{x}_{\mathrm{inp}} \in \mathbb{R}^{r \times r \times r \times (c_{\mathrm{s}} + c_{\mathrm{m}})}$$

### 修复流 Transformer

修复网络 $\mathcal{G}_{inp}$ 基于 TRELLIS 原有的稀疏结构流 Transformer $\mathcal{G}_s$ 改造而来：仅替换输入投影层以适配扩展后的通道数 $(c_s + c_m)$，其余网络结构保持不变。$\mathcal{G}_{inp}$ 在条件流匹配（Conditional Flow Matching）范式下训练，目标是最小化预测方向向量与真实方向向量之间的差异：

$$\mathcal{L}_{CFM} = \mathbb{E}_{t, \mathbf{q}_{\mathrm{gt}}, \epsilon} \left\| \mathcal{G}_{inp}(\mathbf{x}_{\mathrm{inp}}, t) - (\epsilon - \mathbf{q}_{\mathrm{gt}}) \right\|_{2}^{2}$$

训练数据通过多视角渲染与深度一致性检查构建：从完整资产中保留可见部分，提取可见点云先验-完整结构潜变量对（Figure 3），为条件修复提供监督信号。

### 两阶段推理采样

推理阶段采用 $t=50$ 步的采样策略，分为两个阶段：

1. **结构修复阶段**（前 $s=25$ 步）：保持掩码 $\mathbf{m}_{\mathrm{s}}$ 不变，$\mathcal{G}_{inp}$ 在潜空间中进行条件修复，从可见区域推断缺失的全局结构。
2. **边界细化阶段**（后 $t-s=25$ 步）：将掩码替换为全1掩码，将修复过程转化为标准去噪，平滑修复边界与已知区域之间的过渡，消除几何空洞。

### 下游生成

修复完成的 SS 潜变量通过稀疏结构解码器 $\mathcal{D}_s$ 解码为二值占据网格，随后进入 TRELLIS 的结构化潜变量生成阶段，结合图像/文本条件生成最终的带颜色与细节的3D资产。

### 关键设计决策

整个框架的核心创新在于**将点云先验显式注入潜空间**，而非通过注意力机制间接整合几何信息。这使得可见区域的几何能够被忠实保留（可见区域 F-score 达 0.998，CD 仅 0.007），同时修复网络在不可见区域进行合理补全。两阶段采样策略是平衡结构一致性与边界平滑性的关键：纯修复（50步）会导致边界区域产生几何空洞，而引入细化阶段后边界质量显著提升（Table 4, Figure 6）。

### 补充图表

![[assets/figures/papers/paper_list_l2572_https_arxiv_org_abs_2603_18782/figures/001_Figure_1.jpg]]
*Figure 1: We introduce explicit 3D point cloud priors into 3D generation framework, given a pre-existing point cloud or a feed-forward point cloud prediction from image input, our model generates high-quality 3D assets that faithfully preserve the observed structure while plausibly completing unobserved regions with coherent geometry*

## 核心模块与公式推导

Points-to-3D 的方法核心在于将点云先验显式注入 TRELLIS 的稀疏结构（Sparse Structure, SS）潜变量空间，并将 3D 生成重新定义为**潜空间修复问题**。整体流程包含三个关键阶段：点云先验的潜变量编码、修复网络的训练与推理、以及两阶段采样策略。

### 点云先验的潜变量编码

给定可见区域的点云先验 $P$，首先将其体素化为二值占据网格 $\mathbf{M}'$，随后通过 TRELLIS 预训练的 SS-VAE 编码器 $\mathcal{E}_s$ 转化为稀疏结构潜变量：

$$
\mathbf{q}_{\mathrm{vis}} = \mathcal{E}_s(\mathbf{M}')
$$

该潜变量 $\mathbf{q}_{\mathrm{vis}}$ 直接承载了可见区域的几何信息。为了构建修复任务的输入，需要从 $\mathbf{M}'$ 中提取可见性掩码 $\mathbf{m}_{\mathrm{s}}$——掩码中值为 1 的位置对应已知几何区域，值为 0 的位置对应待修复区域。

随后，将可见区域的潜变量与随机高斯噪声 $\boldsymbol{\epsilon}_{\mathrm{s}}$ 按掩码混合，形成修复的初始状态：

$$
\mathbf{q}_{\mathrm{comb}} = \mathbf{m}_{\mathrm{s}} \odot \mathbf{q}_{\mathrm{vis}} + (1 - \mathbf{m}_{\mathrm{s}}) \odot \boldsymbol{\epsilon}_{\mathrm{s}}
$$

这一混合机制确保已知区域的几何信息被完整保留，而未知区域则由噪声填充，等待修复网络进行推断补全。

### 修复流 Transformer 的输入与训练

修复网络 $\mathcal{G}_{inp}$ 由 TRELLIS 原有的稀疏结构生成网络 $\mathcal{G}_s$ 改造而来。具体改动为：将输入层的通道维度从 $c_{\mathrm{s}}$ 扩展为 $c_{\mathrm{s}} + c_{\mathrm{m}}$，使其能够同时接收混合潜变量和掩码信息，其余网络结构保持不变：

$$
\mathbf{x}_{\mathrm{inp}} = \operatorname{Concat}[\mathbf{q}_{\mathrm{comb}}, \mathbf{m}_{\mathrm{s}}], \quad \mathbf{x}_{\mathrm{inp}} \in \mathbb{R}^{r \times r \times r \times (c_{\mathrm{s}} + c_{\mathrm{m}})}
$$

训练采用条件流匹配（Conditional Flow Matching）损失，目标是让修复网络学习从噪声到真实完整潜变量 $\mathbf{q}_{\mathrm{gt}}$ 的方向向量：

$$
\mathcal{L}_{CFM} = \mathbb{E}_{t, \mathbf{q}_{\mathrm{gt}}, \epsilon} \left\| \mathcal{G}_{inp}(\mathbf{x}_{\mathrm{inp}}, t) - (\epsilon - \mathbf{q}_{\mathrm{gt}}) \right\|_{2}^{2}
$$

### 训练数据构造中的可见性判断

训练数据通过多视角渲染与深度一致性检查自动构建。对于完整资产的每个采样点，通过比较其在当前视角下的投影深度 $\mathbf{D}_{t}(\mathbf{u}_{i})$ 与渲染深度 $w_{i}^{t}$ 的差值来判断可见性：

$$
\mathbf{O}_{i}^{t} = \begin{cases} 1, & \text{if } |\mathbf{D}_{t}(\mathbf{u}_{i}) - w_{i}^{t}| < \tau \end{cases}
$$

仅保留被判定为可见的点云部分作为先验输入，与完整结构潜变量配对形成训练样本对，从而让修复网络学会从局部可见几何推断全局结构。

### 两阶段推理采样

推理阶段采用 $t = 50$ 步采样，分为两个阶段：

- **结构修复阶段**（前 $s = 25$ 步）：保持可见性掩码 $\mathbf{m}_{\mathrm{s}}$ 不变，修复网络在掩码约束下从可见区域推断并补全全局结构。
- **边界细化阶段**（后 $t - s = 25$ 步）：将掩码替换为全 1 掩码 $\mathbf{m}_1$，将修复任务转化为标准去噪过程，以平滑修复边界、消除可能的结构不连续性。

这一分阶段策略的核心洞见在于：纯修复（全程保持掩码）会在边界区域产生几何空洞，而全程标准去噪则会丢失点云先验的硬约束。两阶段结合能够在忠实保留可见几何的同时，实现边界区域的平滑过渡。

### 补充图表

![[assets/figures/papers/paper_list_l2572_https_arxiv_org_abs_2603_18782/figures/003_Figure_3.jpg]]
*Figure 3: Training data processing. We preserve the visible portion of the complete point cloud and convert it into training inputs*

## 实验与分析

### 核心实验设置

实验围绕两个主要任务展开：**单物体3D生成**（Toys4K数据集）和**场景级多物体生成**（3D-FRONT数据集）。评估在两个设定下进行——一是提供精确的真实点云先验（Explicit Priors），二是仅从输入图像通过VGGT前馈预测点云（VGGT Esti.）。所有对比方法在相同训练/测试分割上评估，使用统一的渲染指标（PSNR、SSIM、LPIPS）和几何指标（Chamfer Distance、F-Score）。

### 单物体生成：Toys4K 主结果

Table 1给出了单物体生成的核心定量对比。使用真实点云先验时，Points-to-3D在所有指标上均显著超越基线：

- **渲染质量**：PSNR达到22.91（TRELLIS为21.94，+0.97），SSIM达到92.83（TRELLIS为91.46，+1.37），LPIPS降至0.070（TRELLIS为0.105，-0.035）。这表明点云先验的注入不仅改善了几何，也提升了多视角渲染的一致性。
- **几何精度**：F-Score达到0.963（TRELLIS为0.832，+0.131），Chamfer Distance降至0.013（TRELLIS为0.034，-0.021）。这是全文最关键的证据——将可见点云先验直接编码为结构潜变量并执行潜空间修复，使几何保真度产生了质的飞跃。

当使用VGGT估计的点云（无精确先验）时，Points-to-3D依然在渲染和几何质量上优于TRELLIS等所有不使用显式点云先验的基线。这验证了框架对先验质量具有一定鲁棒性，且即使是不完美的3D线索也能有效引导生成。

### 可见区域保真度：Table 3 的关键发现

Table 3将评估拆分为整体几何与仅可见区域几何。Points-to-3D在可见区域内与真值几乎完全对齐：F-Score达到0.998，Chamfer Distance仅为0.007。这一近乎完美的保真度直接归因于方法的核心机制——通过掩码$m_s$在潜空间中显式保护已知区域，使扩散过程不破坏已观测几何。相比之下，TRELLIS从纯噪声初始化，无法保证生成结果与输入观测的几何一致性。

### 场景级生成：3D-FRONT 主结果

在更复杂的多物体场景生成任务上，Table 2显示了Points-to-3D的压倒性优势。使用点云先验时，PSNR达到21.63（TRELLIS为18.21，+3.42），F-Score达到0.886（TRELLIS为0.478，+0.408）。几何指标上的巨大差距（F-Score提升85%）表明，在场景级生成中，缺乏几何先验的纯生成方法难以恢复合理的空间布局，而Points-to-3D通过注入可见区域结构潜变量，为缺失区域的补全提供了强有力的几何上下文。

### 消融实验：修复步数与细化步数的权衡

Table 4和Figure 6揭示了推理阶段两阶段采样策略的关键作用。总采样步数固定为50步时，**25步修复+25步细化**达到最佳几何性能（CD 0.013, F-Score 0.963, PSNR-N 27.10）：

- **纯修复（50步修复+0步细化）**：虽然能保留可见区域，但边界区域会产生几何空洞。这是因为修复网络仅在掩码约束下运行，边界处缺乏与周围噪声区域的平滑过渡机制。
- **加入细化阶段**：将掩码替换为全1后，模型转化为标准去噪，在最后若干步中对修复边界进行平滑优化。Figure 6的定性结果清晰展示了边界区域质量的显著提升，同时已知区域的几何未被破坏。

这一消融直接验证了方法设计的合理性：修复阶段负责全局结构补全，细化阶段负责边界一致性，两者缺一不可。

### 鲁棒性分析：噪声先验的影响

Table 7（附录B.5）评估了不同噪声水平对生成质量的影响。当向精确点云先验添加不同程度扰动时，生成质量随噪声增大而下降。论文提出了简单的噪声扰动修复策略可部分缓解性能损失，但在高度噪声环境下仍不推荐完全依赖不可靠的3D先验。这一发现与Table 1中VGGT估计结果的鲁棒性形成互补——方法对适度误差具有容忍度，但对严重噪声或大范围缺失的鲁棒性仍是当前瓶颈。

![[assets/figures/papers/paper_list_l2572_https_arxiv_org_abs_2603_18782/figures/025_Table_7.jpg]]
*Table 7: Noisy point cloud priors. We add different levels of perturbation to the accurate point-cloud priors to evaluate the impact of noisy 3D priors, and present the results of our simple repair process for noisy point cloud inputs below*

### 定性结果与对比分析

Figure 4展示了单物体生成的定性对比。使用显式点云先验时，Points-to-3D生成的3D资产在可见区域与输入观测高度一致，在不可见区域给出结构合理的补全。相比之下，TRELLIS等从纯噪声出发的方法无法保证生成结果与输入观测的几何对齐。Figure 5的场景级定性结果进一步印证了Table 2的定量发现——Points-to-3D在多物体场景中保持了空间布局的一致性，而基线方法常出现物体错位或几何失真。

### 与相关方法的公平性讨论

- **与VoxHammer对比**：两者使用相同的3D先验（可见区域提取的点云），但VoxHammer依赖图像条件修复缺失区域，缺乏显式的潜空间修复机制。Points-to-3D通过训练好的修复网络$G_{inp}$直接在结构潜空间中完成补全，因此更充分利用了先验信息。
- **与SAM3D对比**：SAM3D通过注意力机制间接整合点映射，但无法实现显式几何控制。Points-to-3D通过将点云先验直接注入潜空间，实现了更精确的几何可控性，这一点在SAM3D原文中也得到承认。

### 失败模式与局限性

1. **低质量先验退化**：当输入点云存在严重噪声或大范围缺失时，生成质量显著下降。当前方法对不可靠3D先验的鲁棒性有限，高度噪声环境下生成结果可能偏离预期几何。
2. **边界修复的局限**：虽然两阶段采样缓解了边界空洞问题，但在极端遮挡或复杂拓扑变化场景下，修复边界仍可能出现不自然的过渡。
3. **场景泛化未验证**：当前实验集中在物体和室内场景，对于大规模室外场景或高度动态复杂场景的泛化性尚未验证。

### 补充图表

![[assets/figures/papers/paper_list_l2572_https_arxiv_org_abs_2603_18782/figures/004_Table_1.jpg]]
*Table 1: Comparison on single-object generation on Toy4K dataset. We showcase the performance of our method in two scenarios: one where explicit point cloud priors are provided, and another where point cloud are inferred from condition images using VGGT [66]*

![[assets/figures/papers/paper_list_l2572_https_arxiv_org_abs_2603_18782/figures/006_Table_2.jpg]]
*Table 2: Comparison on scene-level generation on 3D-FRONT dataset. Points-to-3D consistently outperforms state-of-the-art multiobject generation methods across all evaluation metrics*

![[assets/figures/papers/paper_list_l2572_https_arxiv_org_abs_2603_18782/figures/010_Table_4.jpg]]
*Table 4: Ablation study. We evaluate the number of inpainting steps (Inp.) and refinement steps (Ref.) in our sampling strategy*

![[assets/figures/papers/paper_list_l2572_https_arxiv_org_abs_2603_18782/figures/005_Figure.jpg]]

![[assets/figures/papers/paper_list_l2572_https_arxiv_org_abs_2603_18782/figures/008_Figure_5.jpg]]
*Figure 5: Scene-level generation on 3D-FRONT. The input point cloud priors setting is the same as in Fig. 4*

![[assets/figures/papers/paper_list_l2572_https_arxiv_org_abs_2603_18782/figures/007_Figure.jpg]]

![[assets/figures/papers/paper_list_l2572_https_arxiv_org_abs_2603_18782/figures/013_Figure_8.jpg]]
*Figure 8: Generation results with 3 input views on Toys4K. The first column of our results uses sampled point-cloud priors extracted from the visible regions of the three input images, whereas the “VGGT-estimated” results rely on point clouds inferred from the input images by VGGT*

![[assets/figures/papers/paper_list_l2572_https_arxiv_org_abs_2603_18782/figures/020_Table_5.jpg]]
*Table 5: Comparison on single-object generation with 3 views input on Toy4K dataset*

## 方法谱系与知识库定位

### 1. 与基础框架的关系

Points-to-3D 直接构建在 **TRELLIS**（Xiang et al., CVPR 2025）的 3D 生成框架之上。TRELLIS 的核心设计是将 3D 资产生成分解为两个阶段：首先在稀疏结构（Sparse Structure, SS）潜空间中通过扩散模型生成二值占据网格，然后在结构化潜变量（Structured Latent, SLAT）空间中生成带颜色与细节的最终资产。TRELLIS 的 SS 潜变量初始化完全来自高斯噪声 $ \boldsymbol{\epsilon}_{\mathrm{s}} $，缺乏将外部几何观测注入生成过程的机制。

Points-to-3D 保留了 TRELLIS 的整体两阶段架构和 SS/SLAT 双 VAE 表示，但对其中的四个关键环节进行了替换与扩展：

- **结构潜变量初始化**：从纯噪声采样改为将可见点云先验体素化后编码为 SS 潜变量 $ \mathbf{q}_{\mathrm{vis}} = \mathcal{E}_s(\mathbf{M}') $，再与噪声通过掩码混合形成修复输入 $ \mathbf{q}_{\mathrm{comb}} = \mathbf{m}_{\mathrm{s}} \odot \mathbf{q}_{\mathrm{vis}} + (1 - \mathbf{m}_{\mathrm{s}}) \odot \boldsymbol{\epsilon}_{\mathrm{s}} $。
- **生成网络输入通道**：将 TRELLIS 原始稀疏结构流 Transformer $ \mathcal{G}_s $ 的输入层替换为扩展通道的投影层，以接收拼接了掩码的输入 $ \mathbf{x}_{\mathrm{inp}} = \operatorname{Concat}[\mathbf{q}_{\mathrm{comb}}, \mathbf{m}_{\mathrm{s}}] $，形成修复网络 $ \mathcal{G}_{inp} $。
- **训练数据构造**：从使用完整资产潜变量进行无条件扩散训练，改为通过多视角渲染与深度一致性检查构建可见点云-完整结构潜变量对，进行条件修复训练。
- **推理采样策略**：从全程标准去噪改为两阶段采样——前 $ s $ 步保持掩码进行结构修复，后 $ t-s $ 步将掩码替换为全 1 转化为标准去噪以细化边界。

这一改造的核心洞察在于：将 3D 生成重新定义为潜空间修复问题，使得可见区域的几何被硬约束保留，而不可见区域的生成由修复网络从可见上下文推断完成。

### 2. 与同类 3D 生成方法的对比定位

**与单物体生成方法的对比**

在 Toys4K 单物体生成基准上，Points-to-3D 与 **GaussianAnything**、**Real3D**、**LGM**（Tang et al., ECCV 2024）等方法进行了对比。这些方法均未显式利用点云先验作为几何约束。Table 1 的结果显示，当提供真实点云先验时，Points-to-3D 在几何指标上取得 F-Score 0.963，显著优于 TRELLIS 的 0.832，且在渲染质量（PSNR 22.91 vs. 21.94）上也全面领先。即使使用 **VGGT** 估计的点云（无精确先验），Points-to-3D 依然在渲染和几何质量上优于所有不使用显式点云先验的基线。

**与利用 3D 先验的方法对比**

- **VoxHammer**：该方法同样使用可见区域提取的点云作为 3D 先验，但依赖图像条件来修复缺失区域，缺乏明确的潜空间修复机制。Points-to-3D 通过训练专用的修复网络 $ \mathcal{G}_{inp} $ 直接在 SS 潜空间中进行条件修复，更充分地利用了先验信息。对比的公平性在于两者使用了相同的 3D 先验来源。
- **SAM3D**：该方法通过注意力机制间接整合点映射，但无法实现显式的几何控制。Points-to-3D 通过将点云先验直接注入潜空间，实现了更精确的几何可控性——这一点在 SAM3D 的论文中也得到承认。

**与场景级多物体生成方法的对比**

在 3D-FRONT 场景级生成基准上，Points-to-3D 与 **MIDI**、**SceneGen** 等方法进行了对比。Table 2 显示，Points-to-3D 在几何指标上取得 F-Score 0.886，远超 TRELLIS 的 0.478（提升 +0.408），PSNR 也从 18.21 提升至 21.63（+3.42）。这表明点云先验的注入在复杂多物体场景中带来的几何忠实度增益更为显著。

### 3. 适用边界

Points-to-3D 的适用性受以下条件约束：

- **先验质量依赖**：方法的核心假设是可见区域的点云先验具有足够的几何精度。当输入点云存在严重噪声或大范围缺失时，生成质量会显著下降。虽然简单的噪声扰动修复策略可以部分缓解低质量点云的影响（Table 7, Appendix B.5），但在高度噪声环境下仍不推荐完全依赖不可靠的 3D 先验。
- **场景规模限制**：当前实现和评估主要集中在单物体（Toys4K）和室内场景（3D-FRONT）。对于大规模室外场景或高度动态复杂场景的泛化性尚未验证。
- **表示形式的耦合**：方法深度绑定 TRELLIS 的稀疏结构潜变量表示和两阶段生成架构。若要将点云先验注入机制迁移到其他 3D 表示（如 3D 高斯、NeRF、隐式场），需要重新设计编码和注入方式。

### 4. 局限与开放问题

**当前局限**

1. **对不可靠先验的鲁棒性有限**：VGGT 估计的点云虽然使 Points-to-3D 仍优于不使用先验的基线，但与使用真实点云先验相比性能有明显差距。这表明方法对先验质量的退化缺乏内在的纠错机制。
2. **边界细化依赖于启发式策略**：两阶段采样（25 步修复 + 25 步细化）的步数分配是基于经验设定的（Table 4 的消融实验验证了该配置的最优性），缺乏自适应的步数调整机制。纯修复（50 步）会导致边界区域产生几何空洞，而过度细化可能破坏已知区域的几何保真度。
3. **控制粒度受限**：当前方法只能对“可见/不可见”区域进行二元掩码控制，无法实现细粒度的局部编辑或属性控制。

**开放问题**

1. **细粒度可控生成**：如何将点云先验的几何可控性与文本/图像条件更灵活地结合，实现对特定区域的局部编辑、材质修改或语义属性控制，是一个重要的延伸方向。
2. **与其他 3D 表示的融合**：能否将可见点云先验直接与 3D 高斯或隐式场等表示结合，绕过体素化的离散化损失，提升生成效率和细节保真度？
3. **规模化涌现能力**：在更大规模、更富多样性的训练数据下，基于点云先验的 3D 生成能否涌现出更强的补全与推理能力——例如从极少量可见几何推断出合理的完整结构？
4. **动态与室外场景泛化**：当前框架在静态室内场景上验证有效，向大规模室外场景或包含动态元素的场景扩展时，点云先验的获取、表示和修复机制需要如何调整？

## 原文 PDF

![[paperPDFs/CVPR_2026/Points_to_3D_Structure_Aware_3D_Generation_with_Point_Cloud_Priors.pdf]]