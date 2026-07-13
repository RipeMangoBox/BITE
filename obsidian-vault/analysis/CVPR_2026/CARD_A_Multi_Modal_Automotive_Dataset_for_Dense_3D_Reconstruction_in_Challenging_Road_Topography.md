---
title: "CARD: A Multi-Modal Automotive Dataset for Dense 3D Reconstruction in Challenging Road Topography"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CARD_A_Multi_Modal_Automotive_Dataset_for_Dense_3D_Reconstruction_in_Challenging_Road_Topography.pdf
project_link: "https://card.content.cariad.digital"
code_link: "https://huggingface.co/CARD-Data"
aliases:
- CARD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过多LiDAR融合、自适应多视图投票、动态修剪和体素清理等流程，为前视图像提供每帧约500K的准密集深度真值，并标注正负地形不规则区域，使得能够直接在二维图像空间中对道路表面几何进行细粒度评估。
primary_logic: CARD有针对性地填补了现有驾驶数据集在道路地形三维几何上的空白，利用双LiDAR融合实现远超现有公共数据集的深度真值密度，同时引入基于车轮接触点的道路相对高度表示和面向地形不规则性的评估协议，为挑战性路面条件下的深度估计与补全设立了更为严格且贴近安全的基准。
claims:
- CARD 每帧提供约 500K 有效深度像素，是 KITTI Depth Completion 的 6.5 倍以上，是其他公开驾驶数据集平均数的 10 倍以上。
- 零样本单目深度估计模型在道路表面不平整区域表现显著下降，而基础立体模型 FoundationStereo 在限定框内误差更低。
- 通过自适应多视图投票和体素清理、动态物体过滤，CARD 的真值管道能够抑制动态点并保留静态道路几何。
- CARD 提供道路地形相对高度的计算方案，将深度转换为相对于路面的高度，可用于分析减速带、坑洼等几何细节。
---

# CARD: A Multi-Modal Automotive Dataset for Dense 3D Reconstruction in Challenging Road Topography

> [!tip] 核心洞察
> CARD有针对性地填补了现有驾驶数据集在道路地形三维几何上的空白，利用双LiDAR融合实现远超现有公共数据集的深度真值密度，同时引入基于车轮接触点的道路相对高度表示和面向地形不规则性的评估协议，为挑战性路面条件下的深度估计与补全设立了更为严格且贴近安全的基准。

