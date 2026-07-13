---
title: "EgoX: Egocentric Video Generation from a Single Exocentric Video"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EgoX_Egocentric_Video_Generation_from_a_Single_Exocentric_Video.pdf
project_link: null
code_link: null
aliases:
- EgoX
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 几何引导自注意力（GGA）通过3D方向相似性偏置引导模型关注空间对应区域；统一的条件注入策略（宽度级联清洁外中心潜变量、通道级联自我中心先验）决定了细节保持与几何一致性。
primary_logic: 利用大规模预训练视频扩散模型的时空先验，结合轻量级LoRA适配、统一条件注入（宽度/通道级联）和几何引导自注意力，可以在仅有一段外中心视频的条件下生成高质量、几何一致的自我中心视频。
claims:
- EgoX利用预训练视频扩散模型的时空知识，通过轻量级LoRA适配进行微调。
- 几何引导的自注意力机制通过3D方向相似度偏置增强空间对齐，抑制不相关区域。
- 清洁潜变量级联策略使模型在整个去噪过程中始终保留外中心的细粒度细节，避免信息丢失。
- EgoX在Seen/Unseen场景的PSNR和FVD等指标上显著超越Exo2Ego-V等基线，尤其在对象级一致性上优势明显。
---

# EgoX: Egocentric Video Generation from a Single Exocentric Video

> [!tip] 核心洞察
> 利用大规模预训练视频扩散模型的时空先验，结合轻量级LoRA适配、统一条件注入（宽度/通道级联）和几何引导自注意力，可以在仅有一段外中心视频的条件下生成高质量、几何一致的自我中心视频。

| 字段 | 内容 |
|------|------|
| 中文题名 | EgoX：基于单段外中心视频的自我中心视频生成 |
| 英文题名 | EgoX: Egocentric Video Generation from a Single Exocentric Video |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.08269) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | EgoX |
| Dataset | Seen Scenes, Unseen Scenes |

> [!tip] 效果简介
> - Seen Scenes 上，PSNR 16.05 vs 14.53 (Exo2Ego-V) (+1.52)；FVD 184.47 vs 622.47 (Exo2Ego-V) (-437.99)。
> - Unseen Scenes 上，PSNR 14.38 vs 12.70 (Exo2Ego-V) (+1.68)；FVD 440.64 vs 1283.50 (Exo2Ego-V) (-842.86)。

## 概要

**核心问题**：从单段外中心（第三人称）视频生成对应的自我中心（第一人称）视频，面临极端相机姿态变化带来的根本性挑战——大量区域在外中心视角中不可见，模型必须合理合成这些区域，同时精确抑制外中心视频中与自我视角无关的背景内容。现有相机可控视频生成方法难以处理如此剧烈的视角变换。

**核心洞察**：EgoX 利用大规模预训练视频扩散模型（Wan 2.1 Inpainting, 14B）的时空先验知识，通过轻量级 LoRA 适配（rank=256）进行微调，避免了从零训练的巨大开销。在此基座上，三个关键设计协同解决了外中心到自我中心转换的核心瓶颈：

1. **统一条件注入策略**：对外中心视频潜变量采用宽度级联（width-wise concatenation），对自我中心先验潜变量采用通道级联（channel-wise concatenation），且外中心潜变量在整个去噪过程中保持清洁（clean latent $x_0$）并固定不变，仅更新噪声潜变量 $z_t$。这确保模型始终保留外中心的细粒度细节，避免信息在去噪过程中丢失。

2. **几何引导自注意力（GGA）**：在自注意力层的 logits 中引入基于 3D 方向余弦相似度的加性偏置 $s_{m,n}^{\prime} = s_{m,n} + \log( g( \hat{q}_m, \hat{k}_n ) \cdot \lambda_g )$，使自我中心查询（query）自适应地聚焦于外中心键（key）中几何对齐的空间区域，从而抑制不相关内容的干扰。

3. **自我中心先验渲染**：通过单目/视频深度估计与对齐，将外中心视频提升为 3D 点云，再以目标自我中心相机姿态渲染出粗略的自我中心先验视频，为扩散模型提供视角引导。

