---
title: "Pre-training under infinite compute"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Pre_training_under_infinite_compute.pdf
project_link: null
code_link: null
openreview_forum_id: ck0aZTAnwK
aliases:
- PTUIC
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "正则化强度（权重衰减），集成成员数量，以及蒸馏策略。"
primary_logic: "通过大幅提高权重衰减（例如30倍于标准值）进行正则化，可以实现损失随参数数量的单调幂律缩放；进一步，对多个独立训练模型进行集成，可获得更低的损失渐近线；组合参数缩放和集成缩放，并通过蒸馏将增益压缩至小模型，能在不增加推理成本的前提下大幅提升数据效率。"
claims:
- "正则化使损失随参数数单调递减"
- "集成缩放实现比参数缩放更低的渐近线"
- "联合参数和集成缩放达到更低损失渐近线3.17"
- "数据效率提升5.17倍"
---

# Pre-training under infinite compute

> [!tip] 核心洞察
> 通过大幅提高权重衰减（例如30倍于标准值）进行正则化，可以实现损失随参数数量的单调幂律缩放；进一步，对多个独立训练模型进行集成，可获得更低的损失渐近线；组合参数缩放和集成缩放，并通过蒸馏将增益压缩至小模型，能在不增加推理成本的前提下大幅提升数据效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 无限计算下的预训练 |
| 英文题名 | Pre-training under infinite compute |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=ck0aZTAnwK) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | 正则化参数缩放、集成与蒸馏方法 |
| Dataset | DCLM 200M validation loss (asymptote), Data efficiency at 200M tokens (effective data ratio), Downstream tasks (PIQA, SciQ, ARC Easy) average error, Ensemble distillation loss retention (300M student) |

> [!tip] 效果简介
> - DCLM 200M validation loss (asymptote) 上，Loss 为 3.17 (joint scaling asymptote)，对比 3.75 (standard unregularized asymptote estimate)，变化 -0.58。
> - Data efficiency at 200M tokens (effective data ratio) 上，Data efficiency multiplier 为 5.17×，对比 1× (standard recipe)，变化 5.17×。
> - Downstream tasks (PIQA, SciQ, ARC Easy) average error 上，Average error (%) 为 best ensemble error，对比 best unregularized model error，变化 >9% relative reduction in error。

## 概要

在数据受限且无计算约束的条件下，标准预训练方法——增加训练轮数（epoch）和模型参数量——会遭遇严重的过拟合，无法通过简单地堆砌算力来持续降低损失。本文的核心洞见是：**通过大幅提高正则化强度（权重衰减可达标准实践的30倍），可以使损失随参数量呈单调幂律缩放**；进一步，**对多个独立训练模型进行集成，可获得比单纯参数缩放更低的损失渐近线**；最后，**组合参数缩放与集成缩放，并通过蒸馏将增益压缩至小模型，能在不增加推理成本的前提下大幅提升数据效率**。

核心结论包括：
- **正则化参数缩放**：联合调优学习率、epoch数和权重衰减后，损失随参数量 $N$ 单调递减，遵循幂律 $\hat{\mathcal{L}}_{200M,N} = 0.05/N^{1.02} + 3.43$，渐近线估计为 3.43。
- **集成缩放**：对 $K$ 个独立训练的 300M 模型进行 logit 平均，当 $K \to \infty$ 时渐近线降至 3.34，低于正则化单模型的渐近线。
- **联合缩放**：同时令 $N \to \infty$ 和 $K \to \infty$，最终损失渐近线估计为 3.17，较标准配方的 3.75 降低 0.58。
- **数据效率**：联合缩放配方在 200M tokens 下实现了 **5.17× 的数据效率提升**，即标准配方需要 5.17 倍数据才能达到相同损失。
- **蒸馏保真**：将 8 模型集成教师蒸馏至单个 300M 学生模型，可保留 **83% 的集成收益**；自蒸馏甚至能匹配正则化配方的渐近线。
- **下游任务验证**：最佳集成模型在 PIQA、SciQ、ARC Easy 上的平均错误率比最佳无正则化模型降低 **超过 9%**。

在方法谱系上，本文的基线是标准预训练配方（**Standard recipe**，Muennighoff et al., 2023；Kaplan et al., 2020）和 Chinchilla 计算最优缩放（Hoffmann et al., 2022）。本文提出的**正则化参数缩放、集成与蒸馏方法**改变了三个关键控制变量：权重衰减从 0.1 提升至 1.6–3.2（最高 30×），epoch 数从 8 增至 16（300M 模型），学习率从 1e-3 提升至 3e-3；并引入集成训练和序列知识蒸馏两个新模块。方法的核心流程包括：AdamW 优化的自回归语言模型预训练循环、基于坐标下降的超参数搜索、独立模型的集成训练与 logit 平均、以及混合真实数据的蒸馏。

