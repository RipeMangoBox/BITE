---
title: "Exploring Synthesizable Chemical Space with Iterative Pathway Refinements"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Exploring_Synthesizable_Chemical_Space_with_Iterative_Pathway_Refinements.pdf
openreview_forum_id: aQKVfKOkR5
aliases:
- ESCSIPR
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "双向合成路径表示与迭代精炼（自底向上解码、自顶向下解码和整体编辑）的组合，使得模型能够系统性地在可合成空间中搜索相似物。"
primary_logic: "将合成路径生成视为双向搜索问题，通过单一自回归模型实现bottom-up和top-down双向采样，并引入基于Edit Flow的整体编辑（Edit Bridge）进行精炼，从而显著提升对可合成空间的覆盖率。"
claims:
- "ReaSyn在Enamine数据集上的重建率达到95.0%，远超SynFormer（66.3%）和SynNet（25.2%）。"
- "在引入未见构建块的ZINC250k测试集上，ReaSyn的重建率为87.9%，而SynFormer仅为18.0%，显示了强大的泛化能力。"
- "双向迭代精炼（BU+TD+EB）在消融研究中显著优于单向生成或仅BU+TD。"
- "Edit Bridge耦合相比空耦合或均匀耦合大幅减少编辑操作数（30 vs 94.6/142.9），且对齐率高达70.56%。"
---

# Exploring Synthesizable Chemical Space with Iterative Pathway Refinements

