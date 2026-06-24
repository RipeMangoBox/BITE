---
title: "RL Grokking Recipe: How Does RL Unlock and Transfer New Algorithms in LLMs?"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RL_Grokking_Recipe_How_Does_RL_Unlock_and_Transfer_New_Algorithms_in_LLMs.pdf
openreview_forum_id: CJJ8VxOWbG
aliases:
- SRPTWUTPG
- RGRHDRUTNAL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "分阶段奖励设计：先使用每个测试用例的通过率作为密集奖励进行预热训练，使模型脱离零奖励区域，再切换到二元全通过率奖励，从而引导模型逐步发现并强化正确求解策略。"
primary_logic: "通过可控的OOD合成编程任务实验，证明恰当的RL训练配方（密集奖励预热 → 稀疏二元奖励）能够引发 grokking 相变，使原本 pass@K=0 的任务被解锁至 100% 准确率，表明RL并非仅限于强化已有技能，而是可以习得全新算法策略；同时，习得策略在探索性和组合性泛化轴上表现良好，但在转换性泛化（需要全新解题模式）上仍然失败。"
claims:
- "在 pass@K=0 的 Manufactoria-HAS 任务上，分阶段 RL 训练后 full pass rate 从 0% 提升至 100%。"
- "直接优化二元全通过奖励的GRPO在 pass@K=0 任务上完全停滞，根本原因是没有成功的 roll-out 提供梯度信号。"
- "两阶段训练（密集奖励预热→二元奖励）导致典型的 grokking 相变：长时间探索平台后奖励突然跃升至接近完美。"
- "RL 训练后在组合泛化任务（如 BouncingSim 的多物体组合）上，full pass rate 从接近 0% 提升至 60–70%。"
---

# RL Grokking Recipe: How Does RL Unlock and Transfer New Algorithms in LLMs?

