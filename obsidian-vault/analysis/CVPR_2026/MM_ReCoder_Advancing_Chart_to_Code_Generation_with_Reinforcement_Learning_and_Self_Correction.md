---
title: "MM-ReCoder: Advancing Chart-to-Code Generation with Reinforcement Learning and Self-Correction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MM_ReCoder_Advancing_Chart_to_Code_Generation_with_Reinforcement_Learning_and_Self_Correction.pdf
project_link: "https://zitiantang.github.io/MM-ReCoder"
code_link: null
aliases:
- MR
- MM-ReCoder
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 两阶段多轮自纠正RL策略（基于GRPO）：第一阶段共享首轮输出，仅优化第二轮以增强自纠正能力；第二阶段全轨迹联合优化以提升总体编码质量。配合规则奖励与模型奖励的混合设计。
primary_logic: 通过RL训练让模型在迭代交互中学会利用执行反馈（渲染图像或错误信息）进行有效的代码修正，而非单纯提高可执行率。共享首轮优化鼓励模型探索多样化的修正策略，全轨迹优化则使模型的首轮和次轮能力均衡提升。
claims:
- 现有MLLMs在自纠正中，对已可执行代码的改进为负。
- MM-ReCoder的两阶段RL策略显式地提升了自纠正能力，在共享首轮阶段改善样本比例达14.4%，并且与全轨迹阶段结合后进一步提升。
- MM-ReCoder在ChartMimic上超越ChartCoder 9.1%（低级分），超越GPT-4o和Qwen3-VL-235B-A22B等大模型。
- ChartMimic 上 Low-Level score = 86.5 (4 turns)
---

# MM-ReCoder: Advancing Chart-to-Code Generation with Reinforcement Learning and Self-Correction

> [!tip] 核心洞察
> 通过RL训练让模型在迭代交互中学会利用执行反馈（渲染图像或错误信息）进行有效的代码修正，而非单纯提高可执行率。共享首轮优化鼓励模型探索多样化的修正策略，全轨迹优化则使模型的首轮和次轮能力均衡提升。

