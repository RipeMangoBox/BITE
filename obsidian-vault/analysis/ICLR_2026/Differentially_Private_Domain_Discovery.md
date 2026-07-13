---
title: "Differentially Private Domain Discovery"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Differentially_Private_Domain_Discovery.pdf
project_link: null
code_link: null
openreview_forum_id: yBpzF8hp3J
aliases:
- WGMWA2
- DPDD
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "加权高斯机制（WGM）的用户贡献限制 Δ₀ 和噪声/阈值参数，以及将目标定义为缺失质量而非简单的发现项数。"
primary_logic: "将集合并问题重新表述为缺失质量，并利用 Zipfian 数据特性，WGM 可获得近乎最优的 ℓ1 缺失质量保证。同时，将 WGM 作为域发现预处理步骤，可将已知域算法扩展到未知域场景。"
claims:
- "WGM 在 Zipfian 数据上具有近乎最优的 ℓ1 缺失质量。"
- "WGM 具有一个分布无关的 ℓ∞ 缺失质量保证。"
- "WGM 作为域发现预处理步骤，可为 top-k 和 k-hitting set 提供新效用保证。"
- "六个真实数据集 (Reddit, Amazon Games, Movie Reviews, Steam Games, Amazon Magazine, Ama... 上 Missing Mass (MM) = WGM"
---

# Differentially Private Domain Discovery

