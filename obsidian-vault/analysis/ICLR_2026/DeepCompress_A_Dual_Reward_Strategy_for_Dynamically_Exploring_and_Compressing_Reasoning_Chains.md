---
title: "DeepCompress: A Dual Reward Strategy for Dynamically Exploring and Compressing Reasoning Chains"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DeepCompress_A_Dual_Reward_Strategy_for_Dynamically_Exploring_and_Compressing_Reasoning_Chains.pdf
project_link: null
code_link: https://github.com/Skytliang/DeepCompress
openreview_forum_id: K5A2jBmEBK
aliases:
- DeepCompress
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "基于模型感知难度（Simple/Hard）的自适应双重长度奖励（β > 0 激励短响应，β < 0 激励长响应）"
primary_logic: "不是所有问题都应缩短推理链。简单的、已掌握的问题应压缩以提高效率，而困难的、未掌握的问题应延长推理链以增加找到正确解的概率。通过动态地根据模型实时能力（群组通过率 vs 批次通过率）划分问题难度并分配对立长度奖励，DeepCompress能在不牺牲准确率的前提下显著提升标记效率。"
claims:
- "更长的响应包含更广泛的潜在正确解（pass@32随长度增加而增加），而现有方法一味追求更短响应会限制LRM的推理边界。"
- "DeepCompress在所有数学基准上均一致地优于基线方法（如DeepMath-Zero），同时显著降低了平均响应长度。"
- "Math (Average over MATH 500, AMC 23, Olympiad Bench, Minerva Math, AIME 24, AIM... 上 Pass@1 Accuracy (%) = 36.6 (3B), 48.7 (7B)"
- "AIME 2024 上 Pass@1 Accuracy (%) = 16.7 (3B), 23.5 (7B)"
---

# DeepCompress: A Dual Reward Strategy for Dynamically Exploring and Compressing Reasoning Chains

