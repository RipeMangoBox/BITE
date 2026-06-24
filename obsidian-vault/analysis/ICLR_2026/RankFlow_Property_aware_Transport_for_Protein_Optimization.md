---
title: "RankFlow: Property-aware Transport for Protein Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RankFlow_Property_aware_Transport_for_Protein_Optimization.pdf
aliases:
- RankFlow
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/chemistry_and_drug_discovery
core_operator: "通过能量函数引导的条件流，将 PLM 的突变表示运输到与目标属性对齐的分布，并利用可微的秩一致性损失 (RC^2) 强制保持突变排序，从而控制预测质量。"
primary_logic: "学习一个属性感知的条件流，以能量函数和秩一致性为目标，可将无监督的蛋白质表示重塑为适应度对齐的嵌入，同时捕获突变间的非加性相互作用，显著提升排序精度和跨实验泛化能力。"
claims:
- "RankFlow 在 ProteinGym 的随机划分下取得 Spearman ρ=0.786，显著优于 Kermut (0.763) 和 ProteinNPT (0.701)。"
- "在 β-内酰胺酶、GB1 和荧光蛋白基准上，RankFlow 的 Spearman 相关系数分别为 0.912、0.856、0.782，均为最优。"
- "消融实验表明，移除 RC^2 损失后各功能类别的 Spearman ρ 平均下降 0.02–0.06，尤其在高阶突变上下降显著。"
- "RankFlow 在跨实验泛化测试中比微调 ESM2/SaProt 回归头的 Spearman 相关度高约 0.05–0.10。"
---

# RankFlow: Property-aware Transport for Protein Optimization

> [!tip] 核心洞察
> 学习一个属性感知的条件流，以能量函数和秩一致性为目标，可将无监督的蛋白质表示重塑为适应度对齐的嵌入，同时捕获突变间的非加性相互作用，显著提升排序精度和跨实验泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | RankFlow：面向蛋白质优化的属性感知传输 |
| 英文题名 | RankFlow: Property-aware Transport for Protein Optimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=uS5rA4fDJp) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/chemistry_and_drug_discovery |
| Method | RankFlow |
| Dataset | ProteinGym Stability, ProteinGym Fitness, ProteinGym Expression, ProteinGym Binding |

> [!tip] 效果简介
> - ProteinGym Stability 上，Spearman ρ 为 0.911，对比 0.876 (DePLM)，变化 +0.035。
> - ProteinGym Fitness 上，Spearman ρ 为 0.742，对比 0.690 (DePLM)，变化 +0.052。
> - ProteinGym Expression 上，Spearman ρ 为 0.765，对比 0.730 (DePLM)，变化 +0.035。

## 概述

蛋白质适应度预测的核心瓶颈在于：主流方法依赖预训练语言模型（PLM）产生的属性无关表示，并普遍假设突变效应为独立位点加和，难以有效捕捉上位效应（epistasis）。这导致在少样本场景下排序能力弱、跨实验泛化差，无法准确刻画蛋白质的适应度景观。RankFlow 通过**属性感知的条件流**重塑 PLM 的突变表示，将其从野生态条件分布运输至与目标属性对齐的分布；同时引入**可微的秩一致性损失（Rank‑Consistent Conditional Flow Loss, RC²）**强制保持相对排序，从而端到端地优化排序精度。该方法利用多模态融合编码器（ESM‑2 + ESM‑IF）和属性引导门（Property‑guided Steering Gate）抑制无关进化偏差，仅引入 37.1M 可训练参数，推理成本较 DePLM 降低 94.4%。

在 ProteinGym 随机划分下，RankFlow 取得整体 Spearman ρ=0.786，显著优于 Kermut（0.763）、DePLM（0.739）等方法；在稳定性、适应度、表达、结合、活性五个功能类别上均达到最优（ρ 分别为 0.911、0.742、0.765、0.781、0.722）。单蛋白基准（β‑内酰胺酶、GB1、荧光蛋白）的 ρ 分别达到 0.912、0.856 和 0.782，均为监督方法的最优水平。跨实验泛化测试中，RankFlow 较直接微调 ESM‑2/SaProt 回归头的 Spearman 相关系数高出约 0.05–0.10，分布外泛化优势明显。消融实验证实，移除 RC² 损失导致各功能类别 ρ 平均降低 0.02–0.06，且在高阶突变上退化尤为突出。总体而言，RankFlow 以条件流与秩一致性损失的协同，将无监督 PLM 表示转化为适应度对齐的嵌入，在排序精度与泛化能力上实现了全面突破。

## 背景与动机

