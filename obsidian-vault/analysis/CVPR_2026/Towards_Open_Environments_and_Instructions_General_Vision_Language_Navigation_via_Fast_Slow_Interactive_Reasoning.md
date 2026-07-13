---
title: "Towards Open Environments and Instructions: General Vision-Language Navigation via Fast-Slow Interactive Reasoning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Towards_Open_Environments_and_Instructions_General_Vision_Language_Navigation_via_Fast_Slow_Interactive_Reasoning.pdf
project_link: null
code_link: null
aliases:
- SVFSIRF
- TOEIGVLNFSIR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过慢推理模块对快推理模块的历史轨迹进行反思，提取并存储结构化通用经验，并通过注意力机制将这些经验动态融合到快推理决策中，实现快慢交互。
primary_logic: 借鉴人类双系统认知理论，构建动态交互式快慢推理框架，使快推理能够在遇到复杂场景时检索并利用慢推理积累的通用经验，从而在不重新调用慢推理的情况下提升泛化能力和决策效率。
claims:
- 在GSA-R2R基准上，我们的方法在基本指令下的测试集（Test-R-Basic和Test-N-Basic）上分别取得70.8和58.4的SR，优于GR-DUET，相对提升分别为1.5%和2.2%。
- 在场景指令下，我们的方法在Test-N-Scene上达到50.7 SR，相比GR-DUET的48.1 SR提升2.6个百分点。
- 消融实验表明，快慢推理（FSR）和指令风格转换（ISC）模块都对性能有贡献，二者结合达到最佳效果（Test-N-Scene SR=50.4）。
- 经验库的最佳容量在50到100之间，过小会导致经验不足，过大则会引入冗余；Test-R-Basic在K=50最优，Test-N-Scene在K=100最优。
---

# Towards Open Environments and Instructions: General Vision-Language Navigation via Fast-Slow Interactive Reasoning

> [!tip] 核心洞察
> 借鉴人类双系统认知理论，构建动态交互式快慢推理框架，使快推理能够在遇到复杂场景时检索并利用慢推理积累的通用经验，从而在不重新调用慢推理的情况下提升泛化能力和决策效率。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向开放环境与指令：通过快慢交互推理实现通用视觉-语言导航 |
| 英文题名 | Towards Open Environments and Instructions: General Vision-Language Navigation via Fast-Slow Interactive Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.09111) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | slow4fast-VLN (Fast-Slow Interactive Reasoning Framework) |
| Dataset | GSA-R2R Test-R-Basic, GSA-R2R Test-N-Basic, GSA-R2R Test-N-Scene |

> [!tip] 效果简介
> - GSA-R2R Test-R-Basic 上，SR 70.8 vs GR-DUET (improvement +1.5% implied) (+1.5%)。
> - GSA-R2R Test-N-Basic 上，SR 58.4 vs GR-DUET (improvement +2.2% implied) (+2.2%)。
> - GSA-R2R Test-N-Scene 上，SR 50.7 ±0.1 vs 48.1 ±0.1 (GR-DUET) (+2.6)。

## 概要

本文针对视觉-语言导航（VLN）在开放世界中的泛化瓶颈，提出了 **slow4fast-VLN** 框架。现有方法在训练集（住宅场景）与测试集（商场、办公室、影院等非住宅场景）分布偏移时性能急剧下降，其根本原因在于缺乏对**快慢双系统认知过程**的显式建模，导致模型在分布外（OOD）场景下推理路径不稳定。

核心思路借鉴人类双系统认知理论，构建了一个**动态交互式快慢推理框架**：快推理模块（基于DUET架构的端到端策略网络）负责实时动作决策并积累历史记忆；慢推理模块利用大语言模型（LLM）对历史轨迹进行反思，提取**结构化通用经验**（场景类型、空间上下文、空间规则、导航策略、历史成功率等），存储于经验库中；在后续推理时，通过多头注意力机制将相关经验动态融合到快推理的视觉特征中，使模型在遇到复杂场景时能检索并利用积累的经验，从而在不重新调用慢推理的情况下提升泛化能力与决策效率。此外，通过LLM思维链提示工程将场景/用户风格指令统一转换为基本风格指令，进一步缓解指令多样性带来的泛化压力。

在**GSA-R2R**基准上，该方法在基本指令下（Test-R-Basic / Test-N-Basic）分别取得 **70.8** 和 **58.4** 的成功率（SR），优于基线 **GR-DUET**（Hong et al., arXiv 2025），相对提升分别为1.5%和2.2%；在场景指令下（Test-N-Scene）达到 **50.7** SR，提升2.6个百分点。消融实验证实快慢推理（FSR）与指令风格转换（ISC）模块均对性能有正向贡献，二者结合效果最优。案例研究表明，慢推理经验增强后导航时间减少46.7%，导航误差降低80%。经验库容量在50–100之间最优，需根据场景复杂度手工调整，是该框架当前的一个实用限制。

