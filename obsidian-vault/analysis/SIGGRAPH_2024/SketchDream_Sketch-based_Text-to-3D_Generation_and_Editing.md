---
title: "SketchDream: Sketch-based Text-to-3D Generation and Editing"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/SketchDream_Sketch_based_Text_to_3D_Generation_and_Editing.pdf
project_link: null
code_link: null
aliases:
- SketchDream
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: SketchDream
primary_logic: SketchDream
claims:
- SketchDream
---

# SketchDream: Sketch-based Text-to-3D Generation and Editing

> [!tip] 核心洞察
> SketchDream

| 字段 | 内容 |
|------|------|
| 中文题名 | SketchDream: Sketch-based Text-to-3D Generation and Editing |
| 英文题名 | SketchDream: Sketch-based Text-to-3D Generation and Editing |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://arxiv.org/abs/2405.06461) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method |  |
| Dataset |  |

## 概要

从单张手绘草图生成高质量三维内容面临核心瓶颈：二维草图与三维模型之间存在严重的空间歧义，现有方法难以在多视角下保持几何一致性与草图忠实度。本文提出 **SketchDream**，一个文本驱动的三维内容生成与局部编辑框架。其核心思路是利用深度信息作为二维输入与三维模型之间的桥梁——通过预测深度图，将输入草图显式地扭曲到多个新视角，从而建立空间对应关系。在此基础上，基于预训练的 **MVDream** 构建一个带三维注意力的多视角 ControlNet，以扭曲后的草图作为条件，直接生成多视角一致的图像，再通过分数蒸馏采样（SDS）优化 NeRF 表示。该方法同时支持基于草图的自由视角局部编辑。用户研究表明，SketchDream 在生成质量和编辑效果上均优于现有基线方法，在文本忠实度方面表现尤为突出，但在新增组件的细节质量上仍有不足。

## 核心方法与创新机理

SketchDream 的核心目标是在 2D 手绘草图与文本提示的联合控制下，实现高质量的 3D 内容生成与任意视角的局部编辑。该任务面临的核心瓶颈是 **2D 草图到 3D 几何的歧义性**：单张 2D 草图缺乏深度信息，无法唯一确定三维形状，且草图本身是稀疏、非写实的轮廓表达，与真实图像的域差异巨大。SketchDream 的破解思路是**引入深度信息作为 2D 输入与 3D 模型之间的桥梁**，并通过多视图一致性约束将草图控制信号从单视角扩展到三维空间。

整个方法框架由两个阶段构成：**第一阶段**是草图驱动的多视图扩散模型（Sketch-based Multi-View Diffusion Model），负责从单张草图和文本生成多视角一致的多视图图像；**第二阶段**是两阶段 3D 优化（Coarse-to-Fine 3D Optimization），利用多视图扩散模型提供的 2D 先验，通过得分蒸馏采样（SDS）将 2D 生成能力提升到 3D NeRF 表示。

### 2.1 草图驱动的多视图扩散模型

该模块建立在预训练的多视图扩散模型 **MVDream**（Shi et al., 2023）之上。MVDream 本身能从文本生成四个方位角均匀分布（0°、90°、180°、270°）的视图图像，但它缺乏对草图条件的响应能力。SketchDream 对 MVDream 的改动（changed slot）是**引入一个 3D ControlNet 分支**，使扩散模型在生成多视图图像时同时接受草图条件的控制。

具体而言，给定输入草图 $S$ 和文本提示 $y$，模型需要生成四个视角 $\{c_1, c_2, c_3, c_4\}$ 下的图像。直接在不同视角独立施加草图条件会导致跨视角的不一致性——因为草图仅描绘了某个特定视角下的轮廓，其他视角的对应关系是未知的。SketchDream 的解决方案是**深度引导的草图变形（Depth-Guided Warping）**：

