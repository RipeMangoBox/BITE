---
title: "SafeDPO: A Simple Approach to Direct Preference Optimization with Enhanced Safety"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SafeDPO_A_Simple_Approach_to_Direct_Preference_Optimization_with_Enhanced_Safety.pdf
project_link: null
code_link: null
openreview_forum_id: PJdw4VBsXD
aliases:
- SafeDPO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "安全边际 Δ（控制安全与不安全响应的对数概率差距，在不改变最优解的前提下增强安全性）。"
primary_logic: "原始硬约束安全对齐目标存在封闭形式最优策略，可通过安全感知的数据对变换将难处理的目标转化为标准DPO风格的损失函数，直接优化而无需辅助模型。"
claims:
- "硬约束安全对齐目标在温和假设下等价于无约束目标，且最优策略天然排除不安全响应。"
- "安全感知转换T(𝒟)使经验数据集上的SafeDPO目标与理论难处理目标等价。"
- "引入安全边际Δ不改变最优解集。"
- "在PKU-SafeRLHF-30K上，SafeDPO将无害率提升至约97%（模型评测）和100%（GPT-4评测），远超DPO-HELPFUL（38.6%模型评测）。"
---

# SafeDPO: A Simple Approach to Direct Preference Optimization with Enhanced Safety

> [!tip] 核心洞察
> 原始硬约束安全对齐目标存在封闭形式最优策略，可通过安全感知的数据对变换将难处理的目标转化为标准DPO风格的损失函数，直接优化而无需辅助模型。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SafeDPO：增强安全性的直接偏好优化简易方法 |
| 英文题名 | SafeDPO: A Simple Approach to Direct Preference Optimization with Enhanced Safety |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=PJdw4VBsXD) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | SafeDPO |
| Dataset | PKU-SafeRLHF-30K (模型评测), PKU-SafeRLHF-30K (GPT-4评测) |

> [!tip] 效果简介
> - PKU-SafeRLHF-30K (模型评测) 上，无害率 (%) 为 97.24，对比 38.6 (DPO-HELPFUL)，变化 +58.64。
> - PKU-SafeRLHF-30K (模型评测) 上，无害性 (平均负成本) 为 5.92，对比 -2.24 (DPO-HELPFUL)，变化 +8.16。
> - PKU-SafeRLHF-30K (模型评测) 上，有用性 (归一化奖励) 为 4.86，对比 10.0 (DPO-HELPFUL, 锚定值)，变化 -5.14。

## 概要

大语言模型的安全对齐是部署前的关键步骤，但主流方法存在明显瓶颈。以 **SafeRLHF**（Dai et al., 2023）为代表的现有方案依赖辅助奖励模型、成本模型和多阶段在线采样训练，计算与概念复杂度高；同时，它们通常采用松弛的期望约束而非严格硬约束，无法从原理上杜绝不安全输出。SafeDPO 针对这两个瓶颈，提出了一条极简路径：**在温和假设下，原始硬约束安全对齐目标存在封闭形式的最优策略，该策略天然排除不安全响应**；基于此，SafeDPO 将难处理的约束优化目标转化为标准 DPO 风格的损失函数，仅需对偏好数据对进行安全感知的重排序/过滤，并引入一个额外的安全边际超参数 $\Delta$，即可实现单阶段、无需辅助模型的直接策略优化。

核心机制包含两个因果旋钮。其一是**安全感知数据变换 $T(\mathcal{D})$**：根据二元安全标签，若首选响应不安全而次选安全则交换二者，双不安全则丢弃该对，从而在经验数据集上精确恢复理论目标。其二是**安全边际 $\Delta$**：在变换后的数据上对安全-不安全对施加额外的对数概率差距惩罚，且理论保证不改变最优解集（Proposition 4.4）。消融实验表明，安全感知变换是安全改进的关键——仅靠数据集过滤（DPO-SAFEBETTER）或为 DPO 变体添加边际均无法达到同等安全水平。