实验证据的强度较高：正则化使损失单调递减（Figure 3，置信度 0.95），集成渐近线低于参数缩放渐近线（Figure 4，置信度 0.95），联合缩放达到 3.17（Figure 5，置信度 0.95），5.17× 数据效率提升（Figure 7，置信度 0.95），蒸馏保留 83% 收益（Figure 8，置信度 0.95），下游任务提升 >9%（Figure 9，置信度 0.95）。消融实验进一步确认了联合调优超参数的必要性、减小批量大小的收益、为集成渐近线优化的超参数选择、以及自蒸馏必须混合真实数据等关键发现。

主要局限包括：渐近线估计存在不确定性（有限参数量和实验噪声），数据缩放定律的外推依赖假设，实验主要限于 DCLM 数据集和 200M tokens 规模，下游任务评估范围有限，集成和蒸馏增加训练/推理成本，以及模型架构搜索有限。开放问题涉及自蒸馏的理论解释、最优超参数的自动化预测、更大数据规模下的泛化性、与其他架构的协同，以及能否设计更高效的无限计算利用算法。

### 数据受限下的预训练困境

大规模语言模型的预训练长期遵循“计算最优”范式：在计算预算约束下，通过同时扩展数据量和模型参数量来最小化损失。Chinchilla缩放定律（Hoffmann et al., 2022）为这一范式提供了理论指导。然而，随着高质量网络文本数据的增长趋于平缓，预训练正逐渐从“计算受限”转向“数据受限”——可用的独特token数量成为瓶颈，而计算资源相对充裕。

在数据受限条件下，标准预训练方法面临根本性困境。当数据量固定时，简单地增加训练轮数（epoch数）或扩大模型参数量，最终都会导致严重的过拟合：验证损失在经过初始下降后反而上升。如Figure 2所示，对于300M参数模型，超过8个epoch后损失开始恶化；当参数量从600M增至1.4B时，更大模型的表现反而更差。这意味着，在数据成为稀缺资源的未来，仅靠“投入更多计算”无法持续降低损失——标准配方存在一个无法突破的性能下限。

### 现有方法的缺口

已有的数据受限预训练策略（如Muennighoff et al., 2023的多epoch训练）试图通过调节epoch数来缓解过拟合，但效果有限。这些方法的核心缺陷在于：

1. **正则化不足**：标准实践中的权重衰减（weight decay）通常设为0.1（Brown et al., 2020），这一数值在数据重复使用场景下远不足以抑制过拟合。
2. **缺乏单调缩放保证**：即使针对每个参数量调优epoch数，损失仍不随参数量单调递减，无法建立可靠的缩放定律来预测更大规模下的性能。
3. **未充分利用集成潜力**：在计算不受限的前提下，独立训练多个模型并集成（ensemble）是一种天然的“以计算换性能”策略，但其在预训练数据效率方面的潜力未被系统探索。

### 本文动机与核心问题

本文试图回答一个根本性问题：**在数据固定、计算无限的前提下，预训练损失的理论下限在哪里？如何接近这一下限？**

具体而言，研究围绕三个递进目标展开：

1. **通过正则化实现单调缩放**：能否通过大幅增强正则化（特别是权重衰减），使损失随参数量呈单调幂律下降，从而建立可外推的缩放定律？
2. **通过集成突破单模型渐近线**：集成多个独立训练的小模型，能否获得比扩展单模型参数量更低的损失渐近线？
3. **通过蒸馏压缩增益**：能否将集成带来的数据效率提升，通过知识蒸馏压缩到单个小模型中，从而在不增加推理成本的前提下享受集成收益？

研究在DCLM数据集（Li et al., 2025）上构建了受控预训练环境，默认使用200M token的数据规模，系统性地探索上述问题。

## 核心方法与创新机理

本文的核心创新在于系统性地揭示了“无限计算、有限数据”这一约束条件下，标准预训练方法的根本性瓶颈，并提出了三条递进式的改进路径，从根本上改变了数据效率的缩放行为。

**瓶颈诊断：标准配方的过拟合陷阱。** 在固定数据（如200M tokens）且无计算约束时，标准预训练配方——增加epoch数或扩展参数数量——会遭遇严重的过拟合，损失无法随计算量增加而单调下降。具体表现为：重复数据超过一定epoch后损失反而上升；在固定epoch下扩展参数规模，1.4B模型的损失甚至高于600M模型（Figure 2）。这一现象表明，简单地堆砌计算资源无法解决数据稀缺问题。

