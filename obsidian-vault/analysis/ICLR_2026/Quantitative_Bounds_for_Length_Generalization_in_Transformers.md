---
title: "Quantitative Bounds for Length Generalization in Transformers"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Quantitative_Bounds_for_Length_Generalization_in_Transformers.pdf
openreview_forum_id: TLSUIyBIfs
aliases:
- QBLGT
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/learning_theory
core_operator: "训练序列长度需足以用短序列模拟长序列的注意力分布与统计量。该能力受参数范数、词汇量、位置周期Δ、局部窗口τ和允许误差ε定量决定。"
primary_logic: "长度泛化的充分条件：若两个变换器在长度≤N的序列上输出一致，则它们在任何长度上的输出也近似一致，只需N大到使短序列能模拟长序列。"
claims:
- "定理4.1给出ℓ∞条件下训练长度N=O(max{2^{p/γ}, L^2 Δ^7 |Σ|^6 τ^2/ε^2})。"
- "引理5.3通过随机子采样构造短序列z，使其在任意Lipschitz函数上的经验均值与长序列x的差在O((G+L)(τ+1)/n^{1/3})内。"
- "定理5.2针对两层无限精度变换器，证明训练长度N ≲ (max(C(f),C(g))/ε)^{max(1/γ,3)}。"
- "SimpleTask 上 Test loss plateau = 训练长度增加时测试损失平台值单调下降"
---

# Quantitative Bounds for Length Generalization in Transformers

> [!tip] 核心洞察
> 长度泛化的充分条件：若两个变换器在长度≤N的序列上输出一致，则它们在任何长度上的输出也近似一致，只需N大到使短序列能模拟长序列。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Transformer长度泛化的定量界限 |
| 英文题名 | Quantitative Bounds for Length Generalization in Transformers |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=TLSUIyBIfs) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/learning_theory |
| Method | 长度泛化定量界限 |
| Dataset | SimpleTask, ModPTask, In-context k-gram |

> [!tip] 效果简介
> - SimpleTask 上，Test loss plateau 为 训练长度增加时测试损失平台值单调下降，对比 最短训练长度时的损失平台值，变化 损失平台值随训练长度增加而下降；随ω增加而上升。
> - ModPTask 上，Test loss plateau 为 训练长度增加时测试损失平台值单调下降，对比 最短训练长度时的损失平台值，变化 损失平台值随训练长度增加而下降；随Δ增加而上升。
> - In-context k-gram 上，Test loss plateau 为 训练长度增加时测试损失平台值单调下降，对比 最短训练长度时的损失平台值，变化 损失平台值随训练长度增加而下降；随S或k增加而上升。

## 概述

Transformer 在短序列上训练后能否泛化到任意长序列——即**长度泛化**（Length Generalization）——是当前大模型能力的关键瓶颈之一。已有理论工作仅证明存在某个有限训练长度后长度泛化是可能的，但未能回答一个根本性的量化问题：**究竟需要多长的训练序列？**

本文首次为 Transformer 的长度泛化提供了**定量界限**，明确给出了训练序列长度 $N$ 的充分条件。核心结论是：长度泛化成立，当且仅当 Transformer 在长序列上的内部行为能被其在短序列上的行为所“模拟”。这一模拟能力受以下因素定量决定：

- **参数范数**（权重矩阵的范数界）
- **词汇量** $|\Sigma|$
- **位置编码的周期** $\Delta$ 与局部窗口 $\tau$
- **允许误差** $\varepsilon$
- **精度** $p$（有限精度设定下）

论文在多个设定下分别建立了界限：有限精度硬注意力与无限精度软注意力、$\ell_\infty$ 误差控制与平均误差控制、单层与两层 Transformer。主要定理表明，所需训练长度对精度、周期和词汇量呈多项式或指数依赖。实验在 SimpleTask、ModPTask 和上下文 k-gram 三个任务上验证了理论预测：测试损失平台值随训练长度增加单调下降，随任务难度参数（$\omega$、$\Delta$、$k$、$S$）增加而上升。

本工作将长度泛化从存在性论证推进到可量化的充分条件，为理解 Transformer 的外推能力提供了首个理论标尺。

## 背景与动机

