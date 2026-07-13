---
title: "Fast Monocular Scene Reconstruction with Global-Sparse Local-Dense Grids"
type: paper
paper_level: A
venue: CVPR
year: 2023
pdf_ref: paperPDFs/CVPR_2023/Fast_Monocular_Scene_Reconstruction_with_Global_Sparse_Local_Dense_Grids.pdf
code_link: null
project_link: https://dongwei.info/publication/ash-mono/
aliases:
- GSLDGGLG
- FMSRGSLDG
tags:
- CVPR_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "采用显式的全局稀疏局部稠密体素网格直接存储和查询SDF、颜色和语义属性，避免MLP，并通过自适应分配、碰撞自由哈希表和体渲染细化，在保持精度的同时实现大幅加速。"
primary_logic: "场景表面仅占空间的极小部分，通过在表面附近自适应分配稀疏体素块，并在块内使用稠密数组进行缓存友好的查询，可实现快速且内存高效的重建；进一步结合尺度校准初始化、可微分体渲染细化以及高维连续条件随机场（CRF）正则化，可达到与SOTA可比的重建质量，同时训练和推理速度提升一个数量级以上。"
claims:
- "提出的方法不使用MLP，直接在稀疏体素块网格中存储SDF，以实现快速重建。"
- "通过尺度校准和体素融合，可以从单目深度先验中快速获得房间级几何初始化。"
- "显式SDF网格允许在一次前向传递中同时计算SDF及其梯度，避免昂贵的双重反向传播。"
- "实验表明，本方法训练速度提升10倍，渲染速度提升100倍，且重建精度与MonoSDF可比，在7-Scenes上更优。"
---

# Fast Monocular Scene Reconstruction with Global-Sparse Local-Dense Grids