> [!tip] 核心洞察
> 通过可控的OOD合成编程任务实验，证明恰当的RL训练配方（密集奖励预热 → 稀疏二元奖励）能够引发 grokking 相变，使原本 pass@K=0 的任务被解锁至 100% 准确率，表明RL并非仅限于强化已有技能，而是可以习得全新算法策略；同时，习得策略在探索性和组合性泛化轴上表现良好，但在转换性泛化（需要全新解题模式）上仍然失败。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | RL 领悟配方：强化学习如何解锁并迁移大语言模型中的新算法？ |
| 英文题名 | RL Grokking Recipe: How Does RL Unlock and Transfer New Algorithms in LLMs? |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=CJJ8VxOWbG); [GitHub](https://github.com/sunblaze-ucb/rl-grok-recipe) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Staged RL with Per-Test Warm-Up (Two-Phase GRPO) |
| Dataset | Manufactoria-HAS (pass@K=0 task), BouncingSim (compositional generalization), BouncingSim (explorative generalization) |

> [!tip] 效果简介
> - Manufactoria-HAS (pass@K=0 task) 上，Full pass rate (test) 为 100%，对比 0% (pass@K=0 for reference model)，变化 +100%。
> - BouncingSim (compositional generalization) 上，Full pass rate on unseen skill combinations 为 60–70%，对比 near-zero before RL，变化 +60–70%。
> - BouncingSim (explorative generalization) 上，Full pass rate on Easy/Medium difficulty 为 Easy 50–75%, Medium 15–50%，对比 near-zero before RL，变化 显著提升，随难度衰减。

## 概述

**核心问题**：在基础模型完全无法解决（pass@K=0）的困难编程任务上，标准强化学习训练为何失败，以及如何设计训练配方使大语言模型能够习得全新算法策略。

**方法定位**：本研究提出**分阶段 GRPO 训练配方**——先用每个测试用例的通过率作为密集奖励进行预热，将模型推出零奖励区域，再切换到二元全通过率奖励进行精化。该方法在标准 GRPO（Guo et al., 2025）框架内仅改变奖励函数阶段，同时探索了课程学习和经验回放等加速策略。研究在 DELTA 基准（包含 Manufactoria 和 BouncingSim 两个合成编程问题家族）上进行受控实验，系统考察可学习性与泛化性。

**核心发现**：
- **Grokking 相变**：分阶段训练配方可在 pass@K=0 任务上引发典型的 grokking 现象——经历长时间探索平台后，模型性能突然跃升至接近完美（Figure 5c）。在 Manufactoria-HAS 任务上，full pass rate 从 0% 提升至 100%（Figure 4）。
- **瓶颈诊断**：直接使用二元全通过奖励的 GRPO 在 pass@K=0 任务上完全停滞，根本原因是没有任何成功的 rollout 提供梯度信号（Figure 5a）；仅使用密集奖励虽能提供初始信号，但会快速饱和，全通过率始终低于 0.01%（Figure 5b）。
- **泛化能力**：RL 习得的策略在探索性泛化和组合泛化轴上表现良好（BouncingSim 组合泛化从接近 0% 提升至 60–70%，Figure 9c），但在需要全新解题范式的转换性泛化上仍然失败（Figure 9d）。
- **课程学习敏感性**：只有与目标任务结构高度对齐的中间课程（REGEX → HAS）才能成功迁移，结构不匹配的课程（COMPR）则无效（Figure 7）。

**证据强度**：上述结论均基于 4 次独立运行的平均值，在合成数据集上进行受控实验，超参数和训练框架保持一致。转换性泛化失败和课程学习对齐敏感性等限制需在后续研究中进一步验证。

## 背景与动机

### 大语言模型的推理能力与强化学习的角色

大语言模型（LLM）在数学、编程和科学推理等领域的表现已取得显著进展，但一个根本性问题尚未得到充分解答：当基础模型在某个任务上完全失败——即使用足够大的采样预算仍无法产生任何正确解答（pass@K=0）——强化学习（RL）能否使模型习得全新的算法策略，还是仅能强化其已有的启发式技能？

现有研究在推理增强方面主要依赖两类范式。一类是推理时扩展（如多数投票、蒙特卡洛树搜索），通过增加推理步数或采样数量来提升正确率；另一类是监督微调（SFT），利用人工标注或模型蒸馏的高质量推理轨迹进行模仿学习。然而，这些方法本质上受限于基础模型的先验能力边界：它们可以放大已有信号，却难以在模型完全无解的“零信号区域”中从零构建新的解题策略。

RL 提供了一个理论上有望突破此限制的路径。通过基于环境反馈的试错探索，RL 不依赖预存的正确轨迹，而是通过奖励信号引导策略搜索。但在实践中，标准 RL 训练配方面临一个关键的冷启动困境：当任务过于困难以至于所有 rollout 均失败时，二元成功/失败奖励始终为零，梯度信号完全消失，训练陷入停滞。

### DELTA 基准的设计动机

为系统性地研究上述问题，本文引入了 DELTA（Distributional Evaluation of Learnability and Transferrability in Algorithmic Coding）——一个受控的合成编程问题基准。DELTA 的设计围绕两个核心维度展开：

**可学习性（learnability）**：RL 能否解决基础模型在 pass@K=0 条件下完全失败的问题家族？这直接检验 RL 是否具备“从零发现”新算法策略的能力。

**可迁移性（transferability）**：RL 习得的算法技能能否泛化到分布外（OOD）场景？本文沿袭并扩展了 OMEGA 框架的泛化分类，定义了四个泛化轴——探索性泛化（同技能、更高难度）、组合性泛化（多技能组合）、转换性泛化（需要全新解题范式）以及课程泛化（通过中间任务桥接）。

选择合成编程环境作为实验平台具有多重优势。首先，编程任务天然提供廉价且分级的反馈信号：每个测试用例的通过状态构成从 0 到 1 的连续奖励空间，这为设计分阶段训练策略提供了可能。其次，合成问题家族通过模板化生成器严格控制难度分布和 OOD 偏移程度，消除了真实世界数据中的混杂偏差，使因果归因成为可能。DELTA 包含两个主要问题域：Manufactoria（基于自定义 DSL 的拼图式编程任务，要求模型学习全新的程序语法和解题策略）和 BouncingSim（物理模拟编程任务，涉及碰撞检测、运动学更新和周期性条件推导）。

### 核心研究问题

本文试图回答以下相互关联的问题：

1. 对于基础模型完全无法解决的任务（pass@K=0），什么样的 RL 训练配方能够可靠地触发“领悟”（grokking）相变——即从长期探索平台期突然跃升至近乎完美的准确率？
2. 这种 RL 驱动的算法习得在多大程度上能够泛化到分布外场景？是否存在某些泛化类型（如转换性泛化）构成当前方法的根本性障碍？
3. 课程学习和奖励塑形（reward shaping）技术如何影响 RL 在困难任务上的探索效率和最终性能？

## 核心创新

### 问题瓶颈：零奖励陷阱

本研究揭示了一个此前未被充分重视的关键瓶颈：在基础模型完全无法解决（pass@K=0）的困难编程任务上，标准的 GRPO 训练会完全停滞。GRPO（Guo et al., 2025）依赖多个 rollout 之间的奖励差异来提供梯度信号——当所有 rollout 都失败、奖励恒为零时，模型无法获得任何学习信号，探索过程被彻底阻断。实验证据清晰展示了这一失败模式：在 Manufactoria-HAS 任务上直接优化二元全通过奖励的 GRPO 训练曲线完全平坦（Figure 5a），模型无法脱离零奖励区域。

### 核心创新：分阶段奖励设计

针对上述瓶颈，本文的核心创新在于**分阶段奖励函数设计**——将单阶段的稀疏二元奖励替换为两阶段训练配方：

**第一阶段（密集预热）**：使用每个测试用例的通过比例作为连续奖励信号（$r \in [0,1]$）。该密集奖励将模型推出零奖励区域，提供初步的学习牵引力，使模型能够探索出部分正确的解题方向。

**第二阶段（稀疏精化）**：从预热检查点出发，切换到严格的二元全通过奖励（所有测试通过得 1，否则得 0）。此阶段强制模型将不完整的部分解精化为精确的完全正确解。

这一配方最关键的因果效应是**引发 grokking 相变**：在密集预热阶段，全通过率长期保持在接近零的水平；切换到二元奖励后，模型经历一段探索平台期，随后在某个临界点发生突变——奖励从接近零跃升至接近完美（Figure 5c）。这表明模型并非简单地逐步改进，而是在探索过程中突然“领悟”了正确的算法策略。

### 与基线的对比

| 训练策略 | 效果 | 失败原因 |
|---------|------|---------|
| 直接 GRPO + 二元奖励 | 完全停滞（pass@K=0 任务） | 无成功 rollout，无梯度信号 |
| 仅密集奖励 | 快速饱和，全通过率 < 0.01% | 奖励信号过于平滑，缺乏对完全正确解的强化 |
| **两阶段训练（本文）** | 全通过率 0% → 100% | 密集预热提供初始探索方向，二元奖励精化为完全解 |

消融实验进一步证实了分阶段设计的必要性：移除预热阶段直接使用二元奖励完全失败；仅使用密集奖励虽然能学习部分策略，但全通过率始终低于 0.01%，模型在局部最优处饱和（Figure 5b）。

### 辅助加速机制

在核心分阶段配方之上，本文还探索了两种加速 grokking 的辅助机制：

- **经验回放**：保存成功的推理轨迹，在后续采样时作为示例插入 rollout。该技术能够更早触发 grokking，但收敛速度略慢于标准训练（Figure 6）。
- **反馈循环**：将验证器的错误信息注入 rollout。该方法加速了 grokking 的出现，但降低了训练稳定性。

### 课程学习的对齐敏感性

除了奖励设计，本文还揭示了**课程学习对任务结构对齐的高度敏感性**。在 Manufactoria-HAS 任务上，先训练基础家族（START/APPEND/EXACT）再经过中间课程 REGEX 的路径成功迁移至目标 HAS 任务，而经过结构不对齐的 COMPR 课程则完全失败（Figure 7）。这表明课程学习的有效性取决于中间任务与目标任务的解题策略重叠程度，而非简单的难度递进。

### 核心洞察

通过可控的 OOD 合成编程任务实验，本文证明了恰当的 RL 训练配方（密集奖励预热 → 稀疏二元奖励）能够引发 grokking 相变，使原本 pass@K=0 的任务被解锁至 100% 准确率。这一发现表明 RL 并非仅限于强化已有技能，而是可以习得全新的算法策略——前提是奖励设计能够引导模型穿越零奖励的“死亡谷”。

## 整体框架

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_CJJ8VxOWbG/figures/002_Figure_1.jpg]]
*Figure 1: Overview of DELTA with controlled RL studies. Left: Synthetic Programming Problem families—Manufactoria with custom syntax and puzzle-like rules, BounceSim with physical simulation, etc. Right: Controlled RL experiments. Top: Learnability shows grokking, where RL shifts from long exploration to sudden convergence, uncovering strategies beyond reference models. Bottom: Generalization extends OMEGA (Sun et al., 2025) across four axes—Exploratory, Compositional, Transformative, and Domain-level—testing adaptation to harder or recombined tasks*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_CJJ8VxOWbG/figures/011_Table_1.jpg]]
*Table 1: Manufactoria Problem families with difficulty levels and acceptance criteria*

