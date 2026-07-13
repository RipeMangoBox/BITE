---
title: "Dens3R: A Foundation Model for 3D Geometry Prediction"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Dens3R_A_Foundation_Model_for_3D_Geometry_Prediction.pdf
project_link: https://g-1nonly.github.io/Dens3R/
code_link: null
openreview_forum_id: kxVjQhkAWz
aliases:
- Dens3R
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将表面法线作为内在不变性先验融入点图表示，并采用两阶段训练策略。"
primary_logic: "法线具有内在不变性（一对一映射），可减少多视角歧义并简化学习；结合共享编解码器和位置插值RoPE，实现高效高分辨率的多任务统一预测。"
claims:
- "引入法线信息可显著提高点图精度"
- "内在不变训练结合法线预测头可产生更准确、更稳定的法线"
- "共享编解码器降低内存和参数，同时保持性能"
- "位置插值RoPE防止高分辨率输入下的退化"
---

# Dens3R: A Foundation Model for 3D Geometry Prediction

> [!tip] 核心洞察
> 法线具有内在不变性（一对一映射），可减少多视角歧义并简化学习；结合共享编解码器和位置插值RoPE，实现高效高分辨率的多任务统一预测。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Dens3R：面向三维几何预测的基础模型 |
| 英文题名 | Dens3R: A Foundation Model for 3D Geometry Prediction |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=kxVjQhkAWz) · [Project](https://g-1nonly.github.io/Dens3R/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Dens3R |
| Dataset | NYUv2 (normal), ScanNet (normal), Sintel (normal), ZEB (image matching) |

> [!tip] 效果简介
> - NYUv2 (normal) 上，Mean Angular Error (↓) 为 16.1，对比 17.5 (Lotus)，变化 -1.4。
> - ScanNet (normal) 上，Mean Angular Error (↓) 为 16.9，对比 18.1 (Lotus)，变化 -1.2。
> - Sintel (normal) 上，Mean Angular Error (↓) 为 30.7，对比 34.9 (DSINE)，变化 -4.2。

## 概要

从单目或多视角图像中联合预测稠密三维几何量（点图、深度、法线、匹配关系）是三维视觉的基础需求，但现有方法普遍面临两大瓶颈：一是缺乏统一的多几何量联合预测框架，各任务通常由独立模型分别处理；二是表面法线这一具有内在不变性的关键几何信息被忽视或仅作为后处理导出，导致点云精度和几何一致性受限。Dens3R 针对上述瓶颈提出了一个统一的前馈视觉基础模型，其核心因果杠杆在于将表面法线作为内在不变性先验融入点图表示，并采用两阶段训练策略逐步构建从尺度不变到内在不变的点图表征，从而减少多视角歧义并简化学习过程。

在方法定位上，Dens3R 继承并扩展了 DUSt3R（Wang et al., 2024）和 MASt3R（Leroy et al., 2024）的稠密点图回归范式，但做出了四项关键改变：将编解码器改为共享权重结构以降低参数和内存开销；引入位置插值 RoPE 解决高分辨率输入下的退化问题；在第二阶段将点图扩展为内在不变形式并加入专用法线预测头；移除置信度损失，利用法线的确定性实现稳定预测。这些设计使 Dens3R 成为一个可同时输出点图、深度图、法线图和匹配特征的统一骨干网络。

主要实验结果表明，Dens3R 在多项基准上实现了有竞争力的性能：法线估计方面，在 NYUv2 上 Mean Angular Error 达 16.1（比 Lotus 低 1.4），在 Sintel 上达 30.7（比 DSINE 低 4.2）；深度估计在 DIODE-outdoor 上 REL 为 0.387（优于 VGGT 的 0.400）；图像匹配在 ZEB 数据集上 Mean AUC@5° 达 64.5（比 MASt3R 高 4.6）；位姿估计在 Map-free 数据集上重投影误差仅 30.4 px（VGGT 为 48.8 px）。消融实验证实，内在不变训练和粗到精策略共同贡献了法线精度的显著提升，共享编解码器减少了约 15% 参数量和约 10% 内存占用，位置插值 RoPE 有效防止了高分辨率退化。模型的主要局限在于对薄结构（细杆、绳索等）的预测精度仍显不足，且对高反射和低纹理区域存在挑战。



三维几何预测是计算机视觉的核心任务之一，涵盖深度估计、表面法线预测、点云重建和相机位姿估计等多个子问题。这些几何量在自动驾驶、机器人导航、增强现实和三维重建等应用中扮演着关键角色。然而，现有方法通常将这些任务视为独立问题分别处理，缺乏一个统一的框架来联合建模多种几何量之间的内在关联。

当前主流方案存在三个显著的瓶颈。第一，**缺乏多几何量联合预测的统一架构**。以 **DUSt3R**（Wang et al., 2024）和 **MASt3R**（Leroy et al., 2024）为代表的点图回归方法仅关注点云重建与匹配，**DSINE**（Bae & Davison, 2024）、**StableNormal**（Ye et al., 2024）等法线估计方法则独立运行，各方法之间无法共享几何先验。第二，**表面法线信息在点图表示中被严重忽视**。法线具有内在不变性——即法线方向不随相机内参或尺度变化而改变，这种一对一映射特性可以有效减少多视角歧义，但现有方法未能将其显式融入点图学习过程。第三，**高分辨率输入下的退化问题**。标准旋转位置编码（RoPE）在处理超出训练分辨率的输入时会导致预测质量急剧下降，限制了模型对精细几何细节的捕捉能力。

从因果机制来看，法线的内在不变性是一个关键的调控旋钮：将法线作为先验融入点图表示，可以迫使模型学习与视角无关的几何特征，从而简化多任务学习并提升预测一致性。同时，共享编解码器设计与位置插值RoPE的结合，为高效处理多视图高分辨率输入提供了结构基础。

本文提出 **Dens3R**，一个面向三维几何预测的基础模型，旨在以统一的前馈架构同时输出高质量的点图、深度图、法线图和匹配特征。其核心动机在于：通过将表面法线的内在不变性显式编码到点图表示中，并采用两阶段训练策略逐步构建从尺度不变到内在不变的几何理解，从而突破现有方法在多几何量联合预测上的精度与效率瓶颈。



## 核心方法与创新机理

Dens3R的核心创新在于将**表面法线作为内在不变性先验**系统性地融入点图表示，并围绕这一设计重构了DUSt3R/MASt3R系列的基础架构与训练范式。其关键改动可归纳为四个相互耦合的changed slots。

### 1. 法线集成与内在不变点图

DUSt3R和MASt3R仅预测点图，未显式建模法线。Dens3R在第二阶段将点图扩展为**内在不变点图（intrinsic-invariant pointmap）**，通过拼接法线特征 $P_i^n = P_i \oplus n$ 将法线信息注入表示。同时新增一个专用的**法线预测头**，对每个视图输出视图空间法线图。

这一设计的因果机制在于：法线具有内在不变性——一个表面点的法线在不同视角下是一对一映射的，不随相机姿态或尺度变化而改变。相比之下，点图的坐标值本身是视角相关的，需要跨视图对齐才能建立一致性。引入法线先验后，模型可以独立关注每个视角的局部几何，减少了多视图歧义，从而简化学习。

实验证据支持这一设计的有效性：
- 仅从尺度不变点图推导的法线精度不足（Figure 3），而加入内在不变训练和法线预测头后，法线边缘更锐利、整体更准确（Figure 4）。
- 消融实验（Table 3）表明，内在不变训练在所有五个法线基准上均显著降低Mean Angular Error并提升 $\delta_{11.25^\circ}$ 指标。

### 2. 两阶段训练策略

Dens3R采用**两阶段训练范式**替代DUSt3R的单阶段点图回归：

- **第一阶段**：训练ViT骨干、点图头和匹配头，学习**尺度不变点图**。损失函数组合了局部3D回归损失 $\mathcal{L}_{\mathrm{pts-loc}}$、全局3D回归损失 $\mathcal{L}_{\mathrm{pts-glb}}$、点图法线损失 $\mathcal{L}_{\mathrm{pts-n}}$ 和像素匹配损失 $\mathcal{L}_{\mathrm{match}}$。
- **第二阶段**：联合微调解码器、点图头和新增的法线头，将表示升级为**内在不变点图**。同时将监督策略从“一对多”映射切换为“一对一”映射，进一步减少歧义。

两阶段设计的因果逻辑是：第一阶段建立跨视图的几何一致性基础，第二阶段利用法线的内在不变性精炼表示。这种渐进式构建使模型先学会“空间在哪”，再学会“表面朝向”，避免了多任务联合训练初期的冲突。

### 3. 共享编解码器架构

DUSt3R和MASt3R对主视图和参考视图使用**分离的解码器**，而Dens3R采用**共享权重的解码器**处理所有帧。这一改动直接减少了模型冗余：根据Table 4的消融，共享结构使参数量从737.6M降至624.2M（约15%），内存占用从4.6GB降至4.1GB（约10%），而计算量保持不变（1.362 TFlops）。

共享解码器的设计动机与法线集成密切相关：当法线提供视角不变的信息后，解码器不再需要为不同视图学习独立的几何解释，共享权重即可有效捕捉跨视角的空间关系。

### 4. 位置插值RoPE

DUSt3R使用的标准RoPE在高分辨率输入下会出现退化——这是RoPE外推的已知问题。Dens3R引入**位置插值RoPE**：$R'(x, m) = R(x, \frac{m L}{L'})$，通过对原始编码进行位置缩放来适配更长的序列长度。

