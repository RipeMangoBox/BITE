---
title: "TabStruct: Measuring Structural Fidelity of Tabular Data"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/TabStruct_Measuring_Structural_Fidelity_of_Tabular_Data.pdf
openreview_forum_id: XOPH34Extq
aliases:
- TabStruct
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "引入无需真实因果结构图的全局效用（global utility）指标，作为全局结构保真度的代理。"
primary_logic: "通过将每个特征作为预测目标并聚合预测性能，可以在无真实因果图的情况下可靠地评估生成数据的全局结构保真度。"
claims:
- "全局效用（global utility）与全局CI得分之间存在强Spearman秩相关（rs=0.84, p<0.001），验证了其作为结构保真度代理的有效性。"
- "在真实世界数据集上，全局效用产生的生成器排名与SCM数据集上的全局CI排名高度一致，表明其可推广至无真实因果图的场景。"
- "传统指标（如ML效能、密度估计）与全局CI的相关性较弱，且SMOTE等模型虽局部效能高但全局结构保真度低，凸显了全局效用作为补充评估维度的必要性。"
- "Six SCM datasets 上 Spearman's rank correlation with Global CI = 0.84 (global utility)"
---

# TabStruct: Measuring Structural Fidelity of Tabular Data

> [!tip] 核心洞察
> 通过将每个特征作为预测目标并聚合预测性能，可以在无真实因果图的情况下可靠地评估生成数据的全局结构保真度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | TabStruct：测量表格数据的结构保真度 |
| 英文题名 | TabStruct: Measuring Structural Fidelity of Tabular Data |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=XOPH34Extq); [GitHub](https://github.com/SilenceX12138/TabStruct) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | TabStruct（包含全局效用指标的结构保真度评估框架） |
| Dataset | Six SCM datasets, 23 real-world datasets |

> [!tip] 效果简介
> - Six SCM datasets 上，Spearman's rank correlation with Global CI 为 0.84 (global utility)，对比 0.14 (local utility)，变化 +0.70。
> - 23 real-world datasets 上，Evaluation time per 1000 samples (s) 为 0.64 (global utility Tiny-default)，对比 1.21 (local utility Full-tuned)，变化 -0.57。

## 概述

表格数据生成模型近年来迅速发展，但现有评估范式主要关注密度估计、机器学习效能和隐私保护等维度，忽略了生成数据与真实数据在**因果结构**上的一致性——即结构保真度（structural fidelity）。这一盲区导致评估结果可能产生误导：某些生成器虽在传统指标上表现优异，却无法复现变量间的条件依赖关系，从而在需要因果推理的下游应用中引发系统性风险。

**核心瓶颈**在于：现有结构保真度评估方法依赖真实因果结构图（SCM），而真实世界数据通常缺乏可用的因果图，使得结构层面的评估在实践中几乎不可行。

针对这一瓶颈，本文提出 **TabStruct**——一个统一的表格生成模型评估框架，核心贡献包括：

1. **将结构保真度确立为独立评估维度**，与密度估计、ML效能、隐私保护并列，形成四维评估体系。
2. **提出全局效用（global utility）指标**：通过将每个特征作为预测目标、聚合异构预测器集成的预测性能，在无需真实因果图的情况下可靠地评估全局结构保真度。
3. **构建大规模基准**：覆盖29个数据集（含6个SCM数据集和23个真实世界数据集）、13个生成器（横跨9个类别），完成超过150,000次评估。

**核心洞察**：全局效用的设计基于一个关键观察——若生成数据保留了变量间的条件依赖结构，则从其他变量预测每个目标变量的性能应与真实数据相近。这一代理指标在SCM数据集上与真实全局CI得分达到强Spearman秩相关（$r_s = 0.84, p < 0.001$），验证了其作为结构保真度代理的有效性。

**主要发现**：
- 传统指标（ML效能、密度估计）与全局CI的相关性较弱，凸显了结构保真度作为补充评估维度的必要性。
- 不同生成器类别在局部与全局结构学习上呈现分化：SMOTE等插值方法局部保真度高但全局结构差，扩散模型（如TabDDPM、TabSyn）则在全局结构上表现更优。
- 全局效用对下游预测器选择具有高度鲁棒性，且计算开销可控（Tiny-default配置下每千样本仅需0.64秒）。

**方法定位**：TabStruct不依赖真实因果图即可评估结构保真度，填补了现有基准在真实世界场景下的评估空白，为表格生成模型的全面诊断提供了实用工具。

## 背景与动机

表格数据是医疗、金融、工业等领域最普遍的数据形态，表格生成模型近年来取得了显著进展，涵盖变分自编码器、扩散模型、自回归Transformer等多个技术路线。然而，评估这些生成模型的保真度（fidelity）仍然是一个悬而未决的挑战。

现有评估范式主要关注三个维度：**统计相似性**（如列分布、成对相关性）、**机器学习效能**（合成数据训练、真实数据测试）和**隐私保护**（如成员推断攻击）。这些指标虽然必要，却共同忽略了一个关键维度——**结构保真度**（structural fidelity），即合成数据是否忠实地保留了原始数据中变量之间的因果依赖关系。

这一缺失的后果是深远的。如 Figure 1 所示，一个物理系统中球的密度、体积、质量和重力之间存在确定的因果结构；如果生成模型仅匹配边际分布和成对相关性，却颠倒了“体积→质量”的因果方向，那么基于合成数据的科学推断将产生系统性偏差。在医疗诊断、政策评估等高风险场景中，这种结构失真可能导致灾难性的决策失误。

现有工作对结构保真度的探索存在三个核心瓶颈：

1. **对真实因果图的强依赖**：现有的结构评估方法（如 CauTabBench）需要已知的因果结构图（SCM）作为参照。然而，在绝大多数真实世界数据集中，真实的因果图是不可得的，这使得此类方法无法推广到实际应用场景。

2. **缺乏有效的代理指标**：传统指标（如 ML 效能、密度估计）与全局结构保真度之间的相关性较弱。实验证据表明，SMOTE 等生成模型虽然在局部 ML 效能上表现良好，但其全局结构保真度显著偏低（Figure 3 left, Section 4.3），说明现有指标无法可靠地反映结构层面的保真度。

3. **评估规模与覆盖面的局限**：以往基准研究在数据集数量、生成器种类和评估维度上均较为有限，难以提供系统性的比较结论。

正是在这一背景下，TabStruct 提出了一个统一的评估框架，将结构保真度确立为表格生成模型的核心评估维度。其核心创新在于引入**全局效用（global utility）**指标——通过将每个特征作为预测目标并聚合预测性能，在无需真实因果图的前提下可靠地评估生成数据的全局结构保真度。这一设计消除了对先验因果知识的依赖，使得结构保真度评估首次可推广至真实世界数据集。

## 核心创新

TabStruct 的核心创新在于将**结构保真度（structural fidelity）**系统性地引入表格生成模型的评估框架，并解决了现有评估范式中一个关键瓶颈：**真实世界数据缺乏可用的因果结构图（SCM），导致结构保真度评估无法落地**。

### 瓶颈突破：从“依赖因果图”到“无 SCM 评估”

现有表格生成评估主要关注密度估计、机器学习效能和隐私保护等维度，但忽视了生成数据是否保留了原始数据的因果结构。部分工作虽已意识到结构保真度的重要性，却面临一个根本性约束——评估需要真实因果结构图作为参照。在绝大多数真实数据集上，这样的因果图并不可得，使得结构保真度评估长期停留在拥有专家验证 SCM 的少量合成数据集上。

TabStruct 的突破在于引入了一个**无需真实因果图的代理指标——全局效用（global utility）**，将结构保真度评估从“必须有 SCM”的约束中解放出来，使其可推广至任意真实世界表格数据。

### 核心洞察：预测性能作为结构保真度的代理

全局效用的设计基于一个简洁而有力的洞察：**如果生成数据保留了原始数据的全局因果结构，那么以每个特征为预测目标、利用其他特征进行预测的性能，应当与在真实数据上的预测性能一致**。这一洞察将结构保真度评估转化为一个可操作的预测任务聚合问题。

具体而言，全局效用将数据集的每个变量依次作为预测目标，使用异构预测器集成（AutoGluon + TabPFN）计算其归一化预测性能，再对所有变量的效用值取平均。归一化设计（公式 4）使得效用值 $\\geq 1$ 表示生成数据的预测性能不劣于参考数据，从而直接反映结构信息的保留程度。

### 关键证据：全局效用与全局 CI 的强相关性

在六个拥有真实因果图的 SCM 数据集上，全局效用与全局 CI 得分之间的 Spearman 秩相关系数达到 **$r_s = 0.84$（$p < 0.001$）**，验证了其作为结构保真度代理的有效性（Table 2, Figure 3 左图）。相比之下，传统指标（如 ML 效能、密度估计）与全局 CI 的相关性显著较弱，且 SMOTE 等模型虽在局部 ML 效能上表现良好，但全局结构保真度却很低——这凸显了将全局效用作为独立评估维度的必要性。

更重要的是，在 23 个真实世界数据集上，全局效用产生的生成器排名与 SCM 数据集上的全局 CI 排名高度一致，表明该指标能够可靠地迁移至无真实因果图的场景，从而实现了评估框架对真实数据的覆盖。

### 评估框架的系统性升级

除核心指标创新外，TabStruct 在评估规模和维度上实现了对以往基准的全面超越：

- **结构保真度维度**：新增局部/全局条件独立性（CI）得分，以及无需真实因果图的全局效用指标，覆盖了此前基准中缺失的结构评估维度（Figure 1, Table 1）。
- **评估规模**：涵盖 29 个数据集（含 SCM 与真实世界）、13 个生成器（覆盖 9 个类别），累计超过 150,000 次评估，远超以往工作的覆盖范围。
- **评估层级**：在 CPDAG（完备部分有向无环图）层面评估结构保真度，而非骨架或 DAG 层面，在语义丰富性与计算可行性之间取得平衡。

### 消融验证的关键发现

全局效用的可靠性得到了多项消融实验的支持：

- **预测器鲁棒性**：即使使用轻量级的“Tiny-default”配置，全局效用仍能产生与“Full-tuned”一致的生成器排名，表明该指标对下游预测器的选择不敏感（Appendix B.2.2, E.4）。
- **归一化的必要性**：若采用绝对预测性能而非归一化效用，与全局 CI 的相关性大幅下降（$r_s = 0.57$ vs 归一化后的 $r_s = 0.84$），验证了归一化设计对消除数据集难度差异的关键作用（Table 27）。
- **样本量影响**：当合成样本量达到或超过参考数据时，全局效用趋于饱和，说明足够的样本量是可靠评估的前提（Table 30, Appendix E.3）。
- **因果顺序对齐**：沿真实因果顺序微调的自回归模型（GReaT-sort）相比原始 GReaT 显著提高了全局效用，说明列顺序与因果结构的对齐对模型的结构学习至关重要（Table 31, Appendix E.3）。

### 方法定位

TabStruct 并非提出新的生成模型，而是提供了一个**统一的评估框架**，将结构保真度与密度估计、ML 效能、隐私保护等传统维度并列，形成对表格生成模型的多维评价体系。其核心贡献在于让结构保真度评估从“有 SCM 才能做”的奢侈品，变成“任意真实数据都能做”的标配工具。

## 整体框架

TabStruct 提出了一套统一的表格生成模型评估框架，其核心创新在于将**结构保真度**（structural fidelity）作为与传统评估维度并列的核心评价轴。框架的整体设计围绕一个关键瓶颈展开：现有评估体系缺乏对生成数据因果结构保真度的有效度量，且需要真实因果结构图（SCM）才能进行评估，而这在真实世界数据中几乎不可得。

### 框架总览

如图 Figure 2 所示，TabStruct 的评估框架由四个主要评估维度构成：

- **结构保真度**：通过条件独立性（CI）得分和全局效用（global utility）指标，评估合成数据是否保留了原始数据的因果结构。
- **机器学习效能**：衡量合成数据在下游预测任务上的表现。
- **密度估计**：评估合成数据分布与真实数据分布的匹配程度。
- **隐私保护**：检测合成数据是否存在泄露训练样本的风险。

这些维度共同覆盖了表格生成模型评估的关键方面，而结构保真度是此前基准工作中被系统性忽视的维度（参见 Table 1 的评估范围对比）。

### 核心评估流水线

框架的评估流水线由五个标准化模块串联而成，确保不同生成器和数据集之间的可比性：

1. **数据准备与分割**：对每个数据集执行训练/验证/测试集划分，进行缺失值填充和特征标准化（数值特征采用 Z-score 归一化，类别特征采用 one-hot 编码），为后续所有模块提供一致的输入格式。

2. **生成器训练与超参搜索**：使用 Optuna 对 13 个生成器进行超参数优化，以最小化验证损失为目标；每个生成器的单次重复运行限时 2 小时，保证实验的可行性和可复现性。

3. **多维指标计算**：并行计算密度估计、隐私保护、ML 效能和结构保真度四类指标。其中结构保真度指标在 SCM 数据集上可直接计算 CI 得分，在真实世界数据集上则依赖全局效用作为代理。

4. **全局效用计算**：这是框架的关键创新模块。其核心思想是：将数据集中的每个变量依次作为预测目标，利用九种异构预测器的集成（AutoGluon + TabPFN），衡量该变量能否被其余变量有效预测。对每个变量计算归一化的相对预测性能（Utility），然后取所有变量 Utility 的平均值作为全局效用。这一设计使得全局效用**无需真实因果图**即可反映生成数据的全局结构保真度。

5. **结果聚合与排名**：采用平均距离到最小值（ADTM）仿射重归一化方法，将多指标、多数据集的结果汇总为统一的生成器排名，便于跨维度比较。

### 输入输出流

框架的输入为原始表格数据集和待评估的生成模型，输出为各维度归一化指标值及生成器的综合排名。在 SCM 数据集上，全局 CI 得分作为结构保真度的金标准；在真实世界数据集上，全局效用作为其可计算的代理指标。实验验证表明，全局效用与全局 CI 得分之间存在强 Spearman 秩相关（rₛ = 0.84, p < 0.001），确认了该代理的有效性。

### 关键设计决策

框架在结构保真度评估上做出了两个重要设计选择：

- **CPDAG 级别的评估**：不要求恢复完整的 DAG 或仅检查骨架（skeleton），而是在 CPDAG（完备部分有向无环图）层面评估，这平衡了语义丰富性和计算可行性。
- **归一化效用的必要性**：消融实验表明，若使用绝对预测性能而非归一化效用计算全局效用，其与全局 CI 的相关性会从 rₛ = 0.84 大幅下降至 rₛ = 0.57，验证了归一化设计的必要性。

## 核心模块与公式推导

### 结构保真度的形式化定义

TabStruct 将表格数据的结构保真度定义为生成数据与真实数据在因果结构层面的对齐程度。由于真实因果结构通常不可直接观测，框架选择在 **马尔可夫等价类（Markov equivalence class）** 层面进行评估，即将因果结构表示为 **CPDAG**（Completed Partially Directed Acyclic Graph）。在此层面，两个 SCM 等价当且仅当它们蕴含相同的条件独立性（Conditional Independence, CI）语句集合。

基于此，框架从两个粒度定义结构保真度：

- **全局结构保真度**：评估数据是否保留了全部变量间的因果依赖关系，对应完整的 CI 语句集合 $\mathcal{C}_{\text{global}}$。
- **局部结构保真度**：聚焦于预测目标 $y$ 直接涉及的 CI 语句，评估与下游任务最相关的局部因果结构。

### 核心指标：CI 得分

CI 得分是量化结构保真度的直接指标。给定 CI 语句集合 $\mathcal{C}$ 和数据集 $\mathcal{D}$，CI 得分定义为在所有语句中被统计检验接受的比例：

$$\operatorname{CI}(\mathcal{C}, \mathcal{D}) = \frac{1}{|\mathcal{C}|} \sum_{\mathcal{C}} \mathbb{1}\left[\widehat{\mathcal{T}}_{\alpha}(\pmb{x}_{j}, \pmb{x}_{k} \mid S_{j,k}, \widehat{S}_{j,k}; \mathcal{D}) = 1\right]$$

其中：
- $\mathcal{C}$ 为待检验的 CI 语句集合（全局或局部）；
- $\widehat{\mathcal{T}}_{\alpha}(\cdot)$ 为 CI 检验指示函数，在显著性水平 $\alpha = 0.01$ 下判断给定条件独立性是否成立；
- $S_{j,k}$ 为真实因果图中变量 $\pmb{x}_j$ 和 $\pmb{x}_k$ 的 d-分离集，$\widehat{S}_{j,k}$ 为对应的依赖集；
- 得分取值范围为 $[0, 1]$，值越高表示合成数据与真实因果结构越一致。

全局 CI 语句集合 $\mathcal{C}_{\text{global}}$ 由真实 SCM 导出，包含所有条件独立语句及其非独立对偶语句，完整刻画了数据的全局因果依赖拓扑。

### 瓶颈突破：全局效用指标

全局 CI 得分需要真实因果图，这在实际场景中几乎不可得。为突破这一瓶颈，TabStruct 提出 **全局效用（global utility）** 作为无需 SCM 的结构保真度代理指标。其核心洞察是：如果生成数据保留了真实数据的全局因果结构，那么以任一变量为预测目标、以其余变量为特征的预测性能应与参考数据一致。

**逐变量效用** 定义为相对预测性能：

$$\mathrm{Utility}_j(\mathcal{D}) := \begin{cases} \mathrm{Perf}_j(\mathcal{D}_{\mathrm{ref}})^{-1} \cdot \mathrm{Perf}_j(\mathcal{D}), & \text{if } x_j \text{ is categorical}, \\ \mathrm{Perf}_j(\mathcal{D})^{-1} \cdot \mathrm{Perf}_j(\mathcal{D}_{\mathrm{ref}}), & \text{if } x_j \text{ is numerical}. \end{cases}$$

其中 $\mathrm{Perf}_j(\mathcal{D})$ 表示以变量 $x_j$ 为目标、数据集 $\mathcal{D}$ 中其余变量为特征时的预测性能（分类用 ROC AUC，回归用 $R^2$）。该比值以参考数据 $\mathcal{D}_{\text{ref}}$ 为基准进行归一化，$\mathrm{Utility}_j \geq 1$ 表示生成数据在该变量上的可预测性不劣于参考数据。

**全局效用** 取所有变量效用的均值：

$$\mathrm{Global\ Utility}(\mathcal{D}) := \frac{1}{D+1} \sum_{j=1}^{D+1} \mathrm{Utility}_j(\mathcal{D})$$

其中 $D$ 为特征数，$D+1$ 包含预测目标 $y$。该指标通过聚合所有变量的预测性能，隐式捕获了变量间的全局依赖结构，无需显式推断因果图。

### 全局效用的计算管线

全局效用的计算依赖异构预测器集成以保证鲁棒性。框架采用 AutoGluon 与 TabPFN 的九模型集成，对每个变量独立训练预测器。关键设计选择包括：

- **归一化必要性**：消融实验表明，若采用绝对预测性能而非归一化效用，与全局 CI 的 Spearman 秩相关从 $r_s = 0.84$ 骤降至 $r_s = 0.57$，证实归一化对消除数据集难度差异至关重要。
- **预测器鲁棒性**：即使使用轻量级“Tiny-default”配置，全局效用仍能产生与“Full-tuned”一致的生成器排名，表明指标对下游预测器选择不敏感。
- **样本量要求**：当合成样本量达到或超过参考数据规模时，全局效用趋于饱和，提示足够的样本量是可靠评估的前提。

## 实验与分析

### 基准有效性验证

TabStruct 基准的合理性首先体现在参考数据（D_ref）的表现上：除隐私指标外，参考数据在所有评估维度上均获得最高分（Table 2），这与“真实数据应是最优生成结果”的直觉一致，验证了评估框架的内在一致性。

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_XOPH34Extq/figures/004_Table_2.jpg]]
*Table 2: Benchmark results of 13 tabular generators on 29 datasets. We report the normalised mean std metric values across datasets. “N/A” denotes that a specific metric is not applicable. We highlight the First, Second and Third best performances for each metric. For visualisation, we abbreviate “conditional independence” as “CI”. The results show that the Top-3 methods in Global CI and Global utility are largely consistent between SCM and real-world datasets. This alignment suggests that the selected SCM datasets represent real-world causal structure, and global utility can serve as an effective metric for global structural fidelity when ground-truth SCM is unavailable*

