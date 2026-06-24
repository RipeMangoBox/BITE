---
title: "Semi-Supervised Preference Optimization with Limited Feedback"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Semi_Supervised_Preference_Optimization_with_Limited_Feedback.pdf
openreview_forum_id: ghwxbTx7do
aliases:
- SSPOS
- SSPOLF
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "利用奖励阈值将大量未配对数据伪标签化，并结合课程学习逐步纳入训练。"
primary_logic: "将偏好对齐重构为贝叶斯最优分类问题，通过奖励阈值在奖励空间中分离胜败响应，从而为未配对数据提供理论上有依据的伪标签。"
claims:
- "在仅有10个、50个、100个配对数据的玩具实验中，SSPO的测试准确率始终超过DPO、ORPO、SimPO等基线，尤其在数据稀缺时优势明显。"
- "在使用仅1% UltraFeedback训练Mistral-7B时，SSPO的AlpacaEval2.0长度控制胜率(LC)达到19.1%，超过使用10%数据训练的最强基线KTO的18.8%。"
- "UltraFeedback (AlpacaEval2.0) 上 LC (Length-Controlled Win Rate) = 19.1%"
- "UltraFeedback (AlpacaEval2.0) 上 WR (Raw Win Rate) = 18.7%"
---

# Semi-Supervised Preference Optimization with Limited Feedback

