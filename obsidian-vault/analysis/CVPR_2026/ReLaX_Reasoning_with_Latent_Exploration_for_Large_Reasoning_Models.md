---
title: "ReLaX: Reasoning with Latent Exploration for Large Reasoning Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ReLaX_Reasoning_with_Latent_Exploration_for_Large_Reasoning_Models.pdf
project_link: null
code_link: "https://github.com/ZhangShimin1/ReLaX"
aliases:
- ReLaX
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过Koopman算子谱分析得到的动力学谱散度（DSD）可以量化潜空间动态的异质性；将DSD作为正则项引入策略优化目标，即可直接调控探索-利用平衡。
primary_logic: 利用Koopman算子理论将LLM/VLM的隐状态演化线性化，并借助DSD度量潜动态的丰富度，将其融入策略优化，比token级熵方法更根本地促进探索-利用平衡，因为潜空间比token空间蕴含更丰富、更稳定的动态信息。
claims:
- RLVR中策略熵H与奖励R呈指数关系 R = -a·exp(H) + b，表明熵崩溃直接限制性能。
- ReLaX在7个多模态和6个纯文本推理基准上取得最优结果，显著超越基线。
- 消融实验证实DSD正则化和自适应KL惩罚是维持高性能的关键，移除后性能大幅下降。
- 训练动态显示，ReLaX维持更高的DSD和熵，避免GRPO的快速僵化，同时获得更高奖励。
---

# ReLaX: Reasoning with Latent Exploration for Large Reasoning Models

