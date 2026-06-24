---
title: "MDP: Multidimensional Vision Model Pruning with Latency Constraint"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/MDP_Multidimensional_Vision_Model_Pruning_with_Latency_Constraint.pdf
project_link: https://github.com/NVlabs/MDP
aliases:
- MMDP
- MDP
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入多维联合剪枝（通道、层、块），通过构建双线性延迟矩阵精确捕获输入/输出通道组合的延迟，并利用块分组将层‑块决策统一纳入 MINLP 进行全局优化，从而在单次求解中获得全局最优的剪枝结构。"
primary_logic: "将剪枝重新形式化为混合整数非线性规划（MINLP），利用完整的延迟成本矩阵和块分组策略同时搜索通道数、层/块保留方案，突破传统迭代式剪枝的局部性，在大剪枝比下实现了精度与速度的帕累托前沿显著提升。"
claims:
- "ImageNet 上 ResNet50 剪枝 85% 时，MDP 达到 Top‑1 70.0%、FPS 5262，大幅优于 HALP 的 68.6%、4101 FPS。"
- "NuScenes 3D 检测中，剪枝 StreamPETR 45%，MDP 获得 mAP 0.451、FPS 37.3，超过密集基线（0.449 mAP, 31.7 FPS）。"
- "消融实验表明，双线性延迟建模和块分组各自独立地改善了精度‑延迟曲线，组合后获得最佳表现。"
- "ImageNet (ResNet50) 上 Top‑1 Accuracy / FPS = 70.0% / 5262 (Ours-85%)"
---

# MDP: Multidimensional Vision Model Pruning with Latency Constraint

