---
title: "EditCtrl: Disentangled Local and Global Control for Real-Time Generative Video Editing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EditCtrl_Disentangled_Local_and_Global_Control_for_Real_Time_Generative_Video_Editing.pdf
project_link: "https://yehonathanlitman.github.io/edit_ctrl"
code_link: null
aliases:
- EditCtrl
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过仅处理蒙版区域内的局部令牌，并结合轻量级的全局时间上下文嵌入来保证视频整体一致性，使得计算量正比于编辑区域大小，而非整个视频分辨率。
primary_logic: 利用冻结预训练视频扩散模型上的轻量适配器（局部编码器和全局嵌入器），可以在不修改基础模型权重的情况下实现计算按需分配，既保持了生成质量，又大幅提升了效率，并能灵活组合其他控制变体。
claims:
- EditCtrl 的局部视频上下文模块仅对蒙版令牌进行操作，计算成本与编辑大小成正比。
- EditCtrl 比现有最先进生成式编辑方法计算效率高 10 倍以上。
- 在 VPBench-Edit 和 DAVIS 等基准上，EditCtrl 在编辑质量、背景保留和文本对齐方面均达到或超越了全注意力基线，同时吞吐量大幅提升（如 1.5B 模型 FPS 4.67 vs VACE 1.3B 的 0.66）。
- VPBench-Edit 上 FPS（越高越好） = 4.67 (EditCtrl 1.5B)
---

# EditCtrl: Disentangled Local and Global Control for Real-Time Generative Video Editing

> [!tip] 核心洞察
> 利用冻结预训练视频扩散模型上的轻量适配器（局部编码器和全局嵌入器），可以在不修改基础模型权重的情况下实现计算按需分配，既保持了生成质量，又大幅提升了效率，并能灵活组合其他控制变体。

