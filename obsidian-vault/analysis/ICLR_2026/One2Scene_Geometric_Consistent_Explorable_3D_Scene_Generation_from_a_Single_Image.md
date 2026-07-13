---
title: "One2Scene: Geometric Consistent Explorable 3D Scene Generation from a Single Image"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/One2Scene_Geometric_Consistent_Explorable_3D_Scene_Generation_from_a_Single_Imag_271d95caee6f.pdf
project_link: "https://one2scene5406.github.io/"
code_link: null
aliases:
- One2Scene
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 将病态问题分解为三个可控子任务，并引入前馈3D高斯泼溅网络生成显式几何支架，为生成过程提供稳定的3D几何和外观先验，从而从根本上缓解几何不一致和误差积累。
primary_logic: 通过将单目全景深度估计重新表述为多视图立体匹配问题，并利用双向特征融合模块加强跨视图一致性，可以高效构建几何精确的3D支架；该支架为任意视角的新视图合成提供强先验，结合双LoRA训练策略处理异质条件，显著提升生成视图的逼真度和多视图一致性。
claims:
- 将全景投影为六个立方体贴图锚点视图，将深度估计转化为多视图立体匹配，利用大规模多视图数据集的几何先验。
- 双向融合模块通过C2E/E2C变换对齐重叠区域特征，增强跨视图几何一致性。
- 使用3D几何支架渲染的目标视图作为条件，结合双LoRA策略引导新视图合成，几何度量（TransErr、RotErr、CamMC）大幅优于此前方法。
- 3D场景生成（DL3DV+RealEstate10K测试集） 上 CLIP-I ↑ = 89.95
---

# One2Scene: Geometric Consistent Explorable 3D Scene Generation from a Single Image

