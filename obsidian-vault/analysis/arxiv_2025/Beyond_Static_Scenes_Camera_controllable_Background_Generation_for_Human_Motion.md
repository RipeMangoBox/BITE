---
title: "Beyond Static Scenes: Camera-controllable Background Generation for Human Motion"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Beyond_Static_Scenes_Camera_controllable_Background_Generation_for_Human_Motion.pdf
project_link: https://yaomingshuai.github.io/Beyond-Static-Scenes.github.io/
code_link: null
aliases:
- BSSCCBGHM
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入相机姿态（Plücker嵌入）作为显式控制信号，并采用两阶段多任务学习策略来增强新区域生成和旧区域一致性。
primary_logic: 通过两阶段训练（先从图像学习空间关系，再从视频学习时间一致性），结合背景外推、场景变化和背景生成等多任务，使模型能够同时处理相机移动、前景位置和场景一致性。
claims:
- 显式相机控制显著改善生成背景的时间一致性。
- 背景外推和场景变化提升生成场景的真实感和一致性。
- 两阶段训练策略优于单阶段训练，显著降低FID和FVD。
- DynaScene在所有定量指标上均优于现有方法CameraCtrl和ActAnywhere。
---

# Beyond Static Scenes: Camera-controllable Background Generation for Human Motion

