---
title: "Mixture-of-Experts Can Surpass Dense LLMs Under Strictly Equal Resource"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Mixture_of_Experts_Can_Surpass_Dense_LLMs_Under_Strictly_Equal_Resource.pdf
project_link: https://huggingface.co/kamanphoebe/moe_surpass_dense
code_link: null
openreview_forum_id: oIdzliJAeA
aliases:
- TSSERMF
- MECSDLUSER
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "激活率（activation rate, r_a = N_a / N），即每token激活参数占总参数的比例。该变量直接决定每token计算成本 M，从而在固定训练计算量 C 下控制可用的训练数据量 D，同时调节参数容量与专家特化程度，是影响MoE性能的核心控制因子。"
primary_logic: "通过统一参数化框架和贪心架构搜索，发现存在一个与模型规模（2B–7B）无关的最优激活率 ≈20%。在此区域下，即使面临严格的 N、C、D 三方对等约束（通过数据复用弥补额外数据需求），MoE模型依然能够稳定超越同等条件下的最优稠密基线，证明增益来自架构本身而非资源倾斜。"
claims:
- "在固定训练计算量 C 下，2B MoE 模型在激活率 r_a≈20% 时验证 BPC 达 0.4857，显著优于匹配计算量的最优稠密基线 (BPC 0.4921)。"
- "7B MoE 模型在固定 C=2.86e21 下，r_a=20.07% 取得 BPC 0.4543，大幅超越相同 C 的稠密基线 (BPC 0.4736)，且该最优激活率与 2B/3B 模型一致。"
- "采用严格数据复用策略（固定唯一数据量 D）时，MoE 模型在最优 r_a 下仍保持对稠密基线的优势，性能下降极小，证明在真正的 N/C/D 三者均等条件下 MoE 可稳定超越稠密模型。"
- "SFT 后的 7B MoE (r_a=20%) 在知识、推理、数学、代码等多个下游基准上综合表现优于使用两倍计算量训练的稠密模型。"
---

# Mixture-of-Experts Can Surpass Dense LLMs Under Strictly Equal Resource

