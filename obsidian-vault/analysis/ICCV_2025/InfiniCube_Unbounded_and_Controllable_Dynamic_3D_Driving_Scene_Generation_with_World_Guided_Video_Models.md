---
title: "InfiniCube: Unbounded and Controllable Dynamic 3D Driving Scene Generation with World-Guided Video Models"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/InfiniCube_Unbounded_and_Controllable_Dynamic_3D_Driving_Scene_Generation_with_World_Guided_Video_Models.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/infinicube/
code_link: null
aliases:
- InfiniCube
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过稀疏体素扩散生成无界三维语义世界，从中渲染几何对齐的语义与坐标引导缓冲区，为视频模型提供强 3D 先验，从而克服自回归长视频生成中的累积误差；再通过双分支前馈重建，将体素分支的几何精度与像素分支的动态/中景细节结合，高效升维为可控动态 3DGS 场景。"
primary_logic: "将 3D 几何先验与 2D 视频生成模型的丰富外观能力解耦——用体素世界作为「世界骨架」提供精确的 3D 引导，使视频模型专注于纹理合成，避免几何失真与累积漂移；重建时再融合体素与像素信息，分别处理静态背景与动态物体，实现高质量可扩展的 3D 动态场景生成。"
claims:
- "提出的引导缓冲区设计显著降低了长视频自回归生成中的累积误差，在 FID 指标上优于 Panacea 和 Vista，且经人工评估，对 HD 地图的长期对齐度明显更高（帧 120 时正响应率 84.8% vs 53.4%）。"
- "双分支重建在 Waymo 数据集的新视角合成中取得最佳 PSNR/SSIM/LPIPS，超越 SCube 等现有方法，验证了体素与像素分支结合的有效性。"
- "道路表面条件 (CRoad) 和体素外推策略消融实验证明设计模块对场景一致性具有关键作用。"
- "语义引导缓冲区是维持长视频质量的最关键成分，坐标缓冲区进一步解决运动引起的细节模糊。"
---

# InfiniCube: Unbounded and Controllable Dynamic 3D Driving Scene Generation with World-Guided Video Models

