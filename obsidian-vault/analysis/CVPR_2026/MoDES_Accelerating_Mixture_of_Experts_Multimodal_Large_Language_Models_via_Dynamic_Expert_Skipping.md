---
title: "MoDES: Accelerating Mixture-of-Experts Multimodal Large Language Models via Dynamic Expert Skipping"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MoDES_Accelerating_Mixture_of_Experts_Multimodal_Large_Language_Models_via_Dynamic_Expert_Skipping.pdf
project_link: null
code_link: "https://github.com/ModelTC/MoDES"
aliases:
- MoDES
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 引入全局调制的局部门控（GMLG）以结合离线的层重要性评分，以及双模态阈值（DMT）为文本和视觉令牌分别设置跳过阈值，从而自适应地跳过冗余专家。
primary_logic: 浅层专家比深层专家对最终输出影响更大，视觉令牌的专家冗余度高于文本令牌，因此需要层次敏感且模态感知的专家跳过策略。
claims:
- 在Kimi-VL-A3B-Instruct上跳过83%专家时，MoDES保持96.25%平均性能，而基线方法（如DiEP）下降超过11%。
- 跳过88%专家时，Qwen3-VL-MoE-30B-A3B-Instruct上MoDES提升达10.67%（97.33% vs 86.66%）。
- 消融研究表明GMLG和DMT对性能提升至关重要：仅使用局部策略在ChartQA上为82.38，加入GMLG后提升至84.20（Skip 83%）。
- 模态差距分析显示，视觉令牌在FFN前后余弦相似度更高，且与FFN权重夹角更接近90°，表明专家对视觉令牌影响较小。
---

# MoDES: Accelerating Mixture-of-Experts Multimodal Large Language Models via Dynamic Expert Skipping

