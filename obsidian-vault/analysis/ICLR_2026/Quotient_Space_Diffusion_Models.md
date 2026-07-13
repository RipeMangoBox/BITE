---
title: "Quotient-Space Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Quotient_Space_Diffusion_Models.pdf
project_link: null
code_link: null
openreview_forum_id: 3JPAkwSVc4
aliases:
- QSDM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "通过水平投影算子 P_x 将更新向量投影到与群作用正交的子空间上，从根本上消除了对等价自由度预测的需求。"
primary_logic: "通过构建商空间（等价类空间）上的扩散过程，并利用水平提升将其映射回原空间进行实现，可以在保持采样正确性的同时，去除学习等价类内运动的冗余。"
claims:
- "该框架消除了学习群作用分量（如旋转）的必要性，从而降低了相对于传统群等变扩散模型的学习难度。"
- "采样器能够保证恢复目标分布，而启发式对齐策略缺乏正确的采样器。"
- "水平训练目标仅监督水平分量，允许模型在垂直方向输出任意值，从而简化了学习任务。"
- "商空间扩散模型在 GEOM-QM9 和 GEOM-DRUGS 数据集上相对于 ET-Flow 取得了 9%-23% 的相对改进。"
---

# Quotient-Space Diffusion Models

> [!tip] 核心洞察
> 通过构建商空间（等价类空间）上的扩散过程，并利用水平提升将其映射回原空间进行实现，可以在保持采样正确性的同时，去除学习等价类内运动的冗余。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 商空间扩散模型 |
| 英文题名 | Quotient-Space Diffusion Models |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=3JPAkwSVc4) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Quotient-Space Diffusion Model |
| Dataset | Protein structure generation (Foldseek AFDB clusters), GEOM-QM9 |

> [!tip] 效果简介
> - Protein structure generation (Foldseek AFDB clusters) 上，Designability (%) scRMSD<2Å (SDE, γ=0.35) 为 97.6，对比 96.0 (Proteína M_FS^small)，变化 +1.6。
> - Protein structure generation (Foldseek AFDB clusters) 上，FPSD vs. PDB (SDE, γ=0.35) 为 274.7，对比 386.5 (Proteína M_FS^small)，变化 -111.8。
> - Protein structure generation (Foldseek AFDB clusters) 上，fJSD vs. AFDB (SDE, γ=0.35) 为 1.55，对比 1.73 (Proteína M_FS^small)，变化 -0.18。

## 概要

在分子构象与蛋白质结构生成等科学任务中，目标分布通常对旋转、平移等连续群作用具有不变性。传统群等变扩散模型虽然能保证生成分布的对称性，但需要神经网络同时学习等价类内部（如旋转自由度）的运动分量。这一冗余学习不仅增加了优化难度，还可能引入训练与采样之间的兼容性问题——部分启发式对齐策略（如 GeoDiff 对齐、AlphaFold3 对齐）虽试图规避该问题，却缺乏保证恢复目标分布的正确采样器。

本文提出**商空间扩散模型**（Quotient-Space Diffusion Models），核心思路是将扩散过程从原始总空间投影到等价类构成的商空间上，再通过水平提升（horizontal lift）将其映射回原空间实现。具体而言，该方法利用水平投影算子 $P_{\mathbf{x}}$ 将更新向量投影到与群作用正交的子空间，从根源上消除了对等价自由度的预测需求，同时通过曲率修正项保证 SDE 采样的分布正确性。

该方法在概念上统一了现有策略：与标准等变扩散相比，它降低了学习难度；与启发式对齐方法相比，它具备正确的采样器。实验表明，商空间扩散在 GEOM-QM9 和 GEOM-DRUGS 分子数据集上相对 ET-Flow 取得 9%–23% 的提升；在蛋白质结构生成任务中，60M 参数的商空间模型不仅超越 Proteína 基线，还在多数关键分布指标上优于更大的 200M 模型，且水平投影操作仅引入极小的计算开销。

### 对称性生成建模的核心瓶颈

在分子构象生成、蛋白质结构设计等科学任务中，目标分布通常具有固有的**对称性**。例如，分子的整体旋转或平移不会改变其内在结构，因此理想的数据分布应在对应的群作用下保持不变。这类问题可自然地建模为：从商空间（等价类空间）中采样，而无需区分同一等价类内的不同表示。

