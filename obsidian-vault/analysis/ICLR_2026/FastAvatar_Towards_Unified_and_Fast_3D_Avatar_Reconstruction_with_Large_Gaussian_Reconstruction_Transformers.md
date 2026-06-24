---
title: "FastAvatar: Towards Unified and Fast 3D Avatar Reconstruction with Large Gaussian Reconstruction Transformers"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/FastAvatar_Towards_Unified_and_Fast_3D_Avatar_Reconstruction_with_Large_Gaussian_Reconstruction_Transformers.pdf
openreview_forum_id: P7zBSCs4Xt
aliases:
- FastAvatar
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入前馈式大型高斯重建Transformer (LGRT)，通过全局-帧注意力机制、多粒度引导编码（相机姿态、表情、头部姿态）和增量高斯聚合（结合landmark跟踪损失与切片融合损失），实现对任意数量、任意顺序输入的直接重建与渐进式质量提升。"
primary_logic: "将VGGT风格的大规模Transformer应用于3D头像任务，直接预测标准空间下的3DGS表示，并利用多粒度编码缓解动画带来的错位；通过增量融合机制，模型能够持续吸收新观测数据并改善重建，从而在速度、质量与数据灵活性之间达到最优平衡。"
claims:
- "FastAvatar在所有输入视图设置（1~16视图）下均取得最优重建质量，并具有最快的渲染速度。"
- "模型具备增量重建能力，重建质量随输入视图增加而单调提升，而对比方法LAM性能反而下降。"
- "消融实验证实全局注意力、GS融合、切片融合损失和跟踪损失对多视图聚合与一致性至关重要。"
- "NeRSemble (1-view) 上 PSNR = 20.08"
---

# FastAvatar: Towards Unified and Fast 3D Avatar Reconstruction with Large Gaussian Reconstruction Transformers

