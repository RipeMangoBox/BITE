---
title: "Beyond Masks: Efficient, Flexible Diffusion Language Models via Deletion-Insertion Processes"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Beyond_Masks_Efficient_Flexible_Diffusion_Language_Models_via_Deletion_Insertion_Processes.pdf
project_link: null
code_link: null
aliases:
- DIDLMD
- BMEFDLMDIP
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "DID用连续时间删除过程和学习到的插入分数替代掩码扩散语言模型的掩码去掩码过程。"
primary_logic: "前向链独立删除token至空序列，反向链通过插入分数和Tau-leaping并行重建变长文本。"
claims:
- "删除插入范式消除了MASK和PAD token造成的Transformer冗余计算。"
- "DID原生支持变长序列并能更好匹配训练数据的长度分布。"
- "并行动态规划使插入分数训练目标可高效计算，同时带来训练和推理加速。"
---

# Beyond Masks: Efficient, Flexible Diffusion Language Models via Deletion-Insertion Processes

> [!tip] 核心洞察
> 通过将前向过程定义为独立标记删除，后向过程定义为基于学习到的插入分数的标记插入，DID模型能够原生支持变长序列，消除冗余计算，并实现内在的自校正机制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 超越掩码：基于删除-插入过程的高效灵活扩散语言模型 |
| 英文题名 | Beyond Masks: Efficient, Flexible Diffusion Language Models via Deletion-Insertion Processes |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=VbvXjs5f72) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Deletion-Insertion Diffusion language models (DID) |
| Dataset | WikiText, Lambada, OpenWebText (固定长度) |

> [!tip] 效果简介
> - WikiText 上，零样本困惑度（越低越好） 为 36.91，对比 38.27，变化 -1.36。
> - Lambada 上，零样本困惑度（越低越好） 为 48.00，对比 51.82，变化 -3.82。
> - OpenWebText (固定长度) 上，训练时间加速比（越高越好） 为 1.99×，对比 1.0×，变化 +0.99×。

## 概要

本文提出了一种新型扩散语言模型——**Deletion-Insertion Diffusion language models (DID)**，旨在解决现有掩码扩散语言模型（MDLM）中因大量非信息性`<MASK>`和`<PAD>`标记导致的计算效率低下问题。DID的核心创新在于将扩散过程从传统的掩码-去掩码范式彻底替换为删除-插入范式：前向过程逐步删除序列中的标记直至为空，后向过程从空序列开始逐步插入标记以重建完整序列。这一范式转换使得DID能够原生支持变长序列，消除冗余计算，并具备内在的自校正机制。实验结果表明，在固定长度设置下，DID实现了高达**1.99倍**的训练加速和**1.58倍**的推理加速；在变长设置下，加速比分别提升至**3.42倍**和**3.79倍**，同时生成质量显著优于现有基线模型。



### 2.1 掩码扩散语言模型的计算瓶颈

现有掩码扩散语言模型（MDLM）如RADD、SMDM等，其核心计算瓶颈源于必须反复处理固定长度的序列。在这些序列中，大量位置被非信息性的`<MASK>`标记（在扩散过程中）和`<PAD>`标记（在处理变长数据时）占据。这些标记虽然不携带语义信息，但模型仍需对其进行完整的Transformer前向计算，导致大量FLOPs被浪费。

### 2.2 现有方法的局限性

- **掩码扩散模型（MDLM）**：前向过程逐步将标记掩码为`<MASK>`状态，后向过程从全掩码序列开始逐步去掩码。处理变长数据时需填充`<PAD>`标记至固定长度，进一步加剧计算浪费。
- **插入式语言模型（ILM）**：虽然支持变长生成，但缺乏严格的扩散理论基础，训练目标不包含似然界，且生成质量有限。
- **Edit Flows**：引入了辅助编辑路径变量，增加了方差和工程开销。

### 2.3 核心洞察

