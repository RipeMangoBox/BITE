---
title: "TrajRAG: Retrieving Geometric-Semantic Experience for Zero-Shot Object Navigation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TrajRAG_Retrieving_Geometric_Semantic_Experience_for_Zero_Shot_Object_Navigation.pdf
project_link: null
code_link: null
aliases:
- TrajRAG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 将历史导航轨迹转化为紧凑的拓扑-极坐标表示，并通过层次化分块和粗到细检索，为当前决策提供相关几何-语义经验。
primary_logic: 通过拓扑极坐标轨迹表示和层次化检索增强生成，将离散的、冗余的导航片段转化为可复用、可匹配的几何-语义经验，并注入大模型推理过程，使智能体能够借鉴以往经验提升零样本导航能力。
claims:
- TrajRAG通过增量积累和检索几何-语义经验，提高了零样本ObjectNav的性能。
- 拓扑-极坐标轨迹表示紧凑编码空间布局和语义上下文。
- 层次化分块结构支持粗到细检索。
- TrajRAG在MP3D、HM3Dv1和HM3Dv2上达到最优成功率和SPL。
---

# TrajRAG: Retrieving Geometric-Semantic Experience for Zero-Shot Object Navigation

> [!tip] 核心洞察
> 通过拓扑极坐标轨迹表示和层次化检索增强生成，将离散的、冗余的导航片段转化为可复用、可匹配的几何-语义经验，并注入大模型推理过程，使智能体能够借鉴以往经验提升零样本导航能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | TrajRAG: 面向零样本物体导航的几何-语义经验检索 |
| 英文题名 | TrajRAG: Retrieving Geometric-Semantic Experience for Zero-Shot Object Navigation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.01700) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | TrajRAG |
| Dataset | MP3D, HM3D-v1, HM3D-v2 |

> [!tip] 效果简介
> - MP3D 上，SR(%) / SPL(%) 42.6 / 18.0。
> - HM3D-v1 上，SR(%) / SPL(%) 62.5 / 33.9。
> - HM3D-v2 上，SR(%) / SPL(%) 78.1 / 40.2。

## 概要

零样本物体导航（Zero-Shot ObjectNav）要求智能体在未见过的三维环境中，仅凭开放词汇物体目标（如“找一个沙发”）进行搜索。现有方法——无论是依赖单步观测的LLM/VLM规划器，还是利用回合内记忆的场景图方法——都面临一个共同瓶颈：**决策完全依赖大模型中与场景无关的常识知识，缺乏对三维空间布局和物体共现关系的长期经验积累**，导致策略缺乏场景针对性，且每轮导航结束后经验被丢弃，无法复用。

TrajRAG 将这一瓶颈转化为一个**检索增强生成（RAG）问题**：将历史导航轨迹转化为可存储、可检索、可匹配的几何-语义经验，在导航过程中为当前决策提供场景相关的历史先例。其核心洞察在于，通过**拓扑-极坐标轨迹表示**和**层次化检索增强生成**，将离散冗余的导航片段压缩为紧凑的结构化经验，并注入大模型推理过程，使智能体能够“借鉴以往经验”提升零样本导航能力。

该方法在三个主流基准上取得了最优结果：MP3D 上成功率达 42.6% / SPL 18.0%，HM3D-v1 上 62.5% / 33.9%，HM3D-v2 上 78.1% / 40.2%，验证了几何-语义经验检索对零样本导航的有效性。

**零样本物体导航（Zero-Shot ObjectNav）** 要求智能体在未见过的三维环境中，仅凭开放词汇物体类别（如“找到一张床”）就能定位并到达目标。近年来，基于大语言模型（LLM）或视觉语言模型（VLM）的方法在此任务上取得了显著进展，其核心范式是将当前观测转化为文本或视觉提示，交由大模型进行常识推理以选择下一步航点。

然而，现有方法存在一个根本性的瓶颈：**决策完全依赖大模型中编码的场景无关常识，缺乏对三维空间布局和物体共现关系的长期经验积累**。具体表现为以下三个层次的问题：

1. **单步上下文方法**（如早期LLM-based导航）：仅将当前时刻的原始观测输入规划器，完全丢弃历史导航中积累的空间结构信息，导致对场景整体布局的认知缺失（图1a）。