**方法定位**：EgoX 属于基于预训练视频扩散模型的视角转换方法，与 **Exo2Ego-V**（外中心到自我中心视频生成基线）、**TrajectoryCrafter**（相机控制基线）等方法相比，其核心区别在于利用几何先验显式引导注意力机制，而非仅依赖隐式学习或简单的条件注入。

**主要结果**：在 Ego-Exo4D 数据集的 Seen Scenes 上，EgoX 的 PSNR 达到 16.05（对比 Exo2Ego-V 的 14.53），FVD 降至 184.47（对比 622.47）；在 Unseen Scenes 上，PSNR 为 14.38（对比 12.70），FVD 为 440.64（对比 1283.50），在所有图像级、对象级和视频级指标上均取得最优综合性能。消融实验证实，移除 GGA、自我中心先验或清洁潜变量条件均导致性能显著下降，验证了各组件的必要性。用户研究进一步表明，EgoX 在所有评估问题上获得最高选择数，显著优于所有基线方法。



**任务定义与核心挑战。** 从外中心（第三人称）视频生成自我中心（第一人称）视频，要求模型根据一段观察者视角的输入，合成出“演员眼中所见”的连续画面。这一任务面临的核心瓶颈在于**极端相机姿态变化**：当视角从外中心切换到自我中心时，场景中的大面积区域在输入中完全不可见，模型必须合理合成这些未知区域，同时**抑制外中心画面中与自我中心视角无关的内容**（如远处的背景或旁观者）。Figure 2 直观展示了这一挑战——模型需要保留与视角相关的区域、逼真地补全不可见部分，并忽略无关区域。

**现有方法的缺口。** 已有的外中心到自我中心生成方法（如 **Exo2Ego-V**）通常依赖多视角输入或复杂的3D重建管线，难以在仅有一段外中心视频的条件下工作。另一方面，通用相机控制模型（如 **TrajectoryCrafter**）虽然能够对预训练视频生成模型施加相机运动约束，但其设计面向中等幅度的视角变化，**无法处理外中心到自我中心这种剧烈的视角跳跃**。条件注入策略方面，现有方法多采用通道级联或基于交叉注意力的条件注入（如 **Wan Fun Control**、**Wan VACE**），但这些策略在保留细粒度外中心细节和引导几何一致性方面存在不足——通道级联容易丢失空间信息，而SDEdit式的噪声潜变量级联则会在去噪过程中逐渐模糊输入细节。

**本文动机与核心洞察。** 大规模预训练视频扩散模型（如 Wan 2.1）已经内化了丰富的时空先验，能够生成连贯的视频内容。EgoX 的核心洞察在于：**利用这些预训练时空知识，配合轻量级LoRA适配、统一条件注入策略和几何引导自注意力，可以在仅有一段外中心视频的条件下生成高质量、几何一致的自我中心视频**。具体而言，EgoX 通过三个关键设计突破上述瓶颈：（1）将外中心视频提升为3D点云并渲染粗略的自我中心先验视频，为模型提供显式的视角引导；（2）设计统一的清洁潜变量条件注入策略（宽度级联外中心潜变量、通道级联自我中心先验），确保细节在整个去噪过程中得以保留；（3）在自注意力层引入基于3D方向相似度的几何偏置，使模型自适应地聚焦于空间对应区域。整体流程如 Figure 3 所示，从单段外中心输入到最终自我中心输出，EgoX 实现了端到端的视角变换生成。



## 核心方法与创新机理

EgoX 的核心创新在于将“外中心到自我中心”这一极端视角变换任务，系统性地分解为三个相互协同的技术槽位：**统一条件注入策略**、**几何引导自注意力**和**清洁潜变量表示**。这三个槽位共同解决了现有相机控制模型在剧烈视角变化下大面积不可见区域合成与不相关内容抑制的根本困难。

### 统一条件注入：宽度级联与通道级联的协同

现有方法通常采用单一的通道级联或交叉注意力进行条件注入，或使用 SDEdit 式的噪声潜变量级联。EgoX 提出了一种**双重条件注入策略**：

- **外中心潜变量**：采用**宽度级联**（width-wise concatenation），将清洁的外中心视频潜变量 $x_0$ 与噪声潜变量 $z_t$ 在空间维度上拼接，使模型在整个去噪过程中始终可直接访问外中心的细粒度视觉细节。
- **自我中心先验潜变量**：采用**通道级联**（channel-wise concatenation），将渲染得到的自我中心先验 $p_0$ 作为几何引导信号注入模型。

