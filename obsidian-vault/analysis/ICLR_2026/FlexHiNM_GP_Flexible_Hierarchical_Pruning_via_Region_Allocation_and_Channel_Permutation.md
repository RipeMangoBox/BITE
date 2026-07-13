---
title: "FlexHiNM-GP: Flexible Hierarchical Pruning via Region Allocation and Channel Permutation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/FlexHiNM_GP_Flexible_Hierarchical_Pruning_via_Region_Allocation_and_Channel_Permutation.pdf
project_link: null
code_link: null
openreview_forum_id: YaZraqRsbB
aliases:
- FG
- FlexHiNM-GP
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_theory
core_operator: "将每层权重矩阵自适应划分为密集、2:4 稀疏和全剪枝三个区域，并通过最大化保留重要性分数联合搜索区域边界（vs, ps）。"
primary_logic: "通过为每个层分配不同稀疏级别的三个区域（密集、N:M 稀疏、全剪枝），结合 Gyro‑Permutation 迭代通道重排和基于 Hard Concrete 分布的可微掩码学习，可以在保持硬件兼容性的同时实现灵活的稀疏控制和更高的精度保留。"
claims:
- "在 Deit‑Small 和 Deit‑Base 上 95% 稀疏度时，FlexHiNM‑GP 分别比 HiNM‑GP 高出 2.19% 和 3.16%。"
- "Gyro‑Permutation 将 QQP F1 从 84.78 提升至 85.35，将 SST‑2 准确率从 90.60% 提升至 91.65%。"
- "在 LLaMA2‑7B 下游任务上，FlexHiNM‑GP 在 75% 稀疏度时平均准确率比 HiNM‑GP 高 1.39%。"
- "QQP 上 F1 = 85.35"
---

# FlexHiNM-GP: Flexible Hierarchical Pruning via Region Allocation and Channel Permutation

> [!tip] 核心洞察
> 通过为每个层分配不同稀疏级别的三个区域（密集、N:M 稀疏、全剪枝），结合 Gyro‑Permutation 迭代通道重排和基于 Hard Concrete 分布的可微掩码学习，可以在保持硬件兼容性的同时实现灵活的稀疏控制和更高的精度保留。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | FlexHiNM‑GP：通过区域分配与通道置换实现灵活分层剪枝 |
| 英文题名 | FlexHiNM-GP: Flexible Hierarchical Pruning via Region Allocation and Channel Permutation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=YaZraqRsbB) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_theory |
| Method | FlexHiNM‑GP |
| Dataset | QQP, SST‑2, SQuAD v1.1 |

> [!tip] 效果简介
> - QQP 上，F1 为 85.35，对比 84.78，变化 +0.57。
> - SST‑2 上，Accuracy 为 91.65，对比 90.60，变化 +1.05。
> - SQuAD v1.1 上，F1 为 88.55，对比 88.04，变化 +0.51。

## 概要

固定 N:M 稀疏模式（如 2:4）虽然能够利用硬件加速单元，但其“一刀切”的粒度缺乏灵活性：不同层内权重的重要性分布差异显著，向量级剪枝后保留的向量仍不均匀，导致重要权重在后续 N:M 剪枝中被强制移除。FlexHiNM‑GP 针对这一瓶颈，提出了一种灵活的分层剪枝框架。

核心思路是将每层权重矩阵自适应划分为三个区域——密集区域（4:4）、2:4 稀疏区域和全剪枝区域（0:4），并通过最大化保留的重要性分数联合搜索区域边界（vs, ps）。在此基础上，Gyro‑Permutation 迭代通道重排算法在剪枝前对输出和输入通道进行重排，使不重要元素聚集、重要元素均匀分布，从而提升剪枝效率与精度保留。可微掩码学习则基于 Hard Concrete 分布生成软掩码，在逐步剪枝过程中联合优化权重与掩码，替代静态贪婪选择的 N:M 掩码。

主要实验结果验证了该框架的有效性：在 Deit‑Small 和 Deit‑Base 上 95% 稀疏度时，FlexHiNM‑GP 分别比 HiNM‑GP 高出 2.19% 和 3.16%（Figure G.1）；在 LLaMA2‑7B 下游任务上，75% 稀疏度时平均准确率提升 1.39%（Table 1）；Gyro‑Permutation 的独立贡献使 QQP F1 从 84.78 提升至 85.35，SST‑2 准确率从 90.60% 提升至 91.65%（Table 4）。该方法在保持 NVIDIA Ampere Sparse Tensor Core 硬件兼容性的同时，实现了接近无结构剪枝的精度水平。



