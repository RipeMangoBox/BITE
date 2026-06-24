---
title: "RHINO: Reconstructing Human Interactions with Novel Objects from Monocular Videos"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RHINO_Reconstructing_Human_Interactions_with_Novel_Objects_from_Monocular_Videos.pdf
project_link: "https://lxxue.github.io/RHINO"
code_link: null
aliases:
- RHINO
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: RHINO 利用 3D 感知基础模型（MASt3R）提取稠密、鲁棒的特征匹配，从而通过运动解耦（motion disentanglement）将物体运动从表观运动中分离出来；同时用可微神经 SDF 统一表达几何与接触，以交替优化策略提升形状精度与物理合理性。
primary_logic: 将合成式神经符号距离场（per-component neural SDF）同时用于几何重建和接触推理，将接触作为可微距离信号进行优化，从而在无模板、无先验知识的情况下，从单目视频中获得物理一致的人-物交互重建。
claims:
- RHINO 在 BenchRHINO 数据集上的形状重建指标显著优于所有基线，物体 Chamfer Distance 降至 1.21 cm，而 HOLD 为 4.41 cm，InterTrack 为 11.16 cm。
- 去掉运动解耦后，整体 Chamfer Distance 从 2.65 升至 10.21，说明分离相机与物体运动至关重要。
- 接触优化将穿透深度 (PD) 降低约 56%（从 1.088 降至 0.477），同时大幅提升接触召回率和 F1，证明可微接触先验有效。
- 使用 MASt3R 特征匹配替代传统 SP+SG 或 LoFTR，使物体重建成功率更高，CD 从 4.25 降至 1.09，且在低纹理、对称物体上表现出色。
---

# RHINO: Reconstructing Human Interactions with Novel Objects from Monocular Videos

