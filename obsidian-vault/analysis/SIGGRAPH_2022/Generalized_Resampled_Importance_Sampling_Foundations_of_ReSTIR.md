---
title: "Generalized Resampled Importance Sampling: Foundations of ReSTIR"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Generalized_Resampled_Importance_Sampling_Foundations_of_ReSTIR.pdf
project_link: "https://graphics.cs.utah.edu/research/projects/gris/"
code_link: "https://github.com/NVIDIAGameWorks/2021"
aliases:
- GRISGRP
- GRISFR
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 引入广义重采样重要性采样（GRIS）框架，允许从不同域重用相关样本，并使用无偏贡献权重、移位映射和新的重采样 MIS 权重，通过控制目标函数比值、重采样权重方差以及保证充分的 canonical 样本，恢复无偏性和收敛性。
primary_logic: 通过推广 RIS 的样本域和权重定义、引入移位映射连接不同像素的路径、并设计新型 MIS 权重（广义 Talbot / pairwise），即使在重用相关样本时，也能使输出样本的分布渐进收敛至指定目标分布，从而实现渐进完美的零方差重要性采样。
claims:
- GRIS 允许从不同域重用相关样本并进行移位映射，突破 RIS 的 i.i.d. 限制
- GRIS 提供了收敛保证，当重采样权重总和方差趋于零时，输出 PDF 收敛至目标分布
- ReSTIR PT 在实际场景中显著优于 path tracing 和 ReSTIR GI，MAPE 相对降低 74% 以上
- Carousel 上 MAPE (HDR) = 0.39 (ReSTIR PT)
---

# Generalized Resampled Importance Sampling: Foundations of ReSTIR

> [!tip] 核心洞察
> 通过推广 RIS 的样本域和权重定义、引入移位映射连接不同像素的路径、并设计新型 MIS 权重（广义 Talbot / pairwise），即使在重用相关样本时，也能使输出样本的分布渐进收敛至指定目标分布，从而实现渐进完美的零方差重要性采样。

| 字段 | 内容 |
|------|------|
| 中文题名 | 广义重采样重要性采样：ReSTIR 的理论基础 |
| 英文题名 | Generalized Resampled Importance Sampling: Foundations of ReSTIR |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://graphics.cs.utah.edu/research/projects/gris/) · [Code](https://github.com/NVIDIAGameWorks/2021) · [Project](https://graphics.cs.utah.edu/research/projects/gris/") |
| Topic | #topic/other_unclear |
| Method | Generalized Resampled Importance Sampling (GRIS) and ReSTIR PT |
| Dataset | Carousel, Paris Opera House, Kitchen, Various offline scenes |

> [!tip] 效果简介
> - Carousel 上，MAPE (HDR) 0.39 (ReSTIR PT) vs 1.63 (Path Tracing) (76% lower)。
> - Paris Opera House 上，MAPE (HDR) 0.33 (ReSTIR PT) vs 1.28 (Path Tracing) (74% lower)。
> - Kitchen (Fig. 14) 上，MAPE 0.325 (ReSTIR PT reconn.) vs 0.958 (Path Tracing) (66% lower)。

## 概要

原始重采样重要性采样（RIS）理论要求候选样本独立同分布，而 ReSTIR 通过空间和时间重用引入样本相关性，违背了这一基本假设，导致收敛保证缺失，甚至收敛到错误结果。本文提出**广义重采样重要性采样（GRIS）**框架，从理论上突破 RIS 的 i.i.d. 限制，允许从不同域重用相关样本，并通过无偏贡献权重、移位映射和新型 MIS 权重恢复无偏性与收敛性。在此基础上构建的 **ReSTIR PT** 方法，将 ReSTIR 从直接光照扩展到任意长度路径的重用，在实时渲染中以等时间预算显著优于传统路径追踪和 ReSTIR GI——Carousel 场景 MAPE 误差从 1.63 降至 0.39（降低 76%），Paris Opera House 从 1.28 降至 0.33（降低 74%）；在离线渲染中收敛加速最高达 14.4 倍。方法定位上，GRIS 将 RIS 的样本域从单一域推广至多域、将权重定义从精确 PDF 替换为无偏贡献权重，并引入移位映射连接不同像素路径，属于采样理论层面的基础性扩展。

