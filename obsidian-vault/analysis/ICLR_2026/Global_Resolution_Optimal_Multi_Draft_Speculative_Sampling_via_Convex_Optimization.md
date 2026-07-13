---
title: "Global Resolution: Optimal Multi-Draft Speculative Sampling via Convex Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Global_Resolution_Optimal_Multi_Draft_Speculative_Sampling_via_Convex_Optimization.pdf
project_link: null
code_link: null
openreview_forum_id: gpsczXOsHn
aliases:
- GR
- GROMDSSCO
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "通过互补松弛性将 OTLP 分解为相互独立的内、外系统，并利用子模函数与多面体理论将外系统简化为 O(V log V) 的残差计算，再通过截断凸函数直接求解运输计划参数，从而将指数规模问题转化为可高效近似求解的凸优化。"
primary_logic: "最优运输的验证准则可以由一个低维的 softmax 参数化形式表达，而这些参数可以通过最小化对应的凸函数获得；配合对最优子集 H* 的快速计算和多面体外残差算法，整个算法在保证任意精度的同时实现大幅提速。"
claims:
- "OTLP 可以通过最大流网络精确求解，但网络规模巨大；进一步引入互补松弛性可将网络拆分为仅依赖子集 H* 的内、外系统。"
- "利用多面体理论和子模最小化，外系统残差 p_i 可以在 O(V log V) 时间内求出闭式解。"
- "内、外系统的运输变量可由凸函数 Φ_T 和 Θ_T 的梯度下降求解，并可任意选择截断集 T 来逼近全局最优，误差由 ε_T 和 γ_T 控制。"
- "在 Llama-3 和 Gemma-2 实验中，全局分辨率算法在 100 ms/token 的时间预算内实现了超过 90% 的最优接受率，比通用 LP 或最大流求解器快四个数量级以上。"
---

# Global Resolution: Optimal Multi-Draft Speculative Sampling via Convex Optimization

> [!tip] 核心洞察
> 最优运输的验证准则可以由一个低维的 softmax 参数化形式表达，而这些参数可以通过最小化对应的凸函数获得；配合对最优子集 H* 的快速计算和多面体外残差算法，整个算法在保证任意精度的同时实现大幅提速。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 全局分辨率：通过凸优化的最优多草案投机采样 |
| 英文题名 | Global Resolution: Optimal Multi-Draft Speculative Sampling via Convex Optimization |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=gpsczXOsHn) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Global Resolution |
| Dataset | Llama-3 70B/8B (top‑k i.i.d. drafting), Llama-3 70B/8B (time limit 10 ms/token), Gemma‑2 27B/2B (multi‑step SpecTr) |

> [!tip] 效果简介
> - Llama-3 70B/8B (top‑k i.i.d. drafting) 上，solve time (ms/token) for (k=10, n=5) 为 70.75 (τ=1e‑3) / 99.69 (τ=1e‑4)，对比 General LP > 400000，变化 ~400000× 加速。
> - Llama-3 70B/8B (time limit 10 ms/token) 上，acceptance rate (%) 为 85.65 (τ=1e‑3) / 85.10 (τ=1e‑4)，对比 ≤ 83.94 (best other solver)，变化 +1.71% / +1.16%。
> - Gemma‑2 27B/2B (multi‑step SpecTr) 上，walltime speedup (over vanilla) 为 1.98× (K=4, L=8)，对比 1.0，变化 +98%。

## 概要

**问题瓶颈**：多草案投机采样（multi‑draft speculative sampling）的验证准则本质上是一个最优传输线性规划（OTLP），其变量规模随词汇表大小 $V$ 和草案数 $n$ 呈指数增长（$V^{n+1}$），导致无法直接存储或求解。现有方法要么退化为启发式近似，要么依赖通用 LP/最大流求解器，在毫秒级单 token 时间预算内远不能达到最优接受率。

**核心思路**：本文提出 **Global Resolution** 算法，通过三条理论路径将指数规模的 OTLP 压缩为低维凸优化问题：
1. **互补松弛分解**：将松弛 OTLP 的解分解为相互独立的内、外系统，使问题仅依赖最优子集 $H^*$。
2. **多面体残差计算**：利用子模函数最小化和多面体理论，在 $O(V \log V)$ 时间内求出外系统的残差闭式解。
3. **截断凸优化**：将运输计划参数化为 softmax 形式，通过最小化截断凸函数 $\Phi_T$ 和 $\Theta_T$ 获得近似解，误差由截断集 $T$ 和阈值 $\tau$ 严格控制。

**方法定位**：Global Resolution 属于多草案投机采样的最优验证准则求解器，其上游依赖 i.i.d. 草案生成（如 top‑k 采样），下游输出运输计划以指导重要性采样。与 **K‑SEQ**（Sun et al., 2023）、**MSS**（Miao et al., 2024）、**RSD**（Jeon et al., 2024）等启发式方法以及 **LP with vocabulary truncation**（Khisti et al., 2025）不同，Global Resolution 首次在可证明误差界内逼近全局最优 OTLP 解。

**主要结果**：
- 在 Llama‑3 70B/8B 上，Global Resolution 以 $\tau = 10^{-3}$ 实现 70.75 ms/token 的求解时间，比通用 LP 求解器快约四个数量级（>400,000 ms/token）。
- 在 10 ms/token 的严格时间预算下，Global Resolution 的接受率达 85.65%，比最佳对比求解器高 1.71 个百分点。
- 在 Gemma‑2 27B/2B 的多步 SpecTr 框架中，Global Resolution 实现 1.98× 的墙上时间加速。

