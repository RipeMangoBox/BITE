---
title: Zero-Shot Reconstruction of Animatable 3D Avatars with Cloth Dynamics from a Single Image
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Zero_Shot_Reconstruction_of_Animatable_3D_Avatars_with_Cloth_Dynamics_from_a_Single_Image.pdf
project_link: "https://juhyeon-kwon.github.io/DynaAvatar.github.io/"
code_link: null
aliases:
- ZSRA3ACDFSI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过引入Dynamic Transformer处理运动历史来实现运动感知的非刚性变形预测，并利用静态到动态的知识迁移（LoRA微调）赋予模型零样本泛化能力。
primary_logic: 在大规模静态数据预训练的基础上，仅需轻量级LoRA适配即可从少量动态数据中学习运动相关的布料变形；同时，基于光流对应关系的几何损失（DynaFlow）能有效监督大幅非刚性运动，避免图像损失的颜色-几何歧义。
claims:
- DynaAvatar在4D-Dress、Actors-HQ、DNA-Rendering等多个数据集上取得最佳PSNR/SSIM/LPIPS。
- Dynamic Transformer是建模布料动态的关键组件，移除后性能显著下降。
- 静态到动态的LoRA知识迁移优于从头训练或全参数微调。
- DynaFlow损失函数有效提升大幅布料运动和边缘清晰度。
---

# Zero-Shot Reconstruction of Animatable 3D Avatars with Cloth Dynamics from a Single Image

> [!tip] 核心洞察
> 在大规模静态数据预训练的基础上，仅需轻量级LoRA适配即可从少量动态数据中学习运动相关的布料变形；同时，基于光流对应关系的几何损失（DynaFlow）能有效监督大幅非刚性运动，避免图像损失的颜色-几何歧义。