> [!tip] 核心洞察
> 将剪枝重新形式化为混合整数非线性规划（MINLP），利用完整的延迟成本矩阵和块分组策略同时搜索通道数、层/块保留方案，突破传统迭代式剪枝的局部性，在大剪枝比下实现了精度与速度的帕累托前沿显著提升。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MDP：带延迟约束的多维视觉模型剪枝 |
| 英文题名 | MDP: Multidimensional Vision Model Pruning with Latency Constraint |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2406.12079); [GitHub](https://github.com/NVlabs/MDP) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MDP (Multi-Dimensional Pruning) |
| Dataset | ImageNet (ResNet50), ImageNet (ResNet50, EagleEye setting), NuScenes (StreamPETR) |

> [!tip] 效果简介
> - ImageNet (ResNet50) 上，Top‑1 Accuracy / FPS 为 70.0% / 5262 (Ours-85%)，对比 68.6% / 4101 (HALP-85%)，变化 +1.4% / +1161。
> - ImageNet (ResNet50, EagleEye setting) 上，Top‑1 Accuracy / FPS 为 75.0% / 3052 (Ours-70%)，对比 74.5% / 2597 (HALP-70%)，变化 +0.5% / +455。
> - NuScenes (StreamPETR) 上，mAP / FPS 为 0.451 / 37.3 (Ours-45%)，对比 0.449 / 31.7 (Dense)，变化 +0.002 / +5.6。

## 概述

现有神经网络剪枝方法主要局限于**通道级剪枝**，难以在高剪枝比（70%–90%）下安全移除整层或整块，导致精度大幅下降。同时，延迟建模仅考虑输出通道变化，忽略输入通道的联动变化，使高剪枝比下的精度‑延迟优化严重偏离真实目标。

针对上述瓶颈，本文提出 **MDP（Multi-Dimensional Pruning）**，一种带延迟约束的**多维联合剪枝**框架。核心思路是将剪枝重新形式化为**混合整数非线性规划（MINLP）**：通过构建**双线性延迟矩阵**精确捕获输入/输出通道组合的延迟，并利用**块分组**策略将层‑块决策统一纳入全局优化，在单次求解中获得全局最优的剪枝结构。

主要结果：
- **ImageNet 分类**（ResNet50）：85% 剪枝比下，MDP 达到 Top‑1 70.0%、FPS 5262，显著优于 HALP（68.6%、4101 FPS）；70% 剪枝比下，Top‑1 75.0%、FPS 3052，优于 HALP（74.5%、2597 FPS）。
- **NuScenes 3D 检测**（StreamPETR）：45% 剪枝比下，MDP 获得 mAP 0.451、FPS 37.3，超过密集基线（0.449 mAP, 31.7 FPS）；70% 剪枝比下，mAP 0.394、FPS 43.3，优于 HALP（0.373、42.5 FPS）。
- **Pascal VOC 检测**（SSD512‑RN50）：MDP 达到 mAP 80.0、FPS 125.4，显著超越密集基线（78.0、68.2 FPS）。

消融实验进一步验证了双线性延迟建模和块分组各自独立地改善了精度‑延迟曲线，二者组合获得最佳表现。

## 背景与动机

深度卷积神经网络在图像分类、目标检测等视觉任务上取得了卓越性能，但其庞大的计算量与存储开销严重制约了在资源受限边缘设备上的实时部署。模型剪枝作为最直接的压缩手段之一，旨在移除冗余参数以降低推理延迟，同时尽可能保持原始精度。

### 现有剪枝范式的瓶颈

当前主流的硬件感知剪枝方法，如 **HALP**（Shen et al., NeurIPS 2022）和 **SMCP**（Humble et al., ECCV 2022），几乎完全聚焦于通道级剪枝——即仅削减每层卷积核的输出通道数，而保留完整的网络深度与拓扑结构。这一范式的根本局限在于：当剪枝比推高至 70%–90% 时，大量层被迫压缩至极少数通道，但整层或整块的冗余结构依然存在，导致精度急剧坍塌，而延迟收益却趋于饱和。

更关键的是，现有方法的延迟模型存在系统性偏差。它们通常仅在固定输入通道数的前提下测量输出通道变化对延迟的影响，完全忽略了输入通道的联动效应。在深层网络中，前一层的输出通道即是当前层的输入通道，这种耦合关系使得仅建模单侧通道变化的延迟预测在高剪枝比下严重偏离真实硬件行为，进而误导整个优化过程。

### 从单维到多维剪枝的动机

上述瓶颈揭示了一个被长期忽视的事实：**真正高效的剪枝必须同时考虑“宽度”（通道数）与“深度”（层/块保留）两个维度**。在极端压缩场景下，直接移除整个残差块或特定层，往往比将所有层均匀瘦身更能保全关键表示能力。

然而，将通道、层、块三种粒度的决策统一纳入优化并非易事。层与块之间存在天然的层次依赖关系，且搜索空间呈组合爆炸。传统方法依赖迭代贪婪或背包求解，每一步的局部最优无法保证全局结构的最优性，且难以在单次优化中协调多维决策。

### 本文的核心动机与思路

针对上述缺口，本文提出 **MDP（Multi-Dimensional Pruning）**，核心动机可概括为三点：

1. **多维联合剪枝的必要性**：在高剪枝比下，仅靠通道剪枝已触及精度‑延迟的帕累托边界，必须引入层与块级剪枝来突破这一瓶颈。
2. **延迟建模的精确化**：需要一种能够同时捕获输入与输出通道变化对延迟影响的建模方式，使优化目标与真实硬件行为对齐。
3. **全局最优的单次求解**：将多维剪枝重新形式化为一个混合整数非线性规划（MINLP），在延迟约束下一次性求解所有决策变量，避免迭代式剪枝的局部性缺陷。

通过上述设计，MDP 在 ImageNet 分类与 NuScenes 3D 检测等任务上均展现了显著的帕累托前沿提升——在 85% 剪枝比下，ResNet50 的 Top‑1 精度达到 70.0%，FPS 达到 5262，大幅超越 HALP 的 68.6% 与 4101 FPS（Table 1）。

## 核心创新

MDP 的核心创新在于将传统仅限通道级的剪枝范式重构为**通道‑层‑块联合多维剪枝**，并通过**单次全局优化**替代迭代局部搜索，从而在高剪枝比下实现精度与延迟的帕累托前沿显著提升。这一突破由三个关键 changed slots 共同支撑。

### 从单维通道剪枝到多维联合剪枝

现有硬件感知剪枝方法（如 **HALP**，Shen et al., NeurIPS 2022）仅支持通道级剪枝，当剪枝比推高至 70%–90% 时，无法安全地移除整层或整块，导致精度大幅下降。MDP 引入**块分组策略**，将层按残差块分组并引入块决策变量 $z$，使求解器可以同时决定通道保留数、整层删除和整块删除。这一设计将剪枝粒度从单维扩展至多维，突破了高剪枝比下的结构瓶颈。

### 从不完整延迟模型到双线性配置延迟矩阵

HALP 等方法的延迟模型仅考虑固定输入通道下输出通道数的变化，忽略了输入通道的联动影响，导致高剪枝比下精度‑延迟优化严重偏离真实目标。MDP 为目标硬件逐层构建**双线性延迟成本矩阵**：

$$\mathbf{C}_l = \begin{bmatrix} T_l(1,1) & \cdots & T_l(1,m_l) \\ \vdots & \ddots & \vdots \\ T_l(m_{l-1},1) & \cdots & T_l(m_{l-1},m_l) \end{bmatrix}$$

该矩阵完整记录了所有输入/输出通道组合下的延迟，使优化器能够精确评估任意剪枝配置的真实推理延迟。消融实验表明，仅引入该延迟建模即可在精度‑延迟曲线上显著优于基线（Fig. 4）。

### 从迭代局部优化到单次 MINLP 全局优化

传统方法依赖迭代贪婪或背包求解，每次剪枝仅做局部决策，最终结构远非全局最优。MDP 将剪枝重新形式化为**混合整数非线性规划（MINLP）**，以总重要性最大化为目标、总双层延迟为约束：

$$\underset{\pmb{y},\pmb{z}}{\arg\operatorname*{max}} \sum_{l=1}^{L} \boldsymbol{z}_{\beta(l)} \cdot \left(\pmb{y_l}^{\top} \cdot \hat{\pmb{\mathcal{T}}_l}\right) \quad \text{s.t.} \quad \sum_{l=1}^{L} z_{\beta(l)} \cdot \left(\pmb{y}_l \cdot \left(\pmb{y}_{l-1}^{\top} \cdot \mathbf{C}_l\right)\right) \leq \Psi$$

配合 one‑hot 约束 $\pmb{y}_l^{\top} \cdot \mathbf{1} = 1$，使用 Pyomo/MindtPy 的 Outer Approximation 方法一次性求解所有决策变量。实验显示，在单步剪枝设置下，MDP 显著优于 HALP——后者因延迟模型不准确导致性能崩溃（Table 3）。这一范式转变使得 MDP 在 ResNet50 上仅需约 5 秒即可获得全局最优剪枝结构。

## 整体框架

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2406_12079/figures/002_Figure_2.jpg]]
*Figure 2: Paradigm of our proposed method MDP. We start by computing layer importance and constructing latency cost matrices for each layer. We then group layers within the same block and solve an MINLP to optimize pruning decisions at both channel and block levels. Finally, we extract the pruned subnetwork and finetune it*