## 核心方法与创新机理

### 问题瓶颈：RIS 的 i.i.d. 假设与 ReSTIR 的相关性悖论

重采样重要性采样（RIS）为 Monte Carlo 积分提供了强大的方差削减工具，但其理论基础建立在严格的独立同分布（i.i.d.）假设之上：所有候选样本 $X_i$ 必须从同一域 $\Omega$ 的同一分布 $p$ 中独立抽取。ReSTIR 系列方法通过空间和时间重用打破了这一假设——相邻像素的水库被合并，导致候选样本之间产生复杂的相关性，且样本来自不同像素的不同路径域。这种相关性违背了 RIS 的收敛保证，甚至可能导致收敛到错误的结果（Fig. 2 的两像素示例直观展示了这一失败模式）。本文的核心贡献在于建立广义重采样重要性采样（GRIS）框架，从理论上解决这一瓶颈。

![[assets/figures/papers/paper_list_l48_https_graphics_cs_utah_edu_research_projects_gris/figures/002_Figure_2.jpg]]
*Figure 2: Imagine a two-pixel image, with ReSTIR [Bitterli et al. 2020] separately integrating two 1D functions (left). ReSTIR promises exponential growth in “effective” sample count at linear cost, but each ReSTIR iteration only adds two new independent samples. Other reused samples are duplicates, causing convergence to the wrong result (right). Our GRIS theory explains when such cases occur and how to guarantee proper convergence. For a less abstract, rendered example of inaccurate convergence due to correlations, see Figure 10b*

### 核心机制：GRIS 对 RIS 的三重推广

GRIS 在三个关键维度上推广了 RIS，使其能够处理相关样本、未知 PDF 和不同域的候选样本：

**1. 样本域泛化与移位映射**

传统 RIS 要求所有候选样本 $X_i$ 来自单一域 $\Omega$。GRIS 允许每个候选样本 $X_i$ 来自任意域 $\Omega_i$，通过移位映射 $T_i: \Omega_i \to \Omega$ 将其转换到目标域 $\Omega$。移位映射是 GRIS 的核心创新之一，其设计需满足双射性（保证雅可比行列式存在且可逆），使得 $Y = T_i(X_i)$ 成为目标域中的有效样本。这一推广直接解决了不同像素路径域不兼容的问题。

**2. 无偏贡献权重替代倒数 PDF**

传统 RIS 需要精确的倒数 PDF $1/p_i(X_i)$ 作为权重因子，但在重用场景中，候选样本的边际 PDF 往往是不可追踪的（例如经过多次重采样后的路径分布）。GRIS 引入无偏贡献权重 $W_i$ 作为替代（Definition 4.1）：

$$\mathbb{E}[f(X)W] = \int_{\text{supp}(X)} f(x) \mathrm{d}x$$

$W_i$ 只需满足期望无偏条件，可以是 $1/p_i(X_i)$ 的无偏估计（如前一帧 RIS 的输出权重），从而解除了对精确 PDF 的依赖。

**3. 广义重采样权重与雅可比修正**

结合上述推广，GRIS 的重采样权重变为（Eq. 7）：

$$w_i = m_i(T_i(X_i)) \, \hat{p}(T_i(X_i)) \, W_i \cdot \left| \frac{\partial T_i}{\partial X_i} \right|$$

其中 $m_i$ 是 MIS 权重，$\hat{p}$ 是目标分布，$W_i$ 是无偏贡献权重，$\left| \partial T_i / \partial X_i \right|$ 是移位映射的雅可比行列式。这一公式将 RIS 的适用范围从单一域、已知 PDF 的 i.i.d. 样本扩展到任意域、未知 PDF 的相关样本。

### 收敛性保证：方差条件与 Canonical 样本

GRIS 不仅保证了无偏性，还提供了收敛性保证。理论分析（Section 4.4, Theorem A.2）表明，当以下条件满足时，输出样本 $Y$ 的分布收敛至目标分布 $\hat{p}$：

