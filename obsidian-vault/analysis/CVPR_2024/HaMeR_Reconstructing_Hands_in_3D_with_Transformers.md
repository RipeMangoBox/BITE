---
title: HaMeR Reconstructing Hands in 3D with Transformers
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/HaMeR_Reconstructing_Hands_in_3D_with_Transformers.pdf
project_link: https://geopavlakos.github.io/hamer/
code_link: https://github.com/openmmlab/mmpose
aliases:
- HRH3T
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 同时扩大训练数据规模（4倍达2.7M样本）和采用高容量ViT-H Transformer架构。
primary_logic: 通过一个简单的全Transformer设计，结合大规模数据和超大模型容量，可以显著提升手部网格恢复的准确性和鲁棒性，尤其在野外图像上提升巨大。
claims:
- 扩大数据规模和模型容量是性能提升的关键因素
- 在HInt野外数据集上，PCK@0.05指标相比先前工作提升2-3倍
- 在FreiHAND和HO3Dv2标准基准上取得最先进结果，大多数指标优于先前方法
- 消融实验证实，单独扩大数据或模型容量分别带来提升，两者结合效果最佳
---

# HaMeR Reconstructing Hands in 3D with Transformers

> [!tip] 核心洞察
> 通过一个简单的全Transformer设计，结合大规模数据和超大模型容量，可以显著提升手部网格恢复的准确性和鲁棒性，尤其在野外图像上提升巨大。

