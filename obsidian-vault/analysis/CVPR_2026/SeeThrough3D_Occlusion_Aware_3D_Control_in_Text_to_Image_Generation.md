---
title: "SeeThrough3D: Occlusion Aware 3D Control in Text-to-Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SeeThrough3D_Occlusion_Aware_3D_Control_in_Text_to_Image_Generation.pdf
project_link: "https://seethrough3d.github.io"
code_link: null
aliases:
- SeeThrough3D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 提出遮挡感知的3D场景表示（OSCR），使用半透明且面片颜色编码的3D边界框表现物体，渲染后作为生成模型的条件输入，从而显式编码遮挡区域和朝向信息。
primary_logic: 半透明渲染使被遮挡区域仍然部分可见，为模型提供遮挡推理线索；同时通过掩码注意力将每个边界框内的条件token与对应文本描述绑定，在免分类器的情况下实现精确的多物体布局控制和属性解耦，并利用预训练文生图模型的先验来生成自然外观。
claims:
- 在3DOc-Bench上，SeeThrough3D在所有指标上显著优于基线：深度排序1.46（最佳基线LaRender为1.02），物体得分22.86（LaRender 21.83），角度误差47.92（LaRender 89.63），文本对齐31.87（LaRender 30.20），KID 5.43×10⁻³（LaRender 13.46）
- 消融实验证实，移除半透明渲染导致深度排序降至1.20；移除颜色编码使角度误差飙升至88.77；移除注意力绑定使深度排序降至0.98，物体得分降至20.45
- 注意力可视化显示，模型内部的注意力图清晰地揭示了遮挡边界，被遮挡物体的特征在遮挡物空隙中仍然活跃，表明模型在潜在空间中实现了物体特征解耦
- 3DOc-Bench 上 深度排序（depth ordering↑） = 1.46
---

# SeeThrough3D: Occlusion Aware 3D Control in Text-to-Image Generation

> [!tip] 核心洞察
> 半透明渲染使被遮挡区域仍然部分可见，为模型提供遮挡推理线索；同时通过掩码注意力将每个边界框内的条件token与对应文本描述绑定，在免分类器的情况下实现精确的多物体布局控制和属性解耦，并利用预训练文生图模型的先验来生成自然外观。