MDP 的整体流程围绕一个核心思想展开：将多维剪枝（通道、层、块）统一形式化为一个带延迟约束的混合整数非线性规划（MINLP），并在单次求解中直接获得全局最优的子网络结构。整个 pipeline 包含五个关键模块，按执行顺序构成一条端到端的剪枝流水线，如 Figure 2 所示。

**第一步：层重要性计算。** 对于待剪枝的预训练模型，MDP 首先在目标数据集上运行一个 epoch 的前向传播，利用泰勒准则逐通道计算重要性分数。具体而言，第 $l$ 层第 $j$ 个通道的重要性由 BatchNorm 参数 $\gamma_l^j$、$\beta_l^j$ 及其梯度决定：

$$\mathcal{T}_l^j = |g_{\gamma_l^j} \gamma_l^j + g_{\beta_l^j} \beta_l^j|$$

之后，将每层所有通道的重要性聚合为层重要性向量 $\hat{\mathcal{T}}_l$，其第 $i$ 个分量 $\hat{\mathcal{T}}_l^i$ 表示该层保留 $i$ 个最重要通道时的总重要性（即前 $i$ 大通道重要性之和）。这一步骤为后续的 MINLP 提供了各层在不同通道数下的“价值”度量。

**第二步：延迟矩阵构建。** 传统硬件感知剪枝的延迟模型通常只考虑输出通道数的变化，忽略了输入通道数同样会随前层剪枝而改变。MDP 的核心改进之一是为目标硬件预构建每层的双线性配置延迟查找表，并将其组织为延迟成本矩阵 $\mathbf{C}_l$：

$$\mathbf{C}_l = \begin{bmatrix} T_l(1,1) & \cdots & T_l(1,m_l) \\ \vdots & \ddots & \vdots \\ T_l(m_{l-1},1) & \cdots & T_l(m_{l-1},m_l) \end{bmatrix}$$

其中 $T_l(i,j)$ 是输入通道数为 $i$、输出通道数为 $j$ 时该层的实测延迟。该矩阵精确捕获了输入与输出通道的联动变化对延迟的影响，是高剪枝比下精度‑延迟优化不偏离真实目标的关键保障。