| 字段 | 内容 |
|------|------|
| 中文题名 | 单张图像零样本重建可动画3D虚拟人及布料动态 |
| 英文题名 | Zero-Shot Reconstruction of Animatable 3D Avatars with Cloth Dynamics from a Single Image |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.14772) · [Project](https://juhyeon-kwon.github.io/DynaAvatar.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DynaAvatar |
| Dataset | 4D-Dress, Actors-HQ, DNA-Rendering |

> [!tip] 效果简介
> - 4D-Dress 上，PSNR↑ 19.45 vs 17.42 (LHM) (+2.03)；SSIM↑ 0.916 vs 0.901 (LHM) (+0.015)。
> - Actors-HQ 上，PSNR↑ 23.74 vs 21.03 (LHM) (+2.71)；SSIM↑ 0.960 vs 0.950 (LHM) (+0.010)。
> - DNA-Rendering 上，PSNR↑ 21.38 vs 20.29 (LHM) (+1.09)。

## 概要

从单张图像重建可动画的3D虚拟人并赋予其逼真的服装动态，是数字人领域的核心难题。现有方法——无论是依赖逐主体优化的**PERSONA**，还是零样本前馈模型**LHM**、**IDOL**（Sun et al., CVPR 2025）——均仅基于骨架姿态驱动线性混合蒙皮（LBS）的刚性变换，完全忽略了运动历史对非刚性布料变形的影响。这导致在快速或大幅度动作下，服装僵硬、缺乏真实褶皱，动画效果严重失真。

**DynaAvatar** 首次实现了从单张图像零样本重建具有运动感知布料动态的可动画3D虚拟人。其核心洞察在于：布料变形并非仅由当前姿态决定，而是运动历史的累积效应——例如，相同姿态下“坠落”与“跳跃”的服装形态截然不同（见Figure 6）。为此，DynaAvatar 引入**Dynamic Transformer**，将关节运动历史（线性速度、6D旋转、姿态速度及加速度）编码为运动令牌，与静态几何特征融合，直接预测运动相关的非刚性3D高斯变形。

方法上的关键创新是**静态到动态的知识迁移**策略：在大规模静态人体数据上预训练Static Transformer，获取强几何与外观先验；随后仅通过轻量级**LoRA**微调适配动态数据，使模型从少量动态样本中高效学习布料变形规律。同时，针对大幅非刚性运动下图像损失的颜色-几何歧义问题，提出**DynaFlow损失**——基于光流对应关系的纯几何监督信号，有效引导高斯点沿真实运动轨迹移动。

实验验证全面且有力：DynaAvatar 在4D-Dress、Actors-HQ、DNA-Rendering三个数据集上均取得最佳PSNR/SSIM/LPIPS，相较LHM提升1–3 dB（Table 3）；消融实验证实Dynamic Transformer是布料动态建模的核心组件（Fig. 5），静态到动态LoRA迁移显著优于从头训练或全参数微调（Fig. 7），DynaFlow损失有效改善大幅运动下的布料边缘清晰度（Fig. 8）。此外，对训练数据重新标注的高质量SMPL-X参数使渲染质量额外提升约3 dB PSNR（Table S3），凸显数据质量对动态建模的基础性作用。

在方法谱系上，DynaAvatar 填补了零样本单图像重建与布料动态建模之间的空白（Table 1），其前馈架构在推理速度（1.82秒）和参数量（719M）上亦优于LHM-1B（3.00秒，1.1B）。当前局限性主要在于依赖运动历史导致首帧初始化不准确，以及对极端着装和罕见运动的泛化能力有限。

### 问题背景：从静态重建到动态虚拟人

3D虚拟人重建是计算机视觉与图形学的核心课题之一，在影视制作、游戏开发、虚拟现实等领域具有广泛应用。近年来，基于前馈网络（feed-forward）的单图像3D虚拟人重建方法取得了显著进展，能够从单张RGB图像直接预测可驱动的3D表示，无需逐主体优化（subject-specific optimization），实现了零样本（zero-shot）泛化能力。

然而，这些方法面临一个根本性瓶颈：**它们仅依赖线性混合蒙皮（LBS）等刚性骨骼变换来驱动虚拟人动画，无法建模与运动相关的非刚性布料动态**。具体而言，现有方法假设3D高斯点或网格顶点严格跟随骨骼运动，忽略了衣物褶皱、裙摆飘动、布料拉伸等因运动历史而产生的真实形变。这导致动画结果僵硬、缺乏真实感——尤其是在快速转身、跳跃、下蹲等大幅运动场景下，衣物“粘附”在身体上，与真实世界的物理行为严重不符。

### 现有方法的缺口

Table 1 系统对比了已有虚拟人重建方法的特性。从表中可以看出，当前方法在三个关键维度上存在明显缺口：

1. **零样本与布料动态的割裂**：早期方法（如 **PERSONA**）通过逐主体优化实现布料动态建模，但牺牲了零样本泛化能力；而近年来的零样本方法（如 **IDOL**（Sun et al., CVPR 2025）、**LHM**）虽然支持单图像快速推理，却完全缺乏运动感知的布料变形建模。

2. **物理模拟的局限性**：基于物理模拟的方法可以生成逼真的布料动态，但计算开销巨大、对初始条件和参数高度敏感，难以集成到实时或零样本推理框架中。

3. **训练数据标注质量被忽视**：现有动态数据集（如DNA-Rendering、Actors-HQ）的SMPL-X标注存在缺失帧、噪声和拟合不准确等问题，直接使用这些标注会严重损害模型学习布料动态的能力。

### 核心动机与设计思路

DynaAvatar的提出正是为了填补上述缺口——**实现首个从单张图像零样本重建可动画3D虚拟人并保持运动相关布料动态的框架**。其设计围绕三个核心观察展开：

- **观察一：运动历史是关键因果变量。** 布料形变不仅取决于当前姿态，更取决于运动历史（如加速度、速度方向变化）。因此，模型需要显式编码并利用运动历史信息，而非仅依赖当前帧的姿态参数。

- **观察二：静态先验可迁移。** 大规模静态3D人体数据（如RenderPeople）提供了丰富的几何和外观先验。通过在静态数据上预训练Transformer，再以轻量级LoRA适配动态数据，可以在保留强先验的同时高效学习运动相关变形，避免从头训练的不稳定性。

- **观察三：图像损失存在歧义。** 传统图像重建损失（L1、SSIM、LPIPS）在监督大幅非刚性运动时面临颜色-几何歧义：像素颜色匹配并不意味着底层几何正确。引入基于光流对应关系的纯几何损失（DynaFlow）可以提供显式的变形对齐信号，有效缓解这一问题。

基于上述动机，DynaAvatar设计了Static Transformer（提取静态几何外观）与Dynamic Transformer（融合运动历史预测布料变形）的双阶段架构，并通过静态到动态的知识迁移策略和DynaFlow损失函数，在多个公开数据集上取得了显著优于现有方法的渲染质量与布料动态真实感。

## 核心方法与创新机理

DynaAvatar 的核心创新在于突破了现有单图像 3D 虚拟人重建方法的一个根本瓶颈：**从刚性骨骼变换到运动感知的非刚性布料动态建模**。此前的零样本方法（如 **IDOL** (Sun et al., CVPR 2025)、**LHM**）仅依赖基于姿态的线性混合蒙皮（LBS）进行刚性变换，无法表现衣物随运动产生的褶皱、摆动和形变，导致动画效果僵硬、缺乏真实感（Fig. 1）。DynaAvatar 通过以下三个相互耦合的关键创新解决了这一问题。

### 1. 运动感知的动态变形预测

DynaAvatar 引入了 **Dynamic Transformer** 模块，首次在单图像零样本框架中实现了对运动相关布料动态的直接预测。其核心机制是编码运动历史（包含关节线性速度、6D 旋转、姿态速度及加速度，形状为 $\mathbb{R}^{T \times (K \cdot 21)}$）为运动令牌，并通过多模态 Transformer 与静态几何特征进行融合：

$$\mathbf{T}_{3\mathrm{D}}, \mathbf{T}_{\mathrm{M}} \leftarrow \mathbf{MM}(\mathbf{T}_{3\mathrm{D}}, \mathbf{T}_{\mathrm{M}}; \mathbf{F}_{\mathrm{M}})$$

这使得模型能够感知运动上下文，而非仅响应单帧姿态。消融实验（Fig. 5 & Tab. 2）表明，移除 Dynamic Transformer 后性能显著下降，验证了其作为布料动态建模关键组件的地位。定性结果（Fig. 6）进一步显示，即使姿态几乎一致，不同的运动历史（如下落 vs 跳跃）也会产生截然不同的衣物形变。

### 2. 静态到动态的知识迁移策略

DynaAvatar 提出了 **静态预训练 + LoRA 轻量级适配** 的知识迁移策略。Static Transformer 首先在大规模静态数据上预训练，学习丰富的几何和外观先验；随后仅通过 LoRA 对 Dynamic Transformer 进行微调，从少量动态数据中高效习得运动相关的布料变形。消融实验（Fig. 7）证明，该策略显著优于从头训练或全参数微调，在数据效率与泛化能力之间取得了关键平衡。

### 3. 基于光流对应的几何监督损失

针对大幅非刚性运动下图像损失的颜色-几何歧义问题，DynaAvatar 提出了 **DynaFlow 损失函数**。该损失利用 LightGlue 在渲染图像与真值图像之间计算光流对应点，对渲染的 xy 坐标图施加几何约束：

$$\mathcal{L}_{\mathrm{flow}} = \frac{1}{N} \sum \| \mathbf{M}(\mathbf{p}_{\mathrm{src}}) - \mathbf{p}_{\mathrm{tgt}} \|_1$$

DynaFlow 提供了与变形对齐的显式几何监督信号，有效改善了大幅布料运动和边缘清晰度（Fig. 8）。训练策略上，该损失在训练中后期（约 20K 次迭代后）引入，以避免早期训练不稳定。

| 创新维度 | 基线方法 | DynaAvatar |
|---------|---------|------------|
| 动态建模 | 仅基于姿态的刚性 LBS 变换 | 基于运动历史的 Dynamic Transformer 预测非刚性变形 |
| 知识迁移 | 从头训练或全参数微调 | 静态预训练 + LoRA 轻量级适配 |
| 监督信号 | 仅图像重建损失（L1, SSIM, LPIPS） | 增加 DynaFlow 光流引导的几何损失 |

上述三项创新协同作用，使 DynaAvatar 在 4D-Dress、Actors-HQ、DNA-Rendering 等多个数据集上取得了最优的 PSNR/SSIM/LPIPS 指标（Tab. 3），并保持了 1.82 秒的推理速度和 719M 参数量，优于 LHM-1B（3.00 秒，1.1B 参数）的计算效率（Tab. S2）。

**DynaAvatar** 的整体设计围绕一个核心瓶颈展开：现有单图像零样本虚拟人重建方法（如 **LHM**、**IDOL** (Sun et al., CVPR 2025)）仅依赖刚性骨骼变换（LBS），无法建模非刚性布料动态，导致动画僵硬、缺失真实感。为解决这一问题，DynaAvatar 构建了一个端到端的前馈 Transformer 框架，直接从单张图像预测运动感知的 3D 高斯变形，无需针对特定对象进行优化。

### 流水线总览

整个流水线由五个关键模块串联而成，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2603_14772/figures/004_Figure_2.jpg]]
*Figure 2: Overall pipeline of the proposed DynaAvatar. We first extract detailed geometry and appearance without cloth dynamics using a Static Transformer. Next, cloth dynamics are incorporated from motion history through a Dynamic Transformer. The final 3D avatar in canonical space is reconstructed using a Gaussian decoder and then animated and rendered with LBS and a 3DGS renderer. Since the canonical avatar already encodes motion-dependent cloth dynamics, the animation produced by LBS faithfully maintains these dynamics*

