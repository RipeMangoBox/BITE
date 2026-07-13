---
title: Direction-aware 3D Large Multimodal Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Direction_aware_3D_Large_Multimodal_Models.pdf
project_link: null
code_link: null
aliases:
- PP
- DA3LMM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过显式引入自车姿态作为模型输入，从ScanNet RGB-D序列中自动恢复姿态（PoseRecover），并利用该姿态对点云进行坐标对齐（PoseAlign），直接消除方向歧义。
primary_logic: 自车姿态是3D空间推理的“免费午餐”——它可以自动从视频外参中恢复，且仅需将点云转换到相机参考系即可让冻结的预训练编码器获得方向感知，无需架构改造或全量重训。
claims:
- 语言查询分析显示，ScanQA中46.7%、Scan2Cap中89.7%、SQA3D中95.2%的问题依赖明确的方向推理，但由于缺少自车姿态，这些问题构成不适定问题。
- 在四个不同架构的3D LMM backbone（LL3DA、LL3DA-SONATA、Chat-Scene、3D-LLAVA）上，PoseAlign均带来一致的性能提升，其中3D-LLAVA的ScanRefer mIoU从42.6提升至55.4（+30%相对提升），Scan2Cap LLM-as-judge准确率从28.1提升至31.4。
- 在方向关键问题子集上，PoseAlign-Transform将ScanQA的LLM-as-judge准确率从36.6%提升至40.3%，验证了方法专门解决了方向模糊性。
- 随机姿态替代PoseRecover恢复的姿态会导致性能下降，而仅输入变换后的点云、不调整编码器的基线模型性能严重退化，证明精确的姿态恢复和坐标对齐是性能提升的唯一原因。
---

# Direction-aware 3D Large Multimodal Models

> [!tip] 核心洞察
> 自车姿态是3D空间推理的“免费午餐”——它可以自动从视频外参中恢复，且仅需将点云转换到相机参考系即可让冻结的预训练编码器获得方向感知，无需架构改造或全量重训。

| 字段 | 内容 |
|------|------|
| 中文题名 | 方向感知的3D大型多模态模型 |
| 英文题名 | Direction-aware 3D Large Multimodal Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.19063) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PoseRecover + PoseAlign |
| Dataset | ScanRefer, Multi3DRefer, ScanQA, Scan2Cap |

> [!tip] 效果简介
> - ScanRefer 上，mIoU 55.4 (3D-LLAVA + PoseAlign-T, Clip X=0.3) vs 42.6 (3D-LLAVA baseline) (+12.8 pp (+30.0% relative))。
> - Multi3DRefer 上，mIoU 54.3 (3D-LLAVA + PoseAlign-T, Clip X=0.3) vs 48.1 (3D-LLAVA baseline) (+6.2 pp)。
> - ScanQA 上，LLM-as-judge accuracy 47.3 (3D-LLAVA + PoseAlign-T, Clip X=0.3) vs 45.7 (3D-LLAVA baseline) (+1.6 pp)。

## 概要

**问题与瓶颈**。现有3D室内基准测试（ScanRefer、ScanQA、Scan2Cap等）中40%–95%的查询依赖方向性空间推理，但数据集完全缺失自车姿态信息，导致“左/右/前/后”等方向语义从根本上定义不明确，3D大型多模态模型（LMM）无法学习一致的方向表示。

**核心洞察**。自车姿态是3D空间推理的“免费午餐”——它可以从ScanNet RGB-D序列的相机外参中自动恢复，且仅需将点云转换到相机参考系即可让冻结的预训练编码器获得方向感知，无需架构改造或全量重训。

**方法**。本文提出两阶段框架：**PoseRecover**从RGB-D外参中自动恢复与查询相关的相机姿态，通过物体-截锥体交集计算与Z-buffer可见性验证生成候选姿态列表；**PoseAlign**利用恢复的姿态对点云进行坐标对齐（PoseAlign-Transform），将世界坐标系下的点云变换到自车参考系，使方向语义统一以观察者为锚点。

**主要结果**。在四个不同架构的3D LMM backbone（LL3DA、LL3DA-SONATA、Chat-Scene、3D-LLAVA）上，PoseAlign均带来一致的性能提升。其中，3D-LLAVA在ScanRefer上的mIoU从42.6提升至55.4（+30%相对提升），在Scan2Cap上的LLM-as-judge准确率从28.1提升至31.4。在方向关键问题子集上，PoseAlign-Transform将ScanQA的LLM-as-judge准确率从36.6%提升至40.3%，验证了方法专门解决了方向模糊性。

**方法谱系与知识库定位**。本文属于3D视觉-语言理解中“空间推理增强”方向，区别于现有工作通过改进编码器架构或训练策略来提升性能的思路，转而从数据层面解决方向性不适定问题。与依赖检测器提取物体令牌的**Chat-Scene**、使用Q-Former桥接点云与LLM的**LL3DA**、以及基于超点Transformer的**3D-LLAVA**等基线模型相比，PoseAlign以即插即用的方式注入自车姿态，保持点云编码器冻结，仅微调投影层和LLM的LoRA参数，避免了学习位置捷径的风险。

