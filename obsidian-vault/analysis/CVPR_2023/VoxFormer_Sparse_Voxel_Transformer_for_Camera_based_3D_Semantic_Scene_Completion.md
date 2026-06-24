---
title: "VoxFormer: Sparse Voxel Transformer for Camera-based 3D Semantic Scene Completion"
type: paper
paper_level: A
venue: CVPR
year: 2023
pdf_ref: paperPDFs/CVPR_2023/VoxFormer_Sparse_Voxel_Transformer_for_Camera_based_3D_Semantic_Scene_Completion.pdf
aliases:
- VoxFormer
tags:
- CVPR_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过深度估计生成稀疏的三维占据体素查询提案（query proposals），仅对占据体素进行图像特征交叉注意力，避免了空白体素的特征污染。"
primary_logic: "先重建可见区域，再向被遮挡区域传播信息（reconstruction-before-hallucination），并利用三维空间稀疏性（sparsity-in-3D-space）使模型更高效、更准确。"
claims:
- "VoxFormer在SemanticKITTI上相对几何IoU提升20.0%，语义mIoU提升18.1%。"
- "VoxFormer-S在IoU上从MonoScene的36.80提升至44.02，相对增益19.62%。"
- "VoxFormer-T在短距离（12.8m）mIoU达到21.55，超出MonoScene 75.92%。"
- "VoxFormer的稀疏查询机制仅对占据体素进行交叉注意力，避免了2D→3D密集投影带来的特征歧义。"
---

# VoxFormer: Sparse Voxel Transformer for Camera-based 3D Semantic Scene Completion