**局限与开放问题**：当前算法严格依赖 i.i.d. 草案假设，对非 i.i.d. 草案（如不替换采样或独立不同草案）的子模最小化步骤缺乏高效实现；截断集大小受限于 L‑BFGS‑B 的迭代代价，在高温或大 $(k,n)$ 组合下失败率升高。如何为非 i.i.d. 草案设计可证近似的多面体算法，以及失败时自动切换至混合策略，是后续工作的关键方向。

### 投机采样与多草案验证

大语言模型的自回归解码受限于内存带宽，每生成一个 token 都需要加载全部模型参数。投机采样通过“草稿‑验证”两阶段框架突破这一瓶颈：先用轻量草稿模型生成一组候选 token，再用目标模型并行验证，仅接受与目标分布一致的草稿 token，从而在不改变输出分布的前提下实现加速。

当草稿模型一次生成 $n$ 条草稿序列时，验证阶段面临一个核心问题——如何从 $n$ 条草稿中最大化接受的 token 数量。这一问题被形式化为**最优传输线性规划**（Optimal Transport Linear Program, OTLP）：

$$\max_{C \geq 0} \sum_{i \in \mathcal{V}} \sum_{\bar{i} \in A_i} C_{i,\bar{i}} \quad \text{s.t.} \quad \sum_{\bar{i} \in \mathcal{V}^n} C_{i,\bar{i}} = p(i) \; \forall i, \; \sum_{i \in \mathcal{V}} C_{i,\bar{i}} = p_{\mathrm{draft}}(\bar{i}) \; \forall \bar{i}$$

其中 $p(i)$ 为目标模型在 token $i$ 上的概率，$p_{\mathrm{draft}}(\bar{i})$ 为草稿序列 $\bar{i}$ 的联合概率，$A_i$ 为包含 token $i$ 的草稿序列集合。OTLP 直接优化接受率，但变量数量为 $V^{n+1}$（$V$ 为词汇表大小），随 $n$ 指数增长。

### 现有方法的根本瓶颈

已有的多草案验证方法可归为两类：

- **启发式近似**：如 **K-SEQ**（Sun et al., 2023）、**MSS**（Miao et al., 2024）、**RSD**（Jeon et al., 2024）等方法采用贪心或序列化策略，在计算效率与最优接受率之间存在显著差距。
- **精确求解器**：将 OTLP 或其松弛形式转化为最大流网络，或使用通用线性规划求解器直接求解。然而，即使是最优化的最大流实现，网络规模仍随 $n$ 和 $V$ 急剧膨胀，单 token 求解时间远超实际部署可承受的毫秒级预算。

**核心瓶颈在于**：OTLP 的变量数量 $V^{n+1}$ 使得任何直接求解思路都无法在存储和计算上可行。即使将等式约束松弛为不等式，得到松弛形式：

$$\max_{S \geq 0} \sum_{i \in \mathcal{V}} \sum_{\bar{i} \in \mathcal{V}^n} S_{i,\bar{i}} \quad \text{s.t.} \quad \sum_{\bar{i}} S_{i,\bar{i}} \leq p(i), \; \sum_{i} S_{i,\bar{i}} \leq p_{\mathrm{draft}}(\bar{i}), \; S_{i,\bar{i}}=0 \; \forall \bar{i}\notin A_i$$

问题规模并未实质性缩小。近期工作（Khisti et al., 2025）尝试通过截断词汇表来压缩规模，但截断本身引入的误差缺乏可证界，且无法从根本上消除指数依赖。

### 子集选择视角的启示

Hu et al.（2025）的一个重要发现为突破这一瓶颈提供了线索：最优接受率 $\alpha^*$ 可以通过一个子集选择问题精确计算：

$$\alpha^* = 1 + \min_{H \subseteq \mathcal{V}} \psi(H), \quad \psi(H) = \sum_{i \in H} p(i) - \sum_{\bar{i} \in H^n} p_{\mathrm{draft}}(\bar{i})$$

这一形式将指数规模的 OTLP 转化为对词汇子集 $H$ 的优化。对于 i.i.d. 草稿采样，$\psi(H)$ 具有子模性质，可在 $O(V \log V)$ 内通过排序精确求解。然而，该结果仅给出了最优接受率的**数值**，并未提供达到该接受率的**运输计划**（即验证时的具体接受/拒绝决策）。

### 本文动机

上述进展揭示了一个关键缺口：能否从子集选择的最优解 $H^*$ 出发，反向重构出完整的运输计划，同时避免回到指数规模的原始 OTLP？本文的核心动机正是填补这一缺口——通过建立子集选择、互补松弛性与多面体理论之间的深层联系，将指数规模的 OTLP 分解为两个仅依赖低维参数的凸优化问题，从而在保证任意精度的前提下，将求解时间压缩至实际可用的毫秒级。

## 核心方法与创新机理

### 创新动机：从指数灾难到可解规模

多草案投机采样的最优传输线性规划（OTLP）直接刻画了目标与草稿分布间的最大耦合，但其变量数量随词汇表大小 $V$ 与草案数 $n$ 呈 $V^{n+1}$ 指数增长，导致任何通用求解器均无法在单 token 毫秒级延迟内完成求解。已有近似方法（如 K‑SEQ、MSS、RSD）通过启发式绕过 OTLP，但无法逼近真实最优接受率；而词汇截断的 LP 近似（Khisti et al., 2025）虽缩小了规模，却丢失了全局最优性保证。**核心瓶颈**在于：OTLP 的指数规模使“计算最优验证准则”这一目标在工程上不可行。

