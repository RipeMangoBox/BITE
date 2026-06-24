---
title: "TransPrune: Token Transition Pruning for Efficient Large Vision-Language Model"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TransPrune_Token_Transition_Pruning_for_Efficient_Large_Vision_Language_Model.pdf
project_link: null
code_link: null
aliases:
- TransPrune
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用视觉token在LLM各层传播中发生的表示转换（幅度变化和方向变化）作为token重要性的新信号；尤其是通过累积中间层的Token Transition Variation（TTV），并辅以Instruction-Guided Attention（IGA），使剪枝决策更精准地反映token的语义重要性。
primary_logic: LLM中间层（约第7–14层）中token表示的动态变化——幅度变化率和方向相似度变化——集中且显著地揭示了token的语义信息，其指示重要性强于浅层或深层；通过累积中间层的转换信号，可获得更稳健、更一致的重要性度量。
claims:
- 图2可视化表明，token表示的幅度与方向变化在中间层最显著，且与语义重要性高度相关。
- 消融实验（Table 10）显示，使用层7-12的TTV在MME^P上达到1540，而浅层（层1-6）仅为1515，证明中间层转换信号更有效。
- 累积机制（Table 11）使MME^P从1530提升至1540，幅值与方向分量（Table 12）共同贡献性能，最终组合IGA+TTV达到最佳，证明了所提信号和累积策略的有效性。
- "LLaVA-1.5-7B (综合相对准确率) 上 Acc. (%) = TransPrune-High: 100.0 (-0.0)"
---

# TransPrune: Token Transition Pruning for Efficient Large Vision-Language Model

> [!tip] 核心洞察
> LLM中间层（约第7–14层）中token表示的动态变化——幅度变化率和方向相似度变化——集中且显著地揭示了token的语义信息，其指示重要性强于浅层或深层；通过累积中间层的转换信号，可获得更稳健、更一致的重要性度量。

| 字段 | 内容 |
|------|------|
| 中文题名 | TransPrune：面向高效大视觉语言模型的Token转换剪枝 |
| 英文题名 | TransPrune: Token Transition Pruning for Efficient Large Vision-Language Model |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2507.20630) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | TransPrune |
| Dataset | LLaVA-1.5-7B, LLaVA-1.5-7B MME^P, LLaVA-NeXT-7B, Qwen2.5-VL-7B MME^P |

> [!tip] 效果简介
> - LLaVA-1.5-7B (综合相对准确率) 上，Acc. (%) TransPrune-High: 100.0 (-0.0) vs SparseVLM: 98.8 (-1.2) (性能保留率提升1.2个百分点，同时TFLOPs从41.1%降至40.8%)。
> - LLaVA-1.5-7B MME^P 上，MME^P TransPrune-High: 1540 vs SparseVLM: 1484 (高出56分，TFLOPs更低)。
> - LLaVA-NeXT-7B (综合相对准确率) 上，Acc. (%) TransPrune-High: 99.8 (-0.2) vs PDrop: 99.3 (-0.7) (保留率提升0.5个百分点，TFLOPs从45.4%降至40.0%)。

## 概述

当前大视觉语言模型（LVLM）在推理时需要处理大量视觉token，导致计算开销极高。已有的token剪枝方法——无论是基于注意力分数还是token间相似度——普遍存在**固有的位置偏差与任务无关性**，难以可靠地识别与当前指令语义真正相关的视觉token，使得剪枝效率与多模态性能难以兼顾。

针对这一瓶颈，**TransPrune** 提出了一种全新的token重要性评估范式：利用视觉token在LLM各层传播中发生的**表示转换（Token Transition）**——即幅度变化与方向变化——作为重要性的核心信号。其关键洞见在于，LLM中间层（约第7–14层）中token表示的动态变化集中且显著地揭示了语义信息，其指示性强于浅层或深层。通过累积中间层的**Token Transition Variation（TTV）**，并辅以**Instruction-Guided Attention（IGA）**捕捉指令相关的注意力分布，TransPrune使剪枝决策更精准地反映token的语义重要性（见 Figure 2 和 Figure 3）。

实验表明，TransPrune在多个主流LVLM架构上均实现了**性能几乎无损、推理FLOPs减半以上**的效果。在LLaVA-1.5-7B上，TransPrune-High以40.8%的TFLOPs预算达到100.0%的综合相对准确率保留，MME^P得分1540，显著优于SparseVLM（1484）等同类方法（Table 1）；在LLaVA-NeXT-7B和Qwen2.5-VL-7B上同样取得最优的性能-效率权衡（Table 2、Table 3）。此外，TransPrune可与投影端剪枝方法（如VisionZip）正交结合，在进一步压缩至仅保留36个token时仍几乎无损（Table 4）。消融研究系统验证了中间层TTV累积、IGA融合以及幅度-方向双分量的各自贡献（Table 10–12），确认了所提信号和累积策略的有效性。

