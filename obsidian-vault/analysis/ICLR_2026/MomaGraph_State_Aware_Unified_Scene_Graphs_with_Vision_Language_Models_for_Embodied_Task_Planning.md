---
title: "MomaGraph: State-Aware Unified Scene Graphs with Vision-Language Models for Embodied Task Planning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MomaGraph_State_Aware_Unified_Scene_Graphs_with_Vision_Language_Models_for_Embodied_Task_Planning.pdf
project_link: https://HybridRobotics.github.io/MomaGraph/
code_link: null
openreview_forum_id: 3eTr9dGwJv
aliases:
- MR
- MomaGraph
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过引入统一空间-功能关系的任务导向场景图（MomaGraph），并将其作为中间表示进行 Graph-then-Plan，同时利用精心设计的图对齐奖励函数和 DAPO 强化学习训练 VLM 生成该图，可显著提升规划质量。"
primary_logic: "将场景理解与动作规划解耦，先显式构建一个融合空间与功能信息、包含零件节点且任务相关的场景图，再基于该图进行零样本规划，能够大幅提高规划的准确性与鲁棒性，尤其在多步、需要预条件推理和动态调整的任务中效果突出。"
claims:
- "Graph-then-Plan 在所有模型上一致优于直接规划，证明结构化场景表示对下游规划具有显著增益。"
- "统一空间-功能图优于单一关系图（仅空间或仅功能），验证了两类关系互补的必要性。"
- "RL 训练相比 SFT 和 ICL 大幅提升场景图生成质量和规划表现。"
- "MomaGraph-R1 在开源模型中取得最优，达到与闭源巨模型 GPT-5 等相当的性能。"
---

# MomaGraph: State-Aware Unified Scene Graphs with Vision-Language Models for Embodied Task Planning

