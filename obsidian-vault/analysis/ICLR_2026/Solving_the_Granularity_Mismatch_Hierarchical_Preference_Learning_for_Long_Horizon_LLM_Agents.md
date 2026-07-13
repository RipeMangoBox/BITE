---
title: "Solving the Granularity Mismatch: Hierarchical Preference Learning for Long-Horizon LLM Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Solving_the_Granularity_Mismatch_Hierarchical_Preference_Learning_for_Long_Horizon_LLM_Agents.pdf
project_link: null
code_link: null
openreview_forum_id: s8usvGHYlk
aliases:
- HPLH
- SGMHPLLHLA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入语义连贯的动作组作为中间粒度，并采用基于组长度和样本难度的双重课程学习策略，在偏置-方差权衡中取得平衡。"
primary_logic: "通过分层多粒度偏好优化（轨迹级、步级、动作组级）并配合双重课程调度器，使智能体在不同粒度的监督信号中高效学习，从简单子任务逐步过渡到复杂多步序列。"
claims:
- "HPL在所有基准和模型规模上显著优于现有方法，7B模型下平均得分67.28，超过ETO和IPR 3.81和3.46分。"
- "去除课程学习导致平均性能下降2.51分，验证课程的重要性。"
- "去除组级DPO损失对性能影响最大，说明组级监督是关键组件。"
- "ALFWorld (unseen) 上 success rate (%) = 84.08 (HPL Semantic)"
---

# Solving the Granularity Mismatch: Hierarchical Preference Learning for Long-Horizon LLM Agents

> [!tip] 核心洞察
> 通过分层多粒度偏好优化（轨迹级、步级、动作组级）并配合双重课程调度器，使智能体在不同粒度的监督信号中高效学习，从简单子任务逐步过渡到复杂多步序列。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 解决粒度不匹配：长周期LLM智能体的分层偏好学习 |
| 英文题名 | Solving the Granularity Mismatch: Hierarchical Preference Learning for Long-Horizon LLM Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=s8usvGHYlk) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Hierarchical Preference Learning (HPL) |
| Dataset | ALFWorld (unseen), Average across ALFWorld, WebShop, InterCode-SQL, Average across benchmarks (Qwen2.5-1.5B) |

> [!tip] 效果简介
> - ALFWorld (unseen) 上，success rate (%) 为 84.08 (HPL Semantic)，对比 78.11 (IPR)，变化 +5.97。
> - Average across ALFWorld, WebShop, InterCode-SQL 上，average score 为 67.28 (Qwen2.5-7B)，对比 63.82 (IPR)，变化 +3.46。
> - Average across benchmarks (Qwen2.5-1.5B) 上，average score 为 59.44，对比 55.49 (IPR)，变化 +3.95。

## 概要

在长周期LLM智能体任务中，偏好学习的核心瓶颈在于**粒度不匹配**：轨迹级DPO信号稳定但信用分配能力不足，步级DPO提供细粒度监督，但在有限数据与蒙特卡洛采样条件下方差大、效率低。本文提出**Hierarchical Preference Learning (HPL)**，通过引入语义连贯的动作组作为中间粒度，并采用基于组长度和样本难度的双重课程学习策略，在偏置-方差权衡中取得平衡。

HPL的核心洞察是：**分层多粒度偏好优化**（轨迹级、步级、动作组级）配合双重课程调度器，使智能体在不同粒度的监督信号中高效学习，从简单子任务逐步过渡到复杂多步序列。方法遵循两阶段协议——先通过行为克隆初始化策略，再进行一阶段探索生成层次化偏好数据，最后在离线设置下联合优化三级DPO损失。

实验结果表明，HPL在ALFWorld、WebShop和InterCode-SQL三个基准上显著优于现有方法。以Qwen2.5-7B-Instruct为基座，HPL平均得分达到67.28，分别超过轨迹级DPO方法ETO和步级DPO方法IPR 3.81和3.46分。消融实验进一步验证了组级DPO损失和课程学习机制的关键作用：去除课程学习导致平均性能下降2.51分，而去除组级DPO损失对性能影响最大。



### 长周期LLM智能体的偏好学习挑战

大语言模型驱动的自主智能体在长周期交互任务中面临核心瓶颈：如何将稀疏的终局奖励信号高效地转化为每一步决策的信用分配。当前主流的偏好优化方法主要沿两个粒度展开：**轨迹级DPO**与**步级DPO**，但二者各自存在结构性缺陷。

