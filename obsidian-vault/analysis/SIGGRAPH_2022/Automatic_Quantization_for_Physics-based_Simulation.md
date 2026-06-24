---
title: Automatic Quantization for Physics-based Simulation
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Automatic_Quantization_for_Physics_based_Simulation.pdf
project_link: null
code_link: "https://github.com/Hanke98/AutoQuantizer"
aliases:
- AQA
- AQPBS
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 各物理变量类型的量化分辨率 Δₕ（或等价的分数位宽 bₕ），它直接控制各时间步量化操作引入的误差幅度及整体内存占用。
primary_logic: 将量化误差传播建模为各变量梯度的加权和，利用可微仿真获得误差对各变量的敏感性，从而将离散位宽搜索转化为可通过拉格朗日乘数法解析求解的连续约束优化问题，并引入抖动保证误差独立性。
claims:
- 误差传播模型预测的评估函数分布与实际仿真采样分布高度吻合，说明基于梯度的误差估计算法可靠。
- 在相同内存压缩率下，自动生成的量化方案的仿真效果优于 QuanTaichi 和人工精炼方案，使用更少的分数位宽且误差更低。
- 添加抖动（dithering）后，量化误差的分布接近均匀且彼此独立，显著抑制了仿真中的数值偏差，使弹性体等仿真结果更接近全精度参考。
- 二分算法将梯度计算的空间复杂度降至 O(log N)，使长序列仿真（超过 4000 步）的梯度计算成为可能，且实际的承载能力是全展开方案的至少 7.8 倍。
---

# Automatic Quantization for Physics-based Simulation

> [!tip] 核心洞察
> 将量化误差传播建模为各变量梯度的加权和，利用可微仿真获得误差对各变量的敏感性，从而将离散位宽搜索转化为可通过拉格朗日乘数法解析求解的连续约束优化问题，并引入抖动保证误差独立性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向物理仿真的自动量化 |
| 英文题名 | Automatic Quantization for Physics-based Simulation |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://arxiv.org/abs/2207.04658) · [Code](https://github.com/Hanke98/AutoQuantizer) |
| Topic | #topic/other_unclear |
| Method | Automatic Quantization (AutoQuantizer) |
| Dataset | 2D MPM elastic body, 2D MPM dam break, Large-scale Eulerian smoke, Large-scale MLS-MPM fluid |

> [!tip] 效果简介
> - 2D MPM elastic body (manual vs. auto) 上，Fraction bits reduction & error ratio 12.7% fewer bits; 94.5% lower error vs Human-designed scheme (Refined QuanTaichi) (12.7% / 94.5%)。
> - 2D MPM dam break (Memory-bounded, 2.5×) 上，Relative error (e_mem) 9.9% vs Float32 reference (9.9%)。
> - Large-scale Eulerian smoke (228M active voxels) 上，Memory compression 1.93× vs Float32 simulation (1.93×)。

## 概要

物理仿真中，为各物理变量分配定点量化位宽需要人工枚举指数级增长的搜索空间，对非专家用户几乎不可行，且缺乏理论误差指导。本文提出 **Automatic Quantization (AutoQuantizer)**，将量化误差传播建模为各变量梯度的加权和，利用可微仿真获取误差敏感性，从而将离散位宽搜索转化为可通过拉格朗日乘数法解析求解的连续约束优化问题；同时引入均匀抖动使量化误差近似独立，保证误差传播公式的适用性。系统在低分辨率全精度仿真上运行一次后，即可根据用户指定的误差容限或内存压缩比自动生成最优分数位宽方案，并借助二分梯度检查点算法支持长序列仿真。实验表明，在相同内存压缩率下，自动生成的方案比 **QuanTaichi**（Hu et al., 2021）及人工精炼方案减少 12.7% 的位宽且误差降低 94.5%；在 2.5× 压缩率下相对误差仅 9.9%；大规模场景（400M 粒子）可实现约 2× 的实际内存压缩。方法定位为 Taichi 语言扩展，提供从可微仿真、约束优化到位打包存储的完整自动化量化管线。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