> [!tip] 核心洞察
> 将集合并问题重新表述为缺失质量，并利用 Zipfian 数据特性，WGM 可获得近乎最优的 ℓ1 缺失质量保证。同时，将 WGM 作为域发现预处理步骤，可将已知域算法扩展到未知域场景。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 差分隐私域发现 |
| 英文题名 | Differentially Private Domain Discovery |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=yBpzF8hp3J) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Weighted Gaussian Mechanism (WGM) 及其元算法 (Algorithm 2) |
| Dataset | 六个真实数据集 (Reddit, Amazon Games, Movie Reviews, Steam Games, Amazon Magazine, Amazon Pantry), 三个小数据集 (Steam Games |

> [!tip] 效果简介
> - 六个真实数据集 (Reddit, Amazon Games, Movie Reviews, Steam Games, Amazon Magazine, Ama... 上，Missing Mass (MM) 为 WGM，对比 Policy Gaussian / Policy Greedy，变化 WGM 的 MM 保持在对比机制的 5% 以内。
> - 三个小数据集 (Steam Games, Amazon Magazine, Amazon Pantry) 上，Top-k Missing Mass 为 WGM + Peeling Exponential，对比 Limited-domain top-k (Durfee & Rogers 2019)，变化 更小的 Top-k MM（一致优于）。
> - 三个小数据集 (Steam Games, Amazon Magazine, Amazon Pantry) 上，Number of missed users 为 WGM + User Peeling，对比 Non-private baseline (public domain) and known-domain private algorithm，变化 性能与已知域非私有基线相当，有时更优。

## 概要

**核心问题**：在差分隐私（DP）下进行“域发现”（domain discovery）——即从多个用户各自持有的项集中识别出所有出现过的项——面临一个根本性瓶颈：域未知，现有算法缺乏可证明的效用保证，且难以在隐私保护与缺失质量之间取得良好权衡。

**核心思路**：本文将集合并问题重新表述为**缺失质量**（missing mass, MM）的最小化，而非简单追求发现项的数量。基于这一视角，作者采用并分析了**加权高斯机制**（Weighted Gaussian Mechanism, WGM），其关键控制旋钮包括用户贡献限制 $\Delta_0$、噪声/阈值参数，以及利用 Zipfian 数据特性获得近乎最优的 $\ell_1$ 缺失质量保证。

**方法定位**：WGM 本身是一个简单且可扩展的集合并算法（源自 Gopi et al., 2020），本文将其作为“域发现预处理步骤”，与现有的已知域私有 top-k 和 k-hitting set 算法组合，形成元算法（Algorithm 2），从而将已知域算法的效用保证扩展到未知域场景。

**主要结果**：
- **理论上**，WGM 在 Zipfian 数据上具有近乎最优的 $\ell_1$ 缺失质量保证（Theorem 3.3），同时拥有一个分布无关的 $\ell_\infty$ 缺失质量保证（Theorem 3.6）。
- **实验上**，在六个真实数据集上，WGM 的缺失质量保持在策略机制（Policy Gaussian / Policy Greedy）的 5% 以内（Figure 1）；在 top-k 和 k-hitting set 任务中，WGM + Peeling 组合算法一致优于现有未知域基线（Figure 2, Figure 3）。
- **消融分析**表明，增大 $\Delta_0$ 可有效降低子采样误差，从而改善缺失质量。

**局限与开放问题**：$\ell_1$ 缺失质量的理论上下界之间仍存在间隙；实验仅在固定隐私预算 $(1, 10^{-5})$-DP 下进行；$\ell_1$ 保证依赖 Zipfian 假设，更一般分布下仅有 $\ell_\infty$ 保证。

在推荐系统、基因组关联分析、文本语料库挖掘等应用中，数据常常以“用户-集合”的形式存在：每个用户贡献一个项目集合，而分析的目标是从全体用户的并集中发现一个高质量的子集。例如，从用户购买记录中发现热门商品，或从基因组数据中发现高频变异位点。这类任务统称为**域发现**（domain discovery），其核心挑战在于：域本身是未知的，算法必须在没有先验项目列表的情况下，从分布式、可能重叠的用户集合中筛选出有意义的项目。

当引入**差分隐私**（differential privacy, DP）约束时，域发现问题变得尤为困难。现有工作大多假设域是已知且公开的，算法只需在有限候选集上进行私有选择。然而，在域未知的真实场景中，算法面临双重困境：

1. **缺乏可证明的效用保证**：由于域未知，现有 DP 算法无法提供关于输出质量的严格理论界，尤其是当效用度量从简单的“发现项数”转向更贴近实际的**缺失质量**（missing mass, MM）时——即未被输出集覆盖的项目频率之和。
2. **隐私与效用的权衡难以控制**：在域发现中，每个用户可能贡献大量项目，直接对原始计数加噪会注入过多噪声；而限制用户贡献又可能丢弃重要信息。如何在隐私预算、用户贡献限制和最终缺失质量之间取得可预测的平衡，是此前方法未能系统解决的问题。

本文的核心洞察在于：将域发现的目标重新表述为**缺失质量的最小化**，而非简单地最大化发现项数。缺失质量天然地惩罚遗漏高频项的行为，更符合下游任务对“覆盖重要内容”的实际需求。基于这一视角，作者聚焦于一种已在实践中使用的简单机制——**加权高斯机制**（Weighted Gaussian Mechanism, WGM），并证明当数据满足**Zipfian性质**（即项目频率呈多项式衰减，这在真实数据中普遍成立）时，WGM 可以获得近乎最优的 $\ell_1$ 缺失质量保证（Theorem 3.3）；同时，该机制还具备一个**分布无关的 $\ell_\infty$ 缺失质量保证**（Theorem 3.6），使其在最坏情况下仍有理论兜底。

更关键的是，WGM 可以作为“域发现预处理步骤”，与现有的已知域私有算法无缝组合：先用 WGM 从全体用户并集中筛选出一个有限候选域 $D$，再在 $D$ 上运行已知域的 top-k 选择或 k-hitting set 算法。这一元算法框架（Algorithm 2）将已知域方法的效用保证首次扩展到了未知域场景，为私有 top-k 和 k-hitting set 问题提供了新的理论界（Theorem 4.3, Theorem 4.5）。

在实验层面，作者在六个真实数据集（Reddit、Amazon Games、Movie Reviews、Steam Games、Amazon Magazine、Amazon Pantry）上验证了上述主张：WGM 在集合并任务上的缺失质量保持在策略机制（Policy Gaussian / Policy Greedy）的 5% 以内（Figure 1）；在 top-k 缺失质量上，WGM 组合算法一致优于现有的有限域 top-k 基线（Durfee & Rogers, 2019）（Figure 2）；在 k-hitting set 任务上，其性能与已知域的非私有基线相当甚至更优（Figure 3）。

综上所述，本文通过重新定义效用度量、利用 Zipfian 数据特性、以及提出域发现与已知域算法的组合范式，系统性地填补了差分隐私域发现在理论保证和实用效能之间的缺口。

## 核心方法与创新机理

本工作的核心创新在于将差分隐私下的域发现问题从“发现项的数量”这一传统视角，重新表述为**缺失质量 (Missing Mass)** 的优化问题，并基于此提出了**加权高斯机制 (Weighted Gaussian Mechanism, WGM)**。这一视角转换直接催生了三个关键的“changed slots”，构成了方法的核心贡献。

**瓶颈洞察**：在差分隐私下进行域发现时，由于真实域未知，现有算法（如 Policy Gaussian 机制, Gopi et al., 2020；Policy Greedy 机制, Carvalho et al., 2022）缺乏可证明的效用保证，且难以在隐私保护与遗漏关键项之间取得良好权衡。根本原因在于，传统方法以“发现多少项”为优化目标，而忽略了被遗漏项的频率分布——在典型的幂律分布数据中，遗漏一个高频项比遗漏多个低频项的代价大得多。

**因果旋钮**：WGM 通过三个关键设计来扭转上述权衡：

1. **效用度量替换**：将目标从发现项数改为缺失质量
   $$ \mathrm{MM}(W, S) := \sum_{x \in \bigcup_i W_i \setminus S} \frac{N(x)}{N} $$
   这一定义直接惩罚高频项的遗漏，使隐私预算的分配天然倾向于保留“重要的”项。相应地，在 top-k 选择中采用 Top-k 缺失质量 $\mathrm{MM}^k(W,S)$ 作为度量，而非简单的准确率。

2. **加权用户贡献**：WGM 在构建直方图时，对每个用户 $i$ 的项赋予权重 $1/\sqrt{|\widetilde{W}_i|}$（而非等权或无权），即
   $$ \widetilde{H}(x) = \sum_{i=1}^{n} \left( \frac{1}{|\widetilde{W}_i|} \right)^{1/2} \mathbf{1}\{x \in \widetilde{W}_i\} $$
   这一加权策略有效控制了来自“大用户”（拥有大量项的用户）的贡献方差，是 WGM 在 Zipfian 数据上获得近乎最优 $\ell_1$ 缺失质量保证的关键（Theorem 3.3）。相比之下，其他 DP 集合并算法未采用此类加权。

3. **用户项数限制与子采样**：WGM 通过参数 $\Delta_0$ 限制每个用户最多贡献的项数，并采用无放回随机抽样。这一设计不仅限定了敏感度，也直接控制了子采样引入的误差——理论表明，子采样误差可能主导缺失质量，因此应使 $\Delta_0$ 尽可能接近 $\max_i |W_i|$（见消融分析）。

**核心洞察**：利用 Zipfian 数据特性（频率以多项式衰减），WGM 可获得近乎最优的 $\ell_1$ 缺失质量保证（Theorem 3.3），同时具备一个分布无关的 $\ell_\infty$ 缺失质量保证（Theorem 3.6）。更重要的是，WGM 可作为**域发现预处理步骤**嵌入元算法（Algorithm 2）：先用一半隐私预算运行 WGM 获得有限域 $D$，再用另一半预算在该域上运行已知域算法（如 Peeling Exponential Mechanism 用于 top-k，或 User Peeling Mechanism 用于 k-hitting set）。这一设计将已知域算法的效用保证**扩展到了未知域场景**，为 top-k（Theorem 4.3）和 k-hitting set（Theorem 4.5）提供了新的可证明效用界。

**证据强度**：上述创新点均有严格理论支撑——$\ell_1$ 缺失质量上界（Theorem 3.3）与下界（Theorem 3.5）在 $\epsilon$ 和 $N$ 的依赖上匹配至对数因子，表明 WGM 在 Zipfian 假设下近乎最优。实验部分在六个真实数据集上验证了 WGM 的集合并缺失质量保持在 Policy 机制的 5% 以内（Figure 1），且 WGM + Peeling 的组合在 top-k 缺失质量上一致优于 Limited-domain top-k 基线（Durfee & Rogers, 2019）（Figure 2）。

本文提出了一种面向差分隐私域发现的元算法框架，其核心思路是将“未知域”问题转化为“已知域”问题：先用一个隐私集合并（set union）算法获取一个有限候选域，再在该候选域上运行现有的已知域私有选择算法。

### 问题建模

设有 $n$ 个用户，每个用户 $i$ 持有一个项集 $W_i$，整体数据集记为 $W = (W_1, \dots, W_n)$。全局项全集为 $\bigcup_i W_i$，总规模 $M$ 可能极大甚至无限。所有算法需满足**健全性**（Assumption 1）：输出集 $S$ 必须是输入数据集中出现过的项，即 $S \subseteq \bigcup_i W_i$。

效用度量采用**缺失质量**（Missing Mass, MM），而非简单的发现项数：

$$\mathrm{MM}(W, S) := \sum_{x \in \bigcup_i W_i \setminus S} \frac{N(x)}{N}$$

其中 $N(x)$ 为项 $x$ 在全体用户中的出现频次，$N = \sum_x N(x)$ 为总条目数。缺失质量衡量的是未被输出集覆盖的项所占的频率份额，更贴近实际应用中对“覆盖质量”的需求。

### 元算法流程（Algorithm 2）

整个框架由两个阶段级联而成，共享总隐私预算 $(\varepsilon, \delta)$：

1. **域发现阶段**：以 $(\varepsilon/2, \delta/2)$ 的隐私预算运行**加权高斯机制**（Weighted Gaussian Mechanism, WGM），从原始数据集 $W$ 中输出一个有限候选域 $D$。
2. **已知域选择阶段**：以剩余 $(\varepsilon/2, \delta/2)$ 的预算，在域 $D$ 上运行现有的已知域私有算法 $B$（如 peeling exponential mechanism 做 top-k 选择，或私有贪心算法做 k-hitting set），得到最终输出集 $S$。

```
输入: 用户数据集 W, 用户贡献上限 Δ₀, 隐私预算 (ε, δ), 目标参数 k
阶段1: D ← WGM(W, Δ₀, ε/2, δ/2)     // 域发现
阶段2: S ← B(W, D, k, ε/2, δ/2)     // 已知域私有选择
输出: S
```

### WGM 内部模块

WGM 是域发现阶段的核心算子，由四个子模块串联构成：

1. **子采样（Subsampling）**：对每个用户 $i$，从其项集 $W_i$ 中无放回随机抽取 $\min\{\Delta_0, |W_i|\}$ 个项，构造截断数据集 $\widetilde{W}$。$\Delta_0$ 是用户贡献上限，限制了每个用户对输出的最大影响。
2. **加权直方图（Weighted Histogram）**：计算每个项 $x$ 的加权计数：
   $$\widetilde{H}(x) = \sum_{i=1}^{n} \frac{1}{\sqrt{|\widetilde{W}_i|}} \cdot \mathbf{1}\{x \in \widetilde{W}_i\}$$
   权重 $1/\sqrt{|\widetilde{W}_i|}$ 的设计使得用户级 $\ell_2$ 敏感度受控，是后续高斯噪声隐私分析的基础。
3. **高斯噪声注入（Gaussian Noise Addition）**：对每个项的加权计数添加独立高斯噪声 $Z_x \sim \mathcal{N}(0, \sigma^2)$，得到噪声计数 $\widetilde{H}'(x) = \widetilde{H}(x) + Z_x$。
4. **阈值筛选（Thresholding）**：输出噪声计数超过阈值 $T$ 的所有项：$D = \{x : \widetilde{H}'(x) \geq T\}$。

噪声参数 $\sigma$ 和阈值 $T$ 需满足 Theorem 3.2 给出的条件以保证 $(\varepsilon, \delta)$-DP，其渐近取值为：
$$\sigma = \Theta\left(\frac{1}{\varepsilon}\sqrt{\log(1/\delta)}\right), \quad T = \tilde{\Theta}_{\Delta_0,\delta}\left(\max\{\sigma, 1\}\right)$$

### 设计要点

- **$\Delta_0$ 的选取**：子采样引入的误差可能主导缺失质量，因此 $\Delta_0$ 应尽可能接近 $\max_i |W_i|$，以最小化信息损失。
- **效用度量的转变**：将优化目标从“发现项数”转为“缺失质量”，使理论分析能够与数据分布（特别是 Zipfian 性质）挂钩，从而获得近乎最优的 $\ell_1$ 缺失质量保证（Theorem 3.3）。在无法假设 Zipfian 分布时，WGM 仍有一个分布无关的 $\ell_\infty$ 缺失质量保证（Theorem 3.6）。
- **级联隐私预算分配**：两阶段各占一半预算，在实验中固定为 $(1, 10^{-5})$-DP 总量，未探索其他分配比例（这是该框架的一个已知局限）。

### 问题形式化：缺失质量（Missing Mass）

论文将域发现的质量度量从传统的“发现项数”转向**缺失质量（Missing Mass, MM）**。给定用户项集集合 $W = \{W_1, \dots, W_n\}$ 和输出集 $S$，缺失质量定义为未被 $S$ 覆盖的项的频率之和：

$$\mathrm{MM}(W, S) := \sum_{x \in \bigcup_i W_i \setminus S} \frac{N(x)}{N}$$

其中 $N(x)$ 是项 $x$ 在全体用户中出现的总次数，$N = \sum_x N(x)$ 是总出现次数。这一度量直接反映“遗漏了多少高频项”，比单纯计数更能刻画域发现的效用损失。论文进一步引入广义缺失质量 $\mathrm{MM}_p$，取 $\ell_p$ 范数；$p=1$ 即为标准 MM，$p=\infty$ 则退化为最大缺失频率。

### WGM 的三阶段流水线

**加权高斯机制（Weighted Gaussian Mechanism, WGM）** 是本文的核心集合并算法，参数为噪声水平 $\sigma > 0$、阈值 $T \geq 1$ 和用户贡献上限 $\Delta_0 \geq 1$。算法分三个阶段执行：

1. **子采样（Subsampling）**：对每个用户 $i$，从其项集 $W_i$ 中无放回随机抽取 $\min\{\Delta_0, |W_i|\}$ 个项，构造子采样数据集 $\widetilde{W}$。这一步将每个用户的贡献量限制在 $\Delta_0$ 以内，是控制敏感度的关键。

2. **加权直方图（Weighted Histogram）**：对每个项 $x$ 计算加权计数：
   $$\widetilde{H}(x) = \sum_{i=1}^{n} \left( \frac{1}{|\widetilde{W}_i|} \right)^{1/2} \mathbf{1}\{x \in \widetilde{W}_i\}$$
   权重 $1/\sqrt{|\widetilde{W}_i|}$ 的设计使得每个用户对直方图的 $\ell_2$ 敏感度贡献被均匀化，这是 WGM 区别于无加权或等权方案的**核心因果旋钮**。

3. **加噪与阈值筛选**：对每个 $x$ 添加独立高斯噪声 $Z_x \sim \mathcal{N}(0, \sigma^2)$，得到 $\widetilde{H}'(x) = \widetilde{H}(x) + Z_x$，然后输出 $S = \{x : \widetilde{H}'(x) \geq T\}$。

### 隐私约束与参数选取

为保证 $(\varepsilon, \delta)$-DP，$\sigma$ 和 $T$ 需满足 Theorem 3.2 给出的精确条件，其渐近形式为：

$$\sigma = \Theta\left(\frac{1}{\varepsilon}\sqrt{\log(1/\delta)}\right), \quad T = \tilde{\Theta}_{\Delta_0, \delta}\left(\max\{\sigma, 1\}\right)$$

这里的 $\tilde{\Theta}$ 隐藏了对数因子。**关键洞察**：阈值 $T$ 需要随 $\sigma$ 和 $\Delta_0$ 增长，以控制假阳性（纯噪声项被输出）的概率。

### 缺失质量的理论保证

在数据满足 **Zipfian 性质**（频率呈多项式衰减，Definition 3.1）的假设下，WGM 具有近乎最优的 $\ell_1$ 缺失质量保证（Theorem 3.3）：

$$\operatorname{MM}(W,S) = \tilde{O}_{\beta,C,N}\left(\frac{C^{1/s}}{s-1}\left(\frac{\max_i|W_i|}{N\sqrt{q^\star}}\right)^{\frac{s-1}{s}}(T+\sigma)^{\frac{s-1}{s}}\right)$$

其中 $(C,s)$ 是 Zipfian 参数，$q^\star$ 是隐私参数相关的量。代入 $\sigma$ 和 $T$ 的 DP 约束后（Corollary 3.4），上界进一步简化为：

$$\mathrm{MM}(W,S) \leq \tilde{O}_{\beta,\delta,\Delta_0,C,N}\left(\frac{C^{1/s}}{s-1}\left(\frac{\max_i|W_i|}{\varepsilon N\sqrt{q^\star}}\right)^{\frac{s-1}{s}}\right)$$

该界的**因果机制**：缺失质量由两部分误差构成——子采样误差（由 $\Delta_0$ 控制）和噪声引起的漏报误差（由 $\sigma$ 和 $T$ 控制）。当 $\Delta_0$ 接近 $\max_i |W_i|$ 时，子采样误差最小化；这也是实验消融中“增大 $\Delta_0$ 降低 MM”的理论依据。

对于**不满足 Zipfian 的一般分布**，WGM 退而求其次，提供一个分布无关的 $\ell_\infty$ 缺失质量保证（Theorem 3.6），确保最大遗漏频率有界。

### 元算法：从域发现到已知域任务

WGM 作为域发现预处理步骤，嵌入到 **Algorithm 2（元算法）** 中：将总隐私预算平分，前半部分运行 WGM 获得有限域 $D$，后半部分在 $D$ 上运行已知域私有算法（如 Peeling Exponential Mechanism 做 top-k，或 User Peeling Mechanism 做 k-hitting set）。

以 **top-k 缺失质量**为例，组合算法的效用保证为（Theorem 4.3）：

$$\mathrm{MM}^k(W,S) \leq \tilde{O}_{\beta,\delta,\Delta_0}\left(\frac{k}{N}\left(\frac{\max_i |W_i|}{\varepsilon\sqrt{q^\star}} + \frac{\sqrt{k}\log(M)}{\varepsilon}\right)\right)$$

该界的**瓶颈**在于第一项来自 WGM 域发现的误差传播，第二项来自已知域 top-k 算法本身的误差。类似地，k-hitting set 的近似保证为（Theorem 4.5）：

$$\mathrm{Hits}(W,S) \geq \left(1 - \frac{1}{e}\right)\operatorname{Opt}(W,k) - \tilde{O}_{\beta,\delta,\Delta_0}\left(\frac{k \cdot \max_i |W_i|}{\varepsilon\sqrt{q^\star}} + \frac{k^{3/2}}{\varepsilon}\log(Mk)\right)$$

即保留贪心算法的 $(1-1/e)$ 近似比，附加一个与域发现误差相关的加性损失项。

### 已知局限与未闭合问题

- 上界与下界之间存在间隙：Theorem 3.5 给出的下界为 $\Omega\big(\frac{C^{1/s}}{s-1}(\frac{1}{\varepsilon N})^{(s-1)/s}\big)$，与上界在 $\max_i |W_i|$ 和 $q^\star$ 的依赖上未完全匹配。
- 上述 $\ell_1$ 保证强依赖于 Zipfian 假设；在更一般分布下仅有 $\ell_\infty$ 保证，能否获得更一般的 $\ell_1$ 保证仍是开放问题。
- top-k 和 k-hitting set 的上下界同样未闭合，缩小这些差距是论文提出的自然后续方向。

## 实验与关键发现

### 实验设置

实验在六个真实数据集上进行：Reddit、Amazon Games、Movie Reviews、Steam Games、Amazon Magazine 和 Amazon Pantry。数据集规模差异显著，Amazon Games 拥有最多用户（约 154 万），Reddit 拥有最多项（约 15 万）和最多用户-项交互对（约 3200 万）。所有实验均采用固定总隐私预算 $(1, 10^{-5})$-DP，其中元算法（Algorithm 2）将预算均分给 WGM 域发现阶段和后续已知域私有多选阶段。用户贡献限制 $\Delta_0$ 在集合并实验中作为横轴变量探索，在 top-k 和 k-hitting set 实验中固定为 100。

### 集合并缺失质量主结果

Figure 1 展示了三个大数据集（Reddit、Amazon Games、Movie Reviews）上集合并缺失质量（MM）随 $\Delta_0$ 变化的曲线。核心发现是：**WGM 在所有数据集和 $\Delta_0$ 取值下的缺失质量均保持在策略机制（Policy Gaussian 和 Policy Greedy）的 5% 以内**。这一结果验证了 WGM 作为集合并算法的竞争力——尽管策略机制是专门为集合并设计的，WGM 在实用层面几乎不损失效用。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_yBpzF8hp3J/figures/003_Figure_1.jpg]]
*Figure 1: Set Union MM as a function of $\Delta _ { 0 }$ . Note that lower is better*

