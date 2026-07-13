---
title: "FlashDLM: Accelerating Diffusion Language Model Inference via Efficient KV Caching and Guided Diffusion"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/FlashDLM_Accelerating_Diffusion_Language_Model_Inference_via_Efficient_KV_Caching_and_Guided_Diffusion.pdf
project_link: null
code_link: https://github.com/ZhanqiuHu/flash-dlm-experimental
openreview_forum_id: KUfKvlX3VY
aliases:
- FFGD
- FlashDLM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "通过缓存已稳定 token 的键值（KV）投影来避免重复计算（FreeCache），以及利用轻量级自回归模型对扩散生成的 token 进行一致性引导（Guided Diffusion），在几乎不损失准确率的情况下大幅减少所需计算量和去噪迭代次数。"
primary_logic: "已完成去噪的 token 的 KV 投影在后续步骤中具有高度时间稳定性（余弦相似度高），可以安全地缓存而不会严重影响输出质量；利用小型自回归模型的预测一致性作为免训练的信号，能够安全地并行揭晓多个 token，有效缓解因子化限制并减少总去噪步数。"
claims:
- "KV 投影在干净 token 上随时间高度稳定，余弦相似度接近 1。"
- "FreeCache 在 Dream-7B-Instruct 上实现 4.42 倍加速，准确率仅下降 2.28 个百分点（79.68% → 77.40%）。"
- "FreeCache+Qwen2.5-1.5B-Instruct 引导扩散在 PiQA 上实现 34.1 倍加速（0.43s vs 14.62s）。"
- "Guided Diffusion 无需 token 级校正，与投机解码不同，仅使用 AR 模型的一致性信号。"
---

# FlashDLM: Accelerating Diffusion Language Model Inference via Efficient KV Caching and Guided Diffusion