在 PKU-SafeRLHF-30K 基准上，SafeDPO 将无害率从 DPO-HELPFUL 的 38.6% 提升至约 97%（模型评测）和 100%（GPT-4 评测），同时保持有竞争力的有用性。方法在不同模型规模（1.5B–13B）和随机种子上表现稳健，训练效率约为 SafeRLHF 的 24 倍，且所需网络组件和标注信号大幅减少。主要局限在于：仅在一个安全对齐数据集上验证，模型规模限于 13B，高安全边际下有用性可能受损，GPT-4 自动评估存在安全性与有用性评分耦合问题，且在 XSTest 上展现出 12.4% 的过度拒绝率。

大型语言模型（LLM）的安全对齐是确保其在真实部署中不产生有害输出的核心挑战。当前主流的安全对齐范式，如基于人类反馈的强化学习（RLHF），通常依赖辅助奖励模型和成本模型，并通过多阶段在线策略优化（如PPO-λ）来平衡有用性与无害性。然而，这类方法存在两个根本性瓶颈：

**计算与概念复杂性**：以SafeRLHF（Dai et al., 2023）为代表的安全对齐方法需要额外训练奖励模型、成本模型及其价值函数，并在训练过程中执行昂贵的在线采样与策略评估。这种多阶段、多组件的训练流程显著增加了内存开销和计算时间——SafeRLHF的训练时间约为SafeDPO的24倍（Table 15），且需要更多类型的标注信号（Table 16）。

**松弛约束的局限性**：现有方法通常将安全对齐建模为带松弛期望约束的优化问题，而非严格硬约束。这意味着在最优策略下，不安全响应仍可能以非零概率出现，无法从根本上杜绝有害输出。这种“惩罚但不禁止”的策略在安全攸关场景中留下了系统性风险。

针对上述缺口，本文的核心动机在于探索一条更简洁、更彻底的路径：**能否在直接偏好优化（DPO）框架内，以硬约束的形式实现安全对齐，同时避免引入辅助模型和在线采样？** 这一问题的关键在于，标准DPO仅优化有用性偏好，缺乏对安全性的显式建模；而简单地将安全偏好与有用性偏好混合训练（如DPO-HARMLESS）或过滤不安全样本（如DPO-SAFEBETTER）均无法达到令人满意的安全水平。因此，需要一种理论上严谨、实践中轻量的方法，将硬约束安全对齐目标转化为可直接优化的DPO风格损失函数。

## 核心方法与创新机理

SafeDPO 的核心创新在于将带硬约束的安全对齐问题转化为**无需辅助模型的直接偏好优化**，其关键洞察可归结为两点：**安全感知的数据变换**与**安全边际机制**。

### 瓶颈突破：从松弛约束到硬约束

现有安全对齐方法存在两个结构性瓶颈。其一，以 **SafeRLHF**（Dai et al., 2023）为代表的方法依赖独立的奖励模型和成本模型，需要多阶段训练流程（PPO-λ），显著增加了计算开销和工程复杂度。其二，**SACPO**（Wachi et al., 2024）等方法采用松弛的期望约束而非严格硬约束，仅要求在期望意义上控制成本，无法彻底杜绝不安全输出。

SafeDPO 直接处理原始硬约束优化问题（Equation 6），其约束条件为 $c(x,y) \leq 0, \ \forall x, y \sim \pi_\theta$，即强制不安全响应的生成概率为零。论文证明，在温和假设（Assumption 4.1：参考策略下安全响应的总概率大于零）下，该问题存在封闭形式的最优策略，其中不安全响应被天然排除（Proposition 4.2, 4.3）。这一理论突破使得安全对齐可以绕过奖励/成本模型的显式建模。

### 核心操作柄：安全感知变换 T(𝒟)

SafeDPO 的关键因果操作柄是对训练数据对执行**安全感知变换 T**。给定原始偏好数据对 $(x, y_w, y_l)$ 及其二元安全标签 $(h_w, h_l)$，变换规则如下：

- 若首选响应 $y_w$ 安全，则数据对保持不变；
- 若 $y_w$ 不安全而次选响应 $y_l$ 安全，则**交换**两者位置；
- 若两者均不安全，则**丢弃**该数据对。

这一变换使经验数据集上的 SafeDPO 目标与理论上的难处理目标等价（Proposition 4.3），从而将硬约束安全对齐转化为标准 DPO 风格的损失函数（Equation 11）。消融实验提供了决定性证据：仅对数据集进行过滤（DPO-SAFEBETTER）而**不执行交换操作**，无害率远低于 SafeDPO，证明变换逻辑本身——而非简单的数据清洗——是安全改进的关键（Section 5.1.2, Appendix C.1）。

