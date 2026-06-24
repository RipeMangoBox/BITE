---
title: "UniSplat: Unified Spatio-Temporal Fusion via 3D Latent Scaffolds for Dynamic Driving Scene Reconstruction"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/UniSplat_Unified_Spatio_Temporal_Fusion_via_3D_Latent_Scaffolds_for_Dynamic_Driving_Scene_Reconstruction.pdf
openreview_forum_id: Ng2VDbKD4r
aliases:
- UniSplat
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "构造统一的3D潜在支架（3D latent scaffold），并在该支架内直接进行空间和时间融合，从而整合多视图信息并利用历史帧。"
primary_logic: "利用预训练的几何和视觉基础模型构建富含几何和语义上下文的3D潜在支架，在此基础上执行统一的时空融合，并通过双分支动态感知的高斯元解码和静态高斯记忆实现流式动态场景重建和场景补全。"
claims:
- "在空间融合基础上加入时间融合使PSNR再提升0.58dB，SSIM再提升0.04，验证了时空融合的有效性。"
- "双分支解码器相比于仅点分支，PSNR从24.62提升至25.08，LPIPS从0.38降至0.30，表明体素分支补充了缺失区域。"
- "UniSplat在nuScenes上达到25.37 PSNR，超过Omni-Scene 1.10dB，同时在运行时效率上达到4.0 FPS（Omni-Scene 2.5 FPS）。"
- "UniSplat在Waymo多视图重建中PSNR达到29.58（最优尺度对齐），明显优于所有前馈基线方法。"
---

# UniSplat: Unified Spatio-Temporal Fusion via 3D Latent Scaffolds for Dynamic Driving Scene Reconstruction

