---
title: "Motion-Zero: Zero-Shot Moving Object Control Framework for Diffusion-Based Video Generation"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/Motion_Zero_Zero_Shot_Moving_Object_Control_Framework_for_Diffusion_Based_Video_Generation.pdf
project_link: null
code_link: null
aliases:
- MZ
- Motion-Zero
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 在扩散模型的推理阶段，通过三个关键操作实现零样本轨迹控制：(1)利用初始噪声先验模块(D DIM Inversion +局部混合)为初始噪声注入位置先验；(2)在交叉注意力图上施加空间约束损失(内部/外部/中心/相似性损失)，引导注意力响应集中在目标边界框内；(3)通过偏移时序注意力机制，将不同帧的目标区域对齐到同一参考位置，保证运动物体的时序一致性。
primary_logic: 预训练视频扩散模型本身已具备丰富的物体运动知识，但缺乏显式的语义对齐；通过操纵初始噪声、交叉注意力图和时序注意力，可以在不进行任何额外训练的情况下，赋予任意预训练视频扩散模型精确的物体轨迹控制能力，实现零样本、即插即用的控制。
claims:
- 空间约束(SC)是实现精确位置控制的最关键模块，移除后mIoU从0.54骤降至0.18。
- Motion-Zero在零样本设置下显著提升了基线模型的生成质量和控制指标，例如在ZeroScope上Text Align从20.31提升至21.96，Consistency从0.88提升至0.94。
- Motion-Zero在复杂轨迹上的控制性能全面优于TrailBlazer和Peekaboo，mIoU 0.55、AP50 0.67、Cov. 0.97均最优。
- 用户研究显示Motion-Zero在外观、一致性和控制能力上均显著优于对比方法，Cronbach's α为0.901。
---

# Motion-Zero: Zero-Shot Moving Object Control Framework for Diffusion-Based Video Generation

> [!tip] 核心洞察
> 预训练视频扩散模型本身已具备丰富的物体运动知识，但缺乏显式的语义对齐；通过操纵初始噪声、交叉注意力图和时序注意力，可以在不进行任何额外训练的情况下，赋予任意预训练视频扩散模型精确的物体轨迹控制能力，实现零样本、即插即用的控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | Motion-Zero: 面向扩散视频生成的零样本运动物体控制框架 |
| 英文题名 | Motion-Zero: Zero-Shot Moving Object Control Framework for Diffusion-Based Video Generation |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2401.10150) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | Motion-Zero |
| Dataset | 33 prompts + 8 simple trajectories, 33 prompts + 17 complex trajectories |

> [!tip] 效果简介
> - 33 prompts + 8 simple trajectories (ZeroScope) 上，Text Align (CLIP) 21.96 vs 20.31 (+1.65)；Inter-frame Consistency 0.94 vs 0.88 (+0.06)；PickScore (user preference) 19.89 vs 18.98 (+0.91)。
> - 33 prompts + 17 complex trajectories 上，mIoU 0.55 vs 0.50 (TrailBlazer c.) (+0.05)；AP50 0.67 vs 0.61 (TrailBlazer c.) (+0.06)；Cov. (detection coverage) 0.97 vs 0.91 (TrailBlazer c.) (+0.06)。

## 概要

**瓶颈**：现有文本到视频扩散模型生成的物体运动轨迹具有随机性，用户无法直接控制。已有的运动控制方法依赖大规模标注数据集进行训练，计算成本高，且只能应用于其训练时所基于的特定模型，缺乏跨模型的即插即用能力。

**核心洞察**：预训练视频扩散模型本身已具备丰富的物体运动知识，但缺乏显式的语义对齐。通过操纵初始噪声、交叉注意力图和时序注意力，可以在不进行任何额外训练的情况下，赋予任意预训练视频扩散模型精确的物体轨迹控制能力。

**方法定位**：Motion-Zero 是一个零样本、即插即用的运动物体控制框架。它在扩散模型的推理阶段引入三个关键操作——
1. **初始噪声先验模块 (INPM)**：利用 DDIM Inversion 与局部混合为初始噪声注入位置先验，提升物体外观稳定性和位置准确性；
2. **空间约束 (SC)**：在交叉注意力图上施加内部/外部/中心/相似性损失，引导注意力响应集中在目标边界框内，实现精确的空间位置控制；
3. **偏移时序注意力机制 (STAM)**：将不同帧的目标区域对齐到同一参考位置进行时序注意力，保证运动物体的时序一致性。

