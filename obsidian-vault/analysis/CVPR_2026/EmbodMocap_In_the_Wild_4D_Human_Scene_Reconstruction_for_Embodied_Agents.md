---
title: "EmbodMocap: In-the-Wild 4D Human-Scene Reconstruction for Embodied Agents"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EmbodMocap_In_the_Wild_4D_Human_Scene_Reconstruction_for_Embodied_Agents.pdf
project_link: null
code_link: "https://www.spectacularai.com"
aliases:
- EmbodMocap
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 利用两台移动iPhone的双RGB-D序列的联合标定与优化，在同一度量世界坐标系中同时重建人体与场景。
primary_logic: 通过双视角点追踪损失解决单目深度歧义，并结合场景重建与COLMAP配准实现相机轨迹与世界坐标系对齐，从而在无需静态相机或标记的情况下获得场景一致的人体运动重建。
claims:
- 双视图设置通过像素级稠密对应有效消除深度歧义，显著提升标定精度。
- 在光学动捕基准上，双视图重建的WA-MPJPE（56.61 mm）远优于单目模型GVHMR（66.56 mm）和单视角优化，且随序列长度增加优势更明显。
- 消融实验表明，去掉点追踪损失L_track导致IoU从73.0降至54.3，Reproj误差从9.3升至44.2；去掉3D关键点损失L_kp3d使IoU降至59.3，Reproj升至20.4。
- Optical Mocap Studio (Vicon GT) 上 WA-MPJPE (mm) = 56.61 (Dual View)
---

# EmbodMocap: In-the-Wild 4D Human-Scene Reconstruction for Embodied Agents