消融分析显示，增大 $\Delta_0$ 一致地降低缺失质量，这与理论分析一致：子采样误差是缺失质量的主导因素之一，因此应尽可能将 $\Delta_0$ 设为接近 $\max_i |W_i|$。当 $\Delta_0$ 较小时，子采样丢弃大量用户项导致高频项可能被遗漏；随着 $\Delta_0$ 增大，加权直方图捕获更多真实高频项，噪声阈值筛选后的遗漏减少。

### 数据分布验证

Figure 4 和 Figure 5 分别展示大数据集和小数据集的频率-排名对数-对数图。所有数据集均呈现近似线性衰减趋势，验证了数据近似满足 Zipfian 分布假设。这为 WGM 的 $\ell_1$ 缺失质量理论保证（Theorem 3.3）提供了经验支撑——Zipfian 性质使得高频项集中，WGM 能以高概率捕获它们。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_yBpzF8hp3J/figures/013_Figure_4.jpg]]
*Figure 4: Log-log plot of frequency vs. rank for large datasets*

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_yBpzF8hp3J/figures/016_Figure_5.jpg]]
*Figure 5: Log-log plot of frequency vs. rank for small datasets*

### Top-k 缺失质量结果

Figure 2 展示了三个小数据集（Steam Games、Amazon Magazine、Amazon Pantry）上的 top-k 缺失质量。对比基线为 Durfee & Rogers (2019) 的 limited-domain top-k 机制。结果表明：**WGM + Peeling Exponential Mechanism 的组合方法在所有 k 值下一致获得更小的 top-k 缺失质量**。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_yBpzF8hp3J/figures/006_Figure_2.jpg]]
*Figure 2: Top-k MM as a function of k , using $\Delta _ { 0 }$ = 1 0 0*

