---
title: "MSGNav: Unleashing the Power of Multi-modal 3D Scene Graph for Zero-Shot Embodied Navigation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MSGNav_Unleashing_the_Power_of_Multi_modal_3D_Scene_Graph_for_Zero_Shot_Embodied_Navigation.pdf
project_link: null
code_link: null
aliases:
- MSGNav
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 用动态分配的多模态图像边替代纯文本边，直接在场景图中保留原始视觉证据。
primary_logic: 通过在3D场景图的边上存储共现对象的RGB-D图像，可以保留未失真的空间与外观信息，使视觉语言模型能够进行可靠的开放词汇关系推理，并显著提升对感知误差的鲁棒性。
claims:
- 引入多模态场景图（M3DSG）在GOAT-Bench上相比纯节点基线使成功率（SR）提升15.0%，路径加权成功率（SPL）提升7.8%。
- M3DSG相比传统文本关系图（Concept-graph）在GOAT-Bench上取得更高成功率（60.0 vs 56.2）。
- 完整的MSGNav在GOAT-Bench上达到52.0% SR，显著超越先前最佳零样本方法TANGO (32.1%) 和训练型方法MTU3D (47.2%)。
- 可见性视点决策（VVD）模块将标准成功阈值（0.25m）下的成功率从33.91%大幅提升至51.97%。
---

# MSGNav: Unleashing the Power of Multi-modal 3D Scene Graph for Zero-Shot Embodied Navigation

> [!tip] 核心洞察
> 通过在3D场景图的边上存储共现对象的RGB-D图像，可以保留未失真的空间与外观信息，使视觉语言模型能够进行可靠的开放词汇关系推理，并显著提升对感知误差的鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | MSGNav：释放多模态3D场景图在零样本具身导航中的能力 |
| 英文题名 | MSGNav: Unleashing the Power of Multi-modal 3D Scene Graph for Zero-Shot Embodied Navigation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.10376) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MSGNav |
| Dataset | GOAT-Bench Val Unseen, HM3D-ObjNav |

> [!tip] 效果简介
> - GOAT-Bench Val Unseen 上，SR 52.0 vs 47.2 (MTU3D) (+4.8)；SPL 29.6 vs 27.7 (MTU3D) (+1.9)；SR 52.0 vs 32.1 (TANGO) (+19.9)。
> - HM3D-ObjNav 上，SR 74.1 vs 72.2 (WMNav) (+1.9)；SPL 33.4 vs 33.3 (WMNav) (+0.1)。

## 概要

具身导航中，智能体需要在陌生环境中理解开放词汇的语义目标并规划路径。传统方法依赖**纯文本关系边**构建3D场景图来表示对象间关系，但这导致三个关键瓶颈：**视觉信息丢失**（“on top of”无法传达具体空间布局）、**构建成本高昂**（需为每对对象生成文本描述）、以及**词汇受限**（固定词汇表难以覆盖开放世界目标），严重阻碍零样本导航的泛化能力。

MSGNav 的核心洞察是：**用动态分配的多模态图像边替代纯文本边，直接在场景图的边上存储共现对象的RGB-D图像**，从而保留未失真的空间与外观信息。这一设计使视觉语言模型（VLM）能够进行可靠的开放词汇关系推理，并显著提升对感知误差的鲁棒性。

围绕这一思想，MSGNav 构建了完整的零样本导航系统，包含五个关键模块：**多模态3D场景图构建（M3DSG）** 从RGB-D观测增量构建对象节点和图像边关系；**关键子图选择（KSS）** 压缩场景图以降低VLM推理成本；**自适应词汇更新（AVU）** 利用VLM和视觉证据动态扩展词汇表；**闭环推理（CLR）** 记忆历史决策以提升推理一致性；以及**基于可见性的视点决策（VVD）**，通过3D射线投射分析候选视点的遮挡程度，解决“最后一公里”问题——即目标定位后如何选择最佳观测视点。

**主要结果：** 在GOAT-Bench的Val Unseen划分上，MSGNav以**52.0%成功率（SR）** 显著超越先前最佳零样本方法TANGO（32.1%）和训练型方法MTU3D（47.2%）。在HM3D-ObjNav上同样达到领先的74.1% SR。消融实验验证了各模块的独立贡献：引入M3DSG相比纯节点基线使SR提升**15.0%**，在此基础上加入VVD模块进一步带来**12.5% SR**的提升；VVD模块在标准成功阈值（0.25m）下将成功率从33.91%大幅提升至**51.97%**。

