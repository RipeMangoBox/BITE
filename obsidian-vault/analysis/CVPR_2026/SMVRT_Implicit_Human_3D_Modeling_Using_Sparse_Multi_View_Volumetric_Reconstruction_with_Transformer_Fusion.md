---
title: "SMVRT: Implicit Human 3D Modeling Using Sparse Multi-View Volumetric Reconstruction with Transformer Fusion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SMVRT_Implicit_Human_3D_Modeling_Using_Sparse_Multi_View_Volumetric_Reconstruction_with_Transformer_Fusion.pdf
project_link: null
code_link: null
aliases:
- SMVRT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过三阶段注意力引导的特征融合（AFM：全局-局部交替增强2D特征；MMFT：在体积网格中心选择性聚合多视角多层级特征；QFT：在查询点融合3D体积特征与保留细节的低层2D特征），实现视图间信息的自适应整合与细节保留。
primary_logic: 在稀疏多视图人体重建中，预先在共享3D体积中心（而非每个查询点）进行视图感知的特征选择与融合，并结合查询点处的2D-3D交叉注意力，能够在避免计算冗余的同时，稳健地聚合多视角信息并保留表面精细结构。
claims:
- 融合模块消融（Table 4）：完整模型（MMFT+QFT+AFM）在所有指标上显著优于移除所有融合模块的基线（No fusion）以及仅加入单个模块的变体，验证了三阶段融合的必要性。
- 与基线方法对比（Table 1/Figure 3）：SMVRT在THUman2.1数据集上的法向一致性（NC）达0.940，明显高于Zins et al.的0.900和MV-PIFu的0.844，且定性结果展示了对手指、衣物褶皱等细节的更好保留。
- 细节保持模块消融（Table 7）：在QFT中引入低层2D特征（detail preserver）使NC从0.937提升至0.940，IOU从0.950升至0.958，表明2D细节对高质量重建的关键作用。
- THUman2.1 上 Normal Consistency (NC) = 0.940
---

# SMVRT: Implicit Human 3D Modeling Using Sparse Multi-View Volumetric Reconstruction with Transformer Fusion

> [!tip] 核心洞察
> 在稀疏多视图人体重建中，预先在共享3D体积中心（而非每个查询点）进行视图感知的特征选择与融合，并结合查询点处的2D-3D交叉注意力，能够在避免计算冗余的同时，稳健地聚合多视角信息并保留表面精细结构。

| 字段 | 内容 |
|------|------|
| 中文题名 | SMVRT：基于稀疏多视角体积重建与Transformer融合的隐式人体三维建模 |
| 英文题名 | SMVRT: Implicit Human 3D Modeling Using Sparse Multi-View Volumetric Reconstruction with Transformer Fusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Fan_SMVRT_Implicit_Human_3D_Modeling_Using_Sparse_Multi-View_Volumetric_Reconstruction_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | SMVRT |
| Dataset | THUman2.1 |

> [!tip] 效果简介
> - THUman2.1 上，Normal Consistency (NC) 0.940 vs 0.900 (Zins et al.) (+0.040)；Normal Consistency (NC) 0.940 vs 0.844 (MV-PIFu) (+0.096)。

## 概述

**核心问题**：从稀疏多视角图像（如4个环绕相机）重建高保真三维人体，面临两大瓶颈：一是不同视角间存在严重的自遮挡，导致局部区域（如腋下、手部）重建不完整；二是传统方法在融合多视图特征时，难以自适应地区分可见视角与遮挡视角的贡献，简单拼接或平均池化会引入噪声、丢失细节。

**核心思路**：SMVRT提出一种端到端的隐式三维重建框架，其关键创新在于**三阶段注意力引导的特征融合机制**——在2D特征层面通过交替全局-局部注意力（AFM）增强跨视图一致性；在3D体积构建阶段，将多视图特征投影到共享的体积网格中心，利用几何感知的Transformer（MMFT）进行视图选择性的特征聚合；在查询点解码阶段，通过交叉注意力（QFT）融合3D体积特征与保留细节的低层2D特征。这一设计使得模型能够**在计算冗余可控的前提下，稳健地整合多视角信息并保留表面精细结构**。

**方法定位**：与逐查询点融合的基线方法（如**Zins et al.**, 3DV 2021）和基于拼接的隐式重建方法（如**MV-PIFu**, Saito et al., ICCV 2019）不同，SMVRT将首次融合操作前置于体积网格中心，仅在最终解码时引入查询点级别的2D-3D交叉注意力，从而在效率与精度之间取得平衡。