> [!tip] 核心洞察
> 将VGGT风格的大规模Transformer应用于3D头像任务，直接预测标准空间下的3DGS表示，并利用多粒度编码缓解动画带来的错位；通过增量融合机制，模型能够持续吸收新观测数据并改善重建，从而在速度、质量与数据灵活性之间达到最优平衡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | FastAvatar：基于大型高斯重建Transformer的统一快速3D化身重建 |
| 英文题名 | FastAvatar: Towards Unified and Fast 3D Avatar Reconstruction with Large Gaussian Reconstruction Transformers |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=P7zBSCs4Xt); [GitHub](https://github.com/TyrionWuYue/FastAvatar) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FastAvatar |
| Dataset | NeRSemble (1-view), NeRSemble (4-view), NeRSemble (16-view) |

> [!tip] 效果简介
> - NeRSemble (1-view) 上，PSNR 为 20.08，对比 17.30 (LAM)，变化 +2.78。
> - NeRSemble (4-view) 上，PSNR 为 22.12，对比 17.52 (GaussianAvatars)，变化 +4.60。
> - NeRSemble (16-view) 上，LPIPS 为 0.092，对比 0.281 (GaussianAvatars)，变化 -0.189。

## 概述

3D化身重建面临三大瓶颈：现有方法无法利用场景先验知识，导致对完整3D观察的严重依赖；依赖参数化代理模型进行观察对齐，精度与鲁棒性不足；无法有效处理可变长度的输入数据，数据利用率低。**FastAvatar** 针对这些问题，提出了一种统一且快速的前馈式重建框架。

其核心思路是引入**大型高斯重建Transformer（LGRT）**，直接预测规范空间下的3DGS表示。LGRT采用全局注意力与帧注意力交替机制，实现跨帧空间配准与融合；配合**多粒度引导编码**（相机姿态、表情系数、头部姿态），缓解动画驱动的错位问题；并通过**增量高斯聚合**机制，使模型能够持续吸收任意数量、任意顺序的新观测数据，实现重建质量的渐进提升。

在NeRSemble数据集上，FastAvatar在所有输入视图设置（1~16视图）下均取得最优重建质量，同时保持最快的渲染速度：单视图PSNR达20.08，渲染帧率240 FPS；16视图PSNR达22.29，LPIPS低至0.092。消融实验证实，全局注意力、GS融合、切片融合损失和跟踪损失对多视图聚合与一致性至关重要。

**方法定位**：FastAvatar属于前馈式3DGS化身重建方法，区别于逐场景优化的GaussianAvatars和单图前馈的LAM，其关键创新在于将VGGT风格的大规模Transformer架构引入头像任务，实现可变长度输入的直接重建与增量更新，在速度、质量与数据灵活性之间取得最优平衡。

## 背景与动机

### 问题背景

真实感3D头像重建是数字人、影视制作和沉浸式通信中的核心任务。近年来，3D高斯泼溅（3D Gaussian Splatting, 3DGS）凭借其高质量实时渲染能力，成为该领域的主流表示。然而，现有方法在实际部署中面临三个相互关联的瓶颈，制约了其从实验室走向真实应用。

### 现有方法的三大瓶颈

**瓶颈一：无法利用场景先验，依赖完整观测。** 基于优化的方法（如 **MonoGaussianAvatar** 和 **GaussianAvatars**）需要对每个新身份从头进行逐场景优化，建模时间通常以分钟甚至小时计。这类方法丢弃了从大规模数据中可学习的通用人脸先验，导致在输入视图稀疏时（如单目或少量视角）重建质量急剧下降。前馈式方法（如 **LAM**）虽然通过单图推理缓解了速度问题，但其架构设计天然无法融合多帧信息，新增观测不仅无法提升重建质量，反而可能引入干扰。

**瓶颈二：依赖参数化代理模型进行观察对齐，精度与鲁棒性不足。** 现有方法普遍采用FLAME等3D参数化模型作为几何代理，将多帧观测对齐到规范空间。然而，FLAME的线性混合蒙皮（LBS）和有限的表情基无法精确建模复杂面部肌肉动态、细微皱纹和眼动追踪。当输入帧的表情、姿态和相机视角差异较大时，基于代理的对齐容易产生错位，导致重建结果出现模糊和伪影。

**瓶颈三：无法有效处理可变长度输入，数据利用率低。** 真实场景中，可用观测数量往往因设备、时长和遮挡等因素动态变化。现有方法要么只能接受固定长度的输入（如单帧或固定多帧），要么在输入帧数增加时性能不升反降。例如，LAM在输入视图从1帧增至16帧时，定量指标反而恶化（见Table 1）。这种“数据越多越差”的反直觉现象，根源在于缺乏有效的多帧融合与增量更新机制。

### 核心动机

上述瓶颈共同指向一个根本性挑战：**如何构建一个统一的前馈框架，既能利用大规模数据中的场景先验，又能灵活吸收任意数量的观测，并在速度与质量之间取得最优平衡？**

FastAvatar的提出正是为了回答这一问题。其核心洞察在于：将VGGT风格的大规模Transformer架构引入3D头像任务，通过全局-帧交替注意力机制实现跨帧空间配准，利用多粒度引导编码（相机姿态、表情系数、头部姿态）缓解动画带来的错位，并设计增量高斯聚合机制使模型能够持续吸收新观测并改善重建。这一设计使得FastAvatar在单帧输入时即可提供高质量结果（PSNR 20.08），并随着输入帧数增加实现单调质量提升（16帧PSNR达22.29），同时保持远超对比方法的推理速度（单帧FPS 240.17）。

### 方法定位

FastAvatar处于前馈式可动画3DGS头像重建的交叉点。与基于优化的方法相比，它无需逐场景迭代，建模时间从分钟级降至秒级；与单图前馈方法（如LAM）相比，它原生支持多帧融合与增量重建；与多图回归方法（如Avat3r）相比，它在重建质量和渲染速度上均取得显著优势（16视图LPIPS 0.092 vs. 0.281，FPS 17.65 vs. <10）。

## 核心创新

FastAvatar 的核心创新在于将大规模 Transformer 架构引入 3D 化身重建任务，通过三个关键机制系统性突破了现有方法的瓶颈。

### 1. 从单帧回归到多帧联合建模的架构跃迁

现有前馈方法（如 **LAM**）仅能处理单张图像，无法利用多视图信息；而基于优化的方法（如 **GaussianAvatars**、**MonoGaussianAvatar**）虽能接受多帧，但需逐场景迭代，速度慢且无法跨实例泛化。FastAvatar 提出 **大型高斯重建Transformer (LGRT)**，直接预测规范空间下的 3DGS 属性，支持任意数量、任意顺序的输入帧。

LGRT 的核心是**交替注意力机制**：
- **帧注意力**（frame attention）：基于双流 DiT 模块，聚合单帧内部信息并注入 3D 位置提示；
- **全局注意力**（global attention）：实现跨帧空间配准与融合，使不同视角、不同表情的观测能够在规范空间中对齐。

消融实验证实，移除全局注意力后，单视图 PSNR 从 20.08 骤降至 15.40，身份指标恶化至 0.400（Table 2），表明跨帧配准是模型有效性的前提。

### 2. 多粒度引导编码：缓解动画驱动的错位

参数化模型驱动的 3D 化身方法普遍存在动画错位问题——表情和姿态变化导致不同帧间的空间对应关系模糊。FastAvatar 引入**多粒度引导编码**，将相机姿态 $\pi_i$、表情系数 $z_i^{exp}$ 和头部姿态 $z_i^{pose}$ 分别经 MLP 处理后与 DINOv2 视觉特征拼接：

$$h_i = \mathcal{U}\left( x_i, \mathrm{MLP}([\pi_i, z_i^{exp}, z_i^{pose}]) \right)$$

这一设计为每帧的视觉标记注入了精细的 3D 位置先验，使 Transformer 能够在全局注意力阶段准确配准不同帧的特征，从根本上缓解了动画带来的空间歧义。

### 3. 增量高斯聚合：从固定输入到流式重建

现有方法要么丢弃额外数据，要么固定输入长度，数据利用率低。FastAvatar 通过两个互补机制实现**增量重建**：

- **GS 融合**（GS Fusion）：将各帧预测的高斯属性拼接为统一规范表示 $g_f = \mathcal{U}(g_1, g_2, \cdots, g_N)$，使模型能持续吸收新观测；
- **双损失监督**：**Landmark 跟踪损失**确保多帧高斯模型在关键点级别精确对齐；**切片融合损失**（Sliced Fusion Loss）通过渲染融合模型并与真值比较，监督整体结构一致性。

实验表明，FastAvatar 的重建质量随输入视图增加而单调提升（1-view PSNR 20.08 → 16-view PSNR 22.29），而对比方法 LAM 反而出现性能退化（Table 1, Figure 4）。消融去除 GS 融合后，16 视图 L1 误差从 0.0263 增至 0.0467，PSNR 从 22.19 降至 18.94（Table 2），验证了多帧高斯聚合对多视图质量的关键作用。

### 4. 可微高斯剪枝：效率与质量的平衡

多帧融合导致高斯点数量线性增长，影响渲染效率。FastAvatar 采用 **Gumbel-Softmax 可微掩码**配合 L1 正则化 $\mathcal{L}_{mask} = \frac{1}{N}\sum_{i=1}^{N}|m|$，在训练中自动剪枝超过 50% 的无用高斯点。消融显示，去除剪枝后 4 视图高斯数量从 12.5K 增至 21.7K，而重建质量反而略降（Table 2），表明剪枝不仅提升渲染效率，还能通过稀疏化减少冗余表示对优化的干扰。

## 整体框架

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_P7zBSCs4Xt/figures/002_Figure_2.jpg]]
*Figure 2: The core of FastAvatar is a Large Gaussian Reconstruction Transformer (LGRT), which can flexibly process input data with varying expressions, poses, and camera angles, aggregating them into a high-precision 3DGS avatar model. This capability is enabled by several key designs: the interleaving of global attention and frame attention to register complex input data while encoding 3D positional prompts; multi-granular positional information encoding; and the use of landmark tracking loss and sliced fusion loss, allowing the model to smoothly and incrementally fuse additional input data*

