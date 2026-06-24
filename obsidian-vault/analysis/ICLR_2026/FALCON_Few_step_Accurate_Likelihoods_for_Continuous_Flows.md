---
title: "FALCON: Few-step Accurate Likelihoods for Continuous Flows"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/FALCON_Few_step_Accurate_Likelihoods_for_Continuous_Flows.pdf
openreview_forum_id: FbssShlI4N
aliases:
- FFSALCF
- FALCON
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "通过引入一种混合训练目标，将流匹配损失与可逆性一致性损失相结合，使少步离散流映射在训练过程中获得数值可逆性，从而实现快速且准确的似然评估。"
primary_logic: "只要离散流映射是数值可逆的，即使未完美匹配原始连续时间流，也能通过变量替换公式精确计算似然，因此仅需少数步骤即可在重要性采样中达到与自适应CNF求解器相同的样本质量，从而获得两个数量级的速度提升。"
claims:
- "FALCON 比同等性能的基于CNF的玻尔兹曼生成器快两个数量级。"
- "FALCON 在所有评估指标上均优于当前最先进的离散归一化流玻尔兹曼生成器（SBG），且仅使用其1/250的样本量。"
- "仅通过最小化可逆性损失便足以保证离散流映射的可逆性，无需恢复原始连续时间流。"
- "在较大的分子系统（丙氨酸三肽、四肽、六肽）上，FALCON 在能量 Wasserstein 距离和扭转角 Wasserstein 距离上显著优于 ECNF++ 等连续流基线。"
---

# FALCON: Few-step Accurate Likelihoods for Continuous Flows

