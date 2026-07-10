---
title: "HRBF-Fusion: Accurate 3D Reconstruction From RGB-D Data Using On-the-fly Implicits"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/HRBF_Fusion_Accurate_3D_Reconstruction_From_RGB_D_Data_Using_On_the_fly_Implicits.pdf
project_link: null
code_link: null
aliases:
- HRBF-Fusion
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入两阶段“先粗后精”的在线多模态3D MOT框架，通过粗轨迹生成与跨模态轨迹精化实现双向交叉校正（Sec.III.A, Fig.3）。
primary_logic: 将两阶段检测思想推广至3D MOT，创新性地将融合过程分解为粗匹配与精化两步，并在精化阶段以5类交叉校正操作系统地恢复两个模态中被误删或遗漏的目标，从而生成更鲁棒的LiDAR 3D轨迹。
claims:
- 在KITTI测试集的Car类别上，CrossTracker在HOTA指标上超越此前最优在线方法CasTrack 3.55%（CasA检测器）和2.07%（VirConv检测器）
- 消融实验中，仅使用LiDAR单阶段跟踪的HOTA为78.08%，加入完整TR模块后提升至83.78%（+5.70%）
- 多模态建模模块M3中增加点云几何特征后，分类器F1分数从94.58提升至96.90
- KITTI test set (Car) 上 HOTA = 80.87 (OursC2L2 with CasA+RRC)
---

# HRBF-Fusion: Accurate 3D Reconstruction From RGB-D Data Using On-the-fly Implicits

> [!tip] 核心洞察
> 将两阶段检测思想推广至3D MOT，创新性地将融合过程分解为粗匹配与精化两步，并在精化阶段以5类交叉校正操作系统地恢复两个模态中被误删或遗漏的目标，从而生成更鲁棒的LiDAR 3D轨迹。

| 字段 | 内容 |
|------|------|
| 中文题名 | CrossTracker: 基于交叉校正的鲁棒多模态3D多目标在线跟踪 |
| 英文题名 | HRBF-Fusion: Accurate 3D Reconstruction From RGB-D Data Using On-the-fly Implicits |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://3d.bk.tudelft.nl/liangliang/publications.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | CrossTracker |
| Dataset | KITTI test set, KITTI validation set |

> [!tip] 效果简介
> - KITTI test set (Car) 上，HOTA 80.87 (OursC2L2 with CasA+RRC) vs 77.32 (CasTrackL2 with same detectors) (+3.55)；HOTA 82.04 (OursC3L3 with VirConv+Perma) vs 79.97 (CasTrackL3 with same detectors) (+2.07)。
> - KITTI validation set (Car) 上，HOTA 83.78 (CrossTracker full two-stage) vs 78.08 (LiDAR-only single-stage tracking) (+5.70)。

## 概要

现有相机-激光雷达融合的3D多目标在线跟踪方法普遍采用单阶段架构，按固定顺序处理不同检测集，仅能单向利用相机修正激光雷达的漏检与误检，无法同时纠正相机流中的跟踪失败，导致多模态互补潜力未被充分释放。针对此瓶颈，本文提出**CrossTracker**——首个在线两阶段多模态3D MOT框架。其核心思路是将融合过程分解为“粗轨迹生成（C-TG）”与“跨模态轨迹精化（TR）”两步：首先由多模态建模模块M³融合图像、平面几何与点云特征，输出对象间的一致性概率；随后C-TG在单模态内关联生成初步的相机与LiDAR粗轨迹；最后TR通过五类交叉校正操作，在相机与LiDAR流之间双向恢复被误删或遗漏的目标，最终输出高质量的LiDAR 3D轨迹。在KITTI测试集的Car类别上，CrossTracker在HOTA指标上超越此前最优在线方法CasTrack达3.55%（使用相同CasA检测器），验证集消融显示两阶段交叉校正相较LiDAR单阶段跟踪提升5.70% HOTA。该方法以“两阶段粗到精”的架构创新改变了现有多模态跟踪中缺失双向交叉校正的现状，为后续多传感器在线跟踪提供了新的范式参考。