> [!tip] 核心洞察
> 将场景理解与动作规划解耦，先显式构建一个融合空间与功能信息、包含零件节点且任务相关的场景图，再基于该图进行零样本规划，能够大幅提高规划的准确性与鲁棒性，尤其在多步、需要预条件推理和动态调整的任务中效果突出。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MomaGraph：面向具身任务规划的状态感知统一场景图与视觉-语言模型 |
| 英文题名 | MomaGraph: State-Aware Unified Scene Graphs with Vision-Language Models for Embodied Task Planning |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=3eTr9dGwJv) · [Project](https://HybridRobotics.github.io/MomaGraph/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | MomaGraph-R1 |
| Dataset | MomaGraph-Bench, BLINK (visual correspondence), MomaGraph-Bench (correspondence subset) |

> [!tip] 效果简介
> - MomaGraph-Bench 上，Overall Accuracy (%) 为 71.6 (MomaGraph-R1 w/ Graph)，对比 60.2 (Qwen2.5-VL-7B w/ Graph)，变化 +11.4。
> - MomaGraph-Bench 上，Overall Accuracy (%) - best closed source 为 71.6，对比 73.9 (Claude-4.5-Sonnet w/ Graph)，变化 -2.3。
> - BLINK (visual correspondence) 上，Accuracy (%) 为 63.5 (MomaGraph-R1)，对比 58.7 (Qwen2.5-VL-7B-Instruct)，变化 +4.8。

## 概要

具身任务规划要求机器人理解场景中的物体、部件及其空间与功能关系，并据此生成可执行的动作序列。然而，现有方法面临一个关键瓶颈：场景图通常将空间关系与功能关系分离处理，忽略零件级交互元素和物体状态的时间变化，且与当前任务的相关性不足，导致规划缺乏可靠的结构化知识基础。

MomaGraph 针对上述问题提出了一个统一框架，其核心思想是将场景理解与动作规划解耦——先显式构建一个融合空间与功能信息、包含零件节点且任务相关的场景图，再基于该图进行零样本规划。这一 **Graph-then-Plan** 范式使规划过程能够建立在精确、结构化的中间表示之上，从而大幅提升准确性与鲁棒性，尤其在多步、需要预条件推理和动态调整的任务中效果突出。

具体而言，方法层面的关键创新包括：

- **统一空间-功能场景图**：首次将空间关系（如“在……上面”、“在……左边”）与功能关系（如“打开”、“插入”）统一建模为有向边，并引入零件级交互节点，显式捕捉物体的可操作部件。
- **强化学习训练与图对齐奖励**：基于 Qwen2.5-VL-7B-Instruct 骨干，采用 DAPO 强化学习算法训练 VLM 生成场景图，配合精心设计的加权奖励函数——组合动作类型预测、边语义相似度（空间+功能）、节点 IoU、格式验证和长度惩罚，引导模型输出高质量的结构化表示。
- **状态感知动态更新**：在执行动作后，根据观察到的新状态更新场景图中的功能假设，消除歧义并维持图表示的时间一致性。

实验表明，MomaGraph-R1 在 MomaGraph-Bench 基准上达到 71.6% 的整体准确率，较其基础模型 Qwen2.5-VL-7B 提升 11.4 个百分点，性能与闭源巨模型 GPT-5（71.6%）持平，接近 Claude-4.5-Sonnet（73.9%）。消融实验进一步验证：统一空间-功能图在所有模型上一致优于仅空间或仅功能的单一关系图（如 MomaGraph-R1 统一图 71.6 vs 仅空间 59.9、仅功能 64.9），证明两类关系互补的必要性；RL 训练相比 SFT（63.9）和 ICL（60.2）带来显著增益。在真实机器人实验中，系统在多步长程家庭任务上取得 70% 的总成功率，验证了方法的实用性与鲁棒性。

当前方法仍存在若干局限：评估局限于单房间场景，多视角图像需人工采集，动态更新依赖实际执行而非反事实推理，且仅输出高层动作序列而未生成低层控制命令。这些方向为后续工作留下了明确的拓展空间。



具身任务规划要求机器人在复杂环境中理解场景、推理物体间关系，并生成可执行的动作序列。现有方法通常采用端到端的直接规划范式，即从多视角图像和语言指令直接预测动作序列。然而，这种范式存在一个根本性瓶颈：**场景理解与动作规划被隐式耦合，缺乏显式的结构化中间表示来桥接感知与决策**。

具体而言，当前场景图方法面临三重缺陷：

1. **关系分离**：空间关系（如“在左侧”“在下方”）与功能关系（如“可打开”“可插入”）通常被独立建模，但真实任务往往需要同时推理两类关系。例如，要“打开微波炉”，机器人既需要知道把手在微波炉的**空间位置**（空间关系），也需要理解把手是微波炉的**可操作部件**（功能关系）。

2. **忽略零件级交互**：现有场景图多以物体为节点粒度，缺失对零件级交互元素（如把手、按钮、盖子）的显式建模。然而，大多数操作任务恰恰发生在零件层面，而非物体整体层面。

3. **状态变化缺失**：场景图通常是静态的，不随任务执行而更新。当机器人执行动作后，环境状态发生变化（如抽屉被打开、灯被关闭），静态图无法反映这种动态演变，导致后续规划缺乏最新的环境知识。

这些缺陷共同导致直接规划在需要多步推理、预条件判断和动态调整的长程任务上频繁失败。如 Figure 2 所示，即使强大的闭源模型 GPT-5，在直接规划时也会产生错误动作或遗漏关键步骤。

为突破上述瓶颈，本文提出核心洞见：**将场景理解与动作规划解耦**——先显式构建一个融合空间与功能信息、包含零件节点且任务相关的场景图，再基于该图进行零样本规划。这种 Graph-then-Plan 范式将结构化场景图作为感知与决策之间的中间表示，使规划器能够基于可靠的结构化知识进行推理，而非从原始像素和指令中隐式猜测。



## 核心方法与创新机理

MomaGraph 的核心创新在于将具身任务规划从“端到端黑箱推理”重构为“结构化中间表示 + 零样本规划”的两阶段范式，并通过强化学习训练 VLM 生成高质量的任务导向场景图。相较于现有基线，本文在四个关键维度上做出了实质性改变。

### 1. 规划策略：从 Direct Plan 到 Graph-then-Plan

现有 VLM 基线（如 **GPT-5**、**Claude-4.5-Sonnet**、**Qwen2.5-VL-7B-Instruct**）普遍采用 Direct Plan 策略，即直接从多视角图像和语言指令生成动作序列。然而，如 Figure 2 所示，即使 GPT-5 等强闭源模型也常产生错误动作或遗漏关键步骤。MomaGraph 提出 Graph-then-Plan 框架：模型首先生成结构化的任务导向场景图作为中间表示，再基于该图进行高层任务分解和动作序列规划。Table 2 的消融实验一致表明，在所有模型上 w/ Graph 设置均显著优于 w/o Graph 基线，验证了显式结构化场景表示对下游规划的因果增益。

### 2. 场景图表征：从单一关系图到统一空间-功能图

传统场景图方法通常仅编码空间关系或功能关系中的一种，且忽略零件级交互元素。MomaGraph 首次统一了空间关系与功能关系，并引入零件级交互节点，显式建模物体状态变化。其任务导向场景图定义为：

$$\mathcal{G}_{\mathcal{T}} = ( \mathcal{N}_{\mathcal{T}}, \mathcal{E}_{s}^{\mathcal{T}}, \mathcal{E}_{f}^{\mathcal{T}} )$$

其中 $\mathcal{N}_{\mathcal{T}}$ 为任务相关节点集，$\mathcal{E}_{s}^{\mathcal{T}}$ 和 $\mathcal{E}_{f}^{\mathcal{T}}$ 分别为有向的空间关系边和功能关系边。Table 1 的消融实验提供了强因果证据：MomaGraph-R1 在统一图设置下达到 71.6% 总体准确率，而仅空间图仅 59.9%，仅功能图仅 64.9%；LLaVA-Onevision 上统一图（66.0%）同样大幅领先单一关系图（54.0%/57.0%），证明两类关系互补的必要性。

### 3. 训练范式：从 SFT/ICL 到 DAPO 强化学习

基线方法通常依赖标准指令微调（SFT）或上下文示例（ICL）训练 VLM。MomaGraph-R1 转而采用 DAPO 强化学习算法，配合精心设计的图对齐奖励函数进行训练。奖励函数定义为加权组合：

$$\mathcal{R}(\mathcal{G}_{\mathcal{T}}^{\mathrm{pred}}, \mathcal{G}_{\mathcal{T}}^{\mathrm{gt}}) = w_a \cdot (R_{\mathrm{action}} + R_{\mathrm{edges}} + R_{\mathrm{nodes}}) + w_f \cdot R_{\mathrm{format}} + w_l \cdot R_{\mathrm{length}}$$

其中边奖励基于预测边与真值边之间的平均最大语义相似度计算：

$$R_{\mathrm{edges}} = \frac{1}{|\mathcal{E}_{\mathrm{gt}}^{\mathcal{T}}|} \sum_{e_j \in \mathcal{E}_{\mathrm{gt}}^{\mathcal{T}}} \max_{e_i \in \mathcal{E}_{\mathrm{pred}}^{\mathcal{T}}} S_{\mathrm{edge}}(e_i, e_j)$$

Table 5 显示 RL 训练在 MomaGraph-Bench 上达到 71.6%，相比 SFT（63.9%）提升 +7.7%，相比 ICL（60.2%）提升 +11.4%；在 BLINK 基准上 RL（63.5%）同样显著优于 SFT（60.4%）和 ICL（58.7%）。Table 6 的灵敏度分析进一步表明，奖励权重在合理范围内对最终性能影响有限（波动 ≤3.4%），训练过程稳定。

### 4. 状态感知动态更新机制

现有方法通常以静态快照进行一次性推理，无法适应任务执行过程中的环境变化。MomaGraph 引入状态感知的动态场景图更新机制，在时间步 $t$ 的场景图定义为：

$$\mathcal{G}_{\mathcal{T}}^{(t)} = ( \mathcal{N}_{\mathcal{T}}^{(t)}, \mathcal{E}_{s}^{\mathcal{T},(t)}, \mathcal{E}_{f}^{\mathcal{T},(t)} )$$

执行动作 $a_t$ 并观察到新状态 $s_{t+1}$ 后，通过更新函数剪除不一致的功能假设并强化经确认的对应关系：

$$\mathcal{G}_{\mathcal{T}}^{(t+1)} = \mathcal{U}\Big( \mathcal{G}_{\mathcal{T}}^{(t)}, a_t, s_{t+1} \Big)$$

这一机制使场景图能随交互过程动态演化，在需要预条件推理和多步调整的长程任务中尤为关键。真实机器人实验中，系统在 10 次试验中取得 70% 总成功率（图生成成功率 80%，规划成功率 87.5%），验证了该机制的实用性。

### 创新总结

上述四个 changed slots 形成了完整的因果链条：统一空间-功能图提供了更丰富的结构化知识基础，Graph-then-Plan 解耦了感知与规划，RL 训练确保图生成的高质量，状态感知更新则赋予系统动态适应能力。最终，MomaGraph-R1 以 7B 参数规模在 MomaGraph-Bench 上达到 71.6% 准确率，与闭源巨模型 **GPT-5**（71.6%）持平，仅略低于 **Claude-4.5-Sonnet**（73.9%），在开源模型中取得最优。



![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_3eTr9dGwJv/figures/002_Figure_1.jpg]]
*Figure 1: Overview of the MomaGraph. Given a task instruction, MomaGraph constructs a taskspecific scene graph that highlights relevant objects and parts along with their spatial-functional relationships, enabling the robot to perform spatial understanding and task planning*

