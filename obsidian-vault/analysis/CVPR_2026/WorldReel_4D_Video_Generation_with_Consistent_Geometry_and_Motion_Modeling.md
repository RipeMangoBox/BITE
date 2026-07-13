---
title: "WorldReel: 4D Video Generation with Consistent Geometry and Motion Modeling"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/WorldReel_4D_Video_Generation_with_Consistent_Geometry_and_Motion_Modeling.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Fang_WorldReel_4D_Video_Generation_with_Consistent_Geometry_and_Motion_Modeling_CVPR_2026_paper.html
project_link: https://bshfang.github.io/worldreel/
code_link: null
aliases:
- WorldReel
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 提出与表观无关的几何-运动增强潜在空间（geo-motion latent），并同时联合训练视频扩散模型与多任务4D解码器以及解耦正则化，显式注入4D归纳偏置。
primary_logic: 通过将帧对齐的深度与光流编码为增强潜在特征，让扩散模型在生成过程中显式携带几何与运动信息；配合轻量共享时序DPT解码器和针对静态/动态区域的解耦正则化，实现相机运动与物体运动的分离，从而大幅提升动态场景的时空一致性与几何精度。
claims:
- 在复杂运动数据集上，动态度（dynamic degree）达到1.00，显著超越其他方法，同时保持高主体一致性。
- 深度对数RMSE从0.353降至0.287，相机ATE低至0.005、RTE 0.007、RRE 0.317，均为对比方法中最优。
- 消融实验证实去除geo-motion latent或联合训练阶段会引起视频质量和几何准确性的显著下降。
- Image-to-Video Generation (General motion) 上 FVD ↓ = 336.1
---

# WorldReel: 4D Video Generation with Consistent Geometry and Motion Modeling

