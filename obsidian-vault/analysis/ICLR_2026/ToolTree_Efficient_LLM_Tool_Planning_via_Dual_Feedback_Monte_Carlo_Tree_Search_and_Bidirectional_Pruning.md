---
title: "ToolTree: Efficient LLM Tool Planning via Dual-Feedback Monte Carlo Tree Search and Bidirectional Pruning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ToolTree_Efficient_LLM_Tool_Planning_via_Dual_Feedback_Monte_Carlo_Tree_Search_and_Bidirectional_Pruning.pdf
project_link: null
code_link: null
openreview_forum_id: Ef5O9gNNLE
aliases:
- ToolTree
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "引入预执行先验（r_pre）与后执行效用（r_post）双重反馈，将其整合到蒙特卡洛树搜索的节点选择、扩展、更新与剪枝过程中，使规划同时具备前瞻预测与后顾验证能力。"
primary_logic: "将工具规划形式化为搜索问题，利用预评估分数在展开前过滤低潜力节点，利用后评估分数在执行后剪除无效分支，并通过运行平均更新动作价值，从而在固定预算下自适应分配计算资源，提升准确率与效率。"
claims:
- "ToolTree 在 GTA 和 m&m 数据集上均取得最高平均分，在 GPT-4o 下比最强基线 LATS 分别高出 2.17 和 2.16 个百分点。"
- "在 ToolBench 和 RestBench 等开放工具集基准上，ToolTree 的领先优势保持一致，例如在 ToolBench (GPT-4o) 上平均分 69.04，超出 LATS 2.49 个百分点。"
- "移除后评估组件导致准确率大幅下降 7.5 个百分点，证实执行后反馈是搜索方向的关键驱动力。"
- "双向剪枝分别在不同阶段压缩搜索空间：预剪枝减少展开节点数，后剪枝减少模拟次数，二者协同提升整体效率。"
---

# ToolTree: Efficient LLM Tool Planning via Dual-Feedback Monte Carlo Tree Search and Bidirectional Pruning

> [!tip] 核心洞察
> 将工具规划形式化为搜索问题，利用预评估分数在展开前过滤低潜力节点，利用后评估分数在执行后剪除无效分支，并通过运行平均更新动作价值，从而在固定预算下自适应分配计算资源，提升准确率与效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ToolTree：基于双反馈蒙特卡洛树搜索与双向剪枝的高效大语言模型工具规划 |
| 英文题名 | ToolTree: Efficient LLM Tool Planning via Dual-Feedback Monte Carlo Tree Search and Bidirectional Pruning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Ef5O9gNNLE) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | ToolTree |
| Dataset | GTA (GPT-4o-mini), m&m (GPT-4o-mini), GTA (GPT-4o), m&m (GPT-4o) |

> [!tip] 效果简介
> - GTA (GPT-4o-mini) 上，Average F1 (step-by-step + end-to-end) 为 55.89，对比 53.91 (LATS)，变化 +1.98。
> - m&m (GPT-4o-mini) 上，Average F1 (step-by-step + multi-step) 为 76.90，对比 75.83 (LATS)，变化 +1.07。
> - GTA (GPT-4o) 上，Average F1 (step-by-step + end-to-end) 为 66.95，对比 64.78 (LATS)，变化 +2.17。

## 概要

当前大语言模型（LLM）在调用外部工具时，主流规划策略多采用贪婪或反应式范式（如 ReAct、Chain-of-Thought），这些方法缺乏前瞻性，难以感知工具间的复杂依赖关系，早期次优选择极易导致错误累积。另一方面，基于搜索的规划方法（如 Tree-of-Thought、LATS）虽然具备回溯能力，却面临分支爆炸、计算开销高昂以及动作评价与执行脱节等瓶颈。

**ToolTree** 针对上述困境，将工具规划形式化为一个受双重反馈引导的蒙特卡洛树搜索（MCTS）问题。其核心机制在于引入**预执行先验（r_pre）**与**后执行效用（r_post）**两类信号：前者在工具调用前由 LLM 快速评估候选动作的潜在价值，用于偏置节点选择与展开前剪枝；后者依据实际执行结果对动作进行回溯评分，驱动 Q 值更新与执行后剪枝。通过这种“前瞻预测 + 后顾验证”的闭环，ToolTree 在固定计算预算下自适应地分配搜索资源，有效抑制分支膨胀，并能在早期误判后自行纠偏。

