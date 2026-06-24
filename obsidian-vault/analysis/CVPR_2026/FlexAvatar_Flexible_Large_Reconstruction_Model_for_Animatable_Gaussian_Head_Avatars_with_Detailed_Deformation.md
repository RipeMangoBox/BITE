---
title: "FlexAvatar: Flexible Large Reconstruction Model for Animatable Gaussian Head Avatars with Detailed Deformation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FlexAvatar_Flexible_Large_Reconstruction_Model_for_Animatable_Gaussian_Head_Avatars_with_Detailed_Deformation.pdf
project_link: "https://pengc02.github.io/flexavatar"
code_link: null
aliases:
- FlexAvatar
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 利用结构化Head Query令牌和Transformer注意力机制实现对任意数量、无相机姿态和无表情标签的图像输入的鲁棒融合，并采用基于UV位置图的轻量级UNet解码器实时生成表情依赖的高斯属性变形。
primary_logic: Transformer的跨注意力机制可以对变长、无姿态和无表情的视觉token序列进行规范化表示，结合UV空间特征对齐与UNet驱动的动态变形解码，既保证了多视角3D一致性，又能以45 FPS渲染细节丰富的表情变化。
claims:
- 在NeRSemble测试集上，FlexAvatar的前馈模型无需任何相机姿态或表情标签，在自重建任务上的PSNR达到21.15，显著超过最先进单图头像方法GAGAvatar（19.17），并在CSIM、AKD等指标上全面领先。
- 消融实验证实，移除UV位置图驱动或数据分布调整会导致动态纹理（皱纹、牙齿）明显退化，表明这些组件是精细动态细节的关键。
- NeRSemble (Self Reenactment) 上 PSNR↑ = 21.1516
- NeRSemble (Self Reenactment) 上 SSIM↑ = 0.8335
---

# FlexAvatar: Flexible Large Reconstruction Model for Animatable Gaussian Head Avatars with Detailed Deformation

> [!tip] 核心洞察
> Transformer的跨注意力机制可以对变长、无姿态和无表情的视觉token序列进行规范化表示，结合UV空间特征对齐与UNet驱动的动态变形解码，既保证了多视角3D一致性，又能以45 FPS渲染细节丰富的表情变化。

