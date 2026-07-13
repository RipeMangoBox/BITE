---
title: "An Agentic Framework with LLMs for Solving Complex Vehicle Routing Problems"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/An_Agentic_Framework_with_LLMs_for_Solving_Complex_Vehicle_Routing_Problems.pdf
project_link: null
code_link: null
openreview_forum_id: BMOgYw4EhQ
aliases:
- AAFL
- AFLSCVRP
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "将整体流程分解为三个可管理子任务，并引入四个专门智能体（生成、判断、修改、错误分析）进行迭代协作，确保跨功能一致性和约束满足。"
primary_logic: "通过让LLM扮演知识渊博的开发者角色，直接从原始VRP实例自动提取领域知识，并生成自包含的求解代码，无需手工模块或外部求解器；多智能体协同的迭代验证机制显著提高了生成代码的可靠性和解的可行性。"
claims:
- "AFL在所有17个测试VRP变体上实现了0%的运行错误率 (RER) 和100%的成功率 (SR)，远优于SGE (RER 94.1%) 和DRoC (RER 82.4%)。"
- "AFL在TSPLib、CVRPLib等标准基准上的最优性间隙 (gap) 为1.28%-6.66%，而SGE的间隙高达109%-660%，表明AFL生成解决方案的质量显著更高。"
- "消融研究表明，移除判断智能体 (JA) 和修改智能体 (RA) 后，问题描述的准确率急剧下降，代码可靠性和解的可行性受到严重影响。"
- "17 VRP variants (standard and electric) 上 RER (Runtime Error Rate) / SR (Success Rate) = 0% / 100%"
---

# An Agentic Framework with LLMs for Solving Complex Vehicle Routing Problems

> [!tip] 核心洞察
> 通过让LLM扮演知识渊博的开发者角色，直接从原始VRP实例自动提取领域知识，并生成自包含的求解代码，无需手工模块或外部求解器；多智能体协同的迭代验证机制显著提高了生成代码的可靠性和解的可行性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于大语言模型的智能体框架求解复杂车辆路径问题 |
| 英文题名 | An Agentic Framework with LLMs for Solving Complex Vehicle Routing Problems |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=BMOgYw4EhQ) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | AFL (Agentic Framework with LLMs) |
| Dataset | 17 VRP variants (standard and electric), TSPLib (50-200 nodes), CVRP (n=100), ECVRP (Large instances) |

> [!tip] 效果简介
> - 17 VRP variants (standard and electric) 上，RER (Runtime Error Rate) / SR (Success Rate) 为 0% / 100%，对比 94.1% / 5.9% (SGE)，变化 -94.1% / +94.1%。
> - TSPLib (50-200 nodes) 上，Gap (%) 为 1.28，对比 109.48 (SGE)，变化 -108.20。
> - CVRP (n=100) 上，Objective value 为 10.55 (AFL, T=10000)，对比 10.55 (HGS-PyVRP, best known)，变化 0.00% gap (tie)。

## 概要

车辆路径问题（VRP）是运筹优化领域的经典难题，现实场景中常伴随容量限制、时间窗、多车场、电动车辆充电等复杂约束。现有基于大语言模型（LLM）的求解方法，如 **SGE**（Iklassov et al., 2024）和 **DRoC**（Jiang et al., 2025b），虽然尝试利用LLM生成求解代码，但普遍依赖手工预定义模块或外部求解器，且缺乏系统的错误处理机制，导致运行时错误率居高不下、解的可行性难以保证。

本文提出 **AFL（Agentic Framework with LLMs）**，一个基于多智能体协作的全自动VRP求解框架。其核心思路是将整体求解流程分解为三个可管理的子任务——问题描述、代码生成、解决方案推导——并引入四个专门智能体（生成智能体GA、判断智能体JA、修改智能体RA、错误分析智能体EAA）进行迭代协作。AFL让LLM扮演“知识渊博的开发者”角色，直接从原始VRPLib实例中自动提取领域知识，端到端生成自包含的Python求解器代码，无需任何外部手工模块或人工干预。

实验覆盖17个VRP变体（含标准VRP和电动VRP），结果表明AFL在所有变体上实现了 **0%的运行错误率（RER）和100%的成功率（SR）**，远优于SGE（RER 94.1%）和DRoC（RER 82.4%）。在TSPLib、CVRPLib等标准基准上，AFL的最优性间隙（gap）仅为1.28%–6.66%，而SGE的间隙高达109%–660%。消融研究进一步证实，判断智能体和修改智能体的移除会显著降低问题描述准确率和代码可靠性，验证了多智能体协同迭代机制的关键作用。



