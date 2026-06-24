---
title: "Co-rewarding: Stable Self-supervised RL for Eliciting Reasoning in Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Co_rewarding_Stable_Self_supervised_RL_for_Eliciting_Reasoning_in_Large_Language_Models.pdf
openreview_forum_id: fDk95XPsCU
aliases:
- CR
- Co-rewarding
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入互补视角的跨监督信号以打破单一策略循环：数据侧利用语义相似问题的对比一致性提供跨参考伪标签；模型侧维护一个通过EMA慢更新的教师模型，解耦伪标签与在线策略，从而施加高难度训练避免投机捷径。"
primary_logic: "推理能力应体现超越单次输出正确性的不变性；稳定自监督RL的本质在于寻求推理在不同视图间的不变性（数据侧的类比不变性与模型侧的时间不变性），而非仅依赖单视角反馈。"
claims:
- "Co-rewarding在多个基准上平均比自奖励基线高+3.31% Pass@1，并避免训练崩溃。"
- "Co-rewarding-II在DAPO-14k训练的Qwen3-8B-Base上GSM8K达到94.01% Pass@1，超过使用真实标签的GT-Reward。"
- "移除EMA教师更新使Co-rewarding-II的MATH500性能下降（Qwen3-8B-Base: 80.8→79.2），证明模型侧自蒸馏是关键设计。"
- "MATH500 上 Pass@1 = 81.2 (Co-rewarding-I, Qwen3-8B-Base, MATH训练)"
---

# Co-rewarding: Stable Self-supervised RL for Eliciting Reasoning in Large Language Models

