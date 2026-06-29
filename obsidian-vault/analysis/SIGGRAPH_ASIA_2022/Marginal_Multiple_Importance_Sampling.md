---
title: Marginal Multiple Importance Sampling
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Marginal_Multiple_Importance_Sampling.pdf
project_link: null
code_link: null
aliases:
- MMISMMPSM
- MMIS
tags:
- SIGGRAPH_ASIA_2022
- topic/other_unclear
core_operator: 将每个边际化域视为一个连续的技术空间，随机选择技术并重用辅助变量-样本对来近似边际积分，从而将多个边缘技术组合成无偏估计器。
primary_logic: 边际分布可以看作具有边际PDF的单一采样技术，多个这样的边际技术能够以类似于经典MIS的方式进行组合，产生实用的无偏估计器。
claims:
- MMIS估计器在至少存在一个条件技术对被积函数非零的区域提供正密度的条件下，是所求积分的无偏估计。
- 所提出的多顶点路径滤波和多顶点光子滤波在复杂光照场景下（尤其间接光区域）相比先前方法显著降低了误差。
- Indoor room scene (Fig. 2) 上 Visual error after 350s rendering = Multi-vertex path filtering (ours)
- Caustic-heavy scene (Fig. 3) 上 Visual error after 120s rendering = Multi-vertex photon filtering (ours)
---

# Marginal Multiple Importance Sampling

> [!tip] 核心洞察
> 边际分布可以看作具有边际PDF的单一采样技术，多个这样的边际技术能够以类似于经典MIS的方式进行组合，产生实用的无偏估计器。