> [!tip] 核心洞察
> 只要离散流映射是数值可逆的，即使未完美匹配原始连续时间流，也能通过变量替换公式精确计算似然，因此仅需少数步骤即可在重要性采样中达到与自适应CNF求解器相同的样本质量，从而获得两个数量级的速度提升。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | FALCON：连续流的少步精确似然方法 |
| 英文题名 | FALCON: Few-step Accurate Likelihoods for Continuous Flows |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=FbssShlI4N); [GitHub](https://github.com/danyalrehman/FALCON) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | FALCON (Few-step Accurate Likelihoods for Continuous Flows) |
| Dataset | Tri-alanine (AL3), Alanine tetrapeptide (AL4), Hexa-alanine (AL6) |

> [!tip] 效果简介
> - Tri-alanine (AL3) 上，ε-W2 (能量2-瓦瑟斯坦距离，↓) 为 0.544 ± 0.013 (FALCON)，对比 2.206 ± 0.813 (ECNF++)，变化 -1.662。
> - Alanine tetrapeptide (AL4) 上，ε-W2 (↓) 为 0.686 ± 0.047 (FALCON)，对比 5.638 ± 0.483 (ECNF++)，变化 -4.952。
> - Hexa-alanine (AL6) 上，ε-W2 (↓) 为 0.892 ± 0.311 (FALCON)，对比 10.668 ± 0.285 (ECNF++)，变化 -9.776。

## 概述

**核心问题**：基于连续归一化流（CNF）的玻尔兹曼生成器在计算似然时，需要数千步精确的ODE积分与雅可比计算，这种极高的计算开销严重限制了其在大规模分子采样中的应用。

**方法定位**：FALCON（Few-step Accurate Likelihoods for Continuous Flows）提出了一种混合训练策略，将流匹配损失与可逆性一致性损失相结合，使少步离散流映射在训练过程中获得数值可逆性。核心洞见在于：只要离散流映射是数值可逆的，即使未完美匹配原始连续时间流，也能通过变量替换公式精确计算似然——这从根本上摆脱了对数千步ODE求解器的依赖。

**关键结果**：
- FALCON比同等性能的CNF玻尔兹曼生成器快两个数量级（Fig. 2）。
- 在丙氨酸三肽、四肽、六肽等较大分子系统上，FALCON在能量Wasserstein距离和扭转角Wasserstein距离上显著优于ECNF++等连续流基线（Table 3），例如在六肽上能量Wasserstein距离从10.668降至0.892。
- FALCON在所有评估指标上均优于当前最先进的离散归一化流玻尔兹曼生成器（SBG），且仅使用其1/250的样本量。

## 背景与动机

### 玻尔兹曼生成器的核心挑战

分子系统的统计力学性质依赖于对玻尔兹曼分布

$$p_{\mathrm{target}}(x) \propto \exp(-\mathcal{E}(x))$$

的准确采样，其中 $\mathcal{E}(x)$ 为势能函数，配分函数 $\mathcal{Z} = \int_{\mathbb{R}^d} \exp(-\mathcal{E}(x)) dx$ 通常无法解析计算。玻尔兹曼生成器（Boltzmann Generators）通过训练归一化流将简单先验分布映射到目标分布，并利用自归一化重要性采样（SNIS）进行可观测量估计：

$$\mathbb{E}_{p_{\mathrm{target}}}[o(x)] \approx \frac{\sum_{i=1}^K w(x^i) o(x^i)}{\sum_{i=1}^K w(x^i)}$$

然而，这一范式面临一个根本性瓶颈：**基于连续归一化流（CNF）的方法在计算似然时需要数千步精确的ODE积分与雅可比计算**。具体而言，CNF需沿连续时间轨迹积分瞬时变量替换公式：

$$\log p_s^\theta(x_s) = \int_0^s v_\theta(x_\tau, \tau) d\tau$$

即使采用自适应求解器（如Dormand–Prince 4(5)）并将容限设为 atol=rtol=10⁻⁵，单次似然评估仍需数百至数千步函数评估，严重限制了其在大规模分子系统中的应用。

### 现有方法的缺口

当前玻尔兹曼生成器可分为两条技术路线：

- **连续流方法**（如 **ECNF** (Klein et al., 2023)、**ECNF++** (Tan et al., 2025a)、**BoltzNCE** (Aggarwal et al., 2025)）：通过流匹配（Conditional Flow Matching）训练CNF，能够精确计算似然，但推理速度极慢，难以扩展到丙氨酸六肽等较大系统。
- **离散归一化流方法**（如 **SBG** (Tan et al., 2025a)、**SE(3)-EACF** (Midgley et al., 2023)）：使用耦合层等架构实现快速采样，但缺乏精确的似然计算能力，在重要性采样效率上显著落后于连续流方法。

这种“速度-精度”困境构成了领域内的核心矛盾：连续流精确但缓慢，离散流快速但粗糙。

### FALCON的动机与核心洞察

FALCON的提出基于一个关键洞察：**只要离散流映射 $X_u(x_s, s, t) = x_s + (t-s) u_\theta^\star(x_s, s, t)$ 是数值可逆的，即使未完美匹配原始连续时间流，也能通过精确变量替换公式在每个离散步长上计算似然**。这意味着可以通过少数步骤（如4–16步）实现与自适应CNF求解器相同的样本质量，从而获得两个数量级的速度提升（Fig. 2）。

为实现这一目标，FALCON引入混合训练目标：

$$\mathcal{L}(\theta) = \mathcal{L}_{\mathrm{cfm}}(\theta) + \lambda_{\mathrm{avg}} \mathcal{L}_{\mathrm{avg}}(\theta) + \lambda_r \mathcal{L}_{\mathrm{inv}}(\theta)$$

其中流匹配损失 $\mathcal{L}_{\mathrm{cfm}}$ 保证生成质量，平均速度损失 $\mathcal{L}_{\mathrm{avg}}$ 稳定少步生成，循环一致性可逆性损失

$$\mathcal{L}_{\mathrm{inv}}(\theta) = \mathbb{E}_{s,t,x_s} \| x_s - X_u(X_u(x_s, s, t), t, s) \|^2$$

强制离散流映射获得数值可逆性，从而使少步似然计算成为可能。

## 核心创新

FALCON 的核心创新在于用一套**混合训练范式**替代了传统连续归一化流（CNF）的端到端积分范式，从而在保持精确似然计算能力的同时，将推理所需的函数评估次数从数千步压缩至 4–16 步，实现了两个数量级的速度提升。这一突破可拆解为三个紧密耦合的 changed slots。

### 1. 训练目标：从单一流匹配到混合可逆性约束

传统 CNF 玻尔兹曼生成器（如 **ECNF++** (Tan et al., 2025a)、**ECNF** (Klein et al., 2023)）仅依赖流匹配（Conditional Flow Matching, CFM）损失来学习连续时间向量场 $v(x_\tau, \tau)$。FALCON 则引入了一个三合一的混合损失（Eq. 9）：

$$\mathcal{L}(\theta) = \mathcal{L}_{\mathrm{cfm}}(\theta) + \lambda_{\mathrm{avg}} \mathcal{L}_{\mathrm{avg}}(\theta) + \lambda_r \mathcal{L}_{\mathrm{inv}}(\theta)$$

其中两个新增项各自承担关键功能：

- **平均速度损失 $\mathcal{L}_{\mathrm{avg}}$**：训练网络直接预测区间 $[s, t]$ 内的**平均速度** $u_\theta(x_s, s, t)$，而非瞬时速度。这使得模型天然适配大步长离散映射，避免了连续时间积分在少步设置下的数值误差累积。
- **可逆性损失 $\mathcal{L}_{\mathrm{inv}}$**：通过最小化往返重构误差 $\|x_s - X_u(X_u(x_s, s, t), t, s)\|^2$（Eq. 8），强制离散流映射 $X_u$ 在训练过程中获得**数值可逆性**。这一设计的核心洞察在于：只要离散映射可逆，即使它未完美复现原始连续时间流，也能通过变量替换公式精确计算似然（Proposition 2）。

消融实验（Fig. 6）表明，适中的正则化系数 $\lambda_r=10^1$ 在有效样本量（ESS）和能量 Wasserstein 距离（$\varepsilon$-W2）上达到最佳平衡——过弱则无法保证可逆性，过强则会损害生成质量。

### 2. 似然计算：从 ODE 积分到离散变量替换

传统 CNF 的似然计算依赖沿连续时间轨迹的 ODE 积分（瞬时变量替换公式），需配合自适应求解器（如 Dormand–Prince 4(5)）进行数千步函数评估，且每步需计算雅可比迹。FALCON 将这一过程替换为每个离散步长上的精确变量替换公式，总计算量仅为 $N \cdot d$ 次函数评估（$N=4\text{–}16$ 步，$d$ 为数据维度）。这一改变直接消除了 CNF 似然计算的核心计算瓶颈，是 Fig. 2 中两个数量级加速的直接来源。

### 3. 网络架构：从小型等变网络到可扩展 DiT

连续流基线（如 ECNF++）通常采用小型 SE(3)-等变网络（如 EGNN）以保证物理对称性。FALCON 则转向可扩展的**扩散 Transformer（DiT）**骨干网络，并通过数据增强实现软 SO(3) 旋转等变性。这一架构切换的意义在于：DiT 的高容量使得网络能够在少步约束下学习更复杂的离散映射，而数据增强策略则以较低的计算代价维持了必要的物理对称性。这一选择与混合损失设计形成协同——强正则化的可逆性约束需要足够的模型容量来容纳，而 DiT 恰好提供了这种容量。

### 方法定位

相较于离散归一化流基线（如 **SBG** (Tan et al., 2025a) 使用的 TARFlow），FALCON 的关键区别在于**显式保证了离散映射的可逆性**，从而使得似然计算在数学上严格成立，而非依赖重要性采样的渐近性质。这解释了为何即使 SBG 使用 250 倍样本量（$5\times10^6$ vs $2\times10^5$），其在 $\varepsilon$-W2 上的表现仍显著劣于 4 步 FALCON（Fig. 4）。

## 整体框架

FALCON 的整体框架围绕一个核心思想构建：**在离散步骤中实现数值可逆的流映射，从而绕过连续归一化流（CNF）数千步的 ODE 积分，以极少的函数评估次数完成精确的似然计算**。

### 框架总览

FALCON 的 pipeline 由训练和推理两个阶段构成，其模块关系如下：

1.  **前向离散流映射** $X_u$：将样本从先验分布 $p_0$（如标准高斯）通过 $N$ 个离散步骤映射到目标数据分布。每个步骤由学习到的平均速度网络 $u_\theta$ 参数化。给定起始时间 $s$、终止时间 $t$ 和当前状态 $x_s$，映射定义为：
    $$X_u(x_s, s, t) = x_s + (t-s) u_\theta(x_s, s, t)$$
    推理时，通过组合 $N$ 个这样的离散步骤（例如 $N=4$–$16$），即可完成从噪声到分子构象的生成。

2.  **平均速度网络** $u_\theta$：网络的输入为当前状态 $x_s$ 和时间区间 $[s, t]$，输出为该区间内的平均速度向量。FALCON 采用可扩展的扩散 Transformer（DiT）作为骨干网络，并通过数据增强实现软 SO(3) 旋转等变性，从而摆脱了传统 CNF 玻尔兹曼生成器对小型等变网络（如 EGNN）的依赖。

3.  **混合训练目标**：训练损失由三项组成，共同作用于上述离散映射：
    $$\mathcal{L}(\theta) = \mathcal{L}_{\text{cfm}}(\theta) + \lambda_{\text{avg}} \mathcal{L}_{\text{avg}}(\theta) + \lambda_r \mathcal{L}_{\text{inv}}(\theta)$$
    - **流匹配损失** $\mathcal{L}_{\text{cfm}}$：提供基础的生成建模能力，使离散映射的轨迹逼近连续时间流。
    - **平均速度损失** $\mathcal{L}_{\text{avg}}$：稳定少步生成过程，通过单个雅可比向量乘积（JVP）高效实现。
    - **可逆性正则化损失** $\mathcal{L}_{\text{inv}}$：强制离散映射的数值可逆性。其形式为循环一致性损失：
      $$\mathcal{L}_{\text{inv}}(\theta) = \mathbb{E}_{s,t,x_s} \| x_s - X_u(X_u(x_s, s, t), t, s) \|^2$$
      该损失确保映射在前向和反向传播后能恢复原始输入，从而使变量替换公式在少步离散设置下依然能够精确计算似然。

4.  **自适应推理调度器**：推理时，时间步的分配策略对生成质量有显著影响。FALCON 采用 EDM 调度器（Karras et al., 2022）来分配 $N$ 个推理步长，该调度器在所有评估指标上均显著优于线性、几何、余弦和切比雪夫调度器（Fig. 7）。

### 输入输出流

- **训练阶段**：输入为来自偏置数据集（如短时 MD 模拟轨迹）的分子构象样本。网络 $u_\theta$ 学习将先验噪声映射到这些训练样本，同时通过 $\mathcal{L}_{\text{inv}}$ 保证映射的可逆性。
- **推理阶段**：从先验分布采样噪声，通过 $N$ 步离散映射 $X_u$ 生成候选构象。随后，利用自归一化重要性采样（SNIS）对这些候选构象进行重加权：
  $$\mathbb{E}_{p_{\text{target}}}[o(x)] \approx \frac{\sum_{i=1}^K w(x^i) o(x^i)}{\sum_{i=1}^K w(x^i)}$$
  其中重要性权重 $w(x)$ 由变量替换公式精确计算，无需数值 ODE 积分。最终输出为与目标玻尔兹曼分布一致的样本及可观测量估计。

### 方法谱系与知识库定位

FALCON 处于连续流与离散流方法的交叉点。表 1 从可逆性、回归损失、少步能力和自由形式架构四个维度总结了相关工作的定位。

**表 1: 相关方法概览**

| 方法 | 可逆性 | 回归损失 | 少步能力 | 自由形式架构 |
|------|--------|----------|----------|-------------|
| FALCON (本文) | ✓ | ✓ | ✓ | ✓ |
| ECNF++ (Tan et al., 2025a) | 连续时间可逆 | ✗ | ✗ | ✗ |
| SBG (Tan et al., 2025a) | ✗ | ✗ | ✓ | ✗ |
| RegFlow (Rehman et al., 2025) | ✗ | ✓ | ✓ | ✓ |

与传统 CNF 玻尔兹曼生成器（如 **ECNF** (Klein et al., 2023)、**ECNF++** (Tan et al., 2025a)）相比，FALCON 将似然计算从数千步的自适应 ODE 求解（Dormand–Prince 4(5)，atol=rtol=$10^{-5}$）压缩为 $N \cdot d$ 次函数评估（$N$ 为步数，$d$ 为数据维度），实现了两个数量级的速度提升（Fig. 2）。与离散归一化流玻尔兹曼生成器（如 **SBG** (Tan et al., 2025a)）相比，FALCON 通过引入可逆性损失，使离散映射具备了精确的似然计算能力，从而在重要性采样效率上形成质的差距——即使 SBG 使用 250 倍于 FALCON 的样本量，其在能量 Wasserstein 距离上的表现仍显著逊于 4 步 FALCON（Fig. 4）。

**关键洞察**：FALCON 的成功并不依赖于离散映射完美复现原始连续时间流，而仅需保证映射的数值可逆性。这一洞察将问题从"逼近连续流"转化为"保证局部可逆性"，使得少步推理成为可能，同时保持了似然计算的精确性。

## 核心模块与公式推导

### 离散流映射与可逆性条件

FALCON 的核心创新在于将传统连续归一化流（CNF）的 ODE 积分替换为**少步离散流映射**，同时通过训练保证其数值可逆性，从而绕过高昂的连续时间似然计算。

给定概率流 ODE 的向量场 $v(x_\tau, \tau)$，定义区间 $[s, t]$ 上的**连续流映射**为：

$$X_v(x_s, s, t) = \int_s^t v(x_\tau, \tau) d\tau + x_s$$

FALCON 不直接学习 $v$，而是学习该区间上的**平均速度**：

$$u(x_s, s, t) = \frac{1}{t-s}\int_s^t v(x_\tau, \tau) d\tau$$

由此构建的**离散流映射**为：

$$X_u(x_s, s, t) = x_s + (t-s) u_\theta^\star(x_s, s, t)$$

其中 $u_\theta^\star$ 是训练收敛后的平均速度网络。该映射的雅可比行列式可通过标准自动微分精确计算，无需 ODE 求解器的数千步积分。

**核心洞察**：只要 $X_u$ 是数值可逆的，即使它未完美匹配原始连续流 $X_v$，仍可通过变量替换公式精确计算似然。这一定理基础支撑了 FALCON 的少步似然评估能力。

---

### 混合训练目标

FALCON 的训练目标由三项损失函数加权组合而成：

$$\mathcal{L}(\theta) = \mathcal{L}_{\mathrm{cfm}}(\theta) + \lambda_{\mathrm{avg}} \mathcal{L}_{\mathrm{avg}}(\theta) + \lambda_r \mathcal{L}_{\mathrm{inv}}(\theta)$$

#### 1. 流匹配损失 $\mathcal{L}_{\mathrm{cfm}}$

标准条件流匹配（Conditional Flow Matching）损失，用于学习从先验分布到目标数据分布的条件概率路径，为模型提供基本的生成能力。

#### 2. 平均速度损失 $\mathcal{L}_{\mathrm{avg}}$

$$\mathcal{L}_{\mathrm{avg}} \triangleq \mathbb{E}_{s,t,x_s} \left\| u_\theta(x_s, s, t) - \mathrm{sg}\left( v(x_s, s) - (t-s)\left( v(x_s, s)^\top \nabla \right) v(x_s, s) \right) \right\|^2$$

该损失等价于 **MeanFlow** 损失（Geng et al., 2025a），其作用是使网络 $u_\theta$ 直接回归到区间 $[s, t]$ 上的真实平均速度。$\mathrm{sg}(\cdot)$ 表示停止梯度算子，$v(x_s, s)$ 是时间 $s$ 处的瞬时向量场。

**高效实现**：$\mathcal{L}_{\mathrm{avg}}$ 可通过**单次雅可比向量乘积（JVP）** 调用实现，利用前向自动微分同时计算 $u_\theta$ 及其对 $s$ 的导数：

$$u_\theta(x_s, s, t), \frac{du_\theta}{ds} = \mathrm{jvp}(u_\theta, (x_s, s, t), (v_s, 1, 0))$$

这避免了显式计算完整的 Hessian 矩阵，显著降低了训练开销。

#### 3. 可逆性正则化损失 $\mathcal{L}_{\mathrm{inv}}$

$$\mathcal{L}_{\mathrm{inv}}(\theta) = \mathbb{E}_{s,t,x_s} \| x_s - X_u(X_u(x_s, s, t), t, s) \|^2$$

该损失是一个**循环一致性项**：将样本 $x_s$ 从时间 $s$ 映射到 $t$，再从 $t$ 映射回 $s$，最小化往返重构误差。它强制离散流映射在训练过程中获得局部可逆性，而无需恢复完整的连续时间流。消融实验表明，仅通过最小化此损失便足以保证可逆性（Proposition 2），但适中的正则化系数（$\lambda_r = 10^1$）才能在有效样本量（ESS）和能量瓦瑟斯坦距离（$\varepsilon$-W2）之间取得最佳平衡——过弱则无法保证可逆性，过强则损害生成质量。

---

### 似然计算：从 ODE 积分到变量替换

传统 CNF 的似然计算依赖瞬时变量替换公式的 ODE 积分：

$$\log p_s^\theta(x_s) = \int_0^s \mathrm{Tr}\left[ \nabla v_\theta(x_\tau, \tau) \right] d\tau$$

这需要数千步的数值积分与雅可比迹估计。FALCON 将推理过程离散为 $N$ 步（$N=4\sim 16$），在每个离散步长上应用精确的变量替换公式，仅需 $N \cdot d$ 次函数评估（$d$ 为数据维度），从而获得两个数量级的速度提升。

---

### 推理调度器

FALCON 支持后验调整推理步数，并通过不同的时间步分配策略优化性能。消融实验表明，在 8 步推理设置下，**EDM 调度器**（Karras et al., 2022）在所有评估指标上均显著优于线性、几何、余弦和切比雪夫调度器，这与扩散模型文献中的观察一致。

## 实验与分析

### 主实验结果

FALCON 在丙氨酸二肽（AL2）及更大的分子系统上均表现出显著优势。在 AL2 上，FALCON 在有效样本量（ESS）、能量 Wasserstein 距离（ε-W2）和扭转角 Wasserstein 距离（T-W2）三项指标上均取得最优或次优结果（Table 2），且推理速度比同等性能的 CNF 基线快两个数量级（Figure 2）。

在更大分子系统上，FALCON 的可扩展性优势更为突出。如 Table 3 所示，在丙氨酸三肽（AL3）、四肽（AL4）和六肽（AL6）上，FALCON 的 ε-W2 分别达到 0.544、0.686 和 0.892，而基于 CNF 的 ECNF++（Tan et al., 2025a）在相同系统上的 ε-W2 分别为 2.206、5.638 和 10.668，差距随分子尺寸增大而急剧扩大。这一趋势表明，CNF 基线的 ODE 积分误差在大系统中累积更为严重，而 FALCON 的少步离散映射通过数值可逆性有效规避了这一问题。

与离散归一化流基线 SBG（Tan et al., 2025a）的对比进一步凸显 FALCON 的效率优势。即使将 SBG 的样本量增加至 $5 \times 10^6$（FALCON 评估样本量的 250 倍），其 ε-W2 仍显著劣于 4 步 FALCON（Figure 4）。这说明 SBG 所依赖的标准重要性采样在提案分布与目标分布差异较大时效率低下，而 FALCON 通过可逆流映射生成的提案分布更接近真实玻尔兹曼分布。

### 与自适应 CNF 求解器的对比

Table 5 展示了 FALCON 与使用 Dormand–Prince 4(5) 自适应求解器的 CNF 的详细对比。FALCON 仅需 4–16 次函数评估（NFE）即可达到与自适应 CNF（通常需要数千 NFE）相当的样本质量。例如，在 AL6 上，FALCON 以 16 NFE 取得 ε-W2 = 0.892，而同等 DiT 骨干的自适应 CNF 需约 2000 NFE 才能达到相近性能。这一对比直接验证了核心论断：只要离散流映射数值可逆，即使未完美恢复原始连续时间流，仍可通过变量替换公式精确计算似然。

### 消融实验

**可逆性正则化强度**。Figure 6 展示了正则化系数 $\lambda_r$ 对性能的影响。在 $\lambda_r = 10^1$ 时，ESS 和 ε-W2 达到最佳平衡。过弱的正则化（$\lambda_r \leq 10^0$）无法保证离散映射的可逆性，导致似然计算失效；过强的正则化（$\lambda_r \geq 10^2$）则过度约束网络，损害生成质量。这一消融验证了命题 2（Section 3）的论断：仅通过最小化可逆性损失便足以保证离散流映射的可逆性，但正则化强度需谨慎选择。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_FbssShlI4N/figures/011_Figure_6.jpg]]
*Figure 6: Performance trade-off with increasing regularization*

