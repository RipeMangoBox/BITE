---
title: "Vista4D: Video Reshooting with 4D Point Clouds"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Vista4D_Video_Reshooting_with_4D_Point_Clouds.pdf
project_link: null
code_link: null
aliases:
- Vista4D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 时间持久的4D点云表示（通过静态像素持久化）和在训练中引入带有深度伪影的4D重建多视图数据，使模型学会纠正不完美几何，并结合源视频的上下文条件保持外观一致性。
primary_logic: 通过分割和4D重建使静态像素在时间上持久化，构建4D点云作为显式先验；训练时刻意暴露非正面视图的深度估计伪影，并联合源视频进行上下文条件，使得视频扩散模型能够鲁棒地修补不完美几何和外观，同时实现高精度的相机控制。
claims:
- 用户研究中，Vista4D在内容保留、相机控制精度和总体保真度上均大幅优于基线（总体偏好77.38% vs 最高基线11.03%）
- 在所有相关指标上，Vista4D的相机控制精度（平移误差、旋转误差、内参误差）和3D一致性（RE@SG）均达到最优
- 在iPhone数据集上的新视角视频合成中，Vista4D在PSNR、LPIPS和运动重建（EPE）上均显著优于基线
- 去除深度伪影训练和上下文源视频条件会导致几何伪影和时间抖动
---

# Vista4D: Video Reshooting with 4D Point Clouds

> [!tip] 核心洞察
> 通过分割和4D重建使静态像素在时间上持久化，构建4D点云作为显式先验；训练时刻意暴露非正面视图的深度估计伪影，并联合源视频进行上下文条件，使得视频扩散模型能够鲁棒地修补不完美几何和外观，同时实现高精度的相机控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | Vista4D：基于4D点云的视频重新拍摄 |
| 英文题名 | Vista4D: Video Reshooting with 4D Point Clouds |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.21915) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Vista4D |
| Dataset | 110 video-camera pairs 评估数据集, iPhone 数据集 |

> [!tip] 效果简介
> - 110 video-camera pairs 评估数据集 上，Translation Error ↓ 1.251 vs 1.574 (ReCamMaster) (-0.323)；RE@SG ← (3D一致性) 7.504 vs 12.99 (GEN3C) (-5.486)；FID ← 105.4 vs 94.15 (ReCamMaster) (+11.25)。
> - iPhone 数据集 上，mPSNR ↑ 14.09 vs 13.82 (TrajectoryCrafter) (+0.27)；EPE ← (运动重建) 1.142 vs 2.375 (TrajectoryCrafter) (-1.233)。
> - 用户研究 上，Overall fidelity preference 77.38% vs 11.03% (CamCloneMaster) (+66.35pp)。

## 概要

### 问题与瓶颈

视频重拍（video reshooting）要求从新的相机轨迹和视角重新合成同一动态场景的视频，同时严格保留原始场景的内容与运动。现有方法面临两个核心瓶颈：其一，面对真实世界单目动态视频时，深度估计产生的几何伪影会导致内容保留失败和相机控制不精确；其二，训练阶段通过双重投影（double reprojection）获得的无伪影点云渲染，与推理时来自4D重建的多视图点云伪影分布严重不匹配，使模型对真实场景的鲁棒性不足。

### 核心思路

Vista4D 提出了一种以**时间持久的4D点云**为显式先验的视频重拍框架。其核心洞察在于：通过分割与4D重建使静态像素在所有帧中保持时间持久性，构建一个世界坐标系下的4D点云表示；同时在训练中刻意暴露非正面视图带来的深度估计伪影，并结合源视频的上下文条件（in-context conditioning），迫使视频扩散模型学会鲁棒地修补不完美几何并保持外观一致性。这一设计使得模型能够在精确遵循目标相机轨迹的同时，从源视频中自适应地纠正点云伪影。

### 方法谱系与知识库定位

视频重拍方法可依据先验类型分为两大谱系：

- **隐式先验方法**：通过相机嵌入或参考视频隐式引导生成。如 **ReCamMaster** 和 **CamCloneMaster** 属于此类，相机控制精度较低，输出视频倾向于保持与源视频相似的静态相机。
- **显式先验方法**：通过3D/4D几何表示提供显式引导。如 **TrajectoryCrafter**（逐帧点云）、**EX-4D**（深度水密网格）和 **GEN3C**（3D缓存）。这些方法面临深度伪影鲁棒性不足的问题。

Vista4D 属于显式先验谱系，但通过三个关键改进区别于现有工作：（1）将逐帧3D点云升级为**时间持久的4D点云**，使静态像素跨帧可见；（2）在训练数据中引入**多视图4D重建的非正面伪影**，而非依赖双重投影的无伪影渲染；（3）采用**沿帧维度串联的上下文条件**策略联合处理源视频与点云渲染，而非简单的交叉注意力注入。方法基座为微调的 **Wan2.1-T2V-14B** 视频扩散变换器。

### 主要结果概要

在涵盖110个视频-相机对的评估数据集上，Vista4D 在所有相机控制精度指标上均达到最优：平移误差 1.251、旋转误差和內参误差均显著优于最强基线（Table 1）。3D一致性方面，SuperGlue重投影误差（RE@SG）为 7.504，较最佳基线 GEN3C（12.99）降低 42%。在iPhone数据集的新视角视频合成中，运动重建误差（EPE）为 1.142，显著优于 TrajectoryCrafter（2.375）（Table 2）。用户研究中，Vista4D 以 77.38% 的总体偏好率大幅超越最高基线（11.03%），在内容保留、相机控制精度和总体保真度三个维度均获压倒性优势（Table 4）。

