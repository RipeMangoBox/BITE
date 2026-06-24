---
title: "Exploratory Causal Inference in SAEnce"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Exploratory_Causal_Inference_in_SAEnce.pdf
openreview_forum_id: Ml8t8kQMUP
aliases:
- NESN
- ECIS
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "提出 Neural Effect Search (NES)，一种递归分层（recursive stratification）策略：每次迭代选出当前最显著的神经元作为主效应方向，随后通过分层（stratification）或臂内残差化（arm‑wise residualization）消除该方向对其他神经元的泄漏影响，使后续检验聚焦于残余因果信号。这从根本上..."
primary_logic: "NES 将因果效应发现转化为逐步解缠过程。每轮只确认一个主方向，并利用已确认的神经元作为代理变量，阻断其诱导的虚假关联，从而使后续检验仅对尚未发现的效应敏感。这既是多重检验的纠偏方法，也是有原则的效应解缠算法。"
claims:
- "标准多重检验随着样本量 n 或效应量 τ 增大，会将所有与真实效应纠缠的神经元错误标记为显著，即使使用 Bonferroni 校正也无法避免。"
- "在半合成基准上，当实验功效足够高时，Baseline（Bonferroni, FDR, t‑test）的精确率急剧下降，IoU 趋近于 0，而 NES 始终保持高精确率和高 IoU。"
- "在零效应消融中，NES 返回空集，而 t‑test 和 top‑k 产生大量假阳性。"
- "Theorem 4.1 证明，在适当假设（主对齐、效应解缠等）下，NES 以概率 1 恢复 r 个不同的受处理影响的神经元。"
---

# Exploratory Causal Inference in SAEnce

> [!tip] 核心洞察
> NES 将因果效应发现转化为逐步解缠过程。每轮只确认一个主方向，并利用已确认的神经元作为代理变量，阻断其诱导的虚假关联，从而使后续检验仅对尚未发现的效应敏感。这既是多重检验的纠偏方法，也是有原则的效应解缠算法。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SAEnce 中的探索性因果推断 |
| 英文题名 | Exploratory Causal Inference in SAEnce |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=Ml8t8kQMUP) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Neural Effect Search (NES) |
| Dataset | CelebA semi‑synthetic RCT (Wearing Hat, Eyeglasses), ISTAnt real‑world RCT (ants under social‑immunity treatment) |

> [!tip] 效果简介
> - CelebA semi‑synthetic RCT (Wearing Hat, Eyeglasses) 上，Precision, Recall, Intersection over Union (IoU) 为 在所有样本量 N ∈ {30, …, 1000} 和效应量 τ ∈ {0.1, …, 0.8} 下，NES 保持高 Precision 和高 IoU，Recall 与其他方法相当或更优。，对比 Bonferroni, FDR, t‑test, top‑k：随 N 或 τ 增加，Precision 急剧下降，IoU 趋于 0（显著性崩塌）。，变化 NES 避免了显著性崩塌，IoU 在高功效时远优于所有基线。。
> - ISTAnt real‑world RCT (ants under social‑immunity treatment) 上，F1‑score of discovered concepts (ground‑truth annotation) 为 发现两个显著效应：Neuron 394 (grooming 行为, F1=0.398)；Neuron 550 (背景位置标记, 实验设计偏差, F1=0.568)。，对比 无直接对比（纯探索性实验），但发现与先前文献完全一致。，变化 N/A。

## 概述

**核心问题**：在随机对照实验中，当科学家对“处理究竟影响了什么”缺乏先验知识时，如何直接从高维观测数据中发现未知的因果效应？传统因果推断要求预先定义结果变量 $Y$，而探索性实验中的 $Y$ 往往是隐变量，仅通过复杂测量 $X$（如图像、视频）间接体现。

**探索性因果推断悖论**：本文揭示了一个根本性困境——当利用稀疏自编码器（SAE）将基础模型表示转化为可解释的测量字典后，由于神经元之间的纠缠（一个神经元对多个潜在因子有微弱响应），标准多重检验（无论是否使用 Bonferroni 校正）会随着实验功效增强（样本量 $n$ 或效应量 $\tau$ 增大）而将几乎所有与真实效应有轻微关联的纠缠神经元标记为显著，导致识别结果丧失可解释性（Theorem 3.1, 3.2; Figure 3）。

**方法定位**：本文提出 Neural Effect Search（NES），一种递归分层检验策略。其核心洞察是将因果效应发现转化为逐步解缠过程：每轮只确认一个主效应方向，随后通过分层或臂内残差化消除该方向对其他神经元的泄漏影响，使后续检验聚焦于残余因果信号。这既是多重检验的纠偏方法，也是有原则的效应解缠算法。在适当假设下，NES 以概率 1 恢复所有受处理影响的神经元（Theorem 4.1）。

**方法谱系与知识库定位**：NES 处于预测驱动因果推断与机制可解释性的交叉地带。与经典因果推断（预先指定 $Y$）和预测驱动因果推断（用标注数据训练代理结果模型）不同，NES 面向完全探索性场景，无需任何结果标注。在多重检验维度上，基线方法包括 **Bonferroni 校正**（Bonferroni, 1936）、**FDR**（Benjamini‑Hochberg）以及未校正的 $t$ 检验和 top‑$k$ 选择，这些方法均因忽略神经元纠缠而遭遇显著性崩塌。在因果特征选择维度上，**LASSO**（$\ell_1$ 惩罚逻辑回归）和 **Stability‑selected LASSO** 通过反因果方向（用处理变量回归 SAE 编码）选择相关神经元，但性能与标准多重检验相当，仍无法克服悖论（Figure 37）。