> [!tip] 核心洞察
> 将合成路径生成视为双向搜索问题，通过单一自回归模型实现bottom-up和top-down双向采样，并引入基于Edit Flow的整体编辑（Edit Bridge）进行精炼，从而显著提升对可合成空间的覆盖率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过迭代路径精炼探索可合成化学空间 |
| 英文题名 | Exploring Synthesizable Chemical Space with Iterative Pathway Refinements |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=aQKVfKOkR5); [GitHub](https://github.com/NVIDIA-Digital-Bio/ReaSyn) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | ReaSyn |
| Dataset | Enamine REAL diversity set, ZINC250k reconstructed molecules (ZINC1k), JNK3 hit expansion |

> [!tip] 效果简介
> - Enamine REAL diversity set 上，Reconstruction rate (%) 为 95.0 ± 0.0，对比 66.3 ± 0.6 (SynFormer)，变化 +28.7%。
> - ZINC250k reconstructed molecules (ZINC1k) 上，Reconstruction rate (%) 为 87.9 ± 0.2，对比 18.0 ± 1.2 (SynFormer)，变化 +69.9%。
> - JNK3 hit expansion 上，Analog rate (%) 为 75.7 ± 1.8，对比 61.7 ± 11.2 (SynFormer)，变化 +14.0%。

## 概述

### 问题瓶颈

现代药物发现高度依赖虚拟筛选与分子生成，但绝大多数分子生成模型产出的候选分子缺乏合成路径保证，即**可合成性**成为从计算设计走向实验验证的关键断层。现有可合成分子生成方法（如**SynNet**、**SynFormer**）在以下方面存在根本性不足：其一，生成时仅沿单一方向（自底向上或自顶向下）遍历合成树，难以充分探索可合成化学空间；其二，对未见过的新构建块泛化能力极弱，导致在大规模构建块库上的覆盖率严重不足；其三，缺乏系统性的路径精炼机制，生成路径的质量和多样性受限。

### 核心方法定位

**ReaSyn** 是一种迭代式生成路径精炼框架，将可合成分子生成问题重新定义为**合成路径的双向搜索与整体编辑**。其核心设计包含三个关键创新：

1. **统一的双向路径表示**：摒弃传统方法中构建块指纹与反应类型分离的层次化编码，采用基于SMILES的统一词汇表直接表示合成路径，使单一序列即可支持自底向上（BU）和自顶向下（TD）两种遍历方向。

2. **单模型双向生成**：通过特定的训练与推理方案（在推理时偏置首个token的logit），使单个编码器-解码器Transformer同时掌握BU和TD两个方向的生成能力，在保持内存效率的同时实现双向探索。

3. **Edit Bridge整体编辑**：引入一种基于Edit Flow的离散流模型，对自回归模型生成的路径进行全序列级别的编辑操作（插入、删除、替换），将生成结果从模型分布桥接到真实数据分布，实现路径的整体精炼。

ReaSyn的生成周期由三步迭代构成：**BU解码 → TD解码 → Edit Bridge编辑**，通过多轮循环逐步逼近目标分子的最优可合成类似物。

### 主要结果

在可合成分子重建这一核心基准上，ReaSyn展现出压倒性优势：

- **Enamine REAL多样性测试集**：重建率达 **95.0%**，远超SynFormer的66.3%和SynNet的25.2%。
- **ZINC250k测试集（含未见构建块）**：重建率达 **87.9%**，而SynFormer仅18.0%，体现了强大的分布外泛化能力。
- **JNK3点击扩展任务**：类似物生成率达 **75.7%**，较SynFormer提升14个百分点。

消融实验证实，双向迭代（BU+TD）相比单向生成显著提升性能，而Edit Bridge的加入进一步带来实质性增益。在目标导向分子优化任务（TDC oracles、sEH代理）中，ReaSyn同样取得最优结果。

### 局限与待解决问题

ReaSyn目前未集成选择性、官能团兼容性等更高层次的化学约束，限制了其在精细药物化学场景中的直接应用。Edit Bridge的训练依赖大规模预生成数据（1050万样本）和大量计算资源（120块GPU训练约3天），部署成本较高。此外，模型对构建块库的依赖意味着当库存发生重大变化时，泛化能力仍需进一步提升。如何在动态更新的构建块库和大规模反应集上高效扩展，以及如何降低Edit Bridge的推理开销，是后续研究的重要方向。

## 背景与动机

### 可合成化学空间探索的核心瓶颈

药物发现和分子优化的核心挑战之一，是在广阔的化学空间中高效搜索具有理想性质的分子。然而，一个分子无论性质多么优越，若无法在实验室中实际合成，其价值便大打折扣。因此，**可合成化学空间**——即所有可通过已知反应规则和商业可用构建块（building blocks）合成的分子集合——成为分子生成和优化研究的焦点。

现有方法在探索可合成化学空间时面临两个根本性瓶颈。第一个瓶颈是**可合成性保证的缺失**。大量分子生成模型（如基于图的生成模型、SMILES生成模型）直接输出分子结构，但无法保证生成分子落于可合成空间之内。即使采用后验的合成可及性评分（Synthesis Accessibility, SA）进行过滤，也无法从根本上解决生成-合成之间的鸿沟。

第二个瓶颈是**可合成空间的覆盖率严重不足**。少数方法通过直接生成合成路径来确保可合成性，例如 **SynNet** 和 **SynFormer** 采用自底向上（bottom-up）的合成树生成策略。然而，这些方法在导航大规模可合成空间时存在严重局限：当测试集引入训练阶段未见过的构建块时，重建率急剧下降。例如，SynFormer在Enamine数据集上的重建率为66.3%，但在引入未见构建块的ZINC250k测试集上骤降至18.0%（Table 1）。这揭示了现有方法对**新构建块泛化能力**的根本缺陷。

### 现有方法的表示与搜索局限

从表示层面看，现有合成路径生成方法普遍采用层次化的后序表示（postfix notation），将构建块编码为Morgan指纹，反应类型单独编码。这种表示存在两个问题：（1）Morgan指纹的离散性和稀疏性使得模型难以平滑地泛化到未见构建块；（2）层次化的编码方式限制了模型对合成树结构的灵活操作。

从搜索策略看，现有方法几乎全部采用单向生成——要么仅自底向上（从构建块到最终产物），要么仅自顶向下（从产物逆向分解）。单向搜索限制了模型对合成路径空间的探索范围，无法系统性地在目标分子附近寻找可合成的相似物（analogs）。此外，现有方法缺乏有效的路径精炼（refinement）机制，通常仅依赖束搜索（beam search）的重复采样，无法对已生成的合成路径进行结构层面的整体优化。

### 本文动机：双向迭代精炼框架

针对上述瓶颈，本文提出 **ReaSyn**——一个通过**迭代路径精炼**探索可合成化学空间的框架。ReaSyn的核心动机来自以下观察：可合成投影（synthesizable projection）——即寻找一个合成路径，使其最终产物与目标分子尽可能相似——本质上是一个**双向搜索问题**。自底向上搜索可以从构建块出发探索可合成的产物空间，而自顶向下搜索可以从目标分子出发约束搜索方向。两者结合，辅以整体性的路径编辑，有望系统性地提升对可合成空间的覆盖。

具体而言，ReaSyn的设计围绕三个关键动机展开：

1. **统一的双向路径表示**：提出一种简单的序列化表示，用SMILES直接表示构建块，反应类型为单一token，使得单一模型能够同时支持自底向上和自顶向下的合成树遍历。

2. **迭代精炼机制**：设计一个包含三步的迭代精炼周期——自底向上解码生成初始合成树、自顶向下解码重新预测子树、以及基于Edit Bridge的整体路径编辑——通过多轮迭代逐步逼近最优的可合成相似物。

3. **整体性路径编辑**：引入Edit Flow的离散流模型，在全序列级别上对合成路径进行插入、删除和替换操作，形成从自回归模型输出分布到真实数据分布的“编辑桥接”（Edit Bridge），从而在结构层面精炼合成路径。

## 核心创新

### 瓶颈与动机

现有分子生成模型面临两个紧密耦合的挑战。其一，生成分子的可合成性缺乏保证——模型输出的分子结构可能在化学上合理，但无法通过已知反应和市售构建块实际合成。其二，即使限制在可合成化学空间内，现有方法在大规模搜索时的**覆盖率严重不足**。以最新方法 **SynFormer** 为例，其在 Enamine REAL 多样性集上的重建率仅为 66.3%，而在引入未见构建块的 ZINC250k 测试集上更是骤降至 18.0%（Table 1）。这意味着当目标分子需要调用训练时未见过的构建块时，现有模型几乎完全失效——这是药物发现中 hit-to-lead 优化的典型场景，因为先导化合物优化天然要求探索新颖的化学结构。

### 核心洞察：合成路径生成即双向搜索

ReaSyn 的核心洞察在于将合成路径生成重新定义为**双向搜索问题**。合成树天然具有两种遍历方向：从叶子（构建块）到根（产物）的自底向上（bottom-up）遍历，以及从根到叶子的自顶向下（top-down）遍历。传统方法（如 SynNet、SynFormer）仅采用单一方向生成，这相当于在巨大的可合成空间中仅沿一条路径移动，极易陷入局部区域。ReaSyn 的关键创新是让**单一自回归模型同时掌握两种遍历方向**，并在推理时交替使用，从而系统性地在可合成空间中导航。

### 方法谱系与知识库定位

ReaSyn 处于可合成分子生成与分子优化方法的交叉点。其方法谱系可追溯至两条主线：

- **合成路径生成方法**：SynNet 首次将合成路径表示为树结构并用自回归模型生成，但采用层次化表示（构建块用 Morgan 指纹编码，反应类型单独分类）。SynFormer 在此基础上引入 Transformer 架构，但保留了层次化表示和单向生成。ReaSyn 在表示层和生成策略上同时突破，用统一的 SMILES 词汇表替代层次化编码，并用单一模型实现双向生成。

- **可合成投影方法**：ChemProjector 将任意分子投影到可合成空间，但依赖预定义的合成规则和模板匹配，灵活性有限。ReaSyn 通过生成式建模实现投影，天然支持多样化的合成路径发现。

在分子优化领域，ReaSyn 可作为遗传算法（Graph GA）的变异算子，将不可合成的后代分子投影回可合成空间，形成 **Graph GA-ReaSyn** 组合方法。这与 Graph GA-SF（使用 SynFormer 作为投影器）形成直接对比。

### 关键 changed slots

ReaSyn 相对于基线方法（以 SynFormer 为主要对比对象）在四个维度上做出了实质性改变：

#### 1. 路径表示：从层次化指纹到统一 SMILES 词汇表

SynFormer 采用双层序列表示：token 类型层（`[BB]` 或 `[RXN]`）和 token 特征层（Morgan 指纹或反应类别），需要在每个自回归步骤中分层嵌入和生成。这种层次化设计带来两个问题：一是需要多个分类头分别预测 token 类型和特征，增加了模型复杂度；二是 Morgan 指纹的离散化表示导致构建块空间不平滑，相似的构建块可能具有差异巨大的指纹表示。

ReaSyn 的表示方案彻底简化了这一设计（Figure 7）：构建块直接用 SMILES 字符串表示，反应类型为单 token，所有 token 共享统一词汇表。这一改变使得：
- 自回归生成简化为标准的 next-token prediction，无需多分类头
- SMILES 表示天然平滑——结构相似的构建块具有相似的 SMILES 序列
- 自底向上序列 $p_{\text{BU}}$ 和自顶向下序列 $\bar{p}_{\text{TD}}$ 互为逆序，可由同一词汇表表示

#### 2. 生成方向：从单向到双向统一模型

这是 ReaSyn 最具辨识度的创新。传统方法或仅支持自底向上生成（SynNet），或需要两个独立模型分别处理不同方向。ReaSyn 通过**训练-推理联合设计**实现了单一模型的双向生成能力：

- **训练阶段**：以 50% 概率随机切换训练序列为 $p_{\text{BU}}$ 或 $p_{\text{TD}}$，模型学习两种遍历方向的联合分布
- **推理阶段**：通过偏置第一个 token 的 logit 来控制生成方向——自底向上时强制首个 token 为构建块，自顶向下时强制首个 token 为反应类型

消融实验（Table 6, Table 7）证实：双向训练模型与两个独立单向模型性能无显著差异，但内存效率更高；而双向推理（BU+TD 迭代）相比单向推理（仅 BU 或仅 TD）性能提升显著（Figure 4）。

#### 3. 精炼机制：迭代周期与 Edit Bridge 整体编辑

ReaSyn 的生成不是一次性的，而是通过**迭代精炼周期**逐步逼近目标分子（Figure 2b）。单个周期包含三步：

1. **自底向上解码**：自回归模型从构建块出发，生成初始合成树
2. **自顶向下解码**：随机选择一个子树，自回归模型以自顶向下方向重新预测该子树
3. **整体编辑**：Edit Bridge 模型接收自回归模型生成的完整路径，通过编辑操作在全序列级别进行精炼

第三步是 ReaSyn 独有的机制。传统方法的"精炼"仅限于束搜索的重复采样，缺乏对已生成路径的结构化修正能力。Edit Bridge 的设计动机在于：自回归模型生成的路径虽然合理，但可能存在次优的树骨架（反应连接方式）或语义（构建块选择），这些缺陷难以通过局部重新采样修复。

#### 4. 整体编辑：基于 Edit Flow 的 Edit Bridge

Edit Bridge 是 ReaSyn 在精炼层面的核心贡献。它将编辑操作建模为离散流（discrete flow）过程，支持三种原子操作：**插入**（在路径中插入新构建块或反应）、**删除**（移除冗余节点）、**替换**（更换构建块或反应类型）。关键设计在于**耦合策略**（Table 8）：

- **空耦合**（从空序列开始编辑）：需要平均 142.9 步编辑操作
- **均匀耦合**（随机初始化序列）：需要 94.6 步
- **Edit Bridge 耦合**（从自回归模型生成的序列出发）：仅需 **30 步**，且对齐率高达 **70.56%**

Edit Bridge 耦合的本质是将自回归模型的输出作为"桥接"分布的样本，使离散流过程从接近数据分布的位置出发，大幅降低了编辑难度。这种设计使得 Edit Bridge 能够在有限的计算预算内（推理时仅采样少量编辑轨迹）实现有效的整体精炼。

### 证据强度与待验证点

- **强证据**：Table 1 中 Enamine（95.0% vs. 66.3%）和 ZINC1k（87.9% vs. 18.0%）的重建率对比直接验证了双向生成和精炼机制的有效性。Figure 4 的消融实验清晰展示了 BU+TD+EB 相对于单向生成和 BU+TD 的增益。
- **中等证据**：Edit Bridge 耦合的优势（Table 8）基于训练数据的平均编辑步数统计，其在推理时的实际收益需要结合 Table 1 的端到端结果间接推断。
- **待验证**：双向训练模型与两个独立模型的性能等价性（Table 7）仅在重建率指标上验证，在其他任务（如分子优化）上的表现差异未充分探索。

## 整体框架

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_aQKVfKOkR5/figures/002_Figure_2.jpg]]
*Figure 2: (a) Bottom-up and top-down traversal of a synthetic tree. (b) Overall framework of ReaSyn. ReaSyn’s generation cycle consists of three steps. First, an initial synthetic tree is generated by the autoregressive model in a bottom-up direction. Next, the autoregressive model repredicts a randomly selected subtree in a top-down direction. Finally, the Edit Flow model refines the generated tree in a holistic manner. This process can be repeated multiple times, and the best pathway that yields a product molecule of the highest similarity to the given target molecule is selected as the final solution. The sampling processes of the autoregressive model (the first and the second steps) and the Edit...*

