---
title: "AAMDM: Accelerated Auto-regressive Motion Diffusion Model"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/AAMDM_Accelerated_Auto_regressive_Motion_Diffusion_Model.pdf
project_link: null
code_link: null
aliases:
- AAARMDM
- AAMDM
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将反向扩散过程分解为两个子步骤：使用去噪扩散GAN（DD-GANs）进行快速初步生成（3步）和自回归扩散模型（ADM）进行精炼（2步），并在低维嵌入空间（手工特征x + 可学习潜在变量z）而非全姿态空间中进行过渡建模。
primary_logic: 扩散过程早期从噪声生成样本，后期做微小调整的特性使得可以用少量DD-GAN步快速起草，再用少量ADM步提升质量，同时在嵌入空间学习降低训练复杂度和改善运动学约束。
claims:
- AAMDM在运动质量上接近AMDM200（FID 14.051 vs 12.132），但推理速度快约40倍（173 FPS vs 4.72 FPS），证明了速度与质量的优秀权衡。
- 去除嵌入空间后，多样性DIV降至56.341，FID飙升至128.412，表明过渡必须在嵌入空间中进行。
- 在人工多模态数据集上，AAMDM成功捕获所有模态，而基线方法（如LMM、MotionVAE、AMDM5）难以学习多对多映射，验证了框架的多模态建模能力。
- LaFAN1 (Random Motion Synthesis) 上 FID (越低越好) = 14.051 (AAMDM)
---

# AAMDM: Accelerated Auto-regressive Motion Diffusion Model

> [!tip] 核心洞察
> 扩散过程早期从噪声生成样本，后期做微小调整的特性使得可以用少量DD-GAN步快速起草，再用少量ADM步提升质量，同时在嵌入空间学习降低训练复杂度和改善运动学约束。

| 字段 | 内容 |
|------|------|
| 中文题名 | AAMDM：加速自回归运动扩散模型 |
| 英文题名 | AAMDM: Accelerated Auto-regressive Motion Diffusion Model |
| 会议/期刊 | CVPR 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | AAMDM (Accelerated Auto-regressive Motion Diffusion Model) |
| Dataset | LaFAN1 |

> [!tip] 效果简介
> - LaFAN1 (Random Motion Synthesis) 上，FID (越低越好) 14.051 (AAMDM) vs 12.132 (AMDM200) (+1.919 (质量略低，但速度快约40倍))；DIV (多样性，越高越好) 11.574 (AAMDM) vs 11.165 (AMDM200) (+0.409 (多样性略高))；FPS (帧率) 173 (AAMDM) vs 4.72 (AMDM200) (快约40倍)。

## 概要

交互式角色运动合成面临一个核心瓶颈：标准扩散模型虽能生成高质量、多样化的运动，但其数百步的反向扩散过程导致推理极慢（例如 AMDM200 仅约 4.72 FPS），无法满足实时交互需求；同时，在全姿态空间学习多对多的过渡映射本身具有高难度，使得现有方法难以同时兼顾质量、多样性与实时性。

针对上述问题，本文提出 **AAMDM（Accelerated Auto-regressive Motion Diffusion Model）**，其核心思路是将反向扩散过程分解为两个子步骤——先以去噪扩散GAN（DD-GANs）用 3 步快速生成运动草案，再用自回归扩散模型（ADM）以 2 步进行精炼，从而将总步数压缩至 5 步；同时，过渡建模被迁移到一个低维嵌入空间（由手工特征与可学习潜在变量构成），而非原始的全姿态空间，以降低学习复杂度并改善运动学约束。

在 LaFAN1 数据集上的实验表明，AAMDM 的运动质量（FID 14.051）接近 AMDM200（FID 12.132），但推理速度提升约 40 倍（173 FPS vs. 4.72 FPS），且多样性（DIV）略优于 AMDM200。与基于学习的运动匹配方法 LMM 相比，AAMDM 在 FID 上显著改善（14.051 vs. 49.706）；与基于 VAE 的 MotionVAE 相比，脚滑动率（FFR）大幅降低（0.131 vs. 0.312）。消融实验进一步证实，嵌入空间是维持多样性与质量的关键——移除后 DIV 骤降至 56.341、FID 飙升至 128.412；精炼模块的引入对运动质量有显著正向贡献，而 DD-GAN 步数取 3 可在质量与效率间取得最佳平衡。



### 问题背景

交互式角色动画在游戏、虚拟现实和电影制作中至关重要，其核心挑战在于从给定的前一帧姿态出发，实时合成出既高质量又多样化的后续运动序列。这一任务本质上是一个**序贯条件生成问题**：模型需要在每一帧根据当前状态，从可能的后续运动分布中进行采样。

