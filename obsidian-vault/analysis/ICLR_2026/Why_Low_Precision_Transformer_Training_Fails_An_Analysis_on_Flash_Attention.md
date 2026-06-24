---
title: "Why Low-Precision Transformer Training Fails: An Analysis on Flash Attention"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Why_Low_Precision_Transformer_Training_Fails_An_Analysis_on_Flash_Attention.pdf
openreview_forum_id: 0jHyEKHDyx
aliases:
- SFA
- WLPTTFAFA
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "通过调整softmax归一化因子m，使注意力概率P̄严格小于1，从而阻断有偏舍入误差的累积。"
primary_logic: "训练失败的根本原因不是随机的，而是两种相互交织的现象：1) 注意力机制中跨越不同训练步和token位置的相似低秩表示(R); 2) BF16加法在累积P̄V乘积时有偏的向负向舍入误差。这些舍入误差作为低秩表示的系数，导致梯度更新沿一致方向累积，增加权重谱范数和激活值，最终破坏训练动态。"
claims:
- "使用高精度FP32计算δ即可恢复训练稳定，证实低精度O是失败的直接原因。"
- "(PK)[T]^⊤ X[T]的外积在不同token和训练步间表现出强结构相似性，形成共同低秩方向R。"
- "累计和Σ(δ_lp - δ_hp)[T]在训练步骤中持续为正，表明误差沿R方向累积而不是抵消。"
- "当P̄[T,t]=1时，BF16加法引入负向舍入误差，且V[:,i]大多为负，导致Ō的计算系统性偏小。"
---

# Why Low-Precision Transformer Training Fails: An Analysis on Flash Attention