> [!tip] 核心洞察
> 通过统一参数化框架和贪心架构搜索，发现存在一个与模型规模（2B–7B）无关的最优激活率 ≈20%。在此区域下，即使面临严格的 N、C、D 三方对等约束（通过数据复用弥补额外数据需求），MoE模型依然能够稳定超越同等条件下的最优稠密基线，证明增益来自架构本身而非资源倾斜。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 严格等资源下MoE可超越稠密大语言模型 |
| 英文题名 | Mixture-of-Experts Can Surpass Dense LLMs Under Strictly Equal Resource |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=oIdzliJAeA) · [Project](https://huggingface.co/kamanphoebe/moe_surpass_dense) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | Three-Step Strictly Equal-Resource MoE Framework |
| Dataset | Validation BPC (2B models, fixed C=9.13e20–9.36e20), Validation BPC (7B models, fixed C=2.86e21), CMMLU (7B SFT, strict data reuse) |

> [!tip] 效果简介
> - Validation BPC (2B models, fixed C=9.13e20–9.36e20) 上，BPC 为 0.4857 (MoE, r_a≈20%)，对比 0.4921 (Dense, same C)，变化 -0.0064。
> - Validation BPC (7B models, fixed C=2.86e21) 上，BPC 为 0.4543 (MoE, r_a=20.07%)，对比 0.4736 (Dense, same C)，变化 -0.0193。
> - CMMLU (7B SFT, strict data reuse) 上，Accuracy 为 32.11 (MoE, r_a=20.07%, strict reuse)，对比 31.23 (Dense)，变化 +0.88。

## 概要

当下混合专家（Mixture-of-Experts, MoE）与稠密大语言模型的对比研究存在一个根本性瓶颈：大多数对比是在资源不对等的条件下进行的——要么激活参数量不匹配，要么训练计算量不一致，导致无法确证MoE架构本身的纯性能增益。本工作提出一个核心问题：**当总参数量 N、训练计算量 C 和唯一数据量 D 三者同时严格相等时，MoE能否超越稠密LLM？**

研究的核心因果控制变量是**激活率**（activation rate, $r_{\mathrm{a}} = N_{\mathrm{a}} / N$），即每个token激活的参数量占总参数量的比例。该变量直接决定每token的计算成本 $M$，从而在固定训练计算量 $C$ 下控制可用的训练数据量 $D$，同时调节参数容量与专家特化程度，是影响MoE性能的关键因子。

通过提出**统一参数化框架**和**三步严格等资源MoE方法**（Three-Step Strictly Equal-Resource MoE Framework），本工作在2B–7B参数规模上进行了系统性实验，训练了近200个2B模型和50余个7B模型，累计处理50万亿tokens。核心发现如下：

- **存在与模型规模无关的最优激活率 ≈20%**。在2B、3B、7B三种规模下，该最优激活率稳定一致。
- **在严格等资源约束下MoE可稳定超越稠密基线**。固定 $C$ 时，2B MoE（$r_{\mathrm{a}} \approx 20\%$）验证BPC达0.4857，显著优于匹配计算量的最优稠密基线（BPC 0.4921）；7B MoE（$r_{\mathrm{a}}=20.07\%$）BPC为0.4543，大幅超越稠密基线（BPC 0.4736）。
- **数据复用策略验证了N/C/D三方等价的鲁棒性**。通过严格数据复用弥补MoE因低激活率而需要的额外数据量，MoE模型仍保持对稠密基线的优势，性能下降极小。
- **下游任务验证上游结论**。SFT后的7B MoE（$r_{\mathrm{a}}=20\%$）在知识、推理、数学、代码等多个基准上综合表现优于使用两倍计算量训练的稠密模型。

这些结果表明，MoE的性能增益源自架构本身的参数利用效率优势，而非资源倾斜。该结论为MoE架构在资源受限场景下的部署提供了有力的理论支撑。



大规模语言模型（LLM）的规模化定律表明，增加模型参数量、训练数据量和计算预算能持续提升模型性能。在这一背景下，**Mixture-of-Experts（MoE）** 架构因其稀疏激活特性——每个 token 仅激活部分参数——成为在固定推理计算预算下扩大模型容量的重要范式。然而，一个根本性的问题始终悬而未决：MoE 的性能增益究竟源于架构本身的归纳偏置，还是仅仅因为资源分配的不对等？

### 现有对比的公平性缺口

当前 MoE 与稠密模型的对比研究普遍存在三类资源不匹配，使得无法分离架构的纯贡献：

1. **激活参数量不匹配**：多数 MoE 对比中，激活参数（即每 token 实际参与计算的参数）与稠密基线不一致。当 MoE 以更大的激活参数量获得更好性能时，增益可能来自参数量的增加而非架构优势。
2. **训练计算量不匹配**：由于 MoE 每 token 的计算成本（FLOPs）与激活率直接相关，在相同训练步数下，不同激活率的模型消耗的计算总量差异显著。若不以固定总计算量 $C$ 为约束，对比结果将混杂计算预算的干扰。
3. **数据量不匹配**：低激活率的 MoE 模型每 token 计算量更小，在固定计算预算下可处理更多 token。若直接使用全部可用数据，MoE 与稠密模型接触的独特数据量 $D$ 不同，数据优势可能被误读为架构优势。

这三重不匹配构成了一个“不可能三角”：在总参数量 $N$ 固定的前提下，训练计算量 $C$ 和独特数据量 $D$ 往往无法同时对齐。此前的工作尚未在 **$N$、$C$、$D$ 三者严格相等**的条件下系统评估 MoE 是否真正优于稠密模型。

### 激活率：核心控制变量

MoE 架构的关键自由度是**激活率（activation rate）**，定义为每 token 激活参数占总参数的比例：

$$r_{\mathrm{a}} = N_{\mathrm{a}} / N$$

激活率直接决定每 token 的计算成本 $M$，进而在固定训练计算量 $C$ 下控制可用的训练数据量 $D = C / M$。同时，$r_{\mathrm{a}}$ 调节着参数容量与专家特化程度之间的权衡：过低的激活率意味着每个专家处理更窄的输入分布，可能促进特化但限制参数利用效率；过高的激活率则趋近于稠密模型，丧失稀疏架构的容量优势。

因此，激活率是决定 MoE 性能的核心控制因子，也是公平对比必须显式扫描和优化的维度。

### 本文的核心追问

本文直面上述公平性缺口，提出一个明确的研究问题：

> **在总参数量、训练计算量和数据量三者严格相等的约束下，MoE 能否超越稠密大语言模型？**

为回答这一问题，本文构建了一套三步实验方法论：首先通过统一参数化框架建立稠密与 MoE 模型的可比基础，然后通过贪心架构搜索确保每个候选模型处于（近）最优配置，最后在严格控制 $N$、$C$、$D$ 的条件下扫描激活率，定位最优 $r_{\mathrm{a}}$ 并比较 MoE 与稠密基线的性能。实验覆盖 2B 至 7B 参数规模，累计训练近 200 个语言模型，处理约 50 万亿 token，旨在提供迄今最严格的公平对比证据。



## 核心方法与创新机理

### 1. 问题重新定义：从“资源不对等”到“三方严格对齐”

此前 MoE 与稠密模型的对比普遍存在资源不对等问题——要么激活参数量不匹配，要么总计算量未对齐，导致无法区分性能增益究竟来自架构本身还是来自隐式的资源倾斜。本工作的核心创新在于将问题重新定义为：**在总参数量 N、训练计算量 C 和唯一数据量 D 三者同时严格相等的条件下，MoE 能否超越稠密 LLM**。这一约束设定直接切断了“用更多资源换性能”的捷径，迫使增益只能来自架构层面的效率优势。

### 2. 核心控制变量：激活率 r_a 的发现与系统化利用

本工作将**激活率** $r_a = N_a / N$（每 token 激活参数占总参数的比例）确立为 MoE 性能的核心控制旋钮。该变量的因果机制体现在：

- **计算成本决定器**：在相同总参数量 N 下，MoE 与稠密模型每 token FLOPs 的比率 $R_c$ 主要由 $r_a$ 决定（见公式 $R_c \approx r_a \cdot (\frac{4+3\alpha+2\gamma_d}{4+3\beta+2\gamma_m})$），因此 $r_a$ 直接控制训练计算量 C 的分配方式。
- **数据量调节器**：低 $r_a$ 意味着每 token 计算成本更低，在固定 C 下可处理更多训练 token，从而引入对数据量 D 的额外需求。这一耦合关系是此前研究普遍忽视的瓶颈。
- **容量与特化的权衡面**：$r_a$ 同时调节参数容量（总专家数 E 随 $r_a$ 降低而增大）与专家特化程度，形成性能的非线性控制面。

通过系统扫描 $r_a$ 从 8% 到 58% 的范围，本文发现存在一个与模型规模（2B–7B）无关的**最优激活率 ≈20%**，在该区域下 MoE 稳定超越等资源稠密基线。

### 3. 方法学创新：三步严格等资源框架

为解决上述三方对齐难题，本文提出了 **Three-Step Strictly Equal-Resource MoE Framework**，其核心模块与 changed slots 如下：

| 步骤 | 模块 | 解决的问题 | 相对于稠密基线的 changed slot |
|------|------|-----------|------------------------------|
| Step 1 | 统一参数化 + 贪心架构搜索 | 确保对比在各自最优架构下进行，消除架构次优性干扰 | FFN 类型、层排列、形状比率 $(\zeta, \mu)$、门控机制 |
| Step 2 | 激活率扫描（固定 N, C） | 定位最优 $r_a$ 并量化纯架构增益 | 激活率从 1.0 → ≈0.20 |
| Step 3 | 数据复用策略 | 消除 MoE 因低 $r_a$ 产生的额外数据需求，实现真正 N/C/D 三方对齐 | 数据消费策略从单轮唯一数据 → 严格/宽松复用 |

**关键 changed slots 详述**：

- **FFN 层类型**：从稠密 SwiGLU FFN 替换为带共享专家的 top-K MoE 层（K>1），门控不使用分数归一化（以兼容 K=1 的实验设置）。
- **层排列**：采用 1 个稠密层 + 剩余 MoE 层的 **1dense+SE** 方案，消融实验表明该排列优于全 MoE 层和交错排列（Table 5），可能因首层稠密有助于训练稳定性。
- **模型形状比率**：MoE 的最优形状超参数 $(\zeta \approx 88, \mu \approx 22$ for 2B; $\zeta \approx 85$ for 7B) 与稠密模型不同，需独立搜索确定（Figure 4, Table 8–13）。
- **数据复用**：针对 MoE 在低 $r_a$ 下需处理更多 token 的问题，提出严格复用（固定唯一数据量 $\hat{D}$，重复使用直至消耗完 C）和宽松复用（固定 2 个 epoch）两种方案。严格复用下 MoE 仍保持对稠密基线的优势，且最优 $r_a$ 不变，证明增益并非来自“看了更多不同数据”（Figure 2b, Table 14–16）。

### 4. 创新点总结

1. **首次在 N/C/D 三方严格相等约束下证明 MoE 可超越稠密模型**，排除了资源倾斜这一混淆因素。
2. **发现并验证了与规模无关的最优激活率 ≈20%**，为 MoE 架构设计提供了明确的指导原则。
3. **建立了统一参数化与贪心搜索相结合的系统性公平比较方法论**，可复用于未来的架构对比研究。
4. **提出数据复用策略作为实现三方对齐的关键技术手段**，解决了低 $r_a$ 带来的数据需求膨胀问题。



为回答“严格等资源下 MoE 能否超越稠密 LLM”这一核心问题，本文提出了一套**三步严格等资源 MoE 框架**（Three-Step Strictly Equal-Resource MoE Framework）。该框架的核心设计原则是：在总参数量 $N$、训练计算量 $C$ 和唯一数据量 $D$ 三者同时匹配的条件下，系统性地比较 MoE 与稠密架构的性能差异，从而剥离资源倾斜带来的混淆效应，纯化出架构本身的增益。

### 统一参数化（Unified Parameterization）

框架的第一步是建立稠密与 MoE 模型的统一参数化表示，将两类架构的关键结构超参数——模型宽度 $D_m$、层数 $L$、FFN 比率 $\alpha$（稠密层）和 $\mu$（MoE 层）、序列长度 $S$ 等——与总参数量 $N$ 和每 token 计算量 $M$ 显式关联。这一环节的关键产出是**激活率**（activation rate）的定义：

$$r_a = N_a / N$$

其中 $N_a$ 为每 token 激活的非嵌入参数量。激活率直接决定 MoE 与稠密模型在相同总参数量下的每 token 计算量比率 $R_c$，是该框架中控制资源分配的核心变量。

### 贪心架构搜索（Greedy Architecture Search）

在统一参数化的基础上，框架通过贪心策略依次确定 MoE 的最优架构组件，确保后续对比在“各自最优”的条件下进行。搜索顺序如下：

1. **层组成**：比较全 MoE 层（full）、交错排列（interleave）和首层稠密 + 其余 MoE 层 + 共享专家（1dense+SE）三种方案，确定 1dense+SE 为最优（Table 5）。
2. **共享专家尺寸比**：验证 $D_{se} / (D_{se} + K D_e)$ 对性能影响微小，简化后续搜索空间（Table 5）。
3. **门控归一化**：消融实验表明门控分数归一化对验证损失无显著影响，且当 $K=1$ 时不可用，故统一不采用（Table 6）。
4. **top-K 设置**：扫描不同 $K$ 值，发现中等 $K$（如 4–6）优于 $K=1$ 或过大 $K$（Table 7）。
5. **模型形状比率**：针对不同 $D_m$ 搜索最优的 $\zeta = D_m / L$ 和 $\mu$，为 2B 模型确定 $\zeta \approx 88$、$\mu \approx 22$，为 7B 模型确定 $\zeta \approx 85$（Table 8, Figure 4）。

### 激活率扫描与等资源对比（Activation Rate Sweep）

在固定最优架构后，框架对激活率 $r_a$ 进行系统性扫描（范围约 8%–58%），在固定 $N$ 和 $C$ 的条件下定位最优激活率 $r_a^{**}$，并将其对应的 MoE 模型与同等 $C$ 下优化后的稠密基线进行直接比较。稠密基线采用 Li et al. (2025) 的超参数缩放律优化形状超参数，学习率和批次大小也统一按该缩放律确定，确保对比公平。

### 数据复用策略（Data Reuse Strategy）

由于低激活率 MoE 在固定 $C$ 下可处理更多 token，若限制唯一数据量 $D$，则需对数据进行复用。框架设计了两种方案：

- **严格复用**：固定唯一数据量 $\hat{D}$，通过重复采样使 MoE 与稠密模型消耗完全相同的唯一 token 数，实现 $N$、$C$、$D$ 三方严格均等。
- **宽松复用**：固定训练 epoch 数（如 2），允许不同 $r_a$ 下实际消耗的唯一数据量不同，仅保证 $N$ 和 $C$ 相等。

两种方案均用于验证最优激活率和 MoE 优势的鲁棒性。

### 下游 SFT 与评估（Downstream SFT and Evaluation）

框架最后将预训练模型进行监督微调（SFT），在知识（MMLU, CMMLU）、推理（ARC-C, HellaSwag）、数学（GSM8K）和代码（HumanEval）等多维度基准上评估下游性能，验证上游结论的泛化性。

### 模块间数据流

整个框架的信息流如下：统一参数化模块输出 $N$、$M$、$r_a$ 的显式关系，作为架构搜索和激活率扫描的约束条件；贪心搜索确定的最优架构（1dense+SE、特定 $\zeta$ 和 $\mu$、无门控归一化、中等 $K$）传递给激活率扫描模块；激活率扫描在固定 $N$ 和 $C$ 下定位 $r_a^{**}$，并将对应 MoE 模型与稠密基线对比；数据复用模块在引入唯一数据量 $D$ 约束后重新评估上述结论的稳定性；最终，最优配置的预训练模型进入 SFT 和下游评估环节。



### 统一参数化框架

为实现稠密与MoE架构在严格等资源条件下的系统对比，论文首先构建了一个统一参数化框架，将两类模型的结构超参数显式关联。该框架的核心在于用共享的符号体系表达参数量 $N$、每token计算量 $M$ 以及激活率 $r_{\mathrm{a}}$，从而为后续的架构搜索与公平比较奠定数学基础。

**稠密模型参数近似**（Section 3.1, Equ. (1)）：

$$N \approx (4 + 3\alpha) D_{\mathrm{m}}^2 L = (4 + 3\alpha) \zeta^2 L^3$$

其中 $D_{\mathrm{m}}$ 为模型隐藏维度，$L$ 为层数，$\alpha = D_{\mathrm{ffn}} / D_{\mathrm{m}}$ 为FFN维度与隐藏维度的比率，$\zeta = D_{\mathrm{m}} / L$ 为模型形状比率。该公式将非嵌入参数量表达为形状超参数的函数，使得不同规模的模型可在统一参数空间中进行比较。

**MoE模型参数近似**（Section 3.1, Equ. (4)）：

$$N \approx (4 + 3\mu) D_{\mathrm{m}}^2 L_{\mathrm{e}} + (4 + 3\alpha) D_{\mathrm{m}}^2 L_{\mathrm{d}}$$

此处 $L_{\mathrm{e}}$ 为MoE层数，$L_{\mathrm{d}}$ 为稠密层数，$\mu = (D_{\mathrm{se}} + E D_{\mathrm{e}}) / D_{\mathrm{m}}$ 为MoE层中总FFN维度（共享专家 $D_{\mathrm{se}}$ 与所有 $E$ 个专家 $D_{\mathrm{e}}$ 之和）与隐藏维度的比率。该公式区分了MoE层与稠密层的参数贡献，使总参数量可精确控制。

**激活率定义**（Section 3.1, Equ. (8)）：

$$r_{\mathrm{a}} = N_{\mathrm{a}} / N$$

激活率 $r_{\mathrm{a}}$ 定义为每token激活的非嵌入参数 $N_{\mathrm{a}}$ 占总非嵌入参数 $N$ 的比例。这是整个研究中最核心的控制变量——它直接决定每token的计算成本，从而在固定训练计算量 $C$ 下调控可用的训练数据量 $D$，同时调节参数容量与专家特化程度。

**计算量比率**（Section 3.2, Equ. (10)）：

$$R_{\mathrm{c}} = r_{\mathrm{a}} \left( \frac{4 + 3\alpha + 2\gamma_{\mathrm{d}}}{4 + 3\beta + 2\gamma_{\mathrm{m}}} \right)$$

该公式给出了相同总参数量下MoE与稠密模型每token FLOPs的比率 $R_{\mathrm{c}}$。其中 $\beta = (D_{\mathrm{se}} + K D_{\mathrm{e}}) / D_{\mathrm{m}}$ 为MoE层中激活FFN维度与隐藏维度的比率（$K$ 为top-K选中的专家数），$\gamma_{\mathrm{d}}$ 和 $\gamma_{\mathrm{m}}$ 分别为稠密层和MoE层中注意力计算相关的比率项。由于括号内因子在不同架构间差异有限，**激活率 $r_{\mathrm{a}}$ 是决定计算量比率的主导因素**——这正是后续实验系统扫描 $r_{\mathrm{a}}$ 的理论依据。

**MoE层输出与负载均衡**（Appendix A）：

$$y = \sum_{i=1}^{E} g_i(x) \cdot E_i(x)$$

$$\mathcal{L}_{\mathrm{balance}} = E \sum_{i=1}^{E} f_i p_i, \quad \mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{CE}} + \lambda \mathcal{L}_{\mathrm{balance}}$$