近年来，扩散模型在运动合成领域展现出卓越的生成质量。以 **AMDM**（Shi et al., arXiv 2023）为代表的方法将运动过渡建模为去噪扩散过程，通过数百步反向扩散逐步从噪声中恢复出精细的运动姿态。然而，这种逐帧、多步采样的范式在交互式应用中面临根本性瓶颈：**标准扩散模型需要大量反向扩散步数（如 AMDM200 使用 200 步），导致推理速度极慢，无法满足实时交互的需求。**

### 现有方法缺口

当前运动合成方法在质量、多样性与速度之间存在着难以调和的三角权衡：

- **基于学习的方法**（如 **LMM**，Kolsi et al., SCA 2018）通过运动匹配检索或回归直接生成后续姿态，推理速度快，但倾向于产生确定性或低多样性的输出，无法捕获运动过渡中固有的多模态分布。
- **基于 VAE 的方法**（如 **MotionVAE**，Ling et al., TOG 2020）引入隐变量以增强多样性，但生成的运动质量往往较差，表现为脚滑动等运动学伪影严重（FFR 高达 0.312）。
- **扩散模型方法**中，**AMDM5**（Shi et al., arXiv 2023）仅使用 5 步扩散以追求速度，但生成质量显著不足；而 **AMDM200** 虽然质量最优（FID 12.132），但帧率仅约 4.72 FPS，远低于实时交互所需的水平。

更深层的结构性困难在于：**在全姿态空间（维度高达 338）中直接学习多对多的过渡映射极其困难。** 运动过渡天然具有一对多特性——同一前一帧姿态可以自然过渡到多种合理的后续姿态。在如此高维的空间中，模型难以有效捕获这种条件分布的全部模态，导致模式坍塌或生成质量下降。

### 本文动机

针对上述瓶颈，本文提出 **AAMDM（Accelerated Auto-regressive Motion Diffusion Model）**，其核心动机在于打破扩散模型在运动合成中“高质量必伴随低速度”的固有认知。关键洞察是：**扩散过程的早期阶段负责从噪声中生成样本的粗略结构，后期阶段则进行精细调整。** 因此，可以将这两个阶段解耦——用极少步数的快速生成器完成“起草”，再用少量扩散步数进行“精炼”，从而在保持扩散模型生成质量的同时大幅提升推理速度。

同时，AAMDM 将过渡建模从高维的全姿态空间迁移到**低维嵌入空间**，通过自编码器学习紧凑表示，使模型能够在更易处理的流形上学习多对多映射，从而同时改善训练效率和生成多样性。



## 核心方法与创新机理

AAMDM 的核心创新在于通过**生成空间降维**与**扩散过程分解**两个维度的协同设计，系统性地解决了标准扩散模型在交互式运动合成中“质量‑多样性‑速度”的不可能三角。

### 创新一：嵌入空间中的过渡建模

标准方法（如 **AMDM200** (Shi et al., arXiv 2023)）在全姿态空间 $\mathbf{y}$（维度 338）中直接建模相邻帧的映射 $S(\mathbf{y}_{n-1}) \to \mathbf{y}_n$。这一设计的根本困难在于：全姿态空间的高维性和冗余性使得多对多过渡分布的学习极为困难，同时训练和推理的计算成本高昂。

AAMDM 将过渡建模迁移到低维嵌入空间 $\mathbf{xz}$ 中进行。具体而言，框架首先训练一个自编码器（Encoder $E^{AE}$ 和 Decoder $D^{AE}$），将全姿态向量 $\mathbf{y}$ 映射到紧凑的嵌入向量 $\mathbf{xz} = [\mathbf{x}, \mathbf{z}]$，其中 $\mathbf{x}$ 为手工设计的运动学特征，$\mathbf{z}$ 为可学习的潜在变量。过渡模型仅需学习 $S(\mathbf{xz}_{n-1}) \to \mathbf{xz}_n$，生成后再通过解码器重建全姿态。

这一设计带来的因果效应在消融实验中得到了决定性验证（Table 2, wo/ Emb）：移除嵌入空间后，多样性 DIV 从 11.574 骤降至 56.341（越低越好），运动质量 FID 从 14.051 飙升至 128.412。这表明**嵌入空间是 AAMDM 能够学习多对多过渡映射的必要条件**——在全姿态空间中，模型无法有效捕获过渡分布的多模态特性。

### 创新二：DD‑GAN 起草 + ADM 精炼的双阶段生成

标准扩散模型（如 AMDM200）需要 200 步反向扩散才能生成一帧运动，推理帧率仅 4.72 FPS，远未达到交互式应用的门槛。AAMDM 的核心洞察在于利用扩散过程的阶段性特征：**早期步骤从噪声中生成样本结构，后期步骤进行微调**。基于此，AAMDM 将反向扩散分解为两个功能互补的子模块：

