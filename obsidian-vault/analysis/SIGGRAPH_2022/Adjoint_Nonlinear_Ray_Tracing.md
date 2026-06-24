---
title: Adjoint Nonlinear Ray Tracing
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Adjoint_Nonlinear_Ray_Tracing.pdf
project_link: "http://imaging.cs.cmu.edu/adjoint_nonlinear_tracing/"
code_link: "https://github.com/mitsuba-renderer/enoki"
aliases:
- ANRT
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 用伴随状态法（adjoint state method）替代反向模式自动微分，利用辛可逆积分器实现导数的恒定内存计算。
primary_logic: 通过引入正则参数化和可逆辛欧拉离散化，正向和反向传播共享同一条离散光线路径，无需存储中间状态，实现计算图压缩。
claims:
- 与反向模式自动微分相比，我们的方法内存使用恒定，运行时间线性增长。
- "在燃料注入重建中，我们的方法在所有折射率放大幅度下均显著优于Atcheson et al. [2008]，L2相对误差更低。"
- "离散前向和反向路径的数值差异在10^{-6}量级，验证了可逆积分的准确性。"
- 我们的方法能够处理大偏折光线，突破线性光线假设的限制。
---

# Adjoint Nonlinear Ray Tracing

> [!tip] 核心洞察
> 通过引入正则参数化和可逆辛欧拉离散化，正向和反向传播共享同一条离散光线路径，无需存储中间状态，实现计算图压缩。

| 字段 | 内容 |
|------|------|
| 中文题名 | 伴随非线性光线追踪 |
| 英文题名 | Adjoint Nonlinear Ray Tracing |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://imaging.cs.cmu.edu/adjoint_nonlinear_tracing/) · [Project](http://imaging.cs.cmu.edu/adjoint_nonlinear_tracing/) · [Code](https://github.com/mitsuba-renderer/enoki) |
| Topic | #topic/other_unclear |
| Method | Adjoint Nonlinear Ray Tracing |
| Dataset | GRIN透镜恢复 |

> [!tip] 效果简介
> - 燃料注入数据集 (SFB 382, DFG) 上，L2 相对误差 0.0014 (原始) / 0.014 (10x) / 0.29 (100x) / 3.8 (1000x) vs Atcheson et al. [2008]: 0.0110 / 0.113 / 1.28 / 19.3 (在所有放大倍数下相对误差更低)。
> - 内存与运行时间对比 (合成测试) 上，内存使用量 / 运行时间 内存恒定 (约1 GB以下)，运行时间随步数线性增长 vs 反向模式AD: 内存随步数线性增长，运行时间显著更高 (内存节省数个数量级，运行时间在多数步数下更快)。
> - GRIN透镜恢复 (Luneburg & Maxwell) 上，恢复折射率场与解析解的一致性 (定性) 恢复的折射率场与解析分布高度吻合 vs 无直接对比基线。

## 概要

本文针对**非线性光线追踪约束下折射率场优化的内存瓶颈**：基于反向模式自动微分（reverse-mode AD）的可微渲染在追踪步数增加时，内存消耗线性增长，难以支持高分辨率三维折射率场的梯度优化。

**核心方法**：将优化问题形式化为受Hamilton光线方程约束的终端损失最小化，引入**伴随状态法（adjoint state method）**替代反向模式AD。通过正则参数化变换和**显式可逆辛欧拉积分器**，正向追踪与反向伴随传播共享同一条离散光线路径，反向传播时无需存储中间光线轨迹，实现**内存消耗恒定的梯度计算**。

**主要结果**：
- 与反向模式AD相比，伴随方法内存使用恒定（约1 GB以下），运行时间随步数线性增长，在多数步数下更快（Figure 3）。
- 在燃料注入重建任务上，所有折射率放大幅度下均显著优于假设直线传播的Atcheson et al. (2008)方法（Table 2）。
- 成功应用于GRIN透镜设计、多焦显示、焦散设计、光纤优化及Luneburg/Maxwell透镜恢复等大偏折场景。