FastAvatar 是一个前馈式可动画 3D 化身重建框架，其核心设计目标是打破现有方法对固定长度输入的依赖，实现对**任意数量、任意顺序**输入观测的直接处理与渐进式质量提升。整体函数定义为：

$$\mathcal{G}(I, \pi, z_{exp}, z_{pose})$$

其中 $I$ 为输入 RGB 图像集合，$\pi$ 为相机姿态，$z_{exp}$ 为表情系数，$z_{pose}$ 为头部姿态参数。框架输出一个位于规范空间中的可驱动 3DGS 化身模型，该模型可通过可微光栅化器 $\Psi$ 在给定表情和姿态下渲染为任意视角的 RGB 图像。

### 核心架构：大型高斯重建 Transformer (LGRT)

框架的核心是一个**大型高斯重建 Transformer (LGRT)**，其设计灵感源自 VGGT 架构，但针对 3DGS 直接预测进行了关键改造：将原 VGGT 中的密集预测 Transformer (DPT) 替换为直接预测规范空间 3DGS 属性的 MLP 头。LGRT 通过以下模块协同工作：

1. **DINOv2 特征提取**：将每帧 RGB 图像编码为视觉标记 $x_i$，作为后续处理的语义基础。

2. **多粒度引导编码**：相机姿态 $\pi_i$、表情系数 $z_i^{exp}$ 和头部姿态 $z_i^{pose}$ 分别经 MLP 处理后与视觉特征拼接，形成带有精细 3D 位置先验的面部标记：
   $$h_i = \mathcal{U}\left(x_i, \mathrm{MLP}([\pi_i, z_i^{exp}, z_i^{pose}])\right)$$
   这一设计有效缓解了因动画驱动带来的跨帧空间错位问题。

