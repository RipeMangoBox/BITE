---
title: "UniRelight: Learning Joint Decomposition and Synthesis for Video Relighting"
type: paper
paper_level: A
venue: NeurIPS
year: 2025
pdf_ref: paperPDFs/NEURIPS_2025/UniRelight_Learning_Joint_Decomposition_and_Synthesis_for_Video_Relighting.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/UniRelight/
aliases:
- UniRelight
tags:
- NEURIPS_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将重光照与反照率解调联合建模，在单一视频扩散Transformer中同时对重光照视频和反照率的潜变量进行去噪，并在序列维度上串联以实现跨模态自注意力交互。"
primary_logic: "反照率解调为重光照任务提供了去除阴影、理解场景本征结构的强先验；联合建模能够隐式学习场景表示，避免显式中间状态的误差积累，并有效建模镜面高光、透明等复杂光照效果。"
claims:
- "联合建模在街景用户研究中相比纯重光照模型被68%±14%的参与者偏好，能正确解调阴影而不会将输入阴影烘焙到重光照结果中。"
- "在MIT多光照真实基准上，我们的方法PSNR达到20.76，显著超过所有基线（次佳为17.87），用户研究中96%±4%的样本更偏向本方法。"
- "仅在合成数据上训练时，联合建模已经将PSNR从纯重光照的26.42提升至26.97，验证了反照率信息对重光照的增益。"
- "加入150k真实世界自动标注的视频数据（仅RGB-反照率配对）显著提升了自然图像上的泛化能力，用户偏好度从45%提升至55%。"
---

# UniRelight: Learning Joint Decomposition and Synthesis for Video Relighting

