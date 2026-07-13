---
title: "LASER: Layer-wise Scale Alignment for Training-Free Streaming 4D Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LASER_Layer_wise_Scale_Alignment_for_Training_Free_Streaming_4D_Reconstruction.pdf
project_link: "https://neu-vi.github.io/LASER/"
code_link: null
aliases:
- LASER
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
core_operator: 通过将深度图分割为离散的深度层，计算相邻窗口间每层的尺度因子，并沿时间轴与窗口间传播聚合这些尺度，从而纠正各层的非均匀缩放，实现训练无关的鲁棒流式对齐。（原文：layer-wise scale alignment, which segments depth predictions into discrete layers, computes per-lay...
primary_logic: 将经典的分层场景表示与现代前馈几何模型结合：在深度学习模型已经能够提供强局部几何的前提下，利用深度有序的层结构和基于图的尺度传播，可以有效将各窗口的输出统一为全局一致的长期重建，无需重新训练。（原文：Drawing on classical insights that scenes naturally decompose into depth-ordered layers with distinct geometric properties, we propose layer-wise scale alignment adapted to the modern deep learning reconstruction setting.）
claims:
- 仅使用全局Sim(3)对齐时，不同深度的表面会表现出层间尺度不一致，导致前景与背景的相对缩放出现错误。（原文 Fig.3 及 3.2 节）
- 所提出的逐层尺度对齐（LSA）在所有三个任务（深度估计、相机姿态估计、点图重建）上均显著优于现有流式方法和训练无关的并发工作 VGGT‑Long；使用 π³ 骨干时在 Sintel 上将绝对相对误差（Abs Rel）降至 0.247，比最佳流式基线 STream3Rβ 的 0.264 降低了 6.4%。
- 消融实验表明，去掉 LSA 会导致深度精度明显下降（Sintel Abs Rel 从 0.247 升至 0.328）；去掉时序传播（E_intra）会破坏非重叠帧的尺度一致性。
- Sintel (Video Depth) 上 Abs Rel ↓ = 0.247 (π³+Ours)
---

# LASER: Layer-wise Scale Alignment for Training-Free Streaming 4D Reconstruction

> [!tip] 核心洞察
> 将经典的分层场景表示与现代前馈几何模型结合：在深度学习模型已经能够提供强局部几何的前提下，利用深度有序的层结构和基于图的尺度传播，可以有效将各窗口的输出统一为全局一致的长期重建，无需重新训练。（原文：Drawing on classical insights that scenes naturally decompose into depth-ordered layers with distinct geometric properties, we propose layer-wise scale alignment adapted to the modern deep learning reconstruction setting.）