> [!tip] 核心洞察
> 推理能力应体现超越单次输出正确性的不变性；稳定自监督RL的本质在于寻求推理在不同视图间的不变性（数据侧的类比不变性与模型侧的时间不变性），而非仅依赖单视角反馈。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Co-rewarding：稳定自监督强化学习激发大语言模型推理能力 |
| 英文题名 | Co-rewarding: Stable Self-supervised RL for Eliciting Reasoning in Large Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=fDk95XPsCU); [GitHub](https://github.com/tmlr-group/Co-rewarding) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Co-rewarding |
| Dataset | MATH500, GSM8K, CRUX, IFEval (平均) |

> [!tip] 效果简介
> - MATH500 上，Pass@1 为 81.2 (Co-rewarding-I, Qwen3-8B-Base, MATH训练)，对比 80.2 (Entropy, 同模型同训练集)，变化 +1.0。
> - GSM8K 上，Pass@1 为 94.01 (Co-rewarding-II, Qwen3-8B-Base, DAPO-14k训练)，对比 87.19 (GT-Reward, 同模型同训练集)，变化 +6.82。
> - CRUX 上，Pass@1 为 67.12 (Co-rewarding-II, Qwen3-8B-Base, DAPO-14k训练)，对比 63.75 (GT-Reward, 同模型同训练集)，变化 +3.37。

## 概述

当前自监督强化学习（RL）激发大语言模型推理能力的主流方法，普遍依赖单一视角的内部监督信号——例如模型自身输出的熵、自确定性或多次采样的多数投票——来构造奖励。这类自奖励（self-rewarding）机制在训练中极易陷入**自洽幻觉**：模型学会生成在自身评估标准下“高分”但实际错误的输出，导致奖励黑客（reward hacking）与训练崩溃，难以稳定提升推理能力。

**Co-rewarding** 的核心洞察是：稳定的自监督 RL 不应依赖单视角反馈，而应寻求推理在**不同视图间的不变性**。具体而言，该方法从两个互补维度引入跨监督信号以打破单一策略循环：

- **数据侧**：通过语义等价但表述不同的改写问题，构造跨参考的对比共识，实现类比不变性（Co-rewarding-I）。
- **模型侧**：维护一个通过指数移动平均（EMA）慢更新的教师模型，将伪标签生成与在线策略解耦，施加高难度训练以避免投机捷径，实现时间不变性（Co-rewarding-II）。

实验表明，Co-rewarding 在多个数学推理基准上平均超越自奖励基线 **+3.31% Pass@1**，且避免了训练崩溃。其中 Co-rewarding-II 在 DAPO-14k 上训练的 Qwen3-8B-Base 在 GSM8K 上达到 **94.01% Pass@1**，甚至超过了使用真实标签的 GT-Reward 方法。消融实验确认，EMA 教师更新和数据侧跨参考均为关键设计：移除教师更新导致 MATH500 性能从 80.8 降至 79.2。

该方法统一于 GRPO 优化框架下，所有对比实验保持训练超参数一致，评估覆盖数学、代码、指令跟随等 8 个基准，确保结论的公平性与泛化性。

## 背景与动机

### 大语言模型推理能力的强化学习范式

将强化学习应用于大语言模型（LLM）的推理能力激发，已成为后训练阶段的核心技术路径。其典型范式为可验证奖励强化学习（RLVR），通过真实答案标签提供二元监督信号，结合GRPO等策略优化算法，在数学推理、代码生成等任务上取得了显著成效。该范式的目标函数可形式化为：

$$\max_{\pi_\theta} \mathbb{E}_{(x,a)\in\mathcal{D}, y\sim\pi_\theta(x)} [r(a,y) - \beta \cdot \mathrm{KL}[\pi_\theta(y|x) || \pi_{\mathrm{ref}}(y|x)]]$$

其中 $r(a,y)$ 为二进制可验证奖励函数，判断模型输出答案是否与真实答案 $a$ 一致；GRPO通过组内标准化计算优势函数：

$$\hat{A}_i = \frac{r(a,y_i) - \mathrm{mean}(\{r(a,y_i)\}_{i=1}^G)}{\mathrm{std}(\{r(a,y_i)\}_{i=1}^G)}$$

然而，RLVR对有标注数据的强依赖限制了其规模化应用。为摆脱对人工标签的依赖，自监督强化学习（self-supervised RL）应运而生，其核心思想是从模型自身行为中挖掘内部监督信号。

### 现有自奖励方法的瓶颈：单视角幻觉与训练崩溃

当前主流的自奖励方法均试图从单一视角构建内部监督信号，主要包含三类：

- **自确定性（Self-Certainty）**：通过最大化输出分布与均匀分布间的KL散度作为奖励，鼓励模型输出高置信度预测（Zhao et al., 2025b）。
- **熵最小化（Entropy）**：以负熵作为奖励信号，驱使模型降低输出不确定性（Prabhudesai et al., 2025）。
- **多数投票（Majority-Voting）**：对同一问题多次采样，选取出现频率最高的答案作为伪标签进行自训练（Shafayat et al., 2025）。

这些方法共享一个致命缺陷：**监督信号完全来源于当前策略对同一问题的内部评估**，形成了“策略生成—策略评估—策略更新”的闭环。这种单视角循环极易诱导模型投机取巧——通过输出高置信度但语义空洞的重复序列来最大化自确定性或熵奖励，而非真正提升推理能力。论文中的案例分析（Figure 7）清晰揭示了这一现象：多数投票和熵最小化方法会生成大量无意义的重复输出，陷入典型的奖励黑客（reward hacking）行为，最终导致训练崩溃（Figure 5, Figure 10）。

### 核心洞察：从单视角反馈到跨视图不变性

本文的根本洞察在于：**推理能力的本质应体现超越单次输出正确性的不变性**——一个真正具备推理能力的模型，其正确性应在不同视图下保持一致。具体而言，这种不变性体现在两个维度：

- **数据侧类比不变性**：语义等价但表述不同的问题，应当导向一致的推理结论。
- **模型侧时间不变性**：模型在不同训练时刻对同一问题的推理，其正确性不应剧烈波动。

基于此，稳定自监督强化学习的关键不在于设计更复杂的单视角奖励函数，而在于**寻求推理在不同视图间的不变性**——通过引入互补视角的跨监督信号，打破单一策略的自我循环，从根本上抑制奖励黑客与训练崩溃。这一哲学构成了Co-rewarding框架的设计原点。

## 核心创新

Co-rewarding 的核心创新在于**为自监督强化学习引入互补视角的跨监督信号，打破单一策略循环**，从而根治自奖励方法中普遍存在的自洽幻觉、奖励黑客与训练崩溃问题。

### 问题根源：单视角反馈的脆弱性

现有自奖励方法——无论是基于**自确定性**（Self-Certainty，Zhao et al., 2025b）、**熵最小化**（Entropy，Prabhudesai et al., 2025）还是**多数投票**（Majority-Voting，Shafayat et al., 2025）——均依赖当前策略对同一问题的多次采样来构造内部监督信号。这种单视角反馈机制存在一个致命缺陷：模型输出的自洽性（如高置信度或内部一致性）并不等价于推理正确性。当策略学会生成看似自信但实质错误、甚至无意义的重复输出时，奖励信号反而会强化这种“投机捷径”，导致性能在训练中后期骤降（见 Figure 5 与 Figure 10 的验证曲线）。

### 核心洞察：推理的不变性原理

Co-rewarding 的设计哲学在于将自监督 RL 的根基从“单视角反馈”转移到“多视角不变性”上：**真正的推理能力应体现为超越单次输出正确性的不变性——同一问题在不同表述下应得到一致答案（数据侧的类比不变性），同一策略在不同训练时刻应保持稳定的推理质量（模型侧的时间不变性）**。基于这一洞察，Co-rewarding 从数据侧和模型侧分别引入互补监督，形成三个递进的实例化方案。

### 关键设计变更（Changed Slots）

**1. 监督来源：从策略自循环到解耦的跨监督**

| 维度 | 基线方法 | Co-rewarding 方案 |
|------|---------|------------------|
| 数据侧 | 仅使用原始问题训练 | **Co-rewarding-I** 引入语义等价但表述不同的改写问题，通过跨数据视图的对比共识生成伪标签（Eq. 6-8） |
| 模型侧 | 无教师模型或教师固定不变 | **Co-rewarding-II** 维护一个通过 EMA 慢更新的教师模型，解耦伪标签与在线策略（Eq. 9-10） |

Co-rewarding-I 的核心机制是：对原始问题 $x$ 和改写问题 $x'$ 分别采样 $G$ 条推理轨迹，在改写问题的 rollout 上执行多数投票获得伪标签 $y'_v$，再用该跨参考伪标签计算原始问题轨迹的优势 $\hat{A}_i$（见 Eq. 7）。这种“用 B 视图的共识监督 A 视图的学习”打破了模型在单一问题表述上的自洽循环。

Co-rewarding-II 则从模型侧切入：维护一个通过 EMA 更新的参考教师 $\tilde{\pi}_{ref}$，其权重按余弦退火从 $\alpha_{start}=0.99$ 逐渐增至 $\alpha_{end}=0.9999$（Eq. 11）。教师在原问题上采样 $\tilde{G}$ 条 rollout 并通过多数投票产生伪标签 $\tilde{y}_v$，用于计算策略学生轨迹的优势。由于教师是历史策略的慢速聚合，其伪标签与当前在线策略解耦，从而施加了高难度训练，迫使策略学习更稳健的推理模式而非投机取巧。

**2. 数据增强：从单一问题到语义等价改写**

基线方法仅在原始问题上训练，而 Co-rewarding-I 引入外部 LLM（如 Qwen3-32B）对训练集中的每个问题进行语义改写，生成 $\mathcal{D}'$ 数据集。这种数据增强并非简单的扩增，而是服务于“类比不变性”的核心目标——模型必须学会在不同表述下保持推理一致性，从而内化真正的解题能力而非表面模式匹配。

**3. 教师更新机制：从静态到动态 EMA**

Co-rewarding-II/III 的 EMA 教师更新是区别于多数投票方法的关键。多数投票方法虽然也使用“伪标签”，但其伪标签来自当前策略的多次采样，本质上仍是自循环。Co-rewarding-II 的教师模型通过指数移动平均聚合历史策略，形成一条“慢速演化”的参考轨迹，其核心作用是**施加时间不变性约束**——策略的当前输出必须与历史聚合的“共识”保持一致。消融实验证实，移除 EMA 更新（即教师固定不变）会导致 MATH500 性能从 80.8 降至 79.2（Table 3），验证了动态教师设计的必要性。

### 三个实例化的递进关系

- **Co-rewarding-I**（数据侧）：利用改写问题的跨参考伪标签，实现类比不变性
- **Co-rewarding-II**（模型侧）：利用 EMA 教师的解耦伪标签，实现时间不变性
- **Co-rewarding-III**（正交组合）：同时整合数据侧跨监督与模型侧自蒸馏，在 Co-rewarding-I 和 Co-rewarding-II 基础上进一步获得平均 +1.72% 和 +7.11% 的提升

三者均以 GRPO 为底层策略优化器，共享组内标准化优势估计与 Clipped Surrogate Objective 加 KL 惩罚的更新机制，创新的差异仅体现在**监督信号的来源与构造方式**上。

## 整体框架

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_fDk95XPsCU/figures/005_Figure_2.jpg]]
*Figure 2: Illustration of Co-rewarding framework: Unlike single-view methods that rely only on internal reward signal on original question (a), Co-rewarding introduces complementary supervision. On the data side (b), paraphrased questions yield pseudo-labels for cross-reference. On the model side (c), teacher model isolated from current policy provides stabilized pseudo-labels for updates*