**推理调度器**。Figure 7 比较了线性、几何、余弦、切比雪夫和 EDM 五种调度器在 8 步推理下的表现。EDM 调度器在所有评估指标上均显著优于其他调度器，这与扩散模型文献中的观察一致（Karras et al., 2022）。EDM 调度器的优势在于其时间步分配策略能更好地适应流映射的局部曲率变化。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_FbssShlI4N/figures/012_Figure_7.jpg]]
*Figure 7: Performance vs. choice of inference schedule*

**推理步数**。Figure 5 显示，将推理步数从 8 步减少至 4 步会导致 ε-W2 上升，但 FALCON 仍可维持可比的质量水平。这一特性使得用户可在推理速度与样本质量之间进行后验权衡，无需重新训练模型。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_FbssShlI4N/figures/010_Figure_5.jpg]]
*Figure 5: Improved proposal and re-weighted sample energies with increased steps for alanine dipeptide*

### 计算效率

Table 4 汇总了训练与推理的累计时间。在 AL2 上，FALCON 的累计时间为 7.65 小时，而 CNF 基线需数十小时。随着分子尺寸增大，FALCON 的效率优势进一步扩大：在 AL6 上，FALCON 仅需 25.76 小时，而 CNF 基线的 ODE 积分开销使其累计时间远超此值。所有实验均在 NVIDIA L40S 上以 batch size 1024 进行，确保了对比的公平性。

