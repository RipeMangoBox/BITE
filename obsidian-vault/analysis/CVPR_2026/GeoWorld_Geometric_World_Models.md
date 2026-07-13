---
title: "GeoWorld: Geometric World Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GeoWorld_Geometric_World_Models.pdf
project_link: "https://steve-zeyu-zhang.github.io/GeoWorld"
code_link: null
aliases:
- GeoWorld
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 通过Hyperbolic JEPA将潜在表示映射到双曲流形，利用测地距离自然编码层次关系；并通过Geometric Reinforcement Learning在双曲潜在空间中最小化能量值函数，强制执行测地一致性和三角不等式正则化。
primary_logic: 双曲几何天生适合表示层次化状态结构，将世界模型的潜在动力学约束在双曲测地线上，能够产生结构化、曲率感知的能量景观，从而稳定长时域规划。
claims:
- GeoWorld 产生结构化、曲率感知的能量景观，更好地反映了几何结构与层次关系（图2对比）
- GeoWorld 在 Gromov δ-双曲性上分布更集中，表明学习到的潜在空间具有更强的树状层次几何（图1附录）
- 长时域规划中，完整模型 (SFT+GRL) 在 T=8 时 SR 13.81，远超 V-JEPA 2 的 4.95（表5）
- CrossTask (videos) 上 Success Rate (T=3) = 51.71
---

# GeoWorld: Geometric World Models

> [!tip] 核心洞察
> 双曲几何天生适合表示层次化状态结构，将世界模型的潜在动力学约束在双曲测地线上，能够产生结构化、曲率感知的能量景观，从而稳定长时域规划。