> [!tip] 核心洞察
> 利用Koopman算子理论将LLM/VLM的隐状态演化线性化，并借助DSD度量潜动态的丰富度，将其融入策略优化，比token级熵方法更根本地促进探索-利用平衡，因为潜空间比token空间蕴含更丰富、更稳定的动态信息。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReLaX：面向大型推理模型的潜在探索推理 |
| 英文题名 | ReLaX: Reasoning with Latent Exploration for Large Reasoning Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.07558) · [Code](https://github.com/ZhangShimin1/ReLaX) |
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | ReLaX |
| Dataset | 7 Multimodal benchmarks, 6 Text-only Math benchmarks |

> [!tip] 效果简介
> - 7 Multimodal benchmarks (avg) 上，mean@1 accuracy 53.2 (ReLaX-VL-7B) vs 47.9 (Qwen2.5-VL-7B base) (+5.3)。
> - 6 Text-only Math benchmarks (avg) 上，mean@1 / mean@32 average 49.1 (ReLaX-7B-Math) vs 37.6 (SimpleRL-7B-Math) (+11.5)。

## 概述

大型推理模型在强化学习与可验证奖励（RLVR）训练中普遍面临**性能饱和**问题：随着训练推进，策略的标记级熵（token entropy）迅速下降，而奖励提升随之停滞。本文通过实证揭示，奖励 $R$ 与标记熵 $H$ 之间呈指数关系 $R = -a \cdot \exp(H) + b$（Figure 1），表明**熵崩溃是限制RLVR性能的关键瓶颈**。

然而，本文进一步指出，标记级熵的下降仅是表面症状，根本原因在于策略的**隐状态动力学逐渐丧失多样性**——即“动力学僵化”（computational rigidity），导致探索不足与过早收敛。现有方法（如基于标记级熵正则化的 R1-zero-Div、基于协方差的 KL-Cov、频率奖励 FR3E 等）均未触及这一深层机制。

针对上述问题，本文提出 **ReLaX（Reasoning with Latent Exploration）**，核心思路如下：

- **理论基础**：引入 **Koopman算子理论**，将LLM/VLM最后层隐状态的演化过程线性化，从而在潜空间（latent space）而非标记空间（token space）中分析策略的内部计算动态。
- **核心度量**：提出**动力学谱散度（Dynamic Spectral Dispersion, DSD）**——即Koopman算子特征值幅度的方差 $\mathrm{DSD}(x) = \mathrm{Var}(|\Lambda|)$，用于量化潜动态的异质性与灵活性。
- **优化机制**：将DSD作为正则项融入GRPO目标函数，并辅以自适应KL惩罚，仅在正优势轨迹上鼓励潜空间探索，实现更根本的探索-利用平衡。

**主要结果**：

- 在多模态推理基准（7个）上，**ReLaX-VL-7B** 平均准确率达 53.2%，较基座模型 Qwen2.5-VL-7B（47.9%）提升 +5.3，取得同类7B模型最优（Table 1）。
- 在纯文本数学推理基准（6个）上，**ReLaX-7B-Math** 平均得分 49.1，较 SimpleRL-7B-Math（37.6）提升 +11.5（Table 2）。
- 训练动态分析显示，ReLaX 持续维持更高的 DSD 和策略熵，有效避免 GRPO 的快速动力学僵化，同时获得更高奖励（Figure 3, Figure 8）。

**方法定位**：ReLaX 属于**潜空间探索正则化**范式，区别于传统的标记级探索方法。其关键创新在于将动力学系统理论（Koopman谱分析）引入RLVR训练，从内部计算灵活性角度解决探索不足问题，为推理模型的强化学习训练提供了新的理论视角与实用工具。

## 背景与动机

### 推理模型训练中的探索困境

大型推理模型（Large Reasoning Models, LRMs）通过强化学习与可验证奖励（Reinforcement Learning with Verifiable Rewards, RLVR）进行后训练，已成为提升数学推理、代码生成等复杂任务能力的核心范式。然而，RLVR训练过程面临一个根本性瓶颈：策略模型在优化过程中逐渐丧失行为多样性，导致过早收敛到次优解。

**熵崩溃的表象与本质**。如图1所示，在纯文本LLM和多模态VLM的RLVR训练中，策略性能 R 与token级熵 H 之间呈现指数关系 R = −a·exp(H) + b。这意味着熵的微小下降即会导致奖励的急剧衰减——这一现象被称为“熵崩溃”（entropy collapse）。当策略的token级熵持续走低时，模型陷入确定性输出模式，丧失了探索多样化推理路径的能力，从而限制了最终性能的上限。

然而，token级熵崩溃仅仅是表面症状。ReLaX的核心洞察在于：**RLVR训练中真正的瓶颈是策略隐状态动力学的僵化（computational rigidity）**。随着训练推进，模型内部的计算模式——即隐状态在推理过程中的演化轨迹——逐渐丧失多样性，形成固定的“思维惯性”。这种潜空间层面的动力学僵化，才是导致探索不足和过早收敛的深层原因。

### 现有探索方法的局限

当前主流RLVR方法对探索问题的应对主要集中在token空间层面：

- **熵正则化**（如R1-zero-Div）：直接在token分布上施加熵惩罚，鼓励输出多样性。但token级熵只能反映表层输出随机性，无法触及内部计算过程的灵活性。
- **协方差正则化**（如KL-Cov）：通过约束token分布的协方差结构来避免模式坍塌。这类方法同样停留在输出空间，对隐状态动力学的调控能力有限。
- **奖励塑形**（如FR3E）：通过频率奖励等机制鼓励模型访问低频token。这些方法本质上是启发式的表面干预，缺乏对探索-利用平衡的系统性调控。

上述方法的共同缺陷在于：它们将探索问题建模为token空间的统计多样性问题，而忽略了**潜空间（latent space）比token空间蕴含更丰富、更稳定的动态信息**。一个推理策略的“探索性”不仅体现在它输出了哪些token，更体现在它内部如何组织计算、如何在不同思维模式间切换。仅从token层面干预，如同试图通过调节汽车的尾气排放来控制发动机的运转——治标不治本。

### ReLaX的动机与核心思路

ReLaX的提出基于一个关键认知：**要实现真正的探索-利用平衡，必须直接调控策略的隐状态动力学，而非间接地操纵输出分布**。为此，ReLaX引入Koopman算子理论，将LLM/VLM最后一层隐状态的演化过程线性化，从而能够在潜空间中量化策略计算的灵活性。

具体而言，ReLaX提出**动力学谱散度（Dynamic Spectral Dispersion, DSD）**这一新指标，通过Koopman算子特征值幅度的方差来度量潜动态的异质性。DSD越高，表明模型内部的计算模式越多样化；DSD持续走低，则意味着动力学僵化正在发生。ReLaX将DSD作为正则项融入GRPO优化目标，仅在正优势轨迹上鼓励潜空间探索，同时辅以自适应KL惩罚防止过度发散，从而在根源上缓解RLVR中的探索不足问题。

这一框架的独特之处在于：它首次将RLVR中的探索问题从token空间提升到潜空间层面，利用动力系统理论为探索-利用平衡提供了更根本的调控手段。如后续实验所示，ReLaX在7个多模态推理基准和6个纯文本数学推理基准上均取得最优结果，验证了潜空间探索范式的有效性。

## 核心创新

### 瓶颈诊断：从token级熵崩溃到潜空间动力学僵化

RLVR（Reinforcement Learning with Verifiable Rewards）训练中，策略性能饱和的根本原因并非表层的token级熵崩溃，而是**隐状态动力学的逐渐僵化**。实证分析（Figure 1）揭示，策略奖励 $R$ 与token级熵 $H$ 之间呈指数关系 $R = -a \cdot \exp(H) + b$，这意味着熵的微小下降即可导致性能大幅衰退。然而，token级熵仅是内部计算模式丧失灵活性的外在表现——当策略的潜空间动态趋于单一化，模型便丧失了探索多样化推理路径的能力，过早收敛到次优解。

### 核心机制：动力学谱散度（DSD）与潜空间探索

ReLaX的核心创新在于将探索机制从token空间**下沉到潜空间**，通过量化并调控隐状态动力学的异质性来根本性地促进探索-利用平衡。这一设计基于以下关键洞察：潜空间蕴含比token空间更丰富、更稳定的动态信息，因而更适合作为探索调控的载体。

具体而言，ReLaX引入**动力学谱散度（Dynamic Spectral Dispersion, DSD）**作为潜动态多样性的度量。其理论基础是Koopman算子理论——将LLM/VLM末层隐状态的非线性演化线性化后，Koopman算子特征值幅度的方差即可反映内部计算的灵活程度：

$$\mathrm{DSD}(x) = \mathrm{Var}(|\Lambda|),\quad \text{where } K\Phi = \Phi\Lambda$$

DSD越高，表明模型在潜空间中探索的模式越丰富；DSD持续走低，则意味着动力学僵化正在发生。

### 方法谱系与知识库定位

在RLVR探索机制的方法谱系中，现有工作主要集中在token级操作：

- **Vanilla GRPO**：仅依赖组内归一化优势进行策略更新，无显式探索机制；
- **DAPO**、**KL-Cov**：通过token级协方差或KL散度鼓励输出多样性；
- **R1-zero-Div**、**FR3E**：采用熵正则化或频率奖励塑形来维持表面探索。

这些方法将探索信号作用于token空间，只能间接缓解潜空间的僵化问题。ReLaX则直接从隐状态动力学入手，利用Koopman谱分析将探索信号注入策略优化的核心目标函数，属于**潜空间探索**这一新兴技术路径。

### Changed Slots：相对GRPO的关键改动

| 组件 | GRPO（基线） | ReLaX（改进） |
|------|-------------|--------------|
| **优化目标** | 最大化期望奖励 $\mathcal{I}_{\mathrm{GRPO}}(\theta)$ | 加入DSD正则项与自适应KL惩罚：$\mathcal{I}(\theta) = \mathcal{I}_{\mathrm{GRPO}}(\theta) + \alpha \tilde{\mathcal{L}}_{\mathrm{xp}} + \beta \sum_{i}^{\mathcal{T}} D_{\mathrm{KL}}(\pi_{\theta}(o^i) \parallel \pi_{\mathrm{ref}}(o^i))$ |
| **探索机制** | 依赖token级熵或奖励塑形 | 基于Koopman谱分析的DSD，直接鼓励潜空间计算灵活性 |

其中，**优势塑形的DSD正则项**是关键设计：仅对正优势轨迹（即表现优于组内平均的样本）鼓励其潜动态多样性，避免无意义的随机探索：

$$\tilde{\mathcal{L}}_{\mathrm{xp}} = \log\left(\frac{1}{R}\sum_{i=1}^{R}\exp(-\mathrm{clip}(\hat{A}^i, 0) \cdot \mathrm{DSD}(x^i))\right)$$

**自适应KL惩罚**则仅对DSD超过阈值 $\xi$ 的轨迹施加散度约束，防止潜动态过度发散导致策略崩溃。这一设计使ReLaX在维持更高DSD和熵的同时，仍能获得更优的奖励收敛（Figure 3, Figure 8）。

### 技术实现管线

ReLaX的完整管线包含四个模块：

1. **Koopman字典学习**：使用ResKoopNet训练一个线性层 $g(x) = \sigma(Wx), W \in \mathbb{R}^{d \times m}$ 作为可观测函数，将隐状态映射到线性化空间，拟合后冻结参数；
2. **DSD计算**：基于估计的Koopman算子计算特征值幅度的方差；
3. **DSD正则化**：将优势加权的DSD分数作为损失项加入GRPO目标；
4. **自适应KL惩罚**：对DSD超阈值的轨迹施加KL散度约束。

消融实验（Figure 5）证实，移除自适应KL正则化会导致性能持续下降，移除优势塑形则直接引发训练崩溃，表明这两个设计是ReLaX维持稳定高效探索的必要组件。

## 整体框架

ReLaX 的整体 pipeline 围绕一个核心洞察构建：**RLVR 训练中策略性能饱和的根本原因不在于 token 级熵的崩溃，而在于隐状态动力学的僵化**。因此，ReLaX 将探索机制从 token 空间下沉到潜空间，通过量化并调控隐状态动态的多样性，从根本上改善探索-利用平衡。

### 框架总览

ReLaX 的完整框架如 **Figure 2** 所示，由四个紧密耦合的模块组成，嵌入标准 GRPO 训练流程：

![[assets/figures/papers/paper_list_l2579_https_arxiv_org_abs_2512_07558/figures/002_Figure_2.jpg]]
*Figure 2: Overview of ReLaX. Grounded in Koopman operator theory (upper left), ReLaX employs a neural Koopman dictionary (frozen after one step of learning) during policy optimization to linearize the latent dynamics of last-layer hidden states. This transformation allows us to assess the flexibility of policy’s internal computations through the proposed DSD. The DSD score for each trajectory is subsequently integrated into the GRPO objective, mitigating computational rigidity and enabling a more effective exploration–exploitation tradeoff*

1. **Koopman 字典学习**：在训练开始时，从策略模型的最后一层隐状态中一次性训练一个轻量线性字典，将非线性隐状态演化线性化到 Koopman 算子框架中。字典参数冻结后不再更新。
2. **DSD 计算**：对于每个 rollout 轨迹，利用冻结的 Koopman 字典估计 Koopman 算子，提取其特征值，并计算特征值幅度的方差——即动力学谱散度（Dynamic Spectral Dispersion, DSD），作为该轨迹潜动态多样性的量化指标。
3. **DSD 正则化**：将优势加权的 DSD 分数作为额外的损失项注入 GRPO 目标函数，仅对具有正优势的轨迹鼓励其潜动态多样性，避免低质量轨迹的无意义探索。
4. **自适应 KL 惩罚**：对 DSD 超过预设阈值的轨迹施加 KL 散度惩罚，防止策略在潜空间过度发散，维持优化的稳定性。

### 输入输出流

整个 pipeline 的数据流如下：

- **输入**：训练问题 $q$ 及其对应的 $R$ 条 rollout 轨迹 $\{o^i\}_{i=1}^R$，每条轨迹的最后一层隐状态序列 $\{x_t\}$。
- **Koopman 字典学习阶段**（仅执行一次）：以隐状态 $x$ 为输入，通过单层线性变换加 Sigmoid 激活 $g(x) = \sigma(Wx), W \in \mathbb{R}^{d \times m}$ 参数化 Koopman 可观测函数，利用 ResKoopNet 训练得到 $W$ 后冻结。
- **DSD 计算**：对每条轨迹的隐状态序列应用冻结的 $g(\cdot)$，估计 Koopman 算子 $K$ 及其特征值 $\Lambda$，输出 $\mathrm{DSD}(x) = \mathrm{Var}(|\Lambda|)$。
- **优势塑形**：计算组内归一化优势 $\hat{A}^i$，将 DSD 与 $\mathrm{clip}(\hat{A}^i, 0)$ 结合，形成优势加权的探索正则项 $\tilde{\mathcal{L}}_{\mathrm{xp}}$。
- **输出**：修改后的总优化目标 $\mathcal{I}(\theta) = \mathcal{I}_{\mathrm{GRPO}}(\theta) + \alpha \tilde{\mathcal{L}}_{\mathrm{xp}} + \beta \sum_i^{\mathcal{T}} D_{\mathrm{KL}}(\pi_\theta(o^i) \parallel \pi_{\mathrm{ref}}(o^i))$，用于策略参数 $\theta$ 的梯度更新。

### 模块间的因果依赖

各模块之间存在严格的因果链：

- **Koopman 字典 → DSD**：字典质量直接决定 Koopman 算子估计的准确性，进而影响 DSD 的可靠性。消融实验表明，Koopman 维度 $m \geq 10$ 时 DSD 较为鲁棒，$m=5$ 时谱模式过少导致 DSD 不稳定（**Figure 11**）。
- **DSD → 正则化**：DSD 作为探索信号，通过优势塑形筛选出值得鼓励多样性的轨迹。移除优势塑形会导致训练崩溃，说明无差别地鼓励所有轨迹的潜多样性会引入噪声（**Figure 5**）。
- **自适应 KL → 稳定性**：KL 惩罚仅在 DSD 超过阈值时激活，防止策略过度发散。移除该机制会导致性能持续下降（**Figure 5**），证实其在维持探索-利用平衡中的关键作用。

### 与 token 级方法的本质区别

传统探索方法（如熵正则化、KL-Cov 等）在 token 空间操作，仅能捕捉输出分布的表面多样性。ReLaX 的 DSD 直接作用于隐状态动态，捕捉的是**内部计算模式的灵活性**——这一信号在 token 空间不可见。如 **Figure 6** 所示，在多模态推理基准上，ReLaX 在视觉依赖任务上的增益尤为显著，表明潜空间探索对需要深层视觉-语言融合的推理任务具有独特价值。

> **注意**：Koopman 字典在训练前一次性拟合后冻结，可能无法适应训练后期动力学分布的变化，这是框架的一个已知局限。此外，DSD 计算引入约 10-12% 的额外训练时间开销，主要来自 actor 更新阶段。

## 核心模块与公式推导

ReLaX 的核心创新在于将 **Koopman 算子理论**引入策略优化的内部循环，通过量化并调控隐状态的动力学多样性，从根本上解决 RLVR 训练中的探索不足问题。其方法体系由四个紧密耦合的模块构成。

### 动力学谱散度（DSD）

将 LLM/VLM 的逐 token 隐状态演化视为一个随机非线性动力系统：

$$x_t = F(x_{t-1}, \omega_t), \quad \omega_t \sim P_\omega$$

其中 $x_t$ 为最后一层隐状态。Koopman 算子理论的核心思想是：存在一个可观测函数 $\Phi$，将该非线性系统映射到高维空间后，其演化可被一个线性算子 $K$ 精确描述：

$$K\Phi = \Phi\Lambda$$

其中 $\Lambda$ 为 Koopman 算子的特征值矩阵。ReLaX 的关键洞察是：**特征值幅度的方差直接反映了潜空间动态的异质性**——方差越大，策略内部计算模式越灵活；方差趋近于零，则意味着动力学僵化。由此定义动力学谱散度：

$$\mathrm{DSD}(x) = \mathrm{Var}(|\Lambda|)$$

DSD 本质上是一个无需显式建模探索行为的“计算灵活性”度量，它从潜空间层面捕捉了策略是否陷入固定的推理模式。

### Koopman 字典学习

为在实际训练中高效计算 DSD，ReLaX 使用一个极简的神经网络来近似 Koopman 可观测函数。具体地，可观测函数 $g$ 被参数化为一个线性层加 Sigmoid 激活：

$$g(x) = \sigma(W x), \quad W \in \mathbb{R}^{d \times m}$$

其中 $d$ 为隐状态维度，$m$ 为 Koopman 维度（即谱模式数量）。该字典通过 ResKoopNet 在训练前一次性拟合，随后冻结参数。在策略优化的每一步，仅需将隐状态通过该冻结的线性层，即可估计 Koopman 算子并计算 DSD。这种设计将额外的计算开销控制在约 10–12%，主要来自 actor 更新中的 DSD 计算。

### 优势塑形的 DSD 正则化

直接将 DSD 作为损失项最大化可能导致无意义的随机探索。ReLaX 的关键设计是**仅对正优势轨迹鼓励潜动态多样性**：

$$\tilde{\mathcal{L}}_{\mathrm{xp}} = \log\left(\frac{1}{R}\sum_{i=1}^{R}\exp(-\mathrm{clip}(\hat{A}^i, 0) \cdot \mathrm{DSD}(x^i))\right)$$

其中 $\hat{A}^i$ 为 GRPO 的组内归一化优势：

$$\hat{A}^i = \frac{\mathrm{reward}(q, o^i) - \mathrm{mean}[\mathrm{reward}]}{\mathrm{std}[\mathrm{reward}]}$$

该设计的因果逻辑是：对于优势为正（即表现优于组内平均）的轨迹，其潜动态多样性被鼓励，从而将探索引导至有前景的方向；对于劣势轨迹，DSD 项被置零，避免在低质量区域浪费探索预算。

### 自适应 KL 惩罚与总体目标

为防止 DSD 正则化导致策略过度发散，ReLaX 引入自适应 KL 惩罚——仅对 DSD 超过阈值 $\xi$ 的轨迹施加 KL 散度约束。完整的 ReLaX 优化目标为：

$$\mathcal{I}(\theta) = \mathcal{I}_{\mathrm{GRPO}}(\theta) + \alpha \tilde{\mathcal{L}}_{\mathrm{xp}} + \beta \sum_{i}^{\mathcal{T}} D_{\mathrm{KL}}(\pi_{\theta}(o^i) \parallel \pi_{\mathrm{ref}}(o^i))$$

其中 $\mathcal{I}_{\mathrm{GRPO}}(\theta)$ 为标准 GRPO 目标，$\alpha$ 控制潜空间探索的正则化强度，$\beta$ 控制 KL 惩罚力度，$\mathcal{T}$ 为 DSD 超过阈值的轨迹集合。

### 与 Token 级方法的本质区别

现有探索方法（如 **DAPO** 的 token 级熵正则化、**KL-Cov** 的协方差约束、**R1-zero-Div** 的熵奖励）均在 token 空间操作，只能应对“表面症状”。ReLaX 通过 Koopman 谱分析将探索机制下沉到潜空间：token 级熵崩溃只是内部计算僵化的外在表现，而 DSD 直接度量并调控隐状态动力学的丰富度，从根源上维持探索-利用平衡。

### 补充图表

![[assets/figures/papers/paper_list_l2579_https_arxiv_org_abs_2512_07558/figures/001_Figure_1.jpg]]
*Figure 1: Empirical relationship between policy performance R and token-level entropy H during RLVR training with (a) textonly LLMs and (b) vision-language models (VLMs). Each scatter denotes a single training step, the solid curve fitted by R = −a · exp(H) + b [10]*

## 实验与分析

### 核心瓶颈验证：熵崩溃与性能饱和

RLVR训练中普遍存在一个隐性的性能瓶颈：策略的token级熵（*H*）与奖励（*R*）之间并非线性关系，而是呈现指数衰减耦合 **R = −a·exp(H) + b**（Figure 1）。无论在纯文本LLM还是多模态VLM上，随着训练推进，熵迅速坍缩至接近零值，奖励随之饱和。这表明，表面上的“熵崩溃”只是症状，其根源在于**策略的隐状态动力学逐渐丧失多样性（动力学僵化）**，导致探索不足和过早收敛。ReLaX正是从这一根本问题出发，通过调控潜空间动态来打破僵化。

### 主实验结果

#### 多模态推理基准

Table 1汇总了ReLaX-VL在7个多模态推理基准上的mean@1准确率。在7B规模上，ReLaX-VL-7B取得平均53.2分，相较基座模型Qwen2.5-VL-7B（47.9分）提升**+5.3分**，在所有同类7B推理模型中达到最优。在3B规模上，ReLaX-VL-3B相较基座模型的绝对提升达**+8.3分**。值得注意的是，ReLaX在视觉依赖较强的任务上增益尤为显著——Figure 6a显示，在5个多模态基准上，ReLaX相较KL-Cov和Vanilla GRPO均有稳定提升，其中部分任务的增益超过10个百分点。Figure 9进一步给出了各基准上的完整对比，确认了这一趋势的稳健性。

#### 纯文本数学推理基准

Table 2展示了ReLaX在6个纯文本数学推理基准上的表现。以Qwen2.5-7B-Math为基座，ReLaX-7B-Math的平均得分（mean@1与mean@32综合）达到49.1分，远超SimpleRL-7B-Math的37.6分（**+11.5分**），并在MATH500上取得82.4的mean@1准确率。在Llama3.2-Instruct和Qwen3等其他基座模型上的补充实验（Table 5）同样确认了ReLaX相对于GRPO基线的稳定增益，表明该方法对不同模型架构具有较好的泛化性。

![[assets/figures/papers/paper_list_l2579_https_arxiv_org_abs_2512_07558/figures/016_Table_5.jpg]]
*Table 5: Supplemented comparison of LLM performance (mean@1 & mean@32) trained from Llama3.2-Instruct and Qwen3 across multiple text-only mathematical reasoning benchmarks. The performance gains of ReLaX over the GRPO baseline are highlighted in red. † indicates our reproduced results using publicly available models and standard evaluation code. “–” denotes missing results due to unavailable models*

### 训练动态分析：DSD维持探索-利用平衡

Figure 3对比了ReLaX与Vanilla GRPO在Qwen2.5-VL-Instruct 3B/7B上的完整训练动态。四个关键指标揭示了ReLaX的作用机制：

1. **奖励（Reward）**：ReLaX的奖励曲线始终高于GRPO，且未出现GRPO后期的饱和平台，最终相对性能增益约**10%**。
2. **DSD（动力学谱散度）**：GRPO的DSD在训练早期即快速下降并趋于零，表明隐状态动力学迅速僵化；ReLaX则维持了显著更高的DSD水平，意味着内部计算模式持续保持多样性。
3. **熵（Entropy）**：GRPO的token级熵急剧坍缩，而ReLaX将熵稳定在一个更高但受控的水平，避免了无意义的随机探索。
4. **响应长度（Response Length）**：ReLaX的响应长度保持稳定，未出现GRPO中常见的长度爆炸或骤缩。

Figure 6b-c及Figure 10进一步比较了ReLaX与KL-Cov、Entropy Reg等token级探索方法的训练动态。结果显示，token级方法虽然能在一定程度上延缓熵坍缩，但其DSD仍快速下降，无法从根本上解决动力学僵化问题；唯有ReLaX同时维持了高DSD和高熵。

![[assets/figures/papers/paper_list_l2579_https_arxiv_org_abs_2512_07558/figures/013_Figure_10.jpg]]
*Figure 10: More training dynamics of vanilla GRPO, KL-Cov, Entropy Reg and our ReLaX on Qwen2.5-3B-VL. This figure provides the extended results for Fig. 6b and 6c*

### 消融实验

#### DSD正则化系数 α 的影响

Figure 4展示了不同α取值（0, 0.1, 0.3, 1.0）下策略熵与奖励的训练动态。当**α=0.1**时，奖励达到最高；α增大虽能进一步提升熵，但过强的潜空间探索会损害收敛，导致奖励下降。α=0（即无DSD正则化）时，训练动态退化为GRPO，熵快速坍缩且奖励饱和。

#### 自适应KL惩罚与优势塑形

Figure 5的消融结果表明，移除**自适应KL正则化**后，模型在多个基准上的性能持续下降；移除**优势塑形**（即对正优势轨迹的筛选机制）则导致训练崩溃，性能大幅跳水。这验证了两个设计的关键性：自适应KL惩罚仅对DSD超过阈值ξ的轨迹施加约束，防止潜动态过度发散；优势塑形确保DSD正则化仅作用于“好”的探索方向，避免无意义的随机扰动。

#### Koopman字典维度的影响

Figure 11显示，当Koopman字典维度**m=5**时，谱模式过少导致DSD估计不稳定；当**m≥10**时，DSD计算趋于鲁棒，性能表现稳定。ReLaX默认采用m=10，在计算开销与表征能力之间取得平衡。

### 与Token级探索方法的对比

Figure 6a及Figure 9系统比较了ReLaX与KL-Cov（基于协方差的token级探索）、Entropy Reg（熵正则化）等方法在Qwen2.5-3B-VL上的多模态基准性能。ReLaX在全部5个基准上均优于KL-Cov和Vanilla GRPO，其中在视觉推理密集型任务上的优势尤为突出。Table 8通过DynaMath上的具体案例展示了ReLaX与KL-Cov的推理差异：KL-Cov在视觉内容变化时频繁出现推理失败（如错误识别几何体形状、遗漏关键尺寸），而ReLaX展现出更强的视觉-语言对齐鲁棒性。

### 计算开销

Table 6给出了每训练步的耗时分解。ReLaX相较Vanilla GRPO的额外开销约为**10-12%**，主要来自Actor更新中的DSD计算（包括Koopman字典的前向传播和特征值分解）。考虑到性能增益幅度，这一开销在可接受范围内。

### 失败模式与局限性

尽管ReLaX在多数场景下表现优异，分析中仍识别出以下局限：

- **超参数敏感性**：DSD阈值ξ和正则化系数α需针对不同任务和模型规模调节。α过大会损害收敛（Figure 4），ξ设置不当则可能削弱KL惩罚的稳定作用。
- **Koopman字典的静态性**：字典在训练前一次性拟合并冻结，可能无法适应训练后期动力学分布的变化。这在高动态训练场景下可能成为瓶颈。
- **任务泛化性待验证**：当前实验集中于数学推理和多模态推理，DSD在常识推理、代码生成等更广义推理任务上的有效性尚需进一步检验（开放问题）。
- **规模扩展性未知**：现有实验覆盖3B-7B模型，在更大规模（如30B、70B）上ReLaX的扩展行为尚未被验证（开放问题）。

![[assets/figures/papers/paper_list_l2579_https_arxiv_org_abs_2512_07558/figures/006_Figure_4.jpg]]
*Figure 4: Training dynamics of policy entropy and reward on 3B scale Qwen2.5-VL-3B models by ReLaX with different DSDbased regularization coefficients (1.0, 0.3, 0.1, 0)*

### 补充图表

![[assets/figures/papers/paper_list_l2579_https_arxiv_org_abs_2512_07558/figures/003_Table_1.jpg]]
*Table 1: Comparison of VLM performance (mean@1 accuracy) across multiple multimodal reasoning benchmarks. For 7B scale LRMs, the top-performing and runner-up results of VLMs within each column are marked in red and blue, respectively. † indicates our reproduced results using publicly available models and standard evaluation code. “–” denotes missing results due to unavailable models*

![[assets/figures/papers/paper_list_l2579_https_arxiv_org_abs_2512_07558/figures/005_Table_2.jpg]]
*Table 2: Comparison of LLM performance (mean@1 & mean@32) across multiple text-only mathematical reasoning benchmarks. For each base model, the top-performing and runner-up results of RLVR algorithms within each column are marked in red and blue, respectively. † indicates our reproduced results using publicly available models and standard evaluation code. “–” denotes missing results due to unavailable models*

![[assets/figures/papers/paper_list_l2579_https_arxiv_org_abs_2512_07558/figures/004_Figure_3.jpg]]
*Figure 3: Comparison of training dynamics for Reward, DSD, Entropy, and Response Length under ReLaX (red) and vanilla GRPO (gray) on Qwen2.5-VL-Instruct at the 3B and 7B scales*

![[assets/figures/papers/paper_list_l2579_https_arxiv_org_abs_2512_07558/figures/008_Figure_5.jpg]]
*Figure 5: Evaluation results from the ablation study on Qwen2.5- 7B-Math for text-only reasoning tasks. Results by full ReLaX is highlighted in red, while the dark-blue and light-blue bars respectively correspond to its ablations without adaptive KL regularization and advantage shaping*

![[assets/figures/papers/paper_list_l2579_https_arxiv_org_abs_2512_07558/figures/007_Figure_6.jpg]]
*Figure 6: Comparison of RLVR training methods on Qwen2.5-3B-VL. (a) Evaluation results across 5 multimodal reasoning benchmarks. The values above each bar denote ReLaX’s performance gains over KL-Cov (left) and vanilla GRPO (right). (b) and (c) Training dynamics of policy DSD and policy entropy, respectively*

![[assets/figures/papers/paper_list_l2579_https_arxiv_org_abs_2512_07558/figures/010_Figure_8.jpg]]
*Figure 8: Comparison of training dynamics for Validation Accuracy, DSD, Entropy, and Clipped Gradient Norm under ReLaX (red) and vanilla GRPO (gray) on Qwen2.5-Base at the 3B and 7B scales*

![[assets/figures/papers/paper_list_l2579_https_arxiv_org_abs_2512_07558/figures/015_Figure_11.jpg]]
*Figure 11: Sensitivity analysis for Koopman operator dimension m and DSD threshold ξ on Qwen2.5-3B*

## 方法谱系与知识库定位

### 问题定位：RLVR中的“动力学僵化”瓶颈

ReLaX的核心动机源于对RLVR（基于可验证奖励的强化学习）训练动态的重新诊断。传统观点将性能饱和归因于token级熵的崩溃，但本文通过实证分析揭示了更深层的因果链条：**策略的隐状态动力学逐渐丧失多样性（即“动力学僵化”），导致探索不足和过早收敛；token级熵崩溃只是这一内部计算模式僵化的表面症状**。Figure 1展示了RLVR训练中策略奖励R与token级熵H之间呈指数关系 $R = -a \cdot \exp(H) + b$，表明熵的下降直接限制了性能上限。然而，token级熵仅反映了输出分布的分散程度，无法捕捉模型内部隐状态演化路径的丰富性。这一诊断将问题的焦点从“输出多样性”转移到了“内部计算灵活性”，为后续方法设计提供了新的干预靶点。

### 方法谱系：从Token级探索到潜空间探索

在ReLaX之前，RLVR训练中的探索机制主要集中在token级操作。现有基线方法可大致归为以下几类：

- **基础RLVR算法**：Vanilla GRPO（组相对策略优化）作为标准的RLVR训练框架，通过组内归一化优势 $\hat{A}^i = \frac{\mathrm{reward}(q, o^i) - \mathrm{mean}[\mathrm{reward}]}{\mathrm{std}[\mathrm{reward}]}$ 进行策略更新，但缺乏显式的探索机制。
- **Token级熵正则化**：**R1-zero-Div** 等方法通过在目标函数中直接加入熵奖励来鼓励输出多样性，但Figure 1已表明token级熵与奖励的关系是结果而非原因。
- **Token级协方差探索**：**KL-Cov** 基于协方差矩阵在token空间进行探索，试图在输出分布层面维持多样性。
- **频率奖励塑形**：**FR3E** 通过频率奖励加强探索，DAPO等方法则结合了其他token级探索策略。

这些方法的共同局限在于：它们都在token空间操作，而token空间的信息容量有限，且无法直接反映模型内部计算路径的灵活性。ReLaX的关键突破在于**将探索机制从token空间提升到潜空间**——通过Koopman算子理论将LLM/VLM的隐状态演化线性化，并借助动力学谱散度（DSD）度量潜动态的丰富度，将其融入策略优化。这一视角转换使得探索-利用平衡的调控更加根本，因为潜空间比token空间蕴含更丰富、更稳定的动态信息。

### 核心技术贡献：DSD与Koopman谱分析

ReLaX的方法设计建立在Koopman算子理论之上。该理论允许将非线性动力系统 $x_t = F(x_{t-1}, \omega_t)$ 通过可观测函数映射到线性演化空间，从而分析其全局动态特性。ReLaX的具体实现包含以下关键模块：

1. **Koopman字典学习**：使用ResKoopNet训练一个线性层加Sigmoid激活 $g(x) = \sigma(Wx), W \in \mathbb{R}^{d \times m}$ 作为Koopman可观测函数，拟合后冻结（Section 3.2）。
2. **DSD计算**：基于估计的Koopman算子，计算其特征值幅度的方差 $\mathrm{DSD}(x) = \mathrm{Var}(|\Lambda|), \text{where } K\Phi = \Phi\Lambda$，作为潜动态多样性的量化指标（Eq. 7）。
3. **DSD正则化**：将优势加权的DSD分数作为损失项加入GRPO目标 $\tilde{\mathcal{L}}_{\mathrm{xp}} = \log\left(\frac{1}{R}\sum_{i=1}^{R}\exp(-\mathrm{clip}(\hat{A}^i,0)\cdot\mathrm{DSD}(x^i))\right)$，仅对正优势轨迹鼓励其潜动态多样性，避免无意义探索（Eq. 11）。
4. **自适应KL惩罚**：仅对DSD超过阈值的轨迹施加KL散度惩罚 $\beta \sum_{i}^{\mathcal{T}} D_{\mathrm{KL}}(\pi_{\theta}(o^i) \parallel \pi_{\mathrm{ref}}(o^i))$，防止过度发散（Eq. 12）。

完整的ReLaX目标函数为 $\mathcal{I}(\theta) = \mathcal{I}_{\mathrm{GRPO}}(\theta) + \alpha \tilde{\mathcal{L}}_{\mathrm{xp}} + \beta \sum_{i}^{\mathcal{T}} D_{\mathrm{KL}}(\pi_{\theta}(o^i) \parallel \pi_{\mathrm{ref}}(o^i))$，其中 $\alpha$ 控制潜空间探索的强度，$\beta$ 控制自适应KL惩罚的力度。

### 适用边界与局限性

尽管ReLaX在多个基准上取得了显著提升，其方法设计存在以下适用边界和局限：

1. **计算开销**：ReLaX引入额外计算，每步训练时间增加约10-12%，主要来自actor更新中的DSD计算。对于资源受限的场景，这一开销需要权衡。
2. **字典固定性**：Koopman字典学习需要在训练前一次性拟合，且字典参数在训练过程中保持冻结。随着RLVR训练的推进，策略的隐状态分布可能发生显著偏移，固定的字典可能无法准确捕捉后期的动力学变化。消融实验（Figure 11）表明，Koopman维度 $m=5$ 时谱模式过少导致DSD不稳定，$m \geq 10$ 较为鲁棒，但更大的 $m$ 会进一步增加计算成本。
3. **超参数敏感性**：DSD阈值 $\xi$ 和系数 $\alpha$ 等超参数需要针对不同任务调节。消融实验（Figure 4）显示 $\alpha=0.1$ 时达到最高奖励，$\alpha$ 增大虽提升熵，但过高会损害收敛。移除自适应KL正则化导致性能持续下降，移除优势塑形则导致训练崩溃（Figure 5），表明该方法对超参数配置有一定敏感性，通用性有待进一步验证。
4. **任务范围验证**：当前验证主要集中在数学推理和多模态推理任务。DSD能否推广到更广义的推理任务（如常识推理、代码生成）尚待验证。

### 开放问题与未来方向

基于ReLaX的方法框架和当前局限，以下开放问题值得后续研究关注：

1. **任务泛化**：DSD作为潜动态多样性的度量，其有效性是否局限于数学推理类任务？在常识推理、代码生成等需要不同类型推理模式的任务上，DSD的正则化效果如何？
2. **与先进RL算法的结合**：当前ReLaX基于GRPO框架设计。能否将潜空间探索方法与更先进的RL算法（如PPO变体）或离线RL结合，进一步提升样本效率？
3. **字典架构优化**：是否可以通过更复杂的Koopman字典（如深层网络或自适应更新的字典）进一步提升性能，同时降低额外计算成本？这涉及在动态建模精度和计算效率之间的权衡。
4. **扩展性验证**：当前实验主要在3B和7B规模模型上进行。在更大规模模型（如30B、70B）上，ReLaX的扩展性如何？潜空间动力学的特性是否随模型规模发生质变？

## 原文 PDF

![[paperPDFs/CVPR_2026/ReLaX_Reasoning_with_Latent_Exploration_for_Large_Reasoning_Models.pdf]]
