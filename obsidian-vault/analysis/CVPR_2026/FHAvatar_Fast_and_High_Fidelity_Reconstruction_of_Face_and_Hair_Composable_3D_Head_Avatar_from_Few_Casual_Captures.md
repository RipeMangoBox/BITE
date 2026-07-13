---
title: "FHAvatar: Fast and High-Fidelity Reconstruction of Face-and-Hair Composable 3D Head Avatar from Few Casual Captures"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FHAvatar_Fast_and_High_Fidelity_Reconstruction_of_Face_and_Hair_Composable_3D_Head_Avatar_from_Few_Casual_Captures.pdf
project_link: null
code_link: null
aliases:
- FHAvatar
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 在纹理空间中显式解耦面部与头发组件，分别使用平面高斯和链式高斯进行独立建模，并通过聚合Transformer从多视图数据中学习几何感知的跨视图先验和头-发结构一致性。
primary_logic: 针对面部与头发截然不同的几何特性（面部平坦、头发链状），采用双分支高斯解码器，并结合自适应头发密度图和长度感知的链数/高斯数下采样，在少量随意捕获下实现高质量重建和实时驱动；此外，可选的轻量化细化进一步提升了细节保真度。
claims:
- 在6帧输入下，FHAvatar（full）的PSNR达到23.71，SSIM 0.825，LPIPS 0.296，AKD低至3.08，全面显著优于现有优化类、前馈类和扩散类方法。
- 移除发丝分支导致PSNR下降1.82，SSIM下降0.014，LPIPS上升0.088，验证了解耦面部与头发设计的有效性。
- 即使单帧输入，FHAvatar（single‑pass）的AKD仅为3.96，远低于其他方法（如LAM的48.64），证明了多视角先验和Transformer聚合在稀疏输入下的强大泛化能力。
- 面部‑头发区域解耦评估中，FHAvatar在面部IoU达0.922，头发IoU达0.826，分别领先最优基线6.7%和36%，验证了显式区域分离的精准度。
---

# FHAvatar: Fast and High-Fidelity Reconstruction of Face-and-Hair Composable 3D Head Avatar from Few Casual Captures

> [!tip] 核心洞察
> 针对面部与头发截然不同的几何特性（面部平坦、头发链状），采用双分支高斯解码器，并结合自适应头发密度图和长度感知的链数/高斯数下采样，在少量随意捕获下实现高质量重建和实时驱动；此外，可选的轻量化细化进一步提升了细节保真度。

| 字段 | 内容 |
|------|------|
| 中文题名 | FHAvatar：从少量随意拍摄中快速高保真重建面部与头发可组合的3D头部Avatar |
| 英文题名 | FHAvatar: Fast and High-Fidelity Reconstruction of Face-and-Hair Composable 3D Head Avatar from Few Casual Captures |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.23345) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FHAvatar |
| Dataset | NeRSemble |

> [!tip] 效果简介
> - NeRSemble (1 frame, self-reenactment) 上，PSNR↑/SSIM↑/LPIPS↓/AKD↓/CSIM↑ 22.46 (single‑pass) / 0.803 / 0.325 / 3.96 / 0.522 vs LAM: 16.41 / 0.662 / 0.409 / 48.64 / 0.461 (+6.05 PSNR, +0.141 SSIM, -0.084 LPIPS, -44.68 AKD, +0.061 CSIM)。
> - NeRSemble (6 frames, self-reenactment) 上，PSNR↑/SSIM↑/LPIPS↓/AKD↓/CSIM↑ 23.71 (full) / 0.825 / 0.296 / 3.08 / 0.721 vs GaussianAvatars: 23.44 / 0.784 / 0.300 / 7.41 / 0.465 (+0.27 PSNR, +0.041 SSIM, -0.004 LPIPS, -4.33 AKD, +0.256 CSIM)。

## 概要

从几张随意拍摄的手机照片快速重建高保真、可驱动的3D头部Avatar，是数字人应用的核心需求。然而，现有方法面临两个根本性瓶颈：其一，面部与头发具有截然不同的几何特性——面部呈平坦表面，头发则呈现链状结构——但现有方案通常将它们耦合在统一的建模框架中，忽略了这种内在差异；其二，主流方法要么依赖密集多视图捕获与昂贵的逐身份优化（小时级），要么仅支持单视图前馈推理，在稀疏输入下难以同时保证身份一致性和发丝精细度。

**FHAvatar** 针对上述瓶颈提出了一个前馈重建框架。其核心洞察是：**在纹理空间中显式解耦面部与头发组件**，并分别采用平面高斯（planar Gaussians）和链式高斯（strand-based Gaussians）进行独立建模。具体而言，面部分支将FLAME模板UV空间的每个像素解码为一个平面高斯，而头发分支则利用冻结的SIREN链式生成器，从单目头发特征中生成方向向量，累积形成链式线段并赋予链式高斯。两个分支由一个聚合Transformer（aggregated Transformer）从任意数量和顺序的多视图输入中学习几何感知的跨视图先验，同时促进头-发特征的结构一致性。推理时，模型支持单次前馈重建，并可选配一分钟级的解码器微调以进一步提升细节保真度。

