---
title: "Trading Spaces: Adaptive Subspace Time Integration for Contacting Elastodynamics"
type: paper
paper_level: A
venue: TOG
year: 2024
pdf_ref: paperPDFs/TOG_2024/Trading_Spaces_Adaptive_Subspace_Time_Integration_for_Contacting_Elastodynamics.pdf
project_link: https://www.dgp.toronto.edu/projects/trading-spaces/
aliases:
- ASTI
- TSASTICE
tags:
- TOG_2024
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "用户可调的节点误差阈值 ε_G^e 与模态误差阈值 ε_G^s，直接控制自适应oracle激活节点丰富化和模态丰富化的敏感度，从而在精度与计算成本之间提供连续调节杠杆。"
primary_logic: "将全自由度坐标作为最终状态存储，仅在时间步求解过程中将自适应更新的子空间模态与局部节点丰富化作为加速计算“临时便签”，利用无量纲的梯度误差与能量进度度量在线识别子空间失效区域，同时采用非重叠域分解保证求解稳定性，从而在维持 IPC 无条件不穿透、无反转等关键性质下，实现输出复杂度与动态复杂度（而非网格规模或材料刚度）成比例的高效仿真。"
claims:
- "自适应oracle同时考虑接触与变形力的耦合物理，而非仅依赖几何接触接近度。"
- "自定义线性求解器相比 MKL Pardiso 快 6–40 倍，相比带块 Jacobi 预条件的 Eigen CG 快高达 70 倍。"
- "在输出视觉质量与全空间 IPC 等价的条件下，自适应子空间仿真实现超过一个数量级的端到端加速。"
- "随着误差阈值收紧，自适应子空间求解器单调收敛至全空间 IPC 解，验证了方法的可控性与一致性。"
---

# Trading Spaces: Adaptive Subspace Time Integration for Contacting Elastodynamics

