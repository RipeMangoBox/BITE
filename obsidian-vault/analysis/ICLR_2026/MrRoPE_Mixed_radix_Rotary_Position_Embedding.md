---
title: "MrRoPE: Mixed-radix Rotary Position Embedding"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MrRoPE_Mixed_radix_Rotary_Position_Embedding.pdf
project_link: null
code_link: null
openreview_forum_id: 1J63FJYJKg
aliases:
- MPMRRP
- MrRoPE
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "中间维度的基数扩展因子λ的分布策略（递进式或回归式等）决定了位置信息在频率谱上的重新分配方式，是解决外推失败的关键调节变量。"
primary_logic: "将RoPE扩展理解为一种混合基数转换，通过设计维度特定的λ因子（如递进式扩展），可以在保留高频细节的同时避免低频维度的外推崩溃，从而系统性地突破上下文窗口上限。"
claims:
- "MrRoPE-Pro在128K Needle-in-a-Haystack测试中保持85%以上的召回率，而YaRN在64K后急剧下降。"
- "在Infinite-Bench的检索和对话子集上，MrRoPE-Pro的准确率超过YaRN的两倍以上（KV Retrieval为27% vs 9%，QA Dialogue为22% vs 10%）。"
- "MrRoPE-Pro将RoPE的理论上下文窗口上界从约1K提升至28K，根据RoPE Bound Theory分析。"
- "RULER (LLaMA3-8B-Instruct, 128K context) 上 Average Retrieval Score = 86.6"
---

# MrRoPE: Mixed-radix Rotary Position Embedding

> [!tip] 核心洞察
> 将RoPE扩展理解为一种混合基数转换，通过设计维度特定的λ因子（如递进式扩展），可以在保留高频细节的同时避免低频维度的外推崩溃，从而系统性地突破上下文窗口上限。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MrRoPE：混合基数旋转位置嵌入 |
| 英文题名 | MrRoPE: Mixed-radix Rotary Position Embedding |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=1J63FJYJKg) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | MrRoPE-Pro (Mixed-radix RoPE Progressive) |
| Dataset | RULER (LLaMA3-8B-Instruct, 128K context), Infinite-Bench KV Retrieval (100K‑128K), Infinite-Bench QA Dialogue (100K‑128K) |

> [!tip] 效果简介
> - RULER (LLaMA3-8B-Instruct, 128K context) 上，Average Retrieval Score 为 86.6，对比 79.9 (YaRN)，变化 +6.7。
> - Infinite-Bench KV Retrieval (100K‑128K) 上，Accuracy 为 27%，对比 9% (YaRN)，变化 +18%。
> - Infinite-Bench QA Dialogue (100K‑128K) 上，Accuracy 为 22%，对比 10% (YaRN)，变化 +12%。

## 概要

### 背景与瓶颈

旋转位置嵌入（RoPE）是大语言模型中最广泛使用的位置编码方案之一，但其在处理超长序列时面临根本性瓶颈：高频维度的旋转周期在训练长度外不完整，导致位置信息外推时出现分布外（out-of-distribution）崩溃。从编码理论角度看，这一问题等价于混合基数编码中的**高位数截断**——当序列长度超出编码容量时，高位数字无法完成完整的进位周期，破坏了位置表示的唯一性。

### 核心思想

本文提出 **MrRoPE（Mixed-radix Rotary Position Embedding）**，将 RoPE 的上下文扩展重新诠释为一种**混合基数转换**问题。该框架的核心洞察是：任何 RoPE 扩展方法的本质，都是通过维度特定的基数扩展因子 $\lambda_j$ 在频率谱上重新分配位置信息。基于这一统一视角，现有方法（如 Position Interpolation、NTK-aware Interpolation、YaRN）均可被映射为特定的基数转换策略。

### 方法定位

MrRoPE 属于**训练-自由**的 RoPE 扩展方法，无需额外微调即可实现“短训练、长测试”的泛化。作者提出两种实例化方案：

- **MrRoPE-Uni**：对中间维度采用均匀基数扩展，简洁地扩大编码范围；
- **MrRoPE-Pro**：采用**递进式**基数扩展，使低频维度获得更大的缩放因子（$\lambda_j < \lambda_{j+1}$），在保留高频细节的同时避免低频外推崩溃。

