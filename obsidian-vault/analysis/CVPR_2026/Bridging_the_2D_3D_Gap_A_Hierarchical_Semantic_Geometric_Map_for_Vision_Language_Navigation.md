---
title: "Bridging the 2D-3D Gap: A Hierarchical Semantic-Geometric Map for Vision Language Navigation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Bridging_the_2D_3D_Gap_A_Hierarchical_Semantic_Geometric_Map_for_Vision_Language_Navigation.pdf
project_link: null
code_link: "https://github.com/Teacher-Tom/HSGM_public"
aliases:
- HSGMH
- B23GHSGMVLN
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过构建分层语义-几何地图（HSGM），将3D环境信息转化为VLM可理解的2D BEV地图和可视化路径点，同时将高层语义推理与低层路径规划解耦，从而在不训练的情况下实现可靠的零样本导航。
primary_logic: 将3D几何信息通过多通道BEV地图可视化呈现，让VLM仅负责从离散路径点中做语义选择，低层移动交由经典A*算法，完全规避VLM的几何推理缺陷。
claims:
- HSGM在R2R-CE零样本设置下达到47.9%成功率，超过所有零样本方法和多个监督方法。
- 消融实验表明，完整HSGM地图（几何+语义+决策）相比仅BEV基线，SR从46.0%提升至51.0%。
- 移除子任务分解机制导致成功率大幅下降8.9%。
- 移除结构化CoT提示使SR从51.0%骤降至34.0%，下降17.0%。
---

# Bridging the 2D-3D Gap: A Hierarchical Semantic-Geometric Map for Vision Language Navigation

> [!tip] 核心洞察
> 将3D几何信息通过多通道BEV地图可视化呈现，让VLM仅负责从离散路径点中做语义选择，低层移动交由经典A*算法，完全规避VLM的几何推理缺陷。