> [!tip] 核心洞察
> 反照率解调为重光照任务提供了去除阴影、理解场景本征结构的强先验；联合建模能够隐式学习场景表示，避免显式中间状态的误差积累，并有效建模镜面高光、透明等复杂光照效果。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | UniRelight：学习视频重光照的联合分解与合成 |
| 英文题名 | UniRelight: Learning Joint Decomposition and Synthesis for Video Relighting |
| 会议/期刊 | NeurIPS 2025 |
| Links | [paper](https://arxiv.org/abs/2506.15673) · [Project](https://research.nvidia.com/labs/toronto-ai/UniRelight/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | UniRelight |
| Dataset | SyntheticScenes, MIT multi-illumination |

> [!tip] 效果简介
> - SyntheticScenes 上，PSNR↑ 为 26.97，对比 26.61 (DiffusionRenderer Cosmos)，变化 +0.36。
> - SyntheticScenes 上，SSIM↑ 为 0.847，对比 0.841 (DiffusionRenderer Cosmos)，变化 +0.006。
> - SyntheticScenes 上，LPIPS↓ 为 0.190，对比 0.217 (DiffusionRenderer original)，变化 -0.027。

## 概要

视频重光照旨在将输入视频的光照条件迁移到目标光照环境，同时保持场景的内在属性不变。现有方法面临两大核心瓶颈：**两阶段流水线**（先逆渲染分解G‑buffer，再前向渲染合成）容易在中间表示中累积误差，且难以编码各向异性、透明、次表面散射等复杂材质；**端到端方法**则受限于多光照配对数据的稀缺，在真实场景中泛化能力不足。

UniRelight 提出将**重光照与反照率解调联合建模**——在单一视频扩散Transformer（DiT）中同时对重光照视频和反照率的潜变量进行去噪，通过在序列（时间）维度上串联两种模态的潜变量，实现跨模态自注意力交互。核心洞察在于：反照率解调为重光照提供了去除阴影、理解场景本征结构的强先验，联合建模能够隐式学习场景表示，避免显式中间状态的误差积累，并有效建模镜面高光、透明等复杂光照效果。

方法使用三个互补的光照缓冲（LDR全景、归一化对数强度、方向编码）经VAE编码后注入重光照潜变量通道维，并采用混合训练策略——结合大规模合成数据、MIT多光照真实基准以及150k真实世界自动标注视频，配合条件随机丢弃以增强泛化能力。

**主要结果**：在MIT多光照真实基准上，UniRelight的PSNR达到20.76，显著超过所有基线（次佳Neural Gaffer为17.87），用户研究中96%±4%的样本更偏向本方法（Table 1）。在街景用户研究中，联合建模相比纯重光照模型被68%±14%的参与者偏好，能够正确解调阴影而不会将输入阴影烘焙到重光照结果中（Table 4, Figure 5）。仅在合成数据上训练时，联合建模已将PSNR从纯重光照的26.42提升至26.97（Table 3），验证了反照率信息对重光照的内在增益。真实世界自动标注数据的加入进一步将街景用户偏好从45%提升至55%（Table 4, Figure 6）。

**方法定位**：UniRelight 属于基于扩散模型的视频重光照方法，区别于两阶段显式逆渲染管线（如 **DiffusionRenderer** (Liang et al., arXiv 2025)），也不同于仅利用背景上下文提示的单图像重光照方法（如 **IC-Light** (Zhang et al., ICLR 2025)）。其联合去噪架构受 VideoJAM 启发，但将联合建模从运动-外观扩展至本征分解-重光照的跨模态交互。



### 重光照任务的核心挑战

图像与视频重光照（relighting）旨在保持场景本征属性不变的前提下，根据新的光照条件（如HDR环境图）重新合成场景外观。该任务在电影视觉特效、增强现实、虚拟摄影和数据增强等领域具有广泛需求。然而，实现高质量、可泛化的视频重光照面临两大核心瓶颈。

**瓶颈一：两阶段流水线的误差累积。** 传统重光照方法通常遵循“逆渲染—前向渲染”的两阶段范式：首先估计场景的显式物理属性（如几何、材质、光照），形成G-buffer等中间表示；随后基于这些中间表示进行前向渲染合成新光照下的外观。这一范式存在两个根本性困难：（1）逆渲染本身是一个欠定问题，各中间估计步骤的误差会在流水线中累积，最终损害重光照质量；（2）G-buffer等显式表示难以编码复杂材质现象，如各向异性反射、透明物体、次表面散射等，导致这些效果在重光照结果中丢失或失真。

**瓶颈二：端到端方法的泛化困境。** 近年来，基于扩散模型的端到端重光照方法（如**DiLightNet**，Zeng et al., ACM SIGGRAPH 2024；**Neural Gaffer**，Jin et al., CVPR 2025）试图绕过显式逆渲染，直接从输入图像和光照条件映射到重光照结果。这类方法虽然简化了流水线，但受限于多光照配对数据的稀缺——获取同一场景在多种光照下的真值配对数据成本极高，导致模型主要在合成数据上训练，在真实场景中的泛化能力不足。同时，缺乏对场景本征结构（如反照率）的显式建模，使得这些方法难以正确解调输入图像中的阴影，容易将输入阴影“烘焙”到重光照结果中。

### 联合建模的动机与核心洞察

本工作的核心洞察在于：**反照率解调为重光照任务提供了理解场景本征结构的强先验**。反照率（albedo）是场景在均匀光照下的本征颜色，去除了阴影和镜面高光的影响。如果模型能够同时估计反照率并基于新的光照条件合成重光照结果，则反照率信息可以隐式地引导模型区分“场景本身是什么颜色”与“光照造成了什么效果”，从而更准确地解调输入阴影并合成符合新光照条件的阴影与高光。

基于这一洞察，UniRelight提出将重光照与反照率解调**联合建模**：在单一视频扩散Transformer（DiT）中同时对重光照视频和反照率的潜变量进行去噪，通过序列维度上的串联实现跨模态自注意力交互。这一设计具有三重优势：

1. **避免显式中间表示的误差积累**：模型隐式学习场景表示，无需显式估计G-buffer，从而规避了两阶段流水线中的误差累积问题。
2. **有效建模复杂光照效果**：联合潜空间中的跨模态交互使模型能够捕捉镜面高光、透明折射等难以用显式参数编码的复杂光照现象。
3. **利用稀疏标注的真实数据**：即使在仅有RGB-反照率配对（无多光照真值）的真实世界数据上，反照率解调任务也能为重光照提供有效的学习信号，提升真实场景泛化能力。

### 现有方法缺口与本文定位

| 方法范式 | 代表工作 | 核心问题 |
|---------|---------|---------|
| 两阶段（逆渲染+前向渲染） | **DiffusionRenderer** (Liang et al., arXiv 2025) | 显式G-buffer难以编码复杂材质，误差累积严重 |
| 端到端2D扩散重光照 | **DiLightNet** (Zeng et al., SIGGRAPH 2024)、**Neural Gaffer** (Jin et al., CVPR 2025) | 缺乏场景本征建模，易烘焙输入阴影，真实场景泛化不足 |
| 基于背景提示的单图像重光照 | **IC-Light** (Zhang et al., ICLR 2025) | 依赖背景上下文而非完整光照条件，镜面高光与阴影精度有限 |

UniRelight的定位是填补上述缺口：通过联合建模重光照与反照率解调，在一个统一的视频扩散框架中同时获得高质量重光照结果和场景本征分解，并在合成数据与真实世界自动标注数据的混合训练策略下实现更强的泛化能力。



## 核心方法与创新机理

UniRelight 的核心创新在于将重光照与场景本征分解（反照率解调）统一到一个联合扩散框架中，从根本上改变了传统两阶段流水线的设计范式。这一创新通过三个关键的 **changed slots** 实现：

### 1. 联合建模架构：从两阶段到单一DiT

传统方法（如 **DiffusionRenderer**（Liang et al., arXiv 2025））采用显式的两阶段流水线——先进行逆渲染估计G-buffer，再进行前向渲染合成重光照结果。这种方式存在两个根本性问题：**误差累积**（逆渲染的误差会传播到渲染阶段）和**表达能力受限**（G-buffer无法编码各向异性、透明、次表面散射等复杂材质）。

UniRelight 摒弃了显式中间表示，改为在单一视频扩散Transformer（DiT）中**联合去噪**重光照视频潜变量 $`\hat{\mathbf{z}}^{\mathbf{E}}`$ 和反照率潜变量 $`\hat{\mathbf{z}}^{\mathbf{a}}`$。具体而言，将两者的潜变量沿时间维度串联，并通过可学习的**类型嵌入**（type embeddings）与RoPE位置编码叠加来区分三种模态（输入视频、反照率、重光照）。这种设计使自注意力机制能够跨模态交互，隐式地学习场景表示，从而避免显式G-buffer的误差积累，并能有效建模镜面高光、透明等复杂光照效果。

**证据**：Table 3 显示，移除联合建模（仅训练纯重光照模型）后，PSNR从26.97降至26.42；Figure 5 进一步揭示，纯重光照模型会明显将输入阴影“烘焙”到重光照结果中，而联合模型能正确解调阴影。

### 2. 光照编码：三通道互补表示

基线方法通常仅使用LDR环境图或球谐系数作为光照条件，丢失了高动态范围信息和空间方向细节。UniRelight 设计了**三个互补的光照缓冲**：

- **LDR全景图**：提供基础的视觉外观信息
- **归一化对数强度图** $`\mathbf{E}_{\mathrm{log}} = \log(\mathbf{E} + 1) / E_{\mathrm{max}}`$：捕捉HDR环境图中的高动态范围能量分布
- **方向编码**：显式编码光源的空间方向信息

三者分别经VAE编码后沿通道维串联，形成光照特征 $`\mathbf{h}^{\mathbf{E}}`$，再与重光照潜变量 $`\mathbf{z}^{\mathbf{E}}`$ 沿通道维拼接。这种设计使模型能同时感知光照的颜色、强度和方向，为复杂光照效果（如方向性镜面高光、软阴影）的生成提供了充分的输入信息。

### 3. 数据策略：合成-真实混合训练与条件随机丢弃

重光照任务长期受限于多光照配对数据的稀缺。UniRelight 采用**三阶段混合数据策略**：

- **大型合成数据集**（36,500个3D物体、4,260种PBR材质、766个HDRI环境图）提供全监督信号 $`(\mathbf{I}, \mathbf{I}_E, \mathbf{a}, \mathbf{E})`$
- **MIT多光照真实数据集**提供真实场景的配对监督
- **150k真实世界自动标注视频**（仅RGB-反照率配对）增强自然图像的泛化能力

训练中采用**条件随机丢弃策略**（10%概率丢弃条件）以支持无分类器引导。对于合成和MIT数据，还设计了三种条件模式：12%丢弃输入视频、18%同时提供输入视频和真实反照率、70%默认模式。这种策略使模型既能利用合成数据的完整监督，又能从真实数据中学习自然图像分布，同时保持对反照率条件的使用灵活性。

**证据**：Table 4 显示，加入真实世界自动标注数据后，街景用户偏好从45%提升至55%，证明即使标签稀疏，真实数据仍能显著增强泛化能力。

### 创新本质：反照率作为强先验

上述三个 changed slots 共同服务于一个核心洞察：**反照率解调为重光照提供了去除阴影、理解场景本征结构的强先验**。联合建模使反照率估计和重光照合成相互促进——反照率为重光照提供场景材质信息，重光照任务反过来约束反照率解调的准确性。这种双向增益机制是UniRelight在MIT多光照真实基准上PSNR达到20.76（次佳仅17.87）、用户研究中96%±4%样本被偏好的根本原因。



![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2506_15673/figures/015_Figure_10.jpg]]
*Figure 10: Additional qualitative results on real scenes. Our method provides high-quality albedo estimation and realistic relighting results*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2506_15673/figures/001_Figure_1.jpg]]
*Figure 1: Given an input image (top left) or video, our method jointly estimates albedo (bottom left) and synthesizes relit videos with novel lighting conditions using provided HDR probes. Notably, our estimated albedo maps effectively demodulate shadows and specular highlights, while the relit images exhibit plausible shadows and specular highlights*