MoE层的输出为门控分数 $g_i(x)$ 对各专家输出 $E_i(x)$ 的加权求和。辅助负载均衡损失 $\mathcal{L}_{\mathrm{balance}}$ 通过惩罚专家使用频率 $f_i$ 与平均门控概率 $p_i$ 的乘积来促进专家间的均匀利用，并与交叉熵损失 $\mathcal{L}_{\mathrm{CE}}$ 以权重 $\lambda$ 组合为总训练损失。

### 三步实验方法论

在统一参数化框架之上，论文设计了严格的三步实验流程（Section 3.3）：

1. **贪心架构搜索**（§4）：依次确定层组成（1dense+SE）、门控机制（无归一化）、top-K设置（中等K值如4–6）及模型形状比率（$\zeta$、$\mu$），确保每个候选模型在对比前已达（近）最优架构配置。

2. **激活率扫描**（§5）：在固定总参数量 $N$ 和训练计算量 $C$ 下，系统扫描8%–58%的激活率区间，定位使验证损失最小的最优 $r_{\mathrm{a}}^{*}$，并与同等资源下的最优稠密基线直接比较。

3. **数据复用策略**（§6）：针对MoE因低激活率而需处理更多token（但唯一数据量可能不足）的问题，提出严格复用（固定唯一数据量 $D$）和宽松复用（固定训练轮次）两种方案，确保在 $N$、$C$、$D$ 三者均等的终极约束下完成公平评估。



