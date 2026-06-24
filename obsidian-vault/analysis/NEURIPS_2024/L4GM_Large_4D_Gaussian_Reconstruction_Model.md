---
title: "L4GM: Large 4D Gaussian Reconstruction Model"
type: paper
paper_level: A
venue: NeurIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/L4GM_Large_4D_Gaussian_Reconstruction_Model.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/l4gm/
aliases:
- L4GM
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "利用大规模预训练的3D高斯重建模型(LGM)，并注入时间自注意力层，使模型能通过初始帧的多视角图像将3D信息传播至所有时间步，从而避免每帧独立生成多视图。"
primary_logic: "将已学会静态3D几何的预训练模型迁移至4D时空域，仅需第一帧的多视图图像即可获得整个序列的时空一致性重建，同时保持极高的推理速度。"
claims:
- "在Consistent4D基准上，L4GM在LPIPS (0.12)、CLIP (0.94) 和FVD (691.87) 上均显著优于所有先前方法，且推理速度比优化方法快100-1000倍（仅3秒）。"
- "3D预训练(LGM)不可或缺：移除后模型无法收敛；时间注意力消除闪烁并大幅提升PSNR；端到端微调优于冻结基础LGM层。"
- "用户研究表明，L4GM在总体质量、3D外观、输入视频对齐度以及运动真实感方面均获得最高偏好。"
- "Consistent4D (8 synthetic animations) 上 LPIPS↓ = 0.12"
---

# L4GM: Large 4D Gaussian Reconstruction Model

