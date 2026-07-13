---
title: "PoseGAM: Robust Unseen Object Pose Estimation via Geometry-Aware Multi-View Reasoning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PoseGAM_Robust_Unseen_Object_Pose_Estimation_via_Geometry_Aware_Multi_View_Reasoning.pdf
project_link: "https://windvchen.github.io/PoseGAM"
code_link: null
aliases:
- PoseGAM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将物体几何信息（显式点云图与学习几何特征）通过视图图映射与交叉注意力注入多视图网络，同时构建涵盖19万个物体、多种挑战场景的大规模合成数据集，使网络能够端到端鲁棒预测姿态。
primary_logic: 将点云网络提取的全局几何特征按像素坐标重投影为视图格式，并通过交叉注意力与多视图令牌交互，既弥合了RGB预训练与3D模态的鸿沟，又充分利用了多视图架构的预训练权重，从而直接、准确地估计物体姿态。
claims:
- 在5个BOP核心数据集上平均AR超越先前最佳方法5.1%，在TUD-L上绝对提升17.6% AR。
- 添加点图与几何特征图后，低容错AUC@3从15.07提升至28.18，AUC@30达到84.30。
- FPS视图采样与更多视图数显著优于随机采样，证明全面覆盖物体可增强估计。
- 多视图基础模型VGGT在真实查询图像加入后点云出现较大离散，说明对外观不一致脆弱。
---

# PoseGAM: Robust Unseen Object Pose Estimation via Geometry-Aware Multi-View Reasoning

> [!tip] 核心洞察
> 将点云网络提取的全局几何特征按像素坐标重投影为视图格式，并通过交叉注意力与多视图令牌交互，既弥合了RGB预训练与3D模态的鸿沟，又充分利用了多视图架构的预训练权重，从而直接、准确地估计物体姿态。