### 增强机制：安全边际 Δ

在变换后的数据上，SafeDPO 引入**安全边际 Δ**（Equation 12）。对于安全-不安全数据对，损失函数中额外减去一项 $(\tilde{h}_l - \tilde{h}_w)\Delta$，强制安全响应的对数概率与不安全响应之间保持至少 Δ 的差距。理论保证该边际**不改变最优解集**（Proposition 4.4），但在实践中进一步强化了安全性能。消融显示，Δ 从 0 增至 20 时无害率持续提升，但过大（如 50）会损害有用性（Figure 3, Appendix C.1）。

### 与基线方法的结构性差异

SafeDPO 相对于各基线的 changed slots 可归纳为：

| 组件 | 基线方法 | SafeDPO |
|------|---------|---------|
| 训练数据对 | 原始偏好对 $(x, y_w, y_l)$ | 经安全感知变换 T 处理后的 $(x, \tilde{y}_w, \tilde{y}_l)$ |
| 损失函数 | 标准 DPO 损失（Equation 4） | 带安全边际 Δ 的损失（Equation 12） |
| 超参数 Δ | 无（等效于 0） | Δ ≥ 0，控制安全边际强度 |
| 辅助模型 | SafeRLHF 需奖励/成本模型及价值函数 | 仅需策略网络与参考策略 |

值得注意的是，向其他 DPO 变体（DPO-HELPFUL、DPO-HARMLESS、DPO-SAFEBETTER）简单添加边际 Δ 仅产生有限的安全改进，无法达到 SafeDPO 的安全水平（Appendix C.1, Tables 5-7），进一步验证了安全感知变换是不可或缺的创新组件。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_PJdw4VBsXD/figures/003_Figure_3.jpg]]
*Figure 3: Harmlessness and Helpfulness Variations with Changing ∆. The dashed horizontal line indicates the harmless ratio and helpfulness of each baseline method*

SafeDPO 的整体流程由三个核心模块串联而成：**SFT 参考模型构建** → **安全感知数据转换 T** → **边际增强 DPO 训练**。整个管线仅需偏好数据与二元安全标签，无需额外的奖励模型、成本模型或在线采样，是一个单阶段、离线的直接偏好优化流程。

### 模块关系与数据流

1. **SFT 参考模型 π_ref**：首先通过有监督微调获得初始策略，作为后续 DPO 训练的参考分布。该模块继承自标准 RLHF/DPO 流程，不引入额外复杂度。

2. **安全感知数据转换 T**：这是 SafeDPO 区别于标准 DPO 的关键模块。给定原始偏好数据对 (x, y_w, y_l) 及其二元安全标签 (h_w, h_l)，转换 T 执行以下规则：
   - 若首选响应 y_w 安全（h_w = 0），则数据对保持不变；
   - 若首选响应不安全而次选响应安全（h_w = 1, h_l = 0），则交换两个响应；
   - 若两个响应均不安全（h_w = h_l = 1），则丢弃该数据对。
   
   这一转换将原始数据映射为变换后的数据集 T(𝒟)，使得后续 DPO 损失在经验数据上等价于理论上的难处理安全对齐目标（Proposition 4.3）。

3. **边际增强 DPO 训练**：在变换后的数据 T(𝒟) 上，优化带安全边际 Δ 的 SafeDPO 损失函数。该损失在标准 DPO 损失的基础上，对安全-不安全响应对施加额外的对数概率差距惩罚项 (h̃_l − h̃_w)Δ，其中 h̃ 为转换后的安全标签。安全边际 Δ ≥ 0 是 SafeDPO 引入的唯一额外超参数，且已被证明不改变最优解集（Proposition 4.4）。

### 与 SafeRLHF 的结构对比

Figure 1 直观展示了 SafeDPO 与 SafeRLHF 的组件差异。SafeRLHF 需要额外训练奖励模型和成本模型，并在 PPO 阶段进行在线采样和策略更新，涉及多阶段训练流程。SafeDPO 则将这些组件全部移除，仅保留策略网络和参考策略网络，将安全约束直接编码进数据转换和损失函数中。这一简化带来了显著的效率提升：训练时间约为 SafeRLHF 的 1/24，所需网络组件和标注信号也大幅减少（Table 14-16）。