传统的群等变扩散模型采用一种间接策略：在完整空间上定义扩散过程，同时要求神经网络架构对群作用等变。然而，这一范式存在根本性的冗余——模型被迫学习**等价类内部的运动分量**（如旋转自由度），而这些分量对生成内在系统状态是无关的。正如 Table 1 所总结，常规等变扩散模型在训练时需预测等变自由度内的变化，这不仅增加了学习难度，还可能导致采样时的不兼容。

### 启发式对齐策略的局限

为缓解上述冗余，研究者提出了多种启发式对齐策略：

- **GeoDiff 对齐**（Xu et al., 2022）：将目标样本旋转对齐到当前噪声样本，试图消除旋转自由度内的方差。然而，该方法本质上改变了学习目标（Figure 3 以双原子分子为例展示了这一差异），且缺乏正确的采样器来保证恢复目标分布。
- **AF3 对齐**（Abramson et al., 2024）：进一步将对齐方向反转，将样本向模型输出对齐。该方法虽进一步消除了等价自由度内的方差，但其训练-采样不兼容问题更为突出——由于等价自由度上的输出是任意的，目前尚无已知的正确采样器。

上述方法的共同缺陷在于：它们试图在完整空间中“修补”对称性带来的冗余，而非从根本上重构扩散过程。

### 核心动机与本文思路

本文的核心洞察在于：**通过构建商空间（等价类空间）上的扩散过程，并利用水平提升将其映射回原空间进行实现，可以在保持采样正确性的同时，从根本上消除学习等价类内运动的冗余。**

具体而言，该框架通过**水平投影算子** $P_{\mathbf{x}}$ 将更新向量投影到与群作用正交的子空间上（Figure 2 示意了总空间、商空间及切向量的对应关系）。以二维平面上的 SO(2) 对称分布为例，商空间扩散过程仅沿径向运动，而常规等变扩散模型则包含无效的角向分量（Figure 1）。这一设计使得神经网络无需学习等价类内部的任何运动，从而简化学习任务，同时采样器能够严格保证恢复目标分布。

本文在分子构象生成（GEOM-QM9、GEOM-DRUGS）和蛋白质骨架设计两个任务上验证了该框架的有效性，并建立了商空间扩散建模的严格数学形式。

## 核心方法与创新机理

### 问题瓶颈：等价自由度冗余

在分子构象生成、蛋白质结构生成等科学任务中，目标分布天然具有群对称性——例如，三维结构的整体旋转不改变其内在物理状态。传统群等变扩散模型（如 GeoDiff、ET-Flow、Proteína）虽然通过等变架构保证了输出与输入的对称性兼容，但其训练目标要求模型学习**等价类内（如旋转）的具体运动**。这些运动对生成内在系统状态是不必要的，却显著增加了学习难度，并可能导致采样过程中产生冗余轨迹。

### 核心洞察：商空间上的扩散建模

本文的核心创新在于将扩散过程从原始总空间 $\mathcal{M}$ **投影到商空间 $\mathcal{Q} = \mathcal{M} / \mathcal{G}$**（即等价类空间）上进行建模，再通过**水平提升**（horizontal lift）将其映射回原始空间实现采样。这一框架从根本上消除了对等价自由度预测的需求：

- **水平投影算子 $P_{\mathbf{x}}$**：将更新向量投影到与群作用正交的水平子空间上，去除由群作用产生的垂直（旋转）分量。在 $\mathbb{R}^{3N} / \mathrm{SE}(3)$ 形状空间中，该算子具有显式解析形式：
  $$P_{\mathbf{x}}(\mathbf{v}) = \mathbf{v} - \mathbf{J}^{-1} \left( \sum_{i=1}^{N} \mathbf{x}^{(i)} \times \mathbf{v}^{(i)} \right) \times \mathbf{x}$$

- **曲率修正项 $\tilde{\mathbf{h}}$**：在 SDE 采样中补偿商空间的几何曲率，保证生成分布的正确性，其显式形式为：
  $$\tilde{\mathbf{h}}^{(i)}(\mathbf{x}) = - \big( \operatorname{tr}(\mathbf{J}^{-1}) \mathbf{I} - \mathbf{J}^{-1} \big) \mathbf{x}^{(i)}$$

### Changed Slots：与传统方法的关键差异

