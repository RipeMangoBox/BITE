---
title: "Soft-Masked Diffusion Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Soft_Masked_Diffusion_Language_Models.pdf
openreview_forum_id: Gba02UMvrG
aliases:
- SMS
- SMDLM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "引入一种新颖的**软掩码（Soft-Masking, SM）**机制：在保留掩码的位置，用先前预测的top-k个token的*加权嵌入*与原始[MASK]嵌入做一个*凸组合*，权重由可学习的置信度标定函数动态确定。这使得掩码状态可以传递连续、信息丰富的反馈，而不仅仅是二元状态。"
primary_logic: "将扩散语言模型的掩码反馈从硬二元决策松弛为基于置信度的软组合，能够以极小的额外参数和可并行的训练方式，显著保留并利用预测不确定性，从而在有限的解码步数下大幅提升文本生成和代码生成的质量。"
claims:
- "SM在无约束文本生成（OWT）中，相比于标准二元掩码，在相同计算预算下MAUVE提高0.568，生成困惑度降低25.83。"
- "SM仅需100k步的继续预训练即可融入预训练MDLM，验证困惑度从23.14降至21.63。"
- "将SM微调至Dream-7B仅需33.5k步，在HumanEval（1/4 NFE）上准确率从18.9%提升至25.6%。"
- "k=3在语言建模中效果最佳，k=1在代码生成中性价比最高，且所有k值均优于二元基线。"
---

# Soft-Masked Diffusion Language Models

