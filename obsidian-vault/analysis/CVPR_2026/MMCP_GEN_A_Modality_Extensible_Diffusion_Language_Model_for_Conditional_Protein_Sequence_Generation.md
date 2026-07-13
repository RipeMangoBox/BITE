---
title: "MMCP-GEN: A Modality-Extensible Diffusion Language Model for Conditional Protein Sequence Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MMCP_GEN_A_Modality_Extensible_Diffusion_Language_Model_for_Conditional_Protein_Sequence_Generation.pdf
project_link: null
code_link: null
aliases:
- MG
- MMCP-GEN
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入一个模态可组合且可扩展的条件化机制，通过模态指示头（MMCP-IH）保留模态身份，并通过可学习查询融合模块（MMCP-LQ）进行跨模态特征提取，实现无需重新训练骨干的新模态集成。
primary_logic: 将异构生物条件投影到共享的、模态解耦的表示空间中，利用可学习查询进行跨模态特征聚合，同时保持模态独立性，从而在不动扩散模型骨干的情况下实现可扩展的多模态控制。
claims:
- MMCP-GEN通过可组合和可扩展的条件化机制将结构、功能、配体等条件融合，不需要重新训练骨干网络。
- MMCP-GEN在多种任务上实现最先进的性能，序列恢复率提升最高达5%。
- 联合生成–评分目标进一步对齐序列恢复与结构保真度。
- 新模态的引入只需要轻量投影器和少量查询，无需修改骨干网络。
---

# MMCP-GEN: A Modality-Extensible Diffusion Language Model for Conditional Protein Sequence Generation

> [!tip] 核心洞察
> 将异构生物条件投影到共享的、模态解耦的表示空间中，利用可学习查询进行跨模态特征聚合，同时保持模态独立性，从而在不动扩散模型骨干的情况下实现可扩展的多模态控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | MMCP-GEN: 一种模态可扩展的扩散语言模型用于条件蛋白质序列生成 |
| 英文题名 | MMCP-GEN: A Modality-Extensible Diffusion Language Model for Conditional Protein Sequence Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/An_MMCP-GEN_A_Modality-Extensible_Diffusion_Language_Model_for_Conditional_Protein_Sequence_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | MMCP-GEN |
| Dataset | Curated multimodal protein dataset, CATH |
> [!tip] 效果简介
> - 逆折叠 (Inverse Folding) 上，AAR (氨基酸恢复率) 78.66% vs ProteinMPNN / CFP-GEN (提升最高达5% (best in class))。
> - 功能注释 (EC编号) 评估 上，MRR (平均倒数排名) 0.927 vs DPLM / CFP-GEN / ESM3 (显著优于所有基线)。
> - 新折叠推断 (>400 残基) 上，pdb-TM (与PDB的TM-score) 改善 ~0.05 TM vs DPLM / UR50 (pdb-TM 降低约 0.05)。

## 概要

蛋白质序列的条件生成是可控蛋白质设计的核心问题，其目标是在给定结构、功能、配体等生物条件约束下，生成满足相应性质的新蛋白质序列。当前主流方法——包括基于扩散的蛋白质语言模型**DPLM**（Wang et al., ICML 2024）、大规模蛋白质语言模型**ESM3**（Hayes et al., Science 2025）以及组合功能生成模型**CFP-GEN**（Yin et al., ICML 2025）——通常仅支持单一模态条件，或采用分离的模态特定编码器独立处理各条件信号。这种设计导致跨模态交互受限，且每次引入新模态都需要重新设计架构甚至重新训练骨干网络，严重制约了多模态蛋白质设计的灵活性和可扩展性。

针对上述瓶颈，MMCP-GEN 提出了一种模态可组合且可扩展的条件化机制。其核心洞察在于：将异构生物条件投影到共享的、模态解耦的表示空间中，通过可学习查询进行跨模态特征聚合，同时借助模态指示头保持模态独立性，从而在不修改扩散模型骨干的情况下实现可扩展的多模态控制。具体而言，MMCP-GEN 包含两个关键创新模块：**MMCP-IH**（模态指示头）为每个模态附加可学习的身份标识，保留模态语义的独立性；**MMCP-LQ**（可学习查询融合模块）通过共享查询和模态特定查询联合处理多模态 token，生成紧凑的条件表示以指导离散扩散过程。此外，**MMCP-GS**（联合生成-评分目标）通过 InfoNCE 损失最大化生成序列与真实结构嵌入之间的互信息，进一步对齐序列恢复与结构保真度。

当引入新条件模态时，MMCP-GEN 仅需接入一个冻结的预训练编码器、一个轻量投影器和少量模态特定查询，并在保持扩散语言模型骨干及所有编码器完全冻结的情况下进行微调，无需大规模重新训练。