深度神经网络剪枝是模型压缩与加速的核心技术之一。传统无结构剪枝（Unstructured Pruning）虽能实现高压缩比且精度损失小，但其不规则稀疏模式难以在通用硬件上获得实际加速。为兼顾硬件效率与模型精度，结构化剪枝方案应运而生，其中 N:M 稀疏性（如 2:4 稀疏）因其与 NVIDIA Ampere Sparse Tensor Core 的原生兼容性而备受关注。

然而，现有 N:M 稀疏方法存在一个根本性瓶颈：**固定的 N:M 稀疏比（如 2:4）缺乏灵活性，无法根据层内权重重要性的差异进行细粒度控制**。具体而言，在典型的层次化剪枝流程（HiNM）中，首先通过向量级剪枝移除一定比例的输出通道（列向量），随后对保留的向量统一施加 2:4 结构化剪枝。这一策略隐含假设所有保留向量具有同等重要性，但实际上，经过向量剪枝后的剩余向量仍存在显著的重要性分布不均——部分向量包含大量关键权重，而另一些向量则相对冗余。强制对所有向量施加相同的 2:4 稀疏约束，会导致重要权重在后续 N:M 剪枝中被机械性地移除，造成不必要的精度损失。

图 1 展示了 HiNM 框架的四种变体，直观揭示了这一问题的演进路径：原始 HiNM（图 1a）对全部保留向量施加统一 2:4 稀疏；HiNM-P（图 1b）引入了通道置换以改善权重分布，但仍维持全局统一的稀疏模式；FlexHiNM（图 1c）开始尝试区域化稀疏分配，但缺乏对通道排列的系统优化；FlexHiNM-P（图 1d）则完整结合了区域分配与通道置换，代表了本文方法的核心设计理念。

针对上述瓶颈，FlexHiNM-GP 提出了一个核心洞察：**通过为每层权重矩阵自适应分配三个不同稀疏级别的区域——密集区域（4:4）、2:4 稀疏区域和全剪枝区域（0:4）——并结合 Gyro-Permutation 迭代通道重排与基于 Hard Concrete 分布的可微掩码学习，可以在保持硬件兼容性的同时实现灵活的稀疏控制和更高的精度保留**。

这一设计的关键因果机制在于：区域分配使得重要性最高的权重得以完全保留（密集区域），中等重要的权重承受温和的结构化稀疏（2:4 区域），而不重要的向量则被整体移除（全剪枝区域）。通过联合搜索区域边界参数（向量剪枝比例 vs 和局部稀疏边界 ps），系统能够最大化保留的总重要性分数，从而在目标稀疏度约束下实现最优的精度-效率权衡。

Gyro-Permutation 通道置换算法进一步强化了这一机制：在向量剪枝前对输出通道进行重排，使不重要元素聚集以提高全剪枝效率；在 N:M 剪枝前对每个 tile 内的输入通道进行重排，使重要权重均匀分布以避免在 2:4 剪枝中被集中移除。可微掩码学习则替代了传统的静态贪婪选择，通过 Hard Concrete 分布生成软掩码，在逐步剪枝过程中联合优化权重和掩码，确保稀疏模式能够动态适应微调过程中的重要性变化。

综上，FlexHiNM-GP 的动机源于对固定 N:M 稀疏比刚性约束的突破需求，其核心贡献在于将层次化剪枝从“一刀切”的全局稀疏分配推进到“因层制宜”的自适应区域稀疏控制，从而在结构化稀疏的硬件效率与无结构剪枝的精度上限之间架起了一座桥梁。



## 核心方法与创新机理

FlexHiNM‑GP 的核心创新在于突破固定 N:M 稀疏比（如 2:4）的刚性约束，将每一层的权重矩阵自适应地划分为三个不同稀疏级别的区域，并通过通道置换与可微掩码学习实现端到端优化。以下从三个关键 changed slot 展开分析。

### 从均匀 N:M 稀疏到三区域自适应分配

HiNM‑GP 对向量剪枝后保留的所有向量统一施加 2:4 稀疏约束，忽略了层内权重重要性的异质性——某些向量中重要权重高度集中，强制 2:4 剪枝会不可逆地移除这些关键参数，形成精度瓶颈。FlexHiNM 将这一刚性约束替换为**三区域策略**：密集区域（4:4，全保留）、2:4 稀疏区域和全剪枝区域（0:4，列向量整体移除）。每个层根据自身权重分布自适应决定三个区域的边界，使重要权重可以被完整保留在密集区域，中等重要的权重接受结构化稀疏，而不重要的列向量被整体剪除。

这一设计的因果机制在于：**通过区域划分解耦了“剪多少”与“在哪剪”**。传统 N:M 剪枝中，稀疏度是全局均匀的，而 FlexHiNM 允许层内不同区域采用不同稀疏级别，在保持全局目标稀疏度的前提下最大化保留的重要性分数。

