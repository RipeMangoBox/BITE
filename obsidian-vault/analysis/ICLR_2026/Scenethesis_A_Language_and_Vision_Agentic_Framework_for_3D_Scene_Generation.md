---
title: "Scenethesis: A Language and Vision Agentic Framework for 3D Scene Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Scenethesis_A_Language_and_Vision_Agentic_Framework_for_3D_Scene_Generation_8e8a664a0837.pdf
project_link: "https://research.nvidia.com/labs/dir/scenethesis/"
code_link: "https://github.com/nvidia/warp"
aliases:
- Scenethesis
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 在LLM语言规划之后引入一个由视觉基础模型引导的、基于SDF（有符号距离场）的物理感知优化环，直接操控物体的5自由度姿态，同时施加碰撞避免和稳定性约束，从而决定场景的物理合理性与空间一致性。
primary_logic: 将LLM的语言规划能力与视觉基础模型的紧凑空间先验相耦合，通过语义对应与SDF约束建立端到端的物理感知优化回路，无需训练即可在保持开放域多样性的同时，系统性地消除碰撞与不稳定性，并利用自检式判断模块进行闭环修复。
claims:
- Scenethesis在物理合理性（Col‑O 0.8%, Inst‑O 3.2%）和可交互性（Reach 0.94, Walk 0.96）上显著优于所有对比方法（Table 2）。
- 消融实验表明，增加碰撞和稳定性约束后，碰撞率从22.7%降至0.8%，不稳定率从87.3%降至3.2%（Table 4）。
- 在文本‑图像对齐方面，Scenethesis的CLIP（30.71）、BLIP（77.17）和VQA（0.8269）得分均为最高（Table 1）。
- 72%的场景在首轮优化后通过判断模块；经自检修复后成功率提升至91%（附录B.3）。
---

# Scenethesis: A Language and Vision Agentic Framework for 3D Scene Generation

> [!tip] 核心洞察
> 将LLM的语言规划能力与视觉基础模型的紧凑空间先验相耦合，通过语义对应与SDF约束建立端到端的物理感知优化回路，无需训练即可在保持开放域多样性的同时，系统性地消除碰撞与不稳定性，并利用自检式判断模块进行闭环修复。