1. 首先利用一个预训练的深度估计模型从输入草图 $S$ 生成对应的深度图 $D_s$；
2. 将草图 $S$ 的每个像素根据深度 $D_s$ 和相机参数提升为 3D 点云；
3. 将该点云投影到目标视角 $c_i$，得到变形后的草图 $S_i = \text{Warp}(S, D_s, c_s, c_i)$。

这一操作的因果逻辑是：深度图 $D_s$ 提供了草图轮廓在三维空间中的位置假设，使得原本仅在源视角有效的 2D 轮廓能够被合理地“搬运”到其他视角，从而建立了跨视角的空间对应关系。经过变形后，四个视角的草图条件 $\{S_1, S_2, S_3, S_4\}$ 在几何上相互一致，共同作为 ControlNet 的输入条件。

ControlNet 的训练目标是最小化以下多视图控制损失：

$$\mathcal{L}_{MV-Ctrl}(\phi) = \mathbb{E}_{\mathbf{x}, t, y, s, c, \epsilon} \left[ \| \epsilon - \epsilon_{\phi}(\mathbf{x}_t; t, y, c, s) \|_2^2 \right]$$

其中 $\mathbf{x}_t$ 是加噪后的多视图图像，$t$ 是时间步，$y$ 是文本条件，$c$ 是相机参数，$s$ 是变形后的草图条件，$\epsilon_{\phi}$ 是 ControlNet 预测的噪声。该损失在 MVDream 的 UNet 骨干上微调 ControlNet 分支，而原 MVDream 的权重保持冻结。训练完成后，该模型能够根据单张草图和文本提示，生成四个视角下既忠实于草图轮廓、又保持多视图一致性的图像。

### 2.2 两阶段 3D 优化

有了多视图扩散模型作为 2D 先验后，SketchDream 通过 SDS 优化将 2D 生成能力蒸馏到 3D 表示中。这里采用了从粗到细的两阶段策略，分别对应不同的损失组合。

**粗阶段（Coarse Stage）** 的目标是快速建立大致的几何形状。该阶段使用 3D SDS 损失 $\mathcal{L}_{SDS}^{3D}$，其形式为：

$$\mathcal{L}_{SDS}(\boldsymbol{\theta}, \mathbf{x} = \mathbf{g}(\boldsymbol{\theta}, \mathbf{c})) = \mathbb{E}_{t, \mathbf{c}, \epsilon} \left[ \| \mathbf{x} - \hat{\mathbf{x}}_0 \|_2^2 \right]$$

其中 $\boldsymbol{\theta}$ 是 NeRF 的参数，$\mathbf{g}$ 是体渲染函数，$\mathbf{c}$ 是相机参数，$\hat{\mathbf{x}}_0$ 是扩散模型预测的去噪图像。这里采用 $\mathbf{x}_0$-重建形式的 SDS 损失，而非传统的噪声预测形式，目的是缓解颜色饱和问题。

此外，为了增强生成结果对输入草图的忠实度，在草图视角 $c_s$ 上额外施加 **2D 轮廓损失**：

$$\mathcal{L}_{sil} = \| M_s - C_s^{\alpha} \|_2^2$$

其中 $M_s$ 是从输入草图提取的二值掩码，$C_s^{\alpha}$ 是 NeRF 在草图视角下渲染的 alpha 通道。该损失强制渲染结果的轮廓与输入草图对齐。

**细阶段（Fine Stage）** 的目标是提升细节质量。该阶段的总损失为：

$$\mathcal{L}_{total}^{fine}(\theta) = \beta_1 \mathcal{L}_{SDS}^{3D} + \beta_2 \mathcal{L}_{ISM}^{2D} + \beta_3 \mathcal{L}_{rgb} + \beta_4 \mathcal{L}_{sil} + \beta_5 \mathcal{L}_{ori}$$

其中各损失项的因果分工如下：