3. **交替注意力机制**：LGRT 采用**帧注意力 (Frame Attention)** 与**全局注意力 (Global Attention)** 交替工作的双流 DiT 结构：
   - **帧注意力**负责聚合单帧内部信息并注入 3D 位置提示；
   - **全局注意力**实现跨帧的空间配准与融合，是多帧信息整合的关键操作。

4. **GS Head (MLP)**：从处理后的标记直接预测每帧对应的 3DGS 属性（颜色、透明度、尺度、旋转、偏移等）。

5. **规范空间融合与剪枝**：将所有帧预测的高斯表示拼接为统一模型 $g_f = \mathcal{U}(g_1, g_2, \cdots, g_N)$，并通过 **Gumbel-Softmax 可微掩码**配合 L1 正则化进行稀疏化剪枝：
   $$\mathcal{L}_{mask} = \frac{1}{N}\sum_{i=1}^{N}|m|$$
   该机制可剪除超过 50% 的冗余高斯原语，在提升渲染效率的同时不影响重建质量。

### 增量重建与损失函数

FastAvatar 的关键创新在于其**增量高斯聚合**能力。通过引入**Landmark 跟踪损失**和**切片融合损失**，模型能够对任意数量的高斯模型进行精确对齐与融合，支持流式增量重建——随着新观测数据的持续输入，重建质量单调提升。

总损失函数为多目标的加权组合：
$$\mathcal{L} = \lambda_1 \mathcal{L}_{rgb} + \lambda_2 \mathcal{L}_{ssim} + \lambda_3 \mathcal{L}_{lpips} + \lambda_4 \mathcal{L}_{track} + \lambda_5 \mathcal{L}_{mask}$$
其中权重设置为 $\lambda_1=0.8$，$\lambda_2=0.1$，$\lambda_3=0.1$，$\lambda_4=0.1$，$\lambda_5=0.0005$，在像素级保真度、结构一致性、感知质量和几何对齐之间取得平衡。

### 输入输出流

