---
title: "CineMaster: A 3D-Aware and Controllable Framework for Cinematic Text-to-Video Generation"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/CineMaster_A_3D_Aware_and_Controllable_Framework_for_Cinematic_Text_to_Video_Generation.pdf
project_link: "https://cinemaster-dev.github.io/"
code_link: null
aliases:
- CineMaster
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过交互式3D工作流生成的渲染深度图、摄像机轨迹和物体类别标签作为条件信号，注入预训练的文本到视频扩散模型中，从而精确控制生成视频中的三维布局与运动。
primary_logic: 将用户指定的3D边界框和摄像机运动渲染为投影深度图，结合语义布局注入网络（Semantic Layout ControlNet）和摄像机适配器（Camera Adapter），可解除物体运动与摄像机运动之间的歧义，实现3D感知的联合控制。
claims:
- CineMaster significantly outperforms previous SOTA methods on all metrics (mIoU, Traj-D, FVD, FID, CLIP-T).
- Joint training of Semantic Layout ControlNet and Camera Adapter yields the best overall results.
- Table 1 上 mIoU (object placement accuracy) = 0.551
- Table 1 上 Traj-D (trajectory distance) = 66.29
---

# CineMaster: A 3D-Aware and Controllable Framework for Cinematic Text-to-Video Generation