MomaGraph 提出了一套 **Graph-then-Plan** 的具身任务规划框架，其核心思想是将场景理解与动作规划解耦：先显式构建一个融合空间与功能信息、包含零件级交互节点且与当前任务相关的结构化场景图，再基于该图进行零样本高层任务分解与动作序列生成。

### 输入输出流

框架的输入端由两部分组成：
- **多视角 RGB 图像**：来自机器人搭载的相机（如真实实验中的 D455 深度相机 RGB 通道），提供对操作场景的多角度观测。
- **自然语言任务指令**：描述需要完成的操作目标，如“打开橱柜”“关灯”等。

输出端为**高层动作序列**，即一系列可被后续低层控制器解释执行的子任务步骤。

### 核心模块与数据流

整个 pipeline 由以下模块串联构成：

1. **多视角视觉编码与 VLM 骨干**
   系统以 **Qwen2.5-VL-7B-Instruct** 作为视觉-语言模型基座，接收多视角图像和任务指令，负责将视觉观测与语言语义联合编码。该基座模型的选择为后续 RL 训练提供了统一的表征空间。

2. **任务导向场景图生成模块**
   这是框架的核心创新。VLM 被训练输出一个结构化的任务导向场景图（MomaGraph），形式化定义为：
   $$\mathcal{G}_{\mathcal{T}} = ( \mathcal{N}_{\mathcal{T}}, \mathcal{E}_{s}^{\mathcal{T}}, \mathcal{E}_{f}^{\mathcal{T}} )$$
   其中 $\mathcal{N}_{\mathcal{T}}$ 为与当前任务相关的候选对象节点（含零件级交互元素），$\mathcal{E}_{s}^{\mathcal{T}}$ 为空间关系有向边（如 `[LEFT OF]`、`[TOUCHING]`、`[CLOSE]` 等），$\mathcal{E}_{f}^{\mathcal{T}}$ 为功能关系有向边（如 `[GRASP]`、`[PAIR WITH]`、`[OPEN]` 等），所有边均从触发对象指向受作用对象。该场景图以 JSON 格式输出，同时包含对当前任务所需动作类型的预测。

   为训练模型生成高质量场景图，系统采用 **DAPO 强化学习算法**，并设计了专门的图对齐奖励函数：
   $$\mathcal{R}(\mathcal{G}_{\mathcal{T}}^{\mathrm{pred}}, \mathcal{G}_{\mathcal{T}}^{\mathrm{gt}}) = w_a \cdot (R_{\mathrm{action}} + R_{\mathrm{edges}} + R_{\mathrm{nodes}}) + w_f \cdot R_{\mathrm{format}} + w_l \cdot R_{\mathrm{length}}$$
   其中 $R_{\mathrm{action}}$ 为动作类型预测奖励，$R_{\mathrm{edges}}$ 为边语义相似度奖励（基于空间和功能标签计算预测边与真值边的平均最大语义匹配），$R_{\mathrm{nodes}}$ 为节点完整性 IoU 奖励，$R_{\mathrm{format}}$ 验证输出格式合规性，$R_{\mathrm{length}}$ 为长度惩罚项。超参数 $w_a, w_f, w_l$ 控制各部分的权重。

