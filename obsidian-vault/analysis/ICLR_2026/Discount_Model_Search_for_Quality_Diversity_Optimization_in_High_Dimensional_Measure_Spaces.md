---
title: "Discount Model Search for Quality Diversity Optimization in High-Dimensional Measure Spaces"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Discount_Model_Search_for_Quality_Diversity_Optimization_in_High_Dimensional_Measure_Spaces.pdf
project_link: https://discount-models.github.io
code_link: null
openreview_forum_id: m6Hv0yZO3n
aliases:
- DMSD
- DMSQDOHDMS
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "折扣函数的表示方式：从离散的单元直方图转换为平滑的连续神经网络模型。"
primary_logic: "平滑且连续的折扣函数表示能够在测度相近时为不同解分配有区分度的改进值，从而在高维、高畸变的测度空间中维持有效的探索引导。"
claims:
- "CMA-MAE 的直方图折扣函数在测度相近时导致多个解落入同一单元并获得相同的折扣值，进而无法区分改进方向。"
- "在高维测度空间中，CMA-MAE 探索到的唯一存档单元数量随迭代急剧下降（例如在 10D LP (Sphere) 中降至约 30），证明畸变效应被放大。"
- "DMS 的平滑折扣模型能够在相同测度区域给出不同的折扣值，从而提供更强的改进排序信号。"
- "DMS 在几乎所有基准（包括高维 LP 和 QDDM 域）中均在 QD 分数和覆盖率上显著优于 CMA-MAE 和其他基线。"
---

# Discount Model Search for Quality Diversity Optimization in High-Dimensional Measure Spaces

