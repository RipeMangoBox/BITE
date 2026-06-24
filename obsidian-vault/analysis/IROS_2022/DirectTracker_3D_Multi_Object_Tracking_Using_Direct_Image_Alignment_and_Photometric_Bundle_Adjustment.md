---
title: "DirectTracker: 3D Multi-Object Tracking Using Direct Image Alignment and Photometric Bundle Adjustment"
type: paper
paper_level: A
venue: IROS
year: 2022
pdf_ref: paperPDFs/IROS_2022/DirectTracker_3D_Multi_Object_Tracking_Using_Direct_Image_Alignment_and_Photometric_Bundle_Adjustment.pdf
project_link: https://cvg.cit.tum.de/research/vslam/directtracker
aliases:
- DirectTracker
tags:
- IROS_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入直接图像对齐（DIA）进行帧间跟踪，利用滑动窗口光度束调整（BA）进行3D检测，并将评估相似度从IoU替换为GIoU，从而摆脱对外部3D检测器的依赖，并公平评价立体跟踪器。"
primary_logic: "通过光度误差最小化实现无检测器的连续3D定位，结合多视图几何与外观信息，可获得全局一致且局部平滑的轨迹；GIoU能够处理非重叠边界框，更准确地反映跟踪器的真实性能。"
claims:
- "Our approach outperforms other methods on the overall HOTA metric in 3D tracking."
- "The bounding box refinement (Sec. VI‑B) adds significant boost to the object detection module using both 3D and 2D metrics."
- "We propose to replace restrictive IoU as a similarity measure by GIoU, which allows to fairly evaluate the performance of stereo-based trackers."
- "KITTI Tracking benchmark (Car class, validation set) 上 HOTA (3D GIoU) = 60.734"
---

# DirectTracker: 3D Multi-Object Tracking Using Direct Image Alignment and Photometric Bundle Adjustment