> [!tip] 核心洞察
> 将已学会静态3D几何的预训练模型迁移至4D时空域，仅需第一帧的多视图图像即可获得整个序列的时空一致性重建，同时保持极高的推理速度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | L4GM: 大型4D高斯重建模型 |
| 英文题名 | L4GM: Large 4D Gaussian Reconstruction Model |
| 会议/期刊 | NeurIPS 2024 |
| Links | [paper](https://arxiv.org/abs/2406.10324); [Project](https://research.nvidia.com/labs/toronto-ai/l4gm); [Project](https://research.nvidia.com/labs/toronto-ai/l4gm/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | L4GM |
| Dataset | Consistent4D (8 synthetic animations), Consistent4D |

> [!tip] 效果简介
> - Consistent4D (8 synthetic animations) 上，LPIPS↓ 为 0.12，对比 0.13 (STAG4D) / 0.14 (GaussianFlow)，变化 -0.01 / -0.02。
> - Consistent4D 上，CLIP↑ 为 0.94，对比 0.91 (STAG4D / GaussianFlow)，变化 +0.03。
> - Consistent4D 上，FVD↓ 为 691.87，对比 992.21 (STAG4D)，变化 -300.34。

## 概述

**问题瓶颈**：将单目动态视频转化为高质量、可自由视点渲染的4D资产，现有方法主要依赖多视图输入或耗时的逐场景优化（如 Consistent4D、4DGen、STAG4D），缺乏从普通视频快速生成4D内容的前馈模型，且大规模动态4D训练数据稀缺。

**核心洞察**：大规模预训练的静态3D重建模型（LGM）已内化了丰富的几何先验。通过向其中注入时间自注意力层，可将第一帧的多视图3D信息作为“锚点”传播至整个时间序列，从而仅凭单目视频就获得时空一致的4D高斯表示。

**方法定位**：L4GM 是一种基于前馈U-Net的**视频到4D高斯重建模型**。它以单目视频帧和第一帧的多视图图像（由 ImageDream 生成并经方位对齐）为输入，在预训练 LGM 的跨视图自注意力之后插入时间自注意力，直接输出每一帧对应的3D高斯集合，构成4D表征。该方法还包含自回归长视频重建和4D插值模型，用于处理长序列和提升帧率。

**主要结果**：在 Consistent4D 基准上，L4GM 取得了最优的 LPIPS（0.12）、CLIP（0.94）和 FVD（691.87），同时推理仅需约3秒，比优化类方法快100至1000倍。消融实验证实：3D预训练不可或缺（移除后模型无法收敛），时间自注意力消除了闪烁并显著提升PSNR，端到端微调优于冻结基础层。用户研究也表明，L4GM 在总体质量、3D外观、视频对齐度和运动真实感四个维度上均获得最高偏好。

## 背景与动机

### 4D内容生成的范式瓶颈

从视觉输入重建动态3D内容（即4D重建）是计算机视觉与图形学中长期存在的挑战。这一任务的核心目标是从有限的观测中恢复随时间变化的三维几何与外观，使生成的4D资产能够从任意视角、任意时刻被自由渲染。近年来，随着3D高斯泼溅（3D Gaussian Splatting）等显式表示方法的成熟，静态3D重建已取得显著进展——例如，基于大规模重建模型（Large Reconstruction Model, LRM）的前馈方法能够在数秒内从少量多视图图像中直接预测3D高斯椭球参数，无需逐场景优化。

然而，当场景从静态扩展至动态时，问题难度急剧上升。现有视频到4D的方法主要依赖两类范式：

**优化式方法**（如Consistent4D、4DGen、GaussianFlow、STAG4D、DG4D）以单目视频为输入，通过逐场景迭代优化来拟合4D表示。这类方法通常需要借助视频扩散先验或多视图伪标签来约束时间一致性，但单次重建耗时通常在10分钟至1小时以上（Table 1），难以支撑交互式应用或大规模内容生产。

**两阶段方法**（如Efficient4D）先通过多视图采样生成候选视图，再进行后优化，虽然部分缓解了效率问题，但仍未摆脱优化瓶颈，且生成质量受限于中间视图的可靠性。

上述方法的共同症结在于：**缺乏一种能够从单目视频中直接、快速生成高质量4D资产的前馈模型**。这一缺口的存在，根源于两个相互交织的困难：（1）动态4D训练数据的大规模获取远比静态3D数据困难；（2）如何在保持多视图一致性的同时，有效建模时间维度上的运动与形变，避免逐帧独立重建导致的闪烁与几何断裂。

### 核心动机：从静态3D到动态4D的知识迁移

L4GM的提出基于一个关键的因果洞察：**静态3D重建模型已经学会了对几何与外观的强先验，这些先验可以作为动态建模的锚点**。具体而言，预训练的3D大型重建模型LGM能够从多视图图像中输出空间一致的3D高斯表示，这意味着它已经内化了关于物体形状、纹理和跨视图对应关系的丰富知识。如果能将这一静态3D知识“注入”到时间维度中，模型就无需从零学习4D几何——它只需要学习如何将第一帧的多视图3D信息传播到后续时间步，同时保持时空一致性。

这一思路直接回应了上述两个困难：对于数据稀缺问题，可以利用大规模静态3D数据集（如Objaverse）预训练的基础模型作为初始化，仅需相对有限的动态数据（约51K个4D动画片段，Table 3）进行微调；对于时间建模问题，则通过在预训练U-Net架构中插入时间自注意力层，使模型能够以第一帧的多视图图像为“锚”，将3D结构传播至整个序列，而非对每一帧独立重建。

### 方法定位与边界

L4GM被设计为一个**前馈的、以单目视频加首帧多视图为输入的4D高斯重建模型**。其输出是T组3D高斯参数（每组对应一个时间步），共同构成4D表示。模型明确假设输入视频由静态相机拍摄、对象处于约0°仰角，且场景以单个前景物体为主。这些假设简化了问题空间，但也划定了当前方法的适用范围——自视角视频、多对象遮挡场景以及大幅仰角变化的输入不在设计目标之内。

## 核心创新

L4GM 的核心创新在于将**静态3D重建的大规模预训练能力迁移至动态4D时空域**，从而以纯前馈方式从单目视频快速生成高质量的4D资产。其关键创新点可解构为以下三个相互耦合的“changed slots”：

### 1. 输入模态扩展：从单时间步多视图到“视频帧+首帧多视图”

传统3D重建模型（如基础 LGM）仅接收单个时间步的多视图图像作为输入，输出一组静态3D高斯。L4GM 将输入扩展为**单目视频帧序列**与**首帧（t=1）的多视图图像**的组合（Section 4.1, 4.2）。首帧多视图图像通过 ImageDream 生成并经方位角对齐（Figure 8）获得，为整个时序重建提供了初始的3D几何锚点。这一设计使得模型无需对每一帧独立生成多视图，而是将首帧的3D结构信息作为先验传播至后续所有时间步。

### 2. 时序建模机制：注入时间自注意力层

L4GM 在预训练 LGM 的 U-Net 架构中，**在每个跨视图自注意力层之后插入时间自注意力层**（Section 4.2, Figure 2）。具体实现上，特征张量被重塑为 `(B V) (T H W) C` 的形式，将视图轴视为批次维度，从而在时间维度上执行自注意力操作。这种设计的关键优势在于：
- **复用预训练权重**：跨视图自注意力层保持了多视图一致性，无需从头学习空间几何。
- **消除时序闪烁**：时间自注意力使模型能够跨帧聚合信息，直接输出时空一致的4D高斯序列，而非逐帧独立重建后拼接。

消融实验（Section 6.3, Figure 6b）证实，移除时间自注意力会导致输出出现明显闪烁且 PSNR 显著下降，验证了该模块的必要性。

### 3. 输出表示与帧率增强：从单组3D高斯到4D高斯序列

基础 LGM 输出单组3D高斯椭球体（参数化为 $\mathbf{z}, \mathbf{s}, \mathbf{q}, \alpha, \mathbf{c}$）。L4GM 将其扩展为**T组3D高斯**，每组对应一个时间步，构成完整的4D表示（Section 4.2）。在此基础上，L4GM 进一步引入两个关键扩展：

- **4D插值模型**（Section 4.3, Figure 3右）：从 L4GM 微调而来，接收连续两组多视图渲染图像，生成中间帧的高斯组。训练时利用加权RGB平均作为中间帧的监督信号。该模型可将输出帧率提升至输入帧率的3倍，带来更流畅的运动表现。
- **自回归重建**（Section 4.3, Figure 3左）：对于长视频，采用滑动窗口方式处理，将前一个片段最后一帧的多视图渲染作为下一个片段的输入，相邻片段间有一帧重叠以保持连续性。

### 创新点之间的因果耦合关系

上述三个 changed slots 并非孤立设计，而是形成了一条因果链：**3D预训练提供几何先验 → 首帧多视图注入初始结构 → 时间自注意力将该结构传播至全序列 → 4D高斯序列输出实现时空一致重建**。这种设计使得 L4GM 仅需约3秒即可完成推理，比优化类方法（如 Consistent4D、4DGen 等）快100-1000倍（Table 1），同时保持了领先的重建质量（LPIPS 0.12, CLIP 0.94, FVD 691.87）。

值得注意的是，消融实验（Figure 6a）表明，**若不加载 LGM 的3D预训练权重，模型完全无法收敛**，这从反面印证了预训练几何先验是整个方法体系的基石。而基于 HexPlane 的变形场替代方案在大规模训练中失效（PSNR 提升缓慢且输出近乎静态，Figure 6b），进一步凸显了“预训练迁移+时间注意力”这一技术路线的独特优势。

## 整体框架

L4GM 的整体 pipeline 以“将静态 3D 重建能力迁移至时空域”为核心设计理念，构建在预训练好的 **LGM**（Large 3D Gaussian Reconstruction Model）之上。其输入为一段单目视频以及该视频第一帧对应的多视角图像，输出为与输入帧数对应的 **4D 高斯表示**——即每个时间步一组独立的 3D Gaussian 椭球集合，从而形成动态的 4D 资产。

整个框架由以下关键模块串联而成：

### 1. 多视角生成与方位对齐
系统首先使用 **ImageDream** 以第一帧为条件生成四张正交视角的图像。随后利用 LGM 从这些多视角图像中重建一个静态 3D 高斯场，并从多个方位角渲染该场，选取与输入帧匹配度最高的方位角，以此确定最终的四张对齐多视角图像（Figure 8）。这一步解决了生成式多视角模型输出方位不可控的问题，为后续时空建模提供了稳定的 3D 锚点。

### 2. 4D 重建骨干网络
核心重建模型采用 LGM 的**非对称 U-Net** 结构作为骨干。输入被组织为一个包含视频帧与多视角图像的网格，经过编码器提取特征后，依次通过**跨视角自注意力**（Cross-View Self-Attention）和新增的**时间自注意力**（Temporal Self-Attention）层：

- **跨视角自注意力**：确保同一时间步内不同视角之间的 3D 一致性。
- **时间自注意力**：在跨视角注意力之后插入，将视角轴视为批次维度，对时间序列进行自注意力建模，从而将第一帧的多视角 3D 信息传播至所有后续帧，消除时序闪烁并维持运动连贯性。

解码器最终输出每个时间步、每个像素对应的 3D Gaussian 参数（中心位置 $\mathbf{z}$、缩放 $\mathbf{s}$、旋转四元数 $\mathbf{q}$、不透明度 $\alpha$ 和颜色特征 $\mathbf{c}$），形成完整的 4D 高斯表示。

### 3. 渲染与损失计算
生成的 4D 高斯从多个监督视角进行可微渲染，损失函数由两部分组成：
- **RGB 损失**：结合 MSE 和 LPIPS 感知损失，对渲染图像与真实图像进行逐帧、逐视角监督。
- **掩码损失**：对 Alpha 掩码进行 MSE 监督，辅助前景分割。

总损失为两者之和：$\mathcal{L} = \mathcal{L}_{\mathrm{RGB}} + \mathcal{L}_{\mathrm{Mask}}$。

### 4. 自回归重建与插值
对于长视频，L4GM 采用**滑动窗口自回归**策略：将前一个窗口最后一帧的多视角渲染结果作为下一个窗口的输入，窗口之间保留一帧重叠以维持连续性（Figure 3 左）。此外，框架还包含一个由 L4GM 微调而来的 **4D 插值模型**：给定两个连续的多视角高斯集合，该模型生成中间帧的高斯表示，并利用加权 RGB 平均来监督中间帧的渲染结果，从而将输出帧率提升至输入帧率的 3 倍（Figure 3 右）。

整个 pipeline 的突出特性在于：仅需第一帧的多视角图像即可驱动全部时间步的 3D 一致重建，无需逐帧独立生成多视图，也无需任何测试时优化。这使其在保持极高推理速度（约 3 秒）的同时，实现了时空连贯的 4D 内容生成。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2406_10324/figures/002_Figure_2.jpg]]
*Figure 2: L4GM. The overall model architecture of L4GM. Our model takes a single-view video and single-time step multiview images as input, and outputs a set of 4D Gaussians. It adopts a U-Net architecture and uses cross-view self-attention for view consistency and temporal cross-time self-attention for temporal consistency*