本文提出的 DELTA（**D**istributional **E**valuation of **L**earnability and **T**ransferability in **A**lgorithmic coding）框架构建了一套受控的合成编程问题基准，用于系统性地探究大语言模型在强化学习训练下的**可学习性**（learnability）与**可迁移性**（transferability）。该框架的核心设计逻辑是：通过模板化生成器精确控制问题的难度、分布和组合方式，从而在干净的实验条件下分离出 RL 训练配方的因果效应。

### 框架组成与任务空间

DELTA 包含两个核心的合成编程问题域：

1. **Manufactoria**：一个手工设计的分布外（OOD）问题域，采用完全自定义的 DSL 语法和基于机器人磁带颜色路由的谜题规则。问题族按难度分为 Basic、Easy、Medium、Hard 四个层级（Table 1），涵盖从简单追加/精确匹配到需要条件分支和循环的复杂逻辑。基础模型在该问题域上呈现明显的难度阶梯：Basic 族普遍可解，Medium 族仅 GPT-5 取得非平凡成功率，Hard 族全模型 pass@K=0。

2. **BouncingSim**：基于物理模拟的编程问题域，要求模型编写代码模拟物体在重力、碰撞等约束下的运动轨迹。该域包含六个单技能问题族（ROT OBJ、ROT BOX、MOV BOX、GRAVITY、MULTI BOX、MULTI OBJ），每个族按 BASIC 到 EXTREME 五个难度层级配置物理参数（Table 2）。基础模型在 BouncingSim 上的表现随难度和组合复杂度急剧衰减。