**方法定位**：将伴随状态法引入连续折射介质中的非线性光线传输，属于可微渲染与计算光学的交叉，为高分辨率折射率场反演提供了一种内存高效、可处理大偏折的优化框架。

## 核心方法与创新机理

### 问题瓶颈：非线性光线追踪的可微分内存爆炸

在连续折射率介质中，光线沿弯曲路径传播，其轨迹由Hamilton方程约束。当我们需要通过梯度下降优化折射率场时，必须计算目标函数对折射率场的导数。传统方法使用反向模式自动微分（reverse-mode AD），例如Mitsuba 2（Nimier-David et al., ACM TOG 2019）中的实现，需要在前向传播时存储完整的计算图——包括光线在每个积分步上的位置和速度。在三维体积优化中，光线步数与体积分辨率成正比、与步长成反比。随着分辨率的提高，存储所有中间状态所需的内存呈线性增长，使得高分辨率折射率场的优化在现有硬件上变得不可行。这一内存瓶颈是本文解决的核心问题。

### 核心机制：伴随状态法与可逆辛积分

本文的核心创新在于用**伴随状态法（adjoint state method）**替代反向模式自动微分，从根本上改变了梯度计算的实现路径。伴随状态法的关键思想是：将约束优化问题转化为无约束问题，通过引入拉格朗日乘子（伴随变量），推导出一组伴随常微分方程。这组方程可以从光线终点反向积分，直接累积目标函数对折射率场的梯度，而无需存储前向传播的中间状态。

然而，直接应用伴随状态法面临一个关键挑战：伴随方程中包含了折射率场的Hessian项，且需要前向光线路径的信息。本文通过两个紧密耦合的技术解决了这一问题：

1. **正则参数化变换**：引入正则参数 $\sigma$，满足 $\mathrm{d}\sigma \equiv \mathrm{d}s/\eta$，将原始的光学拉格朗日量转化为具有哈密顿结构的正则形式。在这一参数化下，Hamilton方程呈现为：
   $$\dot{\mathbf{x}} = \mathbf{v}, \quad \dot{\mathbf{v}} = \eta \nabla \eta$$
   其中 $\mathbf{x}$ 为光线位置，$\mathbf{v}$ 为速度，$\eta$ 为折射率场。这一变换使得动力学方程具有**辛结构（symplectic structure）**，为后续的可逆积分奠定了基础。

2. **显式可逆辛欧拉积分器**：利用辛结构的可逆性，设计了一个显式的辛欧拉积分方案。该积分器具有一个关键性质：给定终点状态，可以精确地反向积分回起点状态，且正向和反向路径的数值差异在 $10^{-6}$ 量级。这意味着在反向传播时，我们无需存储前向路径上的所有中间状态，而是可以从终点重新生成整条光线轨迹。

### 三个核心Changed Slots

| 技术组件 | 基线方法（反向模式AD） | 本文方法（伴随状态法） | 因果作用 |
|---------|---------------------|-------------------|---------|
| **梯度计算方法** | 通过计算图反向传播，逐节点累积梯度 | 求解伴随ODE，从终端边界条件反向积分直接累积梯度 | 消除了对计算图存储的依赖 |
| **内存消耗** | 与光线步数成正比（存储所有中间状态） | 恒定值（仅需存储终端状态和累积梯度） | 使得高分辨率优化在硬件上可行 |
| **前向状态存储** | 必须存储完整的光线位置序列 | 无需存储，通过可逆积分在反向传播时重新生成 | 实现计算图压缩，内存从O(N)降至O(1) |

### 方法框架：前向-反向双阶段流程

整个优化框架由三个模块组成，形成闭环迭代：