**轨迹级偏好学习**（如ETO，Song et al., 2024）以完整轨迹为优化单元，信号稳定、方差可控。然而，当轨迹跨越数十步交互时，成功或失败的全局标签无法精细定位关键决策点——信用分配能力严重不足，模型难以辨识哪些动作真正贡献了最终结果。

**步级偏好学习**（如IPR，Xiong et al., 2024）将粒度细化到单步动作，试图提供更精准的监督。但其代价显著：在有限数据预算下，步级奖励的蒙特卡洛估计面临高方差问题；单步动作的语义信息往往不足以支撑可靠的偏好判断，导致优化信号噪声大、效率低。

### 粒度不匹配：核心瓶颈

上述困境的本质是**偏好学习的粒度不匹配**问题：轨迹级过粗，步级过细，二者之间缺少一个能够平衡偏置与方差的中间表示层。长周期任务天然具有层次结构——多个连续动作构成语义连贯的子任务单元（如“找到杯子”→“拿起杯子”→“走到水槽”），这些动作组既承载了足够的上下文信息以降低估计方差，又保持了足够的粒度以支撑有效的信用分配。

### 现有方法的缺口

- **单一粒度优化**：ETO和IPR各自仅在单一粒度上施加偏好信号，无法同时利用粗粒度稳定性和细粒度精准性。
- **缺乏结构化课程**：现有方法通常随机混合所有训练样本，忽略了子任务复杂度和样本难度的分布差异，导致学习路径次优——模型可能过早接触复杂多步序列或难以区分的偏好对，训练效率受限。
- **信用分配单位僵化**：以整个轨迹或单个动作为单位进行信用分配，无法匹配任务内在的子任务结构，导致关键决策信号被稀释或淹没。

### 本文动机

针对上述缺口，本文提出**分层偏好学习（Hierarchical Preference Learning, HPL）**框架，核心思路是：

1. **引入动作组级中间粒度**：将专家轨迹分解为语义连贯的动作组，在轨迹级、步级、动作组级三个层次同时施加DPO偏好优化，构建从粗到细的多粒度监督体系。
2. **设计双重课程学习策略**：沿子任务复杂度（组长度）和样本难度（奖励差距）两个正交维度组织训练进程，从简单短序列逐步过渡到复杂长序列，模拟人类从易到难的学习路径。
3. **保持离线偏好优化范式**：HPL遵循与ETO、IPR相同的两阶段协议（单次探索+离线偏好优化），在不引入在线交互成本的前提下实现多粒度偏好学习的集成。



## 核心方法与创新机理

HPL 的核心创新在于用一个**分层多粒度偏好优化框架**系统性地解决了长周期 LLM 智能体偏好学习中的**粒度不匹配**问题。与现有工作仅在单一粒度上操作不同，HPL 引入了三个关键改变：

### 1. 动作组级偏好：填补粒度鸿沟

现有方法在偏好粒度上存在明显分歧：轨迹级 DPO（如 **ETO**, Song et al., 2024）提供稳定但粗粒度的监督，信用分配能力不足；步级 DPO（如 **IPR**, Xiong et al., 2024）提供细粒度监督，但在有限数据与蒙特卡洛采样条件下方差大、效率低。HPL 在这两个极端之间插入了一个**语义连贯的动作组**作为中间粒度，形成了轨迹级、步级、动作组级三级偏好信号。

动作组的核心直觉是：长周期任务中的专家轨迹可以自然分解为若干语义连贯的子任务片段（例如"先找到杯子，再清洗它，最后放到桌子上"）。以这些片段为单位进行偏好学习，既能获得比轨迹级更精细的信用分配，又能避免步级信号的高方差。组级奖励通过蒙特卡洛估计获得：

$$\hat{r}(G_i) = \frac{1}{M} \sum_{j=1}^{M} R(\tau_i^{(j)}), \quad \mathrm{where} \ \{\tau_i^{(j)}\}_{j=1}^{M} = \mathbf{MC}^{\pi_{\mathrm{ref}}}(\tau_{<t_i}; M)$$

### 2. 双重课程学习：从简单到复杂的结构化训练

仅引入多粒度损失并不足以保证高效学习。HPL 的第二个关键创新是**双重课程调度器**，它沿两个正交维度组织训练过程：

