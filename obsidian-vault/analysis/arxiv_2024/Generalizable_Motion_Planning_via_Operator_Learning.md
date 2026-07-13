---
title: Generalizable Motion Planning via Operator Learning
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/Generalizable_Motion_Planning_via_Operator_Learning.pdf
project_link: null
code_link: https://github.com/ExistentialRobotics/PNO
aliases:
- PNOP
- GMPOL
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将价值函数近似重构为从代价函数空间到价值函数空间的算子学习问题，并设计具有分辨率不变性、障碍物几何编码和三角不等式约束的神经算子（Planning Neural Operator, PNO），实现跨环境、跨分辨率和跨目标位置的泛化。
primary_logic: "Eikonal PDE的解可视为连续算子Ψ: c(x) ↦ V(x)，通过神经算子近似该算子，并结合频域学习（FNO）、障碍物平滑掩码（DAFNO思想）以及满足三角不等式的Deepnorm投影层，使得单一模型能在粗分辨率训练后直接预测高分辨率、新环境和新目标下的价值函数，并可作为ε一致的启发式加速A*。"
claims:
- PNO在Grid World数据集上以显著更低的计算时间达到99.3%的成功率，优于VIN和IEF2D。
- PNO在合成2D地图上实现L2误差为0.1136，在未见过的真实城市地图上将DAFNO的L2误差降低50%，并实现相比于FMM的近10倍加速。
- PNO作为A*的启发式函数，结合障碍膨胀，在MovingAI城市地图上减少33%的节点展开并保持路径接近最优。
- PNO在3D iGibson建筑物环境和4-DOF机械臂规划中均能以高精度（测试L2误差0.19和0.041）生成价值函数，且无需针对新环境重新训练。
---

# Generalizable Motion Planning via Operator Learning

> [!tip] 核心洞察
> Eikonal PDE的解可视为连续算子Ψ: c(x) ↦ V(x)，通过神经算子近似该算子，并结合频域学习（FNO）、障碍物平滑掩码（DAFNO思想）以及满足三角不等式的Deepnorm投影层，使得单一模型能在粗分辨率训练后直接预测高分辨率、新环境和新目标下的价值函数，并可作为ε一致的启发式加速A*。