消融实验证实：联合使用带深度伪影的训练数据与上下文源视频条件是模型鲁棒纠正几何伪影、避免时间抖动的关键（Figure 19）；去除静态像素的时间持久性则导致已见内容保留失败和相机控制精度下降（Figure 20）。

### 视频重拍的愿景与核心矛盾

视频重拍（video reshooting）的目标是，给定一段单目动态场景视频，从用户指定的全新相机轨迹和视角重新合成同一场景、同一动态的视频。这一任务在影视创作、增强现实和虚拟内容生成中具有广泛的应用前景。然而，实现高质量视频重拍面临一个根本性矛盾：模型必须同时精确控制新相机视角下的几何结构，又忠实保留源视频中的动态内容和外观细节。

现有方法在这一矛盾上存在系统性缺陷。基于隐式先验的方法，如 **ReCamMaster** 和 **CamCloneMaster**，通过相机嵌入或参考视频隐式地编码几何信息，在视频保真度指标上表现尚可，但相机控制精度严重不足——当目标相机与源相机差异较大时，生成视频的相机轨迹与用户指定轨迹之间存在显著偏差。基于显式先验的方法，如 **TrajectoryCrafter**（点云条件）、**EX-4D**（深度水密网格条件）和 **GEN3C**（3D缓存条件），虽然通过显式几何表示提供了更强的相机控制能力，却在面对真实世界视频时暴露出致命的鲁棒性问题。

### 真实瓶颈：深度估计伪影与分布不匹配

这一鲁棒性问题的根源在于一个被现有工作普遍忽视的“伪影鸿沟”。从单目视频重建3D/4D点云的过程依赖深度估计，而深度估计在非正面视角、遮挡边界和动态区域不可避免地产生伪影——表现为点云的缺失、漂移和几何畸变。现有方法在构造训练数据时，通常采用**双重投影（double reprojection）**策略：将目标视角的点云先渲染到源视角，再重新渲染回目标视角。这一操作确保训练时模型看到的点云渲染始终来自深度图的“正面”视角，点云伪影被人为消除（见 Figure 3）。

然而，在推理阶段，模型面对的是直接从源视频点云渲染到目标视角的图像——此时目标视角恰是深度估计的“非正面”视角，点云伪影充分暴露。这种训练与推理之间的**深度伪影分布不匹配**，导致现有显式先验方法在真实场景中频繁出现几何错误、内容撕裂和时间抖动，严重限制了其实际可用性。

### 内容保留与相机控制的耦合困境

更深层的问题在于，内容保留和相机控制并非独立维度。当点云存在伪影时，模型若严格遵循点云几何，会将伪影传播到输出视频；若依赖生成先验“修补”伪影，又可能偏离目标相机轨迹或丢失源视频中的动态细节。现有方法缺乏一种机制，使模型能够在遵循显式几何先验与利用视频生成先验之间进行自适应权衡。这一困境在静态像素的处理上尤为突出：逐帧独立的3D点云表示使静态区域在不同帧之间失去时间连续性，导致模型难以在目标相机与源视频帧重叠较少的区域保留已见静态内容。

### 本文动机：以4D持久点云弥合伪影鸿沟

针对上述瓶颈，Vista4D 的动机是构建一种**对真实世界点云伪影鲁棒**的视频重拍框架，同时保持高精度的相机控制和内容保真度。核心思路包含三个相互耦合的设计：

1. **时间持久的4D点云表示**：通过对源视频进行分割和4D重建，使静态像素在世界空间中跨帧持久可见，为视频扩散模型提供时间一致的显式几何先验。
2. **训练中暴露深度伪影**：使用4D重建的多视图动态视频作为训练数据，其中非正面视角的点云渲染天然携带深度估计伪影，使模型学会在推理时纠正不完美几何。
3. **上下文源视频条件**：将源视频与点云渲染沿帧维度串联作为上下文条件（in-context conditioning），使模型能够从源视频中传播几何和外观信息，鲁棒地修补点云伪影。

通过将视频重拍建立在4D持久点云这一显式先验之上，Vista4D 旨在同时实现精确的相机控制、忠实的动态内容保留，以及对真实世界深度估计伪影的强鲁棒性。

## 核心方法与创新机理

Vista4D 的核心创新在于构建了一个**时间持久的 4D 点云表示**，并通过**训练策略与条件机制的双重设计**，使视频扩散模型能够鲁棒地纠正真实世界点云中的几何伪影，从而实现高精度的相机控制与内容保留。其相对于现有基线（如 ReCamMaster、TrajectoryCrafter、GEN3C 等）的关键改进体现在以下三个 changed slots 上。

### 1. 从逐帧 3D 到时间持久的 4D 点云

现有显式先验方法（如 TrajectoryCrafter）将源视频逐帧提升为 3D 点云，但各帧之间缺乏显式的静态结构关联。Vista4D 通过**分割与 4D 重建**使静态像素在时间上持久化：先用 Grounded SAM 2 获取动态像素掩码，反转得到静态像素掩码；再将静态掩码应用于各帧世界空间点云，使静态点跨帧可见（Section 3.1）。这一设计使得从任意目标相机视角渲染点云时，源视频中已见过的静态区域能够被完整保留，而不会因帧间信息缺失产生空洞或内容丢失。