| 字段 | 内容 |
|------|------|
| 中文题名 | LASER：无需训练的流式4D重建逐层尺度对齐 |
| 英文题名 | LASER: Layer-wise Scale Alignment for Training-Free Streaming 4D Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.13680) · [Project](https://neu-vi.github.io/LASER/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation |
| Method | LASER |
| Dataset | Sintel, Bonn, KITTI, KITTI Odometry |

> [!tip] 效果简介
> - Sintel (Video Depth) 上，Abs Rel ↓ 0.247 (π³+Ours) vs 0.264 (STream3Rβ ) (-0.017 (‑6.4%))。
> - Bonn (Video Depth) 上，Abs Rel ↓ 0.048 (π³+Ours) vs 0.069 (STream3Rβ ) (-0.021 (‑30.4%))。
> - KITTI (Video Depth) 上，Abs Rel ↓ 0.054 (π³+Ours) vs 0.080 (STream3Rβ ) (-0.026 (‑32.5%))。

## 概要

**问题瓶颈**：单目深度估计固有的尺度模糊性，在流式（streaming）4D 重建中产生一个此前未被充分解决的深层矛盾——不同场景层（如前景与背景）的相对深度尺度，在不同时间窗口之间无法保持一致。即使采用全局 Sim(3) 变换进行窗口间对齐，也无法消除各层的各向异性缩放，导致融合后的重建出现可见扭曲和度量漂移。

**核心方法**：LASER 提出**逐层尺度对齐**（Layer-wise Scale Alignment, LSA），将深度预测分割为离散的深度层，计算相邻窗口间每层的独立尺度因子，并沿时间轴与窗口间关系图进行传播与聚合，从而纠正各层的非均匀缩放。该方法与冻结的前馈重建器（VGGT 或 π³）配合，以滑动窗口方式处理视频流，**无需任何训练或微调**。

**关键洞察**：将经典的分层场景表示与现代强局部几何先验相结合——在前馈模型已能提供可靠窗口内几何的前提下，利用深度有序的层结构和基于图的尺度传播，有效将各窗口输出统一为全局一致的长期重建。

**主要结果**：
- **深度估计**：在 Sintel 上 Abs Rel 降至 0.247（π³+LASER），比最佳流式基线 STream3Rβ 的 0.264 降低 6.4%；在 Bonn 和 KITTI 上分别降低 30.4% 和 32.5%。
- **相机姿态**：在 Sintel 上 ATE 仅为 0.061，比 STream3Rβ 的 0.213 降低 71.4%；在 KITTI 大规模里程计评估中，比同为训练无关的 VGGT‑Long 平均 ATE 降低约 27%。
- **点图重建**：在 7-Scenes 上 Mean Accuracy 降至 0.021，比 VGGT 离线模式（0.032）提升 34.4%。
- **效率**：在 RTX A6000 GPU 上以 14 FPS 运行，峰值内存仅 6 GB。

**方法定位**：LASER 属于训练无关的流式重建框架，位于离线前馈重建模型（VGGT/π³）与纯流式学习方法（Spann3R、CUT3R、STream3Rβ 等）之间，通过几何后处理弥合离线模型与流式需求之间的鸿沟。

### 从离线重建到流式 4D 重建

从单目视频中恢复稠密的 4D 几何（每帧的深度图与相机姿态，以及全局一致的点云）是计算机视觉的核心课题。近年来，前馈式重建模型取得了长足进展：**DUSt3R** 系列方法能够直接从图像对中预测稠密点图与相机姿态，而 **VGGT** 和 **π³** 等工作进一步将这一能力扩展到多帧联合推理，在离线设定下展现出令人瞩目的几何精度。然而，这些模型在设计上假设可以一次性访问全部帧，其计算复杂度与输入帧数呈超线性增长，难以直接部署到对实时性要求严苛的流式场景中。

将离线重建模型转化为流式系统的直接思路是滑动窗口：将视频流划分为重叠的时域窗口，在每个窗口内独立调用冻结的前馈重建器，再将各窗口的结果增量式地拼接到全局地图中。这一范式的代表是 **VGGT-Long**——它在每个窗口内运行 VGGT，然后通过全局 Sim(3) 变换（统一尺度、旋转和平移）将当前窗口的子地图对齐到世界坐标系。然而，这种策略隐含了一个关键假设：**同一窗口内所有像素的深度尺度是均匀的**。

### 核心瓶颈：层间尺度不一致

单目深度估计存在固有的尺度模糊性——模型在不同时间窗口内预测的深度值，其绝对尺度可能随窗口而变化。当相机平移运动有限时，这一问题尤为突出：前景与背景的相对深度尺度在不同窗口之间出现各向异性的漂移。**全局 Sim(3) 对齐对所有像素施加统一的缩放因子，无法纠正这种层间尺度差异**。

图 3 直观地展示了这一现象：经过全局 Sim(3) 对齐后，前景区域相对于背景结构在连续窗口之间表现出过度缩放或欠缩放。这种各向异性缩放会导致融合后的重建出现可见的扭曲和度量漂移——前景物体可能被系统性放大，而远处的墙壁则被压缩，破坏了全局几何一致性。

### 现有流式方法的局限

近年来涌现的流式重建方法试图从不同角度解决上述问题，但各自存在明显短板：

- **学习型流式方法**（如 **Spann3R** (Wang et al., CVPR 2025)、**CUT3R** (Wang et al., CVPR 2025)、**Point3R** (Wu et al., arXiv 2025)）通过空间记忆或持久状态来维持时序一致性，但需要针对流式设定重新训练或微调模型，无法直接复用日益强大的离线重建模型。
- **基于 VGGT 的流式变体**（如 **StreamVGGT** (Zhuo et al., arXiv 2025)、**VGGT-SLAM**）通过因果注意力或 token 池化使 VGGT 适应流式输入，但受限于 VGGT 自身的窗口内推理能力，且仍面临层间尺度不一致的困扰。
- **训练无关的 VGGT-Long** 虽然无需重新训练即可将离线模型用于流式场景，但其全局 Sim(3) 对齐策略无法处理层间尺度的各向异性，导致长序列下的累积误差。

### 本文动机：将分层场景先验注入现代前馈重建

一个关键的洞察是：**自然场景天然组织为深度有序的层结构，不同层具有相对独立的几何属性**。这一经典认知在传统三维视觉中被广泛利用，但在现代深度学习重建范式中却被忽视。LASER 的核心动机正是弥合这一鸿沟——在深度学习模型已经能够提供强局部几何的前提下，通过显式建模深度层的尺度变化，将各窗口的输出统一为全局一致的长期重建，**无需任何重新训练或微调**。

具体而言，LASER 提出**逐层尺度对齐（Layer-wise Scale Alignment, LSA）**：将深度图分割为离散的深度层，为每一层独立估计尺度因子，并通过层图结构沿时间轴与窗口间传播和聚合这些尺度，从而纠正各层的非均匀缩放。这一设计使得 LASER 能够作为通用框架，将任意离线重建模型（如 VGGT 或 π³）无缝转换为流式系统，在保持 14 FPS 实时性和 6 GB 峰值内存的同时，显著超越现有学习型流式方法和训练无关基线。

## 核心方法与创新机理

### 问题瓶颈：层间尺度不一致

现有的训练无关流式重建方法（如 **VGGT‑Long**）在滑动窗口间采用全局 Sim(3) 对齐，对所有像素施加统一的缩放因子。然而，由于前馈单目模型的固有尺度模糊性，不同深度层（前景与背景）的相对尺度在不同时间窗口间存在显著差异——尤其是在相机平移受限的场景中，这种各向异性缩放无法被单一的全局变换所消除。结果表现为：融合后的重建中，前景区域相对于背景结构出现过度缩放或欠缩放，产生可见的扭曲与度量漂移（图 3）。

### 核心洞察：分层场景表示与现代前馈几何的融合

LASER 的核心洞察在于将经典的分层场景理解与现代深度学习几何重建相结合。场景天然可以分解为具有不同几何属性的深度有序层，而当前的前馈模型（如 VGGT、π³）已经能够为每个局部窗口提供强几何先验。利用这一先验，通过对深度层进行独立尺度估计，并沿时间轴与窗口间传播这些尺度，可以有效将各窗口的输出统一为全局一致的长期重建——全程无需重新训练或微调。

### 关键创新点：逐层尺度对齐（Layer-wise Scale Alignment, LSA）

LASER 的核心创新在于用**逐层尺度对齐**替代全局 Sim(3) 变换，解决了层间各向异性缩放问题。该机制包含三个关键步骤：

1. **深度层提取与图构建**：将 Sim(3) 初步对齐后的伪深度图分割为空间连贯的离散深度层，并以层为节点构建有向图。图中包含两类边——连接相邻窗口重叠时间戳上相同深度层的窗口间边（E_inter），以及连接同一窗口内相邻帧相同层的窗口内时序边（E_intra），边权重由层间交并比（IoU）定义。

2. **逐层尺度估计**：在窗口间边上，对每一层独立地通过 Huber‑robust IRLS 优化，从重叠区域的深度对应中估计最优层尺度因子，而非对所有层使用统一缩放。

3. **尺度传播与聚合**：沿图的窗口间边和时序边传播父节点的平均尺度，最终以 IoU 为权重进行加权平均，为每个像素生成精细化的尺度校正。

### Changed Slots：与基线方法的关键差异

| 设计维度 | 基线方法（VGGT‑Long 等） | LASER 方案 | 创新性质 |
|---------|----------------------|-----------|---------|
| **窗口间对齐方法** | 全局 Sim(3) 变换，所有像素统一缩放 | 逐层尺度对齐（LSA）：深度层分割 → 独立尺度估计 → 图传播聚合 | 核心创新 |
| **相似变换估计策略** | IRLS 联合优化尺度 s 与刚性变换 R, t | 两阶段解耦：先 IRLS 估计全局尺度 s，再基于缩放后的相机锚点用 Kabsch 算法求 R, t | 稳定性改进 |
| **刚性变换输入源** | 使用缩放后的点图（点云）估计 SE(3) | 使用由相机姿态直接推导的最小相机锚点，避免点图预测伪影 | 轨迹一致性改进 |

### 消融验证

消融实验直接验证了上述创新的必要性：
- **去掉 LSA**（wo/ LSA）：Sintel 深度 Abs Rel 从 0.247 升至 0.278，Bonn 从 0.048 升至 0.113，证实逐层尺度校正是精度提升的核心来源。
- **去掉时序传播**（wo/ E_intra）：仅保留窗口间边而忽略非重叠帧间的尺度关系，导致长序列的全局一致性受损。
- **去掉 IRLS 尺度估计**（w/o IRLS）：用闭式解替代鲁棒 IRLS 会严重恶化深度和姿态精度，说明配准阶段的鲁棒估计至关重要。
- **去掉相机锚点**（w/o Anchor）：改用缩放后的点图进行刚性配准，导致 Sintel 旋转误差 RPE_rot 从 0.249 急剧升至 0.742，验证了基于相机姿态的最小锚点对保持轨迹一致性的必要性。

LASER 是一个**无需训练**的流式框架，将任意离线 4D 重建模型转换为在线流式系统。其核心流水线由三个递进阶段构成：**滑动窗口帧分组与局部重建**、**子地图到全局地图的 Sim(3) 配准**，以及**逐层尺度对齐（LSA）**。整个流程沿时间轴增量执行，每到达一个新窗口，系统便将其融合到持续增长的全局地图中，无需回看全部历史帧。

### 滑动窗口与局部重建

给定视频流，LASER 将帧序列划分为重叠的时域窗口。第 $i$ 个窗口定义为：

$$\mathcal{W}_i = \{ t \mid a_i \leq t < a_i + L \}$$

其中 $L$ 为窗口长度（默认 20 帧），$a_i$ 为窗口起始帧索引，相邻窗口重叠 $O$ 帧（默认 5 帧）。在每个窗口内，冻结的前馈重建器 $f$ 直接输出每帧的稠密点图、相机姿态和置信度：

$$f(\{\mathbf{I}_t\}, \mathcal{W}_i) = \{ (\mathbf{P}_t^{(i)}, \mathbf{T}_t^{(i)}, \mathbf{C}_t^{(i)}) \mid a_i \leq t < a_i + L \}$$

LASER 可实例化于不同骨干模型，论文中使用 **VGGT** 和 **π³** 两种离线重建器，均保持冻结状态，无需任何微调。

### 子地图构建与全局 Sim(3) 初步对齐

获得窗口内的逐帧预测后，LASER 将各帧的点图变换到统一的窗口坐标系，构建局部子地图 $S_i$。随后，系统通过两阶段策略将 $S_i$ 配准到全局地图 $G_{i-1}$：

1. **全局尺度估计**：从当前窗口与全局地图在重叠帧上的高置信度点对应中，使用 Huber-鲁棒的 IRLS（迭代重加权最小二乘）优化全局尺度因子 $s_i^w$。
2. **刚性变换估计**：基于缩放后的相机锚点（而非点图），通过 Kabsch 算法求解最优旋转 $\mathbf{R}_i^w$ 和平移 $\mathbf{t}_i^w$。

这一设计（见补充材料第 7 节）相比 VGGT-Long 的联合优化策略更稳定：分离尺度与刚性估计，并使用相机锚点替代点图作为刚性配准源，有效避免了点图预测伪影对轨迹一致性的破坏。

### 逐层尺度对齐（LSA）

全局 Sim(3) 对齐施加统一缩放，无法消除不同深度层之间的各向异性尺度差异——这是单目尺度模糊在流式场景下的核心瓶颈（见 Figure 3）。LSA 模块正是为解决此问题而设计：

1. **深度层提取**：将 Sim(3) 对齐后的伪深度图分割为空间连贯的离散深度层。
2. **层图构建**：以深度层为节点，构建包含两类边的有向图——连接相邻窗口重叠帧上同一深度层的 **窗口间边**（$\mathcal{E}_{\mathrm{inter}}$），以及连接同一窗口内相邻帧的 **窗口内时序边**（$\mathcal{E}_{\mathrm{intra}}$）。边的权重为层间 IoU，仅当 IoU 超过阈值 $\tau$ 时建立连接。
3. **逐层尺度估计与传播**：在窗口间边上，对每层用 Huber-鲁棒 IRLS 从深度对应中估计该层的尺度因子；随后沿图的所有边传播并加权聚合（权重为 IoU），得到每层的最终尺度。
4. **点图调整与全局更新**：将各像素的层尺度应用于已对齐的点图，更新全局地图 $G_i$。

### 效率特性

整个流水线在单张 RTX A6000 GPU 上以 **14 FPS** 运行，峰值内存仅 **6 GB**（Figure 5）。各模块的运行时分解（Figure 8）表明，前馈重建器是主要计算瓶颈，LSA 与子地图配准的额外开销相对较小，保持了流式处理的实时性。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2512_13680/figures/002_Figure_2.jpg]]
*Figure 2: Overview of LASER. LASER converts an offline reconstruction model to a streaming version without retraining. Given a video stream, we process frames in overlapping temporal windows with a frozen feed-forward reconstructor. We incrementally register the submap to the global map with Sim(3) estimation and the proposed layer-wise scale alignment*