## 核心模块与公式推导

### 3D高斯椭球参数化

L4GM继承LGM的3D高斯溅射（3D Gaussian Splatting）表示，将场景建模为一组各向异性的3D高斯椭球。每个高斯椭球由以下参数定义（Section 3）：

$$\mathbf{z} \in \mathbb{R}^3,\quad \mathbf{s} \in \mathbb{R}^3,\quad \mathbf{q} \in \mathbb{R}^4,\quad \alpha \in \mathbb{R},\quad \mathbf{c} \in \mathbb{R}^3$$

其中 $\mathbf{z}$ 为中心位置向量，$\mathbf{s}$ 为各轴缩放系数，$\mathbf{q}$ 为旋转四元数，$\alpha$ 为不透明度，$\mathbf{c}$ 为颜色特征。对于 $T$ 帧的动态场景，模型输出 $T$ 组独立的高斯参数集，构成4D表示。

### 多视图生成与方位对齐模块

该模块负责为第一帧生成空间一致的多视图图像，作为后续时序传播的锚点（Section 4.1）。具体流程为：

1. 使用 **ImageDream** 以第一帧为条件生成四个正交视角（0°、90°、180°、270°）的图像。
2. 将生成的多视图送入预训练的 **LGM** 重建3D高斯，并从多个方位角渲染。
3. 选择与输入帧CLIP相似度最高的渲染方位作为对齐视角，取其正交四视图作为最终的多视图输入。

