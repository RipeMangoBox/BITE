---
title: "Adapt Data to Model: Adaptive Transformation Optimization for Domain-shared Time Series Foundation Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Adapt_Data_to_Model_Adaptive_Transformation_Optimization_for_Domain_shared_Time_Series_Foundation_Models.pdf
project_link: null
code_link: https://github.com/thulab/TATO
aliases:
- TTSATO
- ADMATODSTSFM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/time_series
core_operator: "通过自适应优化输入时间序列的变换管道（上下文切片、尺度归一化、异常值校正），可改善冻结 LTM 的域自适应预测性能，而非微调模型参数。"
primary_logic: "数据适应模型而非模型适应数据：在保持大规模时间序列基础模型冻结不变的前提下，通过自动搜索最优的数据预处理管道，可以在不同下游域中显著提升预测准确性且保持模型通用性。"
claims:
- "TATO在所有先进LTM和广泛使用的数据集上一致且显著地提高了域自适应预测性能，最大MSE降低65.4%，平均降低13.6%。"
- "按模型视角，Timer-LOTSA 的 MSE 平均提升达 24.8%，Chronos-tiny 为 14.5%，Moirai-large 为 14.0%。"
- "去除 Trimmer 或 Scaler 算子显著降低 MSE 提升效果，说明这些变换是关键的。"
- "ETTh1 上 MSE = 0.3901 (TATO)"
---

# Adapt Data to Model: Adaptive Transformation Optimization for Domain-shared Time Series Foundation Models