> [!tip] 核心洞察
> 已完成去噪的 token 的 KV 投影在后续步骤中具有高度时间稳定性（余弦相似度高），可以安全地缓存而不会严重影响输出质量；利用小型自回归模型的预测一致性作为免训练的信号，能够安全地并行揭晓多个 token，有效缓解因子化限制并减少总去噪步数。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | FlashDLM：通过高效KV缓存和引导扩散加速扩散语言模型推理 |
| 英文题名 | FlashDLM: Accelerating Diffusion Language Model Inference via Efficient KV Caching and Guided Diffusion |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=KUfKvlX3VY) · [GitHub](https://github.com/ZhanqiuHu/flash-dlm-experimental) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | FlashDLM (FreeCache + Guided Diffusion) |
| Dataset | GSM8K (8-shot), MMLU-PRO, PiQA |

> [!tip] 效果简介
> - GSM8K (8-shot) 上，准确率 / 延迟 / 加速比 为 77.40% / 10.87s / 4.42× (FreeCache)，对比 79.68% / 48.05s / 1.0× (Dream-7B-Instruct baseline)，变化 准确率 -2.28%，加速 4.42×。
> - GSM8K (8-shot) 上，准确率 / 延迟 / 加速比 为 80.30% / 2.70s / 17.80× (FreeCache+Qwen2.5-1.5B Guided)，对比 79.68% / 48.05s / 1.0×，变化 准确率 +0.62%，加速 17.80×。
> - MMLU-PRO 上，准确率 / 延迟 / 加速比 为 46.64% / 2.35s / 12.48× (FreeCache+Qwen2.5-1.5B Guided)，对比 46.92% / 29.33s / 1.0×，变化 准确率 -0.28%，加速 12.48×。

## 概要

扩散语言模型（Diffusion Language Model, DLM）以并行去噪的方式生成文本，但其推理效率长期受困于一个根本矛盾：每次去噪步骤都需要对**全序列**执行前向计算，导致计算复杂度较自回归模型高出 O(L) 倍（Table 1）。这一瓶颈在长上下文场景中尤为突出，使 DLM 的实际部署面临严重的延迟与计算成本压力。与此同时，并行揭晓多个 token 所依赖的因子化分布假设，天然限制了 token 间的语义连贯性，激进去噪策略往往伴随生成质量的显著退化（Figure 1a）。

本文提出 **FlashDLM**，一个完全免训练的推理加速框架，由两项互补技术构成：

- **FreeCache**：基于一个关键经验发现——已完成去噪的 token 的 Key/Value 投影在后续步骤中具有高度时间稳定性（余弦相似度接近 1，Figure 2）——对已稳定 token 块冻结其 KV 缓存，仅对活动窗口内的 token 重新计算，从而大幅削减冗余计算。
- **Guided Diffusion**：引入轻量级预训练自回归模型作为引导者，对扩散模型提议的 token 进行一致性检查，仅揭晓与 AR 模型预测一致的 token。这有效缓解了因子化限制带来的 token 间不连贯问题，并显著减少所需去噪迭代次数。与投机解码不同，Guided Diffusion 无需 token 级校正，仅依赖一致性信号。

在方法谱系中，FlashDLM 定位于**扩散语言模型推理加速**这一新兴方向，区别于传统的启发式揭晓策略（如基于熵或 Top-K Margin 的并行解码）和需要额外训练的加速方案。其基线参照包括 **Dream-7B-Instruct**（Ye et al., 2025）和 **LLaDA-8B-Instruct**（Nie et al., 2025）等前沿 DLM，引导模型则选用 **Qwen2.5 系列** 自回归模型。

综合实验表明，FlashDLM 在多个基准上实现了显著的端到端加速，同时保持准确率几乎无损：在 Dream-7B-Instruct 上平均加速 **12.14×**，在 LLaDA-8B-Instruct 上平均加速 **13.29×**。其中，FreeCache 单独在 Dream-7B-Instruct 的 GSM8K（8-shot）任务上实现 **4.42×** 加速，准确率仅从 79.68% 降至 77.40%（Table 2）；叠加 Qwen2.5-1.5B-Instruct 引导扩散后，GSM8K 加速达 **17.80×**，准确率反超基线至 80.30%（Table 3），在 PiQA 上更实现 **34.10×** 加速。值得注意的是，较小的引导模型（如 Qwen2.5-1.5B）即可提供足够的一致性信号，且加速比更高，这为实际部署提供了极具吸引力的效率-质量权衡。

FlashDLM 表明，通过挖掘 DLM 去噪过程中的时间冗余和引入轻量外部一致性信号，可以在不修改模型权重、不增加训练成本的条件下，将扩散语言模型的推理效率推向实用水平。其局限性在于 FreeCache 依赖 KV 稳定性假设，该假设在不同架构和任务上的普适性尚待进一步验证；固定块大小策略可能非最优；评估范围目前限于两个 DLM 模型和有限任务类型。



### 扩散语言模型的推理瓶颈

扩散语言模型（Diffusion Language Model, DLM）通过在离散 token 空间上迭代去噪生成文本，避免了自回归（AR）模型的逐 token 串行解码限制。然而，这一生成范式带来了显著的计算开销：在每一个去噪步骤中，DLM 需要对全序列长度 $L$ 的所有 token 执行前向传播，而 AR 模型在解码阶段仅需处理长度为 $l$ 的前缀（$l \ll L$）。如 Table 1 所示，多头注意力（MHA）模块的复杂度从 AR 的 $O(l^2)$ 膨胀为 DLM 的 $O(L^2)$，前馈网络（FFN）模块也从 $O(l)$ 增长至 $O(L)$。这一 $O(L)$ 倍的额外计算量直接导致 DLM 推理延迟显著高于同规模 AR 模型，尤其在长上下文场景下成为实用化的核心瓶颈。

### 并行揭晓的语义连贯性困境

为减少去噪迭代次数，现有 DLM 通常采用启发式置信度策略（如 Top-K Margin 或熵阈值）在单步内并行揭晓多个 token。然而，这种激进的揭晓方式受限于 DLM 的因子化分布假设——模型在预测掩码位置时假设各位置相互独立，忽略了 token 间的语义依赖关系。如 Figure 1(a) 所示，随着去噪步数减少（即单步揭晓 token 数增加），生成质量急剧下降。这一现象揭示了 DLM 推理中“速度-质量”的根本性张力：并行揭晓越多，语义连贯性损失越严重。

### 现有加速方法的局限

面向 AR 模型的投机解码（Speculative Decoding）通过小模型草稿生成、大模型逐 token 校正来实现无损加速，但该范式无法直接迁移至 DLM。DLM 的全序列并行生成特性使得逐 token 校正既违背其设计初衷，又无法充分利用扩散模型的并行草稿能力。此外，针对 DLM 的现有加速工作多集中于减少去噪步数，却忽视了每一步内部重复计算全序列 KV 投影所带来的冗余开销。

### 本文动机与核心观察

本文从两个层面重新审视 DLM 推理效率问题：

**观察一：KV 投影的时间稳定性。** 在 DLM 的去噪过程中，早期已收敛的“干净” token 在后续步骤中几乎不再变化。如 Figure 2 所示，这些 token 的 Key 和 Value 投影在后续去噪步骤间的余弦相似度接近 1，表明其 KV 状态高度稳定。这意味着对这些已完成 token 重复计算 KV 投影是冗余的，直接缓存其 KV 状态即可近似替代重计算。

**观察二：轻量 AR 模型可提供免训练的一致性引导。** 与投机解码要求 AR 模型进行 token 级校正不同，AR 模型仅需对 DLM 的草稿 token 提供“是否一致”的二值信号，即可安全地并行揭晓多个 token。由于不涉及 token 生成或校正，一个轻量级的预训练 AR 模型（如 Qwen2.5-1.5B-Instruct）即可胜任此角色，其额外延迟开销极小。

基于上述观察，本文提出 **FlashDLM**，包含两个免训练的互补技术：**FreeCache**（通过窗口化 KV 缓存消除已稳定 token 的重复计算）和 **Guided Diffusion**（利用轻量 AR 模型的一致性信号安全地并行揭晓 token）。两者协同作用，在几乎不损失准确率的前提下大幅降低 DLM 推理的计算量和去噪迭代次数。



## 核心方法与创新机理

FlashDLM 的核心创新直指扩散语言模型（DLM）推理的两大根本瓶颈：**逐步骤全序列重计算**导致的计算冗余，以及**并行揭晓的因子化分布**引发的 token 间语义断裂。围绕这两个瓶颈，论文提出了两个免训练的即插即用模块——**FreeCache** 与 **Guided Diffusion**，二者协同将端到端推理加速提升至 **12.14× 平均加速比**（Dream-7B-Instruct），同时几乎不损失准确率。

### 瓶颈一：KV 投影的重复计算 → FreeCache

**Baseline 行为**：标准 DLM 推理在每一轮去噪步骤中都对全序列（长度 $L$）重新计算所有 token 的 Key 和 Value 投影。如表 1 所示，这导致 DLM 的 MHA 和 FFN 模块复杂度为 $O(L^2)$ 和 $O(L)$，相比自回归模型每 token 仅需 $O(l)$ 或 $O(l^2)$（$l$ 为前缀长度），DLM 存在 $O(L)$ 倍的额外计算开销。

**核心发现**：论文通过实验揭示了一个关键现象——**已完成去噪的“干净”token 的 KV 投影在后续步骤中具有高度时间稳定性**。Figure 2 的热图显示，这些 token 的 K 和 V 投影余弦相似度接近 1，变化极小。这意味着重复计算这些稳定投影是纯粹的浪费。

**Changed Slot：KV 缓存策略**

| 维度 | Baseline | FreeCache |
|------|----------|-----------|
| 计算范围 | 每步重算全序列所有 token 的 KV | 仅重算活动窗口内 token 的 KV |
| 缓存机制 | 无缓存，每次全量计算 | 对已完成块冻结 KV 投影并复用 |
| 窗口策略 | 固定全序列 | 渐进式缩小窗口，块完成后收缩 |

FreeCache 的具体运作机制（Section 3.2.1）：
1. **初始前向传播**：对全序列计算并保存完整的 KV 投影
2. **块划分**：将生成序列划分为固定大小的块 $B_1, B_2, \dots$
3. **窗口化重计算**：当前活动窗口定义为当前块 $B_i$ 及其后续所有块；仅对该窗口内的 token 重新计算 KV 投影
4. **渐进式冻结**：当块 $B_i$ 完成去噪后，其 KV 投影被冻结，活动窗口随之缩小至 $B_{i+1}$ 及后续块

这一策略的因果逻辑清晰：**KV 稳定性的时间衰减规律**使得“越早完成的 token，其 KV 变化越小”，因此可以安全冻结。实验证据（Table 2）表明，FreeCache 在 Dream-7B-Instruct 上实现 **4.42× 加速**，准确率仅从 79.68% 降至 77.40%（-2.28 个百分点）；在 LLaDA-8B-Instruct 上实现 **6.32× 加速**。

### 瓶颈二：并行揭晓的因子化限制 → Guided Diffusion

**Baseline 行为**：DLM 在每个去噪步骤中，基于启发式置信度策略（如 Top-K Margin、熵）并行揭晓多个 token。然而，并行揭晓依赖于掩码位置上的因子化分布假设，这限制了模型对 token 间联合依赖关系的建模能力，导致生成的 token 缺乏语义连贯性（Section 3.1.2）。Figure 1(a) 显示，随着去噪步数减少，MaskGIT、熵基方法和 Top-K Margin 方法的准确率均显著下降。

**核心发现**：与其让 DLM 独自决定揭晓哪些 token，不如引入一个外部一致性信号来把关。论文发现，**轻量级自回归模型可以作为“引导者”提供免训练的一致性检查**，无需 token 级校正即可有效缓解因子化限制。

**Changed Slot：token 揭晓策略**

| 维度 | Baseline | Guided Diffusion |
|------|----------|------------------|
| 揭晓决策 | 基于 DLM 自身置信度（启发式） | 基于 DLM 提议与 AR 模型预测的一致性 |
| 校正机制 | 无外部验证 | AR 模型匹配检查，无需 token 级校正 |
| 揭晓数量 | 固定或启发式动态 | 由匹配规则 $\mathcal{M}$ 动态确定安全揭晓位数 $k$ |

Guided Diffusion 的运作机制（Section 3.2.2，Figure 3）：
1. **扩散草稿生成**：DLM $f_\theta$ 对所有掩码位置预测 logits，通过策略 $\pi$ 选择提议 token：$t^{\mathrm{DLM}} = \pi(\mathrm{Softmax}(f_{\theta}(x)))$
2. **AR 引导一致性检查**：轻量级 AR 模型 $g_\phi$ 接收扩散草稿，计算自身 logits：$\mathrm{logits}^{\mathrm{AR}} = \mathrm{Softmax}(g_{\phi}(t^{\mathrm{DLM}}))$
3. **匹配揭晓**：通过匹配规则确定安全揭晓的 token 数量 $k = \mathcal{M}(t^{\mathrm{DLM}}, \mathrm{logits}^{\mathrm{AR}})$，仅揭晓与 AR 模型预测一致的 token

这一设计与投机解码有本质区别：**投机解码需要 AR 模型进行 token 级校正**，而 Guided Diffusion 仅使用 AR 模型的一致性信号，无需校正步骤（Section 3.2.2）。由于 AR 引导者只提供“同意/不同意”信号而非生成或校正 token，一个轻量级模型（如 Qwen2.5-1.5B-Instruct）即可胜任，最小化额外延迟开销。

### 协同效应

两种创新的协同体现在因果链的互补上：
- **FreeCache 解决计算瓶颈**：通过缓存稳定 KV 投影，大幅减少每步的计算量
- **Guided Diffusion 解决迭代瓶颈**：通过 AR 引导安全地并行揭晓更多 token，大幅减少总去噪步数

实验数据（Table 3）验证了这一协同效果：在 Dream-7B-Instruct 上，FreeCache + Qwen2.5-1.5B 引导在 PiQA 上实现 **34.1× 加速**（0.43s vs 14.62s），准确率甚至略有提升（83.73% vs 83.58%）；在 GSM8K 上实现 **17.80× 加速**，准确率从 79.68% 提升至 80.30%。值得注意的是，引导扩散甚至能将较小的 Qwen2.5-1.5B 在 GSM8K 上的准确率从 68.54% 提升至 80.3%（Table 4），显示出引导机制本身对生成质量的改善作用。

### 方法边界与待验证点

- **KV 稳定性假设的泛化性**：FreeCache 依赖于 KV 投影的时间稳定性，该假设仅在 Dream-7B-Instruct 和 LLaDA-8B-Instruct 上验证，是否适用于其他 DLM 架构或任务需进一步确认
- **引导模型的规模权衡**：较大的引导模型（如 Qwen2.5-7B）可能提供更强的引导信号但增加延迟和显存（Table 6 显示总显存从 18.7GB 增至 31.9GB），较小的引导模型可能降低准确率——最优选择需根据具体场景权衡
- **块大小策略**：FreeCache 采用固定块大小，Table 7 显示块大小 32 vs 64 会影响加速比和准确率的权衡，自适应动态调整策略有待探索



![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_KUfKvlX3VY/figures/007_Figure_3.jpg]]
*Figure 3: AR-guided Diffusion Model. The diffusion model performs a one-step diffusion process, followed by a one-time forward pass of the AR guider. The matched tokens are unmasked for the next step of diffusion*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_KUfKvlX3VY/figures/005_Figure_2.jpg]]
*Figure 2: Rationale behind the proposed FreeCache: The variation of K and V projections of clean tokens is small throughout the subsequent diffusion steps (measured via cosine similarity)*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_KUfKvlX3VY/figures/003_Figure_2.jpg]]
*Figure 2: (b) Latency-accuracy tradeoff. Pareto front comparing the standard autoregressive baseline with our KV-cache optimized method, highlighting substantial latency reductions at equivalent accuracy levels*