**主要结果**：
- 在半合成基准（CelebA, Wearing Hat / Eyeglasses）上，当实验功效足够高时，Bonferroni、FDR、$t$ 检验和 top‑$k$ 的精确率急剧下降，IoU 趋近于 0，而 NES 始终保持高精确率和高 IoU（Figure 5）。
- 在零效应消融中，NES 返回空集，而 $t$ 检验和 top‑$k$ 产生大量假阳性（Figure 32）。
- 在真实生态学实验（ISTAnt 蚂蚁社会免疫处理）中，NES 发现了两个显著效应：梳理行为（grooming, F1=0.398）和有限样本实验设计偏差（F1=0.568），与先前文献完全一致（Figure 6）。
- 消融实验表明，NES 对基础模型选择（SigLIP / DINOv2）、SAE 维度、非线性和随机种子均稳健；仅当主对齐假设被破坏（如 jump‑ReLU）时方法失效。

**局限性**：NES 依赖 SAE 编码满足主对齐假设；当前仅适用于二值处理和离散概念，扩展至连续效应和多值处理仍有理论缺口；基础模型的信息充分性在实际中难以验证。

## 背景与动机

### 从经典因果推断到探索性因果推断

随机对照试验（RCT）是因果推断的黄金标准。在经典范式中，研究者预先指定一个已知的结果变量 $Y$，在随机化保证无混淆的条件下，通过比较处理组与对照组的平均结果差异来估计平均处理效应（ATE）：

$$\tau = \mathbb{E}[Y \mid T=1] - \mathbb{E}[Y \mid T=0]$$

然而，这一范式隐含了一个关键前提：研究者必须事先知道“应该测量什么”。在许多现代科学实验中——例如生态行为学中观察动物对免疫处理的反应，或神经科学中探测特定刺激的神经关联——真正受处理影响的结果变量往往是未知的。研究者拥有的是高维、复杂的原始观测 $X$（如视频、图像），其中潜藏着多个可能的效应维度，但缺乏先验知识来指定哪一个才是真正的因果结果。

本文正是针对这一“探索性实验”场景，提出了**探索性因果推断**这一新范式。其核心问题可表述为：在仅观测到处理分配 $T$ 和高维原始数据 $X$、而对潜在受影响结果 $Y$ 毫无先验知识的情况下，能否直接从数据中发现处理效应是什么？

### 现有方法的两个关键缺口

实现探索性因果推断面临两个根本性挑战。

**第一个缺口：缺乏可解释的测量通道。** 原始观测 $X$ 是高维且语义密集的，无法直接作为“结果变量”进行统计检验。即使能够检验，显著的像素或波形变化也难以转化为人类可理解的科学发现。因此，需要一种能将高维数据转化为可解释测量字典的表示学习机制。

**第二个缺口：标准多重检验在纠缠表示下的崩溃——“探索性因果推断悖论”。** 即便获得了可解释的表示，直接套用经典的多重假设检验框架（如对所有神经元执行 $t$ 检验并用 Bonferroni 或 FDR 校正）也会系统性地失败。其根本原因在于**神经元纠缠**：在稀疏自编码器等表示学习中，单个潜在因果因子往往不仅激活其“主导”神经元，还会在大量其他神经元上产生微弱但非零的响应（即信息泄漏）。当实验功效随样本量 $n$ 或效应量 $\tau$ 增大而提升时，这些微弱的纠缠信号也会逐一越过显著性阈值，导致几乎所有与真实效应有牵连的神经元都被标记为“显著”。Theorem 3.1 和 Theorem 3.2 从理论上证明了这一现象：标准多重检验会将整个泄漏集合中的神经元错误识别为效应，使识别结果丧失可解释性。Figure 3 通过数值实验直观展示了这一“显著性崩塌”过程——随着功效增强，假阳性爆炸式增长，而真正的效应信号淹没在噪声之中。

### 本文的动机与核心思路

上述两个缺口共同指向一个需求：需要一种既能将高维观测转化为可解释测量，又能在纠缠表示中稳健地分离出真实因果效应的方法。

本文的解决方案由两部分构成。在表示层面，利用预训练基础模型将原始数据映射为语义表示，再通过稀疏自编码器将该表示重构为高维稀疏编码，使每个坐标近似对应单一可解释概念。在推断层面，提出 **Neural Effect Search**——一种递归分层检验策略：每轮选出当前最显著的神经元作为主效应方向，随后通过分层或臂内残差化消除该方向对其他神经元的泄漏影响，使后续检验聚焦于残余因果信号。这一设计将因果效应发现转化为逐步解缠过程，从根本上控制了纠缠导致的效应扩散，从而在理论上（Theorem 4.1）和实验上（Figure 5）均克服了探索性因果推断悖论。

## 核心创新

### 问题重定义：探索性因果推断悖论