ReaSyn 是一个将输入分子投影到可合成化学空间的迭代生成式路径精炼框架。其核心目标是为任意输入分子 $\mathbf{x}$ 寻找一条合成路径 $\mathbf{p}^*$，使得该路径的终产物与 $\mathbf{x}$ 的相似度最大化：

$$
\mathbf{p}^{*} = \underset{\mathbf{p}}{\mathrm{argmax}} \ \mathrm{sim}(\mathrm{prod}(\mathbf{p}), \mathbf{x})
$$

为实现这一目标，ReaSyn 的生成周期由三个核心步骤构成，形成一个闭环的迭代精炼过程（图 2(b)）：

1. **自底向上解码（Bottom-up Decoding）**：自回归模型从叶节点（构建块）出发，向根节点（最终产物）方向生成初始合成树。
2. **自顶向下解码（Top-down Decoding）**：在已有合成树中随机选取一个子树，自回归模型从根向叶方向重新预测该子树的结构。
3. **整体编辑（Holistic Editing）**：Edit Bridge 模型接收自回归模型生成的完整路径序列，通过编辑操作（插入、删除、替换）在序列级别进行整体精炼，同时调整树的骨架结构和语义内容。

这三个步骤可以重复多轮，最终选择产物分子与目标分子相似度最高的路径作为输出。