> [!tip] 核心洞察
> 通过双视角点追踪损失解决单目深度歧义，并结合场景重建与COLMAP配准实现相机轨迹与世界坐标系对齐，从而在无需静态相机或标记的情况下获得场景一致的人体运动重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | EmbodMocap：面向具身智能体的野外4D人体-场景重建 |
| 英文题名 | EmbodMocap: In-the-Wild 4D Human-Scene Reconstruction for Embodied Agents |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.23205) · [Code](https://www.spectacularai.com) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | EmbodMocap |
| Dataset | Optical Mocap Studio, EMDB, Physics-based Character Animation |

> [!tip] 效果简介
> - Optical Mocap Studio (Vicon GT) 上，WA-MPJPE (mm) 56.61 (Dual View) vs 66.56 (GVHMR) (↓9.95)。
> - EMDB (Subset 2) 上，WA-MPJPE (mm) 82.21 (微调π³与VIMO) vs 83.56 (原始π³与VIMO) (↓1.35)。
> - Physics-based Character Animation (Support Skill) 上，Success Rate (%) 66.0 (Ours Full) vs 20.6 (Monocular Baseline) (↑45.4)。

## 概述

**问题瓶颈**：现有高质量人体-场景数据采集依赖昂贵设备（多相机、动作捕捉服、LiDAR）且局限于工作室环境，难以规模化收集野外自然场景下带场景上下文的人体运动数据。这一瓶颈直接阻碍了具身AI学习自然界人类行为的能力。

**核心思路**：EmbodMocap提出利用两台移动iPhone的双RGB-D序列的联合标定与优化，在同一度量世界坐标系中同时重建人体与场景。其关键洞察在于：双视角点追踪损失可有效解决单目深度歧义，结合场景重建与COLMAP配准实现相机轨迹与世界坐标系对齐，从而在无需静态相机或标记的情况下获得场景一致的人体运动重建。

**方法定位**：EmbodMocap并非单一人体姿态估计模型，而是一套完整的四阶段采集与处理系统——场景重建（Stage I）→ 序列处理（Stage II）→ 序列标定（Stage III）→ 运动优化（Stage IV）。其核心创新集中在标定阶段的多约束联合优化（点追踪损失 + Chamfer距离 + 捆绑调整）和运动优化阶段的世界空间SMPLify（引入3D关键点损失）。相对于单目基线（如GVHMR、单视角优化），该方法将“视角数量”从单iPhone扩展为双iPhone，将“深度歧义解决”从依赖COLMAP估计升级为像素级稠密对应约束。

**主要结果**：
- 在光学动捕基准上，双视图重建的WA-MPJPE达到56.61 mm，显著优于单目模型GVHMR（66.56 mm）和单视角优化。
- 消融实验表明，去除点追踪损失导致IoU从73.0骤降至54.3，重投影误差从9.3升至44.2，证实双视图对应是整体性能的关键。
- 在下游具身任务中，EmbodMocap采集的数据使物理角色动画的支撑（Support）技能成功率从单目基线的20.6%提升至66.0%。

**硬件成本**：两台iPhone总成本约$1000，远低于传统动捕系统（>$20K），极大降低了野外数据采集门槛。

## 背景与动机

### 问题背景：具身AI对野外人体-场景交互数据的需求

具身智能体（embodied agents）——无论是虚拟角色还是物理机器人——要在真实世界中自然地行动，必须理解人类如何在复杂场景中运动与交互。这要求训练数据不仅包含人体运动本身，还必须包含与之对应的三维场景几何，且二者需在同一度量坐标系下对齐。然而，构建此类“4D人体-场景”数据集面临根本性困难：现有高质量采集方案依赖昂贵且受限的硬件，难以走出实验室进入野外环境。

**Table 1** 系统对比了现有4D人体-场景数据集的特征差异。传统方案可大致分为两类：一类基于光学动作捕捉（如Vicon）与多相机系统，能提供毫米级精度的真值，但将采集限制在固定工作室内；另一类采用IMU动捕服或手持扫描设备，虽具备一定便携性，却牺牲了场景重建能力或度量尺度精度。这种“精度-便携性-场景感知”的不可能三角，使得现有数据集在场景多样性、交互自然性和采集成本之间始终无法兼得。

### 核心瓶颈：野外场景下度量级人体-场景联合重建的缺失

问题的本质瓶颈在于：**缺乏一种低成本、可移动的采集系统，能在任意野外场景中同时获取度量准确的人体运动与场景几何，并将二者统一在同一世界坐标系下。** 具体而言，现有方案存在以下系统性缺口：

1. **单目方案面临深度歧义。** 从单目RGB视频恢复人体运动（如GVHMR等SOTA方法）虽不依赖特殊硬件，但缺乏绝对尺度信息，且人体在世界空间中的平移估计高度不确定。单目SLAM虽能重建场景，但其尺度漂移和坐标系不一致问题使得人体与场景难以精确对齐。

2. **多传感器方案成本高昂且不可移动。** 光学动捕系统（成本>$20K）和多相机阵列需要固定安装与标定，无法部署于日常起居、户外街道等自然场景。IMU动捕服虽可移动，但无法获取场景信息。

3. **消费级深度传感器潜力未被充分挖掘。** 现代智能手机（如iPhone）已集成RGB-D传感器与VIO里程计，能以极低成本（约$1000/两台）提供带有度量尺度的相机位姿。然而，如何将两个独立移动的RGB-D序列联合标定，消除单视角深度歧义，并将人体运动统一到场景世界坐标系中，仍是一个开放问题。

### 本文动机与核心思路

EmbodMocap的动机正是打破上述瓶颈。其核心洞察是：**利用两台移动iPhone的双RGB-D序列的联合标定与优化，可以在同一度量世界坐标系中同时重建人体与场景。** 这一思路的关键在于：

- **双视图像素级稠密对应消除深度歧义。** 与单目方案不同，双视图设置通过点追踪损失（$ \mathcal{L}_{\mathrm{track}} $）约束两视角间3D反向投影点的一致性，从根本上解决了单目深度估计的不确定性。消融实验证实，移除该损失导致标定IoU从73.0骤降至54.3，重投影误差从9.3升至44.2（Table 2）。

- **场景重建提供世界坐标系锚定。** 先用单iPhone扫描静态场景，通过SpectacularAI SDK获取度量级相机参数并融合TSDF网格，为后续人体运动提供Z-up世界坐标系的绝对参照。

- **多约束联合优化实现序列-场景对齐。** 通过COLMAP注册获取初始刚性变换，再联合优化点追踪损失、Chamfer距离与捆绑调整损失，将双视角相机轨迹统一到场景坐标系中（Eq. 3）。

- **世界空间运动优化提升一致性。** 基于三角化的3D关键点与世界空间SMPLify（Eq. 9），在场景坐标系下直接优化SMPL参数，获得时间一致、场景对齐的人体运动。

这一设计使得EmbodMocap能够在任意场景中（室内/室外）以约$1000的设备成本完成采集，在光学动捕基准上达到WA-MPJPE 56.61 mm（优于单目基线GVHMR的66.56 mm，Table 3），并成功支撑单目人体-场景重建、物理角色动画和真实人形机器人运动控制等下游具身任务。

## 核心创新

EmbodMocap 的核心创新在于**通过两台移动 iPhone 的双 RGB-D 序列联合标定与优化，在同一度量世界坐标系中同时重建人体与场景**，从而突破了现有方法对昂贵动捕设备与工作室环境的依赖。其关键创新点可归结为以下四个“changed slots”：

### 1. 从单目到双目的视角升级

现有野外人体运动捕捉方法通常依赖单一 iPhone（单目），其深度估计依赖 COLMAP 等 SfM 管线，在弱纹理或动态人体区域存在严重深度歧义。EmbodMocap 将视角数量从**单 iPhone（单目）**升级为**双 iPhone（双目）**（Abstract），从而引入了像素级稠密对应的可能性。这一变化是整个系统精度提升的物理基础——双视图几何约束使得原本病态的单目深度估计问题变为可约束的三角化问题。

### 2. 深度歧义解决：从 COLMAP 估计到点追踪损失约束

单目基线依赖 COLMAP 估计深度，但由于人体运动破坏了静态场景假设，COLMAP 在人体区域往往产生大误差。EmbodMocap 引入了**双视图像素级稠密对应（点追踪损失）**来解决这一瓶颈（Sec. 4.2）。具体而言，通过最小化双视图 3D 反向投影点之间的一致性损失 $\mathcal{L}_{\mathrm{track}}$（Eq. 5），系统强制两个视角的几何关系保持一致，从而有效消除深度歧义。

消融实验（Table 2）为这一创新提供了决定性证据：**去掉点追踪损失 $\mathcal{L}_{\mathrm{track}}$ 后，IoU 从 73.0 骤降至 54.3，Reproj 误差从 9.3 飙升至 44.2，深度误差从 0.078 恶化至 2.372**。这表明双视图对应是整体性能的支柱，而非锦上添花的组件。

### 3. 标定方法：从 COLMAP 初始对齐到多约束联合优化

传统方法通常仅依赖 COLMAP 与 SAI 相机轨迹之间的刚性配准来获得初始对齐。EmbodMocap 将此升级为**多约束联合优化**（Eq. 3），在初始偏移变换（Eq. 1）的基础上，联合优化三个互补的损失项：
- **点追踪损失** $\mathcal{L}_{\mathrm{track}}$：约束双视图间的像素级稠密对应；
- **Chamfer 距离**：约束相机轨迹与场景几何的一致性；
- **捆绑调整损失** $\mathcal{L}_{\mathrm{ba}}$：全局优化相机位姿与场景结构。

这种多约束融合策略使得标定对单一约束的失效具有鲁棒性——当点追踪损失被移除时，Chamfer 和捆绑调整无法单独弥补深度歧义（Table 2 中 IoU 从 73.0 降至 54.3 即为明证）。

### 4. 运动优化：从单目 SMPLify 到世界空间 SMPLify

单目基线采用标准 SMPLify，仅依赖 2D 重投影损失与人体先验进行优化，缺乏对世界坐标系下 3D 位置的直接约束。EmbodMocap 将其升级为**世界空间 SMPLify**（Eq. 9），在损失函数中显式加入了**3D 关键点损失 $\mathcal{L}_{\mathrm{3D}}$**——该损失基于双视图三角化得到的 3D 关键点（通过加权重投影误差最小化获得），直接约束 SMPL 模型在世界坐标系中的位置。

消融实验（Table 2）证实了这一创新的必要性：**去掉 3D 关键点损失 $\mathcal{L}_{\mathrm{kp3d}}$ 后，IoU 降至 59.3，Reproj 升至 20.4，深度误差升至 0.609**。这表明世界空间的 3D 约束对于消除深度歧义和保证重建精度至关重要，仅靠 2D 重投影无法实现同等效果。

### 创新链的因果逻辑

上述四个 changed slots 构成了一个因果链：**双视角硬件升级 → 点追踪损失解决深度歧义 → 多约束联合优化实现鲁棒标定 → 世界空间 3D 关键点约束提升运动精度**。这一链条的终端效果在光学动捕基准上得到量化验证：双视图重建的 WA-MPJPE 为 56.61 mm，显著优于单目模型 GVHMR 的 66.56 mm 和单视角优化的 66.96 mm（Table 3, chunk=100），且随序列长度增加优势更加明显。

## 整体框架

EmbodMocap 提出了一套低成本、便携的野外 4D 人体-场景重建系统，仅需两台移动 iPhone 即可在统一度量世界坐标系中同时获取静态场景网格与动态人体运动。其核心流水线由四个顺序阶段构成（Figure 2），各阶段逐步完成场景重建、序列预处理、多约束联合标定与世界空间运动优化，最终输出场景感知的人体运动数据。

![[assets/figures/papers/paper_list_l2637_https_arxiv_org_abs_2602_23205/figures/003_Figure_2.jpg]]
*Figure 2: EmbodMocap: We propose an affordable dataset capture and processing system. From left to right, the four stages (Stage-I to Stage-IV) illustrate our core logic: leveraging high-quality camera matrices provided by SpectacularAI [1] and aligning sequence coordinates to the scene’s world frame. For detailed explanations, please refer to Sec. 3*

**Stage I — 场景重建**：使用单台 iPhone 拍摄场景的 RGB-D 视频，通过 SpectacularAI SDK (SAI) 获取度量尺度、Z轴向上的相机参数 $(K_s, R_{s,n}, T_{s,n})$，再经 PromptDA 深度增强与 TSDF 融合生成静态场景网格。该网格作为后续所有坐标系的参考世界坐标系。

**Stage II — 序列处理**：两台同步 iPhone 录制双视角 RGB-D 视频，SAI 为每帧提供各自本地坐标系下的相机位姿 $(K_v, R_{v,t}, T_{v,t})$；同时，YOLO、ViTPose、SAM2 和 PromptDA 提取人体掩码、2D 关键点与增强深度，VIMO 提供初始 SMPL 参数。

**Stage III — 序列标定**：这是系统的核心创新环节。首先利用已知内参与仅保留背景的 SIFT 特征，将双视角序列注册到 Stage I 的 COLMAP 稀疏模型中，通过最小化 COLMAP 与 SAI 相机位置间的 L2 距离求解初始偏移变换（Eq. (1)）。随后，联合优化点追踪损失 $\mathcal{L}_{\mathrm{track}}$、Chamfer 距离与捆绑调整损失 $\mathcal{L}_{\mathrm{ba}}$（Eq. (3)），将双视角相机轨迹统一对齐到场景世界坐标系。其中，点追踪损失通过约束双视图间像素级稠密对应点的 3D 反向投影一致性（Eq. (5)），有效消除了单目深度歧义。

**Stage IV — 运动优化**：基于标定后的双视角相机参数，对 2D 关键点进行加权三角化得到 3D 关键点（Eq. (7)），随后在世界坐标系下执行 SMPLify 联合优化（Eq. (9)），同时约束 3D 关键点损失 $\mathcal{L}_{\mathrm{3D}}$、时序平滑损失、先验损失和重投影损失，获得时间一致的世界空间人体运动。

整个框架的输入为两台 iPhone 拍摄的 RGB-D 序列，输出为度量世界坐标系下的静态场景网格与 SMPL 人体运动序列。消融实验（Table 2）证实，点追踪损失与 3D 关键点损失是系统性能的关键支柱：去除 $\mathcal{L}_{\mathrm{track}}$ 导致 IoU 从 73.0 骤降至 54.3，重投影误差从 9.3 升至 44.2；去除 $\mathcal{L}_{\mathrm{kp3d}}$ 同样使 IoU 降至 59.3、深度误差升至 0.609。这验证了双视图稠密对应与世界空间 3D 约束对消除深度歧义和保证重建精度的核心作用。

## 核心模块与公式推导

EmbodMocap 的核心逻辑是通过四个顺序阶段，将人体运动与场景统一到同一个度量世界坐标系中。其关键在于**双视图联合标定**与**世界空间运动优化**两个模块的协同。

### 1. 初始刚性变换估计（Stage III 入口）

双视图序列的相机轨迹由 SpectacularAI SDK (SAI) 提供，但处于各自的局部坐标系中。为将其对齐到 Stage I 重建的场景世界坐标系，首先通过 COLMAP 注册获得初始对齐。

设 SAI 提供的相机位置为 $T_{v,t}$，COLMAP 注册得到的相机位置为 $\hat{T}_{v,t}$，通过最小化二者间的 L2 距离来求解初始偏移变换 $(s^{\mathrm{off}}, R^{\mathrm{off}}, T^{\mathrm{off}})$：

$$
\operatorname*{min}_{s^{\mathrm{off}}, R^{\mathrm{off}}, T^{\mathrm{off}}} \sum_{t=1}^{N} \left\| \hat{T}_{v,t} - (s^{\mathrm{off}} R^{\mathrm{off}} T_{v,t} + T^{\mathrm{off}}) \right\|_{2}^{2} \tag{1}
$$

其中 $s^{\mathrm{off}}$ 为尺度因子，$R^{\mathrm{off}}$ 为旋转矩阵，$T^{\mathrm{off}}$ 为平移向量。求解后，将 SAI 相机外参对齐到世界坐标系：

$$
\pmb{R}_{v,t}^{\mathrm{ali}} = \pmb{R}_{v}^{\mathrm{off}} \pmb{R}_{v,t}, \quad \pmb{T}_{v,t}^{\mathrm{ali}} = \pmb{R}_{v}^{\mathrm{off}} \pmb{T}_{v,t} + \pmb{T}_{v}^{\mathrm{off}} \tag{2}
$$

其中 $\pmb{R}_{v}^{\mathrm{off}}$ 仅保留绕 z 轴的全局旋转分量，以保持场景的“Z-up”约定。

### 2. 多约束联合标定（Stage III 核心）

COLMAP 的初始对齐精度有限，尤其在大尺度场景中误差显著。EmbodMocap 引入三种互补的几何约束进行联合优化，目标函数为：

$$
\mathcal{L}_{\mathrm{calib}} = \lambda_{\mathrm{track}} \mathcal{L}_{\mathrm{track}} + \sum_{v} \lambda_{\mathrm{ch}} d_{\mathrm{Chamfer}} + \sum_{v} \lambda_{\mathrm{ba}} \mathcal{L}_{\mathrm{ba},v} \tag{3}
$$

三项损失分别承担不同的校正角色：

**点追踪一致性损失 $\mathcal{L}_{\mathrm{track}}$**：这是双视图设置的核心优势。利用 SAM2 在双视图间建立像素级稠密对应，将 2D 对应点通过当前估计的相机参数反向投影到 3D，约束两个视图中对应 3D 点的一致性：

$$
\mathcal{L}_{\mathrm{track}} = \frac{1}{\sum_{v,t} |\mathcal{Q}_{v,t}|} \sum_{t} \sum_{i} \tilde{w}_{t}^{(i)} \big\| \boldsymbol{Q}_{1,t}^{(i)} - \boldsymbol{Q}_{2,t}^{(i)} \big\|_{2}^{2} \tag{5}
$$

其中 $\boldsymbol{Q}_{v,t}^{(i)}$ 为视图 $v$ 在时刻 $t$ 的第 $i$ 个反向投影 3D 点，$\tilde{w}_{t}^{(i)}$ 为基于对应置信度的权重。该损失直接解决单目深度歧义——消融实验表明，移除 $\mathcal{L}_{\mathrm{track}}$ 后 IoU 从 73.0 骤降至 54.3，深度误差从 0.078 飙升至 2.372（Table 2），证实双视图稠密对应是系统精度的支柱。

![[assets/figures/papers/paper_list_l2637_https_arxiv_org_abs_2602_23205/figures/004_Table_2.jpg]]
*Table 2: The performance of different optimization settings*

**Chamfer 距离 $d_{\mathrm{Chamfer}}$**：约束对齐后的相机点云与场景重建网格之间的一致性，确保相机轨迹与场景几何的全局吻合。

**捆绑调整损失 $\mathcal{L}_{\mathrm{ba},v}$**：在 COLMAP 稀疏重建框架内优化相机参数与 3D 点位置，保持多视图几何一致性。

### 3. 世界空间运动优化（Stage IV）

标定完成后，双视图相机参数已统一到场景世界坐标系。运动优化分为两步：

**3D 关键点三角化**：利用双视图 2D 关键点（由 ViTPose 提取）和已标定的相机参数，通过最小化加权重投影误差三角化得到世界坐标系下的 3D 关键点 $\pmb{Y}_{t,j}$：

$$
\underset{\pmb{Y}_{t,j}}{\operatorname*{min}} \sum_{v=1}^{V} c_{v,t,j} \big\| \pmb{y}_{v,t,j} - \pmb{P}_{v} \pmb{Y}_{t,j} \big\|_{2}^{2} \tag{6}
$$

其中 $\pmb{P}_v$ 为视图 $v$ 的投影矩阵，$c_{v,t,j}$ 为关键点置信度权重。

**世界空间 SMPLify**：以三角化的 3D 关键点为监督，联合优化 SMPL 形体参数 $\beta$、逐帧姿态参数 $\theta_t$ 和世界平移 $\Gamma_t$：

$$
\mathcal{L}_{\mathrm{SMPLify}} = \mathcal{L}_{\mathrm{3D}} + \mathcal{L}_{\mathrm{smooth}} + \mathcal{L}_{\mathrm{prior}} + \mathcal{L}_{\mathrm{reproj}} \tag{9}
$$

- $\mathcal{L}_{\mathrm{3D}}$：3D 关键点损失，约束 SMPL 关节与三角化关键点的一致性。消融实验显示，移除该损失使 IoU 降至 59.3，深度误差升至 0.609（Table 2），说明世界空间 3D 约束对消除深度歧义不可或缺。
- $\mathcal{L}_{\mathrm{smooth}}$：时序平滑损失，抑制帧间抖动。
- $\mathcal{L}_{\mathrm{prior}}$：SMPL 姿态与形体的先验正则项。
- $\mathcal{L}_{\mathrm{reproj}}$：重投影损失，约束 SMPL 关节投影与 2D 关键点的一致性。

与单目 SMPLify 仅依赖重投影和先验不同，世界空间 SMPLify 通过 $\mathcal{L}_{\mathrm{3D}}$ 引入了度量尺度的 3D 监督，这是双视图几何带来的直接增益。

## 实验与分析

### 4.1 标定与运动优化消融实验

EmbodMocap 的标定精度与运动质量高度依赖多约束联合优化框架。表 2 的消融实验揭示了各损失项对系统性能的因果贡献。

**完整模型**（包含点追踪损失 $\mathcal{L}_{\mathrm{track}}$、Chamfer 距离、重投影损失、平滑损失及 3D 关键点损失 $\mathcal{L}_{\mathrm{kp3d}}$）在四个指标上均取得最优：IoU 达 73.0，重投影误差仅 9.3，深度误差 0.078，抖动 0.0128。

**去除点追踪损失 $\mathcal{L}_{\mathrm{track}}$** 是性能崩塌的核心瓶颈：IoU 从 73.0 骤降至 54.3，重投影误差从 9.3 飙升至 44.2，深度误差从 0.078 恶化至 2.372。这直接验证了核心洞察——双视图像素级稠密对应是消除单目深度歧义的不可替代机制。缺乏该约束，双视图间的刚性变换无法被可靠估计，导致相机轨迹在深度方向上严重漂移。

**去除 3D 关键点损失 $\mathcal{L}_{\mathrm{kp3d}}$** 同样造成显著退化：IoU 降至 59.3，重投影误差升至 20.4，深度误差升至 0.609。这表明世界坐标系下的 3D 约束对消除深度歧义至关重要——仅依赖 2D 重投影无法充分约束人体在场景中的绝对位置。

**去除平滑损失** 主要影响时间一致性，抖动指标从 0.0128 升至 0.0218，但对空间精度影响相对较小。**去除 Chamfer 距离**和**仅使用重投影损失**的变体在 IoU 和深度误差上也有明显退化，说明场景几何约束与多视角一致性是互补的。

### 4.2 光学动捕基准对比

在配备 Vicon 光学动捕系统的工作室基准上，EmbodMocap 的双视图优化方案与单目基线进行了严格对比（表 3）。

**与单目模型 GVHMR 对比**：在序列块长度 chunk=100 的设置下，双视图方案的 WA-MPJPE 为 56.61 mm，显著优于 GVHMR 的 66.56 mm（↓9.95 mm）；W-MPJPE 差距更为悬殊，双视图 72.86 mm vs GVHMR 123.44 mm（↓50.58 mm）。值得注意的是，随着序列块长度增加（chunk=25→50→100），双视图优化的优势持续扩大，表明该方法在长序列上的时间一致性远优于纯单目方案。

**与单视角优化基线对比**：单视角优化（仅使用一台 iPhone 配合 COLMAP 校准与单目 SMPLify）在 chunk=100 时 WA-MPJPE 为 64.17 mm，W-MPJPE 为 108.17 mm。双视图方案分别提升 7.56 mm 和 35.31 mm，直接验证了“双视角点追踪损失解决深度歧义”这一可控因果旋钮的有效性。

图 3 的定性对比进一步佐证：单视图重建在深度方向出现明显偏移和穿透伪影，而双视图方案的人体网格与场景地面、物体的接触关系更为准确。

**公平性说明**：该基准实验仅包含一名受试者的 5 段基本动作，人体多样性有限，结论在更广泛人群上的泛化性需进一步验证。

### 4.3 单目人体-场景重建下游任务

EmbodMocap 采集的数据集被用于微调单目人体-场景重建模型 π³（SLAM）与 VIMO（度量尺度人体运动），并在 EMDB 基准的 Subset 2 上评估（表 4）。

在 EMDB 上，微调后的 π³ 与 VIMO 联合方案（Finetuned Both）的 WA-MPJPE 为 82.21 mm，相比原始权重（Untuned）的 83.56 mm 降低了 1.35 mm。单独微调 VIMO（Finetuned VIMO）的 WA-MPJPE 为 83.30 mm，单独微调 π³（Finetuned π³）为 84.56 mm。联合微调优于单独微调，表明场景重建精度与人体运动估计之间存在协同效应——更准确的场景几何有助于约束人体在度量空间中的位置。

图 4 展示了微调模型在 EMDB 上的定性重建结果，人体与场景的接触关系（如坐姿、倚靠）得到较好保持。

### 4.4 物理角色动画技能训练

将 EmbodMocap 数据集用于训练物理角色动画的多种交互技能（表 5），在支撑（Support）技能上，EmbodMocap 完整数据（Ours Full）的成功率达 66.0%，而单目基线（Monocular Baseline）仅为 20.6%（↑45.4）。这一巨大差距源于 EmbodMocap 提供的度量级场景几何与准确的人体-场景接触信息，使物理模拟器能够学习可靠的支撑策略。

在其他技能上（如行走、坐、躺、上下楼梯），EmbodMocap 数据的成功率也普遍优于单目基线，且接触误差（Contact Error）和平均姿态距离（APD）更低。图 5 的定性对比展示了各技能在物理模拟中的视觉差异：单目基线常出现浮空、穿透等物理不真实现象，而 EmbodMocap 训练的模型能保持稳定的接触与平衡。

### 4.5 场景感知运动跟踪

在四个不同 3D 场景上的场景感知运动跟踪评估（表 6）显示，EmbodMocap 数据训练的跟踪框架在长期运动序列上保持了物理真实感。图 6 的定性结果展示了室内外日常交互（行走、坐、躺、爬楼梯、触摸）的跟踪效果，右侧放大视图表明该方法能解决参考数据中存在的穿透和浮空伪影。

### 4.6 已知局限与失败模式

尽管 EmbodMocap 在多项任务上展现了显著优势，实验与系统设计揭示了以下局限：

1. **采集人力依赖**：系统需要两名拍摄者手动操作 iPhone 并使用激光笔进行帧级同步，采集效率受限于人力。当前尚未实现自动化采集流程。

2. **静态场景假设**：Stage I 的场景重建要求场景为静态，不支持包含动态物体（如移动家具、他人）的环境。这限制了在真正“在野”动态场景中的应用。

3. **深度传感器有效距离**：消费级 iPhone 的深度传感器有效距离有限（室内约 3.5 m，室外约 5 m），大规模开放环境（如广场、运动场）的重建质量将显著下降。

4. **数据集规模与多样性**：当前数据集包含 23 个场景、104 段序列，规模仍相对较小，可能不足以覆盖极端多样的交互类型与场景几何。在更大规模数据上的扩展性及对下游任务的性能瓶颈尚待验证。

5. **人体多样性有限**：光学动捕基准仅包含一名受试者，结论在更广泛人体形态上的泛化性需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l2637_https_arxiv_org_abs_2602_23205/figures/005_Figure_3.jpg]]
*Figure 3: Our dual view vs. single view results in optical studio*

