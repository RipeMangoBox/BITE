---
title: "PartField: Learning 3D Feature Fields for Part Segmentation and Beyond"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/PartField_Learning_3D_Feature_Fields_for_Part_Segmentation_and_Beyond.pdf
aliases:
- PartField
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "前馈网络一次性预测连续特征场，用特征距离隐式编码部件与层级，无需文本提示或模板，并通过三元组对比学习吸收多源、多尺度的部件提案。"
primary_logic: "三元组对比损失仅要求正样本距离小于负样本距离（相对关系），自然绕过了多尺度部件和不同定义的冲突，无需显式尺度条件，使得大规模多源训练可行，同时前馈设计带来显著速度与鲁棒性提升。"
claims:
- "PARTFIELD在PartObjaverse-Tiny上平均mIoU达79.18，比次优方法SAMesh（56.86）提高超过22.3%，推理仅需约10秒，而SAMesh需~7分钟。"
- "用三元组损失替代绝对距离约束，避免多尺度冲突，并能训练于2D SAM掩码与3D标签的混合数据。"
- "硬负样本采样（3D-hard、feature-hard）显著提升边界清晰度，表3和Fig.10证实有效。"
- "PartObjaverse-Tiny 上 mIoU (类别无关部件分割) = 79.18"
---

# PartField: Learning 3D Feature Fields for Part Segmentation and Beyond

