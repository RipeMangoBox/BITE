---
title: ParaHome Parameterizing Everyday Home Activities Towards 3D Generative Modeling of Human Object Interactions
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/ParaHome_Parameterizing_Everyday_Home_Activities_Towards_3D_Generative_Modeling_of_Human_Object_Interactions.pdf
project_link: https://jlogkim.github.io/parahome
code_link: null
aliases:
- PPEHAT3GMHOI
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过集成多视角RGB相机与IMU可穿戴设备的异构系统，并设计3D ArUco立方体标记及身体/手部空间校准方法，实现了对复杂交互场景中人体与物体的鲁棒、精确跟踪。
primary_logic: 将人体（SMPL-X）和物体（含关节状态）参数化至统一的时空空间，辅以文本描述，为学习人类日常活动的生成式模型提供了结构化基础；3D立方体标记有效解决了交互中的遮挡问题，异构系统校准确保了多尺度运动的高精度一致性。
claims:
- 3D立方体标记方案在交互期间的跟踪成功率远优于表面标记（1.0 vs 0.76-0.93）
- 手部校准后的平均位置误差仅11毫米（86次触摸）
- 身体校准优化显著减少了骨架偏移（Fig. 4前后对比）
- 混合ParaHome与HumanML3D训练使MDM在文本条件运动生成上超越TEMOS和T2M（RPrecision top3 0.73 vs 0.68/0.38）
---

# ParaHome Parameterizing Everyday Home Activities Towards 3D Generative Modeling of Human Object Interactions

