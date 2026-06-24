---
title: "Cat-PO: Cross-modal Adaptive Token-rewards for Preference Optimization in Truthful Multimodal LLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Cat_PO_Cross_modal_Adaptive_Token_rewards_for_Preference_Optimization_in_Truthful_Multimodal_LLMs.pdf
openreview_forum_id: iIbe6qDN0A
aliases:
- CP
- Cat-PO
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "对每个响应 token 赋予基于跨模态注意力的视觉相关性奖励（全局、局部、语义三层次），并整合到 DPO 损失中进行 token 级优化。"
primary_logic: "利用 MLLM 内在的跨模态注意力机制，计算 token 级别的多层级视觉相关性分数，并将其映射为奖励权重，融入带 KL 正则化的加权 DPO 损失，从而在不引入外部工具的前提下实现更精细的幻觉抑制。"
claims:
- "仅对奖励最高的前 50% token 应用 DPO 即可改善 AMBER-F1 和 MM-Hal 指标，对所有 token 应用则效果更优。"
- "Cat-PO 在 AMBER-Generation 和 MM-Hal 上超越所有基线方法，CHAIR 降至 4.8，Hal 降至 23.7，MM-Hal Score 升至 2.74，Rate 降至 42.0。"
- "消融实验表明，移除 token 级 KL 正则化或单独使用注意力/相似度均导致性能下降，验证了各模块的必要性。"
- "AMBER (Qwen2.5-VL-3B) 上 F1 = ~91.3"
---

# Cat-PO: Cross-modal Adaptive Token-rewards for Preference Optimization in Truthful Multimodal LLMs