**第三步：块分组。** 为将整层删除和整块删除统一到同一优化框架中，MDP 将具有残差连接的层按所属 block 进行分组，并为每个 block 引入一个二值决策变量 $z_{\beta(l)}$。当 $z_{\beta(l)} = 0$ 时，该 block 内所有层被整体移除；当 $z_{\beta(l)} = 1$ 时，block 内的各层仍可通过通道决策变量 $\mathbf{y}_l$ 进行独立的通道稀疏化。这一设计使得优化器可以同时权衡“块级粗粒度删除”与“通道级细粒度稀疏”两种策略。

**第四步：MINLP 建模与求解。** 将上述重要性向量、延迟矩阵和块分组变量整合后，MDP 将剪枝问题形式化为以下 MINLP：

目标函数最大化被保留通道和块的总重要性：
$$\underset{\pmb{y},\pmb{z}}{\arg\operatorname*{max}} \sum_{l=1}^{L} \boldsymbol{z}_{\beta(l)} \cdot \left(\pmb{y_l}^{\top} \cdot \hat{\pmb{\mathcal{T}}_l}\right)$$

约束条件为总双层配置延迟不超过预算 $\Psi$：
$$\sum_{l=1}^{L} z_{\beta(l)} \cdot \left(\pmb{y}_l \cdot \left(\pmb{y}_{l-1}^{\top} \cdot \mathbf{C}_l\right)\right) \leq \Psi$$

同时每层只能选择一个通道数（one‑hot 约束）：
$$\pmb{y}_l^{\top} \cdot \mathbf{1} = 1, \forall l \in [1, L]$$

该 MINLP 使用 Pyomo 建模并通过 MindtPy 的外逼近（Outer Approximation）算法求解。在 ResNet‑50 上，整个求解过程仅需约 5 秒，即可输出全局最优的 $\mathbf{y}$ 和 $\mathbf{z}$ 决策变量。

**第五步：剪枝结构提取与微调。** 根据求解器输出的决策变量，MDP 提取对应的子网络结构——保留 $\mathbf{y}_l$ 指定的通道数，移除 $z_{\beta(l)} = 0$ 的整块——然后在原数据集上微调 $E$ 个 epoch 以恢复精度。微调超参数（学习率、epoch 数等）按经验设定，各数据集的具体配置见 Table 5。

整个 pipeline 的关键优势在于**单次求解的全局性**：与 HALP 等需要多步迭代（最多 30 步）的贪婪式剪枝不同，MDP 在一个统一的优化问题中同时决定所有层的通道数和所有块的去留，从根本上避免了迭代式方法因延迟模型不准确而导致的误差累积和性能崩溃（消融实验中，HALP 在单步设置下性能显著劣化，见 Table 3）。

## 核心模块与公式推导

MDP 将多维剪枝形式化为一个混合整数非线性规划（MINLP），其核心由四个模块串联构成：层重要性计算、延迟矩阵构建、块分组、以及 MINLP 建模与求解。以下逐一展开。

### 层重要性计算

剪枝的首要问题是“哪些通道更重要”。MDP 采用基于 Taylor 展开的准则，利用 BatchNorm 层的缩放因子 $\gamma$ 和偏置 $\beta$ 及其梯度来估计每个通道的重要性。对于第 $l$ 层第 $j$ 个通道，其重要性定义为：

$$\mathcal{T}_l^j = |g_{\gamma_l^j} \gamma_l^j + g_{\beta_l^j} \beta_l^j|$$

其中 $g_{\gamma_l^j}$ 和 $g_{\beta_l^j}$ 分别为损失函数对 $\gamma_l^j$ 和 $\beta_l^j$ 的梯度。该公式本质上衡量了移除该通道对损失的近似一阶影响。

得到逐通道重要性后，需要将其聚合为“层在保留 $i$ 个通道时的总重要性”，以便后续优化器在不同通道数之间做选择。MDP 将层 $l$ 的所有通道重要性从大到小排序，取前 $i$ 个求和：

$$\hat{\mathcal{T}}_l^i = \sum \mathrm{Top\text{-}i}(\pmb{\mathbb{T}}_l), \quad \forall i \in [1, m_l]$$

其中 $m_l$ 为层 $l$ 的原始通道数。这一聚合方式隐含了一个合理假设：剪枝时总是优先保留最重要的通道。

### 双线性延迟矩阵构建

传统硬件感知剪枝在建模延迟时，通常只考虑输出通道数的变化，而将输入通道数固定为原始值。这在高剪枝比下会导致严重的延迟估计偏差——因为前一层的输出通道数（即当前层的输入通道数）同样被大幅削减，两层联动变化对实际延迟的影响不可忽略。

