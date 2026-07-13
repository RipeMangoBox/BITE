---
title: Memory-Augmented Scene Understanding and Exploration for Open-World Aerial Object-Goal Navigation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Memory_Augmented_Scene_Understanding_and_Exploration_for_Open_World_Aerial_Object_Goal_Navigation.pdf
project_link: null
code_link: null
aliases:
- MASUEOWAOGN
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入自适应八叉树记忆（Adaptive Octree Memory）以积累并层次化表示历史观测，同时通过指令引导的查询机制（Instruction-Guided Memory Query）分离场景理解与前沿探索，使代理能够基于全局记忆做出精准的导航决策。
primary_logic: 将3D场景组织为可扩展的八叉树结构，并利用指令调制的场景查询与探索查询分别关注局部目标区域和远距离未探索前沿，在保持紧凑记忆的同时实现高效的目标定位与空间探索。
claims:
- 在UAV-ON基准上，OctMem-Agent相比OpenFly的成功率（SR）提升7.5%（19.50% vs 12.00%），相比Navid提升8.0%，且OSR等指标也全面领先。
- 消融实验显示，仅加入Adaptive Octree Memory即可将SR从基准的12.40%提升至15.70%，再加入Instruction-Guided Memory Query后进一步提升至19.50%。
- 层次化空间聚合（Hierarchical Spatial Aggregation）相比标准体素化显著提高了OSR（29.30% vs 27.50%）和SPL，验证了距离自适应体素化的有效性。
- UAV-ON (Total) 上 SR = 19.50%
---

# Memory-Augmented Scene Understanding and Exploration for Open-World Aerial Object-Goal Navigation

> [!tip] 核心洞察
> 将3D场景组织为可扩展的八叉树结构，并利用指令调制的场景查询与探索查询分别关注局部目标区域和远距离未探索前沿，在保持紧凑记忆的同时实现高效的目标定位与空间探索。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向开放世界空中目标导航的记忆增强场景理解与探索 |
| 英文题名 | Memory-Augmented Scene Understanding and Exploration for Open-World Aerial Object-Goal Navigation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhou_Memory-Augmented_Scene_Understanding_and_Exploration_for_Open-World_Aerial_Object-Goal_Navigation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | OctMem-Agent |
| Dataset | UAV-ON |

> [!tip] 效果简介
> - UAV-ON (Total) 上，SR 19.50% vs 12.00% (OpenFly) (+7.50%)；OSR 29.30% vs 25.90% (OpenFly) (+3.40%)。
> - UAV-ON (Seen) 上，SR 22.72% vs 显著高于所有基线 (显著)。
> - UAV-ON (Unseen) 上，SR 17.57% vs 显著高于所有基线 (显著)。

## 概要

### 问题背景与瓶颈

空中目标导航（Aerial Object-Goal Navigation）要求无人机在仅依赖视觉观测和高层语言指令的条件下，于大规模室外环境中定位并抵达指定目标对象。现有方法——如 **OpenFly**（Gao et al., 2025）、**AOA-F**（Xiao et al., 2025）及 **Navid**（Zhang et al., 2024）——普遍依赖当前帧和短期历史帧进行决策，缺乏对全局场景的结构化记忆。这导致两个核心缺陷：一是代理无法积累和利用长程观测信息，产生目光短浅的导航行为；二是缺乏有效的空间探索策略，在复杂环境中出现冗余徘徊或目标丢失。本质瓶颈在于：**局部观测与短期记忆无法支撑大规模场景中的全局理解与高效探索**。

### 核心方法定位

本文提出 **OctMem-Agent**，一个基于八叉树记忆增强的空中目标导航框架。其核心设计围绕两个因果调节变量展开：

1. **自适应八叉树记忆（Adaptive Octree Memory）**：将历史 RGB-D 观测增量聚合成层次化的 3D 场景表示，为导航决策提供可扩展的长期记忆。
2. **指令引导记忆查询（Instruction-Guided Memory Query）**：通过指令调制的查询机制，将记忆访问解耦为专注于近处目标定位的**场景查询**和关注远距离未探索区域的**探索查询**，从而在紧凑的记忆表征中同时实现高效目标定位与前沿探索。

该方法将 3D 场景组织为距离自适应的八叉树结构——近处细粒度体素保留局部细节，远处粗粒度体素维持全局覆盖——在保持紧凑性的同时赋予代理全局感知能力。

### 主要结果概要