视觉-语言导航（Vision-Language Navigation, VLN）要求智能体在真实三维环境中依据自然语言指令进行自主导航。近年来，VLN在封闭场景设定下取得了显著进展，但现有方法普遍面临一个根本性瓶颈：**在开放世界中的泛化能力不足**。其深层原因在于，现有方法缺乏对快慢认知过程的显式建模，导致在分布外（OOD）场景下推理路径不稳定，产生类似幻觉的错误决策。

具体而言，当前VLN范式存在两大核心挑战。其一，**场景泛化鸿沟**：训练集通常局限于住宅环境，而测试集可能包含商场、办公室、电影院等非住宅场景（见图1），视觉外观和空间布局的巨大差异使得单一推理网络难以可靠迁移。其二，**指令多样性冲击**：真实应用中的指令不仅包括简洁的基本指令，还涵盖场景风格指令和用户个性化指令，指令风格的剧烈变化进一步加剧了模型的泛化压力。

现有工作如**GR-DUET**（Hong et al., arXiv 2025）尝试通过视觉特征适应来缓解场景漂移，但其本质上仍是单次推理范式——每次导航独立决策，缺乏对历史经验的积累与复用。这种设计忽略了人类认知中的一个关键机制：**双系统理论**（Dual-Process Theory）。人类在决策时，快系统负责直觉式快速响应，慢系统则进行深度反思并提炼通用经验，两者动态交互以应对复杂多变的环境。

受此启发，本文提出 **slow4fast-VLN** 框架，核心动机是构建一个动态交互式快慢推理系统：快推理模块（端到端策略网络）负责实时动作输出与记忆积累，慢推理模块（基于LLM的反思网络）对历史轨迹进行结构化反思，提取通用经验并反馈至快推理决策。这一设计使得智能体在遇到复杂场景时，能够检索并利用慢推理积累的经验，从而在不重新调用慢推理的情况下提升泛化能力和决策效率，从根本上缓解开放环境下的推理不稳定性问题。

## 核心方法与创新机理

### 1. 从单一推理到快慢交互双系统

现有视觉-语言导航方法（如 **GR-DUET**，Hong et al., arXiv 2025）普遍采用单一推理网络进行端到端的顺序决策。这类方法在开放世界中面临一个根本性瓶颈：当场景分布发生偏移（OOD）时，推理路径不稳定，类似于幻觉现象，导致泛化能力急剧下降。

本文的核心创新在于从认知科学中汲取灵感，将人类双系统认知理论映射为导航智能体的推理架构。具体而言，方法构建了一个动态交互式快慢推理框架 **slow4fast-VLN**，其形式化定义为：

$$\mathcal { F } = \langle \pi , R , M , A \rangle$$

其中 $\pi$ 为快推理策略网络，$R$ 为慢推理反思函数，$M$ 为经验提取与存储模块，$A$ 为经验赋能函数。每个导航回合 $k$ 的迭代过程为：

$$L _ { k } = \pi ( I _ { k } , E n v ) , \quad R _ { k } = R ( L _ { k } ) , \mathcal { E } _ { k } = M ( R _ { k } ) , \quad \pi _ { k + 1 } = A ( \pi _ { k } , \mathcal { E } _ { k } )$$

这一设计的因果调控机制在于：**慢推理模块对快推理模块的历史轨迹进行反思，提取结构化通用经验，并通过注意力机制动态融合到快推理的决策过程中**。这使得快推理在遇到复杂场景时，能够检索并利用慢推理积累的经验，从而在不重新调用慢推理的情况下提升泛化能力和决策效率。

### 2. 关键改变槽位（Changed Slots）

| 改变维度 | 基线方法（GR-DUET） | 本文方法（slow4fast-VLN） |
|----------|---------------------|--------------------------|
| **推理框架** | 单一策略网络（DUET）顺序决策 | 动态交互式快慢双系统：快推理产生动作并积累记忆，慢推理反思记忆生成经验并反馈给快推理 |
| **经验利用** | 无经验积累，每次导航独立 | 通过LLM反思从历史轨迹中提取结构化经验，存储于经验库，推理时通过多头注意力融合到视觉特征中 |
| **指令处理** | 直接使用原始多样指令 | 通过LLM思维链提示工程将场景/用户风格指令转换为统一的基本风格指令 |

### 3. 经验积累与融合机制

快推理模块（基于DUET架构的策略网络）在每一步生成历史记忆，其数据结构为：