消融实验（Supplementary F.2, Figure 20）证实：去除时间持久性后，模型难以保留源视频中的静态内容（如雪山、金属栅栏），且在目标相机与源帧重叠较少时相机控制精度显著下降。

### 2. 训练数据中主动引入深度伪影

传统方法（如 TrajectoryCrafter 的双重投影策略）通过将目标视频点云先渲染回源相机视角、再重新渲染到目标相机，来构造无伪影的训练对（Figure 3a）。这导致训练时点云始终从正面视角观察深度图，与推理时真实世界 4D 重建产生的非正面视角伪影分布严重不匹配。

Vista4D 改用**多视角动态视频的 4D 重建数据**直接训练：将源视频点云从目标相机渲染，使模型在训练阶段就暴露于空间错位、拖影等典型深度估计伪影（Figure 3b）。这一策略的关键在于让模型学会**利用上下文源视频来纠正不完美几何**，而非被动依赖点云精度（Section 3.2）。消融实验（Supplementary F.1, Figure 19）表明：若移除深度伪影训练，输出视频会出现明显的几何伪影和时间抖动。

### 3. 上下文源视频条件策略

在条件注入方式上，现有方法或仅依赖点云渲染（如 TrajectoryCrafter），或通过交叉注意力注入源视频。Vista4D 采用**沿帧维度串联源视频与点云渲染的潜在 token** 进行上下文条件（in-context conditioning），并联合 alpha 掩码（Section 3.3）。这种设计使模型能够直接从源视频中传播几何和外观信息到输出视频，相比交叉注意力具有更强的自适应纠正能力。

消融实验（Supplementary F.1, Figure 19）对比了无源视频条件、交叉注意力注入和上下文串联三种策略：交叉注意力在部分场景下无法充分纠正伪影（如后退镜头中汽车异常放大），而上下文串联结合深度伪影训练是鲁棒性的关键组合。

Vista4D 的整体 pipeline 围绕一个核心思想构建：**将输入视频与用户指定的目标相机轨迹共同锚定在一个时间持久的 4D 点云表示中**，然后利用微调的视频扩散模型在该显式先验的引导下生成目标视角的视频。整个框架由三个紧密耦合的阶段组成，其端到端流程如 Figure 2 所示。

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2604_21915/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Vista4D. Given an input source video, we build a 4D point cloud where static pixels are temporally persistent via segmentation and 4D reconstruction. We then render the point cloud in the target cameras which users define. Lastly, the source video and point cloud render & alpha mask are jointly processed by the finetuned video diffusion model to generate a video of the same dynamic scene in the target cameras. We provide model architecture details in Supplementary B*

### 阶段一：时间持久 4D 点云的构建

给定一段输入源视频，系统首先借助现成的 4D 重建方法（如 π3 或 STream3R）估计逐帧的深度图、相机外参和内参。通过逆透视投影和世界空间变换，将源视频的每一帧提升为世界坐标系下的 3D 点云：

$$\mathbf{P} = \Omega\left(\Phi^{-1}\left(\left[\mathbf{X}^{\mathrm{src}}, \mathbf{D}^{\mathrm{src}}\right], \mathbf{K}^{\mathrm{src}}\right), \mathbf{T}^{\mathrm{src}}\right)$$

其中 $\mathbf{X}^{\mathrm{src}}$ 为源视频帧，$\mathbf{D}^{\mathrm{src}}$ 为估计深度，$\mathbf{K}^{\mathrm{src}}$ 为相机内参，$\mathbf{T}^{\mathrm{src}}$ 为相机外参。这一步骤将 2D 像素提升为世界空间中的 3D 点。

然而，直接逐帧拼接得到的点云存在一个关键缺陷：**静态像素在不同帧之间是重复且孤立的**，缺乏跨帧的关联性。Vista4D 的突破在于通过分割实现静态像素的时间持久化。具体而言，系统使用 Grounded SAM 2 获取动态物体的像素掩码，将其反转得到静态像素掩码，并仅将静态像素对应的 3D 点在世界空间中跨帧保留。这使得一座山、一面墙等静态场景元素在所有帧中可见，形成一个真正意义上时间持久的 4D 点云。该点云随后在用户定义的目标相机轨迹上进行渲染，输出点云渲染图像 $\mathbf{X}^{\mathrm{src} \to \mathrm{tgt}}$ 及其 alpha 掩码 $\mathbf{M}^{\mathrm{src} \to \mathrm{tgt}}$，作为后续生成阶段的显式几何先验。

### 阶段二：带有深度伪影的训练策略

真实世界视频的 4D 重建不可避免地会产生深度估计伪影，尤其当从非正面视角观察深度图时，这些伪影表现为空间错位的点云条纹或孔洞。传统方法（如 **TrajectoryCrafter**）通过“双重投影”策略回避这一问题：始终从正面视角渲染深度图，从而获得无伪影的点云渲染。然而，这导致训练数据与推理时的伪影分布严重不匹配，模型在真实场景中缺乏对不完美几何的鲁棒性。

