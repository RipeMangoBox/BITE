---
title: Rethinking Intermediate Representation for VLM-based Robot Manipulation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Rethinking_Intermediate_Representation_for_VLM_based_Robot_Manipulation.pdf
project_link: null
code_link: null
aliases:
- SSAR
- RIRVBRM
tags:
- CVPR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: 中间表示的设计范式：通过将中间表示分解为语义词汇表和组合语法，并约束 VLM 按照语法规则组装语义词汇，可以同时影响 VLM 可理解性和动作泛化性。
primary_logic: 受上下文无关文法启发，设计一个语义组装表示（SEAM），其中包含紧凑、语义丰富的词汇表和 VLM 友好的语法规则。这使 VLM 能够像自然语言组合一样生成中间表示，将代码生成转化为语义引导的组装过程，从而在高可理解性和强泛化性之间取得平衡。此外，引入基于检索增强生成（RAG）的少样本分割方法，实现了对操作所需细粒度物体部件的高效、精确分割。
claims:
- SEAM 通过将中间表示分解为语义词汇和组合语法，引导 VLM 以语义丰富且逻辑连贯的方式组装词汇，将代码生成转化为语义引导的组装过程。
- SEAM 的词汇 V 对应 CFG 的非终结符、终结符和起始符的并集，提供语义丰富的人类可读词汇；语法 G 对应产生式规则，但采用语义丰富的格式。
- 设计原则包括 VLM 可读性、适当抽象、简洁性、可靠性、适当最简性和可组合性，旨在实现 VLM 可理解性与动作泛化性的平衡。
- RAG 数据库通过存储关键短语和图像-掩码对，并利用 Levenshtein 距离进行检索，实现了细粒度部件分割。
---

# Rethinking Intermediate Representation for VLM-based Robot Manipulation

> [!tip] 核心洞察
> 受上下文无关文法启发，设计一个语义组装表示（SEAM），其中包含紧凑、语义丰富的词汇表和 VLM 友好的语法规则。这使 VLM 能够像自然语言组合一样生成中间表示，将代码生成转化为语义引导的组装过程，从而在高可理解性和强泛化性之间取得平衡。此外，引入基于检索增强生成（RAG）的少样本分割方法，实现了对操作所需细粒度物体部件的高效、精确分割。

| 字段 | 内容 |
|------|------|
| 中文题名 | 重新思考基于 VLM 的机器人操作中间表示 |
| 英文题名 | Rethinking Intermediate Representation for VLM-based Robot Manipulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.19315) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | SEAM (Semantic Assembly Representation) |
| Dataset | Insert the pen in holder, Recycle the battery, Pick up cup/bowl onto the dish, Fit the lid onto the teapot |

> [!tip] 效果简介
> - Insert the pen in holder 上，success rate (closed-loop) 8/10 (80%) vs 7/10 (70%) [OmniManip closed-loop] (+1/10 (+10%))。
> - Recycle the battery 上，success rate (closed-loop) 8/10 (80%) vs 8/10 (80%) [OmniManip closed-loop] (0)。
> - Pick up cup/bowl onto the dish 上，success rate (closed-loop) 9/10 (90%) vs 8/10 (80%) [OmniManip closed-loop] (+1/10 (+10%))。

## 概要

### 问题背景

基于视觉-语言模型（VLM）的机器人操作面临一个核心瓶颈：**中间表示（intermediate representation）的设计需要在 VLM 可理解性和动作泛化性之间做出权衡**。高层表示（如预定义技能词 `pick`、`place`、`insert`）易于 VLM 理解，但泛化能力差——每遇到新任务都需手动扩充词汇表；低层表示（如关键点坐标、空间轴约束 `get_keypoint`、`move_to`）泛化性好，但要求 VLM 生成复杂的数值约束，导致输出不可靠。这一矛盾制约了 VLM 在开放场景机器人操作中的实用化。

### 核心方法：SEAM

本文提出 **SEAM（Semantic Assembly Representation，语义组装表示）**，核心思想受上下文无关文法（CFG）启发：将中间表示分解为**语义词汇表 $V$** 和**组合语法 $G$**，引导 VLM 按语法规则组装语义词汇，将代码生成转化为语义引导的组装过程。SEAM 在 VLM 可理解性与动作泛化性之间取得平衡——词汇表紧凑且语义丰富，语法规则对 VLM 友好。

