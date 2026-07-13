---
title: "Watermarking Diffusion Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Watermarking_Diffusion_Language_Models.pdf
project_link: null
code_link: https://github.com/eth-sri/diffusion-lm-watermark
openreview_forum_id: 3aBWTYGcaT
aliases:
- DW
- WDLM
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "在上下文哈希分布上以期望方式施加Red‑Green水印，同时增加能使其他token变绿的token概率（即期望增强与预测偏置两项）来最大化生成序列中绿色token的比例。"
primary_logic: "将DLM水印建模为约束优化问题：最大化生成序列的期望绿色token比，同时约束每步分布与原始分布的KL散度。该优化问题的解自然导出两个分量——对上下文哈希分布的期望增强（Red‑Green in expectation）和使后续token更易成为绿色的预测偏置（predictive bias），且可直接复用现有的Red‑Green检测器。"
claims:
- "在LLADA‑8B和DREAM‑7B上，本文方法在1% FPR下检测率（TPR@1）达到99%，而基线方法仅0.49–0.83。"
- "在相同log PPL质量下，本文方法的检测率显著优于朴素基线，且仅需约50 token即可达到基线约350 token的检测性能。"
- "本文方法对局部修改（删除、替换）保持强检测能力，在30%的序列被修改时仍有效。"
- "LLADA‑8B (WATERBENCH prompts, 275 tokens avg) 上 TPR@1%FPR = 0.99"
---

# Watermarking Diffusion Language Models

