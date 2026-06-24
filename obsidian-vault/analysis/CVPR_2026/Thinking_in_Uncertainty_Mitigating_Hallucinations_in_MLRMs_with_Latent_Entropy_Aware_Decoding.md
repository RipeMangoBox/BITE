---
title: "Thinking in Uncertainty: Mitigating Hallucinations in MLRMs with Latent Entropy-Aware Decoding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Thinking_in_Uncertainty_Mitigating_Hallucinations_in_MLRMs_with_Latent_Entropy_Aware_Decoding.pdf
project_link: null
code_link: null
aliases:
- LEADL
- TUMHMLEAD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 基于 token 级熵的自适应推理模式切换：当熵升高时，使用概率加权连续嵌入（latent reasoning）保留多条推理路径；同时注入视觉锚点（visual anchor）以增强视觉注意；熵下降时切换回离散嵌入确保精确收敛。
primary_logic: 利用 token 概率分布构建超级位置表示（superposed representation），使模型在高不确定性时维持语义多样性，避免过早收敛到错误的推理链条，从而减少幻觉发生。
claims:
- 掩码高熵 token 导致推理性能显著下降，表明其是关键信息节点。
- 早期推理步骤中的高熵 token 掩码对最终答案的影响最严重，说明这些 token 对整个推理轨迹有方向性引导作用。
- 无幻觉的高熵 token 比幻觉 token 拥有更高的视觉注意力比率。
- 动态熵阈值策略在 MMHalu 数据集上比固定离散或固定潜在推理分别提升约 +4.7%（R1-Onevision）和 +4.1%（Vision-R1）。
---

# Thinking in Uncertainty: Mitigating Hallucinations in MLRMs with Latent Entropy-Aware Decoding

> [!tip] 核心洞察
> 利用 token 概率分布构建超级位置表示（superposed representation），使模型在高不确定性时维持语义多样性，避免过早收敛到错误的推理链条，从而减少幻觉发生。

| 字段 | 内容 |
|------|------|
| 中文题名 | 不确定中的思考：基于潜在熵感知解码减轻多模态推理模型幻觉 |
| 英文题名 | Thinking in Uncertainty: Mitigating Hallucinations in MLRMs with Latent Entropy-Aware Decoding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.13366) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | Latent Entropy-Aware Decoding (LEAD) |
| Dataset | VStar, RealWorldQA, MMHalu, Bingo |

> [!tip] 效果简介
> - VStar 上，Accuracy (%) 71.2 vs 66.5 (+4.7)。
> - RealWorldQA 上，Accuracy (%) 66.4 vs 62.5 (+3.9)。
> - MMHalu 上，Score (0-6) 3.80 vs 3.52 (+0.28 (+4.7% 满分))。

## 概述

多模态推理模型（MLRM）在生成思维链时，经常在推理的“分叉路口”——尤其是过渡词之后——产生幻觉。本文发现，这一现象的根源在于模型在高不确定性状态下采用离散 token 采样，丢弃了概率分布中蕴含的丰富上下文信息，导致模型忽视视觉线索而过早收敛到错误推理链条。

针对这一瓶颈，本文提出**潜在熵感知解码（Latent Entropy-Aware Decoding, LEAD）**，一种即插即用的推理阶段策略。其核心思想是：以 token 级熵作为模型置信度的实时指标，在高熵阶段切换到概率加权连续嵌入（潜在推理），保留多条推理路径的语义多样性；同时注入视觉锚点以增强对图像内容的注意力；待熵回落时再切回离散嵌入，确保精确收敛。

在多个幻觉与通用推理基准上，LEAD 在 7B 规模 MLRM 上取得一致且显著的提升：MMHalu 得分提高约 +4.7%，VStar 准确率提升 +4.7 个百分点，RealWorldQA 提升 +3.9 个百分点，MMEval-Pro 提升 +4.5 个百分点。消融实验证实，动态熵阈值策略优于固定离散或固定潜在推理，且早期高熵 token 对最终答案具有方向性引导作用。LEAD 在提升推理可靠性的同时，未牺牲生成文本的语法、流畅度与自然度。

## 背景与动机

### 多模态推理模型的幻觉困境

多模态推理模型（Multimodal Large Reasoning Models, MLRMs）在视觉问答、数学推理和科学理解等任务上展现出强大的能力，但其生成的推理链中频繁出现幻觉（hallucination），即模型输出的文本内容与视觉输入不一致或完全脱离视觉线索。这一问题严重削弱了模型在医疗、自动驾驶等高风险场景中的可靠性。