3. **零样本规划模块**
   生成的场景图作为结构化中间表示，被送入规划阶段。该阶段无需额外微调，直接基于场景图中的空间-功能关系、零件归属和动作类型预测，进行高层任务分解并输出动作序列。这一 Graph-then-Plan 策略在 Table 2 中得到充分验证：所有模型在 w/ Graph 设置下均一致优于 w/o Graph 的直接规划基线，表明结构化场景表示对下游规划具有显著增益。

4. **状态感知动态更新机制**
   在执行动作 $a_t$ 并观察到新状态 $s_{t+1}$ 后，系统通过更新函数动态修正场景图：
   $$\mathcal{G}_{\mathcal{T}}^{(t+1)} = \mathcal{U}\Big( \mathcal{G}_{\mathcal{T}}^{(t)}, a_t, s_{t+1} \Big)$$
   初始场景图中的功能关系可能包含一对多的假设映射（如一个把手可能对应多个可操作部件），更新函数 $\mathcal{U}(\cdot)$ 根据实际执行后的状态变化，剪除不一致的功能假设、强化经确认的对应关系，从而消除歧义并保持场景图与真实环境状态同步。这一机制使系统能够在多步长程任务中动态调整规划，而非依赖静态的一次性推理。

### 关键设计决策

- **统一空间-功能关系**：Table 1 的消融实验表明，统一图（Unified）在 MomaGraph-R1 上达到 71.6% 的整体准确率，而仅空间图为 59.9%、仅功能图为 64.9%，验证了两类关系互补的必要性。
- **RL 训练替代 SFT/ICL**：Table 5 显示 RL 训练（71.6%）相比 SFT（63.9%）和 ICL（60.2%）大幅提升场景图生成质量和规划表现，证明基于图对齐奖励的强化学习是使 VLM 学会构建精确任务导向场景图的关键。
- **多视角联合推理**：利用多视角观测捕捉对象对应关系，在 BLINK 视觉对应基准上 MomaGraph-R1 达到 63.5%，领先最强开源基线 3.8 个百分点（Table 3），表明多视角一致性机制有效提升了跨视角的空间推理能力。