FlashDLM 提出了一套免训练的推理加速框架，旨在解决扩散语言模型（DLM）在生成过程中因每步全序列前向计算导致的 O(L) 额外复杂度瓶颈，以及并行揭晓 token 时因因子化分布限制造成的语义不连贯问题。框架由两个正交且可叠加的模块构成：**FreeCache**（高效 KV 缓存）和 **Guided Diffusion**（自回归引导扩散），二者从计算量和去噪迭代次数两个维度协同降低端到端延迟。

### 核心瓶颈与因果机制

DLM 推理的核心瓶颈源于其生成范式与自回归（AR）模型的根本差异。如 Table 1 所示，AR 模型每步仅需处理长度为 l 的前缀，而 DLM 在每一步去噪中都必须对全序列长度 L 进行多头注意力（MHA）和前馈网络（FFN）计算，导致每个 Transformer 模块均产生 O(L) 倍的额外计算开销。这一结构性差异使得 DLM 在长上下文场景下的延迟和计算成本急剧膨胀。

此外，DLM 在并行揭晓多个掩码 token 时，依赖于掩码位置上的因子化分布假设，这限制了模型对 token 间联合依赖关系的建模能力，导致生成的 token 缺乏语义连贯性，尤其在激进减少去噪步数时质量下降显著（Figure 1a）。