蛋白质的适应度（fitness）预测——定量评估点突变或组合突变对稳定性、活性、结合等分子功能的影响——是定向进化与蛋白质工程中的核心计算任务。近年来，蛋白质语言模型（PLM）凭借在大规模序列/结构数据上的预训练，为突变效应建模提供了富有进化信息的嵌入表示，成为众多预测方法（如ProteinNPT、DePLM等）的骨干网络。然而，这类通用嵌入本身是无监督的、与具体功能属性无关的（property‑agnostic），主要编码进化保守性而非目标任务的适应度信号。当仅以少量实验标注数据对线性回归或MLP头进行微调时，极易陷入过拟合：在同一局部表示区域，高适应度突变可能被错误映射为低分，反之亦然（Figure 1a）；由此导致的泛化瓶颈在跨实验（cross‑assay）设定中尤为突出，直接限制了模型的实用价值（Figure 1b）。

另一个普遍的瓶颈在于对突变效应的独立加和假设。大多数方法（例如仅建模单点突变效应并简单求和）忽略突变间的上位效应（epistasis），即多位点突变组合间的非线性交互。由于蛋白质功能往往由残基网络协同决定，忽略这些非加性关系会严重削弱模型对高阶突变（如三重及以上突变）的排序精度，使其难以恢复真实的适应度景观。此外，训练中普遍采用的均方误差损失与基于排序（如Spearman相关系数）的评估指标不一致，进一步阻碍了模型在少样本条件下的排序学习能力。

上述问题共同指向一个需求：需要一种学习范式，既能将原始的、属性无关的PLM表示重塑为与目标属性对齐的嵌入空间，又能显式捕获突变集合内的上位交互，并直接以排序一致性为目标进行优化。本文提出的RankFlow正是围绕这一动机，通过属性感知的条件流传输与可微秩一致性损失，试图突破现有方法的局限。

## 核心创新

现有的蛋白质适应度预测方法（如微调 PLM 后接回归头）受限于两个核心瓶颈：**(1)** PLM 在掩码语言建模目标下学到的表示与下游属性（稳定性、活性等）之间缺乏显式对齐，导致回归头在局部表示空间中容易过拟合，将真正高适应度的突变体映射到低分区域（Figure 1a）；**(2)** 独立位点加和假设无法捕获突变间的上位效应（epistasis），尤其在高突变深度下，组合爆炸使得可靠监督稀缺，排序能力急剧下降。  

RankFlow 针对上述瓶颈提出了一套系统性的 **属性感知流匹配与秩一致性学习框架**，其关键创新体现在以下五个 **changed slots** 上，它们通过因果机制形成闭环，协同将无监督的 PLM 表示重塑为适应度对齐的嵌入，并保留突变之间的非加性相互作用。

### 1. 预测头架构：条件流 + PLM 对数差异头 替代 线性回归/MLP 头  
传统方法（ProteinNPT、DePLM、ESM‑2 微调等）直接将 PLM 嵌入送入线性层或 MLP，并最小化 MSE。这种设计忽视了表示空间与属性空间之间的分布偏移，且对排序不敏感。RankFlow 改用 **条件流匹配头**，训练一个以时间、突变集合和野生态上下文为条件的 U‑Net 流速场 $\mathbf{v}_\theta$（Eqs. 3, 8），将来源于 PLM 的源分布 $p_0$ 按属性感知的路径运输到对齐的目标分布 $q$。预测阶段则通过求解反向 ODE 获得属性对齐表示，再利用 **PLM 头的对数差异**（Eq. 9）求和得到突变适应度得分。  
- **证据**：Table 7 显示，RankFlow 在 ProteinGym 各功能类别上全面超越 DePLM（Stability +0.035, Fitness +0.052, Activity +0.050）。消融实验中，仅用流匹配损失（无 RC²）已超越多数基线，而单独使用流匹配头（无 PLM 头）会使 Activity ρ 从 0.722 骤降至 0.613（Table 8），证明流表示 + PLM 对数差异的组合对精确排序至关重要。

### 2. 目标损失：能量加权流匹配损失 + 可微秩一致性损失（RC²） 替代 均方误差  
MSE 对预测值的相对顺序不敏感，而蛋白质工程场景（如 DMS 筛选）的评价标准正是 Spearman 秩相关。RankFlow 引入 **可微秩一致性损失（RC², Eq. 10）**，通过软排序算子直接最大化预测排序与真实排序之间的 Spearman ρ，使训练目标与评估指标对齐。同时，**属性感知流匹配损失（$L_{\mathrm{PFM}}$, Eq. 8）** 使用能量权重 $\tilde{w}_i(t)$ 对不同突变施加差异化的匹配强度，使得高适应度突变和局部偏差大的突变获得更大的学习信号。  
- **证据**：移除 RC² 后，所有功能类别的 Spearman ρ 平均下降 0.02–0.06，尤其是 Fitness（0.742→0.702）和 Activity（0.722→0.680）下降明显（Table 8）。图 4 进一步表明，RC² 在高突变深度（≥4）上收益更大，印证了其在监管信号稀疏时的核心作用。