| 字段 | 内容 |
|------|------|
| 中文题名 | 可泛化运动规划：基于算子学习的方法 |
| 英文题名 | Generalizable Motion Planning via Operator Learning |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2410.17547) · [Code](https://github.com/ExistentialRobotics/PNO) · [paper](https://arxiv.org/abs/1709.05448) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Planning Neural Operator (PNO) |
| Dataset | Grid World, MovingAI 2D Synthetic, MovingAI 2D Real-world City, iGibson 3D Buildings |

> [!tip] 效果简介
> - Grid World (28×28) 上，Avg. Success Rate (%) / Avg. Computation Time (ms) 99.3% / 6.4 ms vs VIN: 96.7% / 82.1 ms; IEF2D: 97.0% / 20.4 ms (PNO 成功率比 VIN 高2.6%，计算速度快12.8倍)。
> - MovingAI 2D Synthetic (64²) 上，Avg. L2 Relative Error 0.1136 (PNO); 0.0698 (PNO w/ PINN) vs FNO: 0.1996; DAFNO: 0.0985 (PNO 误差比 FNO 降低 43.1%，PINN 进一步降 38.6%)。
> - MovingAI 2D Real-world City (64², 1024²) 上，Avg. L2 Relative Error / Speedup vs FMM 0.1748 (no PINN) / ~10× speedup at 1024² vs DAFNO: 0.4090; FMM: 104.6 ms at 1024² (PNO 误差比 DAFNO 降低 57.3%，计算速度比 FMM 快约10倍)。

## 概要

运动规划是机器人学的基础问题，其核心在于寻找从起点到目标点的无碰撞路径，同时最小化某种代价（如时间或能量）。传统规划算法——包括基于搜索的A*、基于采样的RRT/RRT*以及数值Eikonal求解器（如快速行进法FMM）——在复杂、动态或高分辨率环境中面临计算开销巨大的瓶颈。近年来，神经价值函数预测器（如**VIN**，Tamar et al., NIPS 2016；**IEF2D/3D**，Li et al., 2022；**NTFields**，Ni & Qureshi, 2023a）试图通过深度学习加速这一过程，但它们普遍缺乏跨环境泛化能力和分辨率不变性：一旦环境改变或分辨率提升，模型通常需要重新训练或完全失效，无法实现零样本部署。

本文的核心洞察在于将价值函数近似重新构建为一个**算子学习问题**。作者指出，在均匀代价（最小时间）运动规划假设下，最优价值函数 $V(\pmb x)$ 满足Eikonal偏微分方程 $\|\nabla V(\pmb x)\| = c(\pmb x)$，其解可视为一个连续算子 $\Psi: c(\pmb x) \mapsto V(\pmb x)$，将代价函数空间映射到价值函数空间。基于此，论文提出**规划神经算子（Planning Neural Operator, PNO）**，通过三个关键设计实现跨环境、跨分辨率和跨目标位置的泛化：

1. **频域学习与分辨率不变性**：继承Fourier神经算子（**FNO**，Li et al., 2021）的架构，在频域中进行特征提取，使模型在粗分辨率（如64×64）训练后可直接预测高分辨率（最高1024×1024）下的价值函数，实现16倍超分辨率部署。

2. **障碍物几何编码**：设计平滑指示函数 $\tilde{\chi}_{PNO}(\mathbf{x}) = \tanh(\beta d_S(\pmb x)) (1/c(\pmb x) - 0.5) + 0.5$，将障碍物的符号距离信息硬编码进Fourier层的权重乘法中，显著提升对复杂障碍布局的感知能力。

3. **目标位置泛化与三角不等式约束**：引入Deepnorm投影层 $Q_{PNO}(\phi, \pmb{x}, \pmb{g}) = f_{\theta_Q}(\phi(\pmb{x}) - \phi(\pmb{g}))$，自动满足最优价值函数的三角不等式，使单一模型能够零样本泛化到任意未见过的目标位置。

实验验证覆盖了从2D网格世界到3D建筑环境、再到4-DOF机械臂C空间的多个维度。在Grid World数据集上，PNO以6.4 ms的平均计算时间达到99.3%的规划成功率，速度比VIN快12.8倍（Table 1）。在MovingAI合成和真实城市地图上，PNO的价值函数L2相对误差低至0.1136，相比**DAFNO**（Liu et al., 2023）降低超过50%，并实现相对于FMM的近10倍加速（Table 2）。当PNO作为A*的启发式函数时，结合障碍膨胀策略，在1024×1024城市地图上减少33%的节点展开，同时保持路径最优性（Table 3）。在3D iGibson建筑和4-DOF机械臂规划中，PNO无需对每个新环境重新训练即可获得与需逐环境优化的NTFields可比甚至更优的精度（测试L2误差分别为0.19和0.041），展示了向高维规划扩展的可行性。

PNO的方法定位处于神经算子理论、Eikonal方程求解与启发式搜索规划的交汇点。其核心贡献在于首次将运动规划中的价值函数预测形式化为算子学习问题，并通过架构创新实现了分辨率不变性、障碍物感知和目标泛化三者的统一。该工作为快速、可泛化的神经运动规划开辟了新路径，同时也揭示了若干待解决问题：当前方法依赖均匀代价假设，尚未处理非均匀代价环境；障碍膨胀层数需手工调节；在训练与测试地图分布差异过大时精度仍会下降。

### 运动规划的核心瓶颈

运动规划是机器人学的基础问题，其目标是在有障碍物的环境中找到从起点到目标点的最优路径。从最优控制视角看，该问题可形式化为无限时域首次退出最优控制问题：最小化终端代价与累积运行代价之和，其中系统动力学为 $\dot{\pmb x}(t) = f(\pmb x(t), \pmb u(t))$，价值函数 $V(\pmb x)$ 表示从状态 $\pmb x$ 出发的最小代价。当运行代价仅依赖于状态（即控制无关代价）时，Hamilton-Jacobi-Bellman (HJB) 方程退化为 Eikonal 偏微分方程：

$$\|\nabla V(\pmb x)\| = c(\pmb x)$$

这意味着价值函数的梯度模长等于局部代价函数。求解该方程即可获得全局最优价值函数，进而通过梯度下降导出最优路径。

然而，传统方法面临严重的计算瓶颈。经典搜索算法（如 A*、RRT*）在高分辨率、复杂或动态环境中需要展开大量节点，计算开销随地图规模急剧增长。数值 Eikonal 求解器（如快速行进法 FMM）虽能精确求解，但其计算复杂度与网格点数成正比，在 1024×1024 分辨率下仍需约 100 ms，难以满足实时规划需求。

### 现有学习方法的结构性缺陷

近年来，基于学习的价值函数近似方法试图通过神经网络加速规划，但存在三个根本性局限：

**1. 缺乏跨环境泛化能力。** **VIN**（Tamar et al., NIPS 2016）通过 CNN 模拟值迭代过程，但其卷积核隐式编码了特定环境的转移动力学，无法零样本迁移到未见过的地图。**IEF2D/IEF3D**（Li et al., 2022）利用隐式函数学习场景签名距离，但仍需在训练分布内工作，对分布外场景的泛化能力有限。

**2. 每环境需重新训练。** **NTFields**（Ni & Qureshi, 2023a）和 **P-NTFields**（Ni & Qureshi, 2023b）基于物理信息神经网络（PINN）求解 Eikonal 方程，可在不同目标位置泛化，但模型参数与特定环境绑定——每遇到新地图都需重新优化，这在实际部署中不可接受。

**3. 分辨率固定，无法超分辨率推理。** 基于 CNN 的架构（如 VIN）要求固定的输入尺寸，训练于低分辨率后无法直接处理高分辨率输入，丧失了计算效率优势。

### 核心洞察：从函数近似到算子学习

本文的关键洞察在于重新审视价值函数近似的本质。Eikonal PDE 定义了一个连续算子 $\Psi: c(\pmb x) \mapsto V(\pmb x)$，将代价函数空间映射到价值函数空间。该算子具有三个关键性质：

- **Lipschitz 连续性**：$\|\Psi(c_2) - \Psi(c_1)\|_{L_\infty} \leq \theta_v \theta_c \|c_2 - c_1\|_{L^\infty}$，保证输入代价的微小变化不会导致价值函数的剧烈震荡。
- **三角不等式**：$V(\pmb x, \pmb g) \leq V(\pmb x, \pmb y) + V(\pmb y, \pmb g)$，这是最优性原理的直接推论。
- **分辨率不变性**：算子作用于连续函数空间，理论上与离散化分辨率无关。

因此，若能通过神经算子直接近似 $\Psi$，而非为每个环境学习独立的函数，则可从根本上解决泛化问题。这一思路将运动规划从“逐场景拟合”转变为“学习物理规律”，类似于在流体力学中用 Fourier Neural Operator（FNO, Li et al., 2021）学习 Navier-Stokes 方程的解算子。

### 方法动机与设计目标

基于上述分析，本文提出 **Planning Neural Operator (PNO)**，旨在实现以下目标：

1. **跨环境零样本泛化**：单一模型训练后可直接预测全新地图的价值函数，无需重训练。
2. **分辨率不变性**：在低分辨率（如 64×64）训练，可直接推理高分辨率（如 1024×1024）场景。
3. **目标位置泛化**：支持任意起点-目标对，无需将目标作为额外输入通道。
4. **理论保证**：预测的价值函数满足 ε-一致性，可作为 A* 的启发式保证路径质量。

为实现这些目标，PNO 在 FNO 基础上引入了三个关键设计：障碍物几何的平滑编码、满足三角不等式的 Deepnorm 投影层、以及混合 PINN 损失。这些组件协同工作，使神经算子能够从代价函数空间中捕获运动规划的底层结构，而非记忆特定地图的模式。

## 核心方法与创新机理

PNO 的核心创新在于将运动规划中的价值函数近似重新定义为**从代价函数空间到价值函数空间的算子学习问题**，并围绕这一范式设计了三个关键的技术槽位（changed slots），使其区别于所有现有基线方法。

### 1. 范式转换：从单场景拟合到跨环境算子学习

传统神经规划器（如 **VIN** (Tamar et al., NIPS 2016)、**NTFields** (Ni & Qureshi, 2023a)）将价值函数预测视为对特定环境的函数拟合——模型隐式或显式地记忆场景几何，导致每遇到新环境就需要重新训练或微调。PNO 的因果杠杆在于识别出：在最小时间运动规划假设下，最优价值函数 $V(\pmb{x})$ 是 Eikonal PDE $\|\nabla V(\pmb{x})\| = c(\pmb{x})$ 的解，而该 PDE 定义了一个从代价函数 $c$ 到价值函数 $V$ 的连续算子 $\Psi: c \mapsto V$。通过学习这个算子本身，而非拟合单个场景的解，PNO 获得了**跨环境、跨分辨率、跨目标位置**的零样本泛化能力。

这一范式转换的证据强度很高：在 MovingAI 真实城市地图上，PNO 无需任何重训练即可将 **DAFNO** (Liu et al., 2023) 的 L2 相对误差降低约 57.3%（0.1748 vs 0.4090，Table 2），并在 3D iGibson 建筑环境和 4-DOF 机械臂 C 空间中均保持测试误差在可接受范围（0.19 和 0.041，Figure 3, Figure 4），而 NTFields 和 P-NTFields 需要为每个新环境重新优化。

### 2. 障碍物几何的硬编码：平滑掩码机制

**槽位名称**：障碍物几何编码  
**基线值**：FNO 中无专门障碍编码；DAFNO 仅使用二值掩码区分域内外  
**PNO 方案**：通过平滑指示函数将障碍物几何强编码进 Fourier 层的可学习权重乘法中

PNO 设计了一个平滑掩码函数：
$$\tilde{\chi}_{PNO}(\mathbf{x}) := \tanh(\beta d_S(\pmb x)) (1/c(\pmb x) - 0.5) + 0.5$$

其中 $d_S(\pmb x)$ 为符号距离函数（SDF）。该掩码被直接乘入 Fourier 层的权重矩阵 $R \cdot \tilde{\chi}_{PNO}$，使得频域特征提取过程显式感知障碍物的空间位置和距离信息。为高效获取 SDF，PNO 引入了一个独立训练的辅助 FNO（Auxiliary SDF FNO），从二进制占据栅格直接预测 $d_S$，避免了在线数值求解的开销。

消融实验（Table 2）表明，这一编码是 PNO 相对于 FNO 和 DAFNO 性能提升的关键来源：在合成 2D 地图上，PNO 的 L2 误差（0.1136）比 FNO（0.1996）降低 43.1%；在真实城市地图上，比 DAFNO（0.4090）降低 57.3%。障碍编码的有效性在未见过的城市环境中尤为显著，说明平滑掩码提供了更强的几何归纳偏置。

### 3. 目标位置泛化：满足三角不等式的 Deepnorm 投影层

**槽位名称**：目标位置泛化机制  
**基线值**：VIN/IEF 需将目标位置作为额外输入通道；NTFields 固定目标训练  
**PNO 方案**：Deepnorm 投影层 $Q_{PNO}(\phi, \pmb{x}, \pmb{g}) = f_{\theta_Q}(\phi(\pmb{x}) - \phi(\pmb{g}))$，自动满足三角不等式

最优价值函数天然满足三角不等式 $V(\pmb{x}, \pmb{g}) \le V(\pmb{x}, \pmb{y}) + V(\pmb{y}, \pmb{g})$（最优性原理的直接推论）。PNO 的投影层通过计算隐藏特征 $\phi(\pmb{x})$ 与目标特征 $\phi(\pmb{g})$ 的差异，再经小型网络 $f_{\theta_Q}$ 映射为标量价值，从结构上保证了这一约束。这意味着模型无需为每个目标位置重新计算价值函数，也无需将目标作为额外的空间输入通道——目标泛化被内建于架构之中。

在 MovingAI 城市地图上的消融显示，Deepnorm 投影层（PNO vs DAFNO）贡献了约 50% 的 L2 误差降低（Section 4, Table 2），证明三角不等式约束对跨目标泛化有实质增益。理论上，该设计还使 PNO 作为 A* 启发式时具有 $\epsilon$ 一致性保证（$\epsilon = \max_{\{x, y \in S | x \neq y\}} 1 + 2 \epsilon_{NO} / V(x, y)$），这是现有神经启发式方法所缺乏的性质。

### 4. 分辨率不变性：频域学习的架构红利

**槽位名称**：分辨率不变性实现  
**基线值**：CNN 规划器（VIN）固定输入尺寸，无法处理不同分辨率  
**PNO 方案**：基于 FNO 的频域学习架构，输入/输出分辨率独立于训练分辨率

PNO 继承自 **FNO** (Li et al., 2021) 的频域参数化方式——Fourier 层在频域中学习有限维的权重矩阵，与空间网格的分辨率解耦。这使 PNO 天然具备分辨率不变性：在 $64 \times 64$ 分辨率上训练的模型可直接推理 $1024 \times 1024$ 的输入，实现 16 倍的超分辨率部署（Figure 1）。在计算效率上，PNO 在 $1024^2$ 分辨率下比数值求解器 FMM 快约 10 倍（Table 5），而 VIN 等 CNN 方法完全无法处理训练时未见过的分辨率。

### 5. 训练信号的增强：混合 PINN 损失

**槽位名称**：训练监督信号  
**基线值**：仅使用 L2 损失拟合数值求解器生成的价值函数  
**PNO 方案**：混合 PINN 损失 $\text{Loss} = \|V-\hat{V}\|_{L^2} + \xi (\int(\|\nabla \hat{V}\|-c)^2)^{1/2}$，显式约束梯度满足 Eikonal 方程

这一改进虽非架构层面的核心创新，但在实验中显示出稳定的性能增益：PINN 损失项使 PNO 在合成 2D 数据集上的 L2 误差从 0.1136 进一步降至 0.0698（Table 2），并显著改善了预测价值函数的梯度残差（Figure 7）。然而，权重 $\xi$ 的手工调节是一个实际限制——过大会导致模型退化为纯欧几里得范数解，过小则梯度约束不足。

### 创新边界与待验证点

- 当前所有创新均建立在**均匀代价（最小时间）运动规划**假设之上，非均匀代价（如风险偏好、能量最优）场景的扩展仍是一个开放问题。
- 作为 A* 启发式时，障碍膨胀层数的选择目前依赖实验调参（Table 3），缺乏自适应机制。
- 训练数据仍依赖传统数值求解器（FMM/Dijkstra）离线生成，对于极高维 C 空间（7-DOF 及以上）的数据生成成本可能成为瓶颈，这一点需要在实际应用中验证。

PNO 的整体 pipeline 将运动规划中的价值函数近似重新定义为**从代价函数空间到价值函数空间的算子学习问题**。其核心流程如下：

**输入**：一张二值占据栅格（binary occupancy grid），表示环境中的自由空间与障碍物。

**模块化流水线**：
1. **SDF 预测（辅助 FNO）**：一个独立训练的 Fourier Neural Operator（FNO）将二值占据栅格映射为对应的符号距离函数（SDF） $d_S(\pmb x)$。该模块独立于主网络训练，为后续障碍物编码提供高效的几何信息提取，避免在线调用数值 SDF 求解器。
2. **提升网络（Lifting Network）** $R_{PNO}$：将原始占据栅格（即 $1/c(\pmb x)$）映射到高维特征空间，为频域处理做准备。
3. **改进的 Fourier 层** $L_{m,PNO}$：这是 PNO 的核心特征提取模块。每一层通过 FFT 将特征变换到频域，在频域中乘以**可学习权重矩阵与平滑障碍掩码 $\tilde{\chi}_{PNO}$**，再通过 IFFT 变换回空间域。平滑掩码由 SDF 构造：
   $$\tilde{\chi}_{PNO}(\mathbf{x}) := \tanh(\beta d_S(\pmb x)) (1/c(\pmb x) - 0.5) + 0.5$$
   该设计将障碍物几何信息**硬编码**进 Fourier 层的权重乘法中，使模型显式感知障碍物边界。这一思想借鉴了 **DAFNO**（Liu et al., 2023）对非矩形域引入掩码的做法，但 PNO 使用平滑指示函数替代二值掩码，提供了更丰富的几何梯度信息。
4. **投影层（Deepnorm）** $Q_{PNO}$：将最后一个隐藏层的特征 $\phi(\pmb x)$ 与目标位置 $\pmb g$ 结合，输出最终的价值函数预测：
   $$Q_{PNO}(\phi, \pmb{x}, \pmb{g}) = f_{\theta_Q}(\phi(\pmb{x}) - \phi(\pmb{g}))$$
   该层自动满足三角不等式 $V(\pmb x, \pmb g) \le V(\pmb x, \pmb y) + V(\pmb y, \pmb g)$，是实现**零样本目标位置泛化**的关键机制。与 VIN 或 IEF 需要将目标作为额外输入通道不同，PNO 通过特征差分自然编码了目标条件。

**输出**：给定任意目标位置的价值函数预测 $\hat{V}(\pmb x, \pmb g)$，可直接用于梯度下降规划，或作为 A* 的启发式函数。

**训练监督**：PNO 采用混合损失函数，结合 L2 价值函数误差与 Eikonal 方程的梯度残差约束（PINN 损失）：
$$\mathrm{Loss}(V, \hat{V}) := \|V - \hat{V}\|_{L^2} + \xi \left( \int_{x \in S} (\|\nabla \hat{V}(\pmb{x}, \cdot)\| - c(\pmb{x}))^2 \right)^{1/2}$$
其中真值 $V$ 由 FMM 或 Dijkstra 等传统数值求解器离线生成。PINN 损失项显式约束预测价值函数的梯度模长逼近代价函数，有助于提升预测的物理一致性。

**关键架构特性**：
- **分辨率不变性**：基于 FNO 的频域学习架构使得输入/输出分辨率独立于训练分辨率。模型在 $64 \times 64$ 分辨率训练后，可直接推理 $1024 \times 1024$ 分辨率的场景（Figure 1），实现最高 $16\times$ 的超分辨率部署。
- **跨环境泛化**：障碍物几何编码与 Deepnorm 投影层的组合，使单一模型在未见过的真实城市地图（如 MovingAI 数据集）上无需重训练即可生成高质量价值函数，L2 误差相比 DAFNO 降低约 50%（Table 2）。
- **跨目标泛化**：Deepnorm 层通过特征差分机制，使模型在训练时见过的目标分布之外也能泛化，无需为目标位置设置额外输入通道。

**与基线方法的架构差异**：
- 相比 **FNO**（Li et al., 2021），PNO 增加了障碍物平滑掩码编码和 Deepnorm 投影层，消融实验表明这两项改进分别带来了显著的 L2 误差降低（Table 2）。
- 相比 **DAFNO**（Liu et al., 2023），PNO 用平滑指示函数替代二值掩码，并引入满足三角不等式的投影层，在城市地图上实现约 50% 的误差降低。
- 相比 **VIN**（Tamar et al., NIPS 2016）和 **IEF2D**（Li et al., 2022），PNO 不依赖 CNN 的固定尺寸卷积核，因此天然具备分辨率不变性和更强的跨环境泛化能力。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2410_17547/figures/002_Figure_2.jpg]]
*Figure 2: PNO network architecture. The input to a PNO is a binary occupancy grid, which is transformed into a sign distance function (SDF) via an independently trained FNO. This, along with the original binary map is passed to a series of modified FNO layers which hard encode the obstacles. Finally, this result, along with the goal, is then fed to a projection layer (ensuring satisfaction of the triangle inequality) obtaining the final value function prediction*

