---
title: "RAIN-Merging: A Gradient-Free Method to Enhance Instruction Following in Large Reasoning Models with Preserved Thinking Format"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RAIN_Merging_A_Gradient_Free_Method_to_Enhance_Instruction_Following_in_Large_Reasoning_Models_with_Preserved_Thinking_Format.pdf
openreview_forum_id: PO2iULmu5e
aliases:
- RAIN-Merging
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "通过将ITM任务向量投影到思考标记前向特征零空间来保持思考格式不变，同时利用指令注意力引导的模块级别缩放系数来选择性增强指令遵循，两者构成RAIN-Merging的两阶段调控机制。"
primary_logic: "推理与指令遵循两个任务的任务向量在参数主方向几乎正交，暗示可进行轻量合并，但直接合并会因输出格式差异导致思考段分布偏移。通过在思考标记处施加零空间投影，可消除对思考格式的一阶扰动，再利用指令注意力指标指导模块缩放，无需梯度即可实现指令遵循增强与推理性能保持。"
claims:
- "LRM与ITM任务向量在主要模块的主子空间余弦相似度均低于0.1，说明两种能力参数空间几乎正交。"
- "RAIN-Merging在指令遵循和推理&通用能力平均分上全面超越所有基线合并方法（IF平均48.11，R平均55.59），且仅需约21分钟合并时间。"
- "零空间投影使思考标记KL散度降至0.0065，缺失</think>比例降为0%，有效保护思考格式。"
- "两阶段消融实验表明，同时使用零空间投影和指令注意力引导系数可取得最佳指令遵循与推理权衡。"
---

# RAIN-Merging: A Gradient-Free Method to Enhance Instruction Following in Large Reasoning Models with Preserved Thinking Format

