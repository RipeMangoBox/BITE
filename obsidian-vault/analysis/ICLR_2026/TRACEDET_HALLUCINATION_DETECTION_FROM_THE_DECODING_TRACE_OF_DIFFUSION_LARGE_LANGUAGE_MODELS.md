---
title: "TRACEDET: HALLUCINATION DETECTION FROM THE DECODING TRACE OF DIFFUSION LARGE LANGUAGE MODELS"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/TRACEDET_HALLUCINATION_DETECTION_FROM_THE_DECODING_TRACE_OF_DIFFUSION_LARGE_LANGUAGE_MODELS.pdf
project_link: null
code_link: https://github.com/chang-sx/TraceDet
openreview_forum_id: 4puxTouUSV
aliases:
- TRACEDET
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "信息瓶颈原理驱动的子轨迹提取，自动选择对幻觉最具有判别力的去噪中间步骤。"
primary_logic: "将扩散生成过程建模为动作轨迹，利用中间去噪步骤的熵信号，通过信息瓶颈找出对幻觉最具有判别力的子序列，用于可靠检测。"
claims:
- "TraceDet 将去噪过程建模为动作轨迹，并通过信息瓶颈原理自动发现最具信息量的子轨迹。"
- "在 LLaDA-8B-Instruct 和 Dream-7B-Instruct 上，TraceDet 平均 AUROC 比基线提高 15.2%，并且在 F1 和 TPR@FPR=0.1 指标上也全面领先。"
- "信息瓶颈（IB）原理使 TraceDet 能够从完整动作轨迹中发现最具有判别力的子序列，去除掩码或仅使用平均熵会导致性能显著下降。"
- "TraceDet 通过直接利用去噪过程自然暴露的步级熵信号，消除了多采样带来的计算开销，推理速度远快于基于语义熵等需要多次采样的方法。"
---

# TRACEDET: HALLUCINATION DETECTION FROM THE DECODING TRACE OF DIFFUSION LARGE LANGUAGE MODELS