## 核心方法与创新机理

### 一、问题瓶颈与核心洞察

现有相机-激光雷达融合的3D多目标跟踪方法（如**EagerMOT**（Kim et al., ICRA 2021）等）普遍采用单阶段顺序处理架构：先将检测结果分为“LiDAR-相机共同检测”、“仅LiDAR检测”、“仅相机检测”三类，再按固定顺序依次关联，最后仅用相机检测单向修正LiDAR跟踪失败。这种单阶段架构存在根本性局限——它无法利用独立的轨迹精化阶段实现相机与LiDAR之间的**双向交叉校正**，导致难以同时处理两个模态的误检与漏检（Fig. 1, Fig. 2）。

![[assets/figures/papers/paper_list_l2_https_3d_bk_tudelft_nl_liangliang_publications_html/figures/002_Figure_2.jpg]]
*Figure 2: The advantages and disadvantages of existing data fusion-based multi-modal 3D MOT methods [8]–[10]. These methods can effectively address (a) false detections in either the camera or LiDAR stream and (b) missing detections solely in the LiDAR stream. However, they are limited in their ability to handle (c) missing detections solely in the camera stream and (d) missing detections in both camera and LiDAR streams. In contrast, our CrossTracker draws on the coarse-to-fine concept, effectively addressing all four of these challenges through an innovative two-stage tracking scheme*

![[assets/figures/papers/paper_list_l2_https_3d_bk_tudelft_nl_liangliang_publications_html/figures/001_Figure_1.jpg]]
*Figure 1: Main difference between CrossTracker and its competitors. Prior methods [8]–[10] typically categorize input detections into three sets using data fusion, and then sequentially process these detection sets based on spatial geometric constraints (SGC, e.g., 3D-IoU). They typically start with LiDARcamera detections, followed by LiDAR-only detections. Finally, they use camera-only detections to correct tracking failures caused by potential LiDAR detection problems. However, they are unable to correct tracking failures in the camera stream using their single-stage architecture. Differently, our CrossTracker, the first online two-stage 3D MOT solution, excels in addressing intricate tracking fail...*

具体而言，现有方法能有效应对两类问题：(a) 任一模态的误检；(b) 仅LiDAR漏检。但面对(c) 仅相机漏检和(d) 两模态同时漏检时则无能为力（Fig. 2）。CrossTracker的核心洞察是：**将两阶段检测中“先粗后精”的思想推广至3D MOT**，创新性地将融合过程分解为粗轨迹生成（C-TG）与跨模态轨迹精化（TR）两步，并在精化阶段以5类交叉校正操作系统性地恢复两个模态中被误删或遗漏的目标。

### 二、架构总览：两阶段粗到精框架

CrossTracker是首个在线两阶段多模态3D MOT框架，由三个关键模块串联构成（Fig. 3）：

![[assets/figures/papers/paper_list_l2_https_3d_bk_tudelft_nl_liangliang_publications_html/figures/003_Figure_3.jpg]]
*Figure 3: Overview of CrossTracker. It is the first two-stage multi-modal 3D MOT framework comprising three essential modules: a multi-modal modeling (M3) module, a coarse trajectory generation (C-TG, i.e., stage-1) module, and a trajectory refinement (TR, i.e., stage-2) module. At each frame after the initial frame*

1. **M³（Multi-modal Modeling，多模态建模模块）**：融合图像、平面几何与点云特征，输出对象间的一致性概率，为后续关联提供鲁棒测度。
2. **C-TG（Coarse Trajectory Generation，粗轨迹生成模块，即Stage-1）**：利用M³测度与空间几何约束（SGC），在单模态内关联当前检测与历史轨迹，生成初步的相机粗轨迹和LiDAR粗轨迹。
3. **TR（Trajectory Refinement，轨迹精化模块，即Stage-2）**：通过三步五类交叉校正操作，在相机流与LiDAR流之间转移新出现目标、恢复被误删的轨迹，最终输出高质量的LiDAR 3D轨迹。