> [!tip] 核心洞察
> 通过将帧对齐的深度与光流编码为增强潜在特征，让扩散模型在生成过程中显式携带几何与运动信息；配合轻量共享时序DPT解码器和针对静态/动态区域的解耦正则化，实现相机运动与物体运动的分离，从而大幅提升动态场景的时空一致性与几何精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | WorldReel：具有一致几何与运动建模的4D视频生成 |
| 英文题名 | WorldReel: 4D Video Generation with Consistent Geometry and Motion Modeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Fang_WorldReel_4D_Video_Generation_with_Consistent_Geometry_and_Motion_Modeling_CVPR_2026_paper.html) · [Project](https://bshfang.github.io/worldreel/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | WorldReel |
| Dataset | Image-to-Video Generation, Scene Geometry - Depth, Scene Geometry - Camera Pose |

> [!tip] 效果简介
> - Image-to-Video Generation (General motion) 上，FVD ↓ 336.1 vs GeoVideo: 365.1 (↓ 29.0)。
> - Image-to-Video Generation (Complex motion) 上，Dynamic Degree ↑ 1.00 vs GeoVideo: 0.74 (↑ 0.26)。
> - Scene Geometry - Depth (log-RMSE) 上，log-RMSE ↓ 0.287 vs 0.353 (prior best) (↓ 0.066)。

## 概要

### 问题与瓶颈

当前视频生成模型在动态场景建模中面临根本性瓶颈：缺乏统一的3D场景表示，无法维持随时间演变的稳定几何结构。这一问题直接导致视角漂移、几何闪烁，以及相机运动与场景运动之间的纠缠，严重损害时空一致性。现有方法要么面向近静态场景设计（如**GeoVideo**、**4DNeX**），要么依赖后处理4D重建（如**DimensionX**），难以在生成过程中显式建模几何与运动的动态耦合。

### 核心思路

WorldReel的核心洞察在于：将帧对齐的深度与光流编码为与表观无关的几何-运动增强潜在空间（geo-motion latent），让视频扩散模型在生成过程中显式携带几何与运动信息。具体而言，该方法通过以下机制实现4D归纳偏置的注入：

- **增强潜在空间**：将归一化深度图与光流经3D VAE编码后，与RGB潜在表示在通道维拼接，形成联合潜在输入。
- **时序DPT解码器**：设计轻量共享骨干的多任务解码器，从清理后的geo-motion潜在中同时预测深度、点云、相机位姿、场景流和动态掩膜。
- **解耦正则化**：对静态背景施加深度重投影一致性约束，对动态前景施加场景流空间平滑约束，实现相机运动与物体运动的有效分离。

### 方法定位

WorldReel以**CogVideoX-5B-I2V**（Yang et al., arXiv 2024）为骨干视频扩散模型，仅扩展输入/输出投影层以匹配双倍通道数（新增geo-motion分支权重零初始化），其余Transformer模块保持不变。训练采用两阶段策略：第一阶段预训练时序DPT头，第二阶段端到端联合微调扩散模型与解码器，融合扩散损失、多任务预测损失与正则化项。

### 主要结果

在复杂运动数据集上，WorldReel的动态度（Dynamic Degree）达到**1.00**，显著超越GeoVideo的0.74，同时保持高主体一致性。深度估计的对数RMSE从先前最优的0.353降至**0.287**，相机位姿评估中ATE低至**0.005**、RTE **0.007**、RRE **0.317**，均为对比方法中最优。消融实验证实，去除geo-motion latent或联合训练阶段会导致视频质量和几何准确性的显著下降，验证了各模块的必要性。

### 视频生成的现状与瓶颈

近年来，基于扩散模型的视频生成取得了显著进展，能够从文本或单张图像生成具有丰富表观和运动的高质量视频。然而，当前方法普遍缺乏对底层3D场景结构的显式建模，导致生成结果在时空一致性上存在严重缺陷。具体表现为：**视角漂移**（相机运动与场景内容不一致）、**几何闪烁**（同一表面在不同帧中深度和形状发生抖动）、以及**相机运动与物体运动的纠缠**（无法区分场景中的静态背景与动态前景）。这些问题的根源在于现有视频生成模型仅对RGB像素空间进行建模，未能构建随时间演变的统一3D场景表示。

### 现有方法的局限性

针对上述问题，部分工作尝试引入几何或4D信息来增强视频生成。**GeoVideo** 等几何感知方法主要面向近静态场景设计，在复杂动态场景下难以维持几何一致性。**4DNeX** 等动态点云联合生成方法几乎仅处理固定相机运动，无法应对自由相机轨迹下的场景生成。**DimensionX** 等可控视频扩散与后处理4D重建方法虽然能够输出4D场景表示，但其生成与重建过程分离，缺乏端到端的联合优化，导致表观、几何与运动之间的耦合不够紧密。这些方法的共同缺陷在于：缺乏一个统一的框架，将视频扩散模型的生成能力与显式4D场景表示（深度、点云、相机位姿、场景流）的学习有机结合起来。

### WorldReel的核心动机

WorldReel的核心动机在于填补上述缺口——构建一个端到端的4D生成框架，在生成RGB视频的同时，输出具有一致几何与运动的显式4D场景表示。其关键洞察是：通过将帧对齐的深度与光流编码为**与表观无关的几何-运动增强潜在空间（geo-motion latent）**，显式注入视频扩散模型，使生成过程携带几何与运动信息；配合轻量共享的时序DPT解码器和针对静态/动态区域的解耦正则化，实现相机运动与物体运动的分离，从而大幅提升动态场景的时空一致性与几何精度。这一设计使WorldReel能够从单张输入图像和文本提示出发，直接生成包含RGB帧、逐帧点云、校准相机轨迹、光流和场景流的完整4D场景（Figure 1）。

## 核心方法与创新机理

WorldReel 的核心创新在于为视频扩散模型注入显式的 4D 归纳偏置，使其在生成 RGB 视频的同时，能够维持一致的底层 3D 场景几何与运动结构。这一目标通过三个紧密耦合的机制实现：**与表观无关的几何-运动增强潜在空间（geo-motion latent）**、**轻量多任务 4D 解码器**以及**解耦正则化训练策略**。以下围绕与基线方法的 changed slots 展开分析。

### 潜在空间扩展：从 RGB 到 RGB + Geo-Motion

传统视频扩散模型（如 CogVideoX-5B-I2V）的潜在空间仅编码 RGB 表观信息，缺乏对场景几何和运动的显式表征，导致生成的视频在相机运动与物体运动之间产生纠缠，出现几何漂移和闪烁。WorldReel 的关键改造在于**将潜在空间从单模态 RGB 扩展为 RGB 与 geo-motion 的通道拼接**：

$$
\mathbf{z}_0 = [\mathbf{z}_0^{rgb}; \mathbf{z}_0^{gm}]
$$

其中 geo-motion 潜在 $\mathbf{z}_0^{gm}$ 由帧对齐的归一化深度图与光流图经预训练 3D VAE 编码得到：

$$
\tilde{D}_i = 2 \cdot \frac{D_i - d_{min}}{d_{max} - d_{min}} - 1, \quad \tilde{F}_i^{2d} = \frac{F_i^{2d}}{|F^{2d}|_{max}}
$$
$$
\mathbf{z}_0^{gm} = \mathcal{E}([\tilde{D}; \tilde{F}^{2d}])
$$

这一设计的核心洞察在于：深度与光流作为 2.5D 线索，天然携带了场景的几何结构与帧间运动信息，且与 RGB 表观解耦。将它们编码为与 RGB 潜在同维度的特征图并拼接，使扩散模型在去噪过程中显式地“携带”几何与运动先验，从而引导生成过程朝向时空一致的方向收敛。

### 架构适配：最小侵入的 Transformer 改造

为兼容双倍通道数的增强潜在空间，WorldReel 对 CogVideoX 的 DiT 架构进行了**最小化修改**：仅扩展输入/输出投影层以匹配新的通道维度，新增的 geo-motion 分支权重采用零初始化，其余 Transformer 模块（包括注意力层、FFN 等）完全保持不变。这一策略确保了骨干网络的预训练能力得以完整保留，同时使模型从零开始逐步学习如何利用 geo-motion 信息。

### 多任务 4D 解码器：从生成到重建的桥梁

仅靠增强潜在空间不足以显式输出 4D 场景表示。WorldReel 设计了一个**时序 DPT 解码器**，从清理后的 geo-motion 潜在中提取多尺度稠密特征，并通过共享骨干 + 轻量任务头的方式同时预测深度、点云、相机位姿、场景流和动态掩膜。这使模型超越了单纯的视频生成，成为一个端到端的 4D 场景生成系统。

### 解耦正则化：分离相机与物体运动

联合训练阶段引入了关键的几何与运动正则化项：

$$
\mathcal{L}_{reg} = \mathcal{L}_{reg}^{depth} + \mathcal{L}_{reg}^{flow}
$$

其中 $\mathcal{L}_{reg}^{depth}$ 对静态背景区域强制深度重投影一致性，$\mathcal{L}_{reg}^{flow}$ 对动态前景区域施加场景流空间平滑约束。这一解耦设计迫使模型将相机运动与物体运动分离，是 WorldReel 在复杂运动场景下实现动态度 1.00 的关键因果机制。

### 创新有效性验证

消融实验（Table 3）直接证实了上述创新的必要性：去除 geo-motion latent（w/o g.m.）导致复杂运动下 FVD 升高、动态度和主体一致性显著下降；去除联合训练阶段（w/o joint）则损害深度与相机位姿的准确性（Table 2）。值得注意的是，冻结时序 DPT 骨干（freeze dpt）可获得最低 FVD，但动态度和整体生成质量有所降低，表明 4D 解码器的端到端训练在视频质量与几何一致性之间存在一定的权衡。

WorldReel 的整体设计围绕一个核心矛盾展开：**如何在视频扩散模型中注入显式的 4D 归纳偏置，使生成过程同时携带几何与运动信息，而非仅依赖 RGB 表观信号**。为此，该方法构建了一条从增强潜在空间到多任务 4D 解码的端到端流水线，其关键模块关系与数据流如 Figure 2 所示。

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_WorldReel_4D_Vide/figures/002_Figure_2.jpg]]
*Figure 2: Overview of WorldReel. We augment a video diffusion transformer with a geo–motion latent (from RGB and 2.5D cues such as depth/optical flow) to inject a 4D inductive bias for spatio-temporal consistency. A temporal DPT decoder is trained with direct supervision and regularization to predict unified 4D outputs (depth/point cloud, calibrated camera, 3D scene flow, and masks)*