对幻觉发生模式的统计分析揭示了一个关键现象：**幻觉倾向于在过渡词（transition words）之后集中出现**。如 Figure 1 所示，在 MLRMs 的推理过程中，“接下来”、“因此”、“基于此”等过渡词之后，模型偏离视觉事实的概率显著升高，且这类过渡词后幻觉占整体幻觉案例的相当大比例。这一观察将问题的焦点从“模型是否产生幻觉”转向了“模型在推理的哪些阶段容易产生幻觉”。

### 高熵推理阶段的“信息塌缩”

进一步的分析表明，过渡词与推理过程中的**高熵状态**高度相关。Figure 2 的可视化显示，在推理链中，token 级熵值（token-level entropy）的高峰往往恰好对应过渡词位置。当模型处于高熵状态时，其预测分布 $p_t[v]$ 在多个候选 token 上分配了相近的概率质量，意味着模型此时面临多条可能的推理路径，尚未形成确定的判断。

然而，现有 MLRMs 普遍采用**离散 token 采样**策略：无论当前预测分布的不确定性有多高，模型都会通过 argmax 或采样将分布“塌缩”为一个 one-hot 向量，仅保留一条推理路径，丢弃概率分布中蕴含的丰富上下文信息。这一操作在高熵阶段尤为危险——模型过早地收敛到某一条推理链条，而该链条可能恰好是偏离视觉事实的错误路径，从而导致幻觉。

### 高熵 Token 的关键性证据

为了验证高熵 token 在推理链中的关键作用，研究者进行了系统性掩码实验（Figure 3）。结果表明：

- **掩码高熵 token 造成的性能下降远大于掩码低熵 token**（Figure 3a），证明高熵 token 承载着对推理结果至关重要的信息。
- **早期推理步骤中的高熵 token 掩码对最终答案的影响最为严重**，而后期 token 的影响逐渐衰减（Figure 3b）。这说明推理链早期的方向性决策对整个推理轨迹具有引导性作用，一旦早期高熵阶段的决策出错，后续推理难以纠正。
- **无幻觉的高熵 token 比产生幻觉的高熵 token 拥有更高的视觉注意力比率**（Figure 3d）。这暗示，高熵阶段模型能否保持对视觉信息的充分关注，是区分正确推理与幻觉的关键分水岭。

### 现有方法的缺口

当前主流的幻觉缓解策略主要分为两类：一类是**对比解码**方法，如 **Visual Contrastive Decoding (VCD)**（Leng et al., CVPR 2024），通过对比原始模型与视觉遮蔽模型的输出分布来增强视觉 grounding；另一类是**记忆空间回溯**方法，如 **Memory-space Visual Retracing (MemVR)**（Zou et al., arXiv 2024）和 **Self-Introspective Decoding (SID)**（Huo et al., arXiv 2024），通过回溯或内省机制纠正推理偏差。

这些方法虽然在不同程度上减轻了幻觉，但存在一个共同局限：**它们仍然在离散 token 空间内操作**，未能解决高熵阶段“信息塌缩”这一根本问题。当模型在过渡词后面对多条可能的推理路径时，现有方法缺乏一种机制来保留语义多样性，避免过早锁定到单一推理链条。

### 本文动机

基于上述分析，本文的核心动机是：**在高不确定性推理阶段，用连续潜在表示替代离散 token 采样，以保留多条推理路径的语义信息，避免因过早收敛而导致的幻觉**。具体而言，本文提出利用 token 概率分布构建**超级位置表示（superposed representation）**，使模型在高熵时维持语义多样性，在熵下降时再切换回离散嵌入以确保精确收敛。同时，在高熵阶段注入视觉锚点以增强模型对视觉内容的注意力，从源头减少幻觉的发生。

## 核心创新

LEAD 的核心创新在于将多模态推理中的**不确定性**从“需要消除的噪声”重新定义为“可以利用的信号”。传统离散链式推理（Standard Discrete CoT）在每一步将完整的预测概率分布坍塌为单个采样 token，丢弃了分布中蕴含的丰富上下文信息。LEAD 通过三个相互协同的机制改变了这一范式。

### 1. 熵感知的推理模式切换

LEAD 引入 **token 级熵** $H_t = -\sum_{v} p_t[v] \log p_t[v]$ 作为模型不确定性的实时度量（Eq.4），并据此在两种推理模式间动态切换：

- **高熵状态（$H_t \geq \hat{H}$）**：触发**潜在推理**（latent reasoning），使用概率加权连续嵌入 $\tilde{e}_t = \mathbb{E}_{v\sim p_t}[e(v)]$（Eq.3），以“超级位置表示”保留多条推理路径，避免过早收敛到错误链条。
- **低熵状态（$H_t < \hat{H}$）**：切换回**离散推理**，使用采样 token 的嵌入 $e(r_t)$，确保语义精确收敛。

模式切换规则（Eq.5）为：
$$\tilde{e}_t = \begin{cases} e(r_t) & H_t < \hat{H} \\ \mathbb{E}_{v\sim p_t}[e(v)] & \text{otherwise} \end{cases}$$

