---
title: "CoIn: Coverage and Informativeness-Guided Token Reduction for Efficient Large Multimodal Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CoIn_Coverage_and_Informativeness_Guided_Token_Reduction_for_Efficient_Large_Multimodal_Models.pdf
project_link: null
code_link: null
aliases:
- CoIn
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 将令牌选择准则从单一的重要性或多样性转向联合优化信息量（视觉显著性+跨模态对齐）和覆盖范围（基于体积的子集选择），是关键控制因素。
primary_logic: 将视觉令牌精简重新形式化为最优子集选择问题，通过同时考虑每个令牌的视觉显著性、与文本的语义对齐以及所选子集在特征空间的全局体积，能够选出既显著又具有代表性的紧凑令牌子集，从而在大幅减少令牌的同时保持模型性能。
claims:
- CoIn 在 LLaVA-1.5-13B 上仅保留 5.6% 的令牌（32 个令牌）时，平均准确率仍达 91.0%，显著优于所有基线方法。
- 9 benchmarks (LLaVA-1.5-13B) 上 relative average performance = 91.0% (32 tokens)
- 将视觉令牌精简重新形式化为最优子集选择问题，通过同时考虑每个令牌的视觉显著性、与文本的语义对齐以及所选子集在特征空间的全局体积，能够选出既显著又具有代表性的紧凑令牌子集，从而在大幅减少令牌的同时保持模型性能。
---

# CoIn: Coverage and Informativeness-Guided Token Reduction for Efficient Large Multimodal Models

> [!tip] 核心洞察
> 将视觉令牌精简重新形式化为最优子集选择问题，通过同时考虑每个令牌的视觉显著性、与文本的语义对齐以及所选子集在特征空间的全局体积，能够选出既显著又具有代表性的紧凑令牌子集，从而在大幅减少令牌的同时保持模型性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 覆盖与信息量引导的视觉令牌精简方法用于高效大模态模型 |
| 英文题名 | CoIn: Coverage and Informativeness-Guided Token Reduction for Efficient Large Multimodal Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Du_CoIn_Coverage_and_Informativeness-Guided_Token_Reduction_for_Efficient_Large_Multimodal_CVPR_2026_paper.html) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | CoIn |
| Dataset | 9 benchmarks |

> [!tip] 效果简介
> - 9 benchmarks (LLaVA-1.5-13B) 上，relative average performance 91.0% (32 tokens) vs DivPrune 88.6% (32 tokens) (+2.4%)。

## 概要

大模态模型（Large Multimodal Models, LMMs）在视觉问答、图像描述等任务上表现优异，但其推理效率受到视觉令牌数量过多的严重制约——高分辨率图像经视觉编码器后通常产生数百甚至上千个令牌，直接推高了自注意力机制的计算复杂度和键值缓存的内存开销。这构成了 LMM 实际部署的主要瓶颈。

现有视觉令牌精简方法通常沿着两条独立路径展开：基于重要性的选择（如依据注意力分数或 [CLS] 相似度保留高分令牌）和基于多样性的选择（通过消除成对冗余来维持子集多样性）。然而，单独强调重要性容易导致所选令牌在语义空间高度集中、遗漏全局信息；单独强调多样性则可能丢弃对文本查询至关重要的令牌。**CoIn** 的核心洞见在于，将视觉令牌精简重新形式化为一个**最优子集选择问题**，并引入两个互补的优化目标——**信息量（informativeness）**和**覆盖范围（coverage）**——进行联合求解。

信息量度量每个令牌对下游任务的贡献潜力，由两个正交子准则构成：内在视觉显著性（令牌激活强度的 p-范数）和跨模态对齐（视觉令牌嵌入与文本嵌入的余弦相似度）。覆盖范围则通过所选子集在特征空间中所张成的体积（正则化 Gram 矩阵的对数行列式）来量化，鼓励子集在全局语义空间均匀分布，避免冗余。CoIn 将二者耦合为一个统一的目标函数，并通过贪心算法高效近似求解，从而在极低令牌预算下选出既显著又具代表性的紧凑子集。