| 字段 | 内容 |
|------|------|
| 中文题名 | FlexAvatar: 灵活的大型可动画高斯头部头像重建模型及细致变形 |
| 英文题名 | FlexAvatar: Flexible Large Reconstruction Model for Animatable Gaussian Head Avatars with Detailed Deformation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.17717) · [Project](https://pengc02.github.io/flexavatar) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FlexAvatar |
| Dataset | NeRSemble, FaceCap, Inference Speed |

> [!tip] 效果简介
> - NeRSemble (Self Reenactment) 上，PSNR↑ 21.1516 vs 19.1667 (GAGAvatar) (+1.9849)；SSIM↑ 0.8335 vs 0.8283 (GAGAvatar) (+0.0052)；LPIPS↓ 0.2193 vs 0.2567 (GAGAvatar) (-0.0374)。
> - FaceCap (Ablation) 上，PSNR↑ 23.32 vs 22.74 (w/o Distri Adj) (+0.58)；LPIPS↓ 0.1797 vs 0.1868 (w/o Distri Adj) (-0.0071)。
> - Inference Speed 上，FPS 45 vs 8 (Avat3R, reported) (+37)。

## 概述

### 问题瓶颈

现有3D头部头像重建方法在实际部署中面临三重刚性约束：**输入灵活性受限**（通常依赖多视角捕获、已知相机姿态和表情标签）、**动态细节生成质量不足**（如皱纹、牙齿等表情依赖纹理难以真实呈现），以及**实时性与高质量难以兼顾**。这些约束使得现有方案难以在“随手拍”式的稀疏、无标注输入条件下生成细节丰富的可动画头像。

### 核心方法

FlexAvatar提出了一种**灵活的大规模重建模型**，其核心思路是利用Transformer的结构化注意力机制，将“任意数量、无相机姿态、无表情标签”的输入图像聚合为规范化的头部表示，再通过UV空间的特征对齐与轻量UNet解码器实时生成表情驱动的动态高斯变形。该方法的关键创新在于：

- **输入无关性融合**：通过全局自注意力层融合任意数量（1–4张）图像特征，无需相机姿态或表情标签。
- **规范空间锚定**：使用可学习的Head Query令牌通过交叉注意力将多视角特征聚合为UV特征图，建立3D几何约束。
- **动态变形解码**：以FLAME UV位置图作为驱动信号，输入轻量UNet生成表情依赖的高斯属性差值，实现45 FPS的实时渲染。

### 方法谱系与知识库定位

FlexAvatar定位于**前馈式3D高斯泼溅头像重建**赛道，与以下基线方法形成直接对比：

| 方法 | 输入条件 | 核心机制 | 动态细节 |
|------|----------|----------|----------|
| **GAGAvatar** | 单图，需表情标签 | 基于FLAME的显式变形 | 细节不足 |
| **Portrait4D-v1/v2** | 单图，需相机姿态 | 视频驱动动态建模 | 受限于输入姿态 |
| **HeadGAP** | 单图 | 高斯参数预测 | 静态为主 |
| **Avat3R** | 稀疏视图 | 大型重建模型 | 推理速度慢（8 FPS） |
| **FlexAvatar (本文)** | **1–4图，无姿态/表情** | **Transformer融合 + UV UNet变形** | **45 FPS，细节丰富** |

FlexAvatar在方法层面吸收了大型重建模型（如Avat3R）的Transformer融合范式，但通过引入UV位置图驱动的UNet解码器，实现了更高效、更精细的动态变形。其数据分布调整策略（锚点表达重采样）进一步解决了稀有表情的学习困难，这一设计在现有工作中较为独特。

### 主要结果速览

在NeRSemble测试集的自重建任务上，FlexAvatar的前馈模型（无需任何相机姿态或表情标签）**PSNR达到21.15，显著超过GAGAvatar（19.17）**，并在CSIM、AKD等身份保持指标上全面领先。消融实验证实，UV位置图驱动和数据分布调整是动态细节（皱纹、牙齿）生成的关键组件——移除后会导致明显的纹理退化。推理速度方面，FlexAvatar以45 FPS远超Avat3R的8 FPS，满足实时交互需求。

## 背景与动机

真实感3D头部头像的重建与动画是计算机视觉与图形学中的核心课题，在远程通信、虚拟现实和数字人等领域具有广泛需求。近年来，基于3D高斯泼溅（3D Gaussian Splatting, 3DGS）的方法在渲染质量和速度上取得了显著进展，但其在可动画头像生成方面仍面临两个根本性瓶颈。

**第一个瓶颈是输入灵活性不足。** 现有方法通常依赖多视角捕获系统、已知的相机姿态和精确的表情标签（如FLAME参数）来构建3D表示。例如，基于显式几何的方法需要固定数量的标定视角输入，而基于前馈重建的方法虽然减少了对多视角的依赖，但仍普遍假设相机姿态已知或表情标签可用。这种对受控采集条件的依赖严重限制了方法在实际场景中的适用性——用户往往只能提供1至4张任意姿态、任意表情的普通照片，且无法提供相机标定信息或表情注释。

**第二个瓶颈是动态细节的生成质量不足。** 可动画头像的核心挑战在于如何根据驱动表情实时生成逼真的动态纹理变化，如皱纹的浮现与消失、牙齿的显露与遮挡。现有方法多采用多层感知机（MLP）或繁重的交叉注意力机制来驱动高斯变形，或直接依赖FLAME模型的线性混合蒙皮（LBS）进行形变，但这些方案往往无法捕捉与表情高度相关的精细几何和纹理变化。此外，训练数据的分布偏差——稀有表情（如夸张的闭眼、张嘴露齿）在数据集中占比过低——进一步加剧了动态细节生成的退化。

上述两个瓶颈之间存在深层关联：输入灵活性的缺失迫使方法依赖显式的姿态/表情先验来完成多视图融合与变形驱动，而动态细节的不足则反映了现有表示和解码架构在无监督条件下学习表情-外观映射的能力有限。

FlexAvatar的动机正是同时解决这两个相互制约的问题。其核心洞察在于：Transformer的交叉注意力机制天然具备对变长、无序序列的规范化表示能力，这使得模型可以在不依赖相机姿态和表情标签的条件下，将任意数量的输入图像聚合为统一的规范头部表示；而将这一规范表示建立在FLAME的UV空间中，并利用UV位置图作为驱动信号，则使得轻量级UNet解码器能够以45 FPS的实时速度生成表情依赖的高斯属性变形，从而在不牺牲效率的前提下实现细节丰富的动态纹理。这种“灵活输入融合 + UV空间动态解码”的设计范式，为构建真正实用的可动画头像系统提供了新的技术路径。

## 核心创新

FlexAvatar 的核心创新在于构建了一套**输入灵活、驱动实时、细节丰富**的前馈式可动画高斯头部头像重建框架。与现有方法相比，其关键突破体现在以下三个维度的 changed slots 上。

### 1. 输入条件的彻底解耦：从“强约束”到“零约束”

传统方法（如 **GAGAvatar**、**Portrait4D-v1/v2**、**HeadGAP** 等）通常依赖固定数量的多视角输入，且需要已知的相机姿态和表情标签作为先验。FlexAvatar 彻底打破了这一限制：它支持 **1～4 张任意姿态和表情的无标签图像**作为输入，无需任何相机参数或表情标注（Abstract, Sec 1）。

这一能力的技术基础在于其**输入数目无关的融合机制**。系统使用冻结的 DINOv3 基础视觉 Transformer 从每张图像提取多尺度特征，随后通过一个全局自注意力层将所有图像特征融合为统一的聚合表示 $F_{\mathrm{agg}}$（Eq. (2)）。由于自注意力机制天然支持变长序列，该设计使得模型能够处理任意数量的输入视图，而无需修改网络结构或重新训练。

### 2. 规范头部表示：可学习的 Head Query 令牌

实现“无姿态、无表情”输入融合的关键在于**结构化 Head Query 令牌**的设计。FlexAvatar 引入一组可学习的查询令牌 $Q_{\mathrm{H}}$，通过交叉注意力机制从聚合图像特征中提取规范化的头部表示：

$$F_{\mathrm{Q}} = \mathrm{CrossAttn}(Q_{\mathrm{H}}, F_{\mathrm{agg}}) = \mathrm{softmax}\left(\frac{Q_{\mathrm{H}} K_{\mathrm{agg}}^{\top}}{\sqrt{D}}\right) V_{\mathrm{agg}}$$

这一设计的因果逻辑在于：交叉注意力自动学习将不同视角、不同表情下的图像特征对齐到统一的规范空间，从而隐式地完成了相机姿态和表情的解耦（Sec 3.1, Eq. (3)）。随后，查询令牌被重塑为 UV 特征图 $F_{\mathrm{UV}}$，建立了与 FLAME 模型的显式 3D 几何对应关系（Eq. (4)）。

### 3. 动态变形的精细化驱动：UV 位置图 + 轻量 UNet

在动态变形解码方面，现有方法多采用 MLP 或繁重的交叉注意力机制驱动高斯变形，或直接依赖 FLAME 参数但细节生成不足。FlexAvatar 的创新在于**将 FLAME UV 位置图作为驱动信号**，与身份特征图沿通道维度拼接后，输入轻量级 UNet 解码器生成表情依赖的动态高斯属性差值：

$$\Delta G_{\mathrm{dyn}} = \mathrm{UNet}(\tilde{F}_{UV}), \quad \tilde{F}_{UV} = F_{\mathrm{id}} \oplus P_{\mathrm{driving}}$$

消融实验证实，用 FLAME 系数逐像素拼接替代 UV 位置图会严重削弱动态纹理质量，导致皱纹和牙齿缺失（Fig. 4(a), Table 2 w/o Position Map）。这表明 UV 位置图显式编码了面部区域的几何对应关系，为 UNet 提供了精确的空间引导信号。

### 4. 训练数据分布调整：缓解稀有表情的欠拟合

一个容易被忽视但效果显著的创新是**数据分布调整策略**。FlexAvatar 从 FLAME 表情空间中选取 20 个锚点表达，并基于余弦相似度对训练样本进行重采样，增加边际表情（如眼轮匝肌夸张动作、张嘴露齿）的占比（Sec 3.2, Fig. 5(c)）。消融实验表明，该策略将 FaceCap 上的 PSNR 从 22.74 提升至 23.32，LPIPS 从 0.1868 降至 0.1797（Table 2 w/o Distri Adj），显著改善了稀有表情的渲染质量（Fig. 4(b)）。

### 创新总结

FlexAvatar 的 changed slots 构成了一个完整的因果链条：**输入灵活性**（任意数量、无姿态无表情）→ **规范表示**（Head Query 交叉注意力）→ **精细驱动**（UV 位置图 + UNet）→ **数据平衡**（锚点重采样）。这一链条使得系统能够以 45 FPS 的实时速度渲染细节丰富的表情变化，在 NeRSemble 自重建任务上达到 21.15 PSNR，显著超过单图头像方法 GAGAvatar 的 19.17（Table 1）。

## 整体框架

FlexAvatar 的整体流程遵循“前馈重建 + 动态变形解码”的两阶段范式，目标是从单张或稀疏（1–4 张）无相机姿态、无表情标签的输入图像中，实时重建可动画的 3D 高斯头部头像。其核心设计在于将 Transformer 的灵活融合能力与 UV 空间的几何约束相结合，使得模型能够应对输入数量、视角和表情的任意变化。

**输入与编码。** 给定 $N$ 张任意姿态、任意表情的 RGB 图像 $\{I_i\}_{i=1}^N$，首先使用冻结的 DINOv3 视觉编码器 $E(\cdot)$ 提取多尺度密集特征 $f_i = E(I_i) \in \mathbb{R}^{L \times D}$（公式 1）。随后，一个全局自注意力层将所有图像特征融合为聚合特征 $F_{\mathrm{agg}} \in \mathbb{R}^{(N \times L) \times D}$，实现输入数量无关的表示（公式 2）。

**规范头部表示构建。** 融合后的特征通过一组可学习的 Head Query 令牌 $Q_{\mathrm{H}}$ 进行交叉注意力聚合：

$$F_{\mathrm{Q}} = \mathrm{CrossAttn}(Q_{\mathrm{H}}, F_{\mathrm{agg}}) = \mathrm{softmax}\left(\frac{Q_{\mathrm{H}} K_{\mathrm{agg}}^{\top}}{\sqrt{D}}\right) V_{\mathrm{agg}}$$

得到规范头部表示 $F_{\mathrm{Q}}$（公式 3）。该表示不依赖任何相机姿态或表情标签，仅从图像内容中推断身份与几何信息。随后，$F_{\mathrm{Q}}$ 被重塑为 UV 空间特征图 $F_{\mathrm{UV}} \in \mathbb{R}^{H \times W \times D}$（公式 4），其中 $N_H = H \cdot W$，从而在 3D 几何与 2D 特征之间建立显式映射（UV 结构见 Figure 8，采用 $400 \times 400$ 分辨率）。

**静态高斯属性解码。** UV 特征图经卷积解码器后，输出身份特征图 $F_{\mathrm{id}}$ 和静态高斯属性 $G_{\mathrm{st}}$（公式 5），包括位置、不透明度、颜色、尺度和旋转。这一阶段完成了对头部身份和静态外观的建模。

**动态变形驱动。** 给定驱动表情的 FLAME UV 位置图 $P_{\mathrm{driving}}$，将其与身份特征图沿通道维度拼接：

$$\tilde{F}_{UV} = F_{\mathrm{id}} \oplus P_{\mathrm{driving}}$$

形成动态解码的输入（公式 6）。轻量 UNet 解码器从拼接特征中生成表情依赖的动态高斯属性差值 $\Delta G_{\mathrm{dyn}}$（公式 7），再通过区域掩码与静态高斯融合：

$$G_{\mathrm{dyn}} = G_{\mathrm{st}} + M_{\mathrm{dyn}} \odot \Delta G_{\mathrm{dyn}}$$

得到最终动态高斯点云 $G_{\mathrm{dyn}}$（公式 8）。该设计使得动态纹理（皱纹、牙齿等）能够被精细建模，同时保持推理速度达到 45 FPS。

**渲染与可选微调。** 动态高斯点云经 FLAME 线性混合蒙皮（LBS）后，通过可微分高斯泼溅渲染器 $\mathcal{R}$ 生成最终图像 $I = \mathcal{R}(\mathrm{LBS}(G_{\mathrm{dyn}}), \Theta)$（公式 9）。此外，FlexAvatar 提供可选的 10 秒微调模块（冻结动态 UNet，仅优化解码器参数），在保持变形质量的同时显著提升输入图像的身份一致性和个性化细节。

整个框架的模块关系与数据流如 Figure 2 所示，网络架构的超参数配置见 Table 3。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2512_17717/figures/003_Figure_2.jpg]]
*Figure 2: FlexAvatar reconstructs a high-quality Gaussian head avatar by mapping a flexible number of input images with varying expressions and camera views into Gaussian representations in UV space. We use a flexible feed-forward backbone to obtain static Gaussian attributes and an identity feature map from input images. Given a driving expression signal, we then convert it into a FLAME UV position map and concatenate it with the backbone’s identity feature map; to support real-time driving and produce high-quality dynamic results, the concatenated representation is then fed into a UNet to generate expression-dependent dynamic Gaussian attributes in UV space, which are then sampled into FLAME space...*