### 任务导向场景图的定义

MomaGraph 的核心表示形式是任务导向的场景图，定义为：

$$\mathcal{G}_{\mathcal{T}} = ( \mathcal{N}_{\mathcal{T}}, \mathcal{E}_{s}^{\mathcal{T}}, \mathcal{E}_{f}^{\mathcal{T}} )$$

其中，$\mathcal{N}_{\mathcal{T}}$ 为与任务指令相关的节点集合（包含物体及其零件级交互元素），$\mathcal{E}_{s}^{\mathcal{T}}$ 为空间关系有向边集合，$\mathcal{E}_{f}^{\mathcal{T}}$ 为功能关系有向边集合。两类边均从触发对象指向受作用对象，显式编码了“谁作用于谁”的因果方向。该图以任务指令为条件进行构建，仅保留与当前任务相关的节点与关系，从而避免无关信息对下游规划的干扰。

### 图生成与强化学习训练

MomaGraph-R1 基于 **Qwen2.5-VL-7B-Instruct** 构建，采用 **DAPO** 强化学习算法训练，使其能够从多视角图像中直接生成结构化的任务导向场景图。训练的核心在于精心设计的图对齐奖励函数，该函数由五个分量加权组合而成：

$$\mathcal{R}(\mathcal{G}_{\mathcal{T}}^{\mathrm{pred}}, \mathcal{G}_{\mathcal{T}}^{\mathrm{gt}}) = w_a \cdot (R_{\mathrm{action}} + R_{\mathrm{edges}} + R_{\mathrm{nodes}}) + w_f \cdot R_{\mathrm{format}} + w_l \cdot R_{\mathrm{length}}$$

各分量含义如下：

- **$R_{\mathrm{action}}$**：动作类型预测奖励，衡量模型对任务所需动作类型的判断是否准确。
- **$R_{\mathrm{edges}}$**：边奖励，衡量预测边与真值边之间的语义对齐程度。其计算方式为预测边集 $\mathcal{E}_{\mathrm{pred}}^{\mathcal{T}}$ 中每条边与真值边集 $\mathcal{E}_{\mathrm{gt}}^{\mathcal{T}}$ 的最大语义相似度的平均值：

$$R_{\mathrm{edges}} = \frac{1}{|\mathcal{E}_{\mathrm{gt}}^{\mathcal{T}}|} \sum_{e_j \in \mathcal{E}_{\mathrm{gt}}^{\mathcal{T}}} \max_{e_i \in \mathcal{E}_{\mathrm{pred}}^{\mathcal{T}}} S_{\mathrm{edge}}(e_i, e_j)$$

其中 $S_{\mathrm{edge}}(e_i, e_j)$ 基于空间关系标签和功能关系标签计算语义相似度。

- **$R_{\mathrm{nodes}}$**：节点完整性奖励，基于节点 IoU 衡量预测节点集与真值节点集的重叠程度。
- **$R_{\mathrm{format}}$**：格式验证奖励，确保输出符合 JSON 结构规范。
- **$R_{\mathrm{length}}$**：长度惩罚，抑制冗余输出。

超参数 $w_a$、$w_f$、$w_l$ 分别控制动作/边/节点核心奖励、格式奖励和长度惩罚的相对重要性。消融实验表明，模型在不同权重配置下性能保持稳定（MomaGraph-Bench 上波动 ≤3.4%），训练过程对权重选择不敏感。

### 状态感知的动态图更新

在任务执行过程中，场景图需要随环境状态变化而动态演化。MomaGraph 在时间步 $t$ 的场景图定义为：

$$\mathcal{G}_{\mathcal{T}}^{(t)} = ( \mathcal{N}_{\mathcal{T}}^{(t)}, \mathcal{E}_{s}^{\mathcal{T},(t)}, \mathcal{E}_{f}^{\mathcal{T},(t)} )$$

其中功能边 $\mathcal{E}_{f}^{\mathcal{T},(t)}$ 初始可能包含一对多的假设映射（例如一个把手可能对应多个柜门）。当机器人执行动作 $a_t$ 并观察到新状态 $s_{t+1}$ 后，通过更新函数 $\mathcal{U}(\cdot)$ 对图进行精炼：