#### 1. 训练损失函数：从全分量监督到水平分量监督

| 维度 | 传统等变扩散 | 商空间扩散（本文） |
|------|-------------|-------------------|
| **损失函数** | $\mathbb{E}[\|D_\theta(\mathbf{x}_t, t) - \mathbf{x}_1\|^2]$ | $\mathbb{E}[\|P_{\mathbf{x}_t}(D_\theta(\mathbf{x}_t, t) - \mathbf{x}_1)\|^2]$ |
| **监督范围** | 对所有方向分量均等惩罚 | 仅监督水平分量，允许垂直方向输出任意值 |
| **学习负担** | 需学习等价类内的具体运动 | 完全消除等价自由度内的学习需求 |

水平训练目标（式(10)）的核心机制在于：通过投影算子 $P_{\mathbf{x}_t}$ 将去噪网络输出与干净数据之差投影到水平子空间，使得模型仅需学习在商空间中有意义的更新方向，而无需关心等价类内的旋转变化。这从根本上简化了学习任务。

#### 2. 采样过程动力学：从完整空间到水平提升

| 维度 | 传统等变扩散 | 商空间扩散（本文） |
|------|-------------|-------------------|
| **ODE 采样** | $\mathrm{d}\mathbf{x}_t = \mathbf{v}_\theta(\mathbf{x}_t, t) \mathrm{d}t$ | $\mathrm{d}\mathbf{x}_t = P_{\mathbf{x}_t} \mathbf{v}_\theta(\mathbf{x}_t, t) \mathrm{d}t$ |
| **SDE 采样** | 包含完整漂移项和 Wiener 过程 | 水平投影漂移 + 曲率修正 + 水平投影 Wiener 过程 |
| **采样保证** | 依赖等变架构保证兼容性 | **理论上保证恢复目标分布**（Theorem 4） |

商空间扩散的 SDE 采样器（式(9)）具有严格的理论基础：
$$\mathrm{d}\tilde{\mathbf{x}}_t = \left( P_{\tilde{\mathbf{x}}_t} (\mathbf{b}_t(\tilde{\mathbf{x}}_t)) - \frac{\sigma_t^2}{2} \tilde{\mathbf{h}}(\tilde{\mathbf{x}}_t) \right) \mathrm{d}t + \sigma_t P_{\tilde{\mathbf{x}}_t} \mathrm{d}\mathbf{w}_t$$

值得注意的是，水平提升过程**并非简单地在原始 SDE 各项上添加水平投影**——商空间的几何曲率引入了额外的修正项 $\frac{\sigma_t^2}{2} \tilde{\mathbf{h}}$，这是保证边缘分布正确性的关键。

### 与启发式对齐策略的本质区别

现有工作中存在两种启发式对齐策略：

- **GeoDiff 对齐**（Xu et al., 2022）：通过将目标样本对齐到当前噪声样本 $\mathcal{A}_{\mathbf{y}}(\mathbf{x}) := \mathrm{argmin}_{\mathbf{x}' \in \{g \cdot \mathbf{x}\}} d(\mathbf{x}', \mathbf{y})$ 来减少等价类变化，但**缺乏正确的采样器**，训练-采样不兼容。
- **AF3 对齐**（Abramson et al., 2024）：将目标对齐到模型输出，进一步消除等价自由度内的方差，但同样**缺乏正确的采样器**。

相比之下，商空间扩散通过严格的微分几何框架，**同时解决了训练简化与采样正确性**两个问题。采样器能够保证恢复目标分布，而启发式对齐策略无法提供这一保证。

### 计算开销

水平投影操作的计算开销极小。实验表明，训练速度从原始扩散的 4.19 iters/s 仅略微下降至商空间扩散的 4.10 iters/s，几乎可以忽略不计。

商空间扩散模型（Quotient-Space Diffusion Model）的核心思想是将原始扩散过程投影到等价类空间（商空间）上，再通过水平提升（horizontal lift）将其映射回原始空间进行实现，从而在保持采样正确性的同时，消除对群作用分量（如旋转）的学习需求。整体框架由四个关键模块构成，其输入输出流如下：

**输入**：先验分布 $p_{\text{prior}}$（通常为标准高斯分布），以及目标分布 $p(\mathbf{x}_1)$（具有群 $\mathcal{G}$ 对称性的不变分布，如分子或蛋白质的三维结构分布）。