> [!tip] 核心洞察
> 不是所有问题都应缩短推理链。简单的、已掌握的问题应压缩以提高效率，而困难的、未掌握的问题应延长推理链以增加找到正确解的概率。通过动态地根据模型实时能力（群组通过率 vs 批次通过率）划分问题难度并分配对立长度奖励，DeepCompress能在不牺牲准确率的前提下显著提升标记效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DeepCompress：一种动态探索与压缩推理链的双重奖励策略 |
| 英文题名 | DeepCompress: A Dual Reward Strategy for Dynamically Exploring and Compressing Reasoning Chains |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=K5A2jBmEBK) · [GitHub](https://github.com/Skytliang/DeepCompress) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | DeepCompress |
| Dataset | Math (Average over MATH 500, AMC 23, Olympiad Bench, Minerva Math, AIME 24, AIME 25, Poly Math), AIME 2024, Average Response Length (across math benchmarks), GPQA-Diamond / MMLU-STEM / Big-Bench Hard |

> [!tip] 效果简介
> - Math (Average over MATH 500, AMC 23, Olympiad Bench, Minerva Math, AIME 24, AIM... 上，Pass@1 Accuracy (%) 为 36.6 (3B), 48.7 (7B)，对比 34.6 (DeepMath-Zero-3B), 46.0 (DeepMath-Zero-7B)，变化 +2.0 (3B), +2.7 (7B)。
> - AIME 2024 上，Pass@1 Accuracy (%) 为 16.7 (3B), 23.5 (7B)，对比 11.5 (DeepMath-Zero-3B), 19.4 (DeepMath-Zero-7B)，变化 +5.2 (3B), +4.1 (7B)。
> - Average Response Length (across math benchmarks) 上，Tokens 为 Significantly shorter (e.g., DeepCompress-Zero-3B: 57.9% reduction vs DeepMath-Zero-3B)，对比 DeepMath-Zero，变化 57.9% reduction (3B), 16.6% reduction (7B)。

## 概要

当前大语言推理模型（LRM）面临一个核心的**认知效率瓶颈**：模型在简单问题上往往“过度思考”，生成冗长但无必要的推理链；而在复杂问题上又“思考不足”，未能充分探索解空间，导致求解覆盖率受限。现有的基于长度惩罚的强化学习方法（如DeepMath-Zero）强制优化更短的推理链，虽然提升了效率，却以牺牲准确度为代价，尤其限制了困难问题的求解能力。

针对这一瓶颈，DeepCompress 提出了一个**动态探索与压缩推理链的双重奖励策略**。其核心洞察在于：并非所有问题都应缩短推理链。对于模型已掌握的简单问题，应压缩推理长度以提升效率；而对于模型尚未掌握的困难问题，则应延长推理链以增加找到正确解的概率。为此，DeepCompress 引入了一个**模型感知的动态难度分类机制**，通过实时比较问题的群组通过率（Group Pass Ratio）与批次通过率（Batch Pass Ratio）来自适应地将问题划分为“简单”或“困难”，并据此分配**对立的长度奖励**——简单问题激励短响应（β > 0），困难问题激励长响应（β < 0）。

实验结果表明，DeepCompress 在七大数学推理基准测试上一致优于基线方法：DeepCompress-Zero-7B 平均准确率达 48.7%，较 DeepMath-Zero-7B 的 46.0% 提升 2.7 个百分点；在 AIME 2024 上，3B 和 7B 模型分别提升 5.2 和 4.1 个百分点。与此同时，DeepCompress 显著降低了平均响应长度，3B 模型相较基线缩减 57.9% 的标记量，7B 模型缩减 16.6%，在准确率与效率之间实现了更优的平衡。在 GPQA-Diamond、MMLU-STEM 和 Big-Bench Hard 等通用推理基准上，DeepCompress 同样展现出稳定的泛化增益，验证了该方法在数学推理之外的迁移能力。



### 大语言模型的推理能力与认知低效困境

近年来，大语言模型（LLM）在数学、编程等复杂推理任务上取得了显著进展。通过强化学习与链式思考（Chain-of-Thought）的结合，模型能够生成冗长的推理链以求解高难度问题，展现出令人瞩目的推理深度。然而，这种“以长取胜”的范式背后隐藏着一个关键的认知低效问题：**模型对简单问题“过度思考”，对困难问题却“思考不足”**。

具体而言，当面对一个模型已充分掌握的问题时，生成过长的推理链不仅浪费计算资源，还可能引入冗余步骤甚至自相矛盾；而当面对一个超出模型当前能力边界的问题时，过短的推理链则无法提供足够的探索空间，导致模型难以覆盖潜在的正确解。这一现象在数学推理中尤为突出：如图 Figure 1 所示，随着响应长度的增加，模型的 Pass@1 分数反而下降，而 Pass@32 分数却普遍上升。这表明**更长的响应中包含了更广泛的潜在正确解**，但模型自身无法在单次采样中有效利用这种覆盖率的优势。

### 现有长度控制方法的局限性

为应对上述低效问题，研究者开始探索通过强化学习中的长度奖励来调控推理链长度。其中最具代表性的思路是**基于标记长度的惩罚机制**：对生成长度施加负向奖励，强制模型优化出更短的推理链。这类方法虽然在提升标记效率方面取得了一定成效，但其核心缺陷在于**对所有问题一视同仁**——无论是简单题还是难题，都施加相同的缩短压力。

这种“一刀切”的策略带来了一个根本性的权衡困境：**效率的提升往往以牺牲准确度为代价**。在困难问题上，强制缩短推理链会显著限制模型的求解覆盖率，因为模型尚未探索到正确解路径就被迫终止。换言之，现有方法在追求效率的过程中，无意中压缩了模型在困难问题上的推理边界，导致“思考不足”的问题进一步恶化。

### DeepCompress 的核心动机与洞察

本文的核心洞察在于：**不是所有问题都应缩短推理链**。推理链长度的优化应当是一个自适应过程，其调控方向取决于问题相对于模型当前能力的难易程度：

- **简单问题（Simple）**：模型已掌握的问题，应压缩推理链以提高效率，减少冗余思考。
- **困难问题（Hard）**：模型尚未掌握的问题，应延长推理链以增加探索空间，提升找到正确解的概率。

基于这一洞察，DeepCompress 提出了一种**模型感知的动态难度分类机制**与**双重长度奖励策略**。该方法不再依赖静态的外部难度标签，而是根据模型在训练过程中的实时表现——即一个问题在群组中的通过率（Group Pass Ratio）相对于批次平均通过率（Batch Pass Ratio）的高低——动态判定该问题的难易程度。对于简单问题，赋予正向的长度压缩奖励（β > 0），激励模型生成更短的响应；对于困难问题，则赋予负向的长度扩展奖励（β < 0），鼓励模型进行更充分的探索。

通过这种自适应机制，DeepCompress 在数学推理基准上实现了准确率与标记效率的双重提升，打破了传统方法中“效率-准确率”的零和博弈。



## 核心方法与创新机理

DeepCompress 的核心创新在于将“推理链长度”从一个被动的训练副产品，转变为一个由**模型感知难度（Model-Aware Difficulty）** 主动调控的**自适应优化目标**。它通过一个动态、对立的**双重长度奖励（Dual Length Reward）** 机制，替代了以往 Zero RL 流程中对所有问题一视同仁的静态长度惩罚，从而解决了大语言推理模型（LRM）中“简单问题过度思考，困难问题思考不足”的认知低效瓶颈。

### 1. 从静态惩罚到动态对立的双重长度奖励

传统的 Zero RL 方法（如 **DeepMath-Zero** (He et al., 2025)）通常采用恒定的长度惩罚或干脆忽略长度信号，强制模型在所有问题上都追求更短的推理链。这种做法虽然提升了标记效率，但往往以牺牲困难问题的求解覆盖率为代价。

DeepCompress 的核心洞察是：**并非所有问题都应缩短推理链**。如图 Figure 1 所示，虽然 Pass@1 准确率随响应长度增加而下降，但 Pass@32（即从 32 个样本中至少有一个正确的概率）却随长度增加而普遍上升。这揭示了一个关键事实：更长的响应包含了更广泛的潜在正确解，一味追求短链会限制模型的推理边界。

基于此，DeepCompress 设计了对立的长度奖励模式：
- **对于简单问题**：奖励更短的响应（极性参数 $\beta > 0$）。
- **对于困难问题**：奖励更长的响应（极性参数 $\beta < 0$）。

这一机制在奖励函数层面实现：首先，对于同一个问题生成的 $G$ 个回答，计算其标准化长度 $z_i$：
$$z_i = \frac{|\hat{y}_i| - \mu_i}{\sigma_i + \epsilon}$$
然后，通过一个 Sigmoid 函数将标准化长度 $z_i$ 和难度极性 $\beta$ 转化为长度奖励 $R_z$：
$$R_z(\hat{y}, \beta) = \text{sigmoid}(-\beta z_i) = \frac{1}{1 + e^{\beta z_i}}$$
最终的长度奖励 $R_l = \alpha \times R_z(\hat{y}, \beta)$，其中 $\alpha$ 为控制奖励强度的超参数。当 $\beta > 0$ 时，$z_i$ 越小（链越短），$R_z$ 越大，从而激励简洁推理；当 $\beta < 0$ 时，$z_i$ 越大（链越长），$R_z$ 越大，从而鼓励深度探索。

### 2. 模型感知的实时难度分类

如何动态地、无外部标签地判定一个问题是“简单”还是“困难”？DeepCompress 引入了**模型感知难度（Model-Aware Difficulty）** 机制，其核心思想是：**问题的难度不是静态的，而是相对于模型当前能力而言的**。

该机制通过比较两个实时计算的指标来动态确定 $\beta$ 的符号和强度：
- **群组通过率（Group Pass Ratio）** $P_g(x_i)$：一个问题 $x_i$ 的所有 $G$ 个生成回答中，最终答案正确的比例。
  $$P_g(x_i) = \frac{\sum_{j=1}^{G} \mathbb{I}(R_o(\hat{y}_i^j, y_i) = 1)}{G}$$
- **批次通过率（Batch Pass Ratio）** $P_b$：一个训练批次内所有问题的群组通过率的平均值，代表模型当前的全局性能。
  $$P_b = \frac{\sum_{i=1}^{B} P_g(x_i)}{B}$$

难度参数 $\beta$ 被直接定义为两者之差：
$$\beta_i = P_g(x_i) - P_b \quad \in (-1, 1)$$
- 当 $P_g(x_i) > P_b$ 时，$\beta_i > 0$，表示该问题的通过率显著高于模型平均水平，即对当前模型而言是**简单问题**。
- 当 $P_g(x_i) < P_b$ 时，$\beta_i < 0$，表示该问题的通过率低于平均水平，即对当前模型而言是**困难问题**。

这种设计使得难度划分完全自适应于模型训练过程中的能力增长：随着模型变强，$P_b$ 上升，原来的一些“困难”问题可能转变为“简单”问题，其对应的 $\beta$ 也会由负转正，奖励策略随之从“鼓励长链探索”切换为“鼓励短链压缩”。

### 3. 保障训练鲁棒性的关键设计

为确保上述动态机制稳定运行，DeepCompress 引入了两个关键的稳健性增强设计：

**正确性条件化（Correctness-Conditioning）** ：为防止模型通过生成错误但更短的响应来“窃取”长度奖励，长度奖励 $R_l$ 仅被应用于最终答案正确的响应上：
$$R = \begin{cases} R_o + R_l, & \text{if solution } \hat{y}_i \text{ is correct}, \\ R_o, & \text{otherwise}. \end{cases}$$
其中 $R_o$ 为基于规则验证的二元结果奖励（正确为 +1，错误为 -1）。

**EMA 平滑的批次通过率**：为避免训练初期或数据分布波动导致的 $P_b$ 剧烈抖动，从而影响 $\beta$ 估计的稳定性，DeepCompress 对批次通过率进行指数移动平均（EMA）平滑：
$$P_{b,t} = \lambda \cdot P_{b,t-1} + (1 - \lambda) \cdot P_{b,t}^{true}$$
其中 $\lambda$ 为平滑因子（默认 0.99）。如 Figure 6 所示，平滑后的 $P_b$ 在训练过程中呈现稳定增长，验证了难度判断机制的低噪声特性。

综上，DeepCompress 将“推理链长度”从一个被动的静态惩罚项，升级为一个由模型实时能力驱动的、动态对立的主动优化信号，从而在不牺牲准确率的前提下，显著提升了标记效率。



![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_K5A2jBmEBK/figures/003_Figure_2.jpg]]
*Figure 2: Reward values for our DeepCompress method. Subfigure (a) illustrates the reward for Simple Questions, and (b) for Hard Questions. For both, Blue indicates correct responses and Red indicates incorrect responses. The dashed line denotes the baseline outcome reward ( R _ { o } ) , while the solid line represents our final combined reward ( R = R _ { o } + R _ { l } ) , effectively showcasing how our Dual Length Reward ( R _ { l } ) dynamically modulates the reward signal based on standardized response length (z) and question difficulty (β)*

DeepCompress 的核心洞察在于：大语言推理模型（LRM）的认知效率低下，源于其对所有问题无差别地分配推理资源，导致简单问题“过度思考”而困难问题“思考不足”。为破解这一瓶颈，DeepCompress 构建了一个基于模型实时能力的自适应双重奖励框架，其整体流程如下：

1.  **输入与生成**：给定一个数学问题 $x_i$，模型 $\pi_\theta$ 在策略下生成一组 $G$ 个候选回答 $\{\hat{y}_i^1, \dots, \hat{y}_i^G\}$。该过程基于 Group Relative Policy Optimization（GRPO）算法进行优化。
2.  **结果奖励模块**：对于每个候选回答，一个基于规则的二元验证器根据最终答案的客观正确性，赋予 $+1$ 或 $-1$ 的结果奖励 $R_o$。这是框架的基准信号。
3.  **模型感知难度模块**：此模块是框架的“调度中心”。它实时计算两个关键指标：
    *   **局部性能**：问题 $x_i$ 的组内通过率 $P_g(x_i)$，即该问题 $G$ 个生成样本中正确答案的比例。
    *   **全局性能**：整个训练批次的平均通过率 $P_b$，代表模型当前的整体能力水平。
    通过比较局部与全局性能，该模块动态地为每个问题分配一个难度极性参数 $\beta_i = P_g(x_i) - P_b$。若 $\beta_i > 0$，则问题被判定为“简单”（模型对该问题的掌握程度高于平均水平）；若 $\beta_i < 0$，则被判定为“困难”。
4.  **双重长度奖励模块**：该模块根据难度模块输出的 $\beta_i$ 极性，执行完全相反的长度激励策略。
    *   它首先将候选回答的长度 $|\hat{y}_i|$ 在其组内进行标准化，得到 $z_i$。
    *   然后，通过一个 Sigmoid 函数计算长度奖励 $R_z(\hat{y}, \beta) = \text{sigmoid}(-\beta z_i)$。当 $\beta > 0$（简单问题）时，长度越短（$z_i$ 越小），奖励越高，激励模型压缩推理链；当 $\beta < 0$（困难问题）时，长度越长（$z_i$ 越大），奖励越高，激励模型进行更广泛的探索。
5.  **奖励整合与鲁棒性机制**：最终的训练奖励 $R$ 由结果奖励和长度奖励整合而成。为确保训练稳定并防止奖励黑客行为，框架引入了两个关键设计：
    *   **正确性条件化**：长度奖励 $R_l$ 仅被施加于最终答案正确的回答上，杜绝模型通过生成错误但简短的文本来骗取奖励。
    *   **平滑的全局性能**：为防止训练初期或批次波动导致 $P_b$ 剧烈震荡，框架使用指数移动平均（EMA）来平滑 $P_b$，从而为难度分类提供稳定的基准。

通过这一闭环框架，DeepCompress 无需外部难度标签，而是让模型根据自身“能力水位线”动态地、自适应地调整对推理链长度的偏好，最终在提升准确率的同时显著压缩了平均响应长度。



DeepCompress 在 Zero RL 框架（以 **GRPO** (Shao et al., 2024) 为基础 RL 算法）之上引入两个核心创新模块：**双重长度奖励（Dual Length Reward）** 与 **模型感知难度（Model-Aware Difficulty）**。两者协同工作，使模型能根据自身实时能力自适应地调整对不同难度问题的推理链长度偏好。

---

### 1. 结果奖励模块（Outcome Reward Module）

该模块提供基础的正确性信号，采用基于规则的二元验证器，对每个生成的回答 $ \hat{y} $ 赋予 +1 或 -1 的奖励：

$$R_o(\hat{y}, y) = \begin{cases} +1, & \text{if the extracted final answer is exactly correct,} \\ -1, & \text{otherwise.} \end{cases}$$

这一奖励信号仅依赖于最终答案的客观正确性，不涉及推理过程的质量评估，保证了不同方法间比较的公平性。

---

### 2. 双重长度奖励模块（Dual Length Reward Module）

该模块负责对推理链长度施加精细化的奖惩信号，其核心在于引入极性参数 $ \beta $ 来区分“简单”与“困难”问题下的长度偏好方向。

**步骤一：组内标准化长度**

对于第 $ i $ 个问题，将其 $ G $ 个生成回答的长度进行组内标准化，以消除问题本身对生成长度的天然差异：

$$z_i = \frac{|\hat{y}_i| - \mu_i}{\sigma_i + \epsilon}$$

其中 $ \mu_i $ 和 $ \sigma_i $ 分别为该问题组内 $ G $ 个回答长度的均值与标准差，$ \epsilon $ 为防止除零的小常数。标准化后，$ z_i > 0 $ 表示该回答长于组内平均，$ z_i < 0 $ 表示短于组内平均。

**步骤二：基于 Sigmoid 的非线性长度奖励**

将标准化长度 $ z_i $ 通过 Sigmoid 函数映射为有界的长度奖励，并由极性参数 $ \beta $ 控制奖励方向：

$$R_z(\hat{y}, \beta) = \text{sigmoid}(-\beta z_i) = \frac{1}{1 + e^{\beta z_i}}$$

- 当 $ \beta > 0 $（简单问题）：$ R_z $ 随 $ z_i $ 增大而减小，**激励更短的响应**。
- 当 $ \beta < 0 $（困难问题）：$ R_z $ 随 $ z_i $ 增大而增大，**激励更长的响应**。

**步骤三：缩放**

最终长度奖励由超参数 $ \alpha $ 缩放其整体强度：

$$R_l = \alpha \times R_z(\hat{y}, \beta)$$

---

### 3. 模型感知难度模块（Model-Aware Difficulty Module）

该模块动态决定每个问题的难度标签（Simple/Hard），从而确定 $ \beta $ 的符号与大小。其核心思想是：**不依赖外部静态难度标注，而是基于模型自身的实时求解能力来判定难度**。

**关键指标一：组通过率（Group Pass Ratio）**

对于一个问题的 $ G $ 个生成样本，计算其中正确答案的比例：

$$P_g(x_i) = \frac{\sum_{j=1}^{G} \mathbb{I}(R_o(\hat{y}_i^j, y_i) = 1)}{G}$$

$ P_g $ 反映了模型对特定问题 $ x_i $ 的局部掌握程度。

**关键指标二：批次通过率（Batch Pass Ratio）**

对一个批次内 $ B $ 个问题的组通过率取平均，作为模型当前全局性能的估计：

$$P_b = \frac{\sum_{i=1}^{B} P_g(x_i)}{B}$$

**动态 $ \beta $ 的确定**

将局部性能与全局性能的差值直接作为极性参数 $ \beta $：

$$\beta_i = P_g(x_i) - P_b \quad \in (-1, 1)$$

- 当 $ P_g > P_b $，即该问题的通过率高于批次平均时，$ \beta_i > 0 $，问题被判定为 **Simple**，模型应对其压缩推理链。
- 当 $ P_g < P_b $，即该问题的通过率低于批次平均时，$ \beta_i < 0 $，问题被判定为 **Hard**，模型应对其延长推理链以增加求解覆盖率。

这一设计的因果机制在于：$ \beta $ 的绝对值同时编码了难度程度，使得奖励强度自适应地匹配模型对该问题的掌握差距。

---

### 4. 鲁棒性增强设计

**正确性条件化（Correctness-Conditioned Reward）**

为防止模型通过生成错误但更短的响应来“窃取”长度奖励，长度奖励 $ R_l $ 仅被施加到产生正确答案的响应上：

$$R = \begin{cases} R_o + R_l, & \text{if solution } \hat{y}_i \text{ is correct}, \\ R_o, & \text{otherwise}. \end{cases}$$

**批次通过率的指数移动平均（EMA Smoothing）**

为避免训练初期 $ P_b $ 过低或批次间剧烈波动导致 $ \beta $ 估计失准，对批次通过率施加指数移动平均平滑：

$$P_{b,t} = \lambda \cdot P_{b,t-1} + (1 - \lambda) \cdot P_{b,t}^{\text{true}}$$

其中 $ \lambda $ 为平滑因子（默认 0.99），$ P_{b,t}^{\text{true}} $ 为第 $ t $ 步的真实批次通过率。这一设计确保了难度分类信号在训练过程中的稳定性（见 **Figure 6**，训练过程中 $ P_b $ 呈现稳定增长）。



## 实验与关键发现

### 核心结果：数学推理基准

DeepCompress 在七个数学推理基准上全面超越了现有的 Zero RL 基线模型，同时实现了显著的推理链压缩。Table 1 汇总了 Pass@1 准确率的核心对比结果。


![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_K5A2jBmEBK/figures/004_Table_1.jpg]]
*Table 1: Math reasoning performance. “DeepCompress” denotes models trained with our novel DeepCompress approach, which significantly improves the reasoning accuracy*

