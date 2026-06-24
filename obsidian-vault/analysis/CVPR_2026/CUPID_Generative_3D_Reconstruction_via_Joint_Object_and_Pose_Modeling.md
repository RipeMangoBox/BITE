---
title: "CUPID: Generative 3D Reconstruction via Joint Object and Pose Modeling"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CUPID_Generative_3D_Reconstruction_via_Joint_Object_and_Pose_Modeling.pdf
project_link: "https://cupid3d.github.io"
code_link: null
aliases:
- CUPID
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 在统一流模型中显式联合建模物体与姿态的后验分布，并通过姿态对齐的像素特征注入实现几何重建与纹理保真度的双重提升。
primary_logic: 将相机姿态重新参数化为3D UV立方体（密集3D-2D对应），使得首先生成的粗糙几何与对应关系可通过PnP精确恢复姿态，而后在第二阶段利用恢复的姿态对每个体素注入像素对齐的DINO和低级特征，从而在保持生成多样性的同时大幅提升重建的几何精度和视觉一致性。
claims:
- 联合建模物体与姿态使其在单目重建中显著超越生成式和重建式基线：在Toys4k上中值Chamfer距离降至0.236，优于所有3D方法。
- 姿态对齐的第二阶段调节将PSNR从27.47 dB提升至30.05 dB，验证了像素级特征注入的有效性。
- 多视图和场景级重建无需后优化或微调即可实现，展现出解耦建模的扩展性。
- Toys4k 上 CD (med, mm) = 0.236
---

# CUPID: Generative 3D Reconstruction via Joint Object and Pose Modeling

