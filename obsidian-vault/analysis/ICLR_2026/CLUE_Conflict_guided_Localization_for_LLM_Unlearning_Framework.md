---
title: "CLUE: Conflict-guided Localization for LLM Unlearning Framework"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/CLUE_Conflict_guided_Localization_for_LLM_Unlearning_Framework.pdf
project_link: null
code_link: https://github.com/Zodiark-ch/CLUE
openreview_forum_id: jtRYvazBWv
aliases:
- CLUE
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/interpretability_and_visualization
core_operator: "通过电路发现分别构建遗忘电路和保留电路，转换为合取范式（CNF）并用SAT求解器推理解，据此将每个节点分类为保留节点、遗忘节点或冲突节点，从而允许对不同类型的节点施加差异化的微调目标。"
primary_logic: "遗忘和保留本质上具有组合逻辑特性（AND/OR门），可通过电路发现显式捕捉；电路的CNF可满足性分析能够精确区分每个节点在遗忘与保留中的因果角色，实现细粒度定位。"
claims:
- "CLUE通过提取遗忘集和保留集的电路，将其转换为CNF并求解可满足性，将节点划分为遗忘、保留和冲突三类。"
- "CLUE针对不同节点类别提供差异化的微调策略：遗忘节点仅用遗忘损失，冲突节点用遗忘和保留损失联合优化。"
- "在WMDP Cyber、WMDP Bio和PKU-SafeRLHF三个主要遗忘任务上，CLUE在遗忘效能和保留效用上均一致超越现有定位方法，且修改参数量仅为58.16%-54.88%。"
- "消融实验表明，移除遗忘掩码导致遗忘效能降幅最大（↓0.045），替换冲突掩码导致保留效用降幅最大（↓0.264）。"
---

# CLUE: Conflict-guided Localization for LLM Unlearning Framework