1. **Static Transformer（静态 Transformer）**  
   从单张输入图像中提取详细的几何与外观特征，但不建模任何布料动态。该模块在大规模静态人体捕捉数据上预训练，为后续动态建模提供强先验。

2. **Motion Encoder（运动编码器）**  
   将运动历史编码为运动令牌。运动历史张量的形状为 $\mathbb{R}^{T \times (K \cdot 21)}$，包含 $T$ 帧、$K=22$ 个关节点每个 21 维的运动特征（涵盖关节线性速度、6D 旋转、姿态速度及加速度）。

3. **Dynamic Transformer（动态 Transformer）**  
   这是实现布料动态建模的**核心因果旋钮**。它接收运动令牌，通过多模态 Transformer 模块更新 3D 点令牌，融合运动感知的布料变形信息：
   $$\mathbf{T}_{3\mathrm{D}}, \mathbf{T}_{\mathrm{M}} \leftarrow \mathbf{MM}(\mathbf{T}_{3\mathrm{D}}, \mathbf{T}_{\mathrm{M}}; \mathbf{F}_{\mathrm{M}})$$
   消融实验证实，移除该模块后性能显著下降（Fig. 5 & Tab. 2），验证了其对建模运动相关布料动态的关键作用。

4. **Gaussian Decoder（高斯解码器）**  
   将 Transformer 输出的特征解码为 3DGS 表示，包括均值、缩放、旋转、透明度及颜色参数。