同时，针对细粒度物体部件分割的难题，引入**基于检索增强生成（RAG）的少样本分割方法**：构建图像-掩码对数据库，利用 Levenshtein 距离检索匹配样本，再通过少样本分割网络生成查询图像的部件掩码，实现高效、精确的开放词汇部件级分割。

### 主要结果

在 8 项真实世界机器人操作任务上，SEAM 的闭环平均成功率达 **83.8%**，较先前最优方法 OmniManip 的 68.8% 提升 **15%**。在“按下红色按钮”任务中达到 10/10 完美成功率，在“盖上茶壶盖”任务中领先 20%。消融实验表明，SEAM 在动作泛化性（AG）和 VLM 可理解性（VC）两个指标上实现了平衡，避免了高层表示泛化性差和低层表示可理解性差的极端；RAG 分割方法在精度和运行效率（0.6s）上均优于 OV-Seg、Grounded SAM 等现有方法。

### 方法定位

SEAM 属于**基于 VLM 的中间表示引导范式**，与以下工作形成对比：
- **高层表示**（如 Instruct2Act）：预定义技能词，VLM 可理解性好但泛化需手动扩展；
- **低层表示**（如 VoxPoser 的价值地图、CoPa 的组件级空间约束、ReKep 的关系关键点约束）：动作泛化性强但 VLM 难以可靠生成；
- **OmniManip**（操作感知原语）：当前 SOTA，SEAM 在其基础上通过语义组装和 RAG 分割实现显著提升。

### 问题背景：VLM 驱动的机器人操作与中间表示的瓶颈

视觉语言模型（VLM）在机器人操作中展现出强大的高层推理能力，但其输出无法直接驱动机器人执行。为此，现有方法普遍引入**中间表示**作为 VLM 推理与机器人动作之间的桥梁。中间表示的设计直接影响两个关键属性：**VLM 可理解性**与**动作泛化性**。然而，这两者之间存在根本性的权衡。

### 现有方法的缺口：高层与低层表示的两难

当前中间表示可归为两类范式，各自存在明显缺陷：

- **高层表示**：以预定义技能词为核心。VLM 只需从有限词汇中选择语义明确的词，可理解性高。但其动作泛化性差——每引入一个新任务，就需要手动扩充词汇表，无法自动适应未见过的操作场景。
- **低层表示**：以关键点、空间轴等几何约束为核心。这类表示抽象程度高，泛化能力强，可覆盖多样化的操作动作。但 VLM 需要生成复杂的约束条件，难以稳定输出可靠结果，导致可理解性低下。

这种两难困境构成了当前基于 VLM 的机器人操作系统的核心瓶颈：**高层表示易于理解但泛化不足，低层表示泛化性强但难以理解**。

### 本文动机：以语义组装打破权衡

受上下文无关文法启发，本文提出一种新的中间表示设计范式——**语义组装表示 SEAM**。核心思路是将中间表示分解为两个组件：**语义词汇表**和**组合语法**。VLM 不再直接生成代码或约束，而是按照语法规则从语义词汇中选取并组装词汇，将代码生成转化为语义引导的组装过程。

这一设计的关键在于：词汇表提供语义丰富、人类可读的原子操作，确保 VLM 可理解性；语法规则约束组装方式，使得有限词汇能组合出覆盖广泛任务的表示，保障动作泛化性。两者协同，在高可理解性与强泛化性之间取得平衡。

此外，针对操作中对细粒度物体部件的分割需求，本文引入基于检索增强生成的少样本分割方法，通过构建图像-掩码对数据库并以 Levenshtein 距离检索，实现高效、精确的部件级开放词汇分割。

## 核心方法与创新机理

### 瓶颈洞察：VLM 可理解性与动作泛化性的根本权衡

现有基于 VLM 的机器人操作框架普遍面临一个结构性困境：**中间表示的设计在“VLM 可理解性”与“动作泛化性”之间难以兼得**。