> [!tip] 核心洞察
> 三元组对比损失仅要求正样本距离小于负样本距离（相对关系），自然绕过了多尺度部件和不同定义的冲突，无需显式尺度条件，使得大规模多源训练可行，同时前馈设计带来显著速度与鲁棒性提升。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | PartField：学习用于部件分割及其他任务的3D特征场 |
| 英文题名 | PartField: Learning 3D Feature Fields for Part Segmentation and Beyond |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2504.11451); [Project](https://research.nvidia.com/labs/toronto-ai/partfield-release/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PartField |
| Dataset | PartObjaverse-Tiny, PartNetE, 推理时间 (PartObjaverse-Tiny) |

> [!tip] 效果简介
> - PartObjaverse-Tiny 上，mIoU (类别无关部件分割) 为 79.18，对比 56.86 (SAMesh)，变化 +22.32 (相对提升39.2%)。
> - PartNetE 上，mIoU (类别无关部件分割) 为 59.10，对比 43.86 (SAMPart3D, 次优非自身方法)，变化 +15.24。
> - 推理时间 (PartObjaverse-Tiny) 上，单形状推理时间 为 ~10秒，对比 ~7分钟 (SAMesh) / ~15分钟 (SAMPart3D) / ~1.5小时 (Ultrametric)，变化 快40-540倍。

## 概述

开放世界中的3D部件分割面临一个核心瓶颈：现有方法要么依赖文本提示（如PartSLIP、Find3D），限制了通用性；要么采用逐形状优化的策略（如Ultrametric Feature Field、SAMesh、SAMPart3D），导致推理缓慢、多视图不一致，且难以兼容不同粒度的部件定义。PartField针对这一瓶颈，提出了一种前馈式连续特征场方法，其核心因果机制在于：通过一次前向传播即可预测整个3D形状的部件特征场，用特征向量间的距离隐式编码部件归属与层级关系，无需任何文本提示或预定义模板。

该方法的关键创新在于训练范式的转变。PartField采用三元组对比损失，仅要求正样本对（同一部件内的点）的距离小于负样本对（不同部件的点）的距离，这种相对约束天然绕过了多尺度部件定义之间的冲突，无需显式的尺度条件。这使得模型能够在大规模混合数据上进行训练——包括来自2D基础模型（如SAM2）的多视图掩码提案和来自PartNet等数据集的3D标签——从而吸收多源、多粒度的部件知识。

在PartObjaverse-Tiny基准上，PartField取得了79.18的mIoU，相较于次优方法SAMesh的56.86提高了超过22.3个百分点（相对提升39.2%），同时推理时间仅需约10秒，而SAMesh需要约7分钟，速度提升超过40倍。在PartNetE测试集上，PartField同样以59.10的mIoU显著优于SAMPart3D的43.86。消融实验进一步证实，混合硬负样本采样策略（均匀采样、3D-hard、feature-hard）对提升部件边界清晰度至关重要，将mIoU从77.70提升至79.20。

在方法谱系上，PartField属于前馈式3D特征场学习范式，区别于文本驱动的零样本方法和逐形状优化的NeRF/高斯方法。其连续特征场表示不仅支持高效的部件分割，还展现出跨形状的一致性，可应用于共分割、交互式选择、点对点对应等下游任务。

## 背景与动机

3D形状的部件理解是计算机图形学与视觉领域的长期目标，支撑着形状编辑、运动规划、机器人交互等一系列下游任务。传统有监督方法依赖预定义的部件模板和大量人工标注，难以泛化到开放世界中千差万别的物体类别与部件粒度。近年来，开放世界3D部件分割方法试图突破这一限制，但现有路线存在根本性矛盾。

**文本驱动方法的通用性困境。** 以 **PartSLIP** 和 **Find3D** 为代表的文本驱动方法，通过将3D部件与自然语言描述对齐来实现零样本分割。然而，这种范式将部件定义绑定于文本提示的质量与覆盖度——当物体类别超出语言描述范围，或同一物体在不同任务中需要不同粒度的部件划分时，文本驱动方法难以提供一致的解决方案。

**逐形状优化方法的效率与一致性瓶颈。** 另一类方法，如 **Ultrametric Feature Field**（基于NeRF的逐形状特征场优化）、**SAMesh**（基于SAM2多视图融合的表面部件分解）和 **SAMPart3D**（局部微调蒸馏多视图特征），虽然避免了对文本提示的依赖，但每个形状都需要独立的优化过程。这导致三个严重问题：其一，推理速度极慢——SAMesh约需7分钟，SAMPart3D约需15分钟，Ultrametric Feature Field更长达1.5小时，难以支撑交互式应用；其二，多视图融合过程中的不一致性使得部件边界模糊；其三，逐形状优化缺乏跨形状的共享知识，不同形状的部件定义难以对齐。

**多尺度部件定义的冲突。** 更深层的瓶颈在于：一个3D点在不同粒度下可能属于不同的部件。例如，摩托车把手在粗粒度下与车身前部属于同一部件，在细粒度下则独立为单独部件。现有方法采用绝对距离推拉损失，要求显式指定尺度条件来约束特征距离，这使得多尺度训练数据——尤其是来自2D基础模型（如SAM）的掩码提案与3D人工标签的混合数据——之间存在不可调和的冲突，阻碍了大规模多源训练。

**PartField的动机。** 针对上述缺口，PartField提出了一种根本性的范式转变：用前馈网络一次性预测连续特征场，以特征距离隐式编码部件归属与层级结构。其核心洞察在于：三元组对比损失仅要求正样本距离小于负样本距离这一相对关系，自然绕过了多尺度部件定义的冲突，无需显式尺度条件，使得大规模多源训练成为可能。同时，前馈设计带来了推理速度与跨形状一致性的显著提升。

## 核心创新

PartField 的核心创新在于用**连续特征场 + 三元组对比学习**替代了传统开放世界部件分割中的文本提示依赖或逐形状优化范式，实现了前馈式、多尺度、多源数据兼容的部件分解。

### 1. 从显式定义到隐式特征场：部件表示形式的根本转变

传统方法要么依赖预定义的部件模板或文本提示（如 **PartSLIP**、**Find3D**），要么通过逐形状优化来生成部件（如 **Ultrametric Feature Field**、**SAMesh**）。PartField 则预测一个连续的 3D 特征场 $f(\mathbf{p};S): \mathbb{R}^3 \to \mathbb{R}^n$，直接用特征向量间的距离隐式编码部件归属——两点特征越近，越可能属于同一部件。这一设计使得模型无需任何文本提示或模板即可工作，且天然支持跨模态输入（网格、点云、高斯散点等）。

### 2. 从逐形状优化到前馈预测：训练范式的跃迁

基线方法（如 SAMesh 约需 7 分钟/形状，SAMPart3D 约需 15 分钟/形状，Ultrametric Feature Field 约需 1.5 小时/形状）均需对每个新形状进行独立的优化或融合过程，推理慢且多视图一致性难以保证。PartField 采用一次性前馈网络，推理时间仅约 10 秒，速度提升 40–540 倍，同时避免了逐形状优化带来的不一致性问题。这一范式转变的关键在于：模型在训练阶段已从大规模混合数据中吸收了部件先验，测试时无需任何迭代优化。

### 3. 从绝对距离约束到相对关系约束：损失函数的核心洞见

这是 PartField 最关键的创新。先前工作（如 SAMPart3D）使用推拉损失（pull/push loss），直接最小化或最大化点对间的特征绝对距离，这要求显式的尺度条件来应对不同粒度的部件定义，否则多尺度冲突难以调和。如图 4 所示，同一点在不同粒度下可能属于不同部件，绝对距离约束会强制矛盾的目标。

PartField 转而采用三元组对比损失，仅要求正样本对的距离小于负样本对的距离（即相对关系），而不规定具体距离值：
$$\mathcal{L} = -\frac{1}{2} \Bigg( \log \left( \frac{\text{sim}(f(\mathbf{p}_a), f(\mathbf{p}_b))}{\text{sim}(f(\mathbf{p}_a), f(\mathbf{p}_b)) + \sum_{\mathbf{p}_c} \text{sim}(f(\mathbf{p}_a), f(\mathbf{p}_c))} \right) + \log \left( \frac{\text{sim}(f(\mathbf{p}_b), f(\mathbf{p}_a))}{\text{sim}(f(\mathbf{p}_b), f(\mathbf{p}_a)) + \sum_{\mathbf{p}_c} \text{sim}(f(\mathbf{p}_b), f(\mathbf{p}_c))} \right) \Bigg)$$
其中相似度定义为指数化余弦相似度 $\text{sim}(f(\mathbf{p}_u), f(\mathbf{p}_v)) = \exp(\cos(f(\mathbf{p}_u), f(\mathbf{p}_v)) / \tau)$，$\tau$ 为可学习温度。

这一“弱化”的监督信号自然绕过了多尺度冲突：无论部件粒度如何定义，只要正样本间的相似度高于负样本即可，无需显式尺度条件。这使得模型能够同时吸收来自 2D SAM 掩码和 3D 标注的、粒度不一致的混合训练数据，大幅提升了数据利用效率。

### 4. 从简单负样本到混合硬负样本：边界质量的提升

PartField 引入三种负样本采样策略的混合：均匀采样（uniform）、3D 空间近邻采样（3D-hard，偏好欧氏空间更近的负样本）和特征空间近邻采样（feature-hard，偏好当前特征空间更近的负样本）。消融实验（Table 3）表明，混合硬负采样将 mIoU 从 77.70 提升至 79.20，且定性结果（Figure 10）显示部件边界显著更清晰。这一策略的关键在于：硬负样本集中在决策边界附近，迫使模型学习更精细的特征区分，尤其改善了部件交界处的分割质量。

### 创新总结

| 设计维度 | 基线方法 | PartField | 核心优势 |
|---------|---------|-----------|---------|
| 部件表示 | 文本提示/模板/逐形状优化 | 连续特征场（隐式距离） | 无文本依赖，通用性强 |
| 训练范式 | 逐形状优化/多视图融合 | 前馈网络一次性预测 | 推理快 40-540 倍 |
| 损失函数 | 绝对距离推拉（需尺度条件） | 三元组对比损失（仅相对关系） | 天然兼容多尺度、多源数据 |
| 负样本 | 随机/简单负样本 | 均匀+3D-hard+feature-hard 混合 | 边界更清晰 |

这些创新共同构成了 PartField 在 PartObjaverse-Tiny 上 mIoU 达 79.18（比次优方法 SAMesh 的 56.86 提升 22.3%）的核心驱动力。

## 整体框架

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_11451/figures/001_Figure_1.jpg]]
*Figure 1: We propose PARTFIELD, a feedforward model that predicts part-based feature fields for 3D shapes. The learned features can be clustered to yield a high-quality part decomposition, and our method outperforms the latest open-world 3D part segmentation approaches in both quality and speed. PARTFIELD can be applied to a wide variety of inputs in terms of modality, semantic class, and style. The learned feature field exhibits consistency across shapes, enabling applications such as cosegmentation, interactive selection, and correspondence*