## 背景与动机

### 大视觉语言模型的推理效率瓶颈

大视觉语言模型（Large Vision-Language Models，LVLM）通过将视觉编码器与大语言模型（LLM）深度耦合，在视觉问答、图像描述等多模态任务上取得了显著进展。然而，这类模型在推理时需处理大量视觉token，导致计算开销急剧膨胀。以LLaVA-1.5-7B为例，其视觉编码器通常为每张图像生成576个视觉token，这些token与指令token一同送入LLM进行逐层自注意力计算，使得LLM前向传播的FLOPs（浮点运算次数）成为推理延迟的主要来源。

为缓解这一瓶颈，研究者提出了多种视觉token剪枝方法，其核心思想是在LLM的浅层或中间层识别并丢弃“不重要”的视觉token，从而降低后续层的计算量。这些方法可大致分为两类：**投影端剪枝**（projector-based pruning）和**LLM内部剪枝**（within-LLM pruning）。投影端方法（如**VisionZip**，Yang et al., CVPR 2025；**CDPruner**，Zhang et al., 2025）在视觉token进入LLM之前进行一次性剪枝，而LLM内部方法（如**FastV**，Chen et al., ECCV 2024；**PDrop**，Xing et al., CVPR 2025；**TopV**，Yang et al., CVPR 2025；**ShortV**，Yuan et al., ICCV 2025；**SparseVLM**，Zhang et al., ICML 2025）则在LLM各层中逐步剪枝，以更精细地利用上下文信息。

### 现有Token重要性评估准则的固有缺陷

现有LLM内部剪枝方法在评估视觉token重要性时，主要依赖两类信号：

1. **注意力分数**：利用LLM某一层（通常是最后一层或特定层）的注意力权重，认为被更多token关注的视觉token更重要。然而，注意力分数天然存在**位置偏差**（position bias）——靠近序列起点的token往往获得更高的注意力权重，这与token的语义重要性无关。此外，注意力分数反映的是token间的交互强度，而非token自身对任务响应的贡献。

2. **token间相似度**：通过计算视觉token与指令token或视觉token之间的余弦相似度来评估冗余性。这类方法虽然部分规避了位置偏差，但相似度度量是**任务无关**的——两个语义相似的token可能对当前问题的回答同等重要，也可能完全冗余，仅凭相似度无法区分这两种情形。

这两种准则的根本问题在于：它们从token的**静态表示**或**token间关系**出发，未能捕捉token表示在LLM各层传播过程中的**动态语义演化**。一个视觉token在浅层可能仅编码低级视觉特征，在中间层逐渐融合语义信息，在深层则可能被压缩为对指令响应至关重要的概念载体。仅依赖某一层的静态快照，难以可靠地判断token对最终多模态输出的贡献。

### TransPrune的核心动机与洞察

TransPrune的提出源于一个关键观察：**视觉token在LLM各层传播过程中经历的表示转换——幅度变化和方向变化——能够揭示其语义重要性**。具体而言，在LLaVA-1.5-7B的可视化分析（Figure 2）中，token表示的幅度变化率（输出与输入L2范数之比）和方向变化（余弦相似度）在中间层（约第6–14层）最为集中且显著。那些幅度变化率较大、方向变化更趋正交的token，往往承载着与图像语义理解密切相关的信息。这一现象表明，**token表示的动态转换过程本身就是一个天然的重要性信号**，无需依赖注意力分数或token间相似度等间接指标。

基于此洞察，TransPrune提出了**Token Transition Variation（TTV）**作为新的重要性评估准则。TTV通过量化每个视觉token在自注意力和FFN模块中的幅度变化率和方向变化，直接捕捉token自身表示的语义演化强度。与注意力分数相比，TTV不涉及token间交互，因而天然免疫位置偏差；与相似度度量相比，TTV反映的是token对模型内部计算的“参与度”，与任务语义隐式相关。

此外，TransPrune进一步引入了**Instruction-Guided Attention（IGA）**，通过计算指令token对视觉token的注意力权重，显式建模任务引导的语义相关性。TTV与IGA的互补融合——前者关注token自身的表示动态，后者关注指令对token的选择性关注——使剪枝决策同时具备语义敏感性和任务相关性，从而在更低的TFLOPs预算下保持甚至提升多模态性能。

## 核心创新

