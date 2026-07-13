---
title: "ShapeGen4D: Towards High Quality 4D Shape Generation from Videos"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ShapeGen4D_Towards_High_Quality_4D_Shape_Generation_from_Videos_3a1c93476b93.pdf
project_link: "https://shapegen4d.github.io/"
code_link: null
aliases:
- ShapeGen4D
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过微调预训练3D生成模型（Step1X-3D/Hunyuan3D），插入时空注意力层、设计时间对齐的潜在编码（利用动画扭曲查询点）以及跨帧噪声共享，实现从单帧到多帧的直接推理，无需独立变形网络。
primary_logic: 利用大规模3D数据预训练模型的强泛化能力，将动态网格序列的生成视为帧间条件依赖的3D生成问题；通过时间对齐的潜在编码消除帧间抖动，共享噪声抑制姿态偏移，使扩散模型能隐式学习复杂运动模式，从而原生支持拓扑变化。
claims:
- 在Objaverse测试集上，ShapeGen4D（基于Step1X-3D）的Chamfer距离为0.1220，较基线Step1X-3D（0.1356）显著降低，同时IoU和F-Score均有提升。
- 去除时间对齐潜在编码后，Chamfer距离从0.1096升至0.1348，且观看时抖动明显增加。
- 使用共享噪声相比独立噪声大幅减少帧间闪烁和形状伪影。
- 方法能处理拓扑变化（如物体融合、撕裂、生长等），而基于变形的方法无法胜任。
---

# ShapeGen4D: Towards High Quality 4D Shape Generation from Videos

> [!tip] 核心洞察
> 利用大规模3D数据预训练模型的强泛化能力，将动态网格序列的生成视为帧间条件依赖的3D生成问题；通过时间对齐的潜在编码消除帧间抖动，共享噪声抑制姿态偏移，使扩散模型能隐式学习复杂运动模式，从而原生支持拓扑变化。