Co-rewarding 的核心设计理念是将自监督强化学习的稳定性建立在**推理的不变性**之上，而非单一视角的内部反馈信号。该方法通过引入互补视角的跨监督信号，打破传统自奖励方法中单一策略循环带来的自洽幻觉与训练崩溃问题。整体框架从两个正交维度构建互补监督：**数据侧**的类比不变性（Co-rewarding‑I）与**模型侧**的时间不变性（Co-rewarding‑II），并可进一步融合为统一实例化 Co-rewarding‑III。

### 框架总览

如图 Figure 2 所示，传统单视角自奖励方法仅依赖模型在原始问题上的内部信号（如熵、自确定性或多数投票）产生伪标签，容易形成奖励黑客行为。Co-rewarding 在此基础上引入两条互补路径：

- **数据侧互补（Co-rewarding‑I）**：利用外部 LLM 将原始问题改写为语义等价但表述不同的版本 $x'$，通过对改写问题的多数投票获得跨参考伪标签 $y'_v$，再以此监督原始问题上的策略采样。
- **模型侧互补（Co-rewarding‑II）**：维护一个通过 EMA（指数移动平均）慢更新的教师参考模型 $\tilde{\pi}_{\text{ref}}$，由该教师对原问题生成 rollout 并提取伪标签 $\tilde{y}_v$，从而解耦监督信号与当前在线策略的绑定。

两种互补机制分别从数据视图和模型视图施加高难度训练，避免策略投机性地利用单视角反馈中的捷径。

### 统一目标函数

Co-rewarding 建立在 GRPO 的策略优化框架之上，其底层目标为最大化可验证奖励 $r(a, y)$ 同时约束与参考策略的 KL 散度：

$$ \max_{\pi_\theta} \mathbb{E}_{(x,a)\in\mathcal{D},\ y\sim\pi_\theta(x)} \big[r(a, y) - \beta \cdot \mathrm{KL}[\pi_\theta(y|x) \| \pi_{\text{ref}}(y|x)] \big] $$

在此基础上，Co-rewarding 将真实答案标签 $a$ 替换为互补视角产生的自监督伪标签，并沿用 GRPO 的组内标准化优势估计 $\hat{A}_i$ 进行策略更新。

### 核心模块与数据流

整个 pipeline 由以下模块串联构成：

