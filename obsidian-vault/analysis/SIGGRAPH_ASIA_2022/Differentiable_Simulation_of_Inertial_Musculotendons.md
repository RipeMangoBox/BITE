---
title: Differentiable Simulation of Inertial Musculotendons
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Differentiable_Simulation_of_Inertial_Musculotendons.pdf
project_link: null
code_link: null
aliases:
- IMS
- DSIM
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_physical_simulation
core_operator: 在肌骨腱路径上插入质量点，并将其运动通过雅可比链与骨骼降低坐标绑定，从而在动力学方程中显式包含肌肉惯性项。
primary_logic: 通过将肌肉路径分为三类（直线、折线、包裹表面），并分别利用几何推导、欧拉-拉格朗日（EOL）扩展和神经网络训练光滑雅可比，可以在减少坐标框架下高效地近似复杂肌肉路径的惯性效应，同时保持与传统仿真器兼容、可微并可混合使用。
claims:
- 肌肉惯性使跑步反动力学踝扭矩结果变化高达40%
- 包含肌肉惯性将手指仿真稳定性从5 N力失效提升至20 N
- 二次速度矢量（QVV）是防止能量振荡的必要条件
- 所提方法在无肌肉惯性时与OpenSim结果一致，可优雅退化
---

# Differentiable Simulation of Inertial Musculotendons

> [!tip] 核心洞察
> 通过将肌肉路径分为三类（直线、折线、包裹表面），并分别利用几何推导、欧拉-拉格朗日（EOL）扩展和神经网络训练光滑雅可比，可以在减少坐标框架下高效地近似复杂肌肉路径的惯性效应，同时保持与传统仿真器兼容、可微并可混合使用。

| 字段 | 内容 |
|------|------|
| 中文题名 | 惯性肌骨腱的可微仿真 |
| 英文题名 | Differentiable Simulation of Inertial Musculotendons |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2202.02344) |
| Topic | #topic/graphics_physical_simulation |
| Method | Inertial Musculotendon Simulation |
| Dataset | 与Pai 2010分析结果验证 |

> [!tip] 效果简介
> - 跑步逆动力学（踝关节扭矩） 上，踝关节扭矩变化 惯性引起最大约40%的差异 vs OpenSim（无惯性） (~40%)。
> - 手指点击仿真稳定性 上，不稳定时施加的力阈值 20 N vs 5 N（传统方法） (+15 N)。
> - 与Pai 2010分析结果验证 上，角度归零时间 0.3秒（匹配） vs 0.3秒（分析结果） (0)。

## 概要

传统肌骨仿真器（如 **OpenSim**，Seth et al. 2018）将肌肉质量集中到附着骨骼上，完全忽略肌肉相对于骨骼滑动时产生的惯性效应。这导致两个关键问题：一是在跑步等动态任务中，逆动力学计算的踝关节扭矩偏差可达 **40%**；二是在低惯性关节（如手指）的冲击仿真中，系统极易失稳——传统方法在 5 N 外力下即崩溃，而包含肌肉惯性后可承受 20 N。

本文提出一种**惯性肌骨腱的可微仿真框架**，核心思路是沿肌骨腱路径（中心线）离散化质量点，并通过雅可比链 $J_{\alpha r} = J_{\alpha m} J_{m r}$ 将骨骼降低坐标的运动映射到这些质量点的世界加速度，从而在系统动力学方程中显式包含肌肉惯性项。针对三类肌肉路径——直线（Type I）、折线（Type II）、包裹表面（Type III）——分别采用几何推导、扩展欧拉-拉格朗日公式和神经网络学习光滑雅可比，解决了传统包裹表面库中雅可比跳变导致的能量不连续问题。推导并保留了**二次速度矢量（QVV）项** $\dot{J}_{\alpha m}$，这是维持系统能量守恒的必要条件：消融实验表明，去除 QVV 后总能量剧烈振荡。

实验验证覆盖多个层面：与 **Pai 2010** 分析解一致；跑步逆动力学踝扭矩差异达 40%；手指仿真稳定性阈值从 5 N 提升至 20 N；包裹表面仿真能量保持稳定；当肌肉质量归零时，结果优雅退化至与 OpenSim 一致。框架支持 Hill 型肌肉模型、复杂关节（如样条关节膝关节）和高阶积分器，且与伴随方法无缝兼容，使可微仿真优化速度较无梯度模式提升一个数量级。