> [!tip] 核心洞察
> 将 3D 几何先验与 2D 视频生成模型的丰富外观能力解耦——用体素世界作为「世界骨架」提供精确的 3D 引导，使视频模型专注于纹理合成，避免几何失真与累积漂移；重建时再融合体素与像素信息，分别处理静态背景与动态物体，实现高质量可扩展的 3D 动态场景生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | InfiniCube：基于世界引导视频模型的无界可控动态 3D 驾驶场景生成 |
| 英文题名 | InfiniCube: Unbounded and Controllable Dynamic 3D Driving Scene Generation with World-Guided Video Models |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2412.03934) · [Project](https://research.nvidia.com/labs/toronto-ai/infinicube/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | InfiniCube |
| Dataset | Waymo Open Dataset (90 test sequences), Waymo Open Dataset (Human Evaluation of HD Map Alignment), Waymo Open Dataset (Novel View Synthesis at T+5), Waymo Open Dataset (Novel View Synthesis at T+10) |

> [!tip] 效果简介
> - Waymo Open Dataset (90 test sequences) 上，FID (lower is better) at 200 frames 为 显著低于基线，100 帧后仍保持高质量，对比 Panacea (FID 快速上升), Vista (FID 快速上升)，变化 ~100 帧后优势明显。
> - Waymo Open Dataset (Human Evaluation of HD Map Alignment) 上，Positive Rate (%) 为 84.6 (frame 40), 83.9 (frame 80), 84.8 (frame 120)，对比 Panacea: 76.8 (frame 40), 54.0 (frame 80), 53.4 (frame 120)，变化 +7.8% ~ +31.4%。
> - Waymo Open Dataset (Novel View Synthesis at T+5) 上，PSNR↑ / SSIM↑ / LPIPS↓ 为 20.80 / 0.73 / 0.42，对比 SCube: 19.90 / 0.72 / 0.47，变化 +0.90 / +0.01 / -0.05。

## 概要

自动驾驶仿真对高保真、长距离、可模拟且可控的 3D 动态场景生成提出了严苛需求。现有方法在此目标上存在结构性分裂：大规模 3D 场景生成方法（如 **InfiniCity**、**WoVoGen**）多局限于室内或静态场景，缺乏对布局、外观和动态行为的灵活控制；而视频生成模型（如 **Vista**、**Panacea**）虽能产生丰富的纹理细节，却受限于帧数少、3D 一致性差，无法直接支撑物理仿真。两类方法的根本瓶颈在于——前者缺少高保真外观建模能力，后者缺少稳定的 3D 几何先验，难以同时满足自动驾驶仿真对“真实感几何 + 长程外观 + 可控动态”的三重约束。

InfiniCube 的核心洞察是将 3D 几何先验与 2D 外观生成解耦：**用稀疏体素扩散模型构建无界三维语义世界作为“世界骨架”，从中渲染像素对齐的几何引导缓冲区，为视频模型注入强 3D 先验，从而克服自回归长视频生成中的累积误差；再通过双分支前馈重建，将体素分支的几何精度与像素分支的动态/中景细节融合，高效升维为可控的动态 3DGS 场景。** 这一设计使得 2D 视频模型可以专注于纹理合成，而几何一致性和长程稳定性由 3D 世界骨架保证。

在 Waymo Open Dataset 上的实验验证了该范式的有效性：

- **长视频质量**：在 200 帧自回归生成中，InfiniCube 的 FID 显著优于 Panacea 和 Vista，100 帧后优势尤为明显；人工评估显示，第 120 帧时对 HD 地图的对齐正响应率达 84.8%，远超 Panacea 的 53.4%（Fig. 9a, Tab. 2）。
- **新视角合成**：双分支重建在 T+5 和 T+10 帧的 PSNR/SSIM/LPIPS 上全面超越 SCube 等现有方法，验证了体素与像素分支融合的有效性（Tab. 3）。
- **场景规模**：可生成约 100,000 m² 的无界动态场景，支持 20 秒以上的驾驶长度（Fig. 1, Table 1）。

消融实验进一步揭示了关键设计的作用：语义引导缓冲区是维持长视频质量的最关键成分，坐标缓冲区通过提供稳定的 3D 对应进一步抑制运动模糊；道路表面条件 CRoad 对地面生成的正确性不可或缺；重叠潜变量外推策略显著提升了体素块间的过渡一致性。

方法定位上，InfiniCube 处于**稀疏体素扩散生成、世界引导视频生成与前馈 3DGS 重建**的交汇点。它继承了 XCube 的稀疏体素 LDM 框架，但通过外推策略将其扩展至无界场景；借鉴 Stable Video Diffusion 的视频先验，但以 3D 引导缓冲区替代传统的图像平面条件注入；在重建端，则以双分支架构弥补了 SCube 等单分支方法在动态物体和中景区域的不足。

**主要局限**包括：大规模场景生成耗时较长（30,000 m² 体素外推约 6 分钟，200 帧视频生成约 8 分钟），尚无法实时交互；对无自车轨迹覆盖区域需额外生成虚拟轨迹；长距离块间的全局语义一致性仍有提升空间；模型泛化能力受限于 Waymo 训练数据。

自动驾驶仿真对高保真、可扩展且可控的 3D 环境生成提出了严苛需求。理想的仿真场景需同时满足三项条件：**无界的大规模空间覆盖**（数百米级）、**丰富的动态物体与外观细节**，以及**对布局、行为和环境的灵活控制**。然而，现有方法始终在这三者之间顾此失彼。

### 现有方法的两类缺口

当前主流方案大致分为两条技术路线，各自面临根本性瓶颈：

**路线一：3D 场景生成方法。** 以体素扩散或 NeRF/3DGS 重建为代表的 3D 原生方法（如 **InfiniCity**、**SCube**）能够输出几何一致的渲染表示，但其生成能力多局限于室内场景或小范围室外区域。当扩展至城市级驾驶场景时，这些方法要么缺乏对动态物体的精细控制，要么纹理质量远逊于 2D 生成模型。换言之，它们能“搭好骨架”，却难以“填充血肉”。

**路线二：视频生成模型。** 以 **Vista**、**Panacea** 为代表的 2D 视频模型（后者将 HD 地图投影为图像平面条件）能够合成丰富的纹理与动态外观，但存在两个致命缺陷：一是生成帧数有限（通常不超过 25 帧），无法覆盖长距离驾驶；二是缺乏 3D 一致性，自回归生成时累积误差迅速导致几何漂移和纹理崩溃，无法直接用于物理仿真。

### 核心矛盾与本文动机

上述两类方法的困境指向同一个深层矛盾：**3D 几何精度与 2D 外观丰富性难以兼得**。3D 方法受限于生成模型的表达能力，2D 方法则缺乏几何约束而无法保持长程稳定。自动驾驶仿真恰好要求二者同时成立——既需要精确的道路结构以支撑传感器仿真，又需要逼真的纹理和动态物体以训练感知模型。

InfiniCube 的动机正是拆解这一矛盾：**将 3D 几何先验与 2D 外观生成解耦**。用一个可控的 3D 体素世界作为“世界骨架”，提供精确的几何与语义引导；再让视频模型专注于纹理合成，从骨架中渲染像素级对齐的引导缓冲区以抑制累积误差。最后，通过双分支重建将体素的几何精度与像素的动态细节融合为可渲染的动态 3DGS 场景，从而一次性打通“无界、可控、高保真”三重要求。

## 核心方法与创新机理

InfiniCube 的核心创新在于将 3D 几何先验与 2D 视频生成模型的丰富外观能力进行系统性解耦，构建了一个“世界骨架引导视频生成、双分支融合升维重建”的生成范式。该方法通过三个紧密耦合的机制，系统性地解决了现有方法在高保真、长距离、可模拟和可控性上的瓶颈。

**1. 3D 引导缓冲区：将体素世界作为视频生成的几何锚点**

现有视频生成基线（如 Panacea 将 HD 地图投影为 2D 条件，Vista 仅依赖首帧自回归）缺乏对全局 3D 几何的持续感知，导致长视频生成中累积误差迅速放大。InfiniCube 的核心突破在于引入了**像素级对齐的 3D 引导缓冲区**——从已生成的稀疏体素世界中渲染出语义缓冲区（Semantic Buffer）和坐标缓冲区（Coordinate Buffer），作为视频模型的条件注入（§ 4.2, Fig. 2, Fig. 8）。这一设计将体素世界作为“世界骨架”，使视频模型在每一步自回归中都能感知全局运动和环境变化，从而将 Stable Video Diffusion XT 的高质量帧数从原始的 25 帧扩展至 200 帧。

消融实验证实，语义缓冲区是维持长视频质量的最关键成分，坐标缓冲区则通过提供稳定的 3D 对应关系进一步抑制运动模糊（Fig. 9b）。定量评估表明，在 120 帧时，InfiniCube 对 HD 地图的人工评估对齐正响应率达 84.8%，而 Panacea 仅为 53.4%（Tab. 2），FID 曲线在 100 帧后优势显著（Fig. 9a）。

**2. 无界体素世界外推：无需训练即可扩展至大规模场景**

与单块扩散生成（如 XCube）不同，InfiniCube 采用基于重绘（Repaint）的块间重叠潜变量外推策略，通过公式
$$\mathbf{X}_{\mathrm{new}}^{\mathrm{vx}} = (1 - \mathbf{M}) \odot \hat{\mathbf{X}}_{\mathrm{new}}^{\mathrm{vx}} + \mathbf{M} \odot \hat{\mathbf{X}}_{\mathrm{exist}}^{\mathrm{vx}}$$
将新生成体素块的潜变量与已存在区域的潜变量在重叠掩码 $\mathbf{M}$ 引导下无缝混合（Eq. 1），无需额外训练即可将场景扩展至约 100,000 m²（Fig. 1）。消融实验表明，该外推策略显著优于直接拼接，避免了块间不一致过渡（Fig. S13）。

**3. 双分支前馈重建：体素几何精度与像素动态细节的融合**

现有 3D 重建方法或依赖单一体素分支（如 SCube）导致动态物体和远景细节缺失，或依赖单一像素分支（如 GS-LRM）缺乏几何约束。InfiniCube 提出**体素-像素双分支架构**（§ 4.3, Fig. 4）：体素分支负责从稀疏体素世界和视频帧中重建静态背景的 3D Gaussians，保证几何精度；像素分支则通过 2D UNet，结合 RGB、自监督体素深度掩码与 Depth Anything V2 特征，专门预测动态物体及中景区域的像素级 3D Gaussians。两支路融合后，在新视角合成任务上取得最优 PSNR/SSIM/LPIPS（T+5: 20.80/0.73/0.42; T+10: 19.93/0.72/0.45），超越 SCube 等基线（Tab. 3），且定性结果证实双分支推理消除了单分支的伪影（Fig. 10）。

综上，InfiniCube 的三项关键创新——3D 引导缓冲区的几何锚定、无界体素外推的免训练扩展、双分支融合的几何-外观解耦重建——共同构成了一个从语义世界生成到可控动态 3DGS 场景的完整链路，使模型首次同时满足高保真、长距离、可模拟和可控等自动驾驶仿真需求。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2412_03934/figures/003_Figure_2.jpg]]
*Figure 2: Pipeline. Conditioned on HD maps and bounding boxes, we first generate a 3D voxel world representation. We then render the voxel world into several guidance buffers to boost video generation. The generated video and voxel world are jointly fed into a feedforward dynamic reconstruction module to obtain the final 3DGS representation*