### 3. 突变建模方式：可学习突变集合嵌入 + U‑Net 流头 替代 独立位点加和  
以往方法通常将突变视为独立位点加和，或为每个突变学习固定嵌入后直接求和，无法捕获突变间的上下文依赖。RankFlow 采用 **可学习的突变集合嵌入**（per‑mutation embeddings），将全部突变信息作为集合输入 U‑Net 流头，使得流速场在推理时能够感知组合上位的模式；U‑Net 的下采样‑上采样结构为此提供了对长程依赖的建模能力。  
- **证据**：Figure 4 显示，在突变深度从 1 到 5+ 的变化中，RankFlow 全模型的 Spearman ρ 始终保持优势，而移除流匹配头（仅用 RC²）在高深度下性能急剧衰减，说明非加性交互的捕获主要得益于流匹配与集合建模的联合设计。

### 4. 结构信息利用：多模态融合编码器（ESM‑2 + ESM‑IF）超越 仅序列或可选结构  
为赋予条件流充分的野生态上下文，RankFlow 设计了 **多模态融合编码器**，将 ESM‑2 的序列表示与 ESM‑IF 的结构表示通过自注意力融合，生成条件向量 $[F_i; \mathbf{g}_i]$ 注入流速场（Table 6）。这一设计不仅提供了突变发生位点的空间约束，还使得模型能区分表面暴露位点与活性中心位点（Figure 3），从而更准确地判断突变的适应性后果。  
- **证据**：跨实验泛化测试中，RankFlow 比单独微调 ESM‑2 或 SaPort 回归头的 Spearman 相关度高约 0.05–0.10（Figure 1b），证实融合结构信息对分布外泛化的正向作用。

### 5. 属性对齐机制：Property-guided Steering Gate（PSG）填补 “无” 的空白  
PLM 嵌入天然携带进化保守性等与目标属性无关的信息，容易产生“野生型偏好”——即预测分数高度依赖于与野生型的序列相似度，而非真实物理化学属性。RankFlow 提出的 **PSG**（Eqs. 14‑15）计算每个位点对属性方向的投影，生成门控权重，强调与目标属性最相关的残基，抑制无关进化偏差，从而“聚焦”流的学习方向。  
- **证据**：消融实验显示，移除 PSG 后，Stability ρ 从 0.911 降至 0.902，Fitness ρ 从 0.742 降至 0.730（Table 8 部分结果）。在跨实验泛化中，PSG 帮助模型在面对未见过的新实验类型时仍能保持较高排序精度（Table 4），表明该机制有效剥离了野生型偏好，转向真正属性相关的表示。

---

**总结**：上述五个 changed slots 并非孤立改造，而是构成一条因果链——多模态编码器和 PSG 提供高质量的条件上下文；可学习突变集合嵌入和 U‑Net 流头捕获上位效应；能量函数和 RC² 损失将流匹配过程直接与排序目标对齐。整套设计使得 RankFlow 仅凭 37.1 M 可训练参数（远少于全参微调的 SaProt 650 M），在 ProteinGym 随机划分上取得 Spearman ρ=0.786，超越 SOTA 监督模型（Kermut 的 0.763），并在模数划分下将优势扩大至 +0.057（Table 2），充分验证了属性感知流与秩一致学习作为“causal knob”的有效性。

## 整体框架

![[assets/figures/papers/iclr26_0013_uS5rA4fDJp_RankFlow_Property-aware_Transport_for_Protein_Op/figures/002_Figure_1.jpg]]
*Figure 1: Illustration of RankFlow. (a) In a local region of representation space, a regression head on PLM embeddings can overfit when fine-tuned on a single assay, mapping some truly high-fitness mutants to low scores and vice versa. RankFlow instead reshapes wild-type-conditioned mutant representations into a fitness-aligned distribution, enforcing a property-aware landscape. (b) In a crossassay generalization experiment, models are trained on 40 Deep Mutational Scanning (DMS) assays from the same category and evaluated on a held-out assay; RankFlow achieves higher Spearman correlation than fine-tuned ESM2/SaProt with regression heads, indicating stronger generalization*

![[assets/figures/papers/iclr26_0013_uS5rA4fDJp_RankFlow_Property-aware_Transport_for_Protein_Op/figures/003_Figure_2.jpg]]
*Figure 2: Overview of RankFlow for protein fitness prediction. RankFlow takes wild-typeconditioned PLM representations as the source distribution $p _ { 0 }$ and learns a property-aware conditional flow (Section 3.2) that transports $p _ { 0 }$ to a property-aligned target q . The flow is conditioned on the wild type context (via the Multi-modal Fusion Encoder), the mutation set, and a Property-guided Steering Gate (Section 3.3) that emphasizes positions relevant to the target property. Training uses a dual-objective loss that combines property-aware flow matching with the rank-consistent $\mathsf { R C } ^ { 2 }$ loss*

RankFlow 的核心思想是将蛋白质语言模型（PLM）产出的无监督突变体表征视为源分布 $p_0$，通过一个条件连续流，在野生态上下文、突变集合和属性导向门控的联合引导下，将 $p_0$ 运输到与目标适应度对齐的目标分布 $q$（图 2）。这一运输过程由五个紧密耦合的模块实现，构成从序列/结构输入到排序预测的端到端管线：