这一改动的效果需要与内在不变点图和粗到精训练策略配合才能充分体现。Figure 21/22的对比表明，单独使用插值RoPE不足以解决高分辨率退化问题；只有将其与内在不变点图及粗到精训练方案组合，才能在高分辨率（2K）输入下生成准确且结构良好的点图。

### 5. 置信度损失的移除

DUSt3R使用置信度损失作为自适应权重来调节多视图点图回归，本质上依赖额外视角来补偿单视角预测的不确定性。Dens3R移除了这一损失，理由是：法线的确定性本质（每个表面点有唯一法线方向）消除了对额外视角的依赖，使模型能够稳定地进行单视角法线预测。这一改动的置信度为0.9，需要更多消融证据来确认移除置信度损失对点图精度的独立影响。



![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_kxVjQhkAWz/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Dens3R. We propose Dens3R, a dense visual transformer backbone featuring a shared encoder-decoder architecture and multiple task-specific heads for geometric prediction. To train this foundation model, we adopt a two-stage strategy. In Stage 1, we learn a scale-invariant pointmap by enforcing cross-view mapping consistency across multiple viewpoints. In Stage 2, we incorporate surface normals and leverage one-to-one correspondence constraints to transform the representation into an intrinsic-invariant pointmap. Built upon this unified backbone, additional geometric prediction heads and downstream task branches can be seamlessly integrated to support a wide range of applications*

Dens3R 是一个前馈式密集视觉基础模型，以**未标定相机位姿的图像**为输入，输出统一的密集几何预测：点图（pointmap）、深度图、表面法线图及密集匹配特征。其核心设计围绕三个因果调控旋钮展开：**共享权重的编解码骨干**、**两阶段渐进式训练范式**以及**位置插值旋转位置编码（Position-Interpolated RoPE）**。

### 输入输出流

模型接受广义输入——支持多视图、多分辨率图像序列。对于一对输入图像 $(I_i)_{i=1}^2$，前向传播映射为：

$$(C_i, P_i, D_i, N_i, M_i)_{i=1}^2 = f((I_i)_{i=1}^2)$$

其中 $C_i$ 为相机参数，$P_i$ 为点图，$D_i$ 为深度图，$N_i$ 为视图空间法线图，$M_i$ 为密集匹配特征。这一统一输出使得模型可同时服务于深度估计、法线预测、图像匹配、位姿估计等多种下游任务。

### 骨干架构

Dens3R 采用**密集视觉Transformer骨干**，由以下模块串联构成：

1. **共享权重编码器（Shared-weight Encoder）**：处理输入图像序列，提取多视图图像特征。所有帧共享同一编码器权重，避免为不同视角维护独立编码器。

2. **共享权重解码器（Shared-weight Decoder）**：捕捉跨视角空间关系，建模整体3D场景结构。与 DUSt3R/MASt3R 的关键区别在于，Dens3R 使用**单一共享解码器**处理所有帧，而非为主视图和参考视图分别设置独立解码器。这一设计直接减少了约15%的参数量和约10%的内存占用，计算量不变（Table 4）。

3. **多任务预测头**：解码器输出之上挂载多个轻量级任务专用头——
   - **点图头（Pointmap Head）**：预测尺度不变或内在不变点图；
   - **深度头（Depth Head）**：预测逐像素深度图（第一阶段实例化）；
   - **法线头（Normal Head）**：预测视图空间法线图，提供内在不变性先验（第二阶段新增）；
   - **匹配头（Matching Head）**：提取密集匹配特征，用于图像间像素级对应。

### 位置编码策略

为应对高分辨率输入下标准RoPE的外推退化问题，Dens3R引入**位置插值RoPE**：

$$R'(x, m) = R\left(x, \frac{m L}{L'}\right)$$