**主要结果**：在THUman2.1数据集上，SMVRT的法向一致性（NC）达到**0.940**，显著优于Zins et al.的0.900和MV-PIFu的0.844；在THUman2.0数据集上，倒角距离（CD）指标相比现有方法提升约**2倍**。定性结果显示，SMVRT对手指、衣物褶皱等精细结构的重建质量明显优于基线方法（Figure 3）。消融实验证实，三阶段融合模块的完整组合是性能提升的关键，移除任一模块均导致指标显著下降（Table 4）。

## 背景与动机

从稀疏多视角图像重建高保真三维人体模型是计算机视觉与图形学中长期存在的挑战性课题。该任务在虚拟现实、增强现实、数字人建模、影视特效等应用中具有广泛需求，但其核心难点在于：当输入视图数量有限（例如2至8个环绕相机）时，如何从离散、可能存在遮挡的二维观测中，稳健地推断出完整且细节丰富的三维几何表面。

传统方法主要依赖参数化模板（如SMPL/SMPLX）进行人体姿态与形状拟合，此类方法在身体主干区域表现较好，但对衣物褶皱、手指姿态、面部细节等偏离模板的几何结构往往难以准确恢复。另一类基于隐式函数的方法（如Pixel-Aligned Implicit Function）尝试直接从图像特征预测三维占据场，避免了模板依赖，但其在多视图场景下的特征融合策略仍存在明显局限。

现有融合策略的不足可归纳为两个层面。其一，**特征聚合的粗糙性**：早期工作如**MV-PIFu**（Saito et al., ICCV 2019）采用简单的多视图特征拼接或平均池化，无法区分不同视图对特定空间点的可见性与信息贡献，导致遮挡区域的重建质量严重退化。其二，**融合位置的次优性**：近期方法如**Zins et al.**（3DV 2021）引入局部注意力机制在查询点处进行特征融合，但逐查询点独立计算注意力带来了较高的计算开销，且缺乏对多视图间全局关系的显式建模。图2对比了不同融合策略的差异：3DFG采用顺序拼接，Zins et al.在查询点处局部融合，而本文提出的SMVRT则在体积网格中心进行视图感知的特征选择，再于查询点处融合细节特征。

上述缺陷共同指向一个核心瓶颈：**稀疏多视角输入下，传统方法难以有效融合跨视角特征，导致遮挡区域重建不完整、细节丢失，且简单特征聚合无法区分可见与遮挡视角的贡献**。这构成了本文的研究动机——设计一种端到端的隐式三维重建框架，通过多阶段的Transformer引导特征融合，实现视图间信息的自适应整合与表面精细结构的保留。

## 核心创新

SMVRT 的核心创新在于针对**稀疏多视图人体重建中跨视角特征融合不充分**这一瓶颈，设计了一套三阶段注意力引导的特征融合机制。与现有方法在查询点处进行简单拼接或局部注意力融合不同，SMVRT 将融合操作前置到共享的 3D 体积网格中心，并在不同层级施加差异化融合策略，从而在避免计算冗余的同时，稳健地聚合多视角信息并保留表面精细结构。

### 改变的关键技术槽位

#### 槽位一：2D 特征融合方式 — 交替全局-局部融合模块（AFM）

**基线做法**：现有方法（如 MV-PIFu、Zins et al.）在 2D 特征提取阶段无显式的多视图特征融合，或仅采用简单的拼接操作，各视图特征独立处理，缺乏跨视图的上下文交互。

**SMVRT 改进**：引入 **AFM（Alternating Fusion Module）**，对 ResNet 末级特征进行分块标记化（Tokenization）后，交替应用跨视图全局注意力块与逐帧局部注意力块（见 Eq.2）。全局注意力使各视图特征在共享令牌空间中相互感知，局部注意力则保留单帧内的空间结构。这种“全局-局部交替”的设计，使 2D 特征在进入 3D 融合前已具备更强的视图间判别力。

**证据支撑**：消融实验（Table 4）表明，在“No fusion”基线上单独加入 AFM 即可带来显著的性能提升；完整模型（MMFT+QFT+AFM）相比移除 AFM 的变体在所有指标上均有明显优势。

#### 槽位二：多视图特征聚合为 3D 体积的策略 — 多视图多层级特征融合 Transformer（MMFT）

