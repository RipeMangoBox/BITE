---
title: "DiffusionRenderer: Neural Inverse and Forward Rendering with Video Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/DiffusionRenderer_Neural_Inverse_and_Forward_Rendering_with_Video_Diffusion_Models.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/DiffusionRenderer/
aliases:
- DiffusionRenderer
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将环境光照信息通过专用的环境光编码器提取多分辨率特征，并通过交叉注意力机制注入视频扩散UNet，替代简单的拼接方式，从而更好地保留高动态范围和方向信息，提升渲染一致性。"
primary_logic: "同一个视频扩散模型框架可同时用于神经逆渲染（从视频估计G-buffer）与前向渲染（根据G-buffer和光照生成逼真图像），无需显式路径追踪或精确3D表示；通过合成数据训练逆渲染模型自动为真实视频标注G-buffer，再联合合成与标注数据训练前向模型，有效弥合域间差距。"
claims:
- "在SyntheticScenes复杂场景上，本方法的前向渲染PSNR（26.0 dB）远超最优神经基线RGB↔X（18.5 dB），并在SyntheticObjects上与经典SSRT方法相当，证明了对复杂光照效果的神经逼近能力。"
- "视频扩散模型相比单帧图像模型，在逆渲染中显著降低了金属度RMSE（0.066→0.039，降低41%）和粗糙度RMSE（0.098→0.078，降低20%），证明了时序信息对材质估计的重要性。"
- "联合训练中加入真实世界自适应LoRA模块，在复杂真实场景（如树木）中大幅提升重光照质量，消除了仅合成训练的域偏差。"
- "SyntheticObjects 上 PSNR / SSIM / LPIPS (Neural Forward Rendering) = 28.3 / 0.935 / 0.048"
---

# DiffusionRenderer: Neural Inverse and Forward Rendering with Video Diffusion Models