具身导航要求智能体在陌生环境中根据自然语言指令定位目标物体，其核心挑战在于对复杂三维场景的开放词汇理解。现有方法大致分为两类：基于强化学习的训练型方法和基于视觉语言模型的零样本方法。训练型方法如 **MTU3D** (Gao et al., NeurIPS 2024) 虽在特定基准上表现良好，但受限于封闭词汇和固定训练范式，难以泛化到未见过的物体类别。零样本方法如 **TANGO** (Majumdar et al., 2023) 和 **WMNav** (Yokoyama et al., 2024) 利用大规模预训练模型绕过训练成本，但在复杂场景中的推理精度和路径效率仍显不足。

### 传统场景图的根本瓶颈

3D场景图作为环境的结构化表征，被广泛用于导航推理。然而，传统方法（如 Concept-graph）存在一个根本性瓶颈：**使用纯文本标签表示对象间关系边**。这种设计导致三个连锁问题：

1. **视觉信息丢失**：将丰富的空间-外观关系压缩为离散文本（如“top”、“beside”），不可逆地丢弃了原始视觉证据，使下游推理无法利用关键的空间细节。
2. **构建成本高昂**：为生成准确的文本关系边，需要复杂的空间推理管线，计算开销大且易出错。
3. **词汇受限**：文本关系边受限于预设的词汇表（如 ScanNet-200），无法描述开放世界中多样的物体关系，严重阻碍零样本理解。

### “最后一公里”问题

即使成功定位目标物体，现有方法通常选择距目标最近的可穿越位置作为最终导航点，忽略了**视点可见性**。当该位置被障碍物遮挡或视角不佳时，智能体无法有效观测目标，导致导航在最后阶段失败。本文将此称为“最后一公里”问题（last-mile problem），这是此前方法中未被充分识别和解决的关键失败模式。

### 本文动机

针对上述缺口，本文提出 **MSGNav**，一个基于多模态3D场景图（M3DSG）的零样本导航框架。其核心动机在于：**用动态分配的多模态图像边替代纯文本边，直接在场景图中保留原始视觉证据**，从而消除文本关系边的信息瓶颈。同时，通过基于可见性的视点决策模块解决“最后一公里”问题，实现从场景理解到最终导航的完整闭环。

## 核心方法与创新机理

MSGNav 的核心创新在于对传统 3D 场景图表示的根本性重构，以及针对导航“最后一英里”问题提出的视点决策机制。其技术贡献可凝练为以下四个关键维度的改变。

### 从文本边到多模态图像边的表示跃迁

传统 3D 场景图（如 Concept-graph）使用纯文本标签（如 “top”、“beside”）描述对象间空间关系。这一设计存在三重瓶颈：**（1）视觉信息丢失**——文本无法保留外观、纹理、遮挡等细粒度视觉线索；**（2）构建成本高昂**——需要复杂的空间关系解析器；**（3）词汇受限**——固定词汇表无法覆盖开放世界中的多样关系。

MSGNav 提出的**多模态 3D 场景图（M3DSG）** 将关系边替换为动态分配的多模态图像边集合。具体而言，对于空间距离小于阈值 θ 的每对对象，系统存储其共现的 RGB-D 图像作为边的表示。这一设计直接保留了原始视觉证据，使得视觉语言模型（VLM）能够基于未失真的空间与外观信息进行可靠的开放词汇关系推理，同时显著降低了对感知误差的敏感性。

> **证据支撑**：Table 4 显示，M3DSG 相比使用文本关系边的传统图（Concept-graph）在 GOAT-Bench 上成功率提升 3.8%（60.0 vs 56.2）。Table 3 的消融实验进一步表明，引入 M3DSG 相比纯节点基线使成功率（SR）提升 15.0%，路径加权成功率（SPL）提升 7.8%。

### 自适应词汇更新机制

传统方法依赖固定预设词汇（如 ScanNet-200），无法应对零样本导航中出现的任意开放词汇目标。MSGNav 引入**自适应词汇更新（AVU）** 模块：系统首先以 ScanNet-200 初始化词汇表 $V_{t=0}$，在探索过程中，VLM 检查 M3DSG 中的图像边和对象节点，动态提出所需的新词汇 $\hat{V}_t$ 并加入词汇表。这一机制使场景图能够持续扩展其语义覆盖范围，从根本上突破了固定词汇表的限制。