> [!tip] 核心洞察
> 平滑且连续的折扣函数表示能够在测度相近时为不同解分配有区分度的改进值，从而在高维、高畸变的测度空间中维持有效的探索引导。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 高维测度空间中的质量多样性优化折扣模型搜索 |
| 英文题名 | Discount Model Search for Quality Diversity Optimization in High-Dimensional Measure Spaces |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=m6Hv0yZO3n) · [Project](https://discount-models.github.io) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Discount Model Search (DMS) |
| Dataset | 2D LP (Sphere), 10D LP (Sphere) |

> [!tip] 效果简介
> - 2D LP (Sphere) 上，QD Score 为 6,978.20，对比 6,327.90，变化 +650.30。
> - 2D LP (Sphere) 上，Coverage 为 95.89%，对比 80.95%，变化 +14.94%。
> - 10D LP (Sphere) 上，QD Score 为 6,409.50，对比 608.53，变化 +5,800.97。

## 概要

### 问题瓶颈

质量多样性（Quality Diversity, QD）优化的目标是在测度空间中同时追求解的高目标值和高多样性。当前最先进的黑盒 QD 算法 **CMA-MAE**（Fontaine & Nikolaidis, 2023）使用离散的直方图表示折扣函数——将测度空间划分为单元，每个单元存储一个标量折扣值。然而，在高维测度空间中，这一离散表示引发了严重的**畸变效应**：大量解落入相同的存档单元，获得完全相同的折扣值，导致改进信号 $\Delta(\boldsymbol{\theta}) = f(\boldsymbol{\theta}) - f_A(\boldsymbol{m}(\boldsymbol{\theta}))$ 失效，搜索随之停滞。实验表明，在 10 维线性投影（Sphere）基准上，CMA-MAE 探索到的唯一存档单元数量随迭代急剧下降至仅约 30 个（Figure 1c），几乎完全丧失了探索能力。

### 核心思路

本文的核心洞察是：**平滑且连续的折扣函数表示**能够在测度相近时为不同解分配有区分度的改进值，从而在高维、高畸变的测度空间中维持有效的探索引导。基于此，我们提出 **Discount Model Search (DMS)**，用一个神经网络参数化的平滑折扣模型 $\hat{f}_A(\cdot; \psi)$ 替代 CMA-MAE 的离散直方图。该模型以测度值为输入，输出连续的折扣值，使得即使解落入测度空间的相近区域，也能获得不同的改进排序信号（Figure 1b）。此外，DMS 引入**空点训练机制**：从未被占据的存档单元中心采样“空点”，并以最小目标值 $f_{min}$ 作为训练目标，强制折扣模型在未探索区域输出低值，从而避免对探索程度的误判。

### 方法定位

DMS 属于黑盒 QD 算法，在 MAP-Elites 风格的存档和 CMA-ES 发射器框架下，将折扣函数从离散直方图替换为连续神经网络模型。与仅进行多样性优化的 **DDS**（Lee et al., 2024）不同，DMS 同时优化目标值和多样性；与经典 **MAP-Elites**（Mouret & Clune, 2015）及其变体 **MAP-Elites (line)**（Vassiliades & Mouret, 2018）相比，DMS 通过平滑折扣模型实现了更高效的探索引导。

### 主要结果

在涵盖线性投影（LP）、Arm Repertoire、三角形排列（TA）和潜在空间插值（LSI）的多个域中，DMS 在 QD 分数和覆盖率上全面优于 CMA-MAE 及其他基线（Table 1）。在高维场景中优势尤为显著：10 维 LP (Sphere) 上 QD 分数从 608.53 提升至 6,409.50，覆盖率从 6.95% 提升至 89.21%；10 维 LP (Rastrigin) 上 QD 分数从 246.55 提升至 5,138.81，覆盖率从 2.98% 提升至 88.19%。在 LSI (Hiker) 域中，DMS 能够根据风景图像测度生成与之匹配的登山者图像（Figure 2），展示了该方法在“质量多样性扩散模型”（QDDM）域中的潜力。消融实验进一步确认了空点机制的关键作用：去除空点会导致折扣模型在未探索区域误输出高值，使性能崩溃（Figure 11）。

质量多样性（Quality Diversity, QD）优化的目标是在一个解空间中同时追求解的高目标值（质量）和测度空间中的广泛覆盖（多样性）。近年来，黑盒 QD 算法在机器人控制、程序生成、图像生成等领域取得了显著进展，但其可扩展性始终受限于测度空间的维度。大多数经典 QD 算法——如 **MAP-Elites**（Mouret & Clune, 2015）及其变体 **MAP-Elites (line)**（Vassiliades & Mouret, 2018）——依赖对测度空间的显式网格划分来维护存档，当测度维度升高时，网格单元数量呈指数爆炸，使得这种离散化策略在计算上不可行。

**CMA-MAE**（Fontaine & Nikolaidis, 2023）通过引入折扣函数（discount function）和 CMA-ES 发射器，将 QD 优化重新表述为直接最大化存档改进（archive improvement）：

$$\Delta(\boldsymbol{\theta}) = f(\boldsymbol{\theta}) - f_A(\boldsymbol{m}(\boldsymbol{\theta}))$$

其中 $f(\boldsymbol{\theta})$ 是解的目标值，$f_A(\boldsymbol{m}(\boldsymbol{\theta}))$ 是在测度 $\boldsymbol{m}(\boldsymbol{\theta})$ 处的折扣值。CMA-MAE 将折扣函数 $f_A$ 表示为一个离散直方图：将测度空间划分为单元，每个单元存储一个标量接收阈值 $t_e$，并通过指数移动平均更新：

$$t_e \gets (1-\alpha) t_e + \alpha f(\boldsymbol{\theta}')$$

这一设计使得 CMA-MAE 无需预先定义网格分辨率，从而在理论上适用于任意维度的测度空间。

然而，CMA-MAE 的离散直方图表征在高维测度空间中暴露出根本性缺陷。如 Figure 1(a) 所示，当多个解落入同一存档单元时，它们会获得完全相同的折扣值，导致改进信号 $\Delta_i$ 无法区分这些解的相对优劣。更严重的是，高维测度空间中的畸变效应（distortion）会放大这一问题：随着维度升高，解在测度空间中的分布高度集中，CMA-MAE 探索到的唯一存档单元数量急剧下降——在 10D LP (Sphere) 基准中，这一数字在迭代过程中骤降至约 30（Figure 1(c)），意味着搜索几乎停滞。

**DDS**（Lee et al., 2024）通过核密度估计替代折扣函数，实现了纯多样性优化，在覆盖率上表现优异，但其目标值较低，因为它放弃了质量优化的引导。

本文的核心动机在于：**离散的直方图折扣函数是高维 QD 优化的瓶颈**。当测度相近的解无法获得有区分度的改进值时，CMA-ES 发射器失去了有效的排序信号，导致探索崩溃。一个自然的解决方案是将折扣函数从离散单元映射转变为平滑的连续表示——这正是本文提出 Discount Model Search (DMS) 的出发点。

## 核心方法与创新机理

DMS 的核心创新在于将 CMA-MAE 中**离散的直方图折扣函数替换为平滑的连续神经网络折扣模型**，并配套引入**空点训练机制**以防止模型在未探索区域产生误导性高值。这一设计直接回应了高维测度空间中的根本瓶颈：当测度空间维度升高时，CMA-MAE 的直方图表示因畸变效应导致大量解落入同一单元并获得相同的折扣值，从而使改进信号 $\Delta(\boldsymbol{\theta}) = f(\boldsymbol{\theta}) - f_A(\boldsymbol{m}(\boldsymbol{\theta}))$ 失去区分度，搜索陷入停滞（Figure 1a, 1c）。

具体而言，DMS 在以下两个关键槽位上做出了改变：

**1. 折扣函数表示：从离散直方图到平滑神经网络**

- **Baseline（CMA-MAE）**：将测度空间按单元划分，每个单元存储一个标量折扣值 $t_e$，构成离散的直方图表示。在高维测度空间中，解向量经测度函数映射后高度集中于少数单元，导致不同解获得相同的折扣值，改进排序信号失效。
- **DMS**：用一个参数为 $\psi$ 的神经网络 $\hat{f}_A(\cdot; \psi)$ 来参数化折扣函数，以测度值为输入并输出连续的折扣值。这一平滑表示能够在测度相近时为不同解分配有区分度的折扣值，使得改进值 $\Delta_i$ 能够提供更强的搜索引导信号（Figure 1b）。实验表明，在 10D LP (Sphere) 中，CMA-MAE 探索到的唯一存档单元数急剧下降至约 30，而 DMS 的平滑折扣模型有效规避了此问题，QD 分数从 608.53 提升至 6,409.50，覆盖率从 6.95% 提升至 89.21%（Table 1）。

**2. 空点训练机制：强制未探索区域保持低折扣值**

- **Baseline（CMA-MAE）**：不存在此机制，仅由发射器采样的解来更新折扣值。
- **DMS**：在每轮迭代中，从未被占据的存档单元中心采样 $n_{empty}$ 个“空点”，并以最小目标值 $f_{min}$ 作为训练目标加入数据集 $\mathcal{D}_A$。这强制折扣模型在未探索区域输出低值，从而为发射器提供正确的探索激励。消融实验表明，去除空点（$n_{empty}=0$）会导致折扣模型在未探索区域产生任意高值，使发射器错误地认为测度空间已被完全探索，QD 分数和覆盖率大幅崩溃（Figure 11, Appendix D.2）；仅需添加少量空点（≥10）即可恢复高性能（Figure 10）。

**为什么这两个改变在高维测度空间中至关重要？**

线性投影（LP）测度函数将解向量划分为 $k$ 个块并对每块分量求和，其输出服从 Irwin-Hall 分布（Figure 12）。当测度维度 $k$ 增大时，该分布迅速向中心集中，导致解在测度空间中的分布产生严重畸变——绝大多数解落入极少数单元。CMA-MAE 的离散直方图在此情况下无法提供有意义的改进信号，而 DMS 的平滑折扣模型天然具备跨单元插值能力，使相近但不同测度的解获得有区分的折扣值，从而维持有效的探索引导。空点机制则进一步确保模型不会在未探索区域“猜测”出高折扣值，避免搜索过早收敛到已探索区域的局部最优。

DMS 的整体工作流程围绕两个交替进行的阶段展开：**发射器搜索**与**折扣模型训练**，二者共享一个 MAP-Elites 风格的存档。

### 核心组件与数据流

1. **存档（Archive）**：采用 MAP-Elites 风格的网格划分，将测度空间离散化为若干单元，每个单元保留迄今为止在该测度区域内发现的目标值最优解。存档既作为最终输出的“精英集合”，也为折扣模型提供训练信号。

2. **CMA-ES 发射器（Emitter）**：DMS 维护多个 CMA-ES 实例作为解生成器。每个发射器从自身的高斯分布中采样新解 $\boldsymbol{\theta}$，计算其测度值 $\boldsymbol{m}(\boldsymbol{\theta})$ 和目标值 $f(\boldsymbol{\theta})$，然后通过折扣模型获取该测度处的折扣值 $\hat{f}_A(\boldsymbol{m}(\boldsymbol{\theta}); \psi)$，进而计算存档改进值：

   $$\Delta(\boldsymbol{\theta}) = f(\boldsymbol{\theta}) - \hat{f}_A(\boldsymbol{m}(\boldsymbol{\theta}); \psi)$$

   发射器以最大化 $\Delta$ 为目标，根据改进排序更新自身的均值与协方差矩阵，从而将搜索引导向“目标值高且当前折扣值低”的测度区域。

3. **折扣模型（Discount Model）**：一个由参数 $\psi$ 表示的神经网络，以测度值为输入，输出该测度处的平滑连续折扣值。其核心作用是替代 CMA-MAE 中的离散直方图折扣函数，使得测度相近但落在不同单元的解能够获得有区分度的折扣值，从而维持有效的改进信号。

4. **训练数据集收集**：每轮迭代中，训练集 $\mathcal{D}_A$ 由两部分构成：
   - **发射器采样点**：对于发射器生成的每个解，根据其目标值与当前折扣模型输出的关系计算折扣目标 $t_A$：

     $$t_A = \begin{cases} \hat{f}_A(s) & \text{if } f(\theta) \leq \hat{f}_A(s) \\ (1-\alpha)\hat{f}_A(s) + \alpha f(\theta) & \text{if } f(\theta) > \hat{f}_A(s) \end{cases}$$

     其中 $\alpha$ 为存档学习率，控制目标值对折扣的拉动速度。当新解的目标值不高于当前折扣时，目标保持不变；当新解的目标值更高时，目标按 $\alpha$ 比例向目标值混合上升。
   - **空点（Empty Points）**：从未被占据的存档单元中心采样 $n_{\text{empty}}$ 个点，以全局最小目标值 $f_{\text{min}}$ 作为折扣目标加入训练集。这一机制强制折扣模型在尚未探索的测度区域输出低值，从而引导发射器向这些区域探索。

5. **折扣模型回归**：在每轮迭代的模型训练阶段，使用均方误差（MSE）损失对 $\mathcal{D}_A$ 进行回归训练，使折扣模型 $\hat{f}_A(\cdot; \psi)$ 逼近由数据集中折扣目标所定义的函数。

### 迭代流程

DMS 的完整迭代循环可概括为以下步骤：

1. **发射器采样**：各 CMA-ES 发射器从当前分布中采样一批解。
2. **存档更新**：对于每个解，若其目标值优于存档中对应单元的解，则替换之；同时更新对应单元的折扣目标 $t_A$。
3. **发射器更新**：根据折扣模型输出的改进值 $\Delta$ 对解排序，更新 CMA-ES 的均值与协方差。
4. **空点采样**：从未占据的存档单元中随机采样空点，以 $f_{\text{min}}$ 为目标加入训练集。
5. **折扣模型训练**：在累积的 $\mathcal{D}_A$ 上训练折扣模型。

### 关键设计决策

- **平滑折扣表示**：用神经网络替代离散直方图是本框架的根本创新。在高维测度空间中，CMA-MAE 的直方图表示因“畸变效应”导致大量解落入同一单元并获得相同折扣值，使改进信号失效。DMS 的平滑模型能够在测度相近时为不同解分配有区分度的折扣值，从而维持有效的探索引导。
- **空点机制的必要性**：消融实验表明，若取消耗折扣模型训练中的空点（$n_{\text{empty}}=0$），折扣模型会在未探索区域产生任意高值，使发射器误认为测度空间已被完全探索，导致 QD 分数和覆盖率大幅崩溃。仅需添加少量空点（≥10）即可恢复高性能。
- **存档学习率 $\alpha$**：控制目标优化与探索之间的平衡。$\alpha \to 0$ 时 DMS 退化为纯单目标优化，覆盖度极低；$\alpha$ 在 0.1 附近通常取得最佳综合性能。

### 问题瓶颈与改进信号

DMS 的核心目标是解决 CMA-MAE 在高维测度空间中的畸变失效问题。在 CMA-MAE 中，存档改进值定义为：

$$\Delta(\boldsymbol{\theta}) = f(\boldsymbol{\theta}) - f_A(\boldsymbol{m}(\boldsymbol{\theta}))$$

其中 $f(\boldsymbol{\theta})$ 为目标值，$\boldsymbol{m}(\boldsymbol{\theta})$ 为解的测度向量，$f_A$ 为折扣函数。CMA-MAE 将 $f_A$ 表示为测度空间单元划分上的离散直方图，每个单元存储一个标量折扣值，并通过学习率 $\alpha$ 更新接收阈值：

$$t_e \gets (1-\alpha) t_e + \alpha f(\boldsymbol{\theta}')$$

当测度空间维度升高时，大量解落入相同单元并获得相同的折扣值，导致改进信号 $\Delta$ 失效，搜索停滞（Figure 1(a), Section 4）。在 10D LP (Sphere) 中，CMA-MAE 探索到的唯一存档单元数急剧下降至约 30 个（Figure 1(c)），证实畸变效应被放大。

### 折扣模型

DMS 将折扣函数从离散直方图替换为由神经网络参数化的平滑折扣模型 $\hat{f}_A(\cdot; \psi)$，以测度值 $\boldsymbol{m}(\boldsymbol{\theta})$ 为输入并输出连续折扣值。该平滑表示能够在测度相近时为不同解分配有区分度的改进值，从而在高维测度空间中维持有效的探索引导（Figure 1(b), Section 5）。

折扣模型的训练目标 $t_A$ 由以下规则确定：

$$t_A = \begin{cases} \hat{f}_A(s) & \text{if } f(\theta) \leq \hat{f}_A(s) \\ (1-\alpha)\hat{f}_A(s) + \alpha f(\theta) & \text{if } f(\theta) > \hat{f}_A(s) \end{cases}$$

其中 $s = \boldsymbol{m}(\theta)$ 为解的测度值。当新解的目标值不超过当前折扣时，目标保持原值；当新解的目标值超过当前折扣时，目标按存档学习率 $\alpha$ 在旧折扣与新目标值之间进行线性混合。该规则使折扣模型逐步逼近已探索区域中达到的最高目标值。

### 空点训练机制

为防止折扣模型在未探索区域输出任意高值（从而导致发射器误认为测度空间已被完全探索），DMS 引入空点训练机制。在每轮迭代中，从存档中随机采样 $n_{empty}$ 个未被占据的单元，将其中心测度值加入训练数据集 $\mathcal{D}_A$，并以全局最小目标值 $f_{min}$ 作为训练目标（Algorithm 1 lines 21-23）。该机制强制折扣模型在未探索区域输出低值，确保发射器持续向未探索区域分配搜索资源。

消融实验证实，去除空点（$n_{empty}=0$）会导致折扣模型在未探索区域误输出高值，使 QD 分数和覆盖率大幅下降；仅需添加少量空点（$\geq 10$）即可恢复高性能（Figure 10, Figure 11, Appendix D.2）。

### 算法流程

DMS 在每个迭代中交替执行两个阶段：

1. **发射器搜索阶段**：CMA-ES 发射器从高斯分布采样新解，根据改进值 $\Delta_i = f(\boldsymbol{\theta}_i) - \hat{f}_A(\boldsymbol{m}(\boldsymbol{\theta}_i))$ 排序，并更新均值和协方差以优化存档改进（Algorithm 1 lines 9, 17-18）。
2. **折扣模型训练阶段**：从发射器采样的解和空存档单元中心收集 $(\text{测度}, \text{折扣目标})$ 对构成 $\mathcal{D}_A$，使用 MSE 损失对折扣模型进行回归训练，使其逼近正确的折扣函数（Algorithm 1 line 24）。

MAP-Elites 风格存档保留每个测度单元中已发现的最佳解（Algorithm 1 lines 14-16）。

## 实验与关键发现

### 核心瓶颈与 DMS 的应对机制

CMA-MAE 在高维测度空间中遭遇的根本性失败源于其离散的折扣函数表示。CMA-MAE 将测度空间划分为单元，并在每个单元中存储一个标量折扣值 $f_A$。当测度空间维度升高时，**畸变效应（distortion）**被急剧放大：大量不同的解落入相同的存档单元，获得完全相同的折扣值（Figure 1a）。此时，改进信号 $\Delta(\boldsymbol{\theta}) = f(\boldsymbol{\theta}) - f_A(\boldsymbol{m}(\boldsymbol{\theta}))$ 失效——发射器无法区分解的优劣，搜索陷入停滞。

实验直接验证了这一失败模式。Figure 1c 展示了 CMA-MAE 在 2D LP (Sphere) 和 10D LP (Sphere) 中，每轮迭代采样解所落入的唯一存档单元数量。在 2D 空间中，唯一单元数从约 300 逐渐下降至约 100；而在 **10D 空间中，唯一单元数急剧崩溃至仅约 30**——尽管每轮迭代采样 540 个解，绝大多数解都挤入了极少数单元中，改进信号完全丧失。

DMS 通过将折扣函数从离散直方图替换为**由神经网络参数化的平滑折扣模型** $\hat{f}_A(\cdot; \psi)$，从根本上解决了这一问题。如 Figure 1b 所示，即使两个解的测度非常接近，平滑的折扣模型也能给出不同的折扣值，从而产生有区分度的改进排序信号（$\Delta_2 > \Delta_1$），有效引导搜索。

### 主实验结果

Table 1 汇总了所有算法在所有域中的 QD 分数和覆盖率。DMS 在绝大多数基准上显著优于所有基线方法，尤其是在高维测度空间中优势极为明显。


**线性投影（LP）域：**
- 在 2D LP (Sphere) 中，DMS 的 QD 分数达到 6,978.20，相比 CMA-MAE 的 6,327.90 提升 650.30；覆盖率从 80.95% 提升至 95.89%。
- **10D LP (Sphere) 中差距急剧扩大**：DMS 的 QD 分数为 6,409.50，而 CMA-MAE 仅为 608.53（提升约 5,800）；覆盖率从 6.95% 跃升至 89.21%。这直接印证了平滑折扣模型对高维畸变的克服能力。
- 在 10D LP (Rastrigin) 中，CMA-MAE 的 QD 分数仅为 246.55，覆盖率仅 2.98%；DMS 分别达到 5,138.81 和 88.19%，提升幅度同样超过一个数量级。
- MAP-Elites 系列算法在 10D 空间中表现更差（QD 分数 228.65），进一步说明离散存档在高维测度空间中的根本性局限。

**QDDM 域：**
- 在 TA (MNIST) 中，DMS 与 CMA-MAE 的 QD 分数几乎持平（951.56 vs 954.27），覆盖率略高（99.84% vs 99.48%）。折扣模型可能引入的噪声在此域中略微阻碍了精细目标优化。
- 在 TA (F-MNIST) 中，DMS 在两个指标上均显著优于所有基线。
- 在 **LSI (Hiker)** 中，DMS 的 QD 分数为 214.91，而 CMA-MAE 仅为 14.61，提升超过 200 点。Figure 2 展示了 DMS 在此域中为不同景观测度生成的登山者图像，验证了平滑折扣模型在语义测度空间中的探索引导能力。

**计算时间：** Table 2 显示，在基准域中 DMS 的挂钟时间明显长于 CMA-MAE（如 2D LP Sphere 中 397.83s vs 121.13s），主要来自折扣模型的训练开销。但在 QDDM 域中，由于解评估（如渲染或 StyleGAN 生成）占主导，时间差异大幅缩小（TA MNIST 中 489.90s vs 495.95s）。MAP-Elites 系列算法速度最快但性能最差。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_m6Hv0yZO3n/figures/006_Table_2.jpg]]
*Table 2: Computation (wallclock) time (in seconds) of each algorithm in each domain. We show the mean and standard error of the mean over 20 trials for the benchmark domains and 5 trials for the QDDM domains*

### 消融实验

**存档学习率 $\alpha$ 的影响（Figure 9）：**
$\alpha$ 控制目标优化与探索之间的平衡。当 $\alpha \to 0$ 时，折扣模型几乎不更新，DMS 退化为纯单目标优化，覆盖率极低。随着 $\alpha$ 增大，覆盖率和 QD 分数同步提升，在 $\alpha \approx 0.1$ 附近通常达到最优。这一行为与 CMA-MAE 中的阈值更新机制一致。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_m6Hv0yZO3n/figures/028_Figure_9.jpg]]
*Figure 9: Mean and standard error of the mean of QD Score and Coverage when varying the archive learning rate α in DMS in the benchmark domains. Highlighted lines indicate results from the main paper in Table 1. Mean over 20 trials*