在NeRSemble基准上的实验表明，FHAvatar在6帧输入下达到**PSNR 23.71、SSIM 0.825、LPIPS 0.296、AKD 3.08**，全面优于现有优化类、前馈类和扩散类方法（Table 1）。即使在单帧输入的极端条件下，其AKD低至3.96，远低于其他方法（如LAM的48.64），验证了多视图先验和Transformer聚合在稀疏输入下的强大泛化能力。消融实验进一步证实：移除发丝分支导致PSNR下降1.82、LPIPS上升0.088（Table 2），面部区域IoU达0.922、头发区域IoU达0.826，分别领先最优基线6.7%和36%（Table 3），充分验证了解耦设计的有效性。此外，面部与头发的可组合性还支持无缝发型迁移和纹理空间风格化编辑等应用。

方法定位上，FHAvatar属于**前馈3D高斯泼溅（3DGS）头部重建**路线，与优化类方法（如FlashAvatar、GaussianAvatars、MeGA）和前馈单视图方法（如GAGAvatar、LAM）形成对比，其关键区分点在于双分支解耦建模与多视图聚合Transformer的结合。

### 问题背景

从少量随意拍摄（如手机照片）中快速重建高保真、可驱动的3D头部Avatar，是数字人、影视制作和虚拟社交等应用的核心需求。一个理想的头部Avatar应同时具备高质量的面部外观、精细的发丝几何、准确的身份保持，并支持实时表情驱动与灵活编辑。然而，这一目标面临两大根本性挑战：一是面部与头发在几何形态上存在本质差异——面部近似平坦表面，头发则呈现链状、半透明、高度非结构化的复杂几何；二是稀疏输入条件下，缺乏足够的跨视角信息来约束3D重建，容易导致身份漂移和细节丢失。

### 现有方法缺口

现有3D头部重建方法大致可分为三类，但各类方法均存在明显短板：

**优化类方法**（如 **GaussianAvatars**、**FlashAvatar**、**MeGA**）虽然能生成高质量结果，但依赖密集多视图捕获或昂贵的逐身份优化（通常需数小时），限制了其在实际应用中的可用性。当输入视图稀疏时，这类方法往往难以收敛，无法保持准确的身份和表情控制。

**前馈类方法**（如 **LAM**、**GAGAvatar**）通过单次前向推理实现快速重建，但通常仅支持单一视图输入，缺乏有效的多视图信息融合机制。在稀疏多视图场景下，这类方法无法充分利用跨视角互补信息，导致身份相似度低、视角一致性差。例如，LAM在单帧输入下的平均关键点距离（AKD）高达48.64，远不能满足实用要求。

**扩散类方法**（如 **DiffusionRig**）通过迭代优化进行多视图重建，但推理速度慢，且在表情重演和新视角下难以保持精确控制。

更为关键的是，**现有方法普遍将面部和头发表征耦合在统一建模过程中**，忽略了二者内在的几何差异：面部适合用平面高斯（planar Gaussian）建模，而头发更适合用链式高斯（strand-based Gaussian）沿发丝方向生长。这种耦合建模不仅限制了发丝的精细重建能力，也阻碍了发型迁移、风格化编辑等组合式应用。

### 本文动机

针对上述缺口，本文提出 **FHAvatar**，一个从少量随意拍摄中快速、高保真重建面部与头发可组合3D头部Avatar的框架。其核心动机在于：

1. **显式解耦面部与头发组件**：在纹理空间中分别使用平面高斯和链式高斯进行独立建模，使各自的高斯表征能更好地适配其底层几何特性。
2. **学习几何感知的跨视图先验**：通过聚合Transformer从任意数量和顺序的多视图数据中融合特征，建立鲁棒的头-发结构一致性，使模型在稀疏输入下仍能保持高质量重建和身份保持。
3. **兼顾效率与细节**：单次前馈推理即可完成重建，同时提供可选的一分钟级轻量化细化，在推理速度和细节保真度之间取得灵活平衡。

## 核心方法与创新机理

FHAvatar 的核心创新在于**显式解耦面部与头发的几何表征与建模流程**，并构建了一个**几何感知的多视图聚合前馈框架**，从而在极稀疏、随意拍摄的输入下实现高保真、可实时驱动的 3D 头部 Avatar 重建。

### 1. 面部-头发显式解耦与双分支高斯解码

现有方法（如 **GaussianAvatars**、**MeGA**、**FlashAvatar** 等优化类方法，以及 **GAGAvatar**、**LAM** 等前馈类方法）通常将面部和头发耦合在统一的 3D 高斯或 NeRF 表征中进行建模。这种耦合策略忽略了面部（平坦、连续表面）与头发（细长、链状结构）之间本质的几何差异，导致在稀疏输入下难以同时保持面部精度和发丝细节。

