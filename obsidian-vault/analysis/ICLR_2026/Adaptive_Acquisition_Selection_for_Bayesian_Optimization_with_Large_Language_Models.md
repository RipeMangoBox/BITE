---
title: "Adaptive Acquisition Selection for Bayesian Optimization with Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Adaptive_Acquisition_Selection_for_Bayesian_Optimization_with_Large_Language_Models.pdf
aliases:
- LLMAABO
- AASBOLLM
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/zero_order_and_black_box_optimization
core_operator: "利用预训练大语言模型的推理能力，在每次迭代时根据完整的优化状态文本摘要动态选择最合适的采集函数。"
primary_logic: "将采集函数选择转化为上下文决策问题，通过结构化状态表示使LLM能够零样本地综合多维状态信息，实现动态的探索-利用平衡策略。"
claims:
- "LMABO 在 50 个基准问题上显著优于所有静态、自适应和基于 LLM 的基线方法。"
- "消融实验表明，移除状态摘要的任何元素都会显著降低 LMABO 的性能。"
- "LMABO 根据优化进度动态调整采集函数选择，在停滞时偏好探索，在剩余预算低时偏好利用。"
- "状态敏感性分析表明 LLM 的输出采集函数对每个状态元素的扰动都有响应。"
---

# Adaptive Acquisition Selection for Bayesian Optimization with Large Language Models

> [!tip] 核心洞察
> 将采集函数选择转化为上下文决策问题，通过结构化状态表示使LLM能够零样本地综合多维状态信息，实现动态的探索-利用平衡策略。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于大语言模型的自适应采集函数选择用于贝叶斯优化 |
| 英文题名 | Adaptive Acquisition Selection for Bayesian Optimization with Large Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=EPKmSgXvRe) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/zero_order_and_black_box_optimization |
| Method | LMABO (Language Model-Assisted Adaptive Bayesian Optimization) |
| Dataset | 50 个合成与超参数优化问题 |

> [!tip] 效果简介
> - 50 个合成与超参数优化问题上，总 AUC（越低越好）为 LMABO，对比最佳静态采集函数（EI），变化 -9.7%。
> - 50 个合成与超参数优化问题上，总 AUC 为 LMABO，对比最佳自适应 portfolio 方法，变化 -16.6%。
> - 50 个合成与超参数优化问题上，总 AUC 为 LMABO，对比最佳基于 LLM 的 BO 方法，变化 -54.7%。

## 概述

贝叶斯优化（Bayesian Optimization, BO）在昂贵黑箱函数优化中广泛应用，其性能高度依赖采集函数（Acquisition Function, AF）的选择。现有自适应采集函数选择方法（如基于强化学习或投资组合分配的策略）仅依据历史函数值进行决策，忽略了剩余预算、替代模型超参数、优化停滞状态等全局上下文信息，导致无法动态、精细地实现探索与利用的平衡。

本文提出 **LMABO (Language Model-Assisted Adaptive Bayesian Optimization)**，将采集函数选择重新构造为一个上下文决策任务：以预训练大语言模型（LLM）作为零样本、在线的优化策略师，在每次迭代时根据结构化的文本状态摘要（包含进程状态、性能历史、剩余预算及高斯过程核参数等）从多样化的采集函数组合中动态选出最合适的采集函数。该方法无需任务特定微调，仅通过提示（prompt）引导 LLM 进行推理。

在 50 个合成函数与超参数优化问题上的实验表明，LMABO 的总 AUC 比最佳静态采集函数低 9.7%，比最佳自适应 portfolio 方法低 16.6%，比现有基于 LLM 的 BO 方法低 54.7%，在所有基线中取得了最优的平均相对性能（Mean RP = 1.21）和平均排名（5.62）。消融实验确认状态摘要的每个组件（剩余预算、GP 模型特性、最短距离信息、避免无效采集的指令）都对性能有显著贡献，移除任何一个都会导致性能退化。成本分析显示，单次 50 轮优化的 LLM API 费用约 $0.01，额外延迟约 1 秒/次，对真实应用的影响可忽略。

## 背景与动机