> [!tip] 核心洞察
> 将DLM水印建模为约束优化问题：最大化生成序列的期望绿色token比，同时约束每步分布与原始分布的KL散度。该优化问题的解自然导出两个分量——对上下文哈希分布的期望增强（Red‑Green in expectation）和使后续token更易成为绿色的预测偏置（predictive bias），且可直接复用现有的Red‑Green检测器。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 扩散语言模型的水印方法 |
| 英文题名 | Watermarking Diffusion Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=3aBWTYGcaT) · [GitHub](https://github.com/eth-sri/diffusion-lm-watermark) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | DLM Watermark（基于优化框架的期望增强与预测偏置） |
| Dataset | LLADA‑8B (WATERBENCH prompts, 275 tokens avg), DREAM‑7B (WATERBENCH prompts, 213 tokens avg), LLADA‑8B vs Order‑Agnostic Watermarks (Unigram, PatternMark) |

> [!tip] 效果简介
> - LLADA‑8B (WATERBENCH prompts, 275 tokens avg) 上，TPR@1%FPR 为 0.99，对比 0.63 (for C={-1}, δ=4)，变化 +0.36。
> - DREAM‑7B (WATERBENCH prompts, 213 tokens avg) 上，TPR@1%FPR 为 0.99，对比 0.49 (for C={-1}, δ=4)，变化 +0.50。
> - LLADA‑8B (WATERBENCH prompts, 275 tokens avg) 上，log PPL (quality) 为 1.90 (C={-1},δ=4) / 1.80 (C={-1,1},δ=5)，对比 1.93 (C={-1},δ=4) / 1.86 (C={-1,1},δ=5)，变化 similar or slightly better。

## 概要

**核心问题**：现有自回归语言模型（ARLM）的水印方法依赖已生成的上下文token进行哈希计算，但扩散语言模型（DLM）允许以任意顺序生成token，导致上下文在生成时往往尚不完整。直接将ARLM水印适配到DLM场景，检测率极弱（TPR@1%FPR仅为0.49–0.83），无法实用。

**核心思路**：将DLM水印建模为一个约束优化问题——最大化生成序列的期望绿色token比例，同时约束每步分布与原始分布的KL散度。该优化问题的解自然导出两个分量：（1）**期望增强**，即在上下文哈希的概率分布上以期望方式施加Red‑Green水印；（2）**预测偏置**，即提升那些能使其他token变绿的token的概率。该方法可直接复用现有的Red‑Green检测器，无需修改。

**主要结果**：
- 在LLADA‑8B和DREAM‑7B上，本文方法在1%假阳性率下的检测率（TPR@1）达到**99%**，而朴素基线仅为0.49–0.83（Table 1）。
- 在相同文本质量（log PPL）下，本文方法的检测率显著优于基线，且仅需约**50 token**即可达到基线约350 token的检测性能（Fig. 2）。
- 对局部修改（删除、替换）保持强检测能力，在30%的序列被修改时仍有效（Fig. 3）。

**方法定位**：该方法在方法谱系上属于**优化驱动的扩散语言模型水印**，将Red‑Green水印框架（Kirchenbauer et al., 2023）从自回归场景推广到非自回归的扩散生成场景，通过概率哈希分布上的期望操作解决了上下文不完整带来的核心瓶颈。与顺序无关水印（如Unigram、PatternMark）相比，本文方法在低失真区间的检测率-质量权衡上具有显著优势（Fig. 5）。



### 扩散语言模型的兴起与生成范式的转变

近年来，扩散语言模型（Diffusion Language Models, DLMs）作为一种新兴的文本生成范式受到广泛关注。与传统的自回归语言模型（Autoregressive Language Models, ARLMs）从左到右逐token生成不同，DLMs通过迭代去噪过程生成文本，允许在任意位置、任意顺序更新token。这种非自回归的生成方式带来了独特的优势，但也对现有的技术生态提出了新的适配需求。

### 现有水印方法的根本局限性

当前主流的水印方法，尤其是Red‑Green类型的水印（**KGW**, Kirchenbauer et al., 2023），其核心机制依赖于**已生成的上下文token**进行哈希计算，从而确定当前token的颜色（绿色或红色），并对绿色token的logit施加偏置。这一机制在ARLM中运行良好，因为生成过程严格从左到右，每个token生成时其上下文已完全确定。

然而，在DLM的扩散生成过程中，token可以在任意顺序下被更新或重新掩码，**上下文在生成时常常尚不完整**。直接将ARLM水印应用于DLM——即仅对上下文已确定的token施加水印——会导致水印信号极度稀疏，检测效果极弱。实验表明，这种朴素适配方案在LLADA‑8B和DREAM‑7B上，在1%误报率（FPR）下的检测率（TPR@1）仅能达到0.49–0.83，远不能满足实际应用需求（Table 1）。

### 核心挑战与本文动机

这一困境的根本瓶颈在于：**DLM的任意顺序生成特性使得“上下文”成为一个概率性概念，而非确定性存在**。传统水印依赖的确定性上下文哈希在DLM中不再天然成立，导致水印信号注入的时机和位置难以确定。

本文的核心动机在于，将DLM水印问题从“何时施加水印”的工程适配问题，提升为一个**约束优化问题**：在限制每步分布与原始分布KL散度的前提下，最大化生成序列的**期望绿色token比例**。这一框架的直觉在于：既然上下文在生成时不确定，就在上下文哈希的概率分布上以期望方式施加Red‑Green水印，同时利用能使其他token变绿的token概率偏置，从而在扩散生成的全过程中持续注入水印信号。

该优化框架的解自然导出两个关键分量——**期望增强（Red‑Green in expectation）** 与**预测偏置（predictive bias）**——且可直接复用现有的Red‑Green检测器，无需修改检测端。这一设计使得本文方法在保持与现有水印生态兼容的同时，从根本上解决了DLM场景下的水印失效问题。



## 核心方法与创新机理

### 问题瓶颈：扩散生成中上下文哈希的缺失

现有自回归语言模型（ARLM）的 Red‑Green 水印（如 **KGW**，Kirchenbauer et al., 2023）依赖一个核心机制：在生成每个 token 时，基于其**已确定的上下文**计算哈希值，再根据哈希将词表划分为绿色列表和红色列表，并对绿色 token 施加 logit 偏置。然而，扩散语言模型（DLM）以任意顺序生成 token——token 的上下文在生成时常常**尚未确定**。直接套用 ARLM 水印策略（仅在上下文已确定时施加水印，否则不施加）会导致大量 token 未被水印，检测率极低。

这一瓶颈在实验中得到了量化验证：在 LLADA‑8B 和 DREAM‑7B 上，朴素基线（Naive ARLM Adaptation）在 1% 假阳性率下的检测率（TPR@1）仅为 0.49–0.83，而本文方法达到 0.99（Table 1）。图 2（右）进一步表明，本文方法仅需约 **50 token** 即可达到基线约 **350 token** 的检测性能——效率差距近 7 倍。

### 核心洞察：将水印建模为约束优化问题

本文的关键创新在于**将 DLM 水印重新定义为一个约束优化问题**，而非简单地在确定上下文上施加固定偏置。优化目标为：

$$q^* = \arg\max_{q \in \Delta(\Sigma)^L} \mathbb{E}_{\Omega \sim q}[\hat{\gamma}(\Omega)], \quad \text{subject to } \forall t \in [1,\dots,L], \mathbf{KL}(q_t, p_t(\tilde{\omega})) \leq \varepsilon$$

即**最大化生成序列的期望绿色 token 比例**，同时约束每个位置的水印分布与原始分布的 KL 散度。这一形式化将水印从“何时施加”的启发式规则提升为**全局优化**：算法可以利用整个序列的概率分布信息来决定哪些 token 应被增强。

### 方法解构：期望增强与预测偏置

该优化问题的解（Theorem 3.1）具有简洁的隐式形式：

$$q_t^* \propto p_t \exp(\delta_t \alpha_t(q^*))$$

其中 $\alpha_t(q) = \nabla_{q_t} J(q)$ 是能量函数 $J(q)$（期望绿色比例）对 token 分布 $q_t$ 的梯度。这一梯度自然分解为两个分量（以 SumHash、上下文 $\mathcal{C}=\{-1\}$ 为例）：

$$q_t^* \propto p_t \underbrace{\exp(\delta G^\top p_{t-1})}_{\text{期望增强}} \underbrace{\exp(\delta G p_{t+1})}_{\text{预测偏置}}$$

| 分量 | 机制 | 功能 |
|------|------|------|
| **期望增强**（Expectation Boost） | 在当前 token 的上下文哈希**概率分布**上施加 Red‑Green 偏置 | 即使上下文尚未确定，也能在期望意义上使当前 token 更可能成为绿色 |
| **预测偏置**（Predictive Bias） | 提升那些能使**后续 token** 更易成为绿色的 token 的概率 | 主动塑造未来上下文的哈希分布，使后续生成更有利于水印检测 |

消融实验（Fig. 4, top right）证实：两个分量**结合使用**比各自单独使用能获得更好的检测率-质量权衡，验证了优化框架的有效性。

### 关键 changed slots 总结

| 维度 | 基线方法 | 本文方法 |
|------|----------|----------|
| **水印施加条件** | 仅当上下文已确定时施加，否则不施加 | 为每个 token 计算上下文哈希的概率分布，在**期望上**施加水印 |
| **优化目标** | 按 de facto Red‑Green 规则对 logit 加固定偏移 $\delta$ | 构造约束优化问题，解为指数倾斜分布 $q_t^* \propto p_t \exp(\delta_t \alpha_t(q^*))$ |
| **检测器** | 基于上下文哈希计算 token 颜色 | **完全复用**现有 Red‑Green 检测器（二项式检验），无需修改 |

### 与 ARLM 水印的统一

值得注意的是，当限制到自回归生成场景时，本文的优化框架**精确退化为标准 Red‑Green ARLM 水印**（Sec. 3.3）。这表明本文方法并非另起炉灶，而是将 ARLM 水印从“确定性上下文”推广到“概率性上下文”的自然扩展，实现了两种生成范式下水印方案的统一。



![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_3aBWTYGcaT/figures/001_Figure_1.jpg]]
*Figure 1: An overview of why current watermarks for ARLMs fall short in the diffusion setting (left), how our watermark operates in this setting (middle) and how our watermark detector works (right)*

