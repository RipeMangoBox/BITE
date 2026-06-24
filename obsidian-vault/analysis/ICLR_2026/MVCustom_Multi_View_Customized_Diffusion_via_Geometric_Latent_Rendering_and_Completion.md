---
title: "MVCustom: Multi-View Customized Diffusion via Geometric Latent Rendering and Completion"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MVCustom_Multi_View_Customized_Diffusion_via_Geometric_Latent_Rendering_and_Comp_5fcfc95fff65.pdf
project_link: "https://minjung-s.github.io/mvcustom/"
code_link: null
aliases:
- MVCustom
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 在推理阶段显式注入几何约束：通过深度感知特征渲染（DFR）构建锚点特征网格并跨视角投影，再利用一致性潜在补全（CLC）生成被遮挡区域，从而在训练数据极度有限的情况下强制多视图几何一致性。
primary_logic: 将多视图生成重新定义为视频帧生成问题，利用预训练视频扩散模型（AnimateDiff）中密集时空注意力隐含的时间一致性，并将其迁移为多视图一致性；同时，在推理时通过从单帧估计的深度图构建特征网格并渲染到其他视角，以显式方式确保主体和周围环境的几何对齐，解决了定制化场景下数据稀缺与多视图要求之间的矛盾。
claims:
- MVCustom是唯一在相机姿态准确性、多视图一致性和定制化保真度三个维度上均取得领先的方法，而所有基线方法至少在一项上显著劣化。
- 消融实验证实，去除深度感知特征渲染和一致性潜在补全会导致周围环境静止不随视角变化，而加入后COLMAP重建点数从36.13提升至45.38，相机姿态准确性从0.543提升至0.771。
- 将原始AnimateDiff的1D时序注意替换为密集时空注意（STT）是必要的：1D注意在特征替换时无法保持空间一致性，而STT成功维持了语义流和几何对齐。
- CO3Dv2测试集（多视图定制任务） 上 相机姿态精度 (CPA↑) = 0.735 ± 0.10
---

# MVCustom: Multi-View Customized Diffusion via Geometric Latent Rendering and Completion

> [!tip] 核心洞察
> 将多视图生成重新定义为视频帧生成问题，利用预训练视频扩散模型（AnimateDiff）中密集时空注意力隐含的时间一致性，并将其迁移为多视图一致性；同时，在推理时通过从单帧估计的深度图构建特征网格并渲染到其他视角，以显式方式确保主体和周围环境的几何对齐，解决了定制化场景下数据稀缺与多视图要求之间的矛盾。