![[assets/figures/papers/paper_list_l2637_https_arxiv_org_abs_2602_23205/figures/006_Table_3.jpg]]
*Table 3: Comparision among monocular model, single view optimization, with dual view optimization(ours)*

![[assets/figures/papers/paper_list_l2637_https_arxiv_org_abs_2602_23205/figures/007_Table_4.jpg]]
*Table 4: Comparison of Finetuned Models on EMDB Benchmarks*

![[assets/figures/papers/paper_list_l2637_https_arxiv_org_abs_2602_23205/figures/008_Figure_4.jpg]]
*Figure 4: Quality results of proposed 4D Human & Scene Reconstruction pipeline on EMDB dataset*

![[assets/figures/papers/paper_list_l2637_https_arxiv_org_abs_2602_23205/figures/009_Table_5.jpg]]
*Table 5: Comparison of data duration, Success Rate, Contact Error, and APD for different skills among 3 data settings*

![[assets/figures/papers/paper_list_l2637_https_arxiv_org_abs_2602_23205/figures/010_Figure_5.jpg]]
*Figure 5: Qualitative comparison of 4 basic skills and 2 additional skills*

![[assets/figures/papers/paper_list_l2637_https_arxiv_org_abs_2602_23205/figures/011_Table_6.jpg]]
*Table 6: Quantitative evaluation of scene-aware motion tracking and dataset statistics across four 3D scenes*