通过对原始RoPE $R$ 进行位置缩放，使模型在训练分辨率 $L$ 和推理分辨率 $L'$ 之间平滑过渡。消融实验表明，单独使用插值RoPE不足以完全解决高分辨率退化——必须将其与内在不变点图及粗到精训练策略联合使用（Figure 21/22）。

### 两阶段训练范式

Dens3R 的核心洞察在于：**表面法线具有内在不变性（视角无关的一对一映射），将其融入点图表示可显著减少多视角歧义并简化学习**。基于这一洞察，训练分为两个阶段：

- **第一阶段**：学习**尺度不变点图**。通过跨视图映射一致性约束，训练ViT骨干、点图头和匹配头。损失函数组合了局部3D回归损失 $\mathcal{L}_{\mathrm{pts-loc}}$、全局3D回归损失 $\mathcal{L}_{\mathrm{pts-glb}}$、点图法线损失 $\mathcal{L}_{\mathrm{pts-n}}$ 和像素匹配损失 $\mathcal{L}_{\mathrm{match}}$。

- **第二阶段**：将点图扩展为**内在不变点图** $P_i^n = P_i \oplus n$（拼接法线特征），并新增法线预测头。此阶段将监督从“一对多”映射切换为“一对一”映射以降低歧义，并采用**粗到精分辨率调度**（先在512分辨率上微调建立稳定几何先验，再在1024分辨率上微调）。第二阶段总损失加入预测法线损失 $\mathcal{L}_{\mathrm{n}}$。

