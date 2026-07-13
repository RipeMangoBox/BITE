---
title: "Differentiable Model Predictive Control on the GPU"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Differentiable_Model_Predictive_Control_on_the_GPU.pdf
project_link: null
code_link: https://github.com/ToyotaResearchInstitute/diffmpc
openreview_forum_id: bFYfV6c9zu
aliases:
- DMPCG
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "利用OCP的时间稀疏结构和定制的PCG求解器，以在GPU上实现跨时间步的并行化。"
primary_logic: "通过利用问题结构（如块三对角KTT矩阵）和PCG进行并行求解，可以在不牺牲收敛性的情况下，相比基于序列Riccati递归的方法，在GPU上显著加速可微分MPC。"
claims:
- "DiffMPC avoids Riccati recursions using a tailored PCG routine, enabling significant speedups over existing methods."
- "DiffMPC is 4 times faster than the fastest baseline on GPU for RL."
- "DiffMPC trains approximately 2x faster in wall-clock time for imitation learning."
- "The learned policy succeeds in 100% of trials compared to 70% for the baseline on Supra drifting through water puddles."
---

# Differentiable Model Predictive Control on the GPU

> [!tip] 核心洞察
> 通过利用问题结构（如块三对角KTT矩阵）和PCG进行并行求解，可以在不牺牲收敛性的情况下，相比基于序列Riccati递归的方法，在GPU上显著加速可微分MPC。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GPU上的可微分模型预测控制 |
| 英文题名 | Differentiable Model Predictive Control on the GPU |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=bFYfV6c9zu) · [GitHub](https://github.com/ToyotaResearchInstitute/diffmpc) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | DiffMPC |
| Dataset | Randomly-generated MPC problems (RL), Cart-pole imitation learning, Toyota Supra drifting through water puddles (simulation) |

> [!tip] 效果简介
> - Randomly-generated MPC problems (RL) 上，GPU backward-pass computation time 为 DiffMPC (0.32 s on Problem 1)，对比 trajax (1.83 s on Problem 1)，变化 ~4× speedup。
> - Cart-pole imitation learning 上，wall-clock training speed 为 DiffMPC，对比 trajax，变化 ~2× speedup。
> - Toyota Supra drifting through water puddles (simulation) 上，success rate 为 learned controller 100%，对比 baseline controller 70%，变化 +30%。

## 概要

**问题瓶颈**：可微分模型预测控制（MPC）将最优控制嵌入学习管道，但传统求解器（如 iLQR）依赖沿时间步的顺序 Riccati 递归，难以在 GPU 上高效并行化，严重制约了其在深度学习任务中的可扩展性。

**核心方法**：DiffMPC 用定制化的预条件共轭梯度（PCG）求解器替代 Riccati 递归，直接求解最优控制问题（OCP）KKT 系统的 Schur 补方程组。该求解器利用 OCP 的块三对角稀疏结构，将时间步上的求解过程并行化，同时支持跨问题实例的 warm-start。整体管道采用序列二次规划（SQP）进行前向求解，反向传播通过隐函数定理（IFT）计算梯度，前向已分解的 KKT 矩阵被直接复用。

**关键结果**：
- **速度**：在随机生成的 MPC 强化学习（RL）基准上，DiffMPC 的 GPU 反向传播时间约为最快基线 trajax 的 1/4（~4× 加速）；在倒立摆模仿学习任务上，训练墙钟时间快约 2 倍。
- **梯度质量**：PCG 退出容差在 1e-6 以内时，与有限差分的余弦相似度保持在 0.99 以上。
- **真机验证**：在丰田 Supra 穿越水洼漂移任务中，学习到的控制器成功率 100%，而相同 MPC 结构但未学习的基线仅 70%；实车测试中基线在首个弯道失控，学习控制器成功完成八字漂移。

**方法定位**：DiffMPC 属于可微分优化的 MPC 分支，与基于 iLQR 的 **mpc.pytorch**（Amos et al., 2018）、**trajax**（Frostig et al., 2021）以及通用可微分非线性最小二乘求解器 **Theseus**（Pineda et al., 2022）形成对比。其关键差异在于用并行 PCG 替代顺序 Riccati 递归，从而在 GPU 上获得显著加速，同时保持收敛性。该方法当前仅支持无不等式约束的 OCP，梯度计算采用 Gauss-Newton 近似（忽略动力学曲率），且实车部署时以 OSQP 替代 PCG，训练与线上求解尚未统一。



### 可微分优化与模型预测控制

可微分优化（Differentiable Optimization, DO）将优化问题的解映射视为可微分层，嵌入端到端学习管道。在模型预测控制（MPC）中，控制策略由求解一个参数化的最优控制问题（OCP）产生：

$$\mathbf{OCP:}\ \underset{z=(x,u)}{\mathrm{arg\,min}} \sum_{t=0}^{T}c_t^{x,\theta}(x_t)+\sum_{t=0}^{T-1}c_t^{u,\theta}(u_t)\ \mathrm{s.t.}\ f_t^{\theta}(x_{t+1},x_t,u_t)=0,\ x_0=x_s^{\theta}$$

其中 $\theta$ 为可学习参数（如成本权重、动力学系数或初始状态）。通过可微分MPC，这些参数可通过强化学习（RL）或模仿学习（IL）进行端到端训练，使策略能够自适应于任务需求。

### 现有方法的瓶颈：序列Riccati递归

当前主流的可微分MPC求解器——包括 **mpc.pytorch**（Amos et al., 2018）和 **trajax**（Frostig et al., 2021）——均基于迭代线性二次型调节器（iLQR）。iLQR的核心是Riccati递归，其计算模式具有内在的**时间序列依赖性**：每一时间步的求解必须等待前一步的结果。这种顺序性质带来了两个关键限制：

1. **GPU并行化受阻**：Riccati递归无法在GPU上跨时间步并行执行，导致计算资源利用率低下，限制了可微分MPC在大规模深度学习场景中的可扩展性。
2. **无法利用warm-starting**：在MPC的滚动时域求解中，相邻问题实例高度相似，但iLQR的递归结构无法有效利用前一解的warm-start信息来加速当前求解。

此外，通用的可微分非线性最小二乘求解器如 **Theseus**（Pineda et al., 2022）虽然灵活，但未针对OCP的特殊结构进行定制，同样面临效率瓶颈。

### 本文动机

本文的核心洞察是：**OCP的KKT系统具有块三对角稀疏结构，这一结构可以被利用来设计并行化的线性系统求解器，从而替代序列Riccati递归。** 具体而言，通过Schur补方法将KKT系统转化为关于对偶变量 $\lambda$ 的线性系统 $S\lambda = \gamma$，其中 $S$ 为块三对角矩阵。采用预条件共轭梯度法（PCG）求解该系统，可以在GPU上实现跨时间步的并行化，同时保持收敛性。

基于这一思路，本文提出 **DiffMPC**——一个完全在JAX中实现的可微分MPC求解器，其核心是用定制的PCG例程替代传统的Riccati递归，在正向求解和反向梯度计算中均实现显著的GPU加速。该方法同时支持warm-starting，进一步提升了滚动时域优化场景下的效率。



## 核心方法与创新机理

### 瓶颈：顺序 Riccati 递归阻碍 GPU 并行化

现有可微分 MPC 求解器（如 **mpc.pytorch**（Amos et al., 2018）和 **trajax**（Frostig et al., 2021））依赖 iLQR 框架，其核心是通过时间步上的顺序 Riccati 递归来求解线性系统。这种顺序性质从根本上限制了 GPU 上的并行化能力——每个时间步的计算必须等待前一步完成，导致在批处理或长时域场景下扩展性严重受限。通用可微分非线性最小二乘求解器 **Theseus**（Pineda et al., 2022）虽然不限于 MPC，但同样未针对 OCP 的时间稀疏结构进行专门优化。

### 核心洞察：用结构感知的并行求解替代顺序递归

DiffMPC 的关键洞察在于：**OCP 的 KKT 矩阵具有块三对角稀疏结构，利用这一结构并采用预条件共轭梯度法（PCG），可以在不牺牲收敛性的前提下，将跨时间步的顺序计算转化为可并行的矩阵运算**。具体而言，通过构造 Schur 补系统 $S\lambda = \gamma$ 并采用三对角预条件，PCG 的每次迭代都能在 GPU 上跨所有时间步并行执行，从而突破 Riccati 递归的顺序瓶颈。这一设计同时带来了 warm-starting 能力——PCG 可以利用前一求解实例的解作为初始猜测加速收敛，而 iLQR 的 Riccati 递归无法利用跨问题实例的 warm-start。

### 方法谱系与知识库定位

DiffMPC 位于**可微分优化 × 模型预测控制**的交叉点，其方法谱系可沿两个维度定位：

| 维度 | 传统路径 | DiffMPC 路径 |
|------|----------|-------------|
| 线性系统求解 | Riccati 递归（时间顺序） | PCG + 三对角预条件（时间并行） |
| 梯度计算 | 通过 iLQR 反向传播 | 隐函数定理（IFT）+ 复用前向 KKT 矩阵 |
| 并行策略 | 仅跨批处理维度 | 跨时间步 + 跨批处理双维度并行 |

在可微分 MPC 工具链中，DiffMPC 与现有方法的关系如下：
- **mpc.pytorch** / **trajax**：均基于 iLQR，前向求解和反向传播均依赖顺序 Riccati 递归；DiffMPC 用 PCG 替换了这一核心模块。
- **Theseus**：通用可微分非线性最小二乘求解器，不利用 OCP 的时间稀疏结构；DiffMPC 通过块三对角预条件专门针对 OCP 进行加速。

### Changed Slot：从 Riccati 到 PCG 的线性系统求解

DiffMPC 相对 baseline 的核心 **changed slot** 是线性系统求解器：

- **Baseline 值**：Riccati 递归（顺序遍历时间步，每个时间步涉及小规模矩阵运算，但整体串行）。
- **Proposed 值**：预条件共轭梯度法（PCG），配合三对角预条件（Bu & Plancher, 2024；Adabag et al., 2024）。PCG 将求解过程转化为一系列矩阵-向量乘积，这些乘积可在 GPU 上跨所有时间步并行计算。同时，状态和控制的恢复也可并行化：

$$x_t = -Q_t^{-1}(q_t + A_{t-1}^{+\top}\lambda_t + A_t^\top\lambda_{t+1}),\quad u_t = -R_t^{-1}(r_t + B_t^\top\lambda_{t+1})$$

该 changed slot 的证据强度高（confidence 0.95），直接支撑了论文的核心加速主张。此外，前向 SQP 过程中预计算的 KKT 矩阵 $\frac{\partial F}{\partial w}$ 在反向传播中被复用，仅需一次额外的 PCG 求解即可获得梯度，避免了重新构建矩阵的开销。

### 证据强度总结

| 核心主张 | 证据锚点 | 置信度 |
|----------|----------|--------|
| PCG 替代 Riccati 递归实现时间并行 | Section 3.3 / Algorithm 3 | 0.95 |
| GPU 上 RL 反向传播加速约 4× | Figure 3 / Table 3 | 0.95 |
| 模仿学习训练墙钟时间加速约 2× | Figure 4 | 0.95 |
| 学习策略在漂移任务中成功率 100% vs 基线 70% | Figure 6 | 0.95 |
| Warm-starting 在低 PCG 容差下加速前向求解达 11% | Figure 10 | 0.90 |
| 梯度余弦相似度在 PCG 容差 ≤ 1e-6 时保持 > 0.99 | Figure 9 | 0.90 |

### 局限与待验证问题

尽管核心创新在实验中得到了有力验证，但仍存在几个值得注意的局限：

1. **不等式约束缺失**：当前方法仅支持无约束 OCP，无法原生处理不等式约束（如控制量边界）。虽然可通过增广拉格朗日法或内点法扩展，但实现更复杂，且约束边界处的梯度不连续问题尚未解决。
2. **梯度近似**：梯度计算中忽略了动力学约束的曲率（采用类似 iLQR 的 Gauss-Newton 近似），可能导致梯度精度下降，但消融实验显示在适当 PCG 容差下与有限差分的一致性仍很高。
3. **训练与部署不一致**：实际车辆部署时使用 OSQP 而非训练中的 PCG，PCG 方案尚未在硬件上实时运行。硬件实验仅成功运行一次，结果的可重复性和统计显著性有限。
4. **初始化鲁棒性**：可微分优化管道对初始化敏感，如何提供稳健初始化以避免求解器发散仍是一个开放问题。



![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_bFYfV6c9zu/figures/002_Figure_2.jpg]]
*Figure 2: DiffMPC architecture: forward and backward passes, data flows, and main steps*

