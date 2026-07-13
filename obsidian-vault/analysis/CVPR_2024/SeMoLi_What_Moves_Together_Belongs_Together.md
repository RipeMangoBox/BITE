---
title: "SeMoLi: What Moves Together Belongs Together"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/SeMoLi_What_Moves_Together_Belongs_Together.pdf
code_link: null
project_link: https://research.nvidia.com/labs/dvl/projects/semoli/
aliases:
- SeMoLi
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "使用消息传递网络（MPN）根据空间邻近（proximity）和运动共命运（common fate）原则，以数据驱动的方式学习点之间的边缘分数，将点聚类问题转化为可学习的图分解。"
primary_logic: "将运动信息作为一阶线索，结合空间邻近性，通过消息传递网络实现端到端的类不可知点云实例分割，使得伪标签质量可随训练数据增加而提升，并可跨数据集泛化。"
claims:
- "SeMoLi在Waymo Open数据集上的伪标签质量（3DIoU F1@0.4）达到50.4，显著优于DBSCAN++†的16.2。"
- "使用SeMoLi生成的伪标签训练的目标检测器在移动对象上达到57.5 AP（IoU=0.4），比先前启发式方法提升14个点。"
- "SeMoLi伪标签的噪声远少于DBSCAN，未匹配假阳性率仅为14.5%，而DBSCAN++†为72.0%。"
- "SeMoLi仅在Waymo上训练即可在Argoverse2上泛化，移动对象3DIoU召回率达到45.8，优于DBSCAN++†的33.3。"
---

# SeMoLi: What Moves Together Belongs Together

