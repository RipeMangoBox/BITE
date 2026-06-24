---
title: "Towards Physically Executable 3D Gaussian for Embodied Navigation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Towards_Physically_Executable_3D_Gaussian_for_Embodied_Navigation.pdf
openreview_forum_id: HB6KvsqcAn
aliases:
- S3SPAGE3N
- TPE3GEN
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "在3DGS中注入两个关键能力：(1) 对象级语义接地——通过人工标注添加对象类别、实例ID等信息，生成2D语义地图；(2) 物理感知执行联合——从艺术家创建的网格中提取碰撞体，构建3DGS-网格混合表示，使3DGS在保持照片级渲染的同时具备语义理解与物理交互能力。"
primary_logic: "将高保真渲染（3DGS）与物理仿真（基于网格的碰撞体）解耦，能够创建既具有照片真实感又可物理执行的具身导航环境，从而显著提升VLN模型的泛化性能。"
claims:
- "SAGE-3D将3DGS升级为可执行的、语义和物理对齐的环境"
- "Object-Centric Semantic Grounding为3DGS添加对象级细粒度标注"
- "Physics-Aware Execution Jointing嵌入碰撞对象并构建丰富的物理接口"
- "3DGS-网格混合表示将渲染与物理模拟解耦"
---

# Towards Physically Executable 3D Gaussian for Embodied Navigation