### 模块组成与数据流

ReaSyn 的 pipeline 由以下关键模块串联构成：

**Encoder-Decoder Transformer（自回归模型）**：采用编码器-解码器 Transformer 架构（图 3(a)）。编码器将输入分子编码为隐表示，解码器以自回归方式生成合成路径序列。该模型通过统一的词汇表直接使用 SMILES 表示构建块，反应类型以单 token 编码，消除了先前方法中分层嵌入和独立分类头的复杂性。训练时以 0.5 的概率随机切换自底向上和自顶向下两种路径表示，使单一模型同时掌握双向生成能力。推理时通过偏置第一个 token 的 logit 来控制生成方向。

**Edit Bridge 模型（离散流）**：基于 Edit Flow 的离散扩散模型，接收自回归模型输出的路径序列作为源分布样本，通过编辑操作桥接到数据分布（图 3(b)）。Edit Bridge 的关键设计在于耦合策略——将自回归模型生成的样本与目标序列配对，而非使用空序列或均匀噪声作为起点。这一耦合使训练时平均编辑操作数从 142.9（均匀耦合）降至 30，对齐率高达 70.56%（Table 8），显著提升了精炼效率。

**构建块检索模块**：基于 Morgan 指纹相似度从构建块库中检索最近邻构建块，相似度函数定义为：