PartField 的核心设计是一个**前馈式连续特征场预测器**，它以任意 3D 表示（网格、点云、3D 高斯散点等）为输入，单次前向传播即可输出一个覆盖整个形状的 3D 特征场，随后通过无监督聚类得到多尺度部件分解。整个 pipeline 由四个阶段构成：输入标准化、特征场编码、对比学习训练、聚类后处理。

### 输入标准化

无论原始 3D 表示是什么，PartField 首先将其统一转换为点云格式（Figure 3）。这一设计使模型天然兼容网格、点云、高斯散点等多种模态（Figure 2），无需针对不同表示设计独立编码器。

### 特征场编码器

特征场编码器采用 **PVCNN + 三平面 + Transformer** 的混合架构：

1. **PVCNN 编码**：对输入点云提取逐点特征，并沿三个正交平面（xy、xz、yz）投影聚合，形成初始三平面特征图（每个平面分辨率 $512^2$，128 通道）。
2. **下采样与 Transformer**：将三平面降采样至 $128^2$，每个像素作为一个 token，送入 6 层 Transformer 进行全局关系建模。
3. **上采样恢复**：Transformer 输出经转置 2D CNN 上采样回 $512^2$ 分辨率，得到最终的三平面特征场。

对于任意 3D 查询点 $\mathbf{p}$，将其投影到三个平面并检索对应特征向量，求和得到 448 维的最终特征 $f(\mathbf{p}; S): \mathbb{R}^3 \to \mathbb{R}^{448}$（Section 3.3, Training Details）。