**定位**：该方法改变了传统肌骨仿真中“肌肉惯性表示”这一核心槽位，将原本归入骨骼的肌肉质量显式建模为沿路径分布的质量点及其雅可比映射，同时通过神经网络光滑化解决了包裹表面路径的雅可比不连续问题。

## 核心方法与创新机理

### 问题瓶颈与核心思想

传统肌骨仿真器（如 OpenSim，Seth et al. 2018）在构建动力学方程时，将肌肉的质量集中到其附着的骨骼刚体上，完全忽略了肌肉相对于骨骼滑动时产生的惯性效应。这一简化导致两个关键问题：其一，在跑步等高动态运动中，踝关节的反动力学扭矩计算误差可达40%（Fig. 10）；其二，对于手指等低惯性关节，仿真在极小外力（如5 N）下即出现数值不稳定（§4.4）。

本文的核心洞察是：若将肌肉质量沿其路径离散化为一系列质量点，并通过雅可比链将这些质量点的运动与骨骼的降低坐标（reduced coordinates）绑定，则可以在不改变传统降低坐标仿真框架的前提下，显式地将肌肉惯性项纳入系统动力学方程。这一设计使得方法能够与传统仿真器兼容、可优雅退化（肌肉质量归零时退化为 OpenSim 结果），且天然支持可微性。

### 系统总成：从骨骼到肌肉的雅可比链

整个框架建立在降低坐标描述的多刚体骨骼动力学之上。令 $\dot{\mathbf{q}}_r$ 为骨骼系统的降低关节速度，则任意刚体上的最大速度（maximal velocity）$\dot{\mathbf{q}}_m$ 通过雅可比 $\mathbf{J}_{mr}$ 获得：

$$\dot{\mathbf{q}}_m = \mathbf{J}_{mr} \dot{\mathbf{q}}_r \quad \text{(Eq. 2)}$$

肌肉质量点 $\alpha$ 的世界速度 $\dot{\mathbf{x}}_\alpha$ 则需要进一步通过肌肉路径的运动学映射。定义 $\mathbf{J}_{\alpha m}$ 为从最大速度到肌肉质量点世界速度的雅可比，则最终雅可比链为：

$$\mathbf{J}_{\alpha r} = \mathbf{J}_{\alpha m} \mathbf{J}_{mr} \quad \text{(Eq. 4)}$$

$$\dot{\mathbf{x}}_\alpha = \mathbf{J}_{\alpha r} \dot{\mathbf{q}}_r \quad \text{(Eq. 1)}$$

肌肉质量点的加速度包含科里奥利项和直接加速度项：

$$\ddot{\mathbf{x}}_\alpha = \dot{\mathbf{J}}_{\alpha r} \dot{\mathbf{q}}_r + \mathbf{J}_{\alpha r} \ddot{\mathbf{q}}_r, \quad \dot{\mathbf{J}}_{\alpha r} = \dot{\mathbf{J}}_{\alpha m} \mathbf{J}_{mr} + \mathbf{J}_{\alpha m} \dot{\mathbf{J}}_{mr} \quad \text{(Eq. 5)}$$

通过虚功原理，将肌肉质量点 $\alpha$ 的惯性力投射到降低坐标空间，得到广义肌肉惯性力：

$$\mathbf{J}_{\alpha r}^\top \mathbf{M}_\alpha \mathbf{J}_{\alpha r} \ddot{\mathbf{q}}_r = \mathbf{J}_{\alpha r}^\top \left( \mathbf{f}_\alpha - \mathbf{M}_\alpha \dot{\mathbf{J}}_{\alpha r} \dot{\mathbf{q}}_r \right) \quad \text{(Eq. 6)}$$

将所有肌肉质量点的贡献与骨骼的惯性矩阵和力矢量组合，得到总系统的运动方程：

$$\tilde{\mathbf{M}}_r \ddot{\mathbf{q}}_r = \tilde{\mathbf{f}}_r \quad \text{(Eq. 7a)}$$

其中 $\tilde{\mathbf{M}}_r$ 和 $\tilde{\mathbf{f}}_r$ 分别包含了骨骼和所有肌肉的惯性及力贡献。这一组装过程是模块化的：骨骼动力学模块提供 $\mathbf{J}_{mr}$ 和 $\dot{\mathbf{J}}_{mr}$，肌肉路径运动学模块提供 $\mathbf{J}_{\alpha m}$ 和 $\dot{\mathbf{J}}_{\alpha m}$，二者通过 Eq. 4-5 组合后注入 Eq. 6-7。