DiffMPC 将可微分模型预测控制（MPC）构造为一个端到端的可微分优化管道，其核心设计目标是通过暴露最优控制问题（OCP）的时间稀疏结构，在 GPU 上实现跨时间步的并行化，从而克服传统序列 Riccati 递归方法（如 iLQR）在深度学习场景中的可扩展性瓶颈。

### 管道总览

图 2 给出了 DiffMPC 的整体架构，包含两个主阶段：**前向传播（Forward Pass）** 和**反向传播（Backward Pass）**，二者共享关键的线性系统结构。

```
输入: OCP 参数 θ（成本函数、动力学模型、初始条件等）
       ┌─────────────────────────────────────┐
       │         Forward Pass (SQP)          │
       │  ┌─────────────────────────────┐    │
       │  │ 并行评估 Q, R, q, r, A, B, C │    │
       │  │ 构建 KKT 矩阵 G, H           │    │
       │  │ PCG 求解 Sλ = γ             │    │
       │  │ 并行恢复 z = (x, u)          │    │
       │  │ Line Search 全局化           │    │
       │  └─────────────────────────────┘    │
       │            ↓ 输出 z, KKT 矩阵        │
       ├─────────────────────────────────────┤
       │        Backward Pass (IFT)          │
       │  ┌─────────────────────────────┐    │
       │  │ 复用 KKT 矩阵                │    │
       │  │ PCG 求解灵敏度系统            │    │
       │  │ VJP 计算 ∂ℓ/∂θ              │    │
       │  └─────────────────────────────┘    │
       └─────────────────────────────────────┘
输出: 梯度 ∂ℓ/∂θ
```