贝叶斯优化（BO）通过高斯过程（GP）替代模型估计目标函数后验分布，并由采集函数（AF）引导下一个评估点的选择。常见的静态采集函数，如 Expected Improvement（EI）侧重利用，Upper Confidence Bound（UCB）侧重探索，但其探索-利用权衡是固定的，难以匹配动态变化的优化进程。为突破这一局限，出现了自适应投资组合方法（如 GP‑Hedge、ESP），根据各采集函数的历史性能奖励动态分配权重。然而，这类方法仍存在一个关键瓶颈：**它们仅依据过去的函数值进行决策，忽略了剩余预算、GP 模型超参数（如各输入维度的长度尺度 ℓᵢ 和输出尺度 σ²_f）等对策略选择至关重要的丰富状态信息**。GP 的平方指数核函数

$$
k(\boldsymbol{x}, \boldsymbol{x'}) = \sigma_f^2 \exp\left(-\frac{1}{2} \sum_{i=1}^d \frac{(x_i - x_i')^2}{\ell_i^2}\right)
$$

中，长度尺度 ℓᵢ 控制函数沿各维度的变化速率，输出尺度 σ²_f 决定整体函数值方差，这些超参数直接反映了替代模型对目标函数形状的认知，而现有的自适应机制普遍未能加以利用。此外，人工设计规则或基于强化学习的策略往往依赖大量专家知识或任务特定训练，难以在新任务上快速泛化。

上述局限源于采集函数选择机制未能将 BO 过程的**完整多维状态**（优化进度、性能历史、模型特性等）综合为决策依据。为突破这一瓶颈，[论文] 提出 **LMABO (Language Model‑Assisted Adaptive Bayesian Optimization)**，核心洞见是将采集函数选择转化为**上下文决策问题**：利用预训练大语言模型（LLM）的零样本推理能力，在每次迭代时根据包含**过程状态、性能历史与 GP 模型特征**的结构化文本摘要，动态选择最合适的采集函数。该方法无需任务特定的微调，通过将高维数值状态压缩为 LLM 可理解的文本，使其能像一位优化专家一样综合多维信息，实时调整探索-利用策略。这一设计使 BO 策略能够感知优化过程的阶段性变化——在停滞时偏好探索、在剩余预算不足时转向利用——为自适应采集函数选择开辟了新的范式。

## 核心创新

现有自适应采集函数选择方法（例如 GP‑Hedge、No‑PASt‑BO 等自适应 portfolio）仅依据过去的函数值或替代模型的奖励信号来分配采集函数权重，完全忽略了**剩余优化预算、高斯过程超参数（如长度尺度 ℓᵢ 和输出尺度 σ²_f）以及优化停滞状态**等对探索‑利用平衡至关重要的多维上下文信息。这使得策略无法及时感知优化进程所处阶段，导致预算浪费或过早收敛。

LMABO 将上述缺陷转化为一个可明确操作的改进槽：

1. **采集函数选择策略的重构**  
   基线方法基于历史性能奖励进行投资组合分配（如 GP‑Hedge 的 Hedge 算法），而 LMABO 将采集函数选择重新形式化为**上下文决策问题**：在每次迭代，由一个冻结参数的预训练大语言模型（LLM）充当闭环策略师，根据完整的优化状态摘要**零样本、在线地**从包含 12 个候选采集函数的集合中挑选最合适的一个。该设计无需任务特定微调，利用了 LLM 在综合多源信息时的强推理能力。

2. **状态表示的扩充**  
   基线方法仅以数值形式输入过去的目标函数值。LMABO 构造的结构化文本摘要 Sₜ 显式编码了三个此前被忽略的关键信息源：
   - **进程状态**：当前迭代编号、剩余预算 N_rem、当前最优值 f_min、最近若干次迭代的改进/停滞序列。
   - **性能历史**：替代模型在已观测点上的预测质量（如最短距离、停滞标记）。
   - **GP 模型特征**：从平方指数核  
     $$k(\boldsymbol{x}, \boldsymbol{x'}) = \sigma_f^2 \exp\left(-\frac{1}{2} \sum_{i=1}^d \frac{(x_i - x_i')^2}{\ell_i^2}\right)$$  
     中提取的各输入维度的最小/最大长度尺度 ℓᵢ 以及输出尺度 σ²_f——这些超参数直接反映函数在不同方向上的变化速率和整体方差，是平衡探索与利用的关键信号。