车辆路径问题（VRP）是运筹学与组合优化领域的基础问题之一，其目标是在满足一系列复杂约束的前提下，为一组车辆规划最优配送路线。现实世界中的VRP往往包含容量限制、时间窗、多车场、回程取送货、电动车辆续航等多样约束，这些约束的任意组合会衍生出数十种变体，对求解器的通用性和自适应性提出了极高要求。

当前，针对VRP的求解方法大致可分为三类：精确算法、元启发式算法和基于学习的神经组合优化方法。精确算法在中小规模上可保证最优性，但面对复杂约束组合时计算代价指数增长。元启发式算法（如**HGS-PyVRP**）在标准基准上表现优异，但其核心代码高度针对特定问题结构设计——一旦引入新约束（如电动车辆或开放路径），就需要对算法底层进行大量手工修改，难以自然泛化。基于策略梯度的神经求解器（如**RF-POMO**）虽具备一定学习能力，但通常需要针对每个新变体重新训练模型，且对复杂约束的嵌入仍依赖手工特征工程。

近年来，大语言模型（LLM）在代码生成与推理任务上展现出显著能力，为自动化求解VRP提供了新范式。然而，现有基于LLM的方法普遍存在两个关键瓶颈：

**第一，缺乏真正的端到端自动化。** 早期方法如**SGE**（Iklassov et al., 2024）和**DRoC**（Jiang et al., 2025b）在生成求解代码时，仍需依赖手工预定义的外部模块或求解器（如OR-Tools），并要求人工介入进行实例特定信息的提取与集成。这使得整个流程并非从原始输入到最终解的完全自动化，限制了其在实际场景中的可部署性。

**第二，代码可靠性与解可行性严重不足。** 由于LLM单独生成代码时容易忽略或错误实现复杂约束，导致生成的程序频繁出现运行时错误，或产生违反约束的不可行解。实验数据表明，SGE的运行时错误率（RER）高达94.1%，成功率（SR）仅为5.9%；DRoC的RER也达到82.4%，SR仅17.6%（Table 5）。在解质量方面，SGE在TSPLib基准上的最优性间隙高达109%–660%，与已知最优解相去甚远（Table 6）。这些数字揭示了现有方法在可信度上的根本缺陷——生成的代码不可靠，得出的解不可信。

上述瓶颈的深层原因在于：LLM虽然具备代码生成能力，但缺乏对问题领域的深层理解和对生成结果的有效验证机制。单纯依赖单次提示或检索增强生成，无法保证代码在复杂约束下的逻辑一致性和执行正确性。

基于此，本文提出**AFL（Agentic Framework with LLMs）**，一个基于多智能体协同的LLM框架，旨在实现从原始VRP实例到高质量可行解的全自动化生成。AFL的核心动机是：让LLM扮演一个知识渊博的开发者角色，直接从原始输入中提取领域知识，生成自包含的求解器代码，并通过多智能体迭代验证机制确保代码的可靠性和解的可行性——无需任何手工模块、外部求解器或人工干预。



## 核心方法与创新机理

AFL 的核心创新在于将传统依赖手工模块与人工干预的 LLM-based VRP 求解流程，重构为**全自动、自包含的多智能体协同框架**，从根本上解决了代码不可靠与解不可行的瓶颈。其关键 changed slots 如下：

### 1. 代码生成方式：从手工集成到端到端自动生成

现有 LLM 方法（如 **SGE**（Iklassov et al., 2024）、**DRoC**（Jiang et al., 2025b））依赖手工预定义的模块或外部求解器（如 OR-Tools），需要人工进行集成与适配。AFL 则让 LLM 扮演“知识渊博的开发者”角色，直接从原始 VRPLib 实例中自动提取领域知识，端到端生成完整的 Python 求解器代码，无需任何外部求解器依赖（Table 1, Section 3.3）。生成的代码结构包含 `read_vrp`、`distance`、`cost`、`initial`、`destroy`、`insert`、`validate`、`main` 八个顺序生成的函数，采用统一的破坏-插入启发式，具备跨变体的灵活性（Figure 2）。

### 2. 人工干预程度：从半自动到完全自动化