本文提出的DLM水印方法将扩散语言模型的水印问题形式化为一个**约束优化问题**，并从中导出可操作的生成与检测流程。整体pipeline由三个核心阶段构成：**哈希概率计算**、**能量梯度倾斜**与**标准Red‑Green检测**，其输入输出流与模块关系如下。

### 输入与输出

- **输入**：扩散语言模型在任意生成顺序下提供的逐位置概率分布 $p_t(\tilde{\omega})$，以及一个预定义的上下文窗口 $\mathcal{C}$（如前一token $\mathcal{C}=\{-1\}$ 或前后各一token $\mathcal{C}=\{-1,1\}$）。
- **输出**：经水印倾斜后的逐位置生成分布 $q_t^*$，从中采样得到的token序列 $\Omega$ 携带可被标准Red‑Green检测器识别的统计信号。
- **检测输入**：待检测的token序列 $\omega$ 与水印密钥 $\xi$；检测器对去重后的(token, context-hash)对进行绿色计数，执行二项式检验输出p值。

### 核心模块与数据流

**模块1：哈希概率分布计算（Hash Probability Computation）**

对于序列中的每个位置 $t$，给定当前DLM输出的各位置概率分布 $p$，计算上下文哈希的概率分布 $h_t(p)$。本文主要使用两种哈希方案：

- **SumHash**：$H_t^{\text{SumHash}}(\omega) = \sum_{i \in \mathcal{C}} \omega_{t+i}$，其概率分布为各上下文位置概率分布的卷积 $h_t^{\text{SumHash}}(p)_s = (p_{t+c_1} * \cdots * p_{t+c_k})_s$。
- **MinHash**：$H_t^{\text{MinHash}}(\omega) = \min_{i \in \mathcal{C}} \sigma(\omega_{t+i})$，通过累积乘积计算分布 $h_t^{\text{MinHash}}(p)_s = A_t(s+1) - A_t(s)$。

该模块的输出 $h_t(p)$ 是后续能量函数计算的基础，它将“上下文不确定”这一扩散生成的核心瓶颈转化为可处理的概率分布。

**模块2：能量函数与梯度倾斜（Energy Function & Tilting）**

水印的核心是一个约束优化问题：

$$q^* = \arg\max_{q \in \Delta(\Sigma)^L} \mathbb{E}_{\Omega \sim q}[\hat{\gamma}(\Omega)], \quad \text{s.t. } \forall t, \mathbf{KL}(q_t, p_t(\tilde{\omega})) \leq \varepsilon$$

其中期望绿色token比展开为能量函数 $J(q) = \sum_{t=1}^L h_t(q)^\top \cdot G \cdot q_t$。根据**Theorem 3.1**，该优化问题的隐式解为：

$$q_t^* \propto p_t \exp(\delta_t \alpha_t(q^*))$$

其中 $\alpha_t(q) = \nabla_{q_t} J(q)$ 是能量函数对第 $t$ 个位置分布的梯度。实际操作中，采用**固定点迭代**（fixed‑point iteration）求解：将当前分布 $q$ 按梯度方向进行指数倾斜，实践表明单次迭代即可获得足够好的解。梯度 $\alpha_t(q)$ 可分解为两个分量（详见Sec. 3.3）：

