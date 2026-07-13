---
title: "RAAS: LLM Agentic System Architecture Search with GRPO"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RAAS_LLM_Agentic_System_Architecture_Search_with_GRPO.pdf
project_link: null
code_link: "https://github.com/ridlog/raas"
aliases:
- RRAAS
- RAAS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过两个协同机制实现稳定评估：上下文架构编排（CAO）在同查询上比较候选架构的同行群体，推导出上下文相关的零中心优势信号，解耦任务难度；多试验评估综合（MTAS）聚合多次独立试验的结果，减少执行方差，提供统计上稳健的能力估计。
primary_logic: 稳定的评估信号是智能体架构搜索的关键，通过同行比较消除任务难度偏差，并通过多试验聚合消除执行随机性，从而准确反映架构的真实价值。
claims:
- RAAS在六个基准上一致超过强基线，平均提升+5.41，HumanEval pass@1提升4.08个百分点，MATH accuracy提升8.79个百分点。
- 消融实验表明，移除CAO导致性能下降至接近MaAS基线水平，禁用MTAS则重新引入执行波动并降低最终准确率。
- MATH 上 Accuracy = 60.87%
- GSM8K 上 Accuracy = 95.16%
---

# RAAS: LLM Agentic System Architecture Search with GRPO

> [!tip] 核心洞察
> 稳定的评估信号是智能体架构搜索的关键，通过同行比较消除任务难度偏差，并通过多试验聚合消除执行随机性，从而准确反映架构的真实价值。

