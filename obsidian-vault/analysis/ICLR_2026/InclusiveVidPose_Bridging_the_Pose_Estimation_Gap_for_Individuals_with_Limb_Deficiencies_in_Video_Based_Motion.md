---
title: "InclusiveVidPose: Bridging the Pose Estimation Gap for Individuals with Limb Deficiencies in Video-Based Motion"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/InclusiveVidPose_Bridging_the_Pose_Estimation_Gap_for_Individuals_with_Limb_Deficiencies_in_Video_Based_Motion.pdf
openreview_forum_id: SyQqXAdWUq
aliases:
- IL
- InclusiveVidPose
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "针对肢体缺陷人群构建大规模视频数据集InclusiveVidPose，引入残肢端点关键点（扩展至25点）和评估置信度一致性的新指标LiCC。"
primary_logic: "通过视频级别标注、个性化关键点模式、残肢端点定义以及LiCC指标，揭示了现有模型在肢体缺陷场景下的根本性局限，并推动更具包容性的姿态估计研究。"
claims:
- "现有模型（如ViTPose）在肢体缺陷图像上产生严重错误，例如假肢被预测为自然脚踝。"
- "我们提出25关键点方案，在COCO基础上增加8个残肢端点，以捕捉解剖变异。"
- "InclusiveVidPose数据集包含313个视频、327k帧、398名参与者，提供关键点、分割、跟踪ID等多维标注。"
- "新指标LiCC评估模型区分残肢与完整肢体的置信度一致性，现有方法得分仅约60%。"
---

# InclusiveVidPose: Bridging the Pose Estimation Gap for Individuals with Limb Deficiencies in Video-Based Motion

> [!tip] 核心洞察
> 通过视频级别标注、个性化关键点模式、残肢端点定义以及LiCC指标，揭示了现有模型在肢体缺陷场景下的根本性局限，并推动更具包容性的姿态估计研究。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | InclusiveVidPose: 弥合肢体缺陷人群在视频人体姿态估计中的差距 |
| 英文题名 | InclusiveVidPose: Bridging the Pose Estimation Gap for Individuals with Limb Deficiencies in Video-Based Motion |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=SyQqXAdWUq) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | InclusiveVidPose数据集与LiCC评估指标 |
| Dataset | InclusiveVidPose test (单帧), InclusiveVidPose video benchmark |

> [!tip] 效果简介
> - InclusiveVidPose test (单帧) 上，AP 为 ViTPose-H (InclusiveVidPose训练) 86.3，对比 ViTPose-H (仅COCO训练) 73.6，变化 +12.7。
> - InclusiveVidPose test (单帧) 上，AP 为 ViT-L (InclusiveVidPose训练) 85.5，对比 ViT-L (仅COCO训练) 73.8，变化 +11.7。
> - InclusiveVidPose test (单帧) 上，AP 为 RTMPose-M (InclusiveVidPose训练) 82.2，对比 RTMPose-M (仅COCO训练) 69.5，变化 +12.7。

## 概述

现有视频人体姿态估计（HPE）数据集和模型均假设人体关键点完整，无法处理肢体缺失或假肢等解剖变异。这一根本性瓶颈导致主流模型在肢体缺陷人群上产生严重且不可靠的预测——例如，**ViTPose**（Xu et al., 2022）会将假肢错误地预测为自然脚踝（Figure 2）。针对这一空白，本文提出**InclusiveVidPose**，首个面向肢体缺陷人群的大规模视频姿态估计数据集，包含313个视频、327k帧、398名参与者，并在COCO 17关键点基础上扩展8个残肢端点，形成25关键点模式以捕捉解剖变异（Figure 3）。同时引入新评估指标**LiCC（Limb-specific Confidence Consistency）**，量化模型对残肢与完整肢体的置信度区分能力。实验表明，现有方法在残肢关键点组上AP近乎为0（Table 3），而经InclusiveVidPose训练的ViTPose-H可将AP从73.6提升至86.3（Table 2），揭示了数据驱动方法在包容性姿态估计中的关键作用。

## 背景与动机