> [!tip] 核心洞察
> 利用 MLLM 内在的跨模态注意力机制，计算 token 级别的多层级视觉相关性分数，并将其映射为奖励权重，融入带 KL 正则化的加权 DPO 损失，从而在不引入外部工具的前提下实现更精细的幻觉抑制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Cat-PO：用于真实多模态LLM的跨模态自适应Token奖励偏好优化 |
| 英文题名 | Cat-PO: Cross-modal Adaptive Token-rewards for Preference Optimization in Truthful Multimodal LLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=iIbe6qDN0A); [GitHub](https://github.com/gavinzzx/CatPO) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Cat-PO |
| Dataset | AMBER (Qwen2.5-VL-3B), MM-Hal (Qwen2.5-VL-3B), Training efficiency |

> [!tip] 效果简介
> - AMBER (Qwen2.5-VL-3B) 上，F1 为 ~91.3，对比 Qwen+DPO: ~87.6，变化 +3.7。
> - MM-Hal (Qwen2.5-VL-3B) 上，Score ↑ 为 ~91.3，对比 Qwen+DPO: ~87.4，变化 +3.9。
> - MM-Hal (Qwen2.5-VL-3B) 上，Rate ↓ 为 ~31%，对比 Qwen+DPO: ~39%，变化 -8%。

## 概述

### 问题瓶颈

多模态大语言模型（MLLM）在视觉问答等任务中频繁产生幻觉——生成与图像内容不一致的文本描述。现有偏好优化方法（如 DPO，Rafailov et al., 2023）在解码阶段对响应中的所有 token 统一处理，忽视了不同 token 与视觉内容关联程度的差异。这种粗粒度的优化策略导致幻觉纠正不够精细，限制了模型真实性的提升。

### 核心思路

Cat-PO 提出了一种**跨模态自适应 Token 奖励偏好优化**方法。其核心洞察在于：利用 MLLM 内在的跨模态注意力机制，计算每个响应 token 的多层级视觉相关性分数，并将其映射为奖励权重，融入带 KL 正则化的加权 DPO 损失中。通过这一机制，模型能够在不引入外部工具的前提下，对与视觉内容高度相关的 token 给予更强的优化信号，对幻觉 token 施加更重的惩罚，从而实现更细粒度的幻觉抑制。

### 方法定位

Cat-PO 属于**Token 级偏好优化**范畴，与现有方法的根本区别在于：

| 对比维度 | 标准 DPO / 现有方法 | Cat-PO |
|---------|-------------------|--------|
| Token 处理 | 所有 token 平等对待（均匀权重） | 基于跨模态注意力的分层视觉相关性奖励 |
| 损失函数 | 标准 DPO 损失 | 加权 DPO 损失 + Token 级 KL 正则化 |
| 外部依赖 | 部分方法依赖外部检测模型或工具 | 仅依赖 MLLM 内在多模态能力 |

在方法谱系中，Cat-PO 与 **TPO**（Gu et al., 2024）同属 Token 级 DPO 方向，但 TPO 的奖励信号源自外部分割模型，而 Cat-PO 完全基于模型内在的跨模态注意力与语义相似度，消除了对外部工具的依赖。

### 主要结果

- **幻觉抑制**：在 LLaVA-v1.5-7B 模型上，Cat-PO 在 AMBER-Generation 的 CHAIR 指标降至 4.8，Hal 降至 23.7；在 MM-Hal 上 Score 升至 2.74，Rate 降至 42.0，全面超越 DPO、CSR、POVID、RLHF-V、V-DPO、TPO 等基线方法。
- **跨模型泛化**：在 Qwen2.5-VL-3B 上，Cat-PO 相比 Qwen+DPO 在 AMBER F1 上提升约 3.7 个百分点，MM-Hal Score 提升约 3.9 个百分点，幻觉率降低约 8 个百分点。
- **计算代价可控**：训练时间较 DPO 增加约 38%（单样本平均 2.9s vs 2.1s），但峰值内存开销几乎不变（+0.07%），整体计算代价可接受。

### 证据强度与局限

**强证据支持**：消融实验（Table 2）系统验证了各模块的必要性——移除 Token 级 KL 正则化或单独使用注意力/相似度均导致性能下降；仅对奖励最高的前 50% token 应用 DPO 即可改善幻觉指标（Figure 1b），使用全部 token 加权效果更优。

**需注意的局限**：所有实验仅基于 RLHF-V 数据集，在其他多模态偏好数据上的泛化性有待检验；对抗样本（POPE adversarial）下性能有 2-4% 的轻微下降；可学习融合权重的尝试反而导致性能下降（Table 4），暗示奖励融合方式仍需进一步研究。

## 背景与动机

多模态大语言模型（MLLM）在视觉问答和图像描述等任务中展现出令人瞩目的能力，但幻觉问题——即生成内容与视觉输入不一致——仍然是制约其可靠性的核心瓶颈。现有的偏好优化方法，如 DPO（Rafailov et al., 2023），通过在偏好数据上最大化正负响应的对数概率差来抑制幻觉，但其在解码阶段对响应中的每个 token 赋予相同权重，忽视了一个关键事实：不同 token 与视觉内容的关联程度存在显著差异。

以图 1(a) 为例，当模型回答“桌上有笔记本电脑和杯子”时，内容词“laptop”（跨模态相似度 0.673）和“cup”（0.633）与视觉区域高度对齐，而功能词“a”（0.336）和“the”（0.160）的视觉关联则弱得多。然而标准 DPO 在优化时对所有 token 一视同仁——无论该 token 是真正基于图像生成的，还是模型凭空想象的幻觉内容。这种粗粒度的优化策略使得幻觉纠正不够精细，限制了模型真实性的进一步提升。

这一观察引出了一个自然的假设：如果能在 DPO 中根据 token 与视觉内容的关联程度赋予差异化的奖励，是否可以更有效地抑制幻觉？图 1(b) 的初步实验提供了有力证据：仅对跨模态注意力奖励最高的前 50% token 应用 DPO，即可在 AMBER-F1 和 MM-Hal 幻觉率上获得改善；当对所有 token 按视觉相关性加权时，效果更为显著。这表明，token 级的视觉相关性信号确实能够引导更精准的幻觉纠正。

然而，如何可靠地量化每个 token 的视觉相关性，并将其有效融入偏好优化框架，仍是一个未被系统解决的问题。现有方法要么依赖外部工具提取视觉线索，要么仅使用单一维度的跨模态信号，未能充分利用 MLLM 内在的多层次视觉理解能力。Cat-PO 正是针对这一缺口，提出利用 MLLM 自身的跨模态注意力机制，从全局、局部和语义三个层次计算 token 级的视觉相关性奖励，并将其整合到带 KL 正则化的加权 DPO 损失中，在不引入外部依赖的前提下实现更细粒度的幻觉抑制。

## 核心创新

Cat-PO 的核心创新在于将多模态大语言模型（MLLM）的幻觉抑制从**响应级粗粒度优化**推进到**token 级细粒度优化**。现有偏好优化方法（如 DPO，Rafailov et al., 2023）在解码阶段对所有 token 一视同仁，忽视了不同 token 与视觉内容关联程度的本质差异——内容词（如“laptop”）与功能词（如“a”）的跨模态注意力强度和语义对齐度截然不同（Figure 1a）。Cat-PO 利用 MLLM 内在的跨模态注意力机制，为每个响应 token 计算多层级视觉相关性奖励，并将其融入带 KL 正则化的加权 DPO 损失，从而在不引入外部工具的前提下实现更精细的幻觉纠正。

### 关键机制变更

与标准 DPO 相比，Cat-PO 在三个关键维度上进行了系统性改造：

**1. Token 级奖励机制：从均匀权重到分层视觉相关性奖励**

标准 DPO 对所有 token 赋予均匀权重，无法区分视觉锚定 token 与幻觉 token。Cat-PO 通过三个互补层次计算每个 token 的视觉相关性分数：

- **全局相关性**（$S_{\mathrm{global}}$）：对 token 在所有图像 patch 上的跨模态注意力分数求和，衡量其整体视觉关联度（Equation 2）。
- **局部相关性**（$S_{\mathrm{local}}$）：基于注意力分布的归一化信息熵，量化 token 对特定图像区域的聚焦程度（Equations 3-4）。
- **语义相关性**（$S_{\mathrm{semantic}}$）：计算 token 嵌入与注意力加权视觉上下文向量的余弦相似度，反映语义层面的跨模态对齐（Equation 5）。

三者通过平衡参数 $\alpha$ 融合为统一的视觉相关性分数（Equation 6），再经 tanh 非线性映射转化为 token 权重（Equation 7）。Figure 5 的可视化验证表明，该机制能有效提升真正视觉相关 token（如物体名词）的权重，同时压低幻觉 token。

**2. 损失函数：从标准 DPO 到加权 DPO**

Cat-PO 将 token 级权重显式集成到 DPO 损失中，形成加权 DPO 损失 $\mathcal{L}_{\mathrm{wDPO}}$（Equation 8）。其核心逻辑是：对偏好响应中与视觉高度对齐的 token 给予更高奖励权重，对非偏好响应中的幻觉 token 施加更重惩罚。这一设计使优化信号精准聚焦于最易产生幻觉的 token 位置。

**3. KL 正则化：从隐式约束到显式 token 加权 KL 惩罚**

标准 DPO 仅通过参考模型的对数概率比提供隐式约束。Cat-PO 引入了显式的 token 级加权 KL 散度惩罚 $\mathcal{L}_{\mathrm{KL}}$（Equation 9），按 token 权重对正负样本分别计算 KL 散度，防止策略模型偏离参考模型过远。消融实验（Table 2）证实，移除该 KL 项会导致 MM-Hal Score 和 CHAIR/Hal 指标显著恶化，验证了其对训练稳定性和幻觉抑制的必要性。

### 创新有效性的实证支撑

Figure 1(b) 的预实验提供了直接的动机证据：仅对奖励最高的前 50% token 应用 DPO 即可改善 AMBER-F1 和 MM-Hal 指标，而对所有 token 应用加权 DPO 效果更优。这一发现直接催生了 Cat-PO 的全 token 加权策略。

消融实验（Table 2）进一步确认了各组件的独立贡献：单独使用跨模态注意力或语义相似度作为奖励信号均可提升性能，但二者结合效果更优，说明多级视觉线索存在互补关系。值得注意的是，尝试可学习融合权重（Equation 11）反而导致性能下降（Table 4），暗示在 DPO 设置下固定等权融合更为鲁棒——这一反直觉发现本身也构成了方法设计的重要洞察。

### 与同类方法的本质区别

相较于其他 token 级优化方法（如 **TPO**，Gu et al., 2024），Cat-PO 的独特之处在于**奖励信号的来源**：TPO 依赖外部信号或启发式规则，而 Cat-PO 完全利用 MLLM 内在的跨模态注意力与语义表示，无需额外模型或工具。相较于视觉引导的 **V-DPO**（Xie et al., 2024），Cat-PO 将视觉引导从响应级细化到 token 级，实现了更精准的幻觉定位与纠正。

## 整体框架

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_iIbe6qDN0A/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our proposed Cat-PO framework: (1) The visual images are first projected into the feature space via CLIP+ViT, and the textual question/response tokens are embedded by LLM tokenizer. (2) Cross-modal attention and semantic similarity are extracted in the multi-modal transformer to hierarchically form the global, local, and semantic relevance scores. (3) Token weights are computed by normalizing these scores with positive/negative sample formulas. (4) The weights are integrated into the standard DPO loss to enhance alignment and mitigate hallucinations*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_iIbe6qDN0A/figures/001_Figure_1.jpg]]
*Figure 1: The motivation of our framework. (a) A visual question answering example where the model identifies "a laptop and a cup" on a table, with cross-modal attention heatmaps and cross-modal similarity scores indicating the model’s visual focus and word importance in the response. (b) A performance comparison of token-rewarded DPO, showing AMBER F1 (↑) improving and MM-Hal Hallucination Rate (↓) declining as the percentage of rewarded tokens increases. (c) A comparison of standard DPO versus our Cross-modal Adaptive Token-rewarded Preference Optimization (Cat-PO). The former uses a flat gradient distribution for maximal likelihood optimization. And the latter employs a targeted gradient distribut...*

