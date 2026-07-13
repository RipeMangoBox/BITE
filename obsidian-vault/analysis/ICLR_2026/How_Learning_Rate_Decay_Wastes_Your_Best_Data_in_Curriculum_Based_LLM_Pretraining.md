---
title: "How Learning Rate Decay Wastes Your Best Data in Curriculum-Based LLM Pretraining"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/How_Learning_Rate_Decay_Wastes_Your_Best_Data_in_Curriculum_Based_LLM_Pretraining.pdf
project_link: null
code_link: null
openreview_forum_id: T5wkZJqzkz
aliases:
- CMACCDAMAC
- HLRDWYBDCBLP
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "学习率衰减的激进程度（结束学习率的大小或衰减步数）以及是否采用模型平均。通过适度增加结束学习率（例如接近峰值LR的1/3）或用模型平均（EMA/SMA）完全替代衰减，可以解除对高质量数据更新幅度的压制，充分释放课程学习的潜力。"
primary_logic: "学习率调度隐式地为每个训练样本赋予了重要性权重。标准实践中，为降低噪声而将学习率衰减至极小值，这恰恰抑制了课程学习后期出现的高质量数据的影响。通过在学习率与数据调度之间进行协同设计——采用温和的衰减或结合模型平均，可以在不牺牲训练稳定性的前提下，让模型从高质量数据中获得更大的参数更新，从而突破传统课程学习的收益瓶颈。"
claims:
- "在恒定学习率下，按质量升序排列的课程学习显著优于随机打乱的均匀训练。"
- "采用标准WSD或余弦学习率衰减后，课程学习相对于均匀训练的验证损失优势大幅缩小甚至消失。"
- "将WSD调度的结束学习率调至约1×10⁻³（峰值LR的1/3）能够有效缓解该冲突，并使得课程学习性能超过最优的均匀数据训练。"
- "用模型平均（如EMA）替代学习率衰减，并与课程学习结合（CMA），在多个下游基准上实现了优于标准WSD+均匀基线的性能。"
---

# How Learning Rate Decay Wastes Your Best Data in Curriculum-Based LLM Pretraining

> [!tip] 核心洞察
> 学习率调度隐式地为每个训练样本赋予了重要性权重。标准实践中，为降低噪声而将学习率衰减至极小值，这恰恰抑制了课程学习后期出现的高质量数据的影响。通过在学习率与数据调度之间进行协同设计——采用温和的衰减或结合模型平均，可以在不牺牲训练稳定性的前提下，让模型从高质量数据中获得更大的参数更新，从而突破传统课程学习的收益瓶颈。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 学习率衰减如何在基于课程学习的大语言模型预训练中浪费最佳数据 |
| 英文题名 | How Learning Rate Decay Wastes Your Best Data in Curriculum-Based LLM Pretraining |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=T5wkZJqzkz) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | Curriculum Model Averaging (CMA) 与 Combined Decay-aware Model Averaging (CDMA) |
| Dataset | Core benchmarks (MMLU, ARC-c, ARC-e, CSQA), 8 benchmarks average, Core benchmarks (mid-training), 8 benchmarks average (mid-training) |

> [!tip] 效果简介
> - Core benchmarks (MMLU, ARC-c, ARC-e, CSQA) 上，平均准确率 为 47.02 (SMA + Ascend + Const)，对比 46.21 (WSD + Uniform)，变化 +0.81。
> - 8 benchmarks average 上，平均准确率 为 50.94 (SMA + Ascend + Const)，对比 50.56 (WSD + Uniform)，变化 +0.38。
> - Core benchmarks (mid-training) 上，平均准确率 为 43.82 (EMA + A-T + Const)，对比 41.61 (WSD + U,U)，变化 +2.21。

## 概要

### 核心矛盾：学习率衰减与数据课程的不兼容性

在大语言模型的课程预训练中，一个普遍的做法是按数据质量从低到高安排训练顺序，期望模型先学习简单样本再逐步接触高质量数据。然而，标准的学习率调度——无论是余弦衰减还是WSD（Warmup-Stable-Decay）调度——都要求学习率在训练后期衰减至极低水平（典型结束学习率约为 $1 \times 10^{-5}$）。这种设计原本是为了降低噪声、稳定收敛，但在课程学习的语境下却产生了严重的冲突：当高质量数据被安排在训练后期时，学习率已经衰减到几乎无法产生有效参数更新的程度。

从SGD的参数更新公式可以直观理解这一矛盾：

$$\theta_{t+1} = \theta_t - \eta_t g_t$$

学习率 $\eta_t$ 直接缩放梯度更新量，因此学习率调度隐式地为每个训练样本分配了重要性权重。当 $\eta_t$ 在训练后期趋近于零时，高质量数据对模型参数的贡献被大幅压制，课程学习的潜在优势因此无法发挥。

### 现象验证

实验清晰地揭示了这一不兼容性（Figure 1）：
- **恒定学习率下**：按质量升序排列的课程学习显著优于随机打乱的均匀训练，验证损失更低且收敛更快。
- **WSD或余弦衰减下**：课程学习相对于均匀训练的优势大幅缩小甚至消失，在余弦衰减下退化尤为严重。
- **消融实验**（Figure 2）：增加WSD的衰减步数或降低结束学习率，会系统性地削弱课程学习的验证损失优势。

### 解决方案：两种互补策略

针对上述瓶颈，本文提出两种简单而有效的缓解策略：

1. **适度学习率衰减**：将WSD调度的结束学习率从常规的 $1 \times 10^{-5}$ 提升至约 $1 \times 10^{-3}$（约为峰值学习率的1/3）。这种温和的衰减既保留了训练后期的稳定性，又为高质量数据的更新保留了足够的幅度。实验表明，在此设定下课程学习能够超越最优的均匀数据训练。

2. **模型平均替代衰减**：用指数移动平均（EMA）或简单移动平均（SMA）完全替代学习率衰减。在恒定学习率下完成训练后，对最后若干检查点的参数进行加权平均，以稳定模型并降低噪声，同时保持对高质量数据的更新幅度。该方法与课程学习结合后，被称为**课程模型平均（Curriculum Model Averaging, CMA）**。

