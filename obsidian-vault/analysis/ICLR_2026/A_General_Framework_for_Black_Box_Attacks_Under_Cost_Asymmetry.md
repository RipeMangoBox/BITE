---
title: "A General Framework for Black-Box Attacks Under Cost Asymmetry"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_General_Framework_for_Black_Box_Attacks_Under_Cost_Asymmetry.pdf
project_link: null
code_link: https://github.com/mahdisalmani/Asymmetric-Attacks
aliases:
- AA
- GFBBAUCA
- "Asymmetric Attacks"
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/safety_security
core_operator: "攻击的两个核心操作——边界搜索（binary search）和梯度估计（Monte Carlo采样）——在不对称成本下会产生约一半的高成本查询。通过修改这两个操作的策略，可以主动控制高/低成本查询的比例，从而最小化总成本。"
primary_logic: "将边界搜索的区间分割比例从1:1改为1:c*（成本比率），将梯度估计的采样中心从边界点向低成本区域偏移，并对不同成本的查询赋予不同权重，从而在保持攻击效果的同时显著降低总查询成本。"
claims:
- "AS将区间按1:c*比例分割，最小化期望成本而非查询次数"
- "AGREST将采样中心向低成本区域偏移并加权，减少高成本查询频率"
- "AS的期望成本为O(c* log_{c*+1}(1/τ))，相比binary search的Θ(c* log(1/τ))有Θ(log(c*+1))倍的改进"
- "在c*=10^3时，binary search的累积搜索成本约为AS的2.5倍"
---

# A General Framework for Black-Box Attacks Under Cost Asymmetry