### 三个 Changed Slots：肌肉惯性表示、路径雅可比计算、二次速度矢量

#### Changed Slot 1：肌肉惯性表示——从归入骨骼到独立质量点

**Baseline**：传统方法将肌肉质量集中到附着骨骼上，系统动力学方程中不存在独立的肌肉惯性项。

**Proposed**：沿肌骨腱路径按固定百分比长度 $\alpha$ 插入离散质量点（Fig. 3b），每个质量点具有独立的质量 $\mathbf{M}_\alpha$，其运动通过 $\mathbf{J}_{\alpha r}$ 与骨骼降低坐标绑定。这一改变使得肌肉在相对于骨骼滑动时产生的惯性力被显式建模，且质量点数量可按精度需求调节。

#### Changed Slot 2：包裹表面路径的雅可比计算——从库函数跳变到神经网络光滑映射

**Baseline**：现有包裹表面库（如 OpenSim 使用的库）在计算肌肉路径与包裹表面的接触点时，其雅可比存在不连续性（Fig. 4d-e 实线），导致仿真能量出现跳变（Fig. 4b）。

**Proposed**：训练一个全连接神经网络来拟合从起止点坐标和路径参数到表面坐标的映射：

$$(^S\mathbf{x}_{\text{ori}}, ^S\mathbf{x}_{\text{ins}}, \alpha, r) \rightarrow (^S\mathbf{x}_\alpha) \quad \text{(§3.3.1)}$$

网络训练完成后，解析计算其输出对输入的导数，得到光滑的雅可比：

$$^S\mathbf{J}_{\alpha 0}^{\text{NN}} = \frac{d ^S\mathbf{x}_\alpha}{d ^S\mathbf{x}_{\text{ori}}}, \quad ^S\mathbf{J}_{\alpha i}^{\text{NN}} = \frac{d ^S\mathbf{x}_\alpha}{d ^S\mathbf{x}_{\text{ins}}} \quad \text{(§3.3.2)}$$

这些雅可比随后通过几何变换链（基座运动、起止点运动）组合为世界坐标系下的 $\mathbf{J}_{\alpha m}$。关键创新在于：神经网络的输出在位置层面与库函数几乎无法区分，但其导数却天然光滑，从而消除了能量不连续性（Fig. 4c, 4e 虚线）。

#### Changed Slot 3：二次速度矢量（QVV）项——从缺失到显式推导

**Baseline**：传统方法不考虑肌肉质量的二次速度矢量项 $\dot{\mathbf{J}}_{\alpha r} \dot{\mathbf{q}}_r$。

**Proposed**：本文显式推导并包含了 $\dot{\mathbf{J}}_{\alpha m}$ 和 $\dot{\mathbf{J}}_{mr}$ 的完整表达式（Eq. 5），从而在系统动力学中保留了科里奥利力和离心力项。消融实验（Fig. 8）表明，移除 QVV 项会导致总能量剧烈振荡，证明其对保持系统保守性的必要性。

### 三类肌肉路径的运动学模块

根据肌肉路径的几何复杂度，本文将其分为三类（Fig. 2），并分别设计了 $\mathbf{J}_{\alpha m}$ 和 $\dot{\mathbf{J}}_{\alpha m}$ 的计算模块：

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2202_02344/figures/002_Figure_2.jpg]]
*Figure 2: Concrete running example for Types I, II, and III muscles. In all cases, there are three bones and one muscle. The origin is on body ??, and the insertion is on body ??. Type II muscle has a path point on body ??, and Type III muscle has a wrapping surface ?? defined with respect to body ??*

**类型 I（直线路径）**：肌肉起止点直接连接，无中间路径点。质量点 $\alpha$ 的位置由起止点线性插值得到，其世界速度由起止点的世界速度组合而成。$\mathbf{J}_{\alpha m}$ 通过起止点所在刚体的材料雅可比 $\Gamma$ 和旋转矩阵解析推导（Eq. 8-10）。

