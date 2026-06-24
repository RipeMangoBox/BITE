---
title: "In-Place Test-Time Training"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/In_Place_Test_Time_Training.pdf
openreview_forum_id: dTWfCLSoyl
aliases:
- PTTTPT
- PTTT
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "将MLP块中的最终投影矩阵(W_down)作为快速权重，在推理时通过in-place更新使其能够动态编码上下文信息，而不改变模型架构。"
primary_logic: "复用现有的MLP组件作为快速权重存储器，结合与Next-Token Prediction对齐的学习目标和高效的chunk-wise并行更新策略，可以在不牺牲效率的前提下赋予LLM测试时训练能力。"
claims:
- "In-Place TTT在Qwen3-4B-Base上将RULER基准128k长度下的准确率从74.8%提升至77.0%，并保持到256k的外推能力。"
- "理论分析证明LM对齐的目标能够在期望上增加正确token的logit，而重建目标不能。"
- "消融实验确认chunk size 512和1024性能最佳，且Conv1D和W_target都是必要的。"
- "RULER (Qwen3-4B-Base) 上 Average Accuracy (%) = 77.0 (128k)"
---

# In-Place Test-Time Training

> [!tip] 核心洞察
> 复用现有的MLP组件作为快速权重存储器，结合与Next-Token Prediction对齐的学习目标和高效的chunk-wise并行更新策略，可以在不牺牲效率的前提下赋予LLM测试时训练能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 原位测试时训练 |
| 英文题名 | In-Place Test-Time Training |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=dTWfCLSoyl) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | In-Place Test-Time Training (In-Place TTT) |
| Dataset | RULER (Qwen3-4B-Base), RULER (LLaMA-3.1-8B), RULER (Qwen3-14B-Base), RULER-16k (4B Full Attention) |

> [!tip] 效果简介
> - RULER (Qwen3-4B-Base) 上，Average Accuracy (%) 为 77.0 (128k)，对比 74.8 (128k)，变化 +2.2。
> - RULER (LLaMA-3.1-8B) 上，Average Accuracy (%) 为 83.7 (64k)，对比 81.6 (64k)，变化 +2.1。
> - RULER (Qwen3-14B-Base) 上，Average Accuracy (%) 为 70.6 (64k)，对比 67.9 (64k)，变化 +2.7。

## 概述

**核心问题**：大语言模型在推理时参数完全冻结，无法动态适应持续变化的上下文。这一静态性在长序列推理、在线学习和非平稳信息流中构成根本瓶颈——模型不能将新信息编码为参数化记忆，只能依赖有限的上下文窗口。

**核心洞见**：与其引入额外的快速权重模块，不如复用Transformer中已有的MLP块。具体而言，将门控MLP的最终投影矩阵 $\mathbf{W}_{\mathrm{down}}$ 作为快速权重，在推理时通过原位（in-place）更新使其动态编码上下文信息。这一设计无需改变模型架构，实现了真正的即插即用。

**方法定位**：In-Place TTT 属于测试时训练（Test-Time Training）方法族，但区别于现有工作之处在于三点：
- **架构兼容性**：不替换注意力层，而是复用现成的MLP组件作为快速权重存储器。
- **学习目标**：摒弃通用重建目标，提出与Next-Token Prediction对齐的目标，通过Conv1D和可训练投影 $\mathbf{W}_{\mathrm{target}}$ 融入未来token信息。理论分析（Theorem 1）证明该目标在期望上能增加正确token的logit，而重建目标不能。
- **更新策略**：以chunk-wise并行更新替代逐token顺序更新，chunk size ≥ 512时可充分利用硬件并行性，且支持上下文并行。

**主要结果**：在Qwen3-4B-Base上，In-Place TTT将RULER基准128k上下文长度的平均准确率从74.8%提升至77.0%，并在256k外推场景下保持提升（41.7% → 43.9%）。在LLaMA-3.1-8B和Qwen3-14B-Base上同样获得一致增益（+2.1%和+2.7%）。从头训练实验中，4B模型在RULER-16k上相较Full Attention提升13.4分，在常识推理任务上无退化。效率方面，In-Place TTT引入的prefill吞吐量和峰值内存开销在实际场景中可忽略。

**证据强度**：主要声明的置信度在0.95-0.99之间，受Table 1/2/3的定量结果、Theorem 1的理论推导以及Figure 3的消融实验支撑。当前框架的局限性在于仅适用于基于MLP的快速权重，对非自回归任务的有效性未经验证。

