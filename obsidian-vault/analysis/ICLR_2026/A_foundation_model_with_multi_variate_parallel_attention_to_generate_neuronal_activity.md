---
title: "A foundation model with multi-variate parallel attention to generate neuronal activity"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_foundation_model_with_multi_variate_parallel_attention_to_generate_neuronal_activity.pdf
aliases:
- MVPAM
- FMMVPAGNA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/neuroscience_cognitive_science
core_operator: "多变量并行注意力（MVPA）机制，它将注意力分解为内容、时间和通道三个独立组件，从而解耦了信号的语义、时间动态和空间结构。"
primary_logic: "通过将注意力分解为内容、时间和通道三个并行组件，MVPA能够在不依赖固定通道位置或全局位置编码的情况下，灵活高效地处理通道数可变的异构时间序列数据，从而在iEEG等临床任务中实现强大的跨受试者泛化能力。"
claims:
- "MVPFormer在SWEC iEEG数据集上实现了0.61的平均Kappa值，超越了所有基线模型。"
- "MVPFormer在Brain TreeBank的四个解码任务（pitch, volume, onset, speech）上均达到或超越了SOTA性能。"
- "MVPA的三个组件（内容、时间、通道）在经典时间序列预测任务上的消融实验表明，完整MVPA在多数情况下优于任何单一组件。"
- "MVPFormer在MAYO和FNUSA数据集上的癫痫检测F1分数显著优于Brant-2。"
---

# A foundation model with multi-variate parallel attention to generate neuronal activity