> [!tip] 核心洞察
> 训练失败的根本原因不是随机的，而是两种相互交织的现象：1) 注意力机制中跨越不同训练步和token位置的相似低秩表示(R); 2) BF16加法在累积P̄V乘积时有偏的向负向舍入误差。这些舍入误差作为低秩表示的系数，导致梯度更新沿一致方向累积，增加权重谱范数和激活值，最终破坏训练动态。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 低精度Transformer训练失败原因：Flash Attention分析研究 |
| 英文题名 | Why Low-Precision Transformer Training Fails: An Analysis on Flash Attention |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=0jHyEKHDyx); [GitHub](https://github.com/ucker/why-low-precision-training-fails) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Stabilized Flash Attention (检测并调整重复最大值缓解有偏舍入误差) |
| Dataset | GPT-2 Small (12 layers, 768 dim) pretraining on OpenWebText, GPT-2 Medium (GPT-2M) with AdamW |

> [!tip] 效果简介
> - GPT-2 Small (12 layers, 768 dim) pretraining on OpenWebText 上，Training Stability (Loss Explosion) 为 稳定收敛，无损失爆炸，对比 在数千步后损失突然爆炸，变化 防止失败，实现稳定训练。
> - GPT-2 Medium (GPT-2M) with AdamW 上，Validation Loss Convergence 为 正常收敛，对比 不收敛或爆炸，变化 稳定训练。

## 概述

低精度训练（如BF16）是提升Transformer效率的关键手段，但在结合Flash Attention时，GPT-2等模型的训练会突然出现损失爆炸。本文通过系统性的因果追踪，揭示了这一失败的根本原因并非随机数值噪声，而是两种相互交织的现象：**注意力机制中跨训练步和token位置涌现的相似低秩表示**，与**BF16加法在累积未归一化输出Ō时引入的有偏舍入误差**。这些舍入误差作为低秩表示的系数，导致梯度更新沿一致方向累积，持续增大权重谱范数和激活值，最终破坏训练动态。

核心发现可凝练为一个因果链条：低精度下Flash Attention计算未归一化输出 $\bar{\mathbf{O}} = \bar{\mathbf{P}}\mathbf{V}$ 时，当注意力概率 $\bar{\mathbf{P}}[T,t] = 1$ 且 $\mathbf{V}[:,i]$ 大多为负，BF16加法产生系统性负向舍入误差；该误差通过反向传播中的中间项 $\delta = \text{rowsum}(d\mathbf{O} \circ \mathbf{O})$ 放大，进而使查询投影权重 $\mathbf{W}^Q$ 的梯度更新产生有偏累积，最终导致损失爆炸。

基于此，本文提出**Stabilized Flash Attention**：检测softmax行内是否存在多个相同最大值，若存在则动态调整归一化因子 $m$，确保 $\bar{\mathbf{P}}$ 所有元素严格小于1，从而阻断有偏舍入误差的产生。实验表明，该方法在GPT-2 Small和Medium上均能防止损失爆炸，实现稳定收敛，且仅需对Flash Attention做最小化修改。

## 背景与动机

### 低精度训练的普及与隐忧

在大语言模型训练中，混合精度训练已成为降低显存占用和加速计算的标准方案。BF16（bfloat16）格式因其8位指数和7位尾数的设计，保留了与FP32相同的动态范围，在多数大规模模型上无需特殊调参即可达到与FP32相当的收敛效果。然而，这一看似稳健的方案在特定场景下暴露出隐蔽的不稳定性——社区报告显示，约10%的GPT-2预训练运行在纯BF16下会发生发散。

### Flash Attention的效率代价

Flash Attention（Dao et al., 2022）通过分块（tiling）和核融合策略，将注意力机制的内存复杂度从$O(N^2)$降至$O(N)$，使得长序列训练成为可能。其核心设计包括：前向传播中采用在线安全softmax，通过维护行最大值$m$和归一化因子$l$的运行时统计量，以分块方式累积未归一化输出$\bar{\mathbf{O}} = \bar{\mathbf{P}}\mathbf{V}$；反向传播中则实时重计算注意力分数，并利用关键中间项$\bar{\delta} = \text{rowsum}(d\mathbf{O} \circ \mathbf{O})$高效计算梯度。

然而，当Flash Attention与BF16精度结合时，一个致命的训练失败模式浮现：**损失在数千训练步后突然爆炸**。在GPT-2 Small（12层、12头、嵌入维度768、上下文长度1024）的标准配置下，使用AdamW优化器（$\beta_1=0.9$, $\beta_2=0.95$）、余弦学习率调度（峰值$1\times10^{-3}$）在OpenWebText上训练，BF16 Flash Attention的损失曲线在约6000步后急剧发散，而FP32配置则稳定收敛（图2）。

### 现有理解的缺口

此前的社区讨论将问题归因于数值精度不足，但缺乏对失败机制的深层理解。关键问题悬而未决：**为什么BF16下的Flash Attention会在特定时刻突然崩溃，而非逐渐退化？** 这种突发性暗示着某种累积效应，而非简单的随机噪声。理解这一因果链条，不仅对修复当前问题至关重要，更对推动更低精度（如FP8）训练具有指导意义。本文的目标正是追溯从根本原因到损失爆炸的完整因果链，并据此提出最小侵入性的修复方案。

## 核心创新

### 问题本质的重定义：从随机误差到有偏舍入

本工作的核心创新在于对低精度Flash Attention训练失败的根本原因进行了重新定义。不同于将数值不稳定简单归咎于“精度不足”或“随机舍入误差”的常见认知，本文通过逐层因果追踪揭示了一个更精确的失败机制：**训练失败并非源于随机误差的累积，而是由两种相互交织的现象共同驱动**——注意力机制中跨越不同训练步和token位置的相似低秩表示 $\mathbf{R}$，与BF16加法在累积 $\bar{\mathbf{P}}\mathbf{V}$ 乘积时产生的**有偏向负向舍入误差**。这些舍入误差作为低秩表示 $\mathbf{R}$ 的系数，导致梯度更新沿一致方向累积，持续增加权重谱范数和激活值，最终破坏训练动态。

这一洞察将问题从“精度不足”的模糊诊断，推进到可精确干预的因果环节。

### 关键因果链的定位：$\delta$ 误差与 $\bar{\mathbf{P}}\mathbf{V}$ 乘积

通过系统性的消融实验，本文精确定位了失败链条中的两个关键节点：

1. **$\delta = \mathrm{rowsum}(d\mathbf{O} \circ \mathbf{O})$ 的计算是误差传播的枢纽**。当使用替代公式 $\delta = \mathrm{rowsum}(d\mathbf{P} \circ \mathbf{P})$ 计算时，训练恢复稳定（Section 3.2），证明问题出在由低精度输出 $\mathbf{O}$ 计算 $\delta$ 的环节。

2. **未归一化输出 $\bar{\mathbf{O}} = \bar{\mathbf{P}}\mathbf{V}$ 的BF16累加是误差的根源**。仅将此矩阵乘积在FP32中计算即可稳定训练（Section 3.3.2），进一步将问题收敛到该单一操作。

### 核心修改：自适应归一化因子调整（Stabilized Flash Attention）

基于上述因果分析，本文提出的方法修改极为精简且具有精准的针对性——**仅修改softmax的归一化因子 $m$，在检测到特定条件时进行动态调整**，确保注意力概率 $\bar{\mathbf{P}}$ 的所有元素严格小于1，从而阻断有偏舍入误差的产生条件。

#### 修改的slot

| 组件 | 基线值（Classical Flash Attention, BF16） | 提出值（Stabilized Flash Attention） |
|------|------------------------------------------|--------------------------------------|
| **Softmax归一化因子 $m$** | 直接使用行最大值 $\mathbf{r}_m = \mathrm{rowmax}(\mathbf{S})$ 作为偏移量 | 当某行存在多个相同最大值时动态调整：若 $\mathbf{r}_m > 0$ 且重复，设 $m = \beta \cdot \mathbf{r}_m \, (\beta > 1)$；若 $\mathbf{r}_m < 0$ 且重复，设 $m = 0$ |

#### 设计逻辑

修改的触发条件严格限定于“行内存在多个相同最大值”这一特定数值场景。在该场景下，安全softmax的指数运算 $\exp(\mathbf{S} - m)$ 会产生值为1的元素（即 $\bar{\mathbf{P}}[T, t] = 1$），而BF16加法在此处引入有偏向负向的舍入误差（详见Figure 6分析）。通过将 $m$ 调整为略大于 $\mathbf{r}_m$ 的值（当 $\mathbf{r}_m > 0$ 时乘以 $\beta > 1$），或设为0（当 $\mathbf{r}_m < 0$ 时），保证 $\exp(\mathbf{S} - m')$ 的所有元素严格小于1，从根源上消除了产生有偏舍入误差的数值条件。

该修改的计算开销极小：仅需在在线softmax的每个内循环中增加一次重复最大值检测和条件赋值，不改变Flash Attention的分块计算框架和内存访问模式。

#### 与失败机制的精确对应

| 失败因果环节 | 方法的干预点 |
|-------------|-------------|
| 注意力分数矩阵 $\mathbf{S}$ 的某行存在多个相同最大值 | 检测重复最大值（$\mathbf{r}_s > 1$） |
| $\bar{\mathbf{P}}[T, t] = 1$ 导致BF16累加产生负向舍入误差 | 调整 $m$ 使 $\bar{\mathbf{P}}$ 所有元素 $< 1$ |
| 舍入误差作为低秩表示 $\mathbf{R}$ 的系数，导致梯度更新沿一致方向累积 | 阻断误差源，防止梯度偏差的累积 |

### 方法谱系与知识库定位

该方法属于**训练时数值稳定性修正**类别，与现有工作的关系如下：

- **Flash Attention** (Dao et al., 2022; Dao, 2024)：本工作的修改直接作用于Flash Attention的在线softmax模块，不改变其分块计算和IO感知的核心设计，可作为即插即用的补丁。
- **高精度回退策略**：与简单地将关键计算回退到FP32不同（如Section 3.2中验证的将 $\bar{\mathbf{O}}$ 或 $\mathbf{O}$ 在FP32计算），本方法在保持BF16计算的前提下解决问题，避免了精度提升带来的显存和速度开销。
- **QK归一化/截断、门控注意力**等稳定化技术：本方法针对的是注意力计算中一个此前未被识别的特定失败模式（重复最大值导致的 $\bar{\mathbf{P}}=1$ 场景），与上述技术解决的问题正交，理论上可结合使用。

### 证据强度与局限性

**强证据**：
- 消融实验链条完整且收敛：从禁用分块 → 定位到单层（Layer 2）→ 定位到单头（Head 8）→ 定位到 $\delta$ 计算 → 定位到 $\bar{\mathbf{P}}\mathbf{V}$ 乘积 → 定位到 $\bar{\mathbf{P}}[T, t]=1$ 时的舍入误差，每一步均有对照实验支撑（置信度 0.90–0.95）。
- 提出的修改在GPT-2 Small和GPT-2 Medium上均验证有效（Figure 7），防止了损失爆炸。

**需注意的局限**：
- 分析限于GPT-2架构和BF16精度，对LLaMA等架构及FP8等更低精度的推广性尚未验证。
- 仅在Flash Attention 2的特定失败案例下验证，可能未涵盖所有数值不稳定场景。
- 未探索不同GPU架构上舍入行为的差异。

## 整体框架

本研究采用“反向因果追踪”策略，从训练失败的最终表现（损失爆炸）逐步回溯，定位低精度Flash Attention中数值不稳定的根本原因，并据此提出最小化修复方案。整体分析流程如Figure 1所示，由表及里分为四个层次。

**问题复现与初步定位。** 首先在GPT-2 Small架构（12层，12头，嵌入维度768，序列长度1024）上使用BF16精度和Flash Attention对OpenWebText进行预训练，确认损失在数千步后突然爆炸的失败模式（Figure 2）。随后通过一系列消融实验缩小问题范围：禁用分块（将块大小设为序列长度）仍失败，证明分块非根因；仅在第2层使用Flash Attention即可复现失败，且该层权重谱范数出现异常尖峰（Figure 11），表明失败源自第2层；进一步锁定到注意力头8，其 $\mathbf{W}^Q$ 的谱范数最大（Figure 3）。

**中间变量溯源。** 在反向传播中，Flash Attention使用高效项 $\delta = \operatorname{rowsum}(d\mathbf{O} \circ \mathbf{O})$ 计算梯度。实验表明，用替代公式 $\delta = \operatorname{rowsum}(d\mathbf{P} \circ \mathbf{P})$ 或直接在FP32下重新计算 $\mathbf{O} = \mathbf{P}\mathbf{V}$ 均可恢复训练稳定，证明低精度 $\mathbf{O}$ 是失败的直接原因。进一步，仅对未归一化输出 $\bar{\mathbf{O}} = \bar{\mathbf{P}}\mathbf{V}$ 使用FP32计算即足以稳定训练，将问题精确锁定到该矩阵乘积。

**根因机制分析。** 失败由两种相互交织的现象驱动：其一，注意力机制中 $\mathbf{P}\mathbf{K}$ 与 $\mathbf{X}$ 的外积 $(\mathbf{P}\mathbf{K})[T]^\top \mathbf{X}[T]$ 在不同token位置和训练步间呈现强结构相似性，形成公共低秩方向 $\mathbf{R}$（Figure 4）；其二，BF16加法在累积 $\bar{\mathbf{P}}\mathbf{V}$ 时引入有偏的负向舍入误差。具体而言，当注意力概率 $\bar{\mathbf{P}}[T,t] = 1$ 且 $\mathbf{V}[:,i]$ 大多为负值时，BF16加法因舍入行为不对称（向上舍入的误差幅度大于向下舍入）导致 $\bar{\mathbf{O}}$ 系统性偏小（Figure 6），进而使 $\delta_{lp} - \delta_{hp}$ 持续为正（Figure 5a）。这些正偏误差作为低秩表示 $\mathbf{R}$ 的系数，通过梯度更新

$$d\mathbf{W}_{hp}^{Q} - d\mathbf{W}_{lp}^{Q} \approx \alpha \sum_{T=1}^{N} (\delta_{lp} - \delta_{hp})[T] \mathbf{R}$$

沿一致方向累积，增加权重谱范数和激活值，最终破坏训练动态。

**修复方案。** 基于上述根因，提出Stabilized Flash Attention：在安全softmax中检测行分数矩阵 $\mathbf{S}$ 是否存在多个相同最大值，若存在且行最大值 $r_m > 0$，则将归一化因子调整为 $m = \beta \cdot r_m$（$\beta > 1$），确保 $\bar{\mathbf{P}}$ 所有元素严格小于1，从而阻断有偏舍入误差的累积路径。该修复在GPT-2 Small和GPT-2 Medium上均成功消除损失爆炸（Figure 7）。

## 核心模块与公式推导

### 标准注意力与Flash Attention的数值计算

标准注意力机制定义为 $\mathbf{O} = \text{softmax}(\alpha \mathbf{Q} \mathbf{K}^\top) \mathbf{V}$，其中 $\alpha$ 为缩放因子。该计算需要显式构造 $N \times N$ 的注意力分数矩阵，内存复杂度为 $O(N^2)$。

Flash Attention通过分块策略将内存复杂度降至 $O(N)$。其前向传播采用在线安全softmax算法，维护两个运行统计量：行最大值 $\mathbf{m}$ 和归一化因子 $\mathbf{l}$。对于每个查询块 $\mathbf{Q}_i$，在遍历键值块的内循环中执行：

$$\bar{\mathbf{P}}_i^{(j)} = \exp(\mathbf{S}_i^{(j)} - \mathbf{m}_i^{(j)})$$

$$\bar{\mathbf{O}} = \bar{\mathbf{P}} \mathbf{V}, \quad \mathbf{O} = \bar{\mathbf{O}} / \text{rowsum}(\bar{\mathbf{P}})$$

其中 $\bar{\mathbf{P}}$ 为未归一化的注意力概率，$\bar{\mathbf{O}}$ 为未归一化输出，最终通过除以 $\bar{\mathbf{P}}$ 的行和得到归一化输出 $\mathbf{O}$。

反向传播中，Flash Attention 2采用一种高效计算方式，首先计算关键中间项：

$$\bar{\delta} = \text{rowsum}(d\mathbf{O} \circ \mathbf{O})$$

该中间项是连接前向输出与梯度计算的核心枢纽，也是本文分析训练失败的关键节点。随后，反向传播在运行时重新计算注意力分数以推导分数梯度。

### 梯度误差的数学分解

当使用低精度（BF16）计算输出 $\mathbf{O}_{lp}$ 时，由此导出的 $\delta_{lp}$ 与高精度参考值 $\delta_{hp}$ 之间产生偏差。该偏差通过反向传播链路逐级放大。

**查询梯度误差**。低精度与高精度查询梯度的差异可精确表达为：

$$d\mathbf{Q}_{hp} - d\mathbf{Q}_{lp} = \alpha \cdot \text{diag}(\delta_{lp} - \delta_{hp}) (\mathbf{P}\mathbf{K})$$

该式表明，查询梯度误差正比于 $\delta$ 的误差，并受矩阵 $\mathbf{P}\mathbf{K}$ 调制。$\mathbf{P}\mathbf{K}$ 在此充当了误差传播的方向性载体。

**权重投影梯度误差**。将上述误差进一步投射到查询投影矩阵 $\mathbf{W}^Q$ 的梯度上，得到总梯度误差的展开形式：

$$d\mathbf{W}_{hp}^{Q} - d\mathbf{W}_{lp}^{Q} = \alpha \sum_{T=1}^{N} (\delta_{lp} - \delta_{hp})[T] \cdot (\mathbf{P}\mathbf{K})[T]^{\top} \mathbf{X}[T]$$

该式将总梯度误差表示为 $N$ 个秩一矩阵的加权和，每个秩一矩阵由第 $T$ 个token位置的外积 $(\mathbf{P}\mathbf{K})[T]^{\top} \mathbf{X}[T]$ 构成，权重为对应位置的 $\delta$ 误差 $(\delta_{lp} - \delta_{hp})[T]$。

**低秩结构近似**。实验观察到，不同token位置和训练步之间的外积 $(\mathbf{P}\mathbf{K})[T]^{\top} \mathbf{X}[T]$ 表现出强烈的结构相似性（见Figure 4），可近似为共享的低秩方向 $\mathbf{R}$。因此梯度误差可简化为：

$$d\mathbf{W}_{hp}^{Q} - d\mathbf{W}_{lp}^{Q} \approx \alpha \sum_{T=1}^{N} (\delta_{lp} - \delta_{hp})[T] \mathbf{R}$$

这一近似揭示了失败的核心机制：当 $\delta$ 误差在多个训练步上保持一致的符号偏向（如持续为正），这些误差将作为共享低秩方向 $\mathbf{R}$ 的系数不断累积，驱动权重沿固定方向更新，最终导致权重谱范数膨胀和损失爆炸。

### 未归一化输出的舍入误差溯源

$\delta$ 误差的根源可追溯至前向传播中 $\bar{\mathbf{O}} = \bar{\mathbf{P}} \mathbf{V}$ 的BF16低精度计算。对于单个输出元素，低精度与高精度计算的差异为：

$$\bar{\mathbf{O}}_{lp}[T, i] - \bar{\mathbf{O}}_{hp}[T, i] = \left( \bar{\mathbf{P}}_{lp}[T, :] \mathbf{V}[:, i] \right)_{lp} - \left( \bar{\mathbf{P}}_{hp}[T, :] \mathbf{V}[:, i] \right)_{hp}$$

为定位误差在token序列中的累积过程，定义累积误差函数：

$$\bar{\mathbf{O}}_{\text{error}}(t) = \left( \sum_{t'=1}^{t} \bar{\mathbf{P}}[T, t'] \mathbf{V}[t', i] \right)_{lp} - \left( \sum_{t'=1}^{t} \bar{\mathbf{P}}[T, t'] \mathbf{V}[t', i] \right)_{hp}$$

该函数追踪随token位置 $t$ 递增时误差的演变轨迹。分析表明，当 $\bar{\mathbf{P}}[T, t] = 1$ 时（即注意力概率达到数值饱和），BF16加法引入有偏向的负向舍入误差。由于 $\mathbf{V}[:, i]$ 在问题特征维度上大多为负值，该负向舍入误差被进一步放大，导致 $\bar{\mathbf{O}}$ 系统性偏小，进而通过 $d\mathbf{O} \circ \mathbf{O}$ 的乘积使 $\delta$ 产生正向偏差。

### 稳定化方案的数学调整

所提出的稳定化方法直接干预softmax的归一化因子。标准安全softmax使用行最大值 $\mathbf{r}_m = \text{rowmax}(\mathbf{S})$ 作为偏移量，当某行存在多个相同最大值时，$\bar{\mathbf{P}}$ 中对应位置将精确等于1，触发上述有偏舍入误差。

稳定化方案检测这一条件并动态调整归一化因子。首先计算每行中接近最大值的元素计数：

$$\mathbf{r}_s = \text{rowsum}(\mathbf{r}_m - \mathbf{S} \leq \epsilon)$$

当 $\mathbf{r}_s > 1$（存在多个最大值）时，调整归一化因子：

$$\mathbf{m}' = \text{where}(\mathbf{r}_m > 0 \land \mathbf{r}_s > 1,\; \beta \cdot \mathbf{r}_m,\; \mathbf{r}_m), \quad \beta > 1$$

若 $\mathbf{r}_m > 0$ 且存在重复最大值，则设 $\mathbf{m}' = \beta \cdot \mathbf{r}_m$（$\beta > 1$），使 $\exp(\mathbf{S} - \mathbf{m}')$ 所有元素严格小于1；若 $\mathbf{r}_m \leq 0$，则设 $\mathbf{m}' = 0$。调整后的未归一化注意力概率为：

$$\bar{\mathbf{P}} = \exp(\mathbf{S} - \mathbf{m}')$$

该调整仅在检测到多重最大值的特定行上触发，对正常情况无影响，以最小代价阻断了有偏舍入误差的产生条件。

## 实验与分析

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_0jHyEKHDyx/figures/034_Figure_12.jpg]]
*Figure 12: Token difference visualization*