> [!tip] 核心洞察
> 场景表面仅占空间的极小部分，通过在表面附近自适应分配稀疏体素块，并在块内使用稠密数组进行缓存友好的查询，可实现快速且内存高效的重建；进一步结合尺度校准初始化、可微分体渲染细化以及高维连续条件随机场（CRF）正则化，可达到与SOTA可比的重建质量，同时训练和推理速度提升一个数量级以上。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于全局稀疏局部稠密网格的快速单目场景重建 |
| 英文题名 | Fast Monocular Scene Reconstruction with Global-Sparse Local-Dense Grids |
| 会议/期刊 | CVPR 2023 |
| Links | [paper](https://arxiv.org/abs/2305.13220) · [Project](https://dongwei.info/publication/ash-mono/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Global-Sparse Local-Dense Grids (GS-LD Grids) |
| Dataset | ScanNet scene 0084 (Time), ScanNet, 7-Scenes |

> [!tip] 效果简介
> - ScanNet scene 0084 (Time) 上，Training time (hours) 为 0.47，对比 4.36 (MonoSDF-Grid)，变化 -3.89 h。
> - ScanNet scene 0084 (Time) 上，Inference time (seconds per image) 为 0.25，对比 19.13 (MonoSDF-Grid)，变化 -18.88 s。
> - ScanNet 上，F-score 为 0.710 (Ours +CRF)，对比 0.750 (MonoSDF-Grid)，变化 -0.040。

## 概要

当前基于神经隐式表示的单目场景重建方法（如 **MonoSDF**）依赖 MLP 或特征网格来隐式编码几何与外观，导致训练和推理速度极慢，且无法有效利用场景表面固有的空间稀疏性——真实表面仅占三维空间的极小部分。本文提出 **Global-Sparse Local-Dense Grids (GS-LD Grids)**，一种显式的、可微分的全局稀疏局部稠密体素网格表示，直接在体素中存储 SDF、颜色和语义属性，完全摒弃 MLP，从而在保持与 SOTA 可比重建精度的同时，实现训练速度 **10 倍**提升、渲染速度 **100 倍**提升（Table 1）。

方法的核心思路围绕三个关键机制展开：(1) 提出一种**基于 SfM 与单目深度先验的尺度校准算法**，通过优化逐帧的二维尺度网格，消除单目深度预测的尺度歧义，进而通过体积融合快速获得房间级几何初始化（Figure 6）；(2) 设计**全局稀疏局部稠密的数据结构**，仅在表面附近自适应分配稀疏体素块，块内使用缓存友好的稠密数组进行三线性插值查询，并通过碰撞自由哈希表索引，实现高效的空空间跳过与连续位置采样（Figure 3）；(3) 在显式 SDF 网格上，**单次前向传递即可同时计算 SDF 值及其梯度**，避免了传统隐式方法中昂贵的双重反向传播，进一步加速可微分体渲染细化过程（Eq. 17-18）。

在 ScanNet 和 7-Scenes 基准上的实验表明，该方法在 ScanNet 上取得与 MonoSDF 可比的 F-score（0.710 vs. 0.750），在 7-Scenes 上则优于 MonoSDF（0.454 vs. 0.411），同时训练时间从 4.36 小时降至 0.47 小时，单帧推理时间从 19.13 秒降至 0.25 秒（Table 1, Table 2）。消融实验进一步验证了逐帧尺度优化的关键作用：若仅使用全局单一尺度，初始重建 F-score 将从 0.627 骤降至 0.17（ScanNet），凸显了尺度校准对后续重建质量的决定性影响（Table 3）。



### 单目场景重建的技术瓶颈

从单目图像恢复稠密三维场景几何是计算机视觉与机器人领域的核心问题。传统多视图几何方法（如**COLMAP**）依赖特征匹配与三角测量，在纹理丰富区域表现良好，但在纹理缺失区域（如白墙、地板）往往产生稀疏甚至空白的重建结果。近年来，以**NeRF**为代表的神经辐射场方法通过可微分体渲染实现了高质量的新视图合成，但其原始设计侧重于辐射场而非显式表面。后续工作如**UNISURF**、**NeuS**和**VolSDF**将神经隐式表示与有符号距离函数（SDF）结合，实现了更精确的表面重建。

然而，这些神经隐式方法存在一个根本性瓶颈：它们普遍采用多层感知机（MLP）或特征网格来参数化场景，导致训练和推理速度极慢。以当前代表性方法**MonoSDF**为例，其MLP变体（MonoSDF-MLP）和特征网格变体（MonoSDF-Grid）在单个ScanNet场景上的训练时间长达数小时，每帧推理时间接近20秒。这一速度严重限制了此类方法在实时或交互式应用中的部署可能性。

### 空间稀疏性的利用不足

上述速度瓶颈的根源在于，现有神经隐式方法未能有效利用场景表面的空间稀疏性。真实场景中，三维表面仅占据整个空间体积的极小部分，而MLP或稠密特征网格需要在整个空间范围内进行密集采样和查询。尽管一些方法引入了多分辨率哈希编码或稀疏八叉树结构来缓解这一问题，但它们仍然依赖MLP解码器进行属性查询，且查询过程涉及多次网络前向传播，计算开销依然显著。

### 单目深度先验的尺度歧义

另一个关键挑战在于单目深度先验的利用。单目深度估计网络能够提供丰富的几何线索，但其输出具有未知的全局尺度和帧间尺度不一致性。直接将未校准的单目深度用于三维重建会导致严重的几何畸变和帧间冲突。现有方法（如**ManhattanSDF**）通常依赖曼哈顿世界假设等强约束来缓解尺度问题，但这些假设在实际复杂场景中往往不成立，限制了方法的通用性。

### 本文动机

针对上述问题，本文提出了一种全新的技术路线：**完全摒弃MLP，采用显式的全局稀疏局部稠密（Global-Sparse Local-Dense, GS-LD）体素网格直接存储和查询SDF、颜色及语义属性**。其核心洞察在于：场景表面仅占空间的极小部分，通过在表面附近自适应分配稀疏体素块，并在块内使用稠密数组进行缓存友好的三线性插值查询，可实现快速且内存高效的重建。

为实现这一目标，本文进一步提出了一套完整的流程：首先通过尺度校准算法消除单目深度的帧间歧义，获得一致的几何初始化；随后利用可微分体渲染进行几何细化；最后引入高维连续条件随机场（CRF）在表面样本上联合优化颜色、法线和语义标签，增强物体边界的一致性。实验表明，该方法在ScanNet和7-Scenes数据集上训练速度提升10倍，渲染速度提升100倍，同时重建精度与当前最优方法可比，在7-Scenes上甚至更优。



## 核心方法与创新机理

### 瓶颈洞察：从隐式查询到显式存储

当前基于神经隐式表示的单目场景重建方法（如 **MonoSDF**）将场景几何与外观编码于 MLP 或特征网格中。这种设计导致两个根本性瓶颈：（1）每次查询 SDF 值或颜色均需通过网络前向传播，训练和推理速度极慢；（2）MLP 的全局连续先验难以有效利用场景表面的强空间稀疏性——实际占据空间的表面仅占体积极小比例，却需在整个空间均匀采样。

本文的核心洞察在于：**既然表面仅占空间的极小部分，为何不直接在表面附近显式存储 SDF，而非通过 MLP 隐式编码？** 这一转向显式表征的决策，构成了所有后续加速和精度设计的基础。

### 核心创新：全局稀疏局部稠密网格（GS-LD Grids）

为同时实现快速查询与高精度重建，本文提出 **Global-Sparse Local-Dense Grids（GS-LD Grids）**，其设计遵循三条原则：

**1. 全局稀疏分配（Global Sparsity）**
仅在近似表面附近分配体素块（voxel blocks），而非稠密覆盖整个场景。稀疏块通过碰撞自由哈希表（collision-free hash map）索引，空区域在光线步进时直接跳过，大幅减少无效查询。这一设计将内存和计算集中于有意义的表面区域，是速度提升的关键。

**2. 局部稠密存储（Local Density）**
每个稀疏块内部使用缓存友好的小稠密数组（$8^3$ 体素），直接存储 SDF 值、颜色和语义标签。三线性插值允许在连续位置采样，且无需任何 MLP 参与。与多分辨率特征网格（如 Instant-NGP 风格）相比，单一尺度的稠密数组避免了跨层级索引开销，查询效率提升两个数量级（见 Figure 8）。

**3. 无 MLP 的端到端可微性**
由于 SDF 和颜色直接存储在网格中，梯度可直接回传至体素属性，无需通过神经网络。更重要的是，在显式 SDF 网格中，$f_{\theta_d}$ 与 $\nabla f_{\theta_d}$ 可在同一次前向传递中通过三线性插值联合计算（公式 17-18），避免了隐式方法所需的昂贵双重反向传播。

### 关键方法槽位变更

相较于以 MonoSDF 为代表的基线方法，GS-LD Grids 在以下四个核心槽位进行了根本性替换：

| 方法槽位 | 基线方案（MonoSDF） | 本文方案 | 变更逻辑 |
|---------|-------------------|---------|---------|
| **场景表示** | MLP 或特征网格隐式编码 SDF/颜色 | 全局稀疏局部稠密体素网格，直接存储 SDF/颜色/语义，无 MLP | 用显式存储换查询速度，利用表面稀疏性降低内存 |
| **几何初始化** | 球体初始化（无先验） | 基于 SfM 与单目深度先验的尺度校准与体积融合初始化 | 用快速几何引导替代随机初始化，大幅缩短优化路径 |
| **SDF 梯度计算** | 两次自动微分（计算图回溯） | 单次前向传递中通过三线性插值同时计算 SDF 及其梯度 | 避免双重反向传播，加速体渲染训练 |
| **表面正则化** | Eikonal 正则化 | 高维连续 CRF（颜色、法线、语义）联合 Eikonal 正则化 | 在表面样本上联合优化多模态属性，增强物体边界一致性 |

### 创新之间的因果链路

上述四个槽位变更并非孤立，而是形成了一条因果链路：

1. **显式 SDF 网格**（槽位 1）使得**快速初始化**（槽位 2）成为可能——只需将校准后的深度反向投影并融合，无需任何优化即可获得房间级几何（Figure 6）。
2. 良好的初始化使得后续**可微体渲染细化**（槽位 3）仅需微调噪声区域，而非从零重建，大幅缩短训练时间。
3. 显式网格上的**连续 CRF 正则化**（槽位 4）进一步在表面样本上联合优化颜色、法线和语义标签，提升细节质量而不显著增加计算成本。

消融实验验证了这条链路的有效性：从初始化（F-score 0.627）到体渲染细化（0.714）带来主要精度提升，CRF 进一步微调至 0.710（ScanNet），而训练时间始终保持在 0.47 小时以内——仅为 MonoSDF-Grid 的约 1/9（Table 1）。

### 尺度校准：被低估的关键使能技术

在因果链路中，**逐帧深度尺度优化**（Section 3.3）虽然看似辅助模块，实则是整个系统可行的前提条件。单目深度预测器输出的是无物理尺度的相对深度，若仅使用全局单一尺度因子，初始重建的 F-score 将从 0.627 骤降至 0.17（ScanNet）和 0.26（7-Scenes）（Table 3 vs Table 2）。本文通过 2D 尺度网格 $\phi_i$ 和 SfM 共视约束，在帧间建立局部一致性，使得体积融合能够产生有意义的初始几何。这一设计使得“先融合后细化”的策略成为可能，是该方法区别于纯优化式隐式方法的核心分水岭。



本文提出的**全局稀疏局部稠密网格**（Global-Sparse Local-Dense Grids，GS-LD Grids）是一个从单目图像序列到带颜色与语义标签的三维场景重建的完整流水线。其核心设计理念是将场景表面固有的空间稀疏性显式编码为一种可微分的数据结构，从而在保持与SOTA神经隐式方法可比精度的同时，实现训练速度10倍、推理速度100倍的提升。

### 流水线总览

如图4所示，整个系统按顺序由以下模块构成：

1. **稀疏SfM重建**：首先使用COLMAP对输入的单目图像序列进行运动恢复结构（SfM），获得稀疏三维点云、相机位姿以及帧间共视关系。这些信息为后续深度尺度优化提供了必要的几何锚点和约束。

2. **深度尺度优化**：利用预训练的单目深度估计网络获取每帧的初始深度图，但这些深度图存在未知的绝对尺度。通过构建一个可优化的2D尺度网格，在SfM稀疏点云的共视约束下，联合优化所有帧的深度尺度，消除尺度歧义。

3. **稀疏体素分配与直接融合**：将尺度校准后的深度图反向投影到三维空间，仅在表面附近分配稀疏的体素块（block），形成全局稀疏的体素集合。随后，通过多帧观测的最小二乘融合，直接初始化每个体素的SDF值、颜色和语义标签，无需任何MLP。

4. **去噪**：对融合后的体素属性进行高斯滤波，减少单目深度预测和融合过程中引入的噪声，为后续细化提供更干净的初始状态。

5. **可微分体渲染细化**：利用体积渲染损失（颜色、深度、法线）和Eikonal正则化，对体素网格中的SDF和颜色属性进行端到端优化，恢复几何细节并修剪离群体素。

6. **连续CRF平滑**：在高维连续条件随机场框架下，联合优化表面样本点的颜色、法线和语义标签，增强物体边界处的一致性和细节保真度。

### 模块间的输入输出关系

流水线的信息流是单向且逐步精化的：SfM模块输出相机位姿和稀疏点云，作为深度尺度优化的输入；尺度校准后的深度图驱动稀疏体素分配和直接融合，产生初始的SDF/颜色/语义体素网格；该网格经过去噪后，进入可微分体渲染细化阶段，通过反向传播直接更新体素属性；最后，CRF模块在渲染细化后的表面上进行高维联合平滑，输出最终的重建结果。

### 核心数据结构定位

整个流水线围绕**全局稀疏局部稠密体素网格**这一核心数据结构展开。该结构使用无碰撞哈希表索引稀疏分配的体素块，块内则采用缓存友好的稠密数组存储SDF、颜色和语义属性（见图3）。这种设计使得场景表示完全显式化，无需MLP参与前向查询，从而在单次前向传递中即可同时计算SDF值及其空间梯度，避免了神经隐式方法中昂贵的双重反向传播。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2305_13220/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of our pipeline. We first use structure-from-motion (SfM) to obtain sparse feature-based reconstruction. With the sparse point cloud and covisibility information from SfM, we optimize the scale of predicted monocular depth images (§3.3), and perform volumetric fusion to construct a globally sparse locally dense voxel grid (§3.4). After initialization, we perform differentiable volume rendering to refine the details (§3.5.1), and apply high dimensional continuous CRFs to finetune normals, colors, and labels (§3.5.3)*



### 3.1 全局稀疏局部稠密数据结构

本方法的核心数据结构是一种**全局稀疏、局部稠密的可微体素网格**，直接存储 SDF 值 $\theta_d$、颜色 $\theta_c$ 和语义标签 $\theta_s$，完全摒弃 MLP。其设计遵循两个原则：

- **全局稀疏性**：仅在近似表面附近分配体素块（voxel block），通过无冲突哈希表（collision-free hash map）索引。光线行进（ray marching）时跳过空白区域，仅激活命中块（Figure 3）。
- **局部稠密性**：每个体素块内部使用稠密数组存储属性，支持缓存友好的三线性插值查询，在单次前向传递中同时获取 SDF 值及其梯度。

### 3.2 深度尺度优化模块

单目深度预测存在尺度模糊性，且不同帧的尺度不一致。本方法在 2D 尺度网格 $\phi_i$ 上优化每帧的逐像素尺度因子，利用 SfM 稀疏点云和共视关系作为约束。

**目标函数**：

$$
\operatorname*{min}_{\{\phi_i\}} \sum_{i,j\in\Omega} h(\phi_i,\phi_j) + \lambda \sum_i g(\phi_i)
$$

其中 $\Omega$ 为共视帧对集合，$h$ 为互约束，$g$ 为单帧约束。

**单帧重投影损失**（$g$）：

$$
g(\phi_i) = \sum_{\mathbf{x}_k} \lVert d_{\mathbf{x}_k\to i} - \mathcal{D}_i(\mathbf{p}_{\mathbf{x}_k\to i}) \phi_i(\mathbf{p}_{\mathbf{x}_k\to i}) \rVert^2
$$

其中 $\mathbf{x}_k$ 为 SfM 三维点，$d_{\mathbf{x}_k\to i}$ 为其在帧 $i$ 的重投影深度，$\mathcal{D}_i$ 为单目深度预测，$\phi_i(\mathbf{p})$ 为像素 $\mathbf{p}$ 处的尺度因子。

**二元一致性损失**（$h$）：

$$
h(\phi_i,\phi_j) = \sum_{\mathbf{p}\in\mathcal{D}_i} \Vert d_{ij} - \mathcal{D}_j(\mathbf{p}_{ij})\phi_j(\mathbf{p}_{ij}) \Vert^2 + \|\mathcal{T}_i(\mathbf{p}) - \mathcal{T}_j(\mathbf{p}_{ij})\|^2
$$

强制共视帧之间的深度一致性和颜色一致性，其中 $\mathcal{T}$ 表示颜色观测。

### 3.3 稀疏体素分配与直接融合模块

**体素分配**：将尺度校准后的深度图反向投影为三维点，对每个点所在体素块进行膨胀（dilation）操作以包含邻域，然后对所有帧取并集：

$$
\mathbf{X} = \cup_i \mathbf{X}_i, \quad \mathbf{X}_i = \cup_p \{ \mathrm{Dilate}(\mathrm{Voxel}(\mathbf{p})) \}
$$

其中 $\mathbf{p}$ 为像素坐标，$\mathrm{Voxel}(\cdot)$ 将其映射到对应体素块，$\mathrm{Dilate}(\cdot)$ 膨胀至邻域块（Figure 5）。

**SDF 直接融合**：对每个体素 $\mathbf{v}$，通过最小二乘融合多帧观测初始化 SDF 值：

$$
\theta_d(\mathbf{v}) = \arg\min_d \sum_i \bigl( - (d_{\mathbf{v}i} - \mathcal{D}_i(\mathbf{p}_{\mathbf{v}i}) \phi_i(\mathbf{p}_{\mathbf{v}i}) \bigr)^2
$$

其中 $d_{\mathbf{v}i}$ 为体素中心到相机光心的距离，$\mathbf{p}_{\mathbf{v}i}$ 为体素在帧 $i$ 的投影像素。颜色和语义标签通过类似融合方式初始化，随后经高斯滤波去噪（Figure 7）。

### 3.4 可微体渲染细化模块

**体渲染**：沿射线采样点 $\mathbf{x}_k$，通过三线性插值查询 SDF 值 $f_{\theta_d}(\mathbf{x}_k)$，转换为不透明度 $\alpha(\mathbf{x}_k)$，累积透射率计算渲染权重：

$$
w(\mathbf{x}_k) = \exp\bigl(-\sum_{j<k} \alpha(\mathbf{x}_j) \delta_j\bigr) \bigl(1 - \exp(-\alpha(\mathbf{x}_k) \delta_k)\bigr)
$$

深度渲染为期望终止深度 $D(\mathbf{r}) = \sum_k w(\mathbf{x}_k) t_k$，颜色和法线同理。

**Eikonal 正则化**：强制 SDF 梯度范数接近 1，保证距离场一致性：

$$
\mathcal{L}_{\mathrm{Eik}} = \left( \|\nabla f_{\theta_d}(\mathbf{x})\| - 1 \right)^2
$$

**关键加速机制**：在显式体素网格中，SDF 值及其梯度可在**单次前向传递**中联合计算，避免昂贵的双重反向传播：

$$
f_{\theta_d}(\mathbf{x}) = \sum_{\mathbf{x}_i\in\mathrm{Nb}(\mathbf{x})} r(\mathbf{x},\mathbf{x}_i) \theta_d(\mathbf{x}_i), \quad \nabla_{\mathbf{x}} f_{\theta_d}(\mathbf{x}) = \sum_{\mathbf{x}_i\in\mathrm{Nb}(\mathbf{x})} \nabla_{\mathbf{x}} r(\mathbf{x},\mathbf{x}_i) \theta_d(\mathbf{x}_i)
$$

其中 $\mathrm{Nb}(\mathbf{x})$ 为 $\mathbf{x}$ 的 8 邻域体素中心，$r(\cdot,\cdot)$ 为三线性插值权重。

### 3.5 连续 CRF 平滑模块

在表面 $\mathbb{S}$ 上定义高维连续条件随机场，联合优化颜色、法线和语义标签，增强物体边界一致性：

$$
E(\mathbb{S}) = \int_{\mathbb{S}} \psi_u(\mathbf{x}) d\mathbf{x} + \int_{\mathbb{S}}\!\int_{\mathbb{S}} \psi_p(\mathbf{x}_i,\mathbf{x}_j) d\mathbf{x}_i d\mathbf{x}_j
$$

其中 $\psi_u$ 为一元项（约束优化后属性接近当前值），$\psi_p$ 为二元成对项（基于颜色、法线、语义差异的高斯核加权平滑）。

### 3.6 联合优化损失

细化阶段的总损失为各模块损失的加权和：

$$
\mathcal{L} = \mathcal{L}_c + \lambda_d \mathcal{L}_d + \lambda_n \mathcal{L}_n + \lambda_{\mathrm{Eik}} \mathcal{L}_{\mathrm{Eik}} + \mathcal{L}_{\mathrm{CRF}}
$$

其中 $\mathcal{L}_c$、$\mathcal{L}_d$、$\mathcal{L}_n$ 分别为颜色、深度、法线的渲染损失。网格参数 $\{\theta_d, \theta_c, \theta_s\}$ 使用 RM-SProp 优化，初始学习率 $10^{-3}$，指数调度器 $\gamma=0.1$。



## 实验与关键发现

### 核心性能对比

本文提出的**Global-Sparse Local-Dense Grids (GS-LD Grids)** 在重建精度与计算效率之间实现了显著的权衡突破。在ScanNet场景0084上的时间分析（Table 1）显示，GS-LD Grids的训练时间仅为**0.47小时**，而MonoSDF-Grid需要**4.36小时**，训练加速约**9.3倍**；推理速度差距更为悬殊，GS-LD Grids每帧推理仅需**0.25秒**，MonoSDF-Grid则需要**19.13秒**，加速约**76.5倍**。这一速度优势的核心机制在于：显式SDF体素网格允许在单次前向传递中同时计算SDF值及其梯度（见公式17-18），避免了MLP所需的昂贵双重反向传播。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2305_13220/figures/008_Table_1.jpg]]
*Table 1: Train and inference time (per image) analysis on the Scan-Net scene 0084. Our approach both trains and evaluates faster*