## 实验与关键发现

### 核心发现：最优激活率 ≈20%

本文的核心实验目标是验证在严格等资源（总参数量 N、训练计算量 C、唯一数据量 D）约束下，MoE 架构能否稳定超越稠密基线。实验覆盖 2B、3B、7B 三个模型规模，共训练近 200 个 2B 级模型和 50 余个 7B 级模型，累计处理 50 万亿 token。

**关键控制变量：激活率 $r_a$**。$r_a = N_a / N$ 定义为每 token 激活参数占总非嵌入参数的比例，直接决定每 token 计算成本 $M$，进而在固定训练计算量 $C$ 下控制可用的训练数据量 $D$。这是连接参数量、计算量和数据量三方约束的核心因果旋钮。

**主结果 1：固定 C 下 MoE 超越稠密基线（2B 规模）**。在 $N \approx 2.15\text{B}$、固定训练计算量 $C \approx 9.13 \times 10^{20} \sim 9.36 \times 10^{20}$ FLOPs 的条件下，激活率扫描（8%–58%）显示最优激活率 $r_a^{**} \approx 20\%$。该配置下 MoE 模型验证 BPC 为 0.4857，显著优于同等计算预算下的最优稠密基线（BPC 0.4921），差距为 -0.0064（Table 10, Table 13）。该差异在语言建模的 BPC 尺度上具有实质意义，且所有对比模型均使用通过超参数缩放律优化的形状超参数（如 $\zeta \approx 88$），排除了架构次优性的干扰。