| 字段 | 内容 |
|------|------|
| 中文题名 | MVCustom：基于几何潜在渲染与补全的多视图定制扩散模型 |
| 英文题名 | MVCustom: Multi-View Customized Diffusion via Geometric Latent Rendering and Completion |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=SGsxxbAjXH) · [Project](https://minjung-s.github.io/mvcustom/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | MVCustom |
| Dataset | CO3Dv2测试集（多视图定制任务） |

> [!tip] 效果简介
> - CO3Dv2测试集（多视图定制任务） 上，相机姿态精度 (CPA↑) 0.735 ± 0.10 vs 0.000 ± 0.00 (CustomDiffusion360) (+0.735)；多视图一致性 (DreamSim ↓) 0.121 ± 0.10 vs 0.214 ± 0.15 (Custom Img + Img-MV gen) (-0.093)；主体身份保留 (DreamSim ↓) 0.448 ± 0.11 vs 0.504 ± 0.12 (Custom Img + Img-MV gen) (-0.056)。

## 概述

### 问题背景与核心瓶颈

在定制化生成任务中，用户通常仅提供少量参考图像来指定目标物体的外观与身份。现有方法若直接对文本到多视图扩散模型（如 **CameraCtrl**）应用 DreamBooth-LoRA 微调，会丧失相机可控性；而单图到多视图方法（如 **SEVA**）则产生跨视角伪影和主体身份丢失。**CustomDiffusion360** 虽具备视角感知能力，却仅聚焦主体、无法保证周围场景的全景一致性。因此，核心瓶颈在于：在训练数据极度有限的定制化场景下，如何同时实现多视角几何一致性、主体身份保真度和周围场景的全景一致生成。

### 核心思路与方法定位

MVCustom 将多视图生成重新定义为视频帧生成问题，其核心洞察是：预训练视频扩散模型中隐含的时间一致性可被迁移为多视图一致性。方法将训练与推理阶段分离：**训练阶段**利用姿态条件 Transformer 块（含 FeatureNeRF）从参考视图学习物体的三维特征场，并采用增强密集时空注意力的视频扩散骨干网络（AnimateDiff）捕获帧间依赖；**推理阶段**则显式注入几何约束——通过深度感知特征渲染（DFR）从锚点帧构建特征网格并跨视角投影，再利用一致性潜在补全（CLC）对被遮挡区域进行语义一致的补全，从而强制多视图几何对齐。

### 主要结果与关键发现

在 CO3Dv2 测试集上，MVCustom 是唯一在相机姿态准确性、多视图一致性和定制化保真度三个维度均取得领先的方法（Table 2）。相机姿态精度达到 0.735，而 CustomDiffusion360 为 0.000，表明基线方法完全丧失相机可控性。多视图一致性（DreamSim）为 0.121，较最佳基线降低 0.093；主体身份保留（DreamSim）为 0.448，降低 0.056。消融实验证实：加入 DFR 后 COLMAP 重建点数从 36.13 提升至 43.38，相机姿态精度从 0.543 提升至 0.768；进一步加入 CLC 后重建点数提升至 45.38。此外，密集时空注意力对特征替换时的空间一致性至关重要——1D 时序注意无法维持正确的语义平移，而密集时空注意成功保持了空间流与几何对齐（Figure 5b）。

## 背景与动机

### 多视图定制：一个尚未被充分探索的交叉任务

随着扩散模型在图像生成领域的成功，研究者们逐步将其能力边界从单图生成拓展至多视图生成和主体定制化两个方向。然而，将这两者结合——即在仅提供少量参考图像的条件下，同时实现**多视角几何一致性**、**主体身份保真度**和**周围场景的全景一致生成**——仍是一个几乎未被探索的难题。

Table 1 系统地对比了现有任务范式在这一交叉空间中的能力覆盖。传统的定制化方法（如 Textual Inversion、DreamBooth）虽然能够忠实保留参考主体的身份特征，但完全不具备多视图生成能力，无法输出不同视角下的图像。多视图生成方法（如 Zero-1-to-3、MVDream）虽然能够从文本或单张图像生成多视角一致的输出，却缺乏对特定主体身份的定制化保真度。即便是具备视角感知能力的定制化方法 **CustomDiffusion360**（Kumari et al., 2024），也仅关注主体本身的一致性，而忽略了周围场景在不同视角下的全景一致性。

### 现有方法的系统性缺口

当研究者试图将现有多视图模型直接适配到定制化场景时，会遭遇三类根本性瓶颈：

**瓶颈一：相机可控性的丧失。** 对文本条件相机可控模型（如 **CameraCtrl**）直接应用 DreamBooth-LoRA 微调（即 CameraCtrl + DreamBooth-LoRA 基线，He et al., 2024; Ruiz et al., 2023），虽然试图在保留定制化能力的同时维持视角控制，但实际上微调过程会破坏模型原有的相机姿态响应机制，导致生成结果无法准确对齐目标视角。

**瓶颈二：跨视角伪影与身份丢失。** 将单张定制图像输入图像条件多视图模型（如 **SEVA**，Zhou et al., 2025）的基线方案（Custom Img + Img-MV gen），在输入视角附近尚可维持主体外观，但随着目标视角偏离输入视角，主体身份迅速退化，同时产生严重的跨视角伪影。这是因为单图到多视图的方法缺乏对主体三维几何的显式建模，仅依靠从训练数据中学习到的统计先验来猜测不可见区域。

**瓶颈三：周围环境的视角不一致。** 仅依赖定制化微调（无额外几何约束）的方案会导致一个隐蔽但致命的问题：周围环境在不同视角下保持静态，不随相机运动而发生应有的透视变化。这意味着生成的背景实际上是一个“贴图”，而非真正的三维场景，从根本上破坏了多视图一致性。

### 核心洞察：将多视图生成重新定义为视频帧生成

MVCustom 的核心洞察在于识别出**多视图生成与视频帧生成之间的深层同构性**：相邻视频帧之间的时间一致性与相邻视角之间的空间一致性在数学形式上高度相似。预训练视频扩散模型（AnimateDiff）中的密集时空注意力层天然具备捕获帧间依赖的能力，这种能力可以被迁移为多视图一致性——前提是能够将相机姿态信息有效地注入生成过程，并在推理阶段显式地强制执行几何约束。

这一洞察直接回应了定制化场景下的核心矛盾：训练数据极度有限（仅数张参考图像），但多视图生成要求模型理解物体的三维几何和场景的空间结构。MVCustom 的策略是将这一矛盾拆解为两个可解的子问题——**训练阶段**通过姿态条件 Transformer 块和 FeatureNeRF 从有限视角中学习特征场，**推理阶段**通过深度感知特征渲染和一致性潜在补全显式注入几何约束——从而在数据稀缺的条件下实现多视角几何一致性。

## 核心创新

MVCustom 的核心创新在于将**多视图定制**问题重新定义为**视频帧生成**问题，并通过训练与推理两个阶段的协同设计，解决了现有方法在数据极度有限时无法同时保证几何一致性、主体身份保真度和全景场景一致性的瓶颈。其关键创新点可归纳为以下三个层面：

### 1. 问题重定义与骨干网络迁移

现有方法要么是纯文本/图像到多视图的生成模型（如 **CameraCtrl**，He et al., 2024），不具备定制化能力；要么是定制化方法（如 **CustomDiffusion360**，Kumari et al., 2024），缺乏相机姿态可控性。MVCustom 的因果性洞察在于：**多视图一致性本质上可被建模为时间一致性**。因此，方法将预训练**视频扩散模型 AnimateDiff** 作为生成骨干，将其固有的时序连贯性迁移为多视图空间一致性。这一设计使得模型无需大规模多视图配对数据即可学习跨视角的语义流和几何对齐。

### 2. 密集时空注意力替代1D时序注意

原始 AnimateDiff 使用**1D时序注意力**处理帧间关系，但在多视图场景的特征替换操作中，1D注意无法维持空间一致性——特征图被简单垂直复制，导致语义错位（Figure 5b）。MVCustom 将其替换为**密集时空注意力（Spatio-Temporal Transformer, STT）**，使注意力机制同时在空间和时间维度上建立依赖。消融实验证实，这一替换是特征注入成功的前提：STT 能够正确捕获相机平移带来的空间流变化，而1D注意则完全失败。

### 3. 推理阶段的显式几何约束注入

这是 MVCustom 最具区分度的创新。传统方法完全依赖训练数据隐式学习几何关系，在定制化场景下因数据稀缺而失效。MVCustom 在推理时引入两个互补模块：

- **深度感知特征渲染（Depth-aware Feature Rendering, DFR）**：从锚点帧估计深度图，构建特征网格 $\mathcal{M}_a$，再根据目标相机姿态 $\phi_n$ 渲染特征图 $\mathcal{F}_n^a$ 和可见性掩码 $M_n^a$，通过公式 $\hat{F}_n = M_n^a \odot F_n^a + (1 - M_n^a) \odot F_n$ 注入U-Net。这显式地强制执行了跨视角几何一致性。
- **一致性感知潜在补全（Consistent-aware Latent Completion, CLC）**：对深度渲染后新暴露的区域，通过向前扩散加噪再逐步去噪的随机扰动，生成语义一致且多样化的内容来补全，确保空间连续性。

消融实验（Table A3）定量验证了这一设计：仅定制化微调时，COLMAP 重构点数仅 36.13，相机姿态精度 0.543；加入 DFR 后分别提升至 43.38 和 0.768；再加入 CLC 后进一步提升至 45.38 和 0.771。视觉上，无 DFR/CLC 时周围环境在不同视角下保持静止，不随相机运动变化（Figure 5a-i），而加入后实现了准确的透视对齐。

### 4. 姿态条件 Transformer 与 FeatureNeRF

在训练阶段，MVCustom 设计了**姿态条件 Transformer 块**，内含 **FeatureNeRF** 模块。该模块从多视角参考图像及其相机姿态中学习物体的三维特征场，通过极线几何和体渲染合成目标姿态下的对齐特征图 $X_y := \mathrm{FeatureNeRF}(\{(X_i, \pi_i)\}_{i=1}^{N}, c, \phi)$。这一设计使模型在训练时就能学习姿态-外观的映射关系，为推理阶段的几何约束注入提供了特征空间的基础。

**局限性提示**：FeatureNeRF 学习的是固定的规范姿态，且其辐射场未将文本作为条件输入，因此无法根据文本提示改变定制化物体的内在姿态（如从坐到站）。此外，DFR 对深度估计质量敏感，反射或无纹理表面可能导致几何错误（Figure 6），但这归因于外部深度估计器而非方法本身。

## 整体框架

MVCustom 将多视图定制任务建模为一个条件生成问题：给定一组参考图像-相机位姿对 $\mathbf{Y}$、文本提示 $\mathbf{c}$ 和目标相机位姿序列 $\{\phi_m\}_{m=0}^{M}$，模型需要生成在目标视角下既保持主体身份、又与文本描述一致的多视图图像序列 $\mathbf{x}_{0:M}$。其核心架构围绕“训练阶段学习主体几何表征”与“推理阶段注入显式几何约束”两阶段设计展开。

### 训练管线

训练阶段的核心目标是让模型从少量多视图参考数据中学习定制化主体的身份与几何信息。整体管线（Figure 2a）包含两个并行的分支：

- **主分支（Main Branch）**：接收噪声潜在变量，通过空间Transformer层处理，负责生成图像内容。
- **多视图分支（Multi-View Branch）**：接收参考图像特征 $X_i$ 及其对应的相机位姿 $\pi_i$，通过**姿态条件Transformer块**（Pose-Conditioned Transformer Block）融合跨视角信息。

两个分支的输出特征图在通道维度拼接后，送入投影层融合，最终通过交叉注意力注入文本条件。这种双分支设计使得模型能够同时保持对参考主体外观的忠实度和对文本提示的响应能力。

### 姿态条件Transformer块与FeatureNeRF

姿态条件Transformer块（Figure 2c）是训练阶段学习三维几何表征的关键模块。其内部包含一个轻量级的 **FeatureNeRF** 模块，该模块从多张参考视图的特征图及其相机位姿出发，利用极线几何和体渲染技术，合成目标相机位姿 $\phi$ 下的对齐特征图：

$$X_y := \mathrm{FeatureNeRF}(\{(X_i, \pi_i)\}_{i=1}^{N}, c, \phi)$$

FeatureNeRF 在训练过程中与扩散模型的其他参数联合优化，学习到的隐式特征场编码了主体的三维几何与外观信息。这使得模型在生成新视角时，能够自然地保持主体的跨视角一致性。

### 视频扩散骨干网络与密集时空注意力

MVCustom 采用预训练的文本到视频扩散模型 **AnimateDiff** 作为骨干网络，其核心洞见在于将多视图生成重新定义为视频帧生成问题——视频中相邻帧的时间一致性可以被迁移为多视图间的空间一致性。

为此，方法引入了**密集时空注意力**（Dense Spatio-Temporal Attention, STT），将原始 AnimateDiff 中的 1D 时序注意力替换为全连接的时空注意力。消融实验（Figure 5b）证实，1D 时序注意力在跨视角特征替换时无法维持正确的语义平移，而密集时空注意力成功保持了空间流和几何对齐。训练过程中还采用了**渐进式注意力机制**（Figure 2b），逐步扩大空间注意力范围，进一步增强几何一致性。

视频去噪模型的形式化定义为：

$$D_{\theta}: (\tilde{\mathbf{x}}_{1:N}; \mathbf{Y}, \mathbf{c}, \phi_{1:N}) \mapsto \hat{\mathbf{x}}_{1:N}$$

即将噪声帧序列映射到去噪帧序列，并以参考图像、文本提示和相机位姿为条件。

### 推理阶段：显式几何约束注入

尽管训练后的模型能够生成主体一致的多视图图像，但仅依赖训练数据学习的隐式几何约束仍不足以保证周围环境（如背景、衣物细节）在所有视角下的一致性。为此，推理阶段引入两项核心技术：

1. **深度感知特征渲染（Depth-Aware Feature Rendering, DFR）**：选定一个锚点帧，利用外部深度估计器获取其深度图，结合该帧的 U-Net 特征图构建**锚点特征网格** $\mathcal{M}_a$（包含纹理 $\mathcal{F}_a$、顶点 $\mathcal{P}_a$ 和三角面片 $\mathcal{T}_a$）。对于其他目标视角 $\phi_n$，通过可微网格渲染器渲染出投影特征图 $\mathcal{F}_n^a$ 和可见性掩码 $M_n^a$：

   $$\mathcal{F}_n^a, M_n^a = \mathcal{R}(\mathcal{M}_a, \phi_n), \quad 1 \leq n \leq N, n \neq a$$

   随后按可见区域将渲染特征注入当前特征图：

   $$\hat{F}_n = M_n^a \odot F_n^a + (1 - M_n^a) \odot F_n, \quad 1 \le n \le N, n \neq a$$

   这一操作在 U-Net 的指定层中显式强制执行几何一致性约束。

2. **一致性感知潜在补全（Consistent-Aware Latent Completion, CLC）**：深度渲染后，新暴露的区域（即 $1 - M_n^a$ 对应的部分）需要通过向前扩散加噪、再从早期时间步 $\tau$ 开始去噪的随机扰动过程进行语义补全，确保这些区域在保持多样性的同时与整体场景语义一致。

### 数据流总览

整个 pipeline 的输入输出流可概括为：

- **训练输入**：多视图参考图像 + 相机位姿 + 文本提示
- **训练输出**：去噪后的多视图图像序列，同时优化 FeatureNeRF 和扩散模型参数
- **推理输入**：少量参考图像 + 文本提示 + 目标相机轨迹
- **推理过程**：先通过冻结的扩散骨干网络生成初始多视图序列，再通过 DFR 注入锚点帧几何约束，最后通过 CLC 补全新暴露区域
- **推理输出**：几何一致、身份保真、文本对齐的多视图定制图像

消融实验（Table A3）定量验证了推理策略的有效性：仅使用定制化微调时，COLMAP 重构点数仅为 36.13，相机姿态精度为 0.543；加入 DFR 后分别提升至 43.38 和 0.768；进一步加入 CLC 后达到 45.38 和 0.771，证明显式几何约束和潜在补全对多视图一致性的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_SGsxxbAjXH/figures/003_Figure_2.jpg]]
*Figure 2: Overview. (a) The overall training pipeline, depicting how camera pose conditioning operates with two branches, the main and multi-view. (b) Visualization of our progressive attention mechanism. We gradually broaden the spatial attention field, enhancing geometric consistency. (c) The detailed illustration of the pose-conditioned transformer block. FeatureNeRF and a projection layer are trained to produce a feature map, obtained by concatenating the main-branch and multi-view feature map*

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_SGsxxbAjXH/figures/009_Figure.jpg]]
*Figure: A1: Results with different Dream-Booth models. Since our method keeps spatial transformer layers of the video backbone architecture frozen, we can flexibly apply various publicly available Dream-Booth checkpoints. The figure shows images generated using two different checkpoints: RealisticVision1 and ToonYou2*