> [!tip] 核心洞察
> 将扩散语言模型的掩码反馈从硬二元决策松弛为基于置信度的软组合，能够以极小的额外参数和可并行的训练方式，显著保留并利用预测不确定性，从而在有限的解码步数下大幅提升文本生成和代码生成的质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 软掩码扩散语言模型 |
| 英文题名 | Soft-Masked Diffusion Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Gba02UMvrG); [GitHub](https://github.com/IBM/soft-masked-diffusion-language-models) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Soft-masking (SM) |
| Dataset | OpenWebText unconstrained generation (L=1024), HumanEval (Dream-7B fine-tuned) |

> [!tip] 效果简介
> - OpenWebText unconstrained generation (L=1024) 上，MAUVE ↑ 为 0.596，对比 0.034，变化 +0.562。
> - OpenWebText unconstrained generation (L=1024) 上，Generative perplexity ↓ 为 24.63，对比 50.46，变化 ‑25.83。
> - OpenWebText unconstrained generation (L=1024) 上，MAUVE ↑ (ReMDM)  为 0.766，对比 0.411，变化 +0.355。

## 概述

掩码扩散语言模型（MDLMs）在迭代解码过程中存在一个关键瓶颈：对于每个被保留的掩码位置，模型只能执行二元决策——要么保持[MASK]嵌入，要么替换为预测的离散token。这种硬反馈机制丢弃了前序去噪步骤中产生的丰富分布信息，严重制约了低解码预算下的生成质量与多样性。

本文提出**软掩码（Soft-Masking, SM）**，将上述二元约束松弛为基于置信度的连续反馈。具体而言，对于仍处于掩码状态的token，SM用先前预测的top-k个token的加权嵌入与原始[MASK]嵌入进行凸组合，权重由一个仅含三个可学习参数的置信度标定函数动态确定。该机制使掩码状态能够传递连续、信息丰富的反馈信号，而非简单的二元状态。

**核心洞察**：将扩散语言模型的掩码反馈从硬二元决策松弛为基于置信度的软组合，能够以极小的额外参数和可并行的训练方式，显著保留并利用预测不确定性，从而在有限的解码步数下大幅提升文本生成和代码生成的质量。

在方法谱系中，SM处于**离散扩散语言模型的解码反馈增强**这一细分方向。与标准二元掩码MDLM（Sahoo et al., 2024）及更先进的ReMDM（Wang et al., 2025）等unmasking策略不同，SM并不改变“哪些token被解码”的调度，而是改变“被保留的掩码以何种表示形式反馈给下一轮去噪”。与同期工作CADD（Zheng et al., 2026）和CANDI（Pynadath et al., 2025）在扩散过程层面混合连续/离散状态不同，SM仅在解码反馈层面引入连续表示，保持了MDLM训练范式的简洁性。

**主要结果**：
- 在OpenWebText无约束文本生成中，SM在等计算预算下将MAUVE从0.034提升至0.596（+0.562），生成困惑度从50.46降至24.63（-25.83）；配合ReMDM时MAUVE进一步达到0.766（基线0.411，+0.355）。
- SM仅需100k步继续预训练即可融入预训练MDLM，验证困惑度从23.14降至21.63。
- 在Dream-7B上微调33.5k步后，HumanEval准确率从18.9%提升至25.6%（+6.7%），MBPP从26.6%提升至32.8%（+6.2%）。
- 消融实验表明，SM在去噪过程的前80%步骤中应用效果远优于后80%，top-k值取3在语言建模中效果最佳，取1在代码生成中性价比最高。

## 背景与动机

### 扩散语言模型的迭代解码瓶颈

掩码扩散语言模型（Masked Diffusion Language Models, MDLMs）通过逐步去噪生成文本，在可控生成与并行解码方面展现出潜力。其核心工作流程为：从完全掩码的序列出发，每一步由双向Transformer预测所有掩码位置的token分布，然后依据噪声调度或熵准则选择部分位置进行“去掩码”（unmasking），将预测token写入序列，其余位置保留`[MASK]`状态，形成下一轮迭代的输入。

然而，这一过程存在一个根本性的信息瓶颈：**对于每一步中保留`[MASK]`的位置，标准MDLM仅向其反馈一个二元状态——要么是`[MASK]`嵌入本身，要么是单个已解码token的独热向量**。这意味着上一轮去噪步骤中模型产出的完整概率分布（包含预测的不确定性、备选token的相对置信度等丰富信息）被完全丢弃。这种硬二元决策（hard binary decision）使得模型在后续去噪步骤中只能“盲人摸象”，严重限制了生成质量与多样性，尤其在解码步数受限的高吞吐场景下问题更为突出。

### 现有改进方案的局限

针对上述问题，已有若干工作尝试改进MDLM的反馈机制：

- **ReMDM**（Wang et al., 2025）通过优化去掩码策略（选择哪些位置解码）提升了效率，但并未改变掩码位置的反馈表示本身——被保留的`[MASK]`位置仍然接收二元信息。
- **dInfer**等方法通过提前终止解码来减少迭代次数，但本质上仍是围绕二元掩码状态的启发式加速，未能从根本上解决信息丢失问题。
- **CCDD**（混合连续-离散扩散）和**LDDMs**（潜在离散扩散）通过引入连续潜变量或拼接连续表示来丰富模型内部状态，但这些方法显著增加了序列长度或模型复杂度，且改变了扩散过程本身的数学形式。

### 本文动机：从硬掩码到软掩码

本文的核心洞察在于：**扩散语言模型的掩码反馈不应是“全有或全无”的二元决策，而应是一个能够传递预测不确定性的连续信号**。当一个位置尚未解码时，模型对其已有一定的“猜测”——可能是某个高置信度token，也可能是多个备选token的概率混合。将这些信息编码进掩码状态，而非粗暴地丢弃，应当能够显著改善后续去噪步骤的决策质量。

基于此，本文提出**软掩码（Soft-Masking, SM）**机制：对于每一步中保留的`[MASK]`位置，将其嵌入与上一轮预测的top-k个token的加权嵌入做凸组合，权重由模型对当前预测的置信度（以负熵度量）动态决定。这一设计仅引入三个可学习参数（缩放因子$\omega_s$、陡峭度$\omega_a$、偏移$\omega_b$），训练过程完全可并行，且不改变MDLM的扩散调度或模型架构，仅需在预训练或微调阶段以一定概率替换二元掩码为软掩码即可融入现有流程。

## 核心创新

### 1. 问题瓶颈：二元掩码的信息丢弃

掩码扩散语言模型（MDLMs）在迭代解码过程中，对每个保留的掩码位置执行二元决策：要么保持 `[MASK]` 嵌入，要么用上一步预测的单个离散token替换。这一硬性约束丢弃了模型在去噪过程中产生的**完整概率分布信息**——即模型对每个位置候选token的置信度与不确定性结构——从而限制了生成质量和多样性。

### 2. 方法核心：软掩码（Soft-Masking, SM）

软掩码机制将上述二元反馈松弛为一种**基于置信度的连续凸组合**。对于每一步仍被掩码的位置 $l$，其输入嵌入不再是非此即彼的 `[MASK]` 或离散token，而是：

$$
\mathbf{x}_{t-1}^{l} = \operatorname{sm}\big( \hat{\mathbf{x}}_{t-1}^{l}, \mathbf{p}_{t-1}^{l} \big) = 
\begin{cases} 
\big( 1 - \lambda( \mathbf{p} ) \big) \mathbf{m} + \lambda( \mathbf{p} ) \sum_{i \in \text{top-}k( \mathbf{p} )} \pi_i \mathbf{v}_i, & \hat{\mathbf{x}} = \mathbf{m} \\ 
\hat{\mathbf{x}}, & \text{otherwise} 
\end{cases}
$$

其中：
- $\mathbf{m}$ 为 `[MASK]` 嵌入，$\mathbf{v}_i$ 为词表中第 $i$ 个token的嵌入；
- $\pi_i$ 为归一化后的top-$k$ 概率向量；
- $\lambda(\mathbf{p}) \in [0, \omega_s)$ 为可学习的置信度权重。

对于已解码的token，SM保持其离散值不变，仅在掩码位置注入连续反馈。

### 3. 置信度标定：从熵到权重的可学习映射

SM的关键控制旋钮是 $\lambda(\mathbf{p})$，它决定软反馈的强度。该权重通过负熵（negative entropy）量化模型对当前预测的置信度，并经可学习的缩放sigmoid映射到 $[0, \omega_s]$ 区间：

$$
\lambda( \mathbf{p}_{t-1} ) = \omega_s \cdot \sigma\Big( \omega_a \big( -H( \mathbf{p}_{t-1}^{l} ) - \omega_b \big) \Big)
$$

三个可学习参数的含义：
- **$\omega_s$（缩放因子）**：控制软反馈的最大强度，训练中从接近0逐渐学习到接近1（Figure 3b）；
- **$\omega_a$（陡峭度）**：控制sigmoid的斜率，决定置信度变化对权重的敏感程度；
- **$\omega_b$（偏移量）**：设定置信度阈值，低于该值的低置信度预测将获得较小的 $\lambda$。

这一设计使模型能够**自适应地**调节软反馈强度：当模型对某位置预测高度确信（低熵）时，$\lambda$ 较大，软反馈更接近离散token嵌入；当模型不确定（高熵）时，$\lambda$ 较小，反馈更接近 `[MASK]`，保留更多探索空间。

### 4. Changed Slot：反馈表示的根本性改变

相对于基线MDLM（**Sahoo et al., 2024**），SM仅改变了一个核心组件——**掩码位置的反馈表示**：

| 组件 | 基线（Binary MDLM） | 本文（SM） |
|------|---------------------|------------|
| 掩码反馈 | 保持 `[MASK]` 嵌入 OR 替换为单个预测token的one-hot向量 | `[MASK]` 嵌入与top-$k$ 预测token嵌入的凸组合，权重由置信度标定 |
| 信息量 | 二元状态（掩码/解码） | 连续分布信息（top-$k$ 概率结构） |
| 额外参数 | 0 | 3个（$\omega_s, \omega_a, \omega_b$） |

这一改变使得去噪网络在每一步都能接收到**上一步预测的完整不确定性信息**，而非仅一个硬性决策。实验表明，SM在标准unmasking下将MAUVE从0.034提升至0.596（Table 1），生成困惑度从50.46降至24.63，且该增益在更先进的ReMDM（**Wang et al., 2025**）unmasking策略下依然显著（MAUVE +0.355）。

### 5. 设计要点与消融发现

- **$k=3$ 为语言建模最优**：top-$k$ 值增大到10或全词表（$k=|V|$）时性能下降，表明保留过多低概率token会引入噪声（Figure 5b, Table 10）；
- **$k=1$ 在代码生成中性价比最高**：在Dream-7B微调中，$k=1$ 即可在HumanEval上获得6.7个百分点的提升（Table 3），同时最小化计算开销；
- **SM在去噪早期阶段至关重要**：将SM步骤放在前80%的去噪步比放在后80%效果显著更好（Table 11），表明早期阶段的连续反馈对引导后续解码方向具有决定性作用；
- **训练概率 $p_{sm}=0.8$ 最优**：训练时以80%概率使用SM、20%概率使用二元掩码，可让模型同时适应两种反馈模式；设为1.0则完全丧失处理二元掩码的能力（Figure 5a）。

## 整体框架

Soft-masking (SM) 作为一种即插即用的反馈增强模块，被嵌入到掩码扩散语言模型（MDLM）的标准迭代去噪管线中。该框架的核心是一个双向 Transformer 主干网络 $g_\theta$，负责在每一步预测所有位置的 token 分布。SM 并不改变主干的架构或扩散调度，而是在**去噪步骤之间的反馈回路**上施加影响，将原本的二元硬掩码松弛为信息丰富的软掩码。

### 管线模块与数据流

整个生成过程从完全掩码的序列开始，通过 $T$ 步迭代去噪逐步解码。每一步的数据流如下：

1. **双向 Transformer 前向传播**  
   主干网络 $g_\theta$ 接收当前序列 $\mathbf{x}_t$（其中部分位置为 [MASK]，部分位置已解码为离散 token），输出所有位置的 logits。通过 softmax 得到概率分布 $\mathbf{p}_{t-1}$，并通过采样函数 $h(\cdot)$ 获得预测的原始 token $\hat{\mathbf{x}}_{t-1}$。反向过渡由参数化闭式给出：
   $$p_\theta(\mathbf{x}_s \mid \mathbf{x}_t) = \frac{\alpha_s - \alpha_t}{1 - \alpha_t} f_\theta(\mathbf{x}_t) + \frac{1 - \alpha_s}{1 - \alpha_t} \mathbf{m}$$
   其中 $f_\theta = h \circ g_\theta$。

2. **解掩码策略（Unmasking Strategy）**  
   解掩码函数根据噪声调度和/或熵准则，决定当前步哪些掩码位置应当被采样为离散 token、哪些位置继续保持掩码状态。论文实验了标准解掩码和更先进的 ReMDM（Wang et al., 2025）两种策略。

3. **软掩码反馈（Soft-Masking Function）**  
   这是 SM 的核心创新点。对于解掩码策略判定为**仍保持掩码**的位置，SM 函数 $\mathrm{sm}_\omega$ 执行以下操作：
   - 从该位置的概率分布 $\mathbf{p}_{t-1}^l$ 中提取 top-k 个候选 token，计算其归一化权重 $\pi_i$。
   - 通过置信度加权模块 $\lambda(\mathbf{p})$，将负熵映射为一个标量权重：
     $$\lambda(\mathbf{p}_{t-1}) = \omega_s \cdot \sigma\Big(\omega_a \big(-H(\mathbf{p}_{t-1}^l) - \omega_b\big)\Big)$$
     其中 $\omega_s$、$\omega_a$、$\omega_b$ 为三个可学习参数。
   - 将 [MASK] 嵌入与 top-k 候选 token 的加权嵌入做凸组合：
     $$\mathbf{x}_{t-1}^l = (1 - \lambda) \mathbf{m} + \lambda \sum_{i \in \text{top-}k(\mathbf{p})} \pi_i \mathbf{v}_i$$
     对于已解码的位置，直接保留其离散 token 值。

这一设计使得下一轮去噪步骤接收到的掩码位置不再是信息量为零的 [MASK] 嵌入，而是编码了模型当前预测分布及其置信度的连续向量，从而保留了前序步骤中的不确定性信息。

### 训练机制

SM 的训练采用**双前向传播（two-pass）** 流程（Algorithm 1）：
- **第一遍**：对当前序列 $\mathbf{x}_t$ 执行标准 MDLM 前向传播，获得预测分布 $\mathbf{p}_{t-1}$。
- **第二遍**：对 $\mathbf{x}_t$ 中随机采样的部分掩码位置应用 SM 函数，生成软掩码增强的序列 $\tilde{\mathbf{x}}_{t-1}$，再次前向传播并计算损失。

训练中引入超参数 $p_{sm}$ 控制每步应用 SM 的概率（默认 0.8），保留一定比例的二元掩码训练样本以确保模型兼容两种反馈模式。由于两次前向传播的计算开销，实验在 **iso-update**（匹配梯度更新次数）和 **iso-compute**（匹配总前向传播次数）两种预算下分别评估，后者保证了计算效率的对等比较。

### 模块关系总结

SM 的三个可学习参数 $(\omega_s, \omega_a, \omega_b)$ 是框架中**唯一额外引入的参数量**，可通过与主干网络并行的梯度反向传播高效学习。SM 与解掩码策略、扩散调度完全解耦，可独立应用于标准 MDLM 或 ReMDM 等更先进的变体，也可通过继续预训练或参数高效微调（DoRA）快速适配到预训练模型上。

## 核心模块与公式推导

### 3.1 软掩码反馈机制

掩码扩散语言模型（MDLM）在迭代解码时，对每个仍被掩码的位置执行二元决策：保留 `[MASK]` 嵌入，或用预测的离散 token 替换。这种硬二元反馈丢弃了前序去噪步骤中产生的丰富分布信息，成为限制生成质量与多样性的瓶颈。

软掩码（Soft‑Masking, SM）将这一反馈松弛为连续表示。对于第 $l$ 个位置，记上一步预测的概率分布为 $\mathbf{p}_{t-1}^l$，其对应的 top‑$k$ 归一化概率向量为 $\pi_i$，各 token 的嵌入为 $\mathbf{v}_i$。SM 的反馈定义为：

$$
\mathbf{x}_{t-1}^l = \mathrm{sm}\big( \hat{\mathbf{x}}_{t-1}^l, \mathbf{p}_{t-1}^l \big) = 
\begin{cases} 
\big( 1 - \lambda( \mathbf{p} ) \big) \mathbf{m} + \lambda( \mathbf{p} ) \sum_{i \in \mathrm{top-}k( \mathbf{p} ) } \pi_i \mathbf{v}_i, & \hat{\mathbf{x}} = \mathbf{m} \\[6pt]
\hat{\mathbf{x}}, & \text{otherwise}
\end{cases}
$$

其中 $\mathbf{m}$ 为 `[MASK]` 的嵌入向量。该公式的核心机制是：**对于仍被掩码的 token，用 top‑$k$ 预测 token 的加权嵌入与 mask 嵌入做凸组合；对于已解码 token，保留其离散值不变。**

### 3.2 置信度标定函数

组合权重 $\lambda(\mathbf{p})$ 由预测分布的置信度动态决定。置信度以负熵 $-H(\mathbf{p}_{t-1}^l)$ 量化，并通过可学习的缩放 sigmoid 映射到 $[0, \omega_s]$ 区间：

$$
\lambda( \mathbf{p}_{t-1} ) = \omega_s \cdot \sigma\Big( \omega_a \big( -H( \mathbf{p}_{t-1}^l ) - \omega_b \big) \Big)
$$

其中 $\sigma(\cdot)$ 为标准 sigmoid 函数。三个可学习参数的含义为：
- **$\omega_s$**：缩放因子，控制 SM 反馈的最大强度。实验表明，继续预训练过程中 $\omega_s$ 从接近零逐渐增长至接近 1（Figure 3b），说明模型学会了充分利用软掩码信息。
- **$\omega_a$**：陡峭度参数，调节置信度到权重的映射灵敏度。
- **$\omega_b$**：偏移参数，设定激活软反馈所需的最低置信度阈值。

### 3.3 训练流程

SM 的训练需要两次前向传播（two‑pass），如 Algorithm 1 所述：
1. **第一遍**：对当前掩码输入执行标准去噪，获得预测分布 $\mathbf{p}_{t-1}$。
2. **第二遍**：利用 $\mathbf{p}_{t-1}$ 构造软掩码反馈，再次输入模型计算损失。

这种设计使得 SM 仅引入三个额外参数（$\omega_s, \omega_a, \omega_b$），可与 MDLM 参数并行训练。在 iso‑compute 预算（匹配前向传播次数）下，SM 的计算效率与二元基线对等；在 iso‑update 预算（匹配梯度更新次数）下，SM 的墙钟时间加倍，但性能增益仍显著。

### 3.4 与现有方法的连接

当 $\lambda=1, k=1$ 时，SM 退化为将 argmax 预测 token 的嵌入反馈给掩码位置，与均匀扩散语言模型（uniform DLM）的反馈机制等价。这一退化情形揭示了 SM 的本质优势：通过 $k>1$ 和可学习的 $\lambda \in [0, \omega_s)$，SM 保留了预测分布中的不确定性信息，而非仅传递单点估计。消融实验表明，$k=3$ 在语言建模中效果最佳，$k=1$ 在代码生成中性价比最高，且所有 $k$ 值均优于二元基线（Table 10）。

## 实验与分析

### 核心瓶颈与因果机制验证

掩码扩散语言模型（MDLMs）的生成质量受限于其解码过程中的**硬二元反馈机制**：对每个仍保留掩码的位置，模型要么保留 `[MASK]` 嵌入，要么用单个预测token的独热向量替换，完全丢弃了前一步去噪产生的丰富分布信息。本文提出的**软掩码（Soft-Masking, SM）** 通过一个可学习的置信度标定函数，将 `[MASK]` 嵌入与先前预测的 top‑k 个token的加权嵌入做凸组合，使掩码状态能够传递连续的、信息丰富的反馈。这一松弛操作仅引入三个可学习参数（缩放因子 $\omega_s$、陡峭度 $\omega_a$、偏移 $\omega_b$），且训练过程可并行化。

实验设计围绕两个关键问题展开：（1）SM 能否在**等计算量（iso‑compute）** 和**等更新步数（iso‑update）** 两种预算下，一致地提升文本生成与代码生成的质量？（2）SM 的增益是否源于其保留了预测不确定性，而非简单的参数增加？

### 主实验结果

#### 无约束文本生成（OpenWebText）

在 OpenWebText 上从头训练 169M 参数的 MDLM，SM 在等计算量设定下展现出压倒性优势。**Table 1** 的核心数据如下：


![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Gba02UMvrG/figures/004_Table_1.jpg]]
*Table 1: Unconstrained generation after pretraining from scratch. We report MAUVE (↑) and generative perplexity (↓) of L = 1024 generated tokens using MDLM (Sahoo et al., 2024) with binary masking or our SM. Evaluations are tabulated by varying NFE budgets3. For unmasking, we use either the standard or the more recent ReMDM (Wang et al., 2025); the highest scores are bolded. Gain shows the performance improvement between the SM and the baseline MDLM. †Results of evaluating the ground-truth data and equal-backbone AR model are taken from (Sahoo et al., 2024)*