### 闭环推理与决策记忆

传统零样本导航方法通常采用无记忆的逐次决策，缺乏对历史探索行为的反思能力。MSGNav 的**闭环推理（CLR）** 模块将历史决策响应 $\mathcal{R}_{t-1}$ 存储在决策记忆库 $\mathbf{M}_t$ 中，并在后续的 VLM 查询中作为上下文输入：

$$\mathcal{R}_t, \hat{V}_t = \mathrm{VLM}(\mathbf{S}^k, \mathbf{M}_t, \mathbf{F}, g, t)$$

这一设计使 VLM 能够回溯已探索区域、避免重复搜索，并基于累积经验调整策略，显著提升了决策的一贯性和准确率。

### 基于可见性的视点决策

导航任务中存在一个被忽视的“最后一英里”问题：即使目标对象已被准确定位，传统方法仅选择距目标最近的可穿越位置作为最终导航点，却忽略了该位置可能因遮挡而无法有效观测目标。MSGNav 的**基于可见性的视点决策（VVD）** 模块通过在目标周围均匀采样候选视点，并利用 3D 射线投射评估各视点与目标点云之间的遮挡程度，计算可见性得分，最终选择得分最高的视点作为导航坐标。

> **证据支撑**：Table 5 显示，VVD 模块在标准成功阈值（0.25m）下将成功率从 33.91% 大幅提升至 51.97%。Table 3 的消融实验表明，在 M3DSG 基础上加入 VVD 可进一步带来 12.5% SR 和 6.7% SPL 的提升。

### 关键子图选择：效率保障

为降低 VLM 的推理成本，MSGNav 设计了**关键子图选择（KSS）** 模块，通过“压缩—聚焦—剪枝”三阶段流程从完整的 M3DSG 中提取与任务最相关的子图 $\mathbf{S}^k$。这一设计并非核心表示创新，但为前述模块的高效运行提供了必要的计算可行性保障。

MSGNav 构建了一个连续的“感知—推理—行动”闭环系统，其核心是一个增量式更新的**多模态3D场景图（M3DSG）**。如图 Figure 3 所示，在每一个时间步 $t$，智能体根据当前接收到的 RGB-D 观测 $\mathcal{T}_t$ 和自身位姿，对场景图 $\mathbf{S}_{t-1}$ 进行增量更新，得到 $\mathbf{S}_t$。这一更新过程可形式化为：

![[assets/figures/papers/paper_list_l2641_https_arxiv_org_abs_2511_10376/figures/003_Figure_3.jpg]]
*Figure 3: The overall framework of our MSGNav. At time step t, the agent incrementally constructs the scene graph*

$$\mathbf{S}_t = \mathcal{M}(\mathbf{S}_{t-1}, \mathcal{T}_t), \quad t \in [1, T], \quad \mathbf{S}_0 = (\emptyset, \emptyset)$$

场景图 $\mathbf{S}_t$ 包含一组带有视觉、空间和房间属性的对象节点 $\mathbf{O}_t$，以及一组描述对象间关系的图像边 $\mathbf{E}_t$。与传统3D场景图使用纯文本关系边不同，M3DSG 在边上直接存储共现对象的 RGB-D 图像，从而保留未失真的空间与外观信息，为后续的开放词汇推理提供原始视觉证据。

在此基础上，系统依次通过四个核心模块对场景图进行处理和推理：

1. **关键子图选择（KSS）**：对完整场景图进行“压缩—聚焦—剪枝”操作，提取与导航目标 $g$ 最相关的子图 $\mathbf{S}^k$，大幅降低 VLM 的推理成本。
2. **自适应词汇更新（AVU）**：以 ScanNet-200 初始化词汇表 $V_{t=0}$，在探索过程中由 VLM 检查图像边 $\mathbf{E}_t$ 和对象集 $\mathbf{O}_t$，动态提出所需的新词汇 $\hat{V}_t$，支持开放词汇目标。
3. **闭环推理（CLR）**：将历史决策响应存储于记忆库 $\mathbf{M}_t$ 中，并与关键子图 $\mathbf{S}^k$、前沿图像 $\mathbf{F}$ 和目标 $g$ 一同输入 VLM，进行带记忆反馈的推理查询：

   $$\mathcal{R}_t, \hat{V}_t = \mathrm{VLM}(\mathbf{S}^k, \mathbf{M}_t, \mathbf{F}, g, t)$$

   推理响应 $\mathcal{R}_t$ 指导智能体选择目标对象或探索前沿。