## 背景与动机

大语言模型在推理时面临一个根本性瓶颈：模型参数一旦训练完成便完全冻结，无法根据持续变化的上下文进行动态适应。这种静态特性严重限制了模型在长序列推理和在线学习场景中的表现——当上下文长度远超训练时所见范围，或当输入分布发生漂移时，固定参数的模型难以有效捕捉新出现的模式与依赖关系。

测试时训练（Test-Time Training, TTT）为这一问题提供了潜在的解决路径。TTT的核心理念是在推理过程中将部分模型参数作为“快速权重”进行即时更新，使模型能够将上下文信息编码进权重本身，从而实现动态适应。然而，现有TTT方法在应用于大语言模型时面临两个关键缺口：

**架构不兼容**。传统TTT方法通常需要引入独立的快速权重模块或辅助网络，这要求对现有LLM架构进行侵入式修改，无法作为“即插即用”的增强方案直接应用于已预训练的模型。对于动辄数十亿参数的LLM而言，从零重新设计和训练TTT架构的成本极高，这严重阻碍了TTT技术在LLM领域的广泛采用。

**学习目标错位**。先前TTT方法普遍采用通用重建目标（如重建当前token的嵌入表示）来驱动快速权重更新。然而，LLM的核心训练目标是下一token预测（Next-Token Prediction, NTP），重建目标与NTP之间存在本质差异——前者关注当前输入的忠实还原，后者关注对未来输出的准确预测。这种目标错位意味着快速权重的更新方向可能与语言建模任务的实际需求不一致，限制了TTT对LLM性能的提升潜力。

**计算效率瓶颈**。标准TTT框架要求对每个token进行顺序化的快速权重更新，这种逐token的串行计算模式与LLM推理中高度并行化的批处理范式相冲突，在处理长序列时会引入显著的计算开销，难以在实际部署中大规模应用。

针对上述缺口，In-Place TTT提出了三个层面的解决方案：通过复用MLP块中已有的最终投影矩阵作为快速权重存储器，实现零架构侵入的即插即用增强；设计显式对齐NTP目标的学习信号，使快速权重更新方向与语言建模任务保持一致；提出大块并行更新策略，将逐token的顺序更新替换为chunk级别的并行计算，在保持因果性的同时大幅提升推理效率。

## 核心创新

In-Place TTT 的核心创新在于将 LLM 中已有的 MLP 组件原位复用为测试时训练的快速权重存储器，从而在不改变模型架构的前提下赋予模型推理时的动态上下文适应能力。这一设计围绕三个相互耦合的 changed slots 展开。

**1. 快速权重的原位选择：MLP 最终投影矩阵 (W_down)**

传统 TTT 方法通常需要引入额外的网络模块作为快速权重，这导致与现有预训练 LLM 的架构不兼容。In-Place TTT 的关键洞察是：门控 MLP 块中的最终投影矩阵 $\mathbf{W}_{\mathrm{down}}$ 天然满足快速权重的功能需求——它在每个 token 位置对中间激活进行线性变换，且其输出直接贡献于残差流。因此，方法将 $\mathbf{W}_{\mathrm{down}}$ 从推理时冻结的静态参数转变为可原位更新的快速权重，而输入投影 $\mathbf{W}_{\mathrm{gate}}$ 和 $\mathbf{W}_{\mathrm{up}}$ 则保持冻结作为慢权重：

$$\mathbf{O} = \left( \phi(\mathbf{H}\mathbf{W}_{\mathrm{gate}}^{\top}) \odot (\mathbf{H}\mathbf{W}_{\mathrm{up}}^{\top}) \right) \mathbf{W}_{\mathrm{down}}^{\top}$$

这种“即插即用”的设计意味着任何预训练 Transformer 的 MLP 块都可以直接转化为 TTT 模块，无需改动注意力层或添加额外子网络。在 Qwen3-4B-Base、LLaMA-3.1-8B 和 Qwen3-14B-Base 上的实验均验证了该原位适配的通用性（Table 1, Table 2）。

**2. 更新目标的根本转变：从重建到 Next-Token Prediction 对齐**

先前 TTT 方法普遍采用通用重建目标（如重建当前 token 的嵌入），这本质上是自监督的去噪目标，与语言模型的因果预测目标存在语义错位。In-Place TTT 将快速权重的更新目标重新定义为与 Next-Token Prediction (NTP) 对齐的目标值 $\hat{\mathbf{V}}$：