DID的核心洞察在于：**通过将前向过程定义为独立标记删除，后向过程定义为基于学习到的插入分数的标记插入，DID模型能够原生支持变长序列，消除冗余计算，并实现内在的自校正机制。** 这一设计从根本上避免了`<MASK>`和`<PAD>`标记的产生，从而消除了MDLM中最主要的计算浪费来源。



## 核心方法与创新机理

DID的核心创新可概括为以下三点：

1. **范式转换**：将扩散过程从掩码-去掩码替换为删除-插入，彻底消除`<MASK>`和`<PAD>`标记。
2. **原生变长支持**：模型在变长序列空间上定义，无需填充操作，在变长设置下实现显著的效率提升。
3. **内在自校正机制**：由于插入操作动态调整标记位置，模型在生成过程中能够自动修正早期的不完美生成。




![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_VbvXjs5f72_Beyond_M/figures/001_Figure_1.jpg]]
*Figure 1: (a) MDLMs, sequences padded to length 10.*

DID的整体框架建立在连续时间离散扩散理论之上，由以下核心模块组成：

- **前向删除过程**：一个连续时间马尔可夫链（CTMC），以速率σ(t)独立删除每个标记，逐步缩短序列长度直至为空。
- **后向插入过程**：一个CTMC，其反向转移率由学习到的插入分数s̄_θ定义，通过Tau-leaping方法进行并行采样。
- **插入分数网络 (s̄_θ)**：一个Transformer网络，输入当前序列x_t和时间t，输出形状为|x_t| × |V|的插入分数。
- **并行动态规划算法**：高效计算训练目标中的子序列计数比率，将复杂度从O(m n² V)降低到O(m n)。



### 5.1 前向删除过程

前向过程是一个定义在状态空间∪_{d=0}^∞ V^d上的CTMC，每个标记独立地以速率σ(t)被删除。序列级转移概率具有闭式表达式：

$$p_{t|s}(\mathbf{x}_t|\mathbf{x}_s) = (1 - e^{-(\bar{\sigma}(t)-\bar{\sigma}(s))})^{|\mathbf{x}_s|-|\mathbf{x}_t|} e^{-(\bar{\sigma}(t)-\bar{\sigma}(s))|\mathbf{x}_t|} N(\mathbf{x}_t, \mathbf{x}_s)$$

其中N(x_t, x_s)表示x_t作为x_s的子序列的计数。前向速率矩阵为：

$$Q_t(\mathbf{y}, \mathbf{x}_t) = \sigma(t) N(\mathbf{x}_t, \mathbf{y})$$

### 5.2 后向插入过程与插入分数

后向过程的目标是学习前向过程的时间反转。为此，定义插入分数：

$$\bar{s}(\mathbf{x}_t, t)[i, v] = \frac{\mathbb{E}_{\mathbf{x}_0}\left[(1 - e^{-\bar{\sigma}(t)})^{|\mathbf{x}_0|} N(\mathrm{Ins}(\mathbf{x}_t, i, v), \mathbf{x}_0)\right]}{\mathbb{E}_{\mathbf{x}_0}\left[(1 - e^{-\bar{\sigma}(t)})^{|\mathbf{x}_0|} N(\mathbf{x}_t, \mathbf{x}_0)\right]}$$

该分数表示在位置i插入标记v的期望概率比。反向转移率可表示为插入分数的加权和：

$$\tilde{Q}_t(\mathbf{x}_t, \mathbf{y}) = \sum_{i \in I(\mathbf{x}_t, \mathbf{y})} \left( \frac{\sigma(t) e^{-\bar{\sigma}(t)}}{1 - e^{-\bar{\sigma}(t)}} \bar{s}(\mathbf{x}_t, t)[i, v(\mathbf{x}_t, \mathbf{y})] \right)$$

### 5.3 训练目标：DISE与DICE

DID的训练目标为**去噪插入分数熵（DISE）**，是DSE目标的变分上界：