整个 pipeline 的数据流可概括为：任意帧数的 RGB 图像与对应的相机/表情/姿态参数 → DINOv2 编码 + 多粒度 MLP 编码 → 交替注意力聚合与配准 → GS Head 逐帧预测高斯属性 → 规范空间拼接与可微剪枝 → 可驱动 3DGS 化身 → 可微光栅化渲染输出。这一设计使得 FastAvatar 在单视图到多视图的各种输入设置下均能保持统一的处理范式，无需针对不同输入数量调整架构。

## 核心模块与公式推导

### 整体框架定义

FastAvatar 被形式化为一个前馈式化身重建函数：

$$\mathcal{G}(I, \pi, z_{exp}, z_{pose})$$

其中 $I$ 为任意数量的无序 RGB 观测图像，$\pi$ 为相机姿态参数，$z_{exp}$ 和 $z_{pose}$ 分别为表情系数与头部姿态参数。该函数直接输出一个可驱动的规范空间 3DGS 化身模型。

### 多粒度引导编码模块

每帧观测首先通过 **DINOv2** 提取视觉标记 $x_i$。为缓解因表情和姿态变化导致的跨帧错位问题，引入多粒度引导编码——将相机姿态 $\pi_i$、表情系数 $z_i^{exp}$ 和头部姿态 $z_i^{pose}$ 拼接后经 MLP 处理，与视觉特征共同形成带位置先验的脸标记：

$$h_i = \mathcal{U}\left( x_i, \mathrm{MLP}([\pi_i, z_i^{exp}, z_i^{pose}]) \right)$$

其中 $\mathcal{U}(\cdot)$ 表示拼接操作。该编码为后续注意力模块提供了精细的 3D 空间提示。

### 交替注意力机制（LGRT 核心）

FastAvatar 的核心是 **大型高斯重建Transformer (LGRT)**，其关键设计为**全局注意力**与**帧注意力**的交替堆叠：

- **帧注意力**：基于双流 DiT 块实现，负责聚合单帧内部信息，并将多粒度编码注入，使每帧标记感知自身在 3D 空间中的位置。
- **全局注意力**：实现跨帧的 3D 空间配准与融合，是所有帧信息协调统一的基础操作。

这种交替结构使模型能灵活处理任意数量、任意顺序的输入帧。

### GS Head 与规范空间融合

经注意力模块处理后的标记送入 **GS Head**（MLP），直接预测每帧对应的 3DGS 属性（颜色、透明度、尺度、旋转、偏移等）。所有帧的高斯表示随后在规范空间拼接融合：

$$g_f = \mathcal{U}(g_1, g_2, \cdots, g_N)$$

其中 $g_i$ 为第 $i$ 帧预测的高斯属性组，$g_f$ 为融合后的统一 3DGS 化身。

### 可微高斯剪枝模块

为控制高斯点数量随输入帧数的线性增长，引入 **Gumbel-Softmax 可微掩码**配合 L1 正则化进行剪枝：

$$\mathcal{L}_{mask} = \frac{1}{N} \sum_{i=1}^{N} |m|$$

其中 $m$ 为可训练掩码参数。该机制可剪除超过 50% 的无用高斯点，在提升渲染效率的同时不影响重建质量。

### 切片融合渲染与损失函数

为支持任意帧数的增量融合训练，引入**切片融合损失**。对融合后的高斯模型 $g_{sliced}$ 进行可微渲染：

$$\hat{I}_{sliced} = \Psi(g_{sliced}, \pi_i, z_i^{exp}, z_i^{pose})$$

其中 $\Psi$ 为可微光栅化器。总损失函数为多项加权组合：

$$\mathcal{L} = \lambda_1 \mathcal{L}_{rgb} + \lambda_2 \mathcal{L}_{ssim} + \lambda_3 \mathcal{L}_{lpips} + \lambda_4 \mathcal{L}_{track} + \lambda_5 \mathcal{L}_{mask}$$

