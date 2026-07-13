---
title: Stability-Driven Motion Generation for Object-Guided Human-Human Co-Manipulation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Stability_Driven_Motion_Generation_for_Object_Guided_Human_Human_Co_Manipulation.pdf
project_link: null
code_link: null
aliases:
- SSDCM
- SDMGOGHHCM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过在 Flow Matching 框架中嵌入可执行性感知的接触策略、对抗性交互先验和稳定性驱动的物理仿真，将意图、自然性和有效性三个原则注入生成过程。
primary_logic: 将对象可执行性、双人交互协调性和物理稳定性显式编码为生成过程的引导信号，可以有效解决协同操作中多智能体与物体之间的紧耦合动态问题。
claims:
- 添加稳定性驱动仿真后，穿透深度（Pene.）从 0.15 降至 0.02，接触精度（Contact Acc.）从 0.35 提升至 0.44。
- 对抗性交互先验使 FID 从 26.3 降至 25.5，IDF 从 0.25 降至 0.22。
- 利用预测的接触锚点进行梯度引导，接触精度从 0.35 提升至 0.40。
- Core4D-S1 上 Contact Acc. ↑ = 0.44
---

# Stability-Driven Motion Generation for Object-Guided Human-Human Co-Manipulation

> [!tip] 核心洞察
> 将对象可执行性、双人交互协调性和物理稳定性显式编码为生成过程的引导信号，可以有效解决协同操作中多智能体与物体之间的紧耦合动态问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向对象引导的人人协同操作稳定性驱动运动生成 |
| 英文题名 | Stability-Driven Motion Generation for Object-Guided Human-Human Co-Manipulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_Stability-Driven_Motion_Generation_for_Object-Guided_Human-Human_Co-Manipulation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | StaCOM (Stability-Driven Co-Manipulation) |
| Dataset | Core4D-S1 |

> [!tip] 效果简介
> - Core4D-S1 上，Contact Acc. ↑ 0.44 vs 0.35 (Flow Matching baseline) (+0.09)；Penetration (Pene.) ↓ 0.05 vs 0.15 (Flow Matching baseline) (-0.10)；FID ↓ 25.5 vs 26.3 (Flow Matching baseline) (-0.8)。

## 概要

人人协同操作（human-human co-manipulation）的自动运动生成面临一个核心瓶颈：现有方法缺乏对**物理稳定性、交互自然性与操作意图**的统一建模，导致生成的运动普遍存在穿透、接触不准确和动作不协调等问题。本文提出 **StaCOM（Stability-Driven Co-Manipulation）**，在 Flow Matching 生成框架中显式嵌入三条原则——**意图（intention）、自然性（naturalness）和有效性（effectiveness）**——通过可执行性感知的接触策略、对抗性交互先验和稳定性驱动的物理仿真，将协同操作中多智能体与物体的紧耦合动态问题转化为可引导的生成过程。

在方法谱系上，StaCOM 以 Flow Matching 为骨架，替代了主流的扩散模型（如 MDM），并引入了三个关键模块：接触策略扩散模型、双人交互判别器、以及基于 CMA-ES 的物理仿真校正。相较于 **OMOMO**（Li et al., TOG 2023）的物体轨迹条件单人运动生成和 **InterGen**（Liang et al., IJCV 2024）的多人物交互扩散生成，StaCOM 首次将对象可执行性、双人协调性与物理合理性统一为生成引导信号。

在 Core4D-S1 基准上，StaCOM 相比 Flow Matching 基线将接触精度（Contact Acc.）从 0.35 提升至 0.44，穿透深度（Pene.）从 0.15 降至 0.05，FID 从 26.3 降至 25.5。消融实验证实，稳定性仿真模块是物理合理性提升的关键驱动力，而对抗性交互先验和接触引导则分别贡献了运动自然性和接触准确性的改善。该方法的主要局限在于物理仿真模块推理耗时较长（约 3 分钟处理 128 帧），且目前仅在 Core4D 数据集上验证，向更复杂的推拉任务和多物体共操作场景的泛化能力尚待探索。



### 问题背景

在虚拟现实、具身智能与数字人等应用中，多智能体协同操作物体的运动生成是一个关键且极具挑战性的问题。与单人操作物体（HOI）或纯人际交互不同，**人人协同操作（co-manipulation）** 涉及两个（或多个）人物与一个共享物体之间的紧耦合动态：人物之间需要协调动作以保持物体的稳定，同时每个人的手部必须与物体保持合理的接触，而整个过程中运动还需看起来自然、流畅。

现有工作大多将这一问题拆解为独立的子任务进行处理。例如，**OMOMO**（Li et al., TOG 2023）以物体轨迹为条件生成单人操作运动，但无法建模多人之间的协调；**InterGen**（Liang et al., IJCV 2024）可生成双人交互运动，但缺乏对物体动力学的显式约束；**InterDiff**（Xu et al., ICCV 2023）在扩散模型中引入物理信息以改善人-物交互，但未处理多人协同场景。这些方法的共同缺陷在于：**缺乏对物理稳定性、交互自然性和操作意图的统一建模**，导致生成的运动存在穿透、接触不准确和动作不协调等问题。