Cat-PO 的整体 pipeline 围绕一个核心因果机制展开：**利用 MLLM 内在的跨模态注意力与语义对齐信号，为响应中的每个 token 生成多层级视觉相关性奖励，并将该奖励映射为 token 级权重，融入带 KL 正则化的加权 DPO 损失中进行细粒度优化**。该方法在不引入外部检测模型或工具的前提下，实现了对幻觉 token 的精准抑制。

### 框架总览

如图 2 所示，Cat-PO 框架由四个串联模块构成：

1. **多模态编码**：视觉图像经 CLIP+ViT 投影至特征空间，文本（问题与响应）经 LLM tokenizer 嵌入为 token 序列。
2. **分层视觉相关性计算**：在 MLLM 的跨模态 Transformer 层中，提取文本 token 对图像 patch 的注意力分布与语义嵌入，依次计算三个层级的视觉相关性分数。
3. **Token 权重映射**：将融合后的统一相关性分数通过非线性映射转化为正/负样本的 token 级权重。
4. **加权偏好优化**：将 token 权重集成到 DPO 损失与显式 KL 正则项中，形成最终训练目标。

### 分层视觉相关性奖励

该模块是 Cat-PO 的核心创新，从三个互补维度量化每个响应 token 与视觉内容的关联程度：