| 字段 | 内容 |
|------|------|
| 中文题名 | GeoWorld: 几何世界模型 |
| 英文题名 | GeoWorld: Geometric World Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.23058) · [Project](https://steve-zeyu-zhang.github.io/GeoWorld) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | GeoWorld |
| Dataset | CrossTask, COIN |

> [!tip] 效果简介
> - CrossTask (videos) 上，Success Rate (T=3) 51.71 vs 50.16 (V-JEPA 2 ViT-g384) (+1.55)；Success Rate (T=4) 37.04 vs 35.01 (V-JEPA 2 ViT-g384) (+2.03)。
> - COIN (videos) 上，Success Rate (T=3) 45.29 vs 42.74 (V-JEPA 2 ViT-g384) (+2.55)。
> - CrossTask (images, procedural planning) 上，Success Rate (T=3) 47.47 vs 45.58 (V-JEPA 2 ViT-g384) (+1.89)。

## 概要

预测世界模型通过学习环境的潜在动力学来实现视觉规划，但现有方法（如 **V-JEPA 2**）在欧几里得空间中建模潜在表示，忽略了状态间固有的几何与层次结构。这导致两个关键瓶颈：其一，能量景观无法捕获有意义的测地距离，难以反映状态间的层次化组织关系；其二，多步预测性能随规划步长增加而快速退化——在 CrossTask 数据集上，V-JEPA 2 从 T=3 的成功率 50.16 骤降至 T=8 的仅 4.95（表5）。

**GeoWorld** 针对上述瓶颈提出了一个几何世界模型框架，其核心洞察在于：双曲几何天生适合表示层次化状态结构。通过将世界模型的潜在动力学约束在双曲测地线上，能够产生结构化、曲率感知的能量景观，从而稳定长时域规划。方法上，GeoWorld 通过两个关键模块实现这一目标：

- **Hyperbolic JEPA (H-JEPA)**：将冻结编码器输出的欧几里得表示通过指数映射投影到 Poincaré 球双曲流形，利用测地距离自然编码状态间的层次关系。
- **Geometric Reinforcement Learning (GRL)**：在双曲潜在空间中定义能量成本为测地距离，通过最小化双曲能量值函数并强制执行三角不等式正则化，直接优化预测器的多步一致性。

在 CrossTask 和 COIN 数据集上的目标条件视觉规划实验中，GeoWorld 相比 V-JEPA 2 取得了约 3%（T=3）和 2%（T=4）的成功率提升。消融实验表明，SFT 与 GRL 发挥互补作用——SFT 稳定短期预测，GRL 增强长时域 rollout 一致性，二者结合在 T=8 长时域规划中达到 13.81 的成功率，远超 V-JEPA 2 的 4.95。定性分析显示，GeoWorld 产生的能量景观具有清晰的结构化特征，其潜在空间的 Gromov δ-双曲性分布更集中，验证了学习到的表示具有更强的树状层次几何特性。

### 预测世界模型与视觉规划

基于模型的视觉规划旨在让智能体在潜在空间中模拟未来状态，从而选择最优动作序列。近年来，以 V-JEPA 2 为代表的预测型世界模型（predictive world models）取得了显著进展：它们通过冻结的视觉编码器将观测映射到欧几里得潜在空间，再利用动作条件预测器进行多步前向推演，并借助交叉熵方法（CEM）在能量景观上搜索最优动作。这种“编码-预测-规划”的流水线避免了像素级生成的高昂成本，在 CrossTask 和 COIN 等过程规划基准上展现了竞争力。

### 核心瓶颈：欧几里得空间的几何与层次盲区

然而，现有预测世界模型存在一个根本性局限：**它们完全在欧几里得空间中学习潜在表示，忽略了状态间固有的几何与层次结构**。这导致两个连锁问题：

1. **能量景观缺乏结构化信息**。欧几里得距离作为能量度量时，无法捕获状态之间的测地距离——即沿着数据流形的真实最短路径。由此产生的能量景观是平坦且无结构的，难以反映任务中天然存在的层次关系（例如“更换内存芯片”任务包含“打开机箱→移除旧芯片→插入新芯片→合上机箱”的递进子目标结构）。

2. **多步预测性能随规划步长急剧退化**。当规划时域 T 从 3 步扩展到 4 步乃至更长时，欧几里得空间中的预测误差快速积累。定量证据表明，V-JEPA 2 在 CrossTask 上 T=8 时的成功率（SR）仅为 4.95，而 T=3 时尚有 50.16——性能衰减超过 90%。这说明欧几里得正则化不足以约束长时域推演中的误差传播。

### 动机：引入双曲几何以编码层次结构

上述瓶颈的深层原因在于，**层次化状态结构天然适合用双曲几何表示**。双曲空间具有负曲率，其体积随半径呈指数增长，恰好匹配树状层次结构中节点数随深度指数增长的规律。在双曲流形上，测地距离自然编码了状态之间的层次亲疏关系：同一子树内的节点距离近，不同分支的节点距离远。

GeoWorld 的核心动机正是将这一几何洞察引入预测世界模型：**将潜在表示从欧几里得空间映射到双曲流形（Poincaré 球），并强制潜在动力学沿双曲测地线演化**。这样做的预期收益是：

- 产生**结构化、曲率感知的能量景观**，使能量低谷对应有意义的子目标区域，而非随机的平坦洼地；
- 利用双曲空间的**三角不等式正则化**约束多步预测，使累积误差沿测地线传播时得到几何约束；
- 最终实现**稳定的长时域规划**，缓解欧几里得模型中随步长急剧退化的困境。

### 方法定位

GeoWorld 并非重新设计世界模型的编码器或规划器，而是**在现有预测世界模型框架上替换两个关键组件**：

| 组件 | 基线（V-JEPA 2） | GeoWorld |
|------|------------------|----------|
| 潜在表示空间 | 欧几里得空间 ℝⁿ | 双曲空间（Poincaré 球）𝔹ⁿ_c |
| 能量/距离度量 | 欧几里得距离或 L1 距离 | 双曲测地距离 d_ℍ，辅以三角不等式正则化 |
| 多步优化 | 仅监督微调（教师强制 + rollout） | 加入几何强化学习（GRL），通过双曲能量最小化优化预测器 |

通过这两个变更，GeoWorld 在不改变编码器架构、不引入额外策略网络的前提下，为预测世界模型赋予了层次感知的几何先验。

## 核心方法与创新机理

GeoWorld 的核心创新在于将世界模型的潜在动力学从欧几里得空间迁移到双曲流形上，从而从根本上改变了状态表示和规划优化的几何基础。与现有的预测型世界模型（如 V-JEPA 2）相比，GeoWorld 在三个关键设计槽位上做出了结构性改变。

### 从欧几里得到双曲的表示空间迁移

现有世界模型在欧几里得空间 $\mathbb{R}^n$ 中学习潜在表示，其能量景观基于欧几里得距离或 L1 距离度量。这种设计忽略了一个关键事实：复杂任务的状态空间天然具有层次结构——例如“煮咖啡”包含“研磨咖啡豆”“加热水”等子任务，而子任务内部又包含更细粒度的步骤。欧几里得空间的平坦几何无法有效编码这种树状层次关系，导致能量景观缺乏有意义的测地距离结构。

GeoWorld 提出 **Hyperbolic JEPA (H-JEPA)**，将编码器输出的欧几里得嵌入 $s_t^x$ 通过指数映射投影到 Poincaré 球模型的双曲空间 $\mathbb{B}_c^n$ 上：

$$s_{t,\mathbb{H}}^x = \exp_0(s_t^x) = \operatorname{tanh}(\sqrt{c}\|s_t^x\|)\frac{s_t^x}{\sqrt{c}\|s_t^x\|}$$

这一映射的关键意义在于：双曲空间的负曲率特性使其体积随半径指数增长，天然适合嵌入具有指数分支结构的层次化数据。在双曲流形上，测地距离 $d_{\mathbb{H}}$ 能够自然编码状态间的层次关系——共享父节点的状态在双曲空间中距离更近，而跨分支的状态则被推远。实验证据表明，GeoWorld 学习到的潜在空间在 Gromov δ-双曲性上分布更集中（见附录 Figure 1），验证了其潜在空间确实具有更强的树状层次几何特性。

### 从欧几里得距离到双曲测地距离的能量度量

度量空间的改变直接影响了世界模型的训练目标和能量景观的形态。V-JEPA 2 使用欧几里得距离作为预测误差度量，其能量景观在潜在空间中呈现相对均匀的分布。GeoWorld 则将教师强迫损失替换为双曲测地距离：

$$\mathcal{L}_{\mathrm{TF}}(\theta,\phi) = \frac{1}{T}\sum_{t=1}^T d_{\mathbb{H}}\big(P_\phi(\exp_0(E_\theta(x_t)),a_t),\exp_0(E_\theta(x_{t+1}))\big)$$

这一改变产生了结构化的能量景观。如 Figure 2 所示，在参考潜在状态周围沿两个正交切空间方向扫描能量时，V-JEPA 2 的能量分布相对平坦且缺乏方向性，而 GeoWorld 产生了曲率感知的、结构化的能量景观，能量低谷沿测地线方向自然延伸，更好地反映了潜在状态间的几何结构与层次关系。这种结构化能量景观为后续的基于能量的规划提供了更有效的搜索空间。

### 从纯监督微调到几何强化学习的多步优化

V-JEPA 2 的多步预测仅依赖监督微调（教师强制加两步 rollout），缺乏对长时域一致性的显式优化。GeoWorld 引入了 **Geometric Reinforcement Learning (GRL)**，将多步规划建模为双曲潜在空间中的能量最小化问题。其核心机制包括：

1. **双曲能量最小化**：定义能量成本为预测状态与真实状态间的双曲测地距离 $c_t = d_{\mathbb{H}}(\hat{s}_{t+1,\mathbb{H}}^x, s_{t+1,\mathbb{H}}^x)$，以负能量成本作为奖励信号，通过最小化累积折扣能量来优化预测器：

   $$\mathcal{L}_{\mathrm{GRL}}(\phi) = \mathbb{E}_{a_{1:T}\sim\phi}\left[\sum_{t=1}^T \gamma^{t-1} d_{\mathbb{H}}(\hat{s}_{t+1,\mathbb{H}}^x, s_{t+1,\mathbb{H}}^x)\right] + \beta\mathcal{L}_\Delta$$

2. **三角不等式正则化**：$\mathcal{L}_\Delta$ 强制执行双曲空间中预测状态间的三角不等式约束，确保多步预测的测地一致性，防止预测轨迹偏离流形的几何结构。

消融实验（Table 2）证实了这一创新的有效性：在 CrossTask 数据集上，SFT+GRL 组合在 T=4 时达到 37.04 的成功率，显著优于仅使用 SFT 的 35.92。在长时域规划中（Table 5），差距进一步拉大：T=8 时完整模型的成功率为 13.81，而 V-JEPA 2 仅为 4.95，表明 GRL 的几何约束有效缓解了多步预测中的误差积累问题。

### 创新的协同效应

这三个改变槽位并非孤立存在，而是形成了一条完整的因果链条：双曲表示空间提供了层次化编码的基础，双曲测地距离将这种几何结构转化为结构化的能量景观，而 GRL 则通过能量最小化和测地一致性正则化充分利用了这一结构化景观进行长时域优化。三者共同实现了从“在欧几里得空间中预测”到“在双曲流形上规划”的范式转换。

GeoWorld 是一个几何世界模型，其核心设计理念是将预测世界模型的潜在动力学从欧几里得空间迁移到双曲流形上，从而在能量景观中自然编码状态间的层次结构与几何关系。整个框架由四个关键模块串联构成，形成“编码→投影→预测→规划”的闭环管线。

### 管线概览

**输入**为观测 $x_t$（图像或视频帧）与目标状态 $x_{t+T}$，**输出**为在规划时域 $T$ 内的最优动作序列 $(a_t^*)_{t=1}^T$。管线流程如下：

1. **冻结视觉编码器** $E_\theta$：将观测 $x_t$ 编码为欧几里得潜在表示 $s_t^x \in \mathbb{R}^n$。该编码器基于 V-JEPA 2 在 VideoMix22M 上预训练的权重，并在 GeoWorld 训练中保持冻结。
2. **指数映射投影** $\exp_0(\cdot)$：将欧几里得嵌入 $s_t^x$ 视为 Poincaré 球原点处切空间中的切向量，通过可微双曲投影层映射到双曲空间 $\mathbb{B}_c^n$，得到 $s_{t,\mathbb{H}}^x$。该层的曲率 $c$ 为可学习参数。
3. **动作条件预测器** $P_\phi$：接收当前双曲状态 $s_{t,\mathbb{H}}^x$ 与动作序列 $a_{1:T}$，在双曲潜在空间中自回归地预测未来状态序列 $\hat{s}_{t+1,\mathbb{H}}^x, \dots, \hat{s}_{t+T,\mathbb{H}}^x$。该预测器为约 300M 参数的 Transformer（24 层、16 头、1024 维隐藏层、GELU 激活）。
4. **CEM 规划器**：在双曲潜在空间中，以最小化预测轨迹与目标状态之间的双曲测地距离为能量成本函数，通过 Cross-Entropy Method 搜索最优动作序列。

### 训练流程

GeoWorld 的训练分为两个阶段：

- **阶段一：监督微调（SFT）**。通过教师强制损失 $\mathcal{L}_{\mathrm{TF}}$（单步双曲测地距离）与 rollout 损失 $\mathcal{L}_{\mathrm{rollout}}$（多步预测累积距离）的加权组合 $\mathcal{L}_{\mathrm{SFT}}$ 训练预测器 $P_\phi$ 和投影层。此阶段使模型初步学会在双曲空间中预测状态演化。
- **阶段二：几何强化学习（GRL）**。将规划视为最小化双曲能量值函数的过程——奖励定义为负的双曲能量成本 $r_t = -c_t$，价值函数 $V$ 为规划时域内的折扣累积奖励。GRL 损失 $\mathcal{L}_{\mathrm{GRL}}$ 由期望双曲距离项与三角不等式正则化项 $\beta\mathcal{L}_\Delta$ 组成，直接优化预测器以强制执行测地一致性和层次结构保持。

### 关键设计决策

- **双曲空间的选择**：双曲几何的负曲率特性使测地距离能够自然编码树状层次关系——在层次结构中，兄弟节点间的距离通过共同父节点被压缩，这与任务规划中“高层目标→子步骤”的指数分支结构高度吻合。
- **能量景观的几何约束**：通过将能量成本定义为双曲测地距离并加入三角不等式正则化，GeoWorld 产生的能量景观具有结构化和曲率感知特性（见 Figure 2），相比欧几里得空间的 V-JEPA 2 能量景观更有利于长时域规划。
- **冻结编码器策略**：消融实验表明，全微调编码器仅带来 0.3–0.8% 的成功率提升，冻结编码器足以捕获任务相关的层次结构，同时保持计算效率。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_23058/figures/003_Figure_3.jpg]]
*Figure 3: Overview of GeoWorld. Our geometric world model integrates Hyperbolic JEPA for geometry-preserving latent dynamics and Geometric Reinforcement Learning for geodesic-consistent multi-step refinement. Together with energy-based planning using CEM, GeoWorld enables stable and geometry-aware long-horizon visual planning*