![[assets/figures/papers/paper_list_l2637_https_arxiv_org_abs_2602_23205/figures/012_Figure_6.jpg]]
*Figure 6: We present qualitative results of scene-aware motion tracking, showing four long-term motion examples in different scenes (a, b, c, and d), including daily indoor and outdoor interactions such as walking, sitting, lying, stair climbing, and touching. Our motion tracking framework not only accurately tracks the reference motion but also ensures physical realism, resolving subtle issues, such as interpenetration and floating artifacts, present in the reference data (see zoomed-in views on the right)*

![[assets/figures/papers/paper_list_l2637_https_arxiv_org_abs_2602_23205/figures/013_Figure_7.jpg]]
*Figure 7: A real-world humanoid robot imitating human motions depicted in videos*

![[assets/figures/papers/paper_list_l2637_https_arxiv_org_abs_2602_23205/figures/002_Table_1.jpg]]
*Table 1: Comparison of 4D Human & Scene datasets based on different features*

## 方法谱系与知识库定位

### 问题定位与核心瓶颈

现有高质量人体-场景数据采集依赖昂贵设备（多相机阵列、光学动作捕捉服、LiDAR），且局限于工作室环境，难以规模化收集野外自然场景下带场景上下文的人体运动数据。这一瓶颈直接阻碍了具身AI学习自然界人类行为的能力。EmbodMocap瞄准的核心问题是：**如何在野外环境中，以极低成本（两台消费级iPhone，总成本约$1000）同时重建度量级准确的人体运动与静态场景几何，且无需任何外部标记或固定相机**。