$$\text{Var}\left[\sum_{i=1}^{M} w_{M,i}\right] \xrightarrow{M \to \infty} 0$$

这一条件要求重采样权重总和的方差随候选样本数 $M$ 增加而趋于零。在实践中，这意味着必须控制重用样本的“有效”数量：仅扩大空间重用窗口而不增加 canonical 样本（独立于重用的新样本）会导致发散（Fig. 8）。这一发现直接指导了 ReSTIR PT 中 $M_{\text{cap}}$ 参数的设计——将重用计数上限限制为常数 $M_c$ 是保证收敛的关键（Fig. 9a）。

![[assets/figures/papers/paper_list_l48_https_graphics_cs_utah_edu_research_projects_gris/figures/008_Figure_8.jpg]]
*Figure 8: Breaking*

### 新型 MIS 权重：广义 Talbot 与成对 MIS

传统 RIS 使用 Talbot 平衡启发式 $m_i(x) = p_i(x) / \sum_j p_j(x)$ 作为 MIS 权重。GRIS 推广了这一设计，提出两种新型 MIS 权重：

**广义 Talbot 权重**（Eq. 36）：

$$m_i(y) = \frac{\hat{p}_i(y)}{\sum_{j=1}^{M} \hat{p}_j(y)}$$

其中 $\hat{p}_i$ 是代理目标密度，结合了 canonical 样本数量信息。这一设计确保 canonical 样本获得更高的选择权重。

**保守成对 MIS 权重**（Eq. 37-38）：针对防御性场景设计，始终为 canonical 样本分配不低于 $1/M$ 的权重，防止重用样本主导选择过程。实验证实，这两种 MIS 权重实现了渐进零方差积分，而常数 MIS 权重无法收敛（Fig. 7）。

### ReSTIR PT 的模块化管线

基于 GRIS 理论，ReSTIR PT 构建了完整的路径重用管线（Section 6.3）：

**步骤 1：初始候选生成** — 每个像素独立追踪一条路径 $X_i$，作为 canonical 样本。

**步骤 2：时间重用（GRIS）** — 利用时间移位映射 $T_{\text{temporal}}$ 将前一帧对应像素的水库与当前帧水库进行 GRIS 合并。时间移位映射需保持路径的几何对应关系，在动态场景中可能引入偏差。

**步骤 3：空间重用（GRIS）** — 通过移位映射对随机空间邻居的水库进行 GRIS 合并。移位映射包括三种类型：
- **重连移位**（Reconnection Shift）：将重用路径的末端重新连接到当前像素路径的命中点，适用于漫反射和粗糙表面。
- **随机重放移位**（Random Replay Shift）：通过复制随机数生成相似方向的路径，适用于镜面和光泽表面。
- **混合移位**（Hybrid Shift）：结合重连和随机重放，根据表面粗糙度自适应选择策略（Fig. 5）。

![[assets/figures/papers/paper_list_l48_https_graphics_cs_utah_edu_research_projects_gris/figures/006_Figure_5.jpg]]
*Figure 5: A hybrid shift mapping. The base path selects*

**步骤 4：最终估计** — 计算选定样本 $Y$ 的无偏贡献权重 $W_Y = \frac{1}{\hat{p}(Y)} \sum_{j=1}^{M} w_j$，并估计像素积分 $f(Y) \cdot W_Y$。

**MIS 权重评估**（贯穿步骤 2-3）：在每次重用操作中，使用广义 Talbot 或保守成对 MIS 权重计算 $m_i$，确保 canonical 样本获得足够的选择概率。

### 关键公式的因果链条

GRIS 的理论体系通过以下因果链实现从相关样本到无偏收敛积分的转化：