这一机制的根本洞察是：**高熵 token 并非噪声，而是推理路径分岔的关键节点**。Figure 3(a) 的消融实验证实，掩码高熵 token 导致的性能下降远大于掩码其他 token；Figure 3(b) 进一步表明，早期推理步骤中的高熵 token 对最终答案具有方向性引导作用。

### 2. 视觉锚点注入

在高熵阶段的首次 token 处，LEAD 注入预训练视觉特殊 token 的平均嵌入 $e_{\mathrm{vis}}$，以增强模型对视觉信息的注意：
$$\tilde{e}_{t^\star} = (1-\lambda) \mathbb{E}_{v\sim p_{t^\star}}[e(v)] + \lambda e_{\mathrm{vis}}$$
（Eq.9）

这一设计的动机来自 Figure 3(d) 的发现：无幻觉的高熵 token 比幻觉 token 拥有更高的视觉注意力比率。通过在不确定性最高的时刻强制注入视觉先验，LEAD 有效引导模型“回看”图像，从而减少幻觉。Table 1 的消融表明，注入强度 $\lambda=0.4$ 时在 VStar、MMEval-Pro、MMHalu、Bingo 上均取得最优效果。

### 3. 持久窗口与切换控制

为避免频繁模式切换导致的推理不稳定，LEAD 引入**持久窗口**（persistence window）机制：一旦进入某种推理模式，需在该窗口内持续观察熵值，仅在条件持续满足时才允许切换。同时限制总切换次数 $C_{\mathrm{max}}=5$。Figure 6 的消融显示，窗口大小 128 时性能最优——过小导致频繁切换，过大则退化为固定离散推理。

### 与基线方法的本质差异

| 维度 | 标准离散 CoT | VCD / MemVR / SID | LEAD |
|------|-------------|-------------------|------|
| 推理表示 | 离散 one-hot 嵌入 | 离散嵌入 + 对比/回溯/内省 | 熵自适应切换：连续 ↔ 离散 |
| 视觉注入 | 无额外注入 | 对比扰动 / 记忆回溯 | 高熵时刻视觉锚点注入 |
| 模式切换 | 固定离散 | 固定离散 | 基于熵的动态切换 + 持久窗口 |

LEAD 是一种**即插即用的推理阶段策略**，不改变模型参数，可与现有 MLRM 直接集成。其实质是将推理过程中的不确定性显式建模为语义多样性的载体，而非简单地抑制或忽略。

## 整体框架

LEAD（Latent Entropy-Aware Decoding）是一种即插即用的推理阶段解码策略，不改变底层多模态推理模型（MLRM）的任何参数。其核心思想是：在模型逐 token 生成推理链的过程中，利用 token 级熵作为不确定性指示器，动态切换离散推理与潜在推理两种嵌入模式，从而在高不确定性阶段保留多条推理路径，避免过早收敛到错误的推理链条。

### 输入输出流与基础推理范式

LEAD 建立在标准 MLRM 的解码范式之上。给定图像和文本输入，原始图像首先由**视觉编码器**提取语义特征，再通过**跨模态投影**映射到语言模型的输入空间。在标准离散推理模式下，模型在每一步 $t$ 根据当前上下文预测下一个 token 的分布 $p_t \in \Delta^{|\mathcal{V}|-1}$，然后从该分布中采样一个离散 token $r_t$，其嵌入 $e(r_t)$ 作为下一步的输入：

$$p_t = R_\theta\big(e(\mathbf{x}), e(r_{<t})\big), \quad r_t \sim p_t, \quad r_t \in \mathcal{V}$$

这一过程将完整的预测分布坍缩为单个离散 token，丢弃了分布中包含的丰富上下文信息——这正是 LEAD 试图解决的关键瓶颈。

### 熵感知推理模式切换

LEAD 引入了一个**熵感知推理模式切换**模块，以 token 级熵 $H_t$ 作为模型置信度的代理指标：

$$H_t = -\sum_{v} p_t[v] \log p_t[v]$$

当 $H_t$ 超过动态参考阈值 $\hat{H}$ 时，模型进入**潜在推理**模式：不再采样离散 token，而是使用概率加权连续嵌入（即预测分布下的词嵌入期望）作为下一步输入：

$$\tilde{e}_t = \mathbb{E}_{v \sim p_t}[e(v)]$$

这一“超级位置表示”（superposed representation）隐式保留了多条可能的推理路径，使模型在高不确定性时维持语义多样性。当熵回落至阈值以下时，模型切回离散嵌入模式，确保精确的语义收敛。