> [!tip] 核心洞察
> 推理与指令遵循两个任务的任务向量在参数主方向几乎正交，暗示可进行轻量合并，但直接合并会因输出格式差异导致思考段分布偏移。通过在思考标记处施加零空间投影，可消除对思考格式的一阶扰动，再利用指令注意力指标指导模块缩放，无需梯度即可实现指令遵循增强与推理性能保持。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | RAIN-Merging：一种无需梯度的增强大型推理模型指令遵循并保留思考格式的方法 |
| 英文题名 | RAIN-Merging: A Gradient-Free Method to Enhance Instruction Following in Large Reasoning Models with Preserved Thinking Format |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=PO2iULmu5e); [GitHub](https://github.com/K1nght/RAIN-Merging) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | RAIN-Merging |
| Dataset | IFEval (strict accuracy), Math (average over six benchmarks), Instruction Following Average (IFEval, CELLO, InfoBench, ComplexBench), Reasoning & General Average (Math, GPQA, Aider, Arena-Hard-v2) |

> [!tip] 效果简介
> - IFEval (strict accuracy) 上，Accuracy (%) 为 63.22，对比 55.45 (LRM)，变化 +7.77。
> - Math (average over six benchmarks) 上，Accuracy (%) 为 68.75，对比 64.75 (LRM)，变化 +4.00。
> - Instruction Following Average (IFEval, CELLO, InfoBench, ComplexBench) 上，Avg. Accuracy 为 48.11，对比 44.12 (LRM)，变化 +3.99。

## 概述

**问题瓶颈**：大型推理模型（LRM）在数学、代码等复杂推理任务上表现优异，但其指令遵循能力薄弱。一个关键的结构性冲突在于：LRM 的输出包含显式的 `<think>...</think>` 思考段，而指令微调模型（ITM）仅输出最终答案。若直接对两者进行参数合并，会破坏 LRM 的思考格式，进而损害推理能力。参数空间分析表明，LRM 与 ITM 的任务向量在各子模块的主子空间余弦相似度均低于 0.1，说明两种能力的参数主方向近乎正交——这为轻量合并提供了可能，但输出格式差异仍构成核心障碍。

**核心调控机制**：RAIN-Merging 通过两阶段梯度自由设计解决上述冲突。第一阶段，将 ITM 任务向量投影到由思考标记前向特征构建的零空间，确保在 `<think>` 段内前向特征不变，从而保护思考格式；第二阶段，利用指令注意力对齐度与泄漏度指标，对每个注意力头和 FFN 层求解带约束的二次规划，得到模块级别的差异化缩放系数，选择性增强指令遵循信号。

**主要结果**：在 Qwen2.5-7B-Instruct 与 DeepSeek-R1-Distill-Qwen-7B 的合并实验中，RAIN-Merging 在指令遵循平均分（48.11）和推理与通用能力平均分（55.59）上全面超越所有基线合并方法，相比原始 LRM 分别提升 +3.99 和 +4.56 个百分点；IFEval 严格准确率达 63.22%（+7.77），数学平均准确率达 68.75%（+4.00）。零空间投影使思考标记 KL 散度降至 0.0065，`</think>` 缺失比例降为 0%。该方法仅需约 21 分钟合并时间，且在 1.5B 至 32B 多尺度模型及 Llama 架构上均表现出一致的增益。

**方法定位**：RAIN-Merging 属于无训练合并方法，仅需少量校准数据（150 条推理样本 + 365 条指令样本）用于构建零空间和计算注意力指标，无需梯度更新。其核心贡献在于将输出格式保护显式编码为参数子空间约束，并以注意力信号引导模块级合并强度，为推理与指令遵循能力的协同增强提供了新的调控范式。

## 背景与动机

大型推理模型（LRM）通过显式的链式思考（Chain-of-Thought）机制在数学、编程等复杂推理任务上取得了显著进展，但其指令遵循能力相对薄弱。以 **DeepSeek-R1-Distill-Qwen-7B** 为代表的 LRM 在输出中具有明确的 `<think>...</think>` 思考段，而指令微调模型（ITM，如 **Qwen2.5-7B-Instruct**）仅输出最终答案，两者在输出格式上存在根本性差异。

模型合并（Model Merging）作为一种无需训练即可融合不同模型能力的技术，为增强 LRM 的指令遵循提供了轻量级路径。然而，直接合并面临两个核心瓶颈：

1. **思考格式破坏**：将 ITM 的任务向量直接加性合并到 LRM 上，会导致思考段内的输出分布发生显著偏移。实验表明，简单合并后思考标记处的 KL 散度急剧增大，且生成中缺失 `</think>` 闭合标记的比例大幅上升，严重损害了 LRM 的结构化推理机制。

2. **能力权衡困难**：统一的全局缩放系数无法区分不同模块对推理与指令遵循的敏感性差异。尽管分析发现 LRM 与 ITM 的任务向量在各模块的主子空间余弦相似度均低于 0.1（图 2），表明两种能力在参数空间中近乎正交，暗示合并具有可行性，但缺乏精细的模块级调控机制使得指令遵循增强与推理保持难以兼得。

现有合并方法——包括无数据的 **Task Arithmetic**（Ilharco et al., 2023）、**TIES**、**DARE-TIES**，以及数据依赖的 **ACM-TIES**、**LEWIS-TIES**、**AIM-TIES**——均未针对 LRM 特有的思考格式约束设计保护机制，导致合并后模型在指令遵循基准上的提升以牺牲推理性能为代价，或在推理保持上表现不佳。

上述缺口驱动了 **RAIN-Merging** 的提出：一种无需梯度的两阶段合并方法，核心动机在于**在保持思考格式不变的前提下，选择性增强指令遵循能力**。

## 核心创新

RAIN-Merging的核心创新在于一种**双阶段、无梯度的模型合并机制**，专门解决大型推理模型（LRM）在增强指令遵循能力时面临的**思考格式破坏**与**推理能力退化**两大瓶颈。其关键洞察是：推理与指令遵循两个任务的任务向量在参数空间近乎正交（主子空间余弦相似度低于0.1，Fig. 2），理论上可进行轻量合并，但直接合并会因输出格式差异（LRM具有`<think>...</think>`思考段，而指令微调模型ITM仅输出最终答案）导致思考段分布偏移。

围绕这一瓶颈，RAIN-Merging引入了三个核心changed slots：

### 1. 任务向量零空间投影（Stage 1）
**基线做法**：将ITM任务向量$\Delta_I$直接以全局统一标量$\lambda$加性合并到LRM参数上，不区分思考段与回答段。

**RAIN-Merging做法**：对每个子模块$k$，将ITM任务向量$\Delta_I^k$投影到由思考特殊标记前向特征构建的**零空间**中，得到$\Delta_I^{\perp,k}$（Eq. 5）。具体而言，先通过推理校准集（150个来自Mixture-of-Thoughts的样本）提取思考标记位置，构建前向特征算子$\Phi_{\Omega_{\text{think}}}^k$（Eq. 1），再计算最小二乘正交投影矩阵$P^\perp$（Eq. 4），确保投影后的任务向量满足$\Phi_{\Omega_{\text{think}}} \text{vec}(\Delta_I^\perp) = 0$，即**在思考标记处的前向特征一阶不变**。

**核心机制**：该投影操作将原始带约束优化目标（Eq. 3，在最大化指令跟随代理目标的同时约束思考格式KL散度$\mathcal{L}_{\text{think}} \leq \delta$）**近似解耦**为无约束优化问题。其理论保证来自softmax KL散度的二阶上界（$\frac{1}{8}\|u\|_2^2 + O(\|u\|_2^3)$），零空间投影使思考标记输出logits的扰动$u$为零，从而将KL散度压制在极小范围。

**证据强度**：实验证明，零空间投影使$\mathcal{L}_{\text{think}}$降至0.0065，缺失`</think>`比例降为0%（Fig. 5），有效保护了思考格式。

### 2. 指令注意力引导的模块级缩放系数（Stage 2）
**基线做法**：全局统一标量$\lambda$（如Task Arithmetic）或基于参数统计的固定缩放（如TIES的符号一致性与幅度截断），对所有模块施加相同的合并强度。

**RAIN-Merging做法**：根据**指令注意力对齐度$a^{\tilde{k}}$**（Eq. 9）与**泄漏度$u^{\tilde{k}}$**（Eq. 10）计算每模块的差异化缩放系数$\alpha_\star^{\tilde{k}}$。具体流程为：
1. 在指令校准集（365条经LLM-as-Judge筛选的IFEval蒸馏样本）上，提取每个注意力头对指令约束范围$\mathcal{T}(x)$的对齐注意力，以及对无关注区域$\mathcal{U}(x)$的泄漏注意力；
2. 构建指令注意力代理目标$\mathcal{I}_I^{\text{Proxy}}(\tilde{\alpha}) = \bar{a}(\tilde{\alpha}) - \rho \bar{u}(\tilde{\alpha})$（Eq. 11），在初始合并点$\tilde{\alpha}_{(0)}$处做二阶泰勒展开，用前向注意力统计线性近似梯度$g^{\tilde{k}}$（Eq. 14）和对角Hessian近似$\tilde{H}^{\tilde{k}}$（Eq. 15）；
3. 求解带盒约束的凸二次规划闭式解$\tilde{\alpha}_\star^{\tilde{k}} = \text{clip}_{[\tilde{\alpha}_l, \tilde{\alpha}_u]}(g^{\tilde{k}} / \tilde{H}^{\tilde{k}})$（Eq. 15），对高对齐低泄漏的模块赋予较大系数，反之抑制。

**核心机制**：该设计实现了**模块级别的选择性指令增强**——对注意力输出敏感的Q、K、V、O及FFN模块进行差异化缩放，避免全局统一系数带来的“平均化”效应。对角Hessian近似中的泄漏项$u^{\tilde{k}}$起到正则化作用，惩罚注意力发散。

**证据强度**：分层指令注意力得分对比（Fig. 6）显示，RAIN-Merging在各层均优于LRM和Task Arithmetic；消融实验（Table 4）表明，同时启用Stage 1和Stage 2使指令遵循平均分从46.75（仅Stage 2）提升至48.11，推理平均分从54.22（仅Stage 1）提升至55.59，证实两阶段互补。

### 3. 合并模块范围的精准限定
**基线做法**：部分合并方法可能涉及所有线性层。

**RAIN-Merging做法**：仅合并对注意力输出敏感的Q、K、V、O及FFN模块，避免对推理核心通路的非必要扰动。

**核心机制**：通过限定合并范围，将参数更新的影响集中在与指令理解直接相关的注意力机制和前馈变换上，减少对底层表征和位置编码等基础能力的干扰。

### 整体调控机制
最终合并模型由三要素组装（Eq. 16）：
$$\theta_\star = \theta_R + \lambda \bigoplus_{k=1}^{K} \alpha_\star^k \Delta_I^{\perp,k}$$

其中$\theta_R$为推理模型锚点，$\lambda$为全局标量（消融显示$\lambda \approx 1.0$最优，Fig. A4），$\alpha_\star^k$为模块级缩放系数，$\Delta_I^{\perp,k}$为零空间投影后的任务向量。三者在约21分钟内完成全部计算，无需任何梯度反传。

**方法定位**：RAIN-Merging属于**数据依赖的模型合并**方法，与Task Arithmetic（Ilharco et al., 2023）、TIES、DARE-TIES等无数据方法以及ACM-TIES、LEWIS-TIES、AIM-TIES等数据依赖方法形成对比。其独特之处在于首次将**思考格式的结构约束**显式建模为参数空间的零空间投影，并结合**指令注意力代理指标**实现模块级自适应合并。

## 整体框架

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_PO2iULmu5e/figures/001_Figure_1.jpg]]
*Figure 1: An overview of RAIN-Merging. In the case, the LRM arrives at the correct solution but ignores the required format and specific code. To preserve the reasoning structure, we perform training-free merging by combining a task vector projected onto the null space of the thinking format with instruction-attention guided coefficients. The merged model remains correct while satisfying the specified constraints. See Sec. 3 for details*