TransPrune 的核心创新在于对视觉 token 重要性评估准则的根本性重构。现有 LLM 内部 token 剪枝方法（如 **FastV** (Chen et al., ECCV 2024)、**PDrop** (Xing et al., CVPR 2025)、**SparseVLM** (Zhang et al., ICML 2025) 等）普遍依赖注意力分数或 token 间相似度作为剪枝依据。这类静态指标存在两个结构性缺陷：一是固有的位置偏差——token 在序列中的位置会系统性影响其注意力权重，而非真实的语义贡献；二是任务无关性——注意力分布无法感知当前指令的具体需求，导致剪枝决策与多模态问答的目标产生错位。

TransPrune 将评估准则从“token 间关系”切换为“token 自身表示在 LLM 层间传播时的动态转换”，提出 **Token Transition Variation (TTV)** 作为全新的重要性信号。TTV 捕捉每个视觉 token 在通过自注意力和 FFN 模块后，其表示的**幅度变化率**（输出与输入 L2 范数之比）和**方向变化**（输出与输入的余弦相似度）。核心洞察在于：LLM 中间层（约第 7–14 层）中 token 表示的动态变化集中且显著地揭示了 token 的语义信息——幅度变化越大、方向越正交的 token，往往承载更关键的语义内容（见 Figure 2 的可视化验证）。TTV 将方向变化经 Softmax 归一化后与幅度变化相乘，形成单模块的重要性得分：

$$m(F, T_{\mathrm{in}}) = \frac{\|T_{\mathrm{out}}\|_2}{\|T_{\mathrm{in}}\|_2},\quad d(F, T_{\mathrm{in}}) = \frac{T_{\mathrm{out}} \cdot T_{\mathrm{in}}}{\|T_{\mathrm{out}}\|_2 \|T_{\mathrm{in}}\|_2}$$

$$\mathrm{TTV}(F, T_I) = \mathrm{Softmax}\left(1 - |d(F, T_I)|\right) \cdot m(F, T_I)$$

为进一步弥补 TTV 在任务感知上的不足，TransPrune 引入 **Instruction-Guided Attention (IGA)**，计算指令 token 对视觉 token 的注意力权重并沿指令序列平均，从而注入当前任务的具体语义引导。最终剪枝分数由 TTV 与 IGA 加权融合：

$$\mathrm{Score}_{p_i}(T_I) = \alpha \cdot \mathrm{TTV}_{p_i}(T_I) + (1 - \alpha) \cdot \mathrm{IGA}_{p_i+1}(T_I)$$

第二个关键创新在于**剪枝决策粒度的转变**。已有方法多依赖单层或仅当前层的统计量进行一次性剪枝，重要性评估易受单层噪声干扰。TransPrune 提出 **TTV 累积机制**：在每个剪枝层决策时，聚合从首个累积层到当前层的全部 TTV 历史：

$$\mathrm{TTV}_{p_i}(T_I) = \sum_{l \in A, l \le p_i} \mathrm{TTV}_l(T_I)$$

消融实验（Table 11）证实，引入累积机制后 MME^P 从 1530 提升至 1540，所有基准均有增益，验证了历史转换信息的累积能显著提高剪枝的稳定性和一致性。层间消融（Table 10）进一步表明，中间层（层 7–12）的 TTV 累积效果（MME^P 1540）远优于浅层（层 1–6，MME^P 1515），印证了中间层转换信号富含语义信息的核心假设。

综上，TransPrune 通过“语义转换信号 + 指令引导 + 多层累积”三位一体的设计，将 token 重要性评估从静态、任务无关的注意力范式，推进到动态、语义感知、历史一致的转换度量范式，在显著降低计算开销的同时保持了多模态性能。

## 整体框架

TransPrune 提出一种基于 token 表示动态转换的逐步剪枝框架，其核心思想是将视觉 token 在 LLM 各层传播中的**幅度变化**和**方向变化**作为重要性信号，并结合指令引导的注意力，在多个中间层分阶段剪除低分 token。

### 框架总览

整个 pipeline 由四个关键模块串联构成，如 Figure 3 所示：

![[assets/figures/papers/paper_list_l793_https_arxiv_org_abs_2507_20630/figures/003_Figure_3.jpg]]
*Figure 3: (a) Overview of TransPrune. During pruning, TransPrune computes image token transitions. Tokens whose transitions are closer in magnitude to those of the original tokens, and that exhibit more orthogonal directional changes, are assigned higher TTV scores. In parallel, we compute IGA by averaging the attention from instruction tokens to image tokens. The final score for each token is obtained by summing TTV and IGA, followed by sorting. (b) Accumulation of TTV. To achieve a more precise TTV, we retain TTV scores from earlier layers. For each pruning stage, we accumulate TTV scores from the first accumulated layer up to the current pruning layer*