MDP 通过构建**双线性配置延迟矩阵**来精确捕获这种联动效应。对于卷积层 $l$，其延迟成本矩阵 $\mathbf{C}_l$ 为一个 $m_{l-1} \times m_l$ 的查找表：

$$\mathbf{C}_l = \begin{bmatrix} T_l(1,1) & \cdots & T_l(1,m_l) \\ \vdots & \ddots & \vdots \\ T_l(m_{l-1},1) & \cdots & T_l(m_{l-1},m_l) \end{bmatrix}$$

其中 $T_l(c_{in}, c_{out})$ 表示当输入通道数为 $c_{in}$、输出通道数为 $c_{out}$ 时，该层在目标硬件上的实测延迟。该矩阵通过在实际硬件上逐配置测量获得，为 MINLP 提供了高保真的延迟约束基础。

### 块分组

仅进行通道剪枝无法移除整个残差块，而粗暴地删除整块又可能破坏网络结构。MDP 引入**块分组**机制，将属于同一残差块的所有层归为一组，并引入二元块决策变量 $\boldsymbol{z}$。对于块 $b$，$z_b = 1$ 表示保留该块，$z_b = 0$ 表示整块删除。

块分组后，层 $l$ 的贡献（重要性与延迟）被乘以 $z_{\beta(l)}$，其中 $\beta(l)$ 将层 $l$ 映射到其所属的块索引。当 $z_{\beta(l)} = 0$ 时，该层及其所有通道选择对目标函数和约束的贡献均为零，实现整块删除。当 $z_{\beta(l)} = 1$ 时，层内仍可通过通道选择变量 $\boldsymbol{y}_l$ 进行细粒度的通道剪枝。这一设计将层删除、块删除和通道稀疏化统一到同一优化框架中。

### MINLP 建模与求解

将上述模块整合后，MDP 将剪枝问题形式化为如下 MINLP：

**目标函数**——最大化被保留结构的总重要性：

$$\underset{\pmb{y},\pmb{z}}{\arg\operatorname*{max}} \sum_{l=1}^{L} \boldsymbol{z}_{\beta(l)} \cdot \left(\pmb{y_l}^{\top} \cdot \hat{\pmb{\mathcal{T}}_l}\right)$$

**延迟约束**——总双层配置延迟不超过预算 $\Psi$：

$$\sum_{l=1}^{L} z_{\beta(l)} \cdot \left(\pmb{y}_l \cdot \left(\pmb{y}_{l-1}^{\top} \cdot \mathbf{C}_l\right)\right) \leq \Psi$$

其中 $\boldsymbol{y}_l$ 是层 $l$ 的 one-hot 通道选择向量，$\boldsymbol{y}_l \cdot (\boldsymbol{y}_{l-1}^{\top} \cdot \mathbf{C}_l)$ 精确地从延迟矩阵中查表得到当前输入/输出配置下的延迟值。

**One-hot 约束**——每层只能选择一个通道数：

$$\pmb{y}_l^{\top} \cdot \mathbf{1} = 1, \quad \forall l \in [1, L]$$

该 MINLP 使用 Pyomo 建模并通过 MindtPy 中的 Outer Approximation 方法求解。在 ResNet50 上，求解时间仅约 5 秒。求解完成后，根据 $\boldsymbol{y}$ 和 $\boldsymbol{z}$ 的取值直接提取剪枝子网络，经微调恢复精度。

> **注意**：块分组仅适用于具有残差连接的结构。对于无跳跃连接的网络层，块删除不可行，只能通过通道剪枝将其降至 1 个通道。

## 实验与分析

### 核心实验设置

MDP 的实验覆盖图像分类、2D 目标检测和 3D 目标检测三大视觉任务，所有方法均使用相同的预训练权重和微调超参数，FPS 在统一硬件上测量（ResNet50 使用 NVIDIA TITAN V，StreamPETR 使用 RTX 3090），确保比较公平。剪枝在模型遍历完整数据集一个 epoch 后执行，此时累积的重要性估计已充分收敛；随后对提取的子网络进行固定轮数的微调以恢复精度。

### 图像分类主结果（ImageNet, ResNet50）

Table 1 汇总了 ResNet50 在 ImageNet 上的分类结果，按相近 FPS 分组对比。MDP 在高剪枝比下展现出压倒性优势：