### 关键洞察：互补松弛分解与低维参数化

本文的核心洞察是：OTLP 的最优解可以通过**互补松弛性**（Theorem 5.1）被拆解为两个相互独立的子系统——仅依赖最优子集 $H^*$ 的“内系统”和仅依赖其补集的“外系统”。这一分解将指数规模的耦合约束转化为两个可独立求解的部分，且每个部分的运输变量均可由一个**低维 softmax 参数化形式**表达。具体而言，外系统变量满足 $S_{i,\bar{i}} = \frac{e^{\alpha_i}}{\sum_{j \in \text{set}(\bar{i}) \setminus H^*} e^{\alpha_j}} \cdot p_{\text{draft}}(\bar{i})$，内系统变量满足类似形式。这些参数 $\alpha_i$ 可通过最小化对应的**截断凸函数** $\Phi_T$ 和 $\Theta_T$ 获得，从而将 OTLP 转化为一个变量数至多为 $V$ 的凸优化问题。

### Changed Slots：相对 Baseline 的核心变化

| 变化维度 | Baseline 做法 | 本文方案 | 核心机制 |
|:---|:---|:---|:---|
| **求解运输计划的方式** | 直接求解原始 OTLP（指数规模）或使用启发式近似 | 先求子集 $H^*$，再用多面体求外残差，最后通过凸优化得到 softmax 形式的运输计划 | 互补松弛分解 + 截断凸函数最小化（Section 5.1, 6.1, 6.2, Algorithm 1） |
| **外层系统的残差计算** | 必须求解完整的松弛 LP 或通过最大流网络 | 利用子模函数最小化和多面体算法，在 $O(V \log V)$ 内直接计算 $p_i$ 闭式解 | 连续差分子模最小值 + 多面体理论（Theorem 6.2, Lemma 6.3） |
| **求解器的精度与代价控制** | 受限于硬件，常无法在毫秒级内给出解 | 通过截断集 $T$ 动态平衡误差与代价，可证明误差 $\leq 15\tau$ 且接受率偏离 $\leq 10\tau$ | 截断集选取 + 近似保证（Lemma 6.6, Section 6.3） |

**Slot 1 的深层机制**：互补松弛性将松弛 OTLP 的约束条件重构为内、外两个独立的最大流问题（Theorem 5.1, Equations 6a–6c）。内系统处理 $H^*$ 内的 token，外系统处理 $H^*$ 外的 token，两者间无交叉约束。这一分解使得每个子系统仅需优化至多 $V$ 个变量，而非原始的 $V^{n+1}$ 个。

**Slot 2 的深层机制**：外系统的残差 $p_i = p(i) - \sum_{\bar{i}} S_{i,\bar{i}}^*$ 并非通过求解线性系统获得，而是利用 $\psi(H)$ 的**子模性**（submodularity）和**多面体理论**（polymatroid theory）直接计算。具体而言，将 $V \setminus H^*$ 中的元素按某种顺序排列后，$p_{v_i}$ 可表示为连续前缀子集上 $\psi$ 最小值的差分（Theorem 6.2）。由于 $\psi$ 在 i.i.d. 草稿下具有 $q$-凸性，该最小值可通过排序在 $O(V \log V)$ 内求得（Lemma 6.3），完全避开了显式构建和求解线性系统。

**Slot 3 的深层机制**：截断集 $T$ 控制了凸优化的规模与精度的权衡。外系统截断函数 $\Phi_T$ 仅对 $\bar{i} \in (H^* \cup T)^n \setminus (H^*)^n$ 的草稿项求和，内系统截断函数 $\Theta_T$ 仅对 $\bar{i} \in T^n$ 的草稿项求和。当 $T$ 较小时，凸函数维度低、优化快，但引入的截断误差 $\varepsilon_T$ 或 $\gamma_T$ 较大；当 $T$ 扩大至全集时，误差归零，但优化代价上升。Algorithm 1 选择满足 $\varepsilon_T \leq \tau$ 和 $\gamma_T \leq \tau$ 的最小 $T$，并由 Lemma 6.6 保证最终的运输计划 $C$ 对 OTLP 约束的总 $L_1$ 偏离不超过 $15\tau$，接受率偏离不超过 $10\tau$。

### 方法谱系与知识库定位

本文的方法建立在两条近期工作的交汇点上：
- **子集选择公式**（Hu et al., 2025）：将最优接受率 $\alpha^*$ 的计算转化为 $\min_{H \subseteq \mathcal{V}} \psi(H)$，并证明对于 i.i.d. 草稿可通过排序在 $O(V \log V)$ 内求解 $H^*$。本文直接继承该公式作为计算 $H^*$ 的基础模块。
- **规范分解**（Khisti et al., 2025）：将 OTLP 的解重构为重要性采样参数 $\beta(i|\bar{i})$ 的优化问题。本文证明该 $\beta$-优化与松弛 OTLP 在数学上等价（Theorem 4.1），从而将规范分解的框架纳入自身的理论体系。

在此基础上，本文引入两项此前未被用于投机采样的理论工具：
- **多面体理论**：用于外系统残差的闭式求解，将原本需要线性规划的步骤转化为子模最小化的差分计算。
- **截断凸优化**：用于内、外系统运输变量的参数化求解，将指数规模的耦合约束松弛为可独立优化的 softmax 参数。

