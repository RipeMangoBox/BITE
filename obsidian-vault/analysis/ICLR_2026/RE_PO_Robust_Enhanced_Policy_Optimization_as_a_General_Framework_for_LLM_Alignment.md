---
title: "RE-PO: Robust Enhanced Policy Optimization as a General Framework for LLM Alignment"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RE_PO_Robust_Enhanced_Policy_Optimization_as_a_General_Framework_for_LLM_Alignment.pdf
aliases:
- RPREPO
- RE-PO
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "通过期望最大化（EM）推断每个偏好标签正确性的后验概率（置信度权重），并将其动态融入训练损失，自适应地强调可靠数据、弱化噪声数据。"
primary_logic: "将标签正确性建模为潜在变量，利用 EM 算法联合推断每个样本的软置信度权重和标注者可靠性，在优化策略的同时实现噪声鲁棒对齐。"
claims:
- "在 Mistral-7B 上，RE-DPO 将 AlpacaEval 2 的 LC（长度控制胜率）从 28.5% 显著提升至 35.5%，WR（原始胜率）从 28.6% 提升至 33.0%，实现了 7.0 个百分点的最大提升。"
- "在 Llama-3-8B 上，RE-IPO 将 AlpacaEval 2 的 LC 从 43.6% 提升至 48.3%，WR 从 41.6% 提升至 48.6%，展现了跨算法和跨模型的稳定增益。"
- "在受控合成噪声实验中，RE-PO 估计的标注者可靠性与 GPT-4o 作为参考的真实可靠性高度吻合，验证了可靠性恢复能力。"
- "定性案例显示，RE-PO 对疑似错误标注（如主题分类任务中违反输出格式的长篇回答）赋予极低的后验置信度（w_i ≈ 0.037），并在训练中有效降低其权重。"
---

# RE-PO: Robust Enhanced Policy Optimization as a General Framework for LLM Alignment