**基线做法**：传统方法（如 3DFG 的拼接融合、Zins et al. 的查询点局部注意力）在**每个查询点**处逐点聚合多视图特征。这种方式计算量大，且缺乏对视图可见性的全局判断，在遮挡区域容易引入噪声。

**SMVRT 改进**：提出 **MMFT（Multi-view Multi-level Feature Fusion Transformer）**，将融合操作前置到**共享 3D 体积网格中心**。具体而言，将多视图多层级 2D 特征通过透视投影（Eq.3）映射到体积网格中心，利用几何感知的 Transformer（Eq.4）在网格中心处选择最相关视图的特征进行融合，再经 3D U-Net 正则化形成特征体积（Figure 2(c-d)）。这一设计的关键洞察在于：网格中心是视图间几何一致性的天然锚点，在此处进行视图选择与融合，既能有效区分可见与遮挡视角，又避免了逐查询点计算的冗余。

**证据支撑**：融合策略对比图（Figure 2）清晰展示了 SMVRT 与 3DFG、Zins et al. 在融合位置与机制上的本质差异。Table 4 消融显示，MMFT 模块的加入使模型相较“No fusion”基线有大幅提升。

#### 槽位三：查询点特征解码的组成 — 查询点融合 Transformer（QFT）与细节保持

**基线做法**：查询点解码时仅使用 3D 体积特征或单一视图特征，缺乏对多视图低层细节信息的显式利用，导致重建表面过于平滑，丢失手指、衣物褶皱等精细结构。

**SMVRT 改进**：设计 **QFT（Query Point Fusion Transformer）**，在查询点处将三线性插值的多级 3D 体积特征与各视图投影的**低层 2D 特征**串联后，通过注意力融合（Eq.6）。低层 2D 特征作为“细节保持器”（detail preserver），为解码器提供高频几何线索，使重建表面在保持全局一致性的同时，能够恢复精细的局部结构。

**证据支撑**：细节保持模块消融（Table 7）是最具说服力的证据——在 QFT 中引入低层 2D 特征后，法向一致性（NC）从 0.937 提升至 0.940，IoU 从 0.950 升至 0.958。定性对比（Figure 7）也显示，无细节保持器的重建表面过于平滑，缺失了衣物褶皱等细节。

## 整体框架

SMVRT 是一个端到端的稀疏多视角人体隐式三维重建框架，其核心设计目标是在仅给定少量（2–8 个）环绕相机拍摄的 RGB 图像及相机标定的条件下，重建出高保真的人体几何表面。整个 pipeline 由五个关键模块级联构成：**多模态输入处理与 ResNet 编码器**、**交替全局-局部融合模块（AFM）**、**多视图多层级特征融合 Transformer（MMFT）**、**查询点融合 Transformer（QFT）** 以及 **隐式场解码器（MLP）**。图 1 给出了完整的架构示意。

### 输入流与多模态编码

对于给定的 $N$ 张多视角 RGB 图像 $\bar{I_i} \in \mathbb{R}^{H \times W \times 3}$，系统首先利用预训练的 Sapiens 模型从每张彩色图像中估计出法向图 $N_i$ 和深度图 $D_i$，同时根据相机内外参为每个像素计算 Plücker 射线图 $P_i$，以显式编码视角几何信息。这四种模态（RGB、法向、深度、Plücker 射线）在通道维度拼接后，送入一个修改了首层卷积的 ResNet 编码器，提取多层级 2D 特征图。其中，末级特征图经过分块标记化（tokenization），被投影为维度为 $d$ 的令牌序列，用于后续的注意力融合。

### 三阶段注意力引导的特征融合

SMVRT 的方法论核心在于**三阶段、由粗到细的注意力融合机制**，旨在解决稀疏多视角重建中两个根本性难题：如何从有限且可能相互遮挡的视图中稳健地聚合信息，以及如何在聚合过程中保留对表面细节至关重要的低层纹理线索。

**第一阶段——AFM（交替全局-局部融合模块）** 作用于 2D 特征层面。它将所有视图的令牌序列打包，交替应用跨视图的全局注意力块和逐帧的局部注意力块，使每个视图的特征既能感知其他视图的互补信息，又能保持自身的局部判别力。这一设计避免了简单拼接或平均池化无法区分可见与遮挡视角贡献的缺陷。