- **全局相关性** ($S_{\text{global}}$)：计算 token 对所有图像 patch 的跨模态注意力分数之和（Equation 2），反映 token 的整体视觉参与度。高全局分数意味着该 token 在生成时广泛参考了图像信息。
- **局部相关性** ($S_{\text{local}}$)：基于注意力分布在图像 patch 上的信息熵（Equation 3），定义 $S_{\text{local}} = 1 - H(P_t)/\log N_p$（Equation 4）。分数越高，表示注意力越集中于特定图像区域，token 与局部视觉细节的对齐越紧密。
- **语义相关性** ($S_{\text{semantic}}$)：计算 token 嵌入与注意力加权视觉上下文向量的余弦相似度（Equation 5），衡量 token 在语义空间与视觉内容的对齐程度。

三者通过平衡参数 $\alpha$ 融合为统一视觉相关性分数（Equation 6）：
$$s_i = \alpha \big[ 0.5 \cdot S_{\text{global},i} + 0.5 \cdot S_{\text{local},i} \big] + (1 - \alpha) S_{\text{semantic},i}$$

消融实验证实，单独使用跨模态注意力或语义相似度作为奖励信号均可提升性能，但二者结合效果更优，验证了多级视觉线索的互补性（Table 2）。

### Token 权重映射与加权优化

统一相关性分数 $s_i$ 经 $\tanh$ 非线性映射后，结合基础权重 $\lambda_{\text{ref}}$ 转化为最终 token 权重 $w_i$（Equation 7）。关键设计在于**非对称加权策略**：对偏好响应（$y^+$）中与视觉高度对齐的 token 赋予更高权重，对非偏好响应（$y^-$）中的幻觉 token 施加更重惩罚。

训练目标由两项构成：
- **加权 DPO 损失** $\mathcal{L}_{\text{wDPO}}$（Equation 8）：将 token 权重集成到标准 DPO 损失中，使优化过程聚焦于视觉关键 token。
- **Token 加权 KL 正则项** $\mathcal{L}_{\text{KL}}$（Equation 9）：按 token 权重对正负样本分别计算策略模型与参考模型之间的 KL 散度，防止策略偏离过远，增强训练稳定性。

最终 Cat-PO 损失为 $\mathcal{L}_{\text{Cat-PO}} = \mathcal{L}_{\text{wDPO}} + \mathcal{L}_{\text{KL}}$（Equation 10）。消融实验表明，移除 token 级 KL 正则化会导致 MM-Hal Score 和 CHAIR/Hal 指标恶化，验证了 KL 项对稳定训练和抑制幻觉的必要性（Table 2）。

### 输入输出流

- **输入**：图像 $v$、问题 $x$、偏好响应 $y^+$、非偏好响应 $y^-$。
- **中间表示**：各 Transformer 层的跨模态注意力矩阵、token 嵌入、视觉上下文向量。
- **输出**：经 token 级加权优化后的策略模型 $\pi_\theta$，在推理时直接生成响应，无需额外推理开销。

### 效率特征

Cat-PO 的训练时间较标准 DPO 增加约 38%（平均每样本 2.9s vs. 2.1s），但峰值内存占用几乎不变（40.450 GB vs. 40.420 GB，+0.07%），整体计算代价可控（Table 5）。推理阶段无额外开销，因为 token 奖励计算仅在训练时进行。

## 核心模块与公式推导

Cat-PO 的核心机制是在标准 DPO 损失中引入**分层视觉相关性奖励**与**Token 级 KL 正则化**，从而在解码阶段对每个响应 token 施加差异化的优化信号。整体流程可概括为三步：多层级视觉相关性计算、Token 权重映射、加权损失构建。

### 标准 DPO 损失

Cat-PO 建立在直接偏好优化（DPO）框架之上。给定输入 $x$（图像与问题）、偏好响应 $y^+$ 和非偏好响应 $y^-$，标准 DPO 损失旨在最大化策略模型 $\pi_\theta$ 对偏好响应的对数概率相对于非偏好响应的差距：

$$\mathscr{L}_{\mathrm{DPO}} = -\log \sigma \left( \beta \left( \log \frac{\pi_{\theta}(y^+ \mid x)}{\pi_{ref}(y^+ \mid x)} - \log \frac{\pi_{\theta}(y^- \mid x)}{\pi_{ref}(y^- \mid x)} \right) \right) \tag{1}$$

其中 $\pi_{ref}$ 为冻结的参考模型，$\beta$ 控制偏离参考模型的幅度。该损失对所有 token 平等对待，这是 Cat-PO 改进的出发点。

### 分层视觉相关性奖励

Cat-PO 利用 MLLM 内在的跨模态注意力机制，从三个互补层次量化每个响应 token $y_t$ 与视觉内容的关联程度。

**全局相关性**（Global Relevance）：对 token $y_t$ 在所有 $N_p$ 个图像 patch 上的跨模态注意力分数求和，衡量 token 的整体视觉关联度：

