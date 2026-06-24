---
title: "SpatialHand: Generative Object Manipulation from 3D Prespective"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SpatialHand_Generative_Object_Manipulation_from_3D_Prespective_ec957f118a1e.pdf
project_link: "https://spatialhand.github.io/"
code_link: null
aliases:
- SpatialHand
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将6DoF姿态显式分解为二维位置掩码、深度图和三维方向参数，并作为额外条件输入到扩散Transformer中，是消除歧义的关键控制变量。
primary_logic: 通过将物体6DoF姿态分解为图像生成模型可理解的二维位置、深度和方向分量，并利用自动构建的大规模合成数据与渐进式训练，首次实现了具有完整6DoF控制能力的生成式物体插入与移动。
claims:
- SpatialHand在物体插入任务上，深度误差（AbsRel）相比GPT-4o降低近一半（19.8 vs 38.6），方向准确率（Acc@30°）提升一倍以上（52.0 vs 20.2）。
- 几何感知合成模块能有效纠正遮挡关系，移除该模块后深度误差从19.8增加到25.5。
- 渐进式训练方案对方向控制至关重要，跳过第一阶段训练导致Acc@30°从52.0骤降至28.7。
- 定性结果表明，SpatialHand能在保持物体身份的同时，精确控制旋转、平移和遮挡，而GPT-4o等基线无法可靠遵循方向指令。
---

# SpatialHand: Generative Object Manipulation from 3D Prespective

> [!tip] 核心洞察
> 通过将物体6DoF姿态分解为图像生成模型可理解的二维位置、深度和方向分量，并利用自动构建的大规模合成数据与渐进式训练，首次实现了具有完整6DoF控制能力的生成式物体插入与移动。