### 3.1 滑动窗口与子地图构建

LASER 将输入视频流划分为重叠的时域窗口。第 $i$ 个窗口 $\mathcal{W}_i$ 包含 $L$ 个连续帧，起始帧索引为 $a_i$：

$$\mathcal{W}_i = \{ t \mid a_i \leq t < a_i + L \}$$

在每个窗口内，使用冻结的前馈重建器 $f$（如 VGGT 或 $\pi^3$）为每一帧 $t$ 输出稠密点图 $\mathbf{P}_t^{(i)}$、相机姿态 $\mathbf{T}_t^{(i)}$ 和置信度 $\mathbf{C}_t^{(i)}$：

$$f(\{\mathbf{I}_t\}, \mathcal{W}_i) = \{ (\mathbf{P}_t^{(i)}, \mathbf{T}_t^{(i)}, \mathbf{C}_t^{(i)}) \mid a_i \leq t < a_i + L \}$$

将每帧的点图变换到窗口坐标系，形成局部子地图 $\mathcal{S}_i$。随后，通过全局 Sim(3) 估计将 $\mathcal{S}_i$ 配准到世界坐标系下的全局地图 $\mathcal{G}_{i-1}$，并渐进更新：

$$\mathcal{G}_{i} = \mathcal{G}_{i-1} \cup \{ \mathbf{T}_{t}^{w} \mathbf{P}_{t}^{(i)} \}$$