**模块一：前向非线性光线追踪**
从给定的初始条件 $(\mathbf{x}_0, \mathbf{v}_0)$ 出发，使用辛欧拉积分器沿正则参数 $\sigma$ 前向求解Hamilton方程，直到传播终止于 $\sigma_f$。在此过程中，计算终端损失函数 $C(\mathbf{x}(\sigma_f), \mathbf{v}(\sigma_f))$，例如光线终点与目标位置的L2距离：
$$C_i = \left\| \mathbf{x}(\sigma_f) - \hat{\mathbf{x}} \right\|^2$$
或图像渲染损失：
$$\mathcal{F}_i = \left\| \hat{I}_i - \iint W_{e,i} L_e \, d\mathbf{x}_0 d\mathbf{v}_0 \right\|^2$$
前向追踪完成后，仅保留终端状态 $(\mathbf{x}(\sigma_f), \mathbf{v}(\sigma_f))$ 和损失值，丢弃所有中间状态。

**模块二：反向伴随追踪**
从终端边界条件出发，使用**相同的可逆辛欧拉积分器**反向求解伴随方程。伴随变量 $\boldsymbol{\lambda}$ 和 $\boldsymbol{\mu}$ 满足：
$$\dot{\boldsymbol{\lambda}} = - (\nabla \eta (\nabla \eta)^\top + \eta \operatorname{Hess}(\eta)) \boldsymbol{\mu}, \quad \dot{\boldsymbol{\mu}} = -\boldsymbol{\lambda}$$
终端边界条件由损失函数对终端状态的导数给出：$\boldsymbol{\lambda}(\sigma_f) = \partial C/\partial \mathbf{x}$，$\boldsymbol{\mu}(\sigma_f) = \partial C/\partial \mathbf{v}$。在反向积分过程中，由于积分器的可逆性，前向路径上的光线位置和速度被精确地重新生成，同时伴随变量沿路径传播。折射率场的梯度通过伴随变量 $\boldsymbol{\mu}$ 加权累积：
$$\mathrm{d}_\eta \mathcal{L} = \int_0^{\sigma_f} (\eta \nabla (\mathrm{d}\eta) + \mathrm{d}\eta \nabla \eta)^\top \boldsymbol{\mu} \, \mathrm{d}\sigma$$

**模块三：折射率场更新**
利用模块二计算得到的梯度，通过Adam优化器更新折射率场的参数化表示。更新后的折射率场进入下一轮前向追踪，形成迭代优化循环。

### 模块间的因果链路

三个模块之间的因果关系紧密且不可分割：

1. **模块一 → 模块二**：前向追踪的终端状态决定了伴随方程的边界条件，而损失值的大小直接影响梯度的幅值。前向积分器的辛可逆性是模块二能够重新生成路径的前提——如果积分器不可逆，模块二将无法获取前向路径信息，梯度计算将不准确。

2. **模块二 → 模块三**：伴随追踪输出的梯度场是折射率场更新的唯一依据。梯度的准确性取决于伴随方程的正确推导和辛积分器的数值精度。本文证明，在相同的离散化方案下，正向和反向路径的数值差异仅为 $10^{-6}$ 量级，确保了梯度的可靠性。

3. **模块三 → 模块一**：更新后的折射率场改变了光线的传播路径，使得下一轮前向追踪产生不同的终端状态和损失值，驱动优化向目标方向收敛。

### 关键公式与变量含义

**拉格朗日量构造**：伴随状态法的起点是将约束优化问题转化为无约束问题。引入拉格朗日乘子 $\boldsymbol{\lambda}$ 和 $\boldsymbol{\mu}$ 后，增广拉格朗日量为：
$$\mathcal{L} = C(\mathbf{x}(\sigma_f), \mathbf{v}(\sigma_f)) - \int_0^{\sigma_f} \boldsymbol{\lambda}^\top (\dot{\mathbf{x}} - \mathbf{v}) d\sigma - \int_0^{\sigma_f} \boldsymbol{\mu}^\top (\dot{\mathbf{v}} - \eta \nabla \eta) d\sigma$$
其中积分项强制Hamilton方程作为约束。通过对 $\mathcal{L}$ 进行变分，令各变量的变分为零，即可导出伴随方程和梯度表达式。