- **标准 unmasking + iso‑compute + NFE 1/1**：SM 的 MAUVE 达到 **0.596**，而二元掩码基线仅为 0.034，提升 **+0.562**；生成困惑度从 50.46 降至 **24.63**，降低 25.83。
- **ReMDM unmasking + iso‑compute + NFE 1/1**：SM 的 MAUVE 达到 **0.766**，较基线的 0.411 提升 **+0.355**；生成困惑度从 28.62 降至 **17.29**。

这一结果表明，SM 不仅适用于基础 unmasking 策略，与更先进的 **ReMDM**（Wang et al., 2025）结合时仍能带来大幅增益，且生成多样性（熵）与基线持平（Table 5/7），排除了“以多样性换质量”的假阳性。



![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Gba02UMvrG/figures/014_Table_7.jpg]]
*Table 7: Entropy (↑) with pretraining continuation. We perform unconstrained generation of L = 1024 tokens using MDLM (Sahoo et al., 2024) with binary masking or our SM. For unmasking, we use either standard or ReMDM (Wang et al., 2025)*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Gba02UMvrG/figures/012_Table_5.jpg]]
*Table 5: Generative perplexity (↓) and entropy (↑) with pretraining from scratch. We perform unconstrained generation of L = 1024 tokens using MDLM (Sahoo et al., 2024) with binary masking or our SM. Evaluations are tabulated by varying NFE budgets. For unmasking, we use either the standard or the more recent ReMDM (Wang et al., 2025); the highest scores are bolded. Gain shows the performance improvement between the SM and the baseline MDLM*

