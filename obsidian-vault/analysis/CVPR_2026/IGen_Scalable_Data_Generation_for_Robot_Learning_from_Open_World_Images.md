---
title: "IGen: Scalable Data Generation for Robot Learning from Open-World Images"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/IGen_Scalable_Data_Generation_for_Robot_Learning_from_Open_World_Images.pdf
project_link: "https://chenghaogu.github.io/IGen/"
code_link: null
aliases:
- IGen
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过将非结构化2D图像转化为包含3D点云与空间关键点的结构化场景表征，并引入视觉语言模型（VLM）进行任务推理与动作规划，IGen能够在无需人工标注的情况下从单张图像自动生成可执行的动作序列与视觉观测。
primary_logic: 采用基于实时点云渲染的仿真自由合成方案：利用VLM规划得到的末端执行器SE(3)轨迹，对物体点云施加刚体变换，从而动态合成与动作严格同步的场景点云序列，并逐帧渲染生成视觉观测，实现了从开放世界图像到机器人训练数据的高效转化。
claims:
- 仅使用IGen生成数据训练的策略在多个真实机器人操作任务上的成功率可达66.7%，超过同等时间预算下遥操作数据训练的策略（58.3%）。
- "在Simpler数据集上，IGen重建的场景视觉相似度（LPIPS1: 0.063 vs 0.324）大幅优于Real-to-Sim方法。"
- 在DreamGen Bench上，IGen生成的行为在指令遵循与物理对齐指标上均显著优于TesserAct和Cosmos-Predict2。
- Simpler场景重建 上 PSNR↑ (平均) = 27.0040
---

# IGen: Scalable Data Generation for Robot Learning from Open-World Images

> [!tip] 核心洞察
> 采用基于实时点云渲染的仿真自由合成方案：利用VLM规划得到的末端执行器SE(3)轨迹，对物体点云施加刚体变换，从而动态合成与动作严格同步的场景点云序列，并逐帧渲染生成视觉观测，实现了从开放世界图像到机器人训练数据的高效转化。