此步骤解决了ImageDream生成的多视图与输入帧方位不一致的问题，确保后续4D重建的空间基准可靠（Figure 8, Appendix E）。

### 4D重建骨干网络

L4GM的骨干网络继承自预训练LGM的非对称U-Net结构，核心改动在于注入时间建模能力（Section 4.2）。

**输入处理：** 模型接收一个 $T \times V$ 的图像网格作为输入，其中 $T$ 为视频帧数，$V$ 为每帧的视角数。输入帧包括单目视频帧和第一帧的多视图图像（后者在训练时按概率随机遮挡以模拟推理时的缺失情况）。

**跨视角自注意力（Cross-View Self-Attention）：** 继承自LGM，在U-Net的各层中对不同视角的特征进行自注意力计算，确保同一时刻不同视角间的空间一致性。

**时间自注意力（Temporal Self-Attention）：** L4GM在每个跨视角自注意力层之后插入时间自注意力层。具体实现为将特征张量重排，把视角轴合并到批次维度，使时间步成为序列维度进行自注意力计算：

$$x = \text{rearrange}(x,\; (B\;T\;V)\;H\;W\;C \rightarrow (B\;V)\;(T\;H\;W)\;C)$$

$$x = x + \text{TempSelfAttn}(x)$$

这一设计使得第一帧的多视图3D信息能够通过注意力机制传播到所有时间步，避免每帧独立生成多视图时出现的闪烁和不一致问题。消融实验（Section 6.3, Figure 6b）证实，移除时间自注意力会导致输出出现明显闪烁且PSNR显著下降。