$$\mathcal { L } ( t _ { j } ) = \left[ t _ { j } , j _ { \mathrm { s e q } } , V _ { j } , \mathcal { T } _ { \mathrm { l o c a l } } , I , A _ { j } ^ { s } , F _ { v } ( j ) , \mathcal { U } _ { \mathrm { s t e p } } \right] ^ { \top }$$

慢推理模块利用LLM对这些记忆进行反思，通过思维链提示模板 $\mathcal { P } ( \mathcal { X } ) = \mathcal { P } _ { \mathrm { i n t r o } } + \mathcal { P } _ { \mathrm { c t x } } ( \mathcal { X } ) + \mathcal { P } _ { \mathrm { t a s k s } } + \mathcal { P } _ { \mathrm { o u t p u t } }$ 引导LLM提取结构化经验。每条经验被编码为六维向量：

$$\mathcal { E } = \left[ S _ { t } , C _ { s } , R _ { s } , T _ { n } , \eta _ { s } , f \right] ^ { \top }$$

分别对应场景类型、空间上下文、空间规则、导航策略、历史成功率和出现频率。

在推理阶段，经验库中检索到的相关经验通过多头注意力与快推理的视觉特征进行融合：

$$F _ { \mathrm { a t t } } , \omega = \mathbf { M } \mathbf { u } \mathbf { l } \mathbf { t } \mathbf { i } \mathbf { H } \mathbf { e } \mathbf { a } \mathbf { d } \mathbf { A } \mathbf { t } \mathbf { t } \mathbf { n } ( Q = F _ { v } , K = F _ { e } ^ { \mathrm { e x p } } , V = F _ { e } ^ { \mathrm { e x p } } )$$

$$F _ { \mathrm { f u s e d } } = \sigma \left( W _ { \mathrm { f u s i o n } } \cdot [ F _ { v } ; F _ { \mathrm { a t t } } ] + b _ { \mathrm { f u s i o n } } \right)$$

融合后的特征 $F_{\mathrm{fused}}$ 输入策略网络，输出经验增强的导航动作 $Y _ { \mathrm { e n h a n c e d } } = \pi ( F _ { \mathrm { f u s e d } } , I )$。

### 4. 创新点的证据强度

- **快慢交互推理的有效性**获得消融实验强支撑：仅添加快慢推理框架（FSR）即可在所有指令类型上提升性能，与指令风格转换（ISC）结合后在 Test-N-Scene 上达到最优 SR 50.4（Table 4）。
- **经验库容量的最优区间**在 50 到 100 之间，过小导致经验不足，过大引入冗余（Table 5），验证了经验积累机制的设计合理性。
- **案例研究**提供了直观的因果证据：经过慢推理经验增强后，导航时间减少 46.7%，导航误差降低 80%（Section 3.3）。

### 5. 已知局限

经验库容量 $K$ 目前需根据场景复杂度手工调整，缺乏自适应机制。慢推理依赖大语言模型，在资源受限的实时部署场景中存在计算开销和延迟挑战。指令风格转换的质量可能受LLM能力限制，对极端口语化指令的转换稳定性有待验证。

slow4fast-VLN 框架的核心设计动机源于人类双系统认知理论：系统1（快思考）负责实时、直觉式的决策，系统2（慢思考）则在事后对经验进行深度反思与抽象。现有视觉-语言导航方法在开放世界中泛化能力不足的根本原因，正是缺乏对这种快慢认知过程的显式建模，导致在分布外场景下推理路径不稳定。为此，slow4fast-VLN 构建了一个动态交互式快慢推理框架，其数学形式定义为：

$$\mathcal { F } = \langle \pi , R , M , A \rangle$$

其中 $\pi$ 为快推理策略网络，$R$ 为反思函数，$M$ 为经验提取与存储模块，$A$ 为赋能函数。框架的迭代过程遵循以下闭环：

$$L _ { k } = \pi ( I _ { k } , E n v ) , \quad R _ { k } = R ( L _ { k } ) , \mathcal { E } _ { k } = M ( R _ { k } ) , \quad \pi _ { k + 1 } = A ( \pi _ { k } , \mathcal { E } _ { k } )$$

在每个导航回合 $k$ 中，策略网络 $\pi$ 根据指令 $I_k$ 与环境交互生成历史记忆 $L_k$；反思函数 $R$ 对这些记忆进行深度分析，提取结构化经验集 $\mathcal{E}_k$；赋能函数 $A$ 将经验反馈给策略网络，使其在后续回合中获得更强的泛化能力。这一闭环机制使得快推理在遇到复杂场景时，能够检索并利用慢推理积累的通用经验，而无需每次都重新调用慢推理过程。

### 快推理模块

