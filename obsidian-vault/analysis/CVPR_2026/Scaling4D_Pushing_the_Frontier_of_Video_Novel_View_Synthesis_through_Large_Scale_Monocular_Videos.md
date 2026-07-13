---
title: "Scaling4D: Pushing the Frontier of Video Novel View Synthesis through Large-Scale Monocular Videos"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Scaling4D_Pushing_the_Frontier_of_Video_Novel_View_Synthesis_through_Large_Scale_Monocular_Videos.pdf
project_link: "https://rainbowrui.github.io/scaling4d/"
code_link: null
aliases:
- Scaling4D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将 VNVS 任务重新定义为通用的“对应关系引导生成”（correspondence-guided generation）范式，利用光流（optical flow）在任意单目视频中提取像素对应关系作为控制信号，从而让训练和推理共享统一的对应关系空间。
primary_logic: 通过将渲染过程等价转换为二维像素对应关系，使得大规模单目野生视频可以通过光流模型生成可靠的训练信号；同时，在推理阶段使用深度图计算对应关系，利用训练中光流噪声的自监督鲁棒性来桥接训练-推理差距。
claims:
- 修复范式存在本质缺陷，无法正确处理视角变化导致的遮挡区域。
- 通过光流建立对应关系，使得在任意单目视频上进行自监督训练成为可能。
- Panda-70M 单视角测试集 上 FID = 62.83
- Panda-70M 单视角测试集 上 FVD = 411.17
---

# Scaling4D: Pushing the Frontier of Video Novel View Synthesis through Large-Scale Monocular Videos

> [!tip] 核心洞察
> 通过将渲染过程等价转换为二维像素对应关系，使得大规模单目野生视频可以通过光流模型生成可靠的训练信号；同时，在推理阶段使用深度图计算对应关系，利用训练中光流噪声的自监督鲁棒性来桥接训练-推理差距。