> [!tip] 核心洞察
> 将运动信息作为一阶线索，结合空间邻近性，通过消息传递网络实现端到端的类不可知点云实例分割，使得伪标签质量可随训练数据增加而提升，并可跨数据集泛化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SeMoLi：一起运动的属于一起 |
| 英文题名 | SeMoLi: What Moves Together Belongs Together |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2402.19463) · [Project](https://research.nvidia.com/labs/dvl/projects/semoli/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SeMoLi |
| Dataset | Waymo Open Dataset (伪标签质量), Waymo Open Dataset (移动物体检测), Argoverse2 (移动物体检测, 跨数据集) |

> [!tip] 效果简介
> - Waymo Open Dataset (伪标签质量) 上，3DIoU F1@0.4 为 50.4，对比 16.2 (DBSCAN++†)，变化 +34.2。
> - Waymo Open Dataset (移动物体检测) 上，AP@0.4 为 57.5，对比 ~43.5 (prior heuristic approach)，变化 +14.0。
> - Argoverse2 (移动物体检测, 跨数据集) 上，AP@0.4 为 57.6，对比 82.9 (fully supervised on Argoverse2)，变化 -25.3。

## 概要

激光雷达点云中运动实例的分割与检测，是自动驾驶感知系统的基础能力。现有方法主要依赖基于密度的启发式聚类（如DBSCAN），结合场景流或多帧信息进行后处理。这类管线存在根本性瓶颈：**聚类决策完全由手工设计的空间规则驱动，无法从数据中学习判别性运动模式**，导致稀疏点云下过分割与欠分割严重，且对背景噪声的滤除能力薄弱。

SeMoLi 针对上述瓶颈，将点云实例分割重新建模为**可学习的图分解问题**。其核心操纵变量是：利用消息传递网络（MPN），根据空间邻近（proximity）与运动共命运（common fate）两个格式塔原则，以数据驱动的方式学习点之间的边缘分数，替代传统密度聚类中的硬阈值连接规则。这一转换使得伪标签质量可随训练数据规模增加而单调提升，并可跨数据集泛化。

**核心结论**：
- 在 Waymo Open Dataset 上，SeMoLi 生成的伪标签质量（3DIoU F1@0.4）达到 **50.4**，而最优启发式基线 DBSCAN++† 仅为 **16.2**（Table 3）。
- 使用 SeMoLi 伪标签训练的 PointPillars 检测器，在移动对象上达到 **57.5 AP**（IoU=0.4），比先前启发式方法提升 **14 个点**（Table 6）。
- SeMoLi 伪标签的未匹配假阳性率仅为 **14.5%**，远低于 DBSCAN++† 的 **72.0%**（Table 4），表明噪声显著减少。
- 仅在 Waymo 上训练的 SeMoLi，可直接在 Argoverse2 上泛化，移动对象 3DIoU 召回率达到 **45.8**，优于 DBSCAN++† 的 **33.3**（Table 5）。

**方法定位**：SeMoLi 属于自监督/半监督点云实例分割与检测范式，其知识贡献在于将相关聚类（correlation clustering）与消息传递网络结合，构建了一个**类不可知、纯数据驱动的运动实例分割教师网络**。该方法不依赖任何类别标签，仅利用场景流估计获得的点轨迹作为运动线索，因此天然具备跨数据集迁移能力。

自动驾驶系统需要对周围环境中的物体进行精确的3D检测与跟踪，以保障安全导航。激光雷达（Lidar）作为核心传感器，能够提供稀疏但准确的3D点云数据。然而，构建高性能的3D目标检测器通常依赖大规模、高质量的人工标注数据，这一过程成本高昂且难以覆盖所有场景与类别。

### 现有方法的瓶颈

在缺乏人工标注的情况下，研究者通常采用启发式聚类方法（如DBSCAN）从点云中提取运动物体实例，以生成伪标签用于检测器训练。这类方法遵循“运动共命运”（common fate）和“空间邻近”（proximity）的格式塔原则，通过场景流估计剔除静态点，再基于密度聚类将剩余点分组为物体实例。然而，这些方法存在根本性缺陷：

- **无法利用数据驱动力**：启发式方法依赖固定的密度阈值和距离参数，无法从数据中学习最优的分组策略。随着训练数据增加，其伪标签质量不会提升，这与现代数据驱动范式相悖。
- **过分割与欠分割严重**：在稀疏点云区域（如远距离物体），密度聚类容易将同一物体分裂为多个片段（过分割），或将多个邻近物体合并为一个（欠分割）。
- **背景噪声滤除不足**：场景流估计的误差会导致静态点被误判为运动点，启发式方法缺乏有效机制区分真正的运动物体与噪声点。

### SeMoLi的动机与核心思路

SeMoLi（Segment Moving in Lidar）的提出正是为了突破上述瓶颈。其核心动机是将点云实例分割从启发式规则驱动转变为**数据驱动**的学习范式，使得伪标签质量能够随训练数据规模增加而单调提升。

SeMoLi的核心思路是：将点云聚类问题重新表述为**图分解问题**。具体而言，在由点构建的图上，使用**消息传递网络（Message Passing Network, MPN）**学习每条边连接同一物体实例的概率（边缘分数），再通过相关聚类（correlation clustering）将点分组为实例。这一过程遵循两个基本原则：

- **空间邻近**：空间上靠近的点更可能属于同一物体。
- **运动共命运**：具有相似运动模式（速度大小、方向）的点更可能来自同一运动物体。

通过将格式塔原则编码为可学习的图神经网络，SeMoLi能够端到端地学习类不可知（class-agnostic）的点云实例分割，无需依赖类别标签或预设的聚类参数。

## 核心方法与创新机理

SeMoLi 的核心创新在于将基于启发式规则的点云运动实例分割，转化为一个**数据驱动的可学习图分解问题**。其关键 changed slots 体现在以下几个层面：

### 从密度聚类到消息传递网络学习的范式转变

传统方法（如 DBSCAN、DBSCAN++）依赖基于密度的空间聚类，辅以场景流过滤和多阶段启发式后处理。这类方法的核心瓶颈在于：**无法利用数据驱动力来提升分割性能**，导致稀疏点云下过分割和欠分割严重，且无法有效滤除背景噪声。

SeMoLi 将问题重新定义为：给定一组 Lidar 点轨迹，利用**空间邻近（proximity）和运动共命运（common fate）**两个格式塔原则，通过消息传递网络（MPN）学习点之间的边缘分数，进而通过相关聚类获得实例分割。这一转变使得伪标签质量可随训练数据增加而单调提升（F1 从 50.4 提升至 57.6），展现了数据驱动力。

### 节点与边缘特征编码的重新设计

SeMoLi 在特征层面引入了两个关键变化：

- **节点特征**：从仅使用空间位置扩展为结合速度统计量。初始节点嵌入为：
  $$h_i^{(0)} = (x_i, y_i, z_i, \mathrm{mean}(v_{\tau_i}), \mathrm{min}(v_{\tau_i}), \mathrm{max}(v_{\tau_i}))$$
  其中速度统计量来自自监督轨迹预测网络获得的 24 帧长程运动模式。消融实验（Table 1）表明，位置+速度节点特征将学习性能从纯位置的 51.4 F1 提升至 70.9 F1。

- **边缘特征**：初始化为点对之间的相对空间位移：
  $$h_{ij}^{(0)} = (x_i - x_j, y_i - y_j, z_i - z_j)$$
  消融显示仅使用位置差作为边缘特征优于包含速度特征，表明速度作为边缘特征可能引入噪声。

### 图构建策略的优化

SeMoLi 采用基于空间位置的 k 近邻（kNN）图构建，而非基于速度相似性。Table 1 显示，位置 kNN 在 Oracle 性能上达到 90.9 F1，远高于速度 kNN 的 51.4 F1。这一发现表明，空间邻近性为消息传递提供了更稳定的图拓扑结构，而运动信息更适合作为节点特征而非图的连接准则。

### 简化的后处理管线

与 DBSCAN++ 的多帧跟踪与 ICP 配准不同，SeMoLi 采用**简单的包围盒膨胀至最小尺寸**策略。Table 2 显示，包围盒膨胀将 3DIoU F1 从 30.3 大幅提升至 53.1，而分割 IoU 变化不大。Table 11 进一步表明，基于 ICP 的配准方法因点云噪声反而导致性能下降，验证了简化后处理的合理性。

### 端到端的伪标签生成与检测器训练闭环

SeMoLi 将分割网络作为"教师"，在无标注数据上生成伪标签，用于训练 PointPillars "学生"检测器。这一闭环设计使得检测器在移动对象上达到 57.5 AP（IoU=0.4），比先前启发式方法提升 14 个点（Abstract, Table 6）。更关键的是，SeMoLi 仅在 Waymo 上训练即可泛化至 Argoverse2，移动对象 3DIoU 召回率达到 45.8，优于 DBSCAN++† 的 33.3（Table 5），证明了学习到的运动分组能力具有跨数据集的迁移性。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2402_19463/figures/018_Figure_6.jpg]]
*Figure 6: Overview MPN during training and evaluation: We visualize our MPN. It takes as input points from a point cloud with their corresponding spatial positions $p _ { i }$ , trajectory $t _ { i }$ , and velocities along the trajectory $v _ { i }$ . . We then extract initial node and edge features ${ \bf \bar { \Phi } } _ { h _ { i } ^ { ( 0 ) } }$ and $h _ { i j } ^ { ( 0 ) }$ , apply L MPN layers and for training apply focal loss on the final edge features $h _ { i j } ^ { ( L ) }$ . During Evaluation, we prune edges based on the final edge scores, apply correlation clustering on the remaining, and extract bounding boxes $b _ { c }$ with translation $t _ { c }$ , dimensions l w $h _ { c }$ , and heading in xy-dir...

