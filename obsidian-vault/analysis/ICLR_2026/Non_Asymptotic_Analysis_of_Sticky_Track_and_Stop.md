---
title: "Non-Asymptotic Analysis of (Sticky) Track-and-Stop"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Non_Asymptotic_Analysis_of_Sticky_Track_and_Stop.pdf
project_link: null
code_link: null
openreview_forum_id: vebqP5aioj
aliases:
- TSTSTSST
- NAASTS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/segmentation
core_operator: "通过定义序列 ‘好事件’ {E_t}，可有效控制经验均值的集中性，并利用 C-Tracking 的性质将停止规则近似为采样规则所积累的信息量，从而建立有限置信度下的停止时间上界。"
primary_logic: "在好事件发生的高概率下，TAS 和 S-TAS 的停止统计量可以被采样规则在每一步所积累的 max-min 信息量（形如 T^*(μ)^{-1}）加上次线性误差项下界，这直接导出了期望停止时间的非渐近上界。"
claims:
- "本文首次给出了 TAS 和 S-TAS 的非渐近上界。"
- "定理 1 明确给出了 TAS 的期望停止时间上界，包含与 δ 和 K 相关的项。"
- "在好事件下，C-Tracking 保证了经验分配近似于 oracle 权重，从而建立停止规则与采样规则的联系。"
- "在好事件发生的高概率下，TAS 和 S-TAS 的停止统计量可以被采样规则在每一步所积累的 max-min 信息量（形如 T^*(μ)^{-1}）加上次线性误差项下界，这直接导出了期望停止时间的非渐近上界。"
---

# Non-Asymptotic Analysis of (Sticky) Track-and-Stop

> [!tip] 核心洞察
> 在好事件发生的高概率下，TAS 和 S-TAS 的停止统计量可以被采样规则在每一步所积累的 max-min 信息量（形如 T^*(μ)^{-1}）加上次线性误差项下界，这直接导出了期望停止时间的非渐近上界。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | （粘性）跟踪与停止的非渐近分析 |
| 英文题名 | Non-Asymptotic Analysis of (Sticky) Track-and-Stop |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=vebqP5aioj) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/segmentation |
| Method | Track-and-Stop (TAS) 与 Sticky Track-and-Stop (S-TAS) 的非渐近分析 |
| Dataset |  |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

本文首次对 **Track-and-Stop (TAS)** 及其多答案扩展 **Sticky Track-and-Stop (S-TAS)** 两种固定置信度纯探索算法给出了非渐近的期望停止时间上界。此前的理论保证仅限于渐近最优性（当 $\delta \to 0$ 时），而本文回答了“在有限置信度 $\delta$ 下，这些算法的停止时间如何增长”这一开放问题。

**核心瓶颈**在于：TAS 在经验数据稀少时采样规则不稳定，而 S-TAS 因需处理多个候选答案，非渐近行为更加复杂。**关键分析手段**是通过定义序列“好事件” $\{\mathcal{E}_t\}$ 控制经验均值的集中性，并利用 C-Tracking 的性质将停止规则近似为采样规则所积累的信息量，从而在好事件发生的高概率下建立停止统计量的下界。

**方法定位**上，本文不提出全新算法，而是对已有 TAS 和 S-TAS 框架进行非渐近分析，并在实现层面引入经验均值投影（将 $\hat{\mu}(t)$ 投影到 $[\mu_{\min}, \mu_{\max}]^K$）以处理病态情形。分析依赖两个假设：$\sigma^2$-次高斯指数族（Assumption 1）和参数有界（Assumption 2）。

**主要结果**：
- 对单答案问题，定理 1 给出 TAS 的期望停止时间上界 $\mathbb{E}_\mu[\tau_\delta] \leq 2eK + 10K^4 + T_0(\delta)$，其中 $T_0(\delta)$ 是满足 $t T^\star(\mu)^{-1} - g(t) \geq \beta_{t,\delta}$ 的最小时间，$g(t)$ 为 $O(t^{3/4})$ 的次线性校正项。
- 对多答案问题，S-TAS 同样获得非渐近上界，但包含问题相关常数 $T_\mu$，该常数可能较大，导致实用中的保守性。

**局限性**：上下界之间仍存在间隙，未证明上界的紧致性；分析依赖的分布假设限制了通用性；S-TAS 上界中的 $T_\mu$ 项尚待进一步消解。