> [!tip] 核心洞察
> 通过光度误差最小化实现无检测器的连续3D定位，结合多视图几何与外观信息，可获得全局一致且局部平滑的轨迹；GIoU能够处理非重叠边界框，更准确地反映跟踪器的真实性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DirectTracker：利用直接图像对齐与光度束调整的3D多目标跟踪 |
| 英文题名 | DirectTracker: 3D Multi-Object Tracking Using Direct Image Alignment and Photometric Bundle Adjustment |
| 会议/期刊 | IROS 2022 |
| Links | [paper](https://arxiv.org/abs/2209.14965); [Project](https://vision.in.tum.de/research/vslam/directtracker); [Project](https://cvg.cit.tum.de/research/vslam/directtracker) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DirectTracker |
| Dataset | KITTI Tracking benchmark (Car class, validation set) |

> [!tip] 效果简介
> - KITTI Tracking benchmark (Car class, validation set) 上，HOTA (3D GIoU) 为 60.734，对比 outperforms all other compared methods (see Table I)，变化 highest。
> - KITTI Tracking benchmark (Car class, validation set) 上，HOTA (2D IoU) 为 80.913，对比 comparable to offline MOTSFusion, outperforms others (see Table III)，变化 competitive。

## 概述

### 1. 问题背景与瓶颈

3D多目标跟踪（3D MOT）是自动驾驶场景理解的关键任务。现有主流方法普遍采用“检测-跟踪”范式，即依赖外部单帧3D检测器提供目标边界框，再通过卡尔曼滤波或图神经网络进行帧间关联。这一范式存在两个根本性瓶颈：

**瓶颈一：对外部3D检测器的强依赖。** 无论是**AB3DMOT**（Weng et al., IROS 2020）还是**GNN3DMOT**（Weng et al., arXiv 2020），其跟踪质量高度受限于上游检测器的精度。当检测器在远距离或遮挡场景下失效时，跟踪器无法独立恢复目标轨迹。

**瓶颈二：3D IoU评估指标对立体视觉跟踪器的不公平性。** 基于立体视觉的深度估计在远距离存在系统性误差，导致预测的3D边界框与真值框之间出现零重叠。传统3D IoU在此情况下将正确跟踪的目标错误地标记为假阳性或假阴性，严重低估跟踪器的真实性能。

此外，直接视觉里程计（Direct VO）中成熟的光度误差最小化技术尚未被有效引入MOT领域，形成了方法迁移的空白。

### 2. 核心方法：DirectTracker

DirectTracker提出了一种**无检测器依赖**的3D多目标跟踪框架，其核心洞察是：通过光度误差最小化实现连续的3D定位，结合多视图几何与外观信息，可获得全局一致且局部平滑的轨迹。方法包含三大模块：

- **直接图像对齐（DIA）跟踪**：在两帧之间通过最小化Huber-norm光度误差，直接估计目标的刚体变换，摆脱对外部3D检测框的依赖。
- **滑动窗口光度束调整（BA）**：在关键帧窗口内联合优化目标姿态与稀疏3D点云，实现全局一致的3D定位。
- **凸包回归与多视图优化检测**：从稀疏点云估计3D边界框，并通过融合2D-3D约束的非线性最小二乘优化进行细化。

在评估层面，DirectTracker将相似度度量从3D IoU替换为**3D GIoU**（归一化至[0,1]），使非重叠边界框仍能获得有意义的相似度分数，从而公平评价立体视觉跟踪器。

### 3. 方法谱系与知识库定位

DirectTracker处于**直接法视觉里程计**与**多目标跟踪**的交叉地带，其方法谱系定位如下：

| 维度 | 传统方法 | DirectTracker |
|------|----------|---------------|
| 跟踪机制 | 基于外部3D检测框的卡尔曼滤波关联（AB3DMOT） | 两帧DIA粗到精优化 + 滑窗BA |
| 3D检测来源 | 外部单帧检测器（如Frustum PointNets） | 稀疏点云凸包回归 + 多视图2D/3D联合优化 |
| 评估相似度 | 3D IoU | 3D GIoU（归一化至[0,1]） |

相较于离线重建式跟踪方法**MOTSFusion**（Luiten et al., IEEE RA-L 2020），DirectTracker采用在线滑窗BA而非全局离线优化；相较于**SimpleTrack**（Pang et al., arXiv 2021）等在线方法，其核心区别在于不依赖任何预训练的3D检测器，而是从2D语义分割和深度图直接端到端地生成3D轨迹。

### 4. 主要结果与证据强度

在KITTI Tracking基准（Car类，验证集）上，DirectTracker取得了以下关键结果：

- **3D跟踪（GIoU度量）**：HOTA达到60.734，在所有对比方法中最高（Table I，置信度0.9）。
- **2D跟踪（IoU度量）**：HOTA达到80.913，与离线方法MOTSFusion性能相当，优于其他在线方法（Table III，置信度0.9）。
- **边界框细化消融**：优化细化模块对3D和2D检测精度均有显著增益（Table IV，置信度0.95）。
- **深度质量影响**：将立体深度替换为单目深度后，3D性能显著下降，表明方法对深度估计质量有较强依赖（Table IV，置信度0.9）。

### 5. 局限性与开放问题

DirectTracker当前存在以下局限：仅针对汽车类进行验证，假设地面平坦且物体运动约束为4自由度（平移+偏航）；不估计相机全局姿态，可视化需借助外部VO；滑动窗口BA未实现边缘化先验，可能丢失长时序约束信息。

值得关注的开放方向包括：将方法扩展至6自由度物体运动与多类别跟踪；在Argoverse 2等多样化数据集上验证泛化性；探索相机位姿与对象位姿的联合优化以实现完整的视觉SLAM+MOT框架；以及降低对精确深度估计的依赖。

## 背景与动机

多目标跟踪（MOT）是自动驾驶感知栈中的核心组件，其任务是在连续帧中持续定位并关联场景中的所有动态物体。近年来，3D多目标跟踪因其在三维空间中的直接推理能力而受到广泛关注，主流范式遵循“检测-跟踪”流水线：先由外部3D检测器对每一帧独立生成边界框，再通过卡尔曼滤波或图神经网络等关联机制将检测结果串接为轨迹。代表性工作包括**AB3DMOT**（Weng et al., IROS 2020）、**GNN3DMOT**（Weng et al., arXiv 2020）以及在线方法**SimpleTrack**（Pang et al., arXiv 2021）等。离线方法如**MOTSFusion**（Luiten et al., IEEE RA-L 2020）则通过重建式跟踪获得更优的全局一致性，但牺牲了在线推理能力。

然而，这一范式存在两个深层瓶颈。

**第一，对外部单帧3D检测器的强依赖。** 上述方法均假设每帧已具备来自PointRCNN、Frustum PointNets等检测器的精确3D边界框。这不仅将跟踪性能的上限绑定于检测器的质量，更在根本上割裂了检测与跟踪之间的信息流动——检测器无法利用时序一致性，跟踪器也无法反向修正检测误差。对于基于立体视觉的系统，这一矛盾的后果尤为严重：远距离物体的深度估计误差导致3D边界框产生显著偏移，使得相邻帧的同一物体在3D空间中几乎不重叠。

**第二，传统3D IoU评估指标对立体跟踪器的系统性不公平。** 当深度不确定性使预测框与真值框在3D空间中完全分离时，IoU直接退化为零，无论预测在图像平面或深度排序上是否合理。这导致大量“假阳性”和“假阴性”的惩罚并非源于关联错误，而是源于深度估计的固有偏差。因此，基于IoU的评估不仅低估了立体跟踪器的真实关联能力，也阻碍了无需昂贵激光雷达的纯视觉3D MOT方案的发展。

与此同时，直接视觉里程计（Direct Visual Odometry）领域已证明：通过最小化帧间光度误差，可以在不依赖特征点提取与匹配的情况下实现精确的相机位姿估计。这种“直接图像对齐”（Direct Image Alignment, DIA）技术天然适合处理弱纹理、远距离或运动模糊的场景，而这些正是自动驾驶中3D跟踪的典型困难情形。然而，将直接法从相机位姿估计迁移至多目标跟踪面临非平凡挑战：每个物体是独立运动的刚体，其分割掩码可能不精确，且多物体间的遮挡需要显式建模。

**DirectTracker的动机**正是在上述背景下产生：将直接图像对齐与滑动窗口光度束调整（Bundle Adjustment, BA）引入3D MOT，构建一个不依赖外部3D检测器的统一框架。其核心洞察是：通过光度误差最小化实现帧间连续3D定位，结合多视图几何与外观信息，可以获得全局一致且局部平滑的轨迹；同时，将评估相似度从IoU替换为GIoU（Generalized IoU），使非重叠边界框也能获得有意义的相似度评分，从而公平地评价立体跟踪器的真实性能。

## 核心创新

DirectTracker 的核心创新在于颠覆了传统“先检测后跟踪”的范式，构建了一个**无外部3D检测器依赖**的端到端跟踪框架。其关键突破可归结为三个 changed slots：跟踪机制、3D检测来源与评估相似度度量。

### 1. 跟踪机制：从检测框关联到直接图像对齐

传统方法（如 **AB3DMOT** (Weng et al., IROS 2020)、**GNN3DMOT** (Weng et al., arXiv 2020)）依赖外部3D检测器输出的边界框，通过卡尔曼滤波进行帧间状态预测与关联。DirectTracker 则采用**两帧直接图像对齐（Direct Image Alignment, DIA）**，在 SE(3) 空间内通过粗到精优化，最小化分割掩码区域内的光度误差：

$$
\arg \min_{\mathbf{T}_t^{t-1} \in SE(3)} \sum_{\mathbf{p} \in \Omega_t} || \mathbf{I}_{t-1}(\mathbf{p}') - \mathbf{I}_t(\mathbf{p}) ||_{\gamma}
$$

其中 $\mathbf{p}' = \pi( \mathbf{T}_t^{t-1} \pi^{-1}( \mathbf{p}; \mathbf{D}_t(\mathbf{p}) ) )$，$\gamma$ 为 Huber 范数。该机制将跟踪问题转化为连续帧间的光度一致性优化，从根本上摆脱了对稀疏检测框的依赖，使跟踪器能够直接利用稠密图像信息进行3D运动估计。

当3D DIA优化失败或对应像素过少时，系统回退至稀疏光流进行2D跟踪；若2D跟踪同样失败，则判定目标丢失。消融实验（Table IV, Sec. VII‑F）表明，移除该2D回退机制会导致假阴性增加，跟踪精度下降。

### 2. 3D检测来源：从外部检测器到滑窗光度束调整

传统方法使用外部单帧3D检测器（如 Frustum PointNets）提供目标候选框。DirectTracker 则将3D检测内化为系统的一部分，通过**滑动窗口光度束调整（Photometric Bundle Adjustment, BA）** 联合优化目标姿态与稀疏3D点云。其全局光度能量定义为：

$$
E_{\mathrm{photo}} = \sum_{i \in \mathcal{F}} \sum_{\mathbf{q} \in \mathcal{P}_i} \sum_{j \in \mathcal{Q}} E_{i,\mathbf{q},j}
$$

在滑窗BA获得的稀疏点云基础上，通过凸包回归生成初始3D边界框提案，再经多视图非线性优化细化。细化目标函数融合了2D-3D约束、3D-3D约束与正则化项：

$$
\arg \min_{\mathbf{T}_o} \{ w_1 E_{3\mathrm{D}-2\mathrm{D}} + W(E_{3\mathrm{D}-3\mathrm{D}}) E_{3\mathrm{D}-3\mathrm{D}} + w_3 E_{\mathrm{reg}} \}
$$

其中3D-3D残差项惩罚落在边界框外的空间点，并利用深度不确定性进行加权；动态权重 $W(E_{3\mathrm{D}-3\mathrm{D}})$ 在重建误差较大时自动降低该项影响。消融实验（Table IV）证实，该边界框细化模块对3D和2D检测精度均有**显著增益**，是系统性能的关键贡献因素。

### 3. 评估相似度度量：从3D IoU到3D GIoU

现有3D MOT评估普遍采用3D IoU作为相似度度量。然而，基于立体视觉的跟踪器因远距离物体的深度估计误差，常导致预测框与真值框**零重叠**，从而产生大量虚假的假阳性和假阴性，使评估结果无法真实反映跟踪器性能。DirectTracker 提出以**3D GIoU（Generalized IoU，归一化至[0,1]）**替代IoU，利用GIoU对非重叠边界框仍能提供有意义的距离度量这一特性，实现对立体跟踪器的公平评价。Table I（3D GIoU）与 Table II（3D IoU）的对比清晰地展示了度量变更对评估结果的显著影响，验证了该创新的必要性。

### 创新间的因果耦合

上述三个 changed slots 并非孤立存在，而是形成了紧密的因果链条：DIA 与滑窗BA 使系统脱离了对外部3D检测器的依赖，但同时也导致生成的边界框在远距离处精度受限；GIoU 的引入正是为了在评估层面补偿这一固有特性，使性能评价回归公平。三者协同作用，构成了 DirectTracker “检测-跟踪-评估”一体化的核心创新逻辑。

## 整体框架

DirectTracker 提出了一种**无外部3D检测器的端到端3D多目标跟踪框架**，其核心创新在于将直接图像对齐（Direct Image Alignment, DIA）与基于滑动窗口的光度束调整（Bundle Adjustment, BA）有机结合，形成“跟踪即检测”的闭环系统。整体流程如 Fig. 2 所示，包含三个并行独立工作的核心模块：

1. **对象跟踪模块（Object Tracking）**：基于两帧间直接图像对齐进行3D运动估计，并在图像空间通过匈牙利算法完成2D关联。该模块仅依赖语义分割掩码和深度图，不依赖于任何3D边界框，从而摆脱了传统跟踪方法对外部3D检测器的强依赖。

2. **基于对象的束调整模块（Object-based Bundle Adjustment）**：在滑动窗口内联合优化对象姿态与稀疏3D点云，通过最小化多帧光度误差获得全局一致的3D定位。该模块将直接视觉里程计中的BA技术首次有效迁移至MOT任务中。

3. **3D对象检测模块（3D Object Detection）**：从稀疏滑窗点云出发，通过凸包回归生成初始3D提案，再经由多视图2D/3D联合非线性优化进行细化，最终通过姿态融合输出稳定的3D边界框。

三个模块的协作机制如下：对象跟踪模块为每个对象提供帧间相对位姿初值；束调整模块在关键帧窗口内对位姿和3D点进行联合精化；检测模块则利用精化后的点云生成并优化3D框。**除关联步骤需对所有对象联合执行外，3D检测与跟踪均独立并行运行**，这种解耦设计使得系统在保持全局一致性的同时具备在线处理能力。

输入输出方面，系统以双目（或单目）图像序列、语义分割掩码和深度估计图为输入，输出为每个对象的3D边界框及其在相机坐标系下的连续轨迹。值得注意的是，DirectTracker 不估计相机全局位姿，所有对象位姿均表达于相机坐标系中；可视化时需借助外部视觉里程计系统（如[9]）将轨迹投影至世界坐标系。

### 补充图表

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2209_14965/figures/001_Figure_1.jpg]]
*Figure 1: Qualitative result of our method. Top: 3D object proposals are projected and visualized in the image domain. Bottom: We present object detections and accumulated sparse pointclouds in the world coordinate system. Red dashed bounding boxes represent ground truth objects, whereas the red marks on the ground plane indicate ground truth object positions. Object trajectories are globally consistent. For the moving car on the right the track also exhibits local smoothness. Please note that DirectTracker does not estimate camera poses. Thus we utilize estimates from the visual odometry system [9] for visualization in the world coordinate system*