1. **Token Transition Variation (TTV) 计算模块**  
   对每个视觉 token，分别在自注意力（Self-Attention）和前馈网络（FFN）两个子模块中计算其表示的转换量。具体而言，对于模块 $F$ 和输入 token 表示 $T_{\mathrm{in}}$，定义：
   - 幅度变化率（L2 范数比）：$m(F, T_{\mathrm{in}}) = \frac{\|T_{\mathrm{out}}\|_2}{\|T_{\mathrm{in}}\|_2}$
   - 方向变化（余弦相似度）：$d(F, T_{\mathrm{in}}) = \frac{T_{\mathrm{out}} \cdot T_{\mathrm{in}}}{\|T_{\mathrm{out}}\|_2 \|T_{\mathrm{in}}\|_2}$

   单模块 TTV 得分通过对方向变化做 Softmax 归一化后乘以幅度变化得到：
   $$\mathrm{TTV}(F, T_I) = \mathrm{Softmax}\left(1 - |d(F, T_I)|\right) \cdot m(F, T_I)$$

   同一层内自注意力和 FFN 的 TTV 相加，形成该层的综合重要性：
   $$\mathrm{TTV}_l(T_I) = \mathrm{TTV}(\mathrm{Attention}, T_I) + \mathrm{TTV}(\mathrm{FFN}, T_I)$$

2. **TTV 累积模块**  
   在预定义的累积层集 $A$（例如层 7–12）上，从首个累积层到当前剪枝层 $p_i$ 的 TTV 被逐层累加：
   $$\mathrm{TTV}_{p_i}(T_I) = \sum_{l \in A, l \le p_i} \mathrm{TTV}_l(T_I)$$
   这一累积机制使剪枝决策能够利用 token 在多个中间层的历史转换信息，提升重要性评估的稳定性和一致性。消融实验（Table 11）表明，引入累积后 MME$^P$ 从 1530 提升至 1540，验证了其有效性。

3. **Instruction-Guided Attention (IGA) 计算模块**  
   为弥补 TTV 仅关注 token 自身转换、缺乏任务引导的不足，TransPrune 同时计算指令 token 对视觉 token 的注意力权重，并沿指令序列取平均：
   $$\mathrm{IGA}(T_I) = \frac{1}{L} \sum_{j=1}^{L} A_j$$
   其中 $A_j$ 为第 $j$ 个指令 token 对视觉 token 的注意力值。IGA 从任务语义维度评估 token 相关性，与 TTV 形成互补。

4. **组合评分与剪枝模块**  
   在每个剪枝阶段 $p_i$，用超参数 $\alpha$ 加权融合累积 TTV 和 IGA：
   $$\mathrm{Score}_{p_i}(T_I) = \alpha \cdot \mathrm{TTV}_{p_i}(T_I) + (1 - \alpha) \cdot \mathrm{IGA}_{p_i+1}(T_I)$$
   按综合分数排序后，剪除低分 token。消融实验（Table 13）显示 $\alpha=0.5$ 时性能最优，表明均衡利用 token 自身转换信号和指令引导信号最为有效。

### 输入输出流

- **输入**：视觉编码器输出的视觉 token 序列 $T_I$，以及文本指令 token 序列。
- **处理流程**：视觉 token 进入 LLM 后，在多个预设的剪枝层（如层 7、9、12）分阶段执行剪枝。每个剪枝阶段依次完成 TTV 计算与累积、IGA 计算、分数融合和 token 淘汰。
- **输出**：经过逐层剪枝后保留的高重要性视觉 token 子集，与指令 token 一同继续参与后续层的推理，直至生成最终的多模态回答。

### 核心设计选择

- **中间层聚焦**：Figure 2 的可视化和 Table 10 的消融均表明，token 表示的幅度与方向变化在 LLM 中间层（约第 7–14 层）最为集中且显著，与语义重要性高度相关。因此 TransPrune 将 TTV 累积范围限定在中间层，使用浅层（层 1–6）时 MME$^P$ 从 1540 降至 1515。
- **渐进式剪枝**：不同于依赖单层统计量的一次性剪枝，TransPrune 在多个层分阶段剪枝，每次剪枝都利用累积至今的 TTV 历史，使重要性评估随层加深而愈发稳健。
- **双信号融合**：TTV 从 token 自身表示的动态变化中捕捉语义重要性，IGA 从指令-视觉交互中捕捉任务相关性，二者互补。仅使用 TTV 时 GQA 降至 58.4（完整方法为 61.4，Table 7），仅使用 IGA 时 MME$^P$ 为 1514（完整方法为 1540，Table 12），验证了双信号融合的必要性。