| 字段 | 内容 |
|------|------|
| 中文题名 | HaMeR：基于Transformer的3D手部重建 |
| 英文题名 | HaMeR Reconstructing Hands in 3D with Transformers |
| 会议/期刊 | CVPR 2024 |
| Links | [Project](https://geopavlakos.github.io/hamer/) · [Code](https://github.com/openmmlab/mmpose) · [paper](https://arxiv.org/abs/2312.05251) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HaMeR |
| Dataset | FreiHAND, HO3Dv2, HInt |

> [!tip] 效果简介
> - FreiHAND 上，PA-MPVPE (mm) 5.7 vs 5.8 (MobRecon) (-0.1)。
> - HO3Dv2 上，PA-MPJPE (mm) 7.7 vs 8.3 (AMVUR) (-0.6)。
> - HInt (New Days subset) 上，PCK@0.05 (所有关键点) 48.0 vs 先前方法（未指定） (约2-3倍提升)。

## 概要

**问题瓶颈**：现有3D手部重建方法通常在受限环境下训练，且模型容量有限，导致在非受控场景中鲁棒性不足——不同视角、遮挡、手-物交互等条件下性能退化严重。

**核心洞察**：同时扩大训练数据规模（4倍，达2.7M样本）和采用高容量ViT-H Transformer架构，可以显著提升手部网格恢复的准确性和鲁棒性。这一策略在野外图像上的提升尤为巨大。

**方法定位**：HaMeR采用全Transformer设计，以ViT-H为骨干提取图像令牌特征，通过Transformer解码器直接回归MANO手部模型的姿态、形状和相机参数，属于参数化手部网格恢复路线。相比基于CNN的基线（如**FrankMocap**，Rong et al., ICCV 2021），HaMeR在架构风格和模型容量上进行了根本性升级。

**主要结果**：
- 在HInt野外基准上，PCK@0.05指标相比先前工作提升约2–3倍。
- 在FreiHAND和HO3Dv2标准基准上取得最先进结果，大多数指标优于先前方法。
- 消融实验证实：单独扩大数据或模型容量分别带来提升，两者结合效果最佳。

**局限**：大规模ViT-H模型计算成本高，不适用于移动端或实时应用；依赖MANO参数模型，对手部细节表达有限；单帧方法未利用时序信息。



从单张RGB图像中恢复准确的三维手部网格，是计算机视觉中的一个基础性问题，在增强现实、人机交互和机器人操作等领域有着广泛的应用需求。手部具有高度灵活的关节结构、频繁的自遮挡和物体交互，且在野外图像中常伴随运动模糊、极端视角和复杂光照，这使得单目3D手部重建成为一个极具挑战性的任务。

### 现有方法的瓶颈

当前3D手部重建方法面临两个根本性限制。**第一，训练环境受限**：大多数方法在控制良好的实验室数据集上进行训练和评估，这些数据集通常由少量受试者在理想光照和简单背景下采集，难以覆盖真实世界中丰富多变的手部外观和交互模式。当迁移到非受控的野外场景时——例如不同拍摄视角（第三人称或第一人称）、手部与物体的复杂交互、双手交互、不同肤色、佩戴手套等情形——这些方法的鲁棒性急剧下降。**第二，模型容量有限**：主流方法多基于中等规模的CNN骨干网络（如ResNet50），其表征能力不足以从大规模多样化数据中学习鲁棒的手部先验。这一容量瓶颈与数据扩展需求之间的矛盾，构成了当前方法的深层结构性缺陷。

### 核心动机与假设

HaMeR的核心假设是：**通过同时扩大训练数据规模和采用高容量的Transformer架构，可以大幅提升野外手部网格重建的准确性和鲁棒性**。这一假设建立在两个关键观察之上：其一，手部重建任务本质上需要强语义理解能力，以应对遮挡、视角变化和交互等复杂情形，而Transformer架构在建模长距离依赖和全局上下文方面具有天然优势；其二，现有训练数据虽然分散在多个数据集中，但总量足以支撑大模型训练，关键在于如何有效整合。HaMeR试图验证，一个简单的全Transformer设计——将ViT-H骨干与Transformer解码器头结合——在足够的数据支撑下，能否超越复杂的专用方法，成为野外手部重建的通用解决方案。



## 核心方法与创新机理

HaMeR 的核心创新并非提出复杂的算法模块，而是通过**同时扩大训练数据规模与模型容量**，以极简的全 Transformer 架构实现了 3D 手部重建在野外场景下的鲁棒性跃升。这一思路从根本上回应了先前方法的瓶颈：现有工作在受限环境下训练、模型容量有限，难以泛化到遮挡、手-物交互、不同视角等非受控场景。

具体而言，HaMeR 在三个关键维度上对基线方法进行了系统性改变：

- **骨干网络**：从 **FrankMocap**（Rong et al., ICCV 2021）等基线使用的 ResNet50（CNN）替换为 ViT-H（Vision Transformer），将特征提取从局部卷积范式切换为全局自注意力范式。这一改变使模型具备了更大的感受野和更强的上下文建模能力（Section 3.3）。

- **训练数据规模**：将训练集从 FrankMocap 的约 0.7M 样本扩大至 2.7M 样本（4 倍），整合了多个带手部标注的数据集，包括 Hands23、Epic-Kitchens、Ego4D 等来源。更大规模的数据覆盖了更多样的视角、遮挡和交互场景，为高容量模型提供了充分的训练信号（Section 3.5）。

- **架构风格**：从基于 CNN 的编码器-解码器设计，转向**全 Transformer 设计**——ViT 骨干提取图像令牌后，直接通过一个 Transformer 解码器头（以交叉注意力处理一个查询令牌）回归 MANO 参数和相机参数。整个流程去除了 CNN 特有的归纳偏置，以更统一的方式完成从像素到参数的映射（Section 3.3）。

消融实验（Table 5）为上述创新提供了因果证据：在保持 ResNet50 架构不变的情况下，仅将训练数据扩大 4 倍，即可在 HInt 基准上获得一致的性能提升；同样，保持小训练集不变，仅将骨干替换为 ViT-H，也能带来改进。而**同时采用两项改变（即 HaMeR）取得了远超其他版本的最佳结果**，证实了大数据与大模型的协同效应是性能突破的决定性因素。

从方法谱系来看，HaMeR 延续了 **FrankMocap** 的参数化回归范式（回归 MANO 参数而非直接回归顶点），但通过 Transformer 架构和数据规模的双重放大，使其摆脱了 CNN 小模型的泛化局限。相比 **METRO**（Lin et al., CVPR 2021）和 **Mesh Graphormer**（Lin et al., ICCV 2021）等非参数化 Transformer 基线，HaMeR 以更简单的设计（参数化输出 + 全 Transformer）取得了更优的鲁棒性，尤其在运动模糊、手-手交互、手-物交互等困难场景下优势显著（Figure 3）。



HaMeR 采用一种简洁的全 Transformer 设计，将单目 RGB 图像直接映射为 MANO 手部模型的姿态、形状及相机参数，进而恢复完整的 3D 手部网格与关键点。整个 pipeline 由四个核心模块串联构成，数据流清晰且无复杂多阶段设计。

**输入与预处理**：网络接收一张裁剪后的手部区域 RGB 图像。训练时，该图像来自作者构建的大规模 HInt 数据集（涵盖 Hands23、Epic-Kitchens VISOR、Ego4D 等多个来源，总计 2.7M 训练样本），同时提供 21 个 2D 关键点标注及其遮挡标签。

**ViT 骨干网络**：图像首先送入一个大规模 Vision Transformer 骨干网络（ViT-H），将输入图像分块并提取为序列化的令牌特征。ViT-H 的高容量特性是方法成功的关键因素之一——消融实验表明，仅将 ResNet50 替换为 ViT-H 即可在小训练集上带来一致的性能提升（Table 5, row 4 vs row 2）。

**Transformer 解码器头**：骨干网络输出的令牌特征被送入一个 Transformer 解码器头。该解码器通过交叉注意力机制处理一个可学习的查询令牌，直接回归出参数集 $\Theta = \{\theta, \beta, \pi\}$，其中 $\theta$ 为 MANO 姿态参数，$\beta$ 为形状参数，$\pi$ 为相机参数（包含内参 $K$ 和平移 $t$）。整个映射可形式化为 $f(I) = \Theta$（Section 3.2）。

**MANO 手部模型与输出**：回归得到的 $\theta$ 和 $\beta$ 驱动 MANO 参数化手部模型 $\mathcal{M}(\theta, \beta)$，生成包含 778 个顶点的 3D 手部网格 $M \in \mathbb{R}^{778 \times 3}$ 及对应的 3D 关键点 $X$。随后，3D 关键点通过相机投影函数 $x = \pi(X) = \Pi_K(X + t)$ 映射到 2D 图像坐标，用于与标注进行损失计算。

**损失监督**：训练时采用多损失联合监督，包括：3D 参数与关键点损失 $\mathcal{L}_{\mathrm{3D}} = ||\theta - \theta^{*}||_{2}^{2} + ||\beta - \beta^{*}||_{2}^{2} + ||X - X^{*}||_{1}$、2D 重投影损失 $\mathcal{L}_{\mathrm{2D}} = ||\boldsymbol{x} - \boldsymbol{x}^{*}||_{1}$，以及用于惩罚不自然手部姿态的对抗损失 $\mathcal{L}_{\mathrm{adv}}$。整体架构概览见 Figure 2（底部）。

该框架的核心设计哲学是“简单架构 + 大规模数据 + 大容量模型”：不依赖图卷积、非参数化顶点回归或复杂的多阶段细化，仅通过扩大训练数据规模（4 倍于 FrankMocap）和采用 ViT-H 高容量骨干网络，即可在多个基准上取得显著提升。消融实验证实，单独扩大数据或模型容量均能带来增益，而两者结合（即 HaMeR）效果最佳（Table 5, row 5）。

### 补充图表

![[assets/figures/papers/paper_list_l15_HaMeR_Reconstructing_Hands_in_3D_with_Transformers_motion20v2/figures/001_Figure_1.jpg]]
*Figure 1: Monocular 3D hand mesh reconstruction. We propose HaMeR, a fully transformer-based approach for Hand Mesh Recovery. HaMeR achieves consistent improvements upon the state-of-the-art for 3D hand reconstruction. We can faithfully reconstruct hands in a wide variety of scenarios, including captures from different viewpoints (third person or egocentric), under occlusion, hands that interact with objects or other hands, hands with different skin tones, with gloves, from art paintings or mechanical hands. We encourage the reader to watch our reconstructions in the Supplemental Video to appreciate the temporal stability*

![[assets/figures/papers/paper_list_l15_HaMeR_Reconstructing_Hands_in_3D_with_Transformers_motion20v2/figures/002_Figure_2.jpg]]
*Figure 2: Dataset and Architecture. (Top) Hand crops with keypoint annotations from our HInt dataset of annotations for different image sources, Hands23 [9], Epic-Kitchens [12, 13], and Ego4D [18]. We provide location annotations for 21 hand keypoints as well as the “occlusion” label for each joint. Occluded keypoints are marked using solid dot filled with black while non-occluded ones are filled with white. The pie chart shows the distribution and statistics of our dataset. (Bottom) The architecture for HaMeR follows a fully transformer-based design. We use a large scale ViT backbone [14] followed by a transformer decoder to regress the parameters of the hand*



HaMeR 的整体架构遵循全 Transformer 设计，由三个核心模块串联构成：ViT 骨干网络、Transformer 解码器头以及 MANO 手部参数模型。

**ViT Backbone (ViT-H)**。输入为单张 RGB 手部裁剪图像，ViT-H 将其划分为固定大小的图像块（patches），通过自注意力机制提取全局上下文特征，输出一组令牌特征序列。该模块替代了传统 CNN 编码器（如 ResNet50），是模型容量提升的关键来源。

**Transformer Decoder Head**。解码器头接收 ViT 输出的特征序列，通过交叉注意力处理一个可学习的查询令牌，直接回归出手部参数 $\Theta = \{\theta, \beta, \pi\}$。其中 $\theta \in \mathbb{R}^{15 \times 3}$ 为 MANO 姿态参数（15 个关节的轴角表示），$\beta \in \mathbb{R}^{10}$ 为形状参数，$\pi = \{s, t_x, t_y\}$ 为弱透视相机参数（缩放因子 $s$ 与 2D 平移 $t$）。这一设计将 3D 重建任务简化为端到端的参数回归，无需中间热图或显式拓扑建模。

**MANO Hand Model**。MANO 是一个可微的统计手部模型，定义为映射函数：

$$\mathcal{M}(\theta, \beta) \rightarrow \{M, X\}$$

其中 $M \in \mathbb{R}^{778 \times 3}$ 为手部网格顶点，$X \in \mathbb{R}^{21 \times 3}$ 为 3D 关键点坐标。该模块接收网络回归的姿态和形状参数，输出最终的 3D 手部几何。

**3D 关键点投影**。为与 2D 标注对齐，3D 关键点通过弱透视相机模型投影到图像平面：

$$x = \pi(X) = \Pi_K(X + t)$$

其中 $\Pi_K$ 为固定内参矩阵 $K$ 的正交投影，$t = [t_x, t_y, 0]$ 为 3D 平移向量。

**损失函数**。训练采用多任务损失组合：

$$\mathcal{L}_{\mathrm{3D}} = \|\theta - \theta^{*}\|_{2}^{2} + \|\beta - \beta^{*}\|_{2}^{2} + \|X - X^{*}\|_{1}$$

3D 监督损失由姿态参数的 L2 损失、形状参数的 L2 损失以及 3D 关键点的 L1 损失组成，直接约束 MANO 参数空间和 3D 坐标空间。

$$\mathcal{L}_{\mathrm{2D}} = \|x - x^{*}\|_{1}$$

2D 重投影损失最小化投影关键点 $x$ 与标注关键点 $x^{*}$ 之间的 L1 距离，提供像素级监督信号。

$$\mathcal{L}_{\mathrm{adv}} = \sum_{k} (D_{k}(\Theta) - 1)^{2}$$

对抗损失使用多个判别器 $D_k$ 分别对手部姿态、形状和关节角度的自然性进行约束，惩罚不符合人体工学的参数组合，提升重建结果的物理合理性。

> 注：以上公式均来自论文 Section 3.1 至 3.4 的原始定义，变量含义与原文一致。各模块的消融验证见 Table 5 及相关实验分析。



## 实验与关键发现

### 核心实验设计

HaMeR 的实验验证围绕一个中心假设展开：**大规模训练数据与高容量模型架构的结合是提升野外手部重建鲁棒性的关键因果杠杆**。为此，实验设计覆盖三个层次：在标准受控基准（FreiHAND、HO3Dv2）上验证基础精度；在野外基准 HInt 上检验泛化能力；通过消融实验分离数据规模与模型容量各自的贡献。

评估协议遵循各数据集的标准设置。对于 3D 精度，使用 Procrustes 对齐后的平均每顶点位置误差（PA-MPVPE）和平均每关节位置误差（PA-MPJPE），单位为毫米。对于 HInt 的 2D 评估，所有方法均为 3D 方法，通过将 3D 关节点投影到 2D 后计算 PCK 分数，阈值分别设为 0.05、0.10、0.15，并按子集（New Days、VISOR、Ego4D）和可见性（全部/可见/遮挡）分组报告。

---

### 标准基准结果

**FreiHAND 数据集**（Table 1）：HaMeR 在多数指标上取得最优结果。具体而言，PA-MPVPE 达到 5.7 mm，PA-MPJPE 为 6.0 mm，相较此前最优的 **MobRecon**（Chen et al., CVPR 2022）的 5.8 mm 和 6.0 mm 持平或略有提升。在 F@5mm 和 F@15mm 分数上同样保持竞争力。需要注意的是，FreiHAND 是实验室受控环境下的采集数据，该基准上的提升幅度有限，说明现有方法在该场景下已接近性能饱和。

**HO3Dv2 数据集**（Table 2）：该数据集包含手-物交互场景，难度更高。HaMeR 的 PA-MPJPE 为 7.7 mm，PA-MPVPE 为 7.9 mm，显著优于此前最优的 **AMVUR**（Jiang et al., CVPR 2023）的 8.3 mm 和 8.4 mm，分别降低 0.6 mm 和 0.5 mm。这一结果表明，Transformer 架构对交互场景中的遮挡和复杂手部姿态具有更强的建模能力。

---

### 野外基准 HInt 结果

HInt 是本文引入的大规模野外手部关键点基准，整合了 Hands23、Epic-Kitchens VISOR 和 Ego4D 三个来源的标注。这是检验模型在非受控场景下鲁棒性的核心测试平台。

**Table 3 的关键发现**：

- 在最具挑战性的 PCK@0.05 阈值下，HaMeR 在 New Days 子集的所有关节点上达到 48.0%，相比先前方法提升约 2-3 倍（Abstract 中明确声明）。这一量级的提升在计算机视觉任务中极为罕见，构成了本文最强有力的证据。
- 按可见性分组的结果揭示了一个重要模式：HaMeR 在遮挡关节点上的优势尤为突出。例如，在 VISOR 子集的遮挡关节上，HaMeR 的 PCK@0.05 为 33.9%，而 **FrankMocap**（Rong et al., ICCV 2021）仅为 11.6%，差距接近 3 倍。这表明 Transformer 的全局注意力机制对推断被遮挡的关键点位置具有本质优势。
- 在 Ego4D 的第一人称视角数据上，HaMeR 同样大幅领先，证明了模型对不同视角的适应性。

**Table 4 的补充发现**：当使用 HInt 训练集进行微调后（Ours*），模型在 VISOR 和 Ego4D 等第一人称数据上进一步获得明显提升。这说明即使是大规模预训练模型，针对目标域的部分标注数据进行适配仍能带来收益，但通用模型（Ours）本身已经达到了很强的零样本/少样本泛化水平。

---

### 消融实验：数据规模与模型容量的因果分离

Table 5 的消融实验是本文方法论的基石，系统性地分离了数据规模与模型容量两个因素的独立和联合效应。实验以 **FrankMocap** 的设计为起点，在 HInt 的 New Days 子集上评估。

![[assets/figures/papers/paper_list_l15_HaMeR_Reconstructing_Hands_in_3D_with_Transformers_motion20v2/figures/007_Table_5.jpg]]
*Table 5: Effect of large scale data and deep model. We evaluate the effect of different design choices when testing on HInt. We start from a basic design that follows FrankMocap [49], using a ResNet50 architecture and a small training set (2nd row). Increasing the amount of training data by 4× (3rd row) or adopting a high capacity ViT-H architecture (4th row) results in clear and consistent improvements in 2D accuracy over the base model. Combining the data scale and high capacity architecture, which is the proposed HaMeR (5th row), obtains the best results by large margins*

| 配置 | 骨干网络 | 训练数据 | AUC@0.05 |
|------|----------|----------|----------|
| FrankMocap（参考） | ResNet50 | 小（约 0.7M） | 20.8 |
| Base（复现） | ResNet50 | 小 | 20.4 |
| 仅扩大数据 | ResNet50 | 大（2.7M） | 32.3 |
| 仅扩大模型 | ViT-H | 小 | 30.5 |
| **HaMeR（完整）** | **ViT-H** | **大（2.7M）** | **60.8** |

**因果分析**：

1. **数据规模的独立效应**：在保持 ResNet50 不变的情况下，将训练数据扩大 4 倍使 AUC@0.05 从 20.4 提升至 32.3（+11.9 点），相对提升 58%。这证明大规模数据暴露本身就能显著改善野外泛化能力，即使架构不变。

2. **模型容量的独立效应**：保持小训练集，将 ResNet50 替换为 ViT-H 使 AUC@0.05 从 20.4 提升至 30.5（+10.1 点），相对提升 50%。这表明高容量 Transformer 架构在同等数据条件下具有更强的表示学习能力。

3. **联合效应（超线性增益）**：同时扩大数据和采用 ViT-H 使 AUC@0.05 跃升至 60.8，相比 Base 提升 40.4 点（约 3 倍），且远超两个独立增益之和（11.9 + 10.1 = 22.0）。这一超线性增益揭示了数据规模与模型容量之间存在**协同放大效应**：更大的模型能够更有效地利用更大规模的数据，而更多的数据使大模型的表示能力得以充分释放。这是本文最核心的实证发现。

---

### 定性分析

**Figure 3** 将 HaMeR 与 **METRO**（Lin et al., CVPR 2021）、**Mesh Graphormer**（Lin et al., ICCV 2021）和 FrankMocap 进行可视化对比。HaMeR 在挑战性场景中表现出一致的优势：在运动模糊图像中仍能恢复合理的手部姿态；在手-手交互和手-物交互场景中，手指的穿透和错位现象明显少于基线方法。值得注意的是，METRO 和 Mesh Graphormer 作为非参数化方法（直接回归顶点），在野外场景下更容易产生不自然的网格变形，而 HaMeR 的参数化设计（通过 MANO 参数间接生成网格）起到了隐式正则化的作用。

**Figure 4** 展示了 HaMeR 在 HInt 各子集及互联网图像上的重建结果，涵盖严重遮挡、戴手套、艺术画作中的手部、机械手等极端案例。模型在这些场景下表现出令人印象深刻的鲁棒性，但需要指出的是，这些结果是精心挑选的展示样本，实际失败案例在论文中未被充分呈现。

---

### 失败模式与局限性

基于论文中披露的信息和方法设计的固有限制，可识别以下失败模式：

1. **计算资源瓶颈**：ViT-H 骨干网络参数量巨大，推理成本远高于 ResNet50 等轻量级方案。论文未提供推理延迟数据，但显然不适用于移动端或实时应用场景。这是“大数据+大模型”范式在部署层面的固有代价。

2. **MANO 参数模型的表达上限**：HaMeR 回归 MANO 参数而非直接预测顶点或隐式表面，这意味着手部细节（如手指粗细、指甲形状、皮肤褶皱）受限于 MANO 的低维形状空间。对于需要精细手部几何的下游任务（如手语识别中的细微手指动作），这一限制可能成为瓶颈。

3. **单帧独立推理的时序不稳定性**：尽管论文声称在视频上运行时能保持时序平滑（见 Supplemental Video），但方法本身是逐帧独立的，未显式建模时序信息。在快速运动或极端遮挡导致单帧歧义时，相邻帧的重建结果可能出现跳变。

4. **训练数据偏差**：训练集主要由受控环境数据（FreiHAND、HO3D 等）和部分野外数据（HInt）组成。对于训练分布之外的手部外观（如特殊材质手套、严重污损、极端光照），模型性能可能退化。论文在 Figure 4 中展示的机械手和艺术画作案例虽效果良好，但缺乏系统性的定量评估。

![[assets/figures/papers/paper_list_l15_HaMeR_Reconstructing_Hands_in_3D_with_Transformers_motion20v2/figures/009_Figure_4.jpg]]
*Figure 4: Qualitative results. We present qualitative results of our approach on the test set of HInt. We include images from New Days (row 1-2), VISOR (row 3-4), Ego4D (row 5-6), as well as various Internet images (row 7-8). HaMeR is particularly robust and can gracefully handle cases with heavy occlusion and interactions with objects or other hands*

5. **双手交互的局限性**：在双手紧密交互的场景中，左右手的关键点容易混淆。HaMeR 虽比先前方法有显著改进，但 Table 3 中 VISOR 子集（包含大量手-手交互）的 PCK@0.05 仍仅为 33.9%（遮挡关节），表明这一问题远未解决。

![[assets/figures/papers/paper_list_l15_HaMeR_Reconstructing_Hands_in_3D_with_Transformers_motion20v2/figures/005_Table_3.jpg]]
*Table 3: Evaluation on our HInt benchmark. We report results using PCK scores at three different thresholds. All methods are 3D and we evaluate the scores through the 2D projection of 3D joints. We report separate results for the three subsets of HInt, i.e., New Days of Hands [9], Epic- Kitchens VISOR [13] and Ego4D [18]. We also report separate results considering all joints (first set of rows), considering only the joints annotated as visible (second set of rows), or considering only the joints annotated as occluded (third set of rows)*

---

### 实验结论的可靠性评估

- **高置信度结论**：数据规模与模型容量的协同效应（Table 5）、标准基准上的 SOTA 性能（Table 1、Table 2）均有详实的定量证据支撑，置信度 0.95。
- **中等置信度结论**：HInt 上的 2-3 倍提升（Abstract）基于与先前方法的间接比较，且论文未在 Table 3 中指定具体的对比基线数值，置信度 0.85。建议查阅原论文 Table 3 的完整数据以确认具体对比对象和数值。
- **需手动验证**：Figure 3 和 Figure 4 的定性结果展示的是选择性样本，无法排除“cherry-picking”效应。Supplemental Video 中的时序稳定性声明同样需要独立验证。

![[assets/figures/papers/paper_list_l15_HaMeR_Reconstructing_Hands_in_3D_with_Transformers_motion20v2/figures/003_Table_1.jpg]]
*Table 1: Comparison with the state-of-the-art on the Frei-HAND dataset [64]. We use the standard protocol and report metrics for evaluation of 3D joint and 3D mesh accuracy. PA-MPVPE and PA-MPJPE numbers are in mm*

![[assets/figures/papers/paper_list_l15_HaMeR_Reconstructing_Hands_in_3D_with_Transformers_motion20v2/figures/004_Table_2.jpg]]
*Table 2: Comparison with the state-of-the-art on the HO3D dataset [19]. We use the HO3Dv2 protocol and report metrics that evaluate accuracy of the estimated 3D joints and 3D mesh. PA-MPVPE and PA-MPJPE numbers are in mm*

![[assets/figures/papers/paper_list_l15_HaMeR_Reconstructing_Hands_in_3D_with_Transformers_motion20v2/figures/008_Figure_3.jpg]]
*Figure 3: Qualitative comparison. We compare our approach qualitatively with state-of-the-art methods for hand mesh reconstruction. The previous baselines include METRO [33], Mesh Graphormer [34] and FrankMocap [49]. METRO and Mesh Graphormer are non-parametric methods (regressing MANO vertices directly), while FrankMocap and HaMeR (ours) are parametric methods (regressing MANO parameters). The reconstructions from HaMeR are consistently better, particularly on more challenging examples, e.g., cases with motion blur, or images with hand-hand or hand-object interaction. We encourage the reader to also watch the Supplemental Video for more comparisons over time*

### 补充图表

![[assets/figures/papers/paper_list_l15_HaMeR_Reconstructing_Hands_in_3D_with_Transformers_motion20v2/figures/006_Table_4.jpg]]
*Table 4: Effect of training with HInt. We compare our general model (Ours) with the model trained on HInt as well (Ours∗). We report PCK scores on the test set of HInt. Using the training set of HInt can be helpful particularly to improve performance on egocentric data (VISOR and Ego4D)*



## 定位与知识库关联

### 方法谱系：从CNN到全Transformer的3D手部重建

HaMeR在3D手部重建领域的定位可以沿两条轴线理解：**参数化 vs 非参数化**的网格恢复路径，以及**CNN vs Transformer**的架构演进路径。

在参数化路径上，HaMeR直接继承了**FrankMocap**（Rong et al., ICCV 2021）的范式——通过回归MANO模型的姿态参数$\theta$和形状参数$\beta$来生成手部网格，而非直接回归顶点坐标。FrankMocap使用ResNet50作为骨干网络，在约0.7M样本上训练，代表了参数化方法的基线水平。HaMeR在保持这一参数化回归框架的同时，将骨干网络从ResNet50替换为ViT-H，将训练数据规模扩大4倍至2.7M样本，形成了“相同范式、更大容量”的升级路径。

在非参数化路径上，**METRO**（Lin et al., CVPR 2021）和**Mesh Graphormer**（Lin et al., ICCV 2021）率先将Transformer引入手部网格重建，但采用直接回归MANO顶点坐标的方式。这两种方法证明了Transformer架构在手部重建中的潜力，但其非参数化设计使得输出的手部网格缺乏显式的姿态和形状解耦。HaMeR借鉴了Transformer架构的优势，但回归MANO参数而非顶点，实现了参数化与Transformer的结合。

在轻量化和概率建模方向上，**MobRecon**（Chen et al., CVPR 2022）专注于移动端部署的轻量级设计，在FreiHAND上取得了5.8mm的PA-MPVPE，是HaMeR出现前该基准的最优结果之一。**AMVUR**（Jiang et al., CVPR 2023）引入概率注意力机制和遮挡感知纹理回归，在HO3Dv2上达到8.3mm的PA-MPJPE。HaMeR在FreiHAND上以5.7mm的PA-MPVPE略微超越MobRecon，在HO3Dv2上以7.7mm的PA-MPJPE显著超越AMVUR，表明大规模数据和模型容量带来的增益可以超越精心设计的概率建模或轻量化优化。

### 适用边界与关键局限

**计算资源门槛**：HaMeR使用ViT-H作为骨干网络，这是其性能优势的核心来源，也是其最主要的适用限制。与MobRecon等面向移动端的轻量级方案相比，HaMeR的推理成本显著更高，难以直接部署于实时应用或资源受限设备。消融实验（Table 5）表明，单独使用ViT-H替换ResNet50即可带来性能提升，但若要在实际系统中使用，需要在精度和推理速度之间做出权衡。

**MANO参数模型的表达能力上限**：HaMeR依赖MANO手部模型生成网格，这意味着其输出的手部形状受限于MANO的低维参数空间。对于手指纹理、指甲细节、皮肤褶皱等精细几何特征，参数化方法天然无法表达。非参数化方法（如METRO、Mesh Graphormer）虽然可以回归任意顶点位置，但缺乏结构先验，在遮挡或极端姿态下更易产生非自然形变。HaMeR选择了参数化的鲁棒性，代价是细节表达的损失。

**单帧处理的时序盲区**：HaMeR以单张图像为输入，虽然论文提到在视频上逐帧运行时能保持时序平滑，但该方法并未显式利用时序信息。在快速运动、运动模糊或短暂完全遮挡的场景中，单帧方法缺乏帧间约束，可能产生时序不一致的预测。这为后续的视频版本设计留下了明确的改进空间。

**训练数据分布偏差**：HaMeR的训练数据主要来自受控环境和现有数据集的整合，尽管HInt数据集引入了野外场景标注，但训练数据中极端案例（如特殊手套、机械手、艺术画作中的手）的覆盖仍然有限。Table 4显示，加入HInt训练数据后，模型在以自我为中心的数据（VISOR和Ego4D）上表现提升，说明数据分布对齐对性能有直接影响。在更极端的非自然手形场景中，泛化性能仍需进一步验证。

### 开放问题

1. **极端遮挡下的性能边界**：HaMeR在HInt基准上对遮挡关键点的PCK@0.05达到48.0%（New Days子集，所有关键点），相比先前方法有2-3倍提升，但在双手复杂交互或大面积遮挡场景下的极限性能尚未被系统性地量化。遮挡率与精度下降之间的定量关系值得进一步研究。

2. **时序扩展的潜力**：当前的单帧设计为视频版本留下了明确的改进空间。将HaMeR扩展为时序模型（如加入时序Transformer或光流引导的特征对齐）能否在保持单帧鲁棒性的同时进一步提升精度和平滑性，是一个直接且重要的开放方向。

3. **推理效率的帕累托前沿**：消融实验表明数据和模型容量是性能的关键杠杆，但未探索模型压缩、知识蒸馏或混合精度推理对性能-效率权衡的影响。在保持HaMeR核心优势的前提下，是否存在更高效的架构变体（如ViT-L或ViT-B配合更大数据），目前尚不清楚。

4. **下游任务的增益验证**：HaMeR在标准基准上的提升是否能够转化为机器人操作、手语识别、手势交互等下游任务的实际增益，论文未提供相关实验。3D关键点精度的提升与任务级指标之间的相关性需要进一步验证。

5. **非自然手形的鲁棒性**：论文在Figure 1和Figure 4中展示了机械手和艺术画作的重建结果，表明HaMeR具有一定的泛化能力，但缺乏系统性的定量评估。当输入手形显著偏离MANO模型的训练分布时，模型是否会产生系统性偏差，是一个值得关注的问题。



## 原文 PDF

![[paperPDFs/CVPR_2024/HaMeR_Reconstructing_Hands_in_3D_with_Transformers.pdf]]
