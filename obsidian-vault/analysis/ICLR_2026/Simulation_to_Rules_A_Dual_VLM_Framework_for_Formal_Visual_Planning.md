---
title: "Simulation to Rules: A Dual-VLM Framework for Formal Visual Planning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Simulation_to_Rules_A_Dual_VLM_Framework_for_Formal_Visual_Planning.pdf
openreview_forum_id: 7tlLpQpGlx
aliases:
- SRDVFFVP
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "SimVLM的仿真反馈，用于指导GenVLM迭代优化PDDL文件。"
primary_logic: "通过将视觉规划分解为两个阶段：一个用于模拟动作结果的感知VLM（SimVLM）和一个用于生成和细化形式化规划文件的符号VLM（GenVLM），可以克服VLM的空间推理局限性和直接生成PDDL域文件的挑战。"
claims:
- "VLMFP结合SimVLM和GenVLM，分别用于感知/模拟和符号推理/文件优化，实现了多层面的泛化。"
- "SimVLM通过微调增强了空间推理能力，GenVLM利用大规模知识生成PDDL文件。"
- "VLMFP在未见实例上的规划成功率显著优于基线，证明其有效性。"
- "6 grid-world domains (average) 上 Success rate = 70.0% (Seen), 54.1% (Unseen)"
---

# Simulation to Rules: A Dual-VLM Framework for Formal Visual Planning

