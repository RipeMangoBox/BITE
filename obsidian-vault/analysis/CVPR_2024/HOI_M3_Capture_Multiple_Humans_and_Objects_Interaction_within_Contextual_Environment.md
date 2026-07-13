---
title: "HOI-M3: Capture Multiple Humans and Objects Interaction within Contextual Environment"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/HOI_M3_Capture_Multiple_Humans_and_Objects_Interaction_within_Contextual_Environment.pdf
code_link: null
project_link: https://juzezhang.github.io/HOIM3_ProjectPage
aliases:
- HMMOSMHCCDG
- HOI-M3
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 构建大规模多模态多视角数据集HOI-M3，通过融合密集RGB与物体IMU的鲁棒联合优化实现高精度3D跟踪，从而填补数据空白。
primary_logic: 利用多视图SAM分割掩膜作为核心证据，结合IMU初始化与离屏、碰撞、平滑等多约束联合优化，即使在严重遮挡下也能准确跟踪多人多物的3D运动，为下游捕捉与生成任务奠定基础。
claims:
- HOI-M3是首个同时包含多人多物跟踪的真实世界数据集，在规模（181M帧、20小时）和模态上远超现有数据集。
- 所提单目多人多物捕捉方法在PCKrel与Chamfer距离上显著优于PHOSA和CHORE。
- 消融实验证实离屏损失、IMU初始化和碰撞约束对物体跟踪质量至关重要，缺失会导致退化结果。
- HOI-M3 Multiple HOI Capture 上 PCK_rel (All) = 68.5
---

# HOI-M3: Capture Multiple Humans and Objects Interaction within Contextual Environment

> [!tip] 核心洞察
> 利用多视图SAM分割掩膜作为核心证据，结合IMU初始化与离屏、碰撞、平滑等多约束联合优化，即使在严重遮挡下也能准确跟踪多人多物的3D运动，为下游捕捉与生成任务奠定基础。

