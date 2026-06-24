---
title: "Spatia: Video Generation with Updatable Spatial Memory"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Spatia_Video_Generation_with_Updatable_Spatial_Memory.pdf
code_link: null
aliases:
- Spatia
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 通过显式维护一个三维场景点云作为持久空间记忆，并在每一轮生成中基于该记忆进行条件控制，实现静态场景与动态实体的解耦。
primary_logic: 利用视觉SLAM估计场景点云作为几何锚点，结合检索到的参考帧和投影场景视频，为视频生成提供几何一致的空间引导，同时通过动静态解耦保留动态内容的生成能力。
claims:
- Spatia在WorldScore基准上平均得分69.73，显著优于所有比较方法。
- 同时使用场景投影视频和参考帧显著提升空间记忆指标（相机控制、PSNR_C等）。
- 闭环评估中，Spatia的空间记忆一致性（PSNR_C 19.38, Match Acc 0.698）远超所有基线。
- WorldScore 上 Average Score = 69.73
---

# Spatia: Video Generation with Updatable Spatial Memory

> [!tip] 核心洞察
> 利用视觉SLAM估计场景点云作为几何锚点，结合检索到的参考帧和投影场景视频，为视频生成提供几何一致的空间引导，同时通过动静态解耦保留动态内容的生成能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | Spatia：具有可更新空间记忆的视频生成 |
| 英文题名 | Spatia: Video Generation with Updatable Spatial Memory |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.15716) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | Spatia |
| Dataset | WorldScore, RealEstate, WorldScore Subset |

> [!tip] 效果简介
> - WorldScore 上，Average Score 69.73 vs 66.08 (Voyager) (+3.65)。
> - RealEstate 上，PSNR 18.58 vs 17.79 (Voyager) (+0.79)。
> - WorldScore Subset (Memory Evaluation) 上，PSNR_C 19.38 vs 17.66 (Voyager) (+1.72)。

## 概述

现有视频生成模型在生成长时间、多视角的视频序列时，面临一个核心瓶颈：由于视频数据的高维度特性，模型难以有效编码长时间历史信息，导致空间和时间一致性差，尤其在需要重复访问同一场景位置时，缺乏持久空间记忆。这一问题的根源在于，大多数方法仅依赖前一视频片段作为时序条件，无法维护场景的全局几何表示。

Spatia 提出了一种显式的、可更新的空间记忆机制来解决上述问题。其核心洞察是：利用视觉SLAM估计三维场景点云作为几何锚点，将静态场景与动态实体解耦，从而在保留动态内容生成能力的同时，为视频生成提供几何一致的空间引导。具体而言，Spatia 维护一个三维场景点云作为持久空间记忆，在每一轮生成中基于该记忆进行条件控制，并通过视觉SLAM持续更新该点云。

在方法定位上，Spatia 区别于两类现有工作：一类是静态场景生成模型（如 **WonderJourney** (Yu et al., CVPR 2024)、**Voyager** 等），它们无法处理动态实体；另一类是基础视频生成模型（如 **CogVideoX-I2V** (Yang et al., arXiv 2024)、**Wan2.1** (Wan Team, arXiv 2025) 等），它们通常缺乏持久记忆机制。Spatia 通过引入并行 ControlNet 块融合场景点云条件、基于空间相似度的参考帧检索、以及基于 SAM2 的动态实体分割与排除，实现了动静态解耦的空间记忆视频生成。

实验结果表明，Spatia 在 WorldScore 基准上平均得分 69.73，显著优于最佳基线 Voyager 的 66.08（+3.65）；在闭环空间记忆评估中，Spatia 的 PSNR_C 达到 19.38，Match Accuracy 达到 0.698，远超所有基线方法。消融实验进一步证实，同时使用场景投影视频和参考帧是提升空间一致性的关键，而增大点云密度可在质量与存储开销之间提供可控权衡。