### 理论保证

SafeDPO 的核心理论贡献在于证明了硬约束安全对齐目标（Equation 6）在温和假设下存在闭式最优策略，且该策略天然排除不安全响应——即对任何不安全响应 y，有 π*(y|x) = 0（Proposition 4.2）。进一步地，安全感知数据转换 T 使得在经验数据集上的 SafeDPO 目标与理论上的难处理目标等价，从而提供了一个可证明无偏的估计器。

### 关键设计选择

消融实验表明，安全感知转换 T 是 SafeDPO 安全性能的关键驱动因素。仅靠数据集过滤（如 DPO-SAFEBETTER，仅移除首选响应不安全的样本）无法达到同等的无害率水平。安全边际 Δ 则在此基础上进一步增强安全性，但 Δ 过大（如 50）会损害有用性（Figure 3）。向其他 DPO 变体（如 DPO-HELPFUL、DPO-HARMLESS）添加边际仅产生有限改进，无法达到 SafeDPO 的安全水平，进一步验证了安全感知转换的核心作用。

### 3.1 硬约束安全对齐的闭式解

SafeDPO 的核心起点是将安全对齐建模为一个**硬约束优化问题**，而非传统 SafeRLHF 中的松弛期望约束。该问题的形式为：

$$
\underset {\theta } {\mathop {\operatorname* {m a x} } } \mathbb { E } _ { { x \sim \mathcal { D } } , { y \sim \pi _ { \theta } ( \cdot | x ) } } [ r ( x , y ) - \beta D _ { \mathrm { K L } } ( \pi _ { \theta } ( \cdot  { | } x ) \| { \pi _ { \mathrm { r e f } } ( \cdot  { | } x ) } ) ] , \mathrm { ~ s . t . ~ } c ( x , y ) \leq 0 , \quad \forall x \sim \mathcal { D } , y \sim \pi _ { \theta } ( \cdot  { | } x )
$$

约束 $c(x,y) \leq 0$ 强制要求策略不能为任何提示生成不安全响应（即不安全响应的概率必须为零）。在温和假设（参考策略下安全响应总概率有正下界 $\delta > 0$）下，该问题存在**闭式最优策略**。

关键推导步骤是引入**代价增强奖励**：