在重建质量方面（Table 2），GS-LD Grids在ScanNet上达到**F-score 0.710**（+CRF），与当前最优的MonoSDF-Grid（0.750）差距仅为0.040，但在7-Scenes数据集上以**0.454**反超MonoSDF-Grid的**0.411**（+0.043）。这一跨数据集的表现差异揭示了方法的适用特性：GS-LD Grids在几何结构相对规整的室内场景（7-Scenes）中优势明显，而在纹理丰富、几何复杂的ScanNet场景中略逊于特征网格方法。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2305_13220/figures/010_Table_2.jpg]]
*Table 2: Quantitative comparison of reconstruction quality. While being much faster, our approach is comparable to the state-of-the-art MonoSDF [51] on ScanNet [7] and better on 7-scenes [13]*

Figure 8进一步揭示了底层数据结构的高效性：与NGP-grid相比，GS-LD Grids的端到端查询速度快**两个数量级**，且在大批量点查询时仍保持高效率。这归因于碰撞自由哈希表索引稀疏体素块，以及块内稠密数组的缓存友好设计。


### 阶段消融：从初始化到精细化的增益分析

Table 2的最后三行完整呈现了三个关键阶段的递进贡献：

- **Ours (Init)**：仅通过尺度校准和体积融合初始化，ScanNet F-score为**0.627**，7-Scenes为**0.447**。这表明初始化本身已具备相当的几何质量，验证了尺度校准算法的有效性（Figure 6）。
- **Ours (+Rendering)**：加入可微分体渲染细化后，ScanNet F-score跃升至**0.714**（+0.087），7-Scenes升至**0.460**（+0.013）。体渲染阶段贡献了**主要的精度增益**，尤其在ScanNet上提升显著，说明渲染损失能有效修复初始化阶段的噪声和离群值（Figure 7）。
- **Ours (+CRF)**：进一步施加高维连续CRF后，ScanNet F-score微调至**0.710**（-0.004），7-Scenes降至**0.454**（-0.006）。CRF在ScanNet上出现轻微退化，但在7-Scenes上仍保持正向贡献，说明其平滑效应在场景几何复杂度较高时可能过度约束细节。