> [!tip] 核心洞察
> 将合成式神经符号距离场（per-component neural SDF）同时用于几何重建和接触推理，将接触作为可微距离信号进行优化，从而在无模板、无先验知识的情况下，从单目视频中获得物理一致的人-物交互重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | RHINO：从单目视频重建与未知物体的人类交互 |
| 英文题名 | RHINO: Reconstructing Human Interactions with Novel Objects from Monocular Videos |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.17014) · [Project](https://lxxue.github.io/RHINO) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | RHINO |
| Dataset | BenchRHINO |

> [!tip] 效果简介
> - BenchRHINO (形状重建) 上，Chamfer Distance (Object) [cm] ↓ 1.21 vs 4.41 (HOLD), 11.16 (InterTrack) (-3.20 / -9.95)；Chamfer Distance (Human) [cm] ↓ 2.65 vs 2.69 (HSR), 4.66 (InterTrack) (-0.04 / -2.01)。
> - BenchRHINO (新视角合成) 上，PSNR ↑ / SSIM ↑ / LPIPS ↓ 25.80 / 0.832 / 0.212 vs 22.65 / 0.791 / 0.246 (HSR), 17.92 / 0.646 / 0.513 (HOLD) (+3.15 / +0.041 / -0.034 (vs HSR))。

## 概述

**问题背景与瓶颈** 从单目视频中重建三维人-物交互（HOI）是计算机视觉的核心挑战。现有方法或假设静态场景（如 **HSR**），或依赖已知物体模板，或仅在相机坐标系中运行（如 **HOLD**），无法在移动相机条件下同时恢复人体、未知物体与静态场景在世界坐标系中的形状与运动。核心瓶颈在于：相机运动与物体运动在二维观测中高度纠缠，缺少物体先验使位姿估计困难，且缺乏显式接触约束导致重建结果物理不合理。

**核心方法与因果机制** RHINO 提出三阶段框架解决上述问题。其关键因果链路为：(1) 利用 3D 感知基础模型 **MASt3R** 提取稠密、鲁棒的特征匹配，稳定低纹理区域的运动推断结构（SfM），从而获得物体表观运动与场景相机运动的初始估计；(2) 通过**运动解耦**（motion disentanglement）——识别物体静止帧并求解相似变换，将相机运动从表观运动中分离，恢复物体在世界坐标系中的真实位姿；(3) 采用**合成式神经符号距离场**（per-component neural SDF）统一表达人、物、场景的几何与外观，并将接触建模为可微距离信号，通过两阶段交替优化（先冻结形状后细化姿态）提升物理合理性。

**主要结果与证据强度** 在自建数据集 BenchRHINO 上，RHINO 的物体形状重建 Chamfer Distance 降至 **1.21 cm**，相比 HOLD（4.41 cm）和 InterTrack（11.16 cm）分别降低 **72.6%** 和 **89.2%**（Table 1，高置信度）。新视角合成 PSNR 达到 **25.80 dB**，显著优于 HSR（22.65 dB）和 HOLD（17.92 dB）（Table 2，高置信度）。消融实验证实：移除运动解耦后整体 CD 从 2.65 升至 10.21（Table 4），接触优化将穿透深度降低约 **56%**（从 1.088 降至 0.477，Table 5），MASt3R 特征匹配使物体 CD 从 4.25 降至 1.09（Table 3）。这些证据一致表明，运动解耦与可微接触先验是性能提升的决定性因素。

**局限与开放问题** 当前方法假设物体为刚体，对可变形物体（如衣物）不适用；在严重遮挡、快速运动或仅有限视角观测时，重建质量会下降。未来方向包括扩展到多人与多物体场景、引入时序先验处理快速运动、以及支持铰接或可变形物体的重建。

## 背景与动机

### 问题背景

从单目 RGB 视频中重建三维场景、人体及其与物体的交互，是计算机视觉与图形学中长期存在的核心挑战。随着神经隐式表示（NeRF、NeuS 等）和参数化人体模型（SMPL-X）的成熟，静态场景与孤立人体的 4D 重建已取得显著进展。然而，当场景中的人开始**动态操纵未知物体**时，重建难度急剧上升：相机视角在移动，物体在运动，二者运动在图像平面上纠缠为单一的“表观运动”（apparent motion），使得从像素观测中分离出各运动分量变得极为困难。

更具体地，这类场景面临三重瓶颈：

1. **运动纠缠**：相机运动与物体运动在单目视频中不可区分，直接使用表观运动进行重建会导致物体位姿与形状的严重退化。
2. **物体先验缺失**：被操纵的物体是“未知的”（novel）——没有预先扫描的模板，也没有类别级先验，系统必须从零开始推断其几何形状。
3. **接触信息缺失**：人与物体的物理交互（抓握、推移等）需要精确的接触约束，但现有方法缺乏将接触作为显式优化信号的手段。

### 现有方法缺口

当前最相关的工作可归为三类，但每一类都存在根本性局限：

- **静态场景人体重建方法**（如 **HSR**）能够忠实恢复静态背景和其中移动的人体，但假设场景本身不变。当人体推动桌子或移动椅子时，这些方法将物体运动误判为场景形变，导致物体重建崩溃（见 Figure 2 中桌子的退化重建）。
- **手–物交互重建方法**（如 **HOLD**）专注于从单 RGB 视频恢复手与物体的交互，但仅在相机坐标系中运行，无法建模全局场景上下文，且物体位姿估计对噪声敏感，在移动相机场景下表现脆弱。
- **模板无关的交互追踪方法**（如 **InterTrack**）尝试追踪人–物交互的稀疏点云，但难以泛化到完全未知的物体类别，且输出的稀疏几何缺乏细节形状，无法支撑高质量的交互重建。

上述方法的共同缺陷在于：**无法在统一世界坐标系中，同时解决运动分离、未知物体几何恢复和物理接触推理这三个相互耦合的问题**。

### 本文动机

RHINO 的核心动机正是填补这一空白：**从一段移动相机拍摄的单目 RGB 视频中，在统一世界坐标系下，重建出动态的人体、未知的被操纵物体以及静态背景场景**。这一目标要求系统具备三项关键能力：

- **运动解耦**：将物体运动从相机运动导致的表观运动中分离出来，恢复物体在世界坐标系中的真实运动轨迹。
- **无模板几何重建**：在没有任何物体先验（模板、类别、纹理先验）的情况下，仅凭视频观测恢复物体的精细形状。
- **物理合理的接触建模**：将接触作为可微信号纳入优化过程，使得重建结果不仅视觉上逼真，而且在物理上合理——手不穿透物体、不悬空漂浮。

RHINO 通过三个技术支柱实现这一目标：利用 3D 感知基础模型（MASt3R）提取稠密特征匹配以稳定运动估计；通过运动解耦公式将相机与物体运动分离；以及使用合成式神经符号距离场（per-component neural SDF）同时表达几何与接触，以交替优化策略联合提升形状精度与物理合理性。

## 核心创新

RHINO 的核心创新在于将**运动解耦**与**合成式神经 SDF 联合优化**深度整合，首次在统一世界坐标系下实现了从单目移动视频中同时重建人、未知物体和静态场景，并确保物理上合理的接触。与现有方法相比，RHINO 在三个关键维度上实现了系统性突破。

### 1. 基于 3D 感知特征的运动解耦

现有方法（如 **HOLD**、**InterTrack**）要么仅在相机坐标系中运行，要么直接使用表观运动进行重建，无法在移动相机场景中分离相机与物体的运动。RHINO 的核心洞察是：当相机和物体同时运动时，图像中观测到的物体运动是两者运动的纠缠结果。RHINO 通过以下机制实现解耦：

- **场景-物体运动分离**：利用 SAM2 分割背景区域，通过 SfM 估计相机在世界坐标系中的运动轨迹 $\mathbf{C}_{\mathrm{scn}}$；同时对物体区域使用 MASt3R 提取稠密、3D 感知的特征匹配，通过 SfM 获得物体的表观运动轨迹 $\mathbf{C}_{\mathrm{obj}}$。
- **相似变换对齐**：识别物体静止的帧（$\mathbf{P}_{\mathrm{obj}} = \mathbf{I}$），通过相似变换 $\mathbf{T} \cdot \mathbf{S}$ 将物体相机轨迹与场景相机轨迹对齐，即 $\mathbf{T} \cdot \mathbf{S} \cdot \mathbf{C}_{\mathrm{obj}} = \mathbf{C}_{\mathrm{scn}}$。随后，通过 $\mathbf{P}_{\mathrm{obj}} = \mathbf{C}_{\mathrm{scn}}^{-1} \cdot \mathbf{T} \cdot \mathbf{S} \cdot \mathbf{C}_{\mathrm{obj}}$ 从表观运动中“移除”相机运动，恢复物体在世界坐标系中的真实运动。

消融实验（**Table 4**）表明，移除运动解耦后，整体 Chamfer Distance 从 **2.65 cm 升至 10.21 cm**，所有指标大幅恶化，验证了该模块的不可或缺性。

### 2. 从稀疏匹配到稠密 3D 感知匹配的特征升级

传统物体位姿估计依赖 SuperPoint+SuperGlue (SP+SG) 或 LoFTR 等通用特征匹配器，在低纹理、对称或遮挡物体上容易产生稀疏、不一致的匹配点甚至错误匹配。RHINO 转而使用 **MASt3R** 这一 3D 感知基础模型：

- MASt3R 提供**稠密、鲁棒的 3D 对应关系**，即使在低纹理区域也能稳定匹配（见 **Figure S.1**，SP+SG 产生稀疏关键点，LoFTR 出现错误背景匹配）。
- 定量消融（**Table 3**）显示，使用 MASt3R 后物体重建 Chamfer Distance 从 SP+SG 的 **4.25 cm** 和 LoFTR 的 **3.97 cm** 降至 **1.09 cm**，且成功率更高。

### 3. 可微接触先验驱动的物理合理性优化

现有方法（如 HOLD、InterTrack）缺乏显式的接触建模，重建结果常出现手部漂浮或穿透物体的问题。RHINO 利用 per-component 神经 SDF 的天然优势，将接触转化为**可微距离信号**：

- **吸引损失** $\mathcal{L}_{\mathrm{contact}}$：当人体接触点位于物体外部（SDF ≥ 0）时，通过 $\alpha_1 \tanh(\xi_{x_c}^O / \alpha_2)^2$ 惩罚，吸引手部向物体表面靠近。
- **碰撞损失** $\mathcal{L}_{\mathrm{collision}}$：当接触点穿透物体内部（SDF < 0）时，通过类似形式惩罚穿透。
- **两阶段交替优化**：先冻结形状优化人-物姿态以减少穿透和吸引接触，再联合优化所有参数，避免形状与姿态的耦合干扰。

消融实验（**Table 5**）显示，接触优化将穿透深度（PD）从 **1.088 降至 0.477**（降低约 56%），同时大幅提升接触召回率和 F1 分数。**Figure 8** 的定性对比直观展示了接触优化消除手部穿透和漂浮的效果。

### 4. 合成式神经场统一表达

RHINO 对人、物体和场景分别建模独立的神经 SDF 和外观场，通过**合成式体渲染**（compositional volume rendering）将三部分沿射线排序并累积颜色：

$$C(r) = \sum_{i=1}^{3N} \tau_i \mathbf{c}^{(\cdot)}(\mathbf{x}^i)$$

这一设计使得接触损失可以直接在物体 SDF 上计算，同时各组件通过逆 LBS（人体）和刚体变换（物体）映射到规范空间，实现统一优化。这种“表达即约束”的设计是 RHINO 在物理合理性上超越基线（如 HSR 仅假设静态场景，HOLD 缺乏全局建模）的关键架构优势。

## 整体框架

RHINO 是一个三阶段框架，从单目 RGB 视频中恢复统一世界坐标系下的**人体**、**未知被操纵物体**和**静态场景**的三维重建。其核心设计围绕一个瓶颈展开：当相机与物体同时运动时，表观运动是二者的纠缠结果，直接使用会导致重建崩溃。RHINO 的因果调控旋钮在于**运动解耦**——利用 3D 感知基础模型提取的稠密特征匹配，将物体运动从相机运动中分离出来——以及**可微神经 SDF 统一表达几何与接触**，使接触信号以距离损失的形式参与优化，从而在无模板、无先验知识的前提下获得物理一致的人-物交互重建。

### 输入输出

- **输入**：一段单目 RGB 视频，其中包含一个移动相机、一个被操纵的未知刚体物体，以及一个静态背景场景。
- **输出**：
  - 人体、物体、场景在统一世界坐标系中的**神经隐式形状与纹理**（per-component neural SDF + appearance field）；
  - 物体在世界坐标系中的**每帧刚体位姿**；
  - 人体在世界坐标系中的**每帧 SMPL-X 姿态与形状参数**；
  - 相机在世界坐标系中的**每帧位姿**。

### 三阶段流水线

如图 4 所示，RHINO 将问题分解为三个串行且相互依赖的阶段：

**阶段一：初始化与坐标系统一（Sec. 3.1–3.2）**
1. **场景与相机运动初始化**：利用 SAM2 分割背景区域，对场景像素执行 SfM，估计相机在世界坐标系中的位姿轨迹 $\mathbf{C}_{\mathrm{scn}}$ 和粗糙场景点云。
2. **物体位姿初始化**：基于 MASt3R 在物体区域提取稠密、鲁棒的 3D 感知特征匹配，再通过 SfM 获得物体在相机坐标系中的表观运动轨迹 $\mathbf{C}_{\mathrm{obj}}$。
3. **人体初始化与对齐**：使用 AiOS 估计 SMPL-X 并在相机坐标系下优化关键点，随后通过投影与地面接触约束将人体注册到世界坐标系。
4. **运动解耦与坐标系统一**：识别物体静止帧，通过相似变换对齐相机轨迹，从表观运动中“移除”相机运动，得到物体在世界坐标系中的位姿 $\mathbf{P}_{\mathrm{obj}}$。核心关系为：
   $$
   \mathbf{T} \cdot \mathbf{S} \cdot \mathbf{C}_{\mathrm{obj}} = \mathbf{C}_{\mathrm{scn}} \cdot \mathbf{P}_{\mathrm{obj}}
   $$
   当物体静止（$\mathbf{P}_{\mathrm{obj}} = \mathbf{I}$）时，退化为两个相机轨迹之间的相似变换，可直接求解 $\mathbf{T}$ 和 $\mathbf{S}$；进而推广到运动帧，解出完整的物体世界位姿序列。

**阶段二：合成式神经场联合优化（Sec. 3.3）**
- 为人体、物体、场景分别维护独立的神经 SDF 与 appearance 场。
- 人体点通过逆 LBS 映射到规范空间，物体点通过刚体变换映射到规范空间，场景点直接在世界坐标系中表达。
- 沿相机射线对三个组件的采样点按深度排序，通过**合成体渲染**累积颜色：
  $$
  C(r) = \sum_{i=1}^{3N} \tau_i \, \mathbf{c}^{(\cdot)}(\mathbf{x}^i)
  $$
- 联合优化使用多帧 RGB、掩膜、深度和法线损失，同时细化所有组件的形状、纹理以及人体与物体的姿态。

**阶段三：可微接触优化（Sec. 3.4）**
- 利用物体 SDF 在人体接触点（如手部顶点）计算可微接触损失与碰撞损失：
  $$
  \mathcal{L}_{\mathrm{contact}} = \alpha_1 \tanh(\xi_{x_c}^O / \alpha_2)^2 \quad \text{if } \xi_{x_c}^O \geq 0
  $$
  $$
  \mathcal{L}_{\mathrm{collision}} = \beta_1 \tanh(\xi_{x_c}^O / \beta_2)^2 \quad \text{if } \xi_{x_c}^O < 0
  $$
- 采用两阶段交替优化策略：先冻结形状优化人体-物体姿态以改善接触，再解冻形状进行全局微调。消融实验（Table 5, Figure 8）表明，接触优化将穿透深度降低约 56%（从 1.088 降至 0.477），并大幅提升接触召回率和 F1 分数。

### 关键设计决策与证据

- **MASt3R 特征匹配替代传统 SP+SG / LoFTR**：在低纹理、对称物体上提供更稠密、更鲁棒的对应关系，使物体重建 CD 从 4.25 cm（SP+SG）和 3.97 cm（LoFTR）降至 1.09 cm（Table 3, Figure 7）。
- **运动解耦的必要性**：移除运动解耦后，整体 Chamfer Distance 从 2.65 cm 飙升至 10.21 cm（Table 4），证实分离相机与物体运动是统一世界坐标系重建的前提。
- **可微接触先验**：将接触建模为 SDF 距离信号而非硬约束，使物理合理性可通过梯度优化直接提升，同时不牺牲形状精度。

### 限制与边界条件

当前框架假设物体为**刚体**，无法处理可变形物体（如衣物、软玩具）；当物体仅被有限视角观察、存在快速运动模糊或极端遮挡时，特征匹配与运动解耦的可靠性下降，可能导致形状不完整或位姿噪声。这些场景仍需手动验证重建质量。

### 补充图表

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_17014/figures/004_Figure_4.jpg]]
*Figure 4: Method Overview. Starting with initialized global human and decoupled object poses (Sec. 3.1, Sec. 3.2), we sample points along the camera ray for the human, object and static scene. To enable consistent representation, sampled points are warped into canonical space using inverse LBS for the human and the estimated rigid transformation for the object. All components are then rendered holistically via compositional volume rendering. A global optimization (Sec. 3.3) helps learn the 3D representation of all elements and refine the initial poses via a photometric loss, while encouraging physically plausible contact by leveraging differentiable contact priors (Sec. 3.4)*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_17014/figures/001_Figure_1.jpg]]
*Figure 1: We develop RHINO, a novel framework that reconstructs detailed (dynamic) 3D human-object interactions (HOI) and the surrounding scene within a common world frame from a monocular RGB video with a moving viewpoint. RHINO uses per-component neural SDFs to: (i) capture shape details, and (ii) encourage contact via a differentiable distance term. The “zoom-in insets” highlight plausible contacts. RHINO requires neither a pre-scanned object template nor prior knowledge of the object, unlike most existing work*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_17014/figures/002_Figure_2.jpg]]
*Figure 2: Existing work, such as the HSR [70] SotA method, can faithfully reconstruct the 3D shape of a static scene and of a person moving in it, but struggles when people manipulate objects. As illustrated, when a person pushes a table (top), the static part of the scene is reconstructed well (bottom row, two views), but the table’s reconstruction is degenerate (see the red highlight). Here we do not show the reconstructed person to reduce occlusions*