### 3D 视觉语言任务的现状与瓶颈

3D 大型多模态模型（3D LMMs）在具身智能、空间推理等任务中展现出巨大潜力。然而，现有模型在室内场景理解中普遍面临一个被忽视的根本性问题：**方向性空间推理的不适定性**。对 ScanQA、Scan2Cap 和 SQA3D 等主流基准的语言查询分析显示，**46.7%**（ScanQA）、**89.7%**（Scan2Cap）和 **95.2%**（SQA3D）的问题依赖明确的方向推理（如“左边的椅子”“前面的桌子”），但这些数据集完全缺失自车姿态（ego pose）信息。在没有自车参考系的情况下，“左/右/前/后”等方向语义从根本上无法定义，使得这些查询构成不适定问题——模型被迫在缺乏空间锚点的情况下猜测方向关系。

### 现有方法的缺口

当前 3D LMMs 通常将点云编码为全局特征后与语言模型对齐，但这一范式存在两个关键缺陷：

1. **坐标系的任意性**：ScanNet-v2 等数据集采用固定的世界坐标系，该坐标系与场景语义无任何关联。模型在此坐标系下学习空间推理时，无法建立一致的方向语义映射——“左”在不同场景、不同视角下可能对应完全不同的世界坐标方向。

2. **数据增强的方向破坏**：现有训练流程普遍采用随机旋转、翻转、抖动等点云数据增强，这些操作虽然提升了模型的旋转不变性，但也彻底抹去了任何可能的方向线索，使得模型在方向关键查询上只能依靠统计相关性而非真正的空间理解。

### 核心洞察：自车姿态是“免费午餐”

本文的核心洞察是：**自车姿态可以从 ScanNet 的 RGB-D 序列中自动恢复，无需任何额外标注**。ScanNet-v2 提供了每帧 RGB-D 图像的相机内参 $K$ 和外参 $(\mathcal{R}, t)$，通过计算相机视锥体与场景中目标物体的空间交集，可以确定哪些相机视角“看到”了查询涉及的物体。这一恢复过程完全离线、全自动化，为每个文本-场景对生成候选自车姿态列表。

更重要的是，一旦获得自车姿态，仅需将点云从世界坐标系变换到相机坐标系——即让模型以“自车”为参考系观察场景——就能使冻结的预训练编码器天然获得方向感知能力。这一定位对齐操作无需架构改造、无需全量重训，仅需在指令微调阶段注入姿态信息，即可让现有 3D LMMs 学会一致的方向语义。

### 本文动机

基于上述分析，本文提出 **PoseRecover + PoseAlign** 框架，从数据和模型两个层面系统解决 3D 空间推理中的方向模糊问题：

- **PoseRecover**：自动从 ScanNet RGB-D 外参中恢复查询相关的自车姿态，通过物体-视锥体交集计算与 Z-buffer 可见性验证，为每个查询生成可靠的候选姿态列表。
- **PoseAlign**：将恢复的姿态信息注入现有 3D LMMs，通过点云坐标对齐（PoseAlign-Transform）、特征嵌入（PoseAlign-Embed）或文本提示（PoseAlign-Prompt）三种互斥方案，使模型获得统一的方向参考系。

该方法的核心优势在于其**即插即用**特性：不依赖特定模型架构，可应用于 LL3DA、Chat-Scene、3D-LLAVA 等多种不同设计的 3D LMMs，且仅需冻结点云编码器、微调投影层和 LLM 的 LoRA 参数，避免了昂贵的全量重训。

## 核心方法与创新机理

本文的核心创新并非提出一种新的3D LMM架构，而是识别并系统性地解决了现有3D视觉语言基准测试与模型中一个被长期忽视的根本缺陷：**方向性空间推理的定义不明确问题**。其贡献围绕两条主线展开——姿态恢复（PoseRecover）与姿态对齐（PoseAlign），二者共同构成一套即插即用的方向感知增强方案。

### 问题诊断：方向关键查询的“不适定性”

现有3D室内基准测试（ScanRefer、ScanQA、Scan2Cap、SQA3D）中，40%–95%的查询依赖于明确的方向推理（如“桌子左边的椅子”），但这些数据集完全缺失自车姿态信息。在缺乏观测者参考系的情况下，方向性空间关系成为不适定问题：模型无法从数据中学习到一致的方向语义，只能依赖脆弱的统计相关性或世界坐标系的偶然规律。这一诊断是后续方法设计的逻辑起点，其量化依据来自对多个数据集中语言查询的方向依赖性分析（ScanQA中46.7%、Scan2Cap中89.7%、SQA3D中95.2%的问题涉及方向判断）。

### Changed Slot 1：自车姿态的自动恢复（PoseRecover）

**Baseline状态**：所有现有3D LMM在训练和推理时均不接收任何姿态信息，方向性查询保持不适定。