### 问题建模：从最优控制到Eikonal PDE

运动规划被形式化为无限时域首次退出最优控制问题。系统动力学为 $\dot{\pmb x}(t) = f(\pmb x(t), \pmb u(t))$，最优价值函数 $V(\pmb x)$ 定义为从状态 $\pmb x$ 出发的最小累积代价：

$$V(\pmb{x}) := \min_{\pi} \left\{ c_{\tau}(\pmb{x}(\tau)) + \int_{0}^{\tau} c(\pmb{x}(t), \pi(\pmb{x}(t))) dt \right\}$$

该价值函数满足 Hamilton-Jacobi-Bellman (HJB) 方程，这是最优性的充分条件：

$$0 = \min_{\pmb{u} \in \mathcal{U}} \left\{ \nabla V(\pmb{x})^{\top} f(\pmb{x},\pmb{u}) + c(\pmb{x},\pmb{u}) \right\}, \quad \forall \pmb{x} \in \mathcal{S} \setminus \mathcal{G}$$

当问题简化为全驱动系统（$\dot{\pmb x}(t) = \pmb u(t)$，$\|\pmb u\|=1$）且代价仅依赖状态（最小时间规划中 $c(\pmb x)=1$ 在安全集内，$c(\pmb x)=\infty$ 在障碍物内）时，HJB方程退化为Eikonal PDE：