## 核心模块与公式推导

DirectTracker 由三大核心模块构成：**对象跟踪（Object Tracking）**、**基于对象的束调整（Object-based Bundle Adjustment）** 和 **3D对象检测（3D Object Detection）**。除关联步骤外，跟踪与检测模块独立并行运行（见 Fig. 2），系统不依赖任何外部3D检测器。

### 对象跟踪：两帧直接图像对齐

跟踪模块通过**直接图像对齐（Direct Image Alignment, DIA）** 估计相邻帧间对象的刚体变换。给定当前帧 $t$ 中对象实例的分割掩码 $\Omega_t$，优化目标为最小化掩码区域内像素的光度误差：

$$\arg \min_{\mathbf{T}_t^{t-1} \in SE(3)} \sum_{\mathbf{p} \in \Omega_t} \| \mathbf{I}_{t-1}(\mathbf{p}') - \mathbf{I}_t(\mathbf{p}) \|_{\gamma}$$

其中 $\mathbf{p}'$ 为当前像素 $\mathbf{p}$ 经深度反投影和刚体变换后在前一帧的投影坐标：

$$\mathbf{p}' = \pi\left( \mathbf{T}_t^{t-1} \pi^{-1}\left( \mathbf{p}; \mathbf{D}_t(\mathbf{p}) \right) \right)$$

$\|\cdot\|_{\gamma}$ 为 Huber 范数，以增强对光照变化和遮挡的鲁棒性。优化采用**粗到精（coarse-to-fine）** 的金字塔策略：在低分辨率层初始化姿态，逐层细化至高分辨率层。

对于新轨迹的姿态初始化，系统生成一组姿态候选，仅在**最稀疏的金字塔层级**上比较最终代价值，选择最优候选作为初始估计。若3D DIA 优化失败或对应像素过少，系统回退至**稀疏光流2D跟踪**；若2D跟踪亦失败，对象被视为丢失。

跟踪完成后，所有对象的**关联（association）** 在图像空间中完成：计算当前帧分割掩码与经 DIA 变换后的上一帧掩码之间的 IoU 分数，使用匈牙利算法求解最优匹配。

### 基于对象的滑动窗口束调整

为获得全局一致的3D对象姿态，DirectTracker 在滑动窗口内对关键帧集合 $\mathcal{F}$ 进行**光度束调整（Photometric Bundle Adjustment）**。总光度能量定义为：

$$E_{\mathrm{photo}} = \sum_{i \in \mathcal{F}} \sum_{\mathbf{q} \in \mathcal{P}_i} \sum_{j \in \mathcal{Q}} E_{i,\mathbf{q},j}$$

其中 $\mathcal{P}_i$ 为关键帧 $i$ 中对象掩码内提取的稀疏点集，$\mathcal{Q}$ 为观测到点 $\mathbf{q}$ 的帧集合。单点残差 $E_{i,\mathbf{q},j}$ 采用**局部缩放差平方和（Locally-Scaled Sum of Squared Differences, LSSD）** 配合 Huber 范数：

$$E_{i,\mathbf{q},j} = \sum_{\mathbf{p} \in \mathcal{N}_{\mathbf{q}}} \left\| \mathbf{I}_j(\mathbf{p}') - \frac{\sum_{\mathbf{p} \in \mathcal{N}_{\mathbf{q}}} \mathbf{I}_j(\mathbf{p}')}{\sum_{\mathbf{p} \in \mathcal{N}_{\mathbf{q}}} \mathbf{I}_i(\mathbf{p})} \mathbf{I}_i(\mathbf{p}) \right\|_{\gamma}$$