### 方法定位：协同设计的新范式

本文的核心贡献在于揭示了学习率调度与数据顺序之间的隐式耦合关系，并提出了协同设计的解决思路。在此基础上，进一步将适度衰减与模型平均结合，形成了**衰减感知的联合模型平均（Combined Decay-aware Model Averaging, CDMA）**，在适度衰减（结束学习率约 $1 \times 10^{-3}$）的基础上叠加EMA，产生了先前未被探索的协同优势。

### 主要结果

- **预训练场景**（Table 1）：CMA在核心基准（MMLU、ARC-c、ARC-e、CSQA）上达到47.02%的平均准确率，较WSD+均匀基线（46.21%）提升0.81个百分点，较广泛使用的余弦+均匀基线（44.31%）提升2.71个百分点。
- **Mid-training场景**（Table 2）：CMA的收益更加显著，核心基准平均提升超过2%（43.82% vs. 41.61%），验证了课程学习在数据质量差异更大时的有效性。
- **最优范式探索**（Figure 5）：通过扫描结束学习率并对比有无EMA/有无课程学习的组合，发现适度衰减（结束LR约 $1 \times 10^{-3}$）+ EMA + 课程学习构成最优范式，平均下游任务分数较基线提升1.68%。

### 理论支撑

在简化的二次损失理论模型中，本文证明了随机权重平均（SWA）方法可以突破标准WSD衰减的学习率下界，获得更低的期望损失，其期望损失上界为：

$$\mathbb{E}[\mathcal{L}(\bar{w}_M)] = \tilde{O}(M^{-\frac{2}{3}} L^2)$$

该理论结果为模型平均替代学习率衰减提供了形式化的支撑。

### 局限与待验证问题

当前实验验证主要基于1.5B参数模型和30B token数据量，更大规模下的效果尚待检验。课程学习的收益高度依赖数据质量评分的准确性，若评分模型与下游任务目标不一致，可能导致排序失效。此外，结束学习率的最优设定如何随模型规模和数据量缩放、模型平均能否在更广泛的预训练场景中完全取代学习率衰减，仍是开放问题。



### 大语言模型预训练中的数据质量与学习率调度

大语言模型（LLM）的预训练过程通常包含两个核心设计维度：**数据顺序**与**学习率调度**。在数据层面，传统预训练采用随机打乱的均匀顺序，而课程学习（curriculum learning）则主张将训练样本按质量从低到高排序，使模型先学习简单或低质量样本，再逐步接触高质量数据。在学习率层面，广泛使用的余弦衰减（**Loshchilov & Hutter, 2017**）和WSD（Warmup-Stable-Decay）调度（**Hu et al., 2024**）均将学习率从峰值衰减至极低水平（例如 $1 \times 10^{-5}$），以降低训练后期的噪声并促进收敛。

然而，这两个看似独立的设计选择之间存在一个被忽视的根本性冲突。

### 核心矛盾：课程顺序与学习率衰减的不兼容性

在基于课程学习的LLM预训练中，高质量数据被安排在训练后期。与此同时，标准学习率衰减调度已将学习率降至极低水平。根据SGD参数更新公式 $\theta_{t+1} = \theta_t - \eta_t g_t$，学习率 $\eta_t$ 直接缩放梯度更新量，隐式地为每个训练样本分配了重要性权重。当 $\eta_t$ 在后期衰减至接近零时，高质量样本对模型参数的更新贡献被大幅压制，导致课程学习无法发挥应有的优势。

这一矛盾在实验中得到了明确验证。如**Figure 1**所示，在恒定学习率下，按质量升序排列的课程学习显著优于随机打乱的均匀训练，验证损失更低且收敛更快。然而，当采用标准WSD或余弦学习率衰减后，课程学习相对于均匀训练的验证损失优势大幅缩小甚至完全消失——在余弦衰减下，性能退化更为严重。这表明，**标准学习率衰减策略在优化均匀数据顺序时行之有效，但对于课程学习却是次优的**。

### 现有方法的局限性

已有工作尝试通过数据折叠（data folding）策略缓解这一冲突：将数据划分为多个阶段，在每个阶段内进行排序（**Dai et al., 2025**）。如**Figure 3**所示，折叠策略在余弦衰减下确实能提供一定缓解，但仍无法超越均匀数据基线；而在恒定学习率下，简单的端到端升序排序反而更优，折叠策略的优势完全消失。这说明数据折叠并未从根本上解决学习率衰减对高质量数据的压制问题。

更一般地，实例级课程学习在先前研究中往往收益有限，其原因可能正源于学习率调度与数据顺序之间的深层不兼容性——这一系统性因素在此前的工作中未被充分重视。

### 本文动机与核心思路

本文识别并系统分析了上述瓶颈，提出两条互补的解决方案：

1. **适度学习率衰减**：将WSD调度的结束学习率从典型的 $1 \times 10^{-5}$ 提升至约 $1 \times 10^{-3}$（峰值学习率的约1/3），在保持训练稳定性的同时，为后期高质量数据保留足够的更新幅度。
2. **模型平均替代衰减**：用指数移动平均（EMA）或简单移动平均（SMA）完全替代学习率衰减，通过对最后若干检查点进行加权平均来降低噪声，同时保持恒定学习率以充分利用高质量数据。

通过将数据课程、适度学习率衰减与模型平均进行协同设计，本文旨在突破传统课程学习的收益瓶颈，建立一种先前未被探索的高效预训练范式。



## 核心方法与创新机理

本文的核心创新并非提出全新的算法架构，而是揭示并系统性地解决了一个在大语言模型课程预训练中长期被忽视的**调度冲突**：按数据质量升序排列的课程学习与逐渐衰减的学习率调度之间存在根本性的不兼容。在此基础上，作者通过两个关键“变更槽”（changed slots）的协同调整，将课程学习的潜力从标准衰减调度的压制中解放出来。

### 冲突诊断：学习率衰减作为隐式样本权重