### 自适应边界搜索：联合优化 vs 与 ps

区域划分的核心控制变量是向量剪枝边界 `vs`（完全移除的列向量比例）和局部稀疏边界 `ps`（剩余向量中分配给 2:4 稀疏的比例）。HiNM‑GP 中这两个参数为固定值，无法适应层间差异。FlexHiNM 引入**联合边界搜索**，以最大化保留的总重要性分数 $R_{\text{total}} = R_{\text{dense}} + R_{24}$ 为目标，迭代调整 `(vs, ps)` 对。

`vs` 与 `ps` 之间通过目标稀疏度 `ts` 存在硬约束关系：

$$ps = \frac{2(ts - vs)}{1 - vs}$$

这意味着 `vs` 增大时，剩余向量减少，`ps` 必须相应降低以维持全局稀疏度。搜索过程在这一可行空间内寻找使重要性保留最大的边界组合。消融实验（Table 3）证实，自适应搜索的 OptFlexHiNM 在所有稀疏度下均优于固定边界的 BalFlexHiNM 变体，在 95% 稀疏度时 Deit‑Base 上优势尤为显著。

### Gyro‑Permutation：通道置换消除结构偏差

仅靠三区域划分无法完全解决结构化 N:M 稀疏引入的通道不对齐问题。Gyro‑Permutation 通过迭代的**输出通道置换**与**逐 tile 输入通道置换**，在剪枝前重排通道顺序：输出通道置换将不重要元素聚集到将被整体剪除的列向量中，提高向量剪枝效率；输入通道置换使每个 2:4 tile 内的重要权重均匀分布，避免因集中分布导致强制移除。

Table 4 的消融直接量化了这一贡献：移除 Gyro‑Permutation 后，FlexHiNM 在 QQP 上 F1 从 85.35 降至 84.78，SST‑2 准确率从 91.65% 降至 90.60%。这表明**通道置换是三区域框架发挥潜力的必要条件**，而非可选的附加组件。

### 可微掩码学习替代静态贪婪选择

HiNM‑GP 使用静态贪婪选择的 N:M 掩码，在逐步剪枝过程中缺乏对权重更新的适应能力。FlexHiNM‑GP 引入基于 **Hard Concrete 分布**的可微掩码学习：通过温度 $\tau$ 缩放的重参数化生成软掩码基础值 $s_i = \sigma\big(\frac{1}{\tau}(\log \epsilon_i - \log(1 - \epsilon_i) + \log \alpha_i)\big)$，在复合损失 $L = L_{\text{task}} + L_{\text{sparse}} + L_{\text{hard}}$ 的驱动下联合优化权重与掩码，最终以 0.5 阈值硬化。Table 2 的消融显示，使用 Hard Concrete 掩码学习（H 组件）的变体在各稀疏度下精度均优于固定掩码方案。

### 创新协同与证据强度

上述三个 changed slot 形成协同效应：区域分配提供灵活性空间，边界搜索在该空间内寻找最优划分，Gyro‑Permutation 消除结构化稀疏的结构偏差，可微掩码学习则保证剪枝过程与权重训练的一致性。主要证据链包括：

- **Deit 家族 95% 稀疏度**：FlexHiNM‑GP 比 HiNM‑GP 高 2.19%（Deit‑Small）和 3.16%（Deit‑Base）（Figure G.1，置信度 0.95）
- **LLaMA2‑7B 75% 稀疏度**：平均准确率比 HiNM‑GP 高 1.39%（Table 1，置信度 0.9）
- **Gyro‑Permutation 独立贡献**：QQP F1 +0.57，SST‑2 Acc +1.05（Table 4，置信度 0.95）

需要注意的是，当前方法仅在 NVIDIA Ampere Sparse Tensor Core 的 2:4 模式下验证，对其他 N:M 模式（如 3:4）的泛化性尚未探索。Gyro‑Permutation 仅在边界搜索阶段执行，训练过程中通道顺序固定，无法适应微调后的重要性变化，这一点在评估其实际部署效果时需加以考虑。



![[assets/figures/papers/iclr26_0010_YaZraqRsbB_FlexHiNM-GP_Flexible_Hierarchical_Pruning_via_Re/figures/003_Figure_2.jpg]]
*Figure 2: Pruning pipeline*

FlexHiNM‑GP 的核心流水线由三个逻辑阶段构成：**通道置换 → 分层剪枝 → 掩码学习**。每个阶段作用于权重矩阵的不同维度，协同实现灵活且硬件兼容的稀疏化。

### 流水线总览

给定一个线性层的权重矩阵，流水线按以下顺序执行（对应 Algorithm 1 及 Figure 2）：