### 人体姿态估计的包容性缺口

人体姿态估计（HPE）在运动分析、康复评估和人机交互等领域取得了显著进展，但其核心假设——人体具备完整的标准骨骼结构——长期未被审视。现有HPE数据集（如COCO、MPII、PoseTrack）和主流模型均基于全身关键点完备的个体构建，这导致一个系统性的包容性缺口：**肢体缺陷人群（如上肢或下肢截肢者）的姿态无法被正确感知与评估**。

这一缺口的根本原因体现在三个层面：

1. **关键点定义的解剖不匹配**。标准骨架（如COCO的17关键点）假设所有关节位置均存在且可标注，但残肢的解剖端点并不对应任何预定义关键点。模型在面对残肢时，要么强行将最近的标准关键点（如手腕、脚踝）映射到错误位置，要么输出无意义的低置信度预测。

2. **标注数据的完全缺失**。截至本文工作，尚无任何公开数据集专门针对肢体缺陷人群提供关键点标注。这导致模型在该群体上的性能完全不可知，更无法通过微调来适配。

3. **评估指标的盲区**。传统AP指标仅衡量预测与真值之间的空间距离，无法反映模型是否真正“理解”了残肢与完整肢体的解剖差异——即模型是否对不存在的关节仍赋予高置信度。

### 现有模型的系统性失效

Figure 2 展示了这一问题的具体表现。以在COCO上训练的 **ViTPose**（Xu et al., 2022）为例，其在肢体缺陷图像上的预测呈现三类典型错误：

- **假肢误判为自然关节**：佩戴假肢的个体，其假肢末端被错误预测为自然脚踝，产生虚假的右脚踝检测。
- **残肢端点定位失败**：模型无法定位残肢末端，将手腕关键点错误地放置于躯干上。
- **解剖比例失真**：大腿长度显著不对称时，膝盖关键点被置于髋关节与踝关节之间的解剖学不合理中点。

这些失败并非个别模型的缺陷，而是**固定关键点模式与可变解剖结构之间的根本性冲突**。当模型被训练为在所有人体上寻找相同的17个关键点时，肢体缺失被系统性地误解为遮挡或检测失败，而非一种需要特殊处理的解剖变异。

### 本文动机与核心主张

基于上述分析，本文提出以下核心主张：

- **数据集驱动**：构建首个面向肢体缺陷人群的大规模视频姿态估计数据集 **InclusiveVidPose**，包含313个视频、327k帧、398名参与者，提供关键点、分割掩码、边界框、追踪ID和假肢状态等多维标注（Table 1）。
- **扩展关键点模式**：在COCO 17关键点基础上增加8个残肢端点（索引17-24），形成25关键点骨架，以捕捉个体化解剖变异（Figure 3）。
- **新评估指标**：引入 **肢体特定置信度一致性（LiCC）** 指标，量化模型区分残肢与完整肢体的置信度一致性，弥补传统AP指标的盲区。

通过这一系统性工作，本文旨在揭示现有HPE方法在肢体缺陷场景下的根本性局限，并为更具包容性的姿态估计研究奠定数据与评估基础。

## 核心创新

InclusiveVidPose 的核心创新并非提出新的模型架构，而是从**数据定义**和**评估范式**两个层面重构了面向肢体缺陷人群的姿态估计问题。

### 1. 解剖学驱动的扩展关键点模式

现有姿态估计数据集（如 COCO、MPII）均假设人体具有完整的 17 个标准关键点，这一固定模式从根本上无法捕捉肢体缺失或假肢佩戴者的解剖变异。InclusiveVidPose 在 COCO 17 点骨架基础上，增加了 **8 个残肢端点关键点**（索引 17–24），形成 25 关键点协议（Figure 3）。这些端点被定义为残肢的**稳定解剖学终点**，且明确排除假肢或辅助器具，为模型提供了语义清晰、可区分的定位目标。

该设计的关键机制在于：通过引入残肢端点，模型被迫学习区分“完整肢体关节”与“残肢终点”两种本质上不同的解剖结构。Figure 2 的证据表明，仅在 COCO 上训练的 ViTPose 会将假肢错误预测为自然脚踝，或将残肢端点错误放置于躯干——这正是固定关键点模式失效的直接表现。