**3B 规模模型**：DeepCompress-Zero-3B 在七个基准上的平均准确率达到 36.6%，相比 DeepMath-Zero-3B（34.6%）提升了 2.0 个百分点。在具有挑战性的 AIME 2024 基准上，提升幅度最为显著，从 11.5% 跃升至 16.7%（+5.2 个百分点）。在 MATH 500 上，准确率从 72.8% 提升至 75.3%（+2.5 个百分点）。

**7B 规模模型**：DeepCompress-Zero-7B 以 48.7% 的平均准确率在所有模型中取得最高分，超出 DeepMath-Zero-7B（46.0%）2.7 个百分点。同样，AIME 2024 上的增益最为突出，从 19.4% 提升至 23.5%（+4.1 个百分点）。在 AIME 2025 和 Poly Math 等困难基准上，分别实现了 3.6 和 4.3 个百分点的提升。

值得注意的是，DeepCompress 在提升准确率的同时，显著缩短了生成响应的长度。Figure 3 显示，DeepCompress-Zero-3B 的平均响应长度相比 DeepMath-Zero-3B 减少了 57.9%，而 7B 模型也实现了 16.6% 的缩减。这一结果直接验证了核心假设：通过动态区分问题难度并施加对立长度奖励，模型能够在简单问题上“学会压缩”，在困难问题上“学会探索”，从而同时获得效率与准确率的双重收益。