### 现有方法缺口

从方法论角度审视，现有协同操作运动生成存在三个核心缺口：

1. **意图缺失**：生成的运动往往无法准确反映“两人共同操作物体”这一高层意图。手部何时接触物体、接触在物体的哪个部位，这些关键决策在现有方法中缺乏显式建模，导致生成的抓握位置不合理或与物体轨迹不一致。

2. **自然性不足**：双人协同操作不仅要求个体姿态自然，还要求两人之间的相对运动、力量配合等交互模式符合人类行为习惯。现有方法或仅使用单人运动先验，或完全忽略交互协调性，导致生成的协同动作生硬、缺乏默契。

3. **有效性缺位**：生成的姿态序列在物理上可能不可行——物体可能因受力不平衡而掉落，人物可能穿透物体或地面，接触点可能滑动。纯数据驱动的生成模型无法保证输出满足牛顿力学约束。

### 本文动机

针对上述缺口，本文提出将**意图（Intention）**、**自然性（Naturalness）** 和**有效性（Effectiveness）** 三个原则显式注入运动生成过程。核心洞察是：**将对象可执行性、双人交互协调性和物理稳定性显式编码为生成过程的引导信号，可以有效解决协同操作中多智能体与物体之间的紧耦合动态问题。**

具体而言，本文在 Flow Matching 生成框架中嵌入三个关键机制：可执行性感知的接触策略（意图）、对抗性交互先验（自然性）和稳定性驱动的物理仿真（有效性）。这一设计使得生成的运动既能准确响应物体轨迹，又能保持双人协调与物理合理，从而填补了现有方法在统一建模上的空白。



## 核心方法与创新机理

StaCOM 的核心创新在于将**意图（Intention）**、**自然性（Naturalness）** 与**有效性（Effectiveness）** 三个原则显式编码为生成过程的引导信号，从而解决多人-物体紧耦合协同操作中长期存在的物理不稳定、接触不准确与动作不协调问题。与现有方法相比，该方法在以下四个关键维度上实现了结构性改进。

### 1. 生成范式转换：从扩散模型到 Flow Matching

现有方法（如 **OMOMO** (Li et al., TOG 2023)、**InterGen** (Liang et al., IJCV 2024)）普遍采用扩散模型作为生成框架。StaCOM 转而采用 **Flow Matching** 作为基础生成范式，将运动生成建模为确定性向量场回归问题：从噪声状态 $\mathbf{x}_0$ 出发，通过预测瞬时速度场 $f_{\theta}(\mathbf{x}_{\tau}, \tau, \mathbf{c})$ 沿时间轴将状态传输至数据分布。其核心更新公式为：

$$\mathbf{x}_{\tau+\Delta\tau} = \mathbf{x}_{\tau} + \Delta\tau f_{\theta}(\mathbf{x}_{\tau}, \tau, \mathbf{c})$$

训练目标是最小化预测速度与目标位移之间的均方误差：

$$\mathcal{L}_{\mathrm{flow}} = \mathbb{E}_{\tau, \mathbf{x}_{\tau}} \Big[ \| f_{\theta}(\mathbf{x}_{\tau}, \tau, \mathbf{c}) - (\mathbf{x}_1 - \mathbf{x}_0) \|_2^2 \Big]$$

这一转换带来的优势在于：Flow Matching 通过学习连续且确定的向量场，在推理时仅需少量 Euler 积分步（实验中 $K=10$）即可完成生成，同时为后续接触梯度引导和先验梯度引导提供了天然的介入接口——速度场 $f_{\theta}$ 可直接被校正项调整（见下文第 2、3 点），无需修改去噪过程。

### 2. 接触策略：从无引导到可执行性感知的接触锚点

现有方法在协同操作中缺乏明确的接触引导，导致生成的抓握位置偏离物体可操作区域，表现为接触精度低和滑移。StaCOM 引入**可执行性感知的接触策略生成**，包含两个紧密耦合的子模块：

- **接触策略扩散模型**：以物体的可执行性场（affordance field）和 BPS 特征为条件，通过扩散模型生成多样化的接触锚点 $\hat{\mathbf{p}}_{a,h}$ 及对应法向量 $\hat{\mathbf{n}}_{a,h}$。训练时使用组合损失 $\mathcal{L}_{\mathrm{str}} = \mathcal{L}_{\mathrm{anchor}} + \mathcal{L}_{\mathrm{normal}} + \mathcal{L}_{\mathrm{aff}}$，其中 $\mathcal{L}_{\mathrm{aff}} = -\frac{1}{Z_{\mathrm{pos}}} \sum_{t,a,h} s_{a,h}^t \log \alpha(\hat{\mathbf{p}}_{a,h}^t)$ 强制接触点落在高可执行性区域。