FHAvatar 的关键设计是将面部与头发在 UV 纹理空间中**显式解耦**为两个独立的表征分支：
- **面部分支**：将融合后的头部几何令牌解码为**平面高斯（planar Gaussians）**，每个 UV 像素对应一个高斯，参数包括位置偏移 $\Delta\mathbf{p}$、协方差 $\sigma$、旋转 $\mathbf{r}$、透明度 $\alpha$ 和颜色 $\mathbf{c}$（Eq.5）。平面高斯天然适配面部相对平坦的几何特性。
- **头发分支**：将头发令牌与原始 DiffLocks 特征融合后，通过冻结的 SIREN 链式生成器解码为 $S=256$ 个方向向量 $\mathbf{d}_{1:S}$（Eq.6），累积形成**链式高斯线段（strand-based Gaussians）**，并赋予颜色与透明度。链式高斯能够精确刻画发丝的细长拓扑和复杂走向。

消融实验强有力地验证了这一设计的有效性：**移除发丝分支（w/o Hair Branch）导致 PSNR 下降 1.82，SSIM 下降 0.014，LPIPS 上升 0.088**（Table 2），说明双分支解耦对头发重建质量至关重要。进一步的面部-头发区域解耦评估显示，FHAvatar 在面部 IoU 达 0.922，头发 IoU 达 0.826，分别领先最优基线 6.7% 和 36%（Table 3），证明了显式区域分离的精准度。

### 2. 几何感知的多视图聚合 Transformer

传统方法通常依赖固定视角或单视图输入，缺乏对多视图信息的有效整合能力。FHAvatar 引入了一个**聚合 Transformer 骨干网络**，能够处理任意数量和顺序的输入视图，通过交叉注意力机制将多视角图像特征融合到头部和头发表征中。

具体而言，该 Transformer 包含 4 层聚合块，其中：
- 头部令牌和头发令牌作为**查询（query）**，对多视图图像令牌进行交叉注意力，实现几何感知的特征聚合；
- 图像令牌之间进行帧级自注意力，以建模视图间关系；
- 部分自注意力层在头部和头发令牌间共享，促进**头-发结构一致性**的学习。

这一设计使得模型能够从多视图数据中学习到强大的**跨视图先验**，即使在极端稀疏输入下也能保持高质量重建。定量结果证实了这一点：**即使仅 1 帧输入，FHAvatar（single-pass）的 AKD 低至 3.96，远超 LAM 的 48.64**（Table 1），证明了多视图先验和 Transformer 聚合在稀疏输入下的强大泛化能力。

### 3. 自适应头发密度与长度感知下采样

头发分支的另一项关键创新是**自适应密度图引导的链数与高斯数下采样**。传统方法对头发区域采用均匀采样，无法适应不同发型的长度和密度差异。FHAvatar 从头发令牌中解码出头皮 UV 空间的密度图，根据平均发丝长度自适应地减少链数和每链高斯数 $S$。这使得模型能为不同发型产生差异化的总高斯数——例如男卷发约 54k，女长染发约 84k（Table 4），在质量-效率之间取得最佳平衡（Figure 10）。

### 4. 高效推理与可选快速细化

与逐身份需要数小时优化的方法（如 GaussianAvatars、MeGA）不同，FHAvatar 的核心推理是**单次前馈**过程。此外，论文提出了**可选的快速细化策略**：冻结编码器和 Transformer 骨干，仅对预测的聚合令牌和双分支解码器进行联合优化，耗时仅约一分钟。消融实验表明，**移除快速细化（w/o Finetune）使 PSNR 从 25.14 降至 23.85，SSIM 从 0.796 降至 0.780，LPIPS 从 0.333 升至 0.382**（Table 2），证明轻量化微调能显著提升身份细节保真度，同时保持实用级效率。

FHAvatar 建立了一条前馈重建流水线，其核心设计围绕一个关键洞察展开：面部与头发具有截然不同的几何特性——面部平坦连续，而头发呈链状离散——因此必须在表征层面显式解耦，而非沿用以往方法中统一的耦合建模。整个框架由三个主要阶段构成：**多源令牌化编码**、**多视图聚合 Transformer 骨干**、以及**双分支高斯解码与渲染**，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l1022_https_arxiv_org_abs_2603_23345/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline Overview. FHAvatar reconstructs a compositional face-and-hair 3D Gaussian head in the UV space. Our model starts with encoding image, hair, and face tokens from arbitrary input images and a template head mesh (Sec. 3.1.1), which are fed into the aggregated transformer backbone to perform attention-based multi-view feature aggregation (Sec. 3.1.2). The dual-branch decoders then independently decode planar Gaussians for the face and strand-based Gaussians for the hair at UV pixels, which are combined for real-time rendering under novel views and expressions (Sec. 3.1.3)*