![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_K5A2jBmEBK/figures/006_Figure_3.jpg]]
*Figure 3: Average Response Length across mathematical benchmarks. DeepCompress-Zero models achieve significantly shorter average outputs compared to DeepMath-Zero models*

### 泛化能力验证

为评估方法在数学推理之外的迁移能力，研究者在 GPQA-Diamond、MMLU-STEM 和 Big-Bench Hard 三个通用推理基准上进行了测试（Table 2）。


![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_K5A2jBmEBK/figures/007_Table_2.jpg]]
*Table 2: Performance on the GPQA-Diamond, MMLU-STEM and Big-Bench Hard*

DeepCompress-Zero-3B 在三个基准上分别取得 31.7%、56.0% 和 73.7% 的准确率，全面优于 DeepMath-Zero-3B（29.1%、52.0%、72.5%）。7B 模型同样表现出色，在 GPQA-Diamond 上达到 43.9%，MMLU-STEM 上达到 75.5%，Big-Bench Hard 上达到 85.7%，分别超出基线 1.0、5.6 和 1.1 个百分点。MMLU-STEM 上 5.6 个百分点的显著提升表明，DeepCompress 所培养的自适应推理能力能够有效迁移至科学知识推理等非纯数学任务，而非仅在数学领域过拟合。