物理仿真中的量化能显著降低内存占用，但**人工确定量化方案**面临根本性困难：可量化的物理变量类型随仿真器设计呈指数级增长（例如 MPM 仿真中每个粒子包含位置、速度、变形梯度、仿射速度场等多种属性），且许多变量（如变形梯度）缺乏直观的物理意义，非专家用户只能依赖反复试错来分配位宽，效率极低且难以保证精度。

本文的核心洞察在于：**将量化误差传播建模为各变量梯度的加权和**。具体而言，量化操作在每个时间步向仿真状态注入舍入误差 $\mathbf{e}_t$，这些误差沿仿真时间序列传播并累积，最终影响用户关心的评价函数 $\mathcal{Z}$。若能将评价函数对每个量化误差的敏感度量化，便可自动推导出最优的位宽分配方案。作者利用可微仿真框架获取这些敏感度（即梯度），将原本离散的位宽搜索问题转化为**可通过拉格朗日乘数法解析求解的连续约束优化问题**，并引入抖动（dithering）保证误差的独立性假设成立。

### 方法框架与模块顺序

整个自动量化系统包含五个顺序模块，形成从低分辨率分析到高分辨率部署的完整流水线（Fig. 2）：

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2207_04658_repair/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method. A differentiable simulator is developed on a relatively low resolution in a generic workflow. The user specifies an evaluation function and launches the simulation with float64. Ranges and derivatives are recorded during this run. Our auto-quantization system can then derive a quantization scheme according to the user’s specification on either error or memory constraints. The user starts to refine the simulation on a higher resolution with the derived quantization scheme before eventually getting a quantized large-scale simulator*

1. **可微仿真器（低分辨率全精度运行）**：以 float64 精度执行低分辨率仿真，记录各时间步状态、各变量类型的数值范围，并为后续梯度计算提供计算图基础。
2. **梯度累积与二分检查点算法**：通过可逆 adjoint 核或复合 adjoint 核，沿仿真时间序列反向传播评价函数对各量化变量的偏导数，并利用二分检查点技术将空间复杂度降至 $O(\log N)$。
3. **误差/内存有界优化求解器**：根据用户指定的误差容限或目标内存压缩率，利用线性化的误差期望公式和拉格朗日乘数法，解析计算各变量类型的最优量化分辨率 $\Delta_h$。
4. **抖动注入模块**：在每次定点编码前添加均匀随机噪声，使舍入误差近似满足独立均匀分布，保证误差传播公式的理论前提成立。
5. **位打包存储**：编译器级别的自定义数据结构，允许任意位宽的变量在物理字中紧密排列，最大化内存压缩效率。

### 关键 Changed Slots

#### Slot 1：量化方案确定方式

- **Baseline（QuanTaichi / 人工方案）**：用户需手动为每个物理量指定分数位宽 $b_h$ 及数值范围，依赖专家经验或反复试错。
- **Proposed**：在低分辨率全精度仿真运行一次后，利用自动微分获得各变量类型对评价函数的累加平方梯度 $g_h$，代入解析公式直接计算最优分辨率 $\Delta_h$（等效于确定位宽 $b_h$），并自动从全精度运行中记录范围。整个过程无需人工干预，且一次线性化即可给出方案，无需迭代更新。

#### Slot 2：误差建模与估计

- **Baseline**：未提供理论误差估计手段，用户只能通过反复执行量化仿真来验证方案质量。
- **Proposed**：基于不确定性传播理论，将评价函数的期望偏差 $E[\delta z]$ 表达为各量化误差分量独立积分的和（Eq. 5）。在抖动保证误差独立均匀分布的前提下，该期望可简化为各变量分辨率平方与累加平方梯度的加权和（Eq. 8）：
  $$E[\delta z] = \frac{1}{12}\sum_{h=1}^{H} \Delta_h^2 g_h$$
  其中 $g_h = \sum_{i \in \text{type}_h} (\partial \mathcal{Z} / \partial e_i)^2$ 通过自动微分一次性获得。这一解析公式使得误差约束可被直接纳入优化框架。

#### Slot 3：量化误差特性假设