1. **移位映射** $T_i$ 将不同域的样本统一到目标域，雅可比行列式 $\left| \partial T_i / \partial X_i \right|$ 修正域变换引入的密度变化。
2. **无偏贡献权重** $W_i$ 解除了对精确 PDF 的依赖，使重用样本的权重可追踪。
3. **广义重采样权重** $w_i$ 结合 MIS 权重 $m_i$、目标密度 $\hat{p}$ 和雅可比修正，确保选择概率与目标分布成比例。
4. **方差条件** $\text{Var}[\sum w_i] \to 0$ 保证输出分布渐进收敛至 $\hat{p}$，实现渐进完美的零方差重要性采样。
5. **Canonical 样本约束** 防止重用样本的方差累积导致发散，$M_{\text{cap}}$ 参数是这一约束的工程实现。

这一理论框架将 ReSTIR 从经验性工程方法提升为具有严格收敛保证的数学框架，为后续研究（如体积介质移位映射、自动参数调优）提供了理论基础。

![[assets/figures/papers/paper_list_l48_https_graphics_cs_utah_edu_research_projects_gris/figures/009_Figure_7.jpg]]
*Figure 7: Single-sample integration error with GRIS, with increasing input samples from each pixel within a 7×7 reuse window. Asymptotic zero-variance integration is realized with generalized Talbot and pairwise MIS weights but not with constant MIS weights (red)*

## 实验与关键发现

### 主结果：ReSTIR PT 的误差与加速比

GRIS 框架的直接产物 ReSTIR PT 在实时和离线场景中均表现出对传统路径追踪（PT）和前一版 ReSTIR GI 的显著提升。在 Fig. 1 的两个高复杂度场景中，以 HDR MAPE 为指标，ReSTIR PT 在等时间预算（80 ms, 1920×1080）下将误差降低超过 74%：Carousel 场景从 PT 的 1.63 降至 0.39，Paris Opera House 从 1.28 降至 0.33。作为对比，ReSTIR GI 的 MAPE 分别为 0.45 和 0.39，说明将重用从直接光照扩展到全长路径（长度 10）带来了额外的质量增益。

![[assets/figures/papers/paper_list_l48_https_graphics_cs_utah_edu_research_projects_gris/figures/001_Figure_1.jpg]]
*Figure 1: Our new generalized resampled importance sampling (GRIS) theory extends resampled importance sampling [Talbot 2005] to guarantee convergence even when applied to correlated samples arising from spatiotemporal reuse (i.e., Bitterli et al. [2020]). GRIS allows applying ReSTIR to reuse arbitrary paths, shown with paths of length 10 in the Carousel and Paris Opera House. Main images compare naive path tracing and our new ReSTIR PT in equal time (80 ms at 1920 × 1080). Insets show equal-time path tracing, ReSTIR GI [Ouyang et al. 2021], our ReSTIR PT, plus a converged reference. We significantly improve quality for glossy interreflection, reflections, refractions, and other high-frequency lighti...*

在离线渲染模式下，ReSTIR PT 的重连移位（reconnection shift）在 Kitchen 场景（Fig. 14）中将 MAPE 从 PT 的 0.958 降至 0.325，降幅 66%。以收敛速度衡量，Fig. 17 显示 ReSTIR PT 在多个离线场景中达到同等误差所需时间仅为 PT 的 1/14.4，最高加速达 14.4 倍。

在视觉质量上（Fig. 13），San Miguel 场景的间接光照部分显示 ReSTIR PT 对焦散（caustics）有实质性降噪：重连移位擅长处理接触焦散，而混合移位在远距离焦散上表现更优。玻璃兔子场景（等时间 25 ms）进一步验证了不同移位映射在焦散类型上的互补性。

### 关键消融实验

**MIS 权重的收敛性**（Fig. 7）是最具决定性的消融。在单样本 GRIS 积分中，随着 7×7 重用窗口内每个像素的输入样本数增加，广义 Talbot MIS 权重（Eq. 36）和保守成对 MIS 权重（Eq. 37, 38）实现了渐进零方差积分，而常数 MIS 权重（红色曲线）无法收敛。这直接验证了定理 A.2 的核心条件：只有当重采样权重总和的方差趋于零时，输出样本分布才收敛至目标分布。