与 YaRN（Peng et al., 2023）的回归式缩放（$\lambda_j > \lambda_{j+1}$）形成鲜明对比，MrRoPE-Pro 的递进式策略是其性能优势的结构性来源。

### 主要结果

MrRoPE-Pro 在多项长上下文基准上取得显著提升：

- **Needle-in-a-Haystack（128K）**：召回率保持 85% 以上，而 YaRN 在 64K 后急剧下降；
- **RULER（128K）**：平均检索得分 86.6，较 YaRN 提升 6.7 分；
- **Infinite-Bench（100K–128K）**：KV Retrieval 准确率 27%（YaRN 为 9%），QA Dialogue 准确率 22%（YaRN 为 10%），均实现翻倍以上提升；
- **理论分析**：根据 RoPE Bound Theory，MrRoPE-Pro 将理论上下文窗口上界从约 1K 提升至 28K。

这些结果表明，递进式基数转换策略能系统性地突破 RoPE 的上下文窗口限制，为长文本大语言模型的部署提供了无需训练的实用方案。



### 超长序列处理中的位置外推困境

大语言模型在预训练后通常受限于固定的上下文窗口长度。以旋转位置嵌入（RoPE）为例，其核心机制是通过不同频率的旋转矩阵为每个位置赋予唯一表示。然而，当推理时的序列长度超出训练长度，RoPE 高频维度的旋转周期不完整，导致位置信息进入“分布外”（out-of-distribution）状态——这类似于混合基数编码中高位数被截断的问题，使得模型无法正确区分远距离位置，注意力模式随之崩溃。

这一瓶颈的本质在于：RoPE 各维度的波长跨度极大，低频维度在训练长度内甚至未完成一个完整旋转周期，而高频维度则已完成数十甚至数百个周期。当上下文窗口被强制扩展时，低频维度面临的是“未见过的位置编码”，高频维度则遭遇“周期碰撞”——两者共同导致了外推失败。

### 现有训练‑自由扩展方法的局限

为突破这一限制，研究者提出了一系列无需微调的 RoPE 扩展方法：

- **Position Interpolation (PI)**（Chen et al., 2023）通过均匀缩放位置索引实现上下文扩展，但这等效于对所有维度进行均匀压缩，导致高频维度的细粒度位置信息被过度扭曲，产生“低位碰撞”。
- **NTK‑aware Interpolation** 采用均匀基数缩放策略，虽改善了高频维度的保留，但未充分考虑不同维度对位置信息的差异化贡献。
- **YaRN**（Peng et al., 2023）引入了“NTK‑by‑parts”策略：根据各维度波长与训练长度的关系，将维度分为高频（已完成足够多周期）、中频、低频（未完成完整周期）三类，并对中间维度采用线性插值。然而，YaRN 在中间维度上实际执行的是**回归式基数转换**——缩放因子 $\lambda_j$ 随维度索引递增而递减（$\lambda_j > \lambda_{j+1}$），这意味着更低频的维度反而获得更小的扩展倍数，限制了上下文窗口的理论上限。

### 混合基数视角下的统一框架

MrRoPE 的核心洞察在于：**将 RoPE 扩展重新理解为一种混合基数转换**。在基数系统中，不同“位”（digit）具有不同的基数权重；类似地，RoPE 的不同维度承担着不同粒度的位置编码功能。通过为各维度设计特定的基数扩展因子 $\lambda_j$，可以系统性地重新分配位置信息在频率谱上的分布——在保留高频细节的同时，为低频维度提供足够的扩展以避免外推崩溃。

这一视角不仅统一了 PI、NTK‑aware Interpolation 和 YaRN 等方法——它们均可被映射为特定的基数转换策略——更重要的是，它揭示了一个关键调节变量：**中间维度上基数扩展因子 $\lambda_j$ 的分布策略**。正是这一策略，决定了模型能否在“保留局部细节”与“扩展全局范围”之间取得最优平衡。



## 核心方法与创新机理

### 问题溯源：RoPE 外推失败的本质