其中 $\mathbf{T}_t^w$ 为世界坐标系下的相机姿态。全局 Sim(3) 对齐分两阶段进行：先用 IRLS（迭代重加权最小二乘）从高置信度点对应中估计全局尺度 $s_i^w$：

$$s_i^w = \underset{s > 0}{\arg\min} \sum_{(\mathbf{p},\mathbf{q})\in\mathcal{C}} \rho(\| s\mathbf{p} - \mathbf{q}\|_2)$$

其中 $\rho(\cdot)$ 为 Huber 损失，$\mathcal{C}$ 为窗口重叠区域内的点对应集合。然后，基于缩放后的相机锚点集合 $\mathbf{x}_t$ 与前一窗口的锚点 $\mathbf{y}_t$，用 Kabsch 算法求解最优刚性变换：

$$\mathbf{R}_i^w, \mathbf{t}_i^w = \arg\min_{\mathbf{R}\in SO(3),\mathbf{t}\in\mathbb{R}^3} \sum_{t\in\mathcal{O}_i} \| \mathbf{R}\mathbf{x}_t + \mathbf{t} - \mathbf{y}_t \|_2^2$$

其中 $\mathcal{O}_i$ 为窗口 $i-1$ 与 $i$ 的重叠帧集合。使用相机锚点而非缩放后的点图进行刚性配准，可避免点图预测伪影对轨迹一致性的干扰（消融实验证实，替换为点图会使 Sintel 旋转 RPE 从 0.249 升至 0.742）。