> [!tip] 核心洞察
> 将高保真渲染（3DGS）与物理仿真（基于网格的碰撞体）解耦，能够创建既具有照片真实感又可物理执行的具身导航环境，从而显著提升VLN模型的泛化性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向具身导航的物理可执行3D高斯 |
| 英文题名 | Towards Physically Executable 3D Gaussian for Embodied Navigation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=HB6KvsqcAn); [Project](https://sage-3d.github.io); [Project](https://anonymous.4open.science/r/SAGE-3D-8764) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SAGE-3D (Semantically and Physically Aligned Gaussian Environments for 3D Navigation) |
| Dataset | SAGE-Bench VLN (高级指令), VLN-CE R2R Val-Unseen, 环境渲染速度 (每帧耗时) |

> [!tip] 效果简介
> - SAGE-Bench VLN (高级指令) 上，SR ↑ 为 0.46 (NaVILA-SAGE)，对比 0.21 (NaVILA-base)，变化 +0.25。
> - SAGE-Bench VLN (高级指令) 上，OSR ↑ 为 0.55 (NaVILA-SAGE)，对比 0.26 (NaVILA-base)，变化 +0.29。
> - VLN-CE R2R Val-Unseen 上，SR ↑ 为 0.38 (NaVILA-SAGE)，对比 0.29 (NaVILA-base)，变化 +0.09 (+31%)。

## 概述

### 问题瓶颈

现有3D高斯泼溅（3DGS）虽能提供照片级渲染，但本质上仅包含颜色与密度信息，缺乏对象级语义标注和物理碰撞几何，无法直接作为视觉语言导航（VLN）的环境基础。这导致智能体难以理解“走到沙发左侧的茶几旁”这类细粒度指令，也无法进行安全的物理交互——3DGS场景默认可穿透，碰撞检测完全失效。

### 核心洞察

本工作提出一个关键解耦思路：**将高保真渲染与物理仿真分离**。3DGS负责外观呈现，基于网格的碰撞体负责物理交互，二者通过3DGS-网格混合表示协同工作。这一设计在不牺牲渲染质量的前提下，赋予3DGS环境可执行性。

### 方法定位

**SAGE-3D**（Semantically and Physically Aligned Gaussian Environments for 3D Navigation）通过两个组件实现上述目标：

- **对象级语义接地**：对3DGS场景进行人工对象级标注（类别、实例ID、包围盒），生成2D语义俯视地图，为路径规划和指令生成提供语义基础。
- **物理感知执行联合**：从美术师创建的原始网格中通过CoACD凸分解提取碰撞体，构建3DGS-网格混合表示，并暴露机器人控制、碰撞检测等物理接口。

由此构建的**InteriorGS**数据集包含1,000个高保真3DGS场景及554k+对象实例标注，**SAGE-Bench**则成为首个基于3DGS的VLN基准，提供2M轨迹-指令对及对应的碰撞体。

### 主要结果

| 基准 | 指标 | 基线 | SAGE-3D | 提升 |
|------|------|------|---------|------|
| SAGE-Bench VLN | SR ↑ | 0.21 (NaVILA-base) | 0.46 (NaVILA-SAGE) | +0.25 |
| SAGE-Bench VLN | OSR ↑ | 0.26 (NaVILA-base) | 0.55 (NaVILA-SAGE) | +0.29 |
| VLN-CE R2R Val-Unseen | SR ↑ | 0.29 (NaVILA-base) | 0.38 (NaVILA-SAGE) | +31% |

在环境效率方面，3DGS-网格混合表示相比传统扫描网格渲染速度提升约2.7倍（6.2ms vs 16.7ms/帧），显存占用降低约3.9倍（220MB vs 850MB）。需注意，3DGS数据训练的收敛速度较慢，达到40%成功率需160k次迭代（6.2小时），而扫描网格仅需120k次（4.8小时）。

### 局限与开放问题

当前方法依赖美术师创建的原始网格进行碰撞体提取，对扫描重建的真实场景需额外后处理。物理仿真能力尚未在动态物体、移动障碍物或完全非结构化环境（野外、水下）中验证。此外，所提连续性指标（CSR/ICP/PS）在导航成功率极低的模型上缺乏区分度。如何将语义-物理对齐范式推广至NeRF等其他隐式表示，以及如何实现从虚拟3DGS环境到真实世界的策略迁移，仍有待探索。

## 背景与动机

### 具身导航的环境基础瓶颈

视觉语言导航（VLN）要求智能体在三维环境中理解自然语言指令并执行连续动作。当前主流的VLN基准——如VLN-CE、RxR——普遍依赖Matterport3D等扫描重建网格作为环境基础。这些网格虽然提供了碰撞几何，却存在两个结构性缺陷：其一，扫描网格是真实场景的不完美估计，包含孔洞、噪声和重建伪影，导致物理仿真与视觉渲染的质量均受限制；其二，扫描网格缺乏对象级语义标注，智能体无法区分“椅子”与“桌子”的实例边界，难以执行“绕过沙发后左转进入厨房”这类细粒度指令。

### 3DGS的潜力与缺口

3D高斯泼溅（3D Gaussian Splatting, 3DGS）作为新兴的显式神经表示，以照片级渲染质量和毫秒级帧率在场景重建领域展现出显著优势。然而，**原生3DGS仅编码颜色与密度信息**，不包含对象类别、实例ID或属性标签，亦缺乏可靠的碰撞几何——高斯原语本质上是可穿透的半透明椭球体。这使得3DGS无法直接充当VLN的环境基础：智能体既无法从渲染观测中提取对象级语义以理解精细指令，也无法依赖其进行物理碰撞检测以安全导航。这一“高保真渲染”与“物理可执行性”之间的断裂，构成了3DGS走向具身智能的关键瓶颈。

### 现有方法的缺口

当前VLN领域存在一个明显的范式错配：**环境表示的物理真实性与语义丰富性不可兼得**。扫描网格提供物理约束但渲染质量差、语义缺失；3DGS提供照片级外观但无物理、无语义。部分工作尝试在3DGS上添加语义特征（如通过CLIP嵌入或语义场），但这些方法停留在像素级或场景级，未触及对象级实例分割与物理接口构建。另一类工作则通过仿真引擎（如Habitat、AI2-THOR）提供物理交互，但其视觉渲染与真实世界存在显著域差距。**将高保真渲染与物理仿真解耦，并在同一环境中统一语义接地与物理执行，是该领域尚未被系统探索的方向。**

### 本文动机

针对上述缺口，本文提出**SAGE-3D（Semantically and Physically Aligned Gaussian Environments for 3D Navigation）**，其核心动机在于：通过为3DGS注入对象级语义标注与物理碰撞结构，将其从纯粹的视觉表示升级为**语义-物理对齐的可执行环境**。这一升级使得智能体能够：(1) 在照片级渲染的观测中理解对象级指令；(2) 在物理约束下执行连续导航动作；(3) 利用3DGS的高渲染效率与低显存占用，支持大规模训练。最终目标是验证：**在完全由3DGS构建的环境中训练出的VLN策略，能否在真实世界扫描场景（VLN-CE）上展现出更强的泛化能力。**

## 核心创新

### 问题瓶颈：3DGS为何无法直接支撑具身导航

3D Gaussian Splatting（3DGS）虽能以照片级真实感实时渲染场景，但其原生表示存在两个根本性缺陷，使其无法作为视觉语言导航（VLN）的环境基础：

1. **语义缺失**：传统3DGS仅存储颜色与密度信息，缺乏对象类别、实例ID等细粒度语义标注。智能体虽能“看见”场景，却无法“理解”指令中指向的具体对象。
2. **物理缺失**：3DGS不具备碰撞几何，高斯原语之间可被任意穿透。这导致智能体无法进行物理仿真，难以产生安全、平滑的导航轨迹。

这两个缺陷共同构成了一个因果瓶颈：**没有对象级语义接地，智能体无法解析精细指令；没有物理执行接口，导航行为无法被约束和评估。** 现有VLN基准（如VLN-CE）依赖扫描网格提供碰撞体，但扫描网格本身存在几何失真且缺乏照片级外观，难以同时满足渲染保真度与物理仿真的双重需求。

### 核心洞察：渲染与物理的解耦

SAGE-3D的核心洞察在于**将高保真渲染与物理仿真解耦**。具体而言，3DGS负责提供照片级外观渲染，而通过艺术家创建的精确网格提取碰撞体来承担物理仿真职责。这种“3DGS-网格混合表示”既保留了3DGS的视觉优势，又弥补了其物理交互能力的缺失，从而构建出既具有照片真实感又可物理执行的具身导航环境。

### 方法谱系与知识库定位

SAGE-3D并非提出新的VLN策略模型，而是**重新定义了VLN的环境基础**。在现有方法谱系中：

- **传统VLN环境**（如**VLN-CE**基于Matterport3D扫描网格，Krantz et al., 2020）提供物理碰撞但渲染质量低、几何存在失真。
- **纯3DGS环境**提供照片级渲染但无语义、无物理，仅能用于视觉观测。
- **SAGE-3D**在两者之间架起桥梁：通过注入语义标注层和物理交互层，将3DGS升级为可执行的具身环境。

这一范式与NeRF-based环境（如**NeRF-Navigation**）共享“隐式表示+物理接口”的思路，但SAGE-3D的3DGS-Mesh Hybrid在渲染效率上具有显著优势（每帧6.2ms vs. 扫描网格16.7ms），且在显存占用上更为经济（220MB vs. 850MB）。

### Changed Slots：相对于基线的关键变更

SAGE-3D相对于传统3DGS环境引入了三个核心变更槽位：

| 槽位 | 基线值（传统3DGS） | 提出值（SAGE-3D） | 证据锚点 |
|------|-------------------|-------------------|----------|
| **语义标注层** | 无对象级语义，仅颜色/密度 | 人工标注的对象类别、实例ID与包围盒信息 | “Object-Centric Semantic Grounding, which adds object-level fine-grained annotations to 3DGS” |
| **物理交互层** | 无物理约束，可穿透 | 通过CoACD凸分解提取碰撞体，构建3DGS-网格混合表示，提供物理仿真接口 | “Physics-Aware Execution Jointing, which embeds collision objects into 3DGS and constructs rich physical interfaces.” |
| **环境表示形式** | 纯3DGS外观表示 | 3DGS负责照片级渲染，网格碰撞体负责物理仿真（3DGS-Mesh Hybrid） | “we extract collision bodies ... while using 3DGS to provide photorealistic appearance.” |

这三个槽位的变更并非孤立进行，而是通过**对象级语义接地**和**物理感知执行联合**两条管线协同实现：

1. **对象级语义接地**：首先在3DGS场景上进行人工对象级标注（类别、实例ID、包围盒），构建InteriorGS数据集（1,000个高保真场景，超过554k对象实例）。随后将标注的3D对象投影到二维俯视语义地图，用于路径规划和分层指令生成。

2. **物理感知执行联合**：从艺术家创建的三角网格出发，应用CoACD算法进行凸分解，为每个对象提取碰撞体。这些碰撞体与3DGS渲染层共同构成3DGS-Mesh Hybrid表示，并暴露机器人控制、碰撞检测等物理接口。

### 决定性证据与效果

SAGE-3D的有效性通过以下关键实验得到验证：

- **泛化性能**：仅用SAGE-Bench的3DGS数据训练的NaVILA-SAGE模型，在未见过的VLN-CE R2R Val-Unseen环境中将成功率（SR）从基线的0.29提升至0.38，相对提升31%。这证明3DGS环境训练的策略具有良好的跨环境泛化能力。
- **渲染效率**：3DGS-Mesh Hybrid的平均每帧渲染时间为6.2ms，显著优于扫描网格的16.7ms；显存占用仅220MB，远低于扫描网格的850MB。
- **物理仿真能力**：新设计的连续性指标（CSR、ICP、PS）能够揭示传统指标（SR、SPL）无法捕获的导航自然性问题——例如NaVILA模型虽达到0.39 SR，但其碰撞惩罚高达0.61，路径平滑度仅0.68。

### 局限与开放问题

尽管SAGE-3D在语义-物理对齐方面取得了显著进展，仍存在若干局限：

- **训练收敛速度**：3DGS场景数据训练收敛明显慢于扫描网格数据（达到40% SR需160k次迭代/6.2小时 vs. 120k次/4.8小时），可能影响大规模训练效率。
- **物理仿真依赖**：碰撞体提取依赖美术师创建的原始网格，对于通过扫描重建的真实场景，需要额外的近似或后处理步骤。
- **连续性指标的适用边界**：CSR/ICP/PS在模型导航成功率极低（SR<0.20）时缺乏区分度，限制了其对弱模型的诊断能力。
- **场景覆盖范围**：数据集目前主要覆盖室内及有限类别的户外场景，对于完全非结构化环境（如野外、水下）的物理接口和指令设计尚未验证。

这些局限指向若干开放问题：如何通过课程学习或数据增强加速3DGS环境下的训练收敛？在动态物体场景下能否实时更新3DGS并维持物理仿真的实时性？该语义-物理对齐范式是否可以推广到NeRF等其他隐式表示，形成更通用的具身环境框架？

## 整体框架

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_HB6KvsqcAn/figures/003_Figure_2.jpg]]
*Figure 2: Overview of SAGE-3D, which consists of two key components: (1) Object-Level Semantic Grounding, 3DGS data is annotated by expect at the object level, then be transformed into 2D semantic maps for path planning and instruction generation; (2) Physics-Aware Execution Jointing, where scene and object collision bodies are generated via convex hull decomposition, integrated into 3DGS to form a 3DGS-Mesh Hybrid Representation, with extensive physics simulation interfaces*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_HB6KvsqcAn/figures/001_Figure_1.jpg]]
*Figure 1: Traditional 3DGS vs. Our work. Compared with traditional 3DGS, our InteriorGS provides object-level 3DGS annotations across diverse indoor and outdoor scenes, including furnished homes, gyms, and concert halls as well as swimming pools and amusement parks. Meanwhile, SAGE-Bench contains semantically rich VLN data and detailed physical interfaces, representing a semantically and physically aligned 3DGS paradigm. Specifically, InteriorGS comprises 1,000 annotated 3DGS scenes with over 554k object instances, and SAGE-Bench, the first 3DGS-based VLN benchmark, features 2M trajectory-instruction pairs alongside a matching number of detailed collision bodies, laying a foundation for generalizable...*