$$
\mathrm{sim}(\mathbf{x}, \mathbf{x}') = \frac{1}{\mathrm{dist}(\mathbf{x}, \mathbf{x}') + 0.1}
$$

该模块在自回归模型的块级生成过程中提供候选构建块，引导搜索方向。

**束搜索推理引擎**：引导自回归模型的块级生成过程，结合相似度评分和反应概率进行束搜索，在可合成空间中高效导航。

### 迭代精炼的因果机制

ReaSyn 性能提升的核心在于双向迭代与整体编辑的协同作用。消融实验（Figure 4）表明：仅使用单向生成（BU 或 TD）时重建率有限；引入双向迭代（BU+TD）后性能显著提升；进一步加入 Edit Bridge 整体编辑（BU+TD+EB）后达到最优。这种设计使得模型能够在可合成空间中系统性地“行走”——自底向上探索可能的构建块组合，自顶向下修正子树结构，整体编辑则消除序列级别的局部不一致性，从而大幅提升对可合成空间的覆盖率和泛化能力。

## 核心模块与公式推导

### 可合成投影问题的形式化

ReaSyn 将可合成投影定义为一个优化问题：给定目标分子 $\pmb{x}$，在可合成化学空间中寻找一条合成路径 $\pmb{p}$，使得该路径的最终产物与目标分子的相似度最大化：

$$\pmb { p } ^ { * } = \underset { \pmb { p } } { \mathrm { a r g m a x } } \ \mathrm { s i m } ( \mathrm { p r o d } ( \pmb { p } ) , \pmb { x } )$$

其中 $\mathrm{prod}(\pmb{p})$ 表示沿合成路径 $\pmb{p}$ 执行所有反应后得到的产物分子，$\mathrm{sim}(\cdot, \cdot)$ 为分子相似度度量。这一公式构成了 ReaSyn 所有模块设计的核心目标（Eq. 1）。

### 双向序列化路径表示

ReaSyn 的核心创新之一是用统一的序列化表示替代传统方法中层次化的后序表示（Figure 7）。给定一棵合成树，其自底向上（Bottom-up, BU）路径序列定义为：

$$\pmb{p}_{\mathrm{BU}} := \pmb{p}^{1} \oplus \pmb{p}^{2} \oplus \cdots \oplus \pmb{p}^{B}$$

其中每个 $\pmb{p}^{i}$ 可以是一个构建块（用 SMILES 表示）或一个反应（用单个 token 表示），$\oplus$ 表示序列拼接。对应的自顶向下（Top-down, TD）路径序列则通过反转 BU 序列得到：

$$\bar{\pmb{p}}_{\mathrm{TD}} := \pmb{p}^{B} \oplus \pmb{p}^{B-1} \oplus \dots \oplus \pmb{p}^{1}$$

这一表示的关键优势在于：（1）构建块直接使用 SMILES 表示，避免了 Morgan 指纹带来的离散化信息损失；（2）采用统一词汇表，无需为 token 类型、反应类别和构建块指纹分别设计分类头；（3）BU 和 TD 序列共享相同的词汇表和序列结构，使得单个模型即可处理双向生成。

### 自回归模型与加权训练损失

ReaSyn 采用 Encoder-Decoder Transformer 架构（Figure 3）。编码器接收输入分子 $\pmb{x}$，解码器以自回归方式生成合成路径序列。训练时，模型以 0.5 的概率随机在 BU 和 TD 两种路径表示之间切换，从而在单一模型中同时学习双向生成能力。

为平衡路径中构建块（分子 token）与反应 token 的学习，ReaSyn 引入了加权 token 预测损失：

$$\mathcal { L } = - \underset { \underset { p \sim \{ p _ { \mathrm { B U } } , p _ { \mathrm { T D } } \} } { \mathbb { E } } } { \mathbb { E } } \left[ \frac { 1 } { | \mathcal { T } _ { \mathrm { m o l } } | } \sum _ { i \in \mathcal { I } _ { \mathrm { m o l } } } \log \pi _ { \theta } ( p _ { i } | \pmb { x } , p _ { 1 : i - 1 } ) + \frac { 1 } { | \mathcal { T } _ { \mathrm { o t h e r } } | } \sum _ { j \in \mathcal { I } _ { \mathrm { o t h e r } } } \log \pi _ { \theta } ( p _ { j } | \pmb { x } , p _ { 1 : j - 1 } ) \right]$$