> [!tip] 核心洞察
> 先重建可见区域，再向被遮挡区域传播信息（reconstruction-before-hallucination），并利用三维空间稀疏性（sparsity-in-3D-space）使模型更高效、更准确。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | VoxFormer：面向相机三维语义场景补全的稀疏体素Transformer |
| 英文题名 | VoxFormer: Sparse Voxel Transformer for Camera-based 3D Semantic Scene Completion |
| 会议/期刊 | CVPR 2023 |
| Links | [paper](https://arxiv.org/abs/2302.12251); [GitHub](https://github.com/NVlabs/VoxFormer) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | VoxFormer |
| Dataset | SemanticKITTI, SemanticKITTI hidden test set |

> [!tip] 效果简介
> - SemanticKITTI 上，IoU (51.2m) 为 44.15 (VoxFormer-T) / 44.02 (VoxFormer-S)，对比 36.80 (MonoScene)，变化 +19.62% (VoxFormer-S)。
> - SemanticKITTI 上，mIoU (51.2m) 为 13.35 (VoxFormer-T) / 12.35 (VoxFormer-S)，对比 11.30 (MonoScene)，变化 +18.1% relative (Abstract)。
> - SemanticKITTI 上，mIoU (12.8m, safety-critical short range) 为 21.55 (VoxFormer-T) / 17.66 (VoxFormer-S)，对比 12.25 (MonoScene)，变化 +75.92% (VoxFormer-T) / +44.2% (VoxFormer-S)。

## 概述

### 问题瓶颈

基于单目相机的三维语义场景补全（Semantic Scene Completion, SSC）旨在从二维图像中推理完整的三维几何与语义。现有主流方法**MonoScene**（Cao et al., CVPR 2022）采用密集的2D→3D特征投影策略，将图像特征直接映射到三维体素网格。这一做法的核心缺陷在于：空白或被遮挡的体素也会被赋予来自可见区域的特征，导致严重的特征歧义，妨碍模型对缺失区域的正确补全与语义推理。

### 核心洞察与方法定位

VoxFormer 提出**“先重建，后幻觉”（reconstruction-before-hallucination）**的范式，并充分利用三维空间的稀疏性（sparsity-in-3D-space）。其关键因果调控变量在于：通过深度估计生成稀疏的三维占据体素查询提案（query proposals），仅对占据体素进行图像特征的交叉注意力，从根本上避免了空白体素的特征污染。

方法采用两阶段设计：
- **Stage-1**：基于CNN的轻量查询提案网络，利用图像深度估计重建可见场景几何，从全局可学习体素查询中筛选出占据体素作为稀疏查询提案。
- **Stage-2**：基于MAE-like Transformer架构，先通过可变形交叉注意力为查询提案聚合多视图图像特征，再引入可学习掩码令牌填充未提议体素，通过可变形自注意力实现稀疏到密集的补全与语义分割。

### 主要结果

在 SemanticKITTI 基准上，VoxFormer 取得显著优势：
- **几何补全**：IoU 达 44.02（VoxFormer-S），相对 MonoScene（36.80）提升 **19.62%**。
- **语义分割**：mIoU 达 13.35（VoxFormer-T），相对提升 **18.1%**。
- **安全关键短距离**（12.8m）：mIoU 达 21.55（VoxFormer-T），相对 MonoScene 提升 **75.92%**。
- 隐藏测试集上，IoU 达 43.21，超出 MonoScene **26.5%**。

值得注意的是，VoxFormer 轻量版本（约60M参数）参数量远少于 MonoScene（约150M），训练显存低于 16GB，在高效性与准确性上实现了双重突破。

## 背景与动机

三维语义场景补全（Semantic Scene Completion, SSC）旨在从有限的传感器观测中联合推理出完整的三维几何布局与逐体素语义标签。这项任务对自动驾驶至关重要，因为安全规划需要理解被遮挡区域的空间结构与语义类别——例如，停靠在卡车后方的行人虽然不可见，但其潜在位置必须被系统感知。

早期的SSC方法依赖激光雷达（LiDAR）提供的精确深度测量。**SSCNet**（Song et al., CVPR 2017）开创性地将场景补全与语义标注统一在端到端框架中，但其性能高度依赖稠密的三维输入。后续工作如**LMSCNet**进一步推动了LiDAR-based SSC的发展，然而激光雷达的高成本和有限的分辨率限制了其大规模部署。

相比之下，单目相机因其低成本、高分辨率和丰富的语义信息而成为更具吸引力的替代方案。**MonoScene**（Cao et al., CVPR 2022）首次证明了仅凭单目RGB图像即可实现三维语义场景补全的可行性。然而，MonoScene采用的核心机制——密集的2D→3D特征投影——引入了一个根本性的瓶颈。

### 核心瓶颈：密集投影带来的特征歧义

MonoScene的密集投影策略将二维图像特征沿相机射线均匀地反投影到三维体素网格中。这一操作导致一个严重后果：大量空白或被遮挡的体素被错误地赋予了可见区域的特征。例如，一堵墙后的空间本应是空的或被其他物体占据，但密集投影会强制将墙面纹理特征传播到墙后体素，造成严重的特征污染。模型必须在这种充满歧义的特征空间中同时完成几何补全和语义推理，这本质上是一个病态问题。

更具体地说，这种歧义体现在两个层面：
- **几何层面**：模型难以区分“空白体素”和“被遮挡的占据体素”，因为两者在密集投影后都可能携带非零特征。
- **语义层面**：被遮挡区域的语义标签可能被可见物体的特征所覆盖，导致幻觉式预测。

### 动机：从“先投影后补全”到“先重建后补全”

本文的核心洞察在于逆转传统流程：**不应先将所有二维特征盲目投影到三维空间再尝试去噪，而应首先确定哪些体素是真实可见且被占据的，再仅对这些体素进行特征查询**。这一“先重建，后补全”（reconstruction-before-hallucination）的范式利用了三维空间固有的稀疏性——在自动驾驶场景中，绝大多数体素实际上是空的。通过显式建模这种稀疏性，模型可以避免对空白区域进行无意义的特征计算，从而将注意力集中在真正需要补全的未知区域。

此外，二维图像特征天然对应于可见且占据的表面，而非空白或被遮挡的空间。因此，一种合理的查询机制应当从三维空间出发，主动向二维图像请求特征，而非被动接受密集投影。这促使本文设计一种稀疏的、由三维体素驱动的交叉注意力机制，从根本上消除密集投影带来的特征歧义。

## 核心创新

VoxFormer 的核心创新在于将相机三维语义场景补全（SSC）从“密集投影—后处理”范式转变为“先重建可见、再补全遮挡”的稀疏查询范式。这一转变通过两个关键模块实现：**基于深度的类未知查询提案**和**MAE-like的稀疏到密集Transformer解码器**。

### 从密集投影到稀疏查询：消除特征歧义

现有相机SSC方法的瓶颈在于密集2D→3D特征投影。以 **MonoScene**（Cao et al., CVPR 2022）为代表的方案将图像特征沿深度维度均匀投影到三维体素网格，导致空白或被遮挡的体素也被赋予可见区域的特征，产生严重的**特征歧义**。模型需要在后续的密集3D UNet中自行“清洗”这些被污染的特征，这既低效又不准确。

VoxFormer 反转了这一交互方向：它首先通过深度估计确定场景中哪些体素是真实占据的，然后仅对这些占据体素执行**3D→2D的可变形交叉注意力**，从图像中精准提取视觉特征。这一设计将特征交互从“密集广播”变为“稀疏查询”，从根本上避免了空白体素的特征污染。

### 类未知查询提案：深度引导的稀疏体素选择

具体而言，Stage-1 通过一个轻量级的2D CNN（基于UNet结构）预测低分辨率占据图 $\mathbf{M}_{out}$，并从一组可学习的体素查询 $\mathbf{Q}$ 中选取被占据的位置作为查询提案：

$$\mathbf{Q}_p = \text{Reshape}(\mathbf{Q}[\mathbf{M}_{out}])$$

这一机制的关键在于：
- **深度先验驱动**：利用立体深度估计（MobileStereoNet）获取场景几何的初步线索，再由占据预测网络进行校正，使查询提案聚焦于真正可见的体素。
- **类未知设计**：查询 $\mathbf{Q}$ 在训练前不携带类别信息，避免了类别先验对补全过程的干扰，使模型能够灵活地补全任意形状的物体。
- **计算与显存高效**：相比密集查询（全量体素参与交叉注意力），稀疏查询将训练显存从不可行降至14.6GB以下，同时IoU从密集查询的43.52提升至44.02（Table 4）。

### MAE-like架构：从稀疏到密集的优雅补全

Stage-2 借鉴了MAE（Masked Autoencoder）的思想，将Stage-1的稀疏查询提案作为“可见令牌”，对未提议的体素位置填充**可学习的掩码令牌** $\mathbf{m} \in \mathbb{R}^d$。随后，全体素通过可变形自注意力进行交互：

$$\text{DSA}(\mathbf{F}^{3D}, \mathbf{F}^{3D}) = \text{DA}(\mathbf{f}, \mathbf{p}, \mathbf{F}^{3D})$$

这一设计实现了从稀疏占据体素向密集场景表示的平滑过渡：掩码令牌在自注意力中从邻近的可见体素聚合信息，逐步“幻觉”出被遮挡区域的几何与语义。相比MonoScene的密集3D UNet，MAE-like架构更轻量（VoxFormer-S约60M参数 vs MonoScene约150M参数），且在短距离安全关键区域（12.8m）的mIoU从12.25大幅提升至21.55（VoxFormer-T），相对增益达75.92%。

### 创新总结

| 设计维度 | MonoScene (基线) | VoxFormer (本文) |
|---------|-----------------|-----------------|
| 特征交互方向 | 密集2D→3D投影 | 稀疏3D→2D交叉注意力 |
| 查询来源 | 无显式查询 | 深度引导的类未知查询提案 |
| 解码器架构 | 密集3D UNet | MAE-like稀疏到密集Transformer |
| 核心原则 | 投影后清洗 | 先重建可见，再补全遮挡 |

这一“reconstruction-before-hallucination”的设计哲学，配合三维空间的稀疏性利用，使VoxFormer在几何补全（IoU相对提升20.0%）和语义分割（mIoU相对提升18.1%）上均大幅超越MonoScene，同时训练显存降低一个数量级。

## 整体框架

VoxFormer 采用**两阶段稀疏到密集**的架构范式，核心设计理念是“先重建可见区域，再向被遮挡区域传播信息”（reconstruction-before-hallucination）。整体流程从多帧RGB图像出发，最终输出完整的语义体素网格。

### 输入与输出定义

给定时间戳 $t$ 的输入图像序列 $\mathbf{I}_t = \{I_t, I_{t-1}, \dots\}$，模型输出一个密集的三维语义体素网格：

$$\mathbf{Y}_t \in \{c_0, c_1, \dots, c_M\}^{H \times W \times Z}$$

其中 $c_0$ 表示空体素，$c_1$ 到 $c_M$ 对应 $M$ 个语义类别。在SemanticKITTI数据集上，体素网格尺寸为 $256 \times 256 \times 32$（对应 $51.2\text{m} \times 51.2\text{m} \times 6.4\text{m}$ 的物理空间）。

### 流水线模块

VoxFormer的完整流水线（Figure 2）包含以下六个核心模块，按执行顺序串联：

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2302_12251/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework of VoxFormer. Given RGB images, 2D features are extracted by ResNet50 [61] and the depth is estimated by an off-the-shelf depth predictor. The estimated depth after correction enables the class-agnostic query proposal stage: the query located at an occupied position will be selected to carry out deformable cross-attention with image features. Afterwards, mask tokens will be added for completing voxel features by deformable self-attention. The refined voxel features will be upsampled and projected to the output space for per-voxel semantic segmentation. Note that our framework supports the input of single or multiple images*

1. **2D特征提取**：使用ResNet50骨干网络从RGB图像中提取多尺度特征，再通过FPN融合得到分辨率为输入 $1/16$ 的特征图 $\mathbf{F}_t^{2D} \in \mathbb{R}^{b \times c \times d}$（特征维度 $d=128$）。

2. **深度估计与校正**：通过深度预测器（如MobileStereoNet）估计图像深度 $\mathbf{Z}(u,v)$，随后由一个轻量级2D CNN（UNet-like结构）预测低分辨率占位图进行深度校正。该占位预测器输入尺寸为 $256 \times 256 \times 32$，输出尺寸为 $128 \times 128 \times 16$。

3. **类未知查询提案（Stage-1）**：根据校正后的占位图 $\mathbf{M}_{out}$，从一组预定义的可学习体素查询 $\mathbf{Q}$ 中选取被占据的体素作为查询提案 $\mathbf{Q}_p$：

   $$\mathbf{Q}_p = \text{Reshape}(\mathbf{Q}[\mathbf{M}_{out}])$$

   其中 $\mathbf{Q}_p \in \mathbb{R}^{N_p \times d}$，$N_p$ 为被提议的体素数量。这一步骤是VoxFormer区别于MonoScene（Cao et al., CVPR 2022）等密集投影方法的关键——仅对深度估计为占据的体素进行后续特征查询，避免了空白或被遮挡体素的特征污染。

4. **可变形交叉注意力（Stage-2）**：查询提案 $\mathbf{Q}_p$ 通过相机投影矩阵映射到各命中视图，在对应的2D特征图 $\mathbf{F}^{2D}$ 上进行可变形交叉注意力（Deformable Cross-Attention, DCA），聚合多视图视觉特征。

5. **掩码令牌与自注意力（Stage-2）**：未被提议的体素位置填充可学习的掩码令牌（mask token）$\mathbf{m} \in \mathbb{R}^d$，表示待预测的缺失体素。随后在全体素特征 $\mathbf{F}^{3D}$ 上进行可变形自注意力（Deformable Self-Attention, DSA），促进体素间的信息交互，实现从稀疏到密集的补全。这一设计借鉴了MAE（Masked Autoencoder）的架构思想。

6. **上采样与语义分割头**：将精炼后的体素特征上采样并投影至输出分辨率，通过语义分割头得到每个体素的最终类别预测 $\bar{\mathbf{Y}}_t$。

### 模块间数据流

整个流水线的数据流可概括为：

- **RGB图像** → [ResNet50 + FPN] → **2D特征图** $\mathbf{F}^{2D}$
- **RGB图像** → [深度预测器 + 深度校正CNN] → **校正后占位图** $\mathbf{M}_{out}$
- **可学习体素查询** $\mathbf{Q}$ + **占位图** $\mathbf{M}_{out}$ → [查询选择] → **稀疏查询提案** $\mathbf{Q}_p$
- **$\mathbf{Q}_p$** + **$\mathbf{F}^{2D}$** → [可变形交叉注意力] → **增强的查询特征**
- **增强查询特征** + **掩码令牌** → [可变形自注意力] → **密集体素特征** $\mathbf{F}^{3D}$
- **$\mathbf{F}^{3D}$** → [上采样 + 投影] → **最终语义体素网格** $\bar{\mathbf{Y}}_t$

### 训练损失

Stage-2使用加权交叉熵损失进行端到端训练：

$$\mathcal{L} = -\sum_{k=1}^{K}\sum_{c=c_0}^{c_M} w_c \hat{y}_{k,c} \log\left(\frac{e^{y_{k,c}}}{\sum_c e^{y_{k,c}}}\right)$$

其中 $w_c$ 按类别频率的倒数加权，以缓解类别不平衡问题。

### 设计优势

相比MonoScene的密集2D→3D特征投影方案，VoxFormer的稀疏查询机制带来两个关键优势：其一，仅在占据体素上进行交叉注意力，大幅降低了计算量和GPU显存（训练显存低于16GB）；其二，避免了空白体素被赋予可见区域特征的歧义，使模型能够更清晰地分辨“已知可见”与“需要补全”的区域，为后续的MAE-like密集化提供了更干净的起点。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2302_12251/figures/001_Figure_1.jpg]]
*Figure 1: (a) A diagram of VoxFormer for camera-based semantic scene completion that predicts complete 3D geometry and semantics given only 2D images. After obtaining voxel query proposals based on depth, VoxFormer generates semantic voxels via an MAE-like architecture [3]. (b) A comparison against the state-of-the-art MonoScene [4] in different ranges on SemanticKITTI [5]. VoxFormer performs much better in safetycritical short-range areas, while MonoScene performs indifferently at three distances. The relative gains are marked by red*