## 核心模块与公式推导

MVCustom 将多视图定制任务形式化为一个条件分布建模问题。给定包含 $N$ 张参考图像及其相机位姿的集合 $\mathbf{Y} = \{(\mathbf{I}_i, \pi_i)\}_{i=1}^N$、文本提示 $\mathbf{c}$ 和目标相机位姿序列 $\{\phi_m\}_{m=0}^M$，目标是建模条件分布：

$$p(\mathbf{x}_{0:M} \mid \mathbf{Y}, \mathbf{c}, \{\phi_m\}_{m=0}^{M})$$

其中 $\mathbf{x}_{0:M}$ 表示 $M+1$ 帧目标视角图像（Sec 3.1）。为实现这一目标，MVCustom 采用“训练阶段学习身份与几何表征 + 推理阶段注入显式几何约束”的分离式设计，其核心模块如下。

### 姿态条件 Transformer 块与 FeatureNeRF

训练阶段的核心是**姿态条件 Transformer 块**（Pose-conditioned Transformer Block），其内部包含一个名为 **FeatureNeRF** 的子模块。该模块以参考视图的 U-Net 中间特征图 $X_i$ 及其相机位姿 $\pi_i$ 为输入，通过极线几何约束和体渲染，合成目标位姿 $\phi$ 下的对齐特征图：