CRF模块的内部消融（Figure 10）进一步表明：**语义项和法线项**对重建质量的影响最大，颜色项的影响相对较小。这暗示物体边界一致性主要依赖语义分割先验和法线方向约束，而非颜色相似性。

### 尺度优化的关键性验证

Table 3的消融实验揭示了逐帧深度尺度优化在整个流程中的**决定性作用**：移除该模块（仅使用全局单一尺度）后，初始重建F-score从**0.627骤降至0.17**（ScanNet）和**0.26**（7-Scenes）。这一崩塌式退化说明：单目深度预测的尺度模糊性若不通过SfM稀疏点云进行逐帧校准，将导致多帧融合时产生严重的几何不一致，使得后续的体渲染细化难以弥补初始误差。

### 各场景定量分析

Table 4和Table 5提供了ScanNet和7-Scenes上逐场景的F-score对比。在ScanNet的多个场景中，GS-LD Grids与MonoSDF-Grid的差距通常在0.02-0.05之间，表现稳定。Figure 12的误差热力图显示，重建误差主要集中在**纹理缺乏区域**（如白墙、地板），这些区域的SfM稀疏点云密度不足，导致深度尺度估计精度下降——这是方法当前的主要失败模式。

在7-Scenes上，GS-LD Grids在多数场景中优于MonoSDF-Grid，尤其在几何结构简单、视角覆盖充分的场景中优势突出。Figure 13的误差热力图进一步证实了这一点：误差分布均匀，未出现大面积离群区域。