1. **Gyro‑Permutation（输出通道置换）**：在向量剪枝之前，对权重矩阵的输出通道进行重排，目的是将不重要的元素聚集到特定列向量中，从而提高后续向量剪枝的效率。此置换跨 tile 统一执行。
2. **向量剪枝（Vector Pruning）**：根据全局重要性分数，完全移除一定比例（由边界 $vs$ 控制）的列向量。被移除的向量对应“全剪枝区域”（0:4 稀疏）。
3. **Gyro‑Permutation（输入通道置换）**：在 N:M 剪枝之前，对每个 tile 内的输入通道独立重排，使重要权重在 4 元素组内均匀分布，避免重要权重被 2:4 剪枝强制移除。
4. **N:M 剪枝（2:4 Prune）**：对“2:4 稀疏区域”按行执行 2:4 结构化剪枝，生成符合 Ampere Sparse Tensor Core 要求的 NM 索引。剩余未被向量剪枝移除且未纳入 2:4 剪枝的权重构成“密集区域”（4:4 稀疏）。
5. **边界搜索（Boundary Search）**：通过迭代调整向量剪枝边界 $vs$ 和 N:M 稀疏边界 $ps$，最大化保留的总重要性分数 $R_{\text{total}} = R_{\text{dense}} + R_{2:4}$，从而为每层自适应分配三个区域的稀疏比例。
6. **可微掩码学习**：在逐步剪枝过程中，使用 Hard Concrete 分布参数化的软掩码替代静态 2:4 掩码，联合优化权重与掩码，保证稀疏性约束（$L_{\text{sparse}}$）和 2:4 硬约束（$L_{\text{hard}}$）的满足。

### 模块关系与数据流

三个核心模块之间的依赖关系如下：

- **Gyro‑Permutation** 为剪枝提供优化的通道排列，但它仅在边界搜索阶段执行，训练过程中通道顺序保持固定。这意味着置换的收益依赖于剪枝前的静态分析，无法适应微调后的重要性漂移（这是方法的一个已知局限）。
- **区域分配与边界搜索** 决定了每层权重矩阵中密集、2:4 稀疏、全剪枝三个区域的比例。$vs$ 控制全剪枝向量的比例，$ps$ 控制在剩余向量中分配给 2:4 稀疏的比例，两者通过约束关系 $ps = \frac{2(ts - vs)}{1 - vs}$ 耦合（其中 $ts$ 为目标稀疏度）。
- **可微掩码学习** 作用于 2:4 稀疏区域，通过复合损失 $L = L_{\text{task}} + L_{\text{sparse}} + L_{\text{hard}}$ 驱动掩码收敛到满足 2:4 约束的二值形式。软掩码的中间变量 $s_i = \sigma\left(\frac{1}{\tau}(\log \epsilon_i - \log(1 - \epsilon_i) + \log \alpha_i)\right)$ 通过温度 $\tau$ 控制离散化程度，最终经 0.5 阈值硬化。

### 硬件执行设计

为保持推理加速，FlexHiNM‑GP 设计了自定义 GPU 内核（Figure C.1），采用双流执行：

- **Stream0** 处理稀疏 tile（2:4 区域），利用 activation‑aware loading 减少不必要的内存访问；
- **Stream1** 并行处理密集 tile（4:4 区域），使用标准 Tensor Core。

通道置换信息在线编码在索引中，无需额外的运行时重排开销。

### 关键设计取舍

| 设计选择 | 优势 | 代价/局限 |
|---------|------|----------|
| 三区域分层（密集/2:4/全剪枝） | 灵活匹配层内重要性差异，保留关键权重 | 引入 $vs$、$ps$ 两个搜索维度，增加调优复杂度 |
| Gyro‑Permutation 仅在边界搜索时执行 | 避免训练中重排开销 | 无法适应微调后的重要性变化 |
| Hard Concrete 可微掩码 | 联合优化权重与掩码，精度优于静态贪婪选择 | 需要额外的稀疏性和硬约束正则项调参 |
| 双流内核执行 | 同时利用稀疏和密集 Tensor Core | 仅验证 2:4 模式，对其他 N:M 模式的泛化性未探索 |

> **证据强度说明**：流水线的整体结构在 Section 3.1 和 Algorithm 1 中有明确定义；各模块的消融证据（Table 4 验证 Gyro‑Permutation 贡献，Table 2 验证可微掩码收益，Table 3 验证自适应边界搜索优势）均来自论文实验，置信度≥0.9。关于 Gyro‑Permutation 仅在边界搜索阶段执行这一细节，需注意原文 Section 4.1 明确声明“Channel permutation is performed only during the boundary search stage and is kept fixed throughout training”，这构成方法的一个已知局限。



### 三区域分层剪枝框架