Vista4D 反其道而行之，**刻意在训练中暴露这些伪影**。系统使用 4D 重建的多视图动态视频作为训练数据，直接从非正面视角渲染源视频的点云到目标相机，使模型在训练阶段就面对与推理时一致的深度伪影（Figure 3）。这种“以毒攻毒”的策略迫使模型学会利用其他条件信号来纠正不完美几何。

### 阶段三：上下文条件视频扩散模型

生成阶段基于一个微调的视频扩散变换器（以 Wan2.1-T2V-14B 为基座）。其核心创新在于**上下文条件（in-context conditioning）**策略：将源视频 $\mathbf{X}^{\mathrm{src}}$ 与点云渲染 $\mathbf{X}^{\mathrm{src} \to \mathrm{tgt}}$ 沿帧维度串联，与 alpha 掩码 $\mathbf{M}^{\mathrm{src} \to \mathrm{tgt}}$ 一同作为条件输入。同时，目标相机参数以 Plücker 嵌入的形式注入扩散变换器的每个块中。

训练目标为流匹配损失：

$$\mathcal{L} = \epsilon_{\theta}(\mathbf{X}_{t}^{\mathrm{tgt}}, \mathbf{X}^{\mathrm{src} \to \mathrm{tgt}}, \mathbf{M}^{\mathrm{src} \to \mathrm{tgt}}, \mathbf{X}^{\mathrm{src}}, \mathbf{C}^{\mathrm{tgt}}, t) - \mathbf{V}$$

其中 $\mathbf{C}^{\mathrm{tgt}}$ 为目标相机嵌入，$\mathbf{V}$ 为流向量。该设计使模型能够同时利用显式先验（点云渲染提供粗略几何）和隐式先验（源视频提供外观和运动信息），在两者之间自适应地传播几何与外观信息。对于没有真实源视频的单目训练数据，系统使用 $\mathbf{X}^{\mathrm{tgt} \to \mathrm{src}}$（即从目标视频渲染到源视角的遮挡版本）作为替代，确保训练信号的完整性。

### 输入输出流总结

- **输入**：一段源视频 + 用户定义的目标相机轨迹
- **中间表示**：时间持久的 4D 点云 → 目标视角的点云渲染与 alpha 掩码
- **输出**：在目标相机下、保持源视频动态与外观的新视频
- **关键控制信号**：点云渲染（显式几何）、源视频（外观与运动）、相机嵌入（视角控制）、alpha 掩码（遮挡指示）

这种三阶段设计使得 Vista4D 能够将视频重拍任务分解为几何重建与外观生成两个子问题，并通过上下文条件将二者有机融合，从而在相机控制精度、内容保留和 3D 一致性上均达到最优水平（Table 1）。模型架构的详细配置见 Figure 16。

Vista4D 的方法框架由三个核心模块构成：4D 点云构建、带有深度伪影的训练数据生成、以及扩散模型的条件化策略。以下逐一剖析各模块的设计逻辑与关键公式。

### 3.1 时间持久的 4D 点云构建

给定一段源视频，首先使用 4D 重建方法（如 π3 或 STream3R）估计每帧的深度图、相机外参和内参。随后，将源视频的每一帧通过逆透视投影和世界空间变换提升为世界坐标系下的逐帧 3D 点云：

$$\mathbf{P} = \Omega\left(\Phi^{-1}\left(\left[\mathbf{X}^{\mathrm{src}}, \mathbf{D}^{\mathrm{src}}\right], \mathbf{K}^{\mathrm{src}}\right), \mathbf{T}^{\mathrm{src}}\right)$$

其中，$\mathbf{X}^{\mathrm{src}}$ 为源视频帧，$\mathbf{D}^{\mathrm{src}}$ 为估计的深度图，$\mathbf{K}^{\mathrm{src}}$ 为相机内参矩阵，$\mathbf{T}^{\mathrm{src}}$ 为相机外参，$\Phi^{-1}$ 表示逆透视投影操作，$\Omega$ 表示世界空间变换。该公式将像素从图像空间映射到统一的世界坐标系中。

**时间持久性的实现**：仅靠上述逐帧点云无法保证静态区域（如背景建筑、地面）在不同帧之间的一致性——由于深度估计误差和相机位姿漂移，同一静态像素在不同帧可能被映射到不同的世界坐标。Vista4D 的解决方案是引入分割驱动的静态像素持久化：使用 Grounded SAM 2 获取动态像素掩码，将其反转得到静态像素掩码，然后将该掩码应用于各帧点云。这意味着静态像素只在它们首次被观测的帧中保留其点云位置，并在所有后续帧中保持可见，从而构建出一个静态区域在时间上一致的 4D 点云。最后，在用户指定的目标相机视角下渲染该持久点云，得到点云渲染图像 $\mathbf{X}^{\mathrm{src} \to \mathrm{tgt}}$ 及其 alpha 掩码 $\mathbf{M}^{\mathrm{src} \to \mathrm{tgt}}$，作为后续扩散模型的时间持久、4D-grounded 先验。

### 3.2 深度伪影训练数据

传统方法（如 TrajectoryCrafter）通过双重投影生成训练数据：先将目标视频的点云渲染到源相机视角，再重新渲染回目标相机视角以制造遮挡区域。这一过程始终从正面视角观察深度图，因此训练数据中的点云渲染几乎不含深度估计伪影（Figure 3a）。