## 核心模块与公式推导

VoxFormer 采用两阶段设计，核心思想是“先重建可见区域，再向被遮挡区域传播信息”。以下按流水线顺序拆解关键模块及其数学表达。

### 2D 特征提取

给定当前帧及历史帧 RGB 图像 $\mathbf{I}_t = \{I_t, I_{t-1}, \dots\}$，使用 ResNet-50 骨干网络提取多尺度特征，并通过 FPN 输出分辨率为输入 1/16 的特征图：

$$
\mathbf{F}_t^{2D} \in \mathbb{R}^{b \times c \times d}
$$

其中 $b \times c$ 为空间分辨率，$d=128$ 为特征维度。

### 深度估计与反投影（Stage-1 前置）

采用立体深度估计器（如 MobileStereoNet）预测逐像素深度 $Z(u,v)$，随后通过相机内参将像素反投影至三维空间：

$$
x = \frac{(u - c_u) \cdot z}{f_u}, \quad y = \frac{(v - c_v) \cdot z}{f_v}, \quad z = Z(u, v) \tag{1}
$$

其中 $(f_u, f_v)$ 为焦距，$(c_u, c_v)$ 为主点坐标。反投影后的点云用于判断哪些体素被占据。

### 类未知查询提案（Stage-1）

Stage-1 的核心功能是生成稀疏的体素查询提案，仅对深度估计为占据的体素进行后续交叉注意力，避免空白体素的特征污染。

