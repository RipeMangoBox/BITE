---
title: "CapNav: Benchmarking Vision Language Models on Capability-conditioned Indoor Navigation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CapNav_Benchmarking_Vision_Language_Models_on_Capability_conditioned_Indoor_Navigation.pdf
project_link: null
code_link: "https://github.com/makeabilitylab/CapNav"
aliases:
- CapNav
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过引入显式的代理能力剖面（agent profile），将导航问题从通用路径规划转变为能力依赖的可行性判断与路径选择。
primary_logic: 系统的代理能力变化会显著改变导航可行性和路径选择，而现有VLM无法可靠地整合这类约束，暴露了空间尺寸估计和多帧视觉信息融合的根本缺陷。
claims:
- 导航性能在移动能力约束加重时显著下降；HUMANOID代理的平均CapNav分数最低（39.12%），而无约束的人类代理分数最高（57.83%）。
- 增加视觉输入帧数并不总能带来性能提升，存在视觉整合瓶颈。
- 所有模型在需要隐式空间度量估计的障碍类型（如狭窄通道、转弯半径）上表现明显更差。
- CapNav (full) 上 CapNav Score = 67.18 (Gemini-2.5-pro, thinking)
---

# CapNav: Benchmarking Vision Language Models on Capability-conditioned Indoor Navigation

> [!tip] 核心洞察
> 系统的代理能力变化会显著改变导航可行性和路径选择，而现有VLM无法可靠地整合这类约束，暴露了空间尺寸估计和多帧视觉信息融合的根本缺陷。