**创新一：正则化驱动的单调参数缩放。** 本文发现，通过大幅提高权重衰减（weight decay）至标准实践的约30倍，并对学习率、epoch数和权重衰减进行联合调优，可以使损失随参数数量$N$呈现单调幂律下降。拟合得到的缩放律为：
$$\hat{\mathcal{L}}_{200M,N} = \frac{0.05}{N^{1.02}} + 3.43$$
该幂律的渐近线$E_D = 3.43$定义了正则化配方在无限参数下的最优可能损失，远优于未正则化配方的估计渐近线3.75。这一创新将正则化从防止过拟合的被动手段，提升为主动塑造损失缩放行为的关键控制旋钮。

**创新二：集成缩放实现更低渐近线。** 不同于扩展单一模型参数，本文提出训练$K$个独立模型（仅随机种子不同）并对logits取平均的集成配方。实验表明，集成成员数$K$的缩放同样遵循幂律，且其渐近线（$N=300M, K\to\infty$时为3.34）低于正则化参数缩放的渐近线（$N\to\infty, K=1$时为3.43）。这一发现颠覆了“更大模型必然更好”的直觉——在数据受限时，多个小模型的集成比单个大模型更有效。

**创新三：联合缩放与蒸馏压缩。** 将参数缩放与集成缩放组合，取双重极限$N\to\infty, K\to\infty$，得到联合缩放配方的渐近线估计为3.17，相比标准配方提升了0.58的绝对损失。更重要的是，通过序列知识蒸馏（sequence knowledge distillation），将8模型集成教师的知识压缩到单个300M学生模型中，可保留83%的集成收益（学生损失3.36 vs 集成损失3.32），在不增加推理成本的前提下实现了5.17倍的数据效率提升。此外，自蒸馏（teacher和student同尺寸）意外地有效，能够匹配正则化配方的渐近线性能。

**关键超参数变更（changed slots）。** 相对于标准配方，本文在300M模型上的核心超参数变更包括：权重衰减从0.1提升至1.6（最高达3.2），学习率从$1\times10^{-3}$提升至$3\times10^{-3}$，epoch数从8提升至16。这些变更在不同参数规模上需独立调优，且权重衰减随参数规模增大而进一步升高（Figure 11）。

本研究在“有限数据、无限计算”的假设下，构建了一套系统性的预训练方法框架，旨在突破标准预训练方法在数据受限条件下的过拟合瓶颈。该框架由三个核心模块级联构成：**正则化参数缩放**、**集成缩放**，以及**知识蒸馏压缩**。

### 问题形式化

给定固定的预训练数据量 $D$（默认 200M tokens，来自 DCLM 数据集），目标是在计算资源不受限的条件下最小化验证损失。标准预训练方法可形式化为一个训练例程 $A$，接受数据量 $D$ 和超参数 $H$（包括学习率、epoch 数、权重衰减等），输出模型 $M$ 及其损失 $\mathcal{L}(M)$。数据受限下的最优损失定义为：

$$\mathcal{L}_D^* = \min_H \mathcal{L}(A(D, H))$$

本框架的核心洞察是：当数据量固定时，简单地增加参数数量 $N$ 或重复训练 epoch 数会导致严重过拟合，损失不降反升（Figure 2）。因此，需要重新设计超参数策略和训练范式。

### 模块一：正则化参数缩放

该模块解决“如何在固定数据下通过增加参数数量持续降低损失”的问题。关键操作是**大幅提高权重衰减强度**——最优值可达标准实践（如 Brown et al., 2020 中的 0.1）的 30 倍以上。具体而言，通过坐标下降算法在离散网格中联合搜索每个参数规模 $N$ 下的局部最优学习率、epoch 数和权重衰减（Appendix C.1）。以 300M 模型为例，标准配方的权重衰减为 0.1、学习率 1e-3、epoch 数 8；正则化配方将权重衰减提升至 1.6、学习率提升至 3e-3、epoch 数增至 16（Figure 3 右表 vs Figure 2 表）。经过正则化调优后，损失随参数数量 $N$ 呈单调幂律下降，服从带渐近线的幂律形式：

$$\hat{\mathcal{L}}_{D,N} = \frac{A_D}{N^{\alpha_D}} + E_D$$

在 200M tokens 设定下，拟合结果为 $\hat{\mathcal{L}}_{200M,N} = 0.05/N^{1.02} + 3.43$，渐近线 $E_D = 3.43$ 代表了该配方在 $N \to \infty$ 时所能达到的最低损失。

### 模块二：集成缩放

该模块提供了一条与参数缩放正交的损失降低路径。训练 $K$ 个独立模型，仅在随机种子（控制数据顺序和模型初始化）上不同，预测时对 $K$ 个模型的 logits 取平均：