$$\mathcal{L}_\theta^{\mathrm{DISE}}(\mathbf{x}_0) = \mathbb{E}_{t, \mathbf{x}_t} \left[ \frac{\sigma(t) e^{-\sigma(t)}}{1 - e^{-\sigma(t)}} \sum_{i,v} \left[ \bar{s}_\theta(\mathbf{x}_t, t)[i, v] - \frac{N(\mathrm{Ins}(\mathbf{x}_t, i, v), \mathbf{x}_0)}{N(\mathbf{x}_t, \mathbf{x}_0)} \log \bar{s}_\theta(\mathbf{x}_t, t)[i, v] + C \right] \right]$$

在固定长度设置下，DISE可简化为**去噪插入交叉熵（DICE）**：

$$\mathcal{L}_\theta^{\mathrm{DICE}}(\mathbf{x}_0) = \underset{t, x_t}{\mathbb{E}} \left\{ \frac{\sigma(t) e^{-\bar{\sigma}(t)}}{1 - e^{-\bar{\sigma}(t)}} \sum_{i,v} \frac{N(\mathrm{Ins}(\pmb{x}_t, i, v), \pmb{x}_0)}{N(\pmb{x}_t, \pmb{x}_0)} \bigg[ -\log \bar{s}_\theta(\pmb{x}_t)[i, v] + C \bigg] \right\}$$

### 5.4 并行动态规划算法

DISE目标中的子序列计数比率可通过并行动态规划高效计算。前缀DP递推式为：

$$N(\mathbf{x}_t[:i], \mathbf{x}_0[:j]) = N(\mathbf{x}_t[:i], \mathbf{x}_0[:j-1]) + \delta(\mathbf{x}_t[i-1], \mathbf{x}_0[j-1]) \cdot N(\mathbf{x}_t[:i-1], \mathbf{x}_0[:j-1])$$

结合后缀DP结果，可计算所有插入操作的计数：

$$N(\mathrm{Ins}(\mathbf{x}_t, i, v), \mathbf{x}_0) = \sum_{j=1}^m \left[ \delta(\mathbf{x}_0[j], v) \cdot N(\mathbf{x}_t[:i], \mathbf{x}_0[:j-1]) \cdot N(\mathbf{x}_t[i:], \mathbf{x}_0[j:]) \right]$$

该算法将复杂度从O(m n² V)降低到O(m n)，使DID的训练变得实用。



## 实验与关键发现


### 6.1 零样本语言建模性能

Table 1展示了DID在零样本语言建模困惑度上的表现。DID-F（FLOPs对齐版本）在7个数据集上均优于RADD基线：

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_VbvXjs5f72_Beyond_M/figures/003_Table_1.jpg]]
*Table 1: Table 1: Zero-shot language modeling perplexity. Results for diffusion models are perplexity upper bounds.*

| 数据集 | RADD (Small) | DID-F (Small) | 改进 |
|--------|-------------|---------------|------|
| WikiText | 38.27 | **36.91** | -1.36 |
| Lambada | 51.82 | **48.00** | -3.82 |
| Pubmed | 56.99 | **52.89** | -4.10 |
| AG News | 73.18 | **71.48** | -1.70 |
| LM1B | 72.99 | **72.04** | -0.95 |
| Arxiv | 85.95 | **78.38** | -7.57 |
| PTB | 108.79 | **111.60** | +2.81 |

### 6.2 固定长度设置下的效率提升

Table 2和Table 3展示了固定长度设置下的效率提升：

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_VbvXjs5f72_Beyond_M/figures/004_Table_2.jpg]]
*Table 2: Table 2: Generative perplexity (PPL, evaluated by GPT2 Large), unigram entropy, inference time (in seconds), speedup, and average generation length for fixed-length models under different total denoising steps.*

- **推理加速**：DID在16-512步去噪步数下实现1.30倍至1.58倍的推理加速。例如，在16步时，DID的生成困惑度为158.93，而RADD为284.78。
- **训练加速**：在大模型设置下，DID的训练时间为46.60秒/50步，RADD为92.90秒，加速比达**1.99倍**。

### 6.3 变长设置下的效率提升

