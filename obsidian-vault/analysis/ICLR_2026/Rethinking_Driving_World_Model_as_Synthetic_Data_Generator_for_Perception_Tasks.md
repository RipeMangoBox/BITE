---
title: Rethinking Driving World Model as Synthetic Data Generator for Perception Tasks
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Rethinking_Driving_World_Model_as_Synthetic_Data_Generator_for_Perception_Tasks_e3902bf4ec4f.pdf
project_link: "https://wm-research.github.io/Dream4Drive/"
code_link: null
aliases:
- RDWMASDGPT
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: Rethinking
primary_logic: Rethinking
claims:
- Rethinking
---

# Rethinking Driving World Model as Synthetic Data Generator for Perception Tasks

> [!tip] 核心洞察
> Rethinking

| 字段 | 内容 |
|------|------|
| 中文题名 | Rethinking Driving World Model as Synthetic Data Generator for Perception Tasks |
| 英文题名 | Rethinking Driving World Model as Synthetic Data Generator for Perception Tasks |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=z3cFADf6zZ) · [Project](https://wm-research.github.io/Dream4Drive/) · [arXiv](https://arxiv.org/abs/2602.11144) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method |  |
| Dataset | nuScenes, DriveObj3D |
## 概述

自动驾驶感知模型对训练数据的需求极为庞大，但真实世界数据的采集与标注成本高昂，且难以覆盖长尾场景。现有数据增强方法往往难以在保持几何一致性的同时提供足够的外观多样性。Dream4Drive 提出了一种**3D感知的合成数据生成框架**，其核心思路是：首先将输入视频分解为多张3D感知引导图（深度、法线、边缘、抠图、掩码），随后将多样化的3D资产渲染到这些引导图上，通过视频扩散模型生成几何一致且外观多样的合成视频。

该框架的关键优势在于**数据效率极高**。在相同的训练轮次（1×、2×、3×）下，Dream4Drive 仅需 **420个合成样本（不足真实样本的2%）**，即可在 nuScenes 检测与跟踪任务上超越此前的数据增强基线方法。值得注意的是，在2×训练设置下，仅使用真实数据训练的模型在 mAP 和 NDS 上反而高于混合真实与合成数据训练的模型，这揭示了合成数据质量与数量之间的微妙权衡。

Dream4Drive 的方法定位介于**3D资产驱动仿真**与**生成式视频编辑**之间：它不依赖昂贵的3D标注，仅需RGB视频和3D感知引导图即可训练；同时通过多条件融合适配器将五种引导信号注入扩散Transformer，实现了对场景几何和外观的精细控制。主要结果验证了少样本合成数据对下游感知任务的显著提升效果，为自动驾驶数据增强开辟了新的技术路径。

## 背景与动机

自动驾驶感知模型依赖大规模标注数据，但真实场景的采集与标注成本高昂，且长尾场景覆盖不足。数据增强可缓解这一问题，然而现有方法存在结构性缺陷：**传统增强**（如复制-粘贴）仅操作2D图像平面，缺乏3D几何一致性，导致前景物体与背景的遮挡、尺度、光照不匹配；**基于NeRF/3DGS的场景重建方法**虽能生成多视角一致数据，但依赖昂贵的3D标注，且编辑灵活性受限——难以在指定3D位置插入多样化物体。

近期扩散模型在图像/视频生成上展现出强大能力，为数据合成提供了新路径。但直接将扩散模型用于驾驶场景编辑面临关键瓶颈：**隐式3D控制不足**。纯2D生成模型难以精确指定物体的3D位姿，也无法保证前景与背景在深度、法向、边缘层面的几何对齐，导致合成数据在几何真实性和标注精度上出现退化，进而损害下游感知任务的训练效果。

针对上述缺口，本文提出**Dream4Drive**，一个3D感知的合成数据生成框架。其核心动机是：通过引入**密集3D感知引导图**（深度、法向、边缘、物体轮廓、掩码）作为扩散模型的条件控制信号，在保持原始视频几何结构的前提下，实现3D资产的精确插入与外观多样化编辑。该框架不依赖昂贵的3D标注，仅需RGB视频即可训练，旨在以极少量合成样本（<2%）显著提升感知模型的检测与跟踪性能。

## 核心创新

Dream4Drive 的核心创新在于将自动驾驶数据增广从“隐式生成”或“简单粘贴”推进到**3D 感知引导的视频编辑**范式。与现有基于世界模型或扩散模型的增广方法相比，Dream4Drive 在三个关键维度上做出了根本性改变：

**1. 从 2D 粘贴到 3D 感知场景编辑**

传统的数据增广方法（如 Copy-Paste 或 Naive Insert）直接将物体图像投影到场景中，忽略了 3D 几何一致性，导致合成数据出现透视错误、遮挡不自然等问题。Dream4Drive 首次将视频编辑形式化为一个 **3D 感知的渲染问题**：先对输入视频进行 3D 感知分解，获得稠密的引导图（深度图、法线图、边缘图、抠图、掩码图），再将 3D 资产渲染到这些引导图上。这一 changed slot 使得合成数据在几何上与原始场景保持一致，同时保留了背景的外观细节。

**2. 稠密 3D 感知引导图替代隐式控制**

现有视频编辑方法通常依赖文本或稀疏控制信号（如关键点），难以精确约束物体的 3D 位置和场景几何。Dream4Drive 引入了一种新的 **3D 感知引导图** 形式，包括深度（Depth）、法线（Normal）、边缘（Edge）、抠图（Cutout）和掩码（Mask）五类稠密信号。这些引导图通过一个 **多条件融合适配器（FusionNet）** 注入到扩散 Transformer 中，公式化为：

$$\mathcal{F}_{\mathrm{fusion}} = \mathrm{FusionNet}\left( \bigoplus_{k=1}^{5} \mathrm{3DEmbedder}_k(\mathrm{VAE}(\mathcal{C}_k)) ~ \Big| ~ \mathcal{C}_k \in \{D,N,E,O,M\} \right)$$

这一设计使得模型能够同时感知场景的几何结构、物体边界和前景-背景关系，从而实现精确的 3D 位置编辑。

**3. 仅需 2% 合成样本的高效增广**

与需要大规模合成数据或复杂 3D 标注的方法不同，Dream4Drive 在训练时**不需要任何昂贵的 3D 标注**，仅依赖 RGB 视频和自动提取的 3D 感知引导图。实验表明，在相同训练轮次下，仅插入 **420 个合成样本（不足原始数据量的 2%）** 即可在 nuScenes 检测任务上超越使用全部合成数据的先前方法。这一 changed slot 的关键在于：3D 感知引导图提供了强几何先验，使得少量合成样本就能有效覆盖长尾分布中的几何和外观变化。

**与 baseline 的本质差异总结**：Dream4Drive 将自动驾驶数据增广从“生成新图像”重新定义为“编辑已有视频”，并通过稠密 3D 感知引导图实现了**几何一致性、外观多样性和标注精确性**的统一，而这是隐式生成模型（如 DrivingDiffusion）或简单粘贴方法无法同时保证的。

## 整体框架

Dream4Drive 是一个面向自动驾驶感知的 3D‑aware 合成数据生成框架。其核心思路是：**先对输入视频进行 3D‑aware 的几何‑外观解耦，再在解耦后的引导图空间上渲染 3D 资产，最后通过条件生成模型合成具有几何一致性和外观多样性的编辑视频**。整个 pipeline 可划分为三个主要阶段。

**阶段一：3D‑aware 引导图提取。** 对原始视频的每一帧，同时提取五类密集的 3D‑aware 引导图（guidance maps）：深度图（depth）、法向图（normal）、边缘图（edge）、抠图（cutout）和掩膜（mask）。这些引导图共同编码了场景的几何结构与物体边界信息，为后续的前景‑背景合成提供显式的 3D 约束。

**阶段二：3D 资产渲染与引导图融合。** 在选定的 3D 位置上，将目标 3D 资产投影到场景中，渲染出物体图像和物体掩膜，并与阶段一提取的背景引导图进行组合。此时形成的是一个多通道的条件信号集合，包括背景的深度、法向、边缘、抠图以及前景物体的掩膜和外观信息。

**阶段三：多条件融合的视频生成。** 将上述五类引导图分别通过 VAE 编码后送入各自的 3D Embedder，再经由一个 **FusionNet** 进行多条件融合，得到统一的融合特征 $\mathcal{F}_{\mathrm{fusion}}$：

$$
{\cal F}_{\mathrm{fusion}} = \mathrm{FusionNet}\left( \bigoplus_{k=1}^{5} 3\mathrm{DEmbedder}_k(\mathrm{VAE}({\cal C}_k)) ~ \Big| ~ {\cal C}_k \in \{D,N,E,O,M\} \right)
$$

该融合特征作为条件 $\mathbf{c}$ 注入到扩散 Transformer 的反向去噪过程中：

$$
p_{\theta}(\mathbf{z}_{t-1}|\mathbf{z}_t,\mathbf{c}) = \mathcal{N}(\mathbf{z}_{t-1}; \mu_{\theta}(\mathbf{z}_t,t,\mathbf{c}), \boldsymbol{\Sigma}_{\theta}(\mathbf{z}_t,t,\mathbf{c}))
$$

最终生成编辑后的视频帧。训练时，总损失为扩散损失、掩膜损失和 LPIPS 损失的加权和：

$$
L_{\mathrm{total}} = \lambda_{\mathrm{diffusion}} \mathcal{L}_{\mathrm{diffusion}} + \lambda_{\mathrm{mask}} \mathcal{L}_{\mathrm{mask}} + \lambda_{\mathrm{lpips}} \mathcal{L}_{\mathrm{LPIPS}}
$$

其中权重经验性地设为 $\lambda_{\mathrm{diffusion}}=1.0$，$\lambda_{\mathrm{mask}}=0.1$，$\lambda_{\mathrm{lpips}}=0.1$。

**输入输出流总结：** 输入为原始 RGB 视频和待插入的 3D 资产，输出为编辑后的视频及其精确的 3D 标注（bounding box、track ID 等）。整个训练过程**不需要昂贵的 3D 标注**，仅依赖 RGB 视频和可自动提取的 3D‑aware 引导图。

**关键设计决策：** 与以往依赖隐式 3D 控制或简单投影的方法不同，Dream4Drive 通过显式的密集 3D‑aware 引导图来保持原始视频的几何与外观，同时允许在任意 3D 位置灵活插入多样化的资产，从而在几何一致性和外观多样性之间取得平衡。

## 核心模块与公式推导

### 3D‑Aware 视频编辑流水线

Dream4Drive 的核心流水线由两个级联模块构成：**3D‑Aware 场景编辑** 与 **3D‑Aware 视频渲染**。

**场景编辑模块**（Figure 3）负责将目标 3D 资产嵌入到原始视频帧中。给定输入图像，首先提取背景的深度图、法线图和边缘图，同时渲染目标 3D 资产的对象图像与对象掩码。这五类信息构成 **密集 3D‑Aware 引导图**（dense 3D‑aware guidance maps），分别记为深度图 $D$、法线图 $N$、边缘图 $E$、对象切图 $O$ 和掩码 $M$。引导图的作用是显式编码场景几何与前景‑背景空间关系，为后续生成提供强约束。

**视频渲染模块**（Figure 4）以引导图为条件，驱动扩散 Transformer 生成编辑后的视频帧。该模块的核心是 **多条件融合适配器**（multi‑condition fusion adapter），它将五类引导图分别通过 VAE 编码后，送入各自的 3D Embedder，再由 FusionNet 融合为统一的条件表示：

$${\mathcal F}_{\mathrm{fusion}} = \mathrm{FusionNet}\left( \bigoplus_{k=1}^{5} \mathrm{3DEmbedder}_k(\mathrm{VAE}({\mathcal C}_k)) ~ \Big| ~ {\mathcal C}_k \in \{D,N,E,O,M\} \right)$$

其中 $\bigoplus$ 表示沿通道维度的拼接操作。融合后的特征注入扩散 Transformer 的交叉注意力层，实现几何一致且外观多样的视频生成。

### 扩散模型基础与条件化

Dream4Drive 的生成骨干基于 latent diffusion model。前向扩散过程在隐空间逐步加噪：

$$q(\mathbf{z}_t | \mathbf{z}_0) = \mathcal{N}(\mathbf{z}_t; \sqrt{\bar{\alpha}_t} \mathbf{z}_0, (1 - \bar{\alpha}_t) \mathbf{I})$$

其中 $\mathbf{z}_0$ 为 VAE 编码的隐变量，$\bar{\alpha}_t$ 为累积噪声调度系数。反向去噪过程由神经网络参数化：

$$p_{\theta}(\mathbf{z}_{t-1} \vert \mathbf{z}_t) = \mathcal{N}(\mathbf{z}_{t-1}; \mu_{\theta}(\mathbf{z}_t, t), \boldsymbol{\Sigma}_{\theta}(\mathbf{z}_t, t))$$

为引入 3D‑Aware 引导，条件变量 $\mathbf{c}$（即融合后的引导图特征）被注入反向过程：

$$p_{\theta}(\mathbf{z}_{t-1}|\mathbf{z}_t,\mathbf{c}) = \mathcal{N}(\mathbf{z}_{t-1}; \mu_{\theta}(\mathbf{z}_t,t,\mathbf{c}), \boldsymbol{\Sigma}_{\theta}(\mathbf{z}_t,t,\mathbf{c}))$$

### 训练目标

训练损失由三项加权组成：

$$L_{\mathrm{total}} = \lambda_{\mathrm{diffusion}} \mathcal{L}_{\mathrm{diffusion}} + \lambda_{\mathrm{mask}} \mathcal{L}_{\mathrm{mask}} + \lambda_{\mathrm{lpips}} \mathcal{L}_{\mathrm{LPIPS}}$$

- $\mathcal{L}_{\mathrm{diffusion}}$：标准扩散去噪损失，驱动生成帧逼近真实帧。
- $\mathcal{L}_{\mathrm{mask}}$：掩码损失，约束编辑区域与目标掩码 $M$ 一致，防止前景‑背景泄漏。
- $\mathcal{L}_{\mathrm{LPIPS}}$：感知损失，提升生成帧的视觉保真度。

权重经验设置为 $\lambda_{\mathrm{diffusion}}=1.0$，$\lambda_{\mathrm{mask}}=0.1$，$\lambda_{\mathrm{lpips}}=0.1$。训练仅需 RGB 视频及其 3D‑Aware 引导图，无需昂贵的 3D 标注。

### 补充图表

![[assets/figures/papers/paper_list_l69_https_openreview_net_forum_id_z3cFADf6zZ/figures/003_Figure_3.jpg]]
*Figure 3: The illustration of 3D-aware scene editing. Given the input images, we first obtain the depth map, normal map, and edge map for the background and then render the object image and object mask for the target 3D asset*

![[assets/figures/papers/paper_list_l69_https_openreview_net_forum_id_z3cFADf6zZ/figures/004_Figure_4.jpg]]
*Figure 4: The illustration of 3D-aware video rendering. Given the 3D-aware guidance maps, we employ a multi-condition fusion adapter to control the video generation of a diffusion transformer, rendering the edited video*

![[assets/figures/papers/paper_list_l69_https_openreview_net_forum_id_z3cFADf6zZ/figures/005_Figure_5.jpg]]
*Figure 5: The illustration of creating a 3D asset in DriveObj3D. We first apply a segmentation model to segment the target object, then generate multi-view images, and finally create a 3D mesh from those images*

## 实验与分析

### 主实验结果

Dream4Drive 在 nuScenes 检测与跟踪任务上验证了合成数据的有效性。核心发现是：**仅需 420 个合成样本（不足真实样本的 2%），即可持续提升下游感知性能**，且这一增益在不同训练轮次（1×、2×、3×）下均稳定存在。

在检测任务上，Dream4Drive 在 2× 训练轮次下取得 **mAP 38.7 / NDS 50.6** 的最佳结果，显著优于此前基于世界模型的合成数据增强方法。值得注意的是，此前方法通常需要全量合成数据才能获得增益，而 Dream4Drive 仅用 420 个插入样本即实现超越（Table 1）。在高分辨率（512×768）设定下，Dream4Drive 带来 **4.6 点 mAP 提升（12.7%）和 4.1 点 NDS 提升（8.6%）**（Table 3）。

![[assets/figures/papers/paper_list_l69_https_openreview_net_forum_id_z3cFADf6zZ/figures/010_Table_3.jpg]]
*Table 3: Detection performance under different training epochs (1x, 2x, 3x). “Naive Insert” denotes the direct projection of 3D assets into the original scene. Results are reported at 512×768 resolution*

跟踪任务同样受益：在 1×、2×、3× 训练轮次下，Dream4Drive 的合成数据均带来一致的跟踪性能改善（Table 2, Table 4）。作为对照，“Naive Insert”（直接将 3D 资产投影到原始场景）的性能显著低于 Dream4Drive，验证了 3D 感知引导图在保持几何一致性与视觉真实感方面的关键作用。

![[assets/figures/papers/paper_list_l69_https_openreview_net_forum_id_z3cFADf6zZ/figures/009_Table_2.jpg]]
*Table 2: Comparison of tracking under different training epochs*

![[assets/figures/papers/paper_list_l69_https_openreview_net_forum_id_z3cFADf6zZ/figures/012_Table_4.jpg]]
*Table 4: Tracking performance under different training epochs (1x, 2x, 3x). “Naive Insert” denotes the direct projection of 3D assets into the original scene. Results are reported at 512×768 resolution*

一个反直觉的发现来自 Figure 1：**在 2× 训练轮次下，仅使用真实数据训练的模型在 mAP 和 NDS 上反而高于混入合成数据的模型**。这表明合成数据的增益并非单调递增，其有效性与训练轮次存在交互效应——在特定训练饱和点，合成数据可能引入分布偏移而非正向增强。这一现象在后续缩放分析中得到进一步验证。

![[assets/figures/papers/paper_list_l69_https_openreview_net_forum_id_z3cFADf6zZ/figures/001_Figure_1.jpg]]
*Figure 1: Dream4Drive demonstrates the effectiveness of synthetic data: with fewer than 2% synthetic samples, it consistently improves detection and tracking across epochs, outperforming previous data augmentation baselines under fair evaluation. 1× denotes the baseline training epochs; 2× and 3× represent twofold and threefold increases, respectively*

### 消融实验

**插入位置与视角分析**（Table 5）：按方位划分，前方与后方插入的性能相近，而左侧插入（mAP 40.2, NDS 51.6）显著优于右侧（mAP 39.8, NDS 50.7），mAOE 指标（45.7 vs 51.4）进一步揭示右侧插入引入了更大的朝向误差。按距离划分，近距离插入（mAP 39.7）劣于中距离（40.3）和远距离（40.5），推测原因是近距离资产遮挡相机视野，破坏了场景的感知完整性。

**3D 方法对比**（Table 5）：Dream4Drive 使用的 3D 感知引导图方案在所有对比中均优于朴素的 2D 粘贴和仅使用深度图的方案，验证了多模态 3D 引导（深度、法线、边缘、抠图、掩码）对合成质量的关键作用。

**资产质量评估**（Table 7）：使用 CLIP Image Similarity 和 DINO Image Similarity 评估合成资产与真实资产的相似度。Dream4Drive 的 DriveObj3D 资产生成流程（Figure 5, Figure 6）在多个类别上优于现有基线，为后续视频编辑提供了高质量的 3D 素材基础。

**缩放分析**（Table 8）：增加 OOD 场景数量并不必然带来性能提升。这一发现与 Figure 1 中的反直觉现象一致——合成数据的增益存在边际递减甚至负效应，盲目的数据堆砌并非有效策略。

**风格迁移的 OOD 数据**（Table 9）：对环境进行风格迁移以增加环境多样性，可全面提升下游感知指标，表明外观多样性是合成数据增益的重要维度。

**类别消融**（Table 10）：按资产类别进行消融，报告各类别的 AP 指标，揭示不同类别对合成数据增强的敏感度存在差异。

**自动化程度**（Table 6）：合成 420 个样本所需的人工与自动化工作量对比，展示了 Dream4Drive 流程的高效性——核心步骤由自动化管线完成，仅需有限的人工介入。

### 关键图表结论

- **Figure 1**：合成数据增益与训练轮次存在非单调关系；在 2× 轮次下纯真实数据反超混合数据，提示合成数据的有效性窗口需要谨慎选择。
- **Table 1**：Dream4Drive 以 <2% 合成样本超越此前全量合成数据方法，验证了“质量优于数量”的合成数据策略。
- **Table 5**：插入位置（左侧 vs 右侧、近距离 vs 远距离）对性能有显著影响，右侧和近距离插入是失败模式的高发区域。
- **Table 8**：OOD 样本数量的增加不保证性能提升，合成数据的缩放策略需要更精细的设计。

![[assets/figures/papers/paper_list_l69_https_openreview_net_forum_id_z3cFADf6zZ/figures/013_Table_5.jpg]]
*Table 5: Ablation Studies. We report detection performance across insertion positions and asset, with best results per block (Views, Distances, 3D Methods) in bold, at 512×768 resolution*

![[assets/figures/papers/paper_list_l69_https_openreview_net_forum_id_z3cFADf6zZ/figures/016_Table_8.jpg]]
*Table 8: Scaling analysis with increasing numbers of OOD scenes under different training epochs. More OOD samples do not necessarily yield better performance*

### 失败模式与局限

1. **插入位置敏感性**：右侧插入和近距离插入是明确的性能瓶颈。右侧插入导致更大的朝向误差（mAOE 51.4 vs 左侧 45.7），近距离资产因遮挡相机视野而降低检测精度。
2. **训练轮次交互**：合成数据并非在所有训练阶段都有效。在 2× 轮次下，纯真实数据表现更优，说明合成数据可能引入分布偏移，在模型已充分拟合真实分布时反而造成干扰。
3. **缩放不稳定性**：OOD 样本数量的增加不带来单调增益，表明当前的合成数据生成策略在规模化时面临质量-数量权衡问题。

### 补充图表

![[assets/figures/papers/paper_list_l69_https_openreview_net_forum_id_z3cFADf6zZ/figures/006_Figure_6.jpg]]
*Figure 6: Comparison of 3D asset generation across different methods. Our simple yet effective method produces better 3D assets across diverse categories in autonomous driving, outperforming existing baselines. Con vehicle is construction vehicle; Pdes is Pedestrian; T cone is traffic cone*

![[assets/figures/papers/paper_list_l69_https_openreview_net_forum_id_z3cFADf6zZ/figures/017_Table_9.jpg]]
*Table 9: Effect of style-transferred OOD synthetic data. Adding environmental diversity improves all downstream perception metrics*

![[assets/figures/papers/paper_list_l69_https_openreview_net_forum_id_z3cFADf6zZ/figures/014_Table_6.jpg]]
*Table 6: Automation and manual efforts involved in synthesizing the 420 samples*

## 方法谱系与知识库定位

### 与现有数据增强范式的边界

Dream4Drive 定位于**基于生成模型的 3D 感知数据增强**，与三类现有方法形成明确边界：

1. **基于图形学渲染的合成数据**（如 sim-to-real 域迁移）：依赖人工建模的 3D 场景和物理渲染器，成本高且域间隙显著。Dream4Drive 以真实视频为背景、仅替换前景资产，天然规避了全局渲染的域间隙问题。

2. **基于 2D 生成式编辑的数据增强**（如 copy-paste 或图像级扩散编辑）：缺乏 3D 一致性，插入物体与场景的几何关系（遮挡、深度、光照）不可靠。Dream4Drive 通过密集 3D 感知引导图（深度、法线、边缘、抠图、掩码）显式约束前景-背景合成，这是其与 2D 编辑方法的**核心分水岭**。

3. **驾驶世界模型**（如 driving world model 类方法）：通常以生成未来帧或重建场景为目标，并非专为感知数据增强设计。Dream4Drive 的定位是“用世界模型的生成能力服务于感知任务”，在 nuScenes 检测任务上，仅用 420 个合成样本（不足真实样本的 2%）即可超越先前使用全量合成数据的方法（Table 1），表明其合成数据的“质”而非“量”构成优势。

### 适用边界

- **场景类型**：方法设计围绕自动驾驶街景视频，背景为静态或准静态场景（相机运动、环境光照相对稳定）。对高度动态背景（如密集人群、剧烈光照变化）的适用性未经验证。
- **资产类型**：DriveObj3D 覆盖的类别包括车辆、行人、施工车辆等典型道路参与者。对于细粒度罕见类别或非刚性物体的编辑能力，原文未提供证据。
- **感知任务**：当前验证集中在 3D 目标检测和跟踪（nuScenes 基准）。对在线建图、轨迹预测、占用网络等下游任务的可迁移性属于开放问题。
- **数据效率**：在 2× 训练轮次下达到最优，3× 轮次下增益趋于饱和（Table 3），提示合成数据的边际收益存在上限。

### 局限与开放问题

#### 已识别的局限

1. **近距离插入退化**：消融实验（Table 5）显示，当 3D 资产插入位置过近时（Close: mAP 39.7），性能低于中远距离插入（Mid: 40.3, Far: 40.5）。原文归因于资产遮挡相机视野，这暴露了该方法对插入位置敏感的特性。

2. **左右插入不对称**：左侧插入（mAP 40.2, NDS 51.6）显著优于右侧插入（mAP 39.8, NDS 50.7）。这一不对称性可能源于 nuScenes 数据分布或相机安装位置的偏置，原文未深入分析其成因。

3. **仅验证单帧编辑的时序一致性**：方法以视频为输入输出，但定量评估仅针对逐帧检测/跟踪性能，未直接度量编辑视频的时序闪烁（temporal flickering）或几何抖动。

#### 开放问题

- **3D 资产质量的下游影响**：DriveObj3D 生成的 3D 网格质量（Figure 6）如何定量影响感知模型性能？缺乏资产质量与下游指标之间的归因分析。
- **引导图精度的鲁棒性**：方法依赖深度、法线等引导图的精度。若引导图来自不完美的单目估计器，编辑质量会如何退化？原文未进行引导图噪声的敏感性分析。
- **跨传感器泛化**：当前仅验证单目相机数据。对激光雷达点云、环视多相机等传感器配置的适配方案未讨论。
- **合成数据的最优比例**：420 个样本（<2%）即有效，但该比例是否最优？是否存在合成数据占比的“甜点区”？原文未进行比例扫描实验。

> **注意**：以上开放问题均基于原文未覆盖的分析维度推断，需后续工作验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Rethinking_Driving_World_Model_as_Synthetic_Data_Generator_for_Perception_Tasks_e3902bf4ec4f.pdf]]
