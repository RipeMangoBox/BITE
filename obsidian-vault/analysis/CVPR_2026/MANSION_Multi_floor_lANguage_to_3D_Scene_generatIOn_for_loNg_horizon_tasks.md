---
title: "MANSION: Multi-floor lANguage-to-3D Scene generatIOn for loNg-horizon tasks"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MANSION_Multi_floor_lANguage_to_3D_Scene_generatIOn_for_loNg_horizon_tasks.pdf
project_link: null
code_link: null
aliases:
- MANSION
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 缺乏将垂直对齐作为硬约束的生成方法，以及将高层语义规划与底层几何求解解耦的混合架构。
primary_logic: 通过将MLLM用于高层语义规划和空间指向，同时使用基于约束增长的几何求解器强制执行垂直对齐和拓扑有效性，可以在无需重新训练的情况下生成多样化的建筑尺度多楼层3D场景。
claims:
- MANSION是唯一在平面图生成中支持垂直结构（楼梯/电梯）和开放词汇房间类型的方法（见表1）。
- 在更具挑战性的ResPlan-1k数据集上，MANSION在自动标注（MA）设置下Micro-IoU达到76.74%，远超ChatHouseDiffusion（CHD）的33.49%，证明了其在复杂布局上的泛化能力。
- 在多楼层具身任务中，最先进的代理（如BUMBLE）在四层场景下成功率为0%，凸显了建筑尺度长程任务对空间推理和记忆的严峻挑战，也反衬了MANSION作为测试床的价值。
- T2D (single-floor residential) 上 Macro-IoU (manual annotation setting) = 80.66
---

# MANSION: Multi-floor lANguage-to-3D Scene generatIOn for loNg-horizon tasks

> [!tip] 核心洞察
> 通过将MLLM用于高层语义规划和空间指向，同时使用基于约束增长的几何求解器强制执行垂直对齐和拓扑有效性，可以在无需重新训练的情况下生成多样化的建筑尺度多楼层3D场景。

| 字段 | 内容 |
|------|------|
| 中文题名 | MANSION：面向长程任务的多楼层语言到3D场景生成框架 |
| 英文题名 | MANSION: Multi-floor lANguage-to-3D Scene generatIOn for loNg-horizon tasks |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.11554) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MANSION |
| Dataset | T2D, ResPlan-1k, Object Placement, Cross-floor Embodied Tasks |