### 对比学习训练

PartField 的核心洞见在于**用三元组对比损失替代绝对距离推拉损失**（Figure 4）。传统方法要求正样本对的距离逼近零、负样本对的距离趋近无穷大，这在多尺度部件场景下会产生冲突——同一对点在不同粒度下可能同时是正样本和负样本。PartField 的三元组损失仅要求正样本对的距离小于负样本对的距离（相对关系），自然绕过了这一冲突，无需显式尺度条件。

损失函数采用指数化余弦相似度：

$$\text{sim}(f(\mathbf{p}_u), f(\mathbf{p}_v)) = \exp(\cos(f(\mathbf{p}_u), f(\mathbf{p}_v)) / \tau)$$

其中 $\tau$ 为可学习温度参数。完整的三元组对比损失鼓励 $\text{sim}(f(\mathbf{p}_a), f(\mathbf{p}_b))$ 远大于所有负样本的相似度之和。

训练数据来自两方面的部件提案（part proposals）：
- **2D 提案**：对 Objaverse 等大规模无标注 3D 数据进行多视图渲染，利用 SAM2 提取 2D 类别无关掩码，投影回 3D 作为部件线索。
- **3D 提案**：利用 PartNet 等现有 3D 部件标注数据。

训练时从提案中在线采样三元组，并采用**混合硬负采样策略**（均匀采样、3D-hard、feature-hard），显著提升了部件边界的清晰度（Table 3, Figure 10）。整个模型在 8 块 A100 GPU 上训练约 2 周。

### 聚类后处理

推理时，对输入形状进行一次前馈即可获得所有点的特征向量。随后在网格面特征上应用**凝聚式聚类**（agglomerative clustering），利用面片连通性作为约束，生成层级化的部件分解（Figure 6）。整个推理流程约需 10 秒，比逐形状优化方法（如 SAMesh 约 7 分钟、SAMPart3D 约 15 分钟）快 40–540 倍（Table 1）。

### 关键设计取舍