### 失败现象与复现条件

在BF16精度下使用Flash Attention训练GPT-2 Small（12层，12头，嵌入维度768，上下文长度1024）时，训练损失在数千步后发生突然爆炸（Figure 2）。实验在OpenWebText数据集上进行，使用AdamW优化器（β₁=0.9，β₂=0.95），余弦学习率调度（峰值1e-3，线性预热2000步），全局梯度裁剪1.0，在4块NVIDIA A100（80GB）GPU上以PyTorch DDP运行。为消除数据随机性干扰，所有实验使用记录并重复播放的相同数据批次序列。

### 失败定位：从系统到组件

通过一系列消融实验，研究将失败根源逐级定位到Flash Attention中一个特定的数值计算环节：

**分块策略排除。** 将块大小设为序列长度以禁用分块处理，训练仍然失败，证明分块（tiling）不是失败原因。

**单层定位。** 仅在第2层使用Flash Attention即可复现训练失败，而将该层替换为标准注意力则恢复稳定。Figure 11显示第2层注意力权重矩阵的谱范数出现异常尖峰，进一步确认失败源自此层。

**δ计算定位。** Flash Attention反向传播中高效计算中间项δ = rowsum(dO ∘ O)是关键瓶颈。使用替代公式δ = rowsum(dP ∘ P)计算δ可恢复训练稳定，证明问题出在通过O计算δ的路径上。