> [!tip] 核心洞察
> 将全自由度坐标作为最终状态存储，仅在时间步求解过程中将自适应更新的子空间模态与局部节点丰富化作为加速计算“临时便签”，利用无量纲的梯度误差与能量进度度量在线识别子空间失效区域，同时采用非重叠域分解保证求解稳定性，从而在维持 IPC 无条件不穿透、无反转等关键性质下，实现输出复杂度与动态复杂度（而非网格规模或材料刚度）成比例的高效仿真。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 空间交换：面向接触弹性动力学的自适应子空间时间积分 |
| 英文题名 | Trading Spaces: Adaptive Subspace Time Integration for Contacting Elastodynamics |
| 会议/期刊 | TOG 2024 |
| Links | [paper](https://dl.acm.org/doi/10.1145/3687946); [Project](https://www.dgp.toronto.edu/projects/trading-spaces/) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Adaptive Subspace Time Integration |
| Dataset | Multiple scenes (Armadillo, Boot, etc., Table 1), Linear solver comparison (Table 3), Rubber hand on spikes (Young's modulus sweep, Fig. 16) |

> [!tip] 效果简介
> - Multiple scenes (Armadillo, Boot, etc., Table 1) 上，Time-step solve speedup vs. full-space IPC (Pardiso LLT) 为 0.5–2 minutes (example)，对比 5–30 minutes，变化 6–40x faster。
> - Linear solver comparison (Table 3) 上，Linear system solve time 为 0.04–1.30 s，对比 0.25–21.4 s (IPC Pardiso LLT) / 2.10–36.5 s (IPC CG)，变化 up to 70x vs. CG, ~10x vs. LLT。
> - Rubber hand on spikes (Young's modulus sweep, Fig. 16) 上，Linear solve iterations (robustness under stiffness) 为 Iterations remain practical (~hundreds) up to E=1e9 Pa，对比 IPC-CG capped at 10,000 iterations at E>=1e8 Pa，变化 Our solver avoids explosion and stays well below cap。

## 概述

全空间增量势接触（IPC）仿真能够为弹性动力学提供无穿透、无反转的物理保障，但其计算成本随网格规模与接触复杂度急剧增长。子空间仿真通过降维加速求解，却面临一个根本瓶颈：**无法在时间步求解之前未知全空间解的情况下，在线评估子空间基对当前形变（尤其由接触、摩擦和材料异质性导致的局部形变）的表达充分性**，导致子空间仿真要么质量不足，要么需回溯全空间计算而失去加速意义。

针对这一瓶颈，本文提出**自适应子空间时间积分方法**（Adaptive Subspace Time Integration）。其核心洞察在于：将全自由度坐标作为最终状态的唯一存储，仅在时间步求解过程中将自适应更新的子空间模态与局部节点丰富化作为加速计算的“临时便签”；同时，利用无量纲的梯度误差与能量进度度量在线识别子空间失效区域，并采用非重叠域分解保证求解稳定性。这一设计使得输出复杂度与动态复杂度（而非网格规模或材料刚度）成比例，同时完整保留了 IPC 的无条件不穿透、无反转等关键性质。

方法的自适应oracle同时考虑接触与变形力的耦合物理，而非仅依赖几何接触接近度，从而能够精准识别因接触、摩擦或材料异质性引起的局部形变不足。用户可通过两个可调阈值——节点误差阈值 $\varepsilon_G^e$ 与模态误差阈值 $\varepsilon_G^s$——连续调节精度与计算成本之间的平衡。实验表明，随着误差阈值收紧，自适应子空间求解器单调收敛至全空间 IPC 解，验证了方法的可控性与一致性。

在性能方面，自定义的舒尔补线性求解器相比 MKL Pardiso 快 6–40 倍，相比带块 Jacobi 预条件的 Eigen CG 快高达 70 倍。在输出视觉质量与全空间 IPC 等价的条件下，自适应子空间仿真实现了超过一个数量级的端到端加速。该方法在 Mushroom Madness 等大规模复杂场景（250 万四面体）中成功捕获了橡胶靴踩踏蘑菇王国时的精细局部形变与异构材料交互，充分展示了其在实际应用中的有效性。

## 背景与动机

### 弹性体仿真的计算困境

高分辨率弹性体仿真在视觉特效、虚拟现实和机器人仿真中需求广泛，但全自由度（full-space）求解面临严重的计算瓶颈。以增量势能接触（Incremental Potential Contact, IPC）方法（Li et al., ACM Trans. Graph. 2020）为代表的现代弹性体仿真框架，通过优化形式的时间步求解保证了无条件不穿透和无反转等关键物理性质，然而其计算成本随网格规模急剧增长——典型场景中单个时间步的求解需耗时5至30分钟，严重制约了交互式应用和大规模场景的可行性。

### 子空间方法的潜力与局限

子空间仿真通过将形变约束在一组预计算模态的线性组合内，显著降低有效自由度（DOF），从而大幅加速求解。然而，现有子空间方法面临一个根本性困境：**无法在仿真步求解之前、未知全空间解的情况下，在线评估子空间基对当前形变的表达充分性**。这一困境在涉及接触、摩擦和材料异质性的场景中尤为突出——这些物理过程引发的局部形变（如尖锐接触点的压痕、异构材料界面的应力集中）恰恰是全局子空间模态最难以捕捉的。如图2所示，可用的子空间模型通常能够很好地表示大尺度全局形变，但无法解析局部细节；而一旦子空间表达不足，要么导致仿真质量下降，要么需要回溯全空间计算，从而失去加速意义。

### 现有自适应策略的不足

针对上述问题，已有方法尝试通过自适应策略扩展子空间表达能力，但其oracle设计存在根本性缺陷：大多数方法仅依赖几何接触接近度（geometric contact proximity）来决定丰富化区域，而**忽略了接触力与变形力之间的耦合物理**。这种纯几何的判定方式无法区分“需要丰富化的真实物理变形”与“可由现有子空间充分表示的刚性运动”，导致丰富化资源的大量浪费或关键区域的遗漏。此外，部分方法（如Stencil Descent, Lan et al. 2023）尝试采用坐标下降策略进行局部更新，但其收敛速度在网格细化下显著恶化（图3），无法满足高分辨率仿真的精度需求。

### 本文动机与核心思路

本文的核心洞察在于：**将全自由度坐标作为最终状态存储，仅在时间步求解过程中将自适应更新的子空间模态与局部节点丰富化作为加速计算的“临时便签”**。这一设计使得仿真器能够在保持IPC全部物理保障的前提下，利用无量纲的梯度误差与能量进度度量在线识别子空间失效区域，同时采用非重叠域分解保证求解稳定性，最终实现输出复杂度与动态复杂度（而非网格规模或材料刚度）成比例的高效仿真。

具体而言，本文提出了一套完整的自适应子空间时间积分框架，包含三个核心组件：
- **自适应oracle**：同时考虑接触与变形力的耦合物理，而非仅依赖几何接触接近度；
- **自适应模型**：以全空间坐标为背衬表示，在时间步求解中动态管理活跃模态基与节点丰富化集合；
- **并行时间步求解器**：基于Schur补系统的定制线性求解器，结合密集Cholesky分解与对角预条件共轭梯度法。

实验表明，该方法在输出视觉质量与全空间IPC等价的条件下，实现了超过一个数量级的端到端加速。

## 核心创新

### 1. 问题瓶颈与因果调节杠杆

传统子空间仿真在接触弹性动力学中面临一个根本性瓶颈：**在时间步求解之前，无法在线评估当前子空间基对形变的表达充分性**。当接触、摩擦或材料异质性引发高度局部的变形时，预计算的全局子空间基往往无法有效捕获这些细节，导致仿真质量下降；而若回溯到全空间计算，则完全丧失了子空间方法的加速意义。

本文提出的自适应子空间时间积分方法，通过引入两个用户可调的误差阈值——**节点误差阈值 ε_G^e** 与**模态误差阈值 ε_G^s**——构建了一个连续的精度-成本调节杠杆。这两个阈值直接控制自适应 oracle 激活节点丰富化和模态丰富化的敏感度：阈值越宽松，丰富化越少，计算越快；阈值越严格，丰富化越多，解越逼近全空间 IPC 参考解。如消融实验所验证，随着误差阈值收紧，自适应子空间求解器**单调收敛至全空间 IPC 解**（Fig. 12），证明了方法的可控性与一致性。

### 2. 核心洞察：全空间存储 + 子空间加速的"临时便签"范式

本工作的核心洞察在于**将全自由度坐标作为最终状态存储，仅在时间步求解过程中将自适应更新的子空间模态与局部节点丰富化作为加速计算的"临时便签"**。这一设计带来了三个关键优势：

- **输出质量与全空间 IPC 等价**：最终状态始终以全自由度坐标存储，子空间近似仅用于加速 Newton 迭代的中间求解过程，不引入累积误差或"跳变"伪影。
- **输出复杂度与动态复杂度成比例**：自适应 oracle 仅在变形局部化、接触力集中或弹性冲击波传播等真正需要全空间分辨率的区域激活节点丰富化，而在全局变形占主导的区域依赖子空间模态，使得计算成本与网格规模或材料刚度解耦，转而与场景的动态复杂度挂钩。
- **物理性质完整保留**：采用非重叠域分解保证求解稳定性，在维持 IPC 无条件不穿透、无反转等关键物理性质的前提下实现加速。

### 3. 关键 changed slots：相对基线的方法论创新

#### 3.1 运动学自由度表示：从全空间到自适应混合表示

| 维度 | 基线（Full-space IPC） | 本文方法 |
|------|----------------------|---------|
| **状态存储** | 所有节点自由度直接求解 | 全空间坐标 x ∈ ℝ^{dn} 作为主存储 |
| **时间步求解** | 在全空间系统上执行 Newton 迭代 | 在自适应更新的子空间模态 + 丰富化节点 DOF 的混合系统上求解 |
| **非丰富化区域** | 不适用 | 由掩码后的活跃模态处理 |

这一设计的关键在于：**最终状态始终以全空间坐标存储**，子空间近似仅作为加速 Newton 迭代的"临时便签"（running reduced-model scratch pad）。这从根本上避免了传统子空间方法中因基截断导致的累积误差和视觉跳变问题。

#### 3.2 自适应 Oracle：从无到在线物理耦合评估

| 维度 | 基线 | 本文方法 |
|------|------|---------|
| **自适应机制** | 无（手动选择子空间，或事后全空间分析） | 时间步内在线 oracle |
| **评估依据** | 几何接触接近度 | **接触力与变形力的耦合物理** |
| **评估指标** | 无 | 无量纲逐节点梯度误差 γ_i + 能量进度度量 η_i |
| **决策逻辑** | 无 | 同时激活梯度误差超阈值且进度不足的候选节点/模态 |

这是本文最核心的方法论创新。传统子空间自适应方法（如基于几何接触接近度的启发式规则）无法区分"需要丰富化的局部变形"与"可由现有子空间基表达的全局变形"。本文的 oracle 通过两个互补的无量纲度量解决了这一问题：

- **梯度误差度量 G(x)**：衡量当前子空间基对局部能量梯度的解析能力。当接触力或材料异质性引发局部高梯度时，该度量自然升高。
- **能量进度度量 E(x)**：衡量当前活跃子空间能实现的能量下降。即使梯度误差很大，如果现有模态已能有效降低能量（如纯刚性滑动），则无需丰富化。

Fig. 5 给出了一个典型示例：软方块在无摩擦斜面上纯刚性滑动时，梯度误差很大，但能量进度同样很大——因为刚性平移模态已能完美表达该运动，因此 oracle 正确判定无需丰富化。这一能力使得 oracle 能够**区分"需要丰富化的局部变形"与"可由现有基表达的全局变形"**，避免了不必要的计算开销。

#### 3.3 线性系统求解：从全空间直接/迭代到 Schur 补混合求解

| 维度 | 基线（IPC Pardiso LLT / IPC CG） | 本文方法 |
|------|--------------------------------|---------|
| **系统结构** | 全空间稀疏系统 | Schur 补系统：子空间块（稠密 Cholesky）+ 丰富化节点块（对角预条件 CG） |
| **子空间 Hessian** | 不适用 | 基于 BFGS 的逐子域局部割线近似 |
| **求解性能** | Pardiso LLT：固定成本；CG：刚度增加时迭代爆炸 | 相比 MKL Pardiso 快 6–40 倍，相比 Eigen CG 快高达 70 倍 |

线性求解器的创新体现在两个层面：

1. **系统分解**：将耦合的模态-节点系统通过 Schur 补消元分解为两个独立求解阶段。子空间模态块规模小且稠密，用 Cholesky 直接分解；丰富化节点块用对角预条件 CG 迭代求解。这一分解使得求解成本与丰富化节点数（而非总网格规模）成比例。

2. **子空间 Hessian 近似**：对弹性 Hessian 在活跃子空间中的投影，采用逐子域的 BFGS 局部割线更新，避免了每步重新投影全空间 Hessian 的高昂成本，同时保持了足够的曲率信息以保证 Newton 迭代的收敛速度。

实验验证了这一设计的鲁棒性：在橡胶手落刺床实验中（Fig. 16），当杨氏模量从 1e5 Pa 增至 1e9 Pa 时，IPC-CG 在 E≥1e8 Pa 时即触及 10,000 次迭代上限，而本文求解器的迭代次数虽有增加，但始终保持在实用范围内，远低于上限。

### 4. 方法模块总览

自适应子空间时间积分方法由以下核心模块构成：

| 模块 | 功能 | 证据锚点 |
|------|------|---------|
| **自适应子空间模型管理** | 维护活跃模态基 U_a 与丰富化节点集 X_a，掩码重叠 DOF | Sec. 3.2, 3.6 |
| **逐节点误差度量** | 计算无量纲梯度范数 γ_i，评估子空间对局部力的解析能力 | Eq. (5), Sec. 3.3 |
| **逐节点进度度量** | 估计活跃子空间可实现的局部能量下降 η_i | Eq. (7)(8), Sec. 3.4 |
| **时间步内自适应 Oracle** | 评估节点/模态候选的误差与进度，激活丰富化 | Sec. 3.5, 3.7 |
| **BFGS 子空间 Hessian 近似** | 逐子域局部割线更新弹性 Hessian 在活跃子空间中的投影 | Eq. (20), Sec. 3.9 |
| **Schur 补线性求解器** | 稠密 Cholesky + 对角预条件 CG 求解耦合系统 | Eq. (21)(22), Sec. 3.10 |
| **降采样（Downdating）** | 求解后移除位移贡献可忽略的模态/节点，回收计算资源 | Sec. 3.11 |

降采样模块的消融实验（Fig. 11）显示，启用降采样可减少活跃 DOF 并在端到端仿真中实现 **1.7 倍加速**，且无视觉质量损失，验证了该模块在维持精度前提下的资源回收有效性。

## 整体框架

本文提出的自适应子空间时间积分方法，其核心设计理念是**将全自由度坐标作为唯一的状态存储，而在每个时间步的求解过程中，仅将自适应更新的子空间模态与局部节点丰富化作为加速计算的“临时便签”**。这一策略确保了最终输出与全空间 IPC（Incremental Potential Contact）解在物理上保持一致，同时将求解复杂度从网格规模解耦，转而与当前动态的局部复杂程度成比例。

### 时间步求解的优化形式

每个时间步的求解被统一为一个增量势能（Incremental Potential）的极小化问题：

$$E(x) = K(x) + \alpha h^2 (\Psi(x) + B(x) + D(x))$$

其中 $K(x)$ 为惯性项，$\Psi(x)$ 为弹性变形能，$B(x)$ 为接触障碍能，$D(x)$ 为摩擦耗散能。该优化形式直接继承自全空间 IPC（Li et al., ACM Trans. Graph. 2020），保证了方法的物理基础——无条件不穿透与无反转——在自适应子空间框架下依然成立。

### 管线模块与数据流

整个求解管线由七个核心模块串联构成，形成“评估—丰富化—求解—降采样”的闭环：

1. **自适应子空间模型管理（$U_a$, $X_a$）**：维护当前活跃的模态基 $U_a$ 和已丰富化的节点集合 $X_a$。在非重叠域分解策略下，丰富化节点的自由度被显式离散化，而其余区域的自由度则由活跃模态的线性组合表达。该模块同时负责对重叠自由度进行掩码处理，确保模态与节点自由度之间的正交性（Fig. 6 左）。

2. **逐节点误差度量（$\gamma_i$ 标度）**：对每个节点计算无量纲的梯度误差，归一化因子 $\gamma_i = h^2 a_i \bar{W}_i$ 消除了时间步长、网格面积和材料刚度的影响，使得该度量在不同场景和参数下具有可比性。

3. **逐节点进度度量（$\eta_i$ 标度与 $\Delta E_i$）**：评估当前活跃子空间对每个节点附近能量的下降贡献。若当前子空间已能充分降低局部能量，则即使梯度误差较大（如纯刚性滑动），也无需触发丰富化（Fig. 5）。

4. **时间步内自适应 oracle**：根据误差与进度的双重判据，同时评估节点候选和模态候选的激活条件。只有当某候选的梯度误差超过阈值 $\varepsilon_G$ 且能量进度低于目标时，才将其激活加入系统。这一设计的关键在于**同时考虑了接触力与变形力的耦合物理**，而非仅依赖几何接触接近度。

5. **BFGS 子空间 Hessian 近似**：在每个预计算的 METIS 子域内，对弹性 Hessian 在活跃子空间中的投影进行局部割线更新。这避免了在每次 Newton 迭代中重新组装完整的子空间 Hessian，显著降低了计算开销（Fig. 7）。

6. **Schur 补线性求解器**：将耦合的模态-节点系统通过舒尔补消元分解为两步求解。首先对模态块进行稠密 Cholesky 分解，随后对节点丰富化自由度构建舒尔补系统，使用对角预条件共轭梯度法迭代求解。这一设计使得模态自由度（通常数量较少）的求解保持精确，而大规模节点自由度的求解则受益于迭代法的可扩展性。

7. **降采样（Downdating）**：在时间步求解完成后，移除那些位移贡献可忽略的模态和节点，回收自由度以降低后续时间步的计算成本。实验表明，降采样可减少活跃自由度并带来约 1.7 倍的端到端加速，且无视觉质量损失（Fig. 11）。

### 输入输出流

- **输入**：当前时间步的起始全空间位置 $x^t$、速度 $v^t$、预计算的子空间基库 $U$（如 Skinning Eigenmodes、Biharmonic Coordinates 等），以及用户设定的误差阈值 $\varepsilon_G^e$（节点丰富化）和 $\varepsilon_G^s$（模态丰富化）。
- **输出**：下一时间步的全空间位置 $x^{t+1}$，其视觉质量与全空间 IPC 解等价，但求解过程仅需操作远小于全自由度的活跃变量集合。
- **状态持久化**：全空间坐标 $x$ 始终作为主存储，自适应基和丰富化节点仅在当前时间步的 Newton 迭代中作为加速“便签”存在，步完成后即被更新或丢弃。

这一管线设计使得方法的输出复杂度与当前动态的局部复杂度成比例，而非与网格规模或材料刚度绑定，从而在复杂接触场景（如 Mushroom Madness，Fig. 1）中实现了超过一个数量级的端到端加速。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_dl_acm_org_doi_10_1145_3687946/figures/002_Figure_2.jpg]]
*Figure 2: Top left: available subspace models are generally well-suited for large global deformation but unable to resolve local deformations. Bottom: with our adaptive method a small amount of combined nodal and subspace enrichment closely captures the full-space solution’s deformation (top right)*

## 核心模块与公式推导

### 自适应子空间时间积分框架

方法将每个时间步的求解表述为增量势能（Incremental Potential）的最小化问题。最终状态始终以全自由度坐标 $\boldsymbol{x} \in \mathbb{R}^{dn}$ 存储，但在时间步求解过程中，自适应更新的子空间模态基与局部节点丰富化自由度作为“临时便签”使用，从而在保持 IPC 无条件不穿透、无反转等关键物理性质的前提下，大幅降低有效计算自由度。

**增量势能**定义为各能量项的加权和：

$$E(x) = K(x) + \alpha h^2 \big( \Psi(x) + B(x) + D(x) \big)$$

其中 $K(x)$ 为惯性能量，$\Psi(x)$ 为弹性势能，$B(x)$ 为接触障碍能量，$D(x)$ 为摩擦耗散能，$h$ 为时间步长，$\alpha$ 为时间积分方案决定的系数（隐式欧拉时 $\alpha = 1$）。每个分段线性的离散能量可进一步表示为网格单元模板上能量函数的加权和：

$$\sum_{s \in \mathcal{T}} w_s W_s(x)$$

### 自适应 Oracle 的核心度量

自适应 Oracle 在时间步内在线评估子空间解的质量，并决定是否激活节点丰富化或模态丰富化。其核心在于两个无量纲的逐节点度量。

**逐节点误差度量**：为消除时间步长、网格尺寸和材料参数的依赖性，定义缩放因子

$$\gamma_i = h^2 a_i \bar{W}_i$$

其中 $a_i$ 为节点 $i$ 的面积（或体积）权重，$\bar{W}_i$ 为节点邻域内能量密度 Hessian 的平均范数。由此得到节点 $i$ 的候选丰富化误差度量：

$$G_i(x) = \frac{\|g^i\|_2}{\gamma_i}, \quad g^i = \sum_{s \in \mathcal{T}_i} w_s \nabla W_s(x)$$

$g^i$ 为节点 $i$ 邻域模板上能量梯度的加权和。该度量是无量纲的，对时间步、材料和网格变化具有不变性。

**逐节点进度度量**：评估当前活跃子空间对节点附近能量下降的贡献。定义节点 $i$ 附近的能量变化：

$$\Delta E_i = E_i(x) - E_i(x + d_a)$$

其中 $d_a$ 为当前活跃子空间产生的 Newton 步位移。引入缩放因子

$$\eta_i = h^2 \upsilon_i \bar{W}_i$$

$\upsilon_i$ 为节点 $i$ 的体积权重。由此得到无量纲的进度度量，用于判断当前子空间是否已能充分降低该节点附近的能量。

**模态候选的误差与进度**：对于子空间 $s$ 中的单个模态，其误差投影为

$$g^s = U_s \left( \frac{u_{s,1}}{u_{s,1}^T u_{s,1}}, \cdots, \frac{u_{s,p}}{u_{s,p}^T u_{s,p}} \right)^T \nabla E(x) \in \mathbb{R}^{3n}$$

进度投影为

$$c^s = \bar{U}_s \left( \frac{\bar{u}_{s,1}}{\bar{u}_{s,1}^T \bar{u}_{s,1}}, \cdots, \frac{\bar{u}_{s,p}}{\bar{u}_{s,p}^T \bar{u}_{s,p}} \right)^T \Delta E \in \mathbb{R}^n$$

模态 $s$ 的误差度量取所有节点中最大的归一化梯度：

$$G_s(x) = \max_{j \in [1,n]} \frac{\|g_j^s\|_2}{\gamma_j}$$

### 非重叠域分解与线性系统求解

方法在节点丰富化自由度与活跃模态自由度之间采用**非重叠分解**：被丰富化的节点其自由度从子空间模态的掩码中排除，避免双重表示。由此得到的耦合 Newton 步线性系统具有如下分块结构：

$$\begin{pmatrix} H_q & J \\ J^T & H_x \end{pmatrix} \begin{pmatrix} d_q \\ d_x \end{pmatrix} = -\begin{pmatrix} g_q \\ g_x \end{pmatrix}$$

其中 $d_q$ 为模态坐标的增量，$d_x$ 为丰富化节点自由度的增量。

通过舒尔补消去模态块，得到针对节点丰富化自由度的简化系统：

$$(H_x - J^T H_q^{-1} J) d_x = H_q^{-1} g_q - g_x$$

该舒尔补系统采用对角预条件的共轭梯度法求解。模态块 $H_q$ 的 Hessian 通过逐子域的 BFGS 割线更新近似，并采用稠密 Cholesky 分解求逆。这一自定义线性求解器相比 MKL Pardiso 直接求解快 6–40 倍，相比带 3×3 块 Jacobi 预条件的 Eigen CG 快高达 70 倍。

### 降采样机制

时间步求解完成后，对位移贡献可忽略的模态和节点进行降采样，移除不再需要的自由度，以减少后续时间步的计算开销。该机制在无视觉质量损失的条件下可带来约 1.7 倍的端到端加速。

### Oracle 激活逻辑

自适应 Oracle 在每个时间步内持续评估子空间解质量：当候选节点或模态同时满足误差超过阈值 $G(x) > \varepsilon_G$ 且进度低于目标 $E(x) < \varepsilon_E$ 时，激活相应的丰富化。用户可调的节点误差阈值 $\varepsilon_G^e$ 与模态误差阈值 $\varepsilon_G^s$ 直接控制丰富化的敏感度，在精度与计算成本之间提供连续调节杠杆。随着误差阈值收紧，自适应子空间求解器单调收敛至全空间 IPC 解。

## 实验与分析

### 核心性能表现

本文在涵盖碰撞、摩擦、异构材料与大变形等多个复杂场景上验证了自适应子空间时间积分方法。表1汇总了各场景在单个高难度时间步（大变形与接触密集）下的求解统计与计时对比。在所有测试场景中，自适应子空间求解器相对于全空间IPC（Pardiso LLT直接求解）实现了**6–40倍**的单步加速，同时保持与全空间解视觉等价的输出质量。例如，在“Mushroom Madness”场景（250万四面体）中，自适应方法单步求解耗时约1分钟，而全空间IPC耗时约30分钟。

线性求解器的对比（表3）进一步揭示了加速来源。本文的舒尔补求解器（子空间块稠密Cholesky + 节点丰富化块对角预条件CG）在单步线性系统求解时间为**0.04–1.30秒**，而IPC Pardiso LLT为**0.25–21.4秒**，IPC CG（3×3块Jacobi预条件）为**2.10–36.5秒**。相较于IPC CG，本文线性求解器最快可达**70倍**加速；相较于Pardiso LLT，亦有约**10倍**优势。这一差距源于自适应方法有效降低了线性系统的规模：活跃自由度仅占全空间自由度的一小部分（表1中|E_a|/|V|列），且舒尔补结构将稠密子空间块与稀疏节点块解耦求解，避免了全空间稀疏直接分解的高昂成本。

### 材料刚度鲁棒性

图16展示了橡胶手落在钉床上的实验，通过扫描钉床的杨氏模量（1e5 Pa至1e9 Pa）来测试线性求解器对材料刚度的敏感性。IPC Pardiso LLT的求解时间几乎不随刚度变化，但IPC CG在刚度达到1e8 Pa时迭代次数即触及10,000次上限，求解成本爆炸。本文的舒尔补CG求解器虽然迭代次数也随刚度上升，但始终远低于上限，在E=1e9 Pa时仍保持实用水平。这一鲁棒性得益于子空间模态捕获了主导的全局弹性响应，节点丰富化仅需处理局部接触形变，使得CG系统的条件数受刚度变化的冲击远小于全空间CG。

### 自适应oracle的收敛性与可控性

误差阈值是调节精度与成本的核心杠杆。图12展示了软船落于冰山的阈值分析实验。左两图显示，随着全空间节点误差阈值ε_G^e降低，丰富化节点数单调增加，且以全空间IPC残差衡量的求解残差单调下降，最终收敛至全空间IPC解。右两图表明，子空间模态误差阈值ε_G^s的收紧同样单调提升活跃模态数并改善残差。这一单调收敛行为验证了自适应oracle的可控性：用户通过两个阈值即可在“近似快速解”与“精确全空间解”之间连续调节，无需手动选择子空间规模。

### 降采样（Downdating）的有效性

降采样机制在求解完成后移除对位移贡献可忽略的模态与节点，以降低后续时间步的活跃自由度。图11的消融实验（带刺滚筒碾压软地形）表明，启用降采样后，活跃自由度显著减少，端到端仿真时间获得**1.7倍**加速，且视觉质量无损。这证明降采样是维持长期仿真效率的关键组件，避免了冗余自由度随时间累积。

### 材料刚度与时间步长对丰富化的自适应响应

自适应oracle对材料刚度和时间步长的变化表现出合理的敏感性。图14中，刚性铁砧（E=1e9 Pa）落在不同刚度的“果冻”块上：当果冻较软（1e5 Pa）时，局部形变剧烈，节点丰富化大量激活；当果冻同样刚性（1e9 Pa）时，形变全局化，几乎不需要节点丰富化。图9的补充实验进一步证实，在接触力相似的情况下，仅提高材料刚度即可使丰富化消失，因为刚性材料将接触力传播为全局形变，可由子空间模态充分表达。

图15展示了异构材料场景（弹簧拳头击打明胶头部）在不同时间步长下的丰富化行为。随着时间步长减小，弹性冲击波被更精细地解析，节点丰富化量相应增加。这表明oracle能够感知时间分辨率对形变局部化程度的影响，自动调整计算资源的分配。

### 子空间基质量的影响

方法并非对任意子空间基都同样有效。图17对比了Skinning Eigenmodes、Biharmonic Coordinates和标准Eigenmodes三种子空间在相同oracle容差下的节点丰富化需求。前两者仅需少量节点丰富化即可匹配全空间解，而标准Eigenmodes因缺乏旋转不变性，需要大量节点丰富化来补偿子空间表达的不足。图18进一步展示了极端情况：Skinning Eigenmodes基完全不适合“Koosh”软刺球的触须变形，即使自适应oracle也无法弥补基的表达缺陷；而基于全空间仿真快照构建的小型POD基则更接近全空间解，但仍需显著丰富化以捕获细节。这表明自适应方法的效果受限于候选子空间库的表达能力——这是方法的一个已知局限。

### 与全空间解的位移差异

图13定量比较了自适应子空间解与全空间IPC解在“City”场景中的位移差异。最大差异集中在接触压缩最深的区域（即形变最大的位置），而在模态空间与全自由度空间的界面处也存在小幅位移差异。这些差异在视觉上不可见，但说明在给定阈值下，自适应解并非全空间解的逐顶点精确复现，而是在容差允许内的近似。

### 实验公平性说明

所有对比实验均采用相同的IPC模型与BDF2时间积分器，确保一致的物理保障（不穿透、无反转）。基线IPC求解器（Pardiso LLT、CG）配置为相同的收敛容差（相对残差1e-5）。在子空间模型对比中，保持相同的oracle容差与场景参数，仅改变子空间表示。存储全空间状态的内存开销与IPC相当；性能增益来源于时间步求解期间有效自由度的减少。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_dl_acm_org_doi_10_1145_3687946/figures/001_Figure.jpg]]