> [!tip] 核心洞察
> 将用户指定的3D边界框和摄像机运动渲染为投影深度图，结合语义布局注入网络（Semantic Layout ControlNet）和摄像机适配器（Camera Adapter），可解除物体运动与摄像机运动之间的歧义，实现3D感知的联合控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | CineMaster：面向电影级文本到视频生成的三维感知可控框架 |
| 英文题名 | CineMaster: A 3D-Aware and Controllable Framework for Cinematic Text-to-Video Generation |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](http://arxiv.org/abs/2502.08639v1) · [Project](https://cinemaster-dev.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | CineMaster |
| Dataset | Table 1 |

> [!tip] 效果简介
> - Table 1 上，mIoU (object placement accuracy) 0.551 vs SOTA baselines (lower) (CineMaster highest)；Traj-D (trajectory distance) 66.29 vs SOTA baselines (worse) (CineMaster best)；FVD (Fréchet Video Distance) 1530.9 vs SOTA baselines (higher FVD) (CineMaster lowest (best))。

## 概要

**问题瓶颈**：现有可控视频生成方法依赖二维平面条件，无法让用户像电影导演般在三维空间中直观操控物体与摄像机运动；同时缺乏带有3D边界框和摄像机轨迹标注的大规模真实视频数据集。

**核心方法**：CineMaster提出两阶段框架——首先通过基于Blender的交互式3D工作流，让用户放置3D边界框并定义摄像机运动，渲染出投影深度图和摄像机轨迹作为控制信号；随后将这些信号通过语义布局控制网络（Semantic Layout ControlNet）和摄像机适配器（Camera Adapter）注入预训练的文本到视频扩散模型，解除物体运动与摄像机运动的歧义，实现3D感知的联合控制。

**主要结果**：在mIoU、轨迹距离（Traj-D）、FVD、FID和CLIP-T五项指标上均超越此前SOTA方法（如MotionCtrl、Direct-A-Video），联合训练语义布局控制网络与摄像机适配器获得最优综合性能。

**方法定位**：CineMaster将可控视频生成从二维平面条件提升至三维感知交互范式，填补了3D布局与摄像机联合可控的空白，为电影级AI创作工具提供了新基线。

## 核心方法与创新机理

**瓶颈**：现有可控视频生成方法（如 **MotionCtrl**（Wang et al., arXiv 2023）和 **Direct-A-Video**（Yang et al., ACM SIGGRAPH 2024））依赖二维平面条件图控制物体与摄像机运动，无法让用户像电影导演一样在三维空间中直观操控；同时，缺乏带有 3D 边界框和摄像机轨迹标注的大规模真实视频数据集，制约了 3D 感知视频生成模型的发展。

**核心机制**：CineMaster 将用户指定的 3D 边界框和摄像机运动渲染为投影深度图，通过语义布局注入网络（Semantic Layout ControlNet）和摄像机适配器（Camera Adapter）分别注入预训练的文本到视频扩散模型，从而解除物体运动与摄像机运动之间的歧义，实现 3D 感知的联合控制。

### 关键创新点（Changed Slots）

1. **控制信号来源**：从依赖已有视频提取或二维平面条件图，转变为用户通过交互式 3D 场景编辑直接生成 3D 感知条件信号（投影深度图 + 摄像机轨迹 + 语义标签）。
2. **物体控制维度**：从二维边界框/轨迹（2D）升级为三维边界框（3D），用户可自由调整边界框在 3D 场景中的尺寸和位置。
3. **摄像机运动注入**：从简单 Fourier 嵌入或点追踪，升级为逐 DiT 块的摄像机适配器，显式注入 $3 \times 3$ 旋转矩阵和 $3 \times 1$ 平移矩阵序列。

### 框架流程

CineMaster 分两阶段运作（Figure 2）：

![[assets/figures/papers/paper_list_l4_http_arxiv_org_abs_2502_08639v1/figures/002_Figure_2.jpg]]
*Figure 2: Overview of CineMaster. CineMaster consists of two stages. First, we present an interactive workflow that allows users to intuitively manipulate the objects and camera in a 3D-native manner. Then the control signals are rendered from the 3D engine and fed into a text-to-video diffusion model, guiding the generation of user-intended video content*

- **Stage 1：交互式 3D 工作流**（基于 Blender）。用户交互式放置 3D 边界框并定义摄像机运动，渲染引擎输出投影深度图和摄像机轨迹作为条件信号。
- **Stage 2：条件视频生成**。以预训练的文本到视频扩散模型（含 3D VAE、T5 编码器、Transformer 潜空间扩散模型）为基础，通过以下两个模块注入条件（Figure 3）：
  - **Semantic Layout ControlNet**：语义注入器（Semantic Injector）融合投影深度图与逐实体类别标签，经 DiT-based ControlNet 处理后加至基础模型隐状态，控制空间布局。
  - **Camera Adapter**：将摄像机姿态序列 $\mathbf{RT} = \{\mathbf{RT}_0, \mathbf{RT}_1, \ldots, \mathbf{RT}_{F-1}\} \in \mathbb{R}^{F \times 12}$（每个姿态由 $3 \times 3$ 旋转矩阵和 $3 \times 1$ 平移矩阵展平为 12 维）通过 MLP 对齐维度后，以残差方式注入各 DiT 块的隐状态，经自注意力模块实现摄像机运动控制。

![[assets/figures/papers/paper_list_l4_http_arxiv_org_abs_2502_08639v1/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the network architecture. We design a Semantic Layout ControlNet which consists of a semantic injector and a DiTbased ControlNet. Semantic injector fuses the 3D spatial layout and class label conditions. The DiT-based ControlNet further represents the fused features and adds to the hidden states of the base model. Meanwhile, we inject the camera trajectories by the camera adapter to achieve joint control over object motion and camera motion*

### 关键公式

模型基于 Rectified Flow 框架，前向过程定义干净数据 $z_0$ 与噪声 $\epsilon$ 的线性插值：

$$z_t = (1 - t) z_0 + t \epsilon$$

去噪过程由参数化速度 $v_\Theta$ 描述的 ODE 驱动：

$$d z_t = v_\Theta(z_t, t, c_{text}) dt$$

训练损失为条件流匹配损失，回归速度以匹配 $t=1$ 与 $t=0$ 之间的差：

$$\mathcal{L}_{LCM} = \mathbb{E}_{t, \epsilon \sim \mathcal{N}(0, \mathbf{I}), z_0} \left[ \| (z_1 - z_0) - v_\Theta(z_t, t, c_{text}) \|_2^2 \right]$$

### 数据标注流水线

为支撑训练，论文提出自动化标注流水线（Figure 4），从视频中提取 3D 边界框、类别标签和摄像机姿态，包含四步：实例分割 → 深度估计（DepthAnything V2）→ 逆投影计算 3D 点云与最小体积包围盒 → 实体追踪与逐帧 3D 框调整，最终将整个 3D 场景投影为深度图。需注意，该流水线精度受限于现成模型性能，可能引入数据噪声。

![[assets/figures/papers/paper_list_l4_http_arxiv_org_abs_2502_08639v1/figures/004_Figure_4.jpg]]
*Figure 4: Dataset Labeling Pipeline. We propose a data labeling pipeline to extract 3D bounding boxes, class labels and camera poses from videos. Our pipeline consists of four steps: 1) Instance Segmentation: Obtain instance segmentation results from the foreground in videos. 2) Depth Estimation: Produce metric depth maps using DepthAnything V2. 3) 3D Point Cloud and Box Calculation: Identify the frame with the largest mask for each entity and compute the 3D point cloud of each entity through inverse projection. Then, use the minimum volume method to calculate the 3D bounding box for each entity. 4) Entity Tracking and 3D Box Adjustment: Access the point tracking results of each entity and calculate...*