### 3.2 逐层尺度对齐（LSA）

**问题根源**：全局 Sim(3) 对齐对所有像素施加统一缩放，无法消除单目尺度模糊引起的层间各向异性缩放——前景与背景的相对深度尺度在不同窗口间不一致，导致融合重建出现扭曲和度量漂移（见 Figure 3）。

**核心思路**：将 Sim(3) 对齐后的伪深度图分割为离散的深度层，为每层独立估计尺度因子，并通过层图传播与聚合，纠正各层的非均匀缩放。

**深度层图构建**：以深度层为节点，构建有向图，包含两类边：
- **窗口间边** $\mathcal{E}_{\mathrm{inter}}$：连接相邻窗口在重叠时间戳上的深度层，要求层间 IoU 大于阈值 $\tau$：
  $$\mathcal{E}_{\mathrm{inter}} = \{ ( \mathcal{L}_{t,m}^{(i-1)}, \mathcal{L}_{t,n}^{(i)} ) \mid \operatorname{IoU}( \mathcal{L}_{t,m}^{(i-1)}, \mathcal{L}_{t,n}^{(i)} ) > \tau, t \in \mathcal{O}_{i} \}$$
- **窗口内时序边** $\mathcal{E}_{\mathrm{intra}}$：连接同一窗口内相邻帧的相同深度层，编码时序连续性：
  $$\mathcal{E}_{\mathrm{intra}} = \{ ( \mathcal{L}_{t-1,m}^{(i)}, \mathcal{L}_{t,n}^{(i)} ) \mid \operatorname{IoU}( \mathcal{L}_{t-1,m}^{(i)}, \mathcal{L}_{t,n}^{(i)} ) > \tau, t \in \mathcal{W}_{i} \}$$

**逐层尺度估计**：在窗口间边上，对每层 $\mathcal{L}_{t,n}^{(i)}$ 用 Huber-robust IRLS 从深度对应中估计最优尺度因子：

$$\hat{s}_{t,n}^{(i)} = \arg \min_{s>0 \atop (d_{p}, d_{q}) \in \mathcal{C}_{t,n}^{(i)}} \rho( \| s d_{p} - d_{q} \| )$$