$$\mathrm{LogitAvg}(\{\mathcal{M}_i\}_{i \in [K]})(x) \propto \exp\left(\frac{1}{K}\sum_{i=1}^{K}\log(\mathcal{M}_i(x))\right)$$

集成缩放的关键优势在于：其损失渐近线低于单纯参数缩放的渐近线。在 $N=300M$ 固定参数下，$K \to \infty$ 的集成渐近线为 3.34，低于正则化配方 $N \to \infty$ 时的 3.43（Figure 4）。这意味着，在固定数据下，训练多个小模型的集成比训练单个超大模型更有效。

### 模块三：联合缩放与蒸馏压缩

将参数缩放和集成缩放组合，形成联合缩放配方：同时令 $N \to \infty$ 和 $K \to \infty$，通过双重极限过程估计最优损失：

$$\hat{\mathcal{L}}_D = \lim_{N \to \infty} \lim_{K \to \infty} \min_H \mathcal{L}(\mathcal{E}_A(D, N, K, H))$$

联合缩放的渐近线估计为 3.17，显著优于单独使用任一配方（Figure 5）。然而，集成模型在推理时需要 $K$ 倍计算成本。为解决这一问题，框架引入**序列知识蒸馏**模块：将数据高效的集成教师模型在 $D$ tokens 上预训练后，通过无条件采样生成 $D'$ 个合成 token，与真实数据 $D$ 混合，从头训练一个学生模型。实验表明，将 8-ensemble 教师蒸馏至单个 300M 学生模型，可保留 83% 的集成损失改善（Figure 8）。此外，**自蒸馏**（教师和学生同尺寸同架构）也能有效提升性能，在混合真实数据与合成数据的条件下，可匹配正则化配方的渐近线，且不增加推理成本。

### 数据效率评估

为量化各配方的数据效率增益，框架采用数据缩放定律进行插值比较。损失随种子 token 数 $D$ 的变化服从幂律：

$$\hat{\mathcal{L}}_D = \frac{A}{D^{\alpha}} + E$$

通过计算一个配方达到另一配方同等损失所需的有效数据量 $D'$，可得出数据效率倍数。结果显示：正则化配方相比标准配方的数据效率为 2.29×（Figure 6），联合缩放配方则达到 5.17×（Figure 7），即仅需标准配方约 1/5 的数据即可达到相同损失。

### 输入输出流总结

整个框架的输入为固定规模的预训练文本数据 $D$，输出为经过正则化调优、集成训练和/或蒸馏压缩后的语言模型。各模块可灵活组合：正则化参数缩放适用于单模型训练场景；集成缩放适用于可接受推理成本增加的场景；蒸馏模块则将前两者的增益压缩至小模型，实现推理高效的数据效率提升。

### 关键模块拆解

论文的方法体系围绕“无限计算下提升数据效率”这一目标，由四个核心模块串联而成：

1. **正则化参数缩放**：对固定数据量 $D$，通过联合调优权重衰减、学习率和 epoch 数，使损失随参数数量 $N$ 单调递减。该模块的核心在于打破标准预训练中“增加参数导致过拟合”的瓶颈——标准配方的权重衰减通常固定为 0.1（源自 Brown et al., 2020），而本文发现最优权重衰减可达标准值的 30 倍（例如 300M 模型需 1.6，更大模型需 3.2）。

2. **集成缩放**：训练 $K$ 个独立模型（仅随机种子不同，控制数据顺序和模型初始化），预测时对 logits 取平均。该模块利用集成多样性在固定参数规模下获得比单模型参数缩放更低的渐近损失。

3. **联合缩放**：将参数缩放和集成缩放组合为双重极限过程 $\lim_{N \to \infty} \lim_{K \to \infty}$，通过外推估计在固定数据下可达到的最低损失。内层极限（$K \to \infty$）的超参数采用启发式规则：在正则化最优超参数基础上，epoch 数翻倍、权重衰减减半（Appendix D.4）。

4. **蒸馏压缩**：将集成模型的数据效率增益压缩到小模型中。具体流程为：先用数据高效的教师模型（如 8-集成）无条件采样生成合成数据 $D'$，再将真实数据 $D$ 与合成数据 $D'$ 混合，从头训练学生模型。自蒸馏（师生同规模）同样有效，但必须混合真实数据，否则性能严重退化（Table 4）。

### 关键公式

**参数缩放幂律（带渐近线）**

$$\hat{\mathcal{L}}_{D,N} := \frac{A_D}{N^{\alpha_D}} + E_D$$

- $\hat{\mathcal{L}}_{D,N}$：在固定数据量 $D$ 下，参数数量为 $N$ 时的预测损失
- $A_D$：与数据量相关的缩放系数
- $\alpha_D$：参数缩放指数
- $E_D$：渐近损失，表示在给定数据 $D$ 下无限增大参数能达到的理论下限