Transformer 在自然语言处理、代码生成和数学推理等任务上展现出强大能力，但其**长度泛化**（Length Generalization）——即在短序列上训练后能否在长序列上保持性能——始终是一个核心挑战。实践中，模型在超出训练长度的序列上往往出现性能退化，表现为测试损失不再下降而进入一个平台期。理解这一现象的理论条件，对于设计可扩展的序列模型至关重要。

然而，现有的理论工作存在一个关键缺口：它们仅**定性**地证明了存在某个有限的训练长度，使得长度泛化成为可能，但从未给出**需要多长的训练序列**这一量化答案。换言之，我们不知道为了在长度为 $T$ 的测试序列上达到误差 $\varepsilon$，训练序列长度 $N$ 究竟需要多大。这一缺失使得理论结果难以指导实际训练配置的选择。

本文填补了这一空白，首次为 Transformer 长度泛化提供了**定量界限**。核心洞见在于：长度泛化之所以可能，是因为当训练序列足够长时，模型在长序列上的内部行为可以被其在短序列上的行为所“模拟”。具体而言，如果两个 Transformer 在所有长度不超过 $N$ 的序列上输出一致，那么它们在任意长度序列上的输出也近似一致——关键在于 $N$ 需大到使短序列能够充分复现长序列的注意力分布和统计特征。

为刻画这一条件，本文在多个维度上展开了系统分析：

- **误差控制方式**：$\ell_\infty$ 最坏情况误差与输入分布下的平均误差。
- **注意力精度**：有限精度下的硬注意力（hardmax）与无限精度下的 softmax 注意力。
- **模型深度**：单层与两层 Transformer。
- **位置编码结构**：假设位置编码具有 $\Delta$ 周期性、平移不变性和 $\tau$ 局部性。

在这些设定下，所需训练长度 $N$ 的上界由参数范数、词汇量 $|\Sigma|$、位置周期 $\Delta$、局部窗口 $\tau$ 和允许误差 $\varepsilon$ 等因素定量决定。例如，在有限精度 $\ell_\infty$ 误差设定下，定理 4.1 给出了 $N = O\!\left(\max\!\left\{2^{p/\gamma},\; \frac{L^2 \Delta^7 |\Sigma|^6 \tau^2}{\varepsilon^2}\right\}\right)$ 的界限，其中 $p$ 为精度位数，$\gamma$ 为注意力 logit 的最小间隔。

本文还通过构造性证明揭示了短序列模拟长序列的具体机制：在有限精度情形中，显式构造一条短序列 $z$ 来逼近长序列中硬注意力模式的经验频率（定理 4.1 证明）；在无限精度情形中，则通过从特定分布中随机采样 $z$ 并运用概率方法（定理 5.2 证明），借助引理 5.3 保证子采样序列在任意 Lipschitz 函数上的经验均值与原始长序列的差异以 $O((G+L)(\tau+1)/n^{1/3})$ 为界。

实验在 SimpleTask、ModPTask 和 In-context k-gram 三个合成任务上验证了理论预测：随着训练长度增加，测试损失的平台值单调下降；而增大 $\omega$（位置编码频率）、$\Delta$（周期）或 $S$（词汇量）等参数则使平台值上升，与理论界限的依赖关系定性一致（图 1、2、4）。

尽管如此，当前分析仍限于浅层架构和特定位置编码假设，界限中的指数或多项式依赖也意味着理论值可能远大于实际所需的最小训练长度。这些问题为后续研究指明了方向。

## 核心创新

本文的核心贡献并非提出新的模型架构或训练算法，而是**首次为Transformer的长度泛化能力建立了定量理论**。已有理论工作仅能证明存在某个有限训练长度后可以实现长度泛化，但始终未能回答一个根本性问题：**究竟需要多长的训练序列？** 本文通过构造性证明，给出了训练长度$N$的显式上界，将长度泛化从存在性结果推进到可定量刻画的程度。

### 核心洞察：短序列对长序列的模拟

整个理论框架建立在一个统一的核心洞察之上：**若两个变换器在长度不超过$N$的序列上输出一致，则它们在任何长度上的输出也近似一致**。这一结论成立的关键在于，$N$需要大到使短序列能够"模拟"长序列的内部行为——包括注意力分布和统计量。换言之，长度泛化的充分条件并非模型在长序列上见过足够多的样本，而是模型在短序列上已能复现处理长序列所需的所有计算模式。

### 定量界限的因果调控变量