> [!tip] 核心洞察
> 将偏好对齐重构为贝叶斯最优分类问题，通过奖励阈值在奖励空间中分离胜败响应，从而为未配对数据提供理论上有依据的伪标签。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 有限反馈下的半监督偏好优化 |
| 英文题名 | Semi-Supervised Preference Optimization with Limited Feedback |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ghwxbTx7do); [GitHub](https://github.com/MLAI-Yonsei/SSPO) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Semi-Supervised Preference Optimization (SSPO) |
| Dataset | UltraFeedback (AlpacaEval2.0) |

> [!tip] 效果简介
> - UltraFeedback (AlpacaEval2.0) 上，LC (Length-Controlled Win Rate) 为 19.1%，对比 18.8% (KTO 10%)，变化 +0.3%。
> - UltraFeedback (AlpacaEval2.0) 上，WR (Raw Win Rate) 为 18.7%，对比 16.4% (KTO 10%)，变化 +2.3%。

## 概述

偏好优化是当前大语言模型对齐的核心技术，但其对大规模人工标注配对数据的依赖构成了关键瓶颈——数据获取成本高昂，领域扩展困难。现有方法如DPO、SimPO等仅能利用有限的配对比较数据，而大量未配对的响应数据（如监督微调数据）因缺乏偏好标签被直接丢弃，限制了泛化能力和数据效率。

本文提出的半监督偏好优化（Semi-Supervised Preference Optimization, SSPO）从贝叶斯最优分类的视角重构偏好学习问题，核心思路是利用配对数据上训练的奖励函数，通过奖励阈值在奖励空间中分离胜败响应，为未配对数据提供理论上可论证的伪标签。方法包含三个关键设计：基于核密度估计和贝叶斯风险最小化的阈值学习、对未配对数据的伪标签分配、以及通过自适应调度器实现从配对数据到伪配对数据的课程式学习过渡。

实验表明，SSPO在数据极度稀缺的场景下展现出显著优势。在仅有10个配对数据的玩具实验中，SSPO的测试准确率始终超过DPO、ORPO、SimPO等基线（Table 1）。在使用仅1% UltraFeedback训练Mistral-7B时，SSPO的AlpacaEval2.0长度控制胜率达到19.1%，超过使用10%数据训练的最强基线KTO的18.8%（Table 2），以1%的数据量实现了超越10%数据量基线的性能。

## 背景与动机

大语言模型的对齐训练通常依赖人类偏好标注的配对比较数据。现有偏好优化方法（如 DPO、SimPO、ORPO）直接在这类配对数据上优化策略模型，其性能高度依赖于配对数据的规模与质量。然而，获取大规模高质量人工偏好标注的成本极为高昂，严重制约了偏好优化方法在更广泛领域中的扩展与应用。这一瓶颈的本质在于：**偏好优化对大规模人工标注配对数据的依赖，导致数据获取成本高昂、领域扩展困难**。

在实际场景中，大量未配对的高质量响应（例如来自监督微调数据集的单条回答）虽然被广泛使用，却因缺少偏好标签而被现有方法直接丢弃。这些数据中隐含着丰富的偏好信号——例如，某些回答在格式、完整性或事实准确性上天然优于另一些——但如何从这些无标签数据中提取有效的偏好信息，一直缺乏理论上有依据的方法。

SSPO 的核心动机正是打破这一限制：**将偏好对齐重构为贝叶斯最优分类问题，通过奖励阈值在奖励空间中分离胜败响应，从而为未配对数据提供理论上有依据的伪标签**。具体而言，SSPO 利用在少量配对数据上训练得到的奖励函数，通过贝叶斯风险最小化确定一个动态奖励阈值，将高于阈值的未配对响应标记为“伪胜出”，低于阈值的标记为“伪失败”，从而将大量未配对数据转化为可用的伪配对训练信号。这一框架使得策略模型能够同时从有限的精确标注和大量自动标注的数据中学习，在保持标注效率的同时显著提升对齐质量。

## 核心创新

SSPO 的核心创新在于将偏好优化重新构建为**贝叶斯最优分类问题**，从而为大量未配对数据提供理论上可论证的伪标签策略。这一重构带来了三个关键的 changed slots，使其在有限配对数据场景下显著超越现有基线。

### 从偏好对齐到二元分类的范式转换

传统方法（DPO、SimPO 等）仅利用人工标注的配对数据 $D_L$ 进行优化，丢弃了丰富的未配对响应。SSPO 将偏好分类器建模为 Bradley-Terry 形式：

$$f _ { \theta } ( x , y , y ^ { \prime } ) : = \sigma ( r _ { \theta } ( x , y ) - r _ { \theta } ( x , y ^ { \prime } ) ) \cdot \mathbb { P } ( s = 1 ) + \sigma ( r _ { \theta } ( x , y ^ { \prime } ) - r _ { \theta } ( x , y ) ) \cdot \mathbb { P } ( s = 0 )$$

其中 $r_\theta(x,y)$ 默认采用 SimPO 的奖励形式。这一转换使得偏好学习的目标变为最小化分类期望风险，为未配对数据的利用提供了概率基础。

### 基于奖励阈值的伪标签策略

SSPO 的核心 changed slot 在于**数据使用方式**：它不仅使用配对数据 $D_L$，还通过奖励阈值将未配对数据 $D_U$ 伪标签化后纳入训练。其理论基础是：胜出响应和失败响应在奖励空间中应当可分离。最优阈值 $\delta^*$ 通过最小化贝叶斯风险确定：

$$R ( \delta ) = \mathbb { P } ( s = 1 ) \cdot \int _ { - \infty } ^ { \delta } p ( r \mid s = 1 ) d r + \mathbb { P } ( s = 0 ) \cdot \int _ { \delta } ^ { \infty } p ( r \mid s = 0 ) d r$$

实践中，SSPO 使用核密度估计（KDE）从配对数据的奖励分布中估计该阈值，并通过指数移动平均（EMA）稳定奖励统计量。每个未配对响应的伪标签由标准化奖励与阈值的比较决定：

$$\tilde { s } _ { k } = \mathbb { I } \left\{ r _ { \theta } ( x _ { u } ^ { ( k ) } , y _ { u } ^ { ( k ) } ) > \hat { \delta } \right\}$$

### 自适应课程学习的联合优化

第三个关键 changed slot 是**损失函数**的扩展。SSPO 联合最小化配对数据风险和伪配对交叉熵风险，并通过自适应调度器动态调节两者权重：

$$\mathcal { L } ( f _ { \theta } ) = \gamma ^ { \prime } \cdot R _ { D _ { L } } ( f _ { \theta } ) + ( 1 - \gamma ^ { \prime } ) \cdot R _ { D _ { U } } ( f _ { \theta } ) \quad \mathrm { s . t . } \quad \gamma ^ { \prime } = \operatorname* { m a x } \left\{ \gamma _ { \mathrm { m i n } } , \gamma _ { 0 } \cdot \exp ( - \lambda \tau ) \right\}$$

该调度器实现了课程学习动态：训练初期 $\gamma' \approx 1$，模型专注于从高质量人工标注中学习；随着训练推进，$\gamma'$ 指数衰减至 $\gamma_{\min}$，模型逐渐将学习重心转移到伪标签化的未配对数据上。消融实验（Table 4）证实了这一设计的必要性：Mistral 在 1% 数据上使用自适应调度器时 LC 达到 26.7%，而固定 $\gamma=0.1$ 时仅为 24.1%。

### 创新点的协同效应

这三个 changed slots 形成了一条完整的因果链：**分类视角** → **阈值伪标签** → **课程联合优化**。其效果在极端数据稀缺场景下尤为突出：使用仅 1% UltraFeedback 训练 Mistral-7B 时，SSPO 的 AlpacaEval2.0 长度控制胜率（LC）达到 19.1%，超过使用 10% 数据训练的最强基线 KTO 的 18.8%（Table 2）。在仅有 10 个配对数据的玩具实验中，SSPO 的测试准确率（0.757）也显著优于 SimPO（0.647）和 DPO（0.618）（Table 1），验证了伪标签策略在数据稀缺时的有效性。

## 整体框架

![[assets/figures/papers/iclr26_0009_ghwxbTx7do_Semi-Supervised_Preference_Optimization_with_Lim/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the SSPO framework. Existing preference optimization methods, such as DPO and SimPO, rely solely on a limited number of human-labeled comparisons. These methods discard abundant unpaired responses (e.g., supervised fine-tuning data) due to the lack of preference labels, which hinders generalization and data efficiency. SSPO leverages a reward function trained on labeled comparisons to assign pseudo-labels to unpaired responses. Responses above a learned threshold are treated as (pseudo) winning, and those below as (pseudo) losing. Hence, the policy model optimizes the reward threshold using both labeled and pseudo-labeled data, thereby improving alignment quality and generalizat...*

SSPO 将偏好对齐重构为一个贝叶斯最优分类问题，其核心 pipeline 包含六个串联模块，形成“奖励计算→统计跟踪→阈值估计→伪标签分配→损失计算→自适应加权”的闭环。

**输入与输出流**：系统接受两类数据——少量人工标注的配对偏好数据 $D_L$（包含胜出响应 $y_w$ 和败者响应 $y_l$）以及大量无偏好标签的未配对数据 $D_U$（仅包含提示 $x_u$ 和响应 $y_u$）。输出为经过偏好优化的策略模型 $\pi_\theta$。

**模块关系**：

1. **Reward computation**：对每个响应计算 SimPO 形式的奖励函数 $r_\theta(x, y) = \frac{\beta}{|y|} \log \pi_\theta(y \mid x)$。该奖励值直接驱动后续所有模块。

2. **Statistics update**：使用指数移动平均（EMA，动量 $m=0.95$）跟踪配对数据中胜/败响应奖励的均值 $\mu_t$ 与标准差 $\sigma_t$，以稳定训练过程中的奖励分布漂移。

3. **Threshold estimation**：在配对数据上，通过高斯核密度估计（KDE）分别拟合胜出和败出响应的奖励分布 $\hat{p}_w(r)$ 和 $\hat{p}_l(r)$，然后最小化贝叶斯风险 $R(\delta)$ 得到最优奖励阈值 $\hat{\delta}$。该阈值是分离“胜”与“败”的决策边界。

4. **Pseudo-label assignment**：将未配对数据的标准化奖励与阈值比较：$r_\theta(x_u, y_u) > \hat{\delta}$ 则分配伪标签 $\tilde{s}=1$（伪胜出），否则 $\tilde{s}=0$（伪败出）。这一策略由贝叶斯风险最小化理论保证。

5. **Loss computation**：分别计算配对数据的交叉熵风险 $R_{D_L}(f_\theta)$ 和伪配对数据的交叉熵风险 $R_{D_U}(f_\theta)$。

6. **Adaptive weighting**：通过指数衰减调度器 $\gamma' = \max\{\gamma_{\min}, \gamma_0 \cdot \exp(-\lambda \tau)\}$ 动态调节两者权重。训练初期 $\gamma' \approx 1$，模型主要从高质量人工标注中学习；随着训练步数 $\tau$ 增加，$\gamma'$ 衰减至 $\gamma_{\min}$，学习重心逐步转移到伪标签化的未配对数据上，形成课程学习效果（Figure 2）。

**瓶颈与因果机制**：传统偏好优化方法（DPO、SimPO 等）仅使用配对数据 $D_L$，丢弃了大量未配对响应，在标注数据稀缺时泛化能力受限。SSPO 的关键因果杠杆在于：利用配对数据训练出的奖励函数在奖励空间中分离胜败分布，从而为未配对数据提供有理论依据的伪标签，将数据效率的瓶颈从“标注量”转移到“奖励分布的可分离性”上。

## 核心模块与公式推导

SSPO 将偏好优化重构为贝叶斯最优分类问题，其核心由六个模块串联：奖励计算、统计量更新、阈值估计、伪标签分配、损失计算与自适应加权。整个流程的数学基础建立在 Bradley-Terry 偏好分类器之上。

### 偏好分类器与配对数据风险

SSPO 将偏好预测建模为一个期望分类器。给定提示 $x$ 和两个响应 $y$、$y'$，偏好分类器 $f_\theta(x, y, y')$ 定义为：

$$f _ { \theta } ( x , y , y ^ { \prime } ) : = \sigma ( r _ { \theta } ( x , y ) - r _ { \theta } ( x , y ^ { \prime } ) ) \cdot \mathbb { P } ( s = 1 ) + \sigma ( r _ { \theta } ( x , y ^ { \prime } ) - r _ { \theta } ( x , y ) ) \cdot \mathbb { P } ( s = 0 )$$

其中 $\sigma(\cdot)$ 为 sigmoid 函数，$s$ 为偏好标签（$s=1$ 表示 $y$ 胜出），$\mathbb{P}(s=1)$ 为先验胜率。奖励函数 $r_\theta(x, y)$ 默认采用 SimPO 形式：

$$r_\theta(x, y) = \frac{\beta}{|y|} \log \pi_\theta(y \mid x)$$

其中 $\beta$ 为温度系数，$|y|$ 为响应长度，$\pi_\theta$ 为策略模型。该奖励形式天然具有长度归一化特性，抑制冗长偏差。

在配对人标注数据 $D_L = \{(x^{(j)}, y_w^{(j)}, y_l^{(j)})\}_{j=1}^{n_L}$ 上，期望风险为：

$$R _ { D _ { L } } ( f _ { \theta } ) = \mathbb { E } _ { D _ { L } } \Bigg [ - \log \sigma \left( \frac { \beta } { | y _ { w } | } \log \pi _ { \theta } ( y _ { w } \mid x ) - \frac { \beta } { | y _ { l } | } \log \pi _ { \theta } ( y _ { l } \mid x ) - \Delta \right) \Bigg ]$$

其中 $\Delta$ 为边际项，$y_w$ 和 $y_l$ 分别为胜出和失败响应。该风险函数是传统偏好优化（如 SimPO）的核心，但仅利用配对数据。

### 贝叶斯风险最小化阈值

SSPO 的关键创新在于为未配对数据分配伪标签。设未配对数据集 $D_U = \{(x_u^{(k)}, y_u^{(k)})\}_{k=1}^{n_U}$，每个响应仅有一个奖励值 $r_\theta(x_u, y_u)$，缺乏胜败对比。SSPO 通过奖励阈值 $\delta$ 将响应二分为伪胜出（奖励 $> \delta$）和伪失败（奖励 $\le \delta$）。

阈值选择的理论依据是贝叶斯风险最小化。设 $p(r \mid s=1)$ 和 $p(r \mid s=0)$ 分别为胜出和失败响应的奖励分布，使用阈值 $\delta$ 作为硬决策边界的分类误差总概率为：

$$R ( \delta ) = \mathbb { P } ( s = 1 ) \cdot \int _ { - \infty } ^ { \delta } p ( r \mid s = 1 ) d r + \mathbb { P } ( s = 0 ) \cdot \int _ { \delta } ^ { \infty } p ( r \mid s = 0 ) d r$$

第一项为胜出响应被误判为失败的概率，第二项为失败响应被误判为胜出的概率。最优阈值 $\delta^* = \arg\min_{\delta \in \mathbb{R}} R(\delta)$ 在奖励空间中分离两类分布。

实践中，$p(r \mid s=1)$ 和 $p(r \mid s=0)$ 未知。SSPO 在配对数据 $D_L$ 上使用高斯核密度估计（KDE）来近似：

$$\hat { p } _ { w } ( r ) = \frac { 1 } { n _ { L } \cdot h } \sum _ { j = 1 } ^ { n _ { L } } K \left( \frac { r - r _ { \theta } ( x ^ { ( j ) } , y _ { w } ^ { ( j ) } ) } { h } \right)$$

其中 $K(\cdot)$ 为高斯核，$h$ 为带宽。对失败响应同理可得 $\hat{p}_l(r)$。代入后得到可计算的阈值估计：

$$\hat { \delta } = \operatorname { a r g m i n } _ { \delta \in \mathbb { R } } \hat { R } ( \delta ) , \mathrm { ~ w h e r e ~ } \hat { R } ( \delta ) = \mathbb { P } ( s = 1 ) \cdot \int _ { - \infty } ^ { \delta } \hat { p } _ { w } ( r ) d r + \mathbb { P } ( s = 0 ) \cdot \int _ { \delta } ^ { \infty } \hat { p } _ { l } ( r ) d r$$

### 伪标签分配与未配对数据风险

获得阈值 $\hat{\delta}$ 后，对每个未配对响应分配伪标签：

$$\tilde { s } _ { k } = \mathbb { I } \left\{ r _ { \theta } ( x _ { u } ^ { ( k ) } , y _ { u } ^ { ( k ) } ) > \hat { \delta } \right\}$$

即奖励高于阈值判为伪胜出（$\tilde{s}_k = 1$），否则为伪失败（$\tilde{s}_k = 0$）。未配对数据上的伪标签风险为：

$$R _ { D _ { U } } ( f _ { \theta } ) = \frac { 1 } { n _ { U } } \sum _ { k = 1 } ^ { n _ { U } } \ell ( f _ { \theta } , \tilde { s } _ { k } ) \cdot \mathbb { P } _ { D _ { U } } ( s = \tilde { s } _ { k } )$$

其中 $\ell$ 为交叉熵损失，$\mathbb{P}_{D_U}(s = \tilde{s}_k)$ 为先验置信度权重。

### EMA 统计量更新与训练稳定性

由于奖励函数 $r_\theta$ 在训练过程中持续变化，直接使用当前批次的奖励估计阈值会引入不稳定。SSPO 采用指数移动平均（EMA）跟踪奖励的全局均值 $\mu_t$ 和标准差 $\sigma_t$：

$$\mu_t = m \cdot \mu_{t-1} + (1 - m) \cdot \mu_B, \quad \sigma_t = m \cdot \sigma_{t-1} + (1 - m) \cdot \sigma_B$$

其中 $\mu_B$、$\sigma_B$ 为当前批次的统计量，动量参数 $m = 0.95$。伪标签分配前先将奖励标准化为 $(r - \mu_t) / \sigma_t$，再进行阈值比较。KDE 阈值 $\hat{\delta}_B$ 也在每个批次上重新估计，作为全局贝叶斯风险最小化器的迷你批次近似。

### 自适应加权与课程学习

最终训练目标联合优化配对风险与伪配对风险：

$$\mathcal { L } ( f _ { \theta } ) = \gamma ^ { \prime } \cdot R _ { D _ { L } } ( f _ { \theta } ) + ( 1 - \gamma ^ { \prime } ) \cdot R _ { D _ { U } } ( f _ { \theta } ) \quad \mathrm { s . t . } \quad \gamma ^ { \prime } = \operatorname* { m a x } \left\{ \gamma _ { \mathrm { m i n } } , \gamma _ { 0 } \cdot \exp ( - \lambda \tau ) \right\}$$

其中 $\tau$ 为训练步数，$\gamma_0 = 1$，$\lambda$ 为衰减率。调度器 $\gamma'$ 从 1 指数衰减至 $\gamma_{\min}$，实现课程学习动态：训练初期 $\gamma' \approx 1$，模型主要从高质量人工标注的配对数据学习，建立可靠的奖励函数；随着训练推进，$\gamma'$ 减小，模型逐步纳入伪标签化的未配对数据，扩大有效训练规模。消融实验（Table 4）表明，该自适应调度器是 SSPO 性能的关键——固定 $\gamma' = 0.1$ 时 Mistral 在 1% 数据上的 LC 仅为 24.1%，而使用调度器后提升至 26.7%。

## 实验与分析

### 玩具实验：数据稀缺下的性能优势

为验证SSPO在极端数据稀缺条件下的有效性，作者构建了一个可控的玩具实验。该实验的核心结论是：**SSPO在配对数据极少时（n_L=10）展现出远超所有基线的测试准确率，且优势随噪声水平升高而更加显著**。

具体而言，在无噪声条件下，当仅使用10个配对样本时，SSPO的测试准确率达到0.841，而最强基线SimPO仅为0.762（Table 1, Table 6）。当配对数据中混入50%噪声时，SSPO仍保持0.757的准确率，相比之下SimPO降至0.645，DPO降至0.653。这一差距的因果机制在于：SSPO通过奖励阈值将大量未配对数据伪标签化并纳入训练，有效弥补了配对监督信号的不足；而基线方法完全依赖有限的（且有噪声的）配对数据，难以学到可靠的偏好边界。

![[assets/figures/papers/iclr26_0009_ghwxbTx7do_Semi-Supervised_Preference_Optimization_with_Lim/figures/002_Table_1.jpg]]
*Table 1: Comparison of test accuracy on toy dataset without or with noise in paired data. SSPO consistently and significantly outperforms all baselines across different quantities of paired data*

随着配对数据量增加（n_L=50，n_L=100），SSPO的优势虽有所收窄，但仍保持领先。这表明伪标签策略在数据极稀缺时提供了关键的额外学习信号，是性能提升的核心瓶颈突破点。

### 真实数据主结果：1%配对数据超越10%基线

在真实场景实验中，SSPO的核心主张得到了强有力的验证：**使用仅1% UltraFeedback配对数据训练的Mistral-7B，其AlpacaEval2.0长度控制胜率（LC）达到19.1%，超过了使用10%数据训练的最强基线KTO的18.8%**（Table 2）。这一结果是整个工作的决定性证据，直接支撑了“半监督偏好优化显著提升数据效率”的核心论点。

![[assets/figures/papers/iclr26_0009_ghwxbTx7do_Semi-Supervised_Preference_Optimization_with_Lim/figures/003_Table_2.jpg]]
*Table 2: Performance of AlpacaEval2.0(%) and MT-Bench. LC and WR denote length-controlled and raw win rates for AlpacaEval2.0, and MT is the average MT-Bench score. With just 1% of paired data, SSPO often achieves higher scores than baselines trained on 10% of the data, exhibiting its data efficiency and effectiveness. The best numbers are in bold, and the second-best ones are underlined*

更广泛地看，SSPO在三个模型规模（Phi-2 2.7B、Mistral 7B、Llama3 8B）和三个领域（UltraFeedback、UltraMedical-Preference、DSP Business）上均表现出系统性优势。以Mistral为例，SSPO在1%数据下的原始胜率（WR）为18.7%，而KTO在10%数据下仅为16.4%，差距达2.3个百分点。在MT-Bench平均分上，SSPO同样以7.8分超过KTO的7.7分。

值得注意的失败模式是：在Phi-2小模型上，SSPO的绝对性能仍然较低（1%数据下LC仅为4.9%），说明伪标签质量受限于基座模型的奖励表达能力。此外，评估使用GPT-4-Turbo作为评判模型，存在模型偏好偏差；论文通过长度控制胜率（LC）抑制冗长偏差，但无法完全消除评判噪声。

### 消融研究：自适应调度器是关键使能组件

消融实验揭示了SSPO方法中一个关键的因果旋钮：**自适应调度器对性能至关重要**。Table 4显示，Mistral在1% UltraFeedback数据上，使用自适应调度器时LC达到26.7%，而将权重固定为γ=0.1时仅24.1%，固定为γ=0.5时更低至23.3%。即使固定调度器的最优表现（γ=0.1），仍低于自适应版本2.6个百分点。

![[assets/figures/papers/iclr26_0009_ghwxbTx7do_Semi-Supervised_Preference_Optimization_with_Lim/figures/005_Table_4.jpg]]
*Table 4: SSPO Performance with or without the adaptive scheduler. ✓ denotes the case with adaptive scheduling, while ✗ indicates the case without it. The adaptive scheduler unlocks the method’s full potential and consistently achieves stronger performance than baselines, even when the $\gamma ^ { \prime }$ is fixed

这一现象的内在机制可通过Figure 2（损失贡献比曲线）理解：训练初期，调度器使模型主要学习配对数据（γ'接近1），建立起可靠的奖励基础；随着训练推进，γ'指数衰减，伪配对数据的损失贡献逐步上升，模型开始从大量未配对数据中提取偏好信号。这种“先打好基础，再扩展学习”的课程学习动态，是SSPO能够稳定利用未配对数据的关键。

![[assets/figures/papers/iclr26_0009_ghwxbTx7do_Semi-Supervised_Preference_Optimization_with_Lim/figures/006_Figure_2.jpg]]
*Figure 2: Loss Contribution Ratio. (Mistral trained on 1% of UltraFeedback) This illustrates how the adaptive scheduler shifts the model’s learning focus from paired data (cyan) to pseudo-labeled unpaired data (red), enabling effective and robust learning*

若缺少自适应调度，模型要么过度依赖有限的配对数据（γ过大），导致未配对数据的价值无法释放；要么过早引入噪声伪标签（γ过小），破坏早期奖励函数的学习。

### 敏感性分析：先验概率选择稳健

SSPO的伪标签分配依赖于先验概率P(s=1)的设定。Table 3的敏感性分析表明：**SSPO对先验值的选择具有较好的鲁棒性**。在Mistral上使用10% UltraFeedback数据训练时，先验值从0.1到0.9变化，LC波动范围在28.3%到30.0%之间，最优值出现在先验0.5处（LC=30.0%）。即使采用次优先验0.1，SSPO的LC（28.3%）仍超过所有基线的10%数据最佳结果（KTO 18.8%），说明方法的性能优势不依赖于精细的先验调参。

![[assets/figures/papers/iclr26_0009_ghwxbTx7do_Semi-Supervised_Preference_Optimization_with_Lim/figures/004_Table_3.jpg]]
*Table 3: SSPO performance when varying the assumed prior. We measure the LC and WR for models trained on 10% of UltraFeedback. SSPO remains robust even under suboptimal priors, consistently outperforming baselines*

不过，先验选择确实影响伪标签分布：先验偏向0或1时，阈值会相应偏移，导致更多响应被标记为单一类别，削弱未配对数据的多样性利用。论文建议默认使用无信息先验0.5，这与实验结果一致。

### 定性案例：未配对数据的语义迁移

Table 5和Table 14的案例研究表明，SSPO不仅从伪标签中获得偏好信号，还能从高质量未配对数据中学习到风格和结构特征。例如，在DSP Business领域，KTO基线输出非结构化的关键词堆砌，而SSPO生成的回复采用了专业化的枚举格式，与未配对数据中高质量回复的风格一致。这说明**伪标签机制不仅传递了偏好方向，还隐式地实现了语义和格式的迁移学习**。

### 局限性说明

尽管实验结果整体正面，但需注意以下限制：
1. **伪标签质量依赖配对数据**：当配对数据极少（如n_L=10）时，奖励函数本身可能不准确，导致阈值估计不稳定，伪标签噪声增大。
2. **未覆盖所有领域**：实验仅限于UltraFeedback、UltraMedical和DSP Business三个数据集，在其他领域（如代码、数学推理）的有效性需手动验证。
3. **未验证多模态场景**：所有实验均为文本偏好对齐，方法在多模态或复杂多轮对话中的表现未经验证。

## 方法谱系与知识库定位

### 在偏好优化方法谱系中的位置

SSPO 处于**直接偏好优化（DPO）** 与**半监督学习**的交叉点上。DPO 及其变体（SimPO、ORPO）将偏好对齐建模为成对比较问题，但都严格依赖已标注的偏好配对数据 $D_L$。SSPO 的核心突破在于：将偏好对齐重构为**贝叶斯最优分类问题**，从而为大量未配对数据 $D_U$ 提供有理论依据的伪标签分配机制。

具体而言，SSPO 默认采用 SimPO 的奖励形式：
$$r_{\theta}(x, y) = \frac{\beta}{|y|} \log \pi_{\theta}(y \mid x)$$
并在此基础上构建 Bradley-Terry 偏好分类器。与 KTO（Kahneman-Tversky Optimization）不同，KTO 虽然也能处理未配对信号，但其建模基于前景理论的非对称价值函数，缺乏明确的奖励分布分离理论；SSPO 则通过**奖励阈值 $\hat{\delta}$** 在奖励空间中显式分离胜败响应，伪标签分配具有贝叶斯风险最小化的理论保障。

与 SSRM（半监督奖励建模）和 SPA（Spread Preference Annotation）相比，SSPO 的区别在于：SSRM 侧重于训练独立的奖励模型，而 SSPO 直接优化策略模型；SPA 通过扩散标注扩展配对数据，SSPO 则是利用已有未配对数据中的隐式偏好信号。

### 适用边界

**数据场景**：SSPO 在配对数据极度稀缺（如 1% UltraFeedback）时优势最为显著。在玩具实验中，$n_L=10$ 时 SSPO 的测试准确率达到 0.757，远超 SimPO 的 0.675（Table 1）。在真实场景中，Mistral-7B 仅用 1% 配对数据训练时，AlpacaEval2.0 长度控制胜率（LC）达到 19.1%，超过使用 10% 数据训练的最强基线 KTO 的 18.8%（Table 2）。

**适用条件**：
- 存在大量与配对数据**语义相关**的未配对响应（如 SFT 数据），这些响应中蕴含隐式偏好信号
- 配对数据量足以训练出能够区分胜败奖励分布的奖励函数——这是伪标签质量的基础
- 未配对数据的领域与配对数据基本一致，否则奖励分布分离假设可能失效

**不适用场景**：
- 配对数据极少（如 $n_L < 10$）且质量低下时，KDE 估计的阈值可能不稳定
- 未配对数据与配对数据域严重不匹配时，伪标签可能引入系统性噪声
- 多模态或复杂多轮对话场景尚未验证

### 局限与开放问题

**已知局限**：

1. **伪标签质量依赖配对数据**：SSPO 的阈值 $\hat{\delta}$ 通过核密度估计从 $D_L$ 的奖励分布中学习。当 $D_L$ 极小或噪声较高时，奖励分布估计可能不稳定，导致伪标签噪声增加。消融实验显示，自适应调度器能缓解但不完全消除此问题（Table 4：固定 $\gamma=0.1$ 时 LC 从 26.7 降至 24.1）。

2. **先验概率的敏感性**：$\mathbb{P}(s=1)$ 的选择影响伪标签分布。尽管 Table 3 显示 SSPO 对先验值具有鲁棒性（先验 0.1 到 0.9 之间性能波动有限），但最优先验（0.5）的选择仍需要领域知识或调参。

3. **评估范围有限**：实验仅在 UltraFeedback、UltraMedical、DSP Business 三个文本数据集上进行，使用 GPT-4-Turbo 作为评判模型。未覆盖对话、代码生成、多模态等场景。

4. **计算开销**：SSPO 每步需要额外计算 KDE 阈值和 EMA 统计量更新。Table 9（附录）给出了各配置下的训练吞吐量，但相对于 SimPO 等基线有可测量的额外开销。

**开放问题**：

- **阈值学习的自动化**：当前依赖 KDE 和 EMA 的手动设计，能否通过在线自适应方法（如元学习）自动调整阈值，减少对配对数据分布的依赖？
- **极低信噪比场景**：当未配对数据中隐式偏好信号极弱时，SSPO 是否仍能提取有效信息？这需要更系统的噪声鲁棒性研究。
- **多轮与多模态扩展**：Bradley-Terry 分类框架能否自然扩展到多轮对话偏好或多模态对齐任务？奖励空间的分离假设在这些场景下是否仍然成立？
- **伪标签置信度建模**：当前伪标签是硬分配（高于阈值为胜，低于为败）。能否引入软标签或置信度加权机制，更精细地建模伪标签的不确定性，进一步降低噪声影响？
- **与 SFT 的深度融合**：Table 10 显示 SSPO 优于 DPO+SFT 和 SimPO+SFT 的简单组合。能否在统一框架内更紧密地融合监督微调和偏好优化的目标？

## 原文 PDF

![[paperPDFs/ICLR_2026/Semi_Supervised_Preference_Optimization_with_Limited_Feedback.pdf]]