首先，一个轻量级 2D CNN（UNet-like 结构，记为 $\Theta_{occ}$）对深度图进行校正，预测低分辨率占位图 $\mathbf{M}_{out} \in \{0,1\}^{H' \times W' \times Z'}$。同时，在整个三维空间预定义一组可学习体素查询 $\mathbf{Q} \in \mathbb{R}^{H' \times W' \times Z' \times d}$。根据占位图从中选取占据体素作为查询提案：

$$
\mathbf{Q}_p = \text{Reshape}(\mathbf{Q}[\mathbf{M}_{out}]) \tag{2}
$$

其中 $\mathbf{Q}_p \in \mathbb{R}^{N_p \times d}$，$N_p$ 为被提议的占据体素数量。该机制使查询提案与可见几何结构对齐，从根本上切断了空白体素接收图像特征的路径。

### 可变形交叉注意力（Stage-2）

查询提案 $\mathbf{Q}_p$ 通过相机投影矩阵 $\mathcal{P}$ 映射到各视图，在命中视图上进行可变形交叉注意力以聚合视觉特征。可变形注意力的通用形式为：

$$
\text{DA}(\mathbf{q}, \mathbf{p}, \mathbf{F}) = \sum_{s=1}^{N_s} \mathbf{A}_s \mathbf{W}_s \mathbf{F}(\mathbf{p} + \delta\mathbf{p}_s) \tag{3}
$$