> [!tip] 核心洞察
> 数据适应模型而非模型适应数据：在保持大规模时间序列基础模型冻结不变的前提下，通过自动搜索最优的数据预处理管道，可以在不同下游域中显著提升预测准确性且保持模型通用性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 适应数据给模型：面向域共享时间序列基础模型的自适应变换优化 |
| 英文题名 | Adapt Data to Model: Adaptive Transformation Optimization for Domain-shared Time Series Foundation Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=uTK1SNgi1N) · [GitHub](https://github.com/thulab/TATO) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/time_series |
| Method | TATO (Time-series Adaptive Transformation Optimization) |
| Dataset | ETTh1, ETTm2, Exchange, Overall |

> [!tip] 效果简介
> - ETTh1 上，MSE 为 0.3901 (TATO)，对比 0.4096 (vanilla)，变化 4.8% reduction。
> - ETTm2 上，MSE 为 0.5100，对比 0.6783，变化 24.8% reduction。
> - Exchange 上，MSE 为 0.3144 (TATO)，对比 0.4382 (vanilla)，变化 28.3% reduction。

## 概要

真实世界时间序列的多样性和非平稳性，使得冻结的预训练大时间序列模型（large time‑series model, LTM）在直接应用时面临泛化性与预测精度之间的根本权衡：同一模型在不同下游域上的表现往往参差不齐。针对这一瓶颈，本文提出一种以数据为中心的域自适应范式——**时间序列自适应变换优化（Time‑series Adaptive Transformation Optimization, TATO）**。其核心思想是"适配数据而非微调模型"：在保持大规模预训练 LTM 参数完全冻结的前提下，通过自动搜索最优的输入数据预处理管道，在不牺牲模型通用性的条件下显著提升跨域预测性能。

TATO 框架围绕三类关键变换构建优化空间：上下文切片（调整回看长度）、尺度归一化（统一量纲与分布）和异常值校正（抑制离群点与噪声），共涵盖九个可组合算子。搜索过程采用基于树状结构 Parzen 估计器（TPE）的贝叶斯优化，并引入时间序列增强（翻转、扭曲、噪声注入、平移、趋势添加等）以增强搜索的鲁棒性。最终通过两阶段帕累托排序，在多个评估指标上筛选出兼顾泛化性与稳定性的变换管道。其优化目标可形式化地表示为寻找历史数据上的最优变换 $h^{*} = \operatorname*{min}_{h \in \mathcal{H}} \mathcal{L}(M, D_{history}, h)$，其中 $M$ 为冻结模型，$\mathcal{L}$ 为损失函数。

在多个先进 LTM（Timer‑UTSD、Timer‑LOTSA、Moirai 系列、Chronos‑tiny）及广泛使用的数据集上的实验表明，TATO 带来一致且显著的域自适应预测增益：平均 MSE 降低 13.6%，最大降幅达 65.4%。按模型视角，Timer‑LOTSA 的 MSE 平均提升 24.8%，Chronos‑tiny 提升 14.5%，Moirai‑large 提升 14.0%。消融实验进一步证实，移除上下文切片或尺度归一化算子会导致性能大幅下降，而增加变换搜索试验次数与历史样本数量均可进一步提升效果。需要注意的是，在 Weather 等部分高变异性数据集上，某些模型的收益较小甚至为负，表明极端域偏移下的适配仍需后续关注。



大规模时间序列基础模型（LTM），如 Timer、Moirai 和 Chronos 等，通过在庞大语料上的预训练，展现出强大的时序建模能力。然而，这些模型在预训练后通常以冻结状态直接应用于下游任务。由于真实世界时间序列具有极高的多样性（例如跨域分布差异）和固有的非平稳性（如趋势变化、异常值、噪声水平波动），冻结的 LTM 在泛化性与预测精度之间存在根本性权衡：一个在多数域上训练良好的模型，直接推送到未见域时往往无法一致地保持高性能。这一瓶颈的核心在于，模型的冻结参数无法吸收每个下游域的独特统计特性，造成预测退化。

现有应对方案主要围绕 **"模型适应数据"** 展开，即通过微调预训练参数来适配目标域。但微调不仅带来高昂的计算与存储开销，还可能破坏预训练阶段积累的通用知识，导致灾难性遗忘或过拟合。更需要一种保持模型冻结、仅通过调整输入来弥合域差异的方法，从而在维持模型通用性的同时提升特定域预测质量。图 1 中的示例直观地揭示了这一潜力：对 Moirai 的输入进行降采样可稳定其噪声预测；对 Timer 进行异常值检测和插值能纠正其对天气异常的误读；对 Chronos 进行一阶差分可诱导平稳性，帮助其捕捉汇率趋势。这些现象表明，**恰当的输入变换能够显著改变冻结模型的预测行为**，而统一、自动地找到最优变换配置是解决域适配挑战的关键。

基于此，本文提出 **"数据适应模型"** 的新范式，核心动机是：**在保持大规模时间序列基础模型冻结不变的前提下，通过自适应搜索最优的数据预处理管道，消除不同下游域之间的数据偏差，从而在多个域上显著提升预测准确性**。形式上，将问题建模为在历史数据上优化一个变换管道 $h$，使冻结模型 $M$ 的预测损失 $\mathcal{L}$ 最小化：

$$h^{*} = \operatorname*{min}_{h \in \mathcal{H}} \mathcal{L}(M, D_{history}, h)$$

其中 $\mathcal{H}$ 是由上下文切片、尺度归一化和异常值校正等三类共九种变换算子构成的搜索空间。借助该框架，模型无需任何参数更新，即可自适应地"适应"各域的数据特性。初步验证表明，此方法在多种先进 LTM 上均能实现一致且显著的域自适应预测提升，最高可降低 MSE 达 65.4%，平均降低 13.6%，充分证实了"数据适应模型"路线的可行性与巨大潜力。



## 核心方法与创新机理

现有时间序列基础模型（LTM）以冻结参数进行跨域预测时，面临一个根本性矛盾：真实数据的多样性与非平稳性使得单一模型无法在所有下游域保持一致的精度，而重新微调又会牺牲模型的通用能力。TATO 的关键突破在于将适应策略从"模型适应数据"反转为**数据适应模型**——在保持大规模预训练模型冻结不变的前提下，通过自动搜索最优的预处理变换管道，使原始数据以最适合该模型"口味"的形式输入，从而在不同域上大幅提升预测准确率。

相对于直接将冻结 LTM 应用于原始数据这一基线（即 vanilla FrozenForecasting），TATO 在四个核心槽位上引入实质性变更，每个槽位都直接服务于该适应机制并带来可测量的增益。

**输入预处理管道**  
基线依赖模型内置的简单标准化或无针对性的固定预处理，而 TATO 构建了一个由三类共 9 种算子组成的可配置变换流水线：上下文切片算子（Trimmer、Sampler、Aligner）用于调整回看窗口、采样率和序列长度对齐；尺度归一化算子（Scaler、Differencer、Warper）用于抑制量纲差异、诱导平稳性及对时序形状进行轻度扭曲；异常值校正算子（Denoisor、Imputator、Clipper）用于去除或压制离群噪声。这些算子并非固定执行，而是作为待优化的超参数空间，使变换管道能够针对特定数据分布进行定制。

**管道优化策略**  
基线缺乏对预处理管道的系统优化，TATO 将此建模为黑箱超参数搜索问题，采用树形 Parzen 估计器（TPE）这一贝叶斯优化算法，在由算子类型、参数范围构成的混合搜索空间中高效寻找最优管道配置。TPE 的引入使得搜索具有高效的方向性，相比随机或网格搜索能更快逼近对冻结模型最有利的变换组合，且完全不对模型权重进行任何修改。

**优化阶段的鲁棒性增强**  
在搜索最优管道时，若仅使用少量历史样本，搜索过程容易过拟合到特定的序列形态。TATO 在优化前对输入样本施加系统性的数据增强：时间翻转、时间扭曲、噪声注入（EWMA 平滑与抖动）、平移以及趋势斜率叠加等。这些增强不会改变预测任务的语义，却显著扩大了搜索暴露的样本多样性，迫使搜索算法找到对数据扰动鲁棒的变换管道，从而提升最终管道的泛化稳定性。

**管道选择标准**  
基线通常依据单一误差指标（如 MSE）选优，容易因局部波动陷入次优。TATO 提出一种两阶段帕累托排序方案：第一阶段使用多个误差指标的子集进行帕累托过滤，剔除在若干指标上表现明显落后的试验管道；第二阶段对保留的候选管道，在原始验证样本上计算加权多指标排名，综合选择最具鲁棒性的管道。这种设计兼顾了多目标一致性与筛选的可信度，是搜索阶段收益能够稳定转化为最终预测提升的重要保障。

上述四个变更槽位的协同作用，使 TATO 能够在多种基线 LTM（Timer-UTSD/LOTSA、Moirai 系列、Chronos-tiny）及 8 个广泛使用的数据集上，一致且显著地降低预测误差：MSE 最大降低 65.4%，平均降低 13.6%。消融实验进一步证实，去除 Trimmer 或 Scaler 等关键算子会导致性能大幅下降，而增加试验次数与样本数量能够持续提升优化效果，说明搜索框架本身亦具有良好的扩展性。这些证据表明，以数据为中心的自适应变换优化，是提升冻结时序基础模型域泛化能力的有效且可扩展的路径。



![[assets/figures/papers/iclr26_0006_uTK1SNgi1N_Adapt_Data_to_Model_Adaptive_Transformation_Opti/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the TATO framework. The framework consists of three main stages: (1) Data preparation, where diverse augmentations are applied to input samples to improve robustness; (2) Optimization of time series transformations, where a black-box optimizer searches for effective transformation pipelines comprising various preprocessing operators (e.g., trimming, normalization, denoising); and (3) Two-stage pipeline selection, where candidate pipelines are first filtered via Pareto ranking on validation metrics, followed by weighted multi-indicator ranking to select the optimal transformation pipeline for frozen LTM forecasting*

TATO (Time-series Adaptive Transformation Optimization) 是一个以数据为中心的自适应框架，其核心思想是"数据适应模型，而非模型适应数据"。该框架保持大规模预训练时间序列模型（LTM）完全冻结，通过自动搜索并优化应用于输入序列的**数据预处理变换管道**，使单个通用模型在不同下游预测域上均能获得显著性能提升。整个框架由三个顺序衔接的阶段构成，其总体结构与数据流如图 2 所示。

### 问题形式化

给定一个已冻结的预训练模型 $M$ 和目标域的历史数据 $D_{\text{history}}$，TATO 的目标是搜索一条最优的变换管道 $h^*$，使得模型在该历史数据上的预测损失最小：
$$h^{*} = \operatorname*{min}_{h \in \mathcal{H}} \mathcal{L}(M, D_{\text{history}}, h)$$
其中 $\mathcal{H}$ 为可选变换算子的组合空间，$\mathcal{L}$ 为预测损失（默认采用均方误差）。获得 $h^*$ 后，对后续新样本先施以 $h^*$ 再将变换后的序列馈入冻结模型，即可完成域自适应预测。

### 三阶段流水线

**阶段一：数据准备（Data Preparation）**  
为增强管道搜索的鲁棒性和泛化性，TATO 首先对从 $D_{\text{history}}$ 中均匀采样的训练实例施加多种时序增强。增强策略包括幅度翻转与时间翻转、幅度扭曲与时间扭曲、指数加权移动平均平滑与抖动噪声注入、平移变换以及斜率添加等。这些增强并不改变序列的语义身份，但能够模拟不同分布形态，从而避免优化过程过拟合于历史数据的特定模式。

**阶段二：变换管道优化（Transformation Pipeline Optimization）**  
该阶段是 TATO 的核心。搜索空间由三大类共 9 种变换算子构成：
- **上下文变换**：调整推理回看长度或采样频率，如 `Trimmer`、`Sampler`、`Aligner`。
- **尺度归一化变换**：调节值的范围与分布，如 `Scaler（STD/MinMax）`、`Differencer`、`Warper`。
- **异常值校正变换**：识别并处理异常点，如 `Denoisor`、`Imputator（IQR）`、`Clipper`。

每一条候选管道由上述算子的有序组合及其超参数（如保留点数、IQR 乘子等）构成。TATO 采用贝叶斯优化器——树形结构 Parzen 估计器（TPE）在黑箱设定下进行搜索。每一轮试验将采样得到的管道应用于增强后的历史数据，计算其在冻结模型上的平均预测损失，并将结果反馈给 TPE 以指导后续采样。优化预算（试验次数）预设为 500 次，每条管道在 500 个随机样本上评估。

**阶段三：两阶段帕累托管道选择（Two-Stage Pareto-Based Pipeline Selection）**  
由于单一损失指标难以全面反映管道在多步预测、多尺度上的表现，TATO 采用基于帕累托排序的两阶段筛选。第一阶段：在验证集上同时考察多个误差指标（如不同预测长度的 MSE），滤除那些在任意指标子集上均被其他候选占优的试验。第二阶段：对保留的候选管道，使用原始（未增强）样本重新评估，并计算加权多指标排名，最终选出综合排名最优的管道作为 $h^*$。该机制确保所选管道不仅在优化数据上表现良好，而且能够稳定泛化到未来样本。

### 输入输出流

- **输入**：目标域的历史时间序列集合 $D_{\text{history}}$ 及一个已冻结的大规模预训练模型 $M$。
- **处理流程**：`数据增强 → TPE 搜索（对每条管道：构建算子序列 → 变换增强样本 → 前传冻结模型得损失） → 两阶段帕累托选择`。
- **输出**：最优变换管道 $h^*$，可直接服务于该域后续所有预测请求。对于每个新的查询序列 $\mathbf{x}$，只需先计算 $\mathbf{x}' = h^*(\mathbf{x})$，再通过 $M(\mathbf{x}')$ 生成预测。

该框架将领域自适应问题转化为管道超参数搜索问题，规避了对模型参数的更新，从而在保持模型通用性的同时，实现跨域预测精度的大幅提升（MSE 平均降低 13.6%，最大降低 65.4%）。消融实验证实，完整的三阶段设计和全部算子配置能够带来最佳性能，其中 `Trimmer` 和 `Scaler` 算子的移除会导致性能显著下降，进一步验证了自适应管道优化的必要性。



TATO 在冻结大时间序列模型（LTM）前插入一个自适应搜索的变换管道，使同一模型适应不同下游域。其核心优化目标为

$$
h^{*} = \operatorname*{min}_{h \in \mathcal{H}} \mathcal{L}(M, D_{history}, h)
$$

其中 $M$ 为冻结的 LTM，$D_{history}$ 为目标域的历史数据，$\mathcal{L}$ 为预测损失，$h$ 为从变换空间 $\mathcal{H}$ 中选出的最优变换管道。搜索的目标是找到使历史损失最小的 $h$，直接优化输入而非模型参数。

### 核心模块

TATO 框架由三个模块构成（对应 Figure 2）：

1. **数据准备（增强模块）**  
   对历史输入施加翻转、扭曲、噪声注入、平移和趋势斜率添加等多种增强，扩大训练多样性，提升后续管道搜索对数据扰动的鲁棒性。

2. **变换流水线优化**  
   将九种算子（分属上下文、归一化、异常值三类）组成可搜索的变换管道，采用树状结构 Parzen 估计器（TPE）作为黑盒优化器，在增强后的历史数据上迭代评估候选管道，逐步逼近 $h^{*}$。

3. **两阶段帕累托排序选择**  
   第一阶段在验证集上用多个指标子集滤除劣质候选；第二阶段对保留的管道，在原始样本上计算加权多指标排名，最终选出泛化最优的变换管道，用于冻结 LTM 的推理。

### 关键公式与算子定义

以下给出体系中起决定性作用的变换算子，其超参数由 TPE 统一搜索。

**（1）上下文切片：Trimmer**

$$
T_{\mathrm{trimmer}}(\mathbf{x}, \mathbf{P}_{1}) = \mathbf{x}[\,\mathrm{len}(\mathbf{x}) - \mathbf{P}_{1} : \mathrm{len}(\mathbf{x})\,]
$$

保留输入 $\mathbf{x}$ 的最后 $P_1$ 个时间点，调整回溯窗口以匹配模型的适配范围。

**（2）尺度归一化：Scaler (STD)**

$$
T_{\mathrm{scaler(STD)}}(\mathbf{x}) = \frac{\mathbf{x} - \mu}{\sigma}
$$

将序列标准化为零均值、单位方差，其中 $\mu$ 和 $\sigma$ 分别为输入 $\mathbf{x}$ 的均值和标准差。

**（3）平稳化：Differencer (1)**

$$
T_{\mathrm{differencer(1)}}(\mathbf{x}) = \{\mathbf{x}_{t} - \mathbf{x}_{t-1} \mid t = 1, \dots, \mathrm{len}(\mathbf{x})\}
$$

一阶差分运算，削弱非平稳趋势，使模型更易捕获平稳残差中的模式。

**（4）异常点去除：Imputator (IQR)**

$$
T_{\mathrm{imputator(IQR)}}(\mathbf{x}, \mathbf{P}_{\mathbf{k}}) = \left\{\mathbf{x}_{t} \; \big| \; |\mathbf{x}_{t} - x_{M}| \leq \mathbf{P}_{\mathbf{k}} \cdot \mathrm{IQR}(\mathbf{x}) \right\}
$$

以中位数 $x_{M}$ 为中心，保留绝对偏差不超过 $P_k$ 倍四分位距（IQR）的点，滤除离群值。

**（5）极端值裁切：Clipper**

$$
{\cal T}_{\mathrm{clipper}}(\mathbf{x}, \mathbf{P}_{\mathbf{k}}) = \max\!\big(\min\!\big(\mathbf{x},\, \mathbf{Q}_3 + \mathrm{IQR} \cdot \mathbf{P}_{\mathbf{k}}\big),\, \mathbf{Q}_1 - \mathrm{IQR} \cdot \mathbf{P}_{\mathbf{k}}\big)
$$

将 $\mathbf{x}$ 的所有值限制在 $[\mathbf{Q}_1 - P_k \cdot \mathrm{IQR},\; \mathbf{Q}_3 + P_k \cdot \mathrm{IQR}]$ 区间内，防止极端值扭曲预测。

上述算子连同未列出的 Sampler、Aligner、Warper、Denoisor 等共同构成搜索空间。消融实验表明，移除 Trimmer 或 Scaler 会导致 MSE 提升大幅下降，证明这两个算子在跨域适应中具有关键作用。同时，增大变换试验次数和数据样本数可进一步提升 MSE 降低幅度，验证了搜索框架的可扩展性。

**评价指标**  
文中采用相对误差提升百分比衡量 TATO 相对 vanilla LTM 的改进：

$$
\%\mathrm{Promotion} = \frac{e_V - e_T}{e_V}
$$

其中 $e_V$ 为 vanilla 基线误差，$e_T$ 为 TATO 优化后的误差，正值表示误差降低。综合实验表明 TATO 平均降低 MSE 达 13.6%，最大降幅 65.4%。



## 实验与关键发现

TATO 在六种冻结大时间序列模型（LTM）和八个真实数据集上一致提升了域自适应预测性能，整体 MSE 平均降低 13.6%，最大降低达 65.4%。这一提升源于自适应变换管道对输入数据的非线性校正，而非模型参数的调整，从而缓解了冻结 LTM 在面对多样且非平稳时序时的泛化-精度权衡。

### 主要结果

在 **Table 1** 中，TATO 在所有模型-数据集组合上均获得了正向 %Promotion（误差相对降低率），计时器类（Timer-UTSD/LOTSA）、Moirai 系列和 Chronos-tiny 均受益。典型示例：Moirai-large 在 ETTm2 上 MSE 从 0.6783 降至 0.5100（降低 24.8%），Timer-UTSD 在 Exchange 上 MSE 从 0.4382 降至 0.3144（降低 28.3%）。即使原本性能较强的组合，如 Chronos-tiny 在 ETTh2 上也获得了 1.7% 的改善，表明优化空间普遍存在。

![[assets/figures/papers/iclr26_0006_uTK1SNgi1N_Adapt_Data_to_Model_Adaptive_Transformation_Opti/figures/003_Table_1.jpg]]
*Table 1: MSE and MAE reduction achieved by TATO across different models and datasets. Results are averaged over prediction horizons 24, 48, 96, 192. Positive %Promotion, in bold, indicates performance improvement (error reduction) achieved by TATO compared to the baseline frozen LTM. Best results in each row are highlighted in red, worst in blue*

从模型视角聚合（**Table 6**），Timer-LOTSA 的 MSE 平均提升达 24.80%，Chronos-tiny 为 14.50%，Moirai-large 为 14.00%。这验证了 TATO 对多种预训练范式（掩码重建、混合分布预测等）的兼容性。

误差分布的变化进一步证实一致性：**Figure 3** 显示 Chronos-tiny 在 ETTm2 上的 MAE 分布经 TATO 后整体左移且峰值更集中，说明变换管道稳定降低了尾部高误差样本的比例。

![[assets/figures/papers/iclr26_0006_uTK1SNgi1N_Adapt_Data_to_Model_Adaptive_Transformation_Opti/figures/006_Figure_3.jpg]]
*Figure 3: Distribution of MAE before and after applying TATO on three representative tasks. Across all datasets, TATO consistently shifts the error distribution toward lower values, indicating improved forecasting accuracy compared to the vanilla baseline*

### 消融实验

框架组件的消融（**Figure 5a**）表明，"去除 Trimmer 或 Scaler 算子"会导致性能大幅下降——MSE 降低率显著回落，验证了上下文切片和尺度归一化作为瓶颈变换的关键作用。完整配置（包含全部九种算子、三阶段流程和增强）实现了最佳的 MSE 均值与中位数降低。单独移除数据增强阶段同样会削弱最终管道的鲁棒性，因为搜索空间未充分覆盖目标域的变动模式。

![[assets/figures/papers/iclr26_0006_uTK1SNgi1N_Adapt_Data_to_Model_Adaptive_Transformation_Opti/figures/012_Figure_5.jpg]]
*Figure 5: Ablation study results. (a) Effect of removing key framework components on the reduction of MSE. (b) Effect of removing individual transformation operators on MSE reduction. Mean and median %Promotion are shown for each variant*

### 可扩展性与开销

TATO 的性能随超参搜索试次和历史样本数量增加而提升（**Figure 4**）：固定 100 个样本时，将试次从 50 增至 500，MSE %Promotion 平均值从 7.2% 升至 9.4%；固定 100 试次时，将样本从 50 增至 500，改善从 4.6% 升至 8.8%。二者均未出现饱和，表明更大的计算预算可以带来持续增益。

![[assets/figures/papers/iclr26_0006_uTK1SNgi1N_Adapt_Data_to_Model_Adaptive_Transformation_Opti/figures/010_Figure_4.jpg]]
*Figure 4: Scalability analysis of TATO. (a) MSE improvement with increasing transformation trials (fixed 100 samples). (b) MSE improvement with increasing sample size (fixed 100 trials). Performance consistently improves with more trials and data, ranging from 50 to 500 in both dimensions*

时间开销分析（**Table 2**）显示，即使配置为 500 试次和 500 样本，在中等规模 LTM（Moirai-base）上优化阶段耗时约 200 秒，对于离线场景可接受。更大试次数的进一步实验（**Table 7**）指出，1000 试次下时间成本约 491 秒，MSE 改善达 21.2%，建议实际应用中可根据精度需求选择预算。

### 联合微调的效果

在微调后的 LTM 上叠加 TATO（**Table 3**），多数数据集仍获得额外增益。例如 Timer-UTSD 在 Weather 上的 MSE 从微调后的 0.2685 降至 0.2589（提升 3.6%），说明数据侧优化与参数侧微调具有互补性：微调捕捉跨域共享模式，TATO 专化单域特异性统计特征。

![[assets/figures/papers/iclr26_0006_uTK1SNgi1N_Adapt_Data_to_Model_Adaptive_Transformation_Opti/figures/008_Table_3.jpg]]
*Table 3: Results of prediction using TATO upon finetuning. The average results under prediction lengths of {24,48,96,192} are reported. Positive %Promotion indicates performance enhancement*

### 失败模式与限制

- **高异质性域的边际/负增益**：在 Weather 等数据集上，不同模型增益参差不齐（Timer-UTSD 的 MSE %Promotion 接近零或为负）。天气数据的高度非平稳性可能超出了现有变换搜索空间的覆盖能力，需要更细粒度的局部分段处理或算子扩展。
- **依赖历史数据的代表性**：TATO 假设用于搜索的历史样本能够反映未来数据分布；若目标域出现剧烈概念漂移或采样偏差，所选管道可能失效，表现为优化阶段低验证误差但实际预测灾难性退化的风险。
- **单变量范围的限制**：当前管道仅设计用于单变量视图；直接迁移至多变量场景时，跨通道相关性可能被忽略，导致不同通道间的变换策略冲突。

### 关键图表证据摘要

| 图表 | 结论 |
|------|------|
| Table 1 | 全组合 MSE 降低均值为 13.6%，最大 65.4%，证实 TATO 泛化有效性 |
| Figure 3 | MAE 分布左移集中，说明误差尾部改善是提升的主要来源 |
| Figure 4 | 性能随试次和样本量单调递增，无饱和，可扩展性好 |
| Figure 5a | Trimmer/Scaler 缺失导致大幅退化，证明上下文与尺度校正是核心 |
| Table 3 | TATO 与微调兼容，可叠加使用获得额外收益 |

上述证据统一指向 TATO 的核心洞察：在冻结的共享基础模型之上，通过以数据为中心的变换搜索，能够低成本地恢复域特化精度，而无需触碰模型权重。该路径为时间序列基础模型的部署提供了新的实践范式。



## 定位与知识库关联

TATO 属于数据优先的域自适应策略，与模型微调形成两条正交路线。微调通过调整预训练时间序列大模型（LTM）的参数来捕捉跨域共性，TATO 则通过搜索数据预处理管道优化输入分布，使冻结的 LTM 在特定下游域中获得更好的预测能力。二者互补而非替代：实验表明，在已微调的 Timer-UTSD 与 Timer-LOTSA 上叠加 TATO 仍可获得进一步误差降低（如 Table 3 所示），说明数据侧优化能弥补模型侧微调的剩余泛化缺口。

从方法定位看，TATO 将域自适应问题重新表述为在固定模型 $M$ 下的管道优化问题：
$$h^{*} = \operatorname*{min}_{h \in \mathcal{H}} \mathcal{L}(M, D_{history}, h)$$
其中 $\mathcal{H}$ 是由上下文切片、尺度归一化和异常值校正三类共 9 个算子构成的变换空间，优化过程采用树状结构 Parzen 估计器（TPE），最终通过两阶段帕累托排序选择最优管道。这一方案与传统的固定预处理（如仅做标准化）形成鲜明对照，消融实验表明移除 Trimmer 或 Scaler 算子会显著削弱性能提升，而完整配置在 MSE 平均降低幅度上取得最优。按模型视角统计，Timer-LOTSA 的 MSE 平均提升达 24.8%，Chronos-tiny 为 14.5%，Moirai-large 为 14.0%，验证了该方法对不同架构 LTM 的普适性。

### 适用边界

TATO 的主要应用前提是下游域存在一段可用的历史数据，且该历史数据能大致代表未来预测任务的分布特性。在数据集 Weather 上，部分模型（如 Timer-UTSD）的 MSE 提升极小甚至为负，提示当时间序列的高变异性与噪声掩盖了数据中的稳定模式时，纯数据侧变换的增益可能有限。类似地，Moirai-large 在 Exchange、Chronos-tiny 在 ETTh2 等组合上提升幅度较低，反映当前算子集对趋势反转或分布骤变的适应能力尚有不足。此外，当前方法仅针对单变量预测场景验证，多变量联合预测尚未覆盖，直接扩展需要额外的变换设计。

### 局限与开放问题

1. **搜索空间与算子集的静态性**：TATO 的变换空间预定义为 9 个启发式算子，未包含面向特定领域的新算子（如季节性分解、时频域变换），也未支持自适应算子选择。极端域偏移可能要求超出当前空间的预处理步骤，此时固定算子集可能不足以实现有效适应。

2. **优化开销与数据效率**：尽管 TATO 的优化阶段开销在合理范围内（500 试次量级耗时约数百秒，Table 2），但当历史样本稀缺时（如 < 50 个样本），性能提升从 8.8% 降为 4.6%（Figure 4b），表明数据效率仍可改进。

3. **开放扩展方向**：论文指出三个明确的后续工作：将 TATO 推广至多变量时间序列；丰富算子库以覆盖专业化领域；探索自适应算子选择机制以减少超参空间的人工预设。此外，如何利用生成式增强或元学习从多域历史中学习变换先验，以降低每个新域的搜索成本，也是值得探索的路径。

> 注：以上局限分析主要基于原文实验与讨论中提及的改进点，部分开放问题在现有材料中仅以概要形式出现，未来方向的可行性需结合具体实施验证。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Adapt_Data_to_Model_Adaptive_Transformation_Optimization_for_Domain_shared_Time_Series_Foundation_Models.pdf

![[paperPDFs/ICLR_2026/Adapt_Data_to_Model_Adaptive_Transformation_Optimization_for_Domain_shared_Time_Series_Foundation_Models.pdf]]