| 字段 | 内容 |
|------|------|
| 中文题名 | ShapeGen4D：从视频生成高质量4D形状 |
| 英文题名 | ShapeGen4D: Towards High Quality 4D Shape Generation from Videos |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=r9AJisFLLo) · [Project](https://shapegen4d.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ShapeGen4D |
| Dataset | Held-out Objaverse test set |

> [!tip] 效果简介
> - Held-out Objaverse test set 上，Chamfer↓ 0.1220 vs 0.1356 (Step1X-3D) (-0.0136)；IoU↑ 0.3276 vs 0.3033 (Step1X-3D) (+0.0243)；F-Score↑ 0.2934 vs 0.2617 (Step1X-3D) (+0.0317)。

## 概要

从单目视频中重建动态三维物体是计算机视觉的核心挑战之一。现有4D生成方法面临三重瓶颈：基于分数蒸馏采样（SDS）的优化过程脆弱且耗时；多视图重建方法在多阶段流水线中累积误差，难以保持时空一致性；基于变形场的方法则严重依赖4D训练数据，泛化能力弱，且无法处理拓扑变化——如物体融合、撕裂或生长。这些方法往往将预训练的3D生成模型视为黑盒，未能充分利用其蕴含的强泛化先验。

**ShapeGen4D** 提出了一种原生视频到4D形状生成的框架，直接端到端地从单目视频合成动态网格序列。其核心洞察在于：将动态网格序列的生成重新定义为帧间条件依赖的3D生成问题，通过微调预训练的3D生成模型（如Step1X-3D或Hunyuan3D-2.1），而非外挂独立变形网络，使扩散模型能够隐式学习复杂运动模式，从而原生支持拓扑变化。

方法的关键因果机制体现在三个递进的架构改进上：**时间对齐的潜在编码**——通过动画扭曲将第一帧的查询点传播到后续帧，消除帧间潜在表示的抖动；**时空注意力层**——在冻结的3D基座块之间插入可学习的跨帧注意力，捕获时序依赖关系；**跨帧噪声共享**——在训练和推理阶段对所有帧施加相同的噪声样本，抑制基础模型固有的姿态偏移。这三项设计协同作用，使模型在保留预训练3D先验的同时，获得了对非刚性运动和体积变化的建模能力。

在Objaverse测试集上，ShapeGen4D（基于Step1X-3D）的Chamfer距离达到0.1220，较基线的0.1356显著降低，IoU和F-Score分别提升至0.3276和0.2934。消融实验进一步验证了各组件的关键作用：去除时间对齐潜在编码后Chamfer距离升至0.1348，序列抖动明显增加；使用独立噪声会导致帧间闪烁和形状伪影。方法能够处理包括部件涌现、撕裂、生长、融合、分裂、形态变换乃至物体破碎在内的多种拓扑变化场景，这是基于变形的方法所无法胜任的。

本报告后续章节将依次展开相关工作定位、方法细节、实验分析、消融研究以及局限与展望，为读者提供从问题动机到技术实现的完整图景。

### 问题背景：从视频生成4D内容的需求

从单目视频重建动态3D内容（4D重建）是计算机视觉与图形学的核心挑战之一，其应用涵盖AR/VR、影视制作和数字孪生等场景。传统4D重建方法通常依赖多视图输入或深度传感器，而近年来，随着生成模型的快速发展，从单目视频直接生成动态3D资产（video-to-4D generation）成为新兴方向，旨在以更低的数据采集成本获得可编辑、可渲染的动态网格序列。

### 现有方法的瓶颈

当前4D生成方法主要沿三条技术路线发展，但各自存在根本性局限：

**1. 基于优化的方法（SDS-based）**
以**DreamMesh4D**（Li et al., 2024c）为代表，通过分数蒸馏采样（Score Distillation Sampling）逐帧优化网格。这类方法的脆弱性在于：SDS优化过程本身不稳定，容易产生几何噪声和帧间不一致，且优化耗时较长，难以扩展到长序列。

**2. 多阶段重建方法（Two-stage）**
以**V2M4**（Chen et al., 2025）为代表，先逐帧生成独立网格，再通过后处理优化时间一致性。这种流水线的根本缺陷在于多阶段累计误差：逐帧生成阶段缺乏跨帧约束，导致帧间几何拓扑不一致，后续优化难以完全纠正，尤其在非刚性运动和体积变化场景下表现不佳。

**3. 基于变形的方法（Deformation-based）**
以**GVFD**（Zhang et al., 2025）为代表，通过在预训练3D模型外附加独立变形网络来驱动网格运动。这类方法对4D训练数据依赖严重，泛化能力弱，且变形网络的表达能力受限于连续映射假设——**无法处理拓扑变化**（如物体融合、撕裂、生长、破碎等），因为拓扑变化需要离散的结构改变，无法通过连续变形场建模。

### 关键瓶颈总结

上述方法的共同症结在于：**未能充分继承预训练3D模型的先验知识**。大规模3D生成模型（如Step1X-3D、Hunyuan3D）已展现出强大的单帧几何生成能力，但现有4D方法要么将其作为黑盒逐帧调用（如V2M4），要么在其外部嫁接变形模块（如GVFD），而非在模型内部建立帧间依赖。这导致：
- 帧间几何一致性弱，抖动和闪烁现象严重；
- 对非刚性运动、体积变化的建模能力不足；
- 无法原生支持拓扑变化。

### 本文动机

针对上述瓶颈，本文提出**ShapeGen4D**——首个原生视频到4D网格生成框架。核心思路是：**将动态网格序列的生成重新定义为帧间条件依赖的3D生成问题**，通过微调预训练3D生成模型，在其内部插入时空建模能力，使扩散模型能隐式学习复杂运动模式，而非依赖外部变形网络。这一设计旨在同时解决三个关键问题：
1. **帧间一致性**：通过时间对齐的潜在编码和跨帧噪声共享消除抖动；
2. **拓扑变化**：摆脱变形场的连续性约束，使模型能原生处理融合、撕裂等离散结构变化；
3. **泛化能力**：充分利用大规模3D预训练先验，降低对4D训练数据的依赖。

## 核心方法与创新机理

ShapeGen4D 的核心创新在于**将动态网格序列生成重新定义为帧间条件依赖的3D生成问题**，并通过对预训练3D生成模型的架构微调实现这一范式转换。区别于现有4D生成方法的优化脆弱性（SDS）、多阶段累计误差（多视图重建）或对变形网络的依赖，该方法直接继承大规模3D预训练模型的强泛化能力，隐式学习复杂运动模式，从而原生支持拓扑变化（如物体融合、撕裂、生长等，见 Figure 7）。

### 关键架构变更

相对于基座3D生成模型（**Step1X-3D** (Li et al., 2025a) 和 **Hunyuan3D-2.1** (TencentHunyuan3DTeam, 2025a)），ShapeGen4D 引入了三个核心 changed slots：

**1. 时间对齐的潜在编码（Latent Encoding Query Points）**

基座模型中，每帧独立通过最远点采样（FPS）选取查询点，导致跨帧潜在编码对应不同的表面位置，产生时间抖动。ShapeGen4D 改为：仅在第一帧采样查询点 $\mathcal{Q}_1$，随后利用动画的变形函数 $w_t$ 将其传播到后续帧，得到时间对齐的查询点集 $\mathcal{Q}_t = w_t(\mathcal{Q}_1)$。这确保了各帧潜在编码对应相同的表面点，显著降低了帧间潜在表示的 $L_2$ 差异（Figure 3(c)）。消融实验表明，去除该对齐后 Chamfer 距离从 0.1096 升至 0.1348，且序列抖动明显增加（Table 3）。

**2. 时空注意力层（Attention Layers）**

基座模型仅使用冻结的单帧内自注意力层。ShapeGen4D 在冻结的基座块之间插入可学习的时空注意力层，对跨帧隐藏状态执行联合自注意力（Figure 2(b)）。这使模型能捕获帧间依赖，在去噪过程中强制时间一致性。消融显示，若替换为仅含时间维度的1D注意力（无帧内交互），会导致灾难性失败，Chamfer 距离飙升至 0.2118（Table 3）。

**3. 跨帧噪声共享（Noise Sampling）**

基座模型为每帧独立采样高斯噪声。ShapeGen4D 改为所有帧共享同一噪声样本。由于基座3D模型生成物体时对输入视角不敏感，常导致序列中姿态偏移（如 Figure 4 中的河马示例），共享噪声能抑制这种跨帧姿态变化，减少闪烁和形状伪影。消融实验证实共享噪声相比独立噪声显著改善了时间平滑性（Table 3, Figure 4）。

### 范式优势

上述三个 changed slots 协同作用，使 ShapeGen4D 区别于两类主流基线：
- **两阶段方法**（如 **V2M4** (Chen et al., 2025)）：逐帧生成网格后再优化时间一致性，累计误差大；
- **基于变形的方法**（如 **GVFD** (Zhang et al., 2025)）：依赖独立变形网络，无法处理拓扑变化。

ShapeGen4D 通过微调而非黑盒扩展的方式，使扩散模型隐式学习运动模式，无需显式变形建模即可处理拓扑变化（Figure 7）。在 Objaverse 测试集上，基于 Step1X-3D 的 ShapeGen4D 相比基座模型 Chamfer 距离降低 10%（0.1356 → 0.1220），IoU 和 F-Score 分别提升 8% 和 12%（Table 1）。

ShapeGen4D 提出了一种端到端的视频到4D形状生成框架，其核心思想是将动态网格序列的生成视为帧间条件依赖的3D生成问题。该方法并非在预训练3D模型之上外挂独立的变形网络，而是直接微调3D生成模型的内部架构，使其原生支持时间维度的建模。

### 输入输出流

框架接收一段单目视频作为输入，输出一个动态的3D网格序列。整个流程由五个核心模块串联构成：

1. **3D VAE 编码器**：将动态网格序列编码为时间对齐的潜在表示序列。
2. **时空扩散 Transformer**：以输入视频为条件，对噪声潜在表示进行逐步去噪，生成动态潜在序列。
3. **3D VAE 解码器**：将潜在序列解码为截断有符号距离场（TSDF），再通过 Marching Cubes 转换为网格序列。
4. **全局姿态配准**：将生成的规范空间网格与输入视频的相机姿态对齐，使重建结果与观测视角一致。
5. **全局纹理化**：通过拓扑一致性转换和纹理传播，为动态网格赋予跨帧一致的表面外观。

### 关键设计决策

框架的架构选择围绕一个核心洞察展开：**大规模3D数据预训练模型具备强泛化能力，将其扩展为4D生成模型时，关键在于建立帧间的条件依赖，而非设计独立的运动建模模块**。这一思路体现在三个关键设计上：

- **微调而非外挂**：与 **GVFD**（Zhang et al., 2025）等并行工作不同，ShapeGen4D 直接修改并微调预训练3D模型（如 Step1X-3D、Hunyuan3D-2.1）的内部结构，在冻结的基座块之间插入可学习的时空注意力层，使模型能联合处理所有帧的隐藏状态。
- **时间对齐的潜在编码**：第一帧采样查询点后，通过动画扭曲将其传播到后续帧，确保各帧的潜在编码对应相同的表面点，从源头抑制帧间抖动。
- **跨帧噪声共享**：在训练和推理时对所有帧施加相同的噪声样本，抑制因3D基座模型的视点无关性导致的姿态偏移和形状闪烁。

### 模块间依赖关系

编码器与解码器构成对称的3D VAE结构，其潜在空间是扩散模型的操作域。时空扩散 Transformer 是生成的核心引擎，它在潜在空间中完成从纯噪声到结构化动态表示的映射，其输出经解码器还原为几何序列。姿态配准和纹理化作为后处理步骤，依次作用于解码后的网格序列，最终产出可渲染的动态资产。这两个后处理模块独立于生成主干，使得几何质量和纹理质量可以分别评估和优化。

ShapeGen4D 的核心架构由三个紧密耦合的模块组成，共同实现从单目视频到动态网格序列的端到端生成。

### 3D VAE 编码器与时间对齐潜在表示

该方法建立在现有 3D 生成模型（**Step1X-3D** (Li et al., 2025a) 和 **Hunyuan3D** (TencentHunyuan3DTeam, 2025a)）的 VAE 架构之上。其关键创新在于将静态 3D 编码扩展为时间对齐的 4D 编码。

编码器通过交叉注意力机制，将子采样的查询点（query points）与稠密点云进行交互，从而将形状编码为潜在表示。对于动态网格序列，时间对齐的实现方式如下：

1. 从第一帧的点云中通过最远点采样（FPS）获取查询点集 $\mathcal{Q}_1$。
2. 利用动画序列提供的变形场 $w_t$，将第一帧的查询点扭曲传播到后续帧：

$$\mathcal{Q}_t = w_t(\mathcal{Q}_1)$$

其中 $\mathcal{Q}_t$ 表示第 $t$ 帧的查询点集。由于这些查询点对应相同的表面位置，编码器产生的潜在表示在时间维度上自然对齐。

这一设计的因果机制在于：对齐的潜在表示使相邻帧的潜在编码在相同 3D 位置上的 $L_2$ 差异显著减小（见 Figure 3），从源头抑制了帧间几何抖动。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_r9AJisFLLo/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of latents with and without aligning query points across frames in (a) and (b). In (c), we visualize the average normalized*

### 时空扩散 Transformer

该模块在冻结的预训练 3D 生成模型基础上进行微调，而非将其作为黑盒使用。具体改动包括两个关键槽位：

**时空注意力层**：在冻结的基座 Transformer 块之间插入可学习的时空注意力层。这些层对跨帧的隐藏状态进行联合自注意力，使模型在去噪过程中能够显式建模帧间依赖关系。与之对比，仅使用 1D 时间注意力（无帧内空间交互）会导致灾难性失败，Chamfer 距离飙升至 0.2118（Table 3）。

**共享噪声策略**：在训练和推理阶段，所有帧共享同一高斯噪声样本。这一设计的因果机制在于：基座 3D 模型倾向于生成与输入图像视点无关的任意朝向形状，这会在序列中引入姿态偏移。共享噪声迫使模型在各帧间保持一致的隐式姿态先验，从而减少闪烁和形状伪影（Figure 4）。

### 3D VAE 解码器与网格重建

解码器将去噪后的潜在序列映射为截断有符号距离场（TSDF），随后通过 Marching Cubes 算法转换为显式网格序列。由于编码阶段已实现时间对齐，解码器无需额外的时序一致性约束即可输出几何连贯的动态网格。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_r9AJisFLLo/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison of noise sharing. The base 3D model generates object shapes in arbitrary orientations agnostic to the input image viewpoint, often causing pose changes across a sequence (e.g. the hippo in the first row). We observe that sharing noise across frames reduces flickering and further improves shape quality in challenging cases such as the flag example*

## 实验与关键发现

### 主实验结果

ShapeGen4D 在 Objaverse 留出测试集上进行了几何质量评估，并与多个基线方法进行了对比。如表1所示，基于 Step1X-3D 的 ShapeGen4D 在所有几何指标上均优于其基础3D模型：Chamfer 距离从 0.1356 降至 0.1220，IoU 从 0.3033 提升至 0.3276，F-Score 从 0.2617 提升至 0.2934。这表明引入时空建模能力后，模型不仅保持了3D生成质量，还获得了显著的提升。当使用更强大的基础模型 Hunyuan3D-2.1 时，Chamfer 距离进一步降至 0.0827，IoU 达到 0.4155，F-Score 达到 0.3971，验证了框架对基础模型选择的灵活性。

在渲染质量评估（表2）中，ShapeGen4D 取得了 LPIPS 0.1359、CLIP 0.9009、FVD 796 和 DreamSim 0.0966 的成绩。需要注意的是，L4GM（Ren et al., 2024）因其预测视图与输入图像天然对齐而具有独特优势，其他方法需额外进行姿态配准，因此该指标并非完全公平对比。本方法的渲染质量还受独立纹理生成模块影响，可能未完全反映几何固有优势。

与两阶段方法 V2M4（Chen et al., 2025）相比，ShapeGen4D 实现了端到端的视频到4D形状生成，避免了逐帧重建与后优化的累计误差。与基于变形的并发工作 GVFD（Zhang et al., 2025）相比，本方法无需独立变形网络，能原生处理拓扑变化（图7），包括部件涌现、撕裂、生长、融合、分裂、变形和物体破碎等复杂场景。

### 消融实验

消融实验（表3）系统验证了三个核心设计的作用：

**时间对齐潜在编码**：去除时间对齐后，Chamfer 距离从 0.1096 升至 0.1348，IoU 和 F-Score 均显著下降。图3的潜变量分析显示，对齐后相邻帧间潜变量的平均归一化 L2 差异明显减小，表明帧间几何表示更加一致，消除了观看时的抖动现象。

**时空注意力设计**：将时空注意力替换为仅含时间维度的1D注意力（无帧内空间交互）导致灾难性失败，Chamfer 距离飙升至 0.2118。这证明帧内与帧间的联合建模对维持形状质量至关重要。

**共享噪声**：使用独立噪声时，帧间闪烁和形状伪影明显增加（图4）。共享噪声通过在所有帧上复制相同的噪声样本，有效抑制了基础3D模型固有的姿态偏移问题——基础模型生成的物体朝向与输入视角无关，容易在序列中产生姿态跳变。

**时间偏移去噪调度**：在去噪调度中引入时间偏移，将更多去噪步骤分配给中高噪声水平，显著提升了结果的稳定性。

此外，表4显示在原始非水密网格上采样查询点相比水密网格仅造成轻微的VAE重建质量下降（Chamfer 0.0369 vs 0.0246），图8的定性对比也表明两者在时间维度上产生视觉相似的几何，这验证了方法对非理想输入网格的鲁棒性。

### 长序列生成与局限性

为生成长度超过训练窗口（16帧）的序列，方法采用 MultiDiffusion 策略，通过重叠窗口扩展生成范围。表5显示，从16帧扩展到32帧时，Chamfer 距离仅从 0.0929 微增至 0.0934，图9的定性结果展示了视觉连贯且时间一致的几何。然而，远距离帧间一致性仍然有限。

方法的主要局限性包括：（1）依赖预训练3D模型的质量，可能受其偏差影响；（2）纹理生成为独立离线步骤，在严重遮挡区域仍可能出现不一致；（3）训练数据来自 Objaverse 合成动画数据集，对真实视频的泛化性待验证；（4）全局姿态配准假设第一帧姿态可估计，若第一帧遮挡严重可能失败。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_r9AJisFLLo/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison with baselines, evaluated on the held-out Objaverse test set*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_r9AJisFLLo/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison of rendering quality. L4GM has a unique advantage because its predictions are inherently aligned with the input image views, whereas other methods are not. Refer to Fig. 6 in the Appendix for visual comparisons*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_r9AJisFLLo/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison with baselines on the held-out Objaverse test set*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_r9AJisFLLo/figures/011_Figure_8.jpg]]
*Figure 8: Qualitative comparison of VAE reconstructions using query points from the watertight mesh versus the original mesh. The first column shows the input point clouds, while the second and third columns show the reconstructed surfaces when using KQV from the watertight mesh and Q directly from the original mesh. Both settings produce visually similar geometry across time*