纯探索（pure exploration）问题是多臂赌博机理论中的核心设置之一：一个学习代理需要在固定置信度 δ 下，通过序贯采样识别出具有某种最优性质的答案，同时尽可能减少采样次数。当正确答案唯一时，**Track-and-Stop（TAS）** 算法在渐近意义下（δ → 0）达到了信息论下界，被视为该领域的基准方法。其核心思路是将采样规则与停止规则解耦：采样规则通过跟踪 oracle 分配权重来逼近最优采样比例，停止规则则基于广义似然比检验判断是否已积累足够信息。对于存在多个正确答案的更一般情形，**Sticky Track-and-Stop（S-TAS）** 通过引入“粘性”机制扩展了 TAS，同样在渐近意义下达到最优。

然而，实际应用中置信度 δ 总是固定的（而非趋于零），此时渐近最优性无法提供任何有限样本保证。现有文献在非渐近分析方面存在明显缺口：TAS 和 S-TAS 在有限置信度下的停止时间上界此前从未被建立。这一缺口的根源在于，当经验数据稀少时，TAS 的采样规则不稳定——oracle 权重的经验估计波动剧烈，导致跟踪行为偏离理想轨迹；而 S-TAS 因需要同时处理多个候选答案，其采样规则的动态更为复杂，进一步加剧了非渐近分析的难度。

针对上述问题，本文首次给出了 TAS 和 S-TAS 的非渐近上界。分析的关键突破在于：通过定义序列“好事件”{E_t} 来控制经验均值的集中性，并利用 C-Tracking 的性质将停止规则近似为采样规则所积累的信息量，从而在有限置信度下建立期望停止时间的显式上界。这一分析框架不仅填补了从渐近理论到有限样本保证之间的空白，也为理解跟踪类算法在有限数据下的行为提供了新的理论工具。



## 核心方法与创新机理

本文的核心贡献在于首次为 Track-and-Stop (TAS) 及其多答案扩展 Sticky Track-and-Stop (S-TAS) 建立了**非渐近期望停止时间上界**。此前的理论仅保证当置信度参数 $\delta \to 0$ 时的渐近最优性，而本文回答了“给定有限 $\delta$，算法究竟需要多少样本”这一开放问题。实现这一突破的关键创新体现在以下三个层面。

### 1. 经验均值的投影修正

TAS 和 S-TAS 的原始采样规则直接基于经验均值 $\hat{\boldsymbol{\mu}}(t)$ 计算 oracle 权重 $\boldsymbol{\omega}(t)$。然而，在数据稀疏的初始阶段，$\hat{\mu}_k(t)$ 可能落在参数空间的有效边界之外，导致 KL 散度 $d(\hat{\mu}_k(t), \cdot)$ 行为病态，进而破坏采样规则的稳定性。本文引入了一个关键修改：**将经验均值正交投影到 $[\mu_{\min}, \mu_{\max}]^K$ 上**，使用投影后的 $\tilde{\boldsymbol{\mu}}(t)$ 计算 oracle 权重。这一改动确保了 $d(\tilde{\mu}_k(t), \cdot)$ 在整个过程中具有良好的 Lipschitz 性质，从而使得后续的集中性分析成为可能。

### 2. 基于“好事件”的非渐近分析框架

分析的核心瓶颈在于，采样规则 $\boldsymbol{\omega}(t)$ 依赖于噪声经验均值，而停止规则又依赖于采样规则积累的分配 $N_k(t)$，形成循环依赖。本文的解决方案是定义一列**“好事件” $\{\mathcal{E}_t\}$**，在这些事件上：
- 经验均值的 KL 散度逼近真实均值的 KL 散度：$d(\hat{\mu}_k(t), \cdot) \approx d(\mu_k, \cdot)$；
- C-Tracking 过程保证经验分配近似于采样权重之和：$\mathbf{N}(t) \approx \sum_{s=1}^t \boldsymbol{\omega}(s)$。

在好事件发生的高概率下，停止统计量可被下界为采样规则在每一步积累的 **max-min 信息量**（形如 $T^\star(\boldsymbol{\mu})^{-1}$）减去一个 $\mathcal{O}(t^{3/4})$ 的次线性误差项 $g(t)$。这直接导出了停止时间的显式上界 $T_0(\delta)$，其定义为满足 $\beta_{t,\delta} \leq t T^\star(\boldsymbol{\mu})^{-1} - g(t)$ 的最小时间 $t$。