在 200M tokens 下的具体拟合结果为 $\hat{\mathcal{L}}_{200M,N} = \frac{0.05}{N^{1.02}} + 3.43$，指数接近 1，渐近线为 3.43。

**数据缩放幂律**

$$\hat{\mathcal{L}}_D := \frac{A}{D^{\alpha}} + E$$

- $\hat{\mathcal{L}}_D$：在种子 token 数 $D$ 下的预测损失
- $A$：缩放系数
- $\alpha$：数据缩放指数
- $E$：无限数据下的渐近损失

该公式用于量化不同方法的数据效率：通过插值计算一种配方需要多少数据才能匹配另一种配方的损失。

**集成 Logit 平均**

$$\mathrm{LogitAvg}(\{\mathcal{M}_i\}_{i\in[K]})(x) \propto \exp\left(\frac{1}{K}\sum_{i=1}^{K}\log(\mathcal{M}_i(x))\right)$$

- $\mathcal{M}_i$：第 $i$ 个集成成员模型
- $K$：集成成员数量
- 对 $K$ 个模型的 logits 取算术平均后通过 softmax 得到最终预测分布

### 因果机制与证据强度

| 机制 | 核心证据 | 置信度 |
|------|----------|--------|
| 正则化使损失随 $N$ 单调递减 | Figure 3 展示联合调优后损失遵循幂律 $\propto N^{-1}$ | 高 |
| 集成渐近线低于参数缩放渐近线 | Figure 4：集成 $K \to \infty$ 渐近线 3.34 vs 正则化 $N \to \infty$ 渐近线 3.43 | 高 |
| 联合缩放达到更低渐近线 | Figure 5 估计联合缩放渐近线为 3.17 | 高 |
| 蒸馏保留 83% 集成收益 | Figure 8：8-集成教师 loss 3.32 → 学生 loss 3.36 | 高 |
| 自蒸馏必须混合真实数据 | Table 4：纯合成数据导致性能崩溃 | 极高 |

### 失败模式与局限

- **渐近线估计的不确定性**：受限于有限参数数量和实验噪声，渐近线估计应视为粗略参考（Appendix I.1），外推至更大规模需谨慎。
- **蒸馏的代价**：集成蒸馏虽能将增益压缩至小模型，但训练时仍需先训练集成教师，增加了总计算开销。
- **自蒸馏的通用性**：自蒸馏的有效性依赖特定的数据混合比例和生成策略，其在不同设置下的稳定性未充分验证。

## 实验与关键发现

### 核心实验设置

论文构建了一个受控的预训练环境，使用DCLM数据集（Li et al., 2025）中的有限网络数据，默认限制为200M tokens，以模拟数据受限的未来场景。基础训练框架采用标准自回归语言模型预训练流程，使用AdamW优化器和余弦学习率调度。模型架构默认使用300M参数的密集模型（Table 2），并在更大规模上验证结论的泛化性。超参数搜索通过受Wen et al. (2025)启发的坐标下降算法在离散网格中迭代寻找局部最优的学习率、epoch数和权重衰减。

### 标准配方的过拟合问题

在数据受限（200M tokens）且无计算约束的条件下，标准预训练配方面临严重的过拟合瓶颈。Figure 2（左）显示，对300M模型而言，重复数据虽然初期降低损失，但epoch数过高时损失反而上升。Figure 2（右）进一步表明，即使为每个参数规模调优epoch数，简单地增加参数数量也无法持续降低损失——1.4B模型的表现甚至不如600M模型。标准配方的超参数配置（Figure 2附表）显示：150M模型使用lr=3e-3, E=8；300M使用lr=1e-3, E=8；600M使用lr=1e-3, E=4；1.4B使用lr=3e-4, E=4。这些结果揭示了一个关键瓶颈：在有限数据下，仅靠扩展计算量（更多epoch或更大模型）会导致严重过拟合，无法实现损失的单调递减。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_ck0aZTAnwK/figures/004_Figure_2.jpg]]
*Figure 2: Evaluating standard recipe of epoching and parameter scaling for 200M tokens. Left: Though repeating the data lowers the loss, too many repetitions results in overfitting for 300M models. Right: We try increasing parameter count, tuning the epoch count at each parameter count. We similarly find that loss starts increasing. Moreover, increasing the parameter count 10× improves the loss by less than 0.1*

### 正则化参数缩放的突破

论文的核心发现是：通过大幅提高权重衰减进行正则化，可以实现损失随参数数量的单调幂律缩放。Figure 3展示了这一突破性结果。与标准配方（红色线）相比，正则化配方（紫色线）联合调优了学习率、epoch数和权重衰减，使损失随参数数量N呈单调递减，且超额损失以约$N^{-1}$的速率下降。具体的超参数变化极为显著：对于300M模型，权重衰减从标准实践的0.1提升至1.6（**30倍于标准值**），学习率从1e-3提升至3e-3，epoch数从8提升至16。对于更大模型，权重衰减进一步增加至3.2。