UniRelight 将视频重光照与场景本征分解统一在一个联合扩散框架内，核心思想是**将反照率解调作为重光照的强先验，让单一视频扩散Transformer同时对重光照视频和反照率的潜变量进行去噪**。这避免了传统两阶段流水线（逆渲染→前向渲染）中显式中间表示（如G-buffer）带来的误差累积，并能隐式学习复杂材质（各向异性、透明、次表面散射等）的光照响应。

### 输入与输出

给定一个输入视频 $\mathbf{I}$ 和目标光照配置，模型同时输出：

- **重光照视频** $\hat{\mathbf{I}}_E$：在新光照条件下渲染的场景外观
- **反照率视频** $\hat{\mathbf{a}}$：去除阴影和镜面高光的场景本征反照率

目标光照配置通过三个互补的光照缓冲表示（Section 4.1）：
1. **LDR全景图** $\mathbf{E}_{\mathrm{ldr}}$：低动态范围环境图，提供基础光照色彩和方向信息
2. **归一化对数强度图** $\mathbf{E}_{\mathrm{log}} = \log(\mathbf{E} + 1) / E_{\mathrm{max}}$：捕捉HDR环境图中的高动态范围能量分布
3. **方向编码图** $\mathbf{E}_{\mathrm{dir}}$：编码每个像素的入射方向信息