### 方法谱系：从单目到双目的关键跃迁

EmbodMocap在方法谱系中处于**单目人体-场景重建**与**专业多相机动捕系统**之间的交叉地带，其设计逻辑是保留前者的便携性，同时逼近后者的精度。

**与单目基线的对比。** 单目人体网格恢复方法（如**GVHMR**）仅依赖单视角RGB输入，通过回归模型估计SMPL参数，但缺乏场景上下文且深度歧义严重。在光学动捕基准上（Table 3, chunk=100），GVHMR的WA-MPJPE为66.56 mm，而EmbodMocap双视图优化达到56.61 mm（↓9.95）。更关键的是，单目方法无法获得场景世界坐标系下的人体运动，因此无法直接支撑具身交互任务。

单目人体-场景重建管线（如**π³ + VIMO**，原始权重）试图将SLAM重建与人体运动估计结合，但在EMDB子集上WA-MPJPE为83.56 mm（Table 4）。EmbodMocap通过在其采集数据集上微调π³与VIMO，将误差降至82.21 mm（↓1.35），表明高质量双视图数据对下游单目模型的提升作用。

**与单视角优化的对比。** 消融实验中，若仅使用单一iPhone并采用COLMAP校准与单视角SMPLify优化，其性能显著劣于双视图方案（Table 3）。核心原因在于单视角缺乏像素级稠密对应，无法有效解决深度歧义——这正是双视图设计的决定性优势。