> [!tip] 核心洞察
> 通过将视觉规划分解为两个阶段：一个用于模拟动作结果的感知VLM（SimVLM）和一个用于生成和细化形式化规划文件的符号VLM（GenVLM），可以克服VLM的空间推理局限性和直接生成PDDL域文件的挑战。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 从模拟到规则：一种用于形式化视觉规划的双VLM框架 |
| 英文题名 | Simulation to Rules: A Dual-VLM Framework for Formal Visual Planning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=7tlLpQpGlx); [Project](https://sites.google.com/view/vlmfp) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | VLMFP |
| Dataset | 6 grid-world domains (average), Frozenlake, Sokoban |

> [!tip] 效果简介
> - 6 grid-world domains (average) 上，Success rate 为 70.0% (Seen), 54.1% (Unseen)，对比 30.7% (Seen), 32.3% (Unseen) [CodePDDL GPT-4o]，变化 +39.3% (Seen), +21.8% (Unseen)。
> - Frozenlake 上，Success rate 为 95.2% (Seen), 81.1% (Unseen)，对比 88.1% (Seen), 77.1% (Unseen) [CodePDDL GPT-4o]，变化 +7.1% (Seen), +4.0% (Unseen)。
> - Sokoban 上，Success rate 为 55.8% (Seen), 25.1% (Unseen)，对比 0.0% (Seen), 0.4% (Unseen) [CodePDDL GPT-4o]，变化 +55.8% (Seen), +24.7% (Unseen)。

## 概述

**问题瓶颈**：视觉语言模型（VLM）在直接处理空间细节和生成正确的PDDL域文件方面存在根本性局限，导致长期视觉规划任务中成功率低下。现有方法要么依赖单次生成缺乏反馈，要么无法精确感知场景中的空间关系与动作后果。

**核心思想**：VLMFP将视觉规划分解为两个专业化阶段——一个用于感知与动作模拟的SimVLM，和一个用于生成与迭代优化形式化规划文件的GenVLM。SimVLM通过微调获得精确的空间推理能力，GenVLM则利用大规模知识生成PDDL文件，并通过仿真一致性反馈实现迭代细化。

**方法定位**：VLMFP属于**双VLM协同的形式化视觉规划框架**，区别于直接生成计划（Direct）、思维链推理（CoT）或单次PDDL生成（CodePDDL）等基线。其关键创新在于引入了**仿真反馈闭环**：SimVLM的模拟执行结果与PDDL环境的符号执行结果进行双向比对（EW评分），产生的自然语言反馈驱动GenVLM更新文件，直至收敛。

**主要结果**：在六个网格世界领域上，VLMFP在未见实例上的平均规划成功率达到70.0%（已见外观）和54.1%（未见外观），相比最强基线CodePDDL（GPT-4o）分别提升39.3和21.8个百分点。在Sokoban等复杂领域，基线方法几乎完全失败（0.0%），而VLMFP达到55.8%和25.1%。消融实验表明，移除预设筛检、反馈机制或更新阶段均导致显著性能下降，其中移除更新阶段对复杂领域是灾难性的（成功率接近零）。在3D长程任务上，VLMFP同样展现出86.4%和79.8%的成功率。

**局限与展望**：SimVLM对全新游戏机制（如冰冻效果）的泛化能力有限；框架依赖固定PDDL域模板，向连续动作空间或开放环境的扩展仍需人工调整；GenVLM的迭代上限为4轮，EW分数不收敛时可能保留错误文件。未来方向包括提升对复杂物理动态的泛化、探索与其他形式化规划语言的兼容性。

## 背景与动机

视觉语言模型（VLMs）在跨模态理解方面取得了显著进展，但将其直接应用于长期视觉规划任务时，仍面临根本性的瓶颈：**VLMs在精细空间细节感知和正确生成形式化规划域文件方面的局限性，导致规划失败率居高不下**。具体而言，现有方法存在以下关键缺口：

1. **空间推理能力不足**：通用VLM在理解复杂空间关系、预测动作执行后果时容易出现幻觉或细节丢失。直接使用未经微调的VLM（如GPT-4o）进行场景描述和动作模拟，其输出在精确字符串匹配率上表现有限，难以支撑后续的符号化规划。

2. **PDDL域文件生成困难**：规划域定义语言（PDDL）要求精确的语法和语义规范。直接让VLM一次性生成完整的PDDL域文件和问题文件极易引入语法错误、遗漏约束条件或误解环境动态，且缺乏有效的自我纠错机制。基线方法CodePDDL（GPT-4o）在未见实例上的平均规划成功率仅为30.7%–32.3%，在复杂领域（如Sokoban）上几乎完全失效（0.0%–0.4%）。

3. **感知与符号推理脱节**：现有方法要么依赖纯符号规划器（需要人工提供精确的PDDL文件），要么完全依赖端到端的VLM推理，缺乏将视觉感知结果自动、可靠地转化为形式化规划规范的桥梁。这种脱节导致系统在面对未见过的视觉外观或环境布局时泛化能力严重受限。

针对上述缺口，**VLMFP**的动机在于：通过将视觉规划任务分解为两个专业化阶段——一个专注于感知与动作模拟的VLM（SimVLM），另一个专注于符号推理与PDDL文件生成优化的VLM（GenVLM）——来系统性克服单一VLM的局限性。SimVLM通过微调增强空间推理能力，为GenVLM提供精确的场景描述和动作执行参考；GenVLM则利用大规模知识生成PDDL文件，并通过仿真一致性反馈进行迭代优化，从而实现从视觉观测到可执行形式化规划的无缝转换。

## 核心创新

### 瓶颈洞察：从视觉感知到形式化规划的断裂

视觉语言模型（VLM）在长期视觉规划任务中面临一个根本性瓶颈：它们难以同时处理精细的空间细节和生成语法、语义均正确的PDDL域文件。直接让VLM端到端地完成“看图→生成规划文件”的路径，往往因空间推理的局限性和符号生成的不可靠性而失败。VLMFP的核心洞察在于，将这一复杂过程**解耦为两个专业化阶段**——感知模拟与符号生成优化——从而绕开了单一模型的能力瓶颈。

### 关键机制：SimVLM的仿真反馈驱动GenVLM迭代优化

VLMFP的因果调节旋钮是**SimVLM的仿真反馈**。框架引入了一个闭环：微调后的SimVLM负责从视觉输入中精确感知场景并模拟动作执行结果；GenVLM则基于SimVLM的场景描述生成PDDL文件，随后将PDDL环境下的符号执行结果与SimVLM的仿真结果进行一致性比对，产生自然语言反馈，驱动GenVLM迭代修正PDDL文件。这一“仿真-比对-修正”循环是VLMFP区别于以往方法的核心机制，使其能够自主纠正PDDL生成中的语义偏差。

### 相对于基线的方法槽位变更

与直接使用VLM生成计划或单次生成PDDL文件的基线方法相比，VLMFP在三个关键槽位上实现了根本性改变：

| 方法槽位 | 基线做法 | VLMFP做法 | 证据锚点 |
|---------|---------|----------|---------|
| **场景理解** | 直接使用VLM理解图像（如GPT-4o） | 使用微调后的SimVLM进行精确的空间描述和动作模拟 | Section 3.2, Step 1 |
| **PDDL文件生成** | 单次生成且无反馈（如CodePDDL） | 迭代生成并基于仿真一致性反馈优化 | Section 4.2 |
| **规划执行验证** | 无验证或仅依赖规划器自身 | 通过SimVLM仿真与PDDL环境执行的比较产生自然语言反馈 | Section 4.2, Simulation consistency checking |

这些槽位变更带来了显著的性能跃升。以最强的基线方法**CodePDDL（GPT-4o）**为参照，VLMFP在六个网格世界领域的未见实例上，成功率从30.7%提升至70.0%（视觉外观已见）和从32.3%提升至54.1%（视觉外观未见），分别提升了**39.3和21.8个百分点**（Table 2）。尤其在复杂领域如Sokoban中，基线方法几乎完全失败（0.0%/0.4%），而VLMFP达到了55.8%/25.1%，凸显了迭代优化机制在复杂约束场景下的不可替代性。

### 消融实验揭示的因果证据

消融实验（Table 3）进一步验证了各创新组件的因果贡献：
- **移除预设筛检**使平均成功率降至47.5%，复杂领域（Sokoban、Package）受影响尤为严重，说明语法/语义预过滤是后续一致性检查有效运行的前提。
- **移除反馈机制**使平均成功率降至61.1%，表明仿真一致性反馈为GenVLM提供了关键的修正信号。
- **移除更新阶段**对复杂领域是灾难性的——Sokoban、Package成功率几乎为零——证明单次生成无法应对复杂约束，迭代修正是成功的必要条件。

### 泛化能力的多层次验证

VLMFP的创新不仅体现在性能提升上，还表现在**多层面的泛化能力**：
- **视觉外观泛化**：SimVLM在未见视觉外观上的字符串匹配率仅比已见情况平均下降1.3%（Table 1），表明微调后的感知能力对视觉变化具有鲁棒性。
- **游戏规则泛化**：SimVLM在未见规则上保持较高成功率（Table 4），但在遇到完全新颖的机制（如Rule5的冰冻效果）时，动作执行预测完全失败，揭示了当前方法在全新环境动态面前的局限性。
- **任务维度扩展**：框架成功扩展至3D长周期规划任务（MultiRob、Assembly），在未见实例上达到86.4%/79.8%的成功率，但SimVLM的感知准确率（99.5%）与VLMFP的规划成功率（73.6%）之间的差距表明，从感知到符号规划的转换仍有优化空间。

### 需要人工验证的局限

以下局限性基于论文自身报告，需在实际应用中进一步验证：
- SimVLM对全新环境动态（如冰冻、传送等未见物理效果）的泛化能力有限。
- 框架依赖固定的PDDL域模板，扩展到完全开放或非栅格化环境时可能需要人工调整。
- GenVLM的迭代优化最大轮次为4，当EW分数无法收敛时，返回的PDDL文件可能仍存在错误。

## 整体框架

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_7tlLpQpGlx/figures/001_Figure_1.jpg]]