**输出**：从目标分布中采样的结构 $\mathbf{x}_1$。

### 模块关系与数据流

1. **去噪模型 $D_\theta$**：接收含噪样本 $\mathbf{x}_t$ 和时间步 $t$，预测干净结构 $\mathbf{x}_1$。该模块是标准的扩散模型去噪器，其架构保持等变性（如 ET-Flow 或 Proteína 的骨干网络），但训练目标和采样过程中的梯度流向被商空间框架所改变。

2. **水平投影算子 $P_{\mathbf{x}}$**：这是框架的核心操作。对于任意更新向量 $\mathbf{v}$（如去噪模型输出与目标之差），$P_{\mathbf{x}}(\mathbf{v})$ 将其投影到与群作用正交的水平子空间上，去除由群作用产生的垂直（旋转）分量。在 $\mathbb{R}^{3N}/\mathrm{SE}(3)$ 的具体实现中，投影算子具有显式形式：
   $$P_{\mathbf{x}}(\mathbf{v}) = \mathbf{v} - \mathbf{J}^{-1} \left( \sum_{i=1}^{N} \mathbf{x}^{(i)} \times \mathbf{v}^{(i)} \right) \times \mathbf{x}$$
   其中 $\mathbf{J}$ 为惯性张量。该算子同时作用于训练损失和采样过程。

3. **曲率修正项 $\tilde{\mathbf{h}}$**：在 SDE 采样中，商空间的几何曲率会引入额外的漂移项。该修正项保证生成分布的正确性，其显式形式为：
   $$\tilde{\mathbf{h}}^{(i)}(\mathbf{x}) = - \big( \operatorname{tr}(\mathbf{J}^{-1}) \mathbf{I} - \mathbf{J}^{-1} \big) \mathbf{x}^{(i)}$$
   ODE 采样中不需要此项。

4. **ODE/SDE 采样器**：模拟商空间扩散过程的水平提升。ODE 采样器遵循 $\mathrm{d}\mathbf{x}_t = P_{\mathbf{x}_t} \mathbf{v}_\theta(\mathbf{x}_t, t) \mathrm{d}t$；SDE 采样器则包含水平投影、曲率修正项和水平投影的 Wiener 过程：
   $$\mathrm{d}\mathbf{x}_t = \left( P_{\mathbf{x}_t} (\mathbf{v}_\theta + g_t \mathbf{s}_\theta) + \gamma \eta_t \tilde{\mathbf{h}}(\mathbf{x}_t) \right) \mathrm{d}t + \sqrt{2\gamma\eta_t} P_{\mathbf{x}_t} \mathrm{d}\mathbf{w}_t$$

### 训练与推理流程

**训练阶段**：使用水平投影损失函数：
$$\mathcal{L}(\theta) := \mathbb{E}_{p(t)} w(t) \mathbb{E}_{p(\mathbf{x}_1, \mathbf{x}_t)} \| P_{\mathbf{x}_t} (\mathbf{D}_\theta(\mathbf{x}_t, t) - \mathbf{x}_1) \|^2$$
该损失仅监督去噪模型输出的水平分量，允许模型在垂直方向（等价类内运动方向）输出任意值，从根本上降低了学习难度。训练过程中无需对数据或预测进行任何启发式对齐操作。

**推理阶段**：从先验分布采样初始噪声 $\mathbf{x}_0$，通过 ODE 或 SDE 采样器迭代更新，每一步更新均经过水平投影算子过滤，确保轨迹仅沿商空间方向演化，最终收敛到目标分布。

### 与传统框架的关键区别

传统群等变扩散模型使用不变目标分布和等变架构，但训练损失对所有方向分量均等惩罚，迫使模型学习等价类内的具体运动（如旋转），这增加了学习负担且可能导致采样不兼容。启发式对齐策略（如 GeoDiff 对齐、AF3 对齐）试图通过将目标对齐到当前噪声样本来减少方差，但缺乏正确的采样器。相比之下，商空间扩散模型通过水平投影从根本上消除了对等价自由度的预测需求，且采样器保证恢复目标分布。

### 核心模块

商空间扩散模型的实现围绕四个关键模块展开，每个模块在消除等价类内冗余自由度这一核心机制中承担明确角色：