1. **多模态融合编码器（Multi-modal Fusion Encoder）**：分别利用 ESM‑2（序列）和 ESM‑IF（结构）编码野生型蛋白，再经单层自注意力机制融合，输出野生态条件向量 $\mathbf{c}$（Section 3.4，Table 6）。该向量为后续流传输提供全局的结构‑序列环境。

2. **属性导向的引导门控（Property-guided Steering Gate, PSG）**：对每一位点，计算其在属性方向上的投影并生成标量门控权重 $g_i$（Eq. 14–15）。这些权重与突变集合的嵌入拼接后馈入流头，使模型聚焦于与适应度相关的残基，抑制野生型偏好和无关进化偏差。

3. **条件流头部（Conditional Flow Head）**：采用 U‑Net 1D 架构（4 下采样残差块、2 中间块、4 上采样块），以时间 $t$、突变集合嵌入 $\mathbf{F}_i$ 和门控向量 $\mathbf{g}_i$ 为条件，预测速度场 $\mathbf{v}_{\theta}$（Table 6，Algorithm 1）。该速度场通过匹配高斯条件概率路径的向量场 $u_t(h|h_0)$（Eq. 3）来参数化连续流，实现从 $h_0$ 到属性对齐表征的非线性运输。

4. **能量函数（Energy Function）**：训练时为每个突变体分配一个能量标量
   $$\mathcal{E}_i = -\big(\lambda \tilde{y}_i + (1-\lambda)\frac{\tilde{y}_i - \bar{\tilde{y}}_i}{\sqrt{s_i}}\big)\quad\text{(Eq. 7)}$$
   该能量融合了标准化全局适应度得分与局部置换模式偏差，经 softmax 转化为时间依赖的权重 $\tilde{w}_i(t)$，嵌入属性感知流匹配损失 $\mathcal{L}_{\text{PFM}}$（Eq. 8），使高适应度突变在流匹配中获得更强训练信号。

5. **秩一致性条件流损失（Rank-Consistent Conditional Flow Loss, RC²）**：为直接优化 Spearman 排序相关性，引入可微排序损失
   $$\mathcal{L}_{\text{RFlow}} = \lambda_{\text{rank}}\big(1 - \rho_{\text{soft}}(\mathbf{R}_\tau(\tilde{\mathbf{y}}), \mathbf{R}(\mathbf{y}))\big)\quad\text{(Eq. 10)}$$
   其中预测适应度 $\tilde{y}_i$ 由流运输后的表征经 PLM 头计算突变位点对数概率差异之和获得（Eq. 9）。总损失为 $\mathcal{L} = \mathcal{L}_{\text{PFM}} + \mathcal{L}_{\text{RFlow}}$（Eq. 11），同时约束样本级预测精度与批量内排序一致性。

**输入‑输出流**：管线输入为一条野生型蛋白序列及其结构（用于编码野生态上下文），以及一批由突变集合 $\boldsymbol{\mu}_i$ 定义的突变体。多模态编码器输出野生态特征作为流的起点 $h_0$；PSG 生成位点门控；条件流头以 Heun 求解器（20 步，从 $t=1$ 到 $0$）数值积分，将 $h_0$ 运输为属性对齐的表征 $h_0^{\text{tgt}}$；最后利用 PLM 头输出各突变体的 $\tilde{y}_i$，实现全排序预测。整个框架仅引入 37.1M 可训练参数（Table 4），在不微调大尺寸 PLM 的前提下，通过条件流重塑表征分布来捕获突变间的上位效应，显著提升排序精度与跨实验泛化能力。

## 核心模块与公式推导

RankFlow 的核心机制是通过一个属性感知的条件流，将突变体的 PLM 表示从无监督分布输送到与目标属性对齐的分布（Figure 2）。该框架由五个关键模块构成，下面逐一阐述其作用与对应的关键公式。

### 多模态融合编码器

为获取野生型的丰富上下文，该模块融合序列与结构信息。它使用预训练的 ESM-2（序列）和 ESM-IF（结构）分别编码野生型，然后将两部分特征通过两层 MLP（维度 1280）和一个自注意力层进行跨模态交互，最终输出维度为 1280 的条件向量（Table 6）。这一融合表示为后续的流模型提供结构‐序列耦合的上下文，使运输过程能够感知野生型的局部环境。

### 属性引导转向门（Property-guided Steering Gate, PSG）

PLM 的嵌入常携带与目标属性无关的进化偏差。PSG 的作用是筛选出对目标属性敏感的位置，具体通过计算每个位点的表示向量在属性方向上的投影，生成一个门控向量 $\mathbf{g}_i$，高值表示该位置与目标属性高度相关。门控向量与突变集合嵌入拼接后作为条件输入流头（见 Algorithm 1），从而抑制无关位点的影响并降低野生型偏好。PSG 的具体计算见原文式 (14)、(15)。