### 损失函数

训练采用多视图RGB监督与掩码监督的组合损失（Appendix B）。

**RGB损失** 结合L2重建损失与LPIPS感知损失，对所有时间步和所有视角（包括输入视角 $\mathcal{O}$ 和额外监督视角 $\mathcal{O}_{\text{sup}}$）进行监督：

$$\mathcal{L}_{\text{RGB}} = \sum_{t=1}^{T} \sum_{O \in \mathcal{O} \cup \mathcal{O}_{\text{sup}}} \| I_t^O - f(P_t, O) \|_2^2 + \lambda \mathcal{L}_{\text{LPIPS}}(I_t^O, f(P_t, O))$$

其中 $I_t^O$ 为真实图像，$f(P_t, O)$ 为从高斯参数集 $P_t$ 在视角 $O$ 下的渲染结果。

**掩码损失** 对Alpha通道进行MSE监督，辅助前景分割：

$$\mathcal{L}_{\text{Mask}} = \sum_{t=1}^{T} \sum_{O \in \mathcal{O} \cup \mathcal{O}_{\text{sup}}} \| \alpha_t^O - g(P_t, O) \|_2^2$$

其中 $\alpha_t^O$ 为真实Alpha掩码，$g(P_t, O)$ 为渲染的不透明度。

**总损失** 为两者之和：

$$\mathcal{L} = \mathcal{L}_{\text{RGB}} + \mathcal{L}_{\text{Mask}}$$

### 自回归重建模块

为处理超长视频，L4GM采用滑动窗口的自回归策略（Section 4.3, Figure 3左）。将前一个时间窗口最后一帧的多视图渲染结果作为下一个窗口的输入，相邻窗口间有一帧重叠以保证连续性。消融实验（Figure 6c）表明，$T=16$ 在单次推理质量与自回归效率间取得了最佳平衡；自回归重复超过10次后重建质量开始下降。

### 4D插值模块

该模块由L4GM微调而来，用于将重建帧率提升至输入帧率的3倍（Section 4.3, Figure 3右）。输入为两个连续时刻的多视图渲染图像，输出为中间时刻的高斯参数集。对于中间帧的监督信号，采用两端多视图RGB像素的加权平均作为伪真值。

## 实验与分析

### 主要结果：视频到4D重建基准

L4GM在Consistent4D基准（8个合成动画）上进行了系统评估，对比了当前主流的优化式视频转4D方法，包括**Consistent4D**、**4DGen**、**GaussianFlow**、**STAG4D**、**DG4D (DreamGaussian4D)** 和 **Efficient4D**。实验结果如Table 1所示，L4GM在所有关键指标上均取得最优性能：

- **感知质量**：LPIPS达到0.12，优于STAG4D的0.13和GaussianFlow的0.14，表明生成视图与真实视图的感知差异最小。
- **语义一致性**：CLIP分数达到0.94，高于STAG4D和GaussianFlow的0.91，说明重建结果与输入视频的语义对齐更紧密。
- **时序连贯性**：FVD降至691.87，显著优于STAG4D的992.21，降幅达300点，反映了L4GM在消除闪烁和保持运动平滑性方面的优势。
- **推理速度**：L4GM仅需3秒完成重建，而4DGen耗时约1小时、STAG4D约1小时、DG4D约10分钟，速度提升达100至1000倍。这一数量级的加速源于前馈网络避免了逐场景的迭代优化。

值得注意的是，L4GM的定量优势建立在合成数据训练的基础上，但其在ActivityNet真实视频以及Sora、Veo等生成视频上的泛化表现未见明显域差异，初步验证了方法的鲁棒性。然而，定量评估仅覆盖8个样本，缺乏大规模真实世界验证，结论的统计显著性需要更多实验支撑。

### 用户研究