一个关键发现是，现有评估指标与全局 CI 得分之间缺乏强相关性（Figure 3 left）。无论是密度估计指标还是 ML 效能指标，均无法可靠地反映生成数据的全局结构保真度。这揭示了当前表格生成评估体系中的一个重要盲区：模型可能在传统指标上表现优异，却严重偏离真实数据的因果结构。

### 全局效用作为结构保真度代理的有效性

全局效用（global utility）作为无需真实因果图的结构保真度指标，其有效性通过两项核心证据得到验证：

1. **与全局 CI 的强相关性**：在 6 个 SCM 数据集上，全局效用与全局 CI 得分的 Spearman 秩相关系数达到 **r_s = 0.84（p < 0.001）**，而局部效用仅为 r_s = 0.14（Table 2, Figure 3 left）。这一差距表明，仅关注预测目标变量的局部结构不足以捕捉生成数据的整体因果保真度，必须从全局视角进行评估。

2. **跨场景的排名一致性**：在 23 个真实世界数据集上，全局效用产生的生成器排名与 SCM 数据集上的全局 CI 排名高度一致。这意味着全局效用可以在无法获取真实因果图的实际场景中，可靠地延续基于因果图的结构评估逻辑。

### 归一化的必要性

消融实验表明，归一化处理对全局效用的有效性至关重要。若直接使用绝对预测性能（而非相对于参考数据的归一化性能），全局效用与全局 CI 的相关性显著下降（r_s = 0.57 vs. 归一化后的 0.84，Table 27）。这是因为绝对预测性能受数据集固有可预测性的影响，而归一化有效消除了这一混杂因素，使指标聚焦于合成数据相对真实数据的结构退化程度。