4. **基于可见性的视点决策（VVD）**：当目标对象 $\bar{o}$ 被定位后，VVD 在其周围以多尺度半径 $R = \{r_j\}$ 均匀采样候选视点，通过射线投射评估每个候选视点与目标点云之间的遮挡程度，计算可见性得分，最终选择得分最高的视点 $v_{\text{best}}$ 作为导航终点坐标。

这一框架将场景表示、词汇扩展、决策记忆和视点优化有机整合，使得零样本导航系统能够在复杂环境中进行更全面且上下文感知的场景理解。详细的端到端处理流程可参见 Figure 7。

![[assets/figures/papers/paper_list_l2641_https_arxiv_org_abs_2511_10376/figures/014_Figure_7.jpg]]
*Figure 7: Detailed end-to-end processing flow of the proposed framework. The system executes a continuous sense-reason-act loop across four key stages: (1) multi-modal 3D scene graph construction via Vision Foundation Models (VFMs), (2) closed-loop reasoning based on the extracted sub-graph*

MSGNav 的核心创新在于多模态3D场景图（M3DSG）的构建以及围绕其设计的四个推理模块。以下按系统流程逐一阐述关键模块及其公式。

### 多模态3D场景图（M3DSG）构建

M3DSG 的核心思想是用**动态分配的多模态图像边**替代传统3D场景图中纯文本的关系边。传统方法（如 Concept-graph）使用“top”、“beside”等固定词汇描述对象关系，导致视觉信息丢失和词汇受限。M3DSG 改为在边上存储共现对象的 RGB-D 图像，直接保留原始视觉证据。

场景图 $S_t$ 的增量更新公式为：

$$\mathbf{S}_t = \mathcal{M}(\mathbf{S}_{t-1}, \mathcal{T}_t), \quad t \in [1, T], \quad \mathbf{S}_0 = (\emptyset, \emptyset)$$

其中 $\mathcal{T}_t$ 为当前时刻的 RGB-D 观测，$\mathcal{M}$ 为更新函数。$S_t$ 包含对象节点集合 $O_t$ 和图像边集合 $E_t$。

对象节点的更新依赖视觉基础模型（VFMs）：YOLO-W 用于开放词汇检测，SAM 用于实例分割，CLIP 用于提取视觉嵌入。帧级对象集 $O_t^{\text{frame}}$ 经匹配与合并后形成全局对象集：

$$\mathbf{O}_t = \Phi_{\text{merge}}(\Phi_{\text{match}}(\mathbf{O}_t^{\text{frame}}, \mathbf{O}_{t-1})) \cup \mathbf{O}_t^{\text{frame}}$$

图像边的数量由空间距离阈值 $\theta$ 决定：

$$N_e = \sum_{1 \leq x < y \leq N_o} \mathbb{1}_{\|\text{Pos}_{o_x} - \text{Pos}_{o_y}\| < \theta}$$

### 关键子图选择（KSS）

为降低 VLM 推理成本，KSS 采用“压缩—聚焦—剪枝”三阶段流程，从完整场景图中提取与导航目标 $g$ 最相关的关键子图 $\mathbf{S}^k$。随后 VLM 基于该子图和前沿图像 $\mathbf{F}$ 进行查询：

$$\mathcal{R}_t = \mathrm{VLM}(\mathbf{S}^k, \mathbf{F}, g, t)$$

查询结果 $\mathcal{R}_t$ 指示下一步应探索的前沿或已定位的目标对象。

### 自适应词汇更新（AVU）

AVU 解决了传统固定词汇表（如 ScanNet-200）无法覆盖开放世界目标的问题。系统初始词汇表 $V_{t=0}$ 为 ScanNet-200，在探索过程中，VLM 检查图像边 $E_t$ 中的视觉证据，动态提出所需的新词汇。更新后的查询公式为：

$$\mathcal{R}_t, \hat{V}_t = \mathrm{VLM}(\mathbf{S}^k, \mathbf{F}, g, t)$$

其中 $\hat{V}_t$ 为当前步提议的新词汇，用于扩展词汇表。

### 闭环推理（CLR）

CLR 引入决策历史记忆 $M_t$，存储前序步骤的探索响应，使 VLM 能够参考历史决策进行更一致的推理：