传统因果推断假设科学家已知受处理影响的潜在结果变量 $Y$，只需估计 $T$ 对 $Y$ 的平均处理效应。本文将该范式扩展为**探索性因果推断（Exploratory Causal Inference）**：$Y$ 本身是未知的，科学家仅拥有高维观测 $X$（如视频、图像），目标是直接从数据中发现哪些潜在因子受到了处理的影响。

这一设定面临一个根本性瓶颈。当利用稀疏自编码器（SAE）将基础模型表示转化为可解释的测量字典时，由于**神经元纠缠**——一个神经元可能对多个潜在因子产生微弱响应——标准多重检验（无论是否使用 Bonferroni 校正）会随着实验功效增强（样本量 $n$ 或效应量 $\tau$ 增大）而将几乎所有与真实效应有轻微关联的纠缠神经元标记为显著，导致识别结果丧失可解释性。这就是**探索性因果推断悖论**，由 Theorem 3.1 和 Theorem 3.2 严格刻画，并在 Figure 3 中得到数值验证。

### 核心机制：从一次性检验到递归分层解缠

NES 的核心创新在于将因果效应发现转化为**逐步解缠过程**，其关键操作点体现在三个 changed slots 上：

**1. 效应发现与检验策略：从全量独立检验到递归分层检验**

基线方法（Bonferroni、FDR、t-test、top-k）对所有 $m$ 个神经元执行一次性独立假设检验，完全不考虑神经元间的纠缠结构。NES 采用递归策略（Algorithm 1）：每轮在所有未选神经元上执行假设检验，选出满足 Bonferroni 显著性的最强神经元，将其加入已选集合 $S$；随后通过分层（按已选神经元的激活值 $Z_S$ 将样本分组）或臂内残差化消除已选神经元对其他神经元的泄漏影响，对残余信号再次检验，直至无神经元通过显著性。

这一设计的因果直觉在于：每轮只确认一个主效应方向，并利用已确认的神经元作为代理变量，阻断其诱导的虚假关联，使后续检验仅对尚未发现的效应敏感。Figure 4 以两个潜在因子 $Y_1, Y_2$ 和三个测量通道 $Z_1, Z_2, Z_3$ 为例展示了该递归过程：第一轮选出与 $Y_1$ 主对齐的 $Z_1$，第二轮在控制 $Z_1$ 后识别出与 $Y_2$ 对齐的 $Z_3$，而纠缠神经元 $Z_2$ 的虚假效应被成功消除。

**2. 多重检验校正方式：从全局一次性校正到递归局部校正**

基线方法对全量 $m$ 个神经元一次性计算 p 值后用 Bonferroni（$\alpha/m$）或 FDR 校正。NES 每次递归仅对当前未选神经元（数量为 $m - |S|$）应用 Bonferroni 校正（$\alpha/m$），严格控制族系误差。由于每轮筛选后有效检验空间缩小，且已选神经元的影响已被消除，该策略在控制 I 型错误的同时避免了功效过度分散。

**3. 效应估计中的解缠机制：从关联差异到调整因果效应**

基线方法直接利用神经元的未调整均值对比（关联差异 $\mathbb{E}[Z_j|T=1] - \mathbb{E}[Z_j|T=0]$）进行推断，不做任何解缠处理，导致信息泄漏放大假阳性。NES 在每次递归中通过两种可选机制消除已发现方向 $v_k$ 的泄漏信号：

- **Pooled stratification**：按已选神经元集合 $Z_S$ 的取值将样本分层，在层内估计 $Z_j$ 的处理效应后跨层聚合。
- **Arm-wise residualization**：在处理组和对照组内分别将 $Z_j$ 对 $Z_S$ 回归，取残差作为调整后的信号。

Lemma A.1 证明，调整后的效应估计仅反映尚未识别的因果影响，误差控制在 $\pm\varepsilon$ 以内。这使 NES 既是一种多重检验的纠偏方法，也是一种有原则的效应解缠算法。

### 理论保证：一致性定理

Theorem 4.1 在三个核心假设下证明了 NES 的一致性：
- **信息充分性**：基础模型表示 $h$ 保留了 $X$ 中关于 $Y$ 的全部信息。
- **主对齐**：每个受处理影响的潜在因子存在一个主导神经元，其效应幅值显著大于其他纠缠神经元（Assumption A.2）。
- **效应解缠**：不同潜在因子的效应方向近似正交。

在此条件下，当样本量 $n \to \infty$ 时，NES 输出的神经元集合以概率 1 收敛到 $r$ 个不同受处理影响的神经元：$\Pr(S_{\text{final}} = \{j_1,\dots,j_r\}) \to 1$。这一结果与探索性因果推断悖论形成鲜明对比——后者在样本量增大时会导致所有纠缠神经元被错误标记为显著。

### 与基线方法的本质差异

| 维度 | 基线方法 | NES |
|------|----------|-----|
| 检验结构 | 一次性全量独立检验 | 递归分层检验，逐步解缠 |
| 纠缠处理 | 无，效应泄漏未被控制 | 通过分层/残差化阻断泄漏 |
| 校正策略 | 全局 Bonferroni 或 FDR | 递归局部 Bonferroni |
| 高功效行为 | 精确率崩塌，IoU → 0 | 保持高精确率和高 IoU |
| 零效应场景 | 产生大量假阳性 | 返回空集 |