3. **决策机制的零样本化**  
   基线方法依赖手工设计的规则（如经典 GP‑Hedge 中的对冲更新）或针对特定任务训练的强化学习策略。LMABO 将决策完全委托给**预训练 LLM 的上下文推理**：通过静态初始提示 P₀ 定义角色、可用采集函数及其特性，并将上述状态摘要 Sₜ 嵌入每次的提示 Pₜ 中，LLM 即可生成所选采集函数缩写及决策理由（温度 0.0 保证确定性，无效回退率仅 0.11%）。这种零样本机制使策略天然具备跨函数和跨预算的泛化能力，无需重训练。

上述三个槽位的协同改变带来了决定性的性能优势：在 50 个合成与超参数优化问题上，LMABO 的总体曲线下面积 (AUC) 相比于**最优静态采集函数 (EI) 降低 9.7%**，相比于**最优自适应 portfolio 方法降低 16.6%**，相比于**最优基于 LLM 的 BO 方法降低 54.7%** (Table 1)。消融实验 (Table 2) 进一步证实，**移除状态摘要中任一元素（剩余预算、GP 模型特征、最短距离信息，以及防止无效采集函数的指令）都会显著损害性能**，其中防止无效采集函数的指令被移除后性能退化最为严重 (RP 升至 1.92)。行为分析表明，LMABO 能根据进程动态调整探索‑利用偏好：停滞期倾向选择探索型采集函数（如 Figure 2a 中 UCB、TS 的高频使用），剩余预算低时则转向纯利用型采集函数（如 PosMean），且其采集函数切换频率远高于依赖固定更新规则的自适应方法 (Figure 2b)。状态敏感性分析 (Tables 9–12) 则直接证明，LLM 的输出采集函数会对剩余预算、长度尺度等状态元素的变化做出可解释的响应，而非单纯依赖函数值历史。

## 整体框架

LMABO 的整体流程将 BO 中的采集函数选择重新定义为一个上下文决策任务：在每一轮迭代中，由一个预训练的大语言模型（LLM）作为零样本在线决策器，根据结构化的优化状态摘要动态选择当前最合适的采集函数。该框架的核心创新在于将传统自适应方法中仅依赖历史函数值的选择策略，替换为 LLM 对多维状态信息的综合推理，从而实现对探索-利用平衡的更精细调控。

整个 pipeline 由四个顺序执行的模块构成：

1. **初始提示 $P_0$ 构建**：在优化开始前，构造一条静态的指令性提示，定义 LLM 的角色（"BO 专家"）、可用采集函数清单、状态摘要的格式模板以及要求的输出格式。该提示通过角色赋予和格式约束，使 LLM 在零样本条件下产出结构化的专家级决策。

2. **状态摘要 $S_t$ 生成**：在第 $t$ 次迭代，将当前优化过程的高维数值状态转化为简洁、可读的文本摘要。摘要包含三个关键元素：
   - **过程状态**：当前迭代次数、剩余预算 $N_{\mathrm{rem}}$、已观测的最优值 $f_{\min}$ 及其停滞情况；
   - **性能历史**：最近几次迭代中采集函数的选择记录与对应的改进量；
   - **GP 模型特征**：从高斯过程替代模型中提取的核函数超参数，包括各输入维度的长度尺度 $\ell_i$ 和输出尺度 $\sigma_f^2$，以及最近观测点之间的最短距离。

   该模块是框架的瓶颈所在：其设计决定了 LLM 能否感知替代模型的不确定性和搜索空间的局部结构。消融实验（Table 2）证实，移除状态摘要中的任何一个元素（如剩余预算、GP 模型特征或最短距离）都会显著降低 LMABO 的性能，其中移除"避免无效采集函数"的指令会导致最大退化。

3. **LLM 决策器**：将初始提示 $P_0$ 与当前状态摘要 $S_t$ 拼接为完整提示 $P_t$，发送给预训练 LLM（实验中采用 Gemini 2.5 Flash 或 GPT-4o mini，温度设为 0.0 以保证确定性）。LLM 返回一个选中的采集函数缩写（从 12 个候选采集函数中选择，包括探索型的 PosSTD、UCB、TS、KG 等和利用型的 PosMean、PI、EI、LogEI 等）及相应的选择理由。此过程无需任何任务特定微调，完全依靠 LLM 的上下文推理能力。无效或解析失败的响应会自动回退至 UCB，回退率极低（约 0.11%）。