![[assets/figures/papers/paper_list_l6_https_dl_acm_org_doi_10_1145_3687946/figures/014_Figure.jpg]]
*Figure: Error Threshold (full DOF)*

![[assets/figures/papers/paper_list_l6_https_dl_acm_org_doi_10_1145_3687946/figures/017_Figure_14.jpg]]
*Figure 14: Stiff (E=1e9 Pa) Fig. 14. Our oracle performs well across a broad spectrum of material stiffnesses. We drop a stiff anvil (E = 1e9 Pa) onto a “jello” block with varying stiffness (1e5 Pa, 1e6 Pa, and 1e9 Pa) and observe that the amount of nodal enrichment (shown in dark red) directly varies with the stiffness and so on the amount of localized deformation*

![[assets/figures/papers/paper_list_l6_https_dl_acm_org_doi_10_1145_3687946/figures/019_Figure_16.jpg]]
*Figure 16: We drop a rubber hand on a bed of spikes, vary the spike stiffness, and measure resulting linear solve costs. As the stiffness increases, the runtime of IPC-LLT is effectively fixed, but IPC with a Conjugate Gradient iterative solver with block-jacobi preconditioning explodes in cost. We cap the iterative solves at 10,000 iterations and see that IPC-CG reaches this at stiffnesses of 1e8 Pa and above. Our solver also sees an iteration count increase, but is far less sensitive to stiffness variations than IPC-CG*