- **前馈 vs 逐形状优化**：前馈设计使推理速度提升两个数量级，且天然保证多视图一致性，但代价是需要大规模预训练。
- **相对约束 vs 绝对约束**：三元组损失牺牲了对特征距离绝对尺度的控制，换取了多尺度兼容性和混合数据训练能力。
- **三平面 vs 体素/点云**：三平面在内存效率和表达能力之间取得平衡，但可能引入方向依赖性，对大角度旋转的跨形状一致性尚未充分验证（Limitations）。

## 核心模块与公式推导

### 连续特征场映射

PARTFIELD的核心表示是一个连续的三维特征场，将任意3D点映射到高维特征向量：

$$f(\mathbf{p};S): \mathbb{R}^3 \to \mathbb{R}^n$$

其中，$S$表示输入形状，$\mathbf{p}$为形状上的任意3D点，$n$为特征维度（实际实现中$n=448$）。该特征场的核心性质是：**特征距离隐式编码部件归属**——属于同一部件的点，其特征向量在潜在空间中距离较近；属于不同部件的点，其特征距离较远。

这种连续特征场的设计绕过了预定义模板和文本提示的依赖，使得部件定义完全由特征空间中的距离关系决定，天然支持不同粒度的部件分解。

### 三平面表示与特征查询

为实现高效的前馈预测，PARTFIELD采用三平面（triplane）作为特征场的隐式表示。具体流程如下：

1. **点云采样与PVCNN编码**：将任意3D表示（网格、点云、高斯散点等）统一转换为点云，通过PVCNN编码器提取逐点特征并投影到三个正交平面，形成初始三平面（空间分辨率$512^2$，128通道）。

2. **Transformer全局建模**：三平面首先下采样至$128^2$分辨率，每个像素作为token输入6层Transformer，建模全局上下文关系，再通过转置2D CNN上采样恢复至$512^2$分辨率。

3. **特征查询**：对于任意3D点$\mathbf{p}$，从三个平面分别检索特征并相加，得到448维特征向量$f(\mathbf{p};S)$。

这种前馈设计使得推理仅需约10秒，而逐形状优化的基线方法（如SAMesh需约7分钟，SAMPart3D需约15分钟）则慢40-540倍。

### 三元组对比损失

PARTFIELD的核心训练损失为三元组对比损失，其关键创新在于仅约束特征的**相对距离关系**，而非绝对距离。

**相似度函数**定义为指数化余弦相似度：

$$\text{sim}(f(\mathbf{p}_u), f(\mathbf{p}_v)) = \exp(\cos(f(\mathbf{p}_u), f(\mathbf{p}_v)) / \tau)$$

其中$\tau$为可学习的温度参数，控制特征空间的集中程度。

**完整三元组对比损失**为：

$$\mathcal{L} = -\frac{1}{2} \Bigg( \log \left( \frac{\text{sim}(f(\mathbf{p}_a), f(\mathbf{p}_b))}{\text{sim}(f(\mathbf{p}_a), f(\mathbf{p}_b)) + \sum_{\mathbf{p}_c} \text{sim}(f(\mathbf{p}_a), f(\mathbf{p}_c))} \right) + \log \left( \frac{\text{sim}(f(\mathbf{p}_b), f(\mathbf{p}_a))}{\text{sim}(f(\mathbf{p}_b), f(\mathbf{p}_a)) + \sum_{\mathbf{p}_c} \text{sim}(f(\mathbf{p}_b), f(\mathbf{p}_c))} \right) \Bigg)$$

其中，$\mathbf{p}_a$和$\mathbf{p}_b$为来自同一部件提案的正样本对，$\mathbf{p}_c$为负样本点。该损失的核心约束是：**正样本对的相似度应高于所有负样本对的相似度之和**，即仅要求相对排序关系$\text{sim}(f(\mathbf{p}_a), f(\mathbf{p}_b)) > \text{sim}(f(\mathbf{p}_a), f(\mathbf{p}_c))$，而非强制拉近或推远至特定绝对距离。

这一设计的关键优势在于：同一3D点在不同粒度的部件定义下可能属于不同部件（如Figure 4左侧所示），绝对距离推拉损失（如先前工作[21, 69]采用的pull/push loss）需要显式的尺度条件来区分这些冲突，而三元组损失仅依赖相对关系，**自然绕过了多尺度冲突**，使得大规模多源训练（混合2D SAM掩码与3D标签）成为可能。