**类型 II（折线路径 / EOL 扩展）**：肌肉包含一个或多个中间路径点，附着于特定骨骼上。本文扩展了欧拉-拉格朗日（EOL）strands 框架（Sueda et al. 2011），将其从不可伸长杆推广到可伸长的肌骨腱。核心在于推导组合坐标 $z_i$ 的雅可比 $\mathbf{J}_{sx}$ 及其时间导数 $\dot{\mathbf{J}}_{sx}$（Eq. 11-18），以处理路径点在欧拉坐标（沿路径的弧长参数）和拉格朗日坐标（世界空间）之间的映射。

**类型 III（包裹表面路径 / 神经网络）**：肌肉路径部分包裹在骨骼表面（如圆柱或椭球）上。如 Changed Slot 2 所述，使用神经网络学习表面坐标映射并解析求导，得到光滑的 $\mathbf{J}_{\alpha m}$。世界速度被分解为基座运动、起点运动和止点运动三部分贡献（Eq. 20），每部分通过相应的几何雅可比链计算。

### 模块间的因果关系与数据流

整个方法的模块执行顺序和因果关系如下：

1. **骨骼动力学模块**接收当前状态 $\mathbf{q}_r, \dot{\mathbf{q}}_r$，计算 $\mathbf{J}_{mr}$ 和 $\dot{\mathbf{J}}_{mr}$，并输出骨骼自身的惯性矩阵和广义力。

2. **肌肉路径分类器**根据每块肌肉的几何定义，将其分配到类型 I、II 或 III 子模块。

3. **类型 I/II/III 子模块**分别计算各肌肉质量点的 $\mathbf{J}_{\alpha m}$ 和 $\dot{\mathbf{J}}_{\alpha m}$。类型 III 子模块内部调用预训练的神经网络进行前向推理并解析计算雅可比。

4. **雅可比链组合**（Eq. 4-5）将骨骼雅可比与肌肉雅可比相乘，得到最终的 $\mathbf{J}_{\alpha r}$ 和 $\dot{\mathbf{J}}_{\alpha r}$。

5. **系统组装器**（Eq. 6-7）将所有肌肉质量点的惯性贡献累加到总质量矩阵 $\tilde{\mathbf{M}}_r$ 和总力矢量 $\tilde{\mathbf{f}}_r$ 中，形成最终的降低坐标运动方程。

6. **时间积分器**（支持前向欧拉、BDF1、SDIRK2）推进系统状态。可微性通过伴随方法（adjoint method）在整个仿真轨迹上反向传播梯度（§4.7），支持优化任务。

### 关键公式变量含义速查

| 符号 | 含义 |
|------|------|
| $\mathbf{q}_r$ | 骨骼系统的降低坐标（关节角度等） |
| $\mathbf{q}_m$ | 最大坐标（各刚体的6-DOF位姿） |
| $\mathbf{J}_{mr}$ | 从降低速度到最大速度的骨骼雅可比 |
| $\mathbf{x}_\alpha$ | 肌肉质量点 $\alpha$ 的世界坐标 |
| $\mathbf{J}_{\alpha m}$ | 从最大速度到肌肉质量点速度的肌肉路径雅可比 |
| $\mathbf{J}_{\alpha r}$ | 从降低速度到肌肉质量点速度的最终雅可比（$\mathbf{J}_{\alpha m} \mathbf{J}_{mr}$） |
| $\mathbf{M}_\alpha$ | 肌肉质量点 $\alpha$ 的质量矩阵 |
| $\tilde{\mathbf{M}}_r, \tilde{\mathbf{f}}_r$ | 包含骨骼和肌肉惯性贡献的总质量矩阵和总力矢量 |
| $\dot{\mathbf{J}}_{\alpha r} \dot{\mathbf{q}}_r$ | 二次速度矢量（QVV），科里奥利和离心力项 |

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2202_02344/figures/001_Figure_1.jpg]]
*Figure 1: Muscle inertia (a) changes the inverse dynamics result of running motion by up to 40%, and (b) stabilizes the simulation. Our framework (c) handles Hill-type muscles, complex joints, and higher-order integration, and (d) works flawlessly with the adjoint method for computing the simulation derivatives*

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2202_02344/figures/008_Figure_6.jpg]]
*Figure 6: Comparison to published results [Pai 2010]. (a) Two bones and one muscle, all with the same mass. (b) The solid lines show that after simulating the system with the muscle for 0.3 seconds, the two angles straighten out as in the previous work. The dotted lines show the same simulation but with the mass of the muscle lumped onto the bones*

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2202_02344/figures/010_Figure_8.jpg]]
*Figure 8: (a-b) Energy plots from a Type II muscle with and without QVV. (c-d) Energy plots from a Type III muscle with and without QVV. Kinetic energy is shown in blue, potential energy in red, and total energy in yellow*