- **组长度（L）**：衡量子任务复杂度，短组对应简单子任务，长组对应复杂多步序列
- **样本难度（ΔR）**：定义为获胜组与失败组的奖励差距 $\Delta R = \hat{r}(G_w) - \hat{r}(G_l)$，低 ΔR 表示正负样本难以区分

训练分三个阶段逐步扩展数据范围：Phase 1 仅使用最容易的 $\mathcal{B}_{1,1}$ 桶（短组、低难度）；Phase 2 扩展到 $\mathcal{B}_{1,1} \cup \mathcal{B}_{1,2} \cup \mathcal{B}_{2,1}$；Phase 3 使用全部九个桶 $\bigcup_{L,D} \mathcal{B}_{L,D}$。这一设计使智能体从简单子任务逐步过渡到复杂多步序列，在偏置-方差权衡中取得平衡。

### 3. 联合优化目标

最终训练目标将四个损失项联合优化：

$$\mathcal{L}_{\mathrm{final}}^{(s)} = \mathcal{L}_{\mathrm{BC}} + \mathcal{L}_{\mathrm{traj-DPO}} + \mathcal{L}_{\mathrm{step-DPO}} + \mathcal{L}_{\mathrm{group-DPO}}^{(s)}$$

其中仅组级 DPO 损失随课程阶段动态变化（上标 $s$），轨迹级和步级 DPO 全程参与训练。消融实验（Figure 5）表明，去除组级 DPO 损失对性能影响最大，验证了动作组级监督是整个框架的关键组件。同时，去除课程学习（HPL Static）导致 7B 模型平均得分下降 2.51 分（Table 2），仅使用长度课程或难度课程均不如完整课程，证实了双重课程设计的必要性。

**证据强度说明**：组级 DPO 和双重课程的核心作用有明确的消融实验支持（置信度 0.9–0.95）。语义分割策略依赖外部大模型（如 GPT-4o），引入额外成本和依赖性，这是该方法的一个已知局限。



![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_s8usvGHYlk/figures/002_Figure_2.jpg]]
*Figure 2: An overview of our proposed framework, HPL. Stage 1 generates hierarchical preference data with Action Group Segmentation component. Stage 2 then optimizes the agent with a composite objective, where the training is guided by dual-layer curriculum scheduler*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_s8usvGHYlk/figures/003_Figure_3.jpg]]

HPL 遵循与现有偏好优化工作一致的两阶段协议：**单轮探索 → 离线偏好优化**，但在偏好数据构建与训练调度上进行了层次化重构。如图 2 所示，框架包含两个核心阶段：

### 阶段一：层次化对比数据生成

该阶段的目标是从专家轨迹出发，构建**三个粒度**的偏好对比数据，为后续优化提供多层级监督信号。

1. **行为克隆初始化**：首先在专家轨迹集 $D_{\text{expert}}$ 上通过最大化动作似然训练一个参考策略 $\pi_{\text{ref}}$，作为后续探索和数据生成的基础代理。
2. **轨迹级偏好数据**：使用 $\pi_{\text{ref}}$ 对每条任务指令采样多条完整轨迹，根据最终结果奖励将成功轨迹与失败轨迹配对，形成 $D_{\text{traj}}$。
3. **步级偏好数据**：在专家轨迹的每个时间步 $t$，以历史序列 $\tau_{<t}$ 为条件让 $\pi_{\text{ref}}$ 生成替代动作并完成后续轨迹，将专家后续与替代后续配对，形成 $D_{\text{step}}$。
4. **动作组级偏好数据**：这是 HPL 的核心创新。首先通过**动作组分割**将专家轨迹分解为语义连贯的子任务组 $\{G_1, G_2, ...\}$（支持语义分割、固定长度分割、不确定性分割等策略）；然后对每个动作组 $G_i$ 执行 $M$ 次蒙特卡洛 rollout 估计其奖励 $\hat{r}(G_i)$；最后根据估计奖励将高奖励组与低奖励组配对，形成 $D_{\text{group}}$。

### 阶段二：多粒度偏好优化与双重课程调度

该阶段将三种粒度的 DPO 损失联合优化，并引入**双重课程学习调度器**动态组织训练过程。

**双重课程矩阵**沿两个正交轴组织训练样本：
- **Y 轴（子任务复杂度）**：以动作组长度 $L$ 衡量，短组对应简单子任务，长组对应复杂子任务。
- **X 轴（样本可区分性）**：以奖励差距 $\Delta R = \hat{r}(G_w) - \hat{r}(G_l)$ 衡量，差距大的样本区分度高、学习难度低。