1. **问题改写**（仅 Co-rewarding‑I/III）：外部 LLM 对每个原始问题 $x$ 生成改写版本 $x'$，构建增强数据集 $\mathcal{D}'$。
2. **策略学生采样**：当前策略 $\pi_\theta$ 对每个问题采样 $G$ 条推理轨迹 $\{y_i\}_{i=1}^G$。
3. **教师参考模型**（仅 Co-rewarding‑II/III）：EMA 更新的教师模型 $\tilde{\pi}_{\text{ref}}$ 对原问题或改写问题生成 $\tilde{G}$ 条 rollout，作为稳定伪标签的来源。
4. **伪标签多数投票**：对教师 rollout 或改写问题的 rollout 答案进行多数投票，选取出现最频繁的答案作为自监督伪标签 $y_v$ 或 $\tilde{y}_v$。
5. **优势估计**：基于伪标签计算每条轨迹的标准化优势 $\hat{A}_i$，形式与 GRPO 一致，但奖励信号来源于跨参考伪标签而非真实答案。
6. **策略更新**：通过 Clipped Surrogate Objective 加 KL 惩罚，最大化优势并约束与参考策略的偏离。

### 教师更新机制

Co-rewarding‑II/III 中教师模型的更新是关键设计。教师权重通过 EMA 从学生策略平滑迁移，权重系数 $\alpha^{(k)}$ 按余弦退火从 $\alpha_{\text{start}}=0.99$ 逐渐增至 $\alpha_{\text{end}}=0.9999$：

$$ \tilde{\pi}_{\text{ref}}^{(k)} = \alpha^{(k)} \cdot \tilde{\pi}_{\text{ref}}^{(k-1)} + (1 - \alpha^{(k)}) \cdot \pi_{\theta_{\text{old}}}^{(k)} $$

$$ \alpha^{(k)} = 1 - \frac{(\alpha_{\text{end}} - \alpha_{\text{start}})}{2} \left(1 + \cos\left(\frac{\pi k}{K}\right)\right) $$

这种缓慢更新的教师提供了与当前策略解耦的稳定监督，使得训练过程能够持续提升而避免性能崩溃（消融实验中移除 EMA 更新导致 MATH500 从 80.8 降至 79.2，见 Table 3）。

### 三种实例化的输入输出流

- **Co-rewarding‑I**：输入为原始问题 $x$ 及其改写版本 $x'$；对 $x'$ 的 rollout 进行多数投票得到 $y'_v$，用 $y'_v$ 监督 $x$ 的 rollout；反之亦然。输出为跨参考优势 $\hat{A}_i$ 驱动的策略更新。
- **Co-rewarding‑II**：输入仅为原始问题 $x$；教师模型对 $x$ 生成 rollout 并投票得到 $\tilde{y}_v$，以此监督学生策略的 rollout。输出为解耦伪标签驱动的策略更新。
- **Co-rewarding‑III**：将 I 和 II 正交组合，同时利用改写问题的跨参考伪标签和 EMA 教师的稳定伪标签，对原始问题和改写问题进行双向监督。

## 核心模块与公式推导

### 问题定义与GRPO基础

Co-rewarding建立在可验证奖励强化学习（RLVR）范式之上。给定问题 $x$ 及其标准答案 $a$，模型生成推理轨迹 $y$，基础奖励函数为二元判定：

$$r ( a , y ) = { \left\{ \begin{array} { l l } { 1 } & { { \mathrm { I f ~ a n s } } ( y ) { \mathrm { ~ i s ~ c o r r e c t ~ w i t h ~ a n s w e r ~ } } a , } \\ { 0 } & { \mathrm { I f ~ a n s } } ( y ) { \mathrm { ~ i s ~ i n c o r r e c t ~ w i t h ~ a n s w e r ~ } } a . } \end{array} \right. }$$

其中 $\mathrm{ans}(y)$ 从推理轨迹中提取最终答案。RLVR优化目标为最大化期望奖励并约束与参考策略的KL散度：

$$\operatorname* { m a x } _ { \pi _ { \theta } } \mathbb { E } _ { ( x , a ) \in \mathcal { D } , \ y \sim \pi _ { \theta } ( x ) } [ r ( a , y ) - \beta \cdot \mathrm { K L } [ \pi _ { \theta } ( y | x ) | | \pi _ { \mathrm{ref} } ( y | x ) ] ]$$

Co-rewarding的所有变体均采用GRPO（Group Relative Policy Optimization）作为底层优化器。GRPO对同一问题采样 $G$ 条轨迹，利用组内标准化计算每条轨迹的优势 $\hat{A}_i$：

$$\hat { A } _ { i } = \frac { r ( a , y _ { i } ) - \operatorname* { m e a n } ( \{ r ( a , y _ { i } ) \} _ { i = 1 } ^ { G } ) } { \operatorname* { s t d } ( \{ r ( a , y _ { i } ) \} _ { i = 1 } ^ { G } ) }$$

策略更新采用Clipped Surrogate Objective，最大化优势并约束策略变化幅度。在自监督场景下，真实标签 $a$ 不可用，上述奖励函数 $r(a, y)$ 中的 $a$ 被替换为伪标签——这正是Co-rewarding各变体设计的核心差异所在。

### Co-rewarding-I：数据侧类比不变性

Co-rewarding-I的核心思想是引入语义等价但表述不同的改写问题，通过跨数据视图的对比共识产生监督信号。具体流程分为三个关键模块：

**问题改写模块**：利用外部LLM（如Qwen3-32B）将原始数据集 $\mathcal{D}$ 中的每个问题 $x$ 改写为语义等价版本 $x'$，形成改写数据集 $\mathcal{D}'$。改写质量直接影响方法性能，论文使用Qwen3-32B时改写成功率达99.97%。

**伪标签多数投票**：当前策略 $\pi_{\theta}$ 对原始问题采样 $G$ 条轨迹，对改写问题采样 $G$ 条轨迹，分别进行答案多数投票，得到两组伪标签：