**第二阶段——MMFT（多视图多层级特征融合 Transformer）** 在共享的 3D 体积网格中心进行视图感知的特征选择与聚合。具体而言，每个体积网格中心点通过透视投影映射到各视图的特征图上，采样得到多级 2D 特征，并与深度值拼接后送入几何感知的 Transformer。MMFT 的核心作用是从多个候选视图中**自适应地选择最相关的视图特征**，从而在遮挡区域也能形成稳健的 3D 特征表达。融合后的特征经平均池化形成网格中心的特征向量，再通过 3D U-Net 进行空间正则化，生成多级 3D 特征体积。

**第三阶段——QFT（查询点融合 Transformer）** 在最终的表面查询点处，将三线性插值得到的 3D 体积特征与从各视图投影来的低层 2D 细节特征串联，通过交叉注意力融合，显式地**将 3D 几何先验与 2D 纹理细节对齐**。这一设计的关键在于：低层 2D 特征保留了 ResNet 早期层的高频信息，能够有效补偿 3D 体积在网格化过程中丢失的表面细节。

### 输出流与训练目标

QFT 输出的增强嵌入经平均池化后，与查询点的三维坐标拼接，送入一个轻量 MLP 解码器，预测该点的占据值 $O$。整个网络以二元交叉熵损失（BCE Loss）进行端到端训练，监督信号来自采样点上的占据真值。

### 与基线方法的结构性差异

图 2 将 SMVRT 的融合策略与两类代表性基线进行了对比。**MV-PIFu**（Saito et al., ICCV 2019）采用像素对齐隐式函数，但在多视图融合时仅使用简单的拼接操作，缺乏视图间的显式交互。**Zins et al.**（3DV 2021）在查询点处进行局部注意力融合，虽引入了一定的视图选择能力，但每次查询都需重新计算注意力，计算冗余度高，且难以在遮挡区域形成全局一致的 3D 理解。SMVRT 的关键改进在于：将**首次融合（MMFT）提前到共享的体积网格中心**，以较低的计算代价完成视图选择与 3D 特征构建；随后在查询点处仅进行轻量的 2D-3D 交叉注意力（QFT），在保留细节的同时避免了逐点全量重计算。这一“先体积聚合、后查询精修”的级联策略，是 SMVRT 在稀疏视角下取得显著性能提升的因果枢纽。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_SMVRT_Implicit_Hum/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the SMVRT architecture. Given RGB images, a pretrained Sapiens model [20](not shown) generates normal and depth maps. Camera calibrations are used to compute Plucker [ ¨ 39] rays. The four inputs represent RGB, depth(D), normal(N), Plucker ¨ rays(P), from left to right. These multi-modal inputs are stacked and fed to a ResNet[15] encoder to extract multi-level 2D features. The final-level pixel features are tokenized and passed through an Alternating Fusion Module (AFM) with additional register tokens [10], utilizing either Transformer [40] or Mamba [14] blocks to produce globally regularized features. For 3D volume construction, we bilinearly sample 2D features at each grid cen...*

## 核心模块与公式推导

SMVRT 的核心创新在于三阶段注意力引导的特征融合机制，分别作用于 2D 特征增强、3D 体积构建和查询点解码三个层级，逐步解决稀疏多视图人体重建中跨视角信息整合与细节保留的难题。

### 多模态输入与特征提取

网络的输入包含 N 个视点的 RGB 图像 $\bar{I_i} \in \mathbb{R}^{H \times W \times 3}$ 及其对应的相机内外参矩阵。为增强空间感知能力，系统为每个视点计算 Plücker 射线 $P_i$，将相机位姿信息编码为与图像同尺寸的张量。同时，利用预训练的 Sapiens 模型从 RGB 图像中估计深度图 $D_i$ 和法向图 $N_i$。四种模态（RGB、深度、法向、Plücker 射线）沿通道维度拼接后，送入修改了首层卷积的 ResNet 编码器，提取多层级 2D 特征。末级特征图被划分为 $HW/s^2$ 个块，经线性投影生成维度为 $d$ 的令牌序列：

$$T_{i,j} = \text{Tokenize}(\text{ResNet}(I_i \oplus D_i \oplus N_i \oplus P_i)), \quad j = 1..HW/s^2$$

### AFM：交替全局-局部融合模块

AFM 的目的是在 2D 特征层面实现跨视图的信息交互与各视图自身的特征增强。其核心设计是交替使用全局注意力块和局部注意力块。在全局注意力阶段，所有视图的令牌被打包为联合序列，通过 Transformer 或 Mamba 块进行跨视图注意力计算；在局部注意力阶段，各视图令牌独立地通过逐帧注意力块进行增强。该交替过程可形式化表示为：