> [!tip] 核心洞察
> 同一个视频扩散模型框架可同时用于神经逆渲染（从视频估计G-buffer）与前向渲染（根据G-buffer和光照生成逼真图像），无需显式路径追踪或精确3D表示；通过合成数据训练逆渲染模型自动为真实视频标注G-buffer，再联合合成与标注数据训练前向模型，有效弥合域间差距。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DiffusionRenderer：基于视频扩散模型的神经逆渲染与前向渲染 |
| 英文题名 | DiffusionRenderer: Neural Inverse and Forward Rendering with Video Diffusion Models |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2501.18590); [Project](https://research.nvidia.com/labs/toronto-ai/DiffusionRenderer/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DiffusionRenderer |
| Dataset | SyntheticObjects, SyntheticScenes |

> [!tip] 效果简介
> - SyntheticObjects 上，PSNR / SSIM / LPIPS (Neural Forward Rendering) 为 28.3 / 0.935 / 0.048，对比 RGB←X: 25.2 / 0.896 / 0.077，变化 +3.1 / +0.039 / -0.029。
> - SyntheticScenes 上，PSNR / SSIM / LPIPS (Neural Forward Rendering) 为 26.0 / 0.780 / 0.201，对比 RGB←X: 18.5 / 0.645 / 0.302，变化 +7.5 / +0.135 / -0.101。
> - SyntheticScenes 上，PSNR / SSIM / LPIPS (Relighting) 为 24.63 / 0.756 / 0.257，对比 DiLightNet: 18.88 / 0.576 / 0.344，变化 +5.75 / +0.180 / -0.087。

## 概述

**DiffusionRenderer** 提出一个统一的视频扩散模型框架，同时解决神经逆渲染与前向渲染两个任务。其核心洞察在于：同一个视频扩散模型既可以作为神经逆渲染器（从RGB视频估计法线、深度、漫反射、粗糙度、金属度等G-buffer），也可以作为神经前向渲染器（根据G-buffer与目标环境光图生成逼真图像），从而绕开传统物理渲染对精确3D几何与高质量材质、光照的严苛依赖。

**核心瓶颈**：传统物理渲染（如路径追踪、SSRT）需要精确的3D网格或完整的G-buffer，这在真实场景中难以获取；现有的学习方法（如RGB↔X、DiLightNet）在真实世界泛化性、渲染质量和数据稀缺性上存在明显不足，难以支撑复杂的重光照与编辑任务。

**关键机制**：方法通过三个设计弥合合成-真实域差距并提升渲染质量。其一，设计专用的环境光编码器，将环境光图提取为多分辨率特征，并通过交叉注意力注入视频扩散UNet，替代简单的通道拼接，从而更好地保留高动态范围与方向信息。其二，采用视频扩散模型（基于Stable Video Diffusion）替代单帧图像模型，利用时序信息显著提升材质估计精度。其三，构建真实视频自动标注流水线——先以合成数据训练逆渲染器，再用其为DL3DV10k真实视频自动标注G-buffer与光照标签，最后联合合成数据与标注数据训练前向渲染器，并对真实数据引入可训练的LoRA适配器以缓解域偏差。

**主要结果**：在SyntheticScenes复杂场景上，前向渲染PSNR达26.0 dB，远超最优神经基线RGB↔X的18.5 dB（+7.5 dB）；在SyntheticObjects上与经典SSRT方法相当（28.3 vs 29.4）。视频模型相比图像模型使逆渲染金属度RMSE降低41%（0.066→0.039），粗糙度RMSE降低20%（0.098→0.078）。联合训练中加入真实数据与LoRA后，复杂真实场景（如树木）的重光照质量大幅提升，消除了仅合成训练的域偏差。

**方法定位**：DiffusionRenderer 属于神经渲染方法谱系，与基于图像扩散模型的RGB↔X、DiLightNet，以及经典物理渲染的SSRT、SplitSum形成对比。其独特之处在于以视频扩散模型统一逆渲染与前向渲染，无需显式路径追踪或精确3D表示，并通过合成-真实联合训练策略实现向真实场景的有效泛化。

## 背景与动机

### 问题背景：物理渲染的瓶颈

真实感图像合成与编辑的核心在于模拟光线与场景的交互。经典的基于物理的渲染（Physically Based Rendering, PBR）方法严格遵循渲染方程：

$$L_o(\mathbf{p},\omega_o) = \int_\Omega f_r(\mathbf{p},\omega_o,\omega_i) L_i(\mathbf{p},\omega_i) |\mathbf{n}\cdot\omega_i| d\omega_i$$

该方程描述了表面点 $\mathbf{p}$ 在方向 $\omega_o$ 的出射辐亮度，为双向反射分布函数（BRDF）$f_r$、入射辐亮度 $L_i$ 与余弦项的半球积分。要精确求解此方程，需要完备的三维几何表示（如网格模型）、高质量的材质参数（法线、粗糙度、金属度、反照率等G-buffer）以及准确的环境光照信息。

然而，在真实场景中，这些先决条件往往难以同时满足。**Figure 2** 直观展示了这一困境：当显式三维几何不可用时，屏幕空间光线追踪（SSRT）难以准确表达阴影和反射效果；即便通过逆渲染模型估计出G-buffer，微小的估计误差也会在PBR管线中被放大，导致渲染质量急剧下降。这一根本性瓶颈限制了传统渲染技术在真实世界图像编辑、重光照和物体插入等应用中的可行性。

### 现有方法的缺口

近年来，基于学习的方法尝试绕开显式物理模拟，直接从数据中学习渲染映射。然而，这些方法普遍面临三重挑战：

**域泛化不足**。现有神经渲染与逆渲染模型（如基于单帧图像扩散模型的**RGB↔X**、重光照模型**DiLightNet**、**Neural Gaffer**等）大多在合成数据上训练，面对真实场景中的复杂几何、材质多样性和光照变化时，渲染质量显著下降。合成域与真实域之间的鸿沟成为制约实用化的关键瓶颈。

**数据稀缺性**。真实场景的G-buffer真值标注极度稀缺，难以获取大规模、高质量的训练数据。这迫使现有方法要么局限于合成域，要么在真实场景中表现不稳定。

**渲染质量与复杂效果的折衷**。经典PBR近似方法（如**SplitSum**）计算高效，但难以捕捉互反射、软阴影等全局光照效果。而基于图像扩散模型的方法虽能生成逼真图像，却缺乏对场景内在属性（几何、材质）的显式建模，导致在重光照和材质编辑任务中缺乏一致性和可控性。

### 本文动机

上述缺口揭示了一个核心矛盾：**传统物理渲染依赖难以获取的精确场景表示，而现有学习方法又缺乏足够的真实世界泛化能力和物理一致性**。

本文的出发点是探索一种新的范式——能否用同一个学习框架同时解决逆渲染（从视频估计G-buffer）和前向渲染（根据G-buffer和光照生成逼真图像），从而在无需显式路径追踪或精确三维表示的前提下，实现高质量的重光照与编辑？这一思路的关键洞察在于：视频扩散模型天然具备建模时序一致性和复杂条件分布的能力，若能将环境光照信息有效注入生成过程，并利用合成数据训练的逆渲染模型为真实视频自动标注，便有望弥合域间差距，构建一个端到端的神经渲染系统。

**Figure 1** 展示了这一愿景：从输入视频出发，准确估计几何与材质缓冲，并在指定光照条件下生成照片级真实感的渲染结果，为图像编辑应用提供基础工具。

## 核心创新

DiffusionRenderer 的核心创新在于将**视频扩散模型**统一应用于神经逆渲染与前向渲染，并通过三个关键设计突破传统方法的瓶颈。

### 1. 统一的双向渲染框架

传统渲染管线将逆渲染（从图像恢复材质几何）与前向渲染（从材质几何生成图像）视为独立问题，通常需要显式的3D几何表示或路径追踪。DiffusionRenderer 首次以**单一视频扩散模型架构**同时解决这两个任务：神经逆渲染器从输入视频估计法线、深度、反照率、粗糙度、金属度等G-buffer属性；神经前向渲染器则根据这些G-buffer与目标环境光图生成逼真视频。这一统一框架无需显式3D几何或完美G-buffer，即可逼近路径追踪的着色效果（Figure 2），从根本上规避了经典PBR对精确几何的强依赖。

### 2. 多分辨率环境光交叉注意力注入

现有方法通常将环境光图的VAE编码直接拼接到图像潜变量通道中，这种方式难以有效保留高动态范围和方向信息。DiffusionRenderer 设计了**专用环境光编码器**，将LDR/对数/方向三种编码的环境光图映射为 $K=4$ 层多分辨率特征，并通过扩散UNet的**交叉注意力层**逐级注入光照信息：

$$\mathbf{c}_{\text{env}} := \{ \mathbf{h}_{\text{env}}^i \}_{i=1}^K = \mathcal{E}_{\text{env}}(\mathbf{h}_\mathbf{E})$$

消融实验表明，移除独立环境光编码器会导致前向渲染PSNR下降约0.5 dB（Table 1: Ours 28.3 vs Ours w/o env. encoder 27.8），验证了多分辨率交叉注意力注入相比简单拼接的显著优势。

### 3. 视频时序建模提升材质估计

单帧图像模型在逆渲染中难以区分外观变化是源于材质差异还是光照变化。DiffusionRenderer 基于**Stable Video Diffusion**构建视频扩散模型，利用多帧时序信息约束材质估计。在SyntheticScenes数据集上，视频模型相比单帧图像模型将**金属度RMSE降低41%**（0.066→0.039），**粗糙度RMSE降低20%**（0.098→0.078）（Table 3），充分证明时序上下文对材质属性解耦的关键作用。

### 4. 合成-真实域适应策略

仅使用合成数据训练的前向渲染模型在复杂真实场景（如树木、室外环境）中会出现严重的域偏差。DiffusionRenderer 提出**联合训练+LoRA适配**策略：首先利用训练好的逆渲染器与现成光照估计模型为真实视频自动标注G-buffer与环境光标签，然后联合合成数据与自动标注的真实数据训练前向渲染器，并对真实数据引入可训练的LoRA参数 $\Delta\boldsymbol{\theta}$：

$$\mathcal{L}(\boldsymbol{\theta}, \Delta\boldsymbol{\theta}) = \|\mathbf{f}_{\boldsymbol{\theta}}(\mathbf{z}_\tau^{\text{synth}}; \mathbf{g}^{\text{synth}}, \mathbf{c}_{\text{env}}^{\text{synth}}, \tau) - \mathbf{z}_0^{\text{synth}}\|_2^2 + \|\mathbf{f}_{\boldsymbol{\theta}+\Delta\boldsymbol{\theta}}(\mathbf{z}_\tau^{\text{real}}; \mathbf{g}^{\text{real}}, \mathbf{c}_{\text{env}}^{\text{real}}, \tau) - \mathbf{z}_0^{\text{real}}\|_2^2$$

定性消融（Figure 7）显示，加入LoRA的真实数据联合训练显著消除了合成数据的域偏差，大幅提升真实场景的重光照质量。

## 整体框架

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2501_18590/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison of forward rendering. Our method generates high-quality inter-reflections (top) and shadows (bottom), producing more accurate results than the neural baselines. Figure 5. Qualitative comparison of inverse rendering. We compare with RGB↔X [83] on DL3DV10k dataset. Both methods work well on indoor scenes, while our method predicts finer details in thin structures and more accurate metallic and roughness channels (top), likely benefiting from our curated training data. As compared to RGB↔X, our method generalizes better to outdoor scenes (bottom row)*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2501_18590/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparison of relighting. Our method produces more accurate specular reflections compared to the baselines. Figure 7. Qualitative ablation of relighting. Joint training with real-world data and adding LoRA during training significantly improve relighting quality for real-world scenes*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2501_18590/figures/003_Figure_3.jpg]]
*Figure 3: Method overview. Given an input video, the neural inverse renderer estimates geometry and material properties per pixel. It generates one scene attribute at a time, with the domain embedding indicating the target attributes to generate (Sec. 4.2). Conversely, the neural forward renderer produces photorealistic images given lighting information, geometry, and material buffers. The lighting condition is injected into the base video diffusion model through cross-attention layers (Sec. 4.1). During joint training with both synthetic and real data, we use an optimizable LoRA for real data sources (Sec. 4.4)*