1. **生成模块（DD‑GANs，3 步）**：采用去噪扩散 GAN（Xiao et al.）作为快速起草器。DD‑GAN 将反向扩散建模为条件 GAN 的多模态分布，引入额外潜在变量 $\mathbf{r}^t$，能够在仅 3 步内生成下一步嵌入向量的合理草案。

2. **精炼模块（ADM，2 步）**：以自回归扩散模型对草案进行 2 步精炼。ADM 以前一帧嵌入 $\mathbf{xz}_{n-1}$ 和当前噪声图 $\mathbf{xz}_n^t$ 为条件，直接预测干净的嵌入向量 $\hat{\mathbf{xz}}_n^0$，修正 DD‑GAN 草案中的瑕疵并提升长期生成质量。

两个模块总计仅需 **5 步**（3 + 2），却实现了与 200 步 AMDM200 相当的运动质量。定量结果（Table 1）表明：AAMDM 的 FID 为 14.051，与 AMDM200 的 12.132 仅差 1.919，但推理帧率达到 173 FPS，**加速约 40 倍**。消融实验进一步验证了这一分解设计的必要性：精炼步数 $T_{ADM} > 0$ 显著提升 FID 和 DIV（Table 2, $T_{ADM}$ settings），而 $T_{GAN}=3$ 在质量与效率之间取得最优平衡。

### 创新三：基于梯度的引导扩散控制

AAMDM 在反向扩散过程中引入基于梯度的控制机制（Eq. 13），通过扰动生成向量实现用户指令的实时响应：

$$\hat{\mathbf{xz}}_n^{0,*} = \hat{\mathbf{xz}}_n^0 - \epsilon \alpha^t \nabla_{\mathbf{xz}_n^t} J(\hat{\mathbf{x}}_n^0, \bar{\mathbf{x}}_n)$$

其中 $J$ 为衡量生成运动与用户查询匹配程度的目标函数。这一设计将运动控制无缝集成到扩散采样过程中，无需额外训练分类器或控制网络，保持了框架的简洁性。Table 1 的用户控制场景结果表明，AAMDM 在该场景下同样显著优于基线方法。

### 创新总结：changed slots 的系统性协同

上述三个创新对应了相对基线方法的四个关键 changed slots：

| 设计维度 | 基线值（AMDM200） | AAMDM 方案 | 因果效应 |
|---------|-----------------|-----------|---------|
| 过渡建模空间 | 全姿态空间 $\mathbf{y}$ | 嵌入空间 $\mathbf{xz}$ | 使多对多过渡学习成为可能（移除后 FID 恶化至 128.412） |
| 生成方法 | 200 步 DDPM 反向扩散 | 3 步 DD‑GAN + 2 步 ADM | 40 倍加速，质量基本持平 |
| 条件输入 | 仅前一帧姿态 | 前一帧嵌入 + 时间步 + 潜在变量 $\mathbf{r}^t$ | 支持多模态草案生成 |
| 运动控制 | 无 | 梯度引导扩散 | 实现免训练的实时用户控制 |

这些 changed slots 并非孤立改进，而是形成了因果链条：**嵌入空间降维**降低了过渡建模的难度，使得**少步扩散**成为可能；**DD‑GAN 的多模态生成能力**在嵌入空间中得以充分发挥，捕获多对多过渡分布；**ADM 精炼**弥补了少步生成的精度损失；**梯度引导**则在不破坏生成质量的前提下实现了灵活控制。这一系统性设计是 AAMDM 能够在 LaFAN1 数据集上同时取得高质量（FID 14.051）、高多样性（DIV 11.574）和实时帧率（173 FPS）的根本原因。



AAMDM（Accelerated Auto-regressive Motion Diffusion Model）是一个面向交互式角色运动合成的生成框架，其核心设计目标是同时实现高运动质量、强多样性与实时推理速度。框架通过三个关键组件的协同工作，将标准扩散模型数百步的反向过程压缩至仅需5步，实现了约40倍的推理加速。

### 核心设计理念

标准扩散模型在运动合成中面临双重瓶颈：其一，反向扩散需要数百步迭代，导致推理速度极慢（如AMDM200仅约4.72 FPS），无法满足交互式应用需求；其二，在全姿态空间中直接学习帧间过渡映射时，多对多的条件分布极为复杂，传统方法难以同时捕获所有模态。AAMDM的因果调控思路是将反向扩散过程拆解为两个子阶段——利用去噪扩散GAN（DD-GANs）进行快速初步生成，再用自回归扩散模型（ADM）进行精炼——并将过渡建模从高维全姿态空间迁移至低维嵌入空间，从而降低学习难度并改善运动学约束。

