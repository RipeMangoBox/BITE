---
title: "Gallant: Voxel Grid-based Humanoid Locomotion and Local-navigation across 3-D Constrained Terrains"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Gallant_Voxel_Grid_based_Humanoid_Locomotion_and_Local_navigation_across_3_D_Constrained_Terrains.pdf
project_link: null
code_link: "https://github.com/traveller59/"
aliases:
- Gallant
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 使用基于LiDAR的体素网格作为感知表示，保留完整的三维场景结构；并通过将z轴作为通道的2D CNN高效处理体素网格，使策略能直接利用三维结构信息进行全身控制。
primary_logic: 通过高保真LiDAR仿真、体素网格感知和轻量级2D CNN的端到端训练，单个策略即可泛化到包含地面、横向和顶部障碍物的多种复杂三维地形，并首次在人形机器人上实现超过90%的楼梯和平台穿越成功率。
claims:
- 在Ceiling地形上，Gallant成功率84.3%，而仅用高程图的基线仅为5.3%
- 移除对动态物体（自身连杆）的LiDAR扫描导致成功率从84.3%降至28.4%
- 无LiDAR域随机化（NoDR）的版本在真机测试中成功率显著下降
- z-grouped 2D CNN在推理延迟和训练效率上优于稀疏3D CNN，保持了较高成功率
---

# Gallant: Voxel Grid-based Humanoid Locomotion and Local-navigation across 3-D Constrained Terrains

> [!tip] 核心洞察
> 通过高保真LiDAR仿真、体素网格感知和轻量级2D CNN的端到端训练，单个策略即可泛化到包含地面、横向和顶部障碍物的多种复杂三维地形，并首次在人形机器人上实现超过90%的楼梯和平台穿越成功率。

