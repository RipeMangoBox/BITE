---
title: "V-DPM: 4D Video Reconstruction with Dynamic Point Maps"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/V_DPM_4D_Video_Reconstruction_with_Dynamic_Point_Maps.pdf
project_link: "https://www.robots.ox.ac.uk/~vgg/research/vdpm/"
code_link: null
aliases:
- VD
- V-DPM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入时间不变点图集合 Q = {P_i(t_j, π₀)} 和时间条件解码器（自适应LayerNorm），使网络能够从主干生成的时间可变点图 P 中推断运动并预测任意参考时间戳下的3D点云。这一设计建立了跨时间的像素对应，直接实现场景流的密集恢复，同时避免了成对后优化，赋予模型一次性多帧4D重建的能力。"
primary_logic: 将4D重建分解为两个连续阶段：首先生成时间可变但视角不变的点图（易于从静态主干微调获得），再通过轻量的时间条件解码器将其对齐到统一时间戳，从而获得时间-视角完全不变的点图。这种两阶段设计使得预训练的静态3D重建网络（VGGT）只需少量合成数据微调即可转化为强大的4D重建器，大幅降低了对4D标注数据的需求和训练成本。
claims:
- 在4D重建2‑View EPE任务上，V-DPM的误差约为DPM和St4RTrack的1/5，在所有四个动态数据集上显著超越先前方法。
- 在10帧视频密集追踪EPE上，V-DPM保持与2‑View相近的性能，而DPM误差大幅上升；V-DPM产生的运动轨迹更平滑、自洽。
- 在视频深度估计（AbsRel）上，V-DPM在Sintel/Bonn数据集上远超MonST3R等前馈方法，仅落后于并发工作π³。
- 网络设计消融证明完整的时间条件解码器（深度4 + adaLN）对性能至关重要，简化设计（深度2、加法条件、直接DPT解码器）均导致动态点图误差上升。
---

# V-DPM: 4D Video Reconstruction with Dynamic Point Maps

> [!tip] 核心洞察
> 将4D重建分解为两个连续阶段：首先生成时间可变但视角不变的点图（易于从静态主干微调获得），再通过轻量的时间条件解码器将其对齐到统一时间戳，从而获得时间-视角完全不变的点图。这种两阶段设计使得预训练的静态3D重建网络（VGGT）只需少量合成数据微调即可转化为强大的4D重建器，大幅降低了对4D标注数据的需求和训练成本。