### 三组件架构

AAMDM的整体架构（Figure 2）由以下三个核心模块串联构成：

![[assets/figures/papers/paper_list_l1843_AAMDM_Accelerated_Auto_regressive_Motion_Diffusion_Model/figures/002_Figure_2.jpg]]
*Figure 2: Overview of AAMDM. AAMDM incorporates three pivotal components for better motion quality and faster inference. Firstly, it models transitions within a low-dimensional embedded space*

**1. 嵌入空间构建模块（Autoencoder）**

自编码器负责学习一个低维嵌入空间，将高维全姿态向量 $\mathbf{y}$（维度338，包含关节平移、旋转、速度及根节点速度等信息）映射到紧凑的嵌入表示。具体地，编码器 $E^{AE}$ 将姿态 $\mathbf{y}$ 编码为可学习的潜在变量 $\mathbf{z}$，与手工设计的运动学特征 $\mathbf{x}$ 拼接形成嵌入向量 $\mathbf{xz} \in \mathbf{XZ}$；解码器 $D^{AE}$ 则从 $\mathbf{xz}$ 重建全姿态 $\hat{\mathbf{y}}$。训练时通过值损失（Eq.1）和速度损失（Eq.2）联合优化，确保重建精度与运动连贯性：

$$L_{val}^{D,E} = || \hat{\mathbf{y}} \ominus \mathbf{y} || + || F(\hat{\mathbf{y}}) \ominus F(\mathbf{y}) ||$$

其中 $F(\cdot)$ 为前向运动学函数，$\ominus$ 表示姿态空间中的差异度量。

**2. 生成模块（DD-GANs）**

生成模块采用去噪扩散GAN作为骨干网络，负责在自回归循环中快速生成下一帧嵌入向量的草案。与标准扩散模型假设反向过程为单峰高斯分布不同，DD-GANs将反向分布建模为多模态条件GAN：

$$\hat{\mathbf{xz}}_n^0 = G^{GAN}(\mathbf{xz}_n^t, \mathbf{xz}_{n-1}, \mathbf{r}^t, t)$$

其中 $\mathbf{xz}_{n-1}$ 为前一帧的嵌入向量，$\mathbf{r}^t$ 为额外引入的潜在变量以增强多模态表达能力，$t$ 为扩散时间步。该模块仅需3步即可完成从噪声到草案的生成。

**3. 精炼模块（ADM）**

精炼模块是一个轻量级自回归扩散模型，以前一帧嵌入 $\mathbf{xz}_{n-1}$ 为条件，对生成模块的输出进行2步微调。ADM直接预测干净的嵌入向量而非噪声：

$$\hat{\mathbf{x}}\tilde{\mathbf{z}}_n^0 = G^{ADM}(\mathbf{xz}_n^t, \mathbf{xz}_{n-1}, t)$$

其训练损失为值损失与速度损失的加权组合。精炼模块的引入显著提升了长期生成质量，消融实验表明去除精炼步数（$T_{ADM}=0$）会导致FID和DIV均明显恶化（Table 2）。

### 数据流与推理流程

在推理时，给定前一帧的嵌入向量 $\mathbf{xz}_{n-1}$，系统按以下流程生成下一帧：

1. **草案生成**：DD-GANs从随机噪声出发，经过3步反向扩散生成嵌入向量的初步估计。
2. **精炼优化**：ADM以该草案为起点，经过2步自回归扩散进行质量提升。
3. **姿态重建**：解码器 $D^{AE}$ 将精炼后的嵌入向量 $\mathbf{xz}_n$ 重建为全姿态向量 $\mathbf{y}_n$。
4. **控制引导（可选）**：在用户控制场景下，通过梯度扰动机制调整生成向量：

$$\hat{\mathbf{xz}}_n^{0,*} = \hat{\mathbf{xz}}_n^0 - \epsilon \alpha^t \nabla_{\mathbf{xz}_n^t} J(\hat{\mathbf{x}}_n^0, \bar{\mathbf{x}}_n)$$

其中 $J(\cdot)$ 为衡量生成结果与用户查询匹配度的目标函数。

整个流程总计5步扩散，实现了173 FPS的推理速度，同时运动质量（FID 14.051）接近200步的AMDM200（FID 12.132），验证了“草案-精炼”两阶段策略在速度与质量权衡上的有效性（Table 1）。

### 补充图表

![[assets/figures/papers/paper_list_l1843_AAMDM_Accelerated_Auto_regressive_Motion_Diffusion_Model/figures/001_Figure_1.jpg]]
*Figure 1: We introduce the Accelerated Auto-regressive Motion Diffusion Model (AAMDM), a novel framework designed to synthesize diverse and high-quality character motions at interactive rates*