RAIN-Merging 是一种无需梯度的两阶段模型合并方法，其核心目标是将指令微调模型（ITM）的指令遵循能力注入大型推理模型（LRM），同时严格保护 LRM 原有的 `<think>...</think>` 思考格式和推理能力。图 1 展示了整体流程：给定一个能正确求解但忽略格式约束的 LRM，RAIN-Merging 通过零空间投影的任务向量与指令注意力引导的模块缩放系数相结合，生成一个既能保持推理结构又能满足指令约束的合并模型。

该方法建立在两个关键观察之上：
- **参数正交性**：LRM 与 ITM 的任务向量在主要模块的主子空间余弦相似度均低于 0.1（Fig. 2），表明推理能力与指令遵循能力的参数主方向近乎正交，为轻量合并提供了可行性前提。
- **输出格式冲突**：直接合并会因 ITM 无思考段输出格式而导致 LRM 的 `<think>` 段分布偏移，破坏推理结构。

为应对这一瓶颈，RAIN-Merging 将整体优化目标形式化为一个约束优化问题：在思考特殊标记段的 KL 散度不超过阈值 $\delta$ 的前提下，最大化指令遵循代理目标（Eq. 3）。两阶段管道（Fig. 3）分别解耦这两个约束：

1. **Stage 1：推理感知的零空间投影**。从 Mixture-of-Thoughts 数据集采样 150 个具有思考格式的样本构建推理校准集，提取每个子模块在 `<think>` 段的前向特征，构造前向特征算子 $\Phi_{\Omega_{\mathrm{think}}}^{k}$（Eq. 1）。对每个子模块的 ITM 任务向量 $\Delta_I^k$，通过最小二乘正交投影矩阵 $P^{\perp}$（Eq. 4）将其映射到前向特征零空间，得到 $\Delta_I^{\perp,k}$（Eq. 5）。该投影保证在思考标记处的一阶前向特征扰动为零，从而近似消除思考格式 KL 约束，将原问题简化为无约束的指令跟随最大化问题。

2. **Stage 2：指令注意力引导的模块缩放**。使用从 IFEval 蒸馏并通过 LLM-as-Judge 筛选得到的 365 条指令校准集，对每个注意力头计算指令对齐度 $a^{\tilde{k}}$（注意力在指令相关区域的聚集程度）和泄漏度 $u^{\tilde{k}}$（注意力在无关区域的分散程度），合并为指令注意力代理目标 $\mathcal{I}_I^{\mathrm{Proxy}}$（Eq. 11）。在初始合并点对该目标做二阶泰勒展开，利用前向注意力统计线性近似梯度 $g^{\tilde{k}}$（Eq. 14）和对角 Hessian $\tilde{H}^{\tilde{k}}$，通过带盒约束的凸二次规划闭式解求得每模块最优缩放系数 $\alpha_{\star}^{\tilde{k}}$（Eq. 15）。