- **高层表示**（如预定义技能词 `pick`、`place`、`insert` 等）语义清晰，VLM 易于生成，但泛化能力极差——每引入一个新任务，就需要手动扩充词汇表，模型无法自动适应未见过的操作场景。
- **低层表示**（如关键点坐标 `get_keypoint`、轴约束 `move_to` 等）泛化性强，能够描述任意精细动作，但要求 VLM 生成复杂的空间约束，导致输出不可靠、可理解性骤降。

这一权衡构成了本工作的核心动机：**能否设计一种中间表示范式，同时获得高层的 VLM 可理解性与低层的动作泛化性？**

### 核心机制：语义组装表示 (SEAM)

论文的核心创新是 **SEAM (Semantic Assembly Representation)**，其关键设计理念受**上下文无关文法 (CFG)** 启发，将中间表示分解为两个正交组件：

1. **语义词汇表 (Vocabulary V)**：一组语义丰富、人类可读的操作原语，如 `get_centroid`、`get_axis`、`move_cost` 等。词汇表对应 CFG 中非终结符、终结符与起始符的并集，但采用语义化命名，使 VLM 能像理解自然语言一样理解每个词元的含义。
2. **组合语法 (Grammar G)**：一组 VLM 友好的产生式规则，约束 VLM 按照语法规则组装语义词汇，而非自由生成代码。语法采用语义丰富的格式，而非形式化符号，使组装过程类似于自然语言组合。

这一设计的本质转变在于：**将代码生成重新定义为语义引导的组装过程**。VLM 不再需要凭空生成复杂的约束代码，而是从一个紧凑的语义词汇表中选取词元，按语法规则组合成中间表示 $R = VLM(L, I)$，其中 $L$ 为人类指令，$I$ 为视觉输入。从语言学视角，中间表示被建模为 $\tilde{R} = (V, G)$，即词汇表与语法的二元组。

SEAM 的设计遵循六项原则：**VLM 可读性、适当抽象、简洁性、可靠性、适当最简性、可组合性**，这些原则共同确保了表示在可理解性与泛化性之间的平衡。

### Changed Slot 1：中间表示设计范式的根本转变

| 维度 | Baseline 范式 | SEAM 范式 |
|------|--------------|-----------|
| **表示形式** | 高层：固定技能词（需手动扩充）；低层：关键点/轴约束 | 语义词汇 + 组合语法的组装表示 |
| **VLM 角色** | 直接生成代码或约束 | 从词汇表中选词并按语法组装 |
| **泛化机制** | 高层靠人工添加新词；低层靠约束组合 | 词汇复用 + 语法组合实现零样本泛化 |
| **可理解性** | 高层易理解但泛化差；低层泛化好但易出错 | 语义词汇天然可读，语法约束保证可靠性 |

这一转变的核心优势在于：当面对新任务时，VLM 只需用已有词汇表中的词元，按照语法规则重新组合，无需引入新词汇。这从根本上解决了高层表示“每任务需手动扩充词汇”的痛点，同时避免了低层表示“需生成复杂约束”的不可靠性。

### Changed Slot 2：从通用分割到基于 RAG 的少样本细粒度分割

传统方法依赖通用开放词汇分割（如 OV-Seg、Grounded SAM），通常只能分割整个物体，无法精确定位操作所需的**细粒度物体部件**（如茶壶的壶口边缘、笔筒的开口）。

SEAM 流水线引入了一个**基于检索增强生成 (RAG) 的少样本分割模块**：

- **RAG 数据库**：存储关键短语与图像-掩码对的映射关系，为每个可操作部件提供支持样本。
- **检索机制**：利用 Levenshtein 距离匹配查询短语与数据库中的关键短语，检索最相关的支持图像与掩码。
- **少样本分割网络**：以检索到的支持图像-掩码对为条件，在查询图像上生成目标部件掩码。

这一设计实现了两个关键突破：
1. **细粒度定位**：能够精确分割操作所需的物体部件（如壶口、按钮），而非整个物体，直接支撑后续的轨迹优化。
2. **效率优势**：分割耗时仅 0.6s，优于 LISA (0.9s) 和 Grounded SAM (10.2s)，满足实时操作需求。

### 创新验证：泛化性与可理解性的量化平衡