> [!tip] 核心洞察
> 通过两阶段训练（先从图像学习空间关系，再从视频学习时间一致性），结合背景外推、场景变化和背景生成等多任务，使模型能够同时处理相机移动、前景位置和场景一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 超越静态场景：面向人体运动的相机可控背景生成 |
| 英文题名 | Beyond Static Scenes: Camera-controllable Background Generation for Human Motion |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2504.02004) · [Project](https://yaomingshuai.github.io/Beyond-Static-Scenes.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | DynaScene |
| Dataset | DynaScene test set |

> [!tip] 效果简介
> - DynaScene test set 上，FID 96.18 vs 98.44 (-2.26)；FVD_I3D 55.84 vs 57.54 (-1.70)。

## 概要

现有视频背景生成方法面临一个关键瓶颈：**缺乏显式的相机姿态控制**，导致背景运动与前景人体运动不一致，且无法处理相机移动时新区域内容的生成问题。为解决这一挑战，本文提出 **DynaScene**，一个以相机姿态为显式控制信号驱动背景运动的生成框架。其核心洞察在于：通过两阶段多任务训练策略——第一阶段从图像学习空间关系，第二阶段从视频学习时间一致性——并联合背景外推、场景变化和背景生成等辅助任务，使模型能够同时处理相机移动、前景位置和场景一致性。

在方法定位上，DynaScene 区别于 **CameraCtrl**（仅控制相机运动但无法有效处理前景-背景交互）和 **ActAnywhere**（能生成视频背景但无显式相机控制），首次将相机姿态（Plücker 嵌入）作为显式条件引入视频背景生成任务，并采用 Stable Diffusion 1.5 作为基础去噪网络，结合 AnimateDiff v2 的运动模块实现帧间时间一致性建模。

实验表明，DynaScene 在所有定量指标上均优于现有竞争方法。消融研究进一步验证了各模块的有效性：加入相机控制使 FVD_I3D 提升 7.7%；背景外推和场景变化分别在 FID 和感知指标上带来增益；两阶段训练策略相比单阶段训练，FID 降低 2.26，FVD_I3D 降低 1.70。

### 问题背景

在视频生成与编辑领域，将人体运动无缝嵌入到任意静态场景中是一个具有广泛应用前景的任务，涵盖影视制作、虚拟现实和数字人等方向。该任务的核心挑战在于：给定一段人体前景视频和一张静态场景图像，需要生成与该场景一致、且与前景运动协调的背景视频。

然而，现实世界中的视频拍摄极少使用固定机位。相机运动会引入背景的平移、旋转和缩放，导致场景中原本可见的区域移出画面，同时暴露出此前被遮挡的新区域。这种动态性使得背景生成问题从简单的“纹理填充”升级为“空间推理与内容生成”的复合任务。

### 现有方法的缺口

当前主流的视频背景生成方法存在两个关键瓶颈：

**1. 缺乏显式相机姿态控制**

以 **ActAnywhere** 为代表的方法仅依赖前景运动作为隐式驱动信号，未将相机姿态作为独立的控制条件。这导致生成的背景运动与相机实际运动之间缺乏物理一致性——例如，当相机向左平移时，背景应向右移动，但现有方法可能产生静止或方向错误的背景运动。此外，相机移动所暴露的新区域需要模型凭空生成合理内容，而缺乏姿态信息使模型难以判断“哪些区域是新的、新区域应呈现何种纹理”。

**2. 前景-背景交互建模不足**

相机可控视频生成方法如 **CameraCtrl** 和 **MotionCtrl** 虽然引入了相机姿态控制，但它们的设计目标是生成完整的视频帧，而非专门处理前景与背景的分离合成。当应用于“给定前景、生成背景”的场景时，这些方法难以有效保持前景人物的完整性，同时确保背景与前景在运动、光照和语义上的协调。

### 本文动机

针对上述缺口，本文提出 **DynaScene** 框架，核心动机体现在三个层面：

- **显式相机控制**：将相机姿态（以 Plücker 嵌入形式）作为显式控制信号注入生成过程，使背景运动与相机运动精确对齐，同时为模型提供新区域出现的空间线索。
- **多任务学习增强真实性**：设计背景外推（Background Outpainting）和场景变化（Scene Variation）两个辅助任务，与背景生成主任务联合训练。背景外推训练模型修复被遮挡区域的纹理，场景变化则增强模型对同一场景不同视角的生成能力。
- **两阶段训练策略**：第一阶段在图像层面学习空间关系（背景外推与场景变化），第二阶段在视频层面学习时间一致性。这种分解使模型先掌握“单帧场景理解”，再学习“跨帧运动连贯性”，从而更稳定地收敛。

通过这些设计，DynaScene 旨在实现一个统一框架：既能处理相机移动带来的新区域生成问题，又能保持已有区域的时间一致性，同时确保背景与前景在运动、纹理和光照上的协调。

## 核心方法与创新机理

DynaScene 的核心创新在于将**显式相机姿态控制**引入视频背景生成任务，并通过**两阶段多任务学习策略**解决相机移动带来的新区域生成与旧区域一致性问题。相较于现有方法，其关键改进体现在三个维度的“changed slots”上。

### 1. 显式相机姿态控制：从被动跟随到主动驱动

现有视频背景生成方法（如 **ActAnywhere**）仅依赖前景人体运动来隐式推断背景变化，缺乏对相机运动的直接建模。当相机本身发生平移、旋转或缩放时，背景需要产生与前景一致的视差和透视变化，而隐式方法无法可靠地捕捉这种关系，导致背景运动与前景运动脱节。

DynaScene 的核心设计是将相机姿态作为**显式控制信号**注入生成过程。具体而言，系统从原始视频中提取相机姿态，并以 **Plücker嵌入**（$\mathbf{P} \in \mathbb{R}^{F \times 6 \times H \times W}$，其中 $F$ 为帧数）的形式表示。该嵌入通过专门的 **Camera Encoder** 和 **Camera Adaptor** 模块处理，最终融入去噪 U-Net 的特征空间。这一设计使得模型能够明确感知相机在三维空间中的运动轨迹，从而驱动背景产生与之匹配的几何变换。

消融实验直接验证了这一设计的因果效应：加入相机控制（CC）后，FVD_I3D 提升 7.7%，FVD_3DRes 提升 2.1%，表明视频的时间一致性和视觉保真度均得到显著增强（Table 3）。定性结果（Figure 4）进一步显示，有相机控制时背景与前景的对齐程度明显优于无控制的情况。

### 2. 两阶段训练策略：空间先验与时序精炼的解耦

传统视频生成方法通常采用单阶段训练，直接从视频数据中同时学习空间结构和时间动态。DynaScene 提出**两阶段训练策略**，将空间一致性和时间一致性的学习解耦：

- **第一阶段（图像训练）**：在静态图像上训练，使模型学习场景图像与生成背景之间的空间对应关系，建立对新区域纹理的生成能力。
- **第二阶段（视频训练）**：在视频序列上微调，引入时间注意力模块（来自 **AnimateDiff v2** 的 Motion Module），使模型学习帧间的时间连续性。

这一设计的因果逻辑在于：空间关系的学习需要大量静态场景样本，而时间一致性的学习需要连续帧序列。将两者混合训练可能导致优化目标冲突，而分阶段训练允许模型先建立稳固的空间先验，再学习时间平滑。定量结果支持这一判断：两阶段训练相比单阶段训练，FID 从 98.44 降至 96.18（降低 2.26），FVD_I3D 从 57.54 降至 55.84（降低 1.70）（Table 4）。

### 3. 多任务学习：背景外推与场景变化的联合优化

除核心的背景生成任务外，DynaScene 引入两个辅助任务形成**多任务学习范式**：

- **背景外推（Background Outpainting, BO）**：随机遮挡场景图像的部分区域，要求模型恢复被遮挡的内容。该任务训练模型在相机移动揭示新区域时，生成与已知场景纹理一致的合理内容。
- **场景变化（Scene Variation, SV）**：对同一前景在不同场景下的生成施加一致性约束，确保场景特征（如墙壁纹理、地面材质）在视频中保持稳定。

这两个辅助任务与主任务共享同一去噪 U-Net 权重，通过联合训练实现知识迁移。消融实验揭示了各任务的增量贡献：加入 BO 使 FID 提升 1.13%，表明新生成区域的纹理真实性得到改善（Figure 5 显示伪影被有效消除）；加入 SV 后在像素级和感知指标上均达到最优（Table 3），Figure 6 显示场景元素（如绿色框标注区域）得到更好保留。

### 方法谱系与知识库定位

DynaScene 在视频背景生成的方法谱系中占据了“相机可控”这一此前空白的生态位。与 **CameraCtrl**（相机可控视频生成，但无法有效处理前景-背景交互）和 **ActAnywhere**（视频背景生成，但无显式相机控制）相比，DynaScene 首次将显式相机姿态控制与背景生成任务结合。其技术路线可视为对 **Stable Diffusion 1.5** 视频化扩展（引入 AnimateDiff v2 的 Motion Module）与相机条件注入（Plücker 嵌入 + Camera Adaptor）的融合，同时借鉴了多任务学习中辅助任务设计的思路。

### 局限与待验证边界

尽管创新点明确且证据充分，以下方面仍需注意：
- 当人体前景运动与相机姿态存在语义冲突时（如放大的人体前景与缩小的相机姿态），模型可能生成不理想的结果（Figure 10），其量化容忍极限尚未明确。
- 模型性能高度依赖前景掩码质量；不准确的掩码会在前景-背景边缘产生伪影，这一鲁棒性问题在论文中仅被定性提及，缺乏定量评估。
- 自适应背景光照调整（ABIA）被提及为有效组件（Figure 9），但其具体实现细节和消融实验的定量结果在已有证据中覆盖有限，需查阅附录 D 进行验证。

DynaScene 的整体框架围绕一个核心设计展开：**将相机姿态作为显式控制信号注入视频扩散模型**，使生成的背景运动与前景人体运动及相机运动保持一致。框架接收三类输入：(1) 一张静态场景图像 $I_s$，(2) 一段人体前景帧序列 $\{ I_f^1, ..., I_f^n \}$ 及其对应的前景掩码，(3) 从原始视频中提取的相机姿态。输出为与前景运动同步、且响应相机变化的连贯背景视频。

### 数据流与模块关系

框架的数据流可概括为三条并行的信息通路，最终汇聚于去噪 U-Net（图 2）：

1. **前景与噪声通路**：视频前景帧、前景掩码与噪声潜变量在通道维度拼接后，直接输入去噪 U-Net。这一设计使模型在去噪过程中始终感知前景的空间位置与形状边界。

2. **场景图像通路**：场景图像 $I_s$ 分别经过 **CLIP 图像编码器**和 **ReferenceNet** 处理。CLIP 编码器提取高层次语义信息，通过交叉注意力注入 U-Net；ReferenceNet 则捕获细粒度纹理细节，通过参考注意力机制提供空间对齐的外观约束。两条分支互补，使模型既能理解场景的语义类别（如“草地”“室内”），又能保留纹理一致性。

3. **相机姿态通路**：相机姿态以 **Plücker 嵌入**形式表示，张量形状为 $\mathbf{P} \in \mathbb{R}^{F \times 6 \times H \times W}$（$F$ 为帧数）。该嵌入首先经过 **Camera Encoder** 编码为特征，再由 **Camera Adaptor**（两层线性变换）将其融合到去噪 U-Net 的特征中。这一通路是 DynaScene 区别于 **ActAnywhere** 等无相机控制方法的关键——后者仅依赖前景运动隐式推断背景变化，无法处理相机主动移动时新区域的生成。

### 时间一致性建模

为建模视频帧间的时间一致性，框架在 Stable Diffusion 1.5 的去噪 U-Net 中集成了来自 **AnimateDiff v2** 的运动模块（Motion Module）。该模块在空间注意力之后插入时间注意力层，使各帧的去噪过程相互感知，从而抑制闪烁和抖动。

### 两阶段多任务训练策略

DynaScene 采用**两阶段多任务训练**策略，以解耦空间一致性与时间一致性的学习：

- **阶段 I（图像训练）**：仅使用单帧数据进行训练，重点学习场景图像与背景之间的空间映射关系。此阶段引入**背景外推**辅助任务——随机遮挡场景图像的 $60\%$–$90\%$ 区域，要求模型恢复被遮挡部分，从而强化对新显露区域纹理的生成能力。
- **阶段 II（视频训练）**：在阶段 I 权重基础上，使用完整视频序列进行微调，引入时间注意力学习帧间连续性。**场景变化**任务贯穿两个阶段，通过随机替换场景图像迫使模型适应不同的背景上下文，提升生成场景的多样性与真实感。

所有任务共享同一个去噪 U-Net，通过任务特定的条件信号切换训练目标，而非维护多个独立模型。

### 公平比较中的前景重注入

在与其他方法（如 **CameraCtrl**、**MotionCtrl**）进行公平比较时，DynaScene 在去噪过程的每一步 $t$ 执行前景潜变量重注入操作：

$$h^{t} = h_{ori}^{t} \times M + h_{fore}^{t} \times (1 - M)$$

其中 $h_{ori}^{t}$ 为原始去噪潜变量，$h_{fore}^{t}$ 为前景区域的潜变量，$M$ 为人体前景掩码。这一操作确保比较方法之间的前景重建质量一致，差异仅来源于背景生成能力本身。

### 局限性

框架的性能高度依赖前景掩码的精度。当掩码边缘不准确时，前景与背景交界处会出现明显伪影或融合不佳。此外，当输入存在冲突信号（如放大的人体前景与缩小的相机姿态），模型可能难以生成合理结果（见图 10）。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2504_02004/figures/002_Figure_2.jpg]]
*Figure 2: Overview of DynaScene framework. The noise latent, foreground mask, and human foreground are concatenated into the denoising U-Net. We employ the CLIP encoder and ReferenceNet to capture both high-level semantic features and fine-grained details from the scene image, respectively. The camera pose is integrated into the Camera Encoder. To enhance the model’s ability to generate coherent textures for newly revealed areas and preserve consistency in previously visible areas, we introduce multi-task learning including background outpainting in Stage I and scene variation across all stages. All tasks are trained on the same U-Net model*

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2504_02004/figures/012_Figure_8.jpg]]
*Figure 8: Pipeline of constructing DynaScene Dateset*

