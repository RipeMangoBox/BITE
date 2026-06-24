---
title: "ReconViaGen: Towards Accurate Multi-view 3D Object Reconstruction via Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ReconViaGen_Towards_Accurate_Multi_view_3D_Object_Reconstruction_via_Generation_bd913d15b45e.pdf
project_link: "https://jiahao620.github.io/reconviagen"
code_link: null
aliases:
- ReconViaGen
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将多视图立体重建先验（VGGT提供的全局与局部3D感知特征）融入基于扩散的生成框架（TRELLIS），通过重建感知条件约束生成过程，并引入渲染感知速度补偿机制实现像素级对齐。
primary_logic: 通过微调VGGT提取富含相机姿态、深度和点图信息的图像特征，将其作为全局几何条件和局部逐视图外观条件注入生成模型的去噪过程，从而使生成模型在保证完整性的同时，严格遵从输入视图的几何与纹理信息，显著提升了多视图三维重建的精确度和一致性。
claims:
- 在Dora-bench数据集上，ReconViaGen在PSNR、SSIM、LPIPS、倒角距离和F-score上均显著优于现有最佳方法，PSNR达到22.632。
- 在OmniObject3D数据集上同样取得最优结果，PSNR 19.767, SSIM 0.847等，验证了方法的泛化性。
- 消融实验证明，三个核心设计（全局几何条件GGC、逐视图条件PVC、渲染感知速度补偿RVC）对性能均有重要贡献，组合使用取得最佳效果。
- 随着输入视图数量从1增加到8，重建指标持续提升，表明方法能有效利用多视图信息。
---

# ReconViaGen: Towards Accurate Multi-view 3D Object Reconstruction via Generation