**低精度O确认。** 在反向传播中用FP32重新计算O（即PV乘积）使训练稳定，直接证实低精度BF16下的O是失败根源。

**异常注意力头识别。** 仅对特定注意力头（头1、7、8、9、11、12）使用高精度O即可恢复稳定，其中头8的权重矩阵W^Q具有最大谱范数（Figure 3），影响最为显著。

**未归一化输出定位。** 仅用FP32计算未归一化输出Ō = P̄V即可稳定训练，将问题进一步精确定位到该矩阵乘积的BF16累加过程。

### 根因分析：两种现象的相互作用

训练失败并非随机数值噪声所致，而是两种系统性现象的相互作用。

**现象一：低秩表示的涌现。** Figure 4展示了不同训练步和token位置下，(PK)[T]^⊤ X[T]外积矩阵在输入特征维度546和678上表现出强结构相似性。这意味着存在一个跨token和训练步的共同低秩方向R。查询投影矩阵W^Q的总梯度误差可近似为：

$$d\mathbf{W}_{hp}^{Q} - d\mathbf{W}_{lp}^{Q} \approx \alpha \sum_{T=1}^{N} (\delta_{lp} - \delta_{hp})[T] \mathbf{R}$$

其中(δ_lp - δ_hp)[T]作为低秩表示R的系数。若这些系数持续偏向同一方向，梯度更新将沿R一致累积，而非相互抵消。