这一设计的因果机制在于：宽度级联保证了外中心可见区域的细节保真度，而通道级联则提供了目标视角的几何结构先验。消融实验证实，移除清洁潜变量条件导致 PSNR 下降 0.98、FVD 升至 343.33（Table 2），验证了该策略对细节保留的关键作用。

### 几何引导自注意力：从语义对齐到几何对齐

标准自注意力仅依赖语义相似度建立 token 间的关联，在极端视角变换下容易关注到外观相似但空间无关的区域（如背景中的相似纹理）。EgoX 的**几何引导自注意力**在注意力 logits 中引入了基于 3D 方向余弦相似度的加性偏置：

$$s_{m,n}^{\prime} = s_{m,n} + \log( g( \hat{q}_m, \hat{k}_n ) \cdot \lambda_g )$$

其中几何先验项定义为 $g( \hat{a}, \hat{b} ) = \cos \angle \mathrm{sim}( \hat{a}, \hat{b} ) + 1$，保证非负值。该偏置使自我中心查询 token 优先关注外中心中具有相似 3D 方向的关键 token，从而在几何层面实现空间对齐。

注意力图可视化（Figure 7）直接证实了这一机制的效果：无 GGA 时，模型注意力分散到无关区域；加入 GGA 后，注意力高度集中于几何对应的相关区域。消融实验中移除 GGA 导致 PSNR 下降 1.28、FVD 上升约 70（Table 2），且模型会关注可见区域外的事件并生成不期望的内容（Figure 10），充分证明了几何偏置对空间对齐的不可替代性。

### 清洁潜变量：贯穿全过程的细节锚定

与 SDEdit 等使用噪声潜变量级联的方法不同，EgoX 在整个去噪时间步中始终保持外中心潜变量 $x_0$ 为**清洁且固定**的状态，仅更新噪声潜变量 $z_t$。这一设计的核心洞察在于：去噪过程中的信息损失是渐进且不可逆的，若外中心潜变量也参与加噪-去噪循环，其携带的细粒度细节将逐步退化。通过将 $x_0$ 作为固定锚点，模型在任意去噪步都能回溯到原始外中心的完整视觉信息，从而在合成大面积不可见区域时仍能保持与可见区域的一致性。

### 方法谱系与知识库定位

EgoX 立足于预训练视频扩散模型的时空先验（基于 Wan 2.1 Inpainting 14B 模型），通过轻量级 LoRA 适配（rank=256）进行微调，避免了从零训练的巨大开销。相较于：

- **Exo2Ego-V**：作为外中心到自我中心视频生成的直接基线，缺乏几何引导机制和清洁潜变量策略，在 PSNR 和 FVD 上均显著落后（Seen PSNR: 16.05 vs 14.53, FVD: 184.47 vs 622.47）。
- **TrajectoryCrafter** 等相机控制基线：设计用于温和的相机运动，难以处理外中心到自我中心这种涉及近 180° 视角旋转的极端变换。
- **Wan Fun Control / Wan VACE** 等条件注入基线：分别采用通道级联和辅助编码网络，但缺乏几何偏置和宽度级联的细节保留能力（Wan VACE 虽在视频级指标上得分较高，但主要因其生成静态输出所致）。

EgoX 的贡献不在于提出全新的生成范式，而在于识别了外中心到自我中心生成中“细节保留-几何对齐-内容抑制”的三元张力，并通过统一条件注入、几何引导注意力和清洁潜变量这三个 changed slots 实现了系统性的突破。



EgoX 的整体 pipeline 围绕一个核心思路构建：利用大规模预训练视频扩散模型的时空先验，通过轻量级适配和几何引导，将单段外中心视频转化为高质量、几何一致的自我中心视频。整个框架由四个关键模块串联而成，形成从 3D 重建到条件视频生成的端到端流程。

### 输入与输出

- **输入**：单段外中心视频 $X$（RGB 帧序列）及对应的自我中心相机姿态 $\phi$（对于野生场景，可通过 Viser 交互式设定，见 Figure 8）。
- **输出**：一段从演员第一人称视角观察的自我中心视频，要求保留外中心可见区域的内容、合理合成不可见区域，并抑制不相关的外中心背景（Figure 2 示意了这一核心挑战）。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_08269/figures/010_Figure_8.jpg]]
*Figure 8: In-the-wild Ego camera. The ego camera for the in-thewild example was obtained by interactively determining its extrinsic parameters using Viser [48]*

