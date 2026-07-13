---
title: "TROPHIES: Temporal Reconstruction of Places, Humans, and Cameras from Multi-view Videos"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TROPHIES_Temporal_Reconstruction_of_Places_Humans_and_Cameras_from_Multi_view_Videos.pdf
project_link: null
code_link: null
aliases:
- TROPHIES
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 全局对齐与接触感知优化模块，通过 Sim(3) 对齐、束调整和接触约束，将人体、场景、相机统一到同一个世界坐标系，强制尺度、接触和重力一致性。
primary_logic: 通过设计人感知注意力机制抑制动态区域、采用对称和锚点导向的跨视角注意力实现多视角一致的人体姿态估计，并通过全局优化将两者紧密结合，首次实现了从多视角视频中联合估计静态场景、动态人体和相机轨迹的统一框架。
claims:
- TROPHIES 在 EgoHuman 和 EgoExo4D 数据集上持续优于现有方法，在全局保真度和人-场景一致性上均有显著提升。
- 全局优化后，初期的人-场景错位、漂浮脚等问题得到解决，实现了物理上一致的接地重建。
- 人感知注意力模块在 DUSt3R、MonST3R、CUT3R 基础上均一致提升 TE、AE 和 RRA 指标。
- EgoHumans 上 W-MPJPE = 97.54 (TROPHIES+CUT3R)
---

# TROPHIES: Temporal Reconstruction of Places, Humans, and Cameras from Multi-view Videos

> [!tip] 核心洞察
> 通过设计人感知注意力机制抑制动态区域、采用对称和锚点导向的跨视角注意力实现多视角一致的人体姿态估计，并通过全局优化将两者紧密结合，首次实现了从多视角视频中联合估计静态场景、动态人体和相机轨迹的统一框架。

| 字段 | 内容 |
|------|------|
| 中文题名 | TROPHIES：从多视角视频中时序重建场景、人体与相机 |
| 英文题名 | TROPHIES: Temporal Reconstruction of Places, Humans, and Cameras from Multi-view Videos |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Liu_TROPHIES_Temporal_Reconstruction_of_Places_Humans_and_Cameras_from_Multi-view_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | TROPHIES |
| Dataset | EgoHumans, EgoExo4D |

> [!tip] 效果简介
> - EgoHumans 上，W-MPJPE 97.54 (TROPHIES+CUT3R) vs HSfM (降低超过 50%)；PA-MPJPE 38.8 (Human Branch All Views) vs Prior video methods (优于之前方法)；s-CCA@100 0.52 (CUT3R+human-aware attention) vs original CUT3R (提升)。
> - EgoExo4D 上，W-MPJPE 91.7 (TROPHIES+CUT3R) vs HSfM (同样降低超过 50%)。

## 概要

多视角视频中的人-场景联合重建面临一个根本性瓶颈：现有方法将人体、场景与相机解耦处理，导致三者之间尺度不一致、全局对齐差，无法实现物理上连贯的人-场景交互重建。**TROPHIES** 的核心洞察在于，通过设计人感知注意力机制抑制动态区域对场景重建的干扰，同时采用对称和锚点导向的跨视角注意力实现多视角一致的人体姿态估计，并将两者通过全局优化紧密结合，首次构建了从多视角视频中联合估计静态场景、动态人体和相机轨迹的统一框架。

方法层面，TROPHIES 由三个协同模块构成：**场景分支**利用人感知注意力滤除动态人体干扰，重建静态场景几何；**人体分支**通过对称与锚点参考的跨视角注意力，从同步多视角视频中估计时序一致的人体姿态；**全局对齐与优化模块**则通过 Sim(3) 对齐、束调整和接触约束，将人体、场景、相机统一到同一个世界坐标系，强制尺度、接触和重力一致性。这一设计使得 TROPHIES 能够即插即用地适配 DUSt3R、MonST3R 和 CUT3R 等多种场景重建骨干网络。

实验层面，TROPHIES 在 EgoHumans 和 EgoExo4D 两个数据集上持续优于现有范式：相比逐帧优化的 **HSfM**（Müller et al., arXiv 2024），W-MPJPE 降低超过 50%；定性结果表明，全局优化后初期的人-场景错位、漂浮脚等问题得到解决，实现了物理上一致的接地重建。消融实验进一步验证，人感知注意力在所有骨干网络上均一致提升轨迹误差（TE）、绝对误差（AE）和相对旋转精度（RRA）等指标，证明了模块设计的有效性与泛化性。