## 核心模块与公式推导

RHINO 采用三阶段级联框架（Fig. 4），将单目动态视频中的人、未知物体与静态场景统一重建在世界坐标系中。其核心模块按执行顺序为：**初始化与运动解耦**、**合成式神经场联合优化**、**可微接触精细化**。以下逐一阐述各模块的关键机制与支撑公式。

### 1. 初始化与运动解耦

该模块的目标是为后续联合优化提供粗糙但世界坐标系一致的几何与位姿初值。流程分为三步：

**场景与相机运动初始化**：利用 SAM2 分割背景区域，仅对场景像素执行 SfM，获得相机位姿序列 $\mathbf{C}_{\mathrm{scn}} = \{\mathbf{C}_{\mathrm{scn}}^{i}\}_{i=1}^{N}$ 及稀疏场景点云（Fig. 3a）。

**物体表观运动估计**：对物体掩膜区域使用 **MASt3R** 提取稠密、鲁棒的 3D 感知特征匹配，再通过 SfM 获得物体在相机坐标系下的“表观运动”轨迹 $\mathbf{C}_{\mathrm{obj}}$（Fig. 3b）。消融实验（Table 3, Fig. 7）表明，MASt3R 特征匹配在低纹理、对称物体上显著优于传统的 SP+SG 或 LoFTR，物体重建 CD 从 4.25 cm / 3.97 cm 降至 1.09 cm。