在 LLaVA-1.5-13B 模型上，CoIn 仅保留 **5.6%** 的视觉令牌（32 个令牌）时，在 9 个基准上平均性能仍达到原始模型的 **91.0%**，显著优于 **DivPrune**（Alvar et al., CVPR 2025）的 88.6% 等强基线方法。当保留 128 个令牌时，平均性能保持在 96.2%。该方法不依赖特定的视觉编码器或注意力实现，与 FlashAttention 及 KV 缓存兼容，具有良好的泛化性。

### 大模态模型的效率瓶颈

大模态模型（Large Multimodal Models, LMMs）通过将视觉编码器与大语言模型（LLM）集成，在图像理解、视觉问答和视频分析等任务上取得了显著进展。其标准前向过程可表示为：

$$y = f_{\phi}([V ; T])$$

其中 $V$ 为视觉令牌集合，$T$ 为文本令牌集合，LLM 处理拼接后的序列产生输出 $y$。

然而，视觉编码器通常为每张图像生成数百甚至上千个令牌。这些冗余的视觉令牌导致推理计算量急剧增加和 GPU 内存占用过高，成为 LMM 实际部署的主要瓶颈。在需要处理高分辨率图像或多帧视频的场景中，这一问题尤为突出。

### 现有令牌精简方法的局限性

为缓解上述问题，研究者提出了多种视觉令牌精简方法，主要分为两类：

**基于重要性的方法**（如 **PDrop** (Xing et al., CVPR 2025)、**SparseVLM** (Zhang et al., ICML 2025)、**PruMerge** (Shang et al., ICCV 2025)）通过注意力权重或 [CLS] 相似度等指标评估每个令牌的重要性，保留得分最高的令牌。这类方法的问题是所选令牌往往在特征空间高度集中，丢失了全局空间覆盖，导致细粒度视觉信息缺失。

**基于多样性的方法**（如 **DivPrune** (Alvar et al., CVPR 2025)、**DART**、**CDPruner**）通过惩罚令牌间的成对冗余来鼓励选择多样化。然而，它们通常只关注局部去冗余，缺乏对全局覆盖的显式建模，且忽视了令牌与文本查询之间的语义关联。

两类方法的共同缺陷在于：令牌选择准则单一——要么仅关注重要性，要么仅关注多样性——未能同时兼顾“选什么”和“如何覆盖”两个维度。

### 核心动机与研究思路

CoIn 的核心动机源于一个关键观察：理想的令牌子集应当同时满足两个互补条件——**信息量**（informativeness）和**覆盖范围**（coverage）。信息量确保所选令牌包含对任务有用的语义内容，覆盖范围确保这些令牌在特征空间中分布广泛、避免冗余。

基于此，CoIn 将视觉令牌精简重新形式化为最优子集选择问题：

$$S^{\star} = \operatorname*{argmin}_{S \subseteq V, |S| = K} \mathcal{D}\big( f_{\phi}([V ; T]), f_{\phi}([S ; T]) \big)$$

该目标旨在从原始令牌集 $V$ 中选出大小为 $K$ 的子集 $S$，使得使用子集与使用全部令牌的模型输出差异最小。通过将信息量和覆盖范围纳入统一的优化框架，CoIn 在无需重新训练的前提下，实现了在极高精简率下仍保持模型性能的目标。

### 方法定位

与现有方法相比，CoIn 的关键区别在于：

- **信息量度量**：将内在视觉显著性（$p$-范数激活强度）与跨模态对齐（视觉-文本余弦相似度）相结合，而非仅依赖注意力或 [CLS] 相似度。
- **覆盖范围建模**：通过最大化所选子集在特征空间所张成的体积（对数行列式）来显式保证全局多样性，而非仅做局部去冗余。
- **统一优化**：将信息量求和与覆盖范围对数行列式耦合为单一目标函数，通过贪心算法高效近似求解。