### 公平性说明

需注意以下评估细节可能影响结果解读：
1. MonoSDF使用384×384中心裁剪的单目线索，而本文使用480×640全分辨率预测，输入分辨率的差异可能对重建细节产生影响。
2. 评估时所有方法均统一使用480×640分辨率的渲染深度进行TSDF融合，而非MonoSDF官方评估代码中的更高分辨率（968×1296），这一统一处理保证了时间对比的公平性，但可能略微低估MonoSDF的精度上限。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2305_13220/figures/002_Figure_2.jpg]]
*Figure 2: Qualitative reconstruction comparison on ScanNet [7]. While being 10× faster in training, we achieve similar reconstruction results to state-of-the-art MonoSDF [51], with fine details (see Fig. 9)*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2305_13220/figures/013_Figure_11.jpg]]
*Figure 11: Sparse reconstruction and covisibility matrix of ScanNet scenes selected by ManhattanSDF [14]*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2305_13220/figures/015_Table_4.jpg]]
*Table 4: Scene-wise quantitative results on ScanNet*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2305_13220/figures/016_Figure_12.jpg]]
*Figure 12: Error heatmap from our reconstruction (first row) to groundtruth (second row) for each scene in ScanNet [7]. Points are colorized by distance error ranging from 0 (blue) to 5cm (red) to its nearest neighbor in ground truth. Points with error larger than 5cm are regarded as outliers and colored in black*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2305_13220/figures/019_Figure_13.jpg]]
*Figure 13: Error heatmap from our reconstruction (first row) to groundtruth (second row) for each scene in 7-Scenes [13]. The colorization is the same as Fig. 12*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2305_13220/figures/014_Table_3.jpg]]
*Table 3: Initial reconstruction results without per-frame scale optimization (c. f. Ours (Init) in Table 4-5.)*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2305_13220/figures/017_Table_5.jpg]]
*Table 5: Scene-wise quantitative results on 7-Scenes*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2305_13220/figures/009_Figure_8.jpg]]
*Figure 8: Query time comparison between ours and NGP-grid, lower is better. For end-to-end query, ours is two magnitudes faster, and maintains a high efficiency with a large number of point query. For the grid query operation itself, ours also have a better performance than multiresolution feature grids*