VLMFP 将形式化视觉规划分解为两个协同的 VLM 角色，构建了一条从像素到 PDDL 的闭环流水线（图 1）。其核心洞察是：直接让单一 VLM 同时处理空间感知与符号规划会导致两个环节的误差级联——感知模型难以捕获精确的空间关系，而生成模型缺乏对规划域语义的校验能力。VLMFP 通过引入 SimVLM（仿真视觉语言模型）和 GenVLM（生成视觉语言模型）的职责分离，切断了这一误差链路。

### 流水线模块与数据流

框架接收两类输入：**域描述** $n_d$（自然语言定义的动作空间与目标语义）和**问题图像** $i_p$（当前场景的视觉观测）。四个核心模块按序执行：

1. **SimVLM 场景感知**：SimVLM $V_S$ 基于 $n_d$ 和 $i_p$ 生成自然语言场景描述 $n_p$，精确刻画空间关系、物体位置和初始状态。这是后续符号化的唯一感知锚点。
   
2. **GenVLM 初始 PDDL 生成**：GenVLM $V_G$ 以 $n_d$、$i_p$ 和 $n_p$ 为条件，生成候选 PDDL 域文件 $f_d^{(0)}$ 和问题文件 $f_p^{(0)}$。此时的文件是“一次性”的，未经校验。