$$\hat{\mathbf{V}} = \operatorname{Conv1D}(\mathbf{X}_0) \mathbf{W}_{\mathrm{target}}$$

其中 $\operatorname{Conv1D}$ 在 token 嵌入序列上进行一维卷积以捕获局部未来信息，$\mathbf{W}_{\mathrm{target}}$ 是可训练的投影矩阵。这一设计将未来 token 的信息注入到 TTT 的值目标中，使得快速权重更新直接服务于“预测下一个 token”这一终极任务。

理论分析（Theorem 1）为这一设计提供了严格支撑：使用 LM 对齐目标时，正确 token 的 logit 期望增量存在正下界 $\mathbb{E}[\Delta \ell_n[v^*]] \geq \lambda_{lr} \cdot c_{norm}^2 \cdot c_{align}$，而其他 token 的 logit 变化被限制在极小范围内 $|\mathbb{E}[\Delta \ell_n[w]]| \leq \lambda_{lr} \cdot \epsilon \cdot c_{align}$。相比之下，重建目标对正确 token 的 logit 几乎无增益。消融实验（Figure 3c）进一步证实 Conv1D 和 $\mathbf{W}_{\mathrm{target}}$ 均为实现最优性能的必要组件，且 Conv1D 对长上下文更为关键。

**3. 更新粒度的规模化：从逐 token 顺序更新到 chunk-wise 并行更新**

标准 TTT 的逐 token 顺序更新在长序列推理时效率极低，无法利用现代硬件的并行能力。In-Place TTT 利用 MLP 原位适配的特性，将更新粒度从单个 token 扩展到整个 chunk（块），实现了高效的 chunk-wise 并行更新规则：

$$\mathbf{W}_{\mathrm{down}}^{(i)} = \mathbf{W}_{\mathrm{down}}^{(i-1)} + \eta \hat{\mathbf{V}}_{[i]}^{\top} \mathbf{Z}_{[i]}$$

这一规则使得每个 chunk 内的所有 token 可以并行参与快速权重的梯度更新，同时保持严格的因果性（apply-then-update 循环）。消融实验（Figure 3b）表明 chunk size 512 和 1024 获得最优性能，且较大的 chunk 带来更高的计算效率。效率分析（Figure 4）显示 In-Place TTT 在实际场景中引入的额外开销可忽略不计。

**创新之间的因果耦合关系**

上述三个 changed slots 并非孤立存在，而是形成了一条因果链：MLP 的原位复用（slot 1）使得模型无需额外参数即可承载快速权重，从而允许使用大 chunk 进行高效更新（slot 3）；而 chunk-wise 更新的可行性又为引入需要聚合局部未来信息的 NTP 对齐目标（slot 2）提供了结构基础。三者共同作用，使得 In-Place TTT 能够在保持即插即用和高效推理的前提下，将 LLM 的长上下文推理能力提升到新的水平——在 RULER 基准上，Qwen3-4B-Base 的 128k 准确率从 74.8% 提升至 77.0%，并保持到 256k 的外推能力（Table 1）。

## 整体框架

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_dTWfCLSoyl/figures/006_Figure_3.jpg]]
*Figure 3: Ablation studies on the key design choices of the In-Place TTT framework, evaluated on the RULER benchmark with a 1.7B parameter model. The plots illustrate the impact of: (a) State size, showing that performance improves as the state size scales; (b) Chunk size, demonstrating a performance trade-off where intermediate sizes (e.g., 512, 1024) are optimal; and (c) The LM-Aligned Value objective, confirming that both the convolution (w Conv) and the projection (w Proj) are crucial*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_dTWfCLSoyl/figures/001_Figure_1.jpg]]
*Figure 1: The overall framework of our In-Place Test-Time Training. The module operates sequentially on input chunks. For each chunk, the current fast weights are first applied to the intermediate activations Z to produce the output. Then, these weights are updated using the activations Z and a value V derived from the token embeddings. This ”apply-then-update” cycle allows the model to dynamically adapt to incoming context in a strictly causal manner*

In-Place TTT 的整体框架遵循一个严格的因果“先应用后更新”（apply-then-update）循环，在推理时逐块（chunk-wise）处理输入序列，使得LLM能够动态适应持续变化的上下文，而无需修改模型架构或引入外部存储模块。