**主要结果**：Motion-Zero 在零样本设置下显著提升了基线模型的生成质量和控制指标。在 ZeroScope 上，Text Align 从 20.31 提升至 21.96，Inter-frame Consistency 从 0.88 提升至 0.94。在复杂轨迹控制上，Motion-Zero 的 mIoU 达到 0.55，AP50 达到 0.67，Cov. 达到 0.97，全面优于 TrailBlazer 和 Peekaboo 等零样本方法。消融实验证实空间约束是实现精确位置控制的最关键模块，移除后 mIoU 从 0.54 骤降至 0.18。用户研究（Cronbach's α = 0.901）进一步验证了该方法在外观、一致性和控制能力上的显著优势。



### 问题背景：视频扩散模型中的运动随机性与控制缺失

近年来，基于扩散的文本到视频生成模型取得了显著进展，能够根据文本描述生成具有丰富动态内容的视频。然而，一个核心瓶颈始终存在：**模型生成的物体运动轨迹具有内在随机性，用户无法对运动物体的空间位置和移动路径施加直接控制**。给定相同的文本提示，模型可能产生完全不同的运动模式——物体可能向左或向右移动，可能静止不动，也可能以非预期的方式变形。这种不可控性严重限制了视频生成模型在影视制作、广告设计、教育内容创作等实际场景中的应用价值，因为这些场景往往要求精确的叙事性运动编排。

### 现有方法的缺口：训练依赖与模型锁定

为了实现对生成视频中物体运动的控制，研究者提出了多种方法，但这些方法普遍存在两类关键缺陷：

**1. 训练成本高昂与数据依赖。** 主流方法在标准视频扩散训练目标中引入额外的运动条件（如轨迹边界框序列 $\mathcal{B}$），将损失函数扩展为：

$$\mathcal{L} = \mathbb{E}_{\mathbf{z}_0, \mathbf{c}, \boldsymbol{\epsilon} \sim N(0, \mathbf{I}), t} \left[ \| \boldsymbol{\epsilon} - \boldsymbol{\epsilon}_\theta(\mathbf{z}_t, t, \mathbf{c}, \mathcal{B}) \|_2^2 \right]$$

这要求在大规模标注数据集上进行充分训练，使模型学会将轨迹条件与物体运动关联起来。此类方法不仅需要昂贵的计算资源，还依赖于高质量的运动标注数据，而这类数据的获取和标注成本极高。

**2. 模型特异性与即插即用能力的缺失。** 由于训练过程与特定基础模型的参数深度绑定，这些方法只能应用于其训练时所基于的特定视频扩散模型。当用户希望切换到更新的、生成质量更优的基础模型时，整个训练流程必须重新执行。这种“模型锁定”效应使得现有方案缺乏跨模型的通用性和即插即用能力，难以跟随基础模型的快速迭代节奏。

### 零样本控制方法的进展与不足

近期出现的零样本运动控制方法尝试在推理阶段操纵预训练模型，避免了额外训练。例如，**TrailBlazer**（Ma, Lewis, and Kleijn, 2023）通过操纵交叉注意力图来引导物体运动，**Peekaboo**（Jain et al., 2024）则采用掩码注意力机制实现空间控制。这些方法证明了在推理阶段实现运动控制的可能性，但它们在控制精度、时序一致性和外观保持方面仍存在明显不足——尤其在复杂轨迹场景下，物体容易出现变形、漂移或帧间不一致等问题。

### 核心洞察：预训练模型已具备运动知识，缺乏的是语义对齐

Motion-Zero的核心洞察在于：**预训练视频扩散模型本身已蕴含丰富的物体运动先验知识**——模型能够生成合理的运动模式，说明其内部表示已经编码了关于物体如何移动的隐含知识。问题的关键不在于知识的缺失，而在于缺乏一种机制将这些隐含知识与用户指定的精确轨迹进行显式语义对齐。如果能够在推理阶段有效地“唤醒”并引导这些已有知识，就有可能在无需任何额外训练的前提下，赋予任意预训练模型精确的轨迹控制能力。