| 字段 | 内容 |
|------|------|
| 中文题名 | HOI-M3：在语境环境中捕获多人多物交互 |
| 英文题名 | HOI-M3: Capture Multiple Humans and Objects Interaction within Contextual Environment |
| 会议/期刊 | CVPR 2024 |
| Links |  [Project](https://juzezhang.github.io/HOIM3_ProjectPage)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | HOI-M3 Monocular One-Stage Multiple HOI Capture and Conditional Diffusion Generation |
| Dataset | HOI-M3 Multiple HOI Capture, HOI-M3 Multiple HOI Generation |

> [!tip] 效果简介
> - HOI-M3 Multiple HOI Capture 上，PCK_rel (All) 68.5 vs 43.9 (PHOSA) (+24.6)；Chamfer Distance (All) 235.0 vs 465.8 (CHORE) (-230.8)。
> - HOI-M3 Multiple HOI Generation 上，FID (Joint) 36.906；Pene (%) 9.265。

## 概要

**核心问题**：真实世界中人与物的交互天然涉及多人、多物共存的复杂场景，但现有数据驱动方法受限于数据集的规模与模态，仅能处理单人-单物的简化设定，缺乏对多人多物交互的3D标注数据构成了关键瓶颈。

**核心方案**：本文提出大规模多模态多视角数据集 **HOI-M3**，通过42台密集RGB相机与物体内置IMU的混合采集系统，结合基于多视图SAM分割掩膜与多约束联合优化的鲁棒跟踪管线，首次实现了对多人多物交互的高精度3D运动捕捉。在此基础上，进一步提出单阶段单目多人多物捕捉网络与条件扩散生成模型，支撑下游的捕捉与生成任务。

**方法定位**：在捕捉任务上，所提单阶段方法以统一的中心热图与并行网格图预测替代了PHOSA（Zhang et al., ECCV 2020）、CHORE（Xie et al., ECCV 2022）等多阶段分离式估计范式，并通过视场归一化的绝对深度回归解决了弱投影相机模型导致的根深度不准问题。在生成任务上，以物体几何与人数/物体数为条件，利用PointNet提取物体特征后输入扩散模型，生成多人多物交互序列。

**关键结果**：
- HOI-M3数据集包含1.81亿帧、20小时录制时长，覆盖5类日常室内场景，是首个同时支持多人多物跟踪的真实世界数据集（Table 1）。
- 单目多人多物捕捉在PCK_rel指标上达到68.5，较PHOSA（43.9）提升24.6；Chamfer距离降至235.0，较CHORE（465.8）降低230.8（Table 2）。
- 消融实验证实，离屏损失、IMU初始化与碰撞约束对物体跟踪质量至关重要，缺失任一项均会导致退化解或非物理交互（Figure 12）。
- 多人多物生成在Joint FID上达到36.906，穿透率Pene为9.265%（Table 3）。

**局限与开放问题**：当前数据集受硬件成本与采集条件限制，仅覆盖室内固定光照环境，场景与背景多样性有限，向室外无约束场景扩展仍具挑战。如何在严重遮挡下进一步提升跟踪鲁棒性、如何低成本扩展采集范式、以及如何设计融合模型实现光照与背景泛化，是后续研究的重要方向。



理解人与物体在真实三维空间中的交互（Human-Object Interaction, HOI）是计算机视觉与具身智能领域的核心挑战。从机器人操作到增强现实，从运动分析到数字人驱动，准确感知与重建多人多物的动态交互关系，是实现环境理解与行为模拟的基础。

然而，现有数据驱动方法面临一个根本性瓶颈：**缺乏真实世界中多人多物交互的大规模三维标注数据**。当前公开的HOI或人-场景交互（HSI）数据集——如BEHAVE、InterCap、GRAB等——虽然在特定任务上推动了技术进步，但在交互规模上存在显著局限：它们大多仅包含单人与单个物体的交互场景，无法覆盖日常生活中普遍存在的多人协作、多人共享物体或多人多物并行交互的复杂情形。

这一数据缺口直接导致了两方面的困境。其一，现有的单目HOI捕捉方法（如**PHOSA**（Zhang et al., ECCV 2020）和**CHORE**（Xie et al., ECCV 2022））在设计上仅面向单人-单物场景，当面对多人多物同时出现时，其分离式的估计策略与弱投影相机模型会引发根深度估计不准确、物体身份混淆和交互关系错乱等问题。其二，缺乏大规模多模态基准数据，使得下游任务（如交互序列生成、场景理解）难以向多主体交互方向扩展。

本文的核心动机正是填补这一空白。作者提出了**HOI-M3**——一个大规模、多模态、多视角的真实世界多人多物交互数据集。该数据集包含1.81亿视频帧（约20小时录制时长），由42台Z CAM电影级相机同步采集，覆盖卧室、餐厅、客厅、健身房、办公室五类日常场景。与现有数据集相比，HOI-M3不仅是**首个同时包含多人多物跟踪的真实世界数据集**，其规模与模态丰富度也远超同类（Table 1）。

为构建这一数据集，作者设计了一套鲁棒的联合优化管线：通过融合密集RGB输入与物体内置IMU数据，结合多视图SAM分割掩膜作为核心证据，利用离屏约束、碰撞约束与平滑约束进行联合优化，从而在严重遮挡下也能实现高精度的多人多物三维运动跟踪。这一高质量的真值标注，为后续提出的单阶段单目多人多物捕捉方法与条件扩散交互生成模型奠定了坚实的数据基础。



## 核心方法与创新机理

HOI-M3 的核心创新在于围绕**数据稀缺**与**感知瓶颈**双线展开：一方面构建首个大规模多人多物交互数据集，填补真实 3D 标注空白；另一方面提出单阶段单目捕捉与条件扩散生成方法，突破现有多阶段/分离式方法在多人多物场景下的退化问题。

### 1. 数据集层面的结构性创新

现有 HOI/HSI 数据集（如 BEHAVE、GRAB、InterCap 等）仅覆盖单人单物交互，且规模与模态有限。HOI-M3 通过密集 42 视角 RGB 相机与物体嵌入式 IMU 的混合采集系统，实现了三个关键突破：

- **多人多物跟踪**：首次在真实环境中同时跟踪多人与多物的 3D 运动，覆盖卧室、餐厅、客厅、健身室、办公室五类日常场景。
- **规模跃升**：总计 1.81 亿帧、20 小时录制，远超现有数据集（Table 1）。
- **多模态融合**：结合密集 RGB 与 IMU 信号，通过鲁棒联合优化实现高精度跟踪，为下游任务提供强监督信号。

这一数据集的构建直接回应了本领域的核心瓶颈——**缺乏真实世界多人多物交互的 3D 标注数据**，使得数据驱动方法首次具备处理多人多物场景的训练基础。

### 2. 跟踪管道的关键算法创新

在数据集构建的跟踪管道中，论文提出了**惯性辅助多物体跟踪**方法，其核心创新在于将 IMU 提供的旋转先验与多视图视觉证据深度融合：

- **IMU 初始化**：利用物体嵌入式 IMU 提供旋转初值，解决纯视觉方法在严重遮挡下的旋转恢复难题。
- **联合优化框架**：以 IMU 旋转 $R_t^{\mathrm{IMU}}$ 为基础，联合估计旋转偏移 $R_t^{\mathrm{off}}$ 与平移 $T_t$，优化目标融合四项约束：
  $$R_t^{\mathrm{off}}, T_t = \arg\min_{R,T} (\lambda_{\mathrm{mask}} E_{\mathrm{mask}} + \lambda_{\mathrm{offscreen}} E_{\mathrm{offscreen}} + \lambda_{\mathrm{collision}} E_{\mathrm{collision}} + \lambda_{\mathrm{smt}} E_{\mathrm{smt}})$$
  其中多视图 SAM 分割掩膜作为核心视觉证据，离屏约束防止物体移出画面退化，碰撞约束确保物理合理性，平滑约束保持运动与 IMU 信号的一致性。

消融实验证实，去除离屏项会导致物体移出画面的退化解，无 IMU 初始化则难以恢复旋转，无碰撞约束会产生非物理交互（Figure 12, Appendix E.2）。这一多约束联合优化机制是跟踪精度的关键保障。

### 3. 单目捕捉方法的架构创新

针对下游单目多人多物捕捉任务，论文提出**单阶段统一管道**，与 PHOSA（Zhang et al., ECCV 2020）和 CHORE（Xie et al., ECCV 2022）等现有多阶段/分离式方法形成显著差异：

| 方法维度 | 现有方法（PHOSA/CHORE） | HOI-M3 单阶段方法 |
|---------|----------------------|-------------------|
| **管道架构** | 多阶段分离估计人体与物体 | 单阶段统一预测中心热图、人体网格图、物体网格图及深度 |
| **深度估计** | 弱投影相机模型，根深度不准确 | 视场归一化绝对深度回归 $\hat{Z} = Z \frac{w}{f}$ |
| **输出方式** | 分别处理单人单物，无法扩展 | 并行网格图一次性输出所有人与物体的 3D 姿态 |

单阶段设计的核心优势在于：通过中心热图定位人体根位置与物体中心，网格图编码 SMPL 参数与物体 6D 姿态，深度回归提供绝对尺度，避免了多阶段管道中的误差累积与多人多物场景下的组合爆炸问题。这一架构创新使得方法在 PCK_rel（68.5 vs PHOSA 43.9/CHORE 10.4）和 Chamfer 距离（235.0 vs 1454.3/465.8）上实现大幅领先（Table 2）。

### 4. 生成方法的条件化创新

在多人多物交互生成任务中，论文提出以**物体几何为条件**的扩散生成框架：使用 PointNet 提取多物体几何特征，与预设人数/物体数的特征通过 MLP 融合后输入条件扩散模型。这一设计使得生成结果能够适应不同的场景物体配置，在 FID（36.906）和穿透率 Pene（9.265%）上建立了首个多人多物生成基准（Table 3）。

### 创新边界与局限

上述创新受限于当前数据集的采集条件：42 相机系统与 IMU 嵌入的高硬件成本限制了场景扩展至室外环境；固定光照与有限背景变化制约了捕捉与生成模型的泛化能力；当前仅覆盖 5 类常见房间，场景多样性仍有提升空间。这些局限同时也指明了未来的创新方向——低成本采集范式、仿真-真实混合增强、以及光照/背景不变性建模。



HOI-M3 的整体框架由两大核心阶段构成：**大规模数据集构建**与**下游任务方法设计**。前者通过多模态采集与鲁棒联合优化，填补了真实世界多人多物交互 3D 标注数据的空白；后者则在此数据基础上，分别提出单目单阶段多人多物捕捉和条件扩散交互生成两种方法。

### 数据采集与标注管线

数据集构建的物理基础是 42 台 Z CAM 电影摄影机组成的密集多视角采集系统，同时每件预扫描物体内部嵌入惯性测量单元（IMU），形成 RGB-IMU 混合采集模态（Figure 9）。整个数据生产管线分为四个串行模块：

![[assets/figures/papers/paper_list_l1718_HOI_M3_Capture_Multiple_Humans_and_Objects_Interaction_within_Contextual/figures/012_Figure_9.jpg]]
*Figure 9: Hardware setup*

1. **数据同步与标定**：对 RGB 视频流与 IMU 信号进行时间对齐，并标定 IMU 到 RGB 坐标系的旋转偏移 $R_t^{\mathrm{off}}$，为后续融合优化提供初始外参。
2. **人体运动捕捉**：使用 ViTPose 检测 2D 关键点，经跨视图匹配与三角化重建后，拟合 SMPL 模型参数，获得每帧人体 3D 网格。
3. **惯性辅助多物体跟踪**：以 IMU 提供的旋转 $R_t^{\mathrm{IMU}}$ 为初始化，联合优化旋转偏移 $R_t^{\mathrm{off}}$ 与平移 $T_t$，使物体顶点位置 $V_t^j$ 满足多视图 SAM 分割掩膜、离屏、碰撞、平滑四重约束：

   $$V_t^j(R_t^{\mathrm{IMU}}, R_t^{\mathrm{off}}, T_t) = R_t^{\mathrm{off}} R_t^{\mathrm{IMU}} \mathcal{O}(c_j) + T_t$$

   $$R_t^{\mathrm{off}}, T_t = \arg\min_{R,T} (\lambda_{\mathrm{mask}} E_{\mathrm{mask}} + \lambda_{\mathrm{offscreen}} E_{\mathrm{offscreen}} + \lambda_{\mathrm{collision}} E_{\mathrm{collision}} + \lambda_{\mathrm{smt}} E_{\mathrm{smt}})$$

   其中 $E_{\mathrm{mask}}$ 以 SAM 分割掩膜为核心证据，强制投影轮廓与掩膜一致；$E_{\mathrm{offscreen}}$ 防止物体移出画面产生退化解；$E_{\mathrm{collision}}$ 惩罚人与物、物与物之间的穿透；$E_{\mathrm{smt}}$ 约束估计旋转的平滑度不偏离原始 IMU 信号。消融实验证实，缺失离屏项或 IMU 初始化会导致退化与旋转恢复困难，无碰撞约束则产生非物理交互（Figure 12, Appendix E.2）。
4. **多模态标注生成**：最终输出包含多人 SMPL 参数、多物体 6D 姿态、实例分割掩膜及预扫描物体网格，覆盖卧室、餐厅、客厅、健身室、办公室五类日常场景，总计 181M 帧、20 小时录制（Figure 2, Table 1）。

![[assets/figures/papers/paper_list_l1718_HOI_M3_Capture_Multiple_Humans_and_Objects_Interaction_within_Contextual/figures/002_Figure_2.jpg]]
*Figure 2: Overview of HOI-M3. (a) HOI-M3 across five daily scenarios(Bedroom, Dinning Room, Living Room, Fitness Room, Office), (b) annotated masks corresponding to each subject(human, object), (c) tracking of multiple humans and multiple objects, (d) significant number of pre-scanned object meshes*

### 下游任务方法管线

在 HOI-M3 数据集之上，论文设计了两条下游任务管线，共享数据集提供的 3D 真值监督。

**单目单阶段多人多物捕捉**（Figure 3）以单张 RGB 图像为输入，通过统一网络并行预测四类密集输出图：人体-物体中心热图（定位根关节与物体中心）、人体网格图（SMPL 参数编码）、物体网格图（物体姿态编码）以及视场归一化的绝对深度 $\hat{Z} = Z \frac{w}{f}$。所有人和物体的 3D 姿态一次性从这些图中解码，无需分离式多阶段处理。总损失函数为各分支 L1/MSE 损失的加权和：

$$L_{\mathrm{sum}} = \lambda_{\mathrm{theta}} L_{\mathrm{theta}} + \lambda_{\mathrm{beta}} L_{\mathrm{beta}} + \lambda_{\mathrm{object}} L_{\mathrm{object}} + \lambda_{\mathrm{3D}} L_{\mathrm{3D}} + \lambda_{\mathrm{2D}} L_{\mathrm{2D}} + \lambda_{\mathrm{hm}} L_{\mathrm{hm}} + \lambda_{\mathrm{depth}} L_{\mathrm{depth}}$$

与 PHOSA（Zhang et al., ECCV 2020）和 CHORE（Xie et al., ECCV 2022）的单人-物体分离式估计相比，该单阶段统一设计在多人多物场景中 PCK_rel 提升 +24.6，Chamfer 距离降低 -230.8（Table 2）。

**条件扩散多人多物交互生成**（Figure 4）以预设人数（5 人）与物体数（10 物）及物体几何为条件。首先用 PointNet 提取多物体几何特征，经 MLP 与人数/物体数特征融合后，输入条件扩散模型。扩散过程在 $\mathbb{R}^{500}$ 的交互表示空间中进行（前 440 维为 5 人 SMPL 参数，后 60 维为 10 物体姿态），训练目标为 L1 重建损失 $\mathcal{L} = \mathbb{E}_{x_0,n} \| \hat{x}_{\theta}(x_n, n) - x_0 \|_1$。去噪网络架构见 Figure 8。

两条管线的输入输出关系清晰：捕捉管线从单目 RGB 映射到 3D 交互状态，生成管线则从场景几何与交互规模条件出发，合成符合物理约束的多人多物运动序列。

### 补充图表

![[assets/figures/papers/paper_list_l1718_HOI_M3_Capture_Multiple_Humans_and_Objects_Interaction_within_Contextual/figures/004_Figure_3.jpg]]
*Figure 3: Monocular One-Stage Multiple HOI Capturing Pipeline. Given an input image, the pipeline predicts multiple maps: 1) the human-object center heatmap predicts the probability of the human’s root position or object’s center position, 2) the human mesh map contains the SMPL parameters and root depth, 3) the object mesh map contains the object 6D pose parameters and center depth. Through the sampling process, multiple humans and objects can be captured within a single forward process*