### 核心设计：原位复用MLP为快速权重

框架的关键洞察在于，LLM中广泛存在的门控MLP模块天然具备作为联想存储器（associative memory）的潜力。In-Place TTT 将MLP块中的输入投影矩阵 $\mathbf{W}_{\text{gate}}$ 和 $\mathbf{W}_{\text{up}}$ 视为冻结的慢速权重（slow weights），而将最终投影矩阵 $\mathbf{W}_{\text{down}}$ 重新定位为可适应的快速权重（fast weights），在推理时进行原位更新。这种设计实现了零架构侵入——所有现有组件保持不变，仅 $\mathbf{W}_{\text{down}}$ 的角色从静态投影转变为动态上下文编码器。

### 逐块应用-更新循环

如 Figure 1 所示，框架以块（chunk）为单位顺序处理输入token。对于每个块 $[i]$，流程分为两步：

1. **应用阶段（Apply）**：当前的快速权重 $\mathbf{W}_{\text{down}}^{(i-1)}$ 首先被应用于该块的中间激活 $\mathbf{Z}_{[i]}$，生成MLP输出。这一步与标准Transformer的前向传播完全兼容。
2. **更新阶段（Update）**：随后，利用该块的激活 $\mathbf{Z}_{[i]}$ 和从token嵌入中提取的目标值 $\hat{\mathbf{V}}_{[i]}$，通过一次梯度下降步骤更新快速权重，得到 $\mathbf{W}_{\text{down}}^{(i)}$，为下一个块做好准备。

这种“应用后更新”的顺序严格遵循因果性（causality），确保每个token的表示仅依赖于当前及之前的上下文信息。

### 更新规则与目标对齐

更新规则的具体形式为：
$$\mathbf{W}_{\text{down}}^{(i)} = \mathbf{W}_{\text{down}}^{(i-1)} + \eta \hat{\mathbf{V}}_{[i]}^{\top} \mathbf{Z}_{[i]}$$
其中 $\eta$ 为学习率。该规则源于使用负Frobenius内积作为损失函数时的梯度下降闭式解，避免了显式的反向传播，使得更新在计算上极为高效。

目标值 $\hat{\mathbf{V}}$ 的设计是框架的另一核心。与传统TTT使用当前token嵌入作为重建目标不同，In-Place TTT引入了与Next-Token Prediction（NTP）对齐的目标：
$$\hat{\mathbf{V}} = \operatorname{Conv1D}(\mathbf{X}_0) \mathbf{W}_{\text{target}}$$
该目标通过一维卷积（Conv1D）和可训练投影矩阵 $\mathbf{W}_{\text{target}}$ 从输入嵌入中提取未来token信息，使得快速权重的更新方向与语言模型的最终目标保持一致。理论分析（Theorem 1）证明，这种LM对齐的目标能够在期望上增加正确token的logit，而重建目标则无法提供这一保证。

### 效率优势：大块并行更新

框架采用大块（chunk size ≥ 512）并行更新策略，取代了传统TTT逐token顺序更新的低效方式。这一设计充分利用现代硬件的并行计算能力，同时得益于原位MLP适配的特性，可以使用较大的块大小 $C$ 一次性处理大量token。实验表明，chunk size为512和1024时取得最佳性能，且更大的chunk在效率上更具优势。效率分析确认，In-Place TTT在实际场景中引入的计算和内存开销几乎可以忽略不计。

## 核心模块与公式推导

### 原位MLP快速权重模块

In-Place TTT的核心设计是将Transformer中已有的MLP模块复用为快速权重存储器，而非引入额外结构。具体而言，在标准门控MLP中：

$$
\mathbf{O} = \left( \phi(\mathbf{H}\mathbf{W}_{\mathrm{gate}}^{\top}) \odot (\mathbf{H}\mathbf{W}_{\mathrm{up}}^{\top}) \right) \mathbf{W}_{\mathrm{down}}^{\top}
$$

其中输入投影 $\mathbf{W}_{\mathrm{gate}}$ 和 $\mathbf{W}_{\mathrm{up}}$ 作为冻结的慢权重保持不变，而最终投影矩阵 $\mathbf{W}_{\mathrm{down}}$ 被重新定义为可适应的快速权重，在推理时进行原位更新。这一设计实现了零架构侵入：模型结构完全不变，仅改变 $\mathbf{W}_{\mathrm{down}}$ 在推理过程中的使用方式。