在每个时间步 $t$，系统接收相机检测集 $D_t^c$ 和LiDAR检测集 $D_t^l$，以及历史轨迹 $T_{t-1}^c$ 和 $T_{t-1}^l$。C-TG通过数据关联生成匹配轨迹 $T_t^k$、未匹配检测 $UD_t^k$ 和未匹配轨迹 $UT_t^k$（$k \in \{c, l\}$）。TR模块随后对 $UD_t^k$ 和 $UT_t^k$ 执行交叉校正，更新最终的轨迹集合。

### 三、Changed Slot 1：跨模态特征关联测度——M³模块

**基线方法**依赖手工空间几何约束（如3D-IoU）或多个独立特征进行对象关联，缺乏对多模态特征的统一建模。**CrossTracker**提出端到端的M³网络，首次将图像特征建模（IFM）、平面几何特征建模（GFM）和点云特征建模（PFM）与一致性概率估计统一到一个网络中（Fig. 4）。

#### 3.1 图像特征建模（IFM）

对于帧 $t-1$ 的对象 $i$ 和帧 $t$ 的对象 $j$，IFM以两帧图像和对应的2D检测框为输入。具体操作：
- 将两个对象的2D边界框分别从各自帧的图像中裁剪并拼接为双通道输入。
- 通过共享权重的ResNet-18骨干网络提取联合图像特征 $F_{img} \in \mathbb{R}^{1 \times 512}$。

#### 3.2 平面几何特征建模（GFM）

GFM将2D边界框转化为伪点云补丁以编码平面几何信息：
- 在每个2D框内随机采样512个点，形成伪点云补丁 $P \in \mathbb{R}^{512 \times 2}$。
- 将补丁输入PointNet + MaxPooling，输出平面几何特征 $F_{pg} \in \mathbb{R}^{1 \times 512}$。

这种设计使网络能够感知边界框的形状、位置和尺度等平面几何属性，而无需显式的3D信息。

#### 3.3 点云特征建模（PFM）

PFM利用LiDAR点云提供3D结构信息：
- 对于每个2D检测框，将其对应的3D LiDAR检测框内的点云通过PointNet + MaxPooling提取点云特征 $F_{pc} \in \mathbb{R}^{1 \times 512}$。
- 若某对象无对应3D检测（如仅相机检测），则用零向量填充。

#### 3.4 一致性概率估计与分类器

三种模态特征 $F_{img}$、$F_{pg}$、$F_{pc}$ 沿通道维度拼接后输入分类器。分类器为两个模态分别设计（相机分类器和LiDAR分类器），各自输出对象对 $(i, j)$ 的一致性概率（即相似度分数）。对于模态 $k$，所有历史对象与当前检测之间的相似度构成代价矩阵 $S^k$：

$$S^{k} = \begin{bmatrix}
S_{1,1}^{k} & S_{1,2}^{k} & \cdots & S_{1,N_{t}^{k}}^{k} \\
S_{2,1}^{k} & S_{2,2}^{k} & \cdots & S_{2,N_{t}^{k}}^{k} \\
\vdots & \vdots & \ddots & \vdots \\
S_{M_{t-1}^{k},1}^{k} & S_{M_{t-1}^{k},2}^{k} & \cdots & S_{M_{t-1}^{k},N_{t}^{k}}^{k}
\end{bmatrix}$$

其中 $S_{i,j}^k$ 表示帧 $t-1$ 的第 $i$ 个对象与帧 $t$ 的第 $j$ 个对象在模态 $k$ 下的一致性概率，$M_{t-1}^k$ 和 $N_t^k$ 分别为历史对象数和当前检测数。该矩阵为后续C-TG的数据关联提供核心测度。