基线方法在框架执行阶段仍需人工提取实例特定信息或进行干预。AFL 将整体流程分解为三个可管理的子任务——**问题描述**（Problem Description）、**代码生成**（Code Generation）和**解推导**（Solution Derivation），从原始输入到最终解决方案实现完全自动化，无需任何人工干预（Section 1, Table 1）。

### 3. 错误处理机制：从无反馈到迭代验证-修正闭环

这是 AFL 最关键的 changed slot。SGE 与 DRoC 缺乏系统的错误反馈与修正循环，导致运行错误率（RER）分别高达 94.1% 和 82.4%（Table 5）。AFL 引入了四个专门智能体形成闭环：

- **生成智能体（GA）**：负责生成问题描述与代码。
- **判断智能体（JA）**：评估描述与代码的正确性，检查与实例的冲突、内部一致性及输入定义的规范性。
- **修改智能体（RA）**：根据 JA 的反馈修正描述和代码。
- **错误分析智能体（EAA）**：在解推导阶段诊断运行时错误并提供修复建议。

这一多智能体协同的迭代验证机制使得 AFL 在所有 17 个测试 VRP 变体上实现了 **0% 的 RER 和 100% 的成功率（SR）**，远优于 SGE（SR 仅 5.9%）（Table 5）。消融实验进一步证实，移除 JA 或 RA 后问题描述准确率急剧下降，代码可靠性和解可行性受到严重影响（Figure 3, Section 4.5）。

### 4. 约束处理可靠性：从常被忽略到显式嵌入与反复检查

LLM 单独生成代码时常忽略或错误实现复杂约束。AFL 通过问题描述子任务显式提取约束集合 $K$（作为 $\mathcal{D}(\mathcal{G}) = \{P, S, K, X, Y, Z\}$ 的一部分），并在代码生成和判断阶段反复检查约束嵌入。这使得 AFL 生成的求解器能保证几乎所有约束得到满足，代码可靠性与解可行性接近 100%（Table 12）。



![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BMOgYw4EhQ/figures/003_Figure_1.jpg]]
*Figure 1: Overview of an agentic framework with LLMs for solving complex VRPs*

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BMOgYw4EhQ/figures/001_Table_1.jpg]]
*Table 1: Comparison of representative LLM-based approaches for VRPs*

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BMOgYw4EhQ/figures/004_Figure_2.jpg]]
*Figure 2: Code structure*

AFL 将复杂 VRP 求解流程分解为三个可管理的子任务：**问题描述（Problem Description）**、**代码生成（Code Generation）** 和 **求解推导（Solution Derivation）**。三个子任务由四个专门智能体协同驱动——生成智能体（GA）、判断智能体（JA）、修改智能体（RA）和错误分析智能体（EAA）——形成从原始 VRPLib 实例到可行解的端到端自动化流水线。

### 流水线概览

Figure 1 给出了框架的全局视图。给定一个 VRPLib 格式的 VRP 实例 $\mathcal{G}$，框架首先进入 **问题描述子任务**：GA 生成结构化的数学描述 $\mathcal{D}(\mathcal{G}) = \{P, S, K, X, Y, Z\}$，其中 $P$ 为问题类型标签，$S$ 为自然语言问题陈述，$K$ 为约束集合，$X$ 为所需输入字段，$Y$ 为期望输出格式，$Z$ 为优化目标。JA 随即从三个维度评估该描述——是否与实例冲突、内部是否自洽、输入定义 $X$ 是否与实例字段正确对应——并将反馈传递给 RA 进行修正。GA-JA-RA 在此子任务中迭代，直到描述通过验证。

**代码生成子任务** 接收通过验证的问题描述，GA 按序生成构成完整求解器的各函数：`read_vrp`（解析输入）、`distance`（计算距离矩阵）、`cost`（评估目标值）、`initial`（构造初始可行解）、`destroy`（随机移除部分客户）、`insert`（将移除客户重新插入以最小化额外成本）、`validate`（验证约束满足性）以及 `main`（协调初始化与迭代改进过程，采用模拟退火接受准则）。每个函数生成后，JA 检查其与问题描述的一致性、语法正确性和逻辑完备性，RA 根据反馈进行修正。这种逐函数生成-判断-修正的循环降低了 LLM 单次生成长代码的出错概率。