## 定位与知识库关联

### 与现有4D生成方法的对比与继承

ShapeGen4D 位于视频到4D形状生成这一新兴任务的早期探索节点，其核心设计思路与现有方法形成了明确的差异化。当前4D生成方法可大致归为三类：基于优化的方法、基于变形的方法、以及前馈式方法。ShapeGen4D 通过“微调预训练3D模型+插入时空注意力”的范式，避开了这三类方法的固有瓶颈。

**基于优化的方法**以 **DreamMesh4D**（Li et al., 2024c）为代表，依赖 Score Distillation Sampling（SDS）从视频中蒸馏4D信息。这类方法的脆弱性在于SDS优化过程本身的不稳定性，且通常需要较长的优化时间。ShapeGen4D 采用端到端的前馈推理，无需逐样本优化，在推理效率（3–15分钟）上具有显著优势。

**两阶段重建方法**以 **V2M4**（Chen et al., 2025）为代表，先生成逐帧3D网格，再通过后处理优化时间一致性。这种级联架构引入了多阶段累计误差，且后处理步骤难以从根本上解决帧间抖动问题。ShapeGen4D 通过时间对齐的潜在编码和跨帧噪声共享，从扩散模型的去噪过程内部保证了时间一致性，避免了独立后处理带来的信息损失。