在等更新步数（iso‑update）设定下，SM 因训练需要两次前向传播（two‑pass），墙钟时间加倍，但仍在多数 NFE 预算下优于二元基线。**Figure 6** 显示 SM 的推理开销极小，在生成 1024 token 时累计时间与基线几乎重合。

#### 继续预训练的高效适配

SM 可以高效地融入预训练 MDLM：仅需 **100k 步** 的继续预训练，验证困惑度即从 23.14 降至 **21.63**（Figure 3a）。同时，模型自主学会将缩放因子 $\omega_s$ 从接近 0 提升至接近 1（Figure 3b），表明模型在训练过程中逐渐“信任”软掩码反馈，并充分利用其提供的信息。

**Table 2** 显示，继续预训练后的 SM 在等计算量下 MAUVE 达到 **0.578**（NFE 1/1），远高于二元基线的 0.034；即使在等更新步数下，SM 的 MAUVE 也达到 0.509，验证了其在实际部署场景中的鲁棒性。


![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Gba02UMvrG/figures/005_Table_2.jpg]]
*Table 2: MAUVE (↑) of unconstrained generation after pretraining continuation. Gain shows the performance improvement between the SM and the binary MDLM with pretraining continuation*

#### 代码生成（Dream‑7B / Dream‑Coder‑7B）