### 3. S-TAS 的多答案处理与问题相关常数

S-TAS 面临额外的复杂性：当存在多个正确答案时，算法需要维护一个候选答案集 $\mathcal{I}_t$，并在其中选择一个 $i_t$ 来计算排除该答案的 oracle 权重 $\boldsymbol{\omega}(t) \in \omega^\star(\tilde{\boldsymbol{\mu}}(t), \neg i_t)$。分析揭示，在好事件下，由于映射 $\boldsymbol{\mu} \mapsto i_F(\boldsymbol{\mu})$ 的上半连续性，$\mathcal{I}_t$ 最终会坍缩到真实可行答案集 $i_F(\boldsymbol{\mu})$。这一坍缩所需的时间被刻画为问题相关常数 $T_\mu$，它表示算法区分可行答案集与最优答案集所需的样本量。S-TAS 的最终上界形式为 $\mathbb{E}_{\boldsymbol{\mu}}[\tau_\delta] \leq T_\mu + T_0(\delta) + \mathcal{O}(K^4)$，其中 $T_0(\delta)$ 的定义调整为 $(t - T_\mu) T^\star(\boldsymbol{\mu})^{-1}$，显式反映了这一“识别期”的代价。

### 方法定位

与现有工作的改进路径相比：**Degenne et al. (2019)** 通过在采样规则中引入置信区间实现乐观化，**Barrier et al. (2022)** 则在数据稀少时向均匀探索倾斜以稳定采样。本文的方法正交于这些思路——它保持 TAS/S-TAS 的核心机制不变，通过投影修正和经验均值集中性的精细控制，首次将分析从渐近域推进到非渐近域。值得注意的是，投影步骤仅为处理病态情形的技术性修正，论文进一步证明了存在问题相关时间 $T_{\mathcal{M}}$，在此之后投影步骤可被安全移除而不影响保证。



本文对**Track-and-Stop (TAS)** 与 **Sticky Track-and-Stop (S-TAS)** 两个纯探索算法进行非渐近分析。二者共享一个三段式管道：**采样规则** → **停止规则** → **推荐规则**，核心瓶颈在于经验数据稀少时采样规则的不稳定性——TAS 面临单答案下的经验均值波动，S-TAS 还需额外处理多重答案问题中候选集 $I_t$ 的识别与收敛。

### 管道总览

```
输入: 置信度 δ, 臂数 K, 指数族参数
  │
  ├─[采样规则]─────────────────────────────────────────
  │  每轮 t:
  │    1. 计算投影经验均值 μ̃(t) (投影到 [μ_min, μ_max]^K)
  │    2. 计算 oracle 权重 ω(t) ∈ ω⋆(μ̃(t))
  │    3. C-Tracking + 强制探索选择臂 A_{t+1}
  │         (S-TAS 额外: 先构建置信域 C_t, 确定候选答案集 I_t, 选定 i_t)
  │
  ├─[停止规则]─────────────────────────────────────────
  │  广义似然比检验:
  │    max_{i∈I} inf_{λ∈¬i} Σ_k N_k(t) d(μ̂_k(t), λ_k) ≥ β_{t,δ}
  │    若成立 → 停止, τ_δ = t
  │
  └─[推荐规则]─────────────────────────────────────────
      输出: 达到停止规则 argmax 的答案 î
```

### 模块关系与因果机制

三个模块通过**好事件序列 $\{\mathcal{E}_t\}$** 耦合在一起。在高概率的好事件下：

1. **经验均值集中**：$\hat{\mu}_k(t)$ 与真值 $\mu_k$ 在 KL 散度意义下足够接近，投影步骤保证 $\tilde{\mu}(t)$ 始终落在合法参数域内。
2. **C-Tracking 近似**：采样分配 $N(t)$ 逼近累积 oracle 权重 $\sum_{s=1}^t \omega(s)$，误差受控于 $O(\sqrt{t})$ 量级。
3. **停止统计量下界**：停止规则的检验统计量可被采样规则每步积累的 max-min 信息量（形如 $T^\star(\mu)^{-1}$）加上次线性误差项 $g(t)$ 下界，从而导出有限置信度下的停止时间上界。