| 字段 | 内容 |
|------|------|
| 中文题名 | CapNav：面向能力约束室内导航的视觉语言模型基准测试 |
| 英文题名 | CapNav: Benchmarking Vision Language Models on Capability-conditioned Indoor Navigation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.18424) · [Code](https://github.com/makeabilitylab/CapNav) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CapNav |
| Dataset | CapNav |

> [!tip] 效果简介
> - CapNav (full) 上，CapNav Score 67.18 (Gemini-2.5-pro, thinking) vs 29.35 (Random-walk) (+37.83)。
> - CapNav (capability stress) 上，CapNav Score (HUMANOID vs ADULT) 39.12 (HUMANOID mean) vs 57.83 (ADULT mean) (-18.71)。
> - CapNav (best model vs human upper bound) 上，CapNav Score 67.18 (Gemini-2.5-pro) vs 74.77 (Human best) (-7.59)。

## 概要

### 问题与动机

视觉语言模型（VLM）在通用视觉导航任务中已展现出显著能力，但现有基准普遍忽略了一个关键现实因素：**代理自身的物理移动能力约束**。轮椅使用者无法爬楼梯、人形机器人受限于狭窄通道、扫地机器人不能操作电梯——这些能力差异从根本上改变了导航的可行性与路径选择。然而，当前VLM能否可靠地将此类能力约束纳入导航决策，仍是一个未被系统回答的问题。

### 核心贡献

本文提出 **CapNav**（Capability-Conditioned Navigation），首个面向能力约束室内导航的VLM基准测试。CapNav将导航问题从通用路径规划重新定义为**能力依赖的可行性判断与路径选择**：给定室内空间的巡游视频、导航任务和代理能力剖面（物理尺寸、操作能力），VLM需同时输出任务可行性、有效路径及推理依据。

CapNav具有三个核心设计：

1. **显式能力剖面**：定义五种代表性代理——无运动障碍成人、轮椅使用者、人形机器人、四足机器人、扫地机器人——每种代理具备不同的物理尺寸和功能能力（如能否爬楼梯、操作电梯）。
2. **图基空间抽象**：基于预注释的边级可通行性标签，支持多路径搜索和每代理、每边的可通行性评估，从而允许复数解决方案。
3. **多维度评估体系**：引入可行性F1、路径有效性、路由可通行性准确率、推理有效性四项互补指标，并组合为CapNav综合分数，从决策正确性到推理质量进行全面衡量。

### 关键发现

对13个主流VLM的系统评估揭示了若干重要瓶颈：

- **能力约束下性能骤降**：所有模型在移动能力约束加重时导航性能显著下降。无约束成人代理的平均CapNav分数为57.83%，而人形机器人仅为39.12%，降幅达18.71个百分点。
- **隐式几何约束是主要短板**：模型在具有显著视觉特征的可视障碍（如楼梯、电梯）上表现较好，但在需要隐式空间度量估计的约束类型（狭窄通道、转弯半径）上普遍失效，暴露了VLM在空间尺寸估计方面的根本缺陷。
- **视觉整合瓶颈**：增加输入视频帧数并不总能带来性能提升，收益随模型而异且趋于饱和，表明当前VLM在多帧视觉信息的长程整合上存在瓶颈。
- **最佳模型仍低于人类上限**：性能最强的Gemini-2.5-pro（thinking模式）CapNav分数达67.18%，虽超过人类平均水平，但仍低于最佳人类表现的74.77%。

### 方法定位

CapNav在方法谱系上属于**能力感知的视觉语言导航基准**，区别于传统VLN基准的关键在于将代理能力约束显式纳入任务定义。其评估范式融合了图基可通行性判断与LLM-as-judge推理评估，为后续研究提供了可扩展的框架。数据集包含45个室内场景、2365个导航任务和5075条可通行性标注，代码与基准已开源。

视觉语言模型（VLM）在通用视觉理解与推理任务上取得了显著进展，但在具身导航领域，现有基准主要评估模型在无约束条件下的路径规划能力。真实世界的导航问题并非单纯的“从A到B”的最短路径搜索——代理自身的物理尺寸、运动能力与操作限制（如能否爬楼梯、转弯半径、可通过宽度）从根本上决定了某条路径是否可行。然而，当前VLM导航评估体系普遍忽略这一关键维度，导致我们无法回答一个核心问题：**VLM能否在给定代理能力约束下做出正确的可行性判断与路径选择？**

这一缺口在以下场景中尤为突出：轮椅使用者需要避开楼梯与窄门，人形机器人受限于步幅与平衡能力，扫地机器人无法攀越门槛。同一室内空间、同一导航任务，对不同代理而言可能意味着截然不同的可行路径，甚至完全不可行。现有视觉语言导航（VLN）基准（如R2R、RxR、REVERIE）以人类行走轨迹为参照，假设所有代理具有同质的无约束移动能力，无法捕捉这种能力依赖的导航复杂性。与此相对，机器人领域的导航方法虽考虑运动学约束，却通常依赖精确的几何地图或端到端的模仿学习，缺乏对语义场景理解与自然语言指令的整合，更未在VLM范式下系统评估。

CapNav正是为填补这一空白而提出。其核心动机在于：**将导航问题从通用路径规划重新定义为能力依赖的可行性判断与路径选择**。通过显式引入代理能力剖面（agent profile），CapNav迫使模型在空间理解、尺寸估计与约束推理三个层面同时做出判断——这正是当前VLM所暴露的根本短板。初步证据表明，即便是最先进的VLM，在面临不可视的几何约束（如狭窄通道、转弯半径）时，其导航性能也会急剧下降，揭示了空间度量推理与多帧视觉信息融合的深层瓶颈。

## 核心方法与创新机理

CapNav 的核心创新在于将室内导航任务从“通用路径规划”重新定义为**能力约束下的可行性判断与路径选择问题**。这一范式转换通过三个关键环节实现，直接改变了现有 VLM 导航评估的输入空间、推理逻辑和评价体系。

### 创新一：引入显式的代理能力剖面

传统视觉语言导航（VLN）任务仅向模型提供导航指令和场景视觉信息，隐含假设代理具有无限制的移动能力。CapNav 在任务输入中显式引入了**代理能力剖面（agent profile）**，将导航实例定义为 $\langle S, \tau, \mathbf{a} \rangle$ 三元组，其中 $\mathbf{a}$ 编码了代理的物理尺寸（高度、宽度、长度）和操作性能力（能否爬楼梯、操作电梯、上下坡等）。

这一设计使得**同一场景、同一任务**在不同代理类型下可能具有截然不同的可行性和最优路径。基准覆盖了五种典型实体：无行动障碍的成年人、轮椅使用者、人形机器人、四足机器人和扫地机器人。实验表明，代理能力约束对导航性能的影响极为显著——HUMANOID 代理的平均 CapNav 分数仅为 39.12%，而无约束成年人代理则达到 57.83%，差距高达 18.71 个百分点。这一瓶颈揭示了当前 VLM 在整合空间几何约束与代理物理参数方面的根本性缺陷。

### 创新二：基于图抽象的多路径可通行性评估

现有 VLN 评估通常基于单一路径的轨迹匹配或终点成功率，难以处理**存在多条可行路径**的场景，更无法精细评估路径的局部可通行性。CapNav 采用**图结构空间抽象**，将室内空间建模为语义空间节点和可通行边的连通图 $G = (V, E)$，并为每个代理类型逐边标注可通行性标签 $g_e^{(\mathbf{a})} \in \{0, 1\}$。

这一设计的直接优势体现在两个方面：
1. **支持复数解**：当存在多条从起点到终点的简单路径时，模型可以输出任意有效路径，评估不再依赖单一参考轨迹。
2. **细粒度可通行性评估**：通过 Route Traversability Accuracy 指标 $\mathrm{RTA}(\hat{P}, \mathbf{a}) = \frac{\sum_{e \in E(\hat{P})} g_e^{(\mathbf{a})}}{|E(\hat{P})|}$，可以量化预测路径中实际可通行边的比例，揭示模型在局部几何约束上的推理能力。

### 创新三：四维互补评估体系

CapNav 打破了传统 VLN 仅关注成功率的评估范式，构建了四个互补的评估维度并组合为统一的 CapNav 综合分数：

$$ \mathrm{CapNav} = \lambda_c F_1 + \lambda_p \mathrm{PV} + \lambda_t \overline{\mathrm{RTA}} + \lambda_r \overline{\mathrm{RV}}, \quad \sum \lambda = 1 $$

其中各维度等权（$\lambda = 0.25$），分别衡量：
- **可行性 F1**（Feas-F1）：模型判断任务是否可完成的分类性能。
- **路径有效性**（PV）：预测路径是否为有效的简单路径。
- **路由可通行性准确率**（RTA）：预测路径中边的实际可通行比例。
- **推理有效性**（RV）：通过 LLM-as-judge 评估模型给出的推理理由与标注的一致性。

这一评估体系的设计直击能力约束导航的核心挑战：一个模型可能正确判断任务可行，却选择了包含不可通行边的路径；或者路径正确，但推理理由完全错误。四维分解使得不同模型的失败模式可以被精确诊断。消融实验表明，CapNav 分数构成权重变化对模型排名影响较小（Kendall’s $\tau$ 平均为 0.909），说明评估结论对权重选择具有鲁棒性。

### 方法谱系与知识库定位

CapNav 位于**具身视觉语言导航**与**能力感知评估**的交叉点。与传统的 VLN 基准（如 R2R、RxR）相比，CapNav 不要求模型执行增量动作预测，而是以图空间抽象上的全局路径规划为任务形式，这与 **SayNav**（Rajvanshi et al., CoRL 2023）等高层规划方法在任务粒度上相似，但 CapNav 首次将代理物理能力作为显式输入条件。在评估维度上，CapNav 借鉴了 **MPGD**（He et al., CVPR 2023）等多指标评估的思想，但将评估重心从轨迹几何匹配转向了能力依赖的可通行性验证。与同时期的空间推理基准（如 SpatialBench）相比，CapNav 的独特贡献在于将空间尺寸估计与代理物理约束直接耦合，暴露了 VLM 在“不可视几何约束”（如狭窄通道宽度、转弯半径）上的系统性短板。

CapNav 将能力约束下的室内导航形式化为一个**空间–任务–能力三元组**（Space–Task–Capability triple）的评估问题。给定一个室内空间的巡游视频、其导航图的节点列表、代理的移动能力剖面以及一个导航任务，视觉语言模型（VLM）需要同时输出三个判断：**任务可行性** $\hat{y}$、**导航路径** $\hat{P}$ 和**推理理由** $\hat{\rho}$。这一输入-输出映射可表示为：

$$( \hat { y } , \hat { P } , \hat { \rho } ) = f _ { \theta } ( S , \tau , \mathbf { a } )$$

其中 $S$ 为场景（以巡游视频和导航图节点形式呈现），$\tau$ 为自然语言导航任务，$\mathbf{a}$ 为代理能力剖面——包含代理的物理尺寸（高度、宽度、长度）以及操作能力（如能否爬楼梯、使用电梯等）。

整个基准的数据构建与评估流程由五个核心模块串联而成：

1. **3D场景与视频录制**：基于 HM3D 和 Matterport3D 的室内 3D 扫描，人工录制以人眼高度（1.5 m）为视角的巡游视频，帧率为 2 FPS，确保视频覆盖场景中所有语义空间节点。

2. **导航图构建**：在语义上有意义的空间节点（如房间入口、走廊交叉口、楼梯口等）之间，人工标注可直接通行的边，形成连通图 $G = (V, E)$。该图抽象提供了多路径搜索的基础，支持复数解决方案的评估。

3. **任务生成**：将场景视频与节点列表提供给 Gemini 2.5 Pro，自动生成自然语言导航任务，再经人工验证确保任务有效性和表述清晰性。

4. **可通行性标注**：在专用标注界面中，人工操控 3D 代理模型沿每条可能的简单路径行走，为每条边 $e$ 和每种代理类型 $\mathbf{a}$ 赋予可通行性标签 $g_e^{(\mathbf{a})} \in \{0, 1\}$，并记录不可通行的原因。这一步骤为每个代理类型建立了边级的可通行性真值。

5. **VLM 评估**：给定 $\langle S, \tau, \mathbf{a} \rangle$，VLM 输出可行性判断、路径和理由，系统将其与标注真值进行多维度对比。

评估体系从四个互补维度衡量模型表现：**可行性 F1**（Feas-F1）判断任务是否存在可通行路径；**路径有效性**（Path Validity, PV）验证预测路径是否为从起点到终点的有效简单路径；**路由可通行性准确率**（Route Traversability Accuracy, RTA）计算预测路径中实际可通行边的比例；**推理有效性**（Reasoning Validity, RV）利用 LLM-as-judge 评估模型给出的理由与标注真值的一致性。最终，这四个指标以等权重（各 0.25）组合为 **CapNav 综合分数**：

$$\mathrm { C a p N a v } = \lambda _ { c } F _ { 1 } + \lambda _ { p } \mathrm { P V } + \lambda _ { t } \overline { { { \mathrm { R T A } } } } + \lambda _ { r } \overline { { { \mathrm { R V } } } } , \quad \sum \lambda = 1$$

该框架的核心设计在于：通过引入显式的代理能力剖面，将通用路径规划问题转化为**能力依赖的可行性判断与路径选择**问题。同一场景、同一任务，对于不同代理类型可能具有截然不同的可行性和最优路径——例如，一个需要穿越楼梯的任务对轮椅代理不可行，对四足机器人可行，而对双足人形机器人则取决于其楼梯攀爬能力。这种设计直接暴露了当前 VLM 在空间尺寸估计和几何约束推理方面的根本缺陷。

![[assets/figures/papers/paper_list_l2378_https_arxiv_org_abs_2602_18424/figures/001_Figure_1.jpg]]
*Figure 1: We introduce Capability-Conditioned Navigation (CapNav), a benchmark designed to evaluate how well VLMs can navigate complex indoor spaces given an agent’s specific physical and operational capabilities. CapNav inputs (1) a tour video of an indoor space, (2) nodes of its navigation graph, (3) an agent’s mobility profile, and (4) a navigation task, and evaluates VLM outputs in task feasibility, path validity, route traversability, and reasoning validity*

![[assets/figures/papers/paper_list_l2378_https_arxiv_org_abs_2602_18424/figures/003_Figure_3.jpg]]
*Figure 3: Overview of CapNav’s data construction: Starting from a 3D indoor scan, we manually record a touring video and a navigation graph. We then use Gemini to generate natural language navigation tasks. Finally, per-task and per-agent traversability are annotated by manually controlling agents in the annotation interface*

CapNav将能力约束导航形式化为一个**空间–任务–能力三元组**的查询问题，并通过四个互补指标对VLM输出进行细粒度评估。以下阐述其核心形式化定义与评估体系。

### 任务形式化：空间–任务–能力三元组

CapNav的每个任务实例定义为一个三元组：

$$\langle S , \tau , \mathbf { a } \rangle$$

其中 $S$ 为室内空间的巡游视频与导航图节点列表，$\tau$ 为自然语言导航任务（指定起点与目标），$\mathbf{a}$ 为代理能力剖面（编码物理尺寸与操作能力，如能否爬楼梯、操作电梯等）。给定该三元组，VLM需输出三项预测：

$$( \hat { y } , \hat { P } , \hat { \rho } ) \ = \ f _ { \theta } ( S , \tau , { \bf a } )$$

其中 $\hat{y} \in \{0,1\}$ 为任务可行性判断，$\hat{P}$ 为预测的导航路径（节点序列），$\hat{\rho}$ 为自然语言推理理由。

### 可行性真值定义

可行性真值 $y^{\star}$ 基于预标注的边级可通行性标签严格定义：当且仅当存在一条从源节点 $v_{\mathrm{src}}$ 到目标节点 $v_{\mathrm{tgt}}$ 的简单路径，且路径上每条边 $(u,v)$ 对代理 $\mathbf{a}$ 均可通行时，任务为可行：

$$y ^ { \star } = \mathbb { I } [ \exists P ( v _ { \mathrm { s r c } } , v _ { \mathrm { t g t } } ) : \forall ( u , v ) \in P , g _ { ( u , v ) } ^ { ( \mathbf { a } ) } = 1 ]$$

其中 $g_{(u,v)}^{(\mathbf{a})} \in \{0,1\}$ 为边 $(u,v)$ 对代理 $\mathbf{a}$ 的可通行性标签。这一形式化将导航从通用路径规划转化为**能力依赖的可行性判断**——同一空间、同一任务，不同代理的可行性与最优路径可能截然不同。

### 四维评估指标体系

CapNav从四个互补维度评估VLM输出，并组合为综合分数。

**路径有效性（Path Validity，PV）** 衡量预测路径是否为从源到目标的合法简单路径：

$$\mathrm { P V } = \mathbb { E } \big [ \mathbb { I } ( \hat { P } \in \mathcal { P } _ { \mathrm { s i m p l e } } ( v _ { \mathrm { s r c } } , v _ { \mathrm { t g t } } ) ) \big ]$$

该指标不涉及能力约束，仅检验路径的拓扑合法性——即VLM是否理解导航图结构并输出连通路径。

**路由可通行性准确率（Route Traversability Accuracy，RTA）** 衡量预测路径中实际可通行边的比例，直接反映VLM对代理能力约束的感知精度：

$$\mathrm { R T A } ( \hat { P } , { \bf a } ) = \frac { \sum _ { e \in E ( \hat { P } ) } g _ { e } ^ { ( { \bf a } ) } } { | E ( \hat { P } ) | }$$

RTA捕获VLM的局部可通行性判断能力：即使路径整体有效，若包含不可通行边（如轮椅无法通过的台阶），RTA将低于1.0。

**推理有效性（Reasoning Validity，RV）** 利用LLM-as-judge评估VLM输出的推理理由与标注真值的一致性：

$$\mathrm { R V } = \mathbb { E } \Big [ J _ { \mathrm { L L M } } \big ( \hat { \rho } , \mathcal { R } ^ { \star } ( \hat { P } , { \bf a } ) \big ) \Big ]$$

其中 $\mathcal{R}^{\star}$ 为基于预测路径与代理能力生成的参考理由集合，$J_{\mathrm{LLM}}$ 为LLM判断器。该指标旨在检验VLM是否真正理解了能力约束的因果逻辑，而非仅凭表面模式做出正确预测。

### 综合分数：CapNav Score

四个子指标通过等权加权组合为CapNav综合分数：

$$\mathrm { C a p N a v } = \lambda _ { c } F _ { 1 } + \lambda _ { p } \mathrm { P V } + \lambda _ { t } \overline { { { \mathrm { R T A } } } } + \lambda _ { r } \overline { { { \mathrm { R V } } } } , \sum \lambda . = 1$$

其中 $F_1$ 为可行性预测的F1分数，$\overline{\mathrm{RTA}}$ 和 $\overline{\mathrm{RV}}$ 分别为RTA和RV在所有任务上的均值。默认权重 $\lambda_c = \lambda_p = \lambda_t = \lambda_r = 0.25$。消融实验表明，权重变化对模型排名影响较小（不同方案间Kendall’s $\tau$ 平均为0.909），说明综合分数的结论对权重扰动具有鲁棒性。

### 数据构建流水线

CapNav的数据构建流水线（Figure 3）包含四个关键模块：

1. **3D场景与视频录制**：基于HM3D和Matterport3D的3D室内扫描，手动录制巡游视频（2FPS，人眼高度1.5m）。
2. **导航图构建**：手动标注语义空间节点和直接可通行的边，形成连通图 $G=(V,E)$。
3. **任务生成**：将场景视频和节点列表提供给Gemini 2.5 Pro自动生成导航任务，经人工验证确保有效性。
4. **可通行性标注**：在标注界面中手动操控3D代理模型，为每条边和每种代理类型赋予可通行性标签 $g_e^{(\mathbf{a})} \in \{0,1\}$ 及原因说明。

该流水线产出了包含45个场景、2365个导航任务、5075条可通行性标注的数据集，覆盖五种代理类型（无运动障碍成人、轮椅使用者、扫地机器人、人形机器人、四足机器人）。

![[assets/figures/papers/paper_list_l2378_https_arxiv_org_abs_2602_18424/figures/004_Figure_4.jpg]]
*Figure 4: Examples of CapNav’s agent profiles. Left: each profile specifies the physical dimensions and functional capabilities. Right: the agents’ physical dimensions are rendered and maneuvered in the 3D scenes to help confirm traversability*

![[assets/figures/papers/paper_list_l2378_https_arxiv_org_abs_2602_18424/figures/002_Figure_2.jpg]]
*Figure 2: The CapNav benchmark evaluates whether VLMs can correctly ground differences in agent mobility capabilities when generating navigation plans. This example demonstrates a navigation task that has different feasibility and path for different agents*

## 实验与关键发现

### 主结果：VLM能力约束导航的整体表现

我们在CapNav基准上对13个主流VLM进行了全面评估，表2汇总了各模型在最优帧数设置下的综合表现。所有受测模型均显著优于随机游走基线（CapNav = 29.35%），表明VLM确实具备一定的能力感知导航推理能力。然而，模型间性能差异巨大，且与人类表现存在明显差距。

表现最强的是闭源模型，尤其是 **Gemini-2.5-pro**（thinking模式，CapNav = 67.18%）和 **GPT-5-pro**，它们超过了人类平均水平（CapNav = 60.59%），但仍低于最佳人类表现（CapNav = 74.77%）。开源模型中，**Qwen3-VL-8B** 表现相对较好，但整体与闭源模型存在约10–20个百分点的差距。值得注意的是，**Doubao-Seed-1.6-thinking** 作为空间推理专用模型，其CapNav分数达到64.57%，接近顶级闭源模型，说明显式的空间推理设计对这类任务确有帮助。

从四个子指标来看，模型在**路径有效性**（PV）上表现最好，多数模型能达到0.7以上，说明VLM在给定起点和终点时能较好地生成符合图拓扑的路径。但在**路由可通行性准确率**（RTA）和**推理有效性**（RV）上表现明显薄弱——即便是最强模型，RTA也仅约0.75，RV则普遍低于0.5。这揭示了核心瓶颈：VLM能“找到一条路”，但难以判断这条路对特定代理是否真的可通行，也难以给出与标注一致的推理依据。

### 能力约束压力测试：代理类型间的性能分化

将CapNav分数按代理类型拆分（表2右半部分），可以清晰观察到能力约束加重时的性能退化规律。以无移动能力限制的**ADULT**代理为基线（平均CapNav = 57.83%），各受约束代理的性能均有不同程度下降：

- **WHEELCHAIR**（轮椅使用者）：平均CapNav = 48.21%，下降约9.6个百分点。轮椅面临的主要障碍是楼梯和狭窄通道，其中楼梯是显式视觉特征，模型识别相对容易，因此降幅相对可控。
- **SWEEPER**（扫地机器人）：平均CapNav = 45.35%，下降约12.5个百分点。扫地机器人无法上下楼梯，且受限于低矮空间，但整体尺寸较小，通道宽度约束不严苛。
- **QUADRUPEDAL**（四足机器人）：平均CapNav = 44.08%，下降约13.8个百分点。四足机器人可爬楼梯但无法操作电梯，且宽度限制较严。其性能下降主要来自对电梯依赖场景的误判。
- **HUMANOID**（人形机器人）：平均CapNav = 39.12%，下降约18.7个百分点，是所有代理类型中降幅最大的。人形机器人同时受限于楼梯（不可爬）、电梯（不可操作）、狭窄通道和转弯半径，约束维度最多且最严格。

这一梯度式退化验证了分析中的核心发现：**代理能力约束的维度和严格程度直接决定了VLM导航性能的退化幅度**。特别值得注意的是，HUMANOID与ADULT之间的18.71个百分点差距，远超其他代理类型间的差距，说明当前VLM在处理多重并发约束时存在叠加性失效。

从表1的数据集统计来看，这种性能分化与任务本身的难度分布高度一致：HUMANOID代理的可行任务比率仅为0.22，边可通行性比率仅为0.43，是所有代理类型中最低的。这意味着HUMANOID场景中的正确路径更加稀疏，对模型的路径选择精度要求更高。

### 障碍物类型分析：显式特征与隐式度量的能力鸿沟

图5按障碍物类型拆分了模型准确率，揭示了VLM空间推理的一个根本性缺陷。所有模型在具有**显式视觉特征**的障碍物上表现明显更好——例如楼梯（视觉特征突出）、电梯（有明确的操作面板和门）——而在需要**隐式空间度量估计**的障碍物上表现显著更差。

具体而言，模型对“不能爬楼梯”这类约束的判断准确率普遍较高（多数模型超过70%），因为楼梯具有鲜明的视觉特征，模型可以通过单帧图像直接识别。但对于“狭窄通道”（需要估计通道宽度是否小于代理宽度）和“转弯半径不足”（需要估计转角空间是否足够代理转弯），模型准确率大幅下降，部分模型甚至低于50%。

这一定性发现与定量结果一致：**当前VLM缺乏可靠的空间度量推理能力**。它们擅长识别“有什么”，但不擅长判断“能否通过”。这一瓶颈在需要精确尺寸估计的场景中尤为致命——例如判断轮椅能否通过一个看似宽阔但实际宽度不足的门廊，或判断人形机器人能否在一个看似空旷但转弯半径不足的拐角处转向。

### 视觉输入帧数的影响与整合瓶颈

图6展示了不同帧数预算下的性能变化。总体趋势是：增加输入帧数可以带来性能提升，但收益高度依赖模型，且在高帧数下趋于饱和。这一现象被分析诊断为**视觉整合瓶颈**：VLM在多帧视觉信息的长程整合方面存在根本性限制。

具体表现为：部分模型在帧数从4帧增加到8帧时获得明显收益（如GPT-5-pro提升约3个百分点），但从8帧增加到16帧时收益急剧衰减甚至出现负收益。另一些模型（如部分开源模型）对帧数增加几乎不敏感，性能曲线近乎平坦。这说明当前VLM的视觉编码器或跨帧注意力机制在处理长序列视觉输入时存在信息遗忘或冗余抑制问题，无法有效提取跨帧的几何一致性信息。

### 消融实验：思考模式、微调与指标鲁棒性

**思考模式的影响**：启用thinking模式后，模型平均CapNav分数提升6.87%。这一收益主要来自推理有效性（RV）和可行性F1的提升，说明链式推理有助于模型更系统地权衡代理能力约束。但thinking模式对RTA的提升有限，再次印证了空间度量推理是一个更深层的感知瓶颈，而非单纯的推理链长度问题。

**微调实验**：对Qwen3-VL-8B进行LoRA微调后，测试集CapNav分数从45.26%提升至55.18%（+9.92个百分点），表明模型确实可以从能力约束标注中学习。然而，推理有效性（RV）从0.30降至0.25，出现了“分数上升但解释质量下降”的现象。这提示微调可能使模型学会了“猜测”正确答案的模式，而非真正习得能力约束推理的因果逻辑——这是一个值得关注的泛化风险信号。

**指标权重鲁棒性**：我们测试了多组不同的CapNav分数权重方案，不同方案下模型排名的Kendall’s τ平均为0.909，表明综合分数的结论对权重变化具有较强的鲁棒性，不会因指标组合方式的微调而出现排名反转。

### 人类基线分析

人类参与者在CapNav上的平均分数为60.59%，最佳表现为74.77%。人类在路径有效性（PV）上接近满分，但在RTA和RV上也存在失误，主要发生在需要精确尺寸估计的狭窄通道和转弯半径场景。这说明即便是人类，在缺乏精确测量工具的情况下，仅凭视觉巡视视频进行空间度量判断也存在一定困难——但人类的失误率远低于VLM，且失误模式更倾向于“保守误判”（将可行路径误判为不可行），而非VLM常见的“激进误判”（将不可行路径误判为可行）。

### 失败模式总结

综合以上分析，VLM在CapNav上的主要失败模式可归纳为三类：

1. **空间度量盲区**：对需要精确尺寸估计的障碍物（狭窄通道、转弯半径）缺乏感知能力，倾向于忽略或低估几何约束。
2. **多约束叠加失效**：当代理同时面临多种能力限制时（如HUMANOID），模型难以协调多个约束的联合影响，性能呈非线性下降。
3. **视觉整合瓶颈**：多帧视觉信息无法有效融合，限制了模型从巡视视频中构建连贯空间理解的能力，且增加帧数的边际收益递减。

![[assets/figures/papers/paper_list_l2378_https_arxiv_org_abs_2602_18424/figures/006_Table_2.jpg]]
*Table 2: CapNav performance across 13 VLMs. Each number indicate the best performance under all tested frame settings. Left block reports each task metrics (Feas-F1, PV, RTA, RV, CapNav). Right block reports per-agent composite scores for the five agent types: adult with no motor disabilities, humanoid robot, quadrupedal, sweeping robots, and wheelchair users. Bold number indicate best per block. Blue indicate open-sourced model; Green indicate proprietary; Orange indicate spatial reasoning models*

![[assets/figures/papers/paper_list_l2378_https_arxiv_org_abs_2602_18424/figures/005_Table_1.jpg]]
*Table 1: Ratio of feasible task and traversable edges per agent type*

## 定位与知识库关联

### 1. 任务定义的范式转换

传统的视觉语言导航（VLN）基准通常将导航建模为“给定指令和视觉观察，预测下一步动作”的端到端模仿学习问题，其核心假设是代理的移动能力是通用且无差异的。CapNav 通过引入显式的**代理能力剖面（agent profile）**，将问题从“如何走”转变为“以我的身体条件，能否走通、该走哪条路”。这一转换的关键在于将导航任务形式化为一个 $\langle S, \tau, \mathbf{a} \rangle$ 三元组，其中 $\mathbf{a}$ 编码了代理的物理尺寸（高度、宽度、底盘离地间隙）和操作能力（能否上下楼梯、操作电梯等）。

这一范式与现有工作的根本区别在于：它不再追求单一最优路径，而是承认**不同代理能力下存在复数可行解**。为此，CapNav 采用了基于图的空域抽象——手动标注的导航图 $G=(V,E)$ 中，每条边 $e$ 对每个代理类型 $\mathbf{a}$ 都配有独立的可通行性标签 $g_e^{(\mathbf{a})} \in \{0,1\}$。这种“每代理、每边”的标注策略使得评估可以精确到边级别的可通行性判断，而非仅做整体轨迹匹配。

### 2. 评估体系的创新

在评估指标层面，CapNav 跳出了传统 VLN 中单一的轨迹成功率或路径匹配度，构建了四个互补维度的评估框架：

- **可行性 F1（Feas-F1）**：判断任务是否可完成，这是能力约束导航中最基础的决策；
- **路径有效性（PV）**：预测路径是否为从起点到终点的有效简单路径，检验模型的空间连通性理解；
- **路由可通行性准确率（RTA）**：预测路径中实际可通行边的比例，直接度量模型对物理约束的敏感性；
- **推理有效性（RV）**：通过 LLM-as-judge 评估模型给出的推理理由是否与标注一致。

这四个指标通过等权重加权组合为 **CapNav 综合分数**：
$$\mathrm{CapNav} = \lambda_c F_1 + \lambda_p \mathrm{PV} + \lambda_t \overline{\mathrm{RTA}} + \lambda_r \overline{\mathrm{RV}}, \quad \sum \lambda = 1$$

其中各 $\lambda$ 默认取 0.25。消融实验表明，权重方案的变化对模型排名影响有限（不同方案间 Kendall’s $\tau$ 平均为 0.909），说明该综合分数对权重选择具有较好的鲁棒性。

### 3. 与现有基准和方法的定位关系

CapNav 在基准设计上与以下工作形成对比或互补：

- **传统 VLN 基准**（如 R2R、REVERIE、SOON）：这些基准关注的是指令跟随和视觉-语言对齐，代理能力被视为常量。CapNav 首次将代理移动能力作为显式变量引入导航评估，揭示了 VLM 在能力感知推理上的系统性缺陷。
- **具身导航中的能力建模**：部分机器人导航工作考虑了运动学约束（如转弯半径、底盘尺寸），但通常以规划器或控制器的形式嵌入，而非作为 VLM 评估的维度。CapNav 将能力约束从底层控制提升到高层语义决策层面。
- **空间推理基准**（如 SpatialVLM、SpatialRGPT）：这些工作主要评估 VLM 对空间关系的理解，但未将代理自身尺寸作为推理条件。CapNav 的实验结果（Figure 5）表明，所有模型在需要隐式空间度量估计的障碍类型（狭窄通道、转弯半径）上表现明显更差，暴露了 VLM 在“以我之身度量世界”这一能力上的根本缺陷。

### 4. 适用边界与局限性

**数据集局限**：CapNav 目前仅包含 45 个室内场景（源自 HM3D 和 Matterport3D）、2365 个导航任务和 5075 条可通行性标注。场景规模和布局多样性有限，难以覆盖极端空间约束（如极窄走廊、复杂多楼层结构）和动态障碍物场景。

**代理类型有限**：仅覆盖五种典型移动能力（无运动障碍成人、轮椅使用者、人形机器人、四足机器人、扫地机器人），未涉及更多实际移动辅助设备（如拐杖、助行器）或临时能力状态（如手持重物、推婴儿车）。代理配置的物理参数（如宽度 0.6m 的轮椅）是否具有充分代表性，需要更多实际用户数据验证。

**视觉输入瓶颈**：实验明确显示（Figure 6），增加输入帧数带来的性能提升随模型而异且趋于饱和，这被归因为“视觉整合瓶颈”。这一发现暗示，仅靠增加视觉信息量无法解决空间度量推理问题——VLM 缺乏将多帧 2D 观测转化为精确 3D 几何度量的内在机制。

**微调代价**：对 Qwen3-VL-8B 进行 LoRA 微调后，CapNav 分数从 45.26 提升至 55.18，但推理有效性从 0.30 降至 0.25。这表明当前微调策略可能促使模型学习统计捷径（如记忆场景-能力关联），而非真正提升空间推理能力，导致可解释性退化。

### 5. 开放问题与未来方向

基于上述局限，以下几个方向值得关注：

1. **空间信息注入机制**：如何将显式的空间表征（深度图、点云、拓扑先验、栅格地图）注入 VLM 的推理流程，以弥补其对空间尺寸的忽视？可能的路径包括多模态融合编码器、空间 token 化策略或外部空间记忆模块。

2. **能力感知的强化学习调优**：能否设计以能力约束为显式奖励信号的 RL 调优方案？具体而言，将 RTA 或边级别的可通行性判断作为密集奖励，可能比端到端的任务完成信号更有效地提升模型对行走空间和转弯半径的敏感度。

3. **长视频空间理解**：视觉整合瓶颈的突破可能需要改进多帧信息的融合机制——例如引入时空注意力、关键帧选择策略或显式的 3D 重建中间表示——使 VLM 在长视频中能保持稳定的空间理解。

4. **更大规模与多样化的数据集**：当前 45 个场景的规模限制了统计结论的稳健性和模型泛化能力的评估。建立覆盖更多建筑类型、文化背景、动态环境和临时障碍物的能力约束导航数据集，是推动该方向发展的必要条件。

5. **与机器人系统的闭环验证**：CapNav 目前是离线评估，模型的输出路径未在真实或仿真环境中执行。将 VLM 的能力感知决策与底层导航栈（如局部规划器、SLAM）集成并进行闭环测试，将是验证其实际效用的关键一步。

## 原文 PDF

![[paperPDFs/CVPR_2026/CapNav_Benchmarking_Vision_Language_Models_on_Capability_conditioned_Indoor_Navigation.pdf]]