将 SM 微调至 Dream‑7B 仅需 **33.5k 步**（使用 DoRA 参数高效微调），在 HumanEval 和 MBPP 上取得显著提升（Table 3）：


![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Gba02UMvrG/figures/008_Table_3.jpg]]
*Table 3: Accuracy (%) on coding tasks. Evaluations are tabulated by varying NFE budgets. We finetune the models with 5 seeds and report the mean accuracy (± standard deviation). SM is configured with k=1. Gain shows the comparison between the SM model and the finetuned baseline. The best performing model is marked in bold. The learned SM parameters are given in Appendix C.10*

- **HumanEval + NFE 1/4**：SM 准确率 **25.6%**，二元基线 18.9%，提升 **+6.7%**。
- **MBPP + NFE 1/4**：SM 准确率 **32.8%**，二元基线 26.6%，提升 **+6.2%**。
- 在 HumanEval+ 和 MBPP+ 的扩展测试集上，SM 同样保持优势，最大增益达 **15.1%**。

值得注意的是，SM 在低 NFE 预算（高吞吐场景）下增益最为突出。**Figure 4** 将 SM 集成到 Fast‑dLLM 推理框架后，Dream‑Coder‑7B 在吞吐量‑性能曲线上全面优于二元反馈，验证了 SM 在高吞吐部署中的实用价值。

