---
title: HY-World 2.0 A Multi-Modal World Model for Reconstructing Generating and Simulating 3D Worlds
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/HY_World_2_0_A_Multi_Modal_World_Model_for_Reconstructing_Generating_and_Simulating_3D_Worlds.pdf
project_link: https://3d-models.hunyuan.tencent.com/world/
code_link: https://github.com/Tencent-Hunyuan/HY-World-2.0
aliases:
- HY-World-2.0
- HY-World
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过在四阶段管线中引入视频扩散模型的生成式先验（WorldStereo 2.0使用关键帧VAE和几何记忆）以及升级的前馈重建模块（WorldMirror 2.0的归一化位置编码、深度‑法线耦合），将3D几何严谨性与视频生成的丰富动态先验相融合。
primary_logic: 将全景生成、轨迹规划、基于记忆的一致性世界扩展和深度对齐的3DGS合成组合为一体化管线，既可利用扩散模型先验提升生成世界的逼真度和可探索范围，又能通过前馈多模态重建保证多视图输入的几何精确性，从而在同一框架内统一生成与重建。
claims:
- HY-World 2.0在多项基准上达到开源方法中的最优性能，与闭源模型Marble相当。
- WorldStereo 2.0在单视图3D重建任务中（Tanks-and-Temples和MipNeRF360）取得最高的点云F1分数。
- WorldMirror 2.0跨分辨率保持性能稳定，在7-Scenes上将点图精度误差从0.043降至0.033，相机姿态AUC@30提升超过20个点。
- MaskGaussian将3DGS高斯数量减少73.7%，而PSNR仅下降0.14 dB，解决了生成场景中质量与效率的权衡。
---

# HY-World 2.0 A Multi-Modal World Model for Reconstructing Generating and Simulating 3D Worlds