本文揭示的训练长度$N$并非单一数值，而是受多个可量化因素共同决定的函数。这些因素构成了理解长度泛化的"因果旋钮"：

- **参数范数**：权重矩阵的范数越大，模型对输入扰动的敏感度越高，模拟长序列所需的短序列长度也随之增长。
- **词汇量$|\Sigma|$**：更大的词汇量意味着需要匹配的统计量更多，对模拟精度提出更高要求。
- **位置周期$\Delta$**：位置编码的周期性决定了模型对位置信息的抽象粒度，直接影响模拟效率。
- **局部窗口$\tau$**：模型关注的局部上下文窗口越宽，需要保留的序列结构信息越多。
- **允许误差$\varepsilon$**：对输出精度的要求越严格，所需的训练长度自然越大。
- **精度$p$与logit间隔$\gamma(f)$**：在有限精度下，当训练长度超过$2^{p/\gamma(f)}$时，softmax注意力的非最大项被舍入为零，退化为硬注意力，这从根本上改变了模型的行为模式。

### 有限精度与无限精度的统一处理

本文的另一关键创新在于**同时处理了有限精度和无限精度两种计算模型**，并揭示了两者之间的本质联系。在有限精度下（Section 3.2），当序列长度超过阈值$2^{p/\gamma(f)}$时，softmax注意力等价于硬注意力，这使得模型的计算可被简化为token频率的统计。在无限精度下（Section 3.3），作者提出对$\tau$-后缀的注意力logit乘以$\log i$进行缩放，从而产生三种注意力模式（Token Dominant、Balanced、Position Dominant），使模型在任意长度下都能保持稳定的计算行为。这种统一视角使得定量界限的推导能够覆盖实际部署中的多种精度设定。

### 构造性证明的技术路径

定理4.1（$\ell_\infty$误差）和定理5.2（两层无限精度）的证明采用了不同的构造策略，代表了两种互补的模拟范式：

- **确定性构造**（定理4.1）：通过显式构造一个从任意长序列$x$到短序列$z$的映射，确保$z$在硬注意力模式下保留$x$的关键token频率，从而保证输出近似。所需训练长度$N = O(\max\{2^{p/\gamma}, L^2 \Delta^7 |\Sigma|^6 \tau^2 / \varepsilon^2\})$。

- **随机子采样构造**（引理5.3，支撑定理5.2）：通过从长序列中随机采样子集构造短序列$z$，利用马氏链的平稳分布性质证明$z$在任意Lipschitz函数上的经验均值与$x$的差异在$O((G+L)(\tau+1)/n^{1/3})$内。然后借助概率方法，证明存在一个短序列使模拟成立。定理5.2最终给出训练长度$N \lesssim (\max(C(f), C(g))/\varepsilon)^{\max(1/\gamma, 3)}$，其中$C(f)$是依赖于第一层权重的复杂度度量。

这两种构造路径共同说明了一个深层原理：**长度泛化的本质是统计量保持问题**——只要短序列能足够精确地复现长序列中模型所依赖的统计特征（如token频率、$\tau$-后缀分布），泛化就必然发生。

## 整体框架

本文的核心目标是为 Transformer 的长度泛化能力建立首个定量理论。其分析框架围绕一个中心命题展开：**长度泛化之所以可能，是因为长序列上的 Transformer 内部行为可以被短序列“模拟”**。基于这一洞见，论文构建了从模型假设、序列模拟到界限推导的完整分析管线。

### 模型设定与假设空间

分析采用“极限 Transformer”（limit transformer）作为理论模型，其前向传播定义如下：

- **输入嵌入**：$y_i^{(0)} = E_{x_i} + p_i$，将 token 和位置编码映射为初始表示。
- **自注意力**：第 $l$ 层第 $h$ 个注意力头的 logit 为 $a_{i,j}^{(l,h)} = (y_j^{(l-1)})^\top K_{l,h}^\top Q_{l,h} y_i^{(l-1)} + \phi_{l,h}(j,i)$，其中 $\phi_{l,h}$ 为位置偏置项。
- **MLP + 残差**：通过单隐藏层 MLP 和残差连接进一步变换。
- **输出映射**：线性层将最终表示映射为 logits。

论文对位置编码施加了三个关键结构假设：