论文通过两个自定义指标量化验证了 SEAM 的设计优势：

- **动作泛化性 (AG)**：$AG = 1 - \frac{|\mathcal{V}|}{T}$，即完成 $T$ 个任务所需唯一词汇操作数越少，泛化性越强。
- **VLM 可理解性 (VC)**：$VC = \frac{N_{succ}}{T}$，即 VLM 成功生成正确中间表示的任务比例。

在 Figure 8 的对比分析中，SEAM 在 AG 与 VC 两个维度上均优于纯高层表示（如 Instruct2Act）和纯低层表示（如 ReKep），验证了其“语义组装”设计确实在可理解性与泛化性之间取得了平衡。这一结果并非偶然——词汇表与语法的分离设计使 VLM 既能理解每个词元的语义，又能通过语法组合应对新任务，从而同时提升两个指标。

SEAM 的整体 pipeline 将“基于 VLM 的机器人操作”分解为三个解耦模块：**SEAM 生成模块**、**RAG 分割模块**和**轨迹优化模块**，三者以中间表示为核心纽带，形成从视觉-语言理解到机器人动作执行的端到端流程。图 2 给出了完整的模块关系与数据流。

### 输入与输出流

给定当前场景的 RGB-D 观察图像和自然语言任务指令，pipeline 的输入输出流如下：

1. **VLM 接收多模态输入**：将观察图像与任务指令同时输入 VLM（统一使用 Qwen3-VL-30B-22A）。
2. **生成 SEAM 中间表示**：VLM 依据预定义的语义词汇表 $V$ 和组合语法 $G$，以“语义组装”的方式生成结构化中间表示 $R$。该过程可形式化为 $R = \text{VLM}(L, I)$，其中 $L$ 为人类指令，$I$ 为视觉输入。
3. **RAG 分割定位目标部件**：从指令中解析出目标物体部件名称，通过 RAG 数据库检索最匹配的图像-掩码对，再利用少样本分割网络对当前场景中的细粒度物体部件进行精确分割。
4. **轨迹优化求解夹爪位姿**：将 SEAM 表示中的语义约束转化为可微分的语言成本函数，结合场景点云与分割出的物体部件点云，通过最小化成本并加入平移/旋转正则项，求解夹爪的最优轨迹位姿 $\mathbf{R}, \mathbf{t}$。

### 模块间关系

三个模块之间的依赖关系清晰且单向：

- **SEAM 生成模块**是整个系统的“语义大脑”，负责将高层任务意图转化为结构化的中间表示。该模块的输出直接决定了后续模块的约束空间——词汇表中的函数签名（如 `get_centroid(object_part_name:Str) → Point`、`move_cost(pt1:Point, pt2:Point, offset:List) → Cost`）为轨迹优化提供了语义丰富的成本项。
- **RAG 分割模块**为 SEAM 中的物体部件引用提供视觉定位支持。SEAM 词汇表中的函数参数（如 `object_part_name`）需要精确的 3D 定位，RAG 分割模块通过检索增强的少样本学习，实现了对“茶壶口沿”、“笔筒孔洞”等细粒度部件的分割，其输出点云直接馈入轨迹优化模块。
- **轨迹优化模块**是执行层，将前两个模块的语义约束和几何信息统一为优化问题，通过求解 $\underset{\mathbf{R},\mathbf{t}}{\mathrm{min}}$ 目标函数得到可执行的夹爪轨迹。

### 设计动机：解耦与平衡

该 pipeline 的核心设计动机在于解决现有方法中“VLM 可理解性”与“动作泛化性”之间的根本权衡。高层表示（如 **Instruct2Act** 的预定义技能词）易于 VLM 理解但泛化性差，需为每个新任务手动添加词汇；低层表示（如 **ReKep** 的关系关键点约束）泛化性好但需生成复杂约束，导致 VLM 输出不可靠。SEAM 通过将中间表示建模为 $\tilde{R} = (V, G)$ 的二元组——即语义词汇表与组合语法的分离设计——使 VLM 能够像自然语言组合一样组装中间表示，从而在高可理解性与强泛化性之间取得平衡。这一平衡在后续实验中通过动作泛化性指标 $\mathrm{AG} = 1 - \frac{|\mathcal{V}|}{T}$ 和 VLM 可理解性指标 $\mathrm{VC} = \frac{N_{\mathrm{succ}}}{T}$ 得到定量验证（见 Figure 8）。