拟合的带渐近线的幂律公式为：
$$\hat{\mathcal{L}}_{200M,N} = \frac{0.05}{N^{1.02}} + 3.43$$

该公式预测，当参数数量$N \to \infty$时，正则化配方的最佳可能损失渐近线为**3.43**。这一渐近线估计成为评估单调缩放配方的核心指标。值得注意的是，正则化使得模型可以在超过Chinchilla最优规模140倍的参数下仍保持单调改善，彻底改变了数据受限场景下的缩放行为。

### 集成缩放的替代路径

论文探索了另一种利用无限计算的方式：不扩展单个模型的参数数量，而是训练K个独立模型（仅随机种子不同）并对logits进行平均，构成集成模型。Figure 4对比了扩展参数数量与扩展集成成员数量的效果。集成成员数量K的增加同样可以用幂律拟合，且超额损失以约$1/K$的速率下降。更重要的是，集成缩放的渐近线（N=300M, K→∞时为**3.34**）低于正则化参数缩放的渐近线（N→∞, K=1时为3.43），表明在固定数据下，集成缩放能够实现比单纯扩大模型更低的损失下限。

### 联合参数与集成缩放

论文进一步组合了参数缩放和集成缩放，通过双重极限过程（$N \to \infty, K \to \infty$）估计最佳可能损失。Figure 5展示了这一过程：左侧为每个N拟合K→∞的渐近线，右侧为这些渐近线随N变化的幂律拟合。为优化渐近线而非小K时的损失，论文采用了启发式策略：使用2倍epoch和0.5倍权重衰减的正则化超参数。联合缩放配方的最终渐近线估计为**3.17**，显著优于正则化配方的3.43和标准未正则化配方的估计值3.75，损失降低了0.58。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_ck0aZTAnwK/figures/008_Figure_5.jpg]]
*Figure 5: Composing the regularized and ensembling recipes under the double limit. Left: For each N , we fit a power law on the loss as K increases. We select hyperparameters for low asymptotes instead of loss at small K. Right: We take the asymptotes from the left plot and fit a power law to capture how the asymptote changes for bigger ensemble members. This law’s asymptote estimates the best possible loss under the joint scaling recipe*

### 数据效率的量化提升

论文通过数据缩放定律量化了各配方的数据效率。拟合的带渐近线幂律公式为：
$$\hat{\mathcal{L}}_D := \frac{A}{D^{\alpha}} + E$$

通过插值计算一种配方匹配另一种配方损失所需的有效数据量D'，论文得出以下数据效率提升（Figure 6和Figure 7）：

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_ck0aZTAnwK/figures/010_Figure_7.jpg]]
*Figure 7: Scaling the seed token count for ensembles. Left: For fixed parameter and token count, we fit a power law in K , with hyperparameters optimized for the asymptote. Middle: We take the asymptote of the left 16 laws and fit a power law to measure how the asymptote changes in N . Right: We take the asymptote of the middle 4 laws and fit a power law to measure how the asymptote of asymptotes changes in D. At all token counts, we find over 2 $\times$ and 5 $\times$ 5× data efficiency wins over the regularized and standard recipes respectively

- 正则化配方相比标准配方：**2.29倍**数据效率
- 联合缩放配方相比标准配方：**5.17倍**数据效率

这意味着，联合缩放配方仅需标准配方约1/5的数据即可达到相同的损失水平。该数据效率优势在更大token数量下仍然保持。

### 蒸馏压缩集成收益

为在不增加推理成本的前提下保留集成收益，论文探索了蒸馏策略。Figure 8展示了关键结果：
- **集成蒸馏**：将8-ensemble教师模型蒸馏到300M学生模型，学生损失为3.36，相比8-ensemble的3.32，**保留了83%的集成损失改善**，且优于正则化300M模型的损失3.57。
- **自蒸馏**：使用300M教师和300M学生的自蒸馏（绿色星号）效果惊人，匹配了正则化配方的渐近线，无需增加训练时的参数数量。

自蒸馏的成功依赖于混合真实预训练数据与合成数据的关键策略。Table 4的消融实验表明，仅使用合成数据进行自蒸馏会导致学生模型性能严重退化，必须混合真实数据才能避免崩溃。

### 下游任务验证

