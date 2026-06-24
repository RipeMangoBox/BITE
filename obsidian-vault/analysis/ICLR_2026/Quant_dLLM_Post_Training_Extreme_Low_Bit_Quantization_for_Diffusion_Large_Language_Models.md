---
title: "Quant-dLLM: Post-Training Extreme Low-Bit Quantization for Diffusion Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Quant_dLLM_Post_Training_Extreme_Low_Bit_Quantization_for_Diffusion_Large_Language_Models.pdf
openreview_forum_id: HD7tuVakmR
aliases:
- QD
- Quant-dLLM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "通过模拟扩散去噪的掩码校准（MCS）、数据感知的任意阶量化器（DAQ）以及重要性引导的自适应混合精度（ABMP），有效缓解了2-bit量化误差。"
primary_logic: "在极端低比特下，关键在于校准数据与推理时的激活分布对齐，利用多二进制分解提升权重表示能力，并将有限的比特预算集中在敏感权重的关键块上。"
claims:
- "Quant-dLLM在五个模型上的平均准确率达到51.3%，超过Slim-LLM（40.9%）、GPTQ（36.5%）等所有2-bit基线方法。"
- "MCS使LLaDA-8B-Base的MMLU 5-shot准确率从52.10%提升至56.87%，验证了掩码校准对齐的必要性。"
- "DAQ中的RSR和DOR组件带来巨大增益：LLaDA-8B-Base MMLU基线39.26%→RSR 48.32%→RSR+DOR 56.87%。"
- "在2-bit严格预算下，ABMP通过5%重分配使LLaDA-8B-Base MMLU从54.32%提升至56.87%。"
---

# Quant-dLLM: Post-Training Extreme Low-Bit Quantization for Diffusion Large Language Models