$$\mathcal{G}_{\mathcal{T}}^{(t+1)} = \mathcal{U}\Big( \mathcal{G}_{\mathcal{T}}^{(t)}, a_t, s_{t+1} \Big)$$

更新机制的核心逻辑是：根据实际观察到的状态变化，剪除与观测不一致的功能假设边，同时强化经执行验证确认的对应关系。这一机制使场景图能够随交互过程逐步消除歧义，为后续规划步骤提供更可靠的结构化知识基础。



## 实验与关键发现

### 核心瓶颈验证：Graph-then-Plan 范式的增益

论文首先通过一个关键的对照实验验证了其核心动机：**结构化场景图作为中间表示对下游规划具有显著增益**。在 MomaGraph-Bench 上，所有测试模型在引入场景图辅助推理（w/ Graph）后，其规划准确率均一致且大幅超越直接规划（w/o Graph）基线（Table 2）。这一结果表明，将场景理解与动作规划解耦，先显式构建结构化知识，再基于该知识进行推理，是缓解当前 VLM 直接规划时“知其然不知其所以然”瓶颈的有效路径。该对照实验在统一评估协议下进行，消除了模型预训练差异的干扰，证据置信度高。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_3eTr9dGwJv/figures/007_Table_2.jpg]]
*Table 2: Performance comparison on the MomaGraph-Bench. We report accuracy (%) across four tiers (T1–T4) and the overall score, with and without graph-based reasoning*

### 主实验结果：开源模型达到闭源水平

在 MomaGraph-Bench 综合评测上，**MomaGraph-R1**（基于 Qwen2.5-VL-7B-Instruct 进行 DAPO 强化学习训练）在 w/ Graph 设置下取得了 **71.6%** 的 Overall Accuracy，相较于其基座模型 **Qwen2.5-VL-7B** 的 60.2% 提升了 **+11.4 个百分点**，在所有开源基线中表现最优（Table 2）。更值得关注的是，MomaGraph-R1 的性能已与闭源巨模型 **GPT-5**（71.6%）持平，仅次于 **Claude-4.5-Sonnet**（73.9%），表明通过针对性的结构化表示学习和 RL 训练，小模型可以在特定具身推理任务上达到与大规模闭源模型相当的水平。

在视觉对应推理能力上（Table 3），MomaGraph-R1 在 BLINK 基准上达到 **63.5%**，较基座模型提升 **+4.8%**；在 MomaGraph-Bench 对应子集上达到 **77.5%**，同样提升 **+4.8%**。这验证了方法中多视角一致性机制的有效性——通过场景图显式捕捉跨视角对象对应关系，模型在需要跨视图匹配的推理任务上获得了可观的增益。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_3eTr9dGwJv/figures/008_Table_3.jpg]]
*Table 3: Performance comparison on the BLINK and MomaGraph-Bench. By enforcing multiview consistency, our method significantly improves correspondence reasoning across all opensource models*

### 消融实验：统一图的必要性与训练范式选择

**统一空间-功能图 vs. 单关系图**（Table 1）是最核心的消融。MomaGraph-R1 在仅使用空间关系图时 Overall 降至 59.9%，仅使用功能关系图时降至 64.9%，而统一图达到 71.6%。同样的趋势在 **LLaVA-Onevision** 上也得到复现：统一图 66.0% vs 空间图 54.0% vs 功能图 57.0%。这强有力地证明，空间关系与功能关系是互补的信息维度，单一关系图无法完整刻画具身任务所需的场景语义，联合建模是必要的设计选择。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_3eTr9dGwJv/figures/004_Table_1.jpg]]
*Table 1: Comparison between MomaGraph-R1and LLaVA variants across task tiers*

**RL vs. SFT vs. ICL**（Table 5）的对比进一步揭示了训练范式的重要性。RL 训练在 MomaGraph-Bench 上达到 71.6%，显著优于 SFT 的 63.9%（+7.7%）和 ICL 的 60.2%（+11.4%）；在 BLINK 上 RL 为 63.5%，同样领先 SFT（60.4%）和 ICL（58.7%）。这表明，精心设计的图对齐奖励函数（包含动作类型、边语义相似度、节点 IoU、格式验证和长度惩罚的加权组合）能够为 VLM 提供比标准指令微调或上下文示例更有效的学习信号，引导模型生成更精确的任务导向场景图。

**奖励函数权重的灵敏度分析**（Table 6）显示，模型在不同权重配置下的性能波动不超过 3.4%，表明 DAPO 训练过程对奖励超参数不敏感，具有良好的训练稳定性。

### 真实机器人验证与失败模式分析