**求解推导子任务** 执行已生成的完整求解器代码。若出现运行时错误，EAA 诊断错误原因并生成修复建议，RA 据此修改代码。该子任务持续迭代，直至代码无错误执行并输出满足所有约束的可行解。

### 关键设计决策

**统一启发式模板**：AFL 采用单一的破坏-插入（destroy-insert）启发式作为求解器骨架，而非为不同变体设计不同算法。该模板通过修改 `destroy` 和 `insert` 函数中的约束检查逻辑来适配不同 VRP 变体的特定约束，在灵活性与代码可靠性之间取得平衡。

**缓存与复用**：框架将问题描述 $\mathcal{D}(\mathcal{G})$ 与对应生成代码存入缓冲区。当再次遇到相同问题类型时，可直接复用存储的代码，跳过代码生成阶段，仅需在求解推导阶段针对具体实例运行。

**全自动化与自包含性**：与依赖手工预定义模块或外部求解器（如 OR-Tools）的现有 LLM 方法不同，AFL 直接从原始 VRPLib 输入中提取领域知识，生成自包含的 Python 求解器代码，无需任何人工干预或外部依赖。Table 1 的对比显示，AFL 是唯一同时在“复杂 VRP 支持”“自包含性”“全自动化”和“高可信度”四个维度上达标的框架。

### 智能体角色总结

| 智能体 | 缩写 | 核心职责 |
|--------|------|----------|
| 生成智能体 | GA | 生成问题描述和求解器代码 |
| 判断智能体 | JA | 评估描述和代码的正确性与一致性 |
| 修改智能体 | RA | 根据 JA 或 EAA 的反馈修正描述和代码 |
| 错误分析智能体 | EAA | 诊断求解推导阶段的运行时错误并提供修复建议 |

四个智能体在三个子任务中形成两个闭环：GA-JA-RA 闭环保障问题描述和代码的静态正确性；EAA-RA 闭环处理运行时错误，确保最终产生可行解。这种多层验证机制是实现 0% 运行错误率（RER）和 100% 成功率（SR）的核心因素（Table 5），消融实验（Figure 3）进一步证实，移除 JA 或 RA 将导致问题描述准确率急剧下降。



### 3.1 流水线分解与智能体角色

AFL 将整体求解流程分解为三个可管理的子任务，并引入四个专门智能体进行迭代协作，形成“生成—判断—修正—错误分析”的闭环。

**三个子任务（Subtasks）**

1. **问题描述（Problem Description Subtask）**：从原始 VRPLib 实例自动生成结构化的数学描述。
2. **代码生成（Code Generation Subtask）**：顺序生成组成完整求解器的各函数，并由 GA/JA/RA 迭代完善。
3. **解推导（Solution Derivation Subtask）**：执行生成的代码，通过 EAA 诊断运行时错误并进行修复，直至产生可行解。

**四个专门智能体（Agents）**

- **生成智能体（Generation Agent, GA）**：负责生成问题描述和求解代码。
- **判断智能体（Judgment Agent, JA）**：评估描述和代码的正确性，检查与实例的冲突、内部一致性以及输入定义的规范性。
- **修改智能体（Revision Agent, RA）**：根据 JA 的反馈修正描述和代码。
- **错误分析智能体（Error Analysis Agent, EAA）**：在解推导阶段分析运行时错误并提供修复建议。

### 3.2 问题描述子任务

GA 为给定实例 $\mathcal{G}$ 生成结构化的问题描述：

$$\mathcal{D}(\mathcal{G}) = \{P, S, K, X, Y, Z\}$$

各分量含义：
- $P$：问题类型（如 CVRP、CVRPTW 等）
- $S$：自然语言文本描述
- $K$：约束集合
- $X$：所需输入（从 VRPLib 实例中提取的字段）
- $Y$：期望输出格式
- $Z$：优化目标函数

JA 对 $\mathcal{D}(\mathcal{G})$ 的评估检查三项：(i) 各分量是否与实例冲突；(ii) 分量之间是否内部一致；(iii) 输入定义 $X$ 是否在实例中正确指定。若发现问题，RA 进行修正，GA 和 JA 再次迭代，直至描述通过验证。

### 3.3 代码生成子任务

代码生成采用统一的破坏-插入（destroy-insert）启发式框架，按顺序生成以下相互依赖的函数（详见 Figure 2）：