**基于变形的方法**以 **GVFD**（Zhang et al., 2025）为代表，在3D模型外挂载独立的变形网络来驱动形状变化。这类方法受限于变形网络的表达能力，无法处理拓扑变化（如物体撕裂、融合、生长等），且对非刚性运动和大体积变化的建模能力有限。ShapeGen4D 将动态网格序列的生成视为帧间条件依赖的3D生成问题，使扩散模型能隐式学习复杂运动模式，原生支持拓扑变化（见图7）。

**前馈式4D高斯方法**以 **L4GM**（Ren et al., 2024）为代表，直接生成动态高斯表示。虽然L4GM在渲染质量上因视图天然对齐而具有独特优势（见表2），但其输出为高斯表示而非网格，在后续可编辑性和动画管线集成方面存在局限。ShapeGen4D 直接输出动态网格序列，更易于融入传统图形学工作流。

### 知识库定位：从3D到4D的迁移范式

ShapeGen4D 的方法论核心在于“继承3D先验，扩展时空维度”。这一设计哲学源自近年来3D生成领域的成功经验——大规模3D数据预训练模型（如 **Step1X-3D**（Li et al., 2025a）和 **Hunyuan3D-2.1**（TencentHunyuan3DTeam, 2025a））已展现出强大的泛化能力。ShapeGen4D 的关键创新在于：**不是将3D模型作为黑盒特征提取器，而是直接微调其内部架构**。