| 字段 | 内容 |
|------|------|
| 中文题名 | SeeThrough3D：面向文本到图像生成的遮挡感知三维控制 |
| 英文题名 | SeeThrough3D: Occlusion Aware 3D Control in Text-to-Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.23359) · [Project](https://seethrough3d.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | SeeThrough3D |
| Dataset | 3DOc-Bench |

> [!tip] 效果简介
> - 3DOc-Bench 上，深度排序（depth ordering↑） 1.46 vs 1.02 (LaRender) (+0.44)；物体得分（obj. score↑） 22.86 vs 21.83 (LaRender) (+1.03)；角度误差（angular err.↓） 47.92 vs 89.63 (LaRender) (-41.71)。

## 概述

在文本到图像生成中，实现精确的三维场景布局控制——尤其是多物体遮挡关系下的深度一致性与朝向正确性——仍是一个未解决的挑战。现有方法或依赖深度图表示三维布局（如 **LooseControl**，Bhat et al., SIGGRAPH 2024），或采用二维物体分层表示（如 **LaRender**、**VODiff**），前者无法在被遮挡区域保留物体信息，后者缺乏三维感知能力，导致遮挡关系错误和几何不一致。

SeeThrough3D 针对这一瓶颈，提出了**遮挡感知三维场景表示（OSCR）**：将物体描述为半透明且面片颜色编码的三维边界框，从指定相机视角渲染后作为条件输入生成模型。半透明特性使被遮挡区域仍部分可见，为模型提供遮挡推理线索；颜色编码则传递物体朝向信息。在此基础上，通过**注意力掩码机制**将每个边界框内的条件 token 与对应文本描述绑定，在无需额外分类器的情况下实现精确的多物体布局控制与属性解耦。

方法以预训练的文生图模型 FLUX 为基座，仅在新增 OSCR token 的注意力投影矩阵上注入 LoRA 进行微调，同时阻塞 OSCR token 到图像 token 的注意力，从而保留基座模型的生成先验。

在专门构建的遮挡场景评测基准 **3DOc-Bench** 上，SeeThrough3D 在所有指标上显著超越基线方法：深度排序达 **1.46**（最佳基线 LaRender 为 1.02），角度误差降至 **47.92**（LaRender 为 89.63），图像质量指标 KID 为 **5.43×10⁻³**（LaRender 为 13.46）。消融实验证实，半透明渲染、颜色编码和注意力绑定三者对最终性能均不可或缺。注意力可视化进一步揭示，模型潜在空间中的物体特征呈现解耦状态，被遮挡物体的特征在遮挡物空隙中仍保持活跃，表明模型习得了遮挡推理的能力。

## 背景与动机

### 文本到图像生成中的空间控制困境

近年来，基于扩散模型和流匹配的文本到图像生成取得了显著进展，能够根据自然语言描述生成高质量、高保真的图像。然而，当场景涉及多个物体且存在复杂的空间关系时，仅依赖文本提示难以精确控制物体的三维位置、朝向和相互遮挡关系。用户往往需要反复调整提示词才能获得大致符合预期的布局，这种“盲调”方式效率低下且缺乏可复现性。

这一困境催生了三维布局条件生成的研究方向——在生成过程中引入显式的三维场景描述作为条件信号，使模型能够按照用户指定的空间配置生成图像。

### 现有方法的两个核心缺口

当前的三维布局控制方法主要沿两条技术路线展开，但各自存在根本性局限：

**深度图方法的“不可见”困境。** 以 **LooseControl**（Bhat et al., SIGGRAPH 2024）和 **Build-A-Scene** 为代表的方法将场景编码为深度图，通过深度信息约束物体的空间位置。然而，深度图本质上是二维投影，当物体A遮挡物体B时，B在深度图中完全不可见，模型无从获知被遮挡物体的存在、形状和语义信息。这导致生成结果中遮挡关系混乱——被遮挡的物体可能消失、变形，或错误地出现在遮挡物前方。

**分层方法的“非三维”局限。** 另一类方法如 **LaRender** 和 **VODiff** 将场景分解为物体图层，逐层生成后再合成。这种策略虽然保留了被遮挡物体的信息，但图层操作在二维空间中进行，缺乏对相机视角和透视投影的建模能力。当用户改变观察角度时，图层间的空间关系无法自动适应，生成的遮挡边界与真实三维几何不一致。

简而言之，深度图方法丢失了被遮挡物体的信息，而分层方法丢失了三维空间感知能力——两种方案都无法在复杂多物体场景中同时保证深度一致性、尺度正确性和遮挡合理性。

### 遮挡：被忽视的核心挑战

上述缺口的共同根源在于对**遮挡**这一三维场景基本现象的显式建模缺失。在真实世界中，遮挡并非简单的“前面挡住后面”，而是涉及：

- **部分可见性**：被遮挡物体的可见区域与遮挡物的空隙结构密切相关（例如透过自行车轮辐看到后面的汽车）。
- **朝向依赖**：物体的遮挡模式随相机视角变化而改变。
- **深度排序**：多个物体重叠时，正确的遮挡层级关系是场景几何一致性的基础。

现有方法缺乏对遮挡区域的推理线索，导致模型在生成过程中“猜测”遮挡关系，这在强遮挡场景下几乎必然失败。因此，设计一种能够显式编码遮挡信息、同时保留三维空间感知能力的场景表征，成为突破当前瓶颈的关键。

### SeeThrough3D 的动机与切入点

针对上述问题，SeeThrough3D 提出一个直接而核心的洞察：**如果让被遮挡区域在条件信号中仍然部分可见，模型就能获得遮挡推理的线索，从而在生成过程中自主建立正确的空间关系。** 这一思想源于对人类视觉系统的观察——即使物体被部分遮挡，我们仍能通过可见的片段推断其完整形态和空间位置。

为实现这一目标，SeeThrough3D 设计了**遮挡感知三维场景表征（Occlusion-Aware Scene Representation, OSCR）**，其核心创新在于：

1. **半透明渲染**：将物体表示为半透明的三维边界框，使被遮挡物体透过遮挡物仍然可见，为模型提供遮挡区域的连续视觉线索。
2. **面片颜色编码**：用规范化的颜色映射编码每个边界框面的三维朝向，使模型能够推断物体的空间姿态。
3. **注意力绑定机制**：通过掩码注意力将每个边界框对应的条件token与描述该物体的文本token精确关联，实现免分类器的多物体属性解耦。

这一设计使SeeThrough3D能够在保持预训练文生图模型生成质量的前提下，实现对复杂多物体场景中遮挡关系、物体朝向和相机视角的精确控制。

## 核心创新

SeeThrough3D 的核心创新在于首次将**遮挡感知**引入文本到图像的3D布局控制，解决了现有方法在复杂多物体场景中因缺乏显式遮挡建模而导致的深度不一致与几何错误。其创新围绕三个紧密耦合的“changed slots”展开，形成一个从场景表示到条件注入再到特征绑定的完整闭环。

**1. 遮挡感知场景表示（OSCR）——从深度图到半透明颜色编码边界框**

现有3D布局控制方法（如 **LooseControl** (Bhat et al., SIGGRAPH 2024)）依赖深度图作为条件输入，但深度图在遮挡区域仅保留前景信息，被遮挡物体完全不可见，模型无从推断其存在与深度关系（Figure 3）。SeeThrough3D 提出 **OSCR（Occlusion-Aware Scene Representation）**，将场景中的每个物体表示为一个**半透明且面片颜色编码的3D边界框**，从用户指定的相机视角渲染为2D条件图。半透明渲染使被遮挡物体仍部分可见，为生成模型提供了遮挡推理的直接线索；颜色编码面片（如红、绿、蓝对应不同朝向）则将3D朝向信息显式注入条件信号。这一表示上的根本转变，使得模型无需从隐式深度图中猜测遮挡关系，而是从条件信号中直接“看到”物体的空间排序与朝向。

**2. 条件注入与微调策略——以最小侵入方式利用预训练先验**

SeeThrough3D 将OSCR渲染图通过VAE编码为视觉token，与文本token和噪声图像token拼接后送入预训练的基于DiT的文生图模型（FLUX）。与全参数微调或Adapter方案不同，该方法仅在**新增OSCR token对应的注意力投影矩阵上注入LoRA**，并阻塞OSCR token到图像token的注意力路径（Figure 4）。这一策略的关键优势在于：LoRA的低秩更新仅作用于条件token的处理路径，最大限度地保留了基座模型原有的图像生成先验，使得模型既能响应3D布局控制，又能维持自然外观生成、透明物体渲染、文字生成等原有能力（Figure 8）。

**3. 基于注意力掩码的对象-文本绑定——无分类器的精确布局解耦**

现有基于深度图的方法缺乏对象与文本描述之间的显式绑定机制，导致多物体场景中属性混淆和布局错位。SeeThrough3D 利用OSCR渲染过程中天然可得的各物体amodal分割掩码，在mmDiT块的自注意力计算中施加**结构化注意力掩码**：每个边界框内的OSCR token仅被允许关注其对应物体的文本token，重叠区域则关注多个相关物体（Figure 5）。这一机制在无需额外分类器或损失函数的情况下，实现了对象级别的特征解耦。注意力可视化（Figure 6）证实，模型潜在空间中物体特征保持独立，被遮挡物体的注意力在遮挡物空隙中仍然活跃，精确反映了遮挡边界——这表明模型在潜在空间中自发形成了遮挡推理的强先验。

三个创新点之间存在因果依赖：OSCR的半透明与颜色编码提供了遮挡和朝向的原始信号，注意力掩码绑定确保了这些信号与正确文本描述的对应关系，而LoRA微调策略则保证了条件控制与生成质量之间的平衡。消融实验（Table 2）为这一因果链提供了定量支撑：移除半透明渲染使深度排序从1.46降至1.20；移除颜色编码使角度误差从47.92飙升至88.77，回到基线水平；移除注意力绑定则使深度排序骤降至0.98，物体得分从22.86跌至20.45，生成图像中对象出现明显错位。

## 整体框架

SeeThrough3D 的整体 pipeline 围绕一个核心设计展开：**将遮挡感知的三维场景表征（OSCR）作为条件信号注入预训练的文生图扩散模型**，使模型在生成过程中显式推理物体间的遮挡关系、三维朝向和深度排序。

### 输入与条件构造

用户通过交互式图形界面指定场景中的三维边界框 $\{b_i\}$ 和期望的相机视角 $C$（见 Figure 2）。每个边界框被赋予半透明材质，且六个面片采用规范化的颜色编码——每个面的颜色唯一映射到其三维朝向。这一设计使得渲染后的 OSCR 图像 $r$ 同时编码了三类信息：**物体空间位置**（边界框的投影形状）、**遮挡关系**（半透明使被遮挡区域仍部分可见）、以及**三维朝向**（面片颜色编码）。相比现有方法中仅使用深度图（丢失遮挡信息）或二维图层（丢失三维感知）的表征方式，OSCR 在信息密度和遮挡推理线索上具有根本性优势。

![[assets/figures/papers/paper_list_l2176_https_arxiv_org_abs_2602_23359/figures/002_Figure_2.jpg]]
*Figure 2: OSCR: We propose Occlusion-Aware Scene Representation (OSCR) for 3D layout control in text-to-image generation. OSCR describes objects as translucent 3D boxes, which exposes occluded regions, enabling the generative model to reason about occlusions. Further, each box face is color-coded with a mapping to encode its 3D orientation. (a) A user specifies the object bounding boxes (b0 and*

![[assets/figures/papers/paper_list_l2176_https_arxiv_org_abs_2602_23359/figures/023_Figure.jpg]]
*Figure: 2*

### 条件注入与模型架构

渲染得到的 OSCR 图像 $r$ 经 VAE 编码器转换为潜在 token $z$，与文本提示 token $p$ 和噪声图像 token $x_t$ 拼接后，送入基于 DiT（Diffusion Transformer）架构的文生图模型（见 Figure 4）。模型内部的 mmDiT 块通过自注意力机制联合处理三类 token，使 OSCR 的空间结构信息与文本语义、图像特征在潜在空间中交互。

![[assets/figures/papers/paper_list_l2176_https_arxiv_org_abs_2602_23359/figures/004_Figure_4.jpg]]
*Figure 4: SeeThrough3D: We encode the rendered OSCR condition map r using the VAE to obtain OSCR tokens. These are concatenated with text prompt tokens p and noisy image tokens xt. The concatenated result is passed through the DiT based text-toimage model where they are jointly processed using self attention modules. We inject LoRA [25] onto the attention projections corresponding to OSCR tokens; this enables control while preserving prior of the base model [61, 62, 79]*

为在引入新条件信号的同时保留基座模型的生成先验，SeeThrough3D 采用**轻量级微调策略**：仅对 OSCR token 对应的注意力投影矩阵注入 LoRA 低秩适配器，而不修改基座模型的其他参数。同时，OSCR token 到图像 token 的注意力被阻塞，迫使条件信息通过文本-OSCR 交互路径传递，避免对图像特征空间的直接干扰。

### 对象-文本绑定机制

多物体场景的核心挑战在于将每个边界框的条件信号与对应的文本描述精确绑定。SeeThrough3D 引入**基于注意力掩码的绑定机制**（见 Figure 5）：利用每个物体边界框的 amodal 分割掩码 $s_i$，限制 OSCR token 仅关注其对应物体的文本 token $\{p_i\}$。当多个边界框重叠时，重叠区域的 OSCR token 可同时关注多个物体的文本描述。这一设计在无需额外分类器或交叉注意力模块的前提下，实现了对象级别的条件解耦，使模型能够独立控制每个物体的外观、位置和遮挡关系。

### 数据与训练策略

训练数据通过 Blender 中的受控场景配置生成（见 Figure 7）：在确保强遮挡的同时保持每个物体的充分可见性，经深度估计和深度到图像的生成模型增强后，构建富含遮挡场景的训练集。训练过程中，困难样本（高遮挡场景）被显式保留，消融实验证实移除这些样本会导致所有指标下降，表明数据策略对模型遮挡推理能力的培养至关重要。

### 推理流程

推理时，用户指定边界框布局、相机视角和文本提示，系统渲染 OSCR 图像并编码为 token，经 LoRA 增强的 DiT 模型在注意力掩码的约束下执行去噪生成，最终输出符合三维布局、遮挡关系正确且物体朝向一致的图像。该 pipeline 支持扩展至个性化生成：通过将参考图像经 VAE 编码为外观 token，并使其在对应分割掩码区域内与 OSCR token 交互，可实现基于参考图像的三维控制生成（见 Figure 11）。

## 核心模块与公式推导

SeeThrough3D 的架构围绕三个关键模块构建，分别解决遮挡感知场景表示、条件注入与对象绑定三个核心问题。

**OSCR 渲染器（Occlusion-Aware Scene Representation）**

该模块是方法的核心创新。用户在交互式图形环境中指定物体的 3D 边界框 $\{b_i\}$ 和目标相机视角 $C$，渲染器将每个边界框渲染为半透明且面片颜色编码的图像 $r$（见 Figure 2）。半透明渲染使被遮挡区域仍然部分可见，为生成模型提供遮挡推理线索；每个面片的颜色由其在规范坐标系中的朝向决定，从而显式编码物体的 3D 朝向信息。这一设计与现有方法形成鲜明对比：基于深度图的布局表示（如 **LooseControl**, Bhat et al., SIGGRAPH 2024）无法表示被遮挡物体，而基于物体层的表示（如 **LaRender**、**VODiff**）缺乏 3D 感知能力，无法捕捉相机视角和透视关系（见 Figure 3）。

![[assets/figures/papers/paper_list_l2176_https_arxiv_org_abs_2602_23359/figures/003_Figure_3.jpg]]
*Figure 3: Towards occlusion aware 3D scene layouts: existing methods represent scenes as (a) 3D layout depth maps [4, 19, 65], which fail to represent occluded objects (see dashed red box), or (b) object layers [37, 76], which are not 3D aware, hence fail to capture camera viewpoint and perspective. (c) Therefore, we propose OSCR, where objects are described using translucent 3D bounding boxes. The transparency exposes occluded regions (red box), providing cues for occlusion reasoning, while enabling 3D layout control*

**条件注入机制（mmDiT + LoRA）**

OSCR 渲染图 $r$ 首先通过预训练的 VAE 编码器转换为潜在 token $z$，然后与文本提示 token $p$ 和噪声图像 token $x_t$ 拼接，共同输入基于 DiT 的文生图模型（见 Figure 4）。为在注入 3D 布局控制能力的同时保留基座模型（FLUX）的先验，方法仅在新增 OSCR token 对应的注意力投影矩阵上注入 LoRA，并阻塞 OSCR token 到图像 token 的注意力通路。这种轻量级微调策略避免了全参数微调对预训练先验的破坏。

**注意力掩码绑定模块**

为实现精确的多物体布局控制，方法利用每个边界框的 amodal 分割掩码 $s_i$ 构建注意力掩码 $M$（见 Figure 5）。在 mmDiT 块的自注意力计算中，掩码 $M$ 强制每个边界框 $b_i$ 内的 OSCR token 仅关注对应物体的文本 token $\{p_i\}$。当多个边界框重叠时，交集区域的 token 可同时关注多个对应物体的文本描述。这一机制在无需额外分类器的情况下实现了对象-文本的精确绑定，是保证复杂遮挡场景中布局遵循性的关键。

![[assets/figures/papers/paper_list_l2176_https_arxiv_org_abs_2602_23359/figures/005_Figure_5.jpg]]
*Figure 5: (a) Inside the mmDiT block, text tokens p, image tokens*

**个性化扩展的注意力机制**

在个性化场景中，参考图像 $v$ 通过 VAE 编码器转换为外观 token $v$，并与 OSCR token 和文本 token 一同输入模型。OSCR token 在分割掩码 $s_i$ 范围内同时关注外观 token 和对应文本 token，从而将物体外观绑定到其 3D 边界框上。

### 补充图表

![[assets/figures/papers/paper_list_l2176_https_arxiv_org_abs_2602_23359/figures/007_Figure_6.jpg]]
*Figure 6: Visualizing object disentanglement in latent space: Given a layout with heavy occlusion like (a), our model’s outputs show precise occlusion boundaries (b). To understand this, we visualize attention from image-tokens to object tokens in prompt (bicycle and van). Interestingly, the attention maps themselves reveal occlusion boundaries: inside the empty regions of the bicycle structure, attention on the van remains visible, accurately reflecting its presence behind the bicycle. This suggests that objectspecific features remain distinct in the model’s latent space, indicating strong priors for occlusion reasoning*

## 实验与分析

### 核心定量结果

SeeThrough3D 在专门构建的遮挡感知基准 **3DOc-Bench** 上全面超越现有方法。该基准系统评估深度排序、物体保真度、朝向正确性、文本对齐和图像质量五个维度，结果汇总于 Table 1。

![[assets/figures/papers/paper_list_l2176_https_arxiv_org_abs_2602_23359/figures/010_Table_1.jpg]]
*Table 1: Quantitative comparison: We compute (a) depth ordering, which reflects 3D location and occlusion consistency, (b) CLIP objectness score, which indicates layout adherence and object fidelity (c) angular error, which indicates orientation correctness (d) image-text prompt alignment using CLIP [56], and (e) KID [5], which measures image fidelity*

**深度排序（Depth Ordering ↑）**：SeeThrough3D 取得 1.46，相较最强基线 LaRender 的 1.02 提升 **+0.44**。这一指标的实质含义是：模型生成的图像中，物体间的遮挡关系与输入 3D 布局的一致性。深度排序接近满分（上限约为场景中物体对数），表明 OSCR 的半透明渲染成功为模型提供了遮挡推理所需的深度线索。

**物体得分（Object Score ↑）**：22.86 vs. LaRender 的 21.83（+1.03）。该指标基于 CLIP 在检测到的物体掩码上的置信度，衡量生成物体与文本描述的匹配程度以及布局遵循度。提升虽相对温和，但结合注意力绑定消融实验（移除绑定后骤降至 20.45）来看，注意力掩码机制对确保物体出现在正确位置起到了关键作用。

**角度误差（Angular Error ↓）**：47.92 vs. LaRender 的 89.63，**降低 41.71**，降幅达 46.5%。这是所有指标中优势最显著的一项。LaRender 仅依赖深度图，缺乏朝向信息，其角度误差接近随机水平；而 OSCR 的面片颜色编码（每个面映射到规范颜色）直接为模型提供了 3D 朝向信号，使生成物体的朝向与布局指定高度一致。这一结果直接验证了颜色编码设计的有效性。

**文本对齐（Text Alignment ↑）**：31.87 vs. 30.20（+1.67），表明方法在引入强 3D 条件的同时，并未显著损害基座模型 FLUX 的文本遵循能力。KID（×10⁻³ ↓）：5.43 vs. 13.46（-8.03），图像质量大幅领先，说明半透明渲染和 LoRA 注入策略有效保留了预训练先验，避免了条件控制导致的图像退化。

### 消融实验：设计要素的因果验证

Table 2 和 Figure 12 系统拆解了 OSCR 表征、注意力绑定和数据策略的贡献，每一项移除都导致特定维度的性能退化，形成清晰的因果链条。

![[assets/figures/papers/paper_list_l2176_https_arxiv_org_abs_2602_23359/figures/011_Table_2.jpg]]
*Table 2: Quantitative results of ablative experiments*

| 消融变体 | 深度排序 ↑ | 物体得分 ↑ | 角度误差 ↓ | 文本对齐 ↑ | KID ↓ |
|---------|-----------|-----------|-----------|-----------|-------|
| SeeThrough3D（完整） | 1.46 | 22.86 | 47.92 | 31.87 | 5.43 |
| w/o transparency | 1.20 | 21.67 | 46.15 | 31.39 | 5.90 |
| w/o color-coding | 1.36 | 22.23 | **88.77** | 31.57 | 5.93 |
| w/o binding | **0.98** | **20.45** | 57.44 | 31.61 | 6.35 |
| w/o hard data | — | — | — | — | — |

**移除半透明渲染（w/o transparency）** 使深度排序从 1.46 降至 1.20。当边界框变为不透明时，被遮挡物体的区域完全不可见，模型失去推断遮挡关系的视觉线索。有趣的是，角度误差反而略微下降（46.15），这与论文观察一致：不透明框提供了更清晰的颜色信号，有利于朝向判断，但代价是深度推理能力退化。这揭示了透明性与朝向编码之间存在微妙的权衡。

**移除面片颜色编码（w/o color-coding）** 导致角度误差飙升至 88.77，几乎回到 LaRender 的水平（89.63），而其他指标仅轻微下降。这一“选择性崩溃”强有力地证明：颜色编码是朝向控制的核心机制，而非泛化的条件增强。没有颜色编码时，模型无法从渲染图中提取朝向信息，只能依赖文本提示中的隐含朝向先验。

**移除注意力绑定（w/o binding）** 造成深度排序和物体得分的双重崩塌（0.98 和 20.45）。定性结果（Figure 12）显示，物体出现在错误位置或与错误文本描述关联。这证实了基于 amodal 分割掩码的注意力掩码是实现精确多物体布局控制的必要条件——没有它，OSCR token 与文本 token 之间的对应关系是模糊的，模型无法将“自行车”和“货车”的语义分别绑定到各自的边界框。

**移除困难样本过滤（w/o hard data）** 导致所有指标下降。该消融针对数据策略：训练时若过滤掉强遮挡场景，模型在测试时的遮挡推理能力显著减弱。这反向说明了数据集中保留高遮挡配置对学习遮挡感知表征的重要性。

### 注意力可视化揭示的潜在空间解耦

Figure 6 提供了理解模型内部工作机制的关键证据。在一个自行车严重遮挡货车的场景中，模型输出精确的遮挡边界。更关键的是，从图像 token 到文本 token（“bicycle”和“van”）的注意力图本身揭示了遮挡边界：在自行车结构的空隙区域，对“van”的注意力仍然活跃，准确反映了货车在自行车后方的存在。

这一现象的意义超越了定性展示——它表明模型在潜在空间中实现了物体特征的解耦。即使被遮挡物体的像素级信息在图像空间中不可见，其语义特征在 transformer 的注意力空间中依然保持独立且可寻址。这意味着预训练文生图模型（FLUX）本身具备一定的遮挡推理先验，而 OSCR 的半透明渲染充当了“触发器”，将这些先验引导到正确的 3D 布局约束中。

### 用户偏好与定性对比

用户调查（Figure 10）显示，在遮挡一致性、布局遵循、物体保真度和朝向正确性四个维度上，SeeThrough3D 的输出被偏好的比例均显著高于各基线方法。与 LaRender 和 VODiff 的定性对比（Figure 9）进一步表明，仅基于深度图或图层的方法在复杂遮挡场景中频繁出现物体融合、深度错乱和朝向错误，而 SeeThrough3D 在这些场景中保持了清晰的遮挡边界和正确的空间关系。

![[assets/figures/papers/paper_list_l2176_https_arxiv_org_abs_2602_23359/figures/009_Figure_9.jpg]]
*Figure 9: Qualitative comparison: We compare against works on 3D layout control: LooseControl [4] and Build-A-Scene [19], and on occlusion control: LaRender [76] and VODiff [37]*

![[assets/figures/papers/paper_list_l2176_https_arxiv_org_abs_2602_23359/figures/013_Figure_10.jpg]]
*Figure 10: User study: Each bar indicates the % of times our method’s output was preferred over the baseline, for each category*

### 已知失败模式

论文明确指出了方法的局限性。首先，**布局变化时无法保持图像内容一致性**——修改 3D 布局后重新生成，图像中物体的外观和背景可能完全不同，这限制了其在迭代式场景编辑中的应用。其次，**受基座模型 FLUX 的能力上限约束**，对于某些极端遮挡或非典型配置（例如笼子后的鹦鹉），模型可能无法生成合理结果。最后，**个性化扩展存在显存瓶颈**：当使用参考图像定制物体外观时，所有外观 token 需保留在 transformer 上下文中，多物体个性化场景下显存开销较高。

### 评估的公平性考量

为公平比较，论文对基线方法做了两项重要处理：（1）将 LooseControl 在相同数据集上重新训练，并用其检查点评估 Build-A-Scene（后者依赖前者）；（2）在计算角度误差时采用宽松版本，将 180° 翻转不计为错误，以允许仅依赖深度图的方法（如 LooseControl）公平参与对比。这一处理确保了性能差异归因于方法本身，而非数据分布或评估标准的不对等。

### 补充图表

![[assets/figures/papers/paper_list_l2176_https_arxiv_org_abs_2602_23359/figures/006_Figure_7.jpg]]
*Figure 7: Dataset creation: We place 3D assets in controlled configurations in Blender [12]. Object placements and camera viewpoint are controlled to ensure strong occlusions, while ensuring adequate visibility for each object. To generate realistic augmentations, we estimate image depth, and pass it through a depth-toimage model [35] with diverse background prompts*

![[assets/figures/papers/paper_list_l2176_https_arxiv_org_abs_2602_23359/figures/012_Figure_11.jpg]]
*Figure 11: Personalization: Our method can be extended for personalized 3D control using reference image of an object*

## 方法谱系与知识库定位

### 1. 方法在领域中的定位

SeeThrough3D 处于文本到图像生成中**三维场景布局控制**与**遮挡感知生成**的交叉点。现有工作可沿两条轴线划分：

**轴线一：3D布局控制。** 代表方法如 **LooseControl**（Bhat et al., SIGGRAPH 2024）和 **Build-A-Scene**，通过深度图等条件信号约束生成图像的三维空间结构。这类方法的根本局限在于深度图本质上是2.5D表示——它只能编码可见表面的深度值，被遮挡物体的空间信息完全丢失（见 Figure 3 红色虚线框标注区域）。当场景中存在多个物体且发生严重遮挡时，模型缺乏对被遮挡区域的推理线索，导致深度排序错误和物体错位。

**轴线二：遮挡控制。** 代表方法如 **LaRender** 和 **VODiff**，通过分层表示或对象级布局处理遮挡关系。然而这些方法不具三维感知能力——它们无法捕捉相机视角和透视投影下的空间关系，因此难以实现视角一致的遮挡推理。

SeeThrough3D 的方法论突破在于**将上述两条轴线统一到单一表示框架中**：通过 OSCR（Occlusion-Aware Scene Representation）——半透明且颜色编码的三维边界框渲染图——同时编码三维空间布局和被遮挡区域的线索，使预训练文生图模型能够在潜在空间中自主推理遮挡关系。

### 2. 核心设计决策的因果链条

SeeThrough3D 的性能优势源于三个相互耦合的设计选择，消融实验（Table 2, Figure 12）揭示了其因果贡献：

**半透明渲染 → 深度排序能力。** 移除透明度后，深度排序从 1.46 降至 1.20，物体得分从 22.86 降至 21.67。半透明使被遮挡物体仍部分可见，为模型提供了推断相对深度的视觉线索。注意力可视化（Figure 6）进一步证实：在自行车车架空隙处，模型对“面包车”文本token的注意力仍然活跃，表明被遮挡物体的特征在潜在空间中保持独立，模型实质上实现了隐式的物体特征解耦。

**面片颜色编码 → 朝向控制精度。** 移除颜色编码后，角度误差从 47.92 飙升至 88.77，几乎退回到基线水平。每个边界框的六个面被赋予规范颜色映射，使模型能够从渲染图中直接读取物体的三维朝向信息，而无需依赖深度图的间接推断。

**掩码注意力绑定 → 布局遵循度。** 移除注意力绑定后，深度排序骤降至 0.98，物体得分降至 20.45。该机制利用物体的amodal分割掩码，限制每个边界框内的OSCR token仅关注对应物体的文本token，在免分类器的情况下实现了精确的多物体布局控制和属性解耦。当多个边界框重叠时，交集区域允许同时关注多个物体，自然处理遮挡区域的语义归属。

### 3. 适用边界与能力约束

**基座模型能力天花板。** SeeThrough3D 建立在 FLUX 预训练文生图模型之上，其生成质量的上限受基座模型先验约束。论文明确指出，对于某些极端遮挡或非典型物体配置（如“笼子后的鹦鹉”），模型可能失败——这并非方法本身的缺陷，而是基座模型对罕见空间关系的先验知识不足。

**布局变化的一致性缺失。** 当前方法在给定固定布局时生成质量优异，但无法在布局变化时保持图像内容一致性。这是一个明确的能力边界：SeeThrough3D 是“布局条件生成”方法，而非“布局编辑”方法。论文将此列为未来方向，建议结合编辑方法解决。

**个性化扩展的资源瓶颈。** 当拓展到多物体个性化生成时（Section 3.5），所有参考图像的appearance token需保留在transformer上下文中，导致显存开销随物体数量线性增长。这是注意力绑定机制在个性化场景下的直接代价。

**训练数据分布限制。** 模型训练时使用的布局最多包含4个物体，但推理时展现出对更复杂场景（Figure 8 G-J）的泛化能力。这种泛化源于预训练模型的组合先验，而非训练数据的覆盖，因此在物体数量远超训练分布时，性能可能不可预期地退化。

### 4. 开放问题与未来方向

1. **布局编辑与内容保持。** 如何在保持场景中未修改区域外观一致的前提下，仅改变特定物体的位置或朝向？这需要将当前的条件生成框架与图像编辑技术（如注意力注入或特征混合）结合。

2. **个性化效率优化。** 能否通过模型压缩、特征缓存或检索增强的方式降低多物体个性化的计算开销？当前每增加一个个性化物体即需额外的appearance token，限制了可扩展性。

3. **跨模态与动态场景拓展。** OSCR表示的遮挡感知特性天然适用于视频生成中的时序遮挡推理，或三维场景理解中的多视角一致性建模。将其拓展到视频生成或其他生成模态是一个自然的延伸方向。

4. **评估体系的完善。** 当前3DOc-Bench的深度排序指标依赖单目深度估计模型，其自身误差可能影响评估可靠性。建立具有真实深度标注的基准数据集，或设计无需外部模型的直接评估方法，将有助于更精确地衡量遮挡推理能力。

## 原文 PDF

![[paperPDFs/CVPR_2026/SeeThrough3D_Occlusion_Aware_3D_Control_in_Text_to_Image_Generation.pdf]]