### 2. 置信度一致性评估指标 LiCC

现有评估指标（AP、AR）仅衡量关键点定位精度，无法揭示模型对残肢与完整肢体的**置信度混淆**问题。为此，本文提出 **Limb-specific Confidence Consistency (LiCC)** 指标：

$$\mathrm{LiCC} := \frac{1}{|V|} \sum_{i \in V} \mathbf{1}\big(s_i > \max_{j \in M(i)} s_j\big)$$

其中 $V$ 为可见关键点集合，$M(i)$ 为根据解剖互斥规则 $\mathcal{R}$ 定义的与 $i$ 互斥的关键点集合。LiCC 衡量的是：当某个关键点实际可见时，其预测置信度是否高于所有互斥关键点的置信度。互斥规则基于解剖学约束定义，例如当左腕（关键点 9）存在时，对应的残肢端点（关键点 17、19）不应同时存在。

Table 2 的结果显示，即使模型在 AP 上表现尚可，LiCC 仍仅约 60%，表明现有方法在残肢/完整肢体的置信度区分上存在系统性缺陷。这一指标直接暴露了模型在安全关键型下游应用中的可靠性瓶颈。

### 3. 视频级个性化标注与多维标签体系

不同于传统数据集仅提供关键点坐标，InclusiveVidPose 为每帧提供五类标注（Figure 4）：像素级分割掩码、边界框、持久追踪 ID、肢体缺陷关键点、假肢状态。结合 SAM2 辅助分割和逐帧验证流程，确保了标注质量。更重要的是，数据集支持**个性化关键点掩码**——每位参与者仅标注其实际存在的关键点，避免了“强制预测不存在的关节”这一根本性问题。

这三项创新共同构成了一个闭环：扩展关键点模式定义了“标注什么”，LiCC 指标定义了“评估什么”，而视频级个性化标注体系提供了“如何构建基准”的完整方案。

## 整体框架

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SyQqXAdWUq/figures/003_Table_1.jpg]]
*Table 1: Comparison of existing datasets for human pose estimation. InclusiveVidPose offers unique and richer annotations than previous datasets. It is also the first pose estimation dataset to focus on individuals with limb deficiencies and to include keypoints at the ends of residual limbs*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SyQqXAdWUq/figures/004_Figure_3.jpg]]
*Figure 3: sFigure 3: Demonstration of Our Keypoint Schema. Our extended pose definition is built on the MS COCO keypoint schema by adding eight residual limb end keypoints (17 through 24). The left panel shows the full skeleton: original COCO keypoints are connected by solid lines, and the eight new residual limb end keypoints are marked as purple circles. The right panel presents, for each residual limb end keypoint, a cropped view of a subject with the corresponding amputation and a matching view of the same subject wearing a prosthetic device*

InclusiveVidPose 并非提出新的姿态估计算法，而是构建了一套面向肢体缺陷人群的**数据-标注-评估体系**，其整体框架由四个核心模块串联而成，形成从数据采集到模型诊断的闭环。

### 模块关系与数据流

整个 pipeline 的输入为包含肢体缺陷个体的 RGB 视频，输出为多维度标注数据以及模型性能的量化评估。四个模块的依赖关系如下：

```
视频采集与筛选 → 扩展关键点模式设计 → 多类型逐帧标注 → 基准测试与LiCC评估
```

**视频数据采集与筛选**：从公开来源收集 313 段视频，手动剔除严重遮挡、极端模糊等低质量片段，最终保留 327k 帧，覆盖 398 名参与者（Section 3.2）。这是整个框架的入口，决定了数据的多样性和标注可行性。

**扩展关键点模式设计**：在 COCO 17 关键点基础上增加 8 个残肢端点（编号 17–24），形成 25 点骨架（Figure 3）。残肢端点定义为残肢的解剖学末端，**明确排除假肢或辅助装置**。这一设计是框架的“语义锚点”——它使标注目标与肢体缺陷的解剖现实对齐，而非强行套用标准人体关键点。同时，该模式支持个性化关键点掩码，即对每个个体仅标注其实际存在的关键点。

