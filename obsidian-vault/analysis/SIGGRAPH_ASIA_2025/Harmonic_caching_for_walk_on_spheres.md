---
title: "Harmonic caching for walk on spheres"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2025/Harmonic_caching_for_walk_on_spheres.pdf
project_link: "https://cs.dartmouth.edu/~wjarosz/publications/zhou25harmonic.html"
aliases:
- HCH
- HCWS
tags:
- SIGGRAPH_ASIA_2025
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "利用调和函数在球内的解析傅里叶级数展开替代点估计：通过从球边界发射蒙特卡洛随机游走估计傅里叶系数，然后利用径向衰减的基函数在球内任意位置重建解，从而将边界信息高效传播到整个区域，并可通过自适应重叠球实现全局求解。"
primary_logic: "调和函数在球内的展开本质上是均值性质的一般化，它将边界信息压缩为少量傅里叶系数，结合径向解析缩放实现降维；低阶截断即可在大部分区域内获得高精度重建，而随机截断可消除偏差。通过覆盖域的重叠缓存记录并进行加权混合，可以将局部重建扩展为全局连续解，在同等计算量下显著降低误差和伪影。"
claims:
- "在同等时间内，调和缓存的误差比传统逐点WoS低一个数量级以上。"
- "在所有2D测试场景的30分钟收敛过程中，HC始终取得最低的相对均方误差。"
- "相比边界值缓存和均值缓存，HC产生的相关伪影更少且误差更低。"
- "截断阶数L=10且在球半径的0.9倍范围内重建，偏差可保持极低。"
---

# Harmonic caching for walk on spheres