在 UAV-ON 基准上，OctMem-Agent 相较最强基线 **OpenFly** 实现成功率（SR）**7.5%** 的绝对提升（19.50% vs 12.00%），Oracle 成功率（OSR）提升 **3.4%**（29.30% vs 25.90%），且在已见和未见场景子集上均保持显著领先。消融实验证实，自适应八叉树记忆和指令引导查询各自独立贡献了可观的性能增益，二者协同作用构成了方法有效性的关键支撑。

### 任务定义与挑战

空中目标导航（Aerial Object-Goal Navigation）要求无人机在仅依赖视觉观测和高层语言指令的条件下，在复杂的大规模室外环境中自主导航至指定的目标物体。与室内或地面导航不同，空中导航面临三维空间的自由运动、远距离感知需求以及室外场景的开放世界特性等多重挑战。

形式上，给定语言指令 $\mathcal{I}_{\mathrm{goal}} = \{w_{1}, \ldots, w_{\mathcal{N}_{I}}\}$ 和初始位姿 $p_{0} = (x_{0}, y_{0}, z_{0}, \phi_{0})$，智能体在每个时间步 $t$ 接收观测 $O_{t} = \{\mathbf{D}_{t}, \mathbf{V}_{t}\}$（深度图与RGB图像），并从离散动作空间 $a_{t} \in \mathcal{A}$ 中选择动作，其中 $\mathcal{A} = \{\text{前进}, \text{左转}, \text{右转}, \text{上升}, \text{下降}, \text{停止}\}$。成功的导航要求智能体在有限的步数内到达目标物体附近并执行停止动作。

### 现有方法的瓶颈

当前空中目标导航方法存在一个根本性的瓶颈：**依赖局部观测和短期历史，缺乏全局场景理解和有效的空间探索策略**。这导致智能体在复杂大规模室外环境中产生目光短浅的决策和冗余的探索行为，严重制约了导航成功率。

具体而言，现有基线方法暴露出以下结构性问题：

- **CLIP-H**（零样本基线）直接利用CLIP视觉特征进行导航，完全缺乏对历史信息的建模。
- **OpenFly**（Gao et al., 2025）作为开源航空VLN工具链，仅使用当前帧和前两帧进行决策，无法积累长期场景记忆。
- **AOA-F**（Xiao et al., 2025）基于LLM的航空目标导航方法，使用当前观测和近期位姿历史，但仍局限于短期窗口。
- **Navid**（Zhang et al., 2024）基于视频的VLM导航方法，处理视频序列生成动作，但缺乏显式的3D空间表示。

这些方法的共同缺陷在于：历史观测表示停留在原始帧或短期序列层面，未构建可扩展的3D场景记忆；探索与定位策略耦合在单一的端到端推理中，无法显式区分目标定位与未探索区域的探索。当目标物体暂时被遮挡、超出当前视野或位于远距离未探索区域时，智能体容易陷入原地旋转、丢失目标或重复探索已访问区域的困境。

### 本文动机与核心思路

针对上述瓶颈，本文提出**OctMem-Agent**，一个基于八叉树记忆增强的空中目标导航框架。其核心洞察在于：**将3D场景组织为可扩展的八叉树结构，并利用指令调制的场景查询与探索查询分别关注局部目标区域和远距离未探索前沿，在保持紧凑记忆的同时实现高效的目标定位与空间探索**。

具体而言，OctMem-Agent通过三个关键机制突破现有方法的局限：

1. **自适应八叉树记忆**：增量聚合RGB-D历史观测为层次化3D表示，以可扩展的方式积累全局场景记忆，解决短期历史的视野局限。
2. **指令引导记忆查询**：通过指令调制的双路查询机制，分离场景理解与前沿探索——场景查询专注于附近区域的目标定位，探索查询关注远距离未探索前沿，实现目标定位与空间探索的有效平衡。
3. **层次化空间聚合**：根据距离自适应调整体素尺寸，近距离细粒度保留局部细节，远距离粗粒度保持全局覆盖，在记忆紧凑性与表示精度之间取得平衡。

实验表明，OctMem-Agent在UAV-ON基准上相比最强基线OpenFly实现了7.5%的成功率绝对提升（19.50% vs 12.00%），并在已见和未见环境上均一致优于所有基线方法。

## 核心方法与创新机理

OctMem-Agent 的核心创新在于将空中目标导航从“短视的局部感知”升级为“基于全局记忆的推理”，通过两个关键机制解决现有方法的瓶颈：**自适应八叉树记忆（Adaptive Octree Memory）** 和 **指令引导记忆查询（Instruction-Guided Memory Query）**。