| 字段 | 内容 |
|------|------|
| 中文题名 | PoseGAM：基于几何感知多视图推理的鲁棒未见物体姿态估计 |
| 英文题名 | PoseGAM: Robust Unseen Object Pose Estimation via Geometry-Aware Multi-View Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.10840) · [Project](https://windvchen.github.io/PoseGAM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PoseGAM |
| Dataset | LM-O, T-LESS, TUD-L, IC-BIN |

> [!tip] 效果简介
> - LM-O 上，AR 43.0 vs 42.1 (RayPose) (+0.9)。
> - T-LESS 上，AR 34.1 vs 36.9 (RayPose) (-2.8)。
> - TUD-L 上，AR 56.8 vs 48.3 (RayPose) (+8.5)。

## 概要

未见物体姿态估计的核心瓶颈在于：现有方法依赖显式特征匹配，匹配不可靠时精度急剧下降；而多视图基础模型由于缺乏物体3D几何信息且假设外观一致性，在真实查询图像与渲染模板视图之间存在域差异时，姿态预测严重偏离。PoseGAM 针对这一瓶颈，提出一种几何感知的多视图前馈框架，将物体几何信息——显式点云图与学习几何特征——通过视图图映射与交叉注意力注入多视图网络，同时依托涵盖19万个物体、多种挑战场景的大规模合成数据集进行端到端训练，从而直接、鲁棒地预测物体绝对位姿，无需显式匹配步骤。

在五个 BOP 核心数据集上，PoseGAM 的平均召回率（AR）超越先前最佳方法 **RayPose** 2.0 个百分点（41.1 vs. 39.1），在 TUD-L 上绝对提升达 8.5 个百分点（56.8 vs. 48.3）。消融实验表明，注入点图使低容错 AUC@3 从 15.07 跃升至 25.94，进一步注入几何特征图将 AUC@30 推至 84.30；FPS 视图采样策略与更多视图数对精度增益显著。同时，实验揭示多视图基础模型 VGGT 在加入真实查询图像后点云重建出现较大离散，验证了外观不一致输入的脆弱性，反衬出显式几何注入的必要性。

方法层面，PoseGAM 以 DINOv2 编码多视图图像令牌，PTv3 点云网络提取全局几何特征并按视图重排为特征图，经交叉注意力与多视图令牌交互，弥合了 RGB 预训练与 3D 模态的鸿沟，同时充分利用 VGGT 的多视图架构预训练权重。该方法在范式上从“显式匹配 + 几何求解”转向“端到端前馈直接预测”，在几何信息利用上从“仅 2D-3D 对应”升级为“点图与学习特征的视图级融合”，构成未见物体姿态估计的新基线。

未见物体姿态估计（unseen object pose estimation）面临一个根本性瓶颈：**现有方法普遍依赖显式特征匹配**——先建立查询图像与物体模型之间的2D-3D对应关系，再通过PnP等几何求解器计算位姿。这类范式（如**OSOP**、**ZS6D**、**MegaPose**、**GenFlow**、**GigaPose**、**FoundPose**、**RayPose**）在匹配不可靠时精度急剧下降，而匹配不可靠在纹理稀疏、遮挡严重或光照变化剧烈的真实场景中恰恰是常态。

另一条路径是直接利用多视图基础模型（如**VGGT**）预测相对位姿，但这类模型存在两个致命缺陷：**一是缺乏物体的3D几何信息**，仅依赖RGB外观进行跨视图推理；**二是强假设渲染视图与真实查询图像之间外观一致**。当真实查询图像与合成渲染视图之间存在域差异（domain gap）时，多视图基础模型的重建点云会出现显著离散，导致姿态预测严重偏离——这一脆弱性在论文附录的定性分析（Figure 5）中得到了直接验证。

上述两条路径的困境指向同一个因果杠杆：**如何将物体3D几何信息有效注入多视图推理框架，同时弥合RGB预训练与3D模态之间的鸿沟**。这正是PoseGAM的核心动机——通过显式点云图与学习几何特征的双重注入机制，使网络能够在端到端的前馈过程中直接、鲁棒地预测绝对位姿，从而绕开显式匹配的脆弱环节。

## 核心方法与创新机理

PoseGAM 的核心创新在于**将物体几何信息注入多视图架构，实现端到端的前馈位姿预测**，从而绕开了传统方法对显式特征匹配的依赖。具体而言，该方法在以下四个维度上形成了相对于现有工作的关键突破。

### 1. 范式转变：从“匹配-求解”到“端到端前馈预测”

现有未见物体姿态估计方法普遍遵循“显式特征匹配 + 几何求解”的范式：先建立查询图像与模板渲染图之间的 2D-2D 或 2D-3D 对应关系，再通过 PnP 等几何求解器恢复位姿。无论是以 **OSOP** 为代表的对应关系匹配方法，还是 **MegaPose**、**GenFlow**、**GigaPose**、**FoundPose** 等匹配后细化/定位方法，均依赖匹配质量的可靠性。当物体纹理稀疏、遮挡严重或外观域差异大时，匹配失败会直接导致位姿精度急剧下降。

PoseGAM 将问题重新定义为端到端的前馈回归任务：

$$T_{\mathrm{query}} = \mathrm{Network}(I_{\mathrm{query}}; T, \mathcal{V})$$

网络同时接收查询图像 $I_{\mathrm{query}}$ 和多视图模板图像 $\mathcal{V}$ 及其相机变换 $T$，直接输出物体-相机变换矩阵 $T_{\mathrm{query}}$，无需任何显式匹配步骤。这一范式转变的深层动机在于：**多视图基础模型（如 VGGT）虽具备强大的跨视图推理能力，但因其缺乏物体的 3D 几何信息且假设外观一致性，当真实查询图像与渲染模板视图之间存在域差异时，姿态预测会出现严重偏离**（Figure 5 展示了 VGGT 在加入真实查询图像后重建点云出现显著离散的现象）。PoseGAM 正是通过端到端训练，让网络自行学习弥合这一域隙。

### 2. 几何信息注入：显式点图与学习几何特征的双通道融合

PoseGAM 通过两条互补通道将物体几何信息注入多视图网络：

- **显式点图（Point Maps）**：从物体模型 $\mathcal{M}$ 的每个渲染视角，通过深度图反投影生成世界坐标下的点图 $\mathcal{P}$，经轻量 CNN 编码为点图令牌 $\{\mathbf{p}_i^{(1)}, \mathbf{p}_i^{(2)}, \cdots, \mathbf{p}_i^{(L)}\}$。这些令牌直接编码了物体表面在 3D 空间中的显式位置信息。

- **学习几何特征图（Geometry Feature Maps）**：使用点云网络（PTv3）提取物体点云的全局几何特征，然后按像素坐标将逐点特征重投影为视图格式的特征图 $\mathcal{F} = \{F_i\}$，再经 CNN 编码为几何特征令牌 $\{\mathbf{f}_i^{(1)}, \mathbf{f}_i^{(2)}, \cdots, \mathbf{f}_i^{(L)}\}$。

消融实验（Table 2）有力地证明了这一设计的决定性作用：仅使用 RGB 图像和相机参数时，低容错指标 AUC@3 仅为 15.07；加入点图后，AUC@3 跃升至 25.94；进一步注入几何特征图，AUC@30 从 80.26 提升至 84.30。这表明显式点图主要贡献于精细位姿的准确性，而学习几何特征则在更宽松的容错范围内提供了全局结构约束。

### 3. 几何特征注入方式：视图图重投影与交叉注意力

如何将 3D 几何特征有效注入 2D 多视图网络是一个关键设计选择。PoseGAM 的方案是：**将全局点特征按视图重排为特征图，再通过交叉注意力作为 KV（键-值）输入**，而非直接将原始点云特征令牌拼接到多视图令牌序列中。

具体而言，交叉注意力机制的形式为：

$$\mathrm{CA}(Q \gets \mathbf{multiview~tokens}, KV \gets \mathbf{geometry~tokens})$$

多视图令牌作为查询（Query），几何令牌作为键-值（Key-Value）。这种设计有双重优势：（1）弥合了 RGB 预训练视觉编码器（DINOv2）与 3D 点云模态之间的表示鸿沟；（2）充分利用了多视图架构中预训练 Transformer 权重的跨视图推理能力。Table 5 的消融证实，PTv3 + View Format + CrossAttn 的组合在所有几何注入策略中取得了最佳效果。

### 4. 训练数据分布：大规模多样化合成数据集

为支撑上述方法的训练，PoseGAM 构建了一个包含 **190k+ 物体**的大规模合成数据集，覆盖四种渲染场景：

- **centric**：物体居中渲染，模拟标准模板视图
- **uncentric**：物体偏离中心，模拟检测框不精确的情况
- **变动光照**：随机化环境光照，增强对光照变化的鲁棒性
- **外观编辑**：利用 FLUX.1-Canny-dev 对渲染图进行纹理和外观编辑，模拟真实场景中的外观变异

这一数据策略使得网络在训练阶段即暴露于广泛的域差异，从而在推理时对真实查询图像的外观不一致具有更强的容忍度。

PoseGAM 将未见物体姿态估计重新定义为**端到端前馈多视图推理任务**，彻底摒弃了传统方法中显式特征匹配与几何求解（如 PnP）的级联范式。其核心输入为一张查询图像 $I_{\text{query}}$ 和物体 3D 模型 $\mathcal{M}$，输出为物体到相机的刚体变换 $T_{\text{query}}$：

$$T_{\text{query}} = \mathrm{Network}(I_{\text{query}}; \mathcal{M})$$

为实现这一目标，网络在物体模型周围采样一组相机位姿 $\mathcal{T}$，渲染出多视图模板图像 $\mathcal{V}$ 及对应的深度图、点图等几何表示，将单帧姿态估计扩展为多视图联合推理问题：

$$T_{\text{query}} = \mathrm{Network}(I_{\text{query}}; \mathcal{T}, \mathcal{V})$$

整个 pipeline 由六个核心模块串联构成，数据流如图 2 所示：

1. **DINOv2 图像编码器**：将查询图像（经前景分割裁剪）与 $N$ 幅渲染模板视图分别编码为 $L$ 个视觉令牌序列，每帧额外附加一个相机令牌，形成 $(L+1) \times (N+1)$ 的令牌集合。
2. **相机编码器（MLP）**：将每帧的相机参数（四元数旋转 + 平移向量 + 视场角 FoV）映射为单个相机令牌。对于渲染视图使用已知内外参，对于查询图像则使用可学习的嵌入向量。
3. **点图 CNN**：从物体模型渲染深度图并反投影得到世界坐标系点图 $\mathcal{P}$，经轻量卷积网络提取为 $L$ 个点图令牌 $\{\mathbf{p}_i^{(1)}, \cdots, \mathbf{p}_i^{(L)}\}$。
4. **几何特征提取器（PTv3）**：以逐视图构建的点云（拼接点图、法线图、RGB 图）为输入，提取每点几何特征，再按像素坐标重投影为视图格式的特征图 $\mathcal{F}$，经 CNN 编码为几何特征令牌 $\{\mathbf{f}_i^{(1)}, \cdots, \mathbf{f}_i^{(L)}\}$。
5. **融合 Transformer（24 层）**：交替执行交叉注意力与帧内/帧间自注意力。关键设计在于**多视图令牌作为 Query，几何令牌（点图 + 特征图）作为 Key-Value**，通过交叉注意力将显式与隐式几何信息注入多视图表示，规避了 RGB 预训练与 3D 模态间的特征鸿沟。
6. **姿态解码头**：从查询图像对应的相机令牌解码出相机到物体的变换 $T_{\text{Obj}}^{\text{Cam}}$，再通过矩阵求逆得到最终物体到相机的位姿 $T_{\text{query}}$。

该框架的核心创新在于**几何信息的双重注入机制**：显式点图提供精确的空间坐标约束，学习几何特征则捕获物体的全局形状上下文，二者以视图图（view-map）格式统一表示，使多视图基础模型的预训练权重得以充分利用。

![[assets/figures/papers/paper_list_l2058_https_arxiv_org_abs_2512_10840/figures/002_Figure_2.jpg]]
*Figure 2: Overview of PoseGAM. Given a query image*

PoseGAM 的核心目标是从查询图像 $I_{\mathrm{query}}$ 和物体模型 $\mathcal{M}$ 直接预测物体到相机的变换矩阵 $T_{\mathrm{query}}$，其整体范式定义为：

$$T_{\mathrm{query}} = \mathrm{Network}(I_{\mathrm{query}}; \mathcal{M})$$

该框架将问题重构为多视图推理任务：在物体模型周围采样一组相机位姿并渲染多幅模板视图 $\mathcal{V}$，网络联合处理查询图像与这些模板视图，端到端地估计位姿：

$$T_{\mathrm{query}} = \mathrm{Network}(I_{\mathrm{query}}; T, \mathcal{V})$$

### 1. 多视图令牌提取

网络首先将多视图输入转化为统一的令牌表示。对于 $N$ 幅模板渲染图和 1 幅查询图像，DINOv2 图像编码器将每幅图像提取为 $L$ 个图像令牌，同时相机编码器（MLP）将每帧的相机参数（四元数 + 平移 + 视场角）编码为单个相机令牌：

$$(\mathcal{V}, \mathcal{T}) \to \{ (\mathbf{x}_i^{(1)}, \mathbf{x}_i^{(2)}, \cdots, \mathbf{x}_i^{(L)}, \mathbf{c}_i) \}$$

其中 $\mathbf{x}_i^{(j)}$ 为第 $i$ 帧的第 $j$ 个图像令牌，$\mathbf{c}_i$ 为对应的相机令牌。多视图令牌总数为：

$$(L + 1) \times (N + 1)$$

需要特别注意的是，查询图像的相机参数未知，因此其相机令牌被设为一个可学习的嵌入向量，而非由相机编码器计算得出。

### 2. 显式点图注入

为弥补多视图基础模型缺乏物体 3D 几何信息的缺陷，PoseGAM 引入了显式点图作为几何先验。对于每幅模板视图，从物体模型 $\mathcal{M}$ 渲染深度图，再利用相机内参反投影得到世界坐标下的点图 $\mathcal{P}$：

$$\mathrm{Object}~\mathcal{M} \stackrel{\mathcal{T}}{\to} \mathrm{Depth~Maps} \to \mathrm{Point~Maps}~\mathcal{P}$$

每幅点图 $P_i$ 随后通过一个轻量卷积网络映射为 $L$ 个点图令牌：

$$P_i \stackrel{\mathrm{Conv}}{\to} \{ \mathbf{p}_i^{(1)}, \mathbf{p}_i^{(2)}, \cdots, \mathbf{p}_i^{(L)} \}$$

### 3. 学习几何特征注入

除显式点图外，PoseGAM 还通过点云网络提取学习几何特征。首先利用掩码筛选有效像素，将点图、法线图、RGB 图拼接成逐视图点云：

$$\mathrm{PC}_i = \mathrm{concat}[P_i, O_i, I_i]_{M_i}$$

PTv3 点云网络处理该点云，为每个有效点输出一个特征向量。关键创新在于，这些点特征并不直接作为令牌送入 Transformer，而是按照像素坐标重投影回视图格式，形成几何特征图 $\mathcal{F} = \{ F_i \}$：

$$F_i(u, v) = \begin{cases} \mathbf{e}_i, & \text{if } (u, v) = (u_i, v_i) \\ 0, & \text{otherwise} \end{cases}$$

其中 $\mathbf{e}_i$ 为点 $(u_i, v_i)$ 对应的特征向量，该映射利用相机投影函数 $\pi(\mathbf{q}) = \mathrm{div}(K \mathbf{q})$ 将 3D 点反算到像素坐标。随后，几何特征图 $F_i$ 通过另一个轻量卷积网络编码为 $L$ 个几何特征令牌：

$$F_i \stackrel{\mathrm{Conv}}{\to} \{ \mathbf{f}_i^{(1)}, \mathbf{f}_i^{(2)}, \cdots, \mathbf{f}_i^{(L)} \}$$

### 4. 交叉注意力融合

上述点图令牌与几何特征令牌共同构成几何令牌集合。在 24 层 Fusion Transformer 中，多视图令牌作为查询（Query），几何令牌作为键值（Key-Value），通过交叉注意力机制注入几何信息：

$$\mathrm{CA}(Q \gets \mathbf{multiview~tokens}, KV \gets \mathbf{geometry~tokens})$$

这种设计有效弥合了 RGB 预训练与 3D 模态之间的鸿沟——消融实验证实，将点特征重投影为视图图格式并通过交叉注意力注入，显著优于直接使用原始点云令牌或简单相加融合（Table 5）。

### 5. 位姿解码

Fusion Transformer 输出的查询图像相机令牌被送入位姿解码头，预测相机到物体的变换 $T_{\mathrm{Obj}}^{\mathrm{Cam}}$。由于网络在归一化空间中运行，最终需通过缩放因子 $s$ 将预测结果转换回真实物体尺度：

$$T_{\mathrm{query}} = [\mathbf{R}, \mathbf{t}] = [\mathbf{R}_{\mathrm{norm}}, \frac{\mathbf{t}_{\mathrm{norm}}}{s}]$$

物体到相机的最终位姿 $T_{\mathrm{query}}$ 由矩阵求逆得到。

## 实验与关键发现

### 主实验结果

PoseGAM在BOP基准的5个核心数据集上与现有方法进行了系统比较。所有方法均**不使用细化网络（refinement）或多假设策略**，统一采用BOP标准平均召回率（AR）作为评价指标，AR定义为三个误差函数对应召回率的均值：

$$AR = (AR_{\mathrm{VSD}} + AR_{\mathrm{MSSD}} + AR_{\mathrm{MSPD}}) / 3$$

如Table 1所示，PoseGAM在5个数据集上取得了**41.1的平均AR**，超越此前最佳方法RayPose（39.1）约2.0个绝对百分点。各数据集表现分化明显：

- **TUD-L**：AR达到56.8，较RayPose（48.3）绝对提升8.5点，相对提升17.6%，为所有数据集中提升幅度最大者。
- **IC-BIN**：AR为24.3，较RayPose（21.8）提升2.5点。
- **YCB-V**：AR为47.4，较RayPose（46.2）提升1.2点。
- **LM-O**：AR为43.0，较RayPose（42.1）提升0.9点。
- **T-LESS**：AR为34.1，低于RayPose（36.9）约2.8点，是该数据集上唯一未超越的对比方法。

值得注意的是，PoseGAM在**无纹理物体数据集T-LESS上表现逊于RayPose**，可能原因在于T-LESS物体缺乏纹理信息，使得基于外观编辑的数据增强策略难以有效弥合渲染视图与真实查询之间的域差异。此外，PoseGAM在所有数据集上均显著优于传统基于特征匹配的方法（如**OSOP**、**ZS6D**、**MegaPose**、**GigaPose**、**FoundPose**等），验证了端到端前馈范式的优势。

定性比较（Figure 4）进一步展示了PoseGAM的位姿估计精度：在物体存在部分遮挡或外观变化时，PoseGAM的投影轮廓与查询图像中的物体掩码高度吻合，而对比方法常出现明显偏移。

![[assets/figures/papers/paper_list_l2058_https_arxiv_org_abs_2512_10840/figures/004_Figure_4.jpg]]
*Figure 4: Visual comparison with other methods. From left to right: the query image for pose estimation, object masks with each object shown in a distinct color, and the projection results of different methods after applying the estimated poses to the 3D object models. The projected 3D models are outlined with borders matching the colors of their corresponding masks*

### 消融实验

#### 输入模态的影响

Table 2系统消融了不同输入模态对位姿估计精度的贡献。以仅使用RGB渲染视图（V）和相机参数（T）为基线：

- **加入点图（P）**：低容错指标AUC@3从15.07跃升至25.94，AUC@30从74.01提升至80.26，证明显式点云几何信息对精确位姿估计至关重要。
- **进一步注入几何特征图（F）**：AUC@3提升至28.18，AUC@30达到84.30，表明学习到的几何特征与显式点图形成互补。
- **深度图（D）替代点图**：AUC@3仅16.82，远低于点图方案，说明世界坐标点图比深度图提供了更直接的3D空间约束。

#### 视图采样策略与数量

Table 3比较了不同视图采样策略和视图数量的影响：

- **FPS采样 vs 随机采样**：在10视图设置下，FPS采样AUC@3为28.18，随机采样仅为14.23，差距显著。FPS采样确保了对物体表面的全面覆盖，使网络能够充分感知物体几何。
- **视图数量**：视图数从10增至20时，AUC@3由28.18升至33.59，AUC@30由84.30升至87.36，表明更多视图可提供更密集的几何约束。

#### 微调策略

Table 4探索了不同预训练权重策略的影响：

- 从**VGGT权重初始化**可加速收敛并提升最终精度。
- **微调PTv3**（几何特征提取器）优于冻结其权重，说明让点云网络适应姿态估计任务是有益的。

#### 几何注入策略

Table 5系统比较了不同几何表示与注入方式的组合：

- **PTv3 + View Format + CrossAttn**为最佳组合，验证了将点云特征重投影为视图格式并通过交叉注意力注入的核心设计选择。
- 直接使用**VecSet**格式的原始点云令牌（无视图重排）效果显著下降，说明保持几何特征与视图之间的空间对应关系对多视图融合至关重要。
- 在VecSet中加入**纹理颜色信息**可将AUC@3提高约3.5点，表明外观信息对几何表示有一定补充作用。

### 失败模式分析

多视图基础模型对外观不一致输入的脆弱性是PoseGAM试图解决的核心问题。Figure 5的定性分析揭示了这一现象的严重性：

- 当仅输入渲染视图时，**VGGT**能预测一致的相机位姿，重建点云干净无离群值。
- 一旦加入从真实查询图像裁剪的区域，VGGT预测的查询视图位姿出现严重偏差，重建点云出现明显离散（红色边框标注区域）。

PoseGAM通过注入物体几何信息（点图与几何特征图）缓解了这一问题，但在以下场景仍存在局限：

- **无纹理物体**（如T-LESS）：外观信息匮乏，几何信息成为唯一线索，但渲染与真实之间的微小几何差异仍可能导致精度下降。
- **强反光或透明材质**：外观差异极大，点云重建质量可能受损，进而影响几何特征提取的准确性。
- **多物体遮挡场景**：当前方法仅针对单物体中心场景设计，尚未验证在密集遮挡下的鲁棒性。

### 计算成本与部署考量

PoseGAM模型参数量约**1.5B**，训练需4块A100 GPU约8天。推理阶段需已知相机内参及目标物体的分割掩码（实验中由CNOS提供），实际部署时需额外考虑分割模块的精度与延迟。对于实时应用场景，当前推理成本偏高，模型压缩与加速是未来工程化的重要方向。

![[assets/figures/papers/paper_list_l2058_https_arxiv_org_abs_2512_10840/figures/005_Table_1.jpg]]
*Table 1: Performance Comparisons on BOP Datasets. We report Average Recall (AR) scores on five BOP core datasets. All methods are evaluated without using refinement networks or multi-hypothesis strategies [30, 43]. The best results are shown in bold, and the secondbest results are underlined*

![[assets/figures/papers/paper_list_l2058_https_arxiv_org_abs_2512_10840/figures/006_Table_2.jpg]]
*Table 2: Ablation of input modalities. Comparison of network performance using different combinations of input modalities, including RGB images (V), camera poses (T ), point maps (P), depth maps (D), and geometric feature maps (F)*

![[assets/figures/papers/paper_list_l2058_https_arxiv_org_abs_2512_10840/figures/007_Table_3.jpg]]
*Table 3: Effect of view sampling strategy and number of views. Performance comparison across different strategies for camera poses sampling and varying numbers of rendered images*

![[assets/figures/papers/paper_list_l2058_https_arxiv_org_abs_2512_10840/figures/008_Table_4.jpg]]
*Table 4: Effect of finetuning strategy. Comparison of performance using different pretrained weight strategies*

## 定位与知识库关联

### 1. 范式迁移：从显式匹配到端到端前馈推理

PoseGAM 在未见物体姿态估计领域完成了一次清晰的范式迁移。传统方法的核心逻辑可归纳为“匹配+几何求解”两阶段流水线：首先在查询图像与物体模板渲染图之间建立2D-2D或2D-3D对应关系，再通过PnP等几何求解器恢复物体位姿。代表性工作包括：

- **基于对应关系的方法**：**OSOP** 和 **ZS6D** 依赖显式特征匹配来建立跨视图对应，匹配质量直接决定了后续几何求解的精度上限。
- **匹配后细化方法**：**MegaPose**、**GenFlow**（基于光流）、**GigaPose** 和 **FoundPose**（基于预训练特征）在初步匹配后引入细化网络，试图补偿匹配阶段的误差，但本质上仍受制于匹配可靠性的瓶颈。
- **基于多视图扩散的方法**：**RayPose** 作为前馈方法的先行者，利用扩散模型直接预测位姿，避免了显式匹配，但未充分利用物体的3D几何信息。

PoseGAM 的关键突破在于将问题重新定义为**端到端前馈多视图推理**：网络直接接收查询图像与多幅模板渲染图，联合输出物体的绝对位姿。这一设计消除了显式匹配步骤，使得梯度可以从位姿损失直接回传至视觉编码器，避免了匹配误差的累积放大效应（见 Eq. 1 和 Eq. 2）。在 BOP 核心数据集上，PoseGAM 的平均 AR 达到 41.1，超越此前最佳的 RayPose（39.1）达 5.1%（Table 1）。

### 2. 几何注入：弥合RGB预训练与3D模态的鸿沟

PoseGAM 的第二个核心贡献在于**将物体3D几何信息系统性地注入多视图网络**，这构成了其与现有多视图基础模型的关键分水岭。

**多视图基础模型的脆弱性**：以 **VGGT** 为代表的多视图基础模型虽然能够从多幅图像中预测相机位姿和3D结构，但其隐含假设所有输入视图共享一致的外观分布。当真实查询图像（具有复杂光照、遮挡和背景）与干净渲染视图混合输入时，VGGT 的重建点云出现显著离散（Figure 5），表明其对外观不一致极为敏感。PoseGAM 通过显式注入物体几何信息，使网络不再单纯依赖外观一致性来推断空间关系，从而从根本上规避了这一脆弱性。

**几何注入的双通道设计**：PoseGAM 采用两条互补路径将几何信息注入多视图 Transformer：

1. **显式点图通道**：从物体模型渲染深度图，经相机内参反投影得到世界坐标点图 $\mathcal{P}$（Eq. 7），再由轻量 CNN 编码为点图令牌（Eq. 8），通过交叉注意力作为 KV 输入（Eq. 6）。消融实验表明，仅添加点图即可将低容错指标 AUC@3 从 15.07 提升至 25.94（Table 2），证明显式3D坐标信息对精确对齐至关重要。

2. **学习几何特征通道**：使用点云网络 PTv3 提取逐点特征，按视图像素坐标重排为几何特征图 $\mathcal{F}$（Eq. 9, Eq. 12），再由 CNN 编码为特征令牌（Eq. 10）。这一“重投影为视图图”的策略（Table 5 中的 PTv3+View Format+CrossAttn 组合）被证明优于直接使用原始点云令牌或简单相加融合，因为它充分利用了多视图架构的预训练权重，同时通过交叉注意力机制弥合了 RGB 预训练与 3D 模态之间的表示鸿沟。

两者联合使用将 AUC@30 从 80.26 推升至 84.30（Table 2），验证了显式几何与学习几何的互补性。

### 3. 数据驱动：大规模合成数据的覆盖策略

PoseGAM 构建了包含 **19万个以上物体**的大规模合成数据集，这一规模远超此前工作的训练数据分布。数据构建策略体现了对泛化能力的系统性考量：

- **纹理标准化**：通过 Smart UV Unwrap 和纹理烘焙（整合 Diffuse、Glossy、Transmission 分量）将异构资产统一为规范的几何-外观表示（Section 4.1）。
- **四类渲染场景**：centric（中心视角）、uncentric（偏心视角）、变动光照和外观编辑（利用 FLUX.1-Canny-dev 进行纹理变换），覆盖了从理想条件到域偏移的广泛分布（Figure 3）。
- **视图采样策略**：采用球面 Hammersley 序列定义50个均匀分布的相机位姿，训练时使用 FPS（最远点采样）策略选取视图。消融实验表明，FPS 采样在 AUC@3 上达到 28.18，远超随机采样的 14.23（Table 3），证明全面覆盖物体表面对于位姿估计的鲁棒性至关重要。

### 4. 适用边界与已知局限

PoseGAM 的设计假设和实验设定定义了其当前的适用边界：

- **单刚体假设**：方法仅针对单个刚体物体的位姿估计，不支持非刚性物体、铰接物体或多物体场景的同时估计。Table 1 的评估均以单个物体中心的裁剪区域为输入。
- **输入依赖**：需要已知相机内参及目标物体的分割掩码（实验中由 CNOS 提供），在实际部署中这些前置条件可能不完全满足。
- **计算成本**：模型参数量约 1.5B，训练需 4 块 A100 GPU 约 8 天，推理计算成本较高，限制了在资源受限设备上的部署。
- **材质敏感性**：对于强反光或透明材质物体，因外观与渲染模板差异极大，精度可能显著下降（该点需在真实场景中进一步验证）。
- **场景复杂度**：当前数据集与评估以单物体、相对简洁的场景为主，尚未系统测试多物体遮挡或高度杂乱场景下的鲁棒性。

### 5. 开放问题与后续方向

从 PoseGAM 的局限出发，可识别以下开放研究问题：

1. **多物体扩展**：如何将端到端前馈框架扩展至多物体场景下的同时位姿估计，处理物体间的遮挡和交互？
2. **缩小域隙**：能否利用物理渲染（PBR）管线进一步缩小仿真与真实之间的外观差距，特别是在复杂材质（金属、玻璃）场景下？
3. **数据效率**：是否可以通过自监督学习或少样本微调减少对大规模合成数据的依赖，使方法能快速适配新物体？
4. **动态场景**：如何处理存在运动模糊或动态光照的查询图像？能否结合时序信息对视频中的物体进行平滑位姿跟踪？
5. **轻量化部署**：在保持几何感知能力的前提下，如何通过模型压缩或知识蒸馏降低推理成本，使方法适用于实时机器人应用？

## 原文 PDF

![[paperPDFs/CVPR_2026/PoseGAM_Robust_Unseen_Object_Pose_Estimation_via_Geometry_Aware_Multi_View_Reasoning.pdf]]