- **Baseline**：直接舍入（round-to-nearest）得到的量化误差在时间序列上通常具有强相关性（Fig. 4），违反独立性假设，导致误差传播公式失效。
- **Proposed**：在编码前注入非减法均匀抖动（non-subtractive dither）：
  $$u = \theta_{\text{dither}}(v) = \left\lfloor \frac{v}{\Delta} + \xi \right\rceil, \quad \xi \sim U(-\frac{1}{2}, \frac{1}{2})$$
  这使得舍入误差近似满足独立均匀分布 $U(-\Delta/2, \Delta/2)$，既保证了误差传播公式的理论适用性，又使量化误差的期望为零（无偏），显著抑制了仿真中的系统性数值偏差。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2207_04658_repair/figures/005_Figure_4.jpg]]
*Figure 4: An illustration of the dependence between quantization errors. At each frame, the variable ?? is added by 1.4△ (see the green arrows) and then ?? is rounded down causing a quantization error of −0.4△ (the red arrows). In this simulation pattern, the quantization errors for each frame are all equal to the previous one. Therefore, assuming they are independent random variables is not always reasonable*

### 优化问题形式与解析求解

系统支持两种用户约束模式，均通过线性化转化为连续优化问题：

**误差有界模式**（给定相对误差容限 $\epsilon_{err}$，最小化总内存）：
$$\min_{\Delta_h} \sum_{h=1}^{H} -P_h \log_2 \frac{\Delta_h}{R_h} \quad \text{s.t.} \quad \frac{1}{12}\sum_{h=1}^{H} \Delta_h^2 g_h < (z \cdot \epsilon_{err})^2$$

**内存有界模式**（给定压缩率 $\epsilon_{mem}$，最小化期望误差）：
$$\min_{\Delta_h} \frac{1}{12}\sum_{h=1}^{H} \Delta_h^2 g_h \quad \text{s.t.} \quad \sum_{h=1}^{H} -P_h \log_2 \frac{\Delta_h}{R_h} < \epsilon_{mem} \cdot M$$

其中 $P_h$ 为类型 $h$ 的变量实例数，$R_h$ 为数值范围，$M$ 为全精度内存占用。通过拉格朗日乘数法，误差有界模式下的最优分辨率具有解析解（Eq. 10）：
$$\Delta_h = \sqrt{\frac{12P_h (\epsilon_{err} \cdot z)^2}{g_h \sum_{h=1}^{H} P_h}}$$

该解析解的关键性质是：**分辨率与梯度敏感度的平方根成反比**——对评价函数影响越大的变量类型，分配的分辨率越精细（$\Delta_h$ 越小），这与直觉高度一致。

### 二分梯度算法：降低空间复杂度

直接沿 $T$ 步仿真序列反向传播梯度需要存储所有中间状态，空间复杂度为 $O(T)$。对于超过数千步的长序列仿真，GPU 显存无法承载。本文提出的二分检查点算法（Fig. 6）将序列递归二分，每次仅需存储 $O(\log T)$ 个检查点状态，重计算代价约为全展开方案的 8 倍，但内存承载能力提升 7.8 倍以上，使得超过 4000 步的梯度计算成为可能。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2207_04658_repair/figures/008_Figure_6.jpg]]
*Figure 6: Illustration of the bisection algorithm. Adjoint kernel is back propagating*

### 位打包存储

传统位结构（bit struct）要求每个变量占用完整的物理字（如 32-bit），当变量位宽非标准时会产生内部碎片。本文的位打包（bit pack）数据结构允许任意位宽的变量在物理字中紧密连续排列（Fig. 7），跨字读写通过位操作实现（Fig. 8）。在 GPU 上性能与位结构相当，在 CPU 上因避免了原子操作而略微更快，且显著提升了实际内存压缩率。

### 模块间因果关系

可微仿真器提供计算图和范围 → 二分梯度算法高效获取 $g_h$ → 优化求解器利用 $g_h$ 和范围 $R_h$ 解析计算 $\Delta_h$ → 抖动注入保证误差独立性使 $E[\delta z]$ 公式有效 → 位打包将推导出的非标准位宽方案高效部署。这一链条的核心在于：**梯度 $g_h$ 是连接仿真物理特性与量化方案优化的唯一信息桥梁**，而抖动则是保证该桥梁理论可靠性的关键使能技术。