### 从局部观测到全局场景记忆

现有航空目标导航方法普遍依赖当前观测和极短的历史窗口。**OpenFly**（Gao et al., 2025）仅使用当前帧与前两帧进行决策，**AOA-F**（Xiao et al., 2025）则利用近期位姿历史，二者均缺乏对大规模室外环境的全局场景理解。这种“短视”设计导致代理在目标暂时被遮挡或超出视野时，容易陷入原地旋转或冗余探索（见 Figure 3 定性对比中 OpenFly-Agent 的行为）。

OctMem-Agent 引入**自适应八叉树记忆**，将历史 RGB-D 观测增量聚合为层次化的 3D 表示。具体而言，每一帧的 2D 补丁特征被注入 3D 位置嵌入，形成 3D 补丁 $\mathbf{X}_{3D} = \mathbf{X}_p + \mathbf{P}'$，随后通过**层次化空间聚合**（Hierarchical Spatial Aggregation）按距离自适应划分体素：近距离区域采用细粒度体素以保留局部细节，远距离区域采用粗粒度体素以保持全局覆盖。体素特征通过平均池化 $\mathbf{x}_v = \frac{1}{|\mathcal{T}_v|} \sum_{i \in \mathcal{T}_v} \mathbf{x}_i$ 压缩，最终构建为可扩展的八叉树结构 $\mathcal{M}_t$。这一设计使代理能够在紧凑的记忆中持续积累场景信息，而非每步重新感知。

消融实验直接验证了这一创新的因果效应：基准模型（无记忆）的成功率（SR）仅为 12.40%，加入自适应八叉树记忆后 SR 提升至 15.70%（Table 3），证明全局记忆本身即能显著改善导航决策。

### 从无差别感知到任务分离的查询机制

现有方法将目标定位与空间探索混杂在同一感知过程中，LLM/VLM 直接根据当前观测生成动作，未显式区分“寻找附近目标”和“探索未知区域”两种不同的信息需求。

OctMem-Agent 提出**指令引导记忆查询**模块，通过 FiLM（Feature-wise Linear Modulation）将语言指令 $\mathbf{e}_I$ 注入可学习查询，生成任务特定的场景查询 $\mathbf{Q}_{\text{scene}}$ 和探索查询 $\mathbf{Q}_{\text{explore}}$：

$$\mathbf{Q}_{\text{task}} = \text{FiLM}(\mathbf{Q}, \mathbf{e}_I) = (1 + \gamma(\mathbf{e}_I)) \odot \mathbf{Q} + \beta(\mathbf{e}_I)$$

在此基础上，模块将八叉树记忆按距离阈值 $d_b$ 分区为近处 $\mathcal{M}_{\text{near}}$ 和远处 $\mathcal{M}_{\text{far}}$ 子集。场景查询专注于 $\mathcal{M}_{\text{near}}$，负责定位附近的目标区域；探索查询专注于 $\mathcal{M}_{\text{far}}$，负责识别远距离未探索前沿。这种**任务分离**设计使代理能够同时兼顾局部目标定位和全局空间探索，避免因过度聚焦某一侧而导致失败。

消融实验表明，在已有记忆的基础上加入指令引导记忆查询后，SR 从 15.70% 进一步提升至 19.50%，更关键的是，Oracle 成功率（OSR）从 21.10% 大幅跃升至 29.30%，SPL 从 4.35% 提升至 6.37%（Table 3），证明该模块对探索效率和路径质量有决定性贡献。进一步移除指令调制查询（IMQ）导致 SR 降至 18.60%、OSR 降至 27.30%（Table 5），验证了指令信息在查询过程中的关键作用。

### 与基线方法的系统性差异

| 创新维度 | 基线方法（OpenFly / AOA-F） | OctMem-Agent |
|---------|---------------------------|--------------|
| 历史观测表示 | 当前帧 + 短期历史（≤3 帧），无长期记忆 | 自适应八叉树记忆，增量聚合所有历史 RGB-D 观测 |
| 空间聚合 | 标准体素化或均匀采样 | 层次化空间聚合，距离自适应体素尺寸 |
| 探索与定位策略 | LLM/VLM 直接根据观测生成动作，未显式分离 | 指令引导查询分离场景定位与前沿探索 |
| 记忆查询方式 | 无记忆查询机制 | FiLM 指令调制 + 距离分区查询 |