![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_oIdzliJAeA/figures/014_Table_10.jpg]]
*Table 10: Experimental settings and results of optimal ARs for MoE models N = 2.15B with fixed C. Hyperparameters shared by all experiments: L = 1 6 , S = 2 0 4 8 , $D _ { \mathrm { m } }$ = 1 4 0 8 , $D _ { \mathrm { f f n } }$ = 3 9 0 4 , H = 11, $D _ { \mathrm { h } }$ = 1 2 8 , $\zeta$ = 8 8 . The green row corresponds to the MoE model with the lowest BPC on the validation set

**主结果 2：7B 规模下结论一致且增益更大**。在 $N \approx 6.52\text{B}$、固定 $C = 2.86 \times 10^{21}$ FLOPs 的条件下，$r_a = 20.07\%$ 的 MoE 模型取得 BPC 0.4543，大幅超越相同计算量的稠密基线（BPC 0.4736），差距扩大至 -0.0193（Table 12, Table 13）。这一结果表明，随着模型规模增大，MoE 在等计算约束下的相对优势可能进一步放大。

**主结果 3：最优激活率与模型规模无关**。Figure 1、Figure 2 和 Figure 5 共同揭示，在 2B、3B、7B 三个规模下，验证损失随 $r_a$ 的变化曲线均在 $r_a \approx 20\%$ 处达到最低点。这一跨规模的稳定性是该工作最重要的经验发现之一，暗示存在一个由架构内在特性决定的“甜区”，而非由特定模型尺寸或训练预算偶然产生。