这一因果链条将**采样规则的信息累积速率**直接转化为**停止时间的非渐近控制**，是全文分析的核心洞察。

### 输入输出流

- **输入**：置信水平 $\delta \in (0,1)$，臂数 $K$，单参数指数族（满足 $\sigma^2$-次高斯假设），参数空间有界（Assumption 2）。
- **中间状态**：每轮维护臂计数 $N_k(t)$、经验均值 $\hat{\mu}_k(t)$、投影均值 $\tilde{\mu}_k(t)$、oracle 权重 $\omega(t)$；S-TAS 额外维护置信域 $\mathcal{C}_t$ 和候选答案集 $I_t$。
- **输出**：停止时间 $\tau_\delta$ 与推荐答案 $\hat{\imath}_{\tau_\delta}$，保证 $\mathbb{P}_\mu(\hat{\imath}_{\tau_\delta} \notin i^\star(\mu)) \leq \delta$。

### TAS 与 S-TAS 的分叉点

| 组件 | TAS | S-TAS |
|------|-----|-------|
| 采样规则 | $\omega(t) \in \omega^\star(\tilde{\mu}(t))$ | $\omega(t) \in \omega^\star(\tilde{\mu}(t), \neg i_t)$，其中 $i_t \in I_t$ |
| 候选答案处理 | 无（假设单答案） | 通过置信域 $\mathcal{C}_t$ 动态维护 $I_t$，利用 $\mu \mapsto i_F(\mu)$ 的上半连续性使 $I_t$ 最终坍缩到 $i_F(\mu)$ |
| 上界中的附加项 | $T_0(\delta)$ 直接由信息阈值定义 | 引入问题相关常数 $T_\mu$（区分可行答案集与最优答案集所需的时间） |

S-TAS 的额外复杂度源于：在多重答案问题中，算法必须同时追踪多个可能正确的答案，直到收集到足够证据排除其中一部分。这导致其非渐近上界中出现 $T_\mu$ 项，该常数可能较大，是当前分析的一个保守性来源（需人工验证其紧致性）。



### 关键算法模块

**C-Tracking 采样规则**是 TAS 与 S-TAS 共用的核心采样机制。在每一轮 $t$，算法根据当前投影后的经验 oracle 权重 $\omega(t)$，通过 C-Tracking 结合强制探索选择下一臂：

$$A_{t+1} \in \argmax_{k\in[K]} \sum_{s=K}^t \tilde{\omega}_k(s) - N_k(t)$$

C-Tracking 的关键性质在于：它保证了经验分配 $N(t)$ 近似于累积采样权重 $\sum_{s=1}^t \omega(s)$，这是后续将停止统计量与采样规则所积累的信息量建立联系的桥梁。

**广义似然比停止规则**决定了数据收集何时终止。TAS 在满足以下条件时停止：

$$\max_{i\in\mathcal{I}} \inf_{\lambda\in\neg i} \sum_{k\in[K]} N_k(t) \, d(\hat{\mu}_k(t), \lambda_k) \geq \beta_{t,\delta}$$

其中 $\beta_{t,\delta}$ 为依赖于置信度 $\delta$ 和时间 $t$ 的阈值。停止后，算法推荐达到该 argmax 的答案 $i$。

**经验均值投影**是本文对原始 TAS/S-TAS 的关键修改。算法不直接使用经验均值 $\hat{\mu}(t)$ 计算 oracle 权重，而是先将其正交投影到 $[\mu_{\min}, \mu_{\max}]^K$ 上得到 $\tilde{\mu}(t)$，再计算 $\omega(t) \in \omega^{\star}(\tilde{\mu}(t))$。这一投影确保在病态情形下 $d(\tilde{\mu}_k(t), \cdot)$ 仍然良态，是建立非渐近界的技术前提。

**S-TAS 的候选答案集机制**：S-TAS 在每轮构造置信区域 $\mathcal{C}_t = \{\lambda \in \mathcal{M} : \sum_k N_k(t) d(\hat{\mu}_k(t), \lambda_k) \leq 8K\log(t)\}$，并计算候选答案集 $I_t = \cup_{\lambda\in\mathcal{C}_t} i_F(\lambda)$。算法从中按预定全序选择 $i_t$，再计算 $\omega(t) \in \omega^{\star}(\tilde{\mu}(t), \neg i_t)$。由于 $\mu \mapsto i_F(\mu)$ 的上半连续性，在好事件下 $I_t$ 最终会坍缩到真实最优答案集 $i_F(\mu)$。