消融实验进一步证实，NES 的优势源于递归分层策略本身，而非特定估计量选择：AIPW 估计量仅提供边际效率增益，不改变显著性崩塌现象；臂内残差化在低功效实验中显著提升精度，高功效时增益边际化；替换基础模型或改变 SAE 维度后 NES 仍稳定克服悖论。

## 整体框架

本文提出了一套完整的**探索性因果推断（Exploratory Causal Inference, ECI）**流水线，其核心目标是在科学家对处理效应缺乏先验知识的情况下，直接从高维观测数据中自动发现受处理影响的潜在结果概念。整体框架由四个顺序衔接的模块构成，如图 1 所示。

### 流水线总览

**第一步：实验数据采集。** 在随机化对照试验（RCT）框架下收集样本，每条样本包含高维原始观测 $X$（如图像、视频帧）、二值处理分配 $T \in \{0, 1\}$，以及可能的协变量 $W$。与传统因果推断不同，ECI 设定中科学家**不知道**受处理影响的具体结果变量 $Y$ 是什么——这正是需要从数据中探索发现的目标。

**第二步：可解释表示提取。** 原始观测 $X$ 首先通过一个预训练的基础模型（Foundation Model, FM）$\phi(\cdot)$ 映射到稠密语义表示空间 $h = \phi(X) \in \mathbb{R}^d$。该基础模型需满足**信息充分性假设**：$\mathcal{I}(X, Y) = \mathcal{I}(\phi(X), Y)$，即 FM 表示不丢失关于潜在结果的信息。随后，一个稀疏自编码器（Sparse Autoencoder, SAE）将稠密的 $h$ 重新参数化为高维稀疏编码 $z = f(h) \in \mathbb{R}^m$（$m \gg d$），并通过线性解码器 $\hat{h} = \mathbf{D}z + b_d$ 重建。SAE 的训练目标为：

$$\min_{\mathbf{D}, z \ge 0} \mathbb{E}\big[\|h - \mathbf{D}z - b_d\|_2^2\big] + \lambda \mathcal{S}(z)$$

其中 $\mathcal{S}(z)$ 为稀疏惩罚项。SAE 的作用是将 FM 特征转化为一个**可解释的测量字典**，使每个编码坐标 $Z_j$ 近似对应于单一语义概念，为后续统计检验提供可操作的测量通道。

**第三步：处理效应识别。** 在 SAE 编码空间 $\mathbb{R}^m$ 上，通过本文提出的 **Neural Effect Search（NES）** 算法自动发现受处理影响的神经元集合。NES 是一种递归分层假设检验过程，每轮选出当前最显著的神经元作为主效应方向，随后通过分层或臂内残差化消除该方向对其他神经元的泄漏影响，使后续检验聚焦于残余因果信号。该模块是整个流水线的核心创新，直接回应了**探索性因果推断悖论**——当实验功效增强时，标准多重检验会将所有与真实效应纠缠的神经元错误标记为显著，导致识别结果丧失可解释性。

**第四步：因果发现解释。** 科学家检视 NES 所选神经元对应的 SAE 字典原子 $\mathbf{d}_j$，或通过可视化极值激活样本，将神经网络的发现映射回人类可理解的因果效应。例如，在真实生态学实验中，被选中的神经元可被解释为特定的蚂蚁行为（如梳理行为）或实验设计偏差（如背景位置标记）。

### 模块间的输入输出关系

流水线的数据流是严格单向的：原始观测 $X$ → FM 表示 $h$ → SAE 编码 $Z$ → NES 所选神经元集合 $S_{\text{final}}$ → 人类可读的因果解释。各模块的依赖关系如下：

- **FM 编码器**是 SAE 的上游前提：SAE 的输入完全依赖于 FM 表示的质量和信息充分性。若 FM 丢失了潜在效应的关键信息，则下游所有分析将无法恢复该效应。
- **SAE 编码**是 NES 的统计检验对象：NES 直接对 SAE 编码 $Z$ 的每个坐标执行假设检验。SAE 的**单语义性**（即每个神经元主要对应一个概念）是 NES 主对齐假设（Assumption A.2）成立的基础——若 SAE 高度多语义且无清晰主导神经元，NES 的效应识别精度将受限。
- **NES 输出**是解释模块的输入：NES 返回的神经元索引集合直接映射到 SAE 字典的对应原子，科学家无需接触原始高维数据即可完成解释闭环。

### 框架的因果推断范式定位

如图 2 所示，本文提出的 ECI 范式与经典因果推断和预测驱动因果推断形成对比：在经典范式中，结果 $Y$ 被直接观测；在预测驱动范式中，$Y$ 仅部分标注，需通过预测模型补全；而在 ECI 范式中，**受影响的 $Y$ 本身是未知的**，它隐含在高维测量 $X$ 中，需要模型从数据中自动发现。这一范式转换使得本文方法适用于科学家对潜在效应完全无先验知识的探索性实验场景。

## 核心模块与公式推导

### 探索性因果推断的整体流水线

NES 方法建立在四个顺序模块之上，如 Figure 1 所示：

1. **Foundation Model Encoder**：将高维原始观测 $X$（如图像、视频帧）映射到语义表示空间 $h \in \mathbb{R}^d$。该模块需满足**信息充分性假设**：$\mathcal{I}(X, Y) = \mathcal{I}(\phi(X), Y)$，即基础模型的表示不丢失关于潜在结果 $Y$ 的信息。
2. **Sparse Autoencoder (SAE)**：将稠密的 FM 特征 $h$ 编码为高维稀疏码 $z \in \mathbb{R}^m$ 并线性重建，使每个坐标近似对应单一可解释概念（测量通道）。SAE 的编码-解码形式为：