![[assets/figures/papers/paper_list_l6_https_dl_acm_org_doi_10_1145_3687946/figures/008_Table_1.jpg]]
*Table 1: We report statistics for a single time-step solve (choosing a step with large deformation and contact) for both our method and IPC. |𝑉 |, |𝐹 |, |𝑇 | are the number of vertices, faces, and tetrahedra, respectively, in the scene. | $\mathcal { E } _ { a }$ | / | V | is the ratio of enriched vertices to total vertices. | $U _ { a }$ | / | U | is the ratio of enriched bases to the total number of available bases. These values are measured at the end of the time-step. Timings are reported in 𝑚𝑖𝑛𝑢𝑡𝑒 : 𝑠𝑒𝑐𝑜𝑛𝑑𝑠 format for our algorithm as well the time taken for a full-space IPC to solve the same time-step*

![[assets/figures/papers/paper_list_l6_https_dl_acm_org_doi_10_1145_3687946/figures/009_Table_2.jpg]]
*Table 2: Scene parameters: 𝐸 is Young’s Modulus, 𝜈 is Poisson’s Ratio, Δ𝑡 is the time-step size, 𝐿 is the number of subdomains (same for both nodal enrichment and BFGS), $\epsilon _ { \mathcal { G } } ^ { s }$ and $\epsilon _ { \mathcal { G } } ^ { e }$ are the error thresholds for the subspace DOF and nodal DOF, respectively. $\epsilon _ { d }$ is the downdating threshold and | $U _ { \mathrm { i n i t } }$ | is the size of the initial basis