### 四、Changed Slot 2：跟踪架构——从单阶段到两阶段

**基线方法**（如EagerMOT）采用单阶段分步融合，顺序处理不同检测集且无显式精化。**CrossTracker**引入两阶段粗到精架构，其Stage-1（C-TG）与Stage-2（TR）之间存在明确的因果分工。

#### 4.1 C-TG：粗轨迹生成

C-TG在单模态内独立运行，结合M³输出的一致性概率 $S^k$ 与空间几何约束（SGC）代价 $G^k$ 进行数据关联。SGC代价矩阵定义为：

$$G^{k} = \begin{bmatrix}
G_{1,1}^{k} & G_{1,2}^{k} & \cdots & G_{1,N_{t}^{k}}^{k} \\
G_{2,1}^{k} & G_{2,2}^{k} & \cdots & G_{2,N_{t}^{k}}^{k} \\
\vdots & \vdots & \ddots & \vdots \\
G_{M_{t-1}^{k},1}^{k} & G_{M_{t-1}^{k},2}^{k} & \cdots & G_{M_{t-1}^{k},N_{t}^{k}}^{k}
\end{bmatrix}$$

其中 $G^c$ 为 $1 - \text{2D-IoU}$（相机流），$G^l$ 为3D质心距离（LiDAR流）。通过卡尔曼滤波预测历史位置以补偿帧间位移。

最终关联代价为两者之和，但需满足阈值条件：

$$C_{i,j}^{k} = \begin{cases}
S_{i,j}^{k} + G_{i,j}^{k}, & \text{if } S_{i,j}^{k} \ge \theta_S \text{ or } G_{i,j}^{k} \le \theta_G \\
1000, & \text{otherwise}
\end{cases}$$

当一致性概率满足阈值（$S_{i,j}^{k} \ge \theta_S$）或几何约束满足阈值（$G_{i,j}^{k} \le \theta_G$）时，取两者之和；否则设为极大常数1000以阻断该关联。基于代价矩阵 $C^k$ 使用匈牙利算法求解最优匹配，生成匹配轨迹 $T_t^k$、未匹配检测 $UD_t^k$ 和未匹配轨迹 $UT_t^k$。

#### 4.2 TR：跨模态轨迹精化（核心创新）

TR模块是CrossTracker区别于所有先前方法的关键。其核心在于**识别并转移新出现对象**，以及**恢复被误删的轨迹**，通过三步五类交叉校正操作在相机流与LiDAR流之间双向纠正错误（Fig. 5）：

![[assets/figures/papers/paper_list_l2_https_3d_bk_tudelft_nl_liangliang_publications_html/figures/005_Figure_5.jpg]]
*Figure 5: Five cases of the cross correction in TR. Each camera and LiDAR stream exhibits a trajectory. Solid shapes (squares for camera, cubes for LiDAR) represent detected objects, while dashed shapes indicate missed detections. (a) and (b) identify newly appearing objects from unmatched LiDAR detections in*

![[assets/figures/papers/paper_list_l2_https_3d_bk_tudelft_nl_liangliang_publications_html/figures/010_Figure_5.jpg]]
*Figure 5: ABLATION STUDY RESULTS ON THE KITTI VALIDATION SET FOR THE THREE STEPS WITHIN THE TR MODULE ADDRESSING CASES (A), (B), (C), (D), AND (E) IN FIG. 5. CAMERA-BASED DETECTORS, RRC [27] FOR CARS AND TRACK-RCNN [28] FOR PEDESTRIANS, AND A LIDAR-BASED DETECTOR, POINT-GNN [30] FOR BOTH CARS AND PEDESTRIANS, ARE EMPLOYED IN THE EXPERIMENTS*