在 GTA 与 m&m 两个工具规划数据集上，ToolTree 以 GPT-4o 为后端时分别取得 66.95 与 88.61 的平均 F1 分数，较大幅度领先最强基线 LATS（+2.17 与 +2.16 个百分点）。在开放工具集基准 ToolBench 与 RestBench 上，该优势同样保持稳定：ToolBench（GPT-4o）平均得分 69.04，超出 LATS 2.49 个百分点；RestBench-TMDB 与 Spotify 上分别领先 3.15 与 2.83 个百分点。消融实验进一步揭示，移除后评估组件会导致准确率骤降约 7.5 个百分点，证实执行后真实反馈是搜索方向的关键驱动力；而移除预剪枝或后剪枝中的任一项，均会显著增加节点展开数或模拟次数，验证了双向剪枝在效率层面的协同作用。

综上，ToolTree 通过双反馈 MCTS 与双向剪枝的组合设计，在工具规划的准确率与计算效率之间取得了显著突破，为 LLM 工具调用提供了一种可扩展、可纠错的搜索范式。



大语言模型（LLM）驱动的智能体在复杂任务中需要编排多个外部工具，例如调用搜索引擎、计算器、数据库或 REST API。工具规划的核心挑战在于：每一步的工具选择不仅影响当前结果，还会通过工具间的依赖关系改变后续可用的信息与操作空间，早期的一个次优决策可能导致整个执行链的误差累积与任务失败。

当前主流的工具规划策略可归为两类，各自存在显著局限：

**反应式与贪婪策略**：以 **ReAct**（Yao et al., 2023b）和 **Chain-of-Thought**（Wei et al., 2022）为代表的方法采用逐步决策范式，每一步仅基于当前上下文做出局部最优的工具调用。这类方法缺乏前瞻性，无法评估当前选择对后续步骤的长远影响，在需要多步依赖推理的场景中容易陷入错误传播的陷阱。

**搜索式规划策略**：**Tree-of-Thought**（Yao et al., 2023a）、**LATS**（Zhou et al., 2024）以及 **ToolChain***（Zhuang et al., 2024）等方法将工具规划视为树搜索问题，通过展开多条候选路径来寻找全局最优轨迹。然而，这类方法面临三个核心困境：其一，工具空间的分支因子通常极大，导致搜索树迅速膨胀，计算开销难以承受；其二，搜索过程中的动作评价往往依赖 LLM 的模拟推演而非真实执行反馈，评价信号与实际情况脱节；其三，缺乏有效的剪枝机制，大量计算资源被浪费在低潜力分支上。

上述两类方法的共同盲区在于：**预测性信号与执行后验证信号是割裂的**。贪婪方法仅依赖执行后的即时观察来调整下一步，而搜索方法在展开节点时主要依靠 LLM 的事先推测，两者都没有将“执行前预测”与“执行后验证”有机融合到统一的搜索框架中。

本文的动机正源于此：能否设计一种工具规划范式，同时具备前瞻预测与后顾验证的能力，在有限的计算预算下自适应地分配搜索资源？这要求规划器能够在展开一个工具调用之前就对其潜在效用做出快速评估，避免盲目展开低质量分支；同时，在工具实际执行后，利用真实的执行结果对搜索方向进行纠正，及时剪除已被证伪的路径。ToolTree 正是围绕这一核心思想构建的——它将工具规划形式化为蒙特卡洛树搜索问题，引入预执行先验与后执行效用双重反馈机制，并配合双向剪枝策略，在保持搜索前瞻性的同时大幅压缩无效搜索空间。



## 核心方法与创新机理

ToolTree 的核心创新在于将大语言模型的工具规划重新形式化为一种**双反馈驱动的蒙特卡洛树搜索**过程。与现有贪婪式或反应式规划方法不同，ToolTree 引入了两个互补的评估信号，并将其深度嵌入搜索的各个阶段，从而在固定计算预算下实现了前瞻性探索与后顾性验证的闭环。

### 双反馈机制：预评估先验与后执行效用

现有搜索式规划方法面临两个根本性瓶颈：一是展开前缺乏对动作潜力的预判，导致计算资源浪费在低质量分支上；二是执行后缺乏对实际效果的反馈，使得搜索方向难以纠偏。ToolTree 通过双反馈机制同时解决了这两个问题。

**预评估先验（$r_{\mathrm{pre}}$）** 在工具调用执行前，由 LLM 根据当前上下文对候选动作的潜在效用进行快速评分。该分数被直接整合进节点选择的增强 UCT 准则中：

$$\mathrm{UCT}(s, a) = Q(s, a) + \lambda r_{\mathrm{pre}}(s, a) \sqrt{\frac{\ln N(s)}{N(s, a)}}$$

其中 $r_{\mathrm{pre}}(s,a)$ 作为偏置项，在探索初期引导搜索优先访问预测价值更高的动作，而非仅依赖尚未充分更新的 $Q$ 值。这一设计的关键在于：预评估分数在节点访问计数不足时提供了有价值的先验，而在访问充分后其影响自然衰减。