论文在PIQA、SciQ和ARC Easy三个下游基准上验证了损失改善的迁移效果。Figure 9显示，验证损失与下游基准平均错误率之间存在强相关性。具体结果：

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_ck0aZTAnwK/figures/012_Figure_9.jpg]]
*Figure 9: Performance of pre-trained models on downstream tasks. We have thus far been using validation loss (left) to seperate whether models are better pre-trained models or not. We evaluate the same models and ensembles on downstream benchmarks (right). Models with lower validation loss have lower average error across downstream benchmarks*

- 最佳集成模型相比最佳未正则化模型的平均错误率降低**超过9%**
- 最佳蒸馏模型相比未正则化300M模型的平均错误率降低**7%**
- 正则化使得下游准确率随参数缩放呈平滑的递减收益曲线，类似于验证损失的行为模式
- 集成错误率同样随N和K的增加而改善，与损失趋势一致

### 关键消融实验

论文通过多项消融实验验证了方法的鲁棒性和关键设计选择：

**超参数联合调优的必要性**（Figure 10; Appendix C.2）：固定权重衰减为0.1无法实现单调缩放，证明联合调优权重衰减、学习率和epoch数在每个参数规模上都是至关重要的。

**批量大小的影响**（Figure 12; Appendix C.4）：减小批量大小可提升性能，实际最小可用批量大小为64。这一发现进一步提升了数据效率。

**集成渐近线的超参数优化**（Figure 15; Appendix D.2-D.4）：为集成渐近线优化超参数（更多epoch、更少权重衰减）相比按单模型最优配置能获得更低的集成渐近线，验证了为不同目标定制超参数策略的重要性。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_ck0aZTAnwK/figures/021_Figure_15.jpg]]
*Figure 15: Tuning hyperparameters of ensemble members for lowest asymptote under K $\infty$ We construct ensembles for different K when varying epoch count and weight decay. We find that the ranking between hyperparameters changes across K (left) and that the infinite member asymptote benefiting from more epochs and less weight decay per member*

**集成多样性来源**（Figure 16; Appendix D.3）：仅改变数据顺序或模型初始化即可带来大部分集成收益，其中数据顺序的变化比初始权重的变化更重要。

**自蒸馏的数据混合**（Table 4; Appendix F.3）：仅使用合成数据进行自蒸馏会导致严重退化，必须混合真实预训练数据，这一发现对自蒸馏的实际应用具有重要指导意义。

### 失败模式与局限性

尽管方法在200M tokens设置下取得了显著成功，论文坦诚地指出了多项局限性：

1. **渐近线估计的不确定性**：由于有限参数数量和实验噪声，渐近线估计应被视为粗略估计（Appendix I.1）。对1.5B和3.2B模型的外推预测误差分别为0.005和0.008（Figure 21），表明幂律拟合在适度外推范围内可靠，但更远的外推需谨慎。

2. **数据规模的泛化性**：数据缩放定律的外推依赖于假设，在更大数据规模（如>1T tokens）下的性能表现有待验证。论文在Section 5中验证了结论在更高token数量下保持，但未穷尽所有规模。

3. **领域局限性**：实验主要限于DCLM数据集，泛化到其他领域（如代码、数学、多语言）需要进一步研究。Table 1展示了在OctoThinker推理数据上的初步验证，但范围有限。

4. **下游评估的广度**：下游任务评估仅包含PIQA、SciQ、ARC Easy等少量基准，更广泛的能力评估（如生成质量、推理深度、事实准确性）有待完成。

5. **计算成本的权衡**：集成和蒸馏增加了训练和推理的计算成本。尽管论文在"无限计算"假设下探索，实际应用需要在数据效率和计算开销之间权衡。

6. **自蒸馏的通用性**：自蒸馏的有效性可能依赖于特定的数据混合比例和生成策略，其在不同设置下的通用性未充分探索。

7. **架构搜索的有限性**：模型架构搜索仅限于密集模型和初步的MoE测试（Table 9-10），其他架构（如扩散语言模型、状态空间模型）的效果未知。

8. **持续预训练的差异**：在持续预训练（CPT）场景下，权重衰减不发挥同样的正面作用（Table 6-7），表明方法的适用边界需要进一步界定。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_ck0aZTAnwK/figures/026_Figure_19.jpg]]
*Figure 19: Effect of regularization on overfitting for downstream benchmarks. Downstream benchmarks also reflect the benefit of heavy regularization on performance. The effect of overfitting on downstream benchmarks (right) appears at twice the epoch count compared to validation loss (left)*

## 定位与知识库关联

### 方法沿革与基线关系

本工作在数据受限、计算无限的前提假设下，系统考察了预训练缩放策略的极限行为。其直接对话的基线方法包括两类：