> [!tip] 核心洞察
> 利用预训练的几何和视觉基础模型构建富含几何和语义上下文的3D潜在支架，在此基础上执行统一的时空融合，并通过双分支动态感知的高斯元解码和静态高斯记忆实现流式动态场景重建和场景补全。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | UniSplat：通过3D潜在支架的统一时空融合用于动态驾驶场景重建 |
| 英文题名 | UniSplat: Unified Spatio-Temporal Fusion via 3D Latent Scaffolds for Dynamic Driving Scene Reconstruction |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Ng2VDbKD4r); [Project](https://chenshi3.github.io/unisplat.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | UniSplat |
| Dataset | nuScenes |

> [!tip] 效果简介
> - nuScenes 上，PSNR 为 25.37，对比 Omni-Scene 24.27，变化 +1.10。
> - nuScenes 上，FPS 为 4.0，对比 Omni-Scene 2.5，变化 +1.5。

## 概述

动态驾驶场景重建面临一个核心瓶颈：车载多相机系统提供的视图稀疏且非重叠，场景中又存在复杂的动态对象，现有方法难以在统一框架内有效融合多视图信息并处理时序动态，导致重建质量受限、无法处理运动物体，也难以实现长期场景补全。

UniSplat 的关键思路是**构造一个统一的 3D 潜在支架（3D latent scaffold）**，并在此支架空间内直接进行空间与时间融合。该支架利用预训练的几何基础模型和视觉基础模型，从多视图图像中构建富含几何与语义上下文的稀疏体素表征。在此基础上，UniSplat 通过稀疏 3D U-Net 实现多视图空间融合，再通过自我运动补偿将历史帧支架与当前帧对齐融合，形成流式时空聚合。融合后的支架经双分支解码器生成动态感知的高斯元：点分支保留精细几何细节，体素分支补充覆盖缺失区域；同时通过动态评分过滤，将静态高斯元累积到持久记忆中，实现流式场景补全。

实验表明，UniSplat 在 Waymo 和 nuScenes 两个主流基准上均达到最优性能。在 nuScenes 上，UniSplat 以 25.37 PSNR 超越此前最优方法 Omni-Scene 达 1.10 dB，同时运行效率达到 4.0 FPS（Omni-Scene 为 2.5 FPS）。消融实验进一步验证了各模块的贡献：加入时间融合使 PSNR 额外提升 0.58 dB、SSIM 提升 0.04；双分支解码器相比仅点分支，PSNR 从 24.62 提升至 25.08，LPIPS 从 0.38 降至 0.30。

方法仍存在一定局限：当行人等动态对象被误分类为静态时，会在渲染序列中产生幽灵伪影；玻璃表面的低高斯不透明度可能导致动态掩码与 RGB 内容的感知不对齐。

## 背景与动机

自动驾驶系统依赖车载多相机传感器感知周围环境，而高质量的场景重建与新视图合成是实现安全规划与决策的基础能力。近年来，3D Gaussian Splatting（3DGS）因其显式表征和实时渲染能力，在该领域展现出巨大潜力。然而，将3DGS应用于动态驾驶场景仍面临两个核心瓶颈：

**多视图融合的稀疏性与非重叠性。** 车载相机通常具有有限的视场重叠区域，且各相机朝向差异显著。现有前馈方法（如PixelSplat、MVSplat、DepthSplat）主要针对物体中心或前向视图场景设计，在驾驶场景的多相机设置下难以有效整合跨视图信息。Omni-Scene虽通过Triplane Transformer在图像域进行跨注意力融合，但这种2D域的融合方式缺乏显式的3D空间一致性约束，导致重建几何不完整、跨相机缝隙明显。

**动态对象的处理与长期场景补全。** 驾驶场景中充斥着运动车辆、行人等动态实体。现有方法（如EvolSplat、DriveRecon）要么仅处理静态场景，要么缺乏有效的时序建模机制。直接将多帧高斯元简单聚合会导致动态对象产生“幽灵”伪影——同一物体在多个历史位置留下残影。同时，由于传感器覆盖范围有限，单帧观测无法补全被遮挡或超出视野的场景区域，这要求方法具备跨帧积累静态场景信息的能力。

上述瓶颈的根本原因在于：现有方法缺乏一个统一的表征空间，能够同时承载多视图空间融合与时序信息整合。UniSplat的核心动机正是构建这样一个**统一的3D潜在支架（3D Latent Scaffold）**——利用预训练的几何与视觉基础模型生成富含度量尺度几何和语义上下文的稀疏体素表征，并在该支架内直接执行空间与时间的统一融合。基于此支架，通过双分支解码器生成动态感知的高斯元，并结合动态过滤的记忆机制实现流式场景补全，从而系统性地解决多视图融合、动态建模和场景补全三个相互耦合的挑战。

## 核心创新

UniSplat 的核心创新在于构造了一个**统一的3D潜在支架（3D latent scaffold）**，将原本在图像域执行的跨视图融合与时间聚合迁移到该支架空间内完成，从而更有效地处理动态驾驶场景中稀疏、非重叠的多相机视图和复杂的场景动态。这一设计思路体现在以下四个关键改进上。

### 1. 3D潜在支架构建：从图像域到3D空间的表示迁移

现有方法（如 Omni-Scene）依赖 Triplane Transformer 在图像域进行跨视图交叉注意力（cross-attention）融合，这种2D/2.5D的融合方式难以充分建模驾驶场景的3D几何一致性。UniSplat 转而利用预训练的几何基础模型（如 MoGe-2 或 π³）从多视图图像中生成度量尺度的点云，并通过逐相机尺度预测（Eq. 2）校正尺度一致性：

$$\gamma = \mathrm{MLP}(\operatorname{AvgPool}(\mathbf{F}_t^{\mathrm{geo}}, \{H, W\})) \in \mathbb{R}^{N_{\mathrm{cam}}}$$

随后将点云组织为稀疏体素，以体素内点坐标均值作为粗几何特征（Eq. 3），并结合语义特征形成具有 $C_s$ 维特征的3D支架 $\mathbf{S}_t$（Eq. 4）。这一支架天然携带了场景的几何和语义上下文，为后续融合提供了统一的3D操作空间。

### 2. 统一时空融合：在支架空间内同时处理空间与时间维度

这是 UniSplat 最关键的 changed slot。基线方法 Omni-Scene 仅支持单帧重建，缺乏时间融合能力。UniSplat 在3D支架空间内实现了**空间融合**与**时间融合**的级联：

- **空间融合**（Eq. 5）：通过稀疏3D U-Net $\phi$ 在支架空间内融合多视图特征，增强空间一致性。消融实验（Table 4）表明，仅加入空间融合即可使 PSNR 从 24.14 提升至 24.50（+0.36 dB），SSIM 从 0.68 提升至 0.70。
- **时间融合**（Eq. 6）：将前一帧的融合支架通过自我运动补偿 $\operatorname{Warp}(\mathbf{S}_{t-1}^{\mathrm{fused}}, T_{t-1}^t)$ 后，与当前空间支架进行稀疏张量加法：

$$\mathbf{S}_t^{\mathrm{fused}} = \mathbf{S}_t^{\mathrm{spa}} \oplus \operatorname{Warp}(\mathbf{S}_{t-1}^{\mathrm{fused}}, T_{t-1}^t)$$

在空间融合基础上加入时间融合后，PSNR 进一步提升至 25.08（+0.58 dB），SSIM 提升至 0.74（+0.04），验证了时空融合的显著增益。

### 3. 双分支动态感知高斯解码器：点锚定精化与体素生成互补

传统方法（如 PixelSplat、MVSplat）仅从像素对齐特征预测高斯元，难以覆盖无直接观测的区域。UniSplat 设计了**双分支解码器**：

- **点分支**：从度量尺度点云的锚点中检索3D支架特征（Eq. 7），与2D特征拼接后经 MLP 预测高斯参数（Eq. 8），保留精细几何细节。
- **体素分支**：从体素中心生成 $g=4$ 个高斯元，补充点分支覆盖不足的缺失区域。

消融实验（Table 5）显示，双分支解码器相比仅使用点分支，PSNR 从 24.62 提升至 25.08，LPIPS 从 0.38 降至 0.30，表明体素分支有效补充了缺失区域的覆盖。此外，每个高斯元还包含一个可学习的**动态评分 $d_i$**，为后续动态过滤提供基础。

### 4. 动态感知记忆与流式场景补全

UniSplat 通过动态评分机制实现了**流式场景补全**——这是基线方法不具备的能力。具体而言，仅将动态评分低于阈值 $\tau_d = 0.7$ 的静态高斯元累积到持久记忆中（Eq. 10）：

$$\mathcal{M}_t = \mathcal{M}_{t-1}' \cup \{ G_i \in \mathcal{G}_t \mid d_i < \tau_d \}$$

该记忆随时间逐步补全因传感器覆盖有限而未观测到的区域，同时避免动态对象（如移动车辆）产生幽灵伪影（ghosting artifacts）。动态概率的渲染监督通过可微渲染实现（Eq. 12），Ground-truth 动态掩码则由 3D 边界框跟踪投影结合 SAM2 生成。

### 创新点总结

| 改进维度 | 基线方法 | UniSplat |
|---------|---------|----------|
| 空间融合 | 图像域交叉注意力（Omni-Scene） | 3D支架空间稀疏3D U-Net融合 |
| 时间融合 | 无（仅单帧） | 支架扭曲与稀疏张量加法 + 流式记忆 |
| 高斯解码 | 像素对齐 + 体素锚定 | 双分支：点锚定精化 + 体素生成（$g=4$） |
| 动态建模 | 无（静态重建） | 动态感知高斯 + 动态记忆过滤（$\tau_d=0.7$） |

这些创新共同使 UniSplat 在 nuScenes 上达到 25.37 PSNR（超 Omni-Scene 1.10 dB），同时以 4.0 FPS 的运行时效率优于 Omni-Scene 的 2.5 FPS（Table 7）。

## 整体框架

![[assets/figures/papers/iclr26_0012_Ng2VDbKD4r_UniSplat_Unified_Spatio-Temporal_Fusion_via_3D_L/figures/001_Figure_1.jpg]]
*Figure 1: Overview of UniSplat. Given multi-camera images from vehicle-mounted cameras, UniSplat leverages foundation models to construct geometry-semantic aware 3D latent scaffolds, where unified spatio-temporal fusion is performed. From this scaffold, a dual-branch decoder generates dynamic-aware Gaussian primitives using both point anchors and voxel centers, with dynamic filtering maintaining a persistent memory of static scene content. The red boxes highlight a dynamic car that is filtered out in our memory module (best viewed when zoomed in)*

UniSplat 遵循一个三阶段流水线，其核心瓶颈在于如何将稀疏、非重叠的多相机视图与复杂的场景动态统一到一个可融合的表示空间中。为解决这一问题，UniSplat 构造了一个**3D潜在支架**（3D latent scaffold）作为统一的中间表示，并在该支架内直接执行空间与时间融合，最后通过双分支解码器生成动态感知的高斯元。

### 流水线概览

整个框架的输入是多相机图像序列，输出是动态感知的3D高斯原语及其渲染视图，同时维护一个静态高斯记忆以完成流式场景补全。三个核心阶段如下：

1. **3D支架构建**：利用预训练的几何基础模型（如π³或MoGe-2）从多视图图像中生成度量尺度的点云，并通过逐相机尺度预测校正其度量一致性。点云被体素化为稀疏体素，每个体素以内部点坐标均值为初始几何特征，再注入语义特征形成几何-语义感知的3D潜在支架 $\mathbf{S}_t$。
2. **统一时空融合**：在支架空间内，首先通过稀疏3D U-Net执行空间融合，增强多视图间的空间一致性；然后将前一帧的融合支架经自我运动补偿后与当前空间支架进行稀疏张量加法，实现时间融合。
3. **双分支高斯解码与动态记忆**：从融合支架中，点锚定分支在度量尺度点云位置检索3D特征并预测精细高斯元，体素分支从每个体素中心生成4个补充高斯元。每个高斯元携带可学习的动态评分 $d_i$，评分低于阈值 $\tau_d=0.7$ 的静态高斯元被累积到持久记忆中，实现跨帧场景补全。

### 模块关系与数据流

各模块间的数据依赖关系可概括为以下因果链：

- **几何基础模型** → 度量点云 → **尺度校正**（Eq. 2: $\gamma = \mathrm{MLP}(\operatorname{AvgPool}(\mathbf{F}_t^{\mathrm{geo}}))$）→ 体素化 → 初始支架 $\mathbf{S}_t$（Eq. 4）
- $\mathbf{S}_t$ → **空间融合**（Eq. 5: $\mathbf{S}_t^{\mathrm{spa}} = \phi(\mathbf{S}_t)$）→ 空间支架
- 空间支架 + 前一帧融合支架 → **时间融合**（Eq. 6: $\mathbf{S}_t^{\mathrm{fused}} = \mathbf{S}_t^{\mathrm{spa}} \oplus \operatorname{Warp}(\mathbf{S}_{t-1}^{\mathrm{fused}}, T_{t-1}^t)$）→ 融合支架
- 融合支架 → **双分支解码器**：点分支检索3D特征（Eq. 7），拼接2D特征后经MLP预测高斯参数（Eq. 8: $\{ (\Delta \pmb{\mu}_i, \alpha_i, \pmb{\Sigma}_i, \mathbf{c}_i, d_i) \} = \mathrm{MLP}([f_{t,i}^{3\mathrm{d}}, f_{t,i}^{2\mathrm{d}}])$）；体素分支从体素中心生成补充高斯元
- 高斯动态评分 $d_i$ → **动态过滤**（Eq. 10: $\mathcal{M}_t = \mathcal{M}_{t-1}' \cup \{ G_i \in \mathcal{G}_t \mid d_i < \tau_d \}$）→ 静态记忆累积 → 场景补全渲染

### 关键设计决策

- **为什么在支架空间融合而非图像空间？** 稀疏3D支架天然对齐了多视图的几何结构，避免了图像域跨注意力（如Omni-Scene的Triplane Transformer）带来的计算开销和几何不一致问题。消融实验证实，仅空间融合就使PSNR从24.14提升至24.50（+0.36 dB），加入时间融合后再提升至25.08（+0.58 dB）（Table 4）。
- **为什么需要双分支解码器？** 点分支保留精细几何细节，但在相机旋转等视角变化下会出现覆盖空洞；体素分支以规则体素中心生成高斯元，补充缺失区域。消融显示，双分支相比仅点分支将PSNR从24.62提升至25.08，LPIPS从0.38降至0.30（Table 5）。
- **动态记忆的作用**：通过动态评分过滤，仅静态高斯元进入持久记忆，避免了动态对象（如移动车辆）在时间累积中产生鬼影伪影（Figure 3对比了有无动态过滤的场景补全结果）。

### 输入输出规范

- **输入**：$N_{\mathrm{cam}}$ 个车载相机的同步图像帧，以及帧间自我运动 $T_{t-1}^t$。
- **输出**：当前帧的高斯原语集 $\mathcal{G}_t$（含位置偏移、不透明度、协方差、颜色、动态评分），以及累积的静态记忆 $\mathcal{M}_t$ 的渲染视图。
- **训练监督**：复合损失函数（Eq. 11）包含输入视图的重建损失（MSE + LPIPS）、动态分割损失、尺度损失，以及仅对有效像素的新视图MSE损失。动态真值掩码通过3D边界框跟踪投影结合SAM2生成。

## 核心模块与公式推导

UniSplat 的核心管道由三个关键模块构成：3D 潜在支架构建、统一时空融合、以及双分支动态感知高斯解码。以下逐一展开各模块的设计逻辑与关键公式。

### 3D 潜在支架构建

该模块的目标是从多视图图像中构建一个富含几何与语义上下文的统一3D表示。具体流程为：利用预训练的几何基础模型从各相机视图生成度量尺度的点云，再通过语义基础模型提取逐像素语义特征。由于不同相机的深度预测可能存在尺度不一致，UniSplat 通过一个轻量 MLP 从池化后的几何特征中预测逐相机尺度因子 $\gamma$，以校正点云的度量尺度：

$$\gamma = \mathrm{MLP}(\operatorname{AvgPool}(\mathbf{F}_t^{\mathrm{geo}}, \{H, W\})) \in \mathbb{R}^{N_{\mathrm{cam}}}$$

其中 $\mathbf{F}_t^{\mathrm{geo}}$ 为几何基础模型输出的特征图，$N_{\mathrm{cam}}$ 为相机数量。校正后的点云被体素化为稀疏体素网格，每个体素的初始粗几何特征定义为其内部点坐标的均值：

$$\mathbf{v}_i^{\mathrm{init}} = \frac{\sum_{j \in \mathcal{T}_i} \mathbf{P}_{t,j}}{\sum_{j \in \mathcal{T}_i} 1}$$

其中 $\mathcal{T}_i$ 为落入第 $i$ 个体素内的点索引集合，$\mathbf{P}_{t,j}$ 为点坐标。语义特征则通过点-体素对应关系聚合到体素中，与几何特征拼接后形成最终的3D支架。支架被形式化定义为一组具有 $C_s$ 维特征和3D中心的体素集合：

$$\mathbf{S}_t = \{(\mathbf{v}_i \in \mathbb{R}^{C_s}, \mathbf{p}_i \in \mathbb{R}^3)\}_{i=1}^{N_v}$$

### 统一时空融合

支架构建完成后，UniSplat 在支架空间内直接执行空间融合与时间融合，而非在图像域进行交叉注意力（如 Omni-Scene 的 Triplane Transformer）。空间融合通过一个稀疏3D U-Net（最大下采样8×）在支架空间内融合多视图上下文，增强空间一致性：

$$\mathbf{S}_t^{\mathrm{spa}} = \phi(\mathbf{S}_t)$$

时间融合则将前一帧已融合的支架通过自我运动补偿 $T_{t-1}^t$ 扭曲到当前帧坐标系，与当前空间支架进行稀疏张量加法，再经一个轻量稀疏卷积网络（最大下采样2×）细化：

$$\mathbf{S}_t^{\mathrm{fused}} = \mathbf{S}_t^{\mathrm{spa}} \oplus \operatorname{Warp}(\mathbf{S}_{t-1}^{\mathrm{fused}}, T_{t-1}^t)$$

这种在潜在空间内的统一融合机制是 UniSplat 的核心创新——它避开了图像域融合对重叠区域的依赖，同时隐式学习根据几何一致性聚合多帧特征，抑制动态对象的过时证据。

### 双分支动态感知高斯解码

从融合支架解码高斯元时，UniSplat 采用双分支策略以兼顾精细几何与缺失区域覆盖。

**点分支**：以度量尺度的点云为锚点，从融合支架中检索对应体素的3D特征。给定点 $\mathbf{P}_{t,i}$，其3D特征通过坐标索引检索：

$$f_{t,i}^{3\mathrm{d}} = \mathrm{Retrieve}\left(\mathbf{S}_t^{\mathrm{fused}}, \left\lfloor \frac{\mathbf{P}_{t,i} - \mathbf{p}_{\mathrm{min}}}{\epsilon} \right\rfloor \right)$$

其中 $\mathbf{p}_{\mathrm{min}}$ 为支架边界最小值，$\epsilon$ 为体素尺寸。将检索到的3D特征与对应像素的2D图像特征 $f_{t,i}^{2\mathrm{d}}$ 拼接后，通过 MLP 预测高斯元参数，包括位置偏移 $\Delta \pmb{\mu}_i$、不透明度 $\alpha_i$、协方差 $\pmb{\Sigma}_i$、颜色 $\mathbf{c}_i$，以及动态评分 $d_i$：

$$\{ (\Delta \pmb{\mu}_i, \alpha_i, \pmb{\Sigma}_i, \mathbf{c}_i, d_i) \} = \mathrm{MLP}([f_{t,i}^{3\mathrm{d}}, f_{t,i}^{2\mathrm{d}}])$$

**体素分支**：从每个非空体素中心生成 $g=4$ 个高斯元，补充点分支覆盖不到的区域（如远距离或遮挡区域）。最终高斯元集合为两分支的并集：$\mathcal{G}_t = \mathcal{G}_t^{\mathrm{point}} \cup \mathcal{G}_t^{\mathrm{voxel}}$。

**动态感知记忆**：利用预测的动态评分 $d_i$ 进行动态过滤。仅保留 $d_i < \tau_d$（$\tau_d=0.7$）的静态高斯元，并随时间累积到持久记忆中：

$$\mathcal{M}_t = \mathcal{M}_{t-1}' \cup \{ G_i \in \mathcal{G}_t \mid d_i < \tau_d \}$$

其中 $\mathcal{M}_{t-1}'$ 为前一帧记忆经自我运动补偿后的结果。这一机制实现了流式场景补全——逐步填补因传感器覆盖有限而缺失的区域，同时避免动态对象产生鬼影伪影。

**动态概率渲染**：为监督动态评分的学习，UniSplat 通过可微渲染将高斯动态评分渲染为逐像素的动态概率图：

$$D = \sum_{i \in \mathcal{N}} d_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j)$$