> [!tip] 核心洞察
> 通过微调VGGT提取富含相机姿态、深度和点图信息的图像特征，将其作为全局几何条件和局部逐视图外观条件注入生成模型的去噪过程，从而使生成模型在保证完整性的同时，严格遵从输入视图的几何与纹理信息，显著提升了多视图三维重建的精确度和一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReconViaGen：基于生成实现精确多视图三维物体重建 |
| 英文题名 | ReconViaGen: Towards Accurate Multi-view 3D Object Reconstruction via Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=z0QLeooEEf) · [Project](https://jiahao620.github.io/reconviagen) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ReconViaGen |
| Dataset | Dora-bench, OmniObject3D |

> [!tip] 效果简介
> - Dora-bench 上，PSNR, SSIM, LPIPS, CD, F-score 22.632；PSNR, SSIM, LPIPS, CD, F-score 0.911；PSNR, SSIM, LPIPS, CD, F-score 0.090。
> - OmniObject3D 上，PSNR, SSIM, LPIPS, CD, F-score 19.767；PSNR, SSIM, LPIPS, CD, F-score 0.847；PSNR, SSIM, LPIPS, CD, F-score 0.141。

## 概述

从多视图图像重建高保真三维物体是计算机视觉的核心任务，但现有方法面临两难困境：纯重建方法受限于遮挡与稀疏视角，难以生成完整的物体背面或内部结构；基于扩散模型的生成方法虽能补全缺失区域，却因随机推理过程而无法与输入视图保持严格一致，尤其在局部几何与纹理细节上偏差明显。ReconViaGen 针对此瓶颈，提出将多视图立体重建先验与三维扩散生成先验融合于统一框架，在保证形状完整性的同时，实现与输入视图的像素级对齐。

方法的核心机制在于三个互为补充的设计：(1) 微调 VGGT 作为重建先验提取器，从输入多视图图像中获取蕴含相机姿态、深度与点图信息的全局几何特征与逐视图局部外观特征；(2) 通过条件网络将这些特征分别注入生成模型 TRELLIS 的粗结构生成阶段（SS Flow）与精细纹理生成阶段（SLAT Flow），以重建感知条件约束去噪过程；(3) 引入渲染感知速度补偿机制（RVC），在推理阶段利用渲染损失梯度修正去噪轨迹，进一步提升细节一致性。

在 Dora-bench 与 OmniObject3D 数据集上的实验表明，ReconViaGen 在 PSNR、SSIM、LPIPS、倒角距离与 F-score 等指标上均显著超越现有方法，验证了其重建精度与泛化能力。消融实验进一步证实，全局几何条件、逐视图局部条件与 RVC 三者对最终性能均有独立且互补的贡献。

## 背景与动机

从多视图图像重建完整的三维物体是计算机视觉与图形学的核心任务，在虚拟现实、增强现实、机器人操作和数字内容创作等领域具有广泛需求。该任务的核心挑战在于：输入视图通常只能覆盖物体的部分表面，大量区域因遮挡或视角稀疏而不可见，重建算法必须在信息高度不完整的条件下推断出合理的完整几何与纹理。

现有方法可大致归为两条技术路线。**纯重建方法**（如基于多视图立体的神经隐式表示或前馈网络）严格依赖输入视图提供的几何线索进行深度估计与表面融合。这类方法在可见区域能够保持较高的输入一致性，但面对不可见区域时只能产生不完整的重建结果，如图 Figure 1 左侧所示。**基于扩散的生成方法**（如 TRELLIS 等三维原生扩散模型）利用大规模三维数据学习到的强生成先验，可以从任意稀疏视图中“幻想”出完整的物体形状。然而，这类方法的推理过程本质上是随机的——去噪轨迹由随机噪声初始化，缺乏与输入视图之间确定性的像素级约束。这导致生成结果虽然在整体形状上看起来合理，但在局部几何细节和纹理上与输入视图存在明显的不一致（Figure 1 中间）。

上述困境揭示了一个根本性的瓶颈：**重建先验与生成先验各自具备对方所缺乏的关键能力，但二者在现有框架中处于割裂状态。** 重建方法能保证输入一致性却无法补全不可见区域；生成方法能产生完整形状却无法忠实于输入视图。这一观察引出了一个自然的动机——能否将多视图立体重建提供的强几何约束，系统性地融入扩散生成框架的去噪过程，使生成模型在“幻想”完整形状的同时，严格遵从输入视图的几何与纹理信息？

ReconViaGen 正是在这一动机下提出的。该方法的核心洞察在于：现代多视图立体模型（如 VGGT）不仅能输出深度图和点云，其内部特征还编码了丰富的相机姿态、全局三维结构和逐视图外观信息。如果将这些特征作为条件信号注入扩散模型的去噪过程，就有望在保持生成完整性的同时，实现对输入视图的像素级忠实。这一思路将“重建”与“生成”从对立关系转变为互补关系，为多视图三维重建开辟了新的技术路径。

## 核心创新

ReconViaGen 的核心创新在于将**多视图立体重建先验**系统性地注入**基于扩散的生成框架**，从而在保证生成完整性的同时，实现与输入视图高度一致的三维重建。这一设计针对现有方法的根本矛盾——纯重建方法（因遮挡和稀疏视图导致不完整）与纯生成方法（随机推理导致局部几何和纹理不一致）——提供了统一的解决方案。

### 创新一：重建先验驱动的条件注入

传统基于扩散的三维生成方法（如 TRELLIS）仅使用 DINO 等通用视觉特征作为条件，缺乏对多视图几何关系的显式建模。ReconViaGen 将预训练的多视图立体模型 **VGGT** 微调为重建先验提供者，提取蕴含相机姿态、深度和点图信息的图像特征，并转化为两类互补条件：

1. **全局几何条件（Global Geometry Condition, GGC）**：通过条件网络（Condition Net）将 VGGT 的全局特征聚合为固定长度的令牌列表 $T_g$，注入 SS Flow 的交叉注意力层，为粗结构生成提供全局三维形状约束。
2. **逐视图局部条件（Per-View Condition, PVC）**：为每个输入视图生成视图特定的令牌列表 $P_k$，在 SLAT Flow 中通过加权交叉注意力融合各视图信息，引导纹理和几何细节的精细生成。

这种双层级条件设计使生成过程同时受到全局几何一致性和局部外观保真度的约束，从根本上解决了纯生成方法“看起来合理但不忠于输入”的问题。

### 创新二：渲染感知速度补偿（Rendering-aware Velocity Compensation, RVC）

即使引入了重建先验条件，扩散模型的随机去噪过程仍可能导致生成结果与输入视图之间存在像素级偏差。ReconViaGen 提出渲染感知速度补偿机制，在推理阶段的每个去噪步骤中，通过可微分渲染将当前潜在表示投影到输入视角，计算渲染图像与真实输入之间的复合损失：

$$\mathcal{L}_{\mathrm{RVC}}(v_t) = \mathcal{L}_{\mathrm{SSIM}} + \mathcal{L}_{\mathrm{LPIPS}} + \mathcal{L}_{\mathrm{DreamSim}}$$

该损失结合了结构相似性、感知相似性和语义相似性，其梯度用于修正去噪速度：

$$\Delta v_t = \frac{\partial \mathcal{L}}{\partial \hat{x}_0} \frac{\partial \hat{x}_0}{\partial v_t} = -t \frac{\partial \mathcal{L}}{\partial \hat{x}_0}$$

修正后的潜变量更新规则为 $x_{t_{\mathrm{prev}}} = x_t - (t - t_{\mathrm{prev}}) (v + \alpha \cdot \Delta v)$。这一机制在保持生成完整性的前提下，将去噪轨迹拉向与输入视图像素级对齐的方向，是 ReconViaGen 实现高精度重建的关键技术。

### 创新三：重建与生成先验的互补融合范式

ReconViaGen 并非简单地将重建模型和生成模型串联，而是构建了**粗到细的两阶段协同框架**：SS Flow 利用全局几何条件生成稀疏体素结构，SLAT Flow 在此基础上结合逐视图条件生成结构化潜在表示。消融实验（Table 2）证实，三个核心设计——GGC、PVC、RVC——对性能均有显著贡献，组合使用时达到最优效果。随着输入视图数量从 1 增加到 8，重建指标持续提升（Table 3），表明该方法能有效利用多视图信息，边际增益逐渐减小，符合多视图几何的直觉。

## 整体框架

ReconViaGen 的核心设计思想是将**多视图立体重建先验**与**基于扩散的生成先验**融合为一个互补的三维重建流水线。其整体架构采用“粗到细”的两阶段生成范式，并在推理阶段引入像素级对齐机制，具体包含三个关键环节：

1. **重建先验提取**：以预训练的 VGGT 作为重建先验提供者，输入多视图图像后输出富含相机姿态、深度和点图信息的特征表示。VGGT 经过 LoRA 微调以适应物体重建任务，损失函数为：
   $$ \mathcal{L}_{\mathrm{VGGT}}(\theta) = \mathcal{L}_{\mathrm{camera}} + \mathcal{L}_{\mathrm{depth}} + \mathcal{L}_{\mathrm{nmap}} $$
   该阶段为后续生成过程同时提供全局几何条件和逐视图局部外观条件。

2. **条件注入与粗到细生成**：框架构建于 TRELLIS 之上，包含两个级联的生成阶段。
   - **条件网络** 将 VGGT 特征分别聚合为全局几何令牌列表 $T_g$ 和逐视图局部令牌列表 $P_k$。全局条件通过四层交叉注意力块逐步融合：
     $$ T^{i+1} = \mathrm{CrossAttn}(Q(T^i), K(\phi_{\mathrm{vggt}}), V(\phi_{\mathrm{vggt}})), \quad i \in \{0,1,2,3\} $$
     局部条件则为每个输入视图独立生成：
     $$ P_k^{i+1} = \mathrm{CrossAttn}(Q(P_k^i), K(\phi_k^{\mathrm{vggt}}), V(\phi_k^{\mathrm{vggt}})), \quad i \in \{0,1,2,3\}, k \in \{n\}_{n=1}^N $$
   - **SS Flow** 接收全局几何条件 $T_g$，生成稀疏体素结构的粗 3D 形状，奠定物体的整体几何框架。
   - **SLAT Flow** 在粗结构基础上，结合各视图的局部条件 $P_k$ 进行加权融合：
     $$ y_{j+1} = \sum_{k=1}^N \mathrm{CrossAttn}(Q(y_j'), K(P_k), V(P_k)) \cdot w_k, \quad j \in \{m\}_{m=1}^M $$
     从而生成包含纹理和几何细节的结构化潜在表示。

3. **渲染感知速度补偿**：在 SLAT 去噪推理阶段，将当前预测的 SLAT 渲染为多视图图像并与输入图像对比，计算组合损失（SSIM + LPIPS + DreamSim），通过梯度反向传播获得速度补偿项：
   $$ \Delta v_t = \frac{\partial \mathcal{L}}{\partial \hat{x}_0} \frac{\partial \hat{x}_0}{\partial v_t} = -t \frac{\partial \mathcal{L}}{\partial \hat{x}_0} $$
   最终以缩放后的补偿项修正去噪轨迹：
   $$ x_{t_{\mathrm{prev}}} = x_t - (t - t_{\mathrm{prev}}) (v + \alpha \cdot \Delta v) $$
   该机制使生成结果在像素级别与输入视图严格对齐。

整个框架的数据流为：**多视图图像 → VGGT 特征提取 → 条件网络聚合全局/局部令牌 → SS Flow 粗结构生成 → SLAT Flow 精细生成 + RVC 像素对齐 → 最终三维重建结果**。图 2 给出了框架的完整示意图，清晰展示了各模块间的输入输出关系。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_z0QLeooEEf/figures/002_Figure_2.jpg]]
*Figure 2: An overview illustration of the proposed ReconViaGen framework, which integrates strong reconstruction priors with 3D diffusion-based generation priors for accurate reconstruction at both the global and local level*

## 核心模块与公式推导

ReconViaGen 的核心设计在于将多视图立体重建先验系统性地注入扩散生成框架，形成“重建条件约束生成”的互补范式。该方法包含四个关键模块，其因果链路为：**VGGT 重建先验提取 → 条件网络特征聚合 → 粗到细的流匹配生成 → 渲染感知速度补偿**。

### 3.1 重建先验提取与基础框架

ReconViaGen 以 **TRELLIS** 作为生成骨干，利用其整流流（Rectified Flow）Transformer 在结构化潜在空间中执行从噪声到完整形状的去噪生成。为将重建先验融入生成过程，方法微调了预训练的多视图重建器 **VGGT**，使其适配物体级重建任务。

VGGT 微调的损失函数为多任务组合形式：

$$
\mathcal{L}_{\mathrm{VGGT}}(\theta) = \mathcal{L}_{\mathrm{camera}} + \mathcal{L}_{\mathrm{depth}} + \mathcal{L}_{\mathrm{nmap}} \tag{1}
$$

其中 $\mathcal{L}_{\mathrm{camera}}$ 为相机姿态损失，$\mathcal{L}_{\mathrm{depth}}$ 为深度损失，$\mathcal{L}_{\mathrm{nmap}}$ 为点图损失。通过 LoRA 微调 VGGT 的聚合器（aggregator），在保留预训练 3D 几何先验的同时，使其输出富含物体级多视图感知特征 $\phi_{\mathrm{vggt}}$。这些特征隐式编码了相机姿态、深度和点图信息，成为后续生成条件的来源。

生成框架的训练采用条件流匹配损失：

$$
\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{t, x_0, \epsilon} \| \mathbf{v}_{\theta}(x, t) - (\epsilon - x_0) \|_2^2 \tag{2}
$$

其中 $x_0$ 为目标潜在表示，$\epsilon$ 为噪声，$\mathbf{v}_{\theta}(x, t)$ 为时间步 $t$ 时预测的速度场。

### 3.2 条件网络：双层次条件聚合

条件网络（Condition Net）将 VGGT 特征转化为生成框架可消费的两类条件令牌，分别服务于全局结构生成和局部细节生成。

**全局几何条件（Global Geometry Condition, GGC）** 通过四个交叉注意力块将 VGGT 特征 $\phi_{\mathrm{vggt}}$ 逐步融合为固定长度的全局令牌列表 $T_g$：

$$
T^{i+1} = \mathrm{CrossAttn}(Q(T^i), K(\phi_{\mathrm{vggt}}), V(\phi_{\mathrm{vggt}})), \quad i \in \{0,1,2,3\} \tag{3}
$$

其中 $T^0$ 为随机初始化的可学习令牌列表。该过程将多视图的全局几何信息压缩为紧凑表示，用于指导 SS Flow 的粗结构生成。

**逐视图局部条件（Per-View Condition, PVC）** 为每个输入视图 $k$ 生成视图特定的局部令牌列表 $P_k$：

$$
P_k^{i+1} = \mathrm{CrossAttn}(Q(P_k^i), K(\phi_k^{\mathrm{vggt}}), V(\phi_k^{\mathrm{vggt}})), \quad i \in \{0,1,2,3\}, \; k \in \{n\}_{n=1}^N \tag{4}
$$

其中 $\phi_k^{\mathrm{vggt}}$ 为第 $k$ 个视图的 VGGT 特征。这些逐视图令牌保留了各视角的局部外观和几何信息，在 SLAT Flow 阶段用于精细纹理生成。

### 3.3 粗到细生成与速度补偿

生成过程分为两个阶段：**SS Flow** 和 **SLAT Flow**。

**SS Flow** 接收全局几何条件 $T_g$，通过交叉注意力将其融入去噪过程，生成稀疏体素结构的粗 3D 形状。此阶段仅依赖全局条件，确保整体几何结构的完整性和多视图一致性。

**SLAT Flow** 在粗结构基础上生成包含纹理和几何细节的结构化潜在表示（Structured LATent）。其核心创新在于对多视图局部条件的加权融合：

$$
y_{j+1} = \sum_{k=1}^N \mathrm{CrossAttn}(Q(y_j'), K(P_k), V(P_k)) \cdot w_k, \quad j \in \{m\}_{m=1}^M \tag{5}
$$

其中 $y_j'$ 为当前 SLAT 特征，$P_k$ 为第 $k$ 个视图的局部条件令牌，$w_k$ 为视图权重。该加权机制使生成过程能够自适应地关注不同视图的信息，实现多视角一致的精细重建。

**渲染感知速度补偿（Rendering-aware Velocity Compensation, RVC）** 是推理阶段的关键模块，用于修正 SLAT 去噪轨迹以实现像素级输入对齐。其损失函数组合了结构相似性、感知相似性和语义相似性：

$$
\mathcal{L}_{\mathrm{RVC}}(v_t) = \mathcal{L}_{\mathrm{SSIM}} + \mathcal{L}_{\mathrm{LPIPS}} + \mathcal{L}_{\mathrm{DreamSim}}
$$

该损失评估当前潜在表示渲染图像与输入图像之间的差异。速度补偿项由损失对预测目标 $\hat{x}_0$ 的梯度推导：

$$
\Delta v_t = \frac{\partial \mathcal{L}}{\partial \hat{x}_0} \frac{\partial \hat{x}_0}{\partial v_t} = -t \frac{\partial \mathcal{L}}{\partial \hat{x}_0}
$$

最终，带补偿的 SLAT 更新规则为：

$$
x_{t_{\mathrm{prev}}} = x_t - (t - t_{\mathrm{prev}}) (v + \alpha \cdot \Delta v)
$$

其中 $\alpha$ 为补偿强度的缩放系数。这一机制在不改变训练流程的前提下，通过推理时的梯度引导使生成结果严格遵从输入视图的像素级信息，是 ReconViaGen 实现高精度重建的关键设计。

## 实验与分析

### 核心瓶颈与实验动机

现有纯重建方法因遮挡和稀疏视图导致重建不完整；基于扩散的生成方法虽能生成完整形状，但随机推理过程导致与输入视图不一致，尤其在局部几何和纹理细节上。ReconViaGen的实验设计围绕一个核心因果问题展开：将多视图立体重建先验（VGGT提供的全局与局部3D感知特征）融入基于扩散的生成框架后，能否在保证完整性的同时，严格遵从输入视图的几何与纹理信息？定量与定性实验均围绕这一核心洞察进行验证。

### 主实验结果

Table 1展示了在Dora-bench和OmniObject3D两个数据集上的全面对比。ReconViaGen在所有五项指标（PSNR、SSIM、LPIPS、倒角距离CD、F-score）上均取得最优结果。

在Dora-bench数据集上，ReconViaGen的PSNR达到22.632，SSIM为0.911，LPIPS为0.090，CD为0.090，F-score为0.953，全面超越现有最佳方法。在OmniObject3D数据集上同样取得最优结果，PSNR为19.767，SSIM为0.847，LPIPS为0.141，CD为0.059，F-score为0.959，验证了方法的跨数据集泛化能力。

Figure 3的定性比较进一步印证了定量结论：纯重建方法在遮挡区域产生明显空洞，基于生成的方法虽能补全形状但纹理与输入视图存在明显偏差，而ReconViaGen在形状完整性和纹理一致性上均表现优异。

### 消融实验：三个核心设计的贡献

Table 2的消融实验系统验证了三个核心设计模块的独立贡献。从基础变体（a）开始，逐步引入全局几何条件（GGC）、逐视图条件（PVC）和渲染感知速度补偿（RVC），性能持续提升：

- **引入GGC**（变体a→b）：带来显著性能提升，证明全局几何先验对粗结构生成的关键作用。
- **引入PVC**（变体c）：进一步改善重建质量，尤其在PSNR上提升明显，表明逐视图局部条件有效约束了纹理细节的生成。
- **引入RVC**（变体d）：在形状完整性和细节精度上带来额外增益，验证了像素级对齐机制的必要性。

三个模块组合使用取得最佳效果，证明了重建先验与生成先验互补融合的有效性。Figure 5的定性消融对比直观展示了各变体的视觉差异。

### 视图数量敏感性分析

Table 3展示了输入视图数量从1增加到8时重建指标的持续提升趋势。随着视图数量增加，PSNR、SSIM等指标单调上升，LPIPS和CD单调下降，表明方法能有效利用多视图信息。边际增益逐渐减小，暗示存在信息饱和点。Figure 6的定性对比展示了不同视图数量下的重建质量差异。

### 开放场景泛化

Figure 4展示了在开放场景（in-the-wild）样本上的重建结果。值得注意的是，商用3D生成器通常要求正交视角的输入图像，而ReconViaGen可接受任意相机姿态的视图输入并产生鲁棒输出，体现了VGGT提供的相机姿态估计能力带来的实际优势。

### 失败模式与局限

当前实验分析中未明确报告失败模式。以下潜在局限需要人工验证：条件形式（如全局和局部条件的结构设计）对SS Flow和SLAT Flow性能的影响机制尚未展开分析（论文附录提及但未详述）；在极端稀疏视图（如仅1-2个输入）或严重遮挡场景下的性能边界未充分探索；RVC的迭代优化增加了推理计算开销，其效率-精度权衡未量化讨论。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_z0QLeooEEf/figures/003_Table_1.jpg]]
*Table 1: Evaluation on the Dora-bench and OmniObject3D dataset. Best results are in bold*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_z0QLeooEEf/figures/005_Table_2.jpg]]
*Table 2: Quantitative ablation results on the Dora-bench dataset*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_z0QLeooEEf/figures/009_Table_3.jpg]]
*Table 3: Quantitative ablation results of the number of input images on the Dora-bench dataset*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_z0QLeooEEf/figures/001_Figure_1.jpg]]
*Figure 1: In the task of 3D object reconstruction from multi-view images, existing pure reconstruction methods can only produce incomplete results, while generation-based methods can get plausible complete results but with strong inconsistency with input images. Our ReconViaGen integrates 3D reconstruction and diffusion-based generation priors into one framework that leads to accurate reconstructions*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_z0QLeooEEf/figures/004_Figure_3.jpg]]
*Figure 3: Reconstruction result comparisons between our ReconViaGen and other baseline methods on samples from the Dora-bench and OmniObject3D datasets. Zoom in for better visualization*

