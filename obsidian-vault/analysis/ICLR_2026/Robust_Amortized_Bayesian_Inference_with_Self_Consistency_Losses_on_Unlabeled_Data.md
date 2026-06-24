---
title: "Robust Amortized Bayesian Inference with Self-Consistency Losses on Unlabeled Data"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Robust_Amortized_Bayesian_Inference_with_Self_Consistency_Losses_on_Unlabeled_Data.pdf
aliases:
- SSNPESCLNS
- RABISCLUD
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/probabilistic_methods
core_operator: "在训练目标中引入基于贝叶斯自一致性的损失函数，对无标签数据（包括真实数据）强制执行后验与似然-先验之间的一致性。该损失函数是严格适当的，能直接优化分析后验，无需真实参数。"
primary_logic: "自一致性损失是严格适当的，因此可以与标准模拟损失无缝结合，而不改变目标后验。通过在少量无标签数据上训练，可以显著提高 ABI 的鲁棒性，即使评估数据远远超出训练分布，也能保持准确的、校准良好的后验估计，且不存在准确性与鲁棒性之间的权衡。"
claims:
- "提出的半监督方法允许在无标签数据上训练，无需真实参数。"
- "自一致性损失是严格适当的，针对分析后验，并且与数据分布无关。"
- "标准 NPE 在 μ_obs ≥ 2 时完全失效（后验方差为零），而添加自一致性损失后，即使 μ_obs > 3 也保持准确后验。"
- "NPE+SC (M=15) 在所有参数上均显著优于标准 NPE，平均绝对偏差和 Wasserstein 距离大幅降低。"
---

# Robust Amortized Bayesian Inference with Self-Consistency Losses on Unlabeled Data