这一优势的来源在于 WGM 域发现阶段产生了一个比全集 $\bigcup_i W_i$ 更小但仍包含高质量项的域 $D$。这个缩减的域降低了 Peeling Exponential Mechanism 的搜索空间和有效灵敏度，使其在相同隐私预算下能更准确地选择真正的 top-k 项。

### k-Hitting Set 结果

Figure 3 展示了 k-hitting set 任务上遗漏用户数随 k 的变化。对比基线包括：非私有基线（已知完整域）和已知域私有算法。结果显示，**WGM + User Peeling Mechanism 的组合方法与两个基线方法性能相当，有时甚至更优**。这一反直觉现象的解释在于：WGM 域发现产生的域 $D$ 虽然小于真实域，但滤除了大量低频噪声项，使得后续贪心算法在缩减域上反而能做出更有效的选择。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_yBpzF8hp3J/figures/009_Figure_3.jpg]]
*Figure 3: Number of missed users as a function of k, using $\Delta _ { 0 }$ = 1 0 0*

### 失败模式与局限

尽管理论和实验均表明 WGM 在 Zipfian 数据上表现优异，但存在以下局限：

1. **分布依赖**：$\ell_1$ 缺失质量保证依赖 Zipfian 假设。在非 Zipfian 分布上只能获得较弱的 $\ell_\infty$ 保证（Theorem 3.6），实验未覆盖此类场景，实际表现需手动验证。