1. **Δ-周期性**：$p_i = p_{i+\Delta}$，位置编码以 Δ 为周期重复。
2. **平移不变性**：$\phi_{l,h}(j,i) = \phi_{l,h}(j+t, i+t)$，注意力偏置仅依赖相对位置。
3. **τ-局部性**：$\phi_{l,h}(j,i) = 0$ 当 $|j-i| > \tau$，即位置偏置仅在局部窗口内非零。

这三个假设是后续所有定量界限的基石：周期性将无限位置空间压缩到有限等价类，平移不变性保证行为的一致可迁移性，局部性则限制了长序列中注意力依赖的范围。

### 精度假设与注意力退化

论文区分了两种精度设定，它们从根本上改变了注意力机制的行为：

**有限精度（finite precision）**：假设所有中间计算量绝对值 ≤ $2^{-p}$ 时被舍入为 0。在 softmax 计算中，先将最大 logit 标准化为 0，则其余 logit $a$ 对应的 softmax 项为 $\exp(\log N \cdot a)$。定义 **logit 间隔** $\gamma(f)$ 为最小非零注意力 logit 差值，当序列长度 $N \geq 2^{p/\gamma(f)}$ 时，所有非最大 logit 对应的 softmax 项均 ≤ $2^{-p}$ 而被舍入。此时 softmax 注意力退化为 **硬注意力（hardmax）**：仅在取得最大 logit 的位置上均匀聚合。

**无限精度（infinite precision）**：权重矩阵有界时，τ-后缀位置偏置对注意力的影响会随序列长度发散而衰减至零。为避免这一退化，论文提出对 τ-后缀 logit 乘以 $\log i$ 进行缩放，由此产生三种注意力机制：Token 主导（token logit 远大于位置偏置）、平衡态（两者可比）、位置主导（位置偏置占优）。

### 核心分析管线：从模拟到界限

整个定量界限的推导遵循统一的“模拟-逼近”范式：

1. **构造模拟映射**：对于任意长序列 $x$，构造一个长度 ≤ N 的短序列 $z$，使得两者在 Transformer 各层的关键统计量上近似一致。这些统计量包括：硬注意力模式下的 token 经验频率、τ-后缀与 token 频率的组合分布等。

2. **误差传播与控制**：利用 Transformer 各模块的 Lipschitz 性质，将统计量误差逐层传播为最终输出的误差。单层情况下，输出误差直接由值向量的加权平均误差控制；两层情况下，需额外控制第一层输出表示在第二层注意力计算中的误差累积。

3. **界限实例化**：根据误差控制目标和序列分布假设，给出所需训练长度 N 的显式上界：
   - **ℓ∞ 误差**（定理 4.1）：$N = O\left(\max\left\{2^{p/\gamma}, \frac{L^2 \Delta^7 |\Sigma|^6 \tau^2}{\varepsilon^2}\right\}\right)$，通过确定性构造实现。
   - **平均误差**（定理 4.2）：在 Dirichlet 先验下，$N_0$ 对 $\varepsilon$ 的依赖为 $\varepsilon^{-2-2\alpha_0^{-1}}$，通过概率方法证明。
   - **两层无限精度**（定理 5.2）：$N \lesssim (\max(C(f), C(g))/\varepsilon)^{\max(1/\gamma, 3)}$，其中 $C(f)$ 是依赖第一层权重范数的复杂度度量，$\gamma(f)$ 是位置编码的最大间隔。

### 实验验证管线

为验证理论预测，论文在三个合成任务上进行了实验：

- **SimpleTask**：输出为 token 计数差的正弦函数，控制参数 ω 调节平滑度。
- **ModPTask**：输出为特定模等价类上 token 1 的比例，控制参数 Δ 即周期。
- **In-context k-gram**：在上下文中估计 k-gram 经验分布，控制参数为词表大小 S 和 k。

所有实验采用在线生成数据、μP 初始化、Adam 优化器。核心观测指标是测试损失随测试长度增长的**平台值（plateau）**：对于固定训练长度，测试损失随测试长度增加而趋于稳定；该平台值随训练长度增加而单调下降，随任务难度参数（ω、Δ、S、k）增加而上升。这些现象与理论预测的定性趋势一致，为“更长训练序列带来更好长度泛化”提供了实证支撑。

## 核心模块与公式推导

### 3.1 模型架构：极限Transformer

本文分析的Transformer被定义为“极限Transformer”（Limit Transformer），其核心在于允许上下文长度趋于无穷，从而为长度泛化提供统一的数学框架。模型的前向计算由以下模块构成：