基于这一洞察，Motion-Zero提出了一个完全在推理阶段运行的零样本控制框架，通过三个关键操作——**初始噪声先验注入、空间约束潜变量优化、偏移时序注意力对齐**——实现对预训练视频扩散模型中物体运动轨迹的即插即用式控制。



## 核心方法与创新机理

Motion-Zero 的核心创新在于，它首次证明**无需任何额外训练**即可为任意预训练视频扩散模型赋予精确的物体运动轨迹控制能力。这一突破绕开了现有方法的根本瓶颈：传统文本到视频模型生成的物体轨迹具有随机性，而已有的运动控制方法（如 **MotionCtrl**（Wang et al., arXiv 2023d））依赖大规模标注数据集进行训练，计算成本高，且只能应用于其训练时所基于的特定模型，缺乏跨模型的即插即用能力。

Motion-Zero 的因果操纵杆建立在三个关键创新操作上，它们均在推理阶段作用于冻结的预训练模型：

1.  **初始噪声先验模块 (INPM)**：利用 DDIM Inversion 从元视频中反演出携带位置先验的初始噪声，再通过局部混合操作将其注入目标边界框区域。这为生成过程提供了物体外观稳定性和位置准确性的强先验。
2.  **空间约束 (SC)**：在交叉注意力图上施加一组精心设计的损失函数（内部/外部/中心/相似性损失），通过梯度更新潜变量，强制目标 token 的注意力响应集中在用户指定的边界框内，实现精确的单帧位置控制。
3.  **偏移时序注意力机制 (STAM)**：通过偏移操作将不同帧的目标框区域对齐到同一参考位置，执行时序注意力后再移回原位。这保证了运动物体在时序上的连续性，避免了传统时序注意力在运动场景下导致的内容混合与模糊。

这三个模块的协同作用，使得 Motion-Zero 能够以零样本、即插即用的方式，操纵预训练视频扩散模型内部已具备的丰富物体运动知识，将其与用户指定的轨迹进行显式语义对齐。



Motion-Zero 的推理流水线由三个核心模块串联构成：**初始噪声先验模块 (Initial Noise Prior Module, INPM)**、**空间约束 (Spatial Constraints, SC)** 和**偏移时序注意力机制 (Shift Temporal Attention Mechanism, STAM)**，如图 Fig.2(a) 所示。整个框架冻结预训练视频扩散模型的所有参数，仅在推理阶段对潜变量施加操纵，从而实现零样本、即插即用的运动轨迹控制。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2401_10150/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our Motion-Zero. The total pipeline is shown in (a). Given the box condition*

**输入与输出流**。用户提供两项条件：(1) 文本提示中指定待控制的目标实体；(2) 一个边界框序列 $\mathcal{B} = \{\mathcal{B}^f\}_{f=1}^{N_f}$，定义物体在每一帧中的期望位置。框架输出一段视频，其中目标物体沿指定轨迹运动。

**流水线三阶段**。第一阶段，INPM 利用 DDIM Inversion 从元视频中反演得到初始噪声先验，并通过局部混合操作将先验注入目标框区域，生成携带位置与外观先验的初始潜变量 $\mathbf{z}_T$（详见 Fig.2(b)）。第二阶段，在去噪过程的前 $T_1$ 步，对每个时间步 $t$ 的潜变量 $\mathbf{z}_t$ 施加空间约束损失 $\mathcal{L}_{sp}$，通过梯度更新 $\mathbf{z}_t' = \mathbf{z}_t - \beta_t \cdot \nabla \mathcal{L}_{sp}$ 优化潜变量，使目标 token 的交叉注意力响应集中在用户指定的边界框内。第三阶段，将优化后的 $\mathbf{z}_t'$ 送入配备 STAM 的 3D U-Net 进行去噪；STAM 将各帧目标框区域平移至首帧框位置对齐，执行时序注意力后再移回原位，从而在保证时序一致性的同时避免不同位置内容混合（Fig.2(c)）。在剩余的 $T_2$ 步中，恢复标准视频扩散去噪过程，以保持生成质量。