| 字段 | 内容 |
|------|------|
| 中文题名 | Scaling4D：通过大规模单目视频推进视频新视角合成的前沿 |
| 英文题名 | Scaling4D: Pushing the Frontier of Video Novel View Synthesis through Large-Scale Monocular Videos |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Cai_Scaling4D_Pushing_the_Frontier_of_Video_Novel_View_Synthesis_through_CVPR_2026_paper.html) · [Project](https://rainbowrui.github.io/scaling4d/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Scaling4D |
| Dataset | Panda-70M 单视角测试集, 多视角 iPhone 测试集 |

> [!tip] 效果简介
> - Panda-70M 单视角测试集 上，FID 62.83 vs 最佳基线(约82.31) (显著提升)；FVD 411.17 vs 最佳基线(约632.95) (显著提升)；CLIP-T 27.79 vs 最佳基线(约25.42) (提升)。
> - 多视角 iPhone 测试集 上，PSNR 14.85 vs 所有对比方法 (最佳)；SSIM 0.336 vs 所有对比方法 (最佳)；LPIPS 0.468 vs 所有对比方法 (最佳)。

## 概要

**问题与瓶颈**：视频新视角合成（Video Novel View Synthesis, VNVS）旨在从一段单目视频出发，生成任意新相机轨迹下的连贯视频。现有方法普遍将 VNVS 退化为基于点云渲染的修复（inpainting）任务——即先渲染一张粗糙的目标视角图像与掩码，再由生成模型填补缺失区域。这一范式存在根本性缺陷：修复模型无法正确处理因视角变化而暴露的遮挡区域，倾向于用背景像素错误填充本应出现的新内容（如 Figure 2 所示，人物背面被背景替代）。更关键的是，此类方法因缺乏大规模多视角视频数据，训练与推理之间存在严重的数据分布不一致，导致视觉伪影频发、泛化能力受限。

**核心思路**：本文提出 **Scaling4D**，将 VNVS 重新定义为通用的**对应关系引导生成**（correspondence-guided generation）任务。其核心洞察是：渲染过程在数学上等价于在二维像素平面建立源视角与目标视角之间的稠密对应关系 $\mathbf{C}^{r} \Longleftrightarrow \Phi \circ \mathbf{T}^{r} \circ \Phi^{-1}$。由此，训练阶段可利用光流模型（如 RAFT）在任意单目野生视频中提取帧间像素对应关系作为控制信号，实现大规模自监督训练；推理阶段则通过单目深度估计与相机位姿计算对应关系，利用训练中光流噪声带来的自监督鲁棒性来桥接训练-推理差距。

**方法定位**：Scaling4D 在预训练视频生成基础模型（MMDiT 架构，配合 3D VAE 与 LLM 文本编码器）之上，插入两个可训练模块——**Correspondence Projector** 将 5 通道控制信号（源视频、对应关系、扭曲视频、掩码）编码为控制令牌，**VNVS Block** 通过联合空间注意力机制将控制令牌注入视频特征。训练数据由两部分构成：大规模单目真实视频（通过光流提取对应关系）与合成多视角数据（提供精确几何监督）。

**主要结果**：在 Panda-70M 单视角测试集上，Scaling4D 的 FID 达到 62.83（最佳基线约 82.31），FVD 降至 411.17（最佳基线约 632.95），CLIP-T 提升至 27.79；在多视角 iPhone 测试集上，PSNR / SSIM / LPIPS 均取得最优。消融实验证实，大规模真实单目数据对视觉质量至关重要（仅用合成数据训练时 FVD 从 411.17 恶化至 472.62）。可扩展性分析显示，视觉质量指标（FID、FVD、CLIP-V）随数据量增加呈持续上升趋势，而姿态精度指标（RotError、TransError）在数据量达到 100k 后趋于饱和，提示进一步突破需解决光流与深度估计的固有精度瓶颈。

### 问题背景

视频新视角合成（Video Novel View Synthesis, VNVS）旨在给定一段单目源视频和一组目标相机位姿，生成从新视角观察到的视频内容。该任务在自由视点视频、3D 内容创作、虚拟现实等领域具有广泛应用前景。其核心挑战在于：仅凭单一视角的二维观测，模型需要推断出场景的三维几何结构并补全被遮挡区域的内容，这本质上是一个欠定问题。

### 现有方法的瓶颈：修复范式的根本缺陷

当前主流方法普遍将 VNVS 退化为一个基于点云渲染的修复（inpainting）任务。具体而言，这类方法首先利用深度估计将源视频帧反投影为三维点云，再将点云渲染到目标视角，得到一张带有空洞的渲染图像 $\mathbf{I}^r$ 和对应的掩码 $\mathbf{M}^r$；随后，一个条件生成模型以 $(\mathbf{I}^r, \mathbf{M}^r)$ 为控制信号，对空洞区域进行填充。**GEN3C**（Ren et al., CVPR 2025）、**TrajectoryCrafter**（Yu et al., ICCV 2025）等方法均遵循这一范式。

然而，修复范式存在一个本质性的缺陷：它无法正确处理视角变化导致的遮挡区域。如 Figure 2 所示，当新视角要求展示人物的背部时，修复模型错误地将其填充为背景像素——因为渲染图像 $\mathbf{I}^r$ 在该区域本身就是空洞，模型缺乏任何关于“背部应该出现什么”的几何线索。这一问题并非模型容量不足所致，而是任务定义本身的局限：修复任务将 VNVS 简化为“填充渲染图像中的空洞”，却忽略了新视角合成需要的是“生成从未被观察到的新内容”。

### 训练-推理分布不一致

修复范式的另一个深层问题在于训练与推理之间存在严重的数据分布不一致。在训练阶段，现有方法通常依赖合成多视角数据（如 Objaverse 渲染数据集），其中渲染图像 $\mathbf{I}^r$ 和目标图像 $\mathbf{I}^t$ 之间存在精确的像素对应关系。然而在推理阶段，由于单目深度估计的误差，渲染图像的质量和精度远低于训练数据，导致模型在推理时产生视觉伪影和泛化性退化。这种“训练-推理鸿沟”是制约 VNVS 方法走向实用化的关键瓶颈。

### 核心动机：从修复到对应关系引导的生成

本文的核心动机源于一个关键洞察：渲染过程在数学上等价于二维像素对应关系。具体而言，将源帧通过逆透视投影 $\Phi^{-1}$ 反投影为点云、再经刚体变换 $\mathbf{T}^r$ 和透视投影 $\Phi$ 渲染到目标视角的整个过程，可以等价地表示为一个二维像素对应关系场 $\mathbf{C}^r$：

$$\mathbf{C}^{r} \Longleftrightarrow \Phi \circ \mathbf{T}^{r} \circ \Phi^{-1}$$

这一等价变换意味着，VNVS 任务可以被重新定义为“对应关系引导的生成”任务——模型不再依赖渲染图像的质量，而是直接以像素对应关系作为几何控制信号。更重要的是，在训练阶段，对于任意野生单目视频，可以通过光流模型（如 RAFT）提取帧间的像素对应关系，从而构建自监督训练信号。这使得大规模单目视频数据可以被用于训练，从根本上缓解了训练数据稀缺和分布不一致的问题。

基于以上分析，本文提出 Scaling4D，将 VNVS 重新定义为通用的对应关系引导生成任务，通过统一的对应关系空间桥接训练与推理，并利用大规模单目视频实现可扩展训练，从而显著提升合成结果的视觉质量和鲁棒性。

## 核心方法与创新机理

Scaling4D 的核心创新并非在网络结构上进行边际修补，而是对视频新视角合成（VNVS）的任务范式进行了根本性的重构。文章将这一升级凝练为四个关键的“变更槽位”（changed slots），它们共同构成了从“修复范式”到“对应关系引导生成范式”的跃迁。

### 1. 任务范式：从修复到对应关系引导生成

现有方法（如 **TrajectoryCrafter** (Yu et al., ICCV 2025) 等）普遍将 VNVS 退化为一个基于点云渲染的修复（inpainting）任务：先通过深度估计和相机位姿将源视图点云投影到新视角，得到一个带有空洞的粗糙渲染图，再交由生成模型进行填充。这一范式的根本缺陷在于，修复任务无法正确处理视角变化导致的遮挡区域——新视角下本应显露的物体背面，往往被错误地填充为背景像素（见 Figure 2）。这导致训练与推理之间存在严重的数据分布不一致，产生视觉伪影且泛化性差。

Scaling4D 将 VNVS 重新定义为通用的“对应关系引导生成”（correspondence-guided generation）任务。其核心洞察在于：渲染过程的本质并非“生成像素”，而是“建立二维像素对应关系”。通过将逆透视投影、刚体变换和透视投影的组合操作等价转换为二维对应关系 $C^{r}$，模型的控制信号从“待修复的图像”转变为“像素级的空间映射”：
$$
\mathbf{C}^{r} \Longleftrightarrow \Phi \circ \mathbf{T}^{r} \circ \Phi^{-1}
$$
这一等价变换使得训练和推理能够共享统一的对应关系空间，从根本上弥合了此前范式中存在的数据分布鸿沟。

### 2. 训练数据：解锁大规模单目视频

范式升级的直接红利是训练数据来源的质变。在修复范式下，训练需要精确的相机位姿和多视角数据，这严重限制了可用的数据规模——研究者不得不依赖合成数据或昂贵的多视角采集设备。

Scaling4D 利用对应关系范式，使得任意单目野生视频都可以成为训练样本。对于任意一段单目视频，只需任意选取两个片段作为源视频 $I^{s}$ 和目标视频 $I^{t}$，然后通过现成的光流模型（如 RAFT）即可提取它们之间的像素对应关系 $C^{r}$。这一对应关系恰好充当了训练所需的控制信号，使得大规模自监督训练成为可能。消融实验（Table 3）直接验证了这一创新的价值：仅使用合成数据训练的变体（Ours w/o RealData）在 FVD 指标上劣化至 472.62，证明大规模真实单目数据对视觉质量具有决定性贡献。

### 3. 控制信号：从图像掩码到多通道对应关系张量

控制信号的形态也随之升级。基线方法通常仅输入渲染图像和掩码 $(I^{r}, M^{r})$，信息维度单一。Scaling4D 将控制信号扩展为一个 9 通道张量 $(I^{s}, C^{r}, I^{r}, M^{r})$，同时编码了源视频、像素对应关系、扭曲视频和有效区域掩码。这一设计使得生成模型能够同时感知“从哪里来”（源视频）、“如何映射”（对应关系）、“初步结果”（扭曲视频）和“可信区域”（掩码），从而在生成过程中获得更丰富的几何先验。

### 4. 网络结构：可插拔的控制注入模块

在模型架构层面，Scaling4D 并未重新训练整个生成基础模型，而是在预训练的 MMDiT 基础模型各层之间插入了两个轻量级可训练模块：**Correspondence Projector** 和 **VNVS Block**。

Correspondence Projector 通过一系列卷积层和 Patchify 层将 9 通道控制信号编码为与视频表征形状匹配的控制令牌 $F_{cor}$。VNVS Block 则通过联合空间注意力机制实现控制令牌与视频特征的交互，其核心操作为查询、键、值投影的求和：
$$
\mathbf{F}_{\mathrm{vid}} \leftarrow \mathbf{F}_{\mathrm{vid}} + \mathrm{Attn}( \mathbf{Q}_{\mathrm{vid}} + \mathbf{Q}_{\mathrm{cor}}, \mathbf{K}_{\mathrm{vid}} + \mathbf{K}_{\mathrm{cor}}, \mathbf{V}_{\mathrm{vid}} + \mathbf{V}_{\mathrm{cor}} )
$$
值得注意的是，VNVS Block 有意省略了标准 Transformer 块中的前馈网络（FFN）层，仅保留注意力操作，以最小化对预训练基础模型原有行为的扰动，同时高效地将对应关系控制信息注入生成过程。

### 5. 训练-推理差距的桥接机制

一个隐含但至关重要的创新在于训练与推理之间对应关系来源的桥接策略。训练阶段使用光流模型提取对应关系 $C^{r}_{\mathrm{flow}}$，而推理阶段则使用深度图和相机位姿计算对应关系 $C^{r}_{\mathrm{depth}}$。两者虽然在静态场景下高度一致（见 Figure 8），但光流对应关系天然包含更多噪声和不规则性。文章指出，正是这种“以粗糙训练对抗精细推理”的策略，迫使模型学习到抗噪声的映射能力，从而增强了推理阶段的鲁棒性——这是一个优雅的自监督正则化设计，而非简单的工程妥协。

Scaling4D 的整体框架围绕“对应关系引导生成”这一核心范式构建，将视频新视角合成（VNVS）从传统的点云渲染+修复（inpainting）范式升级为统一的像素对应关系控制生成任务。整个 pipeline 由三个关键阶段串联而成：**对应关系提取 → 控制信号构建 → 条件视频生成**。

### 范式升级的理论基础

传统 VNVS 方法遵循“渲染-修复”范式：先将源视频的 3D 点云渲染到目标视角得到粗糙图像 $I^r$ 和掩码 $M^r$，再通过生成模型修复空洞和遮挡区域。然而，修复任务本质上无法处理视角变化引入的新内容（如人物背面），这造成了训练与推理之间的数据分布不一致，导致视觉伪影和泛化性差。

Scaling4D 的核心洞察在于：渲染过程在数学上等价于二维像素对应关系。具体而言，将源帧的 RGB-D 数据通过相机内参 $K$ 反投影为 3D 点云 $\mathcal{P}$，再经目标相机位姿 $T^r$ 变换后投影回图像平面，这一组合操作等价于一个二维对应关系 $C^r$：

$$\mathbf{C}^{r} \Longleftrightarrow \Phi \circ \mathbf{T}^{r} \circ \Phi^{-1}$$

这一等价变换（Eq. 4）是范式升级的理论基石。它将 VNVS 任务重新定义为：给定源视频 $I^s$ 和对应关系 $C^r$，生成目标视角视频 $I^*$，并与真实目标帧 $I^t$ 计算损失：

$$\mathbf{I}^{s} \xrightarrow{\mathbf{C}^{r}} \mathbf{I}^{r} \xrightarrow{G_{\theta}} \mathbf{I}^{*} \Leftarrow \mathbf{I}^{t}$$

### 数据流与模块关系

整个框架的数据流如图 1 所示，输入为单目源视频和新视角相机轨迹，输出为对应的新视角视频。各模块的职责与交互关系如下：

**1. 对应关系提取模块（上游）**

该模块负责从输入数据中提取像素对应关系 $C^r$，是连接训练与推理的关键桥梁。根据场景不同，采用两种策略：
- **训练阶段**：从大规模单目野生视频中任意选取两个片段作为 $I^s$ 和 $I^t$，通过光流模型（如 RAFT）直接估计二者之间的对应关系 $C^r_{\text{flow}}$。
- **推理阶段**：对源视频估计单目深度图 $D^s$，通过逆透视投影生成点云 $\mathcal{P}$，再根据目标相机位姿 $T^r$ 和相机内参 $K$ 进行透视投影，获得深度引导的对应关系 $C^r_{\text{depth}}$。

**2. 控制信号构建模块**

将源视频 $I^s$、对应关系 $C^r$、渲染图像 $I^r$ 和渲染掩码 $M^r$ 拼接为 9 通道的控制张量 $(I^s, C^r, I^r, M^r) \in \mathbb{R}^{n \times 9 \times h \times w}$，作为后续生成模型的控制输入。其中 $I^r$ 和 $M^r$ 由点云渲染获得，$n$ 为视频帧数。

**3. Correspondence Projector（可训练模块）**

该模块负责将 9 通道控制张量编码为与视频表征形状匹配的控制令牌 $F_{\text{cor}}$。其结构由一系列卷积层后接一个 patchify 层组成，将原始像素空间的控制信号映射到潜在空间的控制令牌序列。

**4. VNVS Block（可训练模块）**

VNVS Block 是控制信息注入生成过程的核心组件。它被插入到预训练基础模型（MMDiT）的各层之间，通过联合空间注意力机制实现视频特征与控制令牌的跨模态交互：

$$\mathbf{F}_{\mathrm{vid}} \leftarrow \mathbf{F}_{\mathrm{vid}} + \mathrm{Attn}(\mathbf{Q}_{\mathrm{vid}} + \mathbf{Q}_{\mathrm{cor}}, \mathbf{K}_{\mathrm{vid}} + \mathbf{K}_{\mathrm{cor}}, \mathbf{V}_{\mathrm{vid}} + \mathbf{V}_{\mathrm{cor}})$$

其中 $\mathbf{Q}_{\mathrm{vid}}, \mathbf{K}_{\mathrm{vid}}, \mathbf{V}_{\mathrm{vid}}$ 为视频特征的查询、键、值投影，$\mathbf{Q}_{\mathrm{cor}}, \mathbf{K}_{\mathrm{cor}}, \mathbf{V}_{\mathrm{cor}}$ 为控制令牌的对应投影。通过将二者在注意力计算中进行求和融合，控制信息被无缝注入视频生成过程。值得注意的是，VNVS Block 省略了标准 Transformer 中的前馈网络（FFN）层，仅保留注意力机制以降低参数量。

**5. MMDiT 基础模型（冻结参数）**

框架采用预训练的 MMDiT 模型作为生成主干。该模型使用 3D VAE 将视频编码到潜在空间，并利用大语言模型（LLM）编码文本输入。在整个训练过程中，基础模型的参数保持冻结，仅训练 Correspondence Projector 和 VNVS Block 两部分。

### 训练-推理差距桥接机制

训练阶段使用光流对应关系 $C^r_{\text{flow}}$，推理阶段使用深度对应关系 $C^r_{\text{depth}}$，二者之间存在天然的精度差异——光流对应关系通常比深度对应关系更粗糙、噪声更大。然而，这种差异反而成为一种自监督正则化：训练时模型被迫学习对噪声鲁棒的映射能力，从而在推理阶段面对更平滑的深度对应关系时表现出更强的泛化性。这一机制是 Scaling4D 能够利用大规模单目视频进行有效训练的核心原因。

![[assets/figures/papers/paper_list_l2587_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_Scaling4D_Pushing/figures/001_Figure_1.jpg]]
*Figure 1: We introduce Scaling4D, a framework for Video Novel View Synthesis (VNVS). Given a monocular source video (first row) and novel poses (second row), Scaling4D generates the novel view video (third row). By reformulating VNVS as a correspondence-guided generation task, our approach bridges the training-inference gap present in previous methods and enables scalable training on large-scale monocular videos, substantially improving the visual quality and robustness of the synthesized results*

### 3.1 范式升级的理论基础：对应关系等价变换

Scaling4D 的核心洞察在于揭示二维像素对应关系与三维几何投影之间的数学等价性。给定源帧的 RGB-D 数据 $[\mathbf{I}_i^s, \mathbf{D}_i^s]$ 和相机内参 $\mathbf{K}$，首先通过逆透视投影将二维像素提升为三维点云：

$$
\mathcal{P}_i = \Phi^{-1}([\mathbf{I}_i^s, \mathbf{D}_i^s], \mathbf{K}), \quad \forall i \in [1, n]
$$

其中 $\Phi^{-1}$ 表示逆投影操作，$\mathcal{P}_i$ 为具有空间坐标和颜色的三维点云。随后，根据目标相机位姿 $\mathbf{T}_i^r$ 对点云进行刚体变换，再通过透视投影 $\Phi$ 渲染到目标视角：

$$
\mathbf{I}_i^r = \Phi(\mathbf{T}_i^r \mathcal{P}_i, \mathbf{K})
$$

上述“逆投影—刚体变换—投影”的复合操作，本质上在二维图像平面上定义了一个像素对应关系 $\mathbf{C}^r$。这一等价关系可形式化表述为：

$$
\mathbf{C}^r \Longleftrightarrow \Phi \circ \mathbf{T}^r \circ \Phi^{-1}
$$

该等价变换（Eq. 4）是 Scaling4D 范式升级的理论基石：它将原本依赖三维渲染管线的几何控制信号，转化为纯粹的二维像素对应关系，从而为利用大规模单目视频进行自监督训练打开了通道。

### 3.2 升级后的训练范式：对应关系引导生成

基于上述等价性，Scaling4D 将 VNVS 任务重新定义为通用的对应关系引导生成范式。训练流程可概括为：

$$
\mathbf{I}^s \xrightarrow{\mathbf{C}^r} \mathbf{I}^r \xrightarrow{G_\theta} \mathbf{I}^* \Leftarrow \mathbf{I}^t
$$

具体而言，利用对应关系 $\mathbf{C}^r$ 将源视频 $\mathbf{I}^s$ 扭曲（warp）为目标视角的渲染图像 $\mathbf{I}^r$，然后通过生成模型 $G_\theta$ 对 $\mathbf{I}^r$ 进行细化，生成最终结果 $\mathbf{I}^*$，并与真实目标帧 $\mathbf{I}^t$ 计算流匹配损失。在训练阶段，$\mathbf{C}^r$ 可通过在任意单目野生视频的两个片段之间应用光流模型（如 RAFT）直接获取，无需真实相机位姿或多视角标注。这一设计使得训练和推理共享统一的对应关系空间，从根本上消除了以往修复范式中训练-推理分布不一致的瓶颈。

### 3.3 控制信号编码：Correspondence Projector

在推理阶段，控制信号被组织为一个 9 通道张量 $(\mathbf{I}^s, \mathbf{C}^r, \mathbf{I}^r, \mathbf{M}^r) \in \mathbb{R}^{n \times 9 \times h \times w}$，其中 $\mathbf{I}^s$ 为源视频，$\mathbf{C}^r$ 为深度图计算得到的对应关系，$\mathbf{I}^r$ 为渲染图像，$\mathbf{M}^r$ 为有效区域掩码。Correspondence Projector 负责将该控制信号编码为与视频表征形状匹配的控制令牌 $\mathbf{F}_{\text{cor}}$。其结构由一系列卷积层后接一个 patchifying 层组成，将空间维度的控制信息压缩为与 MMDiT 基础模型兼容的令牌序列。

### 3.4 控制信息注入：VNVS Block

VNVS Block 是 Scaling4D 网络结构中的核心可训练模块，插入在预训练 MMDiT 基础模型的各层之间。与标准 Transformer 块不同，VNVS Block 省略了前馈网络（FFN）层，仅通过联合空间注意力机制实现控制令牌与视频特征的交融。其注意力计算形式为：

$$
\mathbf{F}_{\text{vid}} \leftarrow \mathbf{F}_{\text{vid}} + \text{Attn}(\mathbf{Q}_{\text{vid}} + \mathbf{Q}_{\text{cor}}, \mathbf{K}_{\text{vid}} + \mathbf{K}_{\text{cor}}, \mathbf{V}_{\text{vid}} + \mathbf{V}_{\text{cor}})
$$

其中 $\mathbf{Q}_{\text{vid}}, \mathbf{K}_{\text{vid}}, \mathbf{V}_{\text{vid}}$ 为视频特征的查询、键、值投影，$\mathbf{Q}_{\text{cor}}, \mathbf{K}_{\text{cor}}, \mathbf{V}_{\text{cor}}$ 为控制令牌的对应投影。通过对两组投影直接求和，VNVS Block 在单个注意力操作中实现了视频内容与控制信号的跨模态交互，将几何对应关系无缝注入生成过程，同时保持基础模型的预训练权重冻结，仅训练 Correspondence Projector 和 VNVS Block 的新增参数。

![[assets/figures/papers/paper_list_l2587_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_Scaling4D_Pushing/figures/004_Figure_4.jpg]]
*Figure 4: Overview of our synthetic data pipeline, including compositional scene layouts, procedural character generation, obstacle-aware camera trajectories, and storage of RGB images, depth maps, and camera matrices*

## 实验与关键发现

### 核心实验设置

Scaling4D 采用预训练的视频生成基础模型 MMDiT 作为骨干网络，该模型使用 3D VAE 将视频编码至潜在空间，并通过 LLM 对文本输入进行编码。所有实验均在统一的 49 帧、480×480 分辨率下进行训练与推理。训练使用 AdamW 优化器，学习率为 $4 \times 10^{-5}$。推理阶段，所有对比方法均使用相同的单目深度估计器 GeometryCrafter 以确保公平性。可训练模块仅包含 Correspondence Projector 和 VNVS Block，二者被插入到预训练基础模型的各层之间，通过联合空间注意力机制实现控制令牌与视频特征的交互。

### 单视角数据集上的主结果

在 Panda-70M 单视角测试集上，Scaling4D 在所有评估指标上均取得了最优结果，显著超越现有方法。定量结果如表 1 所示（详见 **Figure 6 / Table 1**）：FID 达到 **62.83**（最佳基线约 82.31），FVD 达到 **411.17**（最佳基线约 632.95），CLIP-T 达到 **27.79**（最佳基线约 25.42）。FVD 的显著下降表明生成视频的时序一致性和视觉质量获得了实质性提升。

![[assets/figures/papers/paper_list_l2587_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_Scaling4D_Pushing/figures/007_Figure_6.jpg]]
*Figure 6: The qualitative results on the single-view dataset. From left to right, we display target camera trajectory, input images, results of ours, GEN3C [39], TrajectoryCrafter [52], Voyager [21] and ReCamMaster-Wan [2], respectively*

定性对比（**Figure 6**）进一步揭示了方法间的差异。以 **GEN3C**（Ren et al., CVPR 2025）为代表的基于 3D 信息的方法在相机运动幅度较大时，渲染的点云图像会出现严重的空洞和撕裂伪影；**TrajectoryCrafter**（Yu et al., ICCV 2025）等基于修复范式的方法则倾向于用背景像素错误填充本应呈现新内容的遮挡区域，这与 Figure 2 中揭示的修复范式本质缺陷一致。相比之下，Scaling4D 通过对应关系引导生成，能够正确推理并生成遮挡区域的新内容。

### 多视角数据集上的主结果

在具有真实多视角图像监督的 iPhone 测试集上，Scaling4D 同样展现出清晰的定量优势（**Table 2**）：PSNR 达到 **14.85**，SSIM 达到 **0.336**，LPIPS 达到 **0.468**，三项指标均优于所有对比方法。这验证了对应关系引导范式不仅在视觉质量评估（FID/FVD）上有效，在像素级重建精度（PSNR/SSIM/LPIPS）上同样具有竞争力。定性结果（**Figure 7**）显示，Scaling4D 生成的视频在细节保真度和几何一致性方面均优于基线方法。

![[assets/figures/papers/paper_list_l2587_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_Scaling4D_Pushing/figures/008_Figure_7.jpg]]
*Figure 7: The qualitative results on the multi-view dataset. From left to right, we display ground truth images, results of ours, GEN3C [39], TrajectoryCrafter [52], Voyager [21] and ReCamMaster-Wan [2], respectively*

![[assets/figures/papers/paper_list_l2587_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_Scaling4D_Pushing/figures/010_Table_2.jpg]]
*Table 2: The quantitative results on the multi-view dataset*

### 消融实验

消融实验（**Table 3**）揭示了训练数据构成对模型性能的关键影响：

![[assets/figures/papers/paper_list_l2587_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_Scaling4D_Pushing/figures/011_Table_3.jpg]]
*Table 3: Ablation study on the single-view dataset. Results on different variants of our method: training with additional double reprojection data (Ours + DoubleProj), training solely on synthetic data (Ours w/o RealData) and training exclusively on real data (Ours w/o SynData)*

- **真实数据的重要性**：仅使用合成数据训练的变体（Ours w/o RealData）在视觉质量指标上出现大幅劣化（FVD 升至 472.62，相比完整模型 411.17），这证明大规模真实单目视频数据对于模型学习鲁棒、自然的视觉表征至关重要。
- **精度与质量的权衡**：在训练中加入额外的双重重投影数据（Ours + DoubleProj）可提升姿态精度（RotErr 降至 6.27），但可能对视觉质量产生负面影响。这表明在生成任务中，姿态精度与视觉质量之间存在需要仔细权衡的张力关系。

### 训练-推理差距的桥接验证

Scaling4D 的核心设计之一是使用光流对应关系训练、深度对应关系推理，并通过光流噪声的自监督鲁棒性来桥接二者之间的差距。**Figure 8** 提供了这一机制的可视化验证：在静态场景下，基于光流的对应关系 $C_{\mathrm{flow}}^{r}$ 与基于深度的对应关系 $C_{\mathrm{depth}}^{r}$ 高度一致。定量分析进一步表明，光流对应关系具有更高的总变分（$\mathrm{TV}_1(C) = \mathbb{E}[\|\nabla u_t\|_1 + \|\nabla v_t\|_1]$）和拉普拉斯能量（$\mathrm{LapE}(C) = \mathbb{E}[\|\Delta u_t\|_2^2 + \|\Delta v_t\|_2^2]$），即本质上是更“粗糙”的信号。训练过程中对这种粗糙信号的适应，迫使模型学习抗噪声的映射能力，从而在推理时面对更平滑的深度对应关系时表现出更强的鲁棒性。

### 可扩展性分析

**Figure 9** 展示了模型性能随训练数据量增加的变化趋势。随着训练数据规模的扩大，视觉质量指标（FID、FVD）持续改善，展现出良好的可扩展性。然而，姿态精度指标（RotError、TransError）在数据量达到较高水平后趋于饱和，这暗示当前瓶颈可能已从数据规模转移至上游光流和深度估计模型的固有精度限制。

### 失败模式与局限

尽管 Scaling4D 在整体性能上取得了显著提升，仍存在以下可识别的失败模式：

1. **姿态精度饱和**：如可扩展性分析所示，姿态精度的提升在数据量增加后趋于停滞，受限于光流模型（RAFT）和深度模型（GeometryCrafter）的误差传播。
2. **合成数据的局限性**：合成数据虽能提供精确的对应关系监督，但其多样性和真实性有限，模型在合成数据上的过拟合可能损害在真实场景下的泛化性。
3. **上游模型依赖**：整个 pipeline 对多个预训练模型（光流、深度、语言编码器）存在耦合依赖，任一上游模型的误差都会传播至最终生成结果。
4. **极端场景鲁棒性不足**：在含有剧烈非刚体形变、透明物体或镜面反射的场景下，基于光流和深度的对应关系可能失准，导致生成质量下降。这一问题在论文中被列为开放问题，需要进一步研究。

## 定位与知识库关联

### 1. 任务范式的代际跃迁：从“修复”到“对应关系引导生成”

Scaling4D 的核心贡献在于对视频新视角合成（VNVS）任务范式的重新定义。传统方法将 VNVS 视为一个“渲染-修复”问题：先通过点云渲染获得粗糙的目标视角图像 $I^r$ 和掩码 $M^r$，再交由生成模型补全空洞和修复伪影。这一范式在训练与推理之间存在根本性的数据分布不一致——训练时使用的是单目视频的修复任务，推理时却需要处理视角变化带来的遮挡区域。Figure 2 中的案例直观揭示了这一鸿沟：在新视角下，红框区域本应显示人物的背部，但修复范式却错误地填充了背景像素。

Scaling4D 将 VNVS 重新定义为通用的“对应关系引导生成”任务。其理论根基在于一个关键的等价性观察：

$$\mathbf{C}^{r} \Longleftrightarrow \Phi \circ \mathbf{T}^{r} \circ \Phi^{-1}$$

即二维像素对应关系 $C^r$ 与“反投影-刚体变换-投影”的组合操作在数学上等价。这一洞察使得训练和推理可以共享统一的对应关系空间：训练时通过光流模型（如 RAFT）从任意单目视频中提取 $C^r$，推理时则通过深度图计算 $C^r$。由此，VNVS 的训练范式升级为：

$$\mathbf{I}^{s} \xrightarrow{\mathbf{C}^{r}} \mathbf{I}^{r} \xrightarrow{G_{\theta}} \mathbf{I}^{*} \Leftarrow \mathbf{I}^{t}$$

这一范式跃迁使得 Scaling4D 能够利用大规模单目野生视频进行可扩展训练，从根本上打破了此前方法对稀缺多视角数据的依赖。

### 2. 与基线方法的关系图谱

Scaling4D 与现有方法的关系可以从控制信号类型和训练数据来源两个维度进行定位。

**基于3D几何控制的方法**：**GEN3C**（Ren et al., CVPR 2025）将3D信息作为视频生成的条件，但其训练范式仍受限于特定数据分布。**ReCamMaster-Wan** 采用隐式几何控制，同样面临训练数据多样性的瓶颈。Scaling4D 继承了“几何控制信号引导生成”的思路，但通过对应关系的等价变换将其泛化为更通用的形式，从而解锁了大规模单目视频作为训练数据的可能性。

**基于点云修复的方法**：**TrajectoryCrafter**（Yu et al., ICCV 2025）和 **Voyager** 代表了“渲染-修复”范式的典型实现。它们将点云渲染结果作为中间表示，依赖生成模型进行后续修复。Scaling4D 的实验结果（Table 1, Table 2）表明，这种范式在处理视角变化导致的遮挡区域时存在本质缺陷，而对应关系引导的生成范式在 FID（62.83 vs 约82.31）、FVD（411.17 vs 约632.95）等视觉质量指标上实现了显著提升。

值得指出的是，Scaling4D 并非完全抛弃了3D几何信息——推理阶段仍需深度估计器（GeometryCrafter）提供深度图以计算对应关系，但训练阶段通过光流噪声的自监督鲁棒性机制（详见第4.4节分析）有效桥接了训练-推理差距。

### 3. 适用边界与局限

**训练数据规模的饱和效应**：Scaling4D 的可扩展性分析（Figure 9）表明，视觉质量指标（FID, FVD）随训练数据量增加持续改善，但姿态精度指标（RotError, TransError）在数据量达到一定水平后趋于饱和。这一饱和现象可能源于光流和深度估计的固有精度上限，而非模型容量不足。当数据量进一步增加时，如何打破这一瓶颈仍是开放问题。

**上游模型的耦合依赖**：整个 pipeline 强依赖于多个预训练模型——光流估计器（RAFT）、深度估计器（GeometryCrafter）、3D VAE 和 LLM 文本编码器。上游模型的误差会直接传播至下游任务。特别是在含有剧烈非刚体形变、透明物体或镜面反射的场景下，基于光流和深度的对应关系可靠性存疑，目前缺乏系统性的鲁棒性评估。

**合成数据与真实数据的权衡**：消融实验（Table 3）揭示了合成数据与真实数据之间的微妙张力。仅使用合成数据训练（Ours w/o RealData）会导致 FVD 从 411.17 劣化至 472.62，证明大规模真实单目数据对视觉质量至关重要。然而，单纯增加真实数据量可能导致姿态精度饱和；引入额外的双重重投影数据（Ours + DoubleProj）可将 RotErr 降至 6.27，但可能损害视觉质量。这意味着精度与视觉质量之间存在需要显式权衡的帕累托前沿。

**静态场景假设的脆弱性**：训练-推理差距桥接的可视化验证（Figure 8）在静态场景下展示了光流对应与深度对应的良好对齐，但这一对齐在动态场景（尤其是含有独立运动物体的场景）中的保持程度尚未得到充分验证。

### 4. 开放问题与后续方向

1. **突破姿态精度饱和瓶颈**：当训练数据量跨越某个阈值后，如何通过改进对应关系质量（如引入更精确的光流/深度模型）或设计针对性的损失函数来持续提升姿态精度？

2. **降低上游模型耦合度**：能否通过端到端训练或联合优化，减少对多个独立预训练模型的依赖？例如，是否可以将光流/深度估计与生成模型进行一定程度的协同训练？

3. **范式迁移潜力**：对应关系引导的生成范式在理论上具有通用性——任何需要空间一致性的视频/三维生成任务（如视频修复、视角插值、3D场景生成）都可能受益于这一思路。探索该范式在其他任务上的迁移效果是一个有价值的方向。

4. **动态场景鲁棒性**：在含有显著非刚体运动、透明/反射表面的场景下，当前基于光流和深度的对应关系提取机制可能失效。是否需要引入额外的运动表征（如场景流、语义对应）来增强鲁棒性？

5. **训练-推理一致性的理论分析**：当前通过光流噪声的自监督鲁棒性来桥接训练-推理差距的策略在经验上有效，但缺乏严格的理论保证。对 $C_{flow}^r$ 和 $C_{depth}^r$ 之间分布差异的更深入分析（如通过 TV$_1(C)$ 和 LapE$(C)$ 等光滑性度量）可能揭示更优的桥接策略。

## 原文 PDF

![[paperPDFs/CVPR_2026/Scaling4D_Pushing_the_Frontier_of_Video_Novel_View_Synthesis_through_Large_Scale_Monocular_Videos.pdf]]