> [!tip] 核心洞察
> 将标签正确性建模为潜在变量，利用 EM 算法联合推断每个样本的软置信度权重和标注者可靠性，在优化策略的同时实现噪声鲁棒对齐。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | RE-PO: 作为大语言模型对齐通用框架的鲁棒增强策略优化 |
| 英文题名 | RE-PO: Robust Enhanced Policy Optimization as a General Framework for LLM Alignment |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=jDKpOvTCM8); [Project](https://repo-alignment.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | RE-PO (Robust Enhanced Policy Optimization) |
| Dataset | AlpacaEval 2 |

> [!tip] 效果简介
> - AlpacaEval 2 上，LC (Length-Controlled Win Rate, %) 为 35.5 (RE-DPO)，对比 28.5 (DPO)，变化 +7.0。
> - AlpacaEval 2 上，WR (Raw Win Rate, %) 为 33.0 (RE-DPO)，对比 28.6 (DPO)，变化 +4.4。
> - AlpacaEval 2 上，LC (%) 为 48.3 (RE-IPO)，对比 43.6 (IPO)，变化 +4.7。

## 概述

大规模偏好数据集中广泛存在的标注错误与噪声是当前大语言模型对齐训练的主要瓶颈：标准对齐方法（如 DPO、IPO）对所有偏好对一视同仁，容易过拟合不可靠的监督信号，严重损害模型的性能与泛化能力。针对这一问题，本文提出 **RE-PO（Robust Enhanced Policy Optimization）**——一种通用的鲁棒增强策略优化框架。其核心思路是将每个偏好标签的正确性建模为潜在变量，并采用期望最大化（EM）算法联合推断样本的标签置信度与标注者可靠性。在 E-step 中，算法计算每个样本标签为正确的后验概率 `w_i`（Equation 4）；在 M-step 中，将这些置信度作为自适应权重融入偏好损失，从而动态强调可靠数据、抑制噪声标签对策略更新的影响（Equation 5）。该机制可即插即用于 DPO、IPO、SimPO、CPO 等多种现有对齐算法（Table 1），提供统一的噪声鲁棒性增强。

实验在 Mistral-7B 和 Llama-3-8B 两个基座模型上验证了 RE-PO 的增益。以 AlpacaEval 2 为基准，RE-DPO 将 Mistral-7B 的 LC（长度控制胜率）从 28.5% 大幅提升至 35.5%，WR（原始胜率）从 28.6% 提升至 33.0%（Table 2）；RE-IPO 在 Llama-3-8B 上实现 LC 43.6%→48.3%、WR 41.6%→48.6% 的提升。在含多个真实标注者的 MultiPref 数据集上，RE-DPO 同样带来显著且一致的性能进步（Table 3），且对评判模型的变化保持稳健（Table 7）。受控合成噪声实验进一步证实，RE-PO 估计的标注者可靠性与 GPT-4o 的真实可靠性高度吻合（Figure 2）。定性案例显示，RE-PO 对疑似的误标注赋予极低的后验置信度（`w_i≈0.037`），从而在训练中有效衰减其影响（Table 5）。RE-PO 仅引入约 11% 的平均训练时间开销，以轻量的代价实现了可观的鲁棒性提升（Table 8）。

## 背景与动机

当前大语言模型对齐的核心范式依赖于人类偏好数据，通过直接偏好优化（DPO）等损失函数将模型策略拉向“胜者”响应。然而，现实中的大规模偏好数据集（如UltraFeedback）普遍由多位标注者生成，受主观判断、标注规范不一致或自动标注偏差影响，包含大量噪声。标准对齐方法平等对待每一个偏好标签，在不可靠监督信号上直接最小化损失，容易过拟合噪声，导致对齐性能和泛化能力显著下降。

现有的鲁棒对齐尝试存在明显盲区。全局噪声率校正（如rDPO）要求预先知道整体噪声比例，这一假设在实际多标注者场景中难以成立。损失层面的防御（如Hölder-DPO、标签平滑）仅从函数形态上抑制异常值，并未显式区分不同标注者的可靠性或不同样本的噪声程度。这些方法无法回答一个根本性问题：**每一个特定偏好标签在多大程度上可信？** 当标注者群体中存在持续产生错误标注的个体时，整体层面的正则化不足以消除其负面影响。

RE-PO的提出正是为了弥补以上缺口。核心动机是将标签正确性建模为潜在变量，并联合推断每个样本的软置信度权重与每位标注者的可靠性参数，从而在优化策略的同时实现自适应去噪。该框架利用期望最大化（EM）迭代，在E步根据当前模型与标注者可靠性计算每个偏好标签正确的后验概率；在M步将这些概率作为样本级权重，动态强调可靠数据、弱化噪声数据。这种显式的标注者建模和标签级不确定性量化，使得RE-PO能够作为一个通用稳健层，嵌入到DPO、IPO、SimPO、CPO等各类对齐目标中。

此动机的有效性已被多维度证据支持。在受控合成噪声实验中，RE-PO估计的标注者可靠性与真实参考值（由GPT-4o判定）高度吻合，验证了其噪声恢复能力（Figure 2）。在Mistral-7B上，仅将标准DPO替换为RE-DPO，AlpacaEval 2的长度控制胜率（LC）即从28.5%大幅提升至35.5%（+7.0个百分点，Table 2），表明数据噪声是实际对齐瓶颈，且RE-PO的加权策略能有效缓解该瓶颈。定性案例进一步显示，RE-PO对明显违反输出格式的错误偏好标签赋予极低后验置信度（如w_i≈0.037），并在训练中成功将其影响压低（Table 5）。这些结果为RE-PO的动机提供了坚实的实证基础：**通过概率推断区分标签可信度，是实现噪声鲁棒对齐的关键一步**。

## 核心创新

现有对齐方法（如 DPO、IPO、SimPO、CPO）在大规模偏好数据上训练时，面临一个共同瓶颈：数据集中广泛存在的标注错误和不可靠反馈会严重损害对齐性能和泛化能力（real_bottleneck）。标准损失函数将所有样本平等对待，导致模型过拟合噪声标签；简单的标签平滑或基于全局噪声率的鲁棒方法（如 rDPO）则无法捕捉标注者间的异质性，限制了去噪效果。

RE-PO 的核心创新在于**将偏好标签的正确性建模为潜在变量，并通过期望最大化（EM）算法联合推断每个样本的软置信度权重与标注者的可靠性，以此实现“自动识别并弱化噪声数据”的去噪对齐**（core_insight）。与基线相比，该方法在三个关键环节做出了本质改变：

1. **概率化的偏好建模**  
   标准方法将损失函数直接作为优化目标，缺乏对噪声的显式处理。RE-PO 首先从任意偏好损失 $\mathcal{L}_{\mathrm{pref}}$ 中诱导出一个噪声自由的偏好概率（Equation 2）：
   $$p(y_w \succ^* y_l | x, \theta) = \sigma\big( \mathcal{L}_{\mathrm{pref}}(x, y_l \succ y_w; \theta) - \mathcal{L}_{\mathrm{pref}}(x, y_w \succ y_l; \theta) \big)$$
   该构造将损失转换为概率形式，为后续的贝叶斯推断奠定了统一基础，使得 DPO、IPO 等不同目标皆可嵌入同一框架。

2. **自适应样本权重与标注者可靠性推断（E步）**  
   不同于基线对所有样本一视同仁，RE-PO 在每次迭代中利用当前策略 $\theta^{(t)}$ 和标注者可靠性 $\eta_{k_i}^{(t)}$，为每个偏好对计算其标签正确的后验置信度 $w_i^{(t)}$（Equation 4）：
   $$w_i^{(t)} = \frac{p(y_{w,i}\succ^* y_{l,i} | x_i, \theta^{(t)})\,\eta_{k_i}^{(t)}}{p(y_{w,i}\succ^* y_{l,i} | x_i, \theta^{(t)})\,\eta_{k_i}^{(t)} + p(y_{l,i}\succ^* y_{w,i} | x_i, \theta^{(t)})\,(1-\eta_{k_i}^{(t)})}$$
   这一步骤本质上是 E 步：它以软权重的方式量化了每个观测偏好的可信程度，并同时更新每个标注者 $k$ 的可靠性 $\eta_k$——完整批次下即为该标注者所有样本置信度的均值（Equation 6），小批量训练中则通过指数移动平均（EMA）在线更新（Equation 7）。由此，RE-PO 在不依赖人工标定噪声率的前提下，自动“发现”并压低低质量标注者的影响（Figure 2, Figure 3）。

3. **加权协同优化的损失函数（M步）**  
   M 步中，策略参数 $\theta$ 的更新目标变为以 $w_i$ 为权重的交叉熵损失（Equation 5）：
   $$\mathcal{L}_{\mathrm{RE-PO}}(\theta) = -\sum_{i=1}^{N}\Big[ w_i^{(t)}\log p(y_{w,i}\succ^* y_{l,i} | x_i, \theta) + (1-w_i^{(t)})\log p(y_{l,i}\succ^* y_{w,i} | x_i, \theta) \Big]$$
   这一加权机制直接将 E 步推断的噪声概率反馈到训练过程中，使得可靠标签主导梯度更新，而疑似错误的样本被自适应地降权（如定性案例中，RE-PO 对明显错误标注赋予约 $w_i \approx 0.037$ 的极低权重，Table 5）。相比之下，标准 DPO/IPO 对所有样本施加相同权重，标签平滑仅引入全局扰流，均缺乏这种**样本级、动态自适应的去噪能力**。

上述三个改变槽位共同构成了 RE-PO 的“即插即用”鲁棒层：它与底层偏好算法解耦，可无缝增强 DPO、IPO、SimPO 和 CPO 等多个族系，而无需改动原有超参数或训练流程（Table 2 和 Table 3 的一致性提升证明了其通用性）。在 AlpacaEval 2 上，RE-DPO 将 Mistral-7B 的 LC 胜率从 28.5% 提升至 35.5%（+7.0 p.p., Table 2），RE-IPO 将 Llama-3-8B 的 WR 从 41.6% 提升至 48.6%（+7.0 p.p., Table 2）；在真实多标注者数据集 MultiPref 上，RE-DPO 相较于标准 DPO 同样获得 2.4–5.1 个百分点的稳定增益（Table 3），且对评判模型的变更保持鲁棒（Table 7）。受控合成噪声实验进一步显示，RE-PO 估计的标注者可靠性与真实可靠性高度吻合（Figure 2），验证了其**噪声恢复**而非简单过滤的因果机制。

需要指出，RE-PO 的有效性依赖于策略初始化不能严重偏离真实偏好，否则 E 步可能对错误标签赋予误导性的高置信度，造成去噪失灵（limitations）。此外，该方法要求训练数据附带标注者标识，并存在对超参数（初始可靠性 $\eta_0$、EMA 动量 $\alpha$）一定的敏感性（Table 4）。尽管如此，其核心创新——将噪声建模为潜在变量、以 EM 驱动置信度加权——为偏好对齐提供了一个可解释且高效的去噪范式，显著优于仅从损失层面或全局噪声率出发的现有方案。

## 整体框架

![[assets/figures/papers/iclr26_0013_jDKpOvTCM8_RE-PO_Robust_Enhanced_Policy_Optimization_as_a_G/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the Robust Enhanced Policy Optimization (RE-PO) framework. Starting from noisy pairwise feedback, RE-PO uses an Expectation-Maximization (EM) procedure to jointly refine label confidences and the policy. In each iteration, the E-step estimates a confidence score for every observed preference by inferring the posterior probability that the label is correct under the current model and annotator reliabilities. The M-step then uses these scores as adaptive weights to update both the LLM policy and the annotator reliability parameters, progressively down-weighting likely corrupted labels and emphasizing reliable supervision*

RE-PO（Robust Enhanced Policy Optimization）框架针对大规模偏好数据集中普遍存在的标注错误与噪声，通过将标签正确性显式建模为潜在变量，并从数据中联合推断每个样本的置信度以及标注者可靠性，实现对噪声监督信号的自适应鲁棒利用。其整体pipeline以期望最大化（EM）为核心，在训练过程中交替执行标签置信度推断（E-step）、策略更新（M-step）和标注者可靠性在线更新，形成一个闭环迭代（Figure 1，Algorithm 1）。

### 输入与前置模块

框架的输入为带有标注者标识的成对偏好数据 $\mathcal{D}=\{(x_i, y_{w,i}, y_{l,i}, k_i)\}$，其中 $k_i$ 表示第 $i$ 个偏好对的标注者。RE-PO不要求已知全局噪声率或干净标签的先验分布，仅需假设每个标注者 $k$ 拥有一个待估计的可靠性参数 $\eta_k\in[0,1]$，表示其标注正确的概率（Assumption 1）。这一设定使得RE-PO能够在缺乏全局噪声率信息的条件下，从多标注者数据中自动识别并降权不可靠样本。

RE-PO的通用性建立在“诱导偏好概率”的统一形式上。对于任意以损失函数 $\mathcal{L}_{\mathrm{pref}}$ 实现的对齐算法（如DPO、IPO、SimPO、CPO），框架通过

$$
p(y_w \succ^* y_l \mid x, \theta) = \sigma\bigl( \mathcal{L}_{\mathrm{pref}}(x, y_l \succ y_w; \theta) - \mathcal{L}_{\mathrm{pref}}(x, y_w \succ y_l; \theta) \bigr)
$$

将损失函数转化为噪声自由条件下的偏好概率（Equation 2），从而将不同的对齐目标统一到同一概率框架内（Table 1列举了各算法的具体 $\mathcal{L}_{\mathrm{pref}}$ 形式）。

### 核心迭代循环

RE-PO的迭代流程由三个紧密耦合的步骤组成。

**E‑step（标签置信度推断）**  
固定当前策略参数 $\theta^{(t)}$ 和标注者可靠性 $\eta_{k_i}^{(t)}$，对每个样本计算其观测标签为正确的后验概率 $w_i^{(t)}$（Equation 4）：
$$
w_i^{(t)} = \frac{p(y_{w,i}\succ^* y_{l,i} \mid x_i,\theta^{(t)})\,\eta_{k_i}^{(t)}}{p(y_{w,i}\succ^* y_{l,i} \mid x_i,\theta^{(t)})\,\eta_{k_i}^{(t)} + p(y_{l,i}\succ^* y_{w,i} \mid x_i,\theta^{(t)})\,(1-\eta_{k_i}^{(t)})}.
$$
该置信度综合了当前模型的偏好信号与标注者的历史可靠性：当模型强烈支持标注方向且标注者被视为可靠时，$w_i$ 趋近于1；反之则趋近于0，从而实现对可疑标签的软降权。定性案例表明，对于严重错误的标注（如违反输出格式的长篇回答被错误标记为选中），RE-PO可赋予极低的后验置信度（$w_i\approx0.037$，Table 5），并在后续训练中有效抑制其影响。

**M‑step（策略更新）**  
将 $w_i^{(t)}$ 作为自适应权重代入加权交叉熵损失，仅通过优化 $\theta$ 来最小化（Equation 5）：
$$
\mathcal{L}_{\mathrm{RE-PO}}(\theta) = -\sum_{i=1}^{N}\Bigl[ w_i^{(t)}\log p(y_{w,i}\succ^* y_{l,i} \mid x_i,\theta) + (1-w_i^{(t)})\log p(y_{l,i}\succ^* y_{w,i} \mid x_i,\theta) \Bigr].
$$
这一设计使得不可靠样本对梯度更新的贡献被大幅削减，而可靠样本的作用被保留甚至强化，从而在优化策略的过程中天然实现去噪。与标准硬标签损失相比，这一加权机制是RE-PO取得鲁棒性的核心因果旋钮。

**可靠性在线更新**  
由于实际训练以小批量进行，RE-PO采用指数移动平均（EMA）在每个批次后更新标注者可靠性 $\eta_k$（Equation 7）：
$$
\eta_k \leftarrow (1-\alpha)\,\eta_k + \alpha \cdot \frac{\sum_{i\in B\cap\mathcal{I}_k} w_i}{N_{k,B}},
$$
其中 $\alpha$ 为EMA动量。该式等价于将标注者的可靠性逐步收敛至其所有标注置信度的均值，从而在无全批量经验的条件下近似EM的正式更新（Equation 6）。消融实验表明，可靠性初始值 $\eta_0=0.9$ 和动量 $\alpha=0.1$ 能取得较好的性能（Table 4），但框架对这两个超参数存在一定敏感度，需根据场景进行调优。

### 输出与模块关系

整个框架的输出包含两方面：其一为经过对齐优化的策略模型 $\pi_\theta$，其二为推断所得的标注者可靠性分布 $\{\eta_k\}$。后者不仅能用于诊断数据质量，还可为后续数据清洗或标注流程提供反馈。在RE-PO内部，E‑step、M‑step和可靠性更新形成双向信息流：E‑step从策略和可靠性中获取信号，M‑step利用这些信号驱动策略进化，而策略的进化又反过来改变E‑step中的诱导偏好概率，从而可能修正置信度估计。这种交替优化机制使得框架能够逐步将噪声标签的权重推向可忽略的水平，同时强化高质量监督信号。

在实验验证中，RE-PO以插件形式应用于四种主流对齐算法（DPO、IPO、SimPO、CPO），在所有组合上均取得了相对于标准版本和标签平滑版本的稳定增益。例如，在Mistral‑7B上，RE‑DPO将AlpacaEval 2的长度控制胜率从28.5%提升至35.5%（提升7.0个百分点）；在Llama‑3‑8B上，RE‑IPO将原始胜率从41.6%提升至48.6%（提升7.0个百分点，Table 2）。在真实多标注者数据集MultiPref上，RE‑DPO同样展现出显著的提升，并成功识别出高可靠性标注者群体与被持续降权的噪声标注者（Figure 3）。合成噪声实验进一步证实，RE-PO估计的标注者可靠性与GPT‑4o参考真实值高度吻合（Figure 2），验证了其可靠性恢复能力。

### 关键依赖与局限

RE-PO的有效性依赖于几个关键条件。首先，要求训练数据包含标注者标识，因此无法直接用于无标注者信息的聚合数据集。其次，当基础策略与真实偏好严重偏离时，E‑step可能对错误标签赋予误导性的高置信度，导致EM迭代放大初始偏差，这一问题在当前工作中尚未通过理论或机制解决。此外，收敛性分析仅建立在全批量EM之上，实际采用的小批量EMA更新的收敛性质仍属开放问题。最后，RE-PO变体的训练时间较基础方法可能增加30%–40%（如SimPO，Table 8），在资源受限场景下需权衡计算开销与鲁棒增益。尽管如此，RE-PO凭借其概率建模和自适应加权机制，为大规模噪声偏好的对齐提供了一种通用且有效的框架，并可作为后续结合数据过滤、不确定性感知等策略的基础。

## 核心模块与公式推导

RE‑PO 框架的核心瓶颈在于大规模偏好数据普遍包含标注错误与噪声，传统方法平等对待所有样本，导致模型过度拟合不可靠监督。其因果调节杠杆是通过期望最大化（EM）推断每个偏好标签正确性的后验概率（置信度权重 $w_i$），并将该权重动态融入训练损失，从而自适应地强调可靠数据、弱化噪声信号。下文抽取实现这一机制的关键模块与公式，所有变量与推导均严格来自原文。

### 2.1 噪声模型与诱导偏好概率

RE‑PO 引入一个二值潜在变量 $z_i \in \{0,1\}$ 表示第 $i$ 个偏好标签是否真实（$z_i=1$ 表示标签正确），并假设不同标注者 $k$ 具有可学习的可靠性 $\eta_k \in [0,1]$，即 $p(z_i=1 \mid k_i=k) = \eta_k$。在此设定下，观测偏好 $y_{w,i} \succ_{k_i} y_{l,i}$ 的边缘概率通过边际化得到：

$$
p(y_{w,i}\succ_{k_i} y_{l,i} \mid x_i, \theta, \eta) = p(y_{w,i}\succ^* y_{l,i} \mid x_i, \theta)\,\eta_{k_i} + p(y_{l,i}\succ^* y_{w,i} \mid x_i, \theta)\,(1-\eta_{k_i}) \tag{3}
$$

其中 $p(y_w \succ^* y_l \mid x, \theta)$ 称为**诱导噪声自由偏好概率**，它由任意偏好损失函数推导而来，将模型对一对回复的偏好强度映射为概率：

$$
p(y_w \succ^* y_l \mid x, \theta) = \sigma\bigl( \mathcal{L}_{\mathrm{pref}}(x, y_l \succ y_w; \theta) - \mathcal{L}_{\mathrm{pref}}(x, y_w \succ y_l; \theta) \bigr) \tag{2}
$$

这里 $\mathcal{L}_{\mathrm{pref}}$ 可以是 DPO、IPO、SimPO、CPO 等任意对齐算法中的偏好损失分量（形式见表 1），$\sigma(\cdot)$ 为 sigmoid 函数。该概率揭示了 RE‑PO 的通用性：通过损失函数之差将模型对偏好的判别强度转化为软概率，进而允许对不同对齐算法统一建模噪声。

### 2.2 EM 算法：E 步与 M 步

RE‑PO 通过 EM 算法联合推断样本级置信度 $w_i$ 和策略参数 $\theta$。在每轮迭代中：

- **E 步（标签置信度推断）** 固定当前策略 $\theta^{(t)}$ 和标注者可靠性 $\eta_{k_i}^{(t)}$，计算每个样本标签正确的后验概率 $w_i$：

  $$
  w_i^{(t)} = \frac{p(y_{w,i}\succ^* y_{l,i} \mid x_i, \theta^{(t)})\,\eta_{k_i}^{(t)}}{p(y_{w,i}\succ^* y_{l,i} \mid x_i, \theta^{(t)})\,\eta_{k_i}^{(t)} + p(y_{l,i}\succ^* y_{w,i} \mid x_i, \theta^{(t)})\,(1-\eta_{k_i}^{(t)})} \tag{4}
  $$

  直观上，若模型认为给定偏好符合当前策略（$p(y_w\succ^* y_l)$ 高）且标注者历史可靠（$\eta_{k_i}$ 高），则 $w_i$ 趋近于 1；反之若模型认为反向偏好更强，或标注者极不可靠，则 $w_i$ 趋近于 0。$w_i$ 本质上是一种软加权系数，起到“可信度门控”的作用。

- **M 步（策略更新）** 利用 E 步得到的置信度 $w_i$ 构建加权交叉熵目标，最小化该损失以更新策略参数 $\theta$：

  $$
  \mathcal{L}_{\mathrm{RE-PO}}(\theta) = -\sum_{i=1}^{N}\Bigl[ w_i^{(t)}\log p(y_{w,i}\succ^* y_{l,i} \mid x_i, \theta) + (1-w_i^{(t)})\log p(y_{l,i}\succ^* y_{w,i} \mid x_i, \theta) \Bigr] \tag{5}
  $$

  该损失函数将标准偏好优化中对“正例”的硬赋值（$y_w$ 绝对偏好于 $y_l$）替换为两项加权对数项的平衡：置信度高的样本保持接近原方向优化，而置信度极低（$w_i \approx 0$）的样本则被大幅削弱甚至反向学习。这直接实现了对噪声标签的鲁棒脱敏。

### 2.3 标注者可靠性的在线更新

在全批量 EM 框架下，标注者可靠性 $\eta_k$ 的闭式更新为：

$$
\eta_k^{(t+1)} = \frac{\sum_{i \in \mathcal{I}_k} w_i^{(t)}}{N_k} \tag{6}
$$

即每个标注者的可靠性等于其所有标注样本 E 步置信度的平均值。然而实际训练采用小批量随机梯度下降，因此 RE‑PO 改为每次迭代用指数移动平均（EMA）在线维护 $\eta_k$：

$$
\eta_k \leftarrow (1-\alpha)\,\eta_k + \alpha \cdot \frac{\sum_{i \in B \cap \mathcal{I}_k} w_i}{N_{k,B}} \tag{7}
$$

其中 $B$ 为当前小批量，$N_{k,B}$ 为 $B$ 中由标注者 $k$ 标注的样本数，$\alpha$ 为 EMA 动量。消融实验表明，$\eta_0 = 0.9$ 和 $\alpha = 0.1$ 在 Mistral‑7B 上取得最佳性能，过高的初始可靠性（如 $0.99$）或过大动量会损害去噪效果（Table 4），反映出系统对超参数具有一定的敏感性。

### 2.4 核心机制总结

RE‑PO 通过上述公式将对抗噪声的机制分解为两个相互促进的信号通路：E 步利用当前策略的语义校准能力识别可疑标签，产生细粒度的样本置信度 $w_i$；M 步将这些置信度转化为自适应权重，抑制噪声梯度的同时保留干净信号。标注者可靠性 $\eta_k$ 的渐进更新进一步提供了群体层面的先验知识，使模型能够在多标注者环境下自动识别并降权低质量标注源。理论上，当偏好概率分布于 $p^\star \neq 0.5$ 时，全批量 EM 的可靠性估计可以收敛到真值（Theorem 4.1），保证了该机制在最简情形下的可识别性。

## 实验与分析

大规模偏好数据集中普遍存在的标注错误和噪声会导致标准对齐方法（如 DPO、IPO）过拟合不可靠的监督信号，显著降低对齐性能与泛化能力。RE-PO 通过期望最大化（EM）推断每个偏好标签正确性的后验概率（置信度权重 $w_i$），并将该权重动态融入训练损失，自适应地强调可靠数据、弱化噪声数据，从而实现了噪声鲁棒的对齐过程。以下从主结果、消融、可靠性验证、定性分析及失败模式几个方面解析关键实验发现。

### 主结果：跨算法与跨模型的稳健提升

在 AlpacaEval 2 基准上，RE-PO 作为即插即用的鲁棒性层，对 DPO、IPO、SimPO、CPO 四个算法族均带来了显著且一致的性能增益（Table 2）。对于 Mistral-7B-Instruct，RE-DPO 将长度控制胜率（LC）从标准 DPO 的 28.5% 提升至 35.5%（+7.0 个百分点），原始胜率（WR）从 28.6% 提升至 33.0%（+4.4 个百分点），这是所有变体中最大的绝对提升。在 Llama-3-8B-Instruct 上，RE-IPO 将 LC 从 43.6% 提升至 48.3%（+4.7 个百分点），WR 从 41.6% 提升至 48.6%（+7.0 个百分点），展现了跨算法和跨基模型的稳定增益。值得注意的是，RE-PO 增强后的 DPO 在 Llama-3-8B 上达到 LC/WR 分别为 44.1%/46.2%，显著优于同样面向噪声的 rDPO（37.3%/35.4%）和 Hölder-DPO（39.3%/38.2%），这表明显式地对标注者可靠性建模并据此对每个样本进行软加权，比全局噪声率校正或纯损失函数层面的抗噪策略更为有效。

![[assets/figures/papers/iclr26_0013_jDKpOvTCM8_RE-PO_Robust_Enhanced_Policy_Optimization_as_a_G/figures/003_Table_2.jpg]]
*Table 2: Performance comparison on AlpacaEval 2 for Mistral-7B-Instruct-v0.2 and Meta-Llama-3-8B-Instruct fine-tuned on UltraFeedback-based preference datasets. Metrics reported are LC (Length-Controlled Win Rate) and WR (Raw Win Rate), both in percentage points. The table presents reference Baselines (bottom) alongside four algorithm families (DPO, IPO, SimPO, CPO). For each family, we compare the Standard implementation, the variant with Label Smoothing (w/ LS), and RE-PO (w/ RE-PO). Bold denotes the best result within each family for a given backbone*

在真实多标注者数据集 MultiPref 上的实验进一步验证了 RE-PO 在异构噪声下的鲁棒性（Table 3）。在该设定中，每个偏好对带有明确的标注者 ID。在 Llama-3-8B-Instruct 上，RE-DPO 相较于标准 DPO 将 LC/WR 从 36.7%/39.3% 分别提升至 41.1%/44.4%（+4.4/+5.1 个百分点）；在 Mistral-7B-Instruct 上，相应指标亦从 28.8%/26.4% 提高至 31.8%/28.8%（+3.0/+2.4 个百分点）。使用 DeepSeek-V3.2-Exp 作为评判模型时，RE-DPO 同样保持一致的提升趋势（Table 7），表明结论对评判器选择不敏感。

![[assets/figures/papers/iclr26_0013_jDKpOvTCM8_RE-PO_Robust_Enhanced_Policy_Optimization_as_a_G/figures/004_Table_3.jpg]]
*Table 3: Performance of DPO and RE-DPO on AlpacaEval 2 when trained on the MultiPref dataset (Miranda et al., 2024). Results are reported as LC / WR (%) for Mistral-7B-Instruct-v0.2 and Meta-Llama-3-8B-Instruct*

![[assets/figures/papers/iclr26_0013_jDKpOvTCM8_RE-PO_Robust_Enhanced_Policy_Optimization_as_a_G/figures/009_Table_7.jpg]]
*Table 7: Performance of DPO and RE-DPO on AlpacaEval 2 when trained on the Multi-Pref dataset (Miranda et al., 2024) and evaluated with DeepSeek-V3.2-Exp as the judge model. Results are reported as LC / WR (%) for Mistral-7B-Instruct-v0.2 and Meta-Llama-3-8B-Instruct*

### 消融实验：超参数敏感性与组件贡献

RE-PO 的核心超参数包括初始标注者可靠性 $\eta_0$ 和小批量 EMA 更新的动量 $\alpha$。Table 4 的消融结果显示，RE-DPO 在 Mistral-7B-Instruct 上的最佳设置是 $\eta_0 = 0.9$ 且 $\alpha = 0.1$。当 $\eta_0$ 过高（如 0.99，过度自信）或过低（如 0.55，过于保守）时，LC/WR 均有明显下降，说明初始先验需与模型实际的对齐程度匹配，否则 E-step 推断的置信度 $w_i$ 可能向错误方向偏移。动量值极端化同样会损害性能：$\alpha = 0.001$ 时可靠性更新过慢，无法及时适配噪声结构；$\alpha = 1.0$ 时更新过于激进，易受单批噪声冲击。这一敏感性源于小批量随机优化下 EM 迭代的内在波动，实践中需针对新场景进行适度调参。

![[assets/figures/papers/iclr26_0013_jDKpOvTCM8_RE-PO_Robust_Enhanced_Policy_Optimization_as_a_G/figures/005_Table_4.jpg]]
*Table 4: Ablation study on the initial annotator reliability (η0) and the EMA momentum (α). Results are reported for RE-DPO on Mistral-7B-Instruct-v0.2 trained on UltraFeedback-based data, evaluated on AlpacaEval 2 (LC / WR) and Arena-Hard (WR), all in percentage points. The best-performing settings used in our main experiments are highlighted*

与标签平滑（Label Smoothing）的对比构成一项重要的组件消融。Table 2 显示，在所有四个算法族和两个基模型上，RE-PO 变体均一致优于对应的标签平滑变体。标签平滑统一地软化全体标签，无法区分真实偏好与噪声，而 RE-PO 则通过 E-step 为每个样本计算独立的软置信度 $w_i$，对可疑标注实施精准降权，从而更有效地阻断噪声信息的传播。

### 可靠性估计的实证验证（重要图表结论）

**受控合成噪声实验（Figure 2）** 直接检验了 RE-PO 能否从受控的标注错误中恢复出真实的标注者可靠性。实验以 GPT-4o 在 UltraFeedback 上的偏好标注作为真实可靠性 $\eta_{\text{GPT-4o}}$ 的参考，通过向特定标注者的数据副本注入不同程度的合成噪声来模拟多种可靠性水平。在单个标注者设置中，RE-PO 估计的可靠性与预设的真实可靠性高度吻合；在双标注者设置中，即便标注者 1 的数据无噪声，而标注者 2 的数据被逐步添加噪声，RE-PO 仍能准确估计出二者的可靠性，且标注者 2 的估计值随注入噪声率上升而单调下降。这证明 EM 框架能够在模型仅近似校准的情况下，可靠地恢复标注者质量，进而为后续的加权损失提供有效指导。

![[assets/figures/papers/iclr26_0013_jDKpOvTCM8_RE-PO_Robust_Enhanced_Policy_Optimization_as_a_G/figures/007_Figure_2.jpg]]
*Figure 2: Empirical verification of annotator reliability estimation under controlled synthetic noise. Ground-truth reliability ( $\eta \mathrm { G P T - 4 o ) }$ is established using GPT-4o’s labels on UltraFeedback-derived preference pairs, and different reliability levels are simulated by injecting synthetic noise into copies of the dataset. In the single-annotator setting (a), a single annotator’s dataset is perturbed with varying noise rates. In the two-annotator setting (b), Annotator 1 uses the original data with no added noise, while noise is progressively added to Annotator 2’s data. The plots compare ground-truth reliabilities (solid lines) with RE-PO-estimated reliabilities (dashed lines), s...

**标注者可靠性分布（Figure 3）** 呈现了在 MultiPref 训练集上学得的后验标注者可靠性直方图。对于 Mistral-7B 和 Llama-3-8B 两种骨干模型，以及 $\eta_0 \in \{0.80, 0.90, 0.95, 0.99\}$ 四种先验设置，RE-PO 均识别出一个高可靠性的标注者主体，同时判明一组被持续低权重的尾部噪声标注者。该模式对不同先验和骨干表现出较好的鲁棒性，说明 RE-PO 的加权机制能够有效利用标注者结构辅助去噪。

### 定性案例：低置信度样本捕捉标识

Table 5 与 Table 6 分别给出了主题分类和代词-短语识别任务中的低置信度代表性样本。在主题分类案例中，数据集将第一个响应标记为优，第二个为劣；但模型判断两个响应均正确完成任务，且第一个响应因输出冗长（附带额外对话内容）而违反预期格式。RE-PO 对该标签赋予的后验置信度仅为 $w_i \approx 0.037$，将其识别为疑似错误标注并在训练中大幅降低其权重。这一定性证据表明，RE-PO 的软加权机制不仅能抵御随机噪声，还能捕捉到由标注者疏忽或隐性偏好引发的系统性偏差。

### 失败模式与局限性

尽管 RE-PO 在常规设置下表现强劲，但若干失败模式和局限性仍需关注：

1. **策略初始严重不对齐时的失效风险**：如果基础模型与真实偏好偏离较大，E-step 可能会对错误标签给出误导性的高置信度，使 EM 迭代陷入噪声强化的正反馈，导致去噪失败。该风险在理论分析中已被指出，但目前缺乏专门的实验量化验证，需要在实际部署中对初始策略质量进行评估。
2. **对标注者 ID 的强依赖**：RE-PO 假设训练数据中每个偏好对附带标注者标识，以构建个人可靠性参数 $\eta_k$。对于无此信息的聚合数据集，方法无法直接应用，扩展至自动标注者分组尚需进一步研究。
3. **小批量随机 EM 收敛性质未建立**：理论收敛保证（Theorem 4.1）基于全批量 EM 迭代，而实际算法采用小批量 EMA 更新，其收敛性和偏差行为的理论刻画仍然缺失。
4. **计算开销因目标函数而异**：Table 8 显示，SimPO 的 RE-PO 变体训练时间增加了约 30%–40%（主要来自额外的对数概率计算），而 DPO 和 IPO 的变体因损失形式特点甚至略有加速。因此，在计算资源受限的场景下，部分增强变体可能不够经济。
5. **超参数需谨慎调优**：消融实验已表明 $\eta_0$ 和 $\alpha$ 对性能影响显著，迁移到新数据集或新基模型时需重新搜索较优组合，增加了工程成本。

综上，RE-PO 通过自适应样本置信度加权，以较小的工程代价有效缓解了偏好噪声的对齐瓶颈，在多个基准上实现了显著且一致的提升，但应对策略初始偏差、无标注者 ID 场景及进一步提升小批量 EM 的稳定性仍是后续工作的重要方向。

## 方法谱系与知识库定位

RE-PO 并非一种全新的对齐算法，而是一个**通用噪声鲁棒增强框架**，可薄薄包裹于现有偏好优化损失（DPO、IPO、SimPO、CPO）之上，以应对大规模偏好数据中普遍存在的标注错误与噪声。该框架通过期望最大化（EM）推断每个样本标签正确的后验概率 $w_i$，并将其作为软权重动态调节损失，从而在训练过程中**自适应强调可靠数据、弱化噪声数据**。这一思想将标签正确性建模为潜在变量，与以往方法形成鲜明对照。

### 与基线方法及后续工作的关系

- **相对于标准 DPO/IPO/SimPO/CPO**：RE-PO 的唯一核心变化是将原始损失（硬标签、平等对待所有样本）替换为加权 RE-PO 损失（公式 5），其中权重 $w_i^{(t)}$ 由 E-step 计算（公式 4）。在 Mistral-7B 和 Llama-3-8B 的 UltraFeedback 训练中，RE‑DPO 将 AlpacaEval 2 长度控制胜率（LC）从 28.5% 提升至 35.5%（+7.0pp），原始胜率（WR）从 28.6% 提升至 33.0%（Table 2）；相同趋势在所有四个损失族和两个基模型上一致出现。这表明**RE-PO 对各类对齐损失均能提供即插即用的鲁棒性增益**。
- **相对于标签平滑（Label Smoothing）及其他鲁棒偏好方法**：标签平滑通过对硬标签注入均匀噪声提供一种全局正则化，但无法区分每个样本的可靠程度。rDPO 需要已知全局噪声率，Hölder-DPO 通过下降损失应对异常值，但二者均不显式建模标注者差异。RE-PO 通过**引入潜在变量 $z_i$ 和标注者可靠性参数 $\eta_k$**，实现样本级自适应加噪，优于上述方法（Table 2 中 RE-PO 在所有对比中均显著优于“w/ LS”版，且 Llama‑3‑8B 上 RE‑DPO 的 44.1/46.2 远高于 rDPO 的 37.3/35.4 和 Hölder‑DPO 的 39.3/38.2）。
- **在多标注者数据上的表现**：当训练数据包含多个标注者（MultiPref 数据集）时，RE‑DPO 在所有基模型上均超越标准 DPO（Llama‑3‑8B 的 LC/WR 从 36.7/39.3 升至 41.1/44.4；Mistral‑7B 从 28.8/26.4 升至 31.8/28.8，Table 3）。学习到的标注者可靠性分布呈现出**高可靠性多数与持续降权的噪声标注者**，且该模式对先验设置和基模型具有鲁棒性（Figure 3）。
- **可靠性估计的实证验证**：在受控合成噪声实验中，RE-PO 估计的标注者可靠性与 GPT‑4o 作为参考的真实可靠性高度吻合，证明了 EM 程序恢复可靠性参数的能力（Figure 2）。定性案例（Table 5–6）进一步显示，RE-PO 能对疑似错误标注（如违反输出格式的长篇回答）赋予极低置信度（$w_i \approx 0.037$），并在训练中有效降低其权重。

### 适用边界与局限

尽管 RE-PO 在多个基准上展现出一致的增益，其应用仍受到以下明确定义的边界约束：

1. **对标注者 ID 的依赖**：方法假设每个偏好对都附有标注者标识，这使得它无法直接应用于缺乏显式标注者信息的聚合数据集。若需扩展，必须借助聚类或表征学习等手段自动发现潜在标注者组，该方向仍是开放问题。
2. **EM 初始化敏感性与策略严重不对齐时的失效风险**：当基础模型与真实偏好偏离较大时，E-step 可能对错误标签赋予**误导性高置信度**，导致去噪失效甚至放大噪声。目前缺乏一种系统性的稳健初始化或混合策略来防止这一“错误传播”。
3. **超参数敏感**：消融实验（Table 4）表明，初始可靠性 $\eta_0$ 和 EMA 动量 $\alpha$ 对最终性能有显著影响。最佳设置为 $\eta_0=0.9$ 和 $\alpha=0.1$，过度自信（0.99）或过于保守（0.55）以及极端动量均会导致性能下降。这意味着**针对新场景需要重新调优**，缺乏一次设定即可通用的默认值。
4. **理论保证与实际算法的差距**：收敛性分析（Theorem 4.1）建立在全批量 EM 上，而实际采用的小批量随机 EMA 更新（公式 7）的收敛性质和估计偏差尚未完全刻画。因此，大规模训练中可靠性估计的稳定性虽有实证支持，但缺乏严格理论保障。
5. **计算开销因算法而异**：不同基础损失的 RE-PO 变体训练时间变化不一：DPO 和 IPO 的 RE-PO 变体甚至减少了墙钟时间（如 DPO 上 Mistral‑7B 从 7138s 降至 6588s），但 SimPO 的 RE-PO 变体增加了 30%–40% 的训练时间（Table 8），可能限制在资源受限场景下的应用。

### 开放问题

- **严重不对齐下的稳健 EM 设计**：当策略初始化极差时，如何构建混合策略（如先以标准损失预热，再切换至 RE-PO）或引入课程学习，以防止 E-step 产生系统性偏差？
- **无标注者 ID 场景的扩展**：能否通过聚类标注者行为或利用 LLM 本身的自一致性推断潜在标注者组，使 RE-PO 适用于目前大量无 ID 的偏好数据？
- **小批量随机 EM 的理论与方差控制**：亟需理论分析刻画 EMA 更新下 $\eta_k$ 的偏差与方差，以及引入方差削减技术（如控制变量）的可能性。
- **与数据筛选策略的协同**：RE-PO 本质上在优化目标中执行“软删除”，而选择性采样或重采样等数据过滤方法可作为互补。将二者结合能否在几乎不增加计算负担的前提下进一步提升对齐质量？
- **更大规模模型与多样化评判的验证**：目前实验集中在 7B–8B 模型和 AlpacaEval 2 / Arena-Hard 评判基准上，其在 70B 级别模型以及更广泛评判（如基于 LLM 的自动评测、安全对齐评判）中的增益幅度和可靠性恢复能力仍需检验。

## 原文 PDF

![[paperPDFs/ICLR_2026/RE_PO_Robust_Enhanced_Policy_Optimization_as_a_General_Framework_for_LLM_Alignment.pdf]]