**多类型逐帧标注**：由专业标注员与残障分类师协作，对每一帧中的每个个体标注五类信息（Figure 4）：
- 像素级分割掩码
- 边界框
- 持久追踪 ID
- 肢体缺陷关键点（含残肢端点）
- 假肢状态标签

其中，分割掩码借助 **Segment Anything 2 (SAM2)** 进行零样本提示式分割以加速初始掩码生成，后续由人工精修（Section 3.4）。这一模块将原始视频帧转化为结构化的训练/评估样本。

**基准测试与 LiCC 评估**：在数据集上按视频级别以 7:1:2 划分训练/验证/测试集，确保同一个体不出现在多个划分中（Section 4.1）。评估分为两条路径：
- **标准 AP/AR 评估**：在 25 关键点模式上计算 COCO 风格的 AP 和 AR，分别报告标准 17 关节、8 个残肢端点及全 25 点的性能。
- **LiCC 指标评估**：引入 **Limb-specific Confidence Consistency**，衡量模型对可见关键点预测置信度是否高于其互斥关键点集合的最大置信度（Section 4.2）。该指标直接诊断模型是否“知道”某个肢体是缺失的，而非在缺失部位产生高置信度的错误预测。

### 框架的关键设计逻辑

整个框架的核心因果机制在于：**通过重新定义关键点语义和评估标准，暴露并量化现有模型在肢体缺陷场景下的根本性失败模式**。现有模型（如 ViTPose）在 COCO 上训练后，会将假肢预测为自然脚踝，或将残肢端点错误地定位在躯干上（Figure 2）。InclusiveVidPose 的 25 点模式和 LiCC 指标正是针对这一瓶颈设计的“诊断工具”——前者提供正确的解剖目标，后者量化模型区分残肢与完整肢体的置信度一致性。

从表 1 的对比可见，InclusiveVidPose 是首个同时提供分割掩码、边界框、追踪 ID、残肢端点关键点和假肢信息的视频姿态估计数据集，其标注丰富度远超 COCO、MPII、PoseTrack 等现有数据集。这一框架填补了“肢体缺陷人群姿态估计”这一空白领域的数据和评估基础设施。

## 核心模块与公式推导

### 扩展关键点模式设计

当前 HPE 任务使用固定的关键点集合，无法捕捉肢体缺陷个体的解剖变异。InclusiveVidPose 在 MS COCO 的 17 关键点基础上，新增 8 个残肢端点（编号 17–24），形成 25 关键点骨架（Figure 3）。这 8 个端点位于残肢的解剖末端，**明确排除假肢或辅助装置**，为模型提供语义清晰、可区分完整肢体与残肢结构的定位目标。同时，该模式支持个性化关键点掩码——对于不适用于特定个体的关键点，在训练和评估中予以屏蔽，避免模型被迫预测不存在的解剖位置。

### 多类型标注流程

每帧对每位肢体缺陷个体提供五类标注（Figure 4）：
- **像素级分割掩码**：利用 SAM2（Segment Anything 2）进行零样本提示式分割生成初始掩码，经人工修正后得到精确边界。
- **边界框**：包围个体的矩形区域。
- **持久追踪 ID**：跨帧关联同一人物。
- **肢体缺陷关键点**：基于上述 25 关键点模式的坐标标注。
- **假肢状态标签**：指示当前帧是否佩戴假肢。

标注由专业标注员与残障分类师协作完成，确保解剖学准确性和一致性。

### LiCC 指标：肢体特异性置信度一致性

现有姿态估计模型对残肢与完整肢体的预测置信度缺乏校准——模型可能在缺失关节位置输出高置信度的错误预测。为量化这一问题，本文提出 **Limb-specific Confidence Consistency（LiCC）** 指标。

#### 互斥规则集