引入法线信息的因果链条清晰：内在不变训练使点图捕获法线中的几何信息，法线预测头进一步产生更锐利的边缘和更精确的结果（Figure 3/4, Table 3）。由于法线具有确定性，模型不再需要依赖额外视图的置信度加权机制（DUSt3R/MASt3R中的confidence loss），从而实现了更稳定、更准确的预测。

### 多视图后处理

对于多于两帧的输入，Dens3R采用“一对所有”匹配策略计算帧间对应，随后通过三角化获得多视图点云，沿用了MASt3R的后处理管线。



### 整体架构与输出映射

Dens3R 以未标定相机位姿的多视角图像对 $(I_1, I_2)$ 为输入，通过统一的稠密视觉Transformer骨干网络，输出每帧的五类几何量：相机内参 $C_i$、点图 $P_i$、深度图 $D_i$、法线图 $N_i$ 和匹配特征 $M_i$。整体映射关系为：

$$(C_i, P_i, D_i, N_i, M_i)_{i=1}^2 = f((I_i)_{i=1}^2)$$

该骨干网络的核心设计包括三个关键模块：**共享权重的编解码器**、**位置插值旋转位置编码（Position-Interpolated RoPE）**、以及**两阶段训练策略**。以下逐一展开。

---

### 共享权重编解码器

与 DUSt3R/MASt3R 为“主视图”和“参考视图”分别使用独立解码器的设计不同，Dens3R 在所有输入帧之间共享编码器和解码器权重。这一设计带来两个直接收益：

- **参数效率**：参数量从约 737.6M 降至约 624.2M（减少约 15%），内存占用从 4.6 GB 降至 4.1 GB（减少约 10%），而计算量保持不变（1.362 TFlops，Table 4）。
- **跨视角对称性**：共享解码器迫使模型学习视角无关的几何表示，有助于捕捉跨帧的空间关系并建模整体 3D 场景结构。

编码器负责提取每帧的图像特征，解码器则在融合多帧信息后输出统一的几何特征，供下游的任务特定预测头使用。

---

### 位置插值旋转位置编码（Position-Interpolated RoPE）

标准 RoPE 在高分辨率输入下会出现外推退化问题——当推理时的序列长度超过训练时的最大长度，位置编码失效导致预测质量骤降。Dens3R 采用位置插值策略解决这一问题：

$$R'(x, m) = R\left(x, \frac{m L}{L'}\right)$$

其中 $R$ 为原始 RoPE 编码函数，$L$ 为训练时的最大序列长度，$L'$ 为推理时更长的序列长度，$m$ 为位置索引。通过对位置索引进行线性缩放，新的编码 $R'$ 将长序列“压缩”回训练分布范围内，从而保持编码的有效性。

**关键因果链**：位置插值 RoPE 单独使用不足以完全解决高分辨率退化问题（Figure 22 验证了这一点），必须与**内在不变点图表示**和**粗到精训练策略**组合使用，才能在高分辨率（如 2K）输入下生成准确且结构良好的点图（Figure 21）。

---

### 两阶段训练策略与损失函数

Dens3R 采用渐进式两阶段训练范式，逐步构建从“尺度不变”到“内在不变”的点图表示。

#### 第一阶段：尺度不变点图训练

第一阶段的目标是学习跨视角一致的尺度不变点图。训练时使用“一对多”映射策略（一张图像对应多个视角的监督信号），损失函数组合了四个分量：