![[assets/figures/papers/paper_list_l2412_https_arxiv_org_abs_2511_19315/figures/002_Figure_2.jpg]]
*Figure 2: Overall pipeline of our method. Given the current observation and the task instruction, our method first generates the (a) Semantic Assembly Representation (SEAM) with designed vocabulary and grammar, and then (b) translated into an intermediate representation. Next, we retrieve the corresponding support images and support masks from (c) the Retrieval Augmented Generation (RAG) Database and (d) segment the target object parts in the scene. Finally, we solve the gripper’s trajectories for (e) robotic execution*

### 3.1 中间表示的形式化建模

SEAM 将 VLM 生成中间表示的过程建模为语言翻译问题。给定人类指令 $L$ 和视觉观察 $I$，VLM 输出中间表示 $R$：

$$R = \text{VLM}(L, I)$$

进一步，将中间表示 $R$ 抽象为语言学二元组 $\tilde{R} = (V, G)$，其中 $V$ 为语义词汇表，$G$ 为组合语法。这一形式化将代码生成转化为**语义引导的词汇组装过程**，使 VLM 在受约束的语义空间内进行推理，而非自由生成代码。

### 3.2 上下文无关文法的语义适配

SEAM 借鉴上下文无关文法（CFG）的四元组结构 $(V, \Sigma, R, S)$，但做了面向 VLM 可理解性的语义化改造：

- **词汇表 $V$**：对应 CFG 中非终结符 $V$、终结符 $\Sigma$ 和起始符 $S$ 的并集，但全部替换为**语义丰富、人类可读的词汇**，如 `get_centroid`、`get_axis`、`move_cost` 等，而非抽象符号。
- **语法 $G$**：对应 CFG 的产生式规则 $R$，但采用**语义丰富的格式**编写，使 VLM 能像理解自然语言组合规则一样遵循语法约束。

这种设计保留了 CFG 的结构严谨性，同时消除了抽象符号对 VLM 的认知负担。

### 3.3 SEAM 词汇与语法的设计原则

SEAM 的词汇表与语法设计遵循六项原则（Section 3.3），共同作用于 VLM 可理解性与动作泛化性的平衡：

1. **VLM 可读性**：词汇和语法使用自然语言描述，与 VLM 的预训练分布对齐。
2. **适当抽象**：词汇既不过于高层（如单一技能词 `pick`），也不过于底层（如关节角度），而是定位于语义中间层。
3. **简洁性**：词汇表保持紧凑，避免冗余操作原语。
4. **可靠性**：每个词汇对应的底层执行逻辑是确定性的，减少歧义。
5. **适当最简性**：语法规则足够简单，使 VLM 能可靠地组合词汇，但不牺牲表达能力。
6. **可组合性**：词汇可按语法规则自由组装，支持未见任务的泛化。

词汇表 $V$ 与语法 $G$ 的具体设计详见 Table 1，其中包含函数签名如 `get_centroid(object_part_name: Str) → Point` 和 `move_cost(pt1: Point, pt2: Point, offset: List) → Cost` 等语义原语。

### 3.4 基于 RAG 的少样本分割模块

为实现细粒度物体部件定位，SEAM 引入基于检索增强生成（RAG）的少样本分割流水线：

- **RAG 数据库构建**：存储关键短语与对应的**图像-掩码对**（support image 和 support mask），作为少样本分割的参考样本。
- **检索机制**：给定目标部件名称（如 “teapot opening”），利用 **Levenshtein 距离**在数据库中进行短语匹配，检索最相关的图像-掩码对。
- **分割执行**：将检索到的 support image-mask 对与查询图像一同输入少样本分割网络，生成目标部件的精确掩码。

该模块在分割精度和运行效率上均优于通用开放词汇分割方法（如 OV-Seg、Grounded SAM），运行时间仅 0.6s（Table 3）。

### 3.5 轨迹优化目标函数

SEAM 将生成的中间表示转化为**可微分的成本函数**，通过轨迹优化求解夹爪最优位姿。优化问题形式化为：