**去噪网络 $D_\theta$**：与标准扩散模型一致，该模块从含噪样本 $\mathbf{x}_t$ 预测干净结构 $\mathbf{x}_1$。其训练目标由式 (4) 给出，但在商空间框架下，损失函数被替换为仅监督水平分量的版本（见下文训练损失公式）。

**水平投影算子 $P_{\mathbf{x}}$**：这是整个框架的核心操作，负责将更新向量投影到与群作用正交的水平子空间上，从而去除由群作用产生的垂直（如旋转）分量。在 $R^{3N}/SE(3)$ 的具体实现中，该算子的显式形式为：

$$P_{\mathbf{x}}(\mathbf{v}) = \mathbf{v} - \mathbf{J}^{-1} \left( \sum_{i=1}^{N} \mathbf{x}^{(i)} \times \mathbf{v}^{(i)} \right) \times \mathbf{x}$$

其中 $\mathbf{J}$ 为与构型 $\mathbf{x}$ 相关的惯性张量，$\mathbf{x}^{(i)}$ 和 $\mathbf{v}^{(i)}$ 分别为第 $i$ 个原子的位置和速度分量。该公式将速度向量 $\mathbf{v}$ 中对应于整体旋转的分量剥离，仅保留改变分子形状的水平分量。

**曲率修正项 $\tilde{\mathbf{h}}$**：当使用 SDE 采样时，仅对漂移项和扩散项施加水平投影并不足以保证生成正确的边缘分布。商空间的几何曲率会引入额外的漂移效应，必须通过以下修正项进行补偿：

$$\tilde{\mathbf{h}}^{(i)}(\mathbf{x}) = - \big( \operatorname{tr}(\mathbf{J}^{-1}) \mathbf{I} - \mathbf{J}^{-1} \big) \mathbf{x}^{(i)}$$

该修正项源于投影过程中商空间曲率对扩散过程的影响（Theorem 1），是商空间扩散区别于简单“投影后采样”的关键理论贡献。

**ODE/SDE 采样器**：采样器模拟商空间扩散过程的水平提升版本。ODE 采样器直接对水平投影后的速度场积分：

$$\mathrm{d}\mathbf{x}_t = P_{\mathbf{x}_t} \mathbf{v}_\theta(\mathbf{x}_t, t) \mathrm{d}t$$

SDE 采样器则需同时引入曲率修正项和水平投影的 Wiener 过程：

$$\mathrm{d}\tilde{\mathbf{x}}_t = \left( P_{\tilde{\mathbf{x}}_t} (\mathbf{b}_t(\tilde{\mathbf{x}}_t)) - \frac{\sigma_t^2}{2} \tilde{\mathbf{h}}(\tilde{\mathbf{x}}_t) \right) \mathrm{d}t + \sigma_t P_{\tilde{\mathbf{x}}_t} \mathrm{d}\mathbf{w}_t$$

其中 $\mathbf{b}_t$ 为原始扩散过程的漂移项，$\sigma_t$ 为扩散系数。

### 关键公式：水平投影训练损失

商空间框架对训练目标的改造是其降低学习难度的直接机制。标准去噪损失对所有方向分量施加均等惩罚，迫使模型学习等价类内的运动（如旋转），而这些运动对生成内在系统状态是不必要的。商空间扩散通过水平投影算子仅监督输出的水平分量：

$$\mathcal{L}(\theta) := \mathbb{E}_{p(t)} w(t) \mathbb{E}_{p(\mathbf{x}_1, \mathbf{x}_t)} \| P_{\mathbf{x}_t} (\mathbf{D}_\theta(\mathbf{x}_t, t) - \mathbf{x}_1) \|^2$$

其中 $w(t)$ 为时间加权函数，$p(\mathbf{x}_1, \mathbf{x}_t)$ 为干净数据与含噪数据的联合分布。该损失函数的因果机制在于：模型在垂直方向（群作用方向）的输出可以是任意值而不受惩罚，从而将学习容量集中在对生成任务真正重要的形状变化上。这一设计从根本上消除了学习等价类内运动的冗余，是商空间扩散相对于传统群等变扩散模型的核心优势。

### 基础框架：随机插值

商空间扩散建立在随机插值框架之上。先验分布与目标分布之间的含噪样本通过线性插值生成：