### 整体流水线

整个框架围绕**预训练的Cosmos视频扩散骨干**构建，流水线包含以下关键模块（Figure 2）：

**1. VAE潜空间编码（Cosmos-1.0-Tokenizer-CV8x8x8）**

所有视觉信号通过预训练的VAE编码器 $\mathcal{E}$ 映射到统一潜空间。该tokenizer在时空维度上执行8倍压缩，输出通道数为16，即对于输入尺寸 $L \times H \times W$，潜变量尺寸为 $l \times C \times h \times w$，其中 $l = L/8$，$C = 16$，$h = H/8$，$w = W/8$（Section 3）。具体编码对象包括：
- 输入视频 $\mathbf{I}$ → 潜变量 $\mathbf{z}^{\mathbf{I}}$
- 目标重光照视频（训练时） → 潜变量 $\mathbf{z}_0^{\mathbf{E}}$
- 反照率视频 → 潜变量 $\mathbf{z}_0^{\mathbf{a}}$
- 三个光照缓冲分别经VAE编码后沿通道维串联 → 光照特征 $\mathbf{h}^{\mathbf{E}} = (\mathcal{E}(\mathbf{E}_{\mathrm{ldr}}), \mathcal{E}(\mathbf{E}_{\mathrm{log}}), \mathcal{E}(\mathbf{E}_{\mathrm{dir}}))$

**2. 潜变量时序串联与类型嵌入**

这是联合建模的核心设计（Section 4.1）：将重光照视频潜变量 $\mathbf{z}^{\mathbf{E}}$、反照率潜变量 $\mathbf{z}^{\mathbf{a}}$ 和输入视频潜变量 $\mathbf{z}^{\mathbf{I}}$ **沿时间（帧）维度串联**，形成一个扩展的序列。这种串联方式使得DiT模型中的自注意力机制能够跨模态交互——重光照帧可以"看到"对应的反照率帧和输入帧，从而隐式学习场景本征结构与光照效果之间的映射关系。

为区分序列中不同模态的帧，引入**可学习的类型嵌入** $\mathbf{c}_{\mathrm{emb}} \in \mathbb{R}^{K_{\mathrm{emb}} \times C_{\mathrm{emb}}}$（$K_{\mathrm{emb}}=3$，对应输入视频、反照率、重光照三种模态），与标准的RoPE位置编码叠加使用。同时，使用**二值条件掩码**标记每一帧是条件帧（输入视频/反照率）还是去噪目标帧（重光照/反照率）。

**3. 光照特征注入**

光照特征 $\mathbf{h}^{\mathbf{E}}$ 沿**通道维度**与重光照视频潜变量 $\mathbf{z}^{\mathbf{E}}$ 串联，使光照信息直接参与重光照潜变量的去噪过程（Figure 2）。这种设计确保模型能精确感知目标光照环境的空间分布和强度特征。

**4. 联合DiT去噪（Cosmos-Predict1-7B-Video2World）**

核心去噪函数定义为（Equation 1）：

$$\hat{\mathbf{z}}^{\mathbf{E}}(\theta), \hat{\mathbf{z}}^{\mathbf{a}}(\theta) = \mathbf{f}_\theta([\mathbf{z}_\tau^{\mathbf{E}} + \mathbf{h}^{\mathbf{E}}, \mathbf{z}_\tau^{\mathbf{a}}, \mathbf{z}^{\mathbf{I}}]; \mathbf{c}_{\mathrm{emb}}, \tau)$$

其中 $\tau$ 为噪声时间步，$\mathbf{f}_\theta$ 为微调的DiT视频模型。模型从带噪的重光照潜变量（已注入光照特征）、带噪的反照率潜变量和干净的输入视频潜变量中，**同时预测去噪后的重光照潜变量和反照率潜变量**。这一联合去噪过程使得反照率解调与重光照合成相互促进：反照率估计受益于多光照条件提供的本征线索，而重光照合成则利用反照率信息避免将输入阴影烘焙到输出中。

**5. VAE解码**

去噪后的潜变量 $\hat{\mathbf{z}}^{\mathbf{E}}$ 和 $\hat{\mathbf{z}}^{\mathbf{a}}$ 通过预训练的VAE解码器 $\mathcal{D}$ 分别重建为重光照视频 $\hat{\mathbf{I}}_E$ 和反照率视频 $\hat{\mathbf{a}}$。

### 训练损失

模型通过均方误差损失进行端到端训练（Equation 2）：