> [!tip] 核心洞察
> 通过将注意力分解为内容、时间和通道三个并行组件，MVPA能够在不依赖固定通道位置或全局位置编码的情况下，灵活高效地处理通道数可变的异构时间序列数据，从而在iEEG等临床任务中实现强大的跨受试者泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 一种基于多变量并行注意力机制生成神经元活动的基础模型 |
| 英文题名 | A foundation model with multi-variate parallel attention to generate neuronal activity |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=5M1YOW3bRq); [GitHub](https://github.com/IBM/multi-variate-parallel-transformer); [Project](https://huggingface.co/datasets/NeuroTec/SWEC_iEEG_Dataset) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/neuroscience_cognitive_science |
| Method | Multi-Variate Parallel Attention (MVPA) |
| Dataset | SWEC iEEG (Seizure Detection), MAYO iEEG (Seizure Detection), FNUSA iEEG (Seizure Detection) |

> [!tip] 效果简介
> - SWEC iEEG (Seizure Detection) 上，Kappa 为 0.61，对比 Brant-2: 0.08，变化 +0.53。
> - SWEC iEEG (Seizure Detection) 上，Episodic f1 为 0.59，对比 Brant-2: 0.01，变化 +0.58。
> - MAYO iEEG (Seizure Detection) 上，Episodic f1 为 0.36，对比 Brant-2: 0.19，变化 +0.17。

## 概述

本文针对现有深度神经网络处理多变量时间序列时面临的**通道异构性**瓶颈——尤其在颅内脑电图（iEEG）领域，不同受试者的电极布局各不相同，导致模型难以泛化——提出了一种**多变量并行注意力（MVPA）**机制。其核心洞察在于将注意力分解为内容、时间和通道三个独立组件，从而解耦信号的语义、时间动态和空间结构，使模型能够在不依赖固定通道位置或全局位置编码的情况下，灵活处理通道数可变的异构时间序列数据。

在方法上，MVPFormer 采用小波编码器将原始 iEEG 信号编码为连续的 2D 嵌入网格，通过 MVPA 层并行建模时间、空间和内容依赖关系，并基于对比学习进行生成式预训练以预测未来时间步的嵌入表示。其计算复杂度为 $O(T^2 \times \bar{C} + T \times C^2)$，在 NVIDIA A100-80GB GPU 上可将有效上下文长度推至超过 10,000。

实验结果表明，MVPFormer 在三个 iEEG 癫痫检测数据集上显著超越了当前 SOTA 基线 Brant-2：在 SWEC 数据集上平均 Kappa 值达到 0.61（Brant-2 为 0.08），在 MAYO 数据集上 Episodic f1 达到 0.36（Brant-2 为 0.19）。在 Brain TreeBank 的四个语音解码任务中，MVPFormer 在音高和音量任务上达到 SOTA，在起始和语音任务上仅次于 PopT。此外，在经典时间序列预测基准（ETTh1、ETTh2、Weather）上，MVPFormer 也匹配或超越了现有注意力模型的性能。消融实验证实，完整 MVPA 在多数情况下优于任何单一组件，且生成式预训练对性能有显著贡献（Kappa 从 0.61 降至 0.52）。

## 背景与动机

颅内脑电图（iEEG）是神经科学和临床癫痫诊疗中的关键数据模态，但其多变量时间序列特性给深度学习模型带来了根本性挑战。与自然语言或图像数据不同，iEEG 信号由多个电极通道同步采集，每个通道记录局部神经活动。**不同受试者乃至不同手术植入方案下的电极布局（通道数量、空间位置）高度异构**，这导致传统深度神经网络在处理此类数据时面临严重的泛化困难。

现有方法主要分为两类。一类是专门为脑电信号设计的 Transformer 模型，如 BrainBERT、Brant-2 和 PopT。这些模型通常采用标准自注意力机制（vanilla attention），并依赖绝对位置编码（`S`）来标记时间或空间位置。然而，标准自注意力将 2D 时空网格展平为 1D 序列，其计算复杂度为 `O(T^2 × C^2)`，当通道数 `C` 和时间步数 `T` 均较大时，计算开销巨大。更重要的是，**绝对位置编码要求输入具有固定的通道数量和顺序**，这使得模型无法直接应用于通道布局不同的新受试者，即缺乏跨受试者的零样本泛化能力。另一类是通用时间序列预测模型（如 PatchTST、TimesFM、TimeMixer），它们虽然在某些场景下有效，但并未针对 iEEG 信号的通道异构性和时空耦合特性进行专门设计。

本文的核心动机是解决上述瓶颈：**如何设计一种注意力机制，使其既能高效建模多变量时间序列的时空依赖关系，又能天然适应通道数量可变、布局未知的异构数据，从而实现强大的跨受试者泛化？** 为此，作者提出了**多变量并行注意力（Multi-Variate Parallel Attention, MVPA）**。其核心洞察在于：将标准自注意力的计算解耦为三个并行的组件——内容注意力、时间注意力和通道注意力。内容注意力仅关注 token 本身的语义；时间注意力仅关注时间上的相对距离（`T_{t-t'}`）；通道注意力仅关注空间上的相对距离（`C_{c-c'}`）。这种分解使得 MVPA 无需依赖固定的全局位置编码，而是通过可学习的相对位置偏置来灵活编码时空关系。因此，**模型在推理时能够处理任意数量的通道**，因为通道间的交互完全由相对空间距离驱动，而非绝对索引。

这一设计直接改变了两个关键模块。其一，注意力机制从“query 与 key 的绝对位置交互”变为“query 与 key 的相对距离交互”，如公式 (1)-(3) 所示。其二，计算复杂度从标准注意力的 `O(T^2 × C^2)` 降低为 `O(T^2 × C̄ + T × C^2)`，其中 `C̄` 是局部窗口内的通道数（`C̄ << C`），这使得模型能够处理更长的上下文（在 A100 GPU 上有效上下文长度超过 10,000）。此外，作者还引入了基于小波编码的连续嵌入空间和对比学习生成式预训练目标，以进一步提升模型对神经活动动态的建模能力。

简而言之，本文的动机源于 iEEG 数据固有的通道异构性这一现实瓶颈。MVPA 通过将注意力分解为内容、时间和通道三个组件，从根本上绕过了对固定通道布局的依赖，为构建可泛化的神经活动基础模型提供了新的技术路径。

## 核心创新

MVPFormer 的核心创新在于其提出的 **多变量并行注意力（MVPA）** 机制，该机制从根本上改变了 Transformer 处理多变量时间序列的方式，使其能够有效应对颅内脑电图（iEEG）等数据中通道异构性的根本挑战。现有深度神经网络在处理多变量时间序列时，通常将不同通道视为独立特征或需要全局位置编码，这导致模型在面对通道数可变、电极布局各异的跨受试者数据时泛化能力极差。MVPFormer 通过将注意力分解为三个并行的组件来解耦信号的语义、时间动态和空间结构，从而在不依赖固定通道位置的情况下灵活处理异构数据。

**核心改变：注意力机制的重构**

MVPFormer 对标准 Transformer 注意力机制进行了三项关键改造：

1.  **从绝对位置编码到相对位置编码**：标准自注意力（Vanilla attention）使用绝对位置编码 $S$，公式为 $\pmb{a}_{i,j}^{\mathrm{vanilla}} = (\pmb{x}_i + \pmb{S}_i)^T W_q^T W_k (\pmb{x}_j + \pmb{S}_j)$。MVPA 则彻底放弃了绝对位置编码，转而使用**相对位置编码**。它将注意力分解为三个独立组件：
    *   **内容注意力（Content-based attention）**：仅基于 token 本身的语义信息，不包含任何位置信息。
    *   **时间注意力（Time-based attention）**：仅依赖于查询与键之间的**时间距离**（$t-t'$），共享于所有通道。
    *   **通道注意力（Channel-based attention）**：仅依赖于查询与键之间的**空间距离**（$c-c'$），共享于所有时间步。

    这种分解使得模型能够独立地学习时间上的局部依赖和空间上的邻近关系，而无需知道通道在大脑中的绝对位置。实验表明，训练后通道注意力呈现出清晰的**对角结构**，表明模型成功学习到了邻近通道更相关的空间关系。

2.  **计算复杂度的降低**：标准自注意力将 2D 数据展平为 1D 序列，复杂度为 $O(T^2 \times C^2)$。MVPA 通过组件分解和局部窗口（内容注意力仅关注最近的 $L$ 个时间点）将复杂度降低至 $O(T^2 \times \bar{C} + T \times C^2)$，其中 $\bar{C} \ll C$。这使得模型在 NVIDIA A100-80GB GPU 上的有效上下文长度可超过 10,000。

3.  **生成式预训练目标**：与直接进行判别式微调的基线不同，MVPFormer 采用**对比学习**进行生成式预训练。其损失函数为：
    
$$
\mathcal{L}_{c,t} = -\log \frac{\exp(\sin(o_{c,t}, \boldsymbol{e}_{c,t+1}) / \tau)}{\sum_{z_k \in \mathcal{Z}} \exp(\sin(o_{c,t}, z_k) / \tau)}
$$

    该损失函数旨在增加模型输出（$o_{c,t}$）与真实未来嵌入（$\boldsymbol{e}_{c,t+1}$）之间的余弦相似度，同时降低与混淆目标（$z_k$）的相似度。移除该预训练目标后，模型在癫痫检测任务上的 Kappa 值从 0.61 降至 0.52（Table 30），证明了其关键作用。

**决定性证据与性能优势**

MVPA 的成效在多个基准测试中得到验证，尤其是在 iEEG 领域：

*   **癫痫检测（SWEC 数据集）**：MVPFormer 取得了 **0.61 的平均 Kappa 值**，远超当前 SOTA 模型 Brant-2 的 0.08（Table 1）。在更严格的 Episodic F1 指标上，MVPFormer 达到 0.59，而 Brant-2 仅为 0.01。
*   **跨数据集泛化**：在 MAYO 数据集上，MVPFormer 的 Episodic F1 为 0.36，显著高于 Brant-2 的 0.19（Table 28）。在 FNUSA 数据集上，两者表现持平（0.46），表明模型在不同临床环境下的泛化能力存在差异，但仍具竞争力。
*   **语音解码（Brain TreeBank）**：在不依赖电极位置信息的情况下，MVPFormer 在音高（Pitch）和音量（Volume）任务上超越了所有基线，准确率分别达到 0.83 和 0.88（Table 2）。
*   **经典时间序列预测**：在 ETTh1 数据集上，MVPFormer 的平均 MSE 为 0.45，远优于标准 Transformer 的 1.00（Table 39）。
*   **消融实验**：在经典时间序列预测任务上，完整 MVPA（三个组件）在多数情况下优于仅使用内容、时间或通道单一组件的变体（Table 40）。此外，使用 Vanilla Attention 的 MV-Llama 在癫痫检测任务上表现不佳，无法有效泛化（Table 21），这直接证明了 MVPA 架构设计的必要性。

**架构与模块**

MVPFormer 的完整流水线包括：
1.  **小波编码器（Wavelet Encoder）**：使用 db4 小波分解将原始 iEEG 信号在时间和空间上分段，编码为连续的 2D 嵌入网格。
2.  **MVPA 注意力层**：核心模块，对 2D 嵌入网格并行计算内容、时间和通道三个注意力组件。
3.  **MVPFormer 解码器**：基于 Llama2 架构，包含并行注意力和 MLP 块。
4.  **分类头**：一个线性层，用于下游任务的微调。

**局限性**：尽管性能卓越，该创新仍存在局限。根据 Chinchilla 缩放定律，当前 SWEC iEEG 数据集规模（9328 小时）不足以完全训练 MVPFormer-S（75M 参数），更不用说 MVPFormer-M（1.2B 参数）。此外，模型性能在不同受试者间存在显著差异，少数受试者是大部分不一致的来源，其潜在原因尚不明确。

## 整体框架

![[assets/figures/papers/iclr26_0002_5M1YOW3bRq_A_foundation_model_with_multi-variate_parallel_a/figures/002_Figure_2.jpg]]
*Figure 2: MVPFormer architecture and forward pass. iEEG signals are segmented in time and space, encoded via a wavelet-based encoder, and arranged into a 2D embedding grid. These continuous embeddings are processed by MVPA to model temporal, spatial, and content-based dependencies. MVPFormer predicts the next-in-time embedding while reducing similarity to confounders from the same or other subjects. Notched in the bottom right is the resulting cosine similarity with the true target and the confounders after training. The two-step target is the signal twice removed in the future*

MVPFormer 的完整 pipeline 围绕一个核心洞察构建：多变量时间序列（尤其是 iEEG）的通道异构性要求注意力机制必须解耦内容、时间和空间结构，而非依赖固定的绝对位置编码。整体架构由四个模块串联而成，形成从原始信号到下游预测的端到端流。

**输入与编码阶段**：原始 iEEG 信号首先在时间和空间两个维度上被分割，随后通过一个小波编码器（使用 db4 小波分解）将每个时空片段编码为连续的嵌入向量。这些嵌入被排列成一个 2D 网格，其中一维是时间步（T），另一维是通道（C）。这个网格构成了后续注意力计算的基础数据结构。小波编码器的核心作用是将高维、非平稳的生理信号压缩为紧凑且语义丰富的连续表示，为 MVPA 提供稳定的输入。

**核心处理模块——MVPA 注意力层**：这是整个 pipeline 的因果旋钮。MVPA 将标准自注意力分解为三个并行计算的组件（公式 1-3）：
- **内容注意力**：基于查询和键的语义相似度计算，不依赖任何位置编码，仅在局部窗口（L=10 个片段，约 50 秒）内计算，复杂度为 O(L² × C²)。
- **时间注意力**：仅依赖查询与键之间的时间距离（相对位置编码），在所有通道间共享，复杂度为 O(T² × C̄)。
- **通道注意力**：仅依赖查询与键之间的空间距离（相对位置编码），在所有时间步间共享，复杂度为 O(T × C²)。

三个组件的注意力分数求和后经过 softmax 和缩放因子（公式 4）得到最终输出。这种分解使得模型能够同时捕获语义、时间动态和空间结构，同时通过局部窗口和组件分解将总复杂度控制在 O(T² × C̄ + T × C²)，在 A100 GPU 上支持超过 10,000 的有效上下文长度。

**解码器与输出**：MVPFormer 基于 Llama2 架构，包含并行的 MVPA 注意力块和 MLP 块。在预训练阶段，模型使用对比损失（公式 5）预测未来时间步的嵌入表示，增加输出与真实目标之间的余弦相似度，同时降低与混淆目标（来自同受试者或其他受试者）的相似度。在下游任务微调时，解码器输出后接一个简单的线性分类头。

**数据流与模块关系**：信号 → 小波编码 → 2D 嵌入网格 → MVPA 注意力（内容+时间+通道） → Llama2 解码器 → 对比预测头（预训练）/线性分类头（微调）。关键设计约束是：MVPA 的三个注意力组件在训练过程中各自学习不同的依赖模式——通道注意力收敛为对角结构（邻近通道相关性更强），时间注意力收敛为局部聚焦（邻近时间片段关联更强），内容注意力则处理跨时空的语义匹配。

## 核心模块与公式推导

MVPFormer 的核心创新在于 **多变量并行注意力（Multi-Variate Parallel Attention, MVPA）**，它通过将标准自注意力分解为三个并行的组件——内容、时间和通道——来解耦多变量时间序列中语义、时间动态与空间结构这三个维度。该设计直接针对 iEEG 等临床数据中通道数可变、缺乏固定空间布局的核心瓶颈。

### 从标准注意力到 MVPA

标准自注意力（Vanilla Attention）的计算式为：
$$
\pmb{a}_{i,j}^{\mathrm{vanilla}} = (\pmb{x}_i + \pmb{S}_i)^T W_q^T W_k (\pmb{x}_j + \pmb{S}_j)
$$
其中 $\pmb{S}$ 是绝对位置编码。这种方式将位置信息与内容信息相加，强制模型在同一空间内处理二者，且当输入为 2D 网格（通道×时间）时，需要将数据展平为 1D 序列，导致计算复杂度为 $O(T^2 \times C^2)$。

一种直观的改进是双编码注意力（Dual-coded attention），使用独立的学习式时间编码 $\mathcal{T}_t$ 和通道编码 $\mathcal{C}_c$：
$$
\pmb{a}_{c,t,c',t'}^{\mathrm{dual}} = (\pmb{x}_{c,t} + \mathcal{T}_t + \mathcal{C}_c)^T W_q^T W_k (\pmb{x}_{c',t'} + \mathcal{T}_{t'} + \mathcal{C}_{c'})
$$
但这种方式仍然将三个信号混合在同一个注意力计算中，没有实现真正的解耦。

### MVPA 的分解式注意力

MVPA 将注意力分数拆解为三个独立相加的组件（式 1-3）：
$$
\pmb{a}_{c,t,c',t'}^{\mathrm{MVPA}} = \underbrace{\pmb{x}_{c,t}^T W_q^T W_{k_e} \pmb{x}_{c',t'} + \boldsymbol{u}^T W_{k_e} \pmb{x}_{c',t'}}_{\text{内容组件}} + \underbrace{\mathbf{x}_{c,t}^T W_q^T W_{k_t} \mathcal{T}_{t-t'} + v^T W_{k_t} \mathcal{T}_{t-t'}}_{\text{时间组件}} + \underbrace{\mathbf{x}_{c,t}^T W_q^T W_{k_c} \mathcal{C}_{c-c'} + w^T W_{k_c} \mathcal{C}_{c-c'}}_{\text{通道组件}}
$$

- **内容组件（Content-based）**：仅依赖查询 $\pmb{x}_{c,t}$ 和键 $\pmb{x}_{c',t'}$ 的语义相似性，不包含任何位置信息。$\boldsymbol{u}$ 是可学习的偏置项。该组件使用局部窗口（默认 $L=10$ 个时间片段，对应 50 秒），仅计算最近 $L$ 个时间点的注意力，以降低计算量。
- **时间组件（Time-based）**：仅依赖查询 $\pmb{x}_{c,t}$ 与键之间的**时间相对距离** $t-t'$，使用可学习的相对位置编码 $\mathcal{T}_{t-t'}$。该组件在所有通道间共享，因此不包含通道特异性信息。
- **通道组件（Channel-based）**：仅依赖查询 $\pmb{x}_{c,t}$ 与键之间的**空间相对距离** $c-c'$，使用可学习的相对位置编码 $\mathcal{C}_{c-c'}$。该组件在所有时间步间共享。