> [!tip] 核心洞察
> 将扩散生成过程建模为动作轨迹，利用中间去噪步骤的熵信号，通过信息瓶颈找出对幻觉最具有判别力的子序列，用于可靠检测。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | TraceDet：基于扩散大语言模型解码轨迹的幻觉检测 |
| 英文题名 | TRACEDET: HALLUCINATION DETECTION FROM THE DECODING TRACE OF DIFFUSION LARGE LANGUAGE MODELS |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=4puxTouUSV) · [GitHub](https://github.com/chang-sx/TraceDet) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | TraceDet |
| Dataset | TriviaQA-128, HotpotQA-128, CommonsenseQA-128, LLaDA-8B-Instruct (3数据集平均，128/64步) |

> [!tip] 效果简介
> - TriviaQA-128 上，AUROC (%) 为 73.9，对比 57.1 (TSV)，变化 +16.8。
> - HotpotQA-128 上，AUROC (%) 为 66.1，对比 57.6 (TSV)，变化 +8.5。
> - CommonsenseQA-128 上，AUROC (%) 为 77.2，对比 50.5 (TSV)，变化 +26.7。

## 概要

扩散大语言模型（Diffusion LLM, D-LLM）通过迭代去噪生成文本，其逐步解码过程天然暴露了丰富的中间状态信号。然而，现有幻觉检测方法几乎全部围绕自回归模型设计，依赖单步生成信号或多次采样来估计不确定性，无法捕捉 D-LLM 在去噪过程中逐步涌现的幻觉模式。这构成了当前幻觉检测研究的一个关键盲区。

**核心瓶颈**：D-LLM 的去噪轨迹包含大量冗余步骤，并非所有中间状态都对幻觉判别具有同等价值。如何从完整的 T 步去噪序列中自动定位最具信息量的子轨迹，是高效检测的关键。

**TraceDet 的核心思路**：将 D-LLM 的去噪过程建模为动作轨迹（action trace），每一步动作定义为模型对当前中间状态的 token 级预测熵。在此基础上，引入信息瓶颈（Information Bottleneck, IB）原理，通过可微的子实例提取器自动选择对幻觉最具有判别力的去噪子序列，并仅在该子轨迹上进行分类。整个框架无需多次采样，直接复用去噪过程内部已有的步级熵信号。

**主要结果**：在 LLaDA-8B-Instruct 和 Dream-7B-Instruct 两个扩散大语言模型上，TraceDet 在 TriviaQA、HotpotQA 和 CommonsenseQA 三个短答案 QA 基准上，AUROC 平均比最强基线（TSV, Park et al., 2025）提升 15.2 个百分点。消融实验表明，移除掩码机制或仅使用平均熵均会导致性能显著下降，验证了信息瓶颈原理驱动的子轨迹选择是性能提升的核心来源。此外，TraceDet 仅需一次去噪生成即可完成检测，推理速度远快于 Semantic Entropy 等需要多次采样的方法。

**方法定位**：TraceDet 属于**基于扩散生成过程信号**的幻觉检测方法，区别于传统的输出型（如 Perplexity、Semantic Entropy）和隐空间型（如 CCS、TSV）基线。其核心创新在于将信息瓶颈原理引入去噪轨迹的时序选择，为扩散语言模型的幻觉检测开辟了新的技术路径。



扩散大语言模型（Diffusion LLMs, D-LLMs）通过迭代去噪生成文本，在推理效率与可控性上展现出独特优势。然而，与自回归模型类似，D-LLMs 同样面临幻觉（hallucination）问题——模型生成的内容与事实不符。在 D-LLM 的去噪过程中，幻觉并非仅在最终输出中显现，而是随着去噪步骤的推进逐步暴露。TraceDet 将这一现象归纳为三类典型模式（Figure 1）：**交错幻觉**（模型在真实与幻觉内容间反复摇摆）、**不一致猜测**（多个矛盾的关键词导致幻觉）和**持续错误**（模型在整个去噪过程中坚持错误答案）。这些动态模式表明，去噪轨迹本身蕴含着丰富的幻觉信号。

现有幻觉检测方法大多针对自回归模型设计，可归纳为三类。**输出型方法**直接利用最终响应的统计量，如困惑度（Perplexity, Ren et al., 2022）、长度归一化熵（LN-Entropy, Malinin & Gales, 2020）和语义熵（Semantic Entropy, Kuhn et al., 2023），后者需要多次采样（如 $S \geq 10$ 次生成）来估计语义空间的不确定性。**隐空间方法**则挖掘模型内部表示，如基于协方差特征值的 EigenScore（Chen et al., 2024a）、对比一致搜索 CCS（Burns et al., 2022）和真实性分离向量 TSV（Park et al., 2025）。这些方法的共同瓶颈在于：它们仅依赖自回归模型的单步前向信号或最终输出，无法捕捉 D-LLM 在迭代去噪过程中逐步涌现的幻觉模式。

更关键的是，D-LLM 的去噪过程天然暴露了步级 token 熵信号——每一步去噪后，模型对每个位置的 token 预测都携带着不确定性信息。这些中间步骤的熵动态构成了一个信息丰富的“动作轨迹”，但并非所有步骤都对幻觉检测同等重要。直接使用完整轨迹或简单平均会引入噪声，削弱判别力。因此，核心挑战转化为：**如何从高维去噪轨迹中自动筛选出对幻觉最具判别力的子序列**，从而在不增加额外采样开销的前提下实现可靠检测。

TraceDet 的动机正是填补这一空白。它将 D-LLM 的去噪过程建模为动作轨迹（action trace），并引入信息瓶颈（Information Bottleneck, IB）原理来驱动子轨迹的自动提取——在保留与幻觉标签互信息的同时，最大化压缩输入轨迹，从而定位最具信息量的去噪步骤。这一设计使幻觉检测从“被动观察最终输出”转变为“主动追踪生成过程中的不确定性动态”，为 D-LLM 的幻觉检测提供了全新的视角。



## 核心方法与创新机理

### 瓶颈突破：从单步输出信号到去噪过程轨迹

现有幻觉检测方法本质上依赖**自回归模型的单步生成信号**——无论是基于最终输出文本的困惑度（Perplexity）、长度归一化熵（LN-Entropy），还是基于隐藏状态的线性探针（CCS、TSV），抑或需要多次采样的语义熵（Semantic Entropy），它们都仅从模型的一次前向传播或多次独立生成的最终结果中提取特征。这一范式在扩散大语言模型（D-LLM）上面临根本性局限：D-LLM 通过迭代去噪逐步生成响应，幻觉往往在中间步骤中经历**振荡、矛盾猜测或持续强化**的动态过程（Figure 1），这些逐步暴露的判别信号在仅观察最终输出时完全不可见。

TraceDet 的核心突破在于**将检测的输入信号从最终输出前移至整个去噪过程的动作轨迹**。具体而言，它将 D-LLM 的 T 步去噪过程建模为马尔可夫决策过程（MDP），每一步的动作定义为模型在当前中间状态上对最终清洗响应的预测，并提取每步的 token 级最大熵矩阵 $A \in \mathbb{R}^{T \times B \times D}$ 作为动作轨迹。这一信号转换使得检测器能够直接观察到幻觉在去噪过程中的演化模式，而非仅凭最终结果进行推断。

### 机制创新：信息瓶颈驱动的子轨迹自动发现

仅有完整动作轨迹并不足以实现高效检测——并非所有去噪步骤都携带等量的幻觉判别信息。TraceDet 的第二个关键创新是引入**信息瓶颈（Information Bottleneck, IB）原理**，自动从完整轨迹中发现对幻觉最具有判别力的子序列。

这一设计将检测问题从简单的分类任务重新表述为信息论优化问题：

$$\min_{f: A_{sub} \mapsto Y} -I(Y; A_{sub}) + \beta I(A; A_{sub})$$

其中第一项要求子轨迹 $A_{sub}$ 保留与幻觉标签 $Y$ 的最大互信息（充分性），第二项约束 $A_{sub}$ 与完整轨迹 $A$ 的互信息最小化（压缩性），$\beta$ 控制压缩强度。通过这一目标，模型被强制学习一个**最小充分子轨迹**——仅保留对检测真正必要的去噪步骤，丢弃冗余或噪声步骤。

消融实验（Table 3）严格验证了这一机制的贡献：移除掩码机制（TraceDet w/o Masking）导致 Dream-7B 上 AUROC 平均下降约 2.4 个百分点；仅使用平均熵（Ave Entropy）的分类效果极弱（LLaDA 平均 62.8，Dream 平均 65.3），远低于完整 TraceDet，证明时域动态信息是不可替代的。

### 架构创新：端到端可微的子实例提取-预测框架

为实现 IB 目标，TraceDet 设计了两个可微模块的联合训练架构（Figure 2）：

- **子实例提取器 $g_\theta$**：通过时序编码器（正弦位置编码 + 轻量级 Transformer）将动作轨迹 $A$ 编码为上下文嵌入，再通过交叉注意力与线性层生成概率掩码 $\hat{M} \in (0,1)^{T \times B}$，并使用 Gumbel-Softmax 技巧采样出二值掩码 $M$，获得 $A_{sub} = M \odot A$。这一设计使离散的子轨迹选择过程完全可微。

- **子实例预测器 $f_\phi$**：对掩码后的子轨迹进行时序聚合，通过两层 MLP 直接输出每个样本的幻觉概率。

训练目标组合了分类损失与基于伯努利 KL 散度的正则项：

$$\mathcal{L} = \mathcal{L}_{cls} + \beta \mathcal{L}_{ext}, \quad \mathcal{L}_{ext} = \sum_{i=0}^{T-1} \left[ p_{a_i} \log \frac{p_{a_i}}{\tau} + (1 - p_{a_i}) \log \frac{1 - p_{a_i}}{1 - \tau} \right]$$

其中 $\tau$ 控制每步被选中的先验概率（稀疏性约束），$\beta$ 平衡检测精度与压缩强度。这一联合训练范式使得子轨迹选择直接服务于检测目标，而非作为独立的前处理步骤。

### 效率创新：消除多采样计算开销

基于语义熵的方法（如 Kuhn et al., 2023）需要对同一输入进行 $S \geq 10$ 次独立生成以估计语义不确定性，导致推理时间线性膨胀。TraceDet 通过**直接复用去噪过程自然暴露的步级熵信号**，仅需一次去噪生成即可完成检测，无需任何额外采样。Table 4 显示，TraceDet 推理 100 个样本仅需 147.52 秒，而 Semantic Entropy 需要 801.35 秒——速度提升超过 5 倍，同时 AUROC 平均领先 15.2%。这一效率优势源于方法设计层面的根本差异：TraceDet 将去噪过程本身视为信息源，而非将生成视为黑箱。

### 创新边界与适用条件

需注意 TraceDet 的创新建立在两个前提之上：(1) 依赖去噪过程提供的步级 token 熵矩阵，对于不公开中间 logits 的闭源 D-LLM 无法直接应用；(2) 训练仍需少量标注数据（每数据集 200 条），尚未探索全无监督设定。这些限制划定了当前方法创新的适用边界，也为后续扩展指明了方向。



![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_4puxTouUSV/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of TRACEDET. During denoising, a diffusion LLM generates intermediate sequences along with token-level entropy traces, where highlighted words indicate the retained tokens after remasking (left). The sub-instance extractor $g _ { \theta }$ produces a temporal mask M to focus on informative steps, and the predictor $f _ { \phi }$ classifies whether the final response is hallucinated (right)

TraceDet 的核心思路是将扩散大语言模型（D-LLM）的去噪生成过程重新建模为**动作轨迹**，并从中自动发现对幻觉检测最具判别力的子序列。整个框架由四个紧密耦合的模块构成，形成一条从原始去噪信号到二分类决策的端到端流水线。

### 输入信号：从最终输出到动作轨迹

传统幻觉检测方法直接对最终响应文本或单步隐藏状态进行分类，而 TraceDet 将视角前移：它把 D-LLM 从纯噪声逐步去噪到最终响应的完整过程视为一个**马尔可夫决策过程**。具体而言，给定输入提示 $p_0$，模型在 $T$ 步反向去噪中依次产生中间响应 $r_T, r_{T-1}, \dots, r_0$，每一步都伴随一个 token 级的最大熵矩阵。TraceDet 将每一步的熵向量拼接为**动作轨迹** $A \in \mathbb{R}^{T \times B \times D}$，其中 $T$ 为去噪步数，$B$ 为序列长度，$D$ 为词表维度。这一轨迹完整记录了模型在去噪过程中对每个 token 预测的不确定性演化，是后续所有判别信号的唯一来源。

### 核心流水线：提取、选择、判别

TraceDet 的流水线包含四个关键步骤：

1. **熵序列提取**：在 D-LLM 的 $T$ 步去噪过程中，每一步计算 token 级最大熵，形成动作轨迹矩阵 $A$。这一步无需额外采样，直接复用去噪过程自然暴露的步级熵信号。

2. **时序编码器**：将 $A$ 与正弦位置编码结合，通过一个轻量级 Transformer 编码器转换为上下文感知的嵌入表示 $emb$。该编码器的作用是捕获去噪步之间的时序依赖关系，为后续的子轨迹选择提供结构化特征。

3. **子实例提取器 $g_\theta$**：这是 TraceDet 的核心创新模块。它通过交叉注意力机制与线性层生成概率掩码 $\hat{M} \in (0,1)^{T \times B}$，再利用 Gumbel-Softmax 技巧采样出二值掩码 $M \in \{0,1\}^{T \times B}$。将掩码逐元素作用于 $A$，得到子轨迹 $A_{sub} = M \odot A$。这一过程由**信息瓶颈原理**驱动——训练目标迫使 $g_\theta$ 选择与幻觉标签 $Y$ 互信息最大、同时与完整轨迹 $A$ 互信息最小的子序列，即“最小充分子轨迹”。

4. **子实例预测器 $f_\phi$**：对 $A_{sub}$ 进行时序聚合后，通过两层 MLP 直接输出每个样本的幻觉概率。$f_\phi$ 与 $g_\theta$ 联合训练，确保选出的子轨迹对分类任务具有高判别力。

### 训练目标：信息瓶颈驱动的端到端学习

TraceDet 的总损失函数为：

$$\mathcal{L} = \mathcal{L}_{cls} + \beta \mathcal{L}_{ext}$$

其中 $\mathcal{L}_{cls}$ 是标准的二分类交叉熵损失，$\mathcal{L}_{ext}$ 是基于伯努利 KL 散度的可微正则项：

$$\mathcal{L}_{ext} = \sum_{i=0}^{T-1} \left[ p_{a_i} \log \frac{p_{a_i}}{\tau} + (1 - p_{a_i}) \log \frac{1 - p_{a_i}}{1 - \tau} \right]$$

该正则项约束每步被选中的概率 $p_{a_i}$ 向先验稀疏率 $\tau$ 靠拢，$\beta$ 控制压缩强度。整个框架端到端训练，$g_\theta$ 和 $f_\phi$ 在信息瓶颈目标的引导下协同优化：提取器学会聚焦于对幻觉最具判别力的去噪中间步骤，预测器则在这些精选步骤上做出可靠判断。

### 关键设计决策与证据

- **子轨迹选择的有效性**：消融实验表明，移除掩码机制（TraceDet w/o Masking）导致 AUROC 在 Dream-7B 上平均下降约 2.4 个百分点；仅使用平均熵（Ave Entropy）的分类效果远低于完整 TraceDet（LLaDA 平均 62.8 vs 72.0），验证了时域动态信息和信息瓶颈驱动的子轨迹选择是性能增益的核心来源。
- **单次采样效率**：TraceDet 直接复用去噪过程的内部熵信号，无需多次生成。在 100 样本推理耗时对比中，TraceDet 仅需 147.52 秒，远低于 Semantic Entropy 的 801.35 秒（需 $S \geq 10$ 次采样）。
- **超参数鲁棒性**：掩码比率 $\tau$ 在 0.2–0.3、正则化权重 $\beta$ 在 0.8–1.6 范围内性能最优，超出该范围仍保持较高 AUROC；在生成长度 16–128、步长 1–8 的广泛设置下性能稳定。

### 局限与边界

TraceDet 目前仅实现幻觉检测，缺乏基于检测信号的自动纠正机制。其依赖去噪过程提供的步级 token 熵矩阵，对于不公开中间 logits 的闭源 D-LLM 无法直接应用。所有实验基于 7–8B 规模的开源模型和短答案 QA 任务，在更长自由文本生成和多轮对话场景的泛化性尚未验证。训练仍需少量标注数据（每数据集 200 条），未探索全无监督设定。



### 问题形式化：从最终响应分类到动作轨迹检测

扩散大语言模型（D-LLM）通过逐步去噪生成最终响应 $r_0$，其生成过程可形式化为逆向去噪链：

$$r_0 \sim \prod_{t=T-1}^{0} P_{\theta}(r_t \mid r_{t+1}, p_0)$$

其中 $p_0$ 为输入提示，$T$ 为总去噪步数。传统幻觉检测方法直接对最终响应 $r_0$ 进行二元分类：

$$\min_{h \in \mathcal{H}} \mathcal{L}(Y, h(r_0))$$

这一范式忽略了去噪过程中蕴含的丰富中间信号。TraceDet 的核心洞察在于：D-LLM 的去噪过程可被建模为**动作轨迹**（action trace），其中每一步的 token 级预测熵自然暴露了模型的不确定性动态。因此，检测目标被重构为从完整动作轨迹 $A$ 中识别出对幻觉判别最具有信息量的子轨迹 $A_{sub}$，并在其上最小化分类损失：

$$\min_{f,g} \mathcal{L}(Y, f(A_{sub})), \quad \text{s.t.} \quad A_{sub} = g(A)$$

### 信息瓶颈驱动的最小子轨迹选择

上述目标的核心挑战在于：如何自动确定哪些去噪步骤对幻觉检测是充分且必要的。TraceDet 引入**信息瓶颈（Information Bottleneck, IB）原理**来解决这一问题，将子轨迹选择形式化为互信息的最优权衡：

$$\min_{f: A_{sub} \mapsto Y} -I(Y; A_{sub}) + \beta I(A; A_{sub})$$

其中：
- $I(Y; A_{sub})$ 表示子轨迹 $A_{sub}$ 与幻觉标签 $Y$ 之间的互信息，最大化该项（即最小化其负值）确保子轨迹保留足够的判别信息；
- $I(A; A_{sub})$ 表示完整轨迹 $A$ 与子轨迹 $A_{sub}$ 之间的互信息，最小化该项迫使子轨迹尽可能紧凑，剔除冗余步骤；
- $\beta$ 为权衡系数，控制压缩强度与判别力保留之间的平衡。

### 可微近似：从互信息到端到端损失

直接优化互信息目标在实践中不可行，TraceDet 通过两个关键近似将其转化为可端到端训练的损失函数。

**分类损失** $\mathcal{L}_{cls}$：采用标准交叉熵损失，衡量子轨迹预测器 $f_{\phi}$ 对幻觉标签的预测精度。

**提取正则化损失** $\mathcal{L}_{ext}$：将压缩项 $I(A; A_{sub})$ 松弛为伯努利 KL 散度。设 $p_{a_i}$ 为第 $i$ 个去噪步被选入子轨迹的概率，$\tau$ 为预设的目标选择比率（先验稀疏度），则：

$$\mathcal{L}_{ext} = \sum_{i=0}^{T-1} \left[ p_{a_i} \log \frac{p_{a_i}}{\tau} + (1 - p_{a_i}) \log \frac{1 - p_{a_i}}{1 - \tau} \right]$$

该正则项推动每步的选择概率向先验 $\tau$ 靠拢，从而实现可控的稀疏子轨迹提取。

**总训练损失**为两者的加权组合：

$$\mathcal{L} = \mathcal{L}_{cls} + \beta \mathcal{L}_{ext}$$

### 流水线模块与实现细节

TraceDet 的完整流水线由四个核心模块构成，各模块协同实现从原始熵矩阵到幻觉概率的端到端映射。

1. **熵序列提取**：在 D-LLM 的 $T$ 步去噪过程中，记录每步每个 token 位置的最大预测熵，形成动作轨迹矩阵 $A \in \mathbb{R}^{T \times B \times D}$，其中 $B$ 为序列长度，$D$ 为词汇表维度。

2. **时序编码器**：结合正弦位置编码与轻量级 Transformer 编码器，将 $A$ 转换为上下文感知的嵌入表示 $emb$，捕获跨步时序依赖。

3. **子实例提取器 $g_{\theta}$**：通过交叉注意力机制生成概率掩码 $\hat{M}$，其中每个元素的计算方式为：

   $$\hat{m}_{t,b} = \operatorname{Linear}(\operatorname{attn}(emb, A))$$

   随后使用 Gumbel-Softmax 技巧从 $\hat{M}$ 中采样出二值掩码 $M \in \{0,1\}^{T \times B}$，并通过逐元素乘法获得子轨迹：

   $$A_{sub} = M \odot A \in \mathbb{R}^{T \times B \times D}$$

4. **子实例预测器 $f_{\phi}$**：对 $A_{sub}$ 进行时序聚合后，通过两层 MLP 输出每个样本的幻觉概率，完成最终分类。



## 实验与关键发现

### 核心实验设置

TraceDet 在两个开源扩散大语言模型（D-LLM）上进行评估：**LLaDA-8B-Instruct** 和 **Dream-7B-Instruct**。实验覆盖三个短答案事实性 QA 基准：TriviaQA、HotpotQA 和 CommonsenseQA，每个数据集随机采样 2000 条样本，按 1700/100/200 划分为训练/验证/测试集。生成步长设为 128 和 64 两种配置，生成长度固定为 128 tokens。幻觉标签由 **Qwen3-8B** 作为自动裁判进行标注，并在 TriviaQA（90% 一致性）和 HotpotQA（84% 一致性）上与人类评估进行了交叉验证。所有对比方法使用相同的训练/验证/测试划分和随机种子，确保公平比较。

### 主结果：全面领先的幻觉检测性能

Table 1 报告了 TraceDet 与八类基线方法在 AUROC 指标上的全面对比。TraceDet 在两个 D-LLM 和三个数据集的所有配置下均取得最优或次优结果，具体表现为：

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_4puxTouUSV/figures/003_Table_1.jpg]]
*Table 1: AUROC(%) comparison of hallucination detection methods on two D-LLMs across three QA datasets with 128 and 64 generation step lengths. SS is the short for Single Sampling. The highest score is bolded and the second highest is underlined*