- **接触梯度引导**：在推理的每个 Euler 积分步，利用接触损失 $\mathcal{L}_{\mathrm{contact}} = \frac{1}{Z} \sum_{a,h} \mathcal{V}_{a,h} \| \mathbf{w}_{a,h} - \hat{\mathbf{p}}_{a,h} \|_2^2$ 的梯度校正速度场：

$$\tilde{f}_{\theta}(\mathbf{x}_{\tau}) = f_{\theta}(\mathbf{x}_{\tau}) - \gamma \nabla_{\mathbf{x}_{\tau}} \mathcal{L}_{\mathrm{contact}}$$

消融实验证实，仅添加此模块即可使接触精度从 0.35 提升至 0.40（Table 2: +Contact），验证了可执行性感知接触策略对抓握准确性的直接贡献。

### 3. 交互先验：从无先验到对抗性双人交互判别器

现有方法或缺乏交互先验，或仅使用单人运动判别器，无法捕捉双人协同操作中的社交协调性。StaCOM 提出**对抗性交互先验**，包含两个判别器：

- **单人姿态判别器** $\mathcal{D}_{\phi}^{\mathrm{body}}$：评估个体姿态的自然性；
- **双人交互判别器** $\mathcal{D}_{\phi}^{\mathrm{int}}$：评估两人相对空间关系和时序协调性。

训练时使用非饱和二元交叉熵损失 $\mathcal{L}_{\mathrm{prior}}^{(k)}$；推理时，判别器梯度被聚合为引导信号，校正速度场：

$$\tilde{f}_{\theta}(\mathbf{x}_{\tau}) = f_{\theta}(\mathbf{x}_{\tau}) + \eta \sum_{k\in\{\mathrm{body},\mathrm{int}\}} \nabla_{\mathbf{x}_{\tau}} \log \mathcal{D}_{\phi}^{k}$$

消融实验表明，单独添加个体姿态先验使 IDF 从 0.25 降至 0.22，FID 从 26.3 降至 25.5；进一步加入交互先验后，接触精度提升至 0.35 且 FID 维持在 25.4（Table 2: +Individual Prior → +Interaction Prior）。这证明双人交互判别器在保持个体自然性的同时，有效捕捉了协同操作特有的空间协调模式。

### 4. 物理仿真：从无物理约束到稳定性驱动 CMA-ES 优化

现有生成方法完全依赖数据驱动，缺乏物理约束，导致生成的运动存在穿透（penetration）和漂浮（floating）等物理伪影。StaCOM 引入**稳定性驱动仿真模块**，在推理的倒数第二步介入：

- 使用 CMA-ES 算法采样姿态校正偏移量；
- 将校正后的姿态输入配备 PD 控制器的物理引擎进行前向仿真；
- 优化目标为物理损失 $\mathcal{L}_{\mathrm{phys}} = \mathcal{L}_{\mathrm{sim}} + \mathcal{L}_{\mathrm{sta}}$，其中：
  - $\mathcal{L}_{\mathrm{sim}}$ 鼓励仿真结果接近目标姿态和物体位姿；
  - $\mathcal{L}_{\mathrm{sta}}$ 强制执行牛顿-欧拉力/力矩匹配，惩罚不稳定的漂浮和穿透。

消融实验显示，移除仿真模块后穿透深度从 0.05 剧增至 0.16，接触精度从 0.44 降至 0.37（Table 2: Ours vs +Simulation），充分证明物理仿真对消除物理伪影的决定性作用。但需注意，该模块显著增加了推理时间（约 3 分钟处理 128 帧），是当前方法的主要效率瓶颈。

### 创新点之间的因果耦合关系

上述四个创新并非孤立叠加，而是形成了因果闭环：**Flow Matching** 提供可微的速度场，使**接触梯度引导**和**先验梯度引导**能够在推理时直接校正生成方向；**接触策略**确保手部到达正确的可操作区域，为**物理仿真**提供合理的初始接触状态；**交互先验**保证双人动作的协调性，避免仿真中出现不自然的对抗力；**稳定性仿真**最终消除数据驱动生成残留的物理伪影，将穿透深度降至 0.02 的极低水平。这一“生成-引导-仿真”三级递进架构，是 StaCOM 在接触精度（0.44）和穿透深度（0.05）两项关键指标上大幅领先 Flow Matching 基线（分别为 0.35 和 0.15）的根本原因。



StaCOM 的整体设计遵循“意图—自然性—有效性”三原则，通过四个协同模块将对象引导的双人协同操作建模为一个条件运动生成问题。如 Figure 2 所示，给定物体网格及其 6D 轨迹，系统依次经过 **BPS 特征提取**、**Flow Matching 运动生成**、**可执行性感知的接触策略生成**、**对抗性交互先验引导** 以及 **稳定性驱动的物理仿真**，最终输出物理合理且协调的双人操作运动序列。