HOI-M3 的系统架构围绕两个核心任务展开：一是面向数据集构建的**多模态高精度3D跟踪**，二是面向下游应用的**单目多人多物捕捉与生成**。本节聚焦关键模块的设计逻辑与公式含义，不展开实验细节。

---

### 3.5 惯性辅助的多物体跟踪

数据集构建的核心挑战在于：在多人多物密集交互且存在严重遮挡的场景中，仅靠多视角RGB难以鲁棒地恢复物体的6自由度位姿。HOI-M3 的解决方案是融合物体内嵌IMU的旋转信号与多视角分割掩膜，通过联合优化实现高精度跟踪。

**物体顶点位置建模**

对于第 $j$ 个物体在第 $t$ 帧的顶点位置，其3D坐标由IMU旋转、标定偏移与平移共同决定：

$$V_t^j(R_t^{\mathrm{IMU}}, R_t^{\mathrm{off}}, T_t) = R_t^{\mathrm{off}} R_t^{\mathrm{IMU}} \mathcal{O}(c_j) + T_t$$

其中：
- $R_t^{\mathrm{IMU}}$：IMU 提供的原始旋转矩阵，为物体朝向提供强先验
- $R_t^{\mathrm{off}}$：待优化的IMU到RGB坐标系的旋转偏移，用于校正IMU与相机之间的安装偏差
- $T_t$：待优化的物体平移向量
- $\mathcal{O}(c_j)$：预扫描物体模板的第 $j$ 个顶点坐标