### 前向传播：SQP + PCG

前向传播采用**序贯二次规划（SQP）** 求解非凸 OCP（Algorithm 1）。在每次 SQP 迭代中：

1. **并行矩阵评估**：所有时间步的成本 Hessian（$Q_t, R_t$）、梯度（$q_t, r_t$）和动力学 Jacobian（$A_t, B_t$）在 GPU 上并行计算，利用 OCP 的时间独立性。
2. **KKT 系统构建**：形成块三对角结构的 KKT 矩阵 $\frac{\partial F}{\partial w} = \begin{bmatrix} G & H^\top \\ H & 0 \end{bmatrix}$，其中 $G = \mathrm{blkdiag}(Q_0, \ldots, Q_T)$ 为块对角矩阵，$H$ 具有带状稀疏结构（见 Eq. 5）。
3. **PCG 求解**：通过 Schur 补 $S = -H G^{-1} H^\top$ 将系统降维为 $S\lambda = \gamma$，使用**预条件共轭梯度法（PCG）** 迭代求解（Algorithm 3）。预条件子利用 $S$ 的块三对角特性（Bu & Plancher, 2024; Adabag et al., 2024），使 PCG 的每次迭代可在时间维上并行执行——这是 DiffMPC 区别于序列 Riccati 递归的核心机制。
4. **并行原始变量恢复**：一旦获得 $\lambda$，状态和控制通过 $x_t = -Q_t^{-1}(q_t + A_{t-1}^{+\top}\lambda_t + A_t^\top\lambda_{t+1})$ 和 $u_t = -R_t^{-1}(r_t + B_t^\top\lambda_{t+1})$ 在所有时间步上并行恢复（Eq. 11）。
5. **Line Search 全局化**：采用基于 merit function 的标准线搜索（Algorithm 4）确保 SQP 的全局收敛性。

