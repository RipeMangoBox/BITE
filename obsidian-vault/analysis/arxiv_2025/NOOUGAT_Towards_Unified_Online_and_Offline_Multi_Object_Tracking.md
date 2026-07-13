---
title: "NOOUGAT: Towards Unified Online and Offline Multi-Object Tracking"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/NOOUGAT_Towards_Unified_Online_and_Offline_Multi_Object_Tracking.pdf
project_link: null
code_link: null
aliases:
- NOOUGAT
tags:
- arxiv_2025
- topic/other_unclear
- topic/other_unclear/general
core_operator: 非重叠子片段大小T（处理步长）和自回归长期关联（ALT）层——T控制在线（T=1）到离线（如T=256）的行为，ALT层完全可学习地连接历史轨迹与传入轨迹，替代启发式关联。
primary_logic: 通过将视频序列划分为非重叠子片段，用GNN层级独立生成每个子片段的局部轨迹，再通过ALT层自回归融合为全局轨迹，消除了启发式匹配和拼接，使同一个灵活的框架统一了在线与离线跟踪，并通过调整T满足从实时帧级处理到批处理各种场景的时延要求。
claims:
- NOOUGAT在DanceTrack上在线AssA超越Hybrid-SORT 2.3点，离线额外提升3.8点。
- NOOUGAT在SportsMOT上在线AssA超越Diff-MOT 9.2点，离线再提升8.7点。
- ALT层在DanceTrack验证集上在线匹配HOTA显著优于匈牙利算法（64.6 vs 62.1）。
- ALT层替代SUSHI启发式拼接后，DanceTrack验证集IDF1从72.0提升至76.6。
---

# NOOUGAT: Towards Unified Online and Offline Multi-Object Tracking

> [!tip] 核心洞察
> 通过将视频序列划分为非重叠子片段，用GNN层级独立生成每个子片段的局部轨迹，再通过ALT层自回归融合为全局轨迹，消除了启发式匹配和拼接，使同一个灵活的框架统一了在线与离线跟踪，并通过调整T满足从实时帧级处理到批处理各种场景的时延要求。