**STEP-1（处理case (a)和(b)）**：从 $UD_t^l$（未匹配LiDAR检测）中识别新出现对象。以相机数据为参考验证LiDAR检测的真实性，将确认真实的新对象从相机流转移到LiDAR流轨迹 $T_t^l$ 中，重点减少误检。

**STEP-2（处理case (c)和(d)）**：纠正 $UT_{t-1}^c$（未匹配相机轨迹）或 $UT_{t-1}^l$（未匹配LiDAR轨迹）。当某一模态的轨迹因漏检而中断时，利用另一模态的检测信息恢复该轨迹。例如，若LiDAR轨迹因遮挡而中断，但相机仍能检测到该对象，则用相机检测更新LiDAR轨迹。

**STEP-3（处理case (e)）**：纠正 $UT_{t-1}^c$ 和 $UT_{t-1}^l$ 同时存在的情况。当两模态同时漏检（如远距离小目标）导致轨迹中断时，通过跨模态信息互补尝试恢复。这是最具挑战性的情形，也是先前方法完全无法处理的。

TR模块的因果链条清晰：C-TG输出的未匹配检测和未匹配轨迹是TR的输入；TR通过跨模态验证和转移机制，将单模态无法确定的信息（如新目标真实性、中断轨迹的可恢复性）在两模态间交叉确认，最终输出更完整的LiDAR 3D轨迹。

### 五、训练与推理路径

**训练阶段**：M³模块的分类器使用二元交叉熵损失进行端到端训练。正样本为同一对象的帧间匹配对，负样本为不同对象的帧间匹配对。训练数据从KITTI跟踪序列中采样，包含图像、点云和检测框标注。

**推理阶段**：对每帧依次执行M³特征提取与一致性估计 → C-TG单模态粗关联 → TR跨模态交叉校正。M³模块在推理时辅以SGC（空间几何约束）以增强关联鲁棒性。整个流程保持在线性——仅使用当前帧和历史信息，不访问未来帧。

### 六、关键公式变量含义总结

| 符号 | 含义 |
|------|------|
| $S^k$ | 模态 $k$ 的多模态一致性概率矩阵（M³输出） |
| $G^k$ | 模态 $k$ 的空间几何约束代价矩阵 |
| $C^k$ | 模态 $k$ 的最终数据关联代价矩阵 |
| $F_{img}$ | IFM提取的联合图像特征 |
| $F_{pg}$ | GFM提取的平面几何特征 |
| $F_{pc}$ | PFM提取的点云特征 |
| $\theta_S, \theta_G$ | 一致性概率和几何约束的阈值 |
| $T_t^k, UD_t^k, UT_t^k$ | 时刻 $t$ 模态 $k$ 的匹配轨迹、未匹配检测、未匹配轨迹 |

![[assets/figures/papers/paper_list_l2_https_3d_bk_tudelft_nl_liangliang_publications_html/figures/004_Figure_4.jpg]]
*Figure 4: Overview of M3 module. It takes as input two consecutive frames of the image and point cloud, along with their corresponding detections. It independently outputs the consistency probabilities (similarity scores) of two objects for the camera (Sc) and LiDAR (Sl) scenario*

## 实验与关键发现

CrossTracker 在 KITTI 跟踪基准上进行了系统性验证，覆盖 Car 和 Pedestrian 两个类别。实验围绕三个层次展开：主结果与现有方法的全面对比、M3 多模态建模模块的特征消融、以及 TR 轨迹精化模块的交叉校正有效性验证。

### 主结果：KITTI 测试集上的性能优势

**Table I** 给出了 KITTI 测试集上的核心对比结果。在 Car 类别上，CrossTracker 使用 CasA 作为 LiDAR 检测器、RRC 作为相机检测器时，HOTA 达到 80.87%，较相同检测器组合下的在线 CasTrack（77.32%）提升 **+3.55%**。当替换为更强的检测器组合（VirConv + Perma）时，CrossTracker 的 HOTA 进一步提升至 82.04%，较 CasTrack 的 79.97% 高出 **+2.07%**。在 Pedestrian 类别上，CrossTracker 同样展现出竞争力，但提升幅度小于 Car 类别，这与其在行人小目标上的交叉校正噪声问题一致（见下文失败分析）。