InfiniCube 的整体流水线由三个核心阶段级联构成，形成「世界骨架生成 → 世界引导视频合成 → 动态三维重建」的递进范式。给定 HD 地图、三维车辆边界框和文本提示，系统首先构建一个无界语义体素世界，作为贯穿全流程的三维几何先验；随后将该体素世界渲染为像素对齐的引导缓冲区，注入视频生成模型以支撑长距离、高一致性的外观合成；最后通过双分支前馈重建，将体素几何精度与像素级动态细节融合，产出可控的动态 3D Gaussian Splatting (3DGS) 场景。

**阶段一：无界体素世界生成。** 该阶段以 HD 地图、道路表面高程和三维边界框为条件，通过稀疏体素潜在扩散模型 (LDM) 生成语义体素世界。为突破单块生成的尺度限制，InfiniCube 采用基于重绘 (Repaint) 的块间重叠潜变量外推策略，在扩散去噪过程中将新生成块的潜变量与已存在区域的潜变量按重叠掩码混合：

$$
\mathbf{X}_{\mathrm{new}}^{\mathrm{vx}} = (1 - \mathbf{M}) \odot \hat{\mathbf{X}}_{\mathrm{new}}^{\mathrm{vx}} + \mathbf{M} \odot \hat{\mathbf{X}}_{\mathrm{exist}}^{\mathrm{vx}}
$$