首先根据解剖关系定义关键点互斥约束集合 $\mathcal{R}$。例如，当左腕（keypoint 7）可见时，其互斥集合包含左残肢上臂端点（keypoint 17），即 $(7, \{17\}) \in \mathcal{R}$；类似地，左残肢下臂端点（keypoint 19）与左腕互斥。完整规则集见附录 G，核心逻辑为：**若某关键点可见，则其互斥集合内的所有关键点不应同时存在**。

#### 指标定义

给定可见关键点集合 $V$，对于每个 $i \in V$，记 $M(i)$ 为 $i$ 的互斥关键点集合。LiCC 定义为：

$$\mathrm{LiCC} := \frac{1}{|V|} \sum_{i \in V} \mathbf{1}\big(s_i > \max_{j \in M(i)} s_j\big)$$

其中 $s_i$ 为模型对关键点 $i$ 的预测置信度，$\mathbf{1}(\cdot)$ 为指示函数。

**含义**：LiCC 衡量可见关键点的预测置信度超过其所有互斥关键点最大置信度的比例。理想情况下，模型应对真实存在的关键点赋予高置信度，而对互斥（不应存在）的关键点赋予低置信度，此时 LiCC 接近 100%。现有方法在 InclusiveVidPose 上的 LiCC 仅约 60%（Table 2），表明模型在残肢/完整肢体区分上的置信度校准严重不足。

#### 与标准指标的关系

LiCC 与 AP/AR 互补：AP 衡量空间定位精度，LiCC 衡量置信度排序的解剖一致性。一个模型可能获得较高 AP（因为正确预测了可见关键点位置），但 LiCC 较低（因为对互斥关键点也输出了高置信度），这在安全敏感的下游应用中构成风险。

## 实验与分析

### 主要结果：单帧姿态估计基准

Table 2 系统评估了六类模型在 InclusiveVidPose 上的表现。核心发现是：仅使用 COCO 训练的模型直接迁移到肢体缺陷场景时性能大幅下降，而在 InclusiveVidPose 上训练后显著恢复。以 ViTPose-H 为例，COCO→InclusiveVidPose 的 AP 仅 73.6，使用 InclusiveVidPose 训练后提升至 86.3（+12.7）。这一现象在不同架构中普遍存在：ViT-L 从 73.8 升至 85.5，RTMPose-M 从 69.5 升至 82.2。这表明现有模型并非架构能力不足，而是训练数据中缺乏肢体缺陷的表征。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SyQqXAdWUq/figures/008_Table_2.jpg]]
*Table 2: Main experimental results on pose estimation algorithms. We evaluate models including Swin-based top-down heatmap networks (Liu et al., 2021a), ViTPose (Xu et al., 2022), and RTMPose (He et al., 2024), as well as the bottom-up model DEKR (Geng et al., 2021), the detectorbased single-stage model YOLOX-Pose (Maji et al., 2022), and the video-based ViPNAS (Xu et al., 2021). “InclusiveVidPose → InclusiveVidPose” reports training on our training set and evaluation on our validation and test splits. “COCO → InclusiveVidPose” reports training only on COCO and evaluation on our InclusiveVidPose validation and test splits. “InclusiveVidPose + COCO → InclusiveVidPose/COCO” reports training on both da...*

值得注意的是，即使模型在 InclusiveVidPose 上训练并取得较高 AP，新引入的 LiCC 指标仍揭示出深层问题。LiCC 衡量可见关键点的预测置信度是否高于其互斥关键点集合的最大置信度——例如，当左腕存在时，其置信度应高于左肘残肢端点等互斥点。Table 2 显示多数方法的 LiCC 仅约 60%，说明模型在区分残肢与完整肢体时置信度并不一致。这一指标独立于传统 OKS-based AP，捕捉了标准评估无法反映的安全性隐患：即使关键点位置接近真值，模型对残肢/完整肢体的“身份判断”仍可能混乱。

### 视频姿态估计基准