4. **GP 替代模型拟合与采集函数优化**：标准的 BO 步骤。在获得选定的采集函数 $\alpha_t$ 后，拟合高斯过程替代模型 $\mathcal{GP}_{t-1}$（使用平方指数核 $k(\boldsymbol{x}, \boldsymbol{x'}) = \sigma_f^2 \exp\left(-\frac{1}{2} \sum_{i=1}^d \frac{(x_i - x_i')^2}{\ell_i^2}\right)$），然后优化 $\alpha_t$ 以确定下一个查询点 $\boldsymbol{x}_t$，评估目标函数后更新观测数据集。此模块与决策器形成闭环：新的观测将影响下一轮的状态摘要，驱动 LLM 基于最新信息重新决策。

**输入/输出流**：输入为初始设计点集合和总迭代预算；每一轮迭代的输入是上一步的观测历史，输出是选定的采集函数及下一个评估点。框架对 LLM 的查询开销极小：每次迭代 API 调用耗时约 1 秒，50 次迭代总费用约 $0.01，相对于昂贵的黑箱函数评估可忽略。

该框架将采集函数选择转化为**状态→决策**的端到端映射，状态表示的结构完整性是关键因果瓶颈——LLM 通过综合剩余预算、优化进度和模型不确定性等维度，实现了自动化的探索-利用策略调整：分析表明，LMABO 在停滞期偏好探索（如选择 UCB 或 TS），在剩余预算低时显著增加利用型采集函数（如 PosMean）的使用，且其采集函数切换频率高于所有基线自适应方法（Figure 2a–2c）。框架对各状态元素的敏感性也通过扰动实验得到验证（Tables 9–12），LLM 的输出会随剩余预算、最短距离或长度尺度的变化而相应改变。

## 核心模块与公式推导

### 核心模块

LMABO 将采集函数选择转化为上下文决策问题，框架由四个顺序模块构成，每次迭代依次执行：

1. **初始提示 P₀ 构建**
   该静态提示在整个优化过程中保持不变，为 LLM 设定角色（BO 专家）、可用的采集函数组合、预期输入的状态模式以及输出格式（采集函数缩写 + 选择理由）。提示内容确保 LLM 以专家视角进行决策，避免试探性输出。

2. **优化状态摘要 Sₜ 生成**
   在第 t 次迭代，BO 流程的高维数值状态被序列化为结构化文本摘要 Sₜ。摘要包含三类核心元素：
   - **进程状态**：当前迭代索引 t、剩余预算 N_rem、当前最优目标值 f_min、最短距离（最近两个评估点之间的最小欧氏距离）。
   - **性能历史**：近期目标值变化趋势及停滞状态标志。
   - **GP 替代模型特性**：拟合的高斯过程模型 GP_{t-1} 的核函数超参数——各输入维度的长度尺度 ℓ_i 与输出尺度 σ_f²，以及替代模型在各点的均值与不确定性。

   这些元素拼接后构成提示 Pₜ = P₀ + Sₜ，发送给 LLM。

3. **LLM 决策器**
   预训练 LLM（实验中默认使用 Gemini 2.5 Flash）在零样本设定下接收 Pₜ，直接输出选中的采集函数名称及简短推理日志。查询温度设为 0.0 以保证确定性；若 LLM 响应格式无效或失败，自动回退至 UCB 采集函数（回退率仅 0.11%）。

4. **GP 替代模型拟合与采集函数优化**
   使用历史评估数据拟合高斯过程替代模型，然后根据 LLM 选择的采集函数 α_t 在搜索空间中通过多起点 LBFGS‑B 优化该函数，确定下一个评估点 x_t。这一模块为标准 BO 流程，LMABO 未做改动。

上述流程将 LLM 作为闭环策略引擎，每步都能综合当前优化状态的完整上下文动态选择采集函数，无需任务特定微调。

### 关键公式与变量含义

#### 高斯过程核函数
LMABO 使用平方指数核（Squared Exponential Kernel）建模函数平滑性：