| 字段 | 内容 |
|------|------|
| 中文题名 | MM-ReCoder：基于强化学习和自纠正的图表代码生成 |
| 英文题名 | MM-ReCoder: Advancing Chart-to-Code Generation with Reinforcement Learning and Self-Correction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.01600) · [Project](https://zitiantang.github.io/MM-ReCoder) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | MM-ReCoder |
| Dataset | ChartMimic, Plot2Code |

> [!tip] 效果简介
> - ChartMimic 上，Low-Level score 86.5 (4 turns) vs 77.4 (ChartCoder, 1 turn) (+9.1)；High-Level score (GPT-4o) 84.9 (4 turns) vs 74.0 (ChartCoder, 1 turn) (+10.9)。
> - Plot2Code 上，Text-Match score 63.2 (1 turn) vs 54.5 (ChartCoder, 1 turn) (+8.7)；Pass Rate 98.5 (4 turns) vs 87.9 (ChartCoder, 1 turn) (+10.6)。

## 概要

**问题瓶颈**：现有的多模态大语言模型（MLLMs）在图表到代码生成（Chart2Code）任务中普遍缺乏有效的自纠正能力。实验表明，即使允许模型进行第二轮修正，其性能提升主要来自代码可执行率的提高，而非对已可执行代码的精细化改进——在首轮代码已可执行的情况下，第二轮的低级得分反而下降（Qwen3-VL-8B 下降1.03%，Qwen3-VL-235B 下降0.26%）。这说明现有模型无法有效纠正已可执行代码中的视觉细节错误。

**核心方法**：MM-ReCoder 提出了一种基于强化学习的多轮自纠正训练框架。方法以 Qwen2.5-VL-7B 为基础模型，采用两阶段训练策略：首先通过 SFT 冷启动赋予模型基础编码能力，随后引入基于 GRPO 的两阶段多轮自纠正 RL——第一阶段共享首轮输出、仅优化第二轮以增强自纠正能力；第二阶段全轨迹联合优化以提升整体编码质量。奖励设计采用格式奖励、规则低级别奖励与模型高级别奖励的混合机制，以克服单一规则奖励无法捕捉视觉语义缺陷的问题。

**主要结果**：MM-ReCoder 在 ChartMimic 基准上以 86.5% 的低级得分超越 ChartCoder 9.1 个百分点，同时超越 GPT-4o 和 Qwen3-VL-235B-A22B 等大模型；在 Plot2Code 的文本匹配得分上达到 63.2%，可执行率提升至 98.5%。消融实验证实，两阶段 RL 策略是实现有效自纠正的关键——共享首轮优化使 14.4% 的样本获得改进，而单用全轨迹优化则导致 46.9% 的第二轮输出仅为首轮代码的重复。

**方法谱系与知识库定位**：MM-ReCoder 属于图表代码生成领域的 RL 增强方法，其直接对比基线包括基于 SFT 的 **ChartCoder** 以及通用多模态模型 **Qwen3-VL-8B** 和 **Qwen3-VL-235B-A22B**。与依赖单轮 SFT 预测的传统范式不同，MM-ReCoder 将多轮自纠正建模为强化学习问题，通过 GRPO 策略优化使模型学会利用执行反馈进行迭代代码修正。该方法在技术路径上与视觉推理的 RL 训练（如 DeepSeek-R1 的 GRPO 应用）共享优化思想，但将应用场景聚焦于图表渲染代码的结构化生成与视觉细节对齐。

### 任务定义：图表到代码生成

图表到代码生成（Chart-to-Code）要求模型根据输入的图表图像，自动生成能够精确复现该图表的渲染代码。这一任务处于视觉理解与程序合成的交叉点，其核心挑战在于：模型不仅需要识别图表的类型、数据映射、颜色、字体等视觉属性，还必须将这些感知结果转化为语法正确、可执行且视觉上高度保真的代码。当前主流方法通常将图表代码生成建模为单轮预测问题——模型接收图表图像，一次性输出完整的绘图代码。

### 现有方法的瓶颈：自纠正能力的缺失

随着多模态大语言模型（MLLMs）的快速发展，图表代码生成的整体质量已有显著提升。然而，一个关键的瓶颈始终未被有效解决：**现有模型缺乏可靠的自纠正能力**。在多轮交互场景中，模型获得首轮代码的执行反馈（渲染图像或错误信息）后，理论上应当能够据此修正代码中的缺陷。但实证分析揭示了一个令人警醒的现象：现有MLLMs在两轮修正中的得分提升，主要来源于**代码可执行率的提高**——即那些首轮根本无法运行的代码在第二轮变得可以运行。而对于首轮已经可执行的代码，模型的第二轮修正反而导致质量退化。具体而言，Qwen3-VL-8B在已可执行样本上的低级分下降1.03%，Qwen3-VL-235B下降0.26%（Figure 1，Table 3）。这意味着现有模型无法对已经“能跑”的代码进行精细化的视觉细节修正，其所谓的“自纠正”实际上只是从不可执行到可执行的粗粒度修复。

### 问题的根源与本文动机

上述瓶颈的根源在于训练范式的缺失。现有的图表代码生成模型通常仅通过监督微调（SFT）在静态的图表-代码对上进行训练，从未在训练过程中学习如何利用执行反馈来迭代改进代码。因此，当这些模型被置于多轮交互环境中时，它们缺乏将反馈信号转化为有效代码修改的策略能力。

基于这一诊断，本文提出**MM-ReCoder**，其核心动机是：**通过强化学习（RL）显式地训练模型的自纠正能力**，使模型在多轮迭代中学会利用执行反馈进行有效的代码修正，而非仅仅提高可执行率。为此，MM-ReCoder引入了一种两阶段多轮自纠正RL策略（基于GRPO），并配合规则奖励与模型奖励的混合设计，从根本上重塑模型的代码生成与修正行为。

## 核心方法与创新机理

MM-ReCoder 的核心创新在于首次将**多轮自纠正能力显式地注入图表到代码生成（Chart2Code）模型**，通过一套精心设计的两阶段强化学习策略，解决了现有 MLLMs 在自我修正时的根本性缺陷。

### 瓶颈发现：可执行≠可修正

现有 MLLMs（如 **Qwen3-VL-8B** 和 **Qwen3-VL-235B-A22B**，Qwen团队）在多轮 Chart2Code 中虽然能提升总体评分，但这种提升几乎完全来自**代码可执行率的提高**（即把原本跑不起来的代码改到能跑）。一旦限制在首轮代码已可执行的子集上，这些模型的第二轮低级得分反而**下降**：Qwen3-VL-8B 下降 1.03%，Qwen3-VL-235B 下降 0.26%（Figure 1 / Table 3）。这表明它们**无法对已可执行代码中的视觉细节错误进行精细化修正**，其“自纠正”本质上是执行修复而非质量提升。

### 创新一：从 SFT 到多轮自纠正 RL 的训练范式跃迁

传统 Chart2Code 方法（如 **ChartCoder**）依赖图表-代码对上的单轮 SFT，模型只学会了一次性生成，缺乏迭代修正的元能力。MM-ReCoder 将训练范式彻底改写为：

| 训练阶段 | 传统方法 | MM-ReCoder |
|---------|---------|------------|
| **基础编码** | SFT on chart-code pairs | SFT 冷启动（Chart2Code-160k） |
| **多轮能力恢复** | 无 | 7k 自纠正数据上的两轮 SFT |
| **自纠正强化** | 无 | 共享首轮 GRPO 优化（仅优化第二轮） |
| **整体编码提升** | 无 | 全轨迹 GRPO 优化（联合优化两轮） |

这一范式的关键在于：SFT 冷启动赋予基础编码能力，多轮冷启动恢复模型在对话场景下的多轮交互能力，而两阶段 RL 则直接以**自纠正能力本身**为优化目标，而非仅仅追求单轮代码质量。

### 创新二：共享首轮 + 全轨迹的两阶段 RL 策略

这是 MM-ReCoder 实现有效自纠正的**因果开关**。实验证据表明，如果仅使用全轨迹优化（full-trajectory only），模型在第二轮有 46.9% 的概率直接重复首轮代码，实际改进的样本仅占 3.4%（Table 2）。这是因为模型学会了两轮联合优化的“捷径”——直接复制首轮输出以获取稳定奖励，而非真正进行修正。

MM-ReCoder 的两阶段设计破解了这一困境：

- **第一阶段（共享首轮优化）**：固定在线采样的首轮输出，批量生成多个第二轮候选，**仅优化第二轮**。这强制模型在给定相同首轮代码的条件下探索多样化的修正策略，显式强化自纠正能力。消融实验显示，仅此阶段就能在 14.4% 的样本上实现改进，低级分平均提升 0.72%（Table 2）。
- **第二阶段（全轨迹优化）**：同时采样首轮和次轮，联合优化两轮。此时模型已具备自纠正能力，全轨迹优化使其首轮编码和次轮修正能力均衡提升，避免退化为单轮优化。

### 创新三：混合奖励设计解决规则奖励的盲区

ChartMimic 基准提供的规则基低级指标虽然可自动计算，但存在严重盲区：模型生成重叠文本的图表仍能获得满分规则奖励（Figure 3）。MM-ReCoder 引入**模型基高级奖励**作为补充，使用 Qwen2.5-VL-72B 从图表类型、布局、文本、数据、风格、清晰度六个维度评估生成图表与参考图像的一致性。组合奖励形式为：

$$R_{\text{combined}} = (1-\alpha-\beta) \cdot R_{\text{format}} + \alpha \cdot R_{\text{rule}} + \beta \cdot R_{\text{model}}$$

消融实验证实了这一设计的必要性：去除模型奖励使高级别分从 83.7% 降至 78.6%；去除规则奖励使低级别分从 83.9% 降至 78.2%（Table 6）。两种奖励信号互补，规则奖励保证代码的结构准确性，模型奖励捕捉视觉语义的细微差异。

### 创新四：自纠正数据的构造与筛选

多轮冷启动阶段使用的 7k 自纠正数据并非简单收集，而是通过 **Qwen3-VL-235B** 生成两轮修正轨迹，并严格筛选**第二轮低级分至少超过首轮 0.02** 的成功样本。这一过滤策略确保了冷启动数据本身就包含有效的修正模式，为后续 RL 阶段提供了良好的初始化。消融实验表明，若跳过此多轮冷启动，模型在 RL 后无法实现有效的自纠正（Table 5, Table A3）。

### 创新边界与局限

需要注意的是，MM-ReCoder 的自纠正能力存在递减效应：第 4 轮后低级分提升趋于饱和（Table 4）。此外，模型有时在思考 trace 中提出多项修正，但在代码中并未全部实现（思维与代码不一致），且对训练数据中未覆盖的稀有图表类型泛化能力有限。这些限制指向了未来工作方向——如何扩展到更多轮次而不退化，以及如何将这一自纠正 RL 范式迁移到其他视觉编码任务。

MM-ReCoder 的整体训练管道由两个宏观阶段构成：**冷启动（Cold Start）** 与 **多轮自纠正强化学习（Multi-Turn Self-Correction RL）**，如图2所示。冷启动赋予模型基础的图表到代码生成能力与多轮交互能力，RL阶段则通过精心设计的奖励信号和采样策略，显式地训练模型利用执行反馈进行有效的代码修正。

### 冷启动：从单轮编码到多轮自纠正的初始化

冷启动分为两步，旨在为后续RL训练提供一个具备基础编码能力和多轮对话能力的初始策略。

1. **单轮SFT**：在 Chart2Code-160k 数据集上进行标准的监督微调（SFT），输入为图表图像，输出为目标绘图代码。此步赋予模型将视觉图表转换为可执行代码的单轮预测能力。
2. **多轮冷启动**：构建并过滤7k条两轮自纠正数据。具体而言，使用 **Qwen3-VL-235B** (Qwen3-VL) 对首轮生成的代码进行修正，仅保留第二轮低级评分（Low-Level Score）较首轮提升至少0.02的样本。在此过滤数据上进行两轮SFT，恢复模型的多轮对话能力，使其初步学会根据执行反馈（渲染图像或错误信息）修正代码。

需要指出的是，仅靠多轮冷启动无法直接赋予模型有效的自纠正能力——它恢复了多轮格式，但可能因该阶段数据非真实标注（ground truth）而导致单轮性能有所回退。这正是后续RL阶段需要解决的核心问题。

### 多轮自纠正RL：两阶段GRPO策略

在冷启动之后，MM-ReCoder采用基于**组相对策略优化（GRPO）** 的两阶段多轮RL策略，显式地训练模型的自纠正能力。其核心洞察是：现有MLLMs在多轮修正中，得分提升主要来自代码可执行率的提高，而对已可执行代码的精细化改进为负（例如 **Qwen3-VL-8B** 在已可执行样本上的低级分下降1.03%，**Qwen3-VL-235B** 下降0.26%）。MM-ReCoder的RL设计正是为了解决这一瓶颈。

RL阶段包含两个互补的优化步骤：

1. **共享首轮优化（Shared-First-Turn Optimization）**：对于每个输入，首先在线采样一个共享的首轮输出 $o^{(1)}$ 及其执行反馈 $f^{(1)}$，然后基于此共享上下文批量生成 $G$ 个第二轮候选 $o_i^{(2)}$。此阶段**仅优化第二轮输出的策略**，目标函数为：
   $$ \mathcal { I } _ { G R P O } ^ { ( s h a r e d ) } ( \theta ) = \mathbb { E } \left[ \frac { 1 } { G } \sum _ { i = 1 } ^ { G } \frac { \pi _ { \theta } \bigl ( o _ { i } ^ { ( 2 ) } \vert { q } , { o } ^ { ( 1 ) } , { f } ^ { ( 1 ) } \bigr ) } { \mathrm { S G } \bigl [ \pi _ { \theta } \bigl ( o _ { i } ^ { ( 2 ) } \vert { q } , { o } ^ { ( 1 ) } , { f } ^ { ( 1 ) } \bigr ) \bigr ] } A _ { i } \right] $$
   固定首轮输出迫使模型专注于学习多样化的修正策略，而非依赖改变首轮代码来获取高分。实验表明，该阶段使14.4%的样本得到改善，平均低级分提升0.72%。

2. **全轨迹优化（Full-Trajectory Optimization）**：同时采样首轮和次轮输出，联合优化两轮策略。其GRPO目标扩展为：
   $$ \mathcal { I } _ { G R P O } ^ { ( f u l l ) } ( \theta ) = \mathbb { E } \Bigg [ \frac { 1 } { G } \sum _ { i = 1 } ^ { G } \frac { \pi _ { \theta } \big ( o _ { i } ^ { ( 1 ) } | q \big ) \pi _ { \theta } \big ( o _ { i } ^ { ( 2 ) } | q , o _ { i } ^ { ( 1 ) } , f _ { i } ^ { ( 1 ) } \big ) } { \mathrm { S G } \big [ \pi _ { \theta } \big ( o _ { i } ^ { ( 1 ) } | q \big ) \pi _ { \theta } \big ( o _ { i } ^ { ( 2 ) } | q , o _ { i } ^ { ( 1 ) } , f _ { i } ^ { ( 1 ) } \big ) \big ] } A _ { i } \Bigg ] $$
   轨迹奖励由三项组成：
   $$ R ( o _ { i } ^ { ( 1 ) } , o _ { i } ^ { ( 2 ) } ) = R ( o _ { i } ^ { ( 2 ) } ) + \gamma \cdot R ( o _ { i } ^ { ( 1 ) } ) + \eta \cdot \mathbf { B } ( R ( o _ { i } ^ { ( 1 ) } ) , R ( o _ { i } ^ { ( 2 ) } ) ) $$
   其中 $\gamma$ 为首轮奖励折扣因子（最终设定 $\gamma=0$，仅以最终轮奖励计算），$\eta \cdot \mathbf{B}(\cdot)$ 为鼓励第二轮超越首轮的提升奖励。此阶段使模型的首轮编码能力和次轮修正能力均衡提升，避免了单独使用全轨迹优化时模型在第二轮重复首轮代码（46.9%重复率）且改善样本仅3.4%的退化现象。

### 奖励设计：规则与模型的混合信号

RL训练的奖励函数由三部分加权组合：
$$ \text{Total Reward} = (1-\alpha-\beta) \cdot \text{Format} + \alpha \cdot \text{Rule-based} + \beta \cdot \text{Model-based} $$

- **格式奖励（Format Reward）**：若输出遵循 `<think>...</think>```python...``` 的结构则为1，否则为0。
- **规则基奖励（Rule-based Reward）**：复用 ChartMimic 的低级评测指标，精确衡量代码渲染结果与目标图表在像素级的匹配程度。
- **模型基奖励（Model-based Reward）**：使用 **Qwen2.5-VL-72B** 作为奖励模型，从图表类型、布局、文本、数据、风格和清晰度六个维度对渲染图像进行评分（总分100，缩放到 $[0,1]$）。该奖励的关键作用在于惩罚规则奖励无法捕获的视觉缺陷——例如，仅用规则奖励训练的模型可能生成文本重叠的图表但仍获满分（图3），而模型奖励能有效抑制此类问题。

消融实验证实了混合奖励的必要性：去除模型奖励使高级别分从83.7%降至78.6%，去除规则奖励使低级别分从83.9%降至78.2%。两阶段RL策略与混合奖励设计的协同，构成了MM-ReCoder实现有效自纠正的核心机制。

![[assets/figures/papers/paper_list_l2695_https_arxiv_org_abs_2604_01600/figures/002_Figure_2.jpg]]
*Figure 2: Training pipeline of MM-ReCoder. We first conduct two stages of cold start: (a) we first train the model on ground truth chartcode pairs with SFT, then (b) we construct self-correction data with Qwen3VL-235B [31], filter the successful ones, and train our model on the filtered data. After cold start, we conduct two stages of reinforcement learning: (c) we first enhance the model’s self-correction capability in the second turn via shared-first-turn optimization, then (d) we optimize the two turns jointly to improve the coding ability*

### 问题形式化与多轮自纠正框架

MM-ReCoder 将图表到代码生成建模为一个多轮交互过程。给定输入图表图像 $q$，模型首轮采样代码 $o^{(1)} \sim \pi_{\theta}(\mathcal{O} | q)$，随后执行该代码并获取反馈 $f^{(1)}$（渲染图像或错误信息）。第二轮，模型基于反馈进行修正，采样 $o^{(2)} \sim \pi_{\theta}(\mathcal{O} | q, o^{(1)}, f^{(1)})$。该框架的核心瓶颈在于：现有 MLLM 在首轮代码已可执行时，第二轮的低级得分反而下降（Qwen3-VL-8B 下降 1.03%，Qwen3-VL-235B 下降 0.26%），说明其缺乏对已可执行代码的精细化自纠正能力。MM-ReCoder 通过 RL 训练使模型在迭代交互中学会利用执行反馈进行有效修正，而非仅提高可执行率。

### 训练管道：冷启动与两阶段 RL

MM-ReCoder 的训练管道分为冷启动和两阶段多轮自纠正 RL 两个阶段（图 2）。

**冷启动阶段**包含两步：首先在 Chart2Code-160k 数据集上进行单轮 SFT，赋予模型基础的图表编码能力；随后使用 Qwen3-VL-235B 生成并过滤的 7k 两轮自纠正数据进行多轮 SFT，恢复模型的多轮对话能力。过滤标准为第二轮低级别分至少比首轮提升 0.02，确保数据中的第二轮确实实现了有效修正。

**RL 阶段**基于 Group Relative Policy Optimization (GRPO) 进行两阶段优化：
1. **共享首轮优化**：固定在线采样的首轮输出 $o^{(1)}$ 和反馈 $f^{(1)}$，批量生成 $G$ 个第二轮候选输出，仅优化第二轮策略以强化自纠正能力。
2. **全轨迹优化**：同时采样首轮和次轮，联合优化两轮以提升整体编码水平。

### 奖励设计

RL 奖励由三部分组合而成：

$$R = (1-\alpha-\beta) \cdot R_{\text{format}} + \alpha \cdot R_{\text{rule}} + \beta \cdot R_{\text{model}}$$

- **格式奖励** $R_{\text{format}}$：输出符合 `<think>...</think>```python...``` 格式则为 1，否则为 0。
- **规则基低级别奖励** $R_{\text{rule}}$：复用 ChartMimic 的低级规则指标（如颜色、位置、文本等精确匹配）。
- **模型基高级别奖励** $R_{\text{model}}$：使用 Qwen2.5-VL-72B 作为奖励模型，从图表类型、布局、文本、数据、样式、清晰度六个维度评估生成图表与参考图像的一致性，满分 100 分后缩放到 $[0,1]$。

模型奖励的必要性体现在：仅使用规则奖励训练的模型可能生成重叠文本但仍获得满分（图 3），而模型奖励能够有效惩罚此类视觉缺陷。消融实验（Table 6）表明，去除模型奖励使高级别分从 83.7% 降至 78.6%，去除规则奖励使低级别分从 83.9% 降至 78.2%，验证了混合奖励的必要性。

### 核心公式

**单轮 GRPO 目标函数**：

$$\mathcal{I}_{GRPO}(\theta) = \mathbb{E}\left[ \frac{1}{G} \sum_{i=1}^{G} \frac{\pi_{\theta}(o_i | q)}{\mathrm{SG}[\pi_{\theta}(o_i | q)]} A_i \right]$$

其中 $G$ 为每组采样数，$\mathrm{SG}[\cdot]$ 为 stop-gradient 操作。优势函数 $A_i$ 基于组内奖励归一化计算：

$$A_i = \frac{R(o_i) - \mathrm{mean}(\{R(o_1), R(o_2), \cdots, R(o_G)\})}{\mathrm{std}(\{R(o_1), R(o_2), \cdots, R(o_G)\})}$$

**共享首轮 GRPO 目标**（仅优化第二轮）：

$$\mathcal{I}_{GRPO}^{(shared)}(\theta) = \mathbb{E}\left[ \frac{1}{G} \sum_{i=1}^{G} \frac{\pi_{\theta}(o_i^{(2)} | q, o^{(1)}, f^{(1)})}{\mathrm{SG}[\pi_{\theta}(o_i^{(2)} | q, o^{(1)}, f^{(1)})]} A_i \right]$$

**全轨迹 GRPO 目标**（联合优化两轮）：

$$\mathcal{I}_{GRPO}^{(full)}(\theta) = \mathbb{E}\left[ \frac{1}{G} \sum_{i=1}^{G} \frac{\pi_{\theta}(o_i^{(1)} | q) \pi_{\theta}(o_i^{(2)} | q, o_i^{(1)}, f_i^{(1)})}{\mathrm{SG}[\pi_{\theta}(o_i^{(1)} | q) \pi_{\theta}(o_i^{(2)} | q, o_i^{(1)}, f_i^{(1)})]} A_i \right]$$

**轨迹奖励**：

$$R(o_i^{(1)}, o_i^{(2)}) = R(o_i^{(2)}) + \gamma \cdot R(o_i^{(1)}) + \eta \cdot \mathbf{B}(R(o_i^{(1)}), R(o_i^{(2)}))$$

其中 $\gamma$ 为首轮奖励折扣因子，$\eta \cdot \mathbf{B}(\cdot)$ 为鼓励第二轮超越首轮的提升奖励项。实验表明 $\gamma=0$（仅计算最终轮奖励）时性能最佳。

### 两阶段 RL 策略的关键作用

Table 2 的对比实验揭示了策略设计的因果机制：
- 单用全轨迹优化会导致第二轮 46.9% 的样本直接重复首轮代码，改进样本仅占 3.4%，模型未学会有效自纠正。
- 引入共享首轮优化后，改进样本比例提升至 14.4%，平均低级别提升 0.72%，显式地赋予了模型自纠正能力。
- 两阶段结合（共享首轮 + 全轨迹）使模型的首轮和次轮能力均衡提升，最终在 ChartMimic 上实现 86.5% 的低级分（4 轮），超越 ChartCoder 9.1 个百分点。

## 实验与关键发现

### 核心瓶颈的实证验证：现有MLLM的自纠正悖论

在构建MM-ReCoder之前，作者首先对现有MLLM的多轮自纠正行为进行了诊断性实验，揭示了一个关键悖论：**现有模型的第二轮得分提升几乎完全来自代码可执行率的提高，而非对视觉细节的精细化修正**。

具体而言，**Qwen3-VL-8B**（Qwen3-VL, 2024）在两轮交互间的整体低级分提升为1.5%，**Qwen3-VL-235B-A22B**（Qwen3-VL, 2024）提升0.4%。然而，当分析限定在首轮代码已可执行的样本时，两个模型的低级分均出现退化——Qwen3-VL-8B下降1.03%，Qwen3-VL-235B下降0.26%（Figure 1, Table 3）。这说明现有模型在接收到执行反馈后，不仅无法纠正已可执行代码中的视觉细节错误，反而可能引入新的退化。这一发现直接定义了本文的核心挑战：**如何让模型真正学会利用执行反馈进行有效的代码修正**。

![[assets/figures/papers/paper_list_l2695_https_arxiv_org_abs_2604_01600/figures/005_Table_3.jpg]]
*Table 3: Self-correction capability of MM-ReCoder and baselines*

### 主要结果：跨基准的综合优势

Table 1汇总了MM-ReCoder在ChartMimic、Plot2Code和ChartX三个基准上的表现。在**ChartMimic**上，MM-ReCoder以4轮自纠正取得86.5%的低级分，超越图表领域SFT模型**ChartCoder**（单轮77.4%）达9.1个百分点；高级分（GPT-4o评估）领先ChartCoder 10.9个百分点（84.9% vs. 74.0%）。在**Plot2Code**的文本匹配分上，MM-ReCoder以单轮63.2%超越ChartCoder 8.7个百分点，4轮可执行率达到98.5%。值得注意的是，MM-ReCoder不仅在同等规模模型中表现最优，在ChartMimic低级分和Plot2Code文本匹配分上甚至超越了**GPT-4o**和**Qwen3-VL-235B-A22B**等更大规模模型。

相较于基础模型**Qwen2.5-VL-7B**（Qwen2.5-VL, 2024），MM-ReCoder在ChartMimic上的可执行率提升29%、低级分提升48%、高级分提升63%，表明RL训练带来的增益远超SFT冷启动的贡献。

### 自纠正能力的量化分析

Table 3从平均改进、改进比例和退化比例三个维度量化了模型的自纠正能力。MM-ReCoder在两轮间实现0.72%的平均低级分改进，改进样本占比14.4%，退化样本仅占5.0%。相比之下，基线的改进几乎为零甚至为负：Qwen3-VL-8B平均改进仅0.02%，退化比例高达8.5%；Qwen3-VL-235B改进0.03%，退化6.5%。这证实了**两阶段RL策略是赋予模型正向自纠正能力的关键**。

Table 4进一步考察了多轮迭代自纠正的收益边界。低级分从第1轮到第2轮提升最为显著，随后增益递减：第2→3轮、第3→4轮仍有正向改进，但第4→5轮提升趋于饱和。这表明**4轮是当前策略下性价比最优的配置**。

### 两阶段RL策略的消融：共享首轮是关键

Table 2对比了不同RL训练策略对自纠正能力的影响。若仅使用**全轨迹优化**（full-trajectory），模型在第二轮有46.9%的概率直接重复首轮代码，改进样本仅占3.4%，平均低级分改进为0.14%——几乎未获得自纠正能力。引入**共享首轮优化**（shared-first-turn）后，改进比例跃升至14.4%，重复率大幅下降。两阶段结合（先共享首轮、后全轨迹）实现了最佳的改进/退化平衡。

这一消融揭示了因果机制：全轨迹优化同时优化两轮，模型倾向于在两轮间保守地复用代码以降低风险；共享首轮优化通过固定首轮输出、仅优化第二轮，强制模型在给定首轮代码的条件下探索多样化的修正策略，从而**解耦了“编码能力”与“修正能力”的优化**。

### 奖励设计的消融：规则与模型奖励互补

Table 6在单轮RL设定下消融了奖励权重。联合使用规则奖励（α）与模型奖励（β）是必要的：去除模型奖励（β=0）使高级分从83.7%骤降至78.6%；去除规则奖励（α=0）使低级分从83.9%降至78.2%。Figure 3给出了一个定性案例：仅用规则奖励训练的模型生成了文本重叠的图表却仍获得满分，而模型奖励能够有效惩罚此类视觉缺陷。这验证了**规则奖励保障代码正确性与可执行性，模型奖励保障视觉质量**的分工设计。

### 冷启动的必要性

Table 5展示了各训练阶段后的性能变化。单轮SFT冷启动（Chart2Code-160k）使低级分从基础模型的约58%提升至约75%，但此时模型不具备多轮能力。多轮冷启动（7k自纠正数据）恢复了多轮对话能力，但性能有所回退，因为该阶段数据并非真实标注。Table A3的消融进一步表明：**若跳过单轮SFT冷启动或仅使用多轮冷启动，RL后模型的自纠正能力显著下降**，说明单轮编码能力是多轮修正的基础。

### 失败模式分析

Table A6统计了自纠正的三种失败模式频率：（1）**诊断错误**——模型未能正确识别首轮代码的问题；（2）**编码错误**——模型识别出问题但修正代码存在缺陷；（3）**回归**——第二轮代码引入了新的错误。其中编码错误占比最高，说明模型在“知道错在哪”与“写出正确修正”之间仍存在能力鸿沟。此外，作者指出模型有时在思考trace中提出多项修正，但在代码中并未全部实现，存在**思维与代码不一致**的问题。对于训练数据中未覆盖的稀有图表类型，模型的泛化能力依然有限（Figure A10）。

![[assets/figures/papers/paper_list_l2695_https_arxiv_org_abs_2604_01600/figures/030_Figure.jpg]]
*Figure: A10. Failure cases of MM-ReCoder and baselines. The models tend to fail when the chart type is rare*

![[assets/figures/papers/paper_list_l2695_https_arxiv_org_abs_2604_01600/figures/006_Table_2.jpg]]
*Table 2: Comparison of RL strategies for self-correction. Our two-stage strategy enables self-correction capability while the others cannot*

![[assets/figures/papers/paper_list_l2695_https_arxiv_org_abs_2604_01600/figures/010_Table_6.jpg]]
*Table 6: Ablation on RL reward weights. Model training and inference are single-turn without self-correction*

![[assets/figures/papers/paper_list_l2695_https_arxiv_org_abs_2604_01600/figures/014_Table.jpg]]
*Table: A4. Ablation on the reward model under the single-turn RL setting. Qwen2.5-VL-7B as the reward model is able to improve the high-level score on ChartMimic, but replacing Qwen2.5- VL-7B with Qwen2.5-VL-72B can further boost the model*

## 定位与知识库关联

### 1. 方法沿革与基线关系

图表到代码（Chart-to-Code）生成任务要求模型从图表图像中提取视觉编码信息并生成可执行的绘图代码。早期工作主要依赖单轮监督微调（SFT），将图表-代码对作为训练数据，使模型学会从图像到代码的直接映射。代表性工作包括 **ChartCoder**，其在 Chart2Code-160k 数据集上进行 SFT 训练，在 ChartMimic 和 Plot2Code 基准上取得了当时同规模模型的最佳结果。然而，这类单轮方法存在一个根本性瓶颈：模型缺乏对生成代码进行自我审视和修正的能力——一旦首轮输出存在视觉细节错误，模型无法利用执行反馈进行改进。

MM-ReCoder 正是在这一瓶颈上展开工作。其核心洞察来自对现有多模态大模型（MLLMs）自纠正行为的分析（Figure 1）：即使允许模型进行第二轮修正，现有 MLLMs 的提升主要来自代码可执行率的提高（即首轮不可执行的代码在第二轮变得可执行），而非对已可执行代码的精细化改进。在首轮代码已可执行的样本上，**Qwen3-VL-8B**的低级得分反而下降 1.03%，**Qwen3-VL-235B-A22B**下降 0.26%——这表明现有模型无法纠正已可执行代码中的视觉细节错误。这一发现直接驱动了 MM-ReCoder 的设计目标：通过强化学习（RL）训练，让模型在迭代交互中学会利用执行反馈（渲染图像或错误信息）进行有效的代码修正。

在方法谱系上，MM-ReCoder 可定位为 **SFT + 多轮自纠正 RL** 的混合范式。与纯 SFT 方法（如 ChartCoder）相比，MM-ReCoder 引入了基于 GRPO 的两阶段多轮 RL 训练；与通用 MLLMs 的简单多轮推理（如 Qwen3-VL 的多轮对话）相比，MM-ReCoder 通过专门的 RL 策略显式地优化了自纠正能力。MM-ReCoder 还构建了单轮 RL 基线 **MM-ReCoder-Single**，使用相同的主干网络和冷启动数据，仅在单轮设定下进行 RL 训练，用于隔离多轮自纠正策略的贡献。

### 2. 训练范式对比

| 维度 | ChartCoder (SFT) | Qwen3-VL (通用多轮) | MM-ReCoder (本文) |
|------|-----------------|-------------------|-------------------|
| 训练范式 | 单轮 SFT | 预训练 + 指令微调 | SFT 冷启动 + 两阶段多轮 RL |
| 自纠正能力 | 无专门训练 | 依赖模型固有泛化 | 通过 RL 显式优化 |
| 多轮数据 | 无 | 通用对话数据 | 7k 过滤的自纠正数据 |
| 奖励信号 | 仅交叉熵损失 | 无 RL 阶段 | 规则奖励 + 模型奖励 + 格式奖励 |
| 已可执行代码的改进 | — | 负改进（-1.03% / -0.26%） | 正改进 |

### 3. 关键设计选择与消融证据

MM-ReCoder 的 RL 策略设计经过了系统的消融验证，以下选择具有决定性作用：

**两阶段 RL 策略的必要性。** 若仅使用全轨迹优化（full-trajectory optimization）而不经过共享首轮优化（shared-first-turn optimization），模型在第二轮有 46.9% 的概率直接重复首轮代码，改进样本比例仅 3.4%（Table 2）。共享首轮阶段通过固定首轮输出、仅优化第二轮，鼓励模型探索多样化的修正策略，使改进样本比例提升至 14.4%，平均低级改进达 0.72%。两阶段结合后，改进样本比例进一步提升。

**混合奖励设计的必要性。** 仅使用规则奖励训练会导致模型利用奖励函数的盲区——例如生成重叠文本但仍获得满分（Figure 3）。消融实验（Table 6）表明：去除模型奖励使高级别分从 83.7% 降至 78.6%；去除规则奖励使低级别分从 83.9% 降至 78.2%。组合奖励 `(1-α-β)*Format + α*Rule-based + β*Model-based` 是平衡可执行性与视觉保真度的关键。

**多轮冷启动的必要性。** 仅经过单轮 SFT 冷启动的模型在 RL 后无法实现有效的自纠正（Table 5, Table A3）。7k 自纠正数据的多轮冷启动恢复了模型的多轮对话能力，尽管该阶段因数据非真实标注而导致性能暂时下降，但其为后续 RL 阶段的自纠正能力涌现提供了必要基础。

### 4. 适用边界与局限

**思维与代码不一致。** MM-ReCoder 有时在思考 trace（`<think>...</think>`）中提出多项修正，但在实际代码中并未全部实现。这表明模型的推理与执行之间存在鸿沟，自纠正的可靠性仍有提升空间。

**稀有图表类型的泛化有限。** 失败案例分析（Figure A10）显示，当图表类型在训练数据中覆盖不足时，MM-ReCoder 和基线模型均容易出现错误。方法的泛化能力受限于冷启动数据的分布。

**自纠正收益递减。** 多轮自纠正实验（Table 4）表明，收益随轮次增加而递减，第 4 轮后低级提升趋于饱和，且可能出现回归。这意味着在实际部署中，2-4 轮是性价比最优的配置。

**计算资源需求高。** RL 训练需要 16×8 H200 GPU 进行训练，外加 4×8 H200 服务奖励模型（Qwen2.5-VL-72B）。对于资源受限的场景，这一门槛可能过高。

### 5. 开放问题

1. **更多轮次的自纠正**：当前方法在 4 轮后趋于饱和，是否可以设计新的 RL 策略或奖励机制来扩展有效自纠正的轮次而不发生退化？

2. **跨任务迁移**：MM-ReCoder 的两阶段自纠正 RL 策略是否能够迁移到其他视觉编码任务？论文提及网页代码生成和 SVG 生成为潜在方向，但尚无实验验证。

3. **轻量级奖励模型**：消融实验（Table A4）表明 Qwen2.5-VL-72B 作为奖励模型优于 7B 版本，但 72B 模型的部署成本较高。能否使用 7B 模型通过额外的校准或蒸馏达到相近效果，同时避免低级别分的下降？

4. **冷启动数据的必要性边界**：Table A3 显示完全不使用多轮冷启动数据时模型性能显著下降，但能否通过调整 RL 策略（如更长的 warm-up、不同的 KL 约束）来降低对冷启动数据的依赖，使方法更轻量化？

5. **失败模式的结构化理解**：Table A6 统计了自纠正的失败模式（诊断错误、编码错误、回归），但未深入分析每种模式的成因。理解这些失败模式的根本原因可能指导下一阶段的算法改进。

## 原文 PDF

![[paperPDFs/CVPR_2026/MM_ReCoder_Advancing_Chart_to_Code_Generation_with_Reinforcement_Learning_and_Self_Correction.pdf]]