$$\|\nabla V(\pmb{x})\| = c(\pmb{x})$$

这一退化是PNO方法的核心理论基石：价值函数近似被重构为从代价函数空间到价值函数空间的**算子学习问题**，即学习算子 $\Psi: c(\pmb x) \mapsto V(\pmb x)$。

---

### PNO架构：四大核心模块

PNO的整体架构如 Figure 2 所示，由四个功能模块串联构成。

#### 模块一：提升网络 $R_{PNO}$

输入为二进制占据栅格（表示为 $1/c(\pmb x)$），通过一个浅层全连接网络将低维输入映射到高维特征空间，为后续频域处理提供丰富的初始表示。

#### 模块二：辅助SDF FNO

一个独立训练的Fourier Neural Operator（FNO），专门从占据栅格预测符号距离函数 $d_S(\pmb x)$：

$$d_S(\pmb x) = \begin{cases} \inf_{\pmb y \in \partial S} \|\pmb x - \pmb y\|, & \text{if } \pmb x \in S \\ -\inf_{\pmb y \in \partial S} \|\pmb x - \pmb y\|, & \text{if } \pmb x \notin S \end{cases}$$

该模块为后续障碍物编码提供高效的几何信息，避免了在线数值求解SDF的计算开销。

#### 模块三：改进的Fourier层 $L_{m,PNO}$ —— 障碍物几何硬编码