## 核心模块与公式推导

FlexAvatar 的整体设计遵循“前馈大型重建模型”范式，其核心架构由三个关键模块串联构成：**灵活输入融合编码器**、**UV 空间特征解码器**、以及**动态变形 UNet 解码器**。以下按数据流顺序逐一展开。

---

### 3.1 灵活输入融合编码器

该模块的目标是将任意数量（1–4 张）、无相机姿态、无表情标签的输入图像聚合为一个规范的头部表示，从根本上解耦输入条件与重建质量之间的刚性约束。

**图像特征提取**：每张输入图像 $I_i$ 通过冻结的 DINOv3 视觉 Transformer 编码器 $E(\cdot)$ 提取多尺度稠密特征：

$$f_i = E(I_i), \quad i \in \{1, \dots, N\} \tag{1}$$

其中 $f_i \in \mathbb{R}^{L \times D}$，$L$ 为 token 序列长度，$D$ 为特征维度。

**输入数目无关融合**：将所有图像特征拼接后送入一个全局自注意力层，实现跨图像的 token 级交互：

$$F_{\mathrm{agg}} = \mathrm{SelfAttn}(f_1, f_2, \ldots, f_N) \tag{2}$$

自注意力机制天然支持变长输入序列，使得融合过程对输入图像数量 $N$ 不敏感——这是 FlexAvatar 区别于多数需要固定视角数方法的结构性优势。