该动态概率图与由3D边界框追踪结合 SAM2 生成的伪真值动态掩码进行监督，使模型学会区分静态与动态场景内容。

## 实验与分析

### 主要结果

UniSplat 在 Waymo Open 和 nuScenes 两个主流驾驶场景数据集上均取得了最优或次优的重建与新视图合成性能。

在 Waymo 数据集上（Table 1），UniSplat 在前向三视图重建中达到 28.93 PSNR / 0.86 SSIM / 0.18 LPIPS，新视图合成达到 27.34 PSNR；在全六视图设置下（† 表示最优尺度对齐），PSNR 进一步提升至 29.58，显著优于所有前馈基线方法（EvolSplat、DriveRecon、MVSplat、DepthSplat、PixelSplat）。定性对比（Figure 2）显示，UniSplat 生成的几何结构比现有方法更精细、更一致，基线方法在红框标注区域存在明显伪影。

![[assets/figures/papers/iclr26_0012_Ng2VDbKD4r_UniSplat_Unified_Spatio-Temporal_Fusion_via_3D_L/figures/002_Table_1.jpg]]
*Table 1: Quantitative results on the Waymo Dataset. The best results are marked in bold and underlined entries indicate second-place performance. ∗: Evaluation conducted on front 3 views only. †: Results obtained using optimal scale alignment*