FlexHiNM 的核心创新在于将每层权重矩阵自适应划分为三个稀疏级别不同的区域，而非对所有层统一施加固定的 N:M 稀疏模式。具体而言，权重张量被划分为 **密集区域（4:4，即无剪枝）**、**2:4 稀疏区域** 和 **全剪枝区域（0:4）**。这一设计的因果机制在于：不同层乃至同一层内不同通道的重要性分布存在显著差异，固定稀疏比（如 2:4）会强制移除部分重要权重，而三区域划分允许模型在关键通道保留密集连接，在次要通道施加结构化稀疏，在冗余通道完全剪枝，从而在硬件兼容的前提下实现细粒度的稀疏控制。

该框架的流水线包含以下关键模块（Figure 2）：

1. **Gyro‑Permutation（输出通道置换）**：在向量剪枝前对输出通道进行重排，将不重要元素聚集到特定列向量中，提高后续全剪枝效率。
2. **向量剪枝（Vector Pruning）**：根据重要性分数完全移除一定比例（由参数 `vs` 控制）的列向量，形成全剪枝区域。
3. **Gyro‑Permutation（输入通道置换）**：在 N:M 剪枝前对每个 tile 内的输入通道独立重排，使重要权重在 2:4 稀疏 tile 内均匀分布，避免重要权重被 2:4 掩码强制移除。
4. **N:M 剪枝**：对 2:4 稀疏区域按行执行 2:4 结构化剪枝并生成 NM 索引。
5. **边界搜索（Boundary Search）**：联合搜索向量剪枝边界 `vs` 和局部稀疏边界 `ps`，最大化保留的重要性分数。
6. **Hard Concrete 掩码学习**：在逐步剪枝过程中使用可微掩码替换静态 2:4 掩码，通过梯度优化联合调整权重和掩码。

### 关键公式推导

#### 局部稀疏边界与目标稀疏度的关系

在给定目标稀疏度 `ts` 和向量剪枝比例 `vs` 后，剩余向量中分配给 N:M 稀疏的比例 `ps` 由以下约束关系确定：

$$ps = \frac{2(ts - vs)}{1 - vs}$$

**变量含义**：
- `ts`：目标整体稀疏度（Target Sparsity），即最终期望的零值权重比例。
- `vs`：向量稀疏边界（Vector Sparsity boundary），即被完全剪枝的列向量所占比例。
- `ps`：局部稀疏边界（Partial Sparsity boundary），即剩余向量中施加 2:4 稀疏的比例。

该公式的物理意义在于：在向量剪枝移除 `vs` 比例的列向量后，剩余 `(1 - vs)` 比例的向量中，需要将其中 `ps` 比例施加 2:4 稀疏（即每个 tile 中 50% 权重置零），使得整体稀疏度恰好达到 `ts`。Figure 4 展示了不同 `ts` 下 `vs` 与 `ps` 的可行域曲线，揭示了二者之间的权衡关系。

#### 边界搜索的优化目标

边界搜索的核心是最大化保留的总重要性分数 `R_total`：

$$\max_{vs, ps} \; R_{total} = R_{dense} + R_{24}$$

其中 `R_dense` 为密集区域保留的重要性分数之和，`R_24` 为 2:4 稀疏区域保留的重要性分数之和。搜索过程通过迭代调整 `vs` 和 `ps`，在满足目标稀疏度约束的前提下，找到使保留信息量最大的区域划分方案（Figure 3 展示了搜索的五个步骤）。

#### 可微掩码学习的复合损失

FlexHiNM‑GP 采用 Hard Concrete 分布生成软掩码，其采样中间变量为：

$$s_i = \sigma\left(\frac{1}{\tau}(\log \epsilon_i - \log(1 - \epsilon_i) + \log \alpha_i)\right)$$

其中 `τ` 为温度参数，`ε_i ~ Uniform(0,1)` 为随机噪声，`α_i` 为可学习参数。软掩码经过 0.5 阈值二值化得到硬掩码 `z_i`。训练时的复合损失函数为：

$$L = L_{\text{task}} + L_{\text{sparse}} + L_{\text{hard}}$$

$$L_{\text{sparse}} = \lambda_s \cdot \text{mean}(z_i)$$

$$L_{\text{hard}} = \lambda_c \cdot \text{mean}\left(\left| \sum_{i=1}^{4} z_i - 2 \right|\right)$$

**变量含义**：
- `L_task`：原始任务损失（如分类交叉熵）。
- `L_sparse`：稀疏性正则项，驱动掩码值趋向零，由系数 `λ_s` 控制强度。
- `L_hard`：硬 2:4 约束项，惩罚每个 tile 内保留权重数偏离 2 的情况，由系数 `λ_c` 控制强度。