### 流水线总览

给定一张输入图像和文本描述，WorldReel 的输出远不止一段 RGB 视频——它同步生成每帧的深度图、点云、标定相机位姿、光流、场景流以及动态前景掩膜，从而构成一个**持久的动态 3D 场景表示**。这一能力的实现依赖于三个紧密耦合的组件：

1. **几何-运动增强潜在空间**：将帧对齐的归一化深度图与光流图经 3D VAE 编码后，与 RGB 潜在表示在通道维拼接，形成扩散模型的增强输入。这使得扩散过程显式携带 2.5D 几何与运动先验，而非仅从表观推断。
2. **适配的扩散 Transformer**：以 CogVideoX-5B-I2V 的 DiT 为骨干，仅扩展输入/输出投影层以匹配双倍通道数，新增的 geo-motion 分支权重零初始化，其余模块保持不变，从而以最小架构改动接入增强潜在空间。
3. **时序 DPT 解码器与多任务头**：从去噪后的 geo-motion 潜在中提取多尺度稠密特征，经融合骨干与时序 Transformer 处理后，由轻量任务专属头分别预测深度、点云、相机、场景流和动态掩膜。

### 训练策略

训练采用两阶段策略以稳定收敛：

- **第一阶段**：分别训练 geo-motion 增强的 DiT（20K 步）和时序 DPT 头（100K 步），使各模块获得合理的初始化。
- **第二阶段**：端到端联合训练（10K 步），总损失为扩散损失、多任务 DPT 损失与几何/运动正则化损失之和：