在实验验证方面，MMCP-GEN 在多个任务上取得领先性能：在逆折叠任务上，氨基酸恢复率（AAR）达到 78.66%，较**ProteinMPNN**（Dauparas et al., Science 2022）和 CFP-GEN 等基线提升最高达 5%；在功能注释评估中，平均倒数排名（MRR）达到 0.927，显著优于 DPLM、CFP-GEN 和 ESM3；联合生成-评分损失将逆折叠 AAR 从 78.17% 提升至 78.66%，结构质量指标 scTM 从 0.906 提升至 0.912。多模态消融实验进一步证实，融合结构、配体、功能和文本全部模态相比仅使用部分模态，在 GO、IPR、EC 等功能注释指标上均带来显著增益。

蛋白质序列设计是合成生物学的核心问题，其目标是根据给定的生物条件生成满足特定结构、功能或结合要求的氨基酸序列。近年来，深度生成模型在该领域取得了显著进展，尤其是基于蛋白质语言模型（PLM）和扩散模型的方法，如 **DPLM**（Wang et al., ICML 2024）、**ESM3**（Hayes et al., Science 2025）和 **CFP-GEN**（Yin et al., ICML 2025），已展现出强大的序列生成能力。

然而，现有方法存在一个关键瓶颈：**条件化机制对模态的扩展性不足**。当前的可控蛋白质生成方法通常仅支持单一模态条件（如仅结构或仅功能标签），或采用分离的模态特定编码器–适配器对。这种设计导致两个严重后果：

1. **跨模态交互受限**：各模态被独立编码后直接注入生成器，缺乏显式的跨模态特征融合，无法捕捉不同生物条件之间的互补信息，从而降低生成质量。
2. **架构扩展代价高昂**：每引入一种新模态（如配体、文本描述、功能注释），都需要重新设计编码器–适配器对，甚至重新训练整个生成骨干网络。这严重制约了模型在真实生物设计场景中的灵活性和实用价值。

以 **DPLM** 为例，其条件控制依赖特定适配器，模态之间相互隔离；**CFP-GEN** 虽支持功能条件，但同样缺乏对多模态的统一处理框架。**ProteinMPNN**（Dauparas et al., Science 2022）专注于逆折叠任务，仅接受结构条件，无法扩展到其他模态。

上述缺口指向一个明确的研究动机：**能否构建一种模态可组合且可扩展的条件化机制，使得在不修改扩散模型骨干的前提下，灵活集成异构生物条件，并实现跨模态特征的深度融合？**

MMCP-GEN 正是针对这一问题提出的解决方案。其核心思路是将异构生物条件投影到共享的、模态解耦的表示空间中，通过可学习查询（Learnable Queries）进行跨模态特征聚合，同时借助模态指示头（Modality Indicator Heads）保持模态身份的独立性。这一设计使得新模态的引入仅需添加冻结编码器、轻量投影器和少量可学习查询，无需重新训练骨干网络，从而实现了真正意义上的模态可扩展条件生成。

## 核心方法与创新机理

MMCP-GEN 的核心创新在于提出了一种**模态可组合且可扩展的条件化机制**，从根本上改变了多模态蛋白质序列生成中条件信号的集成方式。与现有方法相比，其关键突破体现在三个维度的“changed slots”上。

### 从分离编码到统一条件空间

现有可控蛋白质生成方法（如 **DPLM**（Wang et al., ICML 2024）和 **CFP-GEN**（Yin et al., ICML 2025））通常为每种模态设计独立的编码器-适配器对，各模态在分离的表示空间中处理，导致跨模态交互受限、生成质量下降。MMCP-GEN 通过两个核心模块实现了范式的根本转变：

- **MMCP-IH（模态指示头）**：为每个模态引入一个可学习的指示符元 $t^{(m)}$，将其前置在模态特定的 token 序列前，形成 $\tilde{z}_m = [t^{(m)}; z_1^{(m)}, z_2^{(m)}, ..., z_{n_m}^{(m)}]$。这一设计显式保留了模态身份信息，使模型在统一的共享表示空间中仍能区分不同模态的语义来源。

- **MMCP-LQ（可学习查询融合模块）**：包含共享查询和模态特定查询，通过一个轻量级 Transformer 将拼接后的多模态 token 流 $C = [\tilde{z}_1; \tilde{z}_2; \cdots; \tilde{z}_M]$ 联合处理，生成紧凑的条件表示 $Z(c)$。这一模块实现了真正的跨模态特征聚合，而非简单的拼接或独立处理。

融合后的条件表示通过交叉注意力适配器注入扩散语言模型的隐藏状态：
$$h'(x^{(t)}, c) = h(x^{(t)}) + \mathrm{CrossAttn}(h(x^{(t)}), Z(c))$$

### 无需重训骨干的新模态扩展