2. **情节上下文方法**（如 **VoroNav** (Wu et al., ICML 2024)、**VLFMap** (Yokoyama et al., ICRA 2024)、**SG-Nav** (Yin et al., NeurIPS 2024) 等）：虽然将当前导航情节的记忆结构化为提示用于推理，但在每个情节结束后即丢弃所有经验（图1b）。这意味着智能体每次进入新环境都从零开始，无法借鉴先前在相似布局场景中的成功经验。

3. **缺乏可复用的经验表示**：即使保留了历史轨迹，原始的RGB-D序列或场景图表示过于冗余，难以高效存储、索引和匹配。现有方法未能将离散的导航片段转化为紧凑、可比较、可检索的几何-语义经验单元。

上述缺口导致零样本导航方法在面对复杂场景时决策缺乏针对性——智能体可能重复犯下相似的探索错误，无法利用“在类似布局中目标物体通常出现在哪些区域”这类从经验中可习得的空间先验。

**TrajRAG** 的提出正是为了填补这一缺口。其核心动机是：如果能够将每次导航的轨迹转化为紧凑的表示并持续积累，在后续导航中检索与之空间布局和语义上下文相似的历史经验，注入大模型推理过程，就能使智能体“借鉴以往经验”提升零样本导航的决策质量（图1c）。这一思路将检索增强生成（RAG）范式从文本领域拓展至具身导航的几何-语义空间，为终身经验学习提供了新的技术路径。

## 核心方法与创新机理

TrajRAG 的核心创新在于**将零样本物体导航从“仅依赖大模型常识”的瞬时推理范式，转变为“检索历史几何-语义经验辅助决策”的记忆增强范式**。现有 LLM/VLM 基线方法（如 **VoroNav** (Wu et al., ICML 2024)、**SG-Nav** (Yin et al., NeurIPS 2024)、**BeliefMapNav** (Zhou et al., NeurIPS 2025)）在每轮导航中仅利用单步观测或片段记忆构建提示，导航结束后即丢弃所有经验，缺乏对三维空间布局与物体共现关系的长期积累。TrajRAG 通过三个关键 changed slot 填补了这一空白：

**1. 轨迹表示：从原始序列到拓扑-极坐标轨迹**

基线方法通常将导航历史表示为原始 RGB-D 序列或场景图，信息冗余且难以跨场景匹配。TrajRAG 提出**拓扑-极坐标（topo-polar）轨迹表示**：首先对语义地图的可通行区域进行骨架化提取拓扑节点（8邻域连通分量数 ≥3 的骨架像素，见 Eq. (1)），然后在每个节点处沿 12 个均匀方向进行极坐标射线采样，根据射线命中目标类别、障碍物、未知区域或自由空间返回离散标签（Eq. (2)），形成 12 维扇区向量（Eq. (3)）。该表示**紧凑编码了局部空间布局与语义上下文**，同时通过循环旋转扇区向量计算旋转不变相似度（Eq. (8)），解决了不同场景间朝向偏差带来的匹配困难。

**2. 长期记忆：从“用后即弃”到层次化分块存储**

基线方法在每轮导航后丢弃所有观测，无法积累经验。TrajRAG 构建**层次化分块存储架构**：将每条拓扑-极坐标轨迹组织为 chunk，按几何-语义相似性分组并维护粗索引（组摘要图）；每个 chunk 经 encoder-decoder 变换器编码为嵌入向量 $\mathbf{z} = \mathbf{h}_L' \oplus \mathbf{h}_{\mathrm{g}}$（Eq. (6)），通过对比学习损失（Eq. (7)）训练以增强匹配判别力。导航结束后，新轨迹被整合进 TrajRAG，实现**终身经验积累**。

**3. 检索与推理：从纯常识推理到粗到细经验检索增强**

基线方法完全依赖大模型内置的场景无关常识进行航点选择。TrajRAG 在导航中执行**粗到细检索**：粗检索阶段利用当前拓扑-极坐标轨迹的几何-语义特征快速定位高相似度组，细检索阶段通过序列嵌入精确匹配最相关的历史轨迹片段。检索到的经验（包括布局一致场景和目标达成轨迹）被注入大模型提示中，辅助其估计各候选轨迹到达目标的效率，从而做出更具场景针对性的决策。