> [!tip] 核心洞察
> 通过将单目全景深度估计重新表述为多视图立体匹配问题，并利用双向特征融合模块加强跨视图一致性，可以高效构建几何精确的3D支架；该支架为任意视角的新视图合成提供强先验，结合双LoRA训练策略处理异质条件，显著提升生成视图的逼真度和多视图一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | One2Scene：从单张图像生成几何一致的可探索3D场景 |
| 英文题名 | One2Scene: Geometric Consistent Explorable 3D Scene Generation from a Single Image |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=iEelSbUsSy) · [Project](https://one2scene5406.github.io/) · [paper](https://arxiv.org/abs/2411.04928) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | One2Scene |
| Dataset | 3D场景生成（DL3DV+RealEstate10K测试集）, 全景深度估计（Stanford2D3D）, 全景深度估计（Matterport3D） |

> [!tip] 效果简介
> - 3D场景生成（DL3DV+RealEstate10K测试集） 上，CLIP-I ↑ 89.95 vs 87.82 (SEVA) (+2.13)。
> - 同上 上，CamMC ↓ 0.389 vs 0.998 (VMem) (-0.609)。
> - 全景深度估计（Stanford2D3D） 上，AbsRel ↓ (零样本) 0.0675 vs 0.0984 (ACDNet) (-0.0309)。

## 概要

**问题与瓶颈**：从单张图像生成可自由探索的3D场景是一个严重病态的问题——输入信息极度稀疏，大视角变化下的几何失真和长距离多视图一致性难以维持。现有方法（如迭代导航修复或基于全景的隐式生成）在连续视角移动中积累误差，最终导致几何坍塌和语义漂移。

**核心思路**：One2Scene 将这一病态问题分解为三个可控的子任务，并引入一个前馈3D高斯泼溅（3DGS）网络来构建显式几何支架，为生成过程提供稳定的3D先验。关键洞察在于：将单目全景深度估计重新表述为多视图立体匹配问题，通过双向特征融合（C2E/E2C）强化跨视图几何一致性，从而高效构建精确的3D支架；该支架为任意视角的新视图合成提供强条件，配合双LoRA训练策略处理异质条件输入，显著提升生成视图的逼真度和多视图一致性。

**方法定位**：One2Scene 属于“前馈重建+条件生成”的混合范式，区别于纯自回归视频扩散（如VMem）或迭代优化（如Wonderjourny）路线。其三级流水线——全景锚点生成 → 前馈3DGS支架构建 → 支架引导的新视图合成——在几何显式性和推理效率之间取得了平衡。

**主要结果**：在3D场景生成任务上，One2Scene 的相机一致性指标 CamMC 达到 **0.389**，大幅优于 VMem（0.998）；在全景深度估计的零样本测试中，AbsRel 降至 **0.0675**，较 ACDNet（0.0984）提升约31%。消融实验表明，将前馈重建网络替换为 AnySplat 会导致生成质量显著下降（NIQE: 4.96 vs 4.43），验证了高精度3D支架对最终生成质量的决定性作用。



从单张图像生成可自由探索的3D场景是计算机视觉与图形学中长期存在的核心挑战。其本质困难在于：输入仅为二维平面的稀疏观测，却要求输出覆盖大范围视角、保持几何与语义一致的三维表征。这一问题的病态性（ill-posedness）体现在三个层面：其一，单张图像提供的信息极度不足，遮挡区域、场景背面以及超出视场角的内容完全不可见；其二，在大视角变化下，现有方法普遍出现几何坍塌和语义漂移，生成的新视图往往伴随扭曲、撕裂或内容不一致的伪影；其三，长距离相机运动中的时序一致性难以维持，迭代式生成框架会逐步累积误差，导致场景结构逐渐退化。

现有方法可大致归为两类范式。第一类是基于全景图的生成管线，如 **Dreamscene360**（Zhou et al., ECCV 2024）和 **Pano2Room**（Pu et al., SIGGRAPH Asia 2024），它们首先从输入图像生成360°全景，再将其提升为3D表示。这类方法虽然提供了全局的场景上下文，但全景深度估计本身是一个单目病态问题——传统方法（如Panoformer、Bifuse）缺乏跨视图的几何约束，估计的深度图在重叠区域存在明显的不一致性，导致后续3D重建出现几何错位和语义断裂。第二类是基于迭代导航与修复的方法，如 **Wonderjourny** 和 **VMem**，它们通过逐步扩展已生成区域来构建场景。这类方法的根本缺陷在于误差累积：每一步的微小偏差在迭代过程中被放大，最终导致大范围场景的几何结构发生系统性偏移。

从更根本的视角审视，上述方法共享一个关键瓶颈：缺乏一个显式的、几何可靠的3D先验来锚定生成过程。全景方法将3D推理简化为2D深度回归，丢失了多视图间的几何一致性约束；迭代方法则完全依赖隐式的生成先验，缺乏对场景全局几何结构的显式建模。这引出了一个核心问题：能否在生成过程的早期阶段，高效地构建一个几何精确的3D支架（scaffold），为后续的任意视角合成提供稳定的几何与外观先验？

One2Scene 正是围绕这一核心洞察展开。该方法将单图像到可探索3D场景这一严重病态问题分解为三个可控的子任务：首先生成全景锚点视图以建立全局上下文，然后通过前馈3D高斯泼溅网络将稀疏锚点视图提升为显式几何支架，最后在支架引导下合成任意目标视角的新视图。这一分解策略的关键在于：将单目全景深度估计重新表述为多视图立体匹配问题，并引入双向特征融合模块强制跨视图几何一致性，从而从根本上缓解了深度估计的歧义性和误差累积问题。显式3D支架的引入，使得新视图合成不再仅依赖稀疏的锚点图像，而是获得了来自几何先验的强条件信号，显著提升了大视角变化下的生成逼真度和多视图一致性。



## 核心方法与创新机理

### 问题重构：从病态单目估计到多视图立体匹配

One2Scene 的核心创新在于对单张图像生成可探索 3D 场景这一严重病态问题的根本性重构。传统方法直接预测全景深度或依赖迭代式修复，在大视角变化下累积误差，导致几何坍塌和语义漂移。One2Scene 将该问题分解为三个可控子任务：全景锚点生成、显式 3D 几何支架构建、以及支架引导的新视图合成。

最关键的范式转变发生在第二阶段：**将单目全景深度估计重新表述为多视图立体匹配问题**。具体而言，将生成的全景图投影为六张透视立方体贴图作为稀疏锚点视图，利用大规模多视图数据集的几何先验进行深度估计。这一转变使模型能够利用成熟的立体匹配机制，从根本上缓解了单目估计固有的尺度歧义和几何不确定性。

### 双向融合模块：强制跨视图几何一致性

立方体贴图的六个视图之间存在重叠区域，但传统方法缺乏显式的跨视图特征融合机制。One2Scene 引入**双向融合模块**，通过 C2E（Cube-to-Equirectangular）和 E2C（Equirectangular-to-Cube）变换建立跨视图几何对应：

$$\mathbf{F}_{e} = \mathbf{H}_{c}( \mathbf{C}2\mathbf{E}( \{ \mathbf{F}_{i} \}_{i=1}^{6} ) ), \quad \mathbf{F}_{i}^{\prime} = \mathbf{F}_{i} + \mathbf{E}2\mathbf{C}( \mathbf{F}_{e} )$$

该模块首先将六个立方体贴图的特征图经 C2E 变换融合为等矩形潜空间表示，再经 E2C 变换映射回各视图并以残差方式叠加。这一设计实现了两个关键目标：在潜空间中强制重叠区域的几何一致性，同时通过残差连接保留各视图特有的局部细节。该模块集成在预训练 VGGT 的 DPT 头中，使其成为前馈 3D 高斯泼溅网络的几何感知特征提取器。

### 前馈 3D 几何支架：显式几何先验的构建

基于双向融合后的特征，前馈 3D 高斯泼溅网络为全景图的每个像素预测一组 3D 高斯参数，将 2D 锚点视图提升为显式的 3D 几何支架。高斯中心的计算遵循：

$$\pmb{\mu} = \mathbf{K}^{-1} \pmb{u} d + \bar{\Delta}$$

即利用预测深度 $d$ 和相机内参 $\mathbf{K}$ 将像素坐标反投影到 3D 空间，并加上可学习的位置偏移 $\bar{\Delta}$ 以补偿深度估计误差。这一显式支架的核心价值在于：它可以从任意视角渲染目标视图，为新视图合成提供**强几何和外观先验**，从根本上解决了此前方法中迭代生成导致的误差累积问题。实验表明，该前馈模型仅需约 0.5 秒即可完成支架重建。

### 双 LoRA 训练策略：异质条件的解耦处理

支架渲染视图与原始锚点视图在图像分布上存在显著差异——前者包含由 3DGS 渲染带来的模糊和伪影，后者则是清晰的真实图像。直接通道拼接或共享编码器会混淆这两种异质信号。One2Scene 提出**双 LoRA 训练策略**，使用两个独立的 LoRA 模块分别处理锚点视图和支架渲染视图，通过 3D 注意力机制融合两者的特征。这一设计使模型能够分别适应两种条件模态的分布特性，同时充分利用支架提供的几何约束。

### 条件概率的递进式扩展

One2Scene 的条件建模体现了递进式的设计哲学，从基础锚点条件逐步扩展为完整的几何-时序条件：

1. **锚点条件合成**：$p\left(\mathbf{I}^{\mathrm{tgt}} \mid \mathbf{I}^{\mathrm{anchor}}, \mathbf{p}^{\mathrm{anchor}}, \mathbf{p}^{\mathrm{tgt}}\right)$，仅以锚点视图和姿态为条件。
2. **支架条件合成**：$p\left(\mathbf{I}^{\mathrm{tgt}} \mid \mathbf{I}^{\mathrm{anchor}}, \mathbf{p}^{\mathrm{anchor}}, \mathbf{I}^{\mathrm{render}}, \mathbf{p}^{\mathrm{tgt}}\right)$，引入从支架渲染的目标视角视图作为额外几何条件。
3. **记忆条件合成**：$p\left(\mathbf{I}^{\mathrm{tgt}} \mid \mathbf{I}^{\mathrm{anchor}}, \mathbf{p}^{\mathrm{anchor}}, \mathbf{I}^{\mathrm{render}}, \mathbf{I}^{\mathrm{mem}}, \mathbf{p}^{\mathrm{mem}}, \mathbf{p}^{\mathrm{tgt}}\right)$，进一步引入记忆帧及其姿态以保证长序列生成中的时空一致性。

这一递进式扩展使模型能够同时利用全局锚点信息、显式几何约束和时序上下文，在 CamMC 指标上达到 0.389，显著优于 VMem 的 0.998（越低越好），证明了支架条件对几何一致性的决定性作用。

### 与基线方法的本质差异

| 设计维度 | 基线方法 | One2Scene |
|---------|---------|-----------|
| 深度估计范式 | 单目全景估计（Panoformer、Bifuse 等），缺乏多视图几何约束 | 六视图立体匹配，利用多视图几何先验 |
| 跨视图一致性 | 无显式融合或重叠区域不足导致失效 | 双向融合模块（C2E/E2C）强制边界一致性 |
| 新视图合成条件 | 仅锚点视图或简单通道拼接 | 双 LoRA 分别处理锚点视图与支架渲染视图，经 3D 注意力融合 |
| 几何先验形式 | 隐式或迭代累积 | 显式 3D 高斯支架，可任意视角渲染 |

消融实验进一步验证了这些创新的关键性：将前馈重建网络替换为 AnySplat 后，NIQE 从 4.43 升至 4.96（质量下降），Q-Align 从 4.13 降至 3.61，CamMC 从 0.389 升至 0.616，表明高精度 3D 支架对最终生成质量具有决定性影响。



One2Scene 将“单张图像→可探索3D场景”这一严重病态问题分解为三个可控子任务，构建了一条从稀疏观测到显式几何支架再到任意视角逼真渲染的前馈流水线。其核心洞察在于：**显式3D几何支架**为生成过程提供了稳定的尺度约束和外观先验，从根本上缓解了现有方法在大视角变化下的几何坍塌与误差累积问题。

### 三阶段流水线概览

如图2所示，整个框架由三个阶段级联而成：

1. **锚点视图生成**：输入单张图像，通过专用的图像到全景生成模型（Hunyuan-Pano-DiT）生成360°全景图，为场景提供全局锚点视图。
2. **3D几何支架构建**：将全景图投影为六张立方体贴图（cubemap）锚点视图，利用前馈3D高斯泼溅（3DGS）网络将2D观测提升为显式3D高斯表示，构建几何可靠的3D支架。
3. **支架引导的新视图合成**：以锚点视图和从支架渲染的目标视图为条件，通过双LoRA策略和3D注意力机制生成任意相机姿态下的高质量新视图。

### 数据流与模块关系

**阶段一（锚点视图生成）** 接收单张RGB图像，输出一张360°全景图。该全景图作为后续所有模块的全局锚点，定义了场景的语义和布局边界。

**阶段二（3D几何支架构建）** 是框架的核心创新所在。它将全景深度估计重新表述为多视图立体匹配问题：
- 首先将360°全景投影为六张透视立方体贴图，作为稀疏锚点视图；
- 通过**双向融合模块**（C2E/E2C变换）在六视图间循环融合特征，强制重叠区域的几何一致性：C2E将六张立方体特征图融合为等矩形潜空间，E2C再将融合特征反投影回各视图并以残差方式相加，从而在保留局部细节的同时建立跨视图几何对应；
- 融合后的特征送入前馈3DGS网络，为每个像素预测一组高斯参数（中心 $\pmb{\mu}$、不透明度 $\alpha$、协方差 $\pmb{\Sigma}$、颜色 $\pmb{c}$），其中高斯中心通过 $\pmb{\mu} = \mathbf{K}^{-1} \pmb{u} d + \bar{\Delta}$ 将预测深度反投影到3D空间并加上可学习的位置偏移。

该阶段输出一个显式3D高斯支架，可在约0.5秒内完成重建，并支持从任意视角渲染目标视图。

**阶段三（支架引导的新视图合成）** 以SEVA架构为基础，引入三项关键增强：
- **双LoRA训练策略**：使用两个独立的LoRA模块分别处理锚点视图和支架渲染视图，经3D注意力机制融合，使模型能有效利用异构条件信号；
- **记忆条件模块**：从记忆库中选择最接近的已生成帧作为时序一致性条件，保证长序列生成中的时空连贯性。

合成过程的条件概率模型从基础的锚点条件 $p(\mathbf{I}^{\mathrm{tgt}} \mid \mathbf{I}^{\mathrm{anchor}}, \mathbf{p}^{\mathrm{anchor}}, \mathbf{p}^{\mathrm{tgt}})$ 逐步扩展至支架条件 $p(\mathbf{I}^{\mathrm{tgt}} \mid \mathbf{I}^{\mathrm{anchor}}, \mathbf{p}^{\mathrm{anchor}}, \mathbf{I}^{\mathrm{render}}, \mathbf{p}^{\mathrm{tgt}})$，最终引入记忆条件 $p(\mathbf{I}^{\mathrm{tgt}} \mid \mathbf{I}^{\mathrm{anchor}}, \mathbf{p}^{\mathrm{anchor}}, \mathbf{I}^{\mathrm{render}}, \mathbf{I}^{\mathrm{mem}}, \mathbf{p}^{\mathrm{mem}}, \mathbf{p}^{\mathrm{tgt}})$，逐层增强生成视图的逼真度与多视图一致性。

### 关键设计动机

现有方法（如 **Dreamscene360** (Zhou et al., ECCV 2024)、**Wonderjourny**）在迭代导航和修复过程中累积误差，导致大视角变化下出现明显的几何失真和伪影（见图1）。One2Scene通过**前馈3D支架**为任意视角的新视图合成提供强几何先验，从根本上切断了误差累积链条。消融实验（表2、图4）证实，将前馈重建网络替换为 **AnySplat** 会导致生成质量显著下降（NIQE: 4.96 vs 4.43, Q-Align: 3.61 vs 4.13），验证了高精度3D支架对最终生成质量的决定性作用。

### 补充图表

![[assets/figures/papers/paper_list_l55_https_openreview_net_forum_id_iEelSbUsSy/figures/002_Figure_2.jpg]]
*Figure 2: Overview of One2Scene. Our method consists of three stages: (a) an anchor view generation stage to establish an initial 360-degree representation, (b) a feed-forward 3D Gaussian Splatting stage to construct an explicit 3D geometric scaffold, and (c) a synthesis stage that leverages the scaffold information to produce high-quality novel views. The pipeline enables geometrically consistent and photorealistic novel view synthesis from a single input image*



One2Scene 将单图到可探索3D场景这一严重病态问题分解为三个可控子任务，其核心模块对应三阶段流水线：全景锚点生成、前馈3D几何支架构建、支架引导的新视图合成。

### 全景锚点生成

第一阶段采用专用的图像到全景生成模型（Hunyuan-Pano-DiT），将受限的单张输入视图转换为360°全景表示，为后续模块提供全局锚点视图。该全景随后被投影为六张透视立方体贴图，作为稀疏锚点视图集合 $\{\mathbf{I}_i\}_{i=1}^6$。

### 前馈3D高斯泼溅与双向融合

第二阶段是本方法的核心创新——将单目全景深度估计重新表述为多视图立体匹配问题。六张立方体贴图被送入共享权重的VGGT骨干网络提取特征，随后通过双向融合模块增强跨视图几何一致性。

**双向融合特征更新** 是保证几何一致性的关键机制：

$$\mathbf{F}_{e} = \mathbf{H}_{c}( \mathbf{C}2\mathbf{E}( \{ \mathbf{F}_{i} \}_{i=1}^{6} ) ), \quad \mathbf{F}_{i}^{\prime} = \mathbf{F}_{i} + \mathbf{E}2\mathbf{C}( \mathbf{F}_{e} )$$

其中 $\mathbf{F}_i$ 为第 $i$ 个立方体贴图的特征图，$\mathbf{C}2\mathbf{E}$ 变换将六视图特征融合为等矩形（equirectangular）潜空间表示，经可学习的卷积头 $\mathbf{H}_c$ 处理后得到 $\mathbf{F}_e$；$\mathbf{E}2\mathbf{C}$ 变换再将其映射回各立方体视图空间，以残差连接方式与原始特征相加得到增强特征 $\mathbf{F}_i^{\prime}$。该机制在重叠区域建立显式几何对应，同时保留各视图的局部细节。

融合后的特征经DPT深度头预测逐像素深度 $d$，进而通过反投影计算3D高斯中心：

$$\pmb{\mu} = \mathbf{K}^{-1} \pmb{u} d + \bar{\Delta}$$

其中 $\mathbf{K}$ 为相机内参矩阵，$\pmb{u}$ 为像素坐标，$\bar{\Delta}$ 为可学习的位置偏移量。前馈网络同时预测每个高斯的不透明度 $\alpha_i$、协方差 $\pmb{\Sigma}_i$ 和颜色 $\pmb{c}_i$，从而将2D锚点视图提升为显式3D几何支架。该支架可在任意新视角下渲染，为下游合成提供强几何先验。

### 支架引导的新视图合成与双LoRA

第三阶段以SEVA架构为基础，通过逐步引入条件实现高质量新视图合成。条件概率模型依次扩展为：

锚点条件合成：
$$p\left(\mathbf{I}^{\mathrm{tgt}} \mid \mathbf{I}^{\mathrm{anchor}}, \mathbf{p}^{\mathrm{anchor}}, \mathbf{p}^{\mathrm{tgt}}\right)$$

支架条件合成（加入从3D支架渲染的目标视图 $\mathbf{I}^{\mathrm{render}}$）：
$$p\left(\mathbf{I}^{\mathrm{tgt}} \mid \mathbf{I}^{\mathrm{anchor}}, \mathbf{p}^{\mathrm{anchor}}, \mathbf{I}^{\mathrm{render}}, \mathbf{p}^{\mathrm{tgt}}\right)$$

记忆条件合成（进一步引入记忆帧 $\mathbf{I}^{\mathrm{mem}}$ 及其姿态 $\mathbf{p}^{\mathrm{mem}}$）：
$$p\left(\mathbf{I}^{\mathrm{tgt}} \mid \mathbf{I}^{\mathrm{anchor}}, \mathbf{p}^{\mathrm{anchor}}, \mathbf{I}^{\mathrm{render}}, \mathbf{I}^{\mathrm{mem}}, \mathbf{p}^{\mathrm{mem}}, \mathbf{p}^{\mathrm{tgt}}\right)$$

**双LoRA训练策略** 是处理异质条件的关键设计：锚点视图和支架渲染视图分别通过两个独立的LoRA模块处理，经3D注意力机制融合后注入扩散去噪过程。记忆条件模块则从记忆库中选择与目标姿态最接近的已生成帧，保障长序列生成中的时空一致性。该策略使模型能够同时利用锚点视图的纹理细节和支架渲染视图的几何结构，显著缓解大视角变化下的几何失真问题。



## 实验与关键发现

### 核心性能对比

One2Scene 在 3D 场景生成任务上全面超越现有方法。表1（Table 1）汇总了在 DL3DV 与 RealEstate10K 联合测试集上的定量结果。在感知质量指标上，One2Scene 取得 **NIQE 4.43** 和 **Q-Align 4.13** 的最优成绩；在语义保真度上，**CLIP-I 达到 89.95**，较 SEVA 的 87.82 提升 2.13 个百分点。几何一致性方面的优势更为显著：**CamMC 仅 0.389**，而 VMem 为 0.998，降幅达 0.609；TransErr 与 RotErr 也均处于最低水平。这一差距的根源在于显式 3D 几何支架提供了稳健的尺度约束——VMem 等依赖隐式几何先验的方法在面对大视角变化时，常因尺度歧义导致几何坍塌，而 One2Scene 的支架从源头上锚定了全局空间结构。

![[assets/figures/papers/paper_list_l55_https_openreview_net_forum_id_iEelSbUsSy/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparisons for 3D scene generation*

全景深度估计的零样本泛化能力进一步验证了双向融合模块的有效性。在 Stanford2D3D 数据集上，One2Scene 取得 **AbsRel 0.0675**，较 ACDNet 的 0.0984 降低 30.9%（Table 3）。微调后，在 Matterport3D 上 AbsRel 进一步降至 0.0391。这一性能增益源于将单目全景深度估计重新表述为多视图立体匹配：立方体贴图的六视角投影使模型能够利用大规模多视图数据集中习得的几何先验，而 C2E/E2C 双向融合机制强制了重叠区域的跨视图一致性，避免了传统全景深度估计中边界不连续的问题。

![[assets/figures/papers/paper_list_l55_https_openreview_net_forum_id_iEelSbUsSy/figures/006_Table_3.jpg]]
*Table 3: Comparison of depth estimation on Matterport3D and Stanford2D3D datasets*

定性对比（Figure 3）显示，在大视角变化下，Wonderjourny 和 Dreamscene360 出现明显的几何畸变与伪影，而 One2Scene 生成的视图保持了逼真的纹理细节和场景连贯性。Figure 1 进一步佐证了这一点：输入图像仅覆盖场景的局部区域，但 One2Scene 能生成几何精确且语义合理的不可见区域。

![[assets/figures/papers/paper_list_l55_https_openreview_net_forum_id_iEelSbUsSy/figures/001_Figure_1.jpg]]
*Figure 1: Comparison on large-viewpoint novel view synthesis. Existing methods such as Wonderjourny (Yu et al., 2023) and Dreamscene360 (Zhou et al., 2024) exhibit clear geometric distortions and artifacts, while our method generates photorealistic and geometrically accurate novel views. The input image is highlighted by a red bounding box. The other images represent the novel views*

![[assets/figures/papers/paper_list_l55_https_openreview_net_forum_id_iEelSbUsSy/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparison. Our method retains compelling visual quality and generates plausible continuations of the scene, even under large viewpoint change*

### 消融实验：3D 支架精度的决定性作用

为量化显式几何支架的贡献，论文将前馈 3DGS 重建网络替换为 AnySplat（Table 2, Figure 4）。替换后，生成质量出现系统性退化：**NIQE 从 4.43 恶化至 4.96**，**Q-Align 从 4.13 降至 3.61**，CLIP-I 更是从 89.95 骤降至 81.96。几何指标同样大幅下滑——RotErr 从 0.107 升至 0.367，CamMC 从 0.389 升至 0.616。Figure 4 的可视化对比直观揭示了退化模式：AnySplat 重建的支架存在明显的几何空洞和结构扭曲（顶行），这些缺陷直接传播到最终的生成视图中，导致漂浮物和纹理撕裂（底行）。该消融强有力地证明，高精度 3D 支架不仅是辅助条件，而是保证多视图几何一致性的关键瓶颈。

![[assets/figures/papers/paper_list_l55_https_openreview_net_forum_id_iEelSbUsSy/figures/005_Table_2.jpg]]
*Table 2: Comparison on the 3D scene generation performance by replacing our feed-forward 360° reconstruction network with AnySplat*

![[assets/figures/papers/paper_list_l55_https_openreview_net_forum_id_iEelSbUsSy/figures/007_Figure_4.jpg]]
*Figure 4: Ablation study on reconstruction performance. We compare the 3D scene generation quality by replacing our feedforward network with AnySplat. Top row: reconstruction results. Bottom row: generation results using our model*

### 失败模式与局限性

尽管整体性能优异，One2Scene 仍存在若干可识别的失败模式：

1. **全景生成器的错误传播**：当前框架中全景生成模型为固定组件，若其在输入图像内容稀缺或语义模糊时生成失真的全景，该错误会直接污染后续的支架构建与新视图合成，且缺乏纠正机制。
2. **极端几何条件下的支架缺陷**：在高度遮挡或强反射表面区域，前馈 3DGS 网络预测的深度可能不准确，导致支架出现空洞或伪影。这些缺陷在大视角渲染时尤为明显。
3. **缺乏后处理几何优化**：与 CAT3D 等方法不同，One2Scene 未引入后处理步骤来抑制时序闪烁和漂浮高斯。在长序列自由探索轨迹中，累积的微小误差可能逐渐显现为视觉不一致。
4. **训练数据覆盖有限**：当前训练集（DL3DV + RealEstate10K）以室内和城市场景为主，对室外自然场景的泛化能力尚未验证。更大规模且类别多样化的数据训练有望缓解此问题。

### 关键图表结论速览

- **Table 1**：One2Scene 在所有 6 项指标上均取得最优，CamMC 优势尤为突出，验证了显式支架对几何一致性的核心贡献。
- **Table 2 / Figure 4**：替换为 AnySplat 后生成质量全面退化，证明高精度 3D 支架是不可或缺的瓶颈组件。
- **Table 3**：全景深度估计的零样本与微调结果均显著优于基线，验证了多视图立体匹配范式与双向融合模块的有效性。
- **Figure 3**：大视角变化下的定性对比直观展示了 One2Scene 在几何保真度和视觉质量上的代际优势。



## 定位与知识库关联

### 问题分解范式的谱系定位

One2Scene 的核心贡献在于将“单图→可探索3D场景”这一严重病态问题分解为三个可控子任务：全景锚点生成、前馈3D显式支架构建、支架引导的新视图合成。这一分解策略在谱系上区别于两类主流路线。

**迭代式生成路线**的代表如 **Wonderjourny** 和 **Dreamscene360**（Zhou et al., ECCV 2024），它们通过逐步导航和修复来扩展场景，但每次迭代的微小误差会累积，最终导致几何坍塌和语义漂移——Figure 1 的定性对比清晰展示了这一失效模式。One2Scene 通过一次性构建全局3D支架，从根本上切断了误差累积链条。

**隐式几何先验路线**的代表如 **VMem**，它通过视频扩散模型整合几何先验，但缺乏显式的3D约束。One2Scene 的3D高斯支架提供了明确的尺度约束，有效缓解了单目场景生成中的尺度歧义问题——在 CamMC 指标上，One2Scene 达到 0.389，显著优于 VMem 的 0.998（Table 1），降幅达 61%。

**专用场景生成路线**如 **Pano2Room**（Pu et al., SIGGRAPH Asia 2024）专注于室内场景，而 One2Scene 不限于特定场景类型，其前馈重建网络在 Structured3D、Deep360、Matterport3D、Stanford2D3D 四个数据集上联合训练，覆盖合成与真实场景。

### 深度估计范式的跃迁

在全景深度估计子任务上，One2Scene 完成了一次范式跃迁。传统方法如 Panoformer、Bifuse 等将全景深度估计视为单目问题，缺乏跨视图几何约束。One2Scene 将其重新表述为**多视图立体匹配问题**：将360°全景投影为六张立方体贴图锚点视图，使网络能够利用大规模多视图数据集中蕴含的立体几何先验。

这一范式跃迁的因果机制在于**双向融合模块（C2E/E2C）**。通过 Cube-to-Equirectangular 变换将六视图特征融合到等矩形潜空间，再经 Equirectangular-to-Cube 变换回各视图并残差相加：

$$\mathbf{F}_{e} = \mathbf{H}_{c}( \mathbf{C}2\mathbf{E}( \{ \mathbf{F}_{i} \}_{i=1}^{6} ) ), \quad \mathbf{F}_{i}^{\prime} = \mathbf{F}_{i} + \mathbf{E}2\mathbf{C}( \mathbf{F}_{e} )$$

该模块强制建立了立方体贴图边界重叠区的几何对应关系，同时保留了各视图的局部细节。在零样本设置下，Stanford2D3D 上的 AbsRel 从 ACDNet 的 0.0984 降至 0.0675（Table 3），降幅约 31%，验证了跨视图几何先验的迁移能力。

### 新视图合成的条件注入创新

在新视图合成阶段，One2Scene 基于 **SEVA** 架构，但引入了关键的条件注入创新。基线方法仅使用锚点视图作为条件：

$$p\left(\mathbf{I}^{\mathrm{tgt}} \mid \mathbf{I}^{\mathrm{anchor}}, \mathbf{p}^{\mathrm{anchor}}, \mathbf{p}^{\mathrm{tgt}}\right)$$

One2Scene 引入了两层额外条件。第一层是**支架渲染视图**，通过3D高斯支架从目标视角渲染得到：

$$p\left(\mathbf{I}^{\mathrm{tgt}} \mid \mathbf{I}^{\mathrm{anchor}}, \mathbf{p}^{\mathrm{anchor}}, \mathbf{I}^{\mathrm{render}}, \mathbf{p}^{\mathrm{tgt}}\right)$$

第二层是**记忆帧**，从记忆库中选择与目标视角最接近的已生成帧，保证长序列生成中的时空一致性：

$$p\left(\mathbf{I}^{\mathrm{tgt}} \mid \mathbf{I}^{\mathrm{anchor}}, \mathbf{p}^{\mathrm{anchor}}, \mathbf{I}^{\mathrm{render}}, \mathbf{I}^{\mathrm{mem}}, \mathbf{p}^{\mathrm{mem}}, \mathbf{p}^{\mathrm{tgt}}\right)$$

处理异质条件的核心技术是**双LoRA训练策略**：两个独立的 LoRA 模块分别处理锚点视图和支架渲染视图，随后通过 3D 注意力机制进行融合。这一设计避免了简单通道拼接导致的条件冲突。消融实验（Table 2）表明，将前馈重建网络替换为 **AnySplat** 后，生成质量显著下降（NIQE 从 4.43 升至 4.96，Q-Align 从 4.13 降至 3.61），证明高精度3D支架对最终生成质量的决定性作用。

### 适用边界与局限

**全景生成器的错误传播**：当前框架中全景生成模型（Hunyuan-Pano-DiT）为固定组件，其生成错误（如语义不一致、结构扭曲）会直接传播到下游的支架构建和新视图合成。这是一个串联系统的固有脆弱性。

**极端几何条件下的支架退化**：前馈3DGS网络在极端遮挡或高度反射表面下仍可能产生空洞或伪影。尽管双向融合模块增强了跨视图一致性，但六张立方体贴图的覆盖范围有限，无法处理完全不可见区域。

**缺乏后处理几何优化**：与 **CAT3D** 等方法不同，One2Scene 尚未引入后处理几何一致性优化步骤来抑制时序闪烁和漂浮物。这限制了长序列生成中的视觉稳定性。

**训练数据规模与多样性**：当前训练数据限于 DL3DV + RealEstate10K（新视图合成）和四个全景深度数据集（支架构建），在更大规模、更丰富类别（含室外自然场景）的数据集上训练可进一步提升泛化性。

### 开放问题

1. **后处理几何优化的集成**：如何将类似 CAT3D 的几何一致性优化无缝集成到前馈框架中，同时保持推理效率（当前支架构建仅需 0.5 秒）？

2. **数据规模化**：在更大规模且更丰富类别的数据集上训练是否会带来质的提升？特别是室外无界场景的支架构建仍是一个开放挑战。

3. **推理效率的进一步压缩**：前馈3DGS的推理时间虽已很快，但要支持实时可探索场景生成，仍需进一步压缩。

4. **可控生成的拓展**：能否将语言或文本条件融入支架构建过程，实现语义可控的场景生成？这需要重新设计条件注入机制。

5. **端到端联合优化**：当前三阶段为独立训练，端到端联合优化可能进一步提升各模块间的协同性，但面临的挑战在于不同模块的损失函数和训练数据如何统一。



## 原文 PDF

![[paperPDFs/ICLR_2026/One2Scene_Geometric_Consistent_Explorable_3D_Scene_Generation_from_a_Single_Imag_271d95caee6f.pdf]]
