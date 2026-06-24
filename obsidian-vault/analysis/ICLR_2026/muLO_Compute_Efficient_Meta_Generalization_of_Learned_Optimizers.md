---
title: "$\\mu$LO: Compute-Efficient Meta-Generalization of Learned Optimizers"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/muLO_Compute_Efficient_Meta_Generalization_of_Learned_Optimizers.pdf
aliases:
- MLCEMGLO
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/learning_for_optimization
core_operator: "优化器更新缩放、初始化方差和前激活乘数对网络宽度的依赖关系。标准参数化（SP）未正确缩放这些量，导致宽网络中的前激活爆炸和更新不稳定。最大更新参数化（µP）通过引入与扇入（FAN_IN）相关的缩放因子来修正这些依赖关系。"
primary_logic: "将最大更新参数化（µP）应用于学习型优化器架构（small_fc_lopt和VeLO），并采用多宽度元训练策略，可以在不增加计算成本的情况下，显著提升LO对更宽、更深以及更长训练步数任务的元泛化能力。"
claims:
- "µLO在更宽任务上持续获得最佳或次佳平均排名，而SP LO则失败或发散。"
- "µLO在训练步数长达元训练25倍的任务上仍能稳定降低损失，而SP LO则发散或停滞。"
- "µP下的模型前激活在不同宽度上保持稳定，而SP下的模型在宽网络中前激活会爆炸。"
- "多宽度元训练（µLO_M）优于单宽度元训练（µLO_S），尤其是在更宽和更长步数的任务上。"
---

# $\mu$LO: Compute-Efficient Meta-Generalization of Learned Optimizers

