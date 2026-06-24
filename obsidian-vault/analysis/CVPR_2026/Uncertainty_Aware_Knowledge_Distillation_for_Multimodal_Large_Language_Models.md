---
title: Uncertainty-Aware Knowledge Distillation for Multimodal Large Language Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Uncertainty_Aware_Knowledge_Distillation_for_Multimodal_Large_Language_Models.pdf
project_link: null
code_link: "https://github.com/Jingchensun/beta-kd"
aliases:
- BKBWKD
- UAKDMLLM
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 将教师监督形式化为学生激活上的 Gibbs 先验，并通过 Laplace 近似推导出封闭形式的不确定性权重 β。该权重由轻量网络预测，可自适应地在任务级或实例级调节蒸馏损失的强度，从而消除人工调参。
primary_logic: 知识蒸馏可以被统一解释为贝叶斯框架下的最大后验（MAP）估计问题——教师的输出作为学生激活的概率先验，交叉熵为似然，联合优化即等价于最小化带有自适应精度的蒸馏目标，无需手动设定损失权重。
claims:
- 在 ScienceQA 数据集上，实例级 Beta-KD (Cosine-Probs) 将 VQA 准确率从纯 CE 基线的 48.4% 提升至 54.9%，提升幅度超过 6 个百分点。
- 在 MMEP 基准上，Beta-KD (Instance) 相较于 Align-KD 提升 +54.1；在 TextVQA 上相较基线提升 +2.9，展示了跨数据集和跨模型架构的稳健增益。
- ScienceQA 上 VQA-Acc (%) = 54.9
- MMEP 上 Perception Score = 1343.0 (Beta-KD Instance over Align-KD)
---

# Uncertainty-Aware Knowledge Distillation for Multimodal Large Language Models

> [!tip] 核心洞察
> 知识蒸馏可以被统一解释为贝叶斯框架下的最大后验（MAP）估计问题——教师的输出作为学生激活的概率先验，交叉熵为似然，联合优化即等价于最小化带有自适应精度的蒸馏目标，无需手动设定损失权重。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向多模态大语言模型的不确定性感知知识蒸馏 |
| 英文题名 | Uncertainty-Aware Knowledge Distillation for Multimodal Large Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.21426) · [Code](https://github.com/Jingchensun/beta-kd) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Beta-KD (Beta-weighted Knowledge Distillation) |
| Dataset | ScienceQA, MMEP, MMBench_dev, TextVQA |

> [!tip] 效果简介
> - ScienceQA 上，VQA-Acc (%) 54.9 vs 48.4 (Cross-Entropy without KD) (+6.5)。
> - MMEP 上，Perception Score 1343.0 (Beta-KD Instance over Align-KD) vs Align-KD (+54.1)。
> - MMBench_dev 上，Accuracy 60.2 (Beta-KD Instance over Cosine KD) vs Cosine KD (+3.1)。

## 概述

多模态大语言模型（MLLM）的知识蒸馏面临一个核心瓶颈：来自真实标签的交叉熵损失与来自教师模型的多个蒸馏损失构成异构监督信号，它们的尺度、梯度和优化动态各不相同，手动平衡这些信号极其困难，且固定权重无法适应样本或任务的不确定性。

本文提出 **Beta-KD (Beta-weighted Knowledge Distillation)**，一种不确定性感知的知识蒸馏框架。其核心洞察是将知识蒸馏统一解释为贝叶斯框架下的最大后验（MAP）估计——教师的输出作为学生激活上的 Gibbs 先验，交叉熵作为数据似然，联合优化等价于最小化带有自适应精度的蒸馏目标。通过 Laplace 近似，该方法推导出封闭形式的不确定性权重 β，由一个轻量网络预测，可在任务级或实例级自适应调节蒸馏损失的强度，从而消除人工调参。

在方法谱系上，Beta-KD 区别于传统的固定权重蒸馏（如 **Forward KL**，Hinton et al., NIPS 2015；**Reverse KL**，Gu et al., ICLR 2024）和跨模态对齐蒸馏（**Align-KD**，Feng et al., CVPR 2025），将损失平衡问题转化为可学习的贝叶斯推断。实验表明，在 ScienceQA 数据集上，实例级 Beta-KD 将 VQA 准确率从纯交叉熵基线的 48.4% 提升至 54.9%（+6.5 个百分点）；在 MMEP 基准上相较 Align-KD 提升 +54.1；在 TextVQA 上提升 +2.9，且不确定性网络仅引入总参数量 0.03% 的开销，训练速度与无加权方案几乎一致。

## 背景与动机

多模态大语言模型（MLLM）在视觉问答、图像描述等任务上取得了显著进展，但其庞大的参数量和计算开销严重制约了在资源受限场景下的部署。知识蒸馏（Knowledge Distillation, KD）是解决这一矛盾的主流范式——通过让轻量学生模型模仿大型教师模型的输出分布，将教师的知识压缩迁移至学生。然而，在多模态蒸馏的实践中，一个根本性的难题始终未被有效解决：**异构监督信号的平衡问题**。

具体而言，学生模型在训练过程中同时接收两类性质迥异的监督信号：来自真实标签的交叉熵损失（数据监督）和来自教师模型的蒸馏损失（教师监督）。在多模态场景下，蒸馏损失往往不止一个——可能同时包含 KL 散度、特征对齐、概率空间匹配等多种损失项。这些损失具有不同的数值尺度、梯度动态和收敛速度，手动为其分配固定权重（如 $\lambda=1$）不仅需要大量调参经验，更关键的是，固定权重无法适应不同样本或任务的不确定性差异。如 Figure 1(a) 所示，传统 KD 框架难以在“从数据学习”与“从教师学习”之间取得自适应平衡。

现有的蒸馏方法——无论是传统的正向 KL 散度（**FKL**, Hinton et al., NIPS 2015）、缓解分布不匹配的逆向 KL 散度（**RKL**, Gu et al., ICLR 2024）、跨模态对齐蒸馏（**Align-KD**, Feng et al., CVPR 2025），还是基于余弦相似度的概率空间蒸馏——均沿用手动设定损失权重的范式。这种“一刀切”的策略忽视了训练过程中学生模型状态的变化，也未能捕捉样本间的异质性，导致蒸馏效率受限。

本文的核心动机在于：**能否从根本上消除蒸馏过程中的手动调参，使损失权重能够根据学生模型的不确定性自适应调节？** 为此，我们提出 Beta-KD——一个不确定性感知的知识蒸馏框架。其核心洞察是：知识蒸馏可以被统一解释为贝叶斯框架下的最大后验（MAP）估计问题——教师的输出作为学生激活上的 Gibbs 先验，交叉熵作为数据似然，联合优化即等价于最小化带有自适应精度的蒸馏目标。通过 Laplace 近似，我们推导出封闭形式的不确定性权重 $\beta$，并由轻量网络预测，从而在任务级或实例级实现完全自适应的损失平衡（Figure 1(b)）。

## 核心创新

### 瓶颈洞察：多模态知识蒸馏中的异构监督平衡难题

多模态大语言模型的知识蒸馏面临一个根本性挑战：来自数据（交叉熵损失）和教师模型（多个蒸馏损失）的监督信号具有**不同的尺度、梯度动态和优化方向**。传统做法通过手动设定固定权重 $\lambda$ 来组合这些损失：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{CE}} + \lambda \mathcal{L}_{\mathrm{KD}}$$