**模块间的因果依赖**。INPM 为 SC 提供稳定的初始位置锚点——消融实验表明，移除 INPM 后物体易发生严重变形或脱离帧（Fig.7）。SC 是实现精确空间控制的核心，移除后 mIoU 从 0.54 骤降至 0.18（Tab.2）。STAM 则确保运动物体在时序上的连续性，移除后物体会出现模糊和变形（Fig.7）。三个模块协同作用，使得 Motion-Zero 能够在零样本条件下赋予任意预训练视频扩散模型精确的物体轨迹控制能力。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2401_10150/figures/001_Figure_1.jpg]]
*Figure 1: Our Motion-Zero framework endows different pre-trained video diffusion models with the capability to manipulate object trajectories directly, circumventing the need for supplementary training. By designating the target entity in the input prompts and a sequence of bounding boxes, users can intuitively direct the motion path of the object within the generated video*



Motion-Zero 是一个完全在推理阶段运作的零样本运动物体控制框架，无需任何额外训练，即可赋予任意预训练视频扩散模型精确的物体轨迹控制能力。其核心由三个关键模块构成：初始噪声先验模块（INPM）、空间约束（SC）和偏移时序注意力机制（STAM）。这三个模块分别从初始噪声、空间定位和时序一致性三个维度，协同实现了对运动物体的即插即用控制。

### 初始噪声先验模块（INPM）

预训练视频扩散模型的初始噪声通常为随机高斯噪声 $\\mathbf{z}_T \\sim N(0, \\mathbf{I})$，这导致物体在生成过程中的初始位置具有高度随机性。INPM 的核心思想是利用 DDIM Inversion 从一段元视频中反演出携带位置先验的噪声，再通过局部混合操作为目标轨迹的第一帧注入位置先验。

具体而言，INPM 首先对一段包含目标物体的元视频进行 DDIM 反演，获得初始噪声 $\\mathbf{z}_I$。随后，将 $\\mathbf{z}_I$ 第一帧中目标框 $\\mathcal{B}^0$ 区域的噪声块提取出来，与当前随机噪声 $\\mathbf{z}_T$ 第一帧中对应框区域的噪声块进行混合：

$$\\mathbf{Pix}(\\mathbf{z}_T^0, \\mathcal{B}^0) = \\lambda_p \\cdot \\mathbf{Pix}(\\mathbf{z}_I^0, \\mathcal{B}^0) + (1 - \\lambda_p) \\cdot \\mathbf{Pix}(\\mathbf{z}_T^0, \\mathcal{B}^0)$$

其中 $\\mathbf{Pix}(\\cdot, \\mathcal{B})$ 表示提取边界框区域内的像素块，$\\lambda_p$ 为混合系数（经验最优值 0.8）。这一操作使得初始噪声在目标框区域携带了来自元视频的语义先验，从而在生成过程中稳定物体的初始位置和外观。消融实验证实，移除 INPM 后物体易发生严重变形或脱离帧，Text Align 分数也明显下降。

### 空间约束（SC）

空间约束是 Motion-Zero 实现精确位置控制的最关键模块。其核心机制是在每个去噪步 $t$ 利用交叉注意力图上的损失函数优化中间潜变量 $\\mathbf{z}_t$，迫使目标 token 的注意力响应集中在用户指定的边界框内。

**交叉注意力图** 从 U-Net 中间层特征 $\\mathbf{z}_t$ 和文本条件 $\\mathbf{c}$ 计算得到：

$$\\mathbf{A} = \\mathrm{Softmax}\\left(\\frac{\\mathbf{Q}\\mathbf{K}^\\top}{\\sqrt{d}}\\right), \\quad \\mathbf{Q} = \\mathbf{W}_Q \\mathbf{z}_t, \\; \\mathbf{K} = \\mathbf{W}_K \\mathbf{c}$$

基于注意力图 $\\mathbf{A}_k^f$（第 $f$ 帧中目标 token $k$ 的注意力响应），空间约束损失由四个分量组成：