其中 $\mathcal{T}_{\mathrm{mol}}$ 和 $\mathcal{T}_{\mathrm{other}}$ 分别表示分子 token 和其他 token（反应、特殊标记）的索引集合。通过对两类 token 分别取平均后再求和，该损失函数有效缓解了因构建块 token 数量远多于反应 token 而导致的学习不平衡问题（Eq. 2）。

推理时，通过偏置第一个 token 的 logit 来控制生成方向：强制以构建块 token 开始则触发 BU 解码，以反应 token 开始则触发 TD 解码。这一设计使得单个模型无需额外结构即可实现双向采样。

### Edit Bridge 整体编辑模块

自回归模型生成的路径可能存在局部次优问题。为此，ReaSyn 引入了 Edit Bridge——一种基于离散流（Edit Flow）的全序列编辑机制（Figure 3(b)）。Edit Bridge 接收自回归模型生成的完整路径序列，通过三种编辑操作（插入、删除、替换）在 token 级别进行整体精炼，同时修改合成树的骨架结构和语义内容。

Edit Bridge 的关键在于耦合设计：将自回归模型的输出样本与目标序列进行配对，形成从预训练分布到数据分布的“桥接”。实验表明，Edit Bridge 耦合相比空耦合或均匀耦合大幅减少了训练时的编辑操作数（30 vs 94.6/142.9），且对齐率高达 70.56%（Table 8），显著提升了精炼效率。

### 构建块检索与推理引擎

在推理阶段，ReaSyn 使用基于 Morgan 指纹的最近邻检索来获取候选构建块。给定目标分子 $\pmb{x}$ 和候选构建块 $\pmb{x}'$，相似度定义为：

$$\sin ( { \pmb x } , { \pmb x } ^ { \prime } ) = \frac { 1 } { \operatorname { d i s t } ( { \pmb x } , { \pmb x } ^ { \prime } ) + 0 . 1 }$$

其中 $\mathrm{dist}(\cdot, \cdot)$ 为 Morgan 指纹间的距离度量（Eq. 6）。束搜索推理引擎利用该相似度评分和反应概率共同引导自回归模型的块级生成。

### 迭代精炼周期

ReaSyn 的完整生成周期由三个步骤组成（Algorithm 1, Figure 2）：（1）自回归模型以 BU 方向生成初始合成树；（2）随机选择一个子树，以 TD 方向重新预测；（3）Edit Bridge 对整条路径进行整体编辑。该周期可重复多次，最终选择产物与目标分子相似度最高的路径作为输出。消融实验（Figure 4）证实，BU+TD 双向迭代相比单向生成已带来显著提升，而加入 Edit Bridge（BU+TD+EB）后性能进一步提升，验证了三个模块的协同作用。

## 实验与分析

### 核心发现：ReaSyn在可合成空间覆盖率上实现数量级突破

ReaSyn在多项基准测试中展现出对可合成化学空间的系统性覆盖优势，其核心性能提升源于双向路径表示与迭代精炼机制的协同作用。

**可合成分子重建任务**是验证模型对可合成空间覆盖能力的最直接测试。在Enamine REAL多样性数据集上，ReaSyn以**95.0%**的重建率显著超越SynFormer（66.3%）和SynNet（25.2%）（Table 1）。更关键的是泛化能力测试：在引入未见构建块的ZINC1k测试集上，ReaSyn重建率达**87.9%**，而SynFormer骤降至18.0%（Table 1, Figure 1）。这一近70个百分点的差距揭示了ReaSyn的核心能力——通过双向迭代搜索，模型能够在新构建块空间中有效导航，而非简单记忆训练分布。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_aQKVfKOkR5/figures/004_Table_1.jpg]]
*Table 1: Synthesizable molecule reconstruction results. The results are the means and the standard deviations of 3 runs. The best results are highlighted in bold*

在ChEMBL测试集上，ReaSyn同样以33.0%的重建率优于ChemProjector（27.3%）和SynNet（19.7%），且生成分子的Tanimoto相似度（0.588）和构建块多样性（0.576）均达到最高（Table 2）。这表明ReaSyn在保持高重建精度的同时，并未牺牲搜索的多样性。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_aQKVfKOkR5/figures/005_Table_2.jpg]]
*Table 2: Synthesizable molecule reconstruction results with the ChEMBL test set in Luo et al. (2024). The results of SynNet (Gao et al., 2021) and ChemProjector (Luo et al., 2024) are taken from Luo et al. (2024)*

### 消融实验：双向迭代与整体编辑的因果贡献

消融研究（Figure 4）系统拆解了ReaSyn各组件的贡献：