- **LLaDA-8B-Instruct 上**：TraceDet 在 128/64 步配置下平均 AUROC 达 72.0%，比最强基线 **TSV**（Park et al., 2025）的 59.0% 高出 13.0 个百分点。在 CommonsenseQA-128 上优势最为显著，TraceDet 达 77.2%，而 TSV 仅 50.5%（+26.7 个百分点）。
- **Dream-7B-Instruct 上**：TraceDet 平均 AUROC 达 80.8%，比 TSV 的 65.2% 高出 15.6 个百分点。在 TriviaQA-64 上达到 86.7% 的最高单点 AUROC。
- **整体平均**：TraceDet 相比各基线均值提升约 15.2% 的 AUROC。

Table 2 的 F1 分数进一步验证了 TraceDet 的鲁棒性：在所有数据集-模型组合中，TraceDet 均取得最高 F1，例如 CommonsenseQA-64 上达 90.2%。Table 6 的 TPR@FPR=0.1 指标显示，TraceDet 在严格控制误报率（FPR=0.1）的条件下仍保持极高召回率，在 6 个设置中的 5 个取得最优，表明其在实际部署中的可靠性。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_4puxTouUSV/figures/004_Table_2.jpg]]
*Table 2: F1 score (%) comparison between TraceDet and baseline methods. The highest score is bolded*

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_4puxTouUSV/figures/012_Table_6.jpg]]
*Table 6: TPR@FPR=0.1 (%) comparison between TraceDet and baseline methods. The highest score is bolded*