### 实验管线与模块关系

DELTA 的实验管线围绕 GRPO（Guo et al., 2025）强化学习微调循环构建，核心模块如下：

```
┌─────────────────────────────────────────────────────────┐
│                    DELTA 实验管线                         │
├───────────┬───────────┬───────────┬─────────────────────┤
│ 问题生成器 │ 基础模型   │ RL 训练环  │ 泛化评估轴           │
│ (模板化)   │ (pass@K   │ (GRPO)    │ (探索/组合/转换)     │
│           │  评估)    │           │                     │
└───────────┴───────────┴───────────┴─────────────────────┘
```

**问题生成器**：每个问题族从一个参数化模板出发（字母表、磁带操作、接受谓词、数值阈值），在约束搜索空间内扰动参数生成训练和测试实例。这保证了分布的可控性和实验的可复现性。

**基础模型评估**：首先对预训练模型进行 pass@K 评估，识别出 pass@K=0 的“困难前沿”任务族——这些族是 RL 可学习性研究的核心目标。

**RL 训练环**：默认配置为每步 48 个 prompt，每个 prompt 采样 16 个 rollout，学习率 $5 \times 10^{-7}$。训练环的核心创新在于**分阶段奖励设计**：

- **阶段一（密集奖励预热）**：使用每个测试用例的通过比例作为连续奖励信号（$r \in [0,1]$），将模型推出零奖励区域，获得初始学习牵引力。
- **阶段二（二元全通过奖励）**：切换到严格的二元奖励（所有测试通过得 1，否则得 0），强化精确解并触发 grokking 相变。

可选模块包括**经验回放缓冲区**（保存成功轨迹并在后续采样中作为示例插入）和**课程学习路径**（先在相关但更简单的任务族上预热再迁移到目标族）。

**泛化评估轴**：RL 训练后的模型在三个泛化轴上接受评估——探索性泛化（同族更高难度）、组合性泛化（多技能组合）和转换性泛化（需要全新解题范式）。

### 核心瓶颈与因果机制

该框架揭示的关键因果机制是：

- **瓶颈**：在 pass@K=0 任务上，标准 GRPO 因所有 rollout 均失败而完全缺乏梯度信号，训练停滞。
- **因果调节变量**：分阶段奖励设计（密集→稀疏）充当了“探索引导器”——密集奖励将策略搜索引导至正确解附近区域，二元奖励则将近似解精炼为精确解。
- **核心现象**：两阶段训练导致典型的 **grokking 相变**：长时间探索平台后，模型突然发现关键策略，奖励从接近零跃升至接近完美（Figure 5c）。这一现象在 Manufactoria-HAS 任务上最为显著：full pass rate 从 0% 提升至 100%（Figure 4）。

### 证据强度说明