> [!tip] 核心洞察
> 在极端低比特下，关键在于校准数据与推理时的激活分布对齐，利用多二进制分解提升权重表示能力，并将有限的比特预算集中在敏感权重的关键块上。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Quant-dLLM：扩散大语言模型的后训练极低比特量化 |
| 英文题名 | Quant-dLLM: Post-Training Extreme Low-Bit Quantization for Diffusion Large Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=HD7tuVakmR); [GitHub](https://github.com/ZTA2785/Quant-dLLM) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Quant-dLLM |
| Dataset | 5-model Average, LLaDA-8B-Base (7 tasks), LLaDA-Instruct Math & Science, LLaDA-Instruct Code Generation |

> [!tip] 效果简介
> - 5-model Average 上，Avg. Accuracy 为 51.3，对比 40.9 (Slim-LLM)，变化 +10.4。
> - LLaDA-8B-Base (7 tasks) 上，Avg. Accuracy 为 54.06，对比 42.39 (Slim-LLM)，变化 +11.67。
> - LLaDA-Instruct Math & Science 上，Avg. Accuracy 为 >30，对比 <12 (baselines)，变化 >+18。

## 概述

扩散大语言模型（dLLM）通过逐步去噪掩码Token生成回答，其推理过程具有独特的时间步依赖激活分布。直接将为自回归LLM设计的后训练量化（PTQ）方法迁移至dLLM时，忽略了掩码机制与激活分布偏移，导致在2-bit极低比特量化下性能严重崩塌——现有方法如GPTQ、Slim-LLM的平均准确率仅约36%–41%。

针对这一瓶颈，本文提出**Quant-dLLM**，一个专为扩散LLM设计的极低比特权重量化框架。其核心洞察在于：极端低比特下的量化成败取决于三个可控因素——校准数据与推理时激活分布的对齐、权重参数化的表示能力、以及有限比特预算的精准分配。Quant-dLLM通过以下三个模块实现这一目标：

- **掩码校准模拟（MCS）**：构造时间步感知、部分可见的掩码校准数据，使校准分布与扩散去噪推理对齐，消除分布失配。
- **数据感知任意阶量化器（DAQ）**：采用多二进制矩阵行-列缩放叠加（RSR）参数化权重，并通过数据感知目标重构（DOR）将输出误差纳入优化，显著提升2-bit表示能力。
- **自适应块混合精度（ABMP）**：基于离群点检测的重要性分数，在严格2-bit平均预算下将敏感块升级为3-bit、非敏感块降为1-bit，实现精度重分配。

在五个扩散LLM模型（LLaDA-8B-Base/Instruct、LLaDA-1.5、Dream-7B-Base/Instruct）上的实验表明，Quant-dLLM在7个通用任务上的平均准确率达到**51.3%**，显著优于Slim-LLM（40.9%）、GPTQ（36.5%）等所有2-bit基线方法（Table 1）。在数学推理与代码生成任务上，Quant-dLLM是唯一保持可用性能的方法，基线方法几乎完全失效（Figure 3）。消融实验分别验证了MCS、DAQ（RSR+DOR）和ABMP的独立增益，三者协同作用将LLaDA-8B-Base的MMLU 5-shot准确率从基线的39.26%提升至56.87%（Table 2）。

## 背景与动机

扩散大语言模型（diffusion Large Language Models, dLLMs）通过逐步去噪掩码序列生成文本，在推理质量与可控性上展现出独特优势。然而，其自回归式的迭代去噪过程使得单次推理需执行数百至上千步前向传播，计算量与显存开销远超同规模的自回归模型，严重制约了实际部署。后训练量化（Post-Training Quantization, PTQ）是缓解这一瓶颈的常见手段，但现有方法几乎全部为自回归LLM设计，直接迁移到扩散LLM时面临根本性障碍。

**核心瓶颈**在于扩散LLM的推理过程存在时间步依赖的掩码机制。在每一步去噪中，模型仅能看到部分未被掩码的token，而标准PTQ方法在校准时使用全可见序列，忽略了这一分布差异。当量化精度降至2-bit时，这种分布错配导致激活统计量严重偏离推理时的真实分布，使得量化误差急剧放大，性能崩塌。此外，固定码本的2-bit权重量化表示能力有限，难以捕捉扩散LLM权重中关键的离群结构；均匀的精度分配策略则无法将有限的比特预算集中于最敏感的权重块。

针对上述缺口，**Quant-dLLM**提出了三个协同模块：掩码校准模拟（Masked Calibration Simulation, MCS）通过模拟扩散过程的时间步感知掩码，生成与推理分布对齐的校准数据；数据感知任意阶量化器（Data-aware Any-order Quantizer, DAQ）采用多二进制行-列缩放叠加参数化，以数据感知的封闭形式优化替代传统固定码本；自适应块混合精度（Adaptive Blockwise Mixed Precision, ABMP）基于重要性分数在严格2-bit平均预算下重新分配块级精度。三者共同构成了首个面向扩散LLM的极低比特后训练量化框架。

## 核心创新

### 问题瓶颈：自回归PTQ方法直接迁移的失效

将自回归LLM的后训练量化（PTQ）方法直接应用于扩散大语言模型（dLLM）时，在2-bit极低比特下会出现严重的性能崩塌。其根本原因在于两类模型存在本质差异：

1. **时间步依赖的掩码机制**：扩散LLM在推理时采用逐步去噪过程，每个时间步的输入序列包含不同比例的掩码token。而自回归LLM的PTQ校准数据通常使用全可见序列，忽略了这一掩码分布特性，导致校准与推理时的激活分布严重不匹配。
2. **激活分布偏移**：不同去噪时间步下，掩码比例从接近100%逐步降至0%，激活统计量随之剧烈变化。直接使用固定校准数据无法覆盖这一动态范围。

这一瓶颈在实验中表现明显：**GPTQ**（Frantar et al., ICLR 2023）和**GPTAQ**（Li et al., ICML 2025）在五个dLLM模型上的2-bit平均准确率仅为36.5%和35.6%，而采用混合精度的**Slim-LLM**（Huang et al., arXiv 2024）也仅达到40.9%（Table 1）。

### 三个关键创新（Changed Slots）

Quant-dLLM针对上述瓶颈，在三个核心维度上对基线方法进行了系统性改进：

#### 1. 校准数据分布：从全可见序列到时间步感知掩码模拟

| 维度 | 基线方法 | Quant-dLLM (MCS) |
|------|---------|-----------------|
| 校准数据 | 全可见序列（忽略掩码） | 时间步感知、部分可见的掩码模拟数据 |

**Masked Calibration Simulation (MCS)** 通过模拟扩散去噪过程生成校准数据：在多个时间步$t$上对校准样本施加对应比例的掩码，构造出与推理时激活分布对齐的输入批次。这一设计直接解决了分布不匹配问题——MCS使LLaDA-8B-Base的MMLU 5-shot准确率从52.10%提升至56.87%（Table 2a），验证了掩码校准对齐的必要性。

#### 2. 权重参数化：从固定码本到数据感知的任意阶多二进制分解

| 维度 | 基线方法 | Quant-dLLM (DAQ) |
|------|---------|-----------------|
| 权重表示 | 固定2-bit量化码本（如GPTQ） | 多二进制矩阵行-列缩放叠加 |

**Data-aware Any-order Quantizer (DAQ)** 将权重矩阵近似为$K$个二值矩阵的行-列缩放叠加：

$$\hat{\mathbf{W}} = \sum_{k=1}^{K} \left( \pmb{\alpha}_r^{(k)} \pmb{\alpha}_c^{(k)\top} \right) \odot \mathbf{B}_k, \quad \mathbf{B}_k \in \{-1, +1\}^{n \times m}$$

这一参数化包含两个关键子组件：

- **Data-aware Objective Reformulation (DOR)**：通过分析发现量化误差并非均匀分布，而是集中在少数关键权重上。DOR利用MCS模拟数据的二阶矩矩阵$\mathbf{S}_{\mathrm{MCS}}$构造重要性掩码$\mathbf{\Lambda}$，将优化目标重定义为加权重构误差：

$$\widehat{\mathcal{L}}_{\Lambda}(\alpha_r, \alpha_c) = \Big\| \boldsymbol{\Lambda} \odot \big( \mathbf{W} - (\alpha_r \alpha_c^{\top}) \odot \mathbf{B} \big) \Big\|_F^2$$

- **Row-column Successive Re-scaling (RSR)**：针对上述目标，RSR提供封闭形式的行/列缩放因子交替更新，避免了昂贵的迭代优化。

消融实验揭示了两个组件的巨大增益：LLaDA-8B-Base的MMLU从基线39.26%提升至RSR的48.32%，再提升至RSR+DOR的56.87%（Table 2c）。

#### 3. 精度分配：从均匀2-bit到重要性引导的自适应混合精度

| 维度 | 基线方法 | Quant-dLLM (ABMP) |
|------|---------|-----------------|
| 精度策略 | 每块均匀2-bit | 基于重要性分数的自适应块混合精度（1/2/3-bit） |

**Adaptive Blockwise Mixed Precision (ABMP)** 在严格的每层平均2-bit约束下，根据块重要性分数$s_g = \sum_{(i,j) \in g} \mathbf{Z}_{ij}$重新分配精度预算：

$$\frac{1}{|\mathcal{G}|} \sum_{g} b_g = 2, \quad b_g \in \{1, 2, 3\}$$

具体策略为：将top-k最重要块升级为3-bit，bottom-k降级为1-bit，其余保持2-bit。在默认5%重分配比例下，ABMP使LLaDA-8B-Base的MMLU从54.32%进一步提升至56.87%（Table 2b），验证了将有限比特预算集中在敏感权重关键块上的有效性。

### 创新协同效应

三个创新并非孤立运作，而是形成协同增强的闭环：MCS提供分布对齐的校准数据，为DAQ的数据感知优化奠定基础；DAQ通过DOR识别关键权重，其输出的重要性矩阵$\mathbf{Z}$直接驱动ABMP的精度分配决策；ABMP则将DAQ的多二进制表示能力聚焦于最需要表达精度的区域。这一协同使得Quant-dLLM在五个模型上的平均准确率达到51.3%，显著超过Slim-LLM的40.9%（+10.4个百分点，Table 1），且在数学推理和代码生成等复杂任务上，Quant-dLLM是唯一有效保留准确率的方法（Figure 3）。

## 整体框架

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_HD7tuVakmR/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our Quant-dLLM. Masked Calibration Simulation: Aligns calibration with diffusion by simulating masked, timestep-aware inputs. Adaptive Blockwise Mixed Precision: Assigns binary orders by importance under a 2-bit average. Data-aware Any-order Quantizer: Builds multi-binary RC forms with data-aware optimization*

Quant-dLLM 是一个面向扩散大语言模型（dLLM）的后训练极低比特量化框架，其核心目标是在严格的 2-bit 权重平均预算下，最大限度地保留模型在下游任务中的推理能力。框架由三个协同工作的模块组成，形成一条从校准数据生成到权重量化、再到精度分配的完整流水线。

### 流水线总览

框架的输入包括：一个预训练的扩散大语言模型、一份原始校准文本数据（如 C4 子集），以及目标平均比特预算（2-bit）。输出为量化后的模型权重，可直接用于扩散去噪推理。

三个模块的协作关系如下：

1. **掩码校准模拟** 接收原始校准文本，通过模拟扩散模型的掩码去噪过程，生成时间步感知的、部分可见的校准激活数据。这些数据随后被送入下一个模块。
2. **数据感知任意阶量化器** 以 MCS 生成的校准数据为输入，对每一层的权重矩阵执行多二进制分解。它首先通过数据感知目标重构（DOR）识别关键权重区域，然后利用行列连续重缩放（RSR）以封闭形式迭代拟合多个二值矩阵及其缩放因子。
3. **自适应块混合精度** 在 DAQ 完成逐层量化后，根据 DOR 阶段产生的重要性分数，在层内进行块级精度重分配：将关键块升级为 3-bit，非关键块降级为 1-bit，确保层平均比特严格为 2。

这一设计直接回应了核心瓶颈：**直接迁移自回归 LLM 的 PTQ 方法到扩散 LLM 时，忽略了时间步依赖的掩码机制和激活分布偏移，导致 2-bit 量化时性能崩塌。** 三个模块分别从校准对齐、权重参数化、预算分配三个维度缓解这一问题。

### 模块间的数据流与依赖关系

- **MCS → DAQ**：MCS 输出的校准激活用于计算非中心二阶矩矩阵，该矩阵是 DAQ 中 DOR 构建重要性掩码的基础。同时，MCS 模拟的激活分布也为 RSR 的封闭形式更新提供了数据感知的优化目标。
- **DAQ 内部（DOR → RSR）**：DOR 首先基于 MCS 的二阶矩矩阵计算重要性矩阵，通过 3σ 规则检测离群点并生成重要性掩码；RSR 随后在该掩码的加权下，交替更新行缩放因子和列缩放因子，逐阶拟合二进制矩阵。
- **DAQ → ABMP**：DAQ 中 DOR 产生的重要性矩阵被聚合为块级重要性分数，ABMP 据此决定哪些块获得更高的二进制阶数。

### 关键设计决策

- **校准数据对齐**：MCS 并非简单地使用原始文本作为校准数据，而是通过模拟扩散前向过程的掩码调度，生成与推理时激活分布一致的输入。这一设计是性能提升的基础——消融实验表明，仅引入 MCS 就将 LLaDA-8B-Base 的 MMLU 5-shot 准确率从 52.10% 提升至 56.87%。
- **多二进制参数化**：DAQ 将权重矩阵近似为多个二进制矩阵的加权叠加，每个二进制矩阵配有独立的行-列缩放因子。相比于固定码本的 2-bit 量化，这种参数化提供了更丰富的表示能力。
- **严格预算约束下的自适应精度**：ABMP 不改变总比特预算，而是通过“劫富济贫”的方式重新分配——将有限的表示能力集中于对输出误差影响最大的权重块。默认重分配比例为每层 5%，即约 5% 的块获得 3-bit 精度，等量的块降为 1-bit。

## 核心模块与公式推导

### 瓶颈与因果路径

将自回归LLM的权重量化方法直接迁移到扩散LLM时，性能在2-bit下崩塌。根本原因在于两点：**校准分布错位**——标准PTQ使用全可见序列校准，而扩散推理时输入是时间步依赖的部分掩码序列；**低比特表示能力不足**——固定2-bit码本无法有效拟合扩散LLM中更分散的权重分布。Quant-dLLM通过三个模块形成因果链来解决：MCS对齐校准分布 → DAQ增强权重表示 → ABMP集中比特预算。

### 前置：扩散LLM的掩码前向过程

扩散LLM的前向噪声过程定义为对离散token序列的逐步掩码：

$$q ( y _ { t } \mid y ) = \operatorname { C a t } ( \alpha _ { t } y + ( 1 - \alpha _ { t } ) m )$$

其中 $y_t$ 是时间步 $t$ 的掩码扩散序列分布，$m$ 代表掩码token，$\alpha_t$ 控制掩码比例。随着 $t$ 增大，序列中越来越多的token被替换为掩码。这一时间步依赖的掩码机制是校准数据必须对齐的关键特性。

### 模块一：掩码校准模拟（MCS）

MCS解决的核心问题是**校准数据与推理时激活分布的对齐**。具体而言，MCS在 $T$ 个时间步上对校准样本施加不同的掩码比例，生成时间步感知、部分可见的输入序列。这一过程模拟了扩散去噪推理时模型实际接收的输入模式，从而消除校准与推理之间的分布偏移。

为支持后续的数据感知量化，MCS从模拟数据中预计算非中心二阶矩矩阵：

$$\mathbf { S } _ { \mathrm { M C S } } = \mathbb { E } _ { t \sim \pi } \Big [ \sum _ { b } \tilde { \mathbf { X } } _ { b } ( t ) \tilde { \mathbf { X } } _ { b } ( t ) ^ { \top } \Big ] \approx \frac { 1 } { | \mathcal { T } | } \sum _ { t \in \mathcal { T } } \sum _ { b } \tilde { \mathbf { X } } _ { b } ( t ) \tilde { \mathbf { X } } _ { b } ( t ) ^ { \top }$$

其中 $\tilde{\mathbf{X}}_b(t)$ 是时间步 $t$ 下第 $b$ 个校准样本的激活值，$\mathcal{T}$ 为采样的时间步集合。该矩阵编码了扩散推理过程中激活的统计特征。

**消融证据**：在LLaDA-8B-Base上，MCS将MMLU 5-shot准确率从52.10%提升至56.87%（Table 2a），验证了掩码校准对齐的必要性。

### 模块二：数据感知任意阶量化器（DAQ）

DAQ的核心思路是用**多二进制矩阵的行-列缩放叠加**来参数化权重，从而突破固定2-bit码本的表示瓶颈。权重矩阵 $\mathbf{W} \in \mathbb{R}^{n \times m}$ 被分解为 $K$ 个二值分量的叠加：

$$\hat { \mathbf { W } } = \sum _ { k = 1 } ^ { K } \left( \pmb { \alpha } _ { r } ^ { ( k ) } \pmb { \alpha } _ { c } ^ { ( k ) \top } \right) \odot \mathbf { B } _ { k } , \qquad \mathbf { B } _ { k } \in \{ - 1 , + 1 \} ^ { n \times m }$$

其中 $\pmb{\alpha}_r^{(k)} \in \mathbb{R}^n$ 和 $\pmb{\alpha}_c^{(k)} \in \mathbb{R}^m$ 分别是第 $k$ 个分量的行缩放向量和列缩放向量，$\mathbf{B}_k$ 是二值矩阵，$\odot$ 表示逐元素乘积。$K$ 控制量化阶数（$K=1$ 对应2-bit，$K=3$ 对应3-bit）。

DAQ包含两个关键子组件：

**数据感知目标重定义（DOR）**：分析发现量化误差并非均匀分布，而是集中在少数关键权重上。DOR首先从MCS的二阶矩矩阵构建重要性矩阵 $\mathbf{Z}$，然后通过3σ规则检测离群点形成重要性掩码：

$$\widetilde { \mathbf Z } = ( \mathbf Z - \pmb \mu ) \oslash \pmb \sigma , \qquad \pmb \Pi = \mathbb { I } ( | \widetilde { \mathbf Z } | > 3 )$$

其中 $\pmb{\Pi}$ 标记了重要性远超均值的权重位置。最终重要性掩码 $\pmb{\Lambda}$ 为这些位置赋予更高权重，形成加权重构目标：

$$\widehat { \mathcal { L } } _ { \Lambda } ( \alpha _ { r } , \alpha _ { c } ) = \Big \| \boldsymbol { \Lambda } \odot \big ( \mathbf { W } - ( \alpha _ { r } \alpha _ { c } ^ { \top } ) \odot \mathbf { B } \big ) \Big \| _ { F } ^ { 2 }$$

**行列连续重缩放（RSR）**：在给定二值矩阵 $\mathbf{B}$ 和重要性掩码 $\pmb{\Lambda}$ 的条件下，RSR通过交替优化的封闭形式解更新行缩放和列缩放向量：

$$\alpha _ { r } = [ ( \Lambda ^ { 2 } \odot \mathbf { W } \odot \mathbf { B } ) \alpha _ { c } ] \oslash [ ( \Lambda ^ { 2 } \big ( \mathrm { d i a g } \big ( \alpha _ { c } \big ) \alpha _ { c } \big ) + \varepsilon \mathbf { 1 } _ { n } ]$$

$$\alpha _ { c } = [ ( \Lambda ^ { 2 } \odot \mathbf { W } \odot \mathbf { B } ) ^ { \top } \alpha _ { r } ] ~ \oslash ~ [ ( \Lambda ^ { 2 } ( \operatorname { d i a g } ( \alpha _ { r } ) \alpha _ { r } ) + \varepsilon { \bf 1 } _ { m } ]$$

其中 $\oslash$ 表示逐元素除法，$\varepsilon$ 是防止除零的小常数。这两个公式交替迭代直至收敛，无需梯度计算。

**消融证据**：在LLaDA-8B-Base上，基线MMLU为39.26%，单独使用RSR提升至48.32%，RSR+DOR进一步提升至56.87%（Table 2c），证明两个组件缺一不可。

### 模块三：自适应块混合精度（ABMP）

ABMP在严格2-bit平均预算约束下，将有限的比特预算集中分配给最关键的权重块。每个块 $g$ 的重要性分数由重要性矩阵 $\mathbf{Z}$ 的元素和定义：

$$s_g = \sum_{(i,j) \in g} \mathbf{Z}_{ij}$$

在每层内，ABMP将精度从 $\{1, 2, 3\}$ 中选择，满足平均2-bit的硬约束：

$$\frac{1}{|\mathcal{G}|} \sum_{g} b_g = 2, \quad b_g \in \{1, 2, 3\}$$

具体分配策略为：对top-$k$ 最重要的块分配3-bit，对bottom-$k$ 分配1-bit，其余保持2-bit。默认重分配比例 $k = \lfloor 0.05 |\mathcal{G}| \rfloor$，即每层5%的块获得精度升降。

**消融证据**：在5%重分配比例下，ABMP将LLaDA-8B-Base的MMLU从54.32%提升至56.87%（Table 2b）。校准集大小为128时性能最优，增大至256反而导致性能略降（Table 2d），提示过大的校准集可能引入噪声。

## 实验与分析

### 核心瓶颈与因果机制

直接将为自回归LLM设计的后训练量化（PTQ）方法迁移到扩散大语言模型（dLLM）时，2-bit权重量化会导致性能崩塌。其根本原因在于：**自回归PTQ方法忽略了扩散模型特有的时间步依赖掩码机制**。在扩散模型的去噪过程中，不同时间步的输入序列包含不同比例的掩码token，导致激活分布随去噪进程持续偏移。而GPTQ等传统方法使用全可见序列进行校准，与推理时的部分可见掩码输入之间存在严重的分布失配。Quant-dLLM通过三个协同模块解决这一问题：

- **掩码校准模拟（MCS）** 生成时间步感知的掩码校准数据，使校准阶段的激活分布与推理时对齐。
- **数据感知任意阶量化器（DAQ）** 利用多二进制行-列缩放分解提升2-bit权重的表示能力，并通过数据感知目标函数将优化集中在关键权重上。
- **自适应块混合精度（ABMP）** 在严格维持平均2-bit预算的前提下，将有限的比特资源重新分配给敏感度最高的权重块。

### 主要实验结果

**Table 1** 展示了Quant-dLLM与三个2-bit权重量化基线方法在五个扩散LLM模型、七个通用任务上的全面对比。所有方法均使用相同的校准数据（C4数据集，128样本，序列长度4096），仅进行权重量化，无激活量化或重训练。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_HD7tuVakmR/figures/003_Table_1.jpg]]
*Table 1: Results of GPTQ, GPTAQ, Slim-LLM, and our Quant-dLLM with 2-bit weight quantization among 7 tasks on LLaDA-Base, LLaDA-Instruct, LLaDA-1.5, Dream-Base, and Dream-Instruct. The numbers in parentheses represent the number used for evaluation. Best results are marked in bold*

**Quant-dLLM在所有模型上均取得最优平均准确率。** 五个模型的平均准确率达到51.3%，大幅领先最强基线Slim-LLM（40.9%），优势达+10.4个百分点。相比之下，GPTQ和GPTAQ的平均准确率分别仅为36.5%和35.6%，几乎丧失可用性。

在LLaDA-8B-Base上，Quant-dLLM的七任务平均准确率为54.06%，达到全精度模型（61.46%）的87.72%。Slim-LLM仅为42.39%，GPTQ和GPTAQ则分别降至36.80%和37.14%，表明直接迁移自回归PTQ方法会导致严重的性能退化。

**在数学推理、科学推理和代码生成等高难度任务上，Quant-dLLM的优势更加显著。** Figure 3显示，在LLaDA-Instruct上，Quant-dLLM的数学与科学推理平均准确率超过30%，而所有基线方法均低于12%。在代码生成任务上，Quant-dLLM在LLaDA-Instruct和LLaDA-1.5上的Pass@1均超过15%，基线方法则几乎为0%。这表明Quant-dLLM是唯一能在极端低比特下有效保留复杂推理能力的方案。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_HD7tuVakmR/figures/005_Figure_3.jpg]]
*Figure 3: Average accuracy of mathematical & scientific reasoning, and code generation datasets on LLaDA series and Dream series*