$$ \mathcal{L} = \mathcal{L}_{\mathrm{diff}} + \lambda_{\mathrm{dpt}} \mathcal{L}_{\mathrm{dpt}} + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}} $$

其中正则化项 $\mathcal{L}_{\mathrm{reg}}$ 包含深度重投影一致性（约束静态背景跨帧几何一致）和场景流空间平滑性（约束动态前景运动连续），显式实现相机运动与物体运动的解耦。

### 与基线方法的关键差异

与现有工作相比，WorldReel 在三个关键维度上改变了设计范式：

| 维度 | 基线做法 | WorldReel 做法 |
|------|----------|----------------|
| 潜在空间 | 仅 RGB 视频潜在编码 | RGB 潜在 + geo-motion 潜在（归一化深度与光流经 3D VAE 编码后拼接） |
| Transformer 架构 | 标准 DiT 输入/输出投影层 | 扩展投影层匹配双倍通道数，geo-motion 分支零初始化 |
| 解码与监督 | 无显式 4D 解码模块 | 时序 DPT 解码器 + 多任务头 + 解耦正则化，联合预测深度/点云/相机/场景流/掩膜 |

这种设计的核心洞察在于：**与表观无关的几何-运动增强潜在空间**让扩散模型在生成过程中主动携带结构信息，而非被动依赖 RGB 信号重建 3D 一致性。消融实验证实，去除 geo-motion 潜在或联合训练阶段均会导致视频质量和几何准确性的显著下降（Table 3），验证了该设计的必要性。

### 输入输出边界

- **输入**：单张 RGB 图像 + 文本提示
- **输出**：RGB 视频 + 每帧深度图 + 点云 + 标定相机位姿 + 光流 + 场景流 + 动态前景掩膜
- **骨干模型**：CogVideoX-5B-I2V（Yang et al., arXiv 2024），作为视频扩散 Transformer 的基础架构