**后执行效用（$r_{\mathrm{post}}$）** 在工具实际执行后，由 LLM 法官根据执行输出 $o_{t+1}$ 评估动作的真实贡献，输出 $[0,1]$ 区间的分数。该分数承担双重角色：一方面作为即时奖励，通过运行平均更新动作价值：

$$Q(s,a) \gets Q(s,a) + \frac{r_{\mathrm{post}}(s_t,a) - Q(s,a)}{N(s,a)}$$

另一方面作为剪枝依据——若 $r_{\mathrm{post}}(s_t,a) < \tau_{\mathrm{post}}$，则将该边标记为不可扩展，阻止后续模拟继续投入该分支。这种“执行即反馈”的机制使得搜索能够基于真实工具输出快速收敛，而非依赖模拟或终端奖励的延迟信号。

### 双向剪枝：搜索空间的分阶段压缩

ToolTree 在搜索的两个关键阶段施加互补的剪枝操作，形成“展开前过滤—执行后截断”的双向压缩管线。

**预剪枝**作用于展开阶段。给定当前状态 $s_t$ 的所有合法动作 $\mathcal{A}(s_t)$，仅保留预评估分数满足阈值且位于 top-K 的动作进入展开候选集：

$$\mathcal{A}^+(s_t) = \{ a \in \mathcal{A}(s_t) : r_{\mathrm{pre}}(s_t,a) \geq \tau_{\mathrm{pre}} \}, \quad \mathcal{A}_{\mathrm{keep}}(s_t) = \mathrm{top}\mathcal{K}(\mathcal{A}^+(s_t); r_{\mathrm{pre}})$$

这一操作在工具模式或槽位不兼容的调用被实际执行前即予以剔除，显著抑制了分支因子膨胀。消融实验证实，移除预剪枝后中位展开节点数从约 70 跃升至约 95（Figure 4）。

**后剪枝**作用于执行后。当 $r_{\mathrm{post}}$ 低于阈值 $\tau_{\mathrm{post}}$ 时，该状态-动作对被永久标记为不可扩展，后续模拟将不再沿此路径深入。这相当于为搜索设置了“早期止损”机制——一旦某分支被实际执行证明无效，立即回收预算。消融显示，移除后剪枝使中位模拟次数从约 33 增至约 47（Figure 4）。

两种剪枝的协同效应体现在：预剪枝减少了需要实际执行的动作数量，从而降低了后剪枝需要评估的样本量；后剪枝则通过快速淘汰低效路径，间接提升了预评估分数的校准压力。

### 相对于基线的方法槽位变更

ToolTree 相对于现有 MCTS 类方法（如 **LATS**，Zhou et al., 2024）的关键槽位变更可归纳如下：

| 方法槽位 | 基线值 | ToolTree 变更 | 证据锚点 |
|---------|--------|-------------|---------|
| 节点选择准则 | 标准 UCT: $Q(s,a)$ + 探索项 | 增强 UCT: 融入 $r_{\mathrm{pre}}$ 偏置早期探索 | Eq. 1 |
| 展开前剪枝 | 无预剪枝，所有合法动作均可展开 | 依据 $r_{\mathrm{pre}}$ 和阈值 $\tau_{\mathrm{pre}}$ 进行 top-K 过滤 | Section 3.2 |
| 回溯更新值 | 使用模拟或终端奖励 | 使用 $r_{\mathrm{post}}$ 作为即时奖励，运行平均更新 $Q$ | Section 3.1 |
| 执行后剪枝 | 无后剪枝，允许在低效分支上继续投资 | $r_{\mathrm{post}} < \tau_{\mathrm{post}}$ 时标记不可扩展 | Section 3.2 |

消融实验提供了这些变更的因果证据：移除后评估组件导致准确率从 76.44 骤降至 68.94（-7.5 个百分点），证实执行后反馈是搜索方向的核心驱动力；移除预评估同样造成显著下降（71.80，-4.64 个百分点），表明前瞻性信号在避免无效分支上的独立价值（Table 3）。



![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Ef5O9gNNLE/figures/002_Figure_2.jpg]]
*Figure 2: Architecture overview of ToolTree. An input query is processed sequentially via iterative dual evaluation-guided Monte Carlo Tree Search, including selection, pre-evaluation, expansion, execution, post-evaluation and backward-propagation. The Answer Predictor then incorporates the tool trajectories with the highest reward found by the MCTS to produce the final prediction*