## 核心模块与公式推导

TransPrune的核心由四个紧密协作的模块构成，它们共同将“token表示转换”这一新信号转化为可操作的剪枝决策。

### Token Transition Variation (TTV) 计算模块

该模块是TransPrune的信号源，负责量化每个视觉token在LLM各层传播时自身表示发生的动态变化。对于任意一个Transformer子模块 $F$（自注意力或FFN），给定输入token表示 $T_{\mathrm{in}}$ 和输出token表示 $T_{\mathrm{out}}$，首先分别计算幅度变化率与方向变化：

$$m(F, T_{\mathrm{in}}) = \frac{\|T_{\mathrm{out}}\|_2}{\|T_{\mathrm{in}}\|_2},\quad d(F, T_{\mathrm{in}}) = \frac{T_{\mathrm{out}} \cdot T_{\mathrm{in}}}{\|T_{\mathrm{out}}\|_2 \|T_{\mathrm{in}}\|_2}$$

其中 $m(\cdot)$ 为L2范数比，反映表示强度的缩放；$d(\cdot)$ 为余弦相似度，反映表示方向的保持程度。随后，将方向变化经Softmax归一化后与幅度变化相乘，得到单模块的TTV得分：

$$\mathrm{TTV}(F, T_I) = \mathrm{Softmax}\left(1 - |d(F, T_I)|\right) \cdot m(F, T_I)$$

这一设计的直觉在于：方向变化越剧烈（余弦相似度绝对值越小）、幅度变化越显著（范数比越大）的token，其表示经历了更大幅度的语义转换，因而更可能承载关键信息。最后，将同一层内自注意力和FFN两个子模块的TTV相加，形成该层的综合重要性评分：

$$\mathrm{TTV}_l(T_I) = \mathrm{TTV}(\mathrm{Attention}, T_I) + \mathrm{TTV}(\mathrm{FFN}, T_I)$$

### TTV累积模块

单层TTV可能受局部噪声影响，TransPrune引入了跨层累积机制以提升评分的稳定性。在第 $i$ 个剪枝层 $p_i$ 进行决策时，从首个累积层开始直至当前层的所有TTV被求和聚合：

$$\mathrm{TTV}_{p_i}(T_I) = \sum_{l \in A, l \le p_i} \mathrm{TTV}_l(T_I)$$

其中 $A$ 为预定义的累积层集合。消融实验（Table 11）证实，引入累积机制后MME$^P$从1530提升至1540，所有基准均有增益，说明历史转换信息的累积能有效抑制单层评分的波动。

### Instruction-Guided Attention (IGA) 计算模块

TTV仅从token自身转换角度评估重要性，缺乏对当前指令语义的感知。IGA模块通过计算指令token对视觉token的注意力权重来弥补这一缺陷：

$$\mathrm{IGA}(T_I) = \frac{1}{L} \sum_{j=1}^{L} A_j$$

其中 $L$ 为指令token序列长度，$A_j$ 为第 $j$ 个指令token对所有视觉token的注意力分布。沿指令维度取平均后，IGA反映了视觉token被指令token整体关注的程度，即其任务相关性。消融实验（Table 7）显示，仅使用TTV而移除IGA时，GQA从61.4骤降至58.4，证明了IGA在捕捉指令相关信息方面的不可替代性。

### 组合评分与剪枝模块

最终，TTV累积评分与IGA通过超参数 $\alpha$ 进行加权融合：

$$\mathrm{Score}_{p_i}(T_I) = \alpha \cdot \mathrm{TTV}_{p_i}(T_I) + (1 - \alpha) \cdot \mathrm{IGA}_{p_i+1}(T_I)$$

按综合分数排序后，剪除低分token。消融实验（Table 13）表明，$\alpha=0.5$ 时性能最优，即均衡利用token自身转换信号和指令引导信号最为有效。从仅使用IGA的MME$^P$ 1514提升至完整方法的1540（Table 12），幅度分量与方向分量共同贡献了这一增益。

### 补充图表

![[assets/figures/papers/paper_list_l793_https_arxiv_org_abs_2507_20630/figures/002_Figure_2.jpg]]
*Figure 2: Token Transition Visualization in LLaVA-v1.5-7B. We visualize the magnitude and direction changes of token representations within both the self-attention and FFN modules for each layer (excluding residual connections). To measure the magnitude change, we use the ratio of output to input L2 norm; to measure the directional change, we use cosine similarity. Token transitions that reflect semantic importance can be observed across shallow, middle, and deep layers, and they are most concentrated and pronounced in the middle layers (around layers 6–14), where tokens with larger ratios and smaller absolute cosine similarities tend to be more semantically important. We provide more visualization e...*

