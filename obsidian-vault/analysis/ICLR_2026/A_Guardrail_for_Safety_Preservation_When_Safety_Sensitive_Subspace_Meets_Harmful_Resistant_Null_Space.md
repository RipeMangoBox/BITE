---
title: "A Guardrail for Safety Preservation: When Safety-Sensitive Subspace Meets Harmful-Resistant Null-Space"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Guardrail_for_Safety_Preservation_When_Safety_Sensitive_Subspace_Meets_Harmful_Resistant_Null_Space.pdf
project_link: null
code_link: null
aliases:
- GSPWSSSMHRNS
- GuardSpace
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "通过协方差预条件奇异值分解（SVD）将预训练权重显式分解为安全相关和安全无关组件，并构建零空间投影器，将适配器更新约束在有害输入的零空间中。"
primary_logic: "安全对齐的退化源于微调更新干扰了安全相关权重组件，并改变了有害输入上的输出分布。通过冻结安全相关组件、从安全无关组件初始化适配器，并将适配器更新投影到有害输入的零空间，可以同时保持安全行为和下游任务性能。"
claims:
- "GuardSpace 在 Llama-2-7B-Chat 上微调 GSM8K 时，将平均有害分数从 14.4% 降至 3.6%，同时将准确率从 26.0% 提升至 28.0%。"
- "GuardSpace 在 Llama-2-7B-Chat 上微调 SST-2、AGNEWS 和 GSM8K 时，将平均有害分数从 8.10% 降至 2.70%，同时将平均微调准确率从 62.78% 提升至 64.36%。"
- "移除零空间投影器后，有害分数从 3.60% 飙升至 52.00%，证明投影器是安全保持的主要驱动力。"
- "SST-2 上 HS↓ = 1.20"
---

# A Guardrail for Safety Preservation: When Safety-Sensitive Subspace Meets Harmful-Resistant Null-Space

> [!tip] 核心洞察
> 安全对齐的退化源于微调更新干扰了安全相关权重组件，并改变了有害输入上的输出分布。通过冻结安全相关组件、从安全无关组件初始化适配器，并将适配器更新投影到有害输入的零空间，可以同时保持安全行为和下游任务性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 安全护栏：当安全敏感子空间遇到有害抵抗零空间 |
| 英文题名 | A Guardrail for Safety Preservation: When Safety-Sensitive Subspace Meets Harmful-Resistant Null-Space |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=887vde4ZAW) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | GuardSpace |
| Dataset | SST-2, AGNEWS |

> [!tip] 效果简介
> - SST-2 上，HS↓ 为 1.20，对比 AsFT: 3.60，变化 -2.40。
> - SST-2 上，FA↑ 为 91.50，对比 AsFT: 90.10，变化 +1.40。
> - AGNEWS 上，HS↓ 为 2.40，对比 AsFT: 5.60，变化 -3.20。

## 概要

大语言模型在微调过程中普遍面临安全对齐退化的根本瓶颈：即便采用良性数据或低秩适配（LoRA），预训练阶段注入的安全机制仍极易被破坏。现有方法未能区分安全相关与安全无关的权重组件，也无法识别有害的更新方向，导致安全保持与下游任务性能之间存在根本性冲突。

GuardSpace 通过因果性设计直接解决这一冲突。其核心洞察在于：安全对齐的退化源于微调更新干扰了安全相关权重组件，并改变了有害输入上的输出分布。方法分为两步：首先，利用协方差预条件奇异值分解（SVD）将预训练权重显式分解为安全相关（大奇异值分量）和安全无关（小奇异值分量）组件，冻结前者并从后者初始化低秩适配器；其次，构建有害输入的零空间投影器，将适配器更新约束在该空间内，使得有害输入上的输出在微调前后保持不变。

实验证据强有力地支撑了该方法。在 Llama-2-7B-Chat 上微调 GSM8K 时，GuardSpace 将平均有害分数从 14.4%（最先进方法 AsFT）降至 3.6%，同时将准确率从 26.0% 提升至 28.0%。在 SST-2、AGNEWS 和 GSM8K 三个数据集上的平均结果进一步验证了其有效性：有害分数从 8.10% 降至 2.70%，微调准确率从 62.78% 提升至 64.36%。消融研究揭示了零空间投影器的决定性作用——移除后有害分数从 3.60% 飙升至 52.00%，证明该投影器是安全保持的主要驱动力。