## 方法谱系与知识库定位

### 1. 方法谱系：重建与生成的交叉路口

ReconViaGen 的核心贡献在于将**多视图立体重建先验**系统性地注入**基于扩散的生成框架**，从而同时解决了纯重建方法的“不完整性”瓶颈与纯生成方法的“输入不一致性”瓶颈。其方法谱系可沿两条主线追溯：

**重建主线（Reconstruction Lineage）**：传统多视图立体匹配（MVS）及后续基于学习的方法（如 MVSNet 系列）受限于可见表面重建，在遮挡区域和稀疏视图下必然产生空洞或不完整网格。VGGT 作为本工作的重建先验提供者，本身代表了从图像中联合估计相机姿态、深度和点图的强先验。ReconViaGen 通过 LoRA 微调将其适配至物体重建场景，使其输出的特征图富含全局三维几何与局部逐视图外观信息——这些信息在纯重建范式中仅用于深度/点图回归，而在本工作中被重新定位为**生成过程的条件信号**。

**生成主线（Generation Lineage）**：以 TRELLIS 为代表的三维扩散/整流流生成模型能够从噪声中采样出完整、多样的三维形状，但其条件机制（原始 TRELLIS 仅使用 DINO 图像特征）缺乏对输入视图的严格几何遵从性，导致生成结果虽然在语义上合理，却在局部几何和纹理上与输入视图存在偏差。ReconViaGen 在 TRELLIS 的 SS Flow（粗结构生成）和 SLAT Flow（精细生成）两个阶段分别注入全局几何条件（GGC）和逐视图条件（PVC），使生成过程从“自由想象”变为“有约束的补全”。