- **单向生成 vs 双向迭代**：单独使用bottom-up（BU）或top-down（TD）解码时，重建率显著低于BU+TD组合。这验证了核心假设——合成路径搜索本质上是双向问题，单一方向遍历会陷入局部最优。
- **Edit Bridge的增量收益**：在BU+TD基础上加入Edit Bridge整体编辑（BU+TD+EB），性能进一步提升。Edit Bridge的作用机制在于对自回归模型生成的完整路径序列进行联合编辑（插入、删除、替换），纠正树骨架和语义层面的不一致。
- **统一模型 vs 分离模型**：使用单一自回归模型同时支持BU和TD采样的方案，与训练两个分离模型相比性能无显著差异（Table 7），但内存效率更高，验证了统一架构的实用性。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_aQKVfKOkR5/figures/012_Table_7.jpg]]
*Table 7: Synthesizable molecule reconstruction results of ReaSyn that uses two separate autoregressive models for BU and TD and ReaSyn that uses a single autoregressive model that does both BU and TD sampling*

Edit Bridge的耦合策略消融（Table 8）进一步解释了其效率优势：与空耦合（142.9步）或均匀耦合（94.6步）相比，Edit Bridge耦合将训练时平均编辑操作数降至**30.0步**，且对齐率高达**70.56%**。这意味着通过将自回归模型的输出与目标序列智能配对，Edit Bridge大幅缩短了从生成分布到数据分布的桥接路径。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_aQKVfKOkR5/figures/013_Table_8.jpg]]
*Table 8: Comparison of different couplings of Edit Flow. The values are the average of 10,000 random training data*

### 目标导向优化：可合成约束下的性能验证

在TDC oracle优化任务中，将ReaSyn作为遗传算法的变异算子（Graph GA-ReaSyn）后，平均AUC top-10达到0.633，超越所有基于合成的方法基线（Table 3）。在sEH结合亲和力优化任务中，ReaSyn在所有指标（结合亲和力、SA分数、QED、AiZynthFinder成功率）上均优于先前方法（Table 4）。值得注意的是，ReaSyn生成的分子保持了较高的合成可及性（SA分数），避免了传统分子优化中常见的“不可合成高分分子”陷阱。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_aQKVfKOkR5/figures/008_Table_4.jpg]]
*Table 4: Synthesizable goal-directed molecular optimization results on the sEH proxy. The results are the means and the standard deviations of 3 runs. The results for the baselines are taken from Cretu et al. (2025). The best results are highlighted in bold. Table 5: JNK3 hit expansion results. The results are the means and the standard deviations of 3 runs. The best results are highlighted in bold*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_aQKVfKOkR5/figures/007_Table_3.jpg]]
*Table 3: Synthesizable goal-directed molecular optimization results on the TDC oracles. The results are the means of AUC top-10 and average top-10 SA scores of 3 runs. The results for the baselines other than Graph GA-SF and Graph GA are taken from Sun et al. (2025). The best synthesis-based results are highlighted in bold*

### 命中物扩展：可合成类似物的高效发现

在JNK3命中物扩展任务中，ReaSyn的类似物生成率达**75.7%**，显著高于SynFormer的61.7%（Table 5）。Figure 5的分布图显示，ReaSyn生成的类似物在JNK3抑制活性和结构相似度两个维度上均展现出更优的Pareto前沿。Figure 6和Figure 10的示例表明，ReaSyn能够对输入命中物的特定子结构进行修饰，同时保持合成路径的可行性。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_aQKVfKOkR5/figures/009_Figure_5.jpg]]
*Figure 5: The distribution of JNK3 scores and analog similarity of SynFormer and ReaSyn. Figure 6: Examples of generated synthesizable analogs from JNK3 hit expansion. Modified substructures in the analogs are indicated by red*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_aQKVfKOkR5/figures/017_Figure_10.jpg]]
*Figure 10: Examples of hit molecules and generated synthesizable analogs by ReaSyn in JNK3 hit expansion. JNK3 inhibition score measured by the JNK3 proxy and similarity to the input hit are provided at the bottom of each generated analog*

### 失败模式与局限性

尽管ReaSyn在可合成空间覆盖率上取得显著进展，仍需注意以下局限：

1. **化学兼容性约束缺失**：模型未考虑选择性、官能团兼容性等更高层次的药物化学要求，生成的类似物可能需要额外的化学过滤。
2. **Edit Bridge的训练成本**：Edit Bridge依赖大量预生成数据（10.5M样本）和计算资源（120块GPU训练约3天），部署门槛较高。
3. **构建块库依赖性**：模型使用固定反应集和构建块集，当构建块库存发生重大变化时，泛化能力可能下降。ZINC1k实验虽展示了初步泛化能力，但大规模动态更新的构建块库场景仍需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_aQKVfKOkR5/figures/011_Table_6.jpg]]
*Table 6: Reconstruction rate (%) results in synthesizable molecule reconstruction with different train/inference schemes*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_aQKVfKOkR5/figures/014_Table_9.jpg]]
*Table 9: Reconstruction rate (%) results in synthesizable molecule reconstruction of AiZynthFinder (Genheden et al., 2020) and ReaSyn. The results are the means and the standard deviations of 3 runs. The best results are highlighted in bold*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