层次化空间聚合的独立消融（Table 4）显示，相比标准体素化，该设计将 OSR 从 27.50% 提升至 29.30%，SPL 也有提高，验证了距离自适应体素化在保留局部细节和维持全局覆盖之间的平衡优势。

综合来看，OctMem-Agent 的创新链条清晰：**自适应八叉树记忆**解决了“记不住”的问题，**指令引导记忆查询**解决了“查不准”的问题，二者协同实现了从局部反应式导航到全局记忆推理式导航的范式转变。

OctMem-Agent 是一个面向开放世界空中目标导航的记忆增强框架，其核心设计思想是将历史观测积累为可扩展的层次化3D场景记忆，并通过指令引导的查询机制从记忆中提取互补的场景理解与探索信息，最终驱动视觉-语言模型（VLM）生成导航动作。

### 整体流程

框架的输入包括语言指令 $\mathcal{I}_{\mathrm{goal}} = \{w_1, \ldots, w_{\mathcal{N}_I}\}$、初始3D位姿 $p_0 = (x_0, y_0, z_0, \phi_0)$，以及每个时间步 $t$ 的RGB-D观测 $O_t = \{\mathbf{D}_t, \mathbf{V}_t\}$。输出为离散动作 $a_t \in \mathcal{A}$，动作空间 $\mathcal{A}$ 包含六种操作：前进、左转、右转、上升、下降和停止。

整个 pipeline 由三个关键模块串联构成（Figure 2）：

![[assets/figures/papers/paper_list_l2042_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Memory_Augmented/figures/002_Figure_2.jpg]]
*Figure 2: The overall framework of our proposed OctMem-Agent. The agent builds an Adaptive Octree Memory from historical RGB-D data. The instruction-guided query module extracts compact scene and exploration tokens. These tokens are fused with the current visual observation and language instruction, serving as input to the LLM for action inference*

1. **自适应八叉树记忆**（Adaptive Octree Memory）：在每个时间步，将当前RGB-D观测通过深度图反投影生成3D点云，并从2D视觉特征中提取补丁特征，注入3D位置嵌入后得到3D补丁表示 $\mathbf{X}_{3D} = \mathbf{X}_p + \mathbf{P}'$。随后，采用层次化空间聚合策略，根据距离区间 $\mathcal{D} = \{[d_0, d_1), [d_1, d_2), \dots, [d_{K-1}, d_K]\}$ 自适应调整体素尺寸——近距离使用细粒度体素以保留局部细节，远距离使用粗粒度体素以覆盖更大空间范围。在每个体素内，对点特征和位置进行平均池化得到体素表示 $\mathbf{x}_v$ 和 $\mathbf{p}_v$，增量式地更新八叉树结构，形成可扩展的全局场景记忆 $\mathcal{M}_t$。

2. **指令引导记忆查询**（Instruction-Guided Memory Query）：该模块通过特征级线性调制（FiLM）将指令信息注入可学习查询，生成任务特定的查询向量 $\mathbf{Q}_{\mathrm{task}} = \mathrm{FiLM}(\mathbf{Q}, \mathbf{e}_I) = (1 + \gamma(\mathbf{e}_I)) \odot \mathbf{Q} + \beta(\mathbf{e}_I)$。随后，基于距离阈值 $d_b$ 将八叉树记忆分为近处子集 $\mathcal{M}_{\mathrm{near}}$ 和远处子集 $\mathcal{M}_{\mathrm{far}}$：场景查询（scene tokens）专注于近处体素以定位目标区域，探索查询（exploration tokens）关注远处体素以发现未探索前沿。这种解耦设计有效平衡了目标定位与空间探索。

3. **记忆融合动作生成**（Action Generation with Memory Integration）：将语言令牌 $\mathbf{H}_{\mathrm{lang}}$、当前观测令牌 $\mathbf{H}_{\mathrm{obs}}$ 和从记忆中提取的令牌 $\mathbf{H}_{\mathrm{mem}}$ 拼接为输入序列 $\mathbf{H}_{\mathrm{input}} = [\mathbf{H}_{\mathrm{lang}}, \mathbf{H}_{\mathrm{obs}}, \mathbf{H}_{\mathrm{mem}}]$，送入预训练的VLM骨干网络（基于OpenVLA，视觉编码器融合DINOv2和SigLIP特征，语言模型采用LLaMA-2 7B），通过Transformer层处理后预测离散动作令牌。

### 关键设计决策

框架的两个核心创新点直接回应了现有方法的瓶颈：