训练按三阶段逐步扩展数据范围：
- **阶段 1（热身）**：仅使用 $B_{1,1}$（短组、高区分度样本）。
- **阶段 2（中间扩展）**：引入 $B_{1,2}$ 和 $B_{2,1}$，扩展至中等复杂度与中等区分度。
- **阶段 3（全量微调）**：使用全部九个桶 $\bigcup_{L,D} B_{L,D}$。

**最终优化目标**在每个课程阶段 $s$ 定义为：

$$\mathcal{L}_{\text{final}}^{(s)} = \mathcal{L}_{\text{BC}} + \mathcal{L}_{\text{traj-DPO}} + \mathcal{L}_{\text{step-DPO}} + \mathcal{L}_{\text{group-DPO}}^{(s)}$$

其中 $\mathcal{L}_{\text{group-DPO}}^{(s)}$ 的数据子集 $\mathcal{D}_{\text{group}}^{(s)}$ 随课程阶段动态变化，而轨迹级和步级 DPO 损失始终使用全量数据。这种设计使模型从简单的、高置信度的子任务开始学习，逐步过渡到复杂的多步序列，在偏置-方差权衡中取得平衡。



HPL框架的核心由四个模块串联构成，分别解决策略初始化、多粒度偏好数据生成、课程调度与联合优化问题。

### 行为克隆初始化 (Behavior Cloning)

在偏好优化之前，HPL首先通过行为克隆在专家轨迹上训练一个初始策略，作为后续阶段的参考策略 $\pi_{\mathrm{ref}}$。该阶段最大化专家动作的似然：

$$\mathcal{L}_{\mathrm{BC}}(\theta; \mathcal{D}_{\mathrm{expert}}) = -\mathbb{E}_{(u,\tau^{*}) \sim \mathcal{D}_{\mathrm{expert}}} \left[ \sum_{t=1}^{|\tau^{*}|} \log \pi_{\theta}(a_t^{*} | s_t^{*}, u, \tau_{<t}^{*}) \right]$$

其中 $u$ 为任务指令，$\tau^{*}$ 为专家轨迹，$\pi_{\theta}$ 为待优化策略。该模块为后续的分层偏好数据生成提供了有能力的参考策略。

### 分层对比数据生成 (Hierarchical Contrastive Data Generation)

该模块在三个粒度层级上构建偏好对，是HPL方法的核心创新之一：

- **轨迹级**：将专家轨迹 $\tau_w$ 与参考策略 $\pi_{\mathrm{ref}}$ 生成的次优轨迹 $\tau_l$ 配对，若 $\tau_l$ 的最终奖励低于 $\tau_w$，则形成偏好对 $(\tau_w, \tau_l)$，构成数据集 $\mathcal{D}_{\mathrm{traj}}$。

- **步级**：在专家轨迹的每一步 $t$，以历史 $\tau_{<t}$ 为提示，让 $\pi_{\mathrm{ref}}$ 生成替代动作并完成剩余轨迹，形成对比对。该过程产生数据集 $\mathcal{D}_{\mathrm{step}}$。

- **动作组级**：这是HPL解决粒度不匹配问题的关键设计。首先将专家轨迹分割为语义连贯的动作组 $G_i$，然后通过蒙特卡洛采样估计每个组的奖励：

$$\hat{r}(G_i) = \frac{1}{M} \sum_{j=1}^{M} R(\tau_i^{(j)}), \quad \text{where } \{\tau_i^{(j)}\}_{j=1}^{M} = \mathbf{MC}^{\pi_{\mathrm{ref}}}(\tau_{<t_i}; M)$$

即从执行完 $G_i$ 后的状态出发，用 $\pi_{\mathrm{ref}}$ 进行 $M$ 次蒙特卡洛展开，取最终结果奖励的平均值作为该组的估计奖励。基于此估计，为每个上下文 $c$ 构造赢家组 $G_w$ 与输家组 $G_l$ 的偏好对，形成 $\mathcal{D}_{\mathrm{group}}$。

### 双重课程调度器 (Dual-layer Curriculum Scheduler)

课程调度器沿两个正交维度组织训练数据的引入顺序：

- **子任务复杂度（Y轴）**：以动作组长度 $L$ 度量，短组优先。
- **样本可区分性（X轴）**：以样本难度 $\Delta R = \hat{r}(G_w) - \hat{r}(G_l)$ 度量，奖励差距大（易区分）的样本优先。