这三个 changed slot 相互耦合形成闭环：紧凑的拓扑-极坐标表示使大规模轨迹存储和高效检索成为可能，层次化分块架构支撑了粗到细的检索效率，而检索到的经验又通过大模型推理反哺导航决策，最终使零样本导航从“无记忆的常识猜测”升级为“有经验的场景推理”。

TrajRAG 将零样本物体导航重新定义为**检索增强生成（RAG）**问题，其核心思路是将历史导航经验转化为可复用、可匹配的几何-语义记忆，并在推理阶段注入大模型辅助决策。整体框架由一条贯穿“建图—表示—索引—检索—推理—积累”的闭环管线构成，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2649_https_arxiv_org_abs_2605_01700/figures/002_Figure_2.jpg]]
*Figure 2: Navigation Framework of TrajRAG. The agent incrementally maintains a semantic map during navigation. Based on this map, we convert the explored area into a topo-polar trajectory. Candidate trajectories are then generated according to the potential frontiers. For each candidate, TrajRAG retrieves relevant experiences to help the planner estimate which trajectory can reach the goal more efficiently. A coarse-to-fine retrieval strategy is adopted to accelerate retrieval*

### 管线总览

1. **语义建图**：智能体在导航过程中增量式地从 RGB-D 观测构建开放词汇语义地图 $\mathcal{M}_t \in \mathbb{R}^{(2+N_o) \times H \times W}$，其中通道分别编码障碍物、已探索区域和 $N_o$ 类物体语义。
2. **拓扑-极坐标轨迹提取**：对已探索区域进行形态学骨架化，提取拓扑关键节点 $\mathcal{V}_{\mathrm{cand}}$（8-邻域连通分量数 ≥ 3），并对每个节点沿 12 个方向进行极坐标射线采样，得到扇区向量 $\mathbf{s}_k$，形成紧凑的拓扑-极坐标轨迹 $\mathcal{T}_{\mathrm{tp}}$。
3. **层次化分块与索引**：TrajRAG 将轨迹组织为**块（chunk）**，并构建两层索引：
   - **粗索引**：按几何-语义相似性对块进行分组，建立粗粒度检索入口；
   - **细索引**：使用编码器-解码器 Transformer（如 DistilBERT + DistilGPT2）将每个块编码为嵌入 $\mathbf{z} = \mathbf{h}'_L \oplus \mathbf{h}_g$，并通过对比学习损失 $\mathcal{L}_{\mathrm{contrast}}$ 优化嵌入空间。
4. **经验检索**：导航过程中，基于当前部分轨迹生成候选轨迹，执行**粗到细检索**——先定位相似组，再在组内进行细粒度序列匹配，返回最相关的历史轨迹块。
5. **大模型决策**：检索到的几何-语义经验被注入策略模型（如 LLM），辅助其选择下一航点。
6. **终身积累**：每个 episode 结束后，完整轨迹被整合进 TrajRAG 知识库，组摘要图 $\mathcal{G}_{\mathrm{sum}}$ 同步更新，实现经验的持续增长。

### 与现有范式的关键差异

Figure 1 明确对比了三种上下文模式：
- **单步上下文**（VoroNav 等）：LLM/VLM 仅接收当前时刻的原始文本观测，缺乏空间记忆；
- **回合上下文**（SG-Nav 等）：将回合记忆结构化为 prompt，但回合结束后丢弃；
- **回合 + 经验上下文（TrajRAG）**：长期记忆持续积累回合记忆，并在每次决策时检索相关几何-语义经验，弥补大模型常识与场景特定知识之间的鸿沟。

![[assets/figures/papers/paper_list_l2649_https_arxiv_org_abs_2605_01700/figures/001_Figure_1.jpg]]
*Figure 1: Comparisons with LLM/VLM-based Zero-shot Object-Nav methods. (a) Single-step context. the planner (LLM/VLM) receives raw textual observations from the single timestep. (b) Episodic context. episodic memory is structured into prompts for reasoning but discarded after each episode. (c) Episode + experience context. our TrajRAG serves as long-term memory that continuously accumulates episodic memory and retrieves geometric–semantic experience for planning*