即在参考点 $\mathbf{p}$ 附近采样 $N_s$ 个偏移点，由可学习权重 $\mathbf{A}_s$ 和投影矩阵 $\mathbf{W}_s$ 加权求和特征。交叉注意力在多视图上取平均：

$$
\text{DCA}(\mathbf{q}_p, \mathbf{F}^{2D}) = \frac{1}{|V_t|} \sum_{t \in V_t} \text{DA}\big(\mathbf{q}_p, \mathcal{P}(\mathbf{p}, t), \mathbf{F}_t^{2D}\big) \tag{4}
$$

其中 $V_t$ 为查询提案 $\mathbf{q}_p$ 投影后命中的视图集合。该操作仅对 $N_p$ 个占据体素执行，大幅降低计算量。

### 掩码令牌与可变形自注意力（Stage-2）

未被 Stage-1 提议的体素位置填充可学习掩码令牌 $\mathbf{m} \in \mathbb{R}^d$，表示待预测的缺失体素。全体素特征 $\mathbf{F}^{3D}$（包含交叉注意力增强的提案特征与掩码令牌）通过可变形自注意力进行体素间信息传播，实现从稀疏到密集的补全：

$$
\text{DSA}(\mathbf{F}^{3D}, \mathbf{F}^{3D}) = \text{DA}(\mathbf{f}, \mathbf{p}, \mathbf{F}^{3D}) \tag{5}
$$

其中 $\mathbf{f}$ 为查询体素特征，$\mathbf{p}$ 为其三维位置。自注意力使被遮挡区域的掩码令牌能够从邻近可见体素聚合上下文，完成场景补全。

### 上采样与语义分割头

精炼后的体素特征经过上采样和投影，映射至目标输出分辨率 $\mathbf{\bar{Y}}_t \in \{c_0, c_1, \dots, c_M\}^{H \times W \times Z}$，其中 $c_0$ 表示空类别，$c_1$ 到 $c_M$ 为 $M$ 个语义类别。

### 损失函数

Stage-2 使用加权交叉熵损失进行训练，按类别频率的倒数加权以缓解长尾分布问题：

$$
\mathcal{L} = -\sum_{k=1}^{K} \sum_{c=c_0}^{c_M} w_c \, \hat{y}_{k,c} \log\left( \frac{e^{y_{k,c}}}{\sum_c e^{y_{k,c}}} \right) \tag{6}
$$

其中 $K$ 为总体素数量，$\hat{y}_{k,c}$ 为独热标签，$y_{k,c}$ 为预测 logit，$w_c$ 为类别 $c$ 的权重。

### 模块间因果链条

上述模块形成清晰的因果链路：**深度估计 → 占位图校正 → 稀疏查询提案 → 多视图交叉注意力 → 掩码令牌自注意力补全**。关键设计在于将特征交互方向从传统密集 2D→3D 投影反转为稀疏 3D→2D 交叉注意力，仅对深度确认的占据体素查询图像特征，从机制层面消除了空白体素的特征歧义。

## 实验与分析