| 字段 | 内容 |
|------|------|
| 中文题名 | V-DPM：基于动态点图的4D视频重建 |
| 英文题名 | V-DPM: 4D Video Reconstruction with Dynamic Point Maps |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.09499) · [Project](https://www.robots.ox.ac.uk/~vgg/research/vdpm/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | V-DPM |
| Dataset | PointOdyssey / Kubric-F / Kubric-G / Waymo, Sintel, Bonn |

> [!tip] 效果简介
> - PointOdyssey / Kubric-F / Kubric-G / Waymo (2-View 4D) 上，EPE (平均) 约0.03 ~ 0.05 vs DPM: 约0.15 ~ 0.20; St4RTrack: 类似 (误差降低约5倍)。
> - PointOdyssey / Kubric-F / Kubric-G / Waymo (10帧追踪EPE) 上，平均EPE 与2-View相近的低误差 vs DPM: 误差大幅上升 (V-DPM在长序列上保持高精度，DPM性能下降显著)。
> - Sintel (视频深度) 上，AbsRel ↓ 0.247 vs MonST3R: 1.196; DPM: 0.399 (较MonST3R降低79.4%)。

## 概要

从视频中同时恢复场景的3D几何、运动和相机参数是计算机视觉的核心挑战。现有前馈重建方法大多依赖静态点图表示，假设场景静止，无法直接捕捉3D运动（场景流）。即使部分工作将点图扩展至动态场景，也仅能预测时间可变的点图，缺乏时间不变性，必须借助2D跟踪器等额外组件才能恢复密集4D对应；而成对动态点图方法处理多视图时则需要昂贵的后优化。这导致端到端多视图4D重建在准确性和计算效率上均受到限制。

**V-DPM** 提出将4D重建分解为两个连续阶段：首先生成时间可变但视角不变的点图，再通过轻量的时间条件解码器将其对齐到统一时间戳，从而获得时间-视角完全不变的点图。这一设计使得预训练的静态3D重建网络（**VGGT**, Wang et al., CVPR 2025）只需少量合成数据微调即可转化为强大的4D重建器，大幅降低了对4D标注数据的需求和训练成本。

核心结论如下：
- **4D重建精度大幅领先**：在两视图4D重建任务上，V-DPM的EPE误差约为**DPM**（Sucar et al., ICCV 2025）和**St4RTrack**（Feng et al., ICCV 2025）的1/5，在所有四个动态数据集上显著超越先前方法。
- **长序列追踪保持高精度**：在10帧视频密集追踪EPE上，V-DPM保持与两视图相近的低误差，而DPM误差大幅上升；V-DPM产生的运动轨迹更平滑、自洽。
- **视频深度估计显著提升**：在Sintel和Bonn数据集上，V-DPM的深度AbsRel远超**MonST3R**（Zhang et al., arXiv 2024）等前馈方法（Sintel: 0.247 vs 1.196; Bonn: 0.057 vs 0.777）。
- **设计消融验证关键模块**：完整的时间条件解码器（深度4层 + 自适应LayerNorm）对性能至关重要，简化设计均导致动态点图误差上升。

在方法谱系上，V-DPM处于静态多视图重建与动态场景理解的交叉点：它以VGGT的交替注意力架构为骨架，继承其强大的静态几何推理能力，同时引入动态点图表示和时间条件解码机制，实现了从静态到动态的平滑扩展。与仅恢复静态几何或需后优化的动态方法不同，V-DPM一次性前馈即可输出密集的场景流和4D对应，为视频理解、机器人操作等下游任务提供了高效的基础表示。



### 静态重建的繁荣与动态重建的困境

近年来，基于前馈网络的多视图三维重建取得了显著进展。以 **DUSt3R**（Wang et al., CVPR 2024）和 **VGGT**（Wang et al., CVPR 2025）为代表的方法，能够从多张图像中一次性预测场景的密集三维点云和相机参数，无需传统的特征匹配与全局优化。这些方法的核心表示是**静态点图**（Point Maps）——为每个像素预测其在统一世界坐标系下的三维坐标，但隐含假设场景在拍摄期间保持静止。

然而，现实世界是动态的。当场景中存在运动物体、非刚体变形或相机与场景同时运动时，静态点图表示立即失效：同一像素在不同帧中对应的三维点不再相同，网络无法建立跨时间的对应关系。这一根本性限制使得静态重建器无法直接处理视频输入，更无法恢复**场景流**（scene flow）——即场景中每个三维点的运动轨迹。

### 现有动态扩展的局限

为应对动态场景，研究者提出了**动态点图**（Dynamic Point Maps, DPM）表示。**DPM**（Sucar et al., ICCV 2025）将点图扩展为 $P_i(t_j, \pi_k) \in \mathbb{R}^{3 \times H \times W}$，允许为任意视角 $\pi_k$ 和任意时间戳 $t_j$ 下的像素 $i$ 预测三维坐标。然而，DPM 存在两个关键瓶颈：

1. **成对处理的限制**：DPM 仅能处理两视图输入，无法直接建模多视图间的时空一致性。当应用于多帧视频时，必须借助昂贵的后优化步骤（如全局束调整）来融合成对预测，这不仅增加了计算开销，还导致误差在长序列中累积。

2. **时间不变性的缺失**：后续工作如 **MonST3R**（Zhang et al., arXiv 2024）尝试将静态主干网络扩展到动态场景，但仅预测**时间可变点图** $\mathcal{P} = (P_0(t_0, \pi_0), P_1(t_1, \pi_0), \dots)$——每帧点云仅在其自身时间戳下表达。由于缺乏时间不变性，MonST3R 无法直接建立跨帧的像素对应，必须依赖外挂的 2D 跟踪器来恢复运动信息，这割裂了重建与跟踪过程，限制了端到端优化。

### 核心瓶颈与本文动机

上述方法的共同症结在于：**缺乏一种既能保持视角不变性、又能建立时间不变性的统一表示**。视角不变性意味着不同帧的点云表达在同一世界坐标系下，这是多视图几何的基本要求；时间不变性则要求所有帧的点云对齐到同一参考时间戳，从而直接建立跨时间的密集对应。只有同时满足这两种不变性，才能从视频中一次性恢复完整的 4D 重建（3D 形状 + 运动轨迹）。

V-DPM 的动机正是填补这一空白。其核心洞察是：**将 4D 重建分解为两个连续阶段**——首先生成时间可变但视角不变的点图（易于从静态主干微调获得），再通过轻量的时间条件解码器将其对齐到统一时间戳，从而获得时间-视角完全不变的点图。这种两阶段设计使得预训练的静态 3D 重建网络（如 VGGT）只需少量合成数据微调即可转化为强大的 4D 重建器，大幅降低了对 4D 标注数据的需求和训练成本，同时实现了端到端的多视图动态重建。



## 核心方法与创新机理

V-DPM的核心创新在于将4D动态重建任务分解为**两阶段级联预测**，从而将预训练的静态3D重建网络高效转化为强大的4D重建器。这一设计直接回应了领域瓶颈：现有前馈方法（如**MonST3R**，Zhang et al., arXiv 2024）仅能预测时间可变点图，缺乏时间不变性，必须借助2D跟踪器等外部组件才能恢复密集4D对应；而成对动态点图方法（如**DPM**，Sucar et al., ICCV 2025）在处理多视图时需要昂贵的后优化，难以端到端扩展。

### 两阶段表示：从时间可变到时间不变

V-DPM的核心机制是预测两类互补的点图集合（Figure 3）：

- **时间可变点图** $\mathcal{P}$：首先让网络预测一组视角不变但时间可变的点图，每张输入图像 $I_i$ 对应一个点云 $P_i(t_i, \pi_0)$，表达在参考视角 $\pi_0$ 下、各自的时间戳 $t_i$ 上。这一阶段仅需从静态主干微调即可获得，类似于MonST3R的输出。
  
- **时间不变点图** $\mathcal{Q}$：在此基础上，通过新增的时间条件解码器，将骨架特征对齐到统一参考时间戳 $t_j$，预测所有输入图像在**同一时刻**的点云 $P_i(t_j, \pi_0)$，实现视角与时间的双重不变性。

$$
\mathcal{P} = (P_0(t_0, \pi_0), P_1(t_1, \pi_0), \dots, P_{N-1}(t_{N-1}, \pi_0))
$$

$$
\mathcal{Q} = (P_0(t_j, \pi_0), P_1(t_j, \pi_0), \dots, P_{N-1}(t_j, \pi_0))
$$

这一设计的因果杠杆在于：$\mathcal{Q}$ 直接建立了跨时间的像素级对应关系，使得场景流（scene flow）的密集恢复成为网络前馈过程的自然产物，无需任何外部跟踪器或成对后优化。

### 时间条件解码器：轻量但关键的架构增量

为实现从 $\mathcal{P}$ 到 $\mathcal{Q}$ 的转换，V-DPM在**VGGT**（Wang et al., CVPR 2025）静态骨架上新增了一个**时间条件Transformer解码器**（Figure 4），这是方法中唯一的架构增量：

- **结构**：由4个交替的帧注意力（frame attention）和全局注意力（global attention）块组成，接收骨架输出的图像块令牌 $\phi_{p_i}$ 和目标时间戳令牌 $t_j$。
- **条件机制**：采用**自适应LayerNorm (adaLN)**，以目标时间令牌调制每个注意力块中的归一化参数，使特征逐步对齐到统一时间戳。
- **共享DPT头**：时间不变点图的预测复用了时间可变分支的DPT头权重，进一步降低了参数量。

消融实验（补充材料Sec. 7）证实了这一设计的必要性：将解码器深度降至2层、改用加法时间条件、或移除专用Transformer解码器而直接使用DPT头，均导致动态点图误差上升（例如，完整模型EPE为0.0500/0.0472，而DPT decoder方案升至0.0538/0.0502）。

### 训练策略：静态预训练与动态微调的高效结合

V-DPM的另一个关键创新在于**训练策略的精心设计**，使其仅需少量合成动态数据即可从静态预训练权重完成转化：

- **继承静态能力**：直接以VGGT预训练权重初始化骨架和相机姿态回归器，保留了强大的静态多视图几何理解能力。
- **混合数据微调**：在静态+动态混合数据集（ScanNet++、Blended-MVS、Kubric、PointOdyssey、Waymo）上进行微调，使网络同时保持静态重建精度并学习运动推断。
- **损失归一化方案**：采用示例内平均再批次平均的归一化策略，确保稀疏的动态标注（如场景流真值）能够获得与密集静态标注相当的梯度贡献，避免动态信号被淹没。

### 多视图融合的简化

与DPM需要成对预测后进行全局优化不同，V-DPM基于VGGT骨架**一次前馈预测所有帧**的时间可变点图。当需要不同参考时间戳的 $\mathcal{Q}$ 时，仅需重跑轻量的时间条件解码器，而骨架特征完全复用。对于长视频，V-DPM采用滑动窗口 + 束调整融合的后处理策略，在保持精度的同时控制计算开销。

### 创新总结

V-DPM的changed slots清晰体现了其相对于基线的本质提升：

| 维度 | VGGT/DPM基线 | V-DPM创新 |
|------|-------------|----------|
| **输出表示** | 静态点图或仅时间可变点图 | 时间可变 $\mathcal{P}$ + 时间不变 $\mathcal{Q}$ 的组合 |
| **时间建模** | 无或需外部跟踪器 | 时间条件解码器 + adaLN，内建跨时间对应 |
| **训练数据** | 仅静态数据或需大量4D标注 | 静态预训练 + 少量动态混合数据微调 |
| **多视图融合** | 单次前馈或成对后优化 | 骨架特征复用 + 轻量解码器重跑 |

这种“先预测时间可变、再对齐到统一时间戳”的两阶段范式，使得V-DPM在2-View 4D重建EPE上误差约为DPM和**St4RTrack**（Feng et al., ICCV 2025）的1/5（Table 1），并在10帧密集追踪中保持相近精度（Table 2），同时大幅超越MonST3R等前馈方法在视频深度估计上的表现（Sintel AbsRel: 0.247 vs 1.196; Bonn: 0.057 vs 0.777, Table 3）。



V-DPM 的整体 pipeline 围绕一个核心设计展开：**将 4D 重建分解为两个连续阶段**，先预测时间可变但视角不变的点图，再通过轻量的时间条件解码器将其对齐到统一时间戳，从而获得时间-视角完全不变的点图。这一两阶段设计使得预训练的静态多视图重建网络（**VGGT**，Wang et al., CVPR 2025）只需少量合成数据微调，即可转化为强大的 4D 重建器。

### 输入输出流

网络 $\Phi$ 接收 $N$ 张视频帧图像 $\{I_0, \dots, I_{N-1}\}$，输出两组点图：

$$(\mathcal{P}, \mathcal{Q}) := \Phi(I_0, \dots, I_{N-1})$$

- **时间可变点图集 $\mathcal{P}$**：每张输入图像 $I_i$ 对应一个在其自身时间戳 $t_i$ 下、表达在参考视角 $\pi_0$ 中的 3D 点云 $P_i(t_i, \pi_0)$。这组点图视角不变但时间可变，与 **MonST3R**（Zhang et al., arXiv 2024）的预测形式类似。

$$\mathcal{P} = (P_0(t_0, \pi_0), P_1(t_1, \pi_0), \dots, P_{N-1}(t_{N-1}, \pi_0))$$

- **时间不变点图集 $\mathcal{Q}$**：所有输入图像的点云对齐到同一参考时间戳 $t_j$，表达在参考视角 $\pi_0$ 中。这组点图同时具备视角不变性和时间不变性，直接建立了跨时间的像素级对应，可用于密集场景流恢复。

$$\mathcal{Q} = (P_0(t_j, \pi_0), P_1(t_j, \pi_0), \dots, P_{N-1}(t_j, \pi_0))$$

### 模块关系

Figure 2 展示了 V-DPM 的完整架构，由以下五个模块串联构成：

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2601_09499/figures/002_Figure_2.jpg]]
*Figure 2: Model architecture of V-DPM. Our model decodes both time-variant point maps as in MonST3R [30] and time-invariant point maps corresponding to a fixed timestamp*