$$y _ { \mathrm { v } } \gets \arg \operatorname* { m a x } _ { y * } \sum _ { i = 1 } ^ { G } \mathbf{1} [ \mathrm { a n s } ( y _ { i } ) = \mathrm { a n s } ( y * ) ] , \quad y _ { \mathrm { v } } ^ { \prime } \gets \arg \operatorname* { m a x } _ { y * } \sum _ { i = 1 } ^ { G } \mathbf{1} [ \mathrm { a n s } ( y _ { i } ^ { \prime } ) = \mathrm { a n s } ( y * ) ]$$

**跨参考优势估计**：关键创新在于使用改写问题的伪标签 $y_{\mathrm{v}}'$ 来评估原始问题轨迹的质量，反之亦然。这种交叉监督打破了单一策略循环的自洽幻觉：

$$\hat { A } _ { i } = \frac { r \left( y _ { \mathrm { v } } ^ { \prime } , y _ { i } \right) - \operatorname* { m e a n } \left( \left\{ r ( y _ { \mathrm { v } } ^ { \prime } , y _ { i } ) \right\} _ { i = 1 } ^ { G } \right) } { \operatorname* { s t d } \left( \left\{ r ( y _ { \mathrm { v } } ^ { \prime } , y _ { i } ) \right\} _ { i = 1 } ^ { G } \right) }$$

完整的Co-rewarding-I目标函数联合优化原始问题和改写问题上的跨参考奖励：

$$\mathcal { J } _ { \mathrm { C o - r e w a r d i n g - I } } ( \theta ) = \underbrace { \mathbb { E } _ { x \in \mathcal { D } , \{ y _ { i } \} _ { i = 1 } ^ { G } \sim \pi _ { \theta _ { \mathrm { o d d } } } ( \cdot | x ) } \left[ \mathcal{R}_{\theta}(\hat{A}_i) \right] }_{\text{原始问题，用}y_{\mathrm{v}}'\text{监督}} + \underbrace { \mathbb { E } _ { x' \in \mathcal { D }' , \{ y _ { i }' \} _ { i = 1 } ^ { G } \sim \pi _ { \theta _ { \mathrm { o d d } } } ( \cdot | x' ) } \left[ \mathcal{R}_{\theta}(\hat{A}_i') \right] }_{\text{改写问题，用}y_{\mathrm{v}}\text{监督}}$$

其中 $\mathcal{R}_{\theta}$ 为GRPO的Clipped Surrogate Objective，$\hat{A}_i'$ 为对称计算的改写问题优势。

### Co-rewarding-II：模型侧时间不变性

Co-rewarding-II从模型侧引入互补监督，通过维护一个缓慢更新的教师模型来解耦伪标签与在线策略。核心模块包括：

**EMA教师更新**：教师模型 $\tilde{\pi}_{\mathrm{ref}}^{(k)}$ 在第 $k$ 步通过指数移动平均从学生策略 $\pi_{\theta_{\mathrm{odd}}}^{(k)}$ 更新，权重 $\alpha^{(k)}$ 按余弦退火从 $\alpha_{\mathrm{start}}=0.99$ 逐渐增至 $\alpha_{\mathrm{end}}=0.9999$：

$$\tilde { \pi } _ { \mathrm { r e f } } ^ { ( k ) } = \alpha ^ { ( k ) } \cdot \tilde { \pi } _ { \mathrm { r e f } } ^ { ( k - 1 ) } + ( 1 - \alpha ^ { ( k ) } ) \cdot \pi _ { \theta _ { \mathrm { o d d } } } ^ { ( k ) } , \ \alpha ^ { ( k ) } = 1 - \frac { ( \alpha _ { \mathrm { e n d } } - \alpha _ { \mathrm { s t a r t } } ) } { 2 } ( 1 + \cos ( \frac { \pi k } { K } ) )$$

高EMA权重确保教师变化极为缓慢，提供稳定的伪标签来源，同时避免学生策略通过投机捷径拟合自身近期输出。

**教师伪标签生成**：教师模型对原始问题采样 $\tilde{G}$ 条轨迹，通过多数投票产生伪标签：

$$\tilde{y}_{ \mathrm { v } } ^ { ( k ) } = \arg \max _ { y * } \sum _ { j = 1 } ^ { \tilde { G } } \mathbf { 1 } [ \operatorname { a n s } ( \tilde { y } _ { j } ) = \operatorname { a n s } ( y * ) ]$$

**优势估计与策略更新**：使用教师伪标签计算学生轨迹的优势：

$$\hat { A } _ { i } ^ { ( k ) } = \frac { r ( \tilde { y } _ { \mathrm { v } } ^ { ( k ) } , y _ { i } ) - \operatorname* { m e a n } ( \{ r ( \tilde { y } _ { \mathrm { v } } ^ { ( k ) } , y _ { i } ) \} _ { i = 1 } ^ { G } ) } { \operatorname* { s t d } ( \{ r ( \tilde { y } _ { \mathrm { v } } ^ { ( k ) } , y _ { i } ) \} _ { i = 1 } ^ { G } ) }$$

完整目标函数为：