### 硬负样本采样策略

为提升训练效率和部件边界清晰度，PARTFIELD采用混合负采样策略，从以下三种来源采样负样本$\mathbf{p}_c$：

- **均匀负样本（uniform）**：从整个形状中随机均匀采样，提供全局对比信号。
- **3D硬负样本（3D-hard）**：优先选择在欧氏空间中靠近$\mathbf{p}_a$的点，这些点在几何上接近但属于不同部件，对边界学习至关重要。
- **特征硬负样本（feature-hard）**：优先选择在当前特征空间中靠近$\mathbf{p}_a$但属于不同部件的点，提供最难的对比信号。

消融实验（Table 3）证实，混合使用三种硬负采样策略将mIoU从77.70提升至79.20，且Figure 10定性显示部件边界显著更清晰。

### 聚类后处理

在推理阶段，PARTFIELD对网格面特征应用凝聚式聚类（agglomerative clustering），利用网格面连通性约束，生成层级化的部件分解。通过调整聚类停止阈值，可从同一特征场中获得从粗到细的多尺度部件分割（如Figure 6所示），无需重新推理。

## 实验与分析

### 主要定量结果

PARTFIELD 在两个公开基准上进行了类别无关的部件分割评估，并与多个代表性基线方法进行了对比。

**PartObjaverse-Tiny 数据集**（Table 1）：
PARTFIELD 取得了 **79.18** 的平均 mIoU，显著优于次优方法 SAMesh 的 56.86（绝对提升 **+22.32**，相对提升 39.2%）。其他基线方法表现如下：SAMPart3D 为 53.47，Ultrametric Feature Field 为 46.83，PartSLIP 为 30.50，Find3D 为 24.66。在推理效率方面，PARTFIELD 的端到端处理时间约为 **10 秒**，而 SAMesh 需要约 7 分钟，SAMPart3D 需要约 15 分钟，Ultrametric Feature Field 需要约 1.5 小时——PARTFIELD 比这些逐形状优化的方法快 **40 至 540 倍**。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_11451/figures/006_Table_1.jpg]]
*Table 1: Quantitative evaluation of class-agnostic part segmentation on PartObjaverse-Tiny [69] dataset. We use instance-level labels and report mean IoU*

**PartNetE 测试集**（Table 2）：
PARTFIELD 取得了 **59.10** 的平均 mIoU，比次优非自身方法 SAMPart3D（43.86）高出 **+15.24**。值得注意的是，PartNetE 包含 1906 个形状，Ultrametric Feature Field 因单形状优化时间过长（累计约 1.5 小时/形状）而无法在此规模上完成评估，这进一步凸显了前馈方法的可扩展性优势。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_11451/figures/007_Table_2.jpg]]
*Table 2: Quantitative evaluation of class-agnostic part segmentation on the PartNetE [31] test set. We use Instance-level labels and report mean IoU. Please refer to the supplementary material for the category group mapping. We do not report results from Ultrametric [12] because of the lengthy runtime on 1906 shapes*

评估采用统一的实例级 mIoU 指标和网格面对齐流程，但需注意基线方法可能因网格拓扑、渲染质量等因素存在性能偏差。

### 消融实验

**训练数据源的影响**（Table 3）：
仅使用 Objaverse 的 2D 部件提案（无 3D 标注）训练即可获得 **77.70** 的 mIoU，表明大规模无标注数据通过 2D 基础模型蒸馏已能提供较强的部件先验。在此基础上加入 PartNet 的 3D 标注数据（仅占 Objaverse 子集约 8%，且仅覆盖 24 个类别），mIoU 进一步提升至 79.20，说明少量高质量 3D 监督在开放世界设定下仍能带来额外增益。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_11451/figures/011_Table_3.jpg]]
*Table 3: Quantative results for ablation study. We report mIoU scores on PartObjaverse-Tiny dataset [69]*