| 字段 | 内容 |
|------|------|
| 中文题名 | Scenethesis：面向3D场景生成的语言与视觉Agentic框架 |
| 英文题名 | Scenethesis: A Language and Vision Agentic Framework for 3D Scene Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=SzhezVoaNB) · [Project](https://research.nvidia.com/labs/dir/scenethesis/) · [paper](https://arxiv.org/abs/2507.02861) · [Code](https://github.com/nvidia/warp) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Scenethesis |
| Dataset | 室内场景文本‑图像对齐（34 prompts, 22 indoor） |

> [!tip] 效果简介
> - 室内场景文本‑图像对齐（34 prompts, 22 indoor） 上，CLIP↑ 30.71 vs 28.32 (Holodeck) (+2.39)。
> - 室内场景文本‑图像对齐 上，BLIP↑ 77.17 vs 51.99 (SceneTeller) (+25.18)；VQA↑ 0.8269 vs 0.8052 (LayoutGPT) (+0.0217)。
> - 室内场景物理合理性 上，Col‑O↓（对象级碰撞率） 0.8% vs 6.1% (Holodeck) (‑5.3%)。

## 概要

**问题瓶颈**：现有学习型3D场景生成方法（如DiffuScene、LayoutGPT）受限于室内数据集分布，长尾空间关系（上方/内部/后方）欠拟合，且缺乏物理合理性约束；纯LLM布局规划（如Holodeck）虽能产生多样化布局，但因缺少视觉与物理基础，常生成方向上不合理的放置、漂浮或穿模。

**核心思路**：在LLM语言规划之后引入一个由视觉基础模型引导的、基于SDF（有符号距离场）的物理感知优化环，直接操控物体的5自由度姿态，同时施加碰撞避免和稳定性约束，从而决定场景的物理合理性与空间一致性。核心洞察是将LLM的语言规划能力与视觉基础模型的紧凑空间先验相耦合，通过语义对应与SDF约束建立端到端的物理感知优化回路，无需训练即可在保持开放域多样性的同时，系统性地消除碰撞与不稳定性，并利用自检式判断模块进行闭环修复。

**方法定位**：Scenethesis是一种免训练的Agentic框架，流水线由四个模块构成——LLM粗场景规划、视觉布局细化、物理感知优化、空间一致性判断——形成“规划-细化-优化-验证”的闭环。

**主要结果**：
- **文本-图像对齐**：CLIP达30.71（Holodeck 28.32）、BLIP达77.17（SceneTeller 51.99）、VQA达0.8269（LayoutGPT 0.8052），均为最高（Table 1）。
- **物理合理性**：对象级碰撞率仅0.8%（Holodeck 6.1%），对象级不稳定率仅3.2%（Holodeck 7.0%），显著优于所有对比方法（Table 2）。
- **可交互性**：可达性0.94、可行走性0.96（Table 2）。
- **消融验证**：增加碰撞和稳定性约束后，碰撞率从22.7%降至0.8%，不稳定率从87.3%降至3.2%（Table 4）；72%的场景在首轮优化后通过判断模块，经自检修复后成功率提升至91%。

**方法谱系与知识库定位**：Scenethesis区别于两类现有方法——学习型布局生成方法（如**DiffuScene**、**LayoutGPT**、**SceneTeller**）受限于训练数据分布，难以泛化到开放域场景；LLM驱动框架（如**Holodeck** (Yang et al., 2024c)、**LayoutVLM**）缺乏物理感知，产生碰撞与不稳定放置。Scenethesis通过耦合视觉基础模型的空间先验与SDF约束优化，在免训练的前提下系统性地补足了物理合理性短板，同时保留了LLM的开放域多样性优势。与基于图像的组合式方法（如**Digital Cousins**、**MIDI**）相比，Scenethesis从文本直接生成完整场景，不依赖输入图像。

从文本描述生成可交互的3D场景，是具身智能、游戏开发与数字孪生等领域的核心需求。理想的场景生成系统需同时满足三个条件：**空间多样性**（能产生开放域、长尾的物体组合与布局）、**物理合理性**（无碰撞、物体稳定支撑、空间关系正确）以及**可交互性**（生成结果可直接用于下游仿真与导航任务）。然而，现有方法在这三个维度上始终处于“跷跷板”状态——任一维度的提升往往以牺牲其他维度为代价。

**学习型方法的分布外困境。** 以DiffuScene、LayoutGPT为代表的扩散模型或自回归布局生成器，从3D‑FRONT等室内数据集学习物体类别共现与空间分布。这类方法在训练分布内的常见布局上表现良好，但受限于数据集的封闭性：3D‑FRONT仅覆盖约6.8K个住宅场景，长尾空间关系（如“物体置于架内”“物体悬挂于另一物体下方”“物体位于另一物体后方”）在数据中极为稀疏，导致模型在这些关系上系统性欠拟合。更根本的是，学习型方法缺乏显式的物理约束——它们输出的是统计意义上的“合理”布局，而非物理上可行的放置方案。当面对训练分布之外的提示（如非住宅场景、非常规物体组合）时，碰撞与不稳定问题急剧恶化。

**纯LLM规划的视觉盲区。** Holodeck、LayoutVLM等方法将布局规划完全委托给大语言模型或视觉语言模型，利用LLM的世界知识产生多样化的物体选择与空间安排。这一范式天然具备开放域优势——LLM可以自由组合训练数据中罕见的物体与关系。但其致命缺陷在于**缺少视觉基础**：LLM以符号化方式操作物体类别与坐标，无法感知3D网格的实际几何形状，也无法验证生成布局在视觉上是否与文本描述对齐。结果表现为三类典型失败——物体漂浮、穿模、以及方向性放置错误（如沙发背对电视）。Holodeck虽引入了后处理规则（贴墙、z轴去穿透），但这些启发式修正无法处理复杂的多物体交互场景，且常常引入新的物理矛盾。

**物理感知闭环的缺失。** 上述两类方法的共同瓶颈在于：布局生成与物理验证是解耦的。学习型方法完全跳过物理验证；LLM方法至多进行粗略的3D包围盒干涉检查，无法处理非凸物体的精细碰撞，也无法建模“支撑—被支撑”的稳定性关系。这意味着**物理合理性从未作为一阶优化目标进入布局生成回路**，而是被降级为可有可无的后处理步骤。

**Scenethesis的核心动机**正是打破这一僵局：将LLM的开放域规划能力与视觉基础模型的紧凑空间先验相耦合，在布局生成回路中嵌入一个由SDF（有符号距离场）驱动的物理感知优化环。该优化环直接操控物体的5自由度姿态，同时施加碰撞避免与稳定性约束，使物理合理性从“事后修补”升级为“内生属性”。配合基于GPT‑5的自检式判断模块进行闭环修复，框架无需任何训练即可在保持开放域多样性的同时，系统性地消除碰撞与不稳定性——这正是当前所有文本到3D场景生成方法未能达成的目标。

## 核心方法与创新机理

Scenethesis 的核心创新并非单一算法突破，而是将**语言规划、视觉基础与物理感知优化**耦合为一条无需训练的 agentic 流水线，系统性地解决了现有方法在开放域 3D 场景生成中“多样化布局”与“物理合理性”难以兼得的瓶颈。

### 瓶颈诊断：数据分布偏差与视觉-物理基础的缺失

现有学习型方法（如 **DiffuScene**、**LayoutGPT**、**SceneTeller**）受限于室内数据集（如 3D‑FRONT）的分布，导致长尾空间关系（上方、内部、后方）欠拟合，且缺乏物理合理性约束。纯 LLM 布局规划方法（如 **Holodeck**，Yang et al., 2024c）虽能产生多样化布局，但因缺少视觉与物理基础，常生成方向上不合理的放置、漂浮或穿模。Scenethesis 的核心洞察在于：**将 LLM 的语言规划能力与视觉基础模型的紧凑空间先验相耦合，通过语义对应与 SDF 约束建立端到端的物理感知优化回路，无需训练即可在保持开放域多样性的同时，系统性地消除碰撞与不稳定性**。

### 核心因果机制：从粗规划到物理感知优化的闭环

Scenethesis 通过三个关键 changed slots 实现了上述耦合，形成一条从粗到精、从语义到物理的因果链：

1. **布局规划方式：LLM 粗规划 + 视觉基础模型细化。** 纯 LLM 符号式规划缺乏视觉基础，而纯数据驱动方法泛化受限。Scenethesis 采用 LLM 选择锚点物体并构建粗空间层次（Section 3.1），随后引入视觉模块进行三步细化：图像生成提供视觉引导、场景图构建提取物体间关系、资产检索匹配 3D 模型（Section 3.2）。这一设计使布局规划同时具备语言多样性和视觉可落地性。

2. **碰撞检测与物理约束：从 3D 包围盒粗略检查到基于 SDF 的网格级约束。** 现有方法多以 3D 包围盒近似物体，仅进行粗略干涉检查或后处理纠正。Scenethesis 的核心突破在于：在物体表面采样点，利用 SDF 计算每个采样点到其他物体表面的有符号距离，并据此施加**平移碰撞损失**（Eq. 2）和**缩放碰撞损失**（Eq. 3），同时通过**稳定性损失**（Eq. 4）促使物体底面与支撑表面接触。这一设计使框架能够处理精细放置场景（如将物体放入架内各层，而非仅置于顶部，见 Figure 6），从根本上消除了漂浮和穿模。

3. **布局修正机制：从一次性输出到闭环自检修复。** 现有方法无反馈或仅依赖后处理规则（如贴墙、z 轴去穿透）。Scenethesis 引入 GPT‑5 判断模块，对物体类别准确性、朝向对齐和整体空间一致性进行打分（Section 3.4）；任一项低于阈值时触发重新规划与优化，形成闭环修复。实验表明，72% 的场景在首轮优化后通过判断模块，经自检修复后成功率提升至 91%（附录 B.3）。

### 关键证据：消融实验揭示各组件的因果贡献

消融实验（Table 4）清晰展示了各组件对物理合理性的因果贡献：仅使用原始布局（点云投影）时，碰撞率高达 22.7%，不稳定率 87.3%；增加姿态对齐后，碰撞降至 10.6%，不稳定降至 74.2%；进一步添加 SDF 碰撞约束后，碰撞降至 3.6%，不稳定降至 69.8%；最终加入稳定性约束后，碰撞与不稳定分别降至 **0.8%** 和 **3.2%**。这一递进式改进证明，物理感知优化回路是 Scenethesis 实现物理合理性的决定性因素，而非 LLM 规划或资产选择的附带效果。

### 方法谱系与知识库定位

Scenethesis 位于文本到 3D 场景生成、LLM 驱动布局规划与物理感知优化的交叉点。与 **Holodeck**（Yang et al., 2024c）等纯 LLM 框架相比，Scenethesis 的关键区别在于引入了视觉基础模型引导的物理约束优化；与 **DiffuScene** 等学习型方法相比，Scenethesis 无需训练即可泛化到室内外开放域场景，且物理合理性指标显著更优（Col‑O 0.8% vs. Holodeck 6.1%，Table 2）。在文本-图像对齐维度，Scenethesis 的 CLIP（30.71）、BLIP（77.17）和 VQA（0.8269）得分均为所有对比方法中最高（Table 1），表明视觉细化模块有效弥补了纯 LLM 规划与视觉现实之间的鸿沟。

Scenethesis 是一种无需训练的 Agentic 流水线，将 LLM 的语言规划能力与视觉基础模型的空间先验相耦合，通过闭环的物理感知优化生成开放域、物理合理的可交互 3D 场景。整个流水线由四个核心模块串联构成，形成“规划—细化—优化—判断”的闭环回路（Figure 2）。

![[assets/figures/papers/paper_list_l61_https_openreview_net_forum_id_SzhezVoaNB/figures/002_Figure_2.jpg]]
*Figure 2: Scenethesis is an agentic pipeline: an LLM drafts a coarse scene planning, a vision module grounds and refines it, a physics-aware optimizer iteratively aligns poses and enforces contact/support constraints, and a judge verifies spatial coherence*

**输入输出流**：系统以自然语言文本提示为输入，输出一个包含 3D 物体资产及其 5‑DoF 姿态（3D 位置 + 偏航角 + 缩放）的物理合理场景布局。流水线各模块的职责与数据流转如下：

1. **粗场景规划（Coarse Scene Planning）**：LLM 根据用户提示选择物体、确定锚点对象，并构建以锚点为中心的粗空间层次结构——其他物体被放置在相对于该锚点的位置上。该阶段输出一个符号化的粗布局，包含物体列表及层级关系，但缺乏精确的空间坐标与视觉基础。

2. **布局视觉细化（Layout Visual Refinement）**：视觉模块将 LLM 的粗布局“落地”到图像空间。具体通过三个步骤完成：（i）利用图像生成器根据粗布局生成引导图像；（ii）从引导图像中提取场景图，获取物体间的空间关系与层次结构；（iii）基于场景图进行 3D 资产检索与 3D 包围盒（3DBB）估计。该阶段输出一个带有 3DBB 和层次关系的场景图，为后续优化提供初始姿态和结构约束。

3. **物理感知优化（Physics‑Aware Optimization）**：这是框架的核心创新环节。优化器首先通过语义对应（RoMa 提取引导图像与渲染图像间的高置信度密集对应点）对齐物体姿态；随后在场景图层次上迭代施加基于 SDF（有符号距离场）的物理约束——包括平移碰撞损失、缩放碰撞损失和稳定性损失——直接操控物体的 5‑DoF 参数，系统性地消除碰撞并确保支撑稳定性。该阶段将粗布局转化为物理合理的精细布局。

4. **空间一致性判断（Spatial Coherence Judgment）**：GPT‑5 判断模块对优化后的场景进行三项评估：物体类别准确性、朝向对齐度、整体空间一致性。任一项得分低于阈值时，系统触发重新规划与优化，形成闭环修复。实验表明，72% 的场景在首轮优化后通过判断，经自检修复后成功率提升至 91%（附录 B.3）。

**关键设计决策**：与纯 LLM 布局规划（如 **Holodeck**，Yang et al., 2024c）不同，Scenethesis 在语言规划后引入了视觉基础模型引导的物理感知优化环，使布局既保持开放域多样性，又具备精细的物理合理性。与学习型方法（如 DiffuScene、LayoutGPT）不同，该框架无需训练，不依赖特定室内数据集的分布先验，因此能够处理长尾空间关系（如架内、柜内放置，见 Figure 6）和室外场景（Table 3）。

> **需要手动验证**：流水线中各模块间的具体接口协议（如场景图的数据格式、优化器与判断模块之间的信息传递细节）在现有证据中未充分展开，建议结合论文正文 Section 3 进行确认。

### 补充图表

![[assets/figures/papers/paper_list_l61_https_openreview_net_forum_id_SzhezVoaNB/figures/012_Figure_8.jpg]]
*Figure 8: Illustration of collision avoidance and stability maintenance. The solid-line circle indicates the 3D object’s current position, while the dotted-line circle marks its anticipated position. The black dot represents the centroid of the target object, the purple dots indicate surface nodes with negative SDF values, and the red point*

Scenethesis 的核心创新在于将 LLM 的语言规划能力与视觉基础模型的空间先验相耦合，并通过 SDF（有符号距离场）约束建立一个端到端的物理感知优化回路。整个流水线由四个关键模块串联而成，如 Figure 2 所示。

### 粗场景规划

LLM 首先根据用户文本提示选择场景中的锚定对象（anchor object），并围绕该锚定对象构建粗粒度的空间层次结构（Section 3.1）。具体而言，LLM 决定场景中应包含哪些物体、各物体相对于锚定对象的大致空间关系（如“沙发前方放置茶几”），从而输出一个初始的符号化布局草稿。这一阶段仅提供粗粒度的语义规划，不涉及精确的 3D 姿态或物理约束。

### 布局视觉细化

粗规划的输出随后被送入视觉细化模块，通过三个步骤将其转化为带有 3D 包围盒（3DBB）和层次关系的场景图（Section 3.2）：(1) **图像引导生成**：利用图像生成模型根据场景描述生成引导图像，提供视觉先验；(2) **场景图构建**：从引导图像中提取物体间的空间关系，构建结构化的场景图；(3) **资产检索**：从整理后的 Objaverse 子集中检索与规划物体匹配的 3D 模型。这一模块的核心作用是为后续的物理感知优化提供视觉基础和初始姿态估计。

### 物理感知优化

这是 Scenethesis 的核心技术模块，负责将粗布局转化为物理合理的 3D 场景。优化过程分为两个阶段：语义对应驱动的姿态对齐和基于 SDF 的物理约束施加。

#### 语义对应提取

对于场景中的每个物体 ${\bf o}_i$ 及其在引导图像中的对应区域 $\tilde{{\bf o}}_i$，使用 RoMa 匹配器提取 $m$ 个高置信度密集语义对应点（Eq. 1, Section 3.3.1）：

$$\{ p ( x , y ) , \tilde { p } ( x , y ) \} _ { i } ^ { m } = \mathrm { R o M a } ( { \bf o } _ { i } , \tilde { { \bf o } } _ { i } )$$

其中 $p(x,y)$ 和 $\tilde{p}(x,y)$ 分别表示渲染图像与引导图像中的匹配点对。在此基础上，通过最小化 2D 重投影误差与 3D 一致性损失的加权和，优化物体的 5‑DoF 姿态参数（3 个平移 + 绕竖直轴的旋转 + 均匀缩放）。

#### SDF 碰撞与稳定性约束

姿态对齐后的布局仍可能存在碰撞和不稳定问题。Scenethesis 引入三个基于 SDF 的损失函数进行精细优化（Section 3.3.2, Figure 3）：

![[assets/figures/papers/paper_list_l61_https_openreview_net_forum_id_SzhezVoaNB/figures/003_Figure_3.jpg]]
*Figure 3: Collision avoidance and stability maintenance*

**平移碰撞损失**（Eq. 2）：当物体表面采样点 ${\bf v}_i \in {\bf V}^-$（SDF 值为负，表示穿透到其他物体内部）时，沿该点到物体质心的方向 ${\bf u}_i$ 将其推出碰撞区域：

$$\mathcal { L } _ { \mathrm { t r a n s l a t i o n } } = \sum _ { \mathbf { v } _ { i } \in \mathbf { V } ^ { - } } || f ( \mathbf { T } , | d _ { i } | , \mathbf { u } _ { i } ) - \mathbf { T } || _ { 2 } ^ { 2 }$$

其中 $d_i$ 为碰撞点的 SDF 值（负值），${\bf T}$ 为物体当前平移向量，$f(\cdot)$ 计算理想的无碰撞位置。

**缩放碰撞损失**（Eq. 3）：当碰撞来自两个及以上不同方向（$N_{\mathrm{cluster}} > 1$）时，驱动物体缩小以避开碰撞：

$${ \mathcal { L } } _ { \mathrm { s c a l e } } = { \left\{ \begin{array} { l l } { \left( \sum _ { \mathbf { v } _ { i } \in V ^ { - } } g ( | d _ { i } | , \mathbf { u } _ { i } ) - s \right) ^ { 2 } , } & { { \mathrm { i f ~ } } N _ { \mathrm { c l u s t e r } } > 1 , } \\ { 0 , } & { { \mathrm { o t h e r w i s e } } . } \end{array} \right. }$$

其中 $g(\cdot)$ 根据碰撞深度和方向计算所需的缩放量，$s$ 为当前缩放因子。

**稳定性损失**（Eq. 4）：促使物体底面点 ${\bf v}_i \in {\bf V}^B$ 与父对象表面接触（SDF 趋近于零），防止漂浮或陷入支撑物内部：

$$\mathcal { L } _ { \mathrm { s t a b i l i t y } } = \sum _ { \mathbf { v } _ { i } \in V ^ { B } } \left( 1 - e ^ { - d _ { i } ^ { 2 } } \right)$$

其中 $d_i$ 为底面采样点的 SDF 值。该损失在 $d_i=0$（恰好接触）时取得最小值，对漂浮（$d_i>0$）和穿透（$d_i<0$）均施加惩罚。

**联合优化**：上述损失与姿态对齐损失加权求和，统一驱动 5‑DoF 优化（Eq. 10, Appendix B.3）：

$$\mathcal { L } = \lambda _ { p } \mathcal { L } _ { p o s e } + \lambda _ { c . T } \mathcal { L } _ { \mathrm { t r a n s l a t i o n } } + \lambda _ { c . S } \mathcal { L } _ { \mathrm { s c a l e } } + \lambda _ { s } \mathcal { L } _ { \mathrm { s t a b i l i t y } }$$

优化过程按场景图的层次结构自顶向下迭代进行，确保父对象先稳定后再处理子对象（Algorithm 1）。消融实验（Table 4）定量验证了各组件的贡献：仅原始布局时碰撞率 22.7%、不稳定率 87.3%；增加姿态对齐后分别降至 10.6% 和 74.2%；添加 SDF 碰撞约束后进一步降至 3.6% 和 69.8%；最终加入稳定性约束后，碰撞率与不稳定率分别降至 0.8% 和 3.2%。

### 空间一致性判断

优化完成后，GPT‑5 判断模块对生成场景进行闭环验证（Section 3.4），从三个维度打分：物体类别准确性、物体朝向对齐度、整体空间一致性。任一项低于阈值时触发重新规划与优化。72% 的场景在首轮优化后通过判断，经自检修复后成功率提升至 91%（Appendix B.3）。

### 补充图表

![[assets/figures/papers/paper_list_l61_https_openreview_net_forum_id_SzhezVoaNB/figures/008_Table_3.jpg]]
*Table 3: Outdoor Scene Qualitative Evaluation*

## 实验与关键发现

### 文本-图像对齐与空间质量

Scenethesis 在文本-图像对齐的三个指标上均取得最优结果（Table 1）。CLIP 得分达 30.71，超过 **Holodeck** (Yang et al., 2024c) 的 28.32；BLIP 得分 77.17，大幅领先 **SceneTeller** 的 51.99（+25.18）；VQA 得分 0.8269，优于 **LayoutGPT** 的 0.8052。这一优势源于视觉基础模型提供的图像引导与语义对应：LLM 粗规划给出物体类别和层次关系后，图像生成和场景图构建为后续优化提供了密集的空间先验，使最终渲染视角与文本描述高度一致。

![[assets/figures/papers/paper_list_l61_https_openreview_net_forum_id_SzhezVoaNB/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation on text–image alignment and spatial quality (↑ higher is better). Spatial quality preference measures GPT-5 and human preference for Ours over baselines*

空间质量偏好方面，GPT-5 和人类评估者均显著偏好 Scenethesis 的输出。该评估将 Scenethesis 与各基线方法成对比较，统计偏好胜率——Scenethesis 在所有对比中均获胜，表明其生成的场景在整体布局合理性上具有一致优势。

### 物理合理性与可交互性

物理合理性是 Scenethesis 相比现有方法的核心突破点。在室内场景上（Table 2），Scenethesis 的对象级碰撞率（Col-O）仅 0.8%，远低于 **Holodeck** 的 6.1%；对象级不稳定率（Inst-O）为 3.20%，同样优于 Holodeck 的 7.00%。场景级指标上，Col-S 为 6%，Inst-S 为 16.67%，均显著低于对比方法。这一结果的因果机制在于：基于网格表面采样点的 SDF 碰撞检测（Eq. 2-3）能够发现包围盒无法捕捉的细粒度穿透，而稳定性约束（Eq. 4）驱动物体底面与支撑表面紧密接触，系统性地消除了漂浮和穿模。

![[assets/figures/papers/paper_list_l61_https_openreview_net_forum_id_SzhezVoaNB/figures/007_Table_2.jpg]]
*Table 2: Physical-plausibility and interactivity results*

可交互性评估进一步验证了物理合理性的实际意义。Scenethesis 的 Reach 指标达 0.94，Walk 指标达 0.96（Table 2），意味着在生成场景中，虚拟角色可以自然地到达物体并自由行走，不会因碰撞或不当放置而被阻挡。相比之下，基线方法因碰撞和布局混乱，可交互性显著降低。

室外场景（Table 3）同样展现出极强的物理合理性：Col-O 仅为 0.06%，Inst-O 为 0.12%，说明 SDF 约束在不同空间尺度下均能有效工作。文本-图像对齐方面，室外场景的 CLIP 和 BLIP 得分同样保持领先。

### 消融实验：各组件的因果贡献

Table 4 的消融实验揭示了物理感知优化回路中各组件的独立贡献，形成一条清晰的因果链：

![[assets/figures/papers/paper_list_l61_https_openreview_net_forum_id_SzhezVoaNB/figures/010_Table_4.jpg]]
*Table 4: Ablation study on the effectiveness of adding each component in spatial and physical constrains*

1. **原始布局**（仅将 3D 模型放入估计的 3D 包围盒）：碰撞率高达 22.7%，不稳定率达 87.3%，空间一致性相似度仅 0.536。此时布局完全依赖 LLM 规划的点云投影，缺乏视觉校准和物理约束。

2. **+ 姿态对齐**：碰撞率降至 10.6%，不稳定率降至 74.2%，相似度提升至 0.732。RoMa 语义对应（Eq. 1）将物体 5-DoF 姿态与引导图像对齐，修正了粗规划中的方向偏差，但物体间仍存在穿透。

3. **+ 碰撞约束**：碰撞率进一步降至 3.6%，不稳定率降至 69.8%，相似度提升至 0.836。SDF 平移损失（Eq. 2）将碰撞表面点沿质心方向推出，缩放损失（Eq. 3）在多点碰撞时缩小物体——两者协同消除了大部分穿透，但物体可能被推到无支撑的位置。

4. **+ 稳定性约束**（完整 Scenethesis）：碰撞率降至 0.8%，不稳定率骤降至 3.2%，相似度保持在 0.836。稳定性损失（Eq. 4）使物体底面 SDF 趋近于零，确保其与父对象表面接触，从根本上解决了漂浮问题。

Figure 7 的可视化消融直观展示了这一渐进式改进：从原始布局的混乱堆叠，到姿态对齐后的方向修正，再到碰撞约束消除穿透，最终稳定性约束使所有物体稳固放置。

![[assets/figures/papers/paper_list_l61_https_openreview_net_forum_id_SzhezVoaNB/figures/011_Figure_7.jpg]]
*Figure 7: Effects of different constraints. (a) image guidance from text input. (b) Raw layout: places 3D models in estimated 3DBBs. (c) + Pose alignment: adjusts 5DoF poses to align the pose. (d) + Collision: adding collision constraint. (e) + Stability: adding stability constraint*

### 精细化放置与层次空间关系

Scenethesis 的一个关键能力是处理长尾空间关系——尤其是“内部”关系。Figure 6 显示，Holodeck 仅能将小物体置于架子顶部，而 Scenethesis 可将包、酒瓶、鞋子、花瓶等精确放入架子的不同隔层内。这一能力源于场景图层次结构：LLM 规划时指定了“架子-隔层-物体”的父子关系，物理优化阶段则按层次顺序迭代施加约束，确保子物体的 SDF 采样点在其父物体的包围空间内进行碰撞检测。

![[assets/figures/papers/paper_list_l61_https_openreview_net_forum_id_SzhezVoaNB/figures/009_Figure_6.jpg]]
*Figure 6: Scenethesis precisely places small objects (e.g., bag, wine bottle, shoes, vase) within shelf compartments rather than only on top (Holodeck)*

### 自检式闭环修复

判断模块的闭环修复机制显著提升了最终成功率。72% 的场景在首轮优化后通过 GPT-5 判断（类别准确、朝向对齐、整体空间一致）；未通过的场景触发重新规划与优化，最终成功率提升至 91%。这一机制有效缓解了图像生成器与 LLM 规划不匹配的问题——当引导图像包含规划之外的物体或遗漏关键物体时，判断模块能识别差异并启动修正。

### 下游应用：数据增强

Scenethesis 生成的场景可作为高质量训练数据。将 5K Scenethesis 场景加入 **MIDI** 的训练集后（Table 7），在 BlendSwap 基准上的场景级和对象级 Chamfer Distance 均降低，F-score 和 IoU 提升。Figure 14 的定性对比显示，加入 Scenethesis 数据后，MIDI 生成的场景在物体布局合理性和空间关系上明显改善。这验证了 Scenethesis 输出的物理合理性和空间一致性对学习型方法具有正向迁移价值。

![[assets/figures/papers/paper_list_l61_https_openreview_net_forum_id_SzhezVoaNB/figures/021_Figure_14.jpg]]
*Figure 14: Qualitative comparison of MIDI generated scenes by training on 3D-FRONT vs. training on 3D-FRONT with additional 5K Scenethesis scenes*

![[assets/figures/papers/paper_list_l61_https_openreview_net_forum_id_SzhezVoaNB/figures/020_Table_7.jpg]]
*Table 7: Quantitative results on BlendSwap. CD-S and CD-O refer to scene-level CD and object-level CD respectively; F-score-S and F-score-O refer to scene-level F-score and object-level F-score respectively. Lower CD is better; higher F-score/IoU is better. 5K refers to 5K Scenethesis scenes*

### 失败模式与局限

尽管整体表现优异，Scenethesis 存在以下可识别的失败模式：

- **遮挡与小物体**：当目标物体在引导图像中被严重遮挡或本身极小（如桌上的笔），RoMa 提取的语义对应点数量不足，导致姿态优化不稳定或失败。此时优化可能收敛到局部极小值，物体方向出现偏差。

- **资产库缺失**：3D 资产检索受限于整理后的 Objavverse 子集。对于独特物体（如沙滩垫、特殊设计品），检索结果可能与图像引导存在外观差异，导致生成场景与预期不完全匹配。Figure 18 展示了这种差异的典型案例。

- **刚体假设**：当前优化仅处理刚性、正立的 5-DoF 姿态，无法表示关节类物体（如打开状态的抽屉、门）的交互状态，限制了几何复杂度和场景的功能性表达。

- **多轮重规划开销**：当图像生成器与 LLM 规划不匹配时，需要多轮自检和重新规划，增加了端到端运行时间。

## 定位与知识库关联

### 1. 核心瓶颈与因果机制

现有3D场景生成方法面临两个结构性瓶颈。其一，学习型方法（如 **DiffuScene**、**LayoutGPT**、**SceneTeller**）受限于室内数据集（如3D‑FRONT）的分布，导致长尾空间关系（上方/内部/后方）欠拟合，且缺乏物理合理性约束。其二，纯LLM布局规划方法（如 **Holodeck** (Yang et al., 2024c)）虽能产生多样化布局，但因缺少视觉与物理基础，常生成方向上不合理的放置、漂浮或穿模——例如，将物体简单置于架子顶部而非内部各层（Figure 6）。

Scenethesis的因果操纵变量在于：在LLM语言规划之后，引入一个由视觉基础模型引导的、基于SDF的物理感知优化环，直接操控物体的5‑DoF姿态，同时施加碰撞避免和稳定性约束。这一设计决定了场景的物理合理性与空间一致性。其核心洞察是将LLM的语言规划能力与视觉基础模型的紧凑空间先验相耦合，通过语义对应与SDF约束建立端到端的物理感知优化回路，无需训练即可在保持开放域多样性的同时，系统性地消除碰撞与不稳定性，并利用自检式判断模块进行闭环修复。

### 2. 方法谱系中的定位

Scenethesis在3D场景生成的方法谱系中占据“开放域物理感知布局优化”这一独特位置，与现有方法形成以下关键差异：

| 方法维度 | 纯LLM规划方法（如Holodeck） | 学习型生成方法（如DiffuScene, LayoutGPT） | Scenethesis |
|---------|---------------------------|----------------------------------------|-------------|
| 布局规划方式 | 纯LLM符号式规划，缺乏视觉基础 | 完全从数据学习布局 | LLM粗规划 + 视觉基础模型细化（图像生成、场景图构建、深度/3DBB估计） |
| 碰撞检测与物理约束 | 以3DBB近似物体，仅粗略干涉检查或后处理纠正 | 依赖数据分布隐式约束 | 基于网格表面采样点的SDF碰撞检测与层次迭代约束（Eq.2‑4），支持精细放置（如架内、柜内） |
| 布局修正机制 | 无反馈或仅一次性输出，依赖后处理规则 | 无反馈 | GPT‑5判断模块对类别、朝向、整体空间一致性打分；低于阈值时触发重新规划与优化（闭环修复） |

具体而言，Scenethesis相对于 **Holodeck** 的改进体现在三个层面：（1）引入图像生成与场景图构建，为LLM的粗规划提供视觉基础；（2）用SDF约束替代3DBB近似，实现网格级碰撞检测，使物体可被精确放置于架子内部而非仅顶部（Figure 6）；（3）引入自检判断模块，对不合格场景进行闭环修复，将首轮优化成功率从72%提升至91%（附录B.3）。相对于 **LayoutGPT** 和 **IDesign** 等基于VLM的布局设计方法，Scenethesis通过物理感知优化弥补了它们缺乏物理合理性约束的缺陷。

在基于图像的场景合成/重建方法（如 **Digital Cousins**、**MIDI**）的对比中，Scenethesis展示了文本驱动的开放域生成能力，而非依赖输入图像进行重建（Figure 17）。值得注意的是，Scenethesis生成的场景可作为数据增强源：在3D‑FRONT基础上增加5K Scenethesis场景训练 **MIDI‑3D**，可显著提升其生成质量（Figure 14, Table 7）。

### 3. 适用边界与局限

尽管Scenethesis在物理合理性和文本‑图像对齐方面表现优异，其适用边界受以下因素制约：

**姿态对齐的鲁棒性限制**：姿态对齐依赖物体在引导图像中的可见区域。对于严重遮挡或极小物体，语义对应点数量不足可能导致优化不稳定。这是视觉基础模型（RoMa）在极端条件下的固有限制，而非框架设计缺陷。

**资产库覆盖范围**：3D资产检索受限于整理后的Objaverse子集，部分独特物体（如沙滩垫、特殊设计品）可能缺失，导致生成场景与图像引导出现差异（Figure 18）。这限制了Scenethesis在需要高度特定物体的场景中的适用性。

**刚体假设**：当前优化假设物体为刚性、正立的5‑DoF姿态，未处理关节类物体（如抽屉、门）的交互状态。这意味着无法生成“打开的书”或“拉开的抽屉”等具有非刚性形变或关节状态的场景。

**运行时间代价**：图像生成器可能产生与LLM规划不完全匹配的物体，需要多轮自检重规划，增加了端到端生成时间。这一代价在交互式应用中可能成为瓶颈。

### 4. 开放问题

基于上述局限，以下开放问题值得进一步探索：

1. **语义对应的鲁棒性提升**：如何在小物体和重度遮挡情况下提升语义对应的鲁棒性，以避免姿态优化失败？可能的路径包括多视角一致性约束或引入物体级别的先验形状信息。

2. **关节物体的支持**：能否将生成式3D模型（如带关节的资产）纳入当前框架，以突破仅能处理刚体的限制？这需要扩展优化变量空间，从5‑DoF刚体姿态扩展至包含关节参数的更高维空间。

3. **资产库多样性的扩展**：如何扩大资产库的多样性，例如引入更广泛的3D数据集或生成式资产（如通过文本到3D生成模型实时创建缺失物体），进一步缩小生成结果与图像引导之间的差距？

4. **物理感知优化的学习化融合**：是否可以将物理感知优化融入学习型场景生成器的训练目标，从而在保持推理速度的同时提升生成结果的物理合理性？这可能通过将SDF约束作为可微损失函数嵌入生成模型的训练过程来实现。

## 原文 PDF

![[paperPDFs/ICLR_2026/Scenethesis_A_Language_and_Vision_Agentic_Framework_for_3D_Scene_Generation_8e8a664a0837.pdf]]