最终注意力输出经过 softmax 和缩放：
$$
A = \frac{\operatorname{softmax}(\pmb{a}^{\mathrm{MVPA}}) V}{\sqrt{d}}
$$

### 计算复杂度分析

MVPA 的总复杂度为 $O(T^2 \times \bar{C} + T \times C^2)$，其中 $T$ 是时间片段数，$C$ 是通道数，$\bar{C}$ 是局部窗口内的平均通道数（由于内容组件使用局部窗口 $L \ll T$，其复杂度为 $O(L^2 \times C^2)$）。这使得 MVPA 在时间维度上具有次二次复杂度，在 NVIDIA A100-80GB GPU 上可将有效上下文长度推至超过 10,000（如 100 通道 × 100 时间片段）。相比之下，将 2D 数据展平后使用标准自注意力的复杂度为 $O(T^2 \times C^2)$，在大规模数据上不可行。

### 预训练目标：对比损失

MVPFormer 的生成式预训练采用对比损失（式 5）：
$$
\mathcal{L}_{c,t} = -\log \frac{\exp(\sin(o_{c,t}, \boldsymbol{e}_{c,t+1}) / \tau)}{\sum_{z_k \in \mathcal{Z}} \exp(\sin(o_{c,t}, z_k) / \tau)}
$$
其中 $o_{c,t}$ 是模型对通道 $c$ 在时间 $t$ 的输出嵌入，$\boldsymbol{e}_{c,t+1}$ 是真实的下一个时间步嵌入（由小波编码器生成），$\mathcal{Z}$ 是混淆目标集合（包含来自同一受试者其他通道的嵌入以及来自其他受试者的嵌入），$\tau=0.1$ 是温度参数。该损失通过增加输出与真实目标之间的余弦相似度、降低与混淆目标之间的相似度，迫使模型学习具有时间预测能力的通用神经表示。