![[assets/figures/papers/paper_list_l6_https_dl_acm_org_doi_10_1145_3687946/figures/020_Table_3.jpg]]
*Table 3: We report the linear solver costs of the scenes shown, comparing our Schur complement solver against IPC with Pardiso LLT, and IPC-CG with 3 × 3-block-jacobi preconditioning. Linear systems are collected from the beginning of a representative time-step (large deformation and contact). We report the number nonzero in our full coupled system, the number of nonzeros for the full-space IPC problem, as well the number of iterations. Both iterative solvers are solved to a relative residual of 1e-5*

## 方法谱系与知识库定位

### 1. 与前驱工作的关系

本文的自适应子空间时间积分方法建立在两条研究脉络的交汇处：**子空间仿真**与**基于增量势的接触处理（IPC）**。

#### 1.1 相对于全空间 IPC 的继承与超越

本方法将 **Full-space IPC**（Li et al., ACM Trans. Graph. 2020）作为物理模型与求解质量的“黄金标准”基线。全空间 IPC 通过增量势公式统一处理弹性、接触障碍与摩擦，具备无条件不穿透与无反转的关键保障。本文完整继承了这些物理性质——全自由度坐标始终作为最终状态的主存储，自适应子空间仅作为时间步求解期间的加速“便签”——从而在输出端保持与全空间 IPC 等价的物理保真度。