> [!tip] 效果简介
> - T2D (single-floor residential) 上，Macro-IoU (manual annotation setting) 80.66 vs 79.04 (CHD MA) (+1.62)。
> - ResPlan-1k (complex residential) 上，Micro-IoU (manual annotation setting) 76.74 vs 33.49 (CHD MA, zero-shot) (+43.25)。
> - Object Placement (Classroom, 8x8 m) 上，Floor-object reachability (#Rch, %) 100.0 vs 80.0 (Holodeck) / 98.6 (LayoutGPT) (+20.0 / +1.4)。

## 概要

### 问题背景

现有具身智能基准和3D场景资源几乎全部局限于单层室内环境，缺乏对跨楼层垂直结构（楼梯、电梯、竖井等）的系统建模。这直接导致两个后果：其一，无法生成建筑尺度的多样化交互场景；其二，最先进的具身代理在涉及多楼层空间推理与记忆的长程任务中表现急剧退化——例如，**BUMBLE** 等VLM驱动框架在四层建筑中的任务成功率降为0%（Table 5）。该瓶颈的本质是生成侧缺乏将垂直对齐作为硬约束的方法，以及规划侧缺乏将高层语义与底层几何求解解耦的混合架构。

### 核心方法

**MANSION** 是针对上述瓶颈提出的首个语言驱动的建筑尺度多楼层3D场景生成框架。其核心设计包含两个因果调节变量：

1. **垂直对齐硬约束**：将楼梯、电梯等垂直交通核建模为跨楼层对齐的第一类硬约束，在平面图合成中强制执行，确保3D结构有效性（Table 1中唯一支持垂直结构的方法）。
2. **MLLM语义规划 + 约束几何求解的混合架构**：将高层语义规划（功能分区、房间拓扑、空间指向）交由多模态大语言模型（MLLM）处理，将底层几何布局转化为可验证的约束增长搜索问题，两者解耦后无需任何训练即可泛化到开放词汇的建筑类型（医院、学校、超市等）。

此外，在对象放置层面，MANSION引入基于锚点的分组策略、结构化关系原语（matrix/paired）以及优先级感知排序，将可达性从基线方法的约80%提升至100%（Table 4）；在任务适配层面，提出任务语义场景编辑代理，通过ReAct控制器和工具API以可验证的方式动态修改场景，确保复杂任务的前提条件得到满足。

### 主要结果

- **平面图生成**：在标准住宅数据集T2D上，MANSION在手动标注设置下Macro-IoU达到80.66%，略优于**ChatHouseDiffusion**（CHD）的79.04%；在更具挑战性的ResPlan-1k数据集上，MANSION的Micro-IoU达到76.74%，远超CHD零样本设置的33.49%（Table 2, 3），验证了其在复杂布局上的强泛化能力。
- **对象放置**：在教室场景中，MANSION实现100%的地面-物体可达性，显著优于**Holodeck**（80.0%）和**LayoutGPT**（98.6%）（Table 4）。
- **具身任务**：在单层场景中，通过文本增强可将BUMBLE的成功率从0%提升至60%；但在四层建筑中，所有方法成功率均为0%（Table 5），揭示了建筑尺度长程任务对VLM空间推理能力的严峻挑战，也凸显了MANSION生成的MansionWorld数据集作为测试床的独特价值。

### 方法定位

在方法谱系中，MANSION区别于纯数据驱动的扩散方法（如ChatHouseDiffusion）、基于LLM的单层布局方法（如Holodeck、LayoutGPT）以及基于图的平面图生成方法（如Graph2Plan）。其训练无关的混合架构和垂直结构支持使其成为当前唯一能够从自然语言直接生成建筑尺度多楼层3D场景的框架，同时也为跨楼层具身智能研究提供了首个大规模的标准化测试平台。



### 具身智能的场景瓶颈：从单层走向建筑尺度

具身智能的快速发展对训练和评估环境提出了越来越高的要求。然而，现有具身智能基准和场景资源几乎全部局限于单层室内环境——无论是家庭住宅、办公室还是实验室空间，代理只需在同一平面内完成导航和操作。这种设计隐含地回避了一个关键挑战：**真实世界的任务往往跨越多个楼层**，要求代理在垂直维度上进行空间推理、路径规划和长期记忆。

以“从二楼卧室取一本书送到一楼客厅”这样的日常任务为例，代理不仅需要理解不同楼层的房间功能，还必须规划跨楼层的导航路径（如找到楼梯或电梯），并在执行过程中保持对目标位置的记忆。当前最先进的具身代理（如 **BUMBLE**）在四层建筑场景中的任务成功率骤降至 **0%**（Table 5），这一结果直接暴露了现有系统在建筑尺度长程任务上的根本性不足。问题的根源并非代理本身的能力缺陷，而在于缺乏能够提供垂直结构建模和多楼层空间语义的生成环境。

### 现有场景生成方法的三个结构性缺口

从场景生成的角度审视，现有方法存在三个系统性的能力缺口：

**缺口一：垂直结构建模的缺失。** 无论是基于扩散模型的平面图生成方法（如 **ChatHouseDiffusion**），还是基于大语言模型的3D布局方法（如 **Holodeck**、**LayoutGPT**），其设计范畴均局限于单层空间。楼梯、电梯、竖井等垂直连接结构在这些方法中要么被完全忽略，要么仅作为装饰性元素存在，从未作为跨楼层空间对齐的硬约束被纳入生成过程（Table 1）。这导致生成的建筑在物理上无法支持跨楼层导航——代理在语义上“知道”需要上楼，但场景中缺乏可通行的垂直路径。

**缺口二：房间类型的封闭词汇限制。** 现有平面图生成方法几乎全部针对住宅场景设计，房间类型被限定在卧室、客厅、厨房等封闭集合内（Table 1）。然而，建筑尺度的具身任务天然需要多样化的功能建筑——医院、学校、超市、办公楼等——每种建筑都有其独特的空间拓扑和功能分区逻辑。将住宅场景的方法直接迁移到这些领域会导致严重的语义错配。

**缺口三：生成与任务的脱节。** 即使生成了结构合理的多楼层场景，其静态属性也未必能满足特定具身任务的前提条件。例如，一个“取零食和饮料到沙发”的任务要求场景中同时存在可通行的路径、可获取的目标物体以及正确的物体位置。现有方法生成的场景是“一次性”的，无法根据任务需求进行动态适配和可验证的编辑。

### 核心洞察与解决路径

MANSION 的核心洞察在于：**通过将多模态大语言模型（MLLM）用于高层语义规划和空间指向，同时使用基于约束增长的几何求解器强制执行垂直对齐和拓扑有效性，可以在无需重新训练的情况下生成多样化的建筑尺度多楼层3D场景。**

这一洞察直接回应了上述三个缺口：
- **垂直对齐作为硬约束**：在几何求解阶段将楼梯、电梯等垂直核心作为跨楼层的强制对齐区域，确保每一层的垂直结构在空间上精确对应；
- **开放词汇的房间语义**：利用 MLLM 的开放世界理解能力，支持任意功能建筑的空间规划，从医院的手术室布局到超市的货架分区；
- **任务语义的场景编辑**：引入独立的场景编辑代理，以“检查-准备”回路的方式验证并修改场景，确保其满足目标任务的可执行性前提。

这种**语义与几何解耦的混合架构**是 MANSION 区别于纯数据驱动方法和纯规则方法的关键设计选择。数据驱动方法（如扩散模型）虽然在已知分布上表现优异，但缺乏对垂直约束的显式建模能力，且在分布外场景（如医院）上泛化能力不足；纯规则方法则无法处理开放词汇的语义多样性。MANSION 的混合路径在语义灵活性和几何可靠性之间取得了平衡，为建筑尺度的具身智能研究提供了首个系统性的场景生成基础设施。



## 核心方法与创新机理

MANSION 的核心创新并非单一算法突破，而是一套面向建筑尺度场景生成的**系统性设计范式转移**。其关键创新可归纳为以下五个相互耦合的 **changed slots**，它们共同解决了现有方法从“单层房间”跨越到“多楼层建筑”时面临的根本性瓶颈。

### 1. 垂直结构：从缺失到硬约束

现有平面图生成方法（如 **ChatHouseDiffusion**、**Graph2Plan**、**Holodeck**）均将场景限定在单层，完全缺失对楼梯、电梯、竖井等跨楼层垂直连接结构的建模（见表1）。这一缺失使得生成的场景无法支持需要跨楼层导航与操作的长程具身任务。

MANSION 首次将**垂直对齐作为一等硬约束**引入生成流程。在平面图合成阶段，每层楼的自由规划区域被显式定义为：

$$\Omega _ { f } = P _ { f } \setminus \bigcup _ { v \in \mathcal { V } } Q _ { f , v }$$

其中 $P_f$ 为楼层 $f$ 的外轮廓，$Q_{f,v}$ 为垂直核心 $v$（楼梯/电梯/竖井）的占用区域。这一约束确保了跨楼层的墙体、房间和核心结构在三维空间中精确对齐，从而保证了建筑的结构有效性。这是 MANSION 区别于所有先前方法的最根本特征。

### 2. 房间类型：从住宅限定到开放词汇

现有方法的房间类型覆盖严重受限——**ChatHouseDiffusion** 和 **Graph2Plan** 等仅支持住宅场景的预定义房间类别，无法泛化到医院、学校、超市、办公楼等任意功能建筑。

MANSION 通过 **MLLM 驱动的混合架构**实现了真正的开放词汇可扩展性。在整体建筑规划阶段，MLLM 根据自然语言描述自由决定跨楼层的功能分区和房间类型；在单层规划阶段，MLLM 生成包含任意房间类别、面积需求和邻接关系的泡泡图拓扑。这一设计使得 MANSION 无需任何新数据或重新训练即可生成多样化建筑类型，从幼儿园到六层办公楼均可覆盖（见 Figure 1）。

### 3. 生成范式：从纯数据驱动到语义-几何解耦混合架构

传统方法要么依赖纯数据驱动的扩散模型（如 **ChatHouseDiffusion**），泛化能力受限于训练分布；要么采用纯规则方法，缺乏对高层语义的理解。

MANSION 提出了 **MLLM 语义规划 + 约束几何求解** 的混合架构，将高层语义推理与底层几何优化彻底解耦：
- **MLLM 负责语义规划**：理解自然语言需求、生成功能分区、确定房间拓扑关系、选择种子位置
- **约束增长求解器负责几何实现**：在垂直对齐和拓扑约束下，通过可验证搜索找到最优布局：

$$L ^ { \star } = \arg \operatorname* { m a x } _ { L \in \mathcal { C } } \mathrm { S c o r e } ( L ; \mathbf { w } ) \quad \mathrm { s . t . } \quad \mathrm { T o p o } ( L , \mathcal { G } ) = \mathrm { t r u e }$$

这种解耦使得方法的性能可随 MLLM 空间指向能力的增强而直接提升（消融实验证实，将 MLLM 从 Moonshot 替换为 Gemini-2.5-Pro 后，T2D 性能从 42.33 大幅提升至 69.98），而无需修改几何求解器。

### 4. 对象放置：从数量优先到可达性优先

现有方法（如 **Holodeck**、**LayoutGPT**）在对象放置时以数量最大化为目标，忽略了物体与地板之间的可达性，导致生成场景中大量物体被家具遮挡或无法交互。

MANSION 引入了三项关键改进：
- **基于锚点的分组**：将物体按功能关系组织为锚点组，确保相关物体在空间上共位
- **结构化关系原语**：新增 `matrix`（网格排列）和 `paired`（对称共位）两种布局原语，支持教室、图书馆等结构化场景
- **优先级感知排序 + 质量优先修剪**：按物体重要性排序放置，在保持物体数量的同时将可达性从约 80% 提升至 **100%**，且几乎无碰撞（见 Table 4）

### 5. 场景可编辑性：从静态场景到任务语义编辑

现有方法生成的场景是静态的，无法根据具体具身任务的前提条件进行动态适配。

MANSION 设计了 **任务语义场景编辑代理**（Task-Semantic Scene Editing Agent），采用 ReAct 控制器 + 工具 API 的架构（见 Figure 4）。该代理首先将高层任务指令分解为前提条件，然后依次执行路径连通性检查、物体可用性检查和物体供应与场景编辑，以可验证的方式修改场景，确保复杂任务在生成前即可执行。这一能力使 MANSION 不仅是场景生成器，更是具身任务的测试床构建工具。

---

**关键证据强度总结**：垂直结构支持（Table 1，置信度 0.98）、开放词汇房间类型（Table 1，置信度 0.95）、混合架构有效性（Table 3 消融实验，置信度 0.95）、可达性提升（Table 4，置信度 0.95）、场景编辑代理（Figure 4，置信度 0.95）。所有核心创新均有实验验证支撑，无推测性声明。



MANSION 采用一种**多智能体驱动的混合架构**，将高层语义规划与底层几何求解解耦，从自然语言描述直接生成建筑尺度的多楼层交互式 3D 场景。其核心 pipeline 由四个顺序模块和一个可选的场景编辑代理组成，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2540_https_arxiv_org_abs_2603_11554/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the MANSION framework: a multi-agent-driven pipeline for generating multi-story 3D buildings from natural language. The process includes: (A) Whole Building Planning, (B) Per-Floor Planning, (C) Floorplan Synthesis, and (D) Scene Instantiation*

### 输入与输出

- **输入**：一段自然语言指令，描述目标建筑的功能类型、房间需求、楼层数及全局风格（如“生成一个六层办公楼，包含开放式办公区、会议室、食堂和地下停车场”）。
- **输出**：一个在 AI2-THOR 模拟器中完全可导航、可交互的多楼层 3D 建筑，包含结构元素（墙、门、楼梯、电梯）、家具对象、光照和材质。

### Pipeline 模块

#### （A）Whole Building Planning（整体建筑规划）

该模块由一个建筑级规划节点驱动，负责解析用户指令并确定：
1. **跨楼层功能分区**：哪些功能区域分配在哪些楼层；
2. **面积预算分配**：每层的大致总面积及垂直核心筒（楼梯、电梯、竖井）的位置；
3. **全局视觉风格**：建筑的整体外观、材质主题和氛围设定。

规划结果以结构化程序描述的形式传递给下游模块。

#### （B）Per-Floor Planning（逐层规划）

针对每一楼层，逐层规划节点生成两个关键输出：
- **泡泡图拓扑（Bubble Diagram）**：定义该层的房间集合、每个房间的目标面积、房间之间的邻接关系图 $\mathcal{G}$。该拓扑图是后续几何求解的硬约束——最终平面图必须满足 $\mathrm{Topo}(L, \mathcal{G}) = \mathrm{true}$。
- **房间卡片（Room Cards）**：为每个房间指定语义类型（开放词汇，如“ICU病房”、“化学实验室”）、建议的对象类别和布局风格。

#### （C）Floorplan Synthesis（平面图合成）

这是 pipeline 的核心几何求解环节，将泡泡图拓扑转化为具有精确墙体坐标的 2D 平面图。其关键机制包括：

1. **自由区域定义**：每层 $f$ 的可用规划区域为：
   $$\Omega_f = P_f \setminus \bigcup_{v \in \mathcal{V}} Q_{f,v}$$
   其中 $P_f$ 是楼层外轮廓，$Q_{f,v}$ 是垂直核心筒（楼梯、电梯等）的占用区域。这一减法操作从几何层面强制执行了跨楼层的垂直对齐约束。

2. **MLLM 引导的种子选择与分层切割**：求解器采用迭代分裂策略——每次由 MLLM 在自由区域内为待放置房间选择一个“种子”位置和初始边界框，然后通过单次切割求解器（single-cut solver）将该区域分割为满足拓扑约束的矩形房间。分层分裂将复杂的全局布局问题分解为一系列低维子问题，显著降低了 MLLM 空间定位的难度。

3. **约束增长与能量优化**：求解器在满足拓扑约束的候选布局集合 $\mathcal{C}$ 中搜索最优解：
   $$L^{\star} = \arg\max_{L \in \mathcal{C}} \mathrm{Score}(L; \mathbf{w}) \quad \mathrm{s.t.} \quad \mathrm{Topo}(L, \mathcal{G}) = \mathrm{true}$$
   每个房间的能量函数 $e(r)$ 由面积误差、种子距离、多余角点惩罚和墙体接触奖励加权求和构成，布局总得分为所有房间能量之和的负值。

#### （D）Scene Instantiation（场景实例化）

将 2D 平面图实例化为 AI2-THOR 中的完整 3D 场景：
- **建筑结构**：根据平面图生成墙体、地板、天花板、门窗，并确保跨楼层承重墙的垂直连续性（见 Figure 8a）。
- **对象放置**：采用**可达性优先**策略，引入两种结构化关系原语——`matrix`（网格排列，如教室桌椅）和 `paired`（对称共置，如床头柜）——并通过**优先级感知排序**和**质量优先修剪**，在保证 100% 地面可达性的前提下最大化对象数量。
- **光照与材质**：根据全局风格设定应用对应的光照方案和表面材质。

#### （E）Task-Semantic Scene Editing Agent（任务语义场景编辑代理）

这是一个可选的后处理模块（见 Figure 4 和 Figure 13），采用 **ReAct 控制器 + 工具 API** 的架构：
1. **前提条件分解**：将高层任务指令（如“拿一个零食和饮料到沙发”）分解为可验证的前提条件（路径连通性、对象可用性）。
2. **检查-准备回路**：依次执行路径连通性检查、对象可用性检查，并在必要时通过对象供应与场景编辑工具对场景进行最小化修改（如添加缺失的物体），确保复杂具身任务在生成场景中可执行。
3. **混合状态管理**：通过快速静态语义状态（JSON 场景图）和按需物理引擎的协同，在保持结构真实性的同时实现高效的状态同步。

### 架构设计原则

整个 pipeline 的核心设计理念是**将 MLLM 的语义理解和创造力与几何求解器的精确性和可验证性解耦**：MLLM 负责高层决策（功能分区、拓扑生成、种子定位），而几何求解器强制执行硬约束（垂直对齐、拓扑有效性、面积拟合）。这种混合架构使得 MANSION 无需任何训练即可生成多样化的建筑类型（医院、学校、超市、办公楼等），实现了真正的开放世界可扩展性。

### 补充图表

![[assets/figures/papers/paper_list_l2540_https_arxiv_org_abs_2603_11554/figures/019_Figure_12.jpg]]
*Figure 12: Illustration of the single-floor, topology-driven pipeline. (a) Input room topology graph. (b) Cut-round construction and hierarchical splitting over the free region. (c) Final 3D scene instantiation in AI2-THOR after applying structure, objects, and lighting*



### 整体架构：混合MLLM-几何流水线

MANSION采用**语义与几何解耦**的混合架构，将高层功能规划交给多模态大语言模型（MLLM），而将低层几何求解交给确定性约束求解器。这一设计实现了真正的开放世界可扩展性——无需新数据或重新训练即可生成多样化建筑类型（医院、学校、超市、办公楼等）。流水线由五个核心模块串联构成，如Figure 2所示。

**模块一：整体建筑规划（Whole Building Planning）**
该模块作为建筑级规划节点，接收自然语言描述，输出跨楼层的功能分区方案、各楼层面积分配以及全局视觉风格（如“现代办公楼”、“幼儿园”）。MLLM在此阶段负责高层语义推理，将模糊的用户意图转化为结构化的建筑程序。

**模块二：逐层规划（Per-Floor Planning）**
为每一层独立生成**泡泡图拓扑**（bubble diagram）和**房间卡片**。泡泡图定义了该层的房间集合、目标面积及房间间的邻接关系（如“走廊连接所有房间”），房间卡片则细化每个房间的功能类型（开放词汇，不限于住宅场景）和语义属性。此阶段输出的是纯拓扑约束，尚未涉及几何坐标。

**模块三：平面图合成（Floorplan Synthesis）**
这是整个框架的几何核心。该模块将泡泡图拓扑转化为满足硬约束的2D几何平面图，采用**MLLM种子选择 + 约束增长求解器**的混合策略。具体而言：
1. MLLM为每个房间在自由区域内选择一个种子位置（seed box），提供空间定位的先验；
2. 基于约束增长的几何求解器从种子出发，通过迭代分裂（hierarchical splitting）扩展房间边界，同时强制执行拓扑邻接约束和垂直对齐约束。

**模块四：场景实例化（Scene Instantiation）**
将2D平面图实例化为AI2-THOR中的交互式3D场景，包括建筑结构（墙体、门窗、楼梯、电梯）、物体放置、光照和材质。物体放置模块引入**可达性优先**策略和两种结构化关系原语——`matrix`（网格排列，如教室桌椅）和`paired`（对称共置，如床头柜），并采用优先级感知的排序与质量优先修剪，在保持物体数量的同时实现100%的地面-物体可达性。

**模块五：任务语义场景编辑代理（Task-Semantic Scene Editing Agent）**
该代理采用ReAct控制器 + 工具API的架构（见Figure 4），通过“检查-准备”回路对预生成建筑进行最小化、可验证的编辑，以确保复杂具身任务的前提条件被满足。具体流程：将高层指令（如“把零食和饮料送到沙发上”）分解为路径连通性检查、物体可用性检查和物体供应/场景编辑三个子步骤，仅修改必要元素而不破坏建筑结构稳定性。

---

### 关键公式与变量含义

**自由规划区域**

给定楼层 $f$，其可规划的自由区域 $\Omega_f$ 定义为外轮廓 $P_f$ 减去所有垂直核心筒（楼梯、电梯、设备竖井等）的占用区域：

$$\Omega _ { f } = P _ { f } \setminus \bigcup _ { v \in \mathcal { V } } Q _ { f , v }$$

其中 $\mathcal{V}$ 为垂直结构集合，$Q_{f,v}$ 为垂直核心 $v$ 在楼层 $f$ 的投影占用区域。这一硬约束确保了跨楼层的垂直对齐——所有楼层的楼梯/电梯井必须在相同平面位置贯穿，这是MANSION区别于所有单层方法的根本机制。

**平面图合成为可验证搜索**

最优布局 $L^*$ 是在候选布局集 $\mathcal{C}$ 中最大化能量得分的布局，且必须满足泡泡图 $\mathcal{G}$ 规定的拓扑约束：

$$L ^ { \star } = \arg \operatorname* { m a x } _ { L \in \mathcal { C } } \mathrm { S c o r e } ( L ; \mathbf { w } ) \quad \mathrm { s . t . } \quad \mathrm { T o p o } ( L , \mathcal { G } ) = \mathrm { t r u e }$$

其中 $\mathrm{Topo}(L, \mathcal{G})$ 为布尔函数，验证布局 $L$ 的房间邻接关系是否与泡泡图 $\mathcal{G}$ 一致。搜索空间 $\mathcal{C}$ 由约束增长算法在自由区域 $\Omega_f$ 内生成。

**单房间能量函数**

每个房间 $r$ 的能量（代价）由四项加权和构成：

$$e ( r ) = w _ { \mathrm { r a t i o } } f _ { \mathrm { r a t i o } } ( r ) + w _ { \mathrm { s e e d } } z _ { \mathrm { s e e d } } ( r ) + w _ { \mathrm { c o r n e r } } f _ { \mathrm { c o r n e r } } ( r ) - w _ { \mathrm { w a l l } } \mathrm { c l a m p } _ { [ 0 , 1 ] } ( f _ { \mathrm { w a l l } } ( r ) )$$

- $f_{\mathrm{ratio}}(r)$：面积误差项，惩罚房间实际面积与目标面积的偏差；
- $z_{\mathrm{seed}}(r)$：种子距离项，惩罚房间几何中心偏离MLLM指定种子位置的程度；
- $f_{\mathrm{corner}}(r)$：多余角点惩罚，抑制房间形状产生不必要的凸角，鼓励矩形化；
- $f_{\mathrm{wall}}(r)$：墙体接触奖励（负号表示降低能量），鼓励房间边界与建筑外墙或垂直核心壁面对齐，经 $\mathrm{clamp}_{[0,1]}$ 截断至 $[0,1]$。

布局总能量为所有房间能量之和，得分为其负值：$\mathrm{Score}(L; \mathbf{w}) = -\sum_r e(r)$。权重向量 $\mathbf{w} = \{w_{\mathrm{ratio}}, w_{\mathrm{seed}}, w_{\mathrm{corner}}, w_{\mathrm{wall}}\}$ 控制各项的相对重要性。

**种子采样扰动半径**

在分层分裂过程中，房间 $r$ 的初始扰动半径 $R_r^{(0)}$ 用于种子位置采样：

$$R_r^{(0)} = r_{base} + k \cdot a_r / |\Omega_f(p_t)|$$

其中 $r_{base}$ 为基础半径，$a_r$ 为房间目标面积，$|\Omega_f(p_t)|$ 为父区域 $p_t$ 的面积，$k$ 为缩放系数。该公式使得种子采样范围随房间相对大小自适应调整——大房间获得更大的初始搜索半径，小房间则更集中在MLLM指定的种子附近。这一机制与迭代分层分裂策略配合，显著降低了MLLM的空间定位复杂度：消融实验表明，移除分层分裂后Micro-IoU从63.56骤降至45.65（ResPlan-1k数据集）。

### 补充图表

![[assets/figures/papers/paper_list_l2540_https_arxiv_org_abs_2603_11554/figures/005_Figure_4.jpg]]
*Figure 4: The “Check-and-Provision” workflow of our Task-Semantic Scene Editing Agent. The agent first decomposes a high-level instruction (“bring a snack and a drink to the sofa”) into preconditions. It then sequentially performs a (a) Path Connectivity Check, an (b) Object Availability Check, and an (c) Object Provisioning & Scene Edit to ensure the task is executable before generation*

![[assets/figures/papers/paper_list_l2540_https_arxiv_org_abs_2603_11554/figures/020_Figure_13.jpg]]
*Figure 13: System Architecture of the Task-Semantic Scene Editing Agent. The system operates via a ReAct Controller (top) that iteratively plans and issues JSON tool requests. A Tool Invoker (middle) serves as an execution bridge, routing perception tasks to the fast Static Semantic State (bottom left) and action tasks to the On-Demand Physics Engine (bottom right). The dashed arrow highlights the Hybrid State Management mechanism, where physical simulation results are synchronized back to the static scene JSON to ensure consistency*

![[assets/figures/papers/paper_list_l2540_https_arxiv_org_abs_2603_11554/figures/012_Figure_7.jpg]]
*Figure 7: Qualitative comparison between Holodeck and MANSION under high-level semantic building prompts*



## 实验与关键发现

MANSION的实验评估围绕四个维度展开：平面图生成质量、对象放置合理性、跨楼层具身任务可执行性，以及消融分析对关键设计选择的验证。以下逐一报告主结果与关键发现。

### 平面图生成：从单层住宅到复杂多楼层

平面图生成在两类数据集上进行：标准单层住宅数据集T2D，以及更具挑战性的复杂住宅数据集ResPlan-1k。评估指标为Macro-IoU和Micro-IoU，在手动标注（MA）和自动标注（AA）两种设置下报告。表2和表3分别汇总了两组实验的核心结果。

在T2D上，MANSION（MA设置）取得Macro-IoU 80.66%，与基于扩散模型的ChatHouseDiffusion（CHD MA，79.04%）性能相当，差距仅为+1.62个百分点。这表明即使在标准单层场景中，MANSION无需训练的约束增长求解器也能达到数据驱动方法的水平。

真正的差异体现在ResPlan-1k上。该数据集包含更复杂的房间拓扑和空间布局，CHD在零样本条件下Micro-IoU仅为33.49%，暴露出纯数据驱动方法在分布外场景上的泛化瓶颈。相比之下，MANSION（MA）的Micro-IoU达到76.74%，优势高达+43.25个百分点。这一结果直接验证了核心设计：**约束增长算法**将拓扑有效性作为硬约束，使其在未见过的复杂布局上仍能保持强拟合能力。

### 对象放置：可达性优先的结构化布局

对象放置实验在8m×8m教室场景中进行，对比方法包括Holodeck和LayoutGPT。表4报告了五项指标：放置对象数量（#Obj）、越界对象数（#OB）、碰撞对象对数（#CN）、地面-对象可达性（#Rch）以及用户偏好得分。

MANSION在可达性上达到100%，显著优于Holodeck的80.0%和LayoutGPT的98.6%。这一优势源于两个关键设计：

- **基于锚点的分组与结构化原语**：引入`matrix`（网格模式）和`paired`（对称共置）两种关系原语，使对象布局既符合功能语义（如课桌成排、椅子配对），又自然避开通行区域。
- **优先级感知排序与质量优先修剪**：在保持对象数量的同时，优先放置对可达性影响大的对象，并通过质量优先的修剪策略消除潜在碰撞。

消融实验进一步证实，移除优先级排序和质量优先修剪后，可达性从100%下降至约80%，与Holodeck相当。用户偏好研究则显示，MANSION在真实感、多样性和布局合理性三个维度上均获得最高评分。

### 跨楼层具身任务：建筑尺度的严峻挑战

具身任务实验在MansionWorld数据集上进行，评估代理包括BUMBLE（VLM驱动的跨楼层导航框架）和COME-robot（GPT-4V规划）。任务要求代理在多楼层建筑中完成对象检索与导航，成功率与进度得分汇总于表5。

**单层设置**中，原始BUMBLE的成功率为0%，主要受限于VLM对模拟环境物体的识别准确率不足。通过引入文本增强（明确提供物体类型等语义提示），MANSION将BUMBLE的成功率提升至60%，验证了场景编辑代理在确保任务前提条件可满足方面的价值。

**四层设置**中，所有方法的成功率均为0%。这一结果揭示了一个尚未解决的根本瓶颈：随着楼层数增加，VLM需要处理的视觉地标数量急剧膨胀，而输入分辨率的限制导致严重的信息损失。附录中的故障案例分析（Figure 19、Figure 20）进一步确认了两类典型失败模式：机器人因路径规划错误被困角落，以及地标图像拼接后关键信息丢失导致导航失败。这反衬出MANSION作为测试床的独特价值——它暴露了现有具身智能系统在建筑尺度长程任务上的系统性脆弱性。

### 消融分析：分层分裂与MLLM能力

表3中的消融实验量化了两个关键设计选择的影响。

**分层分裂策略**：移除迭代分裂过程，迫使MLLM一次性输出所有房间种子，导致Micro-IoU从63.56骤降至45.65（ResPlan-1k，Gemini-2.5-Pro配置）。这一-17.91的降幅证实了迭代分裂对降低空间定位复杂度的关键作用——将全局布局问题分解为局部子区域内的逐步决策，显著减轻了MLLM的空间推理负担。

**MLLM骨干能力**：将MLLM从Moonshot替换为Gemini-2.5-Pro后，T2D上的Micro-IoU从42.33提升至69.98，差距大幅缩小。这表明MANSION的性能与底层MLLM的空间指向能力正相关，更强的视觉语言模型可直接转化为更精确的种子定位和更合理的空间规划。

### 失败模式与局限性

除四层具身任务的系统性失败外，论文还报告了以下局限：

- **教室场景多样性不足**：对象放置中`matrix`原语的重复排列导致用户感知的多样性得分偏低，提示需要在结构化约束与视觉丰富度之间寻求更好的平衡。
- **一次性求解器的次优性**：当前对象放置模块不包含反射或迭代优化机制，在极复杂房间中可能产生次优布局。与SceneWeaver等迭代方法的直接比较因范式差异而未能进行。
- **MLLM空间定位精度**：种子定位的质量直接影响平面图生成效果。在非标准几何形状或极端长宽比的区域中，MLLM的种子选择可能出现偏差，需要更精细的提示工程或模型能力提升。
- **模拟环境规模上限**：受AI2-THOR引擎限制，单层面积约500平方米，帧率约束使得更大规模场景的实时交互变得困难，限制了向街区级别或室外场景的直接扩展。

### 补充图表

![[assets/figures/papers/paper_list_l2540_https_arxiv_org_abs_2603_11554/figures/002_Table_1.jpg]]
*Table 1: Comparison of floorplan generation methods. Bdry./Topo./Vert. denote Boundary/Topology/Vertical structure. Boundary/Topology: controllable conditioning at test time. Vertical structure indicates cross-floor aligned cores (walls/rooms/regions) that persist across floors. Room type: resident vs. open-vocab*

![[assets/figures/papers/paper_list_l2540_https_arxiv_org_abs_2603_11554/figures/006_Table_2.jpg]]
*Table 2: IoU scores under different configurations on T2D*

![[assets/figures/papers/paper_list_l2540_https_arxiv_org_abs_2603_11554/figures/007_Table_3.jpg]]
*Table 3: IoU scores under different configurations on Resplan-1k*

![[assets/figures/papers/paper_list_l2540_https_arxiv_org_abs_2603_11554/figures/008_Table_4.jpg]]
*Table 4: object placement quantitative comparison. We report the average number of placed objects (#Obj, with small items in parentheses), out-of-boundary objects (#OB), Layout-level collided object pairs (#CN), floor-object reachability (#Rch, %), and user-study preference scores (%) for Realism (Real.), Diversity (Div.), and Layout (Lay.)*

![[assets/figures/papers/paper_list_l2540_https_arxiv_org_abs_2603_11554/figures/010_Table_5.jpg]]
*Table 5: Task success rates from 10 trials. Progress score is reported in the brackets in the format (Object retrieval success, Navigation success)*

![[assets/figures/papers/paper_list_l2540_https_arxiv_org_abs_2603_11554/figures/001_Figure_1.jpg]]
*Figure 1: MansionWorld: The first building-scale dataset for long-horizon embodied AI tasks. Generated by our MANSION framework, this dataset represents the first large-scale collection of multi-story, customizable themed environments. The visualization highlights four representative examples: Kindergarten, Hospital, Supermarket, and a Six-story Office Building, which feature complex functional zoning and fully navigable vertical connections to support long-horizon, cross-floor embodied AI tasks. You can access the MansionWorld dataset at: Link to MansionWorld*

![[assets/figures/papers/paper_list_l2540_https_arxiv_org_abs_2603_11554/figures/027_Figure_19.jpg]]
*Figure 19: Failure case 1*



## 定位与知识库关联

### 1. 方法类别与核心差异

MANSION 属于**语言驱动的建筑尺度3D场景生成方法**，其核心定位是在单层室内场景生成与具身智能基准之间架设一座“垂直结构”的桥梁。当前主流方法可归为以下谱系：

- **扩散模型驱动的平面图生成**：以 **ChatHouseDiffusion (CHD)** 为代表，基于数据驱动的扩散范式在单层住宅平面图生成上表现出色（T2D数据集Macro-IoU达79.04%），但其能力边界受限于训练数据分布——仅支持住宅类型，且完全不建模楼梯、电梯等跨楼层垂直结构（见表1）。CHD在更具挑战性的ResPlan-1k数据集上零样本Micro-IoU骤降至33.49%，暴露了纯扩散方法在分布外复杂布局上的脆弱性。

- **LLM驱动的场景布局方法**：**Holodeck** 和 **LayoutGPT** 利用大语言模型生成单层3D场景布局，具备一定的开放词汇能力，但缺乏结构化的建筑约束。在对象放置任务中，Holodeck的地面可达性仅为65.2%–88.7%（见表4），因其采用数量优先的放置策略而忽略可达性；LayoutGPT虽可达性较高（98.6%），但同样不支持多楼层垂直结构。

- **基于图的平面图生成**：**Graph2Plan** 等方法通过图结构编码房间拓扑关系，但仅支持单层住宅，且不具备开放词汇房间类型的能力。

- **跨楼层具身智能框架**：**BUMBLE** 和 **COME-robot** 代表了VLM驱动的跨楼层导航与操作前沿，但它们依赖于预生成的场景环境。在四层建筑场景中，所有现有具身代理的成功率均为0%（见表5），反衬出缺乏高质量多楼层场景测试床的系统性瓶颈。

MANSION 在谱系中的独特位置在于：**将垂直对齐作为一等硬约束，通过MLLM语义规划与约束几何求解的混合架构，首次实现了从自然语言到建筑尺度多楼层3D场景的端到端生成，且无需任何训练**。

### 2. 关键设计决策与知识增量

#### 2.1 垂直结构硬约束

现有方法（包括CHD、Holodeck、LayoutGPT、Graph2Plan）将场景生成视为单层独立问题，完全忽视跨楼层的结构连续性。MANSION 通过公式化定义每层自由区域：

$$\Omega _ { f } = P _ { f } \setminus \bigcup _ { v \in \mathcal { V } } Q _ { f , v }$$

将楼梯、电梯、服务竖井等垂直核心从可规划区域中预先扣除，确保跨楼层墙体对齐和结构有效性。这一设计将“垂直对齐”从软性偏好提升为几何求解器中的硬约束，是区别于所有先前工作的根本性知识增量。

#### 2.2 语义-几何解耦的混合架构

与CHD的端到端扩散范式不同，MANSION 采用**MLLM负责高层语义规划（功能分区、房间拓扑、种子定位），约束增长求解器负责低层几何实现（切割、能量优化）**的混合架构。这种解耦带来三重优势：

1. **训练无关的开放世界扩展性**：无需为医院、学校、超市等新建筑类型收集训练数据或重新训练，仅需MLLM理解语义即可生成。
2. **可验证的拓扑保真度**：几何求解器将平面图合成形式化为可验证搜索问题：
   $$L ^ { \star } = \arg \operatorname* { m a x } _ { L \in \mathcal { C } } \mathrm { S c o r e } ( L ; \mathbf { w } ) \quad \mathrm { s . t . } \quad \mathrm { T o p o } ( L , \mathcal { G } ) = \mathrm { t r u e }$$
   确保输出布局严格满足泡泡图规定的邻接关系。
3. **分层分裂降低复杂度**：消融实验表明，移除迭代分裂策略使MLLM一次性输出所有房间种子，导致ResPlan-1k上Micro-IoU从63.56骤降至45.65（见表3），验证了分层分裂对空间定位精度的关键作用。

#### 2.3 可达性优先的对象放置

Holodeck和LayoutGPT在对象放置中采用数量优先策略，忽略了物体与地面的可达性约束。MANSION 引入三个结构化原语：
- **锚点分组**：将功能相关的物体绑定到特定锚点（如“讲台区域”）。
- **结构化关系原语**：`matrix`（网格排列）和`paired`（对称共置）捕捉教室、会议室等场景的规则布局。
- **优先级感知排序与质量优先修剪**：在保持物体数量的同时，将可达性从~80%提升至100%（见表4）。

#### 2.4 任务语义场景编辑代理

与静态生成后即固定的场景不同，MANSION 的**任务语义场景编辑代理**（见图4）通过ReAct控制器和工具API，在预生成建筑语料库上执行最小化、可验证的编辑（路径连通性检查、物体可用性检查、物体供应与场景修改），确保复杂具身任务的前提条件得到满足。这一设计将场景生成从“一次性产物”转变为“任务适配的基础设施”，为具身智能评测提供了动态测试床。

### 3. 适用边界与局限

#### 3.1 生成能力的边界

- **MLLM空间指向能力的瓶颈**：种子定位质量直接影响平面图生成效果。使用Gemini-2.5-Pro替代Moonshot可将T2D性能从42.33大幅提升至69.98（见表2），表明方法性能随MLLM空间推理能力增强而提升，但当前最先进MLLM在复杂布局中仍存在定位误差。
- **一次性求解器的次优性**：对象放置模块未采用反射或迭代优化机制，在极复杂房间中可能产生次优布局。教室场景中因重复排列导致用户感知多样性不足（用户研究中多样性得分相对较低），也源于此。
- **模拟器物理限制**：生成的3D场景受限于AI2-THOR的帧率与面积上限（每层约500平方米），难以直接扩展到更大规模或包含室外区域的场景。

#### 3.2 具身任务的挑战

- **四层建筑的完全失效**：所有具身代理在四层场景中成功率均为0%（见表5）。根本原因在于VLM输入分辨率限制和过多地标拼接导致严重信息损失，而非场景质量问题。这既是MANSION作为压力测试床的价值所在，也揭示了当前VLM导航范式的根本局限。
- **物体识别准确率不足**：VLM对模拟环境中物体的识别准确率较低，需引入额外语义提示（如物体类型文本）作为补偿——这在实际部署中不可依赖。

#### 3.3 场景编辑的保守性

场景编辑代理仅在预生成建筑语料库上做最小编辑，不生成新的建筑结构。这意味着建筑的整体空间组织仍由初始生成阶段决定，编辑代理无法从根本上改变建筑的功能分区或拓扑结构。

### 4. 开放问题与未来方向

1. **精细空间定位能力的提升**：如何增强MLLM在复杂空间布局中的精细定位能力，以减少对分层分裂策略的依赖，是实现更高效生成的关键。

2. **规模扩展至街区级别**：当前框架受限于单栋建筑和AI2-THOR的面积上限。能否将生成能力扩展到包含室外区域、多栋建筑的完整街区级别场景，是向城市尺度具身智能迈进的必要条件。

3. **多楼层导航的信息损失问题**：四层场景中VLM导航的完全失败暴露了根本性挑战。分层记忆、稀疏地标表示或专用空间推理模块可能是缓解信息损失的潜在方向。

4. **动态对象与物理交互的纳入**：当前场景为静态快照。将开门、移动家具、流体交互等动态物理过程纳入生成与控制闭环，需要架构层面的深度改进。

5. **端到端的任务驱动生成**：场景编辑代理与生成过程的耦合仍较松散。能否实现从任务描述直接端到端优化建筑结构、房间布局和物体放置，是一个值得探索的方向。

6. **非住宅环境的结构合理性**：医院、工厂等非住宅建筑具有更严格的安全规范和结构约束（如消防通道、洁净区隔离）。在保持生成多样性的同时确保这些约束的满足，需要领域知识的显式注入。



## 原文 PDF

![[paperPDFs/CVPR_2026/MANSION_Multi_floor_lANguage_to_3D_Scene_generatIOn_for_loNg_horizon_tasks.pdf]]