| 函数 | 功能 |
|------|------|
| `read_vrp` | 解析 VRPLib 格式文件，提取输入数据 |
| `distance` | 计算距离矩阵 |
| `cost` | 计算给定解的目标函数值 |
| `initial` | 构建满足约束的初始可行解 |
| `destroy` | 随机移除一部分客户以进行扰动 |
| `insert` | 将移除的客户重新插入到可行位置，最小化额外成本 |
| `validate` | 验证解是否满足所有约束 |
| `main` | 协调初始化与迭代改进过程，采用模拟退火接受准则 |

GA 按顺序生成每个函数，每个函数建立在先前已生成的代码之上。每生成一个函数后，JA 和 RA 迭代修正未满足的需求、语法错误和逻辑不一致。

### 3.4 解推导子任务

执行生成的完整代码时，若出现运行时错误，EAA 分析错误信息并提供修复建议，GA 据此修改代码。此迭代持续至代码无错误执行并产生可行解。

### 3.5 模拟退火中的核心公式

在 `main` 函数中，模拟退火（SA）控制解的接受与温度调度：

**接受概率**（接受较差解的概率）：

$$P = \exp\left(-\frac{E_{\mathrm{new}} - E_{\mathrm{current}}}{T}\right)$$

其中 $E_{\mathrm{new}}$ 和 $E_{\mathrm{current}}$ 分别为新解和当前解的目标函数值，$T$ 为当前温度。

**温度调度**（线性冷却）：

$$T = \frac{\mathrm{iteration} - \mathrm{step} + 1}{10}$$

### 3.6 评估指标公式

**运行时错误率（RER）**：

$$\mathrm{RER} = \frac{V_{\mathrm{err}}}{V} \times 100\%$$

其中 $V_{\mathrm{err}}$ 为因运行时故障终止的程序数，$V$ 为总程序数。

**成功率（SR）**：

$$\mathrm{SR} = \frac{V_{\mathrm{succ}}}{V} \times 100\%$$

其中 $V_{\mathrm{succ}}$ 为无错误执行并产生可行解的程序数。



## 实验与关键发现

### 代码可靠性与成功率：AFL 实现零运行错误

AFL 在最关键的可靠性维度上实现了质的突破。在覆盖17个 VRP 变体（含标准与电动 VRP）的测试中，AFL 的**运行时错误率（RER）为 0%，成功率（SR）为 100%**（Table 5）。这意味着 AFL 生成的每一段求解器代码都能无报错执行并产出可行解。


![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BMOgYw4EhQ/figures/007_Table_5.jpg]]
*Table 5: RER and SR*

对比之下，同类 LLM 方法的表现极差：
- **SGE**（Iklassov et al., 2024）的 RER 高达 94.1%，SR 仅 5.9%——绝大多数生成代码在运行阶段即崩溃。
- **DRoC**（Jiang et al., 2025b）的 RER 为 82.4%，SR 为 17.6%，虽有检索增强但仍远未达到可用水平。

这一差异的因果机制在于 AFL 的多智能体迭代验证闭环：判断智能体（JA）和修改智能体（RA）在代码生成阶段逐函数检查正确性，错误分析智能体（EAA）在求解推导阶段诊断运行时错误并提供修复建议。消融实验（Figure 3, Section 4.5）直接验证了这一点——移除 JA 或 RA 后，问题描述的准确率急剧下降，代码生成失败率显著升高，证明了这些智能体对维持流水线稳定性和代码可靠性的不可或缺。


![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BMOgYw4EhQ/figures/009_Figure_3.jpg]]
*Figure 3: Ablation studies on the JA and RA*

### 解质量：在标准与实用基准上接近 SOTA

AFL 不仅在可靠性上碾压同类 LLM 方法，其解质量也显著优于它们，并在多数问题上逼近最先进专用求解器。

**标准基准（Table 3, Table 11）**：在覆盖12个 VRP 变体的48个100节点标准实例上，AFL（T=10000）的最优性间隙（gap）在多数问题上控制在 3% 以内。具体而言：

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BMOgYw4EhQ/figures/005_Table_3.jpg]]
*Table 3: Comparison results on standard benchmarks. More results are shown in Table 11*

- CVRP（n=100）：AFL 目标值 10.55，与 **HGS-PyVRP**（已知最优）持平，gap 为 0.00%。
- CVRP（n=200）：AFL 目标值 9.95，gap 为 0.51%。
- CVRP（n=400）：AFL 目标值 18.61，gap 为 1.75%。
- CVRPTW（n=100）：AFL 目标值 11.71，gap 仅 0.34%。