**Head Query 交叉注意力聚合**：引入一组可学习的结构化 Head Query 令牌 $Q_{\mathrm{H}}$，通过交叉注意力从聚合特征 $F_{\mathrm{agg}}$ 中提取与身份和几何相关的规范表示：

$$F_{\mathrm{Q}} = \mathrm{CrossAttn}(Q_{\mathrm{H}}, F_{\mathrm{agg}}) = \mathrm{softmax}\left(\frac{Q_{\mathrm{H}} K_{\mathrm{agg}}^{\top}}{\sqrt{D}}\right) V_{\mathrm{agg}} \tag{3}$$

其中 $K_{\mathrm{agg}}$、$V_{\mathrm{agg}}$ 由 $F_{\mathrm{agg}}$ 线性投影得到。Head Query 令牌充当“规范锚点”，将变长、多姿态、多表情的视觉证据压缩为固定维度的隐式头部表示，无需显式相机姿态或表情标签。

**UV 特征图重塑**：将查询令牌输出 $F_{\mathrm{Q}}$ 按预设的 UV 拓扑重塑为二维特征图：

$$F_{\mathrm{UV}} \in \mathbb{R}^{H \times W \times D}, \quad N_H = H \cdot W \tag{4}$$

这一操作将 Transformer 的 token 空间映射到 FLAME 模型的 UV 参数域，为后续的几何约束和动态变形提供了结构化的空间载体。本文采用 $400 \times 400$ 的 UV 分辨率（详见 Figure 8）。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2512_17717/figures/011_Figure_8.jpg]]
*Figure 8: UV Structure. Our method use a 400 × 400 UV map structure to establish the mapping relationship between the Gaussian primitives and the FLAME model*