- **标准预训练配方**：以**Muennighoff et al. (2023)** 和**Kaplan et al. (2020)** 为代表的数据重复（epoching）与参数缩放策略。该配方在固定数据量下，通过增加epoch数或参数数量来消耗更多计算，但本文证实其会导致严重过拟合——即使对每个参数规模单独调优epoch数，损失仍随参数增加而上升（Figure 2）。这一发现构成了全文的核心瓶颈诊断。
- **Chinchilla缩放定律**：**Hoffmann et al. (2022)** 提出的计算最优缩放框架，在数据与参数同步增长的条件下给出最优配比。本文将其作为“计算约束下的最优”参照点，进而探索当计算约束被解除（即计算无限但数据固定）时，缩放策略应如何转向。

本文的方法改进可概括为三个递进层次：

1. **正则化参数缩放**：在标准配方基础上，将权重衰减从常规值（如**Brown et al., 2020** 中的0.1）大幅提升至最优值的约30倍（300M模型为1.6，更大模型可达3.2），并联合调优学习率和epoch数。这一改动使损失随参数数量呈现单调幂律下降，指数约为 $-1$（Figure 3）。
2. **集成缩放**：在正则化单模型基础上，引入 $K$ 个独立训练模型（仅随机种子不同）的logit平均集成。集成缩放实现了比纯参数缩放更低的损失渐近线（3.34 vs 3.43，Figure 4），表明在数据固定时，模型多样性比单一模型容量更具渐近优势。
3. **联合缩放与蒸馏**：将参数缩放（$N \to \infty$）与集成缩放（$K \to \infty$）组合为双重极限过程，得到联合渐近线估计3.17（Figure 5）。进一步通过序列知识蒸馏将集成收益压缩至小模型，保留83%的集成改进（Figure 8），并发现自蒸馏（同尺寸师生模型）可匹配正则化配方的渐近线。

### 适用边界与关键约束

本方法体系的有效性依赖于以下边界条件：

- **数据固定假设**：所有缩放策略均以固定数据量为前提（默认200M tokens），在数据可无限增长的场景下，Chinchilla类型的计算最优缩放可能更具优势。论文在Section 5验证了数据效率增益在不同token量下的保持性，但渐近线估计的外推依赖于幂律假设。
- **计算无限假设**：集成和蒸馏带来的性能增益以大量额外训练计算为代价。$K$ 成员集成需要 $K$ 倍训练成本，蒸馏还需额外的合成数据生成与重训练。在计算预算受限的实际场景中，需权衡成本与收益。
- **数据域限制**：实验主要基于DCLM数据集（**Li et al., 2025**），模型架构限于密集Transformer。在持续预训练（CPT）场景下，权重衰减的正则化效果不显著（论文提及但未详述），暗示数据分布偏移可能改变最优正则化策略。
- **下游评估覆盖有限**：下游任务仅包含PIQA、SciQ、ARC Easy等常识推理基准，更广泛的能力维度（如长文本、数学、代码）未经验证。

### 局限性与开放问题

**已识别的局限**：

1. 渐近线估计受限于有限的参数规模（最大约1.4B）和实验噪声，论文明确建议将其视为粗略估计（Appendix I.1）。
2. 数据缩放定律的外推依赖幂律假设，在更大数据规模（如>1T tokens）下的行为未经验证。
3. 模型架构搜索有限，仅初步测试了Mixture-of-Experts，其他架构（如扩散语言模型）的效果未知。
4. 自蒸馏的有效性可能依赖特定的数据混合比例和生成策略，其通用性未充分探索。

**核心开放问题**：

- **自蒸馏为何有效？** 论文引述**Allen-Zhu and Li (2023)** 的理论，将其解释为隐式集成与蒸馏的等价性，但这一解释在预训练场景下的实验验证尚不充分。
- **集成多样性的来源机制**：消融实验表明，仅改变数据顺序或模型初始化即可获得大部分集成收益，其中数据顺序的贡献更大（Figure 16）。这一现象的理论基础——尤其是“多视角数据结构”假说——有待深入。
- **最优正则化的理论预测**：当前依赖昂贵的坐标下降搜索（Appendix C.1）来确定每个参数规模的最优权重衰减、学习率和epoch数。能否从理论上预测这些超参数的最优组合，是降低实验成本的关键。
- **跨领域泛化**：本方法在语言建模预训练中验证有效，但其在视觉、多模态等其他领域的适用性尚待检验。
- **CPT场景的失效原因**：为什么权重衰减在持续预训练中不发挥同样的正面作用？这指向了预训练与微调/持续训练之间正则化需求的根本差异。
- **更优算法的可能性**：集成和蒸馏是本文在“无限计算下更好利用固定数据”方向上的探索，但是否存在更高效的算法（如更优的数据增强、对比学习目标）能进一步降低渐近线，仍是开放问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/Pre_training_under_infinite_compute.pdf]]