目前该方法仍存在若干局限：空间记忆质量高度依赖点云估计精度；动静态解耦在复杂动态场景下可能失效；框架主要面向静态场景背景，在全动态场景中的适用性有待验证。后续研究可探索将空间记忆机制扩展到完全动态的4D场景，以及与更强的基础视频生成模型结合以进一步提升视觉质量与可控性。

## 背景与动机

视频生成领域近年来取得了显著进展，大规模基础模型如 **Veo** (Google, 2024)、**Sora** (OpenAI, 2024)、**Kling** (Kuaishou, 2024) 和 **Hailuo** (MiniMax, 2024) 已展现出令人印象深刻的视觉质量。然而，现有模型面临一个核心瓶颈：由于视频数据的高维度特性，它们难以有效编码长时间历史信息，导致空间和时间一致性不足，尤其在需要重复访问同一场景位置时缺乏持久空间记忆。

当前的方法可大致分为两类，各有其固有局限。静态场景生成模型如 **WonderJourney** (Yu et al., CVPR 2024)、**WonderWorld** (Yu et al., arXiv 2024) 和 **Voyager** 专注于生成场景的静态外观，但无法处理动态实体。另一方面，基础视频生成模型如 **VideoCrafter2**、**EasyAnimate**、**Allegro** (Zhou et al., arXiv 2024)、**CogVideoX-I2V** (Yang et al., arXiv 2024) 和 **Wan2.1** (Wan Team, arXiv 2025) 虽能生成动态内容，却通常缺乏持久记忆机制——它们仅依赖前一视频片段作为上下文，无法在长序列生成中维持空间一致性。

近期一些工作开始探索空间记忆视频生成，如 **SEVA** (Zhou et al., arXiv 2025)、**VMem** (Li et al., arXiv 2025) 和 **ViewCrafter** (Yu et al., arXiv 2024)，试图在生成过程中引入某种形式的场景记忆。但这些方法尚未系统性地解决动静态解耦问题，也未充分利用三维几何信息作为生成条件。

Spatia 的核心动机正是填补这一空白：通过显式维护一个三维场景点云作为持久空间记忆，并在每一轮生成中基于该记忆进行条件控制，实现静态场景与动态实体的解耦。其关键洞察在于利用视觉 SLAM 估计场景点云作为几何锚点，结合检索到的参考帧和投影场景视频，为视频生成提供几何一致的空间引导，同时通过动静态解耦保留动态内容的生成能力。这种设计使得模型能够在长序列、多视角、闭环等场景下保持稳健的空间一致性，并为 3D 交互式编辑等应用提供了基础。

## 核心创新

Spatia 的核心创新在于将视频生成重新定义为一个**以持久空间记忆为条件的迭代生成问题**，通过显式维护并动态更新的三维场景点云，将静态场景几何与动态实体生成解耦，从而在长序列、多视角和闭环生成中实现显著的空间一致性提升。

### 问题瓶颈与因果机制

现有视频生成模型面临的根本瓶颈在于：视频数据的高维度特性使得模型难以有效编码长时间跨度的历史信息，导致空间与时间一致性随序列增长而急剧退化，尤其在需要重复访问同一场景位置时缺乏持久记忆。Spatia 的因果调节变量（causal knob）是**显式维护一个三维场景点云作为持久空间记忆**，并在每一轮生成中基于该记忆进行条件控制。其核心洞察在于：利用视觉 SLAM 估计场景点云作为几何锚点，结合检索到的参考帧和投影场景视频，为视频生成提供几何一致的空间引导；同时通过动静态解耦，将静态场景固定于空间记忆中，保留对动态内容的自由生成能力。

### 关键创新点（Changed Slots）

与现有方法相比，Spatia 在以下四个关键维度上实现了结构性改变：

**1. 空间记忆机制：从无记忆到持久三维点云记忆**