最终合并模型由推理锚点参数、全局标量 $\lambda$ 和缩放后的投影任务向量组合而成（Eq. 16），仅合并对注意力输出敏感的 Q、K、V、O 及 FFN 模块。整个合并过程仅需约 21 分钟，无需任何梯度计算。

## 核心模块与公式推导

RAIN-Merging 的核心调控机制由两个级联阶段构成：**推理感知的零空间投影（Stage 1）** 与 **指令注意力引导的模块缩放（Stage 2）**。两阶段共同解决一个约束优化问题——在保持思考格式 KL 散度不超过阈值 $\delta$ 的前提下，最大化指令跟随代理目标 $\mathcal{I}_I$：

$$
\operatorname*{max}_{\Delta} \mathcal{I}_{I}(\theta_{R}+\Delta) \quad \mathrm{s.t.} \quad \mathcal{L}_{\mathrm{think}}(\theta_{R}+\Delta) \leq \delta
$$

其中 $\theta_R$ 为推理模型锚点参数，$\Delta$ 为待求的参数扰动。

---

### Stage 1：推理感知的零空间投影

**瓶颈**：LRM 输出包含显式的 `<think>...</think>` 思考段，而 ITM 仅输出最终答案。直接将 ITM 任务向量 $\Delta_I$ 加性合并会扰动思考标记处的输出分布，破坏推理格式。

**机制**：对每个子模块 $k$，构建思考标记位置集 $\Omega_{\mathrm{think}}$ 上的前向特征算子 $\Phi_{\Omega_{\mathrm{think}}}^{k}$，将输入向量按克罗内克-向量化形式堆叠：

$$
\Phi_{\{t\}}^{k} := \big[ (h_{1}^{k})^{\top} \otimes \mathrm{diag}(1), \ldots, (h_{T}^{k})^{\top} \otimes \mathrm{diag}(1) \big]
$$

基于该算子构造最小二乘正交投影矩阵 $P^{\perp}$，将 ITM 任务向量映射到前向特征零空间：

$$
P^{\perp}(\Phi_{\Omega_{\mathrm{think}}}^{k}) = \mathrm{diag}(1) - {\Phi_{\Omega_{\mathrm{think}}}^{k}}^{\top} (\Phi_{\Omega_{\mathrm{think}}}^{k} \Phi_{\Omega_{\mathrm{think}}}^{k}^{\top})^{+} \Phi_{\Omega_{\mathrm{think}}}^{k}
$$

投影后的任务向量 $\Delta_I^{\perp,k}$ 满足 $\Phi_{\Omega_{\mathrm{think}}} \mathrm{vec}(\Delta_I^{\perp}) = 0$，即思考标记处前向特征的一阶扰动被消除。结合 softmax KL 散度的二阶上界（$\mathrm{KL}(\mathrm{softmax}(z+u) \| \mathrm{softmax}(z)) \le \frac{1}{8} \|u\|_2^2$），该投影近似满足原始约束，将优化问题简化为：

$$
\boxed{\underset{\Delta^{\perp}}{\operatorname*{max}} \; \mathcal{I}_I(\theta_R + \Delta^{\perp})}
$$

**证据强度**：消融实验（Fig. 5）显示零空间投影使思考标记 KL 散度降至 0.0065，缺失 `</think>` 比例降为 0%，直接验证了格式保护的有效性。

---

### Stage 2：指令注意力引导的模块缩放

**瓶颈**：投影后的任务向量仍需决定每模块的合并强度。全局统一标量无法区分不同注意力头对指令的敏感度差异。

**机制**：定义指令注意力代理目标 $\mathcal{I}_I^{\mathrm{Proxy}}$，由两个统计量构成：

- **对齐度** $a^{\tilde{k}}$：注意力头 $\tilde{k}$ 在指令相关区域 $\mathcal{R}(x)$ 上的归一化注意力响应
- **泄漏度** $u^{\tilde{k}}$：同一注意力头在无关区域 $\mathcal{U}(x)$ 上的归一化注意力响应

代理目标为 $\mathcal{I}_I^{\mathrm{Proxy}}(\tilde{\alpha}) := \bar{a}(\tilde{\alpha}) - \rho \bar{u}(\tilde{\alpha})$，其中 $\rho$ 为泄漏惩罚系数。在初始合并点 $\tilde{\alpha}_{(0)}$ 处做二阶泰勒展开，利用前向注意力统计线性近似梯度：

$$
g^{\tilde{k}} \approx \mathbb{E}_{x\sim\mathcal{D}_I}[a^{\tilde{k}}(x,\tilde{\alpha}_{(0)}) - \rho u^{\tilde{k}}(x,\tilde{\alpha}_{(0)})]
$$

对角 Hessian 近似为 $\tilde{H}^{\tilde{k}} = \mathrm{diag}(1) + \mathbb{E}[u^{\tilde{k}}]$，惩罚高泄漏头的大步长。最终通过带盒约束的凸二次规划求得每头最优缩放系数的闭式解：

$$
\tilde{\alpha}_{\star}^{\tilde{k}} = \mathrm{clip}_{[\tilde{\alpha}_{l},\tilde{\alpha}_{u}]} \left( \frac{g^{\tilde{k}}}{\tilde{H}^{\tilde{k}}} \right)
$$

**最终合并模型**为：

$$
\theta_{\star} = \theta_{R} + \lambda \bigoplus_{k=1}^{K} \alpha_{\star}^{k} \Delta_{I}^{\perp,k}
$$