### 结构化丢弃

为减少连续时间片段和相邻通道之间的信息冗余，MVPFormer 使用结构化丢弃（Structured Dropout），其丢弃率为：
$$
t_{drop} = c_{drop} = 1 - \sqrt{1 - r_{drop}}
$$
其中 $r_{drop}$ 是常规丢弃率。该公式确保整体丢弃的元素数量与常规丢弃相同，但丢弃的是整个通道或整个时间步，而非随机片段。

## 实验与分析

### 主结果：iEEG癫痫检测与语音解码

MVPFormer在三个iEEG癫痫检测数据集上展现了显著的性能提升。在SWEC数据集上，MVPFormer-M取得了0.61的平均Kappa值和0.59的Episodic F1分数，大幅超越当前SOTA模型Brant-2（Kappa 0.08，Episodic F1 0.01）（Table 1）。这一差距（Kappa +0.53，Episodic F1 +0.58）表明标准Transformer架构在处理通道异构的iEEG数据时存在根本性瓶颈，而MVPA的解耦设计有效克服了这一问题。模型还实现了较低的假阳性率（0.15 fp/h）。在MAYO数据集上，MVPFormer的Episodic F1为0.36，显著优于Brant-2的0.19（Table 28）；但在FNUSA数据集上，两者持平（均为0.46，Table 29），提示模型在特定临床环境下的泛化能力存在边界。