**运动解耦与坐标系统一**：当相机与物体同时运动时，$\mathbf{C}_{\mathrm{obj}}$ 中纠缠了相机运动。RHINO 通过识别物体静止帧（$\mathbf{P}_{\mathrm{obj}} = \mathbf{I}$），求解相似变换 $\mathbf{S}$（尺度）与 $\mathbf{T}$（刚性对齐），建立两条相机轨迹之间的映射关系：

$$\mathbf{T} \cdot \mathbf{S} \cdot \mathbf{C}_{\mathrm{obj}} = \mathbf{C}_{\mathrm{scn}} \cdot \mathbf{P}_{\mathrm{obj}} \tag{Eq. 1}$$

当物体静止时简化为 $\mathbf{T} \cdot \mathbf{S} \cdot \mathbf{C}_{\mathrm{obj}} = \mathbf{C}_{\mathrm{scn}}$，可闭式求解 $\mathbf{S}, \mathbf{T}$。推广到运动帧，物体在世界坐标系中的位姿可通过“移除”相机运动恢复：

$$\mathbf{P}_{\mathrm{obj}} = \mathbf{C}_{\mathrm{scn}}^{-1} \cdot \mathbf{T} \cdot \mathbf{S} \cdot \mathbf{C}_{\mathrm{obj}} \tag{Eq. 4}$$