**空间重用窗口与 canonical 样本的平衡**（Fig. 8）揭示了 GRIS 收敛保证的一个关键边界条件。实验固定一个中心 canonical 样本（|R| = 1），逐渐扩大周围重用像素窗口。即使使用了正确的 MIS 权重，若中心像素不产生新的 canonical 样本，方差随窗口扩大而增加——这证明重采样权重总和方差趋于零的条件要求 canonical 样本数量与重用窗口大小保持适当比例，单纯扩大重用半径反而有害。

**M-cap 对时间重用的影响**（Fig. 9）是理解 ReSTIR 实践中收敛行为的关键。Fig. 9a 显示，在包含时间重用的 ReSTIR PT 中，过大的 M-cap（将 M_r 上限设得过高）最终导致噪声增加；过小的 M-cap 无法充分降低误差；适中的 M-cap（绿色曲线）给出持续稳定的低误差。Fig. 9b 进一步表明，在离线模式下关闭时间重用（仅空间 GRIS）比包含时间重用收敛更快，因为时间重用引入了帧间相关性，在平均多帧时反而阻碍收敛。这与 Fig. 2 的理论警示一致：相关样本重用若不加控制，会收敛到错误结果。

**移位映射的选择**（Fig. 11）表明混合移位（重连 + 随机重放）在光泽和镜面表面上优于纯重连移位。在粗糙场景中两者表现接近，但在光泽表面场景中混合移位的误差显著更低。Fig. 12 的消融进一步显示，基于单个 BSDF 瓣的移位映射（lobe-specific shift）减少了噪声并缩短了渲染时间，热力图表明它降低了多瓣材质上的平均路径长度。

### 与 BPR 的对比

Fig. 14 将 ReSTIR PT 与双向路径重用方法 BPR（Bekaert et al., EGSR 2002）进行了等时间对比（Kitchen 场景, 33 ms）。BPR 在低样本数下虽能降低误差，但产生了分散注意力的结构性伪影（structural artifacts）；ReSTIR PT 在同样利用空间重用的情况下，误差更低且无结构性伪影。这归因于 GRIS 的无偏贡献权重和 MIS 权重设计，避免了 BPR 中因重用引入的偏差。

### 失败模式与适用边界

论文明确指出了若干限制条件：

1. **屏幕空间实现的采样不足**：细小几何体或高频光照（如锐利焦散）在屏幕空间重用中可能被遗漏，导致噪声、条纹或斑块。Fig. 13 中两种移位映射在不同焦散类型上的分工也暗示单一移位映射难以同时覆盖所有光路类型。

2. **时间重用的偏差风险**：时间重用依赖精确的双射时间移位映射，在动态场景（运动物体、材质变化）中难以保证，可能引入偏差。Fig. 9b 的离线实验已证实关闭时间重用反而加速收敛。

3. **参数敏感性**：M-cap、重用半径和粗糙度阈值等参数需要手动调节，目前缺乏自动设置机制。Fig. 9a 中 M-cap 选择的敏感性直接体现了这一限制。

4. **体积介质缺失**：论文未提供体积介质中的高效移位映射，限制了 ReSTIR PT 在参与介质场景中的应用。

5. **颜色噪声**：波谱域的颜色噪声问题尚未解决，需要在未来工作中探索跨波长重用或英雄波长（hero wavelength）策略。

![[assets/figures/papers/paper_list_l48_https_graphics_cs_utah_edu_research_projects_gris/figures/010_Figure_9.jpg]]
*Figure 9: (a) Error of ReSTIR PT with temporal reuse, with increasing frame counts and different ??-cap values. A large ??-cap eventually increases noise, while low values do not minimize error. Good ??-caps (green) give consistently low errors. (b) Our offline method (blue) turns off temporal reuse, which converges faster when averaging frames; it avoids the frame-to-frame correlation introduced by temporal reuse*

## 定位与知识库关联

本文的核心贡献在于为**重采样重要性采样（RIS）**理论提供了一个根本性的推广，将原有理论中严格的独立同分布（i.i.d.）假设替换为允许相关样本和跨域重用的广义框架。这一推广直接改变了 RIS 理论中 **“样本域与独立性”** 这一关键 slot：从 Talbot (2005) 原始 RIS 要求的“所有候选样本必须来自同一域 Ω 且相互独立”，转变为 GRIS 中“允许候选样本来自任意域 Ω_i、可相关、且通过移位映射 T_i: Ω_i → Ω 转换至目标域”。

