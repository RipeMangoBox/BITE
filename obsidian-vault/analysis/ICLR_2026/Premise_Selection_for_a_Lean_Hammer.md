---
title: "Premise Selection for a Lean Hammer"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Premise_Selection_for_a_Lean_Hammer.pdf
openreview_forum_id: m04JJNeRK6
aliases:
- PSLH
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/learning_theory
core_operator: "通过为锤子定制数据提取（包含隐式/显式前提）、规范化签名表示、掩码对比学习以及动态前提嵌入缓存，构建了首个可用于 Lean 的端到端领域通用锤子。"
primary_logic: "将神经前提选择与符号证明搜索相结合，并专门为依赖类型理论的锤子流水线设计前提选择，显著提升证明自动化。通过动态适应用户新定义的前提，使锤子可应用于训练数据之外的库和用户局部上下文。"
claims:
- "LEANHAMMER 使用 LEANPREMISE 比现有前提选择器多解决 21% 的目标。"
- "LEANPREMISE (large) 在 Mathlib-test 的 full 设置下取得 30.1% 的证明率。"
- "相对于 ReProver，LEANHAMMER 在 full 设置下多证明了 150% 的定理。"
- "LEANPREMISE 可动态适应用户上下文，推荐训练数据之外的新前提。"
---

# Premise Selection for a Lean Hammer