### 核心实验设置

VoxFormer在**SemanticKITTI**数据集上进行评估，该数据集提供室外驾驶场景的密集语义体素标注。输出空间为$256 \times 256 \times 32$的体素网格，对应$51.2\text{m} \times 51.2\text{m} \times 6.4\text{m}$的物理范围。评估指标为**几何IoU**（二值占据）和**语义mIoU**（20类，含空类），并分别在$12.8\text{m}$、$25.6\text{m}$、$51.2\text{m}$三个距离范围报告结果。

2D特征提取采用**ResNet-50**骨干网络配合**FPN**，输出分辨率为输入图像的$1/16$，特征维度$d=128$。深度估计使用预训练的**MobileStereoNet**（立体版本）或单目深度预测器。Stage-1的占位预测器输入为$256 \times 256 \times 32$，输出低分辨率占位图$128 \times 128 \times 16$。训练采用加权交叉熵损失（按类频率倒数加权），优化器为AdamW，学习率$2 \times 10^{-4}$，共训练24个epoch。VoxFormer有两个变体：**VoxFormer-S**（轻量版，约60M参数）和**VoxFormer-T**（时序版，引入未来帧）。

### 与Camera-based SOTA的比较（Table 1）

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2302_12251/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison against the state-of-the-art camera-based SSC methods. We report the performances inside three volumes, i . e . , 1 2 . 8 $\times$ 1 2 . 8 $\times$ 6 . 4 $\mathrm { m } ^ { 3 }$ , 2 5 . 6 $\times$ 2 5 . 6 $\times$ 6 . 4 $\mathrm { m } ^ { 3 }$ 3, and 5 1 . 2 $\times$ 5 1 . 2 $\times$ 6 . 4 $\mathrm { m } ^ { 3 }$ . The first two volumes are introduced for assessing the SSC performance in safety-critical nearby locations. The top three performances are marked by red, green, and blue respectively

VoxFormer在所有距离范围上均显著超越此前最强的camera-based方法**MonoScene**（Cao et al., CVPR 2022）：

- **几何补全（IoU @ 51.2m）**：VoxFormer-S达到44.02，MonoScene为36.80，**相对提升19.62%**。VoxFormer-T进一步提升至44.15。
- **语义分割（mIoU @ 51.2m）**：VoxFormer-S为12.35，MonoScene为11.30，**相对提升9.3%**。VoxFormer-T达到13.35，**相对提升18.1%**（与Abstract声明一致）。
- **安全关键短距离（mIoU @ 12.8m）**：这是最显著的提升区间。VoxFormer-S达到17.66（MonoScene为12.25，**相对提升44.2%**），VoxFormer-T更是达到21.55，**相对提升75.92%**。

这一短距离的巨大优势验证了论文的核心动机：密集2D→3D投影在近处产生严重的特征歧义，而VoxFormer的稀疏查询机制从根本上避免了这一问题。在隐藏测试集上（Table I），VoxFormer-T的IoU达到43.21，相比MonoScene的34.16**相对提升26.5%**，进一步确认了方法的泛化性。

### 与LiDAR-based方法的比较（Table 2）

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2302_12251/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison against the state-of-the-art LiDAR-based SSC methods. VoxFormer even performs on par with some LiDAR-based methods at close range*

尽管VoxFormer仅使用单目相机输入，其在近距离的表现已可与部分LiDAR-based方法相媲美。例如在$12.8\text{m}$范围内，VoxFormer-T的IoU（65.38）接近**LMSCNet**等LiDAR方法的水平。这证明了“先重建可见区域”策略的有效性——在深度估计可靠的近距区域，相机信息通过稀疏查询被高效利用，弥补了传感器模态的差距。然而在远距离（$>25\text{m}$），深度估计质量下降导致性能差距拉大，这是该方法的主要瓶颈。

### 深度模态消融（Table 3）

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2302_12251/figures/006_Table_3.jpg]]
*Table 3: Ablation study for image depth. With monocular depth, VoxFormer-S performs better than MonoScene in geometry (12.8m, 25.6m, and 51.2m) and semantics (12.8m and 25.6m)*

将立体深度替换为单目深度后，VoxFormer-S仍然在几何指标上全面超越MonoScene（$12.8\text{m}$ IoU: 55.08 vs 53.25; $25.6\text{m}$ IoU: 37.45 vs 34.02; $51.2\text{m}$ IoU: 38.76 vs 36.80）。在短距离语义上同样保持优势（$12.8\text{m}$ mIoU: 14.83 vs 12.25）。这表明**VoxFormer的性能增益并非仅来自更优的深度估计，其稀疏查询和MAE-like架构本身具有更强的鲁棒性**。但需注意，单目深度在远距离语义上（$51.2\text{m}$ mIoU）略低于MonoScene，说明深度质量对远程语义补全仍有关键影响。