### 消融实验：信息瓶颈与掩码机制的关键作用

为隔离 TraceDet 各组件贡献，Table 3 报告了两项消融实验：

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_4puxTouUSV/figures/005_Table_3.jpg]]
*Table 3: AUROC(%) comparison between TraceDet and our proposed baselines (Ave Entropy, TraceDet w/o Masking). The highest score is bolded and the second highest is underlined*

1. **Ave Entropy（仅使用平均步级熵）**：将完整的时域熵序列压缩为单步平均熵后送入分类器。在 LLaDA-8B 上平均 AUROC 仅 62.8，Dream-7B 上仅 65.3，远低于完整 TraceDet。这证明去噪过程的**时域动态信息**（而非简单的平均熵水平）是幻觉检测的关键信号源。

2. **TraceDet w/o Masking（移除子实例掩码模块）**：保留时序编码器和预测器，但直接对全部 T 步轨迹进行分类，不进行子轨迹选择。在 Dream-7B 上平均 AUROC 下降约 2.4 个百分点，验证了信息瓶颈驱动的子轨迹选择机制的有效性——并非所有去噪步骤对幻觉检测同等重要，选择最有判别力的子序列能显著提升性能。

Figure 5 从熵分布角度进一步解释了掩码机制的作用：掩码机制有效降低了所选步级轨迹的最大熵均值与方差，同时保持了对幻觉/非幻觉样本的判别分离度，说明信息瓶颈原理成功压缩了冗余信息而保留了判别性信号。