该模块以chunk-wise方式运行：对于每个输入chunk，先用当前的 $\mathbf{W}_{\mathrm{down}}$ 对中间激活 $\mathbf{Z}$ 进行投影产生输出（apply），再利用同一chunk的 $\mathbf{Z}$ 和目标值 $\mathbf{V}$ 对 $\mathbf{W}_{\mathrm{down}}$ 进行更新（update），形成严格的因果“先应用-后更新”循环。

### Chunk-wise快速权重更新规则

为适配现代硬件的并行特性，In-Place TTT将逐token的顺序更新替换为chunk-wise批量更新。更新规则基于梯度下降的一步近似，在使用负Frobenius内积作为损失函数时，可简化为封闭形式：

$$
\mathbf{W}_{\mathrm{down}}^{(i)} = \mathbf{W}_{\mathrm{down}}^{(i-1)} + \eta \hat{\mathbf{V}}_{[i]}^{\top} \mathbf{Z}_{[i]}
$$

其中：
- $\mathbf{W}_{\mathrm{down}}^{(i-1)}$ 为处理第 $i$ 个chunk前的快速权重
- $\mathbf{Z}_{[i]}$ 为第 $i$ 个chunk的中间激活（作为键）
- $\hat{\mathbf{V}}_{[i]}$ 为第 $i$ 个chunk对应的LM对齐目标值（作为值）
- $\eta$ 为学习率

该更新规则本质上执行了一次外积关联记忆操作：将当前chunk的上下文信息通过 $\hat{\mathbf{V}}_{[i]}^{\top} \mathbf{Z}_{[i]}$ 写入 $\mathbf{W}_{\mathrm{down}}$，使模型能够动态编码持续变化的上下文。

### LM对齐目标值生成

目标值 $\hat{\mathbf{V}}$ 的设计是In-Place TTT区别于先前TTT方法的关键。传统TTT使用当前token的嵌入作为重建目标，而In-Place TTT引入与Next-Token Prediction对齐的目标，显式融入未来token信息：

$$
\hat{\mathbf{V}} = \operatorname{Conv1D}(\mathbf{X}_0) \mathbf{W}_{\mathrm{target}}
$$

其中：
- $\mathbf{X}_0$ 为当前token的嵌入
- $\operatorname{Conv1D}$ 为1维卷积操作，用于聚合局部未来token信息
- $\mathbf{W}_{\mathrm{target}}$ 为可训练的投影矩阵

该设计使得快速权重更新时，$\hat{\mathbf{V}}$ 携带了当前token“应该预测什么”的信息，从而与语言模型的预训练目标保持一致。

### 理论保证

**定理1** 从理论上证明了LM对齐目标相对于重建目标的优势。在使用LM对齐目标进行一次快速权重更新后，正确token $v^*$ 的logit期望增量满足下界：

$$
\mathbb{E}[\Delta \ell_n[v^*]] \geq \lambda_{lr} \cdot c_{norm}^2 \cdot c_{align}
$$

而其他token $w \neq v^*$ 的logit期望变化被严格约束：

$$
|\mathbb{E}[\Delta \ell_n[w]]| \leq \lambda_{lr} \cdot \epsilon \cdot c_{align}, \quad \forall w \neq v^*
$$

其中 $\lambda_{lr}$ 为学习率相关项，$c_{norm}$ 和 $c_{align}$ 为正值常数，$\epsilon$ 为小量。这表明LM对齐目标在期望上能够选择性地提升正确token的预测概率，同时几乎不影响其他token的logit分布。相比之下，使用重建目标时，正确token的logit变化也被 $\epsilon$ 量级的上界所约束，无法提供有效的信号增强。

### 推理时数值稳定机制

为防止快速权重在极长序列中累积更新导致无界增长，In-Place TTT在推理时对每次更新的增量进行Frobenius范数裁剪：

$$
\Delta \mathbf{W}_{\mathrm{down}}^{(i)} \leftarrow \tau \cdot \Delta \mathbf{W}_{\mathrm{down}}^{(i)} / \| \Delta \mathbf{W}_{\mathrm{down}}^{(i)} \|_F
$$

其中 $\tau$ 为裁剪阈值，$\Delta \mathbf{W}_{\mathrm{down}}^{(i)} = \eta \hat{\mathbf{V}}_{[i]}^{\top} \mathbf{Z}_{[i]}$。该操作确保每次更新的幅度有界，从而保证推理过程的数值稳定性。