## 实验与分析

### 主结果：多模型、多基准下的高效剪枝

TransPrune 作为 LLM 内部剪枝方法，在三种主流 LVLM 架构上均以更低的 TFLOPs 预算实现了最优或次优的性能保留。Table 1 展示了在 LLaVA-1.5-7B 上的全面对比：TransPrune-High 在仅使用 40.8% TFLOPs 的条件下，综合相对准确率达到 100.0%（即与未剪枝模型性能无衰减），而此前最强的 SparseVLM（Zhang et al., ICML 2025）在 41.1% TFLOPs 下仅保留 98.8% 准确率。在感知密集型基准 MME^P 上，TransPrune-High 取得 1540 分，比 SparseVLM 的 1484 分高出 56 分，同时计算量更低。TransPrune-Low 进一步将 TFLOPs 压缩至 37.0%，仍保持 98.4% 的相对准确率，优于同等预算下所有对比方法。

![[assets/figures/papers/paper_list_l793_https_arxiv_org_abs_2507_20630/figures/004_Table_1.jpg]]
*Table 1: Performance of within-LLM methods across different benchmarks on LLaVA-1.5-7B. TransPrune-High and TransPrune-Low achieve the best performance under low TFLOPs settings. Bold font highlights the best-performing results, and underlined values denote the second-best performance*

在 LLaVA-NeXT-7B 上（Table 2），TransPrune-High 以 40.0% TFLOPs 达到 99.8% 的相对准确率，超过 PDrop（Xing et al., CVPR 2025）的 99.3%（45.4% TFLOPs），在更低的计算开销下实现了更优的性能保留。在 Qwen2.5-VL-7B 上（Table 3），TransPrune 在 MME^P 上取得 1580 分，显著优于 FastV（Liang Chen et al., ECCV 2024）的 1563 分，且 TFLOPs 从 53.6% 降至 45.1%。这些跨架构的一致性结果表明，基于 token 转换信号的重要性评估准则具有较好的泛化性。

![[assets/figures/papers/paper_list_l793_https_arxiv_org_abs_2507_20630/figures/005_Table_2.jpg]]
*Table 2: Performance of within-LLM methods across different benchmarks on LLaVA-Next-7B. TransPrune-High and TransPrune-Low achieve the best performance under low TFLOPs settings*

![[assets/figures/papers/paper_list_l793_https_arxiv_org_abs_2507_20630/figures/006_Table_3.jpg]]
*Table 3: Performance of within-LLM methods across different benchmarks on Qwen2.5-VL-7B*

### 与投影端方法的协同效应

TransPrune 作为 LLM 内部剪枝方法，可与投影端剪枝方法无缝叠加，实现端到端的极致压缩。当与 VisionZip（Yang et al., CVPR 2025）结合时（Table 4），在仅保留 24 个视觉 token、TFLOPs 降至 0.44（原始模型的 11.5%）的极端设定下，综合准确率仍达 97.2%，与单独使用 VisionZip 的 98.4% 仅有 1.2 个百分点的差距。与 CDPruner（Zhang et al., 2025）结合时（Table 5），同样在 24 token、0.44 TFLOPs 下达到 97.6% 准确率。这表明 TransPrune 的剪枝信号与投影端方法的压缩策略是互补的——前者在 LLM 内部剔除语义冗余，后者在输入阶段减少 token 数量，二者叠加可在几乎不牺牲性能的前提下将计算量压缩一个数量级。

![[assets/figures/papers/paper_list_l793_https_arxiv_org_abs_2507_20630/figures/007_Table_4.jpg]]
*Table 4: Performance when combined with the projector-based method VisionZip. Our method achieves a reduction in FLOPs while maintaining performance comparable to VisionZip alone*

![[assets/figures/papers/paper_list_l793_https_arxiv_org_abs_2507_20630/figures/008_Table_5.jpg]]
*Table 5: Performance when combined with the projector-based method CDPruner. Our method achieves a reduction in FLOPs while maintaining performance comparable to CDPruner alone*

### 视频理解的扩展性

在 Video-LLaVA 视频基准上（Table 6），TransPrune 同样展现出优势。相比 FastV 和 PDrop 等基线，TransPrune 在多个视频问答任务上以更低的 TFLOPs 取得更高得分，说明基于 token 转换动态的重要性评估在时序视觉场景中依然有效。需要注意的是，视频场景下视觉 token 数量成倍增长，剪枝的收益更为显著。

### 消融实验：TTV 与 IGA 的各自贡献