WorldReel 的核心架构围绕三个关键模块展开：**几何-运动增强潜在空间**、**时序 DPT 解码器**以及**解耦正则化训练目标**。以下逐一拆解其设计原理与关键公式。

### 几何-运动增强潜在空间

标准视频扩散模型仅在 RGB 潜在空间上执行去噪，缺乏对场景三维结构与运动的显式建模。WorldReel 的核心创新在于引入与表观无关的几何-运动增强潜在表示，将帧对齐的深度图与光流作为额外的条件信号注入扩散过程。

具体而言，对于每帧的深度图 $D_i$ 和二维光流 $F_i^{2d}$，首先进行归一化处理以匹配 3D VAE 的数值范围：

$$
\tilde{D}_i = 2 \cdot \frac{D_i - d_{min}}{d_{max} - d_{min}} - 1
$$

$$
\tilde{F}_i^{2d} = \frac{F_i^{2d}}{|F^{2d}|_{max}}
$$

归一化后的深度与光流在通道维拼接，经预训练的 3D VAE 编码器 $\mathcal{E}$ 压缩为 geo-motion 潜在表示：

$$
\mathbf{z}_0^{gm} = \mathcal{E}([\tilde{D}; \tilde{F}^{2d}])
$$

最终，将 RGB 潜在 $\mathbf{z}_0^{rgb}$ 与 geo-motion 潜在在通道维度拼接，形成增强潜在输入：

$$
\mathbf{z}_0 = [\mathbf{z}_0^{rgb}; \mathbf{z}_0^{gm}]
$$

**架构适配**：为处理双倍通道数的增强潜在，仅需扩展 DiT 的输入/输出投影层，新增的 geo-motion 分支权重采用零初始化，其余 Transformer 模块保持不变。这一最小化修改策略确保模型在初始阶段行为与原始骨干网络一致，随后逐步学习利用几何-运动信息。

### 时序 DPT 解码器

从去噪后的 geo-motion 潜在中，WorldReel 通过定制的时序 DPT 解码器提取统一的 4D 场景表示。该解码器包含：

- **共享 DPT 骨干**：融合时序 Transformer 的多尺度稠密特征提取网络，从 geo-motion 潜在中重建空间结构信息。
- **轻量任务专用头**：基于共享特征分别预测深度图、点云、相机位姿、场景流和动态掩膜。

DPT 预训练阶段的多任务损失为：

$$
\mathcal{L}_{dpt} = \mathcal{L}_{depth} + \mathcal{L}_{pc} + \mathcal{L}_{cam} + \mathcal{L}_{mask} + \lambda_{flow} \mathcal{L}_{flow} \tag{2}
$$

其中各分量分别对应深度、点云、相机参数、动态掩膜和场景流的监督损失，$\lambda_{flow}$ 为场景流损失的权重系数。

### 解耦正则化与联合训练目标

为分离相机运动与场景运动，WorldReel 引入针对静态/动态区域的解耦正则化：

$$
\mathcal{L}_{reg} = \mathcal{L}_{reg}^{depth} + \mathcal{L}_{reg}^{flow} \tag{3}
$$

- **深度重投影一致性** $\mathcal{L}_{reg}^{depth}$：对静态背景区域，强制跨帧深度图在相机运动下的重投影一致性，抑制几何闪烁。
- **场景流空间平滑** $\mathcal{L}_{reg}^{flow}$：对动态前景区域，约束 3D 场景流的空间平滑性，避免运动估计的局部畸变。

场景流伪标签通过光流对应与点云计算获得，仅在前景区域（$\hat{M}_i(\mathbf{u}) = 1$）赋值：

$$
\hat{F}_i^{3d}(\mathbf{u}) = \begin{cases} P_{i+1}(\mathbf{q}(\mathbf{u})) - P_i(\mathbf{u}), & \text{if } \hat{M}_i(\mathbf{u}) = 1 \\ \mathbf{0}, & \text{otherwise} \end{cases} \tag{5}
$$

