---
title: "Spilled Energy in Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Spilled_Energy_in_Large_Language_Models.pdf
project_link: null
code_link: http://github.com/OmnAI-Lab/spilled-energy/
openreview_forum_id: EXFKk4Y3yc
aliases:
- SE
- SELLM
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "溢出能量（spilled energy），即通过能量基模型（EBM）框架分解得到的相邻时间步能量之间的不匹配量（ΔE_θ）。"
primary_logic: "将LLM的softmax分类器重新解释为能量基模型（EBM），利用链式法则将序列概率分解为多个交互的EBM，发现相邻步间的能量应该在理论上相等，但实际解码中会出现“溢出”，该溢出与错误高度相关，从而提供了一种无需训练、仅从logits计算得到的幻觉检测信号。"
claims:
- "溢出能量在合成算术任务中能清晰分离正确与错误答案，特别是在难以检测的范围（[1,10]）上优于logits置信度。"
- "在九个真实世界基准上，溢出能量（Spilled ΔE with Min pooling）平均AuROC大幅超过Orgad et al. (2025)的探测分类器，在LLaMA-Instruct上达到73.16%，且跨任务泛化能力强。"
- "溢出能量分布直方图显示，正确与错误答案的能量值能通过简单阈值轻松分离，且该现象在多个数据集和LLM（LLaMA、Mistral、Gemma）上一致重现。"
- "合成算术 (Math Sums, 13-digit) 上 AuROC = Spilled ΔE 显著分离正确/错误答案，尤其在 Hard 范围表现优异"
---

# Spilled Energy in Large Language Models