从多视角视频中同时重建动态人体、静态场景与相机轨迹，是通向物理世界 4D 理解的核心难题。这项任务要求系统不仅估计每一帧的人体姿态与场景几何，还必须将三者统一到**同一个世界坐标系**下，并保持**尺度一致性、接触合理性与时序稳定性**。然而，现有方法普遍将人体、场景与相机解耦处理，导致三大根本性缺口。

**缺口一：尺度断裂与全局不对齐。** 当前主流的人体重建方法——如单帧估计器 **HMR2**（Goel et al., ICCV 2023）、单目轨迹方法 **TRAM**（Wang et al., ECCV 2024）以及基于重力-视角坐标的 **GVHMR**（Shen et al., SIGGRAPH Asia 2024）——均在各自独立的坐标空间中输出结果。与此同时，场景重建方法如 **DUSt3R**（Wang et al., CVPR 2024）和 **CUT3R**（Wang et al., CVPR 2025）则产生另一套尺度与位姿。当这些输出被拼合时，人体漂浮、脚部悬空、穿透场景等物理上不可能的现象几乎不可避免。

**缺口二：动态人体对静态场景重建的污染。** 密集多视角场景重建模型依赖跨视角特征匹配来建立几何对应，但运动的人体会在时序上引入不一致的视觉模式，破坏静态区域的对应关系。现有方法缺乏机制来区分“应当匹配的静态结构”与“应当忽略的动态人体”，导致重建的场景点云在人体区域出现畸变和空洞。

**缺口三：多视角人体姿态估计缺乏有效的跨视角几何融合。** 单目视频方法仅利用时序信息，无法利用同一时刻多视角之间的几何约束。即使有多视角输入，先前工作也往往将其视为独立视图分别处理，再事后对齐，而非在特征层面进行对称的跨视角几何推理。这导致不同视角估计的人体姿态不一致，时序上出现抖动。

最新工作 **HSfM**（Müller et al., arXiv 2024）尝试逐帧联合重建人、场景与相机，但其每帧独立优化，尺度漂移随时间累积，当结果聚合时空间不一致性显著（见 Figure 5 定性对比）。**TROPHIES** 正是在这一背景下提出，其核心动机是：**设计一个统一框架，通过人感知注意力保护场景重建免受动态干扰，通过对称与锚点导向的跨视角注意力实现多视角一致的人体姿态估计，再通过全局 Sim(3) 对齐、束调整与接触约束将两者紧密耦合，首次实现从多视角视频中联合估计静态场景、动态人体和相机轨迹的物理连贯重建。**

## 核心方法与创新机理

TROPHIES 的核心创新并非孤立地改进单个模块，而是通过**三个关键设计槽位（changed slots）**将场景重建、人体姿态估计与相机轨迹估计耦合为一个统一的优化问题，从而解决了现有方法中三者解耦导致的尺度不一致与全局对齐失败这一根本瓶颈。

### 1. 人感知注意力：让场景重建“无视”动态人体

现有基于 DUSt3R、MonST3R、CUT3R 等框架的密集重建方法，在处理包含人体的动态场景时，会将运动的人体区域误认为场景几何的一部分，导致重建结果出现畸变与伪影。TROPHIES 在场景分支中引入**人感知注意力（Human-aware Attention）**，通过注意力掩码机制抑制人体区域的跨帧信息传递。

具体而言，对于 DUSt3R 和 MonST3R，该方法将注意力重加权为：

$$softmax^{ab}(\hat{\mathbf{A}}) = \begin{cases} 0 & \mathrm{if~} M_{\mathrm{human}}^{ab} \\ \mathrm{softmax}(A^{ab}) & \mathrm{otherwise} \end{cases}$$

其中 $M_{\mathrm{human}}^{ab}$ 为二值人体掩码。对于 CUT3R，则采用多记忆库解耦策略：一个记忆库在同一时刻的多视角间聚合人-场景特征以保持空间一致性，另一个记忆库跨时间存储静态场景特征以维持时序稳定性。这一设计使得场景分支能够“无视”动态人体，仅从静态区域学习几何信息。

消融实验（Table 4）证实，在 DUSt3R、MonST3R、CUT3R 三种骨干网络上引入人感知注意力后，TE、AE 和 RRA 指标均获得一致提升——例如 CUT3R 的 s-CCA@100 从基线提升至 0.52，表明重建的几何一致性与稳定性显著增强。