**Table 3** 确认了压缩效率：Quant-dLLM将LLaDA-8B-Base的模型大小从FP16的16.09 GB压缩至3.69 GB（约4.3倍压缩），与GPTQ（3.70 GB）和Slim-LLM（3.72 GB）处于同等水平，验证了“同等内存成本下最优准确率”的核心主张。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_HD7tuVakmR/figures/007_Table_3.jpg]]
*Table 3: (d) Ablation Study for Calibration Set Size*

### 消融实验

**Table 2** 在LLaDA-8B-Base和Dream-7B-Base上系统消融了三个核心组件的贡献，以MMLU 5-shot准确率为评估指标。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_HD7tuVakmR/figures/006_Table_2.jpg]]
*Table 2: Ablation studies on LLaDA-8B-Base and Dream-7B-Base. We report MMLU in 5 shots. (a) Effectiveness of MCS (b) Effectiveness of ABMP (c) Ablation Study for DAQ*

**MCS的独立贡献显著。** Table 2a显示，在LLaDA-8B-Base上，引入MCS将MMLU从52.10%提升至56.87%（+4.77个百分点）；在Dream-7B-Base上从37.81%提升至40.22%（+2.41个百分点）。这直接验证了“掩码校准对齐是扩散LLM量化的必要条件”这一核心论断。