超越之处在于**计算效率的根本性重构**：全空间 IPC 的求解成本与网格规模强相关（直接法 Pardiso LLT 或迭代法 CG 均需处理完整自由度），而本文通过在线自适应地激活子空间模态与局部节点丰富化，将求解复杂度从“网格规模”解耦为“动态复杂度”。在视觉等价条件下，端到端加速超过一个数量级（Table 1）；自定义线性求解器相比 MKL Pardiso 快 6–40 倍，相比带块 Jacobi 预条件的 Eigen CG 快高达 70 倍（Table 3）。

#### 1.2 相对于已有子空间方法的改进

已有子空间仿真方法（如 **Skinning Eigenmodes**（Benchekroun et al., ACM Trans. Graph. 2023）、**Biharmonic Coordinates**（Weber et al., Computer Graphics Forum 2012）及标准特征模态）面临的核心瓶颈是：**无法在仿真步求解之前未知全空间解的情况下，在线评估子空间基对当前形变（尤其由接触、摩擦和材料异质性导致的局部形变）的表达充分性**。这导致子空间仿真要么质量不足，要么需回溯全空间计算而失去加速意义。

本文的核心突破在于提出了一种**在线、时间步内的自适应 oracle**，该 oracle 同时考虑接触与变形力的耦合物理，而非仅依赖几何接触接近度。具体而言：
- **梯度误差度量**（$G_i(x)$ 与 $G_s(x)$）：通过无量纲化的每节点梯度范数，识别当前子空间无法充分表达力平衡的局部区域；
- **能量进度度量**（$\eta_i$ 与 $\Delta E_i$）：评估当前活跃子空间在局部已产生的能量下降，避免对纯刚性运动等已被良好捕获的变形进行冗余丰富化（如 Fig. 5 所示）。