该设计的因果机制在于：通过可微掩码学习，模型可以在训练过程中联合优化权重和稀疏模式，避免静态贪婪选择导致的次优解。消融实验（Table 2）表明，使用 Hard Concrete 掩码学习（H 组件）比固定静态 2:4 掩码可获得更高精度。

#### Gyro‑Permutation 的优化目标

通道置换的优化问题可形式化为在满足列向量掩码约束 `C_v`、2:4 掩码约束 `C_{2:4}` 和目标稀疏度约束 `C_s` 的前提下，最大化保留的重要性分数：

$$\operatorname*{argmax}_{\Lambda_O, \Lambda_I^0, \ldots, \Lambda_I^{T-1}} \| M \odot D[\Lambda_O; \Lambda_I] \| \quad \text{s.t.} \quad M \text{ satisfies } C_v, C_{2:4}, C_s$$

该问题被分解为两个子问题：
- **输出通道置换**：通过排列 `Λ_O` 将不重要元素聚集到将被剪枝的向量中。
- **Tile 级输入通道置换**：在每个 tile 内通过排列 `Λ_I` 使重要权重均匀分布，确保 2:4 掩码能保留更多关键权重。

Gyro‑Permutation 通过采样、聚类、分配三步迭代求解（Figure 6），采样调度采用粗到细模式（如 8, 1, 4, 1, 2, 1, 1），以平衡全局探索与局部精化。

### 单调性约束

为保证逐步剪枝的稳定性，边界参数需满足单调性约束：向量剪枝比例 `vs` 随目标稀疏度 `ts` 非递减（即 `d(vs)/d(ts) ≥ 0`），且剩余密集权重数 `M = N(1 + vs - 2ts)` 随 `ts` 平滑递减（`dM/dts < 0`）。这些约束确保了剪枝过程的渐进性和不可逆性，避免训练过程中的剧烈结构变化。



## 实验与关键发现

### 主要结果

FlexHiNM‑GP 在视觉 Transformer、文本编码器和大语言模型三类架构上均展现出相对于层次 N:M 基线的显著精度提升，且在高稀疏度下优势进一步放大。

**Deit 家族（ImageNet‑1K，V=64）。** 在逐步剪枝曲线（Figure 7a）中，FlexHiNM‑GP 在 75% 稀疏度下于 Deit‑Base 上取得 81.13% Top‑1 准确率，在 87.5% 稀疏度下仍保持 76.85%，超过 HiNM‑GP 约 1.2–1.5 个百分点。当向量尺寸扩大至 V=128 时（Figure G.1），差距更为突出：90% 稀疏度下 FlexHiNM‑GP 分别比 HiNM‑GP 高出 1.45%（Deit‑Small）和 1.28%（Deit‑Base）；在极端的 95% 稀疏度下，这一优势扩大至 2.19% 和 3.16%，表明三区域分配在高稀疏区能够有效保留关键权重，而固定 2:4 策略在此区域会强制移除大量重要元素。

**Bert‑Base（QQP / SST‑2 / SQuAD v1.1）。** Table 4 给出了 Gyro‑Permutation 的隔离贡献：FlexHiNM‑GP 相比无通道置换的 FlexHiNM，QQP F1 从 84.78 提升至 85.35（+0.57），SST‑2 准确率从 90.60% 提升至 91.65%（+1.05），SQuAD F1 从 88.04 提升至 88.55（+0.51）。这些增益表明，仅靠三区域划分无法完全解决 N:M 结构化稀疏引入的通道不对齐问题，Gyro‑Permutation 提供的额外重排是稳定提升的必要条件。


![[assets/figures/papers/iclr26_0010_YaZraqRsbB_FlexHiNM-GP_Flexible_Hierarchical_Pruning_via_Re/figures/014_Table_4.jpg]]
*Table 4: Impact of Gyro-Permutation on FlexHiNM*

**LLaMA2‑7B 下游任务。** Table 1 汇总了六个下游任务（OBQA、ARC‑C、ARC‑E、PIQA、HellaSwag、WinoGrande）在 75% 和 87.5% 稀疏度下的性能。在 75% 稀疏度时，FlexHiNM‑GP 的平均准确率比 HiNM‑GP 高 1.39%；在 87.5% 稀疏度时仍然保持优势。需要注意的是，该规模下的加速比与精度权衡尚未充分量化，且仅测试了两个稀疏度点，更细粒度的 scaling 行为仍需手动验证。


![[assets/figures/papers/iclr26_0010_YaZraqRsbB_FlexHiNM-GP_Flexible_Hierarchical_Pruning_via_Re/figures/009_Table_1.jpg]]
*Table 1: Llama2-7B Downstream task performance (%)*

### 消融实验