> [!tip] 核心洞察
> 自一致性损失是严格适当的，因此可以与标准模拟损失无缝结合，而不改变目标后验。通过在少量无标签数据上训练，可以显著提高 ABI 的鲁棒性，即使评估数据远远超出训练分布，也能保持准确的、校准良好的后验估计，且不存在准确性与鲁棒性之间的权衡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于无标签数据自一致性损失的鲁棒摊销贝叶斯推断 |
| 英文题名 | Robust Amortized Bayesian Inference with Self-Consistency Losses on Unlabeled Data |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=E1dANKwo4I); [GitHub](https://github.com/bayesflow-org/self-consistency-real) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/probabilistic_methods |
| Method | Semi-supervised Neural Posterior Estimation with Self-Consistency Loss (NPE + SC) |
| Dataset | Multivariate normal means (10-dimensional, μ_prior=0, μ_obs up to 5), Air passenger traffic forecasting (Eurostat data, 15 countries), Hodgkin-Huxley neuron model (200-dim time series, out-of-simulation) |

> [!tip] 效果简介
> - Multivariate normal means (10-dimensional, μ_prior=0, μ_obs up to 5) 上，后验准确性（定性/MMD） 为 对于 μ_obs=5，后验估计几乎完美（与解析后验重合），即使远超出训练数据分布。，对比 μ_obs ≥ 2 时后验崩塌（方差为零），完全失效。，变化 从完全失效到近乎完美的定性改进。。
> - Air passenger traffic forecasting (Eurostat data, 15 countries) 上，参数 α 的平均绝对偏差 |μ - μ_Stan| 为 0.002 ± 0.001 (NPE+SC, M=15)，对比 0.079 ± 0.019 (standard NPE)，变化 -0.077。
> - Air passenger traffic forecasting (Eurostat data, 15 countries) 上，参数 α 的 Wasserstein 距离 为 0.006 ± 0.001 (NPE+SC, M=15)，对比 0.086 ± 0.019 (standard NPE)，变化 -0.080。

## 概述
标准摊销贝叶斯推断（ABI）在训练分布以外的观测数据上，后验近似会严重偏离真实后验，并出现方差崩塌（图1），且无法通过增加模拟数据来纠正。核心瓶颈在于神经网络后验估计器在有限模拟数据下的预渐近行为较差，导致在模拟稀疏或模型误设定区域产生高度有偏的推断。为此，本文提出**半监督神经后验估计方法 NPE+SC**，将贝叶斯自一致性转化为严格适当的损失函数，对无标签数据（不依赖真实参数）强制执行后验与似然‑先验之间的一致性。该方法在标准模拟损失上叠加自一致性损失（对数贝叶斯比率的方差），直接优化分析后验，从而在仅使用少量无标签观测的条件下，显著提升 ABI 的鲁棒性，且不存在准确性与鲁棒性之间的权衡。实验表明，在多元正态均值、航空客流预测、霍奇金‑赫胥黎神经元模型及 MNIST 图像去噪等多个基准上，NPE+SC 即使面对远超训练分布的数据，也能保持准确、校准良好的后验估计，将后验平均偏差、标准差偏差和 Wasserstein 距离大幅压缩，并在参数维度达到 10 维、无标签样本仅 4 个的极限场景下仍带来明显鲁棒性增益（表1、图2）。进一步的对比显示，NPE+SC 在真实数据上的后验估计与 Stan（MCMC 黄金标准）高度吻合，且优于基于域对抗、噪声注入等其他鲁棒性基线。

## 背景与动机

摊销贝叶斯推断（Amortized Bayesian Inference, ABI）通过神经网络直接学习从观测数据到后验分布的映射，在推断速度上具有显著优势，已成为计算负担较重的贝叶斯模型的实用替代方案。标准方法（如神经后验估计，Neural Posterior Estimation, NPE）依赖大量从联合分布 $p(\theta, x)$ 中采样的「标记」模拟数据对 $(\theta, x)$ 进行训练，通过最大化后验似然等严格适当的损失函数来逼近真实后验。

**现有方法的根本瓶颈**：标准 ABI 在训练分布之外的观测数据上，后验近似质量会严重下降甚至完全崩溃。例如，在多维正态均值问题中，当待推断的观测均值 $\mu_{\mathrm{obs}}$ 仅略微超出训练范围（$\mu_{\mathrm{obs}} \geq 2$）时，标准 NPE 的后验方差坍缩为零，即网络对参数的不确定性完全错误地消失（见 Figure 1 红色轮廓）。该现象源于神经网络后验估计器在有限模拟数据下的预渐近行为较差，使得在模拟数据稀疏或模型误设定区域产生高度有偏的推断。即使进一步增加模拟数据量，标准 NPE 也无法纠正这种由分布偏移引起的系统性偏差，严重阻碍了 ABI 在真实场景中的可靠部署。

**本文动机**：上述缺口表明，仅依靠标记模拟数据的监督训练不足以获得鲁棒的摊销后验。本文的核心思想是利用贝叶斯规则自身的一致性约束：对于精确推断，任意参数集下，似然与先验的乘积与后验的比值均等于边际似然，即满足贝叶斯自一致性比率

$$p(x)=\frac{p(x\mid\theta^{(1)})p(\theta^{(1)})}{p(\theta^{(1)}\mid x)}=\cdots=\frac{p(x\mid\theta^{(L)})p(\theta^{(L)})}{p(\theta^{(L)}\mid x)}$$

这一关系不依赖于真实参数值，仅要求后验、似然和先验之间保持内在一致性。在此基础上，本文提出将自一致性性质转化为**严格适当的损失函数**，从而构建一种半监督训练框架：在常规的标记模拟数据损失之外，加入在无标签数据（可来自任意来源，包括真实观测）上计算的自一致性损失。由于该损失只评价后验估计与已知似然-先验模型的相容性，训练过程无需无标签数据的真实参数，却能直接推动近似后验向真实的解析后验收敛。理论上，自一致性损失与标准模拟损失的目标后验一致，因此二者的结合不会改变推断目标，反而能显著增强对分布偏移的鲁棒性，消除以往方法中常见的准确性与鲁棒性之间的权衡。

## 核心创新

标准摊销贝叶斯推断（ABI，如 NPE）仅依靠模拟数据训练神经网络后验估计器，在**训练分布之外的观测**上后验近似迅速崩塌——后验方差收缩为零，产生高度有偏推断，且无法通过增加模拟数据量矫正。根本原因在于有限模拟数据下神经网络后验估计器的预渐近行为极差，在模拟数据稀疏或模型误设定区域形成灾难性外推。本文提出的 **半监督神经后验估计（NPE + SC）** 通过一个简洁而关键的改动解决这一瓶颈：在训练目标中引入**严格适当的贝叶斯自一致性损失**，从而**无需真实参数即可直接在无标签数据上强制后验与似然‑先验的一致性**。这形成了两个核心的 **changed slots**：

- **损失函数**：从单一的严格适当模拟损失 $S$（如最大似然）扩展为  
  $$S + \lambda \cdot C,$$
  其中 $C$ 是在无标签观测 $x^*$ 上计算的自一致性损失，衡量对数贝叶斯自一致性比率的方差（公式 2、4）。该损失是严格适当的——全局极小值当且仅当 $q(\theta|x)$ 等于真实后验 $p(\theta|x)$（命题 1–3），因此不会改变 ABI 的目标后验。

- **训练数据要求**：从仅依赖标记模拟对 $(\theta,x)\sim p(\theta,x)$，变成**同时使用标记模拟数据和无标签观测 $x^*\sim p^*(x)$**（可来自任何源，包括真实数据，无需知道 $\theta$）。这使得训练能直接触及真实数据分布，提供分布外鲁棒性所需的约束。

自一致性损失源于贝叶斯规则的一个基本性质：对于精确推断，似然‑先验乘积与后验的比值不依赖于参数（公式 1）。通过对该比率的对数在建议分布 $p_C(\theta)$ 上取方差，$C$ 将后验、似然和先验之间的内部一致性转化为可优化的标量损失。与依赖对抗训练或噪声注入的鲁棒方法不同，**$C$ 与数据分布无关**，且因严格适当性，它和模拟损失可以无缝结合而不引入准确性与鲁棒性的权衡。实验显示，哪怕仅用 **4 个无标签样本**（对比 1024 个标记样本），NPE+SC 也能显著降低 Wasserstein 距离和平均绝对偏差（Figure 2b、Table 1），并在观测均值远超训练范围时（Figure 1，$\mu_{\mathrm{obs}}\ge2$ 时标准 NPE 完全失效）维持近乎完美的后验估计。因果机制的核心是：**自一致性损失用无标签数据上的贝叶斯规则内在约束取代了过参数化神经网络在模拟数据外的盲目外推**，从而把后验估计器“锚定”在合理区域。

因此，NPE+SC 的创新不在于网络结构（仍使用条件归一化流和摘要网络），而在于**将贝叶斯自一致性的必要条件转化为一个与模拟损失相容、严格适当且可直接利用真实数据的训练信号**。这一设计使得摊销推断第一次在无标签观测上实现了鲁棒性的大幅提升，同时避免了鲁棒性方法中常见的后验目标偏移。

## 整体框架

所提方法——半监督神经后验估计（NPE+SC）——通过将标准模拟训练与贝叶斯自一致性损失相结合，构成一个半监督学习流程。该框架在仅需标记模拟数据的基础上，额外引入无标签观测（可来自真实数据），从而在推断时显著缓解模型误设定或分布偏移导致的后验崩溃问题。

**核心模块与数据流**
1. **后验估计器** $q(\theta \mid x)$：通常采用条件归一化流（conditional normalizing flow）实现，输入为观测 $x$（或经由摘要网络处理后的特征），输出为参数 $\theta$ 的近似后验分布。该网络是端到端训练的主体。
2. **摘要网络** $h(x)$（可选）：针对高维观测（如图像、时间序列）设计，用于提取低维充分统计量，以降低后验网络建模的难度。摘要网络与后验网络联合优化。
3. **模拟损失** $S$：在标记模拟数据对 $(\theta, x) \sim p(\theta, x)$ 上计算的标准损失（如最大化后验概率下的对数边缘似然），强制 $q(\theta \mid x)$ 逼近真实后验 $p(\theta \mid x)$。
4. **自一致性损失** $C$：在无标签观测 $x^* \sim p^*(x)$ 上计算，不依赖真实参数。其数学形式为对数贝叶斯自一致性比率关于建议分布 $p_C(\theta)$ 的方差：
   $$C = \operatorname{Var}_{\theta \sim p_C(\theta)} \left[ \log p(x^* \mid \theta) + \log p(\theta) - \log q(\theta \mid h(x^*)) \right],$$
   该损失是严格适当的，当且仅当 $q(\theta \mid x^*) = p(\theta \mid x^*)$ 时取最小值零，从而在无监督条件下驱动后验满足贝叶斯规则。

**训练与推理流程**
- **训练阶段**：利用 $N$ 个标记模拟样本和 $M$ 个无标签样本，联合优化经验半监督损失：
  $$\mathcal{L} = \frac{1}{N}\sum_{n=1}^N S(q(\theta_n \mid h(x_n)), \theta_n) + \lambda \cdot \frac{1}{M}\sum_{m=1}^M C\left( \frac{p(x_m^* \mid \theta_m) p(\theta_m)}{q(\theta_m \mid h(x_m^*))} \right),$$
  其中权重 $\lambda$ 控制自一致性项的影响（通常采用从 0 线性缓升的调度策略以稳定早期训练）。梯度同时更新后验网络与摘要网络。
- **推理阶段**：给定新观测 $x_{\text{obs}}$，直接通过 $q(\theta \mid h(x_{\text{obs}}))$ 获得近似后验，无需再访问真实参数或运行 MCMC。

整个流程的关键在于：自一致性损失不改变目标后验（因其严格适当性），却能强制网络在无标签数据上维持内部一致性，从而将鲁棒性拓展至训练分布之外的区域。实验证据表明，即使仅用少量无标签样本（如 $M=4$），亦可大幅提升后验准确性（Figure 1, 2），有效克服标准 NPE 在分布偏移时的后验崩塌问题。

## 核心模块与公式推导

标准摊销贝叶斯推断（ABI）的核心瓶颈在于：当观测数据偏离训练模拟分布时，神经网络后验估计器会严重失效，表现为后验方差坍塌为零或产生高度有偏估计。这种行为源于有限模拟数据下估计器的预渐近行为差，且在模拟稀疏或模型误设定区域无法通过增加模拟数据纠正。为此，该方法引入一种基于贝叶斯自一致性的损失函数，强制后验估计器在无标签数据上满足似然-先验-后验之间的内部一致性，从而在不改变目标后验的前提下显著提升鲁棒性。

### 半监督训练框架

方法将标准模拟损失与自一致性损失结合，形成一端可同时利用标记模拟数据和任意来源的无标签观测数据的半监督目标。设后验近似分布为 $q(\theta | h(x))$，其中 $h(x)$ 为可选的摘要网络（用于降维）。整体损失族定义为：

$$
(q^*, h^*) = \argmin_{q,h}\; \mathbb{E}_{(\theta,x)\sim p(\theta,x)}\left[S(q(\theta|h(x)), \theta)\right] + \lambda \cdot \mathbb{E}_{x^*\sim p^*(x)}\left[C\left(\frac{p(x^*|\theta)p(\theta)}{q(\theta|h(x^*))}\right)\right] \tag{2}
$$

其中 $S$ 为标准模拟损失（如最大似然损失），$C$ 为自一致性损失，$\lambda$ 为平衡权重。期望使用 $N$ 个模拟样本和 $M$ 个无标签样本的经验近似替代：

$$
(q^*, h^*) = \argmin_{q,h}\; \frac{1}{N}\sum_{n=1}^N S(q(\theta_n|h(x_n)), \theta_n) + \lambda \cdot \frac{1}{M}\sum_{m=1}^M C\left(\frac{p(x_m^*|\theta_m)p(\theta_m)}{q(\theta_m|h(x_m^*))}\right) \tag{3}
$$

关键优势在于：自一致性项仅需无标签观测 $x^*$ 和模型似然-先验，**无需知道真实参数**，因此可直接利用真实数据提升推断的鲁棒性。

### 自一致性损失及其严格适当性

自一致性损失的构造源于贝叶斯规则的一个基本事实：对于精确推断，边际似然 $p(x)$ 与参数无关，即对任意参数集 $\theta^{(1)},\dots,\theta^{(L)}$，有：

$$
p(x) = \frac{p(x|\theta^{(1)}) p(\theta^{(1)})}{p(\theta^{(1)}|x)} = \cdots = \frac{p(x|\theta^{(L)}) p(\theta^{(L)})}{p(\theta^{(L)}|x)}
$$

若后验近似 $q(\theta|x)$ 偏离真实后验，上述比率将不再是常数。据此定义自一致性损失为**对数贝叶斯自一致性比率的方差**：

$$
C\left(\frac{p(x^*|\theta)p(\theta)}{q(\theta|h(x^*))}\right) = \operatorname{Var}_{\theta\sim p_C(\theta)}\left[\log p(x^*|\theta) + \log p(\theta) - \log q(\theta|h(x^*))\right] \tag{4}
$$

其中 $p_C(\theta)$ 为提议分布（如先验或其他合适分布）。该损失衡量了给定 $x^*$ 下，不同 $\theta$ 对应的对数比率波动程度。当且仅当 $q(\theta|h(x^*)) = p(\theta|x^*)$ 时，比率全局恒定，方差达到最小值零。理论上可证明：

- **Proposition 1**：若似然已知，则 $C$ 作用于贝叶斯自一致性比率是严格适当的，即其全局最小化解唯一地等于真实后验。
- **Proposition 2**：若 $p_C(\theta)$ 的支撑覆盖 $p(\theta|x)$ 的支撑，则方差形式的损失 (4) 是严格适当的。
- **Proposition 3**：在上述条件下，半监督损失 (2) 对任意 $p^*(x)$ 都是严格适当的。

这意味着自一致性损失**不会引入偏差**，其作用纯粹是强化模型内部一致性，且对无标签数据分布 $p^*(x)$ 完全不敏感。

### 关键模块

整套方法由以下组件构成：
1. **后验神经网络估计器 $q(\theta|x)$**：通常采用条件可逆神经网络（归一化流）实现，负责将观测映射为后验分布。
2. **摘要网络 $h(x)$**：可选模块，用于从高维观测中提取低维充分统计量，以适配深度推断网络。
3. **模拟损失 $S$**：在标记模拟数据上优化的标准损失（如最大似然），保证估计器在训练分布内的准确性。
4. **自一致性损失 $C$**：在无标签数据上施加贝叶斯规则约束，通过最小化对数比率方差来驱动后验估计器在分布偏移下保持内部一致。

### 鲁棒性原理与证据

因果调节变量在于 $C$ 的加入。实验表明（见 Figure 1–5, Table 1–2），仅凭少量无标签样本（如 $M=4$），自一致性损失即可使后验估计在极端 OOD 场景下保持准确且校准良好，而标准 NPE 在 $\mu_{\text{obs}}\ge 2$ 时后验完全坍塌（方差为零）。该机制之所以有效，是因为它不依赖 OOD 区域的标记样本，而是通过强制模型满足自身定义的贝叶斯结构来抵抗分布偏移。在 10 维参数空间内，NPE+SC 的后验与解析解几乎重合（MMD 接近零），且这一增益在 100 维时依然显著。此外，在似然由神经网络估计或存在摘要网络的情况下，自一致性损失仍能提供强大的鲁棒性提升（尽管在后验标准差上可能引入符号相反的偏差，见 Figure 7）。权重 $\lambda$ 的调度（如线性缓升）对训练稳定性有重要作用，但其值不控制准确性与鲁棒性之间的权衡，仅需保证初期平稳。

> 需要说明的是，自一致性损失在高维似然联合学习（如 MNIST）中无法完全消除模型误设定带来的偏差，且当前实验的无标签数据规模有限（$M\le 32$），其在大规模真实数据上的扩展性有待进一步验证。

## 实验与分析

本节从主结果、消融研究、鲁棒性对比及失败模式四个层面解析自一致性损失（SC）在半监督摊销贝叶斯推断中的实际效果。核心瓶颈在于标准神经后验估计器（NPE）在分布外（OOD）观测上会出现严重的后验崩塌——方差归零或预测高度有偏——而仅凭增加模拟数据无法纠正。SC损失通过强制后验与已知似然‑先验在无标签数据上满足贝叶斯自一致性，在不牺牲训练分布内准确性的前提下极大提升了OOD鲁棒性。

### 主结果：从完全失效到近乎完美的后验校准
**多元正态均值问题（10维）** 最能暴露标准NPE的脆弱性。图1显示，当观测均值 μ_obs ≥ 2 时，NPE后验方差迅速塌缩到零，参数推断完全失效。相比之下，加入SC损失（NPE+SC）后，即使 μ_obs > 3——远超训练数据覆盖范围——后验分布仍与解析解高度吻合，后验均值的轮廓几乎完全重合。消融实验进一步确认：在参数维度 D≤10 时，NPE+SC与真值后验的最大均值差异（MMD）接近零；D=100时依然保持显著改进（图2a）。

![[assets/figures/papers/iclr26_0016_E1dANKwo4I_Robust_Amortized_Bayesian_Inference_with_Self-Co/figures/001_Figure_1.jpg]]
*Figure 1: Contour plot of the normal means problem using standard NPE (red) or our semi-supervised approach (NPE + SC, blue), with the analytic posterior in gray. Symbols indicate posterior mean estimates (red cross: NPE only; blue square: $\mathrm { N P E } + \mathrm { S } \bar { \mathrm { C } }$ ; gray triangle: reference). Each subplot shows posterior inference on observed data that are increasingly distant from the labeled training data ( $\mu _ { \mathrm { p r i o r } }$ = 0 ) . Only the first two dimensions of the 10-dimensional posterior are shown. While standard NPE collapses to zero variance for $\mu _ { \mathrm { o b s } } \geq$ 2 . , adding the self-consistency loss preserves accurate posterior...

![[assets/figures/papers/iclr26_0016_E1dANKwo4I_Robust_Amortized_Bayesian_Inference_with_Self-Co/figures/002_Figure_2.jpg]]
*Figure 2: (a): Posterior distance between approximate and true posterior for varying parameter dimensionality*

![[assets/figures/papers/iclr26_0016_E1dANKwo4I_Robust_Amortized_Bayesian_Inference_with_Self-Co/figures/003_Figure_2.jpg]]
*Figure 2: (b): Posterior distance between approximate and true posterior for varying unlabeled training data sizes. Figure 2: Posterior distance quantified by maximum mean discrepancy (MMD) to the analytic posterior for variations of the default configuration. Errorbars show ±1 SDs over 10 model refits*

**航空客流预测** 建立在15个欧洲国家的真实数据上，以Stan MCMC结果为金标准。表1显示，标准NPE在参数α上的平均绝对偏差高达 0.079±0.019，Wasserstein距离为 0.086±0.019；而NPE+SC（M=15）将两者分别降至 0.002±0.001 和 0.006±0.001，几乎消除了偏差。对所有参数（α、β、γ、δ、log σ），NPE+SC的后验区间均紧密贴合Stan参考值（图3），且大幅优于在线NPE、VAE以及基于MMD或域对抗的鲁棒对比方法（表2）。值得强调的是，SC损失仅在训练期间使用了 M=8 个国家的无标签观测，仍能泛化到其余国家，体现其小样本鲁棒性。

![[assets/figures/papers/iclr26_0016_E1dANKwo4I_Robust_Amortized_Bayesian_Inference_with_Self-Co/figures/021_Table_1.jpg]]
*Table 1: Posterior metrics for NPE and NPE augmented with self-consistency loss (NPE+SC) relative to Stan. For each parameter, absolute bias in posterior means and standard deviations, as well as Wasserstein distance, are reported. Values are shown as mean (SE) across 15 countries. Self-consistency loss was evaluated using M $\in \{$ 4 , 8 , 1 5 $\}$ countries during training*

![[assets/figures/papers/iclr26_0016_E1dANKwo4I_Robust_Amortized_Bayesian_Inference_with_Self-Co/figures/004_Figure_3.jpg]]
*Figure 3: Comparison of posterior estimates for 15 countries (ISO 3166 alpha-2 codes) among standard NPE (red), NPE + SC (blue), and Stan (reference in gray; Carpenter et al., 2017). Central 50% (thick lines) and 95% (thin lines) posterior intervals of the autoregressive component β are shown, sorted by lower 5% quantile as per Stan (i.e., established benchmark). The SC loss was evaluated on data from M = $\mathbf { 8 }$ countries during training, greatly enhancing ABI’s robustness in both no-misspecification scenarios and real-data evaluations*

**Hodgkin‑Huxley神经元模型** 对OOD时序数据的推断进一步验证了SC损失的预测校准能力。在200维时间序列上，标准NPE生成的后验预测样本严重偏离真实观测；而NPE+SC的预测几乎无偏（图4a）。定量上，针对1000个OOD数据集的平均绝对偏差（MAB）差值直方图几乎全部为负，表明NPE+SC的预测偏差低于NPE的情形覆盖绝大多数样本（图4b）。

![[assets/figures/papers/iclr26_0016_E1dANKwo4I_Robust_Amortized_Bayesian_Inference_with_Self-Co/figures/006_Figure_4.jpg]]
*Figure 4: (a) Posterior predictive samples (gray) inferred from an out-of-simulation dataset (black). NPE only produces highly biased predictions while NPE+SC yields accurate results. (b) Histogram of the mean absolute bias (MAB) difference of posterior predictions computed for 1000 out-of-simulation datasets. NPE+SC has lower bias than NPE for almost all datasets*

**MNIST图像去噪** 将SC损失拓展到高维生成场景。仅用仿真训练的标准NPLE（NPE with likelihood estimation）产生严重像素化且模糊的重建，不确定性图分散且不连贯。加入SC损失后，NPLE+SC生成的后验均值更平滑、忠实于真实数字，后验标准差沿数字轮廓集中，不确定性表达与边缘结构高度吻合（图5、图17）。这一改进源于SC损失在无标签真实图像上约束后验与估计似然的一致性，从而抑制了模型在OOD区域的偏置放大。

### 消融研究：少样本与极端分布偏移下的稳健性
- **无标签数据规模**：即使仅用 M=4 个无标签观测（对比 1024 个仿真样本），SC损失仍带来明显的后验MMD下降（图2b），表明该方法对小规模真实数据高效。
- **数据分布偏移**：当无标签数据的真实均值 μ* 偏离训练分布（μ*≥1）时，NPE+SC在所有指标上的改进最为剧烈（后验均值偏差、标准差偏差、MMD同时大幅降低，图6 bottom）。这证明SC损失并非要求无标签数据与训练分布匹配，而是通过自一致性约束校正OOD推断偏差。
- **高维与组件失效**：在参数维度升高到50时，SC损失依然能压低偏差并维持较低MMD（图6 top）。然而，当似然函数由神经网络估计时，SC损失虽能改善后验均值偏差和MMD，却引入了符号相反的后验标准差偏差（图7 top）。这说明SC损失的效果受限于似然模型的准确度——若似然本身存在拟合误差，一致性约束会部分将其传递到后验的不确定性标定中。具有摘要网络时，SC损失在全部指标上均保持稳健增益（图7 bottom），进一步确认了对充分统计量提取的兼容性。

### 失败模式与局限
- **似然联合估计的不确定性反转**：如上所述，在同时学习后验与似然时，SC损失可能减小均值偏差却反转标准差偏差方向，导致不确定性标定出现新的系统误差（图7 top）。需要手动验证更复杂场景下该反转的严重程度。
- **高维生成中的残余偏差**：在MNIST去噪等极高维似然‑后验联合任务中，SC损失无法完全消除仿真模型误设定引起的重构偏差，后验均值的锐化与真实图像之间仍有差距（图5）。这提示SC损失单独不足以补偿严重的仿真‑现实差异，可能需要与事后校正方法结合。
- **训练调度依赖性**：λ（自一致性权重）需采用线性缓升调度，否则早期训练会出现不稳定性。当前实验仅在较小规模无标签数据（M≤32）上评估，更大规模真实数据上的有效性和扩展性仍有待验证。

### 整体结论
自一致性损失将贝叶斯内部一致性转化为可微的严格适当损失，使得在任意来源的无标签数据上训练时，后验估计器能够抵抗训练分布偏移。实验一致表明，NPE+SC在分布内保持与标准NPE相当的性能，而在分布外将完全失效的推断恢复至金标准水平，且无需访问真实参数。这种“无准确‑鲁棒权衡”的特性使SC损失成为提高摊销贝叶斯推断实际部署可靠性的有力工具。

## 方法谱系与知识库定位

### 与基线及后续方法的关系
本文所提方法 NPE+SC（基于自一致性损失的半监督神经后验估计）处于摊销贝叶斯推断（ABI）与半监督学习的交叉点。其核心改造点在于训练目标和数据需求：相较于标准 NPE 仅依赖标记模拟对的模拟损失 $S$，NPE+SC 通过引入严格适当的自一致性损失 $C$ 直接在无标签观测 $x^*$ 上强化后验‑似然‑先验的一致性（Equation 2–4），从而将训练数据扩展至任何来源的无标签样本，包括真实数据。这一设计使得 NPE+SC 与现有鲁棒 ABI 方法在机制上形成本质差异：

- **与注入式/对抗式鲁棒方法**（NPE‑MMD、NPE‑DANN、NNPE）不同，自一致性损失基于贝叶斯规则本身的代数不变性构造，无需显式噪声添加或域分类器，其**严格适当性**（Proposition 1–3）保证了标签损失与无标签损失可无缝叠加而不改变目标后验。这意味着它消除了鲁棒性与准确性之间的常见权衡。
- **与在线 NPE、Schmitt et al. (2024) 及 VAE 等后续方案**相比，NPE+SC 在航空客流预测上取得更小的 Wasserstein 距离、均值偏差与标准差偏差（Table 2），且仅需在训练过程中访问少量无标签国家数据（M=4‑15）就能将推断质量提升至与 Stan 金标准接近的水平（Figure 3）。

相比只依赖模拟‑再校正的后处理范式，NPE+SC 属于在**训练阶段即引入无标签数据分布信息的正则化方法**，其适用范围覆盖了从低维正态均值到中维时序、再到高维图像的多种推断任务，且不要求无标签数据与模拟数据同分布。

### 适用边界
根据实验证据，NPE+SC 的能力边界可以沿以下维度界定：

1. **似然已知程度**  
   当似然函数解析可求时，NPE+SC 在极端的分布外（OOD）观测上仍能恢复近乎无偏的后验。例如，在 10 维正态均值问题中，标准 NPE 在 $\mu_{\text{obs}}\ge 2$ 时后验方差崩塌至零，而 NPE+SC 即便在 $\mu_{\text{obs}}>3$ 时后验仍与解析解几乎重合（Figure 1）。  
   **退化条件**：当似然本身由神经网络估计时，自一致性损失虽可持续降低后验均值的偏差和 MMD，但同时会**引入符号相反的后验标准差偏差**（Figure 7 top）。此时方法不能完全补偿似然估计的不准确，**整体性能受限于似然网络的预训练质量**。

2. **参数维度与计算规模**  
   NPE+SC 在参数维度 $D\le10$ 时可逼近完美后验，在 $D=100$ 时仍提供显著增益（Figure 2a）。每批训练中使用的无标签数据量可极低：M = 4 个样本即可带来可见的鲁棒性提升（Figure 2b）。  
   然而，当**同时面对高维参数和高维似然**（如 784 维的 MNIST 图像去噪）时，自一致性损失虽使重建更平滑并产出连贯的不确定性图（Figure 5、Figure 16‑17），却无法完全消除由模型误设定导致的后验偏差，去噪质量仍受限于似然估计的体系误差。

3. **训练稳定性与超参数**  
   虽然 λ 在理论上不控制准确‑鲁棒平衡（严格适当性保证），但其**调度策略对训练稳定性至关重要**：高维场景中若固定 λ≈1，训练早期可能不稳定，需要采用线性缓升至 1 的调度（Appendix B）。

4. **无标签数据分布偏移**  
   NPE+SC 不要求无标签数据与模拟训练数据同分布。当无标签数据的均值偏离训练均值 $\mu^* \ge 1$ 时，SC 损失即可提供极大改进（Figure 6 底行），证明其适用于模型误设定下的真实观测。

当前实验主要在规模较小（M≤32）的无标签集上进行验证，**在更大规模真实数据流和持续学习场景中的行为尚未充分评估**，这构成一个潜在的适用边界。

### 已知局限与开放问题
**已知局限**：
- **似然‑后验联合估计中的偏差传递**：当似然由神经网络近似时，自一致性损失会引入符号相反的后验标准差偏差（Figure 7 top），表明单纯依赖贝叶斯自一致性很难同时校正两个近似组件的系统误差。
- **模型误设定的残留偏差**：在高维似然（如 MNIST 似然模型）存在错误设定时，SC 损失不能将其完全排除，性能仍受限于似然估计的结构性误差。
- **训练超参数敏感性**：λ 调度以及建议分布 $p_C(\theta)$ 的选择可能影响收敛速度和终态性能，缺乏自适应机制。

**开放问题**：
1. 当前自一致性损失建立在封闭形式似然的基础上。如何为**自由形式流**（如流匹配、基于分数的扩散模型）构建计算高效且严格适当的自一致性目标，仍是待解决的方法论缺口。
2. 在**后验与极高维似然（如原始像素级生成模型）的联合学习**中，如何有效注入自一致性正则以避免偏差放大，需要新的联合训练架构。
3. 如何将自一致性损失与**事后校准**（post‑hoc correction）方法体系化结合，以进一步扩展准确推断的 OOD 覆盖边界，是提升实用性的重要方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/Robust_Amortized_Bayesian_Inference_with_Self_Consistency_Losses_on_Unlabeled_Data.pdf]]