### 推理效率：单次生成消除多采样开销

Table 4 对比了各方法在 100 个样本上的平均推理时间。TraceDet 仅需 147.52 秒，与 **CCS**（140.73 秒）和 **TSV**（160.31 秒）相当，但远快于需要多次采样的方法：**Semantic Entropy**（Kuhn et al., 2023）需 801.35 秒（约 5.4 倍），**Lexical Similarity**（Lin et al., 2023）需 528.28 秒。这是因为 TraceDet 直接复用 D-LLM 去噪过程中自然暴露的步级 token 熵信号，无需任何额外生成采样，从根本上消除了多采样带来的计算开销。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_4puxTouUSV/figures/006_Table_4.jpg]]
*Table 4: Average inference time of 100 samples for different methods*

训练效率方面，Table 7 显示 TraceDet 单轮训练仅需 2.25 秒，优于其他需要训练的基线方法，使其在资源受限场景下具有实用优势。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_4puxTouUSV/figures/013_Table_7.jpg]]
*Table 7: Comparison of average epoch training time across TraceDet and training-based baseline methods on TriviaQA using 1700 training samples*

### 参数鲁棒性分析

Figure 3 展示了 TraceDet 对生成长度和步长的敏感性。在生成长度从 16 到 128、步长从 1 到 8 的广泛设置下，AUROC 保持稳定，未出现剧烈波动，表明方法具有良好的参数鲁棒性，不依赖于特定的去噪步长配置。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_4puxTouUSV/figures/008_Figure_3.jpg]]
*Figure 3: (a) TraceDet performance of different generation lengths with step length fixed at 1. (b) TraceDet performance with different step lengths with generation length fixed at 128. All results are reported as AUROC using Dream-7B-Instruct*