### 下游预测器配置的鲁棒性

全局效用对预测器选择表现出高度鲁棒性。即使使用计算开销极低的“Tiny-default”配置（未调参的轻量预测器集成），其产生的生成器排名与“Full-tuned”配置（完整调参的预测器集成）高度一致（Appendix B.2.2, Appendix E.4）。这一特性使得全局效用在计算资源受限的场景下仍具实用价值。

### 计算效率

在 23 个真实世界数据集上，全局效用（Tiny-default 配置）的评估时间为每千样本 **0.64 秒**，低于局部效用（Full-tuned 配置）的 1.21 秒（Figure 4）。这表明全局效用不仅评估维度更全面，在计算效率上也具有优势，适合大规模生成器评估任务。

### 生成器结构学习行为分析

Table 2 和 Figure 3（right）揭示了不同生成器在结构保真度上的显著差异：

- **SMOTE 和贝叶斯网络（BN）** 虽然在局部效用上表现尚可，但全局效用得分较低，说明这些模型倾向于保留预测目标周围的局部结构，却无法维持变量间的全局依赖关系。
- **基于深度学习的生成器**（如 TVAE、CTGAN）在全局结构保真度上表现各异，部分模型在密度估计上接近真实数据，但结构保真度明显不足，进一步印证了结构保真度作为独立评估维度的必要性。
- **自回归模型的行为**值得关注：沿真实因果顺序微调的自回归模型（GReaT-sort）相比原始 GReaT 显著提高了全局效用（Table 31），说明列顺序与因果结构的对齐对模型学习变量间依赖关系具有重要影响。