GeoWorld 的核心架构由四个关键模块串联构成，形成从视觉观测到双曲空间规划的完整闭环。

**模块一：冻结视觉编码器 $E_\theta$**

采用预训练的 V-JEPA 2 编码器，将观测 $x_t$ 映射为欧几里得潜在表示 $s_t^x \in \mathbb{R}^n$：

$$s_t^x = E_\theta(x_t)$$

该编码器在 VideoMix22M 上预训练后冻结，后续实验表明全微调仅带来 0.3–0.8% 的成功率提升，冻结足以保留任务相关的几何结构。

**模块二：指数映射投影 $\exp_0$**

这是将欧几里得表示注入双曲空间的关键操作。将 $s_t^x$ 视为 Poincaré 球模型原点处切空间中的切向量，通过可微的指数映射投影到双曲流形 $\mathbb{B}_c^n$：

$$s_{t,\mathbb{H}}^x = \exp_0(s_t^x) = \tanh(\sqrt{c}\|s_t^x\|)\frac{s_t^x}{\sqrt{c}\|s_t^x\|}$$

其中曲率 $c$ 为可学习参数。训练过程中 $c$ 从初始值 1 逐步下降并收敛至约 0.3，表明适度的负曲率足以编码层次结构且保持训练稳定。

**模块三：动作条件预测器 $P_\phi$**