### FlashDLM 的因果调节点

FlashDLM 通过两个关键洞察切入上述瓶颈：

1. **KV 投影的时间稳定性**：已完成去噪的“干净” token 的 Key 和 Value 投影在后续去噪步骤中具有高度时间稳定性，余弦相似度接近 1（Figure 2）。这意味着可以安全地缓存这些投影，避免重复计算。
2. **轻量 AR 模型的一致性信号**：一个小的预训练 AR 模型可以提供免训练的 token 一致性检查信号，用于判断扩散模型提议的 token 是否可靠，从而安全地并行揭晓多个 token，缓解因子化限制并减少总去噪步数。

### 整体 Pipeline 与模块关系

FlashDLM 的推理流水线由以下模块按序构成：

1. **初始前向传播与 KV 缓存建立**：对包含 prompt 的完整序列执行一次前向传播，计算并保存所有 token 的完整 KV 投影，作为后续缓存的初始状态。

2. **FreeCache：窗口化重计算与渐进式缓存冻结**：将生成序列划分为固定大小的块。对于当前正在去噪的块 $B_i$，仅对活动窗口（$B_i$ 及后续所有块）内的 token 重新计算 KV 投影；已完成去噪的前序块的 KV 投影被冻结并直接复用。随着生成推进，活动窗口动态收缩，计算量逐步降低。