相对于已有的 ReSTIR 工作，本文的定位尤为清晰。**ReSTIR DI**（Bitterli et al., SIGGRAPH 2020）和 **ReSTIR GI**（Ouyang et al., EGSR 2021）在工程上成功实现了时空样本重用，但其理论基础仍依附于 RIS 的 i.i.d. 假设，导致在重用相关样本时缺乏收敛保证，甚至在特定情况下收敛至错误结果（如 Fig. 2 所示的两像素示例）。本文通过 GRIS 框架为这些工程实践提供了严格的理论基础，明确了收敛所需的条件——即重采样权重总和的方差趋于零（Eq. 23）、充分的 canonical 样本数量、以及被积函数与目标密度的比值有界。这一理论补全使得 ReSTIR 类方法从“启发式有效”提升为“有保证渐进收敛”。

在知识库中的挂载点，GRIS 可被定位为**蒙特卡洛积分与重要性采样理论**的一个新节点。它向上连接至：
- **Talbot (2005)** 的 RIS 理论（提供基本无偏性框架和归一化方法）；
- **Veach & Guibas (1995)** 的多重重要性采样（MIS），尤其是平衡启发式权重；
- **梯度域渲染**中的移位映射概念（Lehtinen et al., SIGGRAPH 2013），GRIS 将其推广为跨域样本转换的通用工具。

向下则催生了 **ReSTIR PT**——首个将时空重用应用于完整路径的实时路径追踪器。这一应用的关键创新在于设计了三种移位映射（重连、随机重放、混合），将不同像素的路径双射映射至当前像素的路径空间，从而使 GRIS 的重采样机制能够在路径积分上运作。与 **BPR**（Bekaert et al., EGSR 2002）等早期空间路径重用方法相比，ReSTIR PT 在低样本数下避免了结构性伪影，且误差显著降低（Kitchen 场景 MAPE: BPR 未报告具体数值，但 Fig. 14 显示 ReSTIR PT 在等时间对比中明显优于 BPR 和路径追踪）。

GRIS 的适用边界值得注意。理论上，框架允许任意域的重用，但实践中受限于移位映射的设计质量。当前实现仅支持屏幕空间内的重用，对细小几何体或高频光照（如锐利焦散）可能出现欠采样噪声（Fig. 13 显示不同移位映射擅长不同类型的焦散）。时间重用需要精确的双射时间移位映射，在动态场景中难以保证，可能引入偏差——这正是 Fig. 9b 显示离线场景关闭时间重用反而收敛更快的原因。此外，框架要求被积函数 f 与目标密度 p̂ 的比值有界，这在路径空间中通过截断或 Russian roulette 近似满足，但并非严格成立。

后续研究可从以下几个方向展开：
1. **自动参数设置**：当前 M-cap、重用半径、粗糙度阈值等参数需手动调节，如何根据场景特征自动设置是实用化的关键。
2. **体积介质移位映射**：本文未提供体积散射介质中的高效移位映射，这限制了 GRIS 在参与介质渲染中的应用。
3. **波谱域重用**：颜色噪声问题（不同波长的路径被错误重用）需要在波谱域设计更精细的移位映射或 MIS 权重。
4. **流形探索移位**：局部移位决策的局限性（如重连移位只能改变路径的一个顶点）可能通过流形探索方法克服，以同时处理接触焦散和远距离焦散。
5. **引导重采样**：如何为动画或材质变化后的重新渲染引导重采样过程，是一个开放问题。

总体而言，GRIS 在理论层面将 RIS 从“独立同分布”的窄域推广至“相关跨域”的广域，在实践层面为 ReSTIR 类方法提供了收敛保证，其核心洞察——通过无偏贡献权重、移位映射和新型 MIS 权重的组合，即使重用相关样本也能渐进收敛至目标分布——为实时和离线渲染中的样本重用技术奠定了统一的理论基础。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Generalized_Resampled_Importance_Sampling_Foundations_of_ReSTIR.pdf]]