最终端到端联合训练的总损失融合扩散损失、多任务预测损失与正则化项：

$$
\mathcal{L} = \mathcal{L}_{diff} + \lambda_{dpt} \mathcal{L}_{dpt} + \lambda_{reg} \mathcal{L}_{reg} \tag{4}
$$

其中 $\mathcal{L}_{diff}$ 为标准的视频潜在扩散去噪损失（式 1），$\lambda_{dpt}$ 和 $\lambda_{reg}$ 分别控制多任务损失与正则化项的权重。

### 训练策略

WorldReel 采用两阶段训练策略：第一阶段分别微调 geo-motion 增强 DiT（约 20K 步）和从头训练时序 DPT 头（约 100K 步）；第二阶段端到端联合微调整个模型（约 10K 步），同时施加正则化约束。消融实验证实，去除 geo-motion 潜在或跳过联合训练阶段均会导致视频质量与几何准确性的显著下降（Table 3）。

## 实验与关键发现

### 核心定量结果：视频生成质量

WorldReel在图像到视频生成任务上展现出全面的质量优势，尤其在复杂运动场景下建立了显著领先。Table 1报告了General motion与Complex motion两个划分上的多维度对比。在General motion划分上，WorldReel取得FVD 336.1，较GeoVideo的365.1降低29.0；在Complex motion划分上，FVD为394.2，仍保持竞争力。更具区分度的指标是**动态度（dynamic degree）**：WorldReel在Complex motion划分上达到**1.00**，而GeoVideo仅为0.74，提升了0.26。这一差距直接反映了geo-motion潜在空间对动态场景建模的根本性改进——基线方法（如GeoVideo、4DNeX）主要面向近静态场景设计，在复杂运动下几何漂移和运动不一致问题突出（Figure 3提供了定性佐证），而WorldReel通过显式注入深度与光流先验，在保持高主体一致性的同时大幅增强了运动表达能力。

### 场景几何精度：深度与相机位姿

Table 2展示了场景几何层面的定量评估。WorldReel在深度估计上将log-RMSE从先前最佳的0.353降至**0.287**，降幅达18.7%。相机位姿估计同样表现最优：ATE低至0.005、RTE 0.007、RRE 0.317，均为对比方法中最低。这一组指标直接验证了geo-motion潜在空间与多任务时序DPT解码器的协同效果——扩散模型生成的增强潜在表示携带了足够的几何信息，而DPT解码器通过共享骨干与任务特定头的设计，能够从同一潜在表示中准确恢复深度、点云与相机轨迹。值得注意的是，相机轨迹估计虽具竞争力但非全面最优，这提示在长时序相机运动建模上仍有提升空间。

### 消融实验：各模块的因果贡献

Table 3的系统消融揭示了三个关键设计选择的因果效应：

**去除geo-motion潜在空间（w/o g.m.）**：在Complex motion划分上，动态度和主体一致性显著下降，FVD升高。这表明仅靠RGB潜在空间无法有效建模复杂动态场景的几何与运动结构，geo-motion增强是处理非刚性运动与相机运动耦合问题的必要条件。

**去除联合训练阶段（w/o joint）**：深度与相机位姿准确性明显退化（Table 2），同时视频生成质量受损。这证实了多任务DPT解码器与正则化项的端到端联合优化并非可有可无的后处理——扩散模型在生成过程中需要来自几何监督的梯度信号，才能将几何一致性内化为生成先验。

**冻结时序DPT骨干（freeze dpt）**：该变体取得了最低的FVD，但动态度和整体生成质量有所降低。这揭示了一个有趣的权衡：冻结DPT骨干使扩散模型的训练更加稳定（去噪目标不受解码器梯度干扰），从而获得更好的感知质量指标；但代价是几何与运动的一致性被削弱。这一发现暗示，未来工作可探索更精细的梯度控制策略，在感知质量与几何一致性之间取得更优平衡。

### 失败模式与局限性的实验证据