3. **扩散草稿生成**：扩散模型 $f_\theta$ 对当前序列 $\mathbf{x}$ 中所有掩码位置产生 logits $z_t = f_\theta(\mathbf{x}_t)$，通过策略 $\pi$（如 Top-K Margin）从 $\mathrm{Softmax}(z_t[i])$ 中选择一批候选 token 作为草稿 $t^{\mathrm{DLM}}$。

4. **Guided Diffusion：AR 引导一致性检查**：将扩散草稿 $t^{\mathrm{DLM}}$ 送入轻量 AR 模型 $g_\phi$，获取其 logits $\mathrm{logits}^{\mathrm{AR}} = \mathrm{Softmax}(g_{\phi}(t^{\mathrm{DLM}}))$。通过匹配规则 $\mathcal{M}$ 确定 DLM 提议与 AR 预测一致的最长前缀长度 $k = \mathcal{M}(t^{\mathrm{DLM}}, \mathrm{logits}^{\mathrm{AR}})$，仅揭晓这 $k$ 个 token。与投机解码不同，Guided Diffusion **不需要** AR 模型进行 token 级校正，仅使用一致性信号。

5. **迭代去噪**：揭晓的 token 被填入序列，掩码位置集合 $M_t$ 更新，进入下一轮去噪，直至所有位置完成生成。

### 输入输出流

- **输入**：带有 prompt 的完整序列，其中生成部分初始化为全掩码状态。
- **输出**：完整去噪后的文本序列。
- **中间状态**：FreeCache 维护冻结的 KV 投影缓存和动态收缩的活动窗口；Guided Diffusion 维护扩散模型的草稿 token 和 AR 模型的一致性检查结果。

该框架的两个模块可独立或联合使用。FreeCache 单独使用即可在 Dream-7B-Instruct 上实现 4.42× 加速（准确率仅下降 2.28 个百分点，Table 2）；叠加 Guided Diffusion 后，在 PiQA 上可实现 34.1× 的端到端加速，且准确率略有提升（Table 3）。



### 问题形式化

扩散语言模型（DLM）在每一步去噪时，需要对全序列长度 $L$ 的所有掩码位置进行前向计算。设第 $t$ 步的掩码位置集合为：

$$M_t = \{ i : x_t[i] = [\mathrm{MASK}] \}$$

模型对掩码位置产生对数几率：

$$z_t = f_\theta(\mathbf{x}_t) \quad \mathrm{for} \ i \in M_t$$

随后通过策略 $\pi$ 选择一批位置 $U_t$ 并揭晓其 token：

$$\mathbf{x}_{t-1}[i] = \pi(\mathrm{Softmax}(z_t[i])), \quad i \in U_t$$

这一过程的核心瓶颈在于：每一步都需要对完整序列重新计算注意力中的键值（KV）投影，导致相比自回归模型 $O(L)$ 倍的额外计算开销（Table 1）。同时，并行揭晓多个 token 时，因子化分布假设限制了 token 间的联合依赖建模，导致语义连贯性下降。

### FreeCache：渐进式 KV 缓存冻结

FreeCache 的核心洞察是：已完成去噪的 token 的 KV 投影在后续步骤中具有高度时间稳定性。Figure 2 的热图表明，干净 token 的 K 和 V 投影在后续去噪步中的余弦相似度接近 1，变化极小。

基于此，FreeCache 采用**缩减窗口缓存策略**：

1. **初始前向传播**：对整个序列计算并保存完整的 KV 投影。
2. **固定块划分**：将生成序列划分为固定大小的块 $\{B_1, B_2, \ldots\}$。
3. **窗口化重计算**：当前活动窗口定义为当前块 $B_i$ 及其后续所有块，仅对该窗口内的 token 重新计算 KV 投影。
4. **渐进式冻结**：当块 $B_i$ 完成去噪后，冻结其 KV 投影，活动窗口随即缩小至 $B_{i+1}$ 及后续块。

