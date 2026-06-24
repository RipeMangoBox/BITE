---
title: "Capacity-Aware Inference: Mitigating the Straggler Effect in Mixture of Experts"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Capacity_Aware_Inference_Mitigating_the_Straggler_Effect_in_Mixture_of_Experts.pdf
openreview_forum_id: LuYFpySWA2
aliases:
- CAICATDCAED
- CAIMSEME
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/algorithms
core_operator: "专家容量系数γ，通过设定每个专家可容纳的最大令牌数C=γN̄，直接控制负载不均程度与推理加速。"
primary_logic: "对过载专家采用容量感知令牌丢弃（丢弃少量低分令牌可大幅提升效率且性能损失极小）；对欠载专家利用同一设备上的额外候选专家（扩展丢弃）吸收溢出令牌，从而在容量受限条件下保持甚至提升模型性能。"
claims:
- "OLMoE在仅损失0.9%准确率的情况下，MoE层推理加速30%"
- "基于门控分数的令牌丢弃在γ＝2.0时达到与无容量约束基线相同的平均准确率（64.0）"
- "Mixtral-8×7B-Instruct 应用扩展丢弃后平均性能提升0.2%，推理加速至1.85倍"
- "丢弃过载令牌总量的12%即可使Mixtral-8×7B-Instruct推理速度提升85%"
---

# Capacity-Aware Inference: Mitigating the Straggler Effect in Mixture of Experts