- $\mathcal{L}_{SDS}^{3D}$：利用草图驱动的多视图扩散模型提供 3D 一致的监督信号，维持几何合理性；
- $\mathcal{L}_{ISM}^{2D}$：2D 扩散损失，仅在细阶段引入，用于增强局部纹理细节；
- $\mathcal{L}_{rgb}$：RGB 重建损失，约束渲染图像与参考图像的一致性；
- $\mathcal{L}_{sil}$：轮廓损失，维持草图忠实度；
- $\mathcal{L}_{ori}$：朝向损失，规范法线方向以避免几何伪影。

$\beta_1$ 到 $\beta_5$ 是各损失项的权重系数，用于平衡不同约束之间的强度。

### 2.3 草图驱动的 3D 编辑

在编辑模式下，用户选择一个视角渲染原始 3D 模型，修改该视角下的草图（如添加、删除或变形轮廓），并提供编辑区域的掩码和描述编辑目标的文本提示。系统将修改后的草图通过深度变形传播到其他视角，然后利用已训练的多视图扩散模型在编辑区域进行局部重生成，最后通过 SDS 优化更新 NeRF 的局部区域。这一流程复用了生成阶段的全部模块，仅在输入条件上引入了用户指定的局部编辑信号。

### 2.4 训练与推理路径

**训练阶段**仅涉及多视图 ControlNet 的微调：在 MVDream 预训练权重的基础上，使用深度变形后的多视图草图作为条件，以 $\mathcal{L}_{MV-Ctrl}$ 为目标进行训练。训练配置为学习率 $1 \times 10^{-5}$，批大小 64，训练步数 50k，在两块 NVIDIA RTX A6000 GPU 上完成。

**推理阶段**分为两步：（1）给定草图和文本，通过训练好的多视图扩散模型生成四个视角的图像；（2）以这些图像为 2D 先验，通过两阶段 SDS 优化训练 NeRF，最终得到一个可从任意视角渲染的 3D 表示。

### 2.5 关键创新总结

SketchDream 的创新点可归结为三个 changed slots：

1. **深度引导的草图变形**：利用估计的深度图将单视角草图显式地传播到多个目标视角，解决了 2D 草图到多视图条件的歧义问题，这是连接 2D 输入与 3D 生成的关键因果节点；
2. **草图驱动的多视图 ControlNet**：在 MVDream 基础上插入 ControlNet 分支，使多视图扩散模型能够响应草图条件，同时保持多视图一致性；
3. **两阶段 SDS 优化与多损失协同**：粗阶段快速建立几何，细阶段通过引入 2D 扩散损失和多种正则化损失提升细节，形成从结构到纹理的递进式优化路径。

这三个模块之间存在严格的因果依赖：深度变形为 ControlNet 提供了跨视图一致的条件输入，ControlNet 为 SDS 优化提供了可靠的 2D 先验，而两阶段优化则将 2D 先验最终转化为高质量的 3D 内容。

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2405_06461/figures/001_Figure_1.jpg]]
*Figure 1: Our SketchDream system supports both generation and editing of high-quality 3D contents from 2D sketches. As shown in (a), given hand-drawn sketches and text prompts (on top of each example), our method generates high-quality rendering results of 3D contents from scratch. Existing text-to-3D generation approaches like MVDream [Shi et al. 2023b] generate photo-realistic results but cannot control component layouts and details, such as the door and window in the top example and the pose in the bottom example. In (b), we show sketch-based editing results of NeRFs reconstructed from real models. The newly generated components naturally interact with the original objects, with the unedited regio...*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2405_06461/figures/002_Figure_2.jpg]]
*Figure 2: The overview of our SketchDream for sketch-based generation and editing. Given an input sketch ?? and a text prompt ??, we design a sketch-based multi-view diffusion model (a), which takes ??, depth-warped sketch*

## 实验与关键发现

### 实验设置概述

SketchDream 的实验围绕两个核心任务展开：基于草图的 3D 内容生成和基于草图的局部编辑。训练硬件为两块 NVIDIA RTX A6000 GPU。深度生成模型以学习率 1e-5、批大小 64 训练 50k 步。评估采用定量指标与用户调研相结合的方式，重点考察生成/编辑结果的草图保真度、文本一致性和多视角几何合理性。