## 实验与关键发现

### 主实验结果

**误差受限场景的位宽节省与成功率。** 在 MPM 弹性体（Exp. 1）和 Eulerian 烟雾（Exp. 2）两个基准上，AutoQuantizer 在误差受限模式下的成功率分别为 136/160 和 160/160（Table 2），证明线性化近似在大多数情况下能可靠满足指定的相对误差约束。对于弹性体场景，自动生成的量化方案平均使用 12.7% 更少的分数位宽，同时仿真误差比人工精炼方案（Refined QuanTaichi）低 94.5%（Fig. 13）。在相同总位宽下，自动方案与 float64 参考的视觉一致性明显优于 QuanTaichi 的默认方案。

**内存受限场景的压缩-精度权衡。** 在 2D MPM 溃坝仿真中，当目标压缩率为 2.5× 时，实际压缩率达到 2.51×，相对误差仅为 9.9%（Table 3）。视觉对比（Fig. 10）显示，即使在 3.5× 压缩率下，自动量化方案仍能保持与全精度参考高度相似的流态，而不会出现明显的人工痕迹。

**大规模仿真的实际压缩能力。** 在单张 NVIDIA RTX 3090 GPU 上，AutoQuantizer 成功驱动了三个超大规模仿真（Table 9）：Eulerian 烟雾（228M 活跃体素）达到 1.93× 内存压缩；MLS-MPM 流体（400M 粒子）达到 2.02×；MLS-MPM 弹性体（295M 粒子）达到 2.01×。这些结果表明，自动量化方案在真实的大规模场景中能够实现约 2× 的实际压缩比，且视觉质量与 float32 参考无明显差异（Fig. 17）。

### 关键消融实验

**抖动机制的因果作用。** 移除抖动后，量化误差不再满足独立均匀分布的假设，导致仿真出现严重偏差。在 2D MPM 弹性体下落实验中（Fig. 12），无抖动的量化仿真中弹性方块反弹后穿透天花板，而加抖动的同位数仿真与 float64 参考高度吻合。定量分析（Table 5）表明，无抖动时 round-up 与 round-down 的比例严重失衡（例如某些变量类型中 round-down 比例高达 98.2%），导致评估函数值偏离参考值 10 倍以上；抖动使该比例回归到接近 1:1，评估函数偏差降至可忽略水平。抖动在 CPU 和 CUDA 上的性能开销均较低（Table 6），验证了其实用性。

**位宽配置的敏感性验证。** 以自动生成的基方案为起点，沿两个正交方向（粒子速度 v ↔ 位置 p；变形梯度 F ↔ 仿射速度场 C）调整位宽分配（Fig. 11, Table 4）。当从 p 向 v 转移位宽时，成功率从 20/20 骤降至 0/20；反向转移同样导致成功率下降。这验证了优化解确实处于一个尖锐的最优点，位宽配置的微小偏离会显著影响仿真质量，从而反证了自动优化方法的必要性。

**二分梯度算法的内存-时间权衡。** 与全展开（fully unfolded）梯度计算方案相比，二分检查点算法在时间上慢约 8 倍，但内存承载能力提升 7.8 倍以上（Fig. 14）。全展开方案在超过 2000 步后 GPU 即无法分配足够内存，而二分方案可处理超过 4000 步的长序列仿真，且内存增长仅为对数级。这一特性使得在消费级 GPU 上对长时物理仿真进行梯度计算成为可能。

**误差传播模型的实证验证。** 在 MPM 弹性体仿真中，将基于 Eq. (8) 预测的评估函数概率密度函数与多次实际量化仿真的采样分布进行对比（Fig. 9），两条曲线高度吻合。这直接验证了“量化误差经梯度加权求和”的误差传播模型是准确的，为后续的约束优化提供了可靠的理论基础。