![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_oIdzliJAeA/figures/002_Figure_1.jpg]]
*Figure 1: Performance of N $\approx$ 2 $\mathrm { B }$ models trained with varying data sizes D and activation rates $r _ { \mathrm { a } }$ . (a) With a fixed D , performance gain exhibits a non-linear dependence on training budget C. Conversely, with a fixed $r _ { \mathrm { a } }$ . , increasing D leads to a linear performance gain. These findings indicate an optimal activation rate, $r _ { \mathrm { a } } ^ { * * }$ = 2 0 \% , that is consistent across various $\bar { D }$ values when N is constant. (b) With a fixed training compute C , the optimal activation rate $r _ { \mathrm { a } } ^ { * * }$ = 2 0 \% can be clearly seen

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_oIdzliJAeA/figures/003_Figure_2.jpg]]
*Figure 2: Performance of N $\approx$ 7 $\mathrm { B }$ models trained with varying data sizes D and activation rate $r _ { \mathrm { a } }$ . The optimal activation rate, $r _ { \mathrm { a } } ^ { * * }$ = 2 0 \% , align with the findings for the 2B models (Figure 1). Additionally, compared to training on the unique dataset, the strict data reuse scheme shows only a slight performance reduction, while the loose scheme often yields better performance

### 严格数据复用下的鲁棒性验证

MoE 模型因低激活率而具有更低的每 token 计算成本，在固定 $C$ 下自然需要处理更多 token 才能消耗完计算预算。这引出一个关键公平性问题：如果 MoE 模型“看到”了更多唯一数据，其性能优势是否来自数据量的不对称？

为消除这一混淆因素，本文设计了两种数据复用方案：

- **严格复用**：固定唯一数据量 $D$，通过重复数据使 MoE 和稠密模型在总消耗 token 数（即 $C$）和唯一数据量上完全对齐。
- **宽松复用**：固定训练 epoch 数为 2，允许不同 $r_a$ 的模型使用不同的唯一数据量。

在 7B 规模的严格复用实验中（$\hat{D} = 68\text{B}$，Table 14），$r_a = 20.07\%$ 的 MoE 模型 BPC 为 0.4548，仍显著优于稠密基线的 0.4736。3B 规模的严格复用实验（$\hat{D} = 65\text{B}$，Table 15）同样确认 MoE 优势保持。Figure 2b 和 Figure 5 进一步显示，数据复用仅带来轻微的性能下降，且最优激活率 $r_a^{**}$ 在复用条件下完全不变。

这一发现排除了“数据量不对等”作为 MoE 优势来源的替代解释，证明增益确实来自 MoE 架构本身的归纳偏置。

### 下游任务验证

为检验预训练结论的泛化性，本文对 7B 模型进行监督微调（SFT），在知识、推理、数学、代码等多维度基准上评估（Table 2, Figure 3）。


![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_oIdzliJAeA/figures/005_Table_2.jpg]]
*Table 2: Accuracy of 7B SFT-ed models across different benchmarks*

**核心结论**：$r_a = 20\%$ 的 MoE 模型在严格数据复用条件下，综合下游表现优于使用两倍计算量训练的稠密模型。具体而言：
- CMMLU 准确率：MoE (strict) 32.11 vs. Dense 31.23（+0.88）
- 推理类基准（如 DROP）：MoE 保持稳定优势
- 知识密集型基准（如 MMLU）：数据复用导致一定性能下降（MoE strict 24.57 vs. Dense 25.21），但在宽松复用下 MoE 可恢复优势

这一模式揭示了一个重要的权衡：**数据复用对推理能力的损害极小，但对知识记忆有显著负面影响**。这暗示 MoE 的专家路由机制天然有利于推理模式的泛化，而知识存储可能更依赖充分的唯一数据曝光。

### 架构消融：为何是“1dense+SE”？

在激活率扫描之前，本文通过贪心搜索确定了最优 MoE 架构骨架（Section 4），关键消融结论如下：