### 反向传播：IFT + VJP

反向传播基于**隐函数定理（IFT）** 计算标量损失 $\ell$ 对 OCP 参数 $\theta$ 的梯度（Algorithm 2）。关键设计在于：

- **复用 KKT 矩阵**：前向传播在收敛时已构建并分解了 KKT 矩阵 $\frac{\partial F}{\partial w}$，反向传播直接复用该矩阵求解灵敏度系统，避免了重复的矩阵构建开销。
- **VJP 高效计算**：梯度通过向量-雅可比积（VJP）$\frac{\partial\ell}{\partial\theta}^\top = -\frac{\partial F}{\partial\theta}^\top\left(\left[\frac{\partial F}{\partial w}\right]^{-1}\left[\frac{\partial\ell}{\partial z}\right]\right)$ 计算（Eq. 3），只需一次额外的 PCG 求解，无需显式构建完整的雅可比矩阵。

### 并行性与 Warm-Start

DiffMPC 的并行性来源于三个层面：
1. 矩阵评估在所有时间步上并行；
2. PCG 内部迭代通过块三对角结构实现时间并行；
3. 原始变量恢复在时间维上完全并行。

此外，PCG 的迭代性质天然支持**warm-starting**——将前一次求解的 $\lambda$ 作为下一次求解的初始猜测。这在 MPC 的滚动时域优化中尤为有效，而 iLQR 的 Riccati 递归无法利用这种跨问题实例的 warm-start。消融实验表明，在较低 PCG 退出容差（1e-4）下，warm-starting 可将前向传播时间减少最多 11%（Figure 10）。

