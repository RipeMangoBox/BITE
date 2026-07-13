---
title: "FlexAvatar: Learning Complete 3D Head Avatars with Partial Supervision"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FlexAvatar_Learning_Complete_3D_Head_Avatars_with_Partial_Supervision.pdf
project_link: "https://tobias-kirschstein.github.io/flexavatar/"
code_link: null
aliases:
- FlexAvatar
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入可学习的偏差令牌（bias sinks）z2D 和 z3D，根据训练数据来源（单目/多视图）分别吸收数据集偏差，在推理时全部使用 z3D 令牌以获得解耦的多视图行为，从而生成完整3D头部。
primary_logic: 通过让模型在训练时显式区分单目与多视图数据，并将视图纠缠效应限制在特定令牌中，可以在不牺牲单目泛化能力的前提下，实现从单张图像重建完整且可动画化的3D头部化身。
claims:
- 在单目自重演（self-reenactment）设置中，当渲染相机与驱动相机相同时效果良好，但当渲染相机移动时出现虚影，表明模型依赖视角泄露。
- 在Ava256数据集上的消融实验中，完整的FlexAvatar架构（包含bias sinks）取得了17.2 dB的PSNR，生成了完整的3D头部，验证了bias sinks的有效性。
- VFHQ 上 PSNR↑ (self-reenactment) = 23.47
- VFHQ 上 CSIM↑ (cross-reenactment) = 0.663
---

# FlexAvatar: Learning Complete 3D Head Avatars with Partial Supervision

> [!tip] 核心洞察
> 通过让模型在训练时显式区分单目与多视图数据，并将视图纠缠效应限制在特定令牌中，可以在不牺牲单目泛化能力的前提下，实现从单张图像重建完整且可动画化的3D头部化身。

