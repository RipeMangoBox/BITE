---
title: "Adaptive Conformal Guidance for Learning under Uncertainty"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Adaptive_Conformal_Guidance_for_Learning_under_Uncertainty.pdf
project_link: null
code_link: null
aliases:
- ACGA
- ACGLUU
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "AdaConG用分裂共形预测估计引导信号不确定性，并以单调权重重加权引导损失。"
primary_logic: "校准集先生成预测集大小作为不确定性，再把该不确定性映射为权重并合入任务训练目标。"
claims:
- "共形预测提供分布无关的不确定性信号，用于降低噪声教师、伪标签或模仿策略的影响。"
- "AdaConG无需改动模型架构，可嵌入知识蒸馏、半监督学习和模仿引导强化学习。"
- "在CIFAR知识蒸馏、半监督分类、网格世界和转向预测中，AdaConG带来一致性能提升。"
---

# Adaptive Conformal Guidance for Learning under Uncertainty

> [!tip] 核心洞察
> 利用分裂共形预测（split conformal prediction）量化引导信号的不确定性，并将不确定性映射为自适应权重，动态调节引导损失在总损失中的贡献。高不确定性对应低权重，从而减少对不可靠引导的依赖，同时保留有用信息。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向不确定性学习的自适应共形引导 |
| 英文题名 | Adaptive Conformal Guidance for Learning under Uncertainty |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=1gxP0WtOoO) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Adaptive Conformal Guidance (AdaConG) |
| Dataset | CIFAR-100 (同构结构, 域偏移), CIFAR-10 (40 labels), CIFAR-100 (2500 labels), CIFAR-100 (400 labels) |

> [!tip] 效果简介
> - CIFAR-100 (同构结构, 域偏移) 上，Top-1 准确率 (%) 为 KD+AdaConG: 65.71±0.36 (ResNet50/ShuffleNet-V1)，对比 KD: 54.82±0.28，变化 +10.89。
> - CIFAR-10 (40 labels) 上，Top-1 准确率 (%) 为 FixMatch+AdaConG: 93.12±0.32，对比 FixMatch: 87.14±0.45，变化 +5.98。
> - CIFAR-100 (2500 labels) 上，Top-1 准确率 (%) 为 FlexMatch+AdaConG: 67.85±0.28，对比 FlexMatch: 62.22±0.35，变化 +5.63。

## 概要

本文提出 **Adaptive Conformal Guidance (AdaConG)**，一种通用且轻量的框架，旨在解决学习系统中引导信号（如教师模型输出、伪标签、模仿策略）不可靠时带来的性能下降问题。AdaConG 的核心思想是利用分裂共形预测（split conformal prediction）量化引导信号的不确定性，并将该不确定性映射为自适应权重，动态调节引导损失在总损失中的贡献。该方法适用于监督学习、半监督学习和模仿引导的强化学习等多种场景。实验表明，AdaConG 在知识蒸馏、半监督图像分类、网格世界导航和自动驾驶转向预测等任务中均能显著提升性能，例如在 CIFAR-100 知识蒸馏任务中最高提升 +10.89% 的 Top-1 准确率，在网格世界导航中收敛后奖励超过最强基线的 6 倍。

现有学习系统在依赖引导信号时，通常假设引导始终可靠。然而，由于域偏移、有限数据或策略泛化不足，引导信号常带有噪声或不确定性。盲目信任这些信号会导致性能下降甚至错误传播。例如，在知识蒸馏中，教师模型在域偏移下可能产生误导性输出；在半监督学习中，伪标签可能包含大量噪声；在模仿引导的强化学习中，教师策略可能因环境变化而失效。因此，亟需一种能够动态评估引导信号可靠性并据此调整其影响的方法。

## 核心方法与创新机理

AdaConG 的核心创新在于：

1. **基于共形预测的不确定性量化**：利用分裂共形预测（split CP）计算引导信号的预测集大小，并将其归一化为不确定性度量 u(x)。与启发式方法（如熵、最大 softmax 概率）或后验校准不同，共形预测提供了分布无关的覆盖保证。

2. **自适应权重生成**：将不确定性 u(x) 通过单调递减函数 h 映射为自适应权重 w(x) = h(u(x))，例如指数衰减 w = exp(-γ u)。高不确定性对应低权重，从而减少对不可靠引导的依赖，同时保留有用信息。