消融实验围绕三个核心组件展开：区域分配（F）、Hard Concrete 可微掩码学习（H）和 Gyro‑Permutation（G）。

**组件组合消融（Table 2，Deit‑Base）。** 六种变体中，同时包含 F 和 H 的变体①在 75% 和 80% 稀疏度下取得最优准确率（81.13%、79.46%），而包含 F 和 G 的变体②在 87.5% 及以上稀疏度表现最佳。这表明可微掩码学习在中低稀疏度下对精度保持贡献更大，而 Gyro‑Permutation 在高稀疏度下的通道对齐作用更为关键。单独使用 Hard Concrete（H）相比静态 2:4 掩码可获得更高精度，验证了可微掩码学习的有效性。


![[assets/figures/papers/iclr26_0010_YaZraqRsbB_FlexHiNM-GP_Flexible_Hierarchical_Pruning_via_Re/figures/012_Table_2.jpg]]
*Table 2: flow through hard-sigmoid activation and avoids categorical sampling, making it a more scalable choice for structured sparsity learning. Table 2: Ablation results under variants on Deit-Base*

**边界搜索策略消融（Table 3，Deit‑Base）。** 对比四种边界设定：HiNM‑GP（无区域分配）、OVW（纯向量剪枝）、BalFlexHiNM（固定边界）和 OptFlexHiNM（自适应搜索）。OptFlexHiNM 在所有稀疏度下均优于 BalFlexHiNM，其中在 95% 稀疏度时差距最大（约 1.5 个百分点），证明联合搜索 $v_s$ 和 $p_s$ 以最大化保留重要性分数 $R_{\mathrm{total}}$ 的策略能够为每层找到更优的稀疏分配方案。


![[assets/figures/papers/iclr26_0010_YaZraqRsbB_FlexHiNM-GP_Flexible_Hierarchical_Pruning_via_Re/figures/013_Table_3.jpg]]
*Table 3: Ablation results under boundaries on Deit-Base*

**Gyro‑Permutation 隔离消融（Table 4）。** 如前所述，移除 Gyro‑Permutation 后 FlexHiNM 在 QQP、SST‑2、SQuAD 上全面下降，证实通道置换是 FlexHiNM‑GP 精度优势的关键来源。该置换仅在边界搜索阶段执行，训练过程中通道顺序固定，因此其收益来自初始重排质量而非训练时的动态适应。

### 失败模式与局限性

1. **N:M 模式泛化未验证。** 当前所有实验均基于 NVIDIA Ampere Sparse Tensor Core 支持的 2:4 模式。对于其他 N:M 模式（如 3:4、1:4），三区域框架的扩展性和硬件兼容性尚未探索，需要手动验证。

2. **通道置换的静态性。** Gyro‑Permutation 仅在剪枝前的边界搜索阶段执行一次，训练过程中通道顺序保持不变。这意味着微调后权重重要性的变化无法被置换策略响应，可能在高稀疏度或长训练周期下产生次优分配。

3. **大语言模型的加速比缺失。** LLaMA2‑7B 实验仅报告了精度指标，未提供实际推理加速数据。FlexHiNM‑GP 的自定义 GPU 内核（双流执行：Stream0 处理稀疏 tile，Stream1 处理密集 tile）在 Transformer 上的 wall‑clock 加速效果需要进一步量化。

4. **极端稀疏度下的精度衰减。** 尽管 FlexHiNM‑GP 在 95% 稀疏度下显著优于基线，但与无结构剪枝上界的差距仍然存在（Figure G.1），说明结构化稀疏的固有信息损失在高压缩比下无法完全通过区域分配和通道重排弥补。

### 重要图表结论

- **Figure 7（V=64 逐步剪枝曲线）：** FlexHiNM‑GP 在 Deit 和 Bert 上均逼近无结构剪枝上界，且与 HiNM‑GP 的差距随稀疏度增加而扩大，验证了三区域分配在高稀疏区的关键作用。
- **Table 1（LLaMA2‑7B）：** FlexHiNM‑GP 在 75% 稀疏度下平均领先 HiNM‑GP 1.39%，证明该方法可扩展至 7B 级语言模型。
- **Table 2（组件消融）：** Hard Concrete 可微掩码与区域分配的协同作用在中低稀疏度下最优，Gyro‑Permutation 在高稀疏度下不可或缺。
- **Table 3（边界搜索消融）：** 自适应搜索（OptFlexHiNM）在所有稀疏度下优于固定边界，最大增益出现在 95% 稀疏度。
- **Table 4（Gyro‑Permutation 隔离）：** 通道置换为 FlexHiNM 带来 0.5–1.0 个百分点的稳定提升，是弥合三区域划分与硬件对齐之间差距的关键机制。

### 补充图表