**Token嵌入与位置嵌入**：输入序列 $x$ 中的每个token $x_i$ 被映射为初始表示
$$y_i^{(0)} = E_{x_i} + p_i$$
其中 $E_{x_i}$ 是token嵌入，$p_i$ 是位置嵌入。位置嵌入被假设满足两个关键性质：**$\Delta$-周期性**（$p_i = p_{i+\Delta}$ 对所有 $i$ 成立）和**平移不变性**（$\phi_{l,h}(j,i) = \phi_{l,h}(j+t,i+t)$ 对所有 $t$ 成立）。

**自注意力机制**：第 $l$ 层第 $h$ 个注意力头的logit计算为
$$a_{i,j}^{(l,h)} = (y_j^{(l-1)})^\top K_{l,h}^\top Q_{l,h} y_i^{(l-1)} + \phi_{l,h}(j,i)$$
其中 $\phi_{l,h}(j,i)$ 是仅依赖于位置 $j$ 和 $i$ 的标量偏置。注意力权重通过softmax归一化后，对值向量进行加权聚合。

**MLP与残差连接**：注意力输出经单隐藏层MLP和残差连接进一步变换，最终通过线性解嵌入层映射到输出logits。

### 3.2 有限精度注意力：从softmax到hardmax

有限精度是理解实际Transformer长度泛化的关键。本文假设所有中间计算量绝对值 $\leq 2^{-p}$ 的被舍入为0，其中 $p$ 是精度位数。