3. **预筛检**：对生成的 PDDL 文件进行语法和结构合法性检查，过滤掉包含语法错误或语义矛盾的文件。这一步在进入代价更高的仿真一致性检查之前拦截低级错误，是框架效率的关键保障。

4. **仿真一致性检查与迭代优化**：这是 VLMFP 的核心反馈回路。框架在 SimVLM 的仿真环境与 PDDL 执行环境之间执行双向动作可执行性比较，计算 EW 分数（Exploration Walk Score）量化两者的一致性。若一致性不足，系统生成自然语言反馈 $s$，GenVLM 据此更新 PDDL 文件：
   $$f_d^{(t)}, f_p^{(t)} = V_G \big( n_d, i_p, n_p ; s, f_d^{(t-1)}, f_p^{(t-1)} \big)$$
   该迭代最多进行 4 轮，直至 EW 分数收敛或达到轮次上限。

### 设计逻辑与因果机制

SimVLM 和 GenVLM 的分工对应了人类解决视觉规划问题的两个认知阶段：**感知模拟**与**符号抽象**。SimVLM 经过 430k 数据点的微调（基于 Qwen2-VL-7B），专门强化了空间关系描述和动作后果预测能力，其输出是结构化自然语言而非直接可执行代码——这降低了感知阶段的生成难度。GenVLM 则利用大规模预训练知识处理符号推理，其任务被限定为“根据精确的场景描述生成 PDDL 文件并响应反馈”，而非从原始像素直接跳跃到形式化语言。

消融实验（表 3）揭示了三个组件的因果重要性：移除预筛检使平均成功率降至 47.5%，复杂领域（如 Sokoban、Overcooked）受影响尤为严重；移除反馈机制使平均成功率降至 61.1%；而移除更新阶段对复杂领域是灾难性的，Sokoban、Package 的成功率几乎归零。这表明迭代反馈回路是框架在复杂约束下保持鲁棒性的核心机制，而非可有可无的增强。

## 核心模块与公式推导

### 双VLM架构

VLMFP框架由两个功能分化的视觉语言模型构成：**SimVLM**（Simulation VLM）负责感知与动作模拟，**GenVLM**（Generation VLM）负责符号推理与PDDL文件的生成及迭代优化。该分工的核心动机在于：直接让单一VLM从图像生成完整且正确的PDDL域文件极为困难，而将空间感知与符号生成解耦后，各模块可在其擅长的子问题上发挥优势。

**SimVLM**以Qwen2-VL-7B为基础模型进行微调，输入为领域描述 $n_d$、问题图像 $i_p$ 和动作序列 $\pi = [a_{1:T}]$，输出三类信息：(1) 自然语言场景描述 $n_p$；(2) 逐步推理与动作执行结果；(3) 目标达成判断。其微调数据集涵盖六个网格世界领域，共43万数据点。

**GenVLM**基于大规模VLM（如GPT-4o），利用SimVLM生成的场景描述 $n_p$ 作为桥梁，生成候选PDDL域文件和问题文件，并在仿真一致性反馈的驱动下迭代修正。

### 关键公式

**候选PDDL生成**（Section 3.2, Equation 1）：

$$n_p = V_S(n_d, i_p), \quad f_d^{(0)}, f_p^{(0)} = V_G(n_d, i_p, n_p)$$

