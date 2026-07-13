---
title: "QuietPrune: Query-Guided Early Token Pruning for Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/QuietPrune_Query_Guided_Early_Token_Pruning_for_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/QwenLM/Qwen3-"
aliases:
- QuietPrune
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "核心因果机制是通过文本到视觉适配器将查询嵌入转换为视觉域的[Q-CLS]令牌，并将其插入ViT，以指导基于文本-视觉相关性的令牌剪枝决策；适配器通过投影层的逆变换初始化，使模型能够以极少的训练实现文本指导。"
primary_logic: 在ViT内部进行早期查询引导剪枝，利用自注意力得分作为无额外成本的相关性度量，并通过半结构化分组剪枝保留空间连续性，能够在显著降低延迟的同时保持甚至提升准确性。
claims:
- QuietPrune通过早期ViT剪枝实现延迟降低且保持准确率。
- "轻量级适配器通过逆变换初始化将查询转换为[Q-CLS]令牌。"
- "半结构化2×2分组剪枝基于[Q-CLS]注意力得分，保留空间连续性。"
- 在InternVL3-1B和Qwen3-VL-4B上实现98.5%和95.7%的相对精度及42.1%和33.1%的延迟降低。
---

# QuietPrune: Query-Guided Early Token Pruning for Vision-Language Models

> [!tip] 核心洞察
> 在ViT内部进行早期查询引导剪枝，利用自注意力得分作为无额外成本的相关性度量，并通过半结构化分组剪枝保留空间连续性，能够在显著降低延迟的同时保持甚至提升准确性。