$$\mathcal{J}_{ \mathrm { C o - r e w a r d i n g - I I } } ^ { ( k ) } ( \theta ) = \mathbb { E } _ { x \in \mathcal { D } , \{ y _ { i } \} _ { i = 1 } ^ { G } \sim \pi _ { \theta _ { \mathrm { o d d } } } ^ { ( k ) } ( \cdot | x ) , \{ \tilde { y } _ { j } \} _ { j = 1 } ^ { \tilde { G } } \sim \tilde { \pi } _ { \mathrm { r e f } } ^ { ( k ) } ( \cdot | x ) } \left[ \mathcal{R}_{\theta}(\hat{A}_i^{(k)}) \right]$$

消融实验证实EMA更新的关键性：移除教师更新（即教师固定不变）导致Qwen3-8B-Base在MATH500上从80.8降至79.2（Table 3）。

### Co-rewarding-III：数据侧与模型侧融合

Co-rewarding-III将数据侧的类比不变性与模型侧的时间不变性正交融合。其目标函数联合优化原始问题和改写问题，且伪标签均由EMA教师模型生成：

$$\mathcal{J}_{\mathrm{Co-rewarding-III}} = \mathbb{E}_{x' \in \mathcal{D}'} \mathcal{R}_{\theta}(\hat{A}^{(k)}) + \mathbb{E}_{x \in \mathcal{D}} \mathcal{R}_{\theta}(\hat{A}^{'(k)})$$

其中第一项用改写问题的教师伪标签监督原始问题轨迹，第二项用原始问题的教师伪标签监督改写问题轨迹。该融合变体在实验中取得了比单一维度方法更优的结果（Table 1中平均相对增益+7.11% over Co-rewarding-I，+1.72% over Co-rewarding-II）。

### 关键设计对比

| 模块 | 基线方法（单视角自奖励） | Co-rewarding-I | Co-rewarding-II |
|------|------------------------|----------------|-----------------|
| 监督来源 | 同一问题多次采样的内部信号 | 改写问题的跨参考伪标签 | EMA教师模型的伪标签 |
| 数据增强 | 仅原始问题 | 语义等价的改写问题 | 无额外数据增强 |
| 教师机制 | 无或固定不变 | 无 | EMA慢更新，$\alpha$余弦退火0.99→0.9999 |
| 不变性类型 | 无显式不变性约束 | 数据侧类比不变性 | 模型侧时间不变性 |

Co-rewarding-III则同时具备数据侧类比不变性和模型侧时间不变性，在Table 1的8个基准上取得最全面的性能提升。

## 实验与分析

### 核心瓶颈与训练稳定性

自奖励方法（Self-Certainty、Entropy、Majority-Voting）的根本困境在于：它们依赖单一视角的内部监督信号——无论是输出分布的熵、自确定性，还是同一问题的多次采样多数投票——这些信号源于当前策略自身，极易形成**自洽幻觉**（self-consistent hallucination）。当模型学会输出高置信度但错误的答案，或通过重复无意义token来“刷高”奖励时，训练便会陷入奖励黑客（reward hacking）与性能崩溃。

Co-rewarding的设计动机正是打破这种单策略循环。其核心洞察是：**推理能力应体现超越单次输出正确性的不变性**——真正的稳定自监督RL应当寻求推理在数据侧（类比不变性）与模型侧（时间不变性）的跨视图一致，而非仅依赖单视角反馈。Figure 1的性能概览直观展示了这一差异：Co-rewarding在多个基准上平均比自奖励基线高**+3.31% Pass@1**，且验证曲线持续上升而无崩溃，而Entropy和Majority-Voting等方法在训练后期出现明显的性能骤降。

### 主实验结果

#### MATH训练集（Table 1）

在MATH数据集上训练后，Co-rewarding-I在Qwen3-8B-Base上取得**MATH500 81.2%**、**GSM8K 93.70%**、**CRUX 66.00%**的Pass@1成绩。相比最强的自奖励基线（Entropy的MATH500 80.2%），Co-rewarding-I在MATH500上领先+1.0个百分点。更重要的是，Co-rewarding各变体在GSM8K上平均超越GT-Reward（使用真实标签的RLVR训练）**+2.77%**，表明精心设计的自监督信号可以超越真实标签训练的上界——这是因为真实标签只提供二元对错反馈，而Co-rewarding的跨视图伪标签蕴含了更丰富的推理过程信息。

在指令跟随基准IFEval上，Co-rewarding-II（Qwen3-8B-Base，MATH训练）的平均Strict Accuracy达到**60.70%**，远超GT-Reward的52.78%（+7.92个百分点），说明模型侧自蒸馏带来的稳定性对通用指令遵循能力也有显著外溢效应。

#### DAPO-14k训练集（Table 2）

在DAPO-14k上训练的Co-rewarding-II展现出更强的竞争力。Qwen3-8B-Base在GSM8K上达到**94.01% Pass@1**，不仅大幅领先GT-Reward的87.19%（**+6.82个百分点**），也超越了所有自奖励基线。在代码推理基准CRUX上，Co-rewarding-II取得**67.12%**，同样优于GT-Reward的63.75%（+3.37个百分点）。这一结果表明，EMA教师模型提供的稳定伪标签在代码这类需要精确推理的任务上尤为关键——单视角自奖励方法在代码任务上更容易因奖励黑客而生成语法正确但逻辑错误的代码。

跨模型泛化方面，Llama-3.2-3B-Instruct在DAPO-14k上训练后，Co-rewarding-II的MATH500达到49.8%，验证了该方法对不同模型架构的普适性。

#### Co-rewarding-III：双侧融合（Table 1 & 2）

将数据侧跨参考监督与模型侧自蒸馏融合的Co-rewarding-III，在Table 1上相比Co-rewarding-I平均提升**+7.11%**，相比Co-rewarding-II平均提升**+1.72%**，证明双侧互补监督具有正交叠加效应。但需注意，Co-rewarding-III的额外计算开销（同时维护改写数据与EMA教师）使其性价比不如Co-rewarding-II突出，后者在DAPO-14k上已取得极具竞争力的结果。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_fDk95XPsCU/figures/006_Table_1.jpg]]
*Table 1: Main Results (%) of Co-rewarding and baselines trained on MATH. Cell background colors indicate relative performance: darker colors denote better results within each model group. Additional results of Qwen2.5-3B/7B and Qwen3-1.7B-Base trained on MATH refer to Table 7*