$$\mathcal{L}_{stage1} = \mathcal{L}_{\mathrm{pts-loc}} + \eta_1 \mathcal{L}_{\mathrm{pts-glb}} + \eta_2 \mathcal{L}_{\mathrm{pts-n}} + \eta_3 \mathcal{L}_{\mathrm{match}}$$

各分量含义如下：

- **局部 3D 回归损失** $\mathcal{L}_{\mathrm{pts-loc}}$：衡量预测点图在自身相机坐标系下的回归误差。

$$\mathcal{L}_{\mathrm{pts-loc}} = \left| \frac{1}{z_v} P_{masked}^{v,v} - \frac{1}{\bar{z}_v} \bar{P}_{masked}^{v,v} \right|$$

- **全局 3D 回归损失** $\mathcal{L}_{\mathrm{pts-glb}}$：衡量点图在另一相机坐标系下的对齐误差，强制跨视角几何一致性。

$$\mathcal{L}_{\mathrm{pts-glb}} = \left\| \frac{1}{z_t} P_{masked}^{v,t} - \frac{1}{\bar{z}_t} \bar{P}_{masked}^{v,t} \right\|$$

- **点图法线损失** $\mathcal{L}_{\mathrm{pts-n}}$：通过从点图推导表面法线并与真值比较，鼓励点图学习光滑表面和锐利边缘。

$$\mathcal{L}_{\mathfrak{pts},\mathfrak{n}} = \mathcal{L}_1(N^{v,v}, \hat{N}^{v,v}) + \mathcal{L}_1(N^{v,t}, \hat{N}^{v,t})$$

- **像素匹配损失** $\mathcal{L}_{\mathrm{match}}$：基于 InfoNCE 的密集匹配损失，确保每个像素在两幅图像间有唯一对应。

$$\mathcal{L}_{\mathrm{match}} = - \sum_{(i,j) \in \hat{\mathcal{M}}} \left[ \log \frac{s_\tau(i,j)}{\sum_{k \in \mathcal{P}^1} s_\tau(k,j)} + \log \frac{s_\tau(i,j)}{\sum_{k \in \mathcal{P}^2} s_\tau(i,k)} \right]$$

#### 第二阶段：内在不变点图训练

第一阶段的尺度不变点图直接推导的法线精度不足（Figure 3），因为存在多视角歧义。第二阶段引入**内在不变点图**（Intrinsic-Invariant Pointmap），通过拼接法线信息消除歧义：

$$P_i^n = P_i \oplus n$$

其中 $n$ 为法线特征，$\oplus$ 表示拼接操作。这一表示受 MoGe（Wang et al., 2025b）的仿射不变公式启发，但 Dens3R 进一步将法线作为显式监督信号融入点图表示。

第二阶段的关键调整包括：

- **监督策略切换**：从“一对多”映射切换为“一对一”映射，减少多视角监督引入的歧义。
- **新增法线预测头**：联合微调解码器、点图头和法线头，实现端到端优化。
- **预测法线损失**：直接监督法线头的输出。

$$\mathcal{L}_{\mathrm{n}} = \mathcal{L}_1(N^{v,v}, \bar{N}^{v,v})$$

第二阶段总损失为：

$$\mathcal{L}_{stage2} = \mathcal{L}_{\mathrm{pts-loc}} + \lambda_1 \mathcal{L}_{\mathrm{pts-glb}} + \lambda_2 \mathcal{L}_{\mathrm{pts-n}} + \lambda_3 \mathcal{L}_{\mathrm{n}}$$

其中权重配置为 $\lambda_1 = 1.0$，$\lambda_2 = 0.1$，$\lambda_3 = 1.0$。

#### 粗到精训练

在两阶段框架内，Dens3R 进一步引入粗到精分辨率调度：先在 512 分辨率上微调以建立稳定的几何先验，再在 1024 分辨率上微调以捕捉细粒度细节。消融实验（Table 3）表明，粗到精策略在所有测试数据集上均带来一致的精度提升，尤其对高分辨率输入效果显著。

**因果机制总结**：内在不变训练使点图能够捕获法线中的几何信息，法线头则进一步预测更锐利的边缘和更准确的结果。粗到精策略与位置插值 RoPE 协同，共同解决了高分辨率下的退化问题。移除置信度损失（DUSt3R/MASt3R 中用于自适应加权的组件）之所以可行，是因为法线的确定性使得模型不再依赖额外视角来稳定预测。



## 实验与关键发现

### 核心瓶颈与设计动因