**多约束联合优化目标**

旋转偏移 $R_t^{\mathrm{off}}$ 与平移 $T_t$ 通过最小化四项加权能量函数估计：

$$R_t^{\mathrm{off}}, T_t = \arg\min_{R,T} (\lambda_{\mathrm{mask}} E_{\mathrm{mask}} + \lambda_{\mathrm{offscreen}} E_{\mathrm{offscreen}} + \lambda_{\mathrm{collision}} E_{\mathrm{collision}} + \lambda_{\mathrm{smt}} E_{\mathrm{smt}})$$

四项约束的因果机制如下：

1. **掩膜约束 $E_{\mathrm{mask}}$**：核心证据项。利用多视图SAM分割掩膜，将投影后的物体轮廓与分割掩膜对齐，为跟踪提供逐像素的视觉监督。这是处理遮挡的关键——即使部分顶点被遮挡，剩余可见区域的掩膜匹配仍能约束位姿。

2. **离屏约束 $E_{\mathrm{offscreen}}$**：惩罚物体移出图像边界的退化解。消融实验证实，去除该项会导致物体在遮挡严重时“漂移”出画面，跟踪完全失效。

3. **碰撞约束 $E_{\mathrm{collision}}$**：引入人-人、人-物、物-物之间的穿透惩罚，确保交互的物理合理性。该约束借鉴了已有工作[57, 71]中的碰撞损失设计。消融表明，无碰撞约束时会产生非物理的穿透伪影。