![[assets/figures/papers/paper_list_l10_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Stability_Driven_Mo/figures/002_Figure_2.jpg]]
*Figure 2: Overview. Given an input object trajectory, our method generates co-manipulation motions conditioned on object 6D poses and their BPS features (a). To ensure that the motions are consistent with the object trajectory, an affordance-informed manipulation strategy (b) is introduced to produce explicit contact signals as flow guidance. Building on this design, we further propose an adversarial interaction prior (c) and a stability-driven simulation (d) to enhance motion quality. Note that the contact strategy (b), flow matching (a), and interaction prior (c) are trained separately in advance, while all components are executed jointly at inference time*

### 输入输出流与模块关系

系统的输入为物体网格和其 6D 轨迹（位置与朝向随时间变化），输出为两个交互角色的 SMPL-X 姿态参数序列。各模块在推理时联合执行，但训练阶段是分离的——接触策略扩散模型、Flow Matching 生成网络和对抗性判别器均独立预训练。

**BPS 特征提取** 将逐帧的物体 6D 姿态编码为基点点集（Basis Point Set, BPS）描述符，为后续模块提供紧凑的物体形状与位姿上下文。该描述符作为条件信号同时馈入 Flow Matching 生成网络和接触策略预测网络。

**Flow Matching 生成网络** 是整个框架的核心引擎。它采用 Transformer 架构，将运动生成形式化为从噪声到数据分布的确定性向量场回归问题。在推理时，网络以欧拉积分方式逐步更新双人状态：

$$\mathbf{x}_{\tau+\Delta\tau} = \mathbf{x}_{\tau} + \Delta\tau f_{\theta}(\mathbf{x}_{\tau},\tau,\mathbf{c})$$

其中 $\mathbf{x}_{\tau}$ 为当前扩散时间步的状态，$\mathbf{c}$ 为包含物体 BPS 特征和接触锚点的条件信号。该模块的损失函数为预测速度场与目标位移之间的均方误差：

$$\mathcal{L}_{\mathrm{flow}} = \mathbb{E}_{\tau,\mathbf{x}_{\tau}} \Big[ \| f_{\theta}(\mathbf{x}_{\tau},\tau,\mathbf{c}) - (\mathbf{x}_1 - \mathbf{x}_0) \|_2^2 \Big]$$

**可执行性感知的接触策略模块** 在 Flow Matching 的欧拉积分过程中注入接触引导。该模块首先使用扩散模型根据物体可执行性场（affordance field）预测多样化的接触锚点 $\hat{\mathbf{p}}_{a,h}$ 及其置信度权重 $\mathcal{V}_{a,h}$，然后通过接触损失对生成过程进行梯度校正：

$$\tilde{f}_{\theta}(\mathbf{x}_{\tau}) = f_{\theta}(\mathbf{x}_{\tau}) - \gamma \nabla_{\mathbf{x}_{\tau}} \mathcal{L}_{\mathrm{contact}}$$

$$\mathcal{L}_{\mathrm{contact}} = \frac{1}{Z} \sum_{a,h} \mathcal{V}_{a,h} \| \mathbf{w}_{a,h} - \hat{\mathbf{p}}_{a,h} \|_2^2$$

这一机制强制角色的手腕位置 $\mathbf{w}_{a,h}$ 向高可执行性区域靠拢，从而提升抓取精度和操作一致性。

**对抗性交互先验模块** 由两个独立训练的判别器组成：单人姿态判别器评估个体运动的自然性，双人交互判别器评估角色间的协调性。在推理时，判别器梯度被聚合到速度场中以引导采样过程：

$$\tilde{f}_{\theta}(\mathbf{x}_{\tau}) = f_{\theta}(\mathbf{x}_{\tau}) + \eta \sum_{k\in\{\mathrm{body},\mathrm{int}\}} \nabla_{\mathbf{x}_{\tau}} \log \mathcal{D}_{\phi}^{k}$$

这一机制在不改变生成模型本身的前提下，将运动分布拉向真实交互数据的流形。

**稳定性驱动仿真模块** 在推理的倒数第二步介入，解决 Flow Matching 输出中常见的浮空、穿透和物体受力不一致等物理违规问题。如 Figure 3 所示，该模块使用 CMA-ES 算法采样对 Flow Matching 输出的校正偏移量，将校正后的姿态送入配备 PD 控制器的物理引擎进行短时仿真，并通过物理损失 $\mathcal{L}_{\mathrm{phys}} = \mathcal{L}_{\mathrm{sim}} + \mathcal{L}_{\mathrm{sta}}$ 优化校正参数。其中 $\mathcal{L}_{\mathrm{sim}}$ 保证仿真结果与原始输出的相似性，$\mathcal{L}_{\mathrm{sta}}$ 强制执行牛顿-欧拉方程的力/力矩匹配及能量正则化：

$$\mathcal{L}_{\mathrm{sta}} = \frac{\| \vec{f}(t) - M_o \vec{a} \|_2^2}{\| M_o \vec{g} \|_2^2} + \frac{\| \vec{\mu}(t) - I_o \vec{\alpha} \|_2^2}{\| I_o \vec{\alpha} \|_2^2} + e^{-m(t)}$$