然而，这种静态平衡策略存在两个致命缺陷：一是**调参极其困难**，需要大量试错来寻找合适的 $\lambda$；二是**固定权重无法适应样本间的异质性**——某些样本可能更需要教师引导，而另一些样本的教师信号可能充满噪声。该瓶颈在多模态场景下尤为突出，因为视觉-语言的跨模态对齐进一步放大了监督信号的不匹配程度。

### 核心创新：将知识蒸馏重新解释为贝叶斯最大后验估计

Beta-KD 的核心洞察在于**对知识蒸馏过程进行贝叶斯重铸**：将教师的输出建模为学生激活上的 **Gibbs 先验**，将交叉熵视为数据似然，从而将整个蒸馏过程统一为**最大后验（MAP）估计**问题。

具体而言，教师监督被形式化为一个以能量函数 $\ell(a^s; a^t)$ 为核心的未归一化先验分布：

$$\tilde{p}(a^s \mid a^t, \beta) \propto \exp[-\beta \ell(a^s; a^t)], \quad \beta > 0$$

其中 $\beta$ 作为**精度参数**（precision parameter）控制先验的集中程度——直观上，$\beta$ 越大表示教师先验越强，学生应更多地模仿教师。通过 MAP 推断，优化目标等价于：

$$\min_{a^s} \underbrace{-\log p(y \mid a^s)}_{\text{交叉熵}} + \beta \underbrace{\ell(a^s; a^t)}_{\text{蒸馏损失}} + \log Z_{\beta}(a^t)$$

这一重铸的关键意义在于：**$\beta$ 从人工设定的超参数转变为具有明确贝叶斯解释的不确定性度量**——它量化了教师先验的“可信度”。

### 关键机制：Laplace 近似与摊销优化的自适应权重学习

上述 MAP 目标中的配分函数 $Z_{\beta}(a^t)$ 通常难以计算。Beta-KD 通过 **Laplace 近似**推导出封闭形式的可计算代理目标：

$$\min_{a^s} -\log p(y \mid a^s) + \beta \ell(a^s; a^t) - \frac{d}{2}\log \beta$$

其中 $-\frac{d}{2}\log \beta$ 项作为**正则化器**，防止 $\beta$ 在优化过程中发散至无穷大（即防止学生完全盲从教师）。这一近似将贝叶斯推断转化为端到端可优化的损失函数。