| 字段 | 内容 |
|------|------|
| 中文题名 | Gallant: 基于体素网格的人形机器人在三维受限地形中的行走与局部导航 |
| 英文题名 | Gallant: Voxel Grid-based Humanoid Locomotion and Local-navigation across 3-D Constrained Terrains |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Ben_Gallant_Voxel_Grid-based_Humanoid_Locomotion_and_Local-navigation_across_3-D_Constrained_CVPR_2026_paper.html) · [Code](https://github.com/traveller59/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Gallant |
| Dataset | Ceiling, Stairs and Platform |

> [!tip] 效果简介
> - Ceiling (simulation) 上，Success rate (%) 84.3 ± 0.7 (Gallant) vs 5.3 ± 2.0 (Only-Height-Map) (+79.0%)；Success rate (%) 84.3 ± 0.7 (Gallant) vs 28.4 ± 2.4 (w/o self-scan) (+55.9%)。
> - Stairs and Platform (real-world) 上，Success rate over 90% vs prior methods (elevation/depth) not reaching 90% (N/A)。

## 概要

### 问题瓶颈

人形机器人在三维受限地形（如楼梯、低矮天花板、横向障碍物、多层平台）中的自主行走与局部导航面临两大核心瓶颈。其一，现有感知行走方法普遍依赖**高程图**（elevation map）或深度图像，它们仅提供局部扁平的二维半视图，无法捕捉完整的三维结构——例如横向障碍物的垂直面、天花板的高度限制、多层支撑面的空间关系。其二，LiDAR传感器的高延迟（>100 ms）严重制约了机器人的预判与实时反应能力，导致在部分地形上成功率停滞。这些瓶颈使得已有工作在包含顶部障碍物（如天花板）的场景中几乎完全失效。

### 核心方法

Gallant 提出了一套端到端的感知-控制框架，以**体素网格**（voxel grid）替代高程图作为感知表示，从根本上保留了三维场景的完整结构信息。其方法包含三个关键设计：

1. **高保真LiDAR仿真与体素化**：构建可模拟传感器噪声、延迟，并能扫描动态物体（包括机器人自身连杆）的LiDAR仿真管线，将点云实时转换为机器人坐标系下的体素网格。
2. **z-grouped 2D CNN感知模块**：将体素网格的高度轴作为卷积通道，沿水平面执行2D卷积，在保持垂直结构信息的同时大幅降低计算开销，在推理效率与表示能力之间取得有利平衡。
3. **课程式训练与域随机化**：在八类代表性三维地形上以渐进难度进行课程训练，并通过LiDAR域随机化（姿态扰动、噪声、延迟、缺失体素）实现零样本sim-to-real迁移。

### 关键结论

Gallant 首次在人形机器人上以**单一策略**泛化到包含地面、横向和顶部障碍物的多种复杂三维地形，并在仿真与真机测试中取得突破性表现：

- **天花板地形**：成功率84.3%，而仅使用高程图的基线仅为5.3%（Table 3(c)）。
- **楼梯与平台**：真机测试成功率超过90%，为已有高程图/深度图方法所未达到的水平（Abstract, Fig. 7）。
- **消融验证**：移除对自身连杆的LiDAR扫描使天花板地形成功率从84.3%骤降至28.4%（Table 3(a)）；移除LiDAR域随机化导致真机成功率大幅下降（Fig. 6）；z-grouped 2D CNN在保持较高成功率的同时，推理延迟显著优于稀疏3D CNN（Table 3(b), Fig. 5(d)）。

### 方法谱系与知识库定位

在感知行走方法的谱系中，Gallant 将感知表示从**高程图**（如 **Long et al., ICRA 2025**；**Wang et al. (BeamDojo), arXiv 2025**；**Ren et al., arXiv 2025**）和**深度图像**（如 **Zhuang et al., arXiv 2024** 的人形跑酷方法）推进到**体素网格**，从而首次系统性地覆盖了地面、横向与顶部三类障碍物。与基于点云的碰撞避免方法（**Wang et al., arXiv 2025**）相比，Gallant 通过体素化聚合原始点云并采用轻量2D CNN处理，在保留三维结构的同时降低了维度与计算负担。其LiDAR仿真管线与域随机化策略为感知行走的sim-to-real迁移提供了可复用的工程范式，而z-grouped 2D CNN的设计则为稀疏三维感知的高效处理提供了新的架构选项。



### 人形机器人的三维受限环境行走难题

人形机器人因其类人的身体结构，具备在人类环境中执行复杂任务的潜力。然而，在真实的三维受限地形中实现稳健的行走与局部导航，仍然是一个开放挑战。这些地形不仅包含传统的地面起伏（如楼梯、平台），还涉及横向障碍物（如狭窄门框）和顶部障碍物（如低矮天花板），要求机器人具备完整的三维空间感知能力。

### 现有感知方法的瓶颈

当前基于感知的人形行走方法在感知表示上存在根本性局限。主流方法依赖**高程图**（Elevation Map）或**深度图像**（Depth Image）作为环境表示。高程图将三维场景压缩为二维半视图（2.5D），仅记录每个水平位置上的最高点，这导致两个关键问题：

1. **垂直结构信息的丢失**：高程图无法表示多层结构、天花板高度、横向悬垂物等完整的三维几何。当机器人需要匍匐通过低矮天花板时，高程图完全无法感知头顶的障碍物。
2. **横向障碍物感知不足**：深度图像虽然能捕捉部分前方结构，但视场角有限，且同样缺乏对机器人自身周围完整三维结构的建模。

此外，现有方法中使用的LiDAR传感器存在显著的**延迟问题**（通常超过100 ms），这限制了机器人的预判和实时反应能力。在需要精确落脚的步石柱（Pile）等地形上，这种延迟导致成功率停滞在约80%。

### 本文动机

针对上述瓶颈，本文提出**Gallant**——一个基于体素网格（Voxel Grid）的人形机器人行走与局部导航框架。核心动机在于：

- **保留完整三维结构**：用体素网格替代高程图，将LiDAR点云转化为保留多层级场景结构的感知表示，使策略能够同时推理地面、横向和顶部障碍物。
- **高效的三维感知处理**：通过将z轴作为通道的2D CNN处理体素网格，在计算效率与表示能力之间取得平衡，避免稀疏3D CNN的高延迟问题。
- **端到端sim-to-real迁移**：通过高保真LiDAR仿真（包含对机器人自身连杆的动态扫描）和域随机化，实现从仿真到真机的零样本迁移，首次在人形机器人上实现超过90%的楼梯攀爬和平台穿越成功率。



## 核心方法与创新机理

Gallant 的核心创新在于**感知表示的范式转换**：从传统高程图（Elevation Map）或深度图像切换到基于 LiDAR 点云的**体素网格（Voxel Grid）**，并配套设计了高效的感知网络与高保真仿真管线，使单一策略能够泛化到包含地面、横向和顶部障碍物的多种复杂三维地形。

### 关键创新点

**1. 感知表示：从 2.5D 高程图到完整 3D 体素网格**

现有感知行走方法普遍依赖高程图（如 **Long et al., ICRA 2025**；**Wang et al., arXiv 2025** 的 BeamDojo；**Ren et al., arXiv 2025**）或深度图像（如 **Zhuang et al., arXiv 2024** 的人形跑酷方法），这些表示仅提供局部扁平的 2.5 维视图，无法捕捉完整的三维结构——特别是横向障碍物、天花板高度和多层结构。这一瓶颈直接导致现有方法在 Ceiling 等地形上成功率停滞。

Gallant 采用以机器人为中心的体素网格作为感知表示，保留多层场景结构，聚合原始点云以降低维度，同时覆盖大视场角。这一改变使策略能够“看到”头顶的障碍物和侧面的狭缝，从而做出弯腰、侧身等全身协调动作。

**2. 感知网络：z 轴为通道的 2D CNN**

体素网格的三维特性对网络设计提出挑战。Gallant 提出将高度维（z 轴）作为卷积通道的 **z-grouped 2D CNN**，在 xy 平面上执行标准 2D 卷积，通过通道混合保留垂直结构信息。与标准 3D CNN 相比，该设计将计算和内存开销降低约 $k$ 倍（$k$ 为卷积核尺寸），同时利用高度优化的密集 2D 算子实现高效推理（见 Table 3(b), Fig. 5(d)）。消融实验表明，稀疏 3D CNN 虽取得略高成功率，但推理延迟显著增大，2D CNN 在效率与性能间取得最佳平衡。

**3. LiDAR 仿真：动态物体扫描与域随机化**

传统 LiDAR 仿真仅扫描静态场景，忽略机器人自身连杆的反射。Gallant 开发了**高保真动态 LiDAR 仿真管线**，基于 NVIDIA Warp 实现轻量级射线投射-体素化，能够实时扫描机器人自身的运动连杆。消融实验表明，移除对动态物体的扫描导致 Ceiling 地形成功率从 **84.3% 骤降至 28.4%**（Table 3(a)）——机器人无法感知自己弯腰时背部是否仍高于天花板。

此外，仿真管线引入了系统的**域随机化**：传感器姿态扰动、噪声、延迟和缺失体素。缺少域随机化的版本（NoDR）在真机测试中成功率大幅下降（Fig. 6），验证了其对 sim-to-real 迁移的关键作用。

**4. 非对称 Actor-Critic 架构**

Gallant 采用非对称特权信息设计：Actor 仅接收体素网格感知，而 Critic 额外接收高程图作为特权信息。这一设计改善了训练中的信用分配，使 Gallant 成功率高于仅使用体素网格的版本（Only-Voxel-Grid），同时保持 Actor 在部署时对高程图的零依赖（Sec. 4.2.3）。

**5. 目标到达奖励替代速度跟踪**

传统方法使用速度跟踪奖励，Gallant 将其替换为**目标到达奖励** $r_{\mathrm{reach}} = \frac{1}{1 + \|\mathbf{P}_t\|^2} \cdot \frac{\|(t > T - T_r)}{T_r}$，在回合最后 2 秒内生效，鼓励机器人靠近目标而非单纯维持速度。这一设计使策略能够自主探索合理的行走轨迹，而非被速度指令约束。

### 创新总结

| 维度 | 基线方法 | Gallant 创新 |
|------|---------|-------------|
| 感知表示 | 高程图 / 深度图 (2.5D) | 体素网格 (完整 3D) |
| 感知网络 | 轻量 MLP | z-grouped 2D CNN |
| LiDAR 仿真 | 仅静态场景 | 动态物体扫描 + 域随机化 |
| Critic 信息 | 通用 | 高程图作为特权信息 |
| 奖励函数 | 速度跟踪 | 目标到达奖励 |

这些创新协同作用，使 Gallant 首次在人形机器人上实现超过 90% 的楼梯和平台穿越成功率，并在 Ceiling 地形上取得 **84.3%** 的成功率，而仅用高程图的基线仅为 **5.3%**（Table 3(c)）。



Gallant 的完整 pipeline 由五个核心模块串联构成：**LiDAR 仿真与体素化** → **z-grouped 2D CNN 感知模块** → **本体感觉融合** → **MLP Actor 全身控制** → **PPO 端到端训练框架**。整个系统的信息流如图 Figure 2 所示。

![[assets/figures/papers/paper_list_l1025_https_openaccess_thecvf_com_content_CVPR2026_html_Ben_Gallant_Voxel_Grid/figures/003_Figure_2.jpg]]
*Figure 2: Method Overview. (a) Curriculum-based training over 8 representative terrains enhances generalization, and realistic voxel path alignment achieved via efficient LiDAR simulation with domain-randomized latency and noise. (b) A 2D CNN-based perceptual module processes voxel grid using the z-dimension as input channels, balancing efficiency and representation capability. (c) A latent-aware PPO policy enables zero-shot sim-to-real transfer across diverse obstacles, including ground, lateral, and overhead challenges*

### 输入：观测向量

时刻 $t$ 的观测向量 $o_t$ 包含以下分量（见 Section 3.1）：

$$o_t = ( \mathbf{P}_t, \mathbf{T}_{\mathrm{elapse},t}, \mathbf{T}_{\mathrm{left},t}, a_{t-4:t-1}, \omega_{t-5:t}, g_{t-5:t}, q_{t-5:t}, \dot{q}_{t-5:t}, \mathrm{Voxel\_Grid}_t, v_t, \mathrm{HeightMap}_t )$$

其中 $\mathbf{P}_t$ 为目标相对位置，$\mathbf{T}_{\mathrm{elapse},t}$ 和 $\mathbf{T}_{\mathrm{left},t}$ 为耗时与剩余时间，$a_{t-4:t-1}$ 为历史动作，$\omega_{t-5:t}$ 为角速度，$g_{t-5:t}$ 为重力方向投影，$q_{t-5:t}$ 和 $\dot{q}_{t-5:t}$ 为关节位置与速度，$\mathrm{Voxel\_Grid}_t$ 为体素网格感知输入，$v_t$ 为线性速度。$\mathrm{HeightMap}_t$ 作为**特权信息**仅提供给 Critic 网络，Actor 不直接使用。

### 模块 1：LiDAR 仿真与体素化

基于 NVIDIA Warp（Macklin, 2022）实现的并行化射线投射-体素化管线（Section 3.2），从 LiDAR 点云生成以机器人为中心的体素网格。关键设计包括：

- **动态物体扫描**：仿真管线不仅扫描静态地形，还扫描机器人自身的运动连杆，使体素网格包含机器人与环境之间的空间关系（如蹲伏时头部与天花板的距离）。
- **域随机化**：对 LiDAR 姿态扰动、测量噪声、延迟和缺失体素进行随机化，以缩小 sim-to-real 差距。
- **高效射线投射**：利用预计算的 BVH 在网格局部坐标系下进行射线投射，避免每步重建全局加速结构：

$$\operatorname{raycast}(TM, \mathbf{p}, \mathbf{d}) = T^{-1} \mathrm{raycast}(M, T^{-1} \mathbf{p}, R^{-1} \mathbf{d})$$

### 模块 2：z-grouped 2D CNN 感知模块

体素网格被组织为以 z 轴为通道维度的三维张量，然后通过 2D CNN 在 xy 平面上进行卷积（Section 3.3）：

$$Y_{o,v,u} = \sigma\left( \sum_{c=0}^{C-1} \sum_{\Delta v, \Delta u} \mathbf{W}_{o,c,\Delta v,\Delta u} \cdot X_{c,v+\Delta v,u+\Delta u} + b_o \right)$$

这一设计将 3D 卷积的计算量和内存开销降低了约 $k$ 倍（$k$ 为卷积核尺寸），同时通过通道混合保留了垂直结构信息。消融实验（Table 3(b)）表明，z-grouped 2D CNN 在推理延迟和训练效率上显著优于标准 3D CNN，成功率与稀疏 3D CNN 接近但延迟更低。

### 模块 3-4：本体感觉融合与 MLP Actor

感知模块提取的紧凑特征与关节状态、历史动作、时间信息等本体感觉拼接后，送入基于 MLP 的 Actor 网络，输出全身关节控制指令。Actor 与 Critic 共享特征提取层，但 Critic 额外接收高程图作为特权信息以改善信用分配。

### 模块 5：PPO 训练框架与课程式地形

整个 pipeline 通过 PPO 算法端到端优化。奖励函数以**目标到达奖励**替代传统速度跟踪奖励（Section 3.1）：

$$r_{\mathrm{reach}} = \frac{1}{1 + \|\mathbf{P}_t\|^2} \cdot \frac{\|(t > T - T_r)}{T_r} \quad (T_r = 2s)$$

训练采用课程式策略，在 8 种代表性三维地形（楼梯、天花板、平台、间隙、步石柱、门洞、横向障碍等）上渐进增加难度。地形参数按难度标量 $s \in [0, 1]$ 线性插值：

$${\bf p}_{\tau}(s) = (1 - s) {\bf p}_{\tau}^{\mathrm{min}} + s {\bf p}_{\tau}^{\mathrm{max}}$$

### 关键瓶颈与因果机制

现有方法（如 Long et al., ICRA 2025; Wang et al., arXiv 2025）依赖高程图或深度图像，仅提供局部扁平的 2.5D 视图，无法捕捉横向障碍物、天花板高度、多层结构等完整 3D 信息。Gallant 通过体素网格保留三维场景结构，并利用 z-grouped 2D CNN 高效处理，使单一策略能泛化到包含地面、横向和顶部障碍物的多种复杂地形。**决定性证据**：在 Ceiling 地形上，Gallant 成功率 84.3%，而仅用高程图的基线仅为 5.3%（Table 3(c)）；移除对自身连杆的 LiDAR 扫描后，成功率骤降至 28.4%（Table 3(a)），验证了动态物体感知和完整 3D 表示的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l1025_https_openaccess_thecvf_com_content_CVPR2026_html_Ben_Gallant_Voxel_Grid/figures/005_Figure_3.jpg]]
*Figure 3: Terrain types used to train robots in simulation*