基线方法（如 WonderJourney、Voyager、CogVideoX-I2V 等）仅依赖前一视频片段作为时序上下文，缺乏跨片段的持久空间记忆。Spatia 维护并迭代更新一个全局三维静态场景点云，通过 MapAnything 从生成帧中持续估计和融合场景几何，将空间记忆从“瞬时遗忘”转变为“持久积累”。在推理时，用户可在每一轮交互中基于更新后的点云指定新的相机轨迹和文本指令，实现空间一致的迭代生成（Figure 4）。

**2. 网络架构：并行 ControlNet 块融合场景几何条件**

Spatia 以 Wan2.2 作为基础生成模型，在其主块之外引入**并行 ControlNet 块**，专门处理场景点云投影视频条件。每个网络块包含一个 ControlNet 块与四个主块并行运行，ControlNet 输出通过特征加法与主块特征融合（Figure 3）。这种设计使得几何条件信号能够深度嵌入生成过程，同时保持基础模型的生成能力不被破坏。

**3. 参考帧检索：基于空间重叠的自适应条件增强**

Spatia 引入了一种基于空间相似度的参考帧检索机制：通过计算目标片段与候选帧集合之间的场景点云空间对应关系，检索出与当前视点最相关的 K 个历史帧作为额外条件（Figure 2(b)）。消融实验表明，同时使用场景投影视频和参考帧可将相机控制指标提升至 84.47，PSNR_C 提升至 19.38（Table 4）；单独使用某一类条件则性能显著下降。参考帧数量 K 增大可稳步提升空间记忆指标，但 K>7 后提升趋于平缓（Table 5）。

**4. 动静态解耦：SAM2 分割保护静态记忆纯净性**

Spatia 利用 SAM2 对动态实体进行跟踪与分割，在更新空间记忆时显式排除动态区域，确保场景点云仅保留静态几何信息（Section 6, Figure 7）。这一设计使得模型能够在不污染空间记忆的前提下自由生成动态内容，从根本上解决了静态场景记忆与动态内容生成之间的冲突。

### 证据强度与局限性

Spatia 在 WorldScore 基准上取得平均分 69.73，显著优于最强基线 Voyager 的 66.08（Table 1）；在闭环评估中，PSNR_C 达 19.38，匹配准确率达 0.698，远超所有基线（Table 3），有力支撑了空间记忆机制的有效性。然而，该方法存在以下已知局限：点云估计精度直接影响生成质量，低质量几何重建会降低空间一致性；动静态解耦依赖 SAM2 分割，在复杂动态场景或运动模糊下可能失效；当前框架主要面向静态场景背景，对全动态场景的长序列记忆能力尚待验证；点云密度与存储开销之间存在权衡，实时编辑场景下可能面临效率挑战。

## 整体框架

Spatia 将视频生成重新定义为一个**多模态条件生成问题**，其核心创新在于引入并持续维护一个显式的三维场景点云作为**持久空间记忆**。整个框架围绕“估计—条件—生成—更新”的闭环展开，将静态场景几何与动态内容生成解耦。

### 训练阶段

训练流水线首先将每个训练视频 $V$ 分解为三个部分：

$${V} = {T}^N \cup {P}^M \cup {C}^O$$

其中 ${T}^N$ 为目标片段（target clip），${P}^M$ 为前序片段（preceding clip），${C}^O$ 为候选帧集合（candidate-frame set）。基于这一分解，训练过程依次执行以下步骤（详见 Figure 2）：

![[assets/figures/papers/paper_list_l2596_https_arxiv_org_abs_2512_15716/figures/006_Figure_2.jpg]]
*Figure 2: Overview of the training stage of Spatia. Each training video is divided into a target clip, a preceding clip, and a candidate-frame set. Text tokens are omitted for simplicity. (a) A frame is randomly selected from the candidate-frame set to estimate a 3D scene point cloud S. Using the estimated camera poses together with*

1. **场景点云估计**：从候选帧集合中随机采样一帧，利用 **MapAnything** 估计全局三维静态点云 $S$，同时获取每帧对应的相机位姿。利用估计的相机位姿与 $S$，为目标片段和前序片段分别生成**视图相关的场景点云投影序列**，作为几何条件。