权重设置为 $\lambda_1=0.8$, $\lambda_2=0.1$, $\lambda_3=0.1$, $\lambda_4=0.1$, $\lambda_5=0.0005$。其中 $\mathcal{L}_{track}$ 为地标跟踪损失，用于监督跨帧高斯配准的结构一致性；$\mathcal{L}_{mask}$ 为前述稀疏正则项。

## 实验与分析

### 主要结果

FastAvatar 在 NeRSemble 数据集上进行了全面的定量与定性评估，与三类代表性方法对比：前馈式单图方法 **LAM**、基于优化的单图/多图方法 **MonoGaussianAvatar**、基于优化的多图方法 **GaussianAvatars**。评估涵盖 1/4/8/16 四种输入视图设置，指标包括 PSNR、SSIM、LPIPS、身份一致性（Identity）、建模时间与推理帧率（FPS）。

**Table 1** 展示了核心定量结果。FastAvatar 在所有视图设置下均取得最优重建质量：


![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_P7zBSCs4Xt/figures/003_Table_1.jpg]]
*Table 1: The quantitative comparison among FastAvatar, LAM He et al. (2025), MonoGaussianAvatar Chen et al. (2024c), and GaussianAvatars Qian et al. (2024a) includes 3 critical metrics: Reconstruction quality (PSNR, SSIM, LPIPS); Modeling time: Duration required to reconstruct the 3DGS model; Inference speed: Animation rendering FPS of the output 3DGS model*

- **1 视图**：PSNR 达 20.08，较 LAM 的 17.30 提升 2.78 dB；SSIM 0.860，LPIPS 0.143。渲染速度高达 240.17 FPS，远超 LAM（~125 FPS）和优化方法（均低于 10 FPS）。
- **4 视图**：PSNR 22.12，较 GaussianAvatars 的 17.52 提升 4.60 dB；SSIM 0.880，LPIPS 0.100。
- **16 视图**：PSNR 22.29，LPIPS 降至 0.092（GaussianAvatars 为 0.281），身份一致性指标亦全面领先。

值得注意的是，LAM 出现**逆反趋势**：随着输入视图增加，其定量性能反而下降（Figure 4 定性印证此现象）。这源于 LAM 缺乏有效的跨帧信息融合机制，多余视图引入的错位反而干扰重建。FastAvatar 则凭借全局注意力与增量高斯聚合，实现了重建质量随视图数**单调提升**。


![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_P7zBSCs4Xt/figures/006_Figure_4.jpg]]
*Figure 4: Reconstruction quality as the number of input observations increases. More observations improve reconstruction quality*

**Figure 3** 的定性对比进一步验证：在 1 视图设置下，优化方法（MonoGaussianAvatar、GaussianAvatars）因缺乏多视图约束而产生严重几何失真；LAM 虽能快速推理但细节模糊。随着视图数增加，FastAvatar 的纹理锐度与几何一致性持续改善，而 LAM 的口腔与眼部区域反而出现错位加剧。


![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_P7zBSCs4Xt/figures/004_Figure_3.jpg]]
*Figure 3: We benchmark FastAvatar against representative optimization-based methods (Mono-Gaussian Avatar Chen et al. (2024c), GaussianAvatar Qian et al. (2024a)) and feedforward approaches (LAM He et al. (2025)). Our results demonstrate the performance evolution across methods as the number of input views (referring to input images number) increases. Please zoom in for a better view*

在建模效率方面，FastAvatar 的建模时间随视图数从 0.013s（1 视图）增长至 0.215s（16 视图），仍远快于 GaussianAvatars 的逐场景优化（>100s）。

### 消融实验

**Table 2** 报告了关键组件的消融结果，在 THuman2.0 数据集上验证了各模块的因果贡献：


![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_P7zBSCs4Xt/figures/009_Table_2.jpg]]
*Table 2: Ablation studies on key components of FastAvatar. The appendix visualizations are strongly recommended for better understanding*

