---
title: "SurvHTE-Bench: A Benchmark for Heterogeneous Treatment Effect Estimation in Survival Analysis"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SurvHTE_Bench_A_Benchmark_for_Heterogeneous_Treatment_Effect_Estimation_in_Survival_Analysis.pdf
aliases:
- SB
- SurvHTE-Bench
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/causality
core_operator: "模块化合成数据集的设计——在八个因果配置（操控随机化、可忽略性、阳性、信息性删失）和五个生存场景（不同事件时间分布与删失率）之间正交变化——构成可控的“因果旋钮”，允许在已知真实值的条件下探测估计器对常见假设违反的敏感程度。"
primary_logic: "没有任何一种方法在所有条件下都占优。生存元学习器（特别是基于DeepSurv的S-和匹配学习器）在严重假设违反和高删失率下表现出显著的鲁棒性；但在低删失率、随机化设置的实验中，结果插补方法（如Double-ML）更具优势。最终性能高度依赖于插补算法和基础学习器的选择，而非单一方法家族。"
claims:
- "现有生存HTE方法可系统地归为三类：结果插补方法、直接生存因果方法、生存元学习器。"
- "在40个合成数据集上，基于DeepSurv的S-Learner-Survival获得最低平均Borda排名(5.17)，Matching-Survival排名5.42，Double-ML+Margin排名6.65。"
- "随着删失率上升，生存元学习器和Causal Survival Forest逐渐超越结果插补方法，至情景D时S-Learner-Survival平均排名达到1.6。"
- "在不可忽略性假设被违反时，生存元学习器和Causal Survival Forest的ATE偏误保持相对稳定，而部分结果插补方法偏误有所增大。"
---

# SurvHTE-Bench: A Benchmark for Heterogeneous Treatment Effect Estimation in Survival Analysis