---

### 3.2 UV 空间特征解码与静态高斯生成

将 UV 特征图 $F_{\mathrm{UV}}$ 送入卷积解码器，同时输出身份特征图 $F_{\mathrm{id}}$ 和静态高斯属性图 $G_{\mathrm{st}}$：

$$F_{\mathrm{id}}, G_{\mathrm{st}} = \operatorname{Decoder}(F_{\mathrm{UV}}) \tag{5}$$

静态高斯属性 $G_{\mathrm{st}}$ 包含每个 UV 像素对应的高斯原语的**位置**、**不透明度**、**颜色**、**尺度**和**旋转**。这些属性定义了中性表情下的头部几何与外观，构成后续动态变形的基座。身份特征图 $F_{\mathrm{id}}$ 则编码了与个体相关的纹理和形状信息，将在动态解码阶段与驱动信号融合。

---

### 3.3 动态变形 UNet 解码器

动态变形模块是 FlexAvatar 实现实时高质量表情驱动的核心。其关键设计在于**驱动信号的选择**和**解码器架构的轻量化**。

**驱动信号**：给定目标表情的 FLAME 参数，将其转换为 UV 位置图 $P_{\mathrm{driving}}$——即每个 UV 像素在变形后的 3D 空间坐标。将 $P_{\mathrm{driving}}$ 与身份特征图 $F_{\mathrm{id}}$ 沿通道维度拼接：

$$\tilde{F}_{UV} = F_{\mathrm{id}} \oplus P_{\mathrm{driving}} \tag{6}$$

UV 位置图作为驱动信号的优势在于：它显式编码了表情引起的几何位移，且与 UV 空间天然对齐，避免了逐像素拼接 FLAME 系数带来的空间模糊问题（消融实验证实，替换为系数拼接会导致皱纹和牙齿细节严重退化，见 Figure 4(a)）。

**UNet 动态解码**：将拼接特征 $\tilde{F}_{UV}$ 输入轻量级 UNet，生成表情依赖的动态高斯属性增量 $\Delta G_{\mathrm{dyn}}$：

$$\Delta G_{\mathrm{dyn}} = \mathrm{UNet}(\tilde{F}_{UV}) \tag{7}$$

UNet 的跳跃连接结构有助于保留高频细节（如皮肤皱纹、牙齿边缘），同时其轻量设计保证了推理速度（45 FPS）。

**动态-静态融合与蒙皮**：将动态增量按区域掩码 $M_{\mathrm{dyn}}$ 与静态高斯相加，得到最终动态高斯 $G_{\mathrm{dyn}}$：

$$G_{\mathrm{dyn}} = G_{\mathrm{st}} + M_{\mathrm{dyn}} \odot \Delta G_{\mathrm{dyn}} \tag{8}$$

随后对 $G_{\mathrm{dyn}}$ 应用 FLAME 线性混合蒙皮（LBS），并通过可微 3D 高斯泼溅渲染为 2D 图像：

$$I = \mathcal{R}(\mathrm{LBS}(G_{\mathrm{dyn}}), \Theta) \tag{9}$$

其中 $\Theta$ 为目标相机参数。

---

### 3.4 数据分布调整策略

训练数据的表情分布天然不均衡：中性表情占据主导，而眼轮匝肌夸张收缩、张嘴露齿等边际表情样本稀少。FlexAvatar 采用一种**锚点表达重采样**策略：从训练集中选取 20 个锚点表情（如 Figure 10 所示），计算每个样本与锚点的 FLAME 余弦相似度，据此调整采样权重，增加边际表情的出现频率。这一策略不改变模型结构，却显著提升了稀有表情的动态纹理质量（消融实验中移除该策略导致 PSNR 下降 0.58 dB，见 Table 2）。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2512_17717/figures/014_Figure_10.jpg]]
*Figure 10: Anchor Expressions. Subset of our selected anchor expressions for training*

---

### 3.5 训练目标

总体训练损失由光度损失、感知损失、口部感知损失和正则化项加权组成：

$$\mathcal{L} = \lambda_{l1} \mathcal{L}_{l1} + \lambda_{ssim} \mathcal{L}_{ssim} + \lambda_{lpips} \mathcal{L}_{lpips} + \lambda_{mouth} \mathcal{L}_{m\text{-}lpips} + \lambda_{xyz} \mathcal{L}_{xyz} + \lambda_{scale} \mathcal{L}_{scale} \tag{13}$$