> [!tip] 核心洞察
> 将神经前提选择与符号证明搜索相结合，并专门为依赖类型理论的锤子流水线设计前提选择，显著提升证明自动化。通过动态适应用户新定义的前提，使锤子可应用于训练数据之外的库和用户局部上下文。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向 Lean 的锤子前提选择 |
| 英文题名 | Premise Selection for a Lean Hammer |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=m04JJNeRK6); [GitHub](https://github.com/hanwenzhu/premise-selection) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/learning_theory |
| Method | LEANPREMISE |
| Dataset | Mathlib-test |

> [!tip] 效果简介
> - Mathlib-test 上，Proof rate (full setting) 为 30.1% (LEANPREMISE large)，对比 Existing premise selectors (ReProver et al.)，变化 +21% more goals solved。
> - Mathlib-test 上，相对 ReProver 的提升 为 30.1% (LEANPREMISE large)，对比 ReProver，变化 150% more theorems proved。
> - Mathlib-test 上，Recall@32 为 72.7% (large model)，对比 67.8% (small model)，变化 +4.9%。

## 概述

### 问题瓶颈

在依赖类型理论的交互式定理证明中，锤子（hammer）是一种将当前证明目标翻译为一阶/高阶逻辑，并调用外部自动定理证明器（ATP）求解的关键自动化工具。然而，现有前提选择器存在两个根本瓶颈：**（1）未针对锤子工作流进行优化**——传统选择器通常为下一步策略生成或人工检视设计，提取的前提信息不足以支撑锤子发现端到端证明；**（2）无法动态适应用户局部上下文**——当用户定义训练数据之外的新引理时，选择器无法有效推荐这些前提，严重限制了锤子的适用范围。

### 核心方法

本文提出 **LEANHAMMER**，一个面向 Lean 4 的端到端领域通用锤子系统，其核心是神经前提选择器 **LEANPREMISE**。LEANPREMISE 通过四项关键设计解决上述瓶颈：

1. **定制数据提取**：同时提取显式和隐式前提（包括 `simp`、`rw` 等自动化策略调用的前提），覆盖 term-style 和 tactic-style 证明。
2. **规范化签名表示**：禁用符号美化、使用全限定名，将前提序列化为包含文档字符串、种类、名称、参数和类型的标准化签名。
3. **掩码对比学习**：采用带负采样和正例掩码的 InfoNCE 损失（温度参数 $\tau=0.05$）训练编码器，使状态嵌入与相关前提嵌入在余弦空间中接近。
4. **动态前提缓存**：预计算并缓存 Mathlib 库的前提嵌入，同时实时提取用户新定义前提的嵌入，通过 FAISS 实现快速检索，使锤子可应用于训练数据之外的库和用户局部上下文。

LEANHAMMER 流水线由 Aesop（证明搜索策略）、Lean-auto（翻译目标并调用 ATP Zipperposition）和 Duper（在 Lean 内部基于 ATP 返回的前提重建证明）三个模块协同构成，LEANPREMISE 在其中负责为搜索提供相关前提。

### 主要结果

在 Mathlib-test 基准上，LEANHAMMER 使用 LEANPREMISE（large 模型）在 full 设置下取得 **30.1%** 的证明率，比现有前提选择器多解决 **21%** 的目标。相对于基于检索的神经前提选择器 **ReProver**（Yang et al., NeurIPS 2023），LEANHAMMER 多证明了 **150%** 的定理。消融实验证实，定制的数据提取、负采样和损失掩码均对性能有显著贡献。在跨域泛化基准 miniCTX-v2-test 上，LEANPREMISE 同样展现出有效的动态适应能力，平均证明率达到 20.7%。

### 方法谱系与知识库定位

LEANPREMISE 属于**神经前提选择**方法，与基于检索的选择器（如 ReProver）共享对比学习范式，但通过面向锤子的数据提取和动态上下文适应实现了关键差异化。其符号-神经混合架构将前提选择嵌入到符号证明搜索流水线中，延续了“锤子”方法的传统（将 ITP 目标外包给 ATP），同时引入现代密集检索技术（FAISS 索引、余弦相似度检索）和掩码对比训练策略。该方法在 Lean 4 生态中填补了“可用的领域通用前提选择器”的空白，为后续神经与符号方法的深度融合提供了基础。

## 背景与动机

形式化数学的自动化证明一直是交互式定理证明（ITP）领域的核心挑战。在 Lean 等依赖类型理论（Dependent Type Theory）系统中，**锤子（hammer）** 是一种关键工具：它将当前证明目标与可用前提打包，翻译为一阶逻辑或高阶逻辑问题，交由外部自动定理证明器（ATP）求解，再将解翻译回 Lean 内部证明。然而，锤子的有效性高度依赖**前提选择（premise selection）**——从庞大的数学库中筛选出与当前目标最相关的少量前提。前提选择的质量直接决定了 ATP 能否在有限时间内找到证明：前提太少则信息不足，太多则搜索空间爆炸。

当前 Lean 生态中的前提选择工具存在两个结构性缺口。其一，现有选择器（如基于检索的 **ReProver**，Yang et al., NeurIPS 2023）并非为锤子工作流定制——它们为下一步策略生成而设计，所提取的前提范围和表示形式与锤子的需求不匹配。其二，这些工具仅能检索训练时见过的固定库前提，无法处理用户新定义的局部引理或训练数据之外的库，导致锤子在真实用户场景中失效。

这些缺口形成了一个因果瓶颈：**前提选择器未针对依赖类型理论的锤子流水线进行优化，且无法动态适应用户局部上下文，使得锤子自动化效果远低于其理论潜力。** 本文的核心动机正是填补这一空白——构建一个端到端、领域通用、可动态适应的 Lean 锤子，其前提选择组件从数据提取、表示学习到运行时推理均围绕锤子需求重新设计。

## 核心创新

LEANPREMISE 的核心创新在于围绕“锤子工作流”对神经前提选择进行了端到端的重新设计，解决了现有前提选择器（如 **ReProver** (Yang et al., NeurIPS 2023)）在依赖类型理论下与符号证明搜索脱节的问题。其关键改进体现在以下四个维度：

### 1. 面向锤子的数据提取与前提表示
传统方法仅提取显式出现在下一步策略中的前提，且使用包含符号美化和短名称的原始代码字符串表示。LEANPREMISE 则专门为 Lean-auto 的翻译过程定制了数据提取流水线：
- **提取范围扩展**：同时捕获 `term-style` 和 `tactic-style` 证明中的显式与隐式前提，包括 `simp`、`rw` 等自动化策略在底层调用的隐式前提。
- **签名规范化**：禁用符号美化（如将 `ℕ` 打印为 `Nat`），使用全限定名（如将 `I` 打印为 `Complex.I`），并将文档字符串、种类（定理/定义）、名称、参数和类型组合为统一的规范化签名表示。

### 2. 掩码对比学习
LEANPREMISE 采用带负采样和正例掩码的 InfoNCE 对比损失（温度参数 $τ=0.05$）训练编码器，替代标准对比损失：
$$\mathcal{L}(E) = \frac{1}{B} \sum_{i=1}^{B} \frac{\exp(\mathsf{sim}(E(s_i), E(p_i^+)) / \tau)}{\exp(\mathsf{sim}(E(s_i), E(p_i^+)) / \tau) + \sum_{p_i^- \in \mathcal{N}_i} \exp(\mathsf{sim}(E(s_i), E(p_i^-)) / \tau)}$$
该损失通过随机负采样和排除批次内正例的掩码，使模型学会区分真正相关的前提与表面相似的无关前提。

### 3. 动态运行时适应
LEANPREMISE 通过缓存 Mathlib 的嵌入向量，并在运行时动态提取和嵌入用户本地定义的新前提，利用 FAISS 进行快速余弦相似度检索：
$$\mathtt{select\_premises}(s, k, \mathcal{P}_s) = \mathtt{top-}k_{p \in \mathcal{P}_s} \mathtt{sim}(E(s), E(p))$$
这使锤子能够推荐训练数据之外的库前提和用户局部上下文中的新定义，突破了传统选择器仅能检索固定库的限制。

### 4. 统一锤子流水线集成
LEANPREMISE 作为前提选择器嵌入 LEANHAMMER 流水线，该流水线由 Aesop（可扩展证明搜索）、Lean-auto（依赖类型到高阶逻辑的翻译及外部 ATP 调用）和 Duper（ATP 返回前提的 Lean 内部重建）组成。Aesop 优先使用内建规则探索证明，失败后利用 LEANPREMISE 推荐的前提进行直接应用或调用 Lean-auto，实现了神经检索与符号搜索的深度耦合。

消融实验（Table 4）证实了上述创新的因果效应：使用朴素数据提取导致 Recall@32 从 71.9% 降至 66.8%，移除负采样使其降至 59.5%，移除损失掩码使其降至 69.6%，验证了每个设计选择对性能的显著贡献。

## 整体框架

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_m04JJNeRK6/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the LEANHAMMER pipeline. Phases that can neither fail nor produce a terminal proof are green, phases that can fail but cannot produce a terminal proof are yellow, and phases that can produce a terminal proof are blue. Black solid arrows indicate control flow, while red dashed arrows indicate the transfer of information between phases*

LEANHAMMER 是一个面向 Lean 4 依赖类型理论的统一锤子流水线，其核心设计目标是将神经前提选择与符号证明搜索深度耦合，以突破现有锤子工具在 Lean 生态中的自动化瓶颈。流水线由四个关键模块串联构成：**Aesop**（可扩展证明搜索策略）、**Lean-auto**（依赖类型到高阶逻辑的翻译与外部 ATP 调用）、**Duper**（ATP 返回前提的 Lean 内部证明重建）以及 **LEANPREMISE**（神经前提选择器）。图 1 以颜色编码呈现了各阶段的控制流与信息流：绿色阶段既不会失败也不会产生终结证明，黄色阶段可能失败但不能产生终结证明，蓝色阶段可以产生终结证明；黑色实线箭头表示控制流，红色虚线箭头表示阶段间的信息传递。

流水线的执行逻辑如下。Aesop 首先被调用，优先使用其内建规则搜索短证明；若快速失败，则利用 LEANPREMISE 推荐的前提进行两种尝试：(1) 直接应用前提（premise application rules），(2) 将前提传递给 Lean-auto 进行翻译与外部求解。Lean-auto 将依赖类型目标与选中的前提翻译为高阶逻辑问题，调用外部 ATP Zipperposition 求解；若 ATP 成功找到证明，Duper 基于返回的前提集合在 Lean 内部重建证明。这一设计使得前提选择同时服务于“直接应用”和“翻译后求解”两条路径，充分利用了神经检索与符号搜索的互补优势。

LEANPREMISE 作为流水线的前提选择引擎，通过对比学习训练的编码器将证明状态与候选前提嵌入同一向量空间，利用余弦相似度从可访问前提集中检索 top-k 个最相关前提：

$$\mathtt{select\_premises}(s, k, \mathcal{P}_s) = \mathtt{top-}k_{p \in \mathcal{P}_s} \mathtt{sim}(E(s), E(p))$$

其中 $E(s)$ 和 $E(p)$ 分别为状态和前提的嵌入表示。运行时，LEANPREMISE 缓存 Mathlib 固定版本的前提嵌入，并通过 FAISS 实现快速检索；同时支持动态提取用户局部定义的新前提并实时嵌入，使锤子能够适应训练数据之外的库和用户上下文。这一动态适应能力是 LEANPREMISE 区别于现有前提选择器（如 ReProver, Yang et al., NeurIPS 2023）的关键特性，后者仅能检索固定库中的前提，无法处理用户新定义。

## 核心模块与公式推导

LEANHAMMER 流水线由四个核心模块串联构成，LEANPREMISE 作为神经前提选择器嵌入其中，为后续符号证明搜索提供候选前提。以下聚焦 LEANPREMISE 的前提检索与训练机制。

### 前提检索

给定当前证明状态 $s$ 与可访问前提集 $\mathcal{P}_s$，LEANPREMISE 通过编码器 $E$ 分别嵌入状态与前提，利用余弦相似度检索 top-$k$ 个最相关前提：

$$
\mathtt{select\_premises}(s, k, \mathcal{P}_s) = \mathtt{top\text{-}}k_{p \in \mathcal{P}_s} \mathtt{sim}(E(s), E(p))
$$

其中 $\mathtt{sim}$ 为余弦相似度。运行时，Mathlib 库中所有前提的嵌入被预计算并缓存；当用户引入新定义时，系统动态提取并嵌入这些局部前提，通过 FAISS 在缓存与动态嵌入的联合空间内执行快速最近邻检索。这一设计使 LEANPREMISE 能够适应训练数据之外的库与用户局部上下文。

### 掩码对比学习

编码器 $E$ 通过掩码对比损失训练，目标是拉近状态嵌入与正例前提嵌入的距离，同时推远与负例的距离。损失函数采用带温度参数 $\tau = 0.05$ 的 InfoNCE 变体：

$$
\mathcal{L}(E) = \frac{1}{B} \sum_{i=1}^{B} \frac{\exp(\mathsf{sim}(E(s_i), E(p_i^+)) / \tau)}{\exp(\mathsf{sim}(E(s_i), E(p_i^+)) / \tau) + \sum_{p_i^- \in \mathcal{N}_i} \exp(\mathsf{sim}(E(s_i), E(p_i^-)) / \tau)}
$$

其中 $B$ 为批次大小，$s_i$ 为第 $i$ 个证明状态，$p_i^+$ 为对应的正例前提，$\mathcal{N}_i$ 为从可访问前提集中随机采样的负例集合。损失掩码机制确保批次内其他样本的正例不会被误当作当前样本的负例，从而避免梯度冲突。

### 数据提取与前提表示

LEANPREMISE 的数据提取管线专为锤子工作流设计，与面向下一步策略生成的提取方式存在本质差异：

- **提取范围**：同时捕获显式前提（直接出现在策略调用中的前提）与隐式前提（通过 `simp`、`rw` 等自动化策略间接引用的前提），覆盖 term-style 与 tactic-style 证明。
- **前提表示**：规范化签名表示，禁用符号美化（如 `ℕ` 打印为 `Nat`），使用全限定名（如 `I` 打印为 `Complex.I`），并将文档字符串、种类（定理/定义）、名称、参数和类型组合为统一的前提签名。

消融实验证实，定制数据提取与负采样、损失掩码均对性能有显著贡献：使用朴素数据提取时 Recall@32 从 71.9% 降至 66.8%；移除负采样后 Recall@32 进一步降至 59.5%；移除损失掩码则使 Recall@32 降至 69.6%（见表 4）。

## 实验与分析

### 主结果：Mathlib-test 上的证明率

LEANHAMMER 在 Mathlib-test 上进行了系统评估，所有实验使用统一的时间预算：每个 Zipperposition 调用 10 秒超时，每个定理 300 秒墙钟超时，以及 Lean 的默认心跳限制 200,000。

表 2 展示了不同前提选择器在 Mathlib-test 上的性能。LEANPREMISE (large) 在 **full** 设置下取得 **30.1%** 的证明率，而 ground truth 前提的证明率上限为 41.0%。与现有前提选择器相比，LEANHAMMER 使用 LEANPREMISE 多解决了 **21%** 的目标（Abstract 声明）。相对于基于检索的神经策略生成器 **ReProver**（Yang et al., NeurIPS 2023），LEANHAMMER 在 full 设置下多证明了 **150%** 的定理。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_m04JJNeRK6/figures/004_Table_2.jpg]]
*Table 2: Performance of LEANHAMMER with different premise selectors on Mathlib-test. Table 3: Out-of-Mathlib performance of LEANHAMMER on miniCTX-v2-test (Hu et al., 2025) using the large model trained on Mathlib. For other settings than full, see Table 5 of the extended version of this paper (Zhu et al., 2025)*