### 核心技术贡献的因果机制

EmbodMocap的方法论创新可归结为四个因果环节，每个环节对应一个关键设计选择：

1. **双视图点追踪损失消除深度歧义。** 消融实验（Table 2）提供了强证据：去除点追踪损失L_track后，场景-人体IoU从73.0骤降至54.3，重投影误差从9.3升至44.2，深度误差从0.078恶化至2.372。这表明双视图像素级稠密对应（Eq. 5）是整体性能的基石，其作用远超出简单的多视角几何——它通过约束两个相机间的刚性变换，强制了深度估计的一致性。

2. **世界空间3D关键点损失提供绝对尺度约束。** 去除3D关键点损失L_kp3d后，IoU降至59.3，重投影误差升至20.4，深度误差升至0.609（Table 2）。与仅依赖重投影损失的单目SMPLify不同，世界空间SMPLify（Eq. 9）通过三角化的3D关键点直接约束SMPL根节点的世界平移，从而将人体运动锚定到场景坐标系中。

3. **多约束联合标定替代单一COLMAP对齐。** 传统流程依赖COLMAP进行稀疏重建与相机注册，但在纹理稀疏或动态区域易产生大误差。EmbodMocap的联合标定损失（Eq. 3）将点追踪一致性、Chamfer距离与捆绑调整损失耦合，在优化过程中相互制约，使得双视角相机轨迹能够稳健地对齐到场景世界坐标系。