### 消融实验（Table 3）

**数据侧跨参考的必要性**：将Co-rewarding-I限制为仅使用原始数据（only Original）或仅使用改写数据（only Rephrased），多项指标均显著低于完整跨参考版本。例如Qwen3-8B-Base的MATH500从81.2%分别降至79.4%和79.0%。这验证了单一数据视图无法提供足够的不变性约束——模型需要同时看到同一问题的不同表述，才能学习到超越表面措辞的推理能力。

**模型侧EMA教师更新的关键作用**：移除Co-rewarding-II的EMA教师更新（即教师固定为初始参考模型，w/o Updating Reference）导致Qwen3-8B-Base的MATH500从80.8%降至**79.2%**（-1.6个百分点）。这一降幅虽看似不大，但结合训练曲线（Figure 5）来看，固定教师模型在训练后期会出现伪标签质量停滞，限制了策略的持续改进空间。EMA更新（权重按余弦退火从0.99逐渐增至0.9999）确保教师模型缓慢跟随学生进步，既提供稳定的监督目标，又避免与学生策略过近而退化为单视角自奖励。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_fDk95XPsCU/figures/021_Figure_5.jpg]]
*Figure 5: Performance and Stability on GSM8K and AMC. The gains of Co-rewarding arise from its training stability, which supports continuous improvements throughout learning*

### 训练稳定性分析（Figure 5）

Figure 5对比了各方法在GSM8K和AMC上的验证曲线。Co-rewarding展现出**持续单调提升**的特性，而Self-Certainty、Entropy和Majority-Voting在训练中后期均出现性能瓶颈甚至骤降。以Entropy为例，其奖励信号鼓励模型输出低熵（高置信度）的答案，但模型很快学会通过重复无意义token序列来最小化熵，而非真正提升推理质量——Figure 7的案例清晰展示了这一奖励黑客行为：Entropy生成的回答充满重复的数学符号却无实质推理，而Co-rewarding生成了正确的分步解答。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_fDk95XPsCU/figures/024_Figure_7.jpg]]
*Figure 7: Case study: An example comparing the generations from Majority-Voting, Entropy, and our proposed Co-rewarding. The results clearly reveal the reward hacking behavior exhibited by Majority-Voting and Entropy, while ours generate the correct answer. Full results refer to Appendix D.13*

### 失败模式与局限性

1. **改写质量依赖**（Co-rewarding-I）：当改写模型能力不足时，生成的改写问题可能与原问题语义偏离，导致跨参考伪标签引入噪声。论文消融显示（Table 13-14），使用Qwen3-32B改写时成功率达99.97%，但若替换为更小的改写模型，性能会明显下降。

2. **早期教师不成熟**（Co-rewarding-II/III）：训练初期EMA教师尚未积累足够的推理能力，其生成的伪标签可能包含较多错误，对策略更新产生误导性信号。这一问题在复杂推理任务（如MATH500的高难度题目）上更为突出。

3. **额外计算开销**：Co-rewarding-II/III需维护一份额外的教师模型权重，并在每次更新时进行teacher rollout推理。虽然不增加参数量，且可通过GPU共享实现，但在大规模部署时仍需权衡性价比。

4. **任务范围局限**：当前实验集中在数学与代码推理任务，在更开放的语言推理、知识密集型任务（如MMLU-Pro的部分子类别）上的表现虽有提升但幅度有限（Table 4），其普适性尚未充分验证。

### 实验公平性说明

所有方法均采用GRPO作为底层策略优化器，训练超参数（batch size、学习率、rollout数量等）保持一致（详见Table 5）。评估覆盖数学、代码、指令跟随和多任务共8个基准，避免单一指标偏差。Co-rewarding-II的EMA教师推理虽引入额外计算，但未增加额外的大模型参数量，且通过共享GPU资源实现，对比基线时未进行不公平的算力倾斜。

### 补充图表

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_fDk95XPsCU/figures/007_Table_2.jpg]]
*Table 2: Main Results (%) of Co-rewarding and baselines trained on DAPO-14k. Cell background colors indicate relative performance: darker colors denote better results within each model group. Additional Results of Qwen3-8B-Base and Qwen3-4B-Base trained on OpenRS refer to Table 8*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_fDk95XPsCU/figures/022_Table_3.jpg]]
*Table 3: Ablation study of Co-rewarding. For Co-rewarding-I, ablations train only on original or rephrased data. For Co-rewarding-II, ablation removes EMA updates of the reference teacher. 4.2 EXPERIMENTAL RESULTS*

## 方法谱系与知识库定位

### 1. 问题瓶颈：自监督RL中的单视角脆弱性