SAGE-3D 的核心目标是将传统 3D Gaussian Splatting（3DGS）从纯外观表示升级为**语义与物理对齐的可执行具身导航环境**。其整体架构由两条并行且最终融合的技术管线构成，如 Figure 2 所示。

### 形式化定义

系统将可执行环境形式化为一个语义-物理增强的部分可观测马尔可夫决策过程（POMDP）：

$$
\mathcal{E} = (\mathcal{U}, \mathcal{S}, \mathcal{A}, \mathcal{O}, T, Z; M, \Phi)
$$

其中 $\mathcal{U}$ 为指令空间，$\mathcal{S}$ 为状态空间，$\mathcal{A}$ 为动作空间，$\mathcal{O}$ 为观测空间，$T$ 为状态转移函数，$Z$ 为渲染函数。关键增强在于注入语义层 $M$ 和物理层 $\Phi$，使环境从纯视觉表示转变为可理解指令、可物理交互的执行基础。整个转换过程可概括为：

$$
G \; + \; M \; + \; \Phi \; \longrightarrow \; \mathcal{E}_{\mathrm{exec}}
$$

即将高斯原语 $G$ 与语义 $M$ 和物理 $\Phi$ 结合，输出可执行导航环境。

### 管线一：对象级语义接地（Object-Level Semantic Grounding）