$$\mathcal{L}(\boldsymbol{\theta}) = \mathbb{E}_{(\mathbf{z}_0^{\mathbf{E}}, \mathbf{z}_0^{\mathbf{a}}) \sim p_{\mathrm{data}}, \epsilon \sim \mathcal{N}(0, \sigma^2 I)} \left[ \|\hat{\mathbf{z}}^{\mathbf{E}}(\boldsymbol{\theta}) - \mathbf{z}_0^{\mathbf{E}}\|_2^2 + \lambda_{\mathbf{a}} \|\hat{\mathbf{z}}^{\mathbf{a}}(\boldsymbol{\theta}) - \mathbf{z}_0^{\mathbf{a}}\|_2^2 \right]$$

其中反照率损失权重 $\lambda_{\mathbf{a}} = 0.1$，用于平衡两个任务的训练动态。训练数据采用混合策略：合成多光照数据提供完整监督（输入视频、重光照结果、反照率、环境图四元组），MIT多光照真实数据集提供真实场景的配对监督，以及150k真实世界自动标注视频（仅RGB-反照率配对）增强泛化能力（Section 4.2-4.3）。训练时采用10%概率的条件随机丢弃策略，以支持推理时的无分类器引导。

### 关键设计决策

- **单次去噪 vs 两阶段**：传统方法（如**DiffusionRenderer**，Liang et al., arXiv 2025）先逆渲染估计G-buffer再前向渲染，G-buffer无法编码复杂材质且误差会级联放大。UniRelight在单一DiT中完成全部推理，隐式学习场景表示，避免了显式中间状态的瓶颈。
- **时序串联 vs 通道串联**：将不同模态沿时间维串联而非通道维，充分利用了DiT的自注意力机制进行跨模态信息融合，使反照率帧和重光照帧能够直接交互。
- **三通道光照编码 vs 单一LDR**：相比仅使用LDR环境图的基线（如**DiLightNet**，Zeng et al., ACM SIGGRAPH 2024），三缓冲设计同时保留了色彩、强度和方向信息，使模型能更精确地推理高动态范围光照下的镜面高光和阴影。



### 问题形式化与潜空间映射

UniRelight 将视频重光照与反照率解调统一为联合去噪问题。给定输入视频 $\mathbf{I} \in \mathbb{R}^{L \times H \times W \times 3}$ 和目标光照配置（以 HDR 环境图表示），模型需同时预测重光照视频 $\hat{\mathbf{I}}_E$ 及其对应的反照率图 $\hat{\mathbf{a}}$。

所有视频与图像均通过预训练的 **Cosmos-1.0-Tokenizer-CV8x8x8** VAE 编码器 $\mathcal{E}$ 映射到统一潜空间，压缩因子为：

$$l = \frac{L}{8}, \quad C = 16, \quad h = \frac{H}{8}, \quad w = \frac{W}{8}$$

其中 $L$ 为帧数，$H \times W$ 为空间分辨率，$C$ 为潜变量通道数。解码器 $\mathcal{D}$ 负责将去噪后的潜变量重建为像素空间视频。

### 光照编码模块

为充分捕捉 HDR 环境图的高动态范围与空间分布信息，本方法采用三个互补光照缓冲作为光照表示（Section 4.1）：

1. **LDR 全景图** $\mathbf{E}_{\mathrm{ldr}}$：经色调映射的低动态范围表示，提供场景光照的直观外观信息。
2. **归一化对数强度图** $\mathbf{E}_{\mathrm{log}}$：定义为

$$\mathbf{E}_{\mathrm{log}} = \log(\mathbf{E} + 1) / E_{\mathrm{max}}$$

其中 $E_{\mathrm{max}}$ 为最大强度值，该表示保留 HDR 光源的绝对亮度差异，对镜面高光建模至关重要。

3. **方向编码** $\mathbf{E}_{\mathrm{dir}}$：对环境图的每个像素方向进行编码，提供光源的空间位置先验。

三种表示分别经 VAE 编码器处理后沿通道维串联，形成光照特征 $\mathbf{h}^{\mathbf{E}}$：

$$\mathbf{h}^{\mathbf{E}} = (\mathcal{E}(\mathbf{E}_{\mathrm{ldr}}), \mathcal{E}(\mathbf{E}_{\mathrm{log}}), \bar{\mathcal{E}}(\mathbf{E}_{\mathrm{dir}}))$$

该特征随后与重光照视频的噪声潜变量 $\mathbf{z}_\tau^{\mathbf{E}}$ 沿通道维拼接，注入光照条件。

### 联合去噪架构

核心创新在于将重光照与反照率解调建模为单一扩散 Transformer（DiT，基于 **Cosmos-Predict1-7B-Video2World** 骨干）中的联合去噪任务。具体而言（Section 4.1）：