### Pipeline 模块

**1. 自我中心先验渲染（Egocentric Prior Rendering）**

首先将外中心视频 $X$ 提升为 3D 点云，再从自我中心视角渲染出粗略的先验视频 $P$。具体步骤包括：
- 使用单目深度估计和视频深度估计分别获取深度图，通过逐帧仿射变换对齐得到最终深度 $D^f$（见公式 $D^{f} = \frac{1}{\hat{\alpha} / D^{v} + \hat{\beta}}$）。
- 结合对齐深度 $D^f$ 与自我中心相机姿态 $\phi$，从 3D 点云渲染自我中心先验帧 $P = \mathrm{render}(X, D^{f}, \phi)$。

这一步为后续视频扩散模型提供了粗略的视角引导，但其本身质量有限，需要生成模型进一步精炼。

**2. 视频扩散模型基座（Video Diffusion Model）**

EgoX 采用 **Wan 2.1 (14B) Image-to-Video 模型的 Inpainting 变体** 作为基座模型，通过 **LoRA（rank=256）** 进行轻量级微调，以适配外中心到自我中心的视角转换任务。去噪过程的单步更新公式为：

$$z_{t-1} = f_{\theta}(x_0, z_t \vert x_0, p_0 \vert m^1, m^0)$$

其中 $x_0$ 为清洁外中心视频潜变量，$p_0$ 为自我中心先验潜变量，$m$ 为二元掩码用于区分条件区域与合成区域。

**3. 统一条件注入策略（Unified Conditioning）**

这是 EgoX 区别于现有方法的关键设计之一。模型在潜空间中对两类条件采用不同的注入方式：
- **宽度级联（width-wise concatenation）**：将清洁的外中心潜变量 $x_0$ 与噪声潜变量 $z_t$ 在宽度维度上级联，且 $x_0$ 在整个去噪过程中**保持固定不变**，仅更新 $z_t$。这确保模型在所有时间步都能访问外中心的细粒度细节，避免信息因噪声扰动而丢失。
- **通道级联（channel-wise concatenation）**：将自我中心先验潜变量 $p_0$ 以通道级联方式注入，提供视角引导。

这一策略与 SDEdit 式噪声潜变量级联形成对比：后者在去噪过程中逐渐丢失外中心信息，而 EgoX 的清洁潜变量设计从根本上解决了这一问题。

**4. 几何引导自注意力（Geometry-Guided Self-Attention, GGA）**

在自注意力层中引入基于 3D 方向相似度的几何偏置，使自我中心查询（query）能够聚焦于外中心键（key）中几何对齐的区域。具体地，修改后的注意力 logits 为：

$$s_{m,n}^{\prime} = s_{m,n} + \log( g( \hat{q}_m, \hat{k}_n ) \cdot \lambda_g )$$

其中几何先验项 $g( \hat{a}, \hat{b} ) = \cos \angle \mathrm{sim}( \hat{a}, \hat{b} ) + 1$ 基于 3D 方向向量的余弦相似度计算，保证正值。最终注意力权重为：

$$a_{m,n} = \frac{ \exp( s_{m,n} ) \, g( \hat{q}_m, \hat{k}_n ) \, \lambda_g }{ \sum_{j=1}^{l} \exp( s_{m,j} ) \, g( \hat{q}_m, \hat{k}_j ) \, \lambda_g }$$

Figure 4 直观展示了这一机制：即使橙色和红色 token 来自同一键，由于相机中心不同导致方向向量差异，它们获得不同的注意力分数；而蓝色-红色对因方向相似获得更高分数，绿色-橙色对因方向相反获得更低分数。

### 模块间关系