**空点训练机制的关键作用（Figure 10, Figure 11）：**
空点（empty points）是 DMS 中一个看似微小但至关重要的设计。当 $n_{\text{empty}} = 0$（不添加空点）时，折扣模型在未探索区域会输出**任意高值**（Figure 11），导致发射器错误地认为整个测度空间已被充分探索，即使存档几乎为空。这使 QD 分数和覆盖率大幅崩溃。只需添加少量空点（$\ge 10$），折扣模型就能在未探索区域保持低值输出，性能即可恢复至正常水平。Figure 8 展示了正常训练中折扣模型从初始的 $f_{\text{min}}$ 全域低值，逐步在已探索区域升高、未探索区域维持低值的演变过程。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_m6Hv0yZO3n/figures/023_Figure_8.jpg]]
*Figure 8: Progression of the archive and discount model in DMS in the 2D LP (Sphere) benchmark. The left heatmap shows the archive, while the right heatmap shows the discount model. To plot the discount model, we computed its output at points in a 200 × 200 grid in measure space. The discount model heatmap also shows the dataset $\mathcal { D } _ { A }$ of points on a given iteration — blue circles indicates points created with solutions from the emitters, and yellow triangles indicate empty points. On Iteration 0, the discount model initializes to output $f _ { m i n }$ everywhere. On Iteration 250, as the emitters begin to populate the archive, the discount model begins to output higher values in areas...*

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_m6Hv0yZO3n/figures/038_Figure_11.jpg]]
*Figure 11: Similar to Fig. 8, this figure shows how the archive and discount model in DMS progress across iterations. However, this time, DMS does not train the discount model with any empty points, $\begin{array} { r } { \mathbf { i . e . , \ n _ { e m p t y } = 0 } } \end{array}$ . As a result, the discount model takes on arbitrary values in areas of the measure space that have not been explored yet, as evinced by the high values across the discount model heatmap on Iteration 250 and 10000. Because the discount values are high everywhere, the emitters in DMS mistakenly believe they have explored all areas of the measure space, even though the archive is essentially empty

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_m6Hv0yZO3n/figures/032_Figure_10.jpg]]
*Figure 10: Mean and standard error of the mean of QD Score and Coverage when varying the number of empty points n _ { e m p t y } in DMS in the benchmark domains. Highlighted lines indicate results from the main paper in Table 1. Mean over 20 trials*

