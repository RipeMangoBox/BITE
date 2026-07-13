---
title: "Exploring the Potential of Encoder-free Architectures in 3D LMMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Exploring_the_Potential_of_Encoder_free_Architectures_in_3D_LMMs.pdf
project_link: null
code_link: https://github.com/Ivan-Tang-3D/ENEL
openreview_forum_id: 22Hh0Vj5Dd
aliases:
- EPEFA3L
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "移除预训练的3D编码器，直接让LLM承担3D编码的功能，通过设计LLM内嵌语义编码（自监督损失）和层次化几何聚合策略，使LLM直接从点云token中学习高层语义和局部几何结构。"
primary_logic: "通过LLM内嵌语义编码与层次几何聚合，无编码器架构可以达到甚至超越基于编码器的3D大模型性能，同时消除编码器带来的分辨率依赖和语义偏差。"
claims:
- "ENEL-7B 在 Objaverse 分类(55.55)、描述(51.03 GPT-4)和 VQA(43.8)任务上，性能与13B编码器基线相当。"
- "移除编码器后，分类和描述 GPT-4 分数分别下降 17.5% 和 10.48%，而加入3层 token embedding 可大幅恢复。"
- "注意力可视化显示，无编码器架构的点 token 与文本 token 的语义关联更强，如图 5 所示。"
- "Objaverse 上 GPT-4 score (Captioning) = ENEL-7B: 51.03"
---

# Exploring the Potential of Encoder-free Architectures in 3D LMMs

