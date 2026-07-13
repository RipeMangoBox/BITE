---
title: "$p\\textrm{-less}$ Sampling: A Robust Hyperparameter-Free Approach for LLM Decoding"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ptextrm_less_Sampling_A_Robust_Hyperparameter_Free_Approach_for_LLM_Decoding.pdf
project_link: null
code_link: https://github.com/ryttry/p-less
aliases:
- PLS
- PTLSRHFALD
- "p-less sampling"
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/probabilistic_methods
core_operator: "p-less采样通过计算整个token概率分布的二阶矩（即正确随机猜测的概率L[P]）作为动态截断阈值，该阈值随分布熵自适应变化，无需任何超参数。"
primary_logic: "利用信息论中的Rényi二阶熵（碰撞熵）的指数形式，将截断阈值定义为模型预测概率的平方和，该阈值与分布熵呈负相关，从而在高熵（高温）条件下仍能有效截断低概率token的长尾，保持生成质量。"
claims:
- "p-less采样动态地基于整个token概率分布在每个解码步骤设置截断阈值，且无超参数。"
- "p-less采样在高温下仍能保持高质量输出，而其他方法（如top-p）会退化。"
- "p-less的截断阈值L[P]定义为模型预测概率的平方和，与Rényi二阶熵直接相关。"
- "在数学和逻辑推理任务上，p-less在多个温度下均取得最高或次高的AUC值。"
---

# $p\textrm{-less}$ Sampling: A Robust Hyperparameter-Free Approach for LLM Decoding