| 字段 | 内容 |
|------|------|
| 中文题名 | 弥合2D-3D鸿沟：面向视觉语言导航的分层语义-几何地图 |
| 英文题名 | Bridging the 2D-3D Gap: A Hierarchical Semantic-Geometric Map for Vision Language Navigation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_Bridging_the_2D-3D_Gap_A_Hierarchical_Semantic-Geometric_Map_for_Vision_CVPR_2026_paper.html) · [Code](https://github.com/Teacher-Tom/HSGM_public) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | Hierarchical Semantic-Geometric Map (HSGM) |
| Dataset | R2R-CE Val-Unseen, RxR-CE Val-Unseen |

> [!tip] 效果简介
> - R2R-CE Val-Unseen 上，SR (%) 47.9 vs 32.8 (+15.1%)；SPL (%) 32.8 vs 28.9 (+3.9%)；SR (%) 47.9 vs 39.7 (+8.2%)。
> - RxR-CE Val-Unseen 上，SR (%) 41.8 vs 22.4 (+19.4%)。

## 概要

视觉语言导航（VLN）的核心瓶颈在于当前视觉语言模型（VLM）存在**语义-几何鸿沟**：VLM 缺乏对 3D 几何的深入理解，无法可靠地将自然语言指令与 3D 空间位置对齐，也难以将高层规划转化为可执行的底层动作序列，导致零样本导航不可靠。

针对这一问题，本文提出 **HSGM（Hierarchical Semantic-Geometric Map）**，一种无需训练的分层语义-几何地图框架。其核心思路是：将 3D 环境信息通过多通道 BEV 地图可视化呈现，使 VLM 仅负责从离散路径点中做语义选择，而底层移动交由经典 A* 算法执行，从而**完全规避 VLM 的几何推理缺陷**。具体而言，HSGM 将环境分解为三个层级——几何地图（可导航区域与障碍物）、语义地图（物体实例语义标注）和决策地图（全局路径点图与局部候选路径点），并通过 2D 栅格化与视角投影，为 VLM 提供结构化的视觉输入。

在 R2R-CE 和 RxR-CE 基准上的实验表明，HSGM 在零样本设置下分别达到 **47.9%** 和 **41.8%** 的成功率（SR），超越所有现有零样本方法，甚至优于多个监督方法。消融实验进一步验证了各层地图与解耦策略的关键贡献：完整 HSGM 地图相比仅 BEV 基线提升 5.0% SR，移除子任务分解机制导致 SR 下降 8.9%，而移除结构化 CoT 提示更使 SR 骤降 17.0%。



视觉语言导航（Vision-Language Navigation, VLN）要求智能体在真实3D环境中，根据自然语言指令自主移动至目标位置。近年来，视觉语言模型（VLM）的飞速发展使零样本导航成为可能——智能体无需在特定环境上训练，即可泛化到新场景。然而，当前VLM在VLN中存在一个根本性的瓶颈：**语义-几何鸿沟（semantic-geometric gap）**。

具体而言，VLM擅长从2D图像中提取语义信息，但缺乏对3D几何的深入理解。这导致两个关键失效模式：其一，VLM难以将指令中的语义锚点（如“走到沙发旁”）可靠地与3D空间中的位置对齐；其二，VLM不擅长将高层规划转化为可执行的低层动作序列（如“左转15度，前进0.5米”）。现有零样本方法多依赖VLM直接从RGB图像预测动作，或基于简单的2D语义图做决策，在复杂环境中导航可靠性不足。

本文的核心洞察是：**将3D几何信息通过结构化地图可视化呈现，让VLM仅负责语义层面的路径点选择，而将几何计算完全交由经典规划算法处理**。这一解耦策略从根本上规避了VLM的几何推理缺陷，同时保留了其在语义理解上的优势。为落实这一洞察，本文提出HSGM（Hierarchical Semantic-Geometric Map），一种无需训练即可弥合2D-3D鸿沟的分层语义-几何地图框架。



## 核心方法与创新机理

HSGM的核心创新在于**将VLM从几何推理的任务中彻底解放**，通过构建一种分层语义-几何地图，将3D世界的空间信息转化为VLM可理解的2D视觉提示，同时将高层语义规划与低层运动控制完全解耦。

### 从端到端预测到解耦规划

现有VLM导航方法（如**MapNav** (Zhang et al., ACL 2025)、**AO-Planner** (Chen et al., AAAI 2025)）通常要求VLM直接预测低层动作（如转向角度、移动距离），或基于2D图像进行可达性判断。这种设计将语义理解与几何推理混杂在一起，迫使VLM承担其不擅长的精确空间计算任务，导致零样本导航不可靠。

HSGM的核心洞察在于：**VLM的真正优势在于语义理解和选择，而非几何推理**。基于此，HSGM做出了三个关键改变：

1. **场景表示**：从无结构化地图或简单2D语义图，升级为包含几何层、语义层和决策层的**分层语义-几何地图（HSGM）**。该地图将3D环境的可导航区域、障碍物、物体语义和路径点信息统一建模，并栅格化为多通道2D鸟瞰图（BEV），使VLM无需理解3D几何即可感知空间结构。

2. **运动规划与执行**：从VLM直接预测低层动作，转变为**VLM仅从3D地图采样的离散路径点中做高层选择**。所有路径点之间的实际移动交由经典A*算法在预构建的全局路径点图上执行。这一设计完全规避了VLM的几何推理缺陷——VLM只需回答“去哪个路径点”，而非“如何移动”。

3. **指令处理**：从一次性处理整个指令，转变为**将复杂指令分解为有序子任务**，并引入双重确认和自动回溯机制。子任务具有明确的状态管理（done/pending/in progress），当子任务超时或失败时，Agent自动回溯到上一个子任务重新执行，大幅提升了长指令导航的鲁棒性。

### 因果机制

HSGM的性能提升并非来自更强的VLM或更多训练数据，而是来自**架构层面的能力解耦**：

- **几何地图**提供空间骨架，确保路径点在几何上可达；
- **语义地图**赋予物体语义标签，使VLM能进行目标导向的推理；
- **决策地图**将连续导航空间离散化为有限路径点集，将VLM的决策简化为“选择题”；
- **结构化CoT提示**引导VLM按照“当前状态→子任务目标→候选路径点分析→最优选择”的链条进行推理，确保决策过程可解释且一致。

消融实验直接验证了这一因果链条：完整HSGM地图（几何+语义+决策）相比仅BEV基线，成功率从46.0%提升至51.0%（+5.0%）；移除结构化CoT提示后，成功率骤降至34.0%（-17.0%）；移除子任务分解机制导致成功率下降8.9%。这些结果表明，**HSGM的每一项设计都在弥补VLM与3D世界之间的语义-几何鸿沟**。



HSGM 的整体框架围绕一个核心设计原则构建：**将高层语义推理与低层几何执行彻底解耦**。如图2所示，系统由四个串行阶段组成，形成一条从自然语言指令到最终动作序列的完整闭环。

### 指令分解

导航开始时，用户输入的自然语言指令 $I$ 首先由一个大语言模型（LLM）分解为有序的子任务序列 $\mathcal{T} = \{T_1, \ldots, T_k\}$。每个子任务维护三种状态之一：`done`（已完成）、`pending`（待执行）或 `in progress`（执行中）。这种分解机制将复杂的长指令转化为可逐步验证的短目标，是后续结构化推理的基础。

### 分层地图构建

在每个时间步 $t$，智能体通过三视图（前、左、右）RGB-D传感器获取观测 $\overline{O_t} = \{V_t^i\}_{i=1}^3$，其中 $V_t^i = (I_t^{i, \mathrm{RGB}}, I_t^{i, \mathrm{D}})$。这些多模态数据与相机位姿一同被送入三维重建管线，动态构建**分层语义-几何地图（HSGM）**，包含三个层级：

1. **几何地图** $M_{\mathrm{geo}}$：通过反向投影多视图RGB-D图像构建三维点云，提取可导航区域 $P_{\mathrm{nav}}$（含楼梯区域 $P_{\mathrm{stair}}$）和障碍物 $P_{\mathrm{obs}}$，形成空间骨架。
2. **语义地图** $M_{\mathrm{sem}} = \{(P_{\mathrm{obj},j}, c_j)\}_{j=1}^{N_{\mathrm{obj}}}$：使用YOLO-E实例分割模型获取物体语义标签，投影至三维空间并通过3D IoU进行多帧融合。
3. **决策地图** $\mathcal{M}_{\mathrm{dec}} = \{G, A_{\mathrm{curr}}\}$：在可导航点云上采样离散路径点，构建全局路径点图 $G$（供A*规划）和当前局部路径点集 $A_{\mathrm{curr}}$（供VLM选择）。

### 2D BEV栅格化与视觉提示

为弥合3D几何信息与VLM的2D视觉理解之间的鸿沟，HSGM将三维地图**栅格化**为以智能体为中心的多通道2D鸟瞰图（BEV Map）。同时，局部路径点被赋予数字索引，并**投影**到BEV地图和智能体的前向第一人称视角上，作为视觉提示（visual prompts）直接嵌入VLM的输入空间。

### 解耦导航执行

导航策略被明确分为两层：

- **VLM高层规划器**：以BEV地图和投影路径点为视觉输入，执行结构化思维链（Chain-of-Thought, CoT）推理，从动作空间 $A_t = A_{\mathrm{turn}} \cup A_{\mathrm{curr}}$ 中选择最优路径点，或输出 `STOP`。VLM仅负责语义层面的离散选择，不参与任何几何计算。
- **A*低层控制器**：接收VLM选定的目标路径点后，在预构建的全局图 $G = (V, E)$ 上运行A*算法计算最短路径 $\tau_{\mathrm{path}}$，并执行底层的连续动作序列。

### 子任务管理与回溯

框架内嵌了**双重确认机制**：对于最终子任务，VLM需连续两次输出 `STOP` 才能终止导航，防止过早停止。当某一子任务的步数超出限制时，智能体**自动回溯**至上一子任务重新执行，形成闭环纠错能力。

### 补充图表

![[assets/figures/papers/paper_list_l2179_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Bridging_the_2D_3D/figures/001_Figure_1.jpg]]
*Figure 1: Our proposed Hierarchical Semantic-Geometric Map (HSGM). The 3D environment is modeled via three maps: Geometry, Semantic, and Decision. It is then rasterized into a 2D BEV Map and projected as visual prompts onto the agent’s view, serving as the structured visual input for the VLM*

![[assets/figures/papers/paper_list_l2179_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Bridging_the_2D_3D/figures/002_Figure_2.jpg]]
*Figure 2: Framework Overview. (1) A LLM decomposes the user instruction into a sequence of subtasks. (2) The agent’s sensor data (RGB-D, pose) is used to dynamically construct the 3D Hierarchical Semantic-Geometric Map. (3) The HSGM is rasterized into a 2D BEV map and projected onto the front view of the agent as visual input for the VLM. (4) The VLM performs CoT reasoning to select a waypoint, and the*



HSGM 框架围绕一个核心洞察展开：**将 3D 几何信息转化为 VLM 可理解的 2D 视觉表征，让 VLM 仅负责高层语义选择，底层路径规划完全交由经典 A* 算法执行**。这一解耦设计使 VLM 彻底规避了其固有的几何推理缺陷。以下依次阐述关键模块与核心公式。

---

### 3.1 任务形式化

视觉语言导航任务可形式化为策略函数：

$$a_{t} = \pi_{\theta}(I, \overline{O_{t}}, H_{t})$$

其中 $I$ 为自然语言指令，$H_t$ 为历史上下文，$\overline{O_t}$ 为 $t$ 时刻的多视图观测，由前、左、右三视角的 RGB-D 图像组成：

$$\overline{O_{t}} = \{V_{t}^{i}\}_{i=1}^{3}, \quad V_{t}^{i} = \big(I_{t}^{i, \mathrm{RGB}}, I_{t}^{i, \mathrm{D}}\big)$$

HSGM 的核心创新在于将策略 $\pi_{\theta}$ 解耦为**高层 VLM 规划器**与**低层 A* 执行器**，前者仅从离散路径点中做语义选择，后者负责连续空间中的路径计算与动作执行。

---

### 3.2 指令分解模块（Subtask Decomposition）

复杂指令 $I$ 首先由 LLM 分解为有序子任务序列 $\mathcal{T} = \{T_1, \ldots, T_k\}$，每个子任务维护三种状态：`done`、`pending`、`in progress`。该模块还引入**双重确认机制**：对于最终子任务，VLM 需连续两次输出 `STOP` 才判定任务完成，防止过早终止。若子任务执行超出步数限制，智能体将**自动回溯**至上一子任务的起始位置重新尝试。

---

### 3.3 分层语义-几何地图（HSGM）构建

HSGM 是框架的核心表征，由三个层次组成：

**几何地图 $M_{\mathrm{geo}}$**：基于多视图 RGB-D 图像和相机位姿，将像素反投影至 3D 空间构建点云。定义障碍物 $P_{\mathrm{obs}}$、可通行区域 $P_{\mathrm{nav}}^{\mathrm{init}}$，并检测楼梯区域 $P_{\mathrm{stair}}$。最终可导航点云为：

$$P_{\mathrm{nav}} = P_{\mathrm{nav}}^{\mathrm{init}} \cup P_{\mathrm{stair}}$$

几何地图由可导航区域与障碍物点云并集构成：

$$M_{\mathrm{geo}} = P_{\mathrm{nav}} \cup P_{\mathrm{obs}}$$

**语义地图 $M_{\mathrm{sem}}$**：使用 YOLO-E 实例分割模型获取物体语义，反投影至 3D 空间，并通过 3D IoU 融合多帧观测中的同一实例：

$$M_{\mathrm{sem}} = \{ (P_{\mathrm{obj},j}, c_j) \}_{j=1}^{N_{\mathrm{obj}}}$$

其中 $P_{\mathrm{obj},j}$ 为第 $j$ 个物体实例的点云，$c_j$ 为其类别标签。

**决策地图 $\mathcal{M}_{\mathrm{dec}}$**：在可导航点云上离散化生成路径点，包含两个组件：

$$\mathcal{M}_{\mathrm{dec}} = \{ G, A_{\mathrm{curr}} \}$$

- **全局路径点图 $G = (V, E)$**：用于 A* 全局规划。节点 $v \in V$ 的有效性通过圆柱体占用检查验证：

$$P_{\mathrm{obs}} \cap \mathrm{Cyl}(p_c, r, h) = \emptyset$$

即以节点中心 $p_c$ 为圆心、半径 $r$、高度 $h$ 的圆柱体内无任何障碍物。

- **局部路径点集 $A_{\mathrm{curr}}$**：从当前智能体位置附近的全局节点中采样，作为 VLM 的候选动作空间。

---

### 3.4 2D BEV 栅格化与视觉提示投射

3D HSGM 被栅格化为以智能体为中心的多通道 2D 鸟瞰图（BEV Map），各通道分别编码几何层（可通行/障碍/楼梯）、语义层（物体类别）和决策层（路径点位置）。局部路径点以数字索引标注，并同时投射到 BEV 地图和智能体的前向第一人称视角，形成 VLM 的结构化视觉输入。

---

### 3.5 解耦导航：VLM 规划器与 A* 执行器

**高层 VLM 规划器**：VLM 接收 BEV 地图和投射路径点作为视觉输入，通过**结构化链式思维（CoT）推理**从动作空间 $A_t = A_{\mathrm{turn}} \cup A_{\mathrm{curr}}$ 中选择最优动作，或输出 `STOP`。VLM 仅负责语义层面的路径点选择，不涉及任何连续运动控制。

**低层 A* 执行器**：一旦 VLM 选定目标路径点，A* 算法在预构建的全局图 $G = (V, E)$ 上计算最短路径 $\tau_{\mathrm{path}}$，并执行底层动作序列。这一设计将几何推理完全外包给经典规划算法，VLM 的几何能力不再是瓶颈。

---

### 关键公式速查

| 公式 | 含义 | 所属模块 |
|------|------|----------|
| $a_t = \pi_\theta(I, \overline{O_t}, H_t)$ | 导航策略形式化定义 | 任务建模 |
| $\overline{O_t} = \{V_t^i\}_{i=1}^3$ | 三视图 RGB-D 观测 | 感知输入 |
| $P_{\mathrm{nav}} = P_{\mathrm{nav}}^{\mathrm{init}} \cup P_{\mathrm{stair}}$ | 可导航区域含楼梯 | 几何地图 |
| $M_{\mathrm{geo}} = P_{\mathrm{nav}} \cup P_{\mathrm{obs}}$ | 几何地图定义 | 几何地图 |
| $M_{\mathrm{sem}} = \{(P_{\mathrm{obj},j}, c_j)\}_{j=1}^{N_{\mathrm{obj}}}$ | 语义地图定义 | 语义地图 |
| $\mathcal{M}_{\mathrm{dec}} = \{G, A_{\mathrm{curr}}\}$ | 决策地图定义 | 决策地图 |
| $P_{\mathrm{obs}} \cap \mathrm{Cyl}(p_c, r, h) = \emptyset$ | 路径点圆柱体占用检查 | 决策地图 |



## 实验与关键发现

### 核心实验设置

所有实验在 VLN-CE 的两个标准基准上评测：**R2R-CE** 和 **RxR-CE**。HSGM 为零样本框架，不使用模拟器标注数据进行训练，直接部署 VLM 进行推理。评测指标采用导航任务通用的 Success Rate (SR) 和 Success weighted by Path Length (SPL)。对比方法中，带“*”标记的方法（如 **MapNav** (Zhang et al., ACL 2025)）部分依赖模拟器标注数据训练，须注意公平比较的边界。

### 主实验结果

**Table 1** 汇总了 R2R-CE 和 RxR-CE 的 Val-Unseen 结果。

在 **R2R-CE** 上，HSGM 以 **47.9% SR** 和 **32.8% SPL** 取得零样本方法的最优性能，超过此前最佳的零样本方法 **DreamNav** 达 15.1% SR 和 3.9% SPL。更值得注意的是，HSGM 在零样本设定下已超越多个监督方法，包括 **MapNav** (39.7% SR, 监督) 和 **NaVid** (37.4% SR, 监督)，与监督方法中的最优水平差距大幅缩小。

在指令更长、语言更复杂的 **RxR-CE** 上，HSGM 的优势更为显著：**41.8% SR**，几乎为 **AO-Planner** (Chen et al., AAAI 2025) 的 22.4% 的两倍。该结果验证了分层地图与子任务分解机制对复杂指令的鲁棒处理能力。

### 消融实验

消融实验从两个维度展开：地图层级的贡献（**Table 2**）和导航策略关键组件的贡献（**Table 3**），均基于 R2R Val-Unseen。

![[assets/figures/papers/paper_list_l2179_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Bridging_the_2D_3D/figures/006_Table_2.jpg]]
*Table 2: Ablation study of HSGM map in the BEV map*

![[assets/figures/papers/paper_list_l2179_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Bridging_the_2D_3D/figures/004_Table_3.jpg]]
*Table 3: Ablation study on key components of decoupled navigation strategy. All variants are evaluated on R2R Val-Unseen*

#### 地图层级消融

以仅含基础 BEV 视觉输入的模型为基线（SR 46.0%），逐层叠加 HSGM 的三个地图通道：

- **加入几何地图**（障碍物 + 可导航区域）：SR 提升至 47.3%（+1.3%），验证了 3D 几何信息对路径规划的基础支撑。
- **加入语义地图**（物体实例语义）：SR 进一步提升至 49.2%（+1.9%），表明物体语义能有效辅助 VLM 将指令中的地标与空间位置对齐。
- **完整 HSGM（几何 + 语义 + 决策地图）**：SR 达到 **51.0%**（+5.0% vs. 基线），其中决策地图贡献额外 +1.8%。决策地图提供的离散路径点集将 VLM 的推理空间从连续动作压缩为有限选择，是性能跃升的关键瓶颈突破点。

#### 导航策略组件消融

以完整 HSGM 模型（SR 51.0%）为基准，逐一移除关键机制：

- **移除子任务分解**：SR 骤降 **8.9%**。该结果与 **Figure 3** 的按指令长度分桶分析一致——指令越长（token 数越多），子任务分解带来的增益越明显，说明分解机制有效缓解了 VLM 在长指令上的规划崩溃问题。
- **移除结构化 CoT 提示**：SR 从 51.0% 暴跌至 34.0%，降幅达 **17.0%**。这是所有消融中影响最大的单一因素，表明结构化推理链是 VLM 将视觉感知转化为可靠空间决策的核心机制。
- **移除自动回溯**：Table 4 展示了回溯机制的触发率与恢复成功率。当子任务步数超限时，自动回溯使部分即将失败的导航得以恢复，对最终 SR 有正向贡献。

![[assets/figures/papers/paper_list_l2179_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Bridging_the_2D_3D/figures/005_Figure_3.jpg]]
*Figure 3: Impact of Subtask Decomposition on Success Rate by Instruction Token Count*

![[assets/figures/papers/paper_list_l2179_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Bridging_the_2D_3D/figures/007_Table_4.jpg]]
*Table 4: Effectiveness of the Automatic Backtracking Mechanism. The table shows the percentage of episodes where backtracking was triggered (Trigger Rate) and the success rate of those recovered episodes (Recovery SR)*

### 关键图表结论

- **Table 1**：HSGM 以零样本设定在 R2R-CE (47.9% SR) 和 RxR-CE (41.8% SR) 上均超越所有零样本方法及部分监督方法。
- **Table 2**：几何、语义、决策三层地图各自对 SR 有正向贡献，完整 HSGM 较基线提升 5.0%。
- **Table 3**：子任务分解（-8.9%）和 CoT 提示（-17.0%）是导航成功率的两个最关键支柱。
- **Figure 3**：子任务分解对长指令的增益更大，证实了其缓解长期规划退化问题的能力。
- **Table 4**：自动回溯机制能在一定比例上恢复失败轨迹，提升系统鲁棒性。

![[assets/figures/papers/paper_list_l2179_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Bridging_the_2D_3D/figures/003_Table_1.jpg]]
*Table 1: Navigation performance on R2R-CE and RxR-CE benchmarks. “*” indicates that this method requires partial reliance on the simulator’s labeled data for training. Best zero-shot results are marked in bold, and the second-best is underlined*

### 失败模式与局限

尽管 HSGM 在零样本设定下表现优异，其架构仍存在可识别的失败模式：

1. **深度与位姿依赖**：几何地图的构建依赖 RGB-D 深度图和精确的相机位姿。当深度估计噪声较大或位姿漂移时，可导航区域和障碍物边界会出现偏差，导致路径点采样错误或 A* 规划失败。当前框架未验证在纯单目或 SLAM 位姿下的鲁棒性。
2. **静态环境假设**：A* 低层控制器基于预构建的全局路径点图执行，无法感知或规避移动障碍物。在动态环境中，该机制可能导致碰撞或路径阻塞。
3. **子任务分解质量**：指令分解由 LLM 一次性完成，若初始分解不合理（如子任务粒度过粗或遗漏关键步骤），VLM 高层规划器缺乏在线修正分解的能力，会导致整条轨迹失败。

### 补充图表

![[assets/figures/papers/paper_list_l2179_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Bridging_the_2D_3D/figures/008_Figure_4.jpg]]
*Figure 4: Navigation visualization of HSGM*



## 定位与知识库关联

### 1. 与现有基线的谱系关系

HSGM处于“零样本视觉语言导航（VLN）与结构化场景表示”的交叉节点。与现有工作的关键差异在于，它不试图让VLM直接预测低层动作，而是通过构建显式的分层语义-几何地图，将VLM的角色严格限定为高层语义规划器。

**与零样本VLM导航方法的关系**：现有零样本方法大多依赖VLM从第一人称RGB图像中直接推理动作。**AO-Planner**（Chen et al., AAAI 2025）和**DreamNav**代表了这一范式——前者在R2R-CE上达到32.8% SR，后者为32.8% SR（Table 1）。HSGM以47.9% SR显著超越这些方法（+15.1%），其核心突破在于用BEV地图替代了纯第一人称视角，使VLM获得了对环境拓扑的全局感知。在RxR-CE基准上，HSGM的41.8% SR几乎是AO-Planner（22.4%）的两倍，表明结构化地图对长指令场景的增益更为突出。

**与监督学习方法的关系**：HSGM作为零样本框架，甚至超越了部分依赖模拟器标注数据训练的监督方法。**MapNav**（Zhang et al., ACL 2025）在R2R-CE上达到39.7% SR，HSGM以47.9%领先8.2个百分点。**NaVid**（监督基线）的性能同样被HSGM超越。这表明，精心设计的地图表征与规划解耦策略，可以在不引入训练偏差的情况下，达到甚至超过从标注数据中学习的策略。

**与基于地图的导航方法的关系**：HSGM与经典地图导航方法（如占用栅格地图+几何规划）共享“先建图后规划”的思想，但引入了两个关键升级：（1）将3D几何信息栅格化为VLM可理解的多通道2D BEV图像，实现了语义与几何的桥接；（2）在决策层引入全局路径点图$G$和局部路径点集$A_{\mathrm{curr}}$的双层结构，使得A*算法可以在全局图上规划最短路径，而VLM仅需从局部候选集中做语义选择。

### 2. 方法适用边界

HSGM的有效性依赖于以下前提条件，这些条件定义了其适用边界：

- **传感器要求**：方法假设可获取多视图RGB-D图像和精确的相机位姿（公式$\overline{O_{t}} = \{V_{t}^{i}\}_{i=1}^{3}$，其中每视图包含RGB和深度图）。在深度估计噪声较大或位姿漂移严重的场景下，3D点云重建质量将直接影响地图精度。
- **环境假设**：几何地图构建基于静态环境假设——可导航区域$P_{\mathrm{nav}}$和障碍物$P_{\mathrm{obs}}$被假定为在单次导航任务中保持不变。对于存在移动障碍物或动态变化的场景，A*规划器缺乏实时重规划能力。
- **VLM能力依赖**：高层规划完全依赖VLM的语义推理能力。结构化CoT提示的消融实验表明，移除CoT后SR从51.0%骤降至34.0%（-17.0%），说明方法对VLM的指令理解与推理能力高度敏感。在VLM能力较弱的模型上，性能可能显著退化。
- **子任务分解质量**：指令分解模块依赖LLM将自然语言指令切分为有序子任务。对于高度模糊、多义或需要复杂空间推理的指令，分解质量可能成为瓶颈。Figure 3按指令长度分桶的分析为此提供了证据——子任务分解对长指令的增益更为显著，但也意味着分解错误在长指令中可能产生更严重的级联效应。

### 3. 局限与开放问题

**已识别的局限**：

- **动态环境适应性不足**：当前框架的几何地图是静态构建的，A*规划器在遇到移动障碍物时缺乏在线避障能力。这是纯几何规划方法的固有局限。
- **传感器依赖性强**：对深度图和位姿的精确依赖限制了方法在轻量化硬件（如单目RGB相机）上的部署可能性。
- **子任务粒度的鲁棒性**：消融实验显示，移除子任务分解机制导致SR下降8.9%，而自动回溯机制虽能恢复部分失败（Table 4），但其恢复成功率的具体水平需查看原文确认。这表明子任务管理策略仍有优化空间。

**开放问题**：

1. **轻量化建图**：在不依赖精确深度和位姿的条件下，能否通过单目视觉或神经隐式映射（如NeRF-based方法）构建类似HSGM的结构化表示？这将显著扩展方法的硬件适用范围。
2. **端到端表征学习的融合**：HSGM的解耦规划策略能否与可学习的场景表征相结合？例如，用可训练的编码器替代手工设计的BEV栅格化，可能进一步提升长轨迹导航中的泛化能力。
3. **动态环境扩展**：对于移动障碍物或动态环境，纯几何A*规划如何扩展以保持鲁棒性？可能的路径包括引入局部重规划模块，或在决策地图中编码动态置信度。
4. **跨具身迁移**：HSGM的地图构建逻辑是否可泛化到不同形态的机器人平台（如四足机器人、无人机）？这需要验证可导航区域定义和路径点采样策略的跨平台适应性。



## 原文 PDF

![[paperPDFs/CVPR_2026/Bridging_the_2D_3D_Gap_A_Hierarchical_Semantic_Geometric_Map_for_Vision_Language_Navigation.pdf]]