快推理模块采用基于 **DUET** 架构的端到端策略网络，接收实时视觉观察、导航指令和历史拓扑地图作为输入，直接输出导航动作（如前进、转弯、停止）。在每一步执行过程中，策略网络同步构建历史记忆并存入历史仓库（History Repository），每条历史数据包含时间戳、步数序号、当前视点、局部拓扑图、指令文本、执行动作、视觉描述以及步进度量：

$$\mathcal { L } ( t _ { j } ) = \left[ t _ { j } , j _ { \mathrm { s e q } } , V _ { j } , \mathcal { T } _ { \mathrm { l o c a l } } , I , A _ { j } ^ { s } , F _ { v } ( j ) , \mathcal { U } _ { \mathrm { s t e p } } \right] ^ { \top }$$

这些历史数据构成了慢推理模块进行反思的原始素材。

### 慢推理模块与经验库

慢推理模块利用大语言模型对历史仓库中的导航轨迹进行反思。通过精心设计的链式思考提示模板 $\mathcal{P}(\mathcal{X})$，引导 LLM 从导航数据中提取结构化经验。提示模板由角色定义、上下文填充、任务分解和输出格式约束四部分组成：

$$\mathcal { P } ( \mathcal { X } ) = \mathcal { P } _ { \mathrm { i n t r o } } + \mathcal { P } _ { \mathrm { c t x } } ( \mathcal { X } ) + \mathcal { P } _ { \mathrm { t a s k s } } + \mathcal { P } _ { \mathrm { o u t p u t } }$$

LLM 根据提示模板生成的经验映射为：

$$\mathcal { E } = \mathcal { F } _ { \mathrm { L L M } } ( \mathcal { P } ( \mathcal { X } ) )$$

每条结构化经验 $\mathcal{E}$ 包含六个维度：场景类型 $S_t$、空间上下文 $C_s$、空间规则 $R_s$、导航策略 $T_n$、历史成功率 $\eta_s$ 和出现频率 $f$：

$$\mathcal { E } = \left[ S _ { t } , C _ { s } , R _ { s } , T _ { n } , \eta _ { s } , f \right] ^ { \top }$$

这些经验被存入经验库（Experience Library），形成一个不断增长的通用知识库。消融实验表明，经验库的最优容量 $K$ 在 50 到 100 之间：对于住宅场景的基本指令，$K=50$ 效果最佳；对于非住宅场景指令，$K=100$ 表现最优。容量过小会导致经验不足，过大则会引入冗余信息干扰决策。

### 经验检索与融合

在导航推理阶段，慢推理模块根据当前场景从经验库中检索相关经验，将其编码为特定向量。随后通过多头注意力机制，将快推理网络的视觉特征 $F_v$ 与扩展后的经验特征 $F_e^{exp}$ 进行融合：

$$F _ { \mathrm { a t t } } , \omega = \mathbf { M u l t i H e a d A t t n } ( Q = F _ { v } , K = F _ { e } ^ { \mathrm { e x p } } , V = F _ { e } ^ { \mathrm { e x p } } )$$

融合后的特征通过线性投影和激活函数生成增强特征：

$$F _ { \mathrm { f u s e d } } = \sigma \left( W _ { \mathrm { f u s i o n } } \cdot [ F _ { v } ; F _ { \mathrm { a t t } } ] + b _ { \mathrm { f u s i o n } } \right)$$

最终，策略网络基于融合特征和导航指令输出经验增强的动作决策：

$$Y _ { \mathrm { e n h a n c e d } } = \pi ( F _ { \mathrm { f u s e d } } , I )$$

### 指令风格转换

为应对开放环境中指令风格的多样性（基本指令、场景指令、用户指令），框架引入指令风格转换模块（Instruction Style Conversion）。该模块利用 LLM 链式思考提示工程，将场景风格和用户风格的指令动态转换为统一的基本风格指令，在保留核心导航语义的同时消除格式差异。消融实验证实，该模块对场景风格指令的提升尤为显著，与快慢推理框架结合后在 Test-N-Scene 上达到最优 SR 50.4。