### 样本量的影响

当合成样本量达到或超过参考数据规模时，全局效用趋于饱和（Table 30）。这表明足够的样本量是可靠评估的前提，样本不足可能导致对结构保真度的低估。

### 局限性

需要强调的是，全局效用作为全局结构保真度的代理指标，不能直接量化特定因果边的保真度或局部干预效果。对于需要精确评估某条特定因果关系是否被保留的场景，仍需借助基于因果图的局部 CI 得分。此外，在存在强隐混杂变量的情况下，全局效用与基于 MAG（Maximal Ancestral Graph）的全局 CI 之间虽有统计显著的相关性，但其理论性质尚未完全论证。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_XOPH34Extq/figures/003_Table_1.jpg]]
*Table 1: Evaluation scope comparison between TabStruct and prior tabular generative modelling benchmarks. TabStruct presents a comprehensive evaluation framework for tabular generative models, incorporating a wide range of evaluation dimensions, datasets, and generator categories*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_XOPH34Extq/figures/010_Table_3.jpg]]
*Table 3: onsidered tabular datasets between TabStruct and prior studies. TabStruct introduces a novel benchma tive models, with particular emphasis on evaluating the underlying structure of tabular data. It offers a divers d regression tasks, thereby supporting comprehensive and structure-aware evaluation ac*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_XOPH34Extq/figures/011_Table_4.jpg]]
*Table 4: g a comprehensive and systematic comparison across a broad spectrum of gen*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_XOPH34Extq/figures/012_Table_5.jpg]]
*Table 5: Details of three SCM classification datasets from bnlearn (Scutari, 2011)*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_XOPH34Extq/figures/013_Table_6.jpg]]
*Table 6: Details of three SCM regression datasets from bnlearn (Scutari, 2011)*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_XOPH34Extq/figures/014_Table_7.jpg]]
*Table 7: Details of five classification datasets with large SCMs from bnlearn (Scutari, 2011)*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_XOPH34Extq/figures/015_Table_8.jpg]]
*Table 8: Details of 14 real-world classification datasets*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_XOPH34Extq/figures/016_Table_9.jpg]]
*Table 9: Details of nine real-world regression datasets*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_XOPH34Extq/figures/018_Table_10.jpg]]
*Table 10: Hyperparameter search space of BN*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_XOPH34Extq/figures/019_Table_11.jpg]]
*Table 11: Hyperparameter search space of TVAE*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_XOPH34Extq/figures/020_Table_12.jpg]]
*Table 12: Hyperparameter search space of GOGGLE*