### 整体架构概览

Gallant 的系统架构由三个核心模块构成：(i) 并行化 LiDAR 仿真与体素化管线（Sec. 3.2），(ii) 轻量级 z-as-channel 2D CNN 感知模块（Sec. 3.3），(iii) 基于 PPO 的 actor-critic 强化学习训练框架（Sec. 3.1）。系统整体流程如 Figure 2 所示。

### 观测向量与奖励函数

时刻 $t$ 的观测向量定义为：

$$o_t = ( \mathbf{P}_t, \mathbf{T}_{\mathrm{elapse},t}, \mathbf{T}_{\mathrm{left},t}, a_{t-4:t-1}, \omega_{t-5:t}, g_{t-5:t}, q_{t-5:t}, \dot{q}_{t-5:t}, \mathrm{Voxel\_Grid}_t, v_t, \mathrm{HeightMap}_t )$$

其中 $\mathbf{P}_t$ 为机器人基座相对于目标的位置，$\mathbf{T}_{\mathrm{elapse},t}$ 和 $\mathbf{T}_{\mathrm{left},t}$ 分别为已用时和剩余时间，$a_{t-4:t-1}$ 为历史动作，$\omega_{t-5:t}$ 为历史角速度，$g_{t-5:t}$ 为历史重力方向投影，$q_{t-5:t}$ 和 $\dot{q}_{t-5:t}$ 为关节位置和速度历史，$\mathrm{Voxel\_Grid}_t$ 为体素网格感知，$v_t$ 为指令速度缩放因子，$\mathrm{HeightMap}_t$ 为仅 critic 可访问的特权信息。