RoPE 在处理超长序列时，高频维度的旋转周期不完整导致位置信息外推失败（out-of-distribution），这类似于混合基数编码中的高位数截断问题。具体而言，当测试序列长度超过训练长度时，部分维度（尤其是低频维度）的旋转角度进入未曾见过的区间，破坏了注意力得分的相对位置依赖关系。

### 统一框架：混合基数转换视角

MrRoPE 的核心贡献在于提出了一种统一的混合基数转换框架，将各类 RoPE 扩展方法重新诠释为不同的基数转换策略。该框架的核心公式为：

$$m \theta _ { j } ^ { \prime } = ( m \cdot \frac { b ^ { \frac { - ( j - 1 ) } { D _ { r } } } } { \prod _ { d = 1 } ^ { j - 1 } \lambda _ { d } } ) \bmod 2 \pi$$

通过为每个维度 $j$ 引入独立的基数扩展因子 $\lambda_j$，该框架将上下文窗口扩展问题转化为频率谱上位置信息的重新分配策略选择问题。

### 关键创新：递进式基数扩展策略

与现有方法的核心差异聚焦于**中间维度**（$d_l \leq j < d_h$）的 $\lambda_j$ 分配策略：

| 方法 | 策略 | 行为特征 |
|------|------|----------|
| **YaRN** (Peng et al., 2023) | 回归式（regressive） | $\lambda_j > \lambda_{j+1}$，缩放因子递减 |
| **MrRoPE-Uni** | 均匀式（uniform） | $\lambda_j = S^{1/(d_h - d_l)}$，所有中间维度等比例扩展 |
| **MrRoPE-Pro** | 递进式（progressive） | $\lambda_j = S^{\varepsilon_j}$，$\varepsilon_j$ 呈算术级数递增 |

MrRoPE-Pro 的递进式缩放指数定义为：

$$\epsilon _ { j } = \frac { 2 ( 1 + j - d _ { l } ) } { ( 1 + d _ { h } - d _ { l } ) ( d _ { h } - d _ { l } ) }$$

这一设计的直觉在于：更低频的维度（更大的 $j$）获得更大的基数扩展（$\lambda_j < \lambda_{j+1}$），使其能够编码更长的位置范围，而高频维度保持较小的扩展以保留细节分辨能力。这与 YaRN 的回归式策略形成鲜明对比——YaRN 在中间维度上采用线性插值，导致缩放因子递减，本质上是牺牲低频维度的编码能力来换取高频维度的稳定。

### 机制差异的实证验证

理论分析表明，YaRN 的回归式基数转换可通过以下不等式证明：

$$\frac { \lambda _ { j } } { \lambda _ { j - 1 } } = \frac { c ^ { 2 } / r _ { j } + ( s - 1 ) ^ { 2 } r _ { j } + ( s - 1 ) c \cdot 2 } { c ^ { 2 } / r _ { j } + ( s - 1 ) ^ { 2 } r _ { j } + ( s - 1 ) c \cdot ( b ^ { \frac { 1 } { D _ { r } } } + b ^ { \frac { - 1 } { D _ { r } } } ) } < 1$$

这意味着 $\lambda_{j-1} > \lambda_j$，即缩放因子单调递减。MrRoPE-Pro 通过反转这一趋势，将更多编码容量分配给需要处理长距离依赖的低频维度，从而在保留高频细节的同时避免低频维度的外推崩溃。

### 与现有工作的本质区别

NTK-aware Interpolation 可视为对所有维度进行均匀基数缩放（$\lambda_j = S^{1/(D_r-1)}$），不区分高频与低频维度的不同需求。Position Interpolation (PI)（Chen et al., 2023）则通过均匀缩放位置索引进行扩展，同样缺乏维度特异性的调节。MrRoPE-Pro 首次在中间维度上引入递进式缩放，这是其在长上下文任务上显著超越 YaRN 和 NTK 方法的根本原因。



![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_1J63FJYJKg/figures/001_Figure_1.jpg]]
*Figure 1: The overall framework of our work. Our key contributions are: (1) a unified theoretical framework for major RoPE-extensions, reflecting them into a specific radix conversion behavior; (2) a progressive radix conversion method MrRoPE-Pro, which outperforms other SoTA methods across various tasks*