然而，在推理阶段，模型面对的是从目标相机直接渲染源视频点云的结果——由于目标相机与源相机视角不同，深度图中的非正面区域会暴露出明显的深度估计伪影（如几何扭曲、空洞、条纹等）。这种训练-推理分布不匹配是现有方法在真实世界视频上表现不佳的关键瓶颈。

Vista4D 的训练策略是：直接使用 4D 重建的多视角动态视频对，从目标相机渲染源视频点云（Figure 3b）。这使训练数据中的点云渲染天然包含非正面视角带来的深度伪影，与推理时的分布一致。模型在训练中被迫学会利用源视频的上下文信息来纠正这些不完美几何，从而获得对现实世界点云伪影的鲁棒性。

### 3.3 扩散模型的条件化与训练目标

Vista4D 基于 Wan2.1-T2V-14B 视频扩散变换器进行微调。模型的条件输入包括四类：
- **点云渲染** $\mathbf{X}^{\mathrm{src} \to \mathrm{tgt}}$ 与 **alpha 掩码** $\mathbf{M}^{\mathrm{src} \to \mathrm{tgt}}$：提供显式的 4D 几何先验；
- **源视频** $\mathbf{X}^{\mathrm{src}}$：通过沿帧维度与点云渲染的潜在 token 串联，实现上下文条件化，使模型能够从源视频中传播几何和外观信息；
- **目标相机参数** $\mathbf{C}^{\mathrm{tgt}}$：以 Plücker 嵌入的形式注入扩散变换器的每个块，提供精确的相机控制信号。

训练采用流匹配目标：

$$\mathcal{L} = \epsilon_{\theta}(\mathbf{X}_{t}^{\mathrm{tgt}}, \mathbf{X}^{\mathrm{src} \to \mathrm{tgt}}, \mathbf{M}^{\mathrm{src} \to \mathrm{tgt}}, \mathbf{X}^{\mathrm{src}}, \mathbf{C}^{\mathrm{tgt}}, t) - \mathbf{V}$$

其中，$\mathbf{X}_{t}^{\mathrm{tgt}}$ 是加噪后的目标视频，$\mathbf{V}$ 是目标速度场，$\epsilon_{\theta}$ 为扩散变换器预测的噪声成分，$t$ 为时间步。模型通过最小化该损失，学习在点云先验、源视频上下文和目标相机参数的联合条件下生成与目标视频一致的输出。

对于仅有单目视频的训练数据（无真实 $\mathbf{X}^{\mathrm{src}}$），模型以 $\mathbf{X}^{\mathrm{tgt} \to \mathrm{src}}$（即从源相机渲染目标视频点云得到的遮挡源视频）及其 alpha 掩码作为替代条件，使模型仍能学习从遮挡观测中传播信息的能力。

### 3.4 关键设计决策的因果链

上述三个模块形成了一条清晰的因果链：**时间持久点云**解决了静态内容在不同帧间的几何一致性问题，使模型在目标相机与源视频帧重叠较少时仍能保持精确的相机控制；**深度伪影训练**弥合了训练-推理分布差异，使模型学会纠正不完美几何而非简单复制点云伪影；**上下文源视频条件化**（帧串联方式）相比交叉注意力注入具有更强的自适应性，能够在点云几何严重错误时依赖源视频的外观信息进行修补。消融实验证实，联合使用深度伪影训练与上下文源视频条件是模型鲁棒性的必要条件——单独移除任一项都会导致输出出现明显的几何伪影或时间抖动（Supplementary F.1）；而去除静态像素的时间持久性则会导致静态内容保留不佳和相机控制精度下降（Supplementary F.2）。

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2604_21915/figures/020_Figure_16.jpg]]
*Figure 16: Model architecture. The above diagram shows the model architecture for Vista4D. The fire icon indicates trainable parameters. We build upon Wan2.1-T2V-14B [2], and we omit timestep conditioning, text prompt to token embedding, modulation, layer normalization, output unshuffle, and diffusion model denoising in the diagram for simplicity. All patchify layers are initialized from the base video model besides that of the point cloud render alpha mask, which is zero-initialized. The camera encoder is zero-initialized, and the projector after self-attention is initialized as the identity affine transformation*

## 实验与关键发现

### 核心实验设置

所有定量评估统一在 $672 \times 384$ 分辨率下进行，以消除分辨率差异对指标的影响。评估数据集包含 110 个视频-相机对，覆盖多样化的真实世界动态场景。由于部分基线方法（ReCamMaster、CamCloneMaster、EX-4D、GEN3C）基于 I2V 模型且不支持第一帧源相机与目标相机不同，评估时采用 TrajectoryCrafter 的 infer-direct 模式：将第一帧点云固定，并将源第一帧相机移至目标第一帧相机后再进行推理，以确保公平比较。

### 相机控制精度与3D一致性