$$
\begin{array}{rl}
\underset{\mathbf{R},\mathbf{t}}{\mathrm{min}} & \mathrm{language}\left(P^s \cup \left(\mathbf{R}\mathbf{R}_0^{-1}(P^m - \mathbf{t}_0) + \mathbf{t}\right)\right) \\
& \quad + \alpha\|\mathbf{t} - \mathbf{t}_0\|_2 + \beta\|\mathrm{euler}(\mathbf{R}\mathbf{R}_0^{-1})\|_1
\end{array}
$$

**变量含义**：

- $P^s$：场景点云
- $P^m$：受约束物体（manipulated object）的模型点云
- $\mathbf{R}_0, \mathbf{t}_0$：夹爪当前位姿（旋转矩阵和平移向量）
- $\mathbf{R}, \mathbf{t}$：待优化的目标位姿
- $\mathrm{language}(\cdot)$：由 SEAM 中间表示定义的语言成本函数，对点云的空间关系施加语义约束
- $\alpha\|\mathbf{t} - \mathbf{t}_0\|_2$：平移 L2 正则项，抑制大幅度位移
- $\beta\|\mathrm{euler}(\mathbf{R}\mathbf{R}_0^{-1})\|_1$：旋转欧拉角 L1 正则项，抑制大幅度旋转

**优化机制**：将物体模型点云 $P^m$ 从当前位姿变换到候选目标位姿后，与场景点云 $P^s$ 合并，计算语言成本。通过最小化该成本并加入平滑正则，求解出满足语义约束且运动幅度最小的夹爪位姿。

## 实验与关键发现

### 实验设置

实验在真实世界环境中进行，硬件系统由一台配备夹爪的 UR5 机器人以及两台分别部署在工作空间两侧的 RealSense D435 相机组成（Figure 4）。所有任务中，物体的位置与朝向均随机初始化，每个方法在每项任务上重复执行 10 次以减少随机偏差。对比实验统一使用 Qwen3-VL-30B-22A 作为 VLM 骨干，并采用相同的参考提示框架，确保公平比较。

### 主实验结果

Table 2 汇总了 SEAM 与多个基线方法在 8 项真实世界操作任务上的闭环成功率对比。SEAM 在全部 8 项任务上取得 83.8% 的平均成功率，较主要基线 OmniManip 的 68.8% 提升 15 个百分点。在精细对齐要求较高的任务上，SEAM 的优势尤为显著：在“Fit the lid onto the teapot”任务中，SEAM 成功率达 70%，OmniManip 为 50%（+20%）；在“Press the red button”任务中，SEAM 以 100% 的成功率远超 OmniManip 的 70%（+30%）。在“Open the drawer”和“Open the jar”任务上，SEAM 分别领先 20%。在其余任务上，SEAM 与 OmniManip 持平或领先 10%。

![[assets/figures/papers/paper_list_l2412_https_arxiv_org_abs_2511_19315/figures/007_Table_2.jpg]]
*Table 2: Performance comparison across different methods*

### 中间表示生成质量分析

Figure 6 以“将笔放入笔筒”任务为例，对比了不同方法生成的中间表示。SEAM 生成的表示以语义组装方式描述操作约束（如 `get_centroid`、`move_cost` 等语义词汇的组合），逻辑连贯且易于 VLM 理解。相比之下，高层表示（如 Instruct2Act 的技能词）虽简洁但泛化性受限，低层表示（如 ReKep 的关键点约束）则需生成复杂约束，导致 VLM 输出不可靠。

![[assets/figures/papers/paper_list_l2412_https_arxiv_org_abs_2511_19315/figures/008_Figure_6.jpg]]
*Figure 6: Comparisons among the intermediate representation generated by state-of-the-art methods and our methods for the task “put the pen into the penholder”*

### 开放词汇分割性能

Figure 3 展示了开放词汇分割的定性对比结果。基于 RAG 的少样本分割方法能够精确分割操作所需的细粒度物体部件（如茶壶口边缘、按钮表面），而 OV-Seg、Grounded SAM 等通用分割方法往往只能分割整个物体或无法定位交互部件。Table 3 的耗时对比进一步显示，RAG 分割方法平均耗时仅 0.6 秒，显著快于 Grounded SAM 的 10.2 秒和 LISA 的 0.9 秒，实现了效率与精度的双重优势。