奖励函数遵循 **Ben et al. ** 的框架，但将速度跟踪奖励替换为目标到达奖励：

$$r_{\mathrm{reach}} = \frac{1}{1 + \|\mathbf{P}_t\|^2} \cdot \frac{\|(t > T - T_r)}{T_r} \quad (T_r = 2s)$$

该奖励仅在 episode 的最后 2 秒内生效，鼓励机器人靠近目标，同时为轨迹探索留出充足时间。

### LiDAR 仿真与体素化管线

Gallant 基于 **NVIDIA Warp**（Macklin, 2022）实现了轻量级高效的射线投射-体素化管线。核心创新在于利用网格局部坐标系下的预计算 BVH（包围体层次结构）进行射线投射，避免每步重建全局 BVH：

$$\operatorname{raycast}(TM, \mathbf{p}, \mathbf{d}) = T^{-1} \mathrm{raycast}(M, T^{-1} \mathbf{p}, R^{-1} \mathbf{d})$$

其中 $M$ 为网格，$T$ 为变换矩阵，$\mathbf{p}$ 为射线原点，$\mathbf{d}$ 为射线方向，$R$ 为旋转分量。该变换使得射线投射可在每个网格的局部坐标系中执行，大幅降低计算开销。

LiDAR 仿真管线模拟了传感器噪声与延迟，并支持对动态物体（包括机器人自身运动连杆）的真实扫描。仿真中应用了域随机化，包括姿态扰动、噪声、延迟和缺失体素，这是实现 sim-to-real 零样本迁移的关键（消融实验见 Figure 6）。