模型规模对性能有显著影响：Recall@32 从小模型的 67.8% 提升至大模型的 **72.7%**（+4.9%），full 证明率从 27.9% 提升至 30.1%。在 **cumul** 设置下，大模型单独取得 33.3% 的证明率，而跨模型规模的集成将累积证明率进一步提升至 **34.5%**（+4.4%）。

### 跨域泛化：miniCTX-v2-test

为验证 LEANPREMISE 对训练数据之外库和用户局部上下文的适应能力，论文在 miniCTX-v2-test（Hu et al., 2025）上进行了评估。该基准包含非 Mathlib 的定理，测试模型对未见前提的推荐能力。

LEANPREMISE (large) 在 miniCTX-v2-test 的 full 设置下取得 **20.7%** 的平均证明率。这一结果表明，通过动态提取并嵌入用户新定义的前提、利用 FAISS 快速检索，LEANPREMISE 能够有效泛化到训练数据之外的领域。该能力源于其运行时适应机制：缓存 Mathlib 嵌入的同时，动态处理用户局部上下文中的新前提。

### 消融实验

表 4 在 Mathlib-valid 上对 LEANHAMMER 的关键设计选择进行了消融，揭示了各组件对性能的因果贡献：

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_m04JJNeRK6/figures/005_Table_4.jpg]]
*Table 4: Ablation study of LEANHAMMER with different training settings on Mathlib-valid*

