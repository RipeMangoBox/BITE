---
title: Stable and Efficient Single-Rollout RL for Multimodal Reasoning
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Stable_and_Efficient_Single_Rollout_RL_for_Multimodal_Reasoning.pdf
project_link: "https://mssr-proj.github.io"
code_link: null
aliases:
- MMSSR
- SESRRMR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 基于熵的优势塑造（entropy-based advantage shaping），通过向优势中注入策略熵调节项ψ_t，动态限制低奖励响应的惩罚强度，同时奖励高熵探索，直接抑制熵塌缩。
primary_logic: 在多模态单次推出RL中，显式维护策略熵对于保持训练稳定性至关重要；将熵信号直接耦合到优势函数中，能以极低计算开销（仅需单次推出）替代组归一化效应，实现与组基线相当甚至更优的推理性能。
claims:
- MVSR在Qwen2.5-VL-7B上发生熵塌缩，训练和验证准确率均下降；MSSR通过熵塑造保持熵平稳，准确率持续提升。
- MSSR仅需GRPO一半的训练步数即可达到相当的ID验证准确率。
- 在5个多模态推理基准上，MSSR平均准确率比GRPO、RLOO、REINFORCE++提升2.1%（3B）和2.3%（7B）。
- 消融实验中，交叉模态正则化和熵损失均无法完全阻止熵塌缩或验证精度退化，而MSSR的熵优势塑造可将最终验证精度提升约5%。
---

# Stable and Efficient Single-Rollout RL for Multimodal Reasoning