| 字段 | 内容 |
|------|------|
| 中文题名 | 边缘化的多重重要性采样 |
| 英文题名 | Marginal Multiple Importance Sampling |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](http://www.iliyan.com/publications/MarginalMIS) |
| Topic | #topic/other_unclear |
| Method | Marginal Multiple Importance Sampling (MMIS) / Marginal Path Sampling (MPS) |
| Dataset | Indoor room scene, Caustic-heavy scene, Canonical 1D function, Canonical 4-technique marginal setup |

> [!tip] 效果简介
> - Indoor room scene (Fig. 2) 上，Visual error after 350s rendering Multi-vertex path filtering (ours) vs Path tracing (PT) / West et al. single-vertex filtering (Significantly lower error, better convergence in indirectly lit areas)。
> - Caustic-heavy scene (Fig. 3) 上，Visual error after 120s rendering Multi-vertex photon filtering (ours) vs Photon mapping (PM) / Deng et al. iterative filtering (Reduced error in indirectly lit areas; handles complex caustic lighting better)。
> - Canonical 1D function (Fig. 1) 上，Variance of the estimator MMIS mixing classical and marginal techniques vs Classical MIS only / SMIS with one marginal technique (Lower variance than either baseline alone)。

## 概要

传统多重重要性采样（MIS）要求每个采样技术具备可直接求值的概率密度函数（PDF），但许多高效路径采样技术依赖边际化PDF——需通过积分消除辅助变量，难以实时计算，导致大量技术无法投入实际使用。本文提出边缘化多重重要性采样（MMIS），核心思路是将每个边际化域视为一个连续技术空间，随机选择技术并重用辅助变量-样本对来近似边际积分，从而将多个边缘技术组合为无偏估计器。在此基础上，进一步构建了边缘路径采样（MPS）框架，实现多顶点路径滤波与多顶点光子滤波。实验表明，在复杂光照场景下，所提方法在间接光区域相比路径追踪、光子映射及先前滤波方法显著降低了误差，且MMIS估计器在至少一个条件技术对被积函数非零区域提供正密度时保持无偏。该方法将SMIS从单一技术空间推广至多技术空间，使此前因边际PDF不可算而无法使用的采样技术得以实际应用。

## 核心方法与创新机理

### 问题瓶颈：不可计算的边际PDF阻碍采样技术组合

在渲染的蒙特卡洛积分框架中，像素值的无偏估计需要计算采样技术的概率密度函数（PDF）。经典多重重要性采样（MIS, Veach and Guibas 1995）通过平衡启发式组合多个采样技术，要求每个技术的PDF $p_i(x)$ 可直接求值。然而，大量有效的路径采样技术依赖**边际化PDF**——即需要先采样一个辅助变量 $t$，再条件采样 $x$，其PDF形式为：

$$p_i(x) = \int_{\mathcal{T}_i} p_i(x,t) \mathrm{d}t = \int_{\mathcal{T}_i} p_i(x|t) p_i(t) \mathrm{d}t$$

这个边际积分在渲染场景中通常无法实时计算，导致许多强大的采样技术（如路径滤波中重用辅助顶点构造新路径的技术）无法被纳入MIS框架，严重限制了采样策略的设计空间。West et al. (2020) 提出的随机MIS（SMIS）虽然处理了**单一**技术空间内的边际化问题，但无法组合来自**多个不同**技术空间的边际技术。

### 核心洞察：将边际分布视为单一采样技术

本文的关键洞察在于：**一个技术空间上的边际分布可以被看作一个具有边际PDF的单一采样技术（称为“边际技术”），而多个这样的边际技术可以像经典MIS组合经典技术一样被组合起来**。这打破了“每个技术的PDF必须可直接计算”的限制，将MIS的理论框架从有限个经典技术扩展到包含连续技术空间的边际技术。

### 三个关键Changed Slots

**Slot 1：技术空间定义——从有限集到多连续空间**

- **基线（MIS）**：有限个经典采样技术，每个技术的PDF可直接点值。
- **基线（SMIS）**：单一连续技术空间，通过辅助变量 $t$ 标识空间内的具体技术。
- **本文（MMIS）**：**多个技术空间** $\{\mathcal{T}_i\}_{i=1}^T$，每个空间对应一个边际化域。经典技术可被视作退化的单点技术空间（trivial space），因此MMIS统一了经典技术和边际技术。

**Slot 2：PDF求值——从精确边际到条件PDF平均**

- **基线**：需要精确计算每个技术的边际PDF $p_i(x)$。
- **本文**：仅需计算**条件PDF** $p_i(x|t)$。边际积分通过在所有采样到的辅助变量-样本对 $(t_{i',j'}, x_{i',j'})$ 上平均条件PDF来近似估计。这彻底规避了显式边际积分。

**Slot 3：权重方案——从精确分母到样本重用近似**

- **基线（平衡启发式）**：权重分母为所有技术精确PDF的加权和 $\sum_{i'} n_{i'} p_{i'}(x)$。
- **本文**：分母被近似为所有技术-样本对的条件PDF之和 $\sum_{i'}\sum_{j'} p_{i'}(x|t_{i',j'})$，**重用**生成样本的同一批辅助变量对来估计边际积分。这种“自举”式的分母构造是保证无偏性的关键。

### 方法框架与模块顺序

MMIS估计器从经典MIS出发，经过三步推导得到：

**模块1：技术标识符采样（Technique Identifier Sampling）**

对于每个边际技术空间 $i$，首先从辅助变量分布中采样 $t \sim p_i(t)$。这个 $t$ 标识了技术空间内的一个具体“条件技术”。例如在路径滤波中，$t$ 可以是用于构造新路径的辅助顶点集。

**模块2：条件样本生成（Conditional Sample Generation）**

利用采样到的 $t$，从条件分布 $p_i(x|t)$ 生成样本 $x$。这个条件PDF是可直接计算的——例如给定辅助顶点后，通过连接或扰动生成新路径顶点的概率是可求的。

**模块3：分母累积（Denominator Accumulation）**

对所有技术空间的所有采样对 $(i',j')$，评估其条件PDF在目标样本 $x_{i,j}$ 处的值，并求和形成MMIS权重分母：

$$\langle I \rangle_{\mathrm{MMIS}} = \sum_{i=1}^{T} \sum_{j=1}^{n_i} \frac{f(x_{i,j})}{\sum_{i'=1}^{T} \sum_{j'=1}^{n_{i'}} p_{i'}(x_{i,j}|t_{i',j'})}$$

该估计器的关键性质是：**只要至少存在一个采样到的条件技术在被积函数非零的区域提供正密度，它就是所求积分的无偏估计**。分母中条件PDF的求和近似了理想MIS中的边际PDF求和，这种近似引入额外方差，但保持无偏性。

**模块4：无偏像素估计（Unbiased Pixel Estimation）**

将MMIS框架应用于路径采样，得到边缘路径采样（MPS）估计器。对于 $T$ 个边际路径采样技术，像素值估计为：

$$\langle I_k \rangle_{\mathrm{MPS}} = \sum_{i=1}^{T} \sum_{j=1}^{n_i} \frac{f(\overline{\mathbf{x}}_{i,j})}{\sum_{i'=1}^{T} \sum_{j'=1}^{n_{i'}} p_{i'}(\overline{\mathbf{x}}_{i,j}|\overline{\mathbf{t}}_{i',j'})}$$

其中 $\overline{\mathbf{x}}_{i,j}$ 是第 $i$ 个技术生成的第 $j$ 条路径，$\overline{\mathbf{t}}_{i',j'}$ 是对应的辅助变量。分母展开后为每顶点条件PDF的乘积之和：

$$\sum_{i'=1}^{T} \sum_{j'=1}^{n_{i'}} \prod_{k'=1}^{k} p_{i'}(\mathbf{x}_{i,j,k'}|\overline{\mathbf{y}}_{i',j',k'})$$

### 计算复杂度的关键优化

直接计算上述分母需要 $O(T \cdot n \cdot k)$ 的复杂度（$k$ 为路径顶点数）。本文的关键实现优化在于：将分母从**乘积之和**重组为**和之乘积**，使计算复杂度从指数级降至线性级。这一重组利用了不同技术-样本对之间条件PDF项的重复性，是MPS在实际渲染中可行的核心工程贡献。

### 因果链路总结

```
边际PDF不可计算（瓶颈）
    → 将边际分布视为单一技术（核心洞察）
    → 定义多技术空间（Slot 1改变）
    → 仅需条件PDF求值（Slot 2改变）
    → 重用样本对近似边际积分（Slot 3改变）
    → MMIS无偏估计器成立
    → 应用于路径采样得到MPS框架
    → 分母重组优化使计算可行
    → 多顶点路径/光子滤波实现
```

### 边界条件与适用限制

MMIS框架要求能够计算条件PDF $p_i(x|t)$，因此**不适用于真实分布未知的技术**（如MCMC采样）。此外，每个边际技术空间内需要采样多个技术标识符 $n_i$ 来控制近似方差——$n_i$ 越大，附加方差越小，但计算开销线性增长。实际路径滤波实现中采用了**有偏近似**（假设滤波核内所有顶点可见性相同以避免额外光线投射），在理论上偏离了无偏性，但显著降低了计算成本并保持了视觉质量。

![[assets/figures/papers/paper_list_l64_http_www_iliyan_com_publications_MarginalMIS/figures/009_Figure_3.jpg]]
*Figure 3: A scene lit predominantly by caustics and indirect light from caustics, which is challenging for both bidirectional path tracing and the filtering method of Deng et al. [2021]. Photon mapping shows improvement, but exhibits artifacts in indirectly lit areas. Our filtered variant better handles the complex lighting in this scene and shows reduced error in indirectly lit areas. The zoom-ins show results after 120s of rendering, and all methods use a fixed-radius kernel*

## 实验与关键发现

### 主结果：渲染质量对比

MMIS 框架在两类渲染任务上进行了端到端验证：**多顶点路径滤波**（针对一般全局光照）和**多顶点光子滤波**（针对焦散主导场景）。实验采用等时渲染对比，以视觉误差为主要评判依据。

**室内场景（Figure 2，350 秒渲染）**：路径追踪（PT）逐像素独立采样，噪声明显。West et al. (2020) 的单顶点滤波虽复用顶点构建新路径，但其权重计算开销极大，仅能追踪少量初始路径，导致贡献被模糊成显眼的块状伪影。Deng et al. (2021) 的迭代滤波与本文的多顶点滤波均最大化顶点复用，收敛速度显著更快。本文方法在间接光照区域表现出更低的误差和更少的关联伪影，整体视觉质量明显优于单顶点滤波和路径追踪基线。

**焦散场景（Figure 3，120 秒渲染）**：场景光照以焦散及其间接光为主，这对双向路径追踪和 Deng et al. 的滤波方法均构成挑战。光子映射（PM）有所改善，但在间接光照区域存在伪影。本文的滤波变体能更好地处理复杂光照，在间接光照区域误差降低明显。所有方法均使用固定半径核以保证公平对比。

### 规范函数实验：方差分析

在一维规范函数上，MMIS 的性质得到了定量验证（Figure 1）：

![[assets/figures/papers/paper_list_l64_http_www_iliyan_com_publications_MarginalMIS/figures/001_Figure_1.jpg]]
*Figure 1: Top: Our MMIS estimator can mix classical (top square) and marginal (bottom square) techniques to achieve lower variance than prior theory can. Bottom: MMIS approximates a (hypothetical) MIS estimator that evaluates marginal PDFs (here, four) exactly. The additional variance vanishes the number of techniques sampled from each technique space increases*

- **混合优势（Figure 1 上）**：MMIS 能够混合经典技术（PDF 可直接求值）和边缘技术（PDF 需边际化），其方差低于仅使用经典 MIS 或仅使用 SMIS（单一边缘技术空间）。这直接验证了核心主张：将多个边缘技术空间纳入 MIS 框架可获得比先前理论更低的方差。
- **近似质量（Figure 1 下）**：在 4 个边缘技术的设置下，MMIS 近似于一个假设的、能精确求值边缘 PDF 的 MIS 估计器。随着每个技术空间中采样的技术数量 n 增加，MMIS 引入的附加方差趋于零。这证实了 MMIS 估计器是可控近似：以线性增长的计算开销换取渐近无偏的方差表现。

### 关键消融与设计权衡

**技术采样数量 n 的影响**：增加每个边缘技术中采样的辅助变量-技术对数量 n，可系统性降低 MMIS 的附加方差（Figure 1 下），但计算开销线性增长。实际应用中 n 的选择需要在方差和性能间权衡。

**有偏可见性近似的引入**：理论上的 MPS 估计器要求对每个条件技术评估完整的条件 PDF，这在路径滤波中需要为每个顶点对投射可见性光线。实际实现采用了有偏近似——假设滤波核内的所有顶点具有相同的可见性（Section 5.1）。这一近似虽然偏离了理论无偏性，但避免了大量额外的可见性光线投射，显著降低了计算成本，且在视觉质量上获得了可接受的折衷。

**顶点聚类方案**：为降低 PDF 评估开销，实际系统对顶点进行聚类。聚类引入可控偏差，但换取了大幅降低的计算复杂度——权重分母的计算从指数级重组为线性级（Eq. 14 的重组）。

### 失败模式与适用边界

1. **对采样技术的要求**：MMIS 框架要求能够计算给定辅助变量 t 条件下样本 x 的条件 PDF $p_i(x|t)$。对于 MCMC 等真实分布未知的采样技术，该框架不适用。这限制了可组合的技术类型。

2. **内存开销**：路径滤波和光子滤波需要额外存储顶点及权重信息。在 1280×720 分辨率下，内存开销可达约 800 MB，对高分辨率渲染或内存受限场景构成压力。

3. **附加方差与计算成本的权衡**：虽然增加 n 可使附加方差趋于零，但线性增长的计算成本意味着在严格的时间预算下，MMIS 的实际表现受限于 n 的选择。论文未提供 n 的最优选择理论分析，这仍是开放问题。

4. **有偏近似的影响**：实际系统中采用的统一可见性假设在可见性变化剧烈的场景（如复杂遮挡几何体）下可能引入显著偏差，但论文未对此进行系统的敏感性分析。该点需要手动验证。

5. **与现有框架的统一**：论文指出路径滤波和光子滤波尚未统一到如 VCM/UPS 的框架中，且路径图中出现环（cycle）时的方差减少潜力未被探索，表明当前应用仍限于特定路径拓扑。

![[assets/figures/papers/paper_list_l64_http_www_iliyan_com_publications_MarginalMIS/figures/007_Figure_2.jpg]]
*Figure 2: Comparison of several methods after 350s of rendering. Path tracing (PT) renders every pixel independently and shows noise. West et al.’s [2020] filtering reuses vertices to construct novel paths but its computationally intensive weight computation affords tracing only a small number of initial pathsMVPF(inline) whose contributions are blurred into conspicuous artifacts. Deng et al.’s [2021] iterative filtering and our multi-vertex filtering maximize vertex reuse and are much faster, showing significant improvement. Though different in formulation, these two methods are similar in implementation and performance*

## 定位与知识库关联

### 1. 相对已有方法的本质差异

MMIS 的核心改变在于**技术空间的定义与 PDF 求值方式**这两个相互耦合的 slot。经典 MIS（Veach & Guibas, 1995）要求每个采样技术具备可直接逐点求值的 PDF，这从根本上排除了大量需要边际化辅助变量的实用采样技术。West et al.（2020）的 SMIS 首次将单一技术空间视为连续统，通过重用辅助变量-样本对来近似边际积分，但其框架仅支持一个技术空间，无法组合多个不同的边际技术。

MMIS 将这一思路推广至**多个技术空间**：每个边际化域被建模为一个独立的技术空间，允许同时混合经典技术（退化为平凡空间）和多个边际技术。关键改变在于，MMIS 的权重分母不再依赖精确的边际 PDF，而是用所有技术-样本对的条件 PDF 之和来近似——这一近似虽然引入附加方差，但保持了无偏性（在至少一个条件技术对被积函数非零区域提供正密度的条件下）。相比 SMIS，MMIS 将“可组合的技术集合”从单一连续空间扩展为多个异构空间，从而解锁了路径滤波、光子滤波等先前无法纳入 MIS 框架的技术。

在路径采样层面，Deng et al.（2021）的迭代路径滤波通过顶点重用实现加速，但其权重计算与 MMIS 存在本质差异：Deng et al. 的方法在数学推导上并非 MIS 框架下的无偏估计器，而 MMIS 的多顶点路径滤波（MPS）在理论上具有无偏性保证（尽管实际实现中因可见性近似引入偏差）。两者的实现与性能相似，但 MMIS 提供了更清晰的理论基础。

### 2. 知识库挂载点

MMIS 在知识库中的挂载点位于**多重重要性采样理论**与**路径采样/密度估计框架**的交汇处：

- **上游依赖**：MMIS 直接建立在经典 MIS（Veach & Guibas, 1995）的平衡启发式权重框架之上，其无偏性证明继承了 MIS 的基本结构。同时，MMIS 的边际积分近似策略源自 SMIS（West et al., 2020）的样本重用机制。
- **下游可挂载模块**：MMIS 作为一个通用的估计器框架，可以承载任何满足“条件 PDF 可求值”的边际采样技术。论文中展示了两个实例——多顶点路径滤波和多顶点光子滤波——但框架本身对具体技术的选择是开放的。
- **与邻近工作的关系**：MMIS 与 Deng et al.（2021）的迭代滤波在实现层面高度相似（顶点聚类、内核估计），但在理论定位上不同：前者是 MIS 框架的推广，后者是迭代重建方法。这使得 MMIS 可以借用 MIS 的方差分析工具，而 Deng et al. 的方法则需要不同的收敛性分析路径。

### 3. 适用边界

MMIS 的适用边界由以下条件划定：

- **必要条件**：每个参与组合的边际技术，其条件 PDF $p_i(x|t)$ 必须可逐点求值。这排除了 MCMC 等真实分布未知的采样技术。
- **偏差-方差-开销权衡**：MMIS 的无偏性以附加方差为代价，该附加方差随每个技术空间中采样的技术数量 $n$ 增加而消失，但计算开销线性增长。实际应用中，$n$ 的选择需要在方差与性能之间权衡。
- **内存开销**：路径滤波和光子滤波需要额外存储顶点和权重，在 1280×720 分辨率下可达约 800 MB，限制了在高分辨率或内存受限场景下的直接应用。
- **实际实现的偏差**：为降低计算成本，论文在可见性评估中采用了有偏近似（假设内核内所有顶点可见性相同），这偏离了理论无偏性。在遮挡边界附近可能产生偏差。
- **不适用场景**：对于辅助变量空间极大或条件 PDF 求值本身代价高昂的技术，MMIS 的分母累加步骤可能成为瓶颈。

### 4. 后续启发与开放问题

MMIS 为后续研究提供了几个明确的方向：

- **统一框架**：论文指出，将路径滤波和光子滤波统一到如 VCM/UPS 的框架中是一个自然延伸。MMIS 的多技术空间组合能力为此提供了理论基础。
- **去偏策略**：当前实现中顶点聚类引入的偏差如何通过聚类半径递减方案消除，甚至实现完全无偏，是一个重要的理论问题。
- **最优 $n$ 的方差分析**：每个技术空间中采样技术数量 $n$ 的最优选择涉及附加方差与计算开销的平衡，目前缺乏定量分析工具。
- **路径图中的环**：论文提到路径图中出现环（cycle）时可能带来方差减少潜力，但如何正确使用这些环仍待探索。
- **与其他渲染技术的整合**：MMIS 框架是否能够容纳双向路径追踪中的顶点连接技术、光子映射中的密度估计技术等，值得进一步研究。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Marginal_Multiple_Importance_Sampling.pdf]]