2. **参考帧检索**：基于目标片段与候选帧集合的场景点云计算空间对应关系（空间重叠度），从候选帧中检索与目标片段最相关的 $K$ 个参考帧。这些参考帧提供了额外的外观和纹理先验。

3. **多模态条件生成**：以文本指令、参考帧、前序视频片段、场景投影视频为条件，通过 **Flow Matching** 框架训练生成目标视频。网络架构基于 **Wan2.2** 的主块设计，并在每 4 个主块旁并行引入 1 个 **ControlNet** 块（共 8 个网络块），专门融合场景点云条件。ControlNet 块的输出与主块特征通过加法融合。训练损失为预测速度 $\mathbf{v}_t$ 与真实速度 $\mathbf{u}_t$ 之间的均方误差：

   $$\mathcal{L} = \mathbb{E}_{t, \mathbf{x}_0, \boldsymbol{X}_T} \left\| \mathbf{v}_t - \mathbf{u}_t \right\|^2$$

### 推理阶段

推理阶段采用**迭代交互式**流程（见 Figure 4），将空间记忆的维护与用户控制紧密结合：

![[assets/figures/papers/paper_list_l2596_https_arxiv_org_abs_2512_15716/figures/009_Figure_4.jpg]]
*Figure 4: Illustration of the Spatia inference process. At the first iteration, the user provides an initial image, from which Spatia estimates the initial 3D scene point cloud. The user then specifies a text instruction and a camera path based on the estimated scene, producing a projection video along the desired trajectory that conditions the generation of clip-1. In subsequent iterations, two steps are performed: (1) Spatia updates the spatial memory (3D scene point cloud) using all previously generated frames via MapAnything [42]; and (2) the user specifies a new text instruction and camera path based on the updated scene. Spatia then takes the reference frames (generated as described in Section...*

1. **初始化**：用户提供初始图像，Spatia 通过 MapAnything 估计初始三维场景点云，作为空间记忆的起点。

2. **迭代生成**：在每一轮迭代中，用户基于当前场景点云指定文本指令和相机轨迹。系统沿该轨迹渲染场景投影视频，结合检索到的参考帧和上一轮生成的前序视频片段，通过训练好的条件生成网络产生新的视频片段。

3. **记忆更新**：新生成的视频帧与历史帧一起，通过 MapAnything 重新估计并更新全局场景点云。更新过程中，利用 **SAM2** 分割并追踪动态实体，将其区域从点云更新中排除，确保空间记忆仅保留静态场景几何，实现**动静态解耦**。

这一闭环设计使得 Spatia 能够在长序列生成中持续保持空间一致性——当相机轨迹回到初始视点时，生成的最终帧与初始图像在几何和外观上高度吻合，这是传统无记忆模型无法实现的。

### 补充图表

![[assets/figures/papers/paper_list_l2596_https_arxiv_org_abs_2512_15716/figures/007_Figure_3.jpg]]
*Figure 3: we then generate view-specific scene point cloud sequences for both the target and preceding clips. (b) The most spatially relevant frames are then retrieved from the candidate-frame set as reference frames. (c) The spatial conditions obtained from (a) and (b) guide the video generation process. The detailed network architecture is provided in Figure 3*

## 核心模块与公式推导

Spatia 的核心架构围绕“可更新的三维空间记忆”展开，将长视频生成转化为一个多模态条件生成问题。整个框架由四个关键模块串联而成，并通过 Flow Matching 训练范式统一优化。

### 3.1 场景点云估计

空间记忆的物理载体是一个全局静态三维场景点云 $S$。在训练阶段，对于给定的训练视频 $V$，先将其分解为目标剪辑 ${T}^N$、前序剪辑 ${P}^M$ 和候选帧集 ${C}^O$ 三部分（${V} = {T}^N \cup {P}^M \cup {C}^O$）。随后从候选帧集中随机采样一帧，利用 **MapAnything** 估计场景点云 $S$，同时获得每帧对应的相机位姿。利用估计的相机位姿与 $S$，可为目标剪辑和前序剪辑分别渲染出视图相关的场景投影视频序列，作为后续生成网络的几何条件。

### 3.2 参考帧检索

除了投影视频提供的显式几何引导，Spatia 还引入参考帧作为隐式外观约束。检索过程基于目标剪辑与候选帧集各自关联的场景点云计算空间对应关系，选取空间重叠度最高的 $K$ 帧作为参考帧。这一策略确保参考帧与目标剪辑在三维空间中高度相关，从而为生成网络补充细粒度的纹理和光照信息。详细检索流程见论文 Algorithm 1。

### 3.3 多模态条件生成网络

Spatia 的生成主干基于 **Wan2.2** 架构，并在每个网络块中引入并行的 **ControlNet** 块以融合场景点云条件。具体而言，每个网络块由 1 个 ControlNet 块与 4 个主块并行构成（Figure 3），ControlNet 块接收场景投影视频作为输入，其输出特征以加法方式注入主块，实现几何条件与生成主干的深度融合。文本指令、参考帧和前序视频则作为常规条件信号输入主块。

![[assets/figures/papers/paper_list_l2596_https_arxiv_org_abs_2512_15716/figures/008_Figure_3.jpg]]
*Figure 3: Illustration of a single network block composed of one ControlNet [115] block operating in parallel with four main blocks. Detailed definitions of all token types are provided in Figure 2*

### 3.4 Flow Matching 训练

模型训练采用 Flow Matching 范式，优化目标为最小化网络预测速度 $\mathbf{v}_t$ 与真实速度 $\mathbf{u}_t$ 之间的均方误差：

$$\mathcal{L} = \mathbb{E}_{t, \mathbf{x}_0, \boldsymbol{X}_T} \left\| \mathbf{v}_t - \mathbf{u}_t \right\|^2$$

其中 $t$ 为扩散时间步，$\mathbf{x}_0$ 为干净视频，$\boldsymbol{X}_T$ 为纯噪声。该损失函数驱动网络在多种条件信号（文本、参考帧、前序视频、场景投影视频）的联合引导下，逐步从噪声中还原目标视频剪辑。

### 3.5 推理阶段的空间记忆更新

推理过程（Figure 4）以迭代交互方式展开。首轮迭代中，用户提供初始图像，Spatia 据此估计初始三维场景点云；用户随后指定文本指令和基于场景估计的相机轨迹，生成对应的投影视频作为条件，产出第一个视频剪辑。在后续迭代中，Spatia 利用所有已生成帧通过 MapAnything 更新全局点云，用户基于更新后的场景指定新的指令和相机路径，模型以上一轮生成的视频剪辑、检索到的参考帧以及新的投影视频为条件，生成下一段视频。这一闭环更新机制确保了长序列生成中的几何一致性。

## 实验与分析

Spatia 在多个基准上进行了系统评估，覆盖视觉质量、空间记忆一致性和长序列生成能力。以下从主结果、消融实验、关键图表结论和失败模式四个维度展开分析。

### 主结果：WorldScore 与 RealEstate

**WorldScore 综合评估。** WorldScore 基准同时考察静态场景质量与动态内容生成能力，最终聚合为 Static Score 和 Dynamic Score，取均值作为 Average Score。如 Table 1 所示，Spatia 取得 Average Score **69.73**，显著优于最强基线 Voyager（66.08，+3.65），在 Static Score（72.63）和 Dynamic Score（66.82）上均保持领先。这一结果验证了空间记忆机制在同时保持场景几何一致性和动态生成自由度方面的有效性。

**RealEstate 测试集。** 在 RealEstate 数据集上，Spatia 的 PSNR 达到 **18.58**，SSIM 达到 **0.646**，均超过所有对比方法（Table 2）。值得注意的是，所有基线均使用其默认配置在相同测试样本上复现，确保了公平性。

### 空间记忆机制专项评估

为直接衡量空间记忆的持久性，论文设计了闭环评估协议：要求模型生成一段相机轨迹回到初始视角的视频，然后计算末帧与初始图像之间的 PSNR、SSIM、LPIPS 和 Match Accuracy。Table 3 显示，Spatia 在 PSNR_C（**19.38**）和 Match Accuracy（**0.698**）上大幅领先 Voyager（PSNR_C 17.66, Match Acc 0.507），差距分别达 +1.72 和 +0.191。这表明显式三维点云记忆在保持跨时间步的空间一致性方面具有本质优势，而仅依赖隐式视频上下文的基线在闭环条件下会出现显著的几何漂移。

![[assets/figures/papers/paper_list_l2596_https_arxiv_org_abs_2512_15716/figures/013_Table_3.jpg]]
*Table 3: Memory Mechanism Evaluation on the WorldScore Subset. Each test sample includes a ground-truth initial image. Using this image, we require the model to generate a closed-loop video, where the camera in the final frame returns to the initial viewpoint. We then compute PSNR, SSIM, LPIPS, and Match Accuracy between the final frame and the initial image to evaluate spatial memory consistency*

### 消融实验

**场景投影视频与参考帧的贡献。** Table 4 的消融表明，同时使用场景投影视频和参考帧时，Camera Control 指标达到 84.47，PSNR_C 达到 19.38；单独移除任一条件均导致性能显著下降。这揭示了两类条件的互补机制：投影视频提供粗粒度的几何锚定，参考帧则补充细粒度的外观和纹理信息，二者协同构成了空间记忆的核心。

**参考帧数量。** Table 5 显示，随着参考帧数量 K 从 1 增加到 7，空间记忆指标稳步提升；但当 K 超过 7 后，增益趋于平缓。这说明在一定范围内，更多的历史观测有助于丰富场景表示，但信息冗余随之增加。

**长序列生成。** Table 6 对比了 Spatia 与基础模型 Wan2.2 在长序列生成中的表现。随着生成帧数增加，Wan2.2 的质量急剧下降，而 Spatia 凭借持续更新的空间记忆保持了视觉质量和空间一致性，验证了记忆机制在长时域生成中的关键作用。

**点云密度。** Table 7 探索了点云下采样体素边长 d 的影响。增大 d 可大幅降低内存占用，但会损失精细几何信息，导致生成视频的视觉质量下降。这揭示了空间记忆精度与计算开销之间的核心权衡。

### 关键图表结论

- **Figure 5** 定性展示了三种变体在长序列生成中的差异：完整 Spatia 模型保持场景结构稳定，仅用投影视频的变体出现纹理退化，仅用参考帧的变体则产生几何漂移，直观印证了双条件协同的必要性。
- **Figure 6** 展示了闭环生成的可视化结果，末帧与初始帧高度一致，为 Table 3 的定量结论提供了直观佐证。
- **Figure 7** 展示了动静态解耦效果：SAM2 分割出的动态实体（如行人、车辆）被排除在空间记忆更新之外，静态点云保持纯净，生成视频中动态实体自然融入静态场景。
- **Figure 8** 展示了 3D 交互式编辑能力：用户可直接修改场景点云（删除物体、添加新物体、修改属性），生成视频中编辑效果几何精确，体现了空间记忆作为显式几何表征的可编辑性优势。

![[assets/figures/papers/paper_list_l2596_https_arxiv_org_abs_2512_15716/figures/017_Figure_5.jpg]]
*Figure 5: Qualitative comparison of three variants for long-horizon video generation: (1) our default model Spatia, (2) a variant using only scene videos without reference frames, and (3) a variant using reference frames but no scene videos. The spatial memories shown in the figure are generated by Spatia*

### 失败模式与局限性

Spatia 的性能高度依赖点云估计精度。当 MapAnything 在低纹理区域或复杂几何结构下产生低质量重建时，投影视频的几何引导作用减弱，生成视频的空间一致性随之下降。动静态解耦基于 SAM2 分割，在运动模糊、遮挡或复杂动态场景下可能出现分割失败，导致动态伪影污染静态记忆。此外，当前框架主要针对静态场景背景设计，对完全动态的 4D 场景（如大规模人群、流体运动）的长序列记忆能力尚未验证，这是从“静态记忆”迈向“通用时空记忆”的关键挑战。

### 补充图表

![[assets/figures/papers/paper_list_l2596_https_arxiv_org_abs_2512_15716/figures/010_Table_1.jpg]]
*Table 1: Visual quality comparison on the WorldScore benchmark. The final Static and Dynamic world scores are computed by aggregating all relevant metrics. The Average score represents the mean of the static and dynamic world scores. Static scene generation models cannot handle dynamic entities, while foundation video generation models typically lack persistent memory mechanisms*

![[assets/figures/papers/paper_list_l2596_https_arxiv_org_abs_2512_15716/figures/011_Table_2.jpg]]
*Table 2: Evaluation on RealEstate. We reproduce the results of all baseline methods using their default configurations and evaluate them on the same test samples to ensure a fair comparison*

![[assets/figures/papers/paper_list_l2596_https_arxiv_org_abs_2512_15716/figures/015_Table_4.jpg]]
*Table 4: Impact of incorporating scene projection videos and reference frames on spatial memory modeling. The “Camera Control” metric is adopted from the WorldScore benchmark*

![[assets/figures/papers/paper_list_l2596_https_arxiv_org_abs_2512_15716/figures/016_Table_5.jpg]]
*Table 5: Effects of using different numbers of reference frames*

![[assets/figures/papers/paper_list_l2596_https_arxiv_org_abs_2512_15716/figures/012_Table_6.jpg]]
*Table 6: Memory mechanisms ensure spatial consistency and preserve visual quality in long-horizon generation*

![[assets/figures/papers/paper_list_l2596_https_arxiv_org_abs_2512_15716/figures/014_Table_7.jpg]]
*Table 7: Impact of point cloud density on visual quality. Metrics are computed between the generated videos and the ground-truth videos on the RealEstate test set*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

Spatia 的核心贡献在于将**持久化三维空间记忆**引入视频生成流程，从而在现有工作的两条主线上建立了新的连接点：静态场景生成模型与通用视频生成基础模型。

**相对于静态场景生成模型**：WonderJourney（Yu et al., CVPR 2024）、InvisibleStitch、WonderWorld（Yu et al., arXiv 2024）和 Voyager 等方法专注于从单一或少量图像出发，沿相机轨迹生成视觉一致的静态场景视频。这些方法通常依赖隐式神经表示或逐帧外推，缺乏对场景的显式三维几何建模。Spatia 与它们的关键区别在于：Spatia 维护并迭代更新一个显式的三维场景点云作为空间记忆，而非仅依赖前一视频片段进行条件生成。这一设计使得 Spatia 在闭环评估中展现出显著更强的空间记忆一致性——PSNR_C 达到 19.38，Match Accuracy 为 0.698，而 Voyager 仅分别为 17.66 和 0.507（Table 3）。

**相对于通用视频生成基础模型**：VideoCrafter2、EasyAnimate、Allegro（Zhou et al., arXiv 2024）、CogVideoX-I2V（Yang et al., arXiv 2024）、Vchitect-2.0、LTX-Video 和 Wan2.1（Wan Team, arXiv 2025）等模型在开放域视频生成上展示了强大的视觉质量，但它们通常缺乏持久空间记忆机制，难以在长序列生成中维持空间一致性。Spatia 以 Wan2.2 作为基础架构，通过引入并行 ControlNet 块来融合场景点云条件，在不牺牲基础模型生成能力的前提下，为空间一致性提供了几何引导。Table 1 显示 Spatia 在 WorldScore 基准上的平均得分 69.73 优于所有比较方法，包括最强的基线 Voyager（66.08），表明显式空间记忆对整体视觉质量有正向贡献。

**相对于空间记忆视频生成模型**：SEVA（Zhou et al., arXiv 2025）、VMem（Li et al., arXiv 2025）、ViewCrafter（Yu et al., arXiv 2024）和 FlexWorld 等近期工作同样探索了为视频生成赋予空间记忆。Spatia 的独特之处在于：将空间记忆形式化为三维点云，并通过视觉 SLAM（MapAnything）进行估计与更新，同时引入基于空间重叠的参考帧检索机制。消融实验表明，同时使用场景投影视频和参考帧能将 Camera Control 提升至 84.47、PSNR_C 提升至 19.38，而单独使用任一条件均会导致性能显著下降（Table 4），这验证了多模态空间条件的互补性。

### 2. 适用边界

Spatia 的设计假设决定了其最佳应用场景与能力边界：

- **静态场景背景假设**：Spatia 的空间记忆机制明确针对静态场景背景设计。在更新三维点云时，系统利用 SAM2 跟踪并分割动态实体，将动态区域从空间记忆中排除，以保持静态记忆的纯净性。这意味着 Spatia 擅长处理“静态场景 + 动态实体”的组合场景，但对于完全动态的 4D 场景（如大规模水体、人群流动），其空间记忆的适用性尚未得到验证。
- **点云估计精度依赖**：整个流程的几何一致性建立在 MapAnything 点云估计质量之上。低质量几何重建会直接降低生成视频的空间一致性，这在复杂纹理、透明表面或重复结构场景中可能成为瓶颈。
- **点云密度与效率的权衡**：增大点云下采样体素边长 d 可大幅减少内存占用，但会因损失精细几何信息而导致视觉质量下降（Table 7），这表明在实时编辑或资源受限场景下存在质量与效率的权衡。
- **动态分割的鲁棒性**：动静态解耦依赖 SAM2 的分割精度，在复杂动态场景或运动模糊下可能失败，导致动态残留污染静态记忆。

### 3. 局限与开放问题

**当前局限**：
1. **点云精度瓶颈**：Spatia 的空间一致性上限受限于 MapAnything 的几何重建质量，低纹理或镜面反射区域可能产生不可靠的点云，进而影响生成质量。
2. **动静态解耦的脆弱性**：SAM2 在快速运动、遮挡或模糊场景下的分割失败会导致动态实体被错误地融入空间记忆，破坏场景的静态一致性。
3. **全动态场景支持缺失**：当前框架的空间记忆本质上是静态的，无法建模场景本身的动态变化（如风吹草动、水面波动），限制了其在开放自然环境中的应用。
4. **计算效率**：点云估计、参考帧检索和 ControlNet 条件注入均引入额外计算开销，在实时交互编辑场景下可能面临延迟挑战。

**开放问题**：
1. **4D 空间记忆扩展**：如何将静态点云记忆机制扩展为可建模场景动态的 4D 表示（如可变形点云或神经场），同时保持高效的更新与检索，是提升框架通用性的关键方向。
2. **与更强基础模型的结合**：当前 Spatia 基于 Wan2.2 架构，若能结合更大规模的 DiT 基础模型（如 Sora、Veo 等），有望进一步提升视觉质量与可控性，但需要解决大规模点云条件注入的效率问题。
3. **实时交互优化**：3D 感知编辑中的交互延迟问题如何通过增量式 SLAM、稀疏点云表示或异步更新策略来优化，以支持更流畅的用户体验。
4. **空间记忆的泛化性**：当前空间记忆在闭环评估中表现优异，但其在开放域、长距离探索场景下的泛化能力——特别是当新生成区域与已有记忆产生几何冲突时的一致性维护——仍需进一步研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/Spatia_Video_Generation_with_Updatable_Spatial_Memory.pdf]]