1. **VGGT Backbone（预训练静态特征提取器）**：输入 $N$ 帧图像，通过交替注意力机制输出图像块令牌 $\phi_{p,i}$、相机令牌 $\phi_{c,i}$ 和寄存器令牌 $\phi_{r,i}$，并初步预测相机姿态。该骨干继承自 VGGT 的预训练权重，为后续所有解码提供多视图特征。

2. **Time-Variant DPT Head（时间可变点图解码头）**：直接从骨干的多层特征预测时间可变点图 $\mathcal{P}$，即每个输入帧在其自身时间戳下的 3D 点云。该模块与 MonST3R 的单帧动态预测能力对应，是第一阶段重建的输出。

3. **Time-Conditioned Decoder（时间条件解码器）**：接收骨干输出的图像块令牌 $\phi_{p,i}$ 和目标时间令牌 $t_j$，通过 4 层交替帧注意力/全局注意力的 Transformer 块，以自适应 LayerNorm（adaLN）调制特征，将所有帧的特征对齐到统一时间戳。消融实验表明，完整设计（深度 4 + adaLN）对性能至关重要——降低深度、改用加法条件或移除专用 Transformer 解码器均导致动态点图误差上升（补充材料 Sec. 7）。

4. **Time-Invariant DPT Head（时间不变点图解码头）**：与时间可变头共享权重的 DPT 模块，从时间条件解码器的输出预测时间不变点图 $\mathcal{Q}$。这是第二阶段重建的输出，直接提供跨帧的密集 3D 对应。