- **内部损失** $\\mathcal{L}_i^f$：最大化框内注意力响应值，公式为 $\\mathcal{L}_i^f = 1 - \\frac{1}{P} \\sum \\mathbf{g}(\\mathbf{A}_k^f \\cdot \\mathbf{M}^f, P)$，其中 $\\mathbf{M}^f$ 为框内掩码，$\\mathbf{g}(\\cdot, P)$ 取前 $P$ 个最大值。
- **外部损失** $\\mathcal{L}_o^f$：最小化框外注意力响应值，$\\mathcal{L}_o^f = \\frac{1}{P} \\sum \\mathbf{g}(\\mathbf{A}_k^f \\cdot (1 - \\mathbf{M}^f), P)$。
- **中心损失** $\\mathcal{L}_c^f$：迫使注意力重心与框中心对齐，通过 $L_1$ 距离计算重心坐标 $(W_{\\mathbf{A}_k^f}, H_{\\mathbf{A}_k^f})$ 与框中心 $(\\frac{x_1^f + x_2^f}{2}, \\frac{y_1^f + y_2^f}{2})$ 的偏差。
- **外观相似性损失** $\\mathcal{L}_s$：通过余弦相似度强制相邻帧框内注意力图保持一致，维护外观连续性。

总体空间约束损失为各帧损失的加权和：

$$\\mathcal{L}_{sp} = \\sum_f \\left( \\lambda_i \\mathcal{L}_i^f + \\lambda_o \\mathcal{L}_o^f + \\lambda_c \\mathcal{L}_c^f \\right) + \\lambda_s \\mathcal{L}_s$$

在每个去噪步 $t$，利用该损失的梯度更新潜变量：

$$\\mathbf{z}_t' = \\mathbf{z}_t - \\beta_t \\cdot \\nabla \\mathcal{L}_{sp}$$

其中步长 $\\beta_t$ 随时间递减。消融实验（Table 2）提供了决定性证据：移除 SC 后 mIoU 从 0.54 骤降至 0.18，证实 SC 是实现空间控制的核心模块。超参数 $\\lambda_i = \\lambda_o = 1$、$\\lambda_c = 0.05$、$\\lambda_s = 0.5$ 为经验最优设置，SC 作用步数 $T_1 = 10$ 在控制强度与生成质量间取得最佳平衡。

### 偏移时序注意力机制（STAM）

标准时序自注意力在相同像素坐标的不同帧间计算注意力，当物体在帧间发生位移时，不同帧的注意力区域无法对齐，导致运动物体出现模糊和变形。STAM 通过空间偏移操作解决这一问题：

$$\\mathbf{z}_w^f = \\mathbf{Shift}(\\mathbf{z}^f, \\mathcal{B}^f, \\mathcal{B}^0)$$

首先将各帧目标框 $\\mathcal{B}^f$ 区域平移到与第一帧框 $\\mathcal{B}^0$ 对齐的位置，在偏移后的特征上执行时序注意力：

$$\\mathbf{z}_w' = \\mathbf{TemporalAttention}(\\mathbf{z}_w)$$

最后将各帧特征移回原位置：

$$\\mathbf{z}_w^{f'} = \\mathbf{Shift}(\\mathbf{z}_w^{f'}, \\mathcal{B}^0, \\mathcal{B}^f)$$

这一“偏移-注意力-偏移回”的操作保证了不同帧中同一物体的特征在时序注意力计算时空间对齐，从而维持运动物体的时序一致性和运动连续性。消融实验表明，移除 STAM 后运动物体出现明显的模糊和变形，且 Align 分数下降，证实了其在保持时序一致性方面的关键作用。

三个模块协同工作：INPM 为初始噪声注入位置先验，SC 在去噪过程中逐步优化空间定位，STAM 保证跨帧的运动连续性。整个流程中视频扩散模型的所有参数保持冻结，实现了真正的零样本、即插即用控制。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2401_10150/figures/008_Figure_5.jpg]]
*Figure 5: Attention maps with different components. Prompt: A seal walking on the ice*



## 实验与关键发现

### 主要结果

Motion-Zero 在零样本设置下对多个预训练视频扩散模型实现了即插即用的运动物体轨迹控制，在生成质量和控制精度两个维度上均取得了显著提升。

**生成质量提升。** 以 ZeroScope 为默认基线模型，在 33 条提示词和 8 条简单轨迹的测试集上，Motion-Zero 将 Text Align（CLIP 分数）从 20.31 提升至 21.96（+1.65），Inter-frame Consistency 从 0.88 提升至 0.94（+0.06），PickScore 从 18.98 提升至 19.89（+0.91）（Table 1 左半部分）。这表明施加轨迹控制不仅未损害生成质量，反而通过引入空间约束增强了文本-视觉对齐和帧间连贯性。