---

### 核心公式及其含义

**特征时间的倒数（单答案）**：

$$T^{\star}(\pmb{\mu})^{-1} = \sup_{\omega\in\Delta_K} \inf_{\lambda\in\neg i^{\star}(\pmb{\mu})} \sum_{k\in[K]} \omega_k \, d(\mu_k, \lambda_k)$$

这刻画了纯探索问题的内在难度：max 玩家选择采样权重 $\omega$ 以尽快识别正确答案 $i^{\star}(\mu)$，min 玩家选择使正确答案改变的最坏备择实例 $\lambda$。该量是期望停止时间渐近下界的核心。

**特征时间的倒数（多答案）**：

$$T^{\star}(\pmb{\mu})^{-1} = \sup_{\omega\in\Delta_K} \max_{i\in i^{\star}(\pmb{\mu})} \inf_{\lambda\in\neg i} \sum_{k\in[K]} \omega_k \, d(\mu_k, \lambda_k)$$

多答案情形下，max 操作在正确答案集合 $i^{\star}(\mu)$ 上取最大，以应对多个可能正确答案的复杂性。

**停止阈值 $\beta_{t,\delta}$**：

$$\beta_{t,\delta} = \log\left(\frac{1}{\delta}\right) + K\log\left(4\log\left(\frac{1}{\delta}\right) + 1\right) + 6K\log(\log(t) + 3)$$

该阈值由三项组成：主导项 $\log(1/\delta)$ 来自 Garivier & Kaufmann (2016) 的广义似然比检验框架；第二项修正了多臂带来的联合置信区间膨胀；第三项是时间 $t$ 的慢增长惩罚，保证任意时间停止下的 $\delta$-正确性。

**次线性校正项 $g(t)$（TAS）**：

$$g(t) = 64\sigma D L K^2 \log(K) \sqrt{t \log^2(t)} + 16\sigma D \sqrt{K t^{3/2} \log(t)}$$

$g(t)$ 的增长阶为 $O(t^{3/4})$，在停止条件中用于吸收 C-Tracking 的逼近误差和经验均值与真值的 KL 散度偏差。其中 $\sigma$ 来自 Assumption 1（$\sigma^2$-次高斯指数族），$D$ 和 $L$ 来自 Assumption 2（参数有界性）。

**TAS 的 $T_0(\delta)$**：

$$T_0(\delta) = \inf\left\{t \in \mathbb{N} : \beta_{t,\delta} \leq t \, T^{\star}(\pmb{\mu})^{-1} - g(t)\right\}$$

这是 TAS 期望停止时间上界中与 $\delta$ 相关的关键项。它定义了当累积信息量 $t \cdot T^{\star}(\mu)^{-1}$ 减去次线性误差 $g(t)$ 后首次超过阈值 $\beta_{t,\delta}$ 的时间。

**S-TAS 的问题相关常数 $T_{\mu}$**：

$$T_{\mu} = \max\left\{10K^4, \inf\left\{n \in \mathbb{N} : \sqrt{\frac{64K\sigma^2 \log(n)}{\sqrt{\sqrt{n} + K^2} - 2K}} \leq \epsilon_{\mu}\right\}\right\}$$

$T_{\mu}$ 是 S-TAS 在好事件下区分可行答案集 $i_F(\mu) \cup (\mathcal{I} \setminus i^{\star}(\mu))$ 与最优答案集 $i^{\star}(\mu)$ 所需的时间。该常数直接出现在 S-TAS 的 $T_0(\delta)$ 定义中：

$$T_0(\delta) = \inf\left\{t \in \mathbb{N} : \beta_{t,\delta} \leq (t - T_{\mu}) \, T^{\star}(\mu)^{-1} - g(t)\right\}$$

$T_{\mu}$ 的存在使得 S-TAS 的上界比 TAS 更为保守——在 $t \leq T_{\mu}$ 阶段，算法尚未可靠锁定正确答案集，因此这段时间无法贡献有效的特征时间信息量。该常数的具体值依赖于问题结构参数 $\epsilon_{\mu}$，可能在实用中较大，是当前上界保守性的主要来源。