该管线解决 3DGS 缺乏细粒度语义的根本瓶颈。流程如下：

1. **人工标注**：在 3DGS 场景中对每个对象标注类别、实例 ID 和包围盒信息，构建 InteriorGS 数据集（1,000 个高保真 3DGS 场景，覆盖超 554k 对象实例，涵盖住宅、健身房、音乐厅、泳池、游乐园等多类室内外环境）。
2. **2D 语义俯视图生成**：将标注后的 3D 对象投影到地平面，通过采样对象表面点、计算凸包并融合多视图掩码，生成每对象的 2D 语义掩码：

   $$
   \mathcal{M}_k = \operatorname{Fuse}\left( \operatorname{Hull}\left\{ \Pi_{\mathrm{top}}(p) \mid p \in \operatorname{Surf}(o_k) \right\} \right)
   $$

3. **路径规划与指令生成**：在融合的占据-语义地图上运行基于 A* 的最短路径搜索生成轨迹，再利用 MLLM 结合对象类别、属性和空间关系生成具有因果依赖关系的高级指令，同时生成用于底层控制评估的低级指令。

### 管线二：物理感知执行联合（Physics-Aware Execution Jointing）

该管线解决 3DGS 无碰撞几何、智能体可穿透场景的问题。流程如下：

1. **碰撞体提取**：从美术师创建的原始三角网格出发，应用 CoACD 凸分解算法，为每个对象提取凸碰撞体。
2. **3DGS-网格混合表示**：将碰撞网格嵌入 3DGS 场景，形成混合表示——3DGS 负责照片级真实感渲染，网格碰撞体负责物理仿真。这一解耦设计是核心洞察：渲染与物理分离，使环境同时具备高保真外观和可执行性。
3. **物理接口暴露**：构建丰富的物理仿真接口，包括机器人控制、碰撞检测、刚体动力学等，使智能体能够在环境中进行物理交互。