$\mathcal{N}_{\mathbf{q}}$ 为以点 $\mathbf{q}$ 为中心的图像块。LSSD 通过对参考帧和观测帧的局部亮度进行归一化，有效补偿全局光照变化。BA 联合优化对象在关键帧集合中的姿态及稀疏3D点位置，为后续检测模块提供高精度的稀疏点云。

### 3D对象检测：凸包回归与多视图优化

检测模块基于 BA 输出的稀疏滑动窗口点云生成3D边界框提案，并进一步细化。

**初始提案生成**：假设地面平坦且对象运动约束为4自由度（平移 + 偏航），在对象点云的**凸包（convex hull）** 上拟合最小面积定向包围盒，得到初始3D框。

**多视图非线性优化细化**：将初始提案作为初值，通过非线性最小二乘优化联合利用多视图2D和3D信息：

$$\arg \min_{\mathbf{T}_o} \left\{ w_1 E_{3\mathrm{D}-2\mathrm{D}} + W(E_{3\mathrm{D}-3\mathrm{D}}) E_{3\mathrm{D}-3\mathrm{D}} + w_3 E_{\mathrm{reg}} \right\}$$

优化目标由三项构成：

- **$E_{3\mathrm{D}-2\mathrm{D}}$**：3D框投影与2D检测框/分割掩码之间的一致性约束。
- **$E_{3\mathrm{D}-3\mathrm{D}}$**：惩罚落在对象边界框外的3D点，并引入深度不确定性加权：