值得注意的是，CrossTracker 在 DetA（检测精度）和 AssA（关联精度）两个子指标上均有提升，表明其两阶段架构不仅改善了轨迹关联质量，也通过交叉校正间接提升了有效检测召回。在 KITTI 测试集的 Car 类别上，CrossTracker 超越了包括 AB3DMOT、EagerMOT、DeepFusionMOT 在内的全部 18 个对比方法。

### 消融实验：M3 模块的特征贡献

M3 模块的核心创新在于将图像特征（IFM）、平面几何特征（GFM）和点云特征（PFM）统一建模，输出对象间的一致性概率。**Table II** 从分类器层面验证了各特征的独立贡献：仅使用图像特征时，分类器 F1 分数为 94.58；加入 GFM 后提升至 96.85（+2.27）；再加入 PFM 后达到 96.90（+0.05）。PFM 带来的边际增益虽小，但在下游 3D MOT 任务中却有关键影响。

**Table III** 进一步将消融推进到端到端跟踪任务。在 Car 类别上，加入点云特征后 HOTA 从 83.47 提升至 83.78（+0.31%）；在 Pedestrian 类别上，AssA 从 50.60 大幅提升至 53.60（+3.00%）。这说明点云几何特征对行人这类图像特征不够鲁棒的小目标尤为关键——点云提供的 3D 结构信息能有效弥补图像模态在遮挡和远距离场景下的不确定性。

### 消融实验：TR 模块的交叉校正机制

TR 模块是 CrossTracker 两阶段架构的核心差异点。**Table IV** 通过逐步叠加五类交叉校正操作，量化了每一类情形的贡献。基线为仅使用 LiDAR 的单阶段跟踪，Car HOTA 为 78.08%。

- **STEP-1**（处理 case a 和 b，从 LiDAR 未匹配检测中识别新出现目标，利用相机数据抑制误检）：HOTA 提升至 80.53%（+2.45%）。
- **STEP-2**（处理 case c 和 d，利用另一模态恢复相机或 LiDAR 流中被误删的轨迹）：HOTA 进一步提升至 81.93%（+1.40%）。
- **STEP-3**（处理 case e，恢复两模态同时漏检的轨迹）：HOTA 达到 83.78%（+1.85%），完整 TR 模块总计贡献 **+5.70%**。

这一递进消融揭示了两个关键洞察：其一，case (e)（两模态同时漏检）单独贡献最大（+1.85%），这正是单阶段方法无法处理的盲区；其二，case (a) 和 (b) 的增益（+2.45%）表明，利用相机信息甄别 LiDAR 误检是提升跟踪鲁棒性的高效手段。在 Pedestrian 类别上，TR 模块同样带来 AssA 的提升，但 DetA 略有下降，暗示交叉校正可能在行人场景中引入少量噪声轨迹。

### 检测器组合的鲁棒性验证

**Table V** 展示了不同相机和 LiDAR 检测器组合下的性能变化。当 LiDAR 检测器从 Point-GNN 替换为更强的 CasA 或 VirConv 时，Car HOTA 从 83.78% 分别提升至 85.37% 和 87.89%。这表明 CrossTracker 的两阶段架构对检测器质量具有正向兼容性——更强的检测输入能通过交叉校正机制进一步放大收益。同时，在不同检测器组合下，CrossTracker 始终优于单阶段基线，验证了架构本身的鲁棒性。

### 失败模式与适用边界

**Fig. 7** 展示了一个典型失败案例：当目标处于视场边界且两个模态同时漏检时，CrossTracker 无法通过交叉校正找回该目标。这是因为交叉校正机制依赖至少一个模态提供有效的检测线索；当两模态同时失效时，TR 模块缺乏可参照的锚点。这一边界条件在极端遮挡或传感器盲区场景下尤为突出。