SeMoLi 的整体 pipeline 围绕“以运动为线索、数据驱动地学习点云实例分割”这一核心思想展开，其输入-处理-输出流可概括为四个阶段：

1. **点云预处理与轨迹预测**：首先从原始激光雷达点云中滤除静态点，仅保留具有显著运动（速度 > 1 m/s）的点。随后，利用自监督场景流估计网络为每个保留点预测一条 24 帧的长程轨迹，从而获得该点沿时间维度的完整运动模式（Section 3.1.1, Figure 2）。

2. **基于消息传递网络的运动聚类（SeMoLi 核心）**：将预处理后的点云建模为加权图 $G = (V, E)$，其中节点 $i$ 对应单个点，边 $(i, j)$ 通过空间 k 近邻（kNN）连接。节点特征编码空间位置与沿轨迹的速度统计量（均值、最小值、最大值），边特征编码点对间的相对空间位移。随后，通过 $L$ 层消息传递网络（MPN）迭代更新节点与边的嵌入表示，最终利用二元 sigmoid 分类器为每条边预测一个“属于同一实例”的分数。基于这些边缘分数，应用相关聚类（correlation clustering）将点划分为不同的运动实例（Section 3.1.2, Equation 1–5）。

3. **包围盒生成与膨胀**：对每个点簇计算紧致的 3D 包围盒，然后将其膨胀至预设的最小长宽高尺寸，以逼近无障碍真值框（amodal box），弥补因点云稀疏导致的包围盒过紧问题（Section 3.2, Table 2）。

4. **检测器训练**：将 SeMoLi 在无标注激光雷达数据上生成的伪标签作为监督信号，训练一个类别无关的 PointPillars 目标检测器（学生网络），用于最终的运动物体检测（Section 3.2）。