与直接使用通用 LP 求解器或最大流求解器相比，全局分辨率算法在 Llama-3 70B/8B 的 $(k=10, n=5)$ 配置下实现了约四个数量级的加速（70.75 ms/token vs. >400000 ms/token，Table 1），同时在 10 ms/token 的时间预算下将接受率从 83.94% 提升至 85.65%（Table 2）。在 Gemma-2 27B/2B 的多步 SpecTr 框架中，该方法实现了 1.98× 的墙上时间加速（Table 4）。

**证据强度评估**：互补松弛分解（Theorem 5.1）和外系统闭式解（Theorem 6.2）均有严格数学证明支撑，置信度极高；截断凸函数的近似保证（Lemma 6.6）提供了误差上界，但截断集选取的“最小 $T$”策略在部分 $(k,n)$ 组合下可能导致优化器无法在时间预算内收敛（失败率上升，Figure 5），这是算法的主要失效模式。当前算法严格依赖 i.i.d. 草稿假设以维持 $\psi$ 的子模性和 $q$-凸性；对于非 i.i.d. 草稿方案，子模最小化步骤缺乏高效实现（Table 5），这是向更广泛草稿策略扩展的主要障碍。

Global Resolution 求解器的核心思路是将原始指数规模的 OTLP（变量数量为 $V^{n+1}$）分解为三个可高效求解的独立模块，最终通过凸优化在任意精度下重构出近似最优的运输计划。整个 pipeline 的输入为目标分布 $p(i)$、草稿分布 $p_{\text{draft}}(\bar{i})$ 以及可接受集 $A_i$，输出为满足 OTLP 约束的运输计划 $C_{i,\bar{i}}$，其接受率可在给定误差阈值 $\tau$ 内逼近理论最优值 $\alpha^*$。

### 模块一：计算最优子集 $H^*$

该模块是整个分解的基础。根据子集选择理论（Theorem 3.1, Hu et al., 2025），最优接受率可表达为 $\alpha^* = 1 + \min_{H \subseteq \mathcal{V}} \psi(H)$，其中 $\psi(H) = \sum_{i \in H} p(i) - \sum_{\bar{i} \in H^n} p_{\text{draft}}(\bar{i})$。对于 i.i.d. 草稿采样，$\psi$ 具有 $q$-凸性，使得 $H^*$ 可在 $O(V \log V)$ 时间内通过排序直接确定（Lemma 6.3）。$H^*$ 的作用在于将词汇表划分为内、外两个互不耦合的子系统：$i \in H^*$ 的 token 进入内系统，$i \notin H^*$ 的 token 进入外系统。这一划分是后续互补松弛性成立的前提。

### 模块二：计算外残差 $p_i$

外系统的核心是确定每个 $i \notin H^*$ 在最优解中实际被运输的质量 $p_i \leq p(i)$。利用多面体理论（polymatroid theory），外残差 $p_i$ 存在闭式解，可通过连续差分子模函数 $\psi$ 在不同前缀集上的最小值得到（Theorem 6.2）。具体而言，将 $\mathcal{V} \setminus H^*$ 按任意顺序排列后，$p_i$ 等于相邻前缀集上 $\psi$ 最小值的差分。该步骤的复杂度为 $O(V \log V)$，且与后续凸优化完全解耦。求得的 $p_i$ 直接作为外系统凸函数 $\Phi_T$ 中的常数项输入。

### 模块三：构建截断集并最小化凸函数

内、外系统各自对应一个凸函数 $\Theta_T$ 和 $\Phi_T$，其变量为低维参数 $\alpha_i$，数量不超过 $V$。这两个凸函数的形式源于 softmax 参数化：将运输变量表达为 $S_{i,\bar{i}} \propto e^{\alpha_i} \cdot p_{\text{draft}}(\bar{i})$ 后，互补松弛条件等价于对应凸函数的梯度接近零（Theorem 6.4, 6.5）。为控制计算代价，算法根据误差阈值 $\tau$ 选择最小的截断集 $T$，使得截断误差 $\varepsilon_T \leq \tau$（外系统）或 $\gamma_T \leq \tau$（内系统），然后使用 L‑BFGS‑B 求解器最小化截断后的凸函数。截断集大小决定了优化变量的实际维度，从而在精度与速度之间实现动态平衡。

### 模块四：重构运输计划

从凸优化得到的参数 $\alpha_i$ 出发，通过 softmax 公式重构内、外系统的运输变量 $S_{i,\bar{i}}$。最后，利用残差概率 $p^{\text{res}}(i) = p(i) - p_i$ 和草稿残差 $p_{\text{draft}}^{\text{res}}(\bar{i})$，通过自举项将内、外解拼接为完整的 OTLP 运输计划 $C_{i,\bar{i}}$（Equation 18）。Lemma 6.6 保证该近似解的约束违反量和接受率偏差均被 $\tau$ 的常数倍所控制。

### 输入输出流总结

| 阶段 | 输入 | 输出 | 核心操作 |
|------|------|------|----------|
| 子集选择 | $p(i)$, $p_{\text{draft}}(\bar{i})$ | $H^*$ | 排序求 $\min \psi(H)$ |
| 外残差 | $H^*$, $\psi$ | $p_i$ ($i \notin H^*$) | 多面体差分闭式解 |
| 凸优化 | $H^*$, $p_i$, $\tau$ | $\alpha_i$ | L‑BFGS‑B 最小化 $\Phi_T$ / $\Theta_T$ |
| 重构 | $\alpha_i$, $p_i$, 残差 | $C_{i,\bar{i}}$ | softmax + 残差自举 |