**负样本采样策略**（Table 3, Figure 10）：
- 仅使用均匀负采样（uniform）：mIoU 为 77.70
- 加入 3D-hard 负采样（偏好欧氏空间近邻）：mIoU 提升至 77.90
- 加入 feature-hard 负采样（偏好特征空间近邻）：mIoU 提升至 78.90
- 混合三种采样策略（uniform + 3D-hard + feature-hard）：mIoU 达到 **79.20**

Figure 10 的定性对比显示，硬负样本采样使部件边界更加清晰锐利。例如，椅子的扶手与座面交界处，使用硬负采样的结果边界分明，而仅用均匀负采样的结果存在模糊过渡。这一现象的原因在于：硬负样本集中在部件边界附近的难分点，迫使特征场学习更精确的边界判别能力。

### 层级分解与跨形状应用

**层级部件分解**（Figure 6）：
PARTFIELD 通过调整凝聚式聚类的停止阈值，可生成从粗粒度到细粒度的层级部件结构。例如，摩托车的前部组件在粗粒度下被合并为一个整体，随阈值降低逐步分离为把手、前轮等独立部件。这种层级特性源于三元组对比损失的相对距离约束——特征空间中相似度梯度自然编码了部件粒度的连续谱系，无需显式的尺度条件。

**共分割与对应**（Figure 8, Figure 9）：
- 共分割（Figure 8）：将源形状的部件标签通过特征相似度传播到目标形状，同类部件（如椅腿、扶手）在不同形状间被正确对应。
- 点对点对应（Figure 9）：基于 PARTFIELD 特征使用 Functional Maps 建立的跨形状对应关系，比 SAMPart3D 特征更准确，颜色转移的一致性更高。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_11451/figures/010_Figure_8.jpg]]
*Figure 8: Quantitative results on co-segmentation. We co-segment the shapes from the top row with the corresponding one on the bottom row. The same color indicates the same part. Figure 9. Point-to-point correspondences obtained by Functional Maps [43] using our learned features as input. In each group, the colormap defined on the source shape (left) is transferred to the target shape (right). On the top row, we compare with the features from SAMPart3D*

**交互式探索**（Figure 7）：
点击形状上任意一点，可实时显示该点与同形状内其他区域的特征相似度热力图，以及跨形状的相似区域。这验证了特征场的跨形状语义一致性——例如，点击一把椅子的扶手，另一把不同样式的椅子的扶手区域也会高亮响应。

### 失败模式与局限性

1. **场景尺度限制**：目前仅在物体尺度上验证，尚未扩展到大规模场景。聚类后处理依赖网格连通性，对非流形或不完整几何可能失效。

2. **方向敏感性**：特征场可能存在方向依赖性，对于大角度旋转的跨形状一致性未充分验证。Figure 8 和 Figure 9 的跨形状应用仅在小规模、姿态相近的形状对上展示，其泛化能力有待进一步检验。

3. **聚类依赖**：部件分解的质量依赖于凝聚式聚类的阈值选择和后处理步骤，目前缺乏自动确定最优粒度的方法。

4. **训练成本**：模型在 8 张 A100 GPU 上训练约 2 周，训练成本较高，但推理时仅需单次前馈即可完成。

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

现有开放世界3D部件分割方法面临三重困境：**文本依赖**、**逐形状优化**和**多尺度冲突**。**PartSLIP** 和 **Find3D** 等文本驱动方法需要为每个部件提供语言描述，限制了通用性；**Ultrametric Feature Field** 和 **SAMesh** 等逐形状优化方法则需对每个新形状进行多视图融合与NeRF/高斯优化，单形状推理耗时从数分钟到数小时不等，且多视图一致性难以保证。更关键的是，这些方法采用的绝对距离推拉损失（pull-and-push loss）要求显式指定部件尺度条件，无法兼容不同粒度的部件定义——一个点在不同尺度下可能同时属于不同部件。

PARTFIELD的核心洞察在于：**用三元组对比损失替代绝对距离约束，仅要求正样本距离小于负样本距离（相对关系），自然绕过多尺度冲突**。这使得大规模多源训练（2D SAM掩码与3D标签混合数据）成为可能，同时前馈设计带来显著的速度与鲁棒性提升。