### 能量分布定性分析

Figure 3 展示了 FALCON 生成样本在重要性采样前后的能量直方图与真实 MD 分布的对比。在 AL2 至 AL6 四个系统上，FALCON 的未加权提案分布已接近真实分布，经 SNIS 重加权后几乎完全吻合。这表明 FALCON 学到的流映射能有效将简单先验分布传输至复杂的多模态玻尔兹曼分布，且重要性权重的方差较低，从而保证了 ESS 的高效性。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_FbssShlI4N/figures/006_Figure_3.jpg]]
*Figure 3: True MD energy distribution with best FALCON unweighted and re-sampled proposals for alanine dipeptide (left), tri-alanine (center left), and alanine tetrapeptide (center right), and hexa-alanine (right)*

### 补充图表

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_FbssShlI4N/figures/014_Figure_8.jpg]]
*Figure 8: Left: Training data for alanine dipeptide; Right: Test data for alanine dipeptide*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_FbssShlI4N/figures/015_Figure_9.jpg]]
*Figure 9: Left and left center: Training data for tri-alanine; Right center and right: Test data for tri-alanine*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_FbssShlI4N/figures/016_Figure_11.jpg]]
*Figure 11: First five: Training data for hexa-alanine; Last three: Test data for hexa-alanine*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_FbssShlI4N/figures/017_Figure_10.jpg]]
*Figure 10: First three: Training data for alanine tetrapeptide; Last three: Test data for alanine tetrapeptide*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_FbssShlI4N/figures/020_Figure_14.jpg]]
*Figure 14: Left: Test data for alanine dipeptide; Right: FALCON’s angular predictions for alanine dipeptide*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_FbssShlI4N/figures/021_Figure_15.jpg]]
*Figure 15: Left and left center: Test data for tri-alanine; Right and right center: FALCON’s angular predictions for tri-alanine*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_FbssShlI4N/figures/022_Figure_16.jpg]]
*Figure 16: First three: Test data for alanine tetrapeptide; Last three: FALCON’s angular predictions for alanine tetrapeptide*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_FbssShlI4N/figures/003_Table_1.jpg]]
*Table 1: Related method overview*