大语言模型（LLM）在预训练阶段通过安全对齐（如 RLHF）获得了拒绝有害请求的能力，但这一能力在微调阶段极易退化。即便使用完全良性的下游数据（如 GSM8K 数学推理、SST-2 情感分析）或采用参数高效的 LoRA 方法，微调后的模型仍可能对有害提示产生响应。现有方法（如 AsFT）尝试通过正则化约束来保持安全行为，但未能明确识别预训练权重中哪些组件与安全机制相关、哪些更新方向会破坏安全对齐，导致安全保持与下游任务性能之间存在根本性冲突。

本文的核心洞察在于：安全对齐的退化源于微调更新干扰了安全相关的权重组件，并改变了模型在有害输入上的输出分布。基于此，作者提出 GuardSpace——一种将安全保持问题分解为两个正交环节的方法：首先，通过协方差预条件奇异值分解（SVD）将预训练权重显式分解为安全相关组件（大奇异值对应的分量）和安全无关组件（小奇异值对应的分量）；然后，构建一个零空间投影器，将适配器的更新约束在有害输入的零空间内。这一设计的因果机制在于：冻结安全相关组件保留了原始的安全机制，从安全无关组件初始化适配器确保了训练起点不破坏安全行为，而零空间投影器则保证在整个微调过程中，适配器更新在有害输入上的净效果为零，从而维持输出分布不变。

实验证据有力地支撑了这一设计。在 Llama-2-7B-Chat 上的主实验（Table 1）显示，GuardSpace 在 SST-2、AGNEWS 和 GSM8K 三个数据集上将平均有害分数从基线 AsFT 的 8.10% 降至 2.70%，同时将平均微调准确率从 62.78% 提升至 64.36%。消融研究（Table 4）进一步揭示了零空间投影器的关键作用：移除投影器后，有害分数从 3.60% 飙升至 52.00%，证明投影器是安全保持的主要驱动力。此外，适配器秩的选择（Appendix B.3）表明，使用少量安全无关组件（r=128–512）即可保持低有害分数和高准确率，而过大的 r（1024）会导致安全退化，这验证了安全相关与安全无关组件分离的有效性。



## 核心方法与创新机理

GuardSpace 的核心创新在于将安全保持的瓶颈从“隐式正则化”转向“显式子空间隔离与约束”。现有方法（如 LoRA、AsFT）未能明确识别安全相关的权重组件或有害的更新方向，导致安全保持与下游任务性能之间存在冲突。GuardSpace 通过以下三个关键创新点解决了这一问题：

**1. 安全敏感子空间的显式分解与冻结**

- **瓶颈**：微调过程中，预训练的安全对齐极易退化，因为微调更新会干扰安全相关权重组件，并改变有害输入上的输出分布。现有方法（如 LoRA）允许所有权重可学习，未显式分离安全相关组件。
- **创新**：通过协方差预条件奇异值分解（SVD）将预训练权重显式分解为安全相关和安全无关组件。具体地，使用有害提示集收集激活值，计算协方差矩阵 $\mathbf{C} = \mathbf{X} \mathbf{X}^\top$，然后对 $\mathbf{WC}$ 进行 SVD 分解：$\operatorname{SVD}(\mathbf{WC}) = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^T$。大奇异值对应的分量构成安全相关子空间（冻结），小奇异值对应的分量构成安全无关子空间（用于初始化适配器）。
- **证据强度**：高。该方法在 Llama-2-7B-Chat 上微调 GSM8K 时，将平均有害分数从 14.4% 降至 3.6%，同时将准确率从 26.0% 提升至 28.0%（Abstract）。消融实验表明，使用安全无关组件初始化（无投影器）相比标准 LoRA 降低了 HS，但不如完整 GuardSpace 有效（Table 4）。

**2. 有害抵抗零空间的构建与投影约束**