5. **Camera Pose Regressor（相机姿态回归器）**：从骨干的相机令牌 $\phi_{c,i}$ 回归相机内参和外参，与 VGGT 的设计保持一致。

### 设计优势

这一 pipeline 的关键优势在于**计算效率与表示能力的平衡**：骨干网络只需前馈一次即可预测所有帧的时间可变点图；当需要不同参考时间戳的时间不变点图时，仅需重跑轻量的时间条件解码器，无需重新计算整个骨干。对于长视频序列，V-DPM 采用滑动窗口 + 束调整后处理的方式进行融合，以处理数百帧的输入。

**证据强度**：网络设计的有效性由消融实验强力支撑（置信度 0.98）；两阶段分解的核心洞察在多个动态数据集上得到验证，V-DPM 在 2-View EPE 任务上误差约为 **DPM**（Sucar et al., ICCV 2025）和 **St4RTrack**（Feng et al., ICCV 2025）的 1/5（置信度 0.95）。

### 补充图表

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2601_09499/figures/001_Figure_1.jpg]]
*Figure 1: V-DPM results. We propose a method for extending state-of-the-art static 3D reconstructors like VGGT with Dynamic Point Maps (DPMs). Given a video snippet, V-DPM reconstructs the 3D motion of the scene (i.e., the scene flow), along with its 3D shape and the camera parameters. Because of DPMs, the same representation captures both the static background and complex non-rigid motion*