- **去除全局注意力（w/o global attention）**：1 视图 PSNR 从 20.08 骤降至 15.40，身份指标恶化至 0.400。全局注意力负责跨帧空间配准，缺失后模型退化为单帧独立预测，无法利用多帧互补信息。
- **去除 GS 融合（w/o GS fusion）**：16 视图 L1 误差从 0.0263 增至 0.0467，PSNR 从 22.19 降至 18.94。GS 融合将各帧预测的高斯模型在规范空间拼接为统一表示，缺失后多帧信息无法有效聚合。
- **去除切片融合损失（w/o sliced fusion loss）或跟踪损失（w/o tracking loss）**：重建质量轻微下降，但在增量重建场景中出现细节错位（Figure 9 可视化印证）。两类损失分别监督高斯模型的全局配准与时序一致性。
- **去除高斯剪枝（w/o GS pruning）**：4 视图高斯数量从 12.5K 增至 21.7K，渲染效率下降，而重建指标反而略降，表明剪枝不仅提升效率，还能通过稀疏正则化抑制冗余高斯带来的过拟合。

### 增量重建与长序列扩展

FastAvatar 的核心优势之一是**增量重建能力**：模型可接受任意长度、任意顺序的输入序列，重建质量随观测增加而持续提升（Figure 4）。受 **FramePack** 启发，在处理长序列时，FastAvatar 保留 16 帧均匀采样的稀疏输入，将其余帧压缩为聚合标记表示。Figure 5 显示，在 16 帧稀疏重建的基础上，融入压缩的额外帧可进一步增强纹理细节（如皮肤微结构、毛发边缘）。

Figure 11 展示了流式增量重建：随着流式输入逐步加入，口腔等大部分帧中不可见的区域逐渐改善，同时其他区域的结构一致性得以保持。

### 失败模式与局限性

**Figure 10** 揭示了典型失败案例，根源在于 FastAvatar 依赖 FLAME 参数化模型和 LBS 驱动：


![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_P7zBSCs4Xt/figures/029_Figure_10.jpg]]
*Figure 10: Typical failure cases: FastAvatar relying on LBS and FLAME-based encodings, struggles with complex facial muscle dynamics, fine-grained details (e.g., wrinkles), eye-gaze movements, and structures outside the FLAME topology such as the tongue*

1. **复杂面部动态**：LBS 线性混合无法精确表现非线性肌肉运动，导致皱纹等细粒度表情细节的重现较差。
2. **眼动追踪缺失**：模型无法准确捕获眼球运动方向，通常渲染为平均眼动方向。
3. **拓扑外结构**：高斯点锚定于 FLAME 顶点，无法表示舌头等 FLAME 拓扑外的结构。

此外，建模时间和显存消耗随输入帧数线性增长，16 视图时推理 FPS 降至 17.65，在处理数百帧视频时需进一步优化。

### 视角泛化

Figure 12 验证了 FastAvatar 在大范围新视角下的泛化能力：模型在 14 个完全不在训练集中的新视角上仍能实现高保真重建，表明全局注意力机制有效学习了跨视角的空间配准先验，而非简单记忆训练视角。

## 方法谱系与知识库定位

### 与前馈式可动画化身方法的关系

FastAvatar 在架构范式上直接继承自 **LAM**（单图前馈可动画高斯头像重建方法），但对其进行了根本性扩展。LAM 采用单图像 Transformer 架构，无法利用多帧观测信息，其性能在输入视图增加时反而退化——这一“逆关系”现象在 Table 1 和 Figure 4 中得到明确验证。FastAvatar 将架构基础升级为大型高斯重建 Transformer（LGRT），引入全局注意力与帧注意力交替机制，使模型能够对任意数量的输入帧进行空间配准与融合，从而将前馈方法的适用范围从单图扩展至可变长度多图输入。

与 **Avat3r**（多图前馈回归式可动画 3D 头像方法）相比，FastAvatar 的关键差异在于表示形式与增量能力。Avat3r 采用回归式架构，而 FastAvatar 直接预测规范空间下的 3DGS 属性，避免了回归式方法中常见的误差累积问题。在 Figure 6 的多视图重建视觉对比中，FastAvatar 展现出更优的细节保真度。此外，Avat3r 未报告增量重建能力，而 FastAvatar 通过增量高斯聚合机制（结合 landmark 跟踪损失与切片融合损失）实现了流式输入下的渐进式质量提升（Figure 11）。

