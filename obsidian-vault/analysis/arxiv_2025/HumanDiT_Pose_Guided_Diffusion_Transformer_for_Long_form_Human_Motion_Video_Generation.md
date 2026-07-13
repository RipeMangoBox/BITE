---
title: "HumanDiT: Pose Guided Diffusion Transformer for Long-form Human Motion Video Generation"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/HumanDiT_Pose_Guided_Diffusion_Transformer_for_Long_form_Human_Motion_Video_Generation.pdf
project_link: https://agnjason.github.io/HumanDiT-page/
code_link: https://github.com/blackforest-labs/flux
aliases:
- HumanDiT
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用扩散Transformer (DiT) 替代U-Net，并引入前缀潜在参考策略和Keypoint-DiT，突破固定分辨率限制，实现统一的长序列生成与姿态迁移。
primary_logic: DiT的RoPE与3D全注意力可原生处理不同分辨率/序列长度；前缀潜在参考无需额外网络即保持身份一致性；补丁化姿态引导高效注入时空姿态信息；Keypoint-DiT生成连贯姿态序列，姿态适配器实现精准迁移。
claims:
- HumanDiT在全部测试集（Total）上取得最优FID-VID（25.5），显著优于MimicMotion（39.5）和AnimateAnyone（68.8）。
- 将最大令牌数从80K提升至480K后，SSIM从0.719升至0.838，FID-VID从33.5降至25.5，证明大容量训练对长视频质量的必要性。
- 用户研究中，HumanDiT在时间一致性上以98%的胜率领先于其他方法。
- 前缀潜在参考策略在SSIM (0.719 vs 0.702) 和FID-VID (33.5 vs 35.5) 上均优于潜在拼接参考方式。
---

# HumanDiT: Pose Guided Diffusion Transformer for Long-form Human Motion Video Generation

> [!tip] 核心洞察
> DiT的RoPE与3D全注意力可原生处理不同分辨率/序列长度；前缀潜在参考无需额外网络即保持身份一致性；补丁化姿态引导高效注入时空姿态信息；Keypoint-DiT生成连贯姿态序列，姿态适配器实现精准迁移。