DiffusionRenderer 是一个统一的神经渲染框架，由两个视频扩散模型构成，分别承担神经逆渲染与神经前向渲染任务。其核心设计思路是：**同一个视频扩散模型架构可同时用于从视频估计G-buffer（逆渲染）和根据G-buffer与光照生成逼真图像（前向渲染）**，无需显式路径追踪或精确3D表示。

### 框架总览

整个pipeline包含以下关键模块及其协作关系：

1. **神经逆渲染器（Neural Inverse Renderer）**：输入一段RGB视频 $\mathbf{I}$，逐帧估计场景的几何与材质属性，输出五通道G-buffer：法线 $\hat{\mathbf{n}}$、深度 $\hat{\mathbf{d}}$、漫反射颜色 $\hat{\mathbf{a}}$、粗糙度 $\hat{\mathbf{r}}$、金属度 $\hat{\mathbf{m}}$。每个属性通过一次专用推理生成，由**域嵌入（domain embedding）**指示当前生成的目标通道。

2. **神经前向渲染器（Neural Forward Renderer）**：以逆渲染器输出的G-buffer和目标环境光图 $\mathbf{E}_{\text{tgt}}$ 为条件，生成逼真的RGB视频。该模块作为路径追踪着色的神经近似，将光照信息通过交叉注意力机制注入视频扩散UNet。