![[assets/figures/papers/iclr26_0010_YaZraqRsbB_FlexHiNM-GP_Flexible_Hierarchical_Pruning_via_Re/figures/016_Figure_12.jpg]]
*Figure 12: Figure G.1: Gradual pruning for Deit family (V=128)*




## 定位与知识库关联

### 与基线方法的关系

FlexHiNM‑GP 处于层次化 N:M 剪枝方法的演进脉络上，其直接前身是 HiNM‑GP（带 Gyro‑Permutation 的层次 N:M 剪枝，但无区域分配）。两者的核心差异在于 FlexHiNM‑GP 引入了**三区域自适应分配**（密集区域、2:4 稀疏区域、全剪枝区域）和**可微掩码学习**两个关键改造槽位。

从方法谱系看，该工作的基线可划分为四个层级：

1. **Unstructured（无结构剪枝上界）**：代表不规则稀疏可达到的最高精度，但缺乏硬件加速支持。FlexHiNM‑GP 的目标是在保持 2:4 硬件兼容的前提下尽可能逼近这一上界。

2. **OVW（单纯外向量级剪枝）**：仅执行粗粒度的向量剪枝，可视为 HiNM 框架的特例（当 N:M 稀疏区域退化为零时）。它构成了 HiNM 系列方法的精度下界。

3. **HiNM‑V（无通道置换的层次 N:M 剪枝）**：等效于 Venom 方法，在向量剪枝后对所有保留向量统一施加 2:4 稀疏，但未进行通道重排。该基线用于隔离通道置换的独立贡献。

4. **HiNM‑GP（带 Gyro‑Permutation 但无区域分配）**：在 HiNM‑V 基础上增加了 Gyro‑Permutation 通道置换，但仍对所有保留向量施加统一的 2:4 稀疏。FlexHiNM‑GP 直接在此基线上叠加区域分配和可微掩码学习。

消融实验（Table 4）清晰量化了 Gyro‑Permutation 的独立贡献：移除通道置换后，FlexHiNM 在 QQP 上 F1 从 85.35 降至 84.78，SST‑2 准确率从 91.65% 降至 90.60%，验证了通道重排对缓解 N:M 结构化稀疏中通道不对齐问题的关键作用。

### 适用边界与泛化性

当前方法的验证范围存在明确的边界：

- **硬件平台**：仅在 NVIDIA Ampere Sparse Tensor Core（2:4 模式）上验证了自定义 GPU 内核的加速效果。对其他 N:M 模式（如 3:4、1:4）的泛化性尚未探索，这是一个显著的开放问题。

- **模型架构**：在 Deit‑Small/Base（视觉 Transformer）、Bert‑Base（编码器类语言模型）和 LLaMA2‑7B（解码器类大语言模型）上进行了验证。对视觉 Transformer（ViT）的其他变体或多模态模型的适用性尚未报告。

- **稀疏度范围**：在 75% 至 95% 的宽稀疏度范围内进行了逐步剪枝实验。在大语言模型（7B 级别）上仅测试了 75% 和 87.5% 两个稀疏度，更高稀疏度下的精度-加速权衡尚未充分量化。

### 已知局限

1. **通道置换的静态性**：Gyro‑Permutation 仅在边界搜索阶段执行，训练过程中通道顺序保持固定。这意味着置换方案无法适应微调过程中权重重要性的动态变化，可能限制了端到端优化的潜力。将通道置换纳入训练循环实现联合可微优化，是未来工作的一个自然方向。

2. **N:M 模式的单一性**：三区域框架目前仅针对 2:4 稀疏模式设计。将其扩展到更多 N:M 模式（如 1:4、3:4）并保持硬件兼容性，需要重新设计掩码约束和内核调度策略。

3. **大规模模型的加速验证不足**：在 LLaMA2‑7B 上的实验主要报告了精度指标，实际的推理加速比和吞吐量提升尚未充分量化，这限制了该方法在工业级部署场景中的说服力。

### 开放问题

- **多 N:M 模式扩展**：能否将三区域分层框架推广到支持 1:4、3:4 等多种 N:M 模式，并在不同硬件代际上保持兼容性？

- **端到端可微置换**：是否可以将 Gyro‑Permutation 的采样-聚类-分配流程替换为可微的通道重排机制，实现与掩码学习的联合端到端优化？

- **跨架构泛化**：该方法在视觉 Transformer（ViT）、多模态模型或混合专家（MoE）架构上的表现如何？区域分配策略是否需要针对不同架构的权重分布特性进行调整？



## 原文 PDF

![[paperPDFs/ICLR_2026/FlexHiNM_GP_Flexible_Hierarchical_Pruning_via_Region_Allocation_and_Channel_Permutation.pdf]]