在 nuScenes 数据集上（Table 2），UniSplat 达到 25.37 PSNR / 0.765 SSIM / 0.246 LPIPS，PSNR 超越此前最优的 Omni-Scene 达 1.10 dB，SSIM 同样最优；LPIPS 略逊于 Omni-Scene（0.246 vs. 0.237）。与 Omni-Scene 的定性对比（Figure 4）表明，UniSplat 在新视图合成中产生的伪影更少。

![[assets/figures/papers/iclr26_0012_Ng2VDbKD4r_UniSplat_Unified_Spatio-Temporal_Fusion_via_3D_L/figures/003_Table_2.jpg]]
*Table 2: Quantitative results on the nuScenes Dataset. We highlight best results in bold and secondplace results with underlines. ∗: reported by Wei et al. (2025)*

效率方面（Table 7），UniSplat 在 nuScenes 上达到 4.0 FPS，显著快于 Omni-Scene 的 2.5 FPS，同时参数量为 91.0M（Omni-Scene 81.7M），显存占用 8.30 GB（Omni-Scene 8.22 GB）。需要指出，效率对比排除了几何基础模型的计算成本，以保证与 Omni-Scene 的公平性——Omni-Scene 的单目深度估计成本同样已被预先计算并排除。

![[assets/figures/papers/iclr26_0012_Ng2VDbKD4r_UniSplat_Unified_Spatio-Temporal_Fusion_via_3D_L/figures/012_Table_7.jpg]]
*Table 7: Efficiency comparison on the nuScenes dataset*