Table 1 报告了各方法在相机控制精度和3D一致性上的定量对比。Vista4D 在所有相关指标上均达到最优：

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2604_21915/figures/004_Table_1.jpg]]
*Table 1: Camera control accuracy and 3D consistency. Vista4D consistently shows the most accurate camera control compared to baselines with superior rotation, translation, and intrinsics errors. Our method also significantly outperforms baselines in per-frame 3D consistency with the lowest reprojection error under SuperGlue (RE@SG) [57–59]. Bold indicates best results*

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2604_21915/figures/006_Table_3.jpg]]
*Table 3: Video fidelity. Vista4D consistently outperform point-cloud-conditioned (explicit-prior) baselines for the video fidelity metrics FID, FVD, CLIP-T, and metrics from VBench [61] and VBench-2.0 [62]. Implicit-prior methods (ReCamMaster and CamCloneMaster) outperform our method in some metrics due to their low camera control accuracy (Table 1) that result in output videos with similar, usually more static, cameras to the input video which produces better FID, FVD, and VBench consistency metrics. Bold indicates best results*

- **平移误差**：Vista4D 达到 1.251，相比表现最好的隐式先验基线 ReCamMaster（1.574）降低了 0.323，降幅约 20.5%。这意味着生成视频的相机轨迹在空间位置上更精确地遵循用户指定的目标路径。
- **旋转误差和焦距误差**：Vista4D 同样取得最低值，表明模型能够准确复现目标相机的朝向和视场角。
- **3D一致性（RE@SG）**：Vista4D 取得 7.504，显著优于最佳基线 GEN3C 的 12.99，相对提升约 42.2%。RE@SG 通过 SuperGlue 特征匹配计算重投影误差，衡量生成视频各帧之间的三维几何一致性。这一优势直接源于时间持久的4D点云表示——静态像素在世界空间中跨帧可见，为生成过程提供了稳定的几何锚点。

### 新视角视频合成

Table 2 报告了在 iPhone 数据集上的新视角视频合成质量。该数据集提供多相机同步拍摄的真值视频，可直接评估生成视频与真值之间的像素级和感知级差异：

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2604_21915/figures/005_Table_2.jpg]]
*Table 2: Novel-view video synthesis. Vista4D shows comparable to superior noel-view video synthesis performance on the iphone dataset [60]. EPE (endpoint error) measures optical flow error between the generated and ground truth videos and indicates scene motion reconstruction. Bold indicates best results*

- **PSNR 和 LPIPS**：Vista4D 在 PSNR（14.09）和 LPIPS 上优于所有基线，表明生成的像素值和感知特征更接近真值。TrajectoryCrafter 的 PSNR 为 13.82，差距虽小但一致。
- **运动重建（EPE）**：Vista4D 的端点误差仅为 1.142，而 TrajectoryCrafter 为 2.375，降幅超过 50%。EPE 衡量生成视频与真值视频之间的光流误差，直接反映场景动态重建的准确度。这一显著优势说明，通过分割使静态像素持久化、仅让动态像素逐帧变化，模型能够更精确地保留原始场景的运动模式，而非依赖生成先验“猜测”运动。

### 视频保真度与生成质量

Table 3 报告了视频保真度指标。Vista4D 在所有指标上一致优于基于显式先验（点云/网格/3D缓存）的基线方法（TrajectoryCrafter、GEN3C、EX-4D），验证了带深度伪影训练和上下文源视频条件的有效性。

值得注意的一个反直觉现象是：隐式先验方法（ReCamMaster、CamCloneMaster）在 FID（94.15 vs 105.4）、FVD 和部分 VBench 一致性指标上优于 Vista4D。论文明确指出，这是因为隐式先验方法的相机控制精度较低（见 Table 1），其输出视频的相机运动往往与源视频相似甚至更静态，从而在分布统计上与训练数据更接近，产生了“虚假”的高保真度分数。这一分析揭示了相机控制精度与视频保真度指标之间的内在权衡——更精确地遵循用户指定的新相机轨迹，意味着生成视频的分布偏离源视频更远，FID 等分布度量自然会升高。

### 用户研究

Table 4 报告了用户研究结果，这是对上述定量指标的最终验证。参与者在三个维度上进行偏好判断：

- **内容保留**：Vista4D 获得 77.38% 的偏好，而最高基线 CamCloneMaster 仅 11.03%。
- **相机控制精度**：Vista4D 获得 77.38% 的偏好，最高基线仅 11.03%。
- **总体保真度**：Vista4D 获得 77.38% 的偏好，最高基线仅 11.03%。

三个维度的一致性偏好（均为 77.38% vs 约 11%）强烈表明，Vista4D 在保持源视频外观、精确遵循目标相机、以及整体视觉质量上均实现了显著超越，且这种优势在人类感知层面是高度一致的。

### 消融实验

消融实验揭示了三个关键设计选择的因果作用：

**深度伪影训练与源视频条件**（Supplementary F.1，Figure 19）。联合使用带深度伪影的训练数据与上下文源视频条件，是模型鲁棒纠正点云伪影的充分必要条件。单独移除深度伪影训练（始终使用双重投影生成无伪影渲染），模型在推理时遇到非正面视图的深度估计误差时会产生明显的几何伪影和时间抖动。单独移除上下文源视频条件（替换为无源视频或交叉注意力注入），模型无法有效利用源视频的外观和几何信息来修补不完美点云。交叉注意力注入虽然在某些情况下能纠正伪影，但缺乏自适应性——例如当相机向后飞离时，生成结果中的物体尺寸仍异常偏大。

**静态像素的时间持久性**（Supplementary F.2，Figure 20）。去除时间持久性后，模型难以保留源视频中已见的静态内容（如雪山、金属栅栏），且在目标相机与源视频帧重叠较少时相机控制精度显著下降。这验证了时间持久点云的核心作用：为模型提供跨帧稳定的几何参照，使其在目标视角偏离源视角时仍能准确推断场景结构。