其中 $V_S$ 为SimVLM，$V_G$ 为GenVLM，$f_d^{(0)}$ 和 $f_p^{(0)}$ 分别为初始生成的PDDL域文件和问题文件。SimVLM先将视觉观测转化为结构化自然语言描述，GenVLM再基于该描述生成形式化规划文件——这是整个框架信息流转的第一道关键环节。

**PDDL文件迭代优化**（Section 3.2, Equation 2）：

$$f_d^{(t)}, f_p^{(t)} = V_G \big( n_d, i_p, n_p ; s, f_d^{(t-1)}, f_p^{(t-1)} \big)$$

其中 $s$ 为来自仿真一致性检查的反馈信号，$t$ 为迭代轮次（最大轮次为4）。GenVLM在每轮迭代中接收上一轮PDDL文件的执行反馈，据此修正域定义和问题描述，直至PDDL环境与SimVLM的模拟结果对齐。

**勘探行走评分（EW Score）**（Section 4.2, Equation 3）：

$$m_{\mathrm{EW}}(\hat{d},\hat{p}) = 2\bigg(\Big(\frac{1}{T_{\max}}\sum_{T=1}^{T_{\max}}\mathbb{E}_{q\sim P_{\mathrm{sim},T}}[E_{f_d,f_p}(q)]\Big)^{-1}+\Big(\frac{1}{T_{\max}}\sum_{T=1}^{T_{\max}}\mathbb{E}_{q\sim P_{f_d,f_p,T}}[E_{\sin}(q)]\Big)^{-1}\bigg)^{-1}$$

该评分度量了SimVLM模拟环境与生成PDDL环境之间的双向动作可执行性相似度。具体而言，$P_{\mathrm{sim},T}$ 和 $P_{f_d,f_p,T}$ 分别表示在SimVLM和PDDL环境中长度为 $T$ 的随机动作序列分布，$E_{f_d,f_p}(q)$ 和 $E_{\sin}(q)$ 分别评估动作序列 $q$ 在对方环境中的可执行性。EW分数取两方向期望的调和平均，当两个环境在动作执行层面高度一致时分数较高，以此作为PDDL文件质量的量化指标和反馈生成的依据。

### 管线模块

框架的完整管线包含四个串联模块：

1. **SimVLM场景描述**：从图像中提取空间关系，输出自然语言描述 $n_p$。
2. **GenVLM初始生成**：基于 $n_d$、$i_p$、$n_p$ 生成候选PDDL文件 $f_d^{(0)}, f_p^{(0)}$。
3. **预设筛检（Prescreening）**：过滤语法错误或结构无效的PDDL文件，确保仅有效文件进入一致性检查。消融实验表明，移除此模块使平均成功率从70.0%降至47.5%（Table 3）。
4. **仿真一致性检查与迭代更新**：比较SimVLM与PDDL环境的执行结果，计算EW分数并生成自然语言反馈 $s$，驱动GenVLM更新PDDL文件。移除反馈机制使成功率降至61.1%，移除更新阶段则对复杂领域（Sokoban、Package、Printer、Overcooked）造成灾难性影响，成功率几乎归零（Table 3）。

## 实验与分析

### 主结果：VLMFP在六个网格世界领域全面超越基线

VLMFP在六个网格世界领域（Frozenlake, Maze, Sokoban, Package, Printer, Overcooked）的未见实例上取得了显著优于所有基线的规划成功率。如Table 2所示，以GPT-4o为GenVLM的VLMFP在可见外观（Seen）和不可见外观（Unseen）下的平均成功率分别达到**70.0%**和**54.1%**，而最强基线CodePDDL（GPT-4o）仅分别为30.7%和32.3%，提升幅度达**+39.3%**和**+21.8%**。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_7tlLpQpGlx/figures/005_Table_2.jpg]]
*Table 2: Success rate (%) comparison of VLMFP with baselines on 6 grid world domains*