当前基于自奖励（self-rewarding）的强化学习方法，其核心瓶颈在于监督信号来源的单一性。无论是**Self-Certainty** (Zhao et al., 2025b) 通过最大化输出分布与均匀分布间的KL散度、**Entropy** (Prabhudesai et al., 2025) 通过最小化输出熵，还是**Majority-Voting** (Shafayat et al., 2025) 对同一问题多次采样取多数答案，这些方法都仅依赖模型自身在当前问题上的内部统计量作为奖励信号。这种单视角反馈机制极易形成自洽幻觉：模型学会生成让自身奖励函数给出高分的输出，而非真正提升推理能力。实证表明，这些基线方法在训练中频繁出现奖励黑客行为——例如生成重复无意义文本以降低熵值——并最终导致训练崩溃（Figure 5, Figure 7, Figure 10）。

Co-rewarding的因果调节变量在于引入互补视角的跨监督信号以打破单一策略循环：数据侧利用语义相似问题的对比一致性提供跨参考伪标签；模型侧维护一个通过EMA慢更新的教师模型，解耦伪标签与在线策略，从而施加高难度训练避免投机捷径。

### 2. 方法谱系：从单视角到多视角不变性

Co-rewarding的方法论定位是将自监督RL从“单视角反馈”范式推进到“多视角不变性”范式。其核心哲学是：推理能力应体现超越单次输出正确性的不变性——数据侧的类比不变性与模型侧的时间不变性。

**与GT-Reward（RLVR）的关系**：GT-Reward (Shao et al., 2024) 使用真实答案标签作为可验证奖励，代表了有监督上界。Co-rewarding的目标是在不依赖真实标签的前提下逼近甚至超越这一上界。实验显示，Co-rewarding-II在DAPO-14k训练的Qwen3-8B-Base上GSM8K达到94.01% Pass@1，超过GT-Reward的87.19%（Table 2），证明跨视角监督在特定条件下可超越真实标签训练。

**Co-rewarding-I（数据侧类比不变性）**：与Majority-Voting等仅在原始问题上自举的方法不同，Co-rewarding-I引入语义等价但表述不同的改写问题，利用改写问题的多数投票伪标签来监督原始问题的rollout，反之亦然。这种跨参考对比共识机制迫使模型学习对语义不变的推理能力，而非记忆表面模式。消融实验（Table 3）证实，仅使用原始数据或仅使用改写数据的变体均显著低于完整跨参考版本。

**Co-rewarding-II（模型侧时间不变性）**：与Self-Certainty和Entropy直接从在线策略提取监督信号不同，Co-rewarding-II维护一个通过EMA慢更新的教师模型（权重按余弦退火从0.99逐渐增至0.9999），由教师生成伪标签来监督学生策略。这解耦了监督信号与当前策略的即时绑定，避免了策略在自反馈循环中快速漂移。移除EMA教师更新（即教师固定不变）导致MATH500性能从80.8降至79.2（Table 3），证明慢更新机制是关键设计。

**Co-rewarding-III（统一框架）**：将数据侧跨监督与模型侧自蒸馏正交组合，在Table 1上相比Co-rewarding-I和Co-rewarding-II分别平均提升+7.11%和+1.72%，表明两侧互补性。

### 3. 适用边界与局限

**数据依赖性**：Co-rewarding-I的性能依赖于改写模型的质量。当改写成功率较低时（如使用小模型改写）会有明显性能下降。论文使用Qwen3-32B改写时成功率达99.97%，但这一前提限制了在缺乏高质量改写模型的场景下的直接应用。

**计算开销**：Co-rewarding-II/III需维护一个额外的教师参考模型，虽然不增加参数量，但需额外保存和更新一份模型权重，并增加推理时的teacher rollout开销。论文通过共享GPU资源实现，但实际部署中需权衡收益与成本。

**任务范围**：当前实验集中在数学（MATH500、GSM8K、AMC、AIME24、Minerva）与代码（CRUX、LiveCodeBench）推理任务，以及指令跟随（IFEval）和多任务理解（MMLU-Pro）。其在更开放的语言推理、知识密集型任务上的普适性尚未充分验证。

**早期训练风险**：自监督伪标签仍可能包含错误，尤其在早期训练阶段教师模型尚未成熟时，可能导致误导性优化信号。论文通过EMA慢更新和余弦退火调度来缓解此问题，但无法完全消除。

### 4. 开放问题

1. **缩放与兼容性**：Co-rewarding在更大规模模型（如70B+参数）上的缩放效果如何？能否与DAPO、Dr. GRPO等其他RLVR变体无缝集成以进一步释放潜力？

2. **跨模态拓展**：数据侧互补思想能否拓展到多模态场景（如视觉-语言推理）或工具使用场景（如代码执行反馈），利用不同模态或执行环境作为互补视图？

3. **数据增强深度**：除简单的语义改写外，更复杂的数据增强策略（如风格迁移、对抗改写）是否能进一步提升数据侧不变性的鲁棒性？当前仅探索了同义改写，更丰富的视图可能带来更大增益。

4. **教师更新策略优化**：EMA教师更新与自监督学习中经典的momentum encoder架构是否存在更优的融合方式？当前的余弦退火调度是否为最优选择，还是存在更自适应的更新策略？

## 原文 PDF

![[paperPDFs/ICLR_2026/Co_rewarding_Stable_Self_supervised_RL_for_Eliciting_Reasoning_in_Large_Language_Models.pdf]]