### z-as-channel 2D CNN 感知模块

体素网格的核心处理方式是将 z 轴（高度）作为通道维度，沿 xy 平面执行 2D 卷积：

$$Y_{o,v,u} = \sigma\left( \sum_{c=0}^{C-1} \sum_{\Delta v, \Delta u} \mathbf{W}_{o,c,\Delta v,\Delta u} \cdot X_{c,v+\Delta v,u+\Delta u} + b_o \right)$$

其中 $X$ 为输入体素网格（通道维度为高度切片），$Y$ 为输出特征图，$\mathbf{W}$ 为卷积核，$b_o$ 为偏置，$\sigma$ 为激活函数。该设计将计算量和内存开销相较于 $k^3$ 的 3D 卷积核降低约 $k$ 倍，同时通过通道混合保留了垂直结构信息，在表征能力与计算效率之间取得了有利平衡。

消融实验（Table 3(b), Figure 5(d)）表明，稀疏 3D CNN 虽然成功率略高，但推理延迟显著增大；2D CNN 在效率与性能间达到最佳平衡，是感知模块的最优选择。

![[assets/figures/papers/paper_list_l1025_https_openaccess_thecvf_com_content_CVPR2026_html_Ben_Gallant_Voxel_Grid/figures/008_Figure_5.jpg]]
*Figure 5: Visualization of simulation ablation analyses. (a) The humanoid crouches to traverse under a low ceiling; (b) Voxel grid from LiDAR simulation that includes dynamic objects captures the robot’s own links; (c) LiDAR simulation restricted to static objects excludes robot links from the voxel grid; (d) Mean training iteration time for Gallant with different CNN-based perception modules*