$$
k(\boldsymbol{x}, \boldsymbol{x'}) = \sigma_f^2 \exp\left(-\frac{1}{2} \sum_{i=1}^d \frac{(x_i - x_i')^2}{\ell_i^2}\right)
$$

- **ℓ_i**（长度尺度）：控制函数沿输入维度 i 的变化速率，ℓ_i 越小则该维度函数变化越剧烈。
- **σ_f²**（输出尺度）：决定函数值的总体方差。
- **d**：输入空间维度。

状态摘要中会将 GP 的 ℓ_i 和 σ_f² 作为模型特性反馈给 LLM，用于判断当前替代模型的置信度与探索需求。

#### 基础采集函数
从 12 个采集函数组合中选取的经典公式（完整定义见附录 A）：

**概率改进（PI）**
$$
\alpha_{\mathrm{PI}}(x) = \Phi\left(\frac{\mu(x) - \tau}{\sigma(x)}\right)
$$
- **μ(x)**：GP 在点 x 的预测均值。
- **σ(x)**：GP 在点 x 的预测标准差。
- **τ**：当前最优目标值（incumbent）。
- **Φ**：标准正态累积分布函数。

PI 度量点 x 改进目标 τ 的概率，偏向利用。

**期望改进（EI）**
$$
\alpha_{\mathrm{EI}}(x) = (\mu(x) - \tau)\Phi(z) + \sigma(x)\phi(z), \quad z = \frac{\mu(x) - \tau}{\sigma(x)}
$$
- **φ**：标准正态概率密度函数。
- **z**：标准化改进量。

EI 综合衡量改进概率与改进幅度，是 LMABO 最频繁选择的采集函数之一。

**上置信界（UCB）**
$$
\alpha_{\mathrm{UCB}}(x) = \mu(x) + \kappa \sigma(x)
$$
- **κ**：探索-利用权衡参数，控制不确定性加权的强度。

UCB 通过 κ 显式调节探索倾向。在无效响应回退时，LMABO 默认调用 UCB。

状态摘要中的剩余预算 N_rem 和停滞标志直接影响 LLM 在上述函数间的切换行为：如剩余预算较低时偏向 EI 或 LogEI（利用），停滞时偏向 UCB 或 TS（探索）。

## 实验与分析

**主结果：50 个基准上的全面领先**  
表 1 汇总了 LMABO 与 23 个基线方法在 50 个优化问题上的平均相对性能（Mean RP）和平均排名。LMABO 的 Mean RP 为 1.21，比最佳静态采集函数 EI（1.34）低 9.7%，比最佳自适应 portfolio 方法（如 GP-Hedge Curated）低 16.6%，比最佳基于 LLM 的 BO 方法 LLAMBO （原文中为 LLAMBO 或 LLMP，前者使用 LLM 辅助替代建模）低 54.7%。在所有方法中 LMABO 还取得最低的平均排名（5.62）和最低的 AUC 变异系数（CV=0.37），表明其性能在不同随机种子和问题类型上高度稳定。统计检验确认方法之间差异显著（Friedman 检验 p < 0.05；事后两两比较见原文附录）。  
**机制**：这些增益源于 LMABO 将采集函数选择重塑为上下文决策问题——LLM 在每次迭代接收包含剩余预算、性能历史、GP 超参数（长度尺度 $\ell_i$、输出尺度 $\sigma_f^2$）的文本状态摘要，零样本地综合多维信息，动态调控探索与利用的平衡。传统的自适应方法（如 GP-Hedge）仅依赖过去的函数值进行投资组合分配，而忽略了模型状态和预算约束，导致其 Mean RP 比 LMABO 显著更差（例如 GP-Hedge Curated 的 RP 为 1.51 且排名靠后）。

![[assets/figures/papers/iclr26_0006_EPKmSgXvRe_Adaptive_Acquisition_Selection_for_Bayesian_Opti/figures/001_Table_1.jpg]]
*Table 1: Overall performance comparison of LMABO against all baselines across 50 optimization problems. P-values from Friedman tests in the last row indicate statistically significant differences among methods for both RP and rank. The third and fifth columns show p-values of posthoc pairwise comparisons between LMABO and each method, which confirm that the differences in performance between LMABO and all methods are significant. Exploitative AFs are marked in blue and explorative AFs are marked in magenta (see Appendix A for details)*