预测器是一个约 300M 参数的 Transformer（24 层、16 头、1024 维隐藏层、GELU 激活），以当前双曲状态和动作序列为输入，预测未来双曲潜在状态序列。其训练分为两个阶段：

*监督微调阶段*的目标是最小化预测状态与真实状态之间的双曲测地距离。一步教师强制损失定义为：

$$\mathcal{L}_{\mathrm{TF}}(\theta,\phi) = \frac{1}{T}\sum_{t=1}^T d_{\mathbb{H}}\big(P_\phi(\exp_0(E_\theta(x_t)),a_t),\exp_0(E_\theta(x_{t+1}))\big)$$

为改善长时域一致性，引入 rollout 损失，总监督损失为两者的加权组合：

$$\mathcal{L}_{\mathrm{SFT}}(\theta,\phi) = \lambda\mathcal{L}_{\mathrm{TF}}(\theta,\phi) + (1-\lambda)\mathcal{L}_{\mathrm{rollout}}(\theta,\phi)$$

消融实验表明 $\lambda=0.5$ 时整体性能最优。

*几何强化学习阶段*直接精炼预测器，无需训练额外的策略或奖励模型。能量成本定义为预测状态与目标状态之间的双曲测地距离：

$$c_t(s_{t,\mathbb{H}}^x, s_{t+1,\mathbb{H}}^x) = d_{\mathbb{H}}(P_\phi(\exp_0(E(x_t)),a_t), \exp_0(E(x_{t+1})))$$