4. **平滑约束 $E_{\mathrm{smt}}$**：鼓励估计旋转与原始IMU信号的平滑度保持一致：

$$E_{\mathrm{smt}} = \max(0, \| (R_t^{\mathrm{off}} R_t^{\mathrm{IMU}})^{-1} R_{t+1}^{\mathrm{off}} R_{t+1}^{\mathrm{IMU}} \|_2 - \| (R_t^{\mathrm{IMU}})^{-1} R_{t+1}^{\mathrm{IMU}} \|_2)$$

该约束的核心洞察是：IMU 本身提供高质量的相对旋转变化率，优化后的旋转不应引入额外的抖动。当估计旋转的帧间变化量超过IMU原始变化量时，施加惩罚。

**IMU初始化的关键作用**：消融实验揭示，若无IMU初始化（即 $R_t^{\mathrm{IMU}}$ 缺失），仅靠视觉约束在严重遮挡下难以恢复正确的物体朝向，旋转估计会退化为随机猜测。IMU 为优化提供了可靠的旋转初值，使联合优化能在正确的局部极小值附近收敛。

---

### 4.1 单目单阶段多人多物捕捉

该模块将多视角跟踪得到的3D真值作为监督信号，训练单目网络从单张RGB图像一次性恢复所有人和物体的3D姿态。

**视场归一化深度**

传统弱投影相机模型在多人多物场景中会导致根深度估计严重不准确。HOI-M3 采用视场归一化的绝对深度回归：

$$\hat{Z} = Z \frac{w}{f}$$

其中 $Z$ 为原始深度，$f$ 为焦距，$w$ 为图像宽度。该归一化将深度映射到与图像尺度相关的无量纲空间，使网络能在不同视场下学习一致的深度表征，从而支撑绝对位姿估计（PCKabs）。

**总损失函数**

捕捉网络的训练目标为七项损失的加权和：

$$L_{\mathrm{sum}} = \lambda_{\mathrm{theta}} L_{\mathrm{theta}} + \lambda_{\mathrm{beta}} L_{\mathrm{beta}} + \lambda_{\mathrm{object}} L_{\mathrm{object}} + \lambda_{\mathrm{3D}} L_{\mathrm{3D}} + \lambda_{\mathrm{2D}} L_{\mathrm{2D}} + \lambda_{\mathrm{hm}} L_{\mathrm{hm}} + \lambda_{\mathrm{depth}} L_{\mathrm{depth}}$$