- **85% 剪枝比**：MDP 达到 Top‑1 70.0%、FPS 5262，相较 HALP（Shen et al., NeurIPS 2022）的 68.6%、4101 FPS，精度提升 1.4 个百分点，FPS 提升 28.3%。
- **80% 剪枝比**：MDP 的 72.8% Top‑1、4210 FPS 优于 SMCP（Humble et al., ECCV 2022）的 72.7%、3784 FPS，在精度持平的同时获得显著加速。
- **70% 剪枝比（EagleEye 设置）**：MDP 达到 75.0%、3052 FPS，超越 HALP 的 74.5%、2597 FPS，精度和速度双赢。
- **与仅层剪枝方法对比**：MDP 在相近精度下（74.6% vs. 74.3%）的 FPS 为 3092，是 LayerPrune-Imprint 的 1828 FPS 的 1.69 倍，说明单纯层剪枝在速度收益上远不如多维联合剪枝。

Figure 1 左图展示了 FPS 与 Top‑1 精度的帕累托前沿：MDP 的曲线在所有剪枝比下均位于 HALP 等基线之上，尤其在 85% 极端剪枝比下，MDP 以 2% 的相对精度增益和 28.3% 的 FPS 提升形成绝对支配。


![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2406_12079/figures/001_Figure_1.jpg]]
*Figure 1: MDP exhibits Pareto dominance across different tasks. In contrast to existing methods: [Left] On Imagenet classification, we achieve a 6.2% relative accuracy gain with a 2.6% FPS speedup, and even greater gains at higher pruning ratio: a 2% relative gain with a substantial 28.3% FPS speedup. [Right] On NuScenes 3D object detection, we observe a 5.6% relative mAP improvement alongside a 1.8% FPS increase*

### 目标检测结果

**Pascal VOC（SSD512-RN50）**：如 Figure 3 所示，MDP 剪枝后的模型在 mAP 和 FPS 两个维度上均超越密集基线——mAP 从 78.0 提升至 80.0，FPS 从 68.2 跃升至 125.4（提升 83.9%），实现了“精度反超+大幅加速”的双重收益。在 mAP‑FLOPs 帕累托图上也呈现类似优势。


![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2406_12079/figures/006_Figure_3.jpg]]
*Figure 3: PascalVOC results with SSD512. FPS is measured on NVIDIA TITAN V with batch size of 256. Ours achieve much better mAP-FPS and mAP-FLOPs tradeoffs than the baselines. Table 2: Nuscenes results with StreamPETR. FPS is measured on NVIDIA GeForce RTX 3090 with batch size of 1. Results with similar FPS are grouped. −X% denote the pruning ratio. Ours achieve much better accuracy-FPS tradeoffs than HALP and even surpass performance of dense StreamPETR with much higher FPS*

**NuScenes 3D 检测（StreamPETR）**：Table 2 展示了更具挑战性的 3D 检测场景下的结果：
- **45% 剪枝比**：MDP 获得 mAP 0.451、FPS 37.3，超越密集基线 StreamPETR（Wang et al., ICCV 2023）的 0.449 mAP、31.7 FPS，在精度微涨的同时加速 17.7%。
- **70% 剪枝比**：MDP 以 mAP 0.394、NDS 0.512、FPS 43.3 大幅领先 HALP 的 mAP 0.373、NDS 0.489、FPS 42.5，mAP 优势达 0.021（相对提升 5.6%）。

Figure 1 右图直观展示了 MDP 在 3D 检测任务上的帕累托支配地位。

### 消融实验

**双线性延迟建模与块分组的独立贡献**（Figure 4）：

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2406_12079/figures/008_Figure_4.jpg]]
*Figure 4: Ablation study results on Ima- Table 3: Ablation study results on geNet with ResNet50. We show results ImageNet with ResNet50. We show reof each improvement acting individually. sults of ours and HALP [54] with different Top-right is better. pruning steps*

- 仅引入双线性延迟成本矩阵（无块分组）时，精度‑延迟曲线已显著优于仅考虑输出通道变化的基线延迟模型，验证了同时建模输入/输出通道变化对准确估计延迟的关键作用。
- 仅引入块分组（使用基线延迟模型）时，在高剪枝比下精度‑延迟权衡明显改善，证明块级删除为优化器提供了额外的自由度。
- 两者组合（完整 MDP）在所有延迟预算下均取得最佳表现，说明两项改进具有互补性。