**Logit间隔 $\gamma(f)$**：定义为最小非零注意力logit差值
$$\gamma(f) := \min_{y \in \Sigma} \min_{a, a' \in \mathcal{A}_{(y,i)}} a - a'$$
其中 $\mathcal{A}_{(y,i)}$ 是处理token $x_i = y$ 时所有可能的注意力logit集合。$\gamma(f)$ 刻画了最大注意力logit与其他logit之间的最小差距。

**硬注意力阈值**：当序列长度 $N \geq 2^{p/\gamma(f)}$ 时，对于非最大注意力的位置，其softmax项满足
$$s_j = \exp(\log N \cdot (a - a^*)) \leq 2^{-p}$$
从而被舍入为0。这意味着**在足够长的序列上，有限精度softmax退化为硬注意力**（hardmax），即仅在argmax位置上均匀分配注意力权重。这一退化现象是定理4.1和4.2中 $2^{p/\gamma}$ 项的理论根源。

### 3.3 无限精度注意力：对数缩放的$\tau$-后缀

为避免有限精度下注意力退化的限制，本文进一步分析无限精度设定。此时，若权重矩阵有界，$\tau$-后缀（最近 $\tau$ 个token）的位置偏置对注意力的影响会随序列长度发散而衰减至零。

为解决此问题，提出对$\tau$-后缀的logit乘以 $\log i$ 进行缩放：
$$a_{i,j}^{(l,h)} = (y_j^{(l-1)})^\top K_{l,h}^\top Q_{l,h} y_i^{(l-1)} + \log i \cdot \phi_{l,h}(j,i)$$

这一缩放产生三种注意力模式：
1. **Token主导**：token相似度主导注意力
2. **平衡态**：token相似度与位置偏置共同作用
3. **位置主导**：位置偏置主导注意力

该设计使得Transformer能在任意长度序列上保持对局部上下文（$\tau$-后缀）和全局统计量（如经验频率 $\mu(x_{\leq i})_s = \frac{1}{i}\sum_{j=1}^i \mathbf{1}(x_j = s)$）的联合建模能力。

### 5.1 复杂度度量与位置间隔

对于两层无限精度Transformer，定义复杂度度量
$$C(f) := \exp\left(\operatorname{poly}\left(\{\|V_{1,h}\|,\|K_{1,h}^\top Q_{1,h}\|\}_{h\in[H]},\|A_1\|,\|B_1\|,\|K_{2,1}^\top Q_{2,1}\|\right)\right) \cdot \operatorname{poly}(\dots)$$
该度量取决于第一层权重范数和第二层注意力矩阵范数，直接决定定理5.2中训练长度上界的指数依赖。

**位置间隔 $\gamma(f)$**（与3.2节定义不同）：
$$\gamma(f) := \min_{h} \left(\max \mathcal{P}_h - \max\{p \in \mathcal{P}_h : p \neq \max\}\right)$$
即所有注意力头中，位置编码值的最大间隔的最小值。$\gamma(f)$ 越小，位置之间的区分越困难，所需训练长度越大。

### 5.3 核心仿真引理

长度泛化的理论基石是构造短序列 $z$ 来模拟长序列 $x$ 的行为。引理5.3通过随机子采样实现了这一目标：对于任意Lipschitz函数 $p$，存在子集 $\mathcal{T} \subset [T]$ 使得
$$\left\|\frac{1}{T}\sum_{t=1}^T p(x_{t-\tau:t}, \mu(x_{\leq t})) - \frac{1}{|z|}\sum_{t=1}^{|z|} p(z_{t-\tau:t}, \mu(z_{\leq t}))\right\| \lesssim \frac{(G+L)(\tau+1)}{n^{1/3}}$$
其中 $G$ 是函数 $p$ 的Lipschitz常数上界，$L$ 是Transformer的范数上界，$n$ 是子采样大小。该引理保证了短序列能够以任意精度逼近长序列在$\tau$-后缀和经验频率上的统计量，从而使得在短序列上训练一致的Transformer在任意长度上输出近似一致。

### 上下文k-gram估计器

定义5.4给出了上下文k-gram估计器的显式形式：
$$f^*(x_{1:T}) = \frac{\sum_{t=k+1}^T \mathbf{1}(x_{t-k:t-1}=x_{T-k+1:T}) \cdot \mathbf{e}_{x_t}}{\sum_{t=k+1}^T \mathbf{1}(x_{t-k:t-1}=x_{T-k+1:T})}$$
即对序列中所有与最后 $k-1$ 个token匹配的位置，统计其后继token的经验分布。这是定理5.2在上下文学习场景下的具体应用实例。

## 实验与分析

### 实验设置概述

论文在三个合成任务上验证了长度泛化的定量界限理论：**SimpleTask**、**ModPTask** 和 **In-context k-gram** 任务。所有实验采用在线生成数据，使用 μP 初始化与 Adam 优化器（超参数详见附录 C）。核心观测指标是测试损失（test loss）随测试长度和训练长度的变化行为。

### 主要实验结果

**SimpleTask（Figure 1）**：该任务的目标输出为 $f^*(x_{1:T}) = \sigma\left(\frac{c_0(x) - c_1(x)}{c_0(x) + c_1(x)}\right)$，其中 $\sigma(z) = \sin(\omega z)$。实验表明，对于固定的训练长度，随着测试长度增加，测试损失会**平台化（plateau）**到一个有限值，而非持续发散。更重要的是，该平台值随训练长度增加而**单调下降**，且随任务参数 $\omega$ 增大而上升。这与理论预测一致：更大的 $\omega$ 使函数对输入统计量的变化更敏感，从而需要更长的训练序列来充分模拟长序列的统计行为。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_TLSUIyBIfs/figures/001_Figure_1.jpg]]
*Figure 1: Experiments on SimpleTask. Left: Test loss as a function of test length and train length, for fixed ω. For each fixed train length, as test length increases, the test loss plateaus at a finite value. Right: Final test loss as a function of train length and ω. The value the test loss plateaus at decreases monotonically with train length, and increases monotonically with ω*

**ModPTask（Figure 2）**：该任务输出为 $f^*(x_{1:T}) = \frac{\sum_{t=1}^T \mathbf{1}(x_t=1, t\equiv k \bmod p)}{\sum_{t=1}^T \mathbf{1}(t\equiv k \bmod p)}$，即计算特定模类位置上 token 1 的比例。测试损失同样随测试长度增加而平台化，平台值随训练长度单调下降，随位置周期 $\Delta$ 增大而上升。Figure 3 进一步揭示了注意力模式：训练后的 softmax 注意力近似为硬注意力，在所有满足 $t \equiv k \bmod p$ 的位置上分配近似均匀的注意力权重，而在其他位置上注意力接近零。这直接验证了定理 4.1 的核心机制——有限精度下 softmax 退化为 hardmax，且短序列需能模拟长序列中硬注意力模式的 token 经验频率。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_TLSUIyBIfs/figures/002_Figure_2.jpg]]
*Figure 2: Experiments on ModPTask. Left: Test loss as a function of test length and train length, for fixed $\Delta$ . . For each fixed train length, as test length increases, the test loss plateaus at a finite value. Right: Final test loss as a function of train length and ∆. The value the test loss plateaus at decreases monotonically with train length, and increases monotonically with $\Delta$