| 消融维度 | 结论 | 证据 |
|---------|------|------|
| 层排列 | `1dense+SE`（首层稠密 + 其余 MoE 含共享专家）优于全 MoE 和交错排列 | Table 5 |
| 共享专家尺寸比 | $D_{se} / (D_{se} + K D_e)$ 对性能影响微小 | Table 5 |
| 门控归一化 | 归一化降低负载均衡损失但对验证损失无显著影响；$K=1$ 时不可用 | Table 6 |
| top-K 设置 | $K=4\sim6$ 效果最佳，$K=1$ 和过大的 $K$ 均为次优 | Table 7 |
| 模型形状比 | $\zeta \approx 88$（2B）、$\zeta \approx 85.3$（7B），$\mu$ 随 $D_m$ 增大呈下降趋势 | Table 8, Figure 4 |


![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_oIdzliJAeA/figures/009_Table_5.jpg]]
*Table 5: Experimental settings and results of MoE layer arrangement and shared expert. Hyperparameters shared by all experiments: $D _ { \mathrm { m } }$ = 1 4 0 8 ， $D _ { \mathrm { f f n } }$ = 3 9 0 4 ， $\mathbf { \bar { N o r m } } = \mathbf { T r u e }$

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_oIdzliJAeA/figures/010_Table_6.jpg]]
*Table 6: Experimental settings and results of gate score normalization. Hyperparameters shared by all experiments: Scheme = 1dense, L = 1 7 $D _ { \mathrm { m } }$ = 1 4 0 8 $D _ { \mathrm { f f n } }$ = 3 9 0 4 , H = 22, $D _ { \mathrm { h } }$ = 6 4

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_oIdzliJAeA/figures/011_Table_7.jpg]]
*Table 7: Experimental settings and results of top-K setting. Hyperparameters shared by all experiments: Scheme = ${ \mathrm { 1 d e n s e } }$ L = 1 6 $D _ { \mathrm { m } }$ = 1 4 0 8 ， $D _ { \mathrm { f f n } }$ = 3 9 0 4 , H = 11, $D _ { \mathrm { h } }$ = 1 2 8 , Norm = False

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_oIdzliJAeA/figures/012_Table_8.jpg]]
*Table 8: Experimental settings and results of model shape ratios. Hyperparameters shared by all experiments: Scheme = 1dense, S = 16384, $D _ { \mathrm { h } }$ = 1 2 8*

这些消融确保后续的激活率对比建立在已充分优化的架构基础之上，排除了“MoE 架构未调优”作为竞争性解释的可能性。

### 失败模式与局限

1. **知识密集型任务的退化**：在严格数据复用下，MoE 模型在 MMLU 等知识记忆型基准上出现性能下降。这表明低激活率 + 数据复用的组合可能限制了模型对稀有知识的有效编码，专家路由的稀疏性可能加剧了知识存储的“容量瓶颈”。

2. **规模上限未验证**：实验限于 2B–7B 参数规模，更大规模（如 70B+）下最优激活率是否仍维持 20% 尚未可知。随着模型容量增长，专家特化程度与最优 $r_a$ 的关系可能发生变化。

3. **数据配方依赖性**：训练数据为内部混合数据集（Table 3），与公开数据集（如 The Pile）存在差异，可能影响结论的外部可复现性。最优激活率的普适性需要在不同数据分布下进一步验证。


![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_oIdzliJAeA/figures/006_Table_3.jpg]]
*Table 3: Pretraining data recipe compared with the LLaMA-1 recipe*

4. **专家特化机制未解**：本文仅从现象层面确认了最优激活率的存在，但未深入分析该激活率如何通过影响专家特化程度来提升模型能力，这一因果链仍停留在猜测层面。

### 关键图表导航

- **Figure 1**：2B 模型验证损失随 $r_a$ 和 $D$ 的变化曲面，(b) 子图清晰展示固定 $C$ 下 $r_a^{**} \approx 20\%$ 的最优点。
- **Figure 2**：7B 模型对应结果，同时展示严格/宽松数据复用效果，确认最优激活率跨规模一致。
- **Figure 3**：7B SFT 模型下游性能雷达图，MoE ($r_a=20\%$) 在多维度上超越 2× 计算量稠密基线。
- **Table 2**：SFT 模型在各基准上的详细准确率，含严格/宽松复用对比。
- **Table 10, 12, 13**：固定 $C$ 下 2B/7B MoE 与稠密基线的完整实验配置与 BPC 结果。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_oIdzliJAeA/figures/001_Table_1.jpg]]
*Table 1: Notation*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_oIdzliJAeA/figures/008_Table_4.jpg]]
*Table 4: Common training recipe*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_oIdzliJAeA/figures/013_Table_9.jpg]]
*Table 9: Experimental settings and results of optimal ARs for MoE models with N = 2.15B and fixed ra. Hyperparameters shared by all experiments: L = 16, S = 2048, Dm = 1408, $D _ { \mathrm { f f n } }$ = 3904, H = 11, Dh = 128, ζ = 88*




## 定位与知识库关联

### 1. 与稠密基线的严格对比定位