### 2. 对称与锚点参考的跨视角注意力：让多视角人体估计“相互确认”

传统视频人体姿态估计方法（如 HMR2、TRAM、GVHMR）主要依赖单视角时序特征，缺乏对多视角几何约束的显式建模。TROPHIES 的人体分支通过**两阶段跨视角注意力**机制，将同步多视角视频的几何信息深度融合：

- **第一阶段：对称跨视角注意力。**所有视角之间进行全连接的交叉注意力，交换全局几何信息，使各视角的人体特征相互“确认”。
- **第二阶段：锚点参考融合。**以某一视角为锚点，将其查询 $Q_{\mathrm{anchor}}$ 与其他参考视角的键 $K_{\mathrm{ref}}$ 和值 $V_{\mathrm{ref}}$ 进行交叉注意力融合：

$$F_{\mathrm{anchor}}^{\prime\prime} = \mathrm{softmax}\left(\frac{Q_{\mathrm{anchor}} K_{\mathrm{ref}}^T}{\sqrt{d}}\right) V_{\mathrm{ref}}$$

最终解码输出锚点视角的 SMPL 参数与接触概率。这一设计使得人体姿态估计能够利用多视角三角化的几何约束，在遮挡和深度歧义场景下仍保持时序稳定与空间一致。在 EgoHumans 数据集上，人体分支的 PA-MPJPE 达到 38.8 mm，优于此前的方法（Table 3）。

### 3. 全局对齐与接触感知优化：将人、场景、相机统一到一个世界

这是 TROPHIES 最关键的因果调节旋钮。场景分支与人体分支的输出天然处于不同的尺度空间，直接叠加会产生错位、漂浮脚和穿透等问题。TROPHIES 通过三级优化将两者统一：

1. **Sim(3) 对齐：**利用 ZoeDepth 估计的度量深度，通过相似变换将各静态相机视角的点云与场景分支对齐，统一初始尺度。
2. **联合束调整（Bundle Adjustment）：**构建包含场景点重投影误差 $\mathcal{L}_{\mathrm{Scene}}$ 和 SMPL 关节重投影误差 $\mathcal{L}_{\mathrm{Human}}$ 的全局损失：

$$\mathcal{L}_{\mathrm{BA}} = \frac{1}{N T} \sum_{n,t} \mathcal{L}_{\mathrm{Scene}} + \frac{1}{N T H} \sum_{n,t,h} \mathcal{L}_{\mathrm{Human}}$$

3. **接触感知约束：**引入接触损失 $\mathcal{L}_{\mathrm{contact}}$，鼓励人体接触顶点靠近场景表面，并惩罚地面以下的穿透。最终优化目标为：

$$\mathcal{L}_{\mathrm{opt}} = \mathcal{L}_{\mathrm{BA}} + \lambda_c \mathcal{L}_{\mathrm{contact}}$$

定性结果（Figure 5）直观展示了这一优化的效果：优化前的人体重建存在明显的场景错位和漂浮脚问题，优化后则实现了物理上一致的接地重建。定量上，TROPHIES 在 EgoHumans 上将 W-MPJPE 从 HSfM 的基线降低了超过 50%，达到 97.54 mm（Table 2），并在 EgoExo4D 上同样取得大幅领先。

### 创新总结

TROPHIES 的三个 changed slots 形成了闭环：人感知注意力为场景分支提供了“干净”的静态几何，对称跨视角注意力为人体分支提供了多视角一致的姿态估计，而全局对齐与接触优化则将两者在统一的物理世界坐标系中耦合，强制尺度、接触和重力一致性。这一设计范式首次实现了从多视角视频中联合输出静态场景、动态人体和相机轨迹的统一框架。

TROPHIES 的整体流程由三个核心组件构成：**场景分支（Scene Branch）**、**人体分支（Human Branch）** 以及 **全局对齐与优化（Alignment and Optimization）** 模块。给定时间同步的多视角视频流，系统首先并行运行场景分支与人体分支，分别估计静态场景几何与时序人体姿态，随后通过全局优化阶段将两者统一到同一个世界坐标系下，强制尺度、接触与重力一致性，最终输出物理上连贯的 4D 人-场景重建结果。

### 模块关系与数据流