具体而言，该方法在冻结的3D基座Transformer块之间插入可学习的时空注意力层，对跨帧隐藏状态进行联合自注意力。这种设计保留了3D模型在单帧内的几何建模能力，同时通过新增的时空交互模块捕捉帧间依赖。这一“冻结+插入”的微调策略在参数效率和方法通用性上具有优势——论文同时验证了基于Step1X-3D和Hunyuan3D-2.1两个不同基座模型的效果，表明该方法具有一定的模型无关性。

时间对齐的潜在编码机制是另一个知识迁移的关键设计。3D VAE通常对每帧独立采样查询点（Farthest Point Sampling），导致潜在编码在时间维度上不对齐。ShapeGen4D 改为仅在第一帧采样查询点，通过动画的变形函数 $w_t$ 将查询点传播到后续帧，即 $\mathcal{Q}_t = w_t(\mathcal{Q}_1)$。这一设计确保了潜在编码在时间维度上对应相同的表面点，从源头上消除了帧间抖动。消融实验表明，去除该机制后 Chamfer 距离从 0.1096 升至 0.1348，且观看时抖动明显增加。

### 适用边界与局限

尽管ShapeGen4D在Objaverse合成数据集上取得了显著效果，其适用边界仍受多重因素制约：

1. **对预训练3D模型的依赖**：方法的质量上限受限于基座3D模型的性能。若基座模型对某类形状的生成能力较弱，该缺陷会传递到4D生成结果中。论文在Table 1中展示了基于不同基座模型的性能差异（Hunyuan3D-2.1的Chamfer距离0.0827 vs Step1X-3D的0.1220），佐证了这一点。