### 消融实验与分析

**动态难度分类 vs. 静态策略**：Table 3 的消融对比揭示了动态自适应机制的关键作用。与静态施加“长度惩罚”（始终奖励短响应）或“长度奖励”（始终奖励长响应）的策略相比，DeepCompress 的动态双重奖励在准确率和效率的平衡上均取得最优。静态惩罚策略虽然能缩短长度，但严重损害了困难问题的求解覆盖率；静态奖励策略则导致整体推理链膨胀，效率低下。DeepCompress 通过实时感知模型能力，仅在简单问题上压缩、在困难问题上扩展，避免了单一策略的固有缺陷。


![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_K5A2jBmEBK/figures/012_Table_3.jpg]]

**反思行为的机制解释**：Table 3 进一步揭示了 DeepCompress 在困难问题上提升准确率的行为机制。以 3B 模型为例，DeepCompress-Zero-3B 在困难问题上的平均反思次数为 2.73，高于 DeepMath-Zero-3B 的 2.45，但其平均响应长度却从 11,222 tokens 大幅缩减至 4,853 tokens。这表明模型并非通过无差别地延长推理链来提升性能，而是学会了在困难问题上进行更频繁、更有针对性的反思与自我纠正，同时在简单问题上收敛至更简洁的推理路径。这种“好钢用在刀刃上”的行为模式，正是双重长度奖励与模型感知难度机制协同作用的直接产物。