### 输入输出流

- **输入**：RGB-D 观测、目标物体类别。
- **中间表示**：开放词汇语义地图 → 骨架图 → 拓扑关键节点 → 扇区向量序列 → 轨迹嵌入。
- **检索输出**：与当前候选轨迹最相似的若干历史轨迹块（含几何布局与语义上下文）。
- **最终输出**：策略模型基于检索经验选择的下一航点，驱动智能体逐步逼近目标。

整个框架的关键设计在于将冗余的 RGB-D 序列压缩为**拓扑-极坐标轨迹**，并通过**层次化索引**实现高效检索，使零样本导航首次具备了可积累、可迁移的长期场景经验。

### 语义建图与拓扑骨架提取

导航开始时，智能体基于RGB-D观测增量构建开放词汇语义地图 $\mathcal{M}_t \in \mathbb{R}^{(2+N_o) \times H \times W}$，其中 $N_o$ 为开放词汇物体类别数。该地图包含障碍物通道、已探索区域通道和各物体类别的语义通道。随后对可导航区域进行形态学细化（morphological thinning）得到骨架图 $\mathcal{G}_{\text{skel}}$，并从中提取候选拓扑节点：

$$\mathcal{V}_{\text{cand}} = \{ v \in \mathcal{G}_{\text{skel}} \mid |\mathcal{N}_8(v)| \geq 3 \}$$

其中 $\mathcal{N}_8(v)$ 表示节点 $v$ 的8邻域连通分量数。这一条件筛选出骨架中的分支点和交叉点作为拓扑关键点，这些节点自然标记了场景中的决策位置（如走廊交叉口、房间入口）。提取后的节点按距离阈值 $d_{\min}=0.5\text{m}$ 进行去重，确保表示的紧凑性。

### 拓扑-极坐标轨迹表示

对于每个拓扑节点，TrajRAG通过极坐标采样构建其局部几何-语义描述。以节点为中心，在12个等分方向 $\theta_1,\dots,\theta_{12}$ 上发射射线，采样函数定义为：

$$\phi_k(\theta) = \begin{cases} c, & \text{if hits object } c \\ \text{obstacle}, & \text{if hits obstacle} \\ \text{unknown}, & \text{if hits unknown region} \\ \text{free}, & \text{if no hit within } R \end{cases}$$

该函数对每个方向返回射线击中目标的具体物体类别 $c$、障碍物、未知区域或自由空间。由此每个节点 $k$ 的扇区向量为12维编码：

$$\mathbf{s}_k = [\phi_k(\theta_1), \phi_k(\theta_2), \ldots, \phi_k(\theta_{12})]$$

扇区向量紧凑编码了节点周围360°范围内的语义布局和几何结构。一条完整的拓扑-极坐标轨迹 $\mathcal{T}_{\text{tp}}$ 即为其所有拓扑节点的扇区向量序列，相比原始RGB-D序列大幅压缩了存储开销，同时保留了场景的空间结构信息。

### 层次化分块与粗索引

TrajRAG采用层次化分块架构组织历史轨迹。每条轨迹被划分为固定长度的块（chunk），每个块包含连续的若干拓扑节点。粗索引阶段通过计算块间几何-语义相似性将相似场景的块归入同一组，并为每组维护一个摘要图 $\mathcal{G}_{\text{sum}}$，该摘要图在每次新轨迹加入时增量更新。

检索时，粗阶段利用当前轨迹的关键点与各组摘要图进行匹配，快速筛选出top-k个最相似的组。关键点匹配采用带旋转补偿的语义相似度：

$$S_{ij} = \max_{\Delta\theta} \sin\bigl(\text{Rot}(\mathbf{s}_i, \Delta\theta), \mathbf{s}_j\bigr)$$

该公式通过循环旋转扇区向量 $\Delta\theta$ 补偿智能体朝向差异，取旋转后与目标向量的最大余弦相似度，有效解决了同一场景不同朝向下的匹配问题。

### 细粒度嵌入与对比学习

细索引阶段对每个轨迹块进行序列编码。首先使用编码器（如DistilBERT）将扇区向量序列映射为隐状态 $[\mathbf{h}_1, \dots, \mathbf{h}_L]$，再通过解码器（如DistilGPT2）进行自回归建模，最终轨迹嵌入由解码器末层token与目标语义嵌入拼接形成：