## 实验与关键发现

本文是一篇纯理论分析论文，未提供数值实验、消融研究或实证失败模式。论文的主要贡献在于首次为 Track-and-Stop（TAS）和 Sticky Track-and-Stop（S-TAS）算法建立了**非渐近上界**，其核心结论完全由定理和证明支撑。

### 主要理论结果

**TAS 的有限置信度保证**（定理 1）：
在 Assumption 1（σ²-次高斯指数族）和 Assumption 2（参数有界）下，当正确答案唯一时，TAS 的期望停止时间满足

$$\mathbb{E}_{\mu}[\tau_{\delta}] \leq 2eK + 10K^{4} + T_{0}(\delta),$$

其中 $T_{0}(\delta)$ 由信息量阈值条件定义：

$$T_{0}(\delta) = \inf\left\{ t \in \mathbb{N} : \beta_{t,\delta} \leq t\, T^{\star}(\pmb{\mu})^{-1} - g(t) \right\}.$$

这里 $\beta_{t,\delta}$ 是广义似然比停止阈值，$g(t)$ 是 $\mathcal{O}(t^{3/4})$ 的次线性校正项，$T^{\star}(\pmb{\mu})^{-1}$ 是问题特征时间的倒数。该上界表明，当 $\delta \to 0$ 时，$\mathbb{E}[\tau_{\delta}] \leq T^{\star}(\pmb{\mu})\log(1/\delta) + \mathcal{O}(\sqrt{\log(1/\delta)})$，恢复了 Garivier & Kaufmann（2016）的渐近最优性。

**S-TAS 的有限置信度保证**（定理 2）：
对于多重答案问题，S-TAS 的期望停止时间满足

$$\mathbb{E}_{\mu}[\tau_{\delta}] \leq 2eK + 10K^{4} + T_{\mu} + T_{0}(\delta),$$

其中 $T_{\mu}$ 是问题相关常数，表示在“好事件”下区分可行答案集 $i_{F}(\mu)$ 与最优答案集 $i^{\star}(\mu)$ 所需的时间。$T_{0}(\delta)$ 的定义与 TAS 类似，但信息积累从 $t - T_{\mu}$ 开始计算。

### 关键机理与瓶颈

上界的推导依赖于两个核心技术环节：

1. **“好事件”的定义与控制**：通过定义序列事件 $\{\mathcal{E}_{t}\}$，在高概率下保证经验均值 $\hat{\mu}_{k}(t)$ 与真实均值 $\mu_{k}$ 在 KL 散度意义下充分接近。C-Tracking 采样规则进一步确保经验分配 $N(t)$ 逼近累积的 oracle 权重 $\sum_{s=1}^{t} \omega(s)$。

2. **停止统计量的信息量下界**：在好事件下，停止统计量可以被采样规则每一步积累的 max-min 信息量下界，即

   $$\sum_{s=1}^{t} \inf_{\lambda \in \neg i^{\star}(\mu)} \sum_{k} \omega_{k}(s) d(\mu_{k}, \lambda_{k}) - \tilde{\mathcal{O}}(t^{3/4}),$$

   这直接导出了与 $T^{\star}(\mu)^{-1}$ 的联系。

### 已知局限与未验证属性

- **上下界差距**：本文仅给出上界，未证明其紧致性。非渐近下界尚不完善，是否存在与上界匹配的更紧下界是开放问题。
- **$T_{\mu}$ 的保守性**：S-TAS 上界中的 $T_{\mu}$ 可能较大，导致实用中的保守性。能否消除该常数以获得更简洁的保证，仍需进一步研究。
- **假设依赖性**：分析依赖 Assumption 1 和 Assumption 2，限制了结果在一般分布族上的通用性。
- **投影步骤的额外复杂度**：算法中引入的经验均值投影仅用于处理病态情形，但在一般指数族下增加了实现复杂度，且投影步骤是否可被移除及其对保证的影响尚待分析。

> **注意**：由于本文未包含数值实验，上述所有结论均来自理论推导。建议读者直接参考原文定理陈述和证明细节以验证边界常数的精确性。



## 定位与知识库关联

### 1. 问题定位：纯探索中的最优停止与采样耦合