奖励为负能量成本 $r_t = -c_t$。路径价值函数为规划时域 $T$ 内的期望累积奖励：

$$V(s_{1,\mathbb{H}}^x, s_{1+T,\mathbb{H}}^x) = \mathbb{E}_{a_{1:T}\sim\phi}\left[\sum_{t=1}^T \gamma^{t-1} r_t\right]$$

GRL 总损失结合双曲能量最小化与三角不等式正则化 $\mathcal{L}_\Delta$：

$$\mathcal{L}_{\mathrm{GRL}}(\phi) = \mathbb{E}_{a_{1:T}\sim\phi}\left[\sum_{t=1}^T \gamma^{t-1} d_{\mathbb{H}}(\hat{s}_{t+1,\mathbb{H}}^x, s_{t+1,\mathbb{H}}^x)\right] + \beta\mathcal{L}_\Delta$$

消融表明 $\beta=0.1$、$\gamma=0.99$ 时达到最强结果，且 $\beta>0$ 持续提升性能，验证了三角不等式正则化对保持测地一致性的关键作用。

**模块四：CEM 规划器**

采用交叉熵方法在双曲潜在空间中搜索最优动作序列。能量成本函数衡量预测轨迹与目标潜在状态之间的双曲能量：

$$C((\hat{a}_t)_{t=1}^T; s_{1,\mathbb{H}}^x, s_{1+T,\mathbb{H}}^x) = d_{\mathbb{H}}(P((\hat{a}_t)_{t=1}^T; s_{1,\mathbb{H}}^x), s_{1+T,\mathbb{H}}^x)$$

最优动作序列通过最小化该能量获得：

$$(a_t^*)_{t=1}^T = \arg\min_{(\hat{a}_t)_{t=1}^T} d_{\mathbb{H}}(P((\hat{a}_t)_{t=1}^T; s_{1,\mathbb{H}}^x), s_{1+T,\mathbb{H}}^x)$$

CEM 超参数与 V-JEPA 2-AC 保持一致（$N=800$，$K=80$，$I=10$），保证对比的公平性。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_23058/figures/002_Figure_2.jpg]]
*Figure 2: Energy landscape comparison for V-JEPA 2 [3] and GeoWorld. We visualize the energy by sweeping two orthonormal tangent-space directions (∆x, ∆y) around a reference latent state. GeoWorlds yields a structured, curvature-aware energy landscape that better reflects geometric structure and hierarchical relations among latent states and improves energy-based planning. For more details see Appendix 4*