5. **Animation & Rendering（动画与渲染）**  
   使用 LBS 驱动并渲染最终的动态虚拟人。由于规范空间的虚拟人已编码运动相关的布料动态，LBS 驱动的动画能忠实地保持这些动态效果。

### 静态到动态的知识迁移

DynaAvatar 采用**静态到动态知识迁移策略**来解决零样本泛化问题：在大规模静态数据上预训练 Static Transformer 后，仅通过轻量级 **LoRA** 微调适配动态数据。消融实验表明（Fig. 7），该策略显著优于从头训练或全参数微调，使模型能从少量动态数据中高效学习运动相关的布料变形。

### 损失函数设计

除常规图像重建损失（L1、SSIM、LPIPS）外，DynaAvatar 引入了 **DynaFlow 损失函数**，提供纯几何的、基于光流的监督信号：
$$\mathcal{L}_{\mathrm{flow}} = \frac{1}{N} \sum \| \mathbf{M}(\mathbf{p}_{\mathrm{src}}) - \mathbf{p}_{\mathrm{tgt}} \|_1$$
该损失通过 LightGlue 计算渲染图像与真值图像之间的光流对应关系，鼓励源位置的高斯向目标光流终点移动（Fig. 3）。DynaFlow 有效解决了图像损失中颜色-几何的歧义问题，特别改善了大尺度布料运动和边缘清晰度的建模（Fig. 8）。为规避训练早期的不稳定性，DynaFlow 损失在训练 20K 次迭代后才引入。

### 数据质量保障

高质量 SMPL-X 参数是动态建模的基础。DynaAvatar 对 4D-Dress、Actors-HQ、DNA-Rendering 等数据集的原始标注进行了重新标注，获得了更完整、准确的 SMPL-X 参数。消融实验显示（Table S3 & Fig. 4），该重标注使 PSNR 提升约 3dB，显著改善了渲染质量。

### 整体架构概述

DynaAvatar 采用前馈式 Transformer 架构，从单张图像直接预测动态 3D Gaussian 变形，无需针对特定人物进行优化。整体流程由五个核心模块串联构成，如 Figure 2 所示：

1. **Static Transformer**：从单张图像提取详细几何与外观特征，不建模布料动态。
2. **Motion Encoder**：编码运动历史为运动令牌。
3. **Dynamic Transformer**：融合运动令牌更新静态特征，预测运动相关的布料变形。
4. **Gaussian Decoder**：将 Transformer 输出解码为 3DGS 表示。
5. **Animation & Rendering**：通过 LBS 和 3DGS 渲染器驱动并渲染最终动态虚拟人。

关键设计在于：规范空间下的虚拟人已编码运动依赖的布料动态，因此 LBS 驱动的动画能够忠实地保持这些动态效果。

---

### 静态 Transformer：几何与外观特征提取

静态 Transformer 负责从单张输入图像中提取不包含布料动态的几何与外观先验。其核心操作为多模态 Transformer 模块（MM），以图像令牌更新 3D 点令牌：

$$\mathbf{T}_{3\mathrm{D}}, \mathbf{T}_{\mathrm{I}} \leftarrow \mathbf{MM}(\mathbf{T}_{3\mathrm{D}}, \mathbf{T}_{\mathrm{I}}; \mathbf{F}_{\mathrm{I}})$$

其中：
- $\mathbf{T}_{3\mathrm{D}}$ 为 3D 点令牌，承载规范空间下的几何与外观信息；
- $\mathbf{T}_{\mathrm{I}}$ 为图像令牌，由输入图像经视觉编码器提取；
- $\mathbf{F}_{\mathrm{I}}$ 为全局上下文特征，注入图像级别的语义信息。