**重启规则（Table 7）：**
重启规则的效果具有域依赖性。在低维测度空间（2D）和 Arm Repertoire 中，基于 CMA-ES 收敛的“基本”重启规则表现更好；而在高维测度空间（10D LP）中，固定每 100 次迭代重启的规则显著优于基本规则。

### 重要注意事项

- DDS 虽然在某些域中覆盖率较高（如 Arm Repertoire），但目标值低，因为其仅进行多样性优化而不优化目标。
- 在 TA (MNIST) 中 DMS 的目标分数略微落后于 CMA-MAE，提示折扣模型的平滑性可能引入噪声，在需要精细目标优化的场景中需进一步研究。
- 所有实验均统一了每轮迭代生成的解的数量，以保证公平比较。

*Figure 1: (a): One failure mode of CMA-MAE. On a flat objective f , solutions $\pmb { \theta } _ { 1 }$ and $\pmb { \theta } _ { 2 }$ fall in the same archive cell based on their measures, resulting in identical discount values from the discount function $f _ { A }$ . \ ( $\mathbf { b } ) { \mathrm { : } }$ : In our proposed DMS, the discount model provides a smooth discount function that assigns distinct discount values to $\pmb { \theta } _ { 1 }$ and $\pmb \theta _ { 2 }$ . , showing that $\pmb { \theta } _ { 2 }$ has greater archive improvement than $\theta _ { 1 }$ \ $\mathrm { \bar { ( } } \Delta _ { 2 }$ \ > $\Delta _ { 1 }$ ) and thus providing a stronger signal to guide search. (c): Number of unique cells where...

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_m6Hv0yZO3n/figures/025_Table_4.jpg]]
*Table 4: Pairwise comparisons (Games-Howell test) of the QD Score of each algorithm*