$$E_{3\mathrm{D}-3\mathrm{D}} := \sum_{i \in \mathcal{F}} \sum_{\mathbf{x} \in \mathcal{P}_i^{3\mathrm{D}}} \max\left\{\mathbf{0}, \frac{|\mathbf{T}_o^{-1} \mathbf{T}_i \mathbf{x}| - \frac{1}{2}\mathbf{d}}{\sigma_{\mathbf{x}}}\right\}_{\gamma}$$

其中 $\mathbf{d}$ 为边界框尺寸，$\sigma_{\mathbf{x}}$ 为点 $\mathbf{x}$ 的深度不确定性。**动态权重** $W(E_{3\mathrm{D}-3\mathrm{D}})$ 在3D重建误差较大时自动降低该项的影响，避免稀疏点云噪声主导优化。

- **$E_{\mathrm{reg}}$**：正则化项，约束优化后的姿态不偏离上一帧估计值：

$$E_{\mathrm{reg}} := \| \mathrm{Log}(\mathbf{T}_o^{-1} \mathbf{T}_o^{\prime}) \|$$

**姿态融合**：细化后的对象提案通过加权平均与历史估计融合，利用对角协方差矩阵 $\pmb{\Sigma}_m$ 和朝向角误差 $\sigma_m$ 进行不确定性加权：