### 课程式训练与地形生成

Gallant 采用课程式训练策略，地形难度随训练逐步递增。每种地形类型 $\tau$ 由难度标量 $s \in [0, 1]$ 参数化，地形生成参数通过线性插值确定：

$$\mathbf{p}_{\tau}(s) = (1 - s) \mathbf{p}_{\tau}^{\mathrm{min}} + s \mathbf{p}_{\tau}^{\mathrm{max}}$$

训练覆盖 8 种代表性地形类型（Figure 3），包括楼梯、平台、天花板、横向障碍、步石柱等，具体参数范围见 Table 2。



## 实验与关键发现

### 仿真主实验结果

Gallant在八类代表性三维受限地形上进行了系统性评估，并与多个基线方法进行对比。所有方法均训练4000个迭代，评估时进行5轮独立测试，每轮1000个回合，报告成功率均值与标准差。

**Table 3** 展示了完整的消融与对比结果。在**Ceiling（天花板）**地形上，Gallant取得了**84.3%**的成功率，而仅使用高程图（HeightMap）的基线仅为**5.3%**，差距高达79个百分点。这一结果直接验证了体素网格对顶部障碍物感知的必要性——高程图仅提供二维半视图，完全无法捕捉悬挂天花板的垂直结构信息。

在**Stairs（楼梯）**和**Platform（平台）**等经典地形上，Gallant的成功率均超过90%，首次在人形机器人上达到这一水平。相比之下，此前依赖高程图或深度图像的方法（如Long et al., ICRA 2025; Wang et al., arXiv 2025; Zhuang et al., arXiv 2024）在这些场景中尚未报告达到90%的成功率。

### 消融实验分析

#### 1. 动态物体扫描的必要性

移除对动态物体（即机器人自身连杆）的LiDAR扫描是影响最大的单一消融。如 **Table 3(a)** 所示，在Ceiling地形上，无自身扫描的变体（w/o-Self-Scan）成功率从84.3%骤降至**28.4%**。**Figure 5(b,c)** 直观展示了差异：包含动态扫描的体素网格能清晰捕捉机器人手臂、躯干等连杆的位置，使策略在低矮天花板下做出下蹲避让动作；而仅扫描静态场景时，体素网格缺失自身连杆信息，策略无法判断是否会发生碰撞。

![[assets/figures/papers/paper_list_l1025_https_openaccess_thecvf_com_content_CVPR2026_html_Ben_Gallant_Voxel_Grid/figures/006_Table_3.jpg]]
*Table 3: Simulation ablation results. We present a success rate comparison between Gallant and baselines on the eight representative terrains. The means and standard variation are reported across 5 evaluations, each with 1,000 testing episodes. Success rate is reported as a percentage (e.g., 90 means 90%). For each ablation setting, the best-performing value per metric on each terrain is highlighted in bold*

#### 2. 感知网络架构选择

**Table 3(b)** 对比了z-grouped 2D CNN与标准3D CNN、稀疏2D CNN、稀疏3D CNN的性能。稀疏3D CNN在部分地形上取得略高的成功率，但其推理延迟显著增大（**Figure 5(d)**）。z-grouped 2D CNN将z轴作为通道维度进行2D卷积，计算量和内存开销约为3D卷积核的$1/k$（$k$为核尺寸），同时通过通道混合保留了关键的垂直结构信息，在效率与性能之间取得最佳平衡。

#### 3. 感知表示对比

**Table 3(c)** 直接对比了体素网格与高程图的感知能力。仅使用高程图（Only-Height-Map）在Ceiling地形上几乎完全失败（5.3%），在Lateral Clutter（横向障碍物）地形上也表现不佳。这揭示了高程图的根本局限：它将三维场景压缩为二维高度场，丢失了横向悬垂、顶部遮挡等多层结构信息。

#### 4. 体素分辨率的影响

**Table 3(d)** 展示了体素分辨率对成功率的影响。5cm分辨率在覆盖范围与细节捕获之间取得最佳平衡。2.5cm分辨率虽然更精细，但成功率反而下降至59.0%——更小的体素意味着更稀疏的占用信号，可能导致有效信息密度不足。10cm分辨率也低于5cm，表明过粗的体素丢失了关键的局部几何细节。