## 定位与知识库关联

### 瓶颈识别与核心洞察

本工作的真实瓶颈在于 **CMA-MAE**（Fontaine & Nikolaidis, 2023）在高维测度空间中的失效机制：其折扣函数以离散直方图表示，将测度空间划分为固定单元，每个单元存储一个标量折扣值。当测度空间维度升高时，畸变效应（distortion）被急剧放大——大量解落入相同单元并获得完全相同的折扣值，导致改进信号 $\Delta(\boldsymbol{\theta}) = f(\boldsymbol{\theta}) - f_A(\boldsymbol{m}(\boldsymbol{\theta}))$ 丧失区分度，搜索停滞。实验证据表明，在 10D LP (Sphere) 中，CMA-MAE 探索到的唯一存档单元数随迭代急剧下降至约 30 个，而其每轮采样 540 个解（Figure 1c）。

DMS 的核心因果旋钮是将折扣函数的表示从**离散单元直方图**转换为**平滑连续神经网络模型** $\hat{f}_A(\cdot; \psi)$。这一转换使测度相近的解能获得有区分度的折扣值，从而在高维、高畸变测度空间中维持有效的探索引导（Figure 1b）。

### 与基线方法的关系

**CMA-MAE**（Fontaine & Nikolaidis, 2023）是本工作的主要对比基线和直接前身。DMS 继承了 CMA-MAE 的核心架构——MAP-Elites 风格存档、CMA-ES 发射器、以及基于折扣函数的改进排序机制——但将其离散直方图折扣函数替换为平滑折扣模型。这一替换是决定性的：在 10D LP (Sphere) 中，DMS 的 QD 分数（6,409.50）是 CMA-MAE（608.53）的约 10.5 倍，覆盖率从 6.95% 跃升至 89.21%（Table 1）。