$$
r _ { c } ( x , y ) = { \left\{ \begin{array} { l l } { r ( x , y ) , } & { { \mathrm { i f ~ } } c ( x , y ) \leq 0 , } \\ { - \infty , } & { { \mathrm { o t h e r w i s e } } . } \end{array} \right. }
$$

对不安全响应赋予 $-\infty$ 奖励，使其在最优解中自然被排除。将此奖励代入 KL 正则化 RL 目标的闭式解，得到：

$$
\pi ^ { * } ( y \mid x ) = \frac { 1 } { Z ( x ) } \pi _ { \mathrm { r e f } } ( y \mid x ) \exp { \left( \frac { 1 } { \beta } r _ { c } ( x , y ) \right) }
$$

该最优策略天然满足 $\pi^*(y|x) = 0$ 当 $c(x,y) > 0$，即**不安全响应被构造性排除**。这是 SafeDPO 与基于松弛约束方法（如 SafeRLHF 的 PPO-λ）的本质区别：后者仅约束期望成本，无法彻底杜绝不安全输出。

### 3.2 安全感知数据变换 T

上述闭式解虽然优雅，但直接优化需要完整的奖励函数 $r(x,y)$，这与 DPO 消除显式奖励模型的初衷相悖。SafeDPO 的核心洞察在于：**难处理的原始目标可以通过一个安全感知的数据对变换，等价地转化为标准 DPO 风格的损失函数**。

变换 $T$ 作用于偏好数据集 $\mathcal{D}$ 中的每个四元组 $(x, y_w, y_l, h_w, h_l)$，其中 $h_w, h_l \in \{0,1\}$ 分别表示首选和次选响应的安全标签（$h=0$ 表示安全，$h=1$ 表示不安全）：

1. **若首选安全**（$h_w = 0$）：数据对保持不变。
2. **若首选不安全、次选安全**（$h_w = 1, h_l = 0$）：交换 $y_w$ 与 $y_l$，使安全响应成为新的首选。
3. **若两者均不安全**（$h_w = 1, h_l = 1$）：丢弃该数据对。

这一变换的理论保证来自 **Proposition 4.2 和 4.3**：在温和假设下，基于变换后数据 $T(\mathcal{D})$ 的经验 DPO 目标与原始难处理目标等价（即为无偏估计量）。这意味着 SafeDPO 无需辅助奖励模型或成本模型，仅需在偏好数据上附加二元安全标签即可实现硬约束安全对齐。

### 3.3 带安全边际的 SafeDPO 损失

在变换后的数据上，SafeDPO 的基础损失函数为：

$$
\mathcal { L } _ { \mathrm { S a f e D P O } } ( \theta ) = - \mathbb { E } _ { ( x , \tilde { y } _ { w } , \tilde { y } _ { l } ) \sim T ( \mathcal { D } ) } \bigg [ \log \sigma \bigg ( \beta \log \frac { \pi _ { \theta } \left( \tilde { y } _ { w } \mid x \right) } { \pi _ { \mathrm { r e f } } \left( \tilde { y } _ { w } \mid x \right) } - \beta \log \frac { \pi _ { \theta } \left( \tilde { y } _ { l } \mid x \right) } { \pi _ { \mathrm { r e f } } \left( \tilde { y } _ { l } \mid x \right) } \bigg ) \bigg ]
$$

为进一步增强安全性，SafeDPO 引入**安全边际 $\Delta \geq 0$**，对安全-不安全对施加额外的对数概率差距惩罚：

$$
\mathcal { L } _ { \mathrm { S a f e D P O } } ( \theta ; \Delta ) = - \mathbb { E } _ { T ( \mathcal { D } ) } \Bigg [ \log \sigma \bigg ( \beta \log \frac { \pi _ { \theta } ( \tilde { y } _ { w } \mid x ) } { \pi _ { \mathrm { r e f } } ( \tilde { y } _ { w } \mid x ) } - \beta \log \frac { \pi _ { \theta } ( \tilde { y } _ { l } \mid x ) } { \pi _ { \mathrm { r e f } } ( \tilde { y } _ { l } \mid x ) } - ( \tilde { h } _ { l } - \tilde { h } _ { w } ) \Delta ) \Bigg ) \Bigg ]
$$

其中 $\tilde{h}_w, \tilde{h}_l$ 是变换后的安全标签。当 $\tilde{y}_w$ 安全而 $\tilde{y}_l$ 不安全时，$\tilde{h}_l - \tilde{h}_w = 1$，边际项 $- \Delta$ 生效，要求安全响应的隐式奖励比不安全响应高出至少 $\Delta$ 才能获得低损失。

**Proposition 4.4** 证明：引入 $\Delta$ **不改变最优解集**——最优策略仍为 $\pi^*$，因为该策略下不安全响应的概率已严格为零，额外边际不会产生约束冲突。这一性质保证了 SafeDPO 在增强安全性的同时不会偏离原始硬约束目标的理论最优解。

### 3.4 方法流水线

SafeDPO 的训练流水线由三个模块串联构成：

1. **SFT 参考模型 $\pi_{\text{ref}}$**：通过有监督微调获得初始策略，作为 KL 正则化的锚点。
2. **安全感知数据转换 $T$**：根据二元安全标签对偏好数据对进行重排序/过滤，确保变换后数据中首选响应始终安全。
3. **边际增强 DPO 训练**：在 $T(\mathcal{D})$ 上优化带安全边际 $\Delta$ 的 DPO 目标，直接更新策略网络参数 $\theta$，无需在线采样或辅助模型。

与 SafeRLHF 相比（Figure 1），SafeDPO 消除了红色标注的额外组件：奖励模型训练、成本模型训练、PPO 在线采样循环，仅保留蓝色标注的共享组件（安全标签、参考策略）。这使得 SafeDPO 的训练时间约为 SafeRLHF 的 1/24（Table 15），且所需网络组件仅为策略网络和参考策略（Table 14）。

### 关键公式速查