**控制精度。** 在简单轨迹上，Motion-Zero 的 mIoU 达到 0.54，AP50 达到 0.64，检测覆盖率 Cov. 达到 0.96，Chamfer Distance（CD）低至 0.07。在更具挑战性的 17 条复杂轨迹设置下，Motion-Zero 在所有控制指标上均优于零样本对比方法 TrailBlazer 和 Peekaboo：mIoU 达到 0.55（TrailBlazer 0.50），AP50 达到 0.67（TrailBlazer 0.61），Cov. 达到 0.97（TrailBlazer 0.91），CD 为 0.07（Table 1 右半部分）。值得注意的是，Peekaboo 在复杂轨迹上的 Cov. 仅为 0.70，表明其难以在完整轨迹上保持对运动物体的持续检测，而 Motion-Zero 的 0.97 覆盖率证明了其轨迹级控制的完整性。

**跨模型泛化。** 在 ModelScope 上的实验同样验证了 Motion-Zero 的即插即用能力，定性结果（Fig.3）显示其能在不同模型架构上实现一致的轨迹控制效果，无需任何模型专属的微调。

**用户研究。** 60 名参与者的主观评测（Cronbach's α = 0.901）显示，Motion-Zero 在外观质量（4.75 vs TrailBlazer 3.32）、时序一致性（4.57 vs 3.32）和控制能力（4.67 vs 3.40）三个维度上均显著优于 TrailBlazer（Table 3）。

### 消融实验

消融实验（Table 2）揭示了三个核心模块各自的贡献及其因果机制。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2401_10150/figures/005_Table_2.jpg]]
*Table 2: The table of ablation study on different modules*

**空间约束（SC）是控制能力的核心。** 移除 SC 后，mIoU 从 0.54 骤降至 0.18（降幅 67%），Text Align 和 Inter-frame Consistency 也同步下降。这表明仅靠初始噪声先验（INPM）无法实现精确的位置控制，交叉注意力图上的空间约束损失是实现轨迹对齐的因果瓶颈。注意力图可视化（Fig.5）进一步证实，SC 能将目标 token 的注意力响应有效约束在用户指定的边界框内，而基线模型的注意力分布则呈发散状态。

**初始噪声先验模块（INPM）保障外观稳定性。** 移除 INPM 后，Text Align 明显下降，且生成物体出现严重变形甚至脱离画面（Fig.7 第二行：“the lion's body undergoes significant deformation”）。INPM 通过 DDIM Inversion 从元视频中提取位置先验噪声并与随机噪声局部混合（λ_p = 0.8 为最优经验值，Fig.14），为运动物体提供了稳定的外观和位置初始化，是高质量生成的前提条件。

**偏移时序注意力（STAM）维持运动连续性。** 移除 STAM 后，运动物体出现模糊和变形（Fig.7 末行：“the lion's legs undergo deformation and become blurred”），Text Align 同步下降。STAM 通过将各帧目标框区域平移对齐至首帧位置后进行时序注意力计算，再移回原位，解决了标准时序注意力在运动物体场景下因像素坐标不对齐导致的内容混合问题，是保证运动物体时序一致性的关键设计。

**超参数敏感性。** 约束施加步数 T1 存在质量-控制强度的权衡（Fig.8）：T1 = 10 为最优，更大的 T1 虽然增强控制但会损害物体身份保持和画面清晰度。损失权重 λ_i 和 λ_o 在 1.0 附近表现最优（Fig.9），λ_s 取 0.5 时外观连续性最佳（Fig.10），λ_c 取 0.05 时中心对齐效果最好（Fig.11）。

### 失败模式与局限性

尽管 Motion-Zero 在零样本运动控制上取得了突破性进展，但仍存在以下局限：

1. **继承基模型缺陷。** 生成性能完全依赖于预训练基础模型的能力。当基础模型本身存在物体变形、背景空洞等问题时，控制结果依然会继承这些伪影。这意味着 Motion-Zero 的上限受限于底层视频扩散模型的质量。