ToolTree 将多工具使用形式化为一个可执行轨迹上的蒙特卡洛树搜索（MCTS）问题，其核心 pipeline 由七个模块串联构成：**选择 → 预评估 → 展开 → 执行 → 后评估 → 回溯传播 → 答案预测**，形成一个闭环的迭代搜索过程（Figure 2）。

**输入与初始化**：给定用户查询 $q$ 和工具库 $\mathcal{T}_{\text{lib}}$，系统以根节点 $s_0$（包含查询与初始上下文）为起点，初始化空的搜索树。

**选择（Selection）**：从根节点出发，沿树向下遍历直至到达一个尚未完全展开的节点。选择准则采用**先验增强的 UCT 分数**：

$$\mathrm{UCT}(s, a) = Q(s, a) + \lambda r_{\mathrm{pre}}(s, a) \sqrt{\frac{\ln N(s)}{N(s, a)}}$$

其中 $Q(s,a)$ 为动作价值估计，$r_{\mathrm{pre}}(s,a)$ 为预评估分数，$N(s)$ 与 $N(s,a)$ 分别为状态和动作的访问计数，$\lambda$ 为平衡系数。该公式将前瞻性预评估信号直接注入探索-利用权衡，使搜索在早期就能偏向高潜力分支。

**预评估与展开（Pre-Evaluation & Expansion）**：在展开阶段，LLM 首先为当前状态 $s_t$ 下所有合法动作生成预评估分数 $r_{\mathrm{pre}}(s_t, a)$。随后通过**预剪枝**过滤低质量候选：

$$\mathcal{A}^+(s_t) = \{ a \in \mathcal{A}(s_t) : r_{\mathrm{pre}}(s_t,a) \geq \tau_{\mathrm{pre}} \}, \quad \mathcal{A}_{\mathrm{keep}}(s_t) = \text{top-}K(\mathcal{A}^+(s_t); r_{\mathrm{pre}})$$

仅保留预评估分数高于阈值 $\tau_{\mathrm{pre}}$ 且排名前 $K$ 的动作进入展开。这一机制在工具调用执行前即抑制分支膨胀，避免在明显不合理的候选上浪费计算预算。

**执行与后评估（Execution & Post-Evaluation）**：对通过预剪枝的动作，系统实际调用对应工具并获取输出 $o_{t+1}$。LLM 法官随后根据执行结果生成后评估分数：

$$r_{\mathrm{post}}(s_t, a) = J(C_t, a, o_{t+1}) \in [0, 1]$$

该分数反映动作的真实效用。若 $r_{\mathrm{post}}(s_t, a) < \tau_{\mathrm{post}}$，则触发**后剪枝**——将该状态-动作边标记为不可扩展，阻止后续迭代继续在该分支投入预算。

**回溯传播（Backward Propagation）**：沿当前路径自底向上更新统计量，采用增量式运行平均：

$$N(s, a) \gets N(s, a) + 1, \quad Q(s, a) \gets Q(s, a) + \frac{r_{\mathrm{post}}(s_t, a) - Q(s, a)}{N(s, a)}$$

后评估分数 $r_{\mathrm{post}}$ 作为即时奖励驱动 $Q$ 值更新，使搜索方向逐步收敛于实际效用高的轨迹。

**答案预测（Answer Predictor）**：搜索终止后，系统选取累积奖励最高的完整轨迹，将其作为最优工具规划序列输入答案预测器，生成最终回复。

**关键设计要点**：
- **双重反馈闭环**：预评估（$r_{\mathrm{pre}}$）提供前瞻性引导，后评估（$r_{\mathrm{post}}$）提供后顾性验证，二者分别嵌入选择准则和回溯更新，形成“预测-执行-验证”的完整闭环。
- **双向剪枝协同**：预剪枝在展开前压缩候选空间，后剪枝在执行后截断无效分支，二者在不同阶段削减计算开销，使搜索预算自适应集中于高价值区域。
- **缓存与容错**：同一 rollout 内对 $(a, \text{args}) \mapsto o$ 的映射进行缓存以避免重复调用；工具执行失败时附加类型化错误标记，确保剪枝决策基于明确信号而非隐式超时。



ToolTree 将多工具调用形式化为一个可执行轨迹上的蒙特卡洛树搜索（MCTS）过程。其核心设计在于将双重反馈——执行前的预评估（pre-evaluation）与执行后的后评估（post-evaluation）——嵌入搜索的四个关键阶段：选择、展开、回溯更新与双向剪枝。以下按模块拆解关键机制与公式。

### 增强 UCT 节点选择

标准 MCTS 的选择策略依赖 UCT（Upper Confidence Bound for Trees）平衡利用与探索。ToolTree 将预评估分数直接融入 UCT 公式，使搜索在尚未执行动作之前即能偏置探索方向：