其中 $\mathcal{C}_{t,n}^{(i)}$ 为该层在重叠区域的深度对应集合。

**尺度传播与聚合**：沿图的窗口间边和时序边传播父节点的平均尺度，并以 IoU 为权重进行加权平均，得到每层的最终尺度因子。将各像素的尺度应用于已对齐的点图，更新全局地图。

**消融验证**：完全去掉 LSA 后，Sintel Abs Rel 从 0.247 升至 0.278，Bonn 从 0.048 升至 0.113，证实 LSA 对缓解层间尺度不一致的关键作用。去掉时序传播边（$\mathcal{E}_{\mathrm{intra}}$）会忽略非重叠帧之间的尺度关系，导致长序列全局一致性受损。

## 实验与关键发现

### 核心实验设置

LASER 是一个训练无关（training‑free）的流式框架，其实验评估旨在回答三个问题：(1) 在不重新训练的前提下，能否超越现有的有训练流式方法？(2) 逐层尺度对齐（LSA）对缓解层间尺度不一致是否关键？(3) 框架的各个设计选择如何影响精度与效率？

为公平对比，所有方法均在单张 RTX A6000 GPU 上测量 FPS 与峰值内存，前馈模型使用统一的输入分辨率（VGGT 输入 518×294，DUSt3R 输入 512×288）。在长时间点图评估中，所有方法均过滤掉置信度最低的 40% 点以缓解天空和远背景伪影。在 KITTI 里程计大规模评估中，沿用与 VGGT‑Long 相同的回环检测配置以保证公平性。

### 视频深度估计

Table 1 报告了在 Sintel、Bonn 和 KITTI 三个数据集上的视频深度估计结果。LASER 使用 π³ 骨干时，在 Sintel 上取得 Abs Rel 0.247，比最佳流式基线 **STream3Rβ** 的 0.264 降低了 6.4%；在 Bonn 上 Abs Rel 为 0.048，比 STream3Rβ 的 0.069 降低 30.4%；在 KITTI 上 Abs Rel 为 0.054，比 STream3Rβ 的 0.080 降低 32.5%。即使在 VGGT 骨干下，LASER 也一致优于所有流式方法，验证了训练无关对齐策略的泛化能力。

**关键发现：** LASER 在三个不同场景类型（合成、室内、室外驾驶）上均取得最低的 Abs Rel，且优势在真实场景（Bonn、KITTI）上更为显著，说明 LSA 对真实世界中复杂的层间尺度不一致具有更强的纠正能力。

### 相机姿态估计

Table 2 报告了小规模数据集上的姿态估计结果。LASER（π³）在 Sintel 上取得 ATE 0.061，比 STream3Rβ 的 0.213 降低 71.4%；在 ScanNet 和 TUM 上也一致优于所有流式基线。值得注意的是，LASER 在平移和旋转 RPE 上均显著领先，表明逐层尺度对齐不仅改善了深度精度，也间接提升了相机轨迹的全局一致性。

Table 3 进一步展示了公里级 KITTI 里程计上的大规模姿态估计。LASER（π³+Ours）的平均 ATE 为 24.17，比训练无关的并发工作 **VGGT‑Long** 的 33.12 降低 27.0%（排除高速序列后降幅为 12–21%）。这验证了 LSA 在长序列、大尺度场景下对累积漂移的有效抑制。

### 点图重建

Table 4 报告了室内短期多视图点图估计结果。LASER（VGGT+Ours）在 7‑Scenes 上取得 Mean Accuracy 0.021，甚至优于离线 VGGT 的 0.032（降低 34.4%），说明逐层对齐不仅弥补了流式处理的精度损失，反而通过纠正层间尺度不一致提升了重建质量。在 NRGBD 上，LASER 同样在 Accuracy、Completeness 和 Normal Consistency 三项指标上全面领先。

Table 7 展示了 Waymo 室外长期点图估计结果。LASER 在平均 Chamfer Distance 上显著优于 VGGT‑Long，进一步证明了 LSA 在动态室外场景下的鲁棒性。

### 效率分析

Figure 5 综合对比了各方法的 FPS、峰值内存和姿态误差。LASER 以 14 FPS 运行，峰值内存仅 6 GB，在精度‑效率曲线上形成明显的帕累托前沿——精度远超所有流式方法，同时内存消耗远低于基于全局优化的 VGGT‑SLAM 等方案。Figure 8 的运行时分解显示，前馈推理占据主要耗时，而 LSA 模块本身十分轻量，不会成为吞吐瓶颈。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2512_13680/figures/015_Figure_8.jpg]]
*Figure 8: Runtime analysis of each module within the pipeline*

### 消融实验