**现象二：有偏舍入误差。** Figure 5(a)显示在训练步6580–6680期间，(δ_lp - δ_hp)[T]的累积和持续为正，证实误差沿R方向系统性累积。Figure 6进一步揭示该偏差的微观机制：在注意力概率P̄[T,t]恰好等于1的token位置，Ō的累积误差出现显著负向跳变（Figure 6(b)(c)）。这是因为BF16加法在累加P̄V乘积时，当累加的两个负数产生溢出需要右移舍入时，舍入操作引入一致偏差。同时，问题特征维度（如i=20）上V[:,i]值绝大多数为负（Figure 6(a)），使得P̄[T,t]=1时P̄[T,t]·V[t,i]为负，BF16加法的负向舍入导致Ō系统性偏小。

**因果链条总结：** 注意力机制中涌现的低秩表示R → BF16下Ō = P̄V累加时P̄=1位置引入有偏负向舍入误差 → δ = rowsum(dO ∘ O)产生正偏差 → 梯度更新沿R方向持续累积 → 权重谱范数和激活值增大 → 损失爆炸。

### 稳定化方案与验证

基于根因分析，提出**Stabilized Flash Attention**：检测softmax归一化中行最大值重复出现的情况，并动态调整归一化因子m，确保P̄所有元素严格小于1，从而阻断P̄=1时的有偏舍入误差。具体地，当某行存在多个相同最大值且r_m > 0时，设m' = β·r_m（β>1）；若r_m < 0且重复，设m' = 0。