## 定位与知识库关联

### 问题定位与核心瓶颈

单目场景重建的核心挑战在于从二维图像序列中恢复稠密、精确的三维几何与外观。近年来，以 **MonoSDF** 为代表的神经隐式表示方法在该领域取得了突破性进展，其通过 MLP 或特征网格隐式编码场景的符号距离场（SDF），结合可微分体渲染进行端到端优化。然而，这类方法存在根本性的效率瓶颈：MLP 的前向推理和反向传播计算代价高昂，且隐式表示无法有效利用场景表面的空间稀疏性——真实场景中，表面仅占据三维空间的极小部分，但神经隐式方法通常需要对整个空间进行密集采样或查询，导致训练和推理速度极慢，难以满足实时或大规模应用需求。

### 核心洞见与方法定位

本文提出的 **Global-Sparse Local-Dense Grids（GS-LD Grids）** 方法，其核心洞见在于**将场景重建从“隐式函数学习”范式转向“显式属性存储+可微分细化”范式**。具体而言，该方法直接在显式的体素网格中存储 SDF、颜色和语义属性，完全摒弃 MLP，从而消除了神经网络的推理开销。为兼顾内存效率和表达能力，GS-LD Grids 采用两级稀疏-稠密数据结构：在全局层面，仅在近似表面附近自适应分配稀疏的体素块（通过碰撞自由哈希表索引）；在局部层面，每个体素块内部使用稠密数组存储高分辨率属性，实现缓存友好的快速查询。这种设计使得单次前向传递即可同时计算 SDF 值及其梯度（通过三线性插值解析求导），避免了传统隐式方法中昂贵的双重自动微分。