| 字段 | 内容 |
|------|------|
| 中文题名 | FlexAvatar：利用部分监督学习完整3D头部化身 |
| 英文题名 | FlexAvatar: Learning Complete 3D Head Avatars with Partial Supervision |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Kirschstein_FlexAvatar_Learning_Complete_3D_Head_Avatars_with_Partial_Supervision_CVPR_2026_paper.html) · [Project](https://tobias-kirschstein.github.io/flexavatar/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FlexAvatar |
| Dataset | VFHQ, Ava256, NeRSemble |

> [!tip] 效果简介
> - VFHQ 上，PSNR↑ (self-reenactment) 23.47 vs 见论文Table 2 (N/A)；CSIM↑ (cross-reenactment) 0.663 vs 见论文Table 2 (N/A)。
> - Ava256 上，PSNR↑ (single-image) 16.9 vs 见论文Table 3 (显著优于先前方法)；PSNR↑ (few-shot, 4 images) 21.1 vs 见论文Table 3 (显著优于Avat3r)。
> - NeRSemble 上，LPIPS↓ (monocular) FlexAvatar vs 先前的SOTA方法 (显著降低LPIPS，在所有指标上优于基线)。

## 概要

### 问题瓶颈

单目视频是获取动态人脸数据最便捷的途径，但其中存在一个根本性纠缠：驱动信号（表情与头部姿态）与目标视点天然耦合——训练帧的拍摄视角既是“驱动源”也是“渲染目标”。当模型在这种数据上以朴素方式训练时，它会隐式地依赖视角泄露来重建外观，一旦渲染相机偏离驱动视角，便会产生虚影和不完整的头部几何，无法泛化到自由视点渲染。这一瓶颈直接限制了从单张图像创建完整、可动画化3D头部化身的能力。

### 核心方法定位

FlexAvatar 的核心洞察是：**与其试图消除单目数据中的视角纠缠，不如让模型显式地“意识到”这种偏差，并将其隔离在可控的令牌中**。具体而言，方法引入两个可学习的偏差令牌（bias sinks）——$z_{2D}$ 和 $z_{3D}$，分别对应单目数据与多视图数据。训练时，根据输入图像的数据来源，将对应的偏差令牌拼接到表情序列中，使令牌吸收各自数据模态的特有偏差（尤其是单目数据中驱动-视角的纠缠）。推理时，始终使用 $z_{3D}$ 令牌，使模型继承多视图数据中解耦的行为模式，从而在仅给定单张图像的情况下生成完整、可自由旋转的3D头部。

在方法谱系上，FlexAvatar 延续了基于3D高斯泼溅（3DGS）的头部化身管线，但在三个关键维度上做出改进：

1. **动画机制**：摒弃对3DMM（如FLAME）预定义表达空间的刚性依赖，转而通过交叉注意力直接从数据中学习表情变换，使网络能够捕捉更丰富的面部动画。
2. **解码器架构**：提出结合 PixelShuffle 与 StyleGAN2 启发式块的上采样模块，实现 8× 上采样以增加高斯数量，显著提升渲染质量。
3. **训练损失**：在标准 $L_1$ 与 SSIM 之外，引入基于 DINOv2 和 SAM 的感知损失，增强渲染图像的锐度与结构保真度。

与同期的单图像/少样本化身方法（如 **Avat3r**、**GAGAvatar**、**LAM**）以及单目化身方法（如 **GaussianAvatars**、**FlashAvatar**、**CAP4D**）相比，FlexAvatar 的核心差异化优势在于其 **bias sinks 机制实现了对数据源偏差的显式建模**，从而在不牺牲单目泛化能力的前提下，获得了多视图数据才具备的完整3D几何生成能力。

### 主要结果概览

FlexAvatar 在四个任务、三个数据集上进行了系统验证（见 Table 1）：

- **3D肖像动画（VFHQ）**：在自重演（self-reenactment）中取得 23.47 dB PSNR，跨重演（cross-reenactment）中 CSIM 达到 0.663，均达到有竞争力的水平。
- **单图像化身创建（Ava256）**：PSNR 达 16.9 dB，显著优于先前方法，且生成的头部几何更加完整。
- **少样本化身创建（Ava256, 4张图像）**：PSNR 达 21.1 dB，显著超越 Avat3r。
- **单目化身创建（NeRSemble）**：在所有指标上优于先前 SOTA，LPIPS 显著降低。

消融实验（Table 5）进一步证实：移除 bias sinks 会导致生成不完整的头部，而完整的 FlexAvatar 架构（含 StyleGAN-PixelShuffle 上采样器、bias sinks、感知损失）取得了 17.2 dB PSNR，验证了各组件的必要性。此外，在冻结解码器的情况下对化身代码进行约 200 步拟合优化，可进一步提升身份保持（CSIM=0.682）与表情保真度。

### 局限与开放问题

当前方法假设输入图像包含清晰人脸，对极端遮挡、大角度姿态及复杂发型/配饰的鲁棒性尚未充分验证。动画表达仍依赖 FLAME 提供的表达代码，可能无法完美覆盖超出其表达空间的表情。化身创建过程需数分钟优化，距离实时应用仍有距离。值得探索的开放方向包括：将 bias sinks 机制扩展到人体姿态或通用动态新视角合成任务；进一步解耦身份与表情以实现独立控制；以及利用文本描述等弱监督信号替代单张图像生成化身。

### 3D头部化身的需求与挑战

从单张肖像图像或单目视频创建可自由动画化、可从任意视点渲染的高质量3D头部化身，是计算机视觉与图形学中一个长期存在的核心问题。这一能力在远程呈现、虚拟现实、数字人交互等应用中具有广泛需求。然而，实现这一目标面临一个根本性的瓶颈：**单目视频训练中，驱动信号（表情/头部姿态）与目标视点的固有纠缠**。具体而言，在单目数据中，每一帧的表情和头部姿态与相机视点是高度耦合的——同一时刻只能观测到一个特定视角下的特定表情。当模型在这样的数据上训练时，它会隐式地学会依赖这种视角泄露（viewpoint leakage）来生成输出：只要渲染相机与驱动相机保持一致（$\pi_{target} = \pi_{drive}$），模型表现良好；但一旦渲染相机移动（$\pi_{target} \neq \pi_{drive}$），模型预测就会出现严重的虚影和伪影，无法生成完整的3D头部结构（见 Figure 4）。这使得模型无法泛化到自由视点渲染，从根本上限制了3D化身创建的实用性。

### 现有方法的缺口

近年来，3D头部化身创建领域取得了显著进展，涌现出多种技术路线：

- **基于3D Morphable Model（3DMM）的方法**（如FLAME参数模型）通过预定义的表达空间进行rigging，虽然结构可控，但表达空间受限于3DMM的线性基，难以捕捉微表情和个性化细节。
- **基于3D Gaussian Splatting（3DGS）的方法**（如**GaussianAvatars**、**FlashAvatar**）利用显式3D高斯表示实现了高质量渲染，但在单目训练条件下同样面临视点-驱动纠缠问题。
- **单图像/少样本化身创建方法**（如**Avat3r**、**GAGAvatar**、**LAM**）尝试从极少输入快速构建化身，但生成的3D头部往往不完整——后脑勺、耳朵、颈部等区域缺乏合理的几何和纹理。
- **3D肖像动画方法**（如**Real3D-portrait**、**Voodoo XP**）专注于从驱动视频迁移表情和姿态，但在跨重演（cross-reenactment）场景下的身份保持和视角泛化仍存在不足。

这些方法的共同缺口在于：**无法在保持单目数据泛化能力的同时，获得多视图数据才能提供的3D完整性**。单目数据覆盖广泛的身份和表情，但缺乏多视图几何信息；多视图数据能提供完整的3D监督，但采集成本高昂且身份覆盖有限。如何在训练中融合两类数据的优势，是此前方法未能有效解决的关键问题。

### 本文动机

FlexAvatar的核心动机正是针对上述瓶颈：**通过让模型在训练时显式区分单目与多视图数据，并将视图纠缠效应限制在特定令牌中，从而在不牺牲单目泛化能力的前提下，实现从单张图像重建完整且可动画化的3D头部化身**。

具体而言，本文提出了一种基于Transformer的3D肖像动画模型，引入**可学习的偏差令牌（bias sinks）**——$z_{2D}$和$z_{3D}$——根据训练数据来源（单目/多视图）分别吸收数据集偏差。在训练阶段，当输入来自单目数据集时使用$z_{2D}$令牌，使其吸收“驱动信号与目标视点纠缠”的偏差；当输入来自多视图数据集时使用$z_{3D}$令牌，使其学习解耦的多视图行为。在推理阶段，**始终使用$z_{3D}$令牌**，从而使模型继承多视图数据的解耦特性，生成完整的3D头部，同时保留单目数据训练带来的广泛泛化能力。

这一设计的核心洞察在于：**视图纠缠不是模型结构的固有缺陷，而是数据模态的偏差**。通过将这种偏差显式建模并隔离到特定令牌中，FlexAvatar实现了单目与多视图数据的统一训练，突破了此前方法在3D完整性与泛化能力之间的权衡。

## 核心方法与创新机理

FlexAvatar的核心创新并非提出全新的网络架构，而是**识别并解决了单目视频训练中一个被忽视的根本瓶颈**：驱动信号（表情/头部姿态）与目标视点的固有纠缠。这一纠缠导致模型在训练时依赖“视角泄露”来重建人脸，从而无法生成完整的3D头部，泛化到自由视点渲染时出现严重伪影。围绕这一因果机制，FlexAvatar提出了三项关键创新。

### 1. 偏差令牌（Bias Sinks）：显式解耦数据源偏差

这是FlexAvatar最核心的机制创新。作者观察到，单目数据集（如VFHQ）中，驱动视频的相机视角与目标渲染视角天然一致（$\pi_{target} = \pi_{drive}$），导致模型学会将视角信息隐含地编码到表情驱动信号中。当推理时改变渲染视角（$\pi_{target} \neq \pi_{drive}$），模型便无法生成完整头部，出现虚影或缺失区域（见Figure 4）。

为解决此问题，FlexAvatar引入两个可学习的**偏差令牌** $z_{2D}$ 和 $z_{3D}$，在解码器阶段拼接到表情序列中：
$$s_{exp} \gets [s_{exp}, z_{bias}]$$

训练时，根据输入图像的数据来源选择令牌：单目数据使用 $z_{2D}$，多视图数据使用 $z_{3D}$。这些令牌作为“偏差吸收器”（bias sinks），将数据模态特定的统计偏差（如单目数据中的视角-驱动纠缠）限制在令牌内部，而非污染整个化身表示。推理时，**始终使用 $z_{3D}$ 令牌**，使模型继承多视图数据的解耦行为，生成完整且可自由旋转的3D头部。消融实验证实，移除bias sinks直接导致头部不完整，证明了其关键作用。

### 2. 无模型动画机制：从数据中学习表情变换

与传统方法依赖3DMM（如FLAME）进行线性rigging不同，FlexAvatar采用**基于交叉注意力的无模型动画机制**。解码器通过交叉注意力将序列化的表情代码 $s_{exp}$ 融入化身表示：
$$h_{dec} = \mathrm{ATTENTION}(\mathcal{A}, s_{exp}, s_{exp})$$

这一设计使网络能够从数据中直接学习面部动画变换，无需依赖预定义的3DMM表达空间。其优势在于：动画能力不再受限于FLAME的表达范围，理论上可以捕捉更丰富的面部细节；同时，该架构允许后续替换驱动信号源（如从语音或文本提取的表情特征），具有天然的扩展性。

### 3. StyleGAN-PixelShuffle混合上采样器

为提高渲染质量，FlexAvatar设计了一种结合**PixelShuffle**和**StyleGAN2启发式CNN块**的上采样架构，实现总计8倍的上采样率：
$$h_{map}^{(l+1)} = \mathrm{PIXELSHUFFLE}(h_{map}^{(l)}) + \mathrm{CNN}(h_x^{(l+1)})$$

该设计在增加3D高斯数量的同时，有效提升了渲染图像的锐度和细节保真度。消融实验表明，完整的FlexAvatar架构（含此上采样器）在PSNR（17.2 dB）和视觉质量上均优于消融变体。

### 4. 增强感知损失

FlexAvatar在标准L1和SSIM损失之外，额外引入基于**DINOv2**和**SAM**的感知损失：
$$\mathcal{L}_{rec} = \mathcal{L}_1 + \mathcal{L}_{SSIM} + \mathcal{L}_{DINO} + \mathcal{L}_{SAM}$$

DINOv2损失提供高层语义感知监督，SAM损失增强结构保真度。消融实验证实，这两项感知损失显著提高了渲染图像的锐度和感知相似度。

---

**创新总结**：FlexAvatar的核心贡献在于**识别单目训练中的视角-驱动纠缠瓶颈**，并通过bias sinks机制实现优雅解耦。该方法使模型能够在混合单目/多视图数据上统一训练，在推理时仅使用 $z_{3D}$ 令牌即可从单张图像生成完整、可动画化的3D头部化身。这一设计理念——通过可学习令牌显式吸收并隔离数据源偏差——具有跨领域迁移的潜力。

FlexAvatar 的整体 pipeline 围绕一个 **编码器-解码器-渲染器** 架构构建，其核心设计目标是从单张肖像图像生成可动画化的完整 3D 头部化身，并支持自由视点渲染。整个流程可概括为三个关键阶段：

1. **编码阶段**：编码器 $E$ 将输入图像 $I$ 投影为一个与视点和表情无关的压缩化身潜在码 $\mathcal{A}$：
   $$\mathcal{A} = E(I)$$

2. **解码阶段**：解码器 $D$ 根据表情代码 $z_{exp}$ 将化身码 $\mathcal{A}$ 解码为一组可驱动的 3D 高斯 $\mathcal{G}$：
   $$\mathcal{G} = D(\mathcal{A}, z_{exp})$$

3. **渲染阶段**：可微光栅化器 $\mathcal{R}$ 将 3D 高斯 $\mathcal{G}$ 从指定视点 $\pi$ 渲染为预测图像 $I^{pred}$：
   $$I^{pred} = \mathcal{R}(\mathcal{G}, \pi)$$

该架构的独特之处在于引入了 **bias sinks** 机制——两个可学习的偏差令牌 $z_{2D}$ 和 $z_{3D}$，它们在训练时根据数据来源（单目/多视图）被拼接到表情序列中，以吸收数据集特有的偏差（特别是单目数据中驱动信号与目标视点的固有纠缠）。推理时统一使用 $z_{3D}$ 令牌，使模型继承多视图数据的解耦行为，从而生成完整的 3D 头部。

以下详细展开各模块的职责与交互关系。

### 编码器 E：从图像到化身潜在码

编码器的设计受 **LAM** 启发，目标是产生一个紧凑的化身表示。具体流程为：

- **图像特征提取**：输入图像 $I$ 首先通过 DINOv2 和浅层 ViT 提取多尺度视觉特征，拼接后经 MLP 得到综合图像特征 $f_{img}$：
  $$f_{img} = \mathbf{MLP}([\mathbf{DINO}(I), \mathbf{ViT}([I, I^{pluck}])])$$

- **UV 锚点查询生成**：在 FLAME 模板网格的 UV 空间中均匀采样 3D 表面点 $x_{mesh}$，并对其进行正弦位置编码以生成查询 $Q$：
  $$x_{mesh}, x_{uv} \gets \tau, \quad Q = \mathrm{PE}(x_{mesh})$$

- **交叉注意力编码**：通过从 UV 查询 $Q$ 到图像特征 $f_{img}$ 的交叉注意力，计算得到与视点和表情无关的化身码 $\mathcal{A}$：
  $$\mathcal{A} = \mathrm{ATTENTION}(Q, f_{img}, f_{img})$$

这一设计使化身码 $\mathcal{A}$ 仅编码身份几何与纹理信息，为后续的表情驱动和视点解耦奠定基础。

### 解码器 D：表情注入与高斯生成

解码器接收化身码 $\mathcal{A}$ 和表情代码 $z_{exp}$，通过交叉注意力将表情信息融入化身表示：

- **表情编码**：表情代码 $z_{exp}$ 经 MLP 映射为序列化的表情特征 $s_{exp}$：
  $$s_{exp} = \mathbf{MLP}(z_{exp})$$

- **Bias sink 拼接**：在表情序列后拼接偏差令牌 $z_{bias}$（训练时根据数据来源选择 $z_{2D}$ 或 $z_{3D}$，推理时固定为 $z_{3D}$）：
  $$s_{exp} \gets [s_{exp}, z_{bias}]$$

- **交叉注意力融合**：解码器内部通过交叉注意力将表情信息融入化身表示：
  $$h_{dec} = \mathrm{ATTENTION}(\mathcal{A}, s_{exp}, s_{exp})$$

解码器最终输出 3D 高斯的各项属性（位置、协方差、颜色、不透明度等），这些高斯随后被送入渲染器。

### 上采样器：StyleGAN-PixelShuffle 块

为提升渲染质量，FlexAvatar 在解码器特征图上应用了一种结合 **PixelShuffle** 和 **StyleGAN2 启发式 CNN 块** 的上采样架构，实现总计 8× 的上采样率：

$$h_{map}^{(l+1)} = \mathrm{PIXELSHUFFLE}(h_{map}^{(l)}) + \mathrm{CNN}(h_x^{(l+1)})$$

该设计（详见 Figure 3）有效增加了高斯数量，显著提升了最终渲染图像的视觉质量。

### 渲染器 R

渲染器采用来自 3DGS / gsplat 的基于 tiles 的可微分光栅化器，将解码出的 3D 高斯 $\mathcal{G}$ 从指定相机视点 $\pi$ 渲染为 2D 图像 $I^{pred}$。

### 训练损失

总重建损失由四项组成，结合了像素级和感知级监督：

$$\mathcal{L}_{rec} = \mathcal{L}_1 + \mathcal{L}_{SSIM} + \mathcal{L}_{DINO} + \mathcal{L}_{SAM}$$

其中 $\mathcal{L}_{DINO}$ 和 $\mathcal{L}_{SAM}$ 分别为基于 DINOv2 和 SAM 的感知损失，用于提升渲染图像的锐度和结构保真度。

### Bias Sinks 的核心作用

Bias sinks 是整个框架实现视角解耦的关键机制（详见 Figure 4）。在单目数据训练中，驱动信号（表情/头部姿态）与目标视点天然纠缠——当渲染相机与驱动相机相同时效果良好，但移动渲染相机时会出现明显伪影。通过引入 $z_{2D}$ 和 $z_{3D}$ 两个可学习令牌，模型在训练时显式区分数据来源：单目数据的纠缠效应被 $z_{2D}$ 吸收，多视图数据的解耦行为被 $z_{3D}$ 学习。推理时统一使用 $z_{3D}$，使模型生成完整且可泛化的 3D 头部化身，无需牺牲单目训练带来的泛化能力。

### 动画机制

与传统依赖 3DMM（如 FLAME）进行 rigging 的方法不同，FlexAvatar 采用 **无模型驱动** 方式：表情变换完全从数据中学习，通过解码器内部的交叉注意力融合表情代码 $z_{exp}$。这意味着网络不局限于 FLAME 的预定义表达空间，理论上可以学习更丰富的面部动画，也为后续替换驱动信号（如其他表情编码器）保留了灵活性。

FlexAvatar 的整个生成流程由四个核心模块串联构成，其数学形式可概括为三条主方程。

### 编码器 E：从图像到化身潜在码

编码器 E 将输入图像 $I$ 映射为一个与视点和表情无关的压缩化身表示 $\mathcal{A}$：

$$\mathcal{A} = E(I) \tag{1}$$

具体实现中，编码器首先从 $I$ 中提取图像特征 $f_{img}$，该特征由 DINOv2 和浅层 ViT 的特征拼接后经 MLP 得到：

$$f_{img} = \mathbf{MLP}([\mathbf{DINO}(I), \mathbf{ViT}([I, I^{pluck}])]) \tag{4}$$

随后，在 FLAME 模板网格的 UV 空间内均匀采样 3D 表面点，并对其施加正弦位置编码以生成查询 $Q$：

$$x_{mesh}, x_{uv} \gets \tau, \quad Q = \mathrm{PE}(x_{mesh}) \tag{5-6}$$

化身码 $\mathcal{A}$ 通过从 UV 锚定查询 $Q$ 到图像特征 $f_{img}$ 的交叉注意力计算得到：

$$\mathcal{A} = \mathrm{ATTENTION}(Q, f_{img}, f_{img}) \tag{7}$$

这一设计的核心直觉在于：UV 采样点提供了固定的 3D 空间锚点，交叉注意力机制则负责从 2D 图像特征中“检索”对应的外观信息，从而将单张图像提升为与视角无关的潜在 3D 表示。

### 解码器 D：表情驱动与高斯属性生成

解码器 D 的任务是将表情代码 $z_{exp}$ 融入化身表示，并输出一组可动画的 3D 高斯属性 $\mathcal{G}$：

$$\mathcal{G} = D(\mathcal{A}, z_{exp}) \tag{2}$$

表情代码首先经 MLP 映射为序列化的表情特征：

$$s_{exp} = \mathbf{MLP}(z_{exp}) \tag{8}$$

解码器内部通过交叉注意力将表情信息注入化身表示：

$$h_{dec} = \mathrm{ATTENTION}(\mathcal{A}, s_{exp}, s_{exp}) \tag{9}$$

与传统依赖 3DMM（如 FLAME）进行 rigging 的方法不同，FlexAvatar 采用无模型（model-free）的动画机制：网络直接从数据中学习表情变换，通过交叉注意力融合表情代码，无需依赖预定义的表达空间。这使得动画表达不再受限于 3DMM 的线性混合形状空间，为后续替换驱动信号（如语音或文本驱动的表情特征）保留了结构上的灵活性。

### 上采样器：StyleGAN-PixelShuffle 块

解码器输出的特征图需要上采样以增加高斯数量，从而提升渲染质量。FlexAvatar 提出了一种结合 PixelShuffle 和 StyleGAN2 启发式 CNN 块的上采样架构，总上采样倍率为 8×：

$$h_{map}^{(l+1)} = \mathrm{PIXELSHUFFLE}(h_{map}^{(l)}) + \mathrm{CNN}(h_x^{(l+1)}) \tag{10-11}$$

其中 PixelShuffle 负责高效的空间分辨率提升，StyleGAN2 风格的 CNN 块则通过调制-卷积-解调机制增强特征表达能力。这一设计在保持计算效率的同时，显著改善了渲染图像的视觉质量。

### 渲染器 R：可微分光栅化

渲染器 $\mathcal{R}$ 采用来自 3DGS/gsplat 的基于 tiles 的可微分光栅化器，将 3D 高斯集 $\mathcal{G}$ 从指定相机视角 $\pi$ 渲染为预测图像：

$$I^{pred} = \mathcal{R}(\mathcal{G}, \pi) \tag{3}$$

### Bias Sinks：视点-驱动解耦的关键机制

Bias sinks 是本文解决单目训练中“驱动信号与目标视点纠缠”这一瓶颈的核心创新。其数学形式极其简洁——仅需将可学习的偏差令牌拼接到表情序列：

$$s_{exp} \gets [s_{exp}, z_{bias}] \tag{16}$$

其中 $z_{bias} \in \{z_{2D}, z_{3D}\}$ 是两个可学习令牌。训练时，若输入图像 $I$ 来自单目数据集，则拼接 $z_{2D}$；若来自多视图数据集，则拼接 $z_{3D}$。推理时，始终使用 $z_{3D}$ 令牌。

这一机制的因果逻辑在于：单目视频中，驱动信号（表情/头部姿态）与目标视点天然相关（因为相机通常固定），导致模型学会利用这种“视角泄露”来预测外观，而非学习真正的 3D 结构。通过引入 bias sinks，模型被强制将这种数据集特有的偏差“吸收”到特定令牌中——$z_{2D}$ 承载单目数据的视角纠缠行为，$z_{3D}$ 承载多视图数据的解耦行为。推理时切换至 $z_{3D}$，模型即继承多视图数据的解耦特性，从而生成完整的 3D 头部，即使仅从单张图像输入。

### 训练损失

总重建损失由四项组成：

$$\mathcal{L}_{rec} = \mathcal{L}_1 + \mathcal{L}_{SSIM} + \mathcal{L}_{DINO} + \mathcal{L}_{SAM} \tag{21}$$

其中 $\mathcal{L}_1$ 和 $\mathcal{L}_{SSIM}$ 为像素级损失，$\mathcal{L}_{DINO}$ 和 $\mathcal{L}_{SAM}$ 分别为基于 DINOv2 和 SAM 的感知损失。消融实验表明，额外引入的感知损失显著提升了渲染图像的锐度和感知相似度。

## 实验与关键发现

FlexAvatar在四个任务和三个数据集上进行了系统评估，覆盖3D肖像动画、单图像化身创建、少样本化身创建和单目化身创建等场景（Table 1）。以下从核心定量结果、消融实验和失败模式三个维度展开分析。

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Kirschstein_FlexAvatar/figures/005_Table_1.jpg]]
*Table 1: Overview of Experimental Results. We evaluate FlexAvatar on 4 different tasks and 3 different datasets*