| 字段 | 内容 |
|------|------|
| 中文题名 | IGen：面向机器人学习的大规模开放世界图像数据生成 |
| 英文题名 | IGen: Scalable Data Generation for Robot Learning from Open-World Images |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.01773) · [Project](https://chenghaogu.github.io/IGen/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | IGen |
| Dataset | Simpler场景重建, DreamGen Bench |

> [!tip] 效果简介
> - Simpler场景重建 上，PSNR↑ (平均) 27.0040 vs 17.2649 (Real-to-Sim) (+9.7391)；SSIM↑ (平均) 0.8522 vs 0.6833 (Real-to-Sim) (+0.1689)；LPIPS1↓ (平均) 0.0630 vs 0.3235 (Real-to-Sim) (-0.2605)。
> - DreamGen Bench (指令遵循) 上，成功率比例 (Qwen-3-VL-Plus) 约2倍于基线 vs baseline (TesserAct/Cosmos) (约+100%)。
> - DreamGen Bench (物理对齐) 上，成功率比例 (Qwen-3-VL-Plus) 显著领先 vs baseline (显著提升)。

## 概要

机器人学习面临一个根本性瓶颈：**开放世界图像虽然丰富，却缺乏与机器人动作的配对信息**，无法直接用于视动策略训练。传统的数据采集依赖真实机器人遥操作，成本高昂且环境特定，严重限制了策略的泛化能力。IGen（CVPR 2026）针对这一矛盾，提出了一条从单张开放世界图像自动生成可执行动作序列与视觉观测的技术路径。

其核心洞察在于**将非结构化2D图像转化为包含3D点云与空间关键点的结构化场景表征**，并引入视觉语言模型（VLM）进行任务推理与动作规划。在此基础上，IGen采用基于实时点云渲染的仿真自由合成方案：利用VLM规划得到的末端执行器SE(3)轨迹，对物体点云施加刚体变换，动态合成与动作严格同步的场景点云序列，逐帧渲染生成视觉观测，从而在无需人工标注的条件下实现从开放世界图像到机器人训练数据的高效转化。

**决定性证据**表明该路径有效：
- 仅使用IGen生成数据训练的策略，在多个真实机器人操作任务上平均成功率达**66.7%**，超过同等时间预算下遥操作数据训练的策略（58.3%）（Figure 7）。
- 在Simpler数据集上，IGen重建的场景视觉相似度（LPIPS₁: 0.063 vs. 0.324）大幅优于Real-to-Sim方法，提升达**5.13倍**（Table 1）。
- 在DreamGen Bench行为生成基准上，IGen在指令遵循与物理对齐指标上均显著优于TesserAct和Cosmos-Predict2等视频生成基线（Figure 4）。

**方法定位**：IGen属于数据生成范式，其核心创新在于将“场景重建—动作规划—观测合成”三个模块耦合为一个自动化流水线，改变了传统机器人数据采集对遥操作或物理仿真的依赖。与Real-to-Sim的数字孪生重建、TesserAct/Cosmos的图像到视频生成等方案相比，IGen在视觉保真度与行为物理一致性上均展现出优势。然而，该方法目前仅在桌面级操作任务上验证，对透明/反光物体、动态背景等复杂场景的鲁棒性仍有待检验。



### 机器人数据困境：从遥操作到开放世界

机器人视动策略（visuomotor policy）的训练长期受制于数据采集的“规模-成本”悖论。高质量的动作-观测配对数据通常依赖人工遥操作（human teleoperation）在真实环境中逐条采集，这不仅耗时费力，且每条轨迹都绑定于特定的物理场景与光照条件，导致策略的泛化能力严重受限。与此同时，互联网上充斥着海量的开放世界图像，它们覆盖了丰富的场景、物体和视觉外观，却天然缺失与机器人动作的配对信息——一张静态照片无法直接告诉机器人“如何操作”。

这一结构性缺口构成了机器人学习领域的核心瓶颈：**如何将非结构化的开放世界图像转化为包含可执行动作的结构化训练数据**，从而在保持视觉真实感的同时，实现数据生成的可扩展性？

### 现有路线的局限

针对上述瓶颈，学界与工业界主要探索了三条技术路线，但各自面临难以逾越的障碍：

- **真实遥操作采集**：直接由人类操作员在真实机器人上录制演示。该方法产生的数据物理保真度最高，但采集效率极低，且每次更换任务或场景都需重新部署。在同等时间预算下，遥操作可产生的数据量远不足以覆盖策略泛化所需的视觉分布。
- **Real-to-Sim 数字孪生**：通过重建真实场景的数字孪生体，在仿真环境中生成数据。以 **Simpler**（Li et al., CoRL 2024）为代表的方法试图将真实场景“搬进”仿真器，但其重建保真度严重受限于传感器精度与几何建模能力，视觉相似度（LPIPS）通常较差，导致仿真训练的模型迁移到真实世界时出现显著的感知域差距。
- **视频生成模型**：借助图像到视频扩散模型（如 **TesserAct** (Zhen et al., arXiv 2025) 和 **Cosmos-Predict2** (Agarwal et al., arXiv 2025)）从单张图像直接生成操作行为的视频序列。这类方法虽然生成速度快，但缺乏对3D几何和物理约束的显式建模，生成的动作往往违反物理规律，物体运动与指令意图之间的对齐度也较低。

这三条路线共同揭示了一个深层矛盾：**真实感、可扩展性与物理可靠性三者难以兼得**。遥操作保证了物理可靠性，但牺牲了可扩展性；视频生成模型实现了可扩展性，却丢失了物理可靠性；Real-to-Sim 试图折中，却因重建质量不足而两头落空。

### IGen 的核心动机与设计哲学

IGen 的提出正是为了打破上述三元悖论。其核心洞察在于：**将开放世界图像转化为3D点云表征，使得原本“无动作”的静态场景获得空间操作能力，进而在该结构化空间中通过视觉语言模型（VLM）进行任务推理与动作规划，最终借助实时点云渲染合成与动作严格同步的视觉观测**。

这一设计哲学将问题拆解为三个可控的子问题：场景重建（将2D图像升维为3D可操作空间）、动作规划（在3D空间中推理出可执行的动作序列）、观测合成（基于刚体变换动态生成与动作同步的视觉帧）。三者耦合，使得从单张开放世界图像自动生成大规模、物理一致、视觉逼真的视动数据成为可能，从而在根本上改变机器人学习数据的供给模式。



## 核心方法与创新机理

IGen 的核心创新在于将**开放世界单张 RGB 图像**直接转化为**可执行的视动策略训练数据**，打破了传统机器人数据采集对遥操作或物理仿真的依赖。这一转化通过三个关键槽位（changed slots）的重新设计实现，共同构成了从非结构化图像到结构化机器人经验的高效生成链路。

### 1. 数据来源：从遥操作采集到开放世界图像

**基线方案**依赖真实机器人在特定环境中进行人工遥操作采集，成本高昂且环境特定，限制了策略的泛化能力。**IGen** 将数据来源彻底切换为开放世界互联网图像——仅需单张拍摄的场景照片和一段自然语言任务指令，无需任何人工标注或真实机器人交互（Sec 1: "IGen takes in-the-wild images as the sole visual input and automatically generates robot behaviors at scale without any human annotation"）。

这一转变的因果瓶颈在于：开放世界图像天然缺乏与机器人动作的配对信息，无法直接用于视动策略训练。IGen 通过后续两个槽位的协同设计，将这一信息缺失转化为可控的生成问题。

### 2. 动作生成：从人工演示/视频扩散到 VLM 空间推理

**基线方案**的动作来源分为两类：真实机器人遥操作演示，或基于视频扩散模型的推断（如 **TesserAct** (Zhen et al., arXiv 2025) 和 **Cosmos-Predict2** (Agarwal et al., arXiv 2025)）。这些方法要么依赖昂贵的人工采集，要么缺乏精确的空间约束，导致生成的动作在物理对齐和指令遵循上表现不稳定。

**IGen** 的动作生成采用 VLM 基于 3D 关键点的高层规划与低层控制函数生成方案（Sec 3.2: "VLM decomposes the overall task into a set of sub-stages ... we develop an easily programmable control language in Python ... translating high-level task stages into executable low-level control functions"）。具体而言：

- **空间关键点集** $\mathcal{K} = \{k_j \in \mathbb{R}^3 \mid j=1,\dots,K\}$ 通过对 DINOv2 特征与 3D 坐标进行 K-means 聚类获得，为 VLM 提供了在 3D 像素空间中进行任务推理的空间锚点。
- VLM 将整体任务分解为多个子阶段，每个子阶段对应基于关键点坐标生成的末端执行器 SE(3) 轨迹。
- 低层控制函数以 Python 可编程控制语言的形式输出，直接驱动机器人在仿真环境中执行。

这一设计的因果机制在于：**关键点提供了 VLM 进行空间推理所需的几何参考**，使得高层语义规划能够精确映射到低层动作轨迹，避免了纯生成式方法中常见的物理不一致问题。

### 3. 视觉观测合成：从物理仿真/视频生成到实时点云渲染

**基线方案**的视觉观测合成依赖物理仿真环境渲染（如 **Real-to-Sim** (Li et al., CoRL 2024)）或视频生成模型。前者需要精确的数字孪生建模，后者则面临计算开销大、物理一致性差的问题。

**IGen** 提出了基于实时点云渲染的刚体运动合成方案（Sec 3.3: "we propose a robotic experience synthesis framework based on real-time point cloud rendering ... the manipulated object ... undergoes rigid-body transformations induced by the end-effector poses"）。核心机制如下：

- **被操作物体的刚体变换**：当机械爪闭合时（$t \in \mathcal{T}_{\text{grasp}}$），物体点云跟随末端执行器位姿进行刚体变换：

$$P_{\mathrm{obj}, t} = \begin{cases} P_{\mathrm{obj}, t} & t \notin \mathcal{T}_{\mathrm{grasp}}, \\ \mathbf{T}_t (\mathbf{T}_{t_g})^{-1} \mathbf{T}_{\mathrm{obj}, t_g} P_{\mathrm{obj}, t_g} & t \in \mathcal{T}_{\mathrm{grasp}}. \end{cases}$$

- **任务点云合成**：将静态背景点云、动态物体点云和机器人点云合并，形成完整的动态场景表征：

$$\mathcal{P}_{\mathrm{task}} = \mathcal{P}_{\mathrm{bg}} \cup \mathcal{P}_{\mathrm{obj}} \cup \mathcal{P}_{\mathrm{robot}}$$

- 通过虚拟深度相机逐帧渲染点云序列，生成与动作严格同步的 RGB 视觉观测。

这一方案的因果优势在于：**点云渲染天然保证了几何一致性**，而刚体变换机制确保了物体运动与末端执行器轨迹的物理同步，从根本上避免了视频生成模型中常见的物体形变、运动不一致等问题。

### 创新点之间的因果耦合

三个槽位的创新并非独立，而是形成了一条紧密耦合的因果链路：**场景重建**（3D 点云 + 空间关键点）为 **动作规划**（VLM 空间推理）提供了几何基础，而 **动作规划** 输出的 SE(3) 轨迹又直接驱动 **观测合成** 中的刚体变换与点云渲染。这种端到端的结构化生成范式，使得 IGen 能够从单张图像自动生成大规模、物理一致、视觉逼真的视动数据，在计算效率上达到每样本 18.6 秒、仅需 8.3 GB GPU 显存，分别比 TesserAct 和 Cosmos-Predict2 高效约 30 倍和 200 倍（Fig. 5）。



IGen 将一张开放世界图像和一条自然语言任务描述作为输入，输出成对的视觉观测与机器人动作序列，直接用于视动策略训练。整个框架由三个串行模块构成：**场景重建**、**动作规划**与**观测合成**，其总体流程如 Figure 2 所示。

![[assets/figures/papers/paper_list_l887_https_arxiv_org_abs_2512_01773/figures/002_Figure_2.jpg]]
*Figure 2: Overview of IGen. Given an open-world image and a task description, IGen first reconstructs the environment and objects as point clouds via Foundation Vision Models. After spatial keypoint extraction, VLM maps the task description to high-level plans and low-level control commands. During the robot’s execution in simulation, a virtual depth camera captures the motion point cloud sequences. The resulting end-effector pose trajectory is used to synthesize dynamic point-cloud sequences, which are then rendered frame-by-frame into visual observations of the manipulation. The final output consists of the generated robot actions and the visual observations*

**输入**：一张任意视角的开放世界 RGB 图像 $\mathbf{I}_{\text{bg}} \in \mathbb{R}^{H \times W \times 3}$（经修复去除被操作物体后的背景图）和任务指令文本。

**输出**：$N$ 组 $\{O_i, A_i\}_{i=1}^N$，其中 $O_i$ 为渲染得到的视觉观测序列，$A_i$ 为对应的末端执行器 SE(3) 轨迹与夹爪控制指令。

三个模块的职责与衔接关系如下：

1. **场景重建（Scene Reconstruction）**  
   利用基础视觉模型（Foundation Vision Models）从单张图像中重建环境与物体的结构化 3D 点云，提取空间关键点集 $\mathcal{K} = \{k_j \in \mathbb{R}^3 \mid j=1,\dots,K\}$，并对被操作物体进行形状补全与 6D 位姿估计。该模块将非结构化的 2D 像素转化为可供机器人在其中进行空间推理与运动规划的“可操作工作空间”。

2. **动作规划（Action Planning）**  
   视觉语言模型（VLM）以重建得到的 3D 关键点坐标为空间锚点，将高层任务指令分解为若干子阶段（sub-stages），并生成对应的低层控制函数。这些函数以 Python 可编程控制语言的形式输出，直接指定末端执行器在 SE(3) 空间中的运动轨迹与夹爪开合时机。关键点在此充当 VLM 进行空间数值计算的“坐标接口”，使高层语义推理能够精确映射到可执行的机器人动作。

3. **观测合成（Observation Synthesis）**  
   将规划得到的末端执行器位姿轨迹送入仿真环境，驱动虚拟机械臂运动。同时，被操作物体点云在抓取阶段跟随末端执行器进行刚体变换（见公式 (1)），与静态背景点云和机器人点云联合构成动态任务点云序列 $\mathcal{P}_{\text{task}} = \mathcal{P}_{\text{bg}} \cup \mathcal{P}_{\text{obj}} \cup \mathcal{P}_{\text{robot}}$。虚拟深度相机从固定视角逐帧渲染该点云序列，生成与动作严格同步的 RGB 观测帧。

**模块间的因果瓶颈**：场景重建的质量直接决定关键点坐标的精度，进而影响 VLM 动作规划的空间准确性；而动作规划输出的位姿轨迹又作为观测合成中刚体变换的驱动信号。三者构成一条“重建→规划→渲染”的因果链，任一环节的误差都会沿链传播并放大。消融实验（Figure 17）证实：移除场景重建导致点云不完整，策略完全失效；移除关键点引导使动作失去空间计算依据；移除多步规划则使机械臂直线运动碰撞障碍物。

**数据流闭环**：IGen 的输出并非孤立的视频，而是视觉观测与动作的配对数据。这些数据可直接用于训练扩散策略等视动策略模型，无需任何人工标注或遥操作介入，从而实现了从开放世界图像到机器人操作技能的全自动转化。

### 补充图表

![[assets/figures/papers/paper_list_l887_https_arxiv_org_abs_2512_01773/figures/001_Figure_1.jpg]]
*Figure 1: We propose IGen, a data generation framework that converts open-world images into grounded visuomotor data, enabling scalable data synthesis for robot learning. From a single image, IGen generates large-scale realistic observations and reliable actions. The policies trained solely on IGen-generated data can effectively generalize to real-world scenes and successfully perform manipulation tasks*



IGen 从单张开放世界图像生成视动数据的核心流程由三个串行模块构成：**场景重建**、**动作规划**与**观测合成**。三个模块共同将非结构化的 2D 图像转化为带有可执行动作的结构化机器人经验。

---

### 3.1 场景重建 (Scene Reconstruction)

该模块的目标是将输入图像转化为机器人可操作的 3D 工作空间。流程如下（参见 Figure 2、Figure 8）：

![[assets/figures/papers/paper_list_l887_https_arxiv_org_abs_2512_01773/figures/010_Figure_8.jpg]]
*Figure 8: Single-Image Scene Reconstruction Pipeline*

1. **深度估计与点云生成**：利用基础视觉模型从单张 RGB 图像估计深度，反投影为场景点云。
2. **物体分割与背景修复**：对目标操作物体进行分割并移除，通过修复得到背景图像 $\mathbf{I}_{\mathrm{bg}} \in \mathbb{R}^{H \times W \times 3}$。
3. **物体形状补全与 6D 位姿估计**：对分割出的物体进行 3D 形状补全，并估计其在场景中的初始 6D 位姿。
4. **空间关键点提取**：在场景点云上，对 DINOv2 特征与 3D 坐标进行 K-means 聚类，得到 $K$ 个空间关键点及其三维坐标：

$$
\mathcal{K} = \{k_j \in \mathbb{R}^3 \mid j=1,\dots,K\}
$$

这些关键点作为后续 VLM 进行空间推理和动作规划的**锚点**——VLM 通过引用关键点坐标来指定抓取位置、放置位置和路径点，从而将高层语言指令转化为可计算的 3D 空间约束。

消融实验（Figure 17）表明：移除场景重建模块会导致点云重建不完整，策略无法成功执行任务；移除关键点引导则使 VLM 缺乏空间计算依据，动作生成出错。

---

### 3.2 动作规划 (Action Planning)

该模块利用 VLM 的视觉理解能力，在 3D 关键点空间中进行任务推理与动作生成：

1. **任务分解**：VLM 将整体任务描述分解为一组子阶段，每个子阶段关联特定的空间关键点。
2. **控制函数生成**：作者设计了一种可编程的 Python 控制语言，VLM 将高层任务阶段翻译为可执行的低层控制函数，生成末端执行器的 SE(3) 轨迹。

这一设计的关键优势在于：VLM 直接操作 3D 关键点坐标进行空间推理，而非在 2D 像素空间中进行模糊规划，从而保证了动作的物理可行性与空间精度。消融实验（Figure 17）证实，移除多步规划会导致机械臂直线运动碰撞障碍物，无法抵达目标位置。

---

### 3.3 观测合成 (Observation Synthesis)

该模块是 IGen 实现**动作-观测严格同步**的核心机制。作者提出基于实时点云渲染的机器人经验合成框架，其核心思想是：在仿真环境中驱动机械臂执行已规划的动作，通过虚拟深度相机逐帧捕获动态点云序列并渲染为 RGB 图像。

**关键公式 1：被操作物体点云的刚体变换**

当机械爪闭合抓取物体时，物体点云跟随末端执行器进行刚体变换；否则保持静止：

$$
P_{\mathrm{obj}, t} = \begin{cases}
P_{\mathrm{obj}, t} & t \notin \mathcal{T}_{\mathrm{grasp}}, \\
\mathbf{T}_t (\mathbf{T}_{t_g})^{-1} \mathbf{T}_{\mathrm{obj}, t_g} P_{\mathrm{obj}, t_g} & t \in \mathcal{T}_{\mathrm{grasp}}.
\end{cases}
$$

其中：
- $\mathcal{T}_{\mathrm{grasp}}$ 为抓取状态的时间区间；
- $t_g$ 为抓取时刻；
- $\mathbf{T}_t$ 为 $t$ 时刻末端执行器的 SE(3) 位姿；
- $\mathbf{T}_{\mathrm{obj}, t_g}$ 为抓取时刻物体相对于末端执行器的位姿；
- $P_{\mathrm{obj}, t_g}$ 为抓取时刻的物体点云。

这一公式揭示了 IGen 的**因果机制**：物体的运动完全由末端执行器轨迹驱动，从而保证了生成的动作与视觉观测之间的物理一致性。

**关键公式 2：任务点云合成**

每帧的完整任务点云由三部分并集构成：

$$
\mathcal{P}_{\mathrm{task}} = \mathcal{P}_{\mathrm{bg}} \cup \mathcal{P}_{\mathrm{obj}} \cup \mathcal{P}_{\mathrm{robot}}
$$

其中：
- $\mathcal{P}_{\mathrm{bg}}$ 为静态背景点云（由修复后的背景图像生成）；
- $\mathcal{P}_{\mathrm{obj}}$ 为动态物体点云（按公式 1 进行刚体变换）；
- $\mathcal{P}_{\mathrm{robot}}$ 为仿真中机械臂的点云。

虚拟相机置于固定位置（Figure 9），对每帧的 $\mathcal{P}_{\mathrm{task}}$ 进行渲染，即可得到与动作序列严格同步的 RGB 观测序列 $\mathcal{O}$。

![[assets/figures/papers/paper_list_l887_https_arxiv_org_abs_2512_01773/figures/009_Figure_9.jpg]]
*Figure 9: Robot and Camera Placement in Simulation. In simulation platforms such as IsaacSim, the virtual camera is placed at the position (0, 0, 0), while the robotic arm base is positioned at the corresponding point in the point cloud, denoted as*

---

### 模块间数据流总结

三个模块形成一条**信息增益链**：场景重建将 2D 像素提升为 3D 结构化表征（点云 + 关键点）；动作规划将语言指令转化为可执行的 SE(3) 轨迹；观测合成通过刚体变换与点云渲染，将轨迹展开为视觉-动作配对数据。这一链条的每一环都不可缺失——消融实验（Figure 17）系统性地验证了场景重建、关键点引导和多步规划各自对最终策略成功率的因果贡献。

### 补充图表

![[assets/figures/papers/paper_list_l887_https_arxiv_org_abs_2512_01773/figures/011_Figure_10.jpg]]
*Figure 10: Point Cloud Synthesis during Manipulation. At time*



## 实验与关键发现

### 场景重建保真度评估

为验证IGen将开放世界图像转化为结构化场景表征的质量，论文在Simpler数据集上与Real‑to‑Sim方法（Li et al., CoRL 2024）进行了定量对比。Real‑to‑Sim将真实场景转换为仿真数字孪生，而IGen则通过基础视觉模型直接重建点云并渲染观测。如表1所示，IGen在所有视觉相似度指标上均大幅领先：

- 平均PSNR达到**27.0040**，较Real‑to‑Sim的17.2649提升**+9.74 dB**；
- 平均SSIM达到**0.8522**，较Real‑to‑Sim的0.6833提升**+0.169**；
- 平均LPIPS₁降至**0.0630**，较Real‑to‑Sim的0.3235降低**0.261**，相当于**5.13倍**的感知相似度提升。

这一结果表明，基于点云重建与渲染的IGen能够更忠实地保留原始场景的视觉细节，而Real‑to‑Sim的数字孪生方法在材质、光照和几何对齐上存在明显偏差。需要指出的是，当前评估仅限于Simpler中的桌面场景，对透明物体或复杂几何结构的重建保真度仍需手动验证。

### 行为生成质量对比

在DreamGen Bench上，论文将IGen与TesserAct（Zhen et al., arXiv 2025）和Cosmos‑Predict2（Agarwal et al., arXiv 2025）两种视频生成基线进行了定量对比。评估采用GPT‑4o、Qwen‑3‑VL‑Plus和GLM‑4.5V三个视觉语言模型作为评判器，从**指令遵循**和**物理对齐**两个维度打分：

- **指令遵循**：以Qwen‑3‑VL‑Plus为评估器时，IGen的成功视频比例约为基线的**2倍**，表明其生成的机器人行为与自然语言指令的匹配度显著更高。
- **物理对齐**：IGen同样取得显著领先，说明其基于刚体运动合成的观测序列在物理一致性上远优于视频生成模型的隐式推断。

定性对比（Figure 3）进一步揭示，TesserAct和Cosmos‑Predict2倾向于产生对象漂移、形变或不符合指令的运动轨迹，而IGen通过显式的SE(3)轨迹控制与点云刚体变换，能够生成物理上连贯且任务一致的操作序列。

![[assets/figures/papers/paper_list_l887_https_arxiv_org_abs_2512_01773/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparison of robotic behavior generation using IGen. Given a single captured image and a natural-language manipulation instruction, TesserAct [77], Cosmos [2], and our IGen generate behavior observations. IGen produces more instructionconsistent and physically coherent object motions, closely matching the intended tasks. The green box represents action observations that adhere to physical laws and follow the task instructions, and the checkmark indicates task completion*

### 计算效率分析

在相同输入图像和任务指令下，IGen展现出极高的数据生成效率（Figure 5）：

![[assets/figures/papers/paper_list_l887_https_arxiv_org_abs_2512_01773/figures/005_Figure_4.jpg]]
*Figure 4: Quantitative Comparison of robotic behavior generated by IGen*

- 单样本生成仅需**18.6秒**，占用**8.3 GB** GPU内存；
- 与TesserAct相比效率提升约**30倍**，与Cosmos‑Predict2相比提升约**200倍**。

这种效率优势源于IGen避免了视频扩散模型的迭代去噪过程，转而采用轻量级的点云渲染与合成管线。低资源消耗使得从单张图像生成1000个演示样本成为可行，为后续策略训练提供了规模化数据支撑。

### 真实机器人策略训练与评估

为验证生成数据的下游效用，论文在三个真实机器人操作任务（“Water Flowers”、“Hit Box”、“Place Toy”）上进行了策略训练对比。所有策略采用相同的扩散策略架构，仅训练数据来源不同。评估设置包括零样本π0（Black et al., arXiv 2024）、10/100个人工遥操作样本、100/1000个IGen生成样本，每个任务进行12次独立试验，使用相同的空间随机化区域和物体初始位姿。

核心发现如下（Figure 7）：

![[assets/figures/papers/paper_list_l887_https_arxiv_org_abs_2512_01773/figures/008_Figure_7.jpg]]
*Figure 7: Real-world robot evaluation results. Policies are evaluated under five settings: zero-shot, 10 human-teleoperated samples, 100 human-teleoperated samples, 100 IGen-generated samples, and 1,000 IGen-generated samples. The figure reports both per-task performance (thin lines) and the average across all tasks (thick lines). Compared with human teleoperation, IGensynthesized data can generate substantially more data within a similar time budget and achieve higher success rates*

- **零样本π0**：平均成功率仅约**19.4%**，说明预训练策略在未见场景中泛化能力有限。
- **10个遥操作样本**：成功率仍较低，数据量不足以覆盖操作空间的变化。
- **100个遥操作样本**：平均成功率提升至**58.3%**，但采集成本高昂（约需数小时人工操作）。
- **100个IGen生成样本**：平均成功率达到**44.5%**，已显著优于零样本基线，但略低于100个遥操作样本。
- **1000个IGen生成样本**：平均成功率跃升至**66.7%**，**超越**100个遥操作样本训练的策路（58.3%），且在相似时间预算下可生成数量级更多的数据。

这一结果表明，IGen生成的数据不仅可用于策略训练，而且在大规模生成时能够弥补单样本质量与真实数据的差距，最终实现超越人工采集的性能。

### 消融实验

为诊断各模块的贡献，论文进行了组件消融分析（Figure 17）：

- **移除场景重建**：点云重建不完整，导致后续动作规划缺乏可靠的3D空间参照，策略完全无法执行任务。
- **移除关键点引导**：VLM失去空间计算依据，生成的末端执行器轨迹与物体实际位置不匹配，动作错误率显著上升。
- **移除多步规划**：机械臂采用直线运动，无法规避障碍物，在需要避障的任务中无法抵达目标位置。

这些消融结果验证了场景重建、关键点引导和多步规划三个模块对于生成有效操作数据的必要性。

### 失败模式与局限性

尽管IGen在多项指标上表现优异，仍存在若干已知失败模式：

- **透明与反光物体**：单目深度估计和3D重建对透明或高反光表面敏感，可能导致点云缺失或几何失真，进而影响抓取位姿计算。
- **未见类别物体**：物体补全依赖预训练模型，对训练分布外的物体类别可能产生不合理的形状补全结果。
- **物理不安全规划**：VLM可能生成不符合物理约束的动作序列（如碰撞、不稳定的放置位姿），当前缺乏闭环仿真验证机制。
- **动态背景**：观测合成假设背景静态，无法处理移动障碍物或动态光照变化。

上述问题在论文中已明确提及，实际应用时需根据具体场景进行针对性验证。

### 关键图表指引

- **Table 1**：场景重建保真度对比，展示PSNR/SSIM/LPIPS三项指标的定量优势。
- **Figure 4**：DreamGen Bench上指令遵循与物理对齐的定量对比，以多VLM评估的成功比例度量。
- **Figure 5**：计算效率对比，展示生成时间和GPU内存占用。
- **Figure 7**：真实机器人策略性能曲线，对比零样本、遥操作与IGen数据在不同样本量下的成功率。
- **Figure 17**：消融实验定性结果，展示移除各模块后的失败案例。

![[assets/figures/papers/paper_list_l887_https_arxiv_org_abs_2512_01773/figures/004_Table_1.jpg]]
*Table 1: We compare the visual similarity between the digital-twin scenes reconstructured by Real-to-Sim and those generated by IGen. Real-to-Sim refers to the method in Simpler [40] that converts real-world scenes into simulated digital-twin scenes. We compute the LPIPS [61] variants using AlexNet [36], VGGNet [54], and SqueezeNet [27], denoted as LPIPS1, LPIPS2, and LPIPS3. ↑ / ↓ indicates higher / lower is better*

### 补充图表

![[assets/figures/papers/paper_list_l887_https_arxiv_org_abs_2512_01773/figures/007_Figure_6.jpg]]
*Figure 6: Real-world Experiments. Starting from a captured real-world scene image, IGen automatically generates 1,000 task demonstrations with spatial randomization. The resulting data are used to train a visuomotor policy, which is later deployed and evaluated in the real world. We evaluate our method on real-world tasks including “Water Flowers”, “Hit Box” and “Place Toy”*

![[assets/figures/papers/paper_list_l887_https_arxiv_org_abs_2512_01773/figures/006_Figure.jpg]]

![[assets/figures/papers/paper_list_l887_https_arxiv_org_abs_2512_01773/figures/012_Figure_12.jpg]]
*Figure 12: Hardware Setup. Our experimental setup consists of a Franka Research 3 robotic arm, a tabletop workspace, and a global RGB camera*



## 定位与知识库关联

### 1. 问题定位与核心瓶颈

机器人视动策略（visuomotor policy）的训练长期受困于数据采集成本高昂与环境特定性。真实机器人遥操作采集虽然直接，但每条轨迹耗时数分钟且难以跨场景复用；而互联网图像虽海量丰富，却缺乏与机器人动作的配对信息，无法直接用于策略学习。IGen 瞄准的正是这一“开放世界图像→可执行动作数据”的转化瓶颈：**如何从单张非结构化的 2D 图像中，自动生成包含可靠动作序列与对应视觉观测的训练数据，且无需人工标注**。

### 2. 与基线方法的关系定位

#### 2.1 真实数据采集基线

**Human Teleoperation** 是机器人操作数据采集的传统范式，通过人类遥操作演示获取 (observation, action) 对。其优势在于动作真实可靠，但扩展性极差——IGen 的实验表明，在相近时间预算下，遥操作仅能采集约 100 条轨迹，而 IGen 可生成 1000 条，且训练出的策略成功率高出 8.4 个百分点（66.7% vs 58.3%，Figure 7）。这揭示了一个关键洞察：**在固定时间预算下，生成数据的数量优势可弥补单条数据质量的差距**。

#### 2.2 仿真场景重建基线

**Real-to-Sim**（Simpler, Li et al., CoRL 2024）尝试将真实场景转化为数字孪生仿真环境，再在仿真中采集数据。然而其重建保真度有限：在 Simplers 数据集上，IGen 重建的视觉相似度在 LPIPS₁ 指标上达到 0.063，较 Real-to-Sim 的 0.324 提升了 **5.13 倍**（Table 1）。IGen 的优势在于不追求完整的数字孪生重建，而是直接对场景点云进行操作级合成，避免了纹理、光照等精细建模的误差累积。

#### 2.3 视频/行为生成基线

**TesserAct**（Zhen et al., arXiv 2025）和 **Cosmos-Predict2**（Agarwal et al., arXiv 2025）代表了基于图像到视频生成的机器人行为合成路线。这类方法将任务指令和初始图像输入视频扩散模型，直接生成操作过程的视频帧。然而，扩散模型缺乏对 3D 几何和物理约束的显式建模，导致生成的行为常出现物体穿透、运动不连贯等问题。在 DreamGen Bench 上，IGen 在“指令遵循”维度上的成功率约为基线的 **2 倍**（Figure 4），在“物理对齐”维度上也显著领先。此外，Figure 5 显示 IGen 的生成效率远超基线：**单样本仅需 18.6 秒和 8.3 GB 显存**，比 TesserAct 快约 30 倍，比 Cosmos-Predict2 快约 200 倍。

#### 2.4 零样本策略基线

**π0**（Black et al., arXiv 2024）作为零样本视动策略基线，在 IGen 的真实机器人实验中表现最弱（Figure 7），这从侧面验证了 IGen 生成数据对领域内任务训练的必要性——即使是大规模预训练的通用策略，也难以在未见过的新场景中直接零样本泛化。

### 3. 方法谱系中的技术定位

从技术路线看，IGen 处于 **“重建-规划-合成”三阶段范式**的交汇点：

| 阶段 | 技术路线 | IGen 的选择 | 与替代路线的差异 |
|------|----------|-------------|------------------|
| 场景表征 | 神经辐射场 / 3D Gaussian Splatting / 点云 | **点云** | 点云支持高效的刚体变换与实时渲染，无需训练或优化，适合动态合成 |
| 动作生成 | 强化学习 / 运动规划 / VLM 推理 | **VLM + 关键点引导** | 利用 VLM 的空间推理能力直接从关键点坐标生成控制函数，避免 RL 的样本低效 |
| 观测合成 | 物理仿真渲染 / 视频扩散模型 / 点云渲染 | **点云渲染** | 相比物理仿真无需完整场景建模，相比扩散模型保证物理一致性 |

这一范式使 IGen 在与各类基线的对比中呈现出 **“数据效率-视觉保真-物理一致性”的三维优势**。

### 4. 适用边界与局限

IGen 的能力边界受其技术路线固有约束：

1. **重建质量依赖**：场景重建依赖单目深度估计和 3D 物体补全模型，对透明/反光物体或复杂几何结构可能产生不完整或错误的点云，进而导致后续动作规划失败（消融实验 Figure 17 证实移除场景重建模块后策略完全失效）。

2. **任务空间受限**：目前仅在桌面级操作任务（Water Flowers、Hit Box、Place Toy）上验证，尚未扩展到移动操作或非结构化环境。VLM 生成的动作规划可能缺乏对动态障碍物或复杂接触约束的处理能力。

3. **物理真实性边界**：点云刚体变换假设物体为刚体且抓取后完全跟随末端执行器运动，这忽略了摩擦力、接触变形、多物体交互等复杂物理现象。论文明确指出 VLM 可能产生不符合物理规律或不安全的动作规划。

4. **物体泛化局限**：物体补全依赖预训练模型，对未见过类别的物体可能失效，这限制了 IGen 在开放类别场景中的直接应用。

### 5. 开放问题与未来方向

论文提出的开放问题指向以下研究方向：

- **多物体交互扩展**：当前 IGen 主要处理单物体操作，如何扩展到杂乱场景中的多物体交互（如堆叠、推挤）是一个核心挑战。
- **多视角融合**：能否利用多视角图像或主动感知策略进一步提高重建精度，特别是在遮挡严重或深度估计失效的区域？
- **虚实混合训练**：IGen 生成数据能否与少量真实遥操作数据结合，实现更高效的政策训练？初步实验（Figure 7）显示 100 条 IGen 数据已接近 100 条遥操作数据的性能，暗示混合训练可能进一步突破上限。
- **动态背景处理**：当前假设背景完全静态，如何处理动态背景或移动障碍物对观测合成的影响？
- **闭环仿真验证**：如何对生成数据进行闭环仿真验证，以确保其动力学一致性？当前 IGen 生成的数据未经过物理引擎验证，可能存在隐式的物理不一致。

**注意**：以上开放问题均来自论文自身的讨论（Section 5 及 Limitations 部分），部分方向（如虚实混合训练）已有初步实验证据支持，但完整的解决方案仍需后续工作探索。



## 原文 PDF

![[paperPDFs/CVPR_2026/IGen_Scalable_Data_Generation_for_Robot_Learning_from_Open_World_Images.pdf]]