在方法谱系中，GS-LD Grids 位于**经典多视图几何重建**与**神经隐式重建**的交汇处。它借鉴了经典方法（如 COLMAP）的显式几何表示和体积融合思想，同时保留了神经渲染的可微分优化能力。与纯几何方法相比，它通过可微分体渲染和连续条件随机场（CRF）正则化实现了更高的重建质量；与纯神经隐式方法（如 MonoSDF、UNISURF、NeuS、VolSDF）相比，它通过显式存储和稀疏分配实现了数量级的加速。

### 关键技术创新与基线对比

GS-LD Grids 相对于现有基线方法，在以下关键设计槽位上进行了根本性替换：

| 设计槽位 | 基线方法（以 MonoSDF 为代表） | GS-LD Grids | 核心优势 |
|---------|---------------------------|-------------|---------|
| 场景表示 | MLP 或特征网格隐式编码 SDF | 全局稀疏局部稠密体素网格，直接存储 SDF/颜色/语义 | 无需 MLP 推理，查询速度提升两个数量级（见 Fig. 8） |
| 几何初始化 | 球体初始化，需长时间优化 | 基于 SfM 和单目深度先验的尺度校准与体积融合初始化 | 快速获得房间级几何初始化，无需网格参数优化（见 Fig. 6） |
| SDF 梯度计算 | 两次自动微分（计算图反向传播） | 单次前向传递中三线性插值解析求导（Eq. 17-18） | 避免昂贵的双重反向传播，显著加速训练 |
| 表面正则化 | Eikonal 正则化或无 | 高维连续 CRF（联合优化颜色、法线、语义）+ Eikonal 正则化 | 增强物体边界一致性，提升细节质量 |