这种设计使 CoIn 在 LLaVA-1.5-13B 上仅保留 5.6% 的视觉令牌（32 个令牌）时，仍能在 9 个基准上达到 91.0% 的平均相对性能，显著优于所有基线方法。

## 核心方法与创新机理

CoIn 的核心创新在于将视觉令牌精简重新形式化为一个**最优子集选择问题**，并通过两个互补的准则——**信息量（Informativeness）**与**覆盖范围（Coverage）**——联合引导选择过程。这与既有方法形成了根本性的差异。

### 从单一准则到联合优化

现有令牌精简方法通常依赖单一的筛选准则，可归为两类：

- **基于重要性的方法**：如 **PDrop**（Xing et al., CVPR 2025）、**SparseVLM**（Zhang et al., ICML 2025）、**VisionZip**（Yang et al., CVPR 2025）等，通过注意力分数或 [CLS] 相似度评估每个令牌的重要性，保留得分最高的令牌。这类方法容易选出彼此高度相似、在特征空间集中分布的令牌，造成严重的**冗余保留**。
- **基于多样性的方法**：如 **DivPrune**（Alvar et al., CVPR 2025）、**DART**、**CDPruner** 等，通过惩罚令牌间的成对冗余来鼓励多样性。然而，它们通常只关注局部去冗余，难以保证所选子集在全局特征空间的**覆盖完整性**。

CoIn 的关键突破在于将上述两个维度统一到一个原则性框架中。其目标函数为：

$$S^{*} = \arg\max_{\boldsymbol{S} \subseteq \boldsymbol{V}, |\boldsymbol{S}| = K} \left[ (1 - \alpha) \sum_{i \in S} s_{\mathrm{info}, i} + \alpha \log \det(\mathbf{F}_{\boldsymbol{S}}^{\top} \mathbf{F}_{\boldsymbol{S}}) \right]$$

其中第一项为信息量得分的求和，第二项为所选令牌特征矩阵的正则化 Gram 矩阵的行列式对数，度量子集在特征空间中**张成的体积**。超参数 $\alpha$ 平衡信息量与覆盖范围的相对权重。这一形式将令牌选择从启发式排序提升为**全局优化**，贪心算法在每一步同时考虑候选令牌的个体信息量和加入后对子集体积的边际增益。

### 信息量的双通道设计

CoIn 对“信息量”的定义本身也突破了既有方法。传统重要性方法仅依赖单一信号（如注意力权重），而 CoIn 将信息量分解为两个正交且互补的子准则：

- **内在视觉显著性**：通过令牌特征的 $p$-范数 $\mathbf{s}_{\mathrm{vis}} = \| \mathbf{F}_V \|_p$ 捕获，反映令牌在视觉场景中的感知突出程度，与用户查询无关。
- **跨模态对齐**：通过视觉令牌嵌入与平均文本嵌入的余弦相似度 $\mathbf{s}_{\mathrm{align}} = \frac{\mathbf{F}_V \bar{\mathbf{F}}_T^{\top}}{\|\mathbf{F}_V\| \|\bar{\mathbf{F}}_T^{\top}\|}$ 度量，捕捉令牌与语言指令的语义相关性。

二者通过凸组合融合为整体信息量评分：$\mathbf{s}_{\mathrm{info}} = \beta \mathbf{s}_{\mathrm{vis}} + (1 - \beta) \mathbf{s}_{\mathrm{align}}$。消融实验（Table 7）证实，联合使用两个子准则始终优于单独使用任一者，验证了二者的互补性：视觉显著性提供**查询无关的底层感知线索**，跨模态对齐注入**查询特定的语义引导**。

### 覆盖范围的体积形式化