**创新方案**：PoseRecover从ScanNet RGB-D序列的相机外参中自动恢复与查询相关的自车姿态。其核心流程包括：
- **视锥体计算**：根据相机内参 $K$ 和外参 $(\mathcal{R}, t)$ 构建3D视锥体，即相机可见的空间金字塔区域。
- **物体-视锥体交集度量**：针对不同标注类型（分割掩码、边界框、点位置），分别计算物体与视锥体的交集比率 $\phi_{seg}$、$\phi_{box}$、$\phi_{point}$，作为该姿态与目标物体相关性的量化指标。
- **Z-buffer可见性验证**：建立深度缓冲区，仅保留未被遮挡的可见点，确保恢复的姿态在几何上真实可行。
- **候选姿态列表生成**：为每个物体离线预计算所有相关相机姿态及其交集比率，供训练/推理时采样。

这一流水线完全自动化，无需人工标注，将原本“隐藏”在RGB-D序列外参中的姿态信息显式化为可用的监督信号。

### Changed Slot 2：姿态注入方式（PoseAlign三种变体）

**Baseline状态**：无姿态注入机制，模型仅依赖点云几何特征进行空间推理。

**创新方案**：提出三种互斥的姿态注入设计，将恢复的自车姿态整合到现有3D LMM中：

1. **PoseAlign-Transform（坐标变换）**：将输入点云通过 $(\mathcal{P}_{aligned} | 1)^{\top} = \mathcal{U} \mathcal{T}^{-1} (\mathcal{P} | 1)^{\top}$ 直接变换到恢复的相机坐标系，使“左/右/前/后”统一以自车为参考。这是最直接且效果最优的方案，其关键在于**保持点云编码器冻结**，避免编码器学习到世界坐标系的“位置捷径”。

2. **PoseAlign-Embed（特征嵌入）**：保持点云几何不变，在投影层特征上添加由姿态编码的偏移项 $f_{aligned} = f + \mathrm{MLP}(\mathrm{encode}(\mathcal{R}, t, \mathcal{P}_f))$。适用于点云嵌入预计算后无法修改的场景（如Chat-Scene）。

3. **PoseAlign-Prompt（文本提示）**：将姿态信息转化为文本描述注入LLM输入，效果有限但实现最为轻量。

### Changed Slot 3：姿态选择策略（Clip策略）

**Baseline状态**：无姿态选择机制。

**创新方案**：提出Clip策略——剔除交集分数最高和最低的 $X=30\%$ 候选姿态后随机采样。这一设计的动机在于平衡视角多样性与稳定性：最高交集分数的姿态往往是“正对”物体的极端视角，缺乏多样性；最低分数的姿态则与物体关联过弱。实验表明，Clip策略在ScanQA和Scan2Cap上优于直接选择最高交集分数的Top策略，验证了适度的姿态多样性对方向对齐至关重要。

### Changed Slot 4：数据增强策略的重新设计

**Baseline状态**：常规3D LMM训练中启用随机旋转、翻转、抖动、缩放等点云数据增强。

**创新方案**：在PoseAlign框架下**完全禁用**这些增强，以保留自车坐标对齐。姿态选择的随机性天然充当了旋转-平移增强，既保证了数据多样性，又不破坏方向信息的一致性。

### 创新的核心洞察

上述四个changed slots共同体现了一个核心洞察：**自车姿态是3D空间推理的“免费午餐”**——它可以从现有RGB-D数据中自动恢复，且仅需将点云转换到相机参考系即可让冻结的预训练编码器获得方向感知，无需架构改造或全量重训。这一洞察的强有力证据来自消融实验中的“Baseline PoseAlign-T”设置：基线模型在未训练的情况下直接输入变换后的点云，性能急剧下降，证明改进完全源于LLM生成的定位令牌质量的提升，而非视觉编码器利用了姿态捷径。此外，随机姿态替代PoseRecover恢复的姿态会导致性能下降，进一步验证了精确姿态恢复的必要性。

**方向感知的3D大型多模态模型（Direction-aware 3D LMMs）** 的整体框架由两个松耦合的核心模块构成：**PoseRecover**（离线姿态恢复流水线）与 **PoseAlign**（在线姿态注入机制）。两者通过“姿态选择策略”衔接，形成一条从原始ScanNet数据到方向感知推理的完整通路。

### 2.1 框架总览

整个系统遵循“离线预计算—在线注入”的范式，输入输出流如下：

1. **输入**：ScanNet-v2 场景的3D点云、RGB-D序列的相机内参 $K$ 与外参 $(\mathcal{R}, t)$、以及场景中物体的标注（分割掩码、边界框或位置标注）。
2. **PoseRecover（离线）**：对每个场景中的每个物体，穷举所有相机视角，计算物体与相机视锥体的交集比率，并经Z-buffer可见性验证，生成“物体—候选姿态”映射表。
3. **姿态选择（在线）**：在训练或推理时，根据查询涉及的目标物体，从候选姿态列表中按Clip策略采样一个合理的自车姿态。
4. **PoseAlign（在线）**：将选定的姿态注入现有3D LMM，具体通过**点云坐标变换**（PoseAlign-Transform）、**特征嵌入**（PoseAlign-Embed）或**文本提示**（PoseAlign-Prompt）三种可选机制实现。
5. **输出**：方向感知的3D视觉-语言推理结果（指代分割、问答、密集描述等）。