**证据强度**：消融实验（Table 2）确认 Semantic Layout ControlNet 与 Camera Adapter 的联合训练在所有指标上取得最优结果，置信度高。

## 实验与关键发现

CineMaster 的核心实验目标在于验证两个关键能力：**三维感知的物体布局控制**与**摄像机运动解耦**。实验设计围绕以下维度展开：物体放置精度（mIoU）、运动轨迹距离（Traj-D）、视频生成质量（FVD、FID）以及文本对齐度（CLIP-T）。

### 主结果：三维控制能力的量化优势

在综合基准测试中，CineMaster 在所有五项指标上均显著超越现有 SOTA 方法（Table 1）。具体而言：

![[assets/figures/papers/paper_list_l4_http_arxiv_org_abs_2502_08639v1/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparisons with baselines. ↑ indicates higher is better, while ↓ indicates that lower is better. The best result is shown in bold. Our CineMaster outperforms previous SOTA baselines on all metrics*

- **mIoU 达 0.551**，表明投影深度图引导的语义布局控制网络能够精确地将用户指定的三维边界框映射到生成视频中的物体位置，相较依赖二维平面条件图的基线方法有本质提升。
- **Traj-D 降至 66.29**，说明摄像机适配器注入的显式旋转-平移矩阵有效解耦了物体运动与摄像机运动，而 MotionCtrl（Wang et al., arXiv 2023）和 Direct-A-Video（Yang et al., ACM SIGGRAPH 2024）等二维控制方法在此指标上表现较差。
- **FVD 1530.9 与 FID 175.9** 均为最优，证明三维条件信号的引入并未损害视频生成质量，反而通过更精确的空间约束提升了帧间一致性与视觉保真度。
- **CLIP-T 0.321** 为最高，表明语义标签注入机制在强化空间控制的同时保持了文本语义对齐。

**证据强度**：Table 1 提供了完整的数值对比，置信度较高（0.85）。需注意，论文未报告统计显著性检验（如标准差或 p 值），因此各指标的优势幅度是否具有统计意义尚需手动验证。

### 消融实验：联合训练范式的决定性作用

论文通过消融实验系统评估了训练策略对性能的影响（Table 2），核心发现是：**Semantic Layout ControlNet 与 Camera Adapter 的联合训练（Joint Train）在所有指标上均取得最优结果**。

![[assets/figures/papers/paper_list_l4_http_arxiv_org_abs_2502_08639v1/figures/007_Table_2.jpg]]
*Table 2: Ablation study for training paradigms. Details of each setting are introduced in Sec 4.3. Overall, the setting of “Joint Train” (our final version) achieves the best performance on all metrics than other variants*

这一结果揭示了因果机制：摄像机运动与物体运动在潜空间中存在耦合，若分阶段独立训练各控制模块，模型难以学习到二者的联合分布。联合训练通过同时优化空间布局注入与摄像机姿态注入，使扩散模型能够在去噪过程中协调两种运动信号，从而避免物体与背景之间的运动不一致。

**证据强度**：置信度 0.95，Table 2 提供了清晰的数值支撑。但论文未展示其他消融维度（如语义注入器架构变体、摄像机适配器放置层数等）的实验结果，这些细节的缺失限制了对模块设计的深入理解。

### 定性分析：运动解耦的可视化验证

Figure 5 展示了三种典型场景的定性对比：
- **物体运动 + 静态摄像机**：CineMaster 能保持物体在三维空间中的轨迹一致性，而基线方法常出现物体漂移或形变。
- **静态物体 + 摄像机运动（Pan Up + Zoom In）**：基线方法难以维持物体位置不变，CineMaster 则通过摄像机适配器精确复现了镜头运动。
- **物体运动 + 摄像机运动（Spin Left）**：这是最具挑战性的场景，CineMaster 成功解耦了两种运动，避免了基线方法中常见的运动混淆伪影。

### 失败模式与适用边界

论文明确指出的局限性构成重要的失败模式分析：

1. **三维边界框朝向控制不完整**：由于缺乏可靠的开放集物体姿态估计模型，当前系统无法精确控制物体的旋转方向。这意味着用户只能指定物体的空间位置与尺寸，而无法像真正的三维导演工具那样操控物体的朝向——这是从“位置控制”到“姿态控制”的关键能力缺口。

2. **自动标注流水线的噪声传播**：数据集的 3D 边界框与摄像机轨迹依赖于 DepthAnything V2、GroundingDINO 等现成模型的输出。这些模型的估计误差会通过标注流水线（Figure 4）累积传播，可能导致训练数据中的空间标注不准确，进而影响模型对三维布局的精确建模能力。论文未量化这种噪声对最终指标的影响程度，这是评估结果可信度时需要保留的审慎空间。

3. **物理交互缺失**：当前框架仅控制运动学层面的物体位置与摄像机轨迹，不支持物体形变、碰撞响应等物理模拟。这限制了其在需要真实物理交互的电影级场景中的应用广度。

## 定位与知识库关联

CineMaster 的核心定位在于将文本到视频生成的控制范式从**二维平面约束**推进到**三维感知交互**，其本质差异体现在控制信号来源、运动解耦机制和数据集构建三个维度。

**与现有可控视频生成的本质差异**

现有方法如 **MotionCtrl**（Wang et al., arXiv 2023）和 **Direct-A-Video**（Yang et al., ACM SIGGRAPH 2024）均依赖二维条件图——前者通过点轨迹控制物体运动，后者使用二维边界框序列配合傅里叶嵌入控制摄像机。这些方法面临一个根本性瓶颈：二维投影无法区分物体自身运动与摄像机运动，二者在图像平面上产生歧义。CineMaster 通过引入三维边界框和显式摄像机旋转/平移矩阵，在条件信号层面实现了**运动源头的解耦**——物体在三维空间中的位移与摄像机视角变化被独立编码，从而允许模型学习分离的运动表征。这一设计使得用户能够像电影导演一样，分别操控“演员走位”与“镜头调度”，而非只能提供模糊的二维轨迹。

**知识库挂载点**

CineMaster 的技术脉络可挂载到以下知识节点：

1. **三维条件生成**：继承 **LooseControl**（Bhat et al., 2024）使用三维边界框作为场景表示的思想，但将其从单图生成扩展到视频生成，并增加了摄像机轨迹控制维度。
2. **扩散模型条件注入**：Semantic Layout ControlNet 的设计延续了 **ControlNet**（Zhang et al., ICCV 2023）的零卷积残差注入范式，但将其适配到 DiT（Diffusion Transformer）架构，并设计了语义注入器以融合深度图和类别标签。
3. **摄像机运动控制**：区别于 Direct-A-Video 的傅里叶嵌入方案，Camera Adapter 采用逐 DiT 块注入旋转/平移矩阵的方式，与 **AnimateDiff**（Guo et al., 2024）的运动适配器思路相似，但面向的是显式摄像机参数而非通用运动模式。
4. **自动化标注流水线**：利用 **DepthAnything V2**（Yang et al., 2024）进行深度估计、**GroundingDINO** 进行开放集检测、**CoTracker** 进行点追踪，构建了从视频到三维标注的自动化流程，填补了大规模三维感知视频数据集的空白。

**适用边界**

CineMaster 的适用场景聚焦于需要**精确空间布局和摄像机运动控制**的电影级视频生成，其边界受以下因素制约：

- **物体朝向控制不完整**：由于缺乏可靠的开放集物体姿态估计模型，当前系统仅支持三维边界框的位置和尺寸调整，无法精确控制物体的旋转朝向。这限制了需要精细物体姿态的场景（如人物特定角度、车辆转向等）。
- **标注噪声容忍度**：自动标注流水线的精度受限于现成模型性能，深度估计误差和分割不准确会引入数据集噪声，可能影响模型在边界情况下的生成质量。
- **交互式工作流的实时性**：当前两阶段设计（3D 编辑→离线生成）尚未与实时反馈结合，迭代效率受限于扩散模型的推理速度。

**后续启发**

CineMaster 为以下方向提供了探索基础：

1. **开放集物体姿态估计**：解锁三维边界框的完整方向控制，需要研究不依赖类别先验的通用物体姿态估计方法，这是实现完全三维感知控制的关键缺口。
2. **物理属性扩展**：当前仅控制物体的刚体运动，未来可将形变、碰撞、材质等物理属性纳入交互工作流，进一步提升创作自由度。
3. **实时交互生成**：将三维场景编辑与视频生成解耦为异步流程，或探索一致性模型等加速方案，有望实现“所见即所得”的实时导演体验。
4. **多模态条件融合**：当前仅使用深度图和摄像机参数，未来可融入法线图、光流、语义分割图等多模态几何线索，增强空间控制的精细度。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/CineMaster_A_3D_Aware_and_Controllable_Framework_for_Cinematic_Text_to_Video_Generation.pdf]]