$$\hat{\mathbf{c}} = (\pmb{\Sigma}_p + \pmb{\Sigma}_m)^{-1} (\pmb{\Sigma}_p \mathbf{c}_m + \pmb{\Sigma}_m \mathbf{c}_p)$$

其中 $\mathbf{c}_m$ 为当前测量位置，$\mathbf{c}_p$ 为先验位置，$\pmb{\Sigma}_m$ 和 $\pmb{\Sigma}_p$ 分别为对应的协方差矩阵。

## 实验与分析

### 评估设置与度量创新

DirectTracker在KITTI Tracking基准的Car类验证集上进行评估。为公平评价基于立体视觉的跟踪器，作者提出将相似度度量从传统的3D IoU替换为**3D GIoU**（归一化至[0,1]）。这一改变的核心动机在于：远距离物体的深度估计误差会导致预测框与真值框零重叠，传统IoU会将其错误地判定为假阳性或假阴性，从而低估跟踪器的真实性能。GIoU能处理非重叠边界框，提供更连续的相似度信号。主评估指标采用**HOTA**，它分解为检测精度（DetA）和关联精度（AssA），能更全面地反映跟踪器的综合能力。所有结果均使用官方TrackEval工具计算，并扩展了3D GIoU支持以确保对比公正性。

### 3D多目标跟踪主结果

Table I给出了基于3D GIoU的3D跟踪对比结果。DirectTracker在整体HOTA指标上达到**60.734**，优于所有对比方法。具体而言：

- **AB3DMOT**（Weng et al., IROS 2020）使用PointRCNN检测器时HOTA为47.8，使用Frustum PointNets时为41.8；
- **GNN3DMOT**（Weng et al., arXiv 2020）在相同检测器下分别为48.9和42.6；
- **MOTSFusion**（Luiten et al., IEEE RA-L 2020）作为离线重建式跟踪器，HOTA为50.9；
- **SimpleTrack**（Pang et al., arXiv 2021）与PointRCNN组合时达到55.1。

DirectTracker的高召回率（DetRe 68.573）源于其机会主义跟踪策略——对每个2D检测到的物体都尝试建立3D轨迹。但这也影响了精确率（DetPr 48.048）和整体定位精度（LocA 76.830），反映出无检测器方法在边界框精度上的固有局限。关联精度AssA达到68.573，表明DIA跟踪与滑窗BA机制能有效维持轨迹一致性。

**Table II**展示了使用传统3D IoU度量的结果对比，揭示了度量变更对评估结论的深刻影响。在IoU度量下，DirectTracker的HOTA大幅下降（具体数值需查看原表），因为大量远距离物体的预测框与真值框零重叠，被错误地惩罚为假阳性和假阴性。这验证了GIoU对于立体跟踪器公平评价的必要性。

### 2D多目标跟踪结果

Table III给出了基于2D IoU的HOTA和CLEARMOT指标对比。DirectTracker在2D跟踪上达到HOTA **80.913**，与离线方法MOTSFusion（80.4）性能相当，显著优于其他在线方法。这表明尽管DirectTracker的核心创新在3D领域，其2D跟踪能力同样具有竞争力——DIA在图像空间的直接对齐为2D关联提供了天然优势。

### 消融实验

Table IV系统分析了各组件对性能的贡献，同时评估3D GIoU和2D IoU指标：

**深度质量的影响**：将立体深度估计器（DispNet3）替换为单目深度估计器（Adabins）后，3D性能显著下降。这确认了DirectTracker对准确深度估计的强依赖——DIA的光度误差优化需要可靠的深度初始化，BA中的3D-3D约束也依赖稀疏点云的质量。

**2D跟踪回退机制**：移除2D跟踪回退（即3D DIA失败后不使用稀疏光流进行2D关联）会增加假阴性，降低跟踪精度。该回退机制在遮挡或大运动场景中起到关键兜底作用。

**边界框细化优化**：移除Sec. VI‑B的优化细化模块对3D和2D检测精度均有显著增益（置信度0.95）。该模块通过联合优化2D-3D约束、3D-3D约束和正则化项，有效提升了边界框的定位精度和跨视图一致性。

**灰度DIA vs 彩色DIA**：从彩色DIA切换为灰度DIA对性能影响极小，表明灰度视频流可达到相近精度。这降低了方法对颜色信息的依赖，增强了在低质量视频上的适用性。

**外部尺寸先验**：使用Frustum PointNets提供的外部3D框尺寸可提升结果，但不使用时DirectTracker仍具竞争力。这说明自有的凸包回归+优化细化流程已能产生合理的尺寸估计。

### 失败模式与局限性