Table 7 的消融实验直接验证了 IGA 的必要性：仅使用 TTV 进行剪枝（无指令引导）时，GQA 得分从完整方法的 61.4 骤降至 58.4，表明纯自监督的转换信号无法充分捕捉任务相关的语义需求。IGA 通过聚合指令 token 对视觉 token 的注意力，为剪枝决策引入了任务导向的语义约束，是方法完整性的关键组件。

![[assets/figures/papers/paper_list_l793_https_arxiv_org_abs_2507_20630/figures/010_Table_7.jpg]]
*Table 7: Performance using only TTV*

### 消融实验：中间层转换信号的有效性

Table 10 对比了在不同层区间累积 TTV 的效果。使用中间层（层 7–12）的 TTV 累积在 MME^P 上达到 1540 分，而使用浅层（层 1–6）仅为 1515 分。这定量验证了 Figure 2 的可视化发现：token 表示的幅度变化率和方向变化在中间层最为集中和显著，且与语义重要性高度相关。浅层主要进行局部特征编码，深层趋于收敛，中间层的表示转换承载了最丰富的语义重组信息。

![[assets/figures/papers/paper_list_l793_https_arxiv_org_abs_2507_20630/figures/018_Table_10.jpg]]
*Table 10: Impact of accumulated TTV across different layers*

### 消融实验：累积机制与信号分量

Table 11 验证了 TTV 累积机制的增益：引入跨层累积后，MME^P 从 1530 提升至 1540，所有基准均有正向提升。累积机制通过聚合历史转换信号，平滑了单层噪声，使重要性评估更稳健。

![[assets/figures/papers/paper_list_l793_https_arxiv_org_abs_2507_20630/figures/014_Table_11.jpg]]
*Table 11: Ablation study on the impact of accumulation*

Table 12 进一步拆解了 TTV 的幅度分量与方向分量的贡献。幅度分量对性能提升的贡献大于方向分量，但两者结合效果最佳——仅使用 IGA 时 MME^P 为 1514，加入完整 TTV 后提升至 1540。这证实了 token 自身转换信号（TTV）与指令引导信号（IGA）的互补性。

![[assets/figures/papers/paper_list_l793_https_arxiv_org_abs_2507_20630/figures/016_Table_12.jpg]]
*Table 12: Ablation study on the impact of direction and magnitude*

### 超参数与层选择

超参数 α 控制 TTV 与 IGA 的融合权重。Table 13 显示 α=0.5 时性能最优，表明等权重融合两种信号最为有效，过度偏向任一方都会削弱剪枝质量。

![[assets/figures/papers/paper_list_l793_https_arxiv_org_abs_2507_20630/figures/017_Table_13.jpg]]
*Table 13: Ablation study on the impact of parameter α*

Table 9 探索了不同剪枝层组合的影响。实验表明在层 7、9、12 处执行剪枝（累积层从 5 至 12）在 MME 上达到最佳性能（1540 分），这与中间层转换信号最丰富的发现一致。过早剪枝（如层 5 开始）会丢失尚未充分转换的语义信息，过晚剪枝则计算节省有限。

### 实际效率：延迟与内存

Table 8 报告了在 MME 基准上的实测延迟与内存占用。TransPrune 在取得最高准确率（1540）的同时，延迟为 111.4 ms，内存占用 14.82 GB，均优于或持平于 FastV、SparseVLM 等基线。这验证了 TTV 和 IGA 的额外计算开销（L2 范数、余弦相似度、指令-视觉注意力）在实际部署中是可接受的，剪枝带来的 token 数量减少足以抵消这些开销。

### Token 位置偏好分析

Figure 4 统计了 IGA 和 TTV 在 MME 基准上保留 token 的位置频率分布。IGA 倾向于保留与指令语义直接相关的 token，TTV 则更关注表示转换剧烈的 token，二者在位置偏好上形成互补，共同覆盖了指令相关性与语义重要性的双重维度。Figure 5 的可视化示例进一步展示了 TransPrune 在不同 VQA 提示下能自适应地保留与问题相关的视觉区域，验证了方法的任务感知能力。

## 方法谱系与知识库定位

### 核心创新与差异化定位

TransPrune属于**LLM内部（within-LLM）视觉token剪枝**方法，其核心创新在于引入了一种全新的token重要性评估信号——**Token Transition Variation (TTV)**，并辅以**Instruction-Guided Attention (IGA)**，从token自身表示的动态变化和指令相关性两个维度进行联合评估。这与现有方法形成了根本性的差异。