### 3D肖像动画：VFHQ基准

在VFHQ数据集上，FlexAvatar在自重演（self-reenactment）和跨重演（cross-reenactment）两种设定下均展现出竞争力。自重演任务中，FlexAvatar取得了**23.47 dB的PSNR**，在所有对比方法中表现最优（Table 2）。跨重演任务中，CSIM达到**0.663**，表明化身在身份保持与表情迁移之间取得了良好平衡。值得注意的是，FlexAvatar在除AKD（平均关键点距离）外的所有指标上均优于先前方法，而AKD的略高可能源于模型不依赖3DMM的刚性rigging，而是从数据中学习表情变换——这种无模型动画机制在极端表情下可能产生更自然的形变，但与FLAME关键点的对齐度略有下降。

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Kirschstein_FlexAvatar/figures/006_Table_2.jpg]]
*Table 2: 3D Portrait Animation comparison on the VFHQ dataset. We evaluate the ability to animate a single image by transferring facial motion and head pose from a driving video showing the same person (self-reenactment) or a different person (cross-reenactment)*

### 单图像化身创建：Ava256数据集

单图像化身创建是FlexAvatar的核心亮点。在Ava256数据集上，FlexAvatar取得了**16.9 dB的PSNR**，显著优于Avat3r、GAGAvatar等近期方法（Table 3）。定性结果（Figure 5）进一步验证了这一优势：FlexAvatar生成的3D头部在侧面和后脑区域保持了完整的几何结构，而基线方法往往在这些不可见区域出现空洞或模糊。这种完整性直接归因于bias sinks机制——推理时使用z3D令牌使模型继承了多视图数据的解耦行为，从而从单张正面肖像推断出全头3D表示。

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Kirschstein_FlexAvatar/figures/007_Table_3.jpg]]
*Table 3: Single-image and Few-shot Avatar Creation comparison on the Ava256 dataset*

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Kirschstein_FlexAvatar/figures/011_Figure_5.jpg]]
*Figure 5: Qualitative Single-image Avatar Creation comparison on the Ava256 dataset. We compare our method to the recent stateof-the-art on 3D head avatar creation from a single portrait image. Our method produces more complete 3D head avatars and re-enacts the target expression more faithfully*