> [!tip] 核心洞察
> 在多模态单次推出RL中，显式维护策略熵对于保持训练稳定性至关重要；将熵信号直接耦合到优势函数中，能以极低计算开销（仅需单次推出）替代组归一化效应，实现与组基线相当甚至更优的推理性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向多模态推理的稳定高效单次推出强化学习 |
| 英文题名 | Stable and Efficient Single-Rollout RL for Multimodal Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.18215) · [Project](https://mssr-proj.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MSSR (Multimodal Stabilized Single-Rollout) |
| Dataset | MathVerse, MathVista, MMK12, R1-Onevision-Bench |

> [!tip] 效果简介
> - MathVerse 上，accuracy (%) 49.8 (7B) / 39.6 (3B) vs 48.5 (GRPO 7B) / 36.8 (GRPO 3B) (+1.3 / +2.8)。
> - MathVista 上，accuracy (%) 71.1 (7B) / 63.0 (3B) vs 70.0 (GRPO 7B) / 61.7 (GRPO 3B) (+1.1 / +1.3)。
> - MMK12 上，accuracy (%) 62.5 (7B) / 49.2 (3B) vs 55.8 (GRPO 7B) / 46.1 (GRPO 3B) (+6.7 / +3.1)。

## 概述

多模态大语言模型（MLLM）的推理能力近年来受到广泛关注，但通过强化学习（RL）提升其推理水平仍面临严峻挑战。当前主流的多模态RLVR（Reinforcement Learning with Verifiable Rewards）方法——如**GRPO**（Shao et al., 2024）——依赖每组多个推出样本（rollout）进行组内优势归一化，以获得稳定的训练信号。然而，这种组基（group-based）范式引入了高昂的计算开销：每个输入需要生成多条回复，极大增加了训练成本。

一个自然的替代方案是单次推出（single-rollout）RLVR，即每个多模态输入仅生成一条回复。但本文发现，直接迁移这一范式到多模态场景会引发**灾难性的熵塌缩（entropy collapse）**：策略的生成分布迅速退化，验证精度随之崩坏。其根本原因在于，视觉输入引入的高维噪声加剧了跨模态信用分配（credit assignment）的不稳定性，而缺乏组内规范化使得优势估计方差过大，策略过早收敛到低熵的退化状态。

针对这一瓶颈，本文提出**MSSR（Multimodal Stabilized Single-Rollout）**——一种稳定且高效的单次推出RLVR方法。其核心创新是**基于熵的优势塑造（entropy-based advantage shaping）**：通过向优势函数中注入策略熵调节项，动态限制低奖励响应的惩罚强度，同时奖励高熵探索，从而显式维护策略的生成多样性。该方法以极低的计算开销（仅需单次推出）替代了组归一化效应，实现了与组基线相当甚至更优的推理性能。

核心结论如下：
- **稳定性突破**：MSSR有效抑制了多模态单次推出RL中的熵塌缩现象，训练和验证准确率持续提升，而朴素单次推出基线（MVSR）则迅速退化。
- **效率优势**：MSSR仅需GRPO一半的训练步数即可达到相当的ID验证准确率，且每步训练时间与GRPO相近。
- **泛化性能领先**：在MathVerse、MathVista、MMK12、R1-Onevision-Bench和HallusionBench五个多模态推理基准上，MSSR在Qwen2.5-VL 3B和7B模型上平均准确率分别比GRPO、RLOO、REINFORCE++提升2.1%和2.3%。
- **消融验证**：交叉模态正则化和熵损失等替代方案均无法完全阻止熵塌缩或验证精度退化，而MSSR的熵优势塑造可将最终验证精度提升约5%。

## 背景与动机

### 多模态推理的强化学习困境

大视觉语言模型（VLMs）在多模态推理任务上已展现出显著能力，但其推理深度和稳定性仍然受限。为了进一步激发模型的推理潜力，研究者开始将强化学习验证奖励（RLVR）引入多模态训练。当前主流方法如 **GRPO**（Shao et al., 2024）采用组基线（group-based）策略：对每个输入采样多个回复（rollout），利用组内均值/标准差对奖励进行规范化，从而降低优势估计的方差。这种方法虽然有效，但计算成本高昂——例如，GRPO 对每个 prompt 生成 8 条回复，使得每步训练的计算开销成倍增加。

### 单次推出方法的崩溃问题

为降低计算负担，研究者尝试将文本领域成熟的单次推出（single-rollout）RLVR 方法迁移到多模态场景，如 **REINFORCE++**（Hu et al., 2025）。然而，这些方法在多模态上下文中普遍遭遇严重的训练不稳定性。本文通过系统观察发现，核心问题在于**熵塌缩（entropy collapse）**：由于缺乏组内规范化，单次推出下的优势估计方差过大，导致策略输出熵迅速下降，模型过早收敛到确定性策略，验证精度随之崩坏。视觉输入引入的高维噪声进一步加剧了跨模态信用分配（credit assignment）的不稳定性，使得这一问题在多模态场景下尤为突出。

### 现有稳定化尝试的局限

为抑制熵塌缩，已有工作探索了多种技术路径：
- **KL 正则化**：对参考策略施加 KL 散度约束，但实验表明该方法在单次推出设定下无法独立阻止熵塌缩。
- **交叉模态正则化**：引入纯文本锚策略，通过多模态策略与文本锚之间的 KL 散度进行约束。该方法仅提供部分稳定效果——训练准确率有所提升，但验证准确率仍会退化。
- **显式熵损失**：在目标函数中直接加入熵奖励项。这能部分维持熵值，但验证性能依然下降，且熵保持效果不如预期。

这些尝试表明，在多模态单次推出 RLVR 中，**显式且动态地维护策略熵**对于训练稳定性至关重要，而现有技术尚未有效解决这一问题。

### 本文动机与核心思路

基于以上观察，本文提出 **MSSR（Multimodal Stabilized Single-Rollout）**，一个稳定且高效的单次推出 RLVR 框架。MSSR 的核心创新在于**基于熵的优势塑造（entropy-based advantage shaping）**：通过向优势函数中注入策略熵调节项，动态限制低奖励响应的惩罚强度，同时奖励高熵探索，从而直接抑制熵塌缩。该方法以极低计算开销（仅需单次推出）替代组归一化效应，在保持训练稳定性的同时，实现了与组基线方法相当甚至更优的推理性能。

## 核心创新

MSSR的核心创新在于**将策略熵信号直接耦合到优势函数中，以极低的计算开销（仅需单次推出）替代组归一化的稳定效应**，从而解决多模态单次推出RLVR中因缺乏组内规范化导致的训练崩溃问题。

### 问题根源：熵塌缩与优势估计方差

在多模态RLVR中，当采用单次推出（single-rollout）策略时，无法像**GRPO**（Shao et al., 2024）那样利用组内多个回复计算标准化优势 $A_i = \frac{r_i - \mathrm{mean}(\{r_i\})}{\mathrm{std}(\{r_i\})}$。替代方案MVSR（Multimodal Vanilla Single-Rollout）使用Beta分布基线估计期望奖励 $\hat{v}(x) = \frac{\alpha(x)}{\alpha(x) + \beta(x)}$，并配合批归一化计算优势 $A_t$。然而，视觉输入引入的高维噪声加剧了跨模态信用分配的不稳定性，导致优势估计方差过大。其直接后果是**策略熵迅速塌缩**（Figure 3），模型输出分布过早收敛到确定性策略，训练和验证准确率同步崩坏（Figure 1a-b）。

### 核心机制：基于熵的优势塑造

MSSR的核心因果调节旋钮是**熵优势塑造（entropy-based advantage shaping）**。该方法不改变单次推出的采样策略，而是向原始优势中注入策略熵调节项：

$$\hat{A}_t = A_t + \psi_t$$

其中熵奖励项定义为：

$$\psi_t = \min\left(\frac{|A_t|}{\gamma}, \lambda \cdot \operatorname{stopgrad}(\mathcal{H}_t)\right)$$

$\mathcal{H}_t(\pi_\theta) = -\mathbb{E}_{o \sim \pi_\theta(\cdot|x)}[\log \pi_\theta(o_{<t}|x)]$ 为策略在token $t$ 处的输出分布熵。该设计的精妙之处在于：

1. **动态限制惩罚强度**：当原始优势 $A_t$ 为负（低奖励回复）时，$\psi_t$ 的上限受 $|A_t|/\gamma$ 约束，防止对低奖励回复施加过强的抑制梯度，避免策略过早丧失多样性。
2. **奖励高熵探索**：当策略熵 $\mathcal{H}_t$ 较高时，$\psi_t$ 提供正向奖励，鼓励模型保持输出分布的多样性，直接对抗熵塌缩趋势。
3. **梯度隔离**：$\operatorname{stopgrad}(\mathcal{H}_t)$ 确保熵仅作为奖励信号注入，不通过优势项产生二阶梯度，保持训练稳定。

### 与替代方案的对比

消融实验（Figure 4）系统对比了三种可能的稳定化策略：

- **KL正则化到参考策略**：MVSR中已包含对初始策略的KL散度约束，但Figure 3显示这完全无法阻止熵塌缩，说明仅靠参考策略约束不足以应对多模态场景的高方差优势估计。
- **交叉模态正则化**：引入纯文本锚策略，计算多模态与文本策略间的KL散度 $\mathcal{L}_{\mathrm{KL}} = \mathbb{E}\left[ \mathrm{KL}\left( \pi_\theta(\cdot \mid x_{\mathrm{text}}, x_{\mathrm{image}}) \parallel \pi_\theta(\cdot \mid x_{\mathrm{text}}) \right) \right]$。该方案提供部分稳定效果，训练准确率有所提升，但验证准确率依然退化，且未达到MSSR的性能水平。
- **熵损失项**：直接向损失函数添加熵奖励。该方法可部分保留熵，但验证性能仍下降，且熵的保持效果不如MSSR显著。

MSSR的熵优势塑造将最终验证准确率提升约5%（相对最强单次推出变体），是唯一能同时实现训练稳定、熵保持和验证性能持续提升的方案。

### 计算效率优势

MSSR的关键创新还体现在**以单次推出的计算成本达到组基线的性能**。如Figure 1所示，MSSR仅需GRPO一半的训练步数即可达到相当的ID验证准确率。在训练成本上（Table 3），MSSR每步6.9分钟，与GRPO（6.1分钟）接近，但MSSR仅需1次推出/输入（GRPO需8次），总采样效率更高。这一效率优势源于熵塑造机制有效替代了组归一化的方差缩减功能，使得单次推出策略也能获得稳定的梯度信号。

## 整体框架

MSSR（Multimodal Stabilized Single-Rollout）是一个面向多模态推理的**组无关（group-free）单次推出强化学习**框架，其核心设计目标是在仅使用每个多模态输入的一条采样轨迹的条件下，同时实现训练稳定性和计算效率。整个 pipeline 由五个紧密耦合的模块构成，信息流如图 2 所示。

### 1. 单次推出生成

给定多模态输入 $x$（包含图像与对应问题文本），MSSR 从旧策略 $\pi_{\theta_{\text{old}}}$ 中**仅采样一条回复** $o$。这与 GRPO 等组基线方法（每个 prompt 生成 $G=8$ 条回复）形成根本差异：MSSR 的总批次规模为 2048 prompts × 1 rollout，等价于 GRPO 的 256 prompts × 8 rollouts，从而在保证每步推出样本数公平可比的前提下，将生成计算量降至组方法的 $1/G$。

### 2. Beta 基线估计

由于单次推出无法获得组内统计量来标准化优势，MSSR 为每个多模态输入 $x$ 维护一个共轭 Beta 分布 $\text{Beta}(\alpha(x), \beta(x))$，以其均值 $\hat{v}(x) = \frac{\alpha(x)}{\alpha(x) + \beta(x)}$ 作为期望奖励的基线估计。Beta 分布天然适配二值 Bernoulli 奖励场景，其参数通过自适应折扣因子 $\eta$ 进行指数滑动更新：当滑动窗口内的平均 KL 散度偏离目标值时，$\eta$ 在 $[\eta_{\min}, \eta_{\max}]$ 区间内线性调整，以控制对历史奖励的遗忘速度。

### 3. 优势计算与批次归一化

原始优势定义为单条轨迹奖励与基线估计之差 $A = r - \hat{v}(x)$。为抑制单次推出固有的高方差，MSSR 对当前批次内所有样本的优势进行**批次级归一化**，得到规范化后的优势 $A_t$。这一步骤部分替代了组归一化的方差缩减功能，但仅凭归一化仍不足以应对多模态场景下视觉噪声引入的跨模态信用分配不稳定性。

### 4. 基于熵的优势塑造（核心创新）

MSSR 的关键机制是在原始优势上叠加一个**熵奖励项** $\psi_t$，形成塑造后的优势：

$$
\hat{A}_t = A_t + \psi_t, \quad \psi_t = \min\left(\frac{|A_t|}{\gamma}, \lambda \cdot \operatorname{stopgrad}(\mathcal{H}_t)\right)
$$

其中 $\mathcal{H}_t = -\mathbb{E}_{o \sim \pi_\theta(\cdot|x)}[\log \pi_\theta(o_{<t}|x)]$ 为策略在 token $t$ 处的输出分布熵，$\gamma$ 和 $\lambda$ 为超参数。该设计的因果机制在于：当策略熵较低（模型趋于确定性）时，$\psi_t$ 被 $\lambda \cdot \mathcal{H}_t$ 限制，从而**削弱对低奖励响应的惩罚强度**，防止策略过早塌缩到次优解；当原始优势绝对值过大时，$\min$ 算子以 $|A_t|/\gamma$ 为上限，防止熵奖励过度扭曲梯度信号。通过将熵信号直接耦合到优势函数中，MSSR 以极低的计算开销（无需额外前向传播或组采样）实现了与组归一化等价的稳定效应。

### 5. 策略梯度更新

最终，MSSR 使用塑造后的优势 $\hat{A}_t$ 执行裁剪重要性采样更新，并施加对参考策略的 KL 正则化，目标函数形式与 GRPO 一致，但优势项被替换为 $\hat{A}_t$。整个训练过程中，模型输出熵保持平稳，避免了 MVSR（无熵塑造的单次推出基线）中观察到的熵塌缩现象（Figure 3）。

### 模块间的因果依赖

上述五个模块形成一条清晰的因果链：**单次推出**降低了生成成本，但引入了高方差 → **Beta 基线**提供了个体化期望奖励估计 → **批次归一化**进一步压缩方差 → **熵塑造**通过注入策略熵信号，从根本上抑制了训练不稳定性的根源——即缺乏组内规范化导致的熵塌缩 → **策略更新**在稳定梯度下持续提升推理能力。消融实验（Figure 4）证实，单独使用 KL 正则化、交叉模态正则化或熵损失均无法完全阻止验证精度退化，而 MSSR 的熵优势塑造可将最终验证精度提升约 5%，是稳定训练的必要条件。

### 补充图表

![[assets/figures/papers/paper_list_l2283_https_arxiv_org_abs_2512_18215/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed MSSR approach. Given a multimodal input*

## 核心模块与公式推导

MSSR 的完整训练流程由五个关键模块构成，其核心创新在于将策略熵信号直接耦合到优势函数中，以极低的计算开销（仅需单次推出）替代组归一化效应。

### 单次推出生成

给定多模态输入 $x$（文本 + 图像），从旧策略 $\pi_{\theta_{\text{old}}}$ 中仅采样一条回复轨迹 $o$。这与 GRPO 对每个 prompt 生成 $G=8$ 条回复形成鲜明对比。为保证公平比较，MSSR 将总 batch size 扩展至 2048（即 2048 个 prompt × 1 条 rollout），与 GRPO 的 256 × 8 保持每步总推出样本数等价。

### Beta 基线估计

为替代 GRPO 的组内均值/标准差归一化，MSSR 为每个多模态输入 $x$ 维护一个共轭 Beta 分布 $\text{Beta}(\alpha(x), \beta(x))$，以其均值作为基线价值估计：

$$\hat{v}(x) = \frac{\alpha(x)}{\alpha(x) + \beta(x)}$$

Beta 分布的参数通过自适应折扣因子 $\eta$ 进行更新。$\eta$ 的调整依赖于滑动窗口内的平均 KL 散度 $\overline{\text{KL}}_s$ 与目标 KL 散度 $\text{KL}_{\text{target}}$ 的关系：

- 当 $\overline{\text{KL}}_s > \text{KL}_{\text{target}}$ 时，策略偏离参考策略过大，需加快遗忘：

$$\tau_s = \min\left( \frac{\overline{\mathrm{KL}}_s}{\mathrm{KL}_{\mathrm{target}}}, 1.0 \right), \quad \eta_s = \eta_{\max} - \tau_s \cdot (\eta_{\max} - \eta_{\min})$$

- 当 $\overline{\text{KL}}_s \leq \text{KL}_{\text{target}}$ 时，策略稳定，减缓遗忘：

$$\tau_s = \frac{\overline{\mathrm{KL}}_s}{\mathrm{KL}_{\mathrm{target}}}, \quad \eta_s = \eta_{\min} + \tau_s \cdot (\eta_{\max} - \eta_{\min})$$

### 优势计算与批归一化

原始优势 $A_t = r - \hat{v}(x)$ 在 batch 内进行归一化以降低方差。然而，仅靠批归一化无法解决多模态单次推出场景下的核心问题——视觉输入引入的高维噪声使得跨模态信用分配极不稳定，优势估计方差过大。

### 熵基优势塑造（核心创新）

这是 MSSR 区别于 MVSR 的关键模块。MSSR 在原始优势 $A_t$ 上叠加一个熵奖励项 $\psi_t$，得到塑造后的优势：

$$\hat{A}_t = A_t + \psi_t$$

其中 $\psi_t$ 的定义为：

$$\psi_t = \min\left(\frac{|A_t|}{\gamma}, \lambda \cdot \operatorname{stopgrad}(\mathcal{H}_t)\right)$$

这里 $\mathcal{H}_t$ 是策略在 token $t$ 处的输出分布熵：

$$\mathcal{H}_t(\pi_\theta) = -\mathbb{E}_{o \sim \pi_\theta(\cdot|x)}[\log \pi_\theta(o_{<t}|x)]$$

**设计机理**：$\psi_t$ 取原始优势绝对值除以 $\gamma$ 与缩放后熵的最小值，并通过 $\operatorname{stopgrad}$ 截断梯度回传，使熵信号仅影响优势幅值而不直接参与策略梯度的二阶效应。当策略熵较高（探索充分）时，$\psi_t$ 为正向奖励，鼓励保持多样性；当低奖励回复导致 $A_t$ 为较大负值时，$\psi_t$ 受 $|A_t|/\gamma$ 约束，限制惩罚强度，防止策略过度收缩。这一机制直接抑制了 MVSR 中观测到的熵塌缩现象。

### 策略梯度更新

最终使用塑造后的优势 $\hat{A}_t$ 进行裁剪重要性采样更新，并施加参考策略 KL 正则化。GRPO 的基础目标函数形式为：

$$\mathcal{T}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{o_i\} \sim \pi_{\theta_{\mathrm{old}}}(\cdot|x)} \Bigg[ \frac{1}{G} \sum_{i=1}^{G} \min \big( \rho_i(\theta) A_i, \mathrm{clip} \big( \rho_i(\theta), 1-\epsilon, 1+\epsilon \big) A_i \big) \Bigg]$$

MSSR 在此框架下将 $G=1$、$A_i$ 替换为 $\hat{A}_t$，并加入 KL 正则项以约束策略更新幅度。

### 补充图表

![[assets/figures/papers/paper_list_l2283_https_arxiv_org_abs_2512_18215/figures/003_Figure_3.jpg]]
*Figure 3: Model output entropy during training with Qwen2.5- VL-7B. MVSR (multimodal vanilla single-rollout) suffers from entropy collapse as training progresses, whereas our proposed MSSR (multimodal stabilized single-rollout) preserves entropy*

## 实验与分析

### 核心瓶颈与训练稳定性

多模态单次推出RLVR（MVSR）面临的核心瓶颈在于**优势估计方差过大**。由于缺乏组内规范化（group-wise normalization），单次推出场景下优势信号的噪声被显著放大，直接导致**策略熵迅速塌缩**（Figure 3），进而引发验证精度崩坏。视觉输入引入的高维噪声进一步加剧了跨模态信用分配（credit assignment）的不稳定性。MSSR通过**基于熵的优势塑造（entropy-based advantage shaping）** 直接干预这一因果链条：向原始优势中注入策略熵调节项 $\psi_t = \min\left(\frac{|A_t|}{\gamma}, \lambda \cdot \operatorname{stopgrad}(\mathcal{H}_t)\right)$，动态限制低奖励响应的惩罚强度，同时奖励高熵探索，从而在仅需单次推出的计算开销下，替代组归一化效应，维持训练稳定。

Figure 3 直观展示了这一对比：在 Qwen2.5-VL-7B 上，MVSR 的模型输出熵随训练推进持续下降并最终塌缩；MSSR 则保持熵平稳，训练和验证准确率持续提升（Figure 1a-b）。值得注意的是，MSSR 仅需 **GRPO 一半的训练步数**即可达到相当的 ID 验证准确率（Figure 1 标注），凸显其训练计算效率优势。

![[assets/figures/papers/paper_list_l2283_https_arxiv_org_abs_2512_18215/figures/001_Figure_1.jpg]]
*Figure 1: Performance overview of MSSR: (a–b) Training and validation accuracy of MVSR (Multimodal Vanilla Single-Rollout), GRPO [28] and our MSSR, trained on the Vision-R1-RL [15] training set and validated on its corresponding validation set. MSSR remains stable and improves steadily, whereas MVSR is unstable and collapses. Notably, MSSR reaches a similar final validation accuracy to GRPO with half of the training steps, highlighting its superior training compute efficiency. (c) Our MSSR achieves higher generalization performance across diverse multimodal reasoning benchmarks, including MathVerse [40], MathVista [23], MMK12 [26], R1-Onevision-Bench [37], and HallusionBench [12], compared to other b...*

### 主实验结果

Table 1 汇总了在五个多模态推理基准上的泛化性能对比。MSSR 在所有基准上一致优于或匹配最强的组基线 GRPO，同时显著超越其他组无关方法（RLOO、REINFORCE++）：

![[assets/figures/papers/paper_list_l2283_https_arxiv_org_abs_2512_18215/figures/004_Table_1.jpg]]
*Table 1: Model generalization performance on diverse multimodal reasoning benchmarks. We compare MSSR with GRPO, RLOO, and REINFORCE++ baselines on Qwen2.5-VL 3B and 7B models. For broader context, we also report evaluated results from prior SFT+RL and Zero-RL methods following the evaluation protocol of [46]. MSSR outperforms other baselines, with Qwen2.5-VL-7B + MSSR achieving the strongest average performance across benchmarks*

- **平均准确率提升**：Qwen2.5-VL-3B 上 MSSR 平均 49.5%，较 GRPO 的 47.4% 提升 **+2.1%**；7B 上平均 58.6%，较 GRPO 的 56.3% 提升 **+2.3%**。
- **最大单基准增益**：MMK12 上 7B 模型提升 **+6.7%**（62.5% vs. 55.8%），3B 模型提升 **+3.1%**；HallusionBench 上 3B 模型提升 **+4.3%**。
- **唯一负向波动**：R1-Onevision-Bench 上 3B 模型 MSSR（29.0%）略低于 GRPO（30.2%），差值为 -1.2%，提示该基准对熵塑造的响应模式可能与其他基准不同，需进一步分析。

Table 4 进一步对比了 MVSR 与 MSSR 的直接泛化性能：MVSR 因训练不稳定，在 7B 上增益有限，在 3B 上多项基准甚至低于基模型；MSSR 则在所有基准上一致提升。

![[assets/figures/papers/paper_list_l2283_https_arxiv_org_abs_2512_18215/figures/012_Table_4.jpg]]
*Table 4: Model generalization performance on diverse multimodal reasoning benchmarks. We compare MVSR and MSSR on Qwen2.5-VL 3B and 7B models. As discussed earlier, MVSR’s training instability leads to limited gains for the 7B model and, for the 3B model, often results in performance below the base model across most benchmarks. In contrast, MSSR consistently improves generalization performance across all benchmarks*

### 推理粒度与效率分析

Table 2 展示了推理粒度对比。在 MMK12 基准上，MSSR 平均关键推理步骤数为 **3.3**，显著高于 GRPO 的 **1.9** 和基模型的 3.1；平均回复长度也呈现一致趋势。这表明 MSSR 不仅提升准确率，还促使模型产生更细粒度、结构更稳健的推理过程。

![[assets/figures/papers/paper_list_l2283_https_arxiv_org_abs_2512_18215/figures/009_Table_2.jpg]]
*Table 2: Comparison of reasoning granularity. We measure the average number of key reasoning steps and average response length on the MMK12 benchmark. MSSR produces more finegrained reasoning (3.3 key steps on average) compared to GRPO (1.9) and the base model (3.1), indicating more robust, wellstructured reasoning. The trend is consistent with average response length, where MSSR outputs are longer and more detailed than those from GRPO*

训练成本方面（Table 3），MSSR 每步平均训练时间在 3B/7B 上分别为 5.4/6.9 分钟，略高于 GRPO 的 4.7/6.1 分钟（因熵计算和 Beta 基线维护的额外开销），但考虑到 MSSR 仅需一半步数即可达到相当验证精度，**总体训练时间成本反而更低**。

![[assets/figures/papers/paper_list_l2283_https_arxiv_org_abs_2512_18215/figures/010_Table_3.jpg]]
*Table 3: Training cost across methods on Qwen2.5-VL 3B and 7B models, measured as the average training time per step (mins/step)*

### 消融实验：熵塌缩的替代方案为何失效

Figure 4 系统消融了三种可能的稳定化技术，结论明确：

![[assets/figures/papers/paper_list_l2283_https_arxiv_org_abs_2512_18215/figures/005_Figure_4.jpg]]
*Figure 4: Ablation studies on effectiveness of techniques for preventing entropy collapse and stabilizing multimodal single-rollout training. Cross-modal regularization: This technique provides partial stabilization, increasing training accuracy but still resulting in degraded validation accuracy, and both metrics remain below those achieved by MSSR. Entropy loss: Adding an entropy loss term partially preserves entropy and improves training accuracy toward the end of training, but validation performance still degrades and entropy is not maintained as effectively as in MSSR*

1. **KL 正则化至参考策略**：单独使用无法阻止多模态单次推出场景下的熵塌缩（MVSR 仍塌缩，Figure 3）。
2. **交叉模态正则化**（Cross-modal regularization）：通过文本锚策略提供 KL 散度正则化 $\mathcal{L}_{\mathrm{KL}} = \mathbb{E}\left[ \mathrm{KL}\left( \pi_\theta(\cdot \mid x_{\mathrm{text}}, x_{\mathrm{image}}) \parallel \pi_\theta(\cdot \mid x_{\mathrm{text}}) \right) \right]$，仅能部分稳定训练——训练准确率有所提升，但**验证准确率仍退化**，且两项指标均低于 MSSR（Figure 4a-b）。
3. **熵损失项**（Entropy loss）：虽能部分保留熵，但验证准确率同样退化，且熵的维持效果远不如 MSSR（Figure 4c）。

MSSR 的**熵优势塑造**将最终验证准确率提升约 **5%**（相较于最强的单次推出变体），是唯一能同时保持熵平稳和验证性能持续提升的方案。

### 敏感性分析

Figure 6 展示了滑动窗口大小 $N$ 和 target KL 值对验证准确率的影响：$N=20$ 和 $\mathrm{KL}_{\mathrm{target}}=0.01$ 在训练结束时获得最高验证准确率。训练准确率曲线在各设置下基本一致（Figure 7），说明自适应折扣因子 $\eta$ 的调节机制对超参数选择具有较好的鲁棒性。

![[assets/figures/papers/paper_list_l2283_https_arxiv_org_abs_2512_18215/figures/008_Figure_6.jpg]]
*Figure 6: Sensitivity analysis for effects of sliding window size N and target KL value*

![[assets/figures/papers/paper_list_l2283_https_arxiv_org_abs_2512_18215/figures/011_Figure_7.jpg]]
*Figure 7: Sensitivity analysis for effects of sliding window size N and target KL value KLtarget on adjusting the discount factor η and their impact on training accuracy. (a) Training accuracy under different sliding window sizes N. (b) Training accuracy under different target KL values KLtarget. Across all settings, the training accuracy curves remain largely similar*

### 失败模式与局限性

尽管 MSSR 在数学推理领域表现优异，仍存在以下局限：

- **领域泛化未验证**：训练仅限于 Vision-R1-RL 数学推理数据集，在其他开放域多模态推理任务上的稳定性与泛化性尚需验证。
- **超参数未穷尽探索**：$\gamma=0.4, \lambda=2.0$ 参考前人工序设定，全参数空间下的最优配置未知。
- **模型规模扩展性未知**：仅在 3B 和 7B 的 Qwen2.5-VL 上验证，对更大规模模型或不同多模态架构的适用性缺乏实验支撑。
- **早期回报偏低风险**：熵塑造虽稳定训练，但可能对简单任务过分鼓励探索，导致训练早期回报偏低——这一现象在 Figure 1a 的 MSSR 训练初期准确率曲线中有所体现，但最终被持续提升的趋势所弥补。

### 补充图表

![[assets/figures/papers/paper_list_l2283_https_arxiv_org_abs_2512_18215/figures/007_Figure_5.jpg]]
*Figure 5: Comparison of reasoning outputs from GRPO and MSSR (Multimodal Stabilized Single-Rollout). MSSR produces the correct answer while GRPO fails. We highlight the critical reasoning steps that lead to GRPO’s incorrect answer in red, and the key steps enabling MSSR’s correct prediction in green*

![[assets/figures/papers/paper_list_l2283_https_arxiv_org_abs_2512_18215/figures/014_Figure_10.jpg]]
*Figure 10: Example of reasoning outputs. Comparing the Qwen2.5-VL-7B model fine-tuned with GRPO and MSSR. While GRPO produce incorrect answers, MSSR successfully solves the problem, demonstrating its superior reasoning capability. We highlight the critical reasoning steps that lead to GRPO’s incorrect answer in red, and the key steps enabling MSSR’s correct prediction in green*

## 方法谱系与知识库定位

### 多模态 RLVR 的方法谱系

MSSR 处于**单次推出（single-rollout）RLVR**与**多模态推理**的交叉点，其设计直接回应了现有方法的两个关键瓶颈：组依赖的计算开销和跨模态的熵塌缩。

**组基线方法（group-based）**构成了 MSSR 的直接对比锚点：

- **GRPO**（Shao et al., 2024）：作为当前最强的组基线 RLVR 方法，GRPO 对每个 prompt 采样 $G=8$ 条回复，通过组内均值/标准差归一化计算优势 $A_i = \frac{r_i - \text{mean}(\{r_i\})}{\text{std}(\{r_i\})}$。这种组归一化隐式地提供了方差缩减和熵正则化效应，但代价是每步需要 $G$ 倍的推出计算量。MSSR 的定位是：在仅使用 $1$ 次推出的前提下，通过显式的熵塑造达到与 GRPO 相当的训练稳定性和泛化性能。
- **RLOO**：同为多推出组基线方法，在泛化性能上具有竞争力，但同样面临 $G$ 倍推出开销。在 Table 1 的对比中，RLOO 在多个基准上弱于 MSSR，尤其在大规模模型（7B）上差距更为明显。

**无组方法（group-free）**构成了 MSSR 的技术前身：

- **REINFORCE++**（Hu et al., 2025）：从纯文本 RLVR 适配而来的单次推出基线，在多模态场景下直接塌缩。这揭示了文本域的经验无法简单迁移到视觉-语言联合空间——视觉输入引入的高维噪声使得无组归一化的优势估计方差急剧放大。
- **MVSR（Multimodal Vanilla Single-Rollout）**：本文构建的内部基线，使用共轭 Beta 基线替代组归一化，并进行批次级优势归一化。尽管这些措施部分缓解了方差问题，但**策略熵仍持续塌缩**（Figure 3），验证准确率在训练中后期明显退化（Figure 1b）。这构成了 MSSR 要解决的核心问题：单纯改进基线估计不足以稳定多模态单次推出训练。

**跨模态正则化方法**作为消融对比出现：通过引入纯文本锚策略的 KL 散度约束 $\mathcal{L}_{\mathrm{KL}} = \mathbb{E}[\mathrm{KL}(\pi_\theta(\cdot|x_{\text{text}}, x_{\text{image}}) \parallel \pi_\theta(\cdot|x_{\text{text}}))]$，试图利用文本模态的稳定性来正则化多模态策略。但 Figure 4 显示，该方法仅能部分提升训练准确率，验证准确率仍会退化，且最终性能低于 MSSR。这表明**跨模态约束无法替代对策略熵本身的直接调控**。

### MSSR 在知识库中的定位

从技术机制上看，MSSR 的核心贡献在于**将熵信号直接耦合到优势函数中**，形成一种计算开销极低的训练稳定化策略：

1. **熵优势塑造（entropy-based advantage shaping）**：通过 $\hat{A}_t = A_t + \psi_t$，其中 $\psi_t = \min(|A_t|/\gamma, \lambda \cdot \text{stopgrad}(\mathcal{H}_t))$，MSSR 实现了两个关键效应——当策略熵低时，通过 $\psi_t$ 注入正向奖励鼓励探索；当原始优势为负且绝对值大时，通过 $|A_t|/\gamma$ 上限限制惩罚强度，防止过度抑制低概率但可能正确的推理路径。这与传统的熵正则化（在损失函数中加熵项）有本质区别：后者在消融实验（Figure 4c）中无法有效维持熵或验证性能，因为损失级正则化的梯度信号在单次推出高方差场景下过于微弱。

2. **自适应 Beta 基线**：通过维护每个输入 $x$ 的 Beta 分布 $B(\alpha(x), \beta(x))$ 并以自适应折扣因子 $\eta$ 更新，MSSR 在无需组信息的前提下提供了相对稳定的基线估计。$\eta$ 根据滑动窗口内的平均 KL 散度动态调整（Equation 2-3），在策略剧烈变化时加速遗忘旧估计，在策略稳定时保留更多历史信息。

3. **与 GRPO 的效率-性能权衡**：Table 3 显示，MSSR 的每步训练时间（7B 模型 6.9 mins/step）略高于 GRPO（6.1 mins/step），但考虑到 MSSR 仅需 GRPO 一半的训练步数即可达到相当的验证准确率（Figure 1b），其总体训练计算效率更优。这一优势源于单次推出消除了 $G$ 条回复的生成和评估开销。

### 适用边界与局限

MSSR 的已验证适用边界相对明确：

- **任务域**：当前验证仅限于数学推理领域（基于 Vision-R1-RL 数据集），涵盖 MathVerse、MathVista、MMK12 等数学和多模态推理基准。在开放域视觉问答、文档理解、图表推理等任务上的表现尚未验证。
- **模型规模**：仅在 Qwen2.5-VL 的 3B 和 7B 规模上验证。对于更大规模模型（如 32B、72B）或不同视觉编码器架构，熵塌缩的动力学特性可能发生变化，熵塑造的超参数可能需要重新校准。
- **奖励结构**：当前设置使用二元 Bernoulli 奖励（答案正确/错误），Beta 基线的共轭性质依赖此假设。对于连续奖励或结构化奖励（如部分正确得分、过程奖励），基线估计方法需要相应调整。

### 开放问题

从论文的分析和实验结果中，可以提炼出以下待探索方向：

1. **熵塌缩的跨架构泛化性**：视觉编码器的设计（如 ViT、CNN-based、混合架构）和跨模态融合策略（如 cross-attention、concatenation、perceiver）是否会影响熵塌缩的发生模式和严重程度？MSSR 的熵塑造机制在不同架构下是否需要调整？

2. **自适应熵奖励调度**：当前 $\gamma=0.4$ 和 $\lambda=2.0$ 的设定参考了前人工序，敏感性分析（Figure 6）仅覆盖了滑动窗口大小 $N$ 和目标 KL 值。能否设计一种根据训练动态自动调整 $\gamma$ 和 $\lambda$ 的机制，例如基于熵的滑动统计或验证性能的反馈信号？

3. **与 SFT 的混合训练衔接**：MSSR 目前作为纯 RLVR 阶段使用。在 SFT→RL 的混合训练流程中，SFT 阶段通常会降低策略熵，这可能导致 RL 阶段的初始熵塌缩风险更高。MSSR 的熵塑造机制能否在 SFT 预热后无缝衔接，以及是否需要针对低熵初始化调整 $\lambda$ 参数？

4. **稀疏/延迟奖励场景的适用性**：在多步规划、工具调用、长程推理等奖励更稀疏或延迟的多模态任务中，Beta 基线的更新频率降低，熵塑造是否仍是防止塌缩的最有效手段？是否需要引入额外的信用分配机制（如过程奖励模型）来配合熵正则化？

5. **负迁移风险**：消融实验（Figure 4c）显示熵损失方法在训练后期验证性能退化，MSSR 虽然避免了这一问题，但在简单任务上的过度探索可能导致训练早期回报偏低。是否存在某些任务类型（如低难度、高确定性的视觉识别）上，熵塑造反而引入负迁移？

> **注意**：关于 MSSR 在更大规模模型、非数学域任务、以及与其他视觉编码器架构的兼容性，论文未提供实验证据，上述讨论基于方法机制的合理推演，需后续工作验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/Stable_and_Efficient_Single_Rollout_RL_for_Multimodal_Reasoning.pdf]]