$$X_y := \mathrm{FeatureNeRF}(\{(X_i, \pi_i)\}_{i=1}^{N}, c, \phi)$$

FeatureNeRF 本质上是一个轻量特征场，学习从稀疏参考视图到任意目标视角的特征映射，而非直接生成 RGB 图像。训练时，姿态条件 Transformer 块以双分支结构运行：主分支处理当前帧特征，多视图分支通过 FeatureNeRF 生成跨视角对齐的特征图，二者拼接后经投影层融合，使模型学会在特征空间中保持主体几何一致性（Figure 2c, Sec 3.2）。

### 视频扩散骨干与密集时空注意力

MVCustom 的核心洞察是将多视图生成重新定义为**视频帧生成问题**。为此，方法采用预训练文本到视频扩散模型 **AnimateDiff** 作为骨干网络，其去噪模型可形式化为：

$$D_{\theta}: (\tilde{\mathbf{x}}_{1:N}; \mathbf{Y}, \mathbf{c}, \phi_{1:N}) \mapsto \hat{\mathbf{x}}_{1:N}$$

即将 $N$ 帧含噪输入 $\tilde{\mathbf{x}}_{1:N}$ 映射为去噪帧 $\hat{\mathbf{x}}_{1:N}$，整个过程以参考图像集 $\mathbf{Y}$、文本提示 $\mathbf{c}$ 和相机位姿序列 $\phi_{1:N}$ 为条件（Sec 3.3）。