整个 pipeline 的瓶颈在于凸优化步骤，其代价由截断集大小 $|T|$ 决定。实验表明，在 $\tau = 10^{-3}$ 的设置下，Global Resolution 在 Llama-3 上的平均求解时间为 70.75 ms/token（$k=10, n=5$），相比通用 LP 求解器加速约四个数量级（Table 1），同时接受率达到 85.65%，超过所有对比求解器（Table 2）。

### 问题形式化：从 OTLP 到子集选择

多草案投机采样的最优验证准则可形式化为最优传输线性规划（OTLP）。设目标分布为 $p(i)$，草稿模型联合分布为 $p_{\mathrm{draft}}(\bar{i})$，其中 $\bar{i} \in \mathcal{V}^n$ 表示 $n$ 个草稿 token 的序列，$A_i$ 为包含 token $i$ 的草稿序列集合。原始 OTLP 直接最大化接受率：

$$\max_{C \geq 0} \sum_{i \in \mathcal{V}} \sum_{\bar{i} \in A_i} C_{i,\bar{i}} \quad \text{s.t.} \quad \sum_{\bar{i} \in \mathcal{V}^n} C_{i,\bar{i}} = p(i) \;\forall i,\; \sum_{i \in \mathcal{V}} C_{i,\bar{i}} = p_{\mathrm{draft}}(\bar{i}) \;\forall \bar{i}$$

该问题的变量数量为 $V^{n+1}$，随词汇表大小指数增长，无法直接存储或求解。为此，引入松弛 OTLP，将等式约束放宽为不等式：

$$\max_{S \geq 0} \sum_{i \in \mathcal{V}} \sum_{\bar{i} \in \mathcal{V}^n} S_{i,\bar{i}} \quad \text{s.t.} \quad \sum_{\bar{i}} S_{i,\bar{i}} \leq p(i),\; \sum_{i} S_{i,\bar{i}} \leq p_{\mathrm{draft}}(\bar{i}),\; S_{i,\bar{i}}=0 \;\forall \bar{i}\notin A_i$$

松弛 OTLP 的最优解 $S^*$ 可通过残差构造恢复为原始 OTLP 的解 $C^*$：

$$C^*_{i,\bar{i}} = S^*_{i,\bar{i}} + \frac{p^{\mathrm{res}}(i) \cdot p_{\mathrm{draft}}^{\mathrm{res}}(\bar{i})}{\sum_{j \in \mathcal{V}} p^{\mathrm{res}}(j)}$$

其中 $p^{\mathrm{res}}(i) = p(i) - \sum_{\bar{i}} S^*_{i,\bar{i}}$，$p_{\mathrm{draft}}^{\mathrm{res}}(\bar{i}) = p_{\mathrm{draft}}(\bar{i}) - \sum_i S^*_{i,\bar{i}}$ 分别为运输后的目标与草稿残差概率。

进一步，最优接受率 $\alpha^*$ 可通过子集选择形式计算（Hu et al., 2025）：

$$\alpha^* = 1 + \min_{H \subseteq \mathcal{V}} \psi(H), \quad \psi(H) = \sum_{i \in H} p(i) - \sum_{\bar{i} \in H^n} p_{\mathrm{draft}}(\bar{i})$$

对于 i.i.d. 草稿采样，$\psi$ 具有 $q$-凸性，使得最优子集 $H^*$ 可在 $O(V \log V)$ 时间内通过排序确定。

### 互补松弛分解：内外系统解耦

全局分辨率算法的核心突破在于利用互补松弛性将指数规模的松弛 OTLP 分解为两个独立的小规模系统。**Theorem 5.1** 建立了最优解 $S^*$ 的充要条件：任意非负矩阵 $S^*$ 满足以下系统当且仅当它是松弛 OTLP 的最优解。

**外层系统**（处理 $i \notin H^*$ 和 $\bar{i} \notin (H^*)^n$）：

$$\sum_{\bar{i} \notin (H^*)^n} S_{i,\bar{i}}^* \leq p(i) \quad \forall i \notin H^*, \quad \sum_{i \notin H^*} S_{i,\bar{i}}^* = p_{\mathrm{draft}}(\bar{i}) \quad \forall \bar{i} \notin (H^*)^n$$

**内层系统**（处理 $i \in H^*$ 和 $\bar{i} \in (H^*)^n$）：

$$\sum_{\bar{i} \in (H^*)^n} S_{i,\bar{i}}^* = p(i) \quad \forall i \in H^*, \quad \sum_{i \in H^*} S_{i,\bar{i}}^* \leq p_{\mathrm{draft}}(\bar{i}) \quad \forall \bar{i} \in (H^*)^n$$

**零变量条件**：$S_{i,\bar{i}}^* = 0$ 对所有 $i \in H^*, \bar{i} \notin (H^*)^n$ 以及所有 $\bar{i} \notin A_i$ 成立。

内外系统相互独立，各自可视为二分图上的最大流问题，但变量规模已从 $V^{n+1}$ 降至仅涉及 $H^*$ 或 $\mathcal{V} \setminus H^*$ 的部分。

### 外残差闭式解：多面体理论加速

外层系统的核心是求解残差 $p_i = p(i) - \sum_{\bar{i} \notin (H^*)^n} S_{i,\bar{i}}^*$（$i \notin H^*$）。**Theorem 6.2** 利用多面体理论给出了闭式解。将 $\mathcal{V} \setminus H^*$ 中元素按某种顺序排列为 $v_1, \ldots, v_k$，定义 $H_i = H^* \cup \{v_i, \ldots, v_k\}$，则：