DynaScene 以 Stable Diffusion 1.5 为基础扩散模型，通过四个关键模块的协同设计实现相机可控的背景生成。整体架构如 Figure 2 所示。

### 3.1 基础扩散框架

模型遵循标准潜空间扩散范式。前向过程向干净潜变量 $\mathbf{z}_0$ 逐步添加高斯噪声：

$$\mathbf{z}_t = \sqrt{\bar{\alpha}_t} \mathbf{z}_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{U}([0,1])$$

其中 $\bar{\alpha}_t$ 为累积噪声调度参数，$\mathbf{z}_t$ 为时间步 $t$ 的噪声潜变量。去噪网络 $\epsilon_\theta$ 的训练目标为最小化噪声预测误差：

$$\mathcal{L} = \mathbb{E}_{\mathbf{z}_t, c, \epsilon, t} \left( || \epsilon - \epsilon_\theta(\mathbf{z}_t, c, t) ||_2^2 \right)$$

其中 $c$ 为条件信号，包括场景图像特征、相机姿态嵌入及前景掩码信息。

### 3.2 场景图像处理模块（CLIP & ReferenceNet）

静态场景图像 $I_s$ 通过两条并行的编码路径处理：
- **CLIP 编码器**：提取高层次语义特征，经交叉注意力注入去噪 U-Net，为背景生成提供场景类别和全局布局信息。
- **ReferenceNet**：捕捉细粒度纹理和结构细节，通过参考注意力机制将场景的局部纹理信息传递到生成过程中。