### 少样本化身创建

当提供4张不同视角的图像时，FlexAvatar的PSNR提升至**21.1 dB**，相比单图像设定提升约4.2 dB（Table 3）。这一显著增益表明模型能够有效利用多视图信息来细化化身表示。具体实现中，模型先从一张图像编码得到初始化身码$A^{init}$，随后在保持解码器D冻结的情况下对该码进行1000步优化——这一策略避免了在稀疏输入上过拟合，同时允许身份细节的注入。

### 单目化身创建：NeRSemble基准

在NeRSemble基准上，FlexAvatar在LPIPS指标上显著优于先前方法（Table 4），表明渲染图像在感知质量上更接近真实照片。该基准评估从单目视频重建化身并渲染新视角和新表情的能力，FlexAvatar的优势再次印证了bias sinks对视角-表情纠缠的有效解耦。

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Kirschstein_FlexAvatar/figures/010_Table_4.jpg]]
*Table 4: Monocular Avatar Creation comparison on the NeRSemble Benchmark. We evaluate the ability to render novel views and novel expressions given monocular videos of 5 persons*

### 消融实验

消融实验（Table 5, Figure 7）系统验证了各组件对最终性能的贡献：

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Kirschstein_FlexAvatar/figures/014_Figure_7.jpg]]
*Figure 7: Qualitative Ablation of method components on the Ava256 dataset*