3. **通用框架**：AdaConG 可无缝集成到监督学习、半监督学习和强化学习的训练循环中，仅需修改引导损失的加权方式，无需改变模型架构。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_1gxP0WtOoO_Adaptiv/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the AdaConG approach. AdaConG leverages split CP with calibration to quantify the uncertainty of guidance signals and adaptively modulate their influence. The estimated uncertainty u is converted into an adaptive weight w, which reweights the guidance loss. This weighted guidance loss is then combined with the task loss to update the model, enabling effective learning under uncertain guidance.*

AdaConG 的整体框架如 Figure 1 所示。该框架包含三个核心模块：

1. **分裂共形预测校准模块**：使用校准集计算非一致性分数分位数，构建预测集，量化引导信号的不确定性。
2. **自适应权重生成模块**：将不确定性 u(x) 通过单调递减函数 h 映射为权重 w(x)。
3. **加权损失组合模块**：将自适应加权的引导损失与任务损失结合，更新模型参数。

Figure 1: Overview of the AdaConG approach. AdaConG leverages split CP with calibration to quantify the uncertainty of guidance signals and adaptively modulate their influence. The estimated uncertainty u is converted into an adaptive weight w, which reweights the guidance loss. This weighted guidance loss is then combined with the task loss to update the model, enabling effective learning under uncertain guidance.

### 5.1 引导不确定性量化

对于输入 x，引导信号的不确定性 u(x) 定义为预测集大小的函数：

$$u(x) = g(|\mathcal{C}(x)|) \quad (1)$$

其中，$\mathcal{C}(x)$ 是通过分裂共形预测构建的预测集，g 将集合大小映射到 [0,1] 区间。对于分类任务，具体形式为：

$$u(x) = (|\mathcal{C}(x)| - 1) / (K - 1)$$

其中 K 为类别总数。

### 5.2 自适应权重生成

自适应权重 w(x) 通过不确定性 u(x) 的单调递减函数计算：

$$w(x) = h(u(x)) \quad (2)$$

本文主要采用指数衰减形式：

- 知识蒸馏：$w = \exp(-\gamma u)$，其中 $\gamma = 10.0$
- 半监督学习：$w = \exp(-\gamma u)$，其中 $\gamma = 8.0$

此外，还探索了硬权重函数：$w = 1 \text{ if } u = 0, w = 0 \text{ if } u > 0$，即仅使用零不确定性的教师预测。

### 5.3 监督学习中的损失函数

总损失结合任务损失和自适应加权的引导损失：

$$\mathcal{L} = \lambda_{\mathrm{task}} \mathcal{L}_t + w(x) \cdot \lambda_{\mathrm{guide}} \mathcal{L}_g$$

### 5.4 半监督学习中的无监督损失

未标记数据的自适应加权一致性损失：

$$\mathcal{L}_u = \frac{1}{|\mathcal{D}_u|} \sum_{x \in \mathcal{D}_u} w(x) \ell(f(x_{\mathrm{strong}}), \tilde{y})$$

其中 $\tilde{y}$ 是伪标签，$x_{\mathrm{strong}}$ 是强增强后的图像。

### 5.5 模仿引导强化学习中的自适应权重

在 RL 设置中，分别计算模仿学习（IL）策略和 RL 策略的不确定性 $u_I(s)$ 和 $u_R(s)$，自适应权重为：

$$w(s) = \frac{\exp(-u_I(s))}{\exp(-u_I(s)) + \exp(-u_R(s))}$$

在数据收集阶段，智能体以概率 w(s) 选择 IL 动作，以概率 1-w(s) 选择 RL 动作。RL 策略的分位数通过指数移动平均更新：

$$\hat{q}_R^{(t)} \gets (1-\rho) \hat{q}_R^{(t-1)} + \rho \tilde{q}_R^{(t)}$$

探索概率定义为：

$$\epsilon = \min(0.5 \frac{t}{S_{\text{total}}} + 0.5 \frac{e}{E_{\text{total}}}, 1)$$

## 实验与关键发现

### 6.1 知识蒸馏

Table 1 展示了在 CIFAR-100 同构结构且存在域偏移的情况下，各种知识蒸馏方法的 Top-1 准确率。KD+AdaConG 相比标准 KD 提升高达 +10.89%。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_1gxP0WtOoO_Adaptiv/figures/002_Table_1.jpg]]
*Table 1: Top-1 accuracy (%) of various knowledge distillation methods on CIFAR-100 under homogeneous structure where teacher models underperform due to domain shift. ∆ indicates performance gain over the base method. Following the protocol in (Sun et al., 2024), we highlight in orange ∆ greater than 0.15, indicating non-trivial enhancement. We observe up to +10.89% higher accuracy.*