### 消融实验

消融实验系统性地验证了 UniSplat 各核心组件的贡献。

**特征组成**（Table 3）：同时使用几何特征（Geo）与语义特征（Sem）达到最优性能（PSNR 25.08 / SSIM 0.74 / LPIPS 0.30）。移除语义特征后 LPIPS 从 0.30 增至 0.35（+0.05），表明语义信息对感知质量有显著贡献。单独使用语义特征在 PSNR 和 LPIPS 上略优于单独使用几何特征。

**时空融合**（Table 4）：基线（无时空融合）PSNR 为 24.14。仅加入空间融合（sparse 3D U-Net）使 PSNR 提升至 24.50（+0.36 dB），SSIM 从 0.68 提升至 0.70。在空间融合基础上加入时间融合（warping + 稀疏张量加法）使 PSNR 进一步提升至 25.08（+0.58 dB），SSIM 提升至 0.74（+0.04）。这一组消融直接验证了统一时空融合的核心有效性——时间融合带来的增益（0.58 dB）超过空间融合单独带来的增益（0.36 dB）。

![[assets/figures/papers/iclr26_0012_Ng2VDbKD4r_UniSplat_Unified_Spatio-Temporal_Fusion_via_3D_L/figures/007_Table_4.jpg]]

**双分支解码器**（Table 5）：仅使用点分支（point-anchored）时 PSNR 为 24.62，LPIPS 为 0.38。加入体素分支（voxel-based，每体素生成 4 个高斯元）后 PSNR 提升至 25.08，LPIPS 降至 0.30。定性可视化（Figure 7）揭示了原因：点分支在相机旋转等视角变化下会产生覆盖空洞（红框标注），而体素分支通过连续的体积表示补充了这些缺失区域，双分支结合后既保留了精细几何细节，又维持了稳健的结构完整性。