**输入与令牌化编码。** 流水线接受任意数量与顺序的 RGB 图像 $\mathbf{I} \in \mathbb{R}^{N \times H \times W \times 3}$ 以及一个 FLAME 模板头部网格作为输入。编码阶段并行生成三类令牌：
- **图像令牌** $\mathbf{T}_{\mathrm{image}}$：利用冻结的 DINOv2 骨干提取多尺度视觉特征，再通过可训练的 DPTHead 将其投影为 $N \times P \times C$ 的令牌序列，为后续融合提供丰富的表观信息（Eq.1）。
- **头部几何令牌** $\mathbf{T}_{\mathrm{head}}$：对 FLAME 模板网格在 UV 空间的采样坐标 $\mathbf{X}$ 进行位置编码 $\gamma(\mathbf{X})$，经 MLP 映射为 $H_{\mathrm{uv}} \times W_{\mathrm{uv}} \times C$ 的几何令牌，为面部高斯提供结构先验（Eq.2）。
- **头发令牌** $\mathbf{T}_{\mathrm{hair}}$：先由预训练的 DiffLocks 从输入图像中提取单目头发特征 $f_{\mathrm{hair}}$，再与图像令牌进行交叉注意力增强，最后与头皮区域的位置编码相加，形成头发专用的令牌表示（Eq.3）。

**多视图聚合 Transformer 骨干。** 三类令牌被送入一个 4 层的聚合 Transformer 块。其核心机制是：头部令牌和头发令牌作为查询（query），对所有视图的图像令牌执行交叉注意力，从而从多视角数据中学习几何感知的跨视图先验；图像令牌内部则进行帧级自注意力以建模视角间关系。部分自注意力层在头、发令牌间共享，以促进面部与头发区域的结构一致性。该设计使得模型能够在一次训练中学习对任意帧数的泛化先验，无需针对不同输入数量重新训练。

**双分支高斯解码与渲染。** 聚合后的令牌分别进入两个独立的解码分支：
- **面部分支**：将融合后的头部令牌解码为平面高斯参数——包括 UV 空间的位置偏移 $\Delta\mathbf{p}$、协方差 $\sigma$、旋转 $\mathbf{r}$、透明度 $\alpha$ 和颜色 $\mathbf{c}$（Eq.5）。每个 UV 像素对应一个高斯，适配面部平坦连续的几何特性。
- **头发分支**：将头发令牌与原始 DiffLocks 特征融合，通过冻结的 SIREN 链式生成器解码为 $S=256$ 个方向向量 $\mathbf{d}_{1:S}$（Eq.6），累积形成链式线段并赋予链式高斯。同时，从头皮 UV 密度图自适应下采样链数与每链高斯数，使不同发型产生差异化的总高斯量（例如男卷发约 54k，女长染发约 84k），在质量与效率间取得平衡。

最终，面部与头发高斯被合并，根据目标表情进行变换，并通过可微光栅化渲染为 RGB 图像。由于高斯绑定在 FLAME UV 空间，重建结果支持实时表情驱动。

**可选快速细化。** 为进一步提升身份细节保真度，FHAvatar 提供一种轻量化微调策略：冻结编码器与 Transformer 骨干，仅对聚合后的令牌 $\mathbf{T}_{\mathrm{head}}$、$\mathbf{T}_{\mathrm{hair}}$ 及双分支解码器进行联合优化，耗时约一分钟级别，即可显著改善渲染质量（消融实验显示 PSNR 提升约 1.3 dB）。

**训练目标。** 总损失由三项组成（Eq.10）：头发区域分离损失 $\mathcal{L}_{\mathrm{hair}}$ 强制面部与头发高斯在语义掩码上分离；光度重建损失 $\mathcal{L}_{\mathrm{photo}}$ 约束渲染图像与真值的一致性；正则化项 $\mathcal{L}_{\mathrm{reg}}$ 稳定训练。

FHAvatar 的核心架构围绕“纹理空间解耦建模 + 多视图聚合 Transformer + 双分支高斯解码”三条主线展开。以下按流水线顺序阐述关键模块及其公式化表达。

### 图像令牌提取

为将任意数量的输入图像转化为 Transformer 可处理的令牌序列，FHAvatar 采用冻结的 DINOv2 骨干网络提取多尺度表示，再接一个可训练的 DPTHead 进行降维和融合：

$$
\mathbf{T}_{\mathrm{image}} = \mathrm{DPTHead}\left(\mathrm{DINOv2}(\mathbf{I})\right) \in \mathbb{R}^{N \times P \times C}
$$

其中 $\mathbf{I}$ 为 $N$ 张输入图像，$P$ 为每张图像的令牌数，$C$ 为通道维度。该设计利用了大规模预训练视觉基础模型的泛化能力，同时仅需训练轻量 DPTHead 即可适配头部重建任务。