尽管整体表现优异，实验中也暴露了若干边界条件。首先，当前方法依赖合成数据提供精确的4D监督（相机、点云、场景流），对真实视频仅利用几何与运动伪标签，这意味着在分布外真实场景上的深度与位姿精度可能低于Table 2报告的值——该结论需要额外的跨域评估来验证。其次，生成视频的时间长度固定，扩散模型的离线特性使其难以支持流式推演，这在需要持久世界状态的应用场景中构成瓶颈。此外，模型缺乏可控的场景分解能力，无法对独立实体进行分离编辑，限制了交互式长程生成的灵活性。这些限制在消融实验中虽未直接量化，但构成了方法向实际部署演进时需要解决的核心工程挑战。

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_WorldReel_4D_Vide/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison on image-to-video (I2V) generation under two splits: General motion and Complex motion. Metrics: dynamic degree (d.d.; ↑), motion smoothness (m.s.; ↑), I2V-subject/background (i2v-s./i2v-b.; ↑), subject consistency (s.c.; ↑), Frechet Video ´ Distance (FVD; ↓), and FID (↓). WorldReel achieves the best overall performance, with notably higher dynamic degree while maintaining strong s.c. and perceptual quality (lower FVD/FID). Bold indicates best; underline second-best. Gray rows denote methods that primarily focus on nearly-static scenes*

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_WorldReel_4D_Vide/figures/005_Table_2.jpg]]
*Table 2: Scene geometry evaluation on depth, camera pose, and camera trajectory. WorldReel achieves the best depth and camera accuracy across all pose metrics, with competitive trajectory estimates. Ablations (w/o geomotion, w/o joint) degrade depth or pose quality, confirming the importance of geo–motion latent and joint training. Bold = best, underline = second-best*

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_WorldReel_4D_Vide/figures/006_Table_3.jpg]]
*Table 3: Ablation study on image-to-video generation under General and Complex motion. Variants: base finetuned, w/o g.m. (without geo–motion latent), w/o joint (no joint multi-task decoding/regularizers), freeze dpt (freeze temporal DPT backbone in stage-2), and full (ours). Metrics: dynamic degree (d.d.; ↑), motion smoothness (m.s.; ↑), I2V-subject/background (i2v-s./i2v-b.; ↑), subject consistency (s.c.; ↑), FVD (↓), and FID (↓). Our full model delivers the best overall quality (lowest FID and highest d.d. on complex motion), while freeze dpt attains the lowest FVD; removing geo–motion latent or joint training degrades consistency. Bold = best, underline = second-best*

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_WorldReel_4D_Vide/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative image-to-video comparison on in-the-wild scenes. Given a single input image (left), we show sampled frames from videos generated by 4DNeX [10], DimensionX [52], GeoVideo [3], and WorldReel (ours). Prior methods often exhibit geometry drift and motion inconsistencies (e.g., warped facades, misaligned vehicles), while our results better preserve scene layout and maintain coherent camera and non-rigid dynamics. See the supplementary for prompts, full videos for all methods, and additional comparisons*

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_WorldReel_4D_Vide/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative 4D generation and geometry. For two in-the-wild inputs (left, red boxes), we show selected frames from our generated videos (top rows) alongside the corresponding dynamic point clouds rendered from our pointmaps and camera trajectories (bottom rows). The persistent structure and consistent camera/object motion illustrate a single, stable 3D scene across time, evidencing strong geometric consistency in the underlying world state. See supplementary for additional examples*

## 定位与知识库关联

### 与基线方法的关系

WorldReel 处于**4D感知视频生成**这一新兴交叉地带，其方法设计同时回应了视频扩散模型、4D场景重建和动态场景生成三条技术路线中的关键瓶颈。