无需额外训练即可将体素世界扩展至无界尺度（Fig. 2 左侧模块）。

**阶段二：世界引导视频生成。** 体素世界沿给定的车辆行驶轨迹被渲染为两组引导缓冲区——语义缓冲区 (Semantic Buffer) 和坐标缓冲区 (Coordinate Buffer)——为视频模型提供像素级对齐的三维几何与实例信息。视频生成以 Stable Video Diffusion XT (SVD-XT) 为基础，将引导缓冲区与前一帧潜变量拼接作为条件输入，通过自回归方式逐段生成长达 200 帧的高质量视频。初始帧由基于 FLUX 的 ControlNet 利用语义缓冲区生成，确保首帧即与三维世界对齐（Fig. 2 中部模块）。

**阶段三：双分支动态 3DGS 重建。** 该阶段将体素世界与合成视频联合输入，通过体素分支与像素分支并行重建动态 3DGS 场景。体素分支利用稀疏三维卷积从体素世界和视频帧中提取特征，负责重建静态背景的高斯原语；像素分支采用二维 UNet，结合 RGB 图像、掩码体素深度与 Depth Anything V2 特征，预测动态物体及中景区域的像素级高斯原语。两支路输出融合后，辅以隐式天空建模，形成完整的可渲染动态场景（Fig. 2 右侧模块）。

三个阶段的输入输出关系可概括为：**HD 地图 + 边界框 → 无界语义体素世界 → 引导缓冲区 + 文本 → 长视频 → 动态 3DGS 场景。** 这一设计将三维几何先验与二维外观生成解耦，体素世界作为「世界骨架」提供精确的三维引导，使视频模型专注于纹理合成，重建时再融合体素与像素信息，分别处理静态背景与动态物体，从而在无界尺度上实现高保真、可控制的动态驾驶场景生成。

InfiniCube 将大规模动态 3D 驾驶场景生成分解为三个解耦的核心模块，通过“世界骨架先验”与“外观合成”的分离策略，实现高保真、长距离、可控的场景生成。

### 无界体素世界生成器

该模块以 HD 地图、道路表面和 3D 边界框为条件，通过稀疏体素潜在扩散模型生成语义体素世界。其核心创新在于**无需训练的块间外推策略**，使模型能够突破单块生成的空间限制，扩展至无界场景。

具体而言，在生成新体素块时，利用与已存在区域的重叠潜变量进行混合，通过重绘机制实现无缝拼接。该过程的形式化表达为：

$$
\mathbf{X}_{\mathrm{new}}^{\mathrm{vx}} = (1 - \mathbf{M}) \odot \hat{\mathbf{X}}_{\mathrm{new}}^{\mathrm{vx}} + \mathbf{M} \odot \hat{\mathbf{X}}_{\mathrm{exist}}^{\mathrm{vx}}
$$

其中，$\hat{\mathbf{X}}_{\mathrm{new}}^{\mathrm{vx}}$ 为当前扩散步骤生成的新块潜变量，$\hat{\mathbf{X}}_{\mathrm{exist}}^{\mathrm{vx}}$ 为重叠区域中已存在的潜变量，$\mathbf{M}$ 为重叠掩码，$\odot$ 表示逐元素乘法。该混合策略有效抑制了块间过渡的不一致性。

体素扩散模型的训练采用 v-参数化损失函数：

$$
\mathcal{L}_{\mathrm{Diffusion}} = \mathbb{E}_{t, \mathbf{X}^{vx}, \epsilon \sim \mathcal{N}(0, \mathbf{I})} \left[ \left\| v \left( \sqrt{\bar{\alpha}_t} \mathbf{X}^{vx} + \sqrt{1 - \bar{\alpha}_t} \epsilon, t \right) - \left( \sqrt{\bar{\alpha}_t} \epsilon - \sqrt{1 - \bar{\alpha}_t} \mathbf{X}^{vx} \right) \right\|_2^2 \right]
$$