$$\begin{aligned}
T^{l-1} &= \text{Pack}: T_0^{l-1} \oplus T_1^{l-1} ... \oplus T_N^{l-1} \\
T^l &= \text{Attn}_{\text{AFM}}^{\text{global},l}(T^{l-1}) \\
T^l &= \text{Unpack}: T_0^l, T_1^l, ..., T_N^l \\
T^{l+1} &= \text{Attn}_{\text{AFM}}^{\text{frame},l+1}(T^l), \quad l = 1,2,...,M
\end{aligned}$$

此设计使网络既能捕获全局一致的跨视图对应关系，又能保留各视图独有的局部细节，为后续的 3D 融合提供更具判别力的特征。

### MMFT：多视图多层级特征融合 Transformer

MMFT 是 SMVRT 区别于以往方法的关键模块。传统方法（如 3DFG、Zins et al.）通常在查询点处逐点进行特征聚合，计算开销大且难以显式建模视图可见性。SMVRT 的策略是：先在共享的 3D 体积网格中心进行视图感知的特征选择与融合，再通过 3D U-Net 正则化形成特征体积。

具体而言，对于 3D 空间中的每个网格中心点 $C(x,y,z)$，通过透视投影将其映射到各视点的图像平面：

$$p_{i,u,v} = \pi_i(T_i \circ C(x,y,z))$$

其中 $T_i$ 为相机外参，$\pi_i$ 为内参投影函数。在投影位置处双线性采样多层级 2D 特征，并与深度值 $z_i$ 拼接后，送入几何感知的 Transformer 进行注意力融合：

$$G(F_i^{2D}) = \text{Attn}_{\text{MMFT}}[F_1^{2D}, z_1, ..., F_N^{2D}, z_N]$$

注意力机制使网络能够根据深度一致性和特征相似性，自动选择最相关视点的特征，抑制被遮挡或偏离过大的视图贡献。融合后的各视图特征经平均池化得到网格中心的最终特征向量：

$$F_{\text{fused}} = \text{Average}(G_1, ..., G_N)$$

所有网格中心的特征构成初始特征体积，随后由 3D U-Net 进行多阶段正则化，输出多级 3D 特征体积。

### QFT：查询点融合 Transformer

在查询点 $q$ 处，QFT 负责将 3D 体积特征与保留细节的低层 2D 特征进行最终融合。对于每个视点，将三线性插值得到的 3D 特征 $F_v$ 与投影采样的低层 2D 特征 $F_{i,0}^{2D}$ 及深度 $Z_i$ 串联，形成多组查询向量，通过注意力机制进行融合：

$$F(q) = \text{Attn}_{\text{QFT}}\left[\left(F_v, F_{1,0}^{2D}, Z_1\right), ..., \left(F_v, F_{N,0}^{2D}, Z_N\right)\right]$$

低层 2D 特征的引入是细节保留的关键——高层特征虽语义丰富但空间分辨率低，低层特征则保留了精细的纹理和边缘信息。融合后的特征经平均池化，与查询点坐标拼接，输入 MLP 解码器预测占据值：

$$O = f(\text{Average}(F(q)), x_q, y_q, z_q)$$

### 损失函数

网络采用二元交叉熵损失进行端到端训练：

$$\text{Loss} = -\frac{1}{BN}\sum_{i=1}^{B}\sum_{k=1}^{N}\text{BCE}(O_{\text{pred},i,k}, O_{\text{gt},i,k})$$

其中 $B$ 为批量大小，$N$ 为每个样本的查询点数量，$O_{\text{pred}}$ 和 $O_{\text{gt}}$ 分别为预测和真实的占据值。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_SMVRT_Implicit_Hum/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of fusion strategies. (a) 3DFG [4] iteratively transforms query grids into camera spaces and fuse features sequentially by concatenation. (b) Zins et al. [50] perform local feature fusion at each query point by transformer. (c) In our SMVRT design, the first fusion MMFT occurs at grid centers to selectively choose the most relevant views, followed by QFT fusion at query points for fusing detail-preserving low-level features. (d) Our MMFT module first warps multi-view 2D features onto grid centers, where transformers are used to select the most related cameras. QFT is applied at query point to performing attentional fusion of 2D and 3D features*

## 实验与分析

### 核心性能对比