| 字段 | 内容 |
|------|------|
| 中文题名 | CARD：面向挑战性道路地形的多模态密集三维重建数据集 |
| 英文题名 | CARD: A Multi-Modal Automotive Dataset for Dense 3D Reconstruction in Challenging Road Topography |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Elazab_CARD_A_Multi-Modal_Automotive_Dataset_for_Dense_3D_Reconstruction_in_CVPR_2026_paper.html) · [Project](https://card.content.cariad.digital) · [HuggingFace](https://huggingface.co/CARD-Data) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | CARD |
| Dataset | CARD benchmark, Depth Completion on CARD |

> [!tip] 效果简介
> - CARD benchmark 上，AbsRel (F/B) MoGe2L†: 0.013 (F)/0.027 (B) vs Depth Anything V2: 0.021 (F)/0.041 (B) (Bounding-box AbsRel 降低 34% (0.041->0.027))；Height AbsDiff (B) MoGe2L†: 0.034 vs MoGe2L: 0.051 (降低 0.017)；RMSE (B) FoundationStereo: 0.185 vs MoGe2L: 0.369 (降低 49.8%)。
> - Depth Completion on CARD 上，RMSE (F/B) DMD3C (+FS): 0.7510/0.1918 vs BP-NET: 0.7975/0.1939 (Full-image RMSE 降低 0.0465)；iMAE (F/B) BP-NET: 0.0044/0.0028 vs DMD3C: 0.0050/0.0028 (Full-image iMAE 基准最优)。

## 概要

现有自动驾驶数据集长期聚焦于铺设良好的平坦道路，对坑洼、减速带、崎岖路面、非铺装路面等挑战性道路地形的覆盖严重不足，且缺乏面向道路表面几何的细粒度深度标注与评估协议。这一空白使得深度估计、深度补全等感知模型在非理想路面条件下的行为几乎不可知，直接制约了下游安全相关应用的可靠性。

CARD（CVPR 2026）针对上述瓶颈，构建了首个大规模多模态驾驶数据集，专门面向挑战性道路地形的密集三维重建。其核心贡献体现在三个层面：

1. **准密集深度真值**：通过前-后双LiDAR融合、自适应多视图投票、动态修剪与体素清理等流水线，每帧前视图像提供约 **500K 有效深度像素**，约为 KITTI Depth Completion 的 6.5 倍、其他公开驾驶数据集平均值的 10 倍以上。
2. **道路地形标注与相对高度表示**：引入正地形（凸起，如减速带）和负地形（凹陷，如坑洼）的 2D 边界框标注，并利用车轮接地轨迹将深度转换为相对于路面的高度，使模型能够在二维图像空间中直接评估路面起伏。
3. **面向地形不规则性的评估协议**：在传统全图指标之外，增设限定于地形标注框内的 per-box 评估，更严格地衡量模型对安全关键区域的几何重建能力。

实验揭示了一个关键发现：零样本单目深度估计模型在全图指标上表现强劲，但在道路表面不平整区域性能显著下降；而立体基线 **FoundationStereo**（Wen et al., CVPR 2025）在限定框内的误差大幅低于最优单目模型。在深度补全任务上，结合 FoundationStereo 作为教师信号的 **DMD3C+FS** 变体在 box 级 RMSE 上取得最优。

CARD 数据集覆盖德国和意大利约 110 km、4.7 小时的驾驶数据，按地理位置和地形类别分层划分训练/验证/测试集，代码与数据已开源。



### 核心瓶颈：现有驾驶数据集忽视道路表面三维几何

当前自动驾驶数据集（如KITTI、Waymo、nuScenes等）主要聚焦于平坦、铺设良好的城市道路，在数据采集上存在一个关键的结构性缺失：**缺乏对挑战性道路地形的大规模、多样化真实覆盖与准密集深度标注**。具体而言，坑洼、减速带、崎岖路面、非铺装路面等“非理想”道路表面，在现有数据集中要么完全缺失，要么覆盖极为稀疏（见Table 1）。这一空白导致两个直接后果：

1. **评估盲区**：现有的深度估计与补全基准无法衡量模型在道路不规则区域的几何重建能力，而这些区域恰恰是安全关键场景。
2. **训练偏差**：模型在平坦道路数据上训练后，对路面起伏的感知能力缺乏有效监督信号，难以泛化至真实世界中常见的路面缺陷。

### 因果机制：深度真值密度决定道路几何评估的粒度

评估道路表面几何的关键在于深度真值的**空间密度**。现有公共数据集的深度真值密度普遍不足——KITTI Depth Completion（KITTI-DC）每帧约75K有效点，其他数据集平均低于50K点。这一密度水平足以评估场景级深度，但**远不足以刻画厘米级的路面起伏**（如减速带的高度轮廓、坑洼的边缘形态）。

CARD通过双LiDAR融合流水线，将有效深度像素提升至每帧约500K（约18%图像前景覆盖率），约为KITTI-DC的6.5倍、其他数据集的10倍以上。这一密度跃升使得直接在二维图像空间中对道路表面几何进行细粒度评估成为可能。

### 核心洞察：从“场景深度”到“路面相对高度”的范式转换

CARD的关键洞察在于将评估焦点从通用场景深度转向**道路地形相对高度**。传统深度估计以相机坐标系为参考，无法区分“远处平坦路面”与“近处起伏路面”在安全意义上的本质差异。CARD通过以下创新实现了范式转换：

- **车轮接地轨迹**：利用车辆四轮与路面的连续接触点轨迹，结合车辆位姿，将深度值转换为相对于路面的高度。这一表示直接对应车辆悬架系统的物理激励，具有明确的安全含义。
- **地形不规则标注**：引入2D边界框标注，区分positive（凸起，如减速带）和negative（凹陷，如坑洼）地形，并设计per-box评估协议，仅在不规则区域内衡量模型性能。
- **传感器-路面全标定**：通过Leica测量设备建立传感器到四轮中心及车轮接地点的完整变换链，确保相对高度计算的物理一致性。

### 动机总结

CARD的动机根植于一个简单但被长期忽视的事实：**自动驾驶车辆不仅需要在平坦道路上感知障碍物，更需要在路面本身成为“障碍物”时精确理解其几何形态**。现有数据集和基准无法回答“模型能否准确感知前方减速带的高度”或“能否区分坑洼深度以决定是否减速”这类安全关键问题。CARD通过准密集深度真值、路面相对高度表示和地形不规则评估协议，为这一空白提供了系统性的解决方案。



## 核心方法与创新机理

CARD 的核心创新并非提出新的深度学习模型，而是系统性地填补了现有驾驶数据集在**挑战性道路地形三维几何**上的空白。其创新围绕三个紧密耦合的“changed slots”展开，形成一条从数据采集到评估协议的完整链条。

### 1. 准密集深度真值：从稀疏采样到道路几何的密集覆盖

现有驾驶数据集的深度真值密度严重不足：KITTI Depth Completion 每帧仅约 75K 点，其他公开数据集平均不足 50K 点。这种稀疏性使得对道路表面细微几何（如坑洼、减速带）的评估几乎不可能。

CARD 通过**双 LiDAR 融合与自适应多视图投票**流水线，将每帧有效深度像素提升至约 500K（约占图像前景的 18%），是 KITTI-DC 的 6.5 倍以上、其他公开数据集平均值的 10 倍以上。这一密度的跃升并非简单的数据堆砌，而是通过以下关键设计实现的：

- **体素累积与动态过滤**：将多次 LiDAR 扫描累积到体素中，利用中位数绝对偏差（MAD）滤波剔除离群点，再通过 ICP 流残差剔除动态物体残留，确保真值严格来自静态道路几何。
- **自适应多视图投票**：根据 LiDAR 间基线距离动态调整投票阈值——前向 LiDAR 所需投票数从基线 0.20 m 时的 4 票降至 0.90 m 时的 1 票，后向 LiDAR 相应从 2 票降至 1 票。消融实验（Figure 6）显示，去除该策略会导致近处道路细节丢失或远处噪声增加。

这一密度优势使得深度估计与补全模型能够在道路不规则区域接受更严格的细粒度评估，而非仅在平坦路面上报告全局指标。

### 2. 道路地形标注与相对高度表示：从通用深度到路面几何

传统数据集的深度真值仅定义在相机坐标系下，无法直接反映路面起伏。CARD 引入了两个互补的表示：

- **道路地形 2D 边界框标注**：区分 *positive*（凸起，如减速带）和 *negative*（凹陷，如坑洼）两类不规则地形。标注采用半自动流程——40% 手工标注子集训练 YOLOv8 模型，辅助完成剩余 60% 的标注。
- **路面相对高度表示**：利用四轮接地点的连续轨迹（wheel excitation），将相机坐标系深度转换为相对于路面的高度。这一变换使得对减速带高度、坑洼深度等几何细节的定量分析成为可能。

这两个表示共同支撑了 CARD 的核心评估协议：**限定框内（bounding-box restricted）评估**。实验表明，零样本单目深度估计模型在全局深度指标上表现强劲，但在道路表面不平整区域的限定框内表现显著下降——例如 Depth Anything V2 的限定框 AbsRel 为 0.041，而经过 CARD 微调的 MoGe2L† 降至 0.027，降幅达 34%（Table 3）。这揭示了现有模型在道路地形几何上的系统性弱点，而传统全局指标无法捕捉这一缺陷。

### 3. 传感器-路面标定：从粗略外参到车轮接地级精度

CARD 的传感器标定超越了常规的传感器间外参标定，通过 Leica 测量设备对四个车轮中心及车轮接地点进行精确测量，构建了从传感器到车轮接地点的完整变换链。这一标定是路面相对高度计算的基础，也是 CARD 区别于其他数据集的关键工程创新——它将深度评估从“相机看到了什么”推进到“路面实际几何如何”。



CARD 的真值生成与评估框架围绕一个核心目标构建：**在挑战性道路地形条件下，为前视图像提供高密度、高精度的深度真值，并建立面向路面不规则性的评估协议**。整个流水线可分解为六个紧密耦合的模块，形成从原始传感器数据到可评估深度图的完整链路。

### 1. 传感器标定与位姿估计

流水线的输入层由双 LiDAR（前/后）、立体相机和 IMU 构成（见 Table 2 和 Figure 3）。所有传感器在每次采集日进行三次联合标定（开始、中间、结束），使用标定板和 Leica 测量仪器建立传感器间外参及传感器到车辆坐标系的变换。特别地，Leica 仪器还测量四个车轮中心及车轮接地点的位置，为后续路面相对高度计算提供关键变换链。轨迹层面，采用 **MC2SLAM** 作为紧耦合 LiDAR-惯性里程计进行在线估计，随后通过离线批量优化融合全部 IMU 预积分和回环约束，生成全局一致的 6-DoF 位姿序列。

![[assets/figures/papers/paper_list_l815_https_openaccess_thecvf_com_content_CVPR2026_html_Elazab_CARD_A_Multi_Mo/figures/005_Figure_3.jpg]]
*Figure 3: Rig visualization with sensor locations. Values are approximated and intended only to illustrate the setup. Legend: L1: front LiDAR, L2: rear LiDAR, and hc: left-camera height*

### 2. 多 LiDAR 体素累积

利用批量优化后的高精度位姿，将多次 LiDAR 扫描的运动补偿点云累积到体素网格中。这一步骤的目标是在保持真值严格来源于 LiDAR 实测的前提下，显著提升场景表示的密度。双 LiDAR 的冗余配置使得每帧图像可投影约 **500K 有效深度像素**，约为 KITTI Depth Completion 的 6.5 倍，是其他公开驾驶数据集平均值的 10 倍以上。

### 3. 动态物体过滤

累积体素中不可避免地混入动态物体（车辆、行人等）的回波。CARD 采用三级过滤策略：

- **自适应多视图投票**：根据体素到 LiDAR 的基线距离动态调整所需投票数。前 LiDAR 在基线 0.20 m 时需 4 票，到 0.90 m 时降至 1 票；后 LiDAR 从 2 票降至 1 票。这一机制在保留近处道路细节的同时有效抑制远处噪声。
- **ICP 流动态修剪**：对相邻扫描对计算 ICP 残差，当残差超过 0.10 m 时记为“移动票”，体素累积 ≥2 张移动票则标记为动态并剔除。
- **MAD 体素清理**：对体素内点云计算中位数绝对偏差（MAD），保留满足 $| \boldsymbol{r}_i - \tilde{\boldsymbol{r}} | \leq 1.5 \cdot \text{MAD}$ 的点；若剩余点数不足 2 则丢弃整个体素。

Figure 6 的定性消融表明，缺少体素清理会导致动态点错误注册到静态道路体素中，产生明显的运动伪影；而放弃自适应投票改用单一共识则会损失近处道路细节。

### 4. 遮挡剔除与图像投影

以左相机光心为视点，应用 Open3D 的 Hidden Point Removal 算法剔除被遮挡的三维点，随后将过滤后的静态点云投影到图像平面，生成最终的准密集深度图。为进一步抑制残留动态点，投影后计算每个 LiDAR 点的绝对相对误差，移除超过 15% 误差的点。

### 5. 路面相对高度表示

CARD 引入**车轮激励**概念——每个轮胎接地点在世界坐标系中的连续轨迹时间序列 $[t, x, y, z, q_w, q_x, q_y, q_z]$。结合车辆位姿，将相机坐标系下的深度值转换为相对于路面的高度。这一表示使得减速带（正地形）和坑洼（负地形）的几何起伏可直接在二维图像空间中量化和可视化（见 Figure 1 底部）。

### 6. 道路地形标注与评估协议

标注管线采用半自动化流程：40% 的数据手工标注正/负地形边界框，用于训练 YOLOv8 模型，再由模型辅助完成剩余 60% 的标注。评估时引入 **per-box 协议**，仅在标注框内计算深度误差指标，从而将评估焦点对准路面不规则区域。所有深度评估限制在 80 m 范围内，单目模型统一采用 per-image median scaling 以保证相对几何比较的公平性。

### 输入输出流总结

```
传感器原始数据（LiDAR/相机/IMU）
    │
    ▼
标定与位姿估计（MC2SLAM + 批量优化）
    │
    ▼
多 LiDAR 体素累积 → 动态过滤（自适应投票 + ICP 修剪 + MAD 清理）
    │
    ▼
遮挡剔除 → 图像空间投影 → 准密集深度图（~500K 点/帧）
    │
    ├── 深度评估（全图 / 框内）
    │
    └── 车轮激励 → 路面相对高度 → 地形不规则性分析
```

该框架的核心优势在于：通过双 LiDAR 冗余和自适应投票机制实现了远超现有数据集的真值密度；通过三级动态过滤保证了静态道路几何的纯度；通过路面相对高度表示和 per-box 评估协议，将评估焦点从全局深度误差转移到对安全至关重要的道路表面不规则性上。

### 补充图表

![[assets/figures/papers/paper_list_l815_https_openaccess_thecvf_com_content_CVPR2026_html_Elazab_CARD_A_Multi_Mo/figures/007_Figure_5.jpg]]
*Figure 5: Ground truth generation: motion-compensated LiDAR bursts are voxel-accumulated, dynamic-object filtered, then projected to the left camera to yield dense per-image GT, as explained in Sec. 3.4*



CARD 的真值生成流水线由七个关键模块串联构成，其核心目标是将多 LiDAR 扫描累积为稠密静态场景表示，再投影至前视相机图像空间，获得每帧约 500K 的有效深度像素。以下按处理顺序解析各模块的功能与机理。

### 3.1 多传感器位姿估计与全局优化

精确的传感器 6-DoF 位姿是所有后续点云拼接与投影的基础。CARD 采用两阶段策略：

- **第一阶段**：运行 **MC2SLAM**（NeBMO et al.）作为紧耦合 LiDAR-惯性里程计，实时估计每帧 LiDAR 扫描的初始位姿。
- **第二阶段**：离线批处理优化，利用全部 IMU 测量值、第一阶段里程计约束和回环检测约束，对完整轨迹进行全局精化，消除累积漂移。

这一设计确保了在长距离（约 110 km）、多路段采集条件下，所有传感器位姿具有全局一致性。

### 3.2 体素化多 LiDAR 点云累积

在获得各帧 LiDAR 扫描的精确位姿后，将多次扫描（burst）累积到统一的体素网格中。该步骤的动机是：**在保持真值严格来自 LiDAR 实测的前提下，通过多帧叠加获得稠密得多的场景表示**。体素化累积是后续自适应投票和动态过滤的空间基础。

### 3.3 自适应多视图投票

为抑制 LiDAR 噪声并保留可靠的静态点，CARD 引入 **基线依赖的自适应投票机制**。其核心思想是：近距离物体在前后 LiDAR 中的视差大，需要更多视图一致性来确认；远距离物体视差小，降低投票阈值以避免过度滤除。

具体规则如下（以基线长度 $b$ 为自变量）：
- 前向 LiDAR 所需投票数：随 $b$ 从 0.20 m 增至 0.90 m，投票数从 4 递减至 1。
- 后向 LiDAR 所需投票数：在相同基线范围内从 2 递减至 1。

这种策略比单一共识阈值（Fig. 6 右）更能保留近处道路细节，同时有效抑制远处噪声。

![[assets/figures/papers/paper_list_l815_https_openaccess_thecvf_com_content_CVPR2026_html_Elazab_CARD_A_Multi_Mo/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative ablation of voxel cleaning and adaptive voting. Left: projected depth without voxel cleaning, clearly showing dynamic points registered into static road voxels. Right: projected depth with our pipeline using a single consensus across both Li-DARs, without the adaptive voting strategy*

### 3.4 动态物体过滤：ICP 流与体素清理

动态物体（车辆、行人等）在点云累积中会留下运动伪影，严重污染道路几何真值。CARD 采用两层过滤：

1. **ICP 流动态修剪**：对相邻扫描对计算 ICP 残差。若某体素的残差超过 0.10 m，则计为一次“移动投票”；累计获得至少 2 次移动投票的体素被标记为动态并剔除。
2. **体素清理（MAD 滤波）**：对每个体素内的点，计算其到体素中心的径向距离 $\boldsymbol{r}_i$，以中位数绝对偏差进行离群值修剪：

   $$MAD = \text{median} \left( \left| \boldsymbol { r } _ { i } - \tilde { \boldsymbol { r } } \right| \right)$$

   保留满足 $| \boldsymbol{r}_i - \tilde{\boldsymbol{r}} | \leq 1.5 \cdot MAD$ 的点；若体素内剩余点数少于 2，则丢弃该体素。

消融实验（Fig. 6 左）表明，无体素清理时动态点会错误地注册到静态道路体素中，在深度图上产生明显的运动伪影。

### 3.5 遮挡剔除与图像空间投影

经上述处理后的静态点云以左相机中心为视点，应用 Open3D 中的 Hidden Point Removal 算法剔除被遮挡点。随后将剩余点投影到左相机图像平面，生成最终的准密集深度图。为进一步剔除残留的动态点，对每个投影点计算绝对相对误差，移除误差超过 15% 的点。

### 3.6 车轮激励提取与路面相对高度

CARD 的一项独特贡献是将深度值转换为 **相对于路面的高度**，从而直接刻画路面起伏。其实现依赖于 **车轮激励** 概念：

> 车轮激励定义为每个轮胎接地点的世界坐标系轨迹。

采集车配备了完整的标定链：Leica 测量仪器对四轮中心及车轮接地点进行测量，建立传感器到车辆、车辆到车轮接地点的变换关系。结合车辆位姿，即可获得每个时间戳下车轮接地点的位置与姿态：

$$[ t , x , y , z , q _ { w } , q _ { x } , q _ { y } , q _ { z } ]$$

利用该连续轨迹，将相机坐标系下的深度值转换为相对于路面的高度值，使得减速带（凸起）和坑洼（凹陷）等道路地形不规则性可直接在二维图像空间中量化和评估。

### 3.7 半自动道路地形标注

为支持面向道路地形的定向评估，CARD 提供了 2D 边界框标注，区分：
- **Positive**：凸起地形（如减速带）
- **Negative**：凹陷地形（如坑洼）
- **Off-road**：非铺装路面

标注流程采用人机协作：40% 的数据由人工标注，用于训练 YOLOv8 模型；剩余 60% 由模型辅助标注后人工校验。这种半自动方案在保证标注质量的同时显著降低了人工成本。

---

**公式符号速查**：
- $b$：前后 LiDAR 间的基线长度
- $\boldsymbol{r}_i$：体素内第 $i$ 个点到体素中心的径向距离
- $\tilde{\boldsymbol{r}}$：体素内所有点径向距离的中位数
- $MAD$：中位数绝对偏差，用于体素级离群值检测



## 实验与关键发现

### 基准任务与评估协议

CARD 围绕两个核心任务构建基准：**单目/立体深度估计**与**深度补全**。评估在 80 m 范围内进行，同时引入两种互补的评估区域——全图 (F) 与道路地形不规则边界框限定区域 (B)，后者专门衡量模型在坑洼、减速带等安全关键地形上的表现。所有单目模型评估均采用 per-image median scaling，以公平比较相对几何结构，而非绝对尺度。

道路地形评估的关键创新在于**路面相对高度表示**：利用车轮接地点的连续轨迹与车辆位姿，将深度值转换为相对于路面的高度，从而直接量化模型对路面起伏的感知能力。这一表示使评估从“场景几何”下沉到“道路表面几何”，更贴近行车安全需求。

### 深度估计基准结果

Table 3 汇总了单目与立体深度估计的主要结果。零样本单目模型在全局深度指标上表现强劲，但在道路表面不规则区域（B 区）显著退化：

![[assets/figures/papers/paper_list_l815_https_openaccess_thecvf_com_content_CVPR2026_html_Elazab_CARD_A_Multi_Mo/figures/010_Table_3.jpg]]
*Table 3: CARD benchmark for monocular and stereo depth estimation. All results employ per-image median scaling to evaluate relative geometry. (F) and (B) denote full-image and bounding-box restricted evaluations, respectively. The top rows evaluate monocular models in a zero-shot setting, followed by MoGe2L† fine-tuned on CARD. The final row presents the FoundationStereo [52] zero-shot stereo baseline. A comprehensive analysis is provided in the Supplementary Material*

- **Depth Anything V2** (Yang et al., NeurIPS 2024)：全图 AbsRel 0.021，B 区 AbsRel 0.041——不规则区域误差几乎翻倍。
- **UniDepthV2** (Piccinelli et al., 2025)：B 区 AbsRel 0.051，RMSE 0.428，高度绝对差 (Height AbsDiff) 0.055。
- **MoGe2** (Wang et al., 2025)：B 区 AbsRel 0.050，RMSE 0.425。

这些结果表明，现有零样本单目模型虽然在标准场景中表现良好，但**缺乏对路面微几何的细粒度感知能力**，这正是 CARD 基准的核心诊断价值。

**FoundationStereo** (Wen et al., CVPR 2025) 作为零样本立体基线，在 B 区表现出显著优势：RMSE 0.185，较最优单目模型 MoGe2L (RMSE 0.369) 降低 49.8%。立体匹配提供的显式几何约束使其在路面不规则区域具有更强的结构恢复能力。

经 CARD 微调的 **MoGe2L†** 取得最优单目结果：B 区 AbsRel 0.027（较 Depth Anything V2 降低 34%），Height AbsDiff 0.034（较未微调版降低 0.017）。这验证了 CARD 的准密集真值对单目模型微调的有效性。

Figure 8 展示了坑洼区域的高度预测定性对比：UniDepthV2 几乎无法恢复凹陷结构，而 FoundationStereo 能较好地保留坑洼的几何形态，与定量结果一致。

![[assets/figures/papers/paper_list_l815_https_openaccess_thecvf_com_content_CVPR2026_html_Elazab_CARD_A_Multi_Mo/figures/011_Figure_8.jpg]]
*Figure 8: Height ground truth and predictions for a pothole: GT (left), UniDepthV2 [39], FoundationStereo [52] (right)*

### 深度补全基准结果

Table 4 报告了深度补全任务的评估结果。CARD 提供约 500K 有效深度像素作为稀疏输入，远超 KITTI-DC (~75K) 等现有数据集，为深度补全模型提供了更丰富的几何先验。

![[assets/figures/papers/paper_list_l815_https_openaccess_thecvf_com_content_CVPR2026_html_Elazab_CARD_A_Multi_Mo/figures/012_Table_4.jpg]]
*Table 4: Evaluation results on depth completion task*

- **BP-NET** (Tang et al., CVPR 2024) 在全图 iMAE 上取得最优 (0.0044/0.0028)，表明其在整体深度结构恢复上的优势。
- **DMD3C** (Liang et al., CVPR 2025) 在全图 RMSE 上为 0.7975/0.1939。
- **DMD3C+FS** 变体将单目教师替换为 FoundationStereo 并将损失函数切换为直接 L1 损失后，全图 RMSE 降至 0.7510/0.1918，B 区 RMSE 也有改善，表明立体教师信号对补全任务中道路地形细节的恢复具有增益。

值得注意的是，深度补全模型在 B 区的性能退化幅度普遍小于单目深度估计模型，因为稀疏 LiDAR 输入已经为路面区域提供了直接几何约束。

### 真值管道消融

Figure 6 展示了真值生成管道中两个关键模块的定性消融：

1. **体素清理 (Voxel Cleaning)**：未经过 MAD 滤波的深度投影中，动态物体（车辆、行人）的点云被错误地注册到静态道路体素中，形成明显的运动伪影。启用体素清理后，这些动态残留被有效剔除，道路表面深度图变得干净。

2. **自适应多视图投票 (Adaptive Voting)**：若将前后 LiDAR 的投票策略替换为单一共识阈值，近处道路细节（如路面纹理、微小起伏）会丢失，而远处噪声反而增加。自适应投票通过基线依赖的阈值（前 LiDAR 在 0.20–0.90 m 基线范围内投票数从 4 降至 1，后 LiDAR 从 2 降至 1），在近处保留细节与远处抑制噪声之间取得平衡。

### 与其他数据集的深度密度对比

Figure 2 和 Figure 7 定量和定性地展示了 CARD 的深度真值密度优势：

![[assets/figures/papers/paper_list_l815_https_openaccess_thecvf_com_content_CVPR2026_html_Elazab_CARD_A_Multi_Mo/figures/003_Figure_2.jpg]]
*Figure 2: Ground truth points per image. CARD has more depth points per image than KITTI-DC [16, 47] and DrivingStereo [57]*

![[assets/figures/papers/paper_list_l815_https_openaccess_thecvf_com_content_CVPR2026_html_Elazab_CARD_A_Multi_Mo/figures/009_Figure_7.jpg]]
*Figure 7: Colored point cloud comparison. We show CARD alongside densified ground truth from KITTI-DC [16, 47] and RSRD [62], and LiDAR based ground truth from A2D2 [17], Waymo [44], and DDAD [19]. Each panel shows the input image at top left and the point cloud count in bottom left, and only the KITTI-DC panel includes a zoom-in illustrating distortions from dynamic objects [16, 47]*

- CARD 每帧约 500K 有效深度像素，是 KITTI-DC 的 6.5 倍，是其他公开驾驶数据集平均值的 10 倍以上。
- 与 KITTI-DC、RSRD 的稠密化真值以及 A2D2、Waymo、DDAD 的 LiDAR 真值相比，CARD 在道路表面区域的点云覆盖更为均匀和密集，且不依赖多帧累积或插值带来的运动失真。

### 失败模式与局限

1. **远距离稀疏性**：尽管 CARD 提供了准密集真值，80 m 以外的深度点仍然稀疏，评估限制在 80 m 内部分掩盖了这一局限。
2. **小物体残留误差**：动态过滤依赖 ICP 残差和体素清理，对于缓慢移动或与静态场景几何相似的小物体（如停放的自行车），可能仍有少量误保留。
3. **匿名化影响**：为满足 GDPR 要求，图像中的人脸和车牌经过匿名化处理，可能影响依赖这些特征的感知模型在 CARD 上的训练效果。
4. **地形标注粒度**：当前道路地形标注仅为 2D 边界框，无法提供逐像素的语义分割或 3D 实例级几何模型，限制了更细粒度评估的可能性。

### 补充图表

![[assets/figures/papers/paper_list_l815_https_openaccess_thecvf_com_content_CVPR2026_html_Elazab_CARD_A_Multi_Mo/figures/002_Table_1.jpg]]
*Table 1: Datasets comparison. Entries marked with * indicate values we averaged over subsamples of the respective datasets. Abbreviations: OR=off-road, SP=speed bumps/potholes, UE=uneven roads, Urban=city scenes. L denotes low or not explicitly reported*

![[assets/figures/papers/paper_list_l815_https_openaccess_thecvf_com_content_CVPR2026_html_Elazab_CARD_A_Multi_Mo/figures/006_Figure_4.jpg]]
*Figure 4: (a) Image-level distribution of road-topography labels: positive, such as speed bumps, negative, such as potholes, and offroad, such as non-asphalt cases. (b) Sequence-level statistics: a sequence is marked irregular if it contains at least one positive or negative instance. Example frames above, such as left: off-road, middle: negative, right: positive*

![[assets/figures/papers/paper_list_l815_https_openaccess_thecvf_com_content_CVPR2026_html_Elazab_CARD_A_Multi_Mo/figures/001_Figure_1.jpg]]
*Figure 1: CARD example from Carmiano, Italy. Right: map with annotated positive irregularities (speed bumps) and negative irregularities (potholes) along the driven routes, with one speed bump highlighted. Left: camera image with depth ground truth projected into the image (top) and height relative to the road (bottom)*

![[assets/figures/papers/paper_list_l815_https_openaccess_thecvf_com_content_CVPR2026_html_Elazab_CARD_A_Multi_Mo/figures/004_Table_2.jpg]]
*Table 2: Perception sensor specifications for CARD*



## 定位与知识库关联

### 问题定位：现有驾驶数据集的“平坦化”盲区

CARD 的核心动机源于一个被长期忽视的瓶颈：现有自动驾驶数据集——包括 KITTI、Waymo、nuScenes 等——几乎全部采集自铺设良好的平坦道路，对坑洼、减速带、崎岖路面和非铺装路面等挑战性地形缺乏大规模、多样化的真实覆盖。这一“平坦化”偏差导致两个连锁后果：其一，深度估计与补全模型在非理想路面上的表现缺乏有效基准；其二，道路表面几何的细粒度感知——直接影响悬挂控制、紧急避障和安全规划——无法在二维图像空间中直接评估。CARD 正是围绕这一空白，构建了从数据采集、真值生成到评估协议的完整链条。

### 真值生成管线：从多 LiDAR 融合到图像空间投影

CARD 的真值密度优势并非来自更高线数的单一传感器，而是通过一套精心设计的后处理管线实现的。该管线的关键模块及其设计逻辑如下：

- **位姿估计与批量优化**：以 MC2SLAM 作为紧耦合 LiDAR-惯性里程计提供初始轨迹，随后通过离线批量优化融合全部 IMU 测量、里程计约束和回环检测，获得全局一致的 6-DoF 传感器位姿。这一步骤是后续多帧点云拼接的基础。
- **体素累积与自适应多视图投票**：将多次 LiDAR 扫描累积到体素网格中，利用双 LiDAR 冗余进行投票过滤。投票策略的核心创新在于**基线依赖的自适应阈值**：前向 LiDAR 所需投票数从基线 0.20 m 时的 4 票递减至 0.90 m 时的 1 票，后向 LiDAR 相应从 2 票递减至 1 票。这使近处道路细节得以保留，同时有效抑制远处噪声——消融实验（Figure 6 右）显示，若采用单一共识阈值，近处道路几何会出现明显缺失。
- **动态物体过滤**：通过两个互补机制剔除运动目标。**体素清理**采用中位数绝对偏差（MAD）过滤离群点：保留满足 $| \boldsymbol{r}_i - \tilde{\boldsymbol{r}} | \leq 1.5 \text{MAD}$ 的点，若体素内剩余点数不足 2 则丢弃该体素。**ICP 流动态修剪**则利用扫描间 ICP 残差：当残差超过 0.10 m 时计为“移动投票”，体素收到至少 2 次移动投票即被标记为动态。Figure 6 左的消融清晰展示了无体素清理时动态点被错误注册到静态道路体素中的伪影。
- **遮挡剔除**：以左相机为视点执行 Hidden Point Removal，确保投影到图像空间的深度点均为相机可见。
- **路面相对高度计算**：这是 CARD 区别于所有现有数据集的关键设计。通过标定传感器到四轮中心及车轮接地点的完整变换，CARD 提供每个车轮接地点的世界坐标系轨迹（wheel excitation），进而将相机深度转换为**相对于路面的高度**。这一表示使减速带的凸起和坑洼的凹陷能够被直接量化和可视化（Figure 1 左下）。

### 与现有数据集和方法的谱系关系

**数据集层面**，Table 1 和 Figure 2 给出了系统对比。KITTI Depth Completion 的聚合真值约 75K 点/帧，DrivingStereo 更低，而 CARD 达到约 500K 点/帧——约 6.5 倍于前者，10 倍于其他公开数据集均值。更重要的是，CARD 是唯一同时提供道路地形标注（正/负不规则区域 2D 边界框）和路面相对高度表示的数据集。RSRD 虽涉及道路表面重建，但规模和标注维度远不及 CARD。

**方法评估层面**，CARD 的贡献在于揭示了一个反直觉现象：零样本单目深度估计模型（**Depth Anything V2** (Yang et al., NeurIPS 2024)、**UniDepthV2** (Piccinelli et al., 2025)、**MoGe2** (Wang et al., 2025)）在全局深度指标上表现强劲，但在道路表面不平整区域的限定框内评估中显著退化。例如，Depth Anything V2 在框内 AbsRel 为 0.041，而经 CARD 微调的 MoGe2L† 降至 0.027（降低 34%）。零样本立体模型 **FoundationStereo** (Wen et al., CVPR 2025) 在框内 RMSE 上以 0.185 显著优于最优单目模型的 0.369（降低 49.8%），表明立体基线对道路几何细节的恢复能力更强。

**深度补全任务**上，CARD 评估了 **BP-NET** (Tang et al., CVPR 2024) 和 **DMD3C** (Liang et al., CVPR 2025)。值得注意的是，作者将 DMD3C 的单目教师替换为 FoundationStereo 并改用 L1 损失后，DMD3C+FS 在框内 RMSE 上取得 0.1918，优于原始 DMD3C 和 BP-NET，验证了高密度真值对训练深度补全模型的增益。

### 适用边界与局限

CARD 的设计存在以下明确边界，需在后续使用中审慎考量：

1. **前视局限**：仅覆盖前向立体相机，缺乏 360° 环视覆盖。真值生成管线依赖双 LiDAR 的前向重叠视场，直接扩展到环视系统需要重新设计投票和遮挡剔除策略。
2. **地理多样性不足**：数据采集于德国和意大利，路面类型、交通规则和建筑风格未必代表全球其他地区（如东南亚的雨季泥泞路面或北欧的冰雪覆盖）。
3. **真值质量控制**：尽管动态过滤和离群点剔除已相当严格，但远距离（>80 m）和小物体仍可能保留残余误差。评估范围因此被限制在 80 m 内。
4. **GDPR 匿名化**：人脸和车牌模糊处理可能降低数据集在人/车检测等任务上的训练价值。
5. **标注粒度**：道路地形标注为 2D 边界框，未提供逐像素语义分割或 3D 实例模型，限制了细粒度地形分析的深度。

### 开放问题与后续方向

CARD 开辟了若干值得深入的方向：

- **环视扩展**：如何将多 LiDAR 融合和自适应投票策略推广到 360° 相机系统，实现全向道路地形三维重建？
- **端到端规划集成**：路面相对高度表示能否直接作为端到端规划模型的输入，用于速度调节或局部路径优化？这需要验证高度误差对下游控制策略的敏感性。
- **跨数据集泛化**：利用 CARD 的高密度真值训练的单目/立体模型，能否在 nuScenes 或 Waymo 等传统数据集上零样本提升路面几何感知能力？
- **时间一致性评估**：非规则路面条件下深度补全模型的帧间一致性如何量化？现有指标（RMSE、iMAE）仅评估单帧精度，缺乏对时序稳定性的刻画。
- **全球代表性扩展**：在数据量、国家多样性与采集成本之间如何平衡，以构建更具代表性的全球道路地形数据集？这可能需要社区协作和标准化采集协议。

### 证据强度说明

本节核心结论均有强证据支撑：真值密度优势（Figure 2，置信度 0.95）、零样本模型在路面不规则区域的退化（Table 3，置信度 0.9）、自适应投票和体素清理的消融（Figure 6，置信度 0.98）、路面相对高度表示（wheel excitation 定义，置信度 0.98）。地理多样性不足和匿名化影响等局限来自论文自述，置信度较高。跨数据集泛化和时间一致性评估的开放问题为合理推断，需后续实验验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/CARD_A_Multi_Modal_Automotive_Dataset_for_Dense_3D_Reconstruction_in_Challenging_Road_Topography.pdf]]