#### 5. 域随机化与Sim-to-Real迁移

**Figure 6** 展示了真机测试中三种配置的成功次数对比（每种地形15次试验）。无LiDAR域随机化（NoDR）的版本在真机测试中成功率显著下降，验证了域随机化（姿态扰动、噪声、延迟、缺失体素）对sim-to-real迁移的关键作用。仅用高程图的变体在真机中也表现不佳，与仿真结果一致。

#### 6. Critic特权信息的非对称架构

Gallant的Actor仅接收体素网格作为感知输入，而Critic额外接收高程图作为特权信息。这种非对称架构在训练中改善了信用分配（credit assignment），使得Gallant的成功率高于Actor和Critic均仅使用体素网格的版本（Only-Voxel-Grid），验证了特权信息在RL训练中的价值。

### 真机验证

**Figure 7** 对比了Gallant在仿真与真机中的成功率。在楼梯和平台地形上，真机成功率均超过90%，与仿真结果高度一致，证明了体素网格感知和域随机化策略的有效sim-to-real迁移能力。**Figure 4** 展示了人形机器人在多种真实三维受限地形中的穿行效果，包括低矮天花板下蹲行、横向障碍物绕行、30cm高平台跨越、40cm间隙穿越以及20cm楼梯上下，所有部署均使用同一策略。

### 失败模式与局限

尽管Gallant在多数地形上表现优异，但在**Pile（步石柱）**地形上成功率停滞在约80%。分析表明，LiDAR的10Hz采样率和超过100ms的延迟限制了机器人的预先反应能力——在步石柱这类需要精确落足点选择的地形上，感知延迟导致策略无法及时调整步态。此外，在极窄通道或包含动态障碍物的场景中，当前策略仍有失败可能。未来需探索更低延迟的传感器（如高帧率深度相机或事件相机）或混合感知方案，以实现完全反应式策略。

### 补充图表

![[assets/figures/papers/paper_list_l1025_https_openaccess_thecvf_com_content_CVPR2026_html_Ben_Gallant_Voxel_Grid/figures/009_Figure_6.jpg]]
*Figure 6: Real-world traversal success times over 15 trials. Height Map uses elevation maps as perceptual representation; NoDR is Gallant without LiDAR domain randomization; Gallant denotes the full proposed pipeline. All methods are tested for 15 trials per terrain*

![[assets/figures/papers/paper_list_l1025_https_openaccess_thecvf_com_content_CVPR2026_html_Ben_Gallant_Voxel_Grid/figures/010_Figure_7.jpg]]
*Figure 7: Gallant success rate in simulation and real world*

![[assets/figures/papers/paper_list_l1025_https_openaccess_thecvf_com_content_CVPR2026_html_Ben_Gallant_Voxel_Grid/figures/007_Figure_4.jpg]]
*Figure 4: Humanoid robot traverses diverse 3D constrained terrains in both simulation and the real world. (a)Traversal across the eight simulated training terrain types. (b)Ducking under suspended ceiling obstacles. (c)Local navigation through lateral clutters. (d)Stepping onto a 30cm-high platform and crossing a 40cm gap. (e)Traversing pile-like stepping-stone terrain. (f)(g)Ascending and descending 20cm stairs. All deployments are based on the same policy*

![[assets/figures/papers/paper_list_l1025_https_openaccess_thecvf_com_content_CVPR2026_html_Ben_Gallant_Voxel_Grid/figures/002_Table_1.jpg]]
*Table 1: Comparison between gallant and previous methods. FoV in Solid Angles are computed by parameter of the used sensors*

![[assets/figures/papers/paper_list_l1025_https_openaccess_thecvf_com_content_CVPR2026_html_Ben_Gallant_Voxel_Grid/figures/004_Table_2.jpg]]
*Table 2: Parameters for generating curriculum training terrains*

![[assets/figures/papers/paper_list_l1025_https_openaccess_thecvf_com_content_CVPR2026_html_Ben_Gallant_Voxel_Grid/figures/001_Figure_1.jpg]]
*Figure 1: Overview. Gallant enables a single policy with voxel grids to traverse diverse 3D constrained terrains in real: (a) ascend and descend stairs, (b) pass doors and duck under ceilings, (c) step onto platforms and over gaps, and (d) cross stepping-stone pillars*



## 定位与知识库关联

### 感知行走的方法谱系

Gallant 处于**基于感知的人形机器人行走与局部导航**这一研究脉络中，其核心区分维度是**感知表示**的选择。现有方法可依此分为三个层级：