**DAQ中的两个子组件缺一不可。** Table 2c的逐步消融揭示了清晰的增益路径：在LLaDA-8B-Base上，基线配置（无DAQ优化）的MMLU仅为39.26%；引入行-列逐次重缩放（RSR）后提升至48.32%（+9.06个百分点）；进一步加入数据感知目标重构（DOR）后达到56.87%（+8.55个百分点）。DOR通过构建重要性掩码将优化聚焦于量化误差集中的关键权重子集，与RSR形成互补。

**ABMP在5%重分配比例下效果最优。** Table 2b显示，当ABMP将每层5%的块升级为3-bit、等量块降级为1-bit时，LLaDA-8B-Base的MMLU从54.32%提升至56.87%（+2.55个百分点）。增大重分配比例至10%或15%并未带来进一步增益，说明过度重分配可能损害非关键块的表示质量。

**校准集大小存在最优值。** Table 2d显示，校准样本数从64增至128时，LLaDA-8B-Base的MMLU从55.83%提升至56.87%；但继续增至256时反而降至56.42%。128样本在覆盖充分性与计算开销之间取得了最佳平衡。

### 失败模式与局限性

尽管Quant-dLLM在2-bit权重量化上取得了显著突破，但仍存在以下局限：

- **未涉及激活量化。** 当前方案仅处理权重量化，激活仍保持全精度。权值-激活联合量化是进一步压缩推理开销的关键方向，但需要处理扩散模型特有的时间步依赖激活分布。
- **模型规模验证有限。** 实验仅在7B-8B参数规模的LLaDA和Dream系列模型上进行，未在更大规模（如13B、70B）扩散LLM上验证方法的可扩展性。
- **ABMP重分配比例需手动设定。** 当前5%的比例基于经验选择，缺乏自适应确定机制。不同模型或任务的最优比例可能存在差异。
- **实际推理速度未详细报告。** 虽然模型大小压缩至约3.7 GB，但多二进制分解的推理计算开销、在真实硬件上的延迟和能耗表现尚不明确。
- **校准集大小最优值为经验值。** 128样本的最优性仅在当前实验设置下成立，更系统的大规模校准集影响分析有待开展。