![[assets/figures/papers/iclr26_0002_5M1YOW3bRq_A_foundation_model_with_multi-variate_parallel_a/figures/003_Table_1.jpg]]
*Table 1: Results on the iEEG seizure detection tasks. We compare MVPFormer with multiple baselines across 3 iEEG datasets. The best results are bolded*

在Brain TreeBank语音解码任务中，MVPFormer在pitch（0.83）和volume（0.88）两个任务上达到SOTA，超越了依赖电极绝对位置信息的PopT（分别为0.82和0.87）；在onset和speech任务上略低于PopT（0.87 vs 0.89，0.90 vs 0.91）（Table 2）。这表明MVPA隐式学习的通道空间映射在多数情况下优于显式位置编码，但声学起始检测等精细任务可能仍需要绝对空间信息。

![[assets/figures/papers/iclr26_0002_5M1YOW3bRq_A_foundation_model_with_multi-variate_parallel_a/figures/004_Table_2.jpg]]
*Table 2: Results on the Brain TreeBank tasks. We compare MVPFormer with multiple baselines the 4 tasks of the Brain TreeBank dataset. The models requiring the electrodes’ position are indicated by †. The best results without the electrodes’ position are bolded, while the results where the electrodes’ position is beneficial are underlined*

### 经典时间序列预测基准