**单次剪枝 vs. 迭代剪枝**（Table 3）：
- 当剪枝步数从 30 步降至 1 步时，HALP 因延迟模型不准确导致性能严重退化，而 MDP 在单步设置下依然保持稳定优势。这源于 MDP 的 MINLP 全局优化范式：一次性确定所有决策变量，无需依赖迭代过程中的中间延迟估计。

**跨硬件泛化**（Table 4）：在 Intel CPU Xeon E5 上的推理测试表明，MDP 剪枝模型的加速优势在 CPU 端同样成立，验证了延迟矩阵方法对硬件平台的良好适应性。


![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2406_12079/figures/010_Table_4.jpg]]
*Table 4: Results on Intel CPU Xeon E5*

### 剪枝结构可视化

Figure 5 展示了 MDP 剪枝后的 ResNet50 架构。高剪枝比下，MDP 不仅大幅压缩了各层的通道数，还直接删除了若干完整的残差块，这是传统纯通道剪枝方法无法实现的结构级优化。

### 失败模式与局限性

1. **残差依赖**：块删除机制依赖于残差连接的存在。对于无跳跃连接的纯前馈网络，MDP 只能将层剪枝到 1 个通道，无法安全地整层移除，多维剪枝的收益会打折扣。
2. **查找表构建成本**：双线性延迟矩阵需要为目标硬件逐层预测量 $m_{l-1} \times m_l$ 个配置的延迟。当模型或硬件平台变更时需重新测量，增加了部署的工程开销。
3. **求解器可扩展性**：尽管 MINLP 在 ResNet50 上求解仅需约 5 秒，但在超大规模模型（如 ViT-Huge）上的求解时间和内存消耗尚未验证，可能需要引入近似求解或分解策略。
4. **微调超参数未优化**：剪枝后的微调学习率、epoch 数等直接按经验设定，未针对每个剪枝结构进行调优，精度恢复可能未达到理论上限。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2406_12079/figures/005_Figure.jpg]]
*Figure: (a) FPS versus mAP are plotted(top-right is better). FPS measured on NVIDIA TITANV. (b) FLOPs versus mAP are plotted(top-left is better)*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2406_12079/figures/011_Figure.jpg]]
*Figure: (a) Comparison with smaller networks on ImageNet with pruning ResNet50. Our approach of (b) Results of ours with soft masking on pruning large models across various ratios achieves a ImageNet with ResNet50. Improvement is superior accuracy-speed trade-off compared to existing observed in Top1 at a high FPS level. Topsmaller networks. Top-right is better. right is better*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2406_12079/figures/003_Table.jpg]]
*Table: Additionally, we declare the following entities(all 1-indexed )*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2406_12079/figures/004_Table.jpg]]

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2406_12079/figures/012_Table_5.jpg]]
*Table 5: Training Detail*


## 方法谱系与知识库定位

### 1. 与基线方法的关系

MDP 的核心贡献在于将剪枝从“迭代局部搜索”推向“单次全局优化”，并在粒度上从单一通道剪枝扩展到通道‑层‑块联合剪枝。其与主要基线的关系可概括为以下三个维度：

**（1）剪枝粒度：从通道到多维联合。**
传统方法如 **HALP**（Shen et al., NeurIPS 2022）和 **SMCP**（Humble et al., ECCV 2022）均局限于通道级剪枝，在高剪枝比（70%–90%）下无法安全地移除整层或整块，导致精度大幅下降。**EagleEye**（Li et al., ECCV 2020）同样基于 FLOPs 进行通道剪枝，强调快速子网络评估，但缺乏层/块删除能力。**LayerPrune‑Imprint** 则走向另一极端——仅做层剪枝，通过中间特征印记评估层重要性，但由于不能同时调整通道宽度，其加速效果有限。MDP 通过块分组策略将层‑块决策统一纳入优化，在单次求解中同时决定通道数、层保留和块保留，填补了上述两种范式之间的空白。

**（2）延迟建模：从单变量到双线性配置矩阵。**
HALP 等方法的延迟模型仅考虑固定输入通道下输出通道变化的延迟，忽略了输入通道的联动变化。这一缺陷在高剪枝比下尤为致命：当相邻层均被大量剪枝时，仅建模输出通道的延迟估计严重偏离真实值，导致精度‑延迟优化目标失真。MDP 构建双线性配置延迟矩阵 $\mathbf{C}_l$，精确捕获所有输入/输出通道组合的延迟，使得优化器能够在真实的延迟约束下搜索最优结构。