1. **远距离物体定位精度**：尽管GIoU缓解了评估不公平问题，但远距离物体的深度误差仍导致LocA偏低（76.830），影响整体检测精度。
2. **4自由度运动假设**：方法假设地面平坦，物体仅具有平移和偏航自由度，无法处理俯仰和翻滚变化，限制了在非平坦道路上的应用。
3. **类别单一**：仅在Car类上验证，未扩展到行人、自行车等其他类别。
4. **深度估计依赖**：消融实验明确显示，深度质量是性能瓶颈。单目深度替代方案导致显著退化。
5. **无全局相机位姿**：不估计相机全局姿态，所有对象位姿均为相机坐标系下的相对估计，可视化需借助外部VO系统。

### 关键图表结论

- **Fig. 1**：定性展示了DirectTracker在图像域和世界坐标系中的3D物体提案与轨迹。轨迹呈现全局一致性和局部平滑性，验证了DIA+BA框架的有效性。红色虚线框为真值，红色地面标记为真值位置。
- **Fig. 2**：系统流程图揭示了三大核心模块（跟踪、束调整、检测）的并行独立工作方式，除联合关联步骤外各模块解耦执行，体现了设计的模块化优势。
- **Table I**：核心结果表，确立DirectTracker在3D HOTA上的领先地位。
- **Table IV**：消融实验表，量化了深度质量、2D回退、细化优化等关键设计选择的影响。

### 补充图表

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2209_14965/figures/003_Table.jpg]]
*Table: I*

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2209_14965/figures/004_Table.jpg]]
*Table: EVALUATION OF 3D TRACKING BASED ON 3D GIOU. OUR APPROACH OUTPERFORMS OTHER METHODS ON THE OVERALL HOTA METRIC. THE RECALL IS HIGH SINCE WE OPPORTUNISTICALLY TRACK EVERY OBJECT. NONETHELESS, IT IMPACTS THE PRECISION LEVELS AND OVERALL LOCALIZATION ACCURACY. THE BEST RESULTS PER METRIC ARE INDICATED IN BOLD. TABLE II*

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2209_14965/figures/005_Table.jpg]]
*Table: EVALUATION OF 3D TRACKING BASED ON 3D IOU. WE DEMONSTRATE HOW THE CHANGE OF SIMILARITY MEASURE AFFECTS THE PERFORMANCE OF OUR APPROACH AS MANY BIASED, NON-OVERLAPPING BOUNDING BOXES PENALIZE THE ACCURACY OF OUR TRACKER. THE BEST RESULTS PER METRIC ARE INDICATED IN BOLD. TABLE III EVALUATION OF 2D TRACKING ON HOTA AND CLEARMOT METRICS BASED ON 2D IOU. OUR APPROACH IS COMPETITIVE AGAINST OTHER METHODS ACROSS ALL METRICS AND DEMONSTRATES THE PERFORMANCE COMPARABLE TO THE OFFLINE MOTSFUSION. THE BEST RESULTS ARE INDICATED IN BOLD*

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2209_14965/figures/006_Table.jpg]]
*Table: IV ABLATION STUDY. WE PRESENT THE PERFORMANCE OF OUR METHOD WITH DIFFERENT COMPONENTS OF THE PIPELINE REMOVED OR REPLACED. THE EVALUATION IS CONDUCTED FOR BOTH 3D (GIOU) AND 2D TRACKING (IOU)*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

DirectTracker 在 3D 多目标跟踪（MOT）领域占据一个独特的位置：它同时摆脱了对“外部单帧 3D 检测器”和“传统 3D IoU 评估”的双重依赖，将直接法视觉里程计（Direct VO）的光度误差最小化范式引入 MOT 任务。

**相对于主流 tracking-by-detection 范式**，DirectTracker 与以下基线形成鲜明对比：

- **AB3DMOT** (Weng et al., IROS 2020)：典型的两阶段 pipeline——先由外部 3D 检测器（如 Frustum PointNets）生成单帧检测框，再用卡尔曼滤波进行帧间关联。DirectTracker 则通过两帧直接图像对齐（DIA）完成帧间跟踪，并以滑窗光度束调整（BA）替代外部检测器，实现“无检测框”的跟踪流程。
- **GNN3DMOT** (Weng et al., arXiv 2020)：在图神经网络框架内仍依赖外部 3D 检测框进行关联学习。DirectTracker 的关联则发生在 2D 图像空间，基于 DIA 翘曲分割掩码与输入掩码的 IoU 分数，通过匈牙利算法完成。
- **SimpleTrack** (Pang et al., arXiv 2021)：作为在线 3D MOT 基线，同样依赖外部检测器。DirectTracker 的在线特性体现于逐帧 DIA 优化与滑窗 BA 的增量更新，而非检测-关联的解耦架构。

**相对于 tracking-by-reconstruction 范式**，DirectTracker 与 **MOTSFusion** (Luiten et al., IEEE RA-L 2020) 共享“从重建中检测与跟踪”的思想，但存在关键差异：MOTSFusion 是离线方法，需要完整序列进行 3D 重建与轨迹求解；DirectTracker 采用滑窗 BA，在保持全局一致性的同时支持在线运行。在 2D HOTA 指标上，DirectTracker 与离线 MOTSFusion 性能相当（Table III），验证了滑窗策略的有效性。