其中 $\lambda$ 为全局标量（实验显示 $\lambda \approx 1.0$ 时取得最佳平衡），$\alpha_{\star}^{k}$ 为 Stage 2 输出的模块级缩放系数。

**证据强度**：两阶段消融（Table 4）表明，同时启用 Stage 1 和 Stage 2 使指令跟随平均分从 46.75（仅 Stage 2）提升至 48.11，推理平均分从 54.22（仅 Stage 1）提升至 55.59，证实两阶段互补。Fig. 6 的分层指令注意力得分显示 RAIN-Merging 在各层均优于 LRM 和 Task Arithmetic。

---

### 关键实现约束

- **合并模块范围**：仅合并对注意力输出敏感的 Q、K、V、O 及 FFN 模块（证据锚点：Implementation details）
- **校准数据**：Stage 1 从 Mixture-of-Thoughts 采样 150 个思考格式样本；Stage 2 从 IFEval 蒸馏并通过 LLM-as-Judge 筛选得到 365 条带标注指令范围的样本
- **公平性**：所有数据依赖合并方法使用相同的校准数据，并统一应用 TIES 后处理（符号一致性与幅度截断）

## 实验与分析

### 主结果：指令遵循与推理能力的全面权衡

RAIN-Merging 在合并 Qwen2.5-7B-Instruct（ITM）到 DeepSeek-R1-Distill-Qwen-7B（LRM）的主实验中，实现了指令遵循与推理能力的双重提升（Table 1）。在指令遵循平均分（IFEval、CELLO、InfoBench、ComplexBench）上，RAIN-Merging 达到 48.11，较原始 LRM 的 44.12 提升 3.99 分；在推理与通用能力平均分（Math、GPQA、Aider、Arena-Hard-v2）上达到 55.59，较 LRM 的 51.03 提升 4.56 分。两项指标均显著超越所有基线合并方法，包括 Task Arithmetic（Ilharco et al., 2023）、TIES、DARE-TIES 等无数据方法，以及 ACM-TIES、LEWIS-TIES、AIM-TIES 等数据依赖方法。


![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_PO2iULmu5e/figures/004_Table_1.jpg]]
*Table 1: Comprehensive comparison of instruction following and reasoning & general capabilities. We merge Qwen2.5-7B-Instruct (ITM) into DeepSeek-R1-Distill-Qwen-7B (LRM) and compare our RAIN-Merging against multiple merging methods as well as SFT trained on the same calibration data. “Avg.” denotes the average over all subsets. “RT” reports the run-time for merging or training in minutes. The best and second-best results are highlighted in bold and underlined, respectively*

关键单基准表现如下：
- **IFEval strict accuracy**：RAIN-Merging 达 63.22%，较 LRM 的 55.45% 提升 7.77 个百分点，逼近 ITM 自身的 66.92%。
- **Math 六基准平均**：RAIN-Merging 达 68.75%，较 LRM 的 64.75% 提升 4.00 个百分点，高于 ITM 的 60.33%。
- **GPQA**：RAIN-Merging 达 54.55%，较 LRM 的 48.88% 提升 5.67 个百分点。

值得注意的是，RAIN-Merging 在指令遵循上不仅超越所有合并基线，还优于使用相同校准数据训练的 SFT（48.11 vs. 45.08），且合并时间仅约 21 分钟，远低于 SFT 的 120 分钟。在推理与通用能力上，SFT 出现明显退化（49.51），而 RAIN-Merging 保持了正向增益。

### 可扩展性与架构泛化

在不同模型规模和架构上的实验（Table 2）表明 RAIN-Merging 具有一致的增益模式：

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_PO2iULmu5e/figures/005_Table_2.jpg]]
*Table 2: Merging performance and relative gains of RAIN-Merging across model three scales and two architectures. We merge the corresponding ITM into the LRM with base models: Qwen2.5-1.5B/14B/32B, and Llama-3.1-8B. “Avg.” denotes the average over all subsets. For each scale, the subsequent “(relative gain)” row reports the relative improvement of our method over the LRM, highlighted in green*

- **Qwen2.5-1.5B**：指令遵循平均分从 32.96 提升至 34.97（相对增益 +6.09%），推理平均分从 31.19 提升至 33.74（+8.20%）。
- **Qwen2.5-14B**：指令遵循平均分从 51.33 提升至 52.14（+1.57%），推理平均分从 64.50 提升至 67.05（+3.96%）。
- **Qwen2.5-32B**：指令遵循平均分从 51.77 提升至 53.52（+3.38%），推理平均分从 68.28 提升至 70.59（+3.38%）。
- **Llama-3.1-8B**（跨架构）：指令遵循平均分从 43.83 提升至 48.62（+10.93%），推理平均分从 47.60 提升至 48.94（+2.82%）。

跨架构的显著增益证实了 RAIN-Merging 不依赖于特定模型族的 tokenizer 或模板设计，其核心机制具有较好的泛化性。小模型上的相对增益更大，这可能是因为小模型 LRM 的指令遵循基础更弱，合并 ITM 任务向量的边际收益更高。

### 两阶段消融：零空间投影与指令注意力系数的互补性

Table 4 的消融实验揭示了两个阶段的独立贡献与协同效应：

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_PO2iULmu5e/figures/007_Table_4.jpg]]
*Table 4: Performance of ablation on Stage 1 and Stage 2, under the same setup as Tab. 1. "I Avg." and "R Avg." denote the average performance on instruction-following and reasoning & general benchmarks*