$$\mathrm{UCT}(s, a) = Q(s, a) + \lambda \, r_{\mathrm{pre}}(s, a) \sqrt{\frac{\ln N(s)}{N(s, a)}}$$

其中：
- $Q(s, a)$：状态 $s$ 下动作 $a$ 的累积价值估计，由后评估奖励驱动更新；
- $r_{\mathrm{pre}}(s, a)$：由 LLM 在动作执行前生成的预评估分数，预测该动作的潜在效用；
- $N(s)$：状态 $s$ 的访问次数，$N(s, a)$ 为状态-动作对的访问次数；
- $\lambda$：控制预评估先验对探索项贡献的权重系数。

这一设计的因果逻辑在于：传统 UCT 的探索项仅依赖访问计数，对冷启动节点无差别对待；而 $r_{\mathrm{pre}}$ 作为“前瞻信号”在节点被充分采样前即提供启发式引导，使计算预算向高潜力分支倾斜。

### 后评估驱动的价值更新

每次动作执行后，LLM 法官根据实际工具输出生成后评估分数 $r_{\mathrm{post}}(s_t, a) = J(C_t, a, o_{t+1}) \in [0,1]$，其中 $C_t$ 为当前上下文，$o_{t+1}$ 为工具返回结果。该分数作为即时奖励，通过运行平均更新动作价值：

$$Q(s, a) \gets Q(s, a) + \frac{r_{\mathrm{post}}(s_t, a) - Q(s, a)}{N(s, a)}$$

这一增量式更新避免了对完整轨迹回报的依赖，使搜索能够基于单步执行的真实反馈快速调整价值估计。消融实验证实，移除后评估组件导致准确率从 76.44 骤降至 68.94（下降 7.5 个百分点，Table 3），表明执行后的真实反馈是纠正搜索方向的关键驱动力。

### 双向剪枝

ToolTree 在两个阶段压缩搜索空间，形成互补的剪枝机制：

**预剪枝（Pre-pruning）**：在展开前，依据预评估分数过滤低潜力动作。给定阈值 $\tau_{\mathrm{pre}}$ 和保留数 $K$，候选动作集为：

$$\mathcal{A}^+(s_t) = \{ a \in \mathcal{A}(s_t) : r_{\mathrm{pre}}(s_t, a) \geq \tau_{\mathrm{pre}} \}, \quad \mathcal{A}_{\mathrm{keep}}(s_t) = \mathrm{top}\mathcal{K}(\mathcal{A}^+(s_t); r_{\mathrm{pre}})$$

仅 $\mathcal{A}_{\mathrm{keep}}(s_t)$ 中的动作被展开，其余在搜索树中不予生成。实验表明，移除预剪枝使展开节点中位数从约 70 升至 95（Figure 4），验证了其对分支膨胀的抑制效果。

**后剪枝（Post-pruning）**：若某状态-动作对的执行后分数低于阈值 $\tau_{\mathrm{post}}$，即 $r_{\mathrm{post}}(s_t, a) < \tau_{\mathrm{post}}$，则将该边标记为不可扩展，后续搜索不再向该分支分配计算预算。移除后剪枝使模拟次数中位数从约 33 升至 47（Figure 4），说明后剪枝在提前收敛和节省预算上的作用显著。

两条剪枝路径的协同在于：预剪枝在“事前”过滤明显不合理的动作（如模式不兼容的调用），后剪枝在“事后”基于真实执行结果切除无效分支。二者分别作用于展开阶段和模拟阶段，共同提升单位计算预算下的搜索效率。



## 实验与关键发现

### 核心实验设置

ToolTree 在两类工具规划基准上接受评估：**封闭式基准** GTA 与 m&m，以及**开放式基准** ToolBench、RestBench（TMDB 与 Spotify）。所有规划器共享相同的工具模式、描述与类型预筛选管道，工具调用输出与 LLM 调用均采用一致的缓存策略，计算预算在比较时保持对齐。评测指标涵盖工具选择 F1、参数预测 F1、规划 F1、执行 F1（GTA/m&m），以及 Pass Rate 与 Win Rate（ToolBench/RestBench）。骨干 LLM 采用 GPT-4o-mini 与 GPT-4o 两种配置。

### 主结果：封闭式基准