**实用基准（Table 4）**：在电动 VRP（EVRP）变体上，AFL 展现出对传统元启发式的显著优势。以 **ACO**（蚁群优化）为基线：

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BMOgYw4EhQ/figures/006_Table_4.jpg]]
*Table 4: Comparison results on practical benchmarks*

- FRRPP 大规模实例：AFL（T=10000）的 gap 为 **-24.45%**，即目标值比 ACO 低近四分之一。
- FRRPP 小规模实例：AFL 的 gap 为 -2.72%。

**与同类 LLM 方法的对比（Table 6）**：在 TSPLib、CVRPLib 等经典基准上，AFL 的 gap 为 1.28%–6.66%，而 **SGE** 的 gap 高达 109%–660%，差距在两个数量级以上。**ReEvo**（Ye et al., 2024）的 gap 为 2.17%–7.42%，虽优于 SGE 但仍逊于 AFL。


![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BMOgYw4EhQ/figures/008_Table_6.jpg]]
*Table 6: Gap comparison on benchmark instances*

### 迭代步数的效果：解质量随 T 增加持续提升

AFL 采用模拟退火框架，解质量随迭代步数 T 的增加而单调改善（Table 3, Table 4, Figure 4a）：
- T=500 → T=2000 → T=10000 时，所有变体上的 gap 均呈下降趋势。
- 以 CVRP（n=50）为例：T=500 时 gap 为 10.89%，T=2000 时降至 10.70%，T=10000 时进一步降至 10.59%。

这一趋势的代价是时间开销的增加（Figure 4b），但 AFL 在 T=10000 时仍能在可接受的时间内完成求解。

### 多智能体协作策略的有效性

AFL 的多智能体迭代流程相比简化的提示策略具有显著优势（Table 9）。实验对比了三种策略：

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BMOgYw4EhQ/figures/012_Table_9.jpg]]
*Table 9: Gap comparison across different prompting strategies*

1. **AFL 标准流程**（多智能体迭代验证）
2. **单次提示**（一次性生成全部代码）
3. **备选提示**（多次独立生成后选最优）

AFL 标准流程在所有测试变体上始终实现最低的 gap 和最高的成功率，验证了迭代验证-修正闭环对代码质量和解可行性的因果贡献。

### 失败模式与局限性

尽管 AFL 在可靠性上表现卓越，但仍存在以下边界：

1. **大规模实例的解质量差距**：在 CVRPLib-XXL（高达 16k 节点）上，AFL 能成功运行（Table 18），但解质量不及专门针对该问题调优的先进求解器（如 **POMO**、**LEHD**）。这表明单一的破坏-插入启发式在大规模场景下存在搜索效率瓶颈。

2. **代码生成阶段的时间开销**：代码生成阶段约需 30 分钟（Table 10），虽然相比人类专家设计已极快，但对于需要实时响应的应用场景仍需优化。

3. **LLM 依赖性**：AFL 默认使用 GPT-4.1，在不同 LLM 上的性能存在差异（Table 16），框架效果受底层模型能力制约。

4. **问题迁移的开放性**：当前验证集中在 VRP 领域，能否直接迁移到其他组合优化问题（如调度、装箱）尚待探索。

### 补充图表

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BMOgYw4EhQ/figures/002_Table_2.jpg]]
*Table 2: Constraint descriptions and corresponding VRPLib-format fields*

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BMOgYw4EhQ/figures/010_Table_7.jpg]]
*Table 7: Constraint composition of VRP variants*

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BMOgYw4EhQ/figures/011_Table_8.jpg]]
*Table 8: Main sections of a VRPLIB instance file with descriptions and example*




## 定位与知识库关联

### 1 与现有LLM-based VRP方法的对比定位

AFL 的核心定位是**首个实现全自动化、自包含、高可信度的LLM驱动VRP求解框架**。与已有工作的关键差异体现在三个维度（Table 1）：