### 2.2 模块关系与数据流

两个核心模块是**解耦的**：PoseRecover 在训练前一次性完成，生成静态的姿态索引文件；PoseAlign 在训练/推理时读取该索引，无需重新计算视锥体或可见性。这种设计使得 PoseAlign 可以**即插即用**地接入不同架构的3D LMM backbone（LL3DA、LL3DA-SONATA、Chat-Scene、3D-LLAVA），而无需修改编码器结构。

关键的数据流瓶颈在于**姿态选择策略**。PoseRecover 为每个物体生成了多个候选相机姿态（对应不同RGB-D帧），直接选用交集分数最高的姿态（Top策略）会导致视角多样性不足；而完全随机采样则可能引入极端视角，破坏方向对齐的稳定性。为此，框架采用**Clip策略**：先剔除交集分数最高和最低的 $X=30\%$ 候选姿态，再从剩余候选中等概率随机采样。该策略在视角多样性与姿态稳定性之间取得平衡，是性能提升的关键超参数。

### 2.3 训练与推理流程

在训练阶段，所有点云数据增强（随机旋转、翻转、抖动、缩放）被**完全禁用**，以保持自车坐标对齐的纯粹性。姿态选择的随机性天然充当了旋转-平移增强，避免了额外数据扰动对方向语义的破坏。点云编码器保持冻结，仅对投影层和LLM的LoRA参数进行指令微调，确保性能增益源于更好的方向建模，而非视觉特征捷径。

在推理阶段，对于给定的文本查询，系统根据查询中提及的目标物体检索对应的候选姿态列表，经Clip采样后，将点云变换到相机坐标系，再由冻结的编码器提取特征，最终由LLM生成方向一致的响应。

> **注意**：PoseRecover 恢复的姿态局限于 ScanNet 中离散的 RGB-D 视角，无法覆盖诸如“站在橱柜上”或“蹲在桌子下”等非典型视角。此外，方法假设 agent 可通过 SLAM 获取准确的相机外参，未考虑传感器标定误差或同步噪声的影响。

### 3.1 问题形式化：方向模糊性的根源

现有3D室内基准测试（ScanRefer、ScanQA、Scan2Cap等）中的语言查询大量依赖方向性空间推理，但数据集完全缺失自车姿态信息。经统计，ScanQA中46.7%、Scan2Cap中89.7%、SQA3D中95.2%的问题需要明确的方向判断（如“左边的椅子”“前方的桌子”），这些查询在缺乏自车参考系的条件下本质上构成不适定问题——模型无法确定“左/右/前/后”以谁为准。本文的核心洞察是：**自车姿态是3D空间推理的“免费午餐”**——它可以从ScanNet RGB-D序列的外参中自动恢复，且仅需将点云转换到相机参考系即可让冻结的预训练编码器获得方向感知，无需架构改造或全量重训。

### 3.2 PoseRecover：自车姿态自动恢复流水线

PoseRecover 是一个全自动的离线数据生成流水线，为每个文本-场景对恢复与查询相关的相机姿态。其核心流程如下：

**（1）视锥体计算与物体交集检测**

给定ScanNet-v2的相机内参矩阵 $K$ 和外参 $(\mathcal{R}, t)$，首先将世界坐标系下的点云 $p_i$ 变换到相机坐标系：