在此基础上，Beta-KD 引入**摊销优化网络** $g_{\phi}(h(x))$——一个轻量级 MLP，以学生模型的隐藏表示 $h(x)$ 为输入，预测实例级的不确定性权重 $\beta(x)$。最终联合优化目标为：

$$\min_{\theta, \phi} \mathcal{L}_{\mathrm{CE}}(\theta) + g_{\phi}(h(x)) \ell(\theta) - \frac{d}{2}\log g_{\phi}(h(x))$$

这一设计的核心优势在于：
- **自适应粒度**：支持任务级（全局标量 $\beta$）和实例级（逐样本 $\beta(x)$）两种不确定性建模，后者能捕捉数据内部的异质性和噪声分布；
- **零手动调参**：完全消除了传统 KD 中损失权重的超参数搜索过程；
- **极小开销**：不确定性网络仅引入总参数量 **0.03%** 的额外计算，训练速度与无加权方案几乎一致（如 Align-KD 1.82 it/s vs. Beta-KD Instance 1.85 it/s，见 Table 6）。

### 与基线方法的本质差异

| 维度 | 传统 KD（如 FKL, RKL） | Align-KD | **Beta-KD** |
|------|----------------------|----------|-------------|
| 损失权重 | 手动固定 $\lambda$ | 手动固定 | **自适应学习 $\beta$** |
| 理论基础 | 信息论散度 | 跨模态对齐 | **贝叶斯 MAP 估计** |
| 不确定性建模 | 无 | 无 | **任务级 / 实例级** |
| 多损失扩展 | 需逐一手动调权 | 需逐一手动调权 | **统一框架自动平衡** |

值得注意的是，Beta-KD 的框架对底层蒸馏损失的具体形式（FKL、RKL、Cosine-Probs 等）是**正交的**——它不改变损失函数本身，而是提供了一种通用的自适应加权机制。这使其能够无缝集成到现有的各种 KD 方案中，在 ScienceQA 上以 Cosine-Probs 为基底的实例级 Beta-KD 将 VQA 准确率从纯 CE 基线的 48.4% 提升至 **54.9%**（+6.5 个百分点），并在 MMEP、TextVQA 等六个基准上展现了跨数据集和跨模型架构的稳健增益。

## 整体框架

Beta-KD 将多模态大语言模型的知识蒸馏重新形式化为贝叶斯框架下的最大后验（MAP）估计问题。其核心洞察在于：教师模型的输出可以被解释为学生激活上的 Gibbs 先验，而交叉熵损失则作为数据似然，二者的联合优化等价于最小化带有自适应精度的蒸馏目标，从而消除了传统方法中手动设定损失权重的需求。

### 框架总览

整个 Beta-KD 框架由五个核心模块构成，形成一条从教师监督到学生自适应学习的完整流水线：

1. **教师模型 $f_t$**：以 MobileVLM-7B 作为固定的教师网络，提供冻结的教师激活（logits 或 softmax 后的概率分布），作为学生学习的先验信息源。

2. **学生模型 $f_s$**：以 MobileVLM-1.7B 作为待训练的学生网络，在教师监督与真实标签的联合指导下进行参数更新。

3. **Gibbs 先验形式化**：将教师-学生之间的差异建模为能量函数 $\ell(a^s; a^t)$，并据此定义 Gibbs 分布作为先验：
   $$\tilde{p}(a^s \mid a^t, \beta) \propto \exp[-\beta \ell(a^s; a^t)], \quad \beta > 0$$
   其中 $\beta$ 是控制先验强度的精度参数——$\beta$ 越大，学生激活越被强制靠近教师；$\beta$ 越小，学生越依赖数据自身的似然信号。

4. **不确定性网络 $g_\phi(h(x))$**：一个轻量级 MLP，以学生中间表示 $h(x)$ 为输入，通过摊销优化（amortized optimization）预测实例级（或任务级）的不确定性权重 $\beta$。该网络仅引入总参数量 0.03% 的开销，却能替代人工调参，实现动态的自适应损失平衡。

5. **MAP 目标函数**：经 Laplace 近似后，得到可计算的代理目标：
   $$\min_{a^s} -\log p(y \mid a^s) + \beta \ell(a^s; a^t) - \frac{d}{2}\log \beta$$
   第一项为标准交叉熵损失，第二项为 $\beta$ 加权的蒸馏损失，第三项 $- \frac{d}{2}\log \beta$ 作为正则项防止 $\beta$ 发散。这一形式从理论上统一了数据监督与教师监督的优化目标。

### 输入输出流

给定多模态输入 $x$（图像与文本），学生网络生成逐 token 的激活 $a^s$（可以是 logits $\mathbf{z}^s$ 或 softmax 后的概率 $\mathbf{p}_s^{\tau_s}$）。教师网络同步提供对应的教师激活 $a^t$。系统同时接收两条监督路径：