AAMDM 的核心架构由三个关键模块构成，其设计动机源于对标准扩散模型瓶颈的因果分析：在全姿态空间学习多对多过渡映射困难，且多步反向扩散导致推理速度过慢。为解决这一问题，AAMDM 将反向扩散过程分解为“快速起草”与“精炼”两个子步骤，并将过渡建模空间从全姿态空间迁移到低维嵌入空间。

### 嵌入空间构建模块

该模块由一个自编码器（Encoder $E^{AE}$ 和 Decoder $D^{AE}$）组成，负责学习从全姿态向量 $\mathbf{y}$ 到潜在向量 $\mathbf{z}$ 的映射，以及从拼接向量 $\mathbf{xz} = [\mathbf{x}, \mathbf{z}]$ 重建姿态的过程。其中 $\mathbf{x}$ 为手工设计的运动学特征，$\mathbf{z}$ 为可学习的潜在变量。

自编码器通过两类损失函数进行训练。姿态值损失 $L_{val}^{D,E}$ 同时约束重建姿态的关节旋转/平移值以及前向运动学（FK）关节位置：

$$L_{val}^{D,E} = || \hat{\mathbf{y}} \ominus \mathbf{y} || + || F(\hat{\mathbf{y}}) \ominus F(\mathbf{y}) ||$$

速度损失 $L_{vel}^{D,E}$ 则约束相邻帧之间关节位置的变化速率，以提升时序平滑性：

$$L_{vel}^{D,E} = \left|\left| \frac{F(\hat{\mathbf{y}}_0) \ominus F(\hat{\mathbf{y}}_1)}{\delta n} - \frac{F(\mathbf{y}_0) \ominus F(\mathbf{y}_1)}{\delta n} \right|\right|$$

其中 $\ominus$ 表示姿态空间中的差值运算，$F(\cdot)$ 为前向运动学函数，$\delta n$ 为帧间隔。

### 自回归扩散模型（ADM）精炼模块

ADM 作为过渡建模的骨干网络，在嵌入空间中学习状态转移 $S(\mathbf{xz}_{n-1}) \to \mathbf{xz}_n$。其前向扩散过程向目标嵌入向量逐步添加高斯噪声：

$$q(\mathbf{xz}_n^t | \mathbf{xz}_n^{t-1}) = \mathcal{N}(\sqrt{\alpha^t} \mathbf{xz}_n^{t-1}, (1 - \alpha^t) \mathbf{I})$$

其中 $\alpha^t$ 为第 $t$ 步的噪声调度参数。反向扩散过程则直接预测干净的嵌入向量，以当前噪声图、前一帧嵌入和时间步为条件：

$$\hat{\mathbf{x}}\tilde{\mathbf{z}}_n^0 = G^{ADM}(\mathbf{xz}_n^t, \mathbf{xz}_{n-1}, t)$$

ADM 的训练损失由值损失和速度损失加权组合而成。值损失约束预测嵌入与真实嵌入的差异，速度损失则约束预测序列的速度模式：

$$L_{vel}^{ADM} = \left|\left| \frac{(\hat{\mathbf{x}}_{1:h}^0 - \hat{\mathbf{x}}_{0:h-1}^0)}{h \cdot \delta n} - \frac{(\mathbf{x}_{1:h} - \mathbf{x}_{0:h-1})}{h \cdot \delta n} \right|\right|$$

$$L_{G^{ADM}} = w_{val}^{ADM} L_{val}^{ADM} + w_{vel}^{ADM} L_{vel}^{ADM}$$

其中 $h$ 为预测窗口长度，$w_{val}^{ADM}$ 和 $w_{vel}^{ADM}$ 为损失权重超参数。

### 去噪扩散GAN（DD-GANs）生成模块

为加速推理，AAMDM 引入 DD-GANs 进行快速初步生成。该模块将反向扩散过程建模为多模态条件分布，通过引入额外的潜在变量 $\mathbf{r}^t$ 来捕获过渡的多模态特性：

$$\hat{\mathbf{xz}}_n^0 = G^{GAN}(\mathbf{xz}_n^t, \mathbf{xz}_{n-1}, \mathbf{r}^t, t)$$

DD-GAN 生成器的训练目标为最小化与真实后验分布之间的 KL 散度：

$$L_{G^{GAN}} = - \mathbb{E}_{p(\mathbf{xz}_n^{t-1} | \mathbf{xz}_n^t, \mathbf{xz}_{n-1})} [\log(D^{GAN}(\sim))]$$

其中 $D^{GAN}$ 为判别器，用于区分生成样本与真实样本。

### 梯度引导控制模块

AAMDM 支持通过基于梯度的扩散引导实现用户可控的运动生成。给定用户控制目标函数 $J$，在反向扩散的每一步对生成的嵌入向量进行梯度扰动：