$$\mathcal{R}_t, \hat{V}_t = \mathrm{VLM}(\mathbf{S}^k, \mathbf{M}_t, \mathbf{F}, g, t)$$

这一闭环机制有效避免了重复探索和矛盾决策。

### 基于可见性的视点决策（VVD）

VVD 针对“最后一公里”问题：目标定位后，传统方法选择最近的可穿越位置，常因遮挡导致导航失败。VVD 在目标 $\bar{o}$ 周围以多半径 $R = \{r_j\}_{j=1}^{N_R}$ 均匀采样候选视点，通过射线投射评估每个候选视点与目标点云 $PC_{\bar{o}}$ 之间的遮挡程度，计算可见性得分。最终选择得分最高的视点 $v_{\text{best}}$ 作为导航终点。该模块将标准成功阈值（0.25m）下的成功率从 33.91% 大幅提升至 51.97%（Table 5）。

## 实验与关键发现

### 主要结果

MSGNav在两个主流具身导航基准上均取得了最优性能。在GOAT-Bench的Val Unseen划分上，MSGNav以52.0%的成功率（SR）和29.6%的路径加权成功率（SPL）显著超越所有对比方法（Table 1）。具体而言，相比先前最佳的零样本方法**TANGO**，SR提升19.9个百分点（32.1%→52.0%）；相比先前最佳的训练型方法**MTU3D**，SR提升4.8个百分点（47.2%→52.0%），SPL提升1.9个百分点（27.7%→29.6%）。这表明MSGNav的零样本范式不仅大幅领先同类零样本方法，还超越了依赖大量训练数据的强化学习方法。

![[assets/figures/papers/paper_list_l2641_https_arxiv_org_abs_2511_10376/figures/005_Table_1.jpg]]
*Table 1: Experiments on the “Val Unseen” split of GOAT-Bench. “†” denotes the results we reproduced due to different settings*

在HM3D-ObjNav基准上，MSGNav同样取得74.1% SR和33.4% SPL（Table 2），略微领先先前的零样本最佳方法**WMNav**（72.2% SR, 33.3% SPL），验证了方法的跨基准泛化能力。

![[assets/figures/papers/paper_list_l2641_https_arxiv_org_abs_2511_10376/figures/006_Table_2.jpg]]
*Table 2: Experiments on the HM3D-ObjNav benchmark*

### 消融研究

#### 模块贡献分析

Table 3的逐模块消融实验揭示了各组件的独立贡献。基线模型**3D-Mem**（纯文本关系图）仅取得33.5% SR和20.5% SPL。在此基础上引入多模态场景图（M3DSG）使SR跃升15.0个百分点至48.5%，SPL提升7.8个百分点至28.3%，直接验证了图像边替代文本边这一核心设计决策的有效性。进一步叠加基于可见性的视点决策（VVD）模块后，SR再提升12.5个百分点至61.0%，SPL提升6.7个百分点至35.0%，证实了“最后一公里”问题对导航成功的显著制约。自适应词汇更新（AVU）和闭环推理（CLR）模块的加入进一步带来增益，使完整系统达到最优性能。

#### 场景图表示消融

Table 4将M3DSG与两种替代表示进行对比：纯节点图（Node-only，即Concept-graph去除关系边）和传统文本关系图（Traditional graph，即Concept-graph）。M3DSG取得60.0% SR，相比传统文本关系图的56.2%提升3.8个百分点，相比纯节点图的52.7%提升7.3个百分点。这一梯度式提升表明：（1）关系信息本身对导航至关重要；（2）图像边所保留的视觉证据比文本标签包含更丰富的空间与外观信息，使VLM能进行更可靠的开放词汇关系推理。

#### VVD模块的深度分析

Table 5在不同成功距离阈值下评估VVD模块的效果。在标准0.25m阈值下，VVD将SR从33.91%大幅提升至51.97%，提升幅度达18.06个百分点。随着成功阈值放宽至1.0m，VVD的增益逐渐缩小（从33.91%→51.97%到66.51%→74.05%），但仍保持正向贡献。这说明VVD的核心价值在于将导航终点从“距目标最近的可行走点”优化为“对目标具有最大可见性的视点”，从而在严格精度要求下发挥关键作用。

Figure 5的盒须图统计进一步揭示了VVD的决策机制：高可见性得分的候选视点与真值视点（GT）的距离显著更小，验证了可见性评分与导航精度之间的正相关关系。