$$S_{\mathrm{global}}(y_t) = \sum_{j=1}^{N_p} a_{t,j} \tag{2}$$

其中 $a_{t,j}$ 为 token $y_t$ 对第 $j$ 个图像 patch 的注意力分数。分数越高，表示该 token 与图像内容在全局层面越相关。

**局部相关性**（Local Relevance）：通过注意力分布的集中程度来刻画 token 是否聚焦于特定图像区域。首先计算注意力分布的信息熵：

$$H(P_t) = -\sum_{j=1}^{N_p} P_{t,j} \log(P_{t,j} + \epsilon) \tag{3}$$

其中 $P_{t,j}$ 为归一化后的注意力分布。局部相关性定义为 1 减去归一化熵：

$$S_{\mathrm{local}}(y_t) = 1 - \frac{H(P_t)}{\log N_p} \tag{4}$$

当注意力高度集中于少数 patch 时，熵值低、局部分数高，表明 token 与特定图像局部强相关。

**语义相关性**（Semantic Relevance）：计算 token 嵌入 $\mathbf{e}(y_t)$ 与注意力加权视觉上下文向量 $\mathbf{v}_c(y_t)$ 之间的余弦相似度，反映 token 与视觉内容的语义对齐程度：

$$S_{\mathrm{semantic}}(y_t) = \cos(\mathbf{e}(y_t), \mathbf{v}_c(y_t)) = \frac{\mathbf{e}(y_t) \cdot \mathbf{v}_c(y_t)}{\|\mathbf{e}(y_t)\| \|\mathbf{v}_c(y_t)\|} \tag{5}$$

**多级分数融合**：用平衡参数 $\alpha$ 将三个相关性得分聚合为统一的视觉相关性分数 $s_i$：

$$s_i = \alpha \big[ 0.5 \cdot S_{\mathrm{global},i} + 0.5 \cdot S_{\mathrm{local},i} \big] + (1 - \alpha) S_{\mathrm{semantic},i} \tag{6}$$

其中 $\alpha$ 控制注意力层面（全局+局部）与语义层面的相对权重。消融实验表明，固定等权融合在 DPO 设置下优于可学习融合权重（后者反而导致性能下降，见 Table 4）。

### Token 权重映射与加权损失

将统一相关性分数 $s_i$ 通过 tanh 非线性映射为 $T_i$，并结合基础权重 $\lambda_{ref}$ 生成最终 token 权重 $w_i$。对偏好响应中与视觉高度对齐的 token 给予更高权重，对非偏好响应中的幻觉 token 施加更重惩罚：

$$w_i = \begin{cases} \lambda_{\mathrm{ref}} + T_i, & y_i \in y^+ \\ \lambda_{\mathrm{ref}} + (1 - T_i), & y_i \in y^- \end{cases} \tag{7}$$

**加权 DPO 损失**：将 token 权重集成到 DPO 的对数似然比计算中，形成 $\mathcal{L}_{\mathrm{wDPO}}$：

$$\mathcal{L}_{\mathrm{wDPO}} = -\log \sigma \big[ \beta \big( \pi_{\theta}^{(w)} - \pi_{ref}^{(w)} \big) \big] \tag{8}$$

其中 $\pi_{\theta}^{(w)}$ 和 $\pi_{ref}^{(w)}$ 分别为策略模型与参考模型在 token 级加权下的对数似然比。

**Token 加权 KL 正则项**：为防止策略偏离参考模型过远，引入按 token 权重加权的 KL 惩罚：

$$\mathcal{L}_{\mathrm{KL}} = \lambda \Bigg( \sum_t w_t^+ \mathrm{KL} [ \pi_{\theta}(\cdot \mid h_t^+) \mid\mid \pi_{ref}(\cdot \mid h_t^+) ] + \sum_t w_t^- \mathrm{KL} [ \pi_{\theta}(\cdot \mid h_t^-) \mid\mid \pi_{ref}(\cdot \mid h_t^-) ] \Bigg) \tag{9}$$

其中 $h_t^+$、$h_t^-$ 分别为正负样本在位置 $t$ 的隐藏状态，$\lambda$ 为 KL 正则化系数。消融实验证实，移除该 KL 项会导致 MM-Hal Score 和 CHAIR/Hal 指标恶化（Table 2），验证了其对训练稳定性的关键作用。

**最终 Cat-PO 损失**：

$$\mathcal{L}_{\mathrm{Cat-PO}} = \mathcal{L}_{\mathrm{wDPO}} + \mathcal{L}_{\mathrm{KL}} \tag{10}$$

整个框架的核心洞察在于：利用 MLLM 内在的跨模态注意力机制，在不引入外部工具的前提下，为每个 token 计算多层级视觉相关性奖励，并将其映射为差异化权重融入 DPO 优化。这使得模型能够对与视觉内容紧密关联的 token 施加更强的偏好信号，同时对幻觉 token 施加更重的惩罚，从而实现更细粒度的幻觉抑制。

## 实验与分析

### 主要结果：幻觉抑制与通用能力