$$p_{v_i} = p(v_i) + \min_{T \supseteq H_{i+1}} \psi(T) - \min_{T \supseteq H_i} \psi(T) \quad \forall i \in [k]$$

其中子模函数 $\psi$ 在约束区间上的最小值可通过排序在 $O(V \log V)$ 内计算。**Lemma 6.3** 进一步指出，由于 $H^*$ 外的排序可任意选择，整体外残差计算可优化至 $O(V \log V)$。

### 凸优化求解运输变量：截断 softmax 参数化

获得外残差 $p_i$ 后，需分别求解内外系统的运输变量 $S_{i,\bar{i}}$。全局分辨率发现这些变量可由低维 softmax 参数化形式表达，参数通过最小化对应的凸函数获得。

**外层凸求解器**（**Theorem 6.4**）：对截断集 $T \subseteq \mathcal{V} \setminus H^*$，定义凸函数：

$$\Phi_T((\alpha_i)) = \sum_{\bar{i} \in (H^* \cup T)^n \setminus (H^*)^n} p_{\mathrm{draft}}(\bar{i}) \log\left(\sum_{i \in \mathrm{set}(\bar{i}) \setminus H^*} e^{\alpha_i}\right) - \sum_{i \in T} p_i \alpha_i$$

当梯度接近零时，对应的 softmax 变量 $S_{i,\bar{i}} = \frac{e^{\alpha_i}}{\sum_{j \in \mathrm{set}(\bar{i}) \setminus H^*} e^{\alpha_j}} \cdot p_{\mathrm{draft}}(\bar{i})$ 满足外系统约束，误差由 $\varepsilon_T$ 控制。

**内层凸求解器**（**Theorem 6.5**）：对截断集 $T \subseteq H^*$，定义凸函数：

$$\Theta_T((\alpha_i)) = \sum_{\bar{i} \in T^n} p_{\mathrm{draft}}(\bar{i}) \log\left(1 + \sum_{i \in \mathrm{set}(\bar{i})} e^{\alpha_i}\right) - \sum_{i \in T} p(i) \alpha_i$$

同样通过最小化获得满足内系统约束的 softmax 解，误差由 $\gamma_T$ 控制。

### 精度控制与截断策略

截断集 $T$ 的大小决定了凸优化的代价与精度。**Algorithm 1** 根据目标误差阈值 $\tau$ 自适应选择最小 $T$，使得 $\gamma_T \leq \tau$（内层）且 $\varepsilon_T \leq \tau$（外层），随后使用 L‑BFGS‑B 求解器最小化对应的凸函数。**Lemma 6.6** 给出了近似保证：最终构造的运输计划 $C$ 在 OTLP 等式约束上的总 $L_1$ 偏差不超过 $\alpha + 2\beta$，最优接受率偏差不超过 $\alpha + \beta$，其中 $\alpha, \beta$ 为求解器误差。实际中取 $\tau = 10^{-3}$ 或 $10^{-4}$ 即可在毫秒级时间内达到超过 90% 的最优接受率。

## 实验与关键发现

### 核心发现：求解速度与接受率的双重突破

全局分辨率算法在求解速度上实现了对传统 OTLP 求解器的压倒性优势。在 Llama-3 70B/8B 模型对上，针对典型配置 (k=10, n=5)，全局分辨率在 τ=1e-3 精度下的平均单 token 求解时间仅为 **70.75 ms**，而通用线性规划求解器（General LP）需要超过 400,000 ms，加速比达到约四个数量级（Table 1）。即使将精度提升至 τ=1e-4，求解时间也仅增至 99.69 ms，仍远低于其他任何基线方法。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_gpsczXOsHn/figures/002_Table_1.jpg]]
*Table 1: Further, in Appendix O, we compare these acceptance rates to those for the greedy construction by Hu et al. (2025), described at the start of Section 5. For both Gemma-2 and Llama-3, we find that i.i.d. acceptance rates are higher than greedy for k $\geq$ 1 0 0 , with improvements near 2% for larger k and n. Table 1: Average Llama-3 solve times (ms/token) over k , n , for the five i.i.d. OTLP solvers. General LP and max-flow are baselines, and optimized max-flow and global resolution ( $\tau$ = 1 $0 ^ { - 3 }$ , 1 $0 ^ { - 4 }$ ) are ours. Lower numbers are better. Red numbers are lower bounds from small scale tests due to excessive runtime. Global resolution can be 10,000+ times faster than others...

在严格的时延约束下，全局分辨率的接受率优势同样显著。当单 token 时间预算限制为 10 ms 时，Llama-3 上全局分辨率（τ=1e-3）实现了 **85.65%** 的接受率，比表现最好的基线求解器高出 1.71 个百分点；在 100 ms 预算下，该优势仍保持在 1.03 个百分点（Table 2）。这表明算法在极低时延场景中能更充分地逼近理论最优接受率。

### 多步推理中的墙上时间加速

在基于 SpecTr 框架的多步推理实验中，全局分辨率展现出可观的端到端加速效果。在 Gemma-2 27B/2B 模型对上，当使用 K=4 条独立同分布草稿路径、每步生成 L=8 个 token 时，全局分辨率实现了 **1.98×** 的墙上时间加速比（Table 4）。对应的块效率（每次调用目标模型生成的 token 数）随 K 增加而提升，验证了算法在多步场景中的有效性。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_gpsczXOsHn/figures/009_Table_4.jpg]]
*Table 4: Block efficiency (number of decoded tokens per call to target model) in and walltime speedup (over vanilla autoregressive decoding) for SpecTr with global resolution under different values of K (number of i.i.d. paths). Experiments are run on Gemma-27B/2B with L = 8*