### 开放问题

- 能否将MCS和DAQ的思想扩展到权值-激活联合量化，进一步压缩推理内存和计算？
- 在更大规模扩散LLM（如13B、70B）上，当前方法的量化误差累积特性如何？
- ABMP的重分配比例能否通过可微分或基于信号的方法自动学习？
- 多二进制分解在GPU/边缘设备上的实际推理加速效果如何？
- 该方法对其他类别扩散模型（如文本到图像生成的扩散Transformer）是否适用？

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_HD7tuVakmR/figures/008_Table_4.jpg]]

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_HD7tuVakmR/figures/001_Figure_1.jpg]]
*Figure 1: dLLMs’ performance on 7 general tasks. Our Quant-dLLM yields the best accuracy at equal memory cost*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_HD7tuVakmR/figures/009_Table_5.jpg]]

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_HD7tuVakmR/figures/010_Table_3.jpg]]
*Table 3: Model size of LLaDA-8B-Base under different methods*

## 方法谱系与知识库定位

### 核心瓶颈与因果机制

直接迁移自回归LLM的后训练量化（PTQ）方法到扩散大语言模型（dLLM）时，性能崩塌的根源在于**时间步依赖的掩码机制与激活分布偏移**。具体而言，dLLM的推理过程是一个迭代去噪过程，每个时间步的输入序列包含不同比例的掩码token，导致激活分布随去噪进程动态变化。传统PTQ方法（如GPTQ）在校准阶段假设全可见序列，忽略了这种掩码模式，造成校准-推理分布严重失配。当量化到2-bit极端低比特时，这种失配引发的误差被急剧放大，致使模型性能完全崩塌。