**消融实验：状态摘要要素的因果贡献**  
表 2 的消融研究逐一冻结 LMABO 的关键设计元素。移除状态摘要中的剩余预算、GP 模型特性或最短距离信息均导致 Mean RP 显著上升（性能变差）。其中，移除"避免无效采集函数"的指令造成最大退化——Mean RP 飙升至 1.92，说明 LLM 必须被显式告知不推荐某些采集函数，否则会选择性能极差的策略。使用更小规模的 LLM（Qwen3‑8B）时性能仍优于大多数基线（但劣于 120B 模型），证实大模型的规模缩放对决策质量有帮助，但即使是小模型也能通过结构化状态描述提取有效信号；替换后端为 GPT‑4o mini 时性能与此接近。  
**证据强度**：表 2 中所有消融变体的退化均明显超出随机波动，但需要结合原文的统计检验细节确认差异显著性（原文未在该节详细列出 p 值，读者可查阅附录）。总体而言，状态摘要的每个组件都是 LMABO 高性能的必要条件，而显式的注意事项（如避免无梯度采集函数）起到了安全防护作用。

![[assets/figures/papers/iclr26_0006_EPKmSgXvRe_Adaptive_Acquisition_Selection_for_Bayesian_Opti/figures/002_Table_2.jpg]]
*Table 2: Ablation study on the components of LMABO. We analyze the contribution of LMABO's key components by comparing the full model to multiple ablated versions. LMABO-8B/30B uses open-source LLMs (Qwen3-8B and Qwen3-30B-A3B-Thinking-2507 (Team, 2025)). LMABO-120B uses the open-weight model gpt-oss-120b (OpenAI, 2025). The Mean RP and Mean Rank are calculated using the same global ranking of all baseline and ablation methods as in Table 1*

**策略动态：探索‑利用的自适应切换**  
图 2a‑c 揭示了采集函数选择频率和切换行为。LMABO 对 EI、LogEI 和 TS 存在明确的偏好，且随着优化进程动态变化：早期 EI 使用频率逐渐上升，后期 TS 使用减少，PosMean 在接近预算耗尽时启动。图 2b 进一步显示，LMABO 在探索型和利用型采集函数之间切换的频率远高于任何基线，而这种频繁切换与更优的优化轨迹相关。图 2c 的相态分析表明，当优化陷入停滞时，LMABO 倾向于选择探索型（如前五个 AF）以求突破；而一旦观察到目标函数改进，则转向利用型（如后七个 AF）以精炼极值。  
**因果解释**：状态摘要中的"停滞计数器"和"剩余预算"是该行为的直接驱动因素：停滞多则鼓励探索，预算少则强制利用。这一策略使 LMABO 能模仿有经验的优化专家，根据实时反馈灵活调整决策，避免陷入局部最优或过早收敛。

![[assets/figures/papers/iclr26_0006_EPKmSgXvRe_Adaptive_Acquisition_Selection_for_Bayesian_Opti/figures/021_Figure_2.jpg]]
*Figure 2: (c) AF selection frequency by improvement/stagnation status. "Stagnation" is defined as no improvement in the incumbent, and "Improvement" is defined as any change in the incumbent. Figure 2: LMABO's acquisition function selection behaviors. Note that these behaviors are aggregated across all runs on all problems*

**失败模式与脆弱性**  
虽然原文未系统报告失败案例，但实验揭示了两个脆弱点：其一，若 LLM 不被显式约束避免无效 AF（表 2 消融），性能急剧恶化，说明依赖 LLM 的先验知识在某些情况下会输出反生产的选择；其二，当使用 8B 级小模型时，性能下降明显但仍然可用，表明决策质量对模型规模与训练数据的覆盖面敏感。LLM 调用回退率仅为 0.11%（温度 0.0 时），在极少数无效输出时自动回退至 UCB，因此该机制在工程上安全。  
**实践瓶颈**：每次 LLM 查询的延迟约 1 秒，50 次迭代总 API 费用约 $0.01，相比昂贵的目标函数评估（如超参搜索）可忽略。但若应用于极低延迟场景，可考虑缓存或边缘部署，需要进一步权衡。