**关键交叉机制**：渲染感知速度补偿（RVC）是连接两条主线的关键设计。它利用可微渲染将生成过程中的中间潜表示投影回图像空间，通过 SSIM、LPIPS 和 DreamSim 组合损失计算与输入视图的差异，并将梯度反传修正去噪速度。这一机制本质上是将**重建中的光度一致性约束**转化为**生成过程中的轨迹引导力**，使得生成模型在保持完整性的同时实现像素级对齐。

### 2. 与现有工作的关系定位

**相对于纯重建方法**：ReconViaGen 不直接与 MVSNet、NeuS 等基于优化或神经隐式表示的方法竞争“可见表面精度”，而是通过生成补全解决遮挡和稀疏视图问题。其优势在输入视图数量较少（如 1-4 张）时尤为显著，因为此时纯重建方法的信息缺失最为严重。

**相对于纯生成方法**：与 Zero-1-to-3、One-2-3-45 等以图像/文本为条件的生成方法相比，ReconViaGen 的差异化在于其条件信号来自重建先验而非语义嵌入，因此对输入视图的几何遵从性更强。与直接使用 TRELLIS 相比，本工作通过 GGC、PVC 和 RVC 三个模块将“生成完整形状”的能力与“忠实于输入”的要求解耦并协同。