标准预训练中，学习率调度不仅控制优化步长，更隐式地为每个训练样本分配了重要性权重。从SGD参数更新公式 $\\theta_{t+1} = \\theta_t - \\eta_t g_t$ 可以清晰看出，学习率 $\eta_t$ 直接缩放梯度更新量。当课程学习将高质量数据安排在训练后期时，标准WSD或余弦衰减已将 $\eta_t$ 降至接近零的极小值（如 $1 \times 10^{-5}$），导致高质量样本对模型参数的更新贡献被大幅削弱。**Figure 1** 的实验直接验证了这一冲突：在恒定学习率下，升序课程显著优于随机打乱的均匀训练（**Figure 1(a)**）；但采用WSD或余弦衰减后，课程学习的优势几乎消失甚至反转（**Figure 1(b,c)**）。这表明，问题不在于课程学习本身无效，而在于标准学习率调度与数据排序之间的错配。

### 变更槽一：适度学习率衰减

第一个关键变更是**调整学习率衰减的激进程度**。标准WSD调度将结束学习率设为 $1 \times 10^{-5}$（约为峰值 $3 \times 10^{-3}$ 的 $1/300$），这是为均匀数据顺序优化的设置。**Figure 2** 的消融实验表明，增加衰减步数或降低结束学习率会系统性削弱课程学习相对均匀训练的验证损失优势。相反，将结束学习率提升至约 $1 \times 10^{-3}$（峰值LR的约 $1/3$）时，课程学习的性能先升后降，在 $1 \times 10^{-3}$ 附近达到最优并超越最优的均匀数据训练（**Figure 5(a)**）。这一发现直接挑战了“学习率必须衰减至极小值”的惯性认知——对于课程学习而言，适度衰减才能让后期高质量数据的更新信号不被过度压制。

### 变更槽二：模型平均替代或补充衰减

第二个关键变更是**引入模型平均（Model Averaging）**。作者提出用指数移动平均（EMA）或简单移动平均（SMA）对训练最后若干个检查点进行加权平均，以稳定模型并降低噪声，同时保持对高质量数据的更新幅度。默认设置采用EMA（$\alpha=0.2$），对最后6个检查点进行平均。**Table 1** 的结果表明，将恒定学习率、升序课程与模型平均结合（CMA），在核心基准（MMLU, ARC-c, ARC-e, CSQA）上达到47.02的平均准确率，优于WSD+均匀基线（46.21），提升+0.81。更重要的是，EMA和SMA（赋予后期更高权重）在课程学习下优于加权移动平均（WMA），表明模型平均的权重分配应与数据质量趋势对齐——后期高质量数据对应更高的平均权重。

### 协同效应：CDMA与最优范式

当适度衰减与模型平均联合使用时，产生了**先前未被探索的协同优势**。**Figure 5** 通过扫描结束学习率并比较有无EMA/有无课程学习的各项组合，识别出一个“最优范式”：适度衰减（结束LR约 $1 \times 10^{-3}$）+ EMA + 升序课程。这一组合（CDMA）将平均下游任务分数较Uniform+WSD基线提升1.68%。在mid-training设置中，CMA的收益更加显著——核心基准平均提升超过2%（**Table 2**），因为两阶段训练中数据质量差异更大，课程学习的潜在收益空间也更大。

### 理论支撑

作者进一步通过简化的二次损失理论模型（$\mathcal{L}(\pmb{w}) = \frac{1}{2} \|\pmb{w} - \pmb{w}^*\|_2^2$）证明了：在均匀采样下，任何学习率调度都存在期望损失的下界；而随机权重平均（SWA）方法可以突破这一下界，获得更低的期望损失（**Theorem 4.1**）。**Figure 6** 的模拟可视化直观展示了不同策略在信号/噪声方向上的优化轨迹差异：Ascend+EMA能在信号方向上取得充分进展，而Ascend+WSD因过早衰减导致信号方向更新不足。

### 与基线方法的本质区别

与直接应用课程学习但未经针对性调度的组合（如Ascend + WSD）相比，本文的创新在于**将学习率调度、数据排序与模型平均作为联合设计空间进行系统探索**，而非将它们视为独立组件。标准基线（Uniform + WSD）为均匀数据优化了激进的衰减策略；本文证明，课程学习需要一套完全不同的调度配置——更温和的衰减或完全用模型平均替代衰减——才能释放其潜力。这一发现解释了为什么早期研究中实例级课程学习的收益往往不明显：在标准衰减调度下，高质量数据的更新贡献被系统性压制，课程学习的优势无法体现。



本文的核心贡献并非提出一个全新的训练架构，而是通过诊断**学习率调度与数据课程之间的隐性冲突**，构建了一套协同优化框架。该框架的核心思路是：将原本独立设计的学习率衰减策略与数据排序策略进行联合编排，使得高质量数据在训练后期仍能对参数产生足够幅度的更新。

### 核心矛盾：学习率衰减对课程学习的隐性压制

在大语言模型预训练中，标准实践通常采用两种独立的设计：
- **数据侧**：按质量升序排列训练样本（课程学习），将高质量数据置于训练后期；
- **优化侧**：采用逐渐衰减的学习率调度（如余弦衰减或WSD），使训练后期的学习率降至极低水平。

这两者之间存在根本性的不兼容。SGD参数更新公式 $ \theta_{t+1} = \theta_t - \eta_t g_t $ 表明，学习率 $\eta_t$ 直接缩放梯度的更新幅度，从而隐式地为每个训练样本分配了重要性权重。当高质量数据被安排在训练后期时，标准学习率衰减已将 $\eta_t$ 降至接近零的水平（如 $1\times10^{-5}$），导致这些高质量样本对模型参数的更新贡献被严重压制。

**Figure 1** 清晰地展示了这一矛盾：在恒定学习率下，升序课程学习（Ascend）显著优于随机打乱的均匀训练（Uniform）；但当采用WSD或余弦衰减后，课程学习的优势大幅缩小甚至完全消失。

### 框架总览：三阶段协同优化

针对上述矛盾，本文提出了一套由三个可组合模块构成的协同优化框架：

**模块一：数据质量评分与课程排序**

使用离线质量评估器（如DCLM fastText）为每个训练样本打分，并按质量分数对整个训练集进行**全局升序排列**。对于多领域数据，还需设计域内排序、秩重标定和全局交织的课程构建流程（详见附录D.1）。这一模块决定了“什么数据在何时出现”。