Figure 7的验证损失曲线显示，该方案在GPT-2 Small和GPT-2 Medium上均消除了损失爆炸，实现稳定收敛，且与AdamW和Muon两种优化器兼容。

### 局限与待验证问题

当前分析主要限于GPT-2架构和BF16精度。以下问题需要进一步验证：该低秩结构和有偏舍入误差机制在LLaMA等不同架构中是否普遍存在；FP8等更低位宽下是否出现类似或新的不稳定性；所提稳定化技术与QK归一化、门控注意力等现有方法的兼容性；以及多重最大值现象能否作为训练失败的早期预警指标。

## 方法谱系与知识库定位

### 问题定位与基线关系

本工作针对低精度Transformer训练中一个具体的数值失效模式：BF16精度下Flash Attention导致的训练损失爆炸。该问题的直接基线是**Classical Flash Attention**（Dao et al., 2022; Dao, 2024）的BF16实现，其在GPT-2规模的训练中表现出数千步后损失突然发散，而**Standard Attention**的FP32实现则稳定收敛。这一失败案例已在社区中被多次报告（如nanoGPT的GitHub issue，见Figure 10），但此前缺乏系统性的因果分析。

本工作的核心贡献并非提出全新的注意力机制，而是通过逆向追踪因果链，揭示了失败的根本瓶颈：**未归一化输出 $\bar{\mathbf{O}} = \bar{\mathbf{P}}\mathbf{V}$ 在BF16下计算时引入的有偏舍入误差**，与注意力机制中涌现的相似低秩表示 $\mathbf{R}$ 相互作用，导致权重更新沿一致方向累积，最终破坏训练动态。