**In-context k-gram（Figure 4）**：该任务要求在上下文中估计 k-gram 概率，目标函数为 $f^*(x_{1:T}) = \frac{\sum_{t=k+1}^T \mathbf{1}(x_{t-k:t-1}=x_{T-k+1:T}) \mathbf{e}_{x_t}}{\sum_{t=k+1}^T \mathbf{1}(x_{t-k:t-1}=x_{T-k+1:T})}$。实验显示测试损失平台值随训练长度增加而单调下降，且随词汇量 $S$ 或 k-gram 阶数 $k$ 增大而上升。这与定理 5.2 中界限对 $|\Sigma|$ 和上下文窗口 $\tau$ 的多项式依赖关系定性吻合：更大的 $S$ 和 $k$ 意味着需要模拟的统计量维度更高，从而要求更长的训练序列。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_TLSUIyBIfs/figures/003_Figure_4.jpg]]
*Figure 4: Experiments on the in-context k-gram task. Left: Test loss as a function of test length and train length, for fixed k and S. For each fixed train length, as test length increases, the test loss plateaus at a finite value. Middle: Final test loss as a function of train length and S , for fixed k . The value the test loss plateaus at decreases monotonically with training length, and increases with S. Right: Final test loss as a function of train length and k , for fixed S. The value the test loss plateaus at increases monotonically with k*

### 与理论的一致性分析

三条实验曲线共同支撑了论文的核心理论主张：

1. **平台化现象的存在**：所有任务中测试损失均不随测试长度无限增长，而是收敛到有限平台值，证实长度泛化确实发生，而非模型简单失效。
2. **训练长度的单调效应**：平台值随训练长度增加而单调下降，验证了定理 4.1 和定理 5.2 的核心结论——存在某个有限训练长度 $N$ 后即可实现长度泛化，且更大的 $N$ 带来更小的泛化误差。
3. **任务参数的定量影响**：$\omega$、$\Delta$、$S$、$k$ 等参数对平台值的影响方向与理论界限中的依赖关系一致，为界限中的多项式/指数依赖性提供了定性实证支持。

### 局限性与待验证问题

实验验证仍存在若干局限，需注意：

- **界限的紧致性未验证**：定理中给出的界限（如 $N = O(\max\{2^{p/\gamma}, L^2 \Delta^7 |\Sigma|^6 \tau^2/\varepsilon^2\})$）包含较大的常数和指数依赖，实验仅展示了定性趋势，未直接测试这些界限是否紧致。该点需要手动验证。
- **架构深度受限**：实验仅针对浅层 Transformer，未覆盖更深架构下的长度泛化行为，与理论分析的范围一致但限制了结论的推广性。
- **序列分布假设**：平均误差界限（定理 4.2）要求输入序列服从 Dirichlet 分布或 i.i.d. 分布，实验中是否严格满足该假设需进一步确认。

### 开放问题

论文提出了若干待解决问题，其中与实验直接相关的包括：定理中关于精度 $p$、周期 $\Delta$、词汇量 $|\Sigma|$ 的多项式或指数依赖性在实验中是否紧致；以及不同位置编码方案（如 Alibi、RoPE）对所需训练长度 $N$ 的定量影响，这需要后续实验进行系统比较。

## 方法谱系与知识库定位

### 问题定位与理论贡献边界

本文聚焦于Transformer长度泛化（Length Generalization, LG）的**定量刻画**，其核心贡献在于首次为“需要多长的训练序列才能实现长度泛化”这一开放问题提供了可证明的上下界。与已有理论工作的根本区别在于：先前工作仅证明**存在**某个有限训练长度后可实现长度泛化，但未给出该长度的具体量级或依赖关系。本文则通过构造性的模拟论证（simulation argument），将所需训练长度N显式表达为模型参数范数、词汇量|Σ|、位置编码周期Δ、局部窗口τ、数值精度p和允许误差ε的函数。

这一工作可定位于以下理论脉络的交叉点：