这是PNO区别于FNO/DAFNO的关键创新。传统Fourier层在频域执行：FFT → 乘以可学习权重矩阵 → IFFT。PNO在此过程中**显式编码障碍物几何**：将可学习权重矩阵乘以一个平滑指示函数 $\tilde{\chi}_{PNO}$：

$$\tilde{\chi}_{PNO}(\mathbf{x}) := \tanh(\beta \, d_S(\pmb x)) \, (1/c(\pmb x) - 0.5) + 0.5$$

其中 $\beta$ 控制平滑程度，$d_S(\pmb x)$ 由辅助FNO提供。该掩码在频域权重上施加空间选择性调制，使模型在障碍物区域和自由空间区域学习不同的特征变换模式。消融实验（Table 2）证实，该编码在未见过的真实城市地图上将L2误差降低约50%。

#### 模块四：Deepnorm投影层 $Q_{PNO}$ —— 三角不等式约束与目标泛化

最优价值函数天然满足三角不等式（最优性原理）：

$$V(\pmb{x}, \pmb{g}) \le V(\pmb{x}, \pmb{y}) + V(\pmb{y}, \pmb{g}), \quad \forall \pmb{x}, \pmb{y}, \pmb{g} \in \mathcal{S}$$

PNO通过Deepnorm投影层结构性地保证该约束。设最后一个隐藏层输出特征 $\phi(\pmb x)$，投影层定义为：

$$Q_{PNO}(\phi, \pmb{x}, \pmb{g}) = f_{\theta_Q}(\phi(\pmb{x}) - \phi(\pmb{g}))$$

其中 $f_{\theta_Q}$ 为小型神经网络。该设计的核心机制是：通过输入特征的**差值**而非绝对位置来预测价值，自动满足 $\|Q(\phi,\pmb x,\pmb g)\| \le \|Q(\phi,\pmb x,\pmb y)\| + \|Q(\phi,\pmb y,\pmb g)\|$ 形式的三角不等式，从而支持零样本目标位置泛化——模型无需将目标坐标作为额外输入通道，也无需为每个新目标重新训练。

---

### 训练损失：混合PINN监督

PNO的训练采用混合损失函数，结合监督学习的L2误差和物理信息约束：

$$\mathrm{Loss}(V, \hat{V}) := \|V - \hat{V}\|_{L^2} + \xi \left( \int_{\pmb{x} \in \mathcal{S}} (\|\nabla \hat{V}(\pmb{x}, \cdot)\| - c(\pmb{x}))^2 \right)^{1/2}$$

- **第一项**：预测价值函数 $\hat{V}$ 与数值求解器（FMM或Dijkstra）生成的真值 $V$ 之间的L2误差。
- **第二项**：Eikonal方程残差，显式约束预测梯度的模长逼近代价函数 $c(\pmb x)$。
- **$\xi$**：平衡两项的权重超参数，需手工调整——过大可能导致模型退化为纯欧几里得范数解，过小则梯度约束不足。