**模块二：学习率调度的重新校准**

框架支持两种互补策略：
- **恒定学习率 + 模型平均（CMA）**：完全放弃学习率衰减，在整个训练过程中保持恒定学习率，从而彻底解除对后期高质量数据更新幅度的压制。训练结束后，通过对最后若干检查点进行指数移动平均（EMA）或简单移动平均（SMA）来稳定模型并降低噪声。
- **适度衰减 + 模型平均（CDMA）**：保留WSD调度，但将结束学习率从常规的 $1\times10^{-5}$ 提升至约 $1\times10^{-3}$（峰值学习率的1/3），在保留部分衰减带来的收敛稳定性同时，避免过度压制后期更新。

**模块三：模型平均**

在训练结束时，对最后 $k$ 个检查点（默认 $k=6$）的参数进行加权平均。EMA的权重公式为：
$$ \bar{\pmb{\theta}}_{\mathrm{final}} = \frac{\sum_{i=0}^{k-1} \alpha^i \pmb{\theta}_{T-i}}{\sum_{i=0}^{k-1} \alpha^i} $$
其中 $\alpha=0.2$ 控制衰减率，赋予近期检查点更高权重。这一模块的关键作用在于：**在保持对高质量数据充分更新的前提下，通过平均化消除训练后期的噪声波动**，替代传统学习率衰减的降噪功能。

### 输入输出流与组合逻辑

整个框架的输入输出流如下：

1. **输入**：原始训练语料 → 质量评分器 → 按分数升序排列的数据流
2. **训练**：排序后的数据流 → 恒定LR或适度衰减LR下的标准SGD训练 → 定期保存检查点
3. **输出**：最后 $k$ 个检查点 → EMA/SMA模型平均 → 最终模型

三种策略组合对应不同的权衡：
- **CMA（恒定LR + EMA + 升序）**：最彻底的解耦方案，在预训练和mid-training设置下均取得显著提升（Table 1, Table 2）。
- **CDMA（适度衰减 + EMA + 升序）**：结合衰减的收敛稳定性与模型平均的降噪能力，在扫描结束学习率的实验中被识别为“最优范式”，平均下游任务分数较基线提升1.68%（Figure 5, Section 3.4）。
- **仅适度衰减（无模型平均）**：将WSD结束学习率调至约 $1\times10^{-3}$，虽不及CMA/CDMA，但已能使课程学习性能超越最优的均匀数据训练（Figure 5(a), Section 3.1）。

### 关键设计决策与证据

框架设计的几个关键决策均有实验支撑：

- **全局升序 > 阶段内折叠**：在恒定学习率下，端到端的全局升序排序优于数据折叠策略（Dai et al., 2025），后者仅在衰减调度下提供微小缓解（Figure 3）。
- **EMA/SMA优于WMA**：赋予后期更高权重的EMA和SMA在课程学习下优于加权移动平均（WMA），表明模型平均的权重分配应与数据质量趋势对齐（Table 1, Section 3.2）。
- **Mid-training收益更显著**：在混合质量数据的两阶段训练中，CMA的核心基准平均提升超过2%（Table 2），验证了课程学习在数据质量差异大时更为有效。

该框架的局限性在于：实验验证主要基于1.5B参数模型和30B token数据量，更大规模下的效果尚待检验；模型平均的超参数（EMA衰减率、平均窗口长度）未进行全面搜索；课程学习的收益高度依赖质量评分的准确性。



### 3.1 学习率调度与数据课程的冲突机制

标准预训练中，参数更新遵循 SGD 规则：

$$\theta_{t+1} = \theta_t - \eta_t g_t$$

学习率 $\eta_t$ 直接缩放梯度更新量，这意味着学习率调度隐式地为每个训练样本分配了重要性权重。在基于课程学习的预训练中，数据按质量分数升序排列（Ascend），高质量样本集中在训练后期。然而，标准学习率衰减（如 WSD 或余弦调度）将结束学习率降至极低水平（典型值 $\eta_T \approx 1\times 10^{-5}$），此时高质量数据产生的梯度更新被大幅压制，课程学习的优势因此被系统性削弱。

图 Figure 1 直观展示了这一冲突：在恒定学习率下，升序课程显著优于均匀基线；但在 WSD 或余弦衰减下，该优势大幅缩小甚至消失。图 Figure 2 的消融进一步证实，增加衰减步数或降低结束学习率会系统性缩小课程学习相对于均匀训练的验证损失优势（$\mathcal{L}_{\text{Uniform}} - \mathcal{L}_{\text{Ascend}}$ 趋于零）。

### 3.2 核心策略模块

#### 3.2.1 适度学习率衰减

缓解上述冲突的直接策略是采用更温和的衰减。WSD 调度在衰减阶段的瞬时学习率为：

$$\eta(t) = \eta_0 \left(1 - \sqrt{r(t)}\right) + \eta_T \sqrt{r(t)}$$

其中 $\eta_0$ 为峰值学习率（$3\times 10^{-3}$），$\eta_T$ 为结束学习率，$r(t)$ 为衰减进度。实验表明，将 $\eta_T$ 从 $1\times 10^{-5}$ 提升至约 $1\times 10^{-3}$（峰值 LR 的 1/3）时，课程学习的性能先升后降，在 $\eta_T \approx 1\times 10^{-3}$ 处达到最优并超越最优均匀训练（Figure 5(a)）。

#### 3.2.2 模型平均替代衰减

更彻底的方案是用模型平均完全替代学习率衰减。**Curriculum Model Averaging (CMA)** 的核心流程为：
1. 采用恒定学习率进行全量训练；
2. 对训练最后 $k$ 个检查点进行加权平均，得到最终模型参数。

默认配置使用指数移动平均（EMA），对最后 $k=6$ 个检查点进行加权：

$$\bar{\boldsymbol{\theta}}_{\text{final}} = \frac{\sum_{i=0}^{k-1} \alpha^i \boldsymbol{\theta}_{T-i}}{\sum_{i=0}^{k-1} \alpha^i}$$

其中 $\alpha=0.2$ 控制衰减率，赋予近期检查点更高权重。同时考察了简单移动平均（SMA）和加权移动平均（WMA）作为变体。