### 草稿策略与参数的影响

**i.i.d. vs greedy 草稿策略**：实验系统比较了独立同分布（i.i.d.）草稿与贪心草稿策略的最优接受率。在 Gemma-2 和 Llama-3 上，当 top-k 采样的 k≥100 时，i.i.d. 策略的接受率全面优于贪心策略，尤其在草稿数量 n≥4 时优势接近 2 个百分点（Figure 2, Figure 3）。这一发现为草稿策略的选择提供了明确的指导。

**k 与 n 的边际收益**：增大 top-k 的 k 值和草稿数量 n 均能单调提升最优接受率，但存在明显的边际递减效应。当 k 超过 1000 后，进一步提升带来的接受率增益趋于饱和（Figure 1）。这意味着在实际部署中，选择适中的 k 值即可在计算开销与接受率之间取得良好平衡。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_gpsczXOsHn/figures/001_Figure_1.jpg]]
*Figure 1: Optimal acceptance rates from n i.i.d drafts with top-k sampling with n with target/draft pairs of Gemma-2 27B/2B and Llama-3 70/8B. Increasing k improves acceptance rate significantly up to k = 1 0 0 0 , and increasing n also results in steady increase in optimal acceptance*

### 温度对算法鲁棒性的影响

目标模型的温度是影响全局分辨率性能的关键外部因素。实验表明，当温度降低至 0.2-0.4 区间时，仅需 k=10 的 top-k 草稿即可达到接近最优的接受率，进一步增大 k 的收益极小（Figure 4）。更重要的是，全局分辨率在低温下的**失败率显著降低**——失败指算法因无法在截断集 T 内达到目标误差 τ 而提前终止（Figure 5）。当温度超过 0.6 后，失败率开始上升，这构成了算法的一个明确使用边界：**推荐在低温（<0.6）或小 k 场景下使用以获得最佳可靠性**。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_gpsczXOsHn/figures/007_Figure_4.jpg]]
*Figure 4: Optimal acceptance rates from n i.i.d drafts with top-k sampling with n with the target/draft pair Gemma-2 27B/2B, for various target temperature settings (0.2, 0.4, 0.6, 0.8). Until temperature 0.8, increasing k past 10 results in little acceptance gains for reasonable values of n*

### 消融实验的关键结论

1. **截断集 T 的精度-代价权衡**：τ 从 1e-3 收紧至 1e-4 时，求解时间增加约 40%，但接受率提升有限（在 10 ms 预算下反而略有下降），说明在实际应用中 τ=1e-3 已能提供足够好的近似。

2. **求解器失败模式**：通用 LP 和最大流求解器在多数 (k,n) 配置下因超时而失败，而全局分辨率仅在高温或极端参数组合下出现失败，且失败率可通过调整 τ 或 T 的大小来控制。

3. **非 i.i.d. 草稿的扩展可行性**：Table 5 的定性分析指出，全局分辨率的子模最小化步骤严格依赖 i.i.d. 假设，对于不替换采样或 n≥3 时的独立不同草稿，该步骤缺乏高效实现，这是算法当前的主要局限。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_gpsczXOsHn/figures/010_Table_5.jpg]]
*Table 5: Extending global resolution to three non-i.i.d. drafting regimes. Yes means the extension is immediate; Possible means it requires some work; No means there is a major obstacle*

### 证据强度说明

上述结论中，求解时间与接受率的定量对比（Table 1, Table 2）基于同一 CPU 环境下的公平比较，且记录了各求解器的成功/失败率，证据强度高。温度影响和草稿策略对比（Figure 2-5）基于多组参数扫描，结论方向一致，但具体数值可能因模型对而异，建议在实际部署前进行验证。多步加速比（Table 4）仅在 Gemma-2 单对模型上测试，泛化性需进一步确认。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_gpsczXOsHn/figures/003_Table.jpg]]
*Table: average runtime falls under the time limit. For Llama-3, global resolution with \tau = 0 . 0 0 1 and \tau = 0 . 0 0 0 1 achieve 1.03% and 0.47% higher acceptances than the other solvers for 100 ms/token, and 1.71% and 1.16% higher acceptances for 10 ms/token. While the improvements for Gemma-2 are smaller, they are significant. Thus, global resolution is the state-of-the-art OTLP solver*

## 定位与知识库关联

### 1. 问题根源：多草案投机采样的指数规模瓶颈

多草案投机采样的核心挑战在于求解最优传输线性规划（OTLP）：给定目标模型分布 $p(i)$ 和 $n$ 个草稿的联合分布 $p_{\text{draft}}(\bar{i})$，需要找到一个传输计划 $C_{i,\bar{i}}$ 最大化接受率。原始 OTLP 的变量规模为 $V^{n+1}$（$V$ 为词汇表大小），即使对中等规模的模型也完全无法存储或求解。这一瓶颈使得所有现有方法都必须在准确性与计算代价之间做出妥协。

### 2. 方法演进脉络

#### 2.1 从启发式到可证近似

早期多草案方法采用简单的接受准则，如**MSS**（Miao et al., 2024）和**RSD**（Jeon et al., 2024），它们基于启发式规则而非全局优化，接受率远低于理论上界。**K-SEQ**（Sun et al., 2023）首次尝试近似求解 OTLP，但缺乏对解质量的严格保证。