- **从短期历史到全局记忆的跃升**：现有方法（如OpenFly仅使用当前帧与前两帧）依赖局部观测和短期历史，缺乏对已探索区域的持久表征。自适应八叉树记忆通过增量聚合和层次化体素化，在保持紧凑存储的同时提供了可查询的全局场景表示，使代理能够回溯已探索区域中的目标线索。

- **场景理解与探索的显式解耦**：传统方法将目标定位和区域探索混为一体，导致目光短浅的决策。指令引导记忆查询通过任务特定的场景令牌和探索令牌分别处理近处和远处记忆，使代理既能精确跟踪已发现的目标，又能主动探索未知区域，避免了冗余搜索和目标丢失。

### 公平性保障

OctMem-Agent 基于OpenVLA框架构建，并使用与OpenFly相同的预训练权重进行初始化，确保了与基线方法的公平比较。

### 补充图表

OctMem-Agent 围绕三个关键模块构建：**自适应八叉树记忆**、**指令引导记忆查询**和**动作生成与记忆集成**。下面依次剖析各模块的机制及其核心公式。

### 3.1 问题形式化

在展开模块之前，先定义导航任务的基本符号体系。语言指令 $\mathcal{I}_{\mathrm{goal}} = \{ w_{1}, \ldots, w_{\mathcal{N}_{I}} \}$ 包含 $\mathcal{N}_I$ 个词，描述导航目标对象。初始位姿 $p_{0} = (x_{0}, y_{0}, z_{0}, \phi_{0})$ 给出了无人机在三维空间中的起始位置和偏航角。在时间步 $t$，观测 $O_{t} = \{ \mathbf{D}_{t}, \mathbf{V}_{t} \}$ 包含深度图 $\mathbf{D}_t$ 和 RGB 图像 $\mathbf{V}_t$。动作空间为离散集合 $a_{t} \in \mathcal{A} = \{\text{前进}, \text{左转}, \text{右转}, \text{上升}, \text{下降}, \text{停止}\}$。

### 3.2 自适应八叉树记忆

**动机**：现有方法（如 OpenFly 仅使用当前帧与前两帧）缺乏长期场景记忆，导致决策短视。自适应八叉树记忆通过增量聚合历史 RGB-D 观测，构建可扩展的层次化三维场景表示。

**核心机制**：首先将二维图像特征提升为三维补丁。给定二维补丁特征 $\mathbf{X}_p$ 和对应的三维位置嵌入 $\mathbf{P}'$，通过加法融合得到三维补丁表示：

$$\mathbf{X}_{3D} = \mathbf{X}_p + \mathbf{P}'$$

随后，采用**层次化空间聚合**对三维补丁进行体素化。预定义一组距离区间：

$$\mathcal{D} = \{ [d_0, d_1), [d_1, d_2), \dots, [d_{K-1}, d_K] \}$$

其核心思想是**距离自适应体素化**：距离代理越近的体素尺寸越小（保留细粒度局部细节），距离越远的体素尺寸越大（实现粗粒度全局覆盖）。在每个体素内，对点及其特征进行平均池化：

$$\mathbf{x}_v = \frac{1}{|\mathcal{T}_v|} \sum_{i \in \mathcal{T}_v} \mathbf{x}_i, \quad \mathbf{p}_v = \frac{1}{|\mathcal{T}_v|} \sum_{i \in \mathcal{T}_v} \mathbf{p}_i$$

其中 $\mathcal{T}_v$ 为体素 $v$ 内的点集。通过八叉树结构组织这些体素，实现内存效率与空间覆盖的平衡。

### 3.3 指令引导记忆查询

**动机**：导航任务需要同时完成目标定位（关注附近区域）和前沿探索（关注远处未探索区域）。单一查询机制难以兼顾这两种需求。

**核心机制**：该模块通过两个关键设计实现任务感知的记忆检索。

**指令调制查询**：使用 FiLM（Feature-wise Linear Modulation）将语言指令信息注入可学习查询 $\mathbf{Q}$，生成任务特定的查询：

$$\mathbf{Q}_{\mathrm{task}} = \mathrm{FiLM}(\mathbf{Q}, \mathbf{e}_I) = (1 + \gamma(\mathbf{e}_I)) \odot \mathbf{Q} + \beta(\mathbf{e}_I)$$

其中 $\mathbf{e}_I$ 为指令嵌入，$\gamma(\cdot)$ 和 $\beta(\cdot)$ 为可学习的缩放和偏移函数，$\odot$ 表示逐元素乘法。这使得查询能够根据指令语义自适应调整关注重点。