现有方法缺乏统一的多几何量联合预测框架，且表面法线信息被忽视，导致点云精度和几何一致性受限。Dens3R 的核心设计围绕一个因果调节变量展开：**将表面法线作为内在不变性先验融入点图表示**。法线具有一对一映射的内在不变性，可减少多视角歧义并简化学习；结合共享编解码器和位置插值 RoPE，实现高效高分辨率的多任务统一预测。

### 主要实验结果

#### 表面法线估计

Dens3R 在五个数据集上的法线估计任务中均取得领先或次优结果（Table 1）。在 NYUv2 上，Mean Angular Error 降至 16.1，相比 **Lotus** 的 17.5 降低 1.4；在 ScanNet 上为 16.9（Lotus 为 18.1，降低 1.2）；在 Sintel 上为 30.7，显著优于 **DSINE**（Bae & Davison, 2024）的 34.9，降幅达 4.2。δ11.25° 指标上，Dens3R 在多个数据集上表现尤为突出，表明其预测的法线在角度精度上具有明显优势。定性结果（Figure 4）显示，Dens3R 在物体中心场景和无边界场景中均能生成更准确、更锐利的法线图，对反射表面和背景区域也表现出良好的鲁棒性。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_kxVjQhkAWz/figures/005_Table_1.jpg]]

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_kxVjQhkAWz/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison of normal prediction. We report the mean and median angular errors with each cell colored to indicate the best and the second . Dens3R achieves accurate normal prediction for both indoor and outdoor scenes. *We utilize Lotus-G for a fair comparison. Table 2: Benchmark on image matching on ZEB dataset. We report the AUC values with each cell colored to indicate the best and the second*

#### 图像匹配

在两视图匹配任务上，Dens3R 同样展现出竞争力。ZEB 数据集上 Mean AUC@5° 达到 64.5，相比 **MASt3R**（Leroy et al., 2024）的 59.9 提升 4.6 个点（Table 2）。ScanNet-1500 上 AUC@5° 为 65.6（MASt3R 为 62.4，提升 3.2），MegaDepth-1500 上 AUC@5° 为 73.9（Table 9、Table 10），均取得最优结果。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_kxVjQhkAWz/figures/022_Table_9.jpg]]
*Table 9: Two-view matching comparison on ScanNet-1500 Dataset. We report the AUC values with each cell colored to indicate the best and the second . Our method achieves state-of-the-art for two-view matching, surpassing all the previous methods*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_kxVjQhkAWz/figures/023_Table_10.jpg]]
*Table 10: Two-view matching comparison on MegaDepth-1500 Dataset. We report the AUC values with each cell colored to indicate the best and the second Our method also achieves state-of-theart for the two-view matching using the MegaDepth-1500 Dataset*

#### 深度估计与相机位姿

深度估计方面，Dens3R 在 DIODE-outdoor 上 REL 为 0.387，优于 **VGGT**（Wang et al., 2025a）的 0.400（Table 7）。定性比较（Figure 5、Figure 18-20）显示，Dens3R 在室内人体深度估计和室外自动驾驶场景中均产生更稳定、更准确的深度图，点云重建质量也优于 DUSt3R 系列方法。在 Map-free 数据集上的相机位姿估计中，Dens3R 的重投影误差降至 30.4 px，远低于 VGGT 的 48.8 px（Table 8）。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_kxVjQhkAWz/figures/021_Table_8.jpg]]
*Table 8: Camera pose estimation results of the Map-free dataset. We report the metrics with each cell colored to indicate the best and the second*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_kxVjQhkAWz/figures/020_Table_6.jpg]]
*Table 6: Full quantitative comparison of normal prediction. We report the mean and median angular errors with each cell colored to indicate the best and the second Table 7: Quantitative comparison on monocular depth prediction. We report the relative point error (REL), root mean square error (RMSE) and the percentage of inliers δ1, δ2, δ3 with each cell colored to indicate the best and the second . *We utilize Lotu-G disparity model for comparison*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_kxVjQhkAWz/figures/032_Figure_19.jpg]]
*Figure 19: Additional depth comparison of indoor scenes with VGGT. Dens3R demonstrates more accurate results for human depth estimation*

### 消融研究

#### 内在不变训练与粗到精策略

Table 3 的消融实验验证了两个关键设计的作用。去除内在不变训练（w/o IIT）后，所有数据集上的 Mean Angular Error 均上升，δ11.25° 下降；去除粗到精策略（w/o C2F）同样导致性能退化，尤其在高分辨率场景中细节损失明显。两者结合使用（完整模型）在所有数据集上取得最优法线预测结果。Figure 6 进一步表明，粗到精训练策略使得模型在 2K 分辨率输入下仍能保持细粒度几何细节。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_kxVjQhkAWz/figures/008_Table_3.jpg]]
*Table 3: Normal quantitative metrics for ablation. We demonstrate that both the intrinsic-invariant training and coarse-to-fine strategy contributes to accurate normal predictions*

