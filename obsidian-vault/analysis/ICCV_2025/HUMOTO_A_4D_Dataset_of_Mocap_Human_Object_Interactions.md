---
title: HUMOTO A 4D Dataset of Mocap Human Object Interactions
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/HUMOTO_A_4D_Dataset_of_Mocap_Human_Object_Interactions.pdf
code_link: null
project_link: https://jiaxin-lu.github.io/humoto
aliases:
- HDCM
- H4DMHOI
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: Scene-Driven LLM Scripting生成有目的的动作序列，配合Rokoko EMF套装和双Kinect多模态捕捉，以及专业艺术家的两步质量保证。
primary_logic: 通过结合LLM驱动的有目的交互脚本生成、多模态传感器融合以及专业艺术家的严格清理，可以构建高质量、精细手部和多物体交互的数据集，显著改善物理真实性和动作自然性。
claims:
- HUMOTO在所有数据集中实现了最低的足部滑动（0.958 cm）和最低的穿透（0.0068 cm）。
- 在感知研究中，HUMOTO在总体质量上获得4.78±0.43分，且96%参与者偏好HUMOTO优于BEHAVE。
- HUMOTO的手部姿态和交互质量显著优于对比数据集。
- HUMOTO在人体运动相干性（0.653）和物体运动平滑性（jerk 1.13）上也表现最佳。
---

# HUMOTO A 4D Dataset of Mocap Human Object Interactions

> [!tip] 核心洞察
> 通过结合LLM驱动的有目的交互脚本生成、多模态传感器融合以及专业艺术家的严格清理，可以构建高质量、精细手部和多物体交互的数据集，显著改善物理真实性和动作自然性。