该公式定义了从噪声 $\epsilon$ 到干净潜变量 $\mathbf{X}^{vx}$ 的去噪过程，$v(\cdot)$ 为网络预测的速度场，$\bar{\alpha}_t$ 为噪声调度参数。

### 世界引导视频生成器

该模块将体素世界渲染为**语义缓冲区**和**坐标缓冲区**，作为视频模型的像素级对齐 3D 引导。视频生成基于 Stable Video Diffusion XT 架构，其潜变量表示为：

$$
\dot{\mathbf{X}}^{\mathrm{vd}} = \dot{\mathcal{E}}^{\mathrm{vd}}(\mathbf{D}^{\mathrm{vd}}) \in \mathbb{R}^{h \times w \times T \times 4}
$$

其中 $\mathbf{D}^{\mathrm{vd}}$ 为输入视频，$\dot{\mathcal{E}}^{\mathrm{vd}}$ 为 SVD 编码器，空间下采样因子为 8，即 $h = H/8$，$w = W/8$。视频模型的条件由三部分拼接而成：

$$
\mathbf{C}^{\mathrm{vd}} = \{ \mathbf{C}_{\mathrm{Img}}^{\mathrm{vd}}, \mathbf{C}_{\mathrm{Sem}}^{\mathrm{vd}}, \mathbf{C}_{\mathrm{Crd}}^{\mathrm{vd}} \}
$$

其中 $\mathbf{C}_{\mathrm{Img}}^{\mathrm{vd}}$ 为图像条件，$\mathbf{C}_{\mathrm{Sem}}^{\mathrm{vd}}$ 为语义缓冲区，$\mathbf{C}_{\mathrm{Crd}}^{\mathrm{vd}}$ 为坐标缓冲区，总通道数 $M=12$。在自回归生成中，每步均注入 3D 引导缓冲区，使模型感知全局运动和环境变化，显著抑制累积误差。

初始帧由基于 FLUX 的 ControlNet 生成，以语义缓冲区作为控制图像。

### 双分支动态 3DGS 重建

该模块将体素世界与生成视频联合升维为动态 3D Gaussian Splatting 场景，核心设计为体素分支与像素分支的融合。

**体素分支**负责静态背景重建，从体素世界和视频帧中通过稀疏 3D 卷积提取特征，直接预测 3D Gaussians 参数。

**像素分支**针对动态物体和中景区域，采用 2D UNet 架构。其关键输入包括：
- 自监督体素深度掩码 $\tilde{\mathbf{Z}}$：对渲染体素深度 $\mathbf{Z}$ 进行随机掩码，迫使网络学习鲁棒的深度先验；
- Depth Anything V2 特征 $\mathbf{F}_{\mathrm{DAV2}}$：提供预训练 ViT 骨干提取的深度先验，增强对体素未覆盖区域的深度预测能力。

像素分支将网络预测的深度值转换为 3D Gaussian 中心坐标的计算链为：

$$
\omega^i = \sigma(\mathbf{G}_{\mathrm{depth}}^i), \quad z^i = (1-\omega^i) \cdot z_{\mathrm{near}} + \omega^i \cdot z_{\mathrm{far}}, \quad t^i = z^i / \cos(\mathrm{ray}_d^i, \mathrm{ray}_d^{\mathrm{look-at}}), \quad \mathrm{xyz}^i = \mathrm{ray}_o^i + t^i \cdot \mathrm{ray}_d^i
$$

其中 $\mathbf{G}_{\mathrm{depth}}^i$ 为网络预测的深度 logit，$\sigma$ 为 sigmoid 函数，$z_{\mathrm{near}}$ 和 $z_{\mathrm{far}}$ 为近/远平面，$\mathrm{ray}_o^i$ 和 $\mathrm{ray}_d^i$ 为射线原点与方向。

**天空建模**采用隐式表示，使用轻量 Transformer 编码器与可学习查询令牌交互，提取紧凑的天空外观特征向量 $\mathbf{c} \in \mathbb{R}^{192}$，再通过 AdaLN 调制的 MLP 解码天空颜色：

$$
\mathbf{c}, \tilde{\mathbf{p}}^i = \mathrm{TransformerEncoder}(\mathbf{c}_{\mathrm{query}}, \mathbf{p}^i)
$$

其中 $\mathbf{c}_{\mathrm{query}}$ 为可学习查询令牌，$\mathbf{p}^i$ 为天空图像块特征。该设计使天空表示对未见区域具有良好的泛化性。

## 实验与关键发现

### 实验设置

InfiniCube 在 **Waymo Open Dataset** 上进行训练与评估，使用 618 个序列作为训练集，90 个序列作为测试集。整个训练流程分为三个阶段：体素世界生成阶段耗时约 48 GPU 天，视频生成阶段约 192 GPU 天，场景重建阶段约 32 GPU 天。视频生成基于 **Stable Video Diffusion XT**（SVD-XT）的 25 帧基础模型，推理时设置无分类器引导权重为 3.0，去噪步数为 25。为确保公平对比，所有视频生成基线均采用相同的自回归推理策略和相同的第一帧作为初始条件；**Panacea** 方法基于相同的 SVD-XT 主干进行了重新实现，以保证基础模型能力一致。