1. **定制数据提取 vs. 朴素数据提取**：使用 naive data extraction（仅提取显式前提，不包含 `simp`/`rw` 等自动化调用的隐式前提）导致 Recall@32 从 71.9% 降至 **66.8%**，full 证明率从 34.6% 降至 **33.1%**。这证实了同时提取显式和隐式前提、涵盖 term-style 和 tactic-style 证明的数据提取策略是性能的关键驱动因素。

2. **负采样**：移除负采样（no negative sampling）使 Recall@32 从 71.9% 大幅降至 **59.5%**（-12.4%），full 证明率从 34.6% 降至 **33.0%**。这表明带负采样的 InfoNCE 对比损失对学习有区分力的前提嵌入至关重要。

3. **损失掩码**：移除损失掩码（no loss mask）使 Recall@32 降至 **69.6%**（-2.3%），但累积证明率反而从 37.6% 升至 **38.4%**。论文将这一反常现象归因于噪音，但该点需要进一步验证——损失掩码的收益在 recall 指标上明确，但在端到端证明率上存在不确定性。

### 可用性对比

表 1 提供了现有前提选择工具的可用性对比，与表 2 的定量性能比较正交。LEANPREMISE 的关键优势在于：它是首个专门为依赖类型理论的锤子流水线设计的前提选择器，能够动态适应用户特定上下文，推荐训练数据之外的库前提和用户本地定义的引理。这使其在实际交互式证明场景中具有独特的实用价值。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_m04JJNeRK6/figures/002_Table_1.jpg]]
*Table 1: Usability comparison of existing premise selection tools. Note that this is orthogonal to the quantitative performance comparisons (Table 2)*