- **Bias sinks**：移除bias sinks后，模型生成的头部出现明显的不完整伪影，PSNR显著下降。这直接证明了bias sinks是解决单目训练中驱动-视角纠缠的关键机制。
- **StyleGAN-PixelShuffle上采样器**：完整架构（含该上采样器、bias sinks和感知损失）取得了**17.2 dB的PSNR**，且视觉质量明显优于消融变体。上采样器通过8×分辨率提升，使得3D高斯数量增加，从而支持更精细的几何和纹理表达。
- **感知损失**：额外使用DINOv2和SAM感知损失显著提高了渲染图像的锐度和感知相似度。消融中移除这些损失后，图像细节出现模糊，表明感知损失在保持高频纹理方面发挥了关键作用。
- **测试时拟合**：在保持解码器冻结的情况下对化身码进行200步拟合，可将CSIM提升至**0.682**，同时AKD下降，表明身份保持和表情保真度均得到改善。这一发现暗示编码器提供的初始化身码仍有优化空间，轻量级测试时优化是一种有效的补充策略。

### 失败模式与局限性

尽管FlexAvatar在受控基准上表现优异，但在以下场景中仍存在不足：

1. **极端遮挡与大角度姿态**：当前模型假设输入图像包含完整、清晰的人脸。当面部被严重遮挡或呈现极端侧脸时，编码器可能无法提取足够的身份信息，导致化身码质量下降。这一问题在野外测试中有所体现——复杂发型和配饰区域偶尔出现几何断裂。
2. **FLAME表达空间的限制**：动画表达依赖于FLAME提供的表达代码$z_{exp}$，这意味着超出FLAME预定义表达空间的表情（如极端夸张的嘴型或非对称微表情）可能无法被准确捕捉。尽管网络结构本身允许替换驱动信号，但论文未提供使用其他表达编码器的实验结果。
3. **优化时间**：化身创建过程需要数分钟优化（单图像约200步，少样本约1000步），尚未达到实时应用。对于需要即时生成化身的场景，这一延迟可能构成瓶颈。
4. **野外泛化**：在高度多样化的输入（如绘画、低分辨率照片）上，跨重演结果偶尔出现身份漂移或表情不自然，表明模型在分布外数据上的鲁棒性仍有提升空间。