这一策略将每次去噪步的计算量从全序列 $L$ 逐步缩减至仅活动窗口大小，在 Dream-7B-Instruct 上实现 4.42 倍加速，准确率仅下降 2.28 个百分点（Table 2）。

### Guided Diffusion：自回归引导的并行揭晓

Guided Diffusion 解决并行揭晓导致的语义不连贯问题。其关键设计是引入一个轻量级、冻结的自回归模型作为“引导者”，仅提供一致性信号而非 token 级校正——这与投机解码（Speculative Decoding）有本质区别。

流程如下（Figure 3）：

1. **扩散草稿生成**：扩散模型对所有掩码位置产生提议 token：
   $$t^{\mathrm{DLM}} = \pi(\mathrm{Softmax}(f_{\theta}(x)))$$

2. **AR 一致性检查**：将提议 token 输入自回归模型，计算其 logits：
   $$\mathrm{logits}^{\mathrm{AR}} = \mathrm{Softmax}(g_{\phi}(t^{\mathrm{DLM}}))$$

3. **安全揭晓**：通过匹配规则 $\mathcal{M}$ 确定最长一致前缀长度 $k$：
   $$k = \mathcal{M}(t^{\mathrm{DLM}}, \mathrm{logits}^{\mathrm{AR}})$$
   仅揭晓前 $k$ 个与 AR 模型预测一致的 token，其余位置保持掩码进入下一步去噪。

匹配策略支持 Top-1、Top-2、Top-5 等变体，其中 Top-5 匹配通常获得最佳的速度-准确率权衡（Table 7）。此外，附录 C.4 引入随机引导揭晓条件：

$$\max(\log_{\text{diffusion}}) > \tau \times \max(\log_a)$$

即当扩散模型的最大 logit 超过 AR 模型最大 logit 的 $\tau$ 倍时，该 token 被揭晓。

### 两模块的协同

FreeCache 和 Guided Diffusion 互补且可叠加：FreeCache 减少每步的计算量，Guided Diffusion 减少总去噪步数。在 Dream-7B-Instruct 上，两者联合在 PiQA 实现 34.1 倍加速（0.43s vs 14.62s），准确率反而提升 0.15 个百分点（Table 3）。较小的引导模型（如 Qwen2.5-1.5B-Instruct）即可提供足够信号，且加速比更高，因为其前向开销更低。



## 实验与关键发现

### 核心结果概述

FlashDLM 在多个基准上验证了 FreeCache 与引导扩散的组合加速效果。以 **Dream-7B-Instruct**（Ye et al., 2025）为主扩散模型、**Qwen2.5-1.5B-Instruct** 为引导者的配置下，端到端延迟大幅降低，同时准确率几乎无损甚至略有提升：

- **GSM8K (8-shot)**：准确率从基线 79.68% 提升至 80.30%，延迟从 48.05s 降至 2.70s，加速 **17.80×**（Table 3）。
- **MMLU-PRO**：准确率从 46.92% 微降至 46.64%（−0.28 pp），延迟从 29.33s 降至 2.35s，加速 **12.48×**（Table 3）。
- **PiQA**：准确率从 83.58% 升至 83.73%，延迟从 14.62s 降至 0.43s，加速 **34.10×**（Table 3）。
- **HellaSwag (5-shot)**：准确率从 73.30% 升至 76.63%，延迟从 21.99s 降至 2.46s，加速 **8.94×**（Table 8）。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_KUfKvlX3VY/figures/008_Table_3.jpg]]
*Table 3: Outstanding acceleration achieved by the proposed methods with negligible accuracy drop on Dream-7B-Instruct Ye et al. (2025). The latency value represents the end-to-end problem solving time per problem*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_KUfKvlX3VY/figures/012_Table_8.jpg]]
*Table 8: HellaSwag accuracy, latency, and speedup relative to the Dream-v0-Instruct-7B Baseline*

单独使用 FreeCache（无 AR 引导）时，Dream-7B-Instruct 在 GSM8K 上取得 **4.42×** 加速（48.05s → 10.87s），准确率仅下降 2.28 个百分点（79.68% → 77.40%）；LLaDA-8B-Instruct 上加速 **6.32×**（Table 2）。这一结果表明 KV 缓存策略本身已能显著降低计算开销，而 AR 引导的加入进一步将加速比推至 17× 以上。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_KUfKvlX3VY/figures/006_Table_2.jpg]]
*Table 2: Latency and accuracy of the proposed FreeCache with different Diffusion Language Models. The proposed method achieves 4.42× and 6.32× speedup on Dream-7B-Instruct and LLaDA-8B-Instruct models*

### 消融分析

#### FreeCache 的块大小影响