### 3.1 动态点图表示

V-DPM 的核心表示是多视图动态点图（Dynamic Point Maps, DPMs）的扩展。对于输入图像 $I_i$，其对应的动态点图定义为：

$$P_i(t_j, \pi_k) \in \mathbb{R}^{3 \times H \times W}$$

其中每个像素位置存储一个 3D 点坐标，该坐标表达在视角 $\pi_k$ 和时间 $t_j$ 下。索引 $i$ 表示该点图对应图像 $I_i$ 的像素，而 $j$ 和 $k$ 可任意选择——这种灵活性正是 V-DPM 实现时间不变性的关键。

网络实际预测两组点图，按顺序计算：

**时间可变点图 $\mathcal{P}$**（视角不变，时间可变）：

$$\mathcal{P} = (P_0(t_0, \pi_0), P_1(t_1, \pi_0), \ldots, P_{N-1}(t_{N-1}, \pi_0))$$

每张输入图像的点云在其自身时间戳下表达在参考视角 $\pi_0$ 中。这组点图与 MonST3R 的输出类似，仅具备视角不变性，但无法建立跨时间对应。

**时间不变点图 $\mathcal{Q}$**（视角和时间均不变）：

$$\mathcal{Q} = (P_0(t_j, \pi_0), P_1(t_j, \pi_0), \ldots, P_{N-1}(t_j, \pi_0))$$

所有输入图像的点云对齐到同一参考时间戳 $t_j$，表达在参考视角 $\pi_0$ 中。这组点图直接建立了跨时间的像素级对应关系，使得场景流可以密集恢复。

网络 $\Phi$ 的完整映射为：

$$(\mathcal{P}, \mathcal{Q}) := \Phi(I_0, \ldots, I_{N-1})$$

### 3.2 两阶段重建架构

V-DPM 将 4D 重建分解为两个连续阶段，这一设计是其核心洞察所在：

**第一阶段**：生成时间可变但视角不变的点图 $\mathcal{P}$。该任务与静态重建高度相似，因此可以直接从预训练的静态多视图重建网络（VGGT）微调获得，大幅降低了对 4D 标注数据的需求。

**第二阶段**：通过时间条件解码器将特征对齐到统一时间戳，预测时间-视角完全不变的点图 $\mathcal{Q}$。该解码器复用第一阶段骨架提取的特征，仅需改变参考时间戳时重跑轻量解码器，避免了成对后优化。

### 3.3 关键模块

#### VGGT 骨架

V-DPM 基于 **VGGT**（Wang et al., CVPR 2025）的预训练权重构建。骨架输入 $N$ 张图像，提取图像块令牌、相机令牌和寄存器令牌，通过交替注意力机制输出特征 $\phi_{p_i}, \phi_{c_i}, \phi_{r_i}$，并预测相机姿态。继承 VGGT 的交替注意力架构使得网络天然具备多视图信息融合能力。

#### 时间可变 DPT 头

利用骨架多层特征直接预测时间可变点图 $P_i(t_i, \pi_0)$，每个输入帧在其自身时间戳下输出。该模块与 MonST3R 的设计类似，但共享 VGGT 骨架的多视图特征。

#### 时间条件解码器