2. **隐私预算固定**：所有实验仅使用 $(1, 10^{-5})$-DP 单一预算设置，未系统探索不同 $\epsilon$ 值下的效用变化趋势。

3. **上下界间隙**：top-k 缺失质量的上界（Theorem 4.3）与下界（Section 4.1）之间存在量级差距，k-hitting set 的界同样未匹配，表明理论分析尚有改进空间。

4. **$\Delta_0$ 选择**：虽然增大 $\Delta_0$ 改善效用，但在用户项数差异极大的数据集中，设置过大的 $\Delta_0$ 会增加灵敏度，需在隐私与效用间权衡。实验未给出 $\Delta_0$ 的自适应选择策略。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_yBpzF8hp3J/figures/010_Table_1.jpg]]
*Table 1: Number of users, items, and entries (user-item pairs) for each dataset*

## 定位与知识库关联

### 核心瓶颈与设计动机

在差分隐私（DP）下进行域发现面临一个根本性困境：域本身是未知的，算法不能依赖预先给定的候选项全集。现有算法的效用度量通常基于“发现了多少项”，但这一度量无法区分发现高频项与低频项的价值差异。本文的核心洞察是将问题重新表述为**缺失质量**（Missing Mass, MM）——即未被输出集覆盖的项的频率之和——从而在隐私与效用之间建立更精细的权衡关系。