两个维度交叉形成 $3 \times 3$ 的二维矩阵桶 $\mathcal{B}_{L,D}$，训练分三阶段逐步扩展数据子集：

$$\mathcal{D}_{\mathrm{group}}^{(s)} = \begin{cases} \mathcal{B}_{1,1} & \text{if } s=1 \\ \mathcal{B}_{1,1}\cup\mathcal{B}_{1,2}\cup\mathcal{B}_{2,1} & \text{if } s=2 \\ \bigcup_{L,D}\mathcal{B}_{L,D} & \text{if } s=3 \end{cases}$$

### 多粒度偏好联合优化 (Multi-granularity Preference Optimization)

最终训练目标将行为克隆损失与三个粒度的DPO损失联合优化：

$$\mathcal{L}_{\mathrm{final}}^{(s)} = \mathcal{L}_{\mathrm{BC}} + \mathcal{L}_{\mathrm{traj-DPO}} + \mathcal{L}_{\mathrm{step-DPO}} + \mathcal{L}_{\mathrm{group-DPO}}^{(s)}$$

其中三个DPO损失分别定义如下：

- **轨迹级DPO损失**：在完整轨迹上比较成功与失败样本：

$$\mathcal{L}_{\mathrm{traj-DPO}}(\theta;\mathcal{D}_{\mathrm{traj}}) = -\mathbb{E}_{(\tau_w,\tau_l)\sim\mathcal{D}_{\mathrm{traj}}}\left[\log\sigma\left(\beta\log\frac{\pi_\theta(\tau_w|u)}{\pi_{\mathrm{ref}}(\tau_w|u)} - \beta\log\frac{\pi_\theta(\tau_l|u)}{\pi_{\mathrm{ref}}(\tau_l|u)}\right)\right]$$

- **步级DPO损失**：在决策点比较后续轨迹：

$$\mathcal{L}_{\mathrm{step-DPO}}(\theta;\mathcal{D}_{\mathrm{step}}) = -\mathbb{E}_{(\tau_{<t},\tau_{t:n}^w,\tau_{t:m}^l)\sim\mathcal{D}_{\mathrm{step}}}\left[\log\sigma\left(\beta\log\frac{\pi_\theta(\tau_{t:n}^w|\tau_{<t})}{\pi_{\mathrm{eff}}(\tau_{t:n}^w|\tau_{<t})} - \beta\log\frac{\pi_\theta(\tau_{t:n}^l|\tau_{<t})}{\pi_{\mathrm{eff}}(\tau_{t:n}^l|\tau_{<t})}\right)\right]$$

- **组级DPO损失**：在语义连贯的动作组上提供中间粒度监督：

$$\mathcal{L}_{\mathrm{group-DPO}}(\theta;\mathcal{D}_{\mathrm{group}}) = -\mathbb{E}_{(c,G_w,G_l)\sim\mathcal{D}_{\mathrm{group}}}\left[\log\sigma\left(\beta\log\frac{\pi_\theta(G_w|c)}{\pi_{\mathrm{ref}}(G_w|c)} - \beta\log\frac{\pi_\theta(G_l|c)}{\pi_{\mathrm{ref}}(G_l|c)}\right)\right]$$

其中 $\beta$ 控制策略偏离参考策略的惩罚强度，$\sigma$ 为sigmoid函数。组级DPO损失仅在当前课程阶段 $s$ 对应的数据子集 $\mathcal{D}_{\mathrm{group}}^{(s)}$ 上计算，而轨迹级和步级损失在整个训练过程中保持不变。这种设计使得模型在偏置-方差权衡中取得平衡：轨迹级信号稳定但信用分配粗糙，步级信号细粒度但方差大，组级信号作为中间粒度填补了两者之间的空白。



## 实验与关键发现

### 核心瓶颈与验证目标

长周期LLM智能体的偏好学习面临**粒度不匹配**困境：轨迹级DPO信号稳定但信用分配粗糙，步级DPO提供细粒度监督却在有限数据和蒙特卡洛采样下引入高方差。HPL的核心假设是，在轨迹与单步之间引入**语义连贯的动作组**作为中间粒度，并配合**双重课程学习**，能在偏置-方差权衡中取得更优解。实验围绕三个研究问题展开验证：(1) HPL是否显著超越现有单粒度基线？(2) 动作组分割策略如何影响性能？(3) 课程学习机制是否不可或缺？