运动解耦是框架的**关键因果旋钮**：移除该模块后，世界坐标系下整体 CD 从 2.65 cm 飙升至 10.21 cm（Table 4），验证了分离相机与物体运动对全局重建的决定性作用。

**人体初始化与对齐**：使用 AiOS 在相机坐标系下估计 SMPL-X 参数，再通过投影约束与地面接触约束将人体注册到世界坐标系中。

### 2. 合成式神经场联合优化

获得初始化位姿后，RHINO 采用 **per-component 神经 SDF** 分别表达人体、物体与场景的几何与外观，并通过合成体渲染进行联合优化。

**规范空间映射**：为保持时序一致性，人体采样点通过逆 LBS 变换映射到规范空间 $\mathbf{x}^{H} = LBS^{-1}(\mathbf{x}^{\prime H}, \pmb{\theta})$，物体采样点通过逆刚性变换映射 $\mathbf{x}^{O} = \mathbf{P}_{obj}^{-1} \mathbf{x}^{\prime O}$。场景点本身静止，无需映射。

**合成体渲染**：沿相机射线对三个组件各采样 $N$ 个点，按深度排序后累积颜色：

$$C(r) = \sum_{i=1}^{3N} \tau_{i} \, \mathbf{c}^{(\cdot)}(\mathbf{x}^{i}) \tag{Eq. 11}$$

其中 $\tau_i$ 为累积透射率，$\mathbf{c}^{(\cdot)}$ 为对应组件的外观场输出。该渲染方式使得人体、物体、场景在遮挡关系下自然合成，支持端到端可微优化。

**联合优化损失**：除 RGB 渲染损失外，还引入掩膜损失、深度损失、法线损失，以及针对人体的两项辅助损失——

- **身体先验损失**（Eq. S.1）：鼓励 SMPL-X 网格内部的点具有负 SDF 值，修复因遮挡导致的截断身体几何：
  $$L_{\mathrm{body}} = \gamma_{1} \tanh\left( f_{\mathrm{sdf}}^{H}(x_{\mathrm{b}}) / \gamma_{2} \right)^{2} \quad \text{for } f_{\mathrm{sdf}}^{H}(x_{\mathrm{b}}) \ge 0$$

- **手部 SDF 损失**（Eq. S.2）：利用 SMPL-X 网格提供的 SDF 真值监督手部区域，改善精细手部重建：
  $$L_{\mathrm{hand}} = w(x_{\mathrm{h}}) \, | f_{\mathrm{sdf}}^{H}(x_{\mathrm{h}}) - \xi(x_{\mathrm{h}}) |$$

### 3. 可微接触精细化

RHINO 的核心洞察在于将 **per-component 神经 SDF 同时用于几何重建与接触推理**——接触被表达为可微距离信号，直接参与优化。

从 SMPL-X 网格采样接触点 $x_c$（如指尖、手掌），查询物体 SDF 值 $\xi_{x_c}^{O}$：

- **接触损失**（吸引）：当接触点在物体外部（$\xi_{x_c}^{O} \ge 0$），惩罚正值 SDF，将人体拉向物体表面：
  $$\mathcal{L}_{\mathrm{contact}} = \alpha_{1} \tanh\left( \xi_{x_c}^{O} / \alpha_{2} \right)^{2} \quad \text{if } \xi_{x_c}^{O} \geq 0 \tag{Eq. 12}$$