为验证MVPA的通用性，论文在ETTh1、ETTh2和Weather三个标准预测基准上进行了评估（Table 39）。MVPFormer在所有设定下均大幅超越Vanilla Transformer（例如ETTh2平均MSE 0.38 vs 3.37），并在多数预测长度上达到或接近SOTA模型（PatchTST、TimesFM、TimeMixer、WPMixer）。值得注意的是，MVPFormer在长序列预测（720步）上的优势更为明显，这得益于其次二次复杂度架构对长上下文的有效处理。

### 消融实验与机制验证

**MVPA组件消融**（Table 40）：在经典时间序列预测任务上，完整MVPA（内容+时间+通道）在多数情况下优于仅使用单一组件的变体。移除时间或通道组件后性能显著下降，证实了多维度解耦的必要性。通道组件对多变量数据尤为重要——在ETTh2上，仅使用内容注意力的变体MSE从0.38升至0.50。

**预训练消融**（Table 30）：移除生成式对比预训练后，MVPFormer在SWEC上的Kappa从0.61降至0.52，下降14.8%，表明预训练阶段学习的神经活动动态模式对下游任务至关重要。

**通道选择消融**（Figure 16）：使用所有通道进行检测时，平均Kappa降至0.36，远低于自动通道选择（基于方差/峰度排序，公式r_C = var(C) / (1 + kurt(C))）的0.61。这说明噪声通道会严重干扰模型，而基于信号统计特性的通道筛选是性能的关键瓶颈。