整个框架的关键因果机制在于：**将启发式的密度聚类替换为可学习的图分解**，使伪标签质量能够随训练数据量的增加而单调提升（F1 从 50.4 升至 57.6），并具备跨数据集泛化能力（仅在 Waymo 上训练即可在 Argoverse2 上达到 45.8 的移动对象召回率）。

### 3.1 图构建与节点/边特征初始化

SeMoLi将点云表示为加权图 $G = (V, E)$，其中节点 $V$ 对应点云中的每个点，边 $E$ 基于k近邻（kNN）构建。图构建采用**空间位置**作为相似性度量——消融实验表明，基于位置的kNN图在Oracle性能上达到F1 90.9，远优于基于速度的kNN图（F1 51.4）（Table 1）。

**节点特征初始化**（Equation 1）：每个节点 $i$ 的初始嵌入编码了空间位置和沿预测轨迹的速度统计量：

$$h_i^{(0)} = (x_i, y_i, z_i, \mathrm{mean}(v_{\tau_i}), \mathrm{min}(v_{\tau_i}), \mathrm{max}(v_{\tau_i}))$$

其中 $(x_i, y_i, z_i)$ 为点的空间坐标，$v_{\tau_i}$ 表示点 $i$ 沿其预测轨迹 $\tau_i$ 的速度序列，$\mathrm{mean}$、$\mathrm{min}$、$\mathrm{max}$ 分别为速度的均值、最小值和最大值。消融实验证实，将速度与位置结合作为节点特征显著提升了学习效果（F1从纯位置特征的某基线提升至70.9）（Table 1）。

**边特征初始化**（Equation 2）：边 $(i,j)$ 的初始特征仅编码点对之间的相对空间位移：

$$h_{ij}^{(0)} = (x_i - x_j, y_i - y_j, z_i - z_j)$$

消融实验表明，仅使用位置差作为边特征优于包含速度特征，说明速度作为边特征可能引入噪声（Table 1 edge features）。

### 3.2 消息传递网络

SeMoLi采用 $L$ 层消息传递网络（MPN）迭代更新节点和边嵌入，核心操作包括边更新、消息生成和节点更新三步。

**边更新**（Equation 3）：第 $l$ 层的边嵌入通过融合前一层边嵌入及相邻节点嵌入进行更新：

$$h_{ij}^{(l)} = f(h_{ij}^{(l-1)}, h_i^{(l-1)}, h_j^{(l-1)})$$

其中 $f$ 为可学习的更新函数，$h_i^{(l-1)}$ 和 $h_j^{(l-1)}$ 分别为边两端节点在前一层的嵌入。

**节点更新**（Equation 4）：节点嵌入通过聚合来自所有邻居的消息进行更新。首先计算每条边传递的消息，然后对所有邻居消息进行聚合：

$$m_{i,j}^{(l)} = g(h_{ij}^{(l)}, h_j^{l-1}, h_i^{(l-1)})$$

$$h_i^{(l)} = \phi(\{m_{i,j}^{(l)}\}_{j \in N_i})$$

其中 $g$ 为消息生成函数，$N_i$ 为节点 $i$ 的邻居集合，$\phi$ 为排列不变的聚合函数。

**边分类**（Equation 5）：经过 $L$ 层消息传递后，最终边嵌入通过线性层和sigmoid函数获得边缘分数：

$$\tilde{h}_{ij}^{(L)} = \sigma(f_f(h_{ij}^{(L)}))$$

其中 $f_f$ 为线性变换，$\sigma$ 为sigmoid激活函数。该分数表示边 $(i,j)$ 连接的两个点属于同一实例的概率。

### 3.3 相关聚类与后处理

训练完成后，SeMoLi通过裁剪负边缘（分数低于阈值的边）并应用相关聚类算法，将点云分割为实例簇。这一过程将点聚类问题转化为可学习的图分解问题，核心机制是利用MPN学习到的边缘分数来判断点对是否属于同一运动实例。

### 3.4 包围盒生成与膨胀

从点簇中提取紧致3D包围盒后，SeMoLi采用简单的**包围盒膨胀**策略：将包围盒膨胀至预设的最小宽度、长度和高度。消融实验表明，这一简单策略大幅提升检测性能——3DIoU F1从30.3升至53.1，而分割IoU变化不显著（Table 2）。相比之下，基于ICP的配准方法因点云和轨迹噪声导致性能下降（Table 11），进一步验证了简单膨胀策略在该场景下的有效性。