## 方法谱系与知识库定位

### 1. 方法关系图谱

FALCON 处于连续归一化流（CNF）与离散归一化流（NF）的交叉地带，其核心设计思路是对两类方法的瓶颈进行拆解与重组。

**与连续流（CNF）的关系**。传统基于 CNF 的玻尔兹曼生成器——如 **ECNF** (Klein et al., 2023)、**ECNF++** (Tan et al., 2025a) 和 **BoltzNCE** (Aggarwal et al., 2025)——依赖数千步自适应 ODE 求解器（Dormand–Prince 4(5)）进行似然计算，每次评估需执行雅可比迹估计，计算开销极大。FALCON 保留了 CNF 的概率流 ODE 框架，但将连续时间积分替换为少数离散步骤上的精确变量替换公式，从而将函数评估次数从数千次压缩至 4–16 次。这一替换之所以可行，关键在于 FALCON 不要求离散流映射精确恢复原始连续时间流，而仅要求其具备**数值可逆性**——这正是 Proposition 2 (Section 3) 的核心理论保证。

**与离散归一化流（NF）的关系**。当前最先进的离散 NF 玻尔兹曼生成器 **SBG** (Tan et al., 2025a) 基于 TARFlow 架构，配合标准重要性采样（SBG IS）或序贯蒙特卡洛采样（SBG SMC）。SBG 在丙氨酸二肽上表现良好，但其性能在大规模采样预算下存在天花板：即使将样本量提升至 5×10⁶（FALCON 评估样本量的 250 倍），SBG 在能量 Wasserstein 距离（ε-W2）上仍显著劣于 4 步 FALCON（Fig. 4）。FALCON 的优势源于其流映射的可逆性保证，这使其似然计算在理论上精确，而离散 NF 的似然近似质量受限于网络架构的表达能力。