### 主实验结果

#### 草图驱动的 3D 生成对比

Figure 8 展示了 SketchDream 与现有方法在草图驱动生成任务上的定性对比。对比流程为：对于基线方法，先用 ControlNet（Zhang et al., 2023）从输入草图生成 2D 图像，再将 2D 图像送入各 3D 生成管线。Magic123（Qian et al., 2023）虽能生成逼真结果，但难以保持对输入草图的忠实度；DreamFusion（Poole et al., 2022）和 MVDream（Shi et al., 2023b）在草图一致性上同样表现不佳。SketchDream 通过深度引导的草图变形和 3D ControlNet 的多视角约束，在保持草图几何结构的同时生成高质量 3D 内容。

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2405_06461/figures/008_Figure_8.jpg]]
*Figure 8: Sketch-based generation comparison. For existing approaches, we first utilize ControlNet [Zhang et al. 2023] to generate 2D images and then use these approaches to generate 3D contents from the 2D images. Magic123 [Qian et al. 2023] generates realistic results in the sketch view but has weird geometry in other views. DreamCraft3D [Sun et al. 2023] generates better results in geometry and texture but still has obvious artifacts. With multi-view information, ImageDream [Wang and Shi 2023] generates correct geometry but has too light appearance. In contrast, our method generates better results with correct geometry and realistic appearance*

#### 草图驱动的 3D 编辑对比

Table 2 报告了与 SKED（Mikaeili et al., 2023）在草图编辑任务上的定量对比。评估维度包括四项：文本忠实度（TF）、草图忠实度（SF）、未编辑区域保持（PU）和编辑组件质量（EQ）。SketchDream 在所有四个维度上均优于 SKED。这一优势的核心机制在于：SKED 依赖 2D 扩散模型的编辑能力，缺乏显式的多视角一致性约束，编辑后的 3D 模型在不同视角下容易出现纹理漂移或几何不一致；而 SketchDream 的 sketch-based 多视角扩散模型在编辑过程中同时约束四个正交视角，并通过深度引导的草图变形确保编辑笔触在不同视角间建立正确的空间对应关系。

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2405_06461/figures/013_Table_2.jpg]]
*Table 2: The quantitative comparisons with SKED [Mikaeili et al. 2023] for sketch-based editing. The abbreviations “TF”, “SF”, “PU”, and “EQ” mean text faithfulness, sketch faithfulness, preservation of unedited regions, and editing component quality, respectively. The methods are evaluated in terms of the mean value of the CLIP score and those metrics in the user study. The standard deviation for the CLIP score is also included*

### 关键消融实验

#### 深度引导变形模块的消融

深度引导变形（depth-guided warping）是 SketchDream 建立 2D 草图与 3D 空间之间对应关系的核心模块。消融实验表明：移除深度引导变形、直接将输入草图作为所有视角的条件信号时，生成结果出现严重的多视角不一致——不同视角下的形状轮廓相互矛盾，3D 重建质量显著下降。该模块的因果链路为：输入草图 → 深度估计 → 基于深度和相机参数的视角变形 → 多视角草图条件 → 3D ControlNet 生成多视角一致图像。断裂任一环节都会破坏空间对应关系。

#### 轮廓损失（Silhouette Loss）的消融

公式 $\mathcal{L}_{sil} = \| M_s - C_s^\alpha \|_2^2$ 定义的 2D 轮廓损失在草图视角施加约束，旨在提升生成结果对输入草图轮廓的忠实度。消融结果显示：移除该损失后，生成结果在草图视角的轮廓与输入草图出现可感知偏差，尤其在细粒度几何结构（如动物四肢、物体边缘）上表现明显。该损失作用于 SDS 优化的精细阶段（fine stage），与 3D SDS 损失和 2D ISM 损失协同工作。

#### 精细阶段多损失联合的消融

精细阶段总损失为：