上述因果链由消融实验严密支撑：移除预热阶段的直接 GRPO 完全失败（Figure 5a），仅使用密集奖励的训练快速饱和且全通过率始终低于 0.01%（Figure 5b）。课程学习实验进一步表明，只有与目标族结构对齐的中间课程（REGEX → HAS）才能成功迁移，结构不匹配的课程（COMPR）则无效（Figure 7），这验证了奖励信号设计而非数据量是核心因果因素。

## 核心模块与公式推导

### RL 训练框架：GRPO 微调循环

本工作的核心强化学习训练循环基于 **GRPO**（Group Relative Policy Optimization, Guo et al., 2025）。其关键机制在于：每个训练步采样多个 rollout，利用同一提示下不同生成结果之间的奖励差异来估计优势函数并进行策略梯度更新。默认配置为每个训练步使用 48 个提示，每个提示生成 16 个 rollout，学习率设为 $5 \times 10^{-7}$（Section 3.1）。

GRPO 的一个关键瓶颈在于：当任务属于 **pass@K=0** 类型（即基础模型在任意采样预算下均无法生成全通过的解答）时，所有 rollout 的二元全通过奖励均为零，奖励差异为零，梯度信号完全消失，训练因此停滞。这是直接应用标准 GRPO 在困难编程任务上失败的根本原因。

### 分阶段奖励设计：两阶段 GRPO

为解决 pass@K=0 任务上的零奖励困境，本文提出**分阶段奖励训练配方**，包含两个顺序模块：

**模块一：Per-Test Reward 预热阶段**
- **奖励函数**：将二元全通过奖励替换为每个测试用例的通过比例，即 $r_{\text{dense}} \in [0, 1]$，提供连续的密集奖励信号。
- **作用机制**：即使模型无法一次通过所有测试，部分正确的解答仍能获得非零奖励，从而产生梯度信号，将模型参数推出零奖励区域，使其进入有成功解答可达的探索空间。
- **局限性**：该阶段单独使用会快速饱和，全通过率始终低于 $0.01\%$，无法达到完全正确（Figure 5b）。

**模块二：Binary Full-Pass Reward 阶段**
- **奖励函数**：从预热阶段保存的检查点出发，切换回严格的二元奖励——所有测试用例通过得 $1$，否则得 $0$。
- **作用机制**：此时模型已具备生成部分正确解答的能力，二元奖励能够进一步强化精确的完全正确解，将模型从“部分正确”锐化至“完全正确”。

这一两阶段设计（密集奖励预热 → 稀疏二元奖励）是引发 **grokking 相变**的核心因果操作：训练曲线表现为长时间的低奖励探索平台，随后在某一时刻奖励突然跃升至接近完美（Figure 5c）。

### 加速模块：经验回放

作为可选加速模块，经验回放技术（Experience Replay）在训练过程中保存成功的推理轨迹。在后续采样时，将这些成功轨迹作为示例插入 rollout 中，为模型提供正向示范。实验表明，该技术可以更早触发 grokking 时刻，但收敛速度略慢于标准 GRPO；若进一步加入验证器反馈循环（Feedback-in-the-loop），会加速 grokking 但降低训练稳定性（Figure 6）。

### 关键物理公式（BouncingSim 环境）

以下公式来自 BouncingSim 物理模拟环境的形式化定义（Appendix A.2），是模型需要隐式习得的物理规律：

**完美弹性碰撞反射公式**：当小球与边界发生完美弹性碰撞时，速度向量按以下规则反射：
$$v' = v - 2 (v \cdot \hat{n}) \hat{n}$$
其中 $v$ 为碰撞前速度，$\hat{n}$ 为碰撞面法向量，$v'$ 为反射后速度。

**恒定加速度下的运动学更新**：
$$x(t)=x_0+v_{x0}t+0.5 a_x t^2, \quad y(t)=y_0+v_{y0}t+0.5 a_y t^2$$
其中 $(x_0, y_0)$ 为初始位置，$(v_{x0}, v_{y0})$ 为初速度，$(a_x, a_y)$ 为恒定加速度。

**正多边形间隙公式**：两个同心正 $n$ 边形对应边的平行支撑线之间的距离为：
$$\Delta := a(R_o) - a(R_i) = (R_o - R_i) \cos(\pi/n)$$
其中 $R_o$ 和 $R_i$ 分别为外接圆和内切圆半径。

**周期性角速度条件**：小球在两个旋转正多边形之间实现均匀周期运动的充要条件为：
$$\omega = \frac{k \cdot 2\pi v}{n (R_o - R_i) \cos(\pi/n)}$$
其中 $\omega$ 为多边形旋转角速度，$v$ 为小球线速度，$k$ 为任意正整数。该公式是转换性泛化任务的核心物理约束，当前 RL 训练后的模型仍无法习得此类需要全新解题范式的规律。