Table 1: Top-1 accuracy (%) of various knowledge distillation methods on CIFAR-100 under homogeneous structure where teacher models underperform due to domain shift. ∆ indicates performance gain over the base method. Following the protocol in (Sun et al., 2024), we highlight in orange ∆ greater than 0.15, indicating non-trivial enhancement. We observe up to +10.89% higher accuracy.

### 6.2 半监督学习

Table 2 展示了在半监督图像分类基准上，使用交叉熵作为引导损失时，各基线方法在集成 AdaConG 前后的 Top-1 准确率。FixMatch+AdaConG 在 CIFAR-10（40 标签）上提升 +5.98%，FlexMatch+AdaConG 在 CIFAR-100（2500 标签）上提升 +5.63%。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_1gxP0WtOoO_Adaptiv/figures/003_Table_2.jpg]]
*Table 2: Top-1 accuracy (%) of various baselines with and without AdaConG on several semisupervised image classification benchmarks, using cross-entropy as the guidance loss. ∆ shows mean performance gain w.r.t. conventional methods without AdaConG, upto +5.98% in accuracy. EXPERIMENTAL RESULTS. We present the results in Table 2. As shown, integrating AdaConG consistently improves performance across all baselines. This highlights the effectiveness of AdaConG in semi-supervised learning. By adaptively reweighting the influence of pseudolabels, AdaConG reduces reliance on noisy supervision, mitigating error propagation and leading to improved overall performance.*

Table 3 展示了使用 MSE 作为引导损失时的结果，AdaConG 同样带来一致提升。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_1gxP0WtOoO_Adaptiv/figures/004_Table_3.jpg]]
*Table 3: Top-1 accuracy (%) on CIFAR-100 for semi-supervised image classification. We compare multiple baselines with and without AdaConG using MSE as the guidance loss. ∆ indicates the average improvement over each corresponding baseline.*

Table 3: Top-1 accuracy (%) on CIFAR-100 for semi-supervised image classification. We compare multiple baselines with and without AdaConG using MSE as the guidance loss. ∆ indicates the average improvement over each corresponding baseline.

### 6.3 网格世界导航

Figure 2 展示了在三个网格世界环境（Lava 1, Lava 2, Door）中的学习曲线和预测不确定性。AdaConG 和 Hard AdaConG 收敛更快，在所有环境中均获得更高奖励。在 Lava 2 域偏移环境中，收敛后奖励超过最强基线的 6 倍。Figure 2(d) 显示 AdaConG 的预测不确定性随时间缩小并接近 IL 策略，且始终低于其他基线。

Figure 2: (a-c) Learning Curves. We compare AdaConG and Hard AdaConG with other baselines, including SAC, IBRL, and Soft IBRL, and present their learning curves across three environments: (a) Lava 1, (b) Lava 2, and (c) Door. AdaConG and Hard AdaConG perform similarly, converging faster and achieving higher rewards than other baselines in all environments. (d) Prediction Uncertainty. We show the average prediction uncertainties of AdaConG and other baselines, taking the Lava 1 environment as the example. Over time, the uncertainty of AdaConG shrinks and approach that of the IL policy, demonstrating the development of a well-learned RL policy. In addition, AdaConG maintains lower prediction uncertainty than other baselines, indicating stronger robustness to uncertainty.

### 6.4 自动驾驶转向预测

Table 4 展示了在 SullyChen 数据集域偏移下，各种知识迁移方法在集成 AdaConG 前后的平均准确率（mAcc）。KD+AdaConG 达到 76.8%，相比 KD 的 73.5% 提升 3.3%；FitNet+AdaConG 达到 76.2%，相比 FitNet 的 72.4% 提升 3.8%。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_1gxP0WtOoO_Adaptiv/figures/009_Table_4.jpg]]
*Table 4: Mean accuracy (%) of steer prediction of different knowledge transfer methods with and without AdaConG under domain shifts.*

### 6.5 消融研究

- **异构结构**（Table 5）：在 CIFAR-100 异构结构（如 VGG13/MobileNet-V2）下，KD+AdaConG 相比 KD 提升 +5.69%。
- **硬权重函数**（Table 6）：硬权重函数同样有效，KD+AdaConG (Hard) 相比 KD 提升 +9.31%。
- **分位数 vs 非一致性分数**（Table 7）：使用分位数计算预测集的 AdaConG 优于直接使用非一致性分数。
- **分布偏移**（Table 8）：在 CIFAR-100-C 分布偏移下，KD+AdaConG 相比 KD 提升高达 +18.62%。
- **更大规模数据集**（Table 9）：在 Tiny ImageNet 上，KD+AdaConG 相比 KD 提升高达 +19.02%。
- **α 敏感性**（Figure 4）：AdaConG 对 α 的选择具有鲁棒性，且始终优于标准 KD。
- **定性分析**（Figure 6）：干净图像产生更小的预测集和更高的自适应权重；噪声图像产生更大的预测集和更低的权重。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_1gxP0WtOoO_Adaptiv/figures/010_Table_5.jpg]]
*Table 5: As part of our ablation studies, we evaluate the performance of a heterogeneous teacher-student framework and present the results in the following Table 5. The table shows that, for all knowledge transfer methods, performance improves when combined with AdaConG, further validating the effectiveness of our approach across different teacher-student structures.*