$$\mathbf{z} = f_{\text{E}}(\mathcal{T}_{\text{tp}}) = \mathbf{h}_L' \oplus \mathbf{h}_{\text{g}}, \quad [\mathbf{h}_1', \dots, \mathbf{h}_L'] = \mathcal{D}_{\text{traj}}([\mathbf{h}_1, \dots, \mathbf{h}_L])$$

其中 $\mathbf{h}_{\text{g}}$ 为目标物体的语义嵌入，$\oplus$ 表示向量拼接。这种设计使得轨迹嵌入同时编码了空间结构信息与导航目标语义。

轨迹嵌入通过对比学习进行训练，损失函数为：

$$\mathcal{L}_{\text{contrast}} = -\log \frac{\exp(\sin(\mathbf{z}_i, \mathbf{z}_j^+)/\tau)}{\sum_k \exp(\sin(\mathbf{z}_i, \mathbf{z}_k)/\tau)}$$

其中 $\sin(\cdot,\cdot)$ 为余弦相似度，$\tau$ 为温度系数，$\mathbf{z}_j^+$ 为正样本（同一场景的相似轨迹），$\mathbf{z}_k$ 为批内所有样本。该损失促使相似场景的轨迹嵌入在隐空间中靠近，为后续检索提供判别性特征。

### 粗到细检索与经验积累

导航过程中，智能体从当前语义地图生成候选轨迹（指向各前沿点），对每条候选轨迹执行粗到细检索：粗阶段通过关键点匹配锁定相似组，细阶段将候选轨迹编码为嵌入向量，在组内进行向量相似度搜索，返回最相关的历史轨迹块。检索到的经验以文本形式注入大模型提示中，辅助航点选择决策。

每个导航回合结束后，完整轨迹经拓扑-极坐标转换后整合进TrajRAG知识库，实现终身经验积累。摘要图随之更新，粗索引和细索引增量扩展，使系统在持续使用中不断提升检索质量和导航能力。

![[assets/figures/papers/paper_list_l2649_https_arxiv_org_abs_2605_01700/figures/008_Figure_4.jpg]]
*Figure 4: Navigation with TrajRAG. The left column shows the agent’s ego-view RGB images. The middle column presents the skeletonization and detected keypoints (red) on the skeleton map, where the location icon indicates the ground-truth location of the target (“bed”) for visualization purposes only; the target location is unknown to the agent during navigation. The right column illustrates the agent’s traversed trajectory from the start to the pre-navigation position (light gray), candidate trajectories from the current location to various frontiers (light-colored, with blue dots indicating frontiers), and the trajectory selected by the model (burgundy)*

## 实验与关键发现

TrajRAG 的实验设计围绕三个核心问题展开：（1）拓扑-极坐标轨迹表示和层次化检索策略各自对性能的贡献；（2）TrajRAG 与现有零样本 ObjectNav 方法及不同 RAG 范式相比的优势；（3）经验积累带来的跨场景和跨数据集泛化能力。

### 主实验结果

TrajRAG 在三个标准零样本 ObjectNav 基准上均取得最优结果。在 MP3D 上成功率和 SPL 分别为 **42.6% / 18.0%**，在 HM3D-v1 上为 **62.5% / 33.9%**，在 HM3D-v2 上达到 **78.1% / 40.2%**（Table 5）。对比方法包括基于 LLM 的 VoroNav（Wu et al., ICML 2024）、SG-Nav（Yin et al., NeurIPS 2024），基于 VLM 的 VLFMap（Yokoyama et al., ICRA 2024）、BeliefMapNav（Zhou et al., NeurIPS 2025），以及通用零样本目标导航方法 UniGoal（Yin et al., CVPR 2025）。TrajRAG 在所有数据集上均显著超越这些仅依赖大模型常识、缺乏长期空间经验积累的基线方法，验证了检索增强几何-语义经验对于提升零样本导航决策场景针对性的关键作用。

![[assets/figures/papers/paper_list_l2649_https_arxiv_org_abs_2605_01700/figures/009_Table_5.jpg]]
*Table 5: Comparisons with the related works on MP3D, HM3Dv1 and HM3Dv2 datasets. “OV” denotes if the method supports openvocabulary object goals*