> [!tip] 核心洞察
> 将相机姿态重新参数化为3D UV立方体（密集3D-2D对应），使得首先生成的粗糙几何与对应关系可通过PnP精确恢复姿态，而后在第二阶段利用恢复的姿态对每个体素注入像素对齐的DINO和低级特征，从而在保持生成多样性的同时大幅提升重建的几何精度和视觉一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | CUPID：通过联合物体与姿态建模的生成式3D重建 |
| 英文题名 | CUPID: Generative 3D Reconstruction via Joint Object and Pose Modeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.20776) · [Project](https://cupid3d.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | CUPID |
| Dataset | Toys4k, GSO |

> [!tip] 效果简介
> - Toys4k 上，CD (med, mm) 0.236 vs 1.291 (OpenLRM) (-1.055)；F-score (0.05) ↑ 97.76 vs 90.60 (OpenLRM) (+7.16)；PSNR ↑ (输入视角) 30.05 vs 28.10 (OpenLRM, 近似) (+1.95)。
> - GSO 上，mIOU ↑ 95.27 vs 91.35 (OpenLRM) (+3.92)。

## 概述

现有3D视觉方法长期存在一个根本性割裂：**生成模型**（如**TRELLIS**, Zhao et al., arXiv 2024）能够产生多样化的3D内容，但忽略相机姿态，难以忠实于输入视图；**重建方法**（如**OpenLRM**, He et al., 2023；**LaRa**, Chen et al., CVPR 2024）固守像素对齐，却缺乏生成能力，无法合理补全被遮挡区域。这一割裂的根源在于缺乏对物体与相机姿态的**联合建模**——传统方法要么将姿态视为已知常量，要么将其完全忽略，导致无法从单张图像中同时恢复规范坐标系下的完整3D物体及其拍摄姿态。

CUPID通过一个统一的流模型框架解决了上述瓶颈。其核心洞见在于将相机姿态重新参数化为**3D UV立方体**（即密集的3D-2D对应关系），使得首先生成的粗糙几何与对应关系可通过PnP精确恢复姿态，而后在第二阶段利用恢复的姿态对每个体素注入姿态对齐的DINO和低级视觉特征。这种联合建模策略在保持生成多样性的同时，大幅提升了重建的几何精度和视觉一致性。

实验表明，CUPID在多个基准上显著超越现有方法：在Toys4k数据集上，中值Chamfer距离降至**0.236 mm**，较OpenLRM降低超过1 mm；输入视角的PSNR达到**30.05 dB**，相比整体重建模型提升超过3 dB；同时，相机姿态恢复精度极高，平均旋转误差仅**0.46°**，重投影误差为0.0009（归一化像素）。该方法无需后优化或微调即可自然扩展到多视图条件重建和场景级组合重建，展现出解耦建模的强扩展性。

## 背景与动机

从单张二维图像恢复完整的三维物体是计算机视觉的核心难题。图像形成过程可形式化为 $\mathbf{I} = \mathcal{P}(\mathcal{O}, \pmb{\theta})$——渲染图像 $\mathbf{I}$ 由规范坐标系下的三维物体 $\mathcal{O}$ 与相机姿态 $\pmb{\theta}$ 共同决定。然而，从单一观测 $\mathbf{I}^{\mathrm{cond}}$ 反推 $\mathcal{O}$ 和 $\pmb{\theta}$ 是高度病态的：同一张图像可以由不同的物体-姿态组合产生，而遮挡区域的信息则完全缺失。

现有方法在面对这一病态问题时，呈现出两种割裂的范式。**生成式方法**（如 **TRELLIS**，Zhao et al., arXiv 2024）利用扩散先验从图像生成多样化的三维内容，但普遍忽略相机姿态的显式建模，导致生成结果难以忠实于输入视图的几何与外观。**重建式方法**（如 **OpenLRM**，He et al., 2023；**LaRa**，Chen et al., CVPR 2024）追求像素对齐的输入视图一致性，但缺乏生成能力，无法合理补全被遮挡的区域，且通常将相机姿态固定为单位阵或依赖外部标定。点图回归方法（如 **VGGT**，Wang et al., arXiv 2025；**MoGe**，Lu et al., arXiv 2024）虽能恢复部分几何，但仅输出非完整的三维信息，无法提供可渲染的完整物体模型。

这一割裂的根本瓶颈在于：**缺乏对物体与相机姿态的联合建模**。生成模型忽略姿态，无法建立三维结构与输入像素之间的精确对应；重建模型固守像素对齐，丧失了在遮挡区域进行合理生成的能力。二者各自解决了问题的一半，却无法兼顾几何保真度与生成完整性。

CUPID 的动机正是弥合这一鸿沟：将三维重建重新定义为在统一流模型中对物体与姿态联合后验 $p(\mathcal{O}, \pmb{\theta} \mid \mathbf{I}^{\mathrm{cond}})$ 的估计问题。通过显式建模相机姿态并将其作为第二阶段的调节信号，CUPID 使生成过程既能保持多样性，又能通过姿态对齐的像素特征注入实现高保真的输入视图一致性——在单目重建中将 Chamfer 距离降至 0.236 mm，PSNR 提升超过 3 dB，同时无需任何后优化即可扩展到多视图与场景级重建。

## 核心创新

CUPID的核心创新在于将3D生成与重建统一到一个**联合建模物体与相机姿态**的流模型中，从根本上改变了现有方法将生成与重建割裂的范式。其关键洞察是：**将相机姿态重新参数化为3D UV立方体**——即密集的3D-2D对应关系场——使得生成模型可以在规范空间下同时采样粗糙几何与姿态编码，再通过PnP求解器精确恢复相机矩阵。这一设计带来了三个根本性的方法改进：

1. **从无姿态到显式姿态建模**：现有重建方法（如OpenLRM, He et al., 2023）将相机姿态固定为单位阵或完全忽略，生成方法（如TRELLIS, Zhao et al., arXiv 2024）则不建模输入视图的相机参数。CUPID通过UV立方体这一过参数化表示，将姿态估计内化为生成过程的一部分，使模型能够明确推理“物体在何处、从哪个视角被观察”。

2. **从全局特征到姿态对齐的局部像素特征注入**：TRELLIS等基线使用全局注意力图像特征进行条件生成，缺乏对物体表面与输入图像像素之间精确对应关系的利用。CUPID在第二阶段利用恢复的相机姿态，将每个体素投影到输入图像上，通过双线性插值提取DINO高层特征与卷积低层特征，实现**姿态对齐的条件特征融合**（公式见Eq.3）。消融实验（Table 4）表明，仅添加DINOv2位置嵌入或全局DINO特征带来的PSNR提升有限（约27.5 dB），而完整的姿态对齐局部特征注入将PSNR从27.47 dB显著提升至30.05 dB，验证了这一设计的决定性作用。

3. **从单物体到场景级组合重建的自然扩展**：由于CUPID显式建模了每个物体的3D-2D对应关系，它可以自然地处理多物体场景——通过遮挡感知训练（随机掩码微调）使模型能从部分可见物体生成完整3D，再通过3D-3D相似变换将各物体组合到统一场景坐标系中（Figure 4），无需后优化或额外对齐步骤。

这些改进的因果链条清晰：**UV立方体 → 精确姿态恢复 → 姿态对齐特征注入 → 几何精度与纹理保真度双重提升**。在Toys4k数据集上，CUPID的中值Chamfer距离降至0.236 mm，显著优于OpenLRM的1.291 mm（Table 1）；输入视角PSNR达到30.05 dB，超越所有重建与生成基线（Table 2）。这一联合建模框架将原本割裂的生成多样性与重建忠实性统一到了一个端到端的条件采样过程中。

## 整体框架

CUPID 将生成式单目 3D 重建形式化为在观测约束下对物体与相机姿态联合后验的估计：给定条件图像 $\mathbf{I}^{\mathrm{cond}}$，目标是采样 $p(\mathcal{O}, \pmb{\theta} \mid \mathbf{I}^{\mathrm{cond}})$，且满足图像形成模型 $\mathbf{I}^{\mathrm{cond}} = \mathcal{P}(\mathcal{O}, \pmb{\theta})$（见公式 $\mathbf{I} = \mathcal{P}(\mathcal{O}, \pmb{\theta})$）。为实现这一目标，CUPID 采用了一个两阶段级联流模型，其核心创新在于将相机姿态显式地纳入生成过程，并通过姿态对齐的特征注入实现高保真重建。

**整体流程**（参见 Figure 3）如下：

1. **第一阶段：粗几何与姿态联合生成**。流模型 $G_S$ 以条件图像 $\mathbf{I}^{\mathrm{cond}}$ 为输入，在规范坐标系下同时生成两个关键表示：
   - **占用格子**：描述物体的粗糙 3D 几何形状。
   - **UV 立方体**：一种密集的 3D-2D 对应场，将相机姿态重新参数化为一组体素中心 $\mathbf{x}_i$ 到图像像素坐标 $\mathbf{u}_i$ 的映射。这种过参数化表示使得姿态信息能够自然地嵌入到体积潜在空间中。

2. **PnP 姿态恢复**。从生成的 UV 立方体中提取 3D-2D 对应关系，通过最小二乘优化求解相机矩阵：
   $$\mathbf{P}^* = \underset{\mathbf{P}}{\arg\min} \sum_{i=1}^{L} \left\| \pi(\mathbf{P}, \mathbf{x}_i) - \mathbf{u}_i \right\|^2$$
   再将 $\mathbf{P}^*$ 分解为内参矩阵 $\mathbf{K}$、旋转 $\mathbf{R}$ 和平移 $\mathbf{t}$。该过程可精确恢复相机姿态（平均重投影误差仅 0.0009 归一化像素，旋转误差 0.46°，见 Table 5）。

3. **姿态对齐特征提取**。利用恢复的相机姿态，将第一阶段生成的占用体素投影回输入图像，通过双线性插值提取 DINOv2 高层语义特征：
   $$\mathbf{f}_i^{\mathrm{DINO}} = \mathrm{BilinearInterp}(\mathbf{u}_i, \mathrm{DINO}(\mathbf{I}^{\mathrm{cond}})) \in \mathbb{R}^{1024}$$
   同时，通过浅层卷积头提取低层视觉特征（如颜色、纹理细节）。这些特征经 SlatEncoder 融合为姿态对齐的高层潜在表示：
   $$\{\mathbf{f}_i^{\mathrm{h}}\}_{i=1}^{L} = \mathrm{SlatEncoder}\left(\{\mathbf{x}_i, \mathbf{f}_i^{\mathrm{DINO}}\}_{i=1}^{L}\right)$$

4. **第二阶段：姿态条件精细化**。流模型 $G_L$ 以第一阶段生成的占用格子和姿态对齐特征 $\mathbf{f}^{\mathrm{h}}$ 为条件，在占用体素上生成精细的几何与外观特征。这一设计使得模型能够在保持生成多样性的同时，严格忠实于输入视图的像素级信息。

5. **解码**。最终，解码器将第二阶段生成的体积潜在特征解码为 3D 高斯泼溅或网格表示，完成从单张图像到规范 3D 模型的完整重建。

**模块关系与数据流**：整个管道以 3D VAE 编码器 $\varphi$ 为桥梁，将物体和姿态映射到统一的体积潜在特征空间 $\mathbf{z} = \varphi(\mathcal{O}, \pmb{\theta})$，并通过条件流匹配损失进行端到端训练：
$$\mathcal{L}_{\mathrm{CFM}}(\phi) = \mathbb{E}_{t,\mathbf{z}_0,\epsilon} \left\| \mathbf{v}_\phi(\mathbf{z}_t, \mathbf{I}^{\mathrm{cond}}, t) - (\epsilon - \mathbf{z}_0) \right\|_2^2$$

该框架的关键优势在于**物体与姿态的解耦联合建模**：第一阶段生成粗糙但姿态明确的 3D 结构，第二阶段利用恢复的姿态注入像素对齐特征以提升几何精度和纹理保真度。消融实验证实，仅添加全局 DINO 特征或位置嵌入带来的 PSNR 提升有限（27.47 dB），而完整的姿态对齐局部特征融合可将 PSNR 提升至 30.05 dB（Table 4），验证了该设计的决定性作用。

此外，该框架天然支持**遮挡感知的场景级重建**：通过对各物体进行遮挡感知调节（随机掩码微调）生成完整 3D 模型，再利用 3D-3D 相似变换组合为完整场景（Figure 4），无需后优化或微调即可实现。

### 补充图表

![[assets/figures/papers/paper_list_l2458_https_arxiv_org_abs_2510_20776/figures/003_Figure_3.jpg]]
*Figure 3: Overview of CUPID’s pipeline. From a single input image, CUPID first generates an occupancy and a UV cube in canonical space. Then, a Perspective-n-Point (PnP) solver (i.e., Eq. 2) recovers the camera pose. Using this recovered camera pose, we extract posealigned conditioning latents and visual features (i.e., Eq. 3), along with noisy structured latents, to generate the geometry and appearance features, which will be decoded to the 3D Gaussian splats and mesh*

## 核心模块与公式推导

### 3.1 问题形式化与条件流匹配框架

CUPID将生成式重建形式化为估计物体与姿态的联合后验分布 $p(\mathcal{O}, \pmb{\theta} \mid \mathbf{I}^{\mathrm{cond}})$，并满足观测约束 $\mathbf{I}^{\mathrm{cond}} = \mathcal{P}(\mathcal{O}, \pmb{\theta})$。其中 $\mathcal{O}$ 为规范坐标系下的3D物体，$\pmb{\theta}$ 为相机姿态，$\mathcal{P}$ 为投影映射。

为实现这一目标，CUPID采用条件流匹配（Conditional Flow Matching, CFM）框架。首先使用编码器 $\varphi$ 将3D物体与相机姿态映射为体积潜在特征 $\mathbf{z} = \varphi(\mathcal{O}, \pmb{\theta})$，随后训练一个速度场 $\mathbf{v}_\phi$ 以从噪声恢复该潜在表示。CFM损失函数定义为：

$$\mathcal{L}_{\mathrm{CFM}}(\phi) = \mathbb{E}_{t,\mathbf{z}_0,\epsilon} \left\| \mathbf{v}_\phi(\mathbf{z}_t, \mathbf{I}^{\mathrm{cond}}, t) - (\epsilon - \mathbf{z}_0) \right\|_2^2$$

其中 $\mathbf{z}_0$ 为干净潜在特征，$\epsilon \sim \mathcal{N}(0, \mathbf{I})$ 为噪声样本，$\mathbf{z}_t = (1-t)\mathbf{z}_0 + t\epsilon$ 为时间 $t \in [0,1]$ 的插值状态。该损失驱动速度场学习从噪声到数据分布的最优传输路径。

### 3.2 相机姿态的过参数化表示与PnP恢复

传统方法通常忽略相机姿态或将其固定为单位阵，CUPID的核心创新在于将相机姿态 $\pmb{\theta}$ 重新参数化为密集的3D-2D对应关系——即3D UV立方体。具体而言，在规范空间内定义一个包含 $L$ 个体素的立方体区域，每个体素中心 $\mathbf{x}_i$ 被赋予其在输入图像上的对应像素坐标 $\mathbf{u}_i$：

$$\pmb{\theta} \triangleq \{\mathbf{x}_i, \mathbf{u}_i\}_{i=1}^{L}$$

这种过参数化表示具有两个关键优势：(1) 密集对应关系为后续的PnP求解提供了冗余约束，增强了姿态估计的鲁棒性；(2) UV立方体可直接由第一级流模型生成，与占用格子联合采样，实现了物体几何与相机姿态的端到端联合建模。

从UV立方体恢复全局相机矩阵 $\mathbf{P}$ 的过程通过最小二乘优化完成：

$$\mathbf{P}^* = \underset{\mathbf{P}}{\arg\min} \sum_{i=1}^{L} \left\| \pi(\mathbf{P}, \mathbf{x}_i) - \mathbf{u}_i \right\|^2$$

其中 $\pi$ 为透视投影函数。获得 $\mathbf{P}^*$ 后，通过RQ分解将其拆解为内参矩阵 $\mathbf{K}$、旋转矩阵 $\mathbf{R}$ 和平移向量 $\mathbf{t}$。实验表明，该恢复过程的精度极高：平均重投影误差仅为0.0009（归一化像素坐标），平均旋转误差为0.46°（Table 5）。

### 3.3 两阶段级联流模型

CUPID采用两阶段级联流模型架构（Figure 3），分别对应粗粒度结构生成与姿态对齐的精细化重建。

**第一阶段（$G_S$）：占用与姿态生成。** 该阶段以输入图像 $\mathbf{I}^{\mathrm{cond}}$ 为条件，联合生成规范空间下的占用格子（occupancy grid）与UV立方体。占用格子定义了物体的粗糙几何形状，UV立方体则编码了相机姿态信息。两者共享同一潜在空间，确保了物体形状与观测视角的一致性。

**第二阶段（$G_L$）：姿态对齐的几何与外观生成。** 利用第一阶段恢复的相机姿态 $(\mathbf{K}, \mathbf{R}, \mathbf{t})$，对占用格子中的每个体素进行姿态对齐的特征注入。具体而言，对于每个体素中心 $\mathbf{x}_i$，首先通过恢复的相机参数将其投影到图像平面得到像素坐标 $\mathbf{u}_i$，然后通过双线性插值提取DINOv2高层语义特征：

$$\mathbf{f}_i^{\mathrm{DINO}} = \mathrm{BilinearInterp}(\mathbf{u}_i, \mathrm{DINO}(\mathbf{I}^{\mathrm{cond}})) \in \mathbb{R}^{1024}$$

随后，将体素坐标 $\mathbf{x}_i$ 与DINO特征 $\mathbf{f}_i^{\mathrm{DINO}}$ 拼接，通过SlatEncoder（一种3D VAE编码器）融合为高层几何-外观特征：

$$\{\mathbf{f}_i^{\mathrm{h}}\}_{i=1}^{L} = \mathrm{SlatEncoder}\left(\{\mathbf{x}_i, \mathbf{f}_i^{\mathrm{DINO}}\}_{i=1}^{L}\right)$$

此外，还通过浅层卷积头提取低层视觉特征（如颜色、纹理细节），与高层特征共同注入第二级流模型。这种姿态对齐的局部特征注入机制，使得模型能够精确地将图像像素信息“粘贴”到对应的3D位置，从而在保持生成多样性的同时大幅提升重建的几何精度与视觉一致性。消融实验（Table 4）表明，该设计是性能提升的关键：仅添加全局DINO特征或DINO位置嵌入的提升有限，而完整的姿态对齐局部特征融合将PSNR从27.47 dB提升至30.05 dB。

最终，解码器将第二级流模型生成的潜在特征解码为3D高斯泼溅（3D Gaussian Splatting）或网格表示，支持高质量的任意视角渲染。

### 补充图表

![[assets/figures/papers/paper_list_l2458_https_arxiv_org_abs_2510_20776/figures/002_Figure_2.jpg]]
*Figure 2: Results for generative 3D reconstruction from a single test image. Given an input image (top left), CUPID estimates camera pose (bottom left) and reconstructs 3D model (bottom right), re-rendering the input (top right). It is robust to changes in scale, placement, and lighting while preserving fine details, and supports component-aligned scene reconstruction (bottom row). All results are produced in seconds via feed-forward sampling of the learned model. See cupid3d.github.io for an immersive view of the interactive 3D results*

## 实验与分析

### 核心性能指标

CUPID在单目几何精度、输入视角一致性、完整3D质量三个维度上均实现了对现有方法的显著超越。在Toys4k基准上，CUPID的中值Chamfer距离（CD）降至0.236 mm，相比基于大型重建模型的**OpenLRM**（He et al., 2023）的1.291 mm降低了超过一个数量级（-1.055 mm），F-score（阈值0.05）达到97.76，较OpenLRM的90.60提升7.16个百分点。在GSO数据集上，mIOU达到95.27，优于OpenLRM的91.35（+3.92）。这些结果验证了联合建模物体与姿态的核心假设——将相机姿态从隐式假设中显式化，使得生成过程能够忠实于输入视图的几何约束（Table 1）。

![[assets/figures/papers/paper_list_l2458_https_arxiv_org_abs_2510_20776/figures/005_Table_1.jpg]]
*Table 1: Monocular geometry accuracy. CUPID outperforms all 3D reconstruction and generation baselines and matches point-map regression methods that predict only partial geometry. Note that VGGT uses a ground-truth object mask, which may overestimate accuracy*

值得注意的是，CUPID在几何精度上匹配甚至超越了仅预测部分几何的点图回归方法。**VGGT**（Wang et al., arXiv 2025）虽然使用了真实物体掩码（可能高估精度），CUPID仍能在不依赖掩码先验的情况下达到可比性能。这表明CUPID的生成式框架并未牺牲几何精度，反而通过姿态对齐的特征注入实现了重建与生成的统一。

输入视角一致性方面，CUPID在Toys4k上达到30.05 dB的PSNR，相比OpenLRM的约28.10 dB提升约1.95 dB，LPIPS降至0.089（Table 2）。这一提升直接归因于第二阶段姿态对齐调节机制：恢复的相机姿态使得模型能够精确地将体素投影到输入图像上，提取像素对齐的DINO特征和低级卷积特征，从而在保持生成多样性的同时大幅提升纹理保真度。

![[assets/figures/papers/paper_list_l2458_https_arxiv_org_abs_2510_20776/figures/008_Table_2.jpg]]
*Table 2: Input-view consistency. CUPID achieves superior input view consistency, producing accurate appearance alignment*

完整3D质量评估采用新颖视角的CLIP（ViT-L/14）分数，CUPID在Toys4k上达到0.9291，优于基于2D扩散先验的**LaRa**（Chen et al., CVPR 2024）的约0.9142（+0.0149），表明生成的不可见区域在语义一致性和视觉质量上均具优势（Table 3）。

![[assets/figures/papers/paper_list_l2458_https_arxiv_org_abs_2510_20776/figures/010_Table_3.jpg]]
*Table 3: Comparison on full 3D quality. We report CLIP image scores of novel views following [11]*

### 消融实验：姿态对齐调节的关键作用

Table 4的系统消融揭示了姿态对齐调节（Pose-Aligned Conditioning, PAC）各组件对性能的贡献梯度。基线（a）采用**TRELLIS**（Zhao et al., arXiv 2024）的全局注意力图像特征，PSNR仅为27.47 dB。仅添加DINOv2位置嵌入到SLat潜变量中（b）或拼接全局DINO特征（c）的提升有限，PSNR分别提升至约27.8 dB和28.1 dB。关键突破来自姿态对齐的局部特征注入：当利用恢复的相机姿态将体素投影到图像上，并通过双线性插值提取DINO特征后经3D VAE编码为高层特征$f_i^h$（Eq. 3），再与浅层卷积特征融合（e），PSNR跃升至30.05 dB（+2.58 dB）。这一结果证实了因果机制——姿态对齐使得像素级信息能够精确注入到对应的3D位置，而非依赖全局注意力进行模糊匹配。

Figure 6的定性对比进一步支持了这一结论：无PAC的基线生成结果在纹理细节上模糊且存在几何偏移，而完整方法（e）能够恢复精细的纹理和准确的几何轮廓。消融还表明，仅使用高层DINO特征（d）已能带来显著改善，但融合低级卷积特征（e）进一步提升了边缘锐度和局部细节保真度。

### 姿态恢复精度

CUPID通过3D UV立方体重新参数化相机姿态，并利用PnP求解器从生成的密集3D-2D对应关系中恢复相机矩阵。Table 5显示，恢复的相机姿态具有极高的精度：平均重投影误差仅为0.0009（归一化像素），平均旋转误差0.46°，平均平移误差和视场角误差均处于极低水平。这一精度是第二阶段姿态对齐调节能够有效工作的前提——若姿态估计存在显著误差，投影位置将偏离真实像素，导致特征注入错位，反而损害重建质量。

### 失败模式与局限性

尽管CUPID在受控基准上表现优异，其设计存在若干已知脆弱点：

1. **场景组合依赖分割掩码**：CUPID通过遮挡感知调节（随机掩码微调）支持从部分可见物体生成完整3D，并在场景级重建中通过3D-3D相似变换组合多个物体（Figure 4, Figure 10）。然而，真实图像中的掩码边界错误会传播至重建结果，导致物体边缘出现伪影或缺失。当前方法未提供自动分割方案，需要手动或外部模型提供掩码。

![[assets/figures/papers/paper_list_l2458_https_arxiv_org_abs_2510_20776/figures/004_Figure_4.jpg]]
*Figure 4: Component-aligned scene reconstruction. For a scene with multiple objects, our method can rebuild each object using the occlusion-aware 3D generator and then solve 3D–3D similarity transformation to accurately recompose the scene*

![[assets/figures/papers/paper_list_l2458_https_arxiv_org_abs_2510_20776/figures/029_Figure_10.jpg]]
*Figure 10: Additional examples of component-aligned scene reconstruction. For each example shown, the panels display: (top left) the input image, (top right or bottom left) the final rendered output, and (bottom) the reconstructed individual components, color-coded for clarity*

2. **光照与外观未解耦**：模型未显式分离材质、光照与几何，对极端光照变化（如强阴影、镜面反射）的泛化能力有限。这意味着在野外图像中，重建的纹理可能包含烘焙的阴影或高光，而非真实的漫反射属性。

3. **多视图朝向不一致**：虽然CUPID的解耦建模天然支持多视图条件（Figure 7），各视图独立恢复的3D朝向可能不一致，需要更先进的融合方案来解决跨视图的朝向歧义。

![[assets/figures/papers/paper_list_l2458_https_arxiv_org_abs_2510_20776/figures/011_Figure_7.jpg]]
*Figure 7: Multi-view conditioning. Our decoupled joint modeling naturally supports multi-view conditioning. When multiple input views are available, we fuse the shared view-agnostic object latent across flow paths (similar to MultiDiffusion [2]), enabling object and cameras refinement across all views. Top: inputs; Middle: reconstructed 3D object and camera poses; Bottom: rendered images and geometry*

4. **训练数据偏差**：模型主要在合成渲染数据上训练，对真实世界图像中常见的模糊、噪声、非朗伯表面等复杂情况的鲁棒性尚需进一步验证。遮挡感知训练使用的合成随机掩码可能无法覆盖真实场景中的复杂遮挡模式。

### 重要图表结论

- **Table 1**：CUPID在单目几何精度上超越所有3D重建和生成基线，匹配仅预测部分几何的点图回归方法。
- **Table 2**：输入视角一致性显著优于重建式和生成式方法，PSNR达30.05 dB。
- **Table 3**：完整3D质量（CLIP分数）一致优于所有基线，验证生成多样性未牺牲语义保真度。
- **Table 4**：姿态对齐的局部特征注入是性能提升的关键因果组件，PSNR从27.47 dB提升至30.05 dB。
- **Table 5**：相机姿态恢复精度极高（重投影误差0.0009，旋转误差0.46°），为第二阶段调节提供可靠基础。
- **Figure 5**：定性对比显示CUPID在纹理细节和几何准确性上显著优于OpenLRM和LaRa。
- **Figure 6**：消融定性对比直观展示了PAC各组件的渐进式改进。
- **Figure 7**：多视图条件重建展示了框架的扩展性，无需后优化或微调。
- **Figure 10**：场景级组合重建展示了从单物体到多物体场景的扩展能力。

![[assets/figures/papers/paper_list_l2458_https_arxiv_org_abs_2510_20776/figures/007_Table_4.jpg]]
*Table 4: Ablation studies of pose-aligned conditioning*

![[assets/figures/papers/paper_list_l2458_https_arxiv_org_abs_2510_20776/figures/012_Table_5.jpg]]
*Table 5: Pose Reconstruction Fidelity. We evaluate the accuracy of camera poses recovered from the decoded UV volumes via the PnP algorithm. We report the Reprojection Error in normalized pixels, RRE, RTE, and RFov in degrees*

![[assets/figures/papers/paper_list_l2458_https_arxiv_org_abs_2510_20776/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparison of various pose-aligned conditioning. Our method (e) achieves the best visual quality in terms of color fidelity and detail*

![[assets/figures/papers/paper_list_l2458_https_arxiv_org_abs_2510_20776/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison on input view consistency. We render the input view using its generated camera pose. For view centric methods (LRM, LaRa), we use ground-truth intrinsic for rendering as they do not model intrinsic. Our method produces the highestfidelity geometry and appearance; LRM hallucinates incorrect details, LaRa is overly blurry due to 2D diffusion inconsistencies, and 3D generation method OnePoseGen frequently fails to register pose reliably*

## 方法谱系与知识库定位

### 1. 与基线工作的关系

CUPID 的核心贡献在于将**生成式重建**统一为物体与相机姿态的联合后验估计，从而桥接了此前割裂的两条技术路线：**3D 生成**与**3D 重建**。理解这一谱系定位，需要从以下几个维度审视其与基线工作的关系。

**相对于单目点图回归方法**：**VGGT**（Wang et al., arXiv 2025）和 **MoGe**（Lu et al., arXiv 2024）等单目几何估计方法仅输出仿射不变或度量点图，能够提供部分几何信息，但无法重建完整的3D物体（包括遮挡区域和纹理）。CUPID 在几何精度上与之持平甚至超越——在 Toys4k 上中值 Chamfer 距离降至 0.236 mm（Table 1）——但额外生成了完整纹理的规范模型和精确相机姿态，实现了从“部分几何估计”到“完整3D重建”的质变。需注意 VGGT 使用了真实物体掩码，其精度可能被高估。

**相对于大型重建模型（LRM）**：**OpenLRM**（He et al., 2023）等基于前馈Transformer的重建方法将3D重建视为从图像到三平面或体积特征的单步回归。其根本局限在于：缺乏显式姿态建模，假设输入为规范视角或固定内参，导致对任意视角输入的泛化能力不足；同时，确定性回归缺乏生成多样性，难以补全严重遮挡区域。CUPID 在 Toys4k 上将中值 Chamfer 距离从 OpenLRM 的 1.291 mm 降至 0.236 mm，F-score 从 90.60 提升至 97.76（Table 1），这一超过一个数量级的几何精度提升，本质上源于**解耦的联合建模**：先通过流模型生成粗糙几何与UV立方体（姿态编码），再利用恢复的姿态注入像素对齐特征进行精细重建。

**相对于稀疏视图重建方法**：**LaRa**（Chen et al., CVPR 2024）利用2D扩散先验进行稀疏视图重建，但依赖固定的相机外参假设，且扩散先验与3D几何的一致性缺乏显式约束。CUPID 在输入视角一致性上全面超越：PSNR 达到 30.05 dB（Table 2），LPIPS 降至 0.089，同时在新颖视角的 CLIP 分数上达到 0.9291（Table 3），表明其不仅忠实于输入视图，还能生成语义合理的新颖视角外观。

**相对于3D生成模型**：CUPID 直接以 **TRELLIS**（Zhao et al., arXiv 2024）作为骨干架构，但对其进行了关键性改造。TRELLIS 作为基础3D生成模型，仅使用全局注意力图像特征进行条件生成，缺乏对相机姿态的显式建模，因此生成的3D物体与输入视图之间缺乏几何一致性。CUPID 的改造体现在两个关键槽位：其一，将相机姿态重新参数化为3D UV立方体（密集3D-2D对应），使生成模型能够隐式编码姿态信息；其二，将第二阶段的全局图像特征替换为**姿态对齐的局部像素特征**——通过 PnP 恢复的相机矩阵将体素投影到图像平面，双线性插值提取 DINO 特征，再经 SlatEncoder 与体素坐标融合（Eq. 3）。这一改造使 PSNR 从 27.47 dB 跃升至 30.05 dB（Table 4），证明像素级特征注入是提升重建保真度的关键因果机制。

**相对于单视图生成式姿态估计**：**OnePoseGen** 等工作尝试从单视图同时生成物体和姿态，但缺乏将姿态显式用于后续几何细化的闭环。CUPID 的独特之处在于将姿态估计作为中间表示而非最终输出，通过 PnP 求解器从 UV 立方体恢复精确相机矩阵（平均重投影误差仅 0.0009 归一化像素，旋转误差 0.46°，Table 5），再将这一姿态用于驱动第二阶段的像素对齐特征提取，形成了“生成-恢复-利用”的闭环。

### 2. 适用边界与局限

CUPID 的适用边界由其设计假设和技术依赖共同界定：

**依赖物体分割掩码**：场景级组合重建（Figure 4, Figure 10）需要预先获得各物体的分割掩码。在真实图像中，掩码边界错误会传播到重建结果，导致物体边缘模糊或几何不完整。目前方法未提供自动掩码生成方案，这在野外图像中构成实际部署瓶颈。

**光照与外观未显式解耦**：CUPID 在生成过程中将纹理、材质和光照统一编码在潜在特征中，未进行显式分离。这意味着对极端光照变化（如强阴影、高光）的泛化能力有限——训练数据主要为合成渲染，光照分布相对均匀。

**多视图融合的朝向不一致**：尽管 CUPID 支持多视图条件重建（Figure 7），但各视图独立恢复的3D物体可能具有不同的规范朝向，简单组合可能导致场景不一致。当前方法依赖3D-3D相似变换进行后对齐，但缺乏端到端的多视图一致性约束。

**训练数据偏差**：模型在合成渲染数据上训练，对真实世界中的复杂纹理、运动模糊、传感器噪声等干扰的鲁棒性尚需验证。Figure 2 展示的野外图像重建结果虽有前景，但缺乏大规模真实场景的定量评估。

**遮挡处理的局限性**：遮挡感知训练使用合成随机掩码（App. A.2），对复杂、非规则遮挡（如部分透明物体、细长遮挡物）的泛化可能存在差距。

### 3. 开放问题

CUPID 的设计打开了若干值得深入探索的方向：

1. **野外图像中的自动物体分割**：如何在没有真实掩码的情况下，自动且准确地分割物体，是实现全自动场景重建的关键前提。可能的路径包括集成开放词汇分割模型或设计端到端的联合分割-重建框架。

2. **多物体场景的联合重建**：当前方法将场景重建分解为“单物体重建+后组合”，缺乏对物体间空间关系和遮挡的全局推理。如何从单张图像同时恢复多个物体及其空间布局，是一个更具挑战性的问题。

3. **规范朝向的一致性**：在多视图融合或场景组合时，不同视图生成的3D物体可能具有不一致的规范朝向。这需要设计更先进的融合方案，或在生成过程中引入朝向一致性约束。

4. **材质、光照与几何的显式解耦**：将外观分解为材质属性（BRDF参数）、光照条件和几何形状，不仅有助于提升真实感，还能支持重光照、材质编辑等下游应用。这需要在生成框架中引入物理渲染先验。

5. **偏离图像中心物体的处理**：当前方法假设物体位于图像中心附近，对大幅偏离中心的物体，UV立方体的生成和PnP求解可能退化。如何扩展模型以处理任意位置的物体，是多视图组合和场景重建的关键需求。

6. **生成多样性与重建精度的权衡**：CUPID 展现了生成多样性（Figure 8），但在需要精确重建的场景（如工业检测）中，如何控制生成过程以平衡多样性与确定性，仍需进一步研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/CUPID_Generative_3D_Reconstruction_via_Joint_Object_and_Pose_Modeling.pdf]]