| 字段 | 内容 |
|------|------|
| 中文题名 | EditCtrl：用于实时生成式视频编辑的解耦局部与全局控制 |
| 英文题名 | EditCtrl: Disentangled Local and Global Control for Real-Time Generative Video Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.15031) · [Project](https://yehonathanlitman.github.io/edit_ctrl) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | EditCtrl |
| Dataset | VPBench-Edit, VPBench-Inp |

> [!tip] 效果简介
> - VPBench-Edit 上，FPS（越高越好） 4.67 (EditCtrl 1.5B) vs 0.66 (VACE 1.3B) (+4.01 (≈7× speedup))；PSNR↑ 24.16 (EditCtrl 1.5B) vs 23.84 (VACE 1.3B) (+0.32)。
> - VPBench-Inp (DAVIS) 上，PSNR↑ 23.17 (EditCtrl 1.3B) vs 22.62 (VACE 1.3B) (+0.55)。
> - VPBench-Inp (VPBench) 上，PSNR↑ 25.44 (EditCtrl 1.5B) vs 22.62 (VACE 1.3B) (+2.82)。

## 概要

现有的生成式视频编辑方法，如 **ReVideo**（Mou et al., NeurIPS 2024）、**VideoPainter**（Bian et al., CVPR 2025）以及 **VACE**（Jiang et al., ICCV 2025），在修复视频时始终处理完整的时空上下文，导致计算开销巨大，尤其对于局部、稀疏的编辑任务。全注意力机制使得计算成本不随修复蒙版的大小而缩放，无法实现实时性能。

针对这一瓶颈，**EditCtrl** 提出了一种解耦的局部与全局控制框架。其核心思路是：将计算范围从全空间全注意力，切换为仅对蒙版编辑区域进行局部计算，使计算量与蒙版大小成正比；同时，引入一个轻量级的全局时间上下文嵌入器，从下采样的背景视频中提取紧凑的全局线索，以低开销保证视频整体的时间一致性与场景连贯性。整套框架建立在冻结的预训练文本到视频扩散模型之上，仅通过 LoRA 微调局部编码器并训练轻量全局嵌入器，无需修改基础模型权重，即可实现计算按需分配，并灵活组合其他控制变体。

在 VPBench-Edit 和 DAVIS 等公开基准上，EditCtrl 在编辑质量、背景保留和文本对齐方面均达到或超越了全注意力基线。以 1.5B 参数模型为例，EditCtrl 的推理吞吐量达到 4.67 FPS，而全注意力的 VACE 1.3B 模型仅为 0.66 FPS，计算效率提升超过 10 倍。消融实验进一步证实，解耦的局部与全局适配器是同时获得高效率与高质量的关键：移除全局嵌入器会导致 CLIP 评分和 PSNR 明显下降，而完整的双适配器设计在保持高吞吐量的同时，编辑质量甚至超越了全注意力模型。

EditCtrl 的主要局限在于：高运动场景下可能产生伪影和不正确的场景交互；当编辑蒙版非常大时，细粒度编辑变得困难；背景下采样至固定 256×256 分辨率在极端长宽比或复杂场景下可能丢失细节；以及基于光流的内容传播在长期编辑中可能出现误差累积。

生成式视频编辑旨在根据文本提示和用户指定的编辑区域，对视频进行局部内容修改，同时保持未编辑区域的完整性和整体时间一致性。这一任务在增强现实、视频后期制作和交互式内容创作中具有广泛的应用前景。然而，当前的主流方法面临一个根本性的效率瓶颈：**现有生成式视频编辑方法在修复视频时始终处理完整的时空上下文，导致计算开销巨大，尤其对于局部、稀疏的编辑**。全注意力机制使得计算成本不随修复蒙版的大小而缩放，无法实现实时性能。

具体而言，以 **VACE**（Jiang et al., ICCV 2025）为代表的全注意力视频编辑方法，在去噪过程中对视频所有帧的全空间进行全注意力计算，其计算量与视频分辨率成正比，而与实际需要编辑的区域大小无关。这意味着，即使用户仅希望修改画面中一个微小的物体，系统仍需处理整个视频的所有令牌，造成严重的计算浪费。类似地，**ReVideo**（Mou et al., NeurIPS 2024）和 **VideoPainter**（Bian et al., CVPR 2025）等基于扩散模型的方法同样继承了这一全注意力范式，难以在消费级硬件上实现实时交互。传统的视频修复方法如 **ProPainter**（Zhou et al., ICCV 2023）虽然不依赖生成模型，但其基于流传播的机制缺乏对高层语义和文本引导编辑的支持，无法满足生成式编辑的需求。

这一效率瓶颈的根源在于现有方法的**计算范围**设计：全注意力控制适配器 $c_\phi$ 处理完整的视频上下文，将背景信息与编辑区域信息不加区分地混合计算。这种设计虽然在理论上保证了全局一致性，但在实际应用中导致了不可接受的延迟——例如，VACE 1.3B 模型在 NVIDIA A6000Ada 上的吞吐量仅为 0.66 FPS，远未达到实时编辑的门槛。

EditCtrl 的核心动机正是打破这一计算与编辑区域大小无关的僵局。其核心洞察在于：**利用冻结预训练视频扩散模型上的轻量适配器（局部编码器和全局嵌入器），可以在不修改基础模型权重的情况下实现计算按需分配，既保持了生成质量，又大幅提升了效率，并能灵活组合其他控制变体**。通过将上下文编码解耦为仅处理蒙版区域局部令牌的局部编码器 $c_\phi$，和通过下采样背景提供全局线索的全局嵌入器 $G_\psi$，EditCtrl 实现了计算量与编辑大小成正比的理想缩放特性，为实时生成式视频编辑开辟了新的可能。

## 核心方法与创新机理

EditCtrl 的核心创新在于将生成式视频编辑的计算范式从“全注意力全局处理”转变为“按需局部计算 + 轻量全局引导”的解耦架构。这一转变直接回应了现有方法的根本瓶颈：**计算成本不随编辑区域大小缩放**。

### 关键瓶颈与因果调控

现有生成式视频编辑方法（如 **VACE** (Jiang et al., ICCV 2025)、**VideoPainter** (Bian et al., CVPR 2025)）在修复视频时始终处理完整的时空上下文，全注意力机制使得计算开销与视频总分辨率成正比，即便用户仅编辑画面中一个微小区域，仍需为整个视频付出相同的算力。这从根本上限制了实时编辑的可能性。

EditCtrl 识别出这一瓶颈的因果调控点：**计算范围应当与编辑蒙版大小成正比**。通过仅对蒙版区域内的局部令牌进行操作，EditCtrl 实现了“计算按需分配”——编辑一个 10% 面积的区域，计算量即降至全注意力的约 10%。

### 核心机制：解耦的局部与全局控制

为实现上述目标，EditCtrl 引入了一项关键架构创新：将传统的单一全注意力控制适配器解耦为两个独立组件：

| 组件 | 功能 | 输入 | 计算特性 |
|------|------|------|----------|
| **局部上下文编码器** $c_\phi$ | 负责编辑区域的精细生成控制 | 仅位于蒙版内的局部控制令牌 $\mathbf{C}_{\text{local}}$ | 计算量与蒙版面积成正比 |
| **全局上下文嵌入器** $G_\psi$ | 提供视频级别的时间一致性、光照、运动等全局线索 | 下采样至固定分辨率 256×256 的背景视频 | 计算开销恒定且极小 |

这一解耦设计的精妙之处在于：**局部编码器确保了编辑质量与效率的平衡，而全局嵌入器以极低的固定成本弥补了局部计算可能丢失的视频整体一致性**。消融实验证实了这一设计的必要性——移除全局嵌入器（No G）导致 CLIP 评分从 9.58 降至 9.41，PSNR 从 24.16 降至 23.80；而仅使用局部编码器的朴素版本在质量上明显劣于完整模型。

### 训练策略创新：分段损失函数

EditCtrl 采用了一种分段训练策略，通过损失函数切换来稳定解耦模块的学习过程：

$$\mathcal{L} = \begin{cases} \mathcal{L}_{\phi}, & \text{if } k < n, \\ \mathcal{L}_{\psi}, & \text{if } k \geq n. \end{cases}$$

在前 $n$ 次迭代中，仅优化局部编码器损失 $\mathcal{L}_{\phi}$，使模型先学会在蒙版区域内生成高质量内容；之后切换为联合优化全局嵌入器损失 $\mathcal{L}_{\psi}$，引入全局上下文以提升视频整体一致性。这种“先局部后全局”的训练顺序避免了两个适配器在训练初期相互干扰，是解耦架构成功收敛的关键。

### 与 Baseline 的核心差异

与全注意力基线相比，EditCtrl 在以下三个维度实现了根本性改变：

1. **计算范围**：从“全帧全空间全注意力”变为“仅蒙版区域局部计算”，计算量与蒙版大小成正比。
2. **上下文编码**：从“单一全注意力适配器处理完整视频上下文”变为“局部编码器 + 全局嵌入器”的解耦设计。
3. **模型微调策略**：从“微调完整控制模块或基础模型”变为“仅通过 LoRA（秩 128）微调局部编码器并训练轻量全局嵌入器，基础模型完全冻结”。这一策略不仅保护了预训练模型的生成能力，还使 EditCtrl 能够灵活组合其他控制变体（如风格 LoRA），无需修改基础模型权重。

### 效率与质量的量化突破

这一系列创新带来的直接结果是：EditCtrl 在 VPBench-Edit 基准上的吞吐量达到 **4.67 FPS**（1.5B 模型），而全注意力基线 VACE（1.3B 模型）仅为 **0.66 FPS**，加速比超过 **7 倍**。更关键的是，在实现这一效率飞跃的同时，EditCtrl 的编辑质量（PSNR 24.16 vs 23.84）和文本对齐度均超越全注意力基线，验证了“解耦局部-全局控制”这一核心洞察的正确性：**全注意力中的大量计算实际上是冗余的，轻量级的全局线索足以替代昂贵的全局注意力计算**。

EditCtrl 的整体设计围绕一个核心原则展开：**计算量应与编辑区域大小成正比，而非整个视频的分辨率**。为此，框架将视频编辑任务解耦为局部生成与全局一致性两个正交的子问题，并分别通过轻量级适配器在冻结的预训练视频扩散模型上实现。

### 输入输出流

框架接受三个输入：
- **源视频** $\mathbf{V}_{\text{src}}$：待编辑的原始视频
- **目标编辑蒙版** $\mathbf{V}_m$：指定需要修改的时空区域
- **文本提示** $\mathbf{p}$：描述期望编辑内容的自然语言指令

输出为编辑后的视频，其中蒙版区域的内容被替换为与文本提示一致的新内容，同时非蒙版区域（背景）得到完整保留。

### Pipeline 模块与数据流

整个处理流程可概括为五个关键阶段，对应 Figure 2 所示的架构：

![[assets/figures/papers/paper_list_l864_https_arxiv_org_abs_2602_15031/figures/002_Figure_2.jpg]]
*Figure 2: EditCtrl Video Diffusion Framework Overview. EditCtrl edits a source video given a target edit mask. Foreground content is masked out, giving the background video that is also down-sampled to a constant resolution regardless of the original resolution. The compact global context of the down-sampled background video and the local context at the mask edit region are then encoded. These are given to trainable local and global adapters inside a pretrained text-to-video diffusion model that denoises tokens*

**1. 背景视频提取与下采样**

首先，根据编辑蒙版将源视频中的前景内容抹除，得到仅包含背景信息的视频 $\mathbf{V}_b$。随后，将 $\mathbf{V}_b$ 下采样至固定分辨率 $256 \times 256$，得到紧凑的全局上下文表示 $\mathbf{V}_b^{\downarrow}$。这一固定分辨率的设计使得全局上下文的计算开销与原始视频分辨率解耦，即使处理 4K 视频也能保持恒定。

**2. 控制上下文构建**

使用视频 VAE 编码器 $E$ 将下采样背景视频编码为潜空间特征，再与下采样后的蒙版进行通道维拼接，形成完整的控制上下文 $\mathbf{C}$。这一拼接操作将“在哪里编辑”（蒙版）和“周围是什么”（背景）的信息统一编码。

**3. 局部上下文编码器（$c_\phi$）**

控制上下文 $\mathbf{C}$ 中位于蒙版区域之外的令牌被全部遮蔽，仅保留编辑区域内的**局部上下文令牌** $\mathbf{C}_{\text{local}}$。这些令牌通过可训练的局部编码器 $c_\phi$ 处理，其输出以类似 ControlNet 的方式注入到预训练视频 DiT 的选定 Transformer 层中。由于 $c_\phi$ 仅处理蒙版区域对应的稀疏令牌，其计算量严格正比于编辑区域大小——这是 EditCtrl 实现实时性能的核心机制。

**4. 全局上下文嵌入器（$G_\psi$）**

为保证局部生成内容与整个视频在光照、运动、风格上的时间一致性，框架引入了一个轻量级的全局嵌入器 $G_\psi$。它接收两个输入：来自下采样背景 $\mathbf{V}_b^{\downarrow}$ 的全局上下文令牌，以及 DiT 内部产生的查询特征令牌。$G_\psi$ 通过交叉注意力机制计算全局感知的调制信号，并将其经零初始化线性层叠加到 DiT 的交叉注意力特征上：

$$\mathbf{x} = \mathbf{x} + \mathbf{W}_0 \cdot \text{Attention}(\mathbf{Q}, \mathbf{K}_g, \mathbf{V}_g)$$

这种设计以极小的额外计算开销（全局令牌来自低分辨率背景）为局部生成提供视频级别的全局线索。

**5. 去噪与散射整合**

冻结的预训练文本到视频扩散模型（DiT）接收文本提示 $\mathbf{p}$、局部编码器输出和全局嵌入器调制信号，仅对蒙版区域内的噪声令牌 $\mathbf{z}^t$ 进行去噪。去噪完成后，更新后的令牌被散射回编码后的源视频潜空间中的对应蒙版位置，最终通过 VAE 解码器得到编辑完成的视频。

### 训练策略

EditCtrl 采用**分段训练损失**（Eq. 7）来稳定优化过程：

$$\mathcal{L} = \begin{cases} \mathcal{L}_{\phi}, & \text{if } k < n, \\ \mathcal{L}_{\psi}, & \text{if } k \geq n. \end{cases}$$

在前 $n$ 次迭代中，仅使用掩码感知的局部编码器损失 $\mathcal{L}_{\phi}$ 对 $c_\phi$ 进行 LoRA 微调（秩 128）；之后切换为全局嵌入器损失 $\mathcal{L}_{\psi}$，同时优化 $G_\psi$ 并继续微调 $c_\phi$。基础视频扩散模型的权重全程冻结，这保证了预训练生成能力不被破坏，同时允许 EditCtrl 灵活组合其他控制变体（如风格 LoRA，见 Figure 7）。

### 效率来源的因果机制

EditCtrl 的效率优势来自两个相互协同的设计决策：

| 设计要素 | 机制 | 效果 |
|---------|------|------|
| 局部令牌计算 | $c_\phi$ 仅处理蒙版区域令牌，DiT 仅对蒙版区域去噪 | 计算量 $\propto$ 编辑面积，而非全视频分辨率 |
| 下采样全局上下文 | $G_\psi$ 在 $256 \times 256$ 固定分辨率上提取全局线索 | 全局一致性开销恒定，与原始分辨率无关 |

这一解耦使得 EditCtrl 在 1.5B 参数规模下可达 **4.67 FPS**，而全注意力基线 VACE（1.3B）仅为 **0.66 FPS**（Table 1），实现了约 7 倍的吞吐量提升，同时编辑质量（PSNR 24.16 vs 23.84）和文本对齐度均保持领先。

### 补充图表

![[assets/figures/papers/paper_list_l864_https_arxiv_org_abs_2602_15031/figures/001_Figure_1.jpg]]
*Figure 1: EditCtrl: A Real-time Generative Video Editing Pipeline. EditCtrl supports complex, prompt-guided edits on 4K videos, simultaneously handling an arbitrary number of user-defined masks (Top). To maintain real-time performance, our inference pipeline dynamically allocates compute proportional to the edit mask size (Middle). EditCtrl also intelligently propagates object edits from initial frames into the future (after the orange line), ensuring high temporal and object consistency in the resulting edit (Bottom)*

EditCtrl 的核心设计思想是将视频编辑的控制信号解耦为**局部上下文**与**全局上下文**两个独立通路，使得去噪计算仅作用于编辑蒙版区域，从而将计算复杂度从整个视频分辨率降低为与蒙版面积成正比。整个框架建立在冻结的预训练文本到视频扩散模型之上，仅训练轻量级适配器，不修改基础模型权重。

### 基础扩散模型与条件控制

标准的文本到视频扩散模型通过最小化去噪损失来学习生成过程：

$$ \mathcal{L}_{\mathrm{DM}} = \| \epsilon_{\theta} \left( \bar{\mathbf{z}}^{t}, t; \mathbf{p} \right) - \epsilon_{t} \|_{2}^{2} \tag{1} $$

其中 $\bar{\mathbf{z}}^{t}$ 为完整视频潜空间的噪声表示，$t$ 为时间步，$\mathbf{p}$ 为文本提示，$\epsilon_{\theta}$ 为去噪网络，$\epsilon_{t}$ 为真实噪声。

引入控制适配器 $c_{\phi}$ 后，条件扩散损失扩展为：

$$ \mathcal{L}_{\mathrm{CDM}} = \| \epsilon_{\theta} \left( \bar{\mathbf{z}}^{t}, t; \mathbf{p}, c_{\phi}(\mathbf{C}) \right) - \epsilon_{t} \|_{2}^{2} \tag{2} $$

其中 $\mathbf{C}$ 为背景视频与下采样蒙版的通道拼接。这一形式仍要求适配器处理完整的时空上下文，计算开销不随编辑区域缩小而降低。

### 惰性扩散损失：计算按需分配的第一步

EditCtrl 首先引入**惰性扩散损失**（Lazy Diffusion Loss），将去噪损失的计算范围限制在蒙版区域：

$$ \mathcal{L}_{\mathrm{Lazy-DM}} = \| \epsilon_{\theta} \left( \mathbf{z}^{t} \oplus \mathbf{C}_{\mathrm{enc}}, t; \mathbf{p} \right) - \epsilon_{t} \odot \mathbf{V}_{m}^{\downarrow} \|_{2}^{2} \tag{3} $$

其中 $\mathbf{z}^{t}$ 为仅覆盖编辑区域的局部噪声令牌，$\mathbf{C}_{\mathrm{enc}}$ 为编码后的控制信息，通过通道拼接注入去噪网络。$\mathbf{V}_{m}^{\downarrow}$ 为下采样后的二值蒙版，$\odot$ 表示逐元素乘法。该损失确保梯度仅从需要编辑的区域反向传播，但此时控制适配器仍需处理完整上下文。

### 局部上下文编码器损失：解耦的核心

为实现真正的局部计算，EditCtrl 将控制上下文 $\mathbf{C}$ 中位于下采样蒙版外部的令牌全部遮蔽，仅保留局部上下文令牌 $\mathbf{C}_{\mathrm{local}}$，并据此微调局部编码器 $c_{\phi}$：

$$ \mathcal{L}_{\phi} = \| \epsilon_{\theta} \left( \mathbf{z}^{t}, t; \mathbf{p}, c_{\phi}(\mathbf{C}_{\mathrm{local}}) \right) - \epsilon_{t} \odot \mathbf{V}_{m}^{\downarrow} \|_{2}^{2} \tag{4} $$

此时 $c_{\phi}$ 仅接收编辑区域内的局部令牌，其计算量与蒙版面积成正比，实现了**计算按需分配**的核心目标。该编码器的输出通过残差连接注入 DiT 的选定 Transformer 层，指导局部区域的生成。

### 全局上下文嵌入器：轻量级时间一致性保障

纯粹的局部生成缺乏对视频整体时间一致性、光照和运动的感知。EditCtrl 引入一个轻量级**全局嵌入器** $G_{\psi}$，将下采样至固定分辨率 $256 \times 256$ 的背景视频 $\mathbf{V}_{b}^{\downarrow}$ 编码为全局令牌，通过交叉注意力调制局部生成过程：

$$ \mathbf{x} = \mathbf{x} + \mathbf{W}_{0} \cdot \mathrm{Attention}(\mathbf{Q}, \mathbf{K}_{g}, \mathbf{V}_{g}) \tag{5} $$

其中 $\mathbf{x}$ 为 DiT 中的交叉注意力特征，$\mathbf{Q}$ 来自噪声令牌，$\mathbf{K}_{g}, \mathbf{V}_{g}$ 由 $G_{\psi}$ 从全局上下文令牌中投影得到。$\mathbf{W}_{0}$ 为零初始化线性层，确保训练初期全局模块不干扰已收敛的局部编码器。

引入全局嵌入器后的完整损失为：

$$ \mathcal{L}_{\psi} = \| \epsilon_{\theta} \left( \mathbf{z}^{t}, t; \mathbf{p}, G_{\psi}(\mathbf{C}_{\mathrm{global}}), c_{\phi}(\mathbf{C}_{\mathrm{local}}) \right) - \epsilon_{t} \odot \mathbf{V}_{m}^{\downarrow} \|_{2}^{2} \tag{6} $$

### 分段训练策略

为稳定训练过程，EditCtrl 采用**分段训练损失**，在前 $n$ 次迭代仅优化局部编码器，之后切换为联合优化全局嵌入器：

$$ \mathcal{L} = \begin{cases} \mathcal{L}_{\phi}, & \text{if } k < n, \\ \mathcal{L}_{\psi}, & \text{if } k \geq n. \end{cases} \tag{7} $$

这一策略确保局部编码器先学会在有限上下文下生成合理内容，随后全局嵌入器在此基础上注入时间一致性信息，避免两者在训练初期相互干扰。实验中使用 LoRA（秩 128）微调局部编码器，全局嵌入器则全参数训练，基础 DiT 模型完全冻结。

### 关键模块总结

| 模块 | 输入 | 功能 | 计算特性 |
|------|------|------|----------|
| 局部上下文编码器 $c_{\phi}$ | $\mathbf{C}_{\mathrm{local}}$（仅蒙版区域令牌） | 指导局部编辑区域的精细生成 | 计算量与蒙版面积成正比 |
| 全局上下文嵌入器 $G_{\psi}$ | $\mathbf{V}_{b}^{\downarrow}$（下采样背景视频） | 提供视频级时间一致性、光照、运动等全局线索 | 固定低分辨率输入，开销极小 |
| 冻结 DiT 基础模型 | 噪声令牌、文本提示、适配器输出 | 执行实际去噪生成 | 完全冻结，无训练开销 |

通过上述解耦设计，EditCtrl 在保持生成质量的同时，将推理计算量从全注意力方法的 $\mathcal{O}(H \times W \times T)$ 降低为 $\mathcal{O}(A_{\mathrm{mask}} \times T)$，其中 $A_{\mathrm{mask}}$ 为蒙版面积，$T$ 为帧数，实现了 10 倍以上的计算效率提升。

### 补充图表

![[assets/figures/papers/paper_list_l864_https_arxiv_org_abs_2602_15031/figures/003_Figure_3.jpg]]
*Figure 3: EditCtrl: Local and Global Control Modules. Given the source video*

## 实验与关键发现

EditCtrl 的核心实验目标是在保持或超越全注意力基线编辑质量的同时，验证其计算效率的显著提升。所有实验均在 NVIDIA A6000Ada GPU 上进行，FPS 测量仅统计扩散模型推理吞吐量（排除 VAE 编解码时间），且统一使用 25 步 DDPM 去噪，确保公平比较。

### 视频编辑主结果

在 VPBench-Edit 基准上，EditCtrl 在编辑质量、背景保留和文本对齐方面全面超越现有方法，同时推理效率提升超过一个数量级。如表 1 所示，EditCtrl 1.5B 模型以 **4.67 FPS** 的吞吐量运行，而全注意力的 **VACE**（Jiang et al., ICCV 2025）1.3B 仅达到 0.66 FPS，加速约 7 倍。更关键的是，EditCtrl 在 PSNR（24.16 vs 23.84）和 CLIP 文本对齐分数（9.58 vs 9.56）上均优于 VACE。即使与计算开销更大的 VACE 16B（FPS 仅 0.10）相比，EditCtrl 1.5B 在 PSNR 上仍有 0.32 dB 的优势，而 EditCtrl 16B 达到 24.37 PSNR，进一步拉大质量差距。定性对比（图 4）显示，基线方法如 **ReVideo**（Mou et al., NeurIPS 2024）和 **VideoPainter**（Bian et al., CVPR 2025）要么编辑失败，要么生成内容的外观和融合效果较差，而 EditCtrl 生成的编辑内容视觉吸引力强且结构连贯。

### 视频修复主结果

在视频修复任务上，EditCtrl 同样匹配或超越全注意力基线，同时大幅提升效率。在 DAVIS 数据集上，EditCtrl 1.3B 达到 23.17 PSNR，超过 VACE 1.3B 的 22.62 PSNR（+0.55 dB）；在 VPBench-Inp 上，EditCtrl 1.5B 以 25.44 PSNR 显著领先 VACE 1.3B 的 22.62 PSNR（+2.82 dB）。吞吐量方面，EditCtrl 1.5B 在 VPBench-Inp 上达到 5.57 FPS，在 DAVIS 上达到 5.24 FPS，而传统基于流传播的方法 **ProPainter**（Zhou et al., ICCV 2023）的 FPS 远低于 1。定性结果（图 5）表明，即使使用全注意力，基线方法仍难以生成连贯且视觉上吸引人的修复内容，而 EditCtrl 以更少的计算量成功生成与场景对齐的高保真内容。

### 消融实验

消融实验（表 3）系统验证了局部编码器和全局嵌入器各自的贡献。移除全局嵌入器（No G）导致 CLIP 分数从 9.58 降至 9.41，PSNR 从 24.16 降至 23.80，证明全局时间上下文对生成质量有实质贡献。仅使用局部编码器的“朴素”变体（Naive）虽然质量明显劣于完整模型，但仍保持较高吞吐量，说明局部计算模式是效率提升的关键瓶颈。完整 EditCtrl（双适配器）在保持 4.67 FPS 高吞吐量的同时，PSNR 和文本对齐指标均超越全注意力 VACE 模型（FPS 0.10），验证了解耦设计的有效性——局部模块保证效率，全局模块补充一致性，两者协同实现了质量与速度的帕累托最优。定性消融（图 6）进一步可视化移除任一适配器对编辑质量的损害。

### 失败模式

EditCtrl 在以下场景表现出局限性（图 8）：(a) **高运动场景**下产生伪影和不正确的场景交互，这与全注意力基线类似，可能是视频 VAE 的结构性退化问题；(b) **不准确的编辑掩码**输入导致细粒度编辑困难，当掩码过大时会不必要地改变过多内容。此外，背景视频下采样至固定 256×256 分辨率虽然提高了计算鲁棒性，但在极端长宽比或复杂场景下可能丢失细节；内容传播时使用光流近似未来帧的背景，长期传播存在误差累积风险。

### 重要图表结论

- **图 1**：展示 EditCtrl 端到端实时编辑流程，支持 4K 视频上的多区域、多提示编辑，计算量随蒙版大小动态缩放。
- **表 1**：VPBench-Edit 上 EditCtrl 在 PSNR、CLIP 等指标全面领先，FPS 比 VACE 1.3B 快约 7 倍，比 VACE 16B 快约 47 倍。
- **表 2**：VPBench-Inp 和 DAVIS 修复基准上，EditCtrl 在保持或超越修复质量的同时，推理效率显著提升。
- **表 3**：消融实验证实局部编码器是效率关键，全局嵌入器是质量补充，双适配器组合实现质量与速度的双赢。

### 补充图表

![[assets/figures/papers/paper_list_l864_https_arxiv_org_abs_2602_15031/figures/005_Figure_4.jpg]]
*Figure 4: Video Editing Comparison. EditCtrl generates visually appealing and structurally coherent edited content while the baselines either fail to edit the video correctly or produce content with poor appearance and blending. EditCtrl’s localized editing greatly increases efficiency and enables real-time generative editing*

![[assets/figures/papers/paper_list_l864_https_arxiv_org_abs_2602_15031/figures/007_Figure_5.jpg]]
*Figure 5: Video Inpainting Comparison. Even with full-attention, baseline methods struggle to inpaint content that is coherent and visually appealing, while our method successfully generates high fidelity content that aligns with the scene using much less compute*

![[assets/figures/papers/paper_list_l864_https_arxiv_org_abs_2602_15031/figures/008_Table_3.jpg]]
*Table 3: Quantitative Local and Global Adapter Ablation Comparison. We observe a clear improvement in quality at a minimal reduction in efficiency with the local and global control modules. With both adapters, EditCtrl greatly increases throughput and even exceeds the full-attention model in edit quality*

![[assets/figures/papers/paper_list_l864_https_arxiv_org_abs_2602_15031/figures/009_Figure_6.jpg]]
*Figure 6: Local and Global Adapter Ablation. Removing adapter components harms video editing quality, but together they let EditCtrl perform comparably to a method operating with full-attention*

![[assets/figures/papers/paper_list_l864_https_arxiv_org_abs_2602_15031/figures/011_Figure_8.jpg]]
*Figure 8: Failure Modes for EditCtrl on High Motion (a) & Inaccurate Masks (b)*

![[assets/figures/papers/paper_list_l864_https_arxiv_org_abs_2602_15031/figures/012_Figure_9.jpg]]
*Figure 9: Content Propagation for Augmented Reality. EditCtrl is particularly suitable for deployment in augmented reality applications given its low latency and ability to propagate content to match the user’s movement*

## 定位与知识库关联

### 与基线方法的关系

EditCtrl 的核心设计逻辑是对现有全注意力视频编辑范式的根本性反思，其方法定位可从以下三个维度与基线方法建立谱系关系。

**全注意力视频编辑基线。** EditCtrl 的直接对标基线是 **VACE**（Jiang et al., ICCV 2025），后者采用全注意力控制适配器 $c_\phi$ 处理完整的时空上下文，实现对预训练文本到视频扩散模型的引导。EditCtrl 以 VACE 为基模型，继承了其 ControlNet 风格的适配器架构，但将单一的全注意力控制模块解耦为两个独立组件：仅处理蒙版区域令牌的局部上下文编码器 $c_\phi$，以及通过交叉注意力注入全局时间线索的轻量全局嵌入器 $G_\psi$。这一解耦使得 EditCtrl 在计算量上实现了质的跃迁——FPS 从 VACE 1.3B 的 0.66 提升至 EditCtrl 1.5B 的 4.67（约 7 倍加速），同时在 PSNR 等质量指标上保持或超越 VACE（24.16 vs 23.84）。值得注意的是，EditCtrl 的 16B 变体在 PSNR 达到 24.37 的同时，FPS 仍有 1.19，远高于 VACE 1.3B 的 0.66，表明解耦设计在不同模型规模下均有效。

**其他视频编辑与修复方法。** 与 **ReVideo**（Mou et al., NeurIPS 2024）等基于视频扩散模型的编辑方法相比，EditCtrl 的区别在于其计算按需分配策略——计算成本与编辑蒙版大小成正比，而非整个视频分辨率。与 **VideoPainter**（Bian et al., CVPR 2025）等全注意力生成式修复方法相比，EditCtrl 在修复质量上匹配或超越（VPBench-Inp 上 PSNR 25.44 vs VACE 22.62），同时吞吐量提升一个数量级以上。与传统基于流传播的方法 **ProPainter**（Zhou et al., ICCV 2023）相比，EditCtrl 属于生成式范式，能够根据文本提示生成全新内容，而非仅传播已有像素，适用场景更广。

**与图像域高效编辑方法的延续性。** EditCtrl 将图像域中“仅学习局部适配器而非全量微调”的思路扩展到视频域，使得基础模型权重完全冻结，从而可以灵活组合其他控制变体（如风格 LoRA），无需修改基础模型权重。这一设计使其在方法谱系中处于“冻结基模型 + 轻量适配器”路线的视频域延伸位置。

### 适用边界

EditCtrl 的适用边界由以下关键设计选择决定：

- **编辑区域规模。** 当编辑蒙版非常大时，细粒度编辑变得困难，EditCtrl 会不必要地改变过多内容。这是因为局部编码器的感受野随蒙版扩大而增加，可能导致生成内容缺乏精准控制。
- **运动幅度。** 在高运动场景下，EditCtrl 会产生 artifact 和不正确的场景交互。论文指出这可能与视频 VAE 的结构性退化有关，而非 EditCtrl 独有的问题，全注意力基线同样面临类似挑战。
- **背景下采样分辨率。** 背景视频被固定下采样至 $256\times256$ 以提供紧凑的全局上下文，这一设计在极端长宽比或复杂场景下可能丢失细节，影响全局嵌入器的线索质量。
- **内容传播的长期稳定性。** 在传播编辑内容到未来帧时，使用光流近似背景可能导致误差累积，长期传播质量下降。
- **4K 视频的 VAE 瓶颈。** 虽然 EditCtrl 的扩散推理计算与视频分辨率无关，但 VAE 编解码的开销在高分辨率下仍受 VRAM 限制，这可能成为端到端实时性的瓶颈。

### 局限与开放问题

**已识别的失效模式。** 论文明确展示了 EditCtrl 的两类典型失败案例（Figure 8）：(a) 高运动场景下产生视觉 artifact 和场景交互错误；(b) 不准确的编辑蒙版输入导致生成内容错位。前者可能与视频 VAE 的潜在空间表示能力有关，后者则暴露了方法对蒙版质量的依赖性。

**开放问题。** 基于论文的分析与讨论，以下问题有待进一步探索：

1. 如何减少视频 VAE 对背景内容的退化影响，以提升高运动场景下的生成质量？
2. 极快速运动对局部编码器的挑战如何解决？是否需要引入运动感知的局部上下文编码？
3. 在 4K 视频上，如何降低 VAE 编解码的开销以满足 VRAM 限制，实现真正的端到端实时编辑？
4. 全局嵌入器对剧烈光照变化或场景切换的适应能力如何进一步提升？
5. 对于超长视频，内容传播策略如何缓解误差漂移？是否需要引入关键帧校正机制？

这些问题指向 EditCtrl 方法的核心张力：局部计算的高效性与全局一致性的质量保障之间的平衡。当前设计通过下采样背景和交叉注意力调制实现了较好的折衷，但在极端条件下（高运动、大蒙版、长视频）仍存在改进空间。

## 原文 PDF

![[paperPDFs/CVPR_2026/EditCtrl_Disentangled_Local_and_Global_Control_for_Real_Time_Generative_Video_Editing.pdf]]