这种双路径设计使得模型既能保持场景的语义一致性，又能还原场景图像中的细节纹理。

### 3.3 相机编码器与相机适配器

相机姿态控制是 DynaScene 区别于现有方法的核心创新。相机姿态以 **Plücker 嵌入**形式表示，其张量形状为 $\mathbf{P} \in \mathbb{R}^{F \times 6 \times H \times W}$，其中 $F$ 为视频帧数，$H \times W$ 为空间分辨率，6 通道编码了每条像素射线的 Plücker 坐标。

相机编码器负责将 Plücker 嵌入转换为多尺度特征，相机适配器则通过两层线性层将这些特征与去噪网络的特征进行融合（结构细节见 Figure 7）。这种显式相机姿态控制使得背景运动能够与前景运动保持几何一致性，解决了现有方法中背景运动不可控的核心瓶颈。

### 3.4 运动模块

模型集成了来自 **AnimateDiff v2** 的运动模块，将其插入扩散 U-Net 中以引入时间注意力机制。运动模块在帧间建立时序依赖，确保生成的视频背景在时间维度上平滑连续，避免帧间闪烁和不一致。

### 3.5 VAE 编解码器

遵循 Stable Diffusion 1.5 的标准流程，VAE 编码器 $\mathcal{E}$ 将输入图像压缩到低维潜空间，VAE 解码器 $\mathcal{D}$ 将去噪后的潜变量 $\hat{\mathbf{z}}_0$ 重建为像素空间图像。这一压缩-重建机制显著降低了扩散模型的计算开销。