**与回归流方法的关系**。**RegFlow** (Rehman et al., 2025) 和 **SE(3)-EACF** (Midgley et al., 2023) 等基于回归的流方法也追求少步生成能力，但通常缺乏可逆性保证或似然可计算性。FALCON 通过混合训练目标——流匹配损失 $\mathcal{L}_{\mathrm{cfm}}$ + 平均速度预测损失 $\mathcal{L}_{\mathrm{avg}}$ + 循环一致性可逆性损失 $\mathcal{L}_{\mathrm{inv}}$（Eq. 9）——首次在少步离散流中同时实现了可逆性与精确似然计算，填补了这一空白。

### 2. 关键设计选择的因果链路

FALCON 的性能增益可追溯至三个相互耦合的设计选择：

- **混合训练目标**。$\mathcal{L}_{\mathrm{cfm}}$ 提供基本的流匹配信号，$\mathcal{L}_{\mathrm{avg}}$ 引导网络学习区间平均速度以稳定少步离散映射，$\mathcal{L}_{\mathrm{inv}}$ 通过最小化往返重构误差强制局部可逆性。消融实验表明，适中的可逆性正则化系数 $\lambda_r = 10^1$ 在有效样本量（ESS）和 ε-W2 上达到最佳平衡——过弱（$\lambda_r \leq 10^0$）无法保证可逆性，过强（$\lambda_r \geq 10^2$）则损害生成质量（Fig. 6）。