四个模块形成清晰的因果链：**自我中心先验渲染** 提供粗糙的视角引导 → **统一条件注入** 将外中心细节和先验引导同时送入扩散模型 → **GGA** 在注意力层强制空间对齐 → **LoRA 微调** 使预训练模型适配新任务。消融实验（Table 2）证实，移除任一模块均导致显著性能下降：移除 GGA 使 PSNR 下降 1.28，移除自我中心先验使 PSNR 下降 2.38，移除清洁潜变量使 PSNR 下降 0.98 且 FVD 升至 343.33，验证了各组件的必要性和互补性。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_08269/figures/003_Figure_3.jpg]]
*Figure 3: Overall pipeline. Given an exocentric video input, we first lift it into a 3D point cloud and render the scene from the egocentric viewpoint to obtain the egocentric prior video. The clean exocentric video latent and the egocentric prior latent are combined via widthwise and channel-wise concatenation in the latent space, and then fed into a pretrained video diffusion model equipped with the proposed geometry-guided self-attention*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_08269/figures/023_Table_6.jpg]]
*Table 6: System Prompt for VLM. This is the system prompt used to generate the input text prompt for our model. Since the exocentric views were width-wise concatenated, the prompt describes both the exocentric and egocentric views*



EgoX 的核心架构由三个紧密协作的模块构成：自我中心先验生成、统一条件注入策略，以及几何引导自注意力（GGA）。以下逐一剖析其设计逻辑与关键公式。

### 自我中心先验生成

该模块解决从外中心视频到自我中心视角的3D几何映射问题。流程分为两步：

1. **深度对齐**：对外中心视频的每一帧，分别通过单目深度估计和视频深度估计获得两张深度图。由于二者尺度不一致，需通过逐帧仿射变换进行对齐，得到最终深度图 $D^{f}$：

   $$D^{f} = \frac{1}{\hat{\alpha} / D^{v} + \hat{\beta}}$$

   其中 $D^{v}$ 为视频深度估计结果，$\hat{\alpha}$ 和 $\hat{\beta}$ 为通过最小化与单目深度差异求得的尺度与偏移参数。这一对齐步骤对时域稳定性至关重要——消融实验表明，未对齐的深度会导致点云渲染中出现虚假相机运动，破坏帧间一致性（Figure 9）。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_08269/figures/011_Figure_9.jpg]]
*Figure 9: Depth align comparison. The above egocentric view is rendered from 3D point clouds across all frames. Without depth alignment, the inconsistent depth values between frames lead to unstable and unexpected camera movements*

2. **点云渲染**：将外中心RGB视频 $X$、对齐深度 $D^{f}$ 以及给定的自我中心相机姿态 $\phi$ 输入渲染函数，生成粗略的自我中心先验视频 $P$：

   $$P = \mathrm{render}(X, D^{f}, \phi)$$

   该先验视频为后续扩散模型提供了关键的几何引导，消融实验证实移除它会导致PSNR下降2.38，模型失去视角参照。

### 统一条件注入策略

EgoX 采用了一种双通道条件注入方式，将外中心信息与自我中心先验同时馈入预训练视频扩散模型。单步去噪过程可表示为：

$$z_{t-1} = f_{\theta}(x_0, z_t \mid x_0, p_0 \mid m^1, m^0)$$

其中 $x_0$ 为外中心视频的**清洁潜变量**（在整个去噪过程中保持固定，不参与更新），$p_0$ 为自我中心先验潜变量，$z_t$ 为当前噪声潜变量，$m^1$ 和 $m^0$ 为二值掩码（分别标记需保留和需生成的区域）。

该策略的核心创新在于：
- **宽度级联**：将清洁外中心潜变量 $x_0$ 与噪声潜变量 $z_t$ 在宽度维度拼接，使模型在所有去噪时间步上始终能访问外中心的细粒度细节，避免信息丢失。
- **通道级联**：将自我中心先验潜变量 $p_0$ 通过通道维度注入，提供视角变换的几何引导。

消融实验验证了这一设计的必要性：移除清洁潜变量条件导致PSNR下降0.98，FVD升至343.33，细节保留明显受损。

### 几何引导自注意力（GGA）

GGA 是 EgoX 实现空间对齐的关键机制。其核心思想是：在标准自注意力的logits中引入基于3D方向相似度的几何偏置项，使自我中心查询（query）能够自适应地关注外中心键（key）中几何对应的区域。

对于自我中心查询 $\hat{q}_m$ 和外中心键 $\hat{k}_n$，修正后的注意力logits为：

$$s_{m,n}^{\prime} = s_{m,n} + \log(g(\hat{q}_m, \hat{k}_n) \cdot \lambda_g)$$