### 长视频生成质量对比

InfiniCube 的核心优势在于通过 3D 引导缓冲区显著抑制了长视频自回归生成中的累积误差。如 Fig. 9a 所示，在 Waymo 测试集上以第一帧为条件生成长达 200 帧的视频时，InfiniCube 的 FID 指标始终低于 **Panacea** 和 **Vista** 等基线方法。约 100 帧之后，Panacea 和 Vista 的 FID 快速上升，视频质量急剧退化，而 InfiniCube 仍能维持较低的 FID 和良好的视觉质量。这一趋势在 Fig. 8 的定性对比中也得到印证：InfiniCube 生成的 200 帧视频保持了清晰的道路结构、车辆运动和场景细节，而基线方法在长帧数下出现严重的几何失真和纹理模糊。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2412_03934/figures/010_Figure_8.jpg]]
*Figure 8: Video Model Comparison. Our model can generate high-quality videos of 200 frames from 25-frame SVD-XT by conditioning on guidance buffers. These buffers also enable the motions in the videos to be consistent with the scale of the physical world*

### HD 地图对齐人工评估

为量化生成视频与输入 HD 地图的长期对齐程度，作者通过 **MakeSense AI** 平台进行了人工评估。评估者需判断 HD 地图投影（道路边界、车道线、车辆边界框）与生成 RGB 图像的对齐程度。结果如 Tab. 2 所示：

| 方法 | 第 40 帧正响应率 | 第 80 帧正响应率 | 第 120 帧正响应率 |
|------|-----------------|-----------------|------------------|
| Panacea | 76.8% | 54.0% | 53.4% |
| **InfiniCube** | **84.6%** | **83.9%** | **84.8%** |

InfiniCube 在所有时间节点均显著优于 Panacea，且正响应率随帧数增加几乎不衰减，验证了 3D 引导缓冲区在维持长期空间对齐方面的关键作用。

### 新视角合成评估

在 3D 场景重建质量方面，作者在 Waymo 数据集上进行了新视角合成实验。给定 T 时刻的输入图像，在 T+5 和 T+10 时刻渲染新视角，并与多个基线方法对比。Tab. 3 的结果显示，InfiniCube 在所有指标上均取得最优：

- **T+5 时刻**：PSNR 20.80 / SSIM 0.73 / LPIPS 0.42，较 **SCube**（19.90 / 0.72 / 0.47）分别提升 0.90 / 0.01 / -0.05。
- **T+10 时刻**：PSNR 19.93 / SSIM 0.72 / LPIPS 0.45，较 SCube（18.78 / 0.70 / 0.49）分别提升 1.15 / 0.02 / -0.04。

InfiniCube 同样超越 **PixelNeRF**（Yu et al., CVPR 2021）、**PixelSplat**、**DUSt3R**、**MVSplat** 和 **MVSGaussian** 等新视角合成基线，验证了双分支重建架构的有效性。

### 消融实验

#### 道路表面条件（CRoad）

移除 3D 道路表面条件 CRoad 后，体素世界生成模型有时无法正确确定可行驶区域，导致地面生成错误（Fig. 7）。这一消融实验证明 CRoad 对场景几何一致性的关键作用。

#### 引导缓冲区成分

Fig. 9b 的消融实验表明，**语义缓冲区**是维持长视频质量的最关键引导成分——移除语义缓冲区后，视频质量迅速退化。**坐标缓冲区**通过提供稳定的像素级 3D 对应关系，进一步降低了运动引起的细节模糊和模糊性。两者结合使用才能达到最佳效果。

#### 体素外推策略

在无界体素世界生成中，使用基于 **Repaint** 的重叠潜变量外推策略（Eq. 1）能显著提升不同体素块之间的过渡一致性。如 Fig. S13 所示，不使用重叠潜变量而直接拼接时，块间可能出现不一致的语义过渡。这一设计无需额外训练，即可将体素世界扩展至无界场景。

#### 双分支重建

Fig. 10 和 Tab. 3 的对比表明，单独使用体素分支（SCube）或单独使用像素分支均会产生不同类型的伪影。双分支重建通过体素分支负责静态背景、像素分支负责动态物体及中景区域，有效消除了单一分支的伪影，并在新视角合成指标上取得一致提升。像素分支中引入的自监督体素深度掩码与 **Depth Anything V2** 特征，增强了对体素未覆盖中景区域的深度预测能力，进一步提升了重建质量。

### 失败模式与局限性

尽管 InfiniCube 在各项指标上表现优异，但仍存在以下局限性：