![[assets/figures/papers/iclr26_0012_Ng2VDbKD4r_UniSplat_Unified_Spatio-Temporal_Fusion_via_3D_L/figures/008_Table_5.jpg]]
*Table 5: Ablation study on the two branches of our Gaussian decoder*

**几何基础模型选择**（Table 6）：π³ 模型在 PSNR 上略优于 MoGe-2（25.08 vs. 24.98），SSIM 持平（0.74），LPIPS 略差（0.30 vs. 0.29）。两者差异较小，表明 UniSplat 框架对几何基础模型的选择具有一定鲁棒性。

### 场景补全与动态处理

UniSplat 通过动态感知记忆模块实现流式场景补全。Figure 3 展示了关键对比：无动态过滤时，累积多帧会导致动态车辆产生幽灵伪影（红框标注）；启用动态感知高斯元（动态阈值 $\tau_d = 0.7$）后，静态高斯元被正确筛选并累积到记忆 $\mathcal{M}_t$ 中，有效补全了传感器覆盖范围外的区域，同时避免了动态伪影。Figure 6 进一步验证了潜在支架层面的动态处理能力——移动车辆在两个时间戳（T=0s 和 T=1.3s）的体素渲染结果均无重影或时序不一致。

### 失败模式与局限

尽管整体性能优越，UniSplat 存在以下已知局限：