## 实验与关键发现

### 实验设置概览

GeoWorld 在两个标准的过程规划基准上进行了评估：**CrossTask**（4.7K 视频，83 个任务，105 种动作，平均每视频 8 个动作，375 小时）和 **COIN**（11,287 视频，180 个任务，778 种动作，平均每视频 3.9 个动作，476 小时）。评估指标包括：
- **Success Rate (SR)**：预测动作序列与真实序列的精确匹配率；
- **Mean Accuracy (mAcc)**：每步平均准确率；
- **Mean IoU (mIoU)**：预测序列与真实序列的重叠度。

实验在两种设置下进行：(1) **过程规划设置**（procedural planning），观测和目标均为图像；(2) **视频规划设置**（visual planning with videos），观测和目标均为视频片段。所有对比中，V-JEPA 2 与 GeoWorld 使用相同的预训练冻结编码器（ViT-g384，在 VideoMix22M 上预训练），CEM 规划超参数保持一致（N=800, K=80, I=10），通用 VLM 以零样本评估。

### 主实验结果

#### 过程规划设置（图像输入）

在图像输入的过程规划设置下，GeoWorld 在 CrossTask 和 COIN 上均取得一致的性能提升。**Table 1** 展示了多步目标条件视觉规划的结果。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_23058/figures/004_Table_1.jpg]]
*Table 1: Goal-conditioned visual planning with images on CrossTask [88] and COIN [71] datasets. We evaluate multi-step planning over a horizon T under the procedural planning setup [15], where both observations and goals are specified as images*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_23058/figures/007_Table_1.jpg]]
*Table 1: Ablation of frozen encoder vs. fully fine-tuned model for visual planning with videos on CrossTask [88]*

在 CrossTask 上，GeoWorld（ViT-g384）在 T=3 时达到 **47.47 SR / 73.69 mAcc / 86.55 mIoU**，相比 V-JEPA 2 的 45.58 SR 提升 **+1.89**；在 T=4 时达到 **31.48 SR / 67.30 mAcc / 82.48 mIoU**，相比 V-JEPA 2 的 29.57 SR 提升 **+1.91**。在 COIN 上，GeoWorld 同样展现出稳定优势，T=3 时 SR 达到 **45.29**，比 V-JEPA 2 的 42.74 提升 **+2.55**。

值得注意的是，GeoWorld 在 T=3 时已超越多个基于 VLM 的零样本方法（如 SCHEMA、MTID），且作为预测型世界模型，其性能优势随规划步长增加而扩大，这验证了双曲几何在保持长时域规划一致性方面的作用。

#### 视频规划设置

在视频输入设置下，**Table 2** 展示了更全面的对比结果。GeoWorld 在 CrossTask 上 T=3 时达到 **51.71 SR**（V-JEPA 2 为 50.16，+1.55），T=4 时达到 **37.04 SR**（V-JEPA 2 为 35.01，+2.03）。COIN 上 T=3 达到 **45.29 SR**（V-JEPA 2 为 42.74，+2.55）。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_23058/figures/005_Table_2.jpg]]
*Table 2: Goal-conditioned visual planning with videos on CrossTask [88] and COIN [71] datasets. We evaluate multi-step planning over a horizon T under the visual planning with videos [59] setup, where both observations and goals are specified as video clips*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_23058/figures/009_Table_2.jpg]]
*Table 2: Ablation of Supervised Fine-Tuning (SFT) vs. Geometric Reinforcement Learning (GRL) for visual planning with videos on CrossTask [88]*

视频设置下的提升幅度与图像设置一致，表明双曲潜在空间的几何约束对不同输入模态具有鲁棒性。此外，GeoWorld 在所有指标（SR、mAcc、mIoU）上均超过 V-JEPA 2，说明双曲测地距离作为能量成本不仅提高了精确匹配率，也改善了序列的整体对齐质量。

#### 长时域规划

**Table 5** 专门对比了长时域规划下的成功率。当规划步长 T 从 3 扩展到 8 时，V-JEPA 2 的性能急剧退化（T=8 时 SR 仅 **4.95**），而 GeoWorld 完整模型（SFT+GRL）在 T=8 时仍保持 **13.81** 的 SR，几乎是 V-JEPA 2 的 2.8 倍。这一结果直接支撑了论文的核心主张：双曲能量景观能有效缓解多步预测中的误差积累，稳定长时域规划。