## 实验与关键发现

### 核心瓶颈与验证逻辑

SeMoLi的实验设计围绕一个核心瓶颈展开：**现有启发式聚类方法无法利用数据驱动力来提升分割性能**。为验证数据驱动方法的优势，实验从四个递进层次构建证据链：

1. **伪标签质量**：SeMoLi生成的伪标签在3DIoU F1@0.4上达到50.4，而DBSCAN++†仅16.2（Table 3），提升+34.2点。这一差距的根本原因在于DBSCAN仅依赖空间密度，而SeMoLi通过消息传递网络学习运动共命运原则，有效区分具有相似运动模式的相邻物体。
2. **噪声控制**：SeMoLi的未匹配假阳性率仅为14.5%，而DBSCAN++†高达72.0%（Table 4）。这表明数据驱动方法能有效滤除背景噪声，避免启发式方法在稀疏点云下的过分割问题。
3. **检测器性能**：使用SeMoLi伪标签训练的PointPillars检测器在移动对象上达到57.5 AP（IoU=0.4），比先前启发式方法提升约14个点（Abstract, Table 6）。这验证了高质量伪标签对下游任务的实际价值。
4. **跨数据集泛化**：仅在Waymo上训练的SeMoLi在Argoverse2上移动对象3DIoU召回率达到45.8，优于DBSCAN++†的33.3（Table 5）。这证明学习到的运动分组模式具有跨场景的泛化能力，而非过拟合特定数据分布。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2402_19463/figures/006_Table_2.jpg]]
*Table 2: Bounding box inflation: We inflate tight bounding boxes that enclose point clusters to a minimum width, length, and height. The segmentation performance changes only insignificantly while the detection performance improves drastically. SeMoLi 10 clusters points together correctly, but generates bounding boxes that are significantly tighter around the objects. Table 3. Pseudo-label quality comparison (3DIoU): We compare our SeMoLi to different variants of DBSCAN [30], augmented with scene flow (DBSCAN++), long-term trajectory information (DBSCAN++l) and outlier filtering (†). In gray (top) we report results using ground truth scene flow and trajectories, and below we report scene flow and mo...*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2402_19463/figures/007_Table_4.jpg]]
*Table 4: Class-wise evaluation of pseudo-labels: For class-wise evaluation, we assign GT classes to pseudo-labels that have any overlap GT. We additionally report the % unmatched false positives (uFP), i.e., pseud-labels not matched to any GT box*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2402_19463/figures/008_Table_5.jpg]]
*Table 5: Cross-dataset generalization: We evaluate SeMoLi, trained on 90% labeled Waymo Dataset, on Argoverse2 dataset. Note that we never train our approach on Argoverse2. We merge Bicycle and Bicyclist as well as Motorcycle and Motorcyclist since they are not distinguishable by motion*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2402_19463/figures/010_Table_6.jpg]]
*Table 6: Semi-supervised 3D object detction on Waymo Open Dataset: We evaluate models on all (top) and only moving (bottom) on Waymo Open validation set. % GT indicates the amount of labeled training data, % Pseudo indicates the amount of pseudo-labeled data. Table 7. Cross dataset results: We train PP detector on ground truth data as well as on pseudo labels generated with SeMoLi trained on Waymo Open Dataset*

### 数据驱动力验证

SeMoLi的核心主张是伪标签质量可随训练数据增加而单调提升。实验通过改变训练数据比例（Table 3）验证了这一主张：当训练数据从10%增加到90%时，3DIoU F1@0.4从50.4提升到57.6。相比之下，DBSCAN++†的性能与数据量无关，始终维持在16.2左右。这一对比直接证明了数据驱动力是SeMoLi相对于启发式方法的结构性优势。

### 消融实验的关键发现

**图构建策略**（Table 1）：基于位置的kNN图构建在Oracle性能上显著优于基于速度的构建（F1 90.9 vs 51.4）。这是因为空间邻近性提供了更稳定的分组线索，而仅依赖速度特征容易将远处但速度相似的点错误连接。当同时使用速度和位置作为节点特征时，学习性能提升至70.9 F1，表明运动信息作为补充线索而非主导线索时效果最佳。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2402_19463/figures/005_Table_1.jpg]]
*Table 1: SeMoLi 10 ablation (SegIoU): We discuss different strategies on SeMoLi graph construction, as well as edge and node feature parametrization*