Table 3 报告了 DCPose 和 DSTA 在 InclusiveVidPose 视频基准上的 PoseTrack 风格 AP。两种方法在标准关节上表现尚可（头部、肩部等 AP 在 28%–81%），但在残肢关键点组上几乎完全失效：DCPose 在 ArmLow 组 AP 仅 0.2，DSTA 为 0.0；LegLow 组 DCPose 为 0.3，DSTA 为 0.0。整体均值 AP 仅从 DCPose 的 43.2 微升至 DSTA 的 43.7，说明当前视频模型的时序聚合能力在残肢端点定位上几乎没有增益。Figure 8 的失败案例进一步印证了这一点：DSTA 倾向于将残肢端点和邻近关节放置在与真值明显不符的解剖位置。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SyQqXAdWUq/figures/009_Table_3.jpg]]
*Table 3: PoseTrack-style keypoint AP on InclusiveVidPose. We report AP (%) of DCPose (Liu et al., 2021b) and DSTA (He & Yang, 2024) on standard joints and residual-limb groups (ArmUp, ArmLow, LegUp, LegLow), together with the mean over all keypoints*

### 训练策略消融

Table 4 分析了 ViTPose-H 在不同训练策略下对残肢端点（8 个）和标准关节（17 个）的影响。关键结论是：COCO 预训练或联合训练主要提升的是标准 17 关键点的性能，对 8 个残肢端点的增益有限。从零开始训练在残肢端点上 AP 为 82.4，COCO 初始化后微调升至 84.2（+1.8），而联合训练反而降至 82.2。相比之下，标准 17 关键点在 COCO 初始化后从 87.6 升至 90.4。这表明残肢端点的定位难度本质上高于标准关节，且 COCO 数据中的全身关键点知识难以直接迁移到残肢解剖结构上。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SyQqXAdWUq/figures/011_Table_4.jpg]]
*Table 4: ViTPose-H results on InclusiveVidPose for 8 residual endpoints and 17 standard joints. We report performance on three keypoint sets: the 8 residual endpoints, the standard 17 COCO joints, and the extended 25-keypoint schema. The left block (InclusiveVidPose* → InclusiveVidPose) trains ViTPose-H from scratch on InclusiveVidPose without COCO pretraining. The middle block (InclusiveVidPose → InclusiveVidPose) initializes from COCO weights and fine-tunes only on InclusiveVidPose. The right block (InclusiveVidPose+COCO → InclusiveVidPose) jointly trains on COCO and InclusiveVidPose before evaluation on InclusiveVidPose. AP on the 17 standard keypoints is consistently higher than AP on the 8 resi...*

### 按肢体缺失类型分组分析

Table 5 按缺失部位将测试片段分组，评估 ViTPose-H 在共享的 17 个 COCO 关键点上的表现。各组的 AP 范围在 82–92 之间，其中左腿缺失组最高（AP 92.3），完整肢体组反而最低（AP 75.7）。这一反直觉的结果可能源于完整肢体片段中动作复杂度更高或遮挡更严重。整体而言，各缺失组之间的性能差异不大，说明共享关节的标注在跨缺失类型间保持了一致性，模型并未因特定缺失类型而产生系统性偏差。

### 失败模式与局限性

Figure 7 展示了 ViTPose（ViT-B）在 InclusiveVidPose 训练后的预测案例。即使模型已适配残肢关键点模式，仍然存在以下典型错误：残肢端点被放置在假肢末端而非解剖残端、邻近关节在肢体明显缩短的情况下被拉伸到不合理位置、以及假肢状态（佩戴/未佩戴）影响关键点定位精度。这些错误与 Figure 2 中 COCO 训练模型的失败模式存在本质区别——后者是将假肢误判为自然关节，而前者是在目标定义正确的前提下仍无法精确定位残肢端点。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_SyQqXAdWUq/figures/002_Figure_2.jpg]]
*Figure 2: Examples of keypoint predictions by the ViTPose base model trained the COCO dataset. Left: prostheses are erroneously predicted as natural ankles, leading to false right-ankle detections. Middle: the model fails to localize the residual limb end and places the left-wrist keypoint on the torso. Right: pronounced asymmetry in thigh length results in the right-knee keypoint being placed at an anatomically implausible midpoint between hip and ankle. These cases show limited generalization to limb differences*