其中正则化项约束预测的高斯位置和尺度接近初始化值，防止训练过程中几何漂移：

$$\mathcal{L}_{xyz} = \|P_{\mathrm{pred}} - P_{\mathrm{init}}\|_2^2, \quad \mathcal{L}_{scale} = \|S_{\mathrm{pred}} - S_{\mathrm{init}}\|_2^2 \tag{12}$$

口部感知损失 $\mathcal{L}_{m\text{-}lpips}$ 专门针对口部区域计算 LPIPS，有效提升了牙齿的清晰度和真实感（消融实验中移除该损失导致牙齿细节模糊，见 Figure 4(c) 和 Table 2）。

---

### 3.6 可选微调模块

在保持动态 UNet 冻结的前提下，对解码器参数进行约 10 秒的快速微调，可在不损害变形质量的同时显著提升输入图像的身份一致性和个性化外观（见 Figure 4(d)）。微调损失与前馈训练一致，但仅优化解码器权重。

## 实验与分析

### 实验设置概览

FlexAvatar 在 **NeRSemble** 多视角视频数据集上进行主实验训练与评测，并在 **FaceCap** 数据集上进行消融验证。训练阶段，模型使用 NeRSemble 中 300 个身份的多视角序列，输入为 1–4 张无相机姿态、无表情标签的 RGB 图像。评测分为前馈（feed-forward）模式和微调（finetune）模式：前馈模式直接推理，微调模式冻结动态 UNet 后对解码器进行约 10 秒的个性化优化。对比方法包括 **GAGAvatar**、**LAM**、**Portrait4D-v1/v2**、**HeadGAP** 和 **Avat3R**，所有方法均使用单张输入图像进行推理或微调，并统一采用基于面部关键点的裁剪以保证公平性。

### 主实验结果：自重建任务全面领先

在 NeRSemble 自重建（Self Reenactment）基准上，FlexAvatar 的前馈模型在所有评测指标上均显著超越现有高斯类单图头像生成方法。

**Table 1** 展示了定量对比的核心结果（此处仅列最具代表性的指标，完整数据见原文 Table 1）：

- **PSNR↑**：FlexAvatar 前馈模型达到 **21.15**，较最强基线 GAGAvatar 的 19.17 提升 **+1.98**，微调后进一步提升至 **22.40**。
- **LPIPS↓**：前馈模型 **0.2193**，显著优于 GAGAvatar 的 0.2567（-0.0374），微调后降至 **0.1833**。
- **SSIM↑**：前馈模型 **0.8335**，微调后 **0.8561**。
- **CSIM↑**（身份相似度）：前馈模型 **0.8490**，微调后 **0.8701**，表明身份保持能力优异。
- **AKD↓**（平均关键点距离）：前馈模型 **3.65**，优于 GAGAvatar 的 3.87。
- **AED↓**（平均表情距离）：前馈模型 **2.05**，优于 GAGAvatar 的 2.12。

**Figure 3** 的定性对比进一步印证了数值优势：FlexAvatar 生成的动态纹理（皱纹、牙齿）在 3D 一致性和动画质量上均明显优于基线方法。特别在侧脸、张嘴等极端表情下，GAGAvatar 和 Portrait4D 常出现纹理模糊或牙齿缺失，而 FlexAvatar 保持了清晰的细节。

### 推理速度：45 FPS 实时渲染

在推理效率方面，FlexAvatar 的前馈模型达到 **45 FPS** 的实时渲染速度，远超 Avat3R 的 8 FPS（**Figure 12** 定性对比显示 FlexAvatar 在清晰度和细节真实性上也优于 Avat3R）。这一速度优势源于轻量 UNet 解码器与 UV 空间特征对齐的设计，避免了繁重的交叉注意力逐帧计算。

### 消融实验：三大关键设计验证

**Table 2** 在 FaceCap 数据集上对三个核心组件进行了定量消融，**Figure 4** 提供了对应的定性可视化。

#### 1. UV 位置图驱动信号（w/o Position Map）

移除 FLAME UV 位置图，改用 FLAME 系数逐像素拼接作为驱动信号，导致动态纹理质量严重退化。**Figure 4(a)** 显示，缺少位置图后皱纹完全消失，口腔内部结构模糊不清。定量指标上，PSNR 从完整模型的 **23.32** 下降至 **22.74**，LPIPS 从 **0.1797** 恶化至 **0.1868**。这证实了 UV 位置图提供的空间对齐信息是精细动态变形解码的关键。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2512_17717/figures/006_Figure_4.jpg]]
*Figure 4: Ablation study. Using a position map as the driving signal (a) and performing Data Distribution Adjustment (b) substantially improve the control and realism of dynamic textures, such as oral cavities and wrinkles. Adding a mouth perception loss (c) increases the granular detail of teeth, yielding more complete dental appearance. Finally, applying a finetuning stage (d) further enhances consistency with the input image for widely varying person-specific attributes (e.g., hair, clothing)*