### 主要结果：跨基准与跨规模的性能优势

Table 1汇总了HPL与四个基线方法（SFT、RFT、ETO、IPR）在ALFWorld、WebShop和InterCode-SQL三个基准上的对比。实验覆盖Qwen2.5-1.5B-Instruct和Qwen2.5-7B-Instruct两个模型规模，所有方法均在相同数据划分和硬件条件下复现，确保公平性。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_s8usvGHYlk/figures/004_Table_1.jpg]]
*Table 1: Performance comparison of HPL and baselines across agent benchmarks over 3 random seeds. All methods are evaluated using Qwen2.5-1.5B-Instruct and Qwen2.5-7B-Instruct as base models. The best and second-best results are highlighted in bold and with an underline, respectively*

**Qwen2.5-7B-Instruct下**，HPL (Semantic) 取得平均得分 **67.28**，分别超出轨迹级方法ETO（Song et al., 2024）**3.81分**和步级方法IPR（Xiong et al., 2024）**3.46分**。在ALFWorld unseen子任务上，HPL (Semantic) 成功率达 **84.08%**，较IPR的78.11%提升**5.97个百分点**（Table 1）。值得注意的是，HPL (Fixed-K(3))在ALFWorld seen子任务上取得**85.71%**的最高分，表明固定分组策略在某些分布内场景下同样有效。

**Qwen2.5-1.5B-Instruct下**，HPL (Semantic) 平均得分 **59.44**，超过IPR **3.95分**（55.49）。这一一致性表明HPL的收益不依赖于特定模型规模，小模型同样能从多粒度监督和课程学习中获益。

Table 6和Table 7的ALFWorld子任务分解进一步揭示：HPL在seen和unseen子任务上均一致优于基线，未见明显的分布外泛化衰减。这暗示动作组级别的监督可能帮助模型学到了更可迁移的子任务结构。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_s8usvGHYlk/figures/018_Table_6.jpg]]
*Table 6: Sub-task success rate (%) comparison on the ALFWorld seen set*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_s8usvGHYlk/figures/019_Table_7.jpg]]
*Table 7: Sub-task success rate (%) comparison on the ALFWorld unseen set*

### 动作组分割策略的影响

论文对比了四种分割策略：**Fixed-K**（固定步数分组）、**Uncertainty**（基于模型不确定性动态分组）、**Semantic**（利用GPT-4o进行语义分割），以及**Static**（无课程学习的对照）。结果（Section 4.2）显示，**自适应、内容感知的分割方法普遍优于启发式方法**：HPL (Semantic) 在7B模型下平均得分67.28，优于HPL (Uncertainty) 约0.35分。这验证了语义连贯的动作组确实提供了更结构化的监督信号（Figure 1c所描绘的理想情况）。

然而，语义分割依赖外部强模型（GPT-4o），引入了额外计算成本和依赖性（Table 5显示HPL Semantic需要外部LLM调用，而其他变体不需要）。这构成了一个实用性与性能的权衡：Fixed-K和Uncertainty策略无需外部模型，在资源受限场景下是可行的替代方案。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_s8usvGHYlk/figures/017_Table_5.jpg]]
*Table 5: Resource comparison of SFT, ETO, IPR, and HPL variants on the ALFWorld benchmark with Qwen2.5-1.5B-Instruct*

### 课程学习机制的消融

Table 2的消融实验直接验证了课程学习的必要性。移除课程学习（HPL Static，即静态混合所有难度和长度的样本）导致7B模型平均得分下降**2.51分**（从67.28降至64.77），1.5B模型下降**0.92分**（从59.44降至58.52）。单独移除长度课程（HPL Difficulty CL Only）或难度课程（HPL Length CL Only）均导致性能下降，完整课程在所有基准上表现最优。这表明**组长度（子任务复杂度）和奖励差距（样本可区分性）两个维度对课程调度均有独立贡献**，仅保留单一维度不足以达到最佳效果。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_s8usvGHYlk/figures/005_Table_2.jpg]]
*Table 2: Ablation study on our curriculum learning mechanism of HPL across three agent benchmarks*