SMVRT在THUman2.1数据集上与两个无模板多视图基线方法进行了定量对比（Table 1）。在4相机环绕输入设置下，SMVRT的法向一致性（NC）达到**0.940**，显著优于**Zins et al.**（3DV 2021）的0.900和**MV-PIFu**（Saito et al., ICCV 2019）的0.844，分别提升了+0.040和+0.096。这一差距源于SMVRT三阶段注意力融合机制对多视角信息的有效整合：传统方法在查询点处采用拼接或局部注意力聚合特征，无法区分可见与遮挡视角的贡献，而SMVRT先在共享3D体积网格中心进行视图感知的特征选择（MMFT），再在查询点融合3D-2D细节（QFT），从而在遮挡区域和表面细节上获得更完整的重建。

定性结果（Figure 3）进一步验证了这一优势：在面部、手指和衣物褶皱等细节区域，MV-PIFu和Zins et al.的重建表面出现模糊或缺失，而SMVRT能够清晰保留手指间隙和衣物褶皱的精细几何结构。

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_SMVRT_Implicit_Hum/figures/005_Figure_3.jpg]]
*Figure 3: Comparison between our method and baselines: MV-PIFu [36], Zins et al. [50]. All methods take inputs from 4 cameras. ’Zoom-in’ shows the reconstruction details of faces, fingers, clothes creases. Please zoom in for better visibility. Additional results are provided in the supplementary material. Throughout this paper, the mesh colors denote surface normals unless otherwise specified*

在THUman2.0和MultiHuman数据集上（Table 2），SMVRT同样展现出竞争力，Chamfer Distance指标相较现有方法有约2倍的提升。需要指出的是，Table 2中部分对比方法使用了SMPL/SMPLX模板先验（标注为“S”），而SMVRT作为无模板方法仍取得更优性能，验证了其纯数据驱动融合策略的泛化能力。

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_SMVRT_Implicit_Hum/figures/010_Table_2.jpg]]
*Table 2: Comparison on the THUman2.0 [46] and MultiHuman [46], ’S’ represents SMPL/SMPLX [26, 32] template, ’H’ represents high resolution. The metrics are Chamfer Distance l2 ↓ (×10−5) and Point-to-Surface (P2S ↓) distance l2 (×10−5)*

### 融合模块消融分析

为验证三阶段注意力融合的必要性，Table 4展示了逐步开启各融合模块的性能变化。基线模型“No fusion”移除了AFM并将MMFT和QFT替换为平均池化，其性能在所有指标上均为最低。单独加入MMFT、QFT或AFM均带来提升，但完整模型（MMFT+QFT+AFM）在THUman2.1上达到CD l1 **3.58**、IOU **0.958**、NC **0.940**、F1.0 **0.973**，显著优于所有部分配置。

这一消融揭示了三个模块的互补性：
- **MMFT**在体积中心进行几何感知的视图选择，解决了遮挡视角的干扰；
- **QFT**在查询点融合3D体积特征与低层2D细节，保留了表面精细结构；
- **AFM**在2D特征层面进行跨视图全局与逐帧局部交替增强，提升了各视图特征的判别力。

定性消融（Figure 5）显示，“No fusion”模型重建表面粗糙、细节丢失严重，而逐步加入融合模块后，表面光滑度和细节保真度依次改善。

### 细节保持机制验证

QFT模块中低层2D特征的细节保持作用是SMVRT设计的关键环节。Table 7的消融表明，在QFT中引入低层2D特征（detail preserver）后，NC从0.937提升至0.940，IOU从0.950提升至0.958，CD l1从3.78降至3.58。定性对比（Figure 7）显示，无细节保持的变体重建表面过于平滑，丢失了衣物褶皱和面部细节；而完整QFT能有效保留这些高频几何信息。

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_SMVRT_Implicit_Hum/figures/018_Figure_7.jpg]]
*Figure 7: Visual results with and without detail preserver (dp.) corresponding to*

这一结果证实了核心洞见：3D体积特征经过下采样和正则化后不可避免地损失高频细节，而直接从2D特征图投影的低层特征保留了原始图像的精细结构，通过QFT的注意力融合机制可以将这些细节注入最终的重建表面。

### 输入模态与相机数量影响

输入模态消融（Table 5/Figure 6）表明，完整模态组合（RGB+法向+深度+Plücker射线）获得最佳性能，其中法向图贡献最大。Plücker射线编码了相机几何信息，为网络提供了显式的空间位置先验，有助于跨视图特征对齐。

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_SMVRT_Implicit_Hum/figures/015_Table_5.jpg]]
*Table 5: Qualitative results of ablation studies on different inputs: RGB: color image; N: normals predicted by Sapiens [20]; D: depth predicted by Sapiens [20]; P: Plucker ray map. ¨*