传统方法每次引入新模态都需要重新设计架构或重新训练骨干网络，限制了实际应用中的灵活性。MMCP-GEN 的扩展方式实现了根本性简化：当引入新条件模态时，仅需新增一个冻结的预训练编码器、一个轻量投影器和一个模态指示符元，同时在 MMCP-LQ 中实例化模态特定查询。**扩散语言模型骨干及所有已有编码器完全冻结**，仅对新增的少量参数进行微调。这一设计使模态扩展的计算成本和工程复杂度降至最低。

### 序列-结构一致性显式优化

基线方法（如 DPLM）仅通过加权交叉熵损失 $\mathcal{L}_{CE}$ 最小化序列重建误差，缺乏对生成序列与条件结构之间一致性的显式约束。MMCP-GEN 引入**联合生成-评分目标（MMCP-GS）**，在结构条件可用时，通过 InfoNCE 损失最大化生成序列隐表示与真实结构嵌入之间的互信息：
$$\mathcal{L}_{GS} = -\log \frac{\exp(\mathrm{sim}(g(h(x)), z_{str}) / \tau)}{\sum_{s'} \exp(\mathrm{sim}(g(h(x)), z_{str}') / \tau)}$$

最终训练目标为 $\mathcal{L} = \mathcal{L}_{CE} + \gamma \mathcal{L}_{GS}$，其中 $\gamma$ 为平衡系数。这一设计将序列恢复与结构保真度直接对齐，而非依赖隐式的统计相关性。

消融实验验证了这一创新的有效性：加入 MMCP-GS 损失后，逆折叠任务的 AAR 从 78.17% 提升至 78.66%，scTM 从 0.906 提升至 0.912，pLDDT 从 86.25 提升至 86.88，三项指标均获得一致改善。

MMCP-GEN 以**扩散蛋白质语言模型（DPLM, Wang et al., ICML 2024）**为骨干，在其离散扩散去噪框架之上叠加一套**模态可组合且可扩展的条件化机制**，实现多模态生物条件下的蛋白质序列生成。整体 pipeline 的核心思路是：将异构的生物条件（三维结构、配体、功能注释、文本描述等）统一投影到共享的条件表示空间，再通过可学习查询融合模块聚合为紧凑的条件向量，最终以交叉注意力方式注入扩散 Transformer 的指定层，指导去噪过程还原出满足多模态约束的氨基酸序列。

### 数据流与模块关系

pipeline 的输入输出流可概括为以下阶段：

1. **多模态编码**：每种条件模态由**冻结的预训练编码器**独立处理——GVP-Transformer 编码三维结构、SchNet 编码配体分子图、ProtBERT 编码功能描述与文本。编码器在整个训练过程中保持冻结，仅作为特征提取器。
2. **共享空间投影**：各模态编码器的输出通过**轻量投影器** $P_m$ 映射到统一的 $d_{\text{cond}}$ 维条件空间，得到模态特征序列 $z_i^{(m)}$。
3. **模态身份保持（MMCP-IH）**：每个模态的 token 序列前端被附加一个**可学习的模态指示头** $t^{(m)}$，显式标记该 token 所属的模态身份，实现模态解耦。所有模态的 token 序列随后被拼接为全局条件流 $C$。
4. **跨模态融合（MMCP-LQ）**：引入**共享查询**和**模态特定查询**（各 $k_s = k_m = 4$ 个），通过一个轻量 Transformer 将全局条件流 $C$ 与查询联合处理，生成紧凑的融合条件表示 $Z(c)$。这一设计使得新模态的加入仅需新增模态特定查询，而无需重新训练骨干网络。
5. **条件注入**：融合后的条件表示 $Z(c)$ 通过**交叉注意力适配器**注入 DPLM Transformer 的隐藏状态。适配器被插入到 Transformer 堆栈的后三分之一层（第 24、28、33 层，共 33 层）的前馈子层之后。
6. **去噪生成**：在条件 $c$ 的引导下，扩散模型从被掩码的序列 $x^{(t)}$ 逐步预测干净序列 $\hat{x}^{(0)}$，通过加权交叉熵损失仅对被掩码位置进行监督。
7. **序列-结构对齐（MMCP-GS）**：当结构条件可用时，联合生成-评分损失通过 InfoNCE 最大化生成序列隐表示与真实结构嵌入之间的互信息，进一步强化序列恢复与结构保真度的一致性。

### 核心设计决策

| 设计维度 | 基线策略 (DPLM/CFP-GEN) | MMCP-GEN 策略 |
|---------|----------------------|--------------|
| 条件集成 | 单一模态编码器/适配器，各模态独立处理 | MMCP-IH 保持模态身份 + MMCP-LQ 跨模态融合 |
| 新模态扩展 | 需专门编码器-适配器对，可能需重新训练骨干 | 仅新增冻结编码器、轻量投影器和模态特定查询；骨干完全冻结 |
| 序列-结构一致性 | 仅最小化序列重建损失 | 联合生成-评分目标（InfoNCE 损失） |