**DDS**（Lee et al., 2024）采用核密度估计替代折扣函数，专注于多样性优化。Table 1 显示 DDS 在 Arm Repertoire 中覆盖率显著优于 DMS，但其目标值普遍较低，因为该方法仅进行多样性优化而不显式优化目标函数。DMS 通过存档学习率 $\alpha$ 在目标优化与探索之间取得平衡，在绝大多数域中同时实现了更高的 QD 分数和覆盖率。

**MAP-Elites**（Mouret & Clune, 2015）及其变体 **MAP-Elites (line)**（Vassiliades & Mouret, 2018）作为经典 QD 基线，在高维测度空间中退化严重。在 10D LP (Sphere) 中，MAP-Elites 的 QD 分数仅为 228.65，覆盖率几乎为零（Table 1）。这些方法速度最快（Table 2），但缺乏有效的探索引导机制。

### 关键设计决策的消融证据

**空点训练机制**是 DMS 的必要组件。若取消耗折扣模型训练中的“空点”（$n_{empty}=0$），折扣模型会在未探索区域产生任意高值，使发射器误认为测度空间已被完全探索，导致 QD 分数和覆盖率大幅崩溃（Figure 11）。仅需添加少量空点（$\geq 10$）即可恢复高性能（Figure 10）。这一发现揭示了平滑折扣模型的一个潜在陷阱：神经网络的外推行为可能产生灾难性误信号。