Table 4和Table 5展示了变长设置下的显著效率提升：

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_VbvXjs5f72_Beyond_M/figures/006_Table_4.jpg]]
*Table 4: Table 4: Generative PPL, unigram entropy, inference time (in seconds), and average generation length for variable-length models under different denoising steps. *: as outliers significantly affect PPL, only samples with PPL \< 300 are counted, †: speedup over RADD.*

- **推理加速**：DID在256步时实现**3.79倍**的推理加速。
- **训练加速**：在大模型设置下，DID的训练时间为19.83秒/50步，RADD为67.75秒，加速比达**3.42倍**。
- **生成质量**：DID在64步时的生成困惑度为22.78，远优于RADD的81.92和ILM的161.80。

### 6.4 长度建模能力

Figure 2展示了不同去噪步数下生成长度的累积分布函数（CDF）。DID的生成长度分布与训练数据高度一致，而RADD和ILM则存在显著偏差，证明了DID优越的长度建模能力。

### 6.5 消融研究

- **序列级归一化**（Table 13）：使用DICE目标（含序列级归一化）训练的DID-F在零样本困惑度上优于未使用归一化的版本。例如，WikiText上DID-F为36.91，而DID-F w/o SeqNorm为38.55。
- **DP算法开销**（Table 8, Table 9）：并行动态规划算法在训练中仅占很小一部分时间开销：固定长度下为7.2%-17.0%，变长下为10.1%-27.6%。

### 6.6 可扩展性

Table 20和Table 21展示了1.1B参数模型的下游任务评估结果。DID在8个常识推理任务上的平均准确率为43.25%，优于SMDM。在GSM8K数学推理任务上，DID在不同top-p采样策略下均优于SMDM，例如在p=0.6时DID准确率为38.82%，SMDM为36.01%。

### 补充图表

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_VbvXjs5f72_Beyond_M/figures/005_Table_3.jpg]]
*Table 3: Table 3: Average training time (in seconds) per 50 steps (i.e. batches) on OpenWebText.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_VbvXjs5f72_Beyond_M/figures/011_Table_5.jpg]]
*Table 5: Table 5: Average training time (in seconds) per 50 steps on Stories.*



## 定位与知识库关联

DID在扩散语言模型的发展谱系中占据独特位置：

- **与MDLM的关系**：DID是对MDLM的根本性改进，通过删除-插入范式替代掩码-去掩码范式，解决了MDLM的核心计算瓶颈。DID继承了MDLM的连续时间离散扩散理论基础（Campbell et al., 2022; Lou et al., 2024），但改变了前向和后向过程的具体形式。
- **与插入式模型的关系**：DID将插入式生成（Stern et al., 2019; Gu et al., 2019）与严格的扩散理论相结合，弥补了ILM缺乏似然界的不足。与Edit Flows（Havasi et al., 2025）相比，DID避免了辅助编辑路径变量，通过闭式转移概率和并行动态规划实现了更高效的训练。
- **与混合模型的关系**：DID尚未集成混合自回归模型（如Block Diffusion, Arriola et al., 2025）或高级推理算法（如KV缓存, Wu et al., 2025a），这些是未来有前景的方向。

**局限性**：
1. DID尚未集成先进的推理算法（如KV缓存）或混合自回归模型。
2. 并行动态规划算法在序列长度增加时，其时间成本呈超线性增长（拟合幂律指数a=1.26）。
3. 在变长设置下，DID的生成样本中偶尔会出现困惑度极高的异常值。

**开放问题**：
1. 如何将DID与更先进的推理算法（如KV缓存、推理时缩放）结合以进一步提升效率？
2. DID能否与混合自回归模型（如Block Diffusion）结合，以兼顾自回归和扩散模型的优势？
3. DID的并行动态规划算法能否进一步优化，以支持更长的序列（如超过4k tokens）？
4. DID在更大规模模型（如超过1.1B参数）和更多样化任务上的表现如何？



## 原文 PDF

![[paperPDFs/ICLR_2026/Beyond_Masks_Efficient_Flexible_Diffusion_Language_Models_via_Deletion_Insertion_Processes.pdf]]