消融实验（Figure 7, Table 2）表明，加入PINN损失后PNO的L2相对误差从0.1136降至0.0698，且价值函数的梯度残差显著减小。

---

### 分辨率不变性的实现机制

PNO的分辨率不变性源于FNO的频域学习范式。Fourier层在频域截断固定数量的低频模态进行卷积，该操作与输入/输出的空间离散化分辨率无关。因此，模型在 $64 \times 64$ 分辨率上训练后，可直接推理 $256 \times 256$ 乃至 $1024 \times 1024$ 的输入（Figure 1），实现最高16倍的超分辨率部署，且无需任何架构修改或微调。

## 实验与关键发现

### 核心实验设置

PNO 的训练数据通过传统数值求解器（FMM 或 Dijkstra）离线生成，覆盖 Grid World、合成 2D 地图、真实城市地图（MovingAI）、3D 建筑环境（iGibson）以及 4-DOF 机械臂 C 空间等多种场景。模型在粗分辨率（如 64×64）上训练，随后零样本部署到更高分辨率（最高 1024×1024）及全新环境，评估指标包括 L2 相对误差、规划成功率、计算时间、节点展开数及路径最优性。

### Grid World 规划性能

在 28×28 Grid World 数据集上，PNO 以 **99.3%** 的平均成功率和 **6.4 ms** 的平均计算时间显著优于基线方法（Table 1）。相比之下，**VIN**（Tamar et al., NIPS 2016）的成功率为 96.7%，计算时间为 82.1 ms；**IEF2D**（Li et al., 2022）的成功率为 97.0%，计算时间为 20.4 ms。PNO 在成功率上比 VIN 高 2.6%，计算速度快 12.8 倍，验证了算子学习范式在离散网格规划中的效率优势。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2410_17547/figures/003_Table_1.jpg]]
*Table 1: Comparison of planning on learned value functions on the Grid World dataset at various sizes*

### 2D 价值函数预测精度

在 MovingAI 合成 2D 地图（64²）上，PNO 的 L2 相对误差为 **0.1136**，使用 PINN 损失后进一步降至 **0.0698**（Table 2）。作为对比，基础 **FNO**（Li et al., 2021）的误差为 0.1996，**DAFNO**（Liu et al., 2023）为 0.0985。PNO 相比 FNO 误差降低 43.1%，PINN 变体再降低 38.6%，表明障碍物编码和梯度约束各自贡献显著。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2410_17547/figures/004_Table_2.jpg]]
*Table 2: Average*

在未见过的真实城市地图（64²）上，PNO 的 L2 误差为 **0.1748**，而 DAFNO 为 0.4090，误差降低 **57.3%**。在 1024² 分辨率下，PNO 的计算速度比 FMM 快约 **10 倍**（Table 5），展示了超分辨率部署的实际价值。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2410_17547/figures/011_Table_5.jpg]]
*Table 5: Computation times for super-resolution calculations average over 1000 instances on the Moving AI lab 2D dataset (642 indicates 64 × 64). The DAFNO SDF was calculated using the SciPy numerical solver. The numerical solver used for FMM is via Pykonal*

### 作为 A* 启发式的规划加速

PNO 作为 A* 的启发式函数，结合障碍膨胀策略，在 MovingAI 2D 城市地图（256²–1024²）上显著减少节点展开（Table 3）。在 1024² 分辨率下，PNO（含膨胀）展开 **41,394** 个节点，而欧几里得范数启发式展开 59,965 个节点，减少约 **31%**，且路径最优性保持为 1.000。若不进行障碍膨胀，节点展开更少（31,676），但路径出现 1.5% 的次优性，表明适量膨胀是平衡效率与最优性的关键。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2410_17547/figures/007_Table_3.jpg]]
*Table 3: Comparison of heuristics for A∗ against classical RRT and RRT∗ over 2D maps. The number of eroded layers is 12, 14, and 18 for 2562 , 5122, and 10242, respectively*

### 消融实验

**障碍物编码的贡献**：Table 2 的消融对比表明，PNO 通过平滑障碍掩码 $\tilde{\chi}_{PNO}$ 将障碍物几何强编码进 Fourier 层，相比无此机制的 FNO 和 DAFNO，在合成和真实地图上均大幅降低 L2 误差，尤其在城市地图上优势更明显。

**PINN 损失的增益**：引入混合 PINN 损失（Eq. 15）后，PNO 的 L2 误差进一步降低，且价值函数的梯度残差显著减小（Figure 7），说明显式约束 $\|\nabla \hat{V}\| = c$ 有助于学习更符合 Eikonal 方程的价值函数。

**Deepnorm 投影层的效果**：PNO 的 Deepnorm 输出层 $Q_{PNO}$ 满足三角不等式，使其能零样本泛化到新目标位置。Table 2 中 PNO 相比 DAFNO 在城市地图上约 50% 的误差降低，主要归因于该投影层的目标泛化能力。

**障碍膨胀深度的影响**：Figure 11 和 Table 3 显示，膨胀层数对启发式性能有显著影响。无膨胀时路径次优，适量膨胀（256² 用 12 层，512² 用 14 层，1024² 用 18 层）可恢复路径最优性并减少节点展开。当前膨胀层数依赖实验选择，缺乏自动调节机制。

### 高维规划与跨环境泛化

**3D 建筑环境**：在 iGibson 的 Bolton 等建筑环境中，PNO 的训练 L2 误差为 0.08，测试误差为 0.19（Figure 3）。相比需要每环境重训练的 **NTFields** 和 **P-NTFields**（Ni & Qureshi, 2023a/2023b），PNO 一次训练后即可零样本部署，并实现约 3 倍的规划加速。Figure 9 展示了 PNO 的最差表现案例，提示在测试环境与训练分布差异过大时预测精度会下降。