3. **环境光编码器（Environment Map Encoder）**：将环境光图编码为 $K$ 层多分辨率特征 $\mathbf{c}_{\text{env}} := \{\mathbf{h}_{\text{env}}^i\}_{i=1}^K$，通过扩散UNet各层的交叉注意力注入光照条件。相比直接将环境光VAE编码拼接到图像潜变量通道的简单方案，这种多分辨率注入方式更好地保留了高动态范围和方向信息。

4. **LoRA适配器**：在前向渲染器处理真实世界数据时，引入少量可训练参数 $\Delta\boldsymbol{\theta}$，缓解合成数据与真实数据之间的域差异。

### 数据流与训练策略

DiffusionRenderer 采用分阶段训练策略，以弥合合成数据与真实场景之间的域差距：

- **第一阶段**：在合成视频数据集上训练**逆渲染器**，同时联合InteriorVerse和HyperSim等公开图像本征数据集进行协同训练，提升泛化能力。
- **自动标注阶段**：利用训练好的逆渲染器与现成光照估计模型DiffusionLight，为DL3DV10k真实视频自动生成G-buffer与环境光标签。
- **第二阶段**：联合合成数据与自动标注的真实数据训练**前向渲染器**。合成数据使用基础参数 $\boldsymbol{\theta}$，真实数据额外引入LoRA参数 $\Delta\boldsymbol{\theta}$ 进行域适应。

前向渲染的联合训练目标为：
$$
\mathcal{L}(\boldsymbol{\theta}, \Delta\boldsymbol{\theta}) = \|\mathbf{f}_{\boldsymbol{\theta}}(\mathbf{z}_\tau^{\text{synth}}; \mathbf{g}^{\text{synth}}, \mathbf{c}_{\text{env}}^{\text{synth}}, \tau) - \mathbf{z}_0^{\text{synth}}\|_2^2 + \|\mathbf{f}_{\boldsymbol{\theta}+\Delta\boldsymbol{\theta}}(\mathbf{z}_\tau^{\text{real}}; \mathbf{g}^{\text{real}}, \mathbf{c}_{\text{env}}^{\text{real}}, \tau) - \mathbf{z}_0^{\text{real}}\|_2^2
$$

### 推理流程

在推理阶段，给定输入视频 $\mathbf{I}$ 和目标环境光 $\mathbf{E}_{\text{tgt}}$，框架依次执行：

1. 逆渲染器逐通道估计G-buffer：$\{\hat{\mathbf{n}},\hat{\mathbf{d}},\hat{\mathbf{a}},\hat{\mathbf{r}},\hat{\mathbf{m}}\} = \text{InverseRenderer}(\mathbf{I})$
2. 前向渲染器合成重光照视频：$\hat{\mathbf{I}}_{\text{tgt}} = \text{ForwardRenderer}(\{\hat{\mathbf{n}},\hat{\mathbf{d}},\hat{\mathbf{a}},\hat{\mathbf{r}},\hat{\mathbf{m}}, \mathbf{E}_{\text{tgt}}\})$

该统一框架使得DiffusionRenderer能够同时支撑材质编辑、重光照和物体插入等多种图像编辑应用，无需依赖显式3D几何或精确的路径追踪。

## 核心模块与公式推导

### 整体框架

DiffusionRenderer 由两个视频扩散模型构成统一框架：**神经前向渲染器** 将 G-buffer 与光照条件转化为逼真视频，作为路径追踪着色的神经近似；**神经逆渲染器** 则从输入视频重建几何与材质属性（法线、深度、反照率、粗糙度、金属度）。两者共享 Stable Video Diffusion 骨干，无需显式 3D 几何或路径追踪即可完成双向渲染任务。

### 神经前向渲染器

前向渲染被形式化为条件生成任务。给定几何与材质 G-buffer（相机空间法线 $\mathbf{n} \in \mathbb{R}^{F\times H\times W\times 3}$、归一化相对深度 $\mathbf{d} \in \mathbb{R}^{F\times H\times W\times 1}$、基色 $\mathbf{a} \in \mathbb{R}^{F\times H\times W\times 3}$、粗糙度 $\mathbf{r} \in \mathbb{R}^{F\times H\times W\times 1}$、金属度 $\mathbf{m} \in \mathbb{R}^{F\times H\times W\times 1}$）以及光照条件，模型输出逼真 RGB 视频。