该模块在大规模静态人体数据上预训练，为后续动态建模提供强先验。

---

### Motion Encoder：运动历史编码

为让模型感知运动对布料的影响，Motion Encoder 将运动历史编码为运动令牌。运动历史张量的形状为：

$$\mathbb{R}^{T \times (K \cdot 21)}$$

其中 $T$ 为历史帧数，$K = 22$ 个关节点（含身体 21 个关节 + 1 个根节点），每个关节的 21 维运动特征包括：关节线性速度、6D 旋转表示、姿态速度及加速度。这些时序运动信息构成模型理解“当前帧之前发生了什么”的关键输入。

---

### 动态 Transformer：运动感知的布料变形预测

动态 Transformer 是 DynaAvatar 的核心创新，负责将运动历史信息注入静态特征，预测运动依赖的非刚性布料变形。其更新公式为：

$$\mathbf{T}_{3\mathrm{D}}, \mathbf{T}_{\mathrm{M}} \leftarrow \mathbf{MM}(\mathbf{T}_{3\mathrm{D}}, \mathbf{T}_{\mathrm{M}}; \mathbf{F}_{\mathrm{M}})$$

其中：
- $\mathbf{T}_{\mathrm{M}}$ 为运动令牌，由 Motion Encoder 从运动历史中提取；
- $\mathbf{F}_{\mathrm{M}}$ 为姿态特征，提供当前帧的显式姿态条件。

消融实验（Figure 5, Table 2）表明，移除动态 Transformer 后性能显著下降，验证了该模块是捕捉布料动态的关键组件。此外，Figure 6 展示了即使姿态几乎相同，不同运动历史（如坠落 vs 跳跃、后退 vs 坠落）会导致明显的服装差异，证明动态 Transformer 有效利用了运动上下文信息。

---

### 静态到动态的知识迁移：LoRA 轻量级适配

动态 Transformer 的训练采用静态到动态的知识迁移策略：
- **第一阶段**：Static Transformer 在大规模静态人体数据上预训练，获得强几何与外观先验；
- **第二阶段**：仅对 Dynamic Transformer 进行轻量级 LoRA 微调，从少量动态数据中学习运动依赖的变形。

消融实验（Figure 7）对比了三种策略：从头训练、全参数微调、LoRA 适配。结果表明 LoRA 适配效果最优，验证了静态预训练先验的有效性与轻量级迁移的优越性。

---

### DynaFlow 损失函数：光流引导的几何监督

传统图像重建损失（L1、SSIM、LPIPS）在监督大幅非刚性运动时存在颜色-几何歧义：像素颜色变化可能源于变形或外观变化，难以提供明确的对应关系信号。DynaFlow 损失通过光流建立显式的几何对应关系，仅提供几何监督：

$$\mathcal{L}_{\mathrm{flow}} = \frac{1}{N} \sum \| \mathbf{M}(\mathbf{p}_{\mathrm{src}}) - \mathbf{p}_{\mathrm{tgt}} \|_1$$

其中：
- 使用 LightGlue 在渲染图像与真值图像之间计算光流，获得 $N$ 对匹配的源像素坐标 $\mathbf{p}_{\mathrm{src}}$ 与目标像素坐标 $\mathbf{p}_{\mathrm{tgt}}$；
- $\mathbf{M}(\cdot)$ 为渲染的 xy 坐标图，在源像素位置采样得到该像素对应的 3D 点投影坐标；
- 损失鼓励这些投影坐标向光流目标端点移动，即推动 Gaussian 在图像空间中的投影位置与真值对齐。

Figure 3 直观展示了该损失的工作机制：黑色轮廓白色圆点表示源位置的 Gaussian 投影，损失促使其沿估计光流向目标位置移动。消融实验（Figure 8）证实 DynaFlow 损失有效改善了大幅布料运动和边缘清晰度。此外，该损失在训练中后期（约 20K 次迭代后）引入，以避免早期训练不稳定。

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2603_14772/figures/005_Figure_3.jpg]]
*Figure 3: Visualization of the proposed DynaFlow loss. Our DynaFlow loss encourages the Gaussians at source locations (blackoutlined white circles) to move toward the endpoints of the estimated flow vectors*

## 实验与关键发现

### 核心瓶颈验证

现有单图像零样本3D虚拟人方法（如**IDOL**（Sun et al., CVPR 2025）、**LHM**）仅依赖基于姿态的刚性骨骼变换（LBS）驱动动画，无法建模非刚性布料动态，导致动画僵硬、缺失真实感（Table 1）。DynaAvatar通过在静态几何外观先验之上引入运动感知的非刚性变形预测，直接回应这一瓶颈。

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2603_14772/figures/003_Table_1.jpg]]
*Table 1: Comparison of existing avatar reconstruction methods and the proposed DynaAvatar. Each column indicates whether the method reconstructs avatars in a zero-shot manner (i.e., without subject-specific optimization), whether it supports cloth dynamics, and whether it operates from a single input image*