#### 3.2.3 协同组合（CDMA）

**Combined Decay-aware Model Averaging (CDMA)** 将适度衰减与模型平均联合使用：采用 WSD 调度但将 $\eta_T$ 设在中等水平（约 $1\times 10^{-3}$），并在训练结束时对最后若干检查点施加 EMA。Figure 5 显示，该组合在数据课程下产生了先前未被探索的协同优势，平均下游任务分数较 Uniform + WSD 基线提升 1.68%。

### 3.3 离线数据质量评分与排序

课程构建依赖离线质量评分器（如 DCLM fastText 或 PreSelect）为每个样本打分，并依据分数对训练集进行全局升序排列。对于多领域数据，流程包括域内排序、秩重标定和全局交织（详见附录 D.1）。在 mid-training 场景中，同时支持跨阶段的全局排序（A-T, All-Together）和阶段内独立排序（A, A）两种策略。

### 3.4 理论支撑

为解释上述经验发现，论文构建了一个简化理论模型。考虑二次损失函数：

$$\mathcal{L}(\boldsymbol{w}) = \frac{1}{2} \|\boldsymbol{w} - \boldsymbol{w}^*\|_2^2$$

其中 $\boldsymbol{w}^*$ 为全局最优参数。在梯度可分解为信号方向与噪声方向的假设下（Figure 4），理论分析表明：均匀采样下任何学习率调度均存在期望损失下界；而随机权重平均（SWA）方法可突破该下界，获得更低的期望损失：

$$\mathbb{E}[\mathcal{L}(\bar{\boldsymbol{w}}_M)] = \tilde{O}(M^{-\frac{2}{3}} L^2)$$

该结论从理论上印证了“用模型平均替代过度衰减可更好地利用课程学习中高质量数据”的核心洞见（Theorem 4.1，Figure 6 模拟可视化）。



## 实验与关键发现

### 核心矛盾：学习率衰减与课程学习的结构性冲突

本研究的实验起点是一个看似简单但长期被忽视的观察：在**恒定学习率**下，按数据质量升序排列的课程学习（Ascend）能够显著优于随机打乱的均匀训练（Uniform），验证损失更低且收敛更快（Figure 1(a)）。然而，当引入当前大语言模型预训练中广泛使用的学习率衰减调度后，这一优势几乎消失殆尽。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_T5wkZJqzkz/figures/001_Figure_1.jpg]]
*Figure 1: Data curriculum strategies are less effective when combined with learning rate (LR) schedules that decay to a low scale near the end. (a-c) Experiments on a 1.5B parameter model trained on 30B tokens compare various data curricula (Uniform, Ascending-Order, and Descending-Order by DCLM score (Li et al., 2024)) under constant, Warmup-Stable-Decay (WSD) (Hu et al., 2024; Hagele et al., 2024), and cosine schedules. ¨ While curricula improve validation loss over a uniform baseline with a constant LR, this advantage is significantly reduced during a low-LR phase following LR decay. (d) In the data curriculum, high-quality data is placed in the latter phase, which coincides with the LR decaying t...*

具体而言，在 **WSD（Warmup-Stable-Decay）调度**（Hu et al., 2024）下，课程学习相对于均匀训练的验证损失优势大幅缩小（Figure 1(b)）；而在**余弦衰减**下，性能退化更为严重（Figure 1(c)）。这一现象的根本原因在于参数更新公式所揭示的隐式权重机制：

$$\theta_{t+1} = \theta_t - \eta_t g_t$$

学习率 $\eta_t$ 直接缩放每个样本的梯度更新量，因此学习率调度隐式地为训练序列中的每个样本分配了重要性权重。当高质量数据被安排在训练后期时，标准衰减调度已将学习率压至极低水平（如 $1 \times 10^{-5}$），从而大幅削弱了这些高质量样本对模型参数的更新贡献。

进一步的消融实验系统性地验证了这一因果链条。Figure 2 展示了在不同衰减步数（Long、Mid、Short、Zero）和不同结束学习率（$1 \times 10^{-5}$ 至 $3 \times 10^{-3}$）下，课程学习与均匀训练的验证损失差异。结果表明：**衰减步数越多、结束学习率越低，课程学习相对于均匀训练的优势就越小**。这确证了激进的学习率衰减是抑制课程学习收益的直接原因。

### 策略一：适度学习率衰减

最直接的缓解策略是调整学习率衰减的激进程度。实验在 WSD 调度下扫描结束学习率，从标准的 $1 \times 10^{-5}$ 逐步提升至 $1 \times 10^{-3}$（峰值学习率 $3 \times 10^{-3}$ 的约 1/3）。如 Figure 5(a) 所示，随着结束学习率的提高，课程学习的性能呈现先升后降的趋势，在约 $1 \times 10^{-3}$ 处达到最优，并**超越了经过调优的最优均匀训练结果**。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_T5wkZJqzkz/figures/007_Figure_5.jpg]]
*Figure 5: This figure compares various training strategies, identifying a high-performing and previously underexplored Optimal Regime where moderate learning rate (LR) decay, weight averaging, and curriculum learning produce synergistic advantages. We run experiments on both Uniform (uniformly ordered data) and Ascend (training data arranged by ascending DCLM scores) data schedules. For both schedules, we conduct an ablation on the ending learning rates of WSD schedules, ranging from 1 $\times$ 1 $0 ^ { - 5 } \mathrm { t o }$ 1 $\times$ 1 $0 ^ { - 3 }$ , representing aggressive to moderate LR decay. We denote strategies applying weight averaging as E M A , which compute the final model checkpoint via an EMA...

这一发现揭示了一个关键事实：均匀数据排序与课程数据排序对学习率衰减的需求存在根本性差异。均匀训练偏好更激进的衰减以降低噪声，而课程训练需要更温和的衰减以保留对后期高质量数据的更新能力。若不加调整地沿用为均匀训练优化的超参数，将系统性低估课程学习的潜力。

### 策略二：用模型平均替代学习率衰减