**环境光编码器** 是前向渲染器的关键模块。光照条件以环境光图表示，编码为三种全景图像 $\{\mathbf{E}_{\text{ldr}}, \mathbf{E}_{\text{log}}, \mathbf{E}_{\text{dir}}\}$，分别对应 LDR 颜色、对数亮度与方向编码。环境光编码器 $\mathcal{E}_{\text{env}}$ 从中提取 $K=4$ 层多分辨率特征：

$$\mathbf{c}_{\text{env}} := \{\mathbf{h}_{\text{env}}^i\}_{i=1}^K = \mathcal{E}_{\text{env}}(\mathbf{h}_\mathbf{E})$$

这些多分辨率特征通过扩散 UNet 的交叉注意力层注入，替代了基线方法中将 VAE 编码的环境光图直接拼接到图像潜变量通道的简单做法。消融实验表明，移除独立环境光编码器导致前向渲染 PSNR 下降约 0.5 dB（Table 1: 28.3 → 27.8），验证了多分辨率交叉注意力注入的有效性。

**扩散 UNet** $\mathbf{f}_{\boldsymbol{\theta}}$ 以噪声潜变量 $\mathbf{z}_{\tau}$ 和 G-buffer 潜变量 $\mathbf{g}$ 作为像素级输入，在每一 UNet 层级 $k$ 查询对应的环境光特征 $\mathbf{h}_{\text{env}}^k$，生成目标预测 $\mathbf{f}_{\boldsymbol{\theta}}(\mathbf{z}_{\tau}; \mathbf{g}, \mathbf{c}_{\text{env}}, \tau)$。

### 神经逆渲染器

逆渲染被形式化为从输入视频 $\mathbf{I}$ 到场景属性 G-buffer 的条件生成：

$$\{\hat{\mathbf{n}}, \hat{\mathbf{d}}, \hat{\mathbf{a}}, \hat{\mathbf{r}}, \hat{\mathbf{m}}\} = \text{InverseRenderer}(\mathbf{I})$$

每个 G-buffer 属性在独立通道中生成，由可优化的**域嵌入** $\mathbf{c}_{\text{emb}} \in \mathbb{R}^{K_{\text{emb}} \times C_{\text{emb}}}$ 指示当前生成的目标属性类型（共 5 种）。扩散过程在 G-buffer 潜变量空间进行，噪声潜变量为 $\mathbf{g}_{\tau} = \alpha_{\tau}\mathbf{g}_0 + \sigma_{\tau}\boldsymbol{\epsilon}$，模型预测目标为：

$$\mathcal{L}(\boldsymbol{\theta}, \mathbf{c}_{\text{emb}}) = \|\mathbf{f}_{\boldsymbol{\theta}}(\mathbf{g}_\tau^P; \mathbf{z}, \mathbf{c}_{\text{emb}}^P, \tau) - \mathbf{g}_0^P\|_2^2$$

其中 $\mathbf{z}$ 为输入视频的潜变量，$P$ 表示当前目标属性。

### 联合训练与域适应

前向渲染器的训练联合优化合成数据与真实数据，对真实数据引入可训练的 LoRA 参数 $\Delta\boldsymbol{\theta}$：

$$\mathcal{L}(\boldsymbol{\theta}, \Delta\boldsymbol{\theta}) = \|\mathbf{f}_{\boldsymbol{\theta}}(\mathbf{z}_\tau^{\text{synth}}; \mathbf{g}^{\text{synth}}, \mathbf{c}_{\text{env}}^{\text{synth}}, \tau) - \mathbf{z}_0^{\text{synth}}\|_2^2 + \|\mathbf{f}_{\boldsymbol{\theta}+\Delta\boldsymbol{\theta}}(\mathbf{z}_\tau^{\text{real}}; \mathbf{g}^{\text{real}}, \mathbf{c}_{\text{env}}^{\text{real}}, \tau) - \mathbf{z}_0^{\text{real}}\|_2^2$$

真实数据的 G-buffer 与光照标签由训练好的逆渲染器与 DiffusionLight 自动标注流水线生成。引入 LoRA 的联合训练显著改善了复杂真实场景（如树木）的重光照质量，消除了仅合成训练的域偏差。

### 重光照合成

将逆渲染与前向渲染串联，即可实现重光照：先用逆渲染器从源视频估计 G-buffer，再用前向渲染器结合目标环境光图 $\mathbf{E}_{\text{tgt}}$ 生成重光照视频：

$$\hat{\mathbf{I}}_{\text{tgt}} = \text{ForwardRenderer}(\{\hat{\mathbf{n}}, \hat{\mathbf{d}}, \hat{\mathbf{a}}, \hat{\mathbf{r}}, \hat{\mathbf{m}}, \mathbf{E}_{\text{tgt}}\})$$