> [!tip] 核心洞察
> 将边界搜索的区间分割比例从1:1改为1:c*（成本比率），将梯度估计的采样中心从边界点向低成本区域偏移，并对不同成本的查询赋予不同权重，从而在保持攻击效果的同时显著降低总查询成本。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 成本不对称下黑盒攻击的通用框架 |
| 英文题名 | A General Framework for Black-Box Attacks Under Cost Asymmetry |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=G1fFulgfd8) · [GitHub](https://github.com/mahdisalmani/Asymmetric-Attacks) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/safety_security |
| Method | Asymmetric Attacks |
| Dataset | ImageNet, ResNet-50, ViT-B/32 |

> [!tip] 效果简介
> - ImageNet, ResNet-50 上，Median ℓ₂ distance (c*=2, total cost 15000) 为 A-HSJA: 2.06，对比 HSJA VA: 4.09，变化 -49.6%。
> - ImageNet, ResNet-50 上，Median ℓ₂ distance (c*=10^2, total cost 15000) 为 A-HSJA: 10.74，对比 HSJA VA: 70.4，变化 -84.7%。
> - ImageNet, ResNet-50 上，Median ℓ₂ distance (c*=10^3, total cost 15000) 为 A-CGBA: 6.23，对比 CGBA VA: 9.67，变化 -35.6%。

## 概要

本文针对现有决策型黑盒攻击中一个被忽视但实际重要的瓶颈——查询成本不对称——提出了一个通用框架。在真实场景（如NSFW内容检测）中，不同类别（正常vs标记）的查询成本可能高度不对称，而传统方法（如HSJA、GeoDA、CGBA）假设所有查询成本相等，stealthy attacks虽考虑高成本查询但假设良性查询成本为零，忽略了大量低成本查询的累积开销。

核心洞察在于：攻击的两个核心操作——边界搜索（binary search）和梯度估计（Monte Carlo采样）——在不对称成本下会产生约一半的高成本查询。通过修改这两个操作的策略，可以主动控制高/低成本查询的比例，从而最小化总成本。具体地，本文提出两个关键组件：（1）**Asymmetric Search (AS)**，将区间按成本比率 $1:c^\star$ 分割而非等分，最小化期望成本而非查询次数；（2）**Asymmetric GRadient ESTimation (AGREST)**，将采样中心向低成本区域偏移并对不同成本查询赋予不同权重（重要性采样），减少高成本查询频率。

理论分析表明，AS的期望成本为 $O(c^\star \log_{(c^\star+1)}(1/\tau))$，相比binary search的 $\Theta(c^\star \log(1/\tau))$ 有 $\Theta(\log(c^\star+1))$ 倍的改进。当 $c^\star=10^3$ 时，binary search的累积搜索成本约为AS的2.5倍。

实验在ImageNet（ResNet-50、ViT-B/32、ViT-B/16）上进行，主要结果：在总成本15000、$c^\star=2$ 时，A-HSJA的中位 $\ell_2$ 距离为2.06，相比HSJA的4.09降低49.6%；在 $c^\star=10^2$ 时，A-HSJA为10.74 vs HSJA的70.4（降低84.7%）。该方法兼容HSJA、GeoDA、CGBA等多种攻击，并在高成本不对称（$c^\star=10^4, 10^5, \infty$）下一致优于Stealthy HSJA。消融实验证实AS和AGREST单独使用均有效，联合使用效果最佳。



决策型黑盒攻击（如HSJA、GeoDA、CGBA）通过仅访问模型输出的硬标签（如“对抗”或“非对抗”）来构造对抗样本。这类攻击的核心操作包括两个步骤：沿搜索方向进行**边界搜索**（通常使用二分查找）以精确定位决策边界，以及通过**蒙特卡洛采样**估计梯度方向以更新搜索方向。现有方法（包括Stealthy HSJA）隐含地假设所有查询的成本相等，但在许多实际部署场景中，这一假设不成立。

考虑一个NSFW（不适宜工作场所）内容检测系统：对系统而言，将正常图像标记为NSFW（假阳性）的成本远高于将NSFW图像标记为正常（假阴性）的成本，因为前者会直接导致用户体验下降和用户流失。因此，系统对“标记为NSFW”的查询会施加更高的成本（如人工审核、账户警告等）。更一般地，攻击者面对的查询成本取决于查询结果所属的类别——例如，在内容审核系统中，被标记为“违规”的查询（即高成本查询）可能触发更昂贵的审查流程，而“正常”查询（即低成本查询）则几乎无额外开销。这种**成本不对称**（cost asymmetry）普遍存在于各类安全敏感的应用中，包括欺诈检测、垃圾邮件过滤、医疗诊断等。

现有方法在处理成本不对称时存在根本性缺陷。传统攻击（vanilla attacks）完全无视成本差异，将高成本和低成本查询一视同仁，导致在高成本不对称场景下（如成本比率$c^*=10^3$）产生大量昂贵查询。Stealthy HSJA虽然尝试减少高成本查询，但其设计假设良性（低成本）查询的成本为零，忽略了大量低成本查询的累积开销；更关键的是，它只能处理$c^* \to \infty$的极端情况，无法适用于任意有限成本比率。此外，Stealthy HSJA通过完全避免梯度估计中的高成本查询来工作，这在高成本查询提供关键梯度信息时会严重损害攻击效果。

本文的核心洞察在于：攻击的两个核心操作——边界搜索和梯度估计——在不对称成本下都会产生约一半的高成本查询（当决策边界大致将空间等分时）。通过修改这两个操作的策略，可以主动控制高/低成本查询的比例，从而在保持攻击效果的同时最小化总成本。具体地，本文提出两个通用模块：

1. **非对称搜索（Asymmetric Search, AS）**：将二分查找的区间分割比例从1:1改为$1:c^*$（成本比率），使搜索偏向低成本区域，从而最小化期望成本而非查询次数。理论分析表明，AS的期望成本为$O(c^* \log_{c^*+1}(1/\tau))$，相比二分查找的$\Theta(c^* \log(1/\tau))$有$\Theta(\log(c^*+1))$倍的改进。

2. **非对称梯度估计（Asymmetric Gradient Estimation, AGREST）**：将蒙特卡洛采样的中心从边界点向低成本区域偏移，并对不同成本的查询赋予不同权重（通过重要性采样），从而在保持梯度估计质量的同时显著减少高成本查询的频率。

这两个模块可即插即用地集成到现有决策型攻击（HSJA、GeoDA、CGBA、SurFree）中，形成统一的**非对称攻击（Asymmetric Attacks）**框架。实验表明，在ImageNet上，该方法在不同成本比率下均显著优于传统攻击和Stealthy HSJA：例如，在$c^*=10^2$时，A-HSJA的中位$\ell_2$距离从70.4降至10.74（降低84.7%）；在$c^*=10^3$时，A-CGBA的中位$\ell_2$距离从9.67降至6.23（降低35.6%）。在极端高成本不对称（$c^*=10^4, 10^5, \infty$）下，所有非对称攻击变体均优于Stealthy HSJA。



## 核心方法与创新机理

本文的核心创新在于揭示了现有决策型黑盒攻击在成本不对称场景下的根本瓶颈，并针对性地提出了两种通用修改策略——**Asymmetric Search (AS)** 和 **Asymmetric Gradient Estimation (AGREST)**，从而构建了一个可以即插即用地集成到 HSJA、GeoDA、CGBA 等主流攻击中的通用框架。其关键洞察在于：攻击的两个核心操作——边界搜索和梯度估计——在成本不对称时，天然会产生约一半的高成本查询；通过主动操控这两个操作中的查询类型比例，可以在保持攻击效果的同时，系统性地最小化总查询成本。

**瓶颈与因果机制**：现有方法（如 HSJA）进行边界搜索时，采用标准的二分搜索（Binary Search），每次将区间等分为 1:1，这假设了所有查询成本相等。但在成本不对称场景下（如 NSFW 检测中，查询“正常”类别成本远高于“违规”类别），这种策略会浪费大量成本在昂贵的查询上。同样，梯度估计时，在决策边界点周围进行蒙特卡洛采样，会导致约一半的采样点落入高成本区域。先前的工作如 Stealthy Attacks 虽然考虑了不对称成本，但其仅将良性查询成本设为零，忽略了大量低成本查询的累积开销，且无法处理任意成本比率。

**核心创新一：Asymmetric Search (AS) —— 最小化期望成本的区间搜索**

AS 直接改变了边界搜索的区间分割比例，从传统的 1:1 改为 1:c*（c*为高成本与低成本查询的成本比率）。这一改变的核心目标从“最小化查询次数”转向了“最小化期望成本”。其理论优势体现在定理1中：AS 的期望成本为 O(c* log_{c*+1}(1/τ))，而标准二分搜索的期望成本为 Θ(c* log(1/τ))。这意味着 AS 在理论上获得了 Θ(log(c*+1)) 倍的改进。当 c*=1 时，AS 退化为标准二分搜索；当 c*=∞ 时，则退化为简单的线搜索策略。实验证据（App. C）表明，当 c*=10^3 时，二分搜索的累积搜索成本约为 AS 的 2.5 倍。

**核心创新二：Asymmetric Gradient Estimation (AGREST) —— 偏移采样中心并加权**

AGREST 则修改了梯度估计的采样策略。其核心是**将采样中心从决策边界点 x_t 向低成本区域偏移**，得到新的采样中心 x_t'。这一偏移操作（Overshooting）使得大部分采样点落入低成本区域，从而显著减少高成本查询的频率。为了补偿因采样中心偏移而引入的梯度估计偏差，AGREST 引入了**重要性采样权重**，对高成本查询赋予更高的权重。这种“偏移+加权”的联合设计，使得梯度估计在保持无偏性的同时，大幅降低了高成本查询的比例。实验证据（Table 1）显示，在 c*=10^2 时，AGREST 单独使用即可将 HSJA 的 ℓ₂ 距离从 4.66 降至 2.19（约降低 53%）。

**框架的通用性与改进幅度**：AS 和 AGREST 被设计为可替换的模块，可以独立或联合地插入到任何基于决策的黑盒攻击中。实验结果表明（Table 1），联合使用 AS 和 AGREST（即 A-HSJA, A-GeoDA, A-CGBA, A-SurFree）在所有 c* 值下均优于单独使用任一模块。例如，在 ImageNet 的 ResNet-50 上，当总成本为 15000 且 c*=2 时，A-HSJA 的中位 ℓ₂ 距离为 2.06，相较于 HSJA 的 4.09 降低了 49.6%；当 c*=10^2 时，这一优势扩大到 84.7%（10.74 vs 70.4）。在 ViT-B/32 上，A-CGBA 在 c*=2 时也实现了 33.3% 的改进（1.42 vs 2.13）。此外，在高成本不对称场景下（c*=10^4, 10^5, ∞），所有 Asymmetric Attacks 均一致优于先前的 Stealthy HSJA（Figure 3），这表明该框架不仅解决了任意成本比率问题，也覆盖了 Stealthy Attacks 的设定。

**证据强度与局限性**：上述核心创新的证据强度很高，所有关键声明均有明确的原文锚点和实验数据支持（置信度均为 1.0）。AS 和 AGREST 的算法描述、理论分析（定理1）及消融实验（Table 1）均完整且一致。然而，该框架引入了一个新的超参数 m，用于控制 AGREST 的过冲量，其最优值可能随不同设置（如模型、c*）而变化，需要额外调优（Figure 5）。此外，该框架目前仅处理二分类（源类 vs 非源类）的不对称成本，尚未扩展到多目标类各自具有不同查询成本的更复杂场景，这一点在论文的局限性中已明确指出。



![[assets/figures/papers/iclr26_0002_G1fFulgfd8_A_General_Framework_for_Black-Box_Attacks_Under/figures/001_Figure_1.jpg]]
*Figure 1: Each point represents the median number of queries required by an attack method to reach a median $\ell _ { 2 }$ norm of 10. The x-axis shows the number of flagged queries ( $Q _ { \mathrm { f l a g g e d } }$ ) and the y-axis reports the total number of queries ( $Q _ { \mathrm { t o t a l } }$ ) . It demonstrates the superiority of our method in achieving a more favorable trade-off between flagged and total number of queries in stealthy attack settings

Asymmetric Attacks 是一个通用框架，旨在将现有的决策型黑盒攻击（如 HSJA、GeoDA、CGBA、SurFree）扩展到查询成本不对称的场景。其核心思想是：在攻击的两个关键操作——边界搜索（binary search）和梯度估计（Monte Carlo 采样）——中，主动控制高成本查询与低成本查询的比例，从而在保持攻击效果的同时最小化总查询成本。

该框架的 pipeline 包含四个主要模块：

1.  **Asymmetric Search (AS)**：沿路径搜索决策边界时，不再像传统 binary search 那样将区间等分为 1:1，而是按成本比率 `1:c*` 分割区间。当 `c*=1` 时退化为标准 binary search，当 `c*=∞` 时退化为简单线搜索。该模块的期望成本为 `O(c* log_{c*+1}(1/τ))`，相比 binary search 的 `Θ(c* log(1/τ))` 有 `Θ(log(c*+1))` 倍的改进（Theorem 1）。实验表明，当 `c*=10^3` 时，binary search 的累积搜索成本约为 AS 的 2.5 倍（App. C）。

2.  **Asymmetric Gradient Estimation (AGREST)**：在估计梯度方向时，将采样中心从边界点 `x_t` 向低成本区域偏移至 `x_t'`（即过冲点），从而降低高成本查询的频率。同时，对不同成本的查询赋予不同权重（高成本查询权重更高），以降低估计方差。该模块的梯度估计器为 `\widehat{\nabla S}(\mathbf{x}_t, \omega_t, \beta_t)`（Eq. (6)），其中 `β_t` 为重要性采样权重，`ω_t` 为过冲步长。最优参数由 Theorem 3 给出。

3.  **Overshooting step size scheduler**：根据当前方向与真实梯度之间的夹角 `α_t`，动态调整过冲步长 `ω_t ← ω^⋆ / cos α_t`。初始夹角的余弦期望由 Theorem 4 给出：`\mathbb{E}[\cos \alpha_1] = \frac{\Gamma(d/2)}{2\sqrt{\pi} \Gamma((d+1)/2)}`。

4.  **Query cost budget scheduler**：根据迭代次数分配查询预算 `c_t ← n_t'(c^⋆ + 1)/2`，确保总查询成本受控。

**输入输出流**：输入为源图像 `x`、目标类 `y`、成本比率 `c*`、总查询预算。输出为对抗样本 `x_adv`。在每个迭代中，先通过 AS 搜索边界点 `x_t`，然后通过 AGREST 估计梯度方向 `g_t`，再根据角度调整步长后沿梯度方向更新 `x_t`，直至达到扰动约束或预算耗尽。

该框架兼容多种基础攻击（HSJA、GeoDA、CGBA、SurFree），只需将其中的边界搜索和梯度估计模块替换为 AS 和 AGREST。消融实验（Table 1）表明，AS 单独使用即可降低所有 `c*` 下的扰动（SurFree 上 `c*=2` 时 ℓ₂ 从 4.09 降至 3.45），AGREST 单独使用在大 `c*` 下降低 ℓ₂ 约 40%（HSJA 上 `c*=10^2` 时从 4.66 降至 2.19），两者联合使用效果最佳。



本文的核心创新在于将传统决策型黑盒攻击中的两个关键操作——边界搜索与梯度估计——改造为成本不对称感知的版本。以下分别阐述其核心模块与关键公式。

### 问题形式化

攻击的决策函数定义为：
$$\phi_{\mathbf{x}}(\mathbf{x}') = \mathrm{sign}(S_{\mathbf{x}}(\mathbf{x}'))$$
其中 $\phi_{\mathbf{x}}(\mathbf{x}') = 1$ 表示查询 $\mathbf{x}'$ 是对抗样本（非标记），$\phi_{\mathbf{x}}(\mathbf{x}') = -1$ 表示不是对抗样本（标记/高成本）。

总查询成本重参数化为：
$$\mathrm{cost} := Q_{\mathrm{non-flagged}} + Q_{\mathrm{flagged}} \cdot c^\star$$
其中 $c^\star = (c_{\mathrm{flagged}} + c_0)/c_0$ 是高成本查询相对于低成本查询的成本比率，$Q_{\mathrm{non-flagged}}$ 和 $Q_{\mathrm{flagged}}$ 分别是两类查询的数量。该形式将可调参数从两个减少为一个，便于分析。

### 模块一：Asymmetric Search (AS)

**瓶颈**：传统 binary search 每次将区间等分为 1:1，在成本不对称下会产生约一半的高成本查询，导致总成本次优。

**机制**：AS 将区间按 $1 : c^\star$ 的比例分割，偏向于产生更多低成本查询。具体地，设搜索区间长度为 $m$，则 AS 在距离低成本端 $m/(c^\star+1)$ 处进行查询。当 $c^\star=1$ 时退化为标准二分搜索；当 $c^\star=\infty$ 时退化为简单的线性搜索（仅使用低成本查询）。

**核心公式**：AS 的期望成本为：
$$O(c^\star \log_{(c^\star+1)}(1/\tau))$$
其中 $\tau$ 是搜索精度。相比 binary search 的 $\Theta(c^\star \log(1/\tau))$，AS 实现了 $\Theta(\log(c^\star+1))$ 倍的改进。该结果基于假设 A1（决策边界附近局部线性）和归纳法证明（见附录 B.1）。

### 模块二：Asymmetric Gradient Estimation (AGREST)

**瓶颈**：传统 Monte Carlo 梯度估计在边界点 $\mathbf{x}_t$ 周围均匀采样，导致约一半查询落入低成本区域、一半落入高成本区域，总成本高。

**机制**：AGREST 将采样中心从边界点 $\mathbf{x}_t$ 向低成本区域偏移至 $\mathbf{x}_t' = \mathbf{x}_t + \omega_t \cdot \mathbf{g}_t$（其中 $\omega_t$ 是过冲步长，$\mathbf{g}_t$ 是当前梯度方向），使更多采样点落在低成本区域。同时对不同成本的查询赋予不同权重，通过重要性采样校正偏差。

**核心公式**：AGREST 梯度估计器为：
$$\widehat{\nabla S}(\mathbf{x}_t, \omega_t, \beta_t) = \frac{1}{n_t} \sum_{i=1}^{n_t} \widehat{\phi}_t(\mathbf{x}_t' + \delta\mathbf{u}_i) \mathbf{u}_i$$
其中 $\widehat{\phi}_t(\cdot)$ 是带重要性采样权重的决策函数输出，$\beta_t$ 是低成本查询的权重参数，$\mathbf{u}_i$ 是单位球面上的随机扰动，$\delta$ 是平滑参数。

**最优参数**（Theorem 3）：在给定总查询预算 $c_t$ 和低成本查询概率 $p_t(\omega_t^\star)$ 下，最优查询数量和权重为：
$$n_t^\star = c_t (c^\star - (c^\star - 1) p_t(\omega_t^\star))^{-1}, \quad \beta_t^\star = p_t(\omega_t^\star)$$
该结果假设决策边界局部线性，通过最大化估计梯度与真实梯度的余弦相似度推导得出（见附录 B.3）。

### 模块三：过冲步长调度器

**机制**：过冲步长 $\omega_t$ 根据当前估计梯度与真实梯度之间的夹角 $\alpha_t$ 动态调整：
$$\omega_t \leftarrow \omega^\star / \cos \alpha_t$$
其中 $\omega^\star$ 是基础步长参数。该设计确保在梯度方向不确定时（$\alpha_t$ 大）减小过冲，避免过度偏离边界。

**初始余弦期望**（Theorem 4）：初始方向与梯度之间的夹角余弦期望为：
$$\mathbb{E}[\cos \alpha_1] = \frac{\Gamma(d/2)}{2\sqrt{\pi} \Gamma((d+1)/2)}$$
其中 $d$ 是输入维度。该公式用于初始化 $\alpha_t$ 的估计。

### 模块四：查询预算调度器

**机制**：每轮迭代的总查询预算 $c_t$ 根据迭代次数和成本比率动态分配：
$$c_t \leftarrow n_t'(c^\star + 1)/2$$
其中 $n_t'$ 是预分配的低成本查询数量。该调度确保总成本预算随迭代均匀消耗。

### 关键公式变量含义汇总

| 符号 | 含义 | 来源 |
|------|------|------|
| $\phi_{\mathbf{x}}(\mathbf{x}')$ | 决策函数，输出 $\pm 1$ | Eq. (1) |
| $c^\star$ | 高/低成本查询的成本比率 | Eq. (4) |
| $\tau$ | 边界搜索精度 | Theorem 1 |
| $\omega_t$ | 过冲步长 | Algorithm 1 |
| $\alpha_t$ | 估计梯度与真实梯度的夹角 | Algorithm 1 |
| $\beta_t$ | 低成本查询的重要性采样权重 | Eq. (6) |
| $n_t$ | 每轮迭代的查询数量 | Eq. (6) |
| $d$ | 输入维度 | Theorem 4 |
| $\delta$ | 梯度估计的平滑参数 | Eq. (6) |

**证据强度说明**：AS 的期望成本公式（Theorem 1）和 AGREST 的最优参数公式（Theorem 3）均来自论文的严格证明，置信度为 1.0。初始余弦期望公式（Theorem 4）的推导依赖于 Lévy's Lemma 和球面几何，置信度为 0.95。过冲步长调度器和查询预算调度器来自 Algorithm 1 的伪代码，置信度为 1.0。



## 实验与关键发现

**主实验结果.** 本文在ImageNet数据集上，以ResNet-50和ViT-B/32为主干网络，评估了将Asymmetric Search (AS)和Asymmetric Gradient Estimation (AGREST)集成到HSJA、GeoDA、CGBA、SurFree四种决策型黑盒攻击后的性能。核心指标为中位ℓ₂扰动距离，所有比较均在固定总查询成本下进行，确保公平。表1展示了关键结果：当成本不对称比率c*=2且总成本为15000时，A-HSJA的中位ℓ₂距离为2.06，相比原始HSJA的4.09降低了49.6%；当c*=10²时，A-HSJA的ℓ₂距离为10.74，而HSJA为70.4，降幅达84.7%。在ViT-B/32上，A-CGBA在c*=2时ℓ₂距离为1.42，比CGBA的2.13降低33.3%。这些结果一致表明，AS和AGREST的组合在所有c*值和模型架构下均能显著降低扰动，且优势随c*增大而扩大。在c*=10³时，A-CGBA的ℓ₂距离为6.23，优于CGBA的9.67（降低35.6%）。对于ViT-B/16，A-CGBA在c*=2时ℓ₂距离为0.9，相比CGBA的1.0降低10%，该结果置信度为0.9，需注意其改进幅度较小。

![[assets/figures/papers/iclr26_0002_G1fFulgfd8_A_General_Framework_for_Black-Box_Attacks_Under/figures/003_Table_1.jpg]]
*Table 1: Median $\ell _ { 2 }$ distance for various $c ^ { \star }$ values and different types of attacks across neural network architectures. VA stands for Vanilla Attack. The bold numbers represent the best performance among different variants of each attack for each $c ^ { \star }$ value and model (For a comprehensive analysis of attacks under varying total cost constraints, we refer readers to Tab. 9 and Tab. 10 in App. F, which present exhaustive experimental results across different total cost budgets and query cost $c ^ { \star }$ . .)

**消融分析.** 表1同时提供了AS和AGREST的独立消融结果，以揭示各自贡献。仅使用AS即可在所有c*下降低扰动：例如，在SurFree上c*=2时，ℓ₂距离从4.09降至3.45。仅使用AGREST在大c*下效果显著：在HSJA上c*=10²时，ℓ₂距离从4.66降至2.19，降幅约53%。AS+AGREST联合使用在所有攻击和c*下均优于单独使用任一组件，表明两者在减少高成本查询方面具有互补性。AS通过优化搜索路径降低累积成本，AGREST则通过偏移采样区域和加权减少梯度估计中的高成本查询频率。

**高成本不对称场景.** 图3展示了在c*=10⁴、10⁵和∞（即标记查询成本无限大）的极端场景下，Asymmetric Attacks与先前的不对称成本攻击Stealthy HSJA的对比。在所有三个c*值下，A-HSJA、A-GeoDA和A-CGBA均优于Stealthy HSJA，表现为在相同总成本下实现更低的ℓ₂距离。这表明本文框架不仅适用于中等成本比率，在极端成本不对称下仍能保持优势，而Stealthy HSJA假设良性查询成本为零，忽略了大量低成本查询的累积开销。

**查询成本效率分析.** 图4左图对比了GeoDA中AS与标准二分搜索（binary search）在c*=10³时的累积搜索成本。AS的累积成本显著低于二分搜索，量化结果为二分搜索的成本约为AS的2.5倍（附录C）。这验证了定理1的理论界：AS的期望成本为O(c* log_{c*+1}(1/τ))，相比二分搜索的Θ(c* log(1/τ))有Θ(log(c*+1))倍的改进。图4右图展示了AGREST中低成本查询的理论最优概率与实际经验概率的对比，两者高度吻合，验证了定理3的理论分析。

**超参数敏感性.** 图5和表2分析了超参数m（控制AGREST中采样偏移量）对性能的影响。在c*=10³、总成本150K的设置下，中位ℓ₂距离随m变化呈现U形曲线，存在最优值。表2进一步显示，不同c*值下的最优m可能不同，表明m需要针对具体设置进行调优。本文在实验中固定m独立于c*以简化流程，但指出自动选择m的方法值得探索。

![[assets/figures/papers/iclr26_0002_G1fFulgfd8_A_General_Framework_for_Black-Box_Attacks_Under/figures/009_Table_2.jpg]]
*Table 2: Peformance of HSJA+AGREST to m across different values of $c ^ { \star }$ (25 random images)*

**攻击成功率与迁移性.** 表3和表4报告了在ℓ₂=5和ℓ₂=10约束下的攻击成功率（ASR）。Asymmetric Attacks在所有(c*, 总成本)组合下均取得更高ASR。表5展示了白盒到黑盒的迁移攻击成功率：使用PGD-40在ℓ₂=10下，从ResNet-50源模型迁移到ResNet-152、DenseNet-121、VGG-16等目标模型，Asymmetric Attacks的迁移ASR也优于基线，表明其生成的对抗样本具有更好的泛化性。

![[assets/figures/papers/iclr26_0002_G1fFulgfd8_A_General_Framework_for_Black-Box_Attacks_Under/figures/011_Table_3.jpg]]
*Table 3: ASR (%) under $\ell _ { 2 }$ = 5 for different ( $c ^ { \star }$ , total cost) on ResNet-50

![[assets/figures/papers/iclr26_0002_G1fFulgfd8_A_General_Framework_for_Black-Box_Attacks_Under/figures/012_Table_4.jpg]]
*Table 4: ASR (%) under $\ell _ { 2 }$ = 1 0 for different ( $c ^ { \star }$ , total cost) on ResNet-50

![[assets/figures/papers/iclr26_0002_G1fFulgfd8_A_General_Framework_for_Black-Box_Attacks_Under/figures/017_Table_5.jpg]]
*Table 5: Transfer ASR (%) for different source and target models using PGD-40 with $\ell _ { 2 }$ = 1 0*

**鲁棒性与防御评估.** 表6显示，在PGD训练鲁棒模型（ℓ₂=3）上，Asymmetric Attacks仍保持优势，表明其不仅针对标准模型有效。表7展示了在量化防御下的性能，Asymmetric Attacks同样优于基线，说明其鲁棒性。在CIFAR-10数据集上（表8），Asymmetric Attacks也取得一致改进，验证了方法的跨数据集泛化能力。

**视觉语言模型扩展.** 图8展示了在CLIP模型上的结果：在300次总查询后，Asymmetric Attacks的ℓ₂失真比Stealthy HSJA低40-60%，表明框架可有效扩展到视觉语言模型。该结果置信度为0.9，需注意实验设置的具体细节可能影响结论的普适性。

**失败模式与局限.** 当前框架仅处理二分类（源类 vs 非源类）的不对称成本，未扩展到多目标类各自具有不同查询成本的场景。此外，在大型语言模型（LLM）上的应用面临挑战，因为文本提示是离散的，难以直接应用连续优化方法。超参数m的调优需求也增加了实际部署的复杂性。



## 定位与知识库关联

### 与基线方法的关系

本文提出的非对称攻击框架（Asymmetric Attacks）直接扩展了决策型黑盒攻击谱系中的核心方法——HSJA、GeoDA、CGBA和SurFree。这些基线方法共享一个隐含假设：所有查询的成本相等。在此假设下，边界搜索采用标准的二分搜索（1:1区间分割），梯度估计则围绕边界点进行等权重Monte Carlo采样，导致约一半的查询落入高成本类别。非对称攻击框架通过替换两个关键操作来打破这一假设：将二分搜索替换为非对称搜索（AS），将等权重梯度估计替换为非对称梯度估计（AGREST）。这两个模块可以独立或联合地插入任何决策型攻击中，形成对应的非对称变体（A-HSJA、A-GeoDA、A-CGBA、A-SurFree）。

与先前唯一考虑成本不对称的工作Stealthy HSJA相比，非对称攻击框架在概念和性能上均有本质区别。Stealthy HSJA假设良性查询成本为零，仅优化高成本查询的数量，忽略了大量低成本查询的累积开销；而非对称攻击通过重参数化成本函数 `cost := Q_non-flagged + Q_flagged · c*` 统一处理任意成本比率，并在c*→∞时自然退化为Stealthy的设置。实验表明，在c*=10⁴、10⁵和∞下，A-HSJA在所有总成本预算下均优于Stealthy HSJA（Figure 3），在CLIP模型上ℓ₂失真低40-60%（Figure 8）。这一优势的因果机制在于：非对称攻击同时控制高成本和低成本查询的数量，而非仅压制高成本查询。

### 适用边界

非对称攻击框架的适用性受三个条件约束。第一，成本不对称必须可量化且稳定：攻击者需要知道或能够估计成本比率c*，且该比率在攻击过程中保持不变。第二，决策边界附近的局部线性假设是AS和AGREST理论分析的基础（Assumption A1），当决策边界高度非线性时，AS的区间分割策略和AGREST的偏移采样可能偏离最优。第三，当前框架仅处理二分类场景（源类 vs 非源类），无法直接处理多目标类各自具有不同查询成本的情形。

从实验覆盖范围看，框架在ImageNet上的ResNet-50和ViT-B/32/16上验证有效，在PGD训练鲁棒模型和量化防御下仍保持优势，表明其对模型架构和简单防御的鲁棒性。在CIFAR-10上的结果（Table 8）进一步支持其在小规模数据集上的泛化性。然而，在ViT-B/16上c*=2时A-CGBA的改进幅度仅为10%（ℓ₂从1.0降至0.9），提示在低成本不对称下收益可能边际递减。

### 局限与开放问题

框架引入了一个新的超参数m（控制AGREST中偏移量ω*的缩放），需要针对不同设置调优。Figure 5显示m=0.5在c*=10³时最优，但Table 2表明最优m随c*变化，且在不同c*下性能对m的敏感性不同。目前论文未提供自动选择或迁移m的机制，这是一个实际部署的障碍。

三个明确的开放问题限制了框架的扩展性。第一，如何将框架推广到多目标类场景，其中每个目标类具有不同的查询成本？这需要重新设计搜索和估计策略，因为边界不再是单一的超曲面。第二，如何将框架应用于视觉语言模型（如Vision LLaMA）？这些模型的输出空间是离散的文本token，连续优化方法无法直接应用。第三，如何将AS适配到大型语言模型的越狱攻击？文本提示的离散性质使得二分搜索式的区间分割难以定义，可能需要随机搜索或离散优化的替代方案。此外，决策边界附近局部线性假设的成立范围缺乏定量刻画——当该假设不成立时，AS和AGREST的理论保证（Theorem 1-3）的退化程度未知，这需要进一步的实证或理论分析。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_General_Framework_for_Black_Box_Attacks_Under_Cost_Asymmetry.pdf

![[paperPDFs/ICLR_2026/A_General_Framework_for_Black_Box_Attacks_Under_Cost_Asymmetry.pdf]]