各损失项含义：
- $L_{\mathrm{theta}}$、$L_{\mathrm{beta}}$：SMPL姿态与体型参数的L1回归
- $L_{\mathrm{object}}$：物体6D位姿与尺寸参数的L1回归
- $L_{\mathrm{3D}}$、$L_{\mathrm{2D}}$：3D关键点与2D重投影的监督
- $L_{\mathrm{hm}}$：人体-物体中心热图的MSE损失，用于定位实例
- $L_{\mathrm{depth}}$：归一化深度的回归损失

该单阶段并行预测架构（同时输出中心热图、人体网格图、物体网格图与深度）替代了PHOSA、CHORE等方法的分离式多阶段设计，避免了误差累积，是PCKrel提升+24.6的关键结构因素。

---

### 4.2 条件扩散生成

生成模块以物体几何和预设的人数/物体数为条件，生成多人多物交互序列。交互状态表示为 $\mathbb{R}^{500}$ 维向量：前440维编码5个人的SMPL参数，后60维编码10个物体的6D位姿。

**扩散过程**

前向过程为标准马尔可夫链，逐步向原始数据 $x_0$ 注入高斯噪声：

$$q(x_{1:N} | x_0) := \prod_{n=1}^N q(x_n | x_{n-1})$$

**训练目标**

去噪网络以L1损失预测原始数据：

$$\mathcal{L} = \mathbb{E}_{x_0,n} \| \hat{x}_{\theta}(x_n, n) - x_0 \|_1$$

条件信号通过PointNet提取物体几何特征，经MLP与人数/物体数特征融合后注入去噪网络，引导生成物理合理的多人多物交互序列。

### 补充图表

![[assets/figures/papers/paper_list_l1718_HOI_M3_Capture_Multiple_Humans_and_Objects_Interaction_within_Contextual/figures/005_Figure_4.jpg]]
*Figure 4: Multiple Interaction Generation Pipeline. Given multiple object geometry, we employ Pointnet to extract the geometry features and feed them forward with the features of the preset number of humans and objects using an MLP. The resulting features are then fed into a conditional diffusion model to generate multiple human-object interactions*

![[assets/figures/papers/paper_list_l1718_HOI_M3_Capture_Multiple_Humans_and_Objects_Interaction_within_Contextual/figures/011_Figure_8.jpg]]
*Figure 8: Model architecture of denoising network*



## 实验与关键发现

### 核心实验设计

论文围绕HOI-M3数据集构建了两条评估主线：**单目多人多物捕捉（Monocular Multiple HOI Capture）**与**多人多物交互生成（Multiple Interaction Generation）**。捕捉任务检验从单张RGB图像恢复所有人体SMPL网格与物体6D位姿的能力；生成任务则评估以物体几何为条件、合成合理多人多物交互序列的质量。两条主线共享HOI-M3提供的多视角真值标注，但评估指标与基线选择各有侧重。

### 多人多物捕捉基准结果

Table 2报告了捕捉任务的核心定量结果。论文方法在**PCK_rel（All）**上达到68.5，相较**PHOSA**（Zhang et al., ECCV 2020）的43.9提升+24.6，相较**CHORE**（Xie et al., ECCV 2022）的10.4提升+58.1。在**Chamfer距离（All）**上，论文方法为235.0，PHOSA为1454.3，CHORE为465.8，分别降低-1219.3与-230.8。两组指标一致表明，面向单人-物体设计的PHOSA与CHORE在多人多物场景中性能退化严重，而论文的单阶段统一预测架构在该场景下具有显著优势。

值得注意的是，PHOSA与CHORE采用弱投影相机模型，导致根深度估计不准确，**无法计算PCKabs**——这从侧面印证了论文引入视场归一化绝对深度回归（Eq. 6）的必要性。在“Matched”设定下（仅评估两方法能同时检测到的人与物体），论文方法的PCK_rel仍保持66.0，Chamfer为264.0，优势依然稳固。

Figure 5的定性对比进一步揭示了失败模式：PHOSA与CHORE在多人多物密集交互时，常出现人体-物体空间关系错乱、物体位姿漂移或完全丢失等问题，而论文方法通过中心热图与并行网格图预测，能够更鲁棒地保持全局空间一致性。

### 多人多物生成基准结果

Table 3展示了生成任务的评估指标。论文的条件扩散模型在**Joint FID**上达到36.906，**Pene（穿透率）**为9.265%。由于该任务是论文首次定义，缺乏直接可比的基线方法，这些数值主要作为未来工作的参考基准。Figure 6展示了两个定性序列（客厅环境，2人5物），生成的交互序列在物体几何约束下保持了合理的空间布局与运动连贯性。

### 消融实验：约束项的关键作用

物体跟踪阶段的消融实验（Figure 12与附录E.2）揭示了四项约束的因果贡献：