$$z = f(h) = g(\mathbf{E}^{\top} h + b_e), \quad \hat{h} = \mathbf{D} z + b_d$$

其训练目标为最小化重建损失加稀疏惩罚：

$$\min_{\mathbf{D}, z \ge 0} \mathbb{E}\big[\|h - \mathbf{D} z - b_d\|_2^2\big] + \lambda \mathcal{S}(z)$$

3. **Neural Effect Search (NES)**：递归分层检验，每轮估计每个神经元的调整因果效应，对未选神经元执行假设检验并筛选最显著者，迭代至无显著神经元。
4. **Interpretation**：科学家检视被 NES 选出的神经元所对应的 SAE 字典原子 $d_j$ 或可视化极值激活样本，将神经网络发现映射回人类可理解的因果效应。

### 探索性因果推断悖论的形式化

设潜在结果 $Y_k$ 在 SAE 码空间中的效应方向向量为：

$$v_k := \mathbb{E}[Z \mid do(Y_k=1)] - \mathbb{E}[Z \mid do(Y_k=0)] \in \mathbb{R}^m$$

定义**泄漏集合**为所有被任一因果因子激活的神经元索引：

$$\mathcal{A}_\varepsilon = \bigcup_{k=1}^r \{j : |(v_k)_j| \ge \varepsilon\}, \quad \rho_\varepsilon = \frac{|\mathcal{A}_\varepsilon|}{m}$$

其中 $\rho_\varepsilon$ 为**泄漏指数**，衡量多语义程度。当 $\rho_\varepsilon > r/m$ 时，存在纠缠：一个神经元对多个潜在因子有微弱响应。

**定理 3.1 与 3.2** 揭示了核心悖论：在标准多重检验下（无论是否使用 Bonferroni 校正），随着样本量 $n \to \infty$ 或效应量 $\tau \to \infty$，所有泄漏集合中的神经元都将被错误标记为显著：

$$\Pr\big[\{\text{all } j \in \mathcal{A}_\varepsilon \text{ are rejected}\}\big] \to 1$$

这意味着实验功效越强，假阳性反而越多，识别结果完全丧失可解释性。

### NES 的递归分层机制

NES 的核心思想是将因果效应发现转化为逐步解缠过程（Algorithm 1）。每轮迭代执行以下步骤：

1. **效应估计与解缠**：对于每个未选神经元 $j \notin S$，通过 **pooled stratification**（按已选神经元 $Z_S$ 分层）或 **arm‑wise residualization**（在每臂内回归 $Z_j \sim Z_S$ 取残差）消除已发现方向的泄漏信号，得到调整后的效应估计。这使得调整后的均值仅反映尚未识别的因果影响（Lemma A.1）。
2. **假设检验**：对调整后的效应执行两样本 $t$ 检验，获得 $p$ 值。
3. **Bonferroni 筛选**：以 $\alpha/m$ 为阈值筛选显著神经元（$m$ 为总神经元数，保持族系误差控制）。
4. **主方向确认**：将最显著的神经元加入已选集合 $S$，并在后续测试中以其作为代理变量阻断诱导的虚假关联。
5. **终止条件**：无神经元通过显著性检验时停止。

### 一致性保证

**定理 4.1** 给出了 NES 的理论保证：在适当假设（主对齐、效应解缠等）下，当样本量趋于无穷时，NES 输出的神经元集合以概率 1 收敛到真实的 $r$ 个受不同处理影响的主方向：

$$\Pr(S_{\text{final}} = \{j_1, \dots, j_r\}) \to 1$$

这从理论上证明了递归分层策略能够从根本上控制纠缠导致的效应扩散，避免了标准多重检验的显著性崩塌。

## 实验与分析

### 半合成基准：NES 克服显著性崩塌

实验在 CelebA 数据集上构建半合成 RCT，以“戴帽子”（Wearing Hat）和“戴眼镜”（Eyeglasses）两类属性作为受处理影响的潜在因果因子，通过 SigLIP 基础模型提取特征，再经稀疏自编码器（SAE，维度 m=3072）编码为可解释的测量字典。处理变量 T 为随机分配的二值标签，效应量 τ 控制因果信号的强度，样本量 N 在 30 至 1000 之间变化。评价指标包括精确率（Precision）、召回率（Recall）和交并比（IoU），以衡量方法识别真实效应神经元的准确性。

**核心结果**（Figure 5）：当样本量 N 或效应量 τ 增大，即实验功效提升时，所有基线方法——Bonferroni 校正、FDR（Benjamini‑Hochberg）、未校正 t 检验和 top‑k 选择——的精确率急剧下降，IoU 趋近于零，验证了“探索性因果推断悖论”：功效越强，与真实效应仅有微弱纠缠的神经元越容易被错误标记为显著。相比之下，NES 在所有 N 和 τ 条件下始终保持高精确率和高 IoU，召回率与其他方法相当或更优，是唯一避免显著性崩塌的方法。