- **仅 Stage 1（零空间投影 + 统一 λ）**：指令遵循平均分 44.12（与 LRM 持平），推理平均分 54.22（较 LRM 的 51.03 提升 3.19）。说明零空间投影本身主要保护推理能力，对指令遵循无直接增益。
- **仅 Stage 2（指令注意力引导系数，无投影）**：指令遵循平均分 46.75（较 LRM 提升 2.63），推理平均分 52.56（较 LRM 提升 1.53）。说明指令注意力引导的模块缩放能有效增强指令遵循，但缺少投影保护时推理增益受限。
- **Stage 1 + Stage 2（完整 RAIN-Merging）**：指令遵循平均分 48.11，推理平均分 55.59，两项均达到最优。这证实了两阶段的互补性——零空间投影为推理提供“安全网”，使指令注意力引导的缩放可以在不损害思考格式的前提下更激进地增强指令遵循。

### 思考格式保护机制的有效性验证

Figure 5 从两个维度量化了 Stage 1 的格式保护效果：
- **$\mathcal{L}_{\mathrm{think}}$（思考段 KL 散度）**：RAIN-Merging 仅产生 0.0065 的 KL 散度，而 Task Arithmetic 为 0.0571，TIES 为 0.0207。极低的 KL 散度表明合并后模型在思考特殊标记处的输出分布几乎与原始 LRM 一致。
- **缺失 `</think>` 比例**：RAIN-Merging 在 IFEval 上的缺失率为 0.0%，而 Task Arithmetic 高达 37.33%，TIES 也有 6.89%。这说明直接合并会严重破坏思考段的结束标记生成，导致推理链断裂，而零空间投影完全消除了这一问题。

### 指令注意力引导系数的分层效果

Figure 6 展示了合并后模型在各层的指令注意力得分（对齐度 − 泄漏度）：
- RAIN-Merging 在所有层上均持续优于原始 LRM 和 Task Arithmetic，尤其在中间层（第 10–20 层）增益最为显著。
- Task Arithmetic 在部分层上甚至低于 LRM，说明不加区分的全局合并可能引入注意力泄漏，损害指令跟随。
- 指令注意力引导的模块缩放系数（Figure A6 热力图）显示，不同注意力头和层的系数差异显著，验证了“一刀切”合并策略的不足，以及差异化缩放的必要性。

### 约束推理场景：MathIF 与推理轨迹质量

在 MathIF 基准（Table 5）上，RAIN-Merging 的“Both Acc.”（指令约束与数学答案同时正确）达到 20.48%，较 LRM 的 12.62% 相对提升 62.26%。这表明 RAIN-Merging 不仅提升了指令遵循和数学推理的独立能力，更重要的是增强了二者的协同——模型能在遵循格式约束的前提下完成复杂推理。


![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_PO2iULmu5e/figures/009_Table_5.jpg]]
*Table 5: Merging performance of RAIN-Merging on MathIF under the same configuration as Tab. 1. IF Acc. and Math Acc. are the accuracy of instruction constraints and math answers, respectively. Both Acc. represents both constraints and math answers are correct. Table 6: Evaluation of reasoning and answer traces under the same configuration as Tab. 1. We report Reasoning Internal Coherence (RIC) and Reasoning-Answer Alignment (RAA) on IFEval, AIME25, and GPQA (0-5 scale). The subsequent “(relative gain)” row reports the relative improvement of our method over the LRM, highlighted in green*

推理轨迹质量评估（Table 6）进一步验证了这一点：
- **推理内部一致性（RIC）**：RAIN-Merging 在 IFEval、AIME25、GPQA 上分别达到 4.63、4.42、4.57（5 分制），均优于 LRM。
- **推理-答案对齐度（RAA）**：在 AIME25 上从 3.60 提升至 4.10（+13.89%），在 GPQA 上从 3.76 提升至 4.26（+13.31%）。这说明合并后的模型不仅给出了正确答案，其思考链与最终答案之间的一致性也更强。

### 智能体场景与资源效率

在智能体设置（Table 3）中，RAIN-Merging 在 ALFWorld 上达到 25.00%，在 WebShop 上达到 29.42%，均优于原始 LRM（分别为 18.33% 和 25.24%）和 ITM（分别为 15.83% 和 26.12%）。这证明合并模型在需要多步交互和指令遵循的具身场景中同样有效。


![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_PO2iULmu5e/figures/006_Table_3.jpg]]
*Table 3: Performance of RAIN-Merging in agent settings. We merge Qwen2.5-7B-Instruct (ITM) into DeepSeek-R1-Distill-Qwen-7B (LRM). Figure 4: GPU memory usage comparison between different methods under the same configuration as Tab. 1*

资源方面（Figure 4），RAIN-Merging 的 GPU 内存消耗与 Task Arithmetic 等轻量合并方法相当，远低于 SFT 和 AIM-TIES 等数据依赖方法。结合其约 21 分钟的合并时间，该方法在计算效率上具有显著优势。

### 失败模式与局限性