关键改造在于将原始 AnimateDiff 的 **1D 时序注意力**替换为**密集时空注意力**（Dense Spatio-Temporal Attention, STT）。消融实验（Figure 5b）揭示了这一替换的必要性：1D 时序注意力在特征替换时仅沿时间轴逐位置独立操作，无法感知空间位移，导致特征替换后无法维持正确的语义平移；而 STT 同时建模时空维度的依赖关系，成功保持了跨帧的空间流和几何对齐。

### 深度感知特征渲染（DFR）

推理阶段的核心挑战在于：仅靠训练阶段学到的隐式几何约束，不足以在数据极度有限的定制化场景下保证周围场景的视角一致性。为此，MVCustom 引入**深度感知特征渲染**（Depth-aware Feature Rendering, DFR），在推理时显式注入几何约束。

具体而言，从生成的 $N$ 帧序列中选定一帧作为锚点帧 $a$，利用外部深度估计器获取其深度图，结合该帧的 U-Net 特征图构建**锚点特征网格** $\mathcal{M}_a$（包含纹理 $F_a$、顶点 $P_a$ 和三角面片 $T_a$）。然后，通过可微网格渲染器 $\mathcal{R}$ 将 $\mathcal{M}_a$ 投影到其他目标相机位姿 $\phi_n$，获得渲染特征图 $\mathcal{F}_n^a$ 和可见性掩码 $M_n^a$：

$$\mathcal{F}_n^a, M_n^a = \mathcal{R}(\mathcal{M}_a, \phi_n), \quad 1 \leq n \leq N, n \neq a$$

最后，按可见区域将渲染特征替换到当前帧的对应 U-Net 层特征 $F_n$ 中：