模式切换由三个机制协同控制：
- **动态熵阈值**（$\Delta$）：根据推理过程中的熵分布自适应调整切换阈值。
- **持久窗口**（persistence window）：防止模式频繁抖动，默认窗口大小为 128 token。
- **最大切换次数**（$C_{\max}=5$）：限制总切换次数，避免推理轨迹过度碎片化。

### 视觉锚点注入

在高熵阶段，模型容易忽视视觉线索而产生幻觉。为此，LEAD 在每个高熵阶段的首次 token $t^\star$ 处执行**视觉锚点注入**：将概率加权嵌入与预训练视觉特殊 token 的平均嵌入 $e_{\mathrm{vis}}$ 进行加权混合：

$$\tilde{e}_{t^\star} = (1-\lambda) \mathbb{E}_{v \sim p_{t^\star}}[e(v)] + \lambda e_{\mathrm{vis}}$$

其中注入强度 $\lambda$ 控制视觉信息的干预程度。这一策略鼓励模型在高不确定性时重新关注视觉内容，增强视觉 grounding。

### 整体流程

LEAD 的完整推理流程如 Figure 4 所示：模型接收视觉和文本 token（左侧），在生成响应时持续计算 token 级熵 $H_t$ 并与参考熵 $\hat{H}$ 比较。高熵状态（橙色）触发潜在解码，使用概率加权嵌入保留语义多样性；低熵状态（蓝色）激活离散解码，使用采样 token 实现精确语义收敛。这种自适应切换机制在多模态推理中实现了探索与承诺之间的动态平衡。