### 消融实验

#### 冻结编码器 vs. 全微调

**Table 1（消融）** 对比了冻结编码器与全微调模型在 CrossTask 视频规划上的表现。全微调仅带来 **0.3–0.8% SR** 的微小提升，表明冻结的预训练编码器已足以捕获任务相关的层次结构，双曲投影层和几何强化学习是性能提升的主要来源。这一发现也保证了与 V-JEPA 2 对比的公平性——两者均使用冻结编码器。

#### 监督微调 (SFT) vs. 几何强化学习 (GRL)

**Table 2（消融）** 展示了 SFT 与 GRL 的贡献分解。仅 SFT 的模型在 CrossTask T=4 时达到 35.92 SR，而加入 GRL 后（SFT+GRL）提升至 **37.04 SR**，增幅显著。GRL 的增益在更长规划步长下更为突出，验证了基于双曲能量最小化的强化学习对多步预测一致性的关键作用。

#### SFT 中的 rollout 损失权重 λ

**Table 3（消融）** 探索了 SFT 中教师强迫损失与 rollout 损失的权重 λ。λ=0.5 在所有指标上取得最强整体性能，表明平衡一步预测精度与多步 rollout 一致性对学习稳定的双曲动力学至关重要。极端值（λ=0 仅 rollout，λ=1 仅教师强迫）均导致性能下降。

#### GRL 中的折扣因子 γ 与正则化权重 β

**Table 4（消融）** 分析了 GRL 中两个关键超参数。结果表明 **β=0.1, γ=0.99** 达到最强结果，且 β>0 持续提升性能，证实了三角不等式正则化（$\mathcal{L}_\Delta$）对保持双曲潜在空间中测地一致性的重要性。过大的 β 值会过度约束预测器，反而损害性能。

### 定性分析：能量景观可视化

**Figure 2** 提供了 V-JEPA 2 与 GeoWorld 潜在能量景观的直观对比。通过在参考潜在状态周围沿两个正交切空间方向扫描能量值，GeoWorld 产生了结构化、曲率感知的能量景观，清晰反映了潜在状态间的几何结构与层次关系。相比之下，V-JEPA 2 的欧几里得能量景观呈现无序、平坦的特征，缺乏有意义的结构。这一可视化直接解释了 GeoWorld 在基于能量的规划中表现更优的原因：CEM 优化器在结构化的双曲能量景观上能更有效地沿着测地线找到最优动作序列。

### 曲率学习动态

**Figure 2(d)（消融）** 展示了可学习曲率 c 在监督训练期间的动态变化。曲率从初始值 1 逐步下降，最终收敛至约 **0.3** 的稳定值。这表明模型自主学习到适度的负曲率足以支持层次结构编码，过强的负曲率（c 接近 1）反而会导致空间过度弯曲、距离度量不稳定。这一发现为双曲空间在预测世界模型中的实际部署提供了重要指导。

### 失败模式与局限性

尽管 GeoWorld 在多个基准上取得一致提升，但分析揭示了以下局限：

1. **长时域误差积累未完全消除**：即便使用双曲几何，T=8 时 SR 仍从 T=3 的 51.71 降至 13.81。几何结构只能缓解而非根除多步预测的误差传播问题。
2. **层次结构的隐式性**：当前方法的层次关系源于多步未来扩展的指数分支特性，而非显式的子任务分层规划。这限制了模型在需要显式任务分解的场景中的可解释性和可控性。
3. **任务范围受限**：所有实验限于目标条件视觉规划（CrossTask 和 COIN），尚未在具身环境或需要物理交互的任务中验证。
4. **单层双曲空间的表达力**：可学习曲率收敛至单一值（约 0.3），可能无法充分捕获数据中异构的层次关系（如不同子任务具有不同的分支因子），乘积空间或其他混合几何结构可能提供更强的表达能力。

## 定位与知识库关联

### 1. 与现有预测世界模型的关系

GeoWorld 直接建立在 **V-JEPA 2** 的预测世界模型范式之上，但对其潜在表示空间和能量景观进行了根本性的几何重构。V-JEPA 2 在欧几里得空间 $\mathbb{R}^n$ 中学习潜在动力学，使用 L1 或欧几里得距离作为能量度量，并通过 CEM 进行规划。GeoWorld 保留了 V-JEPA 2 的冻结编码器（ViT-g384，在 VideoMix22M 上预训练）和 CEM 规划框架，但在三个关键维度上进行了替换：