| 字段 | 内容 |
|------|------|
| 中文题名 | HUMOTO：一个包含动作捕捉人-物交互的4D数据集 |
| 英文题名 | HUMOTO A 4D Dataset of Mocap Human Object Interactions |
| 会议/期刊 | ICCV 2025 |
| Links |  [paper](https://arxiv.org/abs/2504.10414) · [Project](https://jiaxin-lu.github.io/humoto)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | HUMOTO Dataset Creation Methodology |
| Dataset | HOI Dataset Comparison, Perceptual Absolute Quality, Perceptual Pairwise Comparison |

> [!tip] 效果简介
> - HOI Dataset Comparison 上，Foot Sliding (cm) 0.958 vs 4.556 (BEHAVE) (减少3.598 cm)；Penetration (cm) 0.0068 vs 0.0606 (BEHAVE) (减少88.8%)；Motion SNR (dB) 9.42 vs 10.88 (Mixamo reference) (接近参考值)。
> - Perceptual Absolute Quality (Likert 1-5) 上，Overall Quality Score 4.78±0.43 vs 2.48±1.05 (BEHAVE) (+2.30)。
> - Perceptual Pairwise Comparison 上，Overall Quality Preference vs BEHAVE 96% (preferred HUMOTO) vs 4% (preferred BEHAVE) (显著偏好)。

## 概要

人-物交互（HOI）数据的获取长期受困于一个核心瓶颈：现有数据集普遍缺乏精细手部动作与多物体协同交互，且动作序列常伴随足部滑动、物体穿透等物理失真，缺乏明确的目的性。这些缺陷直接限制了相关下游任务（如具身智能、运动生成）的性能上限。

本文提出 **HUMOTO**，一个包含动作捕捉的4D人-物交互数据集。其核心洞察在于：通过将大语言模型（LLM）驱动的有目的交互脚本生成、多模态传感器融合（Rokoko EMF动捕服/手套 + 双Kinect RGB-D）以及专业艺术家的严格两步质量保证相结合，可以系统性地构建出具有精细手部姿态、高物理真实性和自然动作连贯性的高质量HOI数据。

**方法定位**：HUMOTO的方法论在三个关键环节上区别于现有数据集（如 **BEHAVE**、**OMOMO**、**IMHD**、**ParaHome**、**GRAB**）：
- **脚本生成**：从手动设计或有限的动作脚本，转变为基于场景驱动的LLM层次化脚本生成（Scene-Driven LLM Scripting），自动产生连贯且有目的性的交互序列。
- **动捕方案**：从纯光学动捕或单RGB-D相机，升级为电磁场动捕服/手套追踪人体与手部，配合双Kinect实现物体6DoF姿态追踪。
- **数据清洗**：从较少或自动化的后处理，转变为专业艺术家两步精炼与独立验证，重点消除足部滑动与物体穿透。

**主要结果**：定量评估（Table 1）表明，HUMOTO在所有对比数据集中实现了最低的足部滑动（0.958 cm）和最低的穿透深度（0.0068 cm），同时在人体运动相干性（0.653）和物体运动平滑性（jerk 1.13）上也表现最优。感知研究进一步验证了这一优势：HUMOTO在总体质量上获得4.78±0.43的Likert评分，且96%的参与者偏好HUMOTO优于BEHAVE。这些证据共同确认了所提方法在提升HOI数据物理真实性和交互自然性方面的有效性。

**局限与展望**：数据集当前仅包含一名表演者，可能引入体型和动作风格偏差；高保真度数据仍需大量手动清理，未来需探索更鲁棒的自动化清洗技术，并扩展表演者多样性。

### 核心瓶颈：现有HOI数据集的物理真实性与交互目的性缺失

人-物交互（Human-Object Interaction, HOI）数据是推动具身智能、机器人操作和运动生成等领域的基石。然而，现有HOI数据集普遍存在三个结构性缺陷，严重制约了下游应用的质量上限。

**第一，精细手部动作的缺失。** 多数数据集要么完全不含手部姿态数据，要么手部跟踪精度不足以支撑精细操作任务（如拧开瓶盖、拿起笔）。这导致从数据中学到的交互策略在面对需要精确手指协调的场景时表现不佳。

**第二，多物体交互场景的匮乏。** 现有数据集通常聚焦于单物体交互，难以反映真实世界中“在厨房里同时操作锅、铲和调料瓶”这类多物体协同的复杂场景。

**第三，物理真实性不足。** 这是最关键的瓶颈——现有数据集普遍存在两类物理伪影：
- **足部滑动（Foot Sliding）**：角色脚部在地面上不自然地漂移，破坏了接触约束的真实感。
- **物体穿透（Penetration）**：物体穿入人体网格，违反了基本的物理碰撞约束。

这些问题的根源在于：传统数据采集流程缺乏对“有目的交互”的顶层设计。动作脚本往往是手动设计的简单重复动作，缺乏连贯的叙事目的，导致采集到的动作虽然局部正确，但整体缺乏人类行为的自然连贯性。

### 方法缺口：从“捕捉动作”到“设计交互”

现有数据集的构建范式可以概括为“先采集，后清理”——依赖纯光学动捕或单RGB-D相机记录动作，再通过自动化后处理修复伪影。这种范式存在两个根本性局限：

1. **脚本生成的随意性**：手动设计的动作脚本难以覆盖物体功能部件的完整使用方式，且缺乏场景上下文的连贯性。例如，“拿起杯子”这一动作可以有数十种不同的执行方式（从桌上拿起、从柜中取出、递给他人的过渡动作等），手动枚举几乎不可能穷尽。

2. **后处理的被动性**：自动化清理算法（如基于优化的足部接触约束）只能缓解部分伪影，无法从根本上消除物理不一致。专业艺术家的手动精修虽然有效，但成本高昂，且现有数据集很少将其纳入标准流程。

### 本文动机：构建高质量、有目的、多模态的HOI数据集

针对上述瓶颈，HUMOTO的动机明确且聚焦：**通过系统性地改进数据采集的全链条——从脚本生成到传感器融合再到质量控制——构建一个在物理真实性和交互自然性上显著优于现有数据集的新基准。**

具体而言，HUMOTO从三个维度切入：

- **有目的的交互设计**：引入Scene-Driven LLM Scripting框架，利用大语言模型（LLM）自动生成具有场景上下文和叙事连贯性的交互脚本，确保每个动作序列都有明确的目的性和自然过渡。
- **多模态传感器融合**：结合Rokoko EMF动捕套装（用于身体和手部跟踪）与双Kinect RGB-D传感器（用于物体姿态跟踪），在保证人体运动精度的同时，实现物体6DoF姿态的鲁棒捕捉。
- **专业级质量保证**：建立两阶段艺术家清理与独立验证流程，将足部滑动和物体穿透等物理伪影降至最低水平。

这一动机的核心洞察在于：**高质量HOI数据不是“捕捉”出来的，而是“设计”出来的——需要从脚本的叙事目的、传感器的互补融合、到艺术家的物理验证形成闭环。**

## 核心方法与创新机理

HUMOTO的核心创新在于系统性地解决了现有HOI数据集在交互质量、物理真实性和动作目的性上的三个关键瓶颈，通过**方法链式重构**实现了数据质量的跨越式提升。

### 创新一：Scene-Driven LLM Scripting——从无目的动作到有目的交互

传统HOI数据集（如BEHAVE、GRAB）的动作脚本多依赖手动设计或有限的动作模板，导致交互序列缺乏连贯的目的性。HUMOTO引入了**Scene-Driven LLM Scripting框架**（见 Figure 2），其核心机制是：

1. **场景化对象聚类**：将63个日常物体按功能逻辑分组为概念性“房间”（如厨房、办公室），建立交互的语义上下文。
2. **层次化LLM提示**：先为每个场景生成可能的交互清单，再针对单个物体提示LLM生成详细的、有目的性的动作序列脚本。
3. **多层级文本标注**：每条序列配有标题、短脚本和长脚本三级文本描述，为下游任务提供不同粒度的语义监督。

**因果机制**：LLM生成的脚本赋予了动作明确的目的性和时间连贯性，从根本上解决了现有数据集中常见的“为动而动”问题。定量证据表明，HUMOTO在人体运动相干性（Coherence）上达到0.653，在所有对比数据集中排名第一（Table 1），直接验证了脚本驱动对运动质量的提升效果。

### 创新二：多模态传感器融合——精细手部与多物体交互的同步捕捉

现有数据集普遍缺乏精细手部姿态数据（如BEHAVE无手部数据）或仅支持单物体交互。HUMOTO的采集系统采用**双模态互补架构**（见 Figure 3）：

- **电磁场动捕**：Rokoko EMF套装和手套实现人体全身及手部的高精度跟踪，不受光学遮挡影响。
- **双Kinect RGB-D**：从两个视角同步记录物体6DoF姿态，配合FoundationPose算法和基于SAM2掩膜差异的动态复位机制，确保物体跟踪的鲁棒性。

**因果机制**：EMF手套捕捉的精细手部姿态（见 Figure 1 中手部细节）填补了现有数据集的空白；双Kinect配置解决了单视角物体跟踪在交互遮挡下的失效问题。Table 2显示HUMOTO是唯一同时具备手部数据、身体数据并支持场景中最多物体的数据集之一。

### 创新三：专业艺术家两步质量保证——物理真实性的最后防线

动捕数据的后处理是决定数据集物理真实性的关键环节，但现有数据集多依赖自动化清理或仅进行有限的人工干预。HUMOTO引入了**两步专业艺术家质量保证机制**（Section 3.3）：

1. **技术精炼**：专业艺术家对动捕数据进行清理，重点关注足部滑动和物体穿透等常见伪影。
2. **独立验证**：由不同艺术家进行独立质量审查，确保清理效果的一致性。

**因果机制**：这一严格的人工质量保证流程直接转化为物理真实性指标的显著优势。Table 1的定量结果显示：
- **足部滑动**：0.958 cm，较BEHAVE的4.556 cm降低79.0%。
- **物体穿透**：0.0068 cm，较BEHAVE的0.0606 cm降低88.8%。

两项指标均为所有对比数据集中的最优值，证明了专业人工清理在消除动捕伪影方面的不可替代性。

### 创新总结：方法链的协同效应

上述三个创新并非孤立存在，而是形成了**“脚本设计→多模态采集→专业清理”的完整质量保障链**。LLM脚本提供了交互的目的性框架，多模态传感器捕获了实现该框架所需的精细数据，而艺术家清理则消除了采集过程中的物理伪影。感知研究结果（Section 4.2.2）为这一协同效应提供了强有力的佐证：HUMOTO在总体质量上获得4.78±0.43分（5分制），96%的参与者偏好HUMOTO优于BEHAVE，交互质量偏好更是达到94%。

HUMOTO 数据集的构建遵循一条端到端的“脚本生成—多模态采集—对象跟踪—质量清洗—标注”流水线，其核心设计目标是解决现有 HOI 数据集中普遍存在的足部滑动、物体穿透、手部姿态粗糙以及交互缺乏目的性等问题。

流水线由五个主要模块串联构成，数据从高层语义逐步转化为可供下游任务直接使用的 4D 交互动画与多层级文本标注。

### 模块关系与数据流

**1. Script Development via LLM（动作脚本生成）**
流水线的起点是 **Scene-Driven LLM Scripting** 框架。该模块首先将 63 个标准家居物品按功能场景聚类为概念性“房间”，然后将房间内的物品组合提供给大语言模型，通过层级化提示词自动生成具有明确目的和连贯动作序列的交互脚本。这一设计替代了传统的手动脚本编写，为后续动捕提供了语义丰富且物理合理的动作蓝图。

**2. Capture Environment Setup（采集环境标定）**
在物理采集阶段，搭建了包含双 Kinect RGB-D 传感器、舞台、灯光及标定板的专用环境。通过表演者在标准化位置的标定流程，实现 EMF 动捕服坐标系与相机坐标系之间的精确对齐，为后续多模态数据融合提供空间基准。

**3. Motion Capture & Object Tracking（运动捕捉与物体跟踪）**
人体运动捕捉采用 **Rokoko EMF 智能套装与手套**，直接获取身体与手部的精细姿态，避免了纯光学方案中常见的遮挡和足部滑动问题。物体 6DoF 姿态则通过双 Kinect 的 RGB-D 数据流，由 **FoundationPose** 算法进行逐帧估计，并辅以基于掩膜像素差异的动态复位机制和 SAM2 辅助分割，以应对交互过程中的遮挡和快速运动。

**4. Data Cleaning and Verification（数据清洗与验证）**
原始采集数据进入两阶段质量保证流程：首先由专业艺术家进行技术精修，重点解决足部滑动、物体穿透和手部姿态异常等问题；随后由独立艺术家进行验证。这一严格的清洗机制是 HUMOTO 在物理真实性指标上大幅领先其他数据集的关键因果环节。

**5. Annotation（文本标注）**
清洗后的序列被赋予多层级文本标注，包括标题、短脚本和长脚本，为文本驱动的运动生成等下游任务提供不同粒度的语义对应。

### 输入输出概览

- **输入**：63 个经艺术家精细建模的家居物品（含 72 个功能部件）、LLM 生成的交互脚本、表演者动作。
- **输出**：包含 SMPL-X 人体参数、物体 6DoF 姿态、手部关节数据、多层级文本标注的 4D HOI 序列。数据集总计包含 41 个场景、超过 120 分钟的交互动画。

该流水线的核心设计哲学在于将 LLM 的语义规划能力、多模态传感器的互补优势以及专业艺术家的人工精修有机结合，从而在自动化效率和数据质量之间取得平衡。

### 数据采集管道核心模块

HUMOTO数据集的构建依赖于一条精心设计的多阶段采集管道，其核心模块如下：

**1. 基于LLM的场景驱动脚本生成 (Scene-Driven LLM Scripting)**
该模块解决了现有HOI数据集动作缺乏目的性和自然连贯性的瓶颈。其工作机制是：首先将采集到的63个日常物品按功能逻辑分组为概念性“房间”（如厨房、办公室），然后将这些分组和物品信息提供给大语言模型（LLM），由LLM自动生成具有层次结构的交互动作脚本。如Figure 2所示，该框架从目标场景出发，准备相关交互对象，最终利用LLM生成详细的动作脚本，确保了动作序列的上下文连贯性和目的性。

**2. 多模态动捕与物体跟踪**
该模块采用电磁场（EMF）技术与视觉传感器融合的方案，以克服纯光学动捕在精细手部交互和物体姿态获取上的局限。具体而言：
- **人体运动捕捉**：表演者穿戴Rokoko EMF智能套装和配对手套，直接获取身体和手部的精确运动数据，避免了光学遮挡问题。
- **物体6DoF姿态跟踪**：双Kinect RGB-D传感器从不同视角记录物体点云，利用FoundationPose算法分析视觉数据以确定物体的6自由度姿态。为解决快速运动或遮挡导致的跟踪丢失，系统引入了一种基于掩膜像素差异的动态复位机制，并借助SAM2辅助生成物体掩膜以提高跟踪鲁棒性。

**3. 专业艺术家两级质量保证 (Two-Stage QA)**
这是确保数据物理真实性的关键模块。采集的原始数据需经过两级专业处理：首先由艺术家进行技术精炼，重点解决足部滑动、物体穿透等常见伪影；随后由另一组艺术家进行独立验证，确保精炼质量。这一严格的人工清理流程是HUMOTO在物理指标上显著优于其他数据集的核心原因。

### 关键公式与评估指标推导

为量化评估数据集质量，HUMOTO定义了一系列评估指标，其公式及物理含义如下：

**1. 足部滑动 (Foot Sliding)**
衡量足部关节在地面接触期间的不自然水平滑动距离。值越低表示足部运动越真实。

$$ \mathrm{Sliding}_j = N_f \sum_{t\in S_j} \| \mathbf{p}_{j,t+1}^{xy} - \mathbf{p}_{j,t}^{xy} \|_2 \cdot (2 - 2^{(\mathbf{p}_{j,t}^z / H_j)}) $$

其中，$S_j$ 表示足部关节 $j$ 与地面接触的时间帧集合，$N_f$ 为归一化因子，$\mathbf{p}_{j,t}^{xy}$ 为关节 $j$ 在时刻 $t$ 的水平位置，$\mathbf{p}_{j,t}^z$ 为垂直高度，$H_j$ 为参考高度阈值。指数项 $(2 - 2^{(\mathbf{p}_{j,t}^z / H_j)})$ 作为权重，使得越接近地面的帧对滑动的惩罚越大。

**2. 运动平滑度 (Jerk)**
通过测量加速度的变化率来量化运动的平滑程度。Jerk值越低，运动越平滑自然。

$$ \mathrm{Jerk} = \frac{1}{N_f - 3} \sum_{t=1}^{N_f-3} \| \mathbf{a}_{t+1} - \mathbf{a}_t \|_2 $$

其中，$N_f$ 为总帧数，$\mathbf{a}_t$ 为时刻 $t$ 的关节加速度向量。该公式计算相邻帧间加速度差的L2范数的平均值。

**3. 运动信噪比 (Motion Signal-to-Noise Ratio, MSNR)**
通过比较平滑后与原始关节速度的信噪比来评估运动质量，值越高表示有用运动信号相对于噪声越强。

$$ \mathrm{SNR} = 10 \log_{10} \left( \frac{ \mathbb{E}[ \hat{v}^2 ] }{ \mathbb{E}[ |v - \hat{v}|^2 ] } \right) $$

其中，$v$ 为原始关节速度，$\hat{v}$ 为经过低通滤波平滑后的速度，$\mathbb{E}[\cdot]$ 表示期望值。分子为平滑信号的平均功率，分母为噪声（原始信号与平滑信号之差）的平均功率。

**4. 运动相干性 (Coherence)**
通过测量姿态簇内紧凑度来量化运动的一致性，值越高表示动作模式越集中、越连贯。

$$ C = 1 - \frac{\mu_d}{\max_d} $$

其中，$\mu_d$ 为姿态簇内各姿态到聚类中心的平均距离，$\max_d$ 为所有姿态到中心的最大距离。该指标归一化到 $[0,1]$ 区间，越接近1表示相干性越好。

**5. 运动多样性 (Diversity)**
使用姿态簇的归一化香农熵来量化运动模式的多样性，值越高表示动作类型越丰富。

$$ D = - \frac{ \sum_{i=1}^{n} p_i \log_2 p_i }{ \log_2 n } $$

其中，$n$ 为姿态簇的数量，$p_i$ 为第 $i$ 个簇中姿态的比例。分母 $\log_2 n$ 为最大可能熵，用于归一化。

**6. 物体穿透 (Penetration)**
通过物体点与人体网格的带符号距离衡量物体穿入人体的程度，正值表示穿透发生。

$$ \mathrm{Penetration}(t) = \min_{p \in \mathcal{P}_{obj}} d(p, \mathcal{M}_h) $$

其中，$\mathcal{P}_{obj}$ 为物体表面采样点集，$\mathcal{M}_h$ 为人体网格，$d(p, \mathcal{M}_h)$ 为点 $p$ 到人体网格的带符号距离函数（正值表示点在网格内部，即穿透）。

**7. 接触熵 (Contact Entropy)**
量化交互状态转换的多样性，值越高表示交互模式越复杂多样。

$$ \operatorname{Entropy} = - \sum_{i,j} p(s_i \to s_j) \log_2 p(s_i \to s_j) $$

其中，$p(s_i \to s_j)$ 为从交互状态 $s_i$ 转移到 $s_j$ 的经验概率。该指标捕捉了交互动态的丰富程度。

**8. 状态一致性 (State Consistency)**
通过平均运行长度与序列长度的比率衡量交互状态的时间稳定性，得分越高表示交互状态越稳定持久。

$$ \mathrm{Consistency} = \frac{1}{N_p} \sum_{p=1}^{N_p} \frac{ \mathrm{Avg.\ Run\ Length}_p }{ \mathrm{Sequence\ Length} } $$

其中，$N_p$ 为序列总数，$\mathrm{Avg.\ Run\ Length}_p$ 为第 $p$ 个序列中交互状态的平均持续帧数。该指标归一化后，值越接近1表示状态越稳定。

![[assets/figures/papers/paper_list_l1768_HUMOTO_A_4D_Dataset_of_Mocap_Human_Object_Interactions/figures/002_Figure_3.jpg]]
*Figure 3: Capture environment. Left: Overview of our capturing environment showing two Kinect cameras, stage, lighting, calibration board, and interaction objects. Right: Calibration procedure with the performer in a standardized position, enabling precise alignment between mocap suit data and camera coordinates*

## 实验与关键发现

### 数据集定量评估

HUMOTO在多个物理真实性指标上全面超越现有HOI数据集。**Table 1**展示了跨数据集的定量对比，所有指标定义详见附录A.2.2。

![[assets/figures/papers/paper_list_l1768_HUMOTO_A_4D_Dataset_of_Mocap_Human_Object_Interactions/figures/006_Table_1.jpg]]
*Table 1: Quantitative evaluation across human-object interaction datasets. Metrics defined in Appendix A.2.1 should be interpreted holistically, as optimal values depend on specific applications. The table includes two additional statistical indicators that provide context for understanding dataset characteristics. Bold indicates best, underline indicates second-best. ↑: higher values are better, ↓: lower values are better, and →: values closer to Mixamo are better*

**足部滑动与穿透**：HUMOTO实现了最低的足部滑动值（0.958 cm），较BEHAVE的4.556 cm减少约79%；物体穿透深度仅为0.0068 cm，较BEHAVE的0.0606 cm降低88.8%。这两项关键指标直接反映了专业艺术家两步质量保证流程的有效性——技术精炼与独立验证相结合，系统性地消除了动捕数据中常见的物理伪影。

**运动质量指标**：HUMOTO在人体运动相干性（Coherence）上达到0.653，为所有对比数据集最优，表明其动作序列具有高度的时间一致性。物体运动平滑性方面，Jerk值仅为1.13，同样排名第一，说明物体轨迹加速度变化平缓，无突变抖动。运动信噪比（MSNR）为9.42 dB，接近Mixamo参考值10.88 dB，证明经过清理后的数据保留了高质量的运动信号。

**交互复杂度**：接触熵（Contact Entropy）和状态一致性（State Consistency）两项统计指标进一步揭示了HUMOTO的交互丰富性。高接触熵值表明手-物接触状态转换模式多样，而状态一致性得分反映了交互动作的时间稳定性。这两个维度共同刻画了HUMOTO在保持物理真实性的同时，提供了比BEHAVE、OMOMO等数据集更丰富的交互模式。

### 感知质量研究

为验证定量指标的感知相关性，作者开展了用户研究，邀请参与者在绝对质量评分（5点Likert量表）和成对比较两个维度上评估HUMOTO与BEHAVE、OMOMO、IMHD、ParaHome的质量差异。

**绝对质量评分**（**Figure 12**）：HUMOTO在总体质量上获得4.78±0.43的高分，远超BEHAVE的2.48±1.05。在人体运动质量、物体运动质量和交互质量三个子维度上，HUMOTO均获得最高评分，且标准差最小，表明参与者对HUMOTO的质量评价高度一致。

**成对比较**（**Figure 13**）：在总体质量偏好上，96%的参与者选择HUMOTO优于BEHAVE；交互质量维度上，94%偏好HUMOTO。与OMOMO和ParaHome的对比中，HUMOTO分别在总体质量上获得65%和67%的偏好率。值得注意的是，在物体运动质量维度上，HUMOTO对ParaHome的优势最为显著，这直接归因于FoundationPose跟踪结合动态复位机制带来的精确物体姿态估计。

### 定性对比分析

**手部姿态与交互精度**（**Figure 6**）：HUMOTO提供了精细的手指关节运动数据，这得益于Rokoko EMF手套的直接捕捉。与BEHAVE和GRAB相比，HUMOTO的手部姿态在抓握物体时表现出更自然的关节弯曲角度和接触点分布。Figure 6的接触图可视化显示，HUMOTO的手-物接触区域与物体功能部件高度吻合，而对比数据集常出现手指穿透或悬空现象。

**机器人学应用验证**（**Figure 8**）：在仿真环境中复现“坐姿持杯”动作时，HUMOTO数据驱动的人体模型几乎无位移漂移，而ParaHome数据在相同动作下出现显著的物体位移。手部操作对比中，HUMOTO的抓握姿态与DexGraspNet生成的机器人抓取形成互补——前者提供自然的人类示范，后者提供物理可行的力闭合方案，二者结合可为机器人模仿学习提供更完整的训练数据。

**姿态估计基准测试**（**Figure 9**）：将HUMOTO的渲染图像作为输入，测试4D Humans和TRAM两种现有姿态估计方法。结果显示，两种方法在HUMOTO的高质量真值骨架上均能产生合理估计，但在精细手部姿态和手-物接触区域仍存在明显偏差，表明HUMOTO可作为评估和提升姿态估计算法的严格基准。

### 运动生成的下游任务验证

**Figure 7**展示了MotionGPT在HUMOTO文本标注上的运动生成结果。短脚本生成的动作仅能捕捉粗粒度的交互意图，长脚本虽提供了更多细节约束，但生成的运动序列在手部精细动作和物体交互时序上仍与HUMOTO真值存在显著差距。这一对比揭示了两点：其一，HUMOTO的多层级文本标注（标题、短脚本、长脚本）为运动生成模型提供了可控的评估梯度；其二，当前文本到运动生成方法在细粒度HOI建模上仍有巨大提升空间，HUMOTO可作为高质量训练和评估数据源。

### 数据集统计特征

**Table 2**汇总了HUMOTO与对比数据集的统计信息。HUMOTO包含7,537秒的总时长，覆盖63个物体和72个功能部件，支持单场景最多4个物体的同时交互。与BEHAVE、GRAB等数据集相比，HUMOTO在物体多样性、手部数据完整性和多物体交互支持上具有明显优势。**Figure 11**进一步揭示了物体出现频率和序列时长分布：移动物体（如球、椅子）和静止物体（如桌子、架子）的交互场景均衡覆盖，序列时长集中在中等范围，避免了过长或过短序列对训练造成的偏差。

### 局限性与失败模式

尽管HUMOTO在各项指标上表现优异，但数据集构建过程中的固有局限值得关注：

1. **单一表演者偏差**：由于EMF动捕服尺寸限制，数据集仅包含一名表演者，可能引入特定体型和运动风格的偏差。在姿态估计和运动生成任务上使用HUMOTO训练时，模型可能对该表演者的身体比例和动作习惯产生过拟合。未来需扩展表演者多样性以缓解此问题。

2. **手动清理成本**：两步质量保证流程虽然保证了数据质量，但需要专业艺术家的大量投入。这一资源瓶颈限制了数据集的快速扩展能力。开发更鲁棒的自动化清理技术——特别是针对足部滑动和物体穿透的自动检测与修正——是降低构建成本的关键方向。

3. **OMOMO异常现象的启示**：定量评估中发现OMOMO数据集呈现高SNR同时高Jerk的现象，即信号干净但加速度变化剧烈。这一矛盾提示现有指标可能无法完全捕捉运动自然性的所有维度，未来需要开发更综合的感知对齐评估框架。

![[assets/figures/papers/paper_list_l1768_HUMOTO_A_4D_Dataset_of_Mocap_Human_Object_Interactions/figures/007_Figure_6.jpg]]
*Figure 6: Quality comparison. We compare different datasets on motion dynamics, hand pose accuracy, and object meshes*

![[assets/figures/papers/paper_list_l1768_HUMOTO_A_4D_Dataset_of_Mocap_Human_Object_Interactions/figures/009_Figure_8.jpg]]
*Figure 8: Data for Robotics. Top: Two simulator visualizations showing human sitting and holding mug. HUMOTO (left) displays minimal displacement, while ParaHome (right) shows significant object displacement during identical actions. Bottom: Hand manipulation comparison between HUMOTO (left) and simulated robotic grasps from DexGraspNet (right)*

![[assets/figures/papers/paper_list_l1768_HUMOTO_A_4D_Dataset_of_Mocap_Human_Object_Interactions/figures/010_Figure_9.jpg]]
*Figure 9: Human motion and pose estimation results on HUMOTO. Comparison between 4D Humans [19] (Mid) and TRAM [64] (Bottom) on rendered images, showing estimated meshes (colored) against ground truth skeleton (white)*

![[assets/figures/papers/paper_list_l1768_HUMOTO_A_4D_Dataset_of_Mocap_Human_Object_Interactions/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the HUMOTO dataset. The dataset contains mocap 4D human-object interaction animations with multiple objects. The unique features of the dataset include its detailed, accurate interaction modeling, specifically the detailed hand pose. The objects are precisely modeled by artists. We additionally provide different abstract levels of text annotation for the interactions*

## 定位与知识库关联

### 核心改进点与基线对比

HUMOTO的构建方法论针对现有HOI数据集的三个关键瓶颈进行了系统性改进：

1. **脚本生成**：从手动设计或有限的动作脚本，转向**Scene-Driven LLM Scripting**框架。该方法首先将63个家居物体按逻辑分组为概念性“房间”，然后利用大语言模型自动生成具有目的性和连贯性的交互序列。这解决了现有数据集中动作缺乏上下文和目的性的问题，使采集的动作更贴近真实人类行为。

2. **动捕系统**：从纯光学动捕或单RGB-D相机方案，转向**多模态传感器融合**——Rokoko电磁场（EMF）套装和手套追踪人体和手部运动，双Kinect RGB-D传感器记录物体6DoF姿态。这种组合解决了光学动捕中常见的遮挡问题，并首次在HOI数据集中实现了对手部精细动作的系统性捕捉。

3. **数据清理**：从较少或自动化的后处理，转向**专业艺术家两步质量保证**——先由艺术家进行技术精炼，再由独立人员进行验证，特别关注足部滑动和物体穿透等物理真实性问题。

这些改进的因果效应在定量评估中得到验证：HUMOTO的足部滑动（0.958 cm）比BEHAVE（4.556 cm）减少78.9%，穿透深度（0.0068 cm）比BEHAVE（0.0606 cm）降低88.8%（Table 1）。感知研究进一步证实，96%的参与者偏好HUMOTO优于BEHAVE，总体质量评分达4.78±0.43（Section 4.2.2）。

### 在HOI数据集谱系中的定位

HUMOTO填补了现有数据集的以下空白：

- **相对于BEHAVE**：BEHAVE提供了多物体交互场景，但缺乏精细手部姿态数据，且存在明显的足部滑动和穿透问题。HUMOTO通过EMF手套捕捉和严格清理流程弥补了这些缺陷。

- **相对于GRAB**：GRAB专注于手-物交互，提供了高质量的手部姿态，但仅包含单一物体交互且缺少全身运动。HUMOTO扩展为全身运动与多物体交互的结合。

- **相对于OMOMO**：OMOMO同样使用多模态动捕，但在定量评估中表现出高SNR伴随高jerk的异常现象——信号干净但包含突变，这一现象的成因尚待研究。HUMOTO在运动平滑性（jerk 1.13）和相干性（0.653）上均表现更优。

- **相对于ParaHome**：ParaHome提供了家庭场景的全身交互数据，但在物体位移精度上存在不足。Figure 8的机器人学对比显示，相同动作下ParaHome出现显著物体位移，而HUMOTO保持了精确的空间关系。

- **相对于IMHD**：IMHD提供了手部数据，但在运动质量和交互多样性上不及HUMOTO。

### 适用边界

HUMOTO的方法论适用于以下场景，但存在明确限制：

1. **表演者偏差**：由于动作捕捉服的尺寸限制，数据集仅包含一名表演者。这引入了对特定人体体型和运动风格的偏差，可能影响基于该数据训练的模型在多样化人群上的泛化能力。对于需要覆盖广泛人体测量学差异的应用（如面向不同体型用户的机器人交互），需要手动验证或补充数据。

2. **资源需求**：高质量数据的生成依赖于大量手动清理和精炼工作。尽管这保证了数据质量，但对于希望快速扩展数据规模的研究者而言，这种资源投资可能不可行。自动化清理技术的缺失是该方法论的一个关键限制。

3. **场景覆盖**：63个家居物体覆盖了常见的交互类型，但数据集仅限于室内家庭场景。对于工业操作、户外活动或专业工具使用等场景，需要重新设计物体集合和脚本生成流程。

### 开放问题

1. **表演者多样性扩展**：如何减轻单一表演者带来的体型偏差，实现多人多样化的HOI数据采集？可能的路径包括开发可调节的动捕服，或通过运动重定向技术将捕获的运动适配到不同体型模型上，但这两种方案都需要验证物理真实性的保持程度。

2. **自动化清理技术**：如何减少高保真度交互数据收集中的手动清理工作量？当前的两阶段艺术家清理流程是质量保证的核心，但也构成了扩展瓶颈。开发能自动检测和修正足部滑动、穿透等问题的鲁棒算法，同时不损失交互细节，是一个关键研究方向。

3. **OMOMO异常现象**：OMOMO数据集中观察到的高SNR同时伴随高jerk的现象，其成因和影响值得进一步研究。理解这一现象可能揭示动捕系统选择或后处理流程对运动质量的隐藏影响。

4. **LLM脚本的真实性边界**：Scene-Driven LLM Scripting生成的脚本是否可能引入语言模型固有的偏差或“幻觉”交互？当前缺乏对LLM生成动作脚本与真实人类行为分布之间差异的系统性研究。

## 原文 PDF

![[paperPDFs/ICCV_2025/HUMOTO_A_4D_Dataset_of_Mocap_Human_Object_Interactions.pdf]]