- **去除离屏项（w/o offscreen loss）**：物体在部分遮挡或移出画面边界时出现退化解，位姿估计完全失效。离屏损失通过惩罚投影到画面外的顶点，强制优化过程将物体约束在可见区域内。
- **去除IMU初始化（w/o IMU Init）**：仅依赖视觉线索难以恢复物体的精确旋转，尤其在对称物体或纹理稀疏的情况下。IMU提供的绝对旋转先验是旋转估计的“锚点”。
- **去除碰撞约束（w/o collision constraint）**：人体与物体、物体与物体之间出现明显穿透，生成的交互在物理上不合理。碰撞损失（引用[57, 71]）通过惩罚网格间穿透，保证了交互的物理可行性。
- **平滑约束**：确保估计的旋转序列与原始IMU信号的平滑度一致，抑制帧间抖动。

这四项约束形成互补：IMU初始化提供旋转先验，掩膜约束提供2D证据，离屏与碰撞约束保证空间合理性，平滑约束保证时序一致性。缺失任一项均会导致特定退化模式。

### 单目3D人体姿态估计补充基准

Table 4（嵌入Figure 10区域）报告了在HOI-M3上的单目3D人体姿态与形状估计结果，以MPJPE与PA-MPJPE为指标。该基准为评估人体重建模块的独立性能提供了参考，但需注意该结果是在多人多物交互的复杂背景下获得的，与单人孤立场景的评估不可直接类比。

### 公平性讨论与评估局限

PHOSA与CHORE原本面向单人-物体场景设计，在多人多物场景中可能因检测召回不足而处于劣势。论文通过“Matched”设定部分缓解了这一问题——仅评估两方法均能检测到的主体——但仍无法完全消除架构层面的不匹配。此外，捕捉任务的评估依赖于HOI-M3的多视角真值，该真值本身由论文的跟踪管道生成，可能存在自洽偏差。生成任务的FID与穿透率指标虽能反映分布质量与物理合理性，但尚缺乏感知层面的用户研究验证。

### 补充图表

![[assets/figures/papers/paper_list_l1718_HOI_M3_Capture_Multiple_Humans_and_Objects_Interaction_within_Contextual/figures/003_Table_1.jpg]]
*Table 1: Dataset Comparisons. We compare our proposed HOI*

![[assets/figures/papers/paper_list_l1718_HOI_M3_Capture_Multiple_Humans_and_Objects_Interaction_within_Contextual/figures/007_Table_2.jpg]]
*Table 2: Multiple HOI capture benchmark. ”Fit to input” represents the vanilla method that fits the object template to image and capture human with Frankmocap [51]. The best results are in bold*

![[assets/figures/papers/paper_list_l1718_HOI_M3_Capture_Multiple_Humans_and_Objects_Interaction_within_Contextual/figures/009_Table_3.jpg]]
*Table 3: Benchmark of multiple HOI generation on*