**任务感知记忆分区**：基于距离阈值 $d_b$ 将八叉树记忆分为近处和远处两个子集：

$$\mathcal{M}_{\mathrm{near}} = \{ \mathbf{m}_c^{(t)} \in \mathcal{M}_t \mid \mathrm{dis}(c) < d_b \}, \quad \mathcal{M}_{\mathrm{far}} = \{ \mathbf{m}_c^{(t)} \in \mathcal{M}_t \mid \mathrm{dis}(c) \geq d_b \}$$

其中 $\mathbf{m}_c^{(t)}$ 为时间步 $t$ 时体素中心 $c$ 处的记忆单元，$\mathrm{dis}(c)$ 为 $c$ 到代理当前位置的距离。场景查询 $\mathbf{Q}_{\mathrm{scene}}$ 关注 $\mathcal{M}_{\mathrm{near}}$（目标定位），探索查询 $\mathbf{Q}_{\mathrm{explore}}$ 关注 $\mathcal{M}_{\mathrm{far}}$（前沿探索），二者通过交叉注意力从各自分区提取互补信息。

### 3.4 动作生成与记忆集成

将语言令牌 $\mathbf{H}_{\mathrm{lang}}$、当前观测令牌 $\mathbf{H}_{\mathrm{obs}}$ 和记忆令牌 $\mathbf{H}_{\mathrm{mem}}$（由场景令牌与探索令牌拼接而成）进行序列拼接：

$$\mathbf{H}_{\mathrm{input}} = [ \mathbf{H}_{\mathrm{lang}}, \mathbf{H}_{\mathrm{obs}}, \mathbf{H}_{\mathrm{mem}} ]$$

该序列输入预训练 VLM 骨干网络（基于 OpenVLA，视觉编码器融合 DINOv2 和 SigLIP 特征，LLM 骨干为 LLaMA-2 7B），通过 Transformer 层处理后预测离散动作令牌，完成从感知到决策的端到端推理。

## 实验与关键发现

### 实验设置

OctMem-Agent 基于 **OpenVLA** 框架构建，并与 **OpenFly**（Gao et al., 2025）使用相同的预训练权重进行初始化，以确保比较的公平性。视觉编码器融合了 **DINOv2** 和 **SigLIP** 的特征，语言模型骨干采用 **LLaMA-2 7B**。所有实验在 **UAV-ON** 基准上开展，该基准按目标物体大小（Small / Medium / Large）和环境可见性（Seen / Unseen）划分测试场景，评估指标包括成功率（SR）、Oracle 成功率（OSR）和按路径长度加权的成功率（SPL）。

### 主实验结果

**Table 1** 展示了各方法在 UAV-ON 基准上按目标物体大小的性能对比。OctMem-Agent 在所有目标尺寸类别上均取得最高的成功率，总体 SR 达到 **19.50%**，相比最强基线 OpenFly（12.00%）提升 **7.5 个百分点**，相比 **Navid**（Zhang et al., 2024）提升 **8.0 个百分点**。OSR 方面，OctMem-Agent 达到 **29.30%**，领先 OpenFly 3.4 个百分点。与零样本基线 **CLIP-H** 相比，SR 和 OSR 分别高出 13.40 和 17.40 个百分点；与基于 LLM 的 **AOA-F**（Xiao et al., 2025）相比，SR 和 OSR 分别高出 12.20 和 11.80 个百分点。这一结果的核心驱动力在于自适应八叉树记忆赋予了代理全局场景理解能力，使其在搜索大型目标（如建筑）时不再受限于局部视野，而基线方法因缺乏长期记忆容易陷入原地旋转或丢失目标的困境。

在环境泛化性方面（**Table 2**），OctMem-Agent 在 Seen 场景下 SR 达 **22.72%**，在 Unseen 场景下 SR 为 **17.57%**，均显著优于所有基线。这表明层次化记忆表示不仅有助于拟合已知环境布局，也能在未见场景中提供有效的空间先验，缓解过拟合风险。

定性对比（**Figure 3**）进一步印证了定量结论：OpenFly-Agent 在导航过程中陷入原地旋转并丢失目标，Navid 则完全未能定位目标物体，而 OctMem-Agent 在整个序列中保持对目标的一致检测并成功抵达终点。