### 管线汇聚：SAGE-Bench 基准

两条管线的输出汇聚为 SAGE-Bench——首个基于 3DGS 的 VLN 基准。其构成包括：

- **分层指令**：高级语义指令（含因果依赖）与低级动作原语指令，共约 2M 轨迹-指令对。
- **两大任务类型**：视觉语言导航（VLN）与视觉探索（Visual Exploration）。
- **两级复杂度**：根据轨迹长度和指令复杂度划分简单与困难样本。
- **三维连续性指标**：除传统 SR/OSR 外，新增连续成功率（CSR）、综合碰撞惩罚（ICP）和路径平滑度（PS），从时间维度捕捉传统指标无法揭示的碰撞、不平滑运动等导航自然连续性问题。

### 输入输出流总结

| 阶段 | 输入 | 处理 | 输出 |
|------|------|------|------|
| 语义接地 | 3DGS 场景 + 人工标注 | 投影→凸包→融合 | 2D 语义俯视图 + 分层指令 |
| 物理联合 | 美术网格 | CoACD 凸分解 | 碰撞体 + 物理接口 |
| 环境构建 | 高斯原语 + 语义 $M$ + 物理 $\Phi$ | 混合表示集成 | 可执行环境 $\mathcal{E}_{\mathrm{exec}}$ |
| 基准生成 | $\mathcal{E}_{\mathrm{exec}}$ | 路径规划 + MLLM 指令生成 | SAGE-Bench（2M 样本） |

该框架的关键优势在于：3DGS-网格混合表示在保持照片级渲染质量（每帧 6.2 ms）的同时，提供了比传统扫描网格（每帧 16.7 ms）快 2.7 倍的渲染速度和 3.9 倍的显存节省（220 MB vs 850 MB），为大规模具身导航训练提供了高效的环境基础。

## 核心模块与公式推导

SAGE-3D 将 3DGS 升级为可执行的语义-物理对齐环境，其核心可形式化为一个转换过程：

$$G \ : + \ : M \ : + \ : \Phi \ : \longrightarrow \ : { \mathcal{E} } _ { \mathrm{exec} }$$

其中 $G$ 为高斯原语，$M$ 为语义标注，$\Phi$ 为物理接口，三者融合生成可执行导航环境 $\mathcal{E}_{\mathrm{exec}}$。该环境被进一步建模为语义-物理增强的部分可观测马尔可夫决策过程：

$$\mathcal{E} = ( \mathcal{U} , \mathcal{S} , \mathcal{A} , \mathcal{O} , T , Z ; M , \Phi )$$

其中 $\mathcal{U}$ 为指令空间，$\mathcal{S}$ 为状态空间，$\mathcal{A}$ 为动作空间，$\mathcal{O}$ 为观测空间，$T$ 为状态转移函数，$Z$ 为渲染函数；$M$ 和 $\Phi$ 分别是注入的语义层与物理层。

### 对象级语义接地

该模块对 3DGS 场景进行人工对象级标注，包含对象类别、实例 ID 和包围盒信息，构建 InteriorGS 数据集。为实现路径规划与指令生成，将标注的 3D 对象投影到二维俯视语义地图。对于每个对象 $o_k$，其 2D 语义掩码 $\mathcal{M}_k$ 通过以下过程生成：