这一优势的根源在于 NES 的递归分层机制：第一轮选出最显著的主效应神经元后，后续检验通过分层或臂内残差化消除该方向对其他神经元的泄漏影响，使残余检验仅对尚未发现的因果效应敏感。基线方法一次性对所有神经元做独立检验，无法阻断纠缠导致的效应扩散。

### 真实世界 RCT：ISTAnt 实验生态学

在 ISTAnt 蚂蚁社会免疫实验中（n=44 段视频，处理组接受免疫刺激），NES 在无任何先验行为知识的情况下，发现了两个显著效应。第一个被选出的神经元（code 394）对应 grooming（梳理）行为，F1=0.398，与先前文献对免疫处理后梳理行为增加的报道完全一致。第二个神经元（code 550）被解释为背景位置标记，F1=0.568，反映了有限样本下的实验设计偏差（处理组与对照组拍摄位置不完全对称）。该实验因样本量较小，NES 内部未使用 Bonferroni 校正，但方法仍成功分离了科学效应与实验偏差。

### 消融实验：方法鲁棒性与组件贡献

**基础模型替换**：将 SigLIP 替换为 DINOv2 后，NES 仍能克服悖论，结果与主实验一致，表明方法对基础模型选择不敏感（Figure 13）。

**SAE 维度与非线性**：将 SAE 维度从 3072 扩展至 12288，NES 性能保持稳定（Figures 14–19）。在不同 SAE 非线性（ReLU、TopK）和随机种子下，方法均有效；仅当使用 jump‑ReLU 破坏主对齐假设时，NES 失效，说明方法依赖 SAE 编码满足每个因果效应存在主导神经元的条件（Figures 20–26）。


![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ml8t8kQMUP/figures/024_Figure_16.jpg]]
*Figure 16: Ablation SAE dimension ( m = 6 1 4 4 ) . Precision, Recall, and IoU in effect identification varying sample size N (top) and effect size τ (bottom), with SAE dimension m = 6 ~ 1 4 4 , 8x DINOv2 dimension n = 7 6 8 . NES consistently replicates the main results, varying the representation dimension m, still overcoming the paradox of Exploratory Causal Inference*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ml8t8kQMUP/figures/029_Figure_20.jpg]]
*Figure 20: Ablation SAE non-linearity (top-5). Precision, Recall, and IoU in effect identification varying sample size N (top) and effect size τ (bottom), with SAE non-linearity by top-k with k = 5. NES consistently replicates the main results using top-k with k = 20, still overcoming the paradox of Exploratory Causal Inference*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ml8t8kQMUP/figures/031_Figure_21.jpg]]
*Figure 21: Ablation SAE non-linearity (top-10). Precision, Recall, and IoU in effect identification varying sample size N (top) and effect size τ (bottom), with SAE non-linearity by top-k with k = 10. NES consistently replicates the main results using top-k with k = 20, still overcoming the paradox of Exploratory Causal Inference*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ml8t8kQMUP/figures/032_Figure_22.jpg]]
*Figure 22: Ablation SAE non-linearity (top-50). Precision, Recall, and IoU in effect identification varying sample size N (top) and effect size τ (bottom), with SAE non-linearity by top-k with k = 50. NES consistently replicates the main results using top-k with k = 20, still overcoming the paradox of Exploratory Causal Inference*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ml8t8kQMUP/figures/034_Figure_23.jpg]]
*Figure 23: Ablation SAE non-linearity (top-100). Precision, Recall, and IoU in effect identification varying sample size N (top) and effect size τ (bottom), with SAE non-linearity by top-k with k = 100. NES consistently replicates the main results using top-k with k = 20, still overcoming the paradox of Exploratory Causal Inference*

**NES 内部门控策略**：在 NES 递归内部使用 Bonferroni、FDR 或未校正 t 检验进行神经元筛选，Bonferroni 和 FDR 在足够功效下表现最优；t 检验在中功效区精度较低，但在高功效时性能接近（Figure 27）。

**臂内残差化**：在低功效实验中，臂内残差化（arm‑wise residualization）显著提升 NES 精确率；高功效时增益边际化，表明解缠机制在信号较弱时尤为关键（Figure 28）。

**效应估计量选择**：将 ATE 估计量替换为 AIPW（增强逆倾向加权）仅带来边际效率增益，不改变显著性崩塌现象，说明 NES 的优势源于递归分层策略而非特定估计量（Figure 29）。

**零效应消融**：在无任何因果效应的零假设场景下，NES 返回空集，而 t 检验和 top‑k 产生大量假阳性，验证了 NES 对 I 型错误的严格控制（Figure 32）。

**额外基线**：LASSO（ℓ1 惩罚逻辑回归）和稳定性选择 LASSO 的性能与标准多重检验相当，同样无法克服悖论，NES 显著优于二者（Figure 37）。这进一步说明，仅靠稀疏正则化不足以解决纠缠导致的效应扩散问题。

**相反效应与不同倾向得分**：在处理产生相反方向效应或倾向得分变化时，NES 均一致克服悖论（Figures 33–36），表明方法对效应异质性和实验设计参数具有鲁棒性。

### 失败模式与局限