现有within-LLM剪枝方法主要依赖两类信号：
- **基于注意力的方法**：如**FastV**（Liang Chen et al., ECCV 2024）利用LLM最后一层的注意力分数进行一次性剪枝；**PDrop**（Xing et al., CVPR 2025）、**TopV**（Yang et al., CVPR 2025）和**ShortV**（Yuan et al., ICCV 2025）在不同层基于注意力进行渐进式剪枝。这类方法的根本问题在于注意力分数存在固有的**位置偏差**，且多为**任务无关**的统计量，难以可靠地反映token与当前指令的语义关联。
- **基于相似度的方法**：如**SparseVLM**（Zhang et al., ICML 2025）通过计算token间的相似度来识别冗余token。这类方法同样缺乏对任务语义的显式建模。

TransPrune的关键突破在于将评估准则从“token之间的关系”（注意力/相似度）转向“token自身的动态变化”（TTV）。如Figure 2所示，token表示在LLM中间层（约第7–14层）的幅度变化率和方向变化最集中且显著，且与语义重要性高度相关。这一观察构成了方法的理论基石。

### 与投影端方法的协同关系

TransPrune作为within-LLM方法，与投影端（projector-based）剪枝方法处于**互补而非竞争**的关系。投影端方法如**VisionZip**（Yang et al., CVPR 2025）和**CDPruner**（Zhang et al., 2025）在视觉token进入LLM之前进行剪枝，而TransPrune在LLM内部进一步筛选。实验表明（Table 4, Table 5），将TransPrune与VisionZip或CDPruner级联使用，可在投影端已剪枝的基础上进一步压缩至仅保留24–36个token，TFLOPs降至0.44–0.78，性能几乎无损（相对准确率97.2%–98.0%），验证了两类方法的正交性和可组合性。

### 适用边界与泛化能力

从实验覆盖的模型和任务来看，TransPrune展现出较强的泛化能力：
- **模型泛化**：在LLaVA-1.5-7B、LLaVA-NeXT-7B和Qwen2.5-VL-7B三个不同架构的LVLM上均取得最优性能（Table 1–3），表明TTV信号对不同LLM骨干具有通用性。
- **任务泛化**：在图像理解（MME、GQA、POPE等）和视频理解（Video-LLaVA, Table 6）任务上均有效，说明token转换信号捕捉的是跨模态的通用语义重要性。
- **效率边界**：方法在TFLOPs约40%–50%的区间内性能保留率最优，且在与投影端方法结合后可进一步压缩至TFLOPs约11.5%的极端低预算场景（Table 4, Table 5）。

### 消融实验揭示的关键机制

消融实验为方法的有效性提供了因果层面的证据链：

1. **IGA的必要性**：仅使用TTV（无IGA）时，GQA从61.4降至58.4（Table 7），表明纯token自身信号缺乏对任务指令的感知能力，IGA弥补了这一缺陷。

2. **中间层TTV的优越性**：使用层7–12的TTV累积在MME^P上达到1540，而浅层（层1–6）仅为1515（Table 10），直接验证了Figure 2的可视化观察——中间层的转换信号最富含语义信息。

3. **累积机制的贡献**：引入TTV累积后，MME^P从1530提升至1540，所有基准均有增益（Table 11），说明历史转换信息的聚合能平滑单层噪声，提高重要性评估的稳定性和一致性。

4. **幅度与方向的互补性**：TTV中的幅度分量对性能提升贡献大于方向分量，但两者结合（IGA+TTV）效果最佳，从仅IGA的1514提升至1540（Table 12）。

5. **融合权重的均衡性**：超参数α设为0.5时性能最优（Table 13），说明均衡利用token自身信号和指令信号最为有效。

### 局限与开放问题

尽管实验证据充分，以下方面仍需关注：

- **计算开销的精确量化**：论文提供了总FLOPs的近似表达式（Section 4.3），但TTV计算中涉及的L2范数和余弦相似度的实际推理延迟增量（Table 8显示TransPrune延迟为111.4ms，低于部分基线但高于FastV的105.2ms）需要在更多硬件平台上验证。
- **剪枝层选择的自动化**：当前剪枝层组合（如7,9,12）通过网格搜索确定（Table 9），缺乏自适应的层选择机制，可能限制在不同深度LLM上的即插即用性。
- **极端压缩场景的鲁棒性**：在与投影端方法结合至24 token的极端场景下，性能开始出现轻微下降（Table 4, Table 5中97.2%–98.0% vs 原始98.4%），更极端的压缩边界尚不明确。
- **长文本/多轮对话场景**：当前实验主要基于单轮VQA基准，TTV信号在多轮交互中是否保持一致性需要进一步验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/TransPrune_Token_Transition_Pruning_for_Efficient_Large_Vision_Language_Model.pdf]]