> [!tip] 核心洞察
> 将最大更新参数化（µP）应用于学习型优化器架构（small_fc_lopt和VeLO），并采用多宽度元训练策略，可以在不增加计算成本的情况下，显著提升LO对更宽、更深以及更长训练步数任务的元泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | µLO：学习型优化器的计算高效元泛化 |
| 英文题名 | $\mu$LO: Compute-Efficient Meta-Generalization of Learned Optimizers |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=f8z2bzOLK2); [GitHub](https://github.com/bentherien/mu_learned_optimization) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/learning_for_optimization |
| Method | µLO（µ-参数化学习型优化器） |
| Dataset | MLP IN32 (ImageNet-32), MLP IN32 (ImageNet-32) W=8192, MLP C10 (CIFAR-10) W=8192, LM (LM1B) W=4096 |

> [!tip] 效果简介
> - MLP IN32 (ImageNet-32) 上，平均排名 为 µLO_M: 1.80 (Large, 1k), 2.00 (XL, 1k), 2.00 (XXL, 1k)，对比 SP LO_M: 排名较低（具体值未在文本中给出，但明确被µLO超越），变化 µLO_M在所有规模上均获得最佳或次佳排名。
> - MLP IN32 (ImageNet-32) W=8192 上，训练损失 为 µLO_M 和 µVeLO_M 达到更低损失，对比 AdamW 和 µAdam 损失较高，变化 µLOs 优于调优后的手设计基线。
> - MLP C10 (CIFAR-10) W=8192 上，训练损失 为 µLOs 匹配或超越最强基线，对比 AdamW 和 µAdam，变化 µLOs 达到或超过手设计基线性能。

## 概述

学习型优化器（Learned Optimizers, LOs）旨在通过元学习自动发现高效的优化规则，以替代手工设计的优化器（如AdamW）。然而，现有LO面临一个根本性瓶颈：**元泛化（meta-generalization）能力严重不足**。当被用于优化比元训练阶段所见网络更宽（隐藏维度更大）的网络时，即使经过大规模元训练（如VeLO使用4000 TPU月），标准参数化（Standard Parametrization, SP）下的LO仍会失败或发散。

本文的核心洞察在于，该问题的根源是**优化器更新、初始化方差与前激活乘数对网络宽度的依赖关系未被正确缩放**。标准参数化（SP）未处理这些依赖，导致宽网络中的前激活爆炸和更新不稳定。作者将最大更新参数化（Maximal Update Parametrization, µP）系统地应用于两种主流LO架构（`small_fc_lopt` 和 VeLO），并提出了一个简单的多宽度元训练策略，由此得到µ-参数化学习型优化器（µLO）。

方法定位上，µLO并非提出新的LO架构，而是**通过改变优化器（optimizee）的参数化方案和元训练分布，在不增加计算成本的前提下，从根本上修复LO的宽度外推失败问题**。具体改动包括：将隐藏层的优化器更新除以扇入（FAN_IN）；对隐藏层和输入层采用 $\\mathcal{N}(0, 1/\\mathrm{FAN\\_IN})$ 初始化，输出层采用 $\\mathcal{N}(0, 1)$；在前向传播中将输出层前激活乘以 $1/\\mathrm{FAN\\_IN}$；并在元训练时使用包含多宽度（128、512、1024）的任务分布。

主要结果令人信服。在跨宽度（最高至8192）、跨深度（5倍于元训练深度）和跨训练步数（25倍于元训练步数）的大规模评估中，µLOs在所有分布外任务上**持续获得最佳或次佳平均排名**（Table 1），而SP LOs则发散或停滞。在MLP任务上，µLOs甚至超越了经过每任务超过500种配置调优的AdamW和µAdam基线。在远分布外的语言模型（LM）和视觉Transformer（ViT）任务上，µLOs也接近或匹配了调优后的手设计基线。关键证据显示（Figure 2），µP下的模型前激活在不同宽度上保持稳定，而SP下的宽网络前激活会爆炸，这直接验证了因果机制。

## 背景与动机

学习型优化器（Learned Optimizers, LOs）旨在通过元学习自动发现高效的优化规则，从而显著降低神经网络的训练时间。然而，一个根本性的瓶颈长期阻碍着它们的实际部署：**元泛化能力严重不足**。具体而言，当LO被要求优化比其在元训练阶段所见网络更宽（即隐藏层维度更大）的网络时，其性能会急剧下降甚至完全失效。这种对网络宽度的脆弱性，使得即使经过大规模计算资源（例如VeLO使用了4000 TPU月）训练的LO，在面对更宽模型时也无法保持有效性能，这构成了现有方法的核心缺口。

该问题的根本原因在于标准参数化（Standard Parametrization, SP）对优化器更新、初始化方差以及前激活值在宽度变化时的缩放关系处理不当。在SP下，随着网络宽度增加，前激活值的尺度会失控地增长（即“爆炸”），导致优化过程不稳定。具体而言，SP未能正确建立更新步长与网络扇入（FAN_IN）之间的依赖关系，使得宽网络中的参数更新幅度与激活值尺度失配，最终引发训练发散或停滞。

针对这一瓶颈，本文的核心动机在于：**将最大更新参数化（Maximal Update Parametrization, µP）引入学习型优化器的架构与元训练流程**，以从根本上修复上述缩放问题。µP通过引入与FAN_IN相关的缩放因子，修正了隐藏层的更新幅度（将更新除以FAN_IN）、初始化方差（隐藏层使用$\mathcal{N}(0, 1/\mathrm{FAN_IN})$）以及前激活乘数（输出层前激活乘以$1/\mathrm{FAN_IN}$），从而确保不同宽度下模型前激活的坐标尺度保持稳定（如Figure 2所示）。这一参数化方案是解决LO宽度外推失败的关键因果杠杆。

基于此，本文提出µLO（µ-参数化学习型优化器）方法，其核心包含两个改变：1）对两种主流LO架构（small_fc_lopt和VeLO）应用µP；2）采用多宽度元训练策略（即在宽度为128、512、1024的MLP任务上联合训练），以进一步提升对未见宽度的泛化能力。这一设计旨在以零额外计算开销的方式，显著增强LO对更宽、更深以及更长训练步数任务的元泛化能力，从而弥合学习型优化器与手工设计优化器（如调优后的AdamW和µAdam）之间的性能差距。

## 核心创新

µLO的核心创新在于将**最大更新参数化（µP）** 系统性地应用于学习型优化器（LO）架构，并辅以**多宽度元训练策略**，从而在不增加计算成本的前提下，根本性地解决了LO在元泛化上的瓶颈——即优化比元训练时所见网络更宽、更深或训练步数更长的任务时性能崩溃的问题。

**根本瓶颈与因果机制：** LO在标准参数化（SP）下失败的根本原因是，其更新规则、初始化方差和前激活乘数未针对网络宽度进行正确缩放。这导致当优化器被应用于更宽的优化目标（optimizee）时，前激活值会爆炸，更新变得不稳定。µP通过引入与扇入（FAN_IN）相关的缩放因子，修正了这些依赖关系，使得模型在不同宽度下的坐标保持稳定。

**具体改变的插槽（Changed Slots）：**

1.  **优化器更新缩放：** 对于优化目标的隐藏层，µLO将SP下的更新规则 $w_t = w_{t-1} - \alpha_W \lambda_1 d \exp(\lambda_2 m)$ 修改为 $w_t = w_{t-1} - \frac{1}{\mathrm{FAN\_IN}} \cdot (\alpha_{w_l} \lambda_1 d \exp(\lambda_2 m))$，即除以扇入。对于输入和输出层，更新保持不变。
2.  **优化器初始化：** 隐藏层和输入层的权重初始化为 $\mathcal{N}(0, \frac{1}{\mathrm{FAN\_IN}})$，而输出层初始化为 $\mathcal{N}(0, 1)$。这与SP下未按层类型区分的初始化不同。
3.  **前激活乘数：** 在前向传播中，输出层的前激活乘以 $\frac{1}{\mathrm{FAN\_IN}}$，而SP下无此缩放。
4.  **元训练任务分布：** 将元训练任务从单一宽度（如宽度512）扩展为**多宽度**（如宽度128、512、1024）。实验证据（Figure 3）明确表明，多宽度元训练的µLO（µLO_M）在更宽和更长步数的任务上均显著优于单宽度元训练的µLO（µLO_S）。

**核心洞察与证据强度：** 这些修改共同作用，使得µLO在多个维度上展现了远超SP LO的元泛化能力。决定性证据如下：
- **宽度泛化（Table 1, Figure 4）：** µLO（µLO_M和µVeLO_M）在宽度高达8192的MLP、ViT和LM等大规模任务上，持续获得最佳或次佳的平均排名，而SP LO则失败或发散。在MLP IN32 W=8192任务上，µLO甚至超越了经过每任务超过500种配置调优的强手设计基线（AdamW, µAdam）。
- **深度泛化（Figure 5）：** µLO在深度为元训练5倍的任务上展现出改进的泛化能力，而SP LO性能下降。
- **训练步数泛化（Figure 6）：** µLO能够无缝泛化到长达元训练步数25倍（25,000步）的任务上，稳定降低损失。相比之下，最佳SP LO要么无法降低损失，要么在训练后期发散。

**方法组成：** 该方法的核心模块包括：两种LO架构（`small_fc_lopt`和`VeLO`）、应用于优化目标的`µ-参数化（µP）`方案，以及`多宽度元训练策略`。值得注意的是，µP的理论保证主要针对宽度缩放，其对深度和训练步数的泛化提升是纯经验性的，这是一个明确的局限性。

## 整体框架

µLO 的完整管线由两个核心模块构成：**µ-参数化（µP）方案** 和 **多宽度元训练策略**。这两个模块分别作用于优化器（optimizee）的初始化/更新规则和元训练阶段的任务分布，共同解决了标准参数化（SP）下学习型优化器在宽度外推时的根本性失败。

**模块关系与输入输出流：**

1.  **µ-参数化模块（µP）**：这是核心的“瓶颈修复”模块。其输入是原始的学习型优化器架构（`small_fc_lopt` 或 `VeLO`）及其待优化的目标网络（optimizee）。µP 模块通过修改 optimizee 的三个关键“旋钮”来改变其行为：
    *   **初始化方差**：隐藏层和输入层权重初始化为 $\mathcal{N}(0, \frac{1}{\mathrm{FAN\_IN}})$，输出层初始化为 $\mathcal{N}(0, 1)$。这确保了不同宽度的网络在初始时刻具有一致的前激活尺度。
    *   **前激活乘数**：在前向传播中，输出层的前激活乘以 $\frac{1}{\mathrm{FAN\_IN}}$。这防止了输出随宽度增加而爆炸。
    *   **优化器更新缩放**：对于隐藏层，学习型优化器生成的更新被重新缩放为 $w_t = w_{t-1} - \frac{1}{\mathrm{FAN\_IN}} \cdot (\alpha_{w_l} \lambda_1 d \exp(\lambda_2 m))$。对于输入/输出层，更新保持不变。这是最关键的一步，它确保了更新步长不会随宽度增加而失控。

    该模块的输出是一个“µ-参数化后的 optimizee”实例，其前激活在不同宽度下保持稳定（如 Figure 2 所示：µP 模型的前激活坐标标准差随宽度稳定，而 SP 模型在宽网络中爆炸）。这个模块不引入额外的计算成本。

2.  **多宽度元训练策略模块**：这是“数据分布”层面的改进。其输入是元训练任务分布。传统方法（SP LO）使用单一宽度的任务进行元训练。µLO 的策略是使用**包含多种宽度**（例如 128、512、1024）的 MLP 任务进行元训练。该模块的输出是一个经过多宽度任务训练后的 µ-参数化学习型优化器（µLO_M）。实验表明（Figure 3），多宽度训练（µLO_M）在更宽和更长步数的任务上均显著优于单宽度训练（µLO_S），这表明任务分布的多样性是提升元泛化能力的另一个关键杠杆。

**整体管线流程：**
1.  初始化一个学习型优化器（如 `small_fc_lopt` 或 `VeLO`）。
2.  在元训练阶段，对于每个元训练任务（一个 MLP），使用 µP 模块对目标网络进行参数化。
3.  使用多宽度任务分布作为元训练数据，训练该学习型优化器。
4.  最终的产出是 µLO（µ-参数化学习型优化器），它可以在未见过的、更宽、更深、更长训练步数的任务上直接使用，无需额外调参。

**与其他方法的对比：**
*   **SP LO（基线）**：使用标准参数化，未修改初始化/更新缩放，通常使用单宽度任务元训练。在宽网络上前激活爆炸，更新不稳定，导致发散或停滞。
*   **µAdam / AdamW（手设计基线）**：是强基线，在每项任务上进行了超过 500 种配置的网格搜索调优。µLO 在宽网络任务上的平均排名（Table 1）持续超越这些基线，尽管 µLO 仅在 MLP 任务上元训练过。

**局限性提醒：** µP 的理论保证仅针对宽度缩放。µLO 在深度和训练步数上的泛化能力是纯经验性的，缺乏严格的理论支撑。此外，实验仅在 MLP、ViT 和 LM 三种任务上进行，其通用性有待更广泛的验证。

## 核心模块与公式推导

### 学习型优化器基础与元学习目标

学习型优化器（LO）的核心思想是使用一个参数化的神经网络（优化器网络）来替代手工设计的优化规则（如 Adam）。给定一个待优化的目标网络（optimizee），LO 的目标是学习一个更新规则，使得 optimizee 在训练步数内能快速降低损失。其标准元学习目标函数为：

$$\underset { \phi } { \operatorname* { m i n } } \ \mathbb { E } _ { ( \mathcal { D } , \mathcal { L } , w _ { 0 } ) \sim \mathcal { T } } \left[ \mathbb { E } _ { ( X , Y ) \sim \mathcal { D } } \left[ \frac { 1 } { T } \sum _ { t = 0 } ^ { T - 1 } \mathcal { L } ( X , Y ; f _ { \phi } ( u _ { t } ) , w _ { t } ) \right] \right]$$

其中，$\phi$ 是优化器网络的参数，$\mathcal{T}$ 是任务分布，$\mathcal{L}$ 是损失函数，$w_t$ 是 optimizee 在时间步 $t$ 的权重，$u_t$ 是优化器网络的输入特征（如梯度、动量等），$f_\phi$ 是优化器网络生成的更新量。该目标旨在最小化所有任务和时间步上的平均损失。

对于本文使用的两种 LO 架构（`small_fc_lopt` 和 `VeLO`），它们在标准参数化（SP）下的每参数更新规则形式为：

$$w _ { t } = w _ { t - 1 } - \alpha _ { W } \lambda _ { 1 } d \exp { ( \lambda _ { 2 } m ) }$$

其中 $d$ 是更新方向，$m$ 是更新幅度，$\alpha_W$ 是层特定的学习率，$\lambda_1$ 和 $\lambda_2$ 是常数。该公式表明 LO 为每个参数独立生成方向和幅度，但 SP 下的该规则在 optimizee 宽度增加时会失效。

### µ-参数化（µP）的核心修改

本文的核心贡献在于将最大更新参数化（µP）应用于 LO 的 optimizee 网络，以解决 SP 下 LO 在宽度外推时的失败问题。µP 的核心思想是：优化器的更新量、初始化方差和前激活乘数必须根据网络宽度（扇入 FAN_IN）进行正确缩放，以确保在宽度趋于无穷时，每个参数都能获得有意义的更新。µP 对 LO 的 modify 涉及三个关键插槽（changed slots）：

**1. 优化器更新缩放（Optimizer Update Scaling）**：这是最关键的修改。在 SP 下，所有层的更新规则相同。在 µP 下，**隐藏层**的更新需要除以扇入 FAN_IN：

$$w _ { t } = w _ { t - 1 } - \frac { 1 } { \mathrm { FAN\_IN } } \cdot \left( \alpha _ { w _ { l } } \lambda _ { 1 } d \exp \left( \lambda _ { 2 } m \right) \right)$$

而对于**输入层和输出层**，更新规则保持不变：

$$w _ { t } = w _ { t - 1 } - \alpha _ { w _ { l } } \lambda _ { 1 } d \exp \left( \lambda _ { 2 } m \right)$$

该缩放的因果机制是：在宽网络中，如果不除以 FAN_IN，隐藏层的更新量会随着宽度增加而累积放大，导致前激活爆炸和训练不稳定。除以 FAN_IN 确保了更新量的尺度与宽度无关。

**2. 优化器初始化（Optimizee Initialization）**：µP 要求隐藏层和输入层的权重初始化为 $\mathcal{N}(0, \frac{1}{\mathrm{FAN\_IN}})$，而输出层的权重初始化为 $\mathcal{N}(0, 1)$。这确保了初始前激活的方差与宽度无关。

**3. 前激活乘数（Optimizee Multipliers）**：在前向传播过程中，输出层的前激活需要乘以 $\frac{1}{\mathrm{FAN\_IN}}$。这确保了输出层的梯度尺度与宽度无关，从而稳定了反向传播。

### 多宽度元训练策略

除了 µP 参数化，本文还引入了一个简单的元训练策略修改：在包含多个不同宽度（如 128、512、1024）的 MLP 任务上进行元训练，而不是仅使用单一宽度。该策略（µLO_M）相比单宽度元训练（µLO_S）在更宽任务和更长训练步数上均表现出显著优势。该策略的因果机制是：多宽度任务分布迫使 LO 学习到与宽度无关的更新规则，从而提升了泛化能力。

### 证据强度与失败模式分析

上述公式和修改均有直接证据支持。更新缩放公式的置信度为 1.0，因为论文明确给出了隐藏层和非隐藏层的区别公式。初始化规则和前激活乘数规则的置信度也为 1.0，证据锚点明确。

SP 下的失败模式是：在宽网络中，SP LO 的前激活会爆炸（Figure 2），导致训练发散或停滞（Figure 6）。µP 通过上述三个缩放规则直接解决了该问题：更新缩放防止了更新量累积，初始化控制了初始激活方差，前激活乘数稳定了梯度尺度。多宽度训练策略则进一步增强了 LO 对宽度变化的鲁棒性。

需要注意的是，µP 的理论保证仅适用于宽度缩放。对于深度和训练步数的泛化，论文中的证据是纯经验性的（Figure 5 和 Figure 6），没有对应的理论公式支持。此外，论文中使用的标准误差公式 $\textstyle { \frac { \sigma } { \sqrt { n } } }$ 仅用于报告实验结果的统计不确定性，并非核心方法公式。

## 实验与分析

### 主结果：µLO在宽网络任务上全面超越基线

核心实验评估了µLO在分布外（OOD）宽网络任务上的元泛化能力。实验套件包含MLP（ImageNet-32、ImageNet-64、CIFAR-10）、语言模型（LM1B）和ViT（CIFAR-10）五种任务，每种任务均测试Large（宽度2048）、XL（MLP宽度4096，Transformer宽度3072）和XXL（各任务最大宽度）三种规模。所有学习型优化器（LO）仅在MLP任务上以FLOP匹配的预算进行元训练，而手设计基线（AdamW和µAdam）在每项任务上均进行了超过500种配置的网格搜索调优。

**决定性证据来自表1的平均排名**：在所有迭代步数和任务规模上，µLO\_M和µVeLO\_M持续获得最佳（粗体）和次佳（下划线）平均排名。例如，在1k步评估中，µLO\_M在Large/XL/XXL规模上的平均排名分别为1.80、2.00和2.00，µVeLO\_M分别为2.60、1.60和1.80，而SP LO和手设计基线的排名均显著更低。这直接验证了核心因果链：µP通过修正优化器更新缩放、初始化方差和前激活乘数对宽度的依赖关系，使LO在宽网络上保持稳定训练，而SP LO因前激活爆炸（图2）导致发散或停滞。

![[assets/figures/papers/iclr26_0001_f8z2bzOLK2_muLO_Compute-Efficient_Meta-Generalization_of_Le/figures/013_Table_1.jpg]]
*Table 1: Summary of optimizer performance on large tasks. We report the average rank of different optimizers across the five tasks in our suite. We evaluate each optimizer on large-width tasks: Large (2048), XL (4096 for MLPs and 3072 for vit and LM), and XXL (largest size for each task see Tab.10 of the appendix). We bold the strongest, underline the second strongest, and italicize the third strongest average rank in each column. We observe that, across all iterations, $\mu \mathrm { L O } _ { M }$ and $\mu { \mathrm { V e L O } } _ { M }$ consistently obtain the best and second-best ranks for all tasks

**图4展示了更细粒度的损失曲线**：在MLP IN32和MLP IN64的8192宽度任务上（图4a-b），µLO\_M和µVeLO\_M在1000步后持续降低损失，最终损失低于调优后的AdamW和µAdam；在MLP C10的8192宽度任务上（图4c），µLO匹配或超越最强基线；在远分布外的LM（宽度4096）和ViT（宽度4096）任务上（图4d-e），µLO接近但未始终超越调优后的手设计基线。这一模式表明：µP对宽度的修正具有普适性，但LO本身的元训练分布（仅MLP）限制了其在完全异质架构上的上限。

### 消融实验：多宽度元训练是必要组件

**图3的消融实验揭示了元训练分布的关键作用**：对比单宽度元训练（µLO\_S，仅宽度128）和多宽度元训练（µLO\_M，宽度128/512/1024），在元训练步长（1000步）内，µLO\_M在宽度≥512时损失更低（图3a）；在5000步（5×元训练步长）时，µLO\_M的优势进一步扩大（图3b）。这表明多宽度策略不仅提升了跨宽度泛化，还意外地改善了跨时间步长的泛化。这一现象的可能机制是：多宽度任务提供了更丰富的梯度信号，使LO学习到更鲁棒的更新策略，而非过拟合到单一宽度的特定动态。

**图2的机制验证实验**：在µP下，MLP第二层前激活的坐标标准差在不同宽度（128-2048）上保持稳定；而在SP下，宽度≥512的模型在训练数百步后前激活爆炸。这直接支撑了µP的因果假设——不正确的缩放导致宽网络不稳定，而µP通过FAN\_IN缩放因子消除了这一瓶颈。

### 跨深度和跨时间步长的泛化

**图5评估了跨深度泛化**：在5×元训练深度的MLP任务上（深度从3层增至15层），µLO\_M和µVeLO\_M的损失曲线低于其SP对应物，且接近或优于调优后的手设计基线。但需注意，这一结果是纯经验性的——论文明确指出Depth-µP的理论保证仅适用于残差网络且块深度为1，不适用于本文的MLP、ViT和Transformer架构。因此，跨深度泛化的改进可能部分源于µP对宽度的稳定化间接改善了深度扩展的数值条件，而非直接修正了深度相关的缩放。

![[assets/figures/papers/iclr26_0001_f8z2bzOLK2_muLO_Compute-Efficient_Meta-Generalization_of_Le/figures/021_Figure_5.jpg]]
*Figure 5: Evaluating generalization capabilities of µLOs to deeper networks. Our focus is on comparing the meta-generalization to deeper tasks of µLOs to SP LOs (all meta-trained exclusively on MLPs). We also report the performance per-task tuned AdamW and µAdam for reference. Each plot reports average training loss over 5 seeds with standard error bars. In each case, µLOs show improved generalization and performance when compared to their SP counterparts*

**图6展示了最令人惊讶的结果**：在长达25,000步（25×元训练步长）的任务上，µLO稳定降低损失，而最优的SP LO要么无法降低损失（图6a），要么出现不稳定（图6b），或在8000步后发散（图6c）。这一发现具有实际意义——它表明µP不仅解决了宽度缩放问题，还通过稳定化训练动态消除了LO在长程优化中的累积误差。但论文未提供这一现象的理论解释，属于需要手动验证的开放问题。

### 失败模式与局限性

1. **远分布外任务的性能上限**：在LM和ViT任务上，µLO虽接近但未始终超越调优后的手设计基线。这可能是因为LO的元训练分布（MLP）与测试任务（Transformer架构）存在根本性差异，µP无法弥补架构级的不匹配。

2. **深度泛化的理论缺失**：跨深度改进是纯经验性的，缺乏µP的理论保证。当深度进一步增加（如10×以上）时，µLO是否仍能保持优势尚不清楚。

3. **计算成本公平性**：虽然µLO与SP LO使用相同的FLOP预算，但手设计基线（AdamW、µAdam）在每项任务上进行了500+配置的调优，而µLO仅在MLP上元训练一次。这种比较偏向LO，因为调优成本远高于元训练成本。论文未讨论这一公平性差异对结论的影响。

## 方法谱系与知识库定位

µLO 的核心贡献在于将最大更新参数化（µP）从手设计优化器（如 Adam）的范畴系统地迁移至学习型优化器（LO）领域。这项工作填补了一个关键空白：尽管 µP 已被证明能保证超参数在不同宽度上的可迁移性（即“超参数迁移”），但此前并未有工作将其应用于 LO 的元泛化问题。µLO 通过修改 LO 对优化目标网络（optimizee）的更新缩放、初始化方差和前激活乘数，使得 LO 在未见过的更宽网络上的行为保持稳定，从而解决了标准参数化（SP）下 LO 因前激活爆炸或更新不稳定而导致的元泛化失败。

**与基线的谱系关系**：
- **SP LO（LO_S, LO_M, VeLO_M）**：直接的前身。µLO 与它们共享相同的优化器架构（`small_fc_lopt` 和 `VeLO`），唯一的区别在于参数化方案。实验表明，SP LO 在宽网络（如宽度 8192）上要么发散，要么损失停滞，而 µLO 则能稳定优化。这直接证明了瓶颈在于参数化而非优化器容量。
- **µAdam**：手设计的 µP 基线。µAdam 是 Adam 的 µP 版本，在每项任务上经过超过 500 种配置的网格搜索调优。µLO 在大多数任务上匹配或超越了 µAdam，且 µLO 仅在 MLP 任务上元训练，未在测试任务上调优。这凸显了 LO 在自动发现有效更新规则方面的潜力，但 µAdam 作为强基线也划定了 µLO 性能的上界参考。
- **AdamW**：SP 下的手设计基线，同样经过密集调优。在极宽网络（如 MLP 宽度 8192）上，µLO 显著优于 AdamW，但在远分布外任务（如 LM 和 ViT）上，µLO 仅接近或匹配 AdamW，并未始终超越。

**适用边界**：
- µLO 的元泛化能力在**宽度轴**上最强，理论上有 µP 保证。在**深度轴**上，µLO 展现出意外但纯经验性的改进（可泛化至 5 倍元训练深度），但 µP 的理论保证并不覆盖深度，且 Depth-µP 仅适用于残差网络且块深度为 1，不适用于本文研究的 MLP 和 Transformer。因此，深度泛化的稳健性需要手动验证。
- 在**训练步数轴**上，µLO 可稳定泛化至 25 倍元训练步数，而 SP LO 则发散或停滞。这种稳定性的根本原因尚不明确，论文仅将其归因于 µP 的“稳定化效应”。
- 实验任务集有限（MLP、ViT、LM），且宽度上限为 8192（MLP）和 3072/12288（Transformer）。更宽模型上的行为未知。

**局限与开放问题**：
1. **参数化的最优选择未定**：论文明确指出“哪种参数化（µP、SP、CompleteP 等）最适合元学习优化器仍是一个开放问题”。CompleteP（Dey et al., 2025）可能同时改善跨深度和宽度的泛化，但尚未与 LO 结合。
2. **深度泛化的理论缺失**：µP 对深度的保证是纯经验性的，且不适用于非残差网络。如何将 µP 与 CompleteP 等方案结合以同时覆盖深度和宽度，是未来重要方向。
3. **远分布外任务的性能差距**：在 LM 和 ViT 任务上，µLO 虽接近但未始终超越调优后的手设计基线。这暗示 LO 的元训练分布（仅 MLP）可能限制了其对完全不同架构的泛化能力。
4. **可扩展性上限未知**：µLO 在比实验最大宽度更宽的模型上表现如何？多宽度元训练策略能否进一步缩放以覆盖更广的任务分布？这些问题需要更大规模的实证研究。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/muLO_Compute_Efficient_Meta_Generalization_of_Learned_Optimizers.pdf

![[paperPDFs/ICLR_2026/muLO_Compute_Efficient_Meta_Generalization_of_Learned_Optimizers.pdf]]