Table 7 展示了 LLaDA-8B-Instruct 在不同块大小下的表现。块大小 64 时 FreeCache 加速 6.32×，准确率 77.18%；块大小 32 时加速比略低但准确率略高。块大小决定了活动窗口的粒度——较大的块减少了 KV 重计算频率，但可能引入更多近似误差。当前固定块大小策略尚未达到最优，动态调整策略是明确的改进方向。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_KUfKvlX3VY/figures/013_Table_7.jpg]]
*Table 7: GSM8K (8-shot) accuracy, latency, and speedup for LLaDA-8B-Instruct with block sizes 32 and 64 and guided diffusion with Qwen2.5-Instruct models. Speedups are relative to the corresponding LLaDA baseline latency. proposed guided unmasking scheme introduces minimal memory overhead compared to the combined memory consumption of the single auto-regressive and baseline diffusion models*

#### 引导模型的规模选择

Table 3 和 Table 7 对比了不同规模 AR 引导模型的效果。关键发现是：**小型 AR 模型已足够提供有效的引导信号**。Qwen2.5-1.5B-Instruct 作为引导者时，加速比最高（34.1× on PiQA），而使用 Qwen2.5-7B-Instruct 时加速比反而下降（因引导模型自身推理开销增大），准确率提升有限。这验证了引导扩散的核心设计原则——AR 模型仅提供一致性信号而非生成或校正 token，因此轻量模型即可胜任。

#### 匹配策略的影响

Table 7 对比了 Top-1、Top-2、Top-5 三种匹配策略。Top-5 匹配通常获得更好的速度-准确率权衡：更宽松的匹配条件允许更多 token 被并行揭晓，减少去噪步数，但过于宽松可能引入不一致 token。附录 C.4 还引入了随机引导揭晓条件：

$$\max(\log_{\text{diffusion}}) > \tau \times \max(\log_a)$$

当扩散模型的最大 logit 超过 AR 模型最大 logit 乘以阈值 $\tau$ 时，该 token 被揭晓，提供了额外的灵活性。

#### 引导扩散对小型 AR 模型的提升

Table 4 展示了一个重要现象：引导扩散不仅加速了扩散模型，还能**提升小型 AR 模型自身的有效准确率**。Qwen2.5-1.5B 在 GSM8K 上独立 AR 推理准确率仅 68.54%，但作为 Dream-7B-Instruct 的引导者参与引导扩散时，组合系统准确率达到 80.3%。这说明扩散模型的强生成能力通过引导机制反哺了小型模型。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_KUfKvlX3VY/figures/009_Table_4.jpg]]
*Table 4: Comprehensive performance comparison on the GSM8K dataset, showing both standard autoregressive (AR) and AR-guided results for various models*

### 内存开销

Table 5 和 Table 6 报告了引导扩散的 GPU 内存占用。以 Dream-7B-Instruct + Qwen2.5-1.5B 为例，总内存 18.7 GB（DLM 14.6 GB + Guide 4.1 GB）；若使用 Qwen2.5-7B 作为引导者，总内存升至 31.9 GB。LLaDA-8B-Instruct 配合 Qwen2.5-1.5B 总内存为 24.8 GB。内存开销主要来自同时加载两个模型，但小型引导模型（1.5B）的额外开销可控。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_KUfKvlX3VY/figures/010_Table_5.jpg]]
*Table 5: LLaDA-8B-Instruct Guided Diffusion Memory Usage (GB)*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_KUfKvlX3VY/figures/011_Table_6.jpg]]
*Table 6: Dream-Instruct-7B Guided Diffusion Memory Usage (GB)*

### 失败模式与局限性

1. **KV 稳定性假设的边界**：FreeCache 依赖 KV 投影在干净 token 上的时间稳定性（Figure 2 余弦相似度接近 1），但这一假设可能不适用于所有 DLM 架构或任务类型。当序列中存在长程依赖需要跨块更新时，冻结早期块的 KV 可能累积误差。

2. **引导模型的规模权衡**：引导模型过大（如 7B）会显著增加延迟和内存，抵消加速收益；过小则引导信号质量下降。当前实验仅在 1.5B 和 7B 两个规模上验证，最优规模的选择机制尚不明确。

3. **评估范围有限**：实验仅覆盖 Dream-7B-Instruct 和 LLaDA-8B-Instruct 两个扩散语言模型，以及有限的推理基准。方法在更大规模 DLM（数十亿参数以上）和更复杂任务（如多轮对话、代码生成）上的有效性仍需验证。

4. **固定块大小的次优性**：FreeCache 使用固定块大小划分序列，无法根据局部 KV 稳定性或扩散不确定性动态调整，可能在“过度保守”（块太小，重计算多）和“过度激进”（块太大，近似误差大）之间无法达到最优平衡。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_KUfKvlX3VY/figures/001_Table_1.jpg]]
*Table 1: Compute complexity of Transformer modules: AR decodes a prefix of length l per token vs. DLM processes full length L each denoising step*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_KUfKvlX3VY/figures/014_Table_9.jpg]]
*Table 9: LLaDA-8B-Instruct Guided Diffusion Memory Usage (GB)*