1. **高程图/深度图范式**：当前主流方法依赖高程图（Elevation Map）或深度图像作为感知输入，提供局部扁平的 2.5D 视图。代表性工作包括 **Long et al.**（ICRA 2025）基于高程图的行走方法，**Wang et al.**（BeamDojo, arXiv 2025）和 **Ren et al.**（arXiv 2025）的人形行走方法，以及 **Zhuang et al.**（arXiv 2024）基于深度图像的人形跑酷方法。这些方法在楼梯和平台等地形上取得进展，但因丢弃了完整的 3D 结构信息，无法感知横向障碍物、天花板高度和多层结构，在 Ceiling 等地形上成功率骤降至 5.3%（Table 3(c)）。

2. **点云范式**：**Wang et al.**（arXiv 2025）采用点云进行全向碰撞避免，保留了更多 3D 信息，但点云的非结构化特性增加了处理复杂度。

3. **体素网格范式（本工作）**：Gallant 提出以机器人坐标系下的体素网格作为感知表示，由 LiDAR 点云经体素化生成，完整保留多层场景结构。这一选择在 FoV 和障碍物覆盖类型上形成质变：高程图方法仅覆盖地面障碍物，而 Gallant 同时覆盖地面、横向和顶部障碍物（Table 1）。

### 感知网络设计的权衡空间

在体素网格的处理上，Gallant 探索了三个架构选项（Table 3(b), Fig. 5(d)）：

- **标准 3D CNN**：用 3D 卷积核处理体素网格，保留完整空间结构，但计算和显存开销大。
- **稀疏 3D CNN**：利用体素稀疏性，取得略高于 Gallant 的成功率，但推理延迟显著增大，不利于实时控制。
- **z-grouped 2D CNN（Gallant 采用）**：将 z 轴作为通道维度，沿 xy 平面做 2D 卷积。这一设计将计算量降低约 $k$ 倍（$k$ 为 3D 核尺寸），同时通过通道混合保留垂直结构信息，在效率与表征能力之间取得最佳平衡。

### 仿真到真实迁移的知识贡献

Gallant 的 sim-to-real 迁移能力建立在三个关键设计上：

1. **动态 LiDAR 仿真**：首次在行走策略训练中模拟对动态物体（包括机器人自身连杆）的 LiDAR 扫描。消融实验表明，移除自身扫描（w/o-Self-Scan）导致 Ceiling 地形成功率从 84.3% 降至 28.4%（Table 3(a)），因为策略无法感知自身与顶部障碍物的相对位置。

2. **LiDAR 域随机化**：对传感器姿态、噪声、延迟和缺失体素进行随机化。真机测试中，无域随机化版本（NoDR）的成功率显著下降（Fig. 6），验证了域随机化对迁移的必要性。

3. **非对称 Actor-Critic 架构**：Critic 接收高程图作为特权信息，Actor 仅使用体素网格。这一设计改善了训练中的信用分配，Gallant 成功率高于仅使用体素网格的版本（Only-Voxel-Grid, Sec. 4.2.3）。

### 适用边界与局限

1. **LiDAR 延迟瓶颈**：当前 LiDAR 工作频率为 10 Hz（延迟 > 100 ms），限制了机器人的预先反应能力。在步石柱（Pile）等需要快速精确落足的地形上，成功率停滞在约 80%，未能突破 90%。

2. **体素分辨率约束**：5 cm 分辨率在覆盖与细节间取得最佳平衡（Table 3(d)）；2.5 cm 分辨率反而导致成功率下降至 59.0%，可能因稀疏性增加和感受野受限。更精细的支撑面信息在当前框架下难以有效利用。

3. **动态障碍物与极窄通道**：当前策略尚未达到 100% 成功率，在极窄或动态障碍物场景中仍有失败可能。策略依赖静态体素网格的快照式感知，缺乏对障碍物运动的时间建模。

### 开放问题

1. **低延迟感知替代方案**：能否用高帧率深度相机或事件相机替代 LiDAR，实现完全反应式策略，将 Pile 等地形的成功率推向接近 100%？

2. **多传感器融合**：如何在不增加延迟的前提下融合 LiDAR 的远距离结构感知与深度相机的近距离高帧率信息，构建混合感知方案？

3. **更高分辨率体素的利用**：如何在保持低延迟的同时提高体素网格分辨率，以捕获更精细的支撑面信息（如步石柱的边缘）？

4. **时态感知扩展**：当前体素网格仅编码单帧空间信息，引入时态体素表示（如 4D 占用栅格）是否能使策略对动态障碍物做出预判性反应？



## 原文 PDF

![[paperPDFs/CVPR_2026/Gallant_Voxel_Grid_based_Humanoid_Locomotion_and_Local_navigation_across_3_D_Constrained_Terrains.pdf]]