Figure 4b 的 3D 敏感度曲面分析了信息瓶颈正则项的超参数影响。掩码比率 τ 在 0.2–0.3、正则化权重 β 在 0.8–1.6 范围内性能最优，超出该范围仍保持较高的 AUROC（75–85%），说明方法对超参数不敏感，降低了实际调参成本。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_4puxTouUSV/figures/010_Figure_4.jpg]]
*Figure 4: (a) TraceDet performance sensitivity to remasking strategies. (b) TraceDet performance sensitivity to $\mathcal { L } _ { e x t }$ parameters $\tau$ and $\beta$ on TriviaQA. All results are reported as AUROC using Dream-7B-Instruct

### 局限性与失败模式

尽管 TraceDet 在检测性能上表现突出，但存在以下明确局限：

1. **仅检测不纠正**：当前框架仅输出幻觉概率，缺乏基于检测信号的自动纠正或缓解策略，无法直接改善生成质量。
2. **依赖中间 logits 访问**：TraceDet 需要去噪过程提供的步级 token 熵矩阵，对于不公开中间 logits 的闭源 D-LLM 无法直接应用。
3. **任务与规模泛化未验证**：所有实验基于 7–8B 规模的开源 D-LLM，且任务局限于短答案 QA，在更长的自由文本生成和多轮对话场景下的有效性仍属未知。
4. **仍需标注数据**：训练需要少量标注样本（每数据集 200 条），尚未探索完全无监督的设定。