尽管 RAIN-Merging 在多数基准上表现优异，但分析揭示了几个值得关注的边界：
1. **非思考段的安全漂移**：零空间投影仅约束思考特殊标记段，对非思考内容和安全相关行为没有正式保障。在对抗性指令或越狱场景下的鲁棒性尚未评估。
2. **校准数据依赖性**：指令校准集仅 365 条样本，且来源于 IFEval 的二次蒸馏和 LLM-as-Judge 筛选。当指令分布发生显著偏移时（如跨语言、代码生成、多模态场景），指令注意力代理指标的泛化性可能下降。Table A8 显示，使用 InfoBench 的开放域指令集时性能略有变化，说明校准数据的选择对最终效果有影响。
3. **R1 模板依赖**：零空间投影依赖 `<think>...</think>` 标记来定位思考段。对于采用隐式思维链或不同模板的模型（如 Claude 的内部推理），该方法需要重新设计标记检测逻辑，否则约束可能失效。
4. **指令改写鲁棒性有限**：Table A10 显示，RAIN-Merging 对改写指令的鲁棒性（HAcc(paraphrase)/HAcc(original)）在某些指令类型上低于 LRM，提示指令注意力代理可能鼓励了针对特定格式模式的“短视”优化，而非深层语义理解。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Table 1 | RAIN-Merging 在指令遵循（48.11）和推理（55.59）平均分上全面超越所有合并基线和 SFT |
| Table 2 | 跨 1.5B–32B 四档规模和 Llama 架构均保持正向增益，小模型相对增益更大 |
| Table 4 | Stage 1 保护推理，Stage 2 增强指令遵循，两阶段协同达到最优权衡 |
| Figure 5 | 零空间投影将 $\mathcal{L}_{\mathrm{think}}$ 降至 0.0065，缺失 `</think>` 率降至 0% |
| Figure 6 | 指令注意力引导系数使各层注意力得分持续优于 LRM 和 Task Arithmetic |
| Table 5 | MathIF 联合正确率相对提升 62.26%，证明约束推理能力的协同增强 |
| Table 6 | 推理-答案对齐度在 AIME25 和 GPQA 上分别提升 13.89% 和 13.31% |

### 补充图表

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_PO2iULmu5e/figures/010_Figure.jpg]]
*Figure: A1: Principal subspace cosine similarity between DeepSeek-R1-Distill-Qwen-1.5B (LRM) and Qwen2.5-1.5B-Instruct (ITM) task vectors for each layer and submodule. Figure A2: Principal subspace cosine similarity between DeepSeek-R1-Distill-Qwen-14B (LRM) and Qwen2.5- 14B-Instruct (ITM) task vectors for each layer and submodule*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_PO2iULmu5e/figures/015_Table.jpg]]
*Table: A4: The hyperparameters of various merging methods in Tab. 1. λ means the global scaling coefficient in merging. k denotes the trim ratio in TIES-Merging. p means the drop rate in DARE merging. τ is sharpness the ACM. ρ is the pruning ratio in LEWIS. ω means the balance factor in AIM. Table A5: The hyperparameters of RAIN-Merging in different model sizes. λ means the global scaling coefficient in RAIN-Merging*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_PO2iULmu5e/figures/011_Table.jpg]]
*Table: A1: Reasoning calibration set construction from Mixture-of-Thoughts. We uniformly sample 50 examples per domain for calibration and 50 for validation. Raw sizes are taken from the official dataset composition page*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_PO2iULmu5e/figures/013_Table.jpg]]
*Table: A2: Instruction-following benchmarks. We list dataset size, constraint taxonomy, composition types, verification, and aggregation strategy*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_PO2iULmu5e/figures/014_Table.jpg]]
*Table: A3: Test set sizes of the six math benchmarks used in our mathematical reasoning (Math) evaluation*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_PO2iULmu5e/figures/016_Table.jpg]]
*Table: A6: Math benchmark results under the same configuration as in Tab. 1. “Avg.” denotes the average over all math benchmarks. The best and second-best results are highlighted in bold and underlined, respectively*


## 方法谱系与知识库定位

### 核心瓶颈与调控逻辑

大型推理模型（LRM）在数学推理、代码生成等任务上表现优异，但其指令遵循能力薄弱。根本瓶颈在于：LRM具有明确的`<think>...</think>`思考段输出格式，而指令微调模型（ITM）仅输出最终答案，两者输出分布存在结构性差异。直接进行参数合并（如Task Arithmetic）会导致思考格式破坏——思考段KL散度上升、`</think>`缺失率增加，进而损害推理能力。

RAIN-Merging的核心调控逻辑建立在两个关键发现之上：
1. **参数正交性**：LRM与ITM的任务向量在主要模块的主子空间余弦相似度均低于0.1（Fig. 2, Fig. A1, Fig. A2），说明推理能力与指令遵循能力的参数主方向几乎正交，为轻量合并提供了理论前提。
2. **格式约束可解耦**：通过在思考标记处施加零空间投影，可消除对思考格式的一阶扰动，使格式保持与指令增强两项任务解耦。

### 方法谱系定位

RAIN-Merging属于**训练无关的模型合并**（training-free model merging）方法，其基线谱系可分为三类：

**无数据合并基线**：
- **Task Arithmetic**（Ilharco et al., 2023）：直接将任务向量加权相加，作为最基础的无数据合并范式。
- **SLERP**、**Karcher**：基于参数空间几何插值的合并方法。
- **TIES-Merging**：通过符号一致性和幅度截断去除任务向量中的冗余和冲突成分。
- **DARE-TIES**：在TIES基础上引入随机参数丢弃（drop rate p），进一步降低干扰。

**数据依赖合并基线**：
- **ACM-TIES**：利用激活一致性度量指导合并，引入锐度参数τ。
- **LEWIS-TIES**：基于参数重要性剪枝（pruning ratio ρ）进行选择性合并。
- **AIM-TIES**：通过注意力对齐指标和平衡因子ω加权合并。

**监督微调对比**：
- **SFT**：在相同校准数据上进行监督微调，作为训练方法的性能上界参考。

RAIN-Merging在合并范式上的三个关键改进槽位：