### 查询提案方式消融（Table 4）

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2302_12251/figures/007_Table_4.jpg]]
*Table 4: Ablation study for query proposal. Our depth-based query proposal performs best. Table 5. Ablation study for temporal input. +N means using the future frame t + N . Memory denotes training memory*

这是验证核心设计选择的关键实验。对比三种查询策略：
- **全查询（All queries）**：对所有体素进行交叉注意力，IoU 39.6，mIoU 10.8，训练显存20.1GB。
- **随机查询（Random queries）**：随机选取占位体素，IoU 42.1，mIoU 11.6。
- **基于深度的查询提案（Ours）**：IoU 44.0，mIoU 12.4，训练显存仅14.6GB。

基于深度的查询提案在性能和效率上均最优。全查询的性能下降直接印证了论文的核心论断——**空白体素参与特征交互会引入歧义噪声**。随机查询虽避免了部分噪声，但缺乏对可见区域的精准定位。该消融强有力地证明了深度引导的稀疏查询是性能提升的因果杠杆。

### 时序输入消融（Table 5）

引入未来帧可进一步提升性能。以VoxFormer-T为基线，添加$t+60$帧后，IoU从44.15提升至45.05，mIoU从13.35提升至16.20（**语义相对提升21.3%**）。这利用了自动驾驶场景中未来帧提供了当前被遮挡区域的补充信息。但需注意，实际部署中未来帧的可用性受限，该配置更适合离线感知任务。

### 特征层分辨率消融（Table 6）

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2302_12251/figures/008_Table_6.jpg]]
*Table 6: Ablation study for 2D image feature layers. Spatial resolution is relative to the input image size. Table 7. Ablation study for architecture*

对比不同FPN层级的2D特征分辨率（$1/8$、$1/16$、$1/32$），$1/16$分辨率在性能与模型大小间取得最佳平衡。更高分辨率（$1/8$）带来边际性能提升但显著增加计算开销，更低分辨率（$1/32$）则因空间信息损失导致性能下降。这一选择体现了对效率的审慎考量。

### 定性分析（Figure 3, Figure I）

定性可视化揭示了VoxFormer的两个关键优势：
1. **场景布局恢复**：在大型自驾驶场景中，VoxFormer能更完整地重建道路、建筑物等宏观结构，而MonoScene常产生碎片化或缺失的占据预测。
2. **细粒度物体补全**：对于树干、杆状物等小目标，VoxFormer表现出更强的形状补全能力。这得益于稀疏查询对可见几何的精确捕捉，以及MAE-like架构从可见区域向被遮挡区域的合理外推。

### 失败模式与局限性

尽管整体性能大幅领先，VoxFormer仍存在以下失败模式：

1. **远距离退化**：在$>25\text{m}$区域，深度估计的不可靠性导致查询提案质量下降，语义分割性能显著衰减，尤其是尾类（如行人、自行车）的IoU几乎为零。这是立体匹配和单目深度估计的固有局限。
2. **动态细粒度物体**：对行人、骑行者的补全精度仍然很低。这些类别在训练数据中占比小，且其非刚性形变和复杂外观使得纯视觉几何推理极为困难。
3. **视角覆盖局限**：当前方法仅使用前向相机（cam2），侧向和后向区域完全未被利用。这限制了全景场景补全的能力，尤其是在交叉路口等需要360°感知的场景。
4. **深度估计与SSC的分离优化**：深度预测器是离线预训练的，未与SSC任务联合优化。深度噪声可能通过查询提案传播为不可恢复的误差。

### 实验公平性说明

所有camera-based方法均在相同的SemanticKITTI数据划分和评估协议下比较。VoxFormer-S参数量（~60M）远小于MonoScene（~150M），训练显存低于16GB，但性能大幅领先，排除了“堆参数取胜”的嫌疑。消融实验均在统一训练配置下进行，确保了内部对比的公平性。隐藏测试集的结果进一步排除了验证集过拟合的可能。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2302_12251/figures/009_Table.jpg]]
*Table: I. Quantitative results of VoxFormer and the state-of-the-art MonoScene on the hidden test set of SemanticKITTI*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

**VoxFormer** 的核心贡献在于将相机三维语义场景补全（SSC）从“密集投影+3D CNN”范式迁移至“稀疏查询+MAE式Transformer”范式。其直接对标基线是 **MonoScene**（Cao et al., CVPR 2022），后者是首个纯相机SSC方法，采用密集2D→3D特征投影后接3D UNet解码。VoxFormer 在以下关键设计点上实现了范式转换：