在真实机器人实验中（Figure 14），系统在四类家庭长程任务上进行了 10 次试验评估。场景图生成成功率为 **80%**，基于图的规划成功率为 **87.5%**，整体端到端任务成功率达到 **70%**。这一结果验证了方法从仿真到真实环境的迁移能力。

失败分析揭示了两个主要瓶颈：
- **图生成阶段**：空间关系错误（如方向判断偏差）和节点缺失是主要失败原因，导致后续规划缺乏正确的空间前提。
- **规划阶段**：动作序列顺序不当——即使场景图本身正确，模型在将图结构转化为动作序列时仍可能出现步骤遗漏或逻辑颠倒。

这些失败模式表明，当前方法的薄弱环节集中在视觉空间感知的精度和图到动作序列的映射可靠性上，而非统一图表征框架本身的设计缺陷。

### 局限性与待验证问题

当前评估局限于单房间家庭场景，尚未涉及多房间或跨楼层的连续操作任务。真实机器人测试仅覆盖 10 次试验，统计意义有待更大规模验证。此外，多视角图像依赖人工预先采集，缺乏主动视角选择能力；动态场景图更新依赖实际执行后的状态观察，无法进行反事实推理。这些限制为后续工作指明了方向：扩展至开放式多房间场景、集成主动视角选择、结合反事实推理进行鲁棒规划，以及与低层运动控制模块的对接。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_3eTr9dGwJv/figures/013_Figure_9.jpg]]
*Figure 9: Task distribution across four room types: kitchen, living room, bedroom, and bathroom*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_3eTr9dGwJv/figures/015_Figure_11.jpg]]
*Figure 11: Statistics of object occurrences, highlighting the most frequent objects in tasks*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_3eTr9dGwJv/figures/016_Figure_12.jpg]]
*Figure 12: Training reward curves during MomaGraph-R1 training*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_3eTr9dGwJv/figures/018_Figure_13.jpg]]
*Figure 13: Validation reward curves during MomaGraph-R1 training*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_3eTr9dGwJv/figures/022_Figure_15.jpg]]
*Figure 15: Real-world robot execution of household tasks*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_3eTr9dGwJv/figures/012_Figure_8.jpg]]
*Figure 8: Dataset statistics: (a) Distribution across four room types; (b)Heatmap showing the correspondence between action types and functional types*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_3eTr9dGwJv/figures/014_Figure_10.jpg]]
*Figure 10: Distribution of functional relationships across all tasks in the dataset*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_3eTr9dGwJv/figures/017_Table_4.jpg]]
*Table 4: DAPO Training Configuration*



## 定位与知识库关联

### 与现有方法的继承与分叉

MomaGraph 的核心思路——将场景图作为具身规划的中间表示——并非凭空出现，而是对两条技术路线的系统性回应与融合。

**场景图构建的传统与瓶颈。** 经典场景图生成（Scene Graph Generation, SGG）主要用于图像理解，通常将空间关系与功能关系分离处理，且图结构在任务执行过程中保持静态。这一范式在具身场景中暴露了两个关键缺陷：其一，零件级交互元素（如“把手”“按钮”）未被显式建模，导致对“打开微波炉”这类需要定位操作部件的任务缺乏结构化支持；其二，物体状态的时间变化（如“门已打开”）无法被图结构捕获，使得多步任务中的预条件推理失去依据。MomaGraph 通过引入统一空间-功能边集 $\mathcal{E}_s^{\mathcal{T}}$ 和 $\mathcal{E}_f^{\mathcal{T}}$ 以及零件级节点，直接填补了这两处空白。消融实验提供了强因果证据：仅保留空间关系时 MomaGraph-R1 的 MomaGraph-Bench Overall 从 71.6 骤降至 59.9，仅保留功能关系时降至 64.9，证实两类关系互补且不可替代。

**VLM 规划范式的分叉点。** 当前基于 VLM 的具身规划主流方案是 Direct Plan，即直接从多视角图像和语言指令生成动作序列。论文的动机实验（Figure 2）表明，即使强如 GPT-5，直接规划仍会产生错误动作或遗漏关键步骤。MomaGraph 选择了一条不同的路径：Graph-then-Plan——先显式生成结构化场景图，再基于该图进行零样本规划。这一解耦策略的因果效应在 Table 2 中得到了跨模型验证：所有测试模型在 w/ Graph 设置下均一致优于 w/o Graph 设置，说明结构化中间表示本身即为规划增益的独立来源，而非特定模型的附带效应。