## 实验与分析

### 核心瓶颈：二元全通过奖励在 pass@K=0 任务上的失效

在基础模型完全无法解决（pass@K=0）的困难编程任务上，标准的 GRPO 训练面临根本性困境。GRPO 依赖于同一 prompt 下多个 rollout 之间的奖励差异来提供梯度信号，然而当所有 rollout 都无法通过全部测试用例时，二元全通过率奖励始终为零，模型无法获得任何有效的学习信号，训练完全停滞。这一机制性瓶颈在 Manufactoria-HAS 任务上得到了明确验证：直接优化二元全通过奖励的 GRPO 训练曲线完全平坦，模型无法脱离零奖励区域（Figure 5a）。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_CJJ8VxOWbG/figures/006_Figure_5.jpg]]
*Figure 5: Comparison of strategies solving “pass@K=0” tasks. (a) Directly optimizing for full-pass rate under GRPO fails. (b) Training with a per-test pass rate provides a smoother reward but quickly saturates. (c) A two-phase training—warming up with per-test pass rate, then switching to full-pass reward. All training is performed on Manufactoria-HAS family and the reference model Qwen3-4B-Instruct-2507*

### 分阶段奖励设计：从密集到稀疏的 grokking 路径

针对上述瓶颈，本文提出两阶段 GRPO 训练配方：

1. **预热阶段（密集奖励）**：使用每个测试用例的通过比例（per-test pass rate）作为连续奖励信号 $r \in [0, 1]$。这一密集奖励提供了平滑的梯度景观，引导模型从零奖励区域逐步探索出部分正确的解题方向。
2. **主训练阶段（稀疏奖励）**：从预热阶段的检查点出发，切换至严格的二元全通过奖励——所有测试用例通过得 1，否则得 0。这一阶段将模型已获得的近似解精炼为精确的完全正确解。

**关键实验结果**（Figure 5c）：在 Manufactoria-HAS 任务上，两阶段训练引发了典型的 **grokking 相变**——模型经历长时间的性能平台期后，全通过率突然跃升至接近完美。最终，该任务家族的全通过率从 pass@K=0 提升至 **100%**（Figure 4），实现了近 100 个百分点的绝对提升。

### 消融实验：各组件贡献的严格验证

**仅用密集奖励的局限性**（Figure 5b）：若仅使用 per-test pass rate 作为奖励而不切换至二元奖励，模型虽能学习部分策略，但全通过率始终低于 0.01%，训练在约 100 步后迅速饱和。密集奖励只能提供初步牵引力，无法驱动模型达到精确全通过。

**仅用二元奖励的失败**（Figure 5a）：直接使用二元全通过奖励的 GRPO 在 pass@K=0 任务上完全失败，训练曲线无任何上升趋势。这确认了预热阶段的必要性——模型必须首先脱离零奖励区域。

**经验回放的影响**（Figure 6）：引入经验回放缓冲（保存成功的推理轨迹并在后续采样时作为示例插入 rollout）可以更早触发 grokking 相变，但收敛速度略慢于标准 GRPO。进一步加入反馈循环（feedback-in-the-loop）虽能加速 grokking 的出现，却降低了训练的稳定性。

**课程学习中的结构对齐敏感性**（Figure 7）：在 Manufactoria-HAS 任务上，采用两阶段课程学习——先在基础问题家族（START/APPEND/EXACT）上训练，再经过中间课程——结果高度依赖于中间课程与目标任务的结构对齐程度。与 HAS 任务结构高度一致的 REGEX 课程能够成功迁移，使模型最终达到高全通过率；而结构不匹配的 COMPR 课程则完全失败，性能停滞在低位。这一发现表明，课程学习的有效性并非来自简单的难度递进，而是取决于任务间解题策略的深层结构一致性。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_CJJ8VxOWbG/figures/007_Figure_7.jpg]]
*Figure 7: Contrast of the two-stage curriculum learning for Manufactoria-HAS. Models first train on basic problems (START/APPEND/EXACT) before branching into one of two intermediate curricula: (i) Stage 2–REGEX, which leads to successful transfer and high pass rates on the target HAS family, or (ii) Stage 2–COMPR, which fails to transfer and plateaus at low performance*

### 泛化研究：习得策略的边界