### 消融实验

#### 节点表示消融

Table 1 在 HM3D-v1 上对比了三种节点表示方式：纯文本邻居聚合（TNA）、仅几何扇区（TPS-G）、仅语义扇区（TPS-S），以及完整的几何+语义扇区表示（TPS-G + TPS-S）。完整表示取得最高 **61.7% SR / 33.2% SPL**，证明极坐标扇区同时编码空间布局和语义上下文是轨迹表示有效性的核心来源。单一模态（纯几何或纯语义）均导致性能下降，说明几何结构与语义信息在经验匹配中具有互补性。

![[assets/figures/papers/paper_list_l2649_https_arxiv_org_abs_2605_01700/figures/003_Table_1.jpg]]
*Table 1: Ablation on node representations in HM3Dv1. TNA: textual neighbor aggregation; TPS-G: topo-polar sector geometry; TPS-S: topo-polar sector semantics*

#### 检索策略消融

Table 2 在 HM3D-v1 上消融了检索策略。仅使用文本嵌入（TE）进行检索时性能最低；引入粗粒度拓扑匹配后有所提升；完整的两阶段粗到细检索（Coarse + Fine SE）取得最优 **61.7% SR / 33.2% SPL**。这表明粗粒度阶段有效缩小了候选空间，细粒度序列嵌入阶段则提供了精确的轨迹级匹配，二者缺一不可。

![[assets/figures/papers/paper_list_l2649_https_arxiv_org_abs_2605_01700/figures/004_Table_2.jpg]]
*Table 2: Ablation study on retrieval strategy in HM3Dv1. TE: text embedding; SE: our sequence embedding*

#### RAG 范式对比

Table 3 将 TrajRAG 与基于文本嵌入的 RAG（TrajTextRAG）和基于图的 RAG（GraphRAG）进行对比。TrajRAG 显著优于两者，说明将轨迹转化为紧凑的拓扑-极坐标序列并采用专门的序列嵌入进行检索，比直接将原始文本或图结构作为检索单元更能捕捉导航经验中的空间-语义关联。

### 跨数据集泛化

Table 4 展示了跨数据集评估结果。当使用 HM3D-v1 与 MP3D 的混合语料库进行检索时，TrajRAG 在两个数据集上的性能均优于仅使用单一数据集语料的配置（置信度 0.9）。这表明 TrajRAG 积累的经验具有可迁移性，层次化分块结构能够有效组织来自不同场景分布的知识，实现跨域泛化的终身学习。

### 失败模式与局限性

论文未提供显式的失败模式分析（limitations 字段为空）。从方法设计推断，潜在风险包括：拓扑骨架化对复杂多层结构的适应性、极坐标采样半径 $R$ 对场景尺度的敏感性，以及层次化分组策略在经验规模急剧增长时的检索精度退化。这些点需要在实际部署中手动验证。

## 定位与知识库关联

### 1. 问题定位：零样本导航中的经验断层

现有零样本物体导航方法的核心瓶颈在于**决策依赖大模型内化的场景无关常识，缺乏对三维空间布局与物体共现关系的长期经验积累**。具体而言，当前主流范式可分为两类：

- **单步上下文方法**：规划器（LLM/VLM）仅接收当前时刻的原始文本观测，完全不具备历史记忆能力。
- **情节上下文方法**：将单次导航轨迹结构化为提示输入大模型，但每个情节结束后即丢弃，无法跨情节复用经验。典型代表包括 **VoroNav**（Wu et al., ICML 2024）、**VLFMap**（Yokoyama et al., ICRA 2024）、**SG-Nav**（Yin et al., NeurIPS 2024）、**UniGoal**（Yin et al., CVPR 2025）和 **BeliefMapNav**（Zhou et al., NeurIPS 2025）。

这些方法虽在零样本设定下取得进展，但每次导航均从零开始推理，无法借鉴历史中“在类似布局场景中如何到达目标”的几何-语义经验。TrajRAG的核心因果调节变量即在于**引入可积累、可检索的长期记忆机制**，将离散冗余的导航片段转化为结构化可复用的经验库。