MrRoPE 提出了一种基于混合基数转换（Mixed‑Radix Conversion）的统一理论框架，将各类 RoPE 上下文扩展方法重新解释为不同的基数转换策略。该框架的核心洞察是：RoPE 在处理超长序列时，高频维度的旋转周期不完整导致位置信息外推失败，其本质类似于混合基数编码中高位数因进位周期不足而产生的截断问题。

**框架输入与输出**：给定一个已在短上下文（训练长度 $L_{\text{train}}$）上预训练的 RoPE 模型，以及目标扩展倍数 $S$，MrRoPE 框架输出一组逐维度的基数扩展因子 $\lambda_j$，用于修正各维度的旋转角度，从而将模型的有效上下文窗口扩展至 $S \times L_{\text{train}}$，全程无需微调。

**pipeline 模块关系**：MrRoPE 的执行流程由三个核心模块串联构成：

1. **维度分类**：根据训练长度 $L_{\text{train}}$ 与各维度波长 $T_d = 2\pi b^{2d/|D|}$ 的关系，将 RoPE 的所有维度分为三类——高频维度（已完成完整旋转周期）、中间维度（部分完成周期）、低频维度（未完成周期）。这一分类决定了后续各维度的处理策略。

2. **递进式 $\lambda$ 计算**：对中间维度按算术级数计算指数 $\varepsilon_j$，并生成缩放因子 $\lambda_j = S^{\varepsilon_j}$，其中 $\varepsilon_j = \frac{2(1 + j - d_l)}{(1 + d_h - d_l)(d_h - d_l)}$，实现递进式基数扩展——更低频维度获得更大的扩展因子，而更高频维度扩展较小。高频维度保持原始基数不变（$\lambda_j = 1$），低频维度则直接采用位置插值。

3. **旋转角度修正与注意力重缩放**：利用累积缩放因子 $\prod_{d=1}^{j-1} \lambda_d$ 调整各维度的基频，得到扩展后的旋转角 $m\theta'_j = (m \cdot b^{-(j-1)/D_r} / \prod_{d=1}^{j-1} \lambda_d) \bmod 2\pi$。最后，沿用 YaRN 的温度因子 $t$ 对注意力得分进行重缩放，以补偿高频维度的改变。

**关键调节变量**：中间维度的基数扩展因子 $\lambda_j$ 的分布策略是决定外推性能的核心调节变量。MrRoPE‑Pro 采用的递进式策略（$\lambda_j < \lambda_{j+1}$）与 YaRN 的回归式策略（$\lambda_j > \lambda_{j+1}$）形成根本性对立。实验证据表明，递进式策略在保留高频细节的同时，避免了低频维度的外推崩溃，从而系统性地突破上下文窗口上限——MrRoPE‑Pro 将 RoPE 的理论上下文窗口上界从约 1K 提升至 28K（见 Figure 5），并在 128K Needle‑in‑a‑Haystack 测试中保持 85% 以上的召回率，而 YaRN 在 64K 后性能急剧下降。



### 3.1 混合基数RoPE（MrRoPE）统一框架

MrRoPE将RoPE的长度扩展重新诠释为一种**混合基数转换**（mixed-radix conversion）过程。其核心思想源于一个关键观察：RoPE在处理超长序列时，高频维度的旋转周期不完整导致位置信息外推失败（out-of-distribution），这类似于混合基数编码中的高位数截断问题。

在此框架下，任何RoPE扩展方法本质上都是在选择一种通过缩放因子 $\lambda$ 在频率谱上重新分配位置信息的策略。MrRoPE的通用旋转角公式为：

$$m \theta _ { j } ^ { \prime } = ( m \cdot \frac { b ^ { \frac { - ( j - 1 ) } { D _ { r } } } } { \prod _ { d = 1 } ^ { j - 1 } \lambda _ { d } } ) \bmod 2 \pi$$

其中：
- $m$ 为位置索引
- $b$ 为RoPE基频
- $D_r$ 为旋转维度总数
- $\prod_{d=1}^{j-1} \lambda_d$ 为累积缩放因子，通过逐维调整频率实现混合基数转换
- $\theta_j'$ 为扩展后的第 $j$ 维旋转角