> [!tip] 核心洞察
> 浅层专家比深层专家对最终输出影响更大，视觉令牌的专家冗余度高于文本令牌，因此需要层次敏感且模态感知的专家跳过策略。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoDES: 通过动态专家跳过来加速混合专家多模态大语言模型 |
| 英文题名 | MoDES: Accelerating Mixture-of-Experts Multimodal Large Language Models via Dynamic Expert Skipping |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.15690) · [Code](https://github.com/ModelTC/MoDES) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | MoDES |
| Dataset | Kimi-VL-A3B-Instruct, Qwen3-VL-MoE-30B-A3B-Instruct |

> [!tip] 效果简介
> - Kimi-VL-A3B-Instruct (Skip 50%) 上，Avg. accuracy (%) 99.91 vs 98.17 (DiEP) (+1.74%)。
> - Kimi-VL-A3B-Instruct (Skip 83%) 上，Avg. accuracy (%) 96.25 vs 88.32 (MC-MoE) (+7.93%)。
> - Qwen3-VL-MoE-30B-A3B-Instruct (Skip 88%) 上，Avg. accuracy (%) 97.33 vs 86.66 (MC-MoE) (+10.67%)。

## 概述

多模态大语言模型（MLLM）在引入混合专家（MoE）架构后，虽然以较低的激活参数量实现了强大的性能，但庞大的专家总数仍导致显著的推理延迟和内存占用。现有的专家跳过方法在应用于MoE MLLM时，普遍忽略了两个关键瓶颈：**不同层的专家对最终输出的全局贡献不均衡**，以及**文本令牌与视觉令牌在专家冗余度上的行为差异**。这导致现有方法在高跳过比例下性能急剧下降——例如，DiEP在跳过83%专家时平均性能下降超过11%。

针对上述问题，本文提出**MoDES**，首个面向MoE MLLM的训练无关（training-free）动态专家跳过框架。其核心思路是通过两个相互配合的机制实现层次敏感且模态感知的专家跳过：**全局调制的局部门控（GMLG）**利用离线校准数据量化每层专家对输出分布的重要性，并将其与局部路由概率结合；**双模态阈值（DMT）**则为文本和视觉令牌分别设置独立的跳过阈值，自适应地保留关键专家。此外，MoDES采用基于单调性假设的**前沿搜索算法**，将最优阈值对的搜索时间从数天压缩至数小时。

实验结果表明，MoDES在多个主流MoE MLLM上均取得显著优势。在Kimi-VL-A3B-Instruct上跳过83%专家时，MoDES保持96.25%的平均性能，相较于MC-MoE提升7.93%；在Qwen3-VL-MoE-30B-A3B-Instruct上跳过88%专家时，性能提升高达10.67%（97.33% vs. 86.66%）。同时，MoDES实现了预填充阶段2.16倍、解码阶段1.26倍的推理加速。消融研究进一步验证了GMLG和DMT对性能提升的关键作用：仅使用局部策略时ChartQA为82.38，加入GMLG后提升至84.20（跳过83%）。

**方法定位**：MoDES属于训练无关的MoE推理加速方法，与基于路由概率的NAEE、结合量化的MC-MoE、以及可微分跳过的DiEP等基线相比，其独特之处在于首次将层级别的全局贡献差异和令牌级别的模态差异同时纳入专家跳过决策。该方法不修改模型权重，可直接部署于现有MoE MLLM，具有较好的通用性和即插即用特性。

**局限与展望**：作为训练无关框架，MoDES可能无法达到训练感知方法的理论上限；前沿搜索依赖的单调性假设在复杂模型中可能不成立；校准数据集仅使用GQA，跨分布泛化能力有待验证；目前仅评估了视觉语言任务，在音频等其他模态上的适用性尚不明确。

## 背景与动机

### 混合专家架构在多模态大模型中的效率瓶颈

多模态大语言模型（MLLM）在视觉问答、图像描述、视频理解等任务上取得了显著进展，但其庞大的参数规模带来了高昂的推理成本。混合专家（Mixture-of-Experts, MoE）架构通过稀疏激活机制，在保持模型容量的同时降低了计算量，成为当前主流 MLLM 的重要设计选择。典型的 MoE 层将前馈网络（FFN）替换为多个并行的专家子网络，并通过路由器为每个 token 选择 top-k 个专家进行激活：

$$ \pi _ { m } ^ { ( l ) } = \frac { \exp ( r _ { m } ^ { ( l ) } ) } { \sum _ { \hat { m } = 1 } ^ { M } \exp ( r _ { \hat { m } } ^ { ( l ) } ) } $$

$$ \mathbf { y } ^ { ( l + 1 ) } = \sum _ { m \in S ^ { ( l ) } } \pi _ { m } ^ { ( l ) } \cdot \mathtt { E x p e r t } _ { m } ^ { ( l ) } ( \mathbf { x } ^ { ( l ) } ) $$

然而，即使采用稀疏激活，MoE MLLM 的推理延迟和显存占用仍然严重制约其实际部署。以 Kimi-VL-A3B-Instruct 和 Qwen3-VL-MoE-30B-A3B-Instruct 为例，单层专家数量可达 32 至 128 个，在视觉 token 数量庞大的场景下，FFN 层的计算量成为推理的核心瓶颈。因此，如何在保持模型性能的前提下进一步减少专家计算量，成为 MoE MLLM 高效推理的关键问题。

### 现有专家跳过方法的局限性

为降低 MoE 的推理成本，研究者提出了多种专家跳过（expert skipping）方法，其核心思想是根据路由概率或专家相似性，动态跳过对输出贡献较小的专家。代表性工作包括：

- **NAEE**：基于局部路由概率的专家跳过方法，通过累积概率阈值决定保留哪些专家。
- **MC-MoE**：结合注意力保护机制和权重量化的专家跳过策略，在跳过专家的同时引入混合精度量化以进一步压缩模型。
- **DiEP**：利用路由概率和专家间相似性的可微分专家跳过方法，通过端到端搜索确定跳过策略。

这些方法在纯文本 LLM 上取得了一定效果，但当直接迁移到 MoE MLLM 时，性能出现了显著下降。如 Figure 1 和 Table 1 所示，在 Kimi-VL-A3B-Instruct 上跳过 83% 专家时，现有最优基线方法（如 DiEP、MC-MoE）的平均性能下降超过 11%（从约 99% 降至 88% 以下），而 MoDES 则保持了 96.25% 的平均准确率。这一巨大差距揭示了现有方法的两个根本性盲区。

### 两大被忽视的关键因素

**因素一：专家的全局层贡献不均衡**

现有方法仅依赖局部路由概率 $\pi_i^{(l)}$ 来估计专家重要性，忽略了不同层对最终输出的影响存在显著差异。如 Figure 2 所示，在 Kimi-VL-A3B-Instruct 上对不同层范围施加 top-k 专家路由限制时，浅层专家减少带来的性能下降远大于深层。这一现象表明，浅层专家对最终输出的全局贡献更大，而仅凭局部概率无法捕捉这种层次敏感的差异性。因此，需要一种能够整合全局层重要性的机制来指导专家跳过决策。

**因素二：不同模态 token 间的行为差异**

MoE MLLM 同时处理文本和视觉两种模态的 token，但现有方法对所有 token 一视同仁地应用相同的跳过策略。Figure 3 的模态差距分析揭示了关键差异：（1）t-SNE 可视化显示，预 FFN 层的文本和视觉 token 在表示空间中分布迥异；（2）视觉 token 在 FFN 前后的余弦相似度显著高于文本 token，表明专家处理对视觉 token 的表示改变较小；（3）视觉 token 与 FFN 权重的夹角更接近 90°，进一步说明视觉 token 与专家权重的交互程度较低。这些发现共同指向一个结论：**视觉 token 的专家冗余度远高于文本 token**，因此应当以更激进的比例跳过视觉 token 对应的专家。

### MoDES 的动机与设计思路

基于上述分析，本文提出 MoDES（Mixture-of-Experts with Dynamic Expert Skipping），这是首个面向 MoE MLLM 的无需训练的（training-free）自适应专家跳过框架。MoDES 的核心设计围绕两个关键创新：

1. **全局调制的局部门控（GMLG）**：通过离线校准数据计算每层的全局重要性因子 $\alpha^{(l)}$，将其与局部路由概率 $\pi_i^{(l)}$ 结合为专家重要性得分 $s_i^{(l)} = \alpha^{(l)} \cdot \pi_i^{(l)}$，从而在跳过决策中同时考虑局部贡献和全局层重要性。

2. **双模态阈值（DMT）**：为文本 token 和视觉 token 分别设置独立的跳过阈值 $\tau_t$ 和 $\tau_v$，使视觉 token 能够跳过更多专家，而文本 token 保留更多专家，实现模态感知的自适应跳过。

此外，MoDES 还引入了基于单调性假设的前沿搜索算法，将阈值搜索时间从数天降至数小时，并通过定制 CUDA 内核实现实际推理加速。实验表明，在跳过 83%–88% 专家的极端条件下，MoDES 仍能保持超过 95% 的原模型性能，同时实现预填充约 2× 和解码约 1.2× 的加速。

## 核心创新

MoDES 的核心创新在于首次针对 MoE 多模态大语言模型（MLLM）的推理效率问题，提出了一个 **training-free 的自适应专家跳过框架**。与现有方法相比，其关键突破体现在两个 **changed slots** 上，分别解决了全局层重要性不均衡和模态间行为差异这两个被忽略的瓶颈。

### 从局部路由到全局调制的门控（GMLG）

现有专家跳过方法（如 **DiEP**、**NAEE**）仅依赖局部的路由概率 $\pi_i^{(l)}$ 来估计专家重要性。然而，MoDES 的动机分析（Figure 2）揭示了一个关键现象：浅层专家对最终输出的影响远大于深层专家——当减少浅层的 top-k 专家路由时，性能下降更为剧烈。这意味着，**仅凭局部路由概率无法捕捉专家在不同层上的全局贡献差异**。

为此，MoDES 引入了 **Globally-Modulated Local Gating (GMLG)** 机制，将专家重要性得分从单一的局部概率修改为全局因子与局部概率的乘积：

$$s_i^{(l)} = \alpha^{(l)} \cdot \pi_i^{(l)}$$

其中，全局因子 $\alpha^{(l)}$ 通过离线校准数据计算得到——对每个校准样本，计算原模型与跳过第 $l$ 层所有专家后的模型在输出分布上的 KL 散度，并取平均：

$$\alpha^{(l)} = \frac{1}{N} \sum_{j=1}^{N} \mathcal{D}_{\mathrm{KL}} \left( \mathtt{prob}_j \| \mathtt{prob}_j^{(l)} \right)$$

这一设计将“该层专家对最终输出的扰动程度”量化为一个可离线计算的标量，并直接调制到每个 token 的局部路由决策中。消融实验证实了 GMLG 的决定性作用：在 Skip 83% 的设置下，仅使用局部概率的变体在 ChartQA 上仅为 82.38，加入 GMLG 后提升至 84.20（Table 4）。

### 从统一阈值到双模态阈值（DMT）

现有方法对所有 token 使用统一的跳过阈值，忽视了文本 token 和视觉 token 在 FFN 层中的行为差异。MoDES 通过模态差距分析（Figure 3）发现：视觉 token 在 FFN 前后的余弦相似度更高，且与 FFN 权重的夹角更接近 90°，表明 **FFN 专家对视觉 token 的影响显著小于对文本 token 的影响**，即视觉 token 具有更高的专家冗余度。

基于此，MoDES 将跳过阈值策略从单一的跨模态阈值修改为 **Dual-Modality Thresholding (DMT)**——为文本 token 和视觉 token 分别设置阈值 $\tau_t$ 和 $\tau_v$：

$$\{ \mathtt{Expert}_i^{(l)} \mid s_i^{(l)} < \tau_{\mathrm{t}} \cdot \mathbb{I}_{\mathrm{t}} + \tau_{\mathrm{v}} \cdot \mathbb{I}_{\mathrm{v}} \}$$

当某个专家的重要性得分低于其对应模态的阈值时，该专家被跳过。这一设计使得模型能够对视觉 token 更激进地跳过专家，而对文本 token 保留更多计算。可视化结果（Figure 8）显示，视觉 token 的专家跳过比例系统性高于文本 token，验证了模态感知策略的有效性。

### 高效阈值搜索的配套创新

双模态阈值引入了二维搜索空间，暴力搜索耗时数天。MoDES 基于单调性假设设计了 **前沿搜索算法**（Algorithm 1），将搜索时间从数天降至约 2 小时（约 45× 加速，Figure 5），且不影响性能。这一工程创新使得 DMT 在实际部署中可行。

### 创新总结

| 设计维度 | 基线方法 | MoDES (changed slots) |
|---------|---------|----------------------|
| 专家重要性估计 | 仅局部路由概率 $\pi_i^{(l)}$ | 全局调制得分 $s_i^{(l)} = \alpha^{(l)} \cdot \pi_i^{(l)}$ (GMLG) |
| 跳过阈值策略 | 统一阈值，无模态区分 | 双模态阈值 $\tau_t, \tau_v$ (DMT) |
| 层重要性建模 | 无全局层信息 | 离线 KL 散度校准的 $\alpha^{(l)}$ |
| 阈值搜索 | 手动/网格搜索（数天） | 前沿搜索（约 2 小时） |

这两个核心 changed slots 共同作用，使得 MoDES 在极高跳过比例下仍能保持性能：在 Kimi-VL-A3B-Instruct 上跳过 83% 专家时，MoDES 保持 96.25% 平均性能，而最强基线 DiEP 下降超过 11%（Table 1）；在 Qwen3-VL-MoE-30B-A3B-Instruct 上跳过 88% 专家时，性能提升达 10.67%（97.33% vs. 86.66%，Table 3）。这些结果表明，**层次敏感且模态感知的专家跳过策略**是 MoDES 相对于现有 training-free 方法的核心优势所在。

## 整体框架

MoDES 是一个 **training-free** 的推理加速框架，其核心目标是在不修改模型参数的前提下，自适应地跳过 MoE MLLM 中冗余的 FFN 专家，从而在保持精度的同时显著降低计算开销。

### Pipeline 总览

MoDES 的推理流程由三个关键模块串联构成，如图 Figure 4 所示：

![[assets/figures/papers/paper_list_l767_https_arxiv_org_abs_2511_15690/figures/004_Figure_4.jpg]]
*Figure 4: Overview of MoDES. At inference, use a text token (e.g., ■ above) at the l-th FFN layer as an example. (a) We compute importance scores*

1.  **全局调制的局部门控 (GMLG)**：对于每一层 MoE FFN，首先计算每个专家的局部路由概率 $\pi_i^{(l)}$，然后乘以一个离线校准得到的全局层重要性因子 $\alpha^{(l)}$，得到最终的专家重要性得分 $s_i^{(l)} = \alpha^{(l)} \cdot \pi_i^{(l)}$。这一设计解决了浅层专家比深层专家对最终输出影响更大的瓶颈。
2.  **双模态阈值 (DMT)**：针对视觉令牌的专家冗余度高于文本令牌的模态差异，MoDES 为文本令牌和视觉令牌分别设置跳过阈值 $\tau_t$ 和 $\tau_v$。当专家重要性得分 $s_i^{(l)}$ 低于其对应模态的阈值时，该专家被跳过。
3.  **前沿搜索算法**：在离线阶段，MoDES 通过一个基于单调性假设的前沿搜索算法（Algorithm 1），在给定目标跳过比例 $\rho$ 的约束下，高效地确定最优阈值对 $(\tau_t, \tau_v)$。该算法将搜索复杂度从朴素搜索的 $\mathcal{O}(D^2)$ 降至 $\mathcal{O}(ND)$，将搜索时间从数天缩短至数小时。

### 输入输出流

在推理时，对于第 $l$ 层 MoE FFN 的输入令牌 $\mathbf{x}^{(l)}$：

1.  **输入**：令牌的隐藏状态 $\mathbf{x}^{(l)}$ 及其模态指示符（文本或视觉）。
2.  **GMLG 评分**：计算该令牌对所有 $M$ 个专家的路由概率 $\pi_i^{(l)}$，并与预计算的全局因子 $\alpha^{(l)}$ 相乘，得到重要性得分向量 $\mathbf{s}^{(l)}$。
3.  **DMT 筛选**：根据令牌模态选择对应阈值 $\tau \in \{\tau_t, \tau_v\}$，筛选出满足 $s_i^{(l)} \ge \tau$ 的专家子集 $\tilde{S}^{(l)}$ 进行实际计算。
4.  **输出**：仅对被选中的专家执行 FFN 计算并加权聚合，输出 $\mathbf{y}^{(l+1)} = \sum_{m \in \tilde{S}^{(l)}} \pi_m^{(l)} \cdot \mathtt{Expert}_m^{(l)}(\mathbf{x}^{(l)})$。

### 关键设计决策

-   **全局因子 $\alpha^{(l)}$ 的离线校准**：通过在一组校准数据（如 GQA 的 1024 个随机样本）上，逐层屏蔽所有专家并计算与原模型输出分布的 KL 散度来量化每层的全局重要性：$\alpha^{(l)} = \frac{1}{N} \sum_{j=1}^{N} \mathcal{D}_{\mathrm{KL}} \left( \mathtt{prob}_j \| \mathtt{prob}_j^{(l)} \right)$。这一过程无需梯度，且 1024 个样本已足以实现大部分性能提升（Table III）。
-   **模态感知的阈值解耦**：文本和视觉令牌在 FFN 前后的余弦相似度及与 FFN 权重的夹角存在显著差异（Figure 3 Middle/Right），证明专家对视觉令牌的影响更小。DMT 通过独立阈值 $\tau_t$ 和 $\tau_v$ 充分利用了这一冗余差异，使得视觉令牌可以跳过更多专家。
-   **CUDA Kernel 实现**：为获得实际推理加速，MoDES 在 CUDA 内核中实现了双模态阈值比较和组 GEMM 操作（Appendix B），在 Kimi-VL-A3B-Instruct 上实现了 prefilling 2.16×、decoding 1.26× 的加速比。

## 核心模块与公式推导

MoDES 是一个训练无关（training-free）的推理加速框架，核心由两个模块构成：**全局调制的局部门控（GMLG）** 和 **双模态阈值（DMT）**。GMLG 负责为每个令牌的每个专家生成重要性得分，DMT 则根据令牌模态决定跳过哪些专家。两者配合，实现了层次敏感且模态感知的专家跳过。

### 全局调制的局部门控（GMLG）

MoE 层的标准输出为 top-k 专家的加权聚合：

$$ \mathbf { y } ^ { ( l + 1 ) } = \sum _ { m \in S ^ { ( l ) } } \pi _ { m } ^ { ( l ) } \cdot \mathtt { E x p e r t } _ { m } ^ { ( l ) } ( \mathbf { x } ^ { ( l ) } ) $$

其中路由概率 $\pi _ { m } ^ { ( l ) }$ 由 Softmax 归一化得到：

$$ \pi _ { m } ^ { ( l ) } = \frac { \exp ( r _ { m } ^ { ( l ) } ) } { \sum _ { \hat { m } = 1 } ^ { M } \exp ( r _ { \hat { m } } ^ { ( l ) } ) } $$

仅依赖局部路由概率 $\pi_i^{(l)}$ 无法反映专家在不同层对最终输出的全局贡献差异。MoDES 引入全局因子 $\alpha^{(l)}$ 来调制局部概率，得到重要性得分：

$$ s _ { i } ^ { ( l ) } = \alpha ^ { ( l ) } \cdot \pi _ { i } ^ { ( l ) } $$

全局因子 $\alpha^{(l)}$ 通过离线校准计算：在少量校准样本上，逐层跳过所有专家，计算原模型与跳过该层专家的模型在输出分布上的 KL 散度平均：

$$ \alpha ^ { ( l ) } = \frac { 1 } { N } \sum _ { j = 1 } ^ { N } \mathcal { D } _ { \mathrm { K L } } \left( \mathtt { p r o b } _ { j } \| \mathtt { p r o b } _ { j } ^ { ( l ) } \right) $$

其中 $\mathtt{prob}_j$ 和 $\mathtt{prob}_j^{(l)}$ 分别为原模型和跳过第 $l$ 层专家的模型对第 $j$ 个校准样本的输出概率。$\alpha^{(l)}$ 越大，说明该层专家对最终输出的影响越大——实验表明浅层 $\alpha^{(l)}$ 显著高于深层（Figure 7），这与 Figure 2 中浅层专家更为关键的发现一致。实际推理时，$\alpha^{(l)}$ 经跨层归一化后使用：$\widetilde { \alpha ^ { ( l ) } } = \frac { \alpha ^ { ( l ) } } { \sum _ { l ^ { \prime } = 1 } ^ { L } \alpha ^ { ( l ^ { \prime } ) } }$。

![[assets/figures/papers/paper_list_l767_https_arxiv_org_abs_2511_15690/figures/002_Figure_2.jpg]]
*Figure 2: Performance on image (i.e., (a)-(b)) and video*

![[assets/figures/papers/paper_list_l767_https_arxiv_org_abs_2511_15690/figures/003_Figure_3.jpg]]
*Figure 3: (Left) t-SNE [52] visualization of pre-FFN text/vision tokens across all layers. (Middle) Cosine similarity between pre-FFN and post-FFN text/vision tokens across layers. (Right) Angle between text/vision tokens and weights across different FFN layers. Here, GQA [25] dataset is used as the model inputs, and the model is employed the same as that in Fig. 2*

### 双模态阈值（DMT）

MoDES 的第二个关键洞察来自模态差距分析（Figure 3）：视觉令牌在 FFN 前后的余弦相似度高于文本令牌，且与 FFN 权重的夹角更接近 90°，说明视觉令牌受专家影响更小、冗余度更高。因此，MoDES 为文本令牌和视觉令牌分别设置阈值 $\tau_t$ 和 $\tau_v$，专家跳过条件为：

$$ \{ \mathtt { E x p e r t } _ { i } ^ { ( l ) } \mid s _ { i } ^ { ( l ) } < \tau _ { \mathrm { t } } \cdot \mathbb { I } _ { \mathrm { t } } + \tau _ { \mathrm { v } } \cdot \mathbb { I } _ { \mathrm { v } } \} $$

当重要性得分 $s_i^{(l)}$ 低于对应模态的阈值时，该专家被跳过。

### 阈值搜索

最优阈值对 $(\tau_t, \tau_v)$ 通过在给定跳过比例 $\rho$ 约束下最小化输出分布 KL 散度来确定：

$$ \operatorname* { m i n } _ { \tau _ { \mathrm { t } } \in \mathcal { B } , \tau _ { \mathrm { v } } \in \mathcal { B } } f ( \tau _ { \mathrm { t } } , \tau _ { \mathrm { v } } ) \quad \mathrm { s . t . } \quad g ( \tau _ { \mathrm { t } } , \tau _ { \mathrm { v } } ) \geq \rho $$

其中 $\mathcal{B}$ 为离散化的阈值候选集，$g(\cdot)$ 为实际跳过比例。MoDES 提出基于单调性假设的前沿搜索算法（Algorithm 1），将搜索复杂度从朴素搜索的 $\mathcal{O}(D^2)$ 降至 $\mathcal{O}(ND)$，搜索时间从数天缩短至约 2 小时（Figure 5）。

### 关键公式速查

| 公式 | 含义 |
|------|------|
| $s_i^{(l)} = \alpha^{(l)} \cdot \pi_i^{(l)}$ | 全局调制后的专家重要性得分 |
| $\alpha^{(l)} = \frac{1}{N}\sum_{j=1}^N D_{\mathrm{KL}}(\mathtt{prob}_j \| \mathtt{prob}_j^{(l)})$ | 通过 KL 散度校准的全局层因子 |
| $\{ \mathtt{Expert}_i^{(l)} \mid s_i^{(l)} < \tau_{\mathrm{t}} \cdot \mathbb{I}_{\mathrm{t}} + \tau_{\mathrm{v}} \cdot \mathbb{I}_{\mathrm{v}} \}$ | 双模态阈值跳过条件 |

消融实验（Table 4）证实，GMLG 和 DMT 对性能提升均至关重要：仅使用局部概率（w/o GMLG）时 ChartQA 为 82.38，加入 GMLG 后提升至 84.20（Skip 83%）；进一步加入 DMT 后达到最优。校准样本数 $N=1024$ 即可实现大部分性能增益（Table III），加倍样本数收益递减。

## 实验与分析

### 主要结果：MoDES 在极高跳过高率下保持性能领先

MoDES 在多个 MoE 多模态大语言模型上，以极高的专家跳过比例实现了最优的性能-效率权衡。在 Kimi-VL-A3B-Instruct 上，当跳过 83% 的专家时，MoDES 仍能保持原始模型 **96.25%** 的平均准确率，而最强基线方法 DiEP 和 MC-MoE 分别下降超过 11%（DiEP 平均 88.32%），MoDES 相对提升 **+7.93%**（Table 1）。在较低的 50% 跳过比例下，MoDES 平均准确率达到 **99.91%**，超过 DiEP 的 98.17% 和 MC-MoE 的 97.69%，分别领先 1.74% 和 2.22%。

![[assets/figures/papers/paper_list_l767_https_arxiv_org_abs_2511_15690/figures/005_Table_1.jpg]]
*Table 1: Performance comparisons for Kimi-VL-A3B-Instruct [50] across various expert skipping ratios. We mark the target ρ (Eq. (6)) and the practical skipping ratio x% (i.e., “Skip x% Experts”) in the table. For each method, we compute the score proportion relative to the default setting*

在更大规模的 Qwen3-VL-MoE-30B-A3B-Instruct 上，MoDES 的优势进一步放大。当跳过 88% 专家时，MoDES 取得 **97.33%** 的平均准确率，而 MC-MoE 仅为 86.66%，性能提升高达 **+10.67%**（Table 3）。这一结果验证了 GMLG 和 DMT 在更大模型上的可扩展性。

![[assets/figures/papers/paper_list_l767_https_arxiv_org_abs_2511_15690/figures/007_Table_3.jpg]]
*Table 3: Performance comparisons across different backbones. InternVL series employs Qwen3 [64] and GPT-OSS [46] as LLM backbones for 30B and 20B models, respectively. The number of experts for each layer of models from upper to lower is 128, 128, and 32*

跨骨干网络的泛化实验（Table 3）覆盖了 InternVL-3.5-30B-A3B-HF（128 专家/层）和 InternVL-3.5-20B-A3B-HF（32 专家/层），MoDES 在所有设置下均一致优于基线方法，表明其不依赖于特定的模型架构或专家数量配置。

### 推理速度实测

MoDES 在实际推理速度上同样带来显著提升。在单张 H200 GPU 上，对于 Kimi-VL-A3B-Instruct（83% 跳过比例），MoDES 的预填充阶段加速 **2.16×**，解码阶段加速 **1.26×**；对于 Qwen3-VL-MoE-30B-A3B-Instruct（88% 跳过比例），预填充加速 **2.03×**，解码加速 **1.24×**（Figure 6）。加速效果在预填充阶段更为明显，这与 MoE 层在长序列预填充中计算占比较高的事实一致。

![[assets/figures/papers/paper_list_l767_https_arxiv_org_abs_2511_15690/figures/008_Figure_6.jpg]]
*Figure 6: Inference speed for (Upper) Kimi-VL-A3B-Instruct [50] and (Lower) Qwen3-VL-MoE-30B-A3B-Instruct [26] on a single H200 GPU. The expert skipping ratios for the former and the latter are 83% and 88%, respectively. The batch size for prefilling is 8, and the sequence length for decoding is 1024*

### 消融研究：GMLG 与 DMT 的独立贡献

消融实验（Table 4）系统拆解了 GMLG 和 DMT 两个核心组件的贡献。以 Kimi-VL-A3B-Instruct 在 83% 跳过比例下的表现为基准：

- **移除 GMLG（仅用局部路由概率）**：ChartQA 上准确率从完整 MoDES 的 84.20 降至 82.38，证明全局层重要性调制对维持性能至关重要。
- **移除 DMT（使用单一阈值）**：性能同样出现明显下降，验证了模态感知阈值策略的必要性。
- **同时移除两者**：性能退化最为严重，说明 GMLG 和 DMT 具有互补效应。

### 校准与搜索效率

校准效率方面，仅需 **1024 个样本**（来自 GQA 数据集）即可实现大部分性能提升，将样本数翻倍带来的收益递减（Table III），表明校准成本可控。

阈值搜索方面，所提出的前沿搜索算法（Algorithm 1）将搜索时间从朴素方法的数天缩短至约 **2 小时**，加速约 **45 倍**（Figure 5），且不影响最终性能。搜索空间大小 D 的消融（Table IV）显示，适度增大 D 可带来性能提升，但边际收益递减，验证了前沿搜索在效率与精度间的良好平衡。

![[assets/figures/papers/paper_list_l767_https_arxiv_org_abs_2511_15690/figures/009_Figure_5.jpg]]

### 量化兼容性

MoDES 与量化技术可正交叠加。采用 MC-MoE 的混合精度量化策略（MoE-FFN 使用混合精度，其他层使用 4-bit 权重量化）后，MoDES 在保持高跳过比例的同时进一步压缩模型体积，且性能损失极小（Table 2），表明 training-free 的跳过策略与训练后量化之间不存在冲突。

![[assets/figures/papers/paper_list_l767_https_arxiv_org_abs_2511_15690/figures/006_Table_2.jpg]]
*Table 2: Performance of combination with quantization. MoDES employs the quantization strategy in MC-MoE [22]: weightonly mixed-precision quantization for MoE-based FFNs and 4-bit weight-only quantization for other layers*

### 失败模式与局限性分析

尽管 MoDES 在多数场景下表现优异，但仍存在以下局限：

1. **校准数据集敏感性**：不同校准数据集（GQA、VQAv2、COCO Caption）对最终性能有一定影响（Table 5），当前仅在 GQA 上校准的策略可能在分布外任务上表现次优。
2. **单调性假设依赖**：前沿搜索依赖于“阈值越严格，跳过比例越高”的单调性假设。虽然在所测试的模型中经验成立，但在某些具有非单调路由行为的复杂 MoE 架构中可能失效。
3. **视觉令牌的极端跳过**：DMT 倾向于为视觉令牌设置更宽松的阈值（跳过更多专家），这在多数视觉理解任务中影响较小，但在需要细粒度视觉推理的任务（如指代表达理解）上可能导致局部信息丢失。
4. **未与训练结合**：作为纯 training-free 框架，MoDES 无法像训练感知方法那样通过学习调整路由策略来进一步优化，其性能上限受限于原始模型的专家冗余度。

![[assets/figures/papers/paper_list_l767_https_arxiv_org_abs_2511_15690/figures/013_Table_5.jpg]]
*Table 5: Ablation results of using 3 different datasets for both calibration and frontier search (C&S)*

### 关键图表结论汇总

- **Figure 1**：MoDES 在 Kimi-VL 和 Qwen3-VL 上，跨所有跳过比例均一致超越 SOTA 基线，且优势随跳过比例增大而扩大。
- **Figure 2**：浅层专家对性能影响远大于深层专家——将 top-k 限制应用于浅层时性能急剧下降，而深层几乎不受影响，直接支撑了 GMLG 中全局层因子的设计动机。
- **Figure 3**：视觉令牌在 FFN 前后的余弦相似度显著高于文本令牌，且视觉令牌与 FFN 权重的夹角更接近 90°，说明专家对视觉令牌的变换作用更弱，为 DMT 中视觉令牌更高跳过率提供了实证基础。
- **Figure 8**：不同层和模态的实际跳过比例分布显示，浅层保留更多专家，深层跳过更多；视觉令牌跳过比例普遍高于文本令牌，与 GMLG 和 DMT 的设计预期一致。

![[assets/figures/papers/paper_list_l767_https_arxiv_org_abs_2511_15690/figures/001_Figure_1.jpg]]
*Figure 1: Average performance (%) vs. expert skipping ratios (%) across different models [26, 50, 57] and methods [6, 22, 42] on 13 benchmarks (as detailed in Sec. 6.1). The left subfigure is for Kimi-VL-A3B-Instruct [50] and the right subfigure is for Qwen3- VL-MoE-30B-A3B-Instruct [26]*

![[assets/figures/papers/paper_list_l767_https_arxiv_org_abs_2511_15690/figures/010_Figure_8.jpg]]
*Figure 8: Visualization of expert skipping ratios (%) across modalities and layers on 13 benchmarks (Sec. 6.1). The left subfigure is for Kimi-VL-A3B-Instruct [50] and the right subfigure is for Qwen3-VL-MoE-30B-A3B-Instruct [26]. The overall skipping ratios for the former and the latter are 83% and 88%, respectively*

### 补充图表

![[assets/figures/papers/paper_list_l767_https_arxiv_org_abs_2511_15690/figures/012_Figure_7.jpg]]
*Figure 7: Visualization results of global contributions*

## 方法谱系与知识库定位

### 方法谱系：从静态路由到训练无关的动态专家跳过

MoDES 属于 **训练无关（training-free）的 MoE 推理加速方法**，其核心思想是通过动态跳过冗余专家来降低计算量，而不需要对模型进行任何微调或重新训练。这一方法谱系可追溯到两类工作：

**1. 基于路由概率的专家跳过方法**

现有方法主要利用局部路由概率来决定跳过哪些专家：
- **NAEE**直接基于路由概率的累积和设定跳过阈值，当某个专家的概率低于阈值时将其跳过。该方法在纯文本 MoE 上表现良好，但应用到 MLLM 时忽略了层间重要性和模态差异。
- **DiEP**在路由概率基础上引入可微分的跳过机制，通过相似性度量进一步筛选专家。然而，其单一阈值策略无法区分文本和视觉令牌的冗余程度差异。
- **MC-MoE**结合了注意力保护机制和量化技术，在跳过专家的同时尝试保护关键注意力模式。但其专家重要性估计仍局限于局部路由信号。

这些方法的共同瓶颈在于：**仅依赖局部路由概率，忽略了专家在不同层对最终输出的全局贡献差异，以及不同模态令牌间的行为差异**。当跳过比例超过 80% 时，这些方法的平均性能下降超过 11%（Table 1），而 MoDES 仅下降约 3.75%。

**2. 降低 top-k 值的直接方法**

最简单的效率提升手段是直接降低每个令牌激活的专家数量（如将默认的 k=6 降至 k=3、k=2 或 k=1）。这种方法的缺陷在于对所有层和所有令牌“一视同仁”，无法利用浅层专家比深层专家更关键（Figure 2）以及视觉令牌专家冗余度更高（Figure 3）的结构性特征。

### MoDES 的核心创新定位

MoDES 在方法谱系中的独特定位体现在两个关键机制：

**全局调制的局部门控（GMLG）** 通过离线校准数据计算每层的全局重要性因子 $\alpha^{(l)}$（Eq. (4)），将其与局部路由概率 $\pi_i^{(l)}$ 相乘得到专家重要性得分 $s_i^{(l)} = \alpha^{(l)} \cdot \pi_i^{(l)}$（Eq. (3)）。这一设计使得浅层专家的高重要性得以保留，而深层专家的冗余可以被更激进地利用。消融实验表明，仅使用局部概率（w/o GMLG）在 ChartQA 上为 82.38，加入 GMLG 后提升至 84.20（Skip 83%，Table 4）。

**双模态阈值（DMT）** 为文本令牌和视觉令牌分别设置跳过阈值 $\tau_t$ 和 $\tau_v$（Eq. (5)），利用视觉令牌在 FFN 前后余弦相似度更高、与 FFN 权重夹角更接近 90° 的模态差距特性（Figure 3），对视觉令牌施加更激进的跳过策略。这一设计是 MoDES 在 MLLM 场景下区别于所有纯文本 MoE 加速方法的关键。

### 适用边界与知识库定位

**适用场景**：
- 基于 MoE 架构的多模态大语言模型（已验证 Kimi-VL-A3B-Instruct、Qwen3-VL-MoE-30B-A3B-Instruct、InternVL 系列）
- 需要高跳过比例（>80%）且希望保持 95% 以上原始性能的场景
- 推理延迟敏感的部署环境（prefilling 加速 2.16×，decoding 加速 1.26×）

**不适用或需谨慎的场景**：
- 纯文本 LLM 的 MoE 加速（MoDES 的 DMT 机制依赖模态差异，在纯文本场景下退化为单一阈值，但 GMLG 仍可发挥作用）
- 需要训练感知优化以获得极致性能的场景（MoDES 是训练无关框架，可能无法达到训练感知方法的理论上限）
- 非视觉语言的多模态任务（如音频、视频动作检测），模态差距的假设需要重新验证

**知识库贡献**：
1. **首次揭示了 MoE MLLM 中专家重要性的层次不均衡性和模态差异**，为后续方法提供了可复用的分析框架
2. **前沿搜索算法**（Algorithm 1）将双阈值搜索从 $\mathcal{O}(D^2)$ 降至 $\mathcal{O}(D)$，搜索时间从数天降至约 2 小时（Figure 5），为实际部署提供了可行路径
3. **与量化的正交兼容性**（Table 2）表明 MoDES 可与模型压缩技术叠加使用，进一步降低推理成本

### 局限性与开放问题

**已知局限**：
1. **训练无关的固有上限**：MoDES 无法像训练感知方法那样学习最优的专家路由策略，在高跳过比例下的性能恢复存在天花板
2. **校准数据依赖**：全局因子 $\alpha^{(l)}$ 的估计依赖于校准数据集的选择（本文使用 GQA 的 1024 个随机样本），虽然消融实验表明 1024 样本已足够（Table III），但不同分布下的泛化能力需要进一步验证
3. **单调性假设**：前沿搜索依赖于 KL 散度随阈值单调变化的假设，虽然在经验上有效，但在某些复杂模型或任务中可能不成立
4. **实现优化空间**：虽然 CUDA 内核实现带来了实际加速，但 Group GEMM 等密集操作仍存在进一步优化的空间

**开放问题**：
1. MoDES 的 GMLG 机制是否适用于纯文本 MoE LLM 或其他类型的 MoE 模型（如语音、统一多模态）？
2. 能否将 MoDES 与训练结合，通过少量微调学习更优的全局因子或阈值策略？
3. 在更细粒度的视觉任务（如图像分割、视频动作检测）上，模态感知的跳过策略是否仍然有效？视觉令牌内部的异质性是否值得进一步建模？
4. 能否自动化确定校准样本数量和搜索空间大小，减少人工调参成本？
5. 前沿搜索的单调性假设在什么情况下会失败？如何检测并自适应地切换到更鲁棒的搜索策略？

## 原文 PDF

![[paperPDFs/CVPR_2026/MoDES_Accelerating_Mixture_of_Experts_Multimodal_Large_Language_Models_via_Dynamic_Expert_Skipping.pdf]]