其中 $s_{m,n}$ 为原始语义相似度logits，$\lambda_g$ 为可学习的缩放因子。几何先验项 $g(\cdot)$ 定义为3D方向向量的余弦相似度加1，保证正值：

$$g(\hat{a}, \hat{b}) = \cos\_\mathrm{sim}(\hat{a}, \hat{b}) + 1$$

最终的注意力权重通过将几何项以乘法形式融入softmax计算得到：

$$a_{m,n} = \frac{\exp(s_{m,n}) \cdot g(\hat{q}_m, \hat{k}_n) \lambda_g}{\sum_{j=1}^{l} \exp(s_{m,j}) \cdot g(\hat{q}_m, \hat{k}_j) \lambda_g}$$

这一设计的直观解释如 Figure 4 所示：尽管橙色和红色token在语义上可能相似，但由于它们源自不同的相机中心，3D方向向量可能截然相反，因此几何偏置会抑制它们之间的注意力权重；而蓝色和红色token具有相似的3D方向，会获得更高的注意力分数。消融实验证实，移除GGA导致PSNR下降1.28、FVD上升约70，注意力图可视化（Figure 7）也直观展示了GGA使模型注意力从无关区域收缩到几何对齐区域的效果。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_08269/figures/004_Figure_4.jpg]]
*Figure 4: Geometry-Guided Self-Attention Overview. 3D direction similarities between egocentric queries and exocentric keys are used as an additive bias in the attention map, guiding the model to focus on geometrically aligned regions. Although the orange and red directions are the same key tokens, their directions differ due to different camera centers. The blue–red pairs have similar directions and thus receive higher scores, whereas the green–orange pairs have opposite directions and obtain lower scores*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_08269/figures/009_Figure_7.jpg]]
*Figure 7: Attention map visualization. Visualization of the attention weights when querying the center token of the egocentric view. Without GGA, the model attends to unrelated regions, whereas with GGA, attention is concentrated on related regions, highlighting improved spatial alignment*

### LoRA微调

EgoX 采用 Wan 2.1（14B）的Inpainting变体作为基础视频扩散模型，通过LoRA（rank=256，batch size=1）进行轻量级适配。这一策略充分利用了大规模预训练模型的时空先验，同时避免了全参数微调的高昂成本。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_08269/figures/007_Table_2.jpg]]
*Table 2: Ablation Study Results. Performance comparison by removing each core component of our framework. The full model achieves the best results, while excluding geometry-guided self-attention, ego prior, or clean latent conditioning causes performance degradation. Best results are highlighted in bold, and second-best results are underlined*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_08269/figures/002_Figure_2.jpg]]
*Figure 2: Exo-to-Ego view generation example. The model has to preserve view-related content from the exocentric input, generate uninformed regions realistically, and ignore unrelated areas for consistent egocentric synthesis*



## 实验与关键发现

### 核心定量结果

EgoX在已见（Seen）和未见过（Unseen）场景上均取得最优综合性能，尤其在图像级和对象级指标上显著领先基线。Table 1汇总了主要对比结果：

- **已见场景**：PSNR达16.05 dB，较Exo2Ego-V的14.53 dB提升1.52 dB；FVD从622.47骤降至184.47，降幅达438点，表明生成视频的时序一致性与真实度大幅改善。
- **未见过场景**：PSNR为14.38 dB（Exo2Ego-V为12.70 dB，+1.68 dB），FVD从1283.50降至440.64（−842.86），泛化优势明确。

需注意，Wan VACE在部分视频级指标上得分更高，但该现象源于其倾向于生成静态输出，导致视频指标虚高，并非真实质量优势。Figure 5的定性对比进一步印证：EgoX生成的自我中心视图几何准确、细节连贯，而基线方法普遍存在失真、内容丢失或帧间不一致问题。

### 消融分析

Table 2和Table 3分别在已见/未见过场景上验证了三个核心组件的必要性，Figure 6提供对应的视觉消融对比：