### 条件流头（U‑Net + 突变嵌入）

流头负责学习从源分布到目标分布的速度场。RankFlow 构造了一条高斯条件路径：

$$p_{t}(h\mid h_{0}) = \mathcal{N}(\mu_{t}\,h_{0},\;\sigma_{t}^{2} I) \tag{1}$$

其中 $h_{0}$ 为突变体的初始表示，$\mu_{t}$、$\sigma_{t}$ 为时间依赖的均值和标准差调度。该路径的条件向量场（即 ODE 定义的真实速度场）为：

$$u_{t}(h\mid h_{0}) = \dot{\mu}_{t}\,\mu_{t}^{-1}\,h + (\dot{\mu}_{t}\,\sigma_{t} - \mu_{t}\,\dot{\sigma}_{t})\,\sigma_{t}\,\mu_{t}^{-1}\,\nabla_{h}\log p_{t}(h\mid h_{0}) \tag{3}$$

网络 $v_{\theta}(h,t)$（即流头）的目标是逼近 $u_{t}(h\mid h_{0})$。流头采用 U‑Net1D 结构，包含 4 层下采样残差块、2 层中间残差块和 4 层上采样残差块，隐藏维度 128，输出维度 1280。它以时间 $t$、带噪的突变表示 $h_t$，以及拼接了突变集合嵌入 $\mathbf{F}_i$ 和 PSG 门控 $\mathbf{g}_i$ 的条件信息作为输入，输出预测的速度场。

为了强调当前预测高但实际可能被低估的突变，RankFlow 引入了一个基于预测分数的能量函数：

$$\mathcal{E}_{i}(h) = -\big( \lambda\,\tilde{y}_{i} + (1-\lambda)\,\frac{\tilde{y}_{i} - \bar{\tilde{y}}_{i}}{\sqrt{s_{i}}} \big) \tag{7}$$

这里 $\tilde{y}_{i}$ 为突变体的当前预测适应度；$\bar{\tilde{y}}_{i}$ 和 $s_{i}$ 分别是由基于替换的编辑距离 $d_{\mathrm{sub}}(i,j)$（式 (4)）定义的邻域内预测值的均值和方差；$\lambda \in [0,1]$ 平衡全局适应度得分与局部相对偏差。能量函数的值用于构造流匹配损失中的权重 $\tilde{w}_i(t)$（由能量导出），从而得到属性感知流匹配损失（PFM Loss）：

$$\mathcal{L}_{\mathrm{PFM}}(\boldsymbol{\theta}) = \mathbb{E}_{t,\,h,\,h_{0}}\Big[ \tilde{w}_{i}(t)\,\big\|\, v_{t}(h; \boldsymbol{\theta}) - \mathbf{u}_{t}(h \mid h_{0}) \big\|_{2}^{2} \Big] \tag{8}$$

### 秩一致性损失（RC²）与总目标

流匹配损失关注逐点精度，而蛋白质工程的核心评价指标是排序能力。为此，RankFlow 引入可微的秩一致性损失 RC²。首先，预测的适应度分数 $\tilde{y}_i$ 由流输出经 PLM 分类头计算突变位点的对数差异和得到：

$$\tilde{y}_{i} \simeq \sum_{m \in \boldsymbol{\mu}_{i}} \big( \log \tilde{Q}_{m=\mathbf{x}_{m}^{\mathrm{mt}}}^{\mathrm{tgt}} - \log \tilde{Q}_{m=\mathbf{x}_{m}^{\mathrm{wt}}}^{\mathrm{tgt}} \big) \tag{9}$$

其中 $\boldsymbol{\mu}_{i}$ 为突变位点集合，$\mathbf{x}_{m}^{\mathrm{mt}}$ 和 $\mathbf{x}_{m}^{\mathrm{wt}}$ 分别为突变型与野生型氨基酸，$\tilde{Q}^{\mathrm{tgt}}$ 为 PLM 头输出的对数概率。RC² 损失通过一个可微秩相关函数 $\rho_{\mathrm{soft}}$ 近似 Spearman 秩相关系数：

$$\mathcal{L}_{\mathrm{RFlow}}(\boldsymbol{\theta}) = \lambda_{\mathrm{rank}} \big( 1 - \rho_{\mathrm{soft}}\big( \mathbf{R}_{\tau}(\tilde{\boldsymbol{y}}),\, \mathbf{R}(\boldsymbol{y}) \big) \big) \tag{10}$$

式中 $\mathbf{R}_{\tau}(\cdot)$ 为温度 $\tau$ 的软排序操作，$\mathbf{R}(\boldsymbol{y})$ 为真实排序，$\lambda_{\mathrm{rank}}$ 控制 RC² 损失的权重。最终总损失为两者的加和：