仿真校正后的状态被回传至欧拉积分循环，用于下一步的状态更新。

### 训练与推理分离的设计逻辑

四个模块中，Flow Matching 生成网络、接触策略扩散模型和对抗性判别器均离线独立训练，仅在推理时通过梯度引导和物理校正实现联合优化。这种解耦设计的优势在于：各模块可针对特定子目标（运动分布匹配、接触精度、自然性、物理稳定性）进行专项优化，同时避免联合训练带来的优化困难与计算开销。但其代价是推理流程复杂且耗时——仿真模块的 CMA-ES 优化处理 128 帧约需 3 分钟，难以满足实时应用需求。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Stability_Driven_Mo/figures/001_Figure_1.jpg]]
*Figure 1: Given an object mesh and its trajectory (green), our method generates coordinated motions that are consistent with the trajectory while remaining natural and physically plausible for co-manipulation*



StaCOM 框架围绕“意图—自然性—有效性”三原则，将协同操作运动生成分解为四个可组合的核心模块：**Flow Matching 生成网络**、**可执行性感知的接触策略**、**对抗性交互先验**、以及**稳定性驱动物理仿真**。各模块在推理时联合执行，共同引导从噪声到协调双人运动的确定性映射。

### Flow Matching 生成网络（基础框架）

StaCOM 采用 Flow Matching 作为基础生成框架，将运动生成形式化为从噪声分布到数据分布的连续向量场回归问题。给定当前状态 $\mathbf{x}_{\tau}$（包含双人的 SMPL-X 姿态参数、全局平移和物体 6D 姿态）和条件 $\mathbf{c}$（物体 BPS 特征与接触锚点），Transformer 结构的流函数 $f_{\theta}$ 预测瞬时速度场，通过欧拉积分更新状态：

$$\mathbf{x}_{\tau+\Delta\tau} = \mathbf{x}_{\tau} + \Delta\tau \, f_{\theta}(\mathbf{x}_{\tau}, \tau, \mathbf{c}) \tag{1}$$

训练时，流匹配损失最小化预测速度与目标位移之间的均方误差：

$$\mathcal{L}_{\mathrm{flow}} = \mathbb{E}_{\tau,\mathbf{x}_{\tau}} \Big[ \| f_{\theta}(\mathbf{x}_{\tau},\tau,\mathbf{c}) - (\mathbf{x}_1 - \mathbf{x}_0) \|_2^2 \Big] \tag{2}$$

为稳定关节解码，对预测的 SMPL-X 参数施加 L1 损失 $\mathcal{L}_{\mathrm{SMPL}}$；为抑制滑步，引入足部接触损失 $\mathcal{L}_{\mathrm{foot}}$，在足部着地时惩罚位移。总损失为加权组合：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{flow}} + \mathcal{L}_{\mathrm{SMPL}} + \mathcal{L}_{\mathrm{foot}} + \mathcal{L}_{\mathrm{prior}} \tag{5}$$

### 可执行性感知的接触策略（意图注入）

为使生成的运动与物体操作意图一致，StaCOM 引入一个独立的扩散模型来预测可执行性感知的接触策略。该模型以物体的可执行性场（affordance field）和 BPS 特征为条件，生成接触锚点位置 $\hat{\mathbf{p}}_{a,h}$、法向量 $\hat{\mathbf{n}}_{a,h}$ 和接触置信度。策略损失由三项组成：

$$\mathcal{L}_{\mathrm{str}} = \mathcal{L}_{\mathrm{anchor}} + \mathcal{L}_{\mathrm{normal}} + \mathcal{L}_{\mathrm{aff}} \tag{6}$$

其中 $\mathcal{L}_{\mathrm{anchor}}$ 为接触点 L2 距离，$\mathcal{L}_{\mathrm{normal}}$ 鼓励法向量对齐，$\mathcal{L}_{\mathrm{aff}}$ 为负对数似然，迫使接触点落在高可执行性区域。在推理时，预测的接触锚点通过梯度引导调整流预测：

$$\mathcal{L}_{\mathrm{contact}} = \frac{1}{Z} \sum_{a,h} \mathcal{V}_{a,h} \| \mathbf{w}_{a,h} - \hat{\mathbf{p}}_{a,h} \|_2^2 \tag{10}$$

$$\tilde{f}_{\theta}(\mathbf{x}_{\tau}) = f_{\theta}(\mathbf{x}_{\tau}) - \gamma \nabla_{\mathbf{x}_{\tau}} \mathcal{L}_{\mathrm{contact}} \tag{11}$$

这一机制将接触意图显式注入生成过程，使手腕位置向可执行性加权的接触目标靠拢。

### 对抗性交互先验（自然性注入）

为提升运动的自然性与交互协调性，StaCOM 训练两个对抗性判别器：**单人姿态判别器** $\mathcal{D}_{\phi}^{\mathrm{body}}$ 和**双人交互判别器** $\mathcal{D}_{\phi}^{\mathrm{int}}$。判别器以非饱和二元交叉熵训练：