**场景分支** 以多视角 RGB 帧为输入，通过人感知注意力机制（human-aware attention）抑制动态人体区域，重建静态场景几何。该分支以 DUSt3R、MonST3R 或 CUT3R 为骨干网络，人感知注意力以即插即用方式嵌入：对于 DUSt3R/MonST3R，采用基于二值人体掩码的注意力重加权（式 6），将人体区域对应的注意力权重置零；对于 CUT3R，则采用多记忆解耦策略，分别维护单时刻多视角特征记忆库和跨时间静态场景特征记忆库，从而在保持空间一致性的同时避免运动区域引入时序不一致。

**人体分支** 接收同步多视角视频帧，通过共享的 Human Video Transformer 进行时序建模，并采用两阶段跨视角注意力机制融合多视角几何信息：第一阶段在所有视角之间执行对称交叉注意力，交换全局几何信息；第二阶段以锚点视角（anchor view）为参考，通过锚点参考融合（式 7）将其他视角的特征聚合到锚点视角。融合后的特征经时序解码后送入双头预测器，分别输出 SMPL 参数和静态接触概率。推理时以锚点视角的 3D 关节作为最终输出，从而嵌入多视角一致性与接触感知。

**全局对齐与优化模块** 将场景分支与人体分支的输出耦合到统一世界坐标系。对于静态相机设置，首先使用 ZoeDepth 估计逐视角度量深度，通过 Sim(3) 对齐（式 8）将反投影深度与场景分支点云配准；随后执行全局束调整（式 9–11），联合优化场景点重投影误差和 SMPL 关节重投影误差。在此基础上，引入接触损失（式 12）鼓励人体接触顶点靠近场景表面并惩罚穿透，最终优化目标（式 13）结合束调整损失与接触约束，强制尺度、接触和重力一致性，消除初期重建中的人-场景错位、漂浮脚等问题（Figure 5）。

### 关键设计动机

现有方法（如 HSfM）将人体、场景与相机解耦处理，逐帧独立优化导致尺度漂移累积和空间不一致。TROPHIES 的核心洞察在于：通过场景分支的人感知注意力滤除动态干扰、人体分支的对称与锚点参考注意力实现多视角一致姿态估计，再通过全局优化将两者紧密耦合，首次实现了从多视角视频中联合估计静态场景、动态人体和相机轨迹的统一框架。

![[assets/figures/papers/paper_list_l25_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_TROPHIES_Temporal/figures/001_Figure_1.jpg]]
*Figure 1: Overview of TROPHIES. Given temporally synchronized video streams, TROPHIES jointly reconstructs dynamic humans, static scene geometry, and camera trajectories within a globally consistent 4D space. Our method couples a human branch and a scene branch through a global alignment and optimization stage that enforces scale, contact, and gravity consistency. This unified reconstruction produces temporally stable and spatially coherent human–scene representations, where human motions, scenes, and camera viewpoints are all aligned in a shared world coordinate frame*

![[assets/figures/papers/paper_list_l25_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_TROPHIES_Temporal/figures/003_Figure_2.jpg]]
*Figure 2: Pipeline Overview. Our framework consists of three components: a Scene Branch that reconstructs the static environment with human-aware attention (implemented as a plugand-play module applicable to DUSt3R, MonST3R, and CUT3R backbones); a Human Branch that estimates temporally coherent body parameters from multi-view videos via symmetric and anchor-referenced attention; and a global Align and Optimization stage that unifies humans, scenes, and cameras under consistent geometry and contact-aware constraints, producing a physically grounded reconstruction in a shared world coordinate system*

TROPHIES 由三个协同模块构成：**场景分支（Scene Branch）**、**人体分支（Human Branch）** 和 **全局对齐与优化（Alignment and Optimization）**。三者通过统一的 Sim(3) 尺度对齐、束调整和接触约束耦合，将静态场景、动态人体与相机轨迹统一到同一个世界坐标系中。

---

### 场景分支：人感知注意力

场景分支的核心创新是**人感知注意力（Human-aware Attention）**，用于抑制动态人体区域对静态场景重建的干扰。该模块以即插即用的方式作用于 DUSt3R、MonST3R 和 CUT3R 等骨干网络。

对于 DUSt3R 和 MonST3R，通过基于二值人体掩码的注意力重加权实现：

$$
\mathrm{softmax}^{ab}(\hat{\mathbf{A}}) = \begin{cases} 0 & \mathrm{if~} M_{\mathrm{human}}^{ab} \\ \mathrm{softmax}(A^{ab}) & \mathrm{otherwise} \end{cases}
$$