$$\hat{\mathbf{xz}}_n^{0,*} = \hat{\mathbf{xz}}_n^0 - \epsilon \alpha^t \nabla_{\mathbf{xz}_n^t} J(\hat{\mathbf{x}}_n^0, \bar{\mathbf{x}}_n)$$

其中 $\epsilon$ 为引导强度，$\bar{\mathbf{x}}_n$ 为用户指定的目标特征（如期望的关节位置或轨迹方向），$J$ 衡量生成结果与用户查询之间的匹配程度。

### 推理流水线

完整推理流程中，DD-GANs 以 3 步反向扩散快速生成下一步嵌入向量的草案，随后 ADM 以 2 步自回归扩散进行精炼，总计 5 步即可完成单帧生成。最终通过解码器 $D^{AE}$ 将嵌入向量 $\mathbf{xz}_n$ 重建为全姿态向量 $\mathbf{y}_n$。这一分解策略利用了扩散过程早期从噪声生成样本、后期做微小调整的特性，使得 DD-GANs 步负责捕获多模态结构，ADM 步负责提升时序一致性和运动学精度。



## 实验与关键发现

### 核心性能权衡：质量与速度的突破

AAMDM的核心实验结论是：在LaFAN1随机运动合成基准上，AAMDM以**约40倍的速度优势**（173 FPS vs 4.72 FPS）实现了与AMDM200接近的运动质量（FID 14.051 vs 12.132），同时多样性略有提升（DIV 11.574 vs 11.165）（Table 1）。这一结果直接验证了“DD-GANs快速起草 + ADM精炼”的两阶段生成策略的有效性——扩散过程早期从噪声生成样本、后期做微小调整的特性，使得用3步DD-GANs快速生成草案、再用2步ADM提升质量成为可能。

![[assets/figures/papers/paper_list_l1843_AAMDM_Accelerated_Auto_regressive_Motion_Diffusion_Model/figures/003_Table_1.jpg]]
*Table 1: In our quantitative analysis, we demonstrate that the AAMDM framework is capable of generating motions of a quality comparable to that of AMDM200, while significantly outperforming other methods in both random sampling and user control scenarios. Meanwhile, the result also indicates that AAMDM is approximately 40 times faster than AMDM200*

与其他基线方法相比，AAMDM在运动质量上大幅领先：FID相比LMM（49.706）降低约35.7，相比MotionVAE（22.981）降低约8.9，相比AMDM5（18.741）降低约4.7。在脚滑动率（FFR）上，AAMDM（0.131）显著优于MotionVAE（0.312），表明嵌入空间建模有效改善了运动学约束的保持。

### 消融实验：设计选择的因果验证

Table 2的消融实验揭示了三个关键设计选择的因果效应：

**精炼模块的必要性**：增加精炼步数T_ADM从0到2，FID从18.741降至14.051，DIV从8.134升至11.574，验证了ADM精炼模块对运动质量和多样性的显著提升作用。这支持了核心洞察——扩散过程的后期微调步骤对生成质量至关重要，不能仅依赖DD-GANs的快速生成。

**生成步数的最优平衡**：T_GAN=3在质量与效率之间取得最佳平衡。继续增大步数虽然质量略有提升，但效率下降明显，验证了3步DD-GANs作为起草模块的充分性。

**嵌入空间的决定性作用**：去除嵌入空间（wo/ Emb）是最具破坏性的消融——多样性DIV从11.574暴跌至56.341（越低越好），FID从14.051飙升至128.412。这一结果表明，在全姿态空间（338维）中学习多对多过渡映射对扩散模型而言极为困难，嵌入空间通过降维和特征解耦显著降低了训练复杂度，是框架成功的前提条件。

### 多模态建模能力的验证

在人工构造的Squ-9-Gaussian多模态数据集上（Figure 4），AAMDM成功捕获了所有过渡模态，而LMM、MotionVAE和AMDM5等基线方法难以学习多对多映射。这验证了AAMDM框架在顺序场景中建模多模态分布映射的独特优势——DD-GANs的多模态分布建模能力与自回归扩散模型的精炼机制相结合，有效解决了标准扩散模型在全姿态空间中学习多对多过渡的瓶颈。

![[assets/figures/papers/paper_list_l1843_AAMDM_Accelerated_Auto_regressive_Motion_Diffusion_Model/figures/005_Figure_4.jpg]]
*Figure 4: Visualization of the learned transition results of an artificial Squ-9-Gaussian experiment in 2D. We show that AAMDM outperforms baseline methods in learning the many-to-many distribution mapping in sequential scenarios*

