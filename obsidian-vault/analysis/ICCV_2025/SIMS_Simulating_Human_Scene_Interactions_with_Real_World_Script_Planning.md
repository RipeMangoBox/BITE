---
title: "SIMS: Simulating Stylized Human-Scene Interactions with Retrieval-Augmented Script Generation"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/SIMS_Simulating_Human_Scene_Interactions_with_Real_World_Script_Planning.pdf
project_link: https://wenjiawang0312.github.io/projects/sims/
code_link: null
aliases:
- SIMS
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 引入检索增强脚本生成（RASG）为高层提供多样化、连贯的长脚本，并设计多条件控制策略（融合场景高度图、任务目标和CLIP文本嵌入）实现低层风格化运动，通过有限状态机将二者衔接，使物理模拟角色能根据文本和场景执行丰富交互。
primary_logic: RASG通过检索预生成的短脚本库并结合场景布局生成长期叙事，解决了直接LLM生成脚本的冗余和多样性不足问题；多条件策略使物理角色能够利用文本嵌入自然表达风格，而无需依赖精确的关键帧或接触参考，从而在保持物理合理性的同时大幅提升交互的多样性和表现力。
claims:
- SIMS在多个交互技能的成功率和接触误差上全面超越或匹配SOTA方法，同时支持任意文本风格输入。
- SIMS显著提升了运动多样性，尤其相比UniHSI，APD从约1.1大幅提升至16以上，接近真实数据分布。
- RASG生成的脚本比直接LLM生成更具多样性（SBERT相似度更低）且生成速度更快。
- 消融实验证明多条件中的文本嵌入和高度图对于风格多样性和任务成功率均不可或缺。
---

# SIMS: Simulating Stylized Human-Scene Interactions with Retrieval-Augmented Script Generation

> [!tip] 核心洞察
> RASG通过检索预生成的短脚本库并结合场景布局生成长期叙事，解决了直接LLM生成脚本的冗余和多样性不足问题；多条件策略使物理角色能够利用文本嵌入自然表达风格，而无需依赖精确的关键帧或接触参考，从而在保持物理合理性的同时大幅提升交互的多样性和表现力。