本文聚焦于 **纯探索（Pure Exploration）** 问题中一类核心算法的非渐近分析，具体对象为 **Track-and-Stop (TAS)** 及其多答案扩展 **Sticky Track-and-Stop (S-TAS)**。纯探索问题的核心目标是在给定置信度 δ 下，以最小化样本复杂度（期望停止时间）的方式识别 bandit 模型中的最优答案集。这类问题与 regret minimization 形成根本性区别：后者关注累积遗憾，而纯探索关注决策的最终正确性和采样效率。

该领域的理论基石由 Garivier & Kaufmann (2016) 奠定，他们证明了单答案纯探索问题的期望停止时间下界为 $T^\star(\mu) \log(1/\delta)$，其中 $T^\star(\mu)^{-1}$ 是一个由采样权重 ω 与最坏备择实例 λ 之间的 max-min KL 散度定义的**特征时间倒数**：

$$T^{\star}(\pmb{\mu})^{-1} = \sup_{\omega \in \Delta_K} \inf_{\lambda \in \neg i^{\star}(\pmb{\mu})} \sum_{k \in [K]} \omega_k d(\mu_k, \lambda_k)$$

这一公式揭示了一个深层结构：最优采样策略是采样者在单纯形上最大化信息获取，而对抗者选择一个使当前答案失效的备择实例来最小化区分难度。TAS 算法正是通过**每一步计算 oracle 权重 ω(t) 并用 C-Tracking 跟踪这些权重**来逼近这一 max-min 解，从而在 δ → 0 时达到渐近最优性。

### 2. 方法沿革：从 TAS 到 S-TAS 的演进瓶颈

TAS 的渐近最优性仅适用于**单答案问题**（即 $i^\star(\mu)$ 为单值）。当存在多个正确答案时，算法面临一个根本性困难：停止规则需要同时排除所有错误答案，而采样规则必须服务于一个动态变化的候选答案集。Degenne & Koolen (2019) 提出的 **S-TAS** 通过引入置信区域 $\mathcal{C}_t$ 和候选答案集 $\mathcal{I}_t$ 来解决这一问题：

$$\mathcal{C}_t = \{\lambda \in \mathcal{M} : \sum_k N_k(t) d(\hat{\mu}_k(t), \lambda_k) \leq 8K \log(t)\}$$

$$\mathcal{I}_t = \bigcup_{\lambda \in \mathcal{C}_t} i_F(\lambda)$$

S-TAS 的核心洞察在于利用 $i_F(\mu)$ 的上半连续性（upper-hemicontinuity）：在“好事件”下，随着数据积累，置信区域收缩，$\mathcal{I}_t$ 最终会坍缩到真实的最优答案集 $i^\star(\mu)$。这一机制使得 S-TAS 能够在多答案场景下恢复渐近最优性。

然而，**非渐近分析面临两个关键瓶颈**：

1. **采样规则的不稳定性**：当经验数据稀少时，经验均值 $\hat{\mu}(t)$ 可能严重偏离真实均值，导致 oracle 权重 ω(t) 剧烈波动。本文通过引入**经验均值投影**（将 $\hat{\mu}(t)$ 正交投影到 $[\mu_{\min}, \mu_{\max}]^K$ 得到 $\tilde{\mu}(t)$，再计算 $\omega(t) \in \omega^\star(\tilde{\mu}(t))$）来缓解这一问题。这一修改的动机是保证 KL 散度 $d(\tilde{\mu}_k(t), \cdot)$ 在边界附近仍然良态，避免病态行为破坏集中不等式。

2. **多重答案的复杂性**：S-TAS 需要在候选答案集 $\mathcal{I}_t$ 中动态选择目标答案 $i_t$，并在该答案的“排除集” $\neg i_t$ 上计算 oracle 权重。这意味着采样策略的优化目标随时间变化，使得停止统计量与累积信息量之间的耦合更加松散。本文的分析通过引入**问题相关常数 $T_\mu$** 来刻画这一复杂性：$T_\mu$ 是 S-TAS 在好事件下将 $\mathcal{I}_t$ 与 $i^\star(\mu)$ 区分开所需的最小时间，其显式形式为：

$$T_{\mu} = \max\left\{10K^4, \inf\left\{n \in \mathbb{N} : \sqrt{\frac{64K\sigma^2 \log(n)}{\sqrt{\sqrt{n} + K^2} - 2K}} \leq \epsilon_{\mu}\right\}\right\}$$