$$\mathcal{L}_{\mathrm{prior}}^{(k)} = -\mathbb{E}_{(\mathbf{R},\beta)\sim\mathcal{D}_{\mathrm{real}}^{(k)}}[\log \mathcal{D}_{\phi}^{k}] - \mathbb{E}_{(\tilde{\mathbf{R}},\tilde{\beta})\sim\mathcal{D}_{\mathrm{gen}}^{(k)}}[\log(1-\mathcal{D}_{\phi}^{k})] \tag{12}$$

训练后的判别器在推理时作为评估器，通过梯度引导修正速度场，使采样姿态向真实分布靠拢：

$$\tilde{f}_{\theta}(\mathbf{x}_{\tau}) = f_{\theta}(\mathbf{x}_{\tau}) + \eta \sum_{k\in\{\mathrm{body},\mathrm{int}\}} \nabla_{\mathbf{x}_{\tau}} \log \mathcal{D}_{\phi}^{k} \tag{14}$$

消融实验（Table 2）表明，单独添加个体姿态先验使 IDF 从 0.25 降至 0.22、FID 从 26.3 降至 25.5；加入交互先验后接触精度提升至 0.35 且 FID 保持在 25.4。

### 稳定性驱动物理仿真（有效性注入）

纯生成模型输出的运动常伴随浮空、穿透等物理伪影。StaCOM 在推理的倒数第二步引入基于 CMA-ES 的稳定性驱动仿真模块。该模块采样校正偏移量，通过 PD 控制器驱动物理仿真，并优化物理损失：

$$\mathcal{L}_{\mathrm{phys}} = \mathcal{L}_{\mathrm{sim}} + \mathcal{L}_{\mathrm{sta}} \tag{15}$$

其中 $\mathcal{L}_{\mathrm{sim}}$ 鼓励仿真后的姿态和物体位姿接近目标值，$\mathcal{L}_{\mathrm{sta}}$ 强制执行力/力矩匹配和能量正则化。消融实验显示，移除仿真模块后穿透深度从 0.05 急剧上升至 0.16，接触精度从 0.44 降至 0.37，验证了物理仿真在消除穿透和提升接触准确性方面的关键作用。

### 模块协同机制

四个模块在推理时形成级联引导管线：Flow Matching 提供基础生成能力；接触策略通过梯度引导（Eq. 11）注入操作意图；交互先验通过判别器梯度（Eq. 14）提升自然性；物理仿真在最后阶段校正不稳定姿态。这种解耦设计使各模块可独立预训练，推理时灵活组合，兼顾生成质量与物理有效性。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Stability_Driven_Mo/figures/003_Figure_3.jpg]]
*Figure 3: Stability-driven simulation pipeline. The CMA-ES algorithm samples corrective offsets*



## 实验与关键发现

### 主实验结果

我们在 Core4D 数据集上将 StaCOM 与多个代表性基线进行了全面对比，结果如 Table 1 所示。Core4D 是目前唯一公开的多人协同操作运动数据集，包含丰富的双人搬运与转向场景，为公平评估提供了标准化的测试平台。

![[assets/figures/papers/paper_list_l10_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Stability_Driven_Mo/figures/005_Table_1.jpg]]
*Table 1: Performance comparison on the Core4D dataset. Metrics marked with ↑ indicate higher is better, while ↓ indicates lower is better*

**接触精度与物理合理性**：StaCOM 在接触精度（Contact Acc.）上达到 0.44，显著优于 Flow Matching 基线的 0.35（+0.09），同时穿透深度（Pene.）从 0.15 降至 0.05。这一提升源于可执行性感知的接触策略与稳定性驱动仿真的协同作用——接触锚点扩散模型将双手引导至物体的高可执行性区域，而 CMA-ES 物理仿真则在倒数第二步纠正了残余的穿透和悬浮伪影。

**运动质量与分布保真度**：在 FID 指标上，StaCOM 达到 25.5，较 Flow Matching 基线的 26.3 降低了 0.8；交互多样性保真度 IDF 从 0.25 降至 0.22。这表明对抗性交互先验（单人姿态判别器 + 双人交互判别器）有效提升了生成运动的自然性和协调性。与 **OMOMO**（Li et al., TOG 2023）和 **InterGen**（Liang et al., IJCV 2024）等现有方法相比，StaCOM 在所有物理合理性指标上均取得一致优势，尤其是在穿透深度和接触精度上拉开了明显差距。

**定性分析**：Figure 4 展示了 ComMDM、InterGen、OMOMO 与 StaCOM 在关键时间戳的生成结果对比。基线方法在物体姿态变化时普遍出现抓握滑移或响应延迟，而 StaCOM 在整个操作序列中保持了协调的双人抓握和稳定的物体对齐。Figure 5 进一步展示了 StaCOM 生成的协作运动，两个角色在转向和抬升过程中保持同步，并展现出精细的抓握调整行为。

### 消融实验