### 主实验结果

**Table 3** 汇总了DynaAvatar与SOTA方法在三个动态人体数据集上的新视角合成定量对比。DynaAvatar在所有数据集上取得最佳PSNR、SSIM和LPIPS：

| 数据集 | 指标 | DynaAvatar | 最佳Baseline (LHM) | 提升 |
|--------|------|-----------|-------------------|------|
| 4D-Dress | PSNR↑ | 19.45 | 17.42 | +2.03 |
| 4D-Dress | SSIM↑ | 0.916 | 0.901 | +0.015 |
| Actors-HQ | PSNR↑ | 23.74 | 21.03 | +2.71 |
| Actors-HQ | SSIM↑ | 0.960 | 0.950 | +0.010 |
| DNA-Rendering | PSNR↑ | 21.38 | 20.29 | +1.09 |

在DNA-Rendering数据集的面部一致性（FC）指标上，DynaAvatar也优于LHM（0.712 vs. 0.697，Table S1）。**Figure 9** 的定性对比进一步显示，DynaAvatar在真实场景图片上能够生成运动相关的布料褶皱和摆动，而LHM和IDOL的输出则呈现刚性跟随姿态的“贴皮”效果。

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2603_14772/figures/014_Figure_9.jpg]]
*Figure 9: Comparison between DynaAvatar and previous single-image–based state-of-the-art methods [38, 61] on in-the-wild images*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2603_14772/figures/015_Table_S.1.jpg]]
*Table S.1: Comparison of face consistency (FC) on DNA-Rendering*

推理效率方面，DynaAvatar参数量719M，单次推理时间1.82秒，优于LHM-1B的3.00秒和1.1B参数（Table S2）。

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2603_14772/figures/016_Table_S.2.jpg]]
*Table S.2: Comparison of computational costs*

### 消融实验

#### 1. Dynamic Transformer是关键组件

**Figure 5** 和 **Table 2** 展示了移除Dynamic Transformer后的性能退化。无动态Transformer时，模型退化为仅依赖静态特征和姿态刚性变换的基线，布料动态完全消失，PSNR在4D-Dress上显著下降。这证实了运动历史建模是捕捉非刚性布料变形的必要条件。

#### 2. 静态到动态的知识迁移策略

**Figure 7** 对比了三种训练策略：（1）从头训练动态模型，（2）全参数微调预训练静态模型，（3）LoRA轻量级适配。结果表明，LoRA微调不仅收敛更快，且最终渲染质量最高。全参数微调可能破坏静态预训练中习得的几何和外观先验，而从头训练则因动态数据稀缺难以学到鲁棒表示。这一结论直接支撑了论文的核心洞察：**大规模静态数据预训练 + 轻量级LoRA适配 = 高效的零样本动态泛化**。

#### 3. DynaFlow损失函数的作用

**Figure 8** 的消融显示，仅使用图像重建损失（L1+SSIM+LPIPS）时，模型在大幅布料运动区域产生模糊和伪影。加入DynaFlow光流引导的几何损失后，布料边缘更清晰，运动轨迹更准确。DynaFlow通过显式提供源-目标像素对应关系，规避了图像损失中颜色与几何的歧义问题。论文还指出，DynaFlow损失在训练中后期（约20K次迭代后）引入可避免早期训练不稳定（Sec 3.3）。

#### 4. 数据重标注的重要性

**Table S3** 和 **Figure 4** 揭示了数据质量对动态建模的决定性影响。原始DNA-Rendering和Actors-HQ数据集的SMPL-X标注存在缺失和噪声。使用重新标注的高质量SMPL-X参数后，PSNR提高约3dB（Table S3），布料变形与图像的对齐度显著改善（Figure 4）。这一发现表明，**准确的姿态和形状标注是学习运动-变形映射的基础**。

#### 5. 运动历史的因果效应

**Figure 6** 提供了最具说服力的因果证据：在几乎相同的姿态下，不同的运动历史导致明显不同的布料形态。例如，空中坠落与向上跳跃的姿态相似，但前者衣物向上飘起，后者向下紧贴。这直接证明Dynamic Transformer成功编码了运动历史信息，而非简单拟合姿态到变形的映射。

### 失败模式与局限性

1. **首帧初始化问题**：Dynamic Transformer依赖运动历史（多帧关节速度、加速度），首帧或无历史时需初始化为零，可能导致起始帧变形不准确。这在需要从静止状态开始的动画序列中尤为明显。