Cat-PO 在 LLaVA-v1.5-7B 和 LLaVA-v1.5-13B 两个模型规模上均取得了领先的幻觉抑制效果。**Table 1** 汇总了 AMBER、MM-Hal、LLaVA-Bench 和 SEED 四个基准上的完整对比。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_iIbe6qDN0A/figures/003_Table_1.jpg]]
*Table 1: Performance comparison on the Discrimination and Generative of AMBER Wang et al. (2023), MM-Hal Sun et al. (2023), LLaVA-Bench Liu et al. (2023b) and SEED Li et al. (2023a) benchmarks. All methods are based on LLaVA-v1.5-7B and -13B Liu et al. (2023b) models with the RLHF-V Yu et al. (2024) dataset, with the best results highlighted in bold*

在 **AMBER-Generation** 上，Cat-PO 将 CHAIR 降至 **4.8**，Hal 降至 **23.7**，显著优于 DPO（Rafailov et al., 2023）、CSR（Zhou et al., 2024b）、POVID（Zhou et al., 2024a）、RLHF-V（Yu et al., 2024）、V-DPO（Xie et al., 2024）和 TPO（Gu et al., 2024）等基线方法。在 **MM-Hal** 上，Score 升至 **2.74**，Rate 降至 **42.0**，同样为最优结果。这表明跨模态自适应 token 奖励机制在减少物体幻觉方面具有明显优势。

在通用能力方面，Cat-PO 在 LLaVA-Bench 上达到 **70.3**，SEED 上达到 **67.0**，说明幻觉抑制并未以牺牲通用对话能力为代价。在 AMBER-Discrimination 上，Cat-PO 也保持了具有竞争力的判别能力（F1: 85.3），但并非所有子项都绝对领先——该任务更侧重图像-文本匹配而非生成式幻觉检测，方法优势在此体现相对有限。

**Figure 3** 进一步展示了在 Qwen2.5-VL-3B 上的跨架构验证结果：Qwen+Cat-PO 在 AMBER F1 上达到约 **91.3**（Qwen+DPO: ~87.6），MM-Hal Score 升至约 **91.3**（Qwen+DPO: ~87.4），Hallucination Rate 降至约 **31%**（Qwen+DPO: ~39%）。这一跨架构迁移表明 Cat-PO 的 token 级奖励机制具有良好的泛化性。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_iIbe6qDN0A/figures/004_Figure_3.jpg]]
*Figure 3: Performance comparison of different Qwen2.5-VL models in terms of AMBER and MM-Hal Benchmarks*

### 消融实验：模块必要性与信号互补

**Table 2** 的消融实验揭示了各模块的独立贡献：

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_iIbe6qDN0A/figures/009_Table_2.jpg]]
*Table 2: Performance of individual Cat-PO modules*

- **仅 DPO**（无任何 token 奖励）作为下界，在 MM-Hal Score 和 AMBER-Gene 指标上表现最差。
- **仅注意力奖励**（Attention-only）和**仅语义相似度奖励**（Similarity-only）均能独立带来性能提升，但效果有限。
- **移除 Token 加权 KL 正则化**（Cat-PO without KL）导致 Score 和 Rate 均出现退化，验证了 KL 项对稳定训练和抑制幻觉的必要性。
- **完整 Cat-PO** 结合注意力与语义信号并保留 KL 项，在所有指标上取得最优。

这一消融链条清晰地表明：**多级视觉线索互补**（注意力提供空间定位，语义相似度提供内容对齐）和 **token 级 KL 正则化**是 Cat-PO 性能的两大支柱。

### 超参数与加权策略分析

**Figure 4** 展示了加权比例、关键超参数 α 和 λ_KL 的影响：

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_iIbe6qDN0A/figures/008_Figure_4.jpg]]
*Figure 4: The performance comparison of (a) different weighting proportions, (b)(c) important hyper-parameters α / $\lambda _ { K L }$ , , and (d) weighting positions in our proposed Cat-PO framework*

- **加权比例**（Figure 4a）：对奖励最高的前 30% token 加权带来的收益大于前 50%，但**使用全部 token 加权仍获得最佳幻觉抑制效果**。这验证了论文的核心假设——即使是视觉相关性较低的 token，其优化仍对整体生成质量有边际贡献。
- **平衡参数 α**（Figure 4b）：α 控制注意力信号与语义信号的融合比例，在 α ≈ 0.5 附近取得最优，说明两类信号在 DPO 设置下具有近似等价的贡献。
- **KL 正则化系数 λ_KL**（Figure 4c）：适中的 λ_KL 值平衡了偏好优化与参考模型约束，过大或过小均导致性能下降。
- **加权位置**（Figure 4d）：对正样本中视觉高相关 token 加权（Top 30%）显著优于对低相关 token 加权（Bottom 30%），进一步证实了奖励信号的有效性。

### 融合策略与鲁棒性