### 与基线方法的本质差异

| 维度 | 文本驱动方法 | 逐形状优化方法 | PARTFIELD |
|------|-------------|---------------|-----------|
| **部件表示** | 文本提示匹配 | 预定义模板/优化规则 | 连续特征场，特征距离隐式定义部件与层级 |
| **训练范式** | 零样本或微调 | 逐形状优化（多视图融合+NeRF） | 一次性前馈预测，大规模混合数据训练 |
| **损失函数** | 文本-特征对齐 | 绝对距离推拉（需尺度条件） | 三元组对比损失（仅相对距离约束） |
| **推理时间** | ~分钟级 | ~7分钟-1.5小时 | ~10秒 |
| **多尺度支持** | 依赖文本粒度 | 需显式尺度条件 | 隐式编码于特征距离 |

**SAMesh** 作为基于SAM2多视图融合的表面部件分解方法，在PartObjaverse-Tiny上达到56.86 mIoU，但需约7分钟推理；**SAMPart3D** 通过局部微调蒸馏多视图特征达到53.47 mIoU，推理约15分钟。PARTFIELD以79.18 mIoU（提升22.3%）和~10秒推理实现了数量级跨越。

### 关键设计选择与消融证据

**三元组对比损失的相对性优势**（Figure 4）：传统推拉损失要求$f(A)$与$f(B)$的绝对距离小于$f(A)$与$f(C)$的绝对距离，当A、B、C的部件归属因尺度而异时产生冲突。PARTFIELD仅要求$sim(f(A), f(B)) > sim(f(A), f(C))$，这种相对关系在不同尺度下均可成立，无需显式尺度条件。

**硬负样本采样的边界增强**（Table 3, Figure 10）：混合均匀采样、3D-hard（欧氏空间近邻负样本）和feature-hard（特征空间近邻负样本）三种策略，将mIoU从77.70提升至79.20，且部件边界显著更清晰。这一设计解决了对比学习中简单负样本导致边界模糊的经典问题。

**多源数据混合训练**（Table 3）：仅用无标注Objaverse的2D SAM提案训练即可获得较好结果，加入少量PartNet 3D标签（仅占Objaverse子集的8%，24个类别）带来额外增益。这验证了方法对弱监督信号的吸收能力。

### 方法边界与失效模式

**场景尺度限制**：当前仅在物体尺度上验证，尚未扩展到大规模场景。特征场的表达能力在复杂场景几何下可能退化，且聚类后处理依赖网格连通性，对非流形或不完整几何可能失效。

**方向敏感性**：特征场可能存在方向依赖性，对于大角度旋转的跨形状一致性未充分验证。Figure 7和Figure 9展示的跨形状特征相似性和点对点对应仅在小规模上验证，泛化能力有待检验。

**聚类后处理的耦合**：当前部件分解依赖凝聚式聚类，聚类阈值的选择直接影响部件粒度。虽然特征场本身编码了层级信息，但从连续特征到离散部件的映射仍是一个开放问题。

### 开放问题与未来方向

1. **场景级扩展**：如何将PARTFIELD扩展到大型场景并保持高效推理？可能需要层次化特征场或自适应分辨率策略。
2. **弱监督/自监督**：能否通过弱监督或自监督进一步减少对3D标签的依赖？当前2D提案已展示潜力，但完全无监督的部件发现仍是挑战。
3. **姿态不变性**：如何解决特征场的方向敏感性，使其在任意姿态下保持跨形状一致性？可能需要显式的姿态归一化或等变特征设计。
4. **下游任务迁移**：学习到的连续特征场能否直接用于运动估计、物理模拟等任务而不需要额外微调？这考验特征空间的泛化性和物理合理性。
5. **可解释性与控制**：如何让用户控制部件分解的粒度？当前聚类阈值是全局参数，未来可能需要交互式或条件化的粒度控制机制。

## 原文 PDF

![[paperPDFs/ICCV_2025/PartField_Learning_3D_Feature_Fields_for_Part_Segmentation_and_Beyond.pdf]]