> [!tip] 核心洞察
> 通过LLM内嵌语义编码与层次几何聚合，无编码器架构可以达到甚至超越基于编码器的3D大模型性能，同时消除编码器带来的分辨率依赖和语义偏差。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 探索无编码器架构在三维大语言模型中的潜力 |
| 英文题名 | Exploring the Potential of Encoder-free Architectures in 3D LMMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=22Hh0Vj5Dd) · [GitHub](https://github.com/Ivan-Tang-3D/ENEL) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | ENEL |
| Dataset | Objaverse, 3D-VQA (3D MM-Vet) |

> [!tip] 效果简介
> - Objaverse 上，GPT-4 score (Captioning) 为 ENEL-7B: 51.03，对比 PointLLM-7B: 44.85，变化 +6.18。
> - Objaverse 上，GPT-4 score (Classification) 为 ENEL-7B: 55.55，对比 PointLLM-7B: 53.00，变化 +2.55。
> - 3D-VQA (3D MM-Vet) 上，GPT-4 score 为 ENEL-7B: 43.80，对比 PointLLM-7B: 41.20，变化 +2.60。

## 概要

基于预训练编码器的3D大语言模型（3D LMMs）存在两个根本性瓶颈：**点云分辨率限制**（训练与推理分辨率不匹配导致空间信息丢失）和**嵌入语义差异**（编码器预训练目标与LLM语义需求不对齐）。本文提出首个无编码器3D大模型 **ENEL**，将3D编码功能直接迁移至LLM内部，通过两大策略实现该目标：预训练阶段的 **LLM内嵌语义编码**（Hybrid Semantic Loss）和指令微调阶段的 **层次化几何聚合**（Hierarchical Geometry Aggregation）。

核心因果机制在于：移除重预训练编码器后，LLM的前4层被设为可学习，配合轻量级Token Embedding模块（仅3M参数）将原始点云转化为高维token；混合语义损失对30%掩码token做特征预测、对70%可见token做点云块重建，促使LLM直接从点云数据中学习高层语义；层次化几何聚合则通过动态网格采样和门控自注意力在LLM早期层间捕获局部几何结构。

主要实验结果（Table 5）表明，ENEL-7B在Objaverse分类（55.55）、描述（51.03 GPT-4）和3D VQA（43.8）任务上全面超越PointLLM-7B编码器基线，甚至与13B增强基线PointLLM-PiSA-13B性能相当。消融实验验证了各模块的关键作用：移除混合语义损失导致描述GPT-4分数下降至47.15，移除门控机制则降至49.61。注意力可视化（Figure 5）进一步显示，无编码器架构的点token与文本token之间具有更强的语义关联。

本方法在物体级3D理解上验证了有效性，尚未扩展到场景级任务，且多模态训练中仍存在轻微的语言能力遗忘（MMLU 47.1% → 46.4%），需通过混合纯文本数据缓解。



三维大语言模型（3D LMMs）旨在赋予大语言模型（LLM）理解三维世界的能力，其典型架构由三个组件构成：3D 编码器、投影层和 LLM。当前主流方法普遍依赖预训练的 3D 编码器（如 Point-BERT）将点云转化为固定数量的 token，再通过投影层送入 LLM 进行多模态推理。然而，这一范式存在两个根本性瓶颈，制约了模型性能的进一步提升。

**瓶颈一：点云分辨率限制。** 预训练编码器在训练阶段固定处理 8192 个点，输出 512 个 token。当推理时输入点云密度发生变化（如降至 2048 点或升至 16384 点），编码器的 token 表示与训练分布产生不匹配，导致空间信息丢失和性能显著退化。这种训练-推理分辨率的不一致性，使模型难以灵活应对不同精度的三维输入。

**瓶颈二：嵌入语义差异。** 3D 编码器的预训练目标（如掩码点云建模）与 LLM 的语义理解需求之间存在根本性的不对齐。编码器提取的特征偏向于局部几何模式，而 LLM 需要的是高层语义概念。这种语义鸿沟使得投影层难以弥合两种模态之间的表示差异，限制了多模态对齐的效果。

上述问题源于一个共同的架构假设：3D 编码器是必不可少的中间层。这引出了一个自然的问题——能否完全移除预训练的 3D 编码器，让 LLM 自身承担 3D 编码的功能？直觉上，LLM 的深层 Transformer 结构具备强大的序列建模能力，理论上可以直接从点云 token 中学习高层语义和局部几何结构，同时消除编码器带来的分辨率依赖和语义偏差。

然而，简单地移除编码器并不可行。初步实验表明（Table 1），直接去掉 Point-BERT 编码器后，分类 GPT-4 分数从 53.00 骤降至 35.50（下降 17.5%），描述分数从 44.85 降至 33.37（下降 10.48%）。这说明 LLM 本身缺乏对原始点云 token 的有效编码机制，需要专门设计的训练策略来激发其 3D 理解潜力。

针对这一挑战，本文提出 **ENEL（Encoder-free 3D LMM）**，这是首个无编码器的三维大语言模型。ENEL 的核心思路是将原属于 3D 编码器的功能迁移到 LLM 内部，通过两个阶段的训练策略实现：在预训练阶段，采用 **LLM 内嵌语义编码**（LLM-embedded Semantic Encoding）和混合语义损失，使 LLM 的前几层直接从点云 token 中学习高层语义；在指令微调阶段，引入 **层次化几何聚合**（Hierarchical Geometry Aggregation）策略，使 LLM 能够捕捉点云的局部结构细节。这一设计从根本上规避了编码器带来的分辨率依赖和语义偏差问题，为 3D LMM 提供了一条新的技术路径。



## 核心方法与创新机理

### 问题根源：编码器带来的双重瓶颈

现有 3D 大语言模型（3D LMM）普遍依赖预训练的 3D 编码器（如 Point-BERT）将点云转换为 LLM 可理解的 token。然而，这种架构存在两个根本性瓶颈：

1. **点云分辨率限制**：编码器在训练时固定处理 8192 点并输出 512 个 token。当推理时点云密度变化，编码器无法自适应调整，导致空间信息丢失（Figure 1a）。
2. **嵌入语义差异**：编码器的预训练目标（如掩码建模）与 LLM 的语义理解需求并不对齐，使得编码器输出的 token 难以被 LLM 高效利用（Figure 1b）。

### 核心思路：让 LLM 直接承担 3D 编码

ENEL 的核心创新在于**彻底移除预训练的 3D 编码器**，将编码功能直接迁移到 LLM 内部。这一设计通过五个关键的架构变更（changed slots）实现：

#### 1. 轻量级 Token Embedding 替代重编码器

**Baseline → Proposed**：Point-BERT 预训练编码器（8192 点输入，512 token 输出）→ 3 层轻量级 Token Embedding（T.E.）模块，仅 3M 参数。

该模块通过 FPS（最远点采样）、k-NN（k 近邻）和线性层，将 8192 点压缩为 128 个高维 token。Table 1 的消融显示，移除编码器后分类和描述 GPT-4 分数分别骤降 17.5% 和 10.48%，而加入 3 层 T.E. 可大幅恢复性能，验证了轻量级替代方案的可行性。

#### 2. LLM 内嵌语义编码（Hybrid Semantic Loss）

**Baseline → Proposed**：仅文本语言建模损失 → Hybrid Semantic Loss，对 30% 掩码 token 做特征预测，对 70% 可见 token 做点云块重建。

预训练阶段，ENEL 将 LLM 的前 4 层设为可学习（Table 2），并施加混合语义损失：
- 掩码部分使用 **Masked Modeling Loss**，促使 LLM 学习局部特征：

$$\mathcal{L}_{\mathrm{mask}} = \frac{1}{M * r} \sum_{i=1}^{M * r} \left( \lVert \boldsymbol{F}_{\mathrm{pre}_i} - \boldsymbol{F}_{\mathrm{gt}_i} \rVert_2^2 \right)$$

- 可见部分使用 **Reconstruction Loss**（Chamfer 距离），保留几何结构信息：

$$\frac{1}{M} \sum_{i=1}^{M} \left( \min_j \| a_i - b_j \|_2^2 + \min_j \| b_i - a_j \|_2^2 \right), a = G_{\mathrm{pre}}, b = G$$

Table 3 表明，Hybrid Semantic Loss 达到 52.00% 分类和 47.65% 描述 GPT-4 分数，显著优于单一损失函数。移除该损失后，描述性能降至 47.15，分类降至 50.50（Table 6），证实了其关键作用。

#### 3. 层级化几何聚合（Hierarchical Geometry Aggregation）

**Baseline → Proposed**：无显式几何聚合 → 在 LLM 早期层间进行基于动态网格采样的 token 聚合，后期反向传播，集成门控自注意力。

指令微调阶段，ENEL 通过层级化几何聚合捕捉点云的局部结构。聚合操作使用动态网格采样，网格大小按累积缩放策略增长：

$$s_i = \alpha \cdot e^{\sum_{j=1}^{i} \beta_j}, \quad \beta_j = \gamma \cdot \tanh(\theta_j) + \beta_{\mathrm{ctr}}$$

门控自注意力机制通过可学习参数 α 控制注意力输出的贡献，初始为零以保证训练稳定性：

$$F_{\mathrm{input}}^{n}{}' = \tanh(\alpha) * \text{Self-Attn.}(F_{\mathrm{input}}^{n}) + F_{\mathrm{input}}^{n}$$

Table 4 的消融显示，3 层聚合操作（l=3）、2 个 LLM 层间隔（H=2）并添加自注意力获得最佳性能（分类 55.55，描述 51.03）。移除门控机制后，描述降至 49.61，分类降至 53.60（Table 6）。

#### 4. 混合分辨率训练提升鲁棒性

**Baseline → Proposed**：固定训练分辨率 8K 点 → ENEL-Mix：每批次从 2K 到 16K 随机采样。

Table 12 和 Table 13 表明，混合分辨率训练不仅提升了模型对推理分辨率变化的鲁棒性，还在标准任务上带来一致提升，消除了编码器对固定分辨率的依赖。

### 证据强度

- **决定性证据**：Figure 5 的注意力可视化显示，ENEL 的点 token 与文本 token 的语义关联显著强于编码器基线，直接验证了 LLM 内嵌语义编码的有效性。
- **性能验证**：ENEL-7B 在 Objaverse 分类（55.55）、描述（51.03）和 VQA（43.8）上，性能与 13B 编码器基线 PointLLM-PiSA 相当（Table 5），证明无编码器架构可以超越更大规模的编码器模型。



![[assets/figures/papers/iclr26_0011_22Hh0Vj5Dd_Exploring_the_Potential_of_Encoder-free_Architec/figures/005_Figure_2.jpg]]
*Figure 2: Overall Pipeline of ENEL. The training is divided into two stages: the pre-training stage and the instruction tuning stage. In the first stage, we set the first K layers to be learnable and apply the proposed Hybrid Semantic Loss to embed high-level semantics into the LLM. In the second stage, we adopt the Hierarchical Geometric Aggregation strategy to capture local structures of point clouds*

ENEL 的整体训练流水线分为两个阶段：**预训练阶段**（Pre-training）和**指令微调阶段**（Instruction Tuning），如 Figure 2 所示。两阶段的核心设计目标是将传统 3D 编码器的功能逐步迁移至 LLM 内部，从而消除对独立预训练编码器的依赖。

### 输入处理与 Token 嵌入

原始点云输入包含 8192 个点，每个点具有 6 维特征。ENEL 使用一个轻量级的 **Token Embedding 模块**（仅约 3M 参数）将点云转化为高维 token 序列。该模块通过三轮最远点采样（FPS）和 k-最近邻（k-NN）分组，将点数从 8192 逐步降至 512、256，最终得到 128 个点 token，每个 token 的维度通过线性层从 6 扩展到 288，与 LLM 的嵌入维度对齐。消融实验（Table 1）表明，3 层 Token Embedding 在分类和描述任务上均取得最佳性能——移除编码器后，直接使用单层投影会导致分类 GPT-4 分数从 53.00 骤降至 35.50（下降 17.5%），而 3 层设计可将分数恢复至 45.55。

### 阶段一：LLM 内嵌语义编码

在预训练阶段，ENEL 将 LLM 的**前 4 层设为可学习**（Table 2），使其承担类似编码器的角色，负责捕捉点云 token 间的全局交互。同时，ENEL 提出 **Hybrid Semantic Loss**，为点云 token 提供自监督信号：对 30% 的掩码 token 进行特征预测（Masked Modeling），对 70% 的可见 token 进行点云块重建（Reconstruction）。Table 3 显示，该混合损失在分类（52.00%）和描述（47.65%）任务上显著优于单一的掩码建模（48.5%/45.85%）或重建损失（50.00%/47.33%）。

### 阶段二：层级几何聚合

在指令微调阶段，ENEL 引入 **Hierarchical Geometry Aggregation** 策略（Figure 4），通过在 LLM 早期层间插入聚合与传播操作来捕获点云的局部几何结构。具体而言，点 token 经过动态网格采样（Dynamic Grid Sampling）分组后，在组内使用**门控自注意力**（Gated Self-Attention）进行交互，再通过均值池化聚合为更紧凑的表示；随后通过反向传播操作将聚合信息扩散回原始 token 分布。门控机制通过可学习参数 $\alpha$（初始化为零）控制自注意力输出的贡献：

$$F_{\text{input}}^{n}{}' = \tanh(\alpha) * \text{Self-Attn.}(F_{\text{input}}^{n}) + F_{\text{input}}^{n}$$

Table 4 的消融表明，使用 3 层聚合操作（$l=3$）、2 个 LLM 层间隔（$H=2$）并添加门控自注意力，可获得最优的分类（55.55%）和描述（51.03%）性能。

### 数据流与模块关系

整体数据流可概括为：**原始点云 → Token Embedding（FPS + k-NN + 线性层，128 tokens）→ LLM 前 4 层（可学习，全局交互）→ 层级几何聚合（局部结构捕获）→ LLM 后续层（多模态推理）→ 文本输出**。预训练阶段仅优化前 4 层 LLM 和 Token Embedding，指令微调阶段则额外引入几何聚合模块，两者协同使 ENEL-7B 在 Objaverse 分类（55.55）、描述（51.03）和 3D VQA（43.8）任务上达到甚至超越 13B 编码器基线的性能（Table 5）。



### 3.1 点云Token嵌入模块（Token Embedding Module）

该模块是ENEL中唯一专门为点云设计的前处理网络，参数量仅约3M，远小于传统预训练编码器（如Point-BERT）。其作用是将原始点云转换为LLM可直接处理的token序列。

**处理流程：** 输入为8192个点的点云，每个点包含3维坐标和3维RGB值（共6维）。首先通过线性层将维度从6扩展到288。随后经过三次最远点采样（FPS）和k近邻（k-NN）聚合，逐步将点数从8192降至512、256，最终得到128个高维token，记为 $\{F_i\}_{i=1}^{M} \in \mathbb{R}^{M \times D_1}$，其中 $M=128$。

**关键设计选择：** Table 1的消融实验表明，3层token embedding结构在分类和描述任务上均取得最优性能（GPT-4分类45.55，描述41.36）。直接移除编码器会导致分类GPT-4分数从53.00骤降至35.50（下降17.5%），描述从44.85降至33.37（下降10.48%），而加入3层T.E.模块可大幅恢复性能，验证了该轻量级设计的有效性。

### 3.2 LLM内嵌语义编码与混合语义损失（Hybrid Semantic Loss）

预训练阶段的核心创新在于让LLM的前4层承担编码功能，并通过混合语义损失为点云token提供自监督学习信号。该损失结合了两种互补的预训练目标：

**掩码建模损失（Masked Modeling Loss）：** 对30%的点token进行掩码，要求LLM预测被掩码token的特征表示，损失函数为预测特征 $\boldsymbol{F}_{\mathrm{pre}_i}$ 与真实特征 $\boldsymbol{F}_{\mathrm{gt}_i}$ 之间的均方误差：

$$\mathcal{L}_{\mathrm{mask}} = \frac{1}{M \cdot r} \sum_{i=1}^{M \cdot r} \left( \lVert \boldsymbol{F}_{\mathrm{pre}_i} - \boldsymbol{F}_{\mathrm{gt}_i} \rVert_2^2 \right)$$

其中 $r$ 为掩码比例（0.3），$M$ 为token总数。该损失促使LLM学习点云的局部语义特征。

**重建损失（Reconstruction Loss）：** 对剩余70%的可见token，要求LLM重建对应的点云块几何结构，采用Chamfer距离作为度量：

$$\frac{1}{M} \sum_{i=1}^{M} \left( \min_j \| a_i - b_j \|_2^2 + \min_j \| b_i - a_j \|_2^2 \right), \quad a = G_{\mathrm{pre}}, \; b = G$$

其中 $G_{\mathrm{pre}}$ 为LLM预测的点云块，$G$ 为真实点云块。该损失确保LLM保留点云的几何结构信息。

**设计依据：** Table 3系统比较了不同自监督损失的效果。纯掩码建模（30%掩码率）取得分类49.00、描述45.20的GPT-4分数；纯重建损失取得分类48.00、描述44.46。而混合语义损失（feat目标，即掩码部分做特征预测）将分类提升至52.00、描述提升至47.65，显著优于单一损失。消融实验（Table 6）进一步证实，移除混合语义损失后描述GPT-4从51.03降至47.15，分类从55.55降至50.50。

### 3.3 层级化几何聚合策略（Hierarchical Geometry Aggregation）

在指令微调阶段，ENEL通过层级化几何聚合策略为LLM注入局部几何结构的归纳偏置。该策略在LLM的早期层间交替执行聚合（aggregation）和传播（propagation）操作。

**动态网格采样（Dynamic Grid Sampling）：** 在第 $i$ 次聚合操作中，网格大小 $s_i$ 采用累积缩放策略：

$$s_i = \alpha \cdot e^{\sum_{j=1}^{i} \beta_j}, \quad \beta_j = \gamma \cdot \tanh(\theta_j) + \beta_{\text{ctr}}$$

其中 $\alpha$、$\gamma$、$\theta_j$ 和 $\beta_{\text{ctr}}$ 均为可学习参数。该设计使网格大小随聚合层数自适应调整，逐步捕获不同尺度的局部结构。

**门控自注意力（Gated Self-Attention）：** 在每个网格单元内，对点token应用自注意力以捕获局部几何交互，并通过门控机制自适应控制注意力输出的贡献：

$$F_{\mathrm{input}}^{n}{}' = \tanh(\alpha) * \text{Self-Attn.}(F_{\mathrm{input}}^{n}) + F_{\mathrm{input}}^{n}$$

其中 $\alpha$ 为可学习参数，初始化为零以保证训练初期的稳定性。随后对融合后的特征进行均值池化得到聚合token：

$$F_{\mathrm{agg}}^{i} = \text{MeanPooling}(F_{\mathrm{input}}^{n}{}')$$

聚合后的token经过若干LLM层处理后，通过反向传播操作恢复至原始token分布，确保后续LLM层能继续处理完整的token序列。

**关键消融发现（Table 4）：** 使用3次聚合操作（$l=3$）、聚合与传播操作间间隔2个LLM层（$H=2$）并加入门控自注意力，取得最佳性能（分类55.55，描述51.03）。移除门控机制后描述降至49.61、分类降至53.60（Table 6），验证了门控自注意力对局部几何建模的关键作用。



## 实验与关键发现

### 核心瓶颈验证：编码器移除的影响

为验证预训练编码器带来的分辨率限制与语义差异问题，Table 1 给出了直接移除编码器后的性能变化。以 PointLLM-7B 为基线，移除其 Point-BERT 编码器后，分类 GPT-4 分数从 53.00 骤降至 35.50（降幅 17.5%），描述 GPT-4 分数从 44.85 降至 33.37（降幅 10.48%）。这一断崖式下降表明，编码器并非可选的附属模块——直接丢弃编码器会导致 LLM 无法从原始点云 token 中提取有效语义。


![[assets/figures/papers/iclr26_0011_22Hh0Vj5Dd_Exploring_the_Potential_of_Encoder-free_Architec/figures/003_Table_1.jpg]]
*Table 1: Token Embedding. Performance on Objaverse with PointLLM-7B as the baseline. ‘Cls’/‘Cap’: classification/captioning tasks. ‘Avg’: accuracy under prompts “What is this?" and “This is an object of." ‘S-BERT’: Sentence-BERT. ‘T.E.’: our designed token embedding module*

ENEL 的核心设计正是针对这一瓶颈：用仅 3M 参数的 3 层轻量级 Token Embedding（T.E.）模块替代重编码器，使分类恢复至 45.55，描述恢复至 41.36。该模块仅依赖 FPS、k-NN 和线性层进行点云到 token 的投影，不引入预训练语义偏差。

### 预训练损失设计：混合语义损失的有效性

Table 3 系统对比了不同自监督损失在无编码器架构下的表现。关键发现：


![[assets/figures/papers/iclr26_0011_22Hh0Vj5Dd_Exploring_the_Potential_of_Encoder-free_Architec/figures/007_Table_3.jpg]]
*Table 3: LLM-embedded Semantic Encoding. In pre-training, we explore the effects of different self-supervised learning losses targeting point tokens. Ψ and Φ denote mask ratios of 60% and 30%, respectively. Subscripts patch and feat indicate loss targets. For Hybrid Semantic Loss, the subscripts patch and feat refer to the masked modeling target, with reconstruction targeting the corresponding feat and patch*

- **掩码建模损失**（Masked Modeling Loss）在 30% 掩码率下取得分类 49.00、描述 45.20 的 GPT-4 分数，优于 60% 掩码率（47.00 / 43.64），说明适度的掩码比例对 LLM 学习点云特征至关重要。
- **重建损失**（Reconstruction Loss）单独使用时表现较弱（分类 46.00，描述 42.42），但其关注点云几何结构的特性与掩码建模形成互补。
- **对比损失**（Contrastive Loss）和**知识蒸馏损失**（Knowledge Distillation Loss）在无编码器场景下均不及掩码建模，表明直接对齐全局表征的方式难以替代局部特征学习。

ENEL 提出的**混合语义损失**（Hybrid Semantic Loss）将两者结合：对 30% 掩码 token 做特征预测（$\mathcal{L}_{\mathrm{mask}}$），对 70% 可见 token 做点云块重建（Chamfer 距离）。该设计在分类（52.00）和描述（47.65）上均显著优于单一损失，验证了“语义特征学习 + 几何结构保留”双目标的必要性。

### 层级几何聚合策略的消融

Table 4 展示了指令微调阶段层级几何聚合（Hierarchical Geometry Aggregation）的消融结果。该策略通过在 LLM 前几层间插入聚合-传播操作，使点 token 在局部邻域内交互，捕捉细粒度几何结构。


![[assets/figures/papers/iclr26_0011_22Hh0Vj5Dd_Exploring_the_Potential_of_Encoder-free_Architec/figures/009_Table_4.jpg]]
*Table 4: Hierarchical Geometry Aggregation. In the instruction tuning stage, we conduct the experiments of Hierarchical Geometry Aggregation strategy. l represents the number of aggregation and propagation operations. H refers to the LLM layers between l aggregation and l propagation operations. + Self-Attn. represents the incorporation of the gated self-attention in the aggregation*

- **聚合层数 $l$**：$l=3$ 时分类达 55.55、描述达 51.03，优于 $l=1$（54.10 / 49.40）和 $l=4$（54.80 / 50.08），表明适度的层次深度能平衡局部细节与全局上下文。
- **LLM 层间隔 $H$**：$H=2$ 表现最佳（55.55 / 51.03），$H=8$ 时性能下降（54.55 / 49.65），说明聚合操作应密集分布在早期编码层，而非分散到深层。
- **门控自注意力**（Gated Self-Attention）：添加门控机制后，分类从 54.75 提升至 55.55，描述从 50.02 提升至 51.03。门控参数 $\alpha$ 初始为零，通过 $\tanh(\alpha)$ 自适应控制自注意力输出的贡献，确保训练初期稳定性。

### 主要结果：与编码器基线的全面对比

Table 5 汇总了 ENEL 与主流编码器基线的性能对比。在 Objaverse 基准上：


![[assets/figures/papers/iclr26_0011_22Hh0Vj5Dd_Exploring_the_Potential_of_Encoder-free_Architec/figures/010_Table_5.jpg]]
*Table 5: Comparison of different models on various 3D understanding tasks. A primary focus is placed on GPT-4 evaluation, along with data-driven metrics (Sentence-BERT). The * indicates the Qwen2.5-7B LLM base and the ShapeLLM training data. The α denotes reproduced results. † denotes the model is implemented based on the ShapeLLM baseline*

| 模型 | 参数量 | 描述 GPT-4 | 分类 GPT-4 | 3D-VQA GPT-4 |
|------|--------|-----------|-----------|-------------|
| PointLLM-7B | 7B | 44.85 | 53.00 | 41.20 |
| PointLLM-PiSA-13B | 13B | 48.70 | 54.90 | 42.00 |
| **ENEL-7B** | **7B** | **51.03** | **55.55** | **43.80** |

ENEL-7B 以 7B 参数规模在全部三项任务上超越 PointLLM-7B，描述任务提升尤为显著（+6.18）。更关键的是，ENEL-7B 在描述和分类上均超越了 13B 的 PointLLM-PiSA-13B，证明无编码器架构并非以牺牲性能为代价——相反，消除编码器带来的语义偏差和分辨率限制后，LLM 能更直接地从点云中学习有效表征。

在 ModelNet40 分类（Table 8）上，ENEL-7B 以 54.26% 的平均准确率超越 PointLLM-7B（52.63%）和 ShapeLLM-7B（53.08%），进一步验证了跨基准的泛化性。

### 关键组件消融：各模块的独立贡献

Table 6 通过逐一移除 ENEL 的核心组件，量化各模块的贡献：


![[assets/figures/papers/iclr26_0011_22Hh0Vj5Dd_Exploring_the_Potential_of_Encoder-free_Architec/figures/018_Table_6.jpg]]
*Table 6: Ablation Experiments. We begin the ablation experiments by changing the single configuration of the module from ENEL. Ψ and Φ denote mask ratios of 60% and 30%, respectively. For Hybrid Semantic Loss, the subscripts patch and feat refer to the masked modeling target, with reconstruction targeting the corresponding feat and patch. l represents the number of aggregation and propagation operations. H refers to the LLM layers between l aggregation and l propagation operations. O refers to the LLM layer between two individual aggregation or propagation operations*

- **移除混合语义损失**：描述从 51.03 降至 47.15（-3.88），分类从 55.55 降至 50.50（-5.05），降幅最大，证明预训练自监督信号是 LLM 编码能力的核心来源。
- **移除门控机制**：描述降至 49.61（-1.42），分类降至 53.60（-1.95），表明门控自注意力对局部几何建模不可或缺。
- **掩码目标从特征切换为点云块**：描述降至 50.00，分类降至 54.40，说明特征级预测比几何重建更适合 LLM 的语义学习。
- **掩码率从 30% 调至 60%**：描述降至 48.66，分类降至 53.10，进一步确认 30% 掩码率在特征预测场景下的最优性。

### 计算效率与分辨率鲁棒性

Table 7 对比了 ENEL-7B 与 PointLLM-7B 的计算开销。ENEL 在预训练阶段减少 29.7% 训练时间、16.4% 显存占用和 20.5% FLOPs，收敛所需步数也减少 25.3%。效率提升源于移除了重编码器的前向/反向计算。

Table 12 展示了推理分辨率鲁棒性。PointLLM-7B 在训练分辨率（8K）下描述 GPT-4 为 44.85，但降至 2K 时骤降至 30.43——编码器对输入点密度高度敏感。ENEL-7B 在 2K 下仍保持 42.04，且混合分辨率训练（ENEL-Mix）进一步将 2K 性能提升至 44.56。Table 13 表明 ENEL-Mix 在标准任务上也带来一致提升，验证了数据多样性不会牺牲绝对性能。

### 注意力可视化：语义编码的本质差异

Figure 5 通过可视化文本 token 对点 token 的平均注意力分数，揭示了编码器基线与无编码器架构在语义编码上的本质差异。编码器基线中，注意力分布较为分散且强度较低，表明 LLM 难以从编码器输出的 token 中提取与文本语义直接相关的信息。ENEL 中，注意力更集中于语义相关的点区域，且强度更高——这直接验证了“LLM 内嵌语义编码”的核心假设：让 LLM 直接处理点云 token，能建立更强的跨模态语义关联。

### 灾难性遗忘的缓解

Table 10 显示，直接进行多模态指令微调会导致 MMLU 从原始 Vicuna-7B 的 47.1% 降至 46.4%。在指令微调数据中混入 12K 纯文本样本后，MMLU 恢复至 47.3%，略超原始水平。这表明适度的文本数据混合能有效缓解 LLM 在多模态训练中的语言能力退化，且不会损害 3D 理解性能。

### 失败模式与局限

1. **场景级 3D 理解的缺失**：当前 ENEL 仅在物体级基准（Objaverse, ModelNet40）上验证，尚未扩展到场景级任务。物体级点云通常具有完整几何，而场景级点云存在遮挡、稀疏和不规则分布，无编码器架构能否直接泛化尚需验证。

2. **混合语义损失的超参数敏感性**：Table 14 显示，$\lambda_{\text{mask}}$ 和 $\lambda_{\text{recon}}$ 的极端取值会导致性能明显下降，对比温度 $\tau$ 也需仔细调节。这增加了在不同数据分布下的调参成本。

3. **LLM 层数的可学习性权衡**：Table 2 表明，可学习层数从 4 层增加到 8 层或 12 层时性能反而下降（分类从 47.50 降至 46.75），说明过多的可学习层可能破坏 LLM 原有的语言能力。这一权衡在大规模 LLM 上可能更为显著。



## 定位与知识库关联

### 与编码器基线的根本差异

ENEL 与现有 3D LMM 的核心分歧在于**是否保留独立的预训练 3D 编码器**。以 PointLLM 为代表的编码器基线采用“编码器-投影-LLM”三段式架构：Point-BERT 将 8192 点压缩为 512 个 token，经投影层送入冻结的 Vicuna-7B。这一设计带来两个结构性瓶颈：(1) **分辨率锁死**——训练时固定 8K 点输入，推理时改变点密度会导致空间信息丢失（Figure 1a）；(2) **语义偏差**——编码器的预训练目标（掩码点云建模）与 LLM 的语义需求不对齐，导致嵌入空间存在系统性差异（Figure 1b）。

ENEL 的应对策略是**将编码功能迁移至 LLM 内部**，仅保留一个 3 层、约 3M 参数的轻量级 Token Embedding 模块（基于 FPS、k-NN 和线性层），将原始点云转化为 128 个高维 token 后直接送入 LLM。Table 1 的消融实验直接量化了这一迁移的代价与收益：完全移除编码器使分类 GPT-4 分数从 53.00 骤降至 35.50（-17.5%），描述从 44.85 降至 33.37（-10.48%）；但加入 3 层 Token Embedding 即可将分类恢复至 45.55，描述恢复至 41.36，证明 LLM 本身具备承担编码功能的潜力。

### 与 ShapeLLM 的架构适配验证

为排除 ENEL 对特定编码器基线的过拟合，作者在 ShapeLLM 框架上复现了无编码器变体 ENEL†。ShapeLLM 采用不同的编码器架构和训练数据，但 ENEL† 在 Objaverse 描述任务上达到 54.78 GPT-4 分数，超过其编码器版本 ShapeLLM-7B（Table 5）。这一跨框架验证表明，无编码器设计并非 PointLLM 的特例，而是一种**可泛化的架构选择**。

### 两阶段训练范式的设计逻辑

ENEL 的训练分为预训练和指令微调两个阶段，每个阶段解决编码器移除后暴露的不同问题：

**预训练阶段——LLM 内嵌语义编码**。编码器移除后，LLM 失去了点云自监督信号的来源。ENEL 通过 Hybrid Semantic Loss 填补这一空缺：对 30% 的掩码 token 做特征预测（MSE 损失，Eq. 1），对 70% 的可见 token 做点云块重建（Chamfer 距离，Eq. 2）。Table 3 的系统对比表明，单一损失均无法达到最优——掩码建模（48.5% 分类 / 45.85% 描述）和重建（49.5% / 46.10%）各有侧重，而混合损失（52.00% / 47.65%）实现了互补。这一发现揭示了一个关键机制：**高层语义和局部几何结构需要不同的自监督目标来诱导**，单一损失会导致信息偏置。

**指令微调阶段——层次化几何聚合**。预训练后的 LLM 对点云的局部几何结构仍不够敏感。ENEL 在早期 LLM 层间插入层次化几何聚合操作（Figure 4）：通过动态网格采样（网格尺寸按 $s_i = \alpha \cdot e^{\sum_{j=1}^{i} \beta_j}$ 累积缩放）将点 token 分组，组内应用门控自注意力（$F_{\text{input}}^{n}{}' = \tanh(\alpha) * \text{Self-Attn.}(F_{\text{input}}^{n}) + F_{\text{input}}^{n}$）捕捉局部结构，聚合后再通过反向传播恢复原始 token 分布。Table 4 的消融确定了最优配置：3 层聚合（l=3）、2 个 LLM 层间隔（H=2）、启用门控自注意力，此时分类达到 55.55，描述达到 51.03。

### 适用边界与已知局限

**任务边界**。当前 ENEL 仅在物体级 3D 理解基准（Objaverse、ModelNet40）上验证，尚未扩展到场景级任务（如 3D 室内问答、场景理解）。物体级点云的结构复杂度远低于场景级，层次化几何聚合在密集、大规模点云上的有效性需独立验证。

**语言能力保持**。多模态训练会侵蚀 LLM 的通用语言能力。ENEL 在指令微调中混入 12K 纯文本样本后，MMLU 从 46.4% 恢复至 47.3%，略超原始 Vicuna-7B 的 47.1%（Table 10），表明灾难性遗忘可缓解但未根除。

**超参数敏感性**。Hybrid Semantic Loss 的掩码比例（30% vs 60%）、损失权重（λ_mask, λ_recon）以及对比温度 τ 对性能影响显著。Table 3 显示 60% 掩码比例使分类从 49.00% 降至 47.00%，描述从 45.20% 降至 43.64%。这些参数目前依赖经验调节，缺乏自动化或理论指导。

**分辨率鲁棒性的代价**。混合分辨率训练（ENEL-Mix，每批次从 2K 到 16K 随机采样）提升了推理分辨率变化的鲁棒性（Table 12），但这一策略本质上是数据增强，并未从架构层面解决分辨率不变性问题。

### 开放问题

1. **场景级扩展**：层次化几何聚合能否直接迁移到场景级点云（>10^5 点），还是需要引入稀疏注意力或层次化分区机制？
2. **更大规模验证**：当前实验基于 7B/13B 的 LLaMA/Vicuna 和 Objaverse 数据集。在更大规模 LLM（如 70B+）和更大规模 3D 数据集上的可扩展性尚未验证。
3. **损失函数统一**：Hybrid Semantic Loss 本质上是两个独立损失的线性组合。是否存在更统一的点云-语言对齐目标，能同时捕获语义和几何信息？
4. **多表示泛化**：无编码器框架目前仅针对点云设计。能否将相同的“LLM 内嵌编码”思路应用于体素、网格或神经场等其他 3D 表示？Token Embedding 模块需要如何适配？



## 原文 PDF

![[paperPDFs/ICLR_2026/Exploring_the_Potential_of_Encoder_free_Architectures_in_3D_LMMs.pdf]]