2. **极端着装与罕见运动**：训练数据集的服装和运动多样性有限，对极端着装风格（如长裙、斗篷）或罕见运动（如翻滚、倒立）的泛化能力可能不足，布料变形可能出现不符合物理规律的拉伸或穿透。

3. **姿态估计依赖**：尽管DynaAvatar比物理模拟更鲁棒，但在姿态估计严重错误的情况下（如遮挡、极端视角），输入的运动历史特征本身包含误差，布料变形仍可能出现失真。这是所有依赖SMPL-X作为驱动信号的零样本方法的共同弱点。

4. **多人物交互未探索**：当前框架仅支持单人重建与动画，多人物交互场景（如拥抱、握手）中的布料碰撞和遮挡尚未涉及。

### 方法谱系与知识库定位

DynaAvatar处于**单图像零样本3D虚拟人重建**与**布料动态建模**的交叉点。与以下方法形成明确对比：

- **IDOL**（Sun et al., CVPR 2025）、**LHM**：同样支持单图像零样本重建，但仅使用刚性LBS驱动，无布料动态。
- **PERSONA**：需要逐主体优化（非零样本），且不支持布料动态。
- 物理模拟方法（如论文引用的[9]）：可生成物理真实布料，但需要手动设置材质参数，对输入噪声敏感，且计算开销大（Figure S2）。
- 扩散生成方法（如论文引用的[57]）：可生成动态纹理，但缺乏显式3D几何一致性（Figure S3）。

DynaAvatar的核心贡献在于**首次实现零样本单图像到可动画3D虚拟人的布料动态重建**，其技术路线——静态预训练Transformer + LoRA动态适配 + 光流几何监督——为后续研究提供了可复用的范式。

## 定位与知识库关联

### 单图像3D虚拟人重建的演化脉络

单图像3D虚拟人重建的目标是从一张RGB图像中恢复可驱动、可渲染的完整人体表示。该领域的发展可沿两条主线梳理：**优化式方法**与**前馈式方法**，而DynaAvatar的贡献在于将前馈式方法的能力边界从刚性动画推向了运动感知的非刚性布料动态。

**早期优化式方法**（如PIFu系列、ICON、ECON）通过逐体素或逐顶点优化从单图重建3D人体，但通常需要逐实例优化，无法实现零样本推理。**PERSONA**等后续工作将优化范式与3D Gaussian Splatting（3DGS）结合，实现了更高质量的纹理和几何重建，但仍需对每个新身份进行测试时优化，推理成本高、泛化受限。

**零样本前馈式方法**是近年来的主流突破方向。**LHM**（Large Human Model）率先展示了基于Transformer的单图零样本3DGS虚拟人重建，直接预测规范空间中的3D高斯参数并通过线性混合蒙皮（LBS）驱动动画。**IDOL**（Sun et al., CVPR 2025）进一步引入双分支架构分别处理人体与服装。然而，这些方法的共同局限在于：动画过程仅依赖刚性骨骼变换（LBS），**无法建模运动相关的非刚性布料变形**——这正是DynaAvatar瞄准的核心瓶颈（Table 1 明确对比了各方法的零样本能力、布料动态支持与单图输入特性）。

### DynaAvatar的方法定位

DynaAvatar并非对现有前馈架构的增量修补，而是通过三个关键设计将零样本虚拟人重建从“刚性动画”推入“运动感知动态”的新阶段：

| 设计维度 | 已有方法（LHM / IDOL） | DynaAvatar |
|---------|----------------------|------------|
| 动态建模 | 仅LBS刚性变换 | Dynamic Transformer + 运动历史编码 |
| 知识来源 | 从头训练或全参数微调 | 静态预训练 + LoRA轻量适配 |
| 几何监督 | 仅图像重建损失 | 额外引入DynaFlow光流几何损失 |
| 数据质量 | 依赖原始标注 | 重新标注高质量SMPL-X参数 |

**Dynamic Transformer**是方法的核心创新。它接收运动编码器（Motion Encoder）从运动历史中提取的时序特征——包括关节线性速度、6D旋转、姿态速度及加速度，形成形状为 $\mathbb{R}^{T \times (K \cdot 21)}$ 的运动令牌（$K=22$个关节点，每关节21维特征），通过多模态Transformer模块更新3D点令牌：

$$\mathbf{T}_{3\mathrm{D}}, \mathbf{T}_{\mathrm{M}} \leftarrow \mathbf{MM}(\mathbf{T}_{3\mathrm{D}}, \mathbf{T}_{\mathrm{M}}; \mathbf{F}_{\mathrm{M}})$$