$${ \mathcal{M} } _ { k } = \operatorname{Fuse} \left( \operatorname{Hull} \left\{ \Pi _ { \mathrm{top} } ( p ) \mid p \in \operatorname{Surf} ( o _ { k } ) \right\} \right)$$

具体而言：从对象表面 $\operatorname{Surf}(o_k)$ 采样点 $p$，通过 $\Pi_{\mathrm{top}}$ 投影到地面平面，取凸包 $\operatorname{Hull}$ 后，再通过多视图融合 $\operatorname{Fuse}$ 得到最终的 2D 语义掩码。

### 物理感知执行联合

该模块解决 3DGS 缺乏碰撞几何的问题。核心思路是从美术师创建的三角网格出发，应用 CoACD 凸分解算法提取每个对象的碰撞体，构建 **3DGS-网格混合表示**：3DGS 负责照片级渲染，网格碰撞体负责物理仿真。这一解耦设计使得环境同时具备高保真外观与可靠的碰撞检测、机器人控制等物理接口。

### 导航连续性指标

为评估物理仿真下的导航质量，SAGE-Bench 引入三个连续性指标：

**连续成功率 (CSR)**：衡量智能体在满足任务条件的前提下，位于参考路径允许走廊内的时间比例。

$$\mathrm{CSR} = \frac{1}{T} \sum_{t=1}^{T} s(t)$$

**综合碰撞惩罚 (ICP)**：对轨迹上的碰撞强度进行时间平均，同时反映碰撞频率与持续时间。

$$\mathrm{ICP} = \frac{1}{T} \sum_{t=1}^{T} c(t)$$

**路径平滑度 (PS)**：基于连续航向角变化幅度的归一化平滑度评分，值越高表示路径越平滑。

$$\mathrm{PS} = 1 - \frac{1}{T-1} \sum_{t=2}^{T} \min \left( \frac{ | \Delta \theta_t | }{ \pi }, 1 \right)$$

其中 $\Delta \theta_t = \theta_t - \theta_{t-1}$ 为相邻时间步的航向角变化量。

## 实验与分析

### 实验设置

SAGE-Bench基准包含两个核心任务：**视觉语言导航（VLN）** 与 **视觉探索**。VLN任务测试集包含35个场景、1148条样本（944条高级指令、204条低级指令），视觉探索测试集覆盖100个场景。所有模型在8×NVIDIA H20上以统一超参数（batch size 256, lr=2e-5）训练，训练与测试场景无重叠。

评估指标分为两类：**传统离散指标**（SR、OSR、SPL、CR）和本文新提出的**连续性指标**——连续成功率（CSR）、综合碰撞惩罚（ICP）和路径平滑度（PS）。CSR衡量智能体在参考路径允许走廊内的停留时间比例，ICP对轨迹上的碰撞强度进行时间平均，PS基于连续航向角变化幅度评估路径平滑度。当模型导航成功率极低（SR<0.20）时，其碰撞率、ICP和PS指标被标记为灰色，因为模型行为近似随机动作，连续性指标缺乏可比性。

### 主实验结果

**SAGE-Bench VLN任务**（Table 2）：**NaVILA-SAGE** 取得最优表现，SR达0.46，OSR达0.55，SPL达0.48，显著超越所有闭源与开源基线。相比之下，NaVILA-base的SR仅为0.21，OSR为0.26，表明在SAGE-Bench的3DGS语义-物理对齐环境中训练对VLN性能有决定性提升。开源MLLM智能体（如InternVL-3-8B、Qwen2.5-VL-7B）的SR普遍低于0.20，其连续性指标被标记为灰色，说明通用MLLM在具身导航任务中存在严重的能力短板。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_HB6KvsqcAn/figures/005_Table_2.jpg]]
*Table 2: Comparison of different models on VLN and Visual Exploration tasks on SAGE-Bench. Bold values represent the best performance across all methods. Gray values indicate that these metrics lack comparative significance due to the low navigation performance of the models. Table 3: Rendering speed and training convergence comparison*

**环境渲染效率**（Table 3）：3DGS-网格混合表示每帧平均渲染耗时仅6.2 ms，显存占用220 MB，而传统扫描网格（如MP3D/HM3D）需16.7 ms和850 MB，分别提升约2.7倍和3.9倍。然而，3DGS数据存在收敛速度劣势：达到40% SR需160k次迭代（6.2小时），扫描网格仅需120k次迭代（4.8小时）。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_HB6KvsqcAn/figures/006_Table_3.jpg]]