### 学习范式兼容性

DiffMPC 作为一个完全可微分的策略 $\pi^\theta(x_0)$，可直接嵌入标准的强化学习（RL）和模仿学习（IL）框架：

- **RL 目标**：$\max_\theta \mathbb{E}\left[\sum_{t=1}^{H} R(x_t, \pi^\theta(x_t))\right]$，其中状态通过仿真环境递推，梯度经 DiffMPC 的反向传播传递。
- **IL 目标**：$\min_\theta \mathbb{E}\left[\|(\hat{u}_0, \ldots, \hat{u}_T) - \pi_{0:T}^\theta(x_0)\|^2\right]$，最小化 MPC 策略输出与专家演示控制序列的平方误差。

整个管道使用 JAX 实现，便于与主流深度学习框架集成。



### 前向传播：SQP与PCG求解

DiffMPC的前向传播采用序列二次规划（SQP）框架求解参数化最优控制问题OCP。对于一般非凸的OCP，SQP在每次迭代中构造一个QP子问题，其KKT系统具有块三对角结构：

$$\frac{\partial F}{\partial w} = \begin{bmatrix} G & H^\top \\ H & 0 \end{bmatrix}, \quad G = \mathrm{blkdiag}(Q_0,\ldots,Q_T), \quad H = \begin{bmatrix} I & 0 & 0 \\ A_0 & B_0 & A_0^+ \\ & \ddots & \ddots \end{bmatrix}$$

其中 $G$ 为分块对角矩阵，包含各时间步的状态和控制Hessian近似；$H$ 为动力学约束的Jacobian矩阵，呈现块双对角结构。

求解该KKT系统的核心瓶颈在于线性方程组的求解。传统可微分MPC方法（如**Theseus** (Pineda et al., 2022)、**mpc.pytorch** (Amos et al., 2018)、**trajax** (Frostig et al., 2021)）依赖Riccati递归，该递归本质上是时间维度上的顺序操作，无法在GPU上有效并行化。

DiffMPC的关键设计是用**预条件共轭梯度法（PCG）**替代Riccati递归。具体而言，通过构造Schur补将系统解耦为两步：

$$S := -HG^{-1}H^\top, \quad \gamma := d + HG^{-1}b$$

$$S\lambda = \gamma, \quad z = -G^{-1}(b + H^\top\lambda)$$

其中 $S$ 为Schur补矩阵，$\lambda$ 为拉格朗日乘子，$z$ 为原始变量。PCG求解器（Algorithm 3）利用 $S$ 的块三对角结构，配合三对角预条件子（Bu & Plancher, 2024），在GPU上实现跨时间步的并行化。一旦 $\lambda$ 求解完成，原始变量 $z$ 可通过下式在GPU上并行恢复：

$$x_t = -Q_t^{-1}(q_t + A_{t-1}^{+\top}\lambda_t + A_t^\top\lambda_{t+1}), \quad u_t = -R_t^{-1}(r_t + B_t^\top\lambda_{t+1})$$

前向传播还包含基于merit函数的线搜索（Algorithm 4），以确保SQP的全局收敛性。整体前向流程见Algorithm 1。

### 反向传播：基于隐函数定理的梯度计算

反向传播利用隐函数定理（IFT）计算标量损失 $\ell$ 对OCP参数 $\theta$ 的梯度。给定前向传播得到的KKT矩阵 $\frac{\partial F}{\partial w}$，梯度通过求解单个线性系统获得：

$$\frac{\partial\ell}{\partial\theta}^\top = -\frac{\partial F}{\partial\theta}^\top\left(\left[\frac{\partial F}{\partial w}\right]^{-1}\left[\frac{\partial\ell}{\partial z}\right]\right)$$