**正则参数化的核心作用**：正则参数 $\sigma$ 的引入使得Hamilton方程具有辛结构，这是可逆积分的基础。在原始弧长参数化下，光线方程是二阶ODE，缺乏显式的辛结构，难以设计可逆积分器。正则参数化将问题转化为一阶哈密顿系统，使得辛欧拉积分器可以显式应用。

**梯度表达式的物理含义**：梯度 $\mathrm{d}_\eta \mathcal{L}$ 的表达式表明，折射率场在某点的梯度由伴随变量 $\boldsymbol{\mu}$ 在该点的值加权，权重包含折射率及其梯度的局部信息。直观上，$\boldsymbol{\mu}$ 可以理解为"反向传播的光线动量"，它携带了终端损失对路径上各点的敏感性信息。

### 训练与推理路径

**训练（优化）路径**：给定测量图像或目标几何约束，迭代执行前向追踪 → 反向伴随追踪 → 梯度更新三个步骤。每次迭代中，前向追踪计算当前折射率场下的光线路径和损失，反向追踪计算梯度，Adam优化器更新折射率场。整个过程的内存消耗恒定，不随步数增长。

**推理路径**：优化完成后，折射率场被固定。对于新的初始条件，仅需执行前向追踪即可得到光线路径和终端状态。此时不再需要梯度计算，但可逆积分器的性质确保了前向追踪的数值稳定性。

## 实验与关键发现

### 内存与运行时间的根本性优势

本方法最核心的工程贡献在于将可微分非线性光线追踪的内存消耗从“随步数线性增长”压至恒定。图3的系统性对比表明：伴随状态法在任意光线步数下内存占用保持恒定（约1 GB以下），而基于反向模式自动微分（reverse-mode AD）的基线（Nimier-David et al., ACM TOG 2019）内存消耗随步数线性攀升，在步数较多时可达数个数量级的差距。运行时间方面，伴随状态法随步数线性增长，且在绝大多数步数配置下均快于反向模式AD。这一优势的因果链条清晰：正向追踪采用显式可逆辛欧拉积分器，反向传播时无需存储中间光线位置，而是通过相同的可逆积分器从终端边界条件反向重演正向路径，将整个非线性光线追踪压缩为计算图中的单一节点。

离散可逆性的数值精度经过严格验证：正向积分与反向积分所得光线路径的相对差异在 $10^{-6}$ 量级，表明辛积分器的可逆性在实际计算中足够精确，不会因数值误差累积而破坏梯度计算的正确性。

### 气体流折射率场重建：突破线性假设

在燃料注入数据集（SFB 382, DFG）的重建实验中，本方法与假设光线直线传播的 **Atcheson et al.**（ACM TOG 2008）方法进行了系统对比。Table 2 报告了不同折射率放大幅度下的 L2 相对误差：

| 折射率放大幅度 | 本方法 L2 相对误差 | Atcheson et al. [2008] |
|:---:|:---:|:---:|
| 原始 (1×) | 0.0014 | 0.0110 |
| 10× | 0.014 | 0.113 |
| 100× | 0.29 | 1.28 |
| 1000× | 3.8 | 19.3 |

在所有放大倍数下，本方法的相对误差均显著低于基线。当折射率梯度增大导致光线偏折加剧时，Atcheson et al. 的线性光线假设迅速失效，误差急剧上升；而本方法通过显式求解非线性光线方程，即使在大偏折场景下仍能恢复出有意义的折射率场（Figure 10 的可视化对比直观展示了这一差异）。需注意，在 1000× 放大时，本方法的相对误差也升至 3.8，说明极端梯度下重建质量仍会退化，但退化程度远轻于基线。

### GRIN透镜逆向设计的定性验证

在 Luneburg 透镜和 Maxwell 鱼眼透镜的恢复实验中（Figure 8），本方法从合成测量数据优化得到的折射率场与解析解高度吻合，中心轴剖面的折射率分布与 ground truth 几乎重合。这验证了伴随梯度在已知解析解场景下的正确性和优化收敛能力。