### 与基线方法的关系

**集合并（Set Union）基线**。本文以 **Policy Gaussian mechanism**（Gopi et al., 2020）和 **Policy Greedy mechanism**（Carvalho et al., 2022）作为集合并任务的主要对比方法。这两种策略机制在已知域假设下运行，能够访问完整的项全集以进行阈值筛选。WGM 在未知域设定下，通过加权直方图和高斯噪声注入，在六个真实数据集上将缺失质量保持在策略机制的 5% 以内（Figure 1），表明其在实际效用上接近已知域方法的上限。

**Top-k 基线**。对于 top-k 选择任务，唯一的未知域基线是 **Limited-domain top-k mechanism**（Durfee & Rogers, 2019）。该方法直接在原始数据上运行，不进行显式的域发现预处理。本文提出的 WGM + Peeling Exponential Mechanism 组合算法在所有三个小数据集上一致获得更小的 top-k 缺失质量（Figure 2），验证了“先发现域，再在有限域上运行已知域算法”这一元策略的有效性。

**k-Hitting Set 基线**。k-hitting set 任务对比了非私有基线（使用公开域）和已知域私有算法。实验表明，WGM + User Peeling 组合算法的性能与两种基线方法相当，有时甚至更优（Figure 3）。作者将此归因于 WGM 域发现步骤产生的域虽然小于全集 $\bigcup_i W_i$，但保留了高质量项，从而降低了后续 Peeling 机制的求解难度。