## 方法谱系与知识库定位

### 1. 问题定位：表格生成评估中的结构盲区

现有表格生成模型的评估范式存在一个核心盲区：它们几乎完全依赖统计保真度（如密度估计、列分布匹配）和下游任务效能（如 ML 效能）来评判生成质量，却系统性地忽略了**结构保真度**（structural fidelity）——即生成数据是否保留了原始数据中的因果依赖关系。Figure 1 通过一个物理系统示例直观地说明了这一差距：两个生成器可能产生统计上高度相似的数据，但其中一个完全破坏了变量间的因果方向，导致干预效果的错误推断。

这一盲区的根源在于，现有评估框架（如 SynthEval、SynMeter 等）在设计时未将因果结构纳入评估维度，而少数涉及因果结构的基准（如 CauTabBench）又需要真实的因果结构图（SCM）作为参照，这在绝大多数真实世界数据中不可得。Table 1 系统性地对比了 TabStruct 与先前基准的评估范围，突出了后者在结构保真度维度上的缺失。

### 2. 方法突破：从 SCM 依赖到 SCM-free 的结构评估

TabStruct 的核心贡献在于构建了一个**阶梯式**的结构保真度评估体系：

- **第一层：基于真实 SCM 的 CI 得分**。在已知因果结构图的数据集上，TabStruct 定义了局部 CI 得分（仅涉及预测目标 $y$ 的条件独立语句）和全局 CI 得分（覆盖全部条件独立语句），在 CPDAG 层面（而非骨架或 DAG 层面）评估生成数据与真实因果结构的一致性。这一设计平衡了语义丰富性与计算可行性。