#### VLM选择的影响

Table 9展示了不同VLM后端对MSGNav性能的影响。GPT-4o作为默认VLM取得最佳性能，而替换为其他VLM时性能出现不同程度下降，表明VLM的视觉-语言理解能力是系统性能的重要上限因素。

### 失败模式与局限性

尽管MSGNav取得了显著的性能提升，分析实验结果和论文讨论可归纳出以下失败模式：

1. **感知基础模型的误差传播**：M3DSG的构建依赖于YOLO-W、SAM、CLIP等VFMs的检测、分割和嵌入质量。当这些模型出现漏检、误分类或分割不完整时，场景图中的节点和图像边将携带错误信息，导致VLM推理偏差。这一问题在目标类别超出预训练分布时尤为突出。

2. **“最后一公里”问题的残余**：VVD模块虽大幅缓解了最终视点选择问题，但在复杂动态遮挡场景（如目标被多个物体部分遮挡）下仍可能失效。射线投射方法假设场景完全静态，无法处理移动物体或临时遮挡。

3. **推理延迟**：系统串行调用多个大型预训练模型，单步决策耗时较高，尚未满足实时部署需求。论文未报告具体的端到端延迟数据，但指出这是实际应用的主要瓶颈。

4. **动态环境未覆盖**：当前系统仅针对静态环境设计，未考虑场景中对象的移动、新增或消失。在长期部署场景中，M3DSG需要引入图更新与遗忘机制。

### 关键实验结论

综合以上分析，实验部分的核心结论可归纳为：

- **图像边是场景图表示的关键突破**：M3DSG通过将对象关系存储为原始RGB-D图像而非文本标签，保留了未失真的空间与外观信息，使VLM能够进行可靠的开放词汇关系推理，这是性能提升的根本原因。
- **VVD解决了导航的“最后一公里”瓶颈**：将视点选择从距离最小化转变为可见性最大化，在严格精度要求下贡献了超过18个百分点的SR提升，且其决策与GT视点高度一致。
- **模块协同产生累积增益**：KSS、AVU、CLR、VVD四个模块各自针对效率、词汇覆盖、决策一致性和最终精度四个维度，叠加后产生显著的协同效应。
- **零样本范式超越训练型方法**：MSGNav无需任何导航训练数据，仅依赖预训练VFMs和VLM，在GOAT-Bench上超越训练型SOTA方法MTU3D，展示了基础模型驱动的零样本导航范式的巨大潜力。

![[assets/figures/papers/paper_list_l2641_https_arxiv_org_abs_2511_10376/figures/007_Table_3.jpg]]
*Table 3: Component ablation experiment across the first episode of each scene on the “Val Unseen” split of GOAT-Bench. The first row without any module, which represents our baseline model 3D-Mem [43] results. “VVD”, “AVU”, and “CRV” represent the Visibility-based Viewpoint Decision module, Adaptive Vocabulary Update module, and Closed-loop Reasoning and Verification module*

![[assets/figures/papers/paper_list_l2641_https_arxiv_org_abs_2511_10376/figures/002_Figure_2.jpg]]
*Figure 2: Performance comparisons between our MSGNav and other existing methods for embodied navigation on Goat-Bench [19]: the multi-modal open-vocabulary navigation benchmark. (a) The superiority of our M3DSG over traditional 3D scene graphs. (b) Distance statistics from the goal for the previous method (3D-Mem [43] as an example). (c) Our MSGNav system achieves stateof-the-art performance on the challenging Goat-Bench*

## 定位与知识库关联

### 与现有基线方法的关系

MSGNav 的核心创新在于将传统 3D 场景图的**纯文本关系边**替换为**动态分配的多模态图像边**，从而在零样本具身导航任务中释放视觉语言模型（VLM）的开放词汇推理能力。这一设计使其在方法谱系中处于图基导航与多模态感知的交叉点。

**与传统图基方法的对比。** 早期图基导航方法如 **Concept-graph** 使用固定词汇的文本关系边（如“top”、“beside”）描述对象间空间关系，导致视觉信息大量丢失，且词汇受限。消融实验（Table 4）表明，M3DSG 相比 Concept-graph 在 GOAT-Bench 上成功率提高了 3.8%（60.0 vs 56.2），而纯节点图（无关系边）性能更低。这验证了图像边在保留未失真的空间与外观信息方面的决定性作用。