**状态灵敏度与可解释性**  
表 9‑12 的信息敏感性分析对优化早、中、晚期分别扰动每个状态元素，观察 LLM 输出的采集函数如何改变。结果一致表明，LLM 对剩余预算、当前最佳值、GP 长度尺度和最短距离等元素的扰动都有响应；例如，早期阶段若最短距离极小，系统转向 UCB 以增加探索；晚期阶段若剩余预算极小，则选择 PosMean 以保守利用。这种细粒度的条件响应支持了 LMABO 通过结构化摘要实施上下文推理的核心假设，并为调试和信任提供了可解释的决策链。  
**扩展应用证据**：额外引入任务特定先验知识（如函数的多模态性或维度特征）可以加速早期收敛并降低最终遗憾（图 1），进一步佐证 LMABO 框架能够将自然语言上下文转化为 BO 策略增益。

![[assets/figures/papers/iclr26_0006_EPKmSgXvRe_Adaptive_Acquisition_Selection_for_Bayesian_Opti/figures/006_Figure_1.jpg]]
*Figure 1: Impact of task-specific context on LMABO performance. Results are averaged over 10 runs with standard deviation shown as shaded regions*

**运行时与效率权衡**  
与自适应 portfolio 方法相比，LMABO 并未引入额外的高斯过程推理或采集函数优化的计算开销，其额外成本主要来自 LLM API 调用。表 5 显示，LMABO 的平均运行时间（约 7.8 分钟）远低于 GP-Hedge（109 分钟）和 No-PASt-BO（115 分钟），与单次采集函数的优化时间（约 2 分钟）相比增长可控。这一开销特征使其在成本敏感但目标函数昂贵的场景中极具吸引力。

**总结**：LMABO 通过将 BO 过程的状态浓缩为文本并让 LLM 扮演零样本决策者，在 50 个多样基准上实现了对静态、自适应和 LLM 辅助 BO 方法的大幅领先。消融和动态分析表明，关键增益来自完整的状态描述（尤其是预算和停滞信息），以及显式的安全约束。失败风险集中于小模型和指令遗漏，工程上通过回退机制和低开销 API 调用得到缓解。读者如需核对具体问题的逐题结果与统计细节，应查阅原文附录。

### 补充图表

![[assets/figures/papers/iclr26_0006_EPKmSgXvRe_Adaptive_Acquisition_Selection_for_Bayesian_Opti/figures/012_Figure_10.jpg]]
*Figure 10: (a) AF selection frequency over the optimization process*

![[assets/figures/papers/iclr26_0006_EPKmSgXvRe_Adaptive_Acquisition_Selection_for_Bayesian_Opti/figures/017_Figure_15.jpg]]
*Figure 15: (b) AF switch frequency*

## 方法谱系与知识库定位

### 与基线方法的关系与创新定位

LMABO 在自适应贝叶斯优化（BO）的采集函数选择问题上与三类基线形成对照。第一类为静态采集函数（如 Expected Improvement  `EI` 和 Upper Confidence Bound  `UCB`），它们在整个优化过程中固定地偏向利用或探索，无法根据优化进展动态切换策略。第二类为自适应投资组合方法（如 GP‑Hedge 和 ESP），其决策仅依赖历史函数奖励或信息论准则，忽略了剩余预算、替代模型超参数等丰富的状态信号（见 verified_analysis 中的因果旋钮与瓶颈描述）。第三类为现有基于 LLM 的 BO 辅助方法（LLAMBO 用于替代建模与提议点、LLMP 提供自然语言先验），它们不将 LLM 用作在每次迭代中动态选择采集函数的闭环决策器。

LMABO 填补的核心空白在于 **将采集函数选择重新定义为基于结构化状态摘要的上下文决策任务**，并借助预训练 LLM 的零样本推理进行在线选择，状态摘要同步纳入了剩余预算 `N_rem`、性能历史（如最优值 `f_min` 的停滞信息）以及 GP 模型的长度尺度 `ℓ_i` 和输出尺度 `σ_f^2` 等通常被忽略的维度（据 `Section 4.3` 和 Table 2 消融证据，置信度 0.9–0.95）。这一设计使得 LMABO 从方法上区别于仅依据过去函数值的自适应基线（changed_slots，"采集函数选择策略"从基于历史奖励的投资组合分配变为 LLM 零样本在线决策），并直接导致了大幅的性能提升：在 50 个合成与超参数优化基准上，总 AUC 相对最佳静态 AF 降低 9.7%、相对最佳自适应 portfolio 方法降低 16.6%、相对最佳基于 LLM 的 BO 方法降低 54.7%（Table 1，置信度 0.95）。因此 LMABO 在方法谱系中可定位为 **首个利用 LLM 综合多维优化状态进行零样本动态采集函数选择的框架**。