**4-DOF 机械臂 C 空间**：在 17⁴ 维 C 空间中，PNO 的训练 L2 相对误差为 0.027，测试误差为 0.041（Figure 4），展示了在高维空间中学习价值函数的可行性。Figure 10 提供了固定关节 3 和关节 4 的价值函数切片可视化。

### 失败模式与局限性

1. **分布外泛化衰减**：当测试地图的障碍物布局与训练分布差异过大时，PNO 的预测精度明显下降（Figure 9 为最差案例），表明模型的泛化边界受限于训练数据的覆盖范围。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2410_17547/figures/016_Figure_9.jpg]]
*Figure 9: A second example of comparison between NTFields, P-NTFields, FMM and PNO unseen during training. This example is the worst-performing example for the PNO in terms of*

2. **启发式次优性**：若不进行障碍膨胀，PNO 启发式可能导致 A* 产生次优路径（Table 3 中次优性 1.015）。膨胀层数目前需手工调节，缺乏自适应机制。

3. **PINN 权重敏感**：混合损失中的权重 $\xi$ 需手工调整，过大可能导致价值函数退化为纯欧几里得范数解，过小则梯度约束不足。

4. **训练数据依赖**：当前 PNO 的训练仍需传统数值求解器离线生成真值，对于极高维 C 空间（7-DOF 及以上）数据生成成本高昂，尚未验证。

5. **非均匀代价未覆盖**：实验仅针对均匀代价（最小时间）规划，未处理非均匀代价（如风险偏好、能量最优）的环境。

### 计算效率总览

Table 5 汇总了不同算法在 2D 数据集上的超分辨率计算时间。在 1024² 分辨率下，PNO 的推理时间远低于 FMM 数值求解器，且 DAFNO 的 SDF 计算依赖 SciPy 数值求解器，进一步凸显 PNO 端到端学习的效率优势。Table 4 和 Table 6 分别记录了 PNO 在 Grid World 和作为神经启发式时的模型参数量与性能指标，显示模型规模与任务复杂度正相关。

## 定位与知识库关联

### 从值迭代近似到算子学习：核心范式转换

传统神经运动规划方法将价值函数预测建模为**从环境到价值的映射**，而非从代价函数空间到价值函数空间的算子近似。这一根本差异决定了泛化能力的边界。具体而言：

- **VIN**（Tamar et al., NIPS 2016）通过CNN端到端近似值迭代过程，在离散Grid World上实现了端到端规划。然而，其卷积架构固有地绑定于训练分辨率和特定环境拓扑，无法零样本迁移到新地图或更高分辨率场景。Table 1显示VIN在28×28 Grid World上成功率为96.7%，但计算时间高达82.1 ms，且未见跨环境泛化能力。

- **IEF2D/IEF3D**（Li et al., 2022）引入隐式函数和自编码器学习场景签名距离及路径，在跨环境泛化上迈出一步。但该方法仍需将目标位置作为额外输入通道，且未从算子学习角度处理分辨率不变性问题。Table 1中IEF2D成功率为97.0%，计算时间20.4 ms，在Grid World上优于VIN但仍逊于PNO。

- **NTFields**（Ni & Qureshi, 2023a）和**P-NTFields**（Ni & Qureshi, 2023b）基于PINN求解Eikonal方程，可泛化到不同目标位置。但其核心局限在于**每环境需重新训练**——每次遇到新场景都需进行数千次梯度下降迭代，这从根本上限制了实时部署。在iGibson 3D环境中（Figure 3），PNO无需重训练即可获得与NTFields可比甚至更优的L2误差（测试集0.19），同时实现3倍于FMM的加速。

PNO的关键范式转换在于：将价值函数近似重构为学习**连续算子** $\Psi: c(\mathbf{x}) \mapsto V(\mathbf{x})$，该算子由Eikonal PDE定义。这使得单一模型在训练后能够泛化到任意新代价函数（对应新环境）、任意分辨率和任意目标位置，而无需重新训练或微调。

### 架构创新在知识库中的定位

PNO的架构设计（Figure 2）可分解为三个在现有知识库中有明确锚点的创新模块，每个模块针对特定瓶颈：

**1. 频域学习与分辨率不变性：继承自FNO谱系**

PNO的基础架构继承自**FNO**（Li et al., 2021），后者通过在Fourier空间学习积分核算子实现了对PDE解算子的分辨率不变近似。FNO的核心优势在于：在频域截断固定数量的模式后，模型参数独立于空间离散化分辨率。PNO直接继承了这一特性，使其能在64×64分辨率训练后直接推理1024×1024地图（Figure 1），实现16倍超分辨率部署。Table 2消融实验中，纯FNO在合成2D地图上L2误差为0.1996，验证了频域学习在运动规划中的可行性，但也暴露了缺乏障碍物感知能力的不足。

**2. 障碍物几何编码：DAFNO思想的深化与泛化**

**DAFNO**（Liu et al., 2023）针对非矩形域引入掩码机制，将域几何信息注入Fourier层。PNO将这一思想显著深化：通过平滑指示函数

$$\tilde{\chi}_{PNO}(\mathbf{x}) := \tanh(\beta d_S(\mathbf{x})) (1/c(\mathbf{x}) - 0.5) + 0.5$$

将障碍物几何**强编码**进Fourier层权重乘法中。该设计的精巧之处在于：(a) 利用 $\tanh$ 平滑化避免梯度断裂；(b) 通过符号距离函数 $d_S$ 编码障碍物距离信息，而非仅使用二值占据；(c) 引入辅助SDF FNO独立预测 $d_S$，避免昂贵的在线数值求解。Table 2的消融实验提供了决定性证据：DAFNO在真实城市地图上L2误差为0.4090，而PNO降至0.1748（降幅57.3%），证明了平滑障碍编码相较于简单掩码的显著增益。

**3. 三角不等式约束与目标泛化：Deepnorm投影层**