- **第二层：无需 SCM 的全局效用（global utility）**。这是 TabStruct 最具创新性的贡献。其核心洞察是：如果生成数据保留了原始数据的全局因果结构，那么以每个变量为预测目标、用其余变量进行预测时，其预测性能应与在参考数据上的性能相当。具体而言，全局效用将每个特征 $x_j$ 作为预测目标，利用九种异构预测器的集成（AutoGluon + TabPFN）计算归一化预测性能，再对所有变量取平均：

$$\mathrm{Global\ Utility}(\mathcal{D}) := \frac{1}{D+1} \sum_{j=1}^{D+1} \mathrm{Utility}_j(\mathcal{D})$$

其中每个变量的效用通过相对预测性能定义，使得 $\geq 1$ 表示性能不劣于参考数据。

这一指标的巧妙之处在于：它**不需要真实的因果结构图**，却能够有效代理全局结构保真度。Table 2 和 Figure 3 提供了关键证据：在六个已知真实 SCM 的数据集上，全局效用与全局 CI 得分之间的 Spearman 秩相关系数高达 **$r_s = 0.84$（$p < 0.001$）**，而局部效用仅为 $r_s = 0.14$。更重要的是，在 23 个真实世界数据集上，全局效用产生的生成器排名与 SCM 数据集上的全局 CI 排名高度一致，验证了其向无因果图场景的可推广性。