> [!tip] 核心洞察
> 将人体（SMPL-X）和物体（含关节状态）参数化至统一的时空空间，辅以文本描述，为学习人类日常活动的生成式模型提供了结构化基础；3D立方体标记有效解决了交互中的遮挡问题，异构系统校准确保了多尺度运动的高精度一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | ParaHome：日常家居活动参数化与三维人-物交互生成建模 |
| 英文题名 | ParaHome Parameterizing Everyday Home Activities Towards 3D Generative Modeling of Human Object Interactions |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](https://jlogkim.github.io/parahome) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ParaHome |
| Dataset | System tracking robustness, Text-to-motion, Object-guided motion |

> [!tip] 效果简介
> - System tracking robustness 上，Tracking Success Ratio 1.0 (3D cube marker) vs 0.76 (4 surface markers) (+0.24)。
> - Text-to-motion (ParaHome+HumanML3D mixed) 上，Multimodal dist ↓ 3.75 (MDM mixed) vs 4.32 (MDM HumanML3D) (-0.57)；RPrecision top3 ↑ 0.73 vs 0.68 (+0.05)。
> - Object-guided motion (Refrigerator) 上，MPE glb-joints (cm) ↓ 6.57 vs 9.26 (-2.69)。

## 概要

现有的人-物交互（HOI）数据集普遍存在一个关键瓶颈：无法在自然的家庭环境中，同时以高精度捕获人体全身运动、精细手部动作以及物体的六自由度轨迹。更关键的是，这些数据缺乏统一的参数化表示和对应的文本描述，使得基于生成式模型来学习和合成日常活动变得极为困难。

ParaHome 系统通过一套异构捕获方案解决了上述问题。其核心思路是集成一个由 70 台同步 RGB 相机组成的多视角阵列与一套基于 IMU 的可穿戴动作捕捉设备（包含身体套装和手套），并设计了一种 3D ArUco 立方体标记方案，用于鲁棒地跟踪交互中的物体。为了将多源数据统一到同一时空坐标系下，系统引入了身体空间对齐与手部精细校准两个关键模块，有效解决了多尺度运动的高精度一致性问题。

最终，ParaHome 将人体（采用 SMPL-X 参数化模型）与物体（包含关节状态）统一表示为一个结构化的时空状态序列，并辅以文本描述。这一参数化体系为下游的生成式建模奠定了坚实基础。在验证实验中，混合 ParaHome 与 HumanML3D 数据训练的扩散模型（MDM）在文本条件运动生成任务上显著超越了 **TEMOS**（Petrovich et al., ECCV 2022）和 **T2M**（Guo et al., CVPR 2022），RPrecision top3 达到 0.73。在物体引导的运动合成任务中，加入初始相对空间线索可将全局关节位置误差降低约 30%。系统层面的评估也证实，3D 立方体标记的跟踪成功率远优于传统表面标记方案（1.0 vs 0.76–0.93），手部校准后的平均指尖位置误差仅为 11 毫米。



**核心瓶颈：现有HOI数据集在自然家庭环境中无法同时捕获高精度人体全身运动、精细手部运动和物体轨迹，也缺乏统一参数化表示与文本描述，制约了生成式建模研究。**

### 问题背景

理解人类在日常家庭环境中如何与物体交互，是计算机视觉和具身智能领域的核心挑战之一。从打开抽屉、操作水壶到使用洗衣机，这些看似简单的日常活动涉及复杂的人-物时空关系：人体全身运动提供全局上下文，手部精细操控决定任务成败，物体的刚性位移与关节状态则构成交互的另一半。然而，现有的人-物交互（HOI）数据集在捕获这些多尺度运动时存在根本性缺口——

- **多尺度运动捕获的割裂**：现有数据集要么专注于全身运动而忽略手部细节，要么在受控实验室环境中记录手部动作而丢失自然家庭场景的上下文。尚无系统能在真实家庭环境中同时以高精度捕获人体全身运动、双手手指运动和物体六自由度轨迹。
- **参数化表示的缺失**：大多数数据集以原始传感器数据（RGB图像、深度图、骨架点）形式存在，缺乏将人体（如SMPL-X参数模型）和物体（含关节状态）统一到同一时空坐标系下的结构化参数化表示，这直接阻碍了生成式模型的学习。
- **文本描述的匮乏**：自然语言描述是连接视觉感知与语义理解的关键桥梁，但现有HOI数据集极少提供细粒度的文本注释，使得文本条件的人-物交互生成研究几乎无法开展。

### 现有方法缺口

从方法论层面审视，现有HOI捕获系统面临三个关键技术瓶颈：

1. **物体跟踪的遮挡困境**：在人与物体紧密交互时，附着于物体表面的传统标记极易被手或身体遮挡，导致跟踪失败。**Surface marker tracking**（Nan Jiang et al., ICCV 2023）等方案在交互期间的跟踪成功率仅为0.76–0.93，无法满足高精度建模需求。

2. **异构传感系统的空间对齐难题**：多视角相机系统与可穿戴IMU动作捕捉设备各自拥有独立的坐标系。若不经精确校准，从IMU解算的骨骼运动与相机重建的物体轨迹之间存在系统性偏移，导致人-物空间关系失真。现有方案普遍缺乏针对这一异构系统的鲁棒校准方法。

3. **生成式建模的数据基础薄弱**：以**TEMOS**（Petrovich et al., ECCV 2022）、**T2M**（Guo et al., CVPR 2022）和**MDM**（Tevet et al., arXiv 2022）为代表的文本到运动生成模型，其训练数据（如HumanML3D）主要涵盖孤立的人体动作，缺乏与物体交互的配对数据，导致模型无法理解“拿起杯子”与“打开柜门”这类目标导向行为的空间语义。

### 本文动机

针对上述缺口，本文提出**ParaHome**——一个面向日常家居活动参数化捕获与生成建模的系统性解决方案。其核心动机在于：

- **构建统一参数化HOI数据基础**：通过将人体（SMPL-X参数模型）、物体（含6DoF姿态与关节状态）和文本描述统一至时空参数空间 $\mathbf{S}(t) = \{ \mathbf{S}_p(t), \mathbf{S}_e(t), T(t) \}$，为学习人类日常活动的生成式模型提供结构化训练数据。
- **突破异构系统的高精度校准**：设计身体空间对齐（Eq. 2）与手部校准（Eq. 3）方法，将IMU骨骼坐标系与多视角相机世界坐标系精确配准，使手部指尖触碰误差降至11毫米（86次触摸验证）。
- **解决交互遮挡下的鲁棒跟踪**：引入3D ArUco立方体标记替代传统表面标记，利用其多面可见性在遮挡条件下维持物体跟踪，使跟踪成功率从0.76–0.93提升至1.0（Table 1）。
- **验证数据对生成模型的价值**：通过在MDM框架上混合ParaHome与HumanML3D数据进行训练，证明该参数化数据能显著提升文本条件运动生成的质量（RPrecision top3从0.68提升至0.73），并支持物体引导的运动合成等新任务。

> **注意**：ParaHome系统依赖70台同步RGB相机和可穿戴IMU设备，设置成本较高；数据集覆盖38名参与者和22个物体，规模仍有限。这些限制在后续章节中有详细讨论。



## 核心方法与创新机理

ParaHome 的核心创新在于构建了一套异构感知系统与统一参数化框架，解决了现有 HOI 数据集在自然家庭环境中同时捕获高精度全身运动、精细手部运动和物体轨迹的根本瓶颈。其关键创新点体现在以下四个 changed slots 上：

### 1. 物体标记方案：从表面标记到 3D ArUco 立方体

现有方案（如 **Nan Jiang et al., ICCV 2023** 的虚拟表面标记跟踪）在物体表面附着 IR 标记，交互期间极易因手部遮挡导致跟踪丢失。ParaHome 改用 **3D ArUco 立方体标记**——每个立方体的多个面均印有 ArUco 图案，只要任意一面可见即可被检测和三角化。

**因果机制**：立方体的多面可见性大幅提升了遮挡下的标记检出率。Table 1 (Down) 的定量对比直接验证了这一优势：3D 立方体标记的跟踪成功率达到 **1.0**，而 4 个表面标记仅 **0.76**，即便将表面标记增至 40 个也仅提升至 0.93。这表明立方体方案在根本上解决了交互遮挡问题，而非仅靠增加标记数量来弥补。

### 2. 异构系统空间对齐：身体校准与手部校准

ParaHome 集成了 **70 台同步 RGB 相机**（覆盖 12.4 m² 场景）与 **IMU 可穿戴设备**（Xsens 动作捕捉套装 + Manus 手套），但两者的坐标系天然不统一。现有方案通常依赖出厂标定或简单刚体对齐，缺乏对骨架偏移和手部尺度的精确优化。

ParaHome 设计了两阶段的参数化校准：

- **身体校准**（Eq. 2）：优化骨架偏移量 $\mathcal{B}$ 和身体附着标记位置 $\mathcal{M}^b$，最小化 IMU 正向运动学输出与相机三角化结果之间的差异。Figure 4 的左右对比直观展示了校准前后骨架偏移的显著减小。
- **手部校准**（Eq. 3）：借助特制校准立方体，让参与者用指尖触碰立方体角点，联合优化指尖接触损失 $\mathcal{L}_{tip}$、手腕约束 $\mathcal{L}_{wrist}$ 和穿透惩罚 $\mathcal{L}_{pen}$，校准手部骨骼尺度和标记位置。

**定量证据**：86 次指尖触碰测试中，手部校准后的平均位置误差（APE）仅 **11 mm**（Sec. 4.1），验证了校准协议的高精度。

### 3. 人体模型拟合：从骨骼到 SMPL-X 的参数化

不同于直接使用动作捕捉骨骼，ParaHome 通过**自编码器 latent 优化**将 IMU 姿态映射到 SMPL-X 表面模型（Sec. 3.5）。这一步骤不仅提供了标准化的皮肤网格，还使得接触区域（如手-物接触面）可通过 SDF 距离场进行量化（Figure 5），为下游生成模型提供了结构化的 affordance 信息。

### 4. 训练数据混合：打破 HumanML3D 的领域局限

在文本条件运动生成任务中，现有模型（如 **MDM** (Tevet et al., arXiv 2022)）仅使用 HumanML3D 训练，缺乏精细手部运动和 HOI 上下文。ParaHome 将自身数据与 HumanML3D 混合训练 MDM，在 RPrecision top3 上达到 **0.73**，显著优于仅用 HumanML3D 的 **0.68**，并超越 **TEMOS** (Petrovich et al., ECCV 2022) 的 0.38 和 **T2M** (Guo et al., CVPR 2022) 的相应指标（Table 2）。

**因果分析**：ParaHome 数据补充了 HumanML3D 缺失的 HOI 交互模式和手部细节，使模型学会了更丰富的人-物空间关系。Table 3 进一步表明，在物体引导运动合成中加入初始相对空间线索 $\mathbf{S}_{p\to o}(t)$ 可将全局关节位置误差降低约 **30%**，验证了统一参数化框架对生成式建模的结构性支撑作用。



ParaHome 的总体目标是将家庭场景中的人-物交互（HOI）统一参数化，为三维生成式建模提供结构化数据。系统围绕一个核心状态表示构建，将时刻 $t$ 的场景信息组织为：

$$\mathbf{S}(t) = \{ \mathbf{S}_p(t), \mathbf{S}_e(t), T(t) \}$$

其中 $\mathbf{S}_p(t)$ 是人体状态（身体、左手、右手参数），$\mathbf{S}_e(t)$ 是环境状态（物体位姿与关节状态），$T(t)$ 是文本描述。这一参数化将人体（SMPL-X）和物体统一到同一时空坐标系，辅以自然语言标注，为学习日常活动的生成式模型提供了结构化基础。

系统的硬件与数据流架构如 Figure 2 所示，覆盖约 12.4 m² 的家庭场景。整个 pipeline 由以下核心模块串联而成：

![[assets/figures/papers/paper_list_l1742_ParaHome_Parameterizing_Everyday_Home_Activities_Towards_3D_Generative_M/figures/002_Figure_2.jpg]]
*Figure 2: (Center) Reconstructed scene of ParaHome from top view. Pictures adjacent to the rendering were taken from the center of the room, headed towards the corresponding black dots in the scene. (Right) Pictures of a RGB camera, IMU based motion capture devices with attached body markers and the 3D marker solution on an articulated object*

**1. 多视角视觉感知层（输入）**
70 台同步 RGB 相机环绕场景，从不同视角捕获图像，用于检测附着在人体和物体上的 ArUco 标记的 2D 角点，并通过三角化重建其 3D 位置。这一层负责提供物体与人体在相机世界坐标系中的全局刚性变换线索。

**2. 可穿戴动作捕捉层（并行输入）**
Xsens 惯性动作捕捉套装与 Manus 数据手套独立记录身体关节角度和手指运动，不受视觉遮挡影响。身体和手套上同样附着视觉标记，用于后续空间对齐。

**3. 物体运动解算模块**
对每个物体，通过预校准的标记-物体变换关系 $\mathbf{T}_{mar\_obj}$ 和当前标记姿态 $\mathbf{T}_{mar}(t)$，使用 Kabsch 算法计算物体 6DoF 姿态：

$$\mathbf{T}_{obj}(t) = \mathbf{T}_{mar\_obj} \mathbf{T}_{mar}(t)$$

对于铰接物体（如抽屉、冰箱），系统还根据标记间的相对变换解算关节状态参数。

**4. 身体空间对齐模块**
将 IMU 动作捕捉的骨骼坐标系对齐到相机世界坐标系。通过优化附着在身体上的标记位置 $\mathcal{M}^b$ 和骨骼偏移 $\mathcal{B}$，最小化前向运动学输出与视觉三角化结果之间的差异：

$$\operatorname*{min}_{\mathcal{M}^b,\mathcal{B}} \sum_{t=1}^{T} \lambda_b \mathcal{L}_{body}^t + \lambda_f \mathcal{L}_{foot}^t$$

Figure 4 的校准前后对比直观展示了该模块对骨架偏移的显著修正效果。

**5. 手部校准模块**
借助特制的校准立方体，优化手部骨骼尺度、偏移和标记位置 $\mathcal{M}^h, \mathcal{H}$，使指尖精确触碰立方体角点：

$$\operatorname*{min}_{\mathcal{M}^h,\mathcal{H}} \lambda_t \mathcal{L}_{tip} + \lambda_w \mathcal{L}_{wrist} + \lambda_p \mathcal{L}_{pen}$$

该模块使指尖平均位置误差达到 11 mm（86 次触摸），确保了精细手部交互的高精度。

**6. 后处理增强模块**
对因遮挡丢失的物体跟踪，利用手部运动线索和身体运动进行补全，其效果显著优于线性插值（lerp/slerp）。同时对手部数据进行加权插值以减少抖动。

**7. SMPL-X 拟合模块**
将 IMU 姿态映射到 SMPL-X 参数化人体模型，优化形状参数，并利用自编码器姿态先验确保拟合的合理性。

**8. 合成 RGB 图像生成（可选输出）**
利用 ControlNet，以渲染的深度图、2D 关键点和文本标注为条件，生成逼真的 RGB 图像，为下游视觉任务提供数据增强。

整个 pipeline 的关键设计决策在于：**3D ArUco 立方体标记**替代传统表面标记，在交互遮挡下实现了 1.0 的跟踪成功率（表面标记仅 0.76–0.93）；**异构系统校准**（身体+手部）确保了多尺度运动在统一坐标系下的高精度一致性。这两个设计共同构成了系统能够鲁棒捕获复杂家庭 HOI 数据的因果核心。

### 补充图表

![[assets/figures/papers/paper_list_l1742_ParaHome_Parameterizing_Everyday_Home_Activities_Towards_3D_Generative_M/figures/001_Figure_1.jpg]]
*Figure 1: Our system captures the detailed 3D movements of the human body, hands, and diverse objects, along with text descriptions*



ParaHome 系统的核心在于将异构传感器数据统一到一致的时空坐标系中，并参数化表达人、物、环境的交互状态。其技术路线围绕三个关键环节展开：**HOI 状态参数化**、**物体运动解算**、以及**多传感器空间对齐**。

### HOI 状态参数化

系统将时刻 $t$ 的交互场景抽象为一个统一的参数化表示：

$$\mathbf{S}(t) = \{ \mathbf{S}_p(t), \mathbf{S}_e(t), T(t) \}$$

其中 $\mathbf{S}_p(t)$ 为人体状态，$\mathbf{S}_e(t)$ 为环境（物体）状态，$T(t)$ 为文本描述。人体状态进一步分解为身体与双手参数：

$$\mathbf{S}_p(t) = \{ \mathbf{S}_b(t), \mathbf{S}_{lh}(t), \mathbf{S}_{rh}(t) \}$$

这一参数化将人体（最终拟合为 SMPL-X 模型）和物体（含关节状态）置于统一的时空空间，为后续生成式建模提供了结构化的数据基础。

### 物体运动解算

物体的 6DoF 姿态通过附着其上的 3D ArUco 立方体标记进行跟踪。多视角相机阵列检测标记的 2D 角点并三角化得到 3D 点，进而利用 Kabsch 算法解算标记的刚体变换 $\mathbf{T}_{mar}(t)$。物体的世界位姿由预标定的标记-物体变换与当前标记姿态共同决定：

$$\mathbf{T}_{obj}(t) = \mathbf{T}_{mar\_obj} \mathbf{T}_{mar}(t)$$

对于铰接物体，其关节状态由一组旋转或滑动关节参数描述，每个关节 $i$ 定义为 $\tau_i^j = \{ a_{e,i}^j, p_{e,i}^j, s_{e,i}^j(t) \}$，分别对应关节轴、枢轴点和随时间变化的状态值。

### 多传感器空间对齐

系统同时依赖多视角相机（覆盖全局空间）和 IMU 可穿戴设备（无遮挡地记录身体关节角度与手指运动），两者初始处于不同坐标系。空间对齐通过两个优化模块实现：

**身体校准**（Figure 4 左）优化 IMU 骨骼配置 $\mathcal{B}$ 和身体附着标记位置 $\mathcal{M}^b$，使正向运动学输出与相机三角化结果对齐：

$$\operatorname*{min}_{\mathcal{M}^b,\mathcal{B}} \sum_{t=1}^{T} \lambda_b \mathcal{L}_{body}^t + \lambda_f \mathcal{L}_{foot}^t$$

其中 $\mathcal{L}_{body}^t$ 约束身体标记位置一致性，$\mathcal{L}_{foot}^t$ 利用足部接触地面约束消除滑步。

**手部校准**（Figure 4 右）借助带有 ArUco 标记的校准立方体，优化手部骨骼尺度与标记位置 $\mathcal{M}^h, \mathcal{H}$，使指尖精确触碰立方体角点：

$$\operatorname*{min}_{\mathcal{M}^h,\mathcal{H}} \lambda_t \mathcal{L}_{tip} + \lambda_w \mathcal{L}_{wrist} + \lambda_p \mathcal{L}_{pen}$$

其中 $\mathcal{L}_{tip}$ 惩罚指尖与立方体角点距离，$\mathcal{L}_{wrist}$ 约束手腕位置一致性，$\mathcal{L}_{pen}$ 防止手指穿透立方体表面。经 86 次指尖触碰验证，校准后平均位置误差仅为 **11 mm**（Sec. 4.1），证明了该方案的高精度。

### 后处理增强

为应对交互遮挡导致的跟踪丢失，系统采用基于身体运动线索的插值补全策略（Figure 7c,d），相较于朴素线性插值（lerp/slerp）显著降低了物体平移和旋转的恢复误差。手部运动则通过加权插值减少抖动，恢复后的手部关节误差约 9 mm（Sec. 4.2）。最终，IMU 姿态通过自编码器 latent 优化拟合到 SMPL-X 表面模型，完成人体参数化（Figure 5）。

![[assets/figures/papers/paper_list_l1742_ParaHome_Parameterizing_Everyday_Home_Activities_Towards_3D_Generative_M/figures/005_Figure_5.jpg]]
*Figure 5: An example of SMPL-X shape parameter fitting. (Left) Projected keypoints, mask and rendered SMPL-X with the optimized shape parameter. (Right) Rendered SDF within 5cm to visualize an affordance information using optimized SMPL-X*

### 补充图表

![[assets/figures/papers/paper_list_l1742_ParaHome_Parameterizing_Everyday_Home_Activities_Towards_3D_Generative_M/figures/003_Figure_3.jpg]]
*Figure 3: (Left) Scanned 3D models in ParaHome system. (Right) Articulation state of 3D models. Blue bars show the object-specific parameters*

![[assets/figures/papers/paper_list_l1742_ParaHome_Parameterizing_Everyday_Home_Activities_Towards_3D_Generative_M/figures/004_Figure_4.jpg]]
*Figure 4: (Left) Before/After Body Calibration, Orange: forward kinematic output, Blue: RGB Triangulated Result (Right) Hand Calibration Protocol and Before/After Calibration Protocol*



## 实验与关键发现

### 系统评估：跟踪鲁棒性与校准精度

系统层面的评估围绕两个核心指标展开：**重投影误差**和**跟踪成功率**。Table 1（上）报告了场景内及交互期间的平均重投影误差，整体仅为 **1.021 像素**，操作过程中为 **1.016 像素**，表明多视角三角化重建具有亚像素级精度。这一基础精度为后续物体跟踪和人体对齐提供了可靠的三维参考。

![[assets/figures/papers/paper_list_l1742_ParaHome_Parameterizing_Everyday_Home_Activities_Towards_3D_Generative_M/figures/008_Table_1.jpg]]
*Table 1: Evaluation on system settings (Up) Average Reprojection error detected in the scene and during manipulation by humans. (Down) Average number of tracked object ratio on multiple sampled windows. Numbers in the upper row represent number of virtual passive markers attached to the surface of the target object*

Table 1（下）对比了不同物体标记方案在采样窗口内的平均跟踪成功率。**3D ArUco立方体标记**在交互期间达到了 **1.0** 的跟踪成功率，而表面附着4个虚拟被动标记的方案仅为 **0.76**，即使将表面标记数量增至40个，成功率也仅提升至 **0.93**。这一结果直接验证了核心设计选择：3D立方体标记通过多面可见性有效解决了交互遮挡问题，其优势在于无论物体如何旋转，至少有一个面保持可见。

手部校准的定量评估显示，在86次指尖触摸校准立方体的测试中，**平均位置误差（APE）仅为 11 mm**。考虑到手部动作的精细尺度和IMU手套固有的漂移特性，这一精度得益于公式（3）中指尖损失、腕部约束和穿透惩罚的联合优化。Figure 4 的左右对比直观展示了校准前后的差异：身体校准前，IMU前向运动学输出（橙色）与RGB三角化结果（蓝色）存在明显的骨架偏移；校准后两者高度重合，验证了公式（2）中身体对齐优化的有效性。

### 消融实验：相机数量与后处理增强

Figure 7a 展示了相机数量对标记检测率的影响。以70台相机的检测率为参考，检测率随相机数量增加几乎**线性提升**，未出现明显的饱和趋势。这表明多视角冗余对于克服遮挡至关重要，但也暗示了系统的高硬件成本——这是其可扩展性的主要瓶颈之一。

后处理增强的效果在 Figure 7c 和 7d 中进行了量化。物体跟踪因遮挡丢失后，使用基于身体运动线索的补全方法（proposed hole-filling）与简单的线性插值（lerp/slerp）进行了对比。结果表明，所提补全方法在平移和旋转（以6D表示）上的误差均显著低于插值基线。手部跟踪增强的量化结果为：恢复后的手部关节位置与原始位置的误差仅为 **9 mm**，证明后处理算法在短期跟踪丢失时能有效恢复合理的运动轨迹。

### 文本条件运动生成：数据混合的影响

Table 2 报告了文本条件运动生成任务在不同训练数据和模型上的评估结果。核心发现是：**将ParaHome数据与HumanML3D混合训练，在所有指标上均优于仅使用HumanML3D训练**。

![[assets/figures/papers/paper_list_l1742_ParaHome_Parameterizing_Everyday_Home_Activities_Towards_3D_Generative_M/figures/012_Table_2.jpg]]
*Table 2: Evaluation on different set of data and models*

以MDM（Tevet et al., arXiv 2022）为骨干网络，混合训练将Multimodal距离从 **4.32 降至 3.75**，RPrecision top3 从 **0.68 提升至 0.73**，FID从 **1.09 降至 0.53**。与TEMOS（Petrovich et al., ECCV 2022）和T2M（Guo et al., CVPR 2022）的对比中，混合训练的MDM在RPrecision top3上达到 **0.73**，远超TEMOS的 **0.38** 和T2M的 **0.68**。这一提升的因果机制在于：ParaHome提供了HumanML3D所缺乏的**精细手部运动**和**人-物交互上下文**，使生成模型能够学习更丰富的运动先验。Figure 8 的定性示例展示了模型生成“走向水壶、左手提起、向右手杯子倒水”和“打开柜门”等复杂交互序列的能力。

![[assets/figures/papers/paper_list_l1742_ParaHome_Parameterizing_Everyday_Home_Activities_Towards_3D_Generative_M/figures/009_Figure_8.jpg]]
*Figure 8: A sampled example of (Up) ‘A person walks shortly then lift kettle with left hand and pours toward cup holding right’ (Down) ‘A person opens the cabinet’*

### 物体引导运动合成：空间线索的关键作用

Table 3 报告了物体引导运动合成任务的定量结果。该任务给定物体运动轨迹，生成相应的人体运动序列。消融实验的核心发现是：**加入初始相对空间线索（S_p_tp）可将全局关节位置误差降低约30%**。

![[assets/figures/papers/paper_list_l1742_ParaHome_Parameterizing_Everyday_Home_Activities_Towards_3D_Generative_M/figures/011_Table_3.jpg]]
*Table 3: Quantitative results of object guided motion synthesis task*

以冰箱（Refrigerator）场景为例，加入S_p_tp后，全局关节平均位置误差（MPE glb-joints）从 **9.26 cm 降至 6.57 cm**；抽屉（Drawer）场景中，误差从 **9.92 cm 降至 5.88 cm**。这一结果表明，仅依赖物体运动轨迹不足以唯一确定人体运动——初始的人-物相对姿态提供了关键的歧义消除信息。Figure 9（右）展示了从物体轨迹生成人体运动的定性结果，生成的运动在时序上与物体运动协调一致。Figure 9（左）进一步展示了潜在空间插值的能力，表明扩散模型学习到的运动表示具有良好的连续性和语义可解释性。

![[assets/figures/papers/paper_list_l1742_ParaHome_Parameterizing_Everyday_Home_Activities_Towards_3D_Generative_M/figures/010_Figure_9.jpg]]
*Figure 9: (Left) A sampled example of latent interpolation result. Right most is a sequence generated from the interpolated noise. (Right) Generated body motion(lower) given object motion trajectory from 0 to T(upper)*

### 失败模式与局限性

尽管系统在跟踪和生成任务上表现优异，但仍存在若干明确的失败模式：

1. **物理标记依赖**：系统要求物体附着3D立方体标记、人体穿戴IMU设备并附着身体标记，这限制了用户舒适度和场景扩展性。无标记方案（如纯视觉方法）在复杂交互遮挡下的鲁棒性仍远不及本系统。
2. **高硬件成本**：70台同步RGB相机的部署成本高、灵活性差，难以迁移到不同房间布局。
3. **数据集规模有限**：38名参与者、22个物体的规模可能不足以训练通用HOI生成模型，尤其对于长尾交互类型。
4. **生成精细度不足**：扩散模型生成的手部动作精细度是否足以满足高精度接触任务（如拧瓶盖）仍需验证，当前实验仅针对相对简单的物体（冰箱、抽屉）。
5. **合成RGB真实性**：Figure 6 展示的合成RGB图像虽可用于下游任务，但其真实性有限，可能影响基于视觉的评估指标。
6. **校准自动化程度低**：身体和手部校准需要专门的捕获阶段和人工辅助（如校准立方体的精确放置），难以实现完全自动化。

![[assets/figures/papers/paper_list_l1742_ParaHome_Parameterizing_Everyday_Home_Activities_Towards_3D_Generative_M/figures/006_Figure_6.jpg]]
*Figure 6: (Left) Examples of synthesized RGB images using Para-Home data. (upper) Rendered depth images of ParaHome data. (lower) Synthesized RGB image using text annotation, depth, 2D keypoints. (Right) HOI Reconstruction using synthesized RGB*



## 定位与知识库关联

### 1. 核心方法定位：异构系统校准与参数化HOI数据生成

ParaHome 的核心贡献不在于提出全新的生成模型架构，而在于构建了一套异构感知系统的精确空间校准方案，并以此生成了首个在自然家庭环境中同时参数化人体全身运动、精细手部运动和关节物体运动的大规模数据集。该工作填补了现有HOI数据集的关键空白：**GrabNet**、**GRAB** 等数据集聚焦于手-物交互但缺乏全身运动上下文；**HumanML3D**、**KIT-ML** 等文本-运动数据集虽包含全身运动但缺少物体状态和精细手部信息；**BEHAVE**、**InterCap** 等场景级HOI数据集则受限于无标记姿态估计的精度瓶颈，难以捕获手指级别的接触细节。ParaHome 通过引入3D ArUco立方体标记和身体/手部空间校准优化，将多视角相机系统与IMU可穿戴设备统一到同一世界坐标系，实现了对复杂交互场景中人体与物体的鲁棒、精确跟踪。

### 2. 与基线工作的关系与改进

#### 2.1 物体跟踪方案对比

在物体跟踪层面，ParaHome 直接对比了基于表面虚拟标记的方案（**Nan Jiang et al., ICCV 2023**）。Table 1 (Down) 的消融实验表明，3D立方体标记的跟踪成功率（Tracking Success Ratio）达到 **1.0**，显著优于4个表面标记的0.76，甚至优于40个表面标记的0.93。这一改进的因果机制在于：3D立方体标记在任意视角下至少能提供可见的角点特征，而表面标记在物体旋转或遮挡时容易完全消失。Figure 7a 进一步验证了相机数量对标记检测率的线性提升效应，表明70台相机的冗余设计是鲁棒跟踪的系统保障。

#### 2.2 空间校准方案对比

身体校准（Eq. 2）和手部校准（Eq. 3）是 ParaHome 区别于以往工作的核心技术创新。传统IMU动作捕捉系统（如Xsens套装）输出的是相对于自身骨骼根节点的运动，与相机世界坐标系存在未知偏移；Manus手套的出厂设定也无法保证指尖位置与世界坐标的精确对齐。ParaHome 通过优化身体附着标记位置和骨架偏移量（Figure 4 前后对比直观展示了校准效果），以及利用校准立方体优化手部骨骼尺度和标记位置，实现了手部校准后平均位置误差仅 **11 mm**（86次触摸测试，Sec. 4.1）。这一精度水平使得手指与物体的接触状态可以被可靠地参数化，为下游生成式建模提供了关键的接触约束信息。

#### 2.3 生成模型训练数据混合的消融

在文本条件运动生成任务上，ParaHome 以**MDM**（Tevet et al., arXiv 2022）作为基础扩散模型架构，进行了训练数据混合的消融实验。Table 2 的结果表明，混合 ParaHome + HumanML3D 训练相较于仅用 HumanML3D 训练，在所有指标上均有提升：Multimodal dist 从4.32降至**3.75**，RPrecision top3 从0.68提升至**0.73**，并超越了同期专门设计的文本-运动生成模型 **TEMOS**（Petrovich et al., ECCV 2022）和 **T2M**（Guo et al., CVPR 2022）在相同指标上的表现。这一提升的因果解释在于：ParaHome 数据提供了 HumanML3D 所缺乏的精细手部运动和物体交互上下文，使扩散模型能够学习到更丰富的文本-运动对应关系。

#### 2.4 物体引导运动合成中的空间线索

在物体引导运动合成任务中，ParaHome 引入了初始人-物相对空间线索 $S_{p \to o}(t)$。Table 3 的消融实验表明，加入该线索可将全局关节位置误差（MPE glb-joints）降低约30%：以冰箱（Refrigerator）场景为例，误差从9.26 cm降至**6.57 cm**；抽屉（Drawer）场景从9.92 cm降至**5.88 cm**。这表明，在仅给定物体运动轨迹的条件下，初始相对姿态为生成合理的人体运动提供了关键的锚定信息。

### 3. 适用边界与局限

尽管 ParaHome 在系统精度和生成建模上取得了显著进展，其适用边界受以下因素制约：

1. **物理标记依赖**：系统依赖3D ArUco标记和可穿戴IMU设备，限制了用户舒适度和场景扩展性。身体和手部校准需要专门的捕获阶段和人工辅助，难以完全自动化。

2. **场景与物体多样性有限**：数据集在单一室内环境中采集，包含22个扫描物体和38名参与者。参与者性别、年龄、文化背景的多样性不足，可能导致下游模型产生偏差。

3. **相机系统成本与灵活性**：70台同步RGB相机的设置成本高、灵活性差，难以迁移到不同房间布局或更广泛的现实环境。Figure 7a 虽显示相机数量增加带来线性收益，但未出现饱和点，暗示系统对相机冗余的高度依赖。

4. **生成任务的复杂度限制**：生成实验仅针对简单物体和动作（如打开橱柜、倒水），未涉及多物体协作或长时序复杂任务。扩散模型生成的手部动作精细度是否足以满足高精度接触任务（如精细装配）尚待验证。

5. **合成RGB图像的真实性**：利用ControlNet从深度、2D关键点和文本注释生成的RGB图像（Figure 6）在真实感上仍有局限，可能影响基于合成数据训练的下游HOI估计模型的泛化能力。

### 4. 开放问题与未来方向

1. **无标记化**：如何去除物理标记，实现无标记的鲁棒HOI捕捉，是该系统走向大规模应用的关键瓶颈。可能的路径包括融合神经辐射场（NeRF）或3D高斯泼溅（3DGS）进行场景级姿态估计，但当前技术在手指级别的精度上仍远不及标记方案。

2. **系统可迁移性**：当前系统能否迁移到不同房间布局和更多样化的物体上？这需要解决相机标定自动化、物体3D模型快速获取以及关节参数自动推断等问题。

3. **长时遮挡鲁棒性**：身体校准在长时间遮挡或无标记可见时的鲁棒性如何？当前的后处理增强（Sec. 3.5）虽优于线性插值（Figure 7c,d），但依赖于手部跟踪和IMU数据的可用性，在完全遮挡场景下可能失效。

4. **生成模型的接触精度**：扩散模型生成的手部动作能否满足高精度接触任务？可能需要引入物理仿真约束或接触力反馈作为额外的监督信号。

5. **数据集多样性与公平性**：当前数据集在性别、年龄、文化背景上的多样性不足，是否会导致模型在特定人群上表现退化？这需要在数据集扩展时进行系统性的偏差评估。

6. **系统效率与成本优化**：如何将当前系统扩展为更高效、更低成本的方案？可能的路径包括减少相机数量并用神经渲染补全视角，或用单目/双目SLAM替代部分多视角重建功能。



## 原文 PDF

![[paperPDFs/CVPR_2025/ParaHome_Parameterizing_Everyday_Home_Activities_Towards_3D_Generative_Modeling_of_Human_Object_Interactions.pdf]]