CoIn 的覆盖范围准则同样区别于现有的多样性方法。现有方法多通过惩罚成对相似度来避免冗余，这是一种**局部操作**。CoIn 则通过最大化所选子集在特征空间中所张成子空间的体积 $\mathrm{Vol}(\boldsymbol{S}) = \log \det(\mathbf{F}_{\boldsymbol{S}}^{\top} \mathbf{F}_{\boldsymbol{S}} + \lambda \mathbf{I})$ 来实现**全局覆盖**。这一形式化自然地鼓励所选令牌在特征空间中均匀散布，避免信息冗余，同时保持对特征空间整体结构的覆盖。

Figure 5 直观展示了这一差异：基于重要性的方法选出的令牌高度集中，基于多样性的方法仅实现局部分散，而 CoIn 的覆盖驱动选择实现了全局均匀分布。

### 方法定位与优势总结

CoIn 是一种**无需训练的令牌选择策略**，不依赖特定的视觉编码器或注意力实现，与 FlashAttention 及 KV 缓存兼容。其核心贡献在于将令牌精简从启发式排序提升为原则性的子集优化，并通过信息量与覆盖范围的联合建模，在极低令牌预算下仍保持模型性能。在 LLaVA-1.5-13B 上，CoIn 仅保留 5.6% 的令牌（32 个）时，在 9 个基准上的平均相对性能达 91.0%，显著优于所有基线方法（如 DivPrune 的 88.6%）。

CoIn 将视觉令牌精简重新形式化为一个**最优子集选择问题**，其核心思想是同时优化两个互补准则——**信息量（informativeness）**与**覆盖范围（coverage）**——从而在特征空间中选出一个既显著又具有代表性的紧凑令牌子集。整体流程如图 3 所示，包含两个关键模块：信息量估计与覆盖感知选择，二者共享输入特征并协同工作，最终通过贪心算法输出精简后的令牌子集。

**输入与输出流。** 给定大模态模型（LMM）中视觉编码器输出的视觉令牌集合 $V$（含 $N$ 个令牌，每个令牌对应一个 $d$ 维特征向量）以及由文本编码器或嵌入层产生的文本令牌集合 $T$，CoIn 的目标是从 $V$ 中选出大小为 $K$（$K \ll N$）的子集 $S$，使得模型在使用 $S$ 替代 $V$ 时的输出差异最小化：

$$S^{\star} = \operatorname*{argmin}_{S \subseteq V, |S| = K} \mathcal{D}\big( f_{\phi}([V ; T]), f_{\phi}([S ; T]) \big)$$

其中 $f_{\phi}$ 表示 LLM 的前向过程，$\mathcal{D}$ 为输出分布的距离度量。CoIn 不直接优化该目标，而是通过信息量与覆盖范围两个代理准则来近似求解。

**模块一：信息量估计。** 该模块为每个视觉令牌计算一个信息量分数 $\mathbf{s}_{\mathrm{info}}$，由两个正交的子准则凸组合而成：

$$\mathbf{s}_{\mathrm{info}} = \beta \mathbf{s}_{\mathrm{vis}} + (1 - \beta) \mathbf{s}_{\mathrm{align}}$$

- **内在视觉显著性** $\mathbf{s}_{\mathrm{vis}} = \| \mathbf{F}_V \|_p$：利用令牌特征矩阵的 $p$-范数（默认 $p=2$）捕捉视觉场景中的感知突出程度，该分数与文本查询无关，反映令牌在视觉空间中的固有激活强度。
- **跨模态对齐** $\mathbf{s}_{\mathrm{align}} = \frac{\mathbf{F}_V \bar{\mathbf{F}}_T^{\top}}{\|\mathbf{F}_V\| \|\bar{\mathbf{F}}_T^{\top}\|}$：计算每个视觉令牌嵌入与平均文本嵌入之间的余弦相似度，衡量令牌与当前查询语义的相关性。

两个子准则互补：视觉显著性提供底层感知线索，跨模态对齐则注入查询特定的语义引导。消融实验（Table 7）证实，联合使用两者始终优于单独使用任一子准则。