#### 逐层尺度对齐（LSA）的核心作用

Table 5 的消融实验直接验证了 LSA 的关键性。完全去掉 LSA（wo/ LSA）导致 Sintel Abs Rel 从 0.247 升至 0.278，Bonn 从 0.048 升至 0.113，深度精度显著恶化。去掉时序传播边（wo/ E_intra）仅保留窗口间边，会忽略非重叠帧之间的尺度关系，导致长序列的全局一致性受损。这证实了 LSA 中“窗口间边 + 时序边”的双重图结构对维持全局尺度一致性的必要性。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2512_13680/figures/008_Table_5.jpg]]
*Table 5: Ablation Studies for Layer-wise Scale Alignment (Sec. 3.2). wo/ LSA denotes not using LSA component. w/ SAM 2 denotes replacing the efficient segmentation algorithm [11] with a recent counterpart SAM 2. wo/*

#### 深度层分割策略

Table 5 还显示，将高效分割算法替换为 **SAM 2** 并未进一步改善结果，表明当前基于深度有序的分割策略已足够有效，且保持了轻量性。Table 6 对 IoU 阈值 τ 的消融表明，τ 在合理范围内对精度影响不敏感，默认值提供了良好的层间对应鲁棒性。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2512_13680/figures/009_Table_6.jpg]]
*Table 6: Ablation on LSA (Sec. 3.2)’s IoU threshold τ*

#### 子地图配准设计

Table 8 和 Figure 10 消融了子地图配准阶段的关键设计。用闭式解代替 IRLS 估计尺度（w/o IRLS）会严重恶化深度和姿态精度，验证了 Huber‑robust IRLS 在处理离群点对应时的必要性。用缩放后的点图代替相机锚点（w/o Anchor）会导致旋转误差急剧增大（Sintel RPE_rot 从 0.249 升至 0.742），说明基于相机姿态的最小锚点对于保持轨迹一致性至关重要——点图预测中的局部伪影会污染刚性变换估计。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2512_13680/figures/017_Table_8.jpg]]
*Table 8: Ablation Studies for Submap Registration (Sec. 7). w/o IRLS denotes estimating scale via closed-form solution instead of IRLS. w/o Anchor denotes estimating rigid transformation on scaled point maps instead of scaled camera anchors*

#### 窗口超参数

Figure 7 显示窗口大小 L 在 10–30 范围内鲁棒，默认 L=20 在局部几何质量和计算效率之间取得良好平衡。Figure 9 显示窗口重叠量 O 在 2–10 范围内对精度影响较小，默认 O=5 提供了足够的层间对应信息。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2512_13680/figures/013_Figure_7.jpg]]
*Figure 7: Ablation on window size L. In default, we use L = 20*

### 失败模式与局限性

Figure 12 展示了 LASER 的典型失败案例，主要集中在动态场景。当前深度层图构建仅基于逐帧深度预测，缺乏对象级别的持久上下文，导致：(1) 多个独立运动的物体可能被分配到同一深度层，使层尺度估计受到运动物体的污染；(2) 当物体完全遮挡后重新出现时，层间对应关系无法恢复，导致该物体的尺度传播中断。这些失败模式本质上受限于底层前馈重建器对动态/非刚性场景的处理能力，LASER 作为训练无关框架无法从根本上弥补这一缺陷。

此外，框架的超参数（窗口大小、重叠比例、置信度阈值）需要针对室内/室外不同环境手动调节，缺乏自适应性，这在实际部署中增加了调参负担。

## 定位与知识库关联

### 1. 与流式前馈重建方法的关系

LASER 的核心定位是 **训练无关的流式框架**，它不引入任何可学习参数，而是将冻结的离线重建模型转换为流式系统。这一设计使其与当前主流的流式方法形成了清晰的边界。

**与基于记忆的流式方法对比。** **Spann3R** (Wang et al., CVPR 2025) 和 **CUT3R** (Wang et al., CVPR 2025) 分别通过空间记忆和持久状态实现流式重建，**Point3R** (Wu et al., arXiv 2025) 则采用显式空间指针记忆。这些方法的核心策略是在模型内部维护一个可学习的记忆状态，以跨窗口传递几何信息。LASER 采取了截然不同的路径：它完全依赖冻结模型在每个窗口内的局部预测质量，将跨窗口一致性的责任转移到后处理对齐模块上。这一选择带来了两个直接后果：（1）无需重新训练或微调，可直接受益于任何离线模型的进步；（2）对齐模块的设计成为性能瓶颈——这正是逐层尺度对齐（LSA）所要解决的核心问题。

**与 VGGT 流式变体的对比。** **VGGT-SLAM** 将 VGGT 与 SLAM 优化结合，**StreamVGGT** (Zhuo et al., arXiv 2025) 通过因果注意力或 token 池化使 VGGT 适应流式输入。这些方法或引入额外的优化循环，或修改模型内部结构。LASER 最直接的对比对象是 **VGGT-Long**——同样采用训练无关的滑动窗口策略，但仅使用全局 Sim(3) 对齐。LASER 的关键改进在于识别并解决了全局 Sim(3) 对齐的固有限制：单目尺度模糊导致不同深度层的相对尺度在不同时间窗口间不一致，全局统一缩放无法消除这种各向异性缩放。这一洞察直接催生了逐层尺度对齐（LSA）模块。

**与其他滑动窗口方法的对比。** **STream3Rβ**、**WinT3R** 和 **TTT3R** 均采用滑动窗口策略，但各自引入了不同的对齐或自适应机制。LASER 在实验上对这些方法展现出显著优势：在 Sintel 深度估计上，π³+LASER 的 Abs Rel 为 0.247，优于 STream3Rβ 的 0.264（降低 6.4%）；在 Sintel 相机姿态估计上，ATE 为 0.061，远低于 STream3Rβ 的 0.213（降低 71.4%）。这表明，训练无关的逐层尺度对齐策略在精度上可以超越专门训练的流式方法。

### 2. 方法适用边界

**对骨干模型质量的强依赖。** LASER 的性能直接受限于底层前馈重建器的能力。当骨干模型（VGGT 或 π³）能够提供高质量的局部几何预测时，LSA 可以有效纠正层间尺度不一致，实现全局一致重建。然而，当骨干模型本身在动态或非刚性场景下失效时，LASER 同样无法产生可靠结果。图 Figure 12 明确展示了动态场景下的失败案例，说明框架本身并不具备处理动态物体的独立机制。

**超参数的环境敏感性。** 框架需要针对室内/室外不同环境手动调节超参数，包括窗口大小 L（默认 20）、重叠量 O（默认 5）、置信度阈值等。消融实验表明，窗口大小在 10–30 范围内、重叠量在 2–10 范围内对精度影响较小，但这些结论是在特定数据集上获得的。在实际部署中，不同场景可能需要不同的参数配置，而框架缺乏自适应性。

**LSA 在复杂场景和遮挡下的脆弱性。** 当前深度层图构建仅基于逐帧深度预测，缺乏对象级别的持久上下文。这导致两个问题：（1）多个独立物体可能被分配到同一深度层，使得层尺度估计被不相关物体的深度值污染；（2）当物体完全遮挡后重新出现时，层间对应关系无法恢复，导致该物体的尺度传播链条中断。这些问题在包含大量前景物体交互或频繁遮挡的场景中尤为突出。

### 3. 局限性与开放问题

**局限性 1：超参数自适应缺失。** 框架需要针对不同环境手动调节超参数，缺乏自动感知场景特性并调整参数的能力。一个直接的改进方向是引入轻量级的场景分析模块，根据运动幅度、深度分布等特征动态调整窗口大小和重叠量。

**局限性 2：动态与非刚性场景处理能力受限于骨干模型。** 随着离线重建模型的进步——特别是那些能够处理动态场景或非刚性运动的新模型——LASER 如何更好地利用这些能力仍是一个开放问题。当前框架的对齐模块假设场景是静态的，动态物体的存在会破坏层间对应关系的可靠性。

**局限性 3：LSA 缺乏对象级持久上下文。** 当前仅基于逐帧深度预测的层分割策略无法追踪跨时间的物体身份。引入原始图像的外观信息来增强 LSA 的鲁棒性是一个有前景的方向：外观特征可以帮助区分不同物体、维持遮挡后的身份连续性，从而提高层间对应的准确性和时序追踪能力。

**开放问题 1：如何实现不同环境下超参数的自适应调整，提高框架的通用性？** 这涉及场景复杂度估计、运动模式识别和计算资源感知的动态参数选择。

**开放问题 2：随着离线重建模型的进步，LASER 如何更好地利用动态场景或非刚性运动的处理能力？** 这可能需要重新设计对齐模块，使其能够区分静态背景和动态前景，并分别处理其尺度一致性。

**开放问题 3：能否通过引入原始图像的外观信息来增强 LSA 在复杂场景和严重遮挡下的鲁棒性与时序追踪能力？** 这涉及将视觉特征与几何深度层融合，构建更稳定的跨窗口对应关系。

## 原文 PDF

![[paperPDFs/CVPR_2026/LASER_Layer_wise_Scale_Alignment_for_Training_Free_Streaming_4D_Reconstruction.pdf]]