在 BouncingSim 物理模拟环境上，模型在六个单技能家族的基础难度混合数据上训练 300 步（直接优化二元全通过奖励），训练曲线同样呈现 grokking 跳跃（Figure 9a），随后在三个泛化轴上接受检验：

- **探索性泛化**（同家族、更高难度）：表现随难度阶梯显著衰减——基础难度 70–85%，简单难度 50–75%，中等难度 15–50%，困难难度降至个位数百分比（Figure 9b）。
- **组合性泛化**（未见过的技能组合）：如 ROT BOX + MOV BOX 等多物体组合任务上，全通过率从 RL 训练前的接近 0% 提升至 **60–70%**（Figure 9c）。这表明 RL 习得的算法策略具有一定的可组合性。
- **转换性泛化**（需要全新解题范式）：在需要特殊周期性动态理解的 OOD 测试中，模型表现仍然接近零（Figure 9d）。算法策略的创新性泛化——即习得全新的解题模式——仍然是一个未解决的挑战。

### 失败模式与局限性

1. **密集预热并非万能**：在极难的任务家族（如 Manufactoria-PREPEND）上，即使使用 per-test pass rate 预热，模型仍无法逃离零奖励区域（Figure 8）。预热效果受模型基础能力和任务绝对难度的双重约束。
2. **训练后性能崩塌**：RL 训练在收敛后可能出现策略崩塌现象，模型丧失已习得的解题能力，需要提前停止或稳定化机制。
3. **课程学习的普适性受限**：如前所述，只有结构高度对齐的中间课程才能成功迁移，这限制了课程学习作为通用解法的适用范围。
4. **转换性泛化的持续失败**：在所有需要全新解题范式的 OOD 测试中，RL 训练后的模型表现均接近零，表明当前 RL 配方主要强化和组合已有技能，而非创造质性的新算法策略。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_CJJ8VxOWbG/figures/010_Figure_8.jpg]]
*Figure 8: Warm-up training on the harder Manufactoria-PREPEND family. Figure 9: Generalization Study on BOUNCINGSIM. (a) Training full-pass rate on the Basic-level mixture (6 families, 1k each) for Qwen3-4B-Instruct with binary full-pass reward shows a sharp grokking jump near step 200. (b) Explorative generalization: Before RL (top) the model rarely solves any OOD cases; after RL (bottom) it transfers to Easy/Medium/Hard variants with diminishing gains as difficulty increases (bars aggregate 6 families × 4 tiers; 100 prompts per cell, averaged over 4 runs). (c) Compositional generalization: Zero-shot composition of skills. (d) Transformative generalization: Qualitatively new dynamics (e.g., special...*

### 补充图表

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_CJJ8VxOWbG/figures/003_Figure_2.jpg]]
*Figure 2: The Manufactoria difficulty ladder. 14 problem families are grouped into Basic, Easy, Medium, and Hard levels according to average performance across four popular LLMs. Each test split contains 20–50 problems, and full pass rate are averaged over 4 independent runs*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_CJJ8VxOWbG/figures/012_Table_2.jpg]]
*Table 2: Problem-by-difficulty configurations (aggregated from generator defaults). Abbreviations: f = container diameter factor (relative to 300m base); out/in = outer/inner polygon sides; r = ball radius (m); v = linear speed range (m/s); ω = angular speed (rad/s); amp = translation amplitude (m); g = gravity mode; cts = number of boxes; n = number of balls*

## 方法谱系与知识库定位

### 核心方法定位

本文提出的核心方法是一套**分阶段强化学习训练配方**（Staged RL），其本质是在标准 GRPO 框架内对奖励函数和训练数据进程进行结构化改造，以解决基础模型在困难编程任务上 pass@K=0 时的学习停滞问题。该方法在方法谱系中处于**奖励塑形（reward shaping）与课程学习（curriculum learning）的交叉地带**，但其独特贡献在于揭示了这两种技术的组合如何触发大语言模型中的 **grokking 相变**——即从完全失败到近乎完美准确率的突然跃迁。

### 与基线方法的关系

**标准 GRPO 的失效边界**：本文的直接基线是 **GRPO with binary full-pass reward**（Guo et al., 2025）。在基础模型完全无法解决（pass@K=0）的任务上，该基线因缺乏任何成功的 rollout 提供梯度信号而完全停滞（Figure 5a）。这一失效并非 GRPO 算法本身的缺陷，而是二元全通过奖励在困难探索场景下的固有局限：当所有采样轨迹的奖励均为零时，策略梯度更新缺乏方向性信息。