其中 $M_{\mathrm{human}}^{ab}$ 为人体掩码，当查询-键对落入人体区域时，将 softmax 输出置零，从而阻断动态人体特征的信息传递。对于 CUT3R，则采用多记忆解耦策略：一个记忆库在单时刻聚合多视角的人体与场景特征以保持空间一致性，另一个记忆库跨时间存储静态场景特征以维持时序稳定性。

---

### 人体分支：对称与锚点参考的跨视角注意力

人体分支从同步多视角视频中估计时序一致的人体姿态。其关键设计是两阶段跨视角特征融合：

1. **对称跨视角注意力**：所有视角之间进行全连接的注意力交互，交换全局几何信息。
2. **锚点参考融合**：将多视角特征聚合到指定锚点视角：

$$
F_{\mathrm{anchor}}^{\prime\prime} = \mathrm{softmax}\left(\frac{Q_{\mathrm{anchor}} K_{\mathrm{ref}}^T}{\sqrt{d}}\right) V_{\mathrm{ref}}
$$

其中 $Q_{\mathrm{anchor}}$ 来自锚点视角的查询，$K_{\mathrm{ref}}$、$V_{\mathrm{ref}}$ 来自参考视角的键和值，$d$ 为特征维度。融合后的特征经时序解码后输入双头预测器，分别输出 SMPL 参数和静态接触概率。

人体以 SMPL 模型参数化，在时间 $t$ 的人体 $h$ 表示为：

$$
H_{t}^{h} = \{ \phi_{t}^{h}, \theta_{t}^{h}, \beta^{h}, \gamma_{t}^{h} \}
$$

其中 $\phi_{t}^{h}$ 为全局朝向，$\theta_{t}^{h}$ 为关节旋转，$\beta^{h}$ 为体型系数，$\gamma_{t}^{h}$ 为全局平移。

---

### 全局对齐与优化

该模块将场景分支与人体分支统一到一致的世界坐标系中，消除尺度不一致和空间错位。

**Sim(3) 对齐**：对每个静态相机视角，通过最小化反投影深度与场景分支点云的距离，估计相似变换 $S_i \in \mathrm{Sim}(3)$：

$$
S_i = \arg\min_{S \in \mathrm{Sim}(3)} \sum_{\mathbf{x} \in \Omega_i} \left\| S \cdot K^{-1}[\mathbf{x}, D_i(\mathbf{x})] - \mathbf{P}_i(\mathbf{x}) \right\|_2^2
$$

其中 $K^{-1}[\mathbf{x}, D_i(\mathbf{x})]$ 为像素 $\mathbf{x}$ 反投影到相机坐标系的三维点，$\mathbf{P}_i(\mathbf{x})$ 为场景分支输出的对应世界坐标点。

**束调整损失**：联合优化场景点与人体关节的重投影误差：

$$
\mathcal{L}_{\mathrm{BA}} = \frac{1}{N T} \sum_{n,t} \mathcal{L}_{\mathrm{Scene}} + \frac{1}{N T H} \sum_{n,t,h} \mathcal{L}_{\mathrm{Human}}
$$

其中场景重投影损失和人体重投影损失分别为：

$$
\mathcal{L}_{\mathrm{Scene}} = \left\| K^{(n,t)} [\mathbf{R}^{(n,t)}, \mathbf{T}^{(n,t)}] \mathbf{P}_{\mathrm{scene}} - \mathbf{x}_{\mathrm{scene}}^{(n,t)} \right\|_2^2
$$

$$
\mathcal{L}_{\mathrm{Human}} = \left\| K^{(n,t)} [\mathbf{R}^{(n,t)}, \mathbf{T}^{(n,t)}] \mathrm{SMPL}(H^{(n,t,h)}) - \mathbf{J}_{2D}^{(n,t,h)} \right\|_2^2
$$

**接触损失**：强制人体与场景的物理接触一致性，惩罚穿透和悬空：

$$
\mathcal{L}_{\mathrm{contact}} = \sum_{\mathbf{v} \in \mathcal{C}} \big( \boldsymbol{w}_c \cdot \mathrm{dist}(\mathbf{v}, S_{\mathrm{surface}})^2 + \boldsymbol{w}_p \cdot \max(0, -\mathrm{n}_{\mathcal{S}}^\top (\mathbf{v} - \mathbf{p}_{\mathcal{S}}))^2 \big)
$$