定性对比（Figure 3）进一步印证了这一结论：从相似起始姿态出发，LMM只能生成单一运动模式，而AAMDM能够复现多样化复杂运动。

![[assets/figures/papers/paper_list_l1843_AAMDM_Accelerated_Auto_regressive_Motion_Diffusion_Model/figures/004_Figure_3.jpg]]
*Figure 3: Comparison between motions generated by LMM (top) and AAMDM (Bottom). Starting from a similar character pose, LMM is unable to generate diverse motions while AAMDM can reproduce diverse complex motions*

### 已知局限与失败模式

尽管AAMDM在速度-质量权衡上取得了突破，仍存在以下局限：

1. **运动质量与计算成本的根本矛盾**：虽然相比AMDM200加速约40倍，但FID仍有约1.9的差距。论文指出可通过引入并行计算和时序信息利用进一步优化，但这需要手动验证具体方案的有效性。

2. **梯度引导控制的跟踪精度**：基于梯度的引导扩散机制（Eq.13）在用户指令包含急转弯时偶尔无法精确跟踪目标轨迹。这一失败模式源于梯度扰动机制对复杂非线性控制目标的适应能力有限，原文讨论提及但未给出量化评估。

3. **嵌入空间的概率结构**：当前嵌入空间使用简单的潜在变量建模，论文提出可引入矩阵-费雪分布等更复杂的结构化分布来约束DD-GANs的潜在空间，这暗示当前嵌入空间的概率表达能力可能不足。

### 补充图表

![[assets/figures/papers/paper_list_l1843_AAMDM_Accelerated_Auto_regressive_Motion_Diffusion_Model/figures/006_Table_2.jpg]]
*Table 2: Ablation study results. ∗The default parameters*



## 定位与知识库关联

### 1. 与基线方法的关系

AAMDM 的核心贡献在于解决了交互式运动合成中“质量-多样性-速度”的不可能三角。在 AAMDM 之前，该领域的方法大致分化为两条技术路线：基于学习的运动匹配（如 LMM）与基于生成模型的运动控制器（如 MotionVAE 及 AMDM 系列）。AAMDM 的设计选择直接回应了这些基线的结构性缺陷。

**LMM**（Kolsi et al., SCA 2018）作为运动匹配方法的代表，通过在大规模运动数据库中检索最匹配的过渡片段来实现高保真度的运动合成。其根本瓶颈在于“检索-拼接”范式天然缺乏多样性生成能力——当数据库中没有覆盖当前过渡需求时，LMM 只能返回确定性结果。在 LaFAN1 随机运动合成测试中，LMM 的多样性指标 DIV 仅为 5.374，而 AAMDM 达到 11.574（Table 1）。Figure 3 的定性对比更直观地展示了这一差异：从相同起始姿态出发，LMM 只能生成单一运动轨迹，而 AAMDM 能够复现多样化的复杂运动。AAMDM 通过将过渡建模从“检索”转变为“从学习到的多模态分布中采样”，从根本上突破了这一限制。

**MotionVAE**（Ling et al., TOG 2020）采用变分自编码器框架，能够生成多样化的运动，但其生成质量受限于 VAE 的模糊重建特性。在 Table 1 中，MotionVAE 的 FID 为 22.981，脚滑动率 FFR 高达 0.312——这意味着生成的运动存在严重的物理不合理性。AAMDM 通过引入扩散模型作为主干网络，利用其逐步去噪的生成机制，在保持多样性的同时将 FID 降至 14.051，FFR 降至 0.131。

**AMDM 系列**（Shi et al., arXiv 2023）是 AAMDM 最直接的基线。AMDM200 使用 200 步标准 DDPM 反向扩散，在 LaFAN1 上取得了最优的 FID（12.132），但推理速度仅为 4.72 FPS，远未达到实时交互需求（通常要求 >30 FPS）。AMDM5 将步数压缩至 5 步以换取速度，但 FID 恶化至 18.741，说明简单的步数缩减会导致严重的质量退化。AAMDM 的核心洞察在于：扩散过程早期从噪声生成样本、后期做微小调整的特性，使得可以用少量 DD-GAN 步快速起草，再用少量 ADM 步精炼。这一“分解-协作”策略使 AAMDM 在仅需 5 步总步数（3 步 DD-GAN + 2 步 ADM）的条件下，将 FID 恢复至 14.051，同时推理速度达到 173 FPS——约为 AMDM200 的 40 倍。

### 2. 关键设计选择的因果机制

AAMDM 相对于基线的优势并非来自单一技术创新，而是三个设计槽位的协同改变。消融实验（Table 2）揭示了每个改变的因果贡献。