这是 V-DPM 的核心创新模块。解码器接收骨架输出的图像块特征 $\phi_{p_i}$ 和目标时间令牌 $t_j$，通过交替的帧注意力和全局注意力块处理，以自适应 LayerNorm（adaLN）实现时间条件调制。具体而言，adaLN 利用目标时间令牌调制归一化后的 patch tokens，使特征对齐到统一时间戳，从而输出用于预测时间不变点图的特征。

消融实验（补充材料 Sec. 7）证实了该设计的必要性：完整模型（深度 4 + adaLN）在动态点图指标上最优；将解码器深度降至 2、改用加法时间条件、或移除专用 Transformer 解码器直接使用 DPT 头，均导致误差上升。

#### 时间不变 DPT 头

与时间可变头共享权重的 DPT 模块，从时间条件解码器的输出预测时间不变点图 $P_i(t_j, \pi_0)$。共享权重设计强化了两组点图之间的一致性。

#### 相机姿态回归器

从骨架相机令牌 $\phi_{c_i}$ 回归相机内参和外参，与 VGGT 的设计保持一致。

### 3.4 训练策略

V-DPM 在静态与动态混合数据上微调（ScanNet++、Blended-MVS、Kubric、PointOdyssey、Waymo），采用示例内平均再批次平均的损失归一化方案，确保稀疏动态标注获得充分梯度。损失函数结合了 DPM 的置信度校准损失和 VGGT 的相机姿态回归损失。

### 补充图表

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2601_09499/figures/003_Figure_3.jpg]]
*Figure 3: V-DPM point maps. The point maps*

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2601_09499/figures/004_Figure_4.jpg]]
*Figure 4: Transformer block in the time-conditioned decoder. Conditioning is implemented via adaptive LayerNorm [14, 16]*



## 实验与关键发现

### 4D 重建与密集追踪

V-DPM 在 2‑View 4D 重建任务上展现出压倒性优势。Table 1 报告了四个动态数据集（PointOdyssey、Kubric‑F、Kubric‑G、Waymo）上的 End‑Point Error（EPE），V‑DPM 的平均误差约为 0.03～0.05，而先前方法 **DPM**（Sucar et al., ICCV 2025）和 **St4RTrack**（Feng et al., ICCV 2025）的误差均在 0.15～0.20 区间，V‑DPM 实现了约 5 倍的误差降低。这一结果直接验证了核心设计：时间不变点图集 $\mathcal{Q}$ 的引入，使网络能够一次性建立跨帧的密集像素对应，避免了 DPM 所需的高成本成对后优化。

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2601_09499/figures/008_Table_1.jpg]]
*Table 1: 2-View EPE error for 4D reconstruction, reported for four point clouds (one for each image and time frame)*

在 10 帧视频密集追踪任务中（Table 2），V‑DPM 的性能与 2‑View 设置保持相近的低误差，而 DPM 的误差则大幅上升。这表明 V‑DPM 具备在整个视频片段上推理时间动态的能力，其产生的 3D 轨迹更加平滑且自洽。Figure 7 在 DAVIS 数据集上的定性对比进一步佐证了这一点：V‑DPM 重建的静态背景更准确，动态区域的 3D 轨迹（$P_0(t_9, \pi_0)$）也更连贯，而 DPM 的轨迹则表现出明显的抖动和不一致性。

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2601_09499/figures/010_Table_2.jpg]]
*Table 2: Tracking EPE error reported for 10-frame snippets, evaluating dense tracks of all pixels in the first frame*

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2601_09499/figures/007_Figure_7.jpg]]
*Figure 7: Qualitative comparison of dynamic 3D tracking on the DAVIS dataset [15]; results are reconstructed from 10-frame snippets. On the left we visualise the first and last input frames, and on the right we show the reconstructed point map*

### 视频深度估计

在 Sintel 和 Bonn 数据集上的视频深度评估（Table 3）中，V‑DPM 以显著优势超越所有先前工作，仅略逊于并发工作 **π³**（Wang et al., arXiv 2025）。具体而言，在 Sintel 上 V‑DPM 的 AbsRel 为 0.247，而 **MonST3R**（Zhang et al., arXiv 2024）高达 1.196，DPM 为 0.399；在 Bonn 上 V‑DPM 的 AbsRel 为 0.057，MonST3R 为 0.777，DPM 为 0.087。这一结果揭示了 MonST3R 等早期动态扩展的致命缺陷：仅预测时间可变点图 $\mathcal{P}$ 而缺乏时间不变性，必须借助 2D 跟踪器等外部组件才能恢复运动，导致深度估计严重退化。V‑DPM 通过时间条件解码器直接输出对齐到统一时间戳的点图 $\mathcal{Q}$，从根本上解决了这一问题。

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2601_09499/figures/011_Table_3.jpg]]
*Table 3: Video Depth Evaluation on the Sintel and Bonn datasets*