**超参数鲁棒性**：Figure 5 展示了奖励权重 α 和 EMA 平滑因子 λ 的消融结果。在 α ∈ {0.1, 0.2, 0.5} 和 λ ∈ {0.9, 0.99, 0.999} 的广泛取值范围内，DeepCompress 均一致地优于 DeepMath-Zero-3B 基线（图中虚线所示）。这表明方法对超参数选择不敏感，具有良好的鲁棒性和实际部署可行性。


![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_K5A2jBmEBK/figures/014_Figure_5.jpg]]
*Figure 5: Ablation studies on α and λ. The dashed line represents the DeepMath-Zero-3B baseline*

### 训练动力学

Figure 4 和 Figure 6 从训练过程的角度提供了方法有效性的佐证。Figure 4(a) 显示策略熵在训练过程中保持稳定，未出现灾难性崩溃，表明双重奖励机制未破坏策略的探索能力。Figure 4(c-d) 展示了测试集上 Pass@1 分数的持续提升和响应长度的持续下降，二者同步改善，验证了方法在优化过程中未出现准确率与效率的此消彼长。

Figure 6 监控了平滑批次通过率 P_b 的变化轨迹。P_b 在训练过程中呈现稳定增长，表明模型能力逐步提升。这一稳定性对于模型感知难度分类机制至关重要——如果 P_b 剧烈波动，则基于 P_g - P_b 的动态 β 将失去可靠的参照基准。实验证明 EMA 平滑策略（λ=0.99）有效抑制了批次间的统计噪声，为难度分类提供了稳定锚点。