- **碰撞损失**（穿透惩罚）：当接触点穿透物体内部（$\xi_{x_c}^{O} < 0$），惩罚负值 SDF，防止相互贯穿：
  $$\mathcal{L}_{\mathrm{collision}} = \beta_{1} \tanh\left( \xi_{x_c}^{O} / \beta_{2} \right)^{2} \quad \text{if } \xi_{x_c}^{O} < 0 \tag{Eq. 13}$$

接触优化采用**两阶段交替策略**：先冻结形状参数优化人体/物体位姿以减少穿透与悬空，再联合微调形状与位姿。消融实验（Table 5, Fig. 8）表明，该模块将穿透深度（PD）降低约 56%（从 1.088 降至 0.477），同时大幅提升接触召回率与 F1，证明了可微接触先验对物理合理性的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_17014/figures/003_Figure_3.jpg]]
*Figure 3: Camera & Object motion (Sec. 3.1, Sec. 3.2). When both the camera and object move, their motion entangles into “apparent” motion. To disentangle them, we (a) estimate camera motion in the world frame via SfM on scene-only pixels, (b) estimate apparent motion via SfM on object-only pixels, (c–d) estimate object motion in the world frame by “removing” the camera motion from the apparent one*

## 实验与分析

### 数据集与评估协议

作者构建了 **BenchRHINO** 数据集用于定量评估。该数据集包含多条以移动相机拍摄的单目 RGB 视频，记录了人与未知物体的动态交互过程，并提供了通过多视角扫描获取的物体与场景真值三维形状。对于人体，真值形状由优化后的 SMPL-X 网格提供。评估时，由于不同方法输出格式和坐标系各异，所有结果均经过刚性对齐（ICP 或 Procrustes）后再计算指标，具体对齐方案见附录 S.2.4，以确保比较的公平性。此外，还引入了 **WildRHINO** 作为分布外测试集，用于评估方法的泛化能力。

### 形状重建主结果

Table 1 报告了在 BenchRHINO 数据集上的形状重建定量结果。RHINO 在物体重建上取得了压倒性优势：物体 Chamfer Distance 降至 **1.21 cm**，而 HOLD 为 4.41 cm，InterTrack 为 11.16 cm，分别降低了约 72.6% 和 89.2%。人体重建方面，RHINO 的 Chamfer Distance 为 **2.65 cm**，与 HSR（2.69 cm）基本持平，并显著优于 InterTrack（4.66 cm）。在人+物联合指标上，RHINO 的 CD 为 2.42 cm，远低于 HOLD 的 5.12 cm 和 InterTrack 的 7.87 cm。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_17014/figures/005_Table_1.jpg]]
*Table 1: Evaluation on shape reconstruction. We evaluate on all BenchRHINO sequences, using standard metrics. Columns denote the human (H), object (O), or scene (S). The “Setup” columns indicate whether each model (row) estimates shape for the human, object, or scene*

定性结果（Figure 5）进一步印证了上述结论：HOLD 在物体位姿噪声较大时形状重建退化严重，且无法正确建模交互关系；InterTrack 虽能恢复出大致合理的物体形状，但人体与物体位姿误差较大，导致交互建模失败。RHINO 则忠实地重建了交互过程中的细节形状，与真值最为接近。在更具挑战性的 WildRHINO 分布外数据上（Figure 6），InterTrack 完全失效，而 RHINO 依然能给出反映交互关系的合理重建。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_17014/figures/011_Figure_5.jpg]]
*Figure 5: Evaluation on shape reconstruction (Sec. 4.3) on our BenchRHINO dataset (Sec. 4.1). HOLD [14] struggles with noisy object poses (rows 2, 4) and fails to model interaction. InterTrack [69] recovers reasonable object shape but fails to model the interaction due to large human and object pose errors. Our method (RHINO) faithfully recovers interactions, which lie closer to the ground truth (GT)*

### 新视角合成主结果

Table 2 报告了新视角合成的定量结果。RHINO 在所有指标上均显著优于两个基线：PSNR 达到 **25.80 dB**（HSR 为 22.65 dB，HOLD 为 17.92 dB），SSIM 为 **0.832**（HSR 为 0.791，HOLD 为 0.646），LPIPS 降至 **0.212**（HSR 为 0.246，HOLD 为 0.513）。这一优势源于 RHINO 能够在统一世界坐标系中同时建模动态前景物体与静态背景场景，而 HOLD 仅在相机坐标系中运行，无法重建背景；HSR 则假设场景静态，无法处理被操纵的动态物体。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_17014/figures/006_Table_2.jpg]]
*Table 2: Evaluation on novel-view synthesis. We evaluate on all BenchRHINO sequences. Our method (RHINO) provides substantially better view synthesis quality, outperforming both baselines across all metrics*

### 物体位姿估计消融