- **移除几何引导自注意力（w/o GGA）**：PSNR降至14.77（−1.28），FVD升至254.08（+约70）。Figure 7的注意力图可视化揭示，无GGA时模型会关注外中心视图中的无关区域，而加入GGA后注意力集中到几何对齐的相关区域，空间一致性显著增强。
- **移除自我中心先验（w/o Ego prior）**：PSNR骤降至13.67（−2.38），降幅最大。这表明粗略渲染的自我中心先验为模型提供了关键的视角引导，缺失后模型失去空间锚点，视觉合理性大幅退化。
- **移除清洁潜变量条件（w/o clean latent）**：PSNR降至15.07（−0.98），FVD升至343.33（+约159）。清洁潜变量级联策略确保整个去噪过程中外中心的细粒度细节不丢失，移除后细节保真度明显受损。

此外，Table 4的条件注入策略消融表明，EgoX采用的“宽度级联清洁外中心潜变量+通道级联自我中心先验”方案在所有指标上均优于通道级联基线（Wan Fun Control）和辅助编码网络方案（Wan VACE）。GGA训练/推理方式的消融也确认了集成设计的必要性。

深度对齐的消融（Figure 9）显示，未进行深度对齐会导致点云渲染中的帧间深度不一致，引入虚假相机运动，破坏时域稳定性。

### 失败模式与局限性

Figure 12展示了一个典型失败案例：当外中心输入中动作线索极其稀疏、高度模糊时（如小幅度、部分遮挡的手部动作），模型可能误解动作意图，生成不准确的自我中心视角。该问题本质上是任务高歧义性所致，即人类观察者在相同稀疏证据下同样难以正确推断动作，并非纯粹的模型失效。

其他已知局限包括：当前框架需人工指定自我中心相机姿态（野生场景中通过Viser交互式设置，见Figure 8），尚未集成自动头部姿态估计；在极端姿态变化和高度动态场景下，几何一致性与细节保真度仍有提升空间。

### 运行效率

Table 5报告了各组件在NVIDIA H200 GPU上的运行时间。整体pipeline可在单段外中心视频上高效完成推理，具体耗时分布参见该表。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_08269/figures/013_Figure_10.jpg]]
*Figure 10: GGA benefits example. Without GGA, events occurring outside the visible region are attended to, leading to the generation of unwanted events in the ego view. With GGA, the model effectively focuses only on the visible region, thereby preventing the generation of these unwanted events*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_08269/figures/006_Table_1.jpg]]
*Table 1: Quantitative Results. Comparison on image, object, and video metrics. Our method achieves the best overall performance, with Wan VACE showing higher video scores due to static outputs. Best results are highlighted in bold, and second-best results are underlined*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_08269/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison. Each example shows the exocentric input views and the corresponding generated egocentric views. While other methods fail to reconstruct realistic and coherent videos, our approach produces geometrically accurate and high-quality egocentric generations. N/A indicates that the result is unavailable either due to missing ground truth or the need for additional input views*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2512_08269/figures/008_Figure_6.jpg]]
*Figure 6: Ablation qualitative comparison. Visual results when removing each core component. Removing any single component, GGA, the egocentric prior, or the clean latent representation, results in degraded generation quality and geometric consistency*



## 定位与知识库关联

### 1. 任务定义与核心瓶颈

EgoX 解决的是**从单段外中心（第三人称）视频生成对应自我中心（第一人称）视频**的跨视角生成任务。该任务的核心瓶颈在于：从外中心到自我中心视角的变换通常涉及极端相机姿态变化，导致外中心画面中大面积区域在自我中心视角下不可见，模型必须合理合成这些未观测区域，同时精确抑制外中心视频中不相关的背景内容。现有相机控制类视频生成模型难以处理如此剧烈的视角变换。

### 2. 与基线方法的关系定位

EgoX 在方法谱系上处于**预训练视频扩散模型 + 几何先验引导的视角变换生成**这一交叉区域。其与主要基线的关系如下：

- **Exo2Ego-V**：作为外中心到自我中心视频生成的直接基线，该方法在定量指标上显著落后于 EgoX（Seen Scenes PSNR 14.53 vs. 16.05，FVD 622.47 vs. 184.47），说明单纯依赖数据驱动映射难以应对极端视角变换下的不可见区域合成问题。

- **TrajectoryCrafter**：作为相机控制类基线，其设计目标更偏向于平滑的相机轨迹控制，而非剧烈的第一/第三人称视角切换。在 EgoX 的实验设定下，该类方法难以维持几何一致性和视觉质量。