- **可扩展架构**。FALCON 采用扩散 Transformer（DiT）作为骨干网络，并通过数据增强实现软 SO(3) 旋转等变性。这与 ECNF++ 等基线使用的小型等变网络（如 EGNN）形成对比，使 FALCON 能够利用更大的模型容量处理丙氨酸六肽等复杂分子系统。

- **推理调度器**。在 8 步推理设置下，EDM 调度器（Karras et al., 2022）在所有评估指标上显著优于线性、几何、余弦和切比雪夫调度器（Fig. 7），表明时间步的非均匀分配对少步流映射的质量至关重要。

### 3. 适用边界与局限

- **步数-质量权衡**。减少推理步数（如从 8 步降至 4 步）会导致能量 Wasserstein 距离上升（Fig. 5），说明 FALCON 在极端少步场景（如单步生成）下仍存在质量退化。论文未探索是否可通过架构改进实现真正的单步生成。

- **可逆性的理论保证**。FALCON 的可逆性来自循环一致性损失的经验最小化，而非严格的数学构造。在分布的低密度区域或远离训练数据的区域，离散流映射的数值可逆性可能无法保证，这会影响重要性采样权重的准确性。论文未提供可逆性违反的定量检测机制。

- **领域泛化**。当前评估限于丙氨酸肽系列分子系统（二肽至六肽）。FALCON 在其他玻尔兹曼生成器应用场景（如蛋白质、材料科学、贝叶斯推断）中的表现有待验证。

### 4. 开放问题

1. **单步生成可行性**：是否可以通过更强的可逆性约束或蒸馏策略实现真正的一步精确似然计算？
2. **可逆性认证**：如何在不依赖经验验证的情况下，高效地为离散流映射的数值可逆性提供理论保证或运行时检测？
3. **跨领域迁移**：FALCON 在贝叶斯推断、机器人学等非分子领域的表现如何？其混合训练目标是否需要领域特定的调整？

## 原文 PDF

![[paperPDFs/ICLR_2026/FALCON_Few_step_Accurate_Likelihoods_for_Continuous_Flows.pdf]]