| 设计维度 | MonoScene 基线 | VoxFormer 方案 | 机制差异 |
|---------|---------------|---------------|---------|
| 特征交互方向 | 密集2D→3D投影 | 稀疏3D→2D可变形交叉注意力 | 仅对占据体素查询，避免空白体素被错误赋予可见区域特征 |
| 解码器架构 | 密集3D UNet | MAE式Transformer（掩码令牌+自注意力） | 从稀疏可见区域向被遮挡区域传播信息，实现“先重建后幻构” |
| 查询来源 | 无显式查询机制 | 基于深度校正的类未知查询提案 | 利用深度先验筛选占据体素，降低计算冗余与特征歧义 |

定量层面，VoxFormer-S 在 SemanticKITTI 51.2m 范围上 IoU 从 MonoScene 的 36.80 提升至 44.02（相对增益19.62%），mIoU 从 11.30 提升至 12.35（相对增益18.1%）。在安全关键的12.8m短距离区域，VoxFormer-T 的 mIoU 达到 21.55，超出 MonoScene 75.92%。值得注意的是，VoxFormer 轻量版本参数量约60M，仅为 MonoScene（约150M）的40%，训练显存低于16GB，在效率与精度上形成双重优势。

与 LiDAR-based SSC 方法的比较（Table 2）表明，VoxFormer 在近距离场景下已可与部分激光雷达方法相媲美，但在远距离仍存在差距。这一定位说明纯视觉SSC正在逼近LiDAR方法的近程性能边界，但远程补全仍是开放挑战。

### 2. 适用边界

**输入模态边界**：VoxFormer 设计为仅使用前向单目或立体相机图像（SemanticKITTI 的 cam2），未利用多相机环视信息。侧向和后向区域的补全能力受限于单视角覆盖范围。

**距离边界**：方法性能随距离衰减显著。深度估计在>25m区域不可靠，导致远程体素的查询提案质量下降，语义分割尾类（如行人、自行车）的IoU几乎为零。立体深度估计（VoxFormer-S）在几何补全上优于单目深度（VoxFormer-T），但语义层面的远程退化问题仍未根本解决。

**场景边界**：方法在结构化自驾驶场景（如SemanticKITTI的高速公路与城市道路）中表现良好，但对细粒度动态物体（行人、骑行者）的补全精度较低。这源于深度估计对细长、运动物体的系统性偏差，以及训练数据中尾类样本不足。

**计算边界**：稀疏查询机制使训练显存降至16GB以下，但推理时仍需完整的深度估计与交叉注意力计算，实时性未在论文中明确报告，需手动验证其部署可行性。

### 3. 局限与开放问题

**已知局限**：
1. **远程退化**：>25m区域深度估计噪声导致几何与语义性能骤降，这是纯视觉SSC的共性瓶颈。
2. **单视角限制**：仅使用前向相机，未覆盖侧向和后向空间，限制了全景场景补全能力。
3. **尾类坍塌**：行人、自行车、摩托车等安全关键类别几乎无法补全，反映了深度先验对细粒度几何的失效。
4. **深度预测与SSC解耦**：深度估计模块（MobileStereoNet）与SSC网络独立训练，深度噪声直接传播至查询提案阶段，缺乏联合优化机制。

**开放问题**：
1. 能否通过解耦近程与远程分支（如多尺度查询提案）或引入语义引导的深度精炼来缓解远程退化？
2. 稀疏查询思想能否扩展至多相机360°环视设置，实现全景3D语义场景补全？这需要解决跨相机查询一致性与视野重叠区域的融合问题。
3. 深度预测与SSC的端到端联合优化是否能够通过梯度反馈减少深度噪声对占据提案的干扰？
4. 在训练数据与测试分布存在偏移的真实驾驶场景中，该方法的鲁棒性如何？论文未提供跨数据集或跨天气条件的泛化实验。
5. 掩码令牌的自注意力机制本质上是一种“从可见推演被遮挡”的生成式补全，其幻构能力是否存在系统性偏差（如倾向于生成常见类别而忽略稀有物体）？

### 4. 在知识库中的定位

VoxFormer 处于 **相机三维场景理解** 与 **稀疏Transformer架构** 的交叉点。其“先重建后幻构”（reconstruction-before-hallucination）的设计哲学与 MAE（He et al., CVPR 2022）的自监督预训练范式一脉相承，但将其从2D图像域迁移至3D体素域，并创新性地引入深度引导的稀疏查询作为可见区域先验。该方法为后续工作提供了两个可复用的技术组件：**类未知体素查询提案** 和 **稀疏到密集的MAE式3D解码器**，这两者均可独立嵌入其他3D感知任务（如3D目标检测、占用网络预测）。

与同期工作的关系上，VoxFormer 代表了从“密集投影”到“稀疏查询”的范式转折，后续基于Transformer的3D占用预测方法（如OccFormer、TPVFormer等）在不同程度上延续了稀疏查询与可变形注意力的设计思路，但需手动验证其具体引用关系。

## 原文 PDF

![[paperPDFs/CVPR_2023/VoxFormer_Sparse_Voxel_Transformer_for_Camera_based_3D_Semantic_Scene_Completion.pdf]]