此外，Pedestrian 类别的 DetA 在 TR 模块介入后出现轻微下降，说明当前交叉校正策略在处理小目标时可能引入误关联。这是因为行人的图像特征和点云特征在远距离下信噪比降低，M3 模块输出的一致性概率可靠性下降，导致 STEP-2 和 STEP-3 中的轨迹恢复操作可能将噪声检测错误地关联到已有轨迹。

当前 CrossTracker 仅支持单相机输入，无法直接处理多相机设置下的跨视角关联，这限制了其在自动驾驶多传感器平台上的直接部署。

## 定位与知识库关联

CrossTracker 的本质贡献在于将多模态 3D MOT 的**跟踪架构 slot** 从“单阶段顺序融合”推进至“两阶段粗到精交叉校正”，并在**跨模态特征关联测度 slot** 和**轨迹精化策略 slot** 上同步引入配套创新。以下从这三个 slot 的变更、与知识库的挂载关系、适用边界及后续启发展开。

### 1. 跟踪架构 slot：从单阶段融合到两阶段粗到精

**基线状态**：以 **EagerMOT**（Kim et al., ICRA 2021）为代表的多模态融合方法采用单阶段架构：先将检测结果按模态来源分类为 LiDAR-相机匹配检测、LiDAR-only 检测和相机-only 检测，再按固定顺序（通常先处理匹配检测，再 LiDAR-only，最后用相机-only 修正 LiDAR 漏检）依次关联。该架构存在一个结构性缺陷——相机流中的跟踪失败无法被反向修正（Fig. 2 中的 case (c) 和 (d)），因为处理流程是单向的。

**CrossTracker 的变更**：将 3D MOT 从单阶段范式重构为两阶段“粗到精”框架（C-TG → TR）。这一设计灵感来源于两阶段检测器（如 Faster R-CNN）中 RPN + 精化头的思想，但将其推广至时序关联任务：第一阶段生成相机和 LiDAR 两个模态的初步轨迹，第二阶段在两条轨迹流之间执行双向交叉校正。这是首次在在线 3D MOT 中引入独立的轨迹精化阶段。

**知识库挂载点**：该 slot 变更可挂载至“多目标跟踪架构设计”节点，与以下工作形成谱系关系：
- 单模态两阶段跟踪：**CasTrack**（在线模式）虽采用“检测-关联-精化”的多步流程，但其精化仅在 LiDAR 单模态内进行，不涉及跨模态交叉校正。
- 多模态融合跟踪：**DeepFusionMOT**（Wang et al., RA-L 2022）使用深度关联网络进行相机-LiDAR 融合，但仍为单阶段架构，无独立精化阶段。
- CrossTracker 的独特位置在于：将两阶段思想与多模态双向校正首次结合，使架构 slot 从“处理流程编排”升级为“错误恢复机制设计”。

### 2. 跨模态特征关联测度 slot：从手工几何约束到端到端多模态建模

**基线状态**：现有方法（EagerMOT 等）主要依赖空间几何约束（Spatial Geometric Constraint, SGC），如 3D-IoU 或质心距离，作为跨模态关联的测度。这些手工设计的度量在目标外观相似、部分遮挡或检测噪声较大时区分力不足。

**CrossTracker 的变更**：提出 **M³ 模块**——首个将图像特征建模（IFM）、平面几何特征建模（GFM）和点云特征建模（PFM）统一纳入端到端网络的跨模态一致性估计器。M³ 输出的一致性概率矩阵 $S^k$ 直接反映两个对象属于同一目标的置信度，与 SGC 矩阵 $G^k$ 联合构成关联代价 $C^k$。其中 GFM 通过将 2D 检测框转化为伪点云块并经 PointNet 编码，桥接了图像域与点云域的几何表示。