**位打包的性能基准。** 位打包（bit pack）在 GPU 上的性能与位结构（bit struct）相当，在 CPU 上因避免了原子操作而略微更快（Table 7）。这证明紧凑存储方案不会引入显著的运行时开销，使得自动量化带来的内存节省可以直接转化为更大规模仿真的可行性。

### 适用边界与失效模式

**低分辨率到高分辨率的迁移风险。** 自动量化方案是在低分辨率全精度仿真上推导得到的，论文通过缩放实验（Fig. 15, Table 8）展示了同一方案在四种不同分辨率（粒子数从 16K 到 128K）下均能保持与全精度参考的评估函数高度一致。然而，论文明确指出这一迁移“没有理论保证”，当低分辨率与高分辨率仿真的物理行为差异显著时，方案可能失效。

**线性化近似的约束违反。** 优化求解器基于单次梯度信息进行线性化，不进行迭代更新。Table 2 中弹性体实验的成功率为 136/160（85%），意味着约 15% 的案例中线性化解未能严格满足指定的误差约束。论文将此列为明确限制，并指出需要更精确的非线性误差模型来提升鲁棒性。

**定点量化的类型限制。** 当前系统仅支持定点量化，不支持浮点量化类型。对于需要更大动态范围的变量，定点表示可能因范围估计不准确而发生溢出——当前的范围分析仅通过全精度运行后乘以固定因子获得，在极端场景下仍存在溢出风险。

**初始条件泛化的边界。** Fig. 16 展示了同一量化方案在三种不同初始条件（不同初始位置、不同材料参数）下的仿真结果，视觉上均与全精度参考一致。但这组实验覆盖的变异范围有限，对于更剧烈的参数变化或完全不同的仿真场景，方案的泛化能力尚未被充分验证。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2207_04658_repair/figures/017_Figure_13.jpg]]
*Figure 13: The comparison with human generated schemes. From top to bottom: (a) the float64 reference, (b) the result of our method, (c) the result of QuanTaichi [Hu et al. 2021], and (d) the result via a refined version of (c).As we can see from the last frame, our scheme and the refined humangenerated scheme are closer to the float64 reference, while our scheme uses 12.7% less faction bits. The vertical dashed line is added to help compare the horizontal positions of circles by different methods*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2207_04658_repair/figures/016_Figure_12.jpg]]
*Figure 12: Effect of our dithering scheme. Without dithering (the bottom row), the elastic cubes fall from rest, bounce over the initial position, and smash the ceiling. In comparison, the dithered simulation with the same bit number (the second row) closely resembles the full-precision reference (the first row)*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2207_04658_repair/figures/020_Figure_14.jpg]]
*Figure 14: Comparison of temporal complexity between the bisection algorithm (blue) and the fully unfolded scheme (orange). Note that the orange line ends after 2000 steps since GPU fails to allocate enough memory, and the bisection algorithm is roughly 8 times slower under this situation. However, the bisection scheme is nearly free from memory limitations*

## 定位与知识库关联

本文解决的核心问题是**物理仿真中量化方案的人工设计瓶颈**：在 QuanTaichi（Hu et al., ACM Trans. Graph. 2021）等编译器支持的量化框架中，用户必须手动为每种物理量（位置、速度、变形梯度等）指定分数位宽与数值范围，而搜索空间随数据类型数量指数增长，非专家用户几乎只能依赖试错。本文改变的**核心 slot** 是“量化方案确定方式”——从“用户手工指定”变为“基于一次低分辨率全精度仿真的梯度信息自动推导”。

### 相对于已有工作的本质差异

**QuanTaichi**（Hu et al., 2021）提供了编译器层面的量化类型系统和位宽可配置的存储容器，但将位宽分配的决策完全留给用户。它未提供任何理论误差估计手段，用户需反复运行仿真来验证方案的可行性。本文在此基础上**保留了 QuanTaichi 的定点编解码算法**（见 Section 3.1 明确引用），但将方案生成过程自动化：通过可微仿真获取各量化变量对评价函数的梯度，将误差传播建模为梯度加权和，从而将离散位宽搜索转化为可通过拉格朗日乘数法解析求解的连续约束优化问题。