![[assets/figures/papers/paper_list_l1718_HOI_M3_Capture_Multiple_Humans_and_Objects_Interaction_within_Contextual/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparisons of monocular multiple interaction capture on*

![[assets/figures/papers/paper_list_l1718_HOI_M3_Capture_Multiple_Humans_and_Objects_Interaction_within_Contextual/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative results of multiple interaction generation: We present the outcomes of two distinct sequences within a living room environment, each defined by specific object geometries and a predefined configuration of 2 persons and 5 objects*

![[assets/figures/papers/paper_list_l1718_HOI_M3_Capture_Multiple_Humans_and_Objects_Interaction_within_Contextual/figures/016_Figure_12.jpg]]
*Figure 12: Data examples were captured by our system*

![[assets/figures/papers/paper_list_l1718_HOI_M3_Capture_Multiple_Humans_and_Objects_Interaction_within_Contextual/figures/010_Figure_7.jpg]]
*Figure 7: Statistics of*



## 定位与知识库关联

### 1. 在多人多物交互重建谱系中的位置

HOI-M3 的工作横跨**数据采集、多模态跟踪优化与单目重建**三个层面，其核心贡献在于首次将数据驱动的人-物交互（HOI）研究从“单人-单物”范式推至“多人-多物”真实场景。

在单目 HOI 重建这一支线上，此前的主流方法均围绕单人-单物设定设计。**PHOSA**（Zhang et al., ECCV 2020）通过优化人体与物体的空间关系来感知交互，但其弱投影相机模型在多人物体场景中导致根深度估计严重失准，无法计算绝对 PCK 指标。**CHORE**（Xie et al., ECCV 2022）在接触约束下联合重建人体与物体，但在多人多物共存的复杂遮挡环境中，其分离式估计策略难以维持全局一致性。HOI-M3 的单阶段捕捉网络（Figure 3）通过统一预测人体-物体中心热图、人体网格图、物体网格图及视场归一化深度（$\hat{Z} = Z \frac{w}{f}$），以并行方式一次性输出所有人与物体的 3D 姿态，在架构层面突破了上述基线方法的单实例假设。

在数据集层面，HOI-M3 填补了真实世界多人多物交互 3D 标注数据的空白。Table 1 的对比显示，其规模（181M 帧、20 小时记录）与模态丰富度（密集 RGB + 物体 IMU + 预扫描物体网格）远超现有 HOI/HSI 数据集，是首个同时支持多人多物跟踪的数据集。这一数据基础使得下游的捕捉与生成任务得以在真实交互分布上训练与评估。

### 2. 关键技术决策与基线差异

HOI-M3 的物体跟踪优化（Section 3.5）引入了 IMU 辅助的联合优化范式，这是与纯视觉基线方法的本质区别。物体每帧顶点位置由 IMU 旋转、标定偏移与平移共同决定：

$$V_t^j(R_t^{\mathrm{IMU}}, R_t^{\mathrm{off}}, T_t) = R_t^{\mathrm{off}} R_t^{\mathrm{IMU}} \mathcal{O}(c_j) + T_t$$

优化目标融合了四项约束：

$$R_t^{\mathrm{off}}, T_t = \arg\min_{R,T} (\lambda_{\mathrm{mask}} E_{\mathrm{mask}} + \lambda_{\mathrm{offscreen}} E_{\mathrm{offscreen}} + \lambda_{\mathrm{collision}} E_{\mathrm{collision}} + \lambda_{\mathrm{smt}} E_{\mathrm{smt}})$$

其中，多视图 SAM 分割掩膜（$E_{\mathrm{mask}}$）作为核心视觉证据，离屏约束（$E_{\mathrm{offscreen}}$）防止物体退化出画面，碰撞约束（$E_{\mathrm{collision}}$）惩罚人-物、物-物穿透，平滑约束（$E_{\mathrm{smt}}$）确保估计旋转与原始 IMU 信号的平滑度一致。消融实验（Figure 12，Appendix E.2）证实：去除离屏项导致物体移出画面退化解；无 IMU 初始化时旋转恢复极具挑战；无碰撞约束则产生非物理交互。这一多约束融合的设计使得系统在严重遮挡下仍能保持鲁棒跟踪。

在单目捕捉网络中，另一个关键改进是将弱投影相机模型替换为**视场归一化的绝对深度回归**（$\hat{Z} = Z \frac{w}{f}$），总损失函数为：

$$L_{\mathrm{sum}} = \lambda_{\mathrm{theta}} L_{\mathrm{theta}} + \lambda_{\mathrm{beta}} L_{\mathrm{beta}} + \lambda_{\mathrm{object}} L_{\mathrm{object}} + \lambda_{\mathrm{3D}} L_{\mathrm{3D}} + \lambda_{\mathrm{2D}} L_{\mathrm{2D}} + \lambda_{\mathrm{hm}} L_{\mathrm{hm}} + \lambda_{\mathrm{depth}} L_{\mathrm{depth}}$$

这一设计使得网络能够直接回归可比较的绝对深度，从而在 PCK_rel 上达到 68.5，显著优于 PHOSA 的 43.9 和 CHORE 的 10.4；Chamfer 距离降至 235.0，远低于 PHOSA 的 1454.3 和 CHORE 的 465.8（Table 2）。

### 3. 适用边界与局限

当前方法的有效边界受数据集采集范式的严格约束：

- **环境受限**：受 42 台 Z CAM 摄影机与 IMU 嵌入的硬件成本限制，HOI-M3 仅在 5 类室内场景（卧室、餐厅、客厅、健身室、办公室）的固定光照条件下采集，背景变化极少。模型对室外、野外或无约束光照环境的泛化能力未经检验。
- **场景多样性有限**：构建此类数据集需要大量人力标注，目前仅覆盖有限数量的常见房间布局与物体类别。扩展到更多样化的场景、物体几何与交互类型仍需高昂成本。
- **动态遮挡边界**：尽管多约束优化在现有数据上表现鲁棒，但在极端动态遮挡（如多人密集交互、物体完全被人体遮蔽）下的跟踪精度仍是开放挑战。

### 4. 开放问题

1. **鲁棒跟踪的极限**：在更严重的动态遮挡与快速运动场景中，如何进一步提升多人多物的联合跟踪精度？是否需要引入时序先验或物理模拟约束？
2. **低成本扩展范式**：能否通过仿真-真实混合数据增强策略，以较低成本扩展数据集的场景、光照与交互多样性？神经渲染与域随机化在此场景下的有效性值得探索。
3. **跨域泛化**：如何利用 HOI-M3 的多模态数据（RGB + IMU + 物体几何）设计对光照与背景变化鲁棒的融合模型？自监督域适应或测试时优化可能是可行方向。
4. **交互生成的物理合理性**：当前扩散生成模型（Figure 4）以物体几何和人数/物体数为条件，FID 为 36.906，穿透率 9.265%（Table 3）。如何进一步降低穿透率并提升生成交互的物理真实感，是通往实用化交互合成的关键瓶颈。



## 原文 PDF

![[paperPDFs/CVPR_2024/HOI_M3_Capture_Multiple_Humans_and_Objects_Interaction_within_Contextual_Environment.pdf]]