#### 共享编解码器结构

Table 4 的消融显示，共享编解码器结构在保持相同计算量（1.362 TFlops）的前提下，将内存占用从 4.6 GB 降至 4.1 GB（约 10%），参数量从 737.6M 降至 624.2M（约 15%），同时不影响性能。这一设计显著提升了模型效率。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_kxVjQhkAWz/figures/011_Table_4.jpg]]
*Table 4: Ablation on shared encoder-decoder structure. We conduct experiments for both of the model on image pairs with 512 resolution. With the shared encoder-decoder structure, our model yields lower memory cost and less network parameters*

#### 位置插值 RoPE

Figure 21 和 Figure 22 的高分辨率消融实验揭示了一个关键发现：单独使用位置插值 RoPE 不足以解决高分辨率退化问题；必须将其与内在不变点图表示和粗到精训练策略结合，才能形成完整的高分辨率推理方案。这一组合方案有效防止了此前方法在高分辨率输入下的退化现象。

### 失败模式与局限性

尽管 Dens3R 在多项任务上取得显著提升，仍存在以下局限：

- **薄结构预测**：模型在预测细杆、绳索等薄结构时精度明显下降（Figure 12），受限于网络容量和训练数据噪声。
- **高反射与低纹理区域**：内在不变训练提升了法线质量，但对于某些高反射或低纹理表面仍存在挑战。
- **高分辨率依赖组合方案**：高分辨率推理依赖位置插值 RoPE 与粗到精训练的组合，单独使用插值 RoPE 不足以保证稳定性。

### 关键图表结论汇总

| 图表 | 核心结论 |
|------|----------|
| Table 1 | Dens3R 在五个法线估计基准上取得最优或次优，δ11.25° 优势尤为突出 |
| Table 2 | 两视图匹配 AUC@5° 超越 MASt3R 4.6 个点 |
| Table 3 | 内在不变训练和粗到精策略对法线精度均有显著贡献，两者结合效果最佳 |
| Table 4 | 共享编解码器减少约 15% 参数量和约 10% 内存，计算量不变 |
| Figure 6 | 粗到精训练使 2K 分辨率推理保持细粒度细节 |
| Figure 21/22 | 位置插值 RoPE 单独使用不足，需与内在不变点图和粗到精训练组合 |

### 补充图表

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_kxVjQhkAWz/figures/017_Table_5.jpg]]
*Table 5: Training dataset information. We reorganize a large-scale training dataset and divide the data into three types based on their quality. We also showcase the training objectives we apply during training, the number of image pairs and the corresponding dataset ratio*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_kxVjQhkAWz/figures/019_Table_6.jpg]]



## 定位与知识库关联

Dens3R 并非从零构建，而是深度扎根于以 **DUSt3R**（Wang et al., 2024）为代表的“稠密点图回归”范式，并在此基础上进行了三项关键重构：**将表面法线提升为内在不变性先验**、**统一多帧解码器为共享权重结构**、以及**引入位置插值 RoPE 以支持高分辨率推理**。理解 Dens3R 的定位，需要先厘清它与这一谱系中其他方法的继承与断裂关系。

### 从 DUSt3R/MASt3R 到 Dens3R：继承与突破

DUSt3R 开创性地将多视图立体匹配转化为端到端的点图回归问题，其核心是训练一个 ViT 编码器-解码器网络，直接从图像对中预测尺度不变的点图，并通过置信度损失自适应地融合多视图信息。**MASt3R**（Leroy et al., 2024）在此基础上增加了密集匹配头，将点图回归与特征匹配统一到同一框架中。Dens3R 继承了这一“点图作为通用几何表示”的思想，但识别出了两个关键瓶颈：

1. **解码器冗余**：DUSt3R 和 MASt3R 为主视图和参考视图分别维护独立的解码器，这不仅增加了参数量和内存开销，还隐含地将两个视图的几何推理割裂开来。Dens3R 将两个解码器合并为**共享权重解码器**，让所有输入帧通过同一个解码器处理。这一改动在保持计算量不变的前提下，将参数量从约 7.38 亿降至约 6.24 亿，内存占用从 4.6 GB 降至 4.1 GB（Table 4），同时并未损害性能——因为共享解码器迫使模型学习更通用的跨视角几何表示。