当前数据集的一个固有局限是遮挡与缺失的区分难题。尽管采用多标注员和视频级验证，部分严重遮挡的肢体仍可能被误标为缺失，或反之。这种标签噪声对 LiCC 等依赖互斥规则的指标影响尤为直接。此外，数据仅覆盖 2D RGB 视频，缺乏深度或惯性传感器等多模态信息，限制了在三维空间精确定位残肢端点的可能性。

## 方法谱系与知识库定位

### 1. 基线模型谱系

InclusiveVidPose 作为数据集与评估基准，其方法贡献并非提出新的模型架构，而是通过构建专用数据集和评估指标，系统性地暴露现有姿态估计模型在肢体缺陷人群上的根本性局限。论文评估的基线模型覆盖了当前人体姿态估计的主流范式：

**自顶向下（Top-Down）范式**：该类方法先检测人体边界框，再对框内单人进行关键点回归，是当前精度最高的路线。论文评估的基线包括：
- **ViTPose** (Xu et al., 2022)：基于 Vision Transformer 的姿态估计模型，是当前 COCO 基准上的 SOTA 方法之一。
- **RTMPose** (He et al., 2024)：轻量级实时姿态估计模型，在效率与精度之间取得平衡。
- **Swin-based heatmap networks** (Liu et al., 2021a)：基于 Swin Transformer 的热图回归网络。

**自底向上（Bottom-Up）范式**：该类方法先检测所有关键点，再通过分组算法将其分配到不同人体实例。论文评估了 **DEKR** (Geng et al., 2021)，该模型通过解耦关键点回归来提升密集场景下的性能。

**单阶段（Single-Stage）范式**：该类方法在单次前向传播中同时完成检测和姿态估计。论文评估了 **YOLOX-Pose** (Maji et al., 2022)，该方法将姿态估计集成到 YOLOX 检测框架中。

**视频姿态估计范式**：该类方法利用时序信息提升单帧姿态估计的稳定性和精度。论文评估了两个代表性方法：
- **DCPose** (Liu et al., 2021b)：通过多帧特征融合进行视频姿态估计。
- **DSTA** (He & Yang, 2024)：采用时空聚合机制的视频姿态估计模型。

此外，论文还评估了基于神经架构搜索的视频模型 **ViPNAS + Swin** (Xu et al., 2021)。

### 2. 核心瓶颈与因果机制

现有 HPE 模型在 InclusiveVidPose 上暴露的核心瓶颈并非简单的精度下降，而是**结构性失效**：

**瓶颈一：固定关键点模式的解剖学不匹配**。COCO 的 17 关键点模式假设所有人体拥有完整的四肢，当面对截肢个体时，模型会强行在不存在解剖结构的位置预测关键点。Figure 2 展示了 ViTPose 的典型失败模式：假肢被错误预测为自然脚踝；残肢端点被错误定位到躯干上；大腿长度不对称导致膝关节被放置在不合理的解剖位置。这些错误的根源在于模型缺乏“肢体可能缺失”的先验知识。

**瓶颈二：视频时序信息的失效传递**。Table 3 显示，即使利用多帧信息的视频模型 DCPose 和 DSTA，在残肢关键点组上的 AP 近乎为零（如 ArmLow 组 DCPose 仅 0.2%，DSTA 为 0.0%），远低于标准关节（Head、Shoulder 等可达 60-80%）。这表明时序聚合无法弥补关键点定义层面的结构性缺陷——当目标关键点在解剖上不存在时，多帧信息反而可能放大错误的一致性。

**瓶颈三：置信度校准的系统性偏差**。论文提出的 LiCC 指标（Limb-specific Confidence Consistency）量化了这一现象：现有方法在 InclusiveVidPose 上的 LiCC 仅约 60%。这意味着模型在预测不存在的关键点时，其输出置信度与可见关键点相当甚至更高，导致下游应用无法通过置信度阈值可靠地过滤错误预测。

### 3. 方法适用边界

**InclusiveVidPose 数据集的核心适用场景**：
- 面向肢体缺陷人群的 2D 视频姿态估计研究与评估。
- 作为现有 HPE 模型在包容性维度上的压力测试基准。
- 为开发残肢感知的姿态估计模型提供训练数据。