## 定位与知识库关联

### 与基线方法的因果差异

FlashDLM 的核心加速逻辑建立在两个可验证的因果发现之上：KV 投影的时间稳定性与因子化分布导致的 token 间不连贯性。

**KV 投影稳定性与 FreeCache。** 传统扩散语言模型（DLM）在每一步去噪时对整个序列重新计算注意力键值（KV）投影，导致与自回归模型相比 $O(L)$ 倍的额外计算开销（Table 1）。FlashDLM 揭示了一个关键现象：已完成去噪的 token 的 K 和 V 投影在后续步骤中余弦相似度接近 1（Figure 2），即随时间高度稳定。基于此，FreeCache 采用**缩减窗口缓存策略**：将生成序列划分为固定大小的块，对已完成的块冻结其 KV 投影，仅对当前活动窗口内的 token 重新计算。这与基线方法 **Dream-7B-Instruct**（Ye et al., 2025）和 **LLaDA-8B-Instruct**（Nie et al., 2025）的全序列重计算形成根本性差异——FreeCache 将计算复杂度从 $O(L)$ 降低为与活动窗口大小成正比。

**因子化分布限制与引导扩散。** DLM 并行揭晓 token 时依赖掩码位置上的因子化分布，这限制了建模联合依赖的能力，导致 token 间语义不连贯（Section 3.1.2）。基线方法采用启发式置信度策略（如 Top-K Margin、熵）选择揭晓 token，在减少去噪步数时准确率显著下降（Figure 1a）。FlashDLM 的引导扩散方案彻底改变了这一范式：使用轻量级预训练自回归模型（如 **Qwen2.5-1.5B-Instruct**）对扩散模型提议的 token 进行一致性检查，仅揭晓与 AR 模型预测一致的 token。与投机解码不同，引导扩散**不需要 token 级校正**——AR 模型仅提供一致性信号，而非生成或修正 token（Section 3.2.2）。这从根本上缓解了并行揭晓时的因子化限制。

### 适用边界与限制条件

**FreeCache 的适用范围。** FreeCache 依赖于 KV 投影的时间稳定性假设，其有效性已在 Dream-7B-Instruct 和 LLaDA-8B-Instruct 上验证（Table 2），但该假设是否适用于所有 DLM 架构或所有任务类型尚需进一步验证。当前采用的固定块大小策略（如 32 或 64）可能未达到最优，动态调整策略有待探索。

**引导扩散的权衡。** 引导扩散不能保证无损加速——较大的引导模型（如 **Qwen2.5-7B-Instruct**）可提供更强的引导信号，但会增加内存和延迟开销（Table 6：总内存从 18.7 GB 增至 31.9 GB）；太小的引导模型可能降低准确率。在 GSM8K 上，Qwen2.5-1.5B-Instruct 引导可将准确率从 68.54% 提升至 80.3%（Table 4），表明小模型引导信号已足够有效，但这一结论的泛化性有待更多任务验证。

**评估范围限制。** 当前评估仅限于两个 DLM 模型（Dream-7B-Instruct 和 LLaDA-8B-Instruct）和有限的任务集（GSM8K、MMLU-PRO、PiQA、ARC、HellaSwag、GPQA），在更大规模模型（数十亿参数以上）和更复杂推理任务上的表现未知。

### 与相关方法的关系

FlashDLM 的引导扩散与投机解码形成范式对比：投机解码使用小 AR 模型进行自回归起草，再由大模型校正；而引导扩散**反转了这一范式**——由大扩散模型高效起草，小 AR 模型仅提供一致性信号（Section 4）。这使得引导扩散的起草效率由扩散模型而非小模型决定，同时避免了投机解码中 token 级校正的复杂性和潜在错误传播。

### 开放问题

1. 如何为 FreeCache 设计自适应块大小策略，基于局部 KV 稳定性或扩散不确定性动态调整，以进一步优化速度-准确率权衡？
2. 所提方法能否推广到更大规模的 DLM（例如数十亿参数级别），KV 投影的稳定性假设在更大模型中是否仍然成立？
3. 是否有其他免训练的引导策略可以使用，例如基于扩散模型自身的置信度或集成多个轻量级引导者？
4. 引导扩散与投机解码的结合是否有增益——两者分别从起草效率和校正机制两个维度加速，是否存在互补性？
5. 在高吞吐量生产环境中，引导扩散的 GPU 内存调度（DLM 模型与引导模型共存）如何优化，以最大化吞吐量而非单样本延迟？



## 原文 PDF

![[paperPDFs/ICLR_2026/FlashDLM_Accelerating_Diffusion_Language_Model_Inference_via_Efficient_KV_Caching_and_Guided_Diffusion.pdf]]