> [!tip] 核心洞察
> 将全景生成、轨迹规划、基于记忆的一致性世界扩展和深度对齐的3DGS合成组合为一体化管线，既可利用扩散模型先验提升生成世界的逼真度和可探索范围，又能通过前馈多模态重建保证多视图输入的几何精确性，从而在同一框架内统一生成与重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | HY-World 2.0：一个面向重建、生成和模拟3D世界的多模态世界模型 |
| 英文题名 | HY-World 2.0 A Multi-Modal World Model for Reconstructing Generating and Simulating 3D Worlds |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2604.14268) · [Project](https://3d-models.hunyuan.tencent.com/world/) · [Code](https://github.com/Tencent-Hunyuan/HY-World-2.0) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HY-World 2.0 |
| Dataset | Text‑to‑Panorama, Image‑to‑Panorama, Single‑view 3D Reconstruction, Camera‑Controlled Video Generation |

> [!tip] 效果简介
> - Text‑to‑Panorama (T2P) 上，CLIP‑T 0.258 vs - (最佳)。
> - Image‑to‑Panorama (I2P) 上，CLIP‑I 0.844 vs - (最佳)。
> - Single‑view 3D Reconstruction (Tanks‑and‑Temples) 上，点云 F1‑score 41.43 vs – (优于所有视频生成方法) (-)。

## 概要

### 问题与瓶颈

现有3D世界模型在生成与重建任务之间存在严重割裂：生成方法难以保持严格的几何一致性，重建方法则缺乏对未见区域的生成式先验。同时，开源社区长期缺少一个能够将两种能力统一在同一框架内的多模态世界模型。HY-World 2.0正是针对这一瓶颈而提出——它旨在作为首个开源、系统化的多模态世界模型，将“世界生成”与“世界重建”无缝融合于一个离线3D世界模型范式之中。

### 核心思路

HY-World 2.0的核心洞察在于：将全景生成、轨迹规划、基于记忆的一致性世界扩展和深度对齐的3DGS合成组合为一体化管线。该管线既利用视频扩散模型的生成式先验提升生成世界的逼真度和可探索范围，又通过升级的前馈多模态重建模块保证多视图输入的几何精确性，从而在同一框架内统一生成与重建。

具体而言，管线由四个阶段构成（图2）：
1. **全景生成（HY‑Pano 2.0）**：从文本或单视图图像生成高保真360°全景图，采用基于MMDiT的隐式自适应映射替代显式几何扭曲，结合圆形填充与像素混合消除边界伪影。
2. **轨迹规划（WorldNav）**：对全景场景进行几何与语义解析，规划信息量最大且无碰撞的相机探索路径，支持五种轨迹模式。
3. **世界扩展（WorldStereo 2.0）**：基于关键帧的相机控制视频扩散模型，引入Global‑Geometric Memory（GGM）和增强型Spatial‑Stereo Memory（SSM++）实现多轨迹一致的世界扩展，并采用Keyframe‑VAE保留高频细节。
4. **世界合成（World Composition）**：通过点云扩展、深度对齐和定制3DGS优化（集成MaskGaussian剪枝），将生成的关键帧与初始全景融合为可导航的3D表示。

对于世界重建任务，HY-World 2.0升级了前馈统一模型**WorldMirror 2.0**，引入归一化位置编码、深度‑法线耦合损失和深度掩码预测头，从多视图图像或视频中直接重建点云、深度、法线、相机参数和3D高斯。

### 方法谱系与知识库定位

HY-World 2.0建立在多个前沿工作的基础之上，并通过关键模块的升级实现突破：

- 相对于**HY-World 1.0**（Team HunyuanWorld, arXiv 2025），2.0版本在管线的每一阶段都进行了实质性改进：全景生成从显式几何扭曲升级为MMDiT隐式映射；世界扩展引入GGM/SSM++记忆机制和Keyframe‑VAE；世界合成集成MaskGaussian剪枝；重建模型WorldMirror从绝对位置编码升级为归一化位置编码。
- 在视频生成维度，**WorldStereo**（Tencent Hunyuan 3D Team, 2026）提供相机引导视频生成的基线，HY-World 2.0在此基础上通过潜空间替换（Keyframe‑VAE）、记忆机制重构和DMD蒸馏实现显著提升。
- 在前馈3D重建维度，**MapAnything**（Keetha et al., arXiv 2025）和**DepthAnything3**（Lin et al., arXiv 2025）是代表性基线，WorldMirror 2.0通过多阶段课程学习、深度‑法线耦合和分辨率无关的位置编码在多任务上取得更优性能。
- 作为整体性能的上界参照，闭源商业模型**Marble**（World Labs, 2025）被用于定性比较，HY-World 2.0在多项基准上达到开源方法中的最优性能，与Marble表现相当。

### 主要结果概要

- **全景生成**：在Text‑to‑Panorama（T2P）任务上CLIP‑T达到0.258，Image‑to‑Panorama（I2P）任务上CLIP‑I达到0.844，均为最佳。
- **单视图3D重建**：WorldStereo 2.0在Tanks‑and‑Temples和MipNeRF360上取得最高的点云F1分数（Tanks‑and‑Temples F1为41.43），优于所有视频生成方法。
- **相机控制视频生成**：旋转误差（RotErr）从基线的0.758降至0.492，降幅达35%。
- **多视图重建**：WorldMirror 2.0在7‑Scenes上将点图精度误差从0.043降至0.033，相机姿态AUC@30提升超过20个点；且在高分辨率下保持性能稳定，解决了WorldMirror 1.0的退化问题。
- **3DGS效率**：MaskGaussian将高斯数量减少73.7%（从5.25M降至1.38M），PSNR仅下降0.14 dB，有效解决生成场景中质量与效率的权衡。

### 局限与开放问题

HY-World 2.0仍存在若干局限：深度对齐中的异常检测可能将整条视频标记为离群值导致失效；天空分割（SAM3）在阴天或夜间场景可能出错；管线依赖多个大规模预训练模型，整体鲁棒性受限于这些组件的性能；端到端世界生成耗时约10分钟（NVIDIA H20），离实时交互仍有距离。这些局限指向若干开放问题，包括如何自适应恢复被误判的离群视频、如何在复杂光照下稳定天空掩码、如何进一步降低管线延迟，以及能否将轨迹规划与强化学习结合以自监督方式发现最优探索路径。

### 3D世界模型的演进与割裂

构建可交互的沉浸式3D世界是计算机视觉与图形学的长期目标。近年来，3D世界模型取得了显著进展，但其发展路径呈现出明显的**任务割裂**：一方面，以视频扩散模型为代表的**生成式方法**能够从文本或单张图像合成丰富的动态场景，却难以保证严格的几何一致性；另一方面，以多视图立体重建为核心的**重建式方法**能够从多视角输入中精确恢复3D几何，但缺乏对未观测区域的生成式先验，无法自主扩展世界边界。更关键的是，开源社区长期缺少一个能够**在同一框架内统一生成与重建**的多模态世界模型，使得研究者难以在两类能力之间建立系统性的关联与互补。

### 现有方法的瓶颈

从技术管线来看，这一割裂体现在多个层面：

1. **全景生成与3D扩展的脱节**：现有全景生成方法多依赖显式几何扭曲将透视图像映射至全景域，容易引入投影畸变和边界伪影；而全景到3D世界的扩展则缺乏有效的轨迹规划与一致性记忆机制，导致生成的世界在探索过程中出现内容断裂。

2. **视频生成先验与3D重建的隔离**：视频扩散模型虽能提供丰富的动态先验，但其标准时空VAE在大视角变化下会引入运动模糊，损害重建所需的细节保真度；同时，多轨迹生成时缺乏跨路径的几何记忆，难以保证世界级的一致性。

3. **前馈重建模型的鲁棒性不足**：以**MapAnything**（Keetha et al., arXiv 2025）和**DepthAnything3**（Lin et al., arXiv 2025）为代表的前馈方法在固定分辨率下表现良好，但跨分辨率泛化时性能严重退化——绝对位置编码导致高分辨率输入下重建质量急剧下降，且缺乏深度与法线之间的几何耦合约束。

4. **3D表达的质量-效率权衡**：标准3DGS优化在高斯数量膨胀与渲染质量之间存在尖锐矛盾，尤其在生成场景的低频区域（如天空），冗余高斯不仅浪费计算资源，还可能产生漂浮伪影。

### 闭源模型的启示与开源的空白

闭源商业模型如**Marble**（World Labs, 2025）已初步展示了统一世界生成与重建的潜力，但其技术细节不公开，无法为社区提供可复现的研究基础。HY-World 1.0（Team HunyuanWorld, arXiv 2025）作为先前的开源尝试，建立了基本的生成管线，但在全景生成质量、多轨迹一致性、重建精度和效率方面仍存在显著不足。

### 本文的动机与核心思路

针对上述瓶颈，HY-World 2.0的动机明确：**构建首个开源、系统化的多模态世界模型，在同一框架内无缝统一世界生成与世界重建**。其核心洞察在于：将视频扩散模型的生成式先验与前馈重建模型的几何严谨性融合为一体化管线——通过全景生成建立世界初始化，利用场景解析与轨迹规划确定探索路径，借助记忆机制实现一致的世界扩展，最终通过深度对齐与定制3DGS优化合成可导航的3D表达。这一设计既可利用扩散模型先验提升生成世界的逼真度和可探索范围，又能通过前馈多模态重建保证多视图输入的几何精确性，从而在开源范式下弥合生成与重建之间的鸿沟。

## 核心方法与创新机理

HY-World 2.0 的核心创新在于通过四阶段管线将**视频扩散模型的生成式先验**与**前馈多模态重建的几何严谨性**深度融合，解决了现有3D世界模型在生成与重建任务间的严重割裂。其关键创新体现在以下五个维度的**changed slots**上，每个改进均直接服务于“统一生成与重建”这一核心目标。

---

### 1. 全景生成：从显式几何扭曲到隐式自适应映射

**HY-Pano 1.0** 依赖显式几何扭曲将透视图像映射为全景图，容易在投影边界引入畸变和伪影。**HY-Pano 2.0** 转而采用基于 **MMDiT（Multi-Modal Diffusion Transformer）** 的隐式自适应映射策略，配合**圆形填充（circle padding）** 与**像素混合（pixel blending）** 技术，从扩散模型的潜空间层面消除左右边界的不连续性（Fig. 3）。这一改进使得全景生成不再受限于固定的几何投影假设，从而在文本到全景（T2P, CLIP-T 0.258）和图像到全景（I2P, CLIP-I 0.844）任务上均达到最优（Tab. 4），为后续世界扩展提供了更高质量的全景初始化。

### 2. 视频生成潜空间：从时空VAE到纯空间Keyframe-VAE

**WorldStereo 1.0** 使用时空 Video-VAE 压缩视频帧，在大视角变化下容易引入运动模糊，损失高频纹理和几何细节。**WorldStereo 2.0** 将潜空间替换为**纯空间 Keyframe-VAE**（Fig. 9），仅对单帧进行空间压缩，完整保留高频外观信息。这一改进在保持相机可控性的前提下，显著提升了大视角变化下生成帧的保真度（Fig. 8），使得相机控制误差 RotErr 从基线 0.758 降至 0.492（Tab. 7），为后续的3D重建提供了更可靠的几何线索。

### 3. 多视角一致性记忆：从独立记忆分支到集成式双重记忆

**WorldStereo** 的记忆机制为独立分支，难以与主 DiT 分支充分交互。**WorldStereo 2.0** 引入了两种深度集成的记忆机制：
- **Global-Geometric Memory (GGM)**：通过拼接参考点云和新视角采样点云构造全局点云 $\mathbf{P}^{glo} = [\mathbf{P}^{ref}, \hat{\mathbf{P}}] \in \mathbb{R}^{(N+\hat{N})\times 3}$（Eq. 2），直接注入相机控制分支，提供跨轨迹的全局几何引导。
- **增强型 Spatial-Stereo Memory (SSM++)**：采用**空间拼接**（而非时间拼接）将检索到的参考视图与目标帧在 RoPE 维度上直接拼接（Fig. 11），实现细粒度的纹理一致性。

消融实验表明，同时集成 GGM 和 SSM++ 大幅改善了光度质量与多轨迹一致性；SSM++ 的空间拼接设计在各项指标上均显著优于时间拼接方案（Tab. 8）。

### 4. 世界重建模型：从绝对位置编码到归一化位置编码与深度-法线耦合

**WorldMirror 1.0** 使用绝对位置编码，在高分辨率输入下性能严重退化（7-Scenes 点图精度误差 0.043），且仅依赖几何头进行重建。**WorldMirror 2.0** 进行了三项关键升级：
- **归一化位置编码**：将图像块网格坐标映射到固定 $[-1, 1]$ 范围 $\hat{x}_i = \frac{2i+1}{H_p} - 1, \hat{y}_j = \frac{2j+1}{W_p} - 1$（Eq. 4），实现分辨率无关的特征表示，跨分辨率一致性超过 0.95（Fig. 13）。
- **深度-法线耦合损失** $\mathcal{L}_{\mathrm{d2n}}$（Eq. 7）：通过预测深度反投影计算法线后与真值法线之间的角度误差，强制几何一致性。
- **深度掩码预测头**与**多阶段课程学习**：提升对遮挡和不确定区域的鲁棒性。

这些改进将 7-Scenes 点图精度误差从 0.043 降至 0.033，相机姿态 AUC@30 提升超过 20 个点（Tab. 11），且在高分辨率下性能保持稳定甚至提升，而 WorldMirror 1.0 则严重退化（Fig. 26）。

### 5. 3DGS优化策略：从标准优化到天空约束与MaskGaussian剪枝

生成式3D场景中，标准 3DGS 优化（含球谐函数）容易在天空等低频区域产生大量冗余高斯，导致渲染效率低下。HY-World 2.0 的**World Composition** 阶段采用三项定制优化：
- **仅优化视角无关 RGB**：去除球谐函数的高频分量，避免生成场景中的过拟合。
- **天空区域增长限制**：防止天空区域产生漂浮伪影。
- **集成 MaskGaussian 剪枝**：通过掩码稀疏正则化 $\mathcal{L}_{\mathrm{mask}} = \lambda_m (\frac{1}{N} \sum_{k=1}^{N} M_k)^2$ 鼓励高斯掩码的稀疏性，将高斯数量从 5.254M 降至 1.383M（减少 73.7%），而 PSNR 仅下降 0.14 dB（Tab. 9），有效解决了生成场景中质量与效率的权衡。

---

### 创新总结

上述五个 changed slots 共同构成了 HY-World 2.0 的核心创新体系：**生成侧**通过隐式全景映射和 Keyframe-VAE 提升视觉先验的质量，**一致性与扩展侧**通过双重记忆机制保证多轨迹世界的几何与纹理连贯性，**重建侧**通过归一化编码和深度-法线耦合保证多视图输入的几何精确性，**合成侧**通过定制化 3DGS 优化实现高效渲染。这一体系使得 HY-World 2.0 成为首个在同一框架内统一高质量世界生成与精确世界重建的开源多模态世界模型，在多项基准上达到开源方法最优，与闭源模型 **Marble**（World Labs, 2025）性能相当。

HY‑World 2.0 是一个多模态世界模型，将**世界生成**与**世界重建**统一于同一框架之内。其核心设计围绕一条四阶段管线展开，同时以升级的前馈重建模型为补充，使系统既能从稀疏输入（文本或单视图图像）合成可导航的 3D 场景，又能从多视图观测中恢复精确的几何表示。该框架的总体架构如 **Figure 2** 所示。

![[assets/figures/papers/HY-World_2.0_A_Multi-Modal_World_Model_for_Reconstructing_Generating_and_Simulat_6a92b680015f/figures/003_Figure_2.jpg]]
*Figure 2: Architecture of HY-World 2.0. Our framework presents a four-stage process to transform multi-modal inputs into immersive 3D worlds: (1) initializing the world via Panorama Generation, (2) deriving exploration camera paths through Trajectory Planning, (3) expanding the world observations via memory-driven World Expansion, and (4) constructing the final 3DGS assets using World Composition. The core model/algorithm used in each stage is denoted at the bottom*

### 四阶段生成管线

世界生成遵循以下级联流程：

1. **全景生成（Panorama Generation）**  
   由 **HY‑Pano 2.0** 负责。该模块将文本或单视图图像转换为高保真 360° 全景图，作为世界的初始化表示。其核心改进在于采用基于 MMDiT 的隐式自适应映射替代传统显式几何扭曲，结合圆形填充与像素混合消除边界伪影（见 **Figure 3**）。

![[assets/figures/papers/HY-World_2.0_A_Multi-Modal_World_Model_for_Reconstructing_Generating_and_Simulat_6a92b680015f/figures/005_Figure_3.jpg]]
*Figure 3: Overview of the panorama generation architecture of HY-Pano 2.0. The Left side shows the framework pipeline of panorama generation, while the right side illustrates the circle padding (latent space) and the pixel blending (pixel space) for seamless panorama generation. Figure 4: The initial scene parsing for trajectory planning. We obtain panoramic point clouds, meshes, semantic masks, and NavMesh via several pioneering works [67, 10, 23, 50]*

2. **轨迹规划（Trajectory Planning）**  
   由 **WorldNav** 负责。系统首先对全景图进行几何与语义解析——通过 MoGe2 构建全局全景点云 $\mathbf{P}_{\text{pan}}$，并利用视觉‑语言模型分割天空区域、去除深度不连续点（见 **Figure 4**）。在此基础上，WorldNav 设计五类启发式轨迹模式（规则环绕、重建感知、语义附着、空中环绕、空中漫游），为后续世界扩展生成信息量最大且无碰撞的相机路径（见 **Figure 5** 与 **Table 1**）。

3. **世界扩展（World Expansion）**  
   由 **WorldStereo 2.0** 负责。这是一个基于关键帧的相机控制视频扩散模型，在纯空间 Keyframe‑VAE 潜空间中对每条规划轨迹生成多视图序列。为确保多轨迹间的一致性，模型集成了两种记忆机制：**Global‑Geometric Memory（GGM）** 提供全景点云引导的全局几何记忆，**Spatial‑Stereo Memory++（SSM++）** 通过检索与空间拼接实现细粒度外观一致性（见 **Figure 7**）。三阶段训练策略（相机控制 → 记忆一致性 → DMD 蒸馏）逐步赋予模型精确的可控性与快速推理能力。

![[assets/figures/papers/HY-World_2.0_A_Multi-Modal_World_Model_for_Reconstructing_Generating_and_Simulat_6a92b680015f/figures/009_Figure_7.jpg]]
*Figure 7: Overall pipeline of WorldStereo 2.0. (a) The main Video Diffusion Transformer (DiT) branch is enhanced by the retrieval-based improved Spatial-Stereo Memory (SSM++) for fine-grained consistency. (b) The camera control branch is guided by the panoramic point cloud, serving as Global-Geometric Memory (GGM) to confirm precise camera trajectory following and geometry-aware consistency. Here, we omit the VAE encoding/decoding for simplicity*

4. **世界合成（World Composition）**  
   将生成的关键帧与初始全景融合为可导航的 3D 表示。具体包括：利用 **WorldMirror 2.0** 估计各关键帧的深度图，通过线性对齐将其注册到全景点云坐标系（见 **Figure 14**）；基于对齐后的点云初始化 3DGS，并采用定制优化策略——仅优化视角无关 RGB、限制天空区域增长、集成 **MaskGaussian** 剪枝——在保持渲染质量的同时将高斯数量压缩 73.7%（PSNR 仅下降 0.14 dB）。

### 重建分支

除生成管线外，HY‑World 2.0 升级了前馈重建模型 **WorldMirror 2.0**。该模型以多视图图像（可附带相机位姿、内参、深度图等先验）为输入，统一预测稠密点云、深度图、法线图、相机参数及 3D 高斯原语（见 **Figure 12**）。相比 1.0 版本，关键改进包括：

![[assets/figures/papers/HY-World_2.0_A_Multi-Modal_World_Model_for_Reconstructing_Generating_and_Simulat_6a92b680015f/figures/015_Figure_12.jpg]]
*Figure 12: Model architecture of WorldMirror 2.0, which is a unified feed-forward model that takes multi-view images with optional geometric priors (camera poses, intrinsics, depth maps) as input, and simultaneously predicts dense point clouds, depth maps, surface normals, camera parameters, and 3DGS through a shared Transformer backbone with task-specific DPT decoder heads*

- **归一化位置编码**：将图像块坐标映射至固定 $[-1,1]$ 范围，实现分辨率无关的推理能力（见 Eq. (4)）。
- **深度‑法线耦合损失** $\mathcal{L}_{\mathrm{d2n}}$：通过预测深度反投影计算法线，与真值法线进行角度误差监督，增强几何一致性（见 Eq. (7)）。
- **深度掩码预测头**与**多阶段课程学习**：提升对不可见区域的几何推理鲁棒性。

### 渲染与交互

最终，所有 3D 表示通过 **WorldLens** 渲染平台呈现，该平台支持自动 IBL 光照、碰撞检测与角色交互，实现沉浸式的世界探索体验。

### 输入输出流总结

| 输入模态 | 处理分支 | 输出 |
|---------|---------|------|
| 文本 / 单视图图像 | 四阶段生成管线 | 可导航 3DGS 场景 |
| 多视图图像 / 视频 | WorldMirror 2.0 前馈重建 | 点云、深度、法线、相机位姿、3DGS |

整个管线将扩散模型的生成式先验与前馈重建的几何严谨性有机融合：全景生成与视频扩散提供丰富的动态先验以扩展可探索范围，而 WorldMirror 2.0 的深度对齐与归一化编码则确保多视图输入的几何精确性。这一设计直接回应了现有 3D 世界模型在生成与重建任务间长期割裂的瓶颈——生成方法难以保持几何一致性，重建方法缺乏对未见区域的生成式先验。

HY-World 2.0 的四阶段管线由六个核心模块构成：**HY-Pano 2.0**（全景生成）、**WorldNav**（轨迹规划）、**WorldStereo 2.0**（世界扩展）、**WorldMirror 2.0**（前馈重建）、**World Composition**（世界融合）与 **WorldLens**（渲染平台）。各模块通过关键公式将扩散先验与几何约束耦合，以下逐一剖析。

### HY-Pano 2.0：隐式全景映射

HY-Pano 2.0 摒弃了 HY-Pano 1.0 的显式几何扭曲（explicit geometric warping），转而采用基于多模态扩散 Transformer（MMDiT）的隐式自适应映射。其核心创新在于**圆形填充**（circle padding）与**像素混合**（pixel blending）两个后处理步骤：在潜空间中对全景图左右边界进行圆形填充以消除接缝伪影，再在像素空间通过加权混合进一步平滑过渡（见 Figure 3）。消融实验表明，该隐式映射策略显著优于显式几何扭曲，彻底消除了投影畸变（Sec. 3.2）。

### WorldStereo 2.0：关键帧潜空间与几何记忆

WorldStereo 2.0 是连接视频扩散模型与 3D 重建的核心桥梁，其关键设计包括：

**关键帧 VAE（Keyframe-VAE）**：与 WorldStereo 1.0 使用的时空 Video-VAE 不同，WorldStereo 2.0 采用纯空间压缩的 Keyframe-VAE（见 Figure 9），在保留高频细节的同时避免运动模糊。Figure 8 的定性结果表明，在大视角变化下 Keyframe-VAE 显著提升了生成帧的保真度，同时保持相机可控性（Tab. 7，RotErr 从 0.758 降至 0.492）。

**全局几何记忆（GGM）**：GGM 将全景参考点云 $\mathbf{P}^{ref}$ 与从新视角采样的点云 $\hat{\mathbf{P}}$ 拼接，构造扩展全局点云：

$$\mathbf{P}^{glo} = [\mathbf{P}^{ref}, \hat{\mathbf{P}}] \in \mathbb{R}^{(N + \hat{N}) \times 3}$$

其中 $N$ 为参考点云的点数，$\hat{N}$ 为采样点数。该全局点云通过相机控制分支注入 DiT，为所有生成轨迹提供统一的几何参照（Eq. (2)，Sec. 5.2）。

**增强型空间立体记忆（SSM++）**：SSM++ 采用空间拼接策略（而非时间拼接）将检索到的参考视图与目标帧拼接，配合修改后的 RoPE 位置编码（见 Figure 11），实现细粒度的多轨迹一致性。消融实验（Tab. 8）证实，同时集成 GGM 和 SSM++ 大幅改善光度质量与跨轨迹一致性，且空间拼接远优于时间拼接。

**DMD 蒸馏**：为加速推理，WorldStereo 2.0 通过分布匹配蒸馏（Distribution Matching Distillation）将模型蒸馏至少量步数的学生模型，其梯度为：

$$\nabla \mathcal{L}_{\mathrm{DMD}} = -\mathbb{E}_{t} \left( \int \left( s_{\mathrm{real}}(x_t, t) - s_{\mathrm{fake}}(x_t, t) \right) \frac{dx_t}{d\theta} dz \right)$$

其中 $s_{\mathrm{real}}$ 和 $s_{\mathrm{fake}}$ 分别为真实分布与生成分布的得分函数（Sec. 5.3）。Tab. 8 表明 DMD 蒸馏在保持相机控制的同时略微提升了光度和一致性指标。

### WorldMirror 2.0：分辨率无关的前馈重建

WorldMirror 2.0 对 WorldMirror 1.0 进行了三项关键升级（对比见 Table 3）：

**归一化位置编码**：将图像块网格坐标映射到固定 $[-1, 1]$ 范围，实现分辨率无关的位置编码：

$$\hat{x}_i = \frac{2i+1}{H_p} - 1, \quad \hat{y}_j = \frac{2j+1}{W_p} - 1$$

其中 $H_p$、$W_p$ 分别为高度和宽度方向的块数（Eq. (4)，Sec. 6.2）。Figure 13 的分析表明，归一化 RoPE 在不同分辨率间保持高于 0.95 的跨分辨率一致性。多分辨率测试（Fig. 26, Tab. 11）进一步证实，WorldMirror 1.0 在高分辨率下性能严重退化，而 WorldMirror 2.0 跨分辨率保持甚至提升重建质量。

**深度-法线耦合损失**：通过预测深度反投影计算法线后与真值法线之间的角度误差：

$$\mathcal{L}_{\mathrm{d2n}} = \frac{1}{|\mathcal{V}|} \sum_{x \in \mathcal{V}} \operatorname{arccos}\left(\frac{\tilde{\mathbf{N}}_i(x) \cdot \hat{\mathbf{N}}_i(x)}{\|\tilde{\mathbf{N}}_i(x)\| \|\hat{\mathbf{N}}_i(x)\|}\right)$$

其中 $\tilde{\mathbf{N}}_i(x)$ 为由预测深度反投影得到的法线，$\hat{\mathbf{N}}_i(x)$ 为真值法线，$\mathcal{V}$ 为有效像素集合（Eq. (7)，Sec. 6.2）。该损失将深度估计与表面法线预测显式耦合，增强了重建的几何一致性。

### World Composition：深度对齐与 3DGS 优化

**点云扭曲**：在将生成的关键帧与全景点云对齐时，通过相机旋转 $\mathbf{R}_i^{cw}$、深度 $\mathrm{D}(x)$ 和内参 $\mathbf{K}_i^{-1}$ 将参考视图点云扭曲至目标视图：

$$\mathbf{P}_i^{tar}(x) \simeq \mathbf{R}_i^{cw} \mathrm{D}(x) \mathbf{K}_i^{-1} \hat{x}$$

其中 $\hat{x}$ 为参考视图的像素坐标（Eq. (1)，Sec. 7.1）。

**3DGS 训练总损失**：融合光度、几何、正则化与掩码稀疏性约束：

$$\mathcal{L}_{\mathrm{GS}} = \mathcal{L}_{\mathrm{color}} + \mathcal{L}_{\mathrm{geo}} + \mathcal{L}_{\mathrm{reg}} + \mathcal{L}_{\mathrm{mask}}$$

其中掩码稀疏正则化 $\mathcal{L}_{\mathrm{mask}} = \lambda_m \left( \frac{1}{N} \sum_{k=1}^{N} M_k \right)^2$ 鼓励高斯掩码稀疏性，配合 MaskGaussian 剪枝（Sec. 7.2）。Tab. 9 的消融表明，该策略将高斯数量从 5.254M 降至 1.383M（减少 73.7%），PSNR 仅下降 0.14 dB；同时限制天空区域增长防止浮点伪影。

### 模块间因果链路

上述模块通过信息流形成闭环：HY-Pano 2.0 提供全景初始化 → WorldNav 基于场景解析规划探索轨迹 → WorldStereo 2.0 利用 GGM 和 SSM++ 沿轨迹生成几何一致的关键帧 → WorldMirror 2.0 从关键帧前馈预测点云、深度和法线 → World Composition 通过点云扭曲和深度对齐将生成内容融合为统一的 3DGS 表示 → WorldLens 提供实时渲染与交互。这一管线将视频扩散模型的生成式先验与前馈重建的几何严谨性有机融合，在同一框架内统一了生成与重建。

## 实验与关键发现

### 核心性能全景

HY‑World 2.0 在多项基准上达到开源方法中的最优性能，与闭源模型 **Marble**（World Labs, 2025）相当。这一结论来源于论文摘要声明的整体定位，置信度较高（0.95），但需注意与 Marble 的直接比较仅限于使用相同全景输入的定性展示（Figure 23–24），Marble 内部算法细节未知，定量比较的公平性受限。

管线各模块的量化优势分别体现在全景生成、相机控制视频生成、单视图三维重建以及前馈多模态重建四个维度，下文逐一展开。

### 全景生成：文本与图像条件下的双模态领先

HY‑Pano 2.0 在文本到全景（T2P）和图像到全景（I2P）两项任务上均取得最佳指标。Table 4 报告 T2P 的 CLIP‑T 达到 0.258，I2P 的 CLIP‑I 达到 0.844，两项均优于对比基线。这一性能提升的核心机制在于用 MMDiT 的隐式自适应映射替代 HY‑Pano 1.0 的显式几何扭曲，从根本上消除了投影畸变和边界伪影（Sec. 3.2 消融，置信度 0.9）。Figure 16–18 的定性结果进一步印证了生成全景的视觉保真度。

### 相机控制视频生成：Keyframe‑VAE 与记忆机制的双重增益

WorldStereo 2.0 在相机控制精度上相比基线 **WorldStereo**（Tencent Hunyuan 3D Team, 2026）有显著提升：旋转误差 RotErr 从 0.758 降至 0.492（Table 7，置信度 0.95）。这一改进可归因于两个关键设计：

1. **Keyframe‑VAE 替代时空 Video‑VAE**：纯空间压缩保留高频细节，在大视角变化下显著提升生成帧的保真度，同时保持相机可控性（Fig. 8, Tab. 7，置信度 0.9）。
2. **记忆机制消融**：同时集成 GGM 和 SSM++ 大幅改善光度质量与多轨迹一致性；SSM++ 的空间拼接设计远优于时间拼接方案（Table 8，置信度 0.95）。

此外，域适配阶段冻结交叉注意力和 FFN 层在视觉质量与相机控制精度之间取得了最佳用户偏好（Sec. 8.1.3, Tab. 7），而 DMD 蒸馏在保持相机控制的同时略微提升了光度和一致性指标（Table 8）。

### 单视图三维重建：生成式先验驱动的几何精度

在 Tanks‑and‑Temples 数据集上，WorldStereo 2.0 的点云 F1 分数达到 41.43，优于所有视频生成方法（Table 5，置信度 0.98）。这验证了将视频扩散模型的生成式先验注入三维重建管线的有效性——Keyframe‑VAE 保留的几何细节和记忆机制维持的多视角一致性，共同支撑了从单视图到稠密点云的可靠推理。

### 前馈多模态重建：跨分辨率鲁棒性与精度跃升

WorldMirror 2.0 相比 WorldMirror 1.0 在多个基准上实现了系统性改进。在 7‑Scenes 数据集上，中等分辨率下的点图精度误差从 0.043 降至 0.033（Table 11，置信度 0.95）。更关键的是跨分辨率稳定性：WorldMirror 1.0 在高分辨率下性能严重退化，而 WorldMirror 2.0 借助归一化位置编码（Eq. 4）在从低到高的各分辨率下保持甚至提升重建质量（Fig. 26, Tab. 11，置信度 0.95）。归一化 RoPE 的跨分辨率一致性超过 0.95（Fig. 13），为多尺度部署提供了可靠保证。

相机姿态估计方面，7‑Scenes 上的 AUC@30 提升超过 20 个点（Sec. 8.2.1），深度‑法线耦合损失（Eq. 7）和多阶段课程学习共同贡献了这一增益。Table 12–13 进一步覆盖了深度估计、新视角合成和表面法线估计的结果，WorldMirror 2.0 在 DTU、NRGBD、ScanNet、NYUv2 和 iBims‑1 上均表现出竞争力。

### 3DGS 优化：效率与质量的精细权衡

MaskGaussian 剪枝在 World Composition 阶段解决了生成场景中高斯数量膨胀的问题：高斯数量从 5.254M 降至 1.383M，减少 73.7%，而 PSNR 仅下降 0.14 dB（Table 9，置信度 0.95）。同时，限制天空区域的适应性稠密化（† 标记配置）有效防止了天空浮点伪影。Table 9 的消融覆盖了视角无关 RGB、天空限制和掩码稀疏正则化（Eq. mask）的独立贡献，为实际部署提供了明确的配置指导。

### 轨迹规划消融：渐进式世界扩展的必要性

Figure 19 的定性消融揭示了轨迹规划对世界完整性的关键作用。仅依赖全景视图会导致严重伪影和不完整几何；依次整合 regular、surrounding & reconstruction、wandering 和 aerial 模式的生成视图，才能逐步补全场景结构。Table 1 给出了各模式的详细参数（最大轨迹数、是否附着物体、是否迭代），为不同场景类型下的轨迹策略选择提供了参考。

![[assets/figures/papers/HY-World_2.0_A_Multi-Modal_World_Model_for_Reconstructing_Generating_and_Simulat_6a92b680015f/figures/007_Table_1.jpg]]
*Table 1: Trajectory details of WorldNav. The aerial category comprises both surrounding and wandering trajectories. Note that the maximum number for surrounding and reconstruct-aware trajectories is determined by the count of object segments detected within the panorama*

### 推理效率与失败模式

完整世界生成在 NVIDIA H20 GPU 上耗时约 10 分钟（Table 10），各模块的运行时明细已给出，便于定位优化瓶颈。管线的已知局限包括：

- **深度对齐异常检测**可能将整条视频标记为离群值，导致该轨迹的世界扩展完全失效。
- **天空分割**（依赖 SAM3）在阴天或夜间场景可能出错，影响深度对齐的可靠性。
- 管线依赖多个大规模预训练模型（视频扩散、单目深度、语义分割），整体鲁棒性受限于这些组件的性能。

这些失败模式提示，在复杂光照或非典型场景下，端到端生成质量可能出现退化，实际部署需进行场景适配评估。

![[assets/figures/papers/HY-World_2.0_A_Multi-Modal_World_Model_for_Reconstructing_Generating_and_Simulat_6a92b680015f/figures/006_Figure_5.jpg]]
*Figure 5: Illustration of five modes of trajectories planned in WorldNav. Some trajectories are omitted for a simplified visualization*

## 定位与知识库关联

### 1. 任务定位与核心瓶颈

HY-World 2.0 定位为**首个统一“生成”与“重建”的开源多模态3D世界模型**，其核心动机源于当前领域的结构性割裂：生成式方法（如基于扩散模型的场景合成）难以保持严格的几何一致性，而重建式方法（如前馈多视图立体匹配）缺乏对未见区域的生成式先验。论文明确指出，开源社区缺少同时具备两种能力的系统化方案，而闭源模型 **Marble**（World Labs, 2025）虽已展示此类统一能力，但其技术细节不可获取。

HY-World 2.0 的因果调节变量在于：通过四阶段管线将**视频扩散模型的生成式先验**与**前馈多模态重建的几何精确性**相融合——WorldStereo 2.0 在关键帧VAE潜空间中注入全局几何记忆（GGM）和空间立体记忆（SSM++），WorldMirror 2.0 通过归一化位置编码和深度-法线耦合损失保证跨分辨率的几何保真度——从而在同一框架内弥合生成与重建的鸿沟。

### 2. 与先前版本及基线的演化关系

#### 2.1 相对于 HY-World 1.0 的改进

HY-World 2.0 是对 **HY-World 1.0**（Team HunyuanWorld, arXiv 2025）的全面升级，体现在管线的每个阶段：

- **全景生成**：从 HY-Pano 1.0 的显式几何扭曲升级为基于 MMDiT 的隐式自适应映射，配合圆形填充与像素混合，消除投影畸变和边界伪影（Sec. 3.2）。
- **视频生成潜空间**：从 WorldStereo 的时空 Video-VAE 切换为纯空间 Keyframe-VAE，保留高频细节并减少大视角变化下的运动模糊（Sec. 5.1）。
- **记忆机制**：从独立记忆分支升级为直接集成至 DiT 主分支的 Global-Geometric Memory（GGM）与增强型 Spatial-Stereo Memory（SSM++），实现多轨迹一致性世界扩展（Sec. 5.2）。
- **重建模型**：WorldMirror 1.0 的绝对位置编码被替换为归一化位置编码（Eq. 4），新增深度-法线耦合损失（Eq. 7）、深度掩码预测头和多阶段课程学习（Sec. 6.2）。
- **3DGS优化**：从标准3DGS优化（含球谐函数）简化为仅优化视角无关RGB，限制天空区域增长，并集成 MaskGaussian 剪枝（Sec. 7.2）。

#### 2.2 相对于相关基线的定位

| 基线方法 | 角色与关系 | 关键差异 |
|---------|-----------|---------|
| **WorldStereo**（Tencent Hunyuan 3D Team, 2026） | 相机引导视频生成基线 | HY-World 2.0 将其升级为 WorldStereo 2.0：Keyframe-VAE 替代 Video-VAE，新增 GGM/SSM++ 记忆机制，并引入 DMD 蒸馏加速推理 |
| **MapAnything**（Keetha et al., arXiv 2025） | 前馈3D重建基线 | WorldMirror 2.0 在点云重建精度上显著超越，且在跨分辨率测试中保持稳定（MapAnything 未针对生成式世界任务优化） |
| **DepthAnything3**（Lin et al., arXiv 2025） | 前馈深度/点云重建基线 | 同上，WorldMirror 2.0 通过归一化位置编码和深度-法线耦合损失在高分辨率下优势明显 |
| **Marble**（World Labs, 2025） | 闭源商业世界模型，作为整体性能上界 | HY-World 2.0 在多项基准上达到与 Marble 相当的性能，但 Marble 内部算法未知，比较仅基于相同全景输入 |

### 3. 适用边界与失效模式

#### 3.1 已知局限

论文明确指出的失效模式包括：

1. **深度对齐的离群值检测脆弱性**：当整段生成视频被 WorldMirror 2.0 检测为深度对齐离群值时，该轨迹的世界扩展完全失效，目前缺乏自适应恢复机制。
2. **天空分割的鲁棒性不足**：依赖 SAM3 的天空掩码在阴天或夜间场景可能出错，导致深度对齐将天空区域错误地纳入几何优化，产生浮空伪影。
3. **组件级联的鲁棒性上限**：管线依赖多个大规模预训练模型（视频扩散模型、单目深度估计 MoGe2、语义分割等），整体鲁棒性受限于这些组件的性能边界，任一组件失效可能导致级联错误。
4. **推理延迟**：端到端世界生成耗时约10分钟（NVIDIA H20 GPU），虽已通过 DMD 蒸馏和 MaskGaussian 剪枝优化，但离实时交互仍有显著距离。

#### 3.2 适用边界推断

基于方法设计，以下边界需注意：

- **场景类型**：WorldNav 的轨迹规划依赖语义分割和 NavMesh，对室内外场景均可处理，但高度非结构化或动态场景（如拥挤街道、水体反射）可能超出当前能力。
- **输入模态**：生成模式支持文本或单视图图像输入，重建模式支持多视图图像或视频；不支持深度传感器、LiDAR 等主动深度输入的直接融合。
- **几何精度**：WorldMirror 2.0 在 7-Scenes 上点图精度误差降至 0.033，但这是基于前馈预测的结果，对于需要毫米级精度的工业应用可能不足。

### 4. 开放问题与未来方向

1. **自适应离群值恢复**：当整段生成视频被检测为深度对齐离群值时，如何设计自适应恢复策略（如回退到纯生成式先验或触发重新采样）是提升管线鲁棒性的关键。
2. **光照鲁棒的天空处理**：SAM3 天空掩码在复杂光照条件下的稳定性改进，或探索不依赖显式天空分割的深度对齐策略。
3. **实时交互式世界生成**：当前约10分钟的延迟限制了交互式应用，进一步降低管线延迟（如模型量化、更激进的蒸馏、异步管线化）是工程化方向。
4. **轨迹规划的自主学习**：当前 WorldNav 依赖五种启发式轨迹模式，能否将轨迹规划与强化学习结合，以自监督方式发现最优探索路径，是提升世界覆盖效率的潜在方向。
5. **多模态输入的深度融合**：当前重建模式未充分利用生成式先验（反之亦然），探索生成与重建的更深层次耦合（如用生成先验填补重建缺失区域）可能进一步提升统一框架的能力边界。

## 原文 PDF

![[paperPDFs/arxiv_2025/HY_World_2_0_A_Multi_Modal_World_Model_for_Reconstructing_Generating_and_Simulating_3D_Worlds.pdf]]