### 因果机制的独特发现

论文的分析建立了一条从现象到根源的完整因果链，其关键洞察在于失败**不是随机的数值噪声**，而是两种确定性现象的耦合：

1. **低秩结构涌现**：跨不同训练步和token位置的 $(\mathbf{P}\mathbf{K})[T]^\top \mathbf{X}[T]$ 外积表现出强结构相似性（Figure 4），形成公共低秩方向 $\mathbf{R}$。这使得梯度误差近似为 $\alpha \sum_T (\delta_{lp} - \delta_{hp})[T] \mathbf{R}$，即多个训练步的误差沿同一方向累积而非抵消。

2. **有偏舍入误差**：BF16加法在累积 $\bar{\mathbf{P}}\mathbf{V}$ 时，当注意力概率 $\bar{\mathbf{P}}[T,t]=1$ 且 $\mathbf{V}[:,i]$ 多为负值时，舍入操作产生系统性的负向偏差。这是因为小数值累积激活sticky bit，迫使后续BF16加法向上舍入，导致负向误差占主导（Section 3.3.2, Figure 6）。

这一分析框架将低精度训练失败从“经验性不稳定”提升为“可解释的因果机制”，为后续工作提供了可操作的诊断路径。

### 方法边界与适用条件

**Stabilized Flash Attention** 的修改极为轻量：仅在安全softmax中检测行内是否存在多个相同最大值，并在该条件下动态调整归一化因子 $\mathbf{m}$（若 $\mathbf{r}_m > 0$ 且重复，则 $\mathbf{m}' = \beta\mathbf{r}_m$，$\beta > 1$；若 $\mathbf{r}_m < 0$ 且重复，则 $\mathbf{m}' = 0$）。这确保了 $\bar{\mathbf{P}}$ 的所有元素严格小于1，从源头阻断有偏舍入误差的产生。