![[assets/figures/papers/paper_list_l2424_https_arxiv_org_abs_2601_09111/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method. The policy network processes real-time input, executes actions, and stores historical memory. The slow-reasoning network reflects on these memories to generate generalized experiences, which are then stored. These experiences guide the fast-reasoning network, providing strategic insights when faced with complex scenarios*

### 2.1 快慢交互推理框架形式化

slow4fast-VLN 的核心是将导航任务建模为一个动态交互式的快慢推理系统。框架的形式化定义为：

$$\mathcal{F} = \langle \pi, R, M, A \rangle$$

其中 $\pi$ 为快推理策略网络，$R$ 为反思函数，$M$ 为经验提取与存储模块，$A$ 为赋能函数。每个 episode $k$ 的迭代过程为：

$$L_k = \pi(I_k, Env), \quad R_k = R(L_k), \quad \mathcal{E}_k = M(R_k), \quad \pi_{k+1} = A(\pi_k, \mathcal{E}_k)$$

该过程的因果机制为：策略网络 $\pi$ 在当前指令 $I_k$ 和环境的交互中产生历史记忆 $L_k$；慢推理模块对 $L_k$ 进行反思得到 $R_k$；经验提取模块将反思结果结构化，生成经验集 $\mathcal{E}_k$；赋能函数 $A$ 将这些经验反馈给策略网络，更新为 $\pi_{k+1}$。这一闭环使得快推理在后续导航中能够利用慢推理积累的通用经验，而无需每次重新调用慢推理。

### 2.2 快推理模块与历史记忆构建

快推理模块采用 **DUET** 架构（Chen et al., CVPR 2022）作为端到端策略网络，接收实时视觉观察、导航指令和历史拓扑地图，直接输出导航动作。同时，该模块在每个时间步 $t_j$ 将执行记录存储于历史仓库，构建结构化记忆：

$$\mathcal{L}(t_j) = \left[ t_j, j_{\mathrm{seq}}, V_j, \mathcal{T}_{\mathrm{local}}, I, A_j^s, F_v(j), \mathcal{U}_{\mathrm{step}} \right]^{\top}$$

各维度的含义：
- $t_j$：时间戳；
- $j_{\mathrm{seq}}$：当前步数序号；
- $V_j$：当前视点；
- $\mathcal{T}_{\mathrm{local}}$：局部拓扑结构；
- $I$：导航指令；
- $A_j^s$：执行的导航动作；
- $F_v(j)$：视觉特征描述；
- $\mathcal{U}_{\mathrm{step}}$：步进度量（如距目标的距离变化）。

这一记忆结构是慢推理模块进行反思的原始数据来源。

### 2.3 慢推理模块与经验提取

慢推理模块的核心功能是利用大语言模型（LLM）对历史记忆进行反思，提取可复用的结构化经验。经验向量定义为：

$$\mathcal{E} = \left[ S_t, C_s, R_s, T_n, \eta_s, f \right]^{\top}$$

各维度含义：
- $S_t$：场景类型；
- $C_s$：空间上下文（如走廊、楼梯口、房间连接关系）；
- $R_s$：空间规则（如“经过楼梯后通常需要转弯”）；
- $T_n$：导航策略（如“先直行再左转”）；
- $\eta_s$：历史成功率；
- $f$：经验出现频率。

为引导 LLM 进行有效的反思，论文设计了链式思维（CoT）提示模板：

$$\mathcal{P}(\mathcal{X}) = \mathcal{P}_{\mathrm{intro}} + \mathcal{P}_{\mathrm{ctx}}(\mathcal{X}) + \mathcal{P}_{\mathrm{tasks}} + \mathcal{P}_{\mathrm{output}}$$

其中 $\mathcal{P}_{\mathrm{intro}}$ 定义 LLM 的角色，$\mathcal{P}_{\mathrm{ctx}}(\mathcal{X})$ 填充当前导航上下文，$\mathcal{P}_{\mathrm{tasks}}$ 分解反思任务，$\mathcal{P}_{\mathrm{output}}$ 约束输出格式。LLM 将提示映射为结构化经验：

$$\mathcal{E} = \mathcal{F}_{\mathrm{LLM}}(\mathcal{P}(\mathcal{X}))$$

### 2.4 经验检索与注意力融合

快慢交互的关键在于将慢推理积累的经验动态注入快推理的决策过程。具体而言，慢推理模块从经验库中检索与当前场景相关的经验，编码为向量 $F_e^{\mathrm{exp}}$，然后通过多头注意力机制与快推理网络的视觉特征 $F_v$ 进行融合：

$$F_{\mathrm{att}}, \omega = \mathbf{MultiHeadAttn}(Q = F_v, K = F_e^{\mathrm{exp}}, V = F_e^{\mathrm{exp}})$$

其中 $F_{\mathrm{att}}$ 为注意力加权后的经验特征，$\omega$ 为注意力权重。随后，将原始视觉特征与加权经验特征拼接并通过线性层融合：

$$F_{\mathrm{fused}} = \sigma\left(W_{\mathrm{fusion}} \cdot [F_v; F_{\mathrm{att}}] + b_{\mathrm{fusion}}\right)$$

其中 $\sigma$ 为激活函数，$W_{\mathrm{fusion}}$ 和 $b_{\mathrm{fusion}}$ 为可学习参数。融合后的特征 $F_{\mathrm{fused}}$ 替代原始视觉特征输入策略网络，产生经验增强的导航决策：

$$Y_{\mathrm{enhanced}} = \pi(F_{\mathrm{fused}}, I)$$

这一设计的核心因果机制在于：注意力权重 $\omega$ 使得快推理能够根据当前视觉输入自适应地选择最相关的经验，从而在不增加推理延迟的前提下提升泛化能力。

### 2.5 指令风格转换模块

为处理 GSA-VLN 中多样化的指令风格（Basic、Scene、User），论文引入指令风格转换（ISC）模块。该模块通过 LLM 的 CoT 提示工程，将 Scene 风格和 User 风格的指令动态转换为统一的 Basic 风格指令，同时保留核心导航语义。转换过程设置置信度阈值，仅当转换置信度超过阈值时才采用转换后的指令，否则保留原始指令。这一模块与快慢推理框架正交，可独立或联合使用。

## 实验与关键发现

### 主实验结果

论文在 GSA-R2R 基准上评估了 slow4fast-VLN 框架在三种指令风格下的导航性能：基本指令（Basic）、用户风格指令（User）和场景风格指令（Scene）。该基准的核心挑战在于训练集仅包含住宅场景，而测试集扩展到购物中心、办公室、影院等非住宅场景，同时引入多样化的指令风格，旨在全面检验模型的场景泛化能力。

#### 基本指令下的性能（Table 1）

![[assets/figures/papers/paper_list_l2424_https_arxiv_org_abs_2601_09111/figures/003_Table_1.jpg]]
*Table 1: Comparison of different adaptation methods in GSA-R2R with basic instructions*

在基本指令条件下，slow4fast-VLN 在测试集的两个子集上均取得了最优成功率（SR）：

- **Test-R-Basic（住宅场景）**：SR 达到 **70.8**，SPL 为 65.0，NE 为 2.9，相比基线方法 **GR-DUET**（Hong et al., arXiv 2025）提升约 **1.5%**。
- **Test-N-Basic（非住宅场景）**：SR 达到 **58.4**，SPL 为 52.9，NE 为 4.2，相比 GR-DUET 提升约 **2.2%**。

值得注意的是，非住宅场景下的提升幅度大于住宅场景，这表明快慢交互推理机制对分布外（OOD）场景的适应性更强——慢推理模块积累的通用经验在陌生环境中发挥了更显著的补偿作用。

#### 用户指令下的性能（Table 2）

![[assets/figures/papers/paper_list_l2424_https_arxiv_org_abs_2601_09111/figures/004_Table_2.jpg]]
*Table 2: Comparison of different adaptation methods in GSA-R2R with User instructions*

用户风格指令引入了口语化表达和个性化描述，对模型的指令理解能力提出更高要求。slow4fast-VLN 在 Test-R-User 上取得 **70.8 ± 0.1** 的 SR（加粗最优），保持了与基本指令相当的性能水平。这得益于指令风格转换（Instruction Style Conversion, ISC）模块将多样化的用户指令统一转换为基本风格指令，降低了策略网络的理解负担。

#### 场景指令下的性能（Table 3）

场景风格指令是最具挑战性的设置，指令中融入了场景特有的空间语义（如“经过电影院海报墙后左转”）。slow4fast-VLN 在 Test-N-Scene 上取得 **50.7 ± 0.1** 的 SR，相比 GR-DUET 的 48.1 ± 0.1 提升 **2.6 个百分点**，相对提升幅度达到 5.4%。这一结果验证了快慢推理框架的核心假设：当面对复杂场景时，慢推理模块反思提取的空间规则和导航策略能够有效指导快推理网络做出更准确的决策。

### 消融实验

#### 模块贡献分析（Table 4）

![[assets/figures/papers/paper_list_l2424_https_arxiv_org_abs_2601_09111/figures/007_Table_4.jpg]]
*Table 4: Analysis of ablation experiments on each module*

为验证各模块的独立贡献，论文进行了系统的消融实验：

- **仅添加快慢推理框架（FSR）**：在所有指令类型上均观察到性能提升，表明快慢交互推理机制本身具有普适的增益效果。
- **仅添加指令风格转换（ISC）**：对场景风格指令提升明显，但对基本指令影响较小——这符合预期，因为 ISC 主要解决指令风格的异质性问题，而基本指令本身已具备统一格式。
- **FSR + ISC 组合**：在 Test-N-Scene 上达到最佳 SR **50.4 ± 0.1**，验证了两个模块的协同效应：ISC 负责指令层面的归一化，FSR 负责推理层面的经验增强，二者在互补维度上共同提升了泛化能力。

#### 经验库容量分析（Table 5）

![[assets/figures/papers/paper_list_l2424_https_arxiv_org_abs_2601_09111/figures/008_Table_5.jpg]]
*Table 5: Analysis of the impact of K*

经验库容量 K 是快慢推理框架的关键超参数。实验表明：

- **最优 K 范围**：在 50 到 100 之间，取决于场景复杂度。
- **场景依赖性**：Test-R-Basic（住宅基本指令）在 K=50 时最优；Test-N-Basic 和 Test-N-Scene（非住宅场景）在 K=100 时最优。这表明更复杂的场景需要更大容量的经验库来覆盖多样化的空间模式。
- **过小与过大的影响**：K 过小导致经验覆盖不足，无法提供有效指导；K 过大则引入冗余经验，可能造成注意力机制中的噪声干扰。

### 定性分析

#### 轨迹对比（Figure 3）

![[assets/figures/papers/paper_list_l2424_https_arxiv_org_abs_2601_09111/figures/006_Figure_3.jpg]]
*Figure 3: Predicted trajectories of GR-DUET (left) and our method (right). A check mark (✓) indicates the destination; A five-pointed star (⋆) marks the final position reached by the agent*

论文提供了 GR-DUET 与 slow4fast-VLN 的预测轨迹对比。在非住宅场景的复杂指令下，GR-DUET 的轨迹出现明显偏离，未能到达目标位置；而 slow4fast-VLN 借助慢推理经验库中的空间规则，成功规划出更准确的路径并抵达目标。

#### 案例研究（Figure 4）

在一个具体案例中，论文对比了仅使用快推理与启用快慢交互推理的导航表现：

- **导航时间**：从 15 秒降至 8 秒，减少 **46.7%**。
- **导航误差**：从 1.5 米降至 0.3 米，降低 **80%**。

该案例直观展示了慢推理经验对快推理决策的增强效果：经验库中存储的“靠近门口地板通风口”等空间上下文信息，使智能体在类似场景中能快速定位目标，避免无效探索。

### 失败模式与局限性

尽管 slow4fast-VLN 在 GSA-R2R 基准上取得了显著提升，但仍存在以下局限：

1. **经验库容量的手工调整**：K 值需要根据场景复杂度预先设定，缺乏自适应机制。在动态变化的开放环境中，固定容量可能导致经验覆盖不足或冗余。
2. **慢推理的计算开销**：慢推理模块依赖大语言模型（LLM）进行反思和经验提取，在资源受限的实时部署场景中可能引入不可忽视的延迟。
3. **指令风格转换的稳定性**：ISC 模块的效果受 LLM 能力限制，对于极端口语化或罕见的指令风格，转换质量可能不稳定，进而影响下游导航性能。
4. **场景覆盖的边界**：当前经验库的经验来源于训练集中的住宅场景，对于与训练分布差异极大的非住宅场景（如工厂、医院），经验迁移的有效性尚待验证。

### 公平性说明

论文中未明确讨论公平性相关考量，如不同场景类型或指令风格下的性能均衡性分析。建议在后续研究中补充跨场景、跨指令类型的细粒度公平性评估。

## 定位与知识库关联

### 1. 基线关系与差异化贡献

本工作 slow4fast-VLN 的核心基线为 **GR-DUET**（Hong et al., arXiv 2025），后者是近期面向 GSA-VLN 场景适应任务的代表性方法，专注于视觉特征适应。slow4fast-VLN 在此基础上进行了三个关键维度的差异化拓展：

**推理框架的根本性重构。** GR-DUET 采用单一推理网络进行顺序决策，而 slow4fast-VLN 构建了动态交互式快慢推理框架 $\mathcal{F} = \langle \pi, R, M, A \rangle$。该框架将导航过程建模为迭代优化循环：快推理策略网络 $\pi$ 在每个 episode $k$ 中生成历史记忆 $L_k$，慢推理通过反思函数 $R$ 和提取模块 $M$ 生成结构化经验集 $\mathcal{E}_k$，再通过赋能函数 $A$ 更新策略 $\pi_{k+1}$（见 Eq. 1-2）。这种设计将单次推理扩展为“执行-反思-增强”的闭环，从根本上改变了导航智能体的学习范式。

**经验积累与泛化机制。** GR-DUET 缺乏经验积累机制，每次导航独立进行。slow4fast-VLN 引入了基于 LLM 的慢推理模块，通过 CoT 提示模板 $\mathcal{P}(\mathcal{X})$ 从历史轨迹中提取结构化经验向量 $\mathcal{E} = [S_t, C_s, R_s, T_n, \eta_s, f]^\top$，包含场景类型、空间上下文、空间规则、导航策略、历史成功率与出现频率六个维度（Eq. 4-6）。这些经验被存储于经验库中，并在推理时通过多头注意力与快推理的视觉特征 $F_v$ 进行融合，生成经验增强的融合特征 $F_{\text{fused}}$（Eq. 7-8）。这一机制使得智能体能够在遇到类似场景时直接利用历史经验，无需重新调用慢推理。

**指令风格统一化处理。** GR-DUET 直接使用原始多样指令，而 slow4fast-VLN 通过 LLM 驱动的指令风格转换（ISC）模块，将场景风格和用户风格指令动态转换为统一的基本风格指令，为导航模型提供格式一致的输入。消融实验证实，ISC 对场景风格指令提升尤为显著（Table 4）。

### 2. 适用边界

**正向适用条件：**
- **结构化室内环境**：框架在 Matterport3D 场景中验证有效，适用于住宅、商场、办公室、影院等具有明确空间拓扑的室内场景。
- **离散导航动作空间**：快推理基于 DUET 架构，假设导航图（navigation graph）已知，适用于离散视点间的导航任务。
- **指令多样性场景**：ISC 模块使得框架能够处理基本、场景、用户三种风格的指令，适用于开放词汇的指令理解场景。
- **批量离线经验积累**：慢推理在 episode 完成后进行反思，适用于允许离线经验更新的场景。

**不适用或需适配的场景：**
- **连续控制空间**：框架未在连续动作空间的导航任务（如 Habitat 平台的 point-goal 导航）上验证。
- **实时严格低延迟场景**：慢推理依赖 LLM 调用，引入额外计算开销，在需要毫秒级响应的实时部署中存在挑战。
- **极端动态环境**：经验库中的空间规则和导航策略基于静态场景假设，对于频繁变化的动态环境（如人流密集的商场）可能失效。
- **跨语言指令**：ISC 模块仅在英文指令上验证，跨语言泛化能力未知。

### 3. 局限与开放问题

**已识别的局限：**

1. **经验库容量依赖手工调参**：经验库最优容量 $K$ 在 50 到 100 之间，且依赖于场景复杂度——$K=50$ 对住宅基本指令最优，$K=100$ 对非住宅场景指令最优（Table 5）。目前缺乏自动适应机制，过小导致经验不足，过大引入冗余并可能降低性能。

2. **慢推理的计算开销**：慢推理依赖 LLM 进行 CoT 反思，在资源受限的边缘设备上部署存在挑战。虽然案例研究表明经验增强后导航时间减少 46.7%，但慢推理本身的推理成本未被量化讨论。

3. **指令风格转换的稳定性**：ISC 模块的效果受 LLM 能力限制，对于极端口语化或少见的指令风格，转换质量可能不稳定。论文未讨论转换失败时的回退策略。

4. **单模态经验表示**：经验库仅存储文本形式的结构化经验，未充分利用视觉模态的丰富信息（如场景图像特征），可能限制了经验表达的细粒度。

**开放问题：**

- **自适应经验库管理**：如何实现经验库容量的自适应调整，根据场景复杂度和任务分布动态平衡存储开销与泛化性能？
- **经验的可解释符号化**：能否将慢推理提取的经验抽象为可解释的符号规则（如空间逻辑表达式），以进一步加速推理并提升可解释性？
- **跨环境迁移**：在更复杂、动态的真实世界环境（如室外导航、多层建筑）中，快慢交互推理的有效性如何？经验库能否跨环境迁移？
- **ISC 置信度自适应**：指令风格转换的置信度阈值如何自适应确定，以在转换质量和效率之间取得平衡？
- **在线慢推理**：当前慢推理在 episode 完成后离线执行，能否实现 episode 内的在线反思，以应对需要即时纠错的场景？

### 4. 知识库定位

slow4fast-VLN 处于**视觉-语言导航（VLN）** 与**认知启发的具身智能**的交叉点。其核心贡献在于将人类双系统认知理论（Kahneman, 2011）显式地建模为可计算的快慢交互推理框架，区别于以下几条技术路线：

- **端到端 VLN 方法**（如 DUET, Chen et al., ECCV 2022）：仅依赖单一推理网络，缺乏显式的反思与经验积累机制。
- **基于 LLM 的规划方法**（如 NavGPT, Zhou et al., 2023）：将 LLM 直接作为规划器，但未构建结构化经验库实现跨 episode 的知识积累。
- **元学习/持续学习 VLN 方法**：关注跨任务的快速适应，但通常不区分快慢推理的时间尺度。

slow4fast-VLN 的经验库机制与检索增强生成（RAG）范式存在概念上的亲缘性，但将其应用于具身导航的动作空间，通过注意力融合实现视觉特征层面的经验注入，而非文本生成层面的知识增强。这一设计为构建具有持续学习能力的通用导航智能体提供了新的技术路径。

## 原文 PDF

![[paperPDFs/CVPR_2026/Towards_Open_Environments_and_Instructions_General_Vision_Language_Navigation_via_Fast_Slow_Interactive_Reasoning.pdf]]