**明确的方法边界**：
- **模态限制**：数据集仅包含 2D RGB 视频，不覆盖 3D 姿态、深度图或惯性传感器（IMU）等多模态数据。因此，基于该数据集训练的模型无法直接推广到 3D 姿态估计或传感器融合场景。
- **遮挡与缺失的歧义性**：论文明确指出，即使通过多标注员和视频验证流程，遮挡的肢体与缺失的肢体仍有时难以区分，可能给标签带来少量噪声。这一歧义性在严重遮挡场景下会进一步放大。
- **COCO 预训练的有限迁移**：Table 4 的消融实验揭示了一个关键发现——COCO 预训练或联合训练主要提升标准 17 关键点的性能，对 8 个残肢端点 AP 提升有限（从 82.4 到 84.2，联合训练后反而降至 82.2）。这表明残肢端点的定位能力难以从完整肢体的预训练中迁移获得，需要专门的训练数据和可能的新模型设计。

### 4. 局限与开放问题

**已识别的局限**：
1. **标注歧义性**：遮挡与缺失肢体的区分困难，可能引入标签噪声，影响模型在边界情况下的可靠性。
2. **置信度校准不足**：当前姿态模型对缺失或假肢关节的预测置信度不可靠，影响安全敏感型下游应用（如康复评估、假肢控制）的可用性。
3. **模态单一**：仅覆盖 2D RGB 视频，未利用深度或惯性传感器等多模态信息。

**开放问题**：
1. **自动区分遮挡与缺失**：如何设计算法或标注流程，更可靠地自动区分遮挡与缺失的肢体，以提升标注质量和模型鲁棒性？
2. **置信度校准**：如何改进姿态估计模型，使其在遇到缺失或假肢关节时输出校准良好的置信度，使 LiCC 接近 100%？
3. **合成数据补充**：如何有效利用合成数据补充罕见肢体缺失案例（如多肢缺失组合），同时保护参与者隐私？
4. **多模态融合**：多模态数据（深度、IMU 等）能否显著提升残肢端点的定位精度，特别是在严重遮挡或快速运动场景下？
5. **模型架构创新**：Table 4 表明 COCO 预训练对残肢端点几乎无帮助，这是否意味着需要全新的模型架构——例如引入“肢体存在性”的显式先验或基于解剖约束的推理机制——而非仅仅依赖数据驱动？

### 5. 知识库定位

InclusiveVidPose 在 HPE 领域的定位是**包容性基准**，其贡献与影响体现在以下维度：

- **与现有数据集的差异**：Table 1 系统对比了 InclusiveVidPose 与 COCO、MPII、PoseTrack、OCHuman、CrowdPose、Halpe、HumanArt 等数据集。InclusiveVidPose 是首个聚焦肢体缺陷人群的姿态估计数据集，且唯一同时提供分割掩码、边界框、追踪 ID、残肢端点关键点和假肢状态信息的多维标注。

- **对模型研发的推动**：该工作揭示了一个被忽视的研究方向——姿态估计模型的**解剖学包容性**。现有的模型设计和评估体系隐式假设“完整人体”，InclusiveVidPose 打破了这一假设，要求未来的模型能够感知并适应人体的解剖变异。

- **评估体系的补充**：LiCC 指标为姿态估计的置信度评估提供了新维度，不仅衡量关键点定位精度，还衡量模型对“肢体是否存在”的结构性认知能力。这一指标可推广到其他涉及人体变异性的视觉任务。

- **社会影响维度**：该数据集通过接近平衡的性别分布（女性 51%，男性 49%）和假肢使用比例（52% 佩戴假肢，48% 未佩戴），以及覆盖多种肢体缺失类型和部位，确保了模型的通用性和公平性，避免了对特定子群体的系统性偏见。

## 原文 PDF

![[paperPDFs/ICLR_2026/InclusiveVidPose_Bridging_the_Pose_Estimation_Gap_for_Individuals_with_Limb_Deficiencies_in_Video_Based_Motion.pdf]]