多焦点显示（Figure 6）和焦散设计（Figure 7）等应用进一步展示了方法的灵活性：前者优化 GRIN 透镜使单一掩模图案在不同距离平面上形成不同的聚焦图像，后者设计折射率场使焦散图案在传感器移动时保持形状稳定。

![[assets/figures/papers/paper_list_l5_https_imaging_cs_cmu_edu_adjoint_nonlinear_tracing_repair/figures/006_Figure_6.jpg]]
*Figure 6: A multifocal display. (Row 1) Collimated light passes through a mask to form an all-in-focus projected image of a lego scene. Placing a GRIN lens in front of the mask produces a 2D intensity distribution that can change as a function of distance. We optimize this GRIN lens to create a focal stack of this lego scene. (Row 2) The optimized intensity distribution at different plane positions, where plane A is the closest to the GRIN lens and plane C is the furthest. (Row 3) The target (ground truth) focal stack*

![[assets/figures/papers/paper_list_l5_https_imaging_cs_cmu_edu_adjoint_nonlinear_tracing_repair/figures/009_Figure_7.jpg]]
*Figure 7: Caustic design. The caustic pattern remains in shape as the sensor moves away from the volume. Since the cost function does not promote uniform energy distribution, the caustic contains bright spots*

### 体积分辨率的消融实验

Figure 5 展示了体积分辨率从 $33^3$ 增至 $257^3$ 时图像重建质量的逐步提升。这一消融实验表明，更高的空间分辨率允许折射率场表达更精细的空间变化，从而更准确地控制光线偏折以实现目标图像。但分辨率提升也意味着优化变量数立方级增长，对计算资源和收敛性提出更高要求——论文未报告在更高分辨率下的收敛失败案例，这一点需要在实际应用中验证。

![[assets/figures/papers/paper_list_l5_https_imaging_cs_cmu_edu_adjoint_nonlinear_tracing_repair/figures/007_Figure_5.jpg]]
*Figure 5: Effect of volume resolution. We optimize volumes of different resolution to reproduce a picture of Albert Einstein, under the same setting as in Figure 4. As the volume resolution increases, so does reproduction accuracy. The image is courtesy of Yousuf Karsh. ©Yousuf Karsh*

### 光纤设计的定量对比

在光纤设计任务中（Figure 9），本方法优化得到的折射率剖面与抛物线型 GRIN 光纤剖面进行了对比。优化设计展现出更优的点扩散函数（PSF），在焦点处的光斑更集中。这一定量改进源于方法能够自由优化折射率分布，而非受限于预设的函数形式。

![[assets/figures/papers/paper_list_l5_https_imaging_cs_cmu_edu_adjoint_nonlinear_tracing_repair/figures/008_Figure_9.jpg]]
*Figure 9: A comparison between the optimized fiber design and the parabolic profile. (a) A cross-section of each fiber with the ray trajectories. Light disperses the farther it travels in both fibers, but much less so in the optimized fiber. (b) Images of the focused source at each of the focus points in the fibers. The images from the optimized fiber are better focused. (c) A cross-section of the images, showing the PSF of the fiber at each of the focus points. The optimized fiber retains better focus at the farther hop*

### 方法的适用边界与失败模式

论文明确指出的限制条件构成了方法的适用边界：

1. **局部极小值敏感性**：优化需要良好的初始化，否则容易陷入局部极小。论文未提出系统性的初始化策略，这在实际部署中可能成为瓶颈。
2. **测量数据充分性未知**：在重建任务中，需要多少及何种测量数据才能唯一地恢复折射率场是一个开放问题。当前实验使用已知的测量配置，但未分析欠定条件下的失效模式。
3. **纯折射假设**：当前方法仅适用于无散射的纯折射介质，无法处理体积散射效应。对于烟雾、生物组织等散射性介质，方法直接失效。
4. **离散化偏差**：辛欧拉积分器的步长越大，离散化引入的偏差越大。论文未量化步长与梯度精度之间的关系，也未提出自适应步长策略。
5. **制造约束缺失**：优化得到的 GRIN 透镜折射率分布可能无法实际制造（如折射率变化过于剧烈或超出材料可实现范围），方法未融入可制造性约束。