$$\hat{F}_n = M_n^a \odot F_n^a + (1 - M_n^a) \odot F_n, \quad 1 \le n \le N, n \neq a$$

这一操作强制不同视角下可见的相同三维区域共享一致的特征表示，从而显式地执行几何一致性约束（Sec 3.4, Figure 3a）。

### 一致性感知潜在补全（CLC）

DFR 渲染后，目标视角中原本被遮挡、在锚点网格中不可见的区域（即 $1 - M_n^a$ 对应的区域）仍需生成合理内容。**一致性感知潜在补全**（Consistent-aware Latent Completion, CLC）负责处理这些新暴露区域：对这些区域的潜在表示进行向前扩散加噪，然后在语义条件引导下去噪，从早期时间步 $\tau$（接近 $T$）迭代执行至 $T$，从而生成语义一致且多样化的补全内容，确保跨视角的空间连续性（Sec 3.4, Figure 3b）。

### 方法谱系与知识库定位

MVCustom 在多视图生成与定制化两条技术路线的交叉点上做出了关键创新。与直接对相机可控文本到多视图模型（如 **CameraCtrl**, He et al., 2024）应用 DreamBooth-LoRA 微调（**DreamBooth**, Ruiz et al., 2023）的朴素基线不同，MVCustom 将骨干网络从图像扩散模型替换为视频扩散模型，通过密集时空注意力将时间一致性迁移为多视图一致性。与仅关注主体保真度、不保证全景多视图一致性的视角感知定制化方法 **CustomDiffusion360**（Kumari et al., 2024）相比，MVCustom 通过 DFR 和 CLC 在推理阶段显式约束了周围环境的几何一致性。与单图到多视图方法（如 **SEVA**, Zhou et al., 2025）相比，MVCustom 利用多张参考视图构建 FeatureNeRF 特征场，有效缓解了跨视角伪影和身份丢失问题。

### 补充图表

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_SGsxxbAjXH/figures/004_Figure_3.jpg]]
*Figure 3: (a) Anchor feature mesh*

## 实验与分析

### 核心定量结果

MVCustom在CO3Dv2测试集上的多视图定制任务中，是唯一在相机姿态准确性、多视图一致性和定制化保真度三个维度上均取得领先的方法，而所有基线方法至少在一项上显著劣化（**Table 2**）。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_SGsxxbAjXH/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison on multi-view generation, customization, and inference cost. We highlight the best score in light red and the second-best in yellow*

**相机姿态精度（CPA↑）**：MVCustom达到 $0.735 \pm 0.10$，而直接对CameraCtrl应用DreamBooth-LoRA的基线（**CameraCtrl + DreamBooth-LoRA**, He et al., 2024; Ruiz et al., 2023）仅为 $0.074 \pm 0.05$，具备视角感知的定制化方法**CustomDiffusion360**（Kumari et al., 2024）则完全无法估计相机姿态（$0.000 \pm 0.00$）。这一悬殊差距表明，仅依靠定制化微调或视角感知机制无法在数据极度有限的场景下维持相机可控性，而MVCustom通过FeatureNeRF学习的三维特征场与姿态条件Transformer块成功将相机姿态信号编码进了生成过程。

**多视图一致性（DreamSim↓）**：MVCustom取得 $0.121 \pm 0.10$，显著优于单图到多视图基线**SEVA**（Zhou et al., 2025）的 $0.214 \pm 0.15$。在CLIP图像相似度指标上，MVCustom同样以 $0.933 \pm 0.048$ 超越SEVA的 $0.877 \pm 0.067$（**Table A1**）。这表明将多视图生成重新定义为视频帧生成，并利用密集时空注意力迁移时间一致性为多视图一致性的策略是有效的。

**主体身份保留（DreamSim↓）**：MVCustom的 $0.448 \pm 0.11$ 优于SEVA的 $0.504 \pm 0.12$，证明即使不牺牲几何一致性，定制化保真度仍可维持甚至提升。

### 消融研究

消融实验系统性地验证了推理阶段两个核心模块的因果贡献（**Table A3, Figure 5a**）：

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_SGsxxbAjXH/figures/013_Table.jpg]]
*Table: A3: Quantitative evaluation of inference strategies. “# of COLMAP recon” indicate the average number of reconstructed points from multi-view images with target camera poses by COLMAP. Best results are highlighted in bold; second-best in italic. Evaluations conducted on rotation-aware camera trajectory and translation trajectory*

1. **仅定制化微调（无DFR/CLC）**：周围环境在不同视角下保持静态，不随相机运动变化，COLMAP成功重构的3D点数仅为36.13，相机姿态精度为0.543。这揭示了单纯依赖训练数据学习几何的瓶颈——模型无法将定制化主体的视角变化推广到新生成的周围场景。