- **表示空间**：从欧几里得空间 $\mathbb{R}^n$ 映射到 Poincaré 球模型的双曲空间 $\mathbb{B}_c^n$，通过可微指数映射 $\exp_0(\cdot)$ 实现，曲率 $c$ 作为可学习参数。
- **距离度量**：从欧几里得距离替换为双曲测地距离 $d_{\mathbb{H}}$，并引入三角不等式正则化 $\mathcal{L}_\Delta$ 强制执行测地一致性。
- **多步优化**：在监督微调（SFT，包含教师强制和 rollout 损失）之上，增加几何强化学习（GRL）阶段，直接通过双曲能量最小化优化预测器，而非训练额外的策略或奖励模型。

这种设计使得 GeoWorld 的能量景观呈现出 V-JEPA 2 所不具备的结构化、曲率感知特性（见 Figure 2 对比）。在 Gromov δ-双曲性指标上，GeoWorld 学习到的潜在空间分布更集中，表明其具有更强的树状层次几何（附录 Figure 1）。

### 2. 与其他规划范式的对比

GeoWorld 属于**基于能量的预测世界模型**路线，与生成式世界模型和 LLM-based 规划方法形成对比：

- **生成式世界模型**（如 **VideoWorld**、**MTID**）：通过生成像素级未来帧进行规划，计算成本高且容易在长时域累积视觉伪影。GeoWorld 在潜在空间中操作，避免像素生成，通过双曲测地线直接优化动作序列。
- **LLM-based 规划**（如 **SCHEMA**）：依赖语言模型的常识推理进行任务分解，但缺乏对视觉动态的细粒度建模。GeoWorld 在连续视觉潜在空间中学习动力学，能够捕获任务执行中的几何与层次结构。

GeoWorld 的独特优势在于将双曲几何的层次表示能力与基于能量的规划相结合，使得规划过程自然地沿着测地线进行，而非在欧几里得空间中线性插值。

### 3. 适用边界与局限

**适用场景**：
- 目标条件视觉规划，特别是具有层次结构的程序性任务（如烹饪、设备维修）。
- 需要长时域一致性的多步规划（T=3, 4, 8）。
- 观测和目标均为图像或视频片段的任务设定。

**明确局限**：
1. **层次结构的来源**：当前方法中的层次关系源于多步未来扩展的指数分支特性，而非显式的子任务分层规划。GeoWorld 并未显式建模“高层任务→中层动作→底层执行器”的多级层次。
2. **任务范围受限**：工作目前仅限于目标条件视觉规划，尚未在具身环境（如机器人操作）中验证。双曲几何在物理交互任务中的有效性仍是开放问题。
3. **长时域误差积累**：即便使用双曲几何，长时域预测仍存在误差积累。几何结构只能缓解而非完全消除这一问题——Table 5 显示 T=8 时 SR 从 T=3 的 51.71 下降至 13.81，虽远优于 V-JEPA 2 的 4.95，但绝对性能仍然较低。
4. **编码器依赖**：GeoWorld 依赖预训练的 V-JEPA 2 编码器，消融实验表明全微调仅带来 0.3-0.8% SR 的微小提升，这意味着性能上限部分受限于编码器质量。

### 4. 开放问题

1. **双曲几何如何约束误差积累？** 与欧几里得正则化相比，双曲测地距离和三角不等式正则化在理论上如何具体限制多步预测的误差传播？需要更系统的理论分析。
2. **具身场景的扩展**：能否将 GeoWorld 扩展到具有子任务层次的具身环境中？机器人操作任务通常具有明确的层次分解（任务→技能→原语），双曲几何可能天然适合表示这种结构。
3. **异构层次关系的建模**：当前使用单一曲率 $c$ 的 Poincaré 球模型，但现实任务可能包含不同粒度的层次关系。是否可以将可学习曲率与其他几何结构（如乘积空间 $\mathbb{B}^{n_1}_{c_1} \times \mathbb{B}^{n_2}_{c_2}$）结合以处理异构层次？
4. **实时规划效率**：CEM 规划需要 N=800 个采样轨迹，在双曲空间中计算测地距离的开销高于欧几里得距离。如何在保持几何优势的同时降低规划计算成本？
5. **与 LLM 的融合**：LLM 提供高层任务分解，GeoWorld 提供底层几何规划，两者的结合可能产生更强的长时域规划能力，但接口设计（离散符号与连续双曲表示的对接）仍待探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/GeoWorld_Geometric_World_Models.pdf]]