NES 的有效性建立在两个关键假设之上。第一，**主对齐假设**（Assumption A.2）：每个因果效应在 SAE 码空间中至少存在一个主导神经元，其对该效应的响应显著强于其他效应。当 SAE 使用 jump‑ReLU 等破坏该假设的非线性时，方法失效。第二，**信息充分性假设**：基础模型必须保留与潜在效应相关的全部信息；该假设在实际应用中难以直接验证。此外，极小样本（N≈30–50）且低效应量时，I 型和 II 型错误的平衡缺乏自动最优机制，当前需人工选择校正策略。方法目前仅适用于二值处理变量，对多值或连续处理的扩展尚未实现。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ml8t8kQMUP/figures/012_Figure.jpg]]
*Figure: Most activated images for Neuron 38 Most activated images for Neuron 6051*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ml8t8kQMUP/figures/016_Figure.jpg]]
*Figure: Most activated images for Neuron 3485 Most activated images for Neuron 2865*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ml8t8kQMUP/figures/020_Figure.jpg]]

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ml8t8kQMUP/figures/023_Figure.jpg]]

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ml8t8kQMUP/figures/026_Figure.jpg]]

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ml8t8kQMUP/figures/030_Figure.jpg]]

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ml8t8kQMUP/figures/033_Figure.jpg]]

## 方法谱系与知识库定位

### 1. 问题定位：探索性因果推断的独特挑战

本文所处理的问题——在未知潜在效应变量 Y 的情况下，从高维观测 X 中直接发现受处理影响的因果因子——处于因果推断、表示学习与可解释性研究的交叉地带。传统因果推断（Figure 2 左）假设研究者已知感兴趣的结果变量 Y，可直接测量并估计平均处理效应 $\tau = \mathbb{E}[Y(T=1) - Y(T=0)]$。预测驱动的因果推断（Prediction-Powered Causal Inference, Figure 2 中）则利用部分标注的 Y 训练预测模型，将缺失的 Y 从 X 中恢复。本文提出的探索性因果推断（Exploratory Causal Inference, Figure 2 右）更进一步：Y 完全未知，研究者仅拥有处理分配 T 和高维测量 X，目标是直接从数据中生成关于“什么被影响了”的可解释假设。

这一设定将因果发现从验证性范式推向探索性范式，其核心瓶颈并非效应估计的统计效率，而是**当测量通道（SAE 神经元）与潜在因果因子之间存在纠缠时，标准多重检验方法会在实验功效增强时发生显著性崩塌**——将所有与真实效应微弱关联的神经元全部标记为显著，导致发现结果丧失可解释性（Theorem 3.1, Theorem 3.2; Figure 3）。

### 2. 基线方法族系及其失效机制

论文系统比较了以下基线方法，并揭示了它们在探索性因果推断场景下的共同失效模式：

| 方法 | 核心机制 | 在 ECI 悖论下的表现 |
|------|----------|---------------------|
| **t-test (uncorrected)** | 对每个神经元独立执行两样本 t 检验，不做多重校正 | 假阳性率随 m 线性膨胀 |
| **Bonferroni correction** (Bonferroni, 1936) | 将显著性阈值设为 α/m，严格控制族系错误率 | 当 n 或 τ 增大时，所有纠缠神经元仍被拒绝（Theorem 3.1, 3.2），精确率急剧下降（Figure 5） |
| **FDR (Benjamini-Hochberg)** (Schweder and Spjøtvoll, 1982) | 控制错误发现率 | 与 Bonferroni 类似，在高功效时精确率和 IoU 趋于 0（Figure 5） |
| **top-k selection** | 直接选取效应绝对值最大的 k 个神经元，不做统计推断 | 在零效应消融中产生大量假阳性（Figure 32）；无法区分真实效应与纠缠泄漏 |
| **LASSO (logistic)** | 通过 ℓ₁ 惩罚的逻辑回归从 SAE 编码中反向选择与处理相关的神经元 | 性能与标准多重检验相当，仍无法克服悖论（Figure 37） |
| **Stability-selected LASSO** | 在多次自举子样本上重复 LASSO 拟合，根据稳定性得分选择神经元 | 同样无法克服显著性崩塌（Figure 37） |

这些方法的共同缺陷在于：它们将每个神经元视为独立的假设检验单元，忽略了 SAE 编码空间中由因果因子诱导的**纠缠结构**——一个潜在因子 $Y_k$ 会在多个神经元上产生非零效应方向 $v_k$（Equation 5），形成泄漏集合 $\mathcal{A}_\varepsilon$（Equation 6）。当实验功效足够高时，这些纠缠信号全部达到统计显著性，使方法无法区分“主导神经元”与“被泄漏的神经元”。

### 3. NES 与基线方法的核心差异

**Neural Effect Search (NES)** 通过三个关键设计从根本上区别于上述基线：

**（1）递归分层替代一次性检验。** 基线方法对所有 m 个神经元执行单轮假设检验；NES 采用迭代策略（Algorithm 1）：每轮选出当前最显著的神经元加入已选集合 S，随后通过分层（stratification）或臂内残差化（arm-wise residualization）消除该方向对其他神经元的泄漏影响，再对残余信号进行下一轮检验，直至无显著神经元。这等价于将因果效应发现转化为逐步解缠过程。

**（2）动态 Bonferroni 校正。** 每轮仅对当前未选神经元（数量为 $m - |S|$）应用 Bonferroni 校正（$\alpha/m$），而非一次性对所有 m 个神经元校正，从而在控制 I 型错误的同时保持对残余效应的检验功效（Algorithm 1 line 6）。