2. **超参数缺乏自动化。** 当前所有超参数（λ 序列、T1、λ_p 等）均为经验设定。当应用于新的基础模型或不同分辨率的生成任务时，可能需要人工重新调整参数以获得最优效果，缺乏自动化的参数适配机制。

3. **单物体与无场景语义交互。** 框架当前仅支持控制单个物体的轨迹，且轨迹由用户直接指定为边界框序列，缺乏与场景语义的智能交互（如自动避障、符合物理规律的路径规划）。在多物体场景下，物体间的遮挡、交互以及注意力冲突问题尚未解决。

4. **质量-控制权衡。** 约束施加步数等设计存在固有的质量-控制强度权衡：过强的控制可能导致物体身份丢失和画面模糊，需要在具体应用中根据需求进行折中。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2401_10150/figures/003_Table_1.jpg]]
*Table 1: Automatic metric on baseline methods and SOTA methods. The left half indicates the quality of the generation, while the right half demonstrates the control capability of the model. All metrics expect CD to be such that higher values(↑) indicate better performance. (c.) means the method is tested in complex trajectories. Align means Text Align, Cons. means Consistency and Pick. means PickScore*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2401_10150/figures/010_Figure_7.jpg]]
*Figure 7: Ablation studies on different components. We use ZeroScope as our baseline model. To demonstrate the coherence of the generated object’s motion, we captured every other frame, resulting in a total of 6 frames. The prompt is A lion is walking on the field. Zoom in for the best view*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2401_10150/figures/004_Figure_3.jpg]]
*Figure 3: Quality comparison results on different methods. We take one frame from every three frames. The input prompt: A fish is swimming in the sea. We employed ModelScope (a) and ZeroScope (b) as our baseline models and compared the effect of incorporating additional prompts with the integration of our Motion-Zero. In addition, we conducted a comparative analysis with TrailBlazer and Peekaboo*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2401_10150/figures/011_Figure_8.jpg]]
*Figure 8: Ablation studies on T1 ranging from 0 to 30. The prompt is A squirrel descending a tree after gathering nuts. Zoom in for the best view*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2401_10150/figures/017_Figure_14.jpg]]
*Figure 14: Ablation studies on different*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2401_10150/figures/012_Figure_9.jpg]]
*Figure 9: Ablation studies on different*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2401_10150/figures/015_Figure_10.jpg]]
*Figure 10: Ablation studies on different*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2401_10150/figures/016_Figure_11.jpg]]
*Figure 11: Ablation studies on different*



## 定位与知识库关联

### 与基线方法的关系

**预训练视频扩散模型基线。** Motion-Zero以冻结的预训练文本到视频扩散模型为底层引擎，主要实验采用 **ZeroScope**（Sterling, 2023）作为默认基线，并在 **ModelScope**（Wang et al., 2023b）上验证跨模型通用性。这两类模型均基于标准视频扩散训练损失（Eq.1）和3D U-Net架构，在推理时从随机高斯噪声 $z_T \sim N(0, I)$ 出发，经多步去噪生成视频。Motion-Zero的核心主张是：无需修改模型权重，仅通过操纵初始噪声分布、交叉注意力图和时序注意力机制，即可赋予任意预训练视频扩散模型精确的物体轨迹控制能力。

**零样本运动控制方法。** 与Motion-Zero同属“免训练推理时控制”范式的代表性工作包括：

- **TrailBlazer**（Ma, Lewis, and Kleijn, 2023）：通过操纵交叉注意力图实现简单的运动方向控制。Table 1显示其在复杂轨迹上的控制精度（mIoU 0.50, AP50 0.61, Cov. 0.91）全面落后于Motion-Zero（mIoU 0.55, AP50 0.67, Cov. 0.97），且用户研究中外观、一致性、控制能力三项评分（3.32/3.32/3.40）均显著低于Motion-Zero（4.75/4.57/4.67）。
- **Peekaboo**（Jain et al., 2024）：基于掩码注意力的零样本空间控制方法，在复杂轨迹上的控制指标（mIoU 0.42, AP50 0.44, Cov. 0.81）与Motion-Zero差距更为明显。