### 3. 与现有评估维度的关系：互补而非替代

Figure 3（左）的相关性热图揭示了一个重要发现：**传统评估指标（ML 效能、密度估计等）与全局 CI 的相关性普遍较弱**。这意味着，仅凭现有指标无法可靠地判断生成数据是否保留了因果结构。一个典型案例是 SMOTE：该模型在局部 ML 效能上表现良好，但全局结构保真度显著偏低，表明它虽然能生成对下游任务有用的样本，却破坏了变量间的全局依赖关系。

因此，全局效用并非要替代现有指标，而是作为一个**补充评估维度**，填补了结构保真度这一长期被忽视的评估空白。Table 2 的综合基准结果（覆盖 13 个生成器、29 个数据集、150,000+ 次评估）表明，只有同时考虑统计保真度、ML 效能和结构保真度，才能对表格生成模型形成全面的评判。

### 4. 适用边界与已知局限

尽管全局效用在实验中表现出色，其适用边界需要审慎界定：

- **局部结构的不可见性**：全局效用衡量的是整体因果结构的保留程度，但**不能直接量化特定因果边的保真度**，也无法评估局部干预效果。对于需要精确控制特定变量间因果关系的下游应用，仍需依赖基于 SCM 的局部 CI 得分。

- **计算效率的权衡**：Figure 4 显示，全局效用的 "Tiny-default" 配置在每 1000 样本上仅需 0.64 秒，显著快于局部效用的 "Full-tuned" 配置（1.21 秒）。但对于特征数超过 100 的大规模数据集，计算时间仍可能成为瓶颈。