### 头部几何令牌编码

面部区域在 UV 空间中具有规整的拓扑结构。FHAvatar 从 FLAME 模板网格的 UV 坐标出发，经位置编码后通过 MLP 生成几何先验令牌：

$$
\mathbf{T}_{\mathrm{head}} = \mathrm{MLP}\left(\gamma(\mathbf{X})\right) \in \mathbb{R}^{H_{\mathrm{uv}} \times W_{\mathrm{uv}} \times C}
$$

$\mathbf{X}$ 为 FLAME UV 空间的坐标，$\gamma(\cdot)$ 为位置编码函数。这些令牌为后续的面部分支解码提供了显式的几何锚点。

### 头发特征令牌化

头发具有链状细长结构，难以直接从通用图像特征中恢复。FHAvatar 引入 DiffLocks 提取单目头发特征，再通过交叉注意力与图像令牌交互，并叠加头皮位置编码：

$$
f_{\mathrm{hair}} = \mathrm{DiffLocks}(\mathbf{I}_{\mathrm{f}}), \quad \mathbf{T}_{\mathrm{hair}} = \mathrm{CrossAttn}(\mathbf{T}_{\mathrm{image}}, f_{\mathrm{hair}}) + \mathbf{T}_{\mathrm{head}}^{\mathrm{scalp}}
$$

$\mathbf{I}_{\mathrm{f}}$ 为输入图像的前景区域，$\mathbf{T}_{\mathrm{head}}^{\mathrm{scalp}}$ 为头皮区域的几何令牌。DiffLocks 提供的领域特定特征与图像令牌的交叉注意力机制，使得头发令牌既保留了单目线索，又融合了多视图上下文。

### 多视图融合 Transformer 骨干

上述三类令牌（图像、头部、头发）被送入 4 层聚合 Transformer 块。其核心操作包括：
- **头/发令牌作为查询** 对图像令牌进行交叉注意力，从多视图中聚合面部和发丝信息；
- **图像令牌进行帧级自注意力**，建模不同视角间的对应关系；
- **头部与头发令牌共享部分自注意力层**，促进面-发结构一致性学习。

该设计使模型能够处理任意数量和顺序的输入视图，并从中学习几何感知的跨视图先验，这是 FHAvatar 在稀疏输入下仍能保持高质量重建的关键。

### 双分支高斯解码器

#### 面部分支：平面高斯

面部分支将聚合后的头部令牌 $\mathbf{T}_{\mathrm{head}}$ 解码为 UV 空间中的平面高斯参数。所有参数共享卷积骨干，但各自拥有独立的 MLP 头：

$$
\{\Delta\mathbf{p}, \sigma, \mathbf{r}, \alpha, \mathbf{c}\} = \mathcal{D}_{\mathrm{face}}\big(\mathbf{T}_{\mathrm{head}}\big)
$$

各参数含义：
- $\Delta\mathbf{p}$：相对 FLAME 模板顶点的位置偏移；
- $\sigma$：高斯协方差（各向异性缩放）；
- $\mathbf{r}$：旋转四元数；
- $\alpha$：透明度；
- $\mathbf{c}$：RGB 颜色。

每个 UV 像素对应一个平面高斯，天然适配面部平坦的几何特性。

#### 头发分支：链式高斯

头发分支采用链式线段建模发丝的细长结构。首先将头发令牌 $\mathbf{T}_{\mathrm{hair}}$ 作为修正项与原始 DiffLocks 特征 $f_{\mathrm{hair}}$ 融合，经冻结的 SIREN 链式生成器解码为 $S = 256$ 个方向向量：

$$
\mathbf{d}_{1:S} = \mathcal{D}_{\mathrm{dir}}\left(\gamma\mathbf{T}_{\mathrm{hair}} + f_{\mathrm{hair}}\right)
$$

这些方向向量从头皮 UV 像素出发，逐段累积形成链式线段。每条线段上附着多个 3D 高斯，其颜色和透明度由额外解码器预测。此外，从 $\mathbf{T}_{\mathrm{hair}}$ 解码的头皮密度图引导自适应下采样：根据平均发丝长度和密度，动态调整激活的链数和每链高斯数，使不同发型（如男卷发约 54k 高斯，女长染发约 84k 高斯）均能达到质量-效率最优平衡。

### 渲染与动画

面部和头发高斯合并后，根据目标表情参数变换至世界空间，通过可微光栅化渲染为 RGB 图像。由于所有高斯均绑定在 FLAME UV 空间，表情驱动仅需更新模板变形，无需重新推理，从而支持实时动画。

### 训练目标

总损失由三部分构成：

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{hair}} + \mathcal{L}_{\mathrm{photo}} + \mathcal{L}_{\mathrm{reg}}
$$