#### 数学推理（补充验证）

在 GSM8k 和 Math‑500 上微调 Dream‑7B（Table 8），SM（k=3）在多数 NFE 预算下优于二元基线，但增益幅度小于文本和代码任务。这暗示数学推理对软掩码提供的分布信息敏感度可能较低，或需要更大的 k 值与不同的置信度标定策略——该点需手动验证。


![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Gba02UMvrG/figures/019_Table_8.jpg]]
*Table 8: Accuracy (%) on math tasks. Evaluations are displayed under varying computational NFE budgets. We finetune the models with 5 seeds and report the mean accuracy (± standard deviation). SM is configured with k=3. Gain shows the comparison between the SM model and the finetuned baseline*

### 消融研究

#### SM 训练概率 $p_{\text{sm}}$

训练时以概率 $p_{\text{sm}}$ 应用 SM（否则使用二元掩码），Figure 5a 显示 $p_{\text{sm}}$ 从 0.5 增加到 0.8 能提升性能，但设为 1.0 会**损害生成质量**。原因是模型完全失去处理二元掩码的能力，在推理早期步骤（此时置信度低、SM 反馈噪声大）表现退化。这一发现揭示了 SM 训练中“适度暴露二元状态”的必要性。

#### Top‑k 值的选择

Figure 5b 和 Table 10 的系统消融表明：

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Gba02UMvrG/figures/021_Table_10.jpg]]
*Table 10: Comparison of different finetuned (FT) models, each trained with a different k value. The k = | $\nu$ | ablation is trained and evaluated with a learnable softmax temperature. Evaluations are performed on all three computational budgets and four math and coding evaluation tasks. The binary baselines are also included for comparison. We see that k = 1 , 3 and 5 perform best, with degrading performance at higher k values. The best performing model is highlighted in bold, and the second best is underlined*

- 语言建模中 **k=3** 达到最优，继续增大到 k=10 或全词表（k=|V|）性能反而下降。
- 代码生成中 **k=1** 性价比最高，k=3 和 k=5 次之。
- 全词表消融（k=|V|）配合可学习 softmax 温度后性能仍不及 k=3，说明**稀疏的 top‑k 反馈已足够捕获关键分布信息**，过大的 k 引入噪声。

#### SM 应用时机的关键性

**Table 11** 的消融直接验证了 SM 的核心价值在于早期去噪阶段：
- **SM→Binary**（前 80% 步骤用 SM，后 20% 用二元掩码）：性能大幅优于二元基线。
- **Binary→SM**（前 20% 用二元，后 80% 用 SM）：增益显著缩小。

这一结论与直觉一致：早期步骤中模型不确定性高，软掩码提供的连续分布信息对全局结构规划至关重要；后期步骤中 token 已大部分解码，二元反馈的精度已足够。

Table 12 进一步探索了时间依赖的 SM→Binary 切换策略（线性衰减、阶梯衰减），所有变体均优于纯二元基线，但简单的固定比例切换已接近最优。

#### 与同期工作的对比

**Figure 9** 将 SM 与同期方法 **CANDI**（Pynadath et al., 2025）和 **CADD**（Zheng et al., 2026）在生成困惑度‑熵权衡曲线上进行比较：SM 在所有 NFE 预算下均位于更优的 Pareto 前沿，即在保持更高多样性的同时实现更低困惑度。Table 13 的定量对比进一步确认了 SM 的领先地位。

### 失败模式与局限

1. **等更新步数下的墙钟时间加倍**：SM 训练需要两次前向传播，在 iso‑update 预算下实际训练时间约为二元基线的两倍。虽然等计算量设定下公平可比，但在计算资源严格受限的场景中需权衡。

2. **极端高吞吐场景的微小延迟**：尽管 Figure 6 显示推理开销极小，但 top‑k 嵌入的实时计算在极致吞吐（如批量服务数千请求）时可能成为瓶颈。代码生成中采用 k=1 正是为了最小化这一开销。

3. **大规模模型验证缺失**：本文实验上限为 7B 参数，SM 在更大模型（>70B）和更复杂推理任务（如长链 CoT）上的有效性尚待验证。数学推理任务上的增益相对温和（Table 8），暗示 SM 的收益可能随任务类型和模型规模变化。

4. **扩散调度未联合优化**：SM 的可学习参数仅在掩码反馈层面引入，未尝试与扩散噪声调度联合优化，可能存在未开发的潜力。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Table 1 | SM 在等计算量下 MAUVE 提升最高 +0.562，生成困惑度降低 25.83 |
| Figure 3 | 100k 步继续预训练即可显著降低验证困惑度，模型自主学会利用 SM |
| Table 3 | 代码生成低 NFE 预算下准确率提升 6–7 个百分点，最高增益 15.1% |
| Figure 4 | SM 与 Fast‑dLLM 集成后在高吞吐场景全面优于二元反馈 |
| Figure 5 | $p_{\text{sm}}=0.8$、k=3 为语言建模最优配置；$p_{\text{sm}}=1.0$ 有害 |
| Table 11 | SM 必须应用于去噪早期阶段（前 80%），后期切换为二元即可 |
| Figure 9 | SM 在生成困惑度‑熵权衡上优于同期方法 CANDI 和 CADD |