本工作的核心基线是**经过形状超参数优化的稠密 Transformer**。作者采用 Li et al. (2025) 提出的超参数缩放律，对稠密模型的形状比率 $\zeta$（$D_m/L$ 的比值）和 $\alpha$（FFN 维度与 $D_m$ 的比值）进行优化，确保稠密基线在给定的总参数量 $N$ 和训练计算量 $C$ 下达到近似最优性能。这一设计使得后续的 MoE 对比不再是“优化后的 MoE vs 未优化的稠密”，而是两种架构在各自最优配置下的公平较量。

MoE 模型与稠密基线的核心差异体现在五个架构槽位上：

| 架构槽位 | 稠密基线 | 本文 MoE 方案 |
|---|---|---|
| FFN 类型 | Dense SwiGLU FFN | Top-K MoE + 共享专家，无门控归一化（$K>1$） |
| 激活率 $r_a$ | 1.0（全部参数激活） | ≈0.20（贪心搜索确定的最优值） |
| 层排列 | 全部稠密层 | 1 层稠密 + 其余 MoE 层（1dense+SE） |
| 形状比率 $\zeta, \mu$ | 针对稠密优化 | 针对 MoE 重新搜索（如 2B: $\zeta\approx 88$, $\mu\approx 22$） |
| 数据消耗策略 | 单轮唯一数据 | 严格/宽松数据复用以匹配唯一数据预算 $D$ |

通过这五个维度的对齐，作者在 $N$、$C$、$D$ 三者同时相等的条件下建立了 MoE 与稠密模型的公平比较框架，这是本工作区别于此前大多数 MoE 研究的关键方法论贡献。

### 2. 方法谱系中的定位

本工作处于 **MoE 架构公平性评估** 这一细分方向，其方法论可拆解为五个串联模块：

1. **统一参数化框架**：将稠密和 MoE 模型的参数量 $N$、每 token FLOPs $M$、激活率 $r_a$ 用共享的结构超参数显式关联，核心公式为 $R_c \approx r_a \left( \frac{4 + 3\alpha + 2\gamma_d}{4 + 3\beta + 2\gamma_m} \right)$，揭示激活率是控制计算量的主导因子。

2. **贪心架构搜索**：依次确定层组成（1dense+SE 最优）、门控机制（无归一化，因 $K=1$ 时归一化导致零梯度）、top-K 设置（中等 $K$ 如 4–6 优于过大或 $K=1$）及形状比例 $\zeta, \mu$。

3. **激活率扫描**：在固定 $N$ 和 $C$ 下扫描 8%–58% 的激活率，定位最优 $r_a^* \approx 20\%$。

4. **数据复用策略**：针对低 $r_a$ 导致的数据需求膨胀问题，提出严格（固定唯一数据量 $D$）和宽松（固定训练轮次）两种复用方案。

5. **下游 SFT 验证**：对预训练模型进行监督微调，在知识、推理、数学、代码等多维度基准上验证上游结论的泛化性。

该方法链的核心因果机制是：激活率 $r_a$ 作为控制旋钮，通过调节每 token 计算成本 $M$，在固定 $C$ 下反向决定可用的训练数据量 $D$，同时影响参数容量与专家特化程度。实验表明存在一个与模型规模（2B–7B）无关的最优激活率 ≈20%，在此区域下 MoE 可稳定超越等资源稠密基线。

### 3. 适用边界与局限

**已验证的适用范围**：
- 模型规模：2B–7B 参数，更大规模（70B+）下最优激活率是否保持 20% 有待验证
- 训练范式：从零开始的预训练（from-scratch），未覆盖 upcycling 或 MoEfication 等范式
- 架构配置：1dense+SE 层排列、特定形状比率、无门控归一化的 top-K 路由

**已知的局限与退化场景**：
- **数据复用导致知识密集型任务退化**：在严格等数据方案下，知识密集型基准（如 MMLU）性能下降，可能影响强记忆依赖场景的实用性
- **最优激活率的普适性未验证**：20% 的结论依赖于内部数据配方和特定架构优化，尚未验证其对不同数据分布或领域特化的稳定性
- **专家特化机制未解耦**：未深入分析专家特化程度与激活率之间的因果关系，仅停留在猜测层面
- **外部可复现性受限**：训练数据为内部混合数据集，与公开数据集（如 The Pile）的差异可能影响结果的外部复现性

### 4. 开放问题

1. **最优激活率的规模泛化性**：在数十 B 参数规模或不同数据分布下，最优激活率是否仍维持在 20% 附近？
2. **跨范式迁移性**：本结论对于其他 MoE 训练范式（如 upcycling、MoEfication）是否同样成立？
3. **能力增强机制**：最优激活率如何具体增强模型能力——是通过促进专家特化、改善负载均衡，还是其他机制？
4. **数据效率优化**：能否设计更高效的数据复用策略，完全消除在严格等数据约束下对唯一 token 数的额外需求？
5. **与推理效率的联合优化**：当前分析聚焦预训练损失和下游准确率，最优激活率在推理延迟/吞吐量约束下是否需要调整？



## 原文 PDF

![[paperPDFs/ICLR_2026/Mixture_of_Experts_Can_Surpass_Dense_LLMs_Under_Strictly_Equal_Resource.pdf]]