第一项鼓励接触顶点 $\mathbf{v}$ 靠近场景表面 $S_{\mathrm{surface}}$，第二项惩罚穿透地面平面（当顶点位于表面法向 $\mathrm{n}_{\mathcal{S}}$ 的负侧时激活）。

**最终优化目标**：

$$
\mathcal{L}_{\mathrm{opt}} = \mathcal{L}_{\mathrm{BA}} + \lambda_c \mathcal{L}_{\mathrm{contact}}
$$

其中 $\lambda_c$ 为接触损失权重。该目标联合优化相机外参、场景点云和 SMPL 参数，使人体与场景在尺度、接触和重力方向上达成一致。消融实验证实，重力感知项通过稳定垂直运动并抑制漂移，进一步增强了物理合理性。

## 实验与关键发现

### 1. 实验设置

TROPHIES 在两个多视角人体-场景交互数据集上进行评估：**EgoHumans** 和 **EgoExo4D**。前者包含密集的多视角视频，后者覆盖更广泛的日常活动场景。评测指标分为两大类：人体重建精度（W-MPJPE、PA-MPJPE、Accel）和场景-相机一致性（RRA、CCA、s-CCA、TE、AE）。基线方法涵盖单帧人体姿态估计 **HMR2**（Goel et al., ICCV 2023）、单目全局轨迹方法 **TRAM**（Wang et al., ECCV 2024）与 **GVHMR**（Shen et al., SIGGRAPH Asia 2024）、逐帧人-场景-相机重建方法 **HSfM**（Müller et al., arXiv 2024），以及场景重建骨干网络 **DUSt3R**（Wang et al., CVPR 2024）和 **CUT3R**（Wang et al., CVPR 2025）。

### 2. 主实验结果

表 2 汇总了 TROPHIES 在 EgoHumans 和 EgoExo4D 上的核心指标。以 CUT3R 为骨干时，TROPHIES 在 EgoHumans 上达到 W-MPJPE 97.54、PA-MPJPE 20.71、Accel 14.23；在 EgoExo4D 上达到 W-MPJPE 91.7、PA-MPJPE 16.92、Accel 16.72。与 HSfM 相比，W-MPJPE 降低超过 50%，表明全局对齐与接触感知优化有效抑制了逐帧独立估计带来的尺度漂移和空间不一致。

在人类分支的独立评估（表 3）中，TROPHIES 在“All Views”设定下达到 PA-MPJPE 38.8，优于此前所有视频类人体重建方法。这验证了对称跨视角注意力和锚点参考融合机制在融合多视角几何信息方面的有效性——多视角特征通过交叉注意力汇聚到锚点视角，使最终输出的 3D 关节天然嵌入了多视角一致性。

场景-相机一致性方面，引入人感知注意力后，CUT3R 骨干的 s-CCA@100 提升至 0.52，TE 降至 1.83（表 4）。这表明通过注意力掩码抑制动态人体区域，场景分支能够更稳定地重建静态几何，避免运动人体对跨帧特征匹配的干扰。

### 3. 消融实验

**人感知注意力机制**（表 4）在 DUSt3R、MonST3R、CUT3R 三个骨干网络上均一致提升 TE、AE 和 RRA 指标。其核心机制是：同一时刻内所有视角的 patch 自由交换信息以保证多视角一致性，而跨时刻仅允许非人体 patch 参与注意力计算——人体区域被显式掩码，从而切断运动伪影对场景重建的污染。对于 CUT3R 骨干，该机制通过多记忆库解耦实现：一个记忆库聚合单时刻多视角的人-场景特征，另一个存储跨时间的静态场景特征。

**对称与锚点参考的跨视角注意力**（人类分支消融）有效融合了同步多视角的几何线索。对称注意力在所有视角间交换全局信息，锚点参考融合则将特征汇聚到目标视角，使人体姿态估计精度显著提升。

**接触感知优化**的消融体现在定性结果中（图 5）：优化前，人体与场景之间存在明显错位、穿透和漂浮脚现象；引入接触损失 $ \mathcal{L}_{\mathrm{contact}} $ 后，这些伪影被消除，人体脚部与地面正确接触。重力感知项进一步稳定了垂直方向的运动估计，抑制了长时间序列中的漂移。

### 4. 定性分析