**与零样本方法的对比。** 在 GOAT-Bench 上，MSGNav 以 52.0% SR 显著超越先前最佳零样本方法 **TANGO**（32.1% SR），提升幅度达 19.9 个百分点（Table 1）。TANGO 依赖文本描述进行目标推理，缺乏对场景结构的显式图建模，而 MSGNav 通过 M3DSG 将视觉证据直接编码到图结构中，使 VLM 能够进行可靠的开放词汇关系推理。

**与训练型方法的对比。** 即使与需要大量训练的 **MTU3D**（先前 GOAT-Bench 最佳）相比，MSGNav 作为零样本方法仍实现了 4.8% SR 和 1.9% SPL 的领先（52.0 vs 47.2, 29.6 vs 27.7）。在 HM3D-ObjNav 上，MSGNav 同样以 74.1% SR 超越先前最佳零样本方法 **WMNav**（72.2% SR），达到与训练型方法可比甚至更优的性能。这表明精心设计的场景表示可以弥补甚至超越端到端训练带来的先验知识。

**与 3D-Mem 的消融关系。** 消融实验（Table 3）以 **3D-Mem** 作为基线（无任何 MSGNav 模块），其使用纯文本关系边和固定词汇。引入 M3DSG 后 SR 提升 15.0%，SPL 提升 7.8%；进一步加入 VVD 模块再带来 12.5% SR 和 6.7% SPL 的增益。这清晰地建立了从传统图基方法到 MSGNav 的因果链路：**图像边 → 开放词汇推理能力 → 视点优化 → 最终性能提升**。

### 适用边界与局限

尽管 MSGNav 在两个主流基准上取得了领先结果，其设计存在明确的适用边界：

1. **静态环境假设。** M3DSG 的增量构建依赖于场景结构的稳定性，当前系统未考虑移动物体或环境的长期变化。在动态家庭或办公场景中，过时的图像边可能导致 VLM 推理错误。

2. **感知基础模型的依赖链。** 系统依赖 YOLO-W（开放词汇检测）、SAM（实例分割）、CLIP（视觉嵌入）等多个大型预训练模型的级联输出。任一环节的检测遗漏或分割错误都会传播至场景图，造成对象节点缺失或关系边分配错误。论文未量化这种级联误差的影响。

3. **推理延迟约束。** 系统集成了 GPT-4o 等 VLM 进行在线推理，结合 VFMs 的前向传播，单步决策延迟较高。论文明确指出“尚未满足实时部署需求”，当前系统更适合离线或准在线场景。

4. **最后阶段问题的残余风险。** VVD 模块通过射线投射评估候选视点的遮挡程度，在标准 0.25m 成功阈值下将 SR 从 33.91% 提升至 51.97%（Table 5），但在复杂动态遮挡（如窗帘飘动、门开关）下仍可能失效。Figure 5 的盒须图显示，VVD 高评分视点与 GT 视点的距离分布仍存在离群值，表明视点选择并非总是最优。

5. **词汇扩展的边界。** AVU 模块虽然支持自适应词汇更新，但其扩展能力受限于 VLM 对图像边内容的语义理解。对于极其罕见或高度特化的目标类别，VLM 可能无法准确提出新词汇，导致目标定位失败。

### 开放问题与未来方向

基于上述局限，以下几个方向值得进一步探索：

- **轻量化部署。** 能否通过模型蒸馏、特征缓存或边缘计算降低 VFMs/VLMs 的推理开销，使系统满足实时导航需求？例如，用更轻量的局部特征替代 CLIP 嵌入来加速场景图构建。

- **动态环境适应。** 如何扩展 M3DSG 以处理移动物体和长期场景变化？可能的思路包括引入时间衰减机制或结合强化学习进行主动感知更新。

- **主动视点优化。** 当前 VVD 是被动选择最优候选视点，能否结合主动感知策略，在导航过程中动态调整视角以最大化目标可见性？

- **感知鲁棒性增强。** 如何减轻基础模型级联误差对场景图一致性的影响？可能的方案包括多帧一致性检验、不确定性建模或端到端的图结构学习。

- **更大范围泛化。** M3DSG 的构建依赖于对象间的空间邻近性（距离阈值 θ），在大范围开放世界环境中如何高效管理图规模并保持推理质量，仍需验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/MSGNav_Unleashing_the_Power_of_Multi_modal_3D_Scene_Graph_for_Zero_Shot_Embodied_Navigation.pdf]]