### 关键图表结论

- **Figure 4**：直观展示了bias sinks解决的核心问题——单目训练中驱动信号与目标视点的纠缠。当渲染相机与驱动相机不同时，无bias sinks的模型出现明显虚影，而引入bias sinks后伪影消失。
- **Figure 5**：定性对比证实FlexAvatar在单图像化身创建中生成更完整的3D头部，尤其在非正面视角下优势显著。
- **Figure 7**：消融研究的可视化结果，直观呈现各组件对生成质量的贡献。
- **Table 5**：完整的消融定量结果，为架构设计选择提供了数据支撑。

## 定位与知识库关联

### 核心创新与差异化定位

FlexAvatar 的核心贡献在于提出一种**可学习偏差令牌（bias sinks）** 机制，首次系统性地解决了单目视频训练中驱动信号与目标视点固有纠缠的问题。这一创新使其在方法谱系中占据独特位置：它既不同于依赖3DMM强先验的传统方法，也不同于近期基于3D高斯泼溅（3DGS）但未显式处理数据偏差的工作。

具体而言，FlexAvatar 在以下几个维度上与现有工作形成差异化：

1. **与3DMM驱动方法的区别**：传统3D肖像动画方法（如 **Real3D-portrait**、**Voodoo XP**）依赖 FLAME 等3D可变形模型进行表情rigging，其动画能力受限于预定义的表达空间。FlexAvatar 采用无模型（model-free）的动画机制，通过交叉注意力直接从数据中学习表情变换（Section 3.2），理论上可捕捉更丰富的面部动态，且不依赖3DMM的参数化表达。