2. **加入深度感知特征渲染（DFR）**：COLMAP重构点数提升至43.38，相机姿态精度跃升至0.768。DFR通过从锚点帧的深度图和特征图构建特征网格，并根据目标相机姿态渲染特征图注入U-Net，以显式几何约束强制周围环境随视角正确平移。Figure 5a-ii直观展示了这一效果：建筑等背景元素随相机平移产生了正确的空间位移。

3. **进一步加入一致性潜在补全（CLC）**：COLMAP重构点数最终达到45.38。CLC对深度渲染后新暴露的区域进行向前加噪再降噪的随机扰动，生成语义一致且多样化的补全内容，增强了全局几何一致性。

**密集时空注意力（STT）的必要性**：Figure 5b的对比实验表明，当进行特征替换操作时，原始AnimateDiff的1D时序注意力无法保持空间一致性——特征图被简单地垂直复制，未能捕捉预期的平移语义流。而STT成功维持了空间流和几何对齐，这是特征替换策略得以生效的前提条件。

### 深度质量的影响

MVCustom的几何一致性依赖于外部深度估计器的质量。Figure 6展示了深度准确性对背景透视对齐的影响：准确的深度图产生与相机运动一致的背景透视，而错误的深度估计导致不真实的渲染结果。这一失败模式主要出现在反射或无纹理表面场景，但归因于深度估计器本身，而非MVCustom的方法设计。

### 推理成本权衡

MVCustom的推理成本（130.92秒/采样，19.29GB显存）高于基线方法（**Table 2**），主要开销来自额外的深度估计器和特征替换步骤。作者认为，在数据极度有限的定制化场景下，为显式几何一致性付出的额外计算开销是合理的权衡——其他方法要么完全丧失相机可控性，要么产生严重的跨视角伪影和身份丢失，无法同时满足多视图定制的三个核心要求。

### 补充图表

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_SGsxxbAjXH/figures/002_Table_1.jpg]]
*Table 1: Comparison of existing tasks and representative methods. Fidelity refers to preserving object identity from reference images and alignment with textual prompts in customization. Holistic denotes whether both subjects and the surroundings described in a prompt are synthesized. S.MV evaluates whether subjects remain consistent across different viewpoints. H.MV consistency refers to whether both subjects and their surroundings are holistically consistent across viewpoints. MV stands for multi-view*

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_SGsxxbAjXH/figures/010_Table.jpg]]
*Table: A1: Additional quantitative evaluation of multi-view consistency. Our method achieves the highest multi-view consistency across all three image similarity metrics, demonstrating that the generated images exhibit strong alignment and similarity with each other across different viewpoints*

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_SGsxxbAjXH/figures/008_Figure_6.jpg]]
*Figure 6: Comparison of background perspective alignment in generated images depending on the quality of estimated depth*

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_SGsxxbAjXH/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results. The light blue boxes indicate the multi-view training dataset for the target concept, while the light pink boxes illustrate the inference phase, where results are conditioned on new text and target camera poses*

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_SGsxxbAjXH/figures/007_Figure_5.jpg]]
*Figure 5: Results of ablation studies. (a) Stepwise effect of applying depth-aware feature rendering (DFR) and consistent-aware latent completion under x-translation camera pose. (b) Impact of temporal attention on feature replacement. (i) Feature replacement vertically copies the feature map from frame 1 to frame 2. Our method successfully enforces spatial flow, whereas 1D temporal attention fails to capture the intended translation*

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_SGsxxbAjXH/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between MVCustom and existing approaches extended to multi-view customization. The light blue box shows the reference multi-view images and corresponding camera poses of a customized object. The ’X’ marks indicate regions inconsistent with either the reference object’s appearance or across views, while ’O’ marks indicate well-maintained consistency. Our approach clearly outperforms existing methods by achieving accurate viewpoint alignment and robust multi-view consistency for both the customized object and novel surroundings generated from diverse textual prompts*

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_SGsxxbAjXH/figures/011_Figure.jpg]]
*Figure: A2: Results on ablation study*

## 方法谱系与知识库定位

### 任务定位与基线谱系

MVCustom 瞄准的是**多视图定制生成**这一新兴任务，其核心矛盾在于：仅提供少量参考图像时，需同时满足主体身份保真度、多视角几何一致性以及周围场景的全景一致生成。Table 1 系统对比了现有任务在此四维能力上的覆盖情况，MVCustom 是首个在所有维度上均能胜任的方法。

具体而言，现有基线可归为三类，各自存在结构性缺陷：

- **单图到多视图生成**（如 **SEVA**，Zhou et al., 2025）：将定制图像作为输入，通过图像条件多视图模型生成新视角。此类方法缺乏对主体身份的显式建模，随着视角偏离输入图像，主体外观和周围场景均出现严重伪影和身份丢失（Figure 4 定性证实）。

- **文本条件相机可控模型 + 定制化微调**（如 **CameraCtrl** + **DreamBooth-LoRA**，He et al., 2024；Ruiz et al., 2023）：对预训练文本到多视图模型直接应用定制化微调。问题在于，定制化微调破坏了原模型的相机可控性，导致生成的视角与目标相机姿态严重偏离（Table 2 中相机姿态精度 CPA 极低）。