ReaSyn 处于**可合成分子生成**与**合成路径规划**的交叉点，其核心贡献在于将合成路径生成重新定义为双向搜索问题，并通过迭代精炼机制系统性地扩展对可合成空间的覆盖。

**相对于合成路径生成方法**：早期工作如 **SynNet** 采用层次化表示，将构建块编码为 Morgan 指纹、反应类型单独分类，以自底向上（bottom-up）方式逐层构建合成树。**SynFormer** 在此基础上引入 Transformer 架构，但仍沿用类似的层次化序列表示。ReaSyn 的关键突破在于三点：（1）**统一词汇表表示**——直接用 SMILES 表示构建块，将反应类型简化为单一 token，消除了层次化解码中的多分类头设计（Figure 7）；（2）**双向生成**——单一自回归模型通过训练时随机切换方向（概率 0.5）和推理时偏置首个 token logit，同时支持 bottom-up 和 top-down 采样，而此前方法仅支持单向遍历；（3）**迭代精炼**——引入 Edit Bridge 整体编辑机制，对自回归模型生成的完整路径序列进行插入、删除、替换操作，形成 BU→TD→EB 的闭环精炼周期（Figure 2b）。

**相对于可合成投影方法**：**ChemProjector** 通过学习从分子到合成路径的映射实现可合成投影，但其路径表示和生成方向均受限。ReaSyn 在 ChEMBL 测试集上的重建率达到 33.0%，而 ChemProjector 仅为 18.0%（Table 2），表明双向迭代精炼在跨数据集泛化上具有显著优势。

**相对于逆合成规划方法**：传统逆合成工具如 **AiZynthFinder** 从目标分子出发递归分解为可用构建块，其搜索空间受限于单次逆向推理。ReaSyn 将其纳入对比（Table 9），结果显示 ReaSyn 的重建率远超 AiZynthFinder，验证了双向生成+整体编辑在探索可合成空间上的有效性。

**相对于分子优化方法**：在目标导向优化任务中，ReaSyn 被集成为遗传算法（Graph GA）的变异算子，将每一代后代分子投影到可合成空间。这种“生成后投影”的策略使 Graph GA-ReaSyn 在 TDC oracles 上达到平均得分 0.633，优于所有基于合成的方法（Table 3），并在 sEH 结合亲和力优化中全面领先（Table 4）。

### 2. 适用边界

**强适用场景**：
- **可合成分子重建**：当目标分子本身可由给定构建块库和反应集合成时，ReaSyn 的双向搜索能高效找到对应路径（Enamine 数据集上 95.0% 重建率）。
- **hit 扩展**：在 JNK3 抑制剂扩展任务中，ReaSyn 生成类似物的比例达 75.7%，且保持了较高的结构多样性（Figure 5），适合先导化合物优化中的骨架跃迁需求。
- **大规模构建块库导航**：统一词汇表和束搜索推理引擎使 ReaSyn 能在包含数十万构建块的库中有效检索和组合。

**弱适用或需谨慎的场景**：
- **构建块库剧烈变化**：当构建块库存发生重大更新时，模型对未见构建块的泛化虽优于 SynFormer（ZINC1k 上 87.9% vs 18.0%），但仍存在性能下降，需重新训练或微调。
- **高精度化学约束**：ReaSyn 未显式建模选择性、官能团兼容性等药物化学家关注的精细约束，生成分子可能在实际合成中遇到副反应或选择性不足的问题。
- **反应规则固定**：模型依赖预定义的反应模板集，无法发现或利用新型化学反应。

### 3. 局限与开放问题

**已确认的局限**：
1. **训练成本高**：Edit Bridge 的训练需预生成 10.5M 样本，并使用 120 块 GPU 训练约 3 天，部署门槛较高。
2. **推理计算开销**：完整迭代周期包含自回归解码（束搜索）+ Edit Bridge 编辑，每轮均需多次前向传播，在需要高通量筛选的场景中可能成为瓶颈。
3. **化学约束缺失**：未考虑选择性、特定官能团兼容性等更高层次约束，限制了在精细药物设计中的应用。

**开放问题**：
- 能否将选择性、官能团兼容性等约束编码为 Edit Bridge 编辑操作中的额外条件或奖励信号，实现约束感知的精炼？
- 在保持编辑质量的前提下，能否通过知识蒸馏或编辑操作剪枝降低 Edit Bridge 的推理开销？
- 如何设计增量学习策略，使 ReaSyn 在构建块库动态更新时无需完全重新训练？
- ReaSyn 的双向迭代框架是否可扩展到更大规模的反应模板集（如 USPTO 全量模板）和百万级构建块库？

## 原文 PDF

![[paperPDFs/ICLR_2026/Exploring_Synthesizable_Chemical_Space_with_Iterative_Pathway_Refinements.pdf]]