$$\mathcal{L}_{total}^{fine}(\theta) = \beta_1 \mathcal{L}_{SDS}^{3D} + \beta_2 \mathcal{L}_{ISM}^{2D} + \beta_3 \mathcal{L}_{rgb} + \beta_4 \mathcal{L}_{sil} + \beta_5 \mathcal{L}_{orient}$$

其中 $\mathcal{L}_{ISM}^{2D}$ 为 2D 扩散损失，用于提升细节质量。消融实验表明：单独移除 2D 扩散损失会导致生成结果纹理模糊、细节缺失；单独移除轮廓损失会削弱草图一致性；同时移除两者时，3D 内容的质量和草图忠实度均大幅下降。各损失项之间存在互补关系：3D SDS 提供多视角一致性基础，2D ISM 补充高频细节，轮廓损失锚定草图视角的几何约束。

### 失败模式与适用边界

#### 草图质量敏感

SketchDream 对输入草图的质量有一定要求。当手绘草图过于潦草、线条稀疏或结构严重不完整时，深度引导变形模块难以建立可靠的空间对应关系，导致多视角生成结果出现形状坍塌或语义错乱。论文展示的失败案例中，极简线条的草图（如仅用两三笔勾勒的物体）会使生成结果偏离预期几何结构。

#### 复杂拓扑编辑的局限

在局部编辑任务中，当用户的编辑笔触涉及大幅度的拓扑变化（如添加与主体不连通的部件、创建复杂的镂空结构）时，基于深度变形的草图传播可能无法正确处理遮挡关系和新结构的深度排序，导致编辑区域出现几何伪影。此限制源于深度引导变形假设编辑前后的深度结构保持局部连续性。

#### 视角覆盖范围

当前系统的多视角生成覆盖四个均匀分布的水平方位角，对于极端俯仰角下的草图条件缺乏显式建模。当用户期望从大俯角或大仰角观察并编辑 3D 内容时，生成质量可能下降。这一边界条件的根源在于 MVDream 基座模型的训练视角分布。

#### 计算资源需求

SDS 优化过程需要为每个 3D 资产进行迭代优化，生成单个 3D 内容需消耗可观的 GPU 时间和显存（两块 A6000），限制了实时交互式应用场景。编辑任务虽可在已有 3D 模型基础上进行，但仍需完整的优化流程。

### 用户调研验证

论文通过用户调研对生成和编辑结果进行主观评估。调研维度包括：整体质量、草图忠实度、文本一致性和多视角合理性。SketchDream 在所有维度上的用户偏好评分均显著高于基线方法。值得注意的是，在“草图忠实度”维度上的优势最为突出，验证了深度引导变形和轮廓损失设计的有效性。但需注意，用户调研的样本量和受试者背景信息在已有材料中未明确，该结论的统计稳健性需要人工核实。

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2405_06461/figures/012_Table.jpg]]

## 定位与知识库关联

SketchDream 在文本驱动的 3D 内容生成与编辑这一技术脉络中，其核心定位在于**将 2D 手绘草图作为显式的 3D 几何控制信号引入多视图扩散过程**，从而改变了传统 text-to-3D 方法中几何控制缺失或仅依赖文本模糊描述的格局。相对于已有工作，SketchDream 改变的 slot 是**条件信号的模态与空间对齐方式**：它将原本仅由文本提示（text prompt）驱动的多视图生成，替换为“文本 + 深度引导的草图多视图条件”联合驱动。

### 相对于已有方法的本质差异

**相对于单视图 sketch-to-3D 方法**（如 Sketch2Model 等），SketchDream 不依赖单视图的形状先验假设，而是通过多视图扩散模型在生成阶段就建立跨视角的 3D 一致性。这避免了单视图方法在不可见区域出现几何歧义的根本缺陷。