Table 1 报告了 GTA 与 m&m 上 ToolTree 与 8 个基线的对比。ToolTree 在所有配置下均取得最高平均分：

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Ef5O9gNNLE/figures/003_Table_1.jpg]]
*Table 1: Comparison of ToolTree with other baselines across GTA and m&m. The experiment is carried out under both step-by-step and end-to-end mode. ”Tool” stands for tool selection F1 score; $\mathrm { \ " { A r g } ^ { \mathrm { \prime \prime } } }$ stands for argument prediction F1 score; ”Plan” and ”Exec” stand for planning and execution F1 score. Ours achieves the best performance overall

- **GTA (GPT-4o-mini)**：ToolTree 平均 F1 达 55.89，超出最强基线 LATS（53.91）**+1.98** 个百分点。
- **m&m (GPT-4o-mini)**：ToolTree 平均 F1 达 76.90，超出 LATS（75.83）**+1.07** 个百分点。
- **GTA (GPT-4o)**：ToolTree 平均 F1 达 66.95，超出 LATS（64.78）**+2.17** 个百分点。
- **m&m (GPT-4o)**：ToolTree 平均 F1 达 88.61，超出 LATS（86.45）**+2.16** 个百分点，较 Zero-Shot 提升超过 8 个百分点。

这一结果的核心驱动力在于双反馈机制：预评估分数在展开前过滤低潜力动作，避免分支膨胀；后评估分数提供基于真实执行结果的即时奖励，纠正早期次优选择带来的错误累积。相比之下，贪婪策略（ReAct）缺乏前瞻性，标准 MCTS 变体（LATS）虽具备搜索能力但缺少执行后验证与双向剪枝，导致计算资源被浪费在无效分支上。

### 主结果：开放式基准

Table 2 展示了 ToolBench 与 RestBench 上的开放工具集规划结果。ToolTree 的领先优势保持一致：

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Ef5O9gNNLE/figures/005_Table_2.jpg]]
*Table 2: Open-set tool-planning results on RestBench and ToolBench using GPT-4o-mini and GPT-4o as back-end LLMs. Higher values indicate better performance; the best score for each dataset-model pair is highlighted in bold. ”Pass” and ”Win” refer to pass rate and win rate*

- **ToolBench (GPT-4o-mini)**：ToolTree 平均分 55.07，超出 LATS（52.92）**+2.15** 个百分点。
- **ToolBench (GPT-4o)**：ToolTree 平均分 69.04，超出 LATS（66.55）**+2.49** 个百分点。
- **RestBench-TMDB (GPT-4o-mini)**：ToolTree 平均分 62.79，超出 LATS（59.00）**+3.79** 个百分点。
- **RestBench-TMDB (GPT-4o)**：ToolTree 平均分 74.50，超出 LATS（71.35）**+3.15** 个百分点。
- **RestBench-Spotify (GPT-4o-mini)**：ToolTree 平均分 57.74，超出 LATS（56.33）**+1.41** 个百分点。
- **RestBench-Spotify (GPT-4o)**：ToolTree 平均分 71.36，超出 LATS（68.53）**+2.83** 个百分点。

在开放工具集场景下，工具数量更多、依赖关系更复杂，搜索空间呈指数级增长。ToolTree 的双向剪枝在此场景下优势尤为明显：预剪枝依据预评估分数与阈值 $\tau_{\mathrm{pre}}$ 过滤 schema 或槽位不兼容的调用，后剪枝在 $r_{\mathrm{post}} < \tau_{\mathrm{post}}$ 时立即标记该边为不可扩展，阻止后续预算继续投入低效分支。二者协同压缩搜索空间，使有限的计算预算集中于高潜力轨迹。

### 效率分析

Figure 3 展示了不同步数限制（12–128）下的渐进效率对比。ToolTree 在所有步数限制下均取得最高效率曲线，且优势在步数限制 12–64 区间最为显著。这表明 ToolTree 在严格的计算预算约束下仍能保持性能领先——预剪枝减少了需要展开的节点数，后剪枝提前终止了对无效分支的模拟，从而将计算资源自适应地分配给最有希望的搜索方向。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Ef5O9gNNLE/figures/004_Figure_3.jpg]]
*Figure 3: Progressive efficiency analysis across step limits. (a) Performance vs. step limit; (b) Runtime vs. step limit; (c) Efficiency vs. step limit. ToolTree achieves the highest efficiency compared with baselines. mprovements are largest for step limits between 12 and 64*

### 消融实验

Table 3 报告了双评估与双向剪枝的消融结果，揭示了各组件的因果贡献：

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Ef5O9gNNLE/figures/007_Table_3.jpg]]
*Table 3: Ablation of dual evaluation and bidirectional pruning on accuracy and token cost*