**Table 4** 对比了固定等权融合与可学习融合权重的效果。令人意外的是，可学习融合（Equation 11: $s_i = \gamma S_{global,i} + \delta S_{local,i} + (1-\gamma-\delta) S_{semantic,i}$）反而导致性能下降（MM-Hal Score 从 2.76 降至 2.55）。论文推测这可能源于 DPO 训练中可学习参数的不稳定性或过拟合，但未给出严格证明——**该点需要进一步研究确认**。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_iIbe6qDN0A/figures/014_Table_4.jpg]]

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_iIbe6qDN0A/figures/013_Table_3.jpg]]
*Table 3: CatPO performance on overall and adversarial subsets of POPE Li et al. (2023c). Table 4: Comparison of Cat-PO (general) and Cat-PO (with learnable fusion)*

**Table 3** 展示了在 POPE 对抗子集上的鲁棒性：Cat-PO 在 adversarial 子集上准确率下降约 2%（85.6 → 84.0），精确率下降约 4%（95.2 → 91.3）。这一轻微衰减表明方法在极端对抗情形下仍有一定局限性，但整体退化幅度可控。

### 训练效率与代价

**Table 5** 对比了 DPO 与 Cat-PO 的训练开销：

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_iIbe6qDN0A/figures/019_Table_5.jpg]]

- 平均每样本处理时间：DPO 为 **2.1s**，Cat-PO 为 **2.9s**（**+38%**）。
- 峰值显存占用：DPO 为 **40.420 GB**，Cat-PO 为 **40.450 GB**（**+0.07%**，几乎不变）。

时间开销的增加主要来自跨模态注意力提取与多级分数计算，但显存开销几乎未增长，整体计算代价在可接受范围内。然而，论文未系统比较与强化学习方法（如 PPO）的资源消耗和收敛特性，**该对比的缺失限制了效率优势的完整评估**。

### 训练动态与 Token 级行为分析

**Figure 6** 展示了 Cat-PO 的训练动态：损失平滑下降，奖励边际稳步增长，梯度范数保持稳定，表明优化过程相对稳定，未出现明显的训练崩溃或发散。

**Figure 8**（附录）对比了 Cat-PO 与 DPO 在 chosen 响应上的 token 级对数概率：Cat-PO 不仅学习了更强的偏好响应偏好，而且以更高的置信度生成这些响应。**Figure 9**（附录）的统计进一步显示，Cat-PO 模型下平均 **97.60%** 的正样本 token 经历了对数概率的正向增长，**99.98%** 的样本呈现总对数概率的净增长——这从 token 级别定量验证了方法的有效性。

### 失败模式与局限

1. **对抗鲁棒性有限**：POPE adversarial 子集上存在 2-4% 的性能衰减，极端对抗情形下 token 奖励机制可能被误导。
2. **可学习融合失效**：可学习权重融合策略反而不如固定等权融合，暗示当前 DPO 框架下奖励融合方式仍需进一步研究。
3. **训练时间增加**：38% 的时间开销在实际部署中可能成为瓶颈，尤其在大规模数据或更大模型上。
4. **评估指标局限**：主要指标集中在幻觉检测（CHAIR、Hal、MM-Hal），对生成多样性、流畅性、事实一致性等维度尚未全面评估。
5. **数据与模型泛化性**：所有实验基于 RLHF-V 数据集和 LLaVA/Qwen 架构，其他多模态偏好数据或模型架构上的泛化性有待检验。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_iIbe6qDN0A/figures/025_Figure_10.jpg]]
*Figure 10: Four comparative examples showing generation differences between DPO and our Cat-PO. (1) Beach horse riding: Cat-PO provides specific details about rider attire and horse movement. (2) Sand skateboarding: Cat-PO adds contextual information about terrain and activity. (3) Beach dogs: Cat-PO correctly identifies three dogs with distinct color patterns. (4) Children playing: Cat-PO notes precise subject count, positions, and presence of a toy*

## 方法谱系与知识库定位

### 与偏好优化方法的继承与分化

Cat-PO 建立在直接偏好优化（**DPO**, Rafailov et al., 2023）的框架之上，继承了其通过比较偏好/非偏好响应的对数概率差来对齐模型的核心理念。标准 DPO 损失（Equation 1）对所有响应 token 施加均匀的优化信号，隐含假设每个 token 对偏好学习的贡献相等。Cat-PO 的核心突破在于打破这一均匀性假设：它利用多模态大语言模型（MLLM）内在的跨模态注意力机制，为每个响应 token 计算多层级视觉相关性分数，并将其映射为差异化权重，融入加权 DPO 损失（Equation 8）中。

在偏好数据构造层面，Cat-PO 与同期工作共享了 RLHF-V 数据集（Yu et al., 2024），该数据集通过人工标注提供段级细粒度反馈。但 Cat-PO 的优化粒度超越了段级：**RLHF-V** 使用密集 DPO 在段级别进行优化，**TPO**（Gu et al., 2024）虽引入了 token 级 DPO，但其 token 重要性信号来源和加权策略与 Cat-PO 有本质差异——Cat-PO 的权重直接源自跨模态注意力分布、局部信息熵和语义相似度的三层次融合，而非外部模型或启发式规则。**V-DPO**（Xie et al., 2024）同样利用视觉信息引导 DPO，但侧重图像级别的整体对齐，未深入到 token 粒度的视觉相关性建模。