| 改进槽位 | 基线方法 | RAIN-Merging | 证据锚点 |
|---------|---------|-------------|---------|
| 任务向量预处理 | 原始ITM任务向量Δ_I直接加性合并 | 将Δ_I投影到由思考标记前向特征构建的零空间，得到Δ_I^⟂，保证思考标记处前向特征不变 | Eq. (5) |
| 合并系数策略 | 全局统一标量λ或基于参数统计的固定缩放 | 根据指令注意力对齐度和泄漏度计算每模块系数α_⋆^k（通过二次规划闭式解），针对不同注意力头和FFN层差异化缩放 | Eq. (15) |
| 合并模块范围 | 可能包含所有线性层 | 仅合并对注意力输出敏感的Q、K、V、O及FFN模块 | 实现细节 |

### 两阶段管道的因果机制

**Stage 1: 推理感知的零空间投影**

该阶段的核心目标是**消除合并对思考格式的扰动**。具体机制为：
1. 从Mixture-of-Thoughts数据集采样150个具有完整思考格式的样本，提取`<think>...</think>`标记位置集合Ω_think。
2. 对每个子模块k，基于思考标记输入构建前向特征算子Φ_Ω_think^k，计算最小二乘正交投影矩阵P^⟂（Eq. 4）。
3. 将ITM任务向量Δ_I^k投影到零空间，得到Δ_I^{⟂,k}（Eq. 5）。

该操作的因果效应：投影后的任务向量满足Φ_Ω_think · vec(Δ_I^⟂) = 0，即对思考标记处的前向特征无贡献，从而在一阶近似下消除输出分布偏移。实验证据显示，零空间投影使思考段KL散度降至0.0065，`</think>`缺失率降为0%（Fig. 5），有效保护了思考格式。

**Stage 2: 指令注意力引导的模块缩放**

该阶段的核心目标是**选择性增强指令遵循能力**。具体机制为：
1. 构建指令校准集：从IFEval二次蒸馏并通过LLM-as-Judge筛选得到365条样本，每条样本标注指令相关区域R(x)、约束输出范围T(x)和无关注区域U(x)。
2. 计算每个注意力头的指令对齐度a^k̃（指令区域对约束输出的注意力聚合）和泄漏度u^k̃（无关注区域对约束输出的注意力聚合），合并为指令注意力代理目标`I_I^Proxy = ā - ρ·ū`（Eq. 11）。
3. 在初始合并点对代理目标做二阶泰勒展开，利用前向注意力统计线性近似梯度g^k̃（Eq. 14），并用对角Hessian近似H̃^k̃惩罚高泄漏头（Eq. 15）。
4. 求解带盒约束的凸二次规划，得到每头最优缩放系数α_⋆^k̃的闭式解（Eq. 15）。

该操作的因果效应：指令注意力引导的模块缩放使合并后模型在各层指令注意力得分上均优于LRM和Task Arithmetic（Fig. 6），表明Stage 2有效提升了指令跟随能力。

**两阶段协同**：消融实验（Table 4）证实，同时启用Stage 1和Stage 2使指令跟随平均分从46.75（仅Stage 2）提升至48.11，推理平均分从54.22（仅Stage 1）提升至55.59，证明两阶段具有互补效应——零空间投影保护推理格式，指令注意力引导增强指令遵循。

### 适用边界与局限

**格式依赖性强**：
方法依赖R1风格模板和分词器提取`<think>...</think>`来构建零空间。若模型采用隐式思维链（hidden chain-of-thought）或不同模板，约束可能减弱或失效。零空间投影能否扩展到保护其他结构化输出格式（如代码段标识符、特定JSON模板）仍是开放问题。

**校准数据规模与质量**：
指令校准集仅365条样本，且包含来自LLM-as-Judge自动标注的噪声。跨语言或任务域分布偏移可能影响合并系数的泛化性。实验显示，使用不同指令校准集（IFEval vs InfoBench）会导致性能波动（Table A8），表明Stage 2的系数求解对校准数据分布敏感。

**安全与能力漂移**：
尽管对思考段施加KL约束有助于保持推理格式，但非思考内容和安全相关行为可能仍有漂移，目前没有正式的安全保障机制。指令注意力代理指标可能鼓励针对格式匹配的短视优化，而非深层语义理解。

**架构与规模泛化**：
实验主要聚焦于Qwen/DeepSeek家族模型（1.5B-32B），在多模态LLMs、工具使用、代码生成和多语言场景下的适用性仍需系统评估。在更大模型（如70B+）上的效果尚不明确。

**合并模块范围限制**：
仅合并Q/K/V/O/FFN模块，未考虑embedding层、LayerNorm等组件，可能遗漏部分指令遵循能力的参数载体。

### 开放问题

1. **跨格式扩展**：零空间投影能否泛化到保护其他结构化输出格式（如代码块标记、特定模板约束），而不仅限于`<think>`标记？
2. **隐式推理适应**：如何设计更通用的思考令牌检测方法以适应非R1格式或隐式推理过程，使方法不依赖特定分词器行为？
3. **安全性保证**：如何正式保证合并后模型的安全性，防止指令注入攻击或有害输出漂移？
4. **大规模验证**：在70B+参数规模和更多架构（如非Qwen系列、混合专家模型）上的效果如何？
5. **多模态扩展**：RAIN-Merging的零空间投影和指令注意力引导机制能否适配视觉-语言模型的多模态输入输出格式？
6. **动态合并策略**：当前方法使用静态校准集计算合并系数，能否设计在线自适应机制，根据推理时的指令类型动态调整缩放系数？

## 原文 PDF

![[paperPDFs/ICLR_2026/RAIN_Merging_A_Gradient_Free_Method_to_Enhance_Instruction_Following_in_Large_Reasoning_Models_with_Preserved_Thinking_Format.pdf]]