#### 2. 数据分布调整策略（w/o Distri Adj）

移除基于 20 个锚点表达和 FLAME 余弦相似度的重采样策略后，模型在稀有表情上的表现显著下降。**Figure 4(b)** 和 **Figure 5(c)** 显示，未调整分布时眼轮匝肌夸张动作（翻白眼）和张嘴露齿等边际表情的纹理质量明显变差。定量上，PSNR 下降 **0.58**，LPIPS 上升 **0.0071**。该结果说明数据分布调整有效缓解了训练数据中常见表情过采样导致的尾部表情欠拟合问题。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2512_17717/figures/008_Figure_5.jpg]]
*Figure 5: Evaluation. (a) The model’s feed-forward test metrics show significant improvement as the training ID number increases. (b) Increasing the number of training identities led to a significant improvement in convergence speed. (c) A higher proportion of marginal expressions (eye rolling, mouth opening, frowning) is sampled after data distribution adjustment*

#### 3. 口部感知损失（w/o Mouth Loss）

移除针对口部区域的 LPIPS 感知损失后，牙齿的清晰度和完整度明显下降。**Figure 4(c)** 显示牙齿边缘模糊、齿间结构缺失。定量上，PSNR 下降 **0.41**，LPIPS 上升 **0.0047**。这表明口部区域需要额外的感知监督才能生成真实的牙齿细节。

#### 4. 微调策略（w/o Finetune）

**Figure 4(d)** 对比了前馈与微调结果：10 秒微调在保持动态变形质量的同时，显著提升了与输入图像的身份一致性和个性化外观（如发型、肤色）。定量上，微调后 PSNR 从 21.15 提升至 22.40（Table 1），LPIPS 从 0.2193 降至 0.1833。

### 训练规模与输入灵活性分析

**Figure 5(a-b)** 揭示了训练身份数量对模型性能的显著影响：随着训练 ID 数从 50 增至 300，前馈测试指标持续提升，且收敛速度明显加快。这表明 FlexAvatar 的性能受益于更大规模的 3D 数据，但当前 3D 数据集的身份多样性仍有限。

**Figure 6** 展示了输入图像数量对重建质量的影响：从单图增至 4 图时，模型能学习到更准确的形状和外观信息，PSNR 和 CSIM 均稳步提升。当前受 GPU 内存限制最多支持 4 张输入，如何进一步扩展输入视图数量是未来的开放问题。

**Figure 7** 验证了模型对输入相机姿态和表情的鲁棒性：无论输入图像的视角和表情如何变化，FlexAvatar 均能自动适应并保持良好的身份保持能力和动画质量，体现了 Transformer 交叉注意力机制对无姿态、无表情输入的泛化能力。

### 失败模式与局限性

尽管 FlexAvatar 在多数场景下表现优异，分析揭示了以下失败模式：

1. **稀有面部配件伪影**：眼镜、帽子等训练数据中代表性不足的特征会导致伪影，**Figure 11** 的后脑勺渲染也显示非面部区域的纹理有时不够真实。
2. **非头部元素缺失**：身体、衣物和极端复杂发型未被建模，限制了全身真实感。
3. **光照泛化中等**：虽然微调有所改善，但在极端光照条件下仍可能出现不一致，构建完全可重光照的头像仍是未来方向。
4. **输入视图数量受限**：当前最多 4 张输入（受 GPU 内存限制），更多视图可进一步提升重建稳定性，但需要更高效的融合机制。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2512_17717/figures/015_Figure_11.jpg]]
*Figure 11: Back head results. 360-degree rendering of our head avatars*

### 架构超参数

**Table 3** 列出了网络架构的关键超参数，包括 UV 特征图分辨率（400×400，**Figure 8**）、Transformer 层数、UNet 通道数等。这些配置在实时性（45 FPS）与重建质量之间取得了平衡。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2512_17717/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparisons on Nersemble test dataset. In feedforward evaluations, our method surpasses other Gaussian-based single-image avatar generation approaches on every tested metric. Moreover, applying a subsequent finetuning stage yields additional gains in reconstruction fidelity and perceptual quality, further improving the realism and accuracy of generated outputs*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2512_17717/figures/009_Table_2.jpg]]
*Table 2: Quantitative Ablation Study on FaceCap*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2512_17717/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparisons with baseline methods. Our single-image feed-forward and finetuned results both outperform other methods in terms of 3D consistency and animation quality, especially on details like wrinkles or teeth. Please zoom in to see the details*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2512_17717/figures/010_Figure_7.jpg]]
*Figure 7: Evaluation on the camera pose and expression of input images. Our model can automatically adapt to different input viewpoints and expressions while maintaining good ID preservation capability and animation results*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2512_17717/figures/012_Table_3.jpg]]
*Table 3: Hyperparameters of our network architecture*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2512_17717/figures/016_Figure_15.jpg]]
*Figure 15: Additional cross-reenactment results*

## 方法谱系与知识库定位

### 核心贡献与因果机制