$$(x_i', y_i', z_i')^{\mathsf{T}} = \mathcal{R}^{-1} (p_i - t) \tag{1}$$

随后利用内参矩阵 $K$ 将相机系坐标投影到图像平面，获得像素坐标 $(u_i, v_i)$：

$$(u_i, v_i, 1)^{\mathtt{T}} = \lfloor K (x_i', y_i', z_i')^{\mathtt{T}} / z_i' \rfloor \tag{2}$$

**（2）Z-Buffer可见性验证**

为每个像素建立深度缓冲区，保存最小深度值，确保仅保留未被遮挡的可见点：

$$Z_{\mathcal{P}}^{u_i, v_i} = \min_{j | (u_j, v_j) = (u_i, v_i)} (z_j') \tag{3}$$

**（3）交集比率计算**

根据标注类型，采用不同策略计算物体与视锥体的交集比率：

- **分割掩码**：计算物体掩码 $M_{obj}$ 内可见点的比例：

$$\phi_{seg} = \frac{1}{|M_{obj}|} \sum_{\substack{k \in M_{obj}, 0 \le u_k < U, 0 \le v_k < V}} \mathbb{I}[z_k' < Z_{\mathcal{P}}^{u_k, v_k} + \delta] \tag{4}$$

- **边界框**：采用蒙特卡洛采样估计框与视锥体的交集比率：

$$\phi_{box} = \frac{1}{|\mathcal{P}_{sample}|} \sum_{p \in \mathcal{P}_{sample}} \mathbb{I}[p \in F] \tag{5}$$

**（4）候选姿态列表生成**

为每个物体离线预计算所有相机姿态及其交集比率，形成候选姿态列表，供训练和推理时采样（Figure 2）。

![[assets/figures/papers/paper_list_l2382_https_arxiv_org_abs_2602_19063/figures/002_Figure_2.jpg]]
*Figure 2: The offline data generation pipeline for PoseRecover. (a) Object annotations and camera poses are obtained from ScanNetv2 [12]. Camera poses and objects are downsampled for visibility. Zoom in for details. (b) PoseRecover exhaustively calculates the intersection rates between objects and camera frustums. (c) Visibility of the intersection is further validated with a z-buffer. (d) These intersection rates are saved and later sampled during training or inference to supplement ego poses to models*

### 3.3 姿态选择策略：Clip截断采样

直接选择交集分数最高的姿态（Top策略）会导致视角多样性不足。本文提出**Clip策略**：剔除交集分数最高和最低的 $X$ 比例候选后，从剩余姿态中随机采样。默认 $X=0.3$，平衡了视角多样性与姿态稳定性。KDE分析（Figure 4）表明，随着Clip Ratio增大，候选姿态间的最大偏航角差迅速集中在零附近，验证了该策略的有效性。

### 3.4 PoseAlign：三种姿态注入方案

本文设计了三种互斥的姿态注入方式，将恢复的自车姿态融入现有3D LMM架构（Figure 3）：

**（1）PoseAlign-Transform（坐标变换）**

直接将输入点云从世界坐标系变换到恢复的相机坐标系，并适配编码器所需的坐标轴约定（front-left-up）：

$$(\mathcal{P}_{aligned} | 1)^{\top} = \mathcal{U} \mathcal{T}^{-1} (\mathcal{P} | 1)^{\top}, \quad \mathcal{T} = \begin{bmatrix} \mathcal{R} & t \\ 0 & 1 \end{bmatrix} \tag{8}$$

其中 $\mathcal{U}$ 为坐标轴转换矩阵。该方案使“左/右/前/后”统一以自车为参考，冻结的点云编码器可直接感知方向信息。同时，训练中**完全禁用**随机旋转、翻转、抖动、缩放等常用点云增强，以保持自车坐标对齐；姿态采样的随机性天然充当了旋转-平移增强。

**（2）PoseAlign-Embed（特征嵌入）**

保持点云几何不变，在投影层特征上添加由姿态编码的偏移项：

$$f_{aligned} = f + \mathrm{MLP}(\mathrm{encode}(\mathcal{R}, t, \mathcal{P}_f)) \tag{9}$$

该方案适用于依赖预计算点云嵌入的模型（如Chat-Scene）。

**（3）PoseAlign-Prompt（文本提示）**

将姿态信息转化为文本提示注入LLM输入，属于最轻量的注入方式。

### 3.5 训练策略

所有变体均保持点云编码器冻结，仅对投影层和LLM的LoRA参数进行指令微调，避免模型学习位置捷径。消融实验证实：基线模型在未训练的情况下直接输入变换后的点云（Baseline PoseAlign-T）性能急剧下降，说明改进完全归因于LLM生成的定位令牌质量的提升，而非视觉编码器利用了姿态捷径。

## 实验与关键发现

### 1. 实验设置

#### 1.1 基准模型与数据集

为验证方法的通用性，作者在四种架构迥异的3D LMM骨干网络上应用PoseAlign修改：**LL3DA**（点云编码器+Q-Former）、**LL3DA-SONATA**（SONATA编码器替代）、**Chat-Scene**（检测器提取物体令牌）和**3D-LLAVA**（超点Transformer）。除Chat-Scene因其依赖预计算点云嵌入而采用PoseAlign-Embed外，其余模型均使用PoseAlign-Transform。

评估覆盖五个标准3D视觉-语言基准：**ScanRefer**（指代分割）、**Multi3DRefer**（多目标指代分割）、**ScanQA**（问答）、**SQA3D**（情景问答）和**Scan2Cap**（密集描述）。主要指标包括：ScanRefer/Multi3DRefer的mIoU，ScanQA/SQA3D的LLM-as-judge准确率（L-A），以及Scan2Cap的CiDEr@0.5（C@0.5）和LLM-as-judge准确率。

#### 1.2 公平性控制

为确保对比公平，实验采取了严格的控制措施：

- **数据增强禁用**：所有PoseAlign变体均禁用常用的点云数据增强（随机旋转、翻转、抖动、缩放），以保持自车坐标对齐。姿态选择的随机性天然充当了旋转-平移增强。
- **统一训练协议**：基线模型与改进模型在相同的PoseRecover基准下训练，batch size、优化器保持一致。基线模型不接收姿态信息，改进模型接收额外姿态输入。
- **编码器冻结**：所有方法的点云编码器均保持冻结，仅微调投影层和LLM的LoRA参数，确保改进源于更好的方向建模而非视觉特征捷径。
- **LLM-as-judge双模型验证**：使用GPT-OSS-20B和GPT-5-mini两套模型进行LLM-as-judge评估，结果一致，验证了该指标的可靠性。

### 2. 主要结果

#### 2.1 跨模型一致性提升

Table 1展示了各基线模型及其PoseAlign变体在五个基准上的性能对比。核心发现是：**PoseAlign在所有骨干网络上均带来一致的性能提升**，验证了自车姿态作为通用方向锚点的有效性。

以3D-LLAVA为例（Table 2），PoseAlign-Transform（Clip X=0.3）在ScanRefer上取得**55.4% mIoU**，相比基线42.6%提升**+12.8个百分点（相对提升30.0%）**；在Multi3DRefer上达到54.3% mIoU（基线48.1%，+6.2 pp）。在Scan2Cap上，LLM-as-judge准确率从28.1%提升至31.4%（+3.3 pp）；ScanQA上从45.7%提升至47.3%（+1.6 pp）。

![[assets/figures/papers/paper_list_l2382_https_arxiv_org_abs_2602_19063/figures/006_Table_2.jpg]]
*Table 2: Ablation experiment on 3D-LLAVA. ‘Baseline PoseAlign-T’ is the performance of the baseline model on PoseAlign-T data, where the input point cloud is transformed to the camera location following Equation 8. ‘Random Pose’ uses random camera poses instead of those found by PoseRecover*

值得注意的是，**3D-LLAVA + PoseAlign-T在ScanRefer上超越了所有对比方法**，包括传统专家模型（如Scan2Cap、ScanQA）和其他3D LMM基线。

#### 2.2 方向关键子集验证

Table 4专门评估了方向关键问题子集上的表现。在ScanQA的方向关键问题上，3D-LLAVA + PoseAlign-T将LLM-as-judge准确率从基线的36.6%提升至**40.3%**（+3.7 pp），直接验证了方法专门解决了方向模糊性这一核心瓶颈。该子集的问题均涉及“左/右/前/后”等方向性空间关系，在无自车姿态时构成不适定问题。

### 3. 消融实验

#### 3.1 姿态注入方式对比

Table 2系统对比了三种PoseAlign变体（Transform、Embed、Prompt）在3D-LLAVA上的表现：

- **PoseAlign-Transform**在指代分割任务上显著优于其他两种方案：ScanRefer mIoU达55.4%，而Embed仅46.4%、Prompt仅44.9%。这表明直接对点云进行坐标变换是最有效的姿态注入方式。
- **PoseAlign-Embed和PoseAlign-Prompt**在ScanQA上表现接近Transform（47.0%和46.9% vs 47.3%），但在需要精确空间定位的指代分割任务上差距明显。

#### 3.2 姿态恢复的必要性

**随机姿态实验**（Table 2 “Random Pose”）使用随机相机姿态替代PoseRecover恢复的姿态，导致ScanRefer mIoU从55.4%降至51.3%，Scan2Cap LLM-as-judge准确率从31.4%降至28.7%。这证明**精确的姿态恢复是性能提升的关键**，随机姿态无法提供有效的方向锚点。

**Baseline PoseAlign-T实验**（Table 2）将基线模型直接应用于变换后的点云（未经训练），性能急剧下降（ScanRefer mIoU仅39.0%）。这排除了视觉编码器利用姿态捷径的可能性，确认改进完全归因于LLM生成的`<SEG>`令牌质量的提升。

#### 3.3 Clip策略与超参数

Table 3和Figure 4分析了Clip Ratio X的影响。Clip策略剔除交集分数最高和最低的X=30%候选后随机采样，平衡视角多样性与稳定性：

- **X=0.3**在ScanQA和Scan2Cap上达到最优LLM-as-judge准确率。
- Figure 4的KDE分布显示，随着Clip Ratio增加，候选姿态间的最大偏航角差异迅速向零集中——更高Clip Ratio降低数据多样性但提升姿态稳定性。
- 完全参数调优实验（Tables 7和8）进一步验证X在0.3附近表现最佳。

### 4. 鲁棒性分析

Table 5展示了方法对姿态噪声的鲁棒性。在恢复的姿态上添加均匀分布的误差后，PoseAlign-T的性能虽有下降但仍显著优于基线，表明方法对一定程度的姿态不精确具有容忍度。这一特性对实际部署中SLAM可能存在的标定误差具有积极意义。

### 5. 失败模式与局限

尽管PoseAlign在多个基准上表现优异，论文也识别了以下局限：

1. **姿态恢复依赖精确外参**：方法假设agent可通过SLAM获取准确的相机外参，未考虑传感器标定误差或同步噪声的极端情况。
2. **视角覆盖受限**：恢复的姿态局限于ScanNet中离散的RGB-D视角，无法覆盖诸如“站在橱柜上”或“蹲在桌子下”等非典型视角。
3. **编码器敏感性依赖**：方法依赖点云编码器对坐标变换的敏感性；若编码器采用旋转不变设计，PoseAlign-Transform的效果可能减弱。
4. **静态环境假设**：当前方法仅针对静态室内环境，未涉及动态场景或室外环境，其中布局和自车运动持续变化。

### 6. 关键图表结论

- **Table 1**：PoseAlign在四种不同架构的3D LMM上均带来一致提升，验证方法的通用性。
- **Table 2**：PoseAlign-Transform在指代分割任务上显著优于Embed和Prompt方案；随机姿态和未训练基线实验排除了混淆因素。
- **Table 3 / Figure 4**：Clip Ratio X=0.3在姿态多样性与稳定性之间取得最优平衡。
- **Table 4**：方向关键子集上的提升直接验证方法解决了方向模糊性这一核心瓶颈。
- **Table 5**：方法对姿态噪声具有一定鲁棒性。
- **Figure 5**（定性对比）：基线模型在世界坐标系下常产生方向错误，而PoseAlign-Transform将坐标系对齐到恢复的自车姿态后，能正确推理空间关系。

![[assets/figures/papers/paper_list_l2382_https_arxiv_org_abs_2602_19063/figures/005_Table_1.jpg]]
*Table 1: Cross-dataset performance comparison on multiple 3D vision-language tasks. ‘PC’ and ‘I’ represent point cloud and image modalities, respectively. Major metrics are highlighted with gray background. Performance on PoseRecover benchmark may differ from those in the original papers due to retraining with lower batch sizes. Baselines in PoseRecover benchmark are comparable with all methods because they do not use pose information, while our modifications are comparable within the benchmark due to additional pose input*

![[assets/figures/papers/paper_list_l2382_https_arxiv_org_abs_2602_19063/figures/007_Table_3.jpg]]
*Table 3: Parameter tuning experiment for Clip Ratio X of PoseAlign-Transform on 3D-LLAVA*

![[assets/figures/papers/paper_list_l2382_https_arxiv_org_abs_2602_19063/figures/008_Table_4.jpg]]
*Table 4: Performance on direction-critical question subset.9cm*

![[assets/figures/papers/paper_list_l2382_https_arxiv_org_abs_2602_19063/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative results of direction-critical questions for 3D-LLAVA baseline (top row) and PoseAlign-Transform (bottom row). The XYZ axes of the world coordinate frame are colored with red, green, and blue, respectively. The baseline paradigm uses default world coordinates of ScanNet-v2, which are non-informative. Instead, the PoseAlign paradigm aligns the coordinate frame to the recovered ego pose, providing an anchor for robust spatial reasoning. Red text highlights wrong answers and green text highlights correct answers*

## 定位与知识库关联

### 1. 核心洞察：自车姿态作为3D空间推理的“免费午餐”

本工作揭示了一个被现有3D视觉语言基准测试系统性忽视的关键瓶颈：**方向性空间推理的不适定性**。通过对ScanQA、Scan2Cap、SQA3D等主流基准的语言查询分析，发现40%至95%的查询依赖明确的方向推理（如“左边的椅子”、“前面的桌子”），但这些数据集完全缺失自车姿态信息，导致模型无法学习一致的方向语义（Section 3.1, Section B.2）。这一发现构成了本工作的核心动机——自车姿态并非奢侈品，而是3D空间推理的必需品。

论文提出的解决方案**PoseRecover + PoseAlign**的核心洞察在于：自车姿态可以自动从ScanNet RGB-D序列的外参中恢复，且仅需将点云转换到相机参考系即可让冻结的预训练编码器获得方向感知能力，无需架构改造或全量重训。这一“免费午餐”式的设计使其能以极小代价嵌入现有3D LMM管线。

### 2. 与基线方法的关系

本工作并非提出全新的3D LMM架构，而是设计了一种**即插即用的方向感知增强模块**，可应用于多种架构迥异的现有模型。实验覆盖了四类代表性基线：

- **LL3DA**：基于点云编码器 + Q-Former的经典架构，其PoseAlign-T变体在ScanQA上C指标达到76.7（Table 1）。
- **LL3DA-SONATA**：将LL3DA的点云编码器替换为SONATA编码器，验证了方法对编码器选择的鲁棒性。
- **Chat-Scene**：基于检测器提取物体令牌的架构，因其依赖预计算的点云嵌入，采用PoseAlign-Embed变体而非Transform（Section 5.1）。
- **3D-LLAVA**：基于超点Transformer的架构，作为主要消融平台，其PoseAlign-T变体在ScanRefer上mIoU从42.6提升至55.4（+30.0%相对提升），在Multi3DRefer上从48.1提升至54.3（Table 2, Section 5.3）。

值得注意的是，**所有PoseAlign变体均禁用了常用的点云数据增强**（随机旋转、翻转、抖动、缩放），以保持自车坐标对齐；姿态选择的随机性天然充当了旋转-平移增强（Section 5.1）。此外，**所有方法的点云编码器均保持冻结**，仅微调投影层和LLM的LoRA参数，确保性能提升源于更好的方向建模而非视觉特征捷径。关键证据在于：基线模型在未训练的情况下直接输入变换后的点云（Baseline PoseAlign-T）性能急剧下降，说明改进完全归因于LLM生成的`<SEG>`令牌质量的提升（Table 2, Section 5.3）。

与传统的专家模型（如Scan2Cap、ScanQA）相比，本工作聚焦于通用3D LMM的方向感知能力增强，而非针对单一任务的优化。Table 1中专家模型的性能可作为参考上限，但PoseAlign变体在多个任务上展现出更一致的跨任务泛化能力。

### 3. 方法谱系中的定位

从方法设计空间来看，PoseAlign探索了三种互斥的姿态注入方案（Figure 3）：

- **PoseAlign-Transform**（坐标变换）：将点云从世界坐标系变换到恢复的相机坐标系，等效于一种有语义意义的旋转-平移增强。这是最直接且最有效的方案，在指代分割任务上显著优于其他变体（Table 2, Section 5.3）。
- **PoseAlign-Embed**（特征调制）：在投影层特征上添加由姿态编码的偏移项，保持点云几何不变。适用于无法直接变换点云的架构（如Chat-Scene）。
- **PoseAlign-Prompt**（文本提示）：将姿态信息注入文本提示。效果有限，验证了在视觉侧注入姿态信息比在语言侧更有效。

在姿态恢复策略上，**Clip策略**（剔除交集分数最高和最低的X=30%候选后随机采样）优于Top策略（直接选最高交集分数），在ScanQA和Scan2Cap上达到最优LLM-as-judge准确率（Table 2, Table 3, Figure 4）。Figure 4的KDE分析揭示了其机理：随着Clip Ratio增大，候选姿态间的最大偏航角差异迅速向零集中，更高的Clip Ratio减少了数据多样性但提升了姿态稳定性，X=0.3在两者间取得最优平衡。

### 4. 适用边界与局限

本方法存在以下明确的适用边界：

1. **对准确外参的依赖**：PoseRecover假设agent可通过SLAM获取准确的相机外参。Table 5的鲁棒性实验表明，添加均匀姿态误差会导致性能下降，但方法在适度噪声下仍保持一定鲁棒性。然而，论文未考虑传感器标定误差或同步噪声对姿态恢复的累积影响，这在真实部署中可能成为瓶颈。

2. **视角覆盖的局限性**：恢复的姿态局限于ScanNet中离散的RGB-D视角，无法覆盖诸如“站在橱柜上”或“蹲在桌子下”等非典型视角。这意味着模型可能在这些非分布内视角下表现退化。

3. **对编码器设计的敏感性**：PoseAlign-Transform的效果依赖点云编码器对坐标变换的敏感性。若编码器采用旋转不变设计（如部分基于相对位置编码的架构），坐标变换可能无法有效传递方向信息，此时PoseAlign-Embed或-Prompt可能更适用，但效果有限。

4. **静态室内环境的限制**：当前方法仅针对ScanNet-v2的静态室内场景，未涉及动态场景或室外环境，其中布局和自车运动持续变化。Figure 6显示即使在PoseAlign自车坐标下，物体分布仍呈现非平凡模式，暗示室外或动态场景的泛化需要更复杂的姿态建模。

### 5. 开放问题

1. **动态场景与连续ego motion的扩展**：如何将方向感知范式扩展到动态或室外场景，使agent在连续变化的ego motion中保持鲁棒的空间推理？这可能需要引入时序姿态序列建模或相对姿态表示。

2. **姿态不确定性建模**：当SLAM提供的姿态存在显著噪声时，能否通过不确定性建模（如概率姿态编码）或在线优化（如迭代姿态精调）进一步提升方向对齐的鲁棒性？Table 5仅探索了均匀噪声，更真实的噪声模型（如累积漂移）有待研究。

3. **无物体标注场景的姿态估计**：如何为类似SQA3D这样缺少物体标注的数据集自动估计与问题相关的合理“自车姿态”，以扩大方法的适用范围？当前PoseRecover依赖分割掩码、边界框或位置标注来计算交集比率，无标注场景需要全新的启发式方法。

4. **更富表达力的姿态表示**：是否可以通过连续姿态序列或相对姿态（如“从A到B的视角”）来进一步提升复杂空间关系推理（如“经过椅子后左转看到的桌子”）的性能？当前方法仅使用单帧离散姿态，可能不足以捕捉路径依赖的空间语义。

5. **跨域泛化与基础模型整合**：当前方法在ScanNet上验证，其在其他室内数据集（如ARKitScenes、HM3D）或仿真环境（如Habitat）上的泛化能力尚未探索。此外，如何将方向感知能力整合到更大规模的基础模型中（如从零预训练阶段就引入自车姿态）是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Direction_aware_3D_Large_Multimodal_Models.pdf]]