![[assets/figures/papers/paper_list_l2412_https_arxiv_org_abs_2511_19315/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative performance comparisons for open vocabulary segmentation between the state-of-the-art methods and our methods on common manipulation*

![[assets/figures/papers/paper_list_l2412_https_arxiv_org_abs_2511_19315/figures/010_Table_3.jpg]]
*Table 3: Comparisons of time elapse between our method and the state-of-the-art methods*

Figure 7 针对“将茶壶盖盖到茶壶上”任务进行了定位与执行的联合分析。RAG 分割方法成功定位到茶壶开口的精细边缘区域，使得后续轨迹优化能够生成准确的对齐动作并成功完成任务；而对比方法未能精确定位开口位置，导致执行失败。

![[assets/figures/papers/paper_list_l2412_https_arxiv_org_abs_2511_19315/figures/009_Figure_7.jpg]]
*Figure 7: Comparisons among open-vocabulary localization for “teapot opening”and their corresponding execution results in the task “fit the teapot lid on the teapot”*

### 动作泛化性与 VLM 可理解性权衡

Figure 8 和 Table 4 从动作泛化性（AG）和 VLM 可理解性（VC）两个维度对各类中间表示进行了定量分析。AG 指标定义为 $1 - |\mathcal{V}|/T$，衡量完成所有任务所需的唯一词汇操作数占比，值越高表示泛化能力越强；VC 指标定义为 $N_{\mathrm{succ}}/T$，衡量 VLM 生成正确中间表示的比率。

SEAM 在两个指标上实现了平衡：其 AG 值显著高于高层表示（后者因需为每个新任务手动添加词汇而泛化性差），同时 VC 值显著高于低层表示（后者因需生成复杂约束导致 VLM 理解困难）。Table 4 进一步揭示了各方法在词汇表 V 和语法 G 设计上的差异——SEAM 通过语义丰富、紧凑的词汇表和 VLM 友好的语法规则，在可理解性与泛化性之间取得了最优折衷。

### 失败模式分析

尽管 SEAM 整体表现优异，部分任务仍存在失败案例。在“Fit the lid onto the teapot”任务中，失败主要源于茶壶开口的精细分割在极端视角或光照条件下出现偏差，导致后续对齐动作不准。在“Open the jar”任务中，失败案例多与夹爪抓取点选择有关——当罐盖边缘特征不明显时，RAG 检索到的支持掩码与查询图像的匹配精度下降。这些失败模式提示，分割模块的鲁棒性在低纹理或遮挡场景下仍有提升空间。

## 定位与知识库关联

### 核心问题定位：中间表示的双重困境

基于 VLM 的机器人操作面临一个根本性权衡：**VLM 可理解性**（VLM-comprehensibility）与**动作泛化性**（action-generalizability）难以兼得。现有方法在两个极端之间摇摆：

- **高层表示**（如 **Instruct2Act** 的预定义技能词 `pick`、`place`、`insert`）：语义清晰，VLM 易于生成正确输出，但每引入一个新任务就需手动扩充词汇表，动作泛化性差。
- **低层表示**（如 **VoxPoser** 的价值地图、**CoPa** 的组件级空间约束、**ReKep** 的关系关键点约束）：泛化能力强，可灵活组合出多样动作，但要求 VLM 生成复杂约束，导致输出不可靠。

这一瓶颈的本质在于：**中间表示的设计范式直接决定了 VLM 推理与动作执行之间的信息传递效率**。SEAM 的核心洞察是，若能约束 VLM 按照组合语法规则组装语义词汇，就能同时影响可理解性和泛化性两个维度。

### SEAM 的方法定位：语义组装范式

SEAM 提出了一种新的中间表示设计范式——**语义组装表示**（Semantic Assembly Representation），其设计灵感来自上下文无关文法（CFG）。形式上，SEAM 将中间表示建模为二元组 $\tilde{R} = (V, G)$：

- **词汇表 $V$**：对应 CFG 中非终结符、终结符和起始符的并集，但提供语义丰富、人类可读的操作原语，如 `get_centroid(object_part_name:Str) → Point`、`move_cost(pt1:Point, pt2:Point, offset:List) → Cost`。
- **语法 $G$**：对应产生式规则，采用语义丰富的格式，引导 VLM 以自然语言组合的方式组装词汇。

与 CFG 的严格形式化不同，SEAM 的语法规则经过 VLM 友好化设计，遵循六项原则：VLM 可读性、适当抽象、简洁性、可靠性、适当最简性和可组合性（Section 3.3）。这使得 VLM 的代码生成过程被转化为**语义引导的组装过程**，在高可理解性和强泛化性之间取得平衡。

### 与现有方法的对比定位

| 方法 | 表示层级 | 核心机制 | 泛化性 | 可理解性 | 关键局限 |
|------|---------|---------|--------|---------|---------|
| **Instruct2Act** | 高层 | 预定义技能词 | 低（需手动扩充词汇） | 高 | 词汇封闭，新任务需人工介入 |
| **VoxPoser** | 低层 | 价值地图轨迹合成 | 高 | 低 | 生成复杂 3D 价值图不可靠 |
| **CoPa** | 低层 | 组件级空间约束 | 高 | 低 | 约束生成质量依赖 VLM 推理 |
| **ReKep** | 低层 | 关系关键点约束 | 高 | 低 | 关键点关系复杂时易出错 |
| **OmniManip** | 中层 | 操作感知原语 | 中 | 中 | 作为主要对比基线，闭环比 SEAM 低 15% |
| **SEAM (本文)** | 语义组装 | 词汇+语法约束组装 | 高 | 高 | 词汇和语法需预先设计 |

在定量对比中，SEAM 在 8 个真实世界任务上取得了 **83.8% 的平均闭环成功率**，比 OmniManip 的 68.8% 高出 15 个百分点（Table 2）。尤其在需要精细对齐的任务（如“盖上茶壶盖”、“按下红色按钮”）上，SEAM 的优势更为显著（分别领先 20% 和 30%）。

### RAG 分割模块的定位

在物体部件分割方面，现有方法（如 OV-Seg、Grounded SAM）通常只能分割整个物体，无法精确定位交互所需的细粒度部件。SEAM 引入的 **RAG 少样本分割方法**通过以下机制实现突破：

- 构建图像-掩码对数据库，存储关键短语与对应分割掩码；
- 利用 Levenshtein 距离进行检索匹配；
- 通过少样本分割网络生成查询图像的掩码。

该方法在分割精度上优于 SOTA 方法，且运行时间最短（0.6s vs LISA 0.9s、Grounded SAM 10.2s）（Table 3），为实时机器人操作提供了可行方案。

### 适用边界与局限

SEAM 的设计依赖预先定义的语义词汇表和组合语法规则，这意味着：

1. **词汇覆盖范围**：词汇表 $V$ 的设计决定了方法能处理的任务类型上限。虽然 SEAM 的泛化性优于高层表示，但其词汇仍为封闭集合，面对完全未见过的操作类型可能需要扩展。
2. **语法表达能力**：组合语法 $G$ 的表达能力受限于设计者的先验知识。对于需要极其复杂空间推理的任务，语法规则可能不足以描述完整约束。
3. **VLM 依赖性**：SEAM 的可理解性优势建立在 VLM 对语义词汇和语法的理解能力之上。当底层 VLM 能力不足时，组装过程仍可能出错。
4. **RAG 数据库构建**：少样本分割的性能依赖于 RAG 数据库中支持图像-掩码对的质量和覆盖度，对于极端罕见的物体部件可能需要额外标注。

### 开放问题

- SEAM 的词汇和语法设计目前依赖人工专家知识。是否可能通过自动发现或学习的方式从任务演示中提取语义词汇和组合规则？
- 在更复杂的多步长序列操作中，SEAM 的组装范式如何扩展以支持时序依赖和条件分支？
- RAG 分割方法在高度遮挡或光照极端的场景下的鲁棒性尚需进一步验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/Rethinking_Intermediate_Representation_for_VLM_based_Robot_Manipulation.pdf]]