为验证各模块的独立贡献，我们在 Core4D-S1 上进行了系统的消融实验（Table 2 / Figure 6），从 Flow Matching 基线出发逐步添加各组件。

![[assets/figures/papers/paper_list_l10_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Stability_Driven_Mo/figures/007_Figure_6.jpg]]
*Figure 6: Ablation of key components on Core4D-S1. The vanilla flow matching model fails to generate realistic interactions. Built upon this baseline, the affordance-informed strategy and interaction prior further improve motion realism and naturalness. Moreover, the physics-based simulation enhances physical plausibility*

**交互先验的作用**：单独添加个体姿态先验（+Individual Prior）使 IDF 从 0.25 降至 0.22，FID 从 26.3 降至 25.5，证明单人姿态判别器有效约束了生成姿态的自然度。进一步加入双人交互先验（+Interaction Prior）后，接触精度从 0.31 提升至 0.35，FID 维持在 25.4，说明交互判别器对协调性有独立的增益。

**接触策略的贡献**：在交互先验基础上加入可执行性感知的接触锚点梯度引导（+Contact），接触精度从 0.35 提升至 0.40，FID 为 26.0。这一结果表明，预测的接触锚点通过梯度校正（Eq. 11）将手腕位置有效拉向高可执行性区域，但仅靠接触引导尚不足以完全消除穿透。

**物理仿真的决定性作用**：完整模型（+Simulation）将穿透深度从 0.16 降至 0.05，接触精度从 0.37 提升至 0.44。移除仿真模块后，穿透深度反弹至 0.16，接触精度降至 0.37，验证了 CMA-ES 物理仿真对物理合理性的决定性贡献。物理损失中的力/力矩匹配项（Eq. 17）强制执行了牛顿-欧拉方程，有效纠正了生成运动中的悬浮和穿透伪影。

### 失败模式与局限性

尽管 StaCOM 在 Core4D 数据集上取得了显著提升，但仍存在以下局限：

- **推理效率瓶颈**：物理仿真模块（PD 控制器 + CMA-ES）处理 128 帧序列约需 3 分钟，难以满足实时交互应用需求。CMA-ES 的迭代采样是主要计算瓶颈。
- **任务泛化能力未知**：实验仅在 Core4D 的搬运与转向场景上进行，对推拉、旋转等多样的协同操作类型以及多物体共操作场景的泛化能力尚未验证。
- **标注依赖性**：接触策略扩散模型的训练需要高质量的物体可执行性标注和接触注释，在噪声较大或缺少精细标注的场景下，接触锚点预测精度可能下降，进而影响整体生成质量。

### 关键图表结论

- **Table 1**：StaCOM 在所有物理合理性指标（Contact Acc. 0.44, Pene. 0.05）和运动质量指标（FID 25.5, IDF 0.22）上均优于现有方法，验证了意图-自然性-有效性三原则统一建模的有效性。
- **Table 2 / Figure 6**：消融实验揭示了各模块的因果链路——交互先验提升自然性，接触策略提升抓握精度，物理仿真消除穿透和悬浮，三者缺一不可。
- **Figure 4**：定性对比直观展示了 StaCOM 在抓握稳定性和响应同步性上的优势，基线方法在物体姿态突变时普遍出现滑移或延迟。