- **期望增强（expectation boost）**：在上下文哈希的期望分布上施加Red‑Green水印，即 $\sum_{h} G_{h,u} h_t(p)_h$。
- **预测偏置（predictive bias）**：提升那些能使其他位置token更易成为绿色的token的概率，即 $\sum_{s \neq t} \sum_{h} \mathbb{P}[H_s(\Omega)=h|\Omega_t=u] (G p_s)_h$。

以SumHash且 $\mathcal{C}=\{-1\}$ 为例，水印分布简化为：

$$q_t^* \propto p_t \exp(\delta G^\top p_{t-1}) \exp(\delta G p_{t+1})$$

其中第一项对应期望增强，第二项对应预测偏置。消融实验（Fig. 4 top right）证实，两个分量结合使用时，在固定文本质量下可获得显著优于单独使用任一分量的检测率。

**模块3：检测器（Detector）**

检测端**完全复用**标准Red‑Green ARLM水印的检测器，无需任何修改。给定待检测序列 $\omega$，对每个位置的(token, context-hash)对进行去重后，统计绿色token总数 $S = \sum_{i=1}^L G_{s_i, t_i}$，执行二项式检验得出p值。本文还针对相关绿色列表的情况引入了修正方差的Z‑score检测统计量（详见App. G）。

### 端到端流程总结

1. DLM输出各位置的概率分布 $p$。
2. 对每个位置 $t$，计算上下文哈希的概率分布 $h_t(p)$（模块1）。
3. 计算能量函数 $J(q)$ 对各位置的梯度 $\alpha_t(q)$（模块2）。
4. 按 $\delta$ 强度对logits进行指数倾斜，得到水印分布 $q_t^*$（模块2），从中采样生成token。
5. 检测时，对生成序列执行去重绿色计数与二项式检验（模块3）。

该pipeline的关键创新在于**将水印施加从“确定性上下文”推广到“上下文哈希的概率分布”**，从而解决了扩散语言模型因任意顺序生成导致上下文不完整、直接应用ARLM水印效果极弱的瓶颈问题。



### 优化框架

本文方法将扩散语言模型（DLM）的水印问题形式化为一个约束优化问题。设 $p(\tilde{\omega})$ 为 DLM 输出的因子化概率分布，$q(\tilde{\omega})$ 为施加水印后的分布。目标是最大化生成序列的期望绿色 token 比例，同时约束每步分布与原始分布的 KL 散度：

$$q^* = \arg\max_{q \in \Delta(\Sigma)^L} \mathbb{E}_{\Omega \sim q}[\hat{\gamma}(\Omega)], \text{ subject to } \forall t \in [1,\dots,L], \mathbf{KL}(q_t, p_t(\tilde{\omega})) \leq \varepsilon$$

其中 $\hat{\gamma}(\Omega)$ 为序列 $\Omega$ 中绿色 token 的比例，$L$ 为序列长度。

期望绿色比例可展开为哈希分布 $h_t$、绿色矩阵 $G$ 与 token 分布 $q_t$ 的内积之和：

$$\mathbb{E}_{\Omega \sim q}[\hat{\gamma}(\Omega)] = \frac{1}{L} \sum_{t=1}^L h_t(q)^\top \cdot G \cdot q_t =: \frac{1}{L} J(q)$$

这里 $J(q)$ 即为能量函数，$G \in \{0,1\}^{|\mathcal{H}| \times |\Sigma|}$ 表示每个哈希值对应的绿色 token 列表，$h_t(q)$ 为位置 $t$ 的上下文哈希概率分布。

该优化问题的隐式解由 **Theorem 3.1** 给出：

$$q_t^* \propto p_t \exp(\delta_t \alpha_t(q^*))$$

其中 $\alpha_t(q) = \nabla_{q_t} J(q)$ 为能量函数对 $q_t$ 的梯度，$\delta_t$ 为水印强度参数。在 logits 空间，最优解等价于向原始 logits 向量添加 $\delta_t \alpha_t(q^*)$ 的偏移量。

### 哈希概率计算模块

水印施加的核心前提是计算上下文哈希的概率分布。本文提出两种哈希方案：

**SumHash** 将上下文 token 的 id 求和作为哈希值：

$$H^{SumHash}_t(\omega) = \sum_{i \in \mathcal{C}} \omega_{t+i}$$

其哈希概率分布为各上下文位置概率分布的卷积：

$$h_t^{SumHash}(p)_s = (p_{t+c_1} * \cdots * p_{t+c_k})_s$$

其中 $\mathcal{C} = \{c_1, \dots, c_k\}$ 为上下文窗口。

**MinHash** 取上下文 token 经随机排列后的最小值：

$$H^{MinHash}_t(\omega) = \min_{i \in \mathcal{C}} \sigma(\omega_{t+i})$$

其概率分布通过累积乘积计算：

$$h_t^{MinHash}(p)_s = A_t(s+1) - A_t(s)$$

其中 $A_t(s) = \prod_{i \in \mathcal{C}} \sum_{v=0}^{s-1} p_{t+i}(\sigma^{-1}(v))$。