领域级分析揭示了更关键的信息。在简单领域Frozenlake上，VLMFP的优势相对温和（Seen: 95.2% vs 88.1%，Unseen: 81.1% vs 77.1%），因为GPT-4o本身已具备较强的常识推理能力。然而，在复杂领域Sokoban上，VLMFP展现出决定性优势：CodePDDL（GPT-4o）的成功率几乎为零（Seen: 0.0%，Unseen: 0.4%），而VLMFP达到**55.8%**（Seen）和**25.1%**（Unseen）。这一对比直接证明了单纯依赖VLM生成PDDL文件而不进行迭代验证和优化的方法在需要精确空间推理和复杂约束的领域会系统性失败，而VLMFP的SimVLM仿真反馈机制是突破这一瓶颈的关键。

值得注意的是，GPT-5作为更强大的基础模型，其直接生成计划（Direct）和思维链（CoT）方法的成功率仍然极低（平均低于5%），表明单纯扩大模型规模无法解决形式化视觉规划的根本挑战——VLM在空间细节理解和PDDL语法正确性上的固有限制。

### 消融实验：三个组件的因果贡献

Table 3的消融实验揭示了VLMFP三个核心组件的不同因果角色：

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_7tlLpQpGlx/figures/006_Table_3.jpg]]
*Table 3: Success rate (%) when removing key components of VLMFP on 6 grid world domains*

**移除更新阶段（No Update）在复杂领域是灾难性的。** 移除PDDL文件迭代更新后，VLMFP退化为单次生成（类似CodePDDL基线），在Sokoban、Package、Printer、Overcooked四个复杂领域成功率几乎为零（分别为0.0%、0.0%、7.2%、1.1%）。这证明GenVLM的初始PDDL生成几乎总是包含错误，而迭代优化是使复杂领域可解的必要条件。

**移除反馈机制（No Feedback）使平均成功率从70.0%降至61.1%。** 这一降幅相对温和，因为GenVLM在没有显式反馈时仍能进行一定程度的自我修正。但在Sokoban领域，成功率从55.8%骤降至25.9%，表明仿真一致性反馈对需要精确动作建模的领域尤为重要。

**移除预设筛检（No Prescreening）使平均成功率降至47.5%。** 筛检的作用是过滤语法和语义错误的PDDL文件，防止无效文件进入一致性检查。在Overcooked领域，移除筛检导致成功率从48.6%降至18.1%，因为该领域的PDDL域文件结构复杂，GenVLM更容易产生语法错误。

### SimVLM的感知与模拟能力分析

SimVLM是VLMFP的感知基础，其性能直接影响整个框架的上限。Table 1显示，SimVLM在可见外观上达到**95.5%**（任务描述）、**85.7%**（执行推理）、**85.5%**（执行结果）、**82.4%**（目标达成）的平均字符串匹配率。在不可见外观上，这些指标分别为82.6%、88.1%、87.8%、85.6%，平均降幅仅**1.3%**，表明SimVLM对视觉外观变化具有强鲁棒性。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_7tlLpQpGlx/figures/004_Table_1.jpg]]
*Table 1: String matching rate (%) for 4 SimVLM output types on 6 grid world domains*

然而，SimVLM的泛化能力存在明确边界。Table 4的规则泛化实验显示，当Frozenlake引入全新游戏机制时，SimVLM的表现急剧分化。对于规则1-4（涉及目标位置、障碍物数量等变化），SimVLM维持了59.2%-99.0%的成功率。但对于Rule5（引入“冰冻”效果——代理可能被冻结在原地），SimVLM的执行结果匹配率降至**0%**，尽管推理步骤匹配率仍有71.1%。这说明SimVLM能够“描述”新规则，但无法正确“模拟”其物理后果，暴露了基于微调的感知模型在遇到训练分布外环境动态时的根本局限。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_7tlLpQpGlx/figures/007_Table_4.jpg]]
*Table 4: Success rate (%) when testing SimVLM on unseen rules for Frozenlake*

### 3D领域扩展验证

VLMFP在2个3D规划任务（MultiRob和Assembly）上进一步验证了框架的可扩展性。Table 5显示，SimVLM在3D领域保持了极高的感知准确率（任务描述99.5%，执行推理99.0%），但VLMFP的规划成功率降至73.6%（Seen）和86.4%（Unseen）。感知准确率与规划成功率之间的差距（约13-26个百分点）表明，从精确的场景理解到正确的PDDL符号化仍存在转换损失，这是当前框架在复杂3D场景下的主要瓶颈。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_7tlLpQpGlx/figures/009_Table_5.jpg]]
*Table 5: SimVLM String matching rate (%) and VLMFP Success rate (%) on 2 3D domains*