**过渡建模空间的降维**是最具决定性的设计选择。当移除嵌入空间（wo/ Emb），直接在 338 维全姿态空间中建模过渡时，多样性 DIV 崩溃至 56.341（正常值约 11），FID 飙升至 128.412。这一结果表明，全姿态空间中的多对多过渡学习面临严重的维度灾难——扩散模型需要在极高维空间中捕获稀疏的多模态条件分布，导致训练不稳定和模式坍塌。嵌入空间的引入（手工特征 x + 可学习潜在变量 z）将过渡建模压缩到低维流形上，显著降低了学习复杂度，同时自编码器的前向运动学损失（$L_{val}^{D,E}$，Eq.1）保证了重建的运动学合理性。

**DD-GAN 与 ADM 的分工协作**解决了“速度-质量”权衡。消融实验显示，当精炼步数 $T_{ADM} = 0$（即仅使用 DD-GAN）时，FID 和 DIV 均显著恶化；增加 $T_{ADM}$ 持续改善质量，验证了精炼模块的必要性。同时，$T_{GAN} = 3$ 被证明是效率与质量的最佳平衡点——继续增大 DD-GAN 步数对质量提升有限，但推理速度下降。这种分工利用了扩散过程的时间特性：DD-GAN 擅长从纯噪声快速生成合理草案（利用其多模态条件分布建模能力），ADM 擅长对草案进行精细调整（利用其逐步去噪的稳定性）。

**嵌入空间中的自回归条件建模**使 AAMDM 能够捕获时序上的多模态过渡。在人工构建的 Squ-9-Gaussian 实验中（Figure 4），数据分布包含 9 个高斯模态的复杂多对多映射。LMM 只能学习到单一模态，MotionVAE 和 AMDM5 虽能覆盖部分模态但存在严重的模式混合或遗漏，而 AAMDM 成功捕获了所有 9 个模态。这归因于扩散模型在嵌入空间中学习条件分布 $q(\mathbf{xz}_n^t | \mathbf{xz}_n^{t-1})$（Eq.5）时，其多步去噪机制天然适合表达复杂多模态条件分布。

### 3. 适用边界与局限

尽管 AAMDM 在随机运动合成上取得了显著的效率-质量权衡，其方法仍存在明确的适用边界。

**运动质量的天花板**：AAMDM 的 FID（14.051）与 AMDM200（12.132）之间仍存在约 15% 的差距。这表明 5 步的生成-精炼流程在极端情况下可能无法完全恢复 200 步扩散的精细细节。对于离线应用场景（如电影级动画），AMDM200 的高质量可能比 AAMDM 的实时性更具价值。

**梯度引导控制的精度限制**：AAMDM 的基于梯度引导机制（Eq.13）通过扰动生成向量来匹配用户指令，但原文讨论中提及该方法在用户指令包含急转弯时偶尔无法精确跟踪。这是因为梯度引导本质上是局部线性近似——当目标轨迹与当前生成分布偏离过大时，单步梯度扰动可能不足以纠正方向。

**嵌入空间的表达能力**：当前嵌入空间使用手工特征 x 与可学习潜在变量 z 的拼接，其概率结构相对简单。原文明确指出现有嵌入空间可进一步改进，例如引入矩阵-费雪分布等更复杂的潜在空间建模方法，以更好地约束去噪扩散 GAN 的潜在空间。

**计算成本的残余瓶颈**：虽然 173 FPS 已满足实时交互需求，但原文仍将“进一步降低计算成本”列为开放问题，暗示在移动设备或大规模多角色场景中，当前方案可能仍不够轻量。

### 4. 开放问题与后续方向

AAMDM 为交互式运动合成开辟了“扩散模型实时化”的技术路径，同时留下了若干值得探索的开放问题。

**结构化潜在空间建模**：能否用矩阵-费雪分布等结构化分布替代当前嵌入空间的简单拼接？这类分布能更好地编码旋转矩阵的几何约束，可能同时提升生成质量和运动学合理性。

**基于学习的控制机制**：当前梯度引导依赖手工设计的控制目标函数 $J$，对复杂指令（如“边跑边挥手”）的表达能力有限。替换为学习到的控制策略网络，可能增强可控性并处理更复杂的用户意图。

**时序信息的并行化利用**：当前自回归生成逐帧进行，虽已通过 DD-GAN 加速每帧生成，但帧间仍为串行。引入时序并行计算（如同时预测多帧草案）可能进一步突破速度瓶颈。

**更大规模数据集的验证**：当前实验仅基于 LaFAN1 数据集，其在运动多样性、角色拓扑等方面的覆盖范围有限。在更大规模、更多样化的运动数据集上验证 AAMDM 的泛化能力，是方法走向实用的必要步骤。



## 原文 PDF

![[paperPDFs/CVPR_2024/AAMDM_Accelerated_Auto_regressive_Motion_Diffusion_Model.pdf]]