**相对于直接法视觉里程计**，DirectTracker 将 DSO 式的光度误差最小化从相机位姿估计迁移到物体位姿估计。核心创新在于：将逐像素的光度误差限制在实例分割掩码区域内，并引入多物体并行 DIA + 联合关联的机制，解决了直接法在动态场景中的对象级跟踪问题。

### 2. 适用边界与关键假设

DirectTracker 的设计隐含以下强假设，构成其适用边界：

1. **4 自由度运动模型**：假设地面平坦，物体运动仅包含平移（x, z）和偏航角（yaw），无法处理俯仰（pitch）和翻滚（roll）变化。这使其不适用于越野、坡道或飞行器场景。
2. **汽车类单一类别**：所有实验仅在 KITTI 的 Car 类上进行，未在行人、自行车等非刚体或多姿态变化类别上验证。
3. **依赖语义分割与 2D 检测**：DIA 需要实例分割掩码定义优化区域；3D 检测需要 2D 边界框提供投影约束。虽不要求像素级精确，但前端模块的失效会传播至整个 pipeline。
4. **不估计相机全局位姿**：所有物体位姿在相机坐标系下计算，可视化需借助外部视觉里程计（VO）系统。这使 DirectTracker 更接近“以相机为中心的物体跟踪器”，而非完整的 SLAM+MOT 框架。
5. **深度估计质量敏感**：消融实验（Table IV）表明，将立体深度（DispNet3）替换为单目深度（Adabins）后，3D 性能显著下降，揭示了方法对准确深度估计的强依赖。

### 3. 局限与已知失效模式

基于论文提供的消融实验与定性分析，可识别以下局限：

| 局限类别 | 具体表现 | 证据锚点 |
|---------|---------|---------|
| 深度依赖性 | 单目深度替代导致 3D HOTA 大幅下降 | Table IV, Sec. VII‑F |
| 2D 跟踪回退 | 移除 2D 跟踪回退机制会增加假阴性（FN），降低跟踪精度 | Table IV, Sec. VII‑F |
| 滑窗信息丢失 | 滑窗 BA 未实现边缘化先验，可能丢失长时序约束信息 | 论文局限性自述 |
| 类别泛化 | 仅在 Car 类上评估，未验证多类别扩展 | 实验设置 |
| 运动模型限制 | 4 自由度假设无法处理俯仰/翻滚，对颠簸路面或翻转物体失效 | 方法设计 |

值得注意的是，边界框细化优化模块（Sec. VI‑B）对 3D 和 2D 检测精度均有显著增益（Table IV），表明多视图 2D-3D 联合优化是该 pipeline 的关键组件，移除后将严重损害性能。此外，从彩色 DIA 切换为灰度 DIA 对性能影响极小，说明光度对齐主要依赖纹理梯度而非颜色信息。

### 4. 开放问题与未来方向

基于 DirectTracker 的设计边界与局限，以下开放问题值得后续工作探索：

1. **6 自由度扩展与多类别跟踪**：如何将运动模型从 4 自由度（SE(2) 约束）扩展至完整的 6 自由度刚体运动（SE(3)），并支持行人、自行车等非刚体或高动态类别？这需要重新设计姿态参数化与正则化策略。

2. **跨数据集泛化验证**：当前仅 KITTI 验证集上的结果不足以证明泛化性。在 Argoverse 2、nuScenes 等更复杂的城市驾驶数据集上评估，可检验方法对密集交通、复杂光照和长序列的鲁棒性。

3. **联合相机-物体位姿优化**：DirectTracker 不估计相机位姿，割裂了场景理解与自运动估计。将相机位姿与多物体位姿纳入统一的滑窗 BA 框架，有望实现完整的视觉 SLAM+MOT 系统。

4. **减轻深度估计依赖**：单目深度替代实验暴露了深度质量的瓶颈效应。融合多模态传感器（如低成本 LiDAR 稀疏点云）或改进单目深度估计网络（如使用时序信息），可降低对立体深度的刚性依赖。

5. **端到端学习化**：当前 DIA 和 BA 均基于手工设计的 Huber-norm 光度误差，未进行数据驱动的端到端优化。学习型特征度量（如深度特征图对齐）或可微分 BA 层可能进一步提升跟踪精度与鲁棒性。

6. **3D GIoU 度量的标准化**：DirectTracker 提出以 3D GIoU 替代 3D IoU 作为相似度度量，以公平评估立体跟踪器。该度量是否能成为 3D MOT 社区的标准评估指标，需要在更广泛的跟踪器和方法上进行基准测试与共识建立。

## 原文 PDF

![[paperPDFs/IROS_2022/DirectTracker_3D_Multi_Object_Tracking_Using_Direct_Image_Alignment_and_Photometric_Bundle_Adjustment.pdf]]