- **数据路径**：真实标签 $y$ 通过交叉熵损失 $\mathcal{L}_{\text{CE}}$ 提供硬监督。
- **教师路径**：教师激活 $a^t$ 通过能量函数 $\ell(a^s; a^t)$ 提供软监督，其强度由不确定性网络预测的 $\beta$ 动态调节。

两条路径的损失在 MAP 目标中自动加权求和，反向传播同时更新学生参数 $\theta$ 和不确定性预测器参数 $\phi$，实现端到端的联合优化。

### 与传统 KD 的关键区别

传统知识蒸馏的总目标为 $\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{CE}} + \lambda \mathcal{L}_{\text{KD}}$，其中 $\lambda$ 是手动选择的固定超参数。这种方法面临两个根本困难：一是来自数据（交叉熵）和来自教师（蒸馏损失）的异构监督信号具有不同的尺度、梯度与优化动态，手动平衡极其困难；二是固定权重无法适应不同样本或任务的不确定性差异。

Beta-KD 通过贝叶斯视角将 $\lambda$ 替换为可学习的 $\beta$，并引入 $\log \beta$ 正则项，使得权重能够根据输入样本的难易程度、教师的置信度以及训练阶段自动调整。如图 1 所示，传统 KD 中教师信号的权重是静态的，而 Beta-KD 通过摊销优化网络为每个实例（或任务）预测专属的 $\beta$ 值，实现了从“一刀切”到“因材施教”的转变。

### 能量函数的选择空间

框架中的能量函数 $\ell(a^s; a^t)$ 具有灵活的选择空间，既可以定义在 logit 空间（如 MSE-Logits、Cosine-Logits），也可以定义在概率空间（如 Forward KL、Reverse KL、Cosine-Probs）。实验表明（Table 1），在概率空间进行蒸馏（尤其是 Cosine-Probs）显著优于在 logit 空间，说明对于多模态生成任务，匹配输出分布比匹配内部表示更为有效。Beta-KD 的不确定性加权机制与具体能量函数的选择是正交的——无论选用何种散度或距离度量，$\beta$ 都能自适应地调节其贡献强度。

### 补充图表