- **Transformer表达能力理论**：与Yun et al. (2019)、Pérez et al. (2021)等关于Transformer图灵完备性及序列到序列映射能力的工作相呼应，但本文关注的是“泛化到未见长度”这一更细粒度的能力边界。
- **长度泛化的机制理解**：与Anil et al. (2022)、Zhou et al. (2024)等关于位置编码方案（如Alibi、RoPE）对长度外推影响的实证研究形成理论互补——本文为这些实证现象提供了定量的理论语言。
- **随机子采样与概率方法**：定理5.2的证明技术（通过Markov链构造随机子采样序列z，再利用概率方法证明存在性）与经典理论计算机科学中的去随机化（derandomization）和采样复杂度分析有方法论上的亲缘关系。

### 适用边界与关键假设

本文的理论保证依赖于一系列明确的假设，这些假设同时界定了结论的适用范围：

1. **架构深度限制**：定理4.1和4.2针对单层Transformer，定理5.2扩展至两层。对于更深架构，作者明确指出需要将最小训练长度与C-RASP程序复杂度联系起来，这是当前工作的直接延伸方向。

2. **位置编码的特定结构**：假设位置编码满足Δ周期性、平移不变性和τ局部性（即只有最近τ个位置可通过位置嵌入相互区分）。这意味着结论不能直接迁移到RoPE等不具备严格周期性的方案上。

3. **精度模型的分立处理**：有限精度分析假设特定的舍入规则（将绝对值≤2^{-p}的量舍入为0），并导出logit margin γ(f)作为硬注意力阈值的关键参数；无限精度分析则要求对τ后缀logit进行对数缩放（乘以log i）以维持注意力在长序列上的非退化性。两种精度假设下的界限不可直接比较。

4. **序列分布的受限假设**：定理4.2的平均误差界限要求输入序列服从Dirichlet分布（或i.i.d.分布），未覆盖马尔可夫链等更一般的序列模型。作者将此列为开放问题。

5. **界限的紧致性未经验证**：定理中的界限包含对1/γ的指数依赖和对Δ、|Σ|的多项式依赖，常数因子较大。作者明确指出这些界限可能不反映实际所需的最小训练长度，其紧致性需要通过实验进一步验证。

### 局限与开放问题

**已识别的局限**：

- 仅覆盖单层和两层Transformer，深度扩展需要全新的技术工具（如与C-RASP程序的对应）。
- 位置编码假设较强（Δ周期性、平移不变性、τ局部性），对实践中常用的RoPE、Alibi等方案的覆盖不足。
- 有限精度分析中，logit margin γ(f)需在训练后测量，无法先验地给出N的估计。
- 平均误差界限对序列分布的假设较严格，实际语言数据的分布特性（如幂律、长程依赖）未被建模。

**明确的开放问题**：

1. **深度扩展与程序复杂度**：将结果推广到更深Transformer，并将最小训练长度N与C-RASP程序长度等复杂度度量建立定量联系。
2. **更一般的序列分布**：在马尔可夫链或更一般的随机过程下，建立长度泛化的平均情况条件。直觉上，若序列分布具有“快速混合”性质，短序列的统计量可能更快地逼近长序列，从而降低所需N。
3. **位置编码方案的定量影响**：系统刻画Alibi、RoPE、NoPE等不同位置编码方案对所需训练长度N的定量效应，为实践中的位置编码选择提供理论指导。
4. **界限紧致性验证**：通过实验检验定理中关于精度p、周期Δ、词汇量|Σ|的指数或多项式依赖是否紧致，或是否存在更紧的上界。
5. **多层无限精度界限的改进**：定理5.2的复杂度度量C(f)包含对权重范数的指数依赖，能否为无限精度下的多层Transformer给出更紧的复杂性与长度泛化界限。

### 在知识库中的定位

本文可作为连接Transformer理论分析与实证长度泛化研究的桥梁。对于后续工作，它提供了可操作的定量框架：若研究者希望证明某个特定任务或架构需要多长的训练序列才能泛化，可参照本文的模拟论证范式——构造一个从长序列到短序列的映射，使得短序列上的Transformer行为以可控误差逼近长序列上的行为，然后推导该映射所需的序列长度上界。同时，本文的局限性也为后续改进指明了方向：放宽位置编码假设、扩展至更深架构、覆盖更真实的序列分布。

## 原文 PDF

![[paperPDFs/ICLR_2026/Quantitative_Bounds_for_Length_Generalization_in_Transformers.pdf]]