### 知识库定位：Token 级跨模态奖励的细粒度偏好优化

Cat-PO 在现有方法谱系中的定位可概括为：**基于内在跨模态注意力信号的 token 级自适应奖励偏好优化方法**。其知识贡献体现在三个层面：

1. **奖励信号来源的内生性**：与依赖外部视觉工具或检测模型的方法不同，Cat-PO 完全利用 MLLM 解码过程中自然产生的跨模态注意力分布和语义相似度。这一设计使其无需额外标注或外部知识库即可实现细粒度幻觉抑制，降低了系统复杂度。

2. **奖励粒度的层次化**：全局相关性（$S_{\mathrm{global}}$，Equation 2）捕捉 token 对图像的整体关注度；局部相关性（$S_{\mathrm{local}}$，Equation 4）通过注意力熵衡量 token 对特定图像区域的聚焦程度；语义相关性（$S_{\mathrm{semantic}}$，Equation 5）计算 token 嵌入与注意力加权视觉上下文的余弦相似度。三者的固定权重融合（Equation 6）形成了一个互补的视觉对齐度量体系。

3. **优化稳定性的显式保障**：Cat-PO 引入了 token 级加权的 KL 正则项（Equation 9），对偏好和非偏好响应分别按 token 权重施加 KL 惩罚。消融实验证实，移除该正则项会导致 MM-Hal Score 和 CHAIR/Hal 指标恶化（Table 2），表明其在防止策略偏离参考模型过远方面发挥了关键作用。

### 适用边界与局限性

**适用前提与已验证范围**：
- 方法基于 LLaVA-v1.5-7B/13B 和 Qwen2.5-VL-3B 架构验证，其有效性依赖于这些模型的多模态 Transformer 层中可提取的跨模态注意力分布。对于使用不同融合策略（如 Q-Former 等感知器重采样）的架构，注意力提取方式可能需要适配。
- 所有实验仅使用 RLHF-V 数据集进行训练，在其他多模态偏好数据（如 POVID 的幻觉注入数据、CSR 的自迭代数据）上的泛化性尚未验证。
- 评估指标集中在幻觉相关基准（AMBER、MM-Hal、POPE、LLaVA-Bench、SEED），对生成多样性、流畅性、推理能力等维度的全面评估尚缺。

**计算代价与效率**：
- Cat-PO 的训练时间较标准 DPO 增加约 38%（平均每样本 2.9s vs. 2.1s，Table 5），主要源于跨模态注意力的提取与三层分数的计算。但峰值内存占用几乎不变（+0.07%），表明额外计算主要增加时间开销而非空间开销。
- 推理阶段无需额外计算（注意力提取仅在训练时用于权重计算），因此推理效率不受影响，但论文未对此进行明确测量。

**鲁棒性边界**：
- 在 POPE 的对抗性子集上，Cat-PO 的准确率、精确率和 F1 分别有约 2%、4%、2% 的轻微下降（Table 3），表明在刻意构造的对抗场景下，基于注意力信号的奖励机制可能受到干扰。
- 可学习融合权重的尝试（Equation 11）反而导致性能下降（Table 4），暗示在 DPO 设置下，固定均匀加权比端到端学习的融合策略更鲁棒。这一反直觉现象的深层原因——是训练不稳定、过拟合，还是 DPO 隐式奖励与可学习权重的优化目标冲突——仍是开放问题。

**未覆盖的场景与局限**：
- 当三个视觉相关性信号均含噪声时（例如图像质量极差、注意力分布高度均匀、语义嵌入缺乏判别力），融合机制的鲁棒性未经验证。
- 方法未与强化学习类方法（如 PPO）进行系统比较，token 级奖励机制与 RL 框架的结合潜力尚不明确。
- 论文声称消除了对外部工具的依赖，但未定量测量由此带来的资源节省效果。

### 开放问题

1. **融合机制的优化方向**：为什么可学习融合权重在 DPO 中不如固定等权融合？是否存在更优的融合策略（如基于置信度的动态加权）来提升鲁棒性？

2. **信号质量退化场景**：当跨模态注意力、局部熵和语义相似度三者均不可靠时，Cat-PO 的奖励机制如何表现？是否可以引入不确定性估计来降权不可靠信号？

3. **架构泛化性**：能否在不显著增加计算开销的前提下，将 token 级跨模态奖励机制推广到使用感知器重采样（如 Q-Former）或专有架构（如 GPT-4V）的 MLLM？

4. **与强化学习的结合**：Token 级奖励机制天然适合与 PPO 等 RL 方法结合，这种组合是否能进一步降低幻觉？其资源消耗和收敛特性如何？

5. **评估维度的扩展**：除幻觉指标外，Cat-PO 对生成文本的多样性、流畅性、事实一致性以及复杂推理能力的影响需要系统评估。

## 原文 PDF

![[paperPDFs/ICLR_2026/Cat_PO_Cross_modal_Adaptive_Token_rewards_for_Preference_Optimization_in_Truthful_Multimodal_LLMs.pdf]]