1. **生成速度**：大规模场景（约 30,000 m²）的体素外推需约 6 分钟，视频生成需约 8 分钟，尚无法满足实时交互需求。
2. **区域覆盖依赖**：若部分场景无自车轨迹覆盖，需额外策略生成虚拟轨迹以渲染引导缓冲区，增加了使用复杂性。
3. **长距离块间一致性**：尽管外推策略缓解了局部接缝问题，但全局范围的语义和纹理一致性仍有待提升。
4. **数据依赖性**：模型训练数据源于 Waymo Open Dataset，向其它地理区域或传感器模态的泛化能力未经验证。

### 关键图表结论总结

- **Fig. 9a / Tab. 2**：3D 引导缓冲区使长视频 FID 显著低于基线，HD 地图对齐正响应率在 120 帧时仍达 84.8%（Panacea 仅 53.4%），证明引导缓冲区设计有效抑制了自回归累积误差。
- **Tab. 3**：双分支重建在新视角合成中取得最优 PSNR/SSIM/LPIPS，验证了体素与像素分支融合的有效性。
- **Fig. 7**：CRoad 消融证明道路表面条件对场景地面生成的一致性至关重要。
- **Fig. 9b**：语义缓冲区是维持长视频质量的最关键成分，坐标缓冲区进一步解决运动模糊问题。
- **Fig. S13**：重叠潜变量外推策略显著优于直接拼接，是块间无缝过渡的关键设计。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2412_03934/figures/005_Figure_4.jpg]]
*Figure 4: Illustration of concepts in the pixel branch. The midground region and masked / full voxel depth*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2412_03934/figures/011_Figure_9.jpg]]
*Figure 9: Comparison of long video generation quality based on the first frame from the Waymo Dataset. FID: lower is better. Table 2. Human evaluation of HD map alignment. We highlight the best and the second*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2412_03934/figures/013_Table_3.jpg]]
*Table 3: Quantitative comparisons of novel view rendering. Metrics are computed at frames T + 5 and T + 10 given frame T as input. We highlight the best , second best and third best*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2412_03934/figures/019_Table.jpg]]
*Table: S4. Semantic categories and their RGB values in the semantic buffer. The RGB values in the table range from 0 to 1. In practice, we rescale the above values from -1 to 1 for the encoder*

## 定位与知识库关联

### 核心问题与现有方法瓶颈

自动驾驶仿真对大规模动态 3D 场景生成提出了三重苛刻需求：**高保真外观、长距离可模拟、以及布局/外观/行为的灵活可控**。现有方法各自仅能覆盖其中部分维度。

**3D 场景生成方法**（如 InfiniCity、WoVoGen、SCube）虽能输出显式 3D 表示，但主要面向室内场景或静态环境，缺乏对动态物体和长距离场景的精细控制能力。**视频生成模型**（如 Stable Video Diffusion XT、Vista、Panacea）在纹理丰富度上表现优异，却受限于 25 帧左右的短时序生成，且缺乏显式 3D 几何约束，自回归长视频生成时累积误差迅速导致画面崩溃。两类方法之间存在根本性的**几何-外观鸿沟**：3D 方法有结构但缺细节，视频方法有细节但缺结构。

InfiniCube 的核心洞察在于**将 3D 几何先验与 2D 视频模型的丰富外观能力解耦**——用稀疏体素世界作为"世界骨架"提供精确的 3D 引导，使视频模型专注于纹理合成，避免几何失真与累积漂移；重建阶段再融合体素与像素信息，分别处理静态背景与动态物体，实现高质量可扩展的 3D 动态场景生成。

### 与关键基线的对比定位

**视频生成基线**

- **Panacea**：基于 HD 地图投影到图像平面作为条件，使用与 InfiniCube 相同的 SVD-XT 主干重新实现。关键差异在于 InfiniCube 用 3D 体素世界渲染的像素对齐引导缓冲区（语义缓冲区 + 坐标缓冲区）替代了平面投影条件。在 Waymo 数据集 200 帧自回归生成中，Panacea 的 FID 在约 100 帧后快速上升，而 InfiniCube 维持显著更低且平稳的 FID 曲线（Fig. 9a）；人工评估中，帧 120 时 HD 地图对齐正响应率差距达 31.4%（84.8% vs 53.4%，Tab. 2），证实 3D 引导对抑制累积误差的决定性作用。

- **Vista**：仅依赖第一帧进行自回归生成，无额外地图或 3D 条件。InfiniCube 通过注入引导缓冲区使模型感知全局运动和环境变化，在长视频质量上同样形成明显优势（Fig. 8, Fig. 9a）。

**3D 重建基线**