| 字段 | 内容 |
|------|------|
| 中文题名 | SpatialHand：基于三维视角的生成式物体操控 |
| 英文题名 | SpatialHand: Generative Object Manipulation from 3D Prespective |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=VpsqfCac2B) · [Project](https://spatialhand.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | SpatialHand |
| Dataset | 自定义三维物体插入基准（20场景×20物体×2姿态） |

> [!tip] 效果简介
> - 自定义三维物体插入基准（20场景×20物体×2姿态） 上，AbsRel↓ (视觉+文本条件) 19.8 vs 38.6 (GPT-4o) (-18.8)。
> - 同上 上，Acc@30°↑ (视觉+文本条件) 52.0 vs 20.2 (GPT-4o) (+31.8)；DINO↑ (视觉+文本条件) 81.7 vs 81.2 (Gemini-2.0) (+0.5)；CLIP↑ (纯文本条件) 72.5 vs 66.5 (Nano Banana) (+6.0)。
> - 三维物体移动基准测试 (Table 2) 上，旋转准确率 Acc@30°↑ 47.8 vs 39.7 (Diffusion Handles) (+8.1)。

## 概述

**问题瓶颈**：现有基于二维图像修复的物体操控方法无法理解底层三维场景布局，导致物体插入与移动时在位置（前方还是后方？）、朝向（面向左还是右？）和遮挡关系上存在根本性歧义（Figure 2）。

**核心方案**：SpatialHand 提出了一种从三维视角出发的生成式物体操控框架。其核心洞察在于：将物体的6自由度（6DoF）姿态显式分解为扩散Transformer可理解的三个条件分量——二维位置掩码、合成深度图、以及三维方向参数（方位角、仰角、平面内旋转），从而消除二维修复中的空间歧义。同时，该方法利用基于合成3D资产与主题驱动生成的大规模自动化数据管线，配合渐进式训练策略，首次实现了具有完整6DoF控制能力的生成式物体插入与移动（Figure 3）。

**关键证据**：在三维感知物体插入任务上，SpatialHand 的深度误差（AbsRel）相比GPT-4o降低近一半（19.8 vs 38.6），方向准确率（Acc@30°）提升一倍以上（52.0 vs 20.2）；在物体移动任务上，遮挡处理VLM准确率较Diffusion Handles提升30个百分点（82.6 vs 52.6）。消融实验证实，几何感知合成模块和渐进式训练方案对深度控制与方向控制分别具有决定性作用（Table 1, Table 2, Table 3）。

**方法定位**：SpatialHand 属于条件扩散生成模型在三维感知图像编辑领域的应用，其技术路线位于扩散Transformer（基于FLUX-Dev）、单目深度估计（Depth Anything）、以及视觉基础模型（Grounding-DINO、SAM）的交汇处。与纯文本驱动的多模态大模型（GPT-4o、Gemini）和基于点云的三维移动方法（Diffusion Handles, Pandey et al., CVPR 2024）相比，本文方法在显式三维姿态控制上具有显著优势。

## 背景与动机

### 问题背景：二维修复在三维场景中的根本性歧义

图像编辑技术在二维像素空间取得了显著进展，特别是基于扩散模型的图像修复（inpainting）方法，能够在用户指定的遮罩区域内生成视觉上逼真的内容。然而，当任务从“填充纹理”升级为“在三维场景中插入或移动物体”时，纯粹的二维修复范式暴露出根本性的结构缺陷。

核心瓶颈在于：**二维修复模型无法理解底层三维场景布局**。当用户希望在桌面上放置一个杯子，或将沙发从房间一侧移动到另一侧时，模型面临两类不可逾越的歧义（如 Figure 2 所示）：

1. **位置歧义**：插入的物体应该位于场景中现有元素的前方还是后方？二维遮罩仅定义了图像平面上的区域，无法传达深度信息，导致遮挡关系完全由模型猜测。
2. **方向歧义**：物体应该面向左侧还是右侧？二维参考图像只提供单一视角的外观，模型缺乏将物体旋转到指定朝向的几何约束。

这些歧义的根源在于，6DoF姿态（三维位置+三维朝向）是三维空间中的连续参数，而传统图像修复的输入条件（遮罩+参考图）仅存在于二维流形上。这种维度不匹配使得现有方法在物体操控任务中产生不可靠的结果——位置错误、朝向随机、遮挡关系混乱。

### 现有方法的缺口

当前能够处理物体插入或移动的方法大致分为三类，但均未完整解决上述歧义：

- **基于大规模多模态语言模型的方法**（如 **GPT-4o**、**Gemini-2.0-Flash**）：这些模型通过自然语言指令进行图像编辑，具备一定的场景理解能力。然而，语言描述无法精确指定三维姿态——用户可以说“把杯子放在桌子左边”，但无法通过文本可靠地控制杯子的精确深度位置和旋转角度。实验表明，GPT-4o 在方向控制上的准确率（Acc@30°）仅为 20.2%，接近随机猜测水平（Table 1）。

- **基于点云的三维物体移动方法**（如 **Diffusion Handles**，Pandey et al., CVPR 2024）：这类方法通过用户交互点云来指定物体的目标位置，但缺乏对物体朝向的显式控制，且在处理复杂遮挡关系时表现不稳定。在遮挡处理准确率上，Diffusion Handles 仅达到 52.6%（Table 2）。

- **基于拖拽或深度条件的方法**：通过拖拽操作或深度图引导物体移动，但前者容易导致物体变形，后者仅提供深度约束而无法控制朝向（如 Figure 13、Figure 14 所示）。

上述方法的共同缺陷是：**将三维操控问题降维为二维或一维条件输入，丢失了关键的姿态信息维度**。

### 本文动机与核心思路

SpatialHand 的动机直接源于上述分析：要实现精确的三维物体操控，必须为生成模型提供完整且可理解的三维姿态条件。本文的核心洞察是：**将物体的 6DoF 姿态显式分解为图像生成模型可理解的三个分量**——二维位置（遮罩）、深度（深度图）和三维方向（方位角、仰角、平面内旋转）——并将这些分量作为额外条件注入扩散 Transformer 的输入序列中。

这一分解策略的关键优势在于：
- **二维位置遮罩**定义了物体在图像平面上的投影区域，与现有修复模型兼容；
- **合成深度图**指定了插入深度，并通过几何感知合成模块保留应位于物体前方的原始前景，从根本上解决遮挡歧义；
- **方向参数投影**将绝对三维方向编码为潜在特征，叠加到物体参考 token 上，使模型能够精确控制物体的旋转姿态。

通过这种“分解—条件注入”的设计，SpatialHand 首次实现了具有完整 6DoF 控制能力的生成式物体插入与移动，为图像编辑中的三维操控任务建立了新的范式。

## 核心创新

SpatialHand 的核心创新在于将物体的 6DoF 姿态显式分解为扩散 Transformer 可直接理解的三维空间条件，从而首次在生成式图像编辑框架中实现了对插入物体位置、深度和朝向的完整且精确的控制。该方法针对现有二维图像修复技术无法理解底层三维场景布局的根本性瓶颈，通过以下三个关键的 changed slots 消除了二维编辑中的空间歧义。

**1. 三维位置条件：从遮罩到深度感知的几何注入**

传统图像修复方法仅依赖二维遮罩指定插入区域，无法区分物体应位于场景元素的前方还是后方。SpatialHand 将三维位置分解为二维位置遮罩和合成深度图两个互补分量。具体而言，模型输入序列从标准的 $[\mathbf{X}, \mathbf{C}_T]$ 扩展为 $[\mathbf{X}, \tilde{\mathbf{C}}_{\mathrm{mask}}, \tilde{\mathbf{C}}_{\mathrm{depth}}, \mathbf{C}_{\mathrm{obj}}]$，其中 $\tilde{\mathbf{C}}_{\mathrm{mask}}$ 是经过几何感知合成的场景遮罩图像，$\tilde{\mathbf{C}}_{\mathrm{depth}}$ 是指定插入深度的合成深度图。关键的几何感知合成模块通过比较场景深度与目标插入深度，自动保留应遮挡插入物体的原始前景区域，从而确保生成的遮挡关系符合三维空间逻辑。消融实验证实，移除该模块后深度误差 AbsRel 从 19.8 显著上升至 25.5（Table 3），验证了深度条件对消除位置歧义的决定性作用。

**2. 三维方向条件：绝对姿态参数的隐式编码**

现有方法缺乏对物体朝向的显式控制，导致插入物体的面向方向存在严重歧义。SpatialHand 引入零初始化 MLP 投影器 $P(\cdot)$，将绝对方向参数——方位角 $\varphi$、仰角 $\theta$ 和平面内旋转 $\delta$——映射到潜在维度，并以残差方式叠加到物体参考 token 上，形成最终输入序列 $[\mathbf{X}, \tilde{\mathbf{C}}_{\mathrm{mask}}, \tilde{\mathbf{C}}_{\mathrm{depth}}, \mathbf{C}_{\mathrm{obj}} + P([\varphi, \theta, \delta])]$。这一设计使得方向控制信号能够与物体的视觉特征在注意力机制中充分交互，而零初始化策略则保证了训练初期的稳定性。实验结果表明，SpatialHand 的方向准确率 Acc@30° 达到 52.0，相比 GPT-4o 的 20.2 提升超过一倍（Table 1），在物体移动任务上也以 47.8 的 Acc@30° 显著优于 Diffusion Handles 的 39.7（Table 2）。

**3. 渐进式训练策略：解耦空间感知与方向控制**

SpatialHand 采用三阶段渐进训练方案，其中第一阶段专注于新视角合成微调，使模型初步建立对三维几何的感知能力；第二阶段引入完整的 6DoF 条件进行端到端训练。消融实验表明，跳过第一阶段直接进行第二阶段训练会导致方向准确率 Acc@30° 从 52.0 骤降至 28.7（Table 3），降幅超过 44%。这一结果揭示了渐进式训练对方向控制能力的关键作用：模型需要先在较为简单的任务中习得空间感知基础，才能有效利用方向条件实现精确的姿态控制。

上述三个 changed slots 相互协同，共同构成了从二维修复到三维感知操控的质变：深度条件解决了“在哪里”的深度歧义，方向条件解决了“朝哪边”的朝向歧义，而渐进训练则确保了这两个条件能够被模型有效吸收和利用。这种将 6DoF 姿态显式分解为图像生成模型可理解的空间条件的设计思路，为生成式物体操控提供了新的范式。

## 整体框架

SpatialHand 的核心设计思想是将物体的 6DoF 姿态显式分解为扩散 Transformer 可理解的三维位置条件与三维方向条件，从而消除传统二维修复方法在物体插入与移动任务中的空间歧义性。整体流程如 Figure 3 所示，系统接收一张场景图像、一个物体参考图像以及目标 6DoF 姿态参数，输出符合指定位置、深度和朝向的合成图像。

![[assets/figures/papers/paper_list_l63_https_openreview_net_forum_id_VpsqfCac2B/figures/003_Figure_3.jpg]]
*Figure 3: Overall pipeline of SpatialHand. We focus on object insertion as our primary task due to its flexibility. SpatialHand decomposes the 6DoF object pose into 3D location (2D mask and depth map) and 3D orientation. These spatial conditions, along with free-view object reference images and text captions, are incorporated into the diffusion transformer’s input tokens*

### 姿态分解与条件构建

6DoF 姿态被分解为两个正交分量：

- **三维位置条件**：由二维位置掩码和合成深度图共同定义。二维位置通过物体边界框对应的二值掩码指定物体在图像平面内的放置区域；合成深度图则显式编码物体在场景中的插入深度，并通过几何感知合成模块保留应遮挡物体的原始前景元素，确保正确的遮挡关系。
- **三维方向条件**：由方位角 $\varphi$、仰角 $\theta$ 和平面内旋转 $\delta$ 三个绝对角度参数描述。这三个参数通过一个零初始化的 MLP 投影器 $P(\cdot)$ 映射到潜在维度，然后叠加到物体参考 token 上，实现方向信息的注入。

### 扩散 Transformer 的输入序列扩展

SpatialHand 基于 FLUX-Dev 扩散 Transformer 架构，将标准的多模态注意力输入序列从 $[\mathbf{X}, \mathbf{C}_T]$ 扩展为：

$$[\mathbf{X}, \tilde{\mathbf{C}}_{\mathrm{mask}}, \tilde{\mathbf{C}}_{\mathrm{depth}}, \mathbf{C}_{\mathrm{obj}} + P([\varphi, \theta, \delta])]$$

其中 $\mathbf{X}$ 为加噪图像 token，$\tilde{\mathbf{C}}_{\mathrm{mask}}$ 为几何感知遮罩场景图像 token，$\tilde{\mathbf{C}}_{\mathrm{depth}}$ 为合成深度图 token，$\mathbf{C}_{\mathrm{obj}}$ 为物体参考图像 token。方向投影 $P([\varphi, \theta, \delta])$ 以残差形式叠加到物体 token 上，使模型在去噪过程中能够同时感知物体的外观、位置、深度和朝向。

### 物体移动的双阶段执行

对于三维物体移动任务，SpatialHand 采用先移除后插入的策略：首先利用二维检测与分割模块（Grounding-DINO + SAM）定位并移除目标物体，然后将其作为新的插入对象，以目标 6DoF 姿态重新插入场景。这一设计将移动任务统一到插入框架下，避免了单独训练移动模型的需求。

### 关键模块协作关系

各模块在推理时的协作流程如下：
1. **场景深度估计模块**（Depth Anything）估计背景场景的深度图，为深度条件提供场景几何参考。
2. **二维检测与分割模块**（Grounding-DINO + SAM）生成物体的二维位置掩码。
3. **物体方向估计模块**（Orient Anything）从物体参考图像中估计其三维方向参数。
4. **几何感知合成模块**通过比较物体指定深度与场景深度图，自动判断遮挡关系，保留应位于物体前方的原始前景像素。
5. **扩散 Transformer** 接收上述所有条件 token，执行多步去噪生成最终图像。

消融实验（Table 3）验证了这一框架中各模块的必要性：移除几何感知合成后深度误差从 19.8 升至 25.5；跳过渐进式训练第一阶段后方向准确率从 52.0 骤降至 28.7，表明位置-深度联合条件与渐进训练是框架有效性的关键支撑。

## 核心模块与公式推导

SpatialHand 的核心设计思路是将物体的 6DoF 姿态显式分解为扩散 Transformer 可理解的三维位置条件与三维方向条件，从而消除传统二维修复中的空间歧义。整体流程如 Figure 3 所示，模型以 FLUX-Dev 扩散 Transformer 为骨干，接收扩展的多模态输入序列。

### 3.1 多模态注意力机制

模型沿用标准的多模态扩散 Transformer 架构，对图像 token 与文本 token 进行联合注意力计算：

$$
\operatorname{Attn}([\mathbf{X}, \mathbf{C}_T]) = \operatorname{Softmax}(\frac{\mathbf{Q}\mathbf{K}^\mathsf{T}}{\sqrt{d}})\mathbf{V}
$$

其中 $\mathbf{X}$ 为加噪图像 token，$\mathbf{C}_T$ 为文本条件 token，$\mathbf{Q}$、$\mathbf{K}$、$\mathbf{V}$ 分别为查询、键、值矩阵，$d$ 为特征维度。该机制为后续空间条件的注入提供了统一的多模态交互框架。

### 3.2 三维位置条件注入

为精确控制物体的插入位置与遮挡关系，SpatialHand 将三维位置分解为二维遮罩与合成深度图两个互补分量，并扩展原始输入序列。

**几何感知遮罩图像**：在目标场景的二维遮罩区域基础上，通过比较场景深度图与指定插入深度，保留应位于物体前方的原始前景像素，形成几何感知遮罩图像 $\tilde{\mathbf{C}}_{\mathrm{mask}}$。该操作确保生成过程中前景遮挡关系被正确保留。

**合成深度图**：将物体渲染深度与场景深度图按指定深度进行合成，生成显式定义插入深度的合成深度图 $\tilde{\mathbf{C}}_{\mathrm{depth}}$，作为深度条件输入。

**物体参考 token**：从多视角物体参考图像中提取的物体身份特征 $\mathbf{C}_{\mathrm{obj}}$，用于保持插入物体的外观一致性。

扩展后的输入序列为：

$$
[\mathbf{X}, \tilde{\mathbf{C}}_{\mathrm{mask}}, \tilde{\mathbf{C}}_{\mathrm{depth}}, \mathbf{C}_{\mathrm{obj}}]
$$

### 3.3 三维方向条件注入

方向控制是实现完整 6DoF 操控的关键。SpatialHand 将物体的绝对三维方向参数化为一组角度值——方位角 $\varphi$、仰角 $\theta$ 和平面内旋转 $\delta$，并通过一个零初始化 MLP 投影器 $P(\cdot)$ 将其映射到与物体参考 token 相同的潜在维度，再以加法方式注入：

$$
[\mathbf{X}, \tilde{\mathbf{C}}_{\mathrm{mask}}, \tilde{\mathbf{C}}_{\mathrm{depth}}, \mathbf{C}_{\mathrm{obj}} + P([\varphi, \theta, \delta])]
$$

零初始化策略确保训练初期方向条件不干扰物体身份的学习，随后逐步获得方向控制能力。消融实验表明，该方向注入机制对姿态遵循度至关重要：跳过相关训练阶段会导致 Acc@30° 从 52.0 骤降至 28.7（Table 3）。

### 3.4 几何感知合成模块

该模块是实现正确遮挡关系的核心组件。其工作原理为：在获得场景深度图与指定插入深度后，逐像素比较两幅深度图——若场景像素的深度值小于插入深度（即该像素对应的真实物体位于插入物体前方），则保留原始场景像素；否则使用遮罩填充。Figure 7 可视化了该模块的开关效果：移除几何感知合成后，深度误差 AbsRel 从 19.8 上升至 25.5（Table 3），验证了其对深度控制与遮挡处理的决定性作用。

![[assets/figures/papers/paper_list_l63_https_openreview_net_forum_id_VpsqfCac2B/figures/010_Figure_7.jpg]]
*Figure 7: Effect of geometry-aware composition. We sequentially present the masked scene, depth map, and synthesized images, with and without applying geometry-aware composition*

### 3.5 渐进式训练策略

SpatialHand 采用三阶段渐进训练以稳定方向控制的学习：

- **阶段一（新视角合成微调）**：在合成数据上训练模型从多视角参考图像生成新视角物体，使模型初步建立三维方向与二维外观之间的映射关系。该阶段训练 60k 步。
- **阶段二（物体插入训练）**：引入完整的三维位置与方向条件，在物体插入任务上联合优化。该阶段训练 20k 步。
- **阶段三（可选微调）**：针对特定场景或物体进行少量步数的适配。

消融实验证实，跳过阶段一直接进行阶段二会导致方向准确率大幅下降（Table 3），说明渐进式训练对方向控制能力的建立具有不可替代的作用。

### 补充图表

![[assets/figures/papers/paper_list_l63_https_openreview_net_forum_id_VpsqfCac2B/figures/002_Figure_2.jpg]]
*Figure 2: Motivation of SpatialHand. 2D inpainting for object insertion/movement suffers from location ambiguity (in front of or behind existing elements?) and orientation ambiguity (facing right or left?). SpatialHand resolves these by adding extra depth and orientation conditions for spatially controlled object manipulation*

![[assets/figures/papers/paper_list_l63_https_openreview_net_forum_id_VpsqfCac2B/figures/004_Figure_4.jpg]]
*Figure 4: Pipeline of training data curation. We start with high-quality synthetic 3D assets. Using a rendering engine and subject-driven generation, we simulate how humans place objects in 3D space. Then, we employ a series of visual foundation models to estimate the 3D information within images*

## 实验与分析

### 核心实验设计与评估体系

SpatialHand的实验验证围绕两个核心任务展开：**三维感知物体插入**（3D-aware object insertion）与**三维感知物体移动**（3D-aware object movement）。评估体系从四个维度综合衡量方法性能：

1. **物体身份保持**：通过DINO和CLIP特征相似度衡量生成物体与参考物体的一致性。
2. **深度控制精度**：采用绝对相对误差（AbsRel）评估插入物体的深度位置准确性。
3. **方向控制精度**：以方向误差在30°以内的准确率（Acc@30°）作为核心指标。
4. **主观质量评估**：包括生成保真度（Fidelity）和姿态遵循度（Adherence）的人工评分（1-5分制），并辅以VLM辅助评估。

测试基准采用自定义构建的数据集，包含20个场景×20个物体×2种姿态的测试样本，同时覆盖视觉条件（提供物体参考图像）和纯文本条件两种设置。

### 三维感知物体插入：主结果分析

Table 1汇总了物体插入任务上的定量对比结果。SpatialHand在深度控制和方向控制两个核心维度上展现出显著优势：

**深度控制**：SpatialHand的AbsRel达到19.8（视觉+文本条件），相比GPT-4o的38.6降低了近一半（-18.8），证明显式深度条件输入有效解决了二维修复中的位置歧义问题。在纯文本条件下，SpatialHand同样取得18.7的AbsRel，显著优于Nano Banana的28.0。

**方向控制**：Acc@30°指标上，SpatialHand在视觉+文本条件下达到52.0，而GPT-4o仅为20.2（+31.8），方向准确率提升超过一倍。这表明将6DoF姿态中的方向分量显式编码为条件信号，是消除方向歧义的因果性关键设计。纯文本条件下，SpatialHand的Acc@30°为47.0，同样大幅领先基线方法。

**物体身份保持**：在DINO相似度上，SpatialHand（81.7）与Gemini-2.0（81.2）基本持平，CLIP相似度（72.5）优于Nano Banana（66.5），说明方法在实现精确空间控制的同时，并未牺牲物体外观的保真度。

**主观评估**：SpatialHand在姿态遵循度上获得4.27/5（视觉+文本），远高于GPT-4o的2.67/5（+1.60），印证了定性结果中观察到的方向指令遵循能力。生成保真度方面，SpatialHand（4.30/5）略优于GPT-4o（4.13/5）。

定性结果（Figure 5, Figure 8）进一步验证了上述结论：GPT-4o等基线方法往往无法可靠遵循方向指令，插入物体的朝向存在随机性；而SpatialHand能够精确控制旋转角度，同时保持物体身份和合理的遮挡关系。

![[assets/figures/papers/paper_list_l63_https_openreview_net_forum_id_VpsqfCac2B/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison on 3D-aware object insertion. Red arrow indicates the desired orientation, and green arrow denotes the left side of the corresponding pose. Zoom in for best view*

![[assets/figures/papers/paper_list_l63_https_openreview_net_forum_id_VpsqfCac2B/figures/011_Figure_8.jpg]]
*Figure 8: More qualitative comparison on 3D-aware object insertion*

### 三维感知物体移动：主结果分析

物体移动任务要求将场景中已有物体移除后，以目标姿态重新插入。Table 2展示了与Diffusion Handles（Pandey et al., CVPR 2024）等方法的对比结果：

**方向控制**：SpatialHand的Acc@30°达到47.8，显著优于Diffusion Handles的39.7（+8.1），证明方法在移动场景下同样具备可靠的方向控制能力。

**平移精度**：平移mIoU达到0.72（Diffusion Handles为0.62，+0.10），深度误差AbsRel降至17.9（Diffusion Handles为23.7，-5.8），表明显式深度条件在移动任务中同样有效。

**遮挡处理**：VLM-Acc指标上，SpatialHand达到82.6，远超Diffusion Handles的52.6（+30.0）。这一巨大差距揭示了SpatialHand几何感知合成模块的核心价值——通过比较深度图保留应位于物体前方的原始前景，确保正确的遮挡关系。定性结果（Figure 6, Figure 9）直观展示了这一优势。

### 消融实验：关键设计验证

Table 3的消融实验揭示了SpatialHand中两个关键设计组件的因果作用：

**几何感知合成模块**：移除该模块后，深度误差AbsRel从19.8上升至25.5（+5.7）。这一结果表明，简单的遮罩修复无法理解场景的三维布局，而通过深度图比较保留前景遮挡是确保深度控制精度的必要条件。Figure 7的可视化消融进一步展示了该模块的效果——不应用几何感知合成时，插入物体可能错误地遮挡本应位于其前方的前景元素。

**渐进式训练方案**：跳过第一阶段（新视角合成微调）直接进行第二阶段训练，导致方向准确率Acc@30°从52.0骤降至28.7（-23.3）。这一大幅下降验证了渐进式训练对方向控制的关键作用——第一阶段通过新视角合成任务使模型学会理解物体在不同视角下的外观变化，为第二阶段的方向条件注入提供了必要的先验知识。

**文本条件的作用**：附录Figure 10的定性消融表明，文本条件在物体朝向变化时对保持物体一致性至关重要。去掉文本条件后，插入物体的外观特征（如纹理、形状细节）可能出现丢失或变形，说明文本描述提供了物体身份的额外约束。

### 公平性讨论与实验局限

实验设计中存在若干需要关注的公平性问题：

- **基线约束差异**：GPT-4o等基于API的基线方法可能不完全遵循遮罩约束，导致背景变化和物体超出边界，使定量比较略有偏差。这并非SpatialHand方法本身的优势，而是实验设置带来的系统性差异。
- **测试集规模与多样性**：当前测试基准仅包含20个场景，且主要基于合成或特定数据集构建。在更大规模的真实世界数据集上的泛化性能尚需进一步验证。这一局限性限制了结论的外部有效性。
- **主观评估偏差**：Fidelity和Adherence评分可能受到评估者偏好的影响。论文已采用VLM辅助评估以部分缓解此问题，但主观指标的固有不确定性仍然存在。

### 失败模式分析

基于论文报告的局限性，SpatialHand存在以下已知失败模式：

1. **位置-朝向耦合问题**：物体朝向与二维边界框存在相互依赖关系——框的长宽比应与特定方向下的物体投影形状匹配。当用户指定的边界框形状与目标朝向严重冲突时，方向控制效果会被削弱。这是方法架构层面的固有限制，使位置和朝向条件更独立是未来工作的重要方向。

2. **特殊物体类型的泛化不足**：模型主要面向通用物体训练，对人类或艺术风格的物体操控未经专项优化。虽然初步实验（Figure 11）展示了向人类主体和艺术主体的泛化能力，但在极端情况下性能可能下降。这一局限源于训练数据的分布偏差。

![[assets/figures/papers/paper_list_l63_https_openreview_net_forum_id_VpsqfCac2B/figures/014_Figure_11.jpg]]
*Figure 11: Qualitative results of moving human and artistic subjects*

3. **复杂材质物体的挑战**：透明、非刚性等复杂物体的插入尚未得到系统处理，这些物体的深度估计和遮挡推理存在固有困难，是当前方法的开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l63_https_openreview_net_forum_id_VpsqfCac2B/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison results on 3D-aware object insertion. Object similarity in the generated image to the reference is measured using DINO↑ and CLIP↑. AbsRel↓ evaluates the accuracy of the inserted object’s depth position, and Acc@30°↑ measures its orientation accuracy*

![[assets/figures/papers/paper_list_l63_https_openreview_net_forum_id_VpsqfCac2B/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison on 3D-aware object movement*

![[assets/figures/papers/paper_list_l63_https_openreview_net_forum_id_VpsqfCac2B/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative comparison on 3D-aware object movement*

![[assets/figures/papers/paper_list_l63_https_openreview_net_forum_id_VpsqfCac2B/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of how the “SpatialHand” can manipulate objects in images from 3D prespective. With the basic ability to insert objects with 6DoF control (top row), allowing for any-degree rotation (middle row), and precise 3D movement (bottom row)*

![[assets/figures/papers/paper_list_l63_https_openreview_net_forum_id_VpsqfCac2B/figures/012_Figure_9.jpg]]
*Figure 9: More qualitative comparison on 3D-aware object insertion*

## 方法谱系与知识库定位

### 核心问题定位与切入点

SpatialHand 瞄准的是一个被现有图像编辑方法系统性忽视的瓶颈：**二维修复模型缺乏对底层三维场景布局的理解**，导致物体插入时的位置、朝向和遮挡关系存在根本性歧义（见 Figure 2）。无论是基于文本指令的大规模多模态模型（如 GPT-4o、Gemini-2.0-Flash），还是基于点云的专用方法（如 **Diffusion Handles** (Pandey et al., CVPR 2024)），都无法可靠地将用户指定的 6DoF 姿态转化为具有正确三维空间关系的生成结果。

SpatialHand 的因果控制变量在于：**将 6DoF 姿态显式分解为二维位置掩码、深度图和三维方向参数，并作为额外条件注入扩散 Transformer 的输入序列**。这一设计使得模型无需从模糊的二维信号中隐式推断三维关系，而是直接接收结构化的空间约束。

### 相对于基线方法的改进维度

#### 与通用图像编辑模型的对比

GPT-4o 和 Gemini-2.0-Flash 等大规模多模态模型虽然在物体保真度（DINO 81.2 vs. SpatialHand 81.7）和 CLIP 相似度上具有竞争力，但在三维控制精度上存在系统性缺陷：GPT-4o 的深度误差 AbsRel 高达 38.6，方向准确率 Acc@30° 仅为 20.2，而 SpatialHand 分别达到 19.8 和 52.0（Table 1）。定性结果（Figure 5、Figure 8）进一步表明，这些基线无法可靠遵循方向指令，常出现物体朝向错误或遮挡关系混乱。

#### 与专用三维操控方法的对比

**Diffusion Handles** (Pandey et al., CVPR 2024) 是物体移动任务的主要对比基线。该方法基于点云操作，但在遮挡处理上存在显著弱点：其 VLM-Acc 仅为 52.6，而 SpatialHand 达到 82.6（Table 2），差距达 30 个百分点。这源于 Diffusion Handles 缺乏显式的深度条件注入机制，无法有效判断前景与背景的遮挡关系。在旋转准确率（39.7 vs. 47.8）和平移 mIoU（0.62 vs. 0.72）上，SpatialHand 同样保持优势。

#### 方法独特性总结

SpatialHand 的独特贡献不在于提出全新的生成架构，而在于**对现有扩散 Transformer 框架（基于 FLUX-Dev）进行最小侵入式的条件扩展**：
- 将标准输入序列 $[\mathbf{X}, \mathbf{C}_T]$ 扩展为 $[\mathbf{X}, \tilde{\mathbf{C}}_{\mathrm{mask}}, \tilde{\mathbf{C}}_{\mathrm{depth}}, \mathbf{C}_{\mathrm{obj}} + P([\varphi, \theta, \delta])]$，通过几何感知遮罩、合成深度图和方向投影器实现三维控制
- 引入几何感知合成模块，通过比较深度图保留前景遮挡，这是现有方法普遍缺失的环节
- 采用零初始化 MLP 投影器将方向参数映射到潜在维度，避免破坏预训练权重

### 适用边界与局限

#### 已知局限

1. **位置与朝向的耦合依赖**：物体朝向与二维边界框存在相互依赖关系——边界框的长宽比应与特定方向下的物体形状匹配。当两者冲突严重时（例如窄长物体被放置在正方形遮罩中），方向控制效果会被削弱。这是将 6DoF 分解为二维位置和三维方向时引入的结构性约束。

2. **物体类型的泛化边界**：模型主要面向通用刚性物体训练。对人类或艺术风格主体的操控（Figure 11）显示了初步泛化能力，但论文明确指出这些场景尚未经过专项训练，极端情况下可能性能下降。

3. **测试规模与生态效度**：评估基准仅包含 20 个场景，且数据主要来自合成管线。在更大规模的真实世界场景中的表现有待验证。

#### 需要人工验证的潜在局限

- 透明物体、非刚性物体的插入能力未在论文中讨论
- 对光照一致性（Figure 12 展示了部分结果）的鲁棒性上限不明确
- 与基于物理的渲染方法（如神经辐射场）的协同潜力未被探索

### 开放问题与未来方向

1. **解耦位置与朝向条件**：如何使边界框形状不再约束方向控制，是实现更灵活 6DoF 操控的关键理论问题。

2. **动态视频扩展**：当前方法仅处理静态图像。将 6DoF 控制能力扩展到视频中的三维物体操控，需要解决时序一致性和运动估计问题。

3. **更大规模真实世界基准**：建立包含多样场景、复杂光照和遮挡关系的真实世界三维物体操控基准，是推动该方向可复现研究的必要基础设施。

4. **复杂物体类别**：透明、镜面反射、非刚性物体的插入涉及更复杂的光线传输和形变建模，可能需要在条件输入中引入额外的物理先验。

## 原文 PDF

![[paperPDFs/ICLR_2026/SpatialHand_Generative_Object_Manipulation_from_3D_Prespective_ec957f118a1e.pdf]]