### 补充图表

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_4puxTouUSV/figures/011_Table_5.jpg]]
*Table 5: Hyperparameter search space for TRACEDET. Notation: † log-spaced; ‡ linearly spaced. ∗ only applies to LLaDA*



## 定位与知识库关联

### 1. 问题定位：扩散语言模型的幻觉检测空白

现有幻觉检测方法主要围绕自回归语言模型设计，其信号来源可归为三类：

- **输出型方法**：直接利用最终生成文本的统计量，如 **Perplexity**（Ren et al., 2022）、**LN-Entropy**（Malinin & Gales, 2020）、**Semantic Entropy**（Kuhn et al., 2023）和 **Lexical Similarity**（Lin et al., 2023）。其中 Semantic Entropy 和 Lexical Similarity 需要多次采样（通常 S≥10）来估计语义空间的不确定性，计算开销大。
- **隐空间方法**：利用模型内部隐藏状态进行检测，如 **EigenScore**（Chen et al., 2024a）基于协方差矩阵特征值、**CCS**（Burns et al., 2022）通过对比一致搜索、**TSV**（Park et al., 2025）学习真实性分离向量。
- **共同局限**：上述方法均依赖自回归模型的单步前向信号或多次采样 logits，无法捕捉扩散大语言模型在迭代去噪过程中逐步暴露的幻觉动态——这是本工作的核心瓶颈。

TraceDet 首次将检测信号源从“最终输出”转移到“生成过程本身”，填补了扩散语言模型幻觉检测的方法空白。

### 2. 方法谱系中的位置：从输出检测到过程检测

TraceDet 的方法学贡献在于将扩散去噪过程建模为**动作轨迹**，并通过**信息瓶颈原理**自动选择最具判别力的子序列。这一设计改变了四个关键设计槽位：