### 与基于优化的化身方法的关系

在基于优化的方法谱系中，**GaussianAvatars** 和 **MonoGaussianAvatar** 代表了逐场景优化的 3DGS 头像重建路线。这类方法依赖参数化代理模型（如 FLAME）进行观察对齐，精度受限，且建模时间随场景复杂度线性增长。FastAvatar 通过多粒度引导编码（相机姿态、表情系数、头部姿态分别经 MLP 处理）缓解了动画驱动的错位问题，同时以前馈方式在秒级完成重建，建模效率提升数个数量级（Table 1：FastAvatar 建模时间远低于优化方法）。

值得注意的是，FastAvatar 与优化方法共享 FLAME 参数化模型的底层驱动机制，因此继承了相同的拓扑限制——高斯点锚定于 FLAME 顶点，无法表示 FLAME 拓扑外的结构（如舌头），且对复杂面部肌肉动态（如皱纹）的再现能力受限（Figure 10 典型失败案例）。

### 架构创新的知识贡献

FastAvatar 的核心架构创新——LGRT——是 VGGT 风格大规模 Transformer 在 3D 头像任务上的首次应用。其关键改造包括：

1. **预测头替换**：将 VGGT 中不稳定的 Dense Prediction Transformer（DPT）替换为直接预测规范空间 3DGS 属性的 MLP，避免了深度估计的中间表示误差。
2. **多粒度引导编码**：通过三个独立 MLP 分别处理相机姿态、表情系数和头部姿态，生成与 DINOv2 视觉标记维度对齐的位置编码，为注意力机制提供精细的 3D 空间先验。
3. **可微高斯剪枝**：采用 Gumbel-Softmax 可微掩码配合 L1 正则化，在训练过程中自动剪枝超过 50% 的无用高斯原语，在不牺牲重建质量的前提下提升渲染效率（消融实验：4 视图下高斯数量从 21.7K 降至 12.5K，性能反而略升）。

### 适用边界与局限

FastAvatar 的适用边界由以下因素界定：

- **FLAME/LBS 依赖性**：模型通过 LBS 和 FLAME 编码驱动动画，无法精确表现复杂面部肌肉动态，皱纹重现质量较差；眼动追踪无法准确捕获，通常渲染为平均眼动方向；FLAME 拓扑外的结构（如舌头）完全无法表示（Figure 10）。
- **计算资源线性增长**：虽然支持任意帧数输入，但建模时间和显存消耗随输入帧数线性增长，推理 FPS 在大量帧时下降明显（Table 1：1 视图 240.17 FPS → 16 视图 17.65 FPS）。
- **训练数据依赖**：模型在 NeRSemble 多视角数据集上训练，其对真实世界无标定数据的泛化能力尚未充分验证。

### 开放问题

1. **突破参数化表征限制**：如何超越 FLAME/LBS 的拓扑约束，捕获更丰富的面部动态（如皱纹、舌头）和拓扑外结构，是提升化身真实感的关键方向。
2. **长序列高效扩展**：在处理数百帧视频时，当前线性增长的资源消耗模式不可持续，需要探索更高效的帧聚合策略（如 FramePack 启发的帧压缩方法已在初步实验中展示潜力，Figure 5）。
3. **流式增量重建的鲁棒性**：滑动窗口增量重建方法在场景突变、遮挡或极端姿态下的鲁棒性是否充分，仍需系统性评估。
4. **in-the-wild 泛化**：方法在更广泛的真实世界无标定数据上的表现，以及跨身份、跨光照条件的泛化能力，需要进一步验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/FastAvatar_Towards_Unified_and_Fast_3D_Avatar_Reconstruction_with_Large_Gaussian_Reconstruction_Transformers.pdf]]