> [!tip] 核心洞察
> 没有任何一种方法在所有条件下都占优。生存元学习器（特别是基于DeepSurv的S-和匹配学习器）在严重假设违反和高删失率下表现出显著的鲁棒性；但在低删失率、随机化设置的实验中，结果插补方法（如Double-ML）更具优势。最终性能高度依赖于插补算法和基础学习器的选择，而非单一方法家族。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SurvHTE-Bench：生存分析中异质性处理效应估计的基准测试 |
| 英文题名 | SurvHTE-Bench: A Benchmark for Heterogeneous Treatment Effect Estimation in Survival Analysis |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=qG6O3jMkCj); [GitHub](https://github.com/Shahriarnz14/SurvHTE-Bench) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/causality |
| Method | SurvHTE-Bench |
| Dataset | 40 Synthetic Datasets (overall CATE RMSE ranking), 40 Synthetic Datasets (family-level CATE RMSE ranking), ACTG Semi-synthetic, MIMIC-i Semi-synthetic (88% censoring) |

> [!tip] 效果简介
> - 40 Synthetic Datasets (overall CATE RMSE ranking) 上，Average Borda rank (lower is better) 为 S-Learner-Survival (DeepSurv): 5.17，对比 Double-ML (Margin): 6.65，变化 1.48。
> - 40 Synthetic Datasets (family-level CATE RMSE ranking) 上，Average Borda rank (lower is better) 为 S-Learner-Survival family: 3.30，对比 Double-ML family: 3.98，变化 0.68。
> - ACTG Semi-synthetic 上，CATE RMSE 为 Double-ML: 10.651 ± 0.239，对比 (Next best in table, not explicitly stated)，变化 N/A。

## 概述

生存分析中异质性处理效应（HTE）的估计缺乏标准化基准，导致评估实践碎片化、方法间比较不一致，研究者难以系统了解各类方法在关键假设违反下的稳健性。本文提出 SurvHTE-Bench，一个全面、模块化的基准框架，旨在填补这一空白。该框架将现有生存 HTE 方法归为三大类——结果插补方法、直接生存因果方法和生存元学习器，并在 40 个合成数据集、两个半合成数据集（ACTG、MIMIC‑IV）和两个真实世界数据集（Twins、ACTG 175）上统一评估了 53 种方法变体。核心设计特色在于通过正交交叉 8 种因果配置（操控随机化、可忽略性、阳性、信息性删失）与 5 种生存场景（不同事件时间分布与删失率），构成可控的“因果旋钮”，使得在已知真实处理效应的条件下，能够逐因子探测估计器对常见假设违反的敏感程度。

主要结论如下：没有任何一种方法在所有条件下均占优。生存元学习器（尤其是基于 DeepSurv 的 S‑ 和匹配学习器）在严重假设违反和高删失率下表现出显著的鲁棒性，S‑Learner‑Survival 在全部 40 个合成数据集上取得最低平均 Borda 排名（5.17），Matching‑Survival 紧随其后（5.42）；但在低删失率的随机化实验中，结果插补方法（如 Double‑ML + Margin）更具精度。整体性能高度依赖于插补算法和基础学习器的选择，而非单一方法家族：Margin 插补在高删失下始终保持最低的插补误差，DeepSurv 作为基础模型普遍优于 RSF 和 DeepHit，从而解释了顶级估计器的构成规律。SurvHTE-Bench 为生存 HTE 方法的选择提供了首个标准化参照系和可复现的比较基础设施，揭示了当前方法在高度删失场景下的共同局限，并指明了未来扩展方向（如时变处理、工具变量、公平性审计等）。

## 背景与动机

生存分析中的异质性处理效应（Heterogeneous Treatment Effect, HTE）估计旨在回答“对于给定的个体，一种处理（如治疗方案）相较于另一种处理，将如何影响其生存结局（如死亡、疾病复发）”。具体地，对每个个体 $i$ 定义其潜在事件时间 $T_i(1)$ 和 $T_i(0)$，并以 $y(\cdot)$ 表示某种变换（例如受限平均生存时间 RMST），则个体处理效应（Conditional Average Treatment Effect, CATE）可表达为：

$$\tau(x) := \mathbb{E}\big[y(T_i(1)) - y(T_i(0)) \mid X_i = x\big].$$

准确地估计 $\tau(x)$ 是个性化决策、药物获益‑风险定量和卫生政策制定的核心基础。

为实现在右删失生存数据中估计 $\tau(x)$，近年来研究者发展出三类主流范式：

- **结果插补方法（Outcome Imputation Methods）**：首先将删失的事件时间通过伪观测（Pseudo-observation）、边际期望（Margin）或逆概率删失加权（IPCW‑T）等策略插补为连续的伪响应，随后直接调用标准的因果效应估计器（如四类元学习器、Double‑ML 或 Causal Forest）。
- **直接生存因果方法（Direct‑Survival CATE Methods）**：将因果建模直接作用于时间‑事件结果，代表性工作包括基于目标学习的生存 CATE 估计算子、树模型扩展（如 Causal Survival Forest）以及深度生存因果模型。
- **生存元学习器（Survival Meta‑Learners）**：通过训练生存模型（如随机生存森林、DeepSurv、DeepHit）替代传统回归器，将经典的 S‑、T‑ 或匹配‑学习器框架适配到生存结局中。

尽管方法谱系日益丰富，该领域却长期面临一个关键障碍：**缺乏标准化、多维度的评估基准**。绝大多数现有研究仅依赖各自设计的合成模拟，通常只关注单一或少量因果假设（如可忽略性、阳性）被违反的情形，且评估协议（样本划分方式、重复次数、性能指标）大相径庭。这一碎片化状况导致两大后果：（1）不同文献中方法的排序和结论难以直接对比，无法形成可靠的选型共识；（2）研究者和实践者无法获知，当关键的识别假设（随机化、可忽略性、阳性、删失可忽略性）被不同程度违反时，哪类方法更具鲁棒性，哪类方法会遭遇灾难性失效。

为填补此缺口，我们提出了 **SurvHTE‑Bench**——一个专为生存分析中 HTE 估计设计的综合基准测试平台。其核心思想是构建一个可控的“因果旋钮”：通过将 **8 种因果配置**（系统性地开关随机化、可忽略性、阳性以及可忽略删失假设）与 **5 种生存场景**（涵盖不同的真实事件时间分布和删失率）正交组合，生成 **40 个已知真实 CATE 的合成数据集**。该模块化设计允许在完全掌控真值的条件下，定量探测不同估计器对常见假设违反的敏感程度。SurvHTE‑Bench 还在统一代码基座上实现了 **53 种系统归类的估计器变体**，覆盖全部三类方法家族，并配套 **标准化评估流程**（10 次随机划分、Borda 排名、赢率分析、辅助消融实验），从而使得两个维度的关键问题得到系统回答：“在何种因果与生存条件下，哪一类方法更为可信？”以及“决定方法最终性能的究竟是方法家族本身，还是底层的插补算法与基学习器选择？”通过这一可复现、可扩展的框架，SurvHTE‑Bench 旨在为生存 CATE 研究提供可靠的比较基础和选型指南，推动该领域向更加鲁棒和透明的方法开发前进。

## 核心创新

生存分析中异质性处理效应（HTE）的评估长期缺少标准化基准，导致不同研究在实验设计、评估协议和方法实现上高度碎片化，难以就方法的稳健性和适用边界形成一致结论。SurvHTE‑Bench 的核心创新在于将评估从“单一场景的个别比较”转变为“可控因果旋钮下的系统性压力测试”，其关键改变体现在三个层面：数据生成、评估协议和方法覆盖。

**模块化合成数据生成：正交变化的因果旋钮。**  
以往基准的合成数据通常由各自作者按狭窄假设生成，仅涉及单一维度的违反（如仅改变删失率或仅引入未观测混杂），无法分离不同假设违反的独立与交互效应。SurvHTE‑Bench 通过将 **8 种因果配置**（操控随机化、可忽略性、阳性、信息性删失的满足/违反组合，表 1）与 **5 种生存场景**（不同事件时间分布与删失率，表 2）**正交交叉**，产生 40 个数据集。这一设计构成一组可控的“因果旋钮”：在已知真实潜在结局（双方事件时间均被生成）的前提下，可独立或联合改变四个核心假设的状态，从而系统地探测估计器在每一种假设被违反时的行为边界（证据锚点：Section 3, Table 1, Table 2）。这种模块化设计是此前生存 CATE 评估中从未实现的。

**标准化评估协议：从单次分割到统计稳健的比较框架。**  
已有研究常采用不一致的数据划分、少量重复运行和非统一的评价指标，导致方法间比较不具可比性。SurvHTE‑Bench 固定采用 **10 次随机训练/验证/测试划分**，基于 **Borda count 排名、胜率分析**等非参数对比手段，并辅以插补误差、收敛性等辅助组件评估，从而在估计精度（CATE RMSE）和平均偏误（ATE bias）上给出方法性能的稳健排序（证据锚点：Section 3, Appendix F）。这一协议直接消除了评估噪声对结论的干扰，使排名结果具有统计意义。

**系统化方法覆盖：53 种变体的统一实现与可比性。**  
以往工作往往孤立考察少数方法，实现的细节差异使得跨研究结论难以合并。SurvHTE‑Bench 将现有生存 CATE 方法归为 **三大族**：结果插补方法（基于 Pseudo‑obs、Margin、IPCW‑T 插补后再用标准 CATE 学习器）、直接生存因果方法（如 Causal Survival Forest、SurvITE）、生存元学习器（S / T / Matching‑Learner + 生存基础模型），并为其 **53 种变体提供了统一、模块化的实现枢纽**，包括统一的超参数网格和可复现配置（证据锚点：Section 3, Table 8, Appendix C/D/E）。这种规模的系统性覆盖确保了方法比较的公平性，也使得消融研究（如插补算法和基础学习器的独立影响）成为可能。

**核心实证洞察：无单一最优方法，组件选择比家族归属更重要。**  
基于上述创新平台，该工作揭示了此前未被系统量化的关键规律：
- 在低删失、随机化设置下，**结果插补方法（尤其是 Double‑ML）** 显著占优；但当删失加剧或可忽略性、阳性等假设被违反时，**生存元学习器（S‑Learner‑Survival 与 Matching‑Survival）** 和 **Causal Survival Forest** 展现出更强的鲁棒性——例如在极端删失场景 D 中，S‑Learner‑Survival 的平均排名降至 **1.6**，远超其他家族（证据锚点：Figure 1, Figure 6, Figure 7；决定性数据点：S‑Learner‑Survival 总体平均 Borda 排名 **5.17**，Matching‑Survival **5.42**，Double‑ML + Margin **6.65**，来自 Figure 1 与 Table 14）。
- 插补算法的选择对结果插补族的影响甚至超过元学习器类型：**Margin 插补**在高删失下始终保持最低的插补误差，使其变体在顶级估计器中频繁出现；而 Pseudo‑obs 在删失加重时性能急剧退化（证据锚点：Table 19, Appendix F.6.1）。
- 对于生存元学习器，以 **DeepSurv** 为基础模型相比 RSF 或 DeepHit 可一致提升一致度指数（C‑index），从根源上解释了 DeepSurv 基变体在整体排名中的统治地位（证据锚点：Appendix F.6.3, Tables 25‑27）。

综上，SurvHTE‑Bench 的创新不仅在于提供了一个基准数据集，更在于它建立了一个 **剖析生存 CATE 方法脆弱性的可控实验平台**，将研究焦点从“哪个方法更好”转向“在什么条件下、为什么某些方法失败，以及组件选择如何决定最终性能”。这一转变对推动该领域的可信评估和鲁棒方法设计具有关键意义。

## 整体框架

![[assets/figures/papers/iclr26_0014_qG6O3jMkCj_SurvHTE-Bench_A_Benchmark_for_Heterogeneous_Trea/figures/001_Table_1.jpg]]
*Table 1: Causal configurations of synthetic datasets. RCT = randomized controlled trial; OBS = observational study; 5 $\theta$ ( 5 ) = 5 0 \% ( 5 \% ) treatment rate; CPS= correctly specified propensity score (ignorability satisfied); UConf = unobserved confounding (ignorability violated); NoPos = lack of positivity; InfC = informative censoring (ignorable censoring violated). ✓= held, ✗= not held*

![[assets/figures/papers/iclr26_0014_qG6O3jMkCj_SurvHTE-Bench_A_Benchmark_for_Heterogeneous_Trea/figures/002_Table_2.jpg]]
*Table 2: Survival scenarios of synthetic datasets. “Low” \<30%, “Med” 30-70%, “High” >70% censoring. AFT = accelerated failure time*

SurvHTE-Bench 旨在为生存分析中的异质性处理效应（Heterogeneous Treatment Effect, HTE）估计建立一套标准化、模块化的评估流程，以缓解该领域因评估实践碎片化而导致的方法比较不一致问题。整个管道（pipeline）由四个核心模块构成，它们以串行方式组织，从数据生成到方法评估再至结果综合输出，形成一个闭环的基准测试系统。

**数据生成模块**负责构造已知真实 HTE 的评估数据集。其核心是合成数据生成器（Synthetic Data Generator），它通过将 8 种因果配置与 5 种生存场景正交交叉，产生 40 个完全合成数据集（Table 1, Table 2）[part_003]。因果配置在 RCT/观察性研究、可忽略性、阳性及可忽略删失等假设上进行可控的满足或违反切换；生存场景则改变事件时间分布（Cox 风险、加速失效时间等）和删失率（低、中、高）[part_008]。对每个样本，生成器同时生成处理组与对照组的潜在事件时间，从而保证 CATE 真值始终已知 [part_003]。为补充合成数据在协变量结构上的局限性，管道还包含半合成数据生成器（Semi-synthetic Data Generator），它取真实的基线协变量（如 ACTG、MIMIC‑IV 记录的临床特征），再根据指定的依赖关系模拟处理分配和潜在结局，既保留真实协变量结构又提供确切真值 [part_005, part_008]。真实世界数据预处理模块负责导入 Twins 数据集和 ACTG 175 临床试验数据，并可按需注射额外删失以考察估计器在高删失下的行为 [part_006]。

**方法实现中心**（Method Implementation Hub）统一实现了 53 个生存 CATE 估计器变体，集中管理其插补策略、基础学习器和超参数配置。根据处理删失/事件时间的策略，所有变体被归为三个家族：① 结果插补方法（Outcome Imputation Methods），先利用伪观测法、Margin 插补或 IPCW‑T 插补将删失生存时间转换为完整连续结局，再应用标准 CATE 学习器（如 S‑/T‑/X‑/DR‑Learner、Double‑ML）；② 直接生存因果方法（Direct‑Survival CATE Methods），如 Causal Survival Forest 和 SurvITE，直接对时间‑事件结果进行因果效应建模；③ 生存元学习器（Survival Meta‑Learners），将标准 S‑、T‑ 和匹配学习器适配到生存设定，以 DeepSurv、Random Survival Forest 等生存模型作为基础学习器 [part_001, part_002, part_007]。三类方法共同置于可复现的实现框架下，允许在同一基准内公平比较 [part_003]。

**评估协议执行器**（Evaluation Protocol Executor）在每个数据集上执行预定义的评价流程：执行 10 次随机训练/验证/测试划分，对每个估计器变体计算 CATE RMSE（衡量个体效应估计精度）与 ATE 偏差（衡量总体效应估计的系统偏误）[part_003]。此外，还计算 Borda 计数综合排名、胜率（Win‑rate）分析、插补准确性 MAE、基础学习器一致性指数（C‑index）以及训练样本量‑误差收敛曲线等一系列辅助指标 [part_004, part_005, part_007]。所有指标均按因果配置、生存场景和插补策略等维度进行正交分层，以刻画每个估计器的稳健性剖面。

**输出分析流**将评估结果以排名图（如 Figure 1）、配置‑误差分布图（如 Figure 2）、场景‑排名趋势（如 Figure 6、Figure 7）和一致性散点图（如 Figure 4）等形式呈现，并结合消融研究（如 Table 19 中插补方法对比，Appendix F.6）揭示性能瓶颈的来源。整个管道从`(因果配置, 生存场景) → 模拟数据集`出发，经`估计器变体池 → 评估指标计算`，最终聚合成`排名 + 稳健性洞察 + 组件影响证据`，形成可重复、可扩展的生存 HTE 方法评测体系。

## 核心模块与公式推导

SurvHTE‑Bench 作为一个标准化基准框架，其核心能力并非提出新的估计器，而是通过**可配置的数据生成管线**与**统一的评估协议**将生存HTE方法的比较从碎片化的对照升级为系统化的压力测试。以下按功能模块与关键公式两层展开。

### 关键模块

1.  **合成数据生成器**  
    正交交叉8个因果配置（见表1：随机化、可忽略性、阳性、可忽略删失的有无）与5个生存场景（见表2：不同AFT/Cox-PH分布与删失率），产生 $8\times5=40$ 个合成数据集。每个样本点同时生成 $T(0)$ 与 $T(1)$，保证真实 $\tau(x)$ 永远已知。该模块是整个基准的“因果旋钮”——通过系统性地打开/闭合核心假设，能定量探测估计器对单一或组合假设违背后的敏感度
$$
Section 3
$$
。

2.  **半合成数据生成器**  
    将真实协变量矩阵（如ACTG、MIMIC‑IV）与模拟的处理分配和潜在事件时间结合。保留真实协变量间的统计结构，同时保持真实反事实已知。此模块用于验证合成结论在高维真实噪音下的迁移性
$$
Section 4.2, Appendix G
$$
。

3.  **真实世界数据预处理**  
    负责处理Twins出生记录和ACTG 175临床试验等数据，包括注入额外删失以模拟不同观测条件（例如从真实高删失场景到更高删失场景）。这些数据提供无干扰暴露或长期随访的独特鉴证
$$
Section 4.3, Appendix H
$$
。

4.  **评估协议执行器**  
    对每份数据执行10次随机训练/验证/测试划分，计算个体处理效应均方根误差（CATE RMSE）、平均处理效应偏差（ATE bias）以及一系列辅助指标，最终输出Borda计数、胜率分析与收敛曲线。该统一协议消除了因划分不一致、指标选择随意造成的不可比性
$$
Section 3, Appendix F
$$
。

5.  **方法实现中心**  
    统合53种生存CATE变体（涵盖结果插补、直接生存因果和生存元学习器三类）的模块化实现，并提供统一的超参数网格和可复现配置。该中心本身不创造新方法，而是作为“方法仓库”保障比较的公平与可复现
$$
Appendix C, D, E
$$
。

### 关键公式与变量含义

以下公式构成基准的估计目标与评价轴心，均来自已有证据，未额外推测。

**1. 条件平均处理效应**
$$
\tau(x) := \mathbb{E}\big[\,y\big(T_i(1)\big) - y\big(T_i(0)\big) \mid X_i = x\,\big]
$$
- $T_i(1),T_i(0)$：个体$i$在两处理状态下的潜在事件时间。
- $y(\cdot)$：事件时间的变换函数（例如受限平均生存时间RMST），借此将生存估计转换为可比较的连续尺度。
- $X_i$：基线协变量。
- 此为本基准的直接估计目标
$$
Section 2
$$
。

**2. CATE均方根误差**
$$
\sqrt{\frac{1}{n}\sum_{i=1}^n\big(\hat{\tau}(X_i) - \tau(X_i)\big)^2}
$$
- $\hat{\tau}(X_i)$：个体条件处理效应的估计值。
- $\tau(X_i)$：真实值。
- 衡量估计的**个体**处理效应精度（合成/半合成数据专有）
$$
Section 3
$$
。

**3. 平均处理效应偏差**
$$
\frac{1}{n}\sum_{i=1}^n \hat{\tau}(X_i) - \Delta
$$
- $\Delta$：真实总体平均水平处理效应。
- 前项为所有个体估计的平均值。
- 反映估计在**总体**层面的系统性偏离
$$
Section 3
$$
。

**4. 边缘插补**
$$
\tilde{T}_{i}^{\text{margin}} = t_i + \frac{\int_{t_i}^{\infty} S_{\text{KM}}(t)\,dt}{S_{\text{KM}}(t_i)}
$$
- $\tilde{T}_{i}^{\text{margin}}$：插补后的伪事件时间。
- $t_i$：删失个体的最后观测时间。
- $S_{\text{KM}}(\cdot)$：总体Kaplan‑Meier生存函数。
- 本质为条件期望插补，利用边缘生存曲线给删失个体补充自$t_i$之后的预期剩余生存时间
$$
Appendix B, Eq. (3)
$$
。

**5. 逆概率删失加权插补**
$$
\tilde{T}_{i}^{\text{IPCW}} = \frac{\sum_{j: t_i < t_j,\ \delta_j=1} t_j}{\sum_{j: t_i < t_j,\ \delta_j=1} 1}
$$
- 分子为在$t_i$之后所有未删失个体的观测事件时间之和。
- 分母为该类个体的计数。
- $\delta_j$：事件指示符（1为事件，0为删失）。
- 将删失个体的事件时间插补为其后真实事件时间的简单平均
$$
Appendix B, Eq. (4)
$$
。

上述公式不仅定义了“什么是好的估计”，也揭示了插补方法（如Margin vs. IPCW‑T）在高删失下的本质差异：Margin基于条件期望保持了条件均值的一致性，而IPCW‑T仅使用实发事件时间进行平均，在严重删失时容易严重失真——这最终解释了为何基于Margin的变体在各排位中频繁跃居前列（附录F.6.1）。

## 实验与分析

### 1. 总体性能排名与合成数据集主结果

在 `8 个因果配置 × 5 个生存场景 = 40 个合成数据集`（表 1、表 2）上，采用 10 次随机训练/验证/测试划分，以 **CATE RMSE**
$$
\sqrt{\frac{1}{n} \sum_{i=1}^n (\hat{\tau}(X_i) - \tau(X_i))^2}
$$
 为基础评测指标的 Borda 计数排名对 53 个估计器变体进行横向比较（图 1，表 14）。

![[assets/figures/papers/iclr26_0014_qG6O3jMkCj_SurvHTE-Bench_A_Benchmark_for_Heterogeneous_Trea/figures/011_Figure_1.jpg]]
*Figure 1: (top) Borda count rankings of the top 10 estimator variants (out of 53 total), based on CATE RMSE across 40 datasets and averaged over 10 repeats (lower is better). (bottom) Family-level rankings, where for each dataset the best method variant within each method family is chosen using validation performance and then ranked on the heldout test set. Black bands connect methods without statistically significant differences (Wilcoxon signed-rank test, FDR-corrected at α = 0.05). Shaded regions indicate the standard error of the rank across datasets*

- **个体变体层面**：基于 DeepSurv 的 **S-Learner-Survival** 获得最低平均排名（5.17），紧随其后的是 Matching‑Survival（5.42）和 **Double‑ML+Margin**（6.65）（图 1 上）。前 10 名中 Margin 插补变体出现频次最高，暗示插补质量是性能的关键决定因素。
- **方法族层面**：S‑Learner‑Survival 族平均排名 3.30，Double‑ML 族 3.98（图 1 下）。生存元学习器在多样化假设下展现出整体更优的鲁棒性。

图 2 展示了情景 C 中各变体的 CATE RMSE 分布：在低删失、随机化设置下，结果插补族的误差方差较小，而生存元学习器在高删失场景下离群误差显著减少，这解释了其总体排名领先的原因。

### 2. 半合成与真实世界验证

在两个半合成数据集（ACTG、MIMIC‑i～v）和两个真实数据（Twins、ACTG 175）上进行补充验证（表 3，图 3、4）。

![[assets/figures/papers/iclr26_0014_qG6O3jMkCj_SurvHTE-Bench_A_Benchmark_for_Heterogeneous_Trea/figures/012_Table_3.jpg]]
*Table 3: CATE RMSE (mean ± std over 10 repeats) on ACTG and MIMIC-i-v semi-synthetic datasets. Best two methods per dataset are bolded*

- **ACTG（低删失）**：**Double‑ML 取得最低 CATE RMSE 10.651±0.239**（表 3），印证了有限删失下结果插补方法的高效性。
- **MIMIC‑i（88％ 删失）**：**Causal Survival Forest 和 S‑Learner‑Survival** 的误差在 7.895–7.921 区间，而插补类 T‑Learner 为 7.964±0.046（表 3），支持“高删失时直接建模生存过程优于事后插补”的结论。
- **Twins 真实数据（h＝30 天 RMST）**：S‑Learner‑Survival 与 DR‑Learner 的 CATE RMSE 约 7.2 天，而 **Double‑ML** 在该任务中表现最差（图 3）。当删失模式与协变量结构发生复杂交互时，生存元学习器的适应能力可能更强；但当前仅基于单次任务，该解读仍需额外验证。
- **ACTG 175 临床试验（ZDV vs ZDV＋ddI）**：引入额外删失后，**Causal Survival Forest 的 CATE 估计与基线高度一致**（散点紧贴对角线），而生存元学习器出现显著偏离（图 4）。说明在真实数据中，方法对删失水平的敏感度差异仍然存在，且最优选择可能因数据集而异。

### 3. 删失率与生存分布的调制效应

图 6 描绘了各方法族在五个生存场景中的平均排名变化趋势。

![[assets/figures/papers/iclr26_0014_qG6O3jMkCj_SurvHTE-Bench_A_Benchmark_for_Heterogeneous_Trea/figures/028_Figure_6.jpg]]
*Figure 6: Average ranking of each model for each Survival Scenario. Shaded regions indicate the standard error of the rank across datasets*

- **低删失（A、B）**：Double‑ML 族保持领先，平均排名约 1‑2。
- **中删失（C）**：各族的排名差距缩小，部分生存元学习器开始反超。
- **高删失（D、E）**：**S‑Learner‑Survival 族直接降至平均排名 1.6**，而依赖 Pseudo‑obs 或 IPCW‑T 插补的变体急剧恶化。

高删失（>70％）且事件时间服从 AFT 分布的场景 D/E 构成当前方法的**公用性能瓶颈**，几乎所有变体的 CATE RMSE 在此急剧升高。

### 4. 因果假设违反的敏感性分析

通过正交的因果配置（表 1），基准独立考察了不可忽略性（UConf）、阳性缺失（NoPos）和信息性删失（InfC）三类违规的影响。

- **不可忽略性违反**：生存元学习器和 Causal Survival Forest 的 **ATE 偏误** 相对稳定，部分结果插补方法偏误增大（附录 F.5 图 13d‑17d，图 7 趋势）。但这仅是“相对于严重恶化”的稳定，所有方法的 ATE 偏差绝对值仍可能超出实际容限。
- **阳性缺失（处理分配概率趋近 0 或 1）**：**全员受损**，没有一类方法表现出系统性免疫力。在弱重叠场景下盲目使用任何方法均不安全。
- **信息性删失**：Pseudo‑obs 和 IPCW‑T 这类依赖可忽略删失假设的插补方法受到明显惩罚，直接建模生存分布的方法受影响相对小——但如果删失依赖性未被正确建模，它们同样会失效。

### 5. 组件消融：插补算法与基础学习器的关键作用

对构成变体的核心模块进行消融分析，揭示了以下机制性规律。

- **插补算法**：**Margin 插补始终获得最低的插补 MAE**，且在高删失下退化最轻（表 19，附录 F.6.1）。Pseudo‑obs 仅在低删失下可接受，否则迅速劣化。这是 Margin‑变体在前 10 名排名中占据高频的根本原因。
- **生存基础模型**：在生存元学习器中，**DeepSurv 作为基础模型的 concordance 指数一致高于 RSF 和 DeepHit**（附录 F.6.3），因此 DeepSurv 变体主导了排行榜，这并非“方法族”优势，而是基础模型性能的传导。
- **CATE 学习器**：在结果插补族内部，**Lasso 回归在场景 C 和 E 常优于 Random Forest 和 XGBoost**，但 RF 在 A、B 场景下具有竞争力（表 20‑23）。不存在单一学习器在所有生存情景中都最优。

![[assets/figures/papers/iclr26_0014_qG6O3jMkCj_SurvHTE-Bench_A_Benchmark_for_Heterogeneous_Trea/figures/123_Table_19.jpg]]
*Table 19: Evaluation on imputation methods across different survival scenarios and causal configurations. MAE between the imputed and true event times on testing set is reported as mean ± std. over 10 experimental repeats. “Total Win” row counts the number of survival configurations × random split combinations (8 × 10 = 80) in which each method achieved the lowest MAE, and is calculated within each scenario. The same rule applies to all the tables below in Appendix F.6*

### 6. 失败模式与现有局限

一致出现的失败模式以及论文报告的局限性如下。

- **高删失 AFT 事件时间**：场景 D/E 下所有估计器的 CATE RMSE 翻倍甚至更差，排名靠前的方法也仅达到勉强可用水平。单纯替换模型不能消除这一瓶颈。
- **删失阳性违反未被覆盖**：当前合成设计未纳入 “删失阳性违反”（某些子组删失概率接近 1）；已知该设置会导致 Margin 和 IPCW 方法失效，未来需要专门设计场景以暴露此弱点。
- **违反程度未经分级调制**：基准仅考察“有/无”违反，而未对不可忽略性强度、重叠违规幅度等连续调制，限制了精细的敏感性判断。
- **评估维度单一**：评价局限于 CATE RMSE 和 ATE 偏误，缺少公平性、可解释性、临床效用等多维审计（section 5）。

### 7. 小结与实践启示

基于上述证据，可提炼出以下实践原则：

- **低删失、随机化设置**：Double‑ML+Margin 是精度与效率的优良选择。
- **删失率 >50％ 或不可忽略性可疑**：转向 **S‑Learner‑Survival（DeepSurv）或 Causal Survival Forest** 通常更可靠。
- **无论方法如何选择，必须预先评估删失依赖性、处理分配重叠和可能存在的未观测混杂**。基准中违反任一核心假设均导致急剧性能退化。

> 以上结论均基于特定估计目标（如 30 天 RMST）和模拟设定，推广至其他时域或数据分布时需审慎。部分细粒度对比值未在原实验中给出，需要进一步手工核对原始表格（见表 3、表 14、附录 F.5 的具体数值）。

## 方法谱系与知识库定位

生存分析中异质性处理效应（HTE）估计长期缺乏统一的评估框架，导致方法比较碎片化、对假设违反的稳健性认知不足。SurvHTE-Bench 的核心贡献并非提出新的估计算法，而是通过系统归类、模块化仿真和一致评价协议，填补了这一标准化基准的空白。它将现有及可自然扩展的生存 HTE 方法划分为三个家族：**结果插补方法**（将删失时间插补为连续数值后应用标准 CATE 估计器，如 Double-ML、X-Learner）、**直接生存因果方法**（直接对时间-事件结果建模，如 Causal Survival Forest、SurvITE）和**生存元学习器**（以生存模型为基学习器的 S/T/Matching-Learner 变体）。相比之下，以往研究中作者常根据自身偏好设定单一或少量违反情景，且分离地比较少数方法，无法揭示各类估计器在因果与删失假设同时变化时的相对优劣。SurvHTE-Bench 通过 **8 种因果配置（操控随机化、可忽略性、阳性、信息性删失的正交组合）× 5 种生存场景（不同事件时间分布与删失率）共 40 个合成数据集**，并配合**53 个系统化变体**、10 次重复实验、Borda 排名和组件消融，构成了可控的“因果旋钮”，使得方法选择不再依赖于孤例展示。

上述基准架构直接暴露了方法的**适用边界**。实验一致表明，没有任何一种方法在所有条件下占优。在**低删失、随机化设置中**，结果插补方法（尤其是 Double-ML）在 CATE RMSE 上领先；但**随着删失率上升**（如 Scenario D），生存元学习器中的 S-Learner-Survival（基于 DeepSurv）和 Matching-Survival 显著超越所有其他类别，S-Learner-Survival 的平均排名可至 1.6。**当不可忽略性等因果假设被违反时**，生存元学习器和 Causal Survival Forest 在 ATE 偏误和 CATE 精度上表现出更平滑的退化，而部分结果插补方法的偏误增大更为明显。进一步消融揭示了性能差异的深层原因：插补算法的选择对结果插补方法至关重要，**Margin 插补**利用 Kaplan‑Meier 条件期望在高删失下始终保持最低的插补误差，使得基于 Margin 的变体频繁出现在 top‑ranked 估计器中；而生存元学习器中，**DeepSurv 作为基模型**在一致性指数上持续优于 RSF 和 DeepHit，解释了该方法家族整体排名靠前的现象。因此，最终性能并非单纯取决于方法家族，而是**插补策略、基学习器与数据生成机制之间非线性交互的结果**。

尽管如此，当前基准存在明确的**局限与开放问题**。首先，所有实验均建立在静态二值处理、基线协变量和右删失的框架内，**尚未覆盖时变治疗、纵向协变量、工具变量或动态治疗方案**等更复杂的因果设定。其次，合成数据生成未模拟**一致性违反（干扰）** 和**删失阳性违反**，而这些在实际医疗场景中并非罕见。第三，评价维度局限于预测准确度和偏误，**缺失公平性、可解释性、临床效用等多维度审计**；作者也明确指出基准不能替代领域特异的验证或公平性评估。从开放问题看，未来扩展方向至少包括：引入分级敏感性分析以连续调节未测量混杂强度或重叠违背程度；将估计目标拓展至条件中位生存时间、时变风险比等更丰富的量纲；以及在多种方法的 CATE RMSE 差异不大时，建立稳定性、可解释性和计算成本的综合选型准则。这些方向将推动基准从单纯的性能排行榜演进为**支持负责任部署的工程知识库**。

## 原文 PDF

![[paperPDFs/ICLR_2026/SurvHTE_Bench_A_Benchmark_for_Heterogeneous_Treatment_Effect_Estimation_in_Survival_Analysis.pdf]]