- $\mathcal{L}_{\mathrm{hair}}$：头发区域分离损失，包含头发掩码的 L2 损失和语义渲染的分割损失，确保面部和头发高斯在空间上正确分离；
- $\mathcal{L}_{\mathrm{photo}}$：光度重建损失（L1 + 感知损失），约束渲染图像与真值的一致性；
- $\mathcal{L}_{\mathrm{reg}}$：正则化项，包括高斯参数的正则约束。

### 可选快速细化

为进一步提升身份细节，FHAvatar 提供可选的轻量化微调阶段：冻结编码器和 Transformer 骨干，仅联合优化聚合令牌 $\mathbf{T}_{\mathrm{head}}$、$\mathbf{T}_{\mathrm{hair}}$ 和双分支解码器。该阶段仅需约一分钟，即可在保持泛化性的前提下显著提升重建保真度（PSNR 从 23.85 提升至 25.14，见 Table 2 消融）。

## 实验与关键发现

### 主要定量结果

FHAvatar在NeRSemble数据集上进行了系统评估，涵盖1帧、3帧、6帧和16帧输入设置。Table 1汇总了与扩散类方法（**DiffusionRig**）、前馈类方法（**GAGAvatar**、**LAM**）和优化类方法（**FlashAvatar**、**GaussianAvatars**、**MeGA**）的全面对比。所有方法均在黑背景下渲染以计算指标，建模时间不含可预计算的驱动参数估计，FPS为动画渲染帧率。

在6帧输入条件下，FHAvatar（full，含快速细化）取得PSNR 23.71、SSIM 0.825、LPIPS 0.296、AKD 3.08、CSIM 0.721，在所有指标上均达到最优或接近最优水平。与优化类方法**GaussianAvatars**（PSNR 23.44、AKD 7.41）相比，FHAvatar在身份保持指标AKD上领先4.33点，CSIM高出0.256，同时建模时间从小时级降至分钟级。前馈类方法**GAGAvatar**和**LAM**在稀疏输入下身份相似度严重退化，而扩散类方法**DiffusionRig**在新表情或新视角下控制精度不足。

在极稀疏的1帧输入下，FHAvatar（single‑pass，无细化）仍取得PSNR 22.46、AKD仅3.96，远优于**LAM**（PSNR 16.41、AKD 48.64），证明多视图先验和Transformer聚合在稀疏输入下具有强泛化能力。

### 面部-头发解耦评估

Table 3报告了面部区域与头发区域的分别评估结果。FHAvatar在面部IoU达0.922，头发IoU达0.826，分别领先最优基线6.7%和36%。这一显著优势验证了显式区域分离设计对精准建模两类几何的贡献——面部区域受益于平面高斯建模，头发区域则通过链式高斯捕捉发丝结构。

### 消融实验

Table 2和Figure 4呈现了关键消融结果：

- **移除发丝分支（w/o Hair Branch）**：PSNR下降1.82，SSIM下降0.014，LPIPS上升0.088。Figure 4显示，缺少发丝分支后头发区域呈现模糊、非链状的几何结构，无法形成清晰的发丝。
- **移除快速细化（w/o Finetune）**：PSNR从25.14降至23.85，SSIM从0.796降至0.780，LPIPS从0.333升至0.382。轻量化微调（冻结编码器和Transformer骨干，仅优化聚合令牌和解码器）在约一分钟内显著提升身份细节保真度。
- **输入帧数影响**：Figure 5的消融曲线显示，从1帧增至6帧时PSNR/SSIM持续提升，6帧后收益递减，表明模型在少量输入下已能充分利用多视图信息。

### 自适应头发分支分析

头发分支在头皮UV分辨率和基顶点数上存在质量-效率权衡（Figure 10）。UV分辨率112、基顶点数24时达到最佳平衡。Table 4展示了自适应机制的效果：不同发型产生差异化的总高斯数——男卷发约54k，女长染发约84k——证明长度感知的链数/高斯数下采样能根据发型复杂度动态分配计算资源。

![[assets/figures/papers/paper_list_l1022_https_arxiv_org_abs_2603_23345/figures/015_Figure_10.jpg]]
*Figure 10: Quality-Efficiency Trade-off in the Hair Branch*

### 应用与鲁棒性验证

FHAvatar的面部-头发可组合设计支持发型迁移（Figure 6），即使跨性别也能无缝转移。纹理空间编辑直接反映到3D高斯（Figure 7），无需重新推理。Figure 9展示了在非正面、极稀疏等挑战性输入下的鲁棒重建结果，Figure 12进一步验证了对长波浪、卷曲等复杂发型的处理能力。

![[assets/figures/papers/paper_list_l1022_https_arxiv_org_abs_2603_23345/figures/007_Figure_6.jpg]]
*Figure 6: Hairstyle Transferring. The compositional face-andhair dual-branch design enables seamless hairstyle transfer between our avatars, even across different genders*

![[assets/figures/papers/paper_list_l1022_https_arxiv_org_abs_2603_23345/figures/008_Figure_7.jpg]]
*Figure 7: Stylize Editing. Texture-based editing or stylization on the reconstruction result enables convenient 3D-aware manipulation without re-inference*