物体位姿初始化的质量直接决定了后续重建的成败。Table 3 比较了三种特征匹配策略在物体位姿估计上的表现（仅报告所有基线均未失败的 5 个序列）。基于 **MASt3R** 的 3D 感知特征匹配使物体重建 CD 降至 **1.09 cm**，而传统的 SuperPoint + SuperGlue 组合为 4.25 cm，LoFTR 为 3.97 cm。Figure 7 的定性对比显示，SP+SG 的关键点过于稀疏且不一致，LoFTR 则容易产生错误的背景匹配，而 MASt3R 提供了稠密、鲁棒的对应关系，尤其在低纹理和对称物体上表现出色（另见补充材料 Figure S.1）。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_17014/figures/013_Table_3.jpg]]
*Table 3: Evaluation on object pose estimation (Sec. 4.5). We compare to SP+SG, a HOLD-inspired [14] baseline that uses SuperPoint [10] and SuperGlue [50], and one that uses LoFTR [53]. Results are reported for BenchRHINO sequences for which all baselines do not fail; see the list of sequences in Supp. Mat*

### 运动解耦消融

Table 4 展示了移除运动解耦模块（w/o MD）的影响。当不分离相机运动与物体运动、直接使用表观运动进行世界坐标系重建时，整体 Chamfer Distance 从 **2.65 cm 急剧恶化至 10.21 cm**，所有子指标（人体、物体、场景）均大幅下降。这强有力地证明了运动解耦是实现在统一世界坐标系中重建动态人-物交互场景的必要前提。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_17014/figures/015_Table_4.jpg]]
*Table 4: Ablation on motion disentanglement (MD) (Sec. 4.5). Removing motion disentanglement leads to a large drop across all metrics, confirming it is essential for world-frame reconstruction*

### 接触优化消融

Table 5 和 Figure 8 展示了可微接触先验的贡献。移除接触优化后（w/o Contact Opt），穿透深度（PD）从 **0.477 升至 1.088**（恶化约 56%），接触召回率和 F1 分数也显著降低。定性结果（Figure 8 及补充材料 Figure S.4）直观地展示了差异：无接触优化时，重建的手部要么穿透物体内部，要么悬浮在物体表面之上而无法形成有效接触；完整方法则恢复出物理上更合理的抓握姿态，与真值更为一致。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_17014/figures/016_Table_5.jpg]]
*Table 5: Ablation on contact refinement (Sec. 4.5). Refining pose via contact reduces penetration depth (PD) and increases contact recall and F1, showing its importance for physical plausibility*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_17014/figures/014_Figure_8.jpg]]
*Figure 8: Effects of contact. We show reconstructions of our framework with (“RHINO (Ours)”) and without (“w/o Contact Opt”) the physical losses of Eq. (12) and Eq. (13). For a bigger version with zoom-in impressions, see Supp. Mat*

### 失败模式与局限性

尽管 RHINO 在 BenchRHINO 和 WildRHINO 上均表现出色，作者明确指出了以下失败模式：

1. **有限视角覆盖**：当物体在视频中仅被有限视角观察（如始终正面朝向相机），未见面的形状可能不完整或不准确。
2. **快速运动**：快速运动导致的运动模糊和帧间大位移会使特征匹配不可靠，进而使运动解耦产生噪声。
3. **极端遮挡**：连续多帧物体几乎完全被身体遮挡时，物体形状和姿态缺乏足够约束，可能出现幻觉几何。
4. **刚体假设**：当前方法假设物体为刚体，无法处理可变形物体（如衣物、软玩具），刚性运动模型会引入伪影。

这些局限性也指向了未来的研究方向：引入时间先验和生成式形状先验以应对快速运动和严重遮挡，扩展至铰接或可变形物体，以及探索多人与多物体的交互场景。

### 补充图表

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_17014/figures/009_Figure.jpg]]

## 方法谱系与知识库定位

### 与现有工作的关系

RHINO 处于**单目动态场景重建**与**人-物交互理解**的交叉点。其核心定位可以从以下三个维度与现有基线建立谱系关系。

**静态场景重建的延伸与突破。** 以 **HSR** 为代表的 SotA 方法能够在移动相机下高质量重建静态场景和其中运动的人体，但其底层假设——场景结构在观测期间保持不变——在物体被操纵时被打破。如 Figure 2 所示，当人推动桌子时，HSR 可以忠实重建静态背景，但桌子的重建完全退化。RHINO 通过引入**运动解耦**机制，将动态前景物体从静态背景中分离，从而突破了这一根本性假设约束。这一突破的量化证据来自 Table 1：HSR 仅能评估人体（CD 2.69 cm）和场景，而 RHINO 额外实现了物体重建（CD 1.21 cm），且在人体指标上保持可比水平（CD 2.65 cm）。

**相机坐标系内交互重建的坐标系升级。** **HOLD** 是单 RGB 视频手-物交互重建的代表方法，但其在相机坐标系内运行，缺乏全局场景建模能力。这意味着：(1) 无法重建背景场景；(2) 相机运动与物体运动纠缠，导致物体姿态估计噪声大。Table 1 中 HOLD 的物体 CD 为 4.41 cm（RHINO 为 1.21 cm），且在新视角合成中 HOLD 的 PSNR 仅为 17.92 dB，远低于 RHINO 的 25.80 dB（Table 2）。值得注意的是，RHINO 在 WildRHINO 实验中将自身估计的物体姿态提供给 HOLD（记为 HOLD*），HOLD* 的物体形状质量显著提升（Figure 6），这反向验证了 RHINO 运动解耦对下游重建的增益是**可迁移的**。