![[assets/figures/papers/paper_list_l2707_https_arxiv_org_abs_2603_21426/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed Beta-KD framework. (a) Conventional KD is hard to balance the learning from data and the learning from teacher signals. (b) Our method introduces an uncertainty-aware weighting framework by recognizing teacher supervision as a Gibbs prior, which naturally induces the prediction of the weights*

## 核心模块与公式推导

### 3.1 问题建模：将知识蒸馏形式化为贝叶斯推断

Beta-KD 的核心洞察在于将知识蒸馏重新解释为一个贝叶斯框架下的最大后验（MAP）估计问题。在多模态大语言模型的蒸馏中，学生模型同时接收两类异构监督信号：来自真实标签的交叉熵损失（数据似然）和来自教师模型的蒸馏损失（先验知识）。传统方法通过手动设定的固定权重 $\lambda$ 来平衡这两类信号：

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{CE}} + \lambda \mathcal{L}_{\mathrm{KD}}
$$

其中，交叉熵损失 $\mathcal{L}_{\mathrm{CE}}$ 定义为：

$$
\mathcal{L}_{\mathrm{CE}} = -\frac{1}{L_y}\sum_{n=1}^{L_y}\sum_{k=1}^{|\mathcal{V}|} e_k(y_n)\log p_{s,k}^{\tau_s}(y_n | x, y_{<n}; \theta)
$$

蒸馏损失 $\mathcal{L}_{\mathrm{KD}}$ 通过散度 $\mathbb{D}$ 匹配学生与教师的概率分布：

$$
\mathcal{L}_{\mathrm{KD}} = \frac{1}{L_y}\sum_{n=1}^{L_y} \mathbb{D}\big(\mathbf{p}_t^{\tau_t} \| \mathbf{p}_s^{\tau_s}(\cdot | x, y_{<n}; \theta) \big)
$$

然而，这两类信号的尺度、梯度与优化动态存在本质差异，手动平衡极其困难。Beta-KD 通过引入贝叶斯视角，将教师监督形式化为学生激活上的 Gibbs 先验，从而将权重 $\lambda$ 转化为具有明确概率意义的不确定性参数 $\beta$。

### 3.2 教师先验的 Gibbs 形式化

Beta-KD 将教师-学生差异建模为能量函数 $\ell(a^s; a^t)$，并据此定义教师引导的 Gibbs 先验分布。未归一化的先验形式为：

$$
\tilde{p}(a^s | a^t, \beta) \propto \exp[-\beta \ell(a^s; a^t)], \quad \beta > 0
$$

其中 $a^s$ 和 $a^t$ 分别表示学生和教师的激活（可以是 logits 或概率），$\beta$ 是控制先验强度的精度参数（即不确定性的倒数）。归一化后的先验分布为：

$$
p(a^s | a^t, \beta) = \frac{1}{Z_{\beta}(a^t)} \exp[-\beta \ell(a^s; a^t)]
$$

其中配分函数 $Z_{\beta}(a^t) = \int \exp[-\beta \ell(a^s; a^t)] da^s$ 保证了概率分布的归一化。$\beta$ 越大，先验越集中，学生被强制更紧密地匹配教师；$\beta$ 越小，先验越平坦，学生更依赖数据自身的似然信号。

### 3.3 MAP 推断与 Laplace 近似

在给定真实标签 $y$ 和教师先验的条件下，学生激活的最优解可通过最大化后验概率获得：

$$
a^{s*} = \arg\max_{a^s} p(y|a^s) p(a^s|a^t, \beta)
$$

取负对数后，该 MAP 目标等价于：

$$
\operatorname*{min}_{a^s} -\log p(y | a^s) + \beta \ell(a^s; a^t) + \log Z_{\beta}(a^t)
$$

其中第一项对应交叉熵损失，第二项是自适应加权的蒸馏损失，第三项是配分函数的对数。直接计算配分函数 $Z_{\beta}(a^t)$ 通常是不可行的，Beta-KD 采用 Laplace 近似对其进行估计。假设能量函数在教师激活 $a^t$ 附近是局部二次的，配分函数可近似为：

$$
Z_{\beta}(a^t) \approx \exp[-\beta \ell(a^t; a^t)] \cdot (2\pi)^{d/2} |\beta \mathbf{H}|^{-1/2}
$$

其中 $d$ 是激活空间的维度，$\mathbf{H}$ 是能量函数在 $a^t$ 处的 Hessian 矩阵。由于 $\ell(a^t; a^t) = 0$（教师与自身无差异），代入后可得可计算的代理目标函数：

$$
\operatorname*{min}_{a^s} -\log p(y | a^s) + \beta \ell(a^s; a^t) - \frac{d}{2}\log \beta
$$

该目标函数的关键特征是引入了 $-\frac{d}{2}\log \beta$ 正则项：它防止 $\beta$ 发散到无穷大（即避免学生过度信任教师），为不确定性估计提供了理论保障。

### 3.4 摊销优化网络与自适应权重预测

为实现 $\beta$ 的自适应学习，Beta-KD 引入一个轻量级的不确定性预测网络 $g_{\phi}(h(x))$。该网络以学生模型的中间表示 $h(x)$ 为输入，通过 MLP 输出实例级（或任务级）的不确定性权重 $\beta$，并通过 softplus 激活函数保证 $\beta > 0$。最终的联合优化目标为：

$$
\operatorname*{min}_{\theta, \phi} \mathcal{L}_{\mathrm{CE}}(\theta) + g_{\phi}(h(x)) \ell(\theta) - \frac{d}{2}\log g_{\phi}(h(x))
$$

其中 $\theta$ 是学生模型参数，$\phi$ 是不确定性网络参数。该框架的模块构成如下：

- **教师模型** $f_t$（如 MobileVLM-7B）：提供固定的教师激活作为先验信息；
- **学生模型** $f_s$（如 MobileVLM-1.7B）：待训练的多模态语言模型；
- **不确定性网络** $g_{\phi}(h(x))$：轻量级 MLP，从学生中间表示预测 $\beta$，仅引入总参数量 0.03% 的开销；
- **Gibbs 先验**：将教师-学生差异建模为能量函数，形成概率先验；
- **MAP 目标函数**：结合交叉熵与自适应加权蒸馏损失的正则化目标。

该框架可在任务级（所有样本共享一个 $\beta$）或实例级（每个样本独立预测 $\beta(x)$）运行。实例级变体能够捕捉样本间的异质性与噪声，对高质量样本分配较大的 $\beta$（更信任教师），对低质量或噪声样本分配较小的 $\beta$（更依赖数据本身），从而实现无人工调参的自动损失平衡。

### 补充图表

![[assets/figures/papers/paper_list_l2707_https_arxiv_org_abs_2603_21426/figures/002_Figure_3.jpg]]
*Figure 3: Visualization of four representative knowledge distillation losses in the probability simplex*

![[assets/figures/papers/paper_list_l2707_https_arxiv_org_abs_2603_21426/figures/005_Figure_4.jpg]]
*Figure 4: Training trajectories and dynamic weight evolution for FKL+CE and RKL+CE objectives. The upper row shows the total training loss over steps, and the lower row illustrates the adaptive evolution of task and instance-level uncertainty weights β. The adaptive adjustment of the weighting parameter β during training ensure a faster overall loss convergence and enhances optimization stability*

## 实验与分析

### 核心瓶颈与实验动机

多模态大语言模型的知识蒸馏面临一个根本性挑战：来自真实标签的交叉熵监督与来自教师模型的多个蒸馏损失具有截然不同的尺度、梯度动态与优化方向。传统做法通过手动设定固定权重 $\lambda$ 来组合这些异构信号（$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{CE}} + \lambda \mathcal{L}_{\text{KD}}$），但这种方式无法适应不同样本或任务的不确定性分布，往往导致次优的迁移效果。Beta-KD 通过将蒸馏过程形式化为贝叶斯框架下的最大后验估计，推导出由数据驱动的自适应不确定性权重 $\beta$，从根本上消除了人工调参的需求。