![[assets/figures/papers/paper_list_l2042_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Memory_Augmented/figures/005_Figure_3.jpg]]
*Figure 3: We present a qualitative comparison of our OctMem-Agent and baseline methods on UAV-ON. OctMem-Agent maintains consistent detection throughout the entire sequence and successfully reaches the goal, while OpenFly-Agent gets stuck rotating in place and loses the target, and Navid fails to locate the object entirely. This highlights the effectiveness of our OctMem-Agent in achieving robust tracking and successful navigation*

### 消融实验

为解耦各组件的贡献，作者设计了递进式消融实验（**Table 3**）。基准模型（无任何记忆机制）的 SR 仅为 **12.40%**，OSR 为 20.60%。仅加入 **Adaptive Octree Memory** 后，SR 提升至 **15.70%**（+3.30 个百分点），OSR 微增至 21.10%。这验证了长期层次化记忆本身即可为导航决策提供有效的场景上下文。在此基础上进一步引入 **Instruction-Guided Memory Query**，SR 跃升至 **19.50%**（再 +3.80 个百分点），OSR 大幅提升至 **29.30%**（+8.20 个百分点），SPL 也从 4.35% 翻倍至 6.37%。该结果表明，指令调制的查询机制通过分离场景定位与前沿探索，显著改善了代理在复杂环境中的探索效率——代理不再盲目游荡，而是能根据任务语义有目的地选择搜索方向。

![[assets/figures/papers/paper_list_l2042_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Memory_Augmented/figures/004_Table_3.jpg]]
*Table 3: Ablation study on key components. We evaluate the impact of Adaptive Octree Memory Representation and Instruction-Guided Memory Query on model performance*

**Table 4** 对比了不同空间聚合策略的影响。标准体素化的 OSR 为 27.50%，SR 为 19.10%；而本文提出的 **层次化空间聚合**（Hierarchical Spatial Aggregation）将 OSR 提升至 **29.30%**（+1.80 个百分点），SR 微增至 19.50%，SPL 亦有提高。这一增益源于距离自适应体素化在近处保留细粒度细节、远处采用粗粒度概括，在保持紧凑记忆的同时兼顾了局部精度与全局覆盖。

**Table 5** 针对指令引导查询进行专项消融。移除指令调制查询（IMQ）后，SR 降至 **18.60%**（-0.90 个百分点），OSR 降至 **27.30%**（-2.00 个百分点），SPL 降至 5.97%。这说明通过 FiLM 将指令语义注入查询向量，能够有效引导记忆提取过程聚焦于任务相关区域，对探索效率的提升尤为关键。

### 瓶颈与失效分析

尽管 OctMem-Agent 取得了显著提升，其绝对成功率（19.50%）仍处于较低水平，反映出开放世界空中目标导航任务本身的极高难度。主要失效模式可归纳为：

1. **深度估计退化**：自适应八叉树记忆的构建强依赖 RGB-D 观测的准确性。在低纹理、动态光照或恶劣天气条件下，深度估计误差会逐帧累积，导致记忆表示失真，进而误导导航决策。
2. **仿真到现实的鸿沟**：当前实验仅限于 UAV-ON 仿真基准，尚未在真实无人机平台验证。真实场景中的传感器噪声、气动扰动和通信延迟等因素可能进一步降低系统可靠性。
3. **离散动作空间的局限**：动作空间限定为六个离散指令（前进、左转、右转、上升、下降、停止），忽略了连续飞行的动力学约束与避障需求，在狭窄或障碍物密集场景中可能无法生成安全轨迹。
4. **动态环境未覆盖**：实验场景为静态环境，未涉及移动障碍物或多智能体交互，方法的鲁棒性边界尚不明确。

### 小结

OctMem-Agent 通过自适应八叉树记忆与指令引导查询的协同设计，在 UAV-ON 基准上以 19.50% 的 SR 刷新了开放世界空中目标导航的最优结果。消融实验清晰表明，记忆机制贡献了约 3.3 个百分点的 SR 增益，而指令引导查询在此基础上进一步贡献约 3.8 个百分点的 SR 提升和 8.2 个百分点的 OSR 提升，是方法性能跃升的关键杠杆。层次化空间聚合以较小的计算代价提供了额外的探索效率改进。然而，绝对性能仍有巨大提升空间，深度估计鲁棒性、真实世界部署和动态环境适应是后续研究需要重点突破的方向。

### 补充图表

