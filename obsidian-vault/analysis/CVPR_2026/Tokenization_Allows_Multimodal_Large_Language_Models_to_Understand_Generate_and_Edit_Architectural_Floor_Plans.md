---
title: Tokenization Allows Multimodal Large Language Models to Understand, Generate and Edit Architectural Floor Plans
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Tokenization_Allows_Multimodal_Large_Language_Models_to_Understand_Generate_and_Edit_Architectural_Floor_Plans.pdf
project_link: https://housemind.github.io/
code_link:
aliases:
  - TAMLLMUGEAFP
tags:
  - CVPR_2026
  - topic/other_unclear
  - topic/other_unclear/general
core_operator: 引入离散的房间实例标记化（VQ-VAE），将几何和语义信息编码为统一的结构化令牌序列，使LLM能够在同一自回归框架中执行空间推理。
primary_logic: 将建筑平面图分解为轮廓和房间实例，并通过分层矢量量化转化为离散空间令牌；将令牌与语义标签交织，形成结构化序列，然后利用多模态对齐和指令微调，使LLM联合建模文本、几何和拓扑关系，实现多任务统一。
claims:
  - HouseMind采用VQ‑VAE将布局离散化为房间实例令牌，并利用LLM进行多模态推理。
  - 通过结构化标记化，平面图被表示为交织的令牌序列，融合了几何和语义信息。
  - HouseMind在理解、生成和编辑任务上优于扩散模型和现有LLM，大幅提升结构一致性并降低FID。
  - 三阶段训练管道（嵌入初始化、多模态预训练、指令调优）对于实现稳健的多模态对齐至关重要。
---

# Tokenization Allows Multimodal Large Language Models to Understand, Generate and Edit Architectural Floor Plans

> [!tip] 核心洞察
> 将建筑平面图分解为轮廓和房间实例，并通过分层矢量量化转化为离散空间令牌；将令牌与语义标签交织，形成结构化序列，然后利用多模态对齐和指令微调，使LLM联合建模文本、几何和拓扑关系，实现多任务统一。