> [!tip] 核心洞察
> 将LLM的softmax分类器重新解释为能量基模型（EBM），利用链式法则将序列概率分解为多个交互的EBM，发现相邻步间的能量应该在理论上相等，但实际解码中会出现“溢出”，该溢出与错误高度相关，从而提供了一种无需训练、仅从logits计算得到的幻觉检测信号。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 大型语言模型中的能量溢出 |
| 英文题名 | Spilled Energy in Large Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=EXFKk4Y3yc) · [GitHub](http://github.com/OmnAI-Lab/spilled-energy/) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | Spilled Energy (溢出能量) |
| Dataset | 合成算术 (Math Sums, 13-digit), 9 个标准基准 (HotpotQA, TriviaQA, Movies 等), MNLI (LLaMA 模型) |

> [!tip] 效果简介
> - 合成算术 (Math Sums, 13-digit) 上，AuROC 为 Spilled ΔE 显著分离正确/错误答案，尤其在 Hard 范围表现优异，对比 Logit E^ℓ，变化 大幅提升 (见 ROC 曲线)。
> - 9 个标准基准 (HotpotQA, TriviaQA, Movies 等) 上，平均 AuROC 为 73.16 (LLaMA-Instruct, Spilled ΔE Min)，对比 51.29 (p(true)), 64.16 (Orgad et al. Mean), 54.62 (Logit E^ℓ Max)，变化 +21.87 vs p(true), +9.00 vs Orgad et al.。
> - MNLI (LLaMA 模型) 上，AuROC 为 99.97 (Spilled ΔE Min)，对比 60.33 (Orgad et al.)，变化 +39.64。

## 概要

大型语言模型（LLM）在生成文本时容易产生幻觉——包括事实性错误、推理失败和偏见输出。检测这些错误面临两个核心瓶颈：其一，传统的softmax置信度或logit概率无法可靠地跨任务、跨数据集指示生成内容的正确性；其二，基于探测分类器（probing classifier）的方法虽然性能较好，但需要针对每个任务和数据集训练额外的分类器，缺乏泛化性且引入训练开销。

本文的核心发现是：**溢出能量（spilled energy）**——一种完全无需训练、直接从LLM输出logits计算得到的信号——能够有效检测幻觉。其理论洞察在于，将LLM的softmax分类器重新解释为能量基模型（EBM），并利用概率链式法则将序列生成过程分解为多个交互的EBM。在理想情况下，相邻时间步的边际能量与局部能量应当相等，但在实际解码中会出现“溢出”，而这种能量不匹配量与生成错误高度相关。

方法层面，本文提出了两个训练无关的度量指标：**溢出能量** $\Delta E_{\theta}$ 和**边际能量** $E_{\theta}^{m}$。相比需要训练探测分类器的Orgad et al. (2025)方法，以及直接使用logit置信度的经典基线，溢出能量在数学上具有严格的EBM推导基础，且完全无需额外训练。

实验结果表明，溢出能量在合成算术任务中能够清晰分离正确与错误答案，尤其在难以检测的错误范围上显著优于logit置信度。在九个真实世界基准上，溢出能量（配合Min池化策略）的平均AuROC达到73.16%（LLaMA-Instruct），相比Orgad et al.的探测分类器提升约9个百分点，相比p(true)提升约22个百分点。该方法的有效性在LLaMA、Mistral、Gemma等多个模型系列上得到一致验证，且对预训练和指令微调变体均适用。

值得注意的是，该方法仍存在一定局限：溢出能量可能在标点符号和句子开头token上产生误报，且当前仅在所测试的模型架构上得到验证，对其他架构的泛化性尚需进一步确认。

大型语言模型（LLM）在广泛任务中展现出卓越能力，但其输出仍频繁出现幻觉——包括事实性错误、偏见和推理失败。这些错误在表面上与正确输出难以区分，严重制约了LLM在高可靠性场景中的部署。

当前主流的幻觉检测方法存在明显瓶颈。最直接的方式是利用模型输出的softmax置信度（即答案token的logit或概率值）作为可靠性指标，但这种方法跨任务的检测能力不稳定，在许多场景下无法可靠分离正确与错误输出。另一类方法是在模型内部表示上训练探测分类器（如Orgad et al., 2025），虽然性能有所提升，但需要为每个任务和数据集单独训练，缺乏跨任务泛化性，且引入了额外的训练开销。

上述困境的根源在于：LLM的softmax输出层本质上是一个判别式分类器，其置信度仅反映当前token在给定上下文中的相对概率，而非模型对输出真实性的可靠度量。这引出了一个核心问题——能否从LLM已有的输出信号中，提取出一种无需训练、且与幻觉内在相关的检测信号？

本文的动机正是从能量基模型（Energy-Based Model, EBM）的视角重新审视LLM的解码过程。将LLM的softmax分类器重新解释为EBM后，序列概率可通过链式法则分解为多个交互的EBM。理论上，相邻时间步的边际能量与条件能量应当相等，但在实际LLM实现中，两者之间存在不匹配——即“溢出能量”（spilled energy）。这一溢出量与模型输出的正确性高度相关，从而提供了一种完全无需训练、仅从输出logits计算得到的幻觉检测信号。

## 核心方法与创新机理

### 从分类器到能量基模型的重新解释

现有幻觉检测方法主要依赖两类信号：一是直接使用答案 token 的 softmax 置信度（即 $E_{\theta}^{\ell}$），二是训练针对特定任务和数据集的特征探测分类器（如 Orgad et al. 2025）。前者跨任务泛化能力差，后者需要额外训练开销且无法泛化到分布外数据。

本文的核心理论创新在于**将 LLM 的最终 softmax 分类器重新解释为能量基模型（EBM）**。具体而言，给定前缀 $\mathbf{x}_{i-1:1}$，模型输出的 logits 向量 $\theta(\mathbf{x}_{i-1:1})$ 定义了序列上的概率分布：

$$p_{\theta}(\mathbf{x}_{i:1}) = \frac{\exp(-E_{\theta}^{\ell}(\mathbf{x}_{i:1}))}{Z_{\theta}}$$

其中局部能量 $E_{\theta}^{\ell}$ 和边际能量 $E_{\theta}^{m}$ 分别定义为：

$$E_{\theta}^{\ell}(\mathbf{x}_{i:1}) = -\theta(\mathbf{x}_{i-1:1})[\mathrm{id}(\mathbf{x}_i)]$$

$$E_{\theta}^{m}(\mathbf{x}_{i-1:1}) = -\log \sum_{k=1}^{V} \exp \theta(\mathbf{x}_{i-1:1})[k]$$

基于链式法则，相邻时间步的边际能量与局部能量在理论上应当相等。但在实际 LLM 解码中，两者之间出现了系统性偏差。

### 溢出能量：无需训练的幻觉检测信号

本文的核心方法创新是**溢出能量（Spilled Energy）**，定义为相邻时间步能量之间的不匹配量：

$$\Delta E_{\theta}(\mathbf{x}_{i:1}) \triangleq -E_{\theta}^{m}(\mathbf{x}_{i:1}) + E_{\theta}^{\ell}(\mathbf{x}_{i:1})$$

这一度量的关键特性在于：当模型正确捕捉当前时间步的能量时，$\Delta E_{\theta}$ 应当为零；而实际解码中出现的非零值——即“溢出”——与模型输出错误高度相关（Fig. 2(c-d)）。该信号**完全从输出 logits 计算，无需任何训练、无需内部表示访问、无需梯度或激活消融**。

| 对比维度 | 基线方法 | 本文方法 |
|---------|---------|---------|
| 检测信号 | 探测分类器或 logit 置信度 | 溢出能量 $\Delta E_{\theta}$ 和边际能量 $E_{\theta}^{m}$ |
| 训练需求 | 需为每个任务/数据集训练分类器 | 完全训练无关，仅使用前向传播 logits |
| 理论基础 | 经验性内部表示分析 | 严格的 EBM 和链式法则推导 |

### 方法流水线

溢出能量的完整计算流水线包含以下模块：

1. **局部能量计算**：获取答案 token 的负 logit 值，对应 EBM 的能量。
2. **边际能量计算**：对词汇表所有 token 做 log-sum-exp 取负，给出前缀的边际能量。
3. **溢出能量计算**：将不同时间步的 $E_{\theta}^{\ell}$ 和 $E_{\theta}^{m}$ 做差，得到错误信号。
4. **答案 token 定位**：识别生成序列中精确答案所在的 token 区间 $[u, w]$，避免非答案 token 上的误报（消融实验表明精确定位平均提升约 24% AuROC，Table 2）。
5. **池化策略**：在答案区间上应用 min/max/mean 聚合，其中 Min 池化整体表现最优（Section 5.2, Table 1）。

此外，论文还提出了缩放溢出能量 $\Delta \bar{E}_s(\mathbf{x}_{i:1}) = |E_{\theta}^{m}(\mathbf{x}_{i:1})| \Delta E_{\theta}(\mathbf{x}_{i:1})$，将溢出能量与边际能量的绝对值相乘，组合两种度量（Section 4.2）。

![[assets/figures/papers/iclr26_0011_EXFKk4Y3yc_Spilled_Energy_in_Large_Language_Models/figures/006_Figure_6.jpg]]
*Figure 6: (d) MNLI MathFigure 2: How energy spills in LLMs. (a) Language Modeling p ( $\mathbf { x } _ { i : 1 }$ ) Hotpotqa WC is attained as a decomposition problem following the chain rule of probability, implemented as autoregressive: we recursively apply a discriminative classifier over the vocabulary V to attain generative modeling with larger context size i.e. p ( $\mathbf { x } _ { i } | \mathbf { x } _ { i - 1 : 1 }$ ) . (b) We reinterpret each discriminative classifier as a generative EBM, finding a connection between two quantities that should be the same across time steps yet are different. We call this difference “the spilled energy” $\Delta E _ { \pmb { \theta } } ( \mathbf { x } _ { i : 1 }$...

本文提出的溢出能量（Spilled Energy）幻觉检测方法是一个完全训练无关（training-free）的推理时框架，其核心流程可归纳为四个模块。

**模块一：局部能量与边际能量计算。** 对于LLM自回归生成的每个时间步$i$，直接从softmax前的logits向量$\theta(\mathbf{x}_{i-1:1})$中提取两类能量值。局部能量$E_{\theta}^{\ell}(\mathbf{x}_{i:1})$定义为当前采样token的负logit：
$$E_{\theta}^{\ell}(\mathbf{x}_{i:1}) = -\theta(\mathbf{x}_{i-1:1})[\mathrm{id}(\mathbf{x}_i)]$$
边际能量$E_{\theta}^{m}(\mathbf{x}_{i-1:1})$则定义为整个词表上log-sum-exp的负值：
$$E_{\theta}^{m}(\mathbf{x}_{i-1:1}) = -\log \sum_{k=1}^{V} \exp \theta(\mathbf{x}_{i-1:1})[k]$$
这两类能量均无需任何额外训练或模型修改，仅需在标准前向传播中保留logits即可获得。

**模块二：溢出能量计算。** 根据链式法则，相邻时间步的边际能量与局部能量在理论上应当相等。但在实际LLM解码中，这种等价关系并不成立，由此产生了“能量溢出”。溢出能量$\Delta E_{\theta}(\mathbf{x}_{i:1})$定义为两者的差值：
$$\Delta E_{\theta}(\mathbf{x}_{i:1}) \triangleq -E_{\theta}^{m}(\mathbf{x}_{i:1}) + E_{\theta}^{\ell}(\mathbf{x}_{i:1})$$
该差值在模型正确建模能量时理论上应为零，非零值即构成错误信号。此外，论文还引入了缩放溢出能量$\Delta \bar{E}_s(\mathbf{x}_{i:1}) = |E_{\theta}^{m}(\mathbf{x}_{i:1})| \Delta E_{\theta}(\mathbf{x}_{i:1})$，将边际能量与溢出能量组合使用。

**模块三：答案Token定位。** 溢出能量在非答案token（如标点符号、句子开头）上可能产生误报。为提升检测精度，框架需识别生成序列中精确答案所在的token区间$[u, w]$。实验表明（Table 2），精确的答案token定位可平均提升约24%的AuROC。在合成算术任务中，答案区间天然可知；在真实世界基准中，则需通过答案匹配策略定位。

**模块四：池化策略与检测输出。** 在答案token区间$[u, w]$上，对溢出能量（或边际能量）应用池化聚合，以获得单一检测分数。论文比较了Min、Max和Mean三种池化策略，其中Min池化在多数设置下表现最优（Section 5.2）。最终输出为一个标量检测信号，通过阈值即可区分正确与错误答案——正确答案的溢出能量值较低，错误答案则显著偏高（Fig. 2(d), Fig. 3）。

整个pipeline的输入仅为LLM在生成过程中的logits序列和答案token区间，输出为一个无需训练的幻觉检测分数。该框架在LLaMA、Mistral、Gemma等多个模型系列上均得到了验证（Table 1, Table 3），且对预训练和指令微调变体均有效。

### 能量基模型（EBM）重解释

LLM 的最终 softmax 分类器被重新解释为能量基模型（Energy-Based Model, EBM）。EBM 通过能量函数 $E_{\theta}(\mathbf{x})$ 定义数据点 $\mathbf{x}$ 的概率分布：

$$p_{\theta}(\mathbf{x}) = \frac{\exp(-E_{\theta}(\mathbf{x}))}{Z_{\theta}}$$

其中 $Z_{\theta} = \sum_{\mathbf{x}} \exp(-E_{\theta}(\mathbf{x}))$ 为离散情况下的配分函数。将这一框架应用于序列生成，利用链式法则将序列概率分解为多个交互的 EBM。

### 局部能量与边际能量

在解码过程的每个时间步，定义两种能量度量（Eq. 7）：

**局部能量** $E_{\theta}^{\ell}(\mathbf{x}_{i:1})$：采样 token 的负 logit 值，直接对应序列在位置 $i$ 的能量：

$$E_{\theta}^{\ell}(\mathbf{x}_{i:1}) = -\theta(\mathbf{x}_{i-1:1})[\mathrm{id}(\mathbf{x}_i)]$$

其中 $\theta(\mathbf{x}_{i-1:1})$ 表示前缀 $\mathbf{x}_{i-1:1}$ 条件下的 logits 向量，$\mathrm{id}(\mathbf{x}_i)$ 为 token $\mathbf{x}_i$ 在词表中的索引。

**边际能量** $E_{\theta}^{m}(\mathbf{x}_{i-1:1})$：前缀条件下所有可能 token 能量的负 log-sum-exp，对应前缀的边际能量：

$$E_{\theta}^{m}(\mathbf{x}_{i-1:1}) = -\log \sum_{k=1}^{V} \exp \theta(\mathbf{x}_{i-1:1})[k]$$

其中 $V$ 为词表大小。

### 溢出能量定义

根据链式法则，相邻时间步的边际能量与局部能量在理论上应该相等，但实际 LLM 解码中二者存在差异。**溢出能量**（Spilled Energy, $\Delta E_{\theta}$）正是捕捉这一不匹配量（Eq. 8）：

$$\Delta E_{\theta}(\mathbf{x}_{i:1}) \triangleq -E_{\theta}^{m}(\mathbf{x}_{i:1}) + E_{\theta}^{\ell}(\mathbf{x}_{i:1})$$

当模型正确建模时间步 $i$ 的能量时，$\Delta E_{\theta}$ 应恒为零。实际解码中该值的偏离程度与模型输出错误高度相关。

### 缩放溢出能量

为进一步增强检测信号，引入**缩放溢出能量**（Scaled Spilled Energy），将溢出能量乘以边际能量的绝对值：

$$\Delta \bar{E}_s(\mathbf{x}_{i:1}) = |E_{\theta}^{m}(\mathbf{x}_{i:1})| \cdot \Delta E_{\theta}(\mathbf{x}_{i:1})$$

该组合度量同时利用溢出量和边际能量幅值两个维度的信息。

### 幻觉检测流水线

完整的检测流程包含四个关键模块：

1. **局部能量计算**：获取生成序列中每个 token 的负 logit。
2. **边际能量计算**：对每个前缀计算 log-sum-exp 的负值。
3. **溢出能量计算**：按 Eq. 8 计算相邻步间能量差。
4. **答案 token 定位与池化**：识别生成序列中精确答案所在的 token 区间 $[u, w]$（Section 4.2），在该区间上应用 Min/Max/Mean 池化聚合溢出能量或边际能量，得到单一检测值。消融实验表明，精确的答案 token 定位可带来约 24% 的性能提升（Table 2），而 Min 池化策略整体优于 Max 和 Mean（Section 5.2）。

## 实验与关键发现

### 合成算术任务：溢出能量的分离能力

为验证溢出能量与错误的关联，论文首先在可控的合成算术任务（Math Sums, 13-digit）上进行测试。LLM 被要求计算两个数的和，通过改变错误答案与正确答案的差值来构造不同难度级别。

Figure 3 的直方图表明，溢出能量能够清晰分离正确与错误答案：正确答案的溢出能量值集中在较低区间，而错误答案的值显著偏高。这种分离在多个模型（LLaMA、Mistral、Qwen3）上一致出现。更重要的是，在**难以检测的范围**（错误与正确答案的差值在 [1,10] 之间）上，溢出能量（Spilled ΔE）的 ROC 曲线显著优于传统的 logit 置信度（E^ℓ），表明溢出能量对细微错误的敏感度更高。

![[assets/figures/papers/iclr26_0011_EXFKk4Y3yc_Spilled_Energy_in_Large_Language_Models/figures/015_Figure_3.jpg]]
*Figure 3: Histograms of Spilled Energy values across models (rows) on Math Sums with different error ranges in the answer (columns, decreasing range left to right, making it harder to detect errors). All sums are performed on 13-digit integers. In the fourth column, we show ROC curves for Hallucination Detection across the error ranges (colors) and methods (line styles). (a) Results by Orgad et al*

**关键发现**：溢出能量作为一种无需训练的信号，在合成算术任务上实现了对正确与错误答案的可靠分离，尤其在最难检测的小误差范围内表现出对 logit 置信度的显著优势。

### 真实世界基准：跨任务幻觉检测性能

Table 1 汇总了在 9 个标准基准（HotpotQA, TriviaQA, Movies, MNLI, Math, IMDB, Winobias, Winogrande 等）上的 AuROC 幻觉检测性能，涵盖 4 个 LLM（LLaMA-3, LLaMA-3-Instruct, Mistral, Mistral-Instruct）。

![[assets/figures/papers/iclr26_0011_EXFKk4Y3yc_Spilled_Energy_in_Large_Language_Models/figures/017_Table_1.jpg]]
*Table 1: Hallucination detection performance, in terms of AuROC, across nine benchmarks and four different LLMs. We measure the generalization across all tasks by computing the average*

**核心结果**：
- **Spilled ΔE with Min pooling** 在 LLaMA-Instruct 上达到 **73.16%** 的平均 AuROC，显著超过所有 baseline：Orgad et al. 的探测分类器（64.16%）、p(true)（51.29%）、Logit E^ℓ Max（54.62%）。
- 在 **MNLI 数据集**上，Spilled ΔE Min 在 LLaMA 模型上达到 **99.97%** AuROC，而 Orgad et al. 仅为 60.33%，提升幅度达 +39.64 个百分点。
- 指令微调（instruction tuning）持续提升溢出能量的检测性能：LLaMA-3 从 68.69% 提升至 73.16%，Mistral 从 73.94% 提升至 77.49%。

**跨任务泛化**：Figure 4 的热力图对比了 Orgad et al. 探测分类器与 Spilled ΔE with Min pooling 的跨数据集泛化能力。探测分类器在分布外（out-of-distribution）测试集上性能大幅下降至接近随机猜测水平，而溢出能量无需训练即可在不同任务间保持稳定的检测能力。热力图中正值区域（红色）广泛分布，表明溢出能量在多数跨任务设置下优于探测分类器。

![[assets/figures/papers/iclr26_0011_EXFKk4Y3yc_Spilled_Energy_in_Large_Language_Models/figures/016_Figure_4.jpg]]
*Figure 4: (a) AuROC performance as percentages of probing classifiers on exact answer tokens by Orgad et al. for LlaMA-3-Instruct. (b) depicts the performance difference between our Spilled ∆E with Min pooling and theirs. Positive values indicate cases where Spilled ∆E outperforms Orgad et al.. This comparison highlights the generalization capabilities of our method, compared to probing classifiers. Legend: low performance high performance*

### 池化策略与答案定位的消融

**池化策略**：Table 1 和补充实验（Table 3）比较了 Max、Mean、Min 三种池化策略。Min 池化在大多数方法上取得最优性能——Spilled ΔE with Min pooling 达到 73.32% 平均 AuROC，优于 Mean（约 70%）和 Max（约 66%）。边际能量（Marginal E^m）同样受益于 Min 池化，但整体性能略低于溢出能量。

![[assets/figures/papers/iclr26_0011_EXFKk4Y3yc_Spilled_Energy_in_Large_Language_Models/figures/019_Table_3.jpg]]
*Table 3: generalizes robustly across diverse benchmarks. We observe that instruction-tuned models tend to amplify the margin by which spilled energy outperforms other methods, whereas on non-aligned Mistral, spilled energy may rank slightly behind marginal energy. We also compare pooling strategies and find that min pooling yields the best overall performance across methods. Table 3 shows our method generalizes to Gemma over different LLM size, 1B and 4B. Table 2: Improvements in AuROC with the exact answer. Average across 4 LLMs and 9 benchmarks*

**精确答案 token 定位**：Table 2 报告了精确答案 token 提取对性能的影响。平均而言，使用精确答案区间 [u,w] 可使溢出能量和边际能量的 AuROC 提升约 **24%**。这一消融表明，能量基检测信号主要集中在答案 token 区间，非答案 token（如标点、句子开头）可能引入误报，需要精确定位来抑制噪声。

### 模型泛化性验证

Table 3 展示了在 Gemma-Instruct 1B 和 4B 上的结果。溢出能量在 Gemma 系列上同样表现出竞争力，验证了该方法对不同模型架构（LLaMA、Mistral、Gemma）的泛化能力。值得注意的是，即使在小规模模型（1B）上，溢出能量仍能保持有效的幻觉检测能力。

### 失败模式与局限

尽管溢出能量在多数场景下表现优异，论文指出了以下失败模式：

1. **标点与句首 token 误报**：溢出能量在标点符号和句子开头的 token 上可能产生较高值，导致误报。精确答案定位（Table 2）部分缓解了此问题，但在完全开放式生成中准确定位答案仍然困难。
2. **边际能量与溢出能量的互补性**：在某些非对齐模型（如 Mistral 非 Instruct 版本）上，边际能量可能略优于溢出能量（Table 1），说明两种信号存在互补性，单一使用溢出能量并非在所有设置下都是最优选择。
3. **架构泛化性未充分验证**：当前评估仅限于 LLaMA、Mistral、Gemma 系列，对其他架构（如 GPT 系列、非 Transformer 架构）的有效性需要进一步验证。

### 证据强度评估

- **高置信度（0.95）**：合成算术任务的分离效果、9 基准上的平均 AuROC 优势、MNLI 上的极端提升、精确答案定位的消融结果均有明确的图表和数据支撑。
- **中等置信度（0.9）**：池化策略的最优选择（Min）在不同设置下表现一致，但并非在所有模型/数据集组合上都严格最优；边际能量与溢出能量的互补性需要更多实验验证。
- **需手动验证**：论文未提供对代码生成、翻译等任务的评估，溢出能量在这些场景下的有效性仍是开放问题。

![[assets/figures/papers/iclr26_0011_EXFKk4Y3yc_Spilled_Energy_in_Large_Language_Models/figures/052_Figure_7.jpg]]
*Figure 7: ROC curves for Hallucination Detection across models (rows) on Math Sums with different error ranges in the answer (columns, decreasing range left to right). All sums are performed on 13-digit integers. Legend: Spilled (ours) Spilled ∆E Logit Eℓ Marginal $\bar { \boldsymbol { E } } ^ { m }$

## 定位与知识库关联

### 与现有幻觉检测方法的关系

溢出能量（Spilled Energy）在幻觉检测方法谱系中占据一个独特位置：它属于**训练无关（training-free）的信号驱动方法**，但建立在严格的能量基模型（EBM）数学框架之上，区别于单纯依赖经验置信度的方案。

**与 Logit 置信度的关系**。直接使用答案 token 的 logit 或 softmax 概率（即 $E_{\theta}^{\ell}$）是最经典的无需训练基线。溢出能量可视为对 logit 置信度的**结构性增强**——它不仅利用单个 token 的局部能量，还引入相邻时间步边际能量与局部能量之间的不匹配量 $\Delta E_{\theta}$ 作为检测信号。在合成算术任务中，当错误范围缩小到难以检测的区间（[1, 10]）时，溢出能量的分离能力显著优于纯 logit 置信度（Fig. 3, Fig. 7）。在九个真实世界基准上，Logit $E^{\ell}$ Max 的平均 AuROC 仅为 54.62%，而 Spilled $\Delta E$ Min 达到 73.16%（Table 1，LLaMA-Instruct），差距约 18.5 个百分点。

**与探测分类器（Orgad et al., 2025）的关系**。Orgad et al. 的方法需要在 LLM 内部表示上为每个任务和数据集训练专门的探测分类器，这带来两个根本问题：（1）**训练成本**——每个新任务都需要重新训练；（2）**泛化性差**——在训练数据集之外的表现接近随机猜测（Fig. 4a）。溢出能量完全消除了训练需求，仅从输出 logits 计算，天然具备跨任务泛化能力。在 LLaMA-Instruct 上，Spilled $\Delta E$ Min 的平均 AuROC（73.16%）比 Orgad et al. 的 Mean 策略（64.16%）高出约 9 个百分点（Table 1）。在 MNLI 数据集上，差距更为悬殊——溢出能量达到 99.97%，而探测分类器仅为 60.33%（Table 1 LLaMA block），差距约 39.6 个百分点。

**与 p(true) 的关系**。p(true) 是一种已有的校准方法，用于评估模型对生成回答真实性的概率。在 LLaMA-Instruct 上，p(true) 的平均 AuROC 仅为 51.29%（Table 1），接近随机水平。溢出能量大幅超越该方法（+21.87 个百分点），表明基于 EBM 分解的结构化信号比单纯的概率校准更有效地捕获了模型内部的错误表征。

### 适用边界

溢出能量的有效性已在以下范围内得到验证：

- **模型架构**：LLaMA（3-8B）、Mistral、Gemma（1B/4B）系列，涵盖预训练和指令微调变体。对其他架构（如 GPT 系列、非自回归模型）的泛化性尚未验证，需进一步实验确认。
- **任务类型**：事实性问答（HotpotQA、TriviaQA）、推理（MNLI）、实体识别（Movies）等九个标准基准，以及合成算术任务。对于代码生成、机器翻译等结构化生成任务的有效性仍是开放问题。
- **信号形式**：溢出能量 $\Delta E_{\theta}$ 和边际能量 $E_{\theta}^{m}$ 在不同设置下性能互补，但溢出能量在多数场景中更优（Table 1, Table 5）。Min 池化策略整体优于 Max 和 Mean 池化（Section 5.2）。

### 已知局限

1. **误报问题**：溢出能量在标点符号和句子开头 token 上容易产生误报。这是因为这些位置的 token 本身携带的语义信息有限，能量不匹配可能源于语言结构而非事实错误。论文明确指出这一局限，但未提出系统性的缓解方案。

2. **答案定位依赖**：精确的答案 token 定位对检测性能至关重要——消融实验表明，准确的答案区间提取平均可提升约 24% 的 AuROC（Table 2）。在极端开放式生成场景中，如何可靠地定位答案 token 区间仍是一个挑战，这可能限制溢出能量在自由形式对话等任务中的直接应用。

3. **架构泛化未验证**：当前实验仅覆盖 LLaMA、Mistral、Gemma 三个模型家族。溢出能量的理论推导依赖于 softmax 分类器到 EBM 的重解释（Section 3.1, Section 4.1），虽然这一推导具有一般性，但不同架构的 logit 分布特性可能影响信号质量，需要更多架构上的实证检验。

4. **公平性与偏见**：论文未涉及模型偏见或公平性评估的专门实验，仅声称溢出能量能检测偏见错误。这一声明的实证支撑尚不充分。

### 开放问题

- **误报抑制**：如何系统性地减少溢出能量在非答案 token 上的误报？是否需要引入 token 位置感知的归一化策略或上下文相关的阈值调整？

- **理论深化**：溢出能量在数学上是否可以解释为某种信息守恒的度量？它与模型校准（calibration）之间是否存在更深层的理论联系？

- **解码时干预**：能否利用溢出能量在解码过程中直接干预生成过程以减少幻觉？例如，当检测到高溢出能量时触发重新采样或回溯机制。

- **任务扩展**：对于代码生成、翻译、摘要等结构化或半结构化任务，溢出能量的有效性如何？是否需要针对不同任务设计特定的池化策略或答案定位方法？

## 原文 PDF

![[paperPDFs/ICLR_2026/Spilled_Energy_in_Large_Language_Models.pdf]]