#### 2.2 子集选择与 LP 松弛

Hu et al. (2025) 提出子集选择公式，将最优接受率 $\alpha^*$ 的计算转化为子模函数 $\psi(H) = \sum_{i \in H} p(i) - \sum_{\bar{i} \in H^n} p_{\text{draft}}(\bar{i})$ 的最小化问题。**Khisti et al. (2025)** 引入规范分解（canonical decomposition），将 OTLP 松弛为不等式约束形式，并通过词汇表截断缩小问题规模。本文证明这两种思路在数学上等价，均为松弛 OTLP 的不同表述。

#### 2.3 本文的突破：凸优化替代指数规模 LP

**Global Resolution** 的核心创新在于将松弛 OTLP 的求解从线性规划/最大流彻底转化为凸优化问题：

| 求解阶段 | 基线方法 | Global Resolution |
|---------|---------|-------------------|
| 求解最优子集 $H^*$ | 需遍历所有 $2^V$ 个子集或依赖通用 LP | 利用 $q$-凸性在 $O(V \log V)$ 内精确求解 |
| 外层残差 $p_i$ | 需完整求解最大流网络 | 基于多面体理论给出闭式解，$O(V \log V)$ |
| 运输变量 $S_{i,\bar{i}}$ | 直接求解 $V^{n+1}$ 变量 | 通过 softmax 参数化降维至 $V$ 个参数，L-BFGS-B 优化 |

这一方法谱系的关键转折点在于**互补松弛性**（Theorem 5.1）的引入：一旦确定 $H^*$，松弛 OTLP 的解被分解为完全独立的内、外两个子系统，每个系统仅涉及 $O(V)$ 而非 $V^{n+1}$ 级别的变量。

### 3. 与基线的定量对比

实验部分直接对比了五种求解器在 Llama-3 70B/8B 上的表现：

- **General LP Solver**：使用通用线性规划求解器求解原始 OTLP，作为准确性的理论上界，但求解时间超过 400,000 ms/token（对 $k=10, n=5$），完全不可实用。
- **Max-Flow OTLP Solver**：将松弛 OTLP 建模为最大流问题并用现成求解器求解，网络规模仍随 $n$ 指数增长。
- **Optimized Max-Flow**：本文改进的最大流求解器，利用 $H^*$ 跳过部分饱和边以减小网络规模，但仍远慢于 Global Resolution。
- **Global Resolution**（$\tau=10^{-3}$）：在 70.75 ms/token 内完成求解，比 General LP 快约 $4000\times$；在 10 ms/token 时间预算下接受率达到 85.65%，比最佳基线高 1.71 个百分点。

### 4. 适用边界与局限

#### 4.1 严格依赖 i.i.d. 草稿假设

当前算法的三个核心步骤——$H^*$ 的 $q$-凸性求解、外残差的多面体闭式解、内/外凸函数的构造——均建立在草稿为独立同分布（i.i.d.）采样的假设之上。对于非 i.i.d. 场景，Table 5 给出了定性分析：

- **不替换采样**：$H^*$ 的计算可扩展，但外残差和凸函数需要重新设计。
- **$n=2$ 独立不同草稿**：可扩展，但需额外工作。
- **$n \geq 3$ 独立不同草稿**：存在重大障碍，子模最小化步骤缺乏高效实现。

#### 4.2 温度敏感性与失败模式

Figure 5 揭示了算法在目标模型温度升高时的脆弱性：当温度超过 0.6 时，求解失败率显著上升。这是因为高温使分布更均匀，截断集 $T$ 需要更大才能满足误差阈值 $\tau$，而 L-BFGS-B 的迭代次数和内存限制了 $|T|$ 的上限。当前推荐在低温（$<0.6$）或小 $k$ 场景下使用以获得最佳可靠性。

#### 4.3 截断集选择的刚性

截断集 $T$ 的选取使用固定大小的硬限制，对某些 $(k,n)$ 组合可能无法达到目标误差 $\tau$ 而提前终止。误差由 $\varepsilon_T$ 和 $\gamma_T$ 控制，Lemma 6.6 证明接受率偏离不超过 $10\tau$，但实际失败意味着该 token 的加速完全丧失。

### 5. 开放问题

1. **非 i.i.d. 草稿的高效算法**：如何为 $n \geq 3$ 的独立不同草稿设计可证近似的子模最小化或多面体算法？这是扩展 Global Resolution 到更一般草稿策略的关键障碍。

2. **混合策略的自动切换**：当 Global Resolution 失败时，能否自动降级至 K-SEQ 或词汇截断等近似方法，以提升多步系统的整体稳健性？这需要在求解器中内嵌失败检测与策略选择逻辑。

3. **自适应截断集**：当前截断集大小由硬编码限制决定，是否可以通过自适应梯度信息或随机采样进一步降低凸函数的优化代价？这可能使算法在高温或大 $k$ 场景下保持可靠性。

4. **与 SpecTr 等框架的深度集成**：Table 4 显示在多步框架中 Global Resolution 实现了 1.98× 的墙上时间加速，但块效率（每调用一次目标模型解码的 token 数）仍有提升空间。如何在多步调度中更好地利用 Global Resolution 的精度优势？

## 原文 PDF

![[paperPDFs/ICLR_2026/Global_Resolution_Optimal_Multi_Draft_Speculative_Sampling_via_Convex_Optimization.pdf]]