$$\mathbf{x}_t = \alpha_t \mathbf{x}_0 + \beta_t \mathbf{x}_1 + \gamma_t \epsilon$$

其中 $\alpha_t, \beta_t, \gamma_t$ 为时间相关的插值系数，$\epsilon$ 为标准高斯噪声。该插值定义了一个从先验分布到目标分布的连续路径，扩散模型通过学习该路径上的速度场或去噪函数来实现生成。

## 实验与关键发现

### 核心实验设计

商空间扩散模型的评估在两个不同尺度的分子结构生成任务上进行：小分子构象生成（GEOM-QM9 和 GEOM-DRUGS）与蛋白质骨架生成（Foldseek AFDB 聚类）。所有对比实验均采用**相同架构、相同训练配置和相同采样步数**（50 NFE），以确保公平比较。蛋白质生成实验进一步采用自条件（self-conditioning）且未使用自引导（autoguidance），以评估基础生成能力。

### 小分子构象生成

在 GEOM-QM9 和 GEOM-DRUGS 数据集上，商空间扩散方案被应用于 ET-Flow 架构（SO(3) 和 O(3) 变体）。如 Table 2 所示，商空间扩散在所有评估指标上均显著优于 ET-Flow 基线，取得 **9%–23% 的相对改进**（Abstract，Section 4.1）。具体而言：

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_3JPAkwSVc4/figures/005_Table_2.jpg]]
*Table 2: The effect of the quotient-space diffusion scheme for molecular structure generation on the GEOM-QM9 and the GEOM-DRUGS datasets using the ET-Flow(SO(3)) and ET-Flow(O(3)) architectures. We use the same sampling steps of 50 NFEs for fair comparison. Best results are marked in bold. Best results for the same architecture are underlined*

- **GEOM-QM9 + ET-Flow(O(3))**：Recall Coverage（mean）从基线提升至 **96.40**。
- **GEOM-DRUGS + ET-Flow(SO(3))**：Precision Coverage（mean）提升至 **72.70**。

该结果表明，去除对等价类内自由度（如旋转）的预测需求，直接转化为生成质量的系统性提升。值得注意的是，改进幅度在不同对称群设定（SO(3) vs. O(3)）下均保持一致，验证了框架对群类型的鲁棒性。

### 蛋白质骨架生成

在蛋白质结构生成任务中，商空间扩散被集成到 Proteína 模型中。Table 3 和 Table 5（Appendix）报告了完整性能对比：

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_3JPAkwSVc4/figures/006_Table_3.jpg]]
*Table 3: The effect of the quotient-space diffusion scheme for protein structure generation using the Prote´ına model. Best results are marked in bold*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_3JPAkwSVc4/figures/011_Table_5.jpg]]
*Table 5: Complete performance comparison of the released Prote´ına checkpoints against our version in the quotient space. Best results are marked in bold*

| 指标 | Proteína M_FS^small (60M) | 商空间扩散 (60M, SDE, γ=0.35) | 改进 |
|------|--------------------------|-------------------------------|------|
| Designability (%) scRMSD<2Å | 96.0 | **97.6** | +1.6 |
| FPSD vs. PDB ↓ | 386.5 | **274.7** | -111.8 |
| fJSD vs. AFDB ↓ | 1.73 | **1.55** | -0.18 |

**关键发现**：60M 参数的商空间模型不仅超越了同等规模的 Proteína 基线，还在大多数关键分布指标上**优于更大的 200M M_FS 模型**（confidence=0.95）。这表明商空间扩散通过降低学习难度，使得较小模型也能实现更优的分布拟合能力。

### 消融实验

#### 计算开销
水平投影操作引入的额外计算成本极小。训练速度对比显示：原始扩散为 **4.19 iters/s**，商空间扩散为 **4.10 iters/s**（Section F.1），开销几乎可忽略。训练损失曲线（Figure 4）进一步证明训练过程在实践中是稳定的（confidence=0.9）。

#### 收敛速度
Figure 5 从两个维度比较了收敛行为：

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_3JPAkwSVc4/figures/009_Figure_5.jpg]]
*Figure 5: Training and sampling convergence speed comparison on GEOM-DRUGS. (Left) The relationship between training epochs and generation performance measured by the precision AMR median metric. (Right) The relationship between the number of function evaluations (NFE) for sampling and generation performance measured by the precision AMR median metric*

