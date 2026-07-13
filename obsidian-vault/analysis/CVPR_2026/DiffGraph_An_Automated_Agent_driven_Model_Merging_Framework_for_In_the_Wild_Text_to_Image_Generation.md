---
title: "DiffGraph: An Automated Agent-driven Model Merging Framework for In-the-Wild Text-to-Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DiffGraph_An_Automated_Agent_driven_Model_Merging_Framework_for_In_the_Wild_Text_to_Image_Generation.pdf
project_link: "https://zhuoling.site/DiffGraph"
code_link: null
aliases:
- DiffGraph
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将专家能力建模为图结构中的节点与边特征，通过图变分自编码器（VGAE）依据动态子图的上下文信息生成融合系数，实现由用户需求驱动的自适应专家选择与融合。
primary_logic: 将模型融合重新定义为图上的动态子图激活问题：构建包含专家能力描述的通用图，利用LLM代理解析用户意图并激活相关子图，VGAE从子图上下文生成融合方案，无需重新训练或测试时优化即可灵活组合任意数量和类型的在线专家。
claims:
- DiffGraph在DABench和DiffusionDB基准上全面超越所有对比方法，在SD1.5上IR达到73.11，比最佳基线显著提升
- 去除节点校准机制导致IR骤降至11.92，证明图结构中的量化能力表征至关重要
- 去除专家选择代理（ESA）或使用随机激活均导致生成质量严重下降，验证了动态子图选择的必要性
- DABench 上 IR / HPS / AS / PS / CS = 73.11 / 30.06 / 6.54 / 20.62 / 84.79 (SD1.5)
---

# DiffGraph: An Automated Agent-driven Model Merging Framework for In-the-Wild Text-to-Image Generation

> [!tip] 核心洞察
> 将模型融合重新定义为图上的动态子图激活问题：构建包含专家能力描述的通用图，利用LLM代理解析用户意图并激活相关子图，VGAE从子图上下文生成融合方案，无需重新训练或测试时优化即可灵活组合任意数量和类型的在线专家。