### 失败模式与局限

尽管 DeepCompress 在数学推理领域取得了显著成效，但分析中仍存在若干值得注意的局限：

1. **规则验证器的固有缺陷**：所有实验均依赖基于规则的结果验证器（Outcome Reward Module），仅根据最终答案的正确性赋予 +1/-1 奖励。这一机制无法区分“推理过程正确但最终答案格式错误”与“推理完全错误”的情况，可能导致模型被训练得过分关注答案格式而非推理质量。在需要部分正确性评估的开放式任务中，这一局限将被放大。

2. **批次统计依赖性**：模型感知难度分类依赖于批次内的问题分布。在极端数据不平衡场景下（例如批次中几乎全是简单题或全是困难题），P_b 的估计可能失真，从而导致 β 的极性判断出现系统性偏差。论文未深入探讨这一边界情况。

3. **任务范围限制**：所有实验集中在数学推理和结构化问答任务上，DeepCompress 在非结构化推理（如长篇创作、多轮对话）中的有效性尚未验证。这类任务中“推理链长度”的定义和奖励方式可能需要根本性的重新设计。



## 定位与知识库关联

### 1. 核心基线：Zero RL 推理范式

DeepCompress 建立在 **Zero RL** 训练范式之上，该范式以纯强化学习（无监督微调）激发大语言模型的推理能力。其直接基线 **DeepMath-Zero**（He et al., 2025）采用 **GRPO**（Shao et al., 2024）作为核心 RL 算法，结合规则验证器提供二元结果奖励（+1/-1），在数学推理任务上取得了有竞争力的表现。其他同期 Zero RL 基线包括 **Open-Reasoner-Zero**（Hu et al., 2025）和 **Qwen-2.5-7B-SRL-ZOO (SimpleRL-Zoo)**（Zeng et al., 2025），以及采用 **DAPO**（Yu et al., 2025）作为 RL 算法的工作。

这些方法的共同瓶颈在于：它们对所有问题施加统一的长度偏好（通常是通过静态惩罚鼓励更短的响应），或者完全忽略长度信号。这导致模型在简单问题上“过度思考”，浪费推理资源，而在困难问题上又因推理链过短而“思考不足”，限制了求解覆盖率。DeepCompress 正是在这一范式下，针对**长度奖励机制**和**难度感知**两个关键槽位进行了创新。