1. **训练收敛**（Left）：商空间扩散比 GeoDiff 对齐策略收敛更快，与 AF3 对齐策略收敛速度相当。
2. **采样收敛**（Right）：在所有函数评估次数（NFE）设置下，商空间扩散始终优于所有基线方法，表明其在采样效率上的系统性优势。

这些结果表明，商空间扩散不仅降低了学习难度，还加速了训练和采样两个阶段的收敛。

### 失败模式与局限性

#### ODE 采样的设计性下降
尽管 ODE 采样能极大改善分布相似度指标（如 fJSD），但会导致**设计性（Designability）急剧下降**（Table 5，Appendix）。这一现象的具体原因尚不明确，文中将其列为开放问题：为什么 ODE 采样会大幅降低蛋白设计性，同时却显著提高分布相似度指标？

#### 对称群依赖
框架需要手动指定系统的对称群以构造商空间，不能自动发现对称性。目前仅在 SE(3) 群（分子结构生成）上验证，文中指出框架可推广至 U(1)、SU(2) 等对称群，但其应用仍留作未来工作（Section F.4）。

#### 任务范围限制
当前验证局限于小分子和蛋白质结构生成任务，其他科学领域（如材料科学、多体物理系统）的适用性尚未探索。

### 开放问题

除上述 ODE 设计性下降问题外，文中还提出以下开放方向：

- 如何为 AF3 对齐方法设计正确的采样器，以解决其训练-采样不兼容问题？
- 商空间扩散框架能否有效扩展到更大规模的对称群和更复杂的流形？
- 对于像平移群这类非紧群，如何处理商空间上的分布并保证数值稳定？


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_3JPAkwSVc4/figures/001_Table_1.jpg]]
*Table 1: Comparison among different training strategies in presence of a symmetry group. Learning difficulty is measured by whether the need to predict in the equivalent degrees of freedom (DoFs), induced by the group actions, is removed, and (if not) whether the variance on the equivalent DoFs is removed. Sampling compatibility means whether there is a sampler that exactly reproduces the target distribution. The denoising form of diffusion model $\scriptstyle \mathbf { D } _ { \theta }$ is used to express the loss functions, where $\mathcal { A } _ { \bf y } ( { \bf$ x } ) (Eq. (11)) represents aligning x towards y, and ¯θ denotes treating θ as constant (i.e., stop-gradient). The conclusions hold using...

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_3JPAkwSVc4/figures/010_Table_4.jpg]]
*Table 4: Hyperparameters for Prote´ına model*

## 定位与知识库关联

### 1. 问题定位：群等变扩散中的等价自由度冗余

在分子构象生成、蛋白质结构生成等科学任务中，目标分布通常对旋转、平移等对称群作用具有不变性——即旋转后的分子构象在物理上等价。主流方法采用**群等变扩散模型**，通过设计等变架构（如 GeoDiff、ET-Flow、Proteína）来匹配这一不变性，使模型输出随输入同步旋转。

然而，这类方法存在一个根本性瓶颈：**模型仍需学习等价类内部的运动分量**（例如，在三维空间中，一个分子构象的所有旋转版本构成一个等价类，模型需要预测旋转方向上的更新）。这些等价自由度内的运动对生成任务而言是冗余的——它们不改变系统的内在状态，却增加了学习负担，并可能导致采样轨迹过长或不稳定。

本文提出的**商空间扩散模型（Quotient-Space Diffusion Model）**正是针对这一问题，通过将扩散过程投影到等价类空间（商空间）上，从根本上消除了对等价自由度预测的需求。

### 2. 与核心基线方法的关系

#### 2.1 传统群等变扩散模型

传统等变扩散模型（如 GeoDiff、ET-Flow、Proteína）采用不变目标分布 $p(\mathbf{x}_1)$ 和等变架构，训练损失为经典的均方误差 $\mathbb{E}\|\mathbf{D}_\theta(\mathbf{x}_t, t) - \mathbf{x}_1\|^2$，对去噪网络输出的**所有方向分量均等惩罚**。这意味着模型被迫学习等价类内的旋转运动，尽管这些运动对最终生成质量无贡献。