4. **场景重建提供度量世界坐标系。** Stage I通过SpectacularAI SDK从单iPhone RGB-D视频获取Z-up世界坐标系下的相机参数，并利用PromptDA深度增强与TSDF融合重建静态场景网格。这一步骤为后续所有对齐操作提供了度量尺度的参考框架。

### 适用边界与局限

**硬件与采集约束。** 当前系统需要两名拍摄者手动操作iPhone，并使用激光笔进行帧级同步，采集过程依赖人力。场景重建阶段要求场景为静态且需要充分的相机运动以确保覆盖，不支持动态场景（如移动家具或他人）。消费级iPhone深度传感器的有效距离有限（室内约3.5m，室外约5m），限制了大规模开放环境下的应用。

**数据规模与多样性。** 当前数据集包含23个场景、104段序列，规模相对较小，可能不足以覆盖极端多样的交互与场景。光学动捕对比实验仅包含一名受试者的5段基本动作，人体多样性有限，因此泛化性结论需谨慎解读。

**下游任务的依赖链。** EmbodMocap对物理角色动画（Table 5）和场景感知运动跟踪（Table 6）的提升依赖于采集数据的质量。在支撑（Support）技能上，加入高度图观测后成功率从单目基线的20.6%提升至66.0%，但仍存在34%的失败率，表明数据驱动的技能学习仍受限于数据覆盖范围。