### 能量函数选择：概率空间优于 Logit 空间

实验首先系统比较了不同能量函数 $\ell(a^s; a^t)$ 对知识迁移效果的影响（Table 1）。在 ScienceQA 数据集上，以 MobileVLM V2 7B 为教师、MobileVLM V2 1.7B 为学生，所有蒸馏方案均在交叉熵基线（VQA-Acc 48.4%）基础上进行对比。关键发现是：**在概率空间进行蒸馏显著优于在 logit 空间操作**。具体而言，Cosine-Probs 取得了 47.2% 的均值准确率，而 Cosine-Logits 和 MSE-Logits 分别为 46.2% 和 45.9%。这一结果表明，对于多模态生成任务，匹配教师与学生的输出概率分布比对齐内部特征表示更为有效。基于此，后续实验均以 Cosine-Probs 作为默认能量函数。

![[assets/figures/papers/paper_list_l2707_https_arxiv_org_abs_2603_21426/figures/004_Table_1.jpg]]
*Table 1: Comparison of different energy-based models for student–teacher knowledge transfer. All losses except CE are distillation losses. MSE-Logits and Cosine-Logits denote losses applied at the pre-softmax logit level, while MSE-Probs and Cosine-Probs are applied at the post-softmax probability level. Results on the ScienceQA dataset (averaged over three runs) show that Cosine-Probs achieves the best performance*

### 自适应不确定性加权的核心增益

Table 2 展示了在 ScienceQA 上两损失平衡（CE + 单一蒸馏损失）的消融结果，这是验证 Beta-KD 核心机制的关键实验。相较于手动固定权重（Manual），任务级 Beta-KD 在所有蒸馏损失类型（FKL、RKL、SFKL、Cosine-Probs）上均取得一致提升。以 Cosine-Probs 为例，任务级 Beta-KD 将 VQA-Acc 从手动加权的 53.1% 提升至 53.9%（+0.8%），IMG-Acc 从 66.0% 提升至 66.3%。

![[assets/figures/papers/paper_list_l2707_https_arxiv_org_abs_2603_21426/figures/006_Table_2.jpg]]
*Table 2: Experimental results of two-loss balancing on the ScienceQA dataset. Each baseline combines Cross-Entropy (CE) with a KL-based distillation loss. Manual uses fixed weights between CE and KL based on their initial scales. Beta-KD (Task) models task-level uncertainty shared across all samples, while Beta-KD (Instance) models instance-level uncertainty adaptive to each input. VQA-Acc denotes the overall question–answering accuracy across all questions, whereas IMG-Acc measures the accuracy on the subset of questions whose explicitly include image inputs. Both strategies consistently enhance knowledge distillation performance across different loss functions*

更关键的是**实例级 Beta-KD 的进一步增益**：在 Cosine-Probs 基础上，实例级权重将 VQA-Acc 推至 54.9%，相较纯 CE 基线提升 +6.5 个百分点，相较手动加权提升 +1.8 个百分点；IMG-Acc 达到 67.5%，提升幅度更为显著。这一趋势在 FKL 和 RKL 上也得到复现——实例级方案分别将 VQA-Acc 从手动加权的 51.4% 和 51.2% 提升至 52.6% 和 52.1%。这表明，样本级的不确定性建模能够有效捕捉数据中的异质性与噪声分布，为困难样本分配更合理的教师监督强度。

### 多损失扩展：三损失平衡验证

Table 3 将验证场景扩展到更复杂的三损失设置（CE + KL 蒸馏 + 特征蒸馏 FD）。在同时平衡三个异构监督信号时，手动调参的难度急剧增加，而 Beta-KD 的自动加权优势更加凸显。以 FKL+FD 组合为例，实例级 Beta-KD 的 VQA-Acc 达到 52.3%，超过手动方案（50.9%）和任务级方案（51.3%）。在 RKL+FD 和 Cosine-Probs+FD 配置下，实例级方案同样保持最优，验证了 Beta-KD 框架在多损失场景下的鲁棒扩展能力。

![[assets/figures/papers/paper_list_l2707_https_arxiv_org_abs_2603_21426/figures/007_Table_3.jpg]]
*Table 3: Experimental results of three-loss balancing on the ScienceQA dataset. Each baseline combines Cross-Entropy (CE), a KL-based distillation loss, and a feature-level distillation (FD) objective. Manual uses fixed weights among CE, KL, and FD based on their initial scales. Beta-KD (Task) models task-level uncertainty shared across all samples, while Beta-KD (Instance) models instance-level uncertainty adaptive to each input*

### 跨基准与跨架构泛化