| 字段 | 内容 |
|------|------|
| 中文题名 | RAAS：基于GRPO的LLM智能体系统架构搜索 |
| 英文题名 | RAAS: LLM Agentic System Architecture Search with GRPO |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Yang_RAAS_LLM_Agentic_System_Architecture_Search_with_GRPO_CVPR_2026_paper.html) · [Code](https://github.com/ridlog/raas) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | RAAS (Robust Architecture Adaptive Search) |
| Dataset | MATH, GSM8K, HumanEval, MBPP |

> [!tip] 效果简介
> - MATH 上，Accuracy 60.87% vs 52.08% (+8.79)。
> - GSM8K 上，Accuracy 95.16% vs 91.84% (+3.32)。
> - HumanEval 上，pass@1 96.31% vs 92.23% (+4.08)。

## 概要

### 问题背景

大语言模型（LLM）驱动的智能体系统在复杂推理任务中展现出巨大潜力，但如何自动设计最优的智能体架构仍是一个开放挑战。现有架构搜索方法面临**评估不稳定性**这一核心瓶颈，具体表现为：

- **任务难度纠缠**：绝对性能分数将架构的内在质量与查询的外部难度混为一谈，导致弱架构在简单查询上看似强大，而强架构在困难查询上被低估。
- **执行方差干扰**：单次执行协议捕获的是执行随机性而非真实能力，评估信号不可靠，无法准确反映架构的真实价值。

这些不稳定性使得搜索过程难以有效区分优劣架构，阻碍了高性能智能体系统的自动化发现。

### 核心方法

RAAS（Robust Architecture Adaptive Search）通过两个协同机制构建稳定的评估体系：

1. **上下文架构编排（CAO）**：在同查询上比较候选架构的同行群体，推导出上下文相关的零中心优势信号，解耦任务难度对评估的干扰。
2. **多试验评估综合（MTAS）**：聚合多次独立试验的结果，减少执行方差，提供统计上稳健的能力估计。

在此基础上，RAAS 采用**优点加权适应**策略，基于上下文优点信号调整算子概率分布，将优化信号精确追溯到具体架构组件。

### 主要结果

RAAS 在六个基准上一致超越强基线，平均提升 **+5.41** 个百分点：

| 基准 | 指标 | RAAS | 最强基线 | 提升 |
|------|------|------|----------|------|
| MATH | Accuracy | 60.87% | 52.08% | +8.79 |
| GSM8K | Accuracy | 95.16% | 91.84% | +3.32 |
| HumanEval | pass@1 | 96.31% | 92.23% | +4.08 |
| MBPP | Accuracy | 84.18% | 78.71% | +5.47 |
| GAIA | Avg Accuracy | 20.84% | 18.06% | +2.78 |

消融实验证实，CAO 和 MTAS 具有协同作用：移除 CAO 导致性能下降至接近基线水平，禁用 MTAS 则重新引入执行波动并降低最终准确率。同时，RAAS 在保持性能优势的同时实现了更优的成本-性能权衡。

### 方法定位

RAAS 属于**基于搜索的智能体架构自动设计**方法，与以下工作形成对比：

- **MaAS**（Zhang et al., 2025）：直接基线，同样基于 Agentic Supernet 进行架构搜索，但使用单次绝对评估，受评估不稳定性困扰。
- **ADAS**（Hu et al., 2025）与 **AgentSquare**（Shang et al., 2025）：自动化智能体系统设计，但未针对性解决评估信号的稳定性问题。
- **AFlow**（Zhang et al., 2025）与 **DyLAN**（Liu et al., 2024）：分别聚焦工作流生成和动态协作网络，与 RAAS 的架构搜索视角互补。

RAAS 的核心贡献不在于搜索空间的设计，而在于**评估范式的革新**——通过同行比较消除任务难度偏差，通过多试验聚合消除执行随机性，从而为架构搜索提供可靠的优化信号。



### 智能体系统的自动化设计需求

大语言模型（LLM）驱动的智能体系统已在数学推理、代码生成、多步骤决策等复杂任务中展现出显著能力。这些系统通常由多个功能模块（如规划器、反思器、工具调用器）按特定拓扑结构编排而成，其架构设计直接影响最终性能。然而，手工设计有效的智能体架构需要大量专家知识和反复试错，这推动了自动化架构搜索方法的发展。

### 现有架构搜索方法的评估困境

当前主流的智能体架构搜索方法，如 **MaAS**（Zhang et al., 2025）、**ADAS**（Hu et al., 2025）、**AgentSquare**（Shang et al., 2025）和 **AFlow**（Zhang et al., 2025），普遍面临一个核心瓶颈：**评估不稳定性**。这一瓶颈体现在两个相互纠缠的维度上：

**任务难度纠缠**：现有方法通常基于单个架构在单个查询上的绝对性能评分来指导搜索。这种评估方式将架构的内在质量与查询的外部难度混为一谈——弱架构在简单查询上可能获得虚高的分数，而强架构在困难查询上则可能被低估。如图1(A)所示，这种混淆导致搜索信号被任务难度噪声严重污染。

**执行方差**：LLM 的输出具有固有的随机性，单次执行协议捕获的往往是执行过程中的瞬态伪影，而非架构的真实能力。当每个候选架构仅执行一次时，评估结果更多地反映了采样随机性，而非架构设计的优劣。

这两个问题共同导致了一个恶性循环：不可靠的评估信号 → 错误的架构选择 → 次优的搜索方向 → 最终性能受限。

### RAAS 的动机与设计思路

上述困境揭示了一个关键洞察：**稳定的评估信号是智能体架构搜索的前提条件**。只有消除任务难度偏差和执行随机性，才能准确反映架构的真实价值，从而引导搜索走向更优的设计。

基于这一洞察，RAAS 通过两个协同机制重构了评估范式：

1. **上下文架构编排（CAO）**：在同查询上比较候选架构的同行群体，推导出上下文相关的零中心优势信号，从而解耦任务难度。每个架构的能力不再以绝对分数衡量，而是以相对于同行基线的偏差来量化。

2. **多试验评估综合（MTAS）**：对每个架构执行多次独立试验，通过统计合成函数聚合结果，有效消除执行方差，提供统计上稳健的能力估计。

图1(B) 展示了 RAAS 的解决方案：通过同行比较消除任务难度偏差，通过多试验聚合消除执行随机性，两者协同产生稳定的评估信号，为可靠的架构发现奠定基础。



## 核心方法与创新机理

RAAS的核心创新在于**重构了智能体架构搜索的评估信号**，将不可靠的绝对性能比较转化为统计稳健的上下文相对评估。这一转变通过两个协同机制实现，对应三个关键的*changed slots*。

### 1. 评估信号类型：从绝对评分到上下文优点

现有方法（如**MaAS** (Zhang et al., 2025)、**ADAS** (Hu et al., 2025)、**AgentSquare** (Shang et al., 2025)）直接使用单个架构在单个查询上的绝对性能评分作为优化信号。这种设计存在根本性缺陷：绝对分数将架构的内在质量与查询的外部难度**纠缠**在一起——弱架构在简单查询上可能获得高分，强架构在困难查询上可能被低估，导致搜索过程被任务难度偏差误导。

RAAS通过**上下文架构编排（CAO）**解耦这一纠缠。其核心操作是：对于每个查询 $q$，同时采样 $N$ 个候选架构构成同辈群体，计算群体平均能力作为上下文基线：

$$\bar{R}_{\mathrm{ctx}}(q) = \frac{1}{N} \sum_{i=1}^{N} \hat{R}(\mathcal{G}_i, q)$$

然后推导每个架构的**上下文优点（Contextual Merit）**：

$$M_{\mathrm{ctx}}(\mathcal{G}_i, q) = \hat{R}(\mathcal{G}_i, q) - \bar{R}_{\mathrm{ctx}}(q)$$

这一零中心信号自动消除了查询难度的影响——无论查询简单还是困难，优点信号只反映架构相对于同辈群体的能力偏差。论文从方差分解的角度论证了这一设计的合理性：

$$\mathrm{Var}[\hat{R}_i] = \mathrm{Var}[\bar{R}_{\mathrm{ctx}}(q)] + \mathrm{Var}[M_i] + 2\mathrm{Cov}[\bar{R}_{\mathrm{ctx}}(q), M_i]$$

通过同行比较，任务上下文波动（$\mathrm{Var}[\bar{R}_{\mathrm{ctx}}(q)]$）不再污染架构质量的估计。

### 2. 执行协议：从单次执行到多试验综合

现有方法对每个候选架构仅执行一次评估，将执行随机性误认为能力差异。RAAS通过**多试验评估综合（MTAS）**将执行协议改为每个架构执行 $K$ 次独立试验，然后通过统计合成函数 $\Phi$（如裁剪均值）聚合：

$$\hat{R}(\mathcal{G}_i, q) = \Phi\left(\{R^{(k)}(\mathcal{G}_i, q)\}_{k=1}^{K}\right)$$

这一设计提供了统计上稳健的能力估计，消除了单次执行中的瞬态伪影。

### 3. 优化信号：从原始得分到优点加权适应

传统方法直接用原始性能得分更新架构分布。RAAS将CAO产生的上下文优点与MTAS的稳健估计结合，形成**优点加权适应（Merit-Weighted Adaptation）**：

$$\Delta_{\phi}(\mathcal{G}_i; q) = \omega_i(\phi) \cdot M_{\mathrm{ctx}}(\mathcal{G}_i, q)$$

其中**影响权重** $\omega_i(\phi) = \nabla_{\phi} \log p(\mathcal{G}_i; \phi)$ 将上下文优点精确归因到超级网中的具体算子，实现组件级别的细粒度优化。最终的GRPO风格梯度估计器为：

$$\Theta_{\mathrm{RAAS}}(\phi; q) = \frac{1}{N} \sum_{i=1}^{N} \nabla_{\phi} \log p(\mathcal{G}_i; \phi) \cdot M_{\mathrm{ctx}}(\mathcal{G}_i, q)$$

### 协同效应的实证验证

消融实验（Figure 5）清晰展示了两个机制的协同贡献：
- **仅用CAO（禁用MTAS）**：重新引入执行波动，最终准确率下降。
- **移除CAO（仅用MTAS或类似）**：性能降至接近MaAS基线水平，表明仅靠多次执行无法消除任务难度偏差。
- **完整RAAS（CAO + MTAS）**：在所有基准上取得最佳结果，验证了两个模块的互补性——CAO提供任务难度的解耦，MTAS提供执行方差的消除，二者共同构成稳定评估信号的充分条件。

这一评估范式的转变是RAAS在六个基准上平均超越最强基线**+5.41个百分点**的根本原因。



RAAS（Robust Architecture Adaptive Search）构建了一个闭环的架构搜索pipeline，核心目标是**在概率化超级网上通过稳定、公平的评估信号来发现高性能智能体架构**。整个框架由四个协同模块串联而成，形成“采样→评估→适应”的迭代优化循环。

### 1. 搜索空间定义：Agentic Supernet

pipeline的起点是将搜索空间形式化为一个概率性超级网（Agentic Supernet）。该超级网由 $L$ 层组成，每层包含一组候选算子 $\mathbb{O}$ 及其对应的概率分布：

$$\mathcal{A} = \left\{ \{\pi_l(\mathcal{O})\}_{\mathcal{O} \in \mathbb{O}} \right\}_{l=1}^{L}$$

每个具体的架构 $\mathcal{G}$ 通过从各层概率分布中采样激活算子来生成，其联合概率为：

$$p(\mathcal{G}) = \prod_{l=1}^{L} \prod_{\mathcal{O} \in \mathbb{O}} \pi_l(\mathcal{O})^{\mathbb{I}_{\mathcal{O} \in \nu_l}}$$

其中 $\nu_l$ 表示第 $l$ 层中被激活的算子集合。这一设计将离散的架构选择转化为可微的概率优化问题，为后续基于梯度的搜索提供了基础。

### 2. 评估信号生成：CAO + MTAS 协同机制

RAAS的核心创新在于**用两个协同机制替换传统方法中不可靠的绝对评分**，从根本上解决评估不稳定性问题。这两个模块构成pipeline中承上启下的关键环节：

- **Contextual Architecture Orchestration (CAO)**：在同一查询 $q$ 上评估 $N$ 个候选架构的同行群体，计算上下文基线 $\bar{R}_{\mathrm{ctx}}(q)$，进而推导出每个架构的上下文优点（Contextual Merit）$M_{\mathrm{ctx}}(\mathcal{G}_i, q) = \hat{R}(\mathcal{G}_i, q) - \bar{R}_{\mathrm{ctx}}(q)$。这一操作将任务难度与架构质量解耦——无论查询难易，优点信号只反映架构相对于同行的真实能力偏差。

- **Multi-Trial Assessment Synthesis (MTAS)**：对每个架构执行 $K$ 次独立试验，通过统计合成函数 $\Phi$（如裁剪均值）聚合结果：$\hat{R}(\mathcal{G}_i, q) = \Phi(\{R^{(k)}(\mathcal{G}_i, q)\}_{k=1}^{K})$。这消除了单次执行的随机波动，提供统计上稳健的能力估计。

两个模块的协同关系体现在：CAO依赖MTAS提供的稳定个体估计来构建可靠的同行基线；MTAS的多试验成本则因CAO的同行比较设计而获得更高的信号效率。消融实验（Figure 5）证实，移除任一模块都会导致性能显著下降，二者组合在所有基准上取得最佳结果。

### 3. 架构分布更新：Merit-Weighted Adaptation

pipeline的最后一环是将评估信号转化为超级网参数的更新。RAAS采用基于上下文优点的加权适应策略：

$$\Theta_{\mathrm{RAAS}}(\phi; q) = \frac{1}{N} \sum_{i=1}^{N} \nabla_{\phi} \log p(\mathcal{G}_i; \phi) \cdot M_{\mathrm{ctx}}(\mathcal{G}_i, q)$$

其中影响权重 $\omega_i(\phi) = \nabla_{\phi} \log p(\mathcal{G}_i; \phi)$ 将架构级的优点信号精确追溯到具体的算子组件，实现细粒度的概率分布调整。超级网参数按 $\phi \leftarrow \phi + \eta \cdot \Theta_{\mathrm{RAAS}}(\phi; q)$ 迭代更新。

### 4. 输入输出流与迭代闭环

整个pipeline的数据流如下：

1. **输入**：查询 $q$ 从任务分布 $\mathcal{D}$ 中采样。
2. **采样阶段**：从当前超级网 $\mathcal{A}(\phi)$ 中采样 $N$ 个候选架构 $\{\mathcal{G}_i\}_{i=1}^{N}$。
3. **评估阶段**：CAO组织 $N$ 个架构在 $q$ 上的同行比较，MTAS对每个架构执行 $K$ 次试验并合成能力估计，输出上下文优点信号 $\{M_{\mathrm{ctx}}(\mathcal{G}_i, q)\}$。
4. **适应阶段**：Merit-Weighted Adaptation根据优点信号更新超级网参数 $\phi$。
5. **循环**：更新后的超级网用于下一轮查询的架构采样，形成迭代优化闭环。

这一设计使得RAAS在搜索过程中持续受益于稳定的评估信号，收敛曲线（Figure 3）显示其相比基线方法更快、更稳定地达到高性能区域。超参数 $N$ 和 $K$ 的敏感性分析（Figure 4）表明，在适中的设置下（如 $N=5, K=5$），RAAS即可在成本可控的前提下获得显著性能增益。

### 补充图表

![[assets/figures/papers/paper_list_l2199_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_RAAS_LLM_Agentic/figures/002_Figure_2.jpg]]
*Figure 2: RAAS framework overview. CAO performs cohort-based peer comparison for contextual fairness, while MTAS aggregates multi-trial executions for statistical robustness, together producing stable evaluation signals for architecture discovery*



RAAS 通过两个协同机制建立稳定、公平的评估信号：**上下文架构编排（CAO）** 和 **多试验评估综合（MTAS）**。CAO 在同查询上评估候选架构的同行群体，通过同行比较推导上下文相关的零中心优势信号，解耦任务难度；MTAS 聚合多次独立试验的结果，减少执行方差，提供统计上稳健的能力估计。两者协同产生稳定的评估信号，驱动架构搜索的优化过程。

### 智能体超级网（Agentic Supernet）

搜索空间被形式化为一个概率性超级网，包含 $L$ 层，每层定义在算子集合 $\mathbb{O}$ 上的概率分布：

$$
\mathcal{A} = \left\{ \{\pi_l(\mathcal{O})\}_{\mathcal{O} \in \mathbb{O}} \right\}_{l=1}^{L}
$$

其中 $\pi_l(\mathcal{O})$ 表示第 $l$ 层选择算子 $\mathcal{O}$ 的概率。给定激活的算子集 $\nu_l$，一个具体架构 $\mathcal{G}$ 的联合概率为：

$$
p(\mathcal{G}) = \prod_{l=1}^{L} \prod_{\mathcal{O} \in \mathbb{O}} \pi_l(\mathcal{O})^{\mathbb{I}_{\mathcal{O} \in \nu_l}}
$$

优化目标是在成本约束下最大化预期效用：

$$
\max \mathbb{E}_{\mathcal{D}}[U_\lambda(\mathcal{G}; q)] \quad \mathrm{s.t.} \ \mathcal{G} \subset \mathcal{A}
$$

### 上下文架构编排（CAO）

CAO 的核心思想是通过同行比较消除任务难度偏差。对于查询 $q$，采样 $N$ 个候选架构组成同行群体，计算上下文基线——同查询下同行群体的平均能力：

$$
\bar{R}_{\mathrm{ctx}}(q) = \frac{1}{N} \sum_{i=1}^{N} \hat{R}(\mathcal{G}_i, q)
$$

能力方差被分解为任务上下文波动、架构质量变化和协方差三部分：

$$
\mathrm{Var}[\hat{R}_i] = \mathrm{Var}[\bar{R}_{\mathrm{ctx}}(q)] + \mathrm{Var}[M_i] + 2\mathrm{Cov}[\bar{R}_{\mathrm{ctx}}(q), M_i]
$$

上下文优点（Contextual Merit）量化架构 $\mathcal{G}_i$ 相对于同行基线的能力偏差：

$$
M_{\mathrm{ctx}}(\mathcal{G}_i, q) = \hat{R}(\mathcal{G}_i, q) - \bar{R}_{\mathrm{ctx}}(q)
$$

该信号以零为中心：正值表示架构在给定查询上优于同行平均，负值表示劣于同行平均。由于同一查询上的任务难度被基线抵消，$M_{\mathrm{ctx}}$ 主要反映架构的内在质量差异，而非查询的外部难度。

### 多试验评估综合（MTAS）

MTAS 通过多次独立试验消除执行随机性。对于每个架构-查询对，执行 $K$ 次独立试验，通过统计合成函数 $\Phi$（如裁剪均值）聚合能力估计：

$$
\hat{R}(\mathcal{G}_i, q) = \Phi\left(\{R^{(k)}(\mathcal{G}_i, q)\}_{k=1}^{K}\right)
$$

多次试验的聚合有效降低了单次执行的方差，使能力估计更接近架构的真实期望表现。

### 优点加权适应（Merit-Weighted Adaptation）

基于上下文优点信号，RAAS 通过影响权重将优点归因到具体算子，实现组件级别的细粒度更新。影响权重量化每个组件对架构概率的贡献：

$$
\omega_i(\phi) = \nabla_\phi \log p(\mathcal{G}_i; \phi) = \sum_{l=1}^{L} \sum_{\mathcal{O} \in \mathcal{V}_{i,l}} \nabla_\phi \log \pi_l(\mathcal{O})
$$

参数更新量为影响权重与上下文优点的乘积：

$$
\Delta_\phi(\mathcal{G}_i; q) = \omega_i(\phi) \cdot M_{\mathrm{ctx}}(\mathcal{G}_i, q)
$$

最终，RAAS 使用 GRPO 风格的梯度估计器更新超级网参数 $\phi$：

$$
\Theta_{\mathrm{RAAS}}(\phi; q) = \frac{1}{N} \sum_{i=1}^{N} \nabla_\phi \log p(\mathcal{G}_i; \phi) \cdot M_{\mathrm{ctx}}(\mathcal{G}_i, q)
$$

迭代更新规则为：

$$
\phi \leftarrow \phi + \eta \cdot \Theta_{\mathrm{RAAS}}(\phi; q)
$$

其中 $\eta$ 为适应率。上下文归一化使适应信号比原始性能分数更一致——任务特定难度不再在学习过程中引入虚假波动，组件级归因则使架构模式的优化精确到单个算子层面。

### 补充图表

![[assets/figures/papers/paper_list_l2199_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_RAAS_LLM_Agentic/figures/001_Figure_1.jpg]]
*Figure 1: An illustration of the core problem and our proposed solution. (A) Problem: Evaluation Instabilities. Easy queries inflate weak architectures while hard queries depress strong ones (task-difficulty entanglement), and single-execution assessments capture transient artifacts rather than true capability (execution variance). (B) RAAS: Stable Evaluation through Synergistic Design. RAAS evaluates cohorts of architectures on the same query through multiple independent trials. CAO derives contextual merit signals via peer comparison, while MTAS synthesizes multi-trial outcomes for statistical robustness, together enabling more reliable architecture discovery*



## 实验与关键发现

### 核心瓶颈：评估不稳定性如何阻碍架构搜索

在深入实验结果之前，必须先理解RAAS所要解决的根本问题：**评估不稳定性**。现有的智能体架构搜索方法（如MaAS、ADAS、AgentSquare等）在评估候选架构时面临两个相互交织的偏差源：

1. **任务难度纠缠**：绝对性能分数将架构的内在质量与查询的外部难度混淆。一个弱架构在简单查询上可能表现出色，而一个强架构在困难查询上可能表现平庸，导致搜索信号被任务难度噪声淹没。

2. **执行方差**：单次执行协议捕获的是LLM采样的随机性而非架构的真实能力。同一架构在同一查询上的多次执行结果可能剧烈波动，使得单次评估无法可靠反映架构价值。

RAAS通过两个协同机制解决这一问题：**上下文架构编排（CAO）** 在同查询上比较候选架构的同行群体，推导出上下文相关的零中心优势信号，解耦任务难度；**多试验评估综合（MTAS）** 聚合多次独立试验的结果，消除执行随机性。以下实验系统性地验证了这一设计的有效性。

### 主要结果：跨基准一致且显著的性能提升

**Table 1** 展示了RAAS与多个强基线方法在数学推理和代码生成基准上的全面对比。RAAS在GPT-4o-mini骨干上取得了**76.55%的平均准确率**，在Qwen-2.5-72b骨干上取得了**76.05%的平均准确率**，均排名第一。

具体而言，在GPT-4o-mini骨干上，RAAS相对于最强基线的提升幅度为：
- **MATH**：60.87%（+8.79个百分点）——数学推理能力的大幅跃升表明CAO的同行比较机制在困难任务上尤为有效，因为困难查询对弱架构的惩罚和强架构的奖励在绝对分数中被压缩，而上下文优点信号能够放大这一差异。
- **GSM8K**：95.16%（+3.32个百分点）——在已接近饱和的基准上仍取得显著提升。
- **HumanEval**：96.31%（+4.08个百分点，pass@1）——代码生成能力接近极限水平。
- **MBPP**：84.18%（+5.47个百分点）——在代码基准上的一致提升验证了方法的跨任务泛化性。
- **GAIA**：20.84%（+2.78个百分点）——**Table 2**进一步按难度级别分解了GAIA结果，RAAS在Level 1上达到29.53%，在所有难度级别上均优于MaAS基线。

![[assets/figures/papers/paper_list_l2199_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_RAAS_LLM_Agentic/figures/004_Table_2.jpg]]
*Table 2: GAIA benchmark results. Accuracy (%) across difficulty levels. Best and second-best results are bold and underlined*

平均而言，RAAS在五个基准上**超越最强基线+5.41**。这一提升幅度的一致性（所有基准均为正向提升，无负面回归）是评估稳定性设计的直接证据：当搜索信号不再被任务难度和执行噪声污染时，优化过程能够可靠地发现更优架构。

### 收敛性分析：更快、更稳定的优化过程

**Figure 3** 展示了RAAS与基线方法在四个基准上的收敛曲线对比。RAAS（红色曲线）表现出两个显著优势：

1. **更快的收敛速度**：RAAS在更少的优化步数内达到更高的性能水平，表明CAO提供的上下文优点信号比原始绝对分数具有更高的信噪比，加速了超级网参数向高质量架构分布的收敛。

2. **更稳定的收敛过程**：基线方法的收敛曲线呈现明显的振荡，而RAAS的曲线更加平滑。这直接归因于MTAS通过多次试验聚合消除了单次执行的随机波动，使得梯度估计更加稳定。

### 消融实验：CAO与MTAS的协同贡献

**Figure 5** 的消融实验系统性地分解了RAAS各组件的贡献，通过比较四种配置：

1. **MaAS基线**：使用单次绝对评估的原始架构搜索。
2. **MaAS + 熵正则化**：仅添加熵正则化以鼓励探索，但不改变评估方式。
3. **仅CAO（无MTAS）**：使用同行比较的上下文优点信号，但每个架构仅执行单次试验。
4. **完整RAAS（CAO + MTAS）**：同时使用上下文同行比较和多试验聚合。

实验结果揭示了三个关键发现：

- **移除CAO导致性能骤降至接近MaAS水平**：当仅使用MTAS的多试验聚合但保留绝对分数评估时，性能提升几乎消失。这证明任务难度解耦是评估稳定性的核心——即使消除了执行方差，只要评估信号仍与任务难度纠缠，搜索就无法有效区分架构质量。

- **禁用MTAS重新引入执行波动并降低准确率**：仅使用CAO的同行比较但保留单次执行时，性能介于MaAS和完整RAAS之间。执行方差的残留使得上下文优点信号仍含有噪声，限制了架构发现的精度。

- **完整RAAS在所有基准上取得最佳结果**：CAO和MTAS的组合产生了**协同效应**——同行比较提供了零中心的相对信号，而多试验聚合确保了该信号的统计可靠性。两者缺一不可。

### 超参数敏感性：同队列规模N与试验次数K

**Figure 4** 的热力图展示了同队列规模N（每个查询采样的架构数）和试验次数K（每个架构的独立执行次数）对MATH准确率的影响。关键观察：

- **N和K的适度取值即可实现稳定性能**：在N=5、K=5的设置下（每查询25次运行），RAAS已达到具有竞争力的准确率，且每查询成本仅$0.31，比MaAS低约6%。
- **增大N的边际收益递减**：当N从3增加到5时性能提升明显，但从5增加到7时提升趋于平缓，表明5个同行架构已足以构建可靠的上下文基线。
- **K的增大持续改善稳定性**：增加试验次数持续降低执行方差，但成本线性增长。这一权衡为实际部署中的成本控制提供了调节空间。

### 成本-性能权衡分析

**Figure 6** 展示了不同方法在成本与性能之间的帕累托边界。RAAS在给定成本预算下一致取得更高的准确率，验证了评估稳定性带来的搜索效率提升——更可靠的评估信号意味着每次查询的评估资源被更有效地利用于区分架构质量，而非浪费在噪声上。

### 失败模式与局限性

尽管RAAS在多个基准上表现优异，但以下局限性需要在解读结果时加以注意：

1. **单轮任务聚焦**：当前实验覆盖数学推理（MATH、GSM8K）和代码生成（HumanEval、MBPP）等单轮任务。在多轮交互式场景（如工具使用、对话式问题解决）中，评估不稳定性的表现可能更为复杂，RAAS的有效性有待验证。

2. **超参数固定**：同队列规模N和试验次数K在所有任务上使用统一设置，但不同任务的难度方差和执行随机性程度不同，自适应分配N和K可能进一步提升成本效益。

3. **理论收敛性缺失**：优点加权适应的收敛性缺乏理论保证，当前仅通过实验观察验证了其稳定性。

4. **骨干模型泛化**：评估限于GPT-4o-mini和Qwen-2.5-72b两个骨干，RAAS在其他模型家族（如Claude、Gemini）上的表现需要进一步验证，特别是考虑到不同模型的采样温度特性可能影响执行方差的量级。

### 补充图表

![[assets/figures/papers/paper_list_l2199_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_RAAS_LLM_Agentic/figures/003_Table_1.jpg]]
*Table 1: Main results across agentic systems. Accuracy (%) on various benchmarks. Best and second-best results are bold and underlined*

![[assets/figures/papers/paper_list_l2199_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_RAAS_LLM_Agentic/figures/005_Figure_3.jpg]]
*Figure 3: Convergence comparison across benchmarks. RAAS demonstrates faster and more stable convergence compared to baseline methods across all four evaluation domains. The red line (RAAS) consistently reaches higher performance levels with fewer optimization steps, while maintaining smoother search trajectories with reduced performance fluctuation (shown by confidence bands)*

![[assets/figures/papers/paper_list_l2199_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_RAAS_LLM_Agentic/figures/006_Figure_4.jpg]]
*Figure 4: Impact of cohort size N and trial count K on MATH accuracy. The heatmap shows accuracy (in %) as a function of the number of architectures sampled per query (N) and independent executions per architecture (K)*

![[assets/figures/papers/paper_list_l2199_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_RAAS_LLM_Agentic/figures/007_Figure_5.jpg]]
*Figure 5: Ablation study of RAAS components. We systematically analyze the contribution of CAO and MTAS modules by comparing: (1) MaAS baseline, (2) MaAS with entropy regularization only, (3) RAAS with CAO only (no MTAS multi-trial synthesis), and (4) full RAAS (CAO + MTAS). The results demonstrate that both contextual orchestration and multi-trial synthesis contribute synergistically to performance gains, with their combination achieving the best results across all benchmarks*

![[assets/figures/papers/paper_list_l2199_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_RAAS_LLM_Agentic/figures/008_Figure_6.jpg]]
*Figure 6: Cost-performance trade-off analysis across different methods*



## 定位与知识库关联

### 智能体架构搜索的演进脉络

RAAS 所处的智能体架构搜索（Agentic Architecture Search）领域，其核心目标是在预定义的算子空间内自动发现最优的智能体系统拓扑。这一方向与传统的神经架构搜索（NAS）共享形式化框架——将搜索空间建模为概率性超级网（Supernet），但面临截然不同的评估挑战：NAS 依赖确定性的验证集精度，而智能体架构的评估信号天然受制于查询难度混淆和执行随机性。

RAAS 的直接前驱是 **MaAS**（Zhang et al., 2025），后者首次将 Agentic Supernet 引入智能体系统搜索，但沿用了传统的单次绝对评估协议。MaAS 的瓶颈在于：绝对性能分数将架构的内在质量与查询的外部难度纠缠在一起，导致弱架构在简单查询上看似强大；同时，单次执行捕获的是瞬态伪影而非真实能力。RAAS 的贡献正是在这一瓶颈上做了外科手术式的改进——保留 Supernet 框架，但从根本上重构了评估信号。

其他并行工作从不同角度探索了智能体系统的自动设计。**ADAS**（Hu et al., 2025）构建了自动智能体系统设计的基准框架，侧重于统一评估协议而非搜索算法本身。**AgentSquare**（Shang et al., 2025）在模块化设计空间内进行自动搜索，但其评估机制同样未系统性地解决任务难度混淆问题。**AFlow**（Zhang et al., 2025）聚焦于工作流的自动生成，侧重于拓扑结构而非算子选择。**DyLAN**（Liu et al., 2024）探索了动态智能体网络协作，关注运行时自适应而非离线架构优化。这些工作的共同局限在于：评估信号的不稳定性未被作为核心问题来建模和解决。

### RAAS 的创新定位

RAAS 的方法论贡献可以精确地定位为 **评估协议的范式转换**，而非搜索算法或搜索空间的创新。具体而言，RAAS 在三个关键槽位上做出了改变：

1. **评估信号类型**：从单架构绝对评分转向同查询同行比较的上下文优点（Contextual Merit）。这一转变的核心机制是方差分解——将原始能力方差 $\mathrm{Var}[\hat{R}_i]$ 分解为任务上下文波动 $\mathrm{Var}[\bar{R}_{\mathrm{ctx}}(q)]$、架构质量变化 $\mathrm{Var}[M_i]$ 和协方差项。通过在同查询上构建同行基线 $\bar{R}_{\mathrm{ctx}}(q)$，CAO 将任务难度的影响从优化信号中解耦出来。

2. **执行协议**：从单次执行转向 $K$ 次独立试验的统计综合。MTAS 通过合成函数 $\Phi$（如裁剪均值）聚合多次试验结果，有效抑制了 LLM 推理的固有随机性对评估的干扰。

3. **优化信号**：从原始性能得分转向基于上下文优点的加权适应。优点加权适应 $\Delta_{\phi}(\mathcal{G}_i; q) = \omega_i(\phi) \cdot M_{\mathrm{ctx}}(\mathcal{G}_i, q)$ 将上下文优点与组件级影响权重耦合，实现了对具体算子的细粒度归因。

值得注意的是，RAAS 的优化器本身采用了 GRPO（Group Relative Policy Optimization）风格的梯度估计器，这与近期大语言模型对齐领域的方法形成呼应，但在智能体架构搜索的语境下是首次应用。

### 适用边界与局限

当前 RAAS 的验证范围存在明确的边界条件，这些边界定义了其知识贡献的适用范围：

**任务域边界**：实验覆盖的基准（MATH、GSM8K、HumanEval、MBPP、GAIA）均为单轮推理任务——数学问题求解和代码生成。在多轮交互式场景（如对话式智能体、工具使用链）中，评估信号的不稳定性可能有不同的表现形式（如对话状态漂移、工具调用失败的模式），RAAS 的 CAO+MTAS 机制是否同样有效尚待验证。

**骨干模型边界**：实验仅在 GPT-4o-mini 和 Qwen-2.5-72b 两个骨干上进行了验证。不同能力层级的模型可能对评估稳定性有不同敏感度——弱模型可能受益于更激进的方差抑制，而强模型可能因过度聚合而损失细粒度区分能力。

**超参数敏感性**：同队列规模 $N$ 和试验次数 $K$ 在实验中采用固定设置（$N=5, K=5$）。Figure 4 的热力图虽然展示了参数空间内的性能分布，但并未提出自适应调整策略。在计算预算受限或查询难度差异极大的场景中，固定参数可能导致效率损失。

**理论保证缺失**：优点加权适应的收敛性目前仅有经验证据支持（Figure 3 的收敛曲线），缺乏理论上的收敛速率或 regret bound 分析。这使得 RAAS 在最坏情况下的行为不可预测。

### 开放问题与后续方向

基于上述边界分析，以下几个方向构成了 RAAS 知识谱系的自然延伸：

- **多轮交互扩展**：将 CAO 的同行比较机制推广到多轮对话场景，需要重新定义“同查询”概念——对话的动态性使得严格的任务等价性难以保证，可能需要引入轨迹对齐或子任务分解策略。

- **自适应资源分配**：开发根据查询难度或搜索阶段动态调整 $N$ 和 $K$ 的策略，以优化成本-效益的帕累托边界。Figure 6 的成本-性能分析为此提供了实证基础，但尚未转化为算法机制。

- **理论收敛分析**：将优点加权适应纳入随机优化的理论框架，分析其在非凸 Supernet 参数空间中的收敛性质，特别是上下文优点信号的方差如何影响收敛速率。

- **跨模型与跨域泛化**：在更多样的 LLM 骨干和任务域（如开放域问答、代码调试、多模态推理）上验证评估稳定机制的普适性，识别可能失效的边界条件。



## 原文 PDF

![[paperPDFs/CVPR_2026/RAAS_LLM_Agentic_System_Architecture_Search_with_GRPO.pdf]]