$$\mathcal{L}(\boldsymbol{\theta}) = \mathcal{L}_{\mathrm{PFM}}(\boldsymbol{\theta}) + \mathcal{L}_{\mathrm{RFlow}}(\boldsymbol{\theta}) \tag{11}$$

联合训练使运输过程既保持局部预测精度，又强制保证全局的突变排序一致性，尤其在突变深度较高、可靠监督稀缺时作用显著（Figure 4）。通过上述模块，RankFlow 将无监督的 PLM 表示重塑为适应度对齐的嵌入，同时捕获突变间的非加性相互作用。

## 实验与分析

### 主要性能对比

**ProteinGym 基准整体表现**  
RankFlow 在 ProteinGym 的随机（Random）、模数（Modulo）和连续（Contiguous）三种评估方案下与现有最佳方法进行了系统对比。由 Table 2 可知，在 Random 方案下 RankFlow 取得 Spearman ρ = 0.786，显著优于 Kermut (0.763) 和 DePLM；在 Modulo 方案下 RankFlow 达到 0.635，较 Kermut (0.578) 提高 0.057。在 Contiguous 方案中，RankFlow 获得 0.589，排名第二，略低于 Kermut (≥0.6)，说明该方法在捕捉蛋白质家族层面的深层进化约束上仍有提升空间。

![[assets/figures/papers/iclr26_0013_uS5rA4fDJp_RankFlow_Property-aware_Transport_for_Protein_Op/figures/006_Table_2.jpg]]
*Table 2: Spearman performance on the ProteinGym benchmark under Random, Modulo, and Contiguous evaluation schemes. Results for Kermut are taken from the original paper (Groth et al., 2024), while all other baseline results are sourced from the ProteinGym website*

按功能类别的细化结果（Table 7）进一步突显了 RankFlow 的优势：稳定性（Stability）ρ = 0.911（DePLM 0.876，提升 0.035）；适应度（Fitness）ρ = 0.742（DePLM 0.690，+0.052）；表达（Expression）ρ = 0.765（DePLM 0.730，+0.035）；结合（Binding）ρ = 0.781（DePLM 0.749，+0.032）；活性（Activity）ρ = 0.722（DePLM 0.672，+0.050）。所有类别均以较大幅度超越 DePLM，且 RankFlow 的可训练参数仅为 37.1M（Table 4），远少于全量微调的 SaProt（650M），体现出模型精度与参数效率的双重优势。

![[assets/figures/papers/iclr26_0013_uS5rA4fDJp_RankFlow_Property-aware_Transport_for_Protein_Op/figures/014_Table_7.jpg]]
*Table 7: Model performance on ProteinGym. We report mean±standard deviation performance under the Random scheme*

**蛋白质工程基准**  
在 β-内酰胺酶、GB1 和荧光蛋白这三个经典适应度预测基准上，RankFlow 同样取得了领先的性能（Table 1）：Spearman ρ 分别达到 0.912、0.856 和 0.782，均为该任务上报道的最优或次优结果，验证了属性感知条件流在不同蛋白质体系上的鲁棒性。

![[assets/figures/papers/iclr26_0013_uS5rA4fDJp_RankFlow_Property-aware_Transport_for_Protein_Op/figures/005_Table_1.jpg]]
*Table 1: Spearman performance of supervised methods on β-lact., GB1, Fluo., and ProteinGym under the Random scheme. Results of CNN, ResNet, LSTM, and Transformer are from Wang et al. (2024); OHE, ESM-MSA, Tranception, and ProteinNPT are from Notin et al. (2023b). best, : second best*

**跨实验泛化能力**  
为评估模型泛化性，RankFlow 在 ProteinGym 上进行了按功能类别的留一实验（leave-one-assay-out）。Table 4 表明，RankFlow 在稳定性、适应度等类别上的 Spearman 相关性普遍高出微调 ESM2/SaProt 回归头 0.05–0.10（亦见 Figure 1(b)），表明通过条件流重塑表示分布的方式能够减轻过拟合，提升对新实验的排序预测能力。

### 消融实验

为量化各模块的贡献，我们进行了系统消融（Table 8 与 Figure 4），核心结论如下：

![[assets/figures/papers/iclr26_0013_uS5rA4fDJp_RankFlow_Property-aware_Transport_for_Protein_Op/figures/010_Figure_4.jpg]]
*Figure 4: Results of ablation study for analyzing contributions of different components. Breakdown performance on assays is grouped by (a) function type and (b) mutation depth*