**边缘特征设计**（Table 1）：仅使用位置差作为边缘特征优于包含速度特征。这一反直觉的结果说明速度作为边缘特征可能引入噪声——两个点即使速度相似，如果空间距离较远，边缘分类器也难以正确判断其是否属于同一实例。

**包围盒膨胀**（Table 2）：将紧致包围盒膨胀至最小尺寸后，3DIoU F1从30.3跃升至53.1，而分割IoU几乎不变。这表明SeMoLi的点聚类本身是准确的，但提取的包围盒过于紧致，与无障碍真值框存在系统性偏差。简单的膨胀策略有效弥补了这一差距，而基于ICP的配准方法（Table 11）因点云和轨迹预测的噪声反而导致性能下降。

**DBSCAN基线的最小样本数**（Table 12）：在DBSCAN++†的重实现中，设置最小样本数为10个点对避免噪声至关重要。如果不设置此参数，F1从16.2骤降至5.3。这一发现揭示了先前工作[30]中报告的性能与本文重实现之间可能存在差异的原因。

### 失败模式与局限性

1. **静态对象召回率低**：SeMoLi聚焦于移动对象，生成的伪标签偏向运动物体所在区域。这导致PointPillars检测器在“所有对象”上的AP（19.5，0%标注数据）远低于“仅移动对象”上的AP（57.5，Table 6）。这是方法设计的固有限制，而非技术缺陷。
2. **跨类别混淆**：SeMoLi无法区分具有相似运动模式的不同类别（如自行车和摩托车），因为它们基于运动共命运原则被归为同一实例。Table 4的类别评估显示，在某些类别上存在较高的类别混淆率。
3. **包围盒过紧**：尽管膨胀处理部分弥补了问题，但与无障碍真值框仍有差距。这源于SeMoLi仅使用单帧点云和轨迹，无法利用多帧信息进行更精确的无障碍估计。
4. **预处理依赖性**：SeMoLi的性能受限于点云预处理和轨迹预测的质量。场景流估计的噪声会传播到后续的图构建和消息传递过程，影响最终聚类质量。

### 需要人工验证的观察

- [30]中报告的DBSCAN精度/召回率与本文重实现差异很大（Table 12），具体原因需要进一步调查。可能涉及场景流估计方法、点云过滤阈值或评估协议的不同。
- 基于ICP的配准方法在噪声较大时性能下降的具体机制（Table 11）需要更多实验分析来确认。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2402_19463/figures/014_Figure.jpg]]
*Figure: (a) Position-based construction. (b) Velocity-based construction*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2402_19463/figures/003_Figure_3.jpg]]
*Figure 3: Train and validation splits: We conduct our experiments using Waymo training set, for which manual labels are available. We pre-fix two separate validation sets, one for validating pseudo-labels (val pseudo), and one for end-model detector performance (val det). We report performance on varying ratios x for training SeMoLi (train pseudo) and generating pseudo-labels for training our detector (train det)*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2402_19463/figures/004_Table.jpg]]

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2402_19463/figures/009_Table.jpg]]

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2402_19463/figures/011_Table_9.jpg]]
*Table 9: SeMoLi 10 ablation modal upper bound: We report upper bound via oracle, i.e., the achievable performance with segments with at least x _ { f } interior points from GT labels*

## 定位与知识库关联

### 核心瓶颈与因果调控

现有基于启发式的点云运动实例分割方法（如DBSCAN及其多阶段变体）面临的根本瓶颈在于：它们无法利用数据驱动力来提升分割性能，导致稀疏点云下过分割和欠分割严重，且无法有效滤除背景噪声。SeMoLi的因果调控旋钮是将点聚类问题转化为可学习的图分解——使用消息传递网络（MPN）根据空间邻近（proximity）和运动共命运（common fate）原则，以数据驱动的方式学习点之间的边缘分数。核心洞察在于：将运动信息作为一阶线索，结合空间邻近性，通过MPN实现端到端的类不可知点云实例分割，使得伪标签质量可随训练数据增加而单调提升，并可跨数据集泛化。

### 方法定位与基线关系

SeMoLi定位于利用自监督运动线索进行类不可知点云实例分割，并以此为伪标签训练下游目标检测器。与基线方法的本质差异体现在以下关键维度：