2. **法线信息的缺失**：DUSt3R 和 MASt3R 的点图表示本质上是尺度不变的，虽然可以通过有限差分从点图中推导法线，但这些法线质量较差（Figure 3），无法为下游任务提供可靠的几何先验。**MoGe**（Wang et al., 2025b）虽然引入了仿射不变表示，但其法线预测同样不够精确。Dens3R 的核心洞察在于：**表面法线具有内在不变性——它与视角无关，是场景的固有属性**。将法线作为显式预测目标并融入点图表示，可以大幅减少多视角歧义，简化学习任务。

### 与其他几何预测方法的边界

在法线估计领域，Dens3R 与 **DSINE**（Bae & Davison, 2024）、**GeoWizard**（Fu et al., 2024）、**StableNormal**（Ye et al., 2024）等专用法线预测器形成对比。这些方法通常针对单目法线估计设计，缺乏与稠密点图、深度图等其他几何量的联合建模能力。Dens3R 的优势在于：法线预测不是孤立任务，而是与点图回归共享编码器-解码器骨干，通过 **内在不变点图**（$P_i^n = P_i \oplus n$）这一表示，将法线作为点图的内在属性进行联合优化。实验表明，这种联合训练产生的法线比专用方法更准确、边缘更锐利（Table 1：NYUv2 上 Mean Angular Error 16.1 vs. Lotus 17.5；Sintel 上 30.7 vs. DSINE 34.9）。

在深度估计和多视图几何领域，Dens3R 与 **DepthAnythingV2**、**VGGT**（Wang et al., 2025a）等方法形成互补。VGGT 是一个多视图几何预测基线，Dens3R 在 DIODE-outdoor 深度估计（REL 0.387 vs. VGGT 0.400）和 Map-free 位姿估计（重投影误差 30.4 px vs. VGGT 48.8 px）上均取得更优结果，表明统一的点图-法线-深度联合表示比分离式预测更具优势。

### 适用边界与局限

Dens3R 的设计假设使其在以下场景表现出色，但也划定了明确的适用边界：

- **薄结构预测是当前能力的硬边界**：模型在预测细杆、绳索等薄结构时精度明显下降（Figure 12）。这受限于 ViT 骨干的感受野设计和训练数据中薄结构标注的噪声水平。这是一个需要手动验证的开放问题：是否可以通过更高分辨率的局部注意力机制或专门的薄结构增强训练来缓解。

- **高分辨率推理依赖组合方案**：位置插值 RoPE 单独使用不足以防止高分辨率退化（Figure 22），必须与内在不变点图和粗到精训练策略组合才能生效。这意味着 Dens3R 的高分辨率能力不是单一技术的产物，而是一个系统工程——这增加了复现和调试的复杂度。

- **多几何量的协调尚未达到最优**：Dens3R 同时预测点图、深度、法线和匹配特征，这些量之间存在紧密的耦合关系（例如法线是点图的导数，深度是点图的投影）。当前的两阶段训练策略虽然有效，但各损失项的权重（$\lambda_1=1.0, \lambda_2=1.0, \lambda_3=0.1$）是经验设定的，如何自动平衡多任务间的梯度冲突仍是一个开放问题。

- **非朗伯体表面和动态场景的鲁棒性未知**：内在不变表示假设表面法线是视角无关的，但这在强反射、半透明或动态形变表面上不再成立。论文未提供在这些退化条件下的系统评估。

### 开放问题与可能的后续方向

从 Dens3R 的定位出发，以下几个方向值得关注：

1. **多几何量的自适应协调**：能否设计一个元学习或不确定性加权机制，动态调整点图、深度、法线、匹配等损失项的权重，使模型在不同场景下自动聚焦于最可靠的几何线索？

2. **薄结构的专项增强**：是否可以在训练数据中合成薄结构增强样本，或引入高频注意力机制（如局部窗口注意力），在不显著增加计算量的前提下提升薄结构预测精度？

3. **位置编码的通用化**：位置插值 RoPE 是针对特定分辨率范围设计的工程方案。是否存在更通用的连续位置编码策略（如基于尺度的可学习编码），使模型对任意分辨率输入都具有鲁棒性？

4. **下游任务的零样本扩展**：Dens3R 的共享骨干理论上可以接入任意预测头。Figure 8 展示了语义分割的初步扩展，但能否在不修改骨干的情况下支持物体检测、场景流估计等更复杂的下游任务，仍有待验证。

5. **内在不变性的边界测试**：系统评估内在不变表示在镜面反射、透明物体、动态场景下的失效模式，将有助于明确这一核心设计的适用范围。



## 原文 PDF

![[paperPDFs/ICLR_2026/Dens3R_A_Foundation_Model_for_3D_Geometry_Prediction.pdf]]