- **SCube**：采用单一体素分支重建 3D Gaussians。InfiniCube 的**双分支重建**在体素分支（负责静态背景）基础上引入像素分支，通过自监督体素深度掩码和 Depth Anything V2 特征预测动态物体及中景区域。Waymo 数据集新视角合成中，T+5 帧 PSNR 提升 0.90 dB，T+10 帧提升 1.15 dB（Tab. 3），且定性结果消除了单分支的伪影（Fig. 10）。

- **PixelNeRF** (Yu et al., CVPR 2021)、**PixelSplat**、**DUSt3R**、**MVSplat**、**MVSGaussian**：作为新视角渲染基线，InfiniCube 在 PSNR/SSIM/LPIPS 三项指标上均取得最优（Tab. 3），验证了双分支融合策略相较于纯像素驱动或纯体素驱动方法的综合优势。

**体素生成基线**

- **InfiniCity** 和 **WoVoGen**：作为 3D 体素/视频联合生成基线，InfiniCube 在场景尺度（~100,000 m²）和输出类型（视频 + 可渲染 3D 表示）上形成差异化（Table 1, Fig. 1）。

### 方法谱系中的位置

InfiniCube 处于**可控 3D 场景生成**与**世界引导视频生成**的交叉地带。其技术谱系可追溯至：

1. **稀疏体素扩散模型**：基于 XCube 的稀疏体素 LDM，通过地图条件化和基于 Repaint 的块间重叠潜变量外推实现无界扩展（Eq. 1），无需额外训练即可生成任意尺度场景。

2. **视频扩散模型的条件注入**：将 3D 体素世界渲染为像素对齐的语义/坐标引导缓冲区，输入 SVD-XT 的潜变量空间作为条件，使视频模型获得隐式 3D 感知能力。

3. **前馈 3D Gaussian 重建**：继承 SCube 等方法的思路，创新性地引入双分支架构——体素分支处理静态几何，像素分支处理动态和中景细节，并通过自监督深度掩码策略增强泛化能力。

4. **隐式天空建模**：采用 STORM 的轻量 Transformer 编码器与 AdaLN 调制 MLP，从图像中隐式建模天空颜色，避免对天空区域进行无效的 3D 重建。

### 适用边界与局限

**适用场景**

- 给定 HD 地图、3D 边界框和文本提示的大规模驾驶场景生成
- 需要长距离（200+ 帧、20s+）视频与可渲染 3DGS 表示的应用
- 需要控制动态物体运动轨迹和天气/光照条件的仿真场景

**关键局限**

1. **生成速度**：大规模场景（30,000 m²）的体素外推约需 6 分钟，视频生成约需 8 分钟，尚无法满足实时交互需求。这是当前方法面向离线仿真应用的根本性约束。

2. **区域覆盖依赖**：引导缓冲区渲染需要自车轨迹覆盖目标区域。对于无轨迹覆盖的场景区域，需额外策略生成虚拟轨迹，增加了使用复杂性和潜在的轨迹合理性风险。

3. **长距离块间一致性**：尽管重叠潜变量外推策略缓解了局部接缝问题（Fig. S13），全局范围的语义和纹理一致性仍有提升空间，可能出现纹理重复或语义漂移。

4. **数据依赖性**：模型训练完全基于 Waymo Open Dataset（618 序列训练，90 序列评估），向其他地理区域（如非美国城市道路）、传感器模态或天气条件的泛化能力未经验证。

5. **动态物体建模粒度**：当前动态物体控制依赖输入的 3D 边界框轨迹，生成的运动模式受限于训练数据分布，对复杂交互行为（如车辆变道、行人随机穿越）的建模能力有限。

### 开放问题

1. **全局一致性的进一步突破**：如何在不显著增加计算成本的前提下，提升长距离块间的全局语义一致性，避免反复生成时的纹理重复或语义漂移？可能的探索方向包括引入全局场景图约束或层次化生成策略。

2. **实时生成的可能性**：当前分钟级的生成速度离实时仿真需求差距明显。模型蒸馏、推理步数压缩、或探索更高效的 3D 表示（如基于哈希网格的混合表示）可能是突破口。

3. **多模态条件扩展**：能否将条件从 HD 地图 + 文本扩展至自然语言描述、俯视图草图或真实传感器数据，使系统适用于更广泛的仿真场景构建？

4. **动态交互建模**：当前动态物体沿预设轨迹运动，缺乏与环境和其他智能体的交互。引入基于物理或规则的交互模型，或从真实驾驶数据中学习交互先验，是提升仿真真实感的重要方向。

5. **跨域泛化**：模型在 Waymo 数据上训练，向其他城市、国家或传感器配置的迁移能力未知。域自适应或少量样本微调策略值得探索。

## 原文 PDF

![[paperPDFs/ICCV_2025/InfiniCube_Unbounded_and_Controllable_Dynamic_3D_Driving_Scene_Generation_with_World_Guided_Video_Models.pdf]]