| 字段      | 内容                                                                                                              |
| ------- | --------------------------------------------------------------------------------------------------------------- |
| 中文题名    | 通过标记化使多模态大语言模型理解、生成和编辑建筑平面图                                                                                     |
| 英文题名    | Tokenization Allows Multimodal Large Language Models to Understand, Generate and Edit Architectural Floor Plans |
| 会议/期刊   | CVPR 2026                                                                                                       |
| Links   | [paper](https://arxiv.org/abs/2603.11640) · [Project](https://housemind.github.io/)                             |
| Topic   | #topic/other_unclear #topic/other_unclear/general                                                               |
| Method  | HouseMind                                                                                                       |
| Dataset | RPLAN                                                                                                           |

> [!tip] 效果简介
> - RPLAN (理解任务) 上，LocAcc (房间定位准确度) 0.969 vs 0.225 (LLaVA-v1.6-Mistral-7B-HF) (+0.744)。
> - RPLAN (生成任务) 上，Micro IoU 0.709 vs 0.589 (ChatHouseDiffusion) (+0.120)；FID ↓ 1.91 vs 11.3 (ChatHouseDiffusion) (-9.39)。
> - RPLAN (编辑任务) 上，△IoU (编辑精度) 0.608 vs 0.053 (FLUX.1-Kontext-dev) (+0.555)。

## 概述

建筑平面图设计长期面临一个核心瓶颈：现有方法将布局合成视为纯视觉过程，缺乏对房间实例级别的显式推理，导致全局空间连贯性差、可控制性弱，且理解、生成与编辑任务被割裂在不同模型中处理。**HouseMind** 针对这一瓶颈，提出将建筑平面图分解为轮廓与房间实例，并通过分层矢量量化（VQ-VAE）将连续几何转化为离散空间令牌——一种“空间语言”。这些令牌与语义标签交织为结构化序列，使多模态大语言模型（LLM）能够在统一的**自回归框架**中联合建模文本、几何与拓扑关系，从而以单一架构执行理解、生成与编辑三项任务。

其核心因果机制在于**离散房间实例标记化**：通过为轮廓和每个房间分别建立码本，将空间推理从连续像素域迁移到离散令牌域，LLM 得以捕获关系性与组合性规律，而非记忆特定布局实例。三阶段训练管道（嵌入初始化、多模态预训练、指令调优）确保了几何令牌与语言令牌的跨模态对齐，是模型获得稳健空间推理能力的关键。

实验表明，HouseMind 在 RPLAN 数据集上全面超越现有方法：理解任务中房间定位准确度（LocAcc）达到 **0.969**，较 LLaVA-v1.6-Mistral-7B-HF 提升 0.744；生成任务的 Micro IoU 达到 **0.709**，FID 降至 **1.91**（ChatHouseDiffusion 为 11.3），降幅达 9.39；编辑任务的 △IoU 达到 **0.608**，而 FLUX.1-Kontext-dev 仅 0.053。同时，图级指标（节点 F1 0.994、边重叠度 0.880）验证了其在结构一致性上的显著优势。消融实验进一步证实，三阶段完整训练获得最低验证损失，结构校正步骤可降低图编辑距离（GED 1.10→1.03）并提升边重叠度，而码本大小在 256–1024 范围内对生成指标影响甚微，表明 VQ-VAE 并非性能瓶颈。

**方法定位**：HouseMind 属于“离散标记化 + 自回归 LLM”范式，区别于扩散模型（如 ChatHouseDiffusion）和纯视觉多模态模型（如 LLaVA、Qwen-VL 系列）。它将平面图生成重新定义为序列建模问题，以房间实例为最小推理单元，实现了细粒度的文本控制与精确的空间编辑。然而，当前编辑能力仍限于添加/删除房间等简单操作，尚未建模门窗等功能构件，生成结果也未对齐人类设计偏好与美学约束——这些构成了后续研究的主要开放方向。

## 背景与动机

建筑平面图设计是建筑信息建模（BIM）与空间规划的核心环节，直接影响居住舒适度、能源效率与施工可行性。传统上，平面图设计依赖专业建筑师的手工绘制或规则驱动的生成系统，前者耗时且难以批量探索，后者则受限于预定义模板，缺乏对复杂空间语义的灵活建模能力。

近年来，深度学习驱动的布局生成方法取得了显著进展。主流范式可分为两类：**基于图像翻译的方法**将平面图视为像素级生成任务，利用卷积网络或扩散模型从边界轮廓直接合成室内布局；**基于图的方法**则将房间实例建模为图节点，通过图神经网络预测邻接关系与空间配置。然而，这两类方法均存在根本性局限：

1. **缺乏实例级显式推理**：现有方法大多将布局合成视为纯视觉过程，在连续像素或坐标空间中操作，难以对“房间”这一核心语义单元进行独立建模与可控操纵。扩散模型（如 **ChatHouseDiffusion**）虽能生成视觉逼真的布局，但其潜在空间缺乏对房间身份、几何属性与拓扑关系的显式表征，导致生成结果的空间连贯性差、可控制性弱。

2. **任务割裂**：理解（从平面图提取空间语义）、生成（从文本描述合成布局）与编辑（按指令修改现有布局）通常由独立模型分别处理，缺乏统一框架。例如，**LLaVA-v1.6-Mistral-7B-HF** 等多模态大语言模型（MLLM）可直接接受平面图图像作为输入进行视觉问答，但其输出仅为自然语言描述，无法生成或修改可操作的布局几何；**Tell2Design** 等文本到布局模型则专注于生成，不具备理解与编辑能力。这种割裂阻碍了人机协同设计流程的闭环。

3. **可控性粒度粗**：现有生成模型大多以全局布局为输出单元，缺乏房间实例级别的细粒度控制。当用户需要“将厨房移至东南角”或“增加一间卧室并调整相邻关系”时，扩散模型或图像翻译模型难以精确定位修改区域，往往导致非目标区域的意外变化。

上述瓶颈的根本原因在于：**平面图的结构化本质（由语义明确的房间实例及其空间关系构成）与现有模型所依赖的连续表示之间存在语义鸿沟**。弥合这一鸿沟需要一种能够同时编码几何、语义与拓扑信息，并能与自然语言指令无缝对接的统一表示形式。

**HouseMind** 的提出正是为了应对这一挑战。其核心动机是：将平面图从连续像素空间“翻译”为大语言模型（LLM）可理解的离散令牌序列，从而将理解、生成与编辑统一为同一自回归序列建模问题。通过引入分层矢量量化（VQ‑VAE）将建筑轮廓与房间实例分别编码为结构化空间令牌，并与语义标签交织形成统一序列，HouseMind 使 LLM 能够在文本、几何与拓扑的联合空间中执行多模态空间推理，实现从“看、说、画、改”的全链路能力。

## 核心创新

### 从连续像素到离散房间实例令牌：空间表示的范式转换

现有建筑平面图生成方法——无论是基于扩散模型的**ChatHouseDiffusion**，还是基于LLM的**FloorPlanLLaMA**——均将布局合成视为连续像素空间或全局图像序列上的视觉生成过程。这种范式存在一个根本性瓶颈：模型缺乏对房间实例级别的显式推理能力，导致全局空间连贯性差、可控制性弱，且理解、生成与编辑任务必须由独立模型分别处理。

HouseMind的核心创新在于引入**离散房间实例标记化**（discrete room-instance tokenization），将空间推理问题彻底转化为结构化序列建模问题。具体而言，该方法将平面图分解为建筑轮廓 $x_o$ 与 $N$ 个房间实例 $\{x_{r_i}\}_{i=1}^N$ 两个层次，并通过分层矢量量化变分自编码器（VQ-VAE）将几何信息编码为离散令牌序列：

$$z_o = E_o(x_o), \qquad z_{r_i} = E_r(x_{r_i}, x_o)$$

其中房间编码器 $E_r$ 以轮廓为条件，使每个房间令牌天然携带其相对于全局边界的空间上下文。这种设计的关键洞察在于：**将连续几何转化为离散令牌后，平面图的空间语义——房间类型、位置、大小、邻接关系——被统一编码为交织的令牌序列**：

$$Z = [z_o, \ell_{r_1}, z_{r_1}, ..., \ell_{r_N}, z_{r_N}]$$

语义标签令牌 $\ell_{r_i}$ 与几何令牌 $z_{r_i}$ 的交织排列，使LLM能够在自回归框架中同时建模文本、几何和拓扑关系，从而在单一架构内实现理解、生成与编辑三项任务的统一。

### 与基线方法的关键差异

| 维度 | 现有方法 | HouseMind |
|------|----------|-----------|
| **空间表示** | 连续像素/坐标空间，全局图像序列 | 离散房间实例令牌，通过分层VQ-VAE将轮廓和房间分别编码 |
| **任务统一性** | 不同任务使用独立模型 | 统一自回归序列模型，同一架构执行三项任务 |
| **可控性粒度** | 全局布局生成，缺乏房间级控制 | 房间实例级别的细粒度推理和文本控制，支持编辑时精确定位修改 |
| **训练流程** | 单阶段或直接训练 | 三阶段：嵌入初始化、多模态预训练、指令调优 |

这一范式转换带来的性能跃迁是决定性的。在生成任务上，HouseMind将FID从**ChatHouseDiffusion**的11.3降至1.91，Micro IoU提升超过10个百分点（0.589→0.709）；在编辑任务上，△IoU从**FLUX.1-Kontext-dev**的0.053跃升至0.608，提升了逾10倍。这些数据表明，离散房间实例令牌不仅是一种更紧凑的表示形式，更从根本上解决了连续生成方法中空间约束难以精确建模的核心难题。

### 三阶段训练管道：跨模态对齐的工程创新

将几何令牌与语言令牌统一输入LLM并非简单的拼接操作。HouseMind设计了**三阶段训练管道**以确保跨模态对齐的稳健性：

- **阶段一（嵌入初始化）**：建立几何令牌与语言令牌之间的跨模态兼容性，确保VQ-VAE输出的离散编码与LLM的嵌入空间在初始化层面即保持一致性。
- **阶段二（多模态预训练）**：在大规模平面图数据上对齐文本与空间表示，使LLM习得全局空间推理能力。
- **阶段三（指令调优）**：通过监督微调赋予模型任务感知的空间推理能力，使其能根据自然语言指令灵活切换理解、生成或编辑模式。

消融实验（Table 4）证实了该设计的必要性：完整三阶段管道获得最低验证损失（0.0830），移除阶段一或阶段二均导致损失上升。这表明，**嵌入初始化和多模态预训练并非可选的优化手段，而是实现稳健跨模态对齐的必要条件**。

## 整体框架

HouseMind 将建筑平面图的理解、生成与编辑统一为单一序列建模问题，其核心在于**层次化离散标记化**与**多模态对齐**两大设计，使轻量级 LLM 能够在同一自回归框架中执行空间推理。

### 平面图的结构化分解与标记化

框架首先将平面图 $x$ 分解为轮廓 $x_o$ 和 $N$ 个房间实例 $\{x_{r_i}\}_{i=1}^N$：

$$x = \{ x_{o}, \{ x_{r_i} \}_{i=1}^{N} \}$$

这一分解是后续所有任务的基础——轮廓定义全局边界约束，房间实例承载语义与几何细节。两个组件分别通过独立的 VQ‑VAE 编码器映射为离散令牌：

$$z_{o} = E_{o}(x_{o}), \qquad z_{r_i} = E_{r}(x_{r_i}, x_{o})$$

其中房间编码器 $E_r$ 以轮廓为条件，使每个房间令牌天然携带其与全局边界的空间关系。量化过程将编码器输出的每个特征向量映射到各自码本中距离最近的码字：

$$z_{j}^{(o)} = e_{k_j^\star}^{(o)}, \quad k_j^\star = \arg\min_k \big\| E_{o}(x_{o})_j - e_k^{(o)} \big\|_2$$

$$z_{i,j}^{(r)} = e_{k_{i,j}^\star}^{(r)}, \quad k_{i,j}^\star = \arg\min_k \big\| E_{r}(x_{r_i}, x_{o})_j - e_k^{(r)} \big\|_2$$

最终，轮廓令牌、语义标签令牌与房间令牌被交织为统一的结构化序列：

$$Z = [ z_{o}, \ell_{r_1}, z_{r_1}, ..., \ell_{r_N}, z_{r_N} ]$$

这一表示将连续布局几何转化为 LLM 可直接消费的离散序列，同时保留了房间实例的语义身份和空间拓扑。

### 三阶段训练管道

HouseMind 通过**三阶段多模态对齐与指令微调管道**（Figure 3）逐步弥合语言与几何之间的模态鸿沟：

![[assets/figures/papers/paper_list_l2347_https_arxiv_org_abs_2603_11640/figures/003_Figure_3.jpg]]
*Figure 3: Overall framework of HouseMind. The model is trained through a three-stage multimodal alignment and instruction tuning pipeline: (S1) Embedding Initialization establishes cross-modal compatibility between geometric and linguistic tokens; (S2) Multimodal Pre-training aligns text and spatial representations; and (S3) Instruction Tuning (SFT) enables task-aware spatial reasoning*

- **S1 嵌入初始化**：建立几何令牌与语言令牌之间的跨模态兼容性，确保令牌级表示的一致性初始化。
- **S2 多模态预训练**：在更大规模数据上对齐文本与空间表示，精炼全局空间推理能力。
- **S3 指令微调**：引入任务感知的指令数据，使模型能够根据自然语言提示执行理解、生成或编辑。

消融实验（Table 4）证实了三阶段的必要性：完整管道取得最低验证损失（0.0830），移除 S1 或 S2 均导致损失上升，表明嵌入初始化和多模态预训练缺一不可。

### 多任务统一推理

在推理阶段，HouseMind 根据任务类型采用不同的自回归生成策略。对于**生成任务**，模型以轮廓令牌 $z_o$ 和文本描述 $s$ 为条件，逐令牌预测布局序列：

$$p(Z \mid z_{o}, s) = \prod_t p(Z_t \mid Z_{<t}, z_{o}, s)$$

对于**编辑任务**，模型以源布局 $Z^{src}$ 和编辑指令 $s$ 为条件，仅修改受指令影响的令牌，保持未涉及区域的几何一致性：

$$p\big(Z^{tgt} \mid Z^{src}, s\big) = \prod_t p\big(Z_t^{tgt} \mid Z^{src}, Z_{<t}^{tgt}, s\big)$$

理解任务则通过相同的序列建模机制，将输入平面图的令牌序列映射为结构化 JSON 或文本描述。这种统一架构使同一 LLM 骨干（Qwen3-0.6B）能够在三项任务间共享空间推理能力，无需为每项任务设计独立模型。

### 关键模块协作关系

整体管道中，VQ‑VAE 标记化模块（Figure A.1）负责将视觉布局压缩为离散空间令牌，LLM 骨干负责序列建模与跨模态推理，三阶段训练管道则确保几何令牌与语言指令的有效对齐。结构校正后处理步骤（Table C.1）进一步改善生成结果的几何一致性，将图编辑距离（GED）从 1.10 降至 1.03。

### 补充图表

![[assets/figures/papers/paper_list_l2347_https_arxiv_org_abs_2603_11640/figures/002_Figure_2.jpg]]
*Figure 2: Understanding: given a prompt, an outline, and an existing floor plan, the model outputs a textual description, a bubble diagram, and structured JSON capturing spatial semantics. Generation: given a prompt and an outline, the model produces a complete, coherent floor plan. Editing: given a prompt, an outline, and a reference floor plan, the model outputs an updated plan aligned with the editing intent*

## 核心模块与公式推导

### 3.1 平面图的结构化分解与离散表示

HouseMind 的核心创新在于将连续的建筑平面图转化为离散的令牌序列，使 LLM 能够直接进行空间推理。一个包含 $N$ 个房间的建筑平面图被分解为两个组成部分：

$$x \ = \ \{ x _ { o } , \ \{ x _ { r _ { i } } \} _ { i = 1 } ^ { N } \}$$

其中 $x_o$ 是定义全局边界的外轮廓掩码，$x_{r_i}$ 是第 $i$ 个房间实例的掩码。这种分解将布局合成从纯视觉过程转变为房间实例级别的结构化推理问题。

### 3.2 分层矢量量化编码

为将几何信息转化为 LLM 可处理的离散令牌，HouseMind 采用两个独立的 VQ-VAE 编码器，分别处理轮廓和房间实例：

$$z _ { o } = E _ { o } ( x _ { o } ) , \qquad z _ { r _ { i } } = E _ { r } ( x _ { r _ { i } } , x _ { o } )$$

关键设计在于房间编码器 $E_r$ 以轮廓 $x_o$ 为条件输入，使房间令牌天然携带其在全局边界内的空间上下文信息，而非孤立编码。

轮廓量化的具体过程为：编码器输出的每个特征向量被映射到轮廓码本中距离最近的码字：

$$z _ { j } ^ { ( o ) } = e _ { k _ { j } ^ { \star } } ^ { ( o ) } , \quad k _ { j } ^ { \star } = \arg \operatorname* { m i n } _ { k } \big\| E _ { o } ( x _ { o } ) _ { j } - e _ { k } ^ { ( o ) } \big\| _ { 2 }$$

房间量化的过程类似，但以轮廓为条件：

$$z _ { i , j } ^ { ( r ) } = e _ { k _ { i , j } ^ { \star } } ^ { ( r ) } , \quad k _ { i , j } ^ { \star } = \arg \operatorname* { m i n } _ { k } \bigl\| E _ { r } ( x _ { r _ { i } } , x _ { o } ) _ { j } - e _ { k } ^ { ( r ) } \bigr\| _ { 2 }$$

其中 $e_k^{(o)}$ 和 $e_k^{(r)}$ 分别为轮廓码本和房间码本中的可学习码字，$j$ 为空间网格位置索引。

### 3.3 结构化令牌序列构建

量化后的令牌与语义标签交织，形成统一的平面图离散表示：

$$Z = [ z _ { o } , \ell _ { r _ { 1 } } , z _ { r _ { 1 } } , . . . , \ell _ { r _ { N } } , z _ { r _ { N } } ]$$

其中 $\ell_{r_i}$ 是房间 $r_i$ 的语义标签令牌（如“卧室”、“厨房”）。这一序列结构使 LLM 能够同时建模几何边界（$z_o$）、语义类别（$\ell_{r_i}$）和空间形态（$z_{r_i}$），在统一的自回归框架内实现多任务推理。

### 3.4 统一生成与编辑的概率建模

**生成任务**以轮廓令牌 $z_o$ 和文本描述 $s$ 为条件，自回归生成完整的布局令牌序列：

$$p ( Z \mid z _ { o } , s ) \ = \ \prod _ { t } p ( Z _ { t } \mid Z _ { < t } , z _ { o } , s )$$

**编辑任务**以源布局 $Z^{\mathrm{src}}$ 和编辑指令 $s$ 为条件，自回归生成目标布局 $Z^{\mathrm{tgt}}$，仅修改受指令影响的令牌：

$$p \big( Z ^ { \mathrm { t g t } } \mid Z ^ { \mathrm { s r c } } , s \big) = \prod _ { t } p \big( Z _ { t } ^ { \mathrm { t g t } } \Big| Z ^ { \mathrm { s r c } } , Z _ { < t } ^ { \mathrm { t g t } } , s \Big)$$

这种统一的概率建模使同一 LLM 骨干无需架构修改即可执行理解、生成和编辑三项任务。

### 3.5 三阶段训练管道

HouseMind 的训练分为三个顺序阶段（图 Figure 3）：

- **Stage 1（嵌入初始化）**：建立几何令牌与语言令牌之间的跨模态兼容性，确保 VQ-VAE 码本与 LLM 嵌入空间的对齐。
- **Stage 2（多模态预训练）**：对齐文本与空间表征，使 LLM 学会联合建模语言指令和布局几何。
- **Stage 3（指令调优/SFT）**：通过任务感知的监督微调，使模型具备理解、生成和编辑的空间推理能力。

消融实验（Table 4）证实，完整的三个阶段训练获得最低验证损失（0.0830），移除 Stage 1 或 Stage 2 均导致损失上升，表明嵌入初始化和多模态预训练缺一不可。

### 补充图表

![[assets/figures/papers/paper_list_l2347_https_arxiv_org_abs_2603_11640/figures/010_Figure.jpg]]
*Figure: A.1. VQ-VAE tokenization framework. The outline branch encodes the global boundary, while the conditional room branch encodes each room with outline context to capture spatial relations*

## 实验与分析

### 主要定量结果

HouseMind 在理解、生成与编辑三项核心任务上均取得显著优势，其核心机制在于将建筑平面图分解为轮廓与房间实例，并通过分层 VQ‑VAE 转化为离散令牌序列，使 LLM 能够在统一的自回归框架中执行空间推理。

**理解任务（Table 1）。** 在 RPLAN 数据集上，HouseMind 的房间定位准确度（LocAcc）达到 0.969，相较 LLaVA-v1.6-Mistral-7B-HF（0.225）提升超过 74 个百分点；房间面积差（AreaDiff）降至 0.549，而所有多模态基线均超过 10.0。这一差距源于离散实例令牌显式编码了几何与语义约束，使模型能够精确提取房间的位置、面积、邻接关系与空间关系，而非依赖像素级模糊推断。

**生成任务（Table 2）。** 与扩散模型 ChatHouseDiffusion 相比，HouseMind 的 Micro IoU 从 0.589 提升至 0.709，Macro IoU 从 0.531 提升至 0.654，FID 从 11.3 大幅降至 1.91，降幅达 83%。在图结构指标上，Node F1 达到 0.994，Edge Overlap 达到 0.880，均优于所有基线。值得注意的是，纯视觉方法（如 ChatHouseDiffusion）在像素指标上尚可，但图级正确性显著落后，说明其缺乏对房间拓扑关系的显式建模；而 HouseMind 通过将语义标签令牌与空间令牌交织，在自回归生成过程中直接约束了房间间的邻接与连通关系。

**编辑任务（Table 3）。** HouseMind 的编辑精度 △IoU 达到 0.608，远超 FLUX.1-Kontext-dev（0.053）和 Qwen-Image-Edit-2509（0.112），表明其能够在保持全局空间一致性的前提下精准执行增删房间的操作。最终布局的 Micro/Macro IoU 分别为 0.702 和 0.651，Node F1 为 0.993，说明编辑后的平面图在像素级和结构级均保持高质量。

### 消融实验

**训练阶段消融（Table 4）。** 完整三阶段训练管道取得最低验证损失（0.0830）。移除 Stage 1（嵌入初始化）后损失升至 0.0840，移除 Stage 2（多模态预训练）后损失升至 0.0831，表明嵌入初始化确保了令牌级跨模态一致性，而多模态预训练进一步细化了全局空间推理能力。两阶段缺一不可，共同支撑了 LLM 对几何与语义的联合建模。

**结构校正消融（Table C.1）。** 在 HouseMind-O 变体中，引入结构校正步骤使图编辑距离（GED）从 1.10 降至 1.03，Edge Overlap 从 0.873 升至 0.880。这表明后处理阶段对生成令牌的几何一致性校验能够有效修正局部拓扑错误，提升最终布局的结构保真度。

**码本大小消融（Table A.3）。** 在 256–1024 范围内，生成指标基本稳定：Macro IoU 在 0.654–0.657 之间，FID 在 1.89–1.97 之间。这说明 VQ‑VAE 的表示能力并非性能瓶颈，HouseMind 的增益主要来源于结构化令牌序列与 LLM 的空间推理能力，而非单纯增加码本容量。

### 失败模式与局限性

尽管 HouseMind 在定量指标上取得显著提升，分析揭示了以下关键局限：

1. **编辑操作的拓扑复杂性受限。** 编辑模块目前仅支持简单增删房间，难以处理房间重组、合并拆分等复杂拓扑变换。Figure D.1 显示编辑任务的 △IoU 分布呈双峰形态，低峰主要由模糊的空间指令导致——当自然语言提示未能精确定义修改区域时，模型难以准确执行编辑意图。

2. **功能构件缺失。** 当前标记化框架仅编码房间实例与轮廓，未包含门、窗、家具等功能构件。这限制了 HouseMind 在详细室内设计场景中的应用，生成的平面图可能不符合专业设计标准。

3. **像素‑结构耦合分析（Figure D.2）。** 散点图显示，扩散模型（Diffusion）的 Macro IoU 与 Edge Overlap 相关性较弱，说明其像素级质量与结构正确性存在脱节；而 HouseMind 的像素‑结构耦合更紧密，但仍存在少量高像素质量、低结构一致性的样本，提示自回归生成过程中偶尔会牺牲拓扑正确性以追求视觉连贯性。

4. **分布外泛化。** 模型在 RPLAN 固定划分上表现优异，但在极端分布外场景（如矛盾约束或逻辑上不可能的空间指令）下的行为尚未系统评估，需进一步验证其鲁棒性。

### 补充图表

![[assets/figures/papers/paper_list_l2347_https_arxiv_org_abs_2603_11640/figures/004_Table_1.jpg]]
*Table 1: Understanding results. Success: success rate; RMR: room match rate; LocAcc: room location accuracy; AreaDiff: room area difference (m2); AdjAcc: room adjacency accuracy; RelAcc: spatial relation accuracy*

![[assets/figures/papers/paper_list_l2347_https_arxiv_org_abs_2603_11640/figures/005_Table_2.jpg]]
*Table 2: Generation results. Micro/Macro IoU measure pixel-level overlap; SSIM [40] and PSNR quantify perceptual similarity; FID [6] and GED [30] evaluate distributional realism; Node F1 and Edge Overlap assess graph-level correctness. * denotes methods without released code; results are reproduced*

![[assets/figures/papers/paper_list_l2347_https_arxiv_org_abs_2603_11640/figures/006_Table_3.jpg]]
*Table 3: Editing results. ∆IoU and ∆MSE measure editing precision (spatial and pixel-level change correctness); Micro/Macro IoU assess final layout quality; GED evaluates distributional realism; Node F1 and Edge Overlap assess graph-level consistency*

![[assets/figures/papers/paper_list_l2347_https_arxiv_org_abs_2603_11640/figures/008_Table_4.jpg]]
*Table 4: Loss under different training-stage configurations*

![[assets/figures/papers/paper_list_l2347_https_arxiv_org_abs_2603_11640/figures/014_Table.jpg]]
*Table: C.1. Impact of Structural Correction in HouseMind-O*

![[assets/figures/papers/paper_list_l2347_https_arxiv_org_abs_2603_11640/figures/012_Table.jpg]]
*Table: A.3. Codebook size ablation study*

![[assets/figures/papers/paper_list_l2347_https_arxiv_org_abs_2603_11640/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison results of understanding, generation, and editing. For understanding tasks (U), HouseMind accurately identifies the number of rooms and their connections. For generation tasks (G), HouseMind preserves both the room layout and the overall outline consistency; the generation prompts are provided in the supplementary materials. For editing tasks (E), HouseMind accurately executes the specified modifications when the instructions are explicit*

![[assets/figures/papers/paper_list_l2347_https_arxiv_org_abs_2603_11640/figures/016_Figure.jpg]]
*Figure: (a) HouseMind-O (b) FloorPlanLLaMA* (c) ChatHouseDiffusion Figure D.2. Pixel–structure coupling analysis. Scatter plots show the correlation between Macro IoU and Edge Overlap for three generation paradigms*

![[assets/figures/papers/paper_list_l2347_https_arxiv_org_abs_2603_11640/figures/015_Figure.jpg]]
*Figure: D.1. Result distribution across tasks. HouseMind-O maintains stable, high-performance distributions in understanding and generation, with the bimodal ∆IoU in editing mainly caused by unclear spatial instructions*

## 方法谱系与知识库定位

### 1. 任务定位：从视觉合成到空间推理的范式迁移

建筑平面图合成长期被建模为纯视觉生成问题，主流范式包括基于生成对抗网络（GAN）、变分自编码器（VAE）和扩散模型的像素级布局生成。这些方法将布局视为连续图像，缺乏对房间实例的显式建模，导致三个核心瓶颈：

- **全局空间连贯性差**：像素级生成难以保证房间之间的拓扑一致性，常出现重叠、缝隙或非连通区域。
- **可控性弱**：文本条件通常以全局嵌入形式注入，无法精确控制单个房间的位置、大小和邻接关系。
- **任务割裂**：理解、生成和编辑需要三个独立模型，无法在统一框架内完成。

HouseMind 的核心贡献在于**将平面图从连续视觉信号转化为离散结构化令牌序列**，使大语言模型（LLM）能够以自回归方式执行空间推理。这一范式迁移的根本洞察是：建筑平面图的本质不是像素排列，而是由轮廓边界和房间实例构成的空间关系图——这种结构天然适合序列化建模。

### 2. 与现有方法的谱系关系

#### 2.1 扩散模型基线：视觉质量与结构控制的张力

**ChatHouseDiffusion**（作为生成任务的主要基线）代表了扩散模型在布局生成中的最新进展。该方法将文本条件注入去噪过程，在视觉质量（FID）上取得了当时最优结果。然而，HouseMind 的实验揭示了扩散范式的结构性缺陷：

- 在 RPLAN 数据集上，ChatHouseDiffusion 的 FID 为 11.3，而 HouseMind 降至 1.91（Table 2），表明扩散模型生成的布局分布与真实分布存在系统性偏差。
- 更关键的是，Micro IoU 从 0.589 提升至 0.709（+20.4%），Macro IoU 从 0.551 提升至 0.654（+18.7%），说明像素级重叠度的提升源于房间实例级别的精确建模，而非视觉质量的简单改善。
- 图级指标进一步验证了这一判断：Node F1 从 0.985 提升至 0.994，Edge Overlap 从 0.873 提升至 0.880——扩散模型在结构正确性上的差距虽小但持续存在。

**Tell2Design** 和 **FloorPlanLLaMA** 分别代表了基于语言模型和序列生成的早期尝试。FloorPlanLLaMA 将布局坐标序列化后输入 LLM，但缺乏离散化标记机制，导致坐标预测的累积误差。HouseMind 的 VQ-VAE 标记化从根本上解决了这一问题：通过将连续几何量化为离散码字，模型只需在有限词汇表上进行分类，而非回归连续值。

#### 2.2 多模态 LLM 基线：通用能力的边界

在理解任务上，HouseMind 与四个通用多模态 LLM 进行了对比：**LLaVA-v1.6-Mistral-7B-HF**、**Qwen3-VL-8B-Instruct**、**InternVL3.5-8B** 和 **MiniCPM-V 4.5**。这些模型在自然图像理解上表现优异，但在平面图理解上几乎完全失效：

- 房间定位准确度（LocAcc）：HouseMind 达到 0.969，而最强基线 LLaVA-v1.6 仅为 0.225（Table 1）。
- 房间匹配率（RMR）：HouseMind 达到 1.000（完美），基线均低于 0.30。

这一悬殊差距揭示了通用多模态 LLM 的根本局限：它们的视觉编码器在自然图像上预训练，缺乏对建筑符号（墙线、房间边界、空间拓扑）的表征能力。HouseMind 通过**领域特定的 VQ-VAE 标记化**将平面图转化为 LLM 可理解的“空间语言”，绕过了通用视觉编码器的表征瓶颈。

#### 2.3 编辑任务基线：精确修改与全局一致性

在编辑任务上，**FLUX.1-Kontext-dev** 和 **Qwen-Image-Edit-2509** 代表了基于扩散的图像编辑方法。这些方法在自然图像编辑中表现出色，但在平面图编辑中暴露了精确性不足的问题：

- △IoU（编辑精度）：HouseMind 达到 0.608，FLUX.1-Kontext-dev 仅为 0.053（Table 3）。
- 扩散编辑方法倾向于在修改区域产生模糊或伪影，且难以保持未修改区域的完全不变。
- HouseMind 的优势在于：编辑操作直接在离散令牌序列上进行，仅修改受指令影响的令牌，天然保证了未编辑区域的完整性。

### 3. 技术演进脉络中的坐标定位

HouseMind 的方法设计体现了三条技术路线的融合：

| 技术路线 | 来源 | HouseMind 的继承与创新 |
|---------|------|----------------------|
| VQ-VAE 离散化 | VQ-VAE（van den Oord et al., NeurIPS 2017）| 分层双分支架构：轮廓和房间分别量化，房间编码以轮廓为条件，保留空间上下文 |
| LLM 多模态对齐 | LLaVA 系列、Qwen-VL 系列 | 三阶段训练管道：嵌入初始化→多模态预训练→指令调优，逐步对齐几何与语言 |
| 结构化布局生成 | HouseGAN、Graph2Plan 等图约束方法 | 将图结构隐式编码为令牌序列的交织模式，无需显式图神经网络 |

值得注意的是，HouseMind 的**三阶段训练管道**（Figure 3）是其成功的关键工程贡献。消融实验（Table 4）表明：

- 完整三阶段训练获得最低评估损失（0.0830）。
- 移除 Stage 1（嵌入初始化）导致损失升至 0.0840，说明随机初始化的几何令牌与语言令牌之间存在模态鸿沟。
- 移除 Stage 2（多模态预训练）导致损失升至 0.0831，说明仅靠指令调优无法充分对齐跨模态表征。

这一发现具有方法论意义：**对于将结构化领域知识注入 LLM 的任务，分阶段对齐策略可能比端到端微调更有效**。

### 4. 适用边界与局限

#### 4.1 当前能力的明确边界

1. **编辑操作受限**：编辑模块仅支持简单的房间添加和删除，无法处理复杂拓扑变换（如合并房间、改变连接关系、调整走廊结构）。这是离散令牌序列编辑的固有局限——序列编辑天然适合局部替换，而拓扑变换需要全局重排。

2. **功能构件缺失**：当前标记化框架仅建模轮廓和房间，未包含门、窗、家具等功能构件。这限制了 HouseMind 在详细室内设计中的应用。将这些构件集成进令牌序列需要扩展 VQ-VAE 分支或引入新的条件编码机制。

3. **美学与偏好对齐不足**：生成结果虽在结构指标上表现优异，但未显式建模人类设计偏好（如空间比例美学、动线合理性）。这可能导致生成布局在专业设计师看来“正确但不够好”。

#### 4.2 分布外泛化的不确定性

论文在 Figure F.1 中展示了分布外（OOD）生成结果，但未提供系统性的 OOD 评估。以下场景需要进一步验证：

- **矛盾约束**：当文本指令包含逻辑上不可能的空间需求时（如“5平方米的宴会厅”），模型的退化行为未知。
- **极端布局**：非常规轮廓形状（如三角形、圆形边界）或超多房间（N > 20）场景下的结构一致性。
- **跨风格迁移**：在 RPLAN 数据集（以住宅为主）上训练的模型，能否泛化到办公、商业等不同建筑类型。

#### 4.3 计算效率与部署约束

HouseMind 使用 Qwen3-0.6B 作为 LLM 骨干，参数量仅 0.6B，远小于通用多模态 LLM（7B–8B）。这一设计选择反映了**领域专用模型的效率优势**：通过 VQ-VAE 将视觉理解外包给专用编码器，LLM 只需处理离散令牌序列，降低了对大规模视觉编码器的依赖。然而，三阶段训练管道的计算成本、VQ-VAE 的推理延迟以及整体流程在终端设备上的部署可行性，论文未给出详细数据。

### 5. 开放问题与未来方向

基于上述分析，HouseMind 开辟了以下研究问题：

1. **功能构件的层次化标记**：如何将门、窗等构件作为房间令牌的“子令牌”集成进序列，形成多层次的空间表示？这可能需要引入层次化 VQ-VAE 或递归标记化策略。

2. **偏好对齐与 RLHF**：能否将设计师反馈纳入训练循环，通过强化学习（RLHF）或直接偏好优化（DPO）提升生成布局的美学和功能质量？这需要构建平面图偏好数据集，定义可量化的偏好指标。

3. **复杂编辑与拓扑变换**：如何扩展编辑能力以支持非局部修改？可能的路径包括：(a) 引入图神经网络作为编辑规划器，先生成目标拓扑再映射为令牌序列；(b) 采用扩散模型与离散令牌的混合架构，利用扩散处理连续变形、令牌处理离散修改。

4. **极端分布外的鲁棒性**：需要系统评估模型在矛盾指令、罕见轮廓和超大规模布局下的行为，建立安全边界和退化模式文档。

5. **轻量化部署**：0.6B 的 LLM 骨干已经较小，但 VQ-VAE 编码器-解码器和三阶段训练流程是否可进一步压缩，以适应移动端或 Web 端实时交互场景？

6. **多模态空间推理的泛化**：HouseMind 的“离散化+LLM”范式能否推广到其他结构化空间推理任务，如电路布局、家具摆放、城市地块规划？这需要验证 VQ-VAE 标记化在不同空间领域中的可迁移性。

## 原文 PDF

![[paperPDFs/CVPR_2026/Tokenization_Allows_Multimodal_Large_Language_Models_to_Understand_Generate_and_Edit_Architectural_Floor_Plans.pdf]]