### 补充图表

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Gba02UMvrG/figures/002_Figure_1.jpg]]
*Figure 1: Illustrative answer generation using masked diffusion language models (MDLMs) via iterative decoding with (a) standard binary masking or (b) our proposed soft-masking. Our softmasking enriches the feedback for the next decoding step by superposing the masked tokens with the previously predicted top-k candidates, enabling more accurate and faster generation*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Gba02UMvrG/figures/011_Table_4.jpg]]
*Table 4: Validation perplexity on OWT. †Results for AR and SEDD were taken from (Sahoo et al., 2025)*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Gba02UMvrG/figures/013_Table_6.jpg]]
*Table 6: Generative perplexity (↓) with pretraining continuation. We perform unconstrained generation of L = 1 0 2 4 tokens using MDLM (Sahoo et al., 2024) with binary masking or our SM. For unmasking, we use either standard or ReMDM (Wang et al., 2025); the highest scores are bolded. Gain shows the performance improvement between the SM and the binary MDLM with pretraining continuation*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Gba02UMvrG/figures/018_Figure_7.jpg]]
*Figure 7: Unconstrained generation trajectory of L = 8 tokens over T = 8 steps using an MDLM with Soft-Masking (trained from scratch, iso-compute, 500k steps). Green-shaded cells indicate masked tokens where SM is active; color intensity corresponds to the SM confidence, with darker green indicating higher certainty. The text inside these cells displays the current top-1 predicted token. Bold, unshaded text represents tokens that have been unmasked (sampled) and fixed*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Gba02UMvrG/figures/020_Table_9.jpg]]
*Table 9: Accuracy (%) on coding tasks. SM has been finetuned in the iso-compute training setting. Evaluations are tabulated by varying NFE budgets. We finetune the models with 5 seeds and report the mean accuracy (± standard deviation). SM is configured with k=1. Gain shows the comparison between the SM model and the finetuned baseline. The best performing model is marked in bold*


## 方法谱系与知识库定位

### 1. 问题定位与核心瓶颈

掩码扩散语言模型（Masked Diffusion Language Models, MDLMs）作为一类非自回归生成模型，通过迭代去掩码过程生成文本。其核心工作流为：从全掩码序列出发，每步由双向Transformer预测各位置token分布，然后根据unmasking策略将部分[MASK]替换为预测token，其余位置保留[MASK]进入下一轮。然而，这一范式存在一个关键的**信息瓶颈**：对于每步中仍被保留为[MASK]的位置，模型仅传递一个二元的“掩码/非掩码”状态，完全丢弃了上一步预测出的完整概率分布信息。

具体而言，在标准二元掩码机制下，位置 $l$ 在步 $t-1$ 的反馈 $x_{t-1}^l$ 要么是离散的预测token，要么是[MASK]嵌入。这意味着模型在后续去噪步中无法感知该位置的预测不确定性——无论模型对该位置是高度确信（熵低）还是高度困惑（熵高），反馈信号完全相同。这一信息损失在解码步数受限（低NFE预算）时尤为致命，因为模型缺乏足够的迭代机会来纠正早期错误。

### 2. 方法谱系：从二元掩码到软掩码

#### 2.1 基线方法：MDLM与二元掩码

**MDLM**（Sahoo et al., 2024）建立了掩码扩散语言模型的标准范式。其前向过程将token以概率 $1-\alpha_t$ 吸收到[MASK]状态，逆向过程通过参数化后验分布 $p_\theta(x_s|x_t)$ 逐步恢复原始token：

$$p_\theta(x_s|x_t) = \frac{\alpha_s - \alpha_t}{1 - \alpha_t} f_\theta(x_t) + \frac{1 - \alpha_s}{1 - \alpha_t} \mathbf{m}$$

其中 $f_\theta = h \circ g_\theta$ 是双向Transformer $g_\theta$ 与采样函数 $h$ 的组合。训练目标为负对数似然的上界：

$$\mathcal{L}(\theta) = -\mathbb{E}_{t \sim U(0,1), x_0 \sim q_{data}, x_t \sim q(\cdot|x_0)} \left[\frac{1}{1-\alpha_t} \log p_\theta(x_0|x_t)\right]$$

在解码阶段，模型采用**标准unmasking**（按噪声调度选择要解码的位置）或**ReMDM**（Wang et al., 2025）等更先进的策略。ReMDM通过熵感知的调度改进了位置选择，但其反馈机制仍停留在二元层面——保留的掩码位置仅接收[MASK]嵌入。

#### 2.2 本文方法：Soft-Masking（SM）

**Soft-Masking（SM）** 的核心创新在于将掩码反馈从**二元硬决策**松弛为**基于置信度的软组合**。对于每步中仍被保留为[MASK]的位置 $l$，SM执行如下操作：

$$\mathbf{x}_{t-1}^l = \text{sm}(\hat{\mathbf{x}}_{t-1}^l, \mathbf{p}_{t-1}^l) = \begin{cases} (1 - \lambda(\mathbf{p})) \mathbf{m} + \lambda(\mathbf{p}) \sum_{i \in \text{top-}k(\mathbf{p})} \pi_i \mathbf{v}_i, & \hat{\mathbf{x}} = \mathbf{m} \\ \hat{\mathbf{x}}, & \text{otherwise} \end{cases}$$