### 环境光自编码器预训练

环境光编码器 $\mathcal{E}_{\text{env}}$ 与解码器 $\mathcal{D}_{\text{env}}$ 通过 L2 重建损失预训练，确保编码特征保留光照与方向信息：

$$\mathcal{L}_{\text{env}} = \|\mathbf{h}_{\mathbf{E}'} - \mathcal{D}_{\text{env}}(\mathcal{E}_{\text{env}}(\mathbf{h}_{\mathbf{E}}), \mathcal{E}_{\text{dir}}(\mathbf{h}_{\mathbf{D}}))\|^2$$

### 关键设计决策的消融证据

1. **视频模型 vs 图像模型**：视频扩散模型替代单帧图像模型，在逆渲染中金属度 RMSE 降低 41%（0.066 → 0.039），粗糙度 RMSE 降低 20%（0.098 → 0.078），证明时序信息对材质估计的重要性（Table 3）。

2. **环境光编码器**：独立的多分辨率交叉注意力注入优于通道拼接，前向渲染 PSNR 提升约 0.5 dB（Table 1）。

3. **Split-sum shading 条件**：额外拼接 split-sum shading 缓存作为条件未带来显著提升，表明模型已能从 G-buffer 和光照中充分学习阴影效果（Table 1）。

4. **1步确定性 vs 多步随机**：1步确定性模型获得更高 PSNR 但导致模糊，多步随机模型更利于真实感细节，前向渲染与重光照任务采用多步随机模型（Table 3）。

## 实验与分析

### 核心实验设置与评估基准

DiffusionRenderer 在三个互补维度上接受检验：**神经前向渲染**（从 G‑buffer 与光照生成 RGB）、**重光照**（改变环境光后的渲染）以及**神经逆渲染**（从视频恢复 G‑buffer）。评估覆盖合成与真实场景，以 PSNR、SSIM、LPIPS 为主要图像质量指标，逆渲染额外使用 RMSE 与平均角度误差。

合成测试集分为两类：
- **SyntheticObjects**：30 个独立物体，每个物体渲染为 24 帧视频，配备 4 种光照条件。
- **SyntheticScenes**：40 个完整场景，同样为 24 帧视频 ×4 种光照，复杂度显著高于单物体设置。

真实场景评估主要依赖 **DL3DV10k** 自动标注数据，并在 **InteriorVerse** 上进行反照率估计的定量基准测试。

基线方法涵盖经典物理渲染与前沿神经方法：**SSRT**（屏幕空间光线追踪）、**SplitSum**（经典 PBR 近似）、**RGB↔X**（图像扩散模型的神经正反向渲染）、**DiLightNet** 与 **Neural Gaffer**（扩散/神经重光照）、**Kocsis et al.**（扩散逆渲染）以及 **FEGR**（3D 逆渲染与重光照）。

### 主结果分析

#### 神经前向渲染

在 SyntheticScenes 上，DiffusionRenderer 取得 **26.0 dB PSNR**，远超最优神经基线 RGB↔X 的 18.5 dB（+7.5 dB），SSIM 从 0.645 提升至 0.780，LPIPS 从 0.302 降至 0.201。这一巨大差距表明，视频扩散模型对复杂场景中的互反射、阴影等全局光照效应具有更强的神经逼近能力（Table 1）。在 SyntheticObjects 上，本方法 PSNR 达 28.3 dB，比 RGB↔X 的 25.2 dB 高出 3.1 dB，且与经典 SSRT 方法（29.4 dB）性能接近，验证了在无需显式 3D 几何或路径追踪的前提下，神经渲染可逼近物理渲染的质量上限。


![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2501_18590/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation of neural rendering. Table 2. Quantitative evaluation of relighting*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2501_18590/figures/013_Table_1.jpg]]
*Table 1: Table S2. User study. We report the percentage of images where users preferred Ours over baselines. A preference > 50% indicates Ours outperforming baselines. Evaluation follows main paper Table 1, 2 on SyntheticScenes and SyntheticObjects*

值得注意的鲁棒性信号是：从 SyntheticObjects 到 SyntheticScenes，DiffusionRenderer 的 PSNR 仅下降 2.3 dB，而其他神经基线出现更大幅度的退化，说明本方法对场景复杂度具有更好的泛化能力。

#### 重光照

在 SyntheticScenes 重光照任务中，DiffusionRenderer 取得 **24.63 dB PSNR**，比 DiLightNet 的 18.88 dB 提升 5.75 dB，SSIM 从 0.576 升至 0.756（Table 2）。定性结果（Figure 6）显示，本方法在镜面反射的准确性和一致性上明显优于基线，尤其在包含复杂阴影与互反射的场景中。用户研究（Table S2）进一步佐证：在 SyntheticScenes 和 SyntheticObjects 上，用户对本方法重光照结果的偏好比例均显著超过 50%。