**与几何感知视频生成方法的关系。** **GeoVideo** 是直接对比的几何感知视频生成方法，但其设计主要面向近静态场景，在复杂运动下动态程度仅达0.74，而WorldReel达到1.00（Table 1）。WorldReel的关键差异在于：GeoVideo缺乏统一的4D场景表示，无法显式建模相机运动与物体运动的解耦；WorldReel通过geo-motion增强潜在空间和时序DPT解码器，将深度、相机位姿、场景流和动态掩膜统一为4D输出，从根本上解决了视角漂移和几何闪烁问题。

**与动态场景生成方法的关系。** **4DNeX** 作为动态点云联合生成方法，几乎仅处理固定相机运动场景，在真实世界动态内容上泛化能力有限。**DimensionX** 采用可控视频扩散加后处理4D重建的两阶段策略，但后处理阶段缺乏与生成过程的端到端耦合，导致重建结果与视频表观不一致。WorldReel将扩散生成与4D解码统一为端到端框架，确保表观、几何和运动的紧耦合。

**与基础视频生成模型的关系。** WorldReel以 **CogVideoX-5B-I2V**（Yang et al., arXiv 2024）为骨干网络，但对其潜在空间和训练目标进行了根本性扩展。标准CogVideoX仅处理RGB视频潜在编码，WorldReel将输入通道加倍以容纳geo-motion潜在，并新增多任务4D解码器与解耦正则化项。值得注意的是，WorldReel对DiT架构的修改极为克制——仅扩展输入/输出投影层，新增的geo-motion分支权重采用零初始化，其余Transformer模块完全复用预训练权重（Sec. 3.2）。这种“最小侵入式”适配策略保证了预训练视频生成能力的完整迁移。

### 适用边界

**数据依赖性边界。** WorldReel当前依赖合成数据提供精确的4D监督信号（相机参数、点云真值、场景流），对真实视频仅利用深度和光流的伪标签。这意味着模型在合成数据覆盖的分布内表现优异，但向完全无约束的真实场景泛化时，4D输出的精度可能受限于伪标签质量。这一权衡本质上是标注成本与泛化能力之间的结构性矛盾。

**时序建模边界。** 生成视频的时间长度固定，扩散模型为离线形式，不支持流式或因果推演。这限制了WorldReel在需要持久世界状态维护或交互式长程生成场景中的适用性。

**场景分解边界。** 当前框架缺乏可控的场景分解能力，无法对场景中的独立实体进行分离编辑或组合式生成。动态掩膜提供了前景/背景的二元分割，但未扩展到多实体级别的细粒度控制。

### 局限与开放问题

**局限1：合成数据依赖与真实场景泛化的权衡。** 精确的4D监督（相机、点云、场景流）主要来自合成渲染数据，真实视频的几何与运动监督只能通过伪标签近似。这导致模型在真实场景中的4D输出精度存在上限。一个开放问题是：**如何利用弱监督或自监督的4D信号（如单目视频中的多视图几何约束）减少对合成标注的依赖？**

**局限2：离线生成范式的时序封闭性。** 固定长度的离线扩散过程无法支持因果推演或持久世界状态。开放问题：**如何将生成范式扩展为流式/因果扩散模型，实现持久的动态世界状态维护？**

**局限3：缺乏可分解的场景表示。** 当前4D输出是场景级的整体表示，缺乏对独立实体的结构化分解。这限制了交互式编辑、局部运动控制和长时序组合生成等应用。开放问题：**如何引入可控的场景分解机制，以支持忠实的长时序、交互式4D生成与编辑？**

### 知识库定位

WorldReel在方法谱系中的核心贡献在于**将4D归纳偏置显式注入视频扩散模型的潜在空间**，而非依赖后处理或多阶段流水线。这一设计选择使其在动态场景的时空一致性和几何精度上建立了新的基准（深度log-RMSE从0.353降至0.287，相机ATE低至0.005），同时保持了与现有视频扩散骨干的高度兼容性。该方法为未来结合更强4D自监督信号和流式生成范式的研究提供了清晰的技术锚点。

## 原文 PDF

![[paperPDFs/CVPR_2026/WorldReel_4D_Video_Generation_with_Consistent_Geometry_and_Motion_Modeling.pdf]]