**模块二：覆盖感知选择。** 为避免所选令牌在特征空间中高度集中或仅局部多样化，CoIn 引入基于体积的子集选择机制。给定候选子集 $\boldsymbol{S}$ 的特征矩阵 $\mathbf{F}_{\boldsymbol{S}}$，其覆盖范围通过正则化 Gram 矩阵的行列式对数来度量：

$$\mathrm{Vol}(\boldsymbol{S}) = \log \det(\mathbf{F}_{\boldsymbol{S}}^{\top} \mathbf{F}_{\boldsymbol{S}} + \lambda \mathbf{I})$$

该体积分数鼓励所选令牌在嵌入空间中张成更大的子空间，从而实现全局分布的覆盖，避免冗余令牌的重复选取。图 5 直观对比了仅基于重要性、仅基于多样性与 CoIn 覆盖准则的令牌分布差异：重要性方法选出的令牌高度集中，多样性方法仅保证局部多样，而 CoIn 的覆盖准则实现了更全局的分布。

**统一目标与贪心求解。** CoIn 将信息量求和与覆盖范围对数行列式耦合为一个统一的最大化目标：

$$S^{*} = \arg\max_{\boldsymbol{S} \subseteq \boldsymbol{V}, |\boldsymbol{S}| = K} \left[ (1 - \alpha) \sum_{i \in S} s_{\mathrm{info}, i} + \alpha \log \det(\mathbf{F}_{\boldsymbol{S}}^{\top} \mathbf{F}_{\boldsymbol{S}}) \right]$$

其中 $\alpha$ 平衡信息量与覆盖范围的权重。由于精确求解该组合优化问题是 NP-hard，CoIn 采用贪心算法逐步选择令牌：每次迭代选择能使当前目标函数增益最大的令牌加入子集，直至达到预算 $K$。该过程无需训练，与 FlashAttention 及 KV 缓存完全兼容，可即插即用于各类 LMM 架构。