### 相机姿态估计

在相机姿态指标上（Table 4），V‑DPM 同样具有竞争力。在 Sintel 上 ATE 仅为 0.105，而 DPM 为 0.67，St4RTrack 为 0.209，V‑DPM 较 DPM 降低了 84.3%。值得注意的是，V‑DPM 在姿态估计上略逊于 π³，但 π³ 不恢复场景流，两者对比维度不同——V‑DPM 在保持有竞争力姿态精度的同时，额外提供了密集的 4D 运动信息。

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2601_09499/figures/009_Table_4.jpg]]
*Table 4: Comparison of pose metrics on the Sintel and TUMdynamics datasets*

### 消融实验

补充材料中的网络设计消融（Sec. 7）证实了完整时间条件解码器的必要性。完整模型（深度 4 + adaLN）在动态点图指标上取得最优结果（EPE 0.0500/0.0472）。当解码器深度降至 2 层时，误差上升至 0.0518/0.0476；将自适应 LayerNorm 替换为加法时间条件后，误差升至 0.0524/0.0484；若完全移除 Transformer 解码器、改用直接 DPT 解码器，误差进一步升至 0.0538/0.0502。这些消融一致表明，adaLN 调制和充分的解码器深度对于将时间可变特征精确对齐到目标时间戳至关重要。

此外，损失归一化策略的消融显示，采用“示例内平均再批次平均”的方案后，动态重建精度得到改善。这一设计平衡了静态标注（通常密集）和稀疏动态标注对梯度的贡献，避免了稀疏动态信号被大量静态像素淹没的问题。

### 失败模式与局限性

尽管 V‑DPM 在动态 4D 重建上表现优异，但存在以下已知局限：

1. **静态精度差距**：在静态深度和相机位姿指标上，V‑DPM 仍略逊于最新的 π³。这表明时间条件解码器的引入可能对静态特征的纯度产生轻微干扰，如何在保留动态性能的同时进一步提升静态几何精度是一个开放问题。
2. **长视频处理开销**：处理数百帧的长视频时，V‑DPM 需采用滑动窗口 + 束调整后处理，而非完全的一次性前馈。这引入了额外的计算开销，与部分端到端方法在测试条件上不完全对齐。
3. **评估规模受限**：当前评估受可用计算资源限制，未在更大规模或更多样化的真实视频数据集上验证。模型在严重遮挡、快速非刚体变形和大幅光照变化下的鲁棒性仍需进一步检验。

### 补充图表

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2601_09499/figures/005_Figure_5.jpg]]
*Figure 5: Dynamic point maps of a robot doing a manipulation task*

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2601_09499/figures/006_Figure_6.jpg]]
*Figure 6: Result of optimisation used for video depth and camera pose evaluation on a sequence from the Bonn dataset*



## 定位与知识库关联

### 1. 方法演进脉络

V-DPM 的核心贡献在于将静态多视图前馈重建架构系统性地扩展至动态场景，其设计沿着“静态点图 → 时间可变点图 → 时间不变点图”的路线递进。

**静态点图基础。** V-DPM 直接继承 **VGGT**（Wang et al., CVPR 2025）的预训练骨架，包括其交替注意力机制、相机姿态回归头以及基于 DPT 的点图解码头。VGGT 假设场景静止，为每个视图输出单一的点图 $P_i(\pi_0)$，这构成了 V-DPM 的起点。

**时间可变扩展。** 与 VGGT 几乎同期，**MonST3R**（Zhang et al., arXiv 2024）和 **DPM**（Sucar et al., ICCV 2025）分别从不同路径尝试处理动态场景。MonST3R 将静态重建网络扩展为预测时间可变点图 $\mathcal{P} = (P_0(t_0, \pi_0), \dots, P_{N-1}(t_{N-1}, \pi_0))$，即每个输入帧在其自身时间戳下的点云。然而，这种表示缺乏时间不变性——不同帧的点云无法直接建立跨时间对应，必须借助额外的 2D 跟踪器才能恢复场景流。DPM 则提出了成对的动态点图表示，但仅处理两视图，多视图场景需要昂贵的后优化。V-DPM 的第一阶段（时间可变 DPT 头）与 MonST3R 思路一致，但将其作为中间产物而非最终输出。