1. **动态误分类**：当行人等动态对象被误分类为静态时，会在渲染序列中产生幽灵伪影（见 Figure 5 失败案例）。这源于动态评分 $d_i$ 的预测误差，当 $d_i$ 未能超过阈值 $\tau_d$ 时，动态高斯元被错误地累积到静态记忆中。

2. **透明表面问题**：玻璃表面的低高斯不透明度可能导致动态掩码与 RGB 内容在感知上不对齐（补充视频 1:03 处观察到）。这暴露了当前动态分割机制在处理半透明材质时的根本性缺陷——不透明度 $\alpha_i$ 与动态评分 $d_i$ 在透明区域缺乏有效耦合。

上述失败模式指向两个开放问题：如何改进动态分割以正确处理透明表面上的动态掩码对齐，以及能否通过引入运动先验或光流进一步减少动态误分类。

## 方法谱系与知识库定位

### 与前馈多视图重建方法的继承与超越

UniSplat 处于前馈式（feed-forward）3D 高斯溅射重建的方法谱系中，其直接技术祖先可追溯至 PixelSplat、MVSplat 和 DepthSplat 等基于代价体或深度特征的多视图重建方法。这些方法的核心瓶颈在于：它们依赖密集的 2D-3D 对应关系，在稀疏、非重叠的驾驶场景多相机设置下，对应关系质量急剧下降，导致重建完整性差。UniSplat 的关键突破在于**将融合空间从 2D 图像域迁移至 3D 潜在支架空间**——通过预训练几何基础模型（如 MoGe-2 或 π³）构建度量尺度的稀疏点云，并组织为富含几何与语义上下文的稀疏体素支架，使得多视图信息能够在统一的 3D 坐标系内直接融合，绕开了 2D 对应匹配的脆弱性。