2. **与单图像化身方法的区别**：近期工作如 **LAM**、**Avat3r**、**GAGAvatar** 专注于从单张图像创建3D头部化身，但在单目训练范式下，它们普遍面临视角泄露问题——当渲染相机偏离驱动视角时产生虚影伪影。FlexAvatar 的 bias sinks 机制通过显式区分单目（z₂D）与多视图（z₃D）数据源，将视角纠缠效应限制在特定令牌中，推理时统一使用 z₃D 以获得解耦的多视图行为，从而生成完整的3D头部。

3. **与单目化身创建方法的区别**：**CAP4D**、**GaussianAvatars**、**FlashAvatar** 等方法从单目视频重建个性化头部化身，但通常需要逐身份优化（per-identity optimization），泛化能力有限。FlexAvatar 通过统一的编码器-解码器架构实现前馈推理，同时借助 bias sinks 在单目与多视图数据上联合训练，兼顾了泛化性与重建完整性。

### 技术组件溯源

FlexAvatar 的架构设计融合了多项已有技术，但其组合方式与改进形成了独特的方法论：

| 组件 | 技术来源 | FlexAvatar 的改进 |
|------|---------|-------------------|
| 编码器交叉注意力 | LAM 的 UV 锚点查询机制 | 引入 DINOv2 与浅层 ViT 拼接的图像特征提取（Eq. 4），增强语义感知能力 |
| 解码器动画机制 | Avat3r 的交叉注意力融合 | 将表情代码序列化并与偏差令牌拼接（Eq. 16），实现视角-表情解耦 |
| 上采样架构 | PixelShuffle + StyleGAN2 | 结合 PixelShuffle 与 StyleGAN2 启发的 CNN 块，实现 8× 上采样（Eq. 10-11），提升高斯数量与渲染质量 |
| 感知损失 | DINOv2、SAM | 额外引入 SAM 感知损失，提升结构保真度（Eq. 21），消融实验证实其对锐度和感知相似度的显著提升 |
| 3D 表示 | 3DGS 高斯泼溅 | 使用基于 tiles 的可微光栅化器（来自 3DGS/gsplat），保持高效渲染 |