Quant-dLLM通过三个协同的因果调节变量缓解了这一瓶颈：
1. **掩码校准模拟（MCS）**：生成时间步感知、部分可见的掩码校准数据，使校准激活分布与推理时对齐；
2. **数据感知任意阶量化器（DAQ）**：采用多二进制行-列缩放叠加的参数化方式，以数据感知目标优化权重重建，提升极端低比特下的表示能力；
3. **自适应块混合精度（ABMP）**：基于重要性分数将有限的2-bit平均预算重新分配，对关键块赋予3-bit、非关键块降至1-bit。

### 方法谱系定位

Quant-dLLM处于**扩散语言模型后训练权重量化**这一新兴交叉领域，其方法谱系可从三个维度定位：

**与自回归LLM量化方法的关系。** Quant-dLLM直接对标三类2-bit权重量化基线：
- **GPTQ**（Frantar et al., ICLR 2023）：基于最优脑手术的逐层量化，使用二阶误差补偿，但假设校准数据为全可见序列，未考虑dLLM的掩码特性；
- **GPTAQ**（Li et al., ICML 2025）：在GPTQ基础上引入激活感知的混合精度分配，但仍沿用自回归模型的校准范式；
- **Slim-LLM**（Huang et al., arXiv 2024）：采用混合精度策略，是2-bit量化中表现最强的基线（五模型平均准确率40.9%）。