### 方法谱系中的定位

从方法谱系来看，WGM 及其元算法（Algorithm 2）处于两条研究线的交汇处：

1. **差分隐私集合并与直方图发布**：WGM 本身继承自 Gopi et al.（2020）的加权高斯机制，其关键改造在于引入用户贡献限制 $\Delta_0$ 和加权方案 $1/\sqrt{|\tilde{W}_i|}$，使得敏感度可控的同时保持对高频项的偏好。与策略机制不同的是，WGM 不需要预先知道域的大小或分布。

2. **差分隐私 top-k 与子模最大化**：元算法将 WGM 作为域发现预处理步骤，然后调用已知域的 Peeling Exponential Mechanism（top-k）或私有贪心算法（k-hitting set）。这种“先发现域，再在域上求解”的分解策略，将未知域问题规约到已知域问题，使得已有的已知域算法可以无缝复用。

### 关键假设与适用边界

WGM 的理论保证依赖于两个核心假设：

- **Zipfian 数据假设**：$\ell_1$ 缺失质量的近乎最优上界（Theorem 3.3）要求数据频率服从多项式衰减，即数据集是 $(C,s)$-Zipfian 的。在更一般的分布下，只能得到分布无关的 $\ell_\infty$ 缺失质量保证（Theorem 3.6），其效用界显著弱于 $\ell_1$ 界。实验数据集的 log-log 频率-排名图（Figure 4, Figure 5）展示了不同程度的 Zipfian 特性，但并非所有真实数据都严格满足这一假设。