这些限制表明，本方法在“可微分非线性光线追踪”这一核心问题上取得了突破，但在从仿真优化到实际系统部署的链条上仍存在多个待解决的工程与理论问题。

![[assets/figures/papers/paper_list_l5_https_imaging_cs_cmu_edu_adjoint_nonlinear_tracing_repair/figures/005_Figure_3.jpg]]
*Figure 3: Runtime and memory use comparison for reverse-mode AD and the adjoint method. The number of steps along a ray is directly proportional to resolution and inversely proportional to step size. For the adjoint method, memory use is constant and runtime increases linearly as a function of the number of steps along a ray. By contrast, memory usage and runtime for reverse-mode AD are both significantly higher. This is because reverse-mode AD requires keeping track of the entire light path to compute gradients*

![[assets/figures/papers/paper_list_l5_https_imaging_cs_cmu_edu_adjoint_nonlinear_tracing_repair/figures/004_Figure_4.jpg]]
*Figure 4: The optimized GRIN lens displaying two images. (Top) Two collimated beams of light (red and blue) simultaneously illuminate two faces of a cubic GRIN lens, which steers the light to form two distinct images on a wall. (Bottom) The optimized images of Albert Einstein and Alan Turing, and the corresponding target images. The image of Albert Einstein is a portrait by Yousuf Karsh. ©Yousuf Karsh. The portrait of Alan Turing is by Elliot & Fry Studio. ©National Portrait Gallery*

## 定位与知识库关联

本文的核心贡献在于改变了可微分渲染管线中**梯度计算这一关键 slot**：将传统的反向模式自动微分（reverse-mode AD）替换为**伴随状态法（adjoint state method）**，从而将非线性光线追踪的导数计算从“内存随步数线性增长”变为“恒定内存”。这一改变直接突破了此前限制高分辨率折射率场优化的内存瓶颈。

### 相对于已有方法的本质差异

**相对于反向模式自动微分（如 Mitsuba 2, Nimier-David et al., ACM TOG 2019）**：
传统可微分渲染器将整个非线性光线追踪过程展开为计算图，逐步存储中间状态（光线位置、速度），在反向传播时通过链式法则累积梯度。这导致内存消耗与光线步数成正比——当体积分辨率提高、步长减小时，内存需求迅速膨胀至数十 GB 甚至无法运行。本文的方法则利用**辛可逆积分器**使前向追踪过程可逆，反向传播时无需存储中间状态，而是沿同一条离散路径反向重演，仅需存储伴随状态变量（λ, μ）的当前值。本质上，这是将“存储计算图”替换为“重新计算”，但通过可逆性保证了重新计算的数值精确性（前向与反向路径的数值差异在 $10^{-6}$ 量级）。这使得内存使用降至恒定值（约 1 GB 以下），且运行时间随步数仅线性增长，在多数步数下反而快于反向模式 AD（Figure 3）。

**相对于 Atcheson et al.（ACM TOG 2008）的气体流重建方法**：
Atcheson 等人的方法建立在**光线直线传播假设**之上，即忽略折射导致的光线弯曲，仅适用于折射率变化微小的弱偏折场景。本文方法直接求解完整的 Hamilton 方程，能够处理大偏折光线（折射率放大 100× 甚至 1000×），从而在强折射率梯度场景中显著优于线性假设方法。在燃料注入数据集上，本文方法在所有折射率放大幅度下的 L2 相对误差均更低（Table 2），且当放大倍数增大时，Atcheson 方法的重建质量急剧恶化，而本文方法仍能保持合理的重建精度（Figure 10）。