## 实验与关键发现

### 主结果概览

本方法在跑步逆动力学、手指仿真稳定性、能量守恒、解析验证和可微优化五个维度上验证了肌肉惯性建模的必要性与有效性。核心发现是：**肌肉惯性可使跑步踝关节扭矩反动力学结果变化高达约40%**，且**将手指仿真的稳定性阈值从传统方法的5 N提升至20 N**。当肌肉质量归零时，方法优雅退化为OpenSim结果，验证了框架的兼容性。

### 跑步逆动力学：踝关节扭矩的惯性效应

在19.1 km/h跑步摆动相（Fig. 9）中，选取四条肌肉（腓肠肌外侧/内侧、比目鱼肌、胫骨前肌）进行逆动力学分析。Fig. 10展示了踝关节扭矩的对比：

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2202_02344/figures/011_Figure_9.jpg]]
*Figure 9: The swing phase of a 19.1 km/h treadmill run, showing only the right leg. The four muscles (and their types) are: gastrocnemius lateral (Type III), gastrocnemius medial (Type III), soleus (Type I), and tibialis anterior (Type II)*

- **OpenSim基线**（蓝色曲线）：传统方法，肌肉质量归入骨骼，无独立惯性项。
- **本文方法，肌肉质量占比0%**（红色曲线）：与OpenSim结果高度一致，验证了框架在无惯性时能优雅退化至传统仿真器水平。
- **本文方法，肌肉质量占比80%**（黄色曲线）：将胫骨段质量的80%转移至肌肉后，踝关节扭矩出现显著偏离，**最大偏差约40%**，尤其在摆动末期扭矩谷值处差异最为明显。

这一结果揭示了关键因果链：传统肌骨仿真器将肌肉质量集中到骨骼上，忽略了肌肉相对于骨骼滑动时产生的附加惯性力。当肌肉质量不可忽略（如小腿肌群）且运动加速度较大时，这种简化导致反动力学推算的关节扭矩产生系统性误差。消融实验进一步表明，随着肌肉质量占比从0%逐步增加到80%，踝关节扭矩单调偏离OpenSim基线，排除了其他混杂因素的干扰。

### 手指点击仿真：低惯性关节的稳定性提升

手指关节属于低惯性系统，传统方法在冲击载荷下极易失稳。实验表明：

- **传统方法**（无肌肉惯性）：在施加5 N外力时仿真即发散失稳。
- **本文方法**（包含肌肉惯性）：可稳定仿真至20 N外力，稳定性阈值提升约4倍。

这一改进的机理在于：肌肉质量点沿肌骨腱路径分布后，系统质量矩阵的条件数得到改善，惯性项对高频冲击起到了阻尼缓冲作用。对于手指这类骨骼质量小、肌肉质量占比相对较高的关节，忽略肌肉惯性会严重低估系统的有效惯量，导致数值积分在接触冲击时发散。

### 能量守恒与二次速度矢量（QVV）消融

能量守恒是验证物理仿真正确性的核心指标。针对Type II（折线路径）和Type III（包裹表面路径）肌肉，进行了包含与不包含QVV项的消融实验（Fig. 8）：

- **不含QVV**：总能量（黄色曲线）出现剧烈振荡，动能（蓝色）与势能（红色）之间存在虚假的能量交换，表明系统不再保守。
- **包含QVV**：总能量保持平稳，动能与势能的转换符合保守系统预期。

这一消融直接验证了QVV项（即$\dot{\mathrm{J}}_{\alpha r} \dot{\mathrm{q}}_r$的广义力贡献）是保持动能守恒的必要条件。在推导肌肉惯性力时（Eq. 5–6），加速度包含$\dot{\mathrm{J}}_{\alpha r} \dot{\mathrm{q}}_r$的科里奥利项和$\mathrm{J}_{\alpha r} \ddot{\mathrm{q}}_r$的直接加速度项。若忽略前者，虚功原理投射到降低坐标空间时将丢失与速度相关的惯性力分量，导致能量不守恒。该结论对Type II和Type III肌肉均成立，说明QVV的必要性与路径类型无关。