**（3）条件效应估计。** 基线方法直接使用关联差异 $\mathbb{E}[Z_j|T=1] - \mathbb{E}[Z_j|T=0]$ 估计每个神经元的效应；NES 在每轮中通过 pooled stratification（按已选神经元 $Z_S$ 分层）或臂内回归取残差，消除已发现方向 $v_k$ 的泄漏信号，使调整后的效应估计仅反映尚未识别的因果影响（Lemma A.1; Algorithm 2）。

**理论保证对比：** Theorem 4.1 证明，在适当假设（主对齐、效应解缠等）下，NES 以概率 1 恢复 r 个不同的受处理影响的神经元，即 $\Pr(S_{\text{final}} = \{j_1,\dots,j_r\}) \to 1$。而标准多重检验方法在大样本下会将整个泄漏集合 $\mathcal{A}_\varepsilon$ 全部拒绝（Theorem 3.1, 3.2），不存在类似的相合性。

### 4. 方法谱系中的位置

NES 可被定位为以下两条研究线的交汇：

**（1）多重检验的纠偏方法。** 传统多重检验校正（Bonferroni, FDR, Holm, Hochberg 等）关注的是独立或任意依赖结构下的错误率控制，但未考虑由潜在因果结构诱导的特定依赖形式。NES 通过递归分层利用了这一结构，可视为一种**结构感知的多重检验校正**——它不改变单次检验的统计量，而是通过条件化已发现效应来消除检验单元间的因果依赖。

**（2）效应解缠算法。** 在因果表示学习领域，解缠（disentanglement）通常指学习相互独立的潜在因子。NES 从不同角度切入：它不要求 SAE 编码本身完全解缠，而是在**推断阶段**通过逐步条件化实现效应的有原则分离。这使得 NES 对 SAE 的单语义性要求更为宽松——仅需满足主对齐假设（Assumption A.2），即每个因果效应存在一个主导神经元，而允许其他神经元存在不同程度的纠缠。

### 5. 适用边界与局限

**（1）主对齐假设的依赖性。** NES 的理论保证依赖于 Assumption A.2（主对齐）：每个受影响的潜在因子 $Y_k$ 存在一个神经元 $j_k$，其在 $v_k$ 方向上的分量显著大于其他神经元。当 SAE 使用 jump-ReLU 等非线性激活时，该假设可能被破坏，导致方法失效（Figures 20–26 消融实验证实了这一点）。对于高度多语义且无清晰主导神经元的表示，识别精度可能受限。

**（2）处理变量的限制。** 当前设计仅适用于**单一二值处理变量**。多值处理或连续处理的扩展尚未实现，这在观察性研究或剂量-响应实验中构成明显缺口。

**（3）结果变量的离散性。** 方法论建立在二值结果（离散概念）的设定上。SAE 的连续激活值虽然可计算统计量，但其因果推断的理论框架和可解释性映射尚不完善。

**（4）基础模型的充分性假设。** 整个流水线假设基础模型满足信息充分性 $\mathcal{I}(X, Y) = \mathcal{I}(\phi(X), Y)$，即 FM 表示保留了关于潜在效应 Y 的全部信息。这一假设在实际应用中难以验证，尤其当 Y 涉及细粒度或领域特定概念时。

**（5）小样本与低效应的权衡。** 在极小样本（如 30–50）且低效应量（τ 接近 0.1）时，I 型/II 型错误的平衡需要在探索性与严谨性之间折衷。当前 NES 未提供自动化的最优门控机制——消融实验（Figure 27）表明，Bonferroni 和 FDR 在足够功效下表现最优，而 t-test 在中功效区精度较低。

**（6）估计量的边际增益。** AIPW 估计量在 RCT 中仅提供边际效率增益，不改变显著性崩塌现象（Figure 29）。NES 的优势源于递归分层策略而非估计量选择，这意味着在观察性研究中，仅替换估计量不足以解决混淆问题。

### 6. 开放问题

1. **连续概念的因果推断。** 如何将 NES 推广到 SAE 连续激活值的因果效应发现与解释？这涉及连续处理变量的理论扩展和连续激活值的可解释性映射。

2. **无标注下的充分性评估。** 在没有标注 Y 的情况下，如何评估基础模型和 SAE 对潜在因果效应的信息充分性及单语义性？这本质上是一个无监督的表示质量评估问题。

3. **多模态测量的系统整合。** 多视角、多传感器的回旋增强（如同时使用视觉、音频、文本模态）如何系统整合到统一的探索性因果推断框架中？

4. **观察性研究的扩展。** 在存在混杂的非随机实验中，如何调整 NES 以控制混淆？这需要将递归分层与因果识别策略（如工具变量、双重稳健估计）结合。

5. **不确定性量化。** 如何量化所选神经元集合的不确定性并提供置信区间？当前 NES 输出的是点估计集合，缺乏对选择稳定性的统计推断。

6. **一次性解缠方法。** 是否存在一个非迭代的、一次性完成效应解缠的方法，在理论上同样一致且计算效率更高？这涉及对 SAE 编码空间中因果依赖结构的全局建模。

## 原文 PDF

![[paperPDFs/ICLR_2026/Exploratory_Causal_Inference_in_SAEnce.pdf]]