### 开放问题

1. **采集自动化。** 能否利用自拍杆或机器人持机减少人力依赖，实现单人操作甚至自主采集？
2. **动态场景适应。** 如何处理包含动态物体的场景，使系统适应真正在野环境中的人-物交互？
3. **传感器融合扩展。** 能否通过融合LiDAR或事件相机扩展有效距离并提升重建密度，以覆盖室外大范围场景？
4. **规模化瓶颈。** 在更大规模数据集上，该方法对下游具身任务的扩展性是否存在性能瓶颈？当前双视图优化的计算成本（联合标定与逐帧SMPLify）是否限制了数据生产效率？

### 知识库定位

EmbodMocap在4D人体-场景重建领域填补了**低成本野外采集**与**度量级精度**之间的空白。与现有数据集（Table 1）相比，其独特优势在于：(1) 仅需消费级设备，(2) 支持任意野外场景，(3) 提供统一世界坐标系下的人体运动与场景几何。这一能力使其成为连接**单目重建模型训练**与**具身智能下游任务**（物理仿真、人形机器人控制）的关键数据基础设施。

## 原文 PDF

![[paperPDFs/CVPR_2026/EmbodMocap_In_the_Wild_4D_Human_Scene_Reconstruction_for_Embodied_Agents.pdf]]