### 3.6 关键操作：前景潜变量重注入

在推理阶段与基线方法（CameraCtrl、MotionCtrl）进行公平比较时，采用前景潜变量重注入操作：

$$h^{t} = h_{ori}^{t} \times M + h_{fore}^{t} \times (1 - M)$$

其中 $h_{ori}^{t}$ 为原始去噪潜变量，$h_{fore}^{t}$ 为前景潜变量，$M$ 为人体前景掩码。该操作确保在去噪的每个时间步 $t$，前景区域保持与原始输入一致，仅背景区域由模型生成，从而消除前景重建质量的差异对比较结果的干扰。

## 实验与关键发现

### 主结果对比

DynaScene 在自建测试集上与两类代表性方法进行了系统对比：相机可控视频生成方法 **CameraCtrl** 和 **MotionCtrl**，以及视频背景生成方法 **ActAnywhere**。为确保公平比较，在 CameraCtrl 和 MotionCtrl 的去噪过程中，通过公式 $h^{t} = h_{ori}^{t} \times M + h_{fore}^{t} \times (1 - M)$ 将前景潜变量重新引入原始潜变量，消除了前景重建差异对评估的影响。

定量结果如 Table 2 所示，DynaScene 在所有七项指标上均取得最优性能：L1 误差 $8.12 \times 10^{-5}$，PSNR 29.27，SSIM 0.506，LPIPS 0.354，FID 96.18，FVD_I3D 55.84，FVD_3DRes 1064.36。值得注意的是，ActAnywhere 虽然能生成视觉质量不错的背景，但由于缺乏显式相机控制，其背景运动与前景运动的一致性显著弱于 DynaScene；CameraCtrl 具备相机控制能力，却无法有效处理前景-背景交互，导致背景纹理与场景图像语义脱节。Figure 3 的定性对比直观展示了这一差异：DynaScene 生成的背景在相机移动时既能保持与前景运动的空间对齐，又能维持场景内容的语义一致性。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2504_02004/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparison with competing methods. † indicates this method is re-implemented by us*

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2504_02004/figures/005_Figure_3.jpg]]
*Figure 3: Comparison with other methods. The first and fifth rows are the video foreground, with the scene image located in the bottom-left corner of the first frame. The 2∼4 and 6∼8 rows are the results of CameraCtrl [17], ActAnywhere [38], and our DynaScene, respectively*