- 将重光照视频潜变量 $\mathbf{z}^{\mathbf{E}}$、反照率潜变量 $\mathbf{z}^{\mathbf{a}}$ 和输入视频潜变量 $\mathbf{z}^{\mathbf{I}}$ 沿**时间（帧）维度**串联为一个联合序列。
- 引入可学习的**类型嵌入** $\mathbf{c}_{\mathrm{emb}} \in \mathbb{R}^{K_{\mathrm{emb}} \times C_{\mathrm{emb}}}$（$K_{\mathrm{emb}}=3$，对应输入视频、反照率、重光照三种模态），与标准 RoPE 位置编码叠加，使模型在自注意力计算中区分不同模态的 token。
- 使用**二值条件掩码**标识序列中每一帧是条件帧（输入视频/反照率）还是去噪目标帧（重光照/反照率）。

联合去噪函数定义为：

$$\hat{\mathbf{z}}^{\mathbf{E}}(\theta), \hat{\mathbf{z}}^{\mathbf{a}}(\theta) = \mathbf{f}_\theta([\mathbf{z}_\tau^{\mathbf{E}} + \mathbf{h}^{\mathbf{E}}, \mathbf{z}_\tau^{\mathbf{a}}, \mathbf{z}^{\mathbf{I}}]; \mathbf{c}_{\mathrm{emb}}, \tau)$$

其中 $\tau$ 为噪声时间步，$\mathbf{f}_\theta$ 为 DiT 模型。该函数从带噪的重光照潜变量（已注入光照特征）、带噪的反照率潜变量以及干净的输入视频潜变量中，同时预测去噪后的重光照与反照率潜变量。

### 训练损失函数

模型通过均方误差损失进行端到端训练，对反照率项施加权重 $\lambda_{\mathbf{a}} = 0.1$ 以平衡两个任务的梯度尺度：

$$\mathcal{L}(\boldsymbol{\theta}) = \mathbb{E}_{(\mathbf{z}_0^{\mathbf{E}}, \mathbf{z}_0^{\mathbf{a}}) \sim p_{\mathrm{data}}, \epsilon \sim \mathcal{N}(0, \sigma^2 I)} \left[ \|\hat{\mathbf{z}}^{\mathbf{E}}(\boldsymbol{\theta}) - \mathbf{z}_0^{\mathbf{E}}\|_2^2 + \lambda_{\mathbf{a}} \|\hat{\mathbf{z}}^{\mathbf{a}}(\boldsymbol{\theta}) - \mathbf{z}_0^{\mathbf{a}}\|_2^2 \right]$$

### 纯重光照消融变体

在消融实验中（Section 5.2），移除联合建模的纯重光照模型将去噪函数简化为：

$$\mathbf{f}_{\theta}([\mathbf{z}_{\tau}^{\mathbf{E}} + \bar{\mathbf{h}}^{\mathbf{E}}]; \mathbf{z}^{\mathbf{I}}, \bar{\tau})$$

该变体不再预测反照率，仅以输入视频为条件对重光照潜变量去噪。实验表明，该简化导致 PSNR 从 26.97 降至 26.42，且在街景数据中明显将输入阴影烘焙到重光照结果中（Table 3, Figure 5），验证了联合建模的必要性。



## 实验与关键发现

### 主实验结果

UniRelight 在两个核心基准上进行了全面评估：合成数据集 **SyntheticScenes** 和真实世界多光照数据集 **MIT multi-illumination**。评估指标包括 PSNR、SSIM、LPIPS 以及用户偏好研究。

在 SyntheticScenes 上，UniRelight 取得了 PSNR 26.97、SSIM 0.847、LPIPS 0.190 的成绩，全面超越了使用相同 Cosmos 视频扩散骨干重实现的强基线 **DiffusionRenderer (Cosmos)**（PSNR 26.61、SSIM 0.841）以及原始 **DiffusionRenderer**（LPIPS 0.217）。这一提升验证了联合建模框架在合成域内的有效性。

在更具挑战性的 MIT multi-illumination 真实基准上，UniRelight 的优势更加显著：PSNR 达到 20.76，远超次佳方法 **Neural Gaffer** 的 17.87（Δ +2.89），SSIM 也从 0.683 提升至 0.749。用户研究进一步印证了这一结论——与 **DiLightNet** 相比，92%±8% 的样本更偏好 UniRelight；与 **Neural Gaffer** 相比为 84%±2%；与 **DiffusionRenderer** 相比则高达 96%±4%。这些结果表明，UniRelight 在面对真实世界复杂材质（如各向异性、透明表面）时具有显著的泛化优势。

在反照率估计任务上，UniRelight 在 SyntheticScenes 上取得了 PSNR 28.07，与专用反照率估计基线 **IntrinsicImageDiffusion** 性能相当（PSNR 28.56），说明联合建模并未牺牲本征分解的质量。

### 消融实验