2. **训练数据分布限制**：训练数据来自Objaverse合成动画数据集，对真实视频的泛化性待验证。真实场景中的复杂背景、遮挡、光照变化等因素可能对条件视频编码模块构成挑战。

3. **纹理生成的独立性**：纹理生成是独立的离线步骤，虽然通过拓扑一致性传播策略（借鉴V2M4的成对网格配准方法）可保持跨帧纹理一致性，但在严重遮挡区域仍可能出现纹理不一致或模糊。

4. **全局姿态配准的脆弱性**：全局姿态配准假设第一帧的相机姿态可被可靠估计。若第一帧存在严重遮挡或视角极端，姿态估计失败将导致整个序列的姿态对齐错误。

5. **长序列生成的退化**：使用MultiDiffusion扩展长序列时，性能存在微小但可察觉的下降（Chamfer距离从0.0929升至0.0934），且远距离帧间的一致性有限。这表明当前框架在建模长程时序依赖方面仍有提升空间。

### 开放问题

论文提出的框架为视频到4D形状生成开辟了新路径，但以下问题值得后续研究关注：

- **视点无关重建的鲁棒性**：基础3D模型倾向于生成任意朝向的形状，与输入图像的视点无关。共享噪声策略虽能部分缓解这一问题（见图4中的河马示例），但在全局刚性旋转场景下仍可能出现姿态偏移。如何在保持生成多样性的同时实现与输入视频的精确姿态对齐，是一个待解决的挑战。

- **可动画化资产的生成**：当前方法生成的是动态网格序列，而非带骨骼绑定或变形控制器的可动画化资产。如何从生成的4D几何中提取可用于下游动画管线（如游戏引擎、电影特效）的完整资产，需要进一步探索。

- **时空3D VAE的可能性**：当前的时间一致性主要通过扩散模型中的时空注意力和噪声共享实现，VAE编解码阶段仍以逐帧处理为主。是否可以使用真正的时空3D VAE直接减少局部时间抖动，是一个值得研究的方向。

- **真实视频的鲁棒性**：当前框架在Objaverse合成数据上验证，对真实户外视频（含复杂背景、动态光照、遮挡）的鲁棒性尚未系统评估。将方法迁移到真实场景可能需要改进条件编码模块或引入额外的鲁棒性训练策略。

## 原文 PDF

![[paperPDFs/ICLR_2026/ShapeGen4D_Towards_High_Quality_4D_Shape_Generation_from_Videos_3a1c93476b93.pdf]]