- **移除后评估（-Post-evaluation）**：准确率从 76.44 骤降至 68.94，下降 **7.5** 个百分点。这是所有消融项中降幅最大的，证实执行后的真实反馈是搜索方向的核心驱动力。没有后评估，搜索树失去基于实际结果的纠错能力，退化为仅依赖先验预测的盲目搜索。
- **移除预评估（-Pre-evaluation）**：准确率降至 71.80，下降 **4.64** 个百分点。前瞻性信号的缺失使得选择策略无法在展开前区分动作潜力，导致大量计算资源浪费在低质量分支上。
- **同时移除双评估**：准确率进一步跌至 66.70，下降近 **10** 个百分点，验证了预评估与后评估的互补性——前者提供前瞻过滤，后者提供后顾验证，二者缺一不可。

Figure 4 从搜索效率维度补充了消融证据：
- **移除预剪枝**：节点展开数中位数从约 70 跃升至约 95，说明预剪枝有效抑制了分支膨胀。
- **移除后剪枝**：模拟次数中位数从约 33 增至约 47，反映出后剪枝在提前收敛和节省预算上的关键作用。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Ef5O9gNNLE/figures/006_Figure_4.jpg]]
*Figure 4: Efficiency comparison of ToolTree and its pruning variants on nodes and rollouts*

### 可扩展性与鲁棒性

Figure 5 展示了 ToolTree 在 Qwen（0.5B–72B）与 LLaMA（1B–70B）家族上的性能随模型规模的变化。两个模型家族在 GTA 与 ToolBench 上均呈现一致的性能增益趋势，表明 ToolTree 作为训练无关的规划模块，其收益可随骨干 LLM 能力的提升而稳定扩展。

Table 9 分析了 LLM 法官的评估误差对任务成功率的影响。预评估与后评估的判决错误率被独立测量，并与实际 ToolTree 性能的绝对差值（∆）对照。结果表明，即便法官存在一定比例的误判，ToolTree 的整体任务成功率仍保持稳健——双向剪枝的设计使得单点评估错误不会导致搜索方向完全偏离，搜索树的多样性提供了容错缓冲。

### 工具库规模压力测试

Table 11 报告了在 14 工具基线基础上逐步添加干扰工具的压力测试结果。添加 10 个干扰工具（共 24 工具）时，平均 F1 仅下降 0.15%；扩展到 +100 干扰工具（共 114 工具）时，性能退化仍保持在可控范围。这验证了预剪枝机制在大规模工具库场景下的过滤有效性——通过预评估分数与阈值 $\tau_{\mathrm{pre}}$ 的筛选，搜索空间被有效压缩，避免了分支爆炸。

### 失败模式与局限

尽管 ToolTree 在多数场景下表现优异，分析揭示了以下值得关注的边界情况：
- 当预评估与后评估的 LLM 法官同时产生系统性偏差时（例如对特定工具类型的评分持续偏高或偏低），双向剪枝可能误删有效分支或保留无效分支。Table 9 的误差分析为此提供了定量证据。
- 在工具调用输出高度不确定或依赖外部实时状态（如网络 API 的瞬时可用性）的场景中，后评估分数的可靠性下降，可能影响 Q 值更新的准确性。此类场景的鲁棒性需要进一步验证。



## 定位与知识库关联

### 1. 在工具规划方法谱系中的位置

ToolTree 位于**基于搜索的 LLM 工具规划**这一新兴分支，其核心创新在于将规划形式化为蒙特卡洛树搜索问题，并通过双反馈机制与双向剪枝解决现有方法的效率-准确性权衡。

#### 1.1 与贪婪/反应式规划的关系

传统工具规划方法多采用贪婪或反应式策略：
- **ReAct**（Yao et al., 2023b）以交替推理-行动的方式逐步调用工具，但缺乏前瞻性，早期次优选择无法被后续纠正。
- **Chain-of-Thought (CoT)**（Wei et al., 2022）通过思维链引导推理，但不具备工具调用的显式规划机制。

ToolTree 与这些方法的本质区别在于**将规划视为搜索问题**：它维护一棵可执行轨迹树，通过预评估分数在展开前预测工具效用，通过后评估分数在执行后验证实际贡献，从而具备从早期误判中恢复的能力。这种“前瞻预测 + 后顾验证”的双反馈机制是贪婪方法所不具备的。

#### 1.2 与树搜索规划的关系

基于树的搜索规划方法试图克服贪婪策略的短视性，但面临分支爆炸和评价脱节的问题：
- **Tree-of-Thought (ToT)**（Yao et al., 2023a）将推理展开为思维树，但依赖 LLM 自评估而非真实执行反馈。
- **A* Search (ToolChain\*)**（Zhuang et al., 2024）引入启发式搜索，但启发函数的设计与工具执行的真实效用之间缺乏直接关联。
- **LATS**（Zhou et al., 2024）将 MCTS 引入语言代理，是 ToolTree 最直接的对比基线，但其选择准则为标准 UCT，未融入执行前先验，且缺少系统性的双向剪枝机制。
- **DFSDT**（Qin et al., 2023）采用深度优先的符号规划，但在大规模工具空间中的扩展性受限。