Quant-dLLM的关键区分点在于**校准数据生成范式的根本转变**——从“全可见序列校准”变为“掩码扩散模拟校准”（MCS），这一改变使校准激活分布从根源上与推理对齐。消融实验证实，仅MCS一项就将LLaDA-8B-Base的MMLU 5-shot准确率从52.10%提升至56.87%（Table 2a）。

**与二进制/多二进制分解方法的关系。** DAQ的核心——多二进制行-列缩放叠加（Eq. 3）——属于权重的加性二进制分解范式。与传统的单码本量化（如GPTQ的固定2-bit码本）不同，DAQ通过K个二进制矩阵的叠加实现“任意阶”精度控制，其表示能力随K线性增长。更重要的是，DAQ引入了两个数据感知组件：
- **数据感知目标重定义（DOR）**：通过分析发现量化误差集中在少数关键权重上，利用MCS激活的二阶矩矩阵构建重要性掩码Λ（Eq. 7），将重建目标从均匀Frobenius范数转为加权范数（Eq. 6）；
- **行列连续重缩放（RSR）**：针对加权目标推导封闭形式的行/列缩放因子更新公式（Eq. 8-9），实现高效迭代优化。

消融实验揭示了组件的因果贡献链：LLaDA-8B-Base MMLU基线39.26% → 加入RSR后48.32% → 再加入DOR后56.87%（Table 2c）。这表明RSR提供了基础的多二进制表示能力，而DOR通过数据感知加权进一步释放了极端低比特下的潜力。