为了弥补自动指标在评估4D生成质量上的局限性，作者进行了用户研究，在24个合成4D场景上对比L4GM与DG4D、STAG4D和GaussianFlow。评估维度包括总体质量、3D外观、输入视频对齐度和运动真实感四个维度。如Table 2所示，L4GM在所有四个维度上均获得最高偏好，其中总体质量维度以65.4%对25.0%显著优于DG4D。这一结果表明，L4GM不仅数值指标占优，在人类主观感知层面同样具有明显优势。

### 消融实验

消融实验揭示了L4GM设计中的关键因果机制，所有结果汇总于Figure 6。

**3D预训练的必要性**：移除LGM的预训练权重后，模型完全无法收敛，PSNR曲线不上升。即使使用较小规模的模型变体进行训练，PSNR也显著低于完整预训练模型。这验证了核心洞察：静态3D几何的先验知识是学习时空一致性的基础，缺乏该先验将导致优化陷入局部极小。

**端到端微调优于冻结基础层**：仅训练时间自注意力层而冻结LGM的其余参数，最终PSNR显著低于端到端微调全部参数。这表明时间建模与空间建模之间存在紧密耦合，冻结空间层会限制时间层对跨帧几何变化的适应能力。

**时间自注意力的关键作用**：移除时间自注意力层后，输出出现明显的帧间闪烁，PSNR大幅下降。这一现象在补充视频中清晰可见，证明时间自注意力是消除时序不一致性的核心机制。

**HexPlane变形场在大规模训练中失效**：作为替代方案，研究者尝试了基于HexPlane的变形场方法（架构见Figure 9），但在大规模训练中PSNR提升极为缓慢，且输出几乎静态，无法有效捕捉动态变化。这从反面证实了直接预测每帧高斯集合的前馈策略更适合大规模4D生成。

**自回归重建的累积误差**：随着自回归重复次数增加，重建质量逐渐下降。实验表明，视频长度T=16在单次推理质量与自回归扩展能力之间取得了最佳平衡。超过10次自回归后，质量退化变得明显。

**4D插值模型的有效性**：4D插值模型成功将重建帧率提升至输入帧率的3倍，带来更流畅的运动表现。该方法通过在两帧高斯集合之间生成中间高斯集合，并利用加权RGB平均作为中间帧监督，避免了从头预测的难度。

### 失败模式与局限性

尽管L4GM在基准上表现优异，但分析揭示了几个系统性失败模式（见Figure 14）：

1. **运动模糊与复杂动作**：在包含快速运动（如行走）的场景中，非参考视角的腿部运动可能出现不自然的扭曲，表明模型对运动模糊的鲁棒性不足。
2. **多对象遮挡**：当场景包含多个相互遮挡的对象时，重建质量显著下降，高斯椭球难以准确分离不同物体的几何边界。
3. **自视角视频**：模型假设输入视频为0°仰角且相机静止，无法处理Ego4D等自视角数据，限制了在可穿戴设备场景中的应用。
4. **单对象限制**：当前仅支持单对象重建，缺乏对多对象交互场景的建模能力。

这些失败模式指向了方法的核心假设边界：静态相机、0°仰角、单对象。突破这些限制需要重新设计输入表示或引入显式的相机位姿估计模块。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2406_10324/figures/007_Figure_6.jpg]]
*Figure 6: PSNR plot. a) Training with different pretrain and training data. b) Training with different design choices. c) Per-frame PSNR with different video lengths T , AR denotes autoregressive*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2406_10324/figures/009_Table_3.jpg]]
*Table 3: (a) Flow magnitude histogram in log scales. (b) Flow magnitude histogram in [0.1, 10]. Table 3: Optical flow magnitude histogram on Objaverse-4D dataset*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2406_10324/figures/005_Table.jpg]]

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2406_10324/figures/008_Table_2.jpg]]
*Table 2: Comparison to baselines by user study on synthesized 4D scenes with 24 examples. Numbers are percentages. Numbers do not add up to 100; difference is due to users voting “no preference” (details in Appendix)*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2406_10324/figures/011_Table_4.jpg]]
*Table 4: Comparison between L4GM and state-of-the-arts approaches on full metrics in the Consistent4D benchmark. Baseline results are from [15]*

## 方法谱系与知识库定位

### 核心定位：前馈式视频转4D的重建模型