**VLN-CE泛化测试**（Table 4）：仅用SAGE-Bench的3DGS数据训练、从未接触VLN-CE样本的模型，在R2R Val-Unseen上表现显著提升。NaVILA-SAGE的SR从NaVILA-base的0.29提升至0.38（+31%），OSR从0.37提升至0.51。NaVid-SAGE同样从NaVid-base的0.24提升至0.31。这验证了SAGE-3D环境在零样本泛化场景下的有效性。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_HB6KvsqcAn/figures/008_Table_4.jpg]]
*Table 4: Results on VLN-CE*

### 连续性指标分析

传统离散指标无法揭示导航过程中的物理质量问题。Figure 4可视化案例显示，NaVILA模型（蓝色轨迹）虽然能完成任务，但存在明显的非平滑运动和持续碰撞，这些缺陷被SR等离散指标掩盖。定量上，NaVILA在SAGE-Bench上取得0.39 SR和0.47 OSR，但其ICP高达0.61、PS仅为0.68（Table 2），表明轨迹存在大量碰撞和航向突变。CSR普遍高于SR，说明该指标对部分成功的导航轨迹更具包容性和鲁棒性。

### 消融实验

**指令层次消融**（Table 5）：所有模型在低级指令下的表现显著优于高级指令。NaVILA在低级指令下SR达0.56，高级指令下仅0.39，差距达0.17。GPT-4.1的差距更为悬殊（0.33 vs 0.11），说明现有VLN模型对因果依赖性强的高级语义指令理解能力不足。

**数据规模消融**（Table 6 & Figure 5）：增加训练场景数量比单纯增加单场景样本数更能提升模型性能。固定400个场景、增加样本数从60k到240k，SR从0.33提升至0.39；而固定60k样本、增加场景数从200到800，SR从0.28提升至0.38。Figure 5曲线显示，两条增长曲线在约60k样本处趋于收敛，表明场景多样性是性能提升的主导因素。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_HB6KvsqcAn/figures/011_Figure_5.jpg]]
*Figure 5: Model performance change curve (number of scenes vs. sample size)*

**指令类型切片分析**（Figure 6）：相对关系类指令（如“走到沙发左侧的桌子旁”）和属性类指令（如“找到红色的椅子”）对现有VLN模型更具挑战性，其SR比其他类型低2%以上，揭示了当前模型在细粒度空间推理和属性绑定上的薄弱环节。

### 关键发现总结

1. **3DGS语义-物理对齐环境是有效的训练基础**：仅用SAGE-Bench数据训练的模型在未见过的VLN-CE环境中取得31%的SR提升，证明照片级渲染与物理仿真解耦的混合表示具有强泛化能力。
2. **连续性指标暴露隐藏缺陷**：传统SR无法反映碰撞、路径不平滑等物理质量问题，CSR/ICP/PS为导航评估提供了更细粒度的诊断维度。
3. **场景多样性优于样本数量**：在固定数据总量下，增加场景数比增加单场景样本数对性能提升更显著，为数据高效训练提供了指导。
4. **高级语义指令仍是瓶颈**：所有模型在高级指令下的表现显著弱于低级指令，相对关系和属性类指令尤为困难，需进一步验证（该结论基于Figure 6的SR差异，具体数值需查阅原文确认）。

## 方法谱系与知识库定位

### 1. 问题定位与核心瓶颈

SAGE-3D 瞄准的是具身视觉语言导航（VLN）中一个关键但长期被忽视的基础设施瓶颈：**现有 3D 环境表示无法同时满足照片级渲染、细粒度语义理解和物理可执行性**。传统 VLN 基准（如 VLN-CE、RxR）依赖 Matterport3D 等扫描重建网格——这些网格存在几何伪影、纹理模糊，且缺乏对象级语义标注。而 3D Gaussian Splatting（3DGS）虽能提供高保真渲染，但本质上只是颜色与密度的集合，没有实例 ID、对象类别或碰撞几何，无法直接支撑智能体的语义推理与安全导航。

SAGE-3D 的核心贡献在于**将渲染与物理仿真解耦**：让 3DGS 专司照片级外观渲染，而通过美术师创建的精确网格提取碰撞体来负责物理交互。这种“3DGS-Mesh Hybrid Representation”在保持视觉真实感的同时，注入了对象级语义接地和物理感知执行联合两大能力，从而将 3DGS 从单纯的视觉资产升级为**可执行的具身环境基础**。