商空间扩散模型的关键改进在于：将训练损失替换为**水平投影损失** $\mathbb{E}\|P_{\mathbf{x}_t}(\mathbf{D}_\theta(\mathbf{x}_t, t) - \mathbf{x}_1)\|^2$（式(10)），仅监督水平分量——即不引起等价类内运动的更新方向。这一改进允许模型在垂直方向（群作用方向）输出任意值，从而显著降低学习难度。

#### 2.2 GeoDiff 对齐策略

GeoDiff（Xu et al., 2022）提出了一种启发式对齐策略：在训练时将目标样本 $\mathbf{x}_1$ 通过对齐算子 $\mathcal{A}_{\mathbf{x}_t}(\mathbf{x}_1) = \arg\min_{\mathbf{x}' \in \{g \cdot \mathbf{x}_1\}} d(\mathbf{x}', \mathbf{x}_t)$ 旋转到与当前噪声样本 $\mathbf{x}_t$ 最近的方向，从而减少等价类内的方差。然而，该方法存在一个关键缺陷：**缺乏正确的采样器**——训练时使用了对齐操作，但采样时无法保证恢复目标分布。

商空间扩散模型通过严格的数学框架解决了这一问题：采样器通过水平提升 ODE/SDE（式(9)、Algorithm 3）模拟商空间上的扩散过程，能够**保证恢复目标分布**。实验表明，商空间扩散比 GeoDiff 对齐收敛更快（Figure 5 左），且在所有函数评估次数（NFE）设置下始终优于所有基线（Figure 5 右）。

#### 2.3 AlphaFold3 对齐策略

AlphaFold3（Abramson et al., 2024）采用了一种更激进的对齐策略：将目标结构直接对齐到模型输出，进一步消除等价自由度内的方差。该方法在蛋白质结构预测中取得了显著效果，但其训练-采样不兼容问题同样未解决。如何为 AF3 对齐方法设计正确的采样器，仍是本文提出的一个开放问题。

### 3. 方法谱系中的位置

从方法论角度看，商空间扩散模型处于**几何深度学习**与**扩散生成模型**的交汇点，其核心贡献在于：

- **几何层面**：通过水平投影算子 $P_{\mathbf{x}}$ 将更新向量投影到与群作用正交的子空间，并引入曲率修正项 $\tilde{\mathbf{h}}$ 补偿商空间的几何弯曲（Theorem 4），构建了商空间上扩散过程的严格水平提升。
- **扩散层面**：将训练与采样统一在商空间框架下，避免了启发式对齐策略的训练-采样不一致问题。

这一框架可推广至 U(1)、SU(2) 等更广泛的对称群，但其应用仍留作未来工作（Section F.4）。

### 4. 适用边界与局限

**已验证的适用范围**：
- 小分子构象生成（GEOM-QM9、GEOM-DRUGS 数据集）
- 蛋白质骨架结构生成（Foldseek AFDB 聚类）

**已知局限**：
1. **对称群需手动指定**：框架要求预先知道系统的对称群以构造商空间，不能自动发现对称性。
2. **非紧群处理未探索**：对于平移群等非紧群，如何处理商空间上的分布并保证数值稳定性仍是开放问题。
3. **ODE 采样的设计性退化**：在蛋白质生成任务中，ODE 采样虽能极大改善分布相似度指标（如 fJSD），但会导致设计性（scRMSD<2Å）急剧下降（Appendix Table 5），其原因尚不明确。
4. **计算开销极小但非零**：水平投影操作仅引入极小的计算开销（训练速度从 4.19 iters/s 降至 4.10 iters/s），在实际应用中可忽略不计。

### 5. 开放问题

1. **AF3 对齐的采样器设计**：如何为 AF3 对齐方法构建正确的采样器，使其训练-采样兼容？
2. **ODE 采样的设计性退化机制**：为什么 ODE 采样在蛋白质生成中会大幅降低设计性，同时却显著提高分布相似度？这一现象是否与商空间的几何结构有关？
3. **更大规模对称群的扩展**：商空间扩散框架能否有效扩展到更大规模的对称群和更复杂的流形（如 SU(2) 对应的量子系统）？
4. **非紧群的处理**：对于平移群等非紧群，如何定义商空间上的概率分布并保证数值稳定性？

## 原文 PDF

![[paperPDFs/ICLR_2026/Quotient_Space_Diffusion_Models.pdf]]