这种“误差+进度”的双重判断机制，使 oracle 能够区分“力不平衡但子空间已可解决”与“力不平衡且子空间无法解决”两种情形，从而精准激活节点丰富化或模态丰富化。

#### 1.3 相对于 Stencil Descent 的选择

本文在方法背景中对比了 **Stencil Descent**（Lan et al., 2023）与 Newton 方法在网格细化下的收敛行为（Fig. 3）。Stencil Descent 作为一种坐标下降法，其收敛速度随网格分辨率增加而恶化；而 Newton 方法保持超线性收敛。这一对比为本文选择 Newton 型求解器（而非坐标下降类方法）作为自适应子空间内部的优化引擎提供了实验依据。

### 2. 方法适用边界

#### 2.1 子空间基质量的依赖性

方法的核心前提是**存在一个具有足够表达能力的初始子空间基**。当子空间基质量不佳时（如标准特征模态缺乏旋转不变性），即使 oracle 正常工作，仍需大量节点丰富化来弥补（Fig. 17 中标准特征模态需要“heavy nodal enrichment”）。在极端情况下（如 Fig. 18 中 Skinning Eigenmodes 对“Koosh”球的细须变形完全不适用），自适应机制可能无法充分捕获全局变形。

这意味着：
- 用户仍需审慎选择与场景变形模式匹配的子空间基；
- 误差阈值 $\varepsilon_G^e$ 与 $\varepsilon_G^s$ 需要针对所提供基的质量进行调整，阈值不随基自动标定；
- 更严格的阈值可在一定程度上缓解基质量不足的问题，但代价是更多丰富化（从而降低加速比）。