该式的核心计算是求解以 $\frac{\partial\ell}{\partial z}$ 为右端项的线性系统，其系数矩阵与前向传播中的KKT矩阵相同。DiffMPC在前向传播中预计算并缓存该矩阵，反向传播时直接复用，通过PCG求解器完成梯度计算（Algorithm 2）。这一设计避免了重新构造矩阵的开销，且PCG的并行特性使得反向传播同样受益于GPU加速。

### 并行性来源与warm-starting

DiffMPC的并行性来自两个层面：其一，每次SQP迭代中所有矩阵（$Q_t, R_t, A_t, B_t$ 等）在GPU上并行计算；其二，PCG例程虽然是迭代式的，但其每次迭代内的矩阵-向量乘积可跨时间步并行执行。此外，PCG天然支持跨问题实例的warm-starting——将前一次求解的 $\lambda$ 作为下一次求解的初始猜测，而iLQR的Riccati递归不具备这一能力。消融实验表明，在较低的PCG退出容差（$10^{-4}$）下，warm-starting可将前向传播时间减少最多11%（Figure 10）。



## 实验与关键发现

### 核心性能基准

DiffMPC 在 GPU 上的主要加速优势体现在两个核心场景中。在**强化学习（RL）基准测试**中，DiffMPC 的 GPU 反向传播计算时间比最快的基线方法快约 4 倍。例如在 Problem 1 上，DiffMPC 的反向传播耗时 0.32 秒，而 trajax 需要 1.83 秒（Table 3, Figure 3）。该基准测试将问题构造为凸问题，禁用线搜索，所有求解器限制为单次迭代，以确保公平比较。在**模仿学习（IL）基准测试**（倒立摆 cart-pole）中，DiffMPC 的 wall-clock 训练速度约为 trajax 的 2 倍，同时保持了相当的收敛性（Figure 4）。两种方法均限制为 5 次 SQP/iLQR 迭代，并使用专家轨迹进行 warm-start。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_bFYfV6c9zu/figures/015_Table_3.jpg]]
*Table 3: Timing results on CPU and GPU across 6 problem instances with mean time and 2σ (s)*

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_bFYfV6c9zu/figures/003_Figure_3.jpg]]
*Figure 3: RL computation times on one of the test problems. Error bars indicate 2σ confidence intervals. Each backward pass also includes one forward pass (to evaluate the inputs of Algorithm 2)*

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_bFYfV6c9zu/figures/004_Figure_4.jpg]]
*Figure 4: Losses over 200 epochs for the pendulum cart-pole IL benchmark*

Table 3 提供了跨 6 个问题实例、CPU 与 GPU 上的全面计时结果。DiffMPC 在 GPU 上的正向和反向传播时间均显著低于 Theseus、mpc.pytorch 和 trajax。值得注意的是，mpc.pytorch 在 GPU 上的原始实现极慢（正向传播 67.9 秒），经过修改后加速约 36 倍（Table 1），但仍远慢于 DiffMPC。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_bFYfV6c9zu/figures/011_Table_1.jpg]]
*Table 1: Computation times (s) with mpc.pytorch for Problem 1 on the GPU*

### 消融实验

**梯度精度与 PCG 退出容差**：DiffMPC 计算的梯度与有限差分之间的余弦相似度在 PCG 退出容差高达 1e-6 时仍保持在 0.99 以上（Figure 9）。这表明 PCG 求解器在较宽松的容差下仍能提供高精度梯度，为加速训练提供了依据。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_bFYfV6c9zu/figures/014_Figure_9.jpg]]
*Figure 9: Cosine similarity between computed gradients and finite differencing across PCG exit tolerances*

**Warm-starting 效果**：warm-starting 在低 PCG 退出容差（1e-4）下可将正向传播时间减少最多 11%，但在更严格的容差（1e-12）下加速效果降至约 4%（Figure 10）。这一效果相对温和，说明 PCG 本身的并行化优势是加速的主要来源，warm-starting 提供的是额外但有限的增益。

### 鲁棒漂移应用验证

DiffMPC 被用于一个具有挑战性的实际任务：通过领域随机化训练 MPC 策略，使丰田 Supra 在水坑中鲁棒漂移。训练使用超过 100 个时间步的大 episode 长度和至少 32 的 batch size（Figure 5 展示了训练管线）。