相机数量消融（Table 3/Figure 4）显示，从2相机增加到4相机带来显著提升，继续增加到8相机仍有增益（CD l1降至2.96），但边际收益递减。值得注意的是，即使在仅2相机的极端稀疏设置下，SMVRT仍能重建出合理的人体形状，体现了MMFT模块在少视图条件下的鲁棒视图选择能力。

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_SMVRT_Implicit_Hum/figures/013_Table_3.jpg]]
*Table 3: Ablation studies on the number of cameras using the full model, ”hds” denotes the image resolution of 1024*

### AFM骨干网络选择

Table 6对比了AFM模块中使用标准Transformer与Mamba的实现。两者精度基本持平，但Mamba变体的训练与推理速度提升约**1.5倍**，为实际部署提供了更高效的替代方案。这一结果表明AFM的交替融合框架对具体注意力实现不敏感，核心收益来自全局-局部交替增强的结构设计。

### 零样本泛化能力

在MultiGarment数据集上的零样本测试（Figure 8/Table 8）验证了SMVRT的泛化性能。使用THUman2.1预训练模型直接推理，SMVRT在未见过的服装类型和人体姿态上仍能保持合理的重建质量，表明三阶段融合策略学习到的是通用的多视图几何推理能力，而非对特定数据分布的过拟合。

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_SMVRT_Implicit_Hum/figures/020_Table_8.jpg]]
*Table 8: Qualitative zero-shot performance on MultiGarment dataset using pretrained full model with 4 cameras*

### 公平性说明

所有基线方法均基于开源实现从头训练，使用相同的数据集划分（0.75:0.05:0.20）和评估指标（IoU、Chamfer Distance、Normal Consistency、F-score），渲染图像使用相同的4个环绕相机设置，确保对比结果的公平性。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_SMVRT_Implicit_Hum/figures/014_Table_4.jpg]]
*Table 4: Ablation studies on fusion modules. ”No fusion” represents model by removing AFM and replace MMFT and QFT with average pooling. ”MMFT” indicates adding only MMFT module on ”No fusion” module, ”QFT” means adding only QFT on ”No fusion”, and ”AFM” means adding AFM only. ”MMFT+ QFT” means enabling MMFT and QFT. ”MMFT+QFT+AFM” means the full model with all fusion modules enabled*

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_SMVRT_Implicit_Hum/figures/019_Table_7.jpg]]
*Table 7: Ablation study of QFT with and without low-level 2D features. With 2D features, we obtain consistently better metrics*

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_SMVRT_Implicit_Hum/figures/017_Table_6.jpg]]
*Table 6: Ablation study on AFM module. We compare the standard transformer and Mamba [14] blocks*

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_SMVRT_Implicit_Hum/figures/004_Figure.jpg]]

## 方法谱系与知识库定位

### 1. 基线对比与差异化分析

SMVRT 的核心定位是**稀疏多视角下的无模板隐式人体重建**，其方法设计直接回应了两类代表性基线的瓶颈：

**与像素对齐隐式方法的对比。** **MV-PIFu**（Saito et al., ICCV 2019）是无模板多视图重建的早期代表，其融合策略为多视图特征拼接后输入像素对齐隐函数。这一策略在稀疏视角下存在明显局限：简单拼接无法区分不同视图的可见性贡献，遮挡区域的特征会直接污染查询点解码。定量结果印证了这一判断——在 THUman2.1 数据集上，SMVRT 的法向一致性（NC）达到 0.940，MV-PIFu 仅为 0.844（Table 1），差距达 0.096。定性对比中（Figure 3），MV-PIFu 在手指、衣物褶皱等细节区域出现明显的几何模糊和缺失，而 SMVRT 保留了更精细的表面结构。

**与局部注意力融合方法的对比。** **Zins et al.**（3DV 2021）在每个查询点处使用 Transformer 进行局部注意力融合，是更近期的基线。这一设计相比拼接有所改进，但存在两个结构性弱点：（1）在查询点处逐点执行注意力计算，计算冗余大且缺乏全局视图选择机制；（2）融合仅依赖查询点投影的局部特征，难以利用跨视图的上下文信息。SMVRT 通过将首次融合（MMFT）前置到共享的 3D 体积网格中心，在网格中心处完成视图感知的特征选择，再通过 3D U-Net 正则化传播邻域信息，有效规避了逐点注意力的冗余。在 THUman2.1 上，SMVRT 的 NC（0.940）显著优于 Zins et al. 的 0.900（Table 1），验证了体积中心融合策略的优势。