### 消融实验

消融实验按组件逐步叠加，量化了相机控制（CC）、背景外推（BO）和场景变化（SV）三项关键设计的贡献（Table 3）。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2504_02004/figures/006_Table_3.jpg]]
*Table 3: Comparison of DynaScene with camera control (CC), background outpainting (BO), and scene variation (SV )*

**相机控制（CC）** 的加入带来了最显著的时序一致性提升：FVD_I3D 改善 7.7%，FVD_3DRes 改善 2.1%。这验证了 Plücker 嵌入作为显式相机姿态信号，能够有效驱动背景运动与前景运动保持同步。Figure 4 的定性对比显示，无 CC 时背景在相机平移过程中出现明显的滑动或错位伪影，而有 CC 时背景与前景的空间对齐关系得到保持。

**背景外推（BO）** 的加入使 FID 提升 1.13%，表明模型对相机移动时新显露区域的纹理生成更加真实。Figure 5 显示，无 BO 时新区域常出现模糊或重复纹理伪影，而加入 BO 后这些伪影被有效消除。

**场景变化（SV）** 在像素级和感知级指标上均带来进一步增益，使完整模型达到最优。Figure 6 的定性分析表明，SV 有助于在保持场景整体结构的前提下生成合理的局部变化，避免了背景过于静态而显得不真实的问题。

**两阶段训练策略** 的消融（Table 4）表明，相比单阶段直接进行视频训练，先图像后视频的两阶段策略使 FID 从 98.44 降至 96.18（降低 2.26），FVD_I3D 从 57.54 降至 55.84（降低 1.70）。这证实了第一阶段图像训练为模型建立了稳健的空间关系先验，第二阶段视频训练在此基础上进一步学习时间一致性，两者协同作用显著优于直接端到端视频训练。