### 3.2 维度分类模块

MrRoPE根据训练长度 $L_{\text{train}}$ 与各维度波长 $T_d$ 的关系，将RoPE维度分为三类：

$$T _ { d } = \frac { 2 \pi } { \theta _ { d } } = 2 \pi b ^ { \frac { 2 d } { | D | } }$$

- **高频维度**（$j < d_l$）：$T_d \leq L_{\text{train}}$，已完成完整旋转周期，保持原始RoPE不变
- **中频维度**（$d_l \leq j < d_h$）：$T_d > L_{\text{train}}$ 但接近训练长度，需进行基数扩展
- **低频维度**（$j \geq d_h$）：$T_d \gg L_{\text{train}}$，未完成完整周期，采用位置插值（PI）

超参数 $\alpha$ 和 $\beta$ 分别控制 $d_l$ 和 $d_h$ 的边界位置（$\alpha=32$, $\beta=1$ 为跨模型默认值）。

### 3.3 递进式基数扩展（MrRoPE-Pro）

MrRoPE-Pro的核心创新在于中间维度的**递进式**（progressive）缩放策略。与YaRN采用的回归式策略（$\lambda_j > \lambda_{j+1}$，缩放因子递减）不同，MrRoPE-Pro使缩放因子随维度索引递增（$\lambda_j < \lambda_{j+1}$），让更低频的维度获得更大的基数扩展。

具体而言，缩放因子定义为 $\lambda_j = S^{\epsilon_j}$，其中 $S$ 为目标扩展倍数，指数 $\epsilon_j$ 呈算术级数递增：

$$\epsilon _ { j } = \frac { 2 ( 1 + j - d _ { l } ) } { ( 1 + d _ { h } - d _ { l } ) ( d _ { h } - d _ { l } ) }$$

两种策略的对比公式为：

$$\lambda _ { d } = \left\{ \begin{array} { l l } { S ^ { \frac { 1 } { d _ { h } - d _ { l } } } , } & { \mathrm { ~ i f ~ } M r R o P E – U n i } \\ { S ^ { \frac { 2 ( 1 + d - d _ { l } ) } { ( 1 + d _ { h } - d _ { l } ) ( d _ { h } - d _ { l } ) } } , } & { \mathrm { ~ i f ~ } M r R o P E – P r o } \end{array} \right.$$

MrRoPE-Uni采用均匀缩放，而MrRoPE-Pro的递进式设计使得低频维度获得更大的编码空间扩展，在保留高频细节的同时避免低频维度的外推崩溃。

### 3.4 注意力得分重缩放

为补偿高频维度的改变，MrRoPE沿用YaRN的温度因子 $t$ 对注意力得分进行重缩放（详见附录A.2）。该模块并非MrRoPE的核心创新，但确保了扩展后模型的注意力分布稳定性。

### 3.5 YaRN的回归式基数转换证明

论文通过数学推导证明了YaRN本质上是一种回归式基数转换方法。其逐维缩放因子的比值满足：

$$\frac { \lambda _ { j } } { \lambda _ { j - 1 } } = \frac { c ^ { 2 } / r _ { j } + ( s - 1 ) ^ { 2 } r _ { j } + ( s - 1 ) c \cdot 2 } { c ^ { 2 } / r _ { j } + ( s - 1 ) ^ { 2 } r _ { j } + ( s - 1 ) c \cdot ( b ^ { \frac { 1 } { D _ { r } } } + b ^ { \frac { - 1 } { D _ { r } } } ) } < 1$$

该不等式表明 $\lambda_{j-1} > \lambda_j$，即YaRN的缩放因子单调递减，构成回归式基数转换。MrRoPE-Pro的递进式策略正是在此关键环节上做出了反向设计。



## 实验与关键发现

### 核心性能验证

MrRoPE-Pro在多个长上下文基准上展现出对基线方法的系统性优势，尤其在超长序列（>64K）场景下性能衰减显著慢于现有方案。

**困惑度评估。** 在Proofpile数据集上，MrRoPE-Pro在LLaMA3-8B和Qwen2.5-3B两个模型、8K至128K多个上下文长度下均取得最低困惑度（Table 1）。以LLaMA3-8B在128K为例，MrRoPE-Pro的困惑度为2.34，优于MrRoPE-Uni和YaRN。在LLaMA2-7B的4K测试中，MrRoPE-Pro（5.72）同样领先YaRN（6.02）和MrRoPE-Uni（5.84），表明递进式策略在不同模型规模和上下文长度下具有一致的增益。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_1J63FJYJKg/figures/004_Table_1.jpg]]
*Table 1: Perplexity scores on proofpile dataset across different models. The best and second-best results are boldfaced and underlined, respectively*