这使得规范空间中的3D高斯表示已经编码了运动相关的布料变形信息，因此后续LBS动画能自然地保留这些动态效果（Figure 2）。消融实验（Figure 5, Table 2）证实，移除Dynamic Transformer后模型退化为仅依赖刚性变换的基线，布料褶皱和摆动效果显著丧失。

**静态到动态的知识迁移**是使零样本泛化可行的关键策略。Static Transformer在大规模静态人体数据上预训练，学习丰富的几何和外观先验；Dynamic Transformer则通过LoRA（Low-Rank Adaptation）轻量级微调从少量动态数据中学习运动相关的变形模式。Figure 7的消融表明，这一策略优于从头训练（缺乏几何先验导致收敛困难）和全参数微调（过拟合动态数据、破坏静态先验）。

**DynaFlow损失函数**解决了图像重建损失在非刚性运动下的颜色-几何歧义问题。传统L1/SSIM/LPIPS损失无法区分“颜色变化”与“几何位移”，而DynaFlow通过LightGlue提取渲染图与真值图之间的光流对应关系，直接监督高斯在屏幕空间的位移：

$$\mathcal{L}_{\mathrm{flow}} = \frac{1}{N} \sum \| \mathbf{M}(\mathbf{p}_{\mathrm{src}}) - \mathbf{p}_{\mathrm{tgt}} \|_1$$

其中 $\mathbf{M}$ 为渲染的xy坐标图，$\mathbf{p}_{\mathrm{src}}$ 和 $\mathbf{p}_{\mathrm{tgt}}$ 为光流的源点与目标点。该损失在训练中后期（约20K次迭代后）引入以避免早期不稳定（Sec 3.3, Figure 3），消融实验（Figure 8）显示其对大幅布料运动和边缘清晰度有显著改善。

### 适用边界与局限

尽管DynaAvatar在4D-Dress、Actors-HQ、DNA-Rendering等多个数据集上取得最佳PSNR/SSIM/LPIPS（Table 3），其适用边界仍受以下因素制约：

1. **运动历史依赖性**：Dynamic Transformer需要历史运动序列作为输入。在首帧或运动历史不可用的情况下，需初始化为零向量，可能导致起始帧的布料变形不准确。这限制了其在实时流式应用中的首帧质量。

2. **服装与运动多样性**：训练数据（4D-Dress、Actors-HQ、DNA-Rendering）的服装类型和运动模式覆盖有限。对极端着装风格（如宽大斗篷、多层裙摆）或罕见运动（如杂技翻滚、舞蹈旋转）的泛化能力可能不足，需进一步验证。

3. **姿态估计鲁棒性**：尽管DynaAvatar比基于物理模拟的方法更鲁棒，但在严重遮挡、极端视角或快速运动导致的姿态估计错误情况下，布料变形仍可能出现失真。方法本身不包含姿态纠正机制。

4. **单人物场景限制**：当前框架仅支持单人重建与动画，多人物交互场景（如拥抱、握手）中的相互遮挡和接触变形尚未探索。

5. **计算开销与容量的权衡**：DynaAvatar推理速度1.82秒、参数量719M，优于LHM-1B（3.00秒，1.1B）（Table S2），但在移动端或实时应用中仍有压缩空间。零样本架构在模型容量与计算效率之间的最优折中仍是一个开放问题。

### 开放问题与未来方向

1. **物理先验的融合**：DynaAvatar学习的是数据驱动的布料变形先验，能否将其与物理模拟（如基于弹性势能的布料模型）相结合，在保持数据驱动鲁棒性的同时提升物理真实感（如惯性效应、碰撞响应）？Figure S2已初步展示了与物理模拟方法的互补性。

2. **长时序一致性**：当前方法以固定窗口的运动历史为输入，如何处理长时间序列上的时间一致性与累积误差问题？引入循环记忆机制或时序平滑约束可能是潜在方向。

3. **面部与手部的精细动画**：当前框架聚焦于身体和布料的动态，能否扩展至面部细节动画（表情皱纹、眼球运动）和手部交互（抓取物体导致的手指变形）？这需要更高分辨率的几何表示和更精细的运动编码。

4. **多模态条件扩展**：除单张图像外，能否融入文本描述、视频序列或物理参数等多模态条件，实现对服装风格和动态行为的更精细控制？

5. **评估体系的完善**：当前评估主要依赖新视角合成的PSNR/SSIM/LPIPS指标，缺乏对布料动态真实感的直接度量。建立包含物理合理性、时序一致性、运动感知质量的综合评估基准是该领域的重要需求。

## 原文 PDF

![[paperPDFs/CVPR_2026/Zero_Shot_Reconstruction_of_Animatable_3D_Avatars_with_Cloth_Dynamics_from_a_Single_Image.pdf]]