### 2. 方法谱系中的位置

TrajRAG处于**检索增强生成与具身导航**的交叉点，其方法谱系可从三个维度定位：

| 维度 | 基线工作 | 基线特征 | TrajRAG 的改进 |
|------|----------|----------|----------------|
| 记忆机制 | VoroNav, SG-Nav 等 | 无长期记忆，情节后丢弃 | 层次化分块存储拓扑-极坐标轨迹，支持终身经验积累 |
| 轨迹表示 | VLFMap, BeliefMapNav | 原始RGB-D序列或场景图 | 拓扑-极坐标轨迹：紧凑编码空间布局与语义上下文 |
| 检索与推理 | 仅依赖大模型常识 | 无检索机制 | 粗到细检索历史经验并注入大模型辅助决策 |

具体而言，TrajRAG通过以下四个关键设计改变（changed slots）实现突破：

1. **长期记忆**：从“无”变为“TrajRAG层次化分块存储拓扑-极坐标轨迹”，每个episode结束后将完整轨迹整合入库，实现终身学习。
2. **轨迹表示**：从“原始RGB-D序列或场景图”变为“拓扑-极坐标轨迹”，通过骨架化提取拓扑节点，并以12维扇区向量编码节点周围局部语义-几何结构。
3. **检索与推理**：从“仅依赖大模型常识”变为“粗到细检索历史经验并注入大模型辅助决策”，先按几何-语义相似性粗筛分组，再基于序列嵌入精排。
4. **经验积累**：从“每轮后丢弃”变为“每轮后整合轨迹”，使知识库随导航次数增长而持续丰富。

### 3. 知识库定位

TrajRAG构建的知识库具有以下特征：

- **知识类型**：几何-语义经验，即“在何种空间布局下，沿何种路径可高效到达目标物体”的轨迹知识。
- **表示形式**：拓扑-极坐标轨迹的层次化分块结构——粗索引按几何-语义相似性分组，细索引通过编码器-解码器Transformer（DistilBERT + DistilGPT2）将每个块编码为隐向量嵌入，并采用对比学习优化嵌入空间。
- **检索方式**：粗到细两阶段检索。粗阶段基于拓扑关键点的扇区向量匹配相似场景组；细阶段通过序列嵌入的余弦相似度精排候选轨迹。
- **与其他RAG变体的区别**：消融实验（Table 3）表明，TrajRAG显著优于基于文本嵌入的TrajTextRAG和基于图的GraphRAG，验证了拓扑-极坐标表示对空间-语义联合建模的优势。

### 4. 适用边界与局限

从实验覆盖范围看，TrajRAG的验证集中于室内物体导航基准（MP3D、HM3D-v1、HM3D-v2），其适用边界可推断如下：

- **适用场景**：室内环境中的零样本开放词汇物体导航，尤其是需要跨情节复用空间经验的长期部署场景。
- **潜在局限**（需手动验证）：
  - 跨数据集泛化实验（Table 4）显示组合检索语料库可提升性能，但未验证在完全未见的环境类型（如室外、动态场景）中的表现。
  - 拓扑-极坐标表示依赖语义地图的质量，在语义分割失败或开放词汇检测不准确的场景下，扇区向量的可靠性可能下降。
  - 论文未报告检索延迟与计算开销，层次化分块在大规模知识库下的扩展性需进一步评估。
  - 经验积累的终身学习效果仅在有限episode数量下验证，长期积累是否会导致检索噪声增加或表示退化尚不明确。

### 5. 开放问题

论文未明确讨论但值得关注的方向包括：

- **主动经验选择**：当前检索完全由当前轨迹驱动，智能体是否可主动规划探索以获取更有价值的经验？
- **经验遗忘与更新**：长期运行中旧经验可能过时或冗余，是否需要引入遗忘机制或经验优先级排序？
- **多模态经验融合**：能否将人类示范或语言指令等异质经验纳入同一知识库？
- **安全与鲁棒性**：检索到的经验若来自失败轨迹，如何避免错误传播？

## 原文 PDF

![[paperPDFs/CVPR_2026/TrajRAG_Retrieving_Geometric_Semantic_Experience_for_Zero_Shot_Object_Navigation.pdf]]