**模型规模与数据规模**（Figure 17）：将预训练数据从18个受试者扩展至58个受试者，癫痫检测性能持续提升，表明当前数据规模（9328小时）尚未达到模型容量上限，符合Chinchilla缩放定律的预期。

**注意力机制可视化**（Figure 19）：训练后的通道注意力矩阵呈现明显的对角结构，表明模型自动学习到了邻近通道间的相关性；时间注意力则聚焦于局部时间窗口，与内容注意力的局部窗口（L=10段，即50秒）设计一致。这验证了MVPA各组件确实捕获了预期的依赖关系。

### 失败模式与局限性

1. **跨数据集泛化不均**：在FNUSA数据集上所有模型表现相似，提示该数据集可能存在独特的临床特征（如发作类型、电极布局）未被MVPA有效捕获。
2. **受试者间变异性**：少数受试者贡献了大部分不一致预测，其潜在原因（如发作模式罕见、电极位置异常）尚不明确，需要人工验证。
3. **噪声鲁棒性**：当信噪比降至30dB时，Kappa骤降至0.12，表明模型对信号质量高度敏感。
4. **数据规模瓶颈**：根据Chinchilla定律，当前9328小时数据不足以完全训练75M参数的MVPFormer-S，更遑论1.2B参数的MVPFormer-M。这限制了更大规模模型的潜力释放。

### 补充图表

![[assets/figures/papers/iclr26_0002_5M1YOW3bRq_A_foundation_model_with_multi-variate_parallel_a/figures/005_Table_3.jpg]]
*Table 3: Results on the time-series forecasting task. We report the mean-squared error (MSE) and mean-absolute error (MAE) averaged over all forecasting lengths*

![[assets/figures/papers/iclr26_0002_5M1YOW3bRq_A_foundation_model_with_multi-variate_parallel_a/figures/006_Table_4.jpg]]
*Table 4: Accuracy on time-series classification tasks. We report the accuracy per task*

![[assets/figures/papers/iclr26_0002_5M1YOW3bRq_A_foundation_model_with_multi-variate_parallel_a/figures/007_Table_5.jpg]]
*Table 5: Ablation of the components of MVPA on the time-series forecasting task. We report the mean-squared error (MSE) and mean-absolute error (MAE) averaged over all forecasting lengths*

## 方法谱系与知识库定位

MVPFormer 的核心创新——多变量并行注意力（MVPA）——直接回应了多变量时间序列建模中一个根本性的结构瓶颈：**通道异构性**。在颅内脑电图（iEEG）等临床场景中，不同受试者的电极布局（通道数、空间位置）各不相同，这使得依赖固定位置编码或全局位置嵌入的标准 Transformer 架构难以跨受试者泛化。MVPA 通过将注意力分解为内容、时间、通道三个并行组件，解耦了语义、时间动态和空间结构三个维度（Figure 1, Equation 1–3），从而在不依赖绝对通道位置信息的情况下，灵活处理通道数可变的输入。