图 5 展示了全局优化前后的对比以及 TROPHIES 与 HSfM 的差异。场景 1-2 中，优化前的重建存在人-场景错位和穿透（红色框标注），优化后实现了物理一致的接地重建。场景 3 中，HSfM 因逐帧独立优化导致尺度漂移累积，人体运动在时序上出现明显的空间不一致；TROPHIES 则通过全局 Sim(3) 对齐和束调整，在整个序列上保持一致的全局尺度，产生稳定连贯的人体运动轨迹。

### 5. 失败模式与局限

当前分析材料未提供明确的失败案例或局限性讨论。从方法设计推断，潜在瓶颈可能包括：极度拥挤场景下人体掩码不准确导致场景分支残留运动伪影；接触损失依赖场景表面重建质量，在稀疏视角或纹理缺失区域可能失效；全局优化假设静态场景，对动态背景（如移动家具）的适应性需要进一步验证。以上推断需人工核实原文。

![[assets/figures/papers/paper_list_l25_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_TROPHIES_Temporal/figures/002_Table_1.jpg]]
*Table 1: Comparison of methods across different features*

![[assets/figures/papers/paper_list_l25_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_TROPHIES_Temporal/figures/007_Table_2.jpg]]
*Table 2: Elevation of TROPHIES on the EgoHumans [26] and EgoExo4D [11] datasets. Across all backbones and datasets, TROPHIES consistently improves human accuracy (lower W-MPJPE, PA-MPJPE, Accel) and enhances scene–camera coherence (higher RRA, CCA, s-CCA), outperforming the original baselines by a large margin. These results demonstrate the generalization of our framework across architectures and domains, yielding globally aligned and physically coherent human–scene reconstructions*

![[assets/figures/papers/paper_list_l25_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_TROPHIES_Temporal/figures/009_Table_4.jpg]]
*Table 4: Ablation Study on the human-aware attention. Across all backbones [57, 58, 65], introducing human-aware attention to the scene branch consistently improves TE, AE and RRA, indicating more stable and geometrically consistent reconstruction*