- **健全性假设（Assumption 1）**：所有算法输出的项必须来自输入数据集中出现的项。这一假设排除了生成新项或合成项的可能性，将问题限定在纯粹的“发现”而非“生成”框架内。

$\Delta_0$ 参数的选择构成了隐私-效用的直接调节旋钮：增大 $\Delta_0$ 可减少子采样误差，从而降低缺失质量，但会增加敏感度，需要更大的噪声来维持相同的隐私保证。理论分析和实验（Figure 1）均表明，子采样误差在 $\Delta_0$ 较小时可能主导缺失质量，因此建议将 $\Delta_0$ 设置得尽可能接近 $\max_i |W_i|$。

### 局限与开放问题

本文留下了若干未解决的问题：

1. **上下界间隙**：$\ell_1$ 缺失质量的上界（Theorem 3.3）与下界（Theorem 3.5）之间存在差距，top-k 和 k-hitting set 的界也未匹配。缩小这些间隙是直接的理论改进方向。

2. **数据依赖的子采样**：当前 WGM 使用均匀无放回抽样来限制用户贡献。若能根据数据特性设计自适应的子采样策略（例如优先保留高频项），可能在不增加隐私成本的前提下进一步降低缺失质量。

3. **分布假设的松弛**：$\ell_1$ 保证严重依赖 Zipfian 假设。能否在更一般的分布族（如重尾分布或具有平滑衰减特性的分布）下获得类似的 $\ell_1$ 保证，是一个重要的开放问题。

4. **隐私预算的分配**：实验仅探索了固定的 $(1, 10^{-5})$-DP 预算。元算法将预算平分给 WGM 和已知域算法，但最优的预算分配比例可能因任务和数据特性而异，值得系统研究。

## 原文 PDF

![[paperPDFs/ICLR_2026/Differentially_Private_Domain_Discovery.pdf]]