**与基线方法的关系。** MVPA 的消融实验（Table 40）清晰展示了其设计优势：在 ETTh1、ETTh2 和 Weather 等经典时间序列预测基准上，完整 MVPA 在多数情况下优于仅保留单一组件的变体。例如，在 ETTh2 上，完整 MVPA 的 MSE 为 0.38，而仅使用内容组件时升至 0.51（数值源自 Table 39 与 Table 40 的对比）。更重要的是，MVPA 相较于标准自注意力（Vanilla Transformer）在 ETTh2 上实现了 MSE 从 3.37 到 0.38 的跨越式下降（Table 39）。在 iEEG 癫痫检测任务中，MVPFormer 在 SWEC 数据集上达到 0.61 的平均 Kappa 值，而当前领域 SOTA 模型 Brant-2 仅 0.08（Table 1），这一巨大差距直接验证了 MVPA 在处理通道异构性上的核心价值。在 Brain TreeBank 语音解码任务上，MVPFormer 在 pitch 和 volume 任务上超越所有基线，但在 onset 和 speech 任务上略逊于 PopT（Table 2），说明当任务高度依赖精确的绝对空间信息时，MVPA 隐式学习的通道关系可能仍不如显式位置编码。

**计算效率与架构定位。** MVPA 通过局部窗口（L=10 个时间片段，约 50 秒）和组件分解将复杂度降至 $O(T^2 \times \bar{C} + T \times C^2)$（其中 $\bar{C} \ll C$），相比标准自注意力 $O(T^2 \times C^2)$ 显著降低。其 Triton 实现 FlashMVPA 在 A100 上可达 20 TFlops，内存消耗与 FlashAttention 2 相当（Tables 10–11）。这使得 MVPFormer 在单个 GPU 上可处理超过 10,000 的有效上下文长度（如 100 通道 × 100 时间片段）。从方法谱系看，MVPA 填补了“解耦注意力机制”在多变量时间序列领域的空白：它不同于将时间/空间分别编码后相加的“双编码注意力”（dual-coded attention），而是通过独立的键投影矩阵 $W_{k_t}$ 和 $W_{k_c}$ 让模型在注意力计算层面直接学习时间距离和空间距离的偏置（Table 6 对比了 MVPA 与现有注意力机制的差异）。

**适用边界与局限性。** 第一，数据规模瓶颈。根据 Chinchilla 缩放定律，当前 SWEC iEEG 数据集（9328 小时，68 名受试者）远不足以完全训练 MVPFormer-S（75M 参数），更不用说 MVPFormer-M（1.2B 参数）。这直接限制了模型潜力的释放。第二，受试者间变异性。模型性能在不同受试者间差异显著，少数受试者是大部分不一致的来源，其潜在原因尚不明确。第三，对绝对空间信息的依赖。SWEC 数据集不包含通道在大脑中的绝对位置信息，这虽然保护了隐私，但也意味着 MVPA 无法利用此类信息——当任务需要精确的空间定位时（如 Brain TreeBank 的 onset 任务），模型性能可能受限。第四，噪声鲁棒性。当信噪比降至 30dB 时，模型 Kappa 值骤降至 0.12。第五，跨临床环境泛化。在 FNUSA 数据集上，MVPFormer 与 Brant-2 表现持平（Episodic F1 均为 0.46，Table 29），表明在某些临床环境下其优势不显著。

**开放问题。** 1) LLM 领域的缩放定律是否适用于 MVPA 这种架构和 iEEG 这种数据？2) 受试者间性能差异的潜在来源是什么——是数据质量、病理特征差异，还是模型对特定信号模式的偏好？3) ictal（发作期）和 interictal（发作间期）状态之间的精确关系是什么？这不仅是模型问题，也是神经科学领域持续讨论的基本问题。4) 将 SWEC iEEG 数据集公开后，是否会增加整体数据可用性并解锁进一步的模型缩放潜力？这些问题的回答将决定 MVPA 方向能否从“特定任务上的显著提升”走向“通用神经信号基础模型的可行路径”。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_foundation_model_with_multi_variate_parallel_attention_to_generate_neuronal_activity.pdf

![[paperPDFs/ICLR_2026/A_foundation_model_with_multi_variate_parallel_attention_to_generate_neuronal_activity.pdf]]