**人工精炼方案**（Human-designed scheme）代表了领域专家反复调试后的结果，但论文实验表明，在相同总位宽下，自动生成的方案相比人工精炼方案减少了 12.7% 的分数位宽，同时误差降低了 94.5%（Fig. 13）。这验证了基于梯度的优化能发现人类直觉难以捕捉的位宽分配策略——特别是变形梯度等缺乏直观物理意义的变量，其数值敏感性无法凭经验判断。

另一个关键差异在于**误差特性的主动干预**：已有量化仿真通常直接舍入，导致舍入误差在时间步间高度相关（Fig. 4），破坏误差传播公式的独立假设。本文引入**非减法抖动**（在编码前添加均匀随机噪声），使量化误差近似满足独立均匀分布，从而保证了误差估计模型的理论适用性。这一机制在已有工作中未见报道。

### 知识库挂载点

本文的方法论贡献可挂载到以下知识库节点：

1. **可微仿真与自动量化**：将量化误差传播建模为梯度加权和（Eq. 5 → Eq. 8），利用自动微分计算敏感性，属于可微仿真在系统优化问题上的新应用。该思路可推广到其他需要自动精度分配的可微计算图场景。

2. **约束优化驱动的系统参数选择**：将误差约束或内存约束下的位宽分配形式化为凸优化问题（Eq. 6, Eq. 7），并通过线性化得到解析解（Eq. 10），避免迭代搜索。这种“一次梯度采样 + 解析求解”的模式为其他资源受限的数值计算系统提供了范式参考。

3. **抖动在数值仿真中的应用**：抖动技术传统上用于信号处理的量化噪声白化，本文将其引入物理仿真的时间序列量化中，证明了其抑制数值偏差的有效性（Table 5, Fig. 12）。这为仿真领域的数值稳定性研究开辟了新方向。

4. **编译器级别的位打包存储**：本文实现的位打包容器（Fig. 7, Fig. 8）允许任意长度自定义数据在物理字中紧密排列，是对 QuanTaichi 位结构存储的改进，可挂载到 DSL 编译器的数据类型后端设计知识库。

### 适用边界与限制

本文方法存在明确的适用边界，需在知识库关联中标注：

- **分辨率迁移无理论保证**：量化方案从低分辨率仿真推导，直接应用于高分辨率仿真时，没有理论保证误差传播特性保持一致。论文仅通过实验（Fig. 15）验证了在 MPM 弹性体场景下方案可跨分辨率迁移，但未提供一般性条件。

- **线性化近似的局限**：优化求解基于单一梯度采样点的线性化，不进行迭代更新。Table 2 显示在误差约束下成功率为 136/160（85%），说明约 15% 的案例未能严格满足约束。对于强非线性仿真场景，可能需要更精确的二阶或迭代误差模型。

- **仅支持定点量化**：当前系统不支持浮点量化类型，无法自动确定指数与尾数的位宽分配。这限制了在动态范围变化剧烈场景下的适用性。

- **范围分析依赖固定膨胀因子**：数值范围通过全精度运行后乘以固定因子获得，在极端场景下仍可能发生溢出。论文未给出该因子的自适应调整策略。

### 后续研究启发

本文为以下研究方向提供了明确起点：

1. **迭代或二阶误差模型**：将当前的线性化单次求解扩展为基于多次采样或二阶梯度信息的迭代优化，以提高误差约束的满足率。

2. **浮点量化的自动位宽分配**：将框架扩展至浮点表示，自动确定指数位宽与尾数位宽，需要建立不同于定点量化的误差传播模型。

3. **自适应分辨率迁移**：研究低分辨率与高分辨率仿真差异较大时的自适应策略，例如基于残差估计的混合精度方案或在线位宽调整。

4. **跨仿真器泛化**：当前实现基于 Taichi 的可微仿真扩展，核心思路（梯度敏感性 + 约束优化）可迁移至其他支持自动微分的仿真框架，但需要验证误差传播模型在不同物理求解器下的适用性。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Automatic_Quantization_for_Physics_based_Simulation.pdf]]