**联合建模的核心作用。** 移除联合建模（仅训练纯重光照模型）导致 SyntheticScenes 上的 PSNR 从 26.97 下降至 26.42。更关键的是，在街景数据上的定性对比（Figure 5）显示，纯重光照模型会将输入图像中的阴影“烘焙”到重光照结果中，而联合模型能正确解调阴影。用户研究量化了这一差异：在街景场景中，仅 32% 的样本偏好纯重光照模型，68%±14% 的参与者偏好联合建模版本。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2506_15673/figures/006_Figure_5.jpg]]
*Figure 5: Ablation on joint modeling. Relighting results on urban street scenes. The orange and green crops highlight regions where the pure relighting model (w/o joint modeling) clearly bakes shadows from the input image into the relit result. Our joint model correctly demodulates the shadows*

**真实世界自动标注数据的增益。** 在仅使用合成数据训练的基线上加入 150k 真实世界自动标注视频（仅提供 RGB-反照率配对，无多光照标签）后，街景用户偏好从 45% 提升至 55%（Table 4, Figure 6）。尽管标签稀疏，这些数据仍显著增强了模型在自然图像上的泛化能力。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2506_15673/figures/010_Table_3.jpg]]
*Table 3: Ablations on joint model- Table 4: User study of relighting on StreetScenes. Each row compares ing designs evaluated on the Synthet- an ablated variant against the base version (Ours w/o auto-labeled data), icScenes dataset. reporting percentage of samples where users prefer the base version*

**反照率作为附加条件的上限。** 当提供真实反照率作为附加条件时，重光照 PSNR 进一步提升至 27.24（vs 26.97），表明模型能够有效利用反照率信息，且联合建模框架的上限更高。

### 失败模式与局限性

尽管 UniRelight 在整体性能上表现优异，但仍存在以下局限：

1. **发光物体处理缺失。** 当前方法无法处理场景内包含发光物体（如可开关的灯具）的情况，因为模型将光照视为完全由外部 HDR 环境图决定。
2. **文本控制不支持。** 不支持基于自然语言的重光照控制，无法通过文本描述指定光照条件。
3. **推理速度。** 推理耗时虽快于两阶段基线 **DiffusionRenderer**（445 秒/57 帧 vs 基线更长），但仍难以满足实时或交互式应用需求（Table 6）。
4. **合成数据偏差。** 模型训练依赖于合成数据，可能导致渲染风格的偏差；真实世界自动标注数据可能引入标签误差。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2506_15673/figures/011_Table_6.jpg]]
*Table 6: Evaluation of inference runtime cost*

### 重要图表结论

- **Table 1** 是核心定量证据，展示了 UniRelight 在合成和真实基准上全面超越所有基线，尤其在 MIT multi-illumination 上的 PSNR 领先幅度达 2.89 dB，用户偏好度均显著高于 50% 随机概率。
- **Figure 5** 直观揭示了联合建模的关键价值：纯重光照模型会烘焙输入阴影，而联合模型通过反照率解调正确移除了原始光照痕迹。
- **Figure 6** 和 **Table 4** 共同证明了真实世界自动标注数据的有效性——即使标签稀疏，也能提升自然场景的泛化能力。
- **Table 3** 的消融数据表明，联合建模带来的 PSNR 增益（+0.55）虽在合成域内看似温和，但其对阴影解调和真实场景泛化的影响在用户研究中被显著放大。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2506_15673/figures/005_Table_1.jpg]]
*Table 1: Quantitative evaluation of relighting, including a user study, where "Ours preferred" indicates the preference over the baselines. A preference over the> 50% indicates Ours outperforming baselines*

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2506_15673/figures/007_Table.jpg]]

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2506_15673/figures/012_Table_5.jpg]]
*Table 5: Quantitative comparison with IC-Light*



## 定位与知识库关联

### 1. 与现有工作的关系

UniRelight 的核心贡献在于将视频重光照任务从传统的两阶段流水线或单阶段端到端映射，推进到**联合本征分解与重光照合成的生成式建模框架**。这一设计直接回应了现有方法的两大结构性缺陷：显式中间表示（如 G-buffer）对复杂材质的表达能力不足，以及多光照配对数据稀缺导致的泛化瓶颈。

**与两阶段方法的对比。** 以 **DiffusionRenderer**（Liang et al., arXiv 2025）为代表的两阶段方法遵循“逆渲染→前向渲染”范式，先估计 G-buffer（反照率、法线、粗糙度等），再以此为条件合成重光照结果。这一管线存在误差累积问题：逆渲染阶段的错误会不可逆地传入前向渲染阶段。更重要的是，G-buffer 作为显式中间表示，天然无法编码各向异性反射、次表面散射、透明材质等复杂光学现象。UniRelight 通过**隐式联合建模**绕过了这一限制——反照率和重光照视频的潜变量在 DiT 模型中通过自注意力交互，无需显式定义材质表示，从而能够建模镜面高光、透明物体等 G-buffer 难以描述的效果。在 MIT 多光照真实基准上，UniRelight 的 PSNR 达到 20.76，显著超过 DiffusionRenderer 的 17.87，用户研究中 96%±4% 的样本更偏向本方法（Table 1），定量印证了隐式联合建模对复杂材质的处理优势。