**相对于其他重建-生成混合方法**：当前领域内存在若干尝试将生成先验引入重建的工作（如利用扩散先验进行神经渲染优化），但多数采用“生成-后优化”的两阶段分离范式。ReconViaGen 的独特之处在于将重建先验作为生成过程的**内在条件**而非外部约束，使条件注入发生在去噪过程的每个时间步，从而实现了更紧耦合的协同。

### 3. 适用边界与局限

根据论文提供的证据，ReconViaGen 的适用边界可从以下维度界定：

**输入模态边界**：方法设计面向多视图 RGB 图像输入，依赖 VGGT 提供的相机姿态估计能力。对于无纹理表面、强反光或极端光照条件下的输入，VGGT 的姿态估计精度可能下降，进而影响条件特征的质量——这一链条上的脆弱性需要在部署时关注。

**物体类别泛化性**：LoRA 微调使用了 Objaverse 的 390K 三维数据，涵盖大量常见物体类别。在 Dora-bench 和 OmniObject3D 上的跨数据集验证表明方法具有一定泛化性，但对于与训练分布差异极大的物体类别（如高度非刚性、极端细粒度结构），性能边界尚不明确。

**计算开销边界**：RVC 机制在推理时需要对每个 SLAT 去噪步骤进行可微渲染和梯度反传，这引入了额外的计算成本。论文未提供与纯 TRELLIS 推理时间的定量对比，这一效率边界需要在实际部署中评估。