L4GM 属于**前馈式单目视频到4D高斯重建**方法。其核心思路是将一个已在大规模数据上学会静态3D几何的预训练模型（**LGM**，即 Large Gaussian Model）迁移至时空域，从而避免传统优化式方法所需的逐场景漫长迭代。具体而言，L4GM 在 LGM 的 U-Net 骨干中注入时间自注意力层，使模型仅需第一帧的多视角图像即可将3D信息传播至所有时间步，输出一组时序一致的4D高斯表示（T 组 3D Gaussians）。这一设计使得推理速度达到秒级（约3秒），比优化式方法快 100–1000 倍。

### 与基线方法的关系

在视频转4D任务中，L4GM 与以下代表性工作形成对比：

- **优化式方法**：**Consistent4D**、**4DGen**、**GaussianFlow**、**STAG4D**、**DG4D (DreamGaussian4D)** 等均为基于优化的视频转4D管线，通常依赖视频扩散先验、光流正则或伪标签来约束动态场景重建。这些方法需对每个场景独立优化，耗时从数十分钟到数小时不等。L4GM 以单次前馈推理替代了迭代优化，在 Consistent4D 基准上取得了更优的 LPIPS (0.12)、CLIP (0.94) 和 FVD (691.87)，同时将推理时间压缩至 3 秒（Table 1）。

- **两阶段方法**：**Efficient4D** 采用“多视图采样 + 优化”的两阶段策略，虽比纯优化方法更快，但仍无法达到实时前馈的水平。L4GM 的端到端前馈设计在速度上具有数量级优势。

- **逐帧3D重建基线**：**OpenLRM** 代表了一类将视频逐帧送入3D重建模型的朴素方案。由于缺乏时序建模，这类方法输出存在严重的帧间闪烁问题。L4GM 通过时间自注意力层显式建模帧间一致性，消除了闪烁伪影，PSNR 显著优于移除时间注意力的变体（Figure 6b）。

- **变形场方法**：论文探索了基于 HexPlane 的变形场作为替代时序建模方案，但在大规模训练中失效，PSNR 提升缓慢且输出近乎静态（Figure 6b）。这表明在数据驱动的大规模训练设定下，直接学习各帧高斯参数比学习隐式变形场更为有效。

### 知识库贡献与适用边界

L4GM 的关键知识贡献在于证明了**3D预训练对4D前馈重建是不可或缺的**。消融实验表明，不加载 LGM 预训练权重时模型无法收敛；使用较小模型变体导致 PSNR 明显更低（Figure 6a）。端到端微调（包括非时间层）优于仅训练时间注意力而冻结基础 LGM 层（Figure 6b）。这为后续4D生成工作提供了明确的架构设计指导：复用成熟的3D重建骨干并注入时序建模，是高效获取时空一致性的可行路径。

**适用边界**：
- 模型假设相机为静态且对象处于 0° 仰角，对自视角（ego-centric）或大仰角变化的视频表现不佳（Figure 14c）。
- 当前仅支持单对象场景；包含遮挡的多对象场景重建质量下降（Figure 14b）。
- 对快速运动或运动模糊的处理不够鲁棒，部分行走动作中非参考视角的腿部运动不自然。

### 局限与开放问题

1. **运动鲁棒性不足**：模型对快速运动和严重遮挡场景的处理能力有限。如何引入显式的运动跟踪或物理合理性约束，而不牺牲前馈推断速度，仍需探索。

2. **输入假设限制**：当前仅支持 0° 仰角、静态相机下的单视角单对象视频。扩展至自视角视频、多对象场景以及自由相机轨迹是重要的工程与研究方向。

3. **与生成式上游的整合**：L4GM 目前依赖 ImageDream 生成第一帧的多视角图像。如何与文本到视频或图像到视频模型无缝结合，实现端到端的文本/图像到4D内容生成，是通向实用化内容创作工具的关键一步。

4. **大规模真实数据训练**：模型仅在合成的 Objaverse-4D 数据集上训练（尽管对 ActivityNet 真实视频和 Sora/Veo 生成视频有良好泛化）。在大规模真实世界4D数据上训练能否进一步提升泛化性和鲁棒性，尚待验证。

5. **高层编辑能力缺失**：L4GM 目前仅支持从视频重建4D资产，缺乏人机交互的4D编辑能力（如局部运动编辑、材质修改等）。发展更高级的交互式4D编辑功能是面向专业应用的重要方向。

## 原文 PDF

![[paperPDFs/NEURIPS_2024/L4GM_Large_4D_Gaussian_Reconstruction_Model.pdf]]