### 关键公式

扩散前向过程采用吸收态马尔可夫过程，逐步将氨基酸替换为 MASK 标记：

$$q ( x _ { i } ^ { ( t ) } | x _ { i } ^ { ( t - 1 ) } ) = \mathrm { C a t } \Big ( x _ { i } ^ { ( t ) } ; \beta _ { t } e _ { x _ { i } ^ { ( t - 1 ) } } + ( 1 - \beta _ { t } ) e _ { \mathrm { M A S K } } \Big )$$

反向去噪在给定多模态条件 $c$ 下预测干净序列：

$$p _ { \theta } ( x ^ { ( t - 1 ) } | x ^ { ( t ) } , c ) = \sum _ { \hat { x } ^ { ( 0 ) } } q ( x ^ { ( t - 1 ) } | x ^ { ( t ) } , \hat { x } ^ { ( 0 ) } ) p _ { \theta } ( \hat { x } ^ { ( 0 ) } | x ^ { ( t ) } , c )$$

交叉注意力适配器将融合表示 $Z(c)$ 注入扩散 Transformer 的隐藏状态：

$$h ^ { \prime } ( x ^ { ( t ) } , c ) = h ( x ^ { ( t ) } ) + \mathrm { C r o s s A t t n } ( h ( x ^ { ( t ) } ) , Z ( c ) )$$

最终训练目标结合扩散去噪损失与结构对齐损失：

$$\mathcal { L } = \mathcal { L } _ { C E } + \gamma \mathcal { L } _ { \mathrm { G S } }$$

其中 $\mathcal{L}_{CE}$ 为仅对被掩码位置计算的加权交叉熵损失，$\mathcal{L}_{GS}$ 为 InfoNCE 形式的联合生成-评分损失，$\gamma$ 为平衡系数。

### 证据强度

- 模态可组合与可扩展机制的核心设计在论文 §3.3 有完整描述，证据充分（置信度 0.95）。
- 联合生成-评分目标的有效性在消融实验中验证：加入 MMCP-GS 后逆折叠 AAR 从 78.17% 提升至 78.66%，scTM 从 0.906 提升至 0.912（置信度 0.95）。
- 新模态扩展仅需冻结骨干的设计在 §3.3.2 有明确说明，但论文未对模态数量增加时的计算开销进行定量分析，该点需手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l2326_https_openaccess_thecvf_com_content_CVPR2026_html_An_MMCP_GEN_A_Modality/figures/001_Figure_1.jpg]]
*Figure 1: Overview of MMCP-GEN. MMCP-GEN unifies structure, ligand, text, functional annotations, and supports new modality extensions into a composable, extensible conditioning space for diffusion-based protein generation. Via MMCP-IH and MMCP-LQ, new modalities are integrated without backbone retraining and with minimal adaptation. Generated sequences are validated post-hoc using ESMFold together with additional biochemical and functional evaluations*

### 1. 离散扩散骨干：前向吸收与反向去噪

MMCP‑GEN 建立在离散扩散蛋白质语言模型 **DPLM** (Wang et al., ICML 2024) 之上，其核心是一个吸收态马尔可夫扩散过程。前向过程逐步将氨基酸 token 替换为 `[MASK]` 标记：

$$q ( x _ { i } ^ { ( t ) } | x _ { i } ^ { ( t - 1 ) } ) = \mathrm { C a t } \Big ( x _ { i } ^ { ( t ) } ; \beta _ { t } e _ { x _ { i } ^ { ( t - 1 ) } } + ( 1 - \beta _ { t } ) e _ { \mathrm { M A S K } } \Big )$$

其中 $x_i^{(t)}$ 为时间步 $t$ 时第 $i$ 个位置的 token，$\beta_t$ 控制吸收速率，$e_{\text{MASK}}$ 为掩码标记的独热向量。

反向去噪过程在给定多模态条件 $c$ 下重建原始序列。模型首先预测干净序列 $\hat{x}^{(0)}$，再由后验概率计算上一步的分布：

$$p _ { \theta } ( x ^ { ( t - 1 ) } | x ^ { ( t ) } , c ) = \sum _ { \hat { x } ^ { ( 0 ) } } q ( x ^ { ( t - 1 ) } | x ^ { ( t ) } , \hat { x } ^ { ( 0 ) } ) p _ { \theta } ( \hat { x } ^ { ( 0 ) } | x ^ { ( t ) } , c )$$

训练时采用加权交叉熵损失，仅对 `[MASK]` 位置计算重建误差，并根据扩散时间步进行加权：