- **隐混杂变量的理论缺口**：在存在强隐混杂变量时，全局效用与基于 MAG（Maximal Ancestral Graph）的全局 CI 之间虽有统计显著的相关性，但其理论性质尚未完全论证。这是一个需要进一步理论分析的方向。

- **单表数据的限制**：当前基准主要关注单表数据，对多表关联或时间序列表格数据的扩展仍有待探索。

### 5. 关键消融发现与设计选择

几项消融实验进一步揭示了全局效用设计中的关键选择：

- **归一化的必要性**：若直接使用绝对预测性能而非归一化效用，与全局 CI 的相关性从 $r_s = 0.84$ 骤降至 $r_s = 0.57$（Table 27），表明相对性能的比较对于消除数据集难度差异至关重要。

- **预测器选择的鲁棒性**：全局效用对下游预测器的选择高度鲁棒，即使使用计算开销极低的 "Tiny-default" 配置，仍能产生与 "Full-tuned" 一致的生成器排名。

- **样本量的饱和效应**：当合成样本量达到或超过参考数据时，全局效用趋于饱和（Table 30），提示足够的样本量是可靠评估的前提。

- **列顺序与因果结构的对齐**：沿真实因果顺序微调的自回归模型（GReaT-sort）相比原始 GReaT 显著提高了全局效用（Table 31），说明表格数据的列顺序与因果结构的对齐对生成模型的结构学习至关重要。

### 6. 开放问题与未来方向

TabStruct 开辟了若干值得深入探索的方向：

1. **可证实的结构保真度指标**：在真实世界场景下，如何开发具有理论保证的结构保真度指标，而非仅依赖经验相关性？

2. **面向评估的轻量级因果结构近似**：当前因果发现算法在真实数据上恢复完美 DAG 仍不可行，能否设计专门服务于评估的、计算高效的因果结构近似方法？

3. **因果结构指导的生成模型设计**：全局效用揭示的列顺序效应暗示，表格数据中固有的因果结构信息可以被更有效地利用来指导生成模型的设计和训练。

4. **向动态与多模态数据的扩展**：全局效用的核心思想——以每个变量为预测目标评估整体依赖结构的保留——是否可以推广至动态表格数据、多模态表格数据或多表关联场景？

## 原文 PDF

![[paperPDFs/ICLR_2026/TabStruct_Measuring_Structural_Fidelity_of_Tabular_Data.pdf]]