消融实验表明，SumHash 与 MinHash 对检测性能无显著影响（Fig. 4 左上）。

### 梯度分解：期望增强与预测偏置

以 SumHash 且上下文 $\mathcal{C} = \{-1\}$ 为例，能量函数简化为：

$$J(p) = \sum_{t=1}^{L} p_{t-1}^{\top} \cdot G \cdot p_t$$

此时水印分布可分解为两个分量：

$$q_t^* \propto p_t \exp(\delta G^\top p_{t-1}) \exp(\delta G p_{t+1})$$

更一般地，梯度 $\alpha_t(p)$ 可分解为：

$$\alpha_t(p)_u = \underbrace{\sum_{h \in \mathcal{H}} G_{h,u} h_t(p)_h}_{\text{期望增强}} + \underbrace{\sum_{s \neq t} \sum_{h \in \mathcal{H}} \mathbb{P}[H_s(\Omega)=h|\Omega_t=u] (G p_s)_h}_{\text{预测偏置}}$$

- **期望增强（Expectation Boost）**：在上下文哈希分布上施加 Red‑Green 水印的期望形式，即使上下文尚未确定，也能在期望意义上提升当前 token 的绿色概率。
- **预测偏置（Predictive Bias）**：提升能使其他位置 token 更易成为绿色的 token 概率，即若当前 token 取某值可使后续 token 的哈希更可能落入绿色列表，则提升该 token 的概率。

消融实验证实，两者结合使用比各自单独使用能获得更好的检测率-质量权衡（Fig. 4 右上）。

### 固定点迭代

由于 $q^*$ 的定义是隐式的（$q^* = f(q^*)$，其中 $f: q \mapsto p \exp(\delta \alpha(q)) / Z(q)$），本文采用固定点迭代求解。实际仅需单次迭代即可收敛，增加迭代次数仅带来边际检测率提升（Fig. 4 左下）。

### 检测器

检测端直接复用 Red‑Green ARLM 水印的检测器：给定文本 $\omega$，计算每个 token 的上下文哈希和颜色，对去重后的 $(hash, token)$ 对进行绿色计数，执行二项式检验：

$$S = \sum_{i=1}^L G_{s_i, t_i}$$

其中 $s_i$ 为位置 $i$ 的哈希值，$t_i$ 为 token id。由于本文使用独立同分布的绿色列表（而非原 Red‑Green 的相关列表），检测统计量 $S$ 在零假设下服从二项分布，可直接计算 $p$ 值。



## 实验与关键发现

### 核心发现：检测率-质量权衡

本文方法在扩散语言模型（DLM）水印任务上实现了显著优于朴素基线的检测率-质量权衡。表1汇总了推荐超参数下的主实验结果。在LLADA-8B上，当使用上下文窗口$C=\{-1\}$且水印强度$\delta=4$时，本文方法在1%假阳性率（FPR）下的真阳性率达**0.99**，而直接适配的Red-Green基线仅为0.63；在DREAM-7B上，相同条件下本文方法TPR@1为0.99，基线仅为0.49。扩大上下文至$C=\{-1,1\}$并相应提高$\delta$后，本文方法在两个模型上均保持0.99的TPR@1，基线则分别为0.83和0.67。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_3aBWTYGcaT/figures/004_Table_1.jpg]]
*Table 1: Detection Performance for Recommended Hyperparameters We compare the detectability of our watermark (TPR@1) for different contexts and the corresponding recommended strength parameter δ. The quality distortion (log PPL, GPT4 scores, and average benchmark accuracy) between the baseline and our approach is similar, and minimal compared to the unwatermarked model, yet our approach consistently reaches 99% TPR@1. Scores are averaged over 600 responses generated at temperature 0.5. The average response length for $\mathrm { L L A D A }$ – 8 $\mathrm { B }$ is 275 and 213 for DREAM-7B. Benchmark accuracies are measured at $\bar { T }$ = 0 . 1 , with accuracy for individual benchmark in Table 3

文本质量方面，以log PPL衡量，本文方法与基线在相同检测强度下的质量损失相近甚至略优。例如LLADA-8B上$C=\{-1\},\delta=4$时，本文方法log PPL为1.90，基线为1.93；GPT-4评分和基准准确率（MMLU、ARC-C、GPQA等六项平均）也表明质量影响与基线相当且相对无水印模型下降极小（表3）。这意味着本文方法在几乎不增加质量代价的前提下，将检测率从不可用水平（0.49-0.83）提升至实用水平（0.99）。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_3aBWTYGcaT/figures/036_Table_3.jpg]]
*Table 3: Extended Benchmark Accuracy We compare the benchmark accuracies between the unwatermarked model, the baselines, and our watermark for LLADA-8B and DREAM-7B. The last column shows the average accuracy, as reported in Table 1*