- **视角感知定制化方法**（如 **CustomDiffusion360**，Kumari et al., 2024）：虽能保留主体身份并反映文本提示，但仅针对主体本身，不保证周围场景随视角变化的一致性。Table 2 显示其相机姿态精度为 0.000，表明完全丧失了多视图几何控制能力。

MVCustom 的关键突破在于将多视图生成**重新定义为视频帧生成问题**，利用预训练视频扩散模型（AnimateDiff）中密集时空注意力隐含的时间一致性，将其迁移为多视图一致性。这一范式转换使得在训练数据极度有限的定制化场景下，仍能通过推理阶段的显式几何约束实现多视图一致生成。

### 核心方法论贡献

MVCustom 的方法论贡献可分解为三个相互协同的层面：

**（1）姿态条件特征场学习。** 训练阶段引入姿态条件 Transformer 块（含 FeatureNeRF），从多视角参考图像及其相机姿态中学习物体的三维特征场。与直接将相机姿态注入交叉注意力的方案不同，FeatureNeRF 通过极线几何和体渲染合成目标位姿下的对齐特征图，为后续推理阶段的几何约束提供了基础表征（Figure 2c）。

**（2）视频扩散骨干与密集时空注意力。** 将 AnimateDiff 的 1D 时序注意替换为密集时空注意（STT），这是方法有效性的必要条件。消融实验（Figure 5b）揭示了一个关键因果机制：当进行跨视角特征替换时，1D 时序注意无法维持空间一致性——特征图在帧间仅被垂直复制，无法反映相机运动带来的语义平移；而 STT 成功保持了空间流和几何对齐，使特征替换能够正确传递相机运动信息。

**（3）推理阶段显式几何约束。** 这是 MVCustom 区别于所有基线方法的核心创新。深度感知特征渲染（DFR）利用外部深度估计器从锚点帧构建特征网格，并根据目标相机姿态渲染特征图注入 U-Net 指定层，显式强制执行几何一致性。一致性潜在补全（CLC）则对深度渲染后新暴露的区域进行随机扰动再降噪，确保补全内容语义一致且多样化。

消融实验（Table A3）定量证实了这一设计的有效性：仅定制化微调时 COLMAP 重构点数仅 36.13，加入 DFR 后提升至 43.38，进一步加入 CLC 后达到 45.38；相机姿态精度则从 0.543 经 DFR 提升至 0.768，CLC 进一步推至 0.771。

### 适用边界与局限

MVCustom 的适用边界受以下因素制约：

**主体姿态不可变性。** FeatureNeRF 学习的是固定的规范姿态，且其辐射场未将文本作为条件输入。因此，MVCustom 无法根据文本提示改变定制化物体的内在姿态（如“从坐到站”），仅能改变相机视角和周围场景。这是一个结构性的能力边界，源于训练阶段的设计选择。

**深度估计依赖性。** DFR 依赖外部深度估计器的准确性。当处理反射表面或无纹理区域时，估计的深度图可能不准确，直接导致特征网格几何错误，进而破坏多视图一致性。Figure 6 展示了深度质量对背景透视对齐的显著影响：准确深度产生一致的背景，错误深度则导致不真实的结果。作者明确指出这归因于深度估计器而非方法本身，但这一依赖性构成了实际部署中的脆弱环节。

**推理计算成本。** MVCustom 的推理成本（130.92 秒/采样，19.29GB 显存）显著高于基线方法，主要来自额外的深度估计器和特征替换步骤。在数据极度有限的定制化场景下，这一计算开销被视为显式几何一致性的合理权衡，但限制了实时或资源受限场景的适用性。

### 开放问题与未来方向

**动态姿态控制。** 能否通过优化动态神经场，或在冻结的 FeatureNeRF 上应用分数蒸馏采样（Score Distillation Sampling），实现在推理时根据文本改变物体姿态？这需要将文本条件引入特征场学习，并处理动态几何建模的挑战。

**深度估计鲁棒性。** 如何进一步提升深度估计的鲁棒性，或探索不依赖于显式深度图的替代几何约束方案？可能的路径包括：引入多视图立体匹配的隐式几何先验、利用扩散模型自身的几何感知能力进行自监督深度精化，或采用神经辐射场风格的隐式几何表示替代显式特征网格。

**更广泛的定制化场景。** 当前方法在 CO3Dv2 数据集上验证，主要针对刚性物体。扩展到可变形物体、复杂光照条件或更大规模场景的多视图定制，需要重新审视特征场表示的表达能力和泛化边界。

## 原文 PDF

![[paperPDFs/ICLR_2026/MVCustom_Multi_View_Customized_Diffusion_via_Geometric_Latent_Rendering_and_Comp_5fcfc95fff65.pdf]]