### 适用边界

LMABO 的设计假设黑箱函数评估成本远高于 LLM 调用开销，这使得该方法在超参数优化、实验设计等典型场景中具有工作可行性。实验表明，每次 LLM 调用延迟约 1 秒，一次 50 次迭代的运行总 API 费用仅约 $0.01，且采用温度 0.0 保证确定性，回退率极低（约 0.11%）（见 fairness_notes）。然而，当函数评估本身非常廉价或需要实时响应时（例如毫秒级模拟器），延迟与成本将不再可忽略，此时 LMABO 可能不占优势。

现有的验证范围主要覆盖中低维问题（COCO 合成函数 2～5 维、BoTorch 合成函数 2～6 维、Bayesmark 超参数调优），且所有实验均在 50 次迭代的预算约束下进行。尽管 LMABO 在该范围内表现出很强的泛化性（Friedman 检验确认统计显著性，Table 1），但在高维 BO 或迭代次数极大增加时，状态摘要的信息密度、LLM 的上下文窗口限制和 GP 替代模型的可靠性都可能引入新的不确定性，需要进一步验证。

### 主要局限

消融实验（Table 2）揭示了状态摘要设计对性能的边际贡献，同时也暴露了其脆弱性。移除"避免无效采集函数"的指令会导致平均相对性能 (RP) 从 1.21 急剧退化至 1.92，说明 LMABO 的高性能高度依赖精心构造的提示工程，而非 LLM 对 BO 任务的内隐理解。同样，去除剩余预算、GP 模型特性（长度尺度、输出尺度）或最短距离中的任意一项均会造成显著性能下降（置信度 0.9）。当使用规模较小的 LLM（如 Qwen3‑8B）替代旗舰模型时，性能有所下滑，但仍优于多数基线（Table 2），表明零样本推理能力受模型容量影响，但框架本身保留了相当的鲁棒性。

此外，LMABO 的决策回退机制虽可靠（无效响应默认回退到 UCB，失败率仅 0.11%），但在极端情况下仍会将控制权交给固定采集函数，这可能在关键阶段引入次优选择。采集函数组合库固定为 12 个（包含探索型与利用型 AF），若特定问题结构超越该集合的覆盖范围，LLM 也无法突破组合限定。

### 开放问题

- **LLM 推理的可解释性与可微调性**：当前 LMABO 以零样本方式使用 LLM，其状态敏感性分析（Tables 9–12）证实 LLM 的输出会受到各状态元素扰动的影响，但这种决策的因果推理过程仍不透明。是否可以通过微调或上下文示例进一步强化决策质量，以及是否会造成对特定问题分布的过拟合，尚待研究。
- **扩展至高维、多目标和约束优化**：现有基准集中于低维无约束问题。在更高维度下，GP 超参数作为状态摘要的一部分能否有效刻画函数景观的不确定性尚不明确；在多目标或带有未知约束的 BO 中，如何将帕累托前沿信息或可行性状态压缩为文本输入并令 LLM 理解，是该方向的关键挑战。
- **自动化状态构建与元学习**：当前状态摘要由人工设计，消融实验固然证明了各组件的有效性，但从长远看，能否学习出最优的状态表示（如通过将代码中的数值数组转化为自然语言的策略）仍是一个开放课题。
- **更大规模 LLM 与成本权衡**：随着迭代次数和问题规模的增长，LLM 调用的成本与延迟可能不再微不足道。是否存在缓存、批量调用或使用更小专用模型的策略，以降低 LMABO 在实际部署中的资源消耗，值得进一步探索。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Adaptive_Acquisition_Selection_for_Bayesian_Optimization_with_Large_Language_Models.pdf

![[paperPDFs/ICLR_2026/Adaptive_Acquisition_Selection_for_Bayesian_Optimization_with_Large_Language_Models.pdf]]