**分割失败的鲁棒性**（Figure 6）。通过故意不将网球拍分割为动态对象，模拟分割失败场景。结果显示，Vista4D 能够利用上下文源视频条件纠正因错误分割产生的点云拖影伪影，体现了模型对4D重建不完美的整体鲁棒性——这一鲁棒性正是深度伪影训练和源视频条件联合作用的结果。

### 推理效率

Table 5 报告了预处理和推理时间。预处理包括 Grounded SAM 2 分割和4D重建，推理为扩散模型的多步去噪过程。具体数值需查看原文表格，但整体流程在单次视频重拍任务中是可接受的，且4D点云构建为一次性开销，支持同一场景的多次重拍复用。

### 失败模式与局限

尽管 Vista4D 展现出显著的鲁棒性，论文明确指出了两个局限：

1. **缺乏显式控制机制**：目前模型无法让用户调节“遵循点云几何”与“依赖视频先验纠正”之间的权衡。当点云质量极差时，模型虽然能利用源视频纠正，但用户无法控制纠正的激进程度。论文建议未来增加一种在显式先验（点云）和隐式先验（源视频/相机嵌入）之间插值的控制信号。

2. **内容偏见与伦理问题**：作为基于大规模预训练视频扩散模型的方法，Vista4D 继承了训练数据中的内容偏见，并可能被用于生成误导性内容或侵犯隐私。在实际应用中需谨慎处理内容所有权和转换性使用等伦理问题。

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2604_21915/figures/024_Figure_19.jpg]]
*Figure 19: Ablation on depth artifacts and source video conditioning. We show ablation samples on training with depth artifacts (we simulate training without depth artifacts by always doing double reprojection for point cloud rendering [7]) and source video conditioning (comparing our in-context/frame-concatenated source video conditioning with no source video and source video injected via cross-attention). Both examples above show 4D reconstruction artifacts carrying over to all ablations, such as on the car (left) or the man’s arm and hand (right, highlighted by yellow boxes). Notably, though injecting the source video via cross-attention can at times correct point cloud artifacts, we find that cros...*

## 定位与知识库关联

### 1. 问题域定位：视频重拍中的先验表示之争

Vista4D 处于**视频重拍（video reshooting）**这一任务线中——给定一段单目动态视频，从用户指定的新相机轨迹重新合成相同动态场景的视频。该任务的核心矛盾在于：如何在精确控制目标相机轨迹的同时，保留源视频中的动态内容与外观。

现有方法按先验表示形式可分为两大阵营：

- **隐式先验方法**：将相机控制信号隐式注入生成模型，不构建显式的场景几何。**ReCamMaster** 将目标相机参数编码为 Plücker 嵌入注入视频扩散模型；**CamCloneMaster** 通过参考视频隐式传递相机运动。这类方法的优势在于生成质量高（FID/FVD 指标占优，见 Table 3），但相机控制精度不足——模型倾向于输出与源视频相似的、通常更静态的相机运动，而非精确遵循目标轨迹。

- **显式先验方法**：先构建场景的显式几何表示，再以此作为生成条件。**TrajectoryCrafter** 使用逐帧 3D 点云，通过双重投影（double reprojection）生成无伪影的训练对；**EX-4D** 使用深度水密网格；**GEN3C** 使用 3D 缓存。这类方法相机控制精度更高，但面对真实世界视频的深度估计伪影时鲁棒性差——训练时使用的无伪影点云与推理时的不完美点云之间存在分布偏移。

Vista4D 属于显式先验阵营，但其核心贡献在于**弥合了这一分布偏移**：通过引入时间持久的 4D 点云表示，并在训练中刻意暴露非正面视角的深度伪影，使模型学会利用源视频的上下文条件来纠正不完美几何。

### 2. 关键设计差异：三个改变的槽位

相较于最近的显式先验基线 **TrajectoryCrafter**，Vista4D 在三个关键设计槽位上做出了实质性改变：

| 设计槽位 | TrajectoryCrafter（基线） | Vista4D（本文） |
|---------|--------------------------|----------------|
| **静态像素表示** | 逐帧 3D 点云，无时间持久性 | 时间持久的 4D 点云：通过分割和 4D 重建使静态像素在所有帧可见（Section 3.1） |
| **训练数据深度伪影** | 双重投影生成无伪影点云渲染（始终从正面视角查看深度图） | 使用 4D 重建的多视图动态视频，包含非正面视角带来的深度伪影（Section 3.2, Figure 3） |
| **源视频条件策略** | 仅使用点云渲染作为条件 | 沿帧维度串联源视频和点云渲染的潜在 token 进行上下文条件（in-context conditioning），并联合 alpha 掩码（Section 3.3） |

**时间持久性**是 4D 点云的核心创新。传统方法对每一帧独立构建 3D 点云，导致静态区域（如背景建筑）在不同帧中重复出现但彼此孤立。Vista4D 使用 Grounded SAM 2 获取动态像素掩码，将静态像素掩码应用于各帧点云，使静态点在世界空间中跨帧可见（Figure 2）。这使得模型在目标相机与源视频帧重叠较少时，仍能访问已见的静态内容，从而显著提升内容保留和相机控制精度（消融实验 Supplementary F.2, Figure 20 证实去除该设计会导致静态内容丢失和相机控制精度下降）。