Figure 4通过ALFWorld上的阶段性能进展为课程学习提供了过程性证据。随着训练从Phase 1（仅简单短组）推进到Phase 3（全量数据），两个模型规模的成功率均单调上升。1.5B模型在6个子任务类型上的分解显示，不同子任务对课程的响应存在差异，但整体趋势一致——这暗示课程调度器成功组织了从简单到复杂的学习路径。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_s8usvGHYlk/figures/013_Figure_4.jpg]]
*Figure 4: Phase-wise performance progression of HPL on the ALFWorld benchmark. (a) Success rates for both 1.5B and 7B models across the three curriculum phases. (b) A detailed breakdown for the 1.5B model on 6 sub-task types*

### 损失组件的消融

Figure 5展示了在Qwen2.5-7B-Instruct上逐一移除DPO损失组件的效果。**移除组级DPO损失对性能影响最为严重**，验证了动作组级监督是HPL的核心组件。移除轨迹级DPO或步级DPO同样导致性能下降，但幅度较小。这一结果与HPL的核心假设一致：组级DPO填补了轨迹级和步级之间的粒度空白，提供了最关键的偏置-方差平衡信号。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_s8usvGHYlk/figures/014_Figure_5.jpg]]
*Figure 5: Ablation study on the HPL loss components on Qwen2.5-7B-Instruct*

### 资源开销分析

Table 5对比了各方法在ALFWorld上的资源消耗。HPL (Semantic) 因依赖GPT-4o进行动作组分割，需要额外的外部LLM调用和生成时间。其他HPL变体（Fixed-K、Uncertainty）不需要外部强模型，其LLM调用次数和生成时间与ETO、IPR处于同一量级。这为实际部署提供了参考：在计算预算有限时，HPL (Fixed-K)或HPL (Uncertainty) 仍能提供显著的性能增益，而无外部模型依赖。

### 失败模式与局限性

尽管HPL在整体指标上表现优异，论文未详细报告具体的失败案例分布。基于方法设计可推断以下潜在失败模式：

1. **语义分割质量敏感**：当GPT-4o产生的动作组分割不合理时（例如将逻辑相关的动作错误拆分），组级DPO的监督信号可能引入噪声。这一问题的严重程度在论文中未量化。
2. **课程阶段阈值需手动设定**：Phase 1到Phase 3的过渡依赖预设的组长度和难度阈值，未实现自适应调度。在不同任务分布下，这些阈值可能需要重新调优。
3. **离线评估假设**：所有实验在固定数据集的一阶段探索后进行离线偏好优化，未验证在线RL场景下的有效性。在在线探索中，组级奖励的蒙特卡洛估计可能面临更大的方差挑战。
4. **Fixed-K策略在unseen子任务上的退化**：Table 7显示，HPL (Fixed-K(3))在unseen子任务上（7B模型82.09%）落后于HPL (Semantic)（84.08%）和HPL (Uncertainty)（83.58%），表明固定分组策略的泛化能力弱于自适应方法。

### 关键图表结论摘要

| 图表 | 核心结论 | 证据强度 |
|------|----------|----------|
| Table 1 | HPL在所有基准和模型规模上显著优于单粒度基线，7B下平均领先ETO 3.81分、IPR 3.46分 | 高（多基准、多规模、3次随机种子） |
| Table 2 | 移除课程学习导致7B模型平均性能下降2.51分，长度和难度课程有独立贡献 | 高（系统消融） |
| Figure 5 | 组级DPO损失对性能贡献最大，验证了中间粒度的核心地位 | 中高（单一模型规模） |
| Figure 4 | 课程三阶段推进中性能单调上升，验证了从简单到复杂的调度有效性 | 中（仅ALFWorld基准） |
| Table 5 | HPL (Semantic) 需外部LLM调用，其他变体计算开销与基线可比 | 中（资源对比，非性能指标） |

### 补充图表

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_s8usvGHYlk/figures/015_Table_3.jpg]]
*Table 3: Hyperparamenters for SFT stage across three agent benchmarks*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_s8usvGHYlk/figures/016_Table_4.jpg]]
*Table 4: Hyperparamenters for Group-DPO stage across three agent benchmarks*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_s8usvGHYlk/figures/020_Table_8.jpg]]



## 定位与知识库关联

### 1. 问题定位与核心瓶颈

在长周期LLM智能体任务中，偏好学习的核心瓶颈并非模型容量不足，而是**监督信号的粒度不匹配**。现有方法在两个极端上摇摆：