## 实验与分析

### 即插即用增强：预训练LLM的长上下文能力跃升

In-Place TTT作为一种“即插即用”的测试时训练增强方案，首先在**Qwen3-4B-Base**（Yang et al., 2025）上进行了验证。实验采用两阶段持续训练课程：第一阶段约20B tokens、32k上下文长度，第二阶段约15B tokens、128k上下文长度，并使用YaRN（Peng et al., 2023）适配RoPE以支持长序列。在此公平训练条件下，In-Place TTT是唯一变量。

**Table 1**展示了RULER基准上的核心结果。在128k上下文长度下，In-Place TTT将基线准确率从74.8%提升至77.0%（+2.2个百分点），并在256k外推场景下维持优势（43.9% vs. 41.7%）。值得关注的是，在64k长度上提升更为显著：从74.3%跃升至78.7%（+4.4个百分点），暗示该方法在中长上下文场景的适配效率更高。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_dTWfCLSoyl/figures/002_Table_1.jpg]]
*Table 1: Evaluation results on the RULER benchmark (Hsieh et al., 2024). We report the average accuracy (%) as scores, with the best results in bold*

该增强效果在更大规模模型上得到复现（**Table 2**）：**LLaMA-3.1-8B**在64k上下文下从81.6%提升至83.7%（+2.1），**Qwen3-14B-Base**从67.9%提升至70.6%（+2.7）。这证实In-Place TTT的提升与模型规模呈正向关联，且与RoPE扩展技术（如YaRN）正交。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_dTWfCLSoyl/figures/003_Table_2.jpg]]
*Table 2: Extension of In-Place TTT to LLaMA-3.1-8B and Qwen3-14B-Base on the RULER benchmark. We report the average accuracy (%) with the best results in bold*

### 从头训练验证：超越注意力基线

为排除预训练偏差，论文在500M和1.5B参数规模下进行了从头训练实验。**Figure 2**的滑动窗口困惑度（Sliding Window Perplexity）曲线显示，In-Place TTT在所有上下文长度上均低于**Sliding-Window Attention (SWA)**和**Full Attention**基线。在4B模型上（**Table 3**），长上下文评测的优势更为明显：

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_dTWfCLSoyl/figures/004_Figure_2.jpg]]
*Figure 2: Sliding Window Perplexity at varying context lengths on the Pile dataset for 500M (left) and 1.5B (right) parameter models. Our In-Place TTT consistently achieves lower perplexity than all competitive baselines*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_dTWfCLSoyl/figures/005_Table_3.jpg]]
*Table 3: Evaluation results of 4B models on common sense reasoning and long-context evaluation benchmarks. Best performance is in bold. “SWA” is Sliding-Window Attention, “Full Attn.” is Full Attention, and “I.P. TTT” is our In-Place TTT*

- **Full Attention + In-Place TTT**在RULER-16k上从6.58跃升至19.99（+13.41）
- **SWA + In-Place TTT**在RULER-8k上从9.91提升至26.80（+16.89）

这表明In-Place TTT对注意力机制的局限性具有独立且互补的补偿能力，尤其在SWA这类信息受限架构上增益更为突出。

### 消融实验：三个关键设计维度的因果验证

在1.7B模型上，**Figure 3**系统消融了核心设计选择：

**(a) 状态大小（快速权重的容量）**：性能随$W_{\text{down}}$矩阵规模扩大而单调提升。这直接验证了核心假设——更大的快速权重空间赋予了模型更强的上下文编码能力，是性能提升的因果瓶颈。

**(b) Chunk大小**：$C=512$和$C=1024$达到最优性能，且$C=1024$具有更好的计算效率。过小的chunk（如$C=128$）限制了并行度，过大的chunk（如$C=4096$）则可能因更新频率过低而损失时序适应性。这一trade-off揭示了chunk-wise更新策略的工程敏感性。

**(c) LM对齐目标的组件必要性**：同时移除Conv1D和$W_{\text{target}}$（即退化为简单重建目标）导致性能显著下降。单独分析显示，Conv1D对长上下文更为关键（提供未来token的局部组合信息），而$W_{\text{target}}$对短上下文更为关键（提供精确的投影对齐）。两者缺一不可，共同构成了NTP对齐目标的必要基础。

### 效率分析：可忽略的推理开销