**模板无关交互追踪的形状精度跃升。** **InterTrack** 是模板无关的 3D 人-物交互追踪方法，输出稀疏点云。其优势在于不依赖物体先验，但难以泛化到未知物体且缺乏细节形状。Table 1 中 InterTrack 的物体 CD 高达 11.16 cm，人体 CD 为 4.66 cm，均显著劣于 RHINO。RHINO 通过**合成式神经 SDF** 统一表达几何与外观，将重建从稀疏点云提升为带纹理的连续曲面，实现了数量级的精度提升。

### 关键技术组件的谱系溯源

RHINO 的三个核心组件分别对现有技术栈进行了关键升级：

1. **特征匹配：从稀疏手工特征到 3D 感知稠密匹配。** 传统 SfM 管线依赖 SuperPoint + SuperGlue（**SP+SG**）或 LoFTR 进行特征匹配。Table 3 的消融实验表明，SP+SG 和 LoFTR 的物体重建 CD 分别为 4.25 cm 和 3.97 cm，而 RHINO 采用的 **MASt3R** 特征匹配将 CD 降至 1.09 cm。Figure S.1 揭示了失败模式：SP+SG 在低纹理区域产生稀疏、不一致的关键点；LoFTR 在物体-背景边界产生错误匹配。MASt3R 的 3D 感知特性使其在对称、低纹理物体上仍能提供鲁棒的稠密对应。

2. **运动建模：从表观运动到解耦运动。** 大多数方法直接使用表观运动进行重建。Table 4 的消融实验是 RHINO 最具说服力的证据之一：移除运动解耦（w/o MD）后，整体 CD 从 2.65 cm 飙升至 10.21 cm，所有指标全面恶化。这直接证明了在移动相机场景中，**分离相机运动与物体运动是重建可行性的必要条件**，而非锦上添花。

3. **接触建模：从隐式约束到可微距离先验。** 现有方法要么无显式接触建模，要么仅依赖图像投影损失间接约束。RHINO 利用 per-component 神经 SDF 将接触转化为可微距离信号。Table 5 的消融显示，移除接触优化后，穿透深度（PD）从 0.477 升至 1.088（恶化约 56%），接触召回率和 F1 显著下降。Figure 8 的定性结果进一步表明，无接触优化时手部要么穿透物体，要么悬浮在物体上方，无法形成合理接触。

### 适用边界与局限

RHINO 的能力边界由以下假设和实际约束共同定义：

**刚性物体假设。** 当前框架假设被操纵物体为刚体，使用单一刚性变换将物体点从世界坐标系映射到规范坐标系。这一假设排除了可变形物体（如衣物、软玩具、被挤压的包装盒）和铰接物体（如笔记本电脑、抽屉）。对于可变形物体，刚性运动模型会引入系统性伪影；对于铰接物体，需要引入部件级运动分解或关节参数化。

**观测完整性与遮挡。** 当物体在视频中仅被有限视角观察（如始终正面朝向相机），未见面的形状可能不完整或不准确。极端遮挡场景（连续多帧物体几乎完全被身体遮挡）会导致物体形状和姿态欠约束，可能出现幻觉几何。这是神经场方法的共性局限——重建质量高度依赖多视角覆盖。

**运动速度与模糊。** 快速运动导致运动模糊和帧间大位移，使 MASt3R 特征匹配不可靠，运动解耦产生噪声。Table 3 的结果是在“所有基线均不失败”的 5 个序列上报告的，暗示在快速运动序列上所有方法（包括 RHINO）都可能失败。

**单人与单物体。** 当前框架假设场景中包含单个人和单个被操纵物体。扩展到多人交互（如两人共同搬运桌子）或多物体操纵（如双手分别操作不同工具）需要解决实例分割、多轨迹关联和交互约束分配等新问题。

### 开放问题与未来方向

1. **非刚性物体的扩展。** 如何将运动解耦和接触优化框架扩展到可变形或铰接物体？可能的路径包括：引入部件级规范空间、学习变形场先验、或利用类别级形状先验约束未见面的几何。

2. **时序先验与生成式形状先验。** 当前方法逐帧独立处理，未显式利用时序一致性先验。引入时序平滑约束或物理模拟器（如刚体动力学）可能改善快速运动和严重遮挡场景的鲁棒性。此外，利用在大规模 3D 数据集上预训练的生成式形状先验（如 3D 扩散模型）可能补全未观测到的物体表面。

3. **实时化与轻量化。** 当前管道包含 SfM、MASt3R 推理和多阶段神经场优化，计算开销较大。能否通过蒸馏、前馈网络或高效神经表示（如 3D Gaussian Splatting）实现近实时的 AR/VR 应用？这是一个工程挑战，但具有明确的应用牵引。

4. **多智能体交互。** 将框架从单人-单物扩展到多人-多物场景，需要解决实例级运动解耦、交互图推理和全局一致性约束等组合问题。这不仅是工程扩展，更涉及场景理解层面的方法创新。

5. **评估基准的完善。** BenchRHINO 是首个面向世界坐标系下人-物交互重建的基准，但其序列数量和物体多样性有限。更大规模、涵盖更多物体类别和交互类型的基准将推动该领域的标准化评估。

## 原文 PDF

![[paperPDFs/CVPR_2026/RHINO_Reconstructing_Human_Interactions_with_Novel_Objects_from_Monocular_Videos.pdf]]