- **秩一致性损失 (RC²) 的作用**：移除 RC² 损失后，各功能类别的 Spearman ρ 平均下降 0.02–0.06，尤其在突变深度 ≥ 3 的高阶突变上退化显著（Figure 4(b)）。例如，Activity ρ 从 0.722 降至 0.680，Fitness ρ 从 0.742 降至 0.702。这表明可微排序目标有效缓解了组合爆炸下监督信号稀疏的问题。
- **属性感知流匹配的必要性**：若仅使用 RC² 损失而舍弃能量引导的条件流匹配（即 L_PFM），性能大幅衰减，Activity ρ 由 0.722 跌至 0.613。反之，仅用 L_PFM 而不加 RC² 也导致排序精度明显降低。二者联合训练形成互补：流匹配负责将嵌入推至属性对齐区域，而 RC² 显式维持序列间的秩序关系。
- **能量函数设计**：消融中考察了仅用全局适应度（λ=1）、仅用局部偏差（λ=0）以及二者混合（λ=0.5）三种方案。混合策略（λ=0.5）在稳定性（0.911 vs 0.902/0.896）等类别上表现最佳（Table 5），说明同时考虑全局属性值与局部替换上下文能更精确地控制流方向。
- **其他部件**：移除属性引导门控 (PSG) 或改用线性调度均会引起小幅性能退化（Table 8），证明聚焦于目标属性相关位点以及选用余弦调度有助于模型收敛，但其影响相对次要，主要增益仍来自流匹配与 RC² 的协同。

### 不确定性估计

RankFlow 采用无侵入架构的 MC‑Dropout 与批次重采样混合策略来量化预测不确定性。Table 3 报告了在 Contiguous 和 Modulo 划分下的不确定性校准指标 ρ_uncertainty，结果显示 RankFlow 在与专门设计的贝叶斯基线（如 Stable Kermut）对比下依然具备竞争力，表明条件流头自身的采样能力即可提供合理的不确定度，为实验设计中的风险权衡提供了依据。

### 计算效率

在推理阶段，RankFlow 采用固定步数（N=20）的 Heun 二阶显式求解器，每步仅需轻型 U-Net 头（128 维隐藏）的前向传播，远低于全尺寸 PLM 的计算开销。与 DePLM 相比，RankFlow 的推理成本降低约 94.4%（证明见 fairness notes），且可训练参数仅 37.1M，保证精度的同时具备实际部署的可扩展性。

### 局限性与失败模式

1. **连续划分下的性能瓶颈**：在 Contiguous 方案中 RankFlow 仍落后于 Kermut，揭示出当前条件流尚难充分建模蛋白质家族内的深度上位效应和长期进化保守模式。
2. **对预训练模型的依赖**：RankFlow 以 PLM 的静态嵌入为源分布，当目标蛋白缺乏丰富的序列/结构同源数据时，表示质量下降会削弱属性对齐效果。
3. **静态结构信息**：融合的 ESM‑IF 仅提供静态三维上下文，无法反映突变导致的构象变化，可能遗漏影响功能的重要动态因素。
4. **极端少样本场景**：在训练样本极为有限时，流匹配与 RC² 的组合仍可能产生过拟合，未来可引入元学习或贝叶斯推断以进一步增强鲁棒性。

## 方法谱系与知识库定位

### 与现有方法的对比与改进定位

RankFlow 在蛋白质适应度预测的方法谱系中，直接回应了当前基于蛋白质语言模型（PLM）的工作所受的两个核心制约：**① PLM 表征的属性无关性**使得直接回归头容易过拟合到检测特异信号（Figure 1）；**② 多数预测器依赖独立位点加和性假设**，难以捕捉突变间的上位效应。为此，RankFlow 不再仅拟合一个从表征到分数的映射函数，而是**学习一个属性感知的条件流**（property‑aware conditional flow），将 PLM 的“野生态”突变表示运输到与目标属性对齐的分布，并以可微的秩一致性损失（RC²）强制保持排序结构。这套设计使模型在多个基准上超越了以回归或高斯过程为代表的主流基线，同时保持了极低的参数增量（约 37.1M 可训练参数，仅为全 PLM 微调的十几分之一，推理成本比 DePLM 低 94.4%）。

下表概括了 RankFlow 相对三类典型基线的方法学改造（对应原文 §3 中的关键槽位变化）：

| 设计维度 | 代表性基线 | RankFlow 的改造 | 因果机制与成效 |
|----------|------------|----------------|----------------|
| **预测头与排序目标** | 线性/MLP 回归头 + MSE（如 ESM‑2/SaProt 微调、ProteinNPT） | 条件流头（U‑Net）对突变集合嵌入输出速度场，解码后通过 PLM 头计算位点对数差异（Eq. 9），并用 RC² 损失（Eq. 10）直接优化排序 | 消除 MSE 对离群值敏感、与排名评估不一致的缺陷；在 ProteinGym 随机划分下 Spearman ρ 达 0.786，较 Kermut（0.763）和 ProteinNPT（0.701）提升显著（Table 2, confidence 0.95） |
| **突变建模方式** | 独立位点加和（DePLM 等固定嵌入） | 可学习的突变集合嵌入 + 条件流头非线性运输 | 能捕获突变间的非加性（上位）效应；消融实验表明，移除 RC² 后高阶突变上的 Spearman ρ 下降突出（Figure 4, confidence 0.9） |
| **结构信息利用** | 仅序列或可选结构（SaProt 为结构感知基线） | 双路融合编码器结合 ESM‑2（序列）与 ESM‑IF（结构），并用 Property‑guided Steering Gate（PSG）聚焦属性相关位点 | 在跨实验泛化测试中，RankFlow 比微调 ESM‑2/SaProt 的 Spearman 相关度高约 0.05–0.10（Figure 1b, confidence 0.85）；β‑内酰胺酶、GB1 和荧光蛋白上的 Spearman 分别达到 0.912、0.856、0.782，均为最优（Table 1, confidence 0.95） |
| **属性对齐机制** | 无（仅依赖 PLM 的全局进化偏差） | 能量函数（Eq. 7）结合标准化全局适应度与局部替换模式偏差，为流匹配分配样本权重；PSG 门控进一步抑制无关进化偏差 | 消融表明，能量函数中混合全局与局部信息（λ=0.5）比仅用全局（λ=1）或局部（λ=0）的稳定性 Spearman ρ 分别高 0.009 和 0.015（Table 8, confidence 0.9）；在 ProteinGym 五大功能类别上平均领先 DePLM 约 0.035–0.052（Table 7, confidence 0.9–0.95） |