ToolTree 相对于上述方法的**关键改进槽位**体现在四个层面：

| 改进槽位 | 基线做法 | ToolTree 做法 | 证据锚点 |
|---------|---------|--------------|---------|
| 节点选择准则 | 标准 UCT: $Q(s,a) +$ 探索项 | 增强 UCT: $Q(s,a) + \lambda r_{\mathrm{pre}}(s,a) \sqrt{\frac{\ln N(s)}{N(s,a)}}$，融入预评估分数偏置早期探索 | Eq. 1 |
| 展开前剪枝 | 无预剪枝，所有合法动作均可展开 | 依据 $r_{\mathrm{pre}}$ 和阈值 $\tau_{\mathrm{pre}}$ 过滤，仅保留 top-K 高潜力动作 | Section 3.2 |
| 回溯更新值 | 使用模拟或终端奖励 | 使用后执行分数 $r_{\mathrm{post}}$ 作为即时奖励，通过运行平均更新 $Q$ 值 | Section 3.1 |
| 执行后剪枝 | 无后剪枝，允许在低效分支上持续投资 | 若 $r_{\mathrm{post}} < \tau_{\mathrm{post}}$，将该边标记为不可扩展，阻止后续预算投入 | Section 3.2 |

这些槽位的协同作用使得 ToolTree 在固定计算预算下自适应分配资源：预评估过滤低潜力节点以抑制分支膨胀，后评估剪除无效分支以提前收敛。

### 2. 适用边界与前提条件

#### 2.1 适用场景

ToolTree 的设计假设和实验覆盖范围表明其适用场景包括：
- **多步工具调用任务**：需要顺序调用多个工具且工具间存在依赖关系的场景（如 GTA、m&m 数据集中的逐步规划）。
- **大规模开放工具集**：当工具库规模较大（如 ToolBench、RestBench）时，预剪枝和后剪枝能有效压缩搜索空间。
- **需要错误恢复的规划**：早期工具选择错误可被后续搜索纠正的场景。

#### 2.2 前提条件与局限

ToolTree 的有效性依赖于以下条件，这些条件也构成了其适用边界：
- **LLM 评估质量**：预评估分数 $r_{\mathrm{pre}}$ 和后评估分数 $r_{\mathrm{post}}$ 均由 LLM 生成，其质量直接影响搜索方向。在 LLM 能力较弱时（如小模型），评估噪声可能导致剪枝误判。
- **工具模式与描述的完整性**：预评估依赖工具的模式和描述信息进行预筛选，若工具描述不准确或不完整，预剪枝可能过滤掉有效动作。
- **计算预算约束**：虽然 ToolTree 在效率上优于基线，但 MCTS 框架本身仍需要多次 LLM 调用来生成评估分数和执行工具，在极端低预算场景下可能不如轻量级贪婪方法。
- **训练无关性**：ToolTree 是训练无关的框架，不涉及模型微调。这意味着其性能上限受限于基座 LLM 的工具使用能力，无法通过训练来内化工具调用模式。

### 3. 开放问题与未来方向

基于 ToolTree 的设计和实验分析，以下问题值得进一步探索：

1. **评估质量的鲁棒性**：当 LLM 生成的预/后评估分数存在系统性偏差时，增强 UCT 的选择策略和双向剪枝的阈值机制如何退化？能否引入校准机制来提升评估可靠性？

2. **阈值自适应**：当前 $\tau_{\mathrm{pre}}$ 和 $\tau_{\mathrm{post}}$ 为固定阈值。在不同任务难度或工具库规模下，自适应调整阈值是否能进一步提升效率-准确率权衡？

3. **与训练方法的结合**：ToolTree 作为训练无关框架，其搜索策略（如增强 UCT 中的 $\lambda$ 权重、剪枝阈值）是否可以通过元学习或强化学习进行优化？

4. **多模态工具规划**：当前验证集中在文本 API 调用场景，双反馈机制在涉及视觉、代码执行等多模态工具时的泛化能力尚未验证。

5. **大规模工具库下的可扩展性**：当工具数量达到数千级别时，预评估的 top-K 筛选和缓存策略是否仍能维持效率优势？

6. **与符号规划的结合**：DFSDT 等符号规划方法在结构化约束推理上具有优势，ToolTree 的搜索框架是否能与符号推理互补，形成混合规划策略？



## 原文 PDF

![[paperPDFs/ICLR_2026/ToolTree_Efficient_LLM_Tool_Planning_via_Dual_Feedback_Monte_Carlo_Tree_Search_and_Bidirectional_Pruning.pdf]]