### 与解析结果的验证

为验证框架的基础正确性，复现了Pai 2010的解析验证场景（Fig. 6）：两骨骼一肌肉，三者质量相等。仿真0.3秒后，两关节角度归零（伸直），**与已发表解析结果完全匹配**。而将肌肉质量归入骨骼的传统方法（虚线）则偏离解析解，进一步证实了肌肉独立惯性项的必要性。

### 包裹表面路径的雅可比光滑性

现有包裹表面库（如OpenSim使用的算法）存在雅可比跳变问题，导致能量不连续（Fig. 4b）。本文使用神经网络学习路径点映射，并解析推导光滑雅可比（§3.3.2），实现了：

- **位置轨迹**：与现有库几乎不可区分（Fig. 4d），验证了网络拟合精度。
- **雅可比**：本文方法（虚线）光滑连续，现有库（实线）存在明显跳变（Fig. 4e）。
- **能量**：本文方法总能量稳定（Fig. 4c），现有库出现虚假能量波动（Fig. 4b）。

这一对比揭示了关键设计选择：神经网络不仅作为函数逼近器，更重要的是其自动微分能力天然产生光滑导数，绕过了传统几何算法中分段处理导致的一阶不连续性。

### 可微仿真与优化效率

在到达任务（reaching）优化中，使用伴随方法计算仿真导数，优化所需仿真次数/时间比无梯度模式**快一个数量级**（§4.7）。这验证了框架的全链路可微性——从肌肉路径雅可比到系统动力学再到伴随反向传播，梯度流动无断裂。

### 适用边界与局限

1. **中心线近似**：当前将肌肉质量沿中心线分布，未使用体积有限元模型，可能低估肌肉体积效应带来的转动惯量。
2. **应变均匀假设**：对于长肌腱肌肉（如部分下肢肌），假设整个肌骨腱应变相等，当肌腱刚度远高于肌腹时会导致惯性被低估。
3. **网络泛化**：包裹表面神经网络的训练依赖于特定几何参数范围，对极端关节角度或非常规表面形状的泛化能力需进一步验证。
4. **计算性能**：当前MATLAB实现存在性能瓶颈，尚未在GPU上批量评估网络，限制了大规模肌骨模型的实时应用。

这些边界条件表明，方法在肌肉质量占比高、加速度大的场景（如冲刺跑、冲击着陆）中价值最大；对于准静态运动或肌肉质量可忽略的关节，传统方法仍可满足精度需求。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2202_02344/figures/009_Figure_7.jpg]]
*Figure 7: Double pendulums with cylinder wrapping. The same trained network is used for a range of input parameters. For comparison, the right-most double pendulum is simulated without a muscle*

## 定位与知识库关联

**核心定位：在传统肌骨仿真器的动力学方程中插入肌肉惯性项**

传统肌骨仿真器（如 **OpenSim**，Seth et al., 2018）将肌肉质量集中到附着骨骼上，系统动力学方程中不存在独立的肌肉惯性项。本文改变的关键 **slot** 是：将“肌肉质量归入骨骼刚体”替换为“沿肌骨腱路径离散化质量点，并通过雅可比链将骨骼降低坐标运动映射到这些点的世界加速度，显式添加到系统动力学方程中”。这一改变的本质是为肌骨仿真引入了一个新的物理维度——肌肉相对于骨骼滑动时的惯性效应，而不改变骨骼动力学的基本框架。

**与知识库的挂载点**

1. **EOL strands 框架的扩展**：本文的 Type II 肌肉路径处理直接继承并扩展了 Eulerian-on-Lagrangian strands 框架（Sueda et al., 2011; Sachdeva et al., 2015）。原框架用于不可伸长的头发/绳索仿真，本文将其扩展至可伸长的肌骨腱，并推导了 $\dot{\mathrm{J}}_{sx}$ 的时间导数（Eq. 11–18），这是原框架中未提供的项。这个扩展使得 EOL 框架首次能够处理具有可变长度的生物力学路径，同时保持动能守恒所需的二次速度矢量（QVV）项。