Motion-Zero相较于上述方法的本质差异在于：它不仅依赖交叉注意力图的空间约束（SC），还引入了初始噪声先验模块（INPM）和偏移时序注意力机制（STAM），形成了“位置先验—空间约束—时序对齐”三位一体的控制链路，从而在保持生成质量的同时实现更精确的轨迹控制。

**需要训练的运动控制方法。** **MotionCtrl**（Wang et al., 2023d, arXiv）代表了需要大规模标注数据训练的SOTA轨迹控制方法。Fig.6的定性对比表明，Motion-Zero在零样本条件下可达到与其可比较的控制效果，但Motion-Zero无需任何训练数据和微调，具备即插即用的跨模型迁移能力。这一对比凸显了Motion-Zero的核心优势：将控制能力从“训练获取”转变为“推理时注入”。

### 适用边界

**模型依赖边界。** Motion-Zero的控制性能完全继承自底层预训练模型。当基础模型本身存在物体变形、背景空洞或运动模糊等生成缺陷时，控制结果依然会保留这些问题。这意味着Motion-Zero的实际上限由所选择的视频扩散模型决定，而非由控制框架本身约束。

**控制对象边界。** 当前框架仅支持单个物体的轨迹控制，且轨迹由用户以边界框序列形式直接指定。缺乏对多物体交互（遮挡、碰撞）、场景语义理解（自动避障、物理规律约束）的支持。轨迹规划完全依赖用户输入，不具备叙事式或语义驱动的自动路径生成能力。

**参数敏感性边界。** 关键超参数为经验设定（$\lambda_i = \lambda_o = 1$, $\lambda_c = 0.05$, $\lambda_s = 0.5$, $\lambda_p = 0.8$, $T_1 = 10$），当迁移至新的基础模型时，可能需要重新调整参数以获得最优效果。消融实验（Fig.14, Fig.8）表明，$\lambda_p$ 偏离0.8会导致轨迹控制失效，$T_1$ 过大虽增强控制但损害物体身份保持和清晰度，揭示了控制强度与生成质量之间的内在权衡。

### 局限与开放问题

**已确认的局限。**

1. **基础模型质量依赖**：生成性能完全受限于底层模型，无法修正预训练模型的固有缺陷。
2. **单物体控制限制**：仅支持单个运动物体的轨迹控制，无法处理多物体场景。
3. **参数手动调节**：超参数为经验设定，缺乏自动化的跨模型参数适配机制。
4. **质量-控制权衡**：约束施加步数 $T_1$ 和空间损失权重存在控制精度与视觉质量之间的折衷，过强控制导致物体身份丢失和画面模糊（Fig.8, Fig.7）。

**开放问题。**

1. **语义交互式轨迹控制**：如何实现物体运动轨迹与视频背景的语义交互？例如，在指定目标点后自动规划避障路径，或根据场景上下文生成符合物理规律的轨迹，实现叙事式控制。
2. **多物体协同控制**：当同时控制多个运动物体时，如何解决物体间的遮挡关系、交互行为建模以及交叉注意力图中的token冲突问题？
3. **自适应参数调节**：能否设计一种机制，自动针对不同基础模型和应用场景调整关键超参数（如 $\lambda$ 序列、$T_1$、$\lambda_p$），消除手动调参的负担？
4. **控制范式泛化**：基于注意力约束的零样本控制理念能否扩展到其他条件维度？例如摄像机运动控制、物体姿态变化、光照条件操纵等更一般的可控生成任务。

### 知识库定位

Motion-Zero在可控视频生成领域的方法谱系中占据“零样本推理时控制”这一独特位置。与需要训练的MotionCtrl等方法和基于简单注意力操纵的TrailBlazer等方法相比，Motion-Zero通过INPM-SC-STAM三模块协同，在控制精度和生成质量之间建立了新的零样本基准。其核心贡献在于揭示了预训练视频扩散模型已隐含丰富的物体运动知识，只需通过推理时的噪声先验注入和注意力引导即可显式化这些知识，为后续的免训练可控生成研究提供了“操纵潜变量和注意力图”这一可泛化的技术范式。



## 原文 PDF

![[paperPDFs/arxiv_2024/Motion_Zero_Zero_Shot_Moving_Object_Control_Framework_for_Diffusion_Based_Video_Generation.pdf]]