**Needle-in-a-Haystack压力测试。** Figure 4的热力图直观展示了两种方法在LLaMA3-8B上的性能差异：YaRN的有效上下文窗口约在64K后出现明显衰减，而MrRoPE-Pro将有效窗口扩展至近96K，在128K深度下仍保持85%以上的ROUGE-1召回率。这一结果直接验证了递进式基数转换在避免高频维度外推崩溃方面的有效性。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_1J63FJYJKg/figures/005_Figure_4.jpg]]
*Figure 4: In the Needle-IN-A-Haystack test, MrRoPE-Pro (right) effectively extends LLaMA3-8B’s context window to nearly 96K, which is much longer than the performance of YaRN (left)*

**RULER综合基准。** Table 2汇总了13个子任务的检索得分。在LLaMA3-8B-Instruct的128K设置下，MrRoPE-Pro取得86.6的平均分，较YaRN（79.9）提升6.7分。值得注意的是，YaRN在64K后性能急剧下降，而MrRoPE-Pro的衰减曲线更为平缓，说明递进式策略有效缓解了中频维度的外推失效问题。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_1J63FJYJKg/figures/006_Table_2.jpg]]
*Table 2: Retrieval scores on RULER benchmark across all 13 subtasks*

**Infinite-Bench真实长文本评估。** Table 3聚焦100K-128K长度的样本，覆盖检索、对话、数学等多类任务。MrRoPE-Pro在关键子集上实现了对YaRN的成倍超越：KV Retrieval准确率从9%提升至27%，QA Dialogue从10%提升至22%。在Passkey Retrieval上达到100%，Number Retrieval达到89%，部分任务（如QA Dialogue、Math Find）的性能已接近GPT-4水平。这一结果说明递进式基数转换不仅适用于合成任务，在真实长文本理解场景中同样具有显著优势。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_1J63FJYJKg/figures/007_Table_3.jpg]]
*Table 3: Long context performance comparison on Infinite-Bench. In each subset, we randomly choose 100 samples with lengths ranging from 100K to 128K. MrRoPE-Pro outperforms YaRN under the same settings while approaching GPT-4 in some tasks (e.g., QA Dialogue, Math Find)*

**LongBench-v2下游任务。** Table 5进一步验证了MrRoPE-Pro在多类型长文本理解（单文档QA、长对话历史理解、多文档QA、长上下文学习、结构化数据理解、代码仓库理解）上的广泛适用性，在两个模型上均保持对YaRN的领先。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_1J63FJYJKg/figures/013_Table_5.jpg]]
*Table 5: Resultes of LLaMA3-8B-Instruct and Qwen2.5-3B-Instruct on LongBenchV2 dataset. SD: Single-Document QA, LD: Long-dialogue History Understanding, MD: Multi-Document QA, LICL: Long In-context Learning, LSD: Long Structured Data Understanding, CU: Code Repository Understanding*

### 消融实验

**递进式 vs. 均匀式策略。** MrRoPE-Uni作为均匀基数扩展的对照方案，其困惑度低于YaRN但高于MrRoPE-Pro（Table 1），直接证明了递进式策略在中间维度上的优越性。该结果与理论预期一致：均匀缩放忽略了不同维度对位置信息敏感度的差异，而递进式缩放通过让更低频维度获得更大扩展因子，更精细地重新分配了频率谱上的位置信息。

