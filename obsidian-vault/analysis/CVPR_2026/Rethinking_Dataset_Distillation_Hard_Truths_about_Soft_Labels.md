---
title: "Rethinking Dataset Distillation: Hard Truths about Soft Labels"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Rethinking_Dataset_Distillation_Hard_Truths_about_Soft_Labels.pdf
project_link: null
code_link: "https://github.com/Guang000/Awesome-Dataset-Distillation"
aliases:
- CCADDCPCADP
- RDDHTASL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 标签设置（从硬标签HL到固定软标签SL再到强软标签SL+KD）通过引入不同程度的教师监督，直接改变了数据质量与计算量对最终性能的相对贡献。在HL设置下，数据质量恢复了决定性作用，并且需要根据给定的计算预算选择合适难度的样本才能达到最优性能。
primary_logic: 数据高效学习中，数据质量的重要性高度依赖标签监督方式；在常用软标签设置下质量的影响被显著削弱，导致方法无法有效区分。因此，有意义的评估与设计应当转向硬标签场景，并将样本难度与计算预算对齐，才能真正推动数据集蒸馏领域的实质性进步。
claims:
- 在SL+KD设置下，性能与子集大小和质量几乎无关，仅由计算量决定，所有子集（包括随机选择）在给定计算预算下都能接近全数据集性能（Figure 1 SL+KD panel）
- 在固定软标签（SL）设置下，EL2N-SL分数分布高度集中，样本难度趋于同质化，解释了数据质量的作用被削弱的根本原因（Figure 2(b)）
- 轨迹匹配（TM）蒸馏目标在大模型（ResNet-18）上损失值恒定（约0.806），与下游泛化无相关性，无法扩展到更大架构（Figure 3/7及DCS分析）
- 提出的CAD-Prune和CA2D在HL设置下，在ImageNet-1K上以明显优势超越RDED和最优coreset（如EL2N-Best），证明了将样本难度与计算预算对齐的有效性（Table 3）
---

# Rethinking Dataset Distillation: Hard Truths about Soft Labels

> [!tip] 核心洞察
> 数据高效学习中，数据质量的重要性高度依赖标签监督方式；在常用软标签设置下质量的影响被显著削弱，导致方法无法有效区分。因此，有意义的评估与设计应当转向硬标签场景，并将样本难度与计算预算对齐，才能真正推动数据集蒸馏领域的实质性进步。