更为彻底的解决方案是**课程模型平均（Curriculum Model Averaging, CMA）**。该方法的核心思路是用恒定学习率配合模型平均，完全解除学习率衰减对后期高质量数据更新的压制。具体操作为：在整个训练过程中保持恒定学习率，训练结束后对最后 $k$ 个检查点进行加权平均（默认 $k=6$，指数移动平均 EMA，衰减率 $\alpha=0.2$）：

$$\bar{\boldsymbol{\theta}}_{\mathrm{final}} = \frac{\sum_{i=0}^{k-1} \alpha^i \boldsymbol{\theta}_{T-i}}{\sum_{i=0}^{k-1} \alpha^i}$$

Table 1 报告了 CMA 与各基线在标准下游基准上的全面对比。在核心基准（MMLU、ARC-c、ARC-e、CSQA）上，**SMA + Ascend + Const 组合达到 47.02 的平均准确率**，较 WSD + Uniform 基线（46.21）提升 **+0.81**，较广泛使用的 Cosine + Uniform 设置（44.31）提升 **+2.71**。在 8 个基准的平均准确率上，CMA 同样取得 +0.38 的稳定提升。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_T5wkZJqzkz/figures/004_Table_1.jpg]]
*Table 1: Curriculum Model Average (CMA) exhibits advantages over standard LR decay schedule pretraining, much better than the widely used Cosine+Uniform setting. Our proposed methods are highlighted in gray. WA: Weight Averaging technique (Section B). Order: Data ordering. LRS: Learning Rate Schedule (WSD: Warmup-Stable-Decay, Cos: Cosine, Const: Constant). Core: Average score on the first four, high signalto-noise tasks according to prior work (Heineman et al., 2025) (MMLU, ARC-c, ARC-e, CSQA). Both the Core and Avg. scores are annotated with a subscript indicating the performance change relative to the baseline ( W S D + U n i f o r m ) . Performance changes are color-coded: bold green ( $\geq$ 0 ....*

关于模型平均方法的选择，实验对比了简单移动平均（SMA）、指数移动平均（EMA）和加权移动平均（WMA）。结果表明，**SMA 和 EMA（赋予后期检查点更高权重）在课程学习下优于 WMA**，这验证了一个直觉：模型平均的权重分配应与数据质量的变化趋势对齐——后期高质量数据对应的检查点应获得更高权重。

值得注意的是，在恒定学习率下将模型平均与均匀数据排序结合（EMA + Uniform）并不能完全匹配标准 WSD 调度的性能，说明模型平均与课程学习之间存在**协同效应**，单独使用任一策略都不足以完全释放潜力。

### 策略三：联合优化——CDMA

将适度衰减与模型平均相结合，形成了**联合衰减感知模型平均（Combined Decay-aware Model Averaging, CDMA）**。Figure 5 通过扫描结束学习率并比较有无 EMA、有无课程学习的各项组合，识别出一个此前未被充分探索的“最优范式”：适度衰减 + EMA + 课程学习。在该范式下，**平均下游任务分数较 Uniform + WSD 基线提升 1.68%**，实现了三者的协同优势。

这一最优范式与此前研究的关注焦点形成鲜明对比。先前工作通常将结束学习率设定在峰值学习率的十分之一（约 $1 \times 10^{-4}$，Dubey et al., 2024; DeepSeek-AI et al., 2024）或固定在 $1 \times 10^{-5}$ 左右（Li et al., 2024; 2025b），这些设定恰好是课程学习收益被严重压制的区间。

### Mid-Training 设置下的放大效应

在混合质量数据的两阶段 mid-training 场景中，CMA 的优势更加显著。Table 2 显示，**EMA + A-T（全局升序排序）+ 恒定学习率组合在核心基准上平均提升 +2.21**（43.82 vs. 41.61），在 8 个基准上平均提升 +1.20。这一放大效应符合预期：mid-training 中数据质量差异更大，课程学习的潜在收益更高，而标准衰减调度的压制效应也更明显。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_T5wkZJqzkz/figures/006_Table_2.jpg]]
*Table 2: The benefit of CMA becomes more prominent in the mid-training setting. Our proposed methods are highlighted in gray. WA: Weight Averaging technique (Section B). Order: Data ordering in two phases (U: Uniform, A: Ascend). A-T (All-Together) sorts data samples in both phases as a whole. LRS: Learning Rate Schedule (WSD: Warmup-Stable-Decay schedule, Const: Constant LR). Core: Average score on the first four, high signal-to-noise tasks (MMLU, ARC-c, ARC-e, CSQA). Both the Core and Avg. scores are annotated with a subscript indicating the performance change relative to the baseline ( W S D + U , $\bar { U }$ ) . Performance changes are color-coded: bold green (≥ 0.5 improvement), light green (> 0...*

实验还验证了一个实用的简化策略：在每个训练阶段内独立进行升序排序（A,A），而非全局排序（A-T）。该简化策略在恒定学习率下仍取得核心分数 43.61（+2.00 vs. 基线），证明了方法的工程可行性。但仅在最后的高质量数据阶段应用课程学习（U,A）并不足以获得最优结果，说明数据排序应贯穿整个训练过程。

### 理论验证：二次损失模型下的分析

为从理论上理解上述现象，本文构建了一个简化的二次损失模型：

$$\mathcal{L}(\boldsymbol{w}) = \frac{1}{2} \|\boldsymbol{w} - \boldsymbol{w}^*\|_2^2$$

在该模型下，理论分析表明：均匀采样配合任意学习率调度，期望损失存在一个下界，而 WSD 衰减会进一步收紧这一下界。相比之下，随机权重平均（SWA）方法可以突破该下界，获得更低的期望损失（Theorem 4.1）。Figure 6 的模拟实验直观展示了不同策略在信号方向和噪声方向上的优化轨迹：Ascend+EMA 能够在信号方向上取得充分进展，而 Ascend+WSD 因过早衰减导致信号方向更新不足，Uniform+WSD 则因信号不一致导致信号方向方差过大。

### 失败模式与局限性

1. **数据折叠策略的有限缓解**：先前工作提出的“数据折叠”（data folding）策略（Dai et al., 2025）在余弦衰减下对课程学习有一定缓解作用，但仍不及均匀基线；在恒定学习率下，简单端到端排序反而更优（Figure 3）。这表明折叠策略只是对衰减冲突的局部修补，而非根本性解决方案。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_T5wkZJqzkz/figures/003_Figure_3.jpg]]
*Figure 3: A stage-wise “data folding” curriculum mitigates the negative interaction observed between data ordering and learning rate (LR) decay (detailed in Section 2), but data folding can not match end-to-end sorting under a constant learning rate. Left: We compare simple ascending curricula (Ascend), sorted by DCLM score, against their “folding” counterparts (Ascend+Folding). The folding method involves partitioning the data into stages (three in our implementation) and performing the sort within each stage. The Descend(+Folding) curriculum is designed in reverse order. Middle: Under a standard cosine LR schedule, folding strategies reduce validation loss compared to simple sorting but are outperf...*