**超参数鲁棒性。** 附录中的敏感性分析（Figure 7、Figure 8）表明，MrRoPE-Pro在128K上下文窗口下改变维度分类边界参数d_h（α）和d_l（β）时，困惑度始终优于YaRN。α=32和β=1被验证为跨模型（LLaMA3-8B、Qwen2.5-3B）的稳健默认配置，方法对超参数选择不敏感。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_1J63FJYJKg/figures/010_Figure_7.jpg]]
*Figure 7: LLama3-8B-Instruct PPL score tested on 128K context window across different $\alpha / \beta$ settings

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_1J63FJYJKg/figures/011_Figure_8.jpg]]
*Figure 8: Qwen2.5-3B-Instruct PPL score tested on 128K context window across different α/β settings*

### 理论分析支撑

**上下文窗口理论上界。** 基于RoPE Bound Theory的分析（Figure 5），MrRoPE-Pro通过提升余弦和函数B_θ(m)的零根范围，将理论上下文窗口上界从原始RoPE的约1K扩展至28K。这一理论结果与实验观测到的有效窗口扩展（NIAH测试中近96K）在趋势上一致，为递进式策略的有效性提供了机理性解释。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_1J63FJYJKg/figures/008_Figure_5.jpg]]
*Figure 5: The cosine sum of the rotation angles in each dimension, measuring the ability to give more attention to similar tokens than a random one. The base value and original context length are consistent with the settings of LLaMA2-7B*

**中间维度注意力分布。** Figure 6展示了中间维度注意力得分随相对位置的分布。MrRoPE-Pro能更稳定地保持高注意力聚集，而YaRN在长距离下注意力分布趋于平坦。这表明递进式基数转换通过优化中间维度的特征表示，稳定了扩展后的注意力得分分布，从而维持了模型对远距离依赖的建模能力。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_1J63FJYJKg/figures/009_Figure_6.jpg]]
*Figure 6: Middle-partial attention score on extended context windows. For each relative position, we randomly selected 50 token pairs’ corresponding attention score calculated by the middle dimensions*

### 公平性说明

所有实验均在无需微调的推理环境下进行，公平对比训练自由的RoPE扩展方法（YaRN、NTK-aware Interpolation）。超参数选择遵循作者推荐的默认值，评估基准覆盖合成任务（RULER、NIAH）和真实长文本任务（Infinite-Bench、LongBench-v2），结果具有代表性。

### 局限性

当前方法聚焦于训练自由的上下文窗口扩展，缺少微调实验限制了与xPOS、LongRoPE等需要训练的扩展方法的直接对比。此外，混合基数转换思想高度依赖RoPE机制本身，其能否推广至其他位置编码方案仍是一个开放问题。理论分析仅在LLaMA2-7B设置下验证，未在其他更大规模模型或非常见基频配置下系统评估。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_1J63FJYJKg/figures/003_Figure_3.jpg]]
*Figure 3: The cumulative scaling factor s _ { d } of different RoPE extension methods across varying dimension index.(Scale-up to 16x and 4x)*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_1J63FJYJKg/figures/012_Table_4.jpg]]
*Table 4: Perplexity scores of LLaMA2-7B-chat-hf on proofpile dataset. The best and second best results are boldfaced and underlined respectively*



## 定位与知识库关联

### 1. 问题根源：RoPE 外推的 OOD 困境

RoPE 在处理超长序列时的核心瓶颈在于高频维度的旋转周期不完整，导致位置信息外推失败（out-of-distribution）。从混合基数编码的视角来看，这等价于高位数截断问题——当序列长度超出训练时的基数表示范围，高位数字无法完成完整的进位周期，导致位置编码失真。这一理论框架将 RoPE 的上下文窗口限制归结为一种编码容量饱和现象。

### 2. 现有方法的基数转换谱系

MrRoPE 框架将主流的训练-自由 RoPE 扩展方法统一为不同的基数转换策略，构成了清晰的方法谱系：

- **Position Interpolation (PI)**（Chen et al., 2023）：通过均匀缩放位置索引进行上下文扩展，等价于对所有维度施加统一的基数压缩，以牺牲高频分辨率为代价换取更长的表示范围。

- **NTK-aware Interpolation**：实现跨所有维度的均匀基数缩放，缩放因子 $\lambda_j = S^{1/(D_r - 1)}$，不区分高频与低频维度的不同需求。