**知识库挂载点**：
- **特征融合层面**：M³ 可挂载至“多模态特征融合”节点，与使用图像+点云双流网络的目标检测融合方法（如 MVX-Net、PointPainting）共享“图像特征提升点云表示”的思路，但 M³ 的目标是输出对象间的一致性概率而非检测分数。
- **关联测度层面**：可挂载至“数据关联度量学习”节点。传统方法使用手工距离（马氏距离、IoU），深度关联方法（如 DeepSORT 的外观特征）通常在单模态内学习。M³ 的独特性在于跨模态学习“两个不同模态检测是否指向同一目标”的二分类能力。

### 3. 轨迹精化策略 slot：从单向修正到五类交叉校正

**基线状态**：EagerMOT 等方法的“精化”仅体现为用相机-only 检测补充 LiDAR 漏检，是单向的、被动的补偿操作，无法处理相机流自身的漏检或两模态同时漏检。

**CrossTracker 的变更**：TR 模块定义了 5 类交叉校正操作（Fig. 5 的 case (a)-(e)），分三步执行：
- **STEP-1**：处理 case (a) 和 (b)，利用相机数据作为参考，从 LiDAR 未匹配检测中识别新出现目标，抑制 LiDAR 误检。
- **STEP-2**：处理 case (c) 和 (d)，用另一模态的检测恢复本模态中被误删的轨迹（相机流或 LiDAR 流）。
- **STEP-3**：处理 case (e)，当两模态同时漏检时，通过跨模态轨迹匹配恢复目标。

这五类操作覆盖了多模态跟踪中所有可能的检测失败组合（Fig. 2），使交叉校正从单向补偿升级为双向、系统化的错误恢复机制。

**知识库挂载点**：该 slot 可挂载至“轨迹管理”与“跟踪失败恢复”节点。与单模态跟踪中的“轨迹重生”（track rebirth）机制相比，CrossTracker 的创新在于利用跨模态冗余信息触发重生，而非依赖盲目的候选区域搜索或长时间窗口。

### 4. 适用边界与局限

- **单相机限制**：当前 CrossTracker 仅支持单相机输入，无法直接处理多相机设置（如 nuScenes 的 6 相机环视），这是向更复杂场景扩展的主要障碍。
- **视场边界失效**：当两模态同时在视场边界漏检时（Fig. 7），交叉校正缺乏任何可用的参考信息，系统退化为单模态跟踪的下限。
- **小目标噪声**：TR 模块在交叉校正行人（Pedestrian）时可能引入噪声，表现为 AssA 提升但 DetA 轻微下降（Table IV），说明小目标的跨模态一致性估计仍有不确定性。
- **检测器依赖**：作为基于检测的跟踪范式，CrossTracker 的性能上限受检测器质量约束（Table V 显示更换检测器可带来约 4% HOTA 差异），但其两阶段架构对检测器质量波动的鲁棒性优于单阶段方法。

### 5. 后续启发与开放问题

1. **多相机扩展**：将 CrossTracker 扩展至多相机设置需要解决跨相机目标关联与 M³ 模块的多视图特征融合问题，这是从 KITTI 向 nuScenes/Waymo 迁移的关键。
2. **端到端化**：当前 M³ 模块与跟踪器是分离训练的，将整个两阶段流程端到端优化可能进一步提升一致性估计与关联决策的协同性。
3. **小目标精化**：针对行人等小目标在 TR 模块中的噪声问题，可探索尺度感知的交叉校正阈值或不确定性建模。
4. **知识库定位**：CrossTracker 在知识库中的核心定位是“在线多模态 3D MOT 的两阶段交叉校正框架”，其 M³ 模块和 TR 模块分别贡献了“跨模态一致性学习”和“系统化错误恢复”两个可复用的设计模式。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/HRBF_Fusion_Accurate_3D_Reconstruction_From_RGB_D_Data_Using_On_the_fly_Implicits.pdf]]