![[assets/figures/papers/paper_list_l940_https_arxiv_org_abs_2603_13366/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of multimodal reasoning and entropy-aware decoding. The model receives both visual and textual tokens (left) and generates responses by integrating contextual information. During reasoning, token-level entropy*

## 核心模块与公式推导

### 3.1 多模态推理模型与离散解码的局限

多模态推理模型（MLRM）接受图像与文本作为输入。原始图像首先经过**视觉编码器（Vision Encoder）**提取语义特征，再通过**跨模态投影（Cross-modal Projection）**映射到语言模型的输入空间。在标准推理过程中，模型在每一步 $t$ 基于多模态上下文和已生成的 token 序列预测下一个 token 的概率分布：

$$p_t = R_\theta\big(\cdot \mid \mathbf{x}, y_{<t}\big) \in \Delta^{|\mathcal{V}|-1}$$

随后从该分布中采样一个离散 token $r_t \sim p_t$，将其嵌入 $e(r_t)$ 作为下一步的输入。这一离散解码策略将完整的预测分布压缩为单一的 one-hot 向量，丢弃了分布中蕴含的丰富上下文信息。当模型处于高不确定性状态时，这种过早的确定性选择极易将推理引入错误路径，从而产生幻觉。

### 3.2 潜在推理：概率加权连续嵌入

LEAD 的核心操作之一是在高熵阶段以**概率加权连续嵌入（probability-weighted continuous embedding）**替代离散 token 嵌入。具体而言，在推理步骤 $t$，模型不采样单个 token，而是计算整个词汇表嵌入的期望：

$$\tilde{e}_t = \mathbb{E}_{v \sim p_t}\big[e(v)\big]$$

该连续向量可视为所有可能 token 嵌入的**超级位置表示（superposed representation）**，它同时保留了多条候选推理路径的语义信息，使模型在高不确定性时维持语义多样性，避免过早收敛到错误的推理链条。

### 3.3 熵感知推理模式切换

模式切换的触发信号来自 **token 级熵（token-level entropy）**，用于量化模型在当前步骤的不确定性：

$$H_t = -\sum_{v} p_t[v] \log p_t[v]$$

LEAD 将当前熵 $H_t$ 与参考阈值 $\hat{H}$ 进行比较，动态选择嵌入模式：

$$\tilde{e}_t = \begin{cases} e(r_t) & H_t < \hat{H} \\ \mathbb{E}_{v\sim p_t}[e(v)] & \text{otherwise} \end{cases}$$

当 $H_t < \hat{H}$ 时，模型处于低不确定性状态，使用离散嵌入确保精确语义收敛；当 $H_t \geq \hat{H}$ 时，模型进入高熵状态，切换为概率加权连续嵌入以保留多条推理假设。

为避免频繁振荡，LEAD 引入**持久窗口（persistence window）**机制：一旦进入某种推理模式，需在该模式下维持一定步数后才允许再次切换。同时设置最大切换次数 $C_{\max}=5$，防止推理过程中模式过度抖动。

### 3.4 视觉锚点注入

在高熵阶段，模型对视觉信息的注意力往往减弱，这是导致多模态幻觉的关键因素。LEAD 在每个高熵阶段的**首个 token**（即进入潜在推理的起始位置 $t^\star$）注入**视觉锚点（visual anchor）**，以增强视觉 grounding：

$$\tilde{e}_{t^\star} = (1-\lambda) \mathbb{E}_{v\sim p_{t^\star}}[e(v)] + \lambda e_{\mathrm{vis}}$$

其中，$e_{\mathrm{vis}}$ 是预训练视觉特殊 token（如 `<|vision_start|>`、`<|image_pad|>`、`<|vision_end|>`）的平均嵌入，$\lambda$ 为注入强度。该操作在保留概率加权嵌入语义多样性的同时，将视觉先验信息显式混合到推理表示中，引导模型在高不确定性时重新关注图像内容。消融实验表明 $\lambda=0.4$ 在多个基准上取得最佳效果（Table 1）。

### 补充图表

![[assets/figures/papers/paper_list_l940_https_arxiv_org_abs_2603_13366/figures/002_Figure_3.jpg]]
*Figure 3: (a) Performance gap when masking different types of token during reasoning. Masking high-entropy tokens produces a larger performance drop than other tokens. (b) Token masking impact across reasoning steps. Earlier tokens tend to have stronger influence on the final answer, while the influence of later ones gradually diminishes. (c) Schematic depiction of reasoning paths at different states. (d) Token density comparisons. On average, high-entropy tokens without hallucinations exhibit higher visual attention ratios compared to hallucinated ones*

![[assets/figures/papers/paper_list_l940_https_arxiv_org_abs_2603_13366/figures/003_Figure_2.jpg]]
*Figure 2: Visualizations of token entropy during the reasoning phase show that tokens with higher entropy often correspond to transition words, consistent with our previous findings*

![[assets/figures/papers/paper_list_l940_https_arxiv_org_abs_2603_13366/figures/001_Figure_1.jpg]]
*Figure 1: Illustrations of the correlation between hallucinations and transition words. In MLRMs, hallucinations tend to emerge more frequently after transition words, and these cases constitute a significant proportion of the overall hallucination occurrences*

## 实验与分析

### 核心发现：高熵token是关键脆弱节点

LEAD 的设计起点是一个可验证的因果假设：多模态推理模型（MLRM）在推理链中产生幻觉，并非随机事件，而是集中发生在模型高度不确定的时刻。作者通过一系列 token 掩码实验验证了这一假设。

**Figure 3 (a-b)** 给出了关键证据。掩码高熵 token 导致的推理性能下降幅度显著大于掩码其他类型 token（Figure 3a），这表明高熵 token 承载着对推理结果至关重要的信息。更值得注意的是，掩码发生的时间点至关重要：在推理链早期步骤中掩码高熵 token，对最终答案的破坏最为严重；随着推理步骤推进，这种影响逐渐衰减（Figure 3b）。这一发现揭示了早期高熵 token 对整个推理轨迹具有方向性引导作用——模型在不确定的十字路口做出的“选择”，会通过自回归机制逐级放大，最终决定推理链条的走向。

**Figure 3 (d)** 进一步揭示了幻觉与视觉注意力的关联：无幻觉的高熵 token 平均拥有更高的视觉注意力比率，而幻觉 token 则表现出视觉注意力不足。这为 LEAD 在高熵阶段注入视觉锚点的策略提供了直接的实证动机。

### 主实验结果：通用推理与幻觉基准

**Table 2** 汇总了 LEAD 在多个 MLRM 上的表现。以 R1-Onevision-7B 为例，LEAD 在幻觉检测基准 MMHalu 上取得 3.80 分（满分 6 分），较基线提升 +0.28 分（相对提升约 +4.7%）；在 Bingo 上取得 3.84 分（满分 5 分），提升 +0.19 分（约 +3.8%）。在需要视觉细节验证的 VStar 基准上，准确率从 66.5% 提升至 71.2%（+4.7%），在 RealWorldQA 上从 62.5% 提升至 66.4%（+3.9%），在 MMEval-Pro 上从 69.4% 提升至 73.9%（+4.5%）。

在 Vision-R1-7B 上，LEAD 同样表现出一致的增益：VStar 准确率从 78.0% 提升至 81.7%（+3.7%），MMEval-Pro 从 71.4% 提升至 75.1%（+3.7%），MMHalu 从 3.69 提升至 3.89（+0.20），Bingo 从 3.56 提升至 3.77（+0.21）。这些结果表明 LEAD 作为一种推理阶段即插即用策略，在不同基础模型上均能稳定提升抗幻觉能力。

### 数学与科学推理基准

**Table 3** 展示了 LEAD 在数学和科学视觉推理任务上的表现。在 MathVision 上，R1-Onevision-7B 的准确率从 28.8% 提升至 32.3%（+3.5%），Vision-R1-7B 从 30.6% 提升至 34.7%（+4.1%）。在 MathVista 上，R1-Onevision-7B 从 66.8% 提升至 71.2%（+4.4%）。在科学推理基准 ScienceQA 上，R1-Onevision-7B 从 85.5% 提升至 87.8%（+2.3%）。这些结果表明，LEAD 的收益不限于专门的幻觉检测基准，在需要严谨推理链的任务中同样有效。

### 消融研究：动态熵阈值的核心作用

LEAD 的核心创新在于根据 token 级熵动态切换推理模式，而非固定使用离散或潜在推理。**Figure 5** 的消融实验直接验证了这一设计选择的必要性。

![[assets/figures/papers/paper_list_l940_https_arxiv_org_abs_2603_13366/figures/005_Figure_5.jpg]]
*Figure 5: Comparisons of average score on MMHalu and Bingo datasets under different entropy thresholds. ∆ denotes the dynamic thresholding strategy in LEAD. ∞ keeps the model in standard discrete CoT reasoning, while 0 keeps it in latent reasoning*

当熵阈值设为 ∞（即始终使用标准离散 CoT 推理）或 0（即始终使用潜在推理）时，模型在 MMHalu 和 Bingo 上的得分均显著低于 LEAD 的动态阈值策略（∆）。动态阈值在 R1-Onevision-7B 上较固定离散推理提升约 +4.7%，较固定潜在推理提升约 +4.1%。这一对比清晰地表明：单纯使用潜在推理并不能解决问题，关键在于**在正确的时刻**切换推理模式——高熵时保留多条推理路径，低熵时精确收敛。

### 消融研究：持久窗口与切换频率

模式切换的频率由持久窗口（persistence window）控制。**Figure 6** 展示了不同窗口大小对 MMHalu 和 Bingo 性能的影响。窗口过小导致频繁切换，模型难以形成稳定的推理链条；窗口过大则退化为近似固定离散推理，丧失了在高熵阶段保留语义多样性的优势。实验表明窗口大小在 128 时达到最佳性能平衡点。此外，作者将单次推理的最大切换次数限制为 5（$C_{\max}=5$），防止过度切换引入噪声。

![[assets/figures/papers/paper_list_l940_https_arxiv_org_abs_2603_13366/figures/007_Figure_6.jpg]]
*Figure 6: Comparisons of model performance under different persistence window sizes. (a) and (b) show model performance with varying window values on the MMHalu and Bingo datasets*

### 消融研究：视觉锚点注入强度

**Table 1** 系统评估了视觉锚点注入强度 λ 的影响。在 R1-Onevision-7B 上，λ=0.4 在四个基准上均取得最佳或接近最佳的结果：VStar 71.2%，MMEval-Pro 73.9%，MMHalu 3.80，Bingo 3.84。当 λ=0（无视觉注入）时，VStar 准确率降至 69.8%，MMHalu 降至 3.70；当 λ 过大（如 0.6-1.0）时，视觉锚点过度主导嵌入表示，反而损害性能。这一非线性关系表明适度的视觉引导最为有效——过弱则视觉 grounding 不足，过强则挤占了语言模型的语义空间。

### 文本质量与推理效率

一个自然的担忧是：在高熵阶段使用概率加权连续嵌入是否会损害生成文本的流畅度和自然度。**Figure 8** 对此进行了评估。在 MMHalu 上，LEAD 生成文本的 PPL（困惑度）、语法正确性、流畅度和自然度评分与基线相当，未出现显著退化。这表明 LEAD 在提升抗幻觉能力的同时，并未牺牲文本质量。

![[assets/figures/papers/paper_list_l940_https_arxiv_org_abs_2603_13366/figures/009_Figure_8.jpg]]
*Figure 8: The average performance is evaluated on MMHalu using R1-Onevision-7B and Vision-R1-7B. PPL1 and PPL2 are calculated using gpt2, while the ratings for Grammar, Fluency and Naturalness are provided by GPT-5*

**Figure 9** 比较了 LEAD 与其他幻觉缓解方法在准确率与推理长度之间的权衡。LEAD 在保持与基线相当的推理长度的同时取得了更高的准确率，而某些对比解码方法（如 VCD）虽然也提升了准确率，但显著增加了推理长度。**Figure 10** 的 Pass@k 评估进一步表明，LEAD 在有限采样预算下具有更好的样本效率。

### 与基线方法的对比

在 Table 2 和 Table 3 中，LEAD 与多种解码策略基线进行了对比。以 R1-Onevision-7B 在 MMHalu 上为例：标准离散 CoT 得分为 3.52，**VCD**（Leng et al., CVPR 2024）为 3.64，**MemVR**（Zou et al., arXiv 2024）为 3.71，**SID**（Huo et al., arXiv 2024）为 3.68，而 LEAD 达到 3.80。LEAD 在所有基准上均优于这些基于对比解码或记忆回溯的方法，且无需额外的视觉扰动或记忆检索模块，仅利用模型自身的概率分布信息。

![[assets/figures/papers/paper_list_l940_https_arxiv_org_abs_2603_13366/figures/011_Table_2.jpg]]
*Table 2: Comparisons of different MLRMs with LEAD across general reasoning and hallucination benchmarks. Scores are reported for MMHalu (ranging from 0 to 6) and Bingo (ranging from 1 to 5), while accuracy is reported for all other benchmarks*

![[assets/figures/papers/paper_list_l940_https_arxiv_org_abs_2603_13366/figures/012_Table_3.jpg]]
*Table 3: Comparisons of different MLRMs with LEAD across mathematical and scientific visual reasoning benchmarks*

### 局限性与失败模式

尽管 LEAD 在多个基准上表现出一致增益，但仍存在若干值得注意的局限：

1. **超参数敏感性**：熵阈值、持久窗口大小（最佳值 128）、最大切换次数（$C_{\max}=5$）和视觉锚点注入强度（最佳值 λ=0.4）均需针对具体模型和任务进行调节。文中提供的默认值基于 7B 规模模型，迁移到其他模型时可能需要重新搜索。

2. **模型规模限制**：实验仅在 7B 规模的 MLRM（R1-Onevision-7B、Vision-R1-7B）上进行，更大规模模型上的效果有待验证。

3. **视觉锚点的编码器依赖**：视觉锚点注入依赖于预训练视觉特殊 token 的平均嵌入，对于使用不同视觉编码器或跨模态投影结构的模型，可能需要适配锚点提取方式。

4. **白盒访问要求**：LEAD 需要获取 token 级概率分布，无法直接应用于仅提供文本输出的 black-box API 服务。

### 补充图表

![[assets/figures/papers/paper_list_l940_https_arxiv_org_abs_2603_13366/figures/006_Table_1.jpg]]
*Table 1: Effect of visual anchor injection strength λ on overall performance. Scores are reported for MMHalu (ranging from 0 to 6) and Bingo (ranging from 1 to 5), while accuracy is reported for VStar and MMEval-Pro. Best results are highlighted in Bold*

![[assets/figures/papers/paper_list_l940_https_arxiv_org_abs_2603_13366/figures/010_Figure_9.jpg]]
*Figure 9: Comparisons of accuracy and reasoning length across multiple hallucination mitigation methods. The x-axis represents the average reasoning length computed on the MathVision dataset with R1-Onevision-7B*

![[assets/figures/papers/paper_list_l940_https_arxiv_org_abs_2603_13366/figures/013_Figure_10.jpg]]
*Figure 10: Pass@k accuracy evaluation of R1-Onevision-7B on sampled data of RealworldQA and MathVista, illustrating results for k ∈ [4, 32]*

## 方法谱系与知识库定位

### 问题定位：多模态推理中的高熵脆弱性

LEAD 的核心切入点并非传统的“幻觉检测”或“后验修正”，而是多模态推理模型（MLRM）在**推理阶段的离散采样机制**。标准离散思维链（CoT）在每一步将完整的预测分布 $p_t$ 坍缩为单个采样 token $r_t$，丢弃了分布中蕴含的语义多样性与不确定性信息。这一机制在高熵推理节点——尤其是过渡词（如“因此”、“接下来”、“然而”）之后——暴露出系统性脆弱：模型在不确定性最高的时刻被迫做出硬性决策，过早收敛到错误的推理链条，从而产生幻觉。

**Figure 1** 和 **Figure 2** 分别从统计和可视化角度揭示了这一关联：幻觉在过渡词后出现的频率显著高于其他位置，且这些 token 的熵值系统性地偏高。这构成了 LEAD 的动机基础——不是消除不确定性，而是在不确定性中维持语义多样性，避免过早锁定错误路径。

### 方法谱系：从对比解码到潜在推理

LEAD 在方法谱系中处于**推理时解码策略**（inference-time decoding）这一分支，与以下基线形成对比：

**对比解码类方法**：**VCD**（Visual Contrastive Decoding, Leng et al., CVPR 2024）通过对原始图像与噪声图像的预测分布进行对比，放大视觉信息的影响。其本质是在输出端施加视觉偏置，但不改变推理过程中的嵌入表示。LEAD 的视觉锚点注入与之有表面相似性，但机制不同：VCD 操作于 logits 层面进行分布对比，LEAD 则在嵌入层面注入视觉先验，且仅在熵升高的关键节点触发。

**记忆回溯类方法**：**MemVR**（Memory-space Visual Retracing, Zou et al., arXiv 2024）通过在记忆空间中回溯视觉信息来修正幻觉。这类方法属于“事后修正”范式，在幻觉可能已经产生后进行干预。LEAD 则属于“事前预防”，在高熵阶段通过潜在推理主动维持多条推理路径，降低幻觉产生的概率。**Figure 7 (a)** 的视觉注意力对比显示，LEAD 在整个推理步骤中维持了更均衡的视觉注意力分配，而 MemVR 的注意力模式更接近基线。

**自我内省类方法**：**SID**（Self-Introspective Decoding, Huo et al., arXiv 2024）通过模型自我评估来检测和修正幻觉。LEAD 与之共享“利用模型内部信号”的设计哲学，但 SID 依赖额外的评估步骤，LEAD 则将不确定性信号（熵）直接嵌入解码循环，无需额外的推理开销。

**固定潜在推理**：将熵阈值设为 0 的纯潜在推理（**Figure 5** 中标记为 0）可视为 LEAD 的一个极端变体。该方法全程使用概率加权连续嵌入，虽保留了语义多样性，但缺乏离散 token 的精确收敛能力，在需要确定性输出的任务上表现不佳。LEAD 的动态切换策略在两者之间取得了平衡。

### 核心机制：熵感知的推理模式切换

LEAD 的方法论贡献可分解为三个相互耦合的机制：

**1. 概率加权嵌入作为超级位置表示**：在高熵状态下，LEAD 不采样离散 token，而是将预测分布 $p_t$ 作为权重，计算所有 token 嵌入的期望 $\tilde{e}_t = \mathbb{E}_{v \sim p_t}[e(v)]$。这一连续嵌入可理解为多条可能推理路径的“超级位置”（superposition），使模型在不确定性最高时保持语义多样性。**Figure 7 (b)** 展示了这一机制的实际效果：高熵 token 的概率分布覆盖多个语义合理的候选项，潜在推理保留了这些可能性，而离散采样则随机选择其一。

**2. 动态切换与持久窗口**：切换规则基于 token 熵与参考阈值的比较（Eq.5），并引入持久窗口机制（persistence window）防止频繁振荡。**Figure 6** 的消融实验表明，窗口大小 128 达到最优——过小导致频繁切换增加计算开销，过大则退化为固定模式。最大切换次数 $C_{\max}=5$ 的设置进一步限制了推理轨迹的复杂度。

**3. 视觉锚点注入**：在高熵阶段的首次 token 处，LEAD 将概率加权嵌入与预训练视觉特殊 token 的平均嵌入 $e_{\mathrm{vis}}$ 进行混合（Eq.9），注入强度 $\lambda$ 控制视觉信息的比重。**Table 1** 显示 $\lambda=0.4$ 在多个基准上取得最优，表明适度的视觉引导最有效——过强会压制文本推理的语义多样性，过弱则不足以提供有效的视觉 grounding。

### 适用边界与局限

LEAD 的适用边界受以下因素制约：

**模型规模与架构依赖**：当前验证仅限于 7B 规模的 MLRM（R1-Onevision-7B 和 Vision-R1-7B）。更大规模模型上的效果有待验证，且模型的预测分布质量直接影响熵估计的可靠性。

**超参数敏感性**：熵阈值、持久窗口大小、最大切换次数、视觉锚点注入强度均需根据模型和任务调节。文中提供的默认值（窗口 128，$C_{\max}=5$，$\lambda=0.4$）在实验设定下有效，但泛化到新模型或新任务时可能需要重新调优。

**白盒访问需求**：LEAD 依赖 token 级概率分布的可获取性，无法直接应用于 black-box API 服务。这限制了其在闭源商业模型上的部署。

**视觉锚点的编码器依赖**：视觉锚点 $e_{\mathrm{vis}}$ 来自预训练视觉特殊 token 的平均嵌入，对于使用不同视觉编码器或投影机制的模型，可能需要重新设计锚点提取策略。

### 开放问题

1. **非推理模型的迁移性**：LEAD 的设计基于 MLRM 的推理阶段特性（过渡词、高熵节点），其在标准多模态大语言模型（MLLM）上的有效性尚未验证。标准 MLLM 的生成模式可能具有不同的熵分布特征。

2. **任务泛化能力**：当前验证集中在视觉推理和幻觉基准上。熵感知切换机制是否可推广到代码生成、多模态对话等需要不同推理模式的任务，仍有待探索。

3. **自适应超参数**：能否通过学习或自适应机制（如基于任务难度动态调整熵阈值）减少对手动调参的依赖，是提升实用性的关键方向。

4. **外部知识融合**：高熵阶段的潜在推理保留了多条语义路径，这为外部知识检索提供了自然的融合接口——能否在潜在空间中注入检索到的知识嵌入，进一步提升事实可靠性？

## 原文 PDF

![[paperPDFs/CVPR_2026/Thinking_in_Uncertainty_Mitigating_Hallucinations_in_MLRMs_with_Latent_Entropy_Aware_Decoding.pdf]]