**与模板驱动方法的对比。** Table 2 报告了在 THUman2.0 和 MultiHuman 数据集上与模板驱动方法（标记为“S”，表示使用 SMPL/SMPLX 模板）的对比。SMVRT 作为无模板方法，在 Chamfer Distance 和 Point-to-Surface 距离上实现了约 2 倍的提升。这表明在稀疏多视角条件下，精心设计的注意力融合机制可以弥补甚至超越模板先验带来的约束优势，同时避免了模板对宽松衣物的拟合偏差。

**融合策略的结构性差异。** Figure 2 清晰展示了三类融合范式的区别：3DFG 在相机空间迭代变换查询网格并顺序拼接特征；Zins et al. 在查询点处进行局部 Transformer 融合；SMVRT 采用两阶段融合——先在网格中心通过 MMFT 进行视图选择，再在查询点通过 QFT 融合 2D-3D 特征。这一“先全局选择、后局部精化”的设计是方法的核心创新。

### 2. 适用边界与局限

**视角数量的敏感性。** Table 3 的相机数量消融显示，完整模型在 2 相机输入时性能显著下降（CD l1 从 3.58 升至更高），4 相机为推荐的实用配置，8 相机获得最佳性能。这表明 SMVRT 的融合机制在极度稀疏（≤2 视角）条件下仍面临信息不足的挑战，其视图选择策略需要至少 3-4 个视角才能有效区分可见与遮挡区域。

**对法向模态的依赖。** Table 5 的输入模态消融表明，法向图对整体精度的贡献最大。这暗示 SMVRT 的性能部分依赖于预训练 Sapiens 模型生成的法向质量——在法向估计失效的场景（如极端光照、非朗伯表面），重建精度可能退化。该依赖关系需要在实际部署中加以注意。

**零样本泛化的边界。** Figure 8 和 Table 8 展示了在 MultiGarment 数据集上的零样本泛化结果。虽然论文声称取得了有竞争力的性能，但定量指标相对于域内测试有所下降。这表明 SMVRT 的融合模块在训练数据分布外仍能工作，但对衣物拓扑和姿态的极端变化可能不够鲁棒——这一点需要手动验证具体退化模式。

**计算开销的隐式代价。** 论文未直接报告推理延迟或显存占用的对比数据。MMFT 在体积网格中心执行注意力、QFT 在查询点执行注意力、AFM 在 2D 特征层面交替全局-局部注意力，三阶段融合的设计在精度上获益，但计算代价高于简单的平均池化或拼接融合。Table 6 显示用 Mamba 替换 AFM 中的 Transformer 可将训练与推理速度提升约 1.5 倍且精度基本持平，这为效率优化提供了可行路径。

### 3. 开放问题与后续方向

**体积中心融合的普适性。** MMFT 在网格中心而非查询点处进行首次融合是本方法的关键设计选择。这一策略是否适用于其他稀疏多视图重建任务（如通用物体、场景级重建）尚待验证。网格中心的分辨率与注意力计算量的权衡也需要更系统的分析。

**多模态贡献的动态加权。** 当前方法将 RGB、深度、法向、Plücker 射线等模态在输入端简单拼接，融合模块隐式学习模态间的权重。在部分模态失效（如深度传感器噪声）时，模型是否能够自适应调整依赖尚不清楚。引入显式的模态不确定性建模可能是改进方向。

**与基于 3D Gaussian Splatting 等新兴表征的关系。** 论文发表于隐式场方法活跃的时期，未涉及与 3D Gaussian Splatting 等显式表征方法的对比。SMVRT 的体积中心融合思想——在共享 3D 空间中聚合多视图信息——与 Gaussian 方法中的 3D 原语优化存在概念上的呼应，但两者的融合机制和适用场景有本质差异，值得后续工作探索。

**更稀疏视角下的极限性能。** 当前实验最低配置为 2 相机，更极端的情况（单目或宽基线双目）下，SMVRT 的融合机制是否仍有效、是否需要引入时序信息或人体先验，是开放的研究问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/SMVRT_Implicit_Human_3D_Modeling_Using_Sparse_Multi_View_Volumetric_Reconstruction_with_Transformer_Fusion.pdf]]