> [!tip] 核心洞察
> 利用信息论中的Rényi二阶熵（碰撞熵）的指数形式，将截断阈值定义为模型预测概率的平方和，该阈值与分布熵呈负相关，从而在高熵（高温）条件下仍能有效截断低概率token的长尾，保持生成质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | p-less采样：一种鲁棒的无超参数LLM解码方法 |
| 英文题名 | $p\textrm{-less}$ Sampling: A Robust Hyperparameter-Free Approach for LLM Decoding |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ItFuNJQGH4) · [GitHub](https://github.com/ryttry/p-less) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/probabilistic_methods |
| Method | p-less sampling |
| Dataset | CSQA, GPQA, GSM8K, QASC |

> [!tip] 效果简介
> - CSQA 上，AUC 为 0.503 (p-less, Llama2-7b)，对比 0.500 (min-p, Llama2-7b)，变化 +0.003。
> - GPQA 上，AUC 为 0.242 (p-less, Llama2-7b)，对比 0.238 (min-p, Llama2-7b)，变化 +0.004。
> - GSM8K 上，AUC 为 0.267 (p-less, Llama2-7b)，对比 0.266 (min-p, Llama2-7b)，变化 +0.001。

## 概要

现有LLM解码的截断式采样方法（如top-p、top-k、min-p）的性能高度依赖超参数，且最优超参数随任务和温度剧烈变化，导致高温下文本质量严重退化。本文提出p-less采样，一种基于信息论的无超参数解码方法，通过计算整个token概率分布的二阶矩（即概率平方和L[P] = Σ P(v)²）作为动态截断阈值，该阈值与Rényi二阶熵（碰撞熵）直接相关，随分布熵自适应变化。

核心创新在于：p-less利用整个分布的信息，在高温下仍能有效截断低概率token的长尾，而其他方法（如top-p）在该条件下会纳入大量低概率token导致性能崩溃。p-less保证非空候选集（因模态概率始终≥L[P]），且计算复杂度从O(|V| log |V|)降至O(|V|)。

在Llama2-7b、Mistral-7b、Llama3-70b三个模型以及数学推理（GSM8K）、逻辑推理（CSQA、QASC、GPQA）和创意写作（Writing Prompts）五个数据集上的实验表明：p-less在多数设置下取得最优或次优的AUC值，在高温下性能退化最小；在创意写作任务中，p-less在τ=2.0时长度控制胜率达65.64（Llama2-7b），而top-p降至0；人类评估中p-less以58.8%多数票获胜。此外，p-less的平均采样速度最快（每token 0.01942秒），比min-p快22%，且CPU时间和RAM使用量均最低。



现有的大语言模型（LLM）解码方法，如 top-p、top-k、min-p 等截断式采样，普遍依赖一个关键假设：存在一组固定的超参数（如 top-p 的 p 值、top-k 的 k 值、min-p 的 p_min 值）能够在所有生成场景下有效工作。然而，这一假设在实际应用中面临根本性挑战——超参数的最优取值不仅随生成任务类型变化，更会因采样温度的改变而剧烈波动。具体而言，当温度升高时，token 概率分布趋于平坦，长尾中低概率 token 的概率值被放大，传统固定阈值方法（如 top-p）会将这些低质量 token 大量纳入采样集，导致文本质量严重退化。这一瓶颈的本质在于：现有方法的截断阈值仅依赖于分布的部分统计量（如累积概率、模态概率），缺乏对分布整体形态的感知能力，因此无法在分布熵变化时自适应调整。

针对上述问题，本文提出 p-less 采样方法。其核心洞察在于：利用信息论中 Rényi 二阶熵（碰撞熵）的指数形式，将截断阈值定义为整个 token 概率分布的二阶矩，即所有 token 预测概率的平方和：

$$L[P_\theta] = \sum_{v \in \mathcal{V}} P_\theta(v \mid x_{1:t-1})^2$$

该阈值 $L[P_\theta]$ 与分布熵呈负相关——当分布集中（低熵）时阈值较高，仅保留少数高概率 token；当分布平坦（高熵）时阈值自动降低，但仍能有效截断长尾中概率过低的 token。这种动态自适应特性使得 p-less 无需任何超参数，且能保证候选集非空（因为至少模态概率 $\geq L[P_\theta]$）。p-less 的因果机制可概括为：通过捕捉分布的二阶矩信息，将截断阈值与分布熵建立直接联系，从而在温度变化时自动调整候选集大小，避免高温下低概率 token 的涌入。



## 核心方法与创新机理

p-less 采样的核心瓶颈在于现有截断式采样方法（如 top-p、top-k、min-p）的性能高度依赖人工调节的超参数，且这些超参数的最优值会随生成任务和采样温度剧烈变化，导致高温下文本质量严重退化。p-less 通过引入一个完全由数据驱动的、无超参数的动态截断机制来破解这一瓶颈。

**因果旋钮**：p-less 将截断阈值定义为模型当前 token 概率分布的二阶矩（即所有 token 概率的平方和），记为 $L[P_θ] = Σ_v P_θ(v)^2$。该阈值与分布的 Rényi 二阶熵（碰撞熵）直接相关：$H_2(p) = -\log L[P]$。由于 $L[P]$ 与分布熵呈负相关——当分布高熵（不确定性强）时 $L[P]$ 变小，当分布低熵（确定性高）时 $L[P]$ 变大——该阈值能随温度自适应调整，在高熵（高温）条件下自动降低以纳入更多 token，但始终能有效截断低概率 token 的长尾。

**核心洞察**：p-less 的阈值从信息论中的“正确随机猜测概率”推导而来。假设采样过程与正确性独立，则随机采样一个 token 恰好是正确 token 的概率为 $L[P] = Σ_v P(S=v)P(T=v)$。当模型预测分布 $P_θ$ 近似真实分布 $P$ 时，$L[P_θ] = Σ_v P_θ(v)^2$ 即为该概率的估计值。因此，p-less 的截断策略具有直观的物理意义：只保留那些概率不低于“随机猜对概率”的 token，从而在理论上最小化因采样而引入错误 token 的风险。

**Changed Slots**：

- **截断阈值确定方式**：基线方法依赖固定超参数（如 top-p 的累积概率阈值 p、top-k 的固定 k 值、min-p 的模态概率分数 p_min）或仅使用单个统计量（如 min-p 仅依赖模态概率）。p-less 则使用整个分布的二阶矩，即所有 token 概率的平方和，该值天然地编码了分布的整体形状（集中度/离散度）。
- **超参数需求**：所有基线方法均需手动调节至少一个超参数（包括 mirostat 的目标惊奇度）。p-less 完全无超参数，阈值完全由当前 token 分布的数据驱动计算得到。
- **温度鲁棒性**：基线方法在高温下截断阈值失效，导致大量低概率 token 被纳入采样集，文本质量急剧下降（如 top-p 在 τ=2.0 时在创意写作任务上胜率降至 0%）。p-less 的阈值随温度动态调整，高温下仍能有效截断长尾，保持生成质量。实验表明 p-less 在 τ=2.0 时在 Writing Prompts 数据集上长度控制胜率达 65.64%（Llama2-7b），而 top-p 为 0%。
- **候选集非空保证**：部分基线方法（如 ϵ-sampling、η-sampling、mirostat）在极端分布下可能产生空候选集，需回退到默认策略。p-less 保证非空候选集，因为至少模态概率大于等于 $L[P]$（当分布完全集中于一个 token 时两者相等）。

**关键证据**：
- p-less 在数学和逻辑推理任务上，在多个模型（Llama2-7b、Mistral-7b、Llama3-70b）和温度下均取得最高或次高的 AUC 值（Table 1）。例如在 Llama2-7b 上，p-less 在 CSQA 的 AUC 为 0.503，GPQA 为 0.242，GSM8K 为 0.267，QASC 为 0.537，均优于或持平于最佳基线 min-p。
- 在创意写作任务上，p-less 在高温（τ=2.0）下长度控制胜率远超基线（Table 2），且人类评估中 p-less 以 58.8% 的多数票获胜；在标注者完全一致的案例中，胜率升至 72.7%。
- p-less 在准确率-多样性前沿上表现出帕累托优势：在相同多样性水平下，p-less 的准确率高于其他方法（Figure 3）。
- p-less 的计算效率最高：平均每 token 采样时间仅 0.01942 秒，比 min-p 快 22%（Table 3），且 CPU 时间和 RAM 使用量均低于 top-p 和 min-p（Table 15）。



![[assets/figures/papers/iclr26_0001_ItFuNJQGH4_ptextrm-less_Sampling_A_Robust_Hyperparameter-Fr/figures/005_Figure_2.jpg]]
*Figure 2: Accuracy vs. temperature curves of each method on CSQA, QASC, and GSM8k using Llama-2-7b. AUC values achieved by each method are provided in the legend (in parentheses) with the best AUC in bold*

p-less采样是一个完全无超参数的LLM解码方法，其核心pipeline由三个串行模块构成：阈值计算、候选集构建、归一化采样。

**1. 阈值计算模块**：在每个解码时间步，对当前token概率分布 $P_\theta(v \mid x_{1:t-1})$ 计算其所有token概率的平方和，即 $L[P_\theta] = \sum_{v \in \mathcal{V}} P_\theta(v \mid x_{1:t-1})^2$。该值在信息论上等价于Rényi二阶熵（碰撞熵）的指数形式 $H_2(p) = -\log \sum_i p_i^2$，因此与分布的熵呈负相关——当分布高熵（高温或不确定性大）时，$L[P_\theta]$ 变小，从而降低截断门槛；当分布低熵（确定性高）时，$L[P_\theta]$ 变大，严格筛选高概率token。这一自适应机制是p-less区别于所有基线方法（top-p、top-k、min-p、ϵ-sampling、η-sampling、Mirostat等）的核心差异：基线方法依赖固定超参数或仅使用单个统计量（如min-p使用模态概率），而p-less利用了整个分布的二阶矩信息。

**2. 候选集构建模块**：筛选出概率不低于阈值 $L[P_\theta]$ 的所有token，构成候选采样集 $\mathcal{V}_{p\mathrm{-less}} = \{ v \in \mathcal{V} : P_\theta(v \mid x_{1:t-1}) \geq L[P_\theta] \}$。该方法保证候选集非空，因为模态概率（最大概率）始终大于等于 $L[P_\theta]$，无需像ϵ-sampling、η-sampling或Mirostat那样在极端分布下回退到默认策略。

**3. 归一化采样模块**：对候选集内的概率进行重归一化，得到最终采样分布 $P_\theta'(x_t \mid x_{1:t-1})|_{x_t := v} = \frac{P_\theta(v \mid x_{1:t-1})}{\sum_{v' \in \mathcal{V}_{p\mathrm{-less}}} P_\theta(v' \mid x_{1:t-1})}$，从中采样下一个token。

**输入输出流**：输入为LLM在每个解码步输出的完整token概率分布（logits经softmax后），输出为选定的下一个token。整个过程在每个时间步独立执行，不依赖历史状态或外部知识。

**pipeline的因果机制**：p-less通过将截断阈值与分布熵挂钩，解决了现有截断式采样方法在高温度设置下性能严重退化的根本瓶颈。当温度升高导致分布趋于均匀时，top-p的累积概率阈值会纳入大量低概率token的长尾，min-p的模态概率倍数阈值也会失效，而p-less的 $L[P_\theta]$ 随熵增大而自适应降低，但降低幅度受二阶矩约束，从而在高熵条件下仍能有效过滤低概率token。实验证据表明，p-less在高温（τ=2.0）下仍保持高质量输出（如Llama2-7b在Writing Prompts任务上的长度控制胜率65.64，而top-p降为0.0），且在准确率-多样性前沿上表现出帕累托优势。

**变体p-less_norm**：论文还提出了一个变体，其阈值为 $\bar{L}[P_\theta] = \frac{|\mathcal{V}|}{|\mathcal{V}| - 1} L[P_\theta] - \frac{1}{|\mathcal{V}| - 1}$，该值比 $L[P_\theta]$ 更小，因此候选集更宽松，在需要更高多样性的场景下表现更优。论文未提供明确的选择指导原则，这是该框架的一个开放问题。



### 核心思想与瓶颈

现有截断式采样方法（如 top-p、top-k、min-p）的性能高度依赖超参数选择，且最优超参数随任务和采样温度变化，导致高温下文本质量严重退化。p-less 采样通过计算整个 token 概率分布的二阶矩（即正确随机猜测的概率 $L[P]$）作为动态截断阈值，该阈值随分布熵自适应变化，无需任何超参数。

### 核心公式

**1. 正确随机猜测概率 $L[P]$**

定义为采样 token 与真实正确 token 匹配的概率（假设采样与正确性独立）：

$$
L[P] := \sum_{v \in \mathcal{V}} \mathcal{P}(S = v \cap \mathcal{T} = v \mid x_{1:t-1}) = \sum_{v \in \mathcal{V}} \mathcal{P}(S = v \mid x_{1:t-1}) \mathcal{P}(\mathcal{T} = v \mid x_{1:t-1})
$$

其中 $\mathcal{V}$ 为词汇表，$S$ 为采样 token，$\mathcal{T}$ 为真实正确 token。

**2. p-less 阈值 $L[P_\theta]$**

将模型预测概率 $P_\theta(v \mid x_{1:t-1})$ 代入上式，得到实际使用的截断阈值：

$$
L[P_\theta] = \sum_{v \in \mathcal{V}} P_\theta(v \mid x_{1:t-1})^2
$$

该值为模型预测概率的平方和，与分布熵呈负相关：高熵（高温）分布中 $L[P_\theta]$ 较小，从而允许更多 token 进入候选集；低熵分布中 $L[P_\theta]$ 较大，仅保留高概率 token。

**3. p-less 采样集**

筛选出概率不低于阈值的 token：

$$
\mathcal{V}_{p\mathrm{-less}} = \{ v \in \mathcal{V} : P_\theta(v \mid x_{1:t-1}) \geq L[P_\theta] \}
$$

该集合保证非空，因为至少模态概率 $\max_v P_\theta(v) \geq L[P_\theta]$。

**4. 归一化采样分布**

对候选集内的概率重新归一化后采样：

$$
P_\theta'(x_t \mid x_{1:t-1})|_{x_t := v} = \frac{P_\theta(v \mid x_{1:t-1})}{\sum_{v' \in \mathcal{V}_{p\mathrm{-less}}} P_\theta(v' \mid x_{1:t-1})} \quad \mathrm{for} \quad v \in \mathcal{V}_{p\mathrm{-less}}
$$

### 变体与理论连接

**5. p-less_norm 阈值 $\bar{L}[P_\theta]$**

减去归一化的错误随机猜测概率，得到更宽松的阈值（允许更多 token）：

$$
\bar{L}[P_\theta] := L[P_\theta] - \frac{1}{|\mathcal{V}| - 1} \times \sum_{u,v \in \mathcal{V}, u \ne v} P_\theta(u \mid x_{1:t-1}) P_\theta(v \mid x_{1:t-1}) = \frac{|\mathcal{V}|}{|\mathcal{V}| - 1} L[P_\theta] - \frac{1}{|\mathcal{V}| - 1}
$$

**6. 与 Rényi 熵的关系**

p-less 阈值直接对应 Rényi 二阶熵（碰撞熵）：

$$
H_2(p) = -\log \sum_i p_i^2 = -\log L[P]
$$

且满足 $L[P] \geq \exp(-H_1(p))$，即阈值大于等于 Shannon 熵的负指数，表明两者负相关。

**7. 与二阶矩的关系**

$L[P]$ 是概率质量函数二阶矩的缩放版本：

$$
\mathcal{L}[P] := \sum_{i=1}^{|\mathcal{V}|} P(x_i)^2 = |\mathcal{V}| \times M[P]
$$

其中 $M[P]$ 为二阶矩。p-less 的计算时间复杂度为 $O(|\mathcal{V}|)$（线性于词汇表大小），而 top-p 等方法需要排序，复杂度为 $O(|\mathcal{V}| \log |\mathcal{V}|)$。

### 模块流程

p-less 采样的完整流水线包含三个模块：

1. **计算阈值**：对当前 token 概率分布计算所有 token 概率的平方和 $L[P_\theta]$。
2. **构建采样集**：筛选出概率 $\geq L[P_\theta]$ 的 token。
3. **归一化采样**：对候选集概率归一化后采样下一个 token。

该流程在每个解码步骤重复执行，无需任何超参数调节。



## 实验与关键发现

### 主结果：数学与逻辑推理任务

p-less采样在数学与逻辑推理任务上展现出与最优基线方法（min-p）相当的AUC性能，且其核心优势在于**无需任何超参数**。在Llama2-7b模型上，p-less在CSQA、GPQA、GSM8K和QASC四个数据集上的AUC分别为0.503、0.242、0.267和0.537，均取得最佳或次佳结果（Table 1）。其变体p-less_norm在部分场景下略优（如GPQA上0.248 vs 0.242），但两者差距微小，说明p-less框架本身已接近信息论意义上的最优截断。值得注意的是，p-less在Llama3-70b上的表现同样稳定，在所有温度和数据集组合下均保持最佳或次佳准确率（Table 5），验证了方法在不同规模模型上的通用性。

![[assets/figures/papers/iclr26_0001_ItFuNJQGH4_ptextrm-less_Sampling_A_Robust_Hyperparameter-Fr/figures/002_Table_1.jpg]]
*Table 1: AUC of LLama2-7b, Mistral-7b, and Llama3-70b across different sampling methods for math and logical reasoning datasets. The best AUC is in bold and the second best is underlined*

![[assets/figures/papers/iclr26_0001_ItFuNJQGH4_ptextrm-less_Sampling_A_Robust_Hyperparameter-Fr/figures/023_Table_5.jpg]]
*Table 5: Accuracy of LLama2-7b, Mistral-7b, and Llama3-70b across sampling methods and temperatures (τ ) for math & logical reasoning datasets. The best accuracy for each model, dataset, and τ is in bold and the second best is underlined*

**温度鲁棒性是p-less区别于所有基线方法的关键差异点。** 现有方法（如top-p、ϵ-sampling）在温度从1.0升至2.0时，准确率急剧下降（例如top-p在Llama2-7b的GSM8K上从τ=1.0的41.9%跌至τ=2.0的15.5%），而p-less的准确率几乎不随温度变化（如GSM8K上从35.2%微降至33.5%）。Figure 2的准确率-温度曲线清晰展示了这一现象：p-less的曲线近乎水平，而其他方法在高熵区域急剧下滑。这一鲁棒性的因果机制在于p-less阈值L[P]与分布熵呈负相关——温度升高导致分布趋于均匀时，L[P]自动降低以纳入更多token，但不会像固定阈值方法那样无限制地接纳长尾token（Figure 1）。

### 主结果：创意写作任务

在Writing Prompts创意写作任务上，p-less的优势更为显著。Table 2显示，在温度τ=2.0时，p-less在Llama2-7b上的长度控制胜率达到65.64，而top-p和ϵ-sampling等方法几乎完全失效（胜率接近0）。这一结果直接验证了p-less在高熵场景下维持生成质量的能力——创意写作需要更高的多样性，但现有方法在高温下会采样到大量无意义token导致文本退化。

![[assets/figures/papers/iclr26_0001_ItFuNJQGH4_ptextrm-less_Sampling_A_Robust_Hyperparameter-Fr/figures/006_Table_2.jpg]]
*Table 2: Length-controlled win rate for 100 sampled prompts from the Writing Prompts dataset*

人类评估进一步确认了p-less的实际可用性。在3位标注者的多数投票中，p-less以58.8%的胜率击败默认采样方法（41.2%）；在标注者完全一致的72.7%案例中，p-less的胜率更高达72.7%。标注者间一致性（约60-70%）属于文本生成评估的典型范围，但72.7%的完全一致胜率表明p-less的优势在判别清晰的案例中尤为突出。

### 消融与机制分析

**效率优势：** p-less的时间复杂度从O(|V| log |V|)降至O(|V|)，因为无需对概率分布进行排序。Table 3显示，p-less的平均每token采样时间（0.01942秒）是所有方法中最快的，比min-p快22%。Table 15进一步表明，p-less的CPU时间和RAM使用量均低于top-p和min-p，这使其更适合资源受限的部署场景。

![[assets/figures/papers/iclr26_0001_ItFuNJQGH4_ptextrm-less_Sampling_A_Robust_Hyperparameter-Fr/figures/007_Table_3.jpg]]
*Table 3: Average sampling time per token (in seconds) for p-less and other methods*

**多样性-准确率权衡：** p-less在QASC数据集上展现出帕累托优势——在相同多样性水平下，p-less的准确率高于所有其他方法（Figure 3）。Table 4显示p-less的多样性稳定在0.63-0.64区间，低于min-p（0.76-0.78）但远高于top-p（0.17-0.57）。这表明p-less在保持高质量输出的同时，能够提供适度的生成多样性，避免了top-p在高温下的退化。Table 11进一步揭示，p-less可以通过略微提高温度（如τ=2.25或τ=2.5）达到与min-p相当的多样性水平，且准确率不会像min-p那样随温度升高而急剧下降。

![[assets/figures/papers/iclr26_0001_ItFuNJQGH4_ptextrm-less_Sampling_A_Robust_Hyperparameter-Fr/figures/008_Table_4.jpg]]
*Table 4: QASC diversity by method & temperature*

**生成长度控制：** p-less在多数数据集和温度下生成最短的平均文本长度（Table 12）。对于Llama2-7b，p-less在CSQA、QASC和GSM8K上几乎在所有温度下都取得最短或次短生成长度。这一特性与p-less的截断机制直接相关——通过排除低概率token，p-less自然倾向于生成更紧凑的推理链，这在数学和逻辑推理任务中是有利的。

**推理模型验证：** 在DeepSeek-R1-Distill-Qwen-7B推理模型上，p-less和p-less_norm同样保持最佳或次佳性能（Table 7）。在CSQA上，p-less_norm在最高温度τ=2.0时取得最佳平均准确率67.2，而所有其他方法在该设置下表现最差。这证实了p-less的鲁棒性不局限于标准语言模型，也能推广到经过强化学习训练的推理模型。

### k阶泛化

p-less的k阶泛化（基于Rényi熵的更高阶）在DeepSeek-R1-Distill-Qwen-7B上的实验（Table 9）显示，二阶（即标准p-less）和三阶表现最优，高阶（如k=5,10）的性能略有下降但仍在合理范围内。这为p-less的信息论基础提供了额外证据——二阶碰撞熵恰好捕捉了分布中token之间的成对交互信息，是截断阈值的最自然选择。

### 失败模式

附录C.13分析了两类典型失败模式。**失败模式1**（Figure 18）：在复杂算术运算步骤处，模型分布的熵突然激增，导致p-less接纳了过多低概率token，最终使算术计算结果出错。**失败模式2**（Figure 19）：问题表述本身存在歧义时，p-less在推理链起始处就选择了错误的理解路径，后续推理虽然逻辑一致但基于错误的前提。这两种模式本质上都是p-less依赖模型自身概率分布的副作用——当模型对正确答案的置信度不足时，任何基于概率的截断方法都难以避免错误。需要指出的是，这些失败模式的分析基于少量示例（附录C.13），其普遍性和频率需要更大规模的系统评估来确认。



## 定位与知识库关联

p-less采样方法定位于LLM解码中截断式采样（truncation sampling）这一技术谱系，其核心创新在于**完全消除超参数**，并利用信息论中的Rényi二阶熵（碰撞熵）来动态确定截断阈值。与现有方法相比，p-less从根本上改变了阈值确定方式：从依赖人工设定的固定超参数（如top-p的累积概率阈值p、top-k的固定k值、min-p的模态概率倍数p_min）转向基于整个概率分布的二阶矩（即概率平方和 $L[P_\theta] = \sum_{v \in \mathcal{V}} P_\theta(v)^2$）。这一转变使得p-less在以下三个关键维度上展现出系统性优势。

**与baseline方法的关系**：p-less在数学推理（GSM8K）、逻辑推理（CSQA、QASC、GPQA）和创意写作（Writing Prompts）三个任务类别上，均实现了与最优baseline相当或更优的AUC/准确率。在Llama2-7b上，p-less在CSQA、GPQA、GSM8K、QASC四个数据集上的AUC分别为0.503、0.242、0.267、0.537，均达到或超过min-p（0.500、0.238、0.266、0.536）等最优baseline。更重要的是，p-less在准确率-多样性前沿上展现出帕累托优势——在相同多样性水平下取得更高准确率，这一特性在QASC数据集上得到明确验证（Figure 3）。在创意写作任务中，p-less在温度τ=2.0时的长度控制胜率高达65.64（Llama2-7b），而top-p等方法在此温度下性能已退化至接近0。

**适用边界**：p-less的适用边界由其阈值机制的数学性质决定。当模型输出概率分布接近均匀分布（高熵）时，$L[P]$趋近于1/|V|，此时p-less会保留几乎所有token，退化为直接采样；当分布极为集中（低熵）时，$L[P]$趋近于最大概率值，此时p-less仅保留少数高概率token，接近贪心解码。因此，p-less在中等熵值范围内表现最优，这一范围恰好覆盖了大多数实际生成场景。实验表明，p-less在温度从0.5到2.0的宽泛范围内均保持稳定性能，而其他方法（如top-p、ϵ-sampling）在高温下性能急剧退化。p-less_norm变体通过减去归一化的错误随机猜测概率，得到更宽松的阈值，在需要更高多样性的场景下表现更优，但论文未提供明确的p-less与p-less_norm选择指导原则。

**局限与失败模式**：论文识别出两种典型失败模式。失败模式1（Figure 18）发生在复杂算术运算处：当模型需要执行多步算术计算时，熵的突增导致p-less接纳过多低概率token，最终使答案计算错误。失败模式2（Figure 19）源于问题表述本身的歧义：p-less可能在推理链起始处就产生误解，即使后续推理逻辑一致，也无法纠正初始错误。这两种模式表明，p-less对分布熵的敏感性既是优势也是弱点——当熵突增反映的是模型对计算步骤的不确定性（而非需要探索的多样性）时，p-less的阈值机制可能适得其反。此外，实验主要集中于数学、逻辑推理和创意写作任务，在其他领域（如代码生成、翻译、对话）的表现尚未验证。p-less在多语言场景下的行为也未探讨，词汇表大小和语言特性可能影响阈值行为。

**开放问题**：第一，p-less_norm与p-less在不同任务和温度下的选择标准是什么？是否存在一个统一的框架来自动选择最优变体？第二，p-less的k阶泛化（基于Rényi熵的更高阶）是否能在某些场景下带来进一步改进？初步实验显示（Table 9），高阶泛化在部分数据集上有轻微提升，但缺乏系统性规律。第三，p-less能否与对比解码、算术采样等互补方法结合使用，以进一步提升生成质量？第四，p-less在非常大的模型（如100B+参数）或推理模型上的行为是否与本文观察一致？在DeepSeek-R1-Distill-Qwen-7B上的初步验证（Table 7）表明p-less在推理模型上同样有效，但需要更多大模型实验来确认其可扩展性。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/ptextrm_less_Sampling_A_Robust_Hyperparameter_Free_Approach_for_LLM_Decoding.pdf

![[paperPDFs/ICLR_2026/ptextrm_less_Sampling_A_Robust_Hyperparameter_Free_Approach_for_LLM_Decoding.pdf]]