![[assets/figures/papers/paper_list_l742_https_openaccess_thecvf_com_content_CVPR2026_html_Du_CoIn_Coverage_and_I/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our proposed CoIn. We first calculate the informativeness and coverage score using input tokens, then apply a greedy subset selection algorithm to obtain the subset*

CoIn 将视觉令牌精简重新形式化为一个最优子集选择问题，其核心由两个互补模块构成：**信息量估计**与**覆盖感知选择**。

### 问题形式化

给定视觉令牌集合 $V$ 和文本令牌集合 $T$，大语言模型的前向传播为：

$$y = f_{\phi}([V ; T])$$

令牌精简的目标是选择一个大小为 $K$ 的子集 $S \subseteq V$，使输出分布与使用全部令牌时的差异最小：

$$S^{\star} = \operatorname*{argmin}_{S \subseteq V, |S| = K} \mathcal{D}\big( f_{\phi}([V ; T]), f_{\phi}([S ; T]) \big)$$

直接优化该目标在计算上不可行，CoIn 通过信息量和覆盖范围两个可计算准则来近似求解。

### 信息量估计模块

信息量定义为两个正交线索的融合：**内在视觉显著性**捕捉令牌在视觉场景中的感知突出度，**跨模态对齐**度量令牌与文本查询的语义相关性。

**视觉显著性分数** 使用令牌特征矩阵 $\mathbf{F}_V$ 的 $p$-范数（默认 $p=2$）来近似令牌的内在激活强度：

$$\mathbf{s}_{\mathrm{vis}} = \| \mathbf{F}_V \|_p$$

**跨模态对齐分数** 计算每个视觉令牌嵌入与平均文本嵌入 $\bar{\mathbf{F}}_T$ 之间的余弦相似度：

$$\mathbf{s}_{\mathrm{align}} = \frac{\mathbf{F}_V \bar{\mathbf{F}}_T^{\top}}{\|\mathbf{F}_V\| \|\bar{\mathbf{F}}_T^{\top}\|}$$

两者归一化后通过凸组合得到**综合信息量分数**：

$$\mathbf{s}_{\mathrm{info}} = \beta \mathbf{s}_{\mathrm{vis}} + (1 - \beta) \mathbf{s}_{\mathrm{align}}$$

其中 $\beta \in [0, 1]$ 控制两个子准则的权重。消融实验（Table 7）表明，联合使用内在显著性与跨模态对齐始终优于单独使用任一子准则，验证了二者的互补性：视觉显著性提供底层感知线索，跨模态对齐注入查询相关的语义引导。

### 覆盖感知选择模块

仅依赖信息量可能导致所选令牌在特征空间中高度集中，造成信息冗余。覆盖感知选择通过最大化所选子集在嵌入空间中所张成的子空间体积来确保全局多样性。

对于所选子集 $\boldsymbol{S}$ 的特征矩阵 $\mathbf{F}_{\boldsymbol{S}}$，其覆盖范围定义为正则化 Gram 矩阵的对数行列式：

$$\mathrm{Vol}(\boldsymbol{S}) = \log \det(\mathbf{F}_{\boldsymbol{S}}^{\top} \mathbf{F}_{\boldsymbol{S}} + \lambda \mathbf{I})$$

其中 $\lambda \mathbf{I}$ 为正则化项，保证数值稳定性。该体积度量鼓励所选令牌在特征空间中广泛分布，避免冗余。

### 统一目标与贪心求解

CoIn 将信息量与覆盖范围耦合为统一目标函数：

$$S^{*} = \arg\max_{\boldsymbol{S} \subseteq \boldsymbol{V}, |\boldsymbol{S}| = K} \left[ (1 - \alpha) \sum_{i \in S} s_{\mathrm{info}, i} + \alpha \log \det(\mathbf{F}_{\boldsymbol{S}}^{\top} \mathbf{F}_{\boldsymbol{S}}) \right]$$

其中 $\alpha \in [0, 1]$ 平衡信息量求和与覆盖范围对数行列式的权重。由于子集选择是组合优化问题，CoIn 采用贪心算法近似求解，逐步选择能最大化边际增益的令牌。消融实验（Table 6）证实，联合使用信息量和覆盖范围的完整 CoIn 优于仅使用信息量或仅使用覆盖范围的变体，验证了两个准则的互补性。

## 实验与关键发现

### 主实验结果

CoIn 在多个主流大模态模型和基准上展现了强泛化能力。在 **LLaVA-1.5-13B** 上，仅保留 **128 个令牌**（约 22.2% 保留率）时，CoIn 达到原始模型 **96.2%** 的平均性能；当令牌预算进一步压缩到 **32 个**（保留率仅 5.6%）时，仍保持 **91.0%** 的平均准确率，显著优于所有基线方法（Table 1）。相比之下，最强的基线方法 **DivPrune**（Alvar et al., CVPR 2025）在 32 令牌设定下仅达到 88.6%，CoIn 领先 **+2.4 个百分点**。

![[assets/figures/papers/paper_list_l742_https_openaccess_thecvf_com_content_CVPR2026_html_Du_CoIn_Coverage_and_I/figures/006_Table_1.jpg]]
*Table 1: Performance on LLaVA-1.5-13B. “Avg.” indicates the average performance relative to the original model across 9 benchmarks*

在 **LLaVA-NeXT-7B** 上，CoIn 在 640 令牌和 320 令牌预算下分别保持 **94.0%** 和 **90.0%** 的平均相对性能（Table 2）。在 **Qwen2.5-VL-7B** 上同样表现稳健（Table 3），而在视频理解的 **LLaVA-OneVision-7B** 上，CoIn 在 3 个视频基准上同样优于对比方法（Table 4）。

![[assets/figures/papers/paper_list_l742_https_openaccess_thecvf_com_content_CVPR2026_html_Du_CoIn_Coverage_and_I/figures/007_Table_2.jpg]]
*Table 2: Performance on LLaVA-NeXT-7B. “Avg.” indicates average performance relative to original model across 9 benchmarks*

![[assets/figures/papers/paper_list_l742_https_openaccess_thecvf_com_content_CVPR2026_html_Du_CoIn_Coverage_and_I/figures/008_Table_3.jpg]]
*Table 3: Performance on Qwen2.5-VL-7B. “Avg.” indicates average performance relative to original model across 7 benchmarks*

![[assets/figures/papers/paper_list_l742_https_openaccess_thecvf_com_content_CVPR2026_html_Du_CoIn_Coverage_and_I/figures/009_Table_4.jpg]]
*Table 4: Performance on LLaVA-OneVision-7B. DyCoke∗ employs grouped token merging with a fixed minimum of 1762 retained tokens. “Avg.” indicates average performance relative to original model across 3 benchmarks*

效率方面，CoIn 在 LLaVA-1.5-13B 上实现 **94.4% 的令牌缩减**，同时推理延迟和内存占用大幅下降（Table 5），且与 FlashAttention 和 KV 缓存完全兼容，无需额外训练。

### 消融实验

**信息量与覆盖范围的互补性。** Table 6 显示，单独使用信息量（Info-only）或单独使用覆盖范围（Cov-only）均显著弱于完整 CoIn。这表明两个准则存在互补——信息量捕获令牌的显著性，覆盖范围确保所选子集的全局多样性，二者联合才能选出既显著又具代表性的紧凑子集。

**信息量内部子准则的分解。** Table 7 进一步消融了信息量的两个组成部分：内在显著性（Intrinsic Saliency, IS）和跨模态对齐（Cross-modal Alignment, CA）。单独使用任一子准则均导致性能下降，二者联合使用（IS+CA）达到最优，验证了视觉显著性提供底层感知线索、跨模态对齐注入查询特异性引导的互补机制。Figure 4(c) 的定量对比也印证了这一结论。

### 超参数敏感性

CoIn 引入两个关键超参数：平衡信息量与覆盖范围的 **α**，以及平衡内在显著性与跨模态对齐的 **β**。Figure 6 展示了在 Qwen 实验的 7 个基准上不同 α 和 β 设置下的平均性能。结果表明，方法对超参数在合理范围内具有一定鲁棒性，但针对不同模型和数据集仍需手动调节以获得最佳性能，这构成实际部署中的一个局限性。

### 关键图表结论

- **Figure 1**：CoIn 在多样基准上均超越强基线，同时显著提升推理效率，验证了方法的整体有效性。
- **Figure 4 (a, b)**：可视化展示了内在显著性关注视觉突出区域（与查询无关），而跨模态对齐则聚焦于与查询语义相关的令牌（如“鞋子”），二者关注点正交且互补。
- **Figure 5**：基于重要性的方法所选令牌高度集中，基于多样性的方法仅实现局部多样，而 CoIn 基于体积的覆盖范围准则能实现更全局的分布覆盖，避免冗余。
- **Table 1–4**：跨模型、跨基准、跨令牌预算的一致性优势，确证了 CoIn 的泛化能力和免训练特性。

![[assets/figures/papers/paper_list_l742_https_openaccess_thecvf_com_content_CVPR2026_html_Du_CoIn_Coverage_and_I/figures/013_Table_6.jpg]]
*Table 6: Ablation on coverage and informativeness. “Info” and “Cov” respectively denote informativeness and coverage terms*

## 定位与知识库关联

### 核心差异：从单准则到双重联合优化

现有视觉令牌精简方法大多沿单一准则设计：**重要性驱动**或**多样性驱动**。CoIn 的根本区别在于将问题重新形式化为一个**最优子集选择**任务，并同时耦合**信息量**与**覆盖范围**两个互补目标。

- **重要性驱动方法**（如 PDrop, Xing et al., CVPR 2025；SparseVLM, Zhang et al., ICML 2025；VisionZip, Yang et al., CVPR 2025）依据注意力权重或 [CLS] 相似度选取高分令牌。这类方法容易选出高度集中的令牌簇，导致特征空间覆盖不足，遗漏全局上下文信息。
- **多样性驱动方法**（如 DivPrune, Alvar et al., CVPR 2025；CDPruner）通过惩罚令牌间的成对冗余来增强子集多样性，但缺乏对每个令牌与文本查询之间语义相关性的显式建模，可能保留视觉上多样但与任务无关的令牌。
- **合并类方法**（如 PruMerge, Shang et al., ICCV 2025；DART）通过聚类或合并减少令牌数量，本质上改变了令牌的原始语义表示，可能引入信息混叠。

CoIn 不依赖上述任何单一策略，而是构建了一个统一目标函数：

$$S^{*} = \arg\max_{\boldsymbol{S} \subseteq \boldsymbol{V}, |\boldsymbol{S}| = K} \left[ (1 - \alpha) \sum_{i \in S} s_{\mathrm{info}, i} + \alpha \log \det(\mathbf{F}_{\boldsymbol{S}}^{\top} \mathbf{F}_{\boldsymbol{S}}) \right]$$

其中信息量项 $s_{\mathrm{info}, i}$ 本身又是两个子准则的凸组合：内在视觉显著性（$p$-范数）与跨模态对齐（视觉令牌与平均文本嵌入的余弦相似度）。覆盖范围项通过所选令牌特征矩阵的 Gram 行列式对数 $\log \det(\mathbf{F}_{\boldsymbol{S}}^{\top} \mathbf{F}_{\boldsymbol{S}} + \lambda \mathbf{I})$ 度量子集在特征空间中张成的体积，显式鼓励全局分散的令牌分布。

### 性能定位与证据强度

在 LLaVA-1.5-13B 上，CoIn 仅保留 5.6% 视觉令牌（32 个）时，9 个基准的平均相对性能达 91.0%，比最强基线 DivPrune 的 88.6% 高出 2.4 个百分点（Table 1，置信度 0.95）。在 LLaVA-NeXT-7B 和 Qwen2.5-VL-7B 上同样保持领先（Table 2、Table 3），表明该方法对视觉编码器和大语言模型架构不敏感，具有跨模型泛化能力。

消融实验提供了因果证据（Table 6、Table 7，置信度 0.95）：(1) 联合使用信息量与覆盖范围的完整 CoIn 优于仅使用任一准则的变体；(2) 在信息量内部，同时包含内在显著性与跨模态对齐优于单独使用任一子准则。这验证了两个层次互补性的必要性——准则间的互补（信息量 + 覆盖范围）和准则内的互补（显著性 + 对齐）。

### 适用边界与局限

CoIn 是一个**免训练**的令牌选择策略，与 FlashAttention 及 KV 缓存兼容，理论上可插入任意大模态模型。但分析明确指出的局限是：超参数 $\alpha$（控制信息量与覆盖范围的权衡）和 $\beta$（控制显著性与对齐的权衡）需要针对不同模型和数据集手动调节，这降低了即插即用的便捷性。该结论来自 verified_analysis 的 limitations 字段，原文中是否有自动化调参方案的讨论需进一步核实。

### 开放问题

分析中提出的两个开放问题值得关注：

1. **极端低令牌预算的语义保真度**：当保留率低于 1%（如 10 个令牌以内）时，基于体积的覆盖准则是否仍能有效捕获关键语义？体积最大化在极低维度下可能退化为选点分散但语义无关的令牌，该边界行为尚未被验证。

2. **跨模态扩展**：当前框架针对单张图像的视觉令牌精简，是否可以扩展到视频时间维度的令牌选择或三维场景表示的空间令牌精简？这需要将覆盖范围的定义从静态特征空间推广到时序或空间结构约束下的子集选择问题。

这两个问题在提供的分析中标记为 open_questions，原文是否有相关讨论需人工确认。

## 原文 PDF

![[paperPDFs/CVPR_2026/CoIn_Coverage_and_Informativeness_Guided_Token_Reduction_for_Efficient_Large_Multimodal_Models.pdf]]