| 公式 | 变量含义 |
|------|----------|
| $r_c(x,y)$ | 代价增强奖励：对不安全响应赋 $-\infty$ |
| $\pi^*(y\|x)$ | 闭式最优策略：以 $r_c$ 为参数的 KL 正则化最优解 |
| $T(\mathcal{D})$ | 安全感知数据变换：交换/丢弃不安全首选对 |
| $\mathcal{L}_{\text{SafeDPO}}(\theta)$ | 基础 SafeDPO 损失：$T(\mathcal{D})$ 上的标准 DPO 损失 |
| $\mathcal{L}_{\text{SafeDPO}}(\theta;\Delta)$ | 带边际的 SafeDPO 损失：对安全-不安全对施加额外间隔 $\Delta$ |
| $\beta$ | KL 惩罚系数，控制策略偏离参考策略的程度 |
| $\tilde{h}_w, \tilde{h}_l$ | 变换后的安全标签（0=安全，1=不安全） |

## 实验与关键发现

### 安全性与有用性的核心权衡

SafeDPO 在 PKU-SafeRLHF-30K 数据集上展现出显著的安全性能提升，同时保持了可竞争的有用性水平。在模型评测协议下（Figure 2a），SafeDPO 实现了约 **97.24%** 的无害率，远高于仅用有用性偏好训练的 DPO-HELPFUL（38.6%），无害性指标（平均负成本）也从 -2.24 跃升至 5.92。作为代价，有用性（归一化奖励）从 10.0 降至 4.86，体现了安全-有用性权衡。在 GPT-4 评测协议下（Figure 2b），SafeDPO 的无害率达到 **100%**，而 DPO-HELPFUL 接近 0%；同时 SafeDPO 的有用性得分（8.14）反而显著高于 DPO-HELPFUL（约 1.48），这一反常现象需谨慎解读——GPT-4 评估器可能将安全性混入有用性判断，导致更安全的回答获得虚高的有用性得分（见附录 D.3/E.3 讨论）。

在安全对比分析中（Table 12），SafeDPO 与各基线方法的逐对比较显示：SafeDPO 不安全而基线安全的 (U, S) 案例数量可忽略不计或为零，表明 SafeDPO 的安全性能至少与基线持平或更优。这一结论在模型评测和 GPT-4 评测下均成立。

### 消融实验：安全感知变换是关键驱动因素

消融实验揭示了 SafeDPO 安全性能的两个关键来源，且二者的贡献有明确的因果层次。

**安全感知数据变换 T 是安全改进的核心。** DPO-SAFEBETTER 仅过滤掉首选响应为不安全的样本对，其无害率远低于 SafeDPO（Figure 2），证明简单的数据集过滤不足以达到 SafeDPO 的安全水平。变换 T 的核心机制在于：当首选响应不安全而次选响应安全时，交换二者的顺序，使模型学习“安全优于不安全”的偏好；同时丢弃双不安全的样本对，避免噪声信号。这一设计直接源于理论分析——Proposition 4.3 证明，在变换后的经验数据集 T(D) 上的 SafeDPO 目标与原始难处理目标等价。

**安全边际 Δ 提供额外的安全增强，但不改变最优解集。** 在 Δ ∈ {0, 2, 5, 10, 20} 范围内，SafeDPO 的安全性能随 Δ 增大而单调提升（Figure 3），且 Proposition 4.4 保证 Δ 的引入不改变最优策略集合。然而，Δ 过大（如 50）会导致有用性显著退化（附录 C.1），表明存在实际可用的 Δ 上限。关键的是，向其他 DPO 变体（DPO-HELPFUL、DPO-HARMLESS、DPO-SAFEBETTER）添加边际仅产生有限的安全改进（Tables 5-7），无法达到 SafeDPO 的安全水平。这进一步证实：**安全感知变换而非边际本身，才是安全改进的主要驱动力。**

### 规模扩展性与鲁棒性

SafeDPO 在不同模型规模上表现出一致的有效性（Table 1 / Table 9）。在 1.5B 至 13B 参数范围内，无害率稳定在 95.5%–97.9% 区间，有用性随模型规模增大而提升，表明该方法可可靠扩展至更大规模模型。在随机种子鲁棒性测试中（Table 13），SafeDPO 在三个不同随机种子上始终获得更高的归一化奖励和更低的成本，且标准差较小，证明性能增益对随机初始化不敏感。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_PJdw4VBsXD/figures/004_Table_1.jpg]]
*Table 1: Comparison of SafeDPO with various reference models on helpfulness, harmlessness, and harmless ratio*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_PJdw4VBsXD/figures/012_Table_9.jpg]]
*Table 9: Comparison of SafeDPO with various reference models on helpfulness, harmlessness, and harmless ratio*