PNO的投影层 $Q_{PNO}(\phi, \mathbf{x}, \mathbf{g}) = f_{\theta_Q}(\phi(\mathbf{x}) - \phi(\mathbf{g}))$ 通过构造自动满足三角不等式。这一设计的理论依据来自最优价值函数的必要条件：$V(\mathbf{x}, \mathbf{g}) \le V(\mathbf{x}, \mathbf{y}) + V(\mathbf{y}, \mathbf{g})$。在知识库中，该约束此前未被显式引入神经运动规划架构。Table 2中PNO相较于DAFNO在城市地图上约50%的L2误差降低，可主要归因于Deepnorm层带来的目标泛化能力提升（DAFNO无此层，需将目标作为额外输入通道处理）。此外，该层使得PNO能够作为**ε一致启发式**嵌入A*框架（Section 5），理论保证 $\epsilon = \max_{\{x, y \in S | x \neq y\}} 1 + 2\epsilon_{NO} / V(x, y)$。

**4. 混合PINN损失：物理约束的注入**

PNO的训练损失

$$\mathrm{Loss}(V, \hat{V}) := \|V - \hat{V}\|_{L^2} + \xi \left( \int_{x \in S} (\|\nabla \hat{V}(\mathbf{x}, \cdot)\| - c(\mathbf{x}))^2 \right)^{1/2}$$

在标准L2监督之外显式约束梯度满足Eikonal方程。这一设计借鉴了PINN范式，但应用于算子学习而非单场景优化。Figure 7的消融显示，PINN损失不仅降低L2误差（Table 2中从0.1136降至0.0698），更显著改善了价值函数的梯度残差分布，使得后续基于梯度的路径提取更加稳定。

### 适用边界与局限

尽管PNO在多个维度展现了强大的泛化能力，其适用边界和局限需明确界定：

**1. 代价函数的均匀性假设**

当前PNO针对最小时间运动规划设计，代价函数简化为 $c(\mathbf{x}) = 1$（安全集内）或 $\infty$（障碍物）。这一假设使得Eikonal方程 $\|\nabla V\| = c$ 退化为均匀代价形式。对于非均匀代价（如风险偏好地图、能量最优、各向异性代价），Eikonal方程虽仍成立，但PNO的障碍编码机制（$\tilde{\chi}_{PNO}$ 中 $1/c(\mathbf{x})$ 项）和训练数据生成流程需重新设计。论文明确指出此为当前局限，且未在非均匀代价场景验证。

**2. 训练数据依赖传统求解器**

PNO的训练真值仍需通过FMM或Dijkstra离线生成。在2D/3D场景中，这一成本可控；但在高维C空间（如7-DOF以上机械臂），数值求解器的计算开销呈指数增长，可能抵消PNO推理阶段的加速优势。当前实验最高验证至4-DOF（Figure 4，17⁴维C空间），测试L2误差0.041表现优异，但更高维度的数据生成可行性仍是开放问题。

**3. 分布外泛化的退化风险**

尽管PNO具有分辨率不变性，当地图拓扑分布与训练集差异过大时，预测精度仍会下降。Figure 9展示了PNO在未见环境中的最差表现案例，提示当前架构对极端未见拓扑的泛化能力有限。这一局限与训练数据的多样性直接相关——论文使用的MovingAI城市地图虽具代表性，但未涵盖所有可能的环境结构。

**4. 障碍膨胀的启发式工程**

PNO作为A*启发式时，需引入障碍膨胀（erosion）以保证路径最优性。Table 3显示：无膨胀时路径次优（次优比1.015），适量膨胀后恢复最优（次优比1.000）且节点展开减少33%。然而，膨胀层数的选择目前依赖实验调参（256²用12层，512²用14层，1024²用18层），缺乏自适应机制。Figure 11虽展示了膨胀深度对性能的影响趋势，但未提供自动选择策略。

**5. PINN损失权重的敏感性**

混合损失中的权重 $\xi$ 需手工调整：过大可能导致模型退化为纯欧几里得范数解（梯度约束过强抑制数据拟合），过小则梯度约束不足。论文未给出 $\xi$ 的系统调参方法或自适应策略，这在实际部署中可能成为工程负担。

### 开放问题与未来方向

基于上述局限，论文引出以下开放问题：

1. **非均匀代价的算子学习**：如何扩展PNO架构以处理 $c(\mathbf{x})$ 为空间变化函数（如风险地图、能量场）的场景，同时保持三角不等式约束和障碍编码的有效性？这可能需要重新设计 $\tilde{\chi}_{PNO}$ 中的代价依赖项，并在训练数据中引入多样的代价分布。

2. **动态启发式与增量规划**：PNO的快速推理能力（1024²地图约10 ms，比FMM快约10倍）使其天然适合作为动态启发式。能否将PNO嵌入LPA*或D* Lite框架，在环境动态变化时仅局部更新启发式，实现实时重规划？

3. **自适应障碍膨胀**：能否通过学习或优化方法自动选择膨胀层数？例如，基于局部障碍密度或路径曲率动态调整膨胀深度，在路径最优性和节点展开数之间实现更精细的权衡。

4. **高维C空间的扩展验证**：PNO在4-DOF C空间中的成功（4.1%相对误差）提示其可能适用于更高维度。但需解决：(a) 高维训练数据生成的计算瓶颈；(b) Fourier层在高维网格上的内存和计算开销；(c) 高维空间中符号距离函数的有效近似。

5. **与其他PDE解算子的统一**：PNO的障碍编码和Deepnorm投影层是否可推广到其他PDE解算子学习任务？例如，Hamilton-Jacobi方程的更一般形式可能受益于类似的几何约束注入机制。

6. **训练数据多样性的系统性增强**：为缓解分布外泛化退化，能否结合生成模型（如扩散模型或GAN）在训练中引入更多样的地图拓扑，或通过数据增强策略（如随机障碍物放置、拓扑变形）提升模型的鲁棒性？

## 原文 PDF

![[paperPDFs/arxiv_2024/Generalizable_Motion_Planning_via_Operator_Learning.pdf]]