- **轨迹级DPO**（如 **ETO**, Song et al., 2024）：对整个轨迹进行偏好比较，信号稳定但信用分配能力极弱——智能体无法区分轨迹中哪些动作真正贡献了成功，哪些只是“搭便车”。
- **步级DPO**（如 **IPR**, Xiong et al., 2024）：对每个动作步进行细粒度监督，理论上能精确定位关键决策，但在有限数据和蒙特卡洛采样条件下，单步奖励估计的方差极大，导致优化信号噪声过高、学习效率低下。

HPL的核心洞察是：**在轨迹的“粗”与步的“细”之间，存在一个被忽视的中间粒度——语义连贯的动作组**。这些动作组对应子任务的自然边界，既能提供比轨迹更精细的信用分配，又能通过组内多步的统计聚合降低单步估计的方差，在偏置-方差权衡中取得更优平衡。

### 2. 方法谱系中的位置

HPL处于**离线偏好优化**与**层次化强化学习**的交叉地带，其方法谱系可沿两个维度展开：

**偏好粒度维度**（从粗到细）：
- 行为克隆基线（**SFT**）：无偏好信号，仅模仿专家轨迹。
- 轨迹级偏好：**RFT**（Yuan et al., 2023）基于成功轨迹进行强化微调；**ETO**（Song et al., 2024）引入轨迹级DPO，提供稳定但粗糙的监督。
- 步级偏好：**IPR**（Xiong et al., 2024）将DPO扩展到单步粒度，监督更精细但方差显著增大。
- 多粒度融合：**HPL**同时使用轨迹级、步级和动作组级偏好信号，通过层次化损失组合实现互补监督。

**课程学习维度**：
- 无课程或静态混合：现有方法通常将所有训练样本统一处理，不考虑样本难度或子任务复杂度的差异。
- 双重课程调度：HPL首次将结构化课程引入动作组级偏好优化，沿**组长度**（子任务复杂度）和**奖励差距**（样本难度）两个正交轴动态调度训练数据，从简单子任务逐步过渡到复杂多步序列。

### 3. 适用边界与关键假设

HPL的有效性建立在以下前提之上，超出这些边界时性能可能退化：

1. **离线数据假设**：HPL遵循“一阶段探索 + 离线偏好优化”的两阶段协议，依赖参考策略π_ref生成的探索数据进行偏好学习。在在线RL设置下，该框架的有效性尚未验证。
2. **外部分割模型依赖**：语义动作组分割需要调用外部强模型（如GPT-4o），这不仅增加了计算成本，还引入了对外部API的依赖。当外部模型不可用或分割质量下降时，性能会受到影响（固定分组策略和不确定性分组在某些任务上表现明显弱于语义分割）。
3. **课程阈值的手工设计**：课程阶段的划分、组长度和难度的阈值均需人工设定，缺乏自适应机制。在任务分布显著不同的新领域，这些超参数可能需要重新调整。
4. **组长度选择**：组级DPO的偏置-方差权衡依赖于合理的组长度。过短的组退化为步级DPO（高方差），过长的组退化为轨迹级DPO（弱信用分配），最优组长度因任务结构而异，目前缺乏自动确定机制。

### 4. 局限与开放问题

**已知局限**（论文明确承认或实验揭示）：
- 语义分割策略依赖外部大模型，引入额外成本和公平性考量。
- 课程难度阈值和阶段划分需手动设定，未实现自适应课程学习。
- 实验仅在一阶段探索后的离线设置下进行，未验证在线RL场景。
- 固定分组策略在某些任务上不如语义分割，分割质量直接影响最终性能。

**开放问题**（论文未解决但值得探索的方向）：
- **自监督动作组分割**：能否开发不依赖外部模型的鲁棒分割技术？例如基于轨迹内部的奖励变化或状态转移的突变点检测。
- **自适应课程调度**：能否直接从数据中学习课程调度策略，取代人工设计的阈值和阶段划分？
- **在线扩展**：如何在在线强化学习设置中整合层次化偏好学习，利用在线探索进一步增强组级信用分配的准确性？
- **跨模态泛化**：该方法能否推广到视觉语言模型或多模态智能体任务，其中动作组的语义边界可能需要结合视觉信息定义？
- **最优组长度理论**：组级DPO的偏置-方差权衡是否存在理论上的最优组长度，能否根据任务结构自动推导？



## 原文 PDF

![[paperPDFs/ICLR_2026/Solving_the_Granularity_Mismatch_Hierarchical_Preference_Learning_for_Long_Horizon_LLM_Agents.pdf]]