### 训练效率与数据效率优势

与 SafeRLHF (Dai et al., 2023) 相比，SafeDPO 展现出显著的效率优势：

- **网络组件**（Table 14）：SafeRLHF 需要额外的奖励模型、成本模型及其价值函数，而 SafeDPO 仅需策略网络和参考策略，大幅降低显存开销。
- **训练时间**（Table 15）：SafeRLHF 因 PPO 的在线 rollout 生成和辅助模型训练而产生大量计算开销，SafeDPO 执行直接离线优化，训练时间约为 SafeRLHF 的 **1/24**。
- **监督信号**（Table 16）：SafeRLHF 依赖多种标注数据训练奖励和成本模型，SafeDPO 仅需偏好数据和安全指示器，数据效率更高。

### 人类评估验证

人类评估结果（Table 2 / Table 11）进一步验证了 SafeDPO 的有效性。在安全性评分上，SafeDPO（0.943）与 SafeRLHF（0.932）相当，均远高于 SFT 基线。在有用性方面，SafeDPO 同样保持了可竞争的水平。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_PJdw4VBsXD/figures/005_Table_2.jpg]]
*Table 2: Human evaluation of safety and helpfulness scores across different methods*

### 过度拒绝问题

在 XSTest 过度拒绝基准上（Table 3），SafeDPO 实现了 100% 的无害率，但过度拒绝率高达 **12.4%**，显著高于 SFT 基线的 0.4%。这表明 SafeDPO 在遇到表面词元触发时可能过度保守，倾向于拒绝本应安全回答的提示。这是硬约束安全对齐方法的一个固有局限：严格排除不安全响应的机制在边界情况下缺乏细粒度判断能力。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_PJdw4VBsXD/figures/006_Table_3.jpg]]
*Table 3: Comparison of over-refusal and harmless ratio*

### 局限性汇总

1. **评估覆盖范围有限**：仅在 PKU-SafeRLHF-30K 一个安全对齐数据集和 XSTest 一个过度拒绝基准上评估，现实复杂安全场景的泛化性未经验证。
2. **模型规模上限**：实验限于 13B 参数，更大规模 LLM（如 70B+）的表现未知。
3. **高安全边际下的有用性退化**：Δ=50 时性能显著下降，实际部署需谨慎调节。
4. **GPT-4 评估耦合问题**：自动评估器可能将安全性混入有用性评分，高估安全对齐方法的有用性表现。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_PJdw4VBsXD/figures/011_Table_8.jpg]]
*Table 8: Alpaca-7b model using the PKU-SafeRLHF-30K dataset, consistent with the original implementation, and no additional modifications are introduced. Table 8: Comparison of PeCAN (P) and MoCAN (M) models across varying λ values on helpfulness, harmlessness, and harmless ratio*

## 定位与知识库关联

### 1. 方法定位：从SafeRLHF到SafeDPO的简化路径

SafeDPO的核心贡献在于将安全对齐从多阶段、多模型的复杂流程压缩为单阶段、无辅助模型的直接偏好优化。其直接对标的工作是**SafeRLHF**（Dai et al., 2023），后者代表了安全对齐领域的主流范式：先训练独立的奖励模型和成本模型，再通过PPO-λ进行多阶段在线策略优化。SafeDPO通过理论推导证明，硬约束安全对齐目标在温和假设下存在封闭形式最优策略（Proposition 4.2），从而将问题转化为一个标准DPO风格的损失函数优化，彻底消除了对辅助模型和在线采样的依赖。

图1清晰地展示了这一简化：SafeRLHF需要额外的奖励模型、成本模型及其价值函数（图中红色组件），而SafeDPO仅需在DPO基础上添加安全标签和单一超参数Δ（图中蓝色组件）。从训练效率看，SafeDPO的训练时间约为SafeRLHF的1/24（Table 15），且所需网络组件从4个以上降至仅需策略网络和参考策略网络（Table 14）。所需监督信号也从多种标注类型简化为偏好对加二元安全标签（Table 16）。