**与混合精度量化方法的关系。** ABMP在严格2-bit平均预算约束下（Eq. 11），基于离群点检测构建的重要性分数（Eq. 10）进行块级精度重分配。与Slim-LLM的混合精度策略相比，ABMP的区分点在于：(1) 重要性分数来源于数据感知的激活分析，而非仅基于权重幅值；(2) 精度选项扩展为{1, 2, 3}-bit三档；(3) 默认仅重分配5%的块，以极小代价换取显著增益——在LLaDA-8B-Base上，5%重分配使MMLU从54.32%提升至56.87%（Table 2b）。

### 适用边界与局限

**已验证的适用范围：**
- 模型架构：LLaDA系列（8B Base/Instruct, 1.5）和Dream系列（7B Base/Instruct），均为基于掩码扩散的语言模型；
- 量化设置：2-bit weight-only，组大小128，校准集128样本（C4数据集，序列长度4096）；
- 任务类型：通用语言理解（MMLU、WinoGrande、PIQA等7项）、数学推理、科学推理、代码生成；
- 压缩效果：约4.3×压缩比（FP16 16.09GB → 2-bit 3.69GB），与同类方法相当（Table 3）。

**明确的局限与未覆盖场景：**
1. **仅支持权重量化**：未涉及激活量化，无法实现端到端整数推理。论文明确指出这是当前方法的边界，激活量化的分布偏移问题在dLLM中更为复杂；
2. **模型规模上限未验证**：实验最大模型为8B参数，未在13B、70B等更大规模模型上测试。扩散LLM的规模化行为可能与自回归模型不同，需要进一步验证；
3. **架构泛化性未测试**：仅验证了LLaDA和Dream两个掩码扩散架构，未测试其他dLLM变体（如基于连续扩散的模型）。不同扩散机制可能导致MCS的掩码模拟策略需要调整；
4. **ABMP重分配比例需手动设定**：默认5%为经验值（Table 2b显示5%最优，10%和15%反而下降），缺乏自动化或可学习的确定机制；
5. **校准集大小经验性**：128样本为最优值，增至256时性能略降（Table 2d），但未探索更大规模或动态选择策略。这一现象可能暗示过拟合风险，需要进一步研究；
6. **实际推理速度未详细报告**：虽然模型大小与同类方法相当（Table 3），但多二进制分解的推理延迟、内存访问模式、硬件适配性等实际部署指标缺失；
7. **极端低比特的残余误差**：即使在最优配置下，Quant-dLLM在LLaDA-8B-Base上的平均准确率（54.06%）仍与全精度（61.46%）存在约7.4个百分点的差距（Table 1），表明2-bit量化仍有信息损失。

### 开放问题与未来方向

1. **权值-激活联合量化**：能否将MCS的掩码对齐思想扩展到激活量化，实现真正的端到端低比特推理？激活的掩码依赖分布可能比权重更复杂，需要新的校准策略；
2. **规模化验证**：在13B、70B甚至更大规模的dLLM上，MCS的掩码模拟策略是否仍然有效？DAQ的多二进制分解在大矩阵上的计算开销是否可控？
3. **自适应精度分配**：ABMP的5%重分配比例能否通过可微分搜索、强化学习或基于损失景观分析的方式自动确定？能否实现跨层的全局最优分配而非逐层独立决策？
4. **硬件协同设计**：多二进制矩阵的存储格式和计算模式与标准INT2/INT4推理引擎不兼容，需要专门的kernel设计。实际推理延迟和能耗的测量是部署落地的关键缺失环节；
5. **跨领域泛化**：MCS-DAQ-ABMP框架的核心思想——掩码对齐校准、多二进制分解、重要性引导精度分配——是否能迁移到其他扩散生成模型（如图像扩散模型、视频扩散模型）的量化？这些领域的激活分布特性可能提供新的挑战和机遇；
6. **校准集鲁棒性**：校准集大小128的最优性是否具有普适性？能否设计校准集质量评估指标或自适应采样策略来替代固定大小的经验选择？
7. **训练感知量化的潜力**：当前方法严格遵循后训练设定（无重训练、无数据增强），但在极端低比特下，轻量级量化感知微调（如仅更新缩放因子）是否能进一步缩小与全精度的差距？

## 原文 PDF

![[paperPDFs/ICLR_2026/Quant_dLLM_Post_Training_Extreme_Low_Bit_Quantization_for_Diffusion_Large_Language_Models.pdf]]