- **瓶颈**：即使初始化良好，微调过程中的梯度更新仍可能偏离安全区域。现有方法（如 AsFT）使用软正则化，但无法保证有害输入上的输出不变性。
- **创新**：对协方差矩阵 $\mathbf{C}$ 进行特征分解：$\mathbf{C} = \mathbf{Q} \boldsymbol{\Lambda} \mathbf{Q}^\top$，从零特征值对应的特征向量构建投影器 $\mathbf{P} = \hat{\mathbf{Q}} \hat{\mathbf{Q}}^\top$。在微调过程中，将适配器更新约束在有害输入的零空间中，确保对于有害输入 $\mathbf{X}$，适配器更新项被零化：$(\mathbf{W}' + \mathbf{B}^* \mathbf{A}^* \mathbf{P}) \mathbf{X} = \mathbf{W}' \mathbf{X}$，输出仅由冻结的安全相关权重决定。
- **证据强度**：极高。消融实验显示，移除零空间投影器后，有害分数从 3.60% 飙升至 52.00%，证明投影器是安全保持的主要驱动力（Table 4）。该投影器在不同有害数据集（AdvBench, MaliciousInstruct, SafeEdit）上均能保持低 ASR，证明其泛化性（Table 7）。

**3. 适配器初始化与优化约束的协同设计**

- **瓶颈**：单独使用安全无关组件初始化或零空间投影器均无法达到最佳效果。初始化确保模型在步骤 0 时安全，但后续更新可能偏离；投影器确保更新不破坏安全，但若初始化不当，初始输出可能已有偏移。
- **创新**：将两个组件协同设计：从安全无关组件（最小 r 个奇异值对应的分量）初始化低秩适配器 $\mathbf{B} = \mathbf{U}[:, -r:] \sqrt{\boldsymbol{\Sigma}[-r:]}, \quad \mathbf{A} = \sqrt{\boldsymbol{\Sigma}[-r:]} (\mathbf{V}^\top \mathbf{C}^{-1})[-r:, :]$（Eq. (5)），并在优化过程中通过投影器 $\mathbf{P}$ 约束更新。这种协同设计使模型在步骤 0 即安全，且在整个训练过程中保持安全。
- **证据强度**：高。在 Llama-2-7B-Chat 上微调 SST-2、AGNEWS 和 GSM8K 时，GuardSpace 将平均有害分数从 8.10% 降至 2.70%，同时将平均微调准确率从 62.78% 提升至 64.36%（Table 1）。使用少量安全无关组件（r=128–512）可保持低 HS 和高 ACC，而过大的 r（1024）会导致 HS 飙升（Appendix B.3）。

**与其他方法的本质区别**：GuardSpace 将安全保持问题从“正则化”范式（如 AsFT 的软约束）转变为“子空间隔离与硬约束”范式。它显式识别并冻结安全相关权重，将可学习容量限制在安全无关子空间，并通过零空间投影器确保更新不改变有害输入上的输出。这种设计不仅保持了安全行为，还通过减少训练冲突提升了下游任务性能。



![[assets/figures/papers/iclr26_0002_887vde4ZAW_A_Guardrail_for_Safety_Preservation_When_Safety-/figures/001_Figure_1.jpg]]
*Figure 1: An overview of GuardSpace. The model is first probed with safety-triggering prompts to obtain the activation X and the covariance matrix $\mathbf { C } = \mathbf { X } \mathbf { X } ^ { \top }$ . I. Initialization in safety-sensitive subspace. We right-precondition the weight by C and factorize $\mathbf { W } \mathbf { C } = \mathbf { U } \mathbf { \Sigma } \mathbf { \Sigma } \mathbf { V } ^ { \top }$ The components with large singular values constitute the safety-relevant subspace (cyan) and are frozen into W′, while the components with small singular values form the safety-irrelevant subspace (blue) and are used to initialize low-rank adapters (A, B). II. Optimization in harmful-resistant nul...

GuardSpace 采用两阶段流水线，将安全保持与下游适配解耦。第一阶段（初始化）通过协方差预条件奇异值分解（SVD）将预训练权重显式分解为安全相关和安全无关组件，并从安全无关组件初始化低秩适配器，同时冻结安全相关组件。第二阶段（优化）构建一个零空间投影器，将适配器更新约束在有害输入的零空间中，从而在微调过程中保持安全行为。

**输入输出流**：输入为预训练模型权重 W 和一组安全触发提示（有害提示）。通过前向传播获取这些提示在特定层（如注意力投影层）的激活值 X，计算协方差矩阵 C = X X^⊤。对 WC 进行 SVD 分解：SVD(WC) = U Σ V^T，将大奇异值对应的分量标记为安全相关（冻结），小奇异值对应的分量标记为安全无关（用于初始化）。同时，对 C 进行特征分解：C = Q Λ Q^⊤，从零特征值对应的特征向量构建投影器 P = Q̂ Q̂^⊤。微调时，适配器更新被投影到零空间：对于有害输入 X，有 (W' + B* A* P) X = W' X，即输出完全由冻结的安全相关权重决定。输出为微调后的模型，在保持与预训练模型相当的安全水平（平均有害分数 2.70% vs. 基础模型 4.40%）的同时，在下游任务上获得平均 +29.74% 的准确率提升。

**模块关系**：安全敏感子空间分解与零空间投影器构建是并行的预计算步骤，两者共同作用于微调过程。安全相关组件的冻结确保了安全机制不被破坏，而零空间投影器则防止适配器更新改变有害输入上的输出分布。消融实验表明，移除零空间投影器后，有害分数从 3.60% 飙升至 52.00%，证明投影器是安全保持的主要驱动力。适配器初始化从安全无关组件开始，与零空间投影器协同工作：模型在步骤 0 即安全，并在整个训练过程中保持安全。

**关键公式**：低秩适配器初始化 B = U[:, -r:] √(Σ[-r:]), A = √(Σ[-r:]) (V^T C^{-1})[-r:, :]；零空间投影器 P = Q̂ Q̂^⊤；有害输入上的零化效果 (W' + B* A* P) X = W' X。



GuardSpace 的核心在于将微调过程分解为两个解耦的阶段：**安全敏感子空间中的初始化** 与 **有害抵抗零空间中的优化**。其底层逻辑是：预训练安全对齐的退化源于微调更新干扰了与安全行为强相关的权重组件，并改变了模型在有害输入上的输出分布。GuardSpace 通过显式分离这些组件并约束更新方向来阻断这一因果链。

### 1. 问题形式化与 LoRA 基线

GuardSpace 建立在 LoRA 微调框架之上。标准 LoRA 将权重更新表示为低秩矩阵的乘积：

$$\mathbf{W}^* = \mathbf{W} + \Delta \mathbf{W} = \mathbf{W} + \mathbf{B}^* \mathbf{A}^*$$

其中 $\mathbf{W} \in \mathbb{R}^{m \times n}$ 是冻结的预训练权重，$\mathbf{B}^* \in \mathbb{R}^{m \times r}$ 和 $\mathbf{A}^* \in \mathbb{R}^{r \times n}$ 是可学习的低秩适配器，$r \ll \min(m, n)$。

安全保持的微调可以形式化为一个约束优化问题：在最小化下游任务损失的同时，约束模型在有害提示集 $\mathcal{H}$ 上的输出变化：

$$\underset{\Delta}{\operatorname*{min}} \mathcal{L}_{\mathrm{task}}(f_{\mathbf{W}+\Delta}; \mathcal{D}), \quad \mathrm{s.t.} \quad \|f_{\mathbf{W}+\Delta}(x) - f_{\mathbf{W}}(x)\| \leq \epsilon, \quad \forall x \in \mathcal{H}$$

该公式体现了安全保持的核心矛盾：任务性能提升（最小化 $\mathcal{L}_{\mathrm{task}}$）与安全行为保持（约束有害输入上的输出偏差）之间的权衡。GuardSpace 通过结构化的初始化与投影约束来近似求解此问题。

### 2. 安全敏感子空间分解与适配器初始化（模块 I）

该模块的目标是识别权重矩阵中与安全行为相关的组件，并将可训练容量分配至安全无关的组件。

**步骤 1：协方差矩阵计算。** 首先，使用一组安全触发提示（有害提示）收集模型中间层的激活值 $\mathbf{X} \in \mathbb{R}^{n \times N}$（$N$ 为 token 总数），计算其协方差矩阵：

$$\mathbf{C} = \mathbf{X} \mathbf{X}^\top$$

$\mathbf{C}$ 编码了有害输入激活的主要方向。

**步骤 2：预条件奇异值分解（SVD）。** 对权重矩阵与协方差矩阵的乘积进行 SVD：

$$\operatorname{SVD}(\mathbf{WC}) = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^T = \sum_{i=1}^R \sigma_i \mathbf{u}_i \mathbf{v}_i^T$$

关键洞察在于：右乘 $\mathbf{C}$ 相当于对权重矩阵进行“预条件”，使得分解出的奇异向量能够反映权重对有害输入激活的响应程度。**大奇异值** $\sigma_i$ 对应的分量 $\mathbf{u}_i \mathbf{v}_i^T$ 对有害输入的输出贡献最大，因此被识别为 **安全相关组件**；**小奇异值** 对应的分量则被认为是 **安全无关组件**。

**步骤 3：权重重构与冻结。** 为了保持预训练输出不变，重构权重矩阵：

$$\hat{\mathbf{W}} = \operatorname{SVD}(\mathbf{WC}) \mathbf{C}^{-1} = \mathbf{U} \boldsymbol{\Sigma} (\mathbf{V}^T \mathbf{C}^{-1}) = \sum_{i=1}^R \sigma_i \mathbf{u}_i \hat{\mathbf{v}}_i^T$$

其中 $\hat{\mathbf{v}}_i^T$ 是 $\mathbf{V}^T \mathbf{C}^{-1}$ 的行向量。GuardSpace 冻结前 $R-r$ 个安全相关分量，构成 $\mathbf{W}'$。

**步骤 4：低秩适配器初始化。** 从最小的 $r$ 个奇异值对应的安全无关分量中提取适配器 $\mathbf{A}$ 和 $\mathbf{B}$：

$$\mathbf{B} = \mathbf{U}[:, -r:] \sqrt{\boldsymbol{\Sigma}[-r:]}, \quad \mathbf{A} = \sqrt{\boldsymbol{\Sigma}[-r:]} (\mathbf{V}^\top \mathbf{C}^{-1})[-r:, :]$$

此初始化确保：1) 适配器的初始权重落在安全无关子空间中；2) 初始输出 $\mathbf{B}^* \mathbf{A}^*$ 为零（因为 $\mathbf{A}$ 和 $\mathbf{B}$ 从同一组奇异值分解中提取，其乘积在初始时与 $\mathbf{W}'$ 互补，但通过训练会偏离）。这一初始化使得模型在训练第 0 步即具备安全行为。

### 3. 有害抵抗零空间投影与优化（模块 II）

该模块的目标是在微调过程中，将适配器的参数更新约束在有害输入的零空间中，从而避免改变模型对有害提示的输出。

**步骤 1：零空间构建。** 对协方差矩阵 $\mathbf{C}$ 进行特征分解：

$$\mathbf{C} = \mathbf{Q} \Lambda \mathbf{Q}^\top$$

由于 $\mathbf{C} = \mathbf{X} \mathbf{X}^\top$，$\mathbf{C}$ 的零空间与 $\mathbf{X}^\top$ 的左零空间相同，即 $\mathcal{N}(\mathbf{X}^\top) = \mathcal{N}(\mathbf{C})$。零空间中的向量 $\mathbf{z}$ 满足 $\mathbf{X} \mathbf{z} = \mathbf{0}$。

**步骤 2：投影器构造。** 令 $\hat{\mathbf{Q}}$ 包含 $\mathbf{C}$ 的零特征值对应的特征向量，则零空间投影器为：

$$\mathbf{P} = \hat{\mathbf{Q}} \hat{\mathbf{Q}}^\top$$

该投影器将任意向量投影到有害输入的零空间中。

**步骤 3：约束优化。** 在微调过程中，将适配器的输出通过投影器 $\mathbf{P}$ 进行约束：

$$(\mathbf{W}' + \mathbf{B}^* \mathbf{A}^* \mathbf{P}) \mathbf{X} = \mathbf{W}' \mathbf{X}$$

对于有害输入 $\mathbf{X}$，由于 $\mathbf{P} \mathbf{X} = \mathbf{0}$，适配器更新项 $\mathbf{B}^* \mathbf{A}^* \mathbf{P}$ 被完全零化，输出仅由冻结的安全相关权重 $\mathbf{W}'$ 决定。对于良性输入（不在 $\mathcal{H}$ 中），投影器不会将其置零，因此适配器可以自由学习下游任务。

### 4. 关键公式与变量含义汇总

| 公式 | 变量含义 | 核心作用 |
|---|---|---|
| $\mathbf{C} = \mathbf{X} \mathbf{X}^\top$ | $\mathbf{X}$: 有害提示的激活值矩阵 | 编码有害输入的主要激活方向 |
| $\operatorname{SVD}(\mathbf{WC}) = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^T$ | $\mathbf{W}$: 预训练权重；$\sigma_i$: 奇异值 | 识别安全相关（大 $\sigma_i$）与安全无关（小 $\sigma_i$）组件 |
| $\mathbf{B} = \mathbf{U}[:, -r:] \sqrt{\boldsymbol{\Sigma}[-r:]}$ | $r$: 适配器秩；$\boldsymbol{\Sigma}[-r:]$: 最小 $r$ 个奇异值 | 从安全无关组件初始化适配器 |
| $\mathbf{P} = \hat{\mathbf{Q}} \hat{\mathbf{Q}}^\top$ | $\hat{\mathbf{Q}}$: $\mathbf{C}$ 零特征值对应的特征向量 | 构建零空间投影器 |
| $(\mathbf{W}' + \mathbf{B}^* \mathbf{A}^* \mathbf{P}) \mathbf{X} = \mathbf{W}' \mathbf{X}$ | $\mathbf{W}'$: 冻结的安全相关权重 | 证明有害输入上适配器更新被零化 |

**关键机制总结：** GuardSpace 通过两个互补的机制实现安全保持。**初始化机制**（模块 I）确保可训练容量初始时位于安全无关子空间，从起点避免安全退化。**投影机制**（模块 II）在整个训练过程中动态约束参数更新，确保安全行为不会被后续的梯度更新破坏。消融实验证实，移除投影器后有害分数从 3.60% 飙升至 52.00%，表明投影器是安全保持的主要驱动力。



## 实验与关键发现

### 主实验结果

GuardSpace 在三个下游任务（SST-2、AGNEWS、GSM8K）上对 Llama-2-7B-Chat 进行了评估，并与标准 LoRA 和最先进的安全保持方法 AsFT 进行了对比。实验结果（Table 1）表明，GuardSpace 在所有任务上均实现了最低的有害分数（HS）和最高的微调准确率（FA）。具体而言，在 GSM8K（数学推理）上，GuardSpace 将平均有害分数从 AsFT 的 14.4% 大幅降至 3.6%，同时将准确率从 26.0% 提升至 28.0%。在三个任务的平均表现上，GuardSpace 将平均 HS 从 AsFT 的 8.10% 降至 2.70%，并将平均 FA 从 62.78% 提升至 64.36%。值得注意的是，GuardSpace 的安全水平（平均 HS 2.70%）甚至优于未微调的基础模型（平均 HS 4.40%），同时在下游任务上获得了 +29.74% 的效用提升。这验证了其核心设计：通过显式分离安全相关和安全无关组件，并约束更新方向，有效缓解了安全保持与任务性能之间的冲突。

![[assets/figures/papers/iclr26_0002_887vde4ZAW_A_Guardrail_for_Safety_Preservation_When_Safety-/figures/002_Table_1.jpg]]
*Table 1: Performance of Llama-2-7B-Chat fine-tuned on different datasets. HS↓ indicates lower is better; FA↑ indicates higher is better. Best results are shown in bold; second-best results are underlined*

### 跨模型与跨数据集的泛化性

GuardSpace 在 Qwen-2-7B-Instruct、Gemma-2-9B-IT 和 Mistral-7B-Instruct 三种不同架构上进行了 GSM8K 微调测试（Table 2）。在所有模型上，GuardSpace 均取得了最低或接近最低的 HS，同时保持了有竞争力的 FA。例如，在 Qwen-2-7B-Instruct 上，GuardSpace 的 HS 为 12.80%，远低于 LoRA 的 49.20% 和 AsFT 的 33.60%，而 FA（70.00%）与 LoRA（70.20%）相当。在 AGNEWS 任务上的跨模型评估（Table 6）进一步证实了这一趋势：GuardSpace 在三个模型上的平均 HS 为 6.67%，平均 FA 为 88.30%，而 LoRA 的平均 HS 高达 43.47%。这表明 GuardSpace 的安全保持机制在不同模型架构和任务上具有良好的泛化性。

![[assets/figures/papers/iclr26_0002_887vde4ZAW_A_Guardrail_for_Safety_Preservation_When_Safety-/figures/003_Table_2.jpg]]
*Table 2: Performance of different model architectures on GSM8K. HS↓ (lower is better); FA↑ (higher is better)*

### 有害数据比例的鲁棒性

在 GSM8K 训练数据中混入不同比例（0%–10%）的有害数据（poisoned data）时（Table 3），GuardSpace 表现出极强的鲁棒性。在所有有害比例下，GuardSpace 的平均 HS 仅为 2.56%，而 LoRA 和 AsFT 的 HS 随有害比例增加而急剧上升（例如，在 10% 有害比例下，LoRA 的 HS 高达 68.40%）。GuardSpace 的 FA 在所有比例下保持稳定（平均 25.88%），表明其零空间投影器能有效防止有害数据对安全行为的侵蚀，同时不影响任务学习。

![[assets/figures/papers/iclr26_0002_887vde4ZAW_A_Guardrail_for_Safety_Preservation_When_Safety-/figures/004_Table_3.jpg]]
*Table 3: Performance of Llama-2-7B-Chat on GSM8K under varying unsafe ratios*

### 消融研究

消融实验（Table 4）揭示了 GuardSpace 各组件的关键作用：
- **零空间投影器**是安全保持的主要驱动力。移除投影器后，HS 从 3.60% 飙升至 52.00%，证明仅靠安全无关初始化不足以维持安全行为。
- **安全无关初始化**（无投影器）相比标准 LoRA 降低了 HS（从 52.00% 降至 14.40%），但远不如完整 GuardSpace 有效。
- **适配器秩 r 的影响**（Appendix B.3, Figure 4）：使用少量安全无关组件（r=128–512）可保持低 HS 和高 ACC；当 r 过大（如 1024）时，HS 急剧上升，因为过多的可学习参数开始干扰安全相关子空间。
- **零空间投影器的泛化性**（Table 7）：在不同有害数据集（AdvBench, MaliciousInstruct, SafeEdit）上，GuardSpace 均能保持低 ASR（平均 5.62%），证明其不依赖于特定有害提示集。

![[assets/figures/papers/iclr26_0002_887vde4ZAW_A_Guardrail_for_Safety_Preservation_When_Safety-/figures/005_Table_4.jpg]]
*Table 4: Ablation study of GuardSpace across models and datasets*

### 表示偏移分析

Figure 5 展示了不同微调方法下模型表示（representation）的偏移量。标准 LoRA 和 AsFT 在微调后，模型在有害输入上的表示发生了显著偏移，导致安全行为退化。而 GuardSpace 的表示偏移极小，几乎与基础模型一致。这从机制上验证了：零空间投影器将适配器更新约束在有害输入的零空间中，从而保证了有害输入上的输出不变性（公式：$(W' + B^* A^* P)X = W' X$）。

### 边界安全查询与通用知识保持

- **边界安全查询**（Appendix C.3）：GuardSpace 在边界安全查询上不会过度拒绝，而是提供上下文适当的拒绝和建设性建议，表明其不会降低模型在模糊安全场景下的有用性。
- **MMLU 评估**（Table 9）：GuardSpace 的平均准确率（45.79）与基础模型几乎相同，且高于 LoRA（45.02）和 AsFT（44.68），表明安全保持不会损害通用知识能力。

### 失败模式与局限性

- **有害提示集的依赖**：GuardSpace 需要访问有害提示集来构建协方差矩阵和零空间投影器。在实际部署中，这可能需要人工收集或依赖公开数据集。
- **分布外有害输入的泛化性**：零空间投影器的有效性依赖于有害提示集能够充分覆盖安全相关子空间。Table 8 的 OOD 评估显示，在语义不相关有害数据集上，GuardSpace 的 HS（0.59）仍远低于 LoRA（21.18），但略高于基础模型（0.00），表明存在一定的泛化边界。
- **预计算开销**：在 7B-9B 模型上，GuardSpace 的预计算阶段（SVD 和特征分解）需要约 17 分钟和 58 GB 内存（Table 10），可能对资源受限场景构成挑战。
- **适配器秩的选择**：r 过小可能限制下游任务性能，过大则导致安全退化。当前缺乏自动选择最优 r 的机制。

### 补充图表

![[assets/figures/papers/iclr26_0002_887vde4ZAW_A_Guardrail_for_Safety_Preservation_When_Safety-/figures/008_Table_5.jpg]]
*Table 5: Models used in our experiments and their official sources*



## 定位与知识库关联

GuardSpace 的提出直接回应了“微调导致安全对齐退化”这一核心瓶颈。其因果机制在于：微调更新会干扰预训练模型中与安全机制强相关的权重组件，并改变模型在有害输入上的输出分布。现有方法（如 LoRA、AsFT）未能显式识别这些安全敏感组件，导致安全保持与下游任务性能之间存在冲突。

**与基线方法的关系**：GuardSpace 在 LoRA 框架上做了两项关键改动。第一，适配器初始化从零初始化（LoRA）或随机初始化变为从预训练权重的安全无关组件（协方差预条件 SVD 分解后最小 r 个奇异值对应的分量）初始化，同时冻结安全相关组件（大奇异值分量）。第二，在优化过程中引入零空间投影器 **P**，将适配器更新严格约束在有害输入的零空间中，使得对于有害输入 **X**，有 **(W' + B\*A\*P)X = W'X**，即输出完全由冻结的安全相关权重决定。消融实验（Table 4）证实，移除该投影器后，有害分数从 3.60% 飙升至 52.00%，说明投影器是安全保持的主要驱动力，而仅使用安全无关组件初始化（无投影器）虽然优于标准 LoRA，但效果远不及完整方法。

**与最先进方法 AsFT 的比较**：在 Llama-2-7B-Chat 上，GuardSpace 在 SST-2、AGNEWS 和 GSM8K 三个数据集上将平均有害分数从 AsFT 的 8.10% 降至 2.70%，同时将平均微调准确率从 62.78% 提升至 64.36%（Table 1）。在 GSM8K 上改善尤为显著（HS 从 14.4% 降至 3.6%，准确率从 26.0% 提升至 28.0%）。跨模型泛化实验（Table 2）显示，GuardSpace 在 Qwen-2-7B-Instruct、Gemma-2-9B-IT、Mistral-7B-Instruct 上均取得最低或接近最低的 HS，同时保持有竞争力的 FA。MMLU 评估（Table 9）表明，GuardSpace 的平均准确率（45.79）与基础模型几乎相同，且高于 LoRA 和 AsFT，说明安全保持不会损害通用知识能力。

**适用边界与条件**：该方法需要访问有害提示集来构建协方差矩阵和零空间投影器。实验表明，投影器在分布内有害数据上效果显著（Table 7 中平均 ASR 仅 5.62%），在语义不相关的分布外有害数据上也能保持低 HS（Table 8 中 HS 为 0.59），但泛化性上限尚未充分刻画。适配器秩 r 是关键超参数：r=128–512 可保持低 HS 和高 ACC，而 r=1024 会导致 HS 飙升（Appendix B.3）。预计算阶段（SVD 和特征分解）在 7B-9B 模型上需要约 17 分钟和 58 GB 内存，对资源受限场景构成挑战。

**局限与开放问题**：
1. **有害提示依赖**：该方法依赖有害提示集来构建投影器，在实际部署中可能难以收集或覆盖所有安全相关子空间。能否设计无需有害提示集的零空间投影器构建方法是一个开放问题。
2. **秩选择缺乏自动化**：适配器秩 r 的选择需要手动权衡安全保持与任务性能，目前缺乏自动选择最优 r 的准则。
3. **方法扩展性**：零空间投影器能否扩展到其他参数高效微调方法（如 Adapter、Prefix Tuning）尚未验证。
4. **大规模模型适用性**：GuardSpace 在 70B+ 模型上的计算开销和有效性有待验证。
5. **长训练稳定性**：消融实验（Appendix B.2）显示，无投影器时 ASR 在 7 个 epoch 后急剧上升（超过 20%），而 GuardSpace 在 10 个 epoch 内保持低 ASR，但更长训练场景下的行为未探索。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Guardrail_for_Safety_Preservation_When_Safety_Sensitive_Subspace_Meets_Harmful_Resistant_Null_Space.pdf

![[paperPDFs/ICLR_2026/A_Guardrail_for_Safety_Preservation_When_Safety_Sensitive_Subspace_Meets_Harmful_Resistant_Null_Space.pdf]]