**仿真结果**：在带水坑的 8 字形漂移中，学习到的策略成功率为 100%，而基线控制器仅为 70%（Figure 6）。学习后的 MPC 参数发生了显著变化：后轮摩擦系数降低了 13%，侧滑角误差代价降低了 58%（Figure 12）。这表明领域随机化使策略学会了更保守的摩擦假设和对侧滑角偏差的更大容忍。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_bFYfV6c9zu/figures/006_Figure_6.jpg]]
*Figure 6: Vehicle states (left) and position trajectories (right) when drifting a figure 8 with puddles*

**硬件验证**：学习到的策略成功部署到实车上。在带水坑的圆形漂移中，学习策略在整个漂移过程中保持了更低的受控侧滑角 β（Figures 7, 8）。在 8 字形漂移的实车测试中，学习控制器在水坑处表现出明显更强的鲁棒性（Figure 13）。但需注意，硬件实验仅成功运行一次，结果的可重复性和统计显著性有限。此外，实车部署时使用 OSQP 而非训练中的 PCG 进行在线求解，线上与训练不完全一致。

### 关键局限与注意事项

1. **不等式约束缺失**：当前方法仅支持无约束 OCP，无法原生处理不等式约束。论文指出可通过增广拉格朗日法或内点法扩展，但实现更复杂，且约束边界处的梯度不连续性问题未解决。
2. **梯度近似**：梯度计算中忽略了动力学约束的曲率（采用类似 iLQR 的 Gauss-Newton 近似），可能影响梯度精度。
3. **训练与部署不一致**：实车部署时 PCG 方案尚未在硬件上实时运行，使用 OSQP 替代。
4. **硬件结果有限**：实车实验仅成功运行一次，统计显著性不足。

### 补充图表

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_bFYfV6c9zu/figures/013_Table_2.jpg]]
*Table 2: Parameters in the RL benchmark: state dimension n _ { x } , control dimension n _ { u } , MPC horizon T , RL episodes length H, batch size B*

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_bFYfV6c9zu/figures/016_Table_4.jpg]]

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_bFYfV6c9zu/figures/017_Table_5.jpg]]
*Table 5: Nominal vehicle model parameters and controller gains for the baseline MPC policy*

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_bFYfV6c9zu/figures/018_Table_6.jpg]]
*Table 6: Parameters used for domain randomization. On water puddles, tire friction coefficients drop to $\mu$ = 0 . 6*



## 定位与知识库关联

### 核心贡献与瓶颈突破

DiffMPC 的核心贡献在于**首次将最优控制问题（OCP）的时间稀疏结构与预处理共轭梯度法（PCG）结合**，在 GPU 上实现了可微分 MPC 的跨时间步并行化。传统方法（如 iLQR）依赖序列化的 Riccati 递归，其顺序性质天然阻碍了 GPU 上的高效并行——这是该领域的真实瓶颈。DiffMPC 通过将 KKT 系统的求解从 Riccati 递归替换为基于块三对角预处理的 PCG 例程，在不牺牲收敛性的前提下，将这一瓶颈打通。

这一设计的因果杠杆在于：PCG 的每次迭代中，矩阵-向量乘积可以跨时间步并行计算，而 Riccati 递归则必须串行推进。同时，PCG 天然支持跨问题实例的 warm-starting，进一步放大了在 MPC 滚动优化场景下的加速效果。

### 与基线方法的关系

DiffMPC 与三类可微分优化/MPC 求解器形成直接对比：

- **基于 iLQR 的可微分 MPC 求解器**：**mpc.pytorch**（Amos et al., NeurIPS 2018）和 **trajax**（Frostig et al., 2021）均使用 Riccati 递归求解 LQR 子问题，其反向传播通过递归的自动微分实现。DiffMPC 在相同 5 次 SQP/iLQR 迭代限制下，GPU 反向传播速度比 trajax 快约 4 倍（Figure 3, Table 3），且模仿学习训练 wall-clock 时间约快 2 倍（Figure 4）。这一加速源于 PCG 对时间维度的并行化，而非对 iLQR 算法本身的改进。