| 字段 | 内容 |
|------|------|
| 中文题名 | DiffGraph：面向开放领域文本到图像生成的自动化智能体驱动模型融合框架 |
| 英文题名 | DiffGraph: An Automated Agent-driven Model Merging Framework for In-the-Wild Text-to-Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.20470) · [Project](https://zhuoling.site/DiffGraph) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DiffGraph |
| Dataset | DABench, DiffusionDB |

> [!tip] 效果简介
> - DABench 上，IR / HPS / AS / PS / CS 73.11 / 30.06 / 6.54 / 20.62 / 84.79 (SD1.5) vs 所有基线方法（DiffAgent, K-LoRA 等）均显著低于本方法 (大幅领先)。
> - DiffusionDB 上，IR / HPS / AS / PS / CS 136.62 / 32.72 / 6.56 / 21.25 / 85.02 (FLUX) vs 所有基线方法均显著低于本方法 (大幅领先)。

## 概要

**核心问题：** 开放领域文本到图像（T2I）生成面临用户需求高度多样且持续演化的挑战，而现有模型融合方法难以充分利用大规模在线专家资源——参数依赖的融合方式（如K-LoRA、LoRA.rar、AutoLoRA等）无法泛化至异构、多样且动态增长的专家模型，固定小规模专家集合或手动选择机制更无法灵活应对“in-the-wild”场景下用户的多变需求。

**核心方法：** DiffGraph 将模型融合重新定义为**图上的动态子图激活问题**。框架包含三个关键组件：
- **图构建代理（GCA）**：自动收集在线专家，通过节点注册与节点校准机制构建可扩展的通用图，以图结构中的节点与边特征量化表征专家能力；
- **专家选择代理（ESA）**：基于LLM自动解析用户意图，分解为视觉属性并自适应检索、过滤合适的CKPT与PEFT专家；
- **融合规划器（MP）**：利用图变分自编码器（VGAE）依据动态激活子图的上下文信息生成融合系数，实现由用户需求驱动的自适应专家组合，无需重新训练或测试时优化即可灵活组合任意数量和类型的在线专家。

**核心结论：** DiffGraph 在 DABench 和 DiffusionDB 两个基准上全面超越所有对比方法——在 SD1.5 上 Image Reward (IR) 达到 73.11，相比最佳基线取得显著提升；在 FLUX 上 IR 达 136.62，验证了跨基座模型的泛化能力。消融实验表明，去除节点校准机制导致 IR 骤降至 11.92，移除 ESA 或随机激活子图分别使 IR 降至 16.12 和 15.36，有力证明了图结构中的量化能力表征与动态子图选择机制的核心作用。此外，DiffGraph 在增量专家场景下（2023→2025）表现接近完整框架，展现出对动态演化专家生态的良好扩展性。

**方法定位：** DiffGraph 属于**智能体驱动的图结构模型融合**范式，区别于传统的参数依赖融合（K-LoRA, LoRA.rar, AutoLoRA）、多概念定制融合（Mix-of-Show, ZipLoRA）以及基于优化的融合方法（Model Swarms, Diffusion Soup）。其核心创新在于将专家管理与融合决策从参数空间解耦至图结构空间，通过 LLM 代理与 VGAE 的协同实现开放场景下的自适应融合。



文本到图像（T2I）生成领域近年来取得了显著进展，以Stable Diffusion、FLUX等为代表的基础模型展现出了强大的通用生成能力。然而，开放域用户需求高度多样化且持续演化，单一基础模型难以覆盖所有视觉概念、艺术风格和细粒度属性组合。为弥补这一缺口，研究社区和开源平台（如HuggingFace、CivitAI）涌现出海量专家模型——包括完整微调检查点（CKPT）和参数高效微调模块（PEFT，如LoRA），它们各自精于特定概念、风格或属性。如何有效利用这些大规模、异构、持续增长的在线专家资源，成为开放域T2I生成的核心瓶颈。

现有模型融合方法主要沿两条技术路线展开。一类方法依赖参数空间操作，如**Mix-of-Show**（Gu et al., NeurIPS 2023）、**ZipLoRA**（Shah et al., ECCV 2024）、**K-LoRA**（Ouyang et al., CVPR 2025）和**LoRA.rar**（Shenaj et al., ICCV 2025），它们通过对模型权重进行算术组合或训练超网络来生成融合权重。这类方法的根本局限在于：融合系数与专家模型参数强绑定，当专家模型来自不同架构、不同微调策略或不同基础模型时，参数空间的线性组合缺乏泛化保证。另一类方法采用优化驱动的融合策略，如**Model Swarms**（Feng et al., ICML 2025）利用粒子群优化搜索最优组合权重，**Diffusion Soup**（Biggs et al., ECCV 2024）采用贪心算法逐步筛选专家。这些方法虽不直接依赖参数结构，但需要在测试时对每个新需求执行优化过程，计算开销随专家池规模线性增长，无法满足实时交互场景的延迟要求。此外，**DiffAgent**（Zhao et al., CVPR 2024）等单专家选择方法仅能激活单一专家，无法组合多个专家的互补能力。

上述方法的共同缺口在于：**它们均无法充分利用大规模在线专家资源**。参数依赖方法只能处理固定的小规模专家集合，优化驱动方法则因计算成本而难以扩展至数百甚至数千个在线专家。当新专家持续涌现时，现有方法要么需要重新训练融合模型，要么需要重新执行优化过程，缺乏对动态演化专家生态的适应能力。更关键的是，这些方法缺乏对专家能力的语义理解——它们仅依赖参数相似性或生成质量分数来决策，无法根据用户需求的语义内容自主判断哪些专家真正相关、如何组合才能最大化需求满足度。

DiffGraph的核心动机正是弥合这一缺口：**将模型融合重新定义为图上的动态子图激活问题**。通过构建包含专家能力描述的通用图结构，并利用大语言模型（LLM）代理解析用户意图、激活相关子图，再以图变分自编码器（VGAE）从子图上下文生成融合方案，DiffGraph实现了无需重新训练或测试时优化的自适应专家组合。这一思路从根本上解耦了专家管理与融合决策，使得框架能够灵活组合任意数量和类型的在线专家，并支持新专家的即插即用集成。



## 核心方法与创新机理

DiffGraph的核心创新在于将**模型融合重新定义为图上的动态子图激活问题**，从而突破现有方法对固定专家集合和参数空间依赖的根本限制。这一范式转换通过三个关键机制实现，形成了“构建—选择—融合”的闭环。

**1. 从参数空间到图空间的表征转换**

现有融合方法（如**K-LoRA**（Ouyang et al., CVPR 2025）、**LoRA.rar**（Shenaj et al., ICCV 2025）、**AutoLoRA**（Li et al., arXiv 2025））直接在参数矩阵层面操作，依赖权重插值或超网络生成融合系数。这种方式隐含假设专家模型处于同一参数空间，无法泛化至异构、多样且持续演化的在线专家生态。DiffGraph将专家能力抽象为图结构中的**节点特征**（由MLLM生成的能力描述文本嵌入）与**边特征**（通过节点校准机制量化的专家对参考提示的响应质量），使融合决策完全脱离参数依赖。

**2. 用户需求驱动的自适应专家选择**

传统方法通常需要手动指定参与融合的专家或基于参数相似度固定选择数量（如**Mix-of-Show**（Gu et al., NeurIPS 2023）针对特定概念组合、**ZipLoRA**（Shah et al., ECCV 2024）针对风格与主体配对）。DiffGraph的**专家选择代理（ESA）**利用LLM将用户提示自动解析为视觉属性摘要，在通用图中检索并过滤相关专家，且参与融合的CKPT与PEFT专家数量由LLM自适应决定，无需人工干预。消融实验验证了这一机制的关键性：移除ESA后IR从73.11骤降至16.12，随机激活子图更降至15.36（Table 4），证明智能选择而非盲目组合是性能的核心保障。

**3. 上下文感知的融合系数生成**

融合系数的生成方式是最关键的changed slot。现有方法或使用固定权重、或基于参数相似度计算、或由超网络从参数中预测，均未利用专家间的能力互补关系。DiffGraph的**融合规划器（MP）**以ESA选定的专家节点及其一阶邻居构建动态子图，通过**图变分自编码器（VGAE）**编码子图的上下文信息，生成每个专家针对当前用户需求的融合权重。VGAE将权重建模为Beta分布（通过$\alpha_i = 1 + e^{a_i}, \beta_i = 1 + e^{b_i}$保证单模态），测试时以期望值$w_i = \frac{\alpha_i}{\alpha_i + \beta_i}$作为确定性系数。消融实验显示，随机融合甚至导致负IR（-5.27），而VGAE方案达到73.11（Table 5），证实上下文感知融合的不可替代性。

**4. 可扩展的增量专家管理**

DiffGraph的**图构建代理（GCA）**通过节点注册和节点校准机制，支持以无训练方式动态添加新专家。节点校准将专家在各参考提示上的生成质量量化为边特征，使图结构持续反映专家的真实能力。在增量实验中，仅使用2023年数据训练、逐步添加至2025年专家的设置下，IR达到69.64，接近完整2025年设置的73.11，且超越所有在2025年设置下训练的方法（Table 2）。去除校准机制后IR暴跌至11.92（Table 3），证明图结构中的量化能力表征是支撑可扩展性的核心支柱。

综上，DiffGraph的三重changed slots——**图空间专家管理、LLM驱动自适应选择、VGAE上下文感知融合**——构成了一条完整的因果链：通用图提供可扩展的能力表征基础，ESA确保相关专家被激活，VGAE从子图上下文生成最优融合方案。这一设计使得DiffGraph无需重新训练或测试时优化，即可灵活组合任意数量和类型的在线专家，应对开放域用户的多样化需求。



DiffGraph 提出了一种**两阶段、三模块**的智能体驱动模型融合管线，将开放域文本到图像生成中的模型融合问题重新定义为**图上的动态子图激活问题**。如图1所示，整个框架由三个核心组件构成：**图构建智能体（Graph Construction Agent, GCA）**、**专家选择智能体（Expert Selection Agent, ESA）** 和**融合规划器（Merging Planner, MP）**，它们协同完成从大规模在线专家资源的组织到用户需求驱动的自适应融合的全流程。

### 第一阶段：通用图构建

在第一阶段，GCA 负责将分散的在线专家资源组织为一个可扩展的**通用图（universal graph）**。具体而言，GCA 自动从公开平台爬取高质量的 CKPT 和 PEFT（如 LoRA）专家模型，并通过两个互补机制将其纳入图结构：

- **节点注册（Node Registration）**：对每个新专家，GCA 调用 MLLM（如 GPT-4o）生成其能力的简洁文本描述，再通过文本嵌入模型将该描述编码为节点特征，从而以无训练的方式将专家初始化为图中的孤立节点。
- **节点校准（Node Calibration）**：为量化专家在具体任务上的表现，GCA 在一组参考提示 $\{r_j\}_{j=1}^{N_r}$ 上评估每个专家，将评估结果作为节点属性的补充，使图结构能够刻画专家的实际能力分布。

这一阶段产出的通用图是后续动态子图激活的基础，其关键优势在于**支持无训练地增量添加新专家**，无需重新训练或重构整个系统。

### 第二阶段：动态子图激活

在第二阶段，系统接收用户需求，由 ESA 和 MP 依次完成专家选择与融合系数生成：

1. **ESA 解析与检索**：ESA 首先利用 LLM 解析用户提示，将其分解为具体的视觉属性需求，并据此在通用图中检索和过滤合适的 CKPT 与 PEFT 专家。所选专家的数量 $N_{\mathrm{ckpt}}$ 和 $N_{\mathrm{peft}}$ 由 LLM 根据需求复杂度自动确定，无需人工指定。

2. **MP 子图激活与融合**：MP 以 ESA 选定的专家节点为中心，激活这些节点及其直接相连的一跳邻居节点，形成一个**上下文相关的子图**。随后，一个训练好的**图变分自编码器（VGAE）**对该子图进行编码，生成用户提示节点与各选定专家节点之间的边权重 $\mathbf{w} \in \mathbb{R}^{|\mathcal{V}_{\mathrm{exp}}|}$，作为最终的融合系数。

### 融合执行与输出

获得融合系数后，MP 按照以下方式合并模型参数：对于 CKPT 专家采用加权平均，对于 LoRA 专家则通过线性组合 LoRA 权重后注入基础模型。合并后的模型直接用于生成满足用户需求的图像，无需额外的测试时优化或微调。

整个管线的**因果逻辑链**可概括为：用户需求 → LLM 解析与专家检索 → 动态子图激活 → VGAE 上下文编码 → Beta 分布建模的融合系数预测 → 模型合并与图像生成。这一设计使得 DiffGraph 能够灵活组合任意数量和类型的在线专家，从根本上突破了传统参数依赖融合方法对固定专家集合的限制。

### 补充图表

![[assets/figures/papers/paper_list_l2166_https_arxiv_org_abs_2603_20470/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our proposed method. Our DiffGraph framework consists of three key components: the Graph Construction Agent (GCA), the Expert Selection Agent (ESA), and the Merging Planner (MP). In the Universal Graph Construction stage, for ease of understanding, we illustrate a simplified example in which GCA collects and organizes N = 8 online experts (indexed as 1–8), and evaluates them on Nr = 3 reference prompts for node calibration. During the Dynamic Subgraph Activation stage, ESA parses user requirements and selects a subset of experts, for example {3, 4, 5, 7}, to participate in the merging process. MP then activates the corresponding subgraph and generates the merging coefficients, w...*



DiffGraph 由三个核心模块构成：**图构建代理（GCA）**、**专家选择代理（ESA）** 和 **融合规划器（MP）**，其工作流程如图 Figure 1 所示。整体框架分为两阶段：通用图构建阶段和动态子图激活阶段。

### 3.1 图构建代理（GCA）

GCA 负责自动收集在线专家资源并构建可扩展的通用图。其核心机制包含两个互补步骤：

- **节点注册（Node Registration）**：当发现新的专家模型时，GCA 首先将其初始化为图中的孤立节点，然后利用 MLLM（如 GPT-4o）生成该专家技能的简洁文本描述，再通过文本嵌入模型将该描述编码为节点特征。
- **节点校准（Node Calibration）**：为量化专家在具体视觉属性上的能力，GCA 使用一组参考提示集 $\{r_j\}_{j=1}^{N_r}$ 对每个专家进行校准评估。评估结果作为节点与参考提示节点之间的边特征，使图结构能够表征专家的能力分布。

### 3.2 专家选择代理（ESA）

ESA 是 LLM 驱动的智能体，负责解析用户需求并自适应选择专家。其工作流程为：首先解析用户提示，生成需求摘要并分解为具体视觉属性；然后在通用图中检索与这些属性相关的 CKPT 专家和 PEFT 专家，形成候选集合 $\mathcal{M}_{\mathrm{ckpt}}$ 和 $\mathcal{M}_{\mathrm{peft}}$；最终由 LLM 自主决定参与融合的专家数量 $N_{\mathrm{ckpt}}$ 和 $N_{\mathrm{peft}}$。

### 3.3 融合规划器（MP）与 VGAE 公式推导

MP 以选定专家节点为中心激活子图，并利用变分图自编码器（VGAE）生成融合系数。

**子图激活**：MP 激活选定专家节点及其直接相连的一跳邻居节点，形成包含用户提示节点和专家节点的子图 $G$。

**融合系数生成**：VGAE 对子图 $G$ 编码得到隐变量 $\mathbf{H}$，再解码生成用户提示节点与各专家节点之间的边权重 $\mathbf{w} \in \mathbb{R}^{|\mathcal{V}_{\mathrm{exp}}|}$，作为融合系数：

$$\mathbf{w} = f(G; \theta) = Dec(\mathbf{w} \mid \mathbf{H}) \ Enc(\mathbf{H} \mid G) \tag{1}$$

**编码器因子分解**：编码器将用户提示节点和专家节点的隐变量独立建模，均值和方差由两层 GCN 生成：

$$Enc(\mathbf{H} \mid G) = \prod_{i=1}^{1+|\nu_{\mathrm{exp}}|} Enc(\mathbf{h}_i \mid G) \tag{2}$$

**解码器因子分解**：解码器根据用户提示隐向量 $\mathbf{h}_p$ 和每个专家隐向量 $\mathbf{h}_{\mathrm{exp},i}$ 独立预测该专家的融合权重 $w_i$：

$$Dec(\mathbf{w} \mid \mathbf{H}) = \prod_{i=1}^{|\mathcal{V}_{\mathrm{exp}}|} Dec(w_i \mid \mathbf{h}_p, \mathbf{h}_{\mathrm{exp},i}; \theta_{dec}) \tag{3}$$

**Beta 重参数化**：为保证权重分布的稳定性和单模态特性，将 $w_i$ 建模为 Beta 分布。前馈网络 $\mathrm{FFN}_{dec}$ 输出原始参数 $a_i, b_i$，通过指数映射确保 $\alpha_i, \beta_i > 1$：

$$\alpha_i = 1 + e^{a_i}, \quad \beta_i = 1 + e^{b_i}$$

测试时直接使用 Beta 分布的期望作为确定性融合系数：

$$w_i = \frac{\alpha_i}{\alpha_i + \beta_i}$$

**优化目标**：由于扩散过程反向传播困难，采用策略梯度近似优化 VGAE 参数 $\theta$，以最大化生成图像质量 $u(\mathbf{I}, \mathbf{p})$：

$$\nabla_{\boldsymbol{\theta}} \mathbb{E}_{\boldsymbol{\theta} \sim \Omega} [u(\mathbf{I}, \mathbf{p})] \approx \frac{1}{B} \sum_{b=1}^{B} u(I_b, p_b) \nabla_{\boldsymbol{\theta}} P(\mathbf{w}_b) \tag{4}$$



## 实验与关键发现

### 主要定量结果

DiffGraph 在两个主流 T2I 生成基准 DABench 和 DiffusionDB 上均取得全面领先。Table 1 报告了以图像相关性（IR）、人类偏好评分（HPS）、美学评分（AS）、提示相似度（PS）和 CLIP 评分（CS）为指标的综合对比。在 SD1.5 骨干上，DiffGraph 的 IR 达到 **73.11**，较所有对比方法实现大幅跃升；在 FLUX 骨干上，IR 进一步提升至 **136.62**，其余四项指标同样全面压制基线。

![[assets/figures/papers/paper_list_l2166_https_arxiv_org_abs_2603_20470/figures/002_Table_1.jpg]]
*Table 1: Quantitative comparisons of different methods on T2I generation quality on the DABench and DiffusionDB datasets. ∗ denotes methods equipped with our modified ESA module*

对比方法覆盖了三类主流路线：单专家选择方法 **DiffAgent**（Zhao et al., CVPR 2024）、参数依赖融合方法 **K‑LoRA**（Ouyang et al., CVPR 2025）、**LoRA.rar**（Shenaj et al., ICCV 2025）、**AutoLoRA**（Li et al., arXiv 2025），以及多概念融合方法 **Mix‑of‑Show**（Gu et al., NeurIPS 2023）、**ZipLoRA**（Shah et al., ECCV 2024）、**Iteris**（Chen et al., CVPR 2025）等。这些方法均无法在开放域多属性组合场景下匹敌 DiffGraph 的表现，根本原因在于其专家选择与融合机制依赖固定专家池或参数空间直接操作，缺乏对大规模在线异构专家动态组合的能力。

### 消融实验：关键机制验证

消融实验从三个维度揭示了 DiffGraph 各组件的因果贡献。

**图结构中的量化能力表征。** 去除节点校准机制（w/o calibration）后，IR 从 73.11 暴跌至 **11.92**（Table 3）。节点校准通过参考提示集 $\{r_j\}_{j=1}^{N_r}$ 评估专家节点的实际生成能力，并将评估结果注入节点特征。失去这一量化表征，图结构退化为仅依赖文本描述的粗糙索引，VGAE 无法获取有效的上下文信号，融合系数近乎随机。

**专家选择代理（ESA）的动态子图选择。** 移除 ESA 或使用随机激活子图策略，IR 分别降至 **16.12** 和 **15.36**（Table 4）。ESA 将用户需求解析为具体视觉属性，据此检索并过滤合适的 CKPT 与 PEFT 专家，数量 $N_{\text{ckpt}}$ 和 $N_{\text{peft}}$ 由 LLM 自动确定。失去这一环节，不相关甚至冲突的专家被纳入融合，严重污染生成质量。随机激活的极端劣化进一步印证：子图结构必须与用户意图精确对齐，而非任意子集均可。

**VGAE 融合规划器的系数生成。** Table 5 对比了五种融合策略：直接平均、随机权重、LLM 生成权重、基于参数相似度的权重，以及 DiffGraph 的 VGAE 方案。随机融合甚至导致 IR 变为 **负值（-5.27）**，表明错误权重组合会引发灾难性冲突。VGAE 通过编码子图节点与边的上下文信息，建模融合权重为 Beta 分布，在测试时以期望值 $w_i = \alpha_i / (\alpha_i + \beta_i)$ 输出确定性系数，显著优于所有替代方案。

### 增量专家扩展性

Table 2 展示了 DiffGraph 在动态演化的专家生态下的表现。以 2023 年专家池为起点，增量添加至 2025 年专家（2023→2025 设置），DiffGraph 的 IR 达到 **69.64**，与在完整 2025 专家池上训练的方法（73.11）差距仅约 3.5 个点，且已超越所有在 2025 设置下训练的基线方法。这一结果证明通用图的节点注册机制支持无训练方式接入新专家，图结构的可扩展性使得框架能够持续受益于在线专家生态的增长。

### 定性分析

Figure 2 以“颜料盒”方式可视化各方法对提示中视觉属性的满足程度：实心格表示属性成功呈现，半实心格表示低质量呈现，空白格表示属性完全缺失。DiffGraph 在多数复杂提示下实现全属性覆盖，而基线方法普遍存在属性遗漏或表达质量不足。这直观印证了动态子图激活机制在细粒度属性组合上的优势。

![[assets/figures/papers/paper_list_l2166_https_arxiv_org_abs_2603_20470/figures/003_Figure_2.jpg]]
*Figure 2: Qualitative comparisons of different methods on T2I generation. Different attributes in the prompt text are labeled with different colors. We illustrate visual attributes in a paint box manner, where a full colored cell denotes an attribute is successfully reflected in the generated image, a half colored cell denotes the attribute is reflected but at low quality, and an empty (white) cell means the corresponding attribute is totally missing. Zoom in for a better view. More examples are in Supplementary*

### 需要手动验证的边界

当前实验未报告 LLM 代理的推理延迟与 API 调用成本数据，大规模部署时的吞吐量瓶颈需进一步评估。此外，通用图构建中参考提示的数量 $N_r$ 和多样性对未知领域专家评估准确性的影响，原文未提供消融分析，相关结论需谨慎外推。

### 补充图表

![[assets/figures/papers/paper_list_l2166_https_arxiv_org_abs_2603_20470/figures/004_Table.jpg]]

![[assets/figures/papers/paper_list_l2166_https_arxiv_org_abs_2603_20470/figures/005_Table.jpg]]



## 定位与知识库关联

### 与现有基线方法的关系

DiffGraph将模型融合重新定义为图上的动态子图激活问题，其设计逻辑与现有工作形成系统性差异。

**单专家选择方法**仅从候选池中挑选单一最优专家，无法组合多个专家的互补能力。典型代表为**DiffAgent**（Zhao et al., CVPR 2024），该方法通过LLM代理解析用户需求并检索单个最匹配的模型，但面对需要同时满足多个视觉属性的复杂提示时，单一模型往往力不从心。

**参数依赖融合方法**直接操作模型参数空间，对专家模型的结构同质性有强假设。**K-LoRA**（Ouyang et al., CVPR 2025）和**AutoLoRA**（Li et al., arXiv 2025）通过线性组合LoRA权重实现融合，要求所有专家共享同一基模型且采用相同秩配置；**LoRA.rar**（Shenaj et al., ICCV 2025）引入超网络预测融合权重，但训练依赖固定专家集合，无法泛化至新专家。**Mix-of-Show**（Gu et al., NeurIPS 2023）和**ZipLoRA**（Shah et al., ECCV 2024）分别针对多概念定制和风格-主体融合场景，融合逻辑硬编码于参数合并规则中，缺乏对用户意图的动态适配。

**优化驱动融合方法**在测试时执行搜索或迭代优化，计算开销大且结果不稳定。**Model Swarms**（Feng et al., ICML 2025）采用粒子群优化在权重空间中搜索融合方案，**Diffusion Soup**（Biggs et al., ECCV 2024）通过贪心算法筛选专家子集，**Iteris**（Chen et al., CVPR 2025）依赖迭代对齐过程，三者均需为每个用户请求重新执行优化，难以规模化部署。

DiffGraph的核心突破在于将融合决策从参数空间迁移至图语义空间：通过图变分自编码器（VGAE）编码专家能力表征与用户需求的上下文关系，生成融合系数。这一设计使方法天然支持异构专家（CKPT与LoRA混合）、动态专家池（无需重新训练即可添加新专家）和自适应专家数量选择。

### 适用边界与关键约束

**适用场景**：DiffGraph面向开放领域文本到图像生成，尤其适用于需要组合多种视觉属性（如“赛博朋克风格的油画质感猫咪，带有梵高笔触”）的复杂提示。其图结构管理机制使其在专家资源持续演化的在线生态中具有独特优势。

**关键约束**：
1. **专家形式限制**：当前框架仅支持CKPT（完整检查点）和LoRA两种模型形式，无法直接处理Adapter、Prefix-tuning等其他参数高效微调方法。扩展至更多专家类型需重新设计节点特征提取与融合系数映射逻辑。
2. **LLM代理依赖**：专家选择代理（ESA）和图构建代理（GCA）均依赖商用MLLM（如GPT-4o），引入API调用成本和推理延迟。在大规模实时部署场景下，LLM代理可能成为吞吐量瓶颈。
3. **静态图特征假设**：融合系数生成完全依赖图结构中预计算的节点与边特征，无法利用用户交互反馈进行动态调整。当参考提示集未能充分覆盖目标领域时，节点校准质量可能下降。

### 局限与开放问题

**已知局限**：论文未明确报告失败案例或退化场景。但从消融实验可推断，当节点校准机制缺失时，IR从73.11骤降至11.92，说明图特征质量直接决定方法上限。在专家描述不准确或参考提示覆盖不足的领域，性能可能显著退化。

**开放问题**：
1. **LLM代理的规模化瓶颈**：ESA和GCA的推理延迟与API成本在大规模部署时是否成为吞吐量瓶颈？是否可能通过小型专用模型蒸馏替代商用LLM？
2. **参考提示集的设计原则**：通用图构建过程中，参考提示的数量$$N_r$$和多样性如何影响未知领域的专家评估准确性？是否存在最优的提示采样策略？
3. **专家类型的可扩展性**：当前仅支持CKPT与LoRA，如何扩展至更多类型的专家模型（如ControlNet、IP-Adapter等条件控制模块）？不同专家类型的融合系数是否需要差异化的生成机制？
4. **动态反馈闭环**：融合系数生成完全依赖静态图特征，能否引入用户交互反馈（如对生成图像的偏好标注）实现在线调整，形成“生成-反馈-优化”闭环？
5. **图结构的时效性维护**：在线专家资源持续更新，如何自动化检测专家能力漂移并触发节点重新校准？图结构的增量更新策略尚待探索。

### 知识库定位

DiffGraph处于**模型融合 × 智能体驱动自动化 × 图表征学习**的交叉点。其将模型融合抽象为子图激活问题的思路，为“大规模异构模型生态的按需组合”提供了通用范式。方法论上，VGAE生成上下文相关融合系数的设计可迁移至其他需要动态加权组合多个黑盒模块的场景（如LLM路由、多模态专家集成）。工程上，两阶段代理架构（离线图构建 + 在线子图激活）为平衡准备开销与推理效率提供了参考模板。



## 原文 PDF

![[paperPDFs/CVPR_2026/DiffGraph_An_Automated_Agent_driven_Model_Merging_Framework_for_In_the_Wild_Text_to_Image_Generation.pdf]]