其中 $\pi_i$ 是top-k预测概率的归一化版本，$\mathbf{v}_i$ 是对应token的嵌入向量。置信度权重 $\lambda(\mathbf{p})$ 通过可学习的缩放sigmoid函数从负熵映射得到：

$$\lambda(\mathbf{p}_{t-1}) = \omega_s \cdot \sigma\Big(\omega_a \big(-H(\mathbf{p}_{t-1}^l) - \omega_b\big)\Big)$$

这一设计具有三个关键特性：
1. **信息保留**：高置信度位置（低熵）的反馈接近纯预测token嵌入，低置信度位置（高熵）则保留更多[MASK]成分，使模型能感知不确定性。
2. **极简参数化**：仅引入 $\omega_s, \omega_a, \omega_b$ 三个可学习参数，训练时通过两轮前向传播（two-pass）即可并行优化。
3. **即插即用**：SM作为反馈层的替换，可与任意unmasking策略（标准、ReMDM）和任意预训练MDLM组合。

#### 2.3 与相关工作的关系

| 方法 | 反馈机制 | 关键差异 |
|------|---------|---------|
| **MDLM** (Sahoo et al., 2024) | 二元掩码 | 丢弃分布信息 |
| **ReMDM** (Wang et al., 2025) | 二元掩码 + 熵感知调度 | 改进unmasking位置选择，但反馈仍为二元 |
| **CANDI** (Pynadath et al., 2025) | 连续松弛 | 并行工作，采用不同的连续化策略 |
| **CADD** (Zheng et al., 2026) | 置信度感知解码 | 并行工作，在解码策略层面引入置信度 |
| **SM（本文）** | 基于置信度的软组合 | 在**反馈嵌入层面**引入连续信息，与unmasking策略解耦 |

SM与CANDI、CADD等并行工作的本质区别在于：SM在反馈表示层面操作，而非在解码调度或采样策略层面。这使得SM可与这些方法互补——例如，SM+ReMDM的组合在Table 1中展现了叠加增益（MAUVE从0.411提升至0.766）。

### 3. 适用边界与实验验证

#### 3.1 已验证的有效场景

- **无约束文本生成**（OpenWebText, 169M参数）：SM在iso-compute预算下将MAUVE从0.034提升至0.596（+0.562），生成困惑度从50.46降至24.63（-25.83）（Table 1）。
- **代码生成**（Dream-7B / Dream-Coder-7B, HumanEval/MBPP）：微调33.5k步后，HumanEval准确率从18.9%提升至25.6%（+6.7%），MBPP从26.6%提升至32.8%（+6.2%）（Table 3）。
- **继续预训练**：仅需100k步即可将预训练MDLM的验证困惑度从23.14降至21.63（Figure 3a）。
- **高吞吐场景**：与Fast-dLLM集成后，SM在低NFE预算下优势尤为显著（Figure 4）。

#### 3.2 关键消融发现

- **top-k选择**：语言建模中k=3最优，代码生成中k=1性价比最高；过大的k值（如k=|V|）反而损害性能（Figure 5b, Table 10）。
- **SM训练概率**：$p_{sm}=0.8$ 优于0.5，但设为1.0会因模型丧失处理二元掩码的能力而降低质量（Figure 5a）。
- **SM作用阶段**：将SM应用于去噪过程的前80%步远比应用于后80%步有效，表明SM在早期去噪阶段至关重要（Table 11）。
- **策略兼容性**：SM与ReMDM组合产生叠加增益（MAUVE +0.355），且生成多样性（熵）与基线持平（Table 5/7）。

### 4. 局限性与开放问题

#### 4.1 已知局限

1. **训练开销**：SM训练需要两次前向传播（two-pass），在iso-update预算下墙钟时间加倍；仅在iso-compute设定下可实现公平比较。
2. **实时计算开销**：top-k嵌入的实时计算在极端吞吐场景下可能引入微小延迟（Figure 6）。
3. **规模验证不足**：未在超过7B参数的模型或更大规模数学推理数据集（如MATH-all）上验证。
4. **调度耦合未探索**：SM仅在反馈层面引入改进，未与扩散调度（如噪声schedule）联合优化。

#### 4.2 开放问题

- **与RLHF的整合**：SM的连续反馈能否与强化学习（如RLHF）结合，进一步优化生成多样性或事实一致性？
- **大规模模型验证**：SM在>70B模型和长链推理（如Chain-of-Thought）中是否依然有效，尤其是在无时间条件编码的模型中？
- **训练效率优化**：是否存在闭式训练方法，避免two-pass带来的额外前向开销？
- **反馈压缩**：SM的连续反馈能否被压缩为更紧凑的表示（如低秩潜变量），以减少对top-k嵌入的计算依赖？
- **扩散类型泛化**：SM对不同扩散模型（均匀扩散、混合扩散）的适应性极限在哪里？
- **安全合规**：SM带来的多样性提升是否可能引入更多不安全输出？如何有效控制？

---

**证据强度说明**：上述核心结论均有Table 1/3/5/7/10/11及Figure 3/5的量化数据支撑，置信度≥0.95。规模局限性和开放问题来自论文自身的讨论与未覆盖的实验设置，需后续工作验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Soft_Masked_Diffusion_Language_Models.pdf]]