Table 5: As part of our ablation studies, we evaluate the performance of a heterogeneous teacher-student framework and present the results in the following Table 5. The table shows that, for all knowledge transfer methods, performance improves when combined with AdaConG, further validating the effectiveness of our approach across different teacher-student structures.

Table 6: Top-1 accuracy (%) of various knowledge distillation methods without and with AdaConG using the hard weighting function. We use ∆ to show performance gain relative to conventional knowledge distillation methods and highlight in orange deltas greater than 0.15, indicating non-trivial enhancement following the protocol in (Sun et al., 2024).

Table 8: Top-1 accuracy (%) of different knowledge distillation methods on CIFAR-100-C. ∆ indicates performance gain over the base method. We observe up to +18.62% higher accuracy improvement.

Table 9: Top-1 accuracy (%) of different knowledge distillation methods on Tiny ImageNet. ∆ indicates performance gain over the base method. We observe up to +19.02% higher accuracy.

Figure 6: Qualitative analysis of adaptive weights. The first row shows original clean images from CIFAR-100, and the second row shows their noisy counterparts. Each image is annotated with the prediction set size (S) and the corresponding adaptive weight (W). Clean images produce smaller prediction sets, indicating lower uncertainty and thus higher weights, while noisy images yield larger prediction sets, reflecting higher uncertainty and consequently lower weights.

### 6.6 计算开销

Table 10 显示，KD+AdaConG 每 epoch 训练时间为 7.04 秒，相比 KD 的 6.87 秒仅增加约 0.003 ms/样本的开销，远低于 MC dropout 的 44.90 秒。Table 11 和 Table 12 分别展示了半监督学习和 RL 中的计算开销对比，AdaConG 仅增加极小的计算量。

Table 10: Comparison of computational overhead between standard KD, KD with AdaConG, and KD with MC dropout.

Table 12: Comparison of computational overhead across key RL baselines.

## 定位与知识库关联

AdaConG 属于**不确定性感知学习**与**共形预测**交叉领域的方法。其方法谱系可定位如下：

- **上游方法**：分裂共形预测（Shafer and Vovk, 2008; Angelopoulos et al., 2020）提供分布无关的不确定性量化；知识蒸馏（Hinton, 2015）、半监督学习（Sohn et al., 2020; Zhang et al., 2021）和模仿引导 RL（Hu et al., 2023）是 AdaConG 的应用场景。
- **同类方法**：与基于熵或最大 softmax 概率的启发式不确定性加权方法相比，AdaConG 提供了理论保证的覆盖率和更鲁棒的不确定性估计。与 MC dropout 等贝叶斯方法相比，AdaConG 计算开销极低。
- **下游应用**：AdaConG 可扩展到标签模糊或不确定监督的场景（如 credal sets）、NLP 任务、主动学习和持续学习等。

**局限性**：
- AdaConG 依赖于明确定义的标签或奖励信号来计算非一致性分数；在标签模糊或缺失的场景中需要额外设计。
- 在 RL 设置中，自适应 CP 的滑动窗口大小 N 和 EMA 平滑因子 ρ 需要手动调整。
- 计算开销虽小（每样本约 0.003 ms 额外开销），但在极大规模部署中仍需考虑。
- 未在自然语言处理（NLP）或图学习等模态上进行验证。

**开放问题**：
- 如何将 AdaConG 扩展到标签模糊或不确定监督的场景（如 credal sets）？
- 在 RL 中，滑动窗口大小 N 和 EMA 因子 ρ 的最优选择是否具有环境无关性？
- AdaConG 在 NLP 任务（如机器翻译、文本分类）中的引导不确定性量化是否有效？
- 能否将 AdaConG 与主动学习或持续学习策略结合，以进一步管理复杂不确定性？

## 原文 PDF

![[paperPDFs/ICLR_2026/Adaptive_Conformal_Guidance_for_Learning_under_Uncertainty.pdf]]