其中 $\epsilon_\mu$ 是问题相关的最小间隔参数。$T_\mu$ 的存在导致 S-TAS 的非渐近上界中出现了 $(t - T_\mu)$ 形式的有效信息积累项，而非 TAS 中的直接 $t$ 倍特征时间。

### 3. 与相关工作的关系

**Degenne et al. (2019)** 提出了 TAS 的乐观变体，在采样规则中引入置信区间，试图在探索和利用之间取得更好的平衡。该方法在经验上可能改善有限样本性能，但本文指出其非渐近分析更为困难，因为乐观性引入了额外的随机性。

**Barrier et al. (2022)** 通过“偏斜”采样规则来稳定 TAS：当数据稀缺时，算法倾向于均匀探索。这一思路与本文的投影方法有相似动机，但实现路径不同——Barrier 等人的方法修改了 C-Tracking 的行为，而本文直接修改了 oracle 权重的输入。

本文的核心贡献在于**首次给出了 TAS 和 S-TAS 的非渐近上界**。具体而言：

- **TAS 的期望停止时间上界**（定理 1）：
  $$\mathbb{E}_\mu[\tau_\delta] \leq 2eK + 10K^4 + T_0(\delta)$$
  其中 $T_0(\delta) = \inf\{t \in \mathbb{N} : \beta_{t,\delta} \leq t T^\star(\mu)^{-1} - g(t)\}$，$g(t)$ 是一个 $O(t^{3/4})$ 的次线性校正项，$\beta_{t,\delta}$ 是保证 δ-正确性的停止阈值。

- **S-TAS 的期望停止时间上界**（定理 2）具有类似结构，但 $T_0(\delta)$ 的定义变为 $\inf\{t : \beta_{t,\delta} \leq (t - T_\mu) T^\star(\mu)^{-1} - g(t)\}$，反映了 $T_\mu$ 带来的信息积累延迟。

### 4. 适用边界与关键假设

本文的分析严格依赖于两个假设：

- **Assumption 1**：臂的奖励分布属于 $\sigma^2$-次高斯指数族，满足 $d(\mu, \mu') \geq (\mu - \mu')^2 / (2\sigma^2)$。这排除了重尾分布或非指数族模型。
- **Assumption 2**：参数空间有界，$\mu_k \in [\mu_{\min}, \mu_{\max}]$。这使得投影步骤有意义，并保证了 KL 散度的 Lipschitz 性质。

这些假设限制了结果的通用性。例如，对于 Bernoulli 分布（有界支撑但方差依赖于均值），Assumption 1 可以通过取最坏情况的 $\sigma^2$ 来满足，但会导致常数因子的保守性。

### 5. 局限与开放问题

**已知局限**：
1. **上下界之间的差距**：本文仅给出了上界，未证明其紧致性。有限置信度下，上界中的 $K^4$ 项和 $g(t)$ 的次线性项是否必要仍不清楚。
2. **$T_\mu$ 的保守性**：S-TAS 上界中的 $T_\mu$ 可能在实际问题中较大，导致上界在中等置信度下失去实用指导意义。能否消除 $T_\mu$ 或以更紧的量替代是一个开放问题。
3. **投影步骤的实现成本**：经验均值投影是为分析便利引入的技术性修改，在一般指数族下增加了实现复杂度。本文指出存在一个问题相关时间 $T_{\mathcal{M}}$，在此之后投影自动失效（经验均值自然落入有效区间），但 $T_{\mathcal{M}}$ 本身可能很大。

**开放问题**：
- 能否将有限置信度分析方法推广到 **regret minimization 采样策略**（如 UCB、Thompson Sampling）的纯探索变体？
- 本文的分析框架是否可以扩展到**无限答案集合**的纯探索问题（如 Poiani et al. 2025 所研究的连续结构 bandit）？
- 是否存在与本文上界匹配的非渐近下界，从而完整刻画 TAS/S-TAS 的有限样本最优性？

> **注意**：本文未提供实验验证，所有结论均为理论推导。对于上界中常数因子的实际紧致性，需要独立的数值研究来评估。



## 原文 PDF

![[paperPDFs/ICLR_2026/Non_Asymptotic_Analysis_of_Sticky_Track_and_Stop.pdf]]