### 局限性

尽管FHAvatar在面部-头发重建上表现优异，其重建和动画基于FLAME模型，难以表示舌头、细微面部皱纹等FLAME未建模的静态区域和动态细节。此外，训练数据的发型分布偏差可能导致复杂配饰或不常见发型的重建失败。

### 补充图表

![[assets/figures/papers/paper_list_l1022_https_arxiv_org_abs_2603_23345/figures/003_Table_1.jpg]]
*Table 1: Quantitative Results under both single-view and multi-view input settings. Note that our model was trained once on mixed input numbers to learn generalizable priors. Modeling time denotes the time required to reconstruct the 3DGS model, excluding the estimation of driving parameters that can be precomputed in advance, while FPS corresponds to the frame rate during the animation rendering process of the output model. All methods are rendered on a black background for metrics calculation*

![[assets/figures/papers/paper_list_l1022_https_arxiv_org_abs_2603_23345/figures/005_Table_2.jpg]]
*Table 2: Ablation Study*

![[assets/figures/papers/paper_list_l1022_https_arxiv_org_abs_2603_23345/figures/006_Figure_4.jpg]]
*Figure 4: Ablation Study. Best viewed with zoom-in*

![[assets/figures/papers/paper_list_l1022_https_arxiv_org_abs_2603_23345/figures/011_Table_3.jpg]]
*Table 3: Face-Region and Hair-Region Evaluation Results*

![[assets/figures/papers/paper_list_l1022_https_arxiv_org_abs_2603_23345/figures/013_Table_4.jpg]]
*Table 4: Adaptive Hair Gaussians*

![[assets/figures/papers/paper_list_l1022_https_arxiv_org_abs_2603_23345/figures/012_Figure_9.jpg]]
*Figure 9: Results under challenging inputs and viewpoints*