2. **包裹表面问题的雅可比光滑化**：现有包裹表面库（如 OpenSim 使用的算法）存在雅可比跳变问题，导致仿真能量不连续。本文的解决方案是用神经网络学习从起止点坐标到表面路径点的映射，并解析计算雅可比（Eq. 20–28），从而获得光滑的导数。这本质上是用数据驱动逼近替代了分段解析几何计算，但保留了物理上必需的解析可微性。该方案可挂载到任何使用包裹表面的肌骨仿真器中。

3. **降低坐标动力学框架的兼容性**：本文方法完全在降低坐标（reduced coordinates）框架内运作，通过 $\mathrm{J}_{\alpha r} = \mathrm{J}_{\alpha m} \mathrm{J}_{m r}$ 的雅可比链将肌肉惯性投射到关节空间（Eq. 4–7）。这使得该方法可以直接与现有的基于降低坐标的刚体动力学引擎（如 OpenSim、MuJoCo 等）混合使用——当肌肉质量设为零时，系统优雅退化到传统结果（Fig. 10 红色与蓝色曲线重合），无需修改仿真器核心。

**相对已有方法的本质差异**

与 **Pai (2010)** 的分析性肌肉惯性模型相比，本文方法不限于简单的二骨一肌系统，而是扩展到任意多体骨骼、三类肌肉路径（直线/折线/包裹表面）、Hill 型肌肉模型和复杂关节类型（如样条关节膝关节，Fig. 11）。Pai 2010 提供了一个解析验证点（Fig. 6，角度归零时间 0.3 秒匹配），但本文的贡献在于将该概念工程化到通用仿真框架中。

与传统肌骨仿真器的“零惯性”假设相比，本文揭示了肌肉惯性在特定场景下的定量重要性：跑步逆动力学中踝关节扭矩差异可达 40%（Fig. 10），低惯性关节（如手指）的仿真稳定性阈值从 5 N 提升至 20 N（§4.4）。这些发现表明，对于高加速度运动（如冲击、跑步摆动相）和低质量肢体（如手指），忽略肌肉惯性会导致系统性偏差。

**适用边界与限制**

1. **质量分布假设**：采用中心线离散化近似肌肉质量分布，未使用体积有限元模型。这意味着对于横截面积变化剧烈或肌肉-骨骼接触力显著的场景，惯性效应可能被低估。需要手动验证：该假设在肌肉形状规则、体积效应次要时是否足够。

2. **应变均匀假设**：对于长肌腱的肌肉（如小腿三头肌），假设整个肌骨腱路径上的应变相等。当肌腱刚度远高于肌肉腹部时，该假设导致肌腱部分的惯性被低估——因为实际应变集中在肌肉腹部，而肌腱几乎不变形，但质量分布假设将质量均匀分配到整条路径上。

3. **神经网络的泛化依赖**：包裹表面肌肉的雅可比计算依赖于针对特定表面几何训练的神经网络。Fig. 7 展示了同一网络在参数范围内的泛化能力，但论文未系统评估跨不同表面形状（如从圆柱到椭球）的迁移性能。这在实际部署中需要针对新几何重新训练或验证。

4. **计算性能瓶颈**：当前实现基于 MATLAB，未在 GPU 上批量评估网络。对于包含大量包裹表面肌肉的全尺寸人体模型，实时性能可能不足。论文未提供与 OpenSim 在完整步态仿真中的计算时间对比。

**后续工作启发**

1. **体积肌肉模型的惯性项**：将中心线近似升级为基于有限元的体积肌肉模型，可以更准确地捕获肌肉收缩时的惯性变化，特别是对于宽大肌肉（如臀大肌）的横向惯性效应。

2. **与可微仿真生态的集成**：本文已证明伴随方法可高效计算仿真导数（§4.7），这为将肌肉惯性纳入基于梯度的运动优化、控制器学习和参数估计打开了通道。后续工作可将该方法集成到现有的可微物理引擎中。

3. **肌肉惯性对运动控制的影响**：40% 的踝关节扭矩差异暗示，中枢神经系统可能已经内化了肌肉惯性模型来进行运动规划。该仿真工具可用于验证运动控制假说，例如肌肉惯性是否解释了肌电信号与关节力矩之间的相位超前现象。

4. **混合仿真策略**：由于肌肉惯性效应在高加速度/低质量场景下显著，而在准静态运动中可忽略，后续工作可以开发自适应切换策略——在需要时激活惯性项，在不需要时退化为传统模型以节省计算。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Differentiable_Simulation_of_Inertial_Musculotendons.pdf]]