![[assets/figures/papers/paper_list_l2042_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Memory_Augmented/figures/003_Table_1.jpg]]
*Table 1: Performance comparison on the UAV-ON benchmark across different target object sizes. Our OctMem-Agent achieves the highest success rates across all object sizes and surpasses all baselines in total performance*

![[assets/figures/papers/paper_list_l2042_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Memory_Augmented/figures/007_Table_4.jpg]]
*Table 4: Ablation study on spatial aggregation methods. We compare our proposed Hierarchical Spatial Aggregation with standard voxelization baseline*

![[assets/figures/papers/paper_list_l2042_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Memory_Augmented/figures/006_Table_5.jpg]]
*Table 5: Ablation study on Instruction-Guided Memory Query. We compare performance with and without Instruction-Modulated Query (IMQ)*

## 定位与知识库关联

### 任务定位与基线谱系

OctMem-Agent 面向**开放世界空中目标导航**（Aerial Object-Goal Navigation），任务设定为：无人机仅依赖 RGB-D 视觉观测和高层语言目标描述（如“找到红色汽车”），在未知的大规模室外环境中自主导航至目标对象。该任务的核心挑战在于**长期记忆的构建与高效利用**——代理需要在数分钟的飞行中积累场景知识，同时平衡目标定位与未探索区域的探索。

现有方法可沿两条轴定位：

- **基于 VLM 的直接推理**：**OpenFly**（Gao et al., 2025）构建了首个开源航空 VLN 工具链，但仅使用当前帧与前两帧作为观测上下文，缺乏长期记忆机制。**Navid**（Zhang et al., 2024）处理视频序列以生成动作，本质上仍是对固定窗口内时序信息的编码，无法形成持久、可扩展的场景表示。**AOA-F**（Xiao et al., 2025）利用 LLM 进行导航决策，依赖近期位姿历史，同样受限于短期记忆。

- **零样本基线**：**CLIP-H** 直接利用 CLIP 视觉特征进行导航，无记忆与推理能力，性能最低（SR 仅 6.10%，Table 1）。

OctMem-Agent 的关键区分点在于**显式构建可扩展的 3D 场景记忆**：不同于上述方法将历史信息隐式编码于模型状态或短时序窗口中，OctMem-Agent 通过自适应八叉树记忆（Adaptive Octree Memory）将全部历史 RGB-D 观测增量聚合为层次化 3D 表示，使代理具备全局场景理解能力。

### 适用边界

方法的设计假设决定了其适用边界：

- **深度与位姿依赖**：八叉树记忆的构建依赖于准确的深度估计和位姿信息。在低纹理、动态光照或恶劣天气条件下，深度传感器和视觉里程计可能退化，导致记忆质量下降。这一限制在论文中已被明确列为局限性（Section 4.4）。

- **静态环境假设**：当前设计未显式建模动态障碍物或移动对象，八叉树记忆的增量更新策略假设场景结构基本稳定。在包含行人、车辆等动态元素的真实环境中，记忆可能包含过时信息。

- **离散动作空间**：动作空间限定为六种离散指令（前进、左转、右转、上升、下降、停止），简化了真实飞行中的连续控制问题，且未考虑避障与动力学约束。

- **仿真验证**：实验仅在 UAV-ON 仿真基准上进行，尚未在真实无人机平台和多传感器场景下验证。

### 局限与开放问题

论文明确指出的局限包括深度/位姿退化风险和仿真验证不足。此外，从方法设计和实验结果中可识别以下开放问题：

1. **多传感器融合**：如何融合 LiDAR、惯性测量等多传感器信息，以提高在低光、恶劣天气或纹理缺失区域下的深度估计鲁棒性？这是从仿真走向真实部署的关键一步。

2. **动态环境适应性**：方法是否能够推广到包含移动障碍物的动态环境？八叉树记忆的增量更新机制能否区分静态结构与瞬态对象？

3. **记忆可扩展性**：层次化八叉树记忆的内存占用和查询效率随场景规模的增长如何？在数平方公里级别的大规模场景中，是否需要进一步压缩或稀疏更新策略？

4. **零样本泛化**：当前方法能否将目标导航能力扩展到未见过的目标类别，而无需额外微调？CLIP 等视觉-语言模型提供了零样本识别的可能性，但如何与记忆机制有效结合仍待探索。

5. **多智能体协同**：方法是否可扩展到多无人机协同导航场景？多代理间的记忆共享与协作探索策略是潜在的研究方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Memory_Augmented_Scene_Understanding_and_Exploration_for_Open_World_Aerial_Object_Goal_Navigation.pdf]]