该方法的设计边界明确：
- **触发条件特定**：仅在注意力分数矩阵某行存在多个相同最大值时才介入，对正常情况无影响。Figure 13显示多重最大值频率与损失爆炸存在相关性，表明该条件在失败场景中确实频繁出现。
- **精度范围限定**：分析主要针对BF16精度，对FP8等更低位宽下是否出现类似的或新的失效模式尚未验证。
- **架构范围限定**：所有实验基于GPT-2架构（Small和Medium），对LLaMA等使用不同注意力变体（如GQA、RoPE）的架构推广性待检验。

### 已知局限与开放问题

**已确认的局限**：

1. **架构泛化性未验证**：分析限于GPT-2的12层/12头配置，且失败主要定位于第2层的少数注意力头（头1,7,8,9,11,12，其中头8影响最大）。对于更大规模模型（数十亿参数）或其他架构，低秩结构 $\mathbf{R}$ 和有偏舍入的耦合是否仍然成立，需要进一步检验。

2. **精度泛化性未探索**：BF16的舍入行为（round-to-nearest-even）是产生有偏误差的关键。FP8使用不同的指数/尾数分配和舍入策略，可能产生定性不同的误差模式。

3. **硬件依赖性未考虑**：不同GPU架构的融合乘加（FMA）实现和舍入行为可能存在差异，当前分析仅在NVIDIA A100上验证。

4. **与现有稳定化技术的交互未评估**：QK归一化（QK-Norm）、QK截断、门控注意力单元（GAU）等方法也旨在改善注意力训练的稳定性，本方法是否与这些技术兼容、能否叠加使用，尚待实验验证。

**开放问题**：

- 多重最大值现象能否在训练早期作为**预警指标**，用于预测即将发生的训练失败？Figure 13提示了这种可能性，但需要更系统的时序分析。
- 能否开发**自动检测工具**在训练期间监控 $\delta$ 误差的累积趋势，并在必要时动态切换精度或调整归一化因子？
- 在FP8训练中，是否会出现类似的“低秩结构 × 有偏舍入”耦合，还是会出现全新的数值失效模式？
- 所发现的低秩结构 $\mathbf{R}$ 是注意力机制训练动力学的固有属性，还是特定初始化/数据分布的产物？这关系到该问题是否会在更大规模训练中自发重现。

### 与相关工作的关系

本工作与低精度训练稳定性研究形成互补：不同于从优化器角度（如损失缩放、混合精度策略）或架构角度（如归一化位置调整）的缓解方案，本工作直接从**注意力计算的数值误差传播路径**入手，通过阻断误差源实现稳定。该方法修改量极小（仅涉及softmax归一化因子的条件调整），不改变模型容量或训练超参数，可作为现有Flash Attention实现的轻量级补丁。

## 原文 PDF

![[paperPDFs/ICLR_2026/Why_Low_Precision_Transformer_Training_Fails_An_Analysis_on_Flash_Attention.pdf]]