Table 4 汇总了在六大多模态基准上的主实验结果，涵盖 MMBench_dev、MMEP、POPE、SEEDBench_IMG、MMMU_DEV_VAL 和 ScienceQA。以 Cosine KD 为基线，Beta-KD（实例级）在 MMBench_dev 上取得 60.2%（+3.1%），在 MMEP 上相较 Align-KD 提升 +54.1 分。值得注意的是，Beta-KD 的增益在不同评估维度上表现一致，未出现对特定数据集的偏倚。

![[assets/figures/papers/paper_list_l2707_https_arxiv_org_abs_2603_21426/figures/009_Table_4.jpg]]
*Table 4: Experimental results of the proposed uncertainty weighting framework on multiple benchmarks*

Table 5 进一步验证了框架的架构泛化能力。在 LLaVA-Qwen 0.5B 学生模型上，Beta-KD（实例级）在 TextVQA 上达到 54.9%（+2.9%），在 ScienceQA 上达到 66.3%（+2.1%），证明不确定性加权机制可跨模型架构有效迁移。

![[assets/figures/papers/paper_list_l2707_https_arxiv_org_abs_2603_21426/figures/011_Table_5.jpg]]
*Table 5: Performance comparison on LLAVA-Qwen Structure on TextVQA and ScienceQA. We report VQA accuracy (%)*

### 训练动态与权重演化

Figure 4 揭示了 Beta-KD 的训练轨迹与不确定性权重 $\beta$ 的动态演变。上排展示了 FKL+CE 和 RKL+CE 的总训练损失曲线，下排展示了任务级和实例级 $\beta$ 的自适应调整过程。相比固定权重方案，Beta-KD 的损失收敛更快且更稳定——$\beta$ 在训练初期自动探索合适的权重范围，随后趋于稳定，无需人工干预。

Figure 5 从师生 logit 分布匹配的角度提供了直观证据。在训练早期（Step10）和后期（Step190），Beta-KD（实例级）均实现了最紧密的师生分布对齐，而手动加权方案在分布尾部存在明显偏差。这从机制层面解释了实例级加权的性能优势：它使学生在整个训练过程中更精确地追踪教师的输出分布。

![[assets/figures/papers/paper_list_l2707_https_arxiv_org_abs_2603_21426/figures/003_Figure_5.jpg]]
*Figure 5: Visualization of teacher–student logit distributions at different training stages. Step10 and Step190 denote early and late training checkpoints. Compare with the training steps, both Beta-KD (Task) and Beta-KD (Instance) reduce the logit matching distance compared to the baseline, with the instance-level variant achieving the closest alignment*

### 效率分析：几乎零开销的自适应

Table 6 报告了训练效率统计。不确定性权重网络 $g_\phi(h(x))$ 仅引入总参数量 0.03% 的额外开销。以 Align-KD 为例，其训练速度为 1.82 it/s，而 Beta-KD（实例级）为 1.85 it/s——自适应加权不仅未降低训练速度，反而因更稳定的优化动态实现了略微加速。内存占用方面，各方案基本持平，证明 Beta-KD 的自适应机制在计算开销上几乎可以忽略。

![[assets/figures/papers/paper_list_l2707_https_arxiv_org_abs_2603_21426/figures/010_Table_6.jpg]]
*Table 6: Statistics of training efficiency*

### 实验公平性说明

所有实验均在 MobileVLM V2（教师 7B，学生 1.7B）和 LLaVA-Qwen 两种框架、六个多模态基准上进行了系统验证。消融实验覆盖了两损失与三损失设置、任务级与实例级粒度、以及多种蒸馏损失类型（FKL、RKL、SFKL、Cosine-Probs）。性能提升在所有配置下保持方向一致，未见对特定模型尺寸、数据集或损失函数的偏倚。

### 补充图表

![[assets/figures/papers/paper_list_l2707_https_arxiv_org_abs_2603_21426/figures/008_Figure_6.jpg]]
*Figure 6: Visualization of Student Entropy*

## 方法谱系与知识库定位

### 1. 问题定位：多模态蒸馏中的损失平衡困境

多模态大语言模型（MLLM）的知识蒸馏面临一个核心瓶颈：来自数据（交叉熵）和教师（多个蒸馏损失）的异构监督信号具有不同的尺度、梯度与优化动态，手动平衡它们极其困难，且固定权重无法适应样本或任务的不确定性。传统的蒸馏总目标形式为：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{CE}} + \lambda \mathcal{L}_{\mathrm{KD}}$$

其中 $\lambda$ 为手动选择的固定超参数。这一范式在单损失场景下已需大量调参，在多损失场景（如同时使用 KL 散度蒸馏和特征蒸馏）下更是组合爆炸。

### 2. 方法谱系：从固定加权到不确定性自适应

**Beta-KD** 将知识蒸馏重新解释为贝叶斯框架下的最大后验（MAP）估计问题——教师的输出作为学生激活上的 Gibbs 先验，交叉熵为似然，联合优化等价于最小化带有自适应精度的蒸馏目标。其核心创新在于通过 Laplace 近似推导出封闭形式的不确定性权重 $\beta$，并由轻量网络预测，从而消除人工调参。