| 字段 | 内容 |
|------|------|
| 中文题名 | HumanDiT：面向长序列人体运动视频生成的姿态引导扩散Transformer |
| 英文题名 | HumanDiT: Pose Guided Diffusion Transformer for Long-form Human Motion Video Generation |
| 会议/期刊 | arXiv 2025 |
| Links | [Project](https://agnjason.github.io/HumanDiT-page/) · [Code](https://github.com/blackforest-labs/flux) · [paper](https://arxiv.org/abs/2502.04847) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | HumanDiT |
| Dataset | Total |

> [!tip] 效果简介
> - Total (TikTok+Talking+Dancing) 上，FID-VID 25.5 vs 39.5 (MimicMotion) (-14.0)；SSIM 0.838 vs 0.776 (MimicMotion) (+0.062)；PSNR 22.8 vs 20.1 (MimicMotion) (+2.7)。

## 概要

**目标问题**：现有姿态引导的人体视频生成方法普遍基于 U‑Net 架构，受限于固定分辨率和短序列长度，且依赖复杂的双流参考网络，导致视觉一致性差，无法在统一框架下同时支持**视频延续**与**姿态迁移**。

**核心方法**：HumanDiT 以**扩散 Transformer (DiT)** 替代传统 3D U‑Net 作为去噪骨干，利用 RoPE 与 3D 全注意力原生支持可变分辨率与动态序列长度。同时提出**前缀潜在参考策略**——将首帧独立编码为无噪前缀潜在，无需额外参考网络即可保持身份一致性；并设计**补丁化姿态引导器**与**Keypoint‑DiT**，分别实现高效时空姿态注入与连贯姿态序列生成，再通过**姿态适配器**完成骨长对齐与运动迁移。

**主要结果**：
- 在 TikTok、Talking、Dancing 三个测试集的综合评估中，HumanDiT 取得最优 **FID‑VID 25.5**，显著优于 MimicMotion (39.5) 和 AnimateAnyone (68.8)（Table 1）。
- 将最大令牌数从 80K 提升至 480K 后，**SSIM 从 0.719 升至 0.838**，FID‑VID 从 33.5 降至 25.5，验证了大容量训练对长视频质量的必要性（Table 2）。
- 用户研究中，HumanDiT 在时间一致性维度上以 **98%** 的胜率领先于对比方法（Table 3）。

**方法定位**：HumanDiT 属于**姿态引导的扩散人体动画生成**范畴，与 DisCo、MagicDance、AnimateAnyone、MimicMotion 等基于 U‑Net 的方法形成对比。其关键差异在于以 DiT 为基础模型，并通过前缀潜在参考与补丁化姿态引导器实现统一的身份保持与姿态控制，同时引入 Keypoint‑DiT 与姿态适配器将能力边界从固定姿态序列生成扩展到视频延续与跨骨骼姿态迁移。



### 问题背景

从单张参考图像生成逼真且时间连贯的长序列人体运动视频，是计算机视觉与生成模型领域的前沿挑战。该任务要求模型同时解决三个核心难题：**身份保持**（生成人物与参考图像外观一致）、**姿态精度**（动作与目标姿态序列对齐）和**长时一致性**（跨帧无闪烁或伪影）。随着数字人、虚拟主播、影视制作等应用对高保真人体视频的需求激增，这一方向在近年受到广泛关注。

### 现有方法缺口

当前主流方法普遍采用基于U-Net的扩散模型作为去噪骨干，并依赖独立的参考网络（如双流结构）注入参考图像信息。这一范式存在三个结构性瓶颈：

1. **固定分辨率与短序列限制**：U-Net架构受限于固定的空间分辨率和时间长度，难以原生支持多分辨率、变长视频生成。模型通常只能处理预定义尺寸和帧数的输入，缺乏对长序列的扩展能力。

2. **参考网络带来的身份漂移**：独立的参考网络（如**AnimateAnyone**等采用的双流设计）在提取参考特征时与去噪过程解耦，导致生成视频中人物外观随时间逐渐偏离参考图像，尤其在长序列场景下身份一致性显著下降。

3. **缺乏统一的视频延续与姿态迁移框架**：现有方法（如**DisCo**、**MagicDance**、**MimicMotion**）通常将视频生成（给定完整姿态序列）和姿态迁移（将模板动作迁移到参考人物）视为独立任务，缺少统一架构来同时支持两种场景。视频延续需要从首帧自动生成连贯的后续姿态，而姿态迁移需要将外部动作序列适配到目标人物的骨骼结构，现有方法无法在一个框架内优雅地解决这两个需求。

### 本文动机

针对上述瓶颈，本文提出**HumanDiT**，核心动机在于用**扩散Transformer（DiT）**替代U-Net作为去噪骨干，从根本上突破固定分辨率和序列长度的限制。DiT原生的RoPE位置编码和3D全注意力机制使其能够灵活处理不同尺寸和长度的视频输入，无需架构修改即可扩展到长序列。

同时，HumanDiT引入**前缀潜在参考策略**，将首帧独立编码为无噪潜在向量并作为前缀拼接到去噪输入中，无需额外参考网络即可保持身份一致性。这一设计不仅简化了训练流程（单阶段端到端训练），还避免了参考网络引入的身份漂移问题。

在姿态处理上，HumanDiT通过**Keypoint-DiT**生成连贯的后续姿态序列以支持视频延续，并通过**姿态适配器**进行骨骼长度对齐和运动解耦以实现精准的姿态迁移，从而在一个统一框架内同时覆盖两类核心应用场景。



## 核心方法与创新机理

HumanDiT 的核心创新在于用**扩散Transformer (DiT)** 体系重构了人体运动视频生成范式，系统性突破了 U-Net 架构在分辨率、序列长度和身份一致性上的瓶颈。其关键改动体现在以下五个维度：

### 1. 去噪骨干网络：从 3D U-Net 到扩散 Transformer (DiT)

传统方法（如 **DisCo**、**MagicDance**、**AnimateAnyone**、**MimicMotion**）普遍采用 3D U-Net 作为去噪骨干，但 U-Net 的卷积结构天然受限于固定分辨率和固定帧数，难以处理可变长度视频。HumanDiT 替换为 DiT 架构（Section 3.3），利用**旋转位置编码 (RoPE)** 和 **3D 全注意力机制**，使模型能原生处理不同分辨率、不同序列长度的输入，无需重新训练或架构调整。这一替换是实现“统一框架支持视频延续与姿态迁移”的架构基础。

### 2. 参考图像条件注入：从双流参考网络到前缀潜在参考

现有方法（如 AnimateAnyone）依赖独立的双流参考网络提取参考图像特征，再注入去噪过程，这不仅增加模型复杂度，还容易引入视觉不一致。HumanDiT 提出**前缀潜在参考策略**（Section 3.3）：将首帧独立通过 3D VAE 编码为无噪潜在向量 $z^0 = \mathcal{E}(x^0)$，直接作为去噪序列的前缀参与 DiT 的 3D 全注意力计算，无需额外参考网络。消融实验证实（Table 2），前缀潜在参考在 SSIM（0.719 vs 0.702）和 FID-VID（33.5 vs 35.5）上均优于潜在拼接方式，证明该策略能以更简洁的机制实现更强的身份保持。

### 3. 姿态引导特征提取：从多层卷积块到补丁化线性姿态引导器

传统姿态注入方式使用多层卷积块处理姿态图，计算开销大且与潜在特征的对齐不够精确。HumanDiT 将姿态图**补丁化**（patch size=4），使其空间-时间维度与视频潜在特征严格对齐，形成姿态令牌 $\mathbf{P}' \in \mathbb{R}^{(f+1) \times h \times w \times 64d}$（Section 3.4）。其中姿态图维度 $d=8$，前 7 维编码人体关键点，最后一维编码最多 20 个背景关键点。这种轻量线性投影方式高效地将时空姿态信息注入 DiT，避免了复杂卷积带来的特征错位。

### 4. 姿态序列生成：从无显式生成到 Keypoint-DiT 自回归生成

此前方法只能使用给定的完整姿态序列，无法自主生成后续动作。HumanDiT 引入 **Keypoint-DiT** 模块（Section 3.4）：以初始帧关键点 $j_0$ 为条件，自回归生成后续关键点序列 $\{j_1, j_2, ..., j_m\} = K(j_0)$，使模型具备**视频延续**能力——从单张图像出发，自主生成连贯的人体运动序列。

### 5. 姿态迁移对齐：从直接使用给定姿态到姿态适配器解耦对齐

当目标姿态来自不同人体（骨骼比例不同）时，直接使用会导致渲染失真。HumanDiT 提出**姿态适配器**（Section 3.4）：利用参考骨骼长度 $l_0^i$ 和模板运动的最大长度 $l_i'$，对关节位置进行骨长归一化对齐 $\hat{j}_k^i = \hat{j}_0^{i-1} + l_0^i \cdot (j_k^i - j_k^{i-1}) / l_i'$，再通过 Keypoint-DiT 细化模块生成过渡帧 $\mathcal{T}_{\mathrm{fix}} = \mathcal{K}(j_0, \hat{\mathcal{I}}, \tau)$，实现精准的姿态迁移。消融可视化（Figure 6）表明，该模块有效解决了手部和面部的不一致问题。

这五个 changed slots 的协同作用，使 HumanDiT 在统一框架下同时支持**多分辨率生成**、**长视频延续**和**跨骨骼姿态迁移**，在 Total 测试集上取得 FID-VID 25.5，显著优于 MimicMotion 的 39.5 和 AnimateAnyone 的 68.8（Table 1）。



HumanDiT 的整体 pipeline 围绕“从单张参考图像生成高保真长序列人体运动视频”这一目标构建，其核心设计思路是用**扩散Transformer (DiT)** 替代传统 U-Net，并引入**前缀潜在参考策略**，从而在统一框架内支持可变分辨率、动态序列长度以及视频延续与姿态迁移两种推理模式。

### 输入输出流

系统的输入包括一张参考图像和一段目标姿态序列（可由外部给定，也可由内置的 Keypoint-DiT 自动生成）。输出为与姿态序列对齐的人体运动视频，视频的分辨率和帧数可在推理时灵活指定，无需重新训练。

### 模块组成与数据流

Figure 2 给出了完整架构。Pipeline 由以下核心模块串联而成：

![[assets/figures/papers/paper_list_l1833_HumanDiT_Pose_Guided_Diffusion_Transformer_for_Long_form_Human_Motion_Vi/figures/002_Figure_2.jpg]]
*Figure 2: The overview of HumanDiT. HumanDiT focuses on generate videos from a single image using a pose-guided DiT model. A 3D VAE is employed to encode video segments into latent space. With 3D full attention, the initial frame (green border) serves as a noise-free prefix latent (green cube) for reference. The pose guider extracts body and background pose features, while the DiT-based denoising model renders the final pixel results. During inference, the keypoint-DiT model produces subsequent motions based on the pose of the first frame. With a guided pose sequence, the pose adapter transfers and refines poses via keypoint-DiT to animate the reference image*

1. **3D VAE 编码器/解码器**  
   视频片段首先通过 3D VAE 编码器压缩到潜在空间，得到潜在向量 $\mathbf{z}_0 = \mathcal{E}(\mathbf{x})$。解码器则负责将去噪后的潜在向量重建为像素级视频帧。这一压缩步骤大幅降低了后续 DiT 去噪的计算开销。

2. **前缀潜在参考**  
   参考图像的首帧被独立送入 3D VAE 编码器，生成无噪的前缀潜在 $z^0 = \mathcal{E}(x^0)$。该前缀潜在在 DiT 的 3D 全注意力机制中作为身份锚点，使模型无需额外的参考网络即可捕获输入人物的外观特征。这是 HumanDiT 区别于 AnimateAnyone 等双流参考网络方案的关键设计。

3. **姿态引导器**  
   姿态图像（包含人体关键点和背景关键点）经过补丁化处理（patch size=4），与潜在特征在时空维度上对齐，生成条件令牌 $\mathbf{P}' \in \mathbb{R}^{(f+1) \times h \times w \times 64d}$（其中 $d=8$，前 7 维编码人体关键点，最后 1 维编码最多 20 个背景关键点）。这些令牌以条件注入的方式送入 DiT 去噪模型，实现精准的时空姿态控制。

4. **DiT 去噪模型**  
   扩散 Transformer 是生成过程的核心引擎。它接收噪声潜在、前缀潜在参考和姿态条件令牌，通过 3D 全注意力与 RoPE 位置编码，在去噪过程中同时建模时空一致性。由于 DiT 原生支持可变序列长度和分辨率，模型可以在训练时使用不同尺寸的数据，推理时灵活适配。

5. **Keypoint-DiT（姿态生成）**  
   在视频延续模式下，Keypoint-DiT $K$ 从首帧人体关键点 $j_0$ 出发，自回归地生成后续姿态序列 $\{j_1, j_2, ..., j_m\} = K(j_0)$。这使 HumanDiT 能够自主驱动人物做出连贯动作，而不依赖外部姿态输入。

6. **姿态适配器与细化模块**  
   当使用模板姿态序列进行姿态迁移时，姿态适配器先将模板运动解耦，再根据参考人物的骨骼长度进行关节位置对齐：
   $$\hat{j}_k^i = \hat{j}_0^{i-1} + l_0^i \cdot (j_k^i - j_k^{i-1}) / l_i'$$
   其中 $l_0^i$ 为参考骨长，$l_i'$ 为模板最大运动长度。随后，Keypoint-DiT 对过渡帧进行细化，生成最终的运动序列 $\mathcal{T}_{\mathrm{fix}} = \mathcal{K}(j_0, \hat{\mathcal{I}}, \tau)$，以缓解手部和面部的不一致问题。

7. **文本掩码处理**  
   在数据预处理和生成过程中，对字幕区域施加掩码，避免文本伪影污染生成结果。

### 训练与推理的统一性

得益于 DiT 的架构特性，整个 Video DiT 仅需**单阶段端到端训练**，无需像 U-Net 方案那样受参考网络的约束。训练时使用不同分辨率和帧数的数据混合训练，推理时即可直接处理未见过的视频尺寸和长度组合，这是 HumanDiT 在灵活性上显著优于固定分辨率 U-Net 基线（如 MimicMotion、AnimateAnyone）的根本原因。

### 补充图表

![[assets/figures/papers/paper_list_l1833_HumanDiT_Pose_Guided_Diffusion_Transformer_for_Long_form_Human_Motion_Vi/figures/001_Figure_1.jpg]]
*Figure 1: HumanDiT is a framework designed to generate high-fidelity, long human motion videos in diverse scenes and flexible resolution*



HumanDiT 围绕扩散Transformer（DiT）构建，以3D全注意力、旋转位置编码（RoPE）和补丁化（patchify）为骨干，突破U-Net固定分辨率的限制，统一支持变长视频生成与姿态迁移。其核心模块如下。

---

### 3D VAE 潜空间压缩

视频首先通过3D VAE编码器压缩至低维潜空间，以降低扩散模型的计算负担：

$$
\mathbf{z}_0 = \mathcal{E}(\mathbf{x})
$$

其中 $\mathbf{x}$ 为输入视频帧序列，$\mathcal{E}$ 为3D VAE编码器，$\mathbf{z}_0$ 为压缩后的潜变量。解码阶段通过对应的3D VAE解码器将去噪后的潜变量重建为像素空间视频。

---

### 前缀潜在参考策略

传统方法（如AnimateAnyone）依赖独立的双流参考网络来保持身份一致性，增加了模型复杂度且难以泛化至变长序列。HumanDiT提出**前缀潜在参考**策略：在推理时，将首帧独立编码为无噪潜变量，作为序列前缀直接拼接到待去噪的潜变量前方：

$$
z^0 = \mathcal{E}(x^0)
$$

其中 $x^0$ 为参考图像（首帧），$z^0$ 为其潜变量表示。该前缀潜变量在扩散过程中保持无噪状态，通过DiT的3D全注意力机制，使模型在生成后续帧时始终可访问首帧的身份特征，无需额外参考网络。消融实验证实，前缀潜在参考在SSIM（0.719 vs 0.702）和FID-VID（33.5 vs 35.5）上均优于潜变量拼接参考方式（Table 2）。

---

### 姿态引导器：补丁化线性注入

姿态信息通过**补丁化姿态引导器**注入DiT。姿态图像维度 $d=8$，前7维编码人体关键点，最后一维绘制不超过20个背景关键点。姿态图像在时间、高度、宽度三个维度上以补丁大小4进行补丁化，与潜变量 $\mathbf{z}$ 的空间对齐：

$$
\mathbf{P}' \in \mathbb{R}^{(f+1) \times h \times w \times 64d}
$$

其中 $f+1$ 为时间维度（含3帧时间填充），$h \times w$ 为空间维度，$64d$ 为每个补丁的展平维度。补丁化后的姿态令牌通过线性投影与扩散时间步嵌入融合后，作为条件注入DiT的各注意力层。相较于U-Net中常用的多层卷积块，该方案更简洁且与Transformer骨干天然兼容。

---

### DiT去噪骨干与训练损失

去噪模型基于DiT架构，采用3D全注意力和RoPE，可原生处理不同分辨率与序列长度的输入。训练沿用潜空间扩散模型的标准均方误差损失：

$$
\mathcal{L} = \mathbb{E}_{z_t, c, t, \epsilon \sim \mathcal{N}(0, I)} \left[ \| \epsilon - \epsilon_\theta (z_t; c, t) \|_2^2 \right]
$$

其中 $z_t$ 为加噪后的潜变量，$c$ 为条件（前缀潜变量与姿态令牌），$t$ 为扩散时间步，$\epsilon$ 为高斯噪声，$\epsilon_\theta$ 为DiT预测的噪声。前向扩散过程遵循标准高斯转移核：

$$
q(z_t | z_{t-1}) = \mathcal{N}(z_t; \sqrt{1 - \beta_t} z_{t-1}, \beta_t I)
$$

---

### Keypoint-DiT：姿态序列生成

为实现视频延续，HumanDiT引入**Keypoint-DiT** $K$，从初始人体关键点 $j_0$ 生成后续 $m$ 个连贯的关键点序列：

$$
\{j_1, j_2, \dots, j_m\} = K(j_0)
$$

该模块使HumanDiT能够在无外部姿态输入的情况下，自回归地生成延续动作，驱动视频内容的自然延伸。

---

### 姿态适配器：运动解耦与骨长对齐

对于姿态迁移任务，**姿态适配器**将模板运动解耦为骨长无关的运动增量，并映射到参考骨骼上。对于第 $i$ 个骨骼，目标关节位置 $\hat{j}_k^i$ 由参考骨长 $l_0^i$ 和模板运动的最大长度 $l_i'$ 对齐计算：

$$
\hat{j}_k^i = \hat{j}_0^{i-1} + l_0^i \cdot (j_k^i - j_k^{i-1}) / l_i'
$$

该公式将模板运动的归一化方向向量缩放到参考骨骼的骨长，从而在保持运动语义的同时适应不同体型的角色。

---

### 姿态细化模块

迁移后的姿态序列通过基于Keypoint-DiT的细化模块进一步平滑过渡并修复手部/面部不一致。在初始帧 $j_0$ 与对齐后的首帧姿态 $\hat{\mathcal{I}}$ 之间填充 $\tau$ 帧过渡帧，形成最终运动序列：

$$
\mathcal{T}_{\mathrm{fix}} = \mathcal{K}(j_0, \hat{\mathcal{I}}, \tau)
$$

其中 $\mathcal{K}$ 为细化模块，输出包含初始帧、$\tau$ 帧过渡帧和对齐姿态序列的完整运动。

---

### 文本掩码处理

为抑制视频中字幕区域的伪影，HumanDiT对文本区域进行检测并掩码处理，在训练和推理中忽略这些区域，避免文本闪烁或扭曲对生成质量的影响。

---

> **注意**：上述公式均来自论文Section 3.1–3.4的明确推导，未进行任何外推或猜测。关于序列并行（sequence parallelism）沿时间维度的具体实现细节，论文未给出公式化描述，此处不予展开。



## 实验与关键发现

### 主要结果

HumanDiT 在 TikTok 及自收集的 Talking、Dancing 三个测试集上全面优于现有姿态引导人体动画方法。在 Total 全集上，HumanDiT 的 FID-VID 降至 **25.5**，相比最强基线 MimicMotion 的 39.5 降低了 14.0；SSIM 达到 **0.838**（+0.062），PSNR 达到 **22.8**（+2.7），FVD 降至 **320**（-138）。这些指标在 Table 1 中均有详细报告，置信度极高（0.99）。

![[assets/figures/papers/paper_list_l1833_HumanDiT_Pose_Guided_Diffusion_Transformer_for_Long_form_Human_Motion_Vi/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison on the TikTok dataset [19] and our self-collected talking and dancing test datasets with existing poseguided human body animation methods. Further details are provided in the supplemental material (Appendix.D.1)*

分数据集来看，HumanDiT 在 TikTok 上的 FID-VID 为 23.3，在 Talking 上为 28.1，在 Dancing 上为 26.0，均显著优于 AnimateAnyone（对应 68.8/72.1/65.3）和 DisCo（对应 49.5/57.2/52.8）。L1 损失同样最低，仅为 $1.73 \times 10^{-5}$，表明生成帧与真实帧在像素级保真度上也具有优势。

定性对比（Figure 3）进一步印证：HumanDiT 在渲染质量和姿态准确性上均明显优于基线方法，尤其在面部细节和手部姿态保持方面表现突出。

![[assets/figures/papers/paper_list_l1833_HumanDiT_Pose_Guided_Diffusion_Transformer_for_Long_form_Human_Motion_Vi/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison. Our approach outperforms others in rendering quality and pose accuracy*

### 消融实验

**最大令牌数（Max Token Size）**。Table 2 显示，将最大令牌数从 80K 提升至 480K 后，所有指标均大幅改善：SSIM 从 0.719 升至 0.838（+0.119），PSNR 从 19.50 升至 22.75（+3.25），FID-VID 从 33.5 降至 25.5（-8.0），FVD 从 382 降至 320（-62）。这直接证明大容量训练对长视频质量至关重要，也是 DiT 架构可扩展性优势的实证支撑。

**前缀潜在参考策略（Prefix-Latent Reference）**。在相同 80K 令牌设置下，前缀潜在参考的 SSIM 为 0.719，FID-VID 为 33.5，均优于潜在拼接参考方式（SSIM 0.702，FID-VID 35.5）。这一策略无需额外参考网络，仅通过将首帧潜在作为无噪前缀注入去噪过程，即可更有效地保持身份一致性。

**姿态适配器与 Keypoint-DiT 细化**。Figure 6 的消融可视化表明，未使用姿态适配器时，生成结果在手部和面部区域存在明显的不一致和伪影；引入姿态适配器并配合 Keypoint-DiT 进行姿态细化后，这些问题得到有效解决。该结论置信度为 0.95，但需注意原文未提供该模块的独立定量指标，建议查阅附录确认完整消融数据。

### 用户研究

Table 3 报告了用户研究结果。在测试集生成视频的对比中，HumanDiT 在时间一致性上以 **98%** 的胜率领先于其他方法，在身份保持和视觉质量上也分别取得 95% 和 92% 的胜率。在野生姿态序列的姿态迁移任务中，HumanDiT 同样在三个维度上全面领先 AnimateAnyone 和 MimicMotion。这从主观评价角度验证了前缀潜在参考和姿态细化模块对视觉一致性的关键贡献。

![[assets/figures/papers/paper_list_l1833_HumanDiT_Pose_Guided_Diffusion_Transformer_for_Long_form_Human_Motion_Vi/figures/008_Table_3.jpg]]
*Table 3: User study. The values represent the win rates of the current method compared to other methods. We ask users to rate the generated videos on our test set (left) and wild pose sequences with pose transfer (right), comparing with Animate Anyone (A.A.) [18] and MimicMotion (M.M.) [69] in terms of temporal consistency, identify preservation, and visual quality*

### 失败模式与局限性

尽管整体性能优异，HumanDiT 仍存在以下已知局限：

1. **极端姿态不匹配**：当参考图像与目标姿态之间存在极端身体比例变化或复杂手部/面部运动时，生成质量可能下降，视觉一致性受损。
2. **多批次误差传播**：长视频生成需分批次推理，后续批次难以完全保留第一帧的身份特征，导致身份漂移。
3. **计算成本**：生成更高分辨率或更长视频仍需高昂的计算开销，480K 令牌训练设置本身即反映了对算力的高需求。
4. **姿态生成模态单一**：当前 Keypoint-DiT 仅支持关键点输入，无法从图像、语音或文本描述生成姿态序列，限制了视频延续的自然性和多模态扩展能力。

这些局限在原文中被明确列出，置信度高，但部分问题（如误差传播的定量分析）尚未提供实验数据，需后续工作验证。

### 补充图表

![[assets/figures/papers/paper_list_l1833_HumanDiT_Pose_Guided_Diffusion_Transformer_for_Long_form_Human_Motion_Vi/figures/005_Table_2.jpg]]
*Table 2: Quantitative results of ablation study on maximin token size and prefix-latent reference strategy for reference image (Ref.). The first two rows are conducted without using sequence parallel*

![[assets/figures/papers/paper_list_l1833_HumanDiT_Pose_Guided_Diffusion_Transformer_for_Long_form_Human_Motion_Vi/figures/009_Figure_6.jpg]]
*Figure 6: Ablation study of pose adapter and pose refinement*

![[assets/figures/papers/paper_list_l1833_HumanDiT_Pose_Guided_Diffusion_Transformer_for_Long_form_Human_Motion_Vi/figures/006_Figure_4.jpg]]
*Figure 4: The template pose-driven human rendering results of HumanDiT on the Flux [4] generated images*

![[assets/figures/papers/paper_list_l1833_HumanDiT_Pose_Guided_Diffusion_Transformer_for_Long_form_Human_Motion_Vi/figures/007_Figure_5.jpg]]
*Figure 5: The video continuation with generated motions*



## 定位与知识库关联

### 1. 技术脉络与基线关系

HumanDiT 的核心定位是**面向长序列人体运动视频生成的统一框架**，其技术路径是对现有姿态引导人体动画方法的系统性重构。在 HumanDiT 之前，该领域的主流方法（如 **DisCo**、**MagicDance**、**AnimateAnyone**、**MimicMotion**）普遍采用以下技术组合：

- **去噪骨干**：基于 3D U-Net 架构，受限于固定分辨率和短序列处理能力。
- **参考图像注入**：依赖双流参考网络（如 AnimateAnyone 的 ReferenceNet）提取身份特征，再与去噪网络进行特征融合。这类设计引入了额外的网络分支，增加了训练复杂度，且在长序列生成中容易出现身份漂移。
- **姿态引导**：通过多层卷积块提取姿态特征，信息压缩路径单一，难以高效注入时空姿态信息。
- **姿态序列获取**：无显式的姿态生成模块，直接使用给定的完整姿态序列驱动生成，缺乏对运动连贯性的建模。

HumanDiT 对上述四个关键槽位进行了**根本性替换**：

| 技术槽位 | 基线方案 | HumanDiT 方案 | 核心优势 |
|---------|---------|--------------|---------|
| 去噪骨干网络 | 3D U-Net | 扩散 Transformer (DiT) | RoPE + 3D 全注意力原生支持可变分辨率/序列长度 |
| 参考图像注入 | 双流参考网络 | 前缀潜在参考 | 无需额外网络，首帧潜在作为无噪前缀保持身份一致性 |
| 姿态引导 | 多层卷积块 | 补丁化线性姿态引导器 (patch=4) | 与潜在特征对齐，高效注入时空姿态信息 |
| 姿态序列生成 | 无显式模块 | Keypoint-DiT + 姿态适配器 | 从单帧姿态生成连贯序列，解耦运动并做骨长对齐 |

这种替换带来了**方法论的统一性**：HumanDiT 无需针对视频延续和姿态迁移分别设计不同的网络结构，同一 DiT 骨干配合前缀潜在参考即可同时支持两种任务。相比之下，AnimateAnyone 等基线方法需要独立的参考网络和复杂的特征融合机制，限制了其在不同场景下的泛化能力。

### 2. 适用边界与能力定位

HumanDiT 的能力边界由其架构设计决定，可以从输入灵活性、生成能力和质量边界三个维度进行定位：

**输入灵活性**：
- 支持任意分辨率的参考图像和视频生成，得益于 DiT 的 RoPE 位置编码和补丁化处理。
- 支持动态序列长度，最大令牌数可扩展至 480K（消融实验中验证）。
- 姿态输入兼容给定姿态序列、Keypoint-DiT 生成序列、以及经姿态适配器迁移的模板运动。

**生成能力**：
- **视频延续**：从单张参考图像出发，Keypoint-DiT 基于首帧姿态生成后续连贯动作序列，实现长视频生成。
- **姿态迁移**：姿态适配器将模板运动的骨骼结构对齐到参考人物的骨骼比例，再通过 Keypoint-DiT 细化过渡帧，实现精准的姿态迁移。
- **多分辨率输出**：同一模型可生成不同分辨率的视频，无需重新训练。

**质量边界**：
- 在标准测试集（TikTok + 自收集的 Talking + Dancing）上，HumanDiT 取得 FID-VID 25.5，显著优于 MimicMotion（39.5）和 AnimateAnyone（68.8）。
- 用户研究中，时间一致性胜率达 98%。
- 但当参考图像与目标姿态存在**极端不匹配**（如身体比例剧烈变化、复杂手部/面部运动）时，视觉一致性仍会下降。
- 长视频的多批次推理存在**误差传播**问题，后续批次难以完全保留第一帧的身份特征。

### 3. 局限性与开放问题

**已验证的局限性**：

1. **极端姿态不匹配**：当参考人物的身体比例与目标姿态差异过大时，姿态适配器的骨长对齐机制可能无法完全补偿，导致生成结果出现形变或伪影。这一问题在手部和面部细节上尤为突出。

2. **多批次推理的身份漂移**：长视频生成采用分段推理策略，每批次以首帧潜在作为前缀参考。但随着批次推进，累积的去噪误差可能导致后续帧的身份特征逐渐偏离参考图像。

3. **计算成本**：生成更高分辨率或更长视频时，DiT 的 3D 全注意力计算开销显著增加。480K 令牌的训练需要序列并行支持，推理阶段的计算资源需求仍然较高。

4. **姿态生成模态受限**：Keypoint-DiT 仅支持从关键点序列生成后续姿态，无法从图像、语音或文本描述等多模态输入生成姿态序列，限制了视频延续的自然交互性。

**开放问题与研究方向**：

1. **鲁棒性提升**：如何设计更鲁棒的身份保持机制，使模型在参考图像与目标姿态极端不匹配时仍能保持视觉一致性？可能的路径包括引入更强的空间变换模块或自适应骨长调整策略。

2. **身份漂移抑制**：能否通过改进前缀潜在参考策略（如多帧参考、滑动窗口更新）或引入显式的身份约束损失来减少多批次推理中的误差累积？

3. **推理效率优化**：如何降低长视频生成的注意力计算开销？可能的方案包括稀疏注意力、时序压缩、或蒸馏出轻量级推理模型。

4. **多模态姿态生成**：如何扩展 Keypoint-DiT 以支持从语音、文本或音乐节奏生成姿态序列？这将使视频延续更加自然，例如根据语音内容生成对应的手势动作。

5. **数据规模与质量**：HumanDiT 使用了 14,000 小时的自收集野外视频数据集，但数据质量对手部和牙齿等细节的影响尚需进一步量化分析。清晰度评分模型的过滤标准与最终生成质量之间的因果关系值得深入研究。



## 原文 PDF

![[paperPDFs/arxiv_2025/HumanDiT_Pose_Guided_Diffusion_Transformer_for_Long_form_Human_Motion_Video_Generation.pdf]]