**相对于传统 GRIN 透镜设计（如抛物型光纤剖面）**：
传统 GRIN 透镜设计依赖解析解或参数化剖面（如 Luneburg 透镜的球对称分布、抛物型折射率剖面），设计自由度受限于预设的函数形式。本文方法将折射率场视为可优化的体积场，不预设任何对称性或函数形式，从而能够设计出性能超越传统剖面的光纤（Figure 9）以及实现多图像投影（Figure 4）、多焦面显示（Figure 6）、焦散图案设计（Figure 7）等传统方法难以实现的复杂光学功能。

### 知识库挂载点

本文的方法论可挂载至以下知识库节点：

1. **可微分渲染（Differentiable Rendering）**：作为可微分渲染管线中“物理约束的梯度计算”这一子模块的替代方案。本文证明了对于具有 ODE/PDE 约束的优化问题，伴随状态法在内存效率上优于通用的反向模式 AD。这一思想可推广至其他以微分方程为约束的可微分模拟问题（如流体模拟、弹性体模拟中的可微物理）。

2. **计算成像中的折射率场重建（Tomographic Refractive Index Reconstruction）**：本文为基于光线偏折的折射率场层析重建提供了统一的优化框架。与传统的基于直线路径的代数重建技术（ART）或滤波反投影不同，本文方法天然处理非线性光线路径，可视为将“光线追踪”与“逆问题求解”紧密耦合的端到端方法。

3. **光学设计与逆向设计（Optical Design / Inverse Design）**：本文为 GRIN 透镜的逆向设计提供了高自由度优化工具。与基于形状优化的传统透镜设计不同，本文直接在体积折射率场上优化，可探索更丰富的设计空间。该框架可进一步与制造约束结合，用于实际 GRIN 元件的可制造性优化。

4. **自动微分技术（Automatic Differentiation）**：本文是“checkpointing”策略（以计算换内存）在连续动力学系统中的一种特例——通过可逆积分器实现了零存储开销的精确 checkpointing。与一般的近似 checkpointing（如每隔若干步存储一次）不同，本文的可逆性保证了数值精度不损失。

### 适用边界

- **介质类型边界**：当前方法仅适用于纯折射介质（无散射、无吸收），不适用于参与介质（participating media）。将散射纳入伴随框架需要重新推导伴随方程，这是论文明确指出的开放问题。
- **初始化敏感性**：优化需要良好的初始折射率场，否则容易陷入局部极小值。论文未提供系统性的初始化策略，这是实际应用中的重要限制。
- **测量数据充分性**：在重建任务中，折射率场的唯一恢复需要足够的测量数据，但论文未给出充分条件的理论分析。数据不足时可能导致解的非唯一性。
- **离散化偏差**：辛欧拉积分器虽然是可逆的，但仍引入离散化偏差，步长越大偏差越大。论文未分析该偏差对梯度准确性和最终优化结果的影响。
- **制造约束缺失**：当前优化不考虑实际 GRIN 透镜的可制造性（如折射率变化范围、空间梯度上限等），优化结果可能无法直接用于制造。

### 后续启发

本文的恒定内存伴随光线追踪为多个方向打开了可能性：

- **高分辨率体积优化**：内存瓶颈的解除使得在更高分辨率（如 $512^3$ 或更高）的体积场上进行优化成为可能，这对气体动力学测量、生物组织成像等应用具有重要意义。
- **多物理场耦合的伴随方法**：本文的框架可扩展至包含散射、吸收、偏振等更复杂的光学效应，也可与热传导、流体动力学等物理场耦合，实现多物理场的联合逆向设计。
- **实时或交互式折射设计**：恒定内存和线性时间复杂度的特性使得该方法有望集成到交互式设计工具中，设计师可以实时调整目标图案并观察 GRIN 透镜的优化结果。
- **神经折射场（Neural Refractive Fields）**：本文的伴随方法可与神经表示（如 NeRF 风格的神经网络参数化折射率场）结合，利用伴随状态法计算网络参数的梯度，实现更紧凑、更平滑的折射率场表示。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Adjoint_Nonlinear_Ray_Tracing.pdf]]