![[assets/figures/papers/paper_list_l1022_https_arxiv_org_abs_2603_23345/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative Comparison on reconstructing unseen identities from both in-the-wild data and the NeRSemble dataset under different capture conditions. LAM struggles to preserve identity similarity, while GAGAvatar and DiffusionRig fail to maintain accurate control under novel expressions or viewpoints. Optimization-based methods such as GaussianAvatars, FlashAvatar, and MeGA often fail to fit under sparse inputs. In contrast, our method delivers high rendering quality, supports accurate expression reenactment, and maintains consistent identity*

## 定位与知识库关联

### 1. 方法谱系：从耦合建模到显式解耦

FHAvatar 处于**3D头部Avatar重建**这一研究脉络中，其核心突破在于将面部与头发的表征从“耦合建模”推进到“显式解耦建模”。现有方法可大致归为三类，FHAvatar 针对每一类的瓶颈做出了差异化改进：

**优化类方法（Optimization-based）** 如 **GaussianAvatars**、**FlashAvatar**、**MeGA**，通常对每个身份进行数十分钟到数小时的逐例优化，在密集多视图（如16帧以上）下可取得高质量结果。然而，当输入视图稀疏（如1–6帧）时，优化过程缺乏足够的跨视角约束，容易陷入局部最优，导致几何坍塌或纹理模糊。FHAvatar 通过**前馈推理+可选一分钟级微调**的范式，将重建时间从小时级压缩至分钟级，且在6帧输入下，PSNR（23.71）已超越 GaussianAvatars（23.44），AKD（3.08）更是远低于后者的7.41（Table 1），证明前馈先验在稀疏输入下比逐例优化更具鲁棒性。

**前馈类方法（Feed-forward）** 如 **GAGAvatar**（单视图3D头部生成）和 **LAM**（单视图面部重建），虽具备实时推理能力，但受限于单视图输入的固有歧义性，难以恢复完整的头部几何，尤其是头发区域。LAM在单帧输入下的AKD高达48.64，而FHAvatar（single-pass）仅3.96（Table 1），差距超过一个数量级。这一优势源于FHAvatar的**聚合Transformer骨干**：它接受任意数量与顺序的视图，通过交叉注意力将多视角图像令牌融合为几何感知的头部与头发令牌，从而学习到强大的跨视图先验。

**扩散类方法（Diffusion-based）** 如 **DiffusionRig**，通过迭代多视图重建来提升质量，但推理速度慢，且在新表情或新视角下难以保持精确控制（Figure 3定性结果佐证）。FHAvatar 以单次前馈即可生成可驱动的高斯Avatar，在效率与可控性上形成代际优势。

### 2. 知识库定位：关键设计决策的因果机制

FHAvatar 的架构可视为对以下核心问题的逐层回答：

**问题一：面部与头发应共享还是分离表征？**  
面部几何以平坦表面为主，适合用**平面高斯（Planar Gaussian）** 建模；头发则呈现链状、细长、高曲率的几何特性，需要**链式高斯（Strand-based Gaussian）** 来捕捉发丝走向。FHAvatar 的双分支解码器正是对这一几何差异的直接回应。消融实验（Table 2）提供了强因果证据：移除发丝分支（w/o Hair Branch）导致PSNR下降1.82，SSIM下降0.014，LPIPS上升0.088。Figure 4进一步可视化显示，无发丝分支时头发呈现模糊的非链状几何，验证了链式高斯对发丝精细建模的不可替代性。

**问题二：如何从稀疏多视图中获取足够的头发几何先验？**  
FHAvatar 引入了**DiffLocks**（单目头发特征提取器）与聚合Transformer的级联设计。DiffLocks从每帧图像中提取初始头发特征，随后作为查询与多视图图像令牌进行交叉注意力，使头发令牌能够聚合来自不同视角的互补信息。这一设计使得即使单帧输入，头发令牌也能借助训练中学到的跨视角先验补偿缺失视角的信息——这正是单帧AKD低至3.96的关键机制。

**问题三：如何平衡头发建模的精度与效率？**  
FHAvatar 提出了**自适应头发密度图与长度感知下采样**策略。头皮UV空间中的密度图从头发令牌解码而来，根据发型的平均链长度自适应调整链数和每链高斯数。Table 4显示，男卷发约54k高斯，女长染发约84k高斯，证明该机制能为不同发型产生差异化的计算资源分配。Figure 10和Table 4进一步给出了UV分辨率与基顶点数的质量–效率权衡曲线，在头皮UV分辨率112、基顶点数24时达到最佳平衡。

**问题四：如何在不破坏泛化性的前提下提升身份细节？**  
FHAvatar 的**可选快速细化（Optional Fast Refinement）** 提供了一种精巧的解决方案：冻结编码器（DINOv2+DPTHead）和Transformer骨干，仅微调聚合后的头部/头发令牌和双分支解码器。这一设计保留了前馈先验的泛化能力，同时允许解码器适应特定身份的细节。消融实验（Table 2）显示，移除微调使PSNR从25.14降至23.85，LPIPS从0.333升至0.382，验证了轻量化微调的有效性。

### 3. 适用边界与局限

FHAvatar 的适用边界由其底层依赖和技术假设划定：

**FLAME模型的表达上限**：FHAvatar的重建与动画均基于FLAME模板网格。FLAME本身不建模舌头、细微面部皱纹、牙齿等静态区域和动态细节，因此FHAvatar天然无法表示这些结构。这是所有基于FLAME的方法（包括GaussianAvatars、MeGA等）的共同局限，而非FHAvatar的特有缺陷。

**训练数据的发型分布偏差**：FHAvatar的头发分支在训练中学习到的先验受限于训练集的发型分布。对于复杂配饰（如发带、发夹）、极端发型（如莫西干头）或罕见发质，重建可能失败。Figure 12展示了部分挑战性发型的结果，但论文未提供系统性的失败案例分析，该局限的严重程度需要实际测试验证。

**“随意拍摄”的隐含假设**：FHAvatar声称支持“few casual captures”，但其评估仍主要在NeRSemble（受控多视角数据集）上进行。In-the-wild数据虽有展示（Figure 3），但缺乏大规模定量评估。在极端光照、遮挡或运动模糊下的鲁棒性尚未被充分验证。

### 4. 开放问题

FHAvatar 留下的开放问题指向3D头部Avatar重建的下一阶段挑战：

1. **超越FLAME的动态细节建模**：如何将舌头、微皱纹、眼球运动等FLAME未覆盖的动态细节集成到3D高斯框架中？可能的路径包括引入额外的局部变形场或神经纹理，但这需要对应的训练数据（如多视角舌头扫描）支持。

2. **复杂发型与配饰的泛化**：能否利用生成模型（如扩散先验）或合成数据增强来缓解发型分布偏差？FHAvatar的UV空间表征天然适合纹理编辑（Figure 7），但几何层面的配饰重建仍是一个开放难题。

3. **显式物理驱动的头发动态**：当前FHAvatar的头发动画通过高斯绑定在FLAME UV空间实现，本质上是运动学驱动。能否将链式高斯进一步赋予物理属性（如质量、刚度），实现更逼真的动态模拟（如风吹、碰撞）？这需要解决高斯表示与物理求解器的接口问题。

4. **单帧输入的极限质量**：FHAvatar在单帧输入下已显著超越现有方法，但单帧AKD（3.96）与6帧（3.08）之间仍有差距。能否通过更强的生成先验（如预训练的3D头发扩散模型）进一步缩小这一差距，使单次拍摄即可达到多帧质量？

## 原文 PDF

![[paperPDFs/CVPR_2026/FHAvatar_Fast_and_High_Fidelity_Reconstruction_of_Face_and_Hair_Composable_3D_Head_Avatar_from_Few_Casual_Captures.pdf]]