与同期工作 Omni-Scene 的对比最能体现这一设计差异。Omni-Scene 采用 Triplane Transformer 在图像域执行跨注意力融合，其空间融合受限于 2D 特征的投影质量；UniSplat 则使用稀疏 3D U-Net 在支架空间内直接融合，实现了更细粒度的空间一致性。定量证据表明，在 nuScenes 上 UniSplat 的 PSNR 达到 25.37 dB，超过 Omni-Scene 1.10 dB（Table 2），同时推理效率达到 4.0 FPS，优于 Omni-Scene 的 2.5 FPS（Table 7）。值得注意的是，Omni-Scene 渲染阶段占推理时间的 60%，是其效率瓶颈，而 UniSplat 通过稀疏体素操作和双分支解码有效规避了这一问题。

### 动态建模的独特贡献

在方法谱系中，UniSplat 最突出的增量贡献在于**流式动态场景处理**。EvolSplat 虽支持多帧重建，但其动态建模能力有限；Omni-Scene 则完全面向静态场景。UniSplat 引入两个相互配合的机制：(1) 时空支架融合通过自我运动补偿扭曲前一帧支架并与当前空间支架进行稀疏张量加法（Eq. 6），使模型隐式学习按几何一致性聚合多帧特征，自然抑制动态对象的过时证据；(2) 动态感知高斯元为每个高斯基元预测动态评分 $d_i$，并通过阈值 $\tau_d = 0.7$ 过滤动态高斯，仅将静态高斯累积到持久记忆 $\mathcal{M}_t$ 中（Eq. 10），实现流式场景补全。

消融实验清晰验证了这两个机制的因果效应：在空间融合基础上加入时间融合使 PSNR 再提升 0.58 dB、SSIM 再提升 0.04（Table 4）；双分支解码器相比仅点分支，PSNR 从 24.62 提升至 25.08，LPIPS 从 0.38 降至 0.30，表明体素分支有效补充了点分支在缺失区域的覆盖不足（Table 5）。

### 适用边界与已知局限

UniSplat 的性能依赖于几个关键前提：

1. **几何基础模型的质量**：支架构建依赖预训练几何模型输出的度量尺度点云。Table 6 显示 π³ 在 PSNR 上略优于 MoGe-2（25.08 vs 24.98），SSIM 持平，表明模型选择对最终性能有可测量的影响。在几何模型失效的场景（如极端低纹理区域），支架质量会退化，进而影响下游重建。

2. **动态分割的准确性**：动态感知机制依赖 SAM2 生成的伪真值动态掩码进行监督。当行人等动态对象被误分类为静态时，会在渲染序列中产生幽灵伪影（Figure 5 失败案例）。更微妙的是，玻璃表面的低高斯不透明度可能导致动态掩码与 RGB 内容的感知不对齐（补充视频 1:03 处观察到），这表明基于不透明度的动态渲染（Eq. 12）在透明表面上存在根本性局限。

3. **传感器覆盖范围**：虽然 UniSplat 的静态记忆机制能够补全跨相机间隙和传感器盲区，但其补全能力受限于历史帧中已观测到的区域。对于从未被任何相机覆盖的区域，模型无法生成可信内容。

### 开放问题

当前方法的局限指向若干值得进一步探索的方向：

- **动态掩码对齐**：如何改进动态分割以正确处理透明表面上的掩码对齐？可能的路径包括引入物理感知的渲染约束，或在训练中显式建模透明材质的不确定性。
- **运动先验的引入**：能否通过引入光流或场景流等运动先验进一步减少动态误分类？当前方法完全依赖外观和几何一致性来隐式学习动态抑制，显式运动线索可能提升对缓慢移动或远距离动态对象的判别能力。
- **支架分辨率的可扩展性**：当前稀疏体素支架的分辨率受限于内存和计算约束（空间融合 U-Net 最大下采样 8×，时间融合 2×）。在更大规模场景或更长序列中，如何在不显著增加计算成本的前提下提升支架容量，仍是一个工程与算法双重挑战。

## 原文 PDF

![[paperPDFs/ICLR_2026/UniSplat_Unified_Spatio_Temporal_Fusion_via_3D_Latent_Scaffolds_for_Dynamic_Driving_Scene_Reconstruction.pdf]]