- **YaRN**（Peng et al., 2023）：采用 NTK-by-parts 策略，在中间维度使用回归式缩放（$\lambda_j > \lambda_{j+1}$），即缩放因子随维度索引递减。论文通过数学证明（Eq. 25）严格推导了 YaRN 的缩放因子单调递减性质：$\frac{\lambda_j}{\lambda_{j-1}} < 1$，确认其属于回归式基数转换。

这三种方法的核心差异在于对中间维度（$d_l \leq j < d_h$）的基数扩展因子 $\lambda_j$ 的分配策略不同，这一策略决定了位置信息在频率谱上的重新分配方式。

### 3. MrRoPE 的递进式突破

MrRoPE 提出了两种训练-自由的扩展策略：

- **MrRoPE-Uni**：对中间维度施加均匀缩放，$\lambda_j = S^{1/(d_h - d_l)}$，作为递进式策略的对照基线。

- **MrRoPE-Pro**：采用递进式基数转换，$\lambda_j = S^{\epsilon_j}$，其中指数 $\epsilon_j = \frac{2(1 + j - d_l)}{(1 + d_h - d_l)(d_h - d_l)}$ 呈算术级数递增（$\lambda_j < \lambda_{j+1}$），使更低频维度获得更大的基数扩展。

这一递进式策略的根本洞察在于：高频维度需要保留细节分辨率，应施加较小扩展；低频维度需要避免外推崩溃，应施加较大扩展。这与 YaRN 的回归式策略形成鲜明对比——YaRN 对低频维度施加较小扩展，导致其在超长上下文（>64K）中性能急剧退化。

### 4. 关键调节变量：$\lambda$ 分配策略

中间维度的基数扩展因子 $\lambda$ 的分布策略是解决外推失败的核心调节变量。MrRoPE-Pro 的递进式设计通过维度特定的 $\lambda$ 因子，在保留高频细节的同时避免低频维度的外推崩溃，从而系统性地突破上下文窗口上限。

实验证据支持这一论断：
- 在 128K Needle-in-a-Haystack 测试中，MrRoPE-Pro 保持 85% 以上的召回率，而 YaRN 在 64K 后急剧下降。
- 在 Infinite-Bench 的检索和对话子集上，MrRoPE-Pro 的准确率超过 YaRN 的两倍以上（KV Retrieval: 27% vs 9%；QA Dialogue: 22% vs 10%）。
- 根据 RoPE Bound Theory 分析，MrRoPE-Pro 将理论上下文窗口上界从约 1K 提升至 28K。

消融实验进一步验证：MrRoPE-Uni 的困惑度低于 YaRN 但高于 MrRoPE-Pro，证明递进式策略在中间维度上确实优于均匀策略和回归式策略。超参数 $\alpha=32$ 和 $\beta=1$ 在 LLaMA3-8B 和 Qwen2.5-3B 上表现出跨模型的稳健性。

### 5. 适用边界与局限

**适用前提**：
- 方法高度依赖于 RoPE 机制本身，其混合基数转换思想能否推广至其他位置编码方案（如 T5 相对偏置、ALiBi）仍是一个开放问题。
- 所有实验均在无需微调的推理环境下进行，与 xPOS、LongRoPE 等需要训练的扩展方法缺乏直接对比。

**已知局限**：
- 理论分析仅在 LLaMA2-7B 设置下验证，未在其他更大规模模型或非常见基频配置下系统评估。
- 中间维度采用线性插值（如 YaRN）是否在特定条件下（如更短上下文）能胜过递进式策略，尚未充分探索。

**开放问题**：
- 混合基数转换框架能否被证明是最优的 RoPE 扩展方式，还是仅作为现有方法的一种重新诠释？
- 对于任意模型和上下文扩展长度，是否存在理论指导的自动 $\lambda$ 策略搜索算法，而非手工设计的递进式方案？
- 该框架是否能无缝结合微调以进一步突破理论编码上限，并与长上下文适配器等方法结合？



## 原文 PDF

![[paperPDFs/ICLR_2026/MrRoPE_Mixed_radix_Rotary_Position_Embedding.pdf]]