值得注意的是，**在连续（Contiguous）划分下 RankFlow 略逊于基于高斯过程的 Kermut**（ρ=0.589 vs. Kermut 约 0.649，Table 2），这提示对蛋白质家族的深层进化约束建模仍有提升空间——Kermut 利用同源序列的连续信息可能更自然地捕捉家族内的保守变异模式，而 RankFlow 的条件流更侧重突变集合内的非加性交互。

### 适用边界与已知局限

综合实验证据与原文讨论，RankFlow 的效能受以下边界条件制约：

1. **预训练模型质量依赖**：所有嵌入来自冻结的 ESM‑2 和 ESM‑IF，其表征能力直接影响条件流的输入空间。当训练数据的蛋白质序列多样性不足、或目标家族与预训练语料差异大时，基础嵌入的表达力会成为性能上界（原文 §5 及公平性说明）。
2. **结构信息的静态局限**：虽然集成了 ESM‑IF 的结构嵌入，但 RankFlow 假定野生型结构固定，**不能动态建模突变引起的构象变化**，因此可能遗漏关键的功能影响（如活性口袋重排）。目前尚无构件缓解这一问题，在强构象耦合的适应度预测任务中需要手动验证。
3. **训练成本的权衡**：每个检测需要独立训练一次条件流，虽然参数仅 37.1M，但对大规模筛选场景（如涵盖数千个检测的 ProteinGym 全集），仍需可观的 GPU 内存和训练时间。原文未给出明确的奇异性讨论，但暗示可探索更轻量架构或蒸馏。
4. **连续评估方案下的排序能力**：如前所述，在突变分布主要按进化家族划分时，RankFlow 的性能不如 Kermut，表明它对“跨家族泛化”的支撑机制还不足以完全取代利用同源序列保守性的方法。

### 开放问题与潜在发展方向

从 RankFlow 的当前设计出发，以下几个方向可望拓展其方法学边界：

- **野生型偏好的进一步消减**  
  尽管 PSG 通过属性方向投影部分抑制了无关进化偏差，但在极端保守的蛋白质上，野生型得分仍可能主导预测。后续可研究基于因果表征学习的去偏策略，或在流匹配中显式建模“属性驱动”与“保守性驱动”两个解耦向量场。

- **从排序预测到生成式设计的延伸**  
  当前的条件流仅输出属性对齐的表示，间接用于分数预测。若将流的方向反转（从属性分布向序列表征分布），有望直接生成具有目标属性的新序列。这与扩散语言模型结合蛋白质设计的前沿趋势相呼应，需要解决离散序列的生成与流模型的衔接。

- **极端少样本条件下的预测鲁棒性**  
  RankFlow 通过 RC² 损失在突变深度较高时表现出优势，但在仅有极少数标记突变（如单点饱和扫描）的条件下，训练条件流可能不稳定。未来可引入元学习或贝叶斯推断组件，使模型能利用跨任务的先验适应度景观，减少对单一检测大量标注的依赖。

- **动态结构信息的注入**  
  当前所引用的结构为静态 ESM‑IF 嵌入。若结合分子动力学模拟或最近发展的蛋白质状态预测模型（如 AlphaFold 系列的构象采样），有望捕捉突变引起的局部环境重排，从而进一步提升表达、活性等功能类别的预测精度。这一方向需要设计将动态结构表征与流匹配速度场对齐的新范式。

这些开放问题既体现了 RankFlow 作为“排序引导的条件流”框架的灵活性，也揭示了其在更真实、更复杂的蛋白质工程场景中尚未覆盖的盲区。未来的跟进工作可据此在表征学习、排序目标与结构动态融合三个维度上继续深化。

## 原文 PDF

![[paperPDFs/ICLR_2026/RankFlow_Property_aware_Transport_for_Protein_Optimization.pdf]]