### 关键图表结论

- **图 1**：LEANHAMMER 流水线由 Aesop（优先使用内建规则探索证明）、Lean-auto（将目标翻译为高阶逻辑调用 Zipperposition）和 Duper（基于 ATP 返回前提重建证明）组成。绿色阶段不会失败且不产生最终证明，黄色阶段可能失败但不产生最终证明，蓝色阶段可产生最终证明。LEANPREMISE 在 Aesop 失败后介入，为直接前提应用和 Lean-auto 调用提供 top-k 前提。

- **表 2**：LEANPREMISE 在 full 设置下证明率 30.1%，显著优于现有前提选择器，且模型规模增加持续提升 recall 和证明率。

- **表 3**：在非 Mathlib 的 miniCTX-v2-test 上 20.7% 的证明率，验证了动态适应机制的有效性。

- **表 4**：定制数据提取和负采样是性能的核心支柱，损失掩码的端到端收益存在不确定性。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_m04JJNeRK6/figures/003_Table.jpg]]
*Table: *Performance upper bound, excluding errors. †Our definition is slightly different from Yang et al. (2023). See Section C of the extended version of this paper (Zhu et al., 2025)*

## 方法谱系与知识库定位

### 与现有前提选择器的关系

LEANPREMISE 是首个专门为依赖类型理论中锤子（hammer）工作流训练的神经前提选择系统。此前的神经前提选择器，如 **ReProver**（Yang et al., NeurIPS 2023），其设计目标是为下一步策略生成（next-tactic generation）提供前提推荐，而非服务于端到端的锤子证明搜索。这一设计差异在数据提取和前提表示两个关键环节产生了实质性分歧：