图2进一步揭示了检测效率的跃升。在$\delta=4$时，本文方法仅需约**50个token**即可达到基线约**350个token**才能实现的检测性能，即检测所需文本长度缩短约7倍。这一优势源于本文方法的核心机制——在上下文哈希的分布上以期望方式施加水印，而非等待上下文完全确定后才介入。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_3aBWTYGcaT/figures/003_Figure_2.jpg]]
*Figure 2: Detection Performance of Our Approach ( L e f t ) We compare the trade-off between watermark detectability (TPR@1) and text quality (log PPL) of our approach and the baseline for different values of the watermark strength parameter δ and sequences of, on average, 275 tokens. (Right) For $\delta$ = 4 . , we compare watermark detectability (TPR@1) between our approach and the baseline as a function of text length. Responses are generated by LLADA-8B with temperature 0.5 and 600 prompts from WATERBENCH. Crosses represent shared parameters between both figures*

### 鲁棒性评估

图3（左）展示了水印对局部修改的鲁棒性。在删除和替换攻击下，本文方法在高达**30%的序列被修改**时仍保持较强的检测能力（TPR@1 > 0.8），且显著优于Red-Green ARLM水印在相同条件下的表现。这一鲁棒性来自水印的“期望增强”机制：由于水印是在上下文哈希的概率分布上施加的，生成序列的多种可能变体也自然地携带水印信号。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_3aBWTYGcaT/figures/006_Figure_3.jpg]]
*Figure 3: Robustness Evaluation of Our Watermark ( L e f t ) We measure the detectability of our watermark (TPR@1) against an increasing percentage of local modifications, using responses generated from LLADA-8B with an average length of 275 tokens. ( R i g h t ) For stronger adversaries, we measure the detectability of our watermark (TPR@1) with respect to the length of the sequence. For both figures, we use $\delta$ = 4 and the previous token as context ( $\mathcal { C } = \{$ - 1 $\}$ ) )

对于更强的攻击者（图3右），本文方法的检测率随文本长度增加而单调提升，在约200 token后TPR@1接近饱和。这表明即使面对具有上下文感知能力的替换攻击，只要生成文本足够长，水印仍可被可靠检测。

### 消融研究

**期望增强与预测偏置的协同**：图4（右上）表明，单独使用期望增强（expectation boost）或预测偏置（predictive bias）均可获得一定的检测性能，但**两者结合**在给定log PPL下实现了最优的TPR@1。这验证了优化框架推导出的两个分量具有互补性——期望增强使当前token在期望意义上更可能为绿色，而预测偏置则提升能使后续token变绿的token概率。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_3aBWTYGcaT/figures/010_Figure_4.jpg]]
*Figure 4: Ablation of Our Watermark Components We compare the trade-off between watermark detectability (TPR@1) and text quality (log PPL) of our approach with various hyperparameters, namely the hashing scheme (Top Left), the two components introduced in Sec. 3.3 (Top Right), the number of fixed-point iterations (Bottom Left) and the ε/δ-parameterization explained in Sec. 3.2 (Bottom Right). Responses are generated by LLADA-8B with temperature 0.5 and 600 prompts*

**固定点迭代次数**：图4（左下）显示，增加固定点迭代次数仅带来边际检测率提升，**单次迭代**已足够接近最优解。这在实际部署中意味着计算开销可控。

**ε-参数化的失效**：图4（右下）揭示了一个重要失败模式——当使用KL散度约束（ε-参数化）替代直接的强度参数δ时，检测率大幅下降。论文明确指出，**KL散度在此场景下不是文本质量的理想代理**，这一发现限制了优化框架理论到实践的直接转化，也解释了为何实际方案采用δ-参数化。

**哈希方案与上下文选择**：SumHash与MinHash两种哈希方案在检测性能上无显著差异（图4左上，图24）。上下文集合的选择影响检测效率-质量权衡：$C=\{-1\}$（仅前一token）在低强度下已表现良好，而$C=\{-1,1\}$（前后各一token）在更高强度下可进一步提升检测率（图14）。

**其他超参数**：绿色列表比例$\gamma$越低，水印强度越弱但质量损失也越小，存在折衷（图12）。top-k近似从top-10以上获益甚微，**top-50为合理选择**（图11）。扩散步数越少，水印检测率越高（图9）。温度从0.3到0.7范围内，本文方法一致显著优于基线（图10）。

### 与顺序无关水印的对比

图5和表2将本文方法与**Unigram**（Zhao et al., 2023）和**PatternMark**（Chen et al., 2025）两类顺序无关水印进行了对比。在检测率-质量权衡上，本文方法在低失真区域（log PPL较低时）的TPR@1显著优于两者。更重要的是，表2揭示了Unigram的一个关键缺陷：其在不同密钥$\xi$下的FPR波动极大——在1%理论FPR下，最大经验FPR达17.0%，标准差1.2%。这意味着Unigram的实际假阳性率在不同密钥间可跨越多个数量级，严重威胁检测可靠性。相比之下，本文方法在使用$C=\{-1\}$时最大FPR@1%为1.7%、标准差0.3%；使用$C=\{-2,-1\}$时进一步降至1.1%和0.1%，**种子间波动随上下文尺寸增大而急剧减小**（图7）。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_3aBWTYGcaT/figures/012_Figure_5.jpg]]
*Figure 5: Detection Performance Comparison with Order-Agnostic Watermarks We study the trade-off between detectability (TPR@1) and text quality (log PPL) of our approach and orderagnostic watermarks for different values of the watermark strength parameter δ and sequences of, on average, 275 tokens. For the left figure, we use ${ \mathcal { C } } = \{$ - 1 $\}$ , and for the right one, we use $\mathcal { C } = \{$ - 1 , 1 $\}$ For the order-agnostic watermarks, we use the same data for both figures

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_3aBWTYGcaT/figures/018_Table_2.jpg]]