| 字段 | 内容 |
|------|------|
| 中文题名 | QuietPrune: 查询引导的视觉语言模型早期标记剪枝 |
| 英文题名 | QuietPrune: Query-Guided Early Token Pruning for Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Gao_QuietPrune_Query-Guided_Early_Token_Pruning_for_Vision-Language_Models_CVPR_2026_paper.html) · [Code](https://github.com/QwenLM/Qwen3-) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | QuietPrune |
| Dataset | InternVL3-1B（六个基准的平均）, Qwen3-VL-4B（六个基准的平均） |

> [!tip] 效果简介
> - InternVL3-1B（六个基准的平均） 上，RA% (相对准确率) 98.5 vs 100 (无剪枝) (-1.5)。
> - InternVL3-1B 上，LR% (延迟降低) 42.1 vs 0 (无剪枝) (+42.1)。
> - Qwen3-VL-4B（六个基准的平均） 上，RA% (相对准确率) 95.7 vs 100 (无剪枝) (-4.3)。

## 概要

视觉语言模型（VLM）在预填充阶段面临严重的延迟瓶颈：视觉Transformer（ViT）生成的大量视觉令牌占据了主导计算开销。实验表明，在多数配置下ViT计算占预填充延迟的50%以上，小模型搭配高分辨率输入时甚至超过75%（见Figure 2）。现有的令牌剪枝方法大多在ViT之后或LLM内部进行晚期剪枝，无法减少ViT自身的计算成本；而少数早期剪枝方法因缺乏文本指导，仅依赖视觉显著性，容易丢失对下游任务关键的语义令牌。

针对上述问题，本文提出**QuietPrune**——一种查询引导的早期令牌剪枝方法。其核心思路是：通过一个轻量级的文本到视觉适配器，将文本查询嵌入转换为视觉域的[Q-CLS]令牌并插入ViT，利用自注意力得分作为无额外开销的文本-视觉相关性度量，在ViT内部进行查询感知的剪枝决策。同时，采用半结构化2×2分组剪枝策略保留空间连续性，并将被剪枝的冗余令牌加权聚合为一个紧凑令牌以保留上下文信息。适配器通过预训练视觉到文本投影层的逆变换进行初始化，使模型仅需极少量训练即可获得有效的文本指导能力。

在InternVL3和Qwen3-VL系列模型上的实验表明，QuietPrune在保持高相对准确率的同时实现了显著的延迟降低：在InternVL3-1B上达到98.5%的相对准确率和42.1%的延迟降低，在Qwen3-VL-4B上达到95.7%的相对准确率和33.1%的延迟降低。与现有SOTA方法相比，QuietPrune在准确率与预填充延迟的权衡上均表现更优（见Figure 1）。



### 视觉-语言模型中的视觉令牌冗余问题

视觉-语言模型（Vision-Language Models, VLMs）通常采用视觉编码器（如ViT）将输入图像转换为大量视觉令牌，再通过投影层将这些视觉令牌输入大语言模型（LLM）进行多模态推理。然而，视觉编码器生成的视觉令牌数量庞大，成为预填充阶段（prefill phase）的主要计算瓶颈。如图2所示，在Qwen3-VL和InternVL3系列模型上，ViT计算占预填充延迟的50%以上，对于小模型搭配高分辨率输入时更超过75%。这一瓶颈严重制约了VLM的推理效率，尤其是在对延迟敏感的实际应用中。

### 现有标记剪枝方法的缺口

为缓解视觉令牌冗余问题，研究者提出了多种标记剪枝方法，大致可分为晚期剪枝和早期剪枝两类：

**晚期剪枝方法**（如**FastV**（Chen et al., ECCV 2024）、**DivPrune**（Alvar et al., CVPR 2025）、**PACT**（Dhouib et al., CVPR 2025））在ViT之后或LLM内部对视觉令牌进行剪枝。这类方法无法减少ViT本身的计算开销，而ViT正是延迟的主要来源。更严重的是，部分晚期剪枝方法（如DivPrune、AIM）的剪枝决策计算开销过大，导致总体预填充延迟反而超过无剪枝模型，出现负的延迟降低率（LR%）。

**早期剪枝方法**（如**SAINT**（Jeddi et al., arXiv 2025））尝试在ViT内部进行剪枝，从而直接减少ViT的计算量。然而，现有早期剪枝方法仅依赖视觉显著性信号（如对[CLS]令牌的注意力得分），缺乏文本查询的指导。这导致一个关键缺陷：在剪枝过程中可能丢弃与用户问题语义相关的视觉令牌，而对问题无关的视觉显著区域却予以保留（如图3所示），最终损害下游任务的准确性。

### 核心动机：查询引导的早期剪枝

上述分析揭示了一个根本性的矛盾：早期剪枝能有效降低延迟，但缺乏文本指导会导致语义关键令牌丢失；晚期剪枝能利用文本信息，却无法减少ViT的计算瓶颈。本文的核心动机正是打破这一困境——**在ViT内部实现查询引导的早期令牌剪枝**，使剪枝决策同时兼顾计算效率与语义保真度。

具体而言，QuietPrune致力于解决三个关键挑战：
1. **如何将文本查询信息注入ViT**：需要设计轻量级机制将文本语义转化为ViT可理解的视觉域信号，且不能引入过多额外开销。
2. **如何度量文本-视觉相关性**：需要一种计算成本极低的相关性度量方式，使其在ViT的多个中间层均可高效执行。
3. **如何保持剪枝后的空间结构**：单个令牌的随机剪枝会破坏视觉令牌的空间位置连续性，需要设计保留空间结构的剪枝粒度。

通过解决上述挑战，QuietPrune旨在实现一个统一的早期剪枝框架，在显著降低预填充延迟的同时，保持甚至提升多模态理解的准确性。



## 核心方法与创新机理

QuietPrune 的核心创新在于将视觉令牌剪枝的决策点从 LLM 内部或 ViT 之后**前移至 ViT 编码阶段**，并通过**查询引导的文本-视觉相关性**替代传统的纯视觉显著性信号，从而在显著降低预填充延迟的同时保持甚至提升模型准确率。其关键创新可归纳为以下四个维度。

### 剪枝位置前移：从晚期剪枝到 ViT 内早期剪枝

现有令牌剪枝方法（如 **FastV** (Chen et al., ECCV 2024)、**DivPrune** (Alvar et al., CVPR 2025)、**PACT** (Dhouib et al., CVPR 2025)）通常在 ViT 完成编码之后、LLM 内部进行剪枝，无法减少 ViT 自身的计算开销。然而，ViT 计算在预填充延迟中占据主导地位——在多数设置下超过 50%，对于小模型配合高分辨率输入时甚至超过 75%（见图 2）。QuietPrune 将剪枝操作嵌入 ViT 内部，在总层数的 1/4、1/2 和 3/4 处三个固定深度进行逐步剪枝，使被剪除的令牌无需参与后续 ViT 层的自注意力计算，从而从根本上削减 ViT 的浮点运算量。

这一位置前移并非没有代价：早期剪枝缺乏文本指导，容易错误丢弃对下游问答至关重要的视觉令牌。QuietPrune 通过以下创新解决了这一矛盾。

### 剪枝指导信号革新：查询引导的文本-视觉相关性

传统早期剪枝方法（如 **SAINT** (Jeddi et al., arXiv 2025)）仅依赖视觉显著性——即视觉令牌对 [CLS] 令牌的注意力得分——作为剪枝依据。这种纯视觉信号无法区分“视觉上显著但语义无关”与“视觉上不显著但语义关键”的区域。QuietPrune 引入**查询引导**机制：通过一个轻量级文本到视觉适配器，将文本查询嵌入映射到视觉域，生成一个 [Q-CLS]（Query [CLS]）令牌，并将其插入 ViT 输入序列的首部。在自注意力计算中，[Q-CLS] 令牌与所有视觉令牌产生的注意力得分天然地度量了**文本-视觉相关性**，无需额外计算开销。消融实验表明，查询引导剪枝相比仅视觉显著性剪枝，在 InternVL3-1B 和 Qwen3-VL-4B 上分别带来 **+4.11%** 和 **+5.94%** 的相对精度提升（见表 2）。

### 剪枝粒度细化：半结构化 2×2 分组剪枝

无结构化的单令牌剪枝会破坏视觉令牌的空间连续性，导致保留的令牌丧失位置信息（见图 5）。QuietPrune 提出**半结构化分组剪枝**：将空间相邻的 2×2 令牌编为一组，以组内令牌对 [Q-CLS] 的平均注意力得分作为该组的相关性度量，整组保留或整组剪除。这一设计在保留空间结构的同时，与主流 VLM（如 InternVL3、Qwen3-VL）中广泛采用的像素洗牌（pixel shuffle）空间合并操作天然兼容，无需额外适配。

### 适配器初始化策略：投影层逆变换

文本到视觉适配器的初始化方式对训练效率和最终性能影响显著。QuietPrune 利用 VLM 中已有的视觉到文本投影层进行**逆变换初始化**：对于线性层，当权重矩阵可逆时直接取逆 $W^* = W^{-1}$，不可逆时使用 Moore-Penrose 伪逆 $W^* = \lim_{\alpha \to 0^+} (W^T W + \alpha I)^{-1} W^T$；对于 LayerNorm，参数初始化为 $\gamma^* = 1/\gamma$，$\beta^* = -\beta/\gamma$。这一策略使适配器在训练初始阶段即具备将文本特征映射回视觉域的能力，相比随机初始化，在 InternVL3-1B 和 Qwen3-VL-4B 上分别带来 **+3.25%** 和 **+2.94%** 的相对精度增益（见表 2），且仅需少量公开数据即可完成训练。

### 冗余令牌聚合：剪枝不丢弃

传统剪枝直接丢弃冗余令牌，可能损失全局上下文信息。QuietPrune 将剪除的令牌按相关性得分加权求和，聚合成一个紧凑令牌，保留在序列中以维持上下文线索。消融实验显示，该操作为 InternVL3-1B 和 Qwen3-VL-4B 分别带来额外 **+0.50%** 和 **+0.84%** 的精度提升（见表 2）。

综合上述创新，QuietPrune 在 InternVL3-1B 上实现 **98.5%** 相对精度和 **42.1%** 延迟降低，在 Qwen3-VL-4B 上实现 **95.7%** 相对精度和 **33.1%** 延迟降低（见表 1），在精度-延迟权衡上显著优于现有方法。



QuietPrune 的整体设计围绕一个核心洞察展开：**在 ViT 内部进行早期查询引导剪枝**，能够在显著降低预填充延迟的同时保持甚至提升模型准确率。其 pipeline 由三个关键模块串联构成，形成一条从文本查询到视觉令牌筛选的因果链路。

### 框架概览

如 Figure 4 所示，QuietPrune 的推理流程如下：

![[assets/figures/papers/paper_list_l778_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_QuietPrune_Query_G/figures/007_Figure_4.jpg]]
*Figure 4: Overall framework of QuietPrune. We perform a query-guided early pruning strategy. An adapter is proposed to convert text embeddings into the visual domain. The adapter leverages the capability of the projector through an inverse transformation and generates a [Q-CLS] token to guide the pruning process of ViT. We propose a semi-structured pruning based on visual-textual relevance. The visual tokens are pruned in a group-wise manner to preserve the positional information. After pruning, we aggregate the redundant tokens into a single token to maintain context cues*

1. **文本到视觉适配器（Text-to-Vision Adapter）**：接收 LLM 的文本查询嵌入，通过逆变换初始化（详见第 4.1 节），将其映射到 ViT 的视觉特征空间，生成一个 [Q-CLS] 令牌。
2. **[Q-CLS] 令牌插入**：将 [Q-CLS] 令牌拼接到视觉令牌序列的首部，作为 ViT 后续层的输入。
3. **半结构化分组剪枝（Semi-structured Pruning）**：在 ViT 的三个固定深度位置（总层数的 1/4、1/2、3/4），利用 [Q-CLS] 与视觉令牌之间的自注意力得分作为文本-视觉相关性度量，对空间相邻的 2×2 令牌组进行剪枝。
4. **冗余令牌聚合（Redundant Token Aggregation）**：将剪枝掉的令牌按相关性得分加权求和，聚合成一个紧凑令牌，以保留被丢弃的上下文信息。
5. **LLM 解码**：经过剪枝后的精简视觉令牌序列与文本令牌拼接，送入 LLM 完成自回归生成。

### 模块间的因果链路

各模块之间存在紧密的因果依赖关系：

- **适配器 → [Q-CLS] 令牌**：适配器是整个剪枝机制的“文本感知”来源。它通过对 VLM 预训练投影层（vision-to-text projector）的逆变换进行初始化，使得模型能够以极少的训练开销（仅适配器参数，其余冻结）将文本查询转换为视觉域的指导信号。若适配器采用随机初始化，相对准确率会下降 2.94%–3.25%（Table 2）。
- **[Q-CLS] 令牌 → 剪枝决策**：剪枝决策完全依赖 [Q-CLS] 令牌与视觉令牌在自注意力层中的注意力得分。与仅基于视觉显著性（如对原始 [CLS] 令牌的注意力）的方法相比，查询引导剪枝在 InternVL3-1B 和 Qwen3-VL-4B 上分别带来 4.11% 和 5.94% 的相对准确率提升（Table 2）。
- **半结构化分组 → 空间连续性保持**：无结构剪枝会破坏令牌的空间位置信息，而 2×2 分组剪枝保留了空间连续性（Figure 5），使后续的空间合并操作（如 pixel shuffle）能正常工作。
- **令牌聚合 → 上下文保留**：将剪枝令牌聚合为一个令牌，在 InternVL3-1B 和 Qwen3-VL-4B 上分别额外带来 0.50% 和 0.84% 的准确率提升（Table 2）。

### 训练范式

QuietPrune 采用知识蒸馏范式进行训练。总损失函数为：

$$\mathcal{L}_{total} = \mathcal{L}_{distill}(Y_s, Y_t) + \mathcal{L}_{ce}(Y_s, Y_{gt})$$

其中 $\mathcal{L}_{distill}$ 是教师模型（未剪枝的原始 VLM）与学生模型（剪枝后的 VLM）输出 logits 之间的 KL 散度，$\mathcal{L}_{ce}$ 是标准交叉熵损失。训练时仅更新适配器参数，ViT 和 LLM 保持冻结，因此训练开销极小。

### 与基线方法的根本差异

| 维度 | 晚期剪枝方法（FastV 等） | QuietPrune |
|------|--------------------------|------------|
| 剪枝位置 | ViT 之后或 LLM 内部 | ViT 内部（1/4、1/2、3/4 深度） |
| 指导信号 | 仅视觉显著性 | 文本查询引导的文本-视觉相关性 |
| 剪枝粒度 | 无结构化单令牌 | 半结构化 2×2 分组 |
| 对 ViT 延迟的影响 | 无（ViT 已完成计算） | 显著降低 ViT 计算量 |

这种“早期+查询引导+半结构化”的组合设计，使得 QuietPrune 能够从根本上削减 ViT 的计算瓶颈——在多数设置中 ViT 占预填充延迟的 50% 以上，小模型高分辨率下甚至超过 75%（Figure 2）。



QuietPrune 由三个核心模块构成：文本到视觉适配器、半结构化分组剪枝机制和冗余令牌聚合模块。整体框架如 Figure 4 所示，其设计目标是在 ViT 内部实现查询引导的早期令牌剪枝，从而在预填充阶段显著降低计算开销。

### 文本到视觉适配器

现有 VLM 通常使用一个视觉到文本的投影层将 ViT 输出的视觉特征映射为 LLM 可接受的令牌嵌入：

$$H_v = proj(F_v)$$

其中 $F_v$ 为 ViT 提取的视觉特征，$proj(\cdot)$ 为投影层。QuietPrune 的核心创新在于反转这一架构：设计一个轻量级的文本到视觉适配器，将文本查询嵌入转换为视觉域特征，进而生成一个 [Q-CLS]（Query [CLS]）令牌，用于指导 ViT 内部的剪枝决策。

适配器的关键设计在于其初始化策略——通过对预训练投影层的逆变换进行初始化，而非随机初始化。具体而言：

- **线性层逆初始化（可逆情况）**：若投影层权重矩阵 $W$ 可逆，适配器线性层权重 $W^*$ 和偏置 $b^*$ 初始化为：

$$W^* = W^{-1}, \quad b^* = -W^{-1} \cdot b$$

- **Moore-Penrose 伪逆初始化（不可逆情况）**：当 $W$ 不可逆时，使用伪逆最小化重构误差：

$$W^* = \lim_{\alpha \to 0^+} (W^T W + \alpha I)^{-1} W^T$$

- **SVD 伪逆**：通过奇异值分解得到伪逆矩阵：

$$W^* = V \Sigma^* U^T$$

- **LayerNorm 逆初始化**：适配器的 LayerNorm 参数 $\gamma^*$ 和 $\beta^*$ 由投影层对应参数 $(\gamma, \beta)$ 的逆变换初始化：

$$\gamma^* = \frac{1}{\gamma}, \quad \beta^* = -\frac{\beta}{\gamma}$$

这一初始化策略使得适配器能够在极少训练数据下快速收敛，充分利用预训练投影层已有的跨模态映射能力。

### 半结构化分组剪枝

[Q-CLS] 令牌被拼接到视觉令牌序列首部，共同输入 ViT。在自注意力层中，标准 QKV 投影为：

$$Q = X W_Q, \quad K = X W_K, \quad V = X W_V$$

注意力分数通过缩放点积计算：

$$A = softmax\left(\frac{Q K^T}{\sqrt{d}}\right)$$

QuietPrune 利用 [Q-CLS] 令牌与各视觉令牌之间的注意力得分作为文本-视觉相关性的度量，无需额外计算开销。为避免无结构剪枝破坏空间位置信息（如 Figure 5 所示），QuietPrune 采用半结构化剪枝：将空间相邻的 $2 \times 2$ 令牌划分为一组，以组内所有令牌对 [Q-CLS] 的平均注意力得分作为该组的相关性分数，按预设剪枝率保留得分最高的组。这一设计既保持了空间连续性，又与主流 VLM 中使用的像素洗牌等空间合并操作天然兼容。

![[assets/figures/papers/paper_list_l778_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_QuietPrune_Query_G/figures/008_Figure_5.jpg]]
*Figure 5: Comparison of unstructured pruning and semi-structured pruning. Unstructured pruning can distort patch positional information, whereas our semi-structured pruning method can preserve spatial continuity*

### 冗余令牌聚合

被剪枝的令牌并非直接丢弃，而是按相关性得分加权聚合为一个紧凑令牌 $x_m$，以保留被剪枝区域的上下文信息。这一设计在消融实验中带来约 0.5%–0.8% 的额外准确率提升。

### 训练目标

QuietPrune 的总损失函数结合了知识蒸馏损失与标准交叉熵损失：

$$\mathcal{L}_{total} = \mathcal{L}_{distill}(Y_s, Y_t) + \mathcal{L}_{ce}(Y_s, Y_{gt})$$

其中 $\mathcal{L}_{distill}$ 为学生模型输出 $Y_s$ 与教师模型（未剪枝模型）输出 $Y_t$ 之间的 KL 散度，$\mathcal{L}_{ce}$ 为学生输出与真实标签 $Y_{gt}$ 的交叉熵。训练时仅更新适配器参数，ViT 和 LLM 保持冻结，因此训练开销极小。



## 实验与关键发现

### 核心实验设置

QuietPrune 在 InternVL3 和 Qwen3-VL 两个主流 VLM 系列上进行验证，涵盖 1B 到 8B 不同参数规模。所有对比方法在 LLM 阶段保持 50% 的平均视觉令牌剪枝率（$R^* = 1 - \frac{\sum_{i=1}^L \hat{T}_i}{\sum_{i=1}^L T_i}$），以确保公平比较。主要评估指标为相对准确率（RA%，即剪枝后准确率与无剪枝准确率之比）和预填充延迟降低率（LR%）。训练时，适配器仅通过少量公开数据优化，VLM 其余参数冻结；总损失函数为教师-学生蒸馏损失（KL 散度）与标准交叉熵损失之和：

$$\mathcal{L}_{total} = \mathcal{L}_{distill}(Y_s, Y_t) + \mathcal{L}_{ce}(Y_s, Y_{gt})$$

### 主实验结果

**Table 1** 展示了各方法在六个基准上的平均表现。QuietPrune 在两个模型系列上均显著优于现有方法：

- **InternVL3-1B**：QuietPrune 达到 **98.5%** 相对准确率，同时实现 **42.1%** 的预填充延迟降低。相比之下，晚期剪枝方法 FastV 和 DivPrune 虽有一定准确率保持能力，但延迟降低有限甚至出现负值（剪枝决策开销超过收益）。
- **Qwen3-VL-4B**：QuietPrune 达到 **95.7%** 相对准确率，延迟降低 **33.1%**。SAINT-Early（早期仅视觉显著性剪枝）在同等剪枝率下准确率大幅下降，验证了查询引导的必要性。

值得注意的公平性问题：部分晚期剪枝方法（如 DivPrune、AIM）的剪枝决策计算开销过大，导致总体预填充延迟反而超过无剪枝模型，出现负 LR% 值。这从反面印证了早期剪枝在 ViT 计算占主导的场景下（ViT 延迟占比超 50%，小模型高分辨率下超 75%）的架构级优势。

### 消融实验

**Table 2** 系统拆解了 QuietPrune 各组件的贡献：

| 消融维度 | 变体 | InternVL3-1B RA% | Qwen3-VL-4B RA% | 增益 |
|---------|------|-----------------|-----------------|------|
| 剪枝结构 | 无结构剪枝 → 半结构化（SS） | → 98.45% | → 95.71% | 空间连续性保留 |
| 指导信号 | 视觉显著性 → 查询引导（QG） | +4.11% | +5.94% | 文本-视觉相关性 |
| 适配器初始化 | 随机初始化 → 逆变换初始化（IT） | +3.25% | +2.94% | 极低训练成本迁移 |
| 令牌聚合 | 无聚合 → 冗余令牌聚合（TA） | +0.50% | +0.84% | 上下文信息保留 |

**关键发现**：

1. **查询引导（QG）是最大单一增益来源**：相比仅依赖视觉显著性（如对 [CLS] 令牌的注意力），引入文本查询作为剪枝指导信号在 InternVL3-1B 和 Qwen3-VL-4B 上分别提升 4.11% 和 5.94% 相对准确率。这直接验证了核心因果机制——文本指导使剪枝决策能保留与问题语义相关的视觉令牌，而非仅保留视觉上显著的区域。

2. **逆变换初始化（IT）以极小成本实现有效迁移**：通过对预训练投影层的伪逆变换初始化适配器参数（线性层使用 Moore-Penrose 伪逆 $W^* = \lim_{\alpha \to 0^+} (W^T W + \alpha I)^{-1} W^T$，LayerNorm 使用逆参数 $\gamma^* = 1/\gamma, \beta^* = -\beta/\gamma$），相比随机初始化提升 2.94%–3.25%。这表明投影层已蕴含视觉-文本跨模态映射能力，逆变换可将其反转为文本-视觉映射，大幅降低适配器训练难度。

3. **半结构化剪枝（SS）保障空间完整性**：2×2 分组剪枝避免无结构剪枝导致的令牌位置信息扭曲（见 **Figure 5**），对依赖空间结构的视觉理解任务尤为重要。

4. **令牌聚合（TA）提供边际但稳定的增益**：将剪枝令牌按相关性得分加权聚合为单个紧凑令牌，以极低成本保留上下文线索。

### 不同剪枝率下的性能曲线

**Figure 6** 展示了各方法在 InternVL3 和 Qwen3-VL 系列上随剪枝率变化的相对准确率和延迟降低曲线。QuietPrune 在宽剪枝率范围内保持显著优势：

- 在 **80% 极端剪枝率**下，QuietPrune 仍维持超过 88% 的相对准确率，而 SAINT-Early 在 **20% 剪枝率**时准确率已跌破 90%。
- 延迟降低随剪枝率单调递增，但 QuietPrune 的准确率-延迟权衡曲线始终位于其他方法之上，表明查询引导机制在不同压缩强度下均能有效筛选关键令牌。

### 可视化分析

**Figure 3** 对比了不同方法的剪枝结果。查询引导方案能针对具体问题保留相关区域（如问题涉及“猫”时保留猫所在区域），而仅视觉显著性的方法可能保留高对比度但无关的背景区域，导致错误预测。**Figure 7** 进一步展示了 QuietPrune 在 InternVL3-1B 上针对不同查询自适应保留视觉令牌的能力，验证了方法的查询感知特性。

### 失败模式与局限性

1. **适配器训练依赖**：尽管逆变换初始化大幅降低了训练成本，适配器仍需通过小规模数据集微调，无法做到完全即插即用。
2. **剪枝层固定**：当前剪枝层固定为 ViT 总层数的 1/4、1/2、3/4，未考虑动态或自适应的剪枝调度，可能在某些输入上过度或不足剪枝。
3. **架构依赖**：半结构化 2×2 分组剪枝依赖主流 VLM 的空间合并操作（如像素洗牌），若模型不采用此类操作则需调整分组策略。
4. **泛化性待验证**：实验仅覆盖 InternVL3 和 Qwen3-VL 系列，其他 VLM 架构（如使用一维序列变换的模型）的适用性尚待检验。
5. **长查询与多轮对话**：对极端长查询或复杂多轮对话场景的性能未充分评估，查询嵌入的表达能力可能成为瓶颈。

### 开放问题

- 能否根据输入复杂度动态调整剪枝率，实现精度-延迟的自适应权衡？
- 剪枝层数和位置是否可通过元学习或强化学习自动搜索？
- 在批量推理场景下，与 KV cache 管理等系统级优化结合能否进一步释放潜力？
- 在多图、长视频等更复杂的多模态场景中，早期查询引导剪枝策略是否仍然有效？

### 补充图表

![[assets/figures/papers/paper_list_l778_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_QuietPrune_Query_G/figures/002_Figure_2.jpg]]
*Figure 2: Latency distribution between ViT and LLM during the prefill phase for the Qwen3-VL and InternVL3 model series across different model sizes with various input resolutions or number of tiles. We report the latency on a single A100 GPU. The ViT accounts for more than 50% of the latency in most settings*

![[assets/figures/papers/paper_list_l778_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_QuietPrune_Query_G/figures/001_Figure_1.jpg]]
*Figure 1: Comparison with SOTA token pruning methods on the InternVL3 series [47]. The proposed QuietPrune method outperforms the existing methods on both accuracy and prefill latency*

![[assets/figures/papers/paper_list_l778_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_QuietPrune_Query_G/figures/006_Figure_3.jpg]]
*Figure 3: Comparison of pruning results with different methods. With the query-guided scheme, our method retains tokens relevant to the input query and makes an accurate prediction*

![[assets/figures/papers/paper_list_l778_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_QuietPrune_Query_G/figures/009_Figure_6.jpg]]
*Figure 6: Comparison of different methods on the InternVL3 and Qwen3-VL series. Left is the relative accuracy, and right is the latency reduction of different methods under various pruning rates*

![[assets/figures/papers/paper_list_l778_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_QuietPrune_Query_G/figures/010_Table_1.jpg]]
*Table 1: Main results on the InternVL3 and Qwen3-VL series. All methods achieve an average pruning rate of 50% in the LLM part. “SAINT-Early” and “SAINT-Late” represent the SAINT method with early pruning and late pruning, respectively. “acc” refers to the accuracy score of the benchmark. “lat” refers to the prefill latency (ms) of each method. “RA%” refers to the relative accuracy compared to the model without pruning. “LR%” refers to the latency reduction compared to the model without pruning. Negative values in “LR%” indicate that the latency of the pruned model is larger than that of the model without pruning. We use red to highlight the best results of all methods and blue to highlight the best...*

![[assets/figures/papers/paper_list_l778_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_QuietPrune_Query_G/figures/012_Table_2.jpg]]
*Table 2: Results of ablation study. “SS” refers to Semi-Structured versus unstructured pruning; “QG”, namely Query-Guided, indicates pruning based on textual-visual relevance versus visual saliency alone; “IT” denotes adapter is initialized via Inverse Transformation versus random initialization; “TA” indicates whether redundant Token Aggregation is applied. “RA%” represents the Relative Accuracy. The Average Score (AS) is evaluated with a 50% pruning rate across six benchmarks*

![[assets/figures/papers/paper_list_l778_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_QuietPrune_Query_G/figures/011_Figure_7.jpg]]
*Figure 7: QuietPrune results on InternVL3-1B model. Our method adaptively retains the visual tokens that are relevant to each query*



## 定位与知识库关联

### 1. 问题定位：从晚期剪枝到早期剪枝的范式转移

视觉语言模型（VLM）的预填充延迟瓶颈长期被定位在LLM解码阶段，因此主流标记剪枝方法普遍采用**晚期剪枝**策略——在ViT完成全部视觉编码后、进入LLM之前或LLM内部进行标记削减。然而，Figure 2的系统性延迟分析揭示了一个被忽视的事实：**ViT计算占预填充延迟的50%以上，在小模型高分辨率场景下甚至超过75%**。晚期剪枝无法触及这一瓶颈，其延迟收益存在理论上限。

QuietPrune的根本贡献在于将剪枝操作**前移至ViT内部**（总层数的1/4、1/2、3/4处），使剪枝收益直接作用于最大计算瓶颈。这一范式转移面临的核心挑战是：早期剪枝缺乏文本查询的语义指导，仅依赖视觉显著性（如对[CLS]令牌的注意力）会丢失与查询语义相关的关键令牌。

### 2. 与基线方法的关系图谱

#### 2.1 晚期剪枝方法

**FastV**（Chen et al., ECCV 2024）是晚期剪枝的典型代表，在LLM内部基于注意力分数动态丢弃视觉令牌。其局限性在于：剪枝发生在ViT计算完成之后，无法减少ViT的预填充成本。Table 1显示，FastV的延迟降低（LR%）显著低于QuietPrune，且在高剪枝率下准确率衰减严重。

**DivPrune**（Alvar et al., CVPR 2025）和**PACT**（Dhouib et al., CVPR 2025）分别采用基于多样性和基于聚类的标记削减策略。这些方法的剪枝决策计算开销过大，Table 1中出现**负LR%值**——剪枝后的总预填充延迟反而超过无剪枝模型，暴露了晚期剪枝在系统效率层面的根本缺陷。

**AIM**（Zhong et al., arXiv 2024）采用自适应多模态推理，结合标记合并与剪枝。尽管在准确率保持上表现较好，但其自适应决策机制的计算开销同样导致延迟收益为负。

#### 2.2 早期剪枝方法

**SAINT**（Jeddi et al., arXiv 2025）是目前唯一与QuietPrune同属早期ViT剪枝范式的方法。SAINT基于视觉令牌与[CLS]令牌的相似度进行剪枝，本质上是**仅视觉显著性驱动**的策略。Figure 6显示，SAINT-Early在20%剪枝率下相对准确率已跌破90%，而QuietPrune在80%剪枝率下仍保持88%以上——这一鲜明对比揭示了纯视觉显著性指导在早期剪枝中的根本不足。

QuietPrune与SAINT的核心差异在于**剪枝指导信号**：QuietPrune通过文本到视觉适配器将查询语义注入ViT，使剪枝决策从“哪些视觉区域显著”转变为“哪些视觉区域与当前查询相关”。消融实验（Table 2）量化了这一差异：查询引导（QG）相比仅视觉显著性，在InternVL3-1B和Qwen3-VL-4B上相对准确率分别提升**4.11%和5.94%**。

### 3. 核心创新点的因果机制

#### 3.1 文本到视觉适配器与逆变换初始化

QuietPrune的关键设计是通过适配器将文本查询嵌入映射到视觉域，生成[Q-CLS]（Query [CLS]）令牌。该适配器的架构与VLM中已有的视觉到文本投影层对称，其参数通过**逆变换初始化**：

- 对于线性层权重$W$，若可逆则初始化为$W^* = W^{-1}$；若不可逆则使用Moore-Penrose伪逆$W^* = \lim_{\alpha \to 0^+} (W^T W + \alpha I)^{-1} W^T$或SVD伪逆$W^* = V \Sigma^* U^T$。
- 对于LayerNorm参数，初始化为$\gamma^* = 1/\gamma$，$\beta^* = -\beta/\gamma$。

这一初始化策略的因果意义在于：适配器在训练开始时近似投影层的逆映射，使[Q-CLS]令牌天然携带与视觉域对齐的查询语义，从而**以极少的训练数据实现文本指导能力**。消融实验（Table 2）表明，逆变换初始化（IT）相比随机初始化，相对准确率分别提升**3.25%和2.94%**。

#### 3.2 半结构化分组剪枝

QuietPrune采用**2×2空间相邻分组**的剪枝粒度，基于[Q-CLS]与各组内视觉令牌的平均注意力得分进行组级剪枝。这一设计的因果逻辑是：主流VLM（如InternVL3、Qwen3-VL）在ViT后采用像素洗牌（pixel shuffle）将2×2令牌合并为单个令牌，因此以2×2组为单位剪枝能保持空间连续性，避免无结构剪枝对位置信息的破坏（Figure 5）。消融实验（Table 2）显示，半结构化剪枝（SS）相比无结构剪枝，相对准确率分别达到**98.45%和95.71%**。

#### 3.3 冗余令牌聚合

剪枝后的令牌并非直接丢弃，而是按相关性得分加权聚合为一个紧凑令牌，以保留被剪枝区域的上下文信息。这一设计在InternVL3-1B和Qwen3-VL-4B上分别带来**0.50%和0.84%**的额外准确率提升（Table 2）。

### 4. 适用边界与局限

#### 4.1 架构依赖性

半结构化2×2分组剪枝依赖于VLM的像素洗牌操作。对于不采用此类空间合并的架构（如采用一维序列变换的模型），剪枝粒度需要重新设计。这一局限在论文中未被充分讨论，其泛化到其他VLM架构（如LLaVA系列）的效果需要独立验证。

#### 4.2 训练需求

尽管适配器参数量极小且仅需少量公开数据训练，但QuietPrune并非完全即插即用。这一训练需求限制了其在零样本部署场景中的直接适用性。

#### 4.3 剪枝调度刚性

剪枝层固定为ViT总层数的1/4、1/2、3/4，未根据输入复杂度进行动态调整。对于简单查询，固定剪枝率可能导致不必要的令牌保留；对于复杂多轮对话或长查询，固定剪枝率可能不足。论文未提供动态剪枝调度的实验证据。

#### 4.4 验证范围

实验仅覆盖InternVL3（1B/2B/4B/8B）和Qwen3-VL（4B/8B）系列。在更广泛的多图、长视频、高分辨率医学影像等场景中的性能尚未评估。此外，极端长查询或复杂推理链下的剪枝质量缺乏定量分析。

### 5. 开放问题

1. **动态剪枝调度**：能否根据输入复杂度（查询长度、图像分辨率、任务难度）自适应调整剪枝率，实现精度-延迟的更优帕累托前沿？
2. **架构泛化**：如何将查询引导早期剪枝推广到不使用2×2空间合并的VLM架构？是否需要设计通用的空间连续性保持机制？
3. **剪枝层搜索**：剪枝层数和位置是否可以通过元学习或强化学习自动搜索，以替代当前的手工固定设置？
4. **系统级协同**：QuietPrune的早期剪枝减少了进入LLM的令牌数量，这为KV cache压缩提供了额外机会。与系统级优化（如KV cache量化、前缀缓存）结合能否进一步释放延迟收益？
5. **多模态扩展**：在视频理解、3D场景理解等更复杂的多模态场景中，查询引导的早期剪枝策略是否仍然有效？是否需要引入时序或深度维度的剪枝机制？



## 原文 PDF

![[paperPDFs/CVPR_2026/QuietPrune_Query_Guided_Early_Token_Pruning_for_Vision_Language_Models.pdf]]