**深度伪影训练**解决了训练-推理分布不匹配的根本问题。TrajectoryCrafter 使用双重投影策略（Figure 3a）：先将目标视频点云渲染到源相机，再重新渲染回目标相机以创建遮挡区域。这一过程始终从正面视角查看深度图，因此训练数据中的点云渲染是无伪影的。然而，真实推理时从目标相机渲染源视频点云会产生非正面视角的深度估计伪影（Figure 3b）。Vista4D 直接使用 4D 重建的多视图动态视频进行训练，使模型暴露于这些伪影中，并结合源视频的上下文条件学会纠正不完美几何（消融实验 Supplementary F.1, Figure 19 证实联合使用深度伪影训练和上下文源视频条件是鲁棒性的关键）。

**上下文条件**（in-context conditioning）区别于交叉注意力注入。Vista4D 将源视频潜在 token 和点云渲染潜在 token 沿帧维度串联后输入扩散变换器，同时联合 alpha 掩码指示哪些区域来自点云渲染。这种设计使模型能够在空间-时间维度上直接比较源视频和点云渲染，从而更自适应地纠正伪影。相比之下，交叉注意力注入（如部分基线尝试）往往不够自适应——消融实验显示，交叉注意力在相机大幅后退时可能导致物体异常放大（Figure 19 left-b）。

### 3. 适用边界

**强适用场景**：
- 真实单目动态视频的重拍，尤其是包含显著相机运动的目标轨迹
- 需要精确相机控制的场景（平移误差 1.251，旋转误差最优，Table 1）
- 4D 场景重组：直接编辑 4D 点云即可实现场景元素的增删和重新组合（Figure 8）
- 动态场景扩展：通过联合 4D 重建将额外视角的静态信息注入点云（Figure 7）
- 长视频推理：通过将新生成块的静态像素注册回持久点云，维持显式的 4D 记忆（Figure 9）

**弱适用场景**：
- 对视频保真度指标（FID/FVD）要求极高且相机控制精度不敏感的场景：隐式先验方法（ReCamMaster, CamCloneMaster）在 FID 上优于 Vista4D（94.15 vs 105.4, Table 3），因为其倾向于输出与源视频相机更接近的、更静态的视频
- 点云质量极差的情况（大面积缺失或严重错误）：虽然上下文条件提供了一定的纠正能力，但极端情况下的鲁棒性尚未系统验证（论文将其列为开放问题）

### 4. 局限性与开放问题

**已识别的局限性**：

1. **缺乏显式控制机制**：模型目前无法让用户调节“遵循点云几何”与“依赖生成先验纠正”之间的权衡。当点云存在伪影时，模型自动决定是纠正还是保留，缺乏用户可控的插值旋钮。论文建议未来增加一种在显式先验（点云）和隐式先验（源视频/相机嵌入）之间插值的控制机制。

2. **继承自基座模型的偏见**：Vista4D 基于 Wan2.1-T2V-14B 微调，继承了训练数据中的内容偏见和伦理风险（如误导性内容生成、隐私问题），在实际部署中需要谨慎处理。

**开放问题**：

1. **连续控制信号设计**：如何设计一个连续的控制信号，让用户能够平滑地在严格遵循点云几何与依赖生成先验之间切换？

2. **极端点云质量下的鲁棒性**：在点云质量极差（例如大面积缺失或严重错误）时，上下文条件是否仍然足够鲁棒？这需要系统性的压力测试。

3. **扩展到更长/交互式视频**：能否将 4D 持久点云思想扩展到更长的视频生成甚至交互式视频重拍？当前的块式推理（Figure 9）已展示了初步可行性，但块间一致性和效率仍是挑战。

4. **多动态对象遮挡处理**：当多个动态对象相互遮挡时，4D 重建和分割的效率与精度如何保证？当前方法依赖 Grounded SAM 2 的逐对象分割，复杂遮挡场景下的性能需要进一步验证。

### 5. 知识库定位

Vista4D 的核心知识贡献在于揭示了**显式先验方法中训练-推理分布匹配的重要性**，并提供了系统性的解决方案：

- **对显式先验路线的推进**：证明了通过时间持久性和深度伪影训练，显式点云先验可以在保持高精度相机控制的同时，达到与隐式方法接近的生成质量。Table 3 显示，Vista4D 在所有显式先验基线中取得了最优的视频保真度指标。

- **对上下文条件策略的验证**：实验表明，沿帧维度串联的上下文条件比交叉注意力注入更适合“参考-目标”对应任务，因为前者保留了空间-时间维度的直接对齐能力。

- **对 4D 场景理解的拓展**：时间持久点云不仅是生成条件，还是一种可编辑、可扩展的 4D 场景表示，支持场景重组（Figure 8）和动态场景扩展（Figure 7）等下游应用，为视频编辑和场景理解提供了新的接口范式。

> **注意**：本文未提供作者、会议/期刊和年份信息，上述基线方法的完整引用（如 He et al., CVPR 2023 等）需要从原始论文中手动核实后补充。

## 原文 PDF

![[paperPDFs/CVPR_2026/Vista4D_Video_Reshooting_with_4D_Point_Clouds.pdf]]