**尺度校准初始化**是 GS-LD Grids 的一项关键创新。现有单目深度估计方法输出的是尺度模糊的相对深度，直接用于重建会导致严重的尺度不一致。本文提出在 SfM 稀疏点云和共视关系的约束下，优化每帧的二维尺度网格，从而消除深度歧义（Eq. 1-6）。消融实验表明，若移除逐帧尺度优化（仅使用全局单一尺度），ScanNet 上的初始重建 F-score 将从 0.627 骤降至 0.17，7-Scenes 上降至 0.26（Table 3），充分验证了该模块的关键性。

**高维连续 CRF 正则化**是另一项差异化设计。传统方法通常仅在二维图像域或三维体素域独立处理几何和外观，而 GS-LD Grids 在表面样本上构建连续 CRF，联合优化颜色、法线和语义标签（Eq. 19-22）。消融实验显示，语义和法线项对重建质量的贡献最大，颜色项影响相对较小（Fig. 10）。

### 适用边界与局限

尽管 GS-LD Grids 在效率上取得了显著突破，其方法设计决定了以下适用边界和局限性：

1. **对 SfM 质量的强依赖**：方法的尺度校准和体素分配均依赖 COLMAP 的稀疏 SfM 结果。在纹理缺乏区域（如白墙、地板），SfM 点云稀疏，导致深度尺度估计不准确，进而影响这些区域的重建质量（见 Fig. 12 误差热力图）。对于运动模糊或低纹理场景，SfM 本身的鲁棒性也可能成为瓶颈。

2. **体素分辨率的固有限制**：当前实现使用 $8^3$ 体素块，体素大小为 1.5cm。这种离散化虽然带来了效率优势，但也限制了对极细小结构（如线缆、植物枝叶）的恢复能力。与可任意分辨率查询的 MLP 隐式表示相比，显式网格的表达能力受限于预定义的体素尺寸。

3. **动态场景未处理**：方法假设场景是静态的，未明确处理动态物体。含有移动人员的场景可能出现伪影或错误融合。

4. **室内场景偏置**：当前实验主要在 ScanNet 和 7-Scenes 等室内数据集上进行，方法对户外大场景（光照变化剧烈、包含天空区域、尺度跨度大）的适应性尚未验证。

### 开放问题与后续方向

基于上述局限，本文指向以下值得探索的开放问题：

1. **鲁棒 SfM 替代方案**：能否结合学习型稠密或半稠密 SfM 方法（如 PatchMatchNet），以提高低纹理区域的尺度估算鲁棒性？更激进的思路是探索无需 SfM 的端到端位姿-重建联合优化。

2. **混合表示**：当前方法完全摒弃了神经特征，但显式网格与神经特征的结合可能实现更精细的表征。例如，在稀疏体素块内存储轻量级特征编码而非直接属性，通过小型解码器查询，可能在不显著牺牲速度的前提下提升表达能力。

3. **户外扩展**：将该方法扩展到户外大场景重建需要解决若干挑战：户外光照变化剧烈，单目深度和语义先验的泛化性需重新评估；天空等无限远区域需要特殊处理；大尺度场景对内存管理和体素分配策略提出了更高要求。

4. **实时在线重建**：当前方法虽已大幅加速，但仍包含离线阶段（SfM、尺度优化）。探索增量式 SfM 与在线体素分配的融合，有望实现实时在线场景重建，这对 AR/VR 和机器人应用具有重要意义。



## 原文 PDF

![[paperPDFs/CVPR_2023/Fast_Monocular_Scene_Reconstruction_with_Global_Sparse_Local_Dense_Grids.pdf]]