$$\mathcal { L } _ { \mathrm { C E } , t } = \mathbb { E } _ { x ^ { ( 0 ) } , c } \Big [ \lambda ( t ) \sum _ { i } b _ { i } ( t ) ( - \log p _ { \theta } ( x _ { i } ^ { ( 0 ) } | x ^ { ( t ) } , c ) ) \Big ]$$

其中 $\lambda(t)$ 为时间步权重，$b_i(t)$ 为指示函数，仅在位置 $i$ 被掩码时取 1。

### 2. 多模态条件化：MMCP‑IH 与 MMCP‑LQ

条件化机制由两个核心模块构成：**模态指示头（MMCP‑IH）** 和 **可学习查询融合模块（MMCP‑LQ）**。

#### 2.1 模态指示头（MMCP‑IH）

每种模态 $m$ 首先通过冻结的预训练编码器 $E^{(m)}$ 提取特征 $h_i^{(m)}$，再由轻量投影器 $P_m$ 映射到共享条件空间 $\mathbb{R}^{d_{\text{cond}}}$：

$$z _ { i } ^ { ( m ) } = P _ { m } ( h _ { i } ^ { ( m ) } ) \in \mathbb { R } ^ { d _ { \mathrm { c o n d } } }$$

为显式标识模态身份，每个模态引入一个可学习的指示向量 $t^{(m)}$，前置到 token 序列前：

$$\tilde { z } _ { m } = \Big [ t ^ { ( m ) } ; z _ { 1 } ^ { ( m ) } , z _ { 2 } ^ { ( m ) } , . . . , z _ { n _ { m } } ^ { ( m ) } \Big ] \in \mathbb { R } ^ { ( n _ { m } + 1 ) \times d _ { \mathrm { c o n d } } }$$

所有模态的 token 序列被拼接为全局条件流：

$$C = [ \tilde { z } _ { 1 } ; \tilde { z } _ { 2 } ; \cdots ; \tilde { z } _ { M } ] \in \mathbb { R } ^ { N \times d _ { \mathrm { c o n d } } } , \quad N = \sum _ { m } ( n _ { m } + 1 )$$

#### 2.2 可学习查询融合模块（MMCP‑LQ）

MMCP‑LQ 通过一个轻量 Transformer 将全局条件流 $C$ 压缩为紧凑的条件表示 $Z(c)$。该模块包含两类可学习查询向量：

- **共享查询** $Q_s \in \mathbb{R}^{k_s \times d_{\text{cond}}}$：跨模态聚合通用条件信息
- **模态特定查询** $Q_m \in \mathbb{R}^{k_m \times d_{\text{cond}}}$：提取各模态特有信息

论文设定 $k_s = k_m = 4$。Transformer 以 $[Q_s; Q_1; \dots; Q_M]$ 作为 query，$C$ 作为 key/value 进行交叉注意力，输出融合后的条件表示 $Z(c)$。

融合表示通过交叉注意力适配器注入扩散骨干。适配器插入在 Transformer 最后三分之一层（共 33 层中的第 24、28、33 层）的前馈子层之后：

$$h ^ { \prime } ( x ^ { ( t ) } , c ) = h ( x ^ { ( t ) } ) + \mathrm { C r o s s A t t n } ( h ( x ^ { ( t ) } ) , Z ( c ) )$$

#### 2.3 新模态扩展

引入新模态 $m_{\text{new}}$ 时，仅需添加冻结编码器 $E^{(m_{\text{new}})}$、轻量投影器 $P_{m_{\text{new}}}$、模态指示 token $t^{(m_{\text{new}})}$ 以及模态特定查询 $Q_{m_{\text{new}}}$。骨干 DPLM 和已有编码器完全冻结，仅新查询和投影器参与微调。这一设计实现了无需重新训练骨干的可扩展多模态集成。

### 3. 联合生成–评分目标（MMCP‑GS）

当条件 $c$ 包含目标结构 $s$ 时，MMCP‑GEN 引入 InfoNCE 损失强制序列与结构的对齐。将生成序列的隐表示 $h(x)$ 经投影头 $g(\cdot)$ 映射后，与真实结构嵌入 $z_{\text{str}}$ 计算相似度，并以批次内其他结构作为负样本：

$$\mathcal { L } _ { \mathrm { G S } } = - \log \frac { \exp ( \mathrm { s i m } ( g ( h ( x ) ) , z _ { \mathrm { s t r } } ) / \tau ) } { \sum _ { s ^ { \prime } } \exp ( \mathrm { s i m } ( g ( h ( x ) ) , z _ { \mathrm { s t r } } ^ { \prime } ) / \tau ) }$$

最终训练目标为扩散去噪损失与结构对齐损失的加权组合：

$$\mathcal { L } = \mathcal { L } _ { C E } + \gamma \mathcal { L } _ { \mathrm { G S } }$$