| 维度 | 基线方法 | SeMoLi |
|------|---------|--------|
| 聚类机制 | DBSCAN密度聚类（基于空间邻近） | MPN学习边缘分数 + 相关聚类 |
| 运动信息利用 | 场景流过滤静态点（DBSCAN++）或长期速度特征（DBSCAN++l） | 自监督轨迹预测网络获得24帧长程运动模式 |
| 物体特征 | 仅空间位置 | 空间位置 + 速度统计量（均值、最小、最大速度） |
| 图构建 | 无图或基于密度连接 | 基于k近邻（位置）的图结构 |
| 后处理 | 多帧跟踪与ICP配准 | 简单包围盒膨胀至最小尺寸 |

具体基线包括：
- **DBSCAN**：基于密度的聚类方法，仅使用空间位置
- **DBSCAN++**：结合空间聚类和场景流聚类的多阶段启发式方法
- **DBSCAN++l**：在DBSCAN++基础上加入长期速度特征的变体
- **DBSCAN++†**：带启发式尺寸过滤的DBSCAN++版本

### 决定性证据强度

以下证据构成方法有效性的核心支撑（置信度均≥0.95）：

1. **伪标签质量跃升**：SeMoLi在Waymo Open数据集上的3DIoU F1@0.4达到50.4，显著优于DBSCAN++†的16.2（Table 3），提升+34.2点。
2. **噪声大幅降低**：SeMoLi伪标签的未匹配假阳性率仅为14.5%，而DBSCAN++†高达72.0%（Table 4），表明数据驱动方法有效抑制了背景噪声。
3. **下游检测增益**：使用SeMoLi伪标签训练的PointPillars检测器在移动对象上达到57.5 AP（IoU=0.4），比先前启发式方法提升约14个点（Abstract, Table 6）。
4. **跨数据集泛化**：仅在Waymo上训练的SeMoLi在Argoverse2上移动对象3DIoU召回率达到45.8，优于DBSCAN++†的33.3（Table 5），证明学习到的聚类策略具有泛化性。
5. **数据驱动力验证**：随着训练数据增加，SeMoLi的伪标签F1分数从50.4单调提升至57.6（Section 4.3, Table 3），展示了数据驱动方法的规模效应。

### 适用边界与局限

1. **依赖预处理质量**：SeMoLi依赖于点云预处理和轨迹预测的质量，预处理和轨迹预测的噪声会沿管线传播并影响最终聚类性能。
2. **静态对象召回率低**：由于聚焦于移动对象（速度>1m/s），生成的伪标签偏向于移动物体所在区域，导致PointPillars检测器对静态对象的召回率较低——在全部对象上仅19.5 AP（0%标注数据），而移动对象上为57.5 AP（Table 6）。
3. **包围盒紧致性问题**：从点簇提取的包围盒过于紧致，虽然膨胀处理弥补了部分差距，但与无障碍真值框仍有距离（Figure 5直观展示了行人的紧致包围盒与真值框的差异）。
4. **跨类别混淆**：基于运动的伪标签无法区分具有相似运动模式的不同类别（如自行车和摩托车），导致跨类别混淆（Table 4的类级评估揭示了这一问题）。
5. **单帧信息局限**：由于使用单帧点云和轨迹，无法有效利用多帧时序信息进行包围盒的无障碍估计。

### 开放问题

1. **数据增强与静态物体召回**：如何通过数据增强解决PointPillars对移动物体区域的偏差，提升对静态物体的召回率？
2. **时序包围盒估计**：如何利用序列数据获得更精确的无障碍包围盒估计，克服包围盒过紧问题？
3. **ICP配准失效机制**：为什么基于ICP的配准方法在噪声较大的点云和轨迹下反而降低性能（Table 11）？这暗示了运动估计噪声与几何配准之间的深层冲突。
4. **细粒度类别区分**：如何在保持类别无关性的同时，区分具有类似运动速度的不同实例类别？
5. **基线复现差异**：DBSCAN++原论文[30]中报告的精度/召回率与本文重实现差异很大，可能源于最小聚类点数设置（Table 12显示无最小点数时F1从16.2降至5.3）或其他实现细节。
6. **扩展至更多类别**：如果将SeMoLi扩展到城市场景中的更多类别（如动物、滑板等），是否需要额外的训练数据，还是现有运动模式已足够覆盖？

## 原文 PDF

![[paperPDFs/CVPR_2024/SeMoLi_What_Moves_Together_Belongs_Together.pdf]]