### 2. 与DPO变体及约束优化方法的对比

在直接偏好优化的方法谱系中，SafeDPO与以下基线形成对照：

- **DPO-HELPFUL**：仅使用有用性偏好的标准DPO，作为非安全基线。其无害率仅38.6%（模型评测），证明标准DPO无法自发产生安全行为。
- **DPO-HARMLESS**：仅用无害性偏好训练DPO，作为安全优先基线。虽然无害率有所提升，但有用性严重受损。
- **DPO-SAFEBETTER**：仅保留优选响应为安全的样本进行DPO训练。该基线用于消融数据过滤的独立效果——实验表明，仅靠过滤远不足以达到SafeDPO的安全水平（Section 5.1.2），揭示了安全感知变换T的不可替代性。
- **SACPO / P-SACPO**（Wachi et al., 2024）：基于约束优化的安全对齐方法，采用拉格朗日松弛将安全约束转化为惩罚项。SafeDPO与之的关键区别在于：SACPO仍依赖松弛约束，而SafeDPO从硬约束出发，通过理论等价变换彻底规避了约束松弛带来的安全漏洞。

消融实验进一步表明，向DPO-HELPFUL、DPO-HARMLESS、DPO-SAFEBETTER等变体直接添加安全边际Δ仅产生有限改进，无法达到SafeDPO的安全水平（Tables 5-7）。这证实了安全感知变换T才是安全改进的核心因果机制，而非边际机制本身。

### 3. 方法适用边界

**适用场景**：
- 拥有二元安全标签的偏好数据场景，数据格式要求为 (x, y_w, y_l, h_w, h_l)，其中h为安全指示器。
- 需要快速、低成本部署安全对齐的中小规模LLM（已验证1.5B至13B参数范围，Table 1/9）。
- 对训练效率敏感的场景：SafeDPO仅需离线数据，无需在线生成文本，计算开销远低于PPO类方法。

**不适用或需谨慎使用的场景**：
- 缺乏明确安全标签的偏好数据集——安全感知变换T依赖二元安全指示器。
- 对过度拒绝（over-refusal）敏感的对话系统：SafeDPO在XSTest上过度拒绝率达12.4%，在表面词元触发时可能过度保守（Table 3）。
- 极高安全边际设置（如Δ=50）会导致有用性显著退化（Figure 3），需要在安全-有用权衡中谨慎选择Δ值。

### 4. 已知局限

1. **评估范围有限**：仅在PKU-SafeRLHF-30K单一安全对齐数据集和XSTest单一过度拒绝基准上验证，现实复杂安全场景覆盖不足。
2. **模型规模上限**：实验限于13B参数规模，更大规模LLM（如70B+）的表现未经验证。
3. **评估偏差风险**：GPT-4作为自动评估器存在安全性与有用性评分耦合问题——更安全的回答可能获得虚高的有用性得分（附录D.3/E.3），导致SafeDPO的有用性优势可能被高估。
4. **过度拒绝倾向**：在XSTest上12.4%的过度拒绝率表明，SafeDPO在识别安全边界时偏向保守，可能拒绝本应正常回答的非有害查询。

### 5. 开放问题

1. **过度拒绝缓解**：如何在保持严格安全性的同时降低过度拒绝率？是否需要引入更细粒度的安全分级而非二元标签？
2. **方法扩展性**：SafeDPO的安全感知变换T和边际增强机制能否推广至其他直接偏好优化变体（如IPO、KTO）或在线采样方法？
3. **评估框架改进**：如何构建更公正的自动评估框架以解耦安全性与有用性，避免GPT-4评估中的耦合偏差？
4. **推理时集成**：SafeDPO与推理时安全干预（如System Prompt、安全分类器）的集成效果如何？能否形成训练-推理协同的安全保障体系？
5. **跨域泛化**：在PKU-SafeRLHF之外的安全领域（如生物安全、网络安全）上，安全感知变换的泛化能力如何？

## 原文 PDF

![[paperPDFs/ICLR_2026/SafeDPO_A_Simple_Approach_to_Direct_Preference_Optimization_with_Enhanced_Safety.pdf]]