其中 $\gamma$ 为平衡系数。消融实验表明，加入 MMCP‑GS 后逆折叠任务的 AAR 从 78.17% 提升至 78.66%，scTM 从 0.906 提升至 0.912，pLDDT 从 86.25 提升至 86.88，验证了该损失对序列–结构一致性的正向作用。

## 实验与关键发现

### 主实验结果

MMCP-GEN 在功能注释、逆折叠和配体条件生成三项核心任务上均取得最优或次优性能，验证了多模态可组合条件机制的有效性。

**功能注释评估（Table 1）**。在 GO 术语、IPR 结构域和 EC 编号三项功能注释子任务上，MMCP-GEN 使用全部四种模态条件（结构+配体+功能+文本）时，在所有指标上均显著优于 **DPLM**（Wang et al., ICML 2024）、**CFP-GEN**（Yin et al., ICML 2025）和 **ESM3**（Hayes et al., Science 2025）等基线。具体而言，EC 编号评估中 MMCP-GEN 取得 MRR 0.927、macro F1 0.928、AUC 0.954，表明多模态条件能够为功能相关的序列生成提供互补信息，而非简单叠加。GO 术语评估中 MRR 达 0.873，IPR 结构域评估中 micro F1 达 0.985，进一步印证了模态组合对功能语义保留的增益。

**逆折叠任务（Table 2）**。在内部数据集上，MMCP-GEN 以氨基酸恢复率（AAR）78.66% 超越 **ProteinMPNN**（Dauparas et al., Science 2022）等专用逆折叠模型，提升幅度最高达 5%。同时，结构质量指标 scTM 达 0.912，pLDDT 达 86.88，表明生成序列不仅恢复率高，且能折叠为与目标结构高度一致的构象。

**配体条件蛋白质设计（Figure 4）**。MMCP-GEN 生成的蛋白质能够复现天然配体结合模式，与 PDB 中对应结构具有强配体相似性。这归因于 MMCP-LQ 模块中的可学习查询能够有效提取配体结合口袋的几何与化学特征，并将其注入扩散去噪过程。

**折叠能力与多样性（Figure 5）**。在四种模态条件下，MMCP-GEN 生成序列经 ESMFold 重折叠后的 pLDDT 分布与天然蛋白质相当，pdb-TM（与 PDB 的 TM-score）较 **DPLM** 和 **UR50** 基线降低约 0.05，表明生成序列具有更高的新颖性。同时，生成样本间的 inner-TM 显示 MMCP-GEN 保持了合理的序列多样性，未出现模式坍塌。

### 消融实验

**模态组合的影响（Table 1）**。逐步增加条件模态可一致提升功能注释性能。仅使用结构条件时，MRR 和 F1 已优于无条件生成基线；加入功能注释或文本描述后，EC 编号的 MRR 进一步提升；使用全部四种模态时达到最优。这验证了 MMCP-IH 的模态解耦能力——各模态信息在共享表示空间中被有效保留，而非相互干扰。

**联合生成-评分损失（MMCP-GS）的作用**。在逆折叠任务中，加入 MMCP-GS 损失后，AAR 从 78.17% 提升至 78.66%，scTM 从 0.906 提升至 0.912，pLDDT 从 86.25 提升至 86.88。该消融直接证明了 InfoNCE 形式的序列-结构对齐损失能够在不增加推理开销的前提下，强化生成序列与目标结构之间的互信息，使序列恢复与结构保真度协同优化。

**可学习查询数量的影响**。论文设定共享查询和模态特定查询数量均为 4（$k_s = k_m = 4$），在计算效率与条件融合质量之间取得平衡。过少的查询可能无法充分捕获跨模态交互，过多则引入冗余参数——但论文未提供该超参数的敏感性分析，此点需读者自行验证。

### 关键图表结论

- **Table 1**：MMCP-GEN 在多模态条件下全面超越 DPLM、CFP-GEN、ESM3 等基线，证明可组合条件机制的有效性。
- **Table 2**：MMCP-GEN 在逆折叠任务上以 AAR 78.66% 取得最优，MMCP-GS 损失带来一致的性能增益。
- **Figure 4**：生成蛋白质的配体结合模式与天然结构高度一致，验证了配体条件编码的有效性。
- **Figure 5**：MMCP-GEN 在折叠能力、新颖性和多样性三个维度上均表现优异，pdb-TM 降低表明生成序列偏离已知 PDB 结构，具有设计新颖性。

![[assets/figures/papers/paper_list_l2326_https_openaccess_thecvf_com_content_CVPR2026_html_An_MMCP_GEN_A_Modality/figures/003_Table_1.jpg]]
*Table 1: Sequence similarity and functional annotation evaluation. Best and second-best results are highlighted in bold and underlined*