**视图数量边界**：消融实验（Table 3）表明性能随输入视图数量增加而持续提升，但边际增益递减。在 1 视图极端情况下，方法仍需依赖生成先验“猜测”不可见区域，此时的不确定性最高。

### 4. 开放问题

论文附录中提及但未充分展开的一个关键问题是：**全局条件（GGC）和局部条件（PVC）的具体结构形式如何影响 SS Flow 和 SLAT Flow 的性能？** 当前设计中，GGC 通过四个交叉注意力块聚合为固定长度的令牌列表，PVC 则为每个视图生成独立的令牌列表并在 SLAT 中进行加权融合。条件令牌的长度、注意力块的深度、视图间融合权重的计算方式等设计选择对最终重建精度和一致性的影响尚未被系统消融。这一问题的探索可能揭示重建先验与生成先验之间更优的信息传递机制。

此外，RVC 中组合损失（SSIM + LPIPS + DreamSim）的各项权重选择依据、RVC 仅在 SLAT 阶段而非 SS 阶段施加的原因，以及 CFG 强度在不同去噪阶段的动态调整策略，均为值得进一步研究的工程维度。

## 原文 PDF

![[paperPDFs/ICLR_2026/ReconViaGen_Towards_Accurate_Multi_view_3D_Object_Reconstruction_via_Generation_bd913d15b45e.pdf]]