> [!tip] 核心洞察
> 对过载专家采用容量感知令牌丢弃（丢弃少量低分令牌可大幅提升效率且性能损失极小）；对欠载专家利用同一设备上的额外候选专家（扩展丢弃）吸收溢出令牌，从而在容量受限条件下保持甚至提升模型性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 容量感知推理：缓解混合专家模型中的掉队者效应 |
| 英文题名 | Capacity-Aware Inference: Mitigating the Straggler Effect in Mixture of Experts |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=LuYFpySWA2); [GitHub](https://github.com/CASE-Lab-UMD/Capacity-Aware-MoE) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/algorithms |
| Method | Capacity-Aware Inference (含 Capacity-Aware Token Drop 和 Capacity-Aware Expanded Drop) |
| Dataset | 8 benchmarks avg (OBQA, PIQA, RTE, WinoGrande, BoolQ, ARC-C, HellaSwag, MMLU) on OLMoE, MoE single layer speedup (OLMoE, Token Drop), 8 benchmarks avg on Mixtral-8×7B-Instruct, End-to-end inference (Mixtral-8×7B-Instruct, Expanded Drop) |

> [!tip] 效果简介
> - 8 benchmarks avg (OBQA, PIQA, RTE, WinoGrande, BoolQ, ARC-C, HellaSwag, MMLU) o... 上，Average Accuracy 为 64.0 (Token Drop, Score, γ=2.0)，对比 64.0 (Dropless)，变化 0.0%。
> - MoE single layer speedup (OLMoE, Token Drop) 上，Speedup ratio 为 1.30× (γ=2.0)，对比 1.00×，变化 30%。
> - 8 benchmarks avg on Mixtral-8×7B-Instruct 上，Average Accuracy 为 0.2% improvement (Expanded Drop, γ=1.5)，对比 Dropless，变化 +0.2%。

## 概述

混合专家（Mixture of Experts, MoE）模型通过稀疏激活机制在扩展模型容量的同时控制计算成本，但其推理效率受限于一个根本性瓶颈：令牌到专家的分配严重不均衡，导致部分专家过载、部分专家欠载，整体时延由负载最重的专家决定——即“掉队者效应”（Straggler Effect）。Figure 1 展示了这一现象：在 OLMoE 模型上，部分专家的归一化负载远超平均值，形成显著的负载差异。

针对这一问题，本文提出**容量感知推理（Capacity-Aware Inference）**，通过引入专家容量约束直接控制负载不均程度，在不显著损失模型性能的前提下实现推理加速。方法包含两个互补策略：

- **容量感知令牌丢弃（Capacity-Aware Token Drop）**：设定专家容量系数 γ，定义每位专家的最大令牌容量 $C = \gamma \bar{N}$（其中 $\bar{N} = tk/n$ 为每专家期望令牌数），对过载专家基于门控分数丢弃超出容量限制的低分令牌。
- **容量感知扩展丢弃（Capacity-Aware Expanded Drop）**：在令牌丢弃基础上，允许每个令牌将同设备上的所有本地专家纳入候选集，再利用设备级容量约束重新分配令牌，从而吸收欠载专家的剩余容量。

核心实验结论如下：

1. **精度保持**：在 OLMoE 上，基于门控分数的令牌丢弃在 γ=2.0 时达到与无容量约束基线相同的平均准确率（64.0），仅损失 0.9% 准确率即可实现 MoE 层 30% 的推理加速。

2. **性能提升**：在 Mixtral-8×7B-Instruct 上应用扩展丢弃后，平均性能提升 0.2%，端到端推理加速达 1.85 倍；仅丢弃 12% 的过载令牌即可获得 85% 的推理速度提升（Figure 7）。

3. **策略优势**：门控分数丢弃（Score）在所有容量系数下均优于顺序、逆序、随机丢弃策略（Table 1）；设备级容量约束优于专家级约束，且允许更低的 γ 值（Table 3）。

4. **安全阈值**：容量系数 γ=1.5 足以维持与无损推理相当的性能，低于 1.0 时性能急剧下降（Figure 12），构成精度-速度权衡的关键拐点。

方法的局限性在于：当 γ<1.0 时性能骤降，限制了极低负载场景的应用；且方法假设专家并行与 All-to-All 通信，通信开销未完全消除。后续值得探索的方向包括自适应动态调整 γ、扩展丢弃中候选专家数 m 的最优权衡、以及与训练阶段负载均衡损失的联合优化。

## 背景与动机

### 混合专家模型推理中的“掉队者效应”

混合专家（Mixture of Experts, MoE）模型通过在推理时仅激活部分专家来实现高效计算，但其性能高度依赖令牌到专家的分配均衡性。实际推理中，令牌分配严重失衡：以OLMoE在Open-BookQA上的表现为例，部分专家的归一化负载超过平均负载的七倍（Figure 2），形成明显的“热专家”与“冷专家”分化。

这一失衡直接导致MoE层整体时延由负载最重的专家决定，即**掉队者效应（Straggler Effect）**。形式化地，MoE层的推理时延 $L$ 与各专家负载的最大值成正比：

$$L \propto \max(\{N_i\}_{i=1}^{n})$$

其中 $N_i$ 为分配给第 $i$ 个专家的令牌数。给定总令牌数 $t$、Top-K 专家数 $k$ 和专家总数 $n$，每个专家的期望令牌数为 $\bar{N} = \frac{t k}{n}$，但实际分配中最大值远超此均值，导致计算资源闲置与通信拥塞并存。

### 现有方法的缺口

当前MoE推理通常采用“无丢弃”策略，即所有令牌均被分配至其Top-K专家，不施加任何容量限制。这种做法虽能保证模型输出的完整性，却无法控制掉队者效应带来的时延膨胀。

训练阶段常用的负载均衡损失虽能在一定程度上缓解专家偏好集中问题，但无法在推理时动态应对输入数据分布变化引起的负载波动。此外，直接丢弃整组低负载专家的“Expert Drop”策略过于粗糙，会造成显著的性能损失。

### 核心动机与关键问题

本文的核心动机在于：**能否通过在推理时主动控制专家负载上限，以极小的性能代价换取显著的推理加速？** 这引出了两个紧密关联的子问题：

1. **过载专家问题**：如何有效限制高负载专家的令牌数量，以消除掉队者效应？
2. **欠载专家问题**：如何利用低负载专家的闲置容量，在容量约束下维持甚至提升模型性能？

解决这两个问题的关键在于引入**专家容量**这一可控变量，通过容量系数 $\gamma$ 定义每个专家可容纳的最大令牌数 $C = \gamma \bar{N}$，从而将时延上界约束在可预测范围内：

$$\max(\{N_i\}_{i=1}^{n}) = \begin{cases} \gamma < 1: \bar{N} \\ \gamma \geq 1: \text{within}\{\bar{N}, \gamma \bar{N}\} \end{cases}$$

这一形式化为容量感知推理提供了理论锚点：当 $\gamma \geq 1$ 时，最高负载被限制在 $\gamma \bar{N}$ 以内，推理时延可控；当 $\gamma < 1$ 时，所有专家负载被强制均衡至 $\bar{N}$，但性能可能急剧下降（Figure 12）。因此，寻找在精度-速度权衡曲面上最优的容量系数与令牌选择策略，构成了本文方法设计的核心驱动力。

## 核心创新

### 创新动机：掉队者效应与负载失衡

MoE推理的核心瓶颈在于令牌分配严重不均衡——部分专家接收的令牌数可达平均值的七倍以上（Figure 2），导致整体时延由负载最重的专家决定，即**掉队者效应**（Figure 1）。形式上，给定总令牌数 $t$、top-k 专家数 $k$ 和专家总数 $n$，每个专家的期望令牌数为 $\bar{N} = \frac{t k}{n}$，而实际时延 $L \propto \max(\{N_i\}_{i=1}^{n})$。传统无容量约束推理允许专家接收任意数量令牌，使得 $\max(N_i)$ 远超 $\bar{N}$，造成严重负载不均。

### 核心创新一：容量感知令牌丢弃（Capacity-Aware Token Drop）

**changed slot：引入专家容量约束**

基线方法对令牌分配不设上限，所有令牌均被分配至所选专家。本方法引入容量系数 $\gamma$，定义每个专家的最大容量 $C = \gamma \bar{N}$，强制丢弃超出容量部分的令牌。容量约束下的最大负载上界为：

$$\operatorname{max}(\{N_i\}_{i=1}^{n}) = \begin{cases} \gamma < 1: \bar{N} \\ \gamma \geq 1: \text{within}\{\bar{N}, \gamma \bar{N}\} \end{cases}$$

这表明当 $\gamma \geq 1$ 时，最重负载被严格限制在 $[\bar{N}, \gamma\bar{N}]$ 区间内，从根本上消除了极端过载。

**changed slot：基于门控分数的令牌选择策略**

基线不丢弃任何令牌。本方法在容量约束下需决定保留哪些令牌，探索了四种选择指标：顺序（Order）、逆序（Reverse Order）、随机（Random）和门控分数（Score）。其中，基于 softmax 和 top-k 操作后的门控分数作为重要性指标，保留得分最高的 $C$ 个令牌，丢弃低分令牌。过载专家的容量阈值定义为：

$$\tau_{\mathcal{I}} = \mathrm{KthValue}(\boldsymbol{S}_{\mathcal{I}}, C)$$

Table 1 的消融实验表明，Score 策略在所有容量系数下均显著优于其他指标——在 $\gamma=2.0$ 时达到与无容量约束基线相同的平均准确率 64.0，而 Random 仅为 61.3。这证明**少量低分令牌的丢弃对性能影响极小**，是该方法有效性的关键支撑。

### 核心创新二：容量感知扩展丢弃（Capacity-Aware Expanded Drop）

**changed slot：候选专家集从 Top-k 扩展至同设备本地专家**

基线仅选取 Top-k 个专家。本方法允许每个令牌额外考虑同设备上所有 $m$ 个本地专家作为候选（共 $k+m$ 个），再利用设备级容量约束淘汰低分令牌。这一设计解决了 Token Drop 的固有缺陷：欠载专家的计算资源未被充分利用，而丢弃的令牌可能原本可以被这些专家有效处理。

扩展丢弃在严格本地容量约束下运行，具体采用设备级容量约束：

$$N_1 + N_2 + ... + N_{n_l} \leq n_l \cdot \gamma \bar{N}$$

Table 3 显示，设备级约束在 Qwen3-MoE 上以 $\gamma=1.0$ 达到平均分 74.8，优于专家级约束在 $\gamma=1.5$ 时的 73.9，且允许更低的容量系数。Table 2 进一步表明，Expanded Drop 在四个 MoE 模型上一致优于 Token Drop 和 Expert Drop（直接丢弃整组低负载专家的消融方案）。

**关键设计选择：不限制每令牌最多选 $k$ 个专家**

扩展丢弃有意不强制每令牌最多选出 $k$ 个专家的约束。Appendix D 的消融实验（Table 11）证实，取消该限制后平均性能从 61.0 提升至 61.2，多个基准任务一致改善。这避免了为保留 top-k 而重复选择与丢弃的复杂操作。

### 创新效果总结

两项创新协同作用：Token Drop 通过容量约束和分数选择直接削减过载专家的计算量，Expanded Drop 利用本地候选专家吸收溢出令牌以维持性能。在 Mixtral-8×7B-Instruct 上，仅丢弃 12% 的过载令牌即可实现 1.85× 端到端推理加速，同时平均性能提升 0.2%（Figure 7, Abstract）。在 OLMoE 上，MoE 层推理加速 30%，准确率仅下降 0.9%。

**需要手动验证的点**：扩展丢弃中候选专家数 $m$ 与负载均衡、精度之间的最优权衡曲面尚未系统探索，文中仅基于经验分析选择了不限制最大专家数的策略。

## 整体框架

![[assets/figures/papers/iclr26_0012_LuYFpySWA2_Capacity-Aware_Inference_Mitigating_the_Straggle/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of Capacity-Aware Token Drop (a) and Expanded Drop (b). Both methods first select experts based on gating scores. In Token Drop, tokens exceeding the local device capacity are discarded prior to All-to-All communication. Expanded Drop enhances expert utilization by allowing each token to consider additional m candidate experts on the same device while still enforcing strict local capacity constraints*

容量感知推理（Capacity-Aware Inference）围绕一个核心矛盾展开：MoE推理的端到端时延由负载最重的专家决定（掉队者效应），而令牌到专家的分配天然存在严重不均衡。该框架在现有MoE推理pipeline中插入两个可选的容量控制模块，在All-to-All通信之前完成令牌筛选与重分配，从而在不改变模型权重的前提下，以极小的性能代价换取显著的推理加速。

### Pipeline总览

整个推理流程由五个模块串联构成：

1. **Gating network（门控网络）**：对每个输入令牌 $\pmb{x}$，路由器 $G$ 计算Softmax得分并选出Top-$k$个专家，形成初始专家候选集 $\mathcal{K} = \mathrm{TopK}(\mathrm{Softmax}(G(\pmb{x})), k)$。
2. **Capacity-Aware Token Drop（容量感知令牌丢弃，可选）**：对每个专家施加容量上限 $C = \gamma \bar{N}$（其中 $\bar{N} = tk/n$ 为期望令牌数），按门控得分保留最高的 $C$ 个令牌，超出容量的低分令牌被直接丢弃。
3. **Capacity-Aware Expanded Drop（容量感知扩展丢弃，可选）**：在Token Drop的基础上，将每个令牌的候选专家集从Top-$k$扩展至同设备上的全部 $m$ 个本地专家（共 $k+m$ 个候选），再施加设备级容量约束进行令牌重分配。
4. **All-to-All communication（全交换通信）**：跨设备交换经容量筛选后的令牌及其得分，完成最终的令牌到专家映射。
5. **Expert computation（专家计算）**：各专家对分配给自己的令牌执行前向计算，输出经门控得分加权求和得到最终结果 $\pmb{\mathcal{Y}} = \sum_{i \in \mathcal{K}} \pmb{G}(\pmb{x})_i \cdot \pmb{E}_i(\pmb{x})$。

两个容量控制模块（Token Drop与Expanded Drop）是框架的核心创新，它们均插入在门控网络之后、All-to-All通信之前，通过提前丢弃部分令牌来削减通信和计算负载。两者的选择取决于场景需求：Token Drop直接对过载专家进行令牌丢弃以降低峰值负载；Expanded Drop则进一步利用欠载专家的空闲容量，将溢出令牌重路由至同设备本地专家，在容量受限条件下保持甚至提升模型性能。

### 容量系数 $\gamma$ 的控制作用

整个框架的可控旋钮是容量系数 $\gamma$。它定义了每个专家的容量上限 $C = \gamma \bar{N}$，直接决定了负载不均的抑制程度与推理加速幅度：

- 当 $\gamma \geq 1$ 时，专家最高负载被约束在 $[\bar{N}, \gamma \bar{N}]$ 区间内，掉队者效应得到有效缓解；
- 当 $\gamma < 1$ 时，所有专家负载被强制压缩至 $\bar{N}$ 以下，但性能会急剧下降（Figure 12显示 $\gamma=1.5$ 是安全阈值）。

实验表明，$\gamma=2.0$ 时基于门控分数的Token Drop即可达到与无容量约束基线相同的平均准确率（Table 1: Score $\gamma=2.0$ Avg 64.0 vs Baseline $+\infty$ 64.0），同时实现MoE层30%的推理加速。将 $\gamma$ 降至1.5并结合Expanded Drop，可在Mixtral-8×7B-Instruct上获得0.2%的平均性能提升和1.85倍端到端推理加速。

### 令牌丢弃策略的选择

在容量约束下，如何选择丢弃哪些令牌至关重要。框架探索了四种评分指标：顺序（Order）、逆序（Reverse Order）、随机（Random）和门控分数（Score）。消融实验（Table 1）表明，基于门控分数的丢弃在所有容量系数下均显著优于其他策略——这源于高门控分数的令牌对最终输出的贡献更大，丢弃低分令牌对模型性能的损害最小。对于多模态MoE模型，框架进一步支持按模态优先级的丢弃策略（如Image-First优先丢弃图像令牌），以适应不同模态对负载均衡的差异化需求。

### 从专家级到设备级的容量约束

Token Drop最初在专家级别施加容量约束，但Expanded Drop的自然扩展是将约束提升到设备粒度：同一设备上所有专家的令牌总数不超过 $n_l \cdot \gamma \bar{N}$。设备级约束允许令牌在同一设备内的专家间自由流动，从而更充分地利用欠载专家的计算资源。Table 3显示，在Qwen3-MoE上，设备级约束（$\gamma=1.0$）的平均性能（74.8）优于专家级约束（$\gamma=1.5$ 的73.9），且允许使用更低的容量系数，获得更高的加速比。

## 核心模块与公式推导

### 3.1 MoE 推理基础

**路由与专家选择**。给定输入令牌 $\pmb{x}$，路由器 $G$ 计算 softmax 得分并选出 top-$k$ 个专家：

$$
\mathcal{K} = \mathrm{TopK}(\mathrm{Softmax}(G(\pmb{x})), k) \tag{1}
$$

被选中专家的输出按门控得分加权求和：

$$
\pmb{\mathcal{Y}} = \sum_{i \in \mathcal{K}} \pmb{G}(\pmb{x})_i \cdot \pmb{E}_i(\pmb{x}) \tag{2}
$$

**负载不均衡的根源**。设总令牌数为 $t$，专家总数为 $n$，每个令牌选 $k$ 个专家，则每个专家的期望令牌数为：

$$
\bar{N} = \frac{t k}{n} \tag{3}
$$

然而实际分配严重偏离期望值——部分专家接收的令牌数可达 $\bar{N}$ 的七倍以上（Figure 2）。由于 MoE 层的整体时延由负载最重的专家决定：

$$
L \propto \max(\{N_i\}_{i=1}^{n}) \tag{4}
$$

这种“掉队者效应”成为推理加速的核心瓶颈。

### 3.2 容量感知令牌丢弃（Capacity-Aware Token Drop）

**核心机制**。引入容量系数 $\gamma$，定义每个专家的容量上限 $C = \gamma \bar{N}$。对每个过载专家，仅保留得分最高的 $C$ 个令牌，其余丢弃。

**令牌得分矩阵**。定义 $S(\pmb{x}) = [s_{ij}]_{t \times n}$ 为每个令牌到每个专家的映射得分矩阵（式 7）。对于过载专家集合 $\mathcal{I}$ 中的专家 $i$，其容量阈值为：

$$
\tau_{\mathcal{I}} = \mathrm{KthValue}(\boldsymbol{S}_{\mathcal{I}}, C) \tag{8}
$$

即保留得分最高的 $C$ 个令牌，丢弃其余。

**丢弃比例**。在容量因子 $\gamma$ 下，被丢弃令牌占总令牌的比例为：

$$
\mathrm{DT} = \frac{\sum_{i=1}^{n} \mathrm{ReLU}(N_i - \gamma \bar{N})}{\sum_{i=1}^{n} N_i} \tag{11}
$$

**四种丢弃策略**。论文探索了四种令牌选择度量（Table 1）：
- **Order**：按令牌在序列中的位置顺序保留
- **Reverse Order**：逆序保留
- **Random**：随机保留
- **Score**：使用 softmax 和 top-k 操作后的门控得分作为重要性指标，保留高分令牌

消融实验表明，**Score 策略在所有容量系数下均显著优于其他三种**。例如在 $\gamma=2.0$ 时，Score 平均准确率 64.0，而 Random 仅 61.3（Table 1）。

**容量约束下的负载上界**。引入容量约束后，专家最高负载的理论上界为：

$$
\operatorname{max}(\{N_i\}_{i=1}^{n}) = \begin{cases} \gamma < 1: \bar{N} \\ \gamma \geq 1: \mathrm{within}\{\bar{N}, \gamma \bar{N}\} \end{cases} \tag{6}
$$

当 $\gamma < 1$ 时，所有专家负载被严格限制在 $\bar{N}$；当 $\gamma \geq 1$ 时，最高负载落在 $[\bar{N}, \gamma\bar{N}]$ 区间内。

### 3.3 容量感知扩展丢弃（Capacity-Aware Expanded Drop）

**核心动机**。Token Drop 仅解决过载专家的问题，但欠载专家的计算资源仍被浪费。Expanded Drop 通过扩展候选专家集来吸收溢出令牌，提升欠载专家的利用率。

**候选集扩展**。设每个设备上部署 $m$ 个专家。对每个令牌，不仅选取 top-k 个专家，还将其所在设备上的**所有 $m$ 个本地专家**纳入候选集（共 $k+m$ 个候选）。随后在设备级容量约束下，按得分重新分配令牌，淘汰低分令牌。

**设备级容量约束**。与专家级约束不同，设备级约束将容量限制施加在设备粒度上：

$$
N_1 + N_2 + ... + N_{n_l} \leq n_l \cdot \gamma \bar{N}
$$

其中 $n_l$ 为设备 $l$ 上的专家数。这意味着同一设备内的专家可以灵活调配容量，只要设备总负载不超过上限即可。

**关键设计选择**：Expanded Drop **不强制**每令牌最多选 $k$ 个专家。消融实验（Table 11）表明，取消此约束对下游任务有益（平均准确率 61.2 vs 61.0），因为允许令牌在扩展候选集中更灵活地匹配高得分专家。

### 3.4 推理流水线

完整流水线包含五个模块：

1. **Gating network**：计算 softmax 得分并选出 top-k 专家（式 1）
2. **Capacity-Aware Token Drop（可选）**：按专家容量对 top-k 分配实施令牌丢弃，仅保留得分最高的令牌（Algorithm 1）
3. **Capacity-Aware Expanded Drop（可选）**：扩展候选专家集至同设备本地专家，再应用设备级容量约束重新分配令牌（Algorithm 2）
4. **All-to-All communication**：跨设备交换令牌及得分，完成最终令牌到专家的映射
5. **Expert computation**：各专家对分配给自己的令牌执行前向计算，输出按式 2 加权组合

两种容量感知方法均**在 All-to-All 通信之前**完成令牌丢弃/重分配，从而减少通信量和专家计算量。时延分解分析（Figure 6）证实，容量感知推理大幅缩减了专家计算、排列和通信的耗时，同时保持门控处理的开销基本不变。

> **注意**：Algorithm 1 和 Algorithm 2 的具体伪代码细节需查阅原文附录 E，此处不逐行复现。

## 实验与分析

### 核心瓶颈与关键控制变量

MoE推理的根本瓶颈在于令牌到专家的分配严重不均衡：部分专家被大量令牌过载，部分专家则严重欠载。推理时延由负载最重的专家决定——即“掉队者效应”（Straggler Effect）。在OLMoE上，部分专家接收的令牌数可达平均值的7倍以上（Figure 2），导致整体时延被少数过载专家拖垮。

控制这一瓶颈的关键变量是**容量系数γ**。给定总令牌数t、top-k专家数k和专家总数n，每个专家的期望令牌数为$\bar{N} = \frac{t k}{n}$。引入γ后，每个专家的容量上限定义为$C = \gamma \bar{N}$，超出容量的令牌将被丢弃。推理时延$L \propto \max(\{N_i\}_{i=1}^{n})$，在容量约束下，最大负载的上界为：

$$
\operatorname{max}(\{N_i\}_{i=1}^{n}) = \begin{cases} \gamma < 1: \bar{N} \\ \gamma \geq 1: \mathrm{within}\{\bar{N}, \gamma \bar{N}\} \end{cases}
$$

当$\gamma \geq 1$时，最大负载被严格限制在$\gamma \bar{N}$以内，从而直接控制掉队者效应的严重程度。

### 主实验结果

**Token Drop：以极小精度代价换取显著加速。** 在OLMoE上，采用基于门控分数的令牌丢弃策略（Score），当$\gamma = 2.0$时，8个基准测试的平均准确率达到64.0，与无容量约束基线（64.0）完全持平（Table 1）。与此同时，MoE单层推理加速30%（Abstract），端到端推理也获得相应提升。

![[assets/figures/papers/iclr26_0012_LuYFpySWA2_Capacity-Aware_Inference_Mitigating_the_Straggle/figures/004_Table_1.jpg]]
*Table 1: Performance comparison across different capacity factors and selection metrics (i.e., Order, Reverse Order, Random, and Score). The baseline operates without capacity constraints, represented as +∞. We report the average performance over multiple random seeds*

**Expanded Drop：在加速的同时实现性能反超。** 在Mixtral-8×7B-Instruct上应用扩展丢弃（Expanded Drop，$\gamma = 1.5$），平均性能比无容量约束基线提升0.2%，端到端推理加速至1.85倍（Abstract）。这一结果的关键机制在于：扩展丢弃允许每个令牌在同设备上额外考虑m个本地专家作为候选，再利用设备级容量约束淘汰低分令牌，从而在欠载专家上吸收原本会被丢弃的溢出令牌，同时保持严格的容量上限。

**设备级约束优于专家级约束。** 在Qwen3-MoE上的对比实验（Table 3）表明，设备级容量约束（$\gamma = 1.0$）的平均得分为74.8，显著优于专家级约束（$\gamma = 1.5$）的73.9。设备级约束允许同一设备内专家间的令牌灵活调配，在更低的容量系数下仍能维持更高性能。

![[assets/figures/papers/iclr26_0012_LuYFpySWA2_Capacity-Aware_Inference_Mitigating_the_Straggle/figures/013_Table_3.jpg]]
*Table 3: Comparison of Device-Level and Expert-Level capacity-aware inference on Qwen3-MoE*

### 消融分析

**令牌丢弃策略的优劣排序。** Table 1系统比较了四种丢弃指标——顺序（Order）、逆序（Reverse Order）、随机（Random）、门控分数（Score）。在所有容量系数下（$\gamma = 2.0, 1.5, 1.0$），基于门控分数的丢弃均取得最高平均准确率。以$\gamma = 2.0$为例：Score 64.0 > Order 63.6 > Reverse Order 63.2 > Random 61.3。这表明Softmax后的门控分数是衡量令牌重要性的有效指标，丢弃低分令牌对模型性能的损害最小。

**容量系数的安全阈值。** Figure 12展示了容量系数从3.0降至0.0时的性能变化曲线：当$\gamma \geq 1.0$时性能保持平稳，$\gamma = 1.5$足以维持与无损推理相当的性能；一旦$\gamma < 1.0$，性能急剧下降。这意味着$\gamma = 1.0$是实际部署的安全下限。

![[assets/figures/papers/iclr26_0012_LuYFpySWA2_Capacity-Aware_Inference_Mitigating_the_Straggle/figures/025_Figure_12.jpg]]
*Figure 12: Performance change as capacity factors decrease from 3.0 to 0.0*

**扩展丢弃中“不限制每令牌最多k个专家”的收益。** Table 11的消融显示，取消“每令牌最多选出k个专家”的约束后，平均准确率从61.0提升至61.2，在多个基准测试上均有稳定改善。这验证了扩展丢弃的设计选择：允许令牌在容量约束下灵活分配到更多候选专家，比强制保留top-k更有益于下游任务。

**多模态场景下的令牌优先级。** 在多模态MoE模型中，图像令牌数量远超文本令牌（例如MME基准中一张图像占576个令牌，文本仅31个令牌，Table 8）。Table 4显示，采用“图像优先丢弃”（Image-First）策略在MME基准上获得最佳感知与认知得分（1362.1 / 297.1 vs 基线1358.1 / 269.6），说明在多模态场景下优先丢弃冗余的图像令牌是更优的负载均衡策略。

### 加速效果的构成分析

Figure 6的时延分解表明，容量感知推理主要缩短了专家计算、令牌置换和通信三个环节的耗时，而门控网络的处理开销基本保持不变。Figure 7进一步量化了丢弃比例与加速收益的关系：在Mixtral-8×7B-Instruct上，丢弃过载令牌总量的12%即可使推理速度提升85%。这一非线性关系说明，少量关键令牌的丢弃即可大幅缓解掉队者效应——因为被丢弃的正是那些导致个别专家严重过载的边际令牌。

### 失败模式与局限

1. **低容量下的性能崩溃。** 当$\gamma < 1.0$时，所有策略的性能均出现断崖式下降（Figure 12），说明容量感知推理无法在极端低负载场景下维持可用精度。
2. **通信开销未完全消除。** 尽管令牌丢弃减少了计算量，All-to-All通信环节仍然保留，整体通信成本未完全消除。
3. **并行策略假设。** 方法假设采用专家并行且令牌在设备间进行All-to-All通信，未在其他并行策略（如张量并行）下充分验证。

### 补充图表

![[assets/figures/papers/iclr26_0012_LuYFpySWA2_Capacity-Aware_Inference_Mitigating_the_Straggle/figures/009_Table_2.jpg]]
*Table 2: Comparison of Expert Drop, Token Drop and Expanded Drop. The capacity factor γ is set to 2.0 for OLMoE and DeepSeek-V2-Lite, and 1.5 for Qwen1.5-MoE-Chat and Mixtral-8×7B-Instruct. For Expert Drop, each forward pass skips one out of eight experts for Mixtral-8×7B-Instruct, and the bottom 10% of lowest load experts for other models*

![[assets/figures/papers/iclr26_0012_LuYFpySWA2_Capacity-Aware_Inference_Mitigating_the_Straggle/figures/005_Figure_4.jpg]]
*Figure 4: Speedup of a single MoE layer compared to the baseline without capacity constraints, achieved through two capacity-aware inference methods: Token Drop and Expanded Drop*

## 方法谱系与知识库定位

### 在MoE推理加速技术谱系中的位置

容量感知推理（Capacity-Aware Inference）处于MoE推理加速技术中“推理时负载均衡”这一分支，与训练阶段通过辅助损失（auxiliary loss）强制专家负载均衡的思路形成互补。训练侧负载均衡损失（如Switch Transformer、GShard中采用的方案）在训练时优化路由，但推理时令牌分布仍可能因数据分布偏移而严重不均——这正是本文揭示的核心问题：**即使训练时专家负载均衡，推理时某些专家仍可能接收超过平均负载7倍以上的令牌**（Figure 2）。容量感知推理直接在推理阶段介入，通过容量约束和令牌丢弃机制截断尾部延迟，无需重新训练或修改模型权重。

与该方法最接近的基线是**Expert Drop**（直接丢弃整组低负载专家），但该方法存在根本性缺陷：丢弃专家意味着其上的所有令牌（包括高门控得分令牌）全部丢失，导致性能大幅下降。容量感知推理通过**令牌级细粒度丢弃**（仅丢弃过载专家上的低分令牌）和**扩展候选专家集**（让令牌有机会被同设备其他专家处理）两个机制，在同等加速比下显著缩小了性能损失。Table 2 的系统对比表明，Expanded Drop 在 OLMoE、Qwen1.5-MoE、DeepSeek-V2-Lite、Mixtral-8×7B-Instruct 四个模型上均一致优于 Expert Drop 和 Token Drop。

### 方法适用边界

**前提条件：**
1. **专家并行部署**：方法假设MoE层采用专家并行策略，每个设备部署一个或多个专家，令牌通过All-to-All通信在设备间交换。若采用张量并行等其他策略，容量约束的粒度需要重新定义。
2. **Top-k路由**：方法针对标准的Top-k稀疏门控MoE架构设计，路由器输出经Softmax后选取前k个专家。对于非Top-k路由（如Hash路由、强化学习路由），需要重新设计得分函数。
3. **批量推理场景**：容量约束的加速效果在批量推理时更为显著，因为此时专家负载不均问题更严重。单令牌推理时负载差异影响有限。

**容量系数γ的安全区间：**
实验表明（Figure 12），γ=1.5 是维持与无损推理相当性能的安全阈值。当γ降至1.0以下时，性能急剧下降——这是容量感知推理的硬性边界。对于Mixtral-8×7B-Instruct，丢弃约12%的过载令牌即可实现85%的推理加速（Figure 7），说明少量令牌丢弃即可换取显著加速，但进一步压缩容量将导致不可接受的性能退化。

**模态敏感性：**
在多模态MoE模型中（Table 4），图像令牌和文本令牌的负载分布存在差异。容量感知推理通过引入模态感知的丢弃策略（如图像优先丢弃）可进一步提升性能，这表明方法需要根据具体模态分布调整丢弃优先级，而非通用地应用统一策略。

### 局限性与未解决问题

1. **通信开销未消除**：容量感知推理虽降低了专家计算量，但All-to-All通信开销依然存在。Figure 6的延迟分解显示，在低容量系数下，通信时间占比相对上升。这限制了加速比的上限。

2. **γ的静态设定**：当前方法使用固定的容量系数γ，无法在运行时根据实际负载动态调整。理想方案应能实时感知各专家负载并自适应调节容量约束，在精度与速度之间动态平衡。

3. **候选专家数m的优化空间**：扩展丢弃中候选专家数m（即同设备上的额外专家数）与负载均衡、精度之间的最优权衡曲面尚未系统探索。m过大会增加门控计算开销，m过小则欠载专家利用率提升有限。

4. **极低容量场景的退化**：当γ<0.5时，仅靠丢弃令牌难以维持性能。是否可通过动态专家复制（将过载专家的知识蒸馏到空闲专家）或运行时专家融合来弥补，是值得探索的方向。

5. **与训练侧优化的协同**：容量感知推理与训练阶段的负载均衡损失是否可以联合优化？例如，在训练时引入容量感知的令牌丢弃作为数据增强，使模型提前适应推理时的令牌丢弃模式，可能进一步缩小性能差距。

6. **长序列生成场景**：在自回归生成中，随着序列增长，令牌分布可能发生漂移，固定的容量系数可能不再适用。如何设计序列长度自适应的容量调度策略仍是一个开放问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/Capacity_Aware_Inference_Mitigating_the_Straggler_Effect_in_Mixture_of_Experts.pdf]]