![[assets/figures/papers/paper_list_l2326_https_openaccess_thecvf_com_content_CVPR2026_html_An_MMCP_GEN_A_Modality/figures/005_Table_2.jpg]]
*Table 2: Comparison on an in-house dataset. MMCP-GEN outperforms prior inverse folding methods in accuracy (AAR) and structural quality (scTM, pLDDT)*

![[assets/figures/papers/paper_list_l2326_https_openaccess_thecvf_com_content_CVPR2026_html_An_MMCP_GEN_A_Modality/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of ligand-conditioned protein designs generated by MMCP-GEN. MMCP-GEN reproduces native ligandbinding patterns with strong ligand similarity to PDB counterparts*

![[assets/figures/papers/paper_list_l2326_https_openaccess_thecvf_com_content_CVPR2026_html_An_MMCP_GEN_A_Modality/figures/007_Figure_5.jpg]]
*Figure 5: Evaluation of protein sequence generation quality across models, measuring foldability (ESMFold pLDDT), novelty (pdb-TM to the PDB), and diversity (inner-TM among generated samples). MMCP-GEN is assessed under four modalities, while CFP-GEN uses three*

### 失败模式与局限

论文未系统报告失败案例，但基于方法设计可推断以下潜在问题：

1. **模态缺失时的退化行为**。MMCP-GEN 使用可学习占位符替代缺失模态，但未量化模态缺失对生成质量的影响程度。在仅提供单一模态的极端情况下，占位符可能引入噪声，性能退化幅度需要进一步实验验证。

2. **新模态扩展的隐性成本**。虽然新模态只需冻结编码器和轻量投影器，但模态特定查询的微调仍需要该模态的配对训练数据。对于数据稀缺的新模态（如特定翻译后修饰），微调效果可能受限。

3. **长序列生成的结构一致性**。论文未讨论序列长度超过 400 残基时的 scTM 和 pLDDT 变化趋势，长序列的全局结构一致性可能是潜在瓶颈——此点需读者结合 Figure 5B 的 pdb-TM 分布自行判断。

4. **多模态冲突**。当不同模态条件提供矛盾信息时（如结构要求疏水核心但功能注释指向亲水残基），MMCP-LQ 的融合策略是否会产生语义混淆，论文未提供分析。

### 补充图表

![[assets/figures/papers/paper_list_l2326_https_openaccess_thecvf_com_content_CVPR2026_html_An_MMCP_GEN_A_Modality/figures/006_Figure_3.jpg]]
*Figure 3: Comparison of MMCP-GEN–generated and reference protein structures. ESMFold-refolded sequences align closely with native PDB structures, demonstrating fold consistency*

## 定位与知识库关联

### 1. 方法谱系

MMCP-GEN 的方法根基建立在离散扩散蛋白质语言模型之上，其直接继承了 **DPLM** (Wang et al., ICML 2024) 的离散扩散生成框架。DPLM 首次将吸收态扩散过程引入蛋白质序列建模，通过逐步掩码与去噪学习氨基酸的分布规律。MMCP-GEN 在此基础上进行了关键性扩展：将原本仅支持单一条件适配器的控制机制，升级为可组合、可扩展的多模态条件化系统。

在条件蛋白质生成这一任务线上，MMCP-GEN 与 **CFP-GEN** (Yin et al., ICML 2025) 形成直接对照。CFP-GEN 专注于组合功能条件的蛋白质生成，但其条件集成方式仍依赖于为每种功能模态设计独立的编码器-适配器对，各模态在条件空间中缺乏显式的交互与解耦机制。MMCP-GEN 的核心突破在于引入了**模态指示头（MMCP-IH）**和**可学习查询融合模块（MMCP-LQ）**，将异构生物条件投影到共享的、模态解耦的表示空间中，通过可学习查询进行跨模态特征聚合，同时保持模态独立性。

从蛋白质语言模型的发展脉络来看，MMCP-GEN 与 **ESM3** (Hayes et al., Science 2025) 代表了两种不同的技术路线。ESM3 通过大规模预训练将结构、功能、序列等多模态信息隐式编码进统一的 Transformer 表示中，其条件控制依赖于提示工程和模型内部的隐式推理。MMCP-GEN 则采取显式的条件化策略，通过冻结的预训练编码器和轻量级投影器将各模态显式映射到共享空间，再由交叉注意力适配器注入扩散骨干。这种显式条件化的优势在于：新模态的引入不需要重新训练骨干网络，仅需添加冻结编码器、轻量投影器和模态特定查询即可。

在逆折叠（inverse folding）这一特定任务上，MMCP-GEN 与 **ProteinMPNN** (Dauparas et al., Science 2022) 形成互补关系。ProteinMPNN 是专门为结构到序列的逆向设计而优化的消息传递网络，在单一结构条件任务上表现优异。MMCP-GEN 则通过联合生成-评分目标（MMCP-GS），在结构条件基础上融合功能、配体等多模态信息，实现了更全面的条件控制。实验表明，MMCP-GEN 在逆折叠任务上的氨基酸恢复率（AAR）达到 78.66%，显著优于包括 ProteinMPNN 在内的先前方法。

### 2. 知识库定位

MMCP-GEN 的核心知识贡献在于提出了**模态可扩展的条件化范式**。这一范式的关键组件包括：

- **模态解耦的共享表示空间**：通过模态特定投影器将各模态特征映射到统一的 $d_{\mathrm{cond}}$ 维空间，同时通过模态指示头保留模态身份信息。这种设计使得不同模态的特征可以在同一空间中进行交互，而不会相互混淆。

- **可学习查询驱动的跨模态融合**：MMCP-LQ 模块包含共享查询和模态特定查询，通过一个 Transformer 将多模态 token 和查询联合处理，生成紧凑的条件表示。这种查询机制使得模型能够自适应地关注不同模态中的关键信息，而非简单地拼接或求和。

- **冻结骨干的可扩展性**：新模态的引入仅需添加冻结编码器、轻量投影器和模态特定查询，扩散语言模型骨干和所有现有编码器完全冻结。这一设计大幅降低了多模态扩展的训练成本，避免了每次引入新模态都需要重新训练整个系统的困境。

- **联合生成-评分对齐机制**：通过 InfoNCE 损失最大化生成序列的隐表示与真实结构嵌入之间的互信息，显式强化了序列恢复与结构保真度之间的一致性。

### 3. 适用边界与局限

尽管 MMCP-GEN 在多模态条件蛋白质生成上展现出显著优势，其方法仍存在若干适用边界：

**模态编码器依赖性**：MMCP-GEN 的可扩展性高度依赖于冻结编码器的表征质量。新模态的表征能力受限于所选编码器的性能——若某模态缺乏足够强大的预训练编码器，其条件控制效果将受到根本性制约。论文中使用的 GVP-Transformer（结构）、SchNet（配体）和 ProtBERT（功能/文本）均为各自领域的成熟模型，但对于新兴或小众的生物模态，可能缺乏同等质量的编码器。

**计算开销的隐忧**：论文未详细讨论模态数量增加时可能产生的计算开销。随着模态数量的增长，条件 token 序列长度 $N = \sum_m (n_m + 1)$ 线性增加，MMCP-LQ 中的 Transformer 处理开销也会随之增长。此外，多模态查询的交互可能导致潜在的模态冲突——当不同模态提供相互矛盾的条件信号时，模型如何协调这些冲突尚未被系统研究。

**零样本模态泛化的未知性**：论文展示了在已知模态组合上的强性能，但对于完全未见过的模态类型（如代谢通路信息、亚细胞定位等），在零样本情况下的泛化性能是否会显著下降，仍是一个开放问题。MMCP-IH 的指示头机制理论上支持任意模态的插入，但实际效果取决于新模态与训练模态在共享空间中的分布对齐程度。

**动态权重学习的缺失**：当前框架中，不同模态的贡献权重通过固定的架构设计（如查询数量 $k_s = k_m = 4$）和损失平衡系数 $\gamma$ 来确定。如何自动学习模态间的动态权重，而非依赖固定的超参数，是进一步提升模型自适应能力的关键方向。

### 4. 开放问题

基于 MMCP-GEN 的方法框架，以下开放问题值得进一步探索：

1. **端到端的模态编码器选择策略**：能否发展自动化的模态编码器选择与适配机制，使模型能够根据任务需求动态选择最优的编码器组合，而非依赖人工预设？

2. **模态冲突消解机制**：当多模态条件提供矛盾信号时（例如结构条件指向一种折叠，而功能注释暗示另一种），模型应如何显式地检测和消解这些冲突？引入不确定性量化或模态可靠性评估可能是潜在方向。

3. **条件空间的语义可解释性**：MMCP-IH 和 MMCP-LQ 构建的共享条件空间是否具有语义可解释的结构？不同模态的条件表示在空间中如何分布，是否形成了有意义的聚类或流形结构？

4. **扩展到动态与时序模态**：当前框架处理的是静态条件（结构、配体、功能标签），能否扩展到动态模态，如分子动力学轨迹、蛋白质构象变化的时间序列等？

5. **生成序列的实验验证闭环**：论文的评估主要基于计算指标（AAR、scTM、pLDDT）和 ESMFold 重折叠验证。将生成序列纳入湿实验验证闭环，并根据实验反馈优化条件化策略，是实现从计算设计到实际应用的关键一步。

## 原文 PDF

![[paperPDFs/CVPR_2026/MMCP_GEN_A_Modality_Extensible_Diffusion_Language_Model_for_Conditional_Protein_Sequence_Generation.pdf]]