**与端到端扩散方法的对比。** **DiLightNet**（Zeng et al., ACM SIGGRAPH 2024）和 **Neural Gaffer**（Jin et al., CVPR 2025）均采用扩散模型直接学习从输入图像到重光照结果的映射，避免显式逆渲染。然而，这类方法受限于多光照配对数据的规模，在真实场景中的泛化能力有限。UniRelight 同样基于扩散模型，但关键区别在于：（1）通过联合反照率解调任务引入场景本征结构的强先验，使模型能够理解阴影与材质的分离，而非简单记忆光照变换模式；（2）引入 150k 真实世界自动标注视频数据（仅需 RGB-反照率配对，无需多光照标注），大幅提升了自然图像上的泛化能力。在街景用户研究中，加入真实数据后用户偏好度从 45% 提升至 55%（Table 4），验证了这一数据策略的有效性。

**与单图像重光照方法的对比。** **IC-Light**（Zhang et al., ICLR 2025）通过背景上下文提示实现单图像重光照，但缺乏对场景本征结构的显式建模。UniRelight 在定量对比中表现更优（Table 5），定性结果显示本方法能产生更精确的镜面高光与阴影（Figure 8）。此外，UniRelight 天然支持视频输入，保持了时序一致性，而 IC-Light 作为单图像方法需要逐帧处理。

**与反照率估计方法的对比。** 在反照率估计这一子任务上，UniRelight 与专门的单图像反照率估计方法 **IntrinsicImageDiffusion**（Kocsis et al., CVPR 2024）相比，PSNR 为 28.07 vs 28.56（Table 2），略低但处于同一水平。考虑到 UniRelight 并非专门优化反照率估计，而是在重光照任务中联合学习，这一结果说明联合建模并未牺牲反照率质量，同时获得了重光照能力的显著增益。

### 2. 适用边界与局限

UniRelight 的设计假设决定了其适用边界：

**支持的场景类型。** 方法适用于以 HDR 环境图作为唯一光源的场景，能够处理室外自然光、室内环境光等全局光照条件。对于包含**发光物体**（如可开关的灯具、显示屏）的场景，当前方法无法处理——模型不具备对场景内独立光源的显式控制能力。

**光照控制粒度。** 光照条件通过 HDR 环境图指定，支持连续的光照变换，但不支持**自然语言文本控制**（如“让场景看起来像黄昏”）。这是与语言驱动的图像编辑方法的重要功能差距。

**材质覆盖范围。** 联合建模能够隐式处理镜面高光、透明材质等复杂效果，但对于极端各向异性材质（如拉丝金属、碳纤维）或强次表面散射材质（如大理石、皮肤），模型的表现受限于训练数据的覆盖范围。合成数据集中包含 4,260 种 PBR 材质，但真实世界中更复杂的材质可能超出分布。

**推理效率。** 推理耗时 445 秒/57 帧（Table 6），虽快于两阶段的 DiffusionRenderer，但仍远未达到实时交互要求。这限制了方法在视频编辑工具中的即时预览场景。

**训练数据偏差。** 模型在合成数据上训练，渲染引擎的物理模型与真实世界存在差距，可能导致渲染风格偏差。真实世界自动标注数据虽缓解了泛化问题，但其反照率标签由预训练模型估计，可能引入系统性误差。

### 3. 开放问题

UniRelight 的架构和数据策略为以下方向提供了自然延伸空间：

1. **场景内动态光源控制。** 如何扩展模型以支持场景中发光物体的独立开关与强度调节？这可能需要将光源表示从单一环境图扩展为包含局部光源的混合表示，并在条件机制中增加光源掩膜或空间位置编码。

2. **文本到重光照的语义控制。** 能否结合自然语言条件实现“使场景变暗并增加暖色调”这类语义级控制？这需要将文本嵌入与现有的光照缓冲表示融合，可能通过交叉注意力机制注入 DiT 模型。

3. **推理加速。** 当前 445 秒的推理时间主要受限于 DiT 模型的多步去噪过程。蒸馏、一致性模型、或减少去噪步数的调度策略是可能的加速路径，但需验证对重光照质量和时序一致性的影响。

4. **联合建模框架的泛化。** 当前的联合去噪框架将反照率作为辅助任务。这一设计是否可推广到其他逆渲染输出（如法线图、深度图、粗糙度图）？如果能够联合估计多种本征属性，模型可能学习到更完整的场景表示，进一步提升重光照质量。这本质上是在探索“以多任务逆渲染驱动前向渲染”的通用框架。

5. **真实世界数据质量闭环。** 当前真实世界自动标注数据依赖预训练模型估计反照率，标签噪声可能限制性能上限。能否通过自监督或半监督策略，在重光照任务本身的信号（如重光照一致性）上构建质量闭环，逐步优化反照率标签？



## 原文 PDF

![[paperPDFs/NEURIPS_2025/UniRelight_Learning_Joint_Decomposition_and_Synthesis_for_Video_Relighting.pdf]]