### 填充任务与自回归掩码策略

在DREAMON-V0-7B的填空（infilling）任务上，本文方法同样显著优于基线（图17），验证了方法对不同DLM生成范式的泛化性。消融还表明，无论使用熵掩码（entropy remasking）还是自回归掩码（autoregressive remasking）策略，本文方法的检测率-质量权衡均一致优于基线（图8）。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_3aBWTYGcaT/figures/039_Figure_17.jpg]]
*Figure 17: Detection Performance on Infilling Tasks (Left) We compare the trade-off between watermark detectability (TPR@1) and text quality (log PPL) of our approach and the baseline for different values of the watermark strength parameter δ and sequences of, on average, 205 tokens. (Right) ROC curves of our watermark and the baseline at log ${ \bf \bar { \it P P L } } ) \approx$ 1 . 9 4 . . Responses are generated with DREAMON-V0-7B at temperature 0.8, metrics are computed over 600 samples and we use the previous token as context ( $\mathrm { i . e . , \bar { \mathcal { C } } = \{ - 1 \} }$ ) . The crosses on the left figure correspond to the same watermark hyperparameters as the right figure

### 失败模式与局限性

1. **ε-参数化失效**：KL散度约束导致检测率大幅下降，说明理论框架中的KL散度并非文本质量的可靠代理，限制了约束优化形式的直接应用。
2. **短文本检测率低**：对于极短文本（<50 token），水印检测率较低，实际应用受限。
3. **自哈希方案的性能差异**：方法依赖无自哈希假设，当放宽至SelfHash方案时，性能与标准方案略有不同（图20）。
4. **鲁棒性评估范围有限**：仅覆盖删除、替换等局部修改，未涉及基于语言模型的重写、摘要等更复杂的对抗性攻击。
5. **模型泛化性未充分验证**：实验仅在LLADA-8B和DREAM-7B上进行，对其他DLM架构（如块扩散、半自回归模型）的泛化性尚不明确。
6. **文本质量评估依赖GPT-4**：作为裁判的GPT-4评分可能存在偏见，且未分析水印对生成多样性和事实一致性的影响。

### 补充图表

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_3aBWTYGcaT/figures/037_Table_4.jpg]]
*Table 4: Benchmark Accuracy with Entropy Remasking We compare the benchmark accuracy on LLADA-8B for our watermark using the recommended hyperparameters (achieving a TPR@1 of 1.0 with the entropy remasking strategy) to that of the unwatermarked model*

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_3aBWTYGcaT/figures/051_Figure_23.jpg]]
*Figure 23: Watermark Performance ROC curves (log scaled) of KGW and our watermark for both LLADA-8B (top) and DREAM-7B (bottom), and different values of δ using ${ \mathcal { C } } = \{$ - 1 $\}$ (left) or $\mathcal { C } = \{$ - 1 , 1 $\}$ (right)



## 定位与知识库关联

### 1. 方法继承与核心突破

本文方法直接继承自 **Red‑Green ARLM 水印**（Kirchenbauer et al., 2023）的检测框架——在生成时通过上下文哈希将词表划分为绿色/红色列表，检测时对绿色 token 计数执行二项式检验。二者的检测器完全兼容，本文明确声明“使用与 Red‑Green ARLM 水印相同的检测器”。

然而，核心瓶颈在于：ARLM 水印依赖已确定的上下文 token 进行哈希计算，而扩散语言模型（DLM）可任意顺序生成 token，导致上下文在生成时常常尚不完整。直接仅对已确定上下文的 token 施加 Red‑Green 水印（即 Naive ARLM Adaptation，本文的 Baseline）效果极弱——在 LLADA‑8B 上 TPR@1%FPR 仅 0.63–0.83，而本文方法可达 0.99（Table 1）。

本文的突破在于将 DLM 水印建模为**约束优化问题**：最大化生成序列的期望绿色 token 比例，同时约束每步分布与原始分布的 KL 散度。该优化问题的解自然导出两个分量：

- **期望增强（Expectation Boost）**：在上下文哈希的概率分布上施加 Red‑Green 水印，而非仅在已确定的上下文上。
- **预测偏置（Predictive Bias）**：提升能使其他位置 token 变绿的 token 概率，即“使后续 token 更易成为绿色”的偏置项。

当限制为自回归情形时，该优化框架精确退化为标准 Red‑Green ARLM 水印，表明本文方法是 ARLM 水印在扩散范式下的自然推广。

### 2. 与现有水印方法的关系

**与 ARLM 水印变体的对比：**