- **数据提取范围**：ReProver 等系统仅提取显式出现在人类证明步骤中的前提，而 LEANPREMISE 的数据提取管线同时捕获显式前提和隐式前提——后者指 `simp`、`rw` 等自动化策略在内部调用的引理。这些隐式前提对锤子的符号求解器（尤其是 Lean-auto 翻译到高阶逻辑后的 Zipperposition 调用）至关重要，但对策略生成则无关紧要。消融实验证实，替换为朴素数据提取后，Recall@32 从 71.9% 降至 66.8%，full 证明率从 34.6% 降至 33.1%（Table 4）。

- **前提表示规范化**：现有系统通常保留 Lean 的符号美化（notation pretty printing）和短名称（short names），而 LEANPREMISE 在签名提取时禁用符号美化（如将 `ℕ` 打印为 `Nat`）并强制使用全限定名（如将 `I` 打印为 `Complex.I`）。这一规范化使得编码器学习到的嵌入对符号求解器更友好，因为翻译到高阶逻辑时符号美化信息会丢失。

在定量层面，LEANHAMMER 使用 LEANPREMISE 在 Mathlib-test 的 full 设置下达到 30.1% 的证明率，相较现有前提选择器多解决 21% 的目标（Abstract），且相对 ReProver 多证明了 150% 的定理（Section 4）。

### 与符号证明工具的集成关系

LEANPREMISE 并非孤立的前提选择器，而是嵌入 LEANHAMMER 流水线中与多个符号证明组件协同工作。该流水线由三个核心模块构成（Figure 1）：

1. **Aesop**：可扩展的证明搜索策略，优先使用内建规则探索证明。若未快速找到证明，则使用 LEANPREMISE 推荐的前提尝试直接应用，或查询 Lean-auto。
2. **Lean-auto**：将依赖类型目标与前提翻译为高阶逻辑问题，调用外部 ATP（Zipperposition）求解。
3. **Duper**：基于 ATP 返回的前提集合在 Lean 内部重建证明。

这种神经-符号混合架构的设计理念是：神经组件（LEANPREMISE）负责缩小搜索空间，符号组件（Aesop、Lean-auto、Duper）负责在缩小的空间内进行可靠证明。与纯粹的神经证明系统（如 ReProver 的端到端策略生成）相比，LEANHAMMER 的优势在于符号组件提供了证明正确性的保证；与纯粹的符号锤子（如 CoqHammer）相比，LEANPREMISE 的神经检索显著提升了前提推荐的精度。

### 适用边界与动态适应能力

LEANPREMISE 的一个关键设计是运行时动态适应能力。在部署时，系统缓存 Mathlib 固定版本的前提嵌入，同时动态提取并嵌入用户在本地定义的新前提，通过 FAISS 进行快速检索。这一机制使得 LEANPREMISE 可以有效推荐训练数据之外的库前提以及用户局部上下文中的新引理。

跨域泛化实验验证了这一能力：在 miniCTX-v2-test（Hu et al., 2025）的非 Mathlib 分割上，仅在 Mathlib 上训练的 LEANPREMISE（large）仍能达到 20.7% 的平均证明率（Table 3）。这表明系统并非简单记忆训练库中的前提关联，而是学习到了可迁移的“状态-前提”相关性模式。

### 局限与开放问题

**当前局限**：

- 消融实验中移除损失掩码（loss mask）后，Recall@32 从 71.9% 降至 69.6%，但累积证明率反而从 37.6% 升至 38.4%（Table 4）。论文将此归因于噪音，但这一反常现象暗示损失掩码的设计可能在某些情况下过滤了有用的正例信号，其机制值得进一步分析。
- 模型集成（ensemble）仅通过简单组合不同规模的模型实现，累积证明率从 30.1% 提升至 34.5%，但更有效的集成方法仍有探索空间。

**开放问题**：

1. 更有效的模型集成方法（Section 4 明确提及）。
2. 神经方法与符号方法的更优组合策略，例如是否可以让神经组件直接指导 ATP 的搜索策略，而非仅提供前提集合。
3. 损失掩码对正例过滤的精确影响机制——当前消融结果中的反常提升需要更系统的归因分析。

## 原文 PDF

![[paperPDFs/ICLR_2026/Premise_Selection_for_a_Lean_Hammer.pdf]]