- **自包含性（Self-Containment）**：现有方法如 **SGE**（Iklassov et al., 2024）和 **DRoC**（Jiang et al., 2025b）依赖手工预定义的模块或外部求解器（如OR-Tools），需要人工集成领域知识。AFL 直接从原始VRPLib实例自动提取领域知识，生成完整的Python求解器代码，无需任何外部依赖或手工模块。
- **全自动化（Full Automation）**：**ARS**（未提供完整引用）和 **DRoC** 在框架执行阶段仍需人工提取实例特定信息或干预。AFL 从原始输入到最终解决方案完全自动化，无需任何人工干预。
- **高可信度（High Trustworthiness）**：SGE 和 DRoC 缺乏系统的错误反馈与修正循环，导致高运行时错误率和不可行解。AFL 引入判断智能体（JA）、修改智能体（RA）和错误分析智能体（EAA），形成迭代的验证-修正闭环，确保代码正确性和解的可行性。

在解质量方面，AFL 在 TSPLib、CVRPLib 等标准基准上的最优性间隙（gap）为 1.28%-6.66%，而 **SGE** 的间隙高达 109%-660%（Table 6），表明 AFL 生成解决方案的质量显著更高。在代码可靠性上，AFL 在所有 17 个测试 VRP 变体上实现了 0% 的运行错误率（RER）和 100% 的成功率（SR），远优于 SGE（RER 94.1%）和 DRoC（RER 82.4%）（Table 5）。

### 2 与专用求解器的关系

AFL 并非旨在替代最先进的专用 VRP 求解器，而是提供一种**通用、灵活且无需问题特定调优**的替代方案：

- 在 CVRP 等被充分研究的问题上，AFL（T=10000）与 **HGS-PyVRP**（当前最先进的启发式求解器）在 n=100 实例上达到平手（目标值均为 10.55），但在 n=200 和 n=400 实例上仍存在差距（Table 3, Table 11）。
- 与通用运筹优化求解器 **OR-Tools**（Furnon & Perron）相比，AFL 在多数变体上表现相当或更优。
- 与基于策略梯度的神经组合优化求解器 **RF-POMO** 相比，AFL 在多个变体上展现出竞争力。

AFL 的真正优势体现在**复杂、非标准的 VRP 变体**上，特别是那些缺乏专用求解器的问题。在电动 VRP（EVRP）实际基准上，AFL（T=10000）相比蚁群优化（ACO）基线实现了 -24.45% 的间隙（Table 4），展现出处理复杂约束的独特能力。

### 3 与迭代进化方法的对比

**ReEvo**（Ye et al., 2024）采用 LLM 迭代进化启发式的方法。AFL 的多智能体流程相比标准的单次提示或备选提示策略，始终实现最低的 gap 和最高的成功率（Table 9）。关键差异在于 AFL 的验证-修正闭环机制：消融研究表明，移除 JA 和 RA 后，问题描述的准确率急剧下降，代码可靠性和解的可行性受到严重影响（Figure 3, Section 4.5）。

### 4 适用边界与局限

AFL 的适用边界和已知局限包括：

- **大规模实例的性能退化**：AFL 在 CVRPLib-XXL（最大 16k 节点）上能运行，但解质量仍不及针对该问题专门调优的先进求解器（如 POMO、LEHD）（Table 18）。
- **代码生成时间开销**：代码生成阶段需要约 30 分钟，虽然相比人类专家设计已很快，但对于实时应用可能需要进一步优化（Table 10）。
- **LLM 依赖性**：当前框架依赖 OpenAI 的 GPT-4.1，虽然对其他 LLM 有一定鲁棒性，但不同 LLM 间效果有差异（Table 16），性能可能受 LLM 能力限制。
- **问题迁移性未验证**：尽管覆盖了复杂约束，但验证集中在 VRP，能否直接迁移到其他组合优化问题有待探索。
- **算法组件单一**：当前版本仅使用单一的破坏-插入启发式，未利用进化搜索或多样化算法组件。
- **约束变更需重新生成**：框架生成的代码是针对特定问题类型，若实例约束改变需重新生成；缓存机制部分缓解但未完全消除此问题。

### 5 开放问题

- AFL 在充分研究的问题（如 CVRP）上尚未超越最先进的专用求解器，如何缩小这一差距是未来工作方向。
- 未来计划引入进化搜索来引导代码生成，可能进一步提升解质量。
- 判断智能体（JA）输出的具体内容与格式细节尚未完全公开，需进一步查阅补充材料。
- 生成智能体（GA）在子任务二中的具体提示词和格式规范有待完整披露。



## 原文 PDF

![[paperPDFs/ICLR_2026/An_Agentic_Framework_with_LLMs_for_Solving_Complex_Vehicle_Routing_Problems.pdf]]