**相对于 MVDream**（Shi et al., 2023）这一直接基座，SketchDream 的增量在于：在 MVDream 的多视图扩散框架上插入了一个 **3D ControlNet** 模块，并设计了**深度引导的草图变形（depth-guided warping）策略**来显式建立输入草图与目标多视图之间的空间对应关系。MVDream 本身仅接受文本和相机参数作为条件，无法处理草图的几何约束；SketchDream 将草图条件 $s$ 通过 ControlNet 注入 UNet 去噪过程，使生成的多视图图像在几何上忠实于输入草图，同时保持文本控制的外观灵活性。这一改变的本质是**将 2D 草图的几何信息通过深度图显式地映射到 3D 空间**，而非像 ControlNet（Zhang et al., ICCV 2023）那样仅在 2D 域内做条件控制。

**相对于 DreamEditor** 和 **SKED** 等 3D 编辑方法，SketchDream 的差异在于编辑接口的设计：DreamEditor 和 SKED 通常依赖文本描述或 3D 操作（如变形、雕刻）来编辑局部区域，而 SketchDream 允许用户在任意视点下通过修改 2D 草图并配合文本提示来实现局部编辑。其编辑流程的关键在于：从原始 3D 模型渲染图像并提取草图，用户修改草图后，通过深度引导的变形将修改后的草图传播到其他视图，再驱动 SDS 优化更新 3D 表示。这使得编辑操作保持了跨视图的几何一致性，而非仅在单个视点生效。

### 知识库挂载点

SketchDream 可挂载到知识库中的以下技术节点：

1. **多视图扩散模型**（Multi-view Diffusion）：直接继承 MVDream 的多视图生成能力，挂载点为“多视图一致性的扩散先验”。
2. **3D ControlNet**：将 2D ControlNet 的受控生成思想扩展到多视图场景，挂载点为“条件扩散模型的空间控制机制”。
3. **Score Distillation Sampling（SDS）**：3D 生成阶段沿用 SDS 优化范式（Poole et al., 2022），并引入 $x_0$-reconstruction 变体以缓解色彩饱和问题，挂载点为“基于扩散先验的 3D 蒸馏优化”。
4. **深度引导的跨视图变形**：利用生成的深度图建立 2D 草图到 3D 空间的映射，挂载点为“深度估计辅助的 2D-3D 对应关系建立”。

### 适用边界

SketchDream 的有效性依赖于以下前提条件，这些也构成了其适用边界：

- **草图质量与深度估计精度**：深度引导的变形策略要求草图对应的深度图具有合理的准确性。对于复杂遮挡或深度歧义严重的区域，变形可能引入几何失真。论文未提供深度估计失败时的定量分析，这一点需要人工验证。
- **多视图一致性的上限**：由于基座 MVDream 本身在极端视角或复杂几何下可能出现多视图不一致，SketchDream 的生成质量受限于该基座的能力天花板。
- **编辑范围**：局部编辑依赖用户提供的 mask 和修改后的草图。对于大幅度的拓扑变化（如增加或删除完整的部件），方法可能难以保持 3D 一致性，因为深度变形无法处理拓扑改变。
- **计算开销**：训练 3D ControlNet 需要 50k 步，3D 生成和编辑均需 SDS 优化，整体流程对 GPU 资源要求较高（使用两张 NVIDIA RTX A6000）。

### 后续启发

SketchDream 为后续研究提供了以下方向性启发：

1. **多模态条件融合的 3D 生成范式**：将草图作为几何模态、文本作为外观模态的解耦控制思路，可推广到手绘线条、边缘图、深度图等其他几何描述形式，形成更通用的多模态 3D 生成框架。
2. **跨视图编辑的一致性传播**：深度引导的变形策略为 3D 编辑中的视图间一致性传播提供了一种可复用的技术方案，可被其他基于扩散先验的 3D 编辑方法借鉴。
3. **2D 草图接口的实用化**：该方法降低了 3D 内容创作的门槛，使得非专业用户可以通过手绘草图参与 3D 资产生成，为交互式 3D 建模工具的设计提供了技术参考。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/SketchDream_Sketch_based_Text_to_3D_Generation_and_Editing.pdf]]