视频质量指标 ColorVideoVDP（Table S1）以 JOD 单位报告感知质量，DiffusionRenderer 在多种光照条件下均取得较高 JOD 值，表明其时序一致性与真实感在视频层面同样占优。

#### 神经逆渲染

逆渲染的核心发现是**时序信息对材质估计至关重要**。视频模型相比单帧图像模型，金属度 RMSE 从 0.066 降至 0.039（降低 41%），粗糙度 RMSE 从 0.098 降至 0.078（降低 20%）（Table 3）。在 InteriorVerse 真实数据集的反照率估计基准上，本方法同样展现出竞争力（Table 4）。定性比较（Figure 5）表明，DiffusionRenderer 在薄结构细节和室外场景泛化方面优于 RGB↔X，这得益于精心构建的训练数据与视频模型固有的时序一致性。


![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2501_18590/figures/005_Table_4.jpg]]
*Table 4: Quantitative benchmark of albedo estimation on InteriorVerse dataset [91]*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2501_18590/figures/006_Table_3.jpg]]
*Table 3: Quantitative evaluation of inverse rendering on SyntheticScenes video dataset. image: per-frame inference as image model. det.: 1-step deterministic inference*

### 消融实验

#### 环境光编码器

移除独立的环境光编码器、改为将 VAE 编码后的环境光图直接拼接到图像潜变量通道，导致前向渲染 PSNR 从 28.3 dB 降至 27.8 dB（约 0.5 dB 损失，Table 1），验证了多分辨率交叉注意力注入机制对保留高动态范围与方向信息的有效性。

#### 视频模型 vs. 图像模型

将视频扩散模型替换为逐帧独立推断的图像模型，逆渲染金属度 RMSE 增加 41%，粗糙度 RMSE 增加 20%（Table 3），前向渲染指标也全面下降（Table 1），证明多帧一致生成对材质解耦和渲染真实感具有因果性贡献。

#### 附加着色条件

额外拼接 split‑sum shading 缓存作为条件输入，未带来显著性能提升（Table 1 中 Ours (+ shading cond.) 与 Ours 性能相当），表明模型已能从 G‑buffer 与环境光中充分学习阴影与全局光照效应，无需显式注入近似着色结果。

#### 真实数据与 LoRA 联合训练

仅使用合成数据训练的前向渲染模型在真实复杂场景（如树木）中出现明显域偏差，重光照质量显著退化。引入自动标注的真实视频数据并附加可训练的 LoRA 参数 Δθ 后，重光照真实感大幅提升（Figure 7），消除了合成‑真实域差异对渲染质量的关键瓶颈。

#### 确定性 vs. 随机采样

1 步确定性模型在 PSNR 等光度指标上优于多步随机模型，但会导致模糊预测，尤其在包含高频细节的歧义区域，LPIPS 等感知指标反而更差（Table 3）。因此，前向渲染与重光照任务采用多步随机模型以捕获更丰富的真实感细节，而逆渲染任务可在精度优先场景下使用确定性推断。

### 失败模式与局限性

尽管 DiffusionRenderer 在多项任务上取得领先，仍存在若干可辨识的失败模式：

1. **推断效率瓶颈**：前向渲染模型在 A100 GPU 上生成 24 帧 512×512 视频需 20.3 秒，难以满足实时应用需求。这是视频扩散模型固有的计算开销，目前尚无内置加速机制。
2. **光照估计误差传播**：真实视频自动标注依赖现成模型 **DiffusionLight** 估计环境光，该模型自身的误差会直接污染前向渲染的训练信号，在极端光照条件下可能产生系统性偏差。
3. **室外泛化不足**：合成训练数据以 Objaverse 室内物体为主，对水面、森林等室外复杂场景及特殊材质（如次表面散射、体积效应）的泛化能力有限，重光照结果可能出现不自然的镜面反射或阴影缺失。
4. **确定性模型的模糊问题**：1 步确定性推断虽然 PSNR 更高，但在高细节区域产生模糊，限制了其在需要高频纹理保真度的应用场景中的使用。
5. **长视频未充分验证**：视频模型虽在 24 帧片段上展现良好时序一致性，但未进行极端长视频测试，长序列中的漂移或闪烁问题尚不明确。

### 开放问题

- 能否通过蒸馏技术将多步扩散模型压缩为快速前馈网络，在保持渲染质量的同时将推断时间降至实时水平？
- 如何改进现成的光照估计算法，以提高真实世界自动标注的准确性与鲁棒性，从根本上缓解误差传播？
- 如何进一步扩展框架以处理动态场景、非刚性物体以及复杂折射/散射效果，突破当前静态场景假设的限制？
- 是否可以利用神经内在特征进行任务特定微调，增强材质编辑与物体插入等内容编辑操作的一致性？