**（3）优化范式：从迭代贪婪到单次 MINLP。**
HALP 采用迭代贪婪或背包求解，需多达 30 步才能逼近目标延迟预算，且每一步的延迟估计误差会累积。MDP 将剪枝重新形式化为混合整数非线性规划（MINLP），以总重要性最大化为目标、总双层延迟为约束，利用 Pyomo/MindtPy 的 Outer Approximation 方法在单次求解中获得全局最优结构。消融实验（Table 3）表明，当剪枝步数降至 1 时，HALP 因延迟模型不准确导致性能崩溃，而 MDP 的单步设置即为标准操作模式，无需迭代。

### 2. 适用边界

MDP 的有效性依赖于以下前提条件，超出这些边界时性能可能下降或方法不再适用：

- **网络结构要求残差连接。** 块删除机制依赖残差块的分组：当块决策变量 $z_{\beta(l)} = 0$ 时，整个残差块被移除，跳跃连接保证了信息流的连续性。对于无跳跃连接的纯顺序网络（如 VGG 风格的直筒结构），块删除不可行，只能通过通道剪枝将层压缩至 1 个通道。
- **延迟查找表需为目标硬件预构建。** 双线性延迟矩阵 $\mathbf{C}_l$ 的准确性取决于对目标硬件上所有输入/输出通道组合的延迟测量。当模型或硬件变化时，需重新测量。在 ResNet50 上，该过程开销可控；但在超大规模模型（如 ViT‑Huge）上的扩展性尚未验证。
- **重要性估计依赖 BatchNorm 参数。** 泰勒通道重要性 $\mathcal{T}_l^j = |g_{\gamma_l^j} \gamma_l^j + g_{\beta_l^j} \beta_l^j|$ 直接依赖 BatchNorm 的权重和偏置梯度。对于不使用 BN 的网络（如部分 Transformer 变体），需要适配替代的重要性准则。
- **MINLP 求解规模可控。** 在 ResNet50（约 50 层）上，MINLP 求解仅需约 5 秒。但在层数更多、通道选项更细粒度的模型中，求解时间可能显著增长，需进一步验证可扩展性。

### 3. 局限与已知问题

- **块删除仅适用于残差结构。** 如前所述，无跳跃连接的网络层无法通过块剪枝移除，只能降低到 1 个通道，限制了多维剪枝的收益。
- **延迟建模的测量成本。** 准确的延迟建模需要为目标硬件预构建查找表，当硬件平台或模型结构变化时需重新测量，缺乏即插即用的泛化能力。
- **微调超参数未优化。** 剪枝后的微调超参数（学习率、epoch 数等）按经验设定，可能未达到最优的精度恢复。论文未探索剪枝结构感知的微调策略。
- **仅验证了 CNN 和 CNN‑Transformer 混合模型。** 实验覆盖 ResNet50（纯 CNN）、SSD512‑RN50（检测头含 CNN）和 StreamPETR（CNN 骨干 + Transformer 检测头），但未在纯 Transformer 模型（如 ViT、Swin）上验证。对于仅由 Transformer 组成的模型，如何在无残差连接的注意力块中安全地进行块剪枝仍是开放问题。

### 4. 开放问题与后续方向

- **纯 Transformer 模型的块剪枝。** 当网络完全由 Transformer 组成时，注意力块内部通常不包含传统意义上的残差连接（或残差连接跨越多个子层）。如何定义和分组“块”以实现安全的块删除，需要重新设计分组策略和约束条件。
- **延迟建模的自动化。** 能否通过元学习或神经网络预测器，避免为每个新硬件手动构建延迟查找表？这将是 MDP 走向实际部署的关键一步。
- **与其他压缩技术的协同。** 将 MDP 与模型量化、知识蒸馏等压缩技术结合，是否可以进一步推动精度‑速度前沿？论文仅在 Fig. 6(b) 中初步探索了与软掩码（soft masking）的集成，观察到高 FPS 水平下的 Top‑1 改善，但更系统的多技术协同研究尚待开展。
- **动态自适应剪枝。** 如何设计自适应策略，根据运行时条件（如设备负载、电量）动态调整延迟预算 $\Psi$ 并即时生成最优子网络？当前 MDP 为每个延迟预算生成一个静态剪枝结构，缺乏运行时灵活性。
- **更大规模模型的验证。** MINLP 求解在 ResNet50 上仅需约 5 秒，但在数百层或数千通道选项的模型中，求解时间和内存消耗的增长曲线尚未被刻画。

## 原文 PDF

![[paperPDFs/CVPR_2025/MDP_Multidimensional_Vision_Model_Pruning_with_Latency_Constraint.pdf]]