### 失败模式分析

综合Table 12的错误类型分布和消融实验结果，VLMFP的主要失败模式可归纳为三类：

1. **PDDL生成错误**：GenVLM在初始生成阶段产生语法或语义错误的PDDL文件，若预设筛检未能捕获或迭代优化未能修正，则导致规划失败。这在约束复杂的领域（如Overcooked、Sokoban）尤为突出。

2. **仿真一致性评分收敛失败**：当EW分数在最大迭代轮次（4轮）内无法收敛时，返回的PDDL文件可能仍包含未被检测的错误。Table 13的收敛率数据显示，复杂领域的收敛率显著低于简单领域。

3. **SimVLM感知失败**：在遇到全新环境动态（如Rule5的冰冻效果）时，SimVLM的动作模拟完全失效，导致后续所有步骤崩溃。这是当前框架最根本的泛化边界。

### 补充图表

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_7tlLpQpGlx/figures/011_Table_6.jpg]]
*Table 6: String matching rate (%) comparison across four metrics on 6 grid world domains*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_7tlLpQpGlx/figures/012_Table_7.jpg]]
*Table 7: String matching rate (%) for 4 SimVLM output types on 6 grid world domains, with LLaVA-NeXT-7B as the base model*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_7tlLpQpGlx/figures/013_Table_8.jpg]]
*Table 8: String matching rate (%) for 4 SimVLM output types on 6 grid world domains, with PaliGemma2-10B as the base model*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_7tlLpQpGlx/figures/014_Table_9.jpg]]
*Table 9: The mean of string matching rate (%) for 4 SimVLM output types on 6 grid world domains across 3 seeds*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_7tlLpQpGlx/figures/015_Table_10.jpg]]
*Table 10: The standard deviation of string matching rate (%) for 4 SimVLM output types on 6 grid world domains across 3 seeds*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_7tlLpQpGlx/figures/017_Table_11.jpg]]
*Table 11: Dataset and Task statistics for six grid world domains*

## 方法谱系与知识库定位

### 方法谱系与基线关系

VLMFP的核心贡献在于将视觉形式化规划分解为两个专业化VLM的协同工作流程，这与现有方法形成了清晰的分野。基线方法可分为三类：

**直接生成基线**（Direct GPT-4o/GPT-5）代表了VLM端到端规划的朴素尝试——模型直接从图像和域描述生成动作序列。这类方法在复杂领域（如Sokoban）几乎完全失败（成功率0.0%），暴露了VLM在空间推理和长期规划上的根本性局限。

**思维链基线**（CoT, Wei et al., 2022）通过显式推理步骤试图增强VLM的规划能力，但本质上仍依赖单一VLM同时处理感知、推理和规划。CoT (GPT-4o)在Sokoban上的0.0%成功率表明，即使引入中间推理，VLM仍无法可靠地处理需要精确空间操作的任务。

**CodePDDL基线**代表了将视觉输入转化为形式化规划语言的直接尝试——GPT-4o生成PDDL域和问题文件，然后由经典规划器求解。这一方法在六个网格世界领域的平均成功率为30.7%（Seen）和32.3%（Unseen），显著优于直接生成方法，但其瓶颈在于：单次生成的PDDL文件缺乏验证和优化机制，语法错误和语义不一致无法被自动纠正。

VLMFP相对于CodePDDL的关键改进在于引入了**闭环反馈机制**：SimVLM的仿真结果与PDDL环境执行结果通过EW评分进行双向比较，产生自然语言反馈驱动GenVLM迭代优化PDDL文件。这一机制使成功率从CodePDDL的30.7%提升至70.0%（Seen），增幅达39.3个百分点。消融实验（Table 3）进一步证实了这一机制的必要性：移除反馈机制导致平均成功率降至61.1%；移除更新阶段对复杂领域（Sokoban、Package、Printer、Overcooked）是灾难性的，成功率几乎归零。