**存档学习率 $\alpha$** 控制目标优化与探索的权衡。$\alpha \to 0$ 时 DMS 退化为纯单目标优化，覆盖率极低；$\alpha$ 在 0.1 附近通常性能最佳（Figure 9）。这一行为与 CMA-MAE 中 $\alpha$ 的作用一致。

**重启规则**具有域依赖性：低维测度空间（2D LP、Arm Repertoire）中基于 CMA-ES 收敛的基本重启规则表现更好；高维测度空间（10D LP）中固定每 100 次迭代重启显著优于基本规则（Table 7）。

### 适用边界与局限

1. **计算开销**：在基准域（LP、Arm Repertoire）中，DMS 因需训练折扣模型，挂钟时间明显长于 CMA-MAE（例如 2D LP Sphere 中 DMS 约 398 秒 vs CMA-MAE 约 121 秒，Table 2）。但在 QDDM 域（TA、LSI）中，由于评估开销占主导，差异较小。

2. **目标优化精度**：折扣模型可能引入噪声，在需要精细目标优化的域（如 TA (MNIST)）中，DMS 的 QD 分数（951.56）略微落后于 CMA-MAE（954.27），尽管覆盖率更高（99.84% vs 99.48%）。

3. **方法适用范围**：DMS 目前仅适用于黑盒 QD 设定，不能直接应用于可微 QD。开发适用于 QDDM 域（测度空间维度远超解空间维度）的高效可微 QD 方法仍是开放问题。

### 开放问题

- 能否用更轻量级的平滑模型（如核方法或高斯过程）替代神经网络，以减少训练开销并降低外推风险？
- 在没有手工测度函数的情况下，如何利用更多样化的模态（文本、音频等）来定义测度空间？
- 如何设计适用于 QDDM 域的可微 QD 方法，使梯度信息能同时优化目标函数和测度空间覆盖？

## 原文 PDF

![[paperPDFs/ICLR_2026/Discount_Model_Search_for_Quality_Diversity_Optimization_in_High_Dimensional_Measure_Spaces.pdf]]