- **Wan Fun Control**（通道级联条件注入）与 **Wan VACE**（辅助编码网络条件注入）：这两类条件注入策略分别代表了扩散模型中条件控制的两种主流范式。EgoX 的实验表明，单纯的通道级联或辅助编码器方案在处理外中心到自我中心视角变换时，均无法同时兼顾细节保留与几何一致性。Wan VACE 虽然在视频级指标上表现较高，但这是由于生成了近乎静态的输出，本质上并未真正解决视角变换问题。

EgoX 的方法创新在于将三类技术要素进行了系统集成：
1. **几何引导自注意力（GGA）**：通过 3D 方向余弦相似度偏置，在注意力计算中显式注入空间对应关系，使自我中心查询 token 聚焦于外中心键 token 中几何对齐的区域。
2. **统一条件注入策略**：对外中心潜变量采用**宽度级联**（width-wise concatenation），对自我中心先验潜变量采用**通道级联**（channel-wise concatenation），且外中心潜变量保持清洁（clean latent $x_0$）并在整个去噪过程中固定不变，仅更新噪声潜变量 $z_t$。
3. **轻量级 LoRA 适配**：基于 Wan 2.1 (14B) Inpainting 变体的预训练时空先验，通过 rank=256 的 LoRA 进行微调，避免全参数微调的高昂成本。

### 3. 技术谱系中的独特定位

从条件注入策略的角度，EgoX 的清洁潜变量级联方案区别于 SDEdit 式的噪声潜变量级联。其核心思想是：将外中心视频的 VAE 编码潜变量 $x_0$ 作为固定条件与噪声潜变量 $z_t$ 在宽度维度拼接，使得模型在所有去噪时间步上都能直接访问外中心的细粒度细节，而非仅依赖逐步去噪过程中的间接信息传递。这一设计与通道级联的自我中心先验 $p_0$ 形成互补——前者保留源域细节，后者提供目标域几何引导。

从注意力机制的角度，GGA 引入的几何偏置项为：
$$s_{m,n}^{\prime} = s_{m,n} + \log( g( \hat{q}_m, \hat{k}_n ) \cdot \lambda_g )$$
其中几何先验 $g( \hat{a}, \hat{b} ) = \cos \angle \mathrm{sim}( \hat{a}, \hat{b} ) + 1$，基于 3D 方向向量间的余弦相似度。这一设计使得最终的注意力权重同时融合了语义相似度（原始 logits）和几何对齐度（乘法偏置项），从而在跨视角生成中实现了空间选择性的信息聚合。

### 4. 适用边界与局限

1. **自我中心相机姿态依赖**：当前框架需要自我中心相机姿态 $\phi$ 作为输入。在受控数据集（如 Ego-Exo4D）中可直接获取，但在野生场景中需通过 Viser 等工具手动指定外参。这限制了方法的全自动化部署能力。

2. **高歧义性场景的动作误解**：当外中心输入中动作线索极为稀疏或部分遮挡时，模型可能产生动作误解。论文明确指出这并非纯粹的模型失败，而是任务本身的高歧义性所致——在此类场景下，即使人类观察者也难以准确推断动作。

3. **未见场景的泛化衰减**：在 Unseen Scenes 上，PSNR 从 16.05 降至 14.38，FVD 从 184.47 升至 440.64，表明泛化能力仍有提升空间。这一衰减趋势在所有消融变体上保持一致，说明核心挑战在于跨场景的几何与外观泛化，而非特定组件的过拟合。

4. **多动态对象场景的未验证能力**：当前实验主要围绕以人物为中心的场景，模型能否处理包含多个独立动态对象的复杂外中心输入仍有待验证。

### 5. 开放问题

- 如何集成自动头部姿态估计模块，消除对人工指定自我中心相机姿态的依赖？
- 如何在极端姿态变化和高度动态场景下进一步提升几何一致性与不可见区域的合成质量？
- 模型能否泛化到更广泛的外中心输入类型，如多人物交互、动态背景占主导的场景？
- 清洁潜变量固定策略是否在所有时间步上均为最优？是否存在自适应调整 $x_0$ 的信息注入强度的改进空间？



## 原文 PDF

![[paperPDFs/CVPR_2026/EgoX_Egocentric_Video_Generation_from_a_Single_Exocentric_Video.pdf]]