**训练范式的跃迁。** 在 VLM 微调层面，标准做法是监督微调（SFT）或上下文示例（ICL）。MomaGraph-R1 转而采用 DAPO（Yu et al., 2025）强化学习算法，并设计了专门的图对齐奖励函数 $\mathcal{R}(\mathcal{G}_{\mathcal{T}}^{\mathrm{pred}}, \mathcal{G}_{\mathcal{T}}^{\mathrm{gt}})$，其由动作类型预测、边语义相似度、节点 IoU、格式验证和长度惩罚五项加权组成。Table 5 的消融显示，RL 训练在 MomaGraph-Bench Overall 上达到 71.6，相比 SFT（63.9）和 ICL（60.2）分别提升 +7.7 和 +11.4 个百分点，在 BLINK 基准上同样保持优势（63.5 vs 60.4 vs 58.7），证明精心设计的结构化奖励是性能跃迁的关键杠杆。

### 与同期/后续工作的关系

在开源 VLM 生态中，MomaGraph-R1 以 7B 参数规模（基于 Qwen2.5-VL-7B-Instruct）在 MomaGraph-Bench 上达到 71.6% Overall，与闭源巨模型 GPT-5（71.6）持平，仅略低于 Claude-4.5-Sonnet（73.9），同时显著超越 InstructBLIP-7B、LLaVA-V1.5-7B、DeepSeek-VL2、InternVL2.5-8B 等开源基线。在视觉对应推理的 BLINK 基准上，MomaGraph-R1 达到 63.5%，领先最强开源基线 LLaVA-Onevision（59.7）约 3.8 个百分点，验证了多视角一致性机制的有效性。

值得关注的是，MomaGraph 的 Graph-then-Plan 范式与近年来兴起的“规划-执行解耦”思路（如 SayCan、Code as Policies 等以语言/代码为中间表示的方法）形成对照。区别在于，MomaGraph 选择场景图而非自然语言或代码作为中间表示，其优势在于图结构天然适合编码关系推理和状态更新，劣势则在于对图生成精度的依赖更高——真实机器人实验中，失败主要源于图生成阶段的空间关系错误或缺失节点，以及规划阶段的动作序列顺序不当。

### 适用边界与局限

**场景范围的约束。** 当前评估局限于单房间家庭场景（厨房、客厅、卧室、浴室），未涉及多房间或跨楼层的连续操作任务。MomaGraph-Scenes 数据集的房间类型分布虽覆盖四类，但场景间的拓扑连接和导航需求未被纳入图结构建模。

**视角获取的被动性。** 多视角图像作为模型输入，需人工预先采集或从仿真环境导出，系统缺乏自动选择有意义视角的能力。这意味着在真实部署中，视角覆盖不足可能导致关键零件被遮挡，进而引发图生成阶段的节点缺失。

**动态更新的执行依赖。** 状态感知动态更新机制 $\mathcal{G}_{\mathcal{T}}^{(t+1)} = \mathcal{U}(\mathcal{G}_{\mathcal{T}}^{(t)}, a_t, s_{t+1})$ 依赖实际执行动作并观察状态变化，无法在想象中完成反事实推理。这限制了系统在规划阶段预判潜在失败并提前调整的能力。

**真实机器人验证的规模。** 真实机器人实验仅测试了有限数量的长程任务（10 次试验），总成功率为 70%（图生成 80%，规划 87.5%），统计意义有待更大规模验证。此外，模型目前仅输出高层动作序列，尚未直接生成可供机器人执行的低层运动控制命令。

### 开放问题

1. **场景扩展与主动感知。** 如何将 MomaGraph 扩展到开放式、多房间场景，并赋予系统目标导向的主动视角选择能力，使其能自主决定“下一步该看哪里”？
2. **反事实推理与鲁棒规划。** 能否将动态更新机制与反事实推理结合，在规划阶段即模拟可能的执行结果并提前调整策略，而非等待实际失败后再被动修正？
3. **端到端控制集成。** Graph-then-Plan 范式能否与分层强化学习或模型预测控制（MPC）集成，直接生成可执行的连续控制信号，从而弥合高层规划与低层执行之间的鸿沟？
4. **奖励权重的自适应调节。** 当前奖励函数中的权重 $w_a, w_f, w_l$ 依赖人工设定（Table 6 显示性能在合理范围内对权重不敏感，波动 ≤3.4%），是否可在训练过程中自动调节以进一步减少人工干预？
5. **跨领域迁移。** 该方法的核心机制——任务导向的统一场景图与状态感知更新——能否迁移至工业装配、农业操作或医疗手术等更复杂的操作领域？这些领域对零件级精度和动态状态追踪的需求可能更高，但也可能面临标注成本激增的挑战。



## 原文 PDF

![[paperPDFs/ICLR_2026/MomaGraph_State_Aware_Unified_Scene_Graphs_with_Vision_Language_Models_for_Embodied_Task_Planning.pdf]]