### 补充图表

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2501_18590/figures/014_Figure.jpg]]

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2501_18590/figures/010_Table.jpg]]
*Table: S1. Quantitative evaluation of relighting in terms of ColorVideoVDP. ColorVideoVDP reports video quality in the JOD (Just-Objectionable-Difference) units. The highest quality (no difference) is reported as 10 and lower values are reported for distorted content. We compute a JOD value per clip for three novel lighting conditions in each series and report the average over all clips*


## 方法谱系与知识库定位

### 物理渲染与神经渲染的十字路口

DiffusionRenderer 位于物理渲染与神经渲染的交叉地带。传统管线依赖显式 3D 几何与路径追踪：**SSRT**（Screen Space Ray Tracing）在缺乏完整网格时无法准确表达阴影与反射，且对 G-buffer 噪声极其敏感；**SplitSum** 近似虽快，但牺牲了互反射等全局光照效果。这些经典方法的根本瓶颈在于——真实场景中难以获取精确的 3D 几何、高质量材质和光照条件。

神经渲染方法试图绕过这一瓶颈。**RGB↔X** 首次将图像扩散模型用于正向与逆向渲染的统一框架，但其单帧处理方式丢失了时序信息，且简单的环境光拼接注入无法充分保留高动态范围与方向信息。**DiLightNet** 与 **Neural Gaffer** 专注于重光照任务，但在复杂阴影与镜面反射场景中存在明显不足。**Kocsis et al.** 探索了扩散模型在逆向渲染中的应用，**FEGR** 则尝试 3D 逆向渲染与重光照的联合优化，但这些方法在真实世界泛化性上均受限于数据稀缺与域偏差。

### 核心设计决策的定位

DiffusionRenderer 做出了三个关键设计选择，使其在方法谱系中占据独特位置：

**视频扩散替代图像扩散。** 将基础模型从单帧图像扩散升级为基于 Stable Video Diffusion 的视频扩散模型，这一选择直接带来逆向渲染中金属度 RMSE 降低 41%（0.066→0.039）、粗糙度 RMSE 降低 20%（0.098→0.078）的显著收益。时序信息对材质估计的贡献在此得到量化验证。

**交叉注意力光照注入替代通道拼接。** 专用环境光编码器 $\\mathcal{E}_{\\text{env}}$ 提取 $K=4$ 层多分辨率特征 $\\mathbf{c}_{\\text{env}} := \\{ \\mathbf{h}_{\\text{env}}^i \\}_{i=1}^K$，通过 UNet 交叉注意力层注入光照信息，而非简单将 VAE 编码后的环境光拼接到图像潜变量通道。消融实验表明，移除独立环境光编码器导致前向渲染 PSNR 下降约 0.5 dB。

**合成-真实联合训练与 LoRA 域适应。** 利用训练好的逆渲染器与 DiffusionLight 为 DL3DV10k 真实视频自动标注 G-buffer 与光照标签，再联合合成数据训练前向渲染器，并对真实数据引入可训练的 LoRA 参数 $\\Delta\\boldsymbol{\\theta}$。这一策略有效弥合了合成-真实域间差距，在复杂真实场景（如树木）中大幅提升重光照质量。

### 适用边界与局限

尽管 DiffusionRenderer 在 SyntheticScenes 上取得 26.0 dB PSNR（远超 RGB↔X 的 18.5 dB），其适用边界仍受多重因素制约：

**推断效率瓶颈。** 24 帧 512×512 视频的前向渲染需 20.3 秒（A100），难以满足实时应用需求。1 步确定性模型虽获更高 PSNR 但导致模糊，多步随机模型细节丰富但推断更慢——这一精度-效率权衡尚未解决。

**光照估计的误差传播。** 真实视频自动标注依赖现成模型 DiffusionLight 估计环境光，该模型的误差可能传播至前向渲染训练。这是整个自动标注流水线的单点故障风险。

**数据分布偏差。** 合成数据集以 Objaverse 室内物体为主，对室外复杂场景（水面、森林、动态天气）的泛化可能不足。虽然真实数据联合训练部分缓解了这一问题，但标注质量的上限仍受逆渲染器与光照估计模型能力约束。

**极端场景未充分验证。** 视频模型虽有更好的时序一致性，但未进行长视频的极端测试；非刚性物体、复杂折射/散射效果的真实性亦未得到系统评估。

### 开放问题

1. **模型压缩与加速。** 能否通过蒸馏技术将多步扩散模型压缩为快速前馈网络，在保持质量的同时将推断时间降至实时水平？
2. **动态场景扩展。** 如何将框架从静态场景扩展到包含非刚性变形、动态光照变化的通用视频重光照？
3. **光照估计的闭环优化。** 是否可以利用神经内在特征进行任务特定微调，或设计端到端的光照估计-渲染联合优化，以提升真实世界自动标注的准确性？
4. **编辑一致性。** 在材质编辑与物体插入等应用中，如何进一步保证多帧间的编辑内容一致性，避免时序闪烁？

## 原文 PDF

![[paperPDFs/CVPR_2025/DiffusionRenderer_Neural_Inverse_and_Forward_Rendering_with_Video_Diffusion_Models.pdf]]