**Figure 4**对比了4B模型在SWA和Full Attention下的prefill吞吐量和峰值内存。In-Place TTT引入的额外计算和存储开销在实用场景下可忽略不计。这得益于两个设计选择：(1) 复用现有MLP的$W_{\text{down}}$作为快速权重，无需引入额外参数存储；(2) chunk-wise更新策略充分利用了GPU的并行计算能力，避免了逐token更新的串行瓶颈。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_dTWfCLSoyl/figures/007_Figure_4.jpg]]
*Figure 4: Efficiency analysis of In-Place TTT. Both prefill throughput (a, b) and peak memory (c, d) metrics are presented for 4B models with Sliding-Window Attention (SWA) and Full Attention at various context lengths. Our In-Place TTT introduces negligible overhead in practical scenarios*

### 理论支撑：为什么NTP对齐目标有效

**Theorem 1**为实验结论提供了理论解释。使用LM对齐目标时，正确token logit的期望增量存在正下界：

$$\mathbb{E}[\Delta \ell_n[v^*]] \geq \lambda_{lr} \cdot c_{norm}^2 \cdot c_{align}$$

而其他token的logit变化被严格约束：

$$|\mathbb{E}[\Delta \ell_n[w]]| \leq \lambda_{lr} \cdot \epsilon \cdot c_{align}, \quad \forall w \neq v^*$$

相比之下，传统重建目标对正确token的logit增量可忽略不计（$|\mathbb{E}[\Delta \ell_n[v^*]]| \leq \lambda_{lr} \cdot \epsilon \cdot c_{align}$）。这从期望意义上解释了为何NTP对齐目标能系统性地提升预测准确率，而重建目标不能。

### 失败模式与局限性

尽管整体性能提升显著，以下边界情况值得关注：

1. **短上下文场景的边际收益递减**：在RULER的4k-8k长度下，部分子任务提升幅度较小（Table 1），表明快速权重在信息已充分冗余的短上下文中作用有限。

2. **极长序列的数值稳定性**：256k外推虽有提升（+2.2），但绝对准确率仅43.9%。论文在附录D.2中采用Frobenius范数裁剪来约束更新增量：

$$\Delta W_{\text{down}}^{(i)} \leftarrow \tau \cdot \Delta W_{\text{down}}^{(i)} / \| \Delta W_{\text{down}}^{(i)} \|_F$$

但该机制在更长序列（如512k+）下的有效性未经实验验证。

3. **架构依赖**：当前设计仅适用于基于MLP的Transformer块，无法直接迁移至其他网络结构（如纯注意力或Mamba架构）。

4. **非自回归任务的未验证性**：NTP对齐目标天然依赖因果序列结构，对双向上下文或非语言建模任务的有效性仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_dTWfCLSoyl/figures/008_Table_4.jpg]]
*Table 4: Training hyperparameters for 500M and 1.5B models*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_dTWfCLSoyl/figures/009_Table_5.jpg]]
*Table 5: Training hyperparameters for 1.7B models and 4B models pretraining*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_dTWfCLSoyl/figures/010_Table_6.jpg]]
*Table 6: Hyperparameters for two-stage continual pre-training*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_dTWfCLSoyl/figures/011_Table_7.jpg]]
*Table 7: Hyperparameters for continual pre-training of LLaMA-3.1-8B and Qwen3-14B-Base*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_dTWfCLSoyl/figures/012_Table_8.jpg]]
*Table 8: Model architectural configurations for 500M and 1.5B Model*

## 方法谱系与知识库定位

### 与现有TTT工作的关系

In-Place TTT建立在测试时训练（Test-Time Training）这一研究脉络之上，但与现有工作存在三个根本性差异：

**架构兼容性**：传统TTT方法（如TTT-Linear）通常需要替换Transformer中的自注意力层，引入专门设计的快速权重模块，这导致与现有预训练LLM的架构不兼容。In-Place TTT通过“原位”设计解决了这一问题——它直接复用MLP块中已有的最终投影矩阵 $W_{\text{down}}$ 作为快速权重，无需修改模型结构。这一设计使其能够作为即插即用的增强模块，直接应用于**Qwen3-4B-Base**（Yang et al., 2025）、**LLaMA-3.1-8B**和**Qwen3-14B-Base**等开源模型，仅需持续预训练即可激活TTT能力。

**更新效率**：标准TTT采用逐token的顺序更新策略，在长序列推理中效率极低。In-Place TTT将其替换为chunk-wise并行更新规则，利用现代硬件的并行计算能力，使得chunk size可扩展至512甚至1024，大幅提升推理吞吐量。