### 适用边界

**有效边界：**
- 框架在**栅格化环境**中表现最佳，六个网格世界领域的平均成功率达到70.0%（Seen）和54.1%（Unseen）。FrozenLake领域（95.2% Seen）的成功表明，当环境动态相对简单且可预测时，VLMFP能够近乎完美地生成正确的PDDL文件。
- **视觉外观泛化**能力强：SimVLM在未见外观上的平均字符串匹配率仅比已见外观低1.3个百分点（Table 1），证明微调后的感知模块对视觉变化具有鲁棒性。
- 框架可扩展到**3D长期规划任务**，在MultiRob和Assembly领域分别达到86.4%和79.8%的成功率（Table 5），尽管3D任务中SimVLM的感知准确率（99.5%）与VLMFP的规划成功率（73.6%）之间存在显著差距。

**失效边界：**
- **全新环境动态**构成硬性障碍。SimVLM在FrozenLake的Rule5（冰冻效果）测试中，动作执行预测完全失败（0%执行成功率，Table 4），因为训练数据中未包含类似机制。这表明SimVLM的仿真能力本质上受限于训练分布，无法推理出未见过的物理效果。
- **复杂约束领域**的PDDL文件生成仍具挑战性。Sokoban在未见外观上的成功率仅为25.1%，远低于FrozenLake的81.1%，反映出GenVLM在处理复杂前提条件和连锁效应时容易产生语义错误。
- 框架依赖**固定的PDDL域模板**，需要人工提供域描述和动作模式骨架。对于完全开放或非栅格化环境，域模板的自动生成本身就是一个未解决的问题。

### 局限与开放问题

**已验证的局限：**
1. **SimVLM的泛化瓶颈**：当遇到训练分布外的环境动态（如Rule5的冰冻机制）时，SimVLM的动作模拟完全失效。这本质上是监督微调范式的固有限制——模型学会的是模式匹配而非因果推理。
2. **感知到符号的转换损失**：3D任务中SimVLM的感知准确率（99.5%）与VLMFP规划成功率（73.6%）之间的差距（Table 5）表明，即使感知近乎完美，GenVLM在将空间描述转化为正确的PDDL谓词和动作效果时仍会引入错误。
3. **迭代优化的收敛限制**：GenVLM的最大迭代轮次为4，当EW分数无法在此限制内收敛时，返回的PDDL文件可能仍包含错误（Table 13）。复杂领域（如Sokoban）的收敛率较低，说明当前反馈机制的信息量不足以快速纠正深层语义错误。
4. **组件依赖性**：消融实验（Table 3）表明，预设筛检、反馈机制和更新阶段三者缺一不可。移除预设筛检使平均成功率降至47.5%，且复杂领域受影响更大，说明语法和结构错误的早期过滤对后续优化至关重要。

**开放问题：**
1. **如何提升SimVLM对全新环境动态的泛化能力？** 可能的路径包括：引入基于物理引擎的仿真作为监督信号、使用对比学习增强空间关系表征、或采用元学习策略使模型快速适应新规则。
2. **框架能否扩展到连续动作空间或精细操作任务？** 当前框架依赖PDDL的离散动作表示，扩展到连续控制需要与运动规划器或基于采样的规划方法集成，这涉及不同形式化语言（如PDDL+）的选择。
3. **如何减少GenVLM在复杂约束下的生成错误？** 更强的基座VLM（如GPT-5）可能部分缓解这一问题，但根本性改进可能需要引入约束求解器作为验证器，或使用程序合成技术确保生成PDDL的语义正确性。
4. **框架是否适用于其他形式化规划语言？** VLMFP的双VLM架构原则上与PDDL无关——SimVLM提供环境仿真，GenVLM生成形式化规范。扩展到RDDL（用于随机规划）或HTN（用于层次规划）需要重新设计输出格式和验证机制，但核心的仿真-优化循环可以保留。

## 原文 PDF

![[paperPDFs/ICLR_2026/Simulation_to_Rules_A_Dual_VLM_Framework_for_Formal_Visual_Planning.pdf]]