下表将 Beta-KD 置于相关工作的谱系中：

| 方法 | 核心机制 | 损失权重策略 | 与 Beta-KD 的关系 |
|------|----------|-------------|-------------------|
| **Forward KL (FKL)** (Hinton et al., NIPS 2015) | 最小化学生与教师概率分布的正向 KL 散度 | 手动固定 $\lambda$ | Beta-KD 的蒸馏损失可选用 FKL，但权重由 $\beta$ 自适应调节 |
| **Reverse KL (RKL)** (Gu et al., ICLR 2024) | 逆向 KL 散度，缓解分布不匹配 | 手动固定 $\lambda$ | 同 FKL，Beta-KD 提供统一的权重学习框架 |
| **Align-KD** (Feng et al., CVPR 2025) | 跨模态对齐知识蒸馏 | 手动固定权重 | Beta-KD 在 Align-KD 基础上引入实例级不确定性权重，在 MMEP 上提升 +54.1 |
| **Cosine-Probs KD** | 基于余弦相似度的概率空间蒸馏 | 无加权或手动加权 | Beta-KD 在 Cosine-Probs 基础上加入自适应 $\beta$，在 MMBench_dev 上提升 +3.1 |
| **Beta-KD (Task-level)** | 任务级 Gibbs 先验 + MAP 估计 | 任务级标量 $\beta$（共享于所有样本） | 本方法的粗粒度版本 |
| **Beta-KD (Instance-level)** | 实例级 Gibbs 先验 + 摊销优化网络 | 实例级 $\beta(x)$（由 $g_\phi(h(x))$ 预测） | 本方法的完整版本，捕捉样本异质性 |

### 3. 关键改进槽位

Beta-KD 对传统蒸馏框架的核心改动集中在 **蒸馏损失权重** 这一槽位：

- **基线值**：手动选择的固定超参数 $\lambda$（如 $\lambda=1$）或基于初始尺度的手动设定。
- **提出值**：由摊销优化网络从数据中学习的不确定性权重 $\beta$（任务级标量或实例级 $\beta(x)$），通过 softplus 保证正值。联合优化目标为：

$$\min_{\theta, \phi} \mathcal{L}_{\mathrm{CE}}(\theta) + g_{\phi}(h(x)) \ell(\theta) - \frac{d}{2}\log g_{\phi}(h(x))$$

其中 $g_\phi$ 为轻量 MLP，仅引入总参数量 0.03% 的开销。

### 4. 适用边界与局限

**已验证的适用场景**：
- 两损失平衡（CE + 单一蒸馏损失）：在 ScienceQA 上，实例级 Beta-KD (Cosine-Probs) 将 VQA 准确率从纯 CE 基线的 48.4% 提升至 54.9%（+6.5 个百分点）。
- 三损失平衡（CE + KL + 特征蒸馏）：任务级和实例级 Beta-KD 均一致优于手动加权。
- 跨模型架构泛化：在 MobileVLM（1.7B 学生，7B 教师）和 LLaVA-Qwen（0.5B 学生）上均有效。
- 跨数据集泛化：在 ScienceQA、MMEP、MMBench_dev、TextVQA 等六个基准上验证。

**已知局限与待验证边界**：
- 分析中未报告明确的失败案例或局限性声明，需人工核实论文原文是否讨论了以下潜在问题：
  - 在极端大教师-小学生差距（如 70B→0.5B）下的 $\beta$ 稳定性。
  - 摊销优化网络 $g_\phi$ 对分布外输入的泛化能力。
  - 在超过三个损失函数的多目标场景下的扩展性。

### 5. 开放问题

论文分析揭示了以下待探索方向：

1. **最优能量表示**：哪种能量函数 $\ell(a^s; a^t)$ 对跨模态知识传递最为有效？Table 1 的初步结论是概率空间（Cosine-Probs）优于 logit 空间（MSE-Logits, Cosine-Logits），但更广泛的能量形式（如基于注意力图或中间特征）尚未探索。

2. **不确定性权重的动态机制**：$\beta$ 的学习动态（Figure 4）显示其在训练过程中自适应演变，但其与样本难度、噪声水平、教师置信度等因素的定量关系尚未被深入分析。

3. **多任务扩展性**：不确定性加权在两损失或多损失设置中的有效性如何随任务数量变化？三损失实验（Table 3）已初步验证，但更多损失组合下的表现仍需探索。

4. **更广泛的学生架构**：该方法在 MobileVLM 和 LLaVA-Qwen 上已验证，但对其他 MLLM 架构（如 BLIP-2、InstructBLIP、LLaVA-1.5 系列）的泛化性尚待确认。

## 原文 PDF

![[paperPDFs/CVPR_2026/Uncertainty_Aware_Knowledge_Distillation_for_Multimodal_Large_Language_Models.pdf]]