2. **质量评分依赖性**：课程学习的收益高度依赖数据质量评分的准确性。实验发现，当使用 PreSelect 评分替代 DCLM fastText 评分时，课程学习的提升幅度有所变化（Table 6），说明评分模型与下游任务目标的一致性至关重要。在部分领域（如代码），仅采用 GitHub 星标数作为质量度量过于粗糙，导致提升有限。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_T5wkZJqzkz/figures/014_Table_6.jpg]]
*Table 6: Downstream performance for experiments with PreSelect score ascending data. Our proposed methods (using WA) are highlighted in gray. WA: Weight Averaging (EMA: Exponential, SMA: Simple). LRS: Learning Rate Schedule (WSD: WSD with decay to 1 $\times$ 1 $0 ^ { - 5 }$ , Const: Constant LR, WSMD: WSD with moderate decay to 1 $\times$ 1 $0 ^ { - 3 }$ ) . Core: Average score on the first four, high signal-to-noise tasks (MMLU, ARC-c, $\operatorname { A R C - e } , \operatorname { C S Q A }$ ) . Both Core and Avg. scores are annotated with a subscript indicating the performance change relative to the baseline (first row). Subscripts in bold green indicate an improvement of $\geq$ 0 . 5 , light green an improv...

3. **超参数敏感性**：模型平均的 EMA 衰减率（0.2）和平均窗口长度（最后 6 个检查点）在实验中固定，未进行全面搜索。不同模型规模或数据量下可能需要额外调优。

4. **规模验证不足**：当前实验主要基于 1.5B 参数模型和 30B token 数据量，更大规模下的效果尚待检验。结束学习率的最优设定如何随模型规模和训练数据量缩放，是否存在一致的缩放定律，仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_T5wkZJqzkz/figures/002_Figure.jpg]]
*Figure: (a) Validation loss for different decay steps. (b) LUniform − LAscend (c) Validation loss for different ending LRs. (d) \mathcal { L } _ { \mathrm { U n i f o r m } } - \mathcal { L } _ { \mathrm { A s c e n d } }*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_T5wkZJqzkz/figures/010_Figure_7.jpg]]
*Figure 7: Downstream task scores and validation losses show high correlation according to the Pearson correlation coefficient (r) and R-square value ( R ^ { 2 } ) . Average is the average score of the total 8 downstream t,asks and Core is the average score of the first 4 downstream tasks (MMLU, ARC-c/e, CSQA) in Tables 1 and 2*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_T5wkZJqzkz/figures/013_Figure_8.jpg]]
*Figure 8: The benefits of a data curriculum using PreSelect scores also diminish. We show the validation loss curves for constant and WSD LR schedules under different data schedules, including uniform, ascending, and descending orders by PreSelect scores. Overall, the ascending curriculum outperforms the uniform baseline under a constant schedule, but cannot match it under the WSD LR schedule. The final validation loss of the data curriculum is higher than that of the uniform-ordering baseline, likely because the score metrics are not perfectly targeted to the validation set*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_T5wkZJqzkz/figures/009_Table_3.jpg]]
*Table 3: Model and optimizer hyperparameters for our Qwen2.5-1.5B experiments*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_T5wkZJqzkz/figures/011_Table_4.jpg]]
*Table 4: Models trained under WSD schedules under 1-sqrt and sqrt-cube decay functions produce similar results*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_T5wkZJqzkz/figures/012_Table_5.jpg]]
*Table 5: Model Checkpoint Weights. Index −k corresponds to the last k-th checkpoint*



## 定位与知识库关联

### 核心矛盾：数据课程与学习率衰减的隐性冲突

本研究揭示了一个此前被忽视的系统性矛盾：在大语言模型预训练中，按数据质量升序排列的课程学习策略与标准学习率衰减调度之间存在根本性的不兼容。这一矛盾的根源在于参数更新公式 $\theta_{t+1} = \theta_t - \eta_t g_t$ 中，学习率 $\eta_t$ 隐式地为每个训练样本分配了重要性权重。当高质量数据被安排在训练后期时，标准余弦衰减或 WSD 衰减（**Warmup-Stable-Decay**，Hu et al., 2024）已将学习率降至接近零的水平（典型结束学习率约为 $1 \times 10^{-5}$），从而大幅削弱了这些高质量样本对模型参数的更新贡献，导致课程学习的潜在优势被系统性地压制。

这一发现解释了为什么实例级课程学习在以往研究中收益往往不明显——先前工作普遍为均匀随机打乱的数据顺序优化学习率调度（如 **Cosine LR schedule**，Loshchilov & Hutter, 2017），而未意识到数据排序与学习率调度之间存在需要协同设计的耦合关系。当直接将这些为均匀数据优化的调度应用于课程学习时，课程学习的真实潜力被严重低估。

### 从冲突诊断到协同设计：CMA 与 CDMA

本研究提出的解决方案遵循一条递进的协同设计路径：

**第一层：解除压制——适度衰减替代激进衰减。** 最直接的缓解策略是将 WSD 调度的结束学习率从标准的 $1 \times 10^{-5}$ 提升至约 $1 \times 10^{-3}$（峰值学习率的约 1/3）。这一调整使得训练后期的学习率仍保持足够大的量级，从而允许高质量数据产生有意义的参数更新。消融实验（Figure 5(a)）表明，结束学习率从 $1 \times 10^{-5}$ 逐步提升至 $1 \times 10^{-3}$ 时，课程学习的性能先升后降，在约 $1 \times 10^{-3}$ 处达到最优并超越最优的均匀数据训练。这一发现直接挑战了“学习率必须衰减至极小值以保证收敛”的普遍认知。