| 设计维度 | 基线方法 | TraceDet 方案 |
|----------|----------|---------------|
| 输入信号 | 最终输出文本、单步隐藏状态或多采样 logits | 去噪过程的步级 token 熵序列（动作轨迹 A） |
| 检测模型 | 线性探针/MLP 直接分类，或基于统计量阈值 | 子实例提取器 g_θ + 子实例预测器 f_φ 联合训练 |
| 训练目标 | 标准交叉熵或自监督对比损失 | 信息瓶颈损失 L = L_cls + β·L_ext，强制子轨迹稀疏且充分 |
| 采样需求 | 多次采样（Semantic Entropy 需 ≥10 次） | 仅需一次去噪生成，直接复用内部熵信号 |

在知识库定位上，TraceDet 属于**过程感知的幻觉检测**这一新兴方向，与以下工作形成互补或对比：

- **与 Semantic Entropy 等不确定性方法的区别**：Semantic Entropy 通过多次采样的答案分布熵来度量不确定性，本质仍是“输出空间”的统计；TraceDet 则利用“去噪时间轴”上的动态信号，单次生成即可获得判别信息。
- **与隐空间方法的区别**：EigenScore、TSV 等方法从最终隐藏状态提取特征，丢失了中间步骤的时序动态；TraceDet 显式建模了 T 步去噪的熵演化轨迹。
- **与可解释性工作的潜在关联**：TraceDet 发现的三种幻觉模式（交错幻觉、不一致猜测、持续错误）为理解扩散语言模型的生成机制提供了新的分析视角，但尚未与自回归模型的幻觉归因工作（如上下文冲突检测）建立直接联系。

### 3. 适用边界

TraceDet 的适用性受以下条件约束：

- **模型架构依赖**：方法依赖去噪过程提供的步级 token 熵矩阵，仅适用于公开中间 logits 的开源扩散语言模型。对于闭源 D-LLM 或仅提供最终输出的 API，无法直接应用。
- **任务范围验证**：当前实验限于短答案问答（TriviaQA、HotpotQA、CommonsenseQA），在长文本自由生成、多轮对话等场景的泛化性未经验证。
- **模型规模验证**：仅在 7–8B 规模的 LLaDA-8B-Instruct 和 Dream-7B-Instruct 上验证，更大规模模型上的表现尚不明确。
- **标注数据依赖**：训练需要少量标注数据（每数据集 200 条），未探索全无监督设定下的可行性。

### 4. 局限与开放问题

**当前局限**：

1. **仅有检测无纠正**：TraceDet 目前仅实现幻觉检测，缺乏基于检测信号的自动纠正或缓解策略，限制了其实用价值。
2. **模型架构耦合**：对中间 logits 的依赖使其无法泛化到闭源扩散模型或其他生成范式（如自回归模型）。
3. **任务覆盖窄**：未在长文本、多轮对话、代码生成等更复杂场景下验证。

**开放问题**：

1. **幻觉去噪动力学的内在机制**：观察到的三种模式（振荡、随机猜测、持续错误）背后的因果机制是什么？这与扩散模型的训练目标、噪声调度有何关联？
2. **从检测到纠正的闭环**：TraceDet 选出的高判别力子轨迹能否作为回溯信号，指导 D-LLM 在去噪过程中自我纠正？这需要设计检测-干预的联合框架。
3. **跨范式迁移**：信息瓶颈驱动的子轨迹选择原理能否扩展到自回归模型的多次采样过程，或推广到图像、视频等其他扩散生成模型的错误检测？
4. **长序列泛化**：在更长的序列和自由格式生成中，信息瓶颈原理是否依然能可靠地选出充分子轨迹？掩码机制是否需要适配长程依赖？
5. **差异化策略**：针对三种不同的幻觉模式，是否需要设计差异化的子轨迹选择策略以进一步提升检测精度？

### 5. 证据强度说明

- **核心主张有强证据支持**：TraceDet 在两种 D-LLM、三个数据集上的 AUROC 平均提升 15.2%，消融实验（Table 3）和推理效率对比（Table 4）均直接验证了信息瓶颈原理和掩码机制的有效性，置信度高。
- **泛化性需进一步验证**：当前实验仅覆盖短答案 QA 和 7–8B 模型，长文本、多轮对话、更大规模模型的结论属于合理推断，需后续工作证实。
- **内在机制分析为探索性**：三种幻觉模式的分类基于对熵轨迹的观察性分析，因果机制的确认需要更严格的受控实验。



## 原文 PDF

![[paperPDFs/ICLR_2026/TRACEDET_HALLUCINATION_DETECTION_FROM_THE_DECODING_TRACE_OF_DIFFUSION_LARGE_LANGUAGE_MODELS.pdf]]