> [!tip] 核心洞察
> 遗忘和保留本质上具有组合逻辑特性（AND/OR门），可通过电路发现显式捕捉；电路的CNF可满足性分析能够精确区分每个节点在遗忘与保留中的因果角色，实现细粒度定位。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | CLUE：冲突导向的LLM遗忘定位框架 |
| 英文题名 | CLUE: Conflict-guided Localization for LLM Unlearning Framework |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=jtRYvazBWv) · [GitHub](https://github.com/Zodiark-ch/CLUE) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/interpretability_and_visualization |
| Method | CLUE |
| Dataset | WMDP Cyber (forget) / Winogrande (retain), WMDP Cyber (forget) / SST-2 (retain), WMDP Cyber (forget) / RTE (retain), WMDP Bio (forget) / Winogrande (retain) |

> [!tip] 效果简介
> - WMDP Cyber (forget) / Winogrande (retain) 上，Retain Utility (accuracy) 为 0.992，对比 0.860 (WAGLE)，变化 +0.132。
> - WMDP Cyber (forget) / SST-2 (retain) 上，Retain Utility (accuracy) 为 0.91，对比 0.771 (WAGLE)，变化 +0.139。
> - WMDP Cyber (forget) / RTE (retain) 上，Retain Utility (accuracy) 为 0.786，对比 0.524 (MEMIT)，变化 +0.262。

## 概要

大型语言模型（LLM）的遗忘（unlearning）任务要求在移除有害或敏感信息的同时，保持模型在非目标任务上的性能。现有定位方法通过梯度或权重归因识别出一组纠缠的“重要”节点，但无法区分其中哪些节点专门负责遗忘、哪些负责保留、哪些同时影响两者。这一粗粒度定位导致非目标技能的灾难性遗忘或目标信息擦除不彻底，构成了当前遗忘研究的核心瓶颈。

CLUE（Conflict-guided Localization for LLM Unlearning）提出了一种冲突导向的细粒度定位框架。其核心洞察在于：遗忘与保留行为本质上具有组合逻辑特性，可通过电路发现显式捕捉为AND/OR门结构；将遗忘电路和保留电路分别转换为合取范式（CNF）后，利用SAT求解器进行可满足性分析，能够精确判定每个节点的因果角色——保留节点（仅影响保留）、遗忘节点（仅影响遗忘）或冲突节点（同时影响两者）。基于这一分类，CLUE采用两阶段掩码微调策略：第一阶段仅对遗忘节点施加遗忘损失，第二阶段对冲突节点联合优化遗忘损失与保留损失，从而实现对不同类型节点的差异化干预。

在WMDP Cyber、WMDP Bio和PKU-SafeRLHF三个主要遗忘任务上，CLUE在遗忘效能和保留效用上均一致超越现有定位方法（包括MEMIT、PCGU、DEPN、WAGLE等），且修改参数量仅为54.88%–58.16%。消融实验进一步验证了节点分类的关键作用：移除遗忘掩码导致遗忘效能降幅最大（↓0.045），替换冲突掩码导致保留效用降幅最大（↓0.264）。



大型语言模型在预训练过程中不可避免地会学习到危险知识（如生物武器制造、网络攻击方法）和不良行为（如生成有害内容），这些能力在部署后可能被恶意利用。LLM遗忘（unlearning）旨在从模型中擦除特定知识或行为，同时最大限度地保留模型在非目标任务上的通用能力，其核心优化目标可形式化为：

$$\min_{\theta} \mathbb{E}_{(x,y_f)\in\mathcal{D}_f}[\mathcal{L}(y_f|x;\theta)] + \lambda \mathbb{E}_{(x,y)\in\mathcal{D}_r}[\mathcal{L}(y|x;\theta)]$$

其中 $\mathcal{D}_f$ 为遗忘集，$\mathcal{D}_r$ 为保留集，$\lambda$ 权衡遗忘效能与保留效用。

### 现有定位方法的瓶颈

为提升遗忘的精确性，近期工作开始引入**定位（localization）**策略——先识别模型中与遗忘目标相关的关键参数子集，再仅对这些参数进行干预。代表性方法包括基于梯度的 WAGLE、DEPN，基于权重归因的 PCGU，以及基于去噪电路的 MEMIT。然而，这些方法存在一个共同的**根本性瓶颈**：

> 现有定位方法只能识别出一组**纠缠的“重要”节点**，无法区分其中哪些节点专门负责遗忘目标、哪些负责保留目标、哪些同时影响两者。

这种粗粒度的定位导致两个严重后果：
- **非目标技能的灾难性遗忘**：对保留任务至关重要的节点被不加区分地修改，造成保留效用（retain utility）大幅下降。
- **目标信息擦除不彻底**：遗忘损失被分散到所有“重要”节点上，缺乏对遗忘专属节点的集中优化，导致遗忘效能（forget efficacy）不足。

### 核心洞察：遗忘与保留的组合逻辑本质

CLUE 的核心洞察在于：遗忘和保留本质上具有**组合逻辑特性**。模型中的信息流可以通过 AND/OR 门来刻画——遗忘行为对应一组逻辑门的激活模式，保留行为对应另一组。通过电路发现（circuit discovery）显式提取这两组逻辑电路，并将其转换为合取范式（CNF），再利用 SAT 求解器进行可满足性分析，就能**精确区分每个节点在遗忘与保留中的因果角色**。

具体而言，节点可被划分为三个互斥的类别：
- **保留节点**：仅对保留任务关键，修改会导致保留效用下降；
- **遗忘节点**：仅对遗忘目标关键，修改可有效擦除目标信息；
- **冲突节点**：同时影响遗忘和保留，需要差异化的联合优化。

这一细粒度分类为后续的差异化微调提供了因果依据，从根本上解决了现有方法“一刀切”式干预的缺陷。



## 核心方法与创新机理

CLUE的核心创新在于将LLM遗忘中的定位问题从“识别一组重要节点”推进到“区分每个节点的因果角色”。现有定位方法（如WAGLE、DEPN、PCGU、MEMIT）通过梯度或权重归因只能识别出一组纠缠的“重要”节点，无法区分其中哪些节点专门负责遗忘、哪些负责保留、哪些同时影响两者。这导致非目标技能的灾难性遗忘或目标信息擦除不彻底——这是当前定位驱动遗忘方法的真实瓶颈。

CLUE通过三个关键设计突破这一瓶颈：

**1. 节点分类粒度：从单一纠缠组到三个互斥类别**

现有方法将所有被定位的节点视为一个整体施加统一干预，而CLUE将节点划分为三类：遗忘节点（forget nodes）、保留节点（retain nodes）和冲突节点（conflict nodes）。这一分类不是启发式的，而是通过电路发现与SAT求解的严格逻辑推理得出——遗忘电路和保留电路被分别提取并转换为合取范式（CNF），联合求解可满足性后，每个节点被赋予确定的状态：状态为0的是遗忘节点，状态为1的是保留节点，无有效赋值的为冲突节点。这种细粒度分类使得后续微调可以对不同角色节点施加差异化目标，从根本上解决了“一刀切”干预带来的遗忘-保留冲突。

**2. 定位机制：从梯度/权重归因到逻辑电路发现+SAT推理**

CLUE的定位机制完全不同于现有方法。它首先通过加噪（noising）和去噪（denoising）两种干预分别提取遗忘集和保留集的基础电路，然后利用Edge-Pruning和逻辑电路框架将这些电路中的边分类为AND门或OR门。接着，通过Tseitin变换将AND/OR门转换为CNF子句：

$$ \begin{cases} (\neg A \lor \neg B \lor C) \land (A \lor \neg C) \land (B \lor \neg C), & \text{if } C = A \land B \\ (A \lor B \lor \neg C) \land (\neg A \lor C) \land (\neg B \lor C), & \text{if } C = A \lor B \end{cases} $$

最后，将遗忘CNF和保留CNF联合，并要求遗忘电路输出为False、保留电路输出为True，通过SAT求解器推理每个节点的赋值。这一设计的核心洞察在于：遗忘和保留本质上具有组合逻辑特性（AND/OR门），电路发现能显式捕捉这种逻辑结构，而CNF可满足性分析则能精确区分每个节点在遗忘与保留中的因果角色。

**3. 微调策略：从统一干预到两阶段掩码差异化微调**

基于节点分类结果，CLUE采用两阶段掩码微调。第一阶段仅对遗忘节点施加遗忘损失，其余参数冻结：

$$ \operatorname*{min}_{\theta_{\mathrm{f}}} \mathbb{E}_{(x, y_f) \in \mathcal{D}_f} [\mathcal{L}(y_f | x; \mathcal{M}_{\mathrm{f}} \odot \theta_{\mathrm{f}} + (1 - \mathcal{M}_{\mathrm{f}}) \odot \theta_{\mathrm{o}})] $$

第二阶段对冲突节点同时施加遗忘损失和保留损失：

$$ \operatorname*{min}_{\theta_c} \mathbb{E}_{(x, y_f) \in \mathcal{D}_f} [\mathcal{L}(y_f | x; \mathcal{M}_{\mathrm{f}} \odot \theta_c + (1 - \mathcal{M}_{\mathrm{f}}) \odot \theta_{\mathrm{o}})] + \lambda \mathbb{E}_{(x, y) \in \mathcal{D}_r} [\mathcal{L}(y | x; \mathcal{M}_{\mathrm{f}} \odot \theta_{\mathrm{c}} + (1 - \mathcal{M}_{\mathrm{f}}) \odot \theta_{\mathrm{o}})] $$

这与现有方法（如GA、NPO、PO）对所有定位节点使用单一损失组合的策略形成鲜明对比。消融实验验证了这一设计的必要性：移除遗忘掩码（$-M_f$）导致遗忘效能降幅最大（↓0.045），替换冲突掩码（$-M_c$，用全1掩码替代）导致保留效用降幅最大（↓0.264），证明遗忘节点和冲突节点的差异化处理对遗忘效能和保留效用分别起关键作用。

上述三个changed slots共同构成了CLUE相对于现有定位驱动遗忘方法的系统性改进。在WMDP Cyber、WMDP Bio和PKU-SafeRLHF三个主要遗忘任务上，CLUE在遗忘效能和保留效用上均一致超越所有现有定位方法，且修改参数量仅为54.88%–58.16%，显著低于其他方法。



![[assets/figures/papers/iclr26_0009_jtRYvazBWv_CLUE_Conflict-guided_Localization_for_LLM_Unlear/figures/002_Figure_2.jpg]]
*Figure 2: Overview from datasets to localization*

![[assets/figures/papers/iclr26_0009_jtRYvazBWv_CLUE_Conflict-guided_Localization_for_LLM_Unlear/figures/003_Figure_3.jpg]]
*Figure 3: The processing from datasets to logical circuits*

CLUE 框架将 LLM 遗忘任务重新表述为一个**冲突导向的定位问题**，其核心 pipeline 包含四个顺序模块，形成从数据到差异化微调的完整闭环。

### 输入与输出流

**输入**包含三部分：遗忘数据集 $\mathcal{D}_f$（包含不希望模型保留的样本及其期望响应 $y_f$）、保留数据集 $\mathcal{D}_r$（包含需要保持性能的样本及其原始响应 $y$），以及预训练的 LLM 模型 $\mathcal{G}$。**输出**是一个经过差异化微调的模型，其中遗忘节点的参数被定向修改以擦除目标信息，冲突节点被联合优化以平衡遗忘与保留，而保留节点保持冻结。

### 模块关系与数据流

整个 pipeline 的数据流如下：遗忘集和保留集分别进入**逻辑电路发现模块**，各自提取出对应的电路子图；两个电路随后进入**电路到 CNF 转换模块**，通过 Tseitin 变换转化为合取范式；联合 CNF 被送入**SAT 求解分类模块**，通过可满足性求解将每个节点划分为三类；最后，分类结果驱动**两阶段掩码微调模块**，对不同类别节点施加差异化优化目标。

#### 模块一：逻辑电路发现（Logical Circuit Discovery）

该模块对遗忘集和保留集分别独立运行。对于每个数据集，首先通过加噪干预（noising-based intervention）和去噪干预（denoising-based intervention）获得两个基本电路 $\mathcal{C}_{Ns}$ 和 $\mathcal{C}_{Dn}$，然后合并为逻辑完备的电路，其中的边被分类为 AND 门、OR 门或 ADDER 门。电路发现的目标是在稀疏性约束下，使子图 $\mathcal{C}$ 的输出分布逼近完整模型 $\mathcal{G}$ 的输出分布：

$$\arg\min_{\mathcal{C}} \mathbb{E}_{(x)\in\mathcal{T}}[D(p_{\mathcal{G}}(y|x)||p_{\mathcal{C}}(y|x))], \text{s.t. } 1 - |\mathcal{C}|/|\mathcal{G}| \geq s$$

其中 $D$ 为 KL 散度，$s$ 控制稀疏度。遗忘电路中的 ADDER 门在实际实现中被简化为 OR 门，保留电路中的 ADDER 门被简化为 AND 门，以保证后续转换的逻辑完备性。

#### 模块二：电路到 CNF 转换（Circuit-to-CNF Conversion）

获得遗忘电路和保留电路后，该模块利用 Tseitin 变换将 AND/OR 门转化为等价的合取范式子句。对于 AND 门 $C = A \land B$，对应子句为：

$$(\neg A \lor \neg B \lor C) \land (A \lor \neg C) \land (B \lor \neg C)$$

对于 OR 门 $C = A \lor B$，对应子句为：

$$(A \lor B \lor \neg C) \land (\neg A \lor C) \land (\neg B \lor C)$$

所有子句的合取分别构成遗忘 CNF $\Phi_{\mathrm{f}}$ 和保留 CNF $\Phi_{\mathrm{r}}$。

#### 模块三：SAT 求解节点分类（SAT-based Node Classification）

将两个 CNF 联合，并附加约束要求遗忘电路输出为 False（目标信息被移除）、保留电路输出为 True（非目标能力被保持），形成统一的 SAT 问题：

$$\Phi = \Phi_{\mathrm{f}} \wedge \Phi_{\mathrm{r}} \wedge (\neg \mathrm{output}_{\mathrm{f}}) \wedge (\mathrm{output}_{\mathrm{r}})$$

SAT 求解器对该公式进行可满足性求解。根据求解结果，节点被分为三类：
- **保留节点**：在所有满足赋值中状态为 1 的节点，专门负责保留能力；
- **遗忘节点**：在所有满足赋值中状态为 0 的节点，专门负责遗忘目标；
- **冲突节点**：不存在有效赋值的节点，即同时参与遗忘和保留电路且无法被单一状态满足的节点。

这一分类粒度是 CLUE 与现有方法的根本差异——现有定位方法（如 WAGLE、DEPN、PCGU）仅能识别一组纠缠的“重要”节点，无法区分子集的功能角色。

#### 模块四：两阶段掩码微调（Two-Stage Masked Fine-Tuning）

基于节点分类结果生成两个二值掩码：遗忘掩码 $\mathcal{M}_{\mathrm{f}}$ 在遗忘节点位置置 1，冲突掩码 $\mathcal{M}_{\mathrm{c}}$ 在冲突节点位置置 1。

**第一阶段**仅对遗忘节点进行微调，使用纯遗忘损失：

$$\operatorname*{min}_{\theta_{\mathrm{f}}} \mathbb{E}_{(x, y_f) \in \mathcal{D}_f} [\mathcal{L}(y_f | x; \mathcal{M}_{\mathrm{f}} \odot \theta_{\mathrm{f}} + (1 - \mathcal{M}_{\mathrm{f}}) \odot \theta_{\mathrm{o}})]$$

**第二阶段**对冲突节点进行微调，联合优化遗忘损失和保留损失：

$$\operatorname*{min}_{\theta_c} \mathbb{E}_{(x, y_f) \in \mathcal{D}_f} [\mathcal{L}(y_f | x; \mathcal{M}_{\mathrm{f}} \odot \theta_c + (1 - \mathcal{M}_{\mathrm{f}}) \odot \theta_{\mathrm{o}})] + \lambda \mathbb{E}_{(x, y) \in \mathcal{D}_r} [\mathcal{L}(y | x; \mathcal{M}_{\mathrm{f}} \odot \theta_{\mathrm{c}} + (1 - \mathcal{M}_{\mathrm{f}}) \odot \theta_{\mathrm{o}})]$$

默认微调方法为 PO+PO（两阶段均使用 Preference Optimization），其余参数在相应阶段保持冻结。这种差异化策略使得遗忘节点被定向擦除，冲突节点在遗忘与保留之间寻求平衡，而保留节点完全不参与微调，从根本上避免了非目标技能的灾难性遗忘。

### 关键设计逻辑

框架的核心洞察在于：遗忘和保留本质上具有**组合逻辑特性**（AND/OR 门），通过电路发现可以显式捕捉这种结构；而电路的 CNF 可满足性分析能够精确区分每个节点在遗忘与保留中的因果角色，实现细粒度定位。消融实验证实了这一设计的有效性——移除遗忘掩码（$-M_f$）导致遗忘效能降幅最大（↓0.045），替换冲突掩码（$-M_c$，用全 1 掩码替代）导致保留效用降幅最大（↓0.264），表明节点分类和差异化微调对最终性能至关重要。



CLUE 的核心流水线由四个模块构成：逻辑电路发现、电路到 CNF 的转换、基于 SAT 的节点分类，以及两阶段掩码微调。以下逐一阐述其机理与关键公式。

### 逻辑电路发现

CLUE 首先从遗忘集 $\mathcal{D}_f$ 和保留集 $\mathcal{D}_r$ 中分别提取逻辑电路。电路发现的目标是寻找一个稀疏子图 $\mathcal{C}$，使其在目标数据集 $\mathcal{T}$ 上的输出分布尽可能逼近完整模型 $\mathcal{G}$：

$$
\arg\min_{\mathcal{C}} \mathbb{E}_{(x)\in\mathcal{T}}[D(p_{\mathcal{G}}(y|x)||p_{\mathcal{C}}(y|x))], \text{ s.t. } 1 - |\mathcal{C}|/|\mathcal{G}| \geq s
$$

其中 $D$ 为分布距离度量，$s$ 为稀疏性约束。为获取逻辑完备的门类型（AND、OR、ADDER），CLUE 采用加噪干预和去噪干预的联合策略：加噪干预揭示哪些边对维持正确输出不可或缺，去噪干预揭示哪些边足以从噪声输入中恢复正确输出。二者联合使用可恢复逻辑完备的门集合。

### 电路到 CNF 的转换

提取的电路包含 AND 门、OR 门和 ADDER 门。在实际实现中，遗忘电路中的 ADDER 门被简化为 OR 门，保留电路中的 ADDER 门被简化为 AND 门，随后利用 Tseitin 变换将电路转换为合取范式（CNF）。对于 AND 门 $C = A \land B$ 和 OR 门 $C = A \lor B$，Tseitin 变换产生以下子句：

$$
\begin{cases}
(\neg A \lor \neg B \lor C) \land (A \lor \neg C) \land (B \lor \neg C), & \text{if } C = A \land B \\
(A \lor B \lor \neg C) \land (\neg A \lor C) \land (\neg B \lor C), & \text{if } C = A \lor B
\end{cases}
$$

该变换在多项式时间内保留了原电路的可满足性，为后续 SAT 求解提供了标准化的逻辑表达。

### 基于 SAT 的节点分类

分别获得遗忘电路和保留电路的 CNF 后，CLUE 将其联合为一个可满足性问题：

$$
\Phi = \Phi_{\mathrm{f}} \wedge \Phi_{\mathrm{r}} \wedge (\neg \mathrm{output}_{\mathrm{f}}) \wedge (\mathrm{output}_{\mathrm{r}})
$$

其中 $\Phi_{\mathrm{f}}$ 和 $\Phi_{\mathrm{r}}$ 分别为遗忘电路和保留电路的 CNF，约束 $\neg \mathrm{output}_{\mathrm{f}}$ 要求遗忘电路输出为 False（即遗忘目标信息被移除），约束 $\mathrm{output}_{\mathrm{r}}$ 要求保留电路输出为 True（即保留能力被维持）。通过 SAT 求解器对 $\Phi$ 求解：

- **保留节点**：在所有可满足赋值中状态恒为 1 的节点，其激活对保留任务必要；
- **遗忘节点**：在所有可满足赋值中状态恒为 0 的节点，其抑制对遗忘任务必要；
- **冲突节点**：不存在有效赋值的节点，即遗忘需求和保留需求在该节点上产生逻辑冲突。

这一分类机制是 CLUE 区别于现有定位方法的核心——现有方法仅能识别一组纠缠的“重要”节点，而 CLUE 通过组合逻辑分析将节点精确划分为三个互斥类别。

### 两阶段掩码微调

基于节点分类结果，CLUE 生成两个二值掩码：遗忘掩码 $\mathcal{M}_{\mathrm{f}}$（遗忘节点对应元素为 1，其余为 0）和冲突掩码 $\mathcal{M}_{\mathrm{c}}$（冲突节点对应元素为 1，其余为 0）。微调分两阶段进行。

**第一阶段**：仅对遗忘节点进行微调，使用遗忘损失，其余参数冻结：

$$
\operatorname*{min}_{\theta_{\mathrm{f}}} \mathbb{E}_{(x, y_f) \in \mathcal{D}_f} [\mathcal{L}(y_f | x; \mathcal{M}_{\mathrm{f}} \odot \theta_{\mathrm{f}} + (1 - \mathcal{M}_{\mathrm{f}}) \odot \theta_{\mathrm{o}})]
$$

其中 $\theta_{\mathrm{o}}$ 为原始模型参数，$\odot$ 表示逐元素乘法。该阶段仅关注信息擦除，不受保留约束干扰。

**第二阶段**：对冲突节点进行微调，同时优化遗忘损失和保留损失：

$$
\operatorname*{min}_{\theta_c} \mathbb{E}_{(x, y_f) \in \mathcal{D}_f} [\mathcal{L}(y_f | x; \mathcal{M}_{\mathrm{f}} \odot \theta_c + (1 - \mathcal{M}_{\mathrm{f}}) \odot \theta_{\mathrm{o}})] + \lambda \mathbb{E}_{(x, y) \in \mathcal{D}_r} [\mathcal{L}(y | x; \mathcal{M}_{\mathrm{f}} \odot \theta_c + (1 - \mathcal{M}_{\mathrm{f}}) \odot \theta_{\mathrm{o}})]
$$

其中 $\lambda$ 为保留损失权重。由于冲突节点同时涉及遗忘和保留功能，该阶段通过联合优化在二者之间寻求平衡。消融实验（Table 2）证实：移除遗忘掩码导致遗忘效能降幅最大（↓0.045），替换冲突掩码导致保留效用降幅最大（↓0.264），验证了差异化微调策略的必要性。



## 实验与关键发现

### 主实验结果

CLUE在三个主流遗忘基准（WMDP Cyber、WMDP Bio、PKU-SafeRLHF）上对遗忘效能（FE）、保留效用（RU）和通用效用（GU）进行了全面评估，并与GA、NPO、PO等微调方法及MEMIT、PCGU、DEPN、WAGLE等定位驱动方法进行了对比。核心结果汇总于Table 1。


![[assets/figures/papers/iclr26_0009_jtRYvazBWv_CLUE_Conflict-guided_Localization_for_LLM_Unlear/figures/004_Table_1.jpg]]
*Table 1: Performance overview of LLM unlearning. “Unlearned Parameter” refers to the percentage of parameters modified, calculated by averaging the percentage of changes in each parameter matrix. “FE” (Forget efficacy) is measured as 1-accuracy and “RU” (Retain utility) is measured as accuracy on the test set of the retain set. “GU” (General utility) is average accuracy on a series of non-target tasks, and specific results can be found in Appendix G*

**遗忘效能与保留效用的双重优势。** 在WMDP Cyber遗忘任务上，CLUE以Winogrande为保留集时保留效用达到0.992，较最强定位基线WAGLE（0.860）提升+0.132；以SST-2为保留集时保留效用为0.91，较WAGLE（0.771）提升+0.139；以RTE为保留集时保留效用为0.786，较MEMIT（0.524）提升+0.262。在WMDP Bio遗忘任务上，CLUE以Winogrande为保留集时保留效用为0.995，较WAGLE（0.885）提升+0.110。在PKU-SafeRLHF遗忘任务上，CLUE以Winogrande为保留集时保留效用为0.956，较WAGLE（0.751）提升+0.205。以上结果表明，CLUE在各类遗忘场景下均能显著降低非目标技能的灾难性遗忘。

**参数修改量的压缩。** CLUE修改参数量仅为58.16%–54.88%，在所有定位方法中最低。相比之下，WAGLE修改参数量为78.71%–71.27%，MEMIT为99.99%。CLUE通过精确区分遗忘节点、保留节点和冲突节点，仅对遗忘节点和冲突节点施加差异化微调，实现了更稀疏且更有效的参数干预。

**通用效用保持。** CLUE在多个非目标任务上的通用效用同样具有竞争力。以WMDP Cyber为遗忘集、SST-2为保留集时，CLUE的通用效用为0.388，显著优于WAGLE（0.217）和MEMIT（0.105）。具体非目标任务上的详细准确率见Table 5。

### 消融实验

为验证CLUE各组件的因果贡献，在WMDP Cyber遗忘集和SST-2保留集上进行了消融实验，结果见Table 2。


![[assets/figures/papers/iclr26_0009_jtRYvazBWv_CLUE_Conflict-guided_Localization_for_LLM_Unlear/figures/005_Table_2.jpg]]
*Table 2: Ablation with WMDP Cyber as forget set and SST-2 as retain set*

**遗忘掩码（M_f）的关键作用。** 移除遗忘掩码（-M_f）导致遗忘效能降幅最大，FE从0.733降至0.688（↓0.045）。这证实了遗忘节点在擦除目标信息中的核心地位——仅通过电路发现定位到遗忘节点并对其施加遗忘损失，是实现高效遗忘的瓶颈所在。

**冲突掩码（M_c）的不可替代性。** 将冲突掩码替换为全1掩码（-M_c），即对冲突节点施加无差别的全局微调，导致保留效用从0.91骤降至0.646（↓0.264）。这表明冲突节点同时承载遗忘和保留功能，必须通过联合优化遗忘损失和保留损失来平衡两者，否则将引发严重的灾难性遗忘。

**微调策略的选择敏感性。** 将CLUE默认的PO+PO策略替换为GA+GA时，保留效用从0.91暴跌至0.381（↓0.529），遗忘效能也从0.733降至0.575（↓0.158）。这说明GA不适合CLUE的定位框架，PO在平衡遗忘和保留目标方面具有更好的适应性。

### 电路稀疏性与遗忘效能的关系

Figure 5揭示了电路稀疏性、忠实度和遗忘效能之间的权衡关系。随着电路稀疏性增加（$|\mathcal{C}|/|\mathcal{G}|$减小），电路忠实度（KL散度）呈上升趋势，表明过于稀疏的电路难以准确捕获模型行为。遗忘效能则在中等稀疏性区间达到最优，过稀疏或过稠密的电路均导致遗忘效能下降。这一发现说明，CLUE的电路发现需要在稀疏性和忠实度之间找到平衡点，过低稀疏性会引入噪声节点，过高稀疏性则会遗漏关键节点。


![[assets/figures/papers/iclr26_0009_jtRYvazBWv_CLUE_Conflict-guided_Localization_for_LLM_Unlear/figures/011_Figure_5.jpg]]
*Figure 5: Circuit Sparsity vs. Circuit Faithfulness and Forget Efficacy*

### 遗忘比例鲁棒性

Figure 7展示了在不同遗忘比例下CLUE与其他方法的对比。随着遗忘集比例从10%增至100%，CLUE在遗忘效能、保留效用和通用效用三个维度上均保持对WAGLE、MEMIT等方法的稳定优势。尤其在低遗忘比例场景下，CLUE的保留效用优势更加显著，表明其细粒度节点分类策略在面对有限遗忘数据时仍能有效保护非目标能力。

### 节点分布分析

Table 3统计了遗忘前后遗忘节点和冲突节点的数量变化。遗忘后，遗忘节点比例普遍增加，冲突节点比例相应减少，说明微调过程成功将部分冲突节点转化为遗忘节点，从而增强了遗忘效果。Figure 8对比了CLUE、MEMIT和WAGLE在Zephyr-7B-beta模型上的节点分布：MEMIT几乎不包含遗忘节点，WAGLE无法区分遗忘节点和冲突节点，而CLUE能够清晰分离三类节点，验证了其细粒度定位的有效性。

### 失败模式与局限

尽管CLUE在主流基准上表现优异，仍存在以下已知失败模式：

1. **多保留集冲突复杂性。** 当保留集为MMLU等大规模多任务数据集时，Figure 4显示遗忘效能随保留任务数量增加而下降。当保留任务数达到7个时，通用效用才超越MMLU基线，表明面对多个保留集时冲突组合的复杂性急剧增加，当前方案缺乏统一的处理框架。


![[assets/figures/papers/iclr26_0009_jtRYvazBWv_CLUE_Conflict-guided_Localization_for_LLM_Unlear/figures/009_Figure_4.jpg]]
*Figure 4: Performance of CLUE when retain set is MMLU dataset and multiple specific tasks. (a) WMDP Cyber*

2. **低稀疏性电路的性能退化。** Figure 5显示，当电路稀疏性过低时，遗忘效能和保留效用均出现下降，说明CLUE的有效性依赖于能够提取到清晰且稀疏的电路。对于无法提取清晰电路的遗忘数据集（如细粒度常识），CLUE的性能可能显著下降。

3. **计算开销。** Table 7和Table 8对比了各方法的计算成本。CLUE的电路发现和SAT求解阶段引入了额外开销，尽管采用EAP优化后总时间可降至3.21小时（WMDP Cyber），仍高于纯微调方法GA（2.33小时）。在更大规模语言模型上，电路发现的可扩展性问题可能进一步加剧。

**注意：** 以上失败模式的分析部分基于论文声明的局限性，具体数值和边界条件需在实际部署中进一步验证。


## 定位与知识库关联

### 与现有工作的关系

CLUE 在 LLM 遗忘领域处于“定位驱动微调”这一技术路线上，但其核心突破在于将定位粒度从单一纠缠节点集推进到三类互斥节点（保留节点、遗忘节点、冲突节点）的细粒度划分。现有定位方法——无论是基于梯度的 WAGLE 和 DEPN，基于权重归因的 PCGU，还是仅使用去噪电路的 MEMIT——本质上都只能识别一组“重要”节点，无法区分这些节点在遗忘和保留任务中分别扮演什么因果角色。这导致两个典型失败模式：要么擦除目标信息不彻底（遗忘效能不足），要么非目标技能发生灾难性遗忘（保留效用骤降）。

CLUE 通过引入逻辑电路发现和 SAT 求解，从根本上改变了这一局面。其关键差异体现在三个维度：

1. **定位机制**：从连续梯度/权重信号转向离散逻辑电路的可满足性分析。CLUE 分别对遗忘集和保留集提取电路，经 Tseitin 变换转为合取范式（CNF），再通过 SAT 求解器判定每个节点在“遗忘电路输出为假、保留电路输出为真”这一联合约束下的赋值状态。这一过程将定位问题转化为组合逻辑推理，从而精确区分三类节点。
2. **分类粒度**：输出不再是单一掩码，而是遗忘掩码 $\mathcal{M}_\mathrm{f}$ 和冲突掩码 $\mathcal{M}_\mathrm{c}$ 的二元组，分别标记仅需遗忘的节点和需要在遗忘与保留之间平衡的节点。
3. **微调策略**：针对不同类别实施差异化监督——遗忘节点仅用遗忘损失优化，冲突节点则联合遗忘损失和保留损失进行约束，而保留节点完全冻结。这种策略避免了现有方法中对所有“重要”节点施加统一损失组合带来的冲突。

实验证据一致支持上述区分。Table 1 显示，CLUE 在 WMDP Cyber、WMDP Bio 和 PKU-SafeRLHF 三个遗忘任务上，遗忘效能（FE）、保留效用（RU）和通用效用（GU）均一致超越 MEMIT、PCGU、DEPN、WAGLE 等定位方法，且修改参数量仅为 54.88%–58.16%，远低于对比方法。Table 2 的消融实验进一步验证了分类的必要性：移除遗忘掩码（-$\mathcal{M}_\mathrm{f}$）导致遗忘效能降幅最大（↓0.045），而将冲突掩码替换为全 1 掩码（-$\mathcal{M}_\mathrm{c}$）导致保留效用降幅最大（↓0.264）。这表明遗忘节点和冲突节点的功能不可互换，统一处理必然损害某一侧性能。

### 适用边界

CLUE 的有效性依赖于两个前提条件，偏离这些条件时性能可能退化：

1. **可提取电路的数据集**：CLUE 要求遗忘集和保留集都能通过 noising + denoising 干预提取出具有足够保真度的逻辑电路。当遗忘数据涉及细粒度常识或模糊语义边界，无法形成清晰的 AND/OR 门结构时，电路发现的质量下降，进而影响节点分类的准确性。论文明确将“无法提取清晰电路的遗忘数据集”列为开放问题。
2. **电路稀疏性-保真度权衡**：Figure 5 揭示了电路稀疏性 $|\mathcal{C}|/|\mathcal{G}|$ 与保真度（KL 散度）及遗忘效能之间的权衡关系。当稀疏性过低（电路过大），冲突节点比例上升，微调时遗忘与保留的张力加剧；当稀疏性过高，电路保真度下降，定位精度受损。这一权衡决定了 CLUE 在实际部署中需要针对具体任务调优稀疏性阈值 $s$。
3. **保留集数量与组合复杂性**：当保留集从单一任务（如 SST-2）扩展到 MMLU 等多任务集合时，Figure 4 显示遗忘效能随特定保留任务数量增加而下降。这是因为每增加一个保留集，冲突组合的复杂性急剧增加，当前 CNF 联合求解和两阶段微调尚无法为所有冲突组合提供针对性方案。论文将此列为开放问题。
4. **模型规模与计算开销**：电路发现涉及对模型中每条边的干预评估，其计算复杂度与模型规模正相关。Table 7 和 Table 8 给出了 WMDP Cyber 和 WMDP Bio 上的计算成本对比，CLUE 的定位阶段开销高于基于梯度的 WAGLE 和 DEPN。论文明确指出现有电路发现算法在超大规模语言模型上的可扩展性是待解决问题。

### 局限与开放问题

**已识别的局限**：

- **电路发现的静态性**：CLUE 在微调前完成节点分类，但微调过程本身会改变节点的功能角色。Table 3 显示遗忘节点和冲突节点数量在遗忘前后发生变化，说明电路是动态的。当前框架无法在微调过程中更新电路以反映关键节点的变化。
- **多保留集的组合爆炸**：当存在多个保留集时，每两个集合之间都可能产生新的冲突组合。现有 CNF 联合求解将所有保留集统一处理，无法为每种冲突组合提供差异化的微调方案。
- **完美平衡的不可达性**：尤其在低稀疏性电路中，冲突节点比例较高，微调过程可能无法在遗忘和保留之间达到完美平衡。Table 2 中 GA+GA 组合导致保留效用巨幅下降（↓0.529）即表明，即使区分了节点类别，微调方法的选择仍对最终平衡有决定性影响。
- **细粒度遗忘数据的电路缺失**：当遗忘数据集无法提取清晰电路时，CLUE 的整个定位管道失效，需要完全不同的方法。

**开放问题**：

1. 如何在微调过程中动态更新电路，使节点分类反映模型参数的实时变化？
2. 面对多个保留集时，如何为每一种可能的冲突组合提供针对性的微调或编辑方案？
3. 除微调外，能否发展针对冲突组合的模型编辑方法，实现更精确的局部干预？
4. 如何处理无法提取清晰电路的遗忘数据集（如细粒度常识、模糊语义边界）？
5. 如何解决电路发现在超大规模语言模型中的可扩展性问题，使其适用于百亿、千亿参数级别的模型？

需要指出的是，上述部分局限和开放问题来自论文自身的讨论，其解决方案尚未在本文中给出，读者在将 CLUE 应用于新场景时应自行评估这些边界条件的影响。



## 原文 PDF

![[paperPDFs/ICLR_2026/CLUE_Conflict_guided_Localization_for_LLM_Unlearning_Framework.pdf]]