| 字段 | 内容 |
|------|------|
| 中文题名 | NOOUGAT：面向统一在线与离线多目标跟踪 |
| 英文题名 | NOOUGAT: Towards Unified Online and Offline Multi-Object Tracking |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2509.02111) · [paper](https://arxiv.org/abs/2206.14651) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | NOOUGAT |
| Dataset | DanceTrack, SportsMOT, MOT17, MOT20 |

> [!tip] 效果简介
> - DanceTrack 上，AssA NOOUGAT Online vs Hybrid-SORT (+2.3)；IDF1 NOOUGAT Online vs Hybrid-SORT (+3.2)。
> - SportsMOT 上，AssA NOOUGAT Online vs Diff-MOT (+9.2)。
> - MOT17 上，AssA NOOUGAT Online vs Diff-MOT (+0.7)。

## 概要

多目标跟踪（MOT）领域长期存在在线与离线范式的割裂：在线跟踪器逐帧处理，依赖匈牙利算法等手工设计的匹配启发式；离线跟踪器则通过滑动窗口将视频划分为重叠子片段，再借助线性规划等规则拼接轨迹。这两种范式各自受限于固定的时延假设——在线方法缺乏对全局时序上下文的利用，离线方法则因窗口重叠导致大量冗余计算，且拼接启发式难以灵活适应不同场景的关联模式。

NOOUGAT 针对上述瓶颈提出了一个统一框架，核心调控变量是**非重叠子片段大小 T** 和**自回归长期关联（ALT）层**。T 控制处理步长：当 T=1 时，模型以帧级在线方式运行；当 T 增大（如 256 帧），模型获得更丰富的时序上下文，性能持续提升，可按需在延迟与精度之间调节。ALT 层则完全以数据驱动的方式学习历史轨迹与传入轨迹之间的关联，替代了传统在线匹配算法和离线拼接启发式，使同一个模型无需任何规则修改即可覆盖从实时到批处理的全场景。

在方法谱系上，NOOUGAT 继承了 **SUSHI**（Cetintas et al., CVPR 2023）的 GNN 层级结构用于局部轨迹生成，但以非重叠划分替代其滑动窗口范式，并用 ALT 层取代其启发式拼接模块。相较于 **Hybrid-SORT**（Yang et al., AAAI 2024）等基于 SORT 的在线方法，NOOUGAT 消除了手工匹配规则；相较于 **DiffMOT**（Lv et al., CVPR 2024）等扩散模型跟踪器，NOOUGAT 在关联阶段提供了端到端可学习的图神经网络方案。

主要实验结果验证了统一框架的有效性：在 DanceTrack 上，NOOUGAT 在线模式 AssA 超越 Hybrid-SORT **2.3 点**，离线模式额外提升 **3.8 点**；在 SportsMOT 上，在线 AssA 超越 DiffMOT **9.2 点**，离线再提升 **8.7 点**。消融实验进一步证实，ALT 层在线匹配的 HOTA（64.6）显著优于匈牙利算法（62.1），且替代 SUSHI 启发式拼接后 IDF1 从 72.0 提升至 76.6。这些结果表明，消除手工设计的匹配与拼接启发式、代之以统一的 GNN 关联学习，是连接在线与离线跟踪的关键路径。

多目标跟踪（MOT）的核心挑战在于跨帧关联检测，以形成一致的轨迹。根据应用场景的时延要求，现有方法被划分为两个几乎互不交叠的范式：**在线跟踪**与**离线跟踪**。在线跟踪器逐帧处理，每帧到来时立即将当前检测与历史轨迹进行匹配，通常依赖匈牙利算法等启发式匹配策略，以满足实时性要求。离线跟踪器则相反，可访问整个视频序列，通过将视频切分为重叠的子片段，在各片段内独立生成局部轨迹，再通过启发式拼接（如线性规划）将这些片段轨迹融合为全局轨迹。这两种范式长期共享一个根本性瓶颈：**核心关联与融合步骤均依赖手工设计的启发式规则**，缺乏数据驱动的灵活性与鲁棒性。

这一瓶颈在三个层面制约着现有方法。第一，启发式匹配（如基于IoU或外观相似度的匈牙利算法）仅使用固定的浅层线索，无法动态适应不同场景和时延上下文中的最相关特征。第二，离线方法中广泛采用的滑动窗口子片段划分（如步幅为窗口大小的一半）导致每一帧被多次处理，产生大量冗余计算。第三，在线与离线方法在架构上相互割裂，无法在同一个框架内灵活调节时延与精度的权衡——部署场景若从实时帧级处理切换到批处理模式，往往需要更换完全不同的跟踪器。

针对上述缺口，**NOOUGAT** 提出了一种统一架构，其核心动机是消除对启发式匹配和拼接的依赖，使同一模型能够覆盖从在线（逐帧）到离线（全序列批处理）的完整时延谱系。该架构的关键设计是一个可调节的处理步长 $T$：当 $T=1$ 时，模型以在线方式逐帧关联；当 $T$ 增大（如 $T=256$）时，模型获得更丰富的时序上下文，性能随之提升，同时以更高的延迟换取精度（见 Figure 2）。这种灵活性使得 NOOUGAT 成为首个通过统一公式满足多样化部署时延需求的多目标跟踪架构。

与现有方法相比，NOOUGAT 在动机层面的核心区分点在于：**用完全可学习的 GNN 关联层替代所有手工启发式**。在线模式下，这替代了匈牙利匹配；离线模式下，这替代了子片段间的启发式拼接。由此，关联过程变为数据驱动的端到端学习，模型能够自动发现不同时序上下文中最重要的关联线索，从而在多个基准上取得显著提升——在线模式下 DanceTrack 的 AssA 超越 **Hybrid-SORT**（Yang et al., AAAI 2024）2.3 点，SportsMOT 上超越 **DiffMOT**（Lv et al., CVPR 2024）9.2 点（Table 1, Table 2）。

## 核心方法与创新机理

NOOUGAT的核心创新在于**将多目标跟踪重新定义为一个统一的可学习关联问题**，从而消除了传统跟踪器中普遍存在的手工启发式匹配与拼接。这一统一框架的实现依赖于三个相互耦合的关键设计：非重叠子片段划分、自回归长期关联（ALT）层和可调节的处理步长T。

### 从滑动窗口到非重叠子片段：消除冗余计算

传统离线跟踪器（如**SUSHI**，Cetintas et al., CVPR 2023）采用滑动窗口方式将视频序列划分为重叠的子片段，步长$k$通常为窗口大小的一半。这种设计导致同一帧被多次处理，产生了大量冗余计算：

$$X_1 = \{ s_{1 T}^1, s_{k T+k-1}^2, ..., s_{C-T+1 C}^{n_1} \}$$

NOOUGAT将这一范式替换为**非重叠子片段划分**，每个帧仅被处理一次：

$$X_2 = \{ s_{1 T}^1, s_{T+1 2T}^2, ..., s_{C-T+1 C}^{n_2} \}$$

这一改变看似简单，但其深层意义在于：它迫使模型必须在一个统一的框架内处理从单帧到长序列的所有时间上下文，而非依赖滑动窗口的重叠区域来“缝合”轨迹。这为后续ALT层的设计奠定了结构基础。

### ALT层：以可学习关联替代启发式匹配与拼接

传统在线跟踪器（如**Hybrid-SORT**，Yang et al., AAAI 2024）依赖匈牙利算法等启发式匹配将当前检测与历史轨迹关联；离线跟踪器（如SUSHI）则需额外的线性规划或启发式拼接步骤来合并子片段轨迹。这些手工设计的规则无法灵活适应不同的时延需求，也难以从数据中学习最优关联策略。

NOOUGAT的**Autoregressive Long-term Tracking (ALT)层**是一个完全可学习的GNN关联模块，自回归地将历史轨迹与当前子片段的局部轨迹融合为全局轨迹：

$$\mathcal{T}_{alt}^1 := \mathcal{T}_{hicl}^1$$

$$\mathcal{T}_{alt}^i := \mathrm{ALT}(\mathcal{T}_{alt}^{i-1}, \mathcal{T}_{hicl}^i)$$

ALT层的图结构根据在线/离线模式灵活切换。在**离线模式**下，图采用全连接结构，允许所有节点（过去轨迹与传入轨迹）之间建立边，这意味着模型可以修订早期的关联决策：

$$V = \{ \mathcal{T}_{past} \cup \mathcal{T}_{incom} \}, E = \{ (T_i, T_j) \in V \times V \}$$

在**在线模式**下，图退化为二分图结构，仅允许过去轨迹连接到传入轨迹，满足实时处理的时间因果约束：

$$V = \{ \mathcal{T}_{past} \cup \mathcal{T}_{incom} \}, E_b = \{ (T_i, T_j) \in \mathcal{T}_{past} \times \mathcal{T}_{incom} \}$$

消融实验直接验证了ALT层的优势。在DanceTrack验证集上，ALT层的在线匹配HOTA达到64.6，显著优于使用相同节点特征的匈牙利算法（62.1）（Table 5）。在离线拼接场景中，ALT层替代SUSHI的启发式拼接后，IDF1从72.0提升至76.6（Table 6）。这表明**数据驱动的关联学习在跨时间上下文的轨迹融合中具有显著优势**。

### 可调节步长T：统一在线与离线行为

处理步长T是NOOUGAT的核心控制旋钮。当$T=1$时，模型逐帧处理，行为等同于在线跟踪器；当$T=256$时，模型以256帧为批次处理，获得丰富的时序上下文，表现为离线跟踪器。如Figure 2所示，在DanceTrack验证集上，性能随T从1增加到256而持续提升，展示了模型在不同时延约束下的平滑调节能力。

这种统一性使得NOOUGAT成为首个**无需改变架构即可同时满足实时帧级处理和批处理场景需求**的跟踪框架。在在线模式下，模型约12 FPS（不含检测）；在离线模式下，仅关联步骤即可达到340 FPS（Table 9-10）。

### 轨迹级速度方向一致性（VDC）扩展

NOOUGAT还将帧级VDC特征（Cao et al., 2023）扩展为**轨迹级VDC**。传统帧级VDC计算过去轨迹最后一帧与传入轨迹第一帧的速度方向夹角，而轨迹级VDC则计算过去轨迹的**前向速度向量**与传入轨迹**后向速度向量的反方向**之间的夹角：

$$\operatorname{VDC}(T_i, T_j) = \cos^{-1} \left( \frac{ \overrightarrow{T}_{i, \mathrm{fwrd}} \cdot (-\overrightarrow{T}_{j, \mathrm{bwrd}}) }{ ||\overrightarrow{T}_{i, \mathrm{fwrd}}|| \; ||\overrightarrow{T}_{j, \mathrm{bwrd}}|| } \right)$$

这一扩展利用了两条轨迹的整体运动趋势，而非仅依赖边界帧的瞬时速度，为ALT层提供了更鲁棒的运动一致性线索。消融实验表明，该扩展为离线跟踪器带来1.4 IDF1点的提升（Table 8）。

### 创新总结

NOOUGAT的核心创新可归纳为三个changed slots：**序列划分方式**从重叠滑动窗口变为非重叠子片段；**跨片段关联方法**从启发式匹配/拼接变为完全可学习的ALT GNN层；**处理步长T**从固定窗口变为可调节的控制参数。这三个改变的协同作用使得同一个框架能够灵活适应从实时到批处理的各种部署场景，并在多个基准上取得了显著的性能提升。

NOOUGAT 的核心设计思想是用**统一的、完全可学习的框架**替代在线跟踪中手工设计的匹配启发式与离线跟踪中手工设计的拼接启发式。如图 1 所示，传统在线跟踪器（1a）对每一帧执行启发式匹配，而传统离线跟踪器（1b）将视频划分为重叠子片段，分别生成轨迹后再用启发式方法拼接——这带来了大量冗余计算。NOOUGAT（1c）通过两个关键机制消除了这两类启发式：**非重叠子片段划分**与**自回归长期关联（ALT）层**，从而在同一个架构内灵活支持从逐帧在线到批处理离线的全部延迟需求。

### 处理流水线

整体流水线由三个核心模块串联构成：

1. **GNN 层级（GNN Hierarchy）**  
   受离线跟踪器 **SUSHI**（Cetintas et al., CVPR 2023）启发，NOOUGAT 首先将输入视频序列划分为大小为 $T$ 的**非重叠子片段**（Equation 3），而非传统方法使用的滑动窗口重叠子片段（Equation 2）。每个子片段被独立送入 GNN 层级，生成该片段内的局部轨迹（tracklets）。这一设计使得每个帧仅被处理一次，从根本上消除了滑动窗口带来的冗余计算。

2. **自回归长期关联层（ALT Layer）**  
   ALT 层是 NOOUGAT 的核心创新。它以自回归方式工作：第 $i$ 步将过去累积的全局轨迹集 $\mathcal{T}_{alt}^{i-1}$ 与当前子片段的局部轨迹集 $\mathcal{T}_{hicl}^i$ 融合，输出更新后的全局轨迹集 $\mathcal{T}_{alt}^i$（Equation 5）。初始步直接将第一个子片段的局部轨迹作为 ALT 轨迹集（Equation 4）。ALT 层本质上是一个**完全可学习的 GNN 关联模块**，替代了传统方法中的匈牙利匹配或线性规划拼接。

3. **节点与边特征提取**  
   在送入 GNN 之前，系统为每条轨迹（节点）和每对轨迹（边）提取丰富的特征，包括几何特征、运动特征、外观（ReID）特征、轨迹速度方向一致性（VDC）以及检测置信度。其中，轨迹级 VDC（Equation 8）将帧级 VDC 扩展为计算过去轨迹的前向速度向量与传入轨迹的后向速度反向量的夹角，为关联提供更强的运动一致性线索。

### 在线与离线的统一

NOOUGAT 通过调节两个关键参数实现从在线到离线的连续切换：

- **处理步长 $T$**：$T=1$ 时，每次仅处理一个传入帧，表现为纯在线跟踪器；$T$ 增大时，每次处理更长的子片段，获得更丰富的时序上下文，性能随之提升（Figure 2），最终在 $T=256$ 时达到离线批处理模式。
- **图连接模式**：在线模式下，ALT 层构建**二分图**（Equation 7），仅允许过去轨迹连接传入轨迹，符合实时约束且不可修改历史关联；离线模式下，ALT 层构建**全连接图**（Equation 6），允许所有节点间互联，从而可以修订过去的关联决策，实现全局优化。

### 特征聚合策略

为适配不同模式，外观特征的时序聚合方式也有所区分：在线模式采用**指数移动平均（EMA）** 逐步更新轨迹的 ReID 特征，满足逐帧处理的需求；离线模式则直接对轨迹内所有检测的 ReID 特征取平均，利用批处理的全局信息。

### 输入输出流

整体输入为视频帧序列的检测结果（边界框、置信度、ReID 特征），输出为全局一致的身份标签分配。流水线无需任何手工设计的匹配阈值、拼接规则或轨迹生命周期管理——所有关联决策均由 ALT 层以数据驱动的方式学习得到。

![[assets/figures/papers/paper_list_l76_https_arxiv_org_abs_2509_02111/figures/002_Figure_1.jpg]]
*Figure 1: (1a) Online trackers using heuristic matching. (1b) Offline trackers using heuristics to stitch overlapping subclips. (1c) Our NOOUGAT architecture eliminates the need for matching and stitching heuristics, and unifies online and offline in a single flexible framework*

![[assets/figures/papers/paper_list_l76_https_arxiv_org_abs_2509_02111/figures/004_Figure_3.jpg]]
*Figure 3: Overview of of NOOUGAT. Our Global GNN module auroregressively connects past and incoming frames. It learns association across various temportal contexts in a data-driven manner, enabling both online and offline operation*

NOOUGAT 的核心由三个关键模块构成：**非重叠子片段划分**、**GNN 层级局部轨迹生成**，以及**自回归长期关联（ALT）层**。这三个模块协同工作，消除了传统在线跟踪器中的启发式匹配和离线跟踪器中的启发式拼接，实现统一的在线/离线跟踪框架。

### 非重叠子片段划分

传统离线跟踪器（如 **SUSHI**，Cetintas et al., CVPR 2023）采用滑动窗口方式将视频划分为重叠子片段，步幅为 $k$：

$$X_1 = \{ s_{1 T}^1, s_{k T+k-1}^2, ..., s_{C-T+1 C}^{n_1} \} \tag{2}$$

这种方式导致同一帧被多次处理，产生大量冗余计算。NOOUGAT 改为将视频划分为**非重叠子片段**，每个子片段大小为 $T$：

$$X_2 = \{ s_{1 T}^1, s_{T+1 2T}^2, ..., s_{C-T+1 C}^{n_2} \} \tag{3}$$

每个帧仅处理一次，消除了冗余。子片段大小 $T$ 是控制处理步长的关键参数：$T=1$ 时退化为帧级在线跟踪，$T$ 越大则提供越丰富的时序上下文，延迟也随之增加，实现连续可调的精度-延迟权衡。

### GNN 层级局部轨迹生成

每个非重叠子片段独立通过 GNN 层级处理，生成该片段内的局部轨迹 $\mathcal{T}_{hicl}^i$。GNN 层级继承自 SUSHI 的图结构，通过消息传递在检测节点间学习关联边。最终边分类公式为：

$$\boldsymbol{y}_{(u,v)}^{\mathrm{pred}} = \mathrm{MLP}_{\mathrm{class}}(\boldsymbol{h}_{(u,v)}^{(S)}) \tag{1}$$

其中 $\boldsymbol{h}_{(u,v)}^{(S)}$ 为第 $S$ 步消息传递后的边嵌入，$\mathrm{MLP}_{\mathrm{class}}$ 将其映射为预测关联分数。该模块的节点和边特征包括几何、运动、外观、轨迹速度方向一致性（VDC）以及检测置信度等多模态线索。

### 自回归长期关联（ALT）层

ALT 层是 NOOUGAT 的核心创新，以完全可学习的方式自回归地融合历史轨迹与传入的局部轨迹，替代启发式匹配和拼接。

**轨迹初始化**：ALT 轨迹集初始化为第一个子片段的局部轨迹：

$$\mathcal{T}_{alt}^1 := \mathcal{T}_{hicl}^1 \tag{4}$$

**自回归更新**：第 $i$ 步，ALT 层融合过去轨迹 $\mathcal{T}_{alt}^{i-1}$ 与当前子片段轨迹 $\mathcal{T}_{hicl}^i$：

$$\mathcal{T}_{alt}^i := \mathrm{ALT}(\mathcal{T}_{alt}^{i-1}, \mathcal{T}_{hicl}^i) \tag{5}$$

**图连接模式**：ALT 层支持两种图连接模式以适应不同场景：

- **全连接图（离线模式）**：允许所有节点互联，支持修订过去的关联决策：

$$V = \{ \mathcal{T}_{past} \cup \mathcal{T}_{incom} \}, \quad E = \{ (T_i, T_j) \in V \times V \} \tag{6}$$

- **二分图（在线模式）**：仅允许过去轨迹连接传入轨迹，符合实时约束：

$$V = \{ \mathcal{T}_{past} \cup \mathcal{T}_{incom} \}, \quad E_b = \{ (T_i, T_j) \in \mathcal{T}_{past} \times \mathcal{T}_{incom} \} \tag{7}$$

### 轨迹级速度方向一致性（VDC）

NOOUGAT 将帧级 VDC 特征扩展为**轨迹级 VDC**，作为 ALT 层的重要运动线索。对于过去轨迹 $T_i$ 和传入轨迹 $T_j$，计算 $T_i$ 的前向速度向量与 $T_j$ 的后向速度向量反方向之间的夹角：

$$\operatorname{VDC}(T_i, T_j) = \cos^{-1} \left( \frac{ \overrightarrow{T}_{i, \mathrm{fwrd}} \cdot (-\overrightarrow{T}_{j, \mathrm{bwrd}}) }{ ||\overrightarrow{T}_{i, \mathrm{fwrd}}|| \; ||\overrightarrow{T}_{j, \mathrm{bwrd}}|| } \right) \tag{8}$$

该特征捕捉轨迹间的运动一致性，消融实验表明为离线跟踪器带来 1.4 IDF1 点的提升（Table 8）。

### 外观特征聚合策略

为适应不同模式，NOOUGAT 采用差异化的外观特征聚合：

- **在线模式**：使用指数移动平均（EMA）对轨迹的 ReID 特征进行时序聚合，满足实时递推要求。
- **离线模式**：直接平均轨迹内所有检测的 ReID 特征，利用完整时序信息获得更稳定的外观表征。

## 实验与关键发现

NOOUGAT 在 DanceTrack、SportsMOT、MOT17、MOT20、BEE24 和 VETRA 等六个基准上进行了全面评估。所有主要对比方法均使用相同的 YOLOX 检测器和 ResNet50-SBS ReID 模型，并采用固定置信度阈值 0.65（而非序列特定阈值），以确保公平性。

### 主要结果

**DanceTrack.** 在线模式下，NOOUGAT 在 AssA 上达到 51.1，超越 **Hybrid-SORT**（Yang et al., AAAI 2024）2.3 点，IDF1 提升 3.2 点（Table 1）。切换到离线模式后，AssA 进一步攀升至 54.9，额外提升 3.8 点。这一趋势表明，ALT 层的自回归融合能有效利用更长的时序上下文，而无需依赖启发式匹配或拼接。

**SportsMOT.** 在线 AssA 达到 66.1，大幅超越 **DiffMOT**（Lv et al., CVPR 2024）9.2 点（Table 2）。离线模式下 AssA 再提升 8.7 点至 74.8。SportsMOT 场景中的剧烈运动和频繁遮挡对传统启发式方法构成严重挑战，而 NOOUGAT 的可学习关联层展现出显著鲁棒性。

**MOT17 与 MOT20.** 在 MOT17 上，在线 AssA 超越 DiffMOT 0.7 点（Table 3）；在 MOT20 上，在线 AssA 超越 DiffMOT 7.0 点（Table 4）。值得注意的是，离线模式下的 MOTA 低于某些基线（如 **CoNo-Link**, Gao et al., AAAI 2024），作者将其归因于固定置信度阈值导致的检测召回较低——这暗示检测与关联分离的管道在低质量检测场景下可能并非最优。

**BEE24 与 VETRA.** 在线 HOTA 分别超越 TOPICTrack 4.5 点（Table 11）和 **BOT-SORT** 17.2 点（Table 12），验证了该方法在跨域场景下的泛化能力。

### 消融实验

**ALT 层 vs. 匈牙利算法.** 在 DanceTrack 验证集上，使用相同节点特征时，ALT 层的在线匹配 HOTA 达到 64.6，显著优于匈牙利算法的 62.1（Table 5）。这证明可学习的 GNN 关联比手工设计的二分匹配启发式更有效。

**ALT 层 vs. 启发式拼接.** 将 **SUSHI**（Cetintas et al., CVPR 2023）的启发式拼接替换为 ALT 层后，IDF1 从 72.0 提升至 76.6（Table 6）。这表明数据驱动的跨片段融合策略优于基于规则的线性规划拼接。

**跟踪线索贡献.** 几何（G）+ 运动（M）+ 外观（A）联合建模取得最优 HOTA 64.6，而纯外观模型表现最差（HOTA 57.9）（Table 7）。几何与运动线索在遮挡场景下提供了关键的互补信息。

**轨迹级 VDC 与训练策略.** 将帧级 VDC 扩展为轨迹级 VDC 为离线跟踪器带来 1.4 IDF1 点提升（Table 8）。此外，引入过去轨迹丢弃增强和跳过帧参数（skip）可进一步提高泛化性。

### 运行时分析

在线模式下，NOOUGAT 的关联速度约为 12 FPS（不含检测），对于需要 >30 FPS 的实时应用可能仍需优化。离线模式下，关联速度可达 340 FPS（Table 9-10）。处理步长 T 提供了延迟与精度之间的连续可调旋钮：T=1 时延迟最低，T=256 时精度最高（Figure 2）。

### 失败模式与局限性

1. **检测质量依赖：** ALT 层依赖于 GNN 层级生成的局部轨迹质量。若检测器严重缺失（如漏检），初始轨迹断开可能传播至后续关联，导致身份碎片化。
2. **低帧率场景未量化：** 虽然定性结果表明 NOOUGAT 能恢复长期遮挡（Figure 5），但论文未提供极低帧率（<1 FPS）或严重遮挡场景下的量化恢复率与遮挡时长关系。
3. **在线速度瓶颈：** 12 FPS 的关联速度限制了在需要实时响应的部署场景中的直接应用，尽管可通过增加 T 提高吞吐，但会增加延迟。
4. **MOTA 权衡：** 在 MOT17/MOT20 上离线 MOTA 低于部分基线，暗示固定置信度阈值导致召回不足的问题在检测-跟踪分离框架中尤为突出。

![[assets/figures/papers/paper_list_l76_https_arxiv_org_abs_2509_02111/figures/011_Table_5.jpg]]
*Table 5: Comparison of our online ALT layer with the Hungarian algorithm on the DanceTrack val set*

![[assets/figures/papers/paper_list_l76_https_arxiv_org_abs_2509_02111/figures/012_Table_6.jpg]]
*Table 6: Comparison of NOOUGAT with our learnable ALT layer with the heuristic stitching in SUSHI on the DanceTrack val set. The first row shows original SUSHI performance; the second row shows our reproduction with matched features for fair comparison*

![[assets/figures/papers/paper_list_l76_https_arxiv_org_abs_2509_02111/figures/015_Table_7.jpg]]
*Table 7: Ablation of our online tracker on DanceTrack val set, using different tracking cues: Appearance (A), Motion and Velocity (M) and Geometry (G)*

![[assets/figures/papers/paper_list_l76_https_arxiv_org_abs_2509_02111/figures/013_Table_8.jpg]]
*Table 8: Ablations of our training parameters on the DanceTrack val set*

## 定位与知识库关联

### 1. 问题根因与关键设计旋钮

NOOUGAT 的核心动机源于一个结构化瓶颈：**现有在线/离线跟踪器普遍依赖手工设计的匹配与拼接启发式**，导致框架无法灵活适应从帧级实时到全序列批处理的不同延迟需求。具体而言，在线方法（如基于 SORT 的系列）使用匈牙利算法或贪心匹配逐帧关联，离线方法（如 **SUSHI** (Cetintas et al., CVPR 2023)）则采用滑动窗口重叠子片段 + 线性规划拼接，后者造成大量冗余计算（同一帧被多次处理）。

NOOUGAT 的因果控制旋钮有二：**非重叠子片段大小 T**（处理步长）和**自回归长期关联（ALT）层**。T 从 1 到 256 连续可调，直接决定行为模式——T=1 等价于在线帧级处理，T=256 等价于批处理离线模式；ALT 层则完全以数据驱动方式学习历史轨迹与传入轨迹的关联，替代所有启发式匹配和拼接。这一设计使同一框架统一了在线与离线跟踪，消除了对两套独立系统的需求。

### 2. 与基线方法的关键差异

| 设计维度 | 在线基线（Hybrid-SORT, DiffMOT） | 离线基线（SUSHI, CoNo-Link） | NOOUGAT |
|---------|-------------------------------|---------------------------|---------|
| **序列划分** | 逐帧处理（无划分） | 滑动窗口重叠子片段（stride = T/2） | 非重叠子片段（步幅 = T），每帧仅处理一次 |
| **跨片段关联** | 匈牙利算法 / 贪心匹配 | 线性规划拼接 / 启发式缝合 | 完全可学习的 ALT GNN 层，自回归融合 |
| **处理步长 T** | 固定为 1（帧级） | 固定窗口大小（如 512 帧） | 可调 T=1 到 T=256，连续可调 |
| **VDC 特征** | 仅帧级使用（Cao et al.） | 未使用 | 扩展为轨迹级 VDC，计算前向与后向速度向量夹角 |
| **外观聚合** | EMA（在线） | 平均 ReID（离线） | 根据在线/离线模式自适应切换 |

**Hybrid-SORT** (Yang et al., AAAI 2024) 是典型的在线 SORT 类方法，依赖运动预测 + 匈牙利匹配，无法利用长期时序上下文。**DiffMOT** (Lv et al., CVPR 2024) 引入扩散模型进行关联，但仍沿用逐帧匹配范式。**SUSHI** (Cetintas et al., CVPR 2023) 是 NOOUGAT 最直接的方法论前身——NOOUGAT 复用了其 GNN 层级结构生成局部轨迹，但将滑动窗口 + 启发式拼接替换为 ALT 层的自回归推理，彻底消除了重叠计算和手工拼接规则。**CoNo-Link** (Gao et al., AAAI 2024) 是另一个离线 GNN 跟踪器，同样依赖固定窗口处理。

### 3. 决定性证据与性能边界

**在线模式**：在 DanceTrack 上，NOOUGAT 在线 AssA 超越 Hybrid-SORT 2.3 点，IDF1 提升 3.2 点（Table 1）；在 SportsMOT 上，AssA 超越 Diff-MOT 9.2 点（Table 2）；在 MOT20 上，AssA 超越 DiffMOT 7.0 点（Table 4）。在 BEE24 和 VETRA 等域外数据集上，HOTA 分别超越 TOPICTrack 4.5 点和 BOT-SORT 17.2 点（Tables 11-12），显示出强泛化能力。

**离线模式**：在 DanceTrack 上离线额外提升 3.8 AssA 点（Table 1），SportsMOT 额外提升 8.7 点（Table 2），验证了增加时序上下文（T 增大）带来的持续增益。

**消融证据**：ALT 层在线匹配 HOTA（64.6）显著优于匈牙利算法（62.1）（Table 5）；ALT 层替代 SUSHI 启发式拼接后，IDF1 从 72.0 提升至 76.6（Table 6）；轨迹级 VDC 扩展为离线跟踪器带来 1.4 IDF1 点提升（Table 8）。这些消融直接验证了可学习关联替代启发式的因果效应。

**公平性保障**：所有主要对比方法使用相同的 YOLOX 检测器和 ResNet50-SBS ReID 模型，基准测试均采用固定置信度阈值 0.65（而非序列特定阈值），确保比较的公正性。

### 4. 适用边界与局限

**推理速度**：NOOUGAT 在线模式关联速度约 12 FPS（不含检测），对于需要 >30 FPS 的实时应用仍需优化。离线模式可达 340 FPS（仅关联），但批处理带来延迟。通过调节 T 可在延迟与精度间权衡（Figure 2），但未给出各 T 值下的端到端延迟曲线。

**检测器依赖**：ALT 层依赖于 GNN 层级生成的局部轨迹质量。若检测器严重缺失（如漏检），初始轨迹断开可能传播至全局关联。在 MOT17/MOT20 上，NOOUGAT 离线模式的 MOTA 低于某些基线（如 CoNo-Link），作者归因于固定置信度阈值导致召回较低，暗示检测-关联分离管道可能非最优。

**极端遮挡场景**：论文提供了长期遮挡恢复的定性结果（Figure 5, Figure 6），但缺少量化的恢复率与遮挡时长关系分析。在极低帧率（<1 FPS）场景下的表现亦未量化。

**训练数据依赖**：在 VETRA 等数据稀缺场景，虽然 HOTA 大幅领先（+17.2），但模型的数据驱动特性可能受益于合成数据增强，这一点尚未探索。

### 5. 开放问题

1. **Skip 参数的泛化**：训练中引入的 skip 参数（8 帧跳过）在不同帧率和运动速度的数据集上如何影响性能？是否存在最优 skip 值的自适应选择机制？
2. **ALT 层权重共享**：ALT 层与层级 GNN 的权重共享是否始终有益？在任务差异极大（如航拍 vs 体育）时是否有微调必要？
3. **端到端联合训练**：如果使用端到端检测器（如 DETR 系列），统一训练是否可进一步提升性能并缓解检测缺失对关联的级联影响？
4. **多摄像机扩展**：NOOUGAT 的自回归关联框架能否扩展到多摄像机 3D 跟踪设置（如自动驾驶场景），处理跨摄像机轨迹融合？
5. **极端数据稀缺**：在 VETRA 等场景，能否通过合成数据增强进一步利用模型的数据驱动学习能力？

## 原文 PDF

![[paperPDFs/arxiv_2025/NOOUGAT_Towards_Unified_Online_and_Offline_Multi_Object_Tracking.pdf]]