**第二层：完全解耦——CMA（Curriculum Model Averaging）。** 更彻底的方案是用模型平均完全替代学习率衰减。CMA 采用恒定学习率进行全训练过程，并在训练结束时对最后 $k$ 个检查点进行指数移动平均（EMA，默认 $\alpha = 0.2$，$k = 6$）：

$$\bar{\pmb{\theta}}_{\mathrm{final}} = \frac{\sum_{i=0}^{k-1} \alpha^i \pmb{\theta}_{T-i}}{\sum_{i=0}^{k-1} \alpha^i}$$

这一设计的核心直觉是：模型平均通过参数空间中的平滑操作降低噪声，而非通过缩小更新步长来压制所有信号——包括高质量数据带来的有价值信号。Figure 4 从损失景观的角度阐释了这一差异：Ascend+EMA 能够在信号方向上保持足够的推进力，同时在噪声方向上通过平均实现平滑，而 Ascend+Decay 则因早期衰减导致信号方向的更新不足。

**第三层：协同优势——CDMA（Combined Decay-aware Model Averaging）。** 进一步研究发现，适度衰减与模型平均之间存在协同效应。CDMA 将数据课程、适度学习率衰减与 EMA 联合设计，形成了一个先前未被探索的高效预训练范式。在 DCLM 基准上，CDMA 最佳组合的平均下游任务分数较 Uniform+WSD 基线提升 1.68%（Figure 5）。这一“最优范式”与“先前关注范式”（无数据课程、无模型平均、结束学习率在 $1 \times 10^{-5}$ 至 $1 \times 10^{-4}$ 之间）形成鲜明对比。

### 与现有方法的定位关系

**相对于标准预训练基线：** 本研究的方法直接对标并超越了两类主流基线——**Cosine+Uniform**（Loshchilov & Hutter, 2017）和 **WSD+Uniform**（Hu et al., 2024）。Table 1 显示，SMA+Ascend+Const 在 Core benchmarks 上达到 47.02，显著优于 Cosine+Uniform 的 44.31 和 WSD+Uniform 的 46.21。值得注意的是，直接组合 WSD+Ascend 仅能提供边际增益，甚至可能降低性能，这进一步验证了协同设计的必要性。

**相对于课程学习变体：** 与 **Data folding curriculum**（Dai et al., 2025）相比，本研究发现在恒定学习率下，简单的端到端全局升序排序优于阶段内折叠策略。折叠策略仅在余弦衰减下提供微小缓解，但仍不及均匀基线（Figure 3）。这表明折叠策略本质上是对 LR 衰减冲突的一种不完美补偿，而非根本性解决方案。

**相对于模型平均方法：** 本研究系统比较了 SMA、EMA 和 WMA 三种平均策略。关键发现是 EMA 和 SMA（赋予后期检查点更高权重）在课程学习下优于 WMA，表明模型平均的权重分配应与数据质量趋势对齐——后期高质量数据对应的检查点应获得更高权重。

### 适用边界与局限

**模型规模与训练数据量的外推性：** 当前验证主要基于 Qwen2.5-1.5B 模型和 30B token 数据量。结束学习率的最优设定（约 $1 \times 10^{-3}$）如何随模型规模和训练数据量缩放，是否存在一致的缩放定律，尚待更大规模实验验证。

**数据质量评分的依赖性：** 课程学习的收益高度依赖数据质量评分的准确性。本研究主要使用 DCLM fastText 评分，在附录中也验证了 PreSelect 评分的一致性。然而，若评分模型与下游任务目标不一致，可能导致排序失效或性能下降。在多领域课程构建中，部分领域（如代码）的质量度量不够精细（仅采用 GitHub 星标数），导致在这些领域上的提升有限。

**模型平均超参数的敏感性：** 当前实验中 EMA 衰减率（$\alpha = 0.2$）和平均窗口长度（最后 6 个检查点）固定，未进行细粒度超参数搜索。在不同模型规模或训练设置下，这些超参数可能需要额外调优以达到最佳性能。

**恒定学习率训练的不稳定性风险：** 虽然 CMA 在 1.5B 规模实验中表现稳定，但在更大规模或更长训练周期中，完全移除学习率衰减可能引入训练不稳定性的风险。CDMA 通过保留适度衰减部分缓解了这一担忧，但该策略的普适性仍需进一步验证。

### 开放问题

1. **缩放定律的建立：** 课程学习中结束学习率的最优设定如何随模型规模和训练数据量缩放？是否存在一致的缩放定律，使得小规模实验中的发现可直接外推至大规模训练？

2. **模型平均与学习率衰减的替代关系：** 模型平均能否在更广泛的预训练场景中完全取代学习率衰减并保持稳定性，还是两者的结合（如 CDMA）更具普适性？这一问题的答案可能依赖于模型规模和训练时长。

3. **自动化联合优化：** 能否开发自动化的超参数搜索策略，根据数据质量分布和任务目标动态联合优化数据排序、学习率调度和模型平均？这需要建立数据质量分布与最优调度参数之间的映射关系。

4. **多阶段训练中的协同：** 在多阶段预训练与微调流水线中，课程学习应如何与其他训练技术（如知识蒸馏、强化学习反馈等）协同工作？Mid-training 实验（Table 2）已初步展示了 CMA 在混合质量数据场景中的显著收益（核心基准平均提升超过 2%），但更复杂的多阶段流水线仍有待探索。

5. **深层制约因素的挖掘：** 为什么在早期研究中实例级课程学习的收益往往不明显——除了 LR 衰减，是否还存在其他深层优化或数据相关的制约因素？例如，优化器的自适应学习率机制、梯度噪声结构或批次内数据混合策略是否也与课程学习存在隐性冲突？



## 原文 PDF

![[paperPDFs/ICLR_2026/How_Learning_Rate_Decay_Wastes_Your_Best_Data_in_Curriculum_Based_LLM_Pretraining.pdf]]