### 适用边界与局限

尽管 FlexAvatar 在多个基准上取得了领先性能，其方法仍存在明确的适用边界：

1. **输入假设**：模型假设输入图像包含清晰、正面或近正面的人脸。对于极端遮挡、大角度姿态（如侧脸超过 90°）或严重模糊的输入，编码器提取的化身码可能质量下降，导致重建失真。这一局限在论文中未进行系统性消融验证，需在实际部署中注意。

2. **表情空间的依赖性**：虽然 FlexAvatar 的动画机制不依赖 3DMM 的 rigging 函数，但训练和推理中使用的表情代码 z_exp 仍来自 FLAME 模型。这意味着超出 FLAME 表达空间的表情（如极端的嘴部变形、非对称面部动作）可能无法被准确驱动。论文指出网络结构本身允许替换驱动信号，但未提供实验验证。

3. **野外场景的鲁棒性**：对于复杂发型（如卷发、长发遮挡面部）、配饰（眼镜、帽子）或非均匀光照条件，渲染质量可能出现瑕疵。Figure 8 展示了部分野外结果，但缺乏大规模定量评估。

4. **计算效率**：化身创建过程需要数分钟优化（单图像场景约 200 步拟合），尚未达到实时应用要求。对于需要即时生成化身的场景（如视频会议），这一延迟可能构成瓶颈。

5. **身份-表情耦合**：当前架构中身份信息与表情信息在解码器中通过交叉注意力融合，但未显式解耦。这可能导致在跨重演（cross-reenactment）时，驱动表情对源身份产生轻微干扰，表现为 CSIM 指标（0.663）仍有提升空间。

### 开放问题与后续方向

FlexAvatar 的 bias sinks 机制开辟了若干值得探索的研究方向：

1. **偏差令牌范式的泛化**：bias sinks 本质上是一种通过可学习令牌吸收数据源特定偏差的方法。这一范式是否可以扩展到其他数据稀缺场景？例如：
   - 人体姿态估计中，2D 标注与 3D 标注的联合训练
   - 通用动态新视角合成中，单目视频与多视图数据的混合训练
   - 文本到3D生成中，不同质量渲染数据的融合
   
   这些场景中，数据源的系统性偏差（如标注精度、视角分布）与 FlexAvatar 面临的单目/多视图纠缠问题具有结构相似性。

2. **身份与表情的进一步解耦**：能否引入显式的身份-表情解耦模块（如对比学习或正交约束），使化身可以独立控制身份插值和表情驱动？这将直接提升跨重演任务中的身份保持（CSIM）和表情保真度（AKD）。

3. **弱监督与多模态扩展**：当前方法依赖单张图像或单目视频。是否可以：
   - 利用文本描述作为弱监督信号，指导特定属性（如发型、年龄）的化身生成？
   - 结合音频驱动，实现语音到面部动画的端到端映射？
   
   这些扩展将显著拓宽 FlexAvatar 的应用场景，但需要解决多模态对齐和生成质量控制等挑战。

4. **实时化与轻量化**：化身创建的数分钟延迟限制了实时应用。可能的优化方向包括：
   - 知识蒸馏，将优化过程压缩为单步前馈推理
   - 高斯剪枝与量化，减少渲染计算量
   - 渐进式上采样，在低分辨率下快速预览

5. **极端姿态与遮挡的鲁棒性**：当前模型未针对大角度姿态和遮挡进行专门设计。引入姿态感知的特征提取或遮挡感知的注意力掩码，可能提升在野外场景下的泛化能力。

### 知识库定位总结

FlexAvatar 位于 **3D头部化身创建与动画** 的交叉点，其方法论贡献可归纳为：

- **核心机制**：bias sinks——一种数据源偏差吸收机制，通过可学习令牌实现单目/多视图联合训练中的视角解耦
- **技术融合**：将 UV 锚点查询、交叉注意力动画、StyleGAN-PixelShuffle 上采样、3DGS 渲染与多尺度感知损失整合为统一框架
- **适用场景**：单图像化身创建、少样本化身创建、3D肖像动画（自重演/跨重演）、单目视频化身创建
- **方法边界**：依赖清晰正面输入、受限于 FLAME 表达空间、计算效率待优化、野外鲁棒性未充分验证

在更广泛的 3D 视觉知识库中，FlexAvatar 的 bias sinks 思想可被视为一种**数据偏差感知的训练策略**，与领域自适应（domain adaptation）、多任务学习中的数据平衡方法形成互补，为数据稀缺场景下的 3D 重建提供了新的解决思路。

## 原文 PDF

![[paperPDFs/CVPR_2026/FlexAvatar_Learning_Complete_3D_Head_Avatars_with_Partial_Supervision.pdf]]