| 字段 | 内容 |
|------|------|
| 中文题名 | 重新思考数据集蒸馏：关于软标签的残酷真相 |
| 英文题名 | Rethinking Dataset Distillation: Hard Truths about Soft Labels |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.18811) · [Code](https://github.com/Guang000/Awesome-Dataset-Distillation) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CA2D (Compute-Aware Dataset Distillation) / CAD-Prune (Compute-Aware Difficulty Pruning) |
| Dataset | ImageNet-1K |

> [!tip] 效果简介
> - ImageNet-1K (ResNet-18, HL) 上，Top-1 Accuracy (%) CA2D: 15.25 / 41.72 / 46.32 vs RDED: 14.34 / 38.49 / 44.36 (+0.91 / +3.23 / +1.96)；Top-1 Accuracy (%) CAD-Prune: 12.57 / 40.21 vs EL2N-Best: 10.53 / 38.44 (+2.04 / +1.77)。
> - ImageNet-1K (ResNet-18, SL+KD) 上，Top-1 Accuracy (%) 最佳coreset (e.g., Forgetting-Easy) ≈ 34.26 / 59.06 / 63.23 vs 随机子集 ≈ 28.82 / 58.10 / 62.87 (微小且接近全数据集性能（~63），性能差距消失)。

## 概要

**核心问题**：数据集蒸馏（Dataset Distillation, DD）旨在将大规模数据集压缩为极小的合成集，使下游模型在其上训练后能逼近在全数据集上的性能。然而，该领域长期依赖**软标签（soft labels）**与**知识蒸馏增强的软标签（SL+KD）**进行评估，这一主流设置掩盖了一个关键事实：**性能几乎完全由计算预算决定，数据子集的大小与质量几乎不带来额外提升**。不同蒸馏方法之间的性能差异在此设置下消失，进步空间接近饱和。与此同时，以轨迹匹配（Trajectory Matching, TM）为代表的小规模蒸馏目标在大模型上失效，损失值恒定且与下游泛化无相关性，暴露出方法可扩展性的严重不足。

**核心洞察**：标签设置是调节数据质量与计算量相对贡献的“因果旋钮”。从硬标签（HL）到固定软标签（SL）再到强软标签（SL+KD），教师监督的介入程度逐步加深，数据质量的决定性作用被逐步削弱。在SL+KD设置下，EL2N分数分布高度集中，样本难度趋于同质化，导致所有子集（包括随机选择）在给定计算预算下均能逼近全数据集性能。唯有回归**硬标签（HL）设置**，数据质量才恢复其决定性作用，且需要根据给定的计算预算选择合适难度的样本才能达到最优性能。

**方法定位**：基于上述洞察，本文提出两项核心方法：
- **CAD-Prune（Compute-Aware Difficulty Pruning）**：一种计算感知的样本难度剪枝指标，通过仅使用与下游计算预算对齐的单个训练检查点及短窗口内的epoch间不确定性均值，高效识别并选取难度适当的样本子集，避免了现有方法（如EL2N-Best）在多epoch滑动窗口穷举搜索的高昂开销。
- **CA2D（Compute-Aware Dataset Distillation）**：以CAD-Prune筛选出的coreset为基础，结合RDED风格的补丁提取与拼接策略构建的合成数据集蒸馏方法。

**主要结果**：在ImageNet-1K的硬标签设置下，CAD-Prune在IPC 10和IPC 50上分别以**12.57%**和**40.21%**的Top-1准确率显著超越EL2N-Best（10.53%/38.44%）；CA2D在IPC 10/50/100上以**15.25%/41.72%/46.32%**的准确率全面超越RDED（14.34%/38.49%/44.36%），验证了将样本难度与计算预算对齐策略的有效性。

**方法谱系与知识库定位**：CA2D继承并改进了RDED的补丁提取框架，其核心创新在于将**计算感知的coreset选择（CAD-Prune）**前置到合成流程中，替代RDED的无差别补丁选取。在coreset方法谱系中，CAD-Prune与EL2N-Best（Lee & Chung, 2024）形成直接对比——前者以计算对齐的单检查点策略替代后者的滑窗穷举，在保持或超越性能的同时大幅降低选择成本。在DD方法谱系中，CA2D与SRe2L、DWA、D4M、Minimax Diffusion等大规模DD方法的关键区分在于：**完全摒弃软标签监督，在硬标签设置下进行蒸馏与评估**，从而恢复数据质量对性能的贡献。本文提出的DCS（Distillation Correlation Score）为DD领域引入了一种零shot评估蒸馏目标质量的工具，目前可适用于DM等可计算损失目标的方法（Spearman ρ=0.41），但对不可优化目标的方法尚需扩展。



### 数据集蒸馏的核心命题与评估困境

数据集蒸馏（Dataset Distillation, DD）旨在将大规模训练集压缩为极小的合成数据集，使下游模型在该合成集上训练后能逼近在全量数据上的泛化性能。这一领域的核心评估范式长期依赖软标签（soft labels）与知识蒸馏（knowledge distillation）的组合设置（SL+KD）：学生模型在合成数据上训练时，不仅使用合成标签，还通过CutMix等增强策略引入教师模型的软标签监督。

然而，**这一主流评估设置正在系统性地掩盖数据蒸馏方法的真实进展**。本工作揭示了一个关键事实：在SL+KD设置下，下游模型的性能几乎完全由计算预算（训练轮次）决定，而与合成数据的质量、大小几乎无关。无论是精心蒸馏的数据集、基于EL2N分数筛选的高质量coreset，还是随机采样的子集，在相同的计算预算下都能收敛到接近全数据集训练的性能水平（Figure 1 SL+KD panel）。这一发现意味着，该领域多年来在SL+KD设置下报告的“性能提升”，很大程度上只是计算预算增加带来的假象，而非数据蒸馏方法本身的实质性进步。

### 软标签如何消解数据质量的作用

为理解上述现象的深层机理，本工作系统分析了三种标签设置下的数据效率行为：

- **硬标签（HL）**：学生模型仅使用合成数据的原始类别标签进行训练，无任何教师软标签注入。
- **固定软标签（SL）**：学生模型使用教师模型对合成数据预先计算并固定的软标签分布进行训练。
- **强软标签（SL+KD）**：在SL基础上，通过CutMix等数据增强策略动态混合教师软标签，是目前DD评估的事实标准。

分析表明，从HL到SL再到SL+KD，随着软标签监督强度的增加，数据质量对最终性能的贡献被逐步削弱。在SL设置下，通过推导EL2N分数在软标签场景的对应形式（EL2N-SL），本工作发现样本的EL2N-SL分数分布高度集中在“容易-中等”难度区间（Figure 2(b)），即软标签使得原本难度各异的样本趋于同质化，从而解释了数据质量作用被削弱的根本原因。在SL+KD的极端情况下，这种同质化效应被进一步放大，导致性能完全由计算量主导，不同方法之间无法形成有效区分。

### 现有蒸馏目标的可扩展性危机

除了评估设置的问题，本工作还揭示了主流DD方法在目标函数层面的根本性缺陷。通过提出**蒸馏相关分数（Distillation Correlation Score, DCS）**——一种零样本评估蒸馏目标与下游泛化对齐程度的指标——本工作发现：

- **轨迹匹配（Trajectory Matching, TM）** 类目标在大模型（如ResNet-18）上损失值恒定（约0.806），与下游泛化性能完全无相关性（Figure 3左），表明该方法无法扩展到实际规模的网络架构。
- **SRe2L和DWA** 所依赖的批归一化（BN）统计匹配目标，其DCS相关系数接近零甚至为负值（Figure 5），意味着这些蒸馏目标与下游泛化之间存在严重错位。
- **分布匹配（Distribution Matching, DM）** 目标仅表现出中等相关性（ρ=0.41，Figure 6a），远未达到可靠指导蒸馏的水平。

这些发现共同指向一个严峻的现实：在SL+KD设置下，数据集蒸馏领域已接近性能饱和，继续沿此路径难以产生实质性突破。有意义的评估与设计必须转向硬标签场景，并将样本难度与计算预算对齐，才能真正推动该领域的进步。



## 核心方法与创新机理

本文的核心创新并非提出一种全新的数据集蒸馏算法，而是通过系统性地揭示现有评估范式的根本缺陷，将研究重心从“在软标签下设计更复杂的蒸馏目标”转移到“在硬标签下对齐样本难度与计算预算”这一被忽视但更具实质性的方向上。具体而言，创新体现在三个层面：**诊断工具、样本筛选机制、以及蒸馏方法的计算感知重构**。

### 1. 诊断工具：蒸馏相关分数 (DCS)

在方法创新之前，论文首先解决了一个前置问题：如何零成本地判断一个蒸馏目标是否值得投入计算资源去优化？现有的蒸馏方法（如SRe2L、DWA、TM）缺乏对蒸馏目标本身质量的快速评估手段，导致大量计算被浪费在与下游泛化无关的目标上。

为此，论文提出了**蒸馏相关分数（Distillation Correlation Score, DCS）**，其核心思想是：一个好的蒸馏目标，其损失值应当与最终模型的泛化性能保持单调关系。DCS通过计算 $m$ 个不同子集（coreset或蒸馏集）的下游测试损失与蒸馏目标损失之间的Spearman秩相关系数来实现这一判断：

$$ \mathrm{DCS}(\phi) = \rho\left( \{\ell_{D_{\mathrm{test}}}(\theta_{S_j}^*)\}_{j=1}^m, \{\mathcal{L}_{\mathrm{distill}}(S_j, \mathcal{D})\}_{j=1}^m \right) $$

DCS的关键价值在于其**零shot评估能力**：无需实际训练下游模型到收敛，仅需在合成阶段记录蒸馏损失，即可快速判断该目标是否与泛化对齐。实验表明，这一工具揭示了多个流行方法的严重错位——SRe2L的BN统计匹配损失与下游性能呈零相关或负相关（$\rho \approx 0$ 或负值），DWA的方差匹配损失同样如此，而TM损失在大模型（ResNet-18）上恒定在约0.806，完全无法反映泛化差异（Figure 3左）。即便是表现相对较好的DM，其相关系数也仅为中等水平（$\rho = 0.41$，Figure 6a）。

DCS的引入改变了方法设计的评估逻辑：在投入大规模计算之前，先用DCS筛选有潜力的蒸馏目标，避免在无效目标上浪费资源。

### 2. 样本筛选机制：计算感知难度剪枝 (CAD-Prune)

现有最优的coreset选择方法（如EL2N-Best）依赖滑动窗口策略，在多个训练阶段的检查点上穷举搜索最优EL2N分数范围，计算开销巨大且缺乏对下游计算预算的显式建模。更关键的是，这些方法没有回答一个核心问题：**在给定的训练计算预算下，什么样的样本难度能带来最优性能？**

CAD-Prune（Compute-Aware Difficulty Pruning）直接针对这一缺口设计，其核心changed slot在于**将样本筛选与下游计算预算对齐**：

- **Baseline（EL2N-Best）**：通过多个epoch的滑动窗口穷举寻找最优分数范围，计算成本高且与下游训练预算脱节。
- **CAD-Prune**：仅使用与计算预算对齐的单个训练阶段（而非全训练轨迹），并通过短窗口内的epoch间不确定性均值计算最终分数。

具体而言，CAD-Prune首先定义epoch间不确定性 $U_k(x)$，衡量样本在以epoch $k$ 开始的 $J$ 个连续epoch中softmax分数的标准差：

$$ U_k(x) = \sqrt{\frac{\sum_{j=0}^{J-1} \left[ \mathbb{S}(y|x,\theta^{k+j}) - \bar{\mathbb{S}} \right]^2}{J-1}} $$

然后，取训练结束前一个小窗口 $W$ 内不确定性分数的均值作为最终得分：

$$ \mathrm{CAD}(x) = \frac{\sum_{k=K-J-W}^{K-J-1} U_k(x)}{W} $$

其中 $K$ 代表总训练epoch数，$J$ 为滑动跨度，$W$ 为窗口大小。这一设计的精巧之处在于：**窗口位置直接对应下游可用的计算预算**——如果下游只有10个epoch的训练预算，CAD-Prune就在教师模型训练的第10个epoch附近采样不确定性，确保选出的样本难度恰好匹配该预算下的学习能力。

对比EL2N-Best的滑窗穷举策略，CAD-Prune在效率上具有显著优势（仅需单个训练阶段的检查点），同时在性能上达到甚至超越前者（Table 3：CAD-Prune在IPC 10/50上分别以+2.04/+1.77个百分点超越EL2N-Best）。消融实验进一步证实，compute-aware的检查点选择远优于使用长时间训练的早期checkpoint，性能提升约7-9个百分点（Table 14）。

### 3. 蒸馏方法重构：计算对齐数据集蒸馏 (CA2D)

CA2D（Compute-Aware Dataset Distillation）将CAD-Prune的样本筛选逻辑嵌入到大规模数据集蒸馏流程中，形成端到端的计算感知蒸馏方法。其相对于RDED的核心changed slot在于：

- **Baseline（RDED）**：无计算感知的样本筛选，简单选取所有图像的最置信补丁进行合成。
- **CA2D**：先用CAD-Prune根据下游计算预算选择合适难度样本组成的coreset，再从该coreset中提取最具影响力的图像补丁并拼接成合成图像。

这一流程包含三个模块：
1. **CAD-Prune coreset选择**：基于计算对齐的训练检查点和epoch间不确定性，识别并选取难度适当的样本子集。
2. **RDED-style补丁提取与拼接**：从筛选出的coreset中提取最具影响力的图像补丁并拼接成合成图像。
3. **学生模型训练（HL）**：仅使用硬标签，在生成的合成数据集上训练下游学生模型。

CA2D的关键洞察在于：**蒸馏集的信息压缩效率取决于源数据的质量与难度分布**。当源数据经过CAD-Prune筛选后，补丁提取过程能够聚焦于那些在给定计算预算下最具学习价值的样本区域，从而提升合成数据的整体效用。

在ImageNet-1K的硬标签设置下，CA2D在所有IPC配置上均显著超越RDED（Table 3）：
- IPC 10：15.25% vs. 14.34%（+0.91）
- IPC 50：41.72% vs. 38.49%（+3.23）
- IPC 100：46.32% vs. 44.36%（+1.96）

值得注意的是，CA2D相对于RDED的优势并非来自更复杂的蒸馏算法，而仅仅来自**对输入数据难度分布的重新校准**。这一结果反向印证了论文的核心主张：在硬标签设置下，数据质量（而非蒸馏技巧）是性能提升的主要驱动力。

### 创新总结

三项创新的逻辑链条清晰：**DCS提供零成本的质量诊断**，揭示现有蒸馏目标的错位问题；**CAD-Prune将样本筛选与计算预算对齐**，解决了“选什么样本”这一被软标签掩盖的核心问题；**CA2D将计算感知筛选嵌入蒸馏流程**，在不改变蒸馏算法本身的情况下实现显著提升。这一创新路径的本质是**将数据集蒸馏的进步来源从“更好的软标签蒸馏技巧”重新定位到“更好的数据质量与计算预算匹配”**，为领域提供了新的研究方向。



本文的核心主张是：**数据集蒸馏领域的评估与设计范式需要从“软标签主导”转向“硬标签+计算感知”**。为此，作者构建了一套从诊断到方法设计的完整框架，包含三条相互验证的主线：

1. **标签设置的可扩展性诊断**：通过系统性地对比 HL（硬标签）、SL（固定软标签）和 SL+KD（强软标签）三种设置下的性能缩放行为，揭示软标签对数据质量作用的系统性掩盖。
2. **蒸馏目标的零样本评估工具 DCS**：提出蒸馏相关分数（Distillation Correlation Score），用于在不训练下游模型的情况下快速判断蒸馏目标与泛化性能的对齐程度。
3. **计算感知的样本筛选与蒸馏方法 CAD-Prune / CA2D**：在硬标签设置下，根据给定的计算预算选择合适难度的样本，并以此为基础构建蒸馏数据集。

三条主线的逻辑关系是：诊断（第一部分）揭示了问题的根源——软标签设置使所有方法趋同，进步空间饱和；工具（第二部分）提供了高效评估蒸馏目标质量的手段，避免盲目设计；方法（第三部分）给出了在硬标签设置下实现实质性改进的具体方案。

---

### 整体 Pipeline

框架的核心流程可概括为三个阶段，如 Figure 1 所示（此处为文字描述，实际图片由汇编器插入）：

![[assets/figures/papers/paper_list_l2097_https_arxiv_org_abs_2604_18811/figures/001_Figure_1.jpg]]
*Figure 1: Scalability analysis of various coresets and large-scale DD sets on ImageNet-1K in SL+KD regime. (Left) Performance of coresets of varying quality (Random vs. EL2N-easy) and size (IPC 10–500+) across compute budgets equivalent to 2–50 epochs of full-dataset training. Unlike the HL setting, performance in SL+KD is dominated by compute, remains largely invariant to coreset quality and size, and quickly saturates to the near-optimal baseline of full dataset (red line of IPC=IN1K). (Middle) Pareto analysis [32] across data fractions shows no pareto-frontier in the SL+KD regime, as all subsets achieve nearly identical accuracy across the IPC values. (Right) Error trends across label settings sho...*

**阶段一：标签设置诊断与数据准备**

- 在 ImageNet-1K 上，使用 ResNet-18 作为教师模型，预计算三种标签设置下的监督信号：
  - **HL**：原始 one-hot 硬标签。
  - **SL**：教师模型对每个样本的 softmax 输出作为固定软标签。
  - **SL+KD**：在 SL 基础上叠加 CutMix 增强的软标签（即 SRe2L 等方法的标配设置）。
- 基于 EL2N 分数生成不同质量和规模的 coreset 子集（IPC 10–700+），以及收集已有的大规模 DD 方法（RDED、SRe2L、DWA、D4M、Minimax Diffusion）的合成数据集。
- 公平性控制：所有子集在相同的计算预算（epoch 数）和优化器配置下训练学生模型；小规模 DD 方法中学习到的软标签被统一替换为教师分配的软标签，消除标签学习带来的不公平优势。

**阶段二：可扩展性分析与 DCS 评估**

- 在三种标签设置下，系统性地改变数据子集的**质量**（Random vs. EL2N-easy）、**大小**（IPC 10–500+）和**计算预算**（2–50 epochs 等效），绘制性能缩放曲线。
- 提出 **EL2N-SL 分数**（Definition 1），用于量化固定软标签设置下样本的重要性分布，揭示软标签使样本难度趋于同质化的机理。
- 提出 **DCS**（Distillation Correlation Score），计算不同子集的蒸馏目标损失与下游测试损失之间的 Spearman 秩相关系数，零样本评估蒸馏目标的质量。

**阶段三：计算感知的样本筛选与蒸馏（CAD-Prune → CA2D）**

- **CAD-Prune**：在硬标签设置下，利用训练过程中的 epoch 间不确定性 $U_k(x)$ 捕捉样本难度动态，取训练结束前小窗口 $W$ 内的均值作为最终 CAD 分数：
  $$U_k(x) = \sqrt{\frac{\sum_{j=0}^{J-1} \left[ \mathbb{S}(y|x,\theta^{k+j}) - \bar{\mathbb{S}} \right]^2}{J-1}}$$
  $$\mathrm{CAD}(x) = \frac{\sum_{k=K-J-W}^{K-J-1} U_k(x)}{W}$$
  其中 $K$ 为总训练 epoch 数，$J$ 为滑动跨度，$W$ 为窗口大小。该分数确保选出的样本难度与给定的计算预算对齐——低预算选简单样本，高预算选困难样本。
- **CA2D**：以 CAD-Prune 筛选出的 coreset 为基础，采用 RDED 风格的补丁提取与拼接策略，生成合成数据集。最终学生模型仅使用硬标签在该合成集上训练。

---

### 模块关系与数据流

```
原始数据集 (ImageNet-1K)
    │
    ├──→ [教师模型 ResNet-18] ──→ 软标签 (SL/SL+KD) / EL2N分数
    │         │
    │         ├──→ Coreset 子集构造 (Random, EL2N-easy/hard, ...)
    │         │
    │         └──→ 标签设置诊断 (HL/SL/SL+KD 缩放分析) ──→ 核心发现: 软标签掩盖数据质量
    │
    ├──→ [DCS 评估框架]
    │         │
    │         ├──→ 输入: 多个子集 + 蒸馏目标损失
    │         │
    │         └──→ 输出: Spearman ρ (目标-泛化对齐程度)
    │                    │
    │                    └──→ 发现: TM loss 在大模型上 ρ≈0; SRe2L/DWA ρ≈0 或负值
    │
    └──→ [CAD-Prune] (硬标签设置)
              │
              ├──→ 训练检查点选择 (与计算预算对齐)
              ├──→ Epoch间不确定性计算 U_k(x)
              ├──→ 窗口均值聚合 → CAD(x) 分数
              │
              └──→ 筛选出的 Coreset
                        │
                        └──→ [CA2D: RDED-style 补丁提取与拼接]
                                  │
                                  └──→ 合成数据集
                                            │
                                            └──→ [学生模型训练 (HL)]
                                                      │
                                                      └──→ 最终性能评估
```

**关键设计决策**：
- CAD-Prune 仅使用**与计算预算对齐的单个训练阶段**（而非 EL2N-Best 的多 epoch 滑动窗口穷举），大幅降低了筛选成本，同时保持相当或更优的性能。
- CA2D 继承了 RDED 的补丁提取策略，但将输入从“所有图像的最自信补丁”替换为“CAD-Prune 筛选出的合适难度样本的补丁”，从而在硬标签设置下实现了对 RDED 的显著超越（Table 3）。
- 整个框架在硬标签设置下运行，避免了软标签对数据质量作用的系统性削弱，使数据选择与蒸馏方法的差异得以真实体现。

---

### 输入输出规范

| 阶段 | 输入 | 输出 | 关键约束 |
|------|------|------|----------|
| 标签设置诊断 | 原始数据集、教师模型 | 三种标签设置下的性能缩放曲线、EL2N-SL 分数分布 | 相同计算预算、统一优化器配置 |
| DCS 评估 | 多个子集（coreset/蒸馏集）、蒸馏目标损失函数 | Spearman 相关系数 ρ | 需可计算代理损失目标 |
| CAD-Prune | 原始数据集、计算预算（epoch 数） | 按难度筛选的 coreset | 仅使用硬标签、单阶段训练 |
| CA2D | CAD-Prune coreset | 合成蒸馏数据集 | 补丁提取策略适配较高分辨率 |
| 学生训练 | 合成数据集（HL） | 学生模型 Top-1 Accuracy | 与基线相同的 epoch 数 |

**局限性说明**：
- CA2D 在极低分辨率数据集（如 CIFAR-100，32×32）上性能弱于专门的小尺度 DD 方法（如 TM），因为基于补丁的合成策略天然适合较高分辨率图像（Table 11）。
- DCS 目前仅适用于可计算代理目标（如损失值）的方法，对于不可优化的 DD 目标尚无法评估。
- 蒸馏集的训练存在压缩-提取权衡：较小的 IPC 需要明显更多的训练轮次才能充分提取信息（Figure 8），增加了计算成本。



### 3.1 蒸馏相关分数（DCS）

**动机**：现有大规模数据集蒸馏（DD）方法的蒸馏目标与下游泛化性能之间缺乏可靠的关联性验证。为此，作者提出DCS作为一种零样本评估指标，快速判断蒸馏目标的质量。

**定义**：给定一个蒸馏方法 $\phi$，其对应的蒸馏目标为 $\mathcal{L}_{\mathrm{distill}}$。在训练集 $\mathcal{D}$ 上，对 $m$ 个不同的数据子集（可以是 coreset 或蒸馏集）$S_j$ 分别进行学生模型训练，得到最优参数 $\theta_{S_j}^*$。DCS 计算下游测试损失与蒸馏目标损失之间的 Spearman 秩相关系数：

$$\mathrm{DCS}(\phi) = \rho\left( \{\ell_{D_{\mathrm{test}}}(\theta_{S_j}^*)\}_{j=1}^m, \{\mathcal{L}_{\mathrm{distill}}(S_j, \mathcal{D})\}_{j=1}^m \right)$$

其中 $\rho$ 为 Spearman 秩相关系数，$\ell_{D_{\mathrm{test}}}$ 为测试集上的经验损失。

**关键发现**（详见 Section G）：
- **SRe2L 和 DWA**：其蒸馏目标（BN 统计匹配）与下游泛化的 DCS 接近零或呈负相关（$\rho \approx 0$ 或负值），表明目标与泛化严重错位（Figure 5）。
- **DM**：基于随机初始化模型输出特征匹配的目标仅具有中等相关性（$\rho = 0.41$）（Figure 6(a)）。
- **TM**：轨迹匹配损失在大模型（ResNet-18）上损失值恒定（约 0.806），与下游泛化完全无相关性（Figure 3 左）。

![[assets/figures/papers/paper_list_l2097_https_arxiv_org_abs_2604_18811/figures/005_Figure_3.jpg]]
*Figure 3: (Left) Analysis of TM Loss objective behavior for different synthesis methods on TinyImageNet. Scatter plot displaying correlation of Avg. TM Loss with In-domain generalization of all the methods. Notice the complete lack of correlation when one evaluates the TM loss for larger architectures like RN-18, even though generalization performance varies significantly for the underlying distilled sets. (Right) Training dynamics of DATM synthesis on TinyImageNet. We track DATM synthesis for ConvNet-D4 (left) and ResNet-18 (right) at IPC 10. Note that despite synthesis of 10k iterations, both TM loss (red curve) and accuracy (black curve) show minimal change*

![[assets/figures/papers/paper_list_l2097_https_arxiv_org_abs_2604_18811/figures/012_Figure_5.jpg]]
*Figure 5: Correlation analysis of distillation loss objectives on ImageNet-1K. We compute the proposed DCS score (see Sec-4 of the main paper) for SRe2L and DWA across multiple IPC settings and data subsets (each data point in the plot represents IPC-subset combination, see Sec. G.2 for details and discussion). One can observe a mis-alignment between these distillation objectives and their generalization performance, with either zero or negative Spearman correlation after adjusting for the bias of size of subsets*

![[assets/figures/papers/paper_list_l2097_https_arxiv_org_abs_2604_18811/figures/013_Figure_6.jpg]]
*Figure 6: DCS Additional results. (a) DCS on small-scale method DM. We use DCS to plot the correlation of DM [39] loss objective with ID generalization error and find better-than-TM but modest correlation of*

**局限性**：DCS 目前仅适用于可计算代理目标（如损失值）的方法，对于不可优化的 DD 目标尚无法评估。

---

### 3.2 固定软标签下的样本重要性分数（EL2N-SL）

**动机**：为解释软标签设置下数据质量作用被削弱的机理，作者将经典 EL2N 分数推广到固定软标签场景。

**定义**：令 $q = (q_1, q_2, ..., q_C)$ 为教师模型分配的固定软标签分布，$T$ 为 softmax 温度，$p(w_t, x)$ 为学生模型在参数 $w_t$ 下对样本 $x$ 的 softmax 概率输出。在 KL 散度损失下，样本 $x$ 的 EL2N-SL 重要性分数定义为：

$$\mathrm{EL2N-SL}(x) = \frac{1}{T} \mathbb{E} \| p(w_t, x) - q(w_t, x) \|_2$$

该分数量化了学生模型预测与教师软标签之间的期望 L2 距离，反映样本在固定软标签下的学习难度。

**关键发现**：在 SL 设置下，EL2N-SL 分数分布高度集中在中低难度区间，样本难度趋于同质化（Figure 2(b)），从根本上解释了数据质量作用被削弱的原因。

---

### 3.3 Epoch 间不确定性（Epoch-wise Uncertainty）

**动机**：CAD-Prune 需要捕捉样本在训练过程中的不确定性，以识别与给定计算预算对齐的合适难度样本。

**定义**：令 $\mathbb{S}(y|x, \theta^{k+j})$ 为在第 $k+j$ 个 epoch 时模型对样本 $x$ 在真实类别 $y$ 上的 softmax 分数，$\bar{\mathbb{S}}$ 为 $J$ 个连续 epoch 内该分数的均值。以 epoch $k$ 为起点的 $J$ 个连续 epoch 内的不确定性定义为：

$$U_k(x) = \sqrt{\frac{\sum_{j=0}^{J-1} \left[ \mathbb{S}(y|x,\theta^{k+j}) - \bar{\mathbb{S}} \right]^2}{J-1}}$$

该公式计算 softmax 分数的标准差，用于捕捉样本在训练过程中的预测波动。高不确定性样本通常对应模型难以稳定拟合的困难样本。

---

### 3.4 CAD-Prune 分数

**动机**：EL2N-Best 需要通过多个 epoch 的滑动窗口穷举寻找最优分数范围，计算开销大。CAD-Prune 仅使用与计算预算对齐的单个训练阶段，并通过短窗口内的不确定性均值实现高效筛选。

**定义**：令 $K$ 为总训练 epoch 数，$J$ 为滑动跨度，$W$ 为窗口大小。CAD-Prune 分数取训练结束前一个小窗口 $W$ 内不确定性分数的均值：

$$\mathrm{CAD}(x) = \frac{\sum_{k=K-J-W}^{K-J-1} U_k(x)}{W}$$

**核心设计**：
- **计算对齐**：窗口位置 $(K-J-W, K-J-1)$ 确保只使用与下游计算预算匹配的训练阶段信息，避免使用长时间训练的早期 checkpoint 导致的选择偏差。
- **高效性**：相比 EL2N-Best 的多 epoch 穷举搜索，CAD-Prune 仅需单个窗口内的统计量，计算效率显著提升（消融实验 Table 14 表明性能与滑窗方法相当，提升约 7-9 个百分点）。

---

### 3.5 轨迹匹配损失（TM Loss）

**背景**：轨迹匹配（TM）是小规模 DD 的经典目标，但在大规模设置下失效。

**定义**：令 $\theta_t$ 为在真实训练集上第 $t$ 步的参数，$\hat{\theta}_{t+N}$ 为在合成集 $\mathcal{S}$ 上训练 $N$ 步后的参数，$\theta_{t+M}$ 为在真实集上训练 $M$ 步后的参数。TM 损失定义为：

$$\mathcal{L}_{TM}(\mathcal{S}, \mathcal{D}_{\mathrm{train}}) = \frac{\| \hat{\theta}_{t+N} - \theta_{t+M} \|_2^2}{\| \theta_t - \theta_{t+M} \|_2^2}$$

其中分母为真实集参数变化范数，用于归一化。

**失效分析**：在大模型（ResNet-18）上，TM 损失值恒定（约 0.806），且与下游泛化无相关性（Figure 3 左）。在 DATM 合成动态中，即使经过 10k 次迭代，TM 损失和准确率变化极小（损失仅在小数点后三位变化，准确率仅提高 2-3%），表明该目标无法有效扩展到更大架构（Figure 3 右，Section G.1）。

### 补充图表

![[assets/figures/papers/paper_list_l2097_https_arxiv_org_abs_2604_18811/figures/003_Figure_2.jpg]]
*Figure 2: Analysis of fixed soft label (SL) setting on ImageNet-1K. (Left) Performance of coresets of varying quality and size across different compute budgets. While scaling dataset size and compute together remains essential for performance, dataset quality beyond a minimum IPC value play only a minor role as indicated by the convergence of EL2N-easy and random subsets. (Middle) Score distributions during training in SL setting cluster within the easy–mid difficulty range, showing that variations in underlying sample quality have limited effect when trained with fixed soft labels. (Right) Optimal hardness analysis also reveals that performance variations across sets in SL are far smaller compared t...*



## 实验与关键发现

### 标签设置对数据高效学习的决定性影响

本研究首先系统性地揭示了标签设置（HL → SL → SL+KD）对数据高效学习性能评估的深层影响，这是过去数据集蒸馏领域被忽视的关键变量。

**SL+KD设置下的性能饱和。** 在ImageNet-1K上，当使用CutMix增强的软标签（SL+KD）训练学生模型时，性能主要由计算预算决定，数据子集的大小和质量几乎不产生影响。如Figure 1所示，无论是随机子集还是基于EL2N分数精选的高质量子集，在相同的计算预算下（相当于全数据集2–50个epoch的训练量），性能均迅速饱和至接近全数据集的水平（约63% Top-1 Accuracy）。具体而言，IPC=10的随机子集仅需约10个epoch等效计算量即可接近饱和，而IPC=50和IPC=100的子集在更低计算量下即达到类似水平。Pareto分析进一步证实，在SL+KD设置下不存在数据效率的Pareto前沿——所有子集在不同IPC值下几乎达到相同的准确率。

**Table 1** 的大规模DD方法对比直接印证了这一发现：在SL+KD设置下，RDED、SRe2L、DWA等DD方法与随机子集、EL2N-easy等coreset方法之间的性能差距大幅缩小。例如，IPC=100时，最佳DD方法（RDED）与随机子集之间的差距从HL设置下的约6个百分点缩小至SL+KD设置下的不足1个百分点。这一现象的根本原因在于，软标签携带了教师模型的丰富知识，使得学生模型无需依赖数据本身的质量即可获得高泛化性能。

**SL设置下的质量作用削弱。** 在固定软标签（SL）设置下，数据质量的作用虽未完全消失，但被显著削弱。Figure 2(a)显示，当IPC超过10后，EL2N-easy子集与随机子集的性能曲线趋于收敛，表明数据质量仅在极低IPC下发挥有限作用。Figure 2(b)揭示了这一现象的机理：在SL设置下，我们定义的EL2N-SL分数分布高度集中在中低难度区间，样本难度趋于同质化。具体而言，EL2N-SL分数的定义如公式所示：

$$\mathrm{EL2N-SL}(x) = \frac{1}{T} \mathbb{E} \| p(w_t, x) - q(w_t, x) \|_2$$

其中 $q$ 为教师软标签分布，$p$ 为学生模型softmax概率，$T$ 为温度参数。该分数衡量样本对软标签拟合的贡献程度。在SL设置下，由于所有样本共享相同的软标签目标，其EL2N-SL分数集中在狭窄的范围内，导致原本难度各异的样本在训练中表现出相似的“影响力”，从而削弱了数据质量选择的效果。

**HL设置下数据质量恢复决定性作用。** 与SL+KD和SL形成鲜明对比，在硬标签（HL）设置下，数据质量恢复了其对性能的决定性影响。Figure 1(b)的Pareto前沿分析显示，在HL设置下存在明确的最优数据选择策略：对于较小IPC（如IPC=10），低难度样本（EL2N-easy）主导性能曲线；随着IPC增大（如IPC=50及以上），最优策略逐渐转向选择更高难度的样本。这表明在HL设置下，需要根据给定的计算预算选择合适难度的样本才能达到最优性能。

**Table 2** 在小规模数据集TinyImageNet上进一步验证了上述结论。在HL设置下，DATM等小规模DD方法相比K-centers等coreset基线有约8个百分点的显著优势；然而在SL设置下，这一优势完全消失，所有方法（包括随机子集）的性能趋于一致。CIFAR-100上的结果（Table 6）以及跨架构迁移实验（Table 7、Table 8）均一致支持这一发现。

**教师强度对SL+KD饱和现象的稳健性。** Figure 4验证了SL+KD设置下性能饱和现象对不同强度教师模型的稳健性。无论是使用较弱的MobileNet-V2教师还是弱化的ResNet-18教师，所有子集在给定计算预算下均不可避免地趋于饱和，表明这一现象并非特定教师模型的产物，而是软标签监督本身的固有特性。

### 蒸馏目标的可扩展性危机

本研究通过提出的蒸馏相关分数（DCS）框架，系统性地诊断了现有DD方法蒸馏目标的可扩展性问题。

**DCS评估框架。** DCS定义为蒸馏目标损失与下游测试损失之间的Spearman秩相关系数：

$$\mathrm{DCS}(\phi) = \rho\left( \{\ell_{D_{\mathrm{test}}}(\theta_{S_j}^*)\}_{j=1}^m, \{\mathcal{L}_{\mathrm{distill}}(S_j, \mathcal{D})\}_{j=1}^m \right)$$

其中 $m$ 个不同子集（coreset或蒸馏集）的下游测试损失与其蒸馏目标损失之间的相关性，直接衡量蒸馏目标与最终泛化性能的对齐程度。DCS接近1表示目标与泛化高度正相关，接近0表示无关，负值则表示目标与泛化背道而驰。

**大规模DD目标的错位。** Figure 5展示了SRe2L和DWA的DCS分析结果。SRe2L的BN统计匹配目标与下游泛化性能的Spearman相关系数 $\rho \approx -0.12$（在Mini-ImageNet-C的OOD任务上同样约为-0.12，见Figure 6(b)），DWA的方差匹配目标同样表现出接近零或负的相关性。这意味着这些蒸馏目标在优化过程中并未有效引导合成数据集朝着提升下游泛化的方向演进。Figure 6(a)显示，DM（分布匹配）目标的DCS为 $\rho = 0.41$，虽优于SRe2L和DWA，但仍仅为中等相关水平。

**轨迹匹配（TM）的扩展性失败。** Figure 3揭示了TM目标在大模型上的根本性失效。在ConvNet-D4上，TM损失与下游泛化之间存在一定相关性；然而当评估架构切换为ResNet-18时，TM损失值恒定在约0.806，与下游泛化性能完全无关（Figure 3左）。Figure 3右进一步展示了DATM在TinyImageNet上的合成动态：尽管经历了10k次迭代的合成优化，TM损失（红色曲线）和准确率（黑色曲线）均几乎无变化——损失值仅在小数点后三位波动，准确率仅提高2–3个百分点。这表明TM目标在大模型上无法提供有效的优化信号，从根本上限制了其可扩展性。

### CAD-Prune与CA2D的核心结果

基于上述分析，本研究提出了计算感知的难度剪枝方法CAD-Prune和计算对齐的数据集蒸馏方法CA2D，并在HL设置下验证了其有效性。

**ImageNet-1K上的核心对比。** Table 3展示了CAD-Prune和CA2D在ImageNet-1K（ResNet-18）HL设置下的核心结果。在coreset选择任务上，CAD-Prune在所有IPC设置下均显著优于EL2N-Best（基于滑动窗口穷举搜索的最优coreset方法）：

- **IPC=10**：CAD-Prune达到12.57%，EL2N-Best为10.53%，提升**+2.04个百分点**；
- **IPC=50**：CAD-Prune达到40.21%，EL2N-Best为38.44%，提升**+1.77个百分点**。

在数据集蒸馏任务上，CA2D（基于CAD-Prune筛选的coreset进行RDED式补丁提取与合成）在所有IPC设置下均以明显优势超越RDED：

- **IPC=10**：CA2D达到15.25%，RDED为14.34%，提升**+0.91个百分点**；
- **IPC=50**：CA2D达到41.72%，RDED为38.49%，提升**+3.23个百分点**；
- **IPC=100**：CA2D达到46.32%，RDED为44.36%，提升**+1.96个百分点**。

值得注意的是，CAD-Prune仅使用与计算预算对齐的单个训练阶段（而非EL2N-Best的多epoch滑动窗口穷举），在效率上具有显著优势，同时性能更优。Table 14的消融实验进一步证实，计算感知的checkpoint选择（CAD-Prune）远优于使用长时间训练的早期checkpoint，性能提升约7–9个百分点，且与滑窗方法EL2N-Best表现相当。

**跨架构迁移。** Table 12展示了CAD-Prune和CA2D在跨架构迁移（ResNet-18 → ResNet-50/ResNet-101）上的表现。CAD-Prune在效率远优于EL2N-Best的同时，性能与之匹配；CA2D在所有IPC和架构设置下均超越RDED，验证了方法的泛化性。

### 压缩-提取权衡与收敛分析

Figure 8揭示了蒸馏集与coreset在训练动态上的本质差异。蒸馏集（RDED/CA2D，实线）在更长训练下性能持续提升，而coreset（CAD-Prune，虚线）的性能较早饱和。这一现象揭示了**压缩-提取权衡**（compression-extraction trade-off）的存在：蒸馏集通过合成将信息高度压缩，需要更多的训练轮次才能充分提取其中的知识；而coreset保留原始图像，信息提取更为直接，但信息上限受限于所选子集本身。

这一权衡也解释了为何在HL设置下，CA2D在IPC=50时相比RDED的优势（+3.23个百分点）大于IPC=10时的优势（+0.91个百分点）——中等IPC下，CAD-Prune筛选的合适难度样本为蒸馏合成提供了更优的原材料，而足够的IPC又为压缩提供了充足的信息量。

### 失败模式与局限性

**低分辨率场景的性能不足。** 在CIFAR-100（32×32）等极低分辨率数据集上，CA2D的性能弱于专门的小尺度DD方法（如TM），因为基于补丁的合成策略天然适合较高分辨率图像（如ImageNet-1K的224×224），在低分辨率下补丁提取的信息增益有限（Table 11）。

**DCS的适用范围限制。** DCS目前仅适用于可用代理目标（如损失值）计算的方法。对于不可优化的DD目标（如某些基于生成模型的方法），尚无法直接应用DCS进行评估，将该框架扩展到更广泛的DD方法仍是一个开放问题。

**蒸馏集训练的额外计算成本。** 如压缩-提取权衡所揭示的，较小IPC的蒸馏集需要明显更多的训练轮次才能充分提取信息，增加了下游训练的计算成本。这一成本需要在数据存储效率与训练计算量之间进行权衡。

### 补充图表

![[assets/figures/papers/paper_list_l2097_https_arxiv_org_abs_2604_18811/figures/002_Table_1.jpg]]
*Table 1: Performance comparison of large-scale DD methods with coreset selection methods on ImageNet-1K. We compare hard label (HL), fixed soft label (SL) and cutmix-augmented soft labels (SL+KD) setting. Model architecture is ResNet-18. Best numbers are bolded within each method type (DD, coresets). Full dataset numbers are reported with the same compute used for the IPC setting. The substantial performance gap between methods (DD or coresets) closes when trained in SL+KD setting*

![[assets/figures/papers/paper_list_l2097_https_arxiv_org_abs_2604_18811/figures/006_Table_3.jpg]]
*Table 3: Performance comparison of the proposed method on ImageNet-1K in HL setting. We compare the proposed computeoptimal coreset CAD-Prune against EL2N-Best obtained using the sliding-window approach of Lee and Chung [21], and the proposed DD method CA2D against RDED. Both the methods outperform their best counterparts on ImageNet-1K in HL setting*

![[assets/figures/papers/paper_list_l2097_https_arxiv_org_abs_2604_18811/figures/019_Figure_8.jpg]]
*Figure 8: Convergence analysis of DD methods vs coresets. We plot downstream student performance (Top-1 Error) as a function of training epochs. One can observe that performance keeps improving for distilled sets (solid line) with longer training, while it saturates for coresets (dashed line), indicating the existence of compression-extraction trade-off in training on distilled set*

![[assets/figures/papers/paper_list_l2097_https_arxiv_org_abs_2604_18811/figures/004_Table_2.jpg]]
*Table 2: Performance comparison of small-scale DD methods with coresets on TinyImageNet in HL and SL setting. Model architecture is ConvNet-D4. The substantial performance gap in the HL setting closes when trained with fixed soft labels*

![[assets/figures/papers/paper_list_l2097_https_arxiv_org_abs_2604_18811/figures/010_Table_6.jpg]]
*Table 6: Performance comparison of small-scale DD methods with coresets on CIFAR-100 in HL and SL setting. Model architecture is ConvNet-D3. The substantial performance gap in the HL setting closes when trained with fixed soft labels*

![[assets/figures/papers/paper_list_l2097_https_arxiv_org_abs_2604_18811/figures/011_Table_7.jpg]]
*Table 7: CIFAR-100 Cross-Architecture Transfer performance comparison of small-scale DD methods with coresets in HL and SL setting. Model architecture is ConvNet-D3. The substantial performance gap in the HL setting closes when trained with fixed soft labels*

![[assets/figures/papers/paper_list_l2097_https_arxiv_org_abs_2604_18811/figures/015_Table_8.jpg]]
*Table 8: TinyImageNet Cross-Architecture Transfer performance comparison of small-scale DD methods with coresets in HL and SL setting. Model architecture is ConvNet-D4. The substantial performance gap in the HL setting closes when trained with fixed soft labels*



## 定位与知识库关联

### 1. 方法谱系：从软标签主导到硬标签回归

本文的核心贡献不是提出一种全新的蒸馏范式，而是对现有数据集蒸馏（DD）评估体系的系统性纠偏，并在纠偏后的框架内提出计算感知的改进方法。理解这一贡献需要先厘清当前领域内三类方法的定位与局限。

**大规模DD方法的软标签依赖。** 以 **SRe2L**（Yin et al., NeurIPS 2024）、**DWA**（Zhou et al., ECCV 2024）、**RDED**（Sun et al., NeurIPS 2024）、**D4M**（Du et al., 2024）和 **Minimax Diffusion**（Gu et al., 2024）为代表的大规模DD方法，其评估长期建立在SL+KD（CutMix增强软标签）设置之上。本文的Figure 1和Table 1（SL+KD面板）揭示了这一设置的致命缺陷：在给定计算预算下，随机子集与精心构造的蒸馏集性能趋同，所有方法均逼近全数据集性能上限，形成了“无Pareto前沿”的饱和状态。这意味着，**SL+KD设置下的性能差异主要由教师软标签提供的监督信号和计算量决定，而非数据本身的质量**——这是该领域进展被高估的根本原因。

**小规模DD方法的可扩展性断裂。** **TM**（Cazenavette et al., CVPR 2022）和 **DATM**（Guo et al., NeurIPS 2024）等基于轨迹匹配的方法在小规模设置（TinyImageNet + ConvNet-D4）上表现强劲，但其蒸馏目标在大模型上完全失效。本文的DCS分析（Figure 3）给出了定量证据：在ResNet-18上，TM损失值恒定于约0.806，与下游泛化性能的Spearman相关系数为零；DATM合成过程中损失仅在小数点后三位变化，准确率仅提升2–3%。这表明**轨迹匹配目标缺乏跨架构的可扩展性**，是其从CIFAR级走向ImageNet级应用的根本障碍。

**Coreset方法的计算无感知。** **EL2N-Best**（Lee & Chung, ICLR 2024）通过多epoch滑动窗口穷举搜索最优EL2N分数范围，虽然有效但计算代价高昂，且未将样本难度选择与下游计算预算对齐。**Random Real**作为简单基线，在SL+KD设置下意外地接近最优方法，进一步印证了软标签对数据质量差异的掩盖效应。

### 2. 知识库定位：三个核心洞察的重构

本文在知识库中的定位可概括为三个层层递进的洞察，每一层都直接挑战了领域的既有假设。

**洞察一：标签设置是数据质量作用的调节变量。** 通过系统对比HL、SL、SL+KD三种标签设置（Table 1, Table 2），本文首次给出定量证据：从HL到SL再到SL+KD，数据质量对性能的贡献递减，计算量的贡献递增。在HL设置下，数据质量恢复了决定性作用，且存在清晰的Pareto前沿——低难度样本在低IPC下占优，高难度样本在高IPC下占优。这一发现将“数据质量是否重要”的问题重新表述为“在什么标签条件下数据质量重要”，为后续研究指明了正确的评估框架。

**洞察二：软标签通过同质化样本难度削弱质量信号。** 本文提出的EL2N-SL分数（Definition 1）揭示了机制层面的原因：在固定软标签设置下，样本的EL2N-SL分数分布高度集中于“易–中”难度区间（Figure 2(b)），不同样本的难度差异被软标签的强监督信号所淹没。这解释了为何在SL+KD下随机子集与精选子集性能趋同——当所有样本的“有效难度”趋于一致时，选择策略自然失效。

**洞察三：蒸馏目标与泛化性能的错位可通过DCS量化。** 提出的DCS（蒸馏相关分数）为蒸馏目标的零样本评估提供了统一框架。DCS分析表明：SRe2L的BN统计匹配目标与泛化性能呈零或负相关（ρ ≈ 0或负值，Figure 5）；DWA的方差匹配目标同样错位；DM的特征匹配目标仅有中等相关性（ρ = 0.41，Figure 6(a)）；TM目标则完全无相关性（Figure 3左）。这一工具使得研究者无需完整训练即可快速判断蒸馏目标的质量，填补了领域内缺乏有效评估指标的空白。

### 3. 方法的适用边界与局限

**分辨率依赖。** CAD-Prune和CA2D的核心设计——基于补丁提取与拼接的合成策略——天然适合较高分辨率图像（如ImageNet-1K的224×224）。在极低分辨率数据集（如CIFAR-100的32×32）上，该方法性能弱于专门的小尺度DD方法（如TM），因为补丁级操作在低分辨率下信息损失严重（Table 11）。这是方法的内在局限，而非实现缺陷。

**DCS的覆盖范围。** DCS目前仅适用于可计算代理目标（如损失值）的蒸馏方法。对于某些不可微或不可计算损失目标的DD方法，DCS尚无法直接应用。将该框架扩展到更广泛的蒸馏目标类型是一个开放问题。

**压缩-提取权衡。** 蒸馏集的训练存在固有的压缩-提取权衡：较小的IPC（如IPC 10）需要明显更多的训练轮次才能充分提取合成数据中的信息，而coreset方法在相同计算量下更早饱和（Figure 8）。这意味着在极低IPC场景下，蒸馏方法的计算优势可能被更长的训练需求所抵消。

### 4. 开放问题与未来方向

**SL+KD设置下的研究是否还有意义？** 本文的核心结论之一是在SL+KD设置下，所有子集（无论质量与大小）几乎均达到全数据集性能，进步空间接近饱和。这引出了一个尖锐的元问题：继续在该设置下进行数据集蒸馏研究，是否还能产生实质性进步？如果答案是否定的，领域需要一次集体性的评估框架迁移。

**如何构建通用的数据选择-蒸馏联合策略？** CAD-Prune证明了将样本难度与计算预算对齐的有效性，但这一策略目前仅针对硬标签设置设计。是否存在一种通用框架，能够在不同标签设置下自动调整数据质量与计算预算的平衡，是值得探索的方向。

**DCS能否成为蒸馏目标设计的指导工具？** DCS目前作为评估工具使用，但其背后的思想——蒸馏目标应与下游泛化性能相关——是否可以反过来指导新蒸馏目标的设计？例如，直接优化DCS或其可微近似，可能产生更有效的蒸馏损失函数。



## 原文 PDF

![[paperPDFs/CVPR_2026/Rethinking_Dataset_Distillation_Hard_Truths_about_Soft_Labels.pdf]]