### 2. 关键创新槽位：从静态长度惩罚到自适应双重奖励

| 创新维度 | 基线方法（Zero RL） | DeepCompress |
|---------|-------------------|-------------|
| **长度奖励机制** | 静态长度惩罚或无长度奖励，对所有问题一视同仁地鼓励更短响应 | **双重长度奖励**：根据问题难度动态分配极性相反的奖励——简单问题（β > 0）激励更短响应，困难问题（β < 0）激励更长响应 |
| **难度分类** | 无动态难度感知，或依赖外部静态标签 | **模型感知难度**：基于实时群组通过率（P_g）与平滑批次通过率（P_b）的差值动态判定问题难易，随模型能力演化自适应调整 |

DeepCompress 的核心洞察源于对推理链长度与求解能力关系的重新审视：**Figure 1** 的证据表明，虽然 pass@1 随响应长度增加而下降，但 pass@32 却随长度增加而上升，这意味着更长的响应包含更广泛的潜在正确解。因此，对困难问题一味追求短链会限制模型的推理边界；而对简单问题，短链已足够覆盖正确解，长链则是冗余。

### 3. 方法定位与谱系关系

DeepCompress 在以下维度上区别于现有工作：

- **与纯效率导向方法的区别**：现有基于长度惩罚的 RL 方法（如静态负长度奖励）以牺牲准确度为代价换取效率。DeepCompress 通过正确性条件化（长度奖励仅作用于正确答案，见公式 10）和自适应极性，实现了**准确率与效率的同步提升**，而非简单的权衡。

- **与外部难度标签方法的区别**：DeepCompress 不依赖任何预定义的难度分类，其“模型感知难度”完全基于模型自身的实时表现（P_g vs P_b），使得难度判定随训练动态演化。附录 **Figure 6** 显示，批次通过率 P_b 在训练过程中稳定增长，验证了该机制的噪声极低。

- **与探索增强方法的区别**：DeepCompress 通过 β < 0 的长链奖励隐式地鼓励困难问题上的探索行为。**Table 3** 的证据表明，DeepCompress 在困难问题上触发了更频繁的“反思”（Reflection）行为（3B 模型：2.73 vs 基线 2.45），同时平均响应长度却显著更短（4,853 vs 11,222 tokens），说明其压缩的是简单问题的冗余推理，而非困难问题的必要探索。

### 4. 适用边界与局限

1. **任务范围受限**：当前验证集中在数学推理基准（MATH 500、AIME、AMC 等）和部分结构化推理任务（GPQA-Diamond、MMLU-STEM、Big-Bench Hard）。在非结构化推理任务（如长篇创作、开放域对话）上的有效性尚未验证。

2. **奖励信号的粗粒度**：基于规则验证器的二元结果奖励无法捕获部分正确或推理过程正确的解答。模型可能被训练得过分关注最终答案格式而非推理质量本身。

3. **批次统计依赖性**：动态难度分类依赖于批次内的问题分布统计（P_g, P_b）。在极端数据不平衡场景下（如批次内全部为极难或极易问题），β 的估计可能失准，导致奖励信号偏差。尽管 EMA 平滑（公式 11）缓解了波动，但该机制的稳定性边界尚未深入探讨。

### 5. 开放问题

- **难度信号的精细化**：当前 β 仅基于 P_g 和 P_b 的差值。是否可以引入更丰富的信号——如模型对答案的置信度、生成过程中的困惑度波动、或推理路径的新颖性——来更精细地刻画“难度”和“探索价值”？

- **奖励解耦与多目标优化**：双重奖励机制目前将长度偏好与正确性条件绑定。是否可以进一步解耦，显式地奖励探索新推理路径的“新颖性”，以避免模型在局部最优解附近过早收敛？

- **规模扩展性**：在更大规模模型（如 Qwen-72B、DeepSeek-V2 等）上应用 DeepCompress 时，效率提升和准确率增益的边际收益如何？更强大的基座模型可能本身已具备更好的长度控制能力，自适应奖励的增量价值可能缩小。

- **向开放式任务的扩展**：如何将该框架扩展至需要多个中间步骤奖励的开放式任务中？例如，在代码生成中，是否可以根据测试用例通过率定义“难度”，并在函数级粒度上施加长度奖励？



## 原文 PDF

![[paperPDFs/ICLR_2026/DeepCompress_A_Dual_Reward_Strategy_for_Dynamically_Exploring_and_Compressing_Reasoning_Chains.pdf]]