**密集奖励的局限性**：另一个自然基线是仅使用 per-test pass rate 作为连续奖励。该方法能提供初始学习信号，使模型脱离零奖励区域，但会快速饱和——全通过率始终低于 0.01%（Figure 5b）。这表明密集奖励虽然能引导探索，但缺乏足够的压力将模型推向精确的完全正确解。

**课程学习的条件有效性**：本文还考察了通过先在相关但更简单的任务家族上训练来预热的方法。实验表明，课程学习的成功高度依赖于任务结构的对齐程度：使用与目标 HAS 任务结构一致的 REGEX 作为中间课程可以成功迁移，而使用结构不匹配的 COMPR 课程则完全失败（Figure 7）。这揭示了课程学习在算法推理任务中的关键约束——并非任意难度递进都能产生正向迁移。

### 方法谱系中的增量贡献

本文的分阶段训练配方（per-test reward warm-up → binary full-pass reward）在以下维度上构成了对现有方法的非平凡推进：

1. **从奖励塑形到相变触发**：传统的奖励塑形旨在平滑优化景观，而本文的配方通过阶段性切换奖励函数，实际上创造了一个“探索-精炼”双阶段动力学——预热阶段将模型推入成功解可达的区域，主阶段则通过二元奖励的严格压力强化精确策略。这种设计导致的不再是渐进式改进，而是典型的 grokking 相变（Figure 5c）。

2. **经验回放作为加速机制**：本文进一步探索了经验回放技术在 RL 训练中的应用——保存成功推理轨迹并在后续采样中作为示例插入。该技术可以更早触发 grokking，但收敛速度略慢于标准 GRPO；加入反馈循环会进一步加速 grokking 但降低训练稳定性（Figure 6）。这为理解 RL 训练中的探索-利用权衡提供了新的实证依据。

### 适用边界与关键局限

**预热效果的模型与任务依赖性**：密集奖励预热并非通用解法。对于极难的任务家族（如 Manufactoria-PREPEND），即使使用 per-test pass rate 预热，模型仍无法逃离零奖励区域（Figure 8）。预热效果因基础模型能力和任务难度而异，需要手动验证具体场景下的有效性。

**课程学习的对齐敏感性**：只有与目标问题结构高度一致的中间课程才能成功迁移。这一约束限制了课程学习在真实世界混合数据集上的普适性——如文中所述，在大规模混合语料中，“自然的课程式递进并不总是存在，添加松散相关的任务家族并不能可靠地平滑学习，甚至可能完全无效”。

**转换性泛化的根本失败**：在需要全新解题范式（如 BouncingSim 中依赖特殊周期性动态的变换任务）的 OOD 测试中，RL 训练后的模型表现依然接近零（Figure 9d）。这表明当前 RL 配方习得的算法策略在“模式创造”层面的泛化上存在根本性瓶颈——模型可以强化和组合已有技能，但难以产生质性的策略创新。

**训练稳定性问题**：RL 训练可能在收敛后出现性能崩塌，模型会丧失已习得的策略。这需要提前停止或额外的稳定化机制，但目前尚未提出系统性的解决方案。

### 开放问题

1. **转换性泛化的突破路径**：在需要全新解题策略的任务上，如何设计训练方法才能使 RL 习得的算法技能产生质性迁移？这可能需要超越当前奖励塑形范式的更根本性方法创新。

2. **困难前沿的显式追踪**：如何在大规模混合评估中显式识别和隔离“困难前沿”子集，以避免聚合指标被大量简单任务稀释？这关乎 RL 进展的可信评估。

3. **跨领域迁移的奖励设计**：在数学和科学等缺乏天然测试用例反馈的领域，如何构建等效的密集递进奖励信号（如基于评分标准的打分、步骤检查器、定理证明器验证）以复制编程任务中的 grokking 成功？

4. **grokking 相变的可靠触发条件**：如何系统性地设计奖励函数和数据混合，以在不同的任务难度和基础模型能力下可靠地触发 grokking 相变？当前配方仍需要针对具体场景进行调试。

5. **RL 崩塌的预防机制**：如何减轻或预防 RL 训练在收敛后出现的策略崩塌现象？可能的路径包括稳定化训练策略、智能早停机制或正则化方法，但均需进一步研究。

## 原文 PDF

![[paperPDFs/ICLR_2026/RL_Grokking_Recipe_How_Does_RL_Unlock_and_Transfer_New_Algorithms_in_LLMs.pdf]]