#### 2.2 位移差异的容差性

尽管方法保证了底层物理模型的不穿透和无反转特性，自适应子空间解与全空间 IPC 解之间在容差允许范围内仍可能存在位移差异。这些差异主要集中在最深压缩的接触点（Fig. 13），以及模态与全自由度空间的界面处。在视觉等价的意义上，这些差异不可见，但对于需要精确逐点位移匹配的应用场景（如某些工程分析），需谨慎评估容差设置。

#### 2.3 材料刚度与时间步长的耦合

Oracle 的丰富化行为自然地适应材料刚度与时间步长变化：
- **软材料**（低杨氏模量）产生更局部的形变，触发更多节点丰富化；**硬材料**（高杨氏模量）形变更全局化，丰富化需求降低甚至为零（Fig. 14, Fig. 9）；
- **更小的时间步长**能更好地解析弹性冲击波，需要更多节点丰富化（Fig. 15）。

这种自适应行为是方法的优势，但也意味着：在极硬材料或极粗时间步长下，方法可能退化为几乎纯子空间仿真；在极软材料或极细时间步长下，丰富化需求可能大幅增加，削弱加速效果。

### 3. 局限与开放问题

#### 3.1 已识别的局限

1. **子空间基质量依赖**（见 2.1）：方法无法从完全不合适的子空间基中“自救”，这是自适应机制的根本性约束。
2. **阈值手动调节**：$\varepsilon_G^e$、$\varepsilon_G^s$ 及降采样阈值 $\varepsilon_d$ 需用户设定，缺乏自动标定机制。
3. **异构子空间库的局限**：当前方法假设单一线性子空间，未支持来自不同物理过程或数据源的异构子空间库的在线切换。

#### 3.2 开放问题（来自原文讨论）

1. **异构子空间库**：如何将方法扩展至支持来自不同过程的子空间库（如不同预计算模态、不同材料区域的局部基）的在线自适应组合？
2. **连续神经子空间与拓扑变化**：如何结合连续神经子空间（Fulton et al., 2019; Modi et al., 2024）或断裂模式（Sellán et al., 2022）来处理拓扑变化场景？
3. **维度扩展**：将该方法扩展到壳和杆等降维单元的可行性与效果如何？
4. **超大规模场景的内存效率**：如何进一步提高子空间构建的内存效率以支持数十亿元素场景？
5. **GPU 并行化**：在 GPU 架构（如 GIPC, Huang et al., 2024）上探索并行管线实现以进一步加速。

### 4. 知识库定位

本文在知识库中的定位可概括为：**面向接触弹性动力学的在线自适应子空间时间积分框架**，其核心贡献在于：

| 维度 | 定位 |
|------|------|
| **物理模型** | 继承 IPC 的无条件不穿透/无反转保障 |
| **自由度管理** | 全空间存储 + 自适应子空间求解“便签” |
| **自适应机制** | 基于耦合物理（非纯几何）的在线 oracle，双阈值可调 |
| **求解器架构** | 非重叠域分解 + Schur 补系统 + 对角预条件 CG + BFGS 子空间 Hessian 近似 |
| **性能特征** | 输出复杂度与动态复杂度成比例，而非网格规模或材料刚度 |
| **控制杠杆** | $\varepsilon_G^e$（节点误差阈值）与 $\varepsilon_G^s$（模态误差阈值）提供精度-成本连续调节 |

该方法在子空间仿真与接触力学交叉领域填补了“在线自适应评估子空间充分性”这一关键空白，为后续研究（异构子空间库、神经子空间、GPU 加速）提供了可扩展的框架基础。

## 原文 PDF

![[paperPDFs/TOG_2024/Trading_Spaces_Adaptive_Subspace_Time_Integration_for_Contacting_Elastodynamics.pdf]]