此外，**自适应背景光照调整（ABIA）** 的定性消融（Figure 9）显示，该模块有效缓解了前景人体与生成背景之间的光照不一致问题，使整体画面光照更加协调。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2504_02004/figures/013_Figure_9.jpg]]
*Figure 9: Analyses of DynaScene w/ and w/o adaptive background illumination adjustment (ABIA). With ABIA, the overall illumination is more consistent with the foreground human*

### 失败模式与局限性

尽管 DynaScene 在整体性能上表现优异，但分析揭示了两个主要失败模式：

1. **前景运动与相机姿态冲突**：当人体前景的运动方向或尺度与相机姿态信号产生矛盾时（例如前景人物放大而相机姿态指示缩小），模型难以协调这两种冲突信号，导致生成背景出现不合理的运动或变形（Figure 10）。目前尚缺乏对该冲突容忍极限的量化分析。

2. **前景掩码质量敏感**：DynaScene 对输入的人体前景掩码质量高度依赖。当掩码提取不准确时，在前景与背景的边缘区域会出现明显的伪影或融合不佳，直接影响最终生成质量。模型对噪声掩码的鲁棒性仍有提升空间。

## 定位与知识库关联

### 任务定位与问题边界

DynaScene 解决的核心任务是**相机可控的人体视频背景生成**（camera-controllable background generation for human motion）。给定一段人体前景视频、一张静态场景图像和相机姿态序列，模型需要生成与前景运动一致、且随相机运动自然变化的背景视频。该任务处于视频生成、相机运动控制和前景-背景合成三个研究方向的交叉点。

与纯相机可控视频生成（如 **CameraCtrl** ）不同，DynaScene 的独特约束在于：背景必须与给定的静态场景图像保持语义和纹理一致性，同时前景人体区域需要被保留而非重新生成。与纯背景生成方法（如 **ActAnywhere** ）相比，DynaScene 引入了显式的相机姿态控制，使背景运动能够响应相机平移、旋转等操作。

### 与基线方法的关键差异

| 方法 | 相机控制 | 前景-背景交互 | 场景一致性 |
|------|----------|---------------|------------|
| **CameraCtrl** | 显式（Plücker嵌入） | 弱（全图生成，无前景保持机制） | 无场景图像约束 |
| **ActAnywhere** | 无 | 强（前景保留，背景生成） | 有场景图像约束 |
| **MotionCtrl** | 显式（相机运动参数） | 弱 | 无场景图像约束 |
| **DynaScene** | 显式（Plücker嵌入） | 强（前景潜变量重注入） | 有场景图像约束 + 多任务增强 |

关键差异体现在三个层面：

1. **控制信号的粒度**：CameraCtrl 和 MotionCtrl 虽然也使用相机控制，但它们生成的是完整视频帧，不区分前景与背景。DynaScene 将相机控制专门作用于背景区域，通过前景潜变量重注入公式 $h^{t} = h_{ori}^{t} \times M + h_{fore}^{t} \times (1 - M)$ 确保前景人体不被修改。这一设计使得公平比较成为可能——在实验中，作者对 CameraCtrl 和 MotionCtrl 也应用了相同的重注入策略以消除前景重建差异。

2. **场景一致性的维持机制**：ActAnywhere 通过场景图像引导背景生成，但缺乏相机控制，导致背景运动与相机轨迹脱节。DynaScene 同时引入 CLIP 编码器（高层语义）和 ReferenceNet（细粒度纹理）来锚定场景特征，使生成的背景始终与给定场景图像保持一致性。

3. **新区域生成的可靠性**：当相机移动导致原本不可见的区域进入视野时，模型需要“想象”出合理的内容。这是纯相机控制方法和纯背景生成方法都未专门处理的难题。DynaScene 通过背景外推（background outpainting）辅助任务来强化这一能力。

### 方法谱系中的继承与创新

DynaScene 的技术架构呈现明显的模块化继承特征：