![[assets/figures/papers/paper_list_l25_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_TROPHIES_Temporal/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative results. Comparison of multi-view reconstructions before and after global optimization (Scenes 1–2) and against prior work (Scene 3). For Scenes 1 and 2, the initial results (a,c) exhibit misalignment between humans and scenes, leading to interpenetration, floating feet, and incorrect grounding (red boxes). Our global optimization (b,d) lead to physically coherent and well-grounded reconstructions. Scene 3 compares HSfM (e) with our TROPHIES framework (f). Since HSfM performs frame-wise independent optimization, its per-frame scale drifts accumulate over time, causing noticeable spatial inconsistencies when the results are aggregated. In contrast, our TROPHIES maintains a global...*

## 定位与知识库关联

### 问题定位：从解耦重建到统一 4D 空间

现有方法在处理多视角视频中的人-场景-相机重建时，普遍采用**解耦策略**：将人体姿态估计、场景重建和相机定位作为独立任务分别处理。这种解耦导致了三个层面的根本性问题：

1. **尺度不一致**：人体分支和场景分支各自估计的尺度因子无法对齐，使得人体在场景中的大小、位置缺乏物理意义。
2. **全局对齐缺失**：逐帧独立优化（如 **HSfM** (Müller et al., arXiv 2024)）导致帧间尺度漂移累积，长序列中人体运动出现空间不一致。
3. **接触约束缺失**：缺乏对人-场景交互的显式建模，导致漂浮脚、穿透地面等物理不合理现象。

TROPHIES 的核心突破在于：通过**全局对齐与接触感知优化模块**，将人体、场景、相机统一到同一个世界坐标系，强制实现尺度、接触和重力的一致性。这一设计将原本解耦的流水线改造为端到端可优化的耦合系统。

### 方法谱系：与基线工作的关系

#### 场景重建分支的继承与改造

TROPHIES 的场景分支建立在三类密集重建骨干网络之上：

- **DUSt3R** (Wang et al., CVPR 2024)：提供密集多视角立体匹配与点云重建能力。
- **MonST3R**：扩展 DUSt3R 至单目时序场景重建。
- **CUT3R** (Wang et al., CVPR 2025)：引入连续 3D 感知，增强时序一致性。

TROPHIES 的关键改造在于引入**人感知注意力机制**（Human-aware Attention）。原有骨干网络的标准跨视角注意力不加区分地处理所有图像区域，导致动态人体区域的运动信息污染静态场景重建。人感知注意力通过二值人体掩码对注意力权重进行重加权（DUSt3R/MonST3R）或多记忆库解耦（CUT3R），在跨时间步的注意力计算中屏蔽人体区域，仅保留非人体区域的信息交换。这一设计使得场景重建在存在动态人体的情况下仍能保持几何一致性。

#### 人体姿态估计分支的继承与改造

人体分支的基线方法包括：

- **HMR2** (Goel et al., ICCV 2023)：单帧人体姿态估计，缺乏时序和多视角约束。
- **TRAM** (Wang et al., ECCV 2024)：单目全局轨迹与运动估计，但未利用多视角几何。
- **GVHMR** (Shen et al., SIGGRAPH Asia 2024)：基于重力-视角坐标的地面人体运动恢复，引入了重力先验但仅限于单目输入。

TROPHIES 的人体分支从两个维度突破上述方法的局限：

1. **对称跨视角注意力**：在同步多视角帧之间进行全连接的跨视角注意力，使所有视角共享全局几何信息，实现多视角一致的人体姿态估计。
2. **锚点参考的特征融合**：以锚点视角的查询向量聚合参考视角的特征，将多视角几何线索浓缩到统一表示中，再通过时序解码器输出 SMPL 参数。

#### 全局优化模块的独特贡献

与 **HSfM** 的逐帧独立优化形成鲜明对比，TROPHIES 的全局优化模块包含三个层次：

- **Sim(3) 对齐**（Eq. 8）：通过最小化反投影深度与场景分支点云之间的距离，估计每个视图的相似变换，将人体分支的局部坐标注册到场景分支的世界坐标。
- **联合束调整**（Eq. 9–11）：同时最小化场景点和人体 SMPL 关节的重投影误差，在统一优化中精化相机参数、场景结构和人体姿态。
- **接触感知约束**（Eq. 12–13）：鼓励接触顶点靠近场景表面，同时惩罚地面以下的穿透，确保物理上合理的接地重建。

### 适用边界与局限

#### 技术依赖与假设

1. **同步多视角输入**：TROPHIES 假设所有相机帧严格时间同步，这一假设在 EgoHumans 和 EgoExo4D 数据集中得到满足，但在非受控采集场景中可能难以保证。
2. **静态场景假设**：场景分支的人感知注意力机制假设非人体区域是静态的。对于包含其他动态物体（如移动的家具、动物）的场景，该机制可能失效，需要进一步验证。
3. **深度估计依赖**：静态相机设置下依赖 ZoeDepth 估计度量深度，其精度直接影响 Sim(3) 对齐质量。在纹理稀疏或光照极端的场景中，深度估计误差可能传播到全局优化。

#### 计算与数据需求

TROPHIES 的全局优化涉及多帧、多视角的联合束调整，计算复杂度随帧数、视角数和人体数量线性增长。对于长序列或多人体场景，优化过程的收敛性和计算开销需要进一步评估。论文未报告推理时间或显存占用的具体数据，实际部署的可行性需要手动验证。

#### 未探索的场景

- **单目或稀疏视角**：TROPHIES 的人体分支依赖多视角几何信息进行对称注意力融合，在单目或仅有两个视角的输入下，跨视角注意力的增益可能大幅衰减。
- **快速运动与遮挡**：当人体运动速度极快或发生严重遮挡时，人体掩码的准确性下降，可能同时影响场景分支的掩码重加权和人体分支的特征提取。
- **人与物体交互**：当前接触约束仅针对场景表面，未建模人体与可移动物体（如椅子、工具）的交互，这类场景的物理合理性仍依赖隐式学习。

### 开放问题

1. **动态场景扩展**：人感知注意力能否泛化到多动态物体的场景？是否需要实例级掩码来区分不同运动模式？
2. **实时性优化**：全局束调整的实时化是否可能？能否通过关键帧选择或分层优化策略降低计算开销？
3. **弱监督与自监督**：接触约束当前依赖场景表面重建质量，能否通过物理模拟或自监督信号增强接触感知的鲁棒性？
4. **跨域泛化**：TROPHIES 在 EgoHumans（室内多人体）和 EgoExo4D（自我-外部视角）上的表现是否可迁移至室外大规模场景或穿戴式相机场景？

## 原文 PDF

![[paperPDFs/CVPR_2026/TROPHIES_Temporal_Reconstruction_of_Places_Humans_and_Cameras_from_Multi_view_Videos.pdf]]