### 2. 与现有环境表示工作的关系

**相对于扫描网格环境**（Matterport3D、Habitat-Matterport 3D 等）：SAGE-3D 的 3DGS-Mesh 混合表示在渲染效率（6.2 ms/frame vs 16.7 ms/frame）和显存占用（220 MB vs 850 MB）上具有数量级优势（Table 3）。更重要的是，扫描网格的几何精度受限于重建算法，而 SAGE-3D 使用的碰撞体直接来自美术师创建的真值网格，物理仿真的可靠性更高。

**相对于纯 3DGS 环境**：传统 3DGS 场景缺乏语义和物理约束，智能体可以“穿透”物体。SAGE-3D 通过 Object-Centric Semantic Grounding 为 3DGS 添加了对象类别、实例 ID 和包围盒等细粒度标注，并通过 CoACD 凸分解从美术网格中提取碰撞体，构建了完整的物理仿真接口。

**相对于其他语义增强的神经渲染**（如 Semantic-NeRF、LERF 等）：这些工作主要在 NeRF 框架下进行语义注入，但 NeRF 的渲染速度远慢于 3DGS，且缺乏物理可执行性的考量。SAGE-3D 在 3DGS 基础上同时解决语义和物理两个维度，形成了更完整的具身环境范式。

### 3. 与下游 VLN 模型的关系

SAGE-3D 提供的是**环境基础设施**而非导航策略本身。它的价值通过两类实验得到验证：

**域内评估**（SAGE-Bench）：在自建的 3DGS 基准上，SAGE-3D 环境支撑了多种 VLN 模型的训练与评估。**NaVILA**（Cheng et al., 2025）在 SAGE-3D 数据上微调后（NaVILA-SAGE）达到 SR=0.46、OSR=0.55（Table 2），显著优于在传统数据上训练的版本。

**跨域泛化**（VLN-CE R2R Val-Unseen）：更关键的是，**仅用 SAGE-3D 数据训练、从未接触过 VLN-CE 样本的模型**，在 VLN-CE 未见环境上将基线成功率从 0.29 提升至 0.38（+31%），证明了高质量 3DGS 环境数据对真实世界策略泛化的推动作用（Table 4）。

### 4. 适用边界与局限

尽管 SAGE-3D 展示了显著的性能提升，其适用边界和局限性同样值得注意：

1. **物理仿真依赖美术网格**：碰撞体的质量取决于美术师创建的原始网格。对于通过扫描重建的真实场景，需要额外的近似或后处理步骤才能提取可靠的碰撞几何，这限制了方法在完全非受控环境中的直接部署。

2. **训练收敛速度较慢**：3DGS 场景数据达到 40% SR 需要 160k 次迭代（6.2 小时），而扫描网格仅需 120k 次（4.8 小时）（Table 3）。这表明 3DGS 渲染的视觉丰富性可能增加了策略学习的样本复杂度。

3. **场景覆盖有限**：InteriorGS 数据集目前主要覆盖室内居住空间及有限类别的户外场景（如健身房、音乐厅、游泳池）。对于完全非结构化环境（如野外、水下）的物理接口和指令设计尚未验证。

4. **连续性指标的低性能盲区**：新提出的 CSR、ICP、PS 指标在模型导航成功率极低（SR<0.20）时缺乏区分度，在 Table 2 中被标记为灰色不可比，限制了其对弱模型的诊断能力。

### 5. 开放问题

从 SAGE-3D 的当前设计出发，以下几个方向值得进一步探索：

- **训练效率优化**：能否通过课程学习（从简单场景到复杂场景）或数据增强策略加速 3DGS 环境下的训练收敛？
- **动态场景扩展**：在存在移动障碍物或动态物体的场景中，能否实时更新 3DGS 并维持物理仿真的实时性？
- **跨表示泛化**：语义-物理对齐的范式是否可以推广到其他隐式神经表示（如 NeRF、3D Gaussian 的变体），形成更通用的具身环境框架？
- **Sim-to-Real 迁移**：在完全虚拟的 3DGS 环境中训练出的 VLN 策略，能否通过微小的域适配（如风格迁移、物理参数校准）实现真实世界的零样本迁移？

## 原文 PDF

![[paperPDFs/ICLR_2026/Towards_Physically_Executable_3D_Gaussian_for_Embodied_Navigation.pdf]]