**时间不变性的建立。** V-DPM 的关键突破在于第二阶段：引入时间条件解码器，从骨架特征中生成时间不变点图 $\mathcal{Q} = (P_0(t_j, \pi_0), \dots, P_{N-1}(t_j, \pi_0))$，将所有视图的点云对齐到统一参考时间戳 $t_j$。这一设计直接建立了跨时间的密集像素对应，使场景流的恢复成为点图之间的简单差分，无需任何外部跟踪组件或成对后优化。

**同期与后续工作。** 在 V-DPM 发表同期，**St4RTrack**（Feng et al., ICCV 2025）也尝试预测动态对应，但在 2-View EPE 指标上误差约为 V-DPM 的 5 倍（Table 1）。另一并发工作 **π³**（Wang et al., arXiv 2025）在静态深度和相机位姿估计上略优于 V-DPM，但不恢复场景流，因此两者的能力边界不同——V-DPM 在动态/运动重建上具有独特优势。

### 2. 技术增量与设计选择

V-DPM 相对于基线的改动集中在三个层面：

**输出表示的维度扩展。** 从 VGGT 的单一静态点图扩展为 $\mathcal{P}$ 与 $\mathcal{Q}$ 的组合，实现了视角和时间双重不变性。这一表示使得网络输出天然支持密集 4D 对应，而无需像 MonST3R 那样依赖外部 2D 跟踪器。

**时间条件解码器的引入。** 在 VGGT 骨架之上新增 4 层交替帧/全局注意力的 Transformer 解码器，通过自适应 LayerNorm（adaLN）以目标时间令牌调制特征。消融实验（补充材料 Sec. 7）表明，这一完整设计对性能至关重要：将解码器深度降至 2 层、改用加法时间条件、或移除专用 Transformer 解码器直接使用 DPT 头，均导致动态点图误差上升。

**训练策略的适配。** VGGT 仅在静态数据集上预训练；V-DPM 在静态+动态混合数据（ScanNet++、Blended-MVS、Kubric、PointOdyssey、Waymo）上微调，并采用示例内平均再批次平均的损失归一化方案，以平衡静态和稀疏动态标注对梯度的影响。这一策略使得预训练的静态主干仅需少量合成动态数据即可转化为强大的 4D 重建器。

### 3. 适用边界与已知局限

**评估覆盖范围。** 当前实验在 PointOdyssey、Kubric-F、Kubric-G、Waymo 四个合成/半合成数据集上验证了 2-View 和 10 帧密集追踪性能，在 Sintel 和 Bonn 上验证了视频深度估计，在 Sintel 和 TUM-dynamics 上验证了相机姿态。但这些数据集的规模和多样性有限，V-DPM 在更大规模真实视频上的泛化性尚未被充分验证。

**静态精度差距。** 在静态深度和相机位姿指标上，V-DPM 仍略逊于并发工作 π³。这表明时间条件解码器的引入可能对静态重建精度产生了轻微的负面影响，或者 π³ 在静态任务上采用了更优的设计选择。

**长视频处理的计算模式。** 虽然 V-DPM 在短片段（10 帧）上实现了端到端前馈推理，但处理数百帧的长视频时仍需滑动窗口 + 束调整后处理，未实现完全的一次性前馈 4D 重建。这与部分完全端到端的方法在测试条件上不完全对齐，且增加了额外计算开销。

**极端场景的鲁棒性。** 论文未系统评估 V-DPM 在严重遮挡、快速非刚体变形、大幅光照变化等极端条件下的表现。这些场景可能对时间条件解码器的对齐能力构成挑战。

### 4. 开放问题

1. **静态与动态性能的权衡。** 如何在保留动态重建优势的同时，进一步提升静态几何和位姿精度？可能的路径包括结合 π³ 的设计选择，或对静态区域和动态区域采用差异化的解码策略。

2. **时间插值与新视角合成。** 时间条件解码器当前设计用于对齐到离散的参考时间戳。能否将其泛化到任意时间插值，实现任意时刻的新视角合成？这需要解码器学习连续的时间表示。

3. **实时应用中的压缩与加速。** 在计算受限的场景（如机器人控制）中，V-DPM 的多层 Transformer 解码器和交替注意力机制可能成为瓶颈。模型能否进一步压缩和加速而不显著损失 4D 重建质量？

4. **对真实世界多样性的泛化。** 当前训练数据以合成场景为主，真实世界视频中的运动模糊、卷帘快门效应、非朗伯表面等挑战尚未被覆盖。更大规模的真实动态数据训练是否必要，或者合成数据训练的模型已具备足够的域迁移能力？



## 原文 PDF

![[paperPDFs/CVPR_2026/V_DPM_4D_Video_Reconstruction_with_Dynamic_Point_Maps.pdf]]