**学习目标**：先前TTT工作普遍采用通用重建目标（如重建当前token的嵌入），这在理论上与语言建模的Next-Token Prediction目标不一致。In-Place TTT首次提出了与NTP对齐的学习目标，通过Conv1D和可训练投影 $W_{\text{target}}$ 从token嵌入中提取未来token信息作为更新目标值。理论分析（Theorem 1）严格证明：LM对齐目标能够在期望上增加正确token的logit（下界 $\mathbb{E}[\Delta \ell_n[v^*]] \geq \lambda_{lr} \cdot c_{norm}^2 \cdot c_{align}$），而重建目标无法提供这一保证。

### 与长上下文建模方法的关系

在长上下文建模的谱系中，In-Place TTT与两类主流方法形成互补而非替代：

**滑动窗口注意力（SWA）**：SWA通过限制注意力范围来降低计算复杂度，但丢弃了窗口外的上下文信息。In-Place TTT的快速权重机制天然具备记忆长程依赖的能力——它将历史上下文压缩到 $W_{\text{down}}$ 的状态中，从而弥补SWA的信息损失。从头训练实验证实了这一互补性：在4B模型上，In-Place TTT在SWA基础上将RULER-8k得分从9.91提升至26.80（Table 3），提升幅度达+16.89。

**全注意力（Full Attention）**：全注意力保留完整上下文但计算代价高昂。In-Place TTT在全注意力基础上仍能带来增益（RULER-16k从6.58提升至19.99），表明快速权重提供的动态适应能力与注意力机制的信息检索能力是正交的。

**RoPE扩展技术**：实验表明In-Place TTT与YaRN等位置编码扩展方法正交。在LLaMA-3.1-8B上结合YaRN后，In-Place TTT仍能在64k上下文带来+2.1的RULER精度提升（Table 2），说明快速权重适应和位置外推解决的是长上下文建模的不同瓶颈。

### 适用边界与局限

1. **架构依赖**：当前框架仅利用MLP块中的 $W_{\text{down}}$ 作为快速权重，无法直接应用于不含门控MLP结构的模型（如纯注意力架构或Mamba类状态空间模型）。扩展到其他网络结构需要重新设计快速权重的载体。

2. **目标函数依赖未来信息**：NTP对齐目标通过Conv1D融合未来token信息来构造更新目标值，这一设计天然依赖自回归的因果结构。对于非自回归任务（如完形填空、双向编码），该目标的适用性未经验证，可能需要重新设计对齐策略。

3. **优化器简化**：当前实现采用单步梯度下降（带Frobenius范数裁剪）作为快速权重更新规则，未探索更复杂的TTT优化器（如Adam风格的动量累积或二阶方法）。这可能在极长序列中限制快速权重的适应能力。

4. **数值稳定性**：快速权重在推理过程中持续累积更新，尽管采用了范数裁剪（$\Delta W_{\text{down}}^{(i)} \leftarrow \tau \cdot \Delta W_{\text{down}}^{(i)} / \|\Delta W_{\text{down}}^{(i)}\|_F$），但在极长序列（如百万token级别）中的数值稳定性尚未系统验证。

### 开放问题

1. **跨模态扩展**：In-Place TTT的“原位复用现有组件”思想能否推广到计算机视觉中的视觉Transformer或视频理解模型？视觉领域的TTT目标函数应如何设计？

2. **多步预测目标**：当前目标仅利用未来token的局部组合（通过Conv1D学习），是否可以通过显式的多步预测（预测未来第k个token）进一步提升快速权重的上下文编码质量？

3. **遗忘机制**：在非平稳序列（如多文档拼接、主题切换）中，快速权重可能保留过时的上下文信息。能否设计精细的forgetting机制（如衰减因子或选择性重置）来提升适应性？

4. **TTT优化器设计**：不同的损失函数（如对比损失、余弦相似度）和优化器选择对快速权重更新质量的影响尚未系统探索。是否存在比当前负Frobenius内积更优的相似度度量？

5. **与KV缓存的关系**：快速权重本质上提供了一种压缩的上下文表示，能否将其与KV缓存压缩技术（如StreamingLLM、H2O）协同设计，实现更高效的长序列推理？

## 原文 PDF

![[paperPDFs/ICLR_2026/In_Place_Test_Time_Training.pdf]]
