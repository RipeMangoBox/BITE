---
title: "UETrack: A Unified and Efficient Framework for Single Object Tracking"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UETrack_A_Unified_and_Efficient_Framework_for_Single_Object_Tracking.pdf
project_link: null
code_link: "https://github.com/kangben258/UETrack"
aliases:
- UETrack
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过引入基于Token池化的混合专家（TP-MoE）消除门控机制，实现高效的多模态特征聚合与专家分工；同时提出目标感知自适应蒸馏（TAD）策略，根据样本特性动态控制蒸馏，避免误导性监督。
primary_logic: 利用相似度驱动的软分配代替硬门控，实现并行化的专家协作；自适应蒸馏过滤不可靠教师信号，从而在保证极快推理速度的同时提升多模态跟踪精度。
claims:
- UETrack-B在LaSOT上达到69.2% AUC，GPU/CPU/AGX速度分别为163/56/60 FPS。
- UETrack-S相较HiT-B在LaSOT AUC提升2.3%，AGX速度提升1.1倍。
- TP-MoE消除了复杂的门控机制，采用加权特征聚合的软分配策略。
- TAD自适应决定是否利用教师模型的监督，并动态调整蒸馏程度。
---

# UETrack: A Unified and Efficient Framework for Single Object Tracking

> [!tip] 核心洞察
> 利用相似度驱动的软分配代替硬门控，实现并行化的专家协作；自适应蒸馏过滤不可靠教师信号，从而在保证极快推理速度的同时提升多模态跟踪精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | UETrack: 统一高效的单目标跟踪框架 |
| 英文题名 | UETrack: A Unified and Efficient Framework for Single Object Tracking |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.01412) · [Code](https://github.com/kangben258/UETrack) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | UETrack |
| Dataset | LaSOT, GOT-10k, VOT-RGBD22, DepthTrack |

> [!tip] 效果简介
> - LaSOT 上，AUC 69.2 vs 64.7 (AsymTrack-B) / 64.6 (HiT-Base) / 60.6 (MixFormerV2-S) (+4.5% over AsymTrack-B)。
> - GOT-10k 上，AO 72.6 vs 67.7 (AsymTrack-B) (+4.9%)。
> - VOT-RGBD22 上，EAO 68.3 vs 68.1 (SUTrack-T) (+0.2%)。

## 概要

单目标跟踪（SOT）在高效性与多模态适应性之间存在显著张力：现有高效跟踪器（如 **HiT-Base** (Kang et al., ICCV 2023)、**MixFormerV2-S** (Cui et al., NeurIPS 2023)、**AsymTrack-B** (Zhu et al., AAAI 2025)）主要局限于RGB场景，而多模态跟踪器（如 **SUTrack-B** (Chen et al., AAAI 2025)）通常设计复杂、推理速度慢，难以在资源受限平台（如Jetson AGX）上实现实时部署。针对这一瓶颈，本文提出 **UETrack**——一个统一且高效的多模态单目标跟踪框架，核心思路是通过**相似度驱动的软分配**替代传统门控机制，实现并行化专家协作，同时以**自适应蒸馏**过滤不可靠的教师监督信号。

UETrack 的核心技术贡献体现在两个层面：

- **TP-MoE（Token-Pooling-based Mixture-of-Experts）**：消除传统MoE中复杂耗时的门控网络，转而采用基于token相似度的软分配策略，使多个专家并行处理特征并通过加权聚合重构输出，在增强多模态表征能力的同时保持高推理效率。
- **TAD（Target-aware Adaptive Distillation）**：引入Adaptive Net，根据样本特性动态决定是否启用教师模型的监督信号，避免对简单样本施加误导性蒸馏，从而在训练阶段实现更精准的知识迁移。

在实验验证层面，UETrack 展现出显著的性能与效率优势：

- **UETrack-B** 在 LaSOT 上达到 **69.2% AUC**，相较 AsymTrack-B 提升 4.5%，同时在 GPU/CPU/AGX 上分别达到 **163/56/60 FPS** 的推理速度。
- **UETrack-S** 相较 HiT-B 在 LaSOT AUC 上提升 **2.3%**，AGX 速度提升 **1.1 倍**。
- 在多模态基准上，UETrack 在 DepthTrack（F-score **60.6%**）、LasHeR（AUC **55.5%**）、VisEvent（AUC **59.2%**）等数据集上均取得领先或可比结果，验证了其跨 RGB、Depth、Thermal、Event、Language 五种模态的统一处理能力。

消融实验进一步证实：移除 TP-MoE 导致平均性能下降 **0.8%**，将其替换为门控 MoE 会使 AGX 速度降低 **21 FPS**；引入 TAD 自适应蒸馏带来 **1.0%** 的整体提升，显著优于标准全量蒸馏。这些结果表明，UETrack 在“精度-速度-模态泛化”三角权衡中实现了有效突破，为资源受限场景下的多模态跟踪提供了可行方案。



### 单目标跟踪的效率瓶颈与多模态困境

单目标跟踪（Single Object Tracking, SOT）是计算机视觉中的基础任务，旨在给定初始帧目标位置后，在后续视频帧中持续定位该目标。近年来，基于Transformer的跟踪器在精度上取得了显著进步，但其计算开销通常较大，难以在资源受限的边缘设备上部署。为此，一系列高效跟踪器相继被提出，如**HiT-Base**（Kang et al., ICCV 2023）、**MixFormerV2-S**（Cui et al., NeurIPS 2023）和**AsymTrack-B**（Zhu et al., AAAI 2025），它们在保持较高精度的同时显著提升了推理速度。

然而，这些高效跟踪器存在一个关键局限：**它们几乎全部针对RGB模态设计，缺乏对多模态输入的原生支持**。在真实世界的跟踪场景中，单一RGB模态往往难以应对复杂的光照变化、遮挡、低对比度等挑战。引入深度（Depth）、热红外（Thermal）、事件（Event）和语言（Language）等辅助模态，能够为目标定位提供互补信息，从而提升跟踪的鲁棒性。

### 现有多模态跟踪器的效率短板

尽管多模态跟踪器（如**SUTrack-B**, Chen et al., AAAI 2025）在精度上表现优异，但其架构设计通常较为复杂，推理速度远低于高效RGB跟踪器。据Figure 1(b)所示的速度-精度权衡对比，当前主流多模态跟踪器在Jetson AGX Xavier边缘设备上的运行速度普遍低于20 FPS的实时性阈值，难以满足实际部署需求。这种“精度高但速度慢”的现状，揭示了一个明确的研究缺口：**缺乏一个统一的高效多模态单目标跟踪框架，能够在极快推理速度的前提下，充分利用多种模态信息提升跟踪精度**。

### 本文动机与核心思路

针对上述困境，本文提出**UETrack**——一个统一且高效的单目标跟踪框架，旨在同时解决两个核心问题：

1. **如何实现高效的多模态特征聚合？** 现有混合专家（Mixture-of-Experts, MoE）机制通常依赖门控网络进行专家选择，这一过程不仅引入额外计算开销，还因门控决策的序列依赖性而难以并行化。UETrack提出**基于Token池化的混合专家模块（Token-Pooling-based MoE, TP-MoE）**，利用相似度驱动的软分配策略替代硬门控，实现专家间的并行协作，在消除门控瓶颈的同时增强多模态表示能力。

2. **如何在不增加推理成本的前提下利用多模态教师知识？** 知识蒸馏是提升轻量模型精度的常用手段，但标准蒸馏策略对所有样本一视同仁，当教师模型在特定样本上产生不可靠预测时，反而会引入误导性监督。UETrack提出**目标感知自适应蒸馏（Target-aware Adaptive Distillation, TAD）**，通过一个轻量的Adaptive Net动态判断每个样本是否需要教师监督，从而过滤不可靠信号，仅在有益时进行蒸馏。

通过这两项核心设计，UETrack在五种模态（RGB、Depth、Thermal、Event、Language）上均实现了精度与速度的优异平衡。例如，UETrack-B在LaSOT上达到69.2% AUC，同时在GPU、CPU和AGX上分别以163、56和60 FPS的速度运行，较SUTrack-T在AGX上加速1.8倍，在CPU上加速2.4倍，且精度相当。



## 核心方法与创新机理

UETrack 的核心创新围绕两个 **changed slots** 展开，分别针对多模态特征聚合的效率瓶颈和知识蒸馏的可靠性问题，形成了一套“高效学生模型 + 自适应蒸馏”的联合设计方案。

### 1. 混合专家机制：从标准 FFN 到 TP-MoE

**Baseline 状态**：现有高效跟踪器（如 **HiT-Base**, Kang et al., ICCV 2023; **MixFormerV2-S**, Cui et al., NeurIPS 2023）的 Transformer 骨干中，前馈网络（FFN）采用标准结构，缺乏多专家分工能力。而传统门控 MoE 引入离散路由和额外门控参数，在资源受限平台上造成显著的推理延迟。

**Proposed 方案**：UETrack 提出 **Token-Pooling-based Mixture-of-Experts (TP-MoE)**，将学生模型骨干中的若干 FFN 替换为无门控的混合专家模块。其核心机制为**相似度驱动的软分配策略**：

1. **局部聚合与专家嵌入**：对输入 token $\mathbf{T}_{\mathrm{in}}$ 进行局部聚合（Aggre），再通过嵌入层得到专家 token $\mathbf{T}_{\mathrm{e}} = \mathrm{Embed}(\mathrm{Aggre}(\mathbf{T}_{\mathrm{in}}))$。
2. **软分配加权聚合**：计算输入 token 与专家 token 的相似度矩阵，经 Softmax 归一化后对输入进行加权聚合，得到各专家的专属输入 $\mathbf{T}_{\mathrm{a}}^i$。
3. **并行专家处理与重构**：各专家独立处理后，通过另一相似度驱动的软分配将专家输出重构为最终输出 $\mathbf{O}$。

完整计算过程如公式 (1) 所示（详见方法部分）。TP-MoE 消除了传统门控 MoE 的离散路由开销，实现了专家的并行化协作与隐式分工。

**因果机制**：软分配使每个 token 能够以连续权重参与多个专家的计算，避免了硬门控的信息丢失和路由不平衡问题；同时，相似度矩阵的计算高度并行化，不引入额外的串行依赖，从而在增强多模态表示能力的同时保持极低延迟。

**证据强度**：消融实验表明，移除 TP-MoE 导致所有基准平均性能下降 0.8%；将 TP-MoE 替换为门控 MoE 则使 AGX 速度下降 21 FPS，验证了无门控设计的效率优势。

### 2. 知识蒸馏策略：从无蒸馏/全量蒸馏到 TAD

**Baseline 状态**：现有高效跟踪器通常独立训练，不利用教师模型的知识迁移；若直接引入标准逐样本全量蒸馏，教师模型对困难样本的不可靠预测会误导学生，导致增益有限甚至性能退化。

**Proposed 方案**：UETrack 提出 **Target-aware Adaptive Distillation (TAD)** 框架，以多模态跟踪器 **SUTrack-B**（Chen et al., AAAI 2025）作为教师模型，通过 **Adaptive Net** 实现样本级的自适应蒸馏决策。

Adaptive Net 根据输入样本的特征输出二值因子 $\alpha \in \{0, 1\}$：当 $\alpha = 1$ 时，该样本接受教师监督（KL 散度损失 $\mathcal{L}_{kd}$ 和 MSE 特征损失 $\mathcal{L}_{f}$）；当 $\alpha = 0$ 时，跳过蒸馏，仅使用真实标签训练。

学生模型的训练目标为：
$$\mathcal{L}_S = \mathcal{L}_{\mathrm{c}}(\hat{p}_s, p) + \lambda_g \mathcal{L}_{\mathrm{g}}(\hat{p}_s, p) + \lambda_{l_1} \mathcal{L}_{l_1}(\hat{p}_s, p) + \mathcal{L}_t(\hat{p}_s, p) + \alpha \left( \lambda_{kd} \mathcal{L}_{kd}(\hat{p}_s, \hat{p}_t) + \lambda_f \mathcal{L}_f(\hat{p}_s, \hat{p}_t) \right)$$

Adaptive Net 本身通过替代预测 $\hat{p}_a$（$\alpha=1$ 时取教师预测，否则取学生预测）的跟踪损失进行优化，使其学会判断教师信号对当前样本是否有益。

**因果机制**：TAD 的核心在于**过滤不可靠的教师信号**——对于教师模型也难以处理的困难样本，强制蒸馏会引入噪声监督；Adaptive Net 通过端到端学习识别这些样本并自动关闭蒸馏，使蒸馏增益集中在教师能提供有效指导的样本上。

**证据强度**：消融实验显示，引入标准蒸馏（无自适应）仅带来有限增益，而 TAD 的自适应机制进一步带来显著提升，整体相较基线提升 1.0%。可视化结果（Figure 7）证实 TAD 在不同模态下均能做出合理的蒸馏决策。

### 创新总结

两个 changed slots 形成协同效应：TP-MoE 在推理侧保证多模态特征聚合的效率上限，TAD 在训练侧提升知识迁移的可靠性。推理时仅使用学生模型，无需教师和 Adaptive Net，从而在 **LaSOT 上达到 69.2% AUC，同时在 GPU/CPU/AGX 上分别运行 163/56/60 FPS**，实现了精度与效率的双重突破。



UETrack的整体训练与推理流程如图2所示，采用师生蒸馏架构，核心由三个模块构成：**学生模型**（Student）、**教师模型**（Teacher）和**自适应网络**（Adaptive Net）。训练阶段三者协同工作，推理阶段仅保留学生模型，从而在保证高效推理的同时获得多模态蒸馏的精度收益。

**输入处理与模态统一**。对于RGB-Depth、RGB-Thermal、RGB-Event等配对模态，UETrack将辅助模态图像与RGB图像沿通道维度拼接，形成6通道复合输入 $\mathbf{I}_c \in \mathbb{R}^{H \times W \times 6}$，经patch embedding层统一转换为token嵌入。对于语言模态，则通过独立的文本编码器提取特征后与视觉token进行融合。这种统一的早期拼接策略避免了为不同模态设计独立的编码分支，是实现轻量化的基础设计。

**学生模型骨干**。学生模型基于**Fast-iTPN-T**构建，采用其前N层作为backbone，预测头采用center head进行目标定位。学生模型的关键改造在于将骨干中部分前馈网络替换为**Token-Pooling-based Mixture-of-Experts（TP-MoE）**模块。TP-MoE通过相似度驱动的软分配策略替代传统门控机制，实现专家的并行化协作与多模态特征增强，是UETrack在保持高速推理的同时提升多模态表示能力的核心设计。

**教师模型与自适应蒸馏**。教师模型采用更强的多模态跟踪器**SUTrack-B**（Chen et al., AAAI 2025），为学生模型提供目标分布和特征图层面的监督信号。与传统逐样本全量蒸馏不同，UETrack引入**Target-aware Adaptive Distillation（TAD）**框架：Adaptive Net根据输入样本的特征自适应地决定是否启用蒸馏（输出二值因子 $\alpha \in \{0, 1\}$），从而过滤不可靠的教师信号，避免误导性监督对轻量学生模型的性能损害。

**推理流程**。推理时仅使用学生模型：6通道复合图像经patch embedding后送入TP-MoE增强的Transformer骨干，最终由center head输出目标边界框。整个流程无额外分支、无门控开销、无教师模型参与，保证了在GPU、CPU和Jetson AGX等不同硬件平台上的高效部署。

### 补充图表

![[assets/figures/papers/paper_list_l949_https_arxiv_org_abs_2603_01412/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of UETrack. The training pipeline consists of a teacher model, a student model, and an Adaptive Net for adaptive distillation. During inference, only the student model is used, with TP-MoE as the core component to enhance multi-modal modeling*



UETrack 的推理仅依赖学生模型，其核心由两个关键模块构成：**Token-Pooling-based Mixture-of-Experts (TP-MoE)** 和 **Target-aware Adaptive Distillation (TAD)**。前者在骨干网络中替代部分前馈网络（FFN），以极低的额外开销实现多模态特征的专家化建模；后者在训练阶段自适应地控制教师监督信号的注入，避免不可靠蒸馏对学生的误导。

### TP-MoE：基于Token池化的无门控混合专家

传统 MoE 依赖离散门控函数将 token 路由至不同专家，这一过程不仅引入额外的门控参数，还因 token 与专家间的硬分配和串行通信而显著拖慢推理速度。TP-MoE 的核心洞察在于：**用相似度驱动的软分配替代硬门控，使所有专家可并行处理，同时通过局部聚合增强短程依赖建模**。

模块的完整计算流程如公式 (1) 所示：

$$
\begin{array} { r l } 
& \mathbf{T}_{\mathrm{e}} = \mathrm{Embed} \left( \mathrm{Aggre} \left( \mathbf{T}_{\mathrm{in}} \right) \right) \\
& \mathbf{T}_{\mathrm{a}} = \mathrm{Split} \left( \mathrm{Softmax} \left( \mathbf{T}_{\mathrm{in}} \mathbf{T}_{\mathrm{e}}^{\top} \right)^{\top} \mathbf{T}_{\mathrm{in}} \right) \\
& \mathbf{O}_{\mathrm{e}} = \mathrm{Merge} \left( \left\{ \mathrm{Expert}_{i} \left( \mathbf{T}_{\mathrm{a}}^{i} \right) \right\}_{i=1}^{E} \right) \\
& \quad \quad \mathbf{O} = \mathrm{Softmax} \left( \mathbf{T}_{\mathrm{in}} \mathbf{T}_{\mathrm{e}}^{\top} \right) \mathbf{O}_{\mathrm{e}}
\end{array}
$$

各步骤的变量含义与功能如下：

- **$\mathbf{T}_{\mathrm{in}}$**：输入 token 序列，来自 Transformer 块中前序层的输出。
- **$\mathrm{Aggre}(\cdot)$**：局部聚合操作，对每个 token 及其邻域进行信息汇聚，增强短程依赖建模能力。
- **$\mathrm{Embed}(\cdot)$**：将聚合后的特征映射为 $E$ 个专家 token $\mathbf{T}_{\mathrm{e}}$，每个专家 token 编码了对应专家所关注的特征原型。
- **$\mathrm{Softmax}(\mathbf{T}_{\mathrm{in}} \mathbf{T}_{\mathrm{e}}^{\top})$**：计算输入 token 与专家 token 之间的相似度矩阵，作为软分配权重。该权重矩阵的转置与 $\mathbf{T}_{\mathrm{in}}$ 相乘，得到按专家分组聚合后的 token 集合 $\mathbf{T}_{\mathrm{a}}$。
- **$\mathrm{Split}(\cdot)$**：将聚合结果沿专家维度切分为 $E$ 组，每组 $\mathbf{T}_{\mathrm{a}}^{i}$ 送入对应的专家网络 $\mathrm{Expert}_{i}$ 独立并行处理。
- **$\mathrm{Merge}(\cdot)$**：合并所有专家的输出，得到 $\mathbf{O}_{\mathrm{e}}$。
- **最终输出 $\mathbf{O}$**：再次利用输入 token 与专家 token 的相似度矩阵，对 $\mathbf{O}_{\mathrm{e}}$ 进行加权重组，使每个原始 token 获得来自所有专家的软性贡献。

该设计的效率优势体现在三个层面：(1) 无需门控网络，消除了额外的参数与计算；(2) 专家间完全并行，无 token 路由的串行等待；(3) 软分配使每个 token 可同时受益于多个专家的知识，避免了硬分配可能造成的容量浪费。消融实验证实，将 TP-MoE 替换为传统门控 MoE 会导致 AGX 平台速度下降 21 FPS，而直接移除 TP-MoE 则使多基准平均性能下降 0.8%。

### TAD：目标感知自适应蒸馏

知识蒸馏在高效模型训练中广泛使用，但标准蒸馏策略对所有样本施加等强度的教师监督，忽略了教师模型本身可能产生不可靠预测的事实。TAD 通过引入一个轻量级 **Adaptive Net**，根据样本特征动态决定是否启用蒸馏以及蒸馏的强度。

Adaptive Net 输出一个标量 $\alpha \in \{0, 1\}$，其决策逻辑嵌入在学生模型的训练目标中：

$$
\mathcal{L}_{S} = \mathcal{L}_{\mathrm{c}}(\hat{p}_{s}, p) + \lambda_{g} \mathcal{L}_{\mathrm{g}}(\hat{p}_{s}, p) + \lambda_{l_{1}} \mathcal{L}_{l_{1}}(\hat{p}_{s}, p) + \mathcal{L}_{t}(\hat{p}_{s}, p) + \alpha \left( \lambda_{kd} \mathcal{L}_{kd}(\hat{p}_{s}, \hat{p}_{t}) + \lambda_{f} \mathcal{L}_{f}(\hat{p}_{s}, \hat{p}_{t}) \right)
$$

其中：
- $\mathcal{L}_{\mathrm{c}}$、$\mathcal{L}_{\mathrm{g}}$、$\mathcal{L}_{l_{1}}$ 分别为分类损失、GIoU 损失和 L1 回归损失，$\mathcal{L}_{t}$ 为任务相关损失，均基于学生预测 $\hat{p}_{s}$ 与真值 $p$ 计算。
- $\mathcal{L}_{kd}$ 和 $\mathcal{L}_{f}$ 分别为 KL 散度损失和特征图 MSE 损失，用于衡量学生预测 $\hat{p}_{s}$ 与教师预测 $\hat{p}_{t}$ 之间的一致性。
- $\lambda_{g}$、$\lambda_{l_{1}}$、$\lambda_{kd}$、$\lambda_{f}$ 为超参数，控制各项损失的相对权重。
- **$\alpha$ 为 Adaptive Net 的输出**：当 $\alpha = 1$ 时，该样本接受教师蒸馏；当 $\alpha = 0$ 时，蒸馏项被完全屏蔽，学生仅依赖真值监督。

为保证 Adaptive Net 自身得到有效训练，UETrack 引入了替代预测机制：

$$
\hat{p}_{a}^{i} = \begin{cases} 
\hat{p}_{t}^{i} & \text{if } \alpha = 1, \\
\hat{p}_{s}^{i} & \text{if } \alpha = 0 
\end{cases}
$$

Adaptive Net 的损失函数使用替代预测 $\hat{p}_{a}$ 与真值 $p$ 计算，但不包含蒸馏项：

$$
\mathcal{L}_{A} = \mathcal{L}_{\mathrm{c}}(\hat{p}_{a}, p) + \lambda_{g} \mathcal{L}_{\mathrm{g}}(\hat{p}_{a}, p) + \lambda_{l_{1}} \mathcal{L}_{l_{1}}(\hat{p}_{a}, p) + \mathcal{L}_{\mathrm{t}}(\hat{p}_{a}, p)
$$

这一设计形成了一种博弈式训练机制：若 Adaptive Net 错误地启用了蒸馏（$\alpha=1$ 但教师预测质量差），$\mathcal{L}_{A}$ 将增大，促使网络调整决策；反之，若错误地屏蔽了有价值的蒸馏信号，同样会受到惩罚。消融实验表明，引入自适应蒸馏后模型总体性能提升 1.0%，而标准蒸馏（无自适应机制）带来的增益明显更弱。

### 补充图表

![[assets/figures/papers/paper_list_l949_https_arxiv_org_abs_2603_01412/figures/004_Figure_3.jpg]]
*Figure 3: TP-MoE architecture diagram*

![[assets/figures/papers/paper_list_l949_https_arxiv_org_abs_2603_01412/figures/003_Figure_4.jpg]]
*Figure 4: Architecture of Adaptive Net*



## 实验与关键发现

UETrack 的实验设计围绕一个核心问题展开：**能否在保持极低计算开销的前提下，统一高效地处理 RGB、Depth、Thermal、Event 和 Language 五种模态的单目标跟踪？** 为此，作者从模型变体效率、RGB 基准主结果、多模态扩展性能、消融验证以及可视化分析五个层面进行了系统性验证。

### 模型变体与效率指标

UETrack 提供三个规模变体以适配不同资源约束场景。Table 1 汇总了参数量、FLOPs 及三种硬件平台上的推理速度。

![[assets/figures/papers/paper_list_l949_https_arxiv_org_abs_2603_01412/figures/005_Table_1.jpg]]
*Table 1: Details of UETrack model variants*

| 变体 | 参数量 | FLOPs | GPU (2080Ti) | CPU (i9-14900KF) | AGX Xavier |
|------|--------|-------|---------------|------------------|------------|
| UETrack-T | 5M | 1.6G | ~200+ FPS | — | — |
| UETrack-S | 9M | 2.5G | 183 FPS | 68 FPS | 67 FPS |
| UETrack-B | 13M | 3.2G | 163 FPS | 56 FPS | 60 FPS |

**关键瓶颈突破**：UETrack-B 在 AGX 上达到 60 FPS，远超实时跟踪的 20 FPS 门槛，同时参数量仅 13M。这一效率优势源于 TP-MoE 消除了传统门控 MoE 的串行路由开销——消融实验证实，将 TP-MoE 替换为门控 MoE 会导致 AGX 速度骤降 21 FPS，直接验证了软分配策略对推理效率的决定性作用。

### RGB 跟踪主结果

Table 2 在 LaSOT、GOT-10k、TrackingNet 和 TNL2K 四个大规模 RGB 基准上对比了 UETrack 与主流高效跟踪器。

![[assets/figures/papers/paper_list_l949_https_arxiv_org_abs_2603_01412/figures/006_Table_2.jpg]]
*Table 2: State-of-the-art (SOTA) comparisons on four large-scale RGB benchmarks. The top three real-time results are highlight with red, blue and green fonts, respectively. The top three speed across different platforms are highlighted in bold*

**LaSOT 上的核心发现**：
- UETrack-B 以 **69.2% AUC** 登顶实时跟踪器榜首，较 AsymTrack-B（64.7%）提升 4.5%，较 HiT-Base（64.6%）提升 4.6%。
- UETrack-S（67.0% AUC）以 9M 参数量超越 HiT-Base（64.6%），**AUC 提升 2.3% 且 AGX 速度达 1.1 倍**，证明轻量级模型同样可从 TP-MoE 中获益。
- UETrack-T 相较 MixFormerV2-S 在 LaSOT 上 AUC 提升 2.8%，AGX 速度仍有 1.1 倍优势。

**GOT-10k 上的表现**：UETrack-B 取得 **72.6% AO**，超过 AsymTrack-B 达 4.9%，进一步验证了统一框架在短时跟踪场景下的泛化能力。

**速度-精度权衡**：Figure 1(b) 的 AGX 散点图清晰展示了 UETrack 系列位于 Pareto 前沿——在同等精度下速度显著领先，在同等速度下精度更高。UETrack-B 相较 SUTrack-T 在 AGX 上快 1.8 倍、CPU 上快 2.4 倍，同时精度相当，打破了“多模态必慢”的固有认知。

### 多模态扩展性能

UETrack 在 Depth、Thermal、Event 和 Language 四种辅助模态上均展现出竞争力。

**Depth 模态**（Table 3）：UETrack-B 在 VOT-RGBD22 上取得 **68.3% EAO**，以 0.2% 微弱优势超越 SUTrack-T，同时在 DepthTrack 上以 **60.6% F-score** 领先 EMTrack 2.3%。值得注意的是，UETrack 的 6 通道拼接输入策略在此场景下未引入额外模态对齐模块，却达到了与专用深度融合方法相当的性能。

**Thermal 模态**（Table 4）：LasHeR 上 UETrack-B 取得 **55.5% AUC**，超越 SUTrack-T 1.6%，表明 TP-MoE 的相似度驱动软分配能有效处理 RGB-T 模态间的互补信息。

**Event 模态**（Table 5）：VisEvent 上 UETrack-B 以 **59.2% AUC** 小幅领先 SUTrack-T 0.4%，验证了框架对异步稀疏事件流的适应性。

**Language 模态**（Table 6）：TNL2K 上 UETrack-B 取得 **58.0% AUC**，超过 SeqTrackv2-B 0.5%，证明 TP-MoE 的 token 级软分配同样适用于视觉-语言跨模态融合。

**跨模态一致性**：UETrack 在所有五种模态上均以明显更低的计算代价达到或超越专用多模态跟踪器的精度，这是现有工作中罕见的统一高效表现。

### 消融实验

Table 7 通过逐步增减核心模块，量化了 TP-MoE 和 TAD 的独立贡献（速度测量基于 AGX）。

![[assets/figures/papers/paper_list_l949_https_arxiv_org_abs_2603_01412/figures/011_Table_7.jpg]]
*Table 7: Ablation Study. ∆ denotes the performance change (averaged over benchmarks) compared with the baseline. The speed is measured on the AGX*

**TP-MoE 的贡献**：
- 移除 TP-MoE（即恢复为标准 FFN）导致所有基准平均性能下降 **0.8%**，同时 AGX 速度无明显变化（软分配未引入额外延迟）。
- 将 TP-MoE 替换为传统门控 MoE 后，AGX 速度从基线骤降 **21 FPS**，精度提升有限。这直接证实：**TP-MoE 的性能增益来自软分配带来的专家分工质量，而非简单的参数增加**。

**TAD 的贡献**：
- 在 TP-MoE 基础上加入标准蒸馏（无自适应），性能提升有限。
- 引入自适应蒸馏后，模型总体提升 **1.0%**，且该增益来自 TAD 对不可靠教师信号的过滤——当教师模型对特定样本预测质量低时，Adaptive Net 自动关闭蒸馏（α=0），避免误导性监督。

**联合效应**：TP-MoE 提供更强的学生模型表征能力，TAD 提供更智能的监督信号，两者协同使 UETrack-B 在 AGX 上以 60 FPS 达到 69.2% LaSOT AUC。

### 可视化分析

**专家注意力分布**（Figure 6）：TP-MoE 中不同专家的注意力热力图显示，各专家自发聚焦于目标的不同空间区域（如中心、边缘、背景上下文），验证了软分配策略确实促成了无监督的专家分工。这种分工无需显式路由，完全由相似度矩阵驱动。

**TAD 自适应决策**（Figure 7）：跨模态样本的 α 值分布表明，TAD 能根据模态特性和样本难度自适应决定是否蒸馏——对于教师模型明显优于学生的困难样本（如遮挡、模糊），α 倾向于 1；对于教师本身也不确定的样本，α 倾向于 0，避免错误累积。

### 已知局限与失效模式

尽管 UETrack 在效率和精度上取得了显著突破，仍存在以下局限：

1. **极端无纹理场景**：当 RGB 和辅助模态同时缺乏可区分纹理时（如纯色墙壁前的目标），6 通道拼接输入无法提供足够判别信息，跟踪漂移风险增大。
2. **语言歧义**：在 Language 模态下，若描述高度歧义或与视觉内容不一致，TAD 可能频繁关闭蒸馏，导致学生模型缺乏有效监督。
3. **输入噪声敏感性**：TP-MoE 的软分配依赖相似度矩阵，当输入 token 噪声较大时（如低质量深度图或事件流），专家分配质量可能下降——这是相似度驱动机制的固有脆弱性。
4. **单目标限制**：当前框架仅针对单目标跟踪设计，未扩展到多目标场景，多目标间的 token 交互机制有待探索。

### 开放性讨论

- TP-MoE 的相似度驱动软分配本质上是一种无参数的 token 分组机制，其可解释性和泛化边界值得进一步理论分析。
- TAD 当前采用硬决策（α∈{0,1}），若能引入连续 α 值实现加权蒸馏，可能进一步释放教师模型的知识迁移潜力。
- 模型在 MCU 级微控制器上的部署可行性尚未验证，TP-MoE 的矩阵乘法开销在极端低算力场景下可能成为瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l949_https_arxiv_org_abs_2603_01412/figures/001_Figure_1.jpg]]
*Figure 1: UETrack vs. Other Trackers. (a) compares UETrack with current efficient and multi-modal trackers; (b) presents a comparison of speed-accuracy trade-offs on the Jetson AGX*

![[assets/figures/papers/paper_list_l949_https_arxiv_org_abs_2603_01412/figures/008_Table_3.jpg]]
*Table 3: SOTA comparisons on depth modality*

![[assets/figures/papers/paper_list_l949_https_arxiv_org_abs_2603_01412/figures/009_Table_4.jpg]]
*Table 4: SOTA comparisons on thermal modality*

![[assets/figures/papers/paper_list_l949_https_arxiv_org_abs_2603_01412/figures/012_Table_5.jpg]]
*Table 5: SOTA comparisons on event modality*

![[assets/figures/papers/paper_list_l949_https_arxiv_org_abs_2603_01412/figures/010_Table_6.jpg]]
*Table 6: SOTA comparisons on language modality*

![[assets/figures/papers/paper_list_l949_https_arxiv_org_abs_2603_01412/figures/013_Figure_6.jpg]]
*Figure 6: Visualization of attention distributions of TP-MoE experts. The bright regions denote the attended areas. Each expert focuses on distinct spatial regions*



## 定位与知识库关联

### 高效跟踪器的演进与UETrack的定位

UETrack处于**高效单目标跟踪**（efficient SOT）与**多模态跟踪**两条研究线的交汇处。现有高效跟踪器如**HiT-Base**（Kang et al., ICCV 2023）、**MixFormerV2-S**（Cui et al., NeurIPS 2023）和**AsymTrack-B**（Zhu et al., AAAI 2025）主要在RGB模态上实现了实时推理，但缺乏对多模态输入的支持。另一方面，多模态跟踪器如**SUTrack-B**（Chen et al., AAAI 2025）虽精度较高，但设计复杂、推理速度慢，难以在资源受限平台部署。UETrack的核心贡献在于**首次构建了一个统一的、同时覆盖RGB、Depth、Thermal、Event和Language五种模态的高效跟踪框架**，填补了“多模态+高效”这一空白。

从技术谱系看，UETrack的学生模型骨干基于**Fast-iTPN-T**，预测头采用经典的**center head**，继承了one-stream跟踪范式的简洁性。其关键创新——TP-MoE——则是对标准Transformer中FFN的替换，将混合专家思想引入跟踪领域，但通过**相似度驱动的软分配**彻底规避了传统MoE中门控网络带来的计算开销和路由不稳定性。

### 与基线方法的关键差异

与代表性高效跟踪器HiT-Base相比，UETrack-S在LaSOT上AUC提升2.3%，同时在Jetson AGX上速度提升1.1倍，实现了精度与效率的双重超越。与多模态教师模型SUTrack-B相比，UETrack-B在AGX上速度快1.8倍、CPU上快2.4倍，且精度保持可比甚至更高（LaSOT AUC 69.2% vs. SUTrack系列）。这验证了TP-MoE和TAD蒸馏策略的有效性——学生模型不仅学到了教师的多模态表示能力，还通过自适应蒸馏过滤了不可靠的教师信号，避免了盲目模仿带来的性能退化。

### 适用边界与局限

UETrack的设计和实验验证存在以下明确边界：

1. **任务边界**：框架目前仅针对单目标跟踪（SOT），论文未涉及多目标跟踪（MOT）的扩展。将TP-MoE的软分配机制推广到多目标场景需要额外的关联建模和数据关联模块。
2. **模态处理方式**：对于Depth、Thermal、Event模态，UETrack采用简单的**6通道拼接**（RGB + 辅助模态）作为输入，未设计模态特定的编码器。这种统一处理虽然简洁高效，但在极端场景下（如完全无纹理的深度图或高度歧义的语言描述）可能不足以充分利用模态互补性。论文也明确指出在语言描述高度歧义时仍可能出现跟踪失败。
3. **软分配的鲁棒性**：TP-MoE的专家分配完全依赖于输入token与专家嵌入的相似度矩阵。当输入噪声较大（如严重遮挡、运动模糊）时，相似度计算可能失准，进而影响专家分工质量。论文未对此类退化场景进行专项消融。
4. **硬件下限**：实验覆盖的最低算力平台为Jetson AGX Xavier（约32 TOPS），未验证在微控制器（MCU）或超低功耗NPU上的部署可行性。

### 开放问题

1. **TP-MoE的跨任务泛化**：相似度驱动的软分配策略消除了门控网络，这一设计范式是否可以推广到其他多模态融合任务，如多模态目标检测、语义分割？其在不同任务密度下的效率-精度权衡曲线值得探索。
2. **TAD的精细化蒸馏**：当前TAD通过Adaptive Net输出二值决策（α∈{0,1}），决定是否对样本进行蒸馏。一个自然的扩展是将教师不确定性量化为连续权重，实现更精细的加权蒸馏，使简单样本更多依赖学生自身学习、困难样本更多借助教师引导。
3. **模态扩展机制**：当前框架对新增模态需要重新训练。是否可以设计一种模态无关的token化方式，使TP-MoE能够零样本或少量样本地适配新模态，而无需从头训练整个学生模型？
4. **实时性定义的统一性**：论文将AGX上超过20 FPS定义为“实时”，这一标准在跟踪社区尚未完全统一。随着边缘设备算力提升，是否需要建立更细粒度的效率等级标准，以便公平比较不同硬件平台上的方法？



## 原文 PDF

![[paperPDFs/CVPR_2026/UETrack_A_Unified_and_Efficient_Framework_for_Single_Object_Tracking.pdf]]