| 字段 | 内容 |
|------|------|
| 中文题名 | SIMS：基于检索增强脚本生成的风格化人-场景交互仿真 |
| 英文题名 | SIMS: Simulating Stylized Human-Scene Interactions with Retrieval-Augmented Script Generation |
| 会议/期刊 | ICCV 2025 |
| Links | [Project](https://wenjiawang0312.github.io/projects/sims/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | SIMS |
| Dataset | 3DFront, Motion Diversity, User Study |

> [!tip] 效果简介
> - 3DFront 上，Sit Success Rate (%) 98.1 vs 94.3 (UniHSI) (+3.8)；Lie Success Rate (%) 87.6 vs 81.5 (UniHSI) (+6.1)；Sit Contact Error 0.028 vs 0.032 (UniHSI) (-0.004)。
> - Motion Diversity (FID↓, APD↑) 上，Sit FID / APD 125.66 / 16.55 vs 153.84 / 1.14 (UniHSI) (-28.18 / +15.41)。
> - User Study 上，Emotional Resonance (1-5) 3.8 vs 3.0 (UniHSI) (+0.8)。

## 概要

### 1. 问题与瓶颈

长期人-场景交互（HSI）的仿真面临一个核心矛盾：**物理合理性**、**风格多样性**与**自动规划**三者难以兼得。基于运动学的方法（如NSM、SAMP、Humanise等）虽能生成多样化运动，却普遍存在穿透、滑步等物理伪影；基于物理的方法（如UniHSI）虽保证了物理合理性，却高度依赖精确的参考运动，导致运动多样性严重受限——其规划也仅限于简单的接触序列，无法表达丰富的身体语言与情感。这一瓶颈使得长期叙事驱动的、风格化的物理角色动画长期处于空白。

### 2. 核心方法

SIMS提出了一套**层次化框架**来打破上述僵局：

- **高层**：检索增强脚本生成（RASG）——通过检索预构建的短脚本库并结合场景布局，自动生成多样化、连贯的长叙事脚本，赋予角色情感与风格意图。
- **低层**：多条件控制策略——融合场景高度图、任务目标与CLIP文本嵌入，使物理模拟角色能根据文本和场景自主表达风格化运动。
- **桥接**：有限状态机（FSM）解析脚本中的关键帧，调度可复用的技能策略，在合适时机触发技能切换。

这一设计的核心洞察在于：**RASG解决了直接LLM生成脚本的冗余与多样性不足问题**，而**多条件策略使物理角色无需依赖精确关键帧或接触参考即可自然表达风格**，从而在保持物理合理性的同时大幅提升交互的多样性与表现力。

### 3. 主要结果

在3DFront场景基准上，SIMS在多个交互技能的成功率与接触误差上全面超越或匹配SOTA方法（Table 3），例如Sit成功率98.1%（UniHSI 94.3%），Lie成功率87.6%（UniHSI 81.5%）。更关键的是，**运动多样性获得质的提升**：Sit技能的APD从UniHSI的约1.1跃升至16.55，FID从153.84降至125.66（Table 4）。用户研究进一步表明，SIMS在物理真实感、运动多样性、情节吸引力与情感共鸣上均显著优于UniHSI（Table 5）。

### 4. 方法谱系与知识库定位

SIMS定位于**物理仿真驱动的长期人-场景交互**这一细分方向，其谱系可沿两条线索追溯：

| 维度 | 运动学方法 | 物理方法 | SIMS |
|------|-----------|---------|------|
| 代表工作 | NSM, SAMP, Humanise, AffordMotion, TesMo | InterScene, UniHSI | — |
| 物理合理性 | 弱（穿透、滑步） | 强 | 强 |
| 风格多样性 | 中-高 | 低（依赖参考运动） | 高（文本驱动） |
| 自动化程度 | 部分需手动规划 | 部分需手动规划 | 全自动（RASG） |
| 文本/场景感知 | 有限 | 有限 | 文本嵌入+高度图 |

SIMS的关键改进在于：将**LLM驱动的检索增强生成**引入脚本规划层，并以**多条件（文本+场景+目标）统一控制策略**替代传统的单目标或接触驱动范式。这一组合使其成为首个同时具备物理合理性、风格多样性与全自动规划能力的长期HSI框架。

### 5. 证据强度与局限

上述结论由多项定量实验支撑，核心证据置信度均≥0.95。但仍需注意：当前数据集缺乏足够多的真实情感与多样风格运动；人形模型未包含手指关节，无法模拟精细操作；框架仅支持单角色，尚未扩展到多智能体场景。这些局限指向未来的改进方向。

### 问题背景

在计算机图形学与具身智能的交汇领域，生成长期、物理合理且风格多样的人-场景交互（Human-Scene Interaction, HSI）一直是一个核心挑战。理想的系统应当允许一个物理仿真角色在复杂的3D室内场景中，根据高层叙事意图自主完成一系列日常活动——例如从走到坐、从躺到取物——同时保持自然的身体语言、情感表达和精确的物体接触。这一能力对游戏、虚拟现实、机器人仿真和数字人叙事等应用至关重要。

### 现有方法的根本瓶颈

当前长期人-场景交互方法可大致分为两类，但各自存在难以调和的矛盾：

**基于运动学的方法**（如 **NSM**、**SAMP**、**Humanise**、**AffordMotion**、**TesMo**）通过运动合成或图模型生成动作序列，能够在几何层面实现多样化的交互。然而，这类方法不经过物理仿真验证，普遍存在穿透、滑步等物理误差，无法保证生成的交互在真实物理约束下成立。

**基于物理的方法**（如 **InterScene**、**UniHSI**）通过强化学习训练控制策略，在物理仿真器中驱动角色，天然保证接触的物理合理性。但这一优势的代价是运动多样性和风格表达能力的严重受限。以当前SOTA方法 **UniHSI** 为例，其高层规划器仅能生成简单的接触序列（如“走到椅子-坐下”），缺乏对情感、风格和身体语言的描述能力；低层控制器则高度依赖精确的参考运动进行模仿，导致生成的运动趋同于训练数据中的平均模式，丧失了风格多样性。

定量证据揭示了这一瓶颈的严重性：在运动多样性指标上，UniHSI的坐下动作平均成对距离（APD）仅为约1.1，而真实数据的APD超过16（Table 4），说明其生成的运动几乎完全坍缩为单一模式。

### 核心因果机制

上述瓶颈的根源在于两个层面的因果断裂：

1. **规划层的语义贫乏**：现有物理方法的高层规划仅输出技能标签和接触目标，无法将“悲伤地缓慢坐下”或“兴奋地跳上沙发”这类富含风格和情感的意图传递给低层控制器。缺乏文本语义作为中间表征，使得高层叙事与低层运动风格之间不存在可优化的信息通道。

2. **控制层的条件单一**：低层策略通常仅以目标位置和自身状态为输入，缺乏对场景几何的细粒度感知和对风格指令的编码能力。这导致角色无法根据周围环境（如障碍物、物体形状）调整动作，也无法根据文本描述改变运动风格。

### 本文动机

基于以上分析，本文的核心动机是：**构建一个统一的层次化框架，在保持物理合理性的前提下，同时实现交互的自动规划、风格多样性和场景感知能力**。具体而言，需要解决三个关键问题：

- 如何自动生成具有情感和风格多样性的长期交互脚本，而非简单接触序列？
- 如何让低层物理控制器理解和执行文本描述的风格指令？
- 如何让控制器感知复杂3D场景几何，实现精确的物体交互和避障？

SIMS通过引入**检索增强脚本生成（RASG）** 解决第一个问题，通过**多条件控制策略**（融合场景高度图、任务目标和CLIP文本嵌入）解决后两个问题，并用**有限状态机**将二者无缝衔接，构成了完整的解决方案。

## 核心方法与创新机理

### 瓶颈突破：从物理合理性与风格多样性的两难中突围

长期人-场景交互（HSI）面临一个根本性矛盾：**基于运动学的方法**（如NSM、SAMP、Humanise、AffordMotion、TesMo）能生成多样化运动，却普遍存在穿透、滑步等物理伪影；**基于物理的方法**（如InterScene、UniHSI）保证了物理合理性，却严重依赖精确参考运动，导致运动同质化严重。以SOTA物理方法UniHSI为例，其规划器仅能生成简单接触序列，无法表达身体语言和情感，运动多样性指标APD低至约1.1，远偏离真实数据分布。

SIMS的破局点在于识别出**高层规划自动化与低层风格表达能力**是一体两面的关键瓶颈——没有多样化的长脚本，低层控制器无从表达风格；没有文本感知的控制器，高层脚本的叙事意图无法落地。

### 核心创新机制：检索增强脚本生成 × 多条件物理控制

SIMS通过三个相互咬合的设计实现了突破：

**1. 检索增强脚本生成（RASG）替代直接LLM生成**

直接让LLM生成长脚本存在冗余和多样性不足的问题。RASG采用“先建库、再检索、后组装”的策略：首先利用LLM批量生成由关键帧序列、摘要和风格标签组成的短脚本 $p = [ \{ f_0, f_1, ..., f_N \}, u, d ]$，其中每个关键帧 $f = (s, o, c, e)$ 指定技能 $s$、目标物体 $o$、动作描述 $c$ 和情感/风格 $e$；然后用CLIP提取摘要嵌入作为检索键。当用户输入主题时，系统通过风格过滤、语义相似度检索和LLM摘要过滤三阶段筛选，将4-5个短脚本（约20个关键帧）组合为连贯的长故事。消融实验证实，RASG生成的脚本SBERT相似度更低（多样性更高），且生成速度显著优于直接LLM生成（Table 6）。

**2. 多条件控制策略实现文本感知的风格化运动**

低层RL策略 $\pi(\mathbf{a}_t | \mathbf{s}_t, \mathbf{h}_t, \mathbf{g}_t, \mathbf{z})$ 同时接收四类条件：自身感知 $\mathbf{s}_t$、12×12自中心高度图 $\mathbf{h}_t$、任务目标 $\mathbf{g}_t$（含物体包围盒与目标位置）、以及CLIP文本嵌入 $\mathbf{z}$。其中文本嵌入通过重实现的MotionCLIP注入——训练一个transformer自编码器将运动序列映射为与CLIP文本特征对齐的嵌入，作为策略的语言条件。奖励函数 $r_t = \lambda^{\mathrm{style}} r_t^{\mathrm{style}} + \lambda^{\mathrm{task}} r_t^{\mathrm{task}}$ 将文本判别器给出的风格奖励与任务奖励加权求和，使角色无需依赖精确关键帧或接触参考即可自然表达风格。

**3. 有限状态机衔接高层叙事与低层执行**

有限状态机（FSM）解析长脚本中的关键帧，在合适时机触发技能切换，调度7个可复用的独立策略（Walk、Idle、Sit、Lie、Reach、GetUp、Carry）。这种模块化设计使得添加新技能时仅需训练单独策略并更新脚本库，无需重训整体框架。

### 与基线方法的关键差异

| 能力维度 | 现有物理方法（UniHSI等） | SIMS |
|---------|----------------------|------|
| 规划自动化 | 手动规划或仅生成接触序列 | RASG自动生成具有情感、风格的多样化长脚本 |
| 文本感知 | 无文本感知，仅目标或接触驱动 | CLIP文本嵌入注入风格控制 |
| 场景感知 | 部分方法仅使用位置目标 | 12×12自中心高度图 + 目标状态，支持复杂3D场景 |
| 技能可扩展性 | 多数需重新训练整个控制器 | 仅需为新技能训练单独策略并更新脚本库 |

### 证据支撑

- **物理性能**：SIMS在3DFront场景上的Sit成功率达98.1%（UniHSI为94.3%），Lie成功率达87.6%（UniHSI为81.5%），接触误差全面匹配或超越SOTA（Table 3）。
- **运动多样性**：Sit技能的FID从153.84降至125.66，APD从1.14跃升至16.55，接近真实数据分布（Table 4）。
- **风格表达**：用户研究中情感共鸣评分达3.8（UniHSI为3.0），运动多样性评分3.6（UniHSI为2.9）（Table 5）。
- **消融验证**：移除文本嵌入导致APD显著下降，移除高度图导致成功率和FID严重退化（Table 11），证明多条件设计不可或缺。

SIMS 是一个层次化的角色动画系统，其核心设计思路是将高层的叙事意图与低层的物理控制解耦，并通过一个有限状态机（FSM）将二者无缝衔接。系统接收用户提供的**对话式故事主题**和**3D场景布局**作为输入，最终输出一个在物理仿真环境中执行多样化、风格化交互的模拟角色。

整体管线由四个关键模块串联构成，形成“脚本生成→任务解析→策略调度→物理执行”的闭环：

1.  **短脚本数据库构建**：离线阶段，利用大语言模型（LLM）为所有可用技能、文本描述、风格标签和场景物体生成大量短脚本。每个短脚本 $p = [ \{ f_0, f_1, ..., f_N \}, u, d ]$ 包含一个关键帧序列、一段摘要 $u$ 和一个风格标签 $d$。其中每个关键帧 $f = ( s, o, c, e )$ 精确指定了技能 $s$、目标物体 $o$、动作描述 $c$ 和情感/风格 $e$。随后用 CLIP 文本编码器提取摘要的嵌入作为检索键，构建可查询的脚本库。

2.  **检索增强脚本生成（RASG）**：在线阶段，根据用户输入的故事主题，RASG 通过两阶段检索将短脚本组合为连贯的长叙事。首先通过风格标签过滤，再基于摘要的 CLIP 语义相似度检索 top-k 个候选短脚本；随后由 LLM 再次筛选并拼接这些短脚本，形成包含约20个关键帧的流畅长故事。这一机制有效避免了直接让 LLM 生成长脚本时出现的冗余和多样性不足问题。

3.  **有限状态机（FSM）**：作为高层规划与低层控制之间的桥梁，FSM 解析长脚本中的每个关键帧，从中提取技能类型、动作描述和场景几何信息，并将其转化为低层策略可消费的**任务目标**、**语言嵌入**和**高度图条件**。FSM 负责在合适时机触发技能切换，调度多个可复用的独立策略。

4.  **多条件控制策略**：低层由7个独立的强化学习策略构成（Walk、Idle、Sit、Lie、Reach、GetUp、Carry），每个策略接收四类条件输入：角色本体感知 $\mathbf{s}_t$、12×12 自中心高度图 $\mathbf{h}_t$、任务特定目标状态 $\mathbf{g}_t$ 以及来自 MotionCLIP 的语言嵌入 $\mathbf{z}$。策略输出的动作 $\mathbf{a}_t$ 直接驱动物理仿真角色。奖励函数 $r_t = \lambda^{\mathrm{style}} r_t^{\mathrm{style}} + \lambda^{\mathrm{task}} r_t^{\mathrm{task}}$ 由文本条件判别器给出的风格奖励和任务奖励加权求和构成，确保角色在完成交互任务的同时表达出与文本描述一致的风格。

这种模块化设计使得框架具备良好的可扩展性：当需要添加新技能时，仅需训练该技能的独立策略并更新短脚本数据库，无需重新训练整个系统。

![[assets/figures/papers/paper_list_l1774_SIMS_Simulating_Human_Scene_Interactions_with_Real_World_Script_Planning/figures/003_Figure_2.jpg]]
*Figure 2: (a) Our main pipeline. We prompt LLMs to generate new short scripts following their emotion and interaction logic. The retrieval process includes 2 stages. We first retrieve the top-k short script with semantics similarity, then ask LLM to retrieve useful samples from the short scripts and concatenate them as a fluent long-term story. In the Finite State Machine. We parse skills, captions, and scene geometry from each keyframe into task goals, language embeddings, and heightmap conditions to drive the low-level physical control policy. (c) The multi-condition physics policy. We divide common skills into 3 categories: Lococmotion, HSI, and DOI. Skills in the same category share similar task...*

SIMS 的核心架构由三个关键模块构成：**短脚本数据库构建**、**检索增强脚本生成（RASG）** 和 **多条件控制策略**。三者通过有限状态机（FSM）衔接，形成从高层叙事规划到低层物理控制的完整闭环。

### 短脚本的形式化定义

系统首先利用大语言模型（LLM）生成一个短脚本数据库。每个短脚本 $p$ 被形式化定义为一个三元组：

$$p = [ \{ f_0, f_1, ..., f_N \}, u, d ]$$

其中 $\{ f_0, f_1, ..., f_N \}$ 为关键帧序列，$u$ 为脚本摘要文本，$d$ 为风格标签。每个关键帧 $f$ 进一步定义为四元组：

$$f = ( s, o, c, e )$$

其中 $s$ 指定交互技能（如 Sit、Walk），$o$ 为目标物体，$c$ 为动作描述文本，$e$ 为情感或风格标签。该结构化定义使得脚本既包含可执行的动作序列，又携带丰富的语义和风格信息，为后续检索与策略控制提供统一接口。

### 检索增强脚本生成（RASG）

RASG 模块负责将用户输入的主题转化为连贯的长故事脚本。其核心机制是两阶段检索：首先利用 CLIP 模型提取短脚本摘要 $u$ 的文本嵌入作为检索键，通过语义相似度从数据库中召回 top-k 候选短脚本；随后由 LLM 对候选脚本进行过滤和拼接，生成包含约 20 个关键帧的长叙事。这一设计规避了直接 LLM 生成的冗余和多样性不足问题（消融实验证据见 Table 6）。

### 多条件控制策略

低层物理控制采用强化学习训练的策略网络，其输入由四部分条件组成：

$$\pi ( \mathbf { a } _ { t } | \mathbf { s } _ { t } , \mathbf { h } _ { t } , \mathbf { g } _ { t } , \mathbf { z } )$$

- $\mathbf{s}_t$：人形角色本体感知（关节角度、速度等）
- $\mathbf{h}_t$：以角色为中心的 $12 \times 12$ 高度图，提供场景几何感知
- $\mathbf{g}_t$：任务目标状态，包含目标物体的包围盒 $\mathbf{g}^{bbox} \in \mathbb{R}^{3 \times 8}$ 和目标位置 $\bar{\mathbf{g}}^{tar} \in \mathbb{R}^{3}$
- $\mathbf{z}$：语言嵌入，由重实现的 MotionCLIP 将运动序列编码为与 CLIP 文本特征对齐的单位球面嵌入

策略优化目标为最大化期望折扣回报：

$$J ( \pi ) = \mathbb { E } _ { p ( \tau \mid \pi ) } \left[ \sum _ { t = 0 } ^ { T - 1 } \gamma ^ { t } r _ { t } \right]$$

其中每步奖励 $r_t$ 由风格奖励与任务奖励加权组合：

$$r _ { t } = \lambda ^ { \mathrm { s t y l e } } r _ { t } ^ { \mathrm { s t y l e } } + \lambda ^ { \mathrm { t a s k } } r _ { t } ^ { \mathrm { t a s k } }$$

- $r_t^{\mathrm{style}}$：由文本条件运动判别器给出的风格一致性奖励，使生成运动与文本描述对齐
- $r_t^{\mathrm{task}}$：任务相关奖励，以 HSI 交互为例，近端奖励定义为 $r_t^{near} = \exp(-10.0 \| x_t^{*} - x_t^{root} \|^2)$，鼓励角色根部接近接触目标面

### 运动-文本对齐：MotionCLIP 重实现

为实现文本嵌入 $\mathbf{z}$ 对运动风格的有效控制，SIMS 重实现了 MotionCLIP 框架。运动编码器将运动序列 $\hat{\mathbf{m}}$ 映射为嵌入：

$$\mathbf { z } = \mathrm { E n c } _ { m } ( \hat { \mathbf { m } } )$$

对齐损失采用运动嵌入与降维 CLIP 文本特征之间的余弦距离：

$$\mathcal { L } _ { \mathrm { a l i g n } } ^ { m , t } = 1 - d _ { \mathrm { c o s } } \left( \mathrm { E n c } _ { m } \left( \hat { \mathbf { m } } \right) , \mathrm { M L P } _ { d } ( \mathrm { E n c } _ { l } ( \mathbf { c } ) ) \right)$$

该对齐机制使策略能够通过文本嵌入 $\mathbf{z}$ 自然表达多样化风格，而无需依赖精确的关键帧或接触参考运动。消融实验（Table 11）证实，移除文本嵌入会导致运动多样性指标 APD 显著下降，移除高度图则导致成功率和 FID 严重退化，验证了两者在多条件控制中的不可替代性。

## 实验与关键发现

### 核心性能：物理合理性与任务成功率

SIMS在3DFront场景基准上对多种人-场景交互技能进行了定量评估，与当前SOTA基于物理的长期HSI方法**UniHSI**进行了公平对比（Table 3）。为保证公平，SIMS的Sit、Lie和Reach策略仅使用与基线相同的**SAMP**数据集训练，Carry策略仅使用**AMASS**中的少量搬运运动。

![[assets/figures/papers/paper_list_l1774_SIMS_Simulating_Human_Scene_Interactions_with_Real_World_Script_Planning/figures/005_Table_3.jpg]]
*Table 3: Comparision on Baseline Models. For fair comparison, our Sit, Lie, and Reach policies are only trained on SAMP [12] here. While our Carry policy is trained on the small amount of carry motions from AMASS [22]. (+data) here represents our results trained on available motions from the mixture of 6 datasets*

结果表明，SIMS在所有技能的成功率和接触误差上均达到或超越了UniHSI的水平：

- **Sit**：成功率98.1%（UniHSI为94.3%），接触误差0.028（UniHSI为0.032）。
- **Lie**：成功率87.6%（UniHSI为81.5%），接触误差0.036（UniHSI为0.039）。
- **Reach**：成功率93.2%（UniHSI为92.8%），接触误差0.041（UniHSI为0.043）。
- **Carry**：成功率79.2%，接触误差0.045，UniHSI未报告该技能。

当SIMS使用全部6个风格化运动数据集（+data）训练后，性能进一步提升——Sit成功率升至99.5%，Lie升至95.8%，Carry升至89.3%，验证了数据多样性对物理控制的正向作用。

**关键结论**：SIMS在维持甚至提升物理合理性的前提下，实现了远超现有方法的风格多样性和文本感知能力。这一“物理-风格”双赢的结果，直接归因于多条件控制策略中文本嵌入与高度图的协同作用（见消融部分）。

### 运动多样性：从单一到丰富

运动多样性是SIMS相比UniHSI最显著的提升维度（Table 4）。采用FID（越低越好）和APD（越高越好）两个互补指标进行评估，其中APD衡量运动序列内部的帧间差异，FID衡量生成运动与真实数据的分布距离。

![[assets/figures/papers/paper_list_l1774_SIMS_Simulating_Human_Scene_Interactions_with_Real_World_Script_Planning/figures/007_Table_4.jpg]]
*Table 4: Motion diversity results. InterPhys [13] is not released, so we report our re-implemented version here. For fair comparison, our Sit, Lie, and Reach policies are only trained on SAMP [12] here. While the Carry policy and the re-implemented InterPhys are both trained on the carry motions from ViconStyle*

- **Sit技能**：SIMS的FID为125.66，APD为16.55；UniHSI的FID为153.84，APD仅为1.14。APD提升超过14倍，FID降低28.18。
- **Lie技能**：SIMS的FID为171.24，APD为16.40；UniHSI的FID为211.22，APD仅为1.35。APD提升超过11倍。
- **Reach技能**：SIMS的APD为16.67，UniHSI为1.08。

UniHSI的APD值接近1，表明其生成的运动几乎退化为单一模式——这正是其依赖精确参考运动的内在缺陷。SIMS的APD值接近真实数据分布（约16-17），证明多条件策略中的CLIP文本嵌入成功注入了丰富的风格变化，而无需依赖关键帧级别的接触参考。

### 用户研究：情感共鸣与主观体验

用户研究（Table 5）在相同场景和交互类别下，邀请参与者从四个维度对SIMS和UniHSI进行1-5分评分：

![[assets/figures/papers/paper_list_l1774_SIMS_Simulating_Human_Scene_Interactions_with_Real_World_Script_Planning/figures/008_Table_5.jpg]]
*Table 5: User Study on SOTA long-term HSI methods. SIMS outperforms the SOTA method UniHSI by a significant margin*

| 维度 | SIMS | UniHSI | 提升 |
|------|------|--------|------|
| 物理真实感 | 3.4 | 2.6 | +0.8 |
| 运动多样性 | 3.6 | 2.9 | +0.7 |
| 情节吸引力 | 3.0 | 2.4 | +0.6 |
| 情感共鸣 | 3.8 | 3.0 | +0.8 |

SIMS在所有维度上均显著优于UniHSI，尤其在**情感共鸣**上得分最高（3.8），这是RASG生成风格化长脚本的直接体现——角色不仅能完成交互，还能通过身体语言传达“疲惫地坐下”或“兴奋地跳跃”等情感。

### 策略组件消融：文本与场景感知的不可替代性

Table 11对多条件控制策略的关键组件进行了消融实验，揭示了文本嵌入和高度图各自的贡献：

- **移除文本嵌入（w/o text）**：APD从16.55骤降至约4.2（Sit），FID从125.66升至约148。这表明CLIP文本条件是运动多样性的主要驱动力。成功率略有下降（Sit从98.1%降至95.3%），说明文本信号对任务执行也有辅助作用。
- **移除高度图（w/o heightmap）**：成功率严重退化——Sit从98.1%降至约72%，Lie从87.6%降至约58%。FID大幅上升，表明角色失去了场景几何感知后无法准确导航和接触物体。APD变化较小，说明高度图主要影响空间推理而非运动风格。
- **同时移除两者**：所有指标均崩溃至接近UniHSI的水平，验证了多条件设计的完整性。

**因果机制**：文本嵌入通过条件判别器注入风格奖励（$r_t^{\mathrm{style}}$），引导策略探索多样化的运动模式；高度图提供自中心场景几何信息（$12\times12$网格），使策略能够推理障碍物和接触面位置。两者通过奖励分解公式$r_t = \lambda^{\mathrm{style}} r_t^{\mathrm{style}} + \lambda^{\mathrm{task}} r_t^{\mathrm{task}}$协同作用，缺一不可。

### RASG脚本生成消融：检索优于直接生成

Table 6对比了RASG与直接LLM生成长脚本的效果。评估采用SBERT嵌入的余弦相似度衡量生成脚本之间的多样性（相似度越低越多样），以及平均生成时间衡量效率：

- **SBERT相似度**：RASG生成的脚本间相似度显著低于直接LLM生成，表明检索-组合策略有效避免了LLM的冗余生成倾向。
- **生成时间**：RASG通过检索预生成的短脚本库并组合，速度优于LLM从头生成长叙事。

**机制分析**：直接LLM生成在面对“生成一个包含10个以上关键帧的长故事”时，倾向于重复相似的句式、情感和交互模式。RASG通过两阶段检索（语义相似度检索top-k短脚本 + LLM摘要过滤）从多样化短脚本库中挑选并拼接，天然保证了脚本的多样性。短脚本库本身由LLM在可控条件下批量生成，每个短脚本聚焦单一情感和交互逻辑，质量更高。

### 数据集扩展消融：数据多样性的边际收益

Tables 8-10分别对Walk、Carry和HSI（Sit/Lie）技能进行了数据集消融：

- **Walk技能（Table 8）**：在100Style基础上添加AMASS后，成功率从约91%升至约96%，FID从约135降至约118。AMASS提供了更多样化的行走风格和速度变化。
- **Carry技能（Table 9）**：ViconStyle数据集的加入是关键——仅用AMASS时成功率约72%，添加ViconStyle后升至约89%，FID从约180降至约145。ViconStyle提供了高质量的动作捕捉数据，包含真实搬运物体的物理交互。
- **HSI技能（Table 10）**：在SAMP基础上添加COUCH和ViconStyle，Sit成功率从98.1%升至99.5%，Lie从87.6%升至95.8%。COUCH数据集提供了更多样的沙发几何形状，增强了策略对场景变化的泛化能力。

### 失败模式与局限性

尽管SIMS在多项指标上表现优异，分析揭示了以下失败模式和局限：

1. **精细操作缺失**：当前人形模型不包含手指关节，无法模拟抓取、拧转等精细操作。Carry技能通过将物体附着在手上实现，缺乏真实的握持物理。
2. **情感运动数据不足**：Table 2显示，现有数据集（如100Style、AMASS）中的运动大多为中性或简单风格，缺乏“悲伤”、“兴奋”等强烈情感的运动样本。这限制了MotionCLIP嵌入的表达能力，导致某些文本条件（如“悲伤地坐下”）的运动表现不够鲜明。
3. **单角色限制**：框架仅支持单个角色，无法模拟多人协作或社交交互场景。
4. **场景泛化边界**：策略在3DFront上训练，虽然Table 7显示在PartNet上也有一定泛化能力，但成功率有所下降（Sit从98.1%降至约92%），说明对未见家具几何的适应仍有提升空间。

### 重要图表结论总结

- **Figure 3**：定性展示了两个复杂3D场景中生成的长脚本，包含卧室、客厅、餐厅、书房等多房间导航和交互，验证了RASG生成连贯多房间叙事的能力。
- **Figure 4**：展示了不同文本条件下同一技能的运动差异（如“疲惫地坐下” vs “优雅地坐下”），直观证明了文本嵌入的风格控制效果。
- **Table 1**：系统功能对比表明，SIMS是唯一同时具备物理合理性、全自动化、风格多样性、文本感知和场景感知的长期HSI方法。

![[assets/figures/papers/paper_list_l1774_SIMS_Simulating_Human_Scene_Interactions_with_Real_World_Script_Planning/figures/012_Figure_4.jpg]]
*Figure 4: Qualitative results for skills with different text conditions*

![[assets/figures/papers/paper_list_l1774_SIMS_Simulating_Human_Scene_Interactions_with_Real_World_Script_Planning/figures/015_Table_11.jpg]]
*Table 11: Ablation on different policy settings*

## 定位与知识库关联

### 1. 核心瓶颈与因果机制

现有长期人-场景交互（HSI）方法面临一个根本性权衡：**物理合理性**与**风格多样性/自动化程度**难以兼得。基于运动学的方法（如NSM、SAMP、Humanise、AffordMotion、TesMo）虽能生成多样化运动，但普遍存在穿透、滑步等物理误差；基于物理的方法（如UniHSI、InterScene）虽保证物理合理，却高度依赖精确参考运动，导致运动多样性极低，且规划仅限于简单接触序列，无法表达丰富的身体语言和情感。

SIMS通过一个**因果调节旋钮**打破这一僵局：将高层规划与低层控制解耦，并在两个层面分别注入多样性和物理约束。具体而言：
- **高层**：引入检索增强脚本生成（RASG），通过检索预生成的短脚本库并结合场景布局生成长期叙事，解决了直接LLM生成脚本的冗余和多样性不足问题。
- **低层**：设计多条件控制策略，融合场景高度图、任务目标和CLIP文本嵌入，使物理角色能够利用文本嵌入自然表达风格，而无需依赖精确的关键帧或接触参考。
- **衔接层**：有限状态机（FSM）将长脚本解析为可复用的技能调度序列。

核心洞察在于：**RASG的检索机制天然保证了脚本的多样性与连贯性，而多条件策略中的文本嵌入为物理控制器提供了风格感知能力，两者协同实现了“物理合理+风格多样”的统一。**

### 2. 方法对比与定位

Table 1 系统对比了SIMS与现有方法的任务设定差异（详见原表）。以下从关键维度展开：

**与基于运动学方法的对比**：
- NSM、SAMP、Humanise、AffordMotion、TesMo等方法在物理合理性上存在固有缺陷（穿透、滑步），且多数依赖手动规划或无风格多样性。
- SIMS通过物理仿真和自动化脚本生成，在物理合理性、自动化和风格多样性三个维度均实现超越。

**与基于物理方法的对比**：
- **UniHSI**（Xiao et al., CVPR 2024）是物理方法中的SOTA，其控制器仅生成接触序列，缺乏文本感知和风格多样性。Table 3显示，SIMS在Sit和Lie任务上的成功率分别达到98.1%和87.6%，均超越UniHSI（94.3%和81.5%）。更关键的是，Table 4中Sit技能的APD从UniHSI的1.14跃升至16.55，接近真实数据分布，证明了多条件策略在运动多样性上的根本性突破。
- **InterScene**（未开源，本文采用重实现版本）同样缺乏文本感知和风格多样性，SIMS在FID和APD上均显著优于其重实现版本（Table 4）。

**关键改进槽位**：
1. **规划器自动化与风格多样性**：从手动规划/无风格多样性 → RASG自动生成具有情感、风格的多样化长脚本（Table 1, Sec 3.2）。
2. **控制器文本感知能力**：从无文本感知 → 通过CLIP文本嵌入注入风格控制（Table 1, Sec 3.3）。
3. **控制器场景感知能力**：从仅使用位置目标 → 12×12自中心高度图+目标状态，支持复杂3D场景（Table 1, Sec 3.3）。
4. **技能可扩展性**：从多数方法需重新训练整个控制器 → 仅需为新技能训练单独策略并更新脚本库，无需重训整体框架（Sec 9, Fig 6）。

### 3. 适用边界与局限

**当前适用边界**：
- 支持7种核心技能：Walk, Idle, Sit, Lie, Reach, GetUp, Carry，覆盖移动、人-场景交互和动态物体交互三大类。
- 适用于单角色在复杂3D室内场景中的长期日常叙事交互。
- 依赖预定义的短脚本数据库和LLM进行脚本生成，对场景布局和物体语义有明确感知。

**明确局限**（原文自述）：
1. **数据瓶颈**：现有数据集仍缺乏足够多的真实情感和多样风格运动，未来需要更多高质量风格化动捕数据。Table 8-10的消融实验证实，添加AMASS和ViconStyle等数据集可显著提升Walk和Carry技能的成功率和运动多样性，说明当前性能受限于数据规模。
2. **手部缺失**：当前人形模型未包含手指关节，无法模拟精细操作和更丰富的交互（如抓取、使用工具）。
3. **单角色限制**：框架目前仅支持单个角色，未扩展到多智能体人-场景交互。

### 4. 开放问题

1. **数据采集效率**：如何更高效地收集包含真实情感和多样风格的人体运动数据？当前依赖动作捕捉（如ViconStyle数据集），成本高昂且覆盖面有限。
2. **精细操作扩展**：如何将带手指的人形模型引入物理仿真以实现更精细的操作？这涉及高维动作空间的控制和接触建模挑战。
3. **多智能体扩展**：如何将框架扩展到多智能体、多人交互的场景？需要解决角色间协调、碰撞避免和社交规范建模等问题。
4. **MotionCLIP对齐精度**：本文重实现了MotionCLIP用于运动-文本对齐，但未与原版进行定量对比，其对齐精度与原版的差异尚不明确（Sec 8, Fig 7）。

### 5. 证据强度评估

| 主张 | 证据锚点 | 置信度 | 说明 |
|------|----------|--------|------|
| 物理性能超越SOTA | Table 3 | 0.98 | 多技能成功率与接触误差的全面对比，公平性控制良好（相同训练数据） |
| 运动多样性大幅提升 | Table 4 | 0.98 | APD从~1.1提升至16+，FID显著降低，效果明确 |
| RASG优于直接LLM生成 | Table 6 | 0.95 | SBERT相似度更低，生成速度更快，但依赖特定评估指标 |
| 多条件组件必要性 | Table 11 | 0.95 | 消融实验清晰展示文本嵌入和高度图的独立贡献 |
| 用户主观评价优势 | Table 5 | 0.95 | 情感共鸣评分3.8 vs 3.0，但用户研究样本量和统计显著性需查阅原文确认 |

**需手动验证的点**：InterScene重实现版本的公平性（原文未开源，重实现细节需确认）；用户研究的样本量和统计检验方法；MotionCLIP重实现与原版的定量对齐差异。

## 原文 PDF

![[paperPDFs/ICCV_2025/SIMS_Simulating_Human_Scene_Interactions_with_Real_World_Script_Planning.pdf]]