- **基础生成骨架**：基于 **Stable Diffusion 1.5** 的潜空间扩散模型，继承其 VAE 编解码器和 U-Net 去噪架构。
- **时序建模**：直接集成 **AnimateDiff v2** 的运动模块（Motion Module），在 U-Net 中插入时间注意力层以实现帧间一致性。
- **相机编码**：Plücker 嵌入的相机表示形式与 CameraCtrl 一致，但 DynaScene 设计了专门的 Camera Encoder 和 Camera Adaptor（两层线性层融合）来将相机特征注入去噪过程，而非简单拼接。
- **场景理解**：CLIP + ReferenceNet 的双路径场景编码策略借鉴了图像驱动视频生成领域的设计范式。

真正的创新在于**两阶段多任务训练策略**（two-stage multi-task training）：

- **第一阶段（图像训练）**：在静态图像上训练背景外推（随机遮挡修复）和场景变化（同一场景的不同视角/光照），让模型先学习空间维度的场景理解能力。
- **第二阶段（视频训练）**：在视频序列上联合训练背景生成、背景外推和场景变化三个任务，让模型在已有空间理解的基础上学习时间一致性。

这种“先空间、后时间”的训练哲学是 DynaScene 区别于其他方法的核心设计选择。消融实验（Table 4）证实，两阶段训练相比单阶段训练在 FID 上降低 2.26，在 FVD_I3D 上降低 1.70，验证了分阶段学习的有效性。

### 适用边界与已知局限

**适用场景**：
- 相机运动幅度适中、前景人体运动与相机运动方向一致的视频。
- 场景图像与目标背景在语义类别上匹配（如室内场景对应室内背景）。
- 前景掩码质量较高、人体轮廓清晰的情况。

**已知失效模式**：

1. **前景-相机运动冲突**：当人体前景的运动方向与相机姿态暗示的背景运动方向相矛盾时（例如人体向前放大但相机在后退缩小），模型难以生成合理结果（见 Figure 10）。这说明模型对物理一致性的理解仍有限，本质上是在学习统计相关性而非物理规律。

2. **掩码质量敏感**：前景掩码的精度直接影响生成质量。不准确的掩码会在前景-背景边缘产生明显伪影或融合不佳。这是一个级联式脆弱性——掩码误差会被扩散模型的迭代去噪过程放大。

3. **极端光照不匹配**：虽然论文提出了自适应背景光照调整（ABIA）来缓解前景与背景的光照不一致（见 Figure 9），但在极端光照差异场景下（如强逆光前景配暗色背景），该机制的有效性仍需进一步验证。

### 开放问题与后续方向

1. **冲突容忍的量化边界**：前景运动与相机姿态之间的冲突程度如何量化？模型在多强的冲突下会从“生成质量下降”过渡到“完全失效”？目前仅有定性示例，缺乏系统性的鲁棒性测试。

2. **多模态相机控制的扩展**：当前相机控制仅限于姿态参数，是否可以将镜头焦距、景深、运动模糊等更丰富的相机属性纳入控制空间？这将使生成结果更接近真实摄影。

3. **实时性与计算效率**：基于扩散模型的多步去噪过程限制了实时应用。是否可以通过蒸馏、一致性模型等技术将推理速度提升到交互级别？

4. **泛化到非人体前景**：DynaScene 的设计以人体前景为核心假设（使用人体掩码、人体视频数据集）。将其扩展到通用前景对象（动物、车辆等）需要重新审视掩码提取和运动先验的设计。

5. **场景图像与视频背景的语义鸿沟**：当场景图像与视频中实际需要的背景存在语义差异时（如场景图像是客厅但视频中人物走到了厨房区域），模型如何决定何时“忠于场景图像”何时“合理外推”？这涉及到场景理解的更高层次语义推理。

## 原文 PDF

![[paperPDFs/arxiv_2025/Beyond_Static_Scenes_Camera_controllable_Background_Generation_for_Human_Motion.pdf]]