![[assets/figures/papers/paper_list_l10_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Stability_Driven_Mo/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison on Core4D-S1, showing manipulations generated by ComMDM, InterGen, and OMOMO (a–c), as well as our approach (d), at key timestamps t ∈ 0, 20, 40, 60, 80, 100. Our results (d) maintain coordinated grasps and stable payload alignment, whereas previous methods exhibit slipping contacts or delayed responses when the green object changes its pose*

### 补充图表

![[assets/figures/papers/paper_list_l10_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Stability_Driven_Mo/figures/006_Figure_5.jpg]]
*Figure 5: Cooperative motions produced by our framework. The two characters remain synchronized while steering and lifting the green object along the given trajectory, exhibiting fine-grained grasp readjustments throughout the interaction*



## 定位与知识库关联

### 1. 生成范式迁移：从扩散模型到 Flow Matching

StaCOM 的核心生成引擎建立在 **Flow Matching** 框架之上，这与当前主流的人体运动生成方法形成了范式层面的差异。现有工作普遍采用扩散模型（Diffusion Models）作为基础架构，例如 **MDM** 及其衍生方法通过逐步去噪生成运动序列。Flow Matching 则将生成过程重新表述为确定性向量场回归问题——学习一个从噪声分布到数据分布的连续传输映射。这一选择带来了两个关键优势：其一，推理时仅需 $K=10$ 步欧拉积分即可完成采样，相比扩散模型的数百步迭代具有理论上的效率优势；其二，确定性向量场天然适合嵌入梯度引导信号，为后续的接触策略校正和对抗性先验引导提供了统一的数学接口。

然而，这一范式迁移也引入了新的适用边界。Flow Matching 的确定性本质使其在需要高度随机性和多样性的场景中可能不如扩散模型的随机微分方程（SDE）采样灵活。论文中通过接触策略扩散模型的显式多样性生成来弥补这一不足，但整体框架的多样性上限仍受限于 Flow Matching 的确定性轨迹。

### 2. 与交互生成方法的定位关系

在人人-物交互生成这一具体任务上，StaCOM 与以下基线方法形成了清晰的差异化定位：

**OMOMO**（Li et al., TOG 2023）作为物体轨迹条件的人体运动生成方法，仅处理单人-物交互场景，缺乏对双人协调性的建模。StaCOM 通过引入双人交互判别器（Interaction Prior）和可执行性感知的接触策略，将问题空间从单人操作拓展至双人协同操作，同时在 Core4D-S1 上将接触精度从 Flow Matching 基线的 0.35 提升至 0.44。

**InterGen**（Liang et al., IJCV 2024）专注于多人交互生成，但缺乏对物体动态的显式建模。StaCOM 通过 BPS 特征编码物体的 6D 姿态和形状上下文，将物体轨迹作为核心条件信号注入生成过程，弥补了 InterGen 在物体引导方面的不足。

**InterDiff**（Xu et al., ICCV 2023）将物理信息引入扩散模型处理人-物交互，但其物理约束主要体现在训练阶段的数据增强层面。StaCOM 则更进一步，在推理阶段引入基于 CMA-ES 的稳定性驱动仿真，通过 PD 控制器直接纠正生成姿态中的穿透和不稳定问题。实验表明，仿真模块使穿透深度从 0.15 降至 0.05（Table 2），但代价是推理时间增加约 3 分钟（处理 128 帧），这在实时应用场景中构成显著劣势。

**CooHOI**（ref ）采用强化学习处理协作式人-物交互，但基于物理仿真器的训练使其难以泛化到新的物体形状和轨迹。StaCOM 的数据驱动生成范式具有更强的泛化潜力，但其对接触标注和可执行性标注的依赖又限制了在弱标注场景下的适用性。

### 3. 模块化设计的适用边界

StaCOM 的四个核心模块——BPS 特征提取、Flow Matching 生成网络、接触策略扩散模型、对抗性交互先验和稳定性驱动仿真——采用分阶段训练的模块化设计。这种设计使得各组件可以独立优化和复用，但也带来了系统复杂度的显著增加。具体而言：

- **接触策略扩散模型**依赖于物体可执行性场的预计算，这要求输入物体具有明确的几何结构和可执行性标注。对于非刚性物体或缺乏可执行性先验的场景，该模块的性能可能显著下降。
- **对抗性交互先验**中的双人交互判别器在训练时需要成对的双人运动数据，这限制了框架向三人及以上多人共操作任务的直接扩展。论文未提供多人扩展的实验证据，该方向仍为开放问题。
- **稳定性驱动仿真**作为推理时的后处理步骤，与 Flow Matching 生成过程相互独立。这种松耦合设计虽然便于实现，但也意味着仿真阶段的优化目标（物理稳定性）与生成阶段的目标（数据分布匹配）之间可能存在不一致，导致仿真校正后的运动偏离自然分布。论文未对这种偏离进行定量分析。

### 4. 知识库中的位置与未解决问题

StaCOM 在人体运动生成的知识图谱中占据了一个交叉节点——它将 Flow Matching 的生成范式、可执行性感知的接触推理、对抗性先验引导和物理仿真后处理整合为一个统一框架。这一整合策略的核心洞察在于：**协同操作中的多智能体与物体之间的紧耦合动态问题，需要将对象可执行性、双人交互协调性和物理稳定性显式编码为生成过程的引导信号**。

然而，以下开放问题限制了该框架的进一步推广：

1. **多人扩展的效率瓶颈**：将框架扩展到三人及以上的共操作任务时，交互判别器的输入维度将呈组合爆炸式增长，CMA-ES 优化的搜索空间也将急剧扩大。如何在保持模型效率和物理合理性的前提下实现多人扩展，论文未给出明确路径。

2. **端到端训练的可行性**：当前物理仿真模块与 Flow Matching 生成网络相互独立，导致推理效率低下。将物理仿真与生成过程更紧密地结合——例如通过可微分物理引擎实现端到端训练——是提升实用性的关键方向，但论文未对此进行探索。

3. **泛化能力的验证边界**：实验仅在 Core4D 数据集上进行，该数据集以搬运类操作为主。对于推拉、旋转等更复杂的协同操作类型，以及多物体共操作场景，StaCOM 的泛化能力尚未得到验证。这需要进一步在更多样化的基准上进行评估。

4. **标注依赖的鲁棒性**：框架对接触注释和物体可执行性标注的质量有较高依赖。在噪声较大或缺少标注的真实场景中，接触策略扩散模型的预测精度和物理仿真的校正效果可能同步退化。论文未对此类退化场景进行消融分析，该点需要手动验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/Stability_Driven_Motion_Generation_for_Object_Guided_Human_Human_Co_Manipulation.pdf]]