- **KGW**（Kirchenbauer et al., 2023）：本文的检测器完全兼容 KGW，但生成端从“确定性上下文哈希”扩展为“上下文哈希的概率分布上的期望操作”。
- **AAR**（Aaronson, 2023）：基于指数极小值采样的自适应水印，本文将其作为 DLM 适配的对比基线之一，实验表明本文方法在检测率-质量权衡上显著优于 AAR（Fig. 15）。
- **KTH**（Kuditipudi et al., 2024）：基于密钥排序的水印，同样被纳入对比，本文方法在相同质量下检测率更高。

**与顺序无关水印的对比：**

- **Unigram**（Zhao et al., 2023）：不依赖 token 顺序的水印方案。本文揭示了 Unigram 的关键缺陷——在不同密钥 ξ 下，FPR@1% 的波动跨越多个数量级，而本文方法的种子间波动随上下文尺寸增大而急剧减小（Fig. 7, Table 2）。同时，在低失真区域，本文方法以相似或更低的 log PPL 实现了更高的 TPR@1（Fig. 5）。
- **PatternMark**（Chen et al., 2025）：Unigram 的扩展，基于颜色模式。本文将其作为顺序无关水印的代表进行对比，结论与 Unigram 类似——本文方法在检测率-质量权衡上整体占优。

**与基于权重扰动的水印对比：**

- **GaussMark**：通过向模型权重添加高斯噪声嵌入水印。本文在跨模型对比中纳入 GaussMark，表明本文方法在相同质量下检测性能更优（Fig. 16）。

### 3. 方法的关键设计空间与消融洞见

**期望增强与预测偏置的协同：** 单独使用期望增强或预测偏置均不如二者结合（Fig. 4, top right），验证了优化框架导出的双分量结构的必要性。

**固定点迭代的边际收益：** 增加迭代次数仅带来微弱的检测率提升，单次迭代已足够（Fig. 4, bottom left），说明优化问题在实践中的收敛速度极快。

**ε‑参数化的失效：** 以 KL 散度为约束的 ε‑参数化导致检测率大幅下降（Fig. 4, bottom right），揭示 KL 散度在此场景下并非文本质量的理想代理——这是理论优雅性与实践有效性之间的重要张力。

**哈希方案的不敏感性：** SumHash 与 MinHash 对检测性能无显著影响（Fig. 4, top left），表明方法对哈希函数的具体选择具有鲁棒性。

**扩散步数的单调效应：** 扩散步数越少，水印检测率越高（Fig. 9），因为更少的重掩码步骤减少了水印信号的稀释。

### 4. 适用边界与局限

**已确认的有效范围：**

- **模型架构：** 在 LLADA‑8B 和 DREAM‑7B 两种扩散语言模型上验证，覆盖自回归重掩码和熵重掩码两种策略（Fig. 8）。
- **文本长度：** 约 50 token 即可达到基线约 350 token 的检测性能（Fig. 2, right），但极短文本（<50 token）的检测率仍较低。
- **生成温度：** 在 0.3–0.7 温度范围内一致显著优于基线（Fig. 10）。
- **鲁棒性：** 对局部修改（删除、替换）保持强检测能力，在 30% 的序列被修改时仍有效（Fig. 3, left）。

**已知局限与待验证边界：**

- **对抗性攻击：** 鲁棒性评估仅覆盖删除、替换等局部修改，未涉及基于语言模型的改写或摘要攻击。
- **模型泛化性：** 仅在两种 DLM 上验证，对块扩散、半自回归等其他 DLM 变体的泛化性尚不明确。
- **长文本趋势：** 检测性能随文本长度超过 300 token 后的变化趋势及极限未明确探索。
- **ε‑参数化的理论-实践鸿沟：** KL 散度约束在实践中失效的原因尚不清晰，是否存在更好的文本质量代理是开放问题。
- **自哈希假设：** 方法依赖无自哈希假设（token 不将自身作为上下文），虽然可放宽（SelfHash 方案），但性能与标准方案略有不同（Fig. 20）。
- **公平性与多样性：** 未专门分析水印对不同语言、领域或社会群体的差异化影响，也未评估对生成多样性和事实一致性的直接影响。

### 5. 开放问题

1. **质量代理的选择：** 为何 ε‑参数化（KL 散度约束）导致检测性能显著下降？是否存在比 KL 散度更适合约束文本质量的替代度量？
2. **极限检测能力：** 水印检测性能随文本长度增长是否存在理论上限？在更长上下文和更大词汇表下的可扩展性如何？
3. **分量解耦优化：** 期望增强与预测偏置两个分量是否能针对特定模型架构进行独立优化或进一步解耦？
4. **鲁棒性边界：** 对基于 LLM 的智能改写、摘要等更强的对抗性编辑，水印的鲁棒性边界在哪里？
5. **采样策略交互：** 不同采样策略（如 top‑p、典型采样）对水印强度的影响尚未系统研究。
6. **安全性分析：** 水印在扩散环境中的安全性（抵抗伪造、密钥泄露、移除攻击等）需要进一步研究。



## 原文 PDF

![[paperPDFs/ICLR_2026/Watermarking_Diffusion_Language_Models.pdf]]