- **通用可微分非线性最小二乘求解器**：**Theseus**（Pineda et al., 2022）是一个基于 PyTorch 的通用可微分非线性优化框架，支持多种求解器（包括 Levenberg-Marquardt 和 Gauss-Newton）。它不专门针对 OCP 的时间稀疏结构优化，因此在 MPC 场景下 GPU 性能显著弱于 DiffMPC（Table 3 中 Theseus 在 GPU 上的前向/反向传播时间远高于 DiffMPC）。

- **基于 OSQP 的部署方案**：在实车部署中，DiffMPC 训练得到的策略使用 OSQP 而非 PCG 进行在线求解。这是工程上的妥协——PCG 方案尚未在硬件上实时运行，OSQP 提供了更成熟的不等式约束处理能力。这种训练与部署的不一致是该方法的已知局限。

### 方法适用边界

**支持的能力**：
- 无不等式约束的参数化 OCP，包括动力学等式约束和参数化的成本函数
- 前向求解（SQP + PCG + 线搜索）与反向梯度计算（基于隐函数定理的 VJP）均可在 GPU 上高效并行
- 可学习参数 $\theta$ 可嵌入成本函数 $c_t^{x,\theta}, c_t^{u,\theta}$、动力学 $f_t^\theta$ 和初始条件 $x_s^\theta$ 中
- 支持强化学习（RL）和模仿学习（IL）两种学习范式，作为可微分策略组件嵌入更大的学习架构

**不支持的场景**：
- **不等式约束**：当前方法仅支持等式约束的 OCP。虽然论文指出可通过增广拉格朗日法或内点法扩展，但这些方法在约束边界上的梯度不连续性会引入新的可微分性挑战，目前尚未实现
- **非 MPC 的一般非线性优化**：方法强依赖 OCP 的时间链式结构（块三对角 KKT 矩阵），不能直接迁移到任意结构的优化问题
- **实时 GPU 求解**：PCG 方案尚未在硬件上实时运行验证，实车部署回退到 OSQP

### 关键局限

1. **梯度近似的精度损失**：反向传播中忽略了动力学约束的曲率（采用类似 iLQR 的 Gauss-Newton 近似），这可能导致梯度精度下降。消融实验表明，PCG 退出容差在 $10^{-6}$ 以内时，梯度余弦相似度保持在 0.99 以上（Figure 9），但更精确的梯度计算需要完整的 Hessian 信息。

2. **不等式约束的缺失**：这是最显著的功能局限。许多实际 MPC 问题（包括车辆漂移中的轮胎力约束）天然需要不等式约束。论文在实车实验中通过 OSQP 绕过这一问题，但训练阶段的不等式约束微分仍是开放问题。

3. **实车验证的统计显著性不足**：硬件实验仅成功运行一次，结果的可重复性有限。虽然仿真中学习策略达到 100% 成功率（对比基线 70%，Figure 6），但硬件结果的泛化性需要更多实验支撑。

4. **Warm-starting 加速有限**：在低 PCG 退出容差（$10^{-4}$）下，warm-starting 可减少前向传播时间约 11%（Figure 10），但在更严格的容差下加速效果降至约 4%。这意味着 warm-starting 的收益在需要高精度求解时并不显著。

### 开放问题

1. **不等式约束的可微分处理**：如何可靠地对不等式约束进行微分，尤其是在约束边界上梯度不连续时？增广拉格朗日法和内点法的可微分实现需要解决约束激活/非激活状态切换时的梯度传播问题。

2. **稳健初始化策略**：SQP 求解器对初始猜测敏感，发散可能导致训练中断。如何为可微分优化管道提供稳健的初始化，以避免求解器发散？

3. **Warm-starting 的泛化收益**：当前 warm-starting 加速仅在 RL 场景的特定容差下验证。在更广泛的任务（如不同 MPC 结构、更长时域、不同系统动力学）中能提供多大加速？

4. **方法泛化到非 MPC 优化**：能否将 PCG + 时间稀疏结构的思想扩展到更一般的非线性优化问题，而不仅限于 MPC？这需要识别其他具有类似块稀疏结构的优化问题类。

5. **PCG 的实时硬件部署**：直接用 PCG 替代 OSQP 并保持实时性是否可行？PCG 的迭代次数在实时约束下是否可控？这需要在嵌入式 GPU 上进行严格的实时性验证。



## 原文 PDF

![[paperPDFs/ICLR_2026/Differentiable_Model_Predictive_Control_on_the_GPU.pdf]]