> [!tip] 核心洞察
> 调和函数在球内的展开本质上是均值性质的一般化，它将边界信息压缩为少量傅里叶系数，结合径向解析缩放实现降维；低阶截断即可在大部分区域内获得高精度重建，而随机截断可消除偏差。通过覆盖域的重叠缓存记录并进行加权混合，可以将局部重建扩展为全局连续解，在同等计算量下显著降低误差和伪影。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Walk on Spheres的调和缓存方法 |
| 英文题名 | Harmonic caching for walk on spheres |
| 会议/期刊 | SIGGRAPH Asia 2025 |
| Links | [paper](https://cs.dartmouth.edu/~wjarosz/publications/zhou25harmonic.pdf); [Project](https://cs.dartmouth.edu/~wjarosz/publications/zhou25harmonic.html) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Harmonic Caching (HC) |
| Dataset | 2D Laplace/Dirichlet/Neumann/Robin 场景集 (Fig.9), Poisson方程（稀疏源项，Fig.11）, 3D Screened Laplace（火鸡腿模型，Fig.14）, 收敛性分析（2D场景，~30分钟运行，Fig.10） |

> [!tip] 效果简介
> - 2D Laplace/Dirichlet/Neumann/Robin 场景集 (Fig.9) 上，Relative MSE (scaled by 100, 1%异常值剔除) 为 最低误差（在所有场景中相对MSE远低于对比方法），对比 WoSt、RWoS、BVC、MVC的误差更高，变化 相比传统WoSt误差降低约一个数量级，且较其它缓存方法亦有显著优势。
> - Poisson方程（稀疏源项，Fig.11） 上，Relative MSE 为 最低误差，对比 RWoS（在有利场景下），变化 HC在源项为狄拉克脉冲的场景下仍获得更低误差。
> - 3D Screened Laplace（火鸡腿模型，Fig.14） 上，Relative MSE (~1500秒等时预算，1%异常值剔除) 为 最低误差，对比 WoSt, BVC, MVC等，变化 显著降低噪声，重建平滑度最优。

## 概述

求解椭圆型偏微分方程（PDE）是计算机图形学与物理仿真中的核心任务。无网格蒙特卡洛方法——尤其是**Walk on Spheres（WoS）**及其衍生方法——因其对复杂几何的天然适应性和逐点求解能力而备受关注。然而，传统WoS方法存在根本性的效率瓶颈：每次随机游走仅估计单个点的解，导致逐点估计方差大，在要求密集或高精度解场的场景下计算成本极高。

为缓解这一问题，研究者提出了多种基于缓存的方差缩减方法，如**边界值缓存（BVC）**和**均值缓存（MVC）**。这些方法试图复用随机游走的中间结果，但普遍存在边界附近伪影、样本复用不充分或奇异性等问题，未能充分利用解的调和结构。

本文提出的**调和缓存（Harmonic Caching, HC）**方法，其核心洞察在于：调和函数在球内的行为可由其边界值的傅里叶级数展开完全描述——这本质上是均值性质的一般化。具体而言，HC从球边界发射蒙特卡洛随机游走来估计少量傅里叶系数，然后利用径向衰减的基函数在球内任意位置解析重建解。这一机制将边界信息高效压缩并传播到整个球内子区域，实现了从“逐点估计”到“区域重建”的范式转变。通过自适应放置多个重叠的调和缓存记录并进行加权混合，HC可将局部重建扩展为全局连续解。

实验证据表明，HC在多个维度上实现了显著提升：
- **误差量级降低**：在同等计算时间内，HC的误差比传统逐点WoS低一个数量级以上（Abstract）。
- **收敛全程最优**：在所有2D测试场景的约30分钟收敛过程中，HC始终取得最低的相对均方误差，独立于运行时间（Fig. 10）。
- **伪影抑制**：相比BVC和MVC，HC产生的相关伪影更少且误差更低（Abstract；Fig. 8, 9）。
- **参数鲁棒性**：截断阶数$L=10$且在球半径的0.9倍范围内重建时，偏差可保持极低（Sec. 3.1）。

HC同时提供有偏（固定截断$L=10$）和无偏（随机截断前缀和估计）两种方案，推荐有偏方案因其方差更低、伪影更少（Fig. 5）。

**方法局限**：HC仅能在域内部降低误差，无法直接改善边界上的解质量（所有WoS缓存方法的共性）；在非光滑诺伊曼边界附近可能产生较强相关伪影（Fig. 15）；有偏版本在球边界附近存在截断偏差。当前方法依赖Walk on Stars（WoSt）作为底层估计器，向变系数PDE的扩展仍有待探索。

## 背景与动机

### 问题背景：椭圆型偏微分方程的蒙特卡罗求解

求解椭圆型偏微分方程（PDE）是计算物理、几何处理与图形学中的核心问题。考虑定义在域 $\Omega \subset \mathbb{R}^d$ 上的拉普拉斯方程：

$$\Delta u(x) = 0 \text{ on } \Omega, \quad u(x) = g(x) \text{ on } \partial\Omega$$

传统数值方法（有限元、有限差分）在复杂几何或高维场景下常受限于网格生成成本。Walk on Spheres（WoS）及其变体**Walk on Stars**（WoSt, Sawhney et al., ACM Trans. Graph. 2023）作为无网格蒙特卡罗求解器，通过从查询点发射随机游走直至击中边界来估计解值，天然适用于复杂域和稀疏查询。然而，WoS类方法的根本瓶颈在于：**逐点估计的方差大，当需要密集或高精度解场时，计算成本急剧攀升**。

### 现有缓存方法的缺口

为缓解逐点估计的低效问题，研究者提出了多种基于缓存的方差缩减策略，其核心思想是将已计算的边界信息复用给邻近查询点。然而，现有方法存在显著局限：

- **边界值缓存（BVC）**：在边界附近缓存解值，但存在奇异性问题，导致近边界区域估计不稳定。
- **均值缓存（MVC）**：利用调和函数的均值性质缓存球心值，但样本复用不充分，边界附近伪影明显。
- **逆向Walk on Spheres（RWoS, Qi et al., Computer Graphics Forum EGSR 2022）**：从源点逆向行走以缩减方差，但在域内部仍产生较强的相关伪影。

这些方法的共同缺陷在于：**未能充分利用解的调和结构**——调和函数在球内的行为完全由其边界值通过傅里叶级数展开决定，而现有缓存方法仅使用了零阶信息（均值性质），丢弃了高阶角向模式所携带的丰富边界信息。

### 核心动机：从均值性质到广义调和展开

调和函数的均值性质指出，球心值等于边界值的平均，即傅里叶级数的零阶项 $a_0$。更一般地，球内任意点的解可通过边界数据的**完整傅里叶级数展开**配合径向衰减精确重建。在二维极坐标下，该展开为：

$$u(r,\theta) = a_0 + 2 \sum_{l=1}^{\infty} \left(\frac{r}{R}\right)^l (a_l \cos l\theta + b_l \sin l\theta)$$

其中傅里叶系数由边界积分定义：

$$a_l = \frac{1}{2\pi} \int_0^{2\pi} u(R,\Theta) \cos(l\Theta) \mathrm{d}\Theta, \quad b_l = \frac{1}{2\pi} \int_0^{2\pi} u(R,\Theta) \sin(l\Theta) \mathrm{d}\Theta$$

这一展开揭示了关键洞察：**将边界信息压缩为少量傅里叶系数，结合径向解析缩放 $(r/R)^l$，即可在球内大部分区域以低阶截断获得高精度重建**——高阶项因径向衰减而迅速贡献递减。这意味着，通过蒙特卡罗估计少量系数，即可高效地将边界信息传播至整个球内子区域，从而突破逐点估计的效率瓶颈。

本文提出的**调和缓存（Harmonic Caching, HC）**正是基于这一原理：从球边界发射WoSt随机游走估计傅里叶系数，再利用调和级数一次性重建球内任意点的解，并通过自适应重叠球的加权混合实现全局求解。

## 核心创新

调和缓存（Harmonic Caching, HC）的核心创新在于将**边界信息的压缩传播**与**局部解析重建的全局混合**相结合，从根本上改变了椭圆型偏微分方程蒙特卡洛求解的方差结构。其关键创新点可归纳为三个层面。

### 1. 解估计机制的范式转变：从逐点估计到区域解析重建

传统Walk on Spheres（WoS）及其变体在每一个查询点独立发射随机游走，仅估计该点的解值。这一逐点策略导致方差随求解密度线性累积，且无法利用解在空间上的结构性冗余。

HC的核心突破在于利用**调和函数在球内的解析傅里叶级数展开**替代逐点估计。具体而言，该方法在域内放置一个球，仅从球边界发射蒙特卡洛随机游走以估计傅里叶系数（$a_l$, $b_l$），随后利用径向衰减的基函数一次性重建整个球内子区域的解：

$$u(r,\theta) = a_0 \mathcal{R}_{\alpha}^0(r,R) + 2 \sum_{l=1}^{\infty} \mathcal{R}_{\alpha}^l(r,R) \left( a_l \cos(l\theta) + b_l \sin(l\theta) \right)$$

其中径向基函数 $\mathcal{R}_{\alpha}^l(r,R)$ 在拉普拉斯情形（$\alpha=0$）下退化为 $(r/R)^l$，在筛选泊松情形下为修正贝塞尔函数之比 $I_l(\sqrt{\alpha}r)/I_l(\sqrt{\alpha}R)$。

这一机制的因果杠杆在于：**调和展开本质上是均值性质的一般化**——零阶项 $a_0$ 即均值性质，而高阶项将边界信息压缩为少量系数，结合径向解析缩放实现降维。低阶截断（$L=10$）即可在大部分区域内获得高精度重建，而随机截断可消除偏差。该机制将“在球内估计 $N$ 个点”的成本从 $O(N)$ 次全局随机游走降至 $O(1)$ 次边界采样加 $O(N)$ 次廉价解析计算，从根本上改变了计算复杂度结构。

### 2. 全局求解策略：自适应重叠缓存与加权混合

HC将局部解析重建扩展为全局求解器的策略是**用重叠调和缓存记录覆盖域**，并通过距离加权平滑混合各记录的重建结果：

$$\widehat{u}(\mathbf{x}) = \frac{\sum_{i \in S(\mathbf{x})} w(d_i) \widehat{u}_i(\mathbf{x})}{\sum_{i \in S(\mathbf{x})} w(d_i)}$$

这一策略的关键设计选择包括：
- **保守重建半径**：仅使用最大内切球半径的0.9倍作为实际重建范围（$R_i = 0.9 R_{\partial\Omega}(p_i)$），以将截断偏差控制在可忽略水平（$r < 0.9R$ 时 $L=10$ 截断偏差极低）。
- **自适应缓存放置**：通过最小权重阈值 $w_{\min}$ 控制缓存密度，确保查询点被足够多的缓存记录覆盖。
- **两阶段填充-精化流程**：初始填充阶段各记录独立估计系数；精化阶段利用已构建的缓存查找边界值，以更低方差重新估计系数，显著降低相关伪影。

相比现有缓存方法，HC的重叠混合策略避免了**边界值缓存（BVC）** 在边界附近的奇异性问题，也克服了**均值缓存（MVC）** 样本复用不充分的局限。

### 3. 截断偏差的灵活处理：有偏高效与无偏可选

针对调和级数截断引入偏差的问题，HC提供了两种方案：
- **有偏方案**（推荐）：固定截断 $L=10$，方差更低，相关伪影更少。
- **无偏方案**：采用随机截断的前缀和估计器，以 $\langle L \rangle = 10$ 的期望截断阶数实现无偏重建，但代价是方差升高。

实验证据表明（Fig. 5），有偏方案因方差优势在实际应用中更为可取，这一设计选择体现了**精度-方差权衡**的务实考量。

### 4. 与现有方法的本质差异

| 机制维度 | 传统WoS/WoSt | BVC/MVC | **Harmonic Caching** |
|---------|-------------|---------|---------------------|
| 解估计 | 逐点独立估计 | 边界/均值缓存复用 | 边界系数压缩 + 区域解析重建 |
| 信息传播 | 无 | 有限复用 | 径向解析缩放传播至整个球内 |
| 缓存半径利用 | — | 使用完整内切球 | 仅用0.9倍半径以控制截断偏差 |
| 全局策略 | 无 | 简单缓存查找 | 自适应重叠放置 + 加权混合 |
| 偏差处理 | 无偏 | 有偏（固定缓存） | 有偏/无偏可选 |

### 5. 证据强度总结

- **误差降低一个数量级以上**：在同等计算时间内，HC的相对MSE比传统逐点WoS低一个数量级以上（Abstract，置信度0.9）。
- **全场景收敛优势**：在所有2D测试场景的30分钟收敛过程中，HC始终取得最低误差曲线，独立于运行时间（Fig. 10，置信度0.95）。
- **伪影抑制**：相比BVC和MVC，HC产生更少的相关伪影和边界噪声（Fig. 8，置信度0.9）。
- **截断鲁棒性**：$L=10$ 且在 $r < 0.9R$ 范围内重建，偏差可保持极低（Sec. 3.1，置信度0.9）。

**需要手动验证的点**：BVC和MVC的具体引用信息在分析数据中缺失，建议核实其原始出处以确保谱系定位的准确性。

## 整体框架

![[assets/figures/papers/paper_list_l2_https_cs_dartmouth_edu_wjarosz_publications_zhou25harmonic_pdf/figures/004_Figure_4.jpg]]
*Figure 4: Overview of our harmonic caching algorithm for solving elliptic PDEs. We leverage the generalized mean value property of harmonic functions (Fig. 2) to reconstruct solutions from local boundary estimates. Within userspecified regions of interest (lef), we adaptively place overlapping spherical cache records (middle), each storing a compact set of Fourier coeficients. Blending local reconstructions from each record yields a smooth, low-error approximation across the region (right)*

调和缓存（Harmonic Caching, HC）将椭圆型偏微分方程的求解重构为两个核心阶段：**缓存填充与精化**，以及**调和展开重建**。其核心思想是利用调和函数在球内的解析傅里叶级数展开，将边界信息压缩为一组紧凑的傅里叶系数，从而在球内任意位置高效重建解。

### 算法总览

算法以用户指定的感兴趣区域（Region of Interest）为输入，在该区域内自适应放置一系列重叠的球形缓存记录（cache records）。每个缓存记录存储一组傅里叶系数，这些系数通过从球边界发射Walk on Stars（WoSt）随机游走进行蒙特卡洛估计。最终，对于任意查询点，系统通过加权混合所有覆盖该点的缓存记录的重建结果，输出平滑的全局解估计（图4）。

```
Algorithm 1: Harmonic Caching for WoSt
─────────────────────────────────────
1.  Cache Population Pass
    - 在感兴趣区域内自适应生成缓存记录
    - 每个记录：从最大内切球边界发射随机游走，估计傅里叶系数
2.  Refinement Pass (可选)
    - 利用已填充的缓存查找重构边界值
    - 以更低方差重新估计各记录的傅里叶系数
3.  Reconstruction
    - 对查询点，加权混合所有覆盖该点的缓存记录的调和级数结果
```

### 缓存填充通道（Cache Population Pass）

系统首先在域内自适应放置球形缓存记录。每个记录的中心 $p_i$ 处，取半径为 $R_i = 0.9 R_{\partial\Omega}(p_i)$ 的球（其中 $R_{\partial\Omega}(p_i)$ 为最大内切球半径），仅使用 $0.9$ 倍半径作为实际重建范围，以有效抑制截断误差（Sec. 3.2）。

对于每个缓存记录，算法在球边界上采样 $N_i$ 个点，从每个点发射WoSt随机游走到达域边界，获得边界值的蒙特卡洛估计 $\widehat{u}(R, \theta_j)$。然后通过蒙特卡洛积分估计傅里叶系数：

$$\widehat{a}_l = \frac{1}{N} \sum_{j=1}^N \frac{\widehat{u}(R,\theta_j) \cos(l\theta_j)}{p(\theta_j) 2\pi}, \quad \widehat{b}_l = \frac{1}{N} \sum_{j=1}^N \frac{\widehat{u}(R,\theta_j) \sin(l\theta_j)}{p(\theta_j) 2\pi}$$

采样采用均匀抖动分布（uniform-jittered distribution），即在球边界上等距分布但随机旋转的点集，以保证估计的无偏性（Sec. 3.1）。

### 精化通道（Refinement Pass）

初始缓存填充时，每条随机游走独立进行，不使用缓存查找。一旦缓存建立，系统复制缓存并执行一次"序曲通道"（overture pass）：利用已填充的缓存记录查找重构边界值，从而以更低方差重新估计各记录的傅里叶系数。精化通道仅使用 $0.5\alpha N$ 个样本，并设置 $w_{\min}=0$，使查询点直接从缓存中获取解（Sec. 3.2）。

### 调和展开重建

对于查询点 $\mathbf{x}$，系统找出所有覆盖该点的缓存记录集合 $S(\mathbf{x})$，对每个记录 $i$ 使用截断的调和级数重建局部估计 $\widehat{u}_i(\mathbf{x})$，然后通过距离加权平滑混合得到最终结果：

$$\widehat{u}(\mathbf{x}) = \frac{\sum_{i \in S(\mathbf{x})} w(d_i) \widehat{u}_i(\mathbf{x})}{\sum_{i \in S(\mathbf{x})} w(d_i)}$$

其中 $d_i = \|\mathbf{x} - p_i\| / R_i$ 为归一化距离，$w(\cdot)$ 为权重函数（Eq. 8）。

调和级数重建本身利用了径向衰减的基函数。以筛选泊松方程为例，齐次解在球内的展开为：

$$u(r,\theta) = a_0 \mathcal{R}_{\alpha}^0(r,R) + 2 \sum_{l=1}^{\infty} \mathcal{R}_{\alpha}^l(r,R) \left( a_l \cos(l\theta) + b_l \sin(l\theta) \right)$$

其中径向基函数 $\mathcal{R}_{\alpha}^l(r,R)$ 在拉普拉斯情形（$\alpha=0$）下简化为 $(r/R)^l$，在筛选情形（$\alpha>0$）下为修正贝塞尔函数之比 $I_l(\sqrt{\alpha}r)/I_l(\sqrt{\alpha}R)$（Eq. 5, 6）。这一展开本质上是均值性质的一般化：零阶项对应球心的均值，高阶项通过投影和径向缩放重建球内完整解。

### 源项处理

当存在非齐次源项 $f(x)$ 时，系统在调和重建的基础上附加源项贡献。通过在球内采样 $M$ 个点，利用离中心格林函数进行蒙特卡洛积分：

$$\widehat{u}_f(r,\theta) = \widehat{u}(r,\theta) + \frac{1}{M} \sum_{j=1}^M \frac{f(R_j,\Theta_j) G(r,\theta;R_j,\Theta_j)}{p(R_j,\Theta_j)}$$

其中 $\widehat{u}(r,\theta)$ 为齐次部分的调和缓存估计（Eq. 10）。由于源项非递归定义，增加源样本的成本相对较低（Fig. 12）。

### 实现要点

系统在CPU上基于Zombie库[**Zombie** (Sawhney and Miller, 2023)]以单精度浮点实现。缓存查找使用多引用八叉树（multi-reference octree）[Pharr and Humphreys 2010]：初始填充阶段通过读写锁保护并发访问，精化阶段则完全无锁（Sec. 4.1）。

### 输入输出流

- **输入**：域几何 $\Omega$、边界条件（Dirichlet/Neumann/Robin）、源项 $f(x)$（可选）、感兴趣区域
- **中间表示**：自适应放置的重叠球形缓存记录，每个存储截断的傅里叶系数 $\{\widehat{a}_l, \widehat{b}_l\}_{l=0}^L$
- **输出**：感兴趣区域内任意点的解估计 $\widehat{u}(\mathbf{x})$，通过加权混合局部调和重建得到

## 核心模块与公式推导

### 问题模型与调和展开基础

调和缓存（Harmonic Caching, HC）面向一般椭圆型偏微分方程，其最广泛形式为筛选泊松方程（Screened Poisson）配以混合边界条件：

$$
\begin{array}{rl}
\Delta u_f(x) - \alpha u_f = -f(x) & \text{on } \Omega, \\
u_f(x) = g(x) & \text{on } \partial\Omega_D, \\
\frac{\partial u_f(x)}{\partial n_x} = h(x) & \text{on } \partial\Omega_N, \\
\frac{\partial u_f(x)}{\partial n_x} + \mu(x) u_f(x) = \ell(x) & \text{on } \partial\Omega_R
\end{array}
$$

其中 $\alpha \ge 0$ 为筛选系数，$f(x)$ 为源项，$\partial\Omega_D$、$\partial\Omega_N$、$\partial\Omega_R$ 分别对应 Dirichlet、Neumann 和 Robin 边界。当 $\alpha=0$ 且 $f=0$ 时退化为拉普拉斯方程。方法的核心洞察在于：**调和函数在球内的展开是均值性质的一般化**——均值性质仅恢复球心的值（零阶项），而完整调和级数可将边界信息压缩为少量傅里叶系数，结合径向解析缩放实现整个球内子区域的降维重建。

对于二维情形，球内齐次解可展开为：

$$
u(r,\theta) = a_0 \mathcal{R}_{\alpha}^0(r,R) + 2 \sum_{l=1}^{\infty} \mathcal{R}_{\alpha}^l(r,R) \left( a_l \cos(l\theta) + b_l \sin(l\theta) \right)
$$

其中径向基函数 $\mathcal{R}_{\alpha}^l(r,R)$ 根据筛选参数 $\alpha$ 自适应选择形式：

$$
\mathcal{R}_{\alpha}^l(r,R) = \begin{cases}
(r/R)^l & \text{if } \alpha=0 \\
\frac{I_l(\sqrt{\alpha}r)}{I_l(\sqrt{\alpha}R)} & \text{if } \alpha>0
\end{cases}
$$

$I_l(\cdot)$ 为第一类修正贝塞尔函数。当 $\alpha=0$ 时，径向缩放退化为简单的幂次衰减 $(r/R)^l$；当 $\alpha>0$ 时，贝塞尔函数比值提供了筛选效应的解析调制。傅里叶系数由边界数据的投影定义：

$$
a_l = \frac{1}{2\pi} \int_0^{2\pi} u(R,\Theta) \cos(l\Theta) \mathrm{d}\Theta, \quad
b_l = \frac{1}{2\pi} \int_0^{2\pi} u(R,\Theta) \sin(l\Theta) \mathrm{d}\Theta
$$

### 核心模块一：缓存填充（Cache Population）

这是 HC 的初始化通道，负责在感兴趣区域内自适应生成缓存记录。每个记录对应一个完全位于域内的球 $B(p_i, R_i)$，其半径取为最大内切球半径的 0.9 倍（$R_i = 0.9 R_{\partial\Omega}(p_i)$），以将截断误差限制在可控范围（Fig. 3 验证了 $L=10$ 在 $r<0.9R$ 内偏差极低）。

对每个缓存记录，从球边界发射 $N$ 条 Walk on Stars（WoSt）随机游走，在边界采样点 $(R, \theta_j)$ 处估计解值 $\widehat{u}(R,\theta_j)$，进而通过蒙特卡洛积分估计傅里叶系数：

$$
\widehat{a}_l = \frac{1}{N} \sum_{j=1}^N \frac{\widehat{u}(R,\theta_j) \cos(l\theta_j)}{p(\theta_j) 2\pi}, \quad
\widehat{b}_l = \frac{1}{N} \sum_{j=1}^N \frac{\widehat{u}(R,\theta_j) \sin(l\theta_j)}{p(\theta_j) 2\pi}
$$

边界采样采用均匀抖动分布（uniform-jittered）：等间距采样点配合随机整体旋转，兼顾均匀覆盖与方差特性。截断阶数取 $L=10$ 作为精度与成本的最佳平衡点——消融实验（Fig. 6 top）表明增大 $L$ 可降低误差但收益递减，$L=1$ 则因丢失高频信息而效果很差。

### 核心模块二：精化通道（Refinement Pass）

首次缓存填充时，各记录的随机游走独立进行，不使用缓存查找。填充完成后，HC 复制缓存并执行精化通道：对每个记录仅使用 $0.5\alpha N$ 条新游走重新估计傅里叶系数，但此时**所有游走均通过已有缓存查找边界值**，从而以更低方差获得系数估计。精化期间设置 $w_{\min}=0$，即只要查询点被任何缓存记录覆盖，就直接从缓存读取解值，无需重新行走到底层边界。这一设计与均值缓存（MVC）的递归复用思路相似，但在边界附近精度更高（Fig. 13）。

### 核心模块三：调和展开重建（Harmonic Expansion Reconstruction）

对任意查询点 $\mathbf{x}$，HC 收集所有覆盖该点的缓存记录集合 $S(\mathbf{x})$，对每个记录 $i$ 利用其存储的傅里叶系数通过截断调和级数计算局部估计 $\widehat{u}_i(\mathbf{x})$，再通过距离加权平滑混合得到全局估计：

$$
\widehat{u}(\mathbf{x}) = \frac{\sum_{i \in S(\mathbf{x})} w(d_i) \widehat{u}_i(\mathbf{x})}{\sum_{i \in S(\mathbf{x})} w(d_i)}
$$

其中 $d_i = \|\mathbf{x} - p_i\| / R_i$ 为归一化距离，权重函数 $w(d)$ 在 $d$ 接近 1 时快速衰减，确保重建主要由查询点附近的缓存记录贡献，同时在各记录覆盖边界处平滑过渡。这一混合策略将局部球内重建扩展为全局连续解场。

### 核心模块四：源项积分（Source Term Integration）

当存在非零源项 $f(x) \neq 0$ 时，齐次解 $\widehat{u}(\mathbf{x})$ 需叠加非齐次贡献。HC 在球内采样 $M$ 个源点 $(R_j, \Theta_j)$，利用离中心格林函数 $G$ 进行蒙特卡洛积分：

$$
\widehat{u}_f(r,\theta) = \widehat{u}(r,\theta) + \frac{1}{M} \sum_{j=1}^M \frac{f(R_j,\Theta_j) G(r,\theta; R_j,\Theta_j)}{p(R_j,\Theta_j)}
$$

该估计器的误差常集中在源项附近（因离中心格林函数的奇异性，见 Fig. 12），但分配额外源样本的成本较低——源项非递归定义，无需行走到底层边界。

### 三维推广

三维情形下，标量傅里叶级数推广为球谐展开：

$$
u(r,\theta,\phi) = \sum_{l=0}^{\infty} \sum_{m=-l}^{l} a_l^m \mathcal{R}_{\alpha}^{l,3D}(r,R) y_l^m(\theta,\phi)
$$

其中 $y_l^m$ 为实球谐函数，三维径向基函数为：

$$
\mathcal{R}_{\alpha}^{l,3D}(r,R) = \begin{cases}
(r/R)^l & \alpha=0 \\
\frac{i_l(\sqrt{\alpha}r)}{i_l(\sqrt{\alpha}R)} & \alpha>0
\end{cases}
$$

$i_l(\cdot)$ 为修正球贝塞尔函数。系数估计与二维流程一致，仅将角向投影替换为球谐投影。

### 有偏与无偏截断选择

固定截断 $L=10$ 的调和缓存是有偏的——截断丢弃了 $l>10$ 的高频分量。HC 同时提供了无偏版本：采用随机截断前缀和估计器（stochastic truncation prefix-sum estimator），使期望截断阶数 $\langle L \rangle = 10$。Fig. 5 的偏差-方差分析表明，无偏版本虽消除了截断偏差，但方差更高，单次运行中相关伪影更明显。因此**推荐使用有偏方案**，因其方差更低且伪影更少，而截断偏差在 $r<0.9R$ 范围内可忽略。

## 实验与分析

![[assets/figures/papers/paper_list_l2_https_cs_dartmouth_edu_wjarosz_publications_zhou25harmonic_pdf/figures/010_Figure_7.jpg]]
*Figure 7: Computation time depends on both the number of cache records and the walks per record used for coeficient estimation. For equal runtime, it is generally beter to use fewer records with more walks (lef) than more records with fewer walks (right)*

### 主结果：调和缓存在等时预算下取得最低误差

调和缓存（HC）在所有测试场景中一致地取得了最低的相对均方误差，且这一优势不依赖于运行时间。在2D Laplace/Dirichlet/Neumann/Robin场景集上（Fig. 9），HC的相对MSE远低于WoSt、RWoS、BVC和MVC。收敛曲线（Fig. 10）表明，在约30分钟的完整收敛过程中，HC全程保持最低误差曲线，相比传统逐点WoSt误差降低超过一个数量级。这一结果与论文摘要中的声明一致：“Our method achieves over an order of magnitude lower error than traditional pointwise WoS in equal time.”

在Poisson方程场景（Fig. 11）中，即使场景被刻意设计为有利于RWoS（三个狄拉克脉冲源项配合零狄利克雷边界），HC仍以更低误差胜出。这源于源项积分对狄拉克函数的精确性，误差仅来自边界解的傅里叶表示。

3D Screened Laplace问题（火鸡腿模型，Fig. 14）在约1500秒等时预算下，HC同样取得最低误差和平滑重建，显著优于WoSt、BVC和MVC。

### 伪影与边界行为

调和缓存在内部区域产生的相关伪影显著少于RWoS，在边界附近的噪声低于MVC，且不存在BVC在边界处的奇异性问题（Fig. 8）。然而，在非光滑诺伊曼边界条件下，HC可能表现出比BVC更强的相关伪影——底层WoSt估计器的噪声会显著污染傅里叶系数（Fig. 15）。在光滑诺伊曼边界附近，HC仍保持最低误差。

### 消融研究

参数消融（Fig. 6）揭示了三个关键控制维度的行为：

1. **截断阶数L**：增加L可降低重建误差，但收益递减。L=1时结果较差，L=10在精度与成本之间取得最佳平衡。在r < 0.9R的保守子区域内，L=10的截断偏差极低。
2. **缓存密度（w_min）**：提高w_min产生更密集的缓存记录并提升精度，成本大致线性增长。
3. **每记录行走数（通过α控制N_i）**：增加行走数能有效抑制系数噪声，降低重建误差。

缓存密度与每记录行走数的权衡（Fig. 7）表明：在固定总计算成本下，使用较少缓存记录但为每个记录分配更多行走的策略，优于相反配置。这一发现对实际部署中的资源分配具有直接指导意义。

### 有偏与无偏方案

固定截断L=10的有偏方案与随机截断（均值=10）的无偏前缀和估计器的对比（Fig. 5）显示：无偏方案消除了截断偏差，但方差更高，表现为更强的相关伪影。论文明确指出“有偏方案因其更低的方差和更少的相关伪影而更为可取”。

### 精化通道的增益

利用已填充缓存进行精化通道（Refinement Pass）可进一步降低误差和伪影（Fig. 13）。该过程类似于MVC的递归复用，但在边界附近取得更高精度，且精化通道使用仅0.5αN样本即可完成系数重估计。

### 误差来源分析

对于一般泊松问题，HC的误差常集中在源项附近（Fig. 12），原因是离中心格林函数的蒙特卡洛估计器（Eq. 10）在该区域方差较大。但分配额外源样本的成本相对较低，因为源项非递归定义。

### 公平性说明

所有对比在同等时间预算下进行，使用相同的底层WoSt求解器和共用的多引用八叉树实现。参考解通过极高样本数（600万行走/点）的WoSt获得，并进行1%异常值剔除。部分方法（如MVC）使用了论文推荐的递归复用设置。

## 方法谱系与知识库定位

### 1. 问题背景与现有方法瓶颈

调和缓存（Harmonic Caching, HC）针对的是椭圆型偏微分方程（PDE）的无网格蒙特卡洛求解问题，其底层依赖于Walk on Spheres（WoS）及其变体Walk on Stars（WoSt）。传统WoS方法的核心瓶颈在于：每次随机游走只能估计单个点的解，当需要密集或高精度的解场时，逐点估计的方差大、效率低下。这一瓶颈在要求全局解场的图形学应用中尤为突出。

为缓解这一问题，已有若干方差缩减方法被提出，但它们各自存在结构性缺陷：

- **Reverse Walk on Spheres（RWoS）**（Qi et al., Computer Graphics Forum (EGSR) 2022）：从源点逆向发射随机游走。该方法在源项稀疏时表现良好，但在域内部区域仍存在较强的相关伪影（见图8顶部插图）。
- **Boundary Value Caching（BVC）**：在边界附近缓存解值。其根本问题在于边界附近存在奇异性，导致重建不稳定（见图8右上插图）。
- **Mean Value Caching（MVC）**：利用均值性质进行缓存复用。虽然能降低方差，但在边界附近噪声较大，且样本复用不够充分（见图8左下插图）。

这些方法的共同局限在于：**未能充分利用解的调和结构**——调和函数在球内的行为完全由其边界值决定，而这一关系可以通过解析的傅里叶级数展开来精确表达。

### 2. 核心机制创新

HC的关键洞察是将调和函数的均值性质一般化：球内任意点的解可以表示为边界数据的傅里叶系数与径向衰减基函数的加权和。这一展开在拉普拉斯方程情形下为：

$$u(r,\theta) = a_0 + 2 \sum_{l=1}^{\infty} \left(\frac{r}{R}\right)^l (a_l \cos l\theta + b_l \sin l\theta)$$

对于筛选泊松方程（$\alpha > 0$），径向基函数变为修改的贝塞尔函数之比：

$$\mathcal{R}_{\alpha}^l(r,R) = \frac{I_l(\sqrt{\alpha}r)}{I_l(\sqrt{\alpha}R)}$$

核心机制转换体现在以下四个维度：

| 机制维度 | 基线方法 | 调和缓存 |
|---------|---------|---------|
| 解估计机制 | 逐点发射随机游走，仅估计单个点的解 | 从球边界发射随机游走估计傅里叶系数，利用调和级数一次性重建整个球内子区域的解 |
| 全局求解策略 | 无缓存或简单逐点估计 | 自适应放置多个重叠调和缓存记录，通过距离加权平滑混合各记录的重建结果 |
| 截断偏差处理 | 固定截断引入偏差（缓存方法通常有偏） | 提供有偏（L=10固定）和无偏（随机截断前缀和估计）两种方案，推荐有偏方案因方差更低 |
| 缓存半径利用 | 使用最大内切球半径（MVC/BVC使用完整球） | 仅使用最大内切球半径的0.9倍作为实际重建范围，以降低截断误差 |

**降维效应**是HC效率优势的数学根源：边界信息被压缩为少量傅里叶系数（典型截断阶数$L=10$），结合径向解析缩放，在球内大部分区域即可获得高精度重建。图3的验证表明，即使在无限频率的Heaviside边界函数下，低阶截断（$L=10$）在保守子区域（$r < 0.9R$）内的偏差仍可忽略。

### 3. 方法管道

HC的完整管道包含四个模块：

1. **缓存填充（Cache Population）**：在感兴趣区域内自适应生成缓存记录，每个记录通过从最大内切球边界发射随机游走估计傅里叶系数（Algorithm 1, Sec. 3.2）。
2. **精化通道（Refinement Pass）**：利用已填充的缓存查找重构边界值，以更低方差重新估计各记录的傅里叶系数（Algorithm 1, Sec. 3.2）。图13显示，这一通道能进一步降低误差和伪影，且精度优于MVC的递归复用。
3. **调和展开重建（Harmonic Expansion Reconstruction）**：对于查询点，通过加权混合所有覆盖该点的缓存记录的调和级数结果得到最终估计值（Algorithm 2, Eq. (8)）。
4. **源项积分（Source Term Integration）**：当存在源项时，通过蒙特卡洛积分球的离中心格林函数来附加非齐次贡献（Eq. (10), Sec. 3.3）。

### 4. 实验证据强度

**主要性能声明**（置信度0.9-0.95）：

- **等时误差优势**：在所有2D测试场景（Dirichlet/Neumann/Robin混合边界条件）的30分钟收敛过程中，HC始终取得最低的相对均方误差（Fig. 10）。相比传统WoSt，误差降低约一个数量级（Abstract）。
- **伪影抑制**：相比BVC和MVC，HC产生的相关伪影更少（Fig. 8），且无BVC的边界奇异性问题。
- **3D扩展性**：在3D screened Laplace问题（火鸡腿模型，~1500秒等时预算）上，HC取得最低误差和最平滑的重建（Fig. 14）。

**消融实验**（置信度0.9）：

- 截断阶数$L$增加可降低重建误差，但收益递减；$L=10$为精度与成本的最佳平衡点（Fig. 6 top）。
- 提高$w_{min}$（增加缓存密度）能降低重建误差，成本大致线性增长（Fig. 6 middle）。
- 增加每记录行走数$N_i$能有效抑制系数噪声（Fig. 6 bottom）。
- 在同等计算时间下，使用较少缓存记录但给每个记录分配更多行走比相反策略更优（Fig. 7）。

**公平性保障**：所有对比在同等时间预算下进行，使用相同的底层WoSt求解器和共用的多引用八叉树实现。参考解通过极高样本数（600万行走/点）的WoSt获得，并进行1%的异常值剔除。

### 5. 适用边界与局限

**适用边界**：

- 适用于椭圆型PDE（拉普拉斯、泊松、筛选泊松）在复杂几何上的求解，支持Dirichlet、Neumann、Robin混合边界条件。
- 在需要密集解场的场景（如热传导可视化）中优势最为显著。
- 方法在域内部降低误差，但不能直接改善边界上的解的质量——这是所有WoS缓存方法的共同局限。

**已知局限**：

1. **非光滑诺伊曼边界**：在此类边界附近，调和缓存可能需要极稠密的缓存记录才能获得良好重建，且可能产生比BVC更强的相关伪影（Fig. 15）。底层WoSt估计器的噪声会显著污染傅里叶系数。
2. **截断偏差**：有偏版本（固定截断$L=10$）在球边界附近（$r$接近$R$）存在截断偏差，尽管在$0.9R$范围内偏差可忽略。无偏版本（随机截断）可消除偏差，但方差更高（Fig. 5）。
3. **底层求解器依赖**：当前方法依赖WoSt作为底层估计器，因此在复杂几何或变系数PDE上的扩展性有限。

### 6. 开放问题

论文明确指出的开放研究方向包括：

1. **重建区域扩展**：能否将重建区域从球扩展至一般的星形区域，以减少所需缓存记录数？
2. **源项融合**：是否可将源项贡献直接融入调和级数展开（多极展开）以进一步降低方差？
3. **变系数PDE推广**：如何将调和缓存框架推广到变系数偏微分方程？
4. **最优无偏截断**：能否基于Misso et al. 2022推导出方差最优的无偏级数截断策略？
5. **自适应缓存密度**：如何在诺伊曼边界附近自动调整缓存密度以提高鲁棒性？

### 7. 在知识库中的定位

调和缓存处于**无网格蒙特卡洛PDE求解器**与**调和分析**的交叉点。它继承了WoS/WoSt的几何灵活性，但通过引入调和级数的解析结构，将方差缩减问题转化为系数估计问题。与BVC/MVC等纯缓存方法相比，HC的独特贡献在于**利用PDE解的解析结构进行降维**，而非仅仅复用已有的点估计。这一思路与近年来图形学中“将物理先验融入蒙特卡洛估计”的趋势一致，但HC在调和函数这一经典领域找到了一个简洁而高效的切入点。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2025/Harmonic_caching_for_walk_on_spheres.pdf]]