FlexAvatar 的核心贡献在于构建了一个 **输入条件高度灵活的前馈式3D头部头像重建框架**。其因果链条可概括为：Transformer 的交叉注意力机制充当“规范化器”，将任意数量、无相机姿态、无表情标签的变长视觉token序列映射到统一的Head Query令牌空间，从而消除了传统方法对固定输入数目和已知相机/表情参数的刚性依赖；随后，UV空间的特征对齐与轻量UNet解码器利用FLAME UV位置图作为驱动信号，以45 FPS的推理速度生成表情依赖的动态高斯属性变形，在保证多视角3D一致性的同时捕捉皱纹、牙齿等精细动态纹理。

### 与基线方法的差异定位

FlexAvatar 与现有工作的关键区别体现在以下维度：

| 维度 | 典型基线方法 | FlexAvatar 改进 |
|------|------------|---------------|
| **输入条件** | 需固定数量多视图、已知相机姿态和表情标签（如 LAM、Portrait4D-v1/v2） | 支持1-4张任意姿态和表情的无标签图像，无需任何相机或表情输入 |
| **头部分表示与融合** | 显式依赖相机姿态构建表示，输入数目固定（如 GAGAvatar、HeadGAP） | Transformer自注意力融合任意数量图像特征，可学习的Head Query令牌通过交叉注意力聚合为规范UV特征图 |
| **动态变形解码** | MLP或繁重的交叉注意力驱动高斯变形，或直接FLAME驱动但细节不足（如 Avat3R） | FLAME UV位置图驱动轻量UNet解码器，生成动态高斯属性差值，实现实时高质量变形 |
| **训练数据分布** | 按原始数据分布采样，稀有表情被忽略 | 选取20个锚点表达并基于FLAME余弦相似度重采样，增加边际表情占比 |

**关键基线说明**：
- **GAGAvatar**：基于单图的前馈高斯头像方法，在NeRSemble自重建任务上PSNR为19.17，是FlexAvatar的主要对标对象。
- **Avat3R**：基于多视图的重建方法，推理速度约8 FPS，FlexAvatar以45 FPS实现了超过5倍的速度优势。
- **Portrait4D-v1/v2**、**LAM**、**HeadGAP**：均需要已知相机姿态或固定输入数目，FlexAvatar在输入灵活性上形成代际差异。

### 适用边界与局限

FlexAvatar 的设计假设和当前实现决定了其适用边界：

1. **罕见面部特征的处理能力有限**：训练数据中眼镜、帽子等配件的代表性不足，导致这些特征上可能出现伪影。该局限源于3D头部数据集的固有分布偏差，而非方法设计缺陷。

2. **非头部元素未建模**：身体、衣物、极端复杂发型等未被纳入建模范围，限制了全身真实感。这是当前3D头部头像重建领域的共性边界。

3. **光照泛化能力中等**：虽然10秒微调策略可在一定程度上改善输入图像的身份一致性和外观匹配，但框架未显式建模光照模型，无法实现完全可重光照的头像。这限制了在任意光照环境下的真实感渲染。

4. **输入视图数量受限于GPU内存**：当前最多支持4张输入图像，虽然实验表明增加输入视图可提升重建稳定性（Figure 6），但内存瓶颈限制了进一步扩展。

5. **模型性能持续受益于数据规模**：实验证实训练身份数量增加可显著提升前馈测试指标和收敛速度（Figure 5(a)(b)），但当前3D数据集的身份多样性仍然有限，暗示模型尚未达到性能饱和点。

### 开放问题与未来方向

基于上述局限，FlexAvatar 框架指出了以下值得探索的方向：

1. **稀有配件的鲁棒重建**：如何有效处理眼镜、帽子等训练数据中代表性不足的面部特征？可能的路径包括数据增强策略或引入配件感知的模块化表示。

2. **建模范围扩展**：如何在保持实时性能（45 FPS）的前提下，将建模范围从头部扩展到身体、衣物和复杂发型？这需要在表示能力和计算效率之间寻找新的平衡点。

3. **显式光照建模**：如何将光照模型显式融入框架，实现完全可重光照的可动画头像？这是从“外观重建”迈向“物理真实感渲染”的关键一步。

4. **大规模2D数据利用**：如何设计两阶段训练框架，充分利用大规模2D图像数据来弥补3D数据在身份多样性和稀有特征覆盖上的不足？当前3D数据集的身份多样性有限，2D数据的引入可能是突破性能瓶颈的有效手段。

5. **输入视图数量的扩展**：如何在有限GPU内存下支持更多输入视图，以进一步提升重建稳定性？这可能需要设计更高效的注意力机制或特征压缩策略。

6. **跨身份重演的一致性**：虽然FlexAvatar在自重建任务上表现优异，但跨身份重演（cross-reenactment）场景下的身份保持和表情迁移质量仍需进一步验证和提升（论文在Figure 15-16中展示了初步结果，但缺乏定量评估）。

## 原文 PDF

![[paperPDFs/CVPR_2026/FlexAvatar_Flexible_Large_Reconstruction_Model_for_Animatable_Gaussian_Head_Avatars_with_Detailed_Deformation.pdf]]