---
title: "Revisiting Weight Regularization for Low-Rank Continual Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Revisiting_Weight_Regularization_for_Low_Rank_Continual_Learning.pdf
openreview_forum_id: pZj2DhfaVD
aliases:
- EL
- RWRLRCL
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "通过弹性权重巩固（EWC）对共享的低秩更新进行正则化，而非为每个任务添加结构隔离的模块。"
primary_logic: "在全维参数空间中估计Fisher信息矩阵，以准确捕捉低秩更新中参数的重要性，并将该正则化施加于低秩分解矩阵的乘积之上，从而在保持固定内存占用的同时实现更好的稳定性-可塑性权衡。"
claims:
- "EWC-LoRA 使用共享 LoRA 模块并通过 EWC 正则化其更新，内存占用不随任务数增加。"
- "在全维空间估计 Fisher 矩阵比单独对 A、B 正则化或使用固定的预计算 Fisher 更有效。"
- "EWC-LoRA 在多个视觉基准上相比 Vanilla LoRA 平均提升 8.92%，并取得与或超越现有最佳低秩 CL 方法的性能。"
- "CIFAR-100 (10 tasks) 上 Final Average Accuracy (Ā₁₀) = 87.91"
---

# Revisiting Weight Regularization for Low-Rank Continual Learning

> [!tip] 核心洞察
> 在全维参数空间中估计Fisher信息矩阵，以准确捕捉低秩更新中参数的重要性，并将该正则化施加于低秩分解矩阵的乘积之上，从而在保持固定内存占用的同时实现更好的稳定性-可塑性权衡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 重新审视低秩持续学习中的权重正则化 |
| 英文题名 | Revisiting Weight Regularization for Low-Rank Continual Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=pZj2DhfaVD); [GitHub](https://github.com/yaoyz96/low-rank-cl) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | EWC-LoRA |
| Dataset | CIFAR-100 (10 tasks), DomainNet (5 tasks), ImageNet-R (10 tasks), ImageNet-A (10 tasks) |

> [!tip] 效果简介
> - CIFAR-100 (10 tasks) 上，Final Average Accuracy (Ā₁₀) 为 87.91，对比 82.99 (Vanilla LoRA)，变化 +4.92%。
> - DomainNet (5 tasks) 上，Average Accuracy (Avg.) 为 79.58，对比 77.44 (Vanilla LoRA)，变化 +2.14%。
> - ImageNet-R (10 tasks) 上，Average Accuracy (Avg.) 为 78.95，对比 75.57 (Vanilla LoRA)，变化 +3.38%。

## 概述

持续学习中的一个核心瓶颈是**稳定性–可塑性困境**：模型在学习新任务时，如何在不遗忘旧知识的前提下保持对新知识的适应能力。在参数高效微调（PEFT）范式下，现有方法主要通过为每个任务分配独立的低秩适配模块（如 InfLoRA、SD-LoRA、CL-LoRA 等）来缓解任务间干扰，但这导致存储开销随任务数量线性增长，且权重正则化策略在低秩持续学习中未被充分利用。

**EWC-LoRA** 针对这一瓶颈提出了一条不同的路径：使用一个**所有任务共享的 LoRA 模块**，并通过弹性权重巩固（EWC）对其更新进行正则化，从而在保持固定内存占用的同时实现任务间干扰的有效抑制。其核心洞察在于，**在全维参数空间中估计 Fisher 信息矩阵**，以准确捕捉低秩更新中参数的重要性，并将该正则化施加于低秩分解矩阵的乘积之上，而非对分解矩阵 A、B 分别正则化或使用固定的预计算 Fisher。

实验表明，EWC-LoRA 在多个视觉基准上相比朴素 LoRA 平均提升 **8.92%**，并取得与现有最佳低秩持续学习方法相当甚至更优的性能。具体而言：

- 在 CIFAR-100（10 任务）上，最终平均准确率从 82.99% 提升至 **87.91%**；
- 在 DomainNet（5 任务）上，平均准确率从 77.44% 提升至 **79.58%**；
- 在 ImageNet-A（10 任务）上，最终平均准确率从 40.01% 大幅提升至 **59.89%**；
- 在语言持续学习基准（T5-large）上，平均准确率达到 **76.39%**，超越 O-LoRA 的 72.42%。

消融实验进一步证实，对全维更新 ΔW = AB 估计 Fisher 的策略（F_ΔW）在平均准确率和稳定性上均显著优于分别对 A、B 正则化或使用固定预计算 Fisher 的方案。同时，EWC-LoRA 在稳定性–可塑性权衡上表现出更好的平衡性：其稳定性与 InfLoRA 相当，但保留了更高的可塑性。

方法的局限性在于，在域迁移显著的基准（如 DomainNet）上增益较为温和，且 Fisher 估计仅在每个任务结束时计算一次，存在陈旧性风险，需通过衰减因子 γ 经验性地缓解。

## 背景与动机

持续学习旨在让模型在顺序学习一系列任务时，既能掌握新知识，又不会灾难性地遗忘旧知识。近年来，参数高效微调（PEFT）与持续学习的结合催生了参数高效持续学习（PECL）这一方向，其核心思想是通过冻结预训练骨干网络，仅训练少量可学习参数来适应新任务，从而在保持预训练知识的同时降低计算开销。

现有 PECL 方法主要采用**结构隔离**策略来缓解任务间干扰：为每个新任务分配独立的低秩适配模块（如 LoRA 分支）或提示向量。InfLoRA、SD-LoRA 等方法通过子空间隔离约束不同任务的参数更新方向；CL-LoRA、BiLoRA 等方式则直接为每个任务添加新的 LoRA 分支。这类策略虽然有效，但存在一个根本性瓶颈：**存储开销随任务数量线性增长**。每遇到一个新任务，模型就需要额外存储一组低秩矩阵，在任务数量较多时内存压力显著。

与此同时，**权重正则化**——以弹性权重巩固（EWC）为代表的另一条技术路线——在低秩持续学习中远未被充分利用。EWC 通过 Fisher 信息矩阵衡量参数对旧任务的重要性，并对重要参数的偏移施加二次惩罚，从而在不增加额外模块的前提下缓解遗忘。然而，将 EWC 直接应用于低秩适配并非易事：低秩更新矩阵 $A$ 和 $B$ 的参数空间与全维权重 $W$ 之间存在非线性映射关系，简单地分别对 $A$、$B$ 正则化或使用固定的预计算 Fisher 矩阵，均会导致次优的稳定性-可塑性权衡。

因此，本文的核心动机是回答一个关键问题：**能否在保持固定内存占用的前提下，通过权重正则化实现与结构隔离方法相当甚至更优的持续学习性能？** 这需要在低秩空间中进行正则化时，准确地捕捉参数在全维空间中的重要性——一个在现有工作中尚未被系统解决的理论与工程挑战。

## 核心创新

### 瓶颈：结构隔离 vs. 正则化

现有的参数高效持续学习（PECL）方法，如 InfLoRA、SD-LoRA、CL-LoRA、BiLoRA 等，主要通过**为每个任务分配独立的低秩适配分支**来缓解任务间干扰。这一策略虽然有效，却导致存储开销随任务数量线性增长，且权重正则化策略在低秩持续学习中未被充分利用。EWC-LoRA 的核心创新在于**将缓解任务间干扰的机制从“结构隔离”切换为“正则化”**——即通过弹性权重巩固（EWC）对共享的低秩更新进行正则化，而非为每个任务添加独立的模块。这一改变使得方法的内存占用和推理成本不再随任务数量增加，保持了固定内存占用。

### 关键机制：全维 Fisher 正则化

将 EWC 与低秩适应直接结合并非易事。EWC-LoRA 的关键设计在于**在全维参数空间中估计 Fisher 信息矩阵，以准确捕捉低秩更新中参数的重要性，并将该正则化施加于低秩分解矩阵的乘积之上**。

具体而言，标准 EWC 通过对新旧参数差异施加二次惩罚来保护重要参数：

$$\mathscr{L}_t'(\mathbf{W}) = \mathscr{L}_t(\mathbf{W}) + \frac{\lambda}{2} (\mathbf{W} - \mathbf{W}_{t-1}^*)^\top \mathrm{diag}(\mathbf{F}_{t-1}^{\mathrm{cum}}) (\mathbf{W} - \mathbf{W}_{t-1}^*)$$

在低秩适应中，更新量 $\Delta\mathbf{W} = \mathbf{A}\mathbf{B}$ 由两个低秩矩阵的乘积构成。EWC-LoRA 将上述正则化项重新表述为对全维更新 $\mathrm{vec}(\mathbf{A}\mathbf{B})$ 的惩罚：

$$\mathscr{L}_t'(\mathbf{A},\mathbf{B}) = \mathscr{L}_t(\mathbf{A},\mathbf{B}) + \frac{\lambda}{2} \mathrm{vec}(\mathbf{A}\mathbf{B})^\top \mathbf{F}_{t-1}^{\mathrm{cum}} \mathrm{vec}(\mathbf{A}\mathbf{B})$$

这一设计选择并非随意为之。消融实验（Table 1）表明，**对 $\mathbf{A}$ 和 $\mathbf{B}$ 分别估计 Fisher 并独立正则化，或使用基于冻结预训练模型预计算的 Fisher 矩阵，均导致次优性能**。在全维空间中对 $\Delta\mathbf{W}$ 进行 Fisher 估计可获得最高的平均准确率（92.27）和稳定性（94.45），且额外内存开销仅为 6GB。理论分析进一步揭示，全空间正则化能够更好地保持低秩更新所诱导的真实几何结构和参数重要性，对 $\mathbf{A}$ 和 $\mathbf{B}$ 提供更忠实有效的约束。

### 累积与更新机制

EWC-LoRA 在每个任务结束后计算当前任务最优参数 $\mathbf{W}_t^*$ 上的对角 Fisher 信息矩阵：

$$F_t^{i,i} = \mathbb{E}_{x \sim \mathcal{D}_t} \left[ \mathbb{E}_{y \sim p_{\mathbf{W}_t^*}} \left[ \left( \frac{\partial \log p_{\mathbf{W}}(y|x)}{\partial w_i} \Big|_{\mathbf{W}=\mathbf{W}_t^*} \right)^2 \right] \right]$$

随后通过衰减因子 $\gamma$ 将其累加到历史累积矩阵中：$\mathbf{F}_t^{\mathrm{cum}} \gets \gamma_t \cdot \mathbf{F}_{t-1}^{\mathrm{cum}} + \mathbf{F}_t$。实验表明，$\gamma$ 在 0.3–0.9 范围内对稳定性-可塑性权衡的影响不敏感，方法对超参数具有良好的鲁棒性。

### 创新效果总结

EWC-LoRA 在四个视觉基准上相比 Vanilla LoRA 平均提升 8.92%，并取得与或超越现有最佳低秩 CL 方法的性能。在 CIFAR-100（10 任务）上最终准确率达 87.91，ImageNet-A 上的提升尤为显著（+19.88%）。在语言持续学习基准上，EWC-LoRA 同样超越 O-LoRA（T5-large: 76.39 vs. 72.42）。方法在取得这些性能的同时，训练时间与 Vanilla LoRA 几乎相同，且内存占用不随任务数增长。

## 整体框架

![[assets/figures/papers/iclr26_0012_pZj2DhfaVD_Revisiting_Weight_Regularization_for_Low-Rank_Co/figures/001_Figure_1.jpg]]
*Figure 1: Overview of learning task $\mathcal { T } _ { t }$ at a specific layer of the ViT model. (a) Prior low-rank CL methods structurally isolate task-specific LoRA parameters by adding a new LoRA branch for each task. (b) The proposed EWC-LoRA employs a shared LoRA module that is learned across all tasks and regularized according to parameter importance measured by a Fisher Information Matrix, which is updated after learning each task*

EWC-LoRA 的核心设计思路是：**用一个所有任务共享的低秩适配模块替代逐任务的结构隔离，再通过全维 Fisher 正则化来抑制任务间干扰**。图 1(b) 给出了该框架在一层 ViT 中的工作流——与先前方法为每个任务添加独立 LoRA 分支（图 1(a)）不同，EWC-LoRA 只维护一组共享的低秩矩阵 A 和 B，并在每个任务结束后更新累积 Fisher 信息矩阵，用于约束后续任务的更新方向。

整个 pipeline 由三个紧密耦合的模块构成：

### 1. 共享低秩分支（Shared LoRA Branch）

所有任务共享同一对低秩分解矩阵 A、B，前向计算时模型权重为 $W = W_0 + AB$。每个任务开始时，A、B 从零或均匀分布初始化；任务训练完成后，学到的增量被直接合并到基础权重中：

$$W_t = W_{t-1} + A_t B_t$$

这意味着**无论任务数量如何增长，模型的可学习参数量和推理时延始终保持恒定**——这是与 InfLoRA、SD-LoRA、CL-LoRA 等逐任务添加分支的方法最根本的结构差异。

### 2. 全维 Fisher 估计（Full-dimensional Fisher Estimation）

在每个任务 t 训练收敛到最优参数 $W_t^*$ 后，EWC-LoRA 并不在低秩参数 A、B 上直接估计 Fisher，而是**对全维更新 $\Delta W = AB$ 计算对角 Fisher 信息矩阵**：

$$F_t^{i,i} = \mathbb{E}_{x \sim \mathcal{D}_t}\left[ \mathbb{E}_{y \sim p_{W_t^*}}\left[ \left( \frac{\partial \log p_W(y|x)}{\partial w_i} \Big|_{W=W_t^*} \right)^2 \right] \right]$$

这一设计有明确的理论动机：附录 A.1.1 的分析表明，对 A 和 B 分别施加正则化会扭曲低秩更新所诱导的真实几何结构，而全维正则化能更忠实地约束参数重要性。Table 1 的消融实验也证实了这一点——$F_{\Delta W}$（即本文方案）在 CIFAR-100 上取得了 92.27 的平均准确率和 94.45 的稳定性，均优于单独对 A、B 估计 Fisher 或使用固定的预计算 Fisher。

### 3. 累积 Fisher 正则化（Accumulated Fisher Regularization）

训练任务 t 时，目标函数被改造为：

$$\mathcal{L}_t'(A,B) = \mathcal{L}_t(A,B) + \frac{\lambda}{2} \,\mathrm{vec}(AB)^\top F_{t-1}^{\mathrm{cum}} \,\mathrm{vec}(AB)$$

其中 $F_{t-1}^{\mathrm{cum}}$ 是前 t-1 个任务 Fisher 矩阵的加权累积：

$$F_t^{\mathrm{cum}} \gets \gamma_t \cdot F_{t-1}^{\mathrm{cum}} + F_t$$

衰减因子 $\gamma$ 控制旧任务重要性的“折现”速度。Figure 4 显示，$\gamma$ 在 0.3–0.9 的宽范围内对稳定性-可塑性权衡的影响不大，说明方法对该超参数不敏感。

### 数据流与训练流程

一次完整的持续学习步骤可以概括为：

1. **初始化**：任务 t 开始时，A、B 从零/均匀分布初始化，基础权重继承自上一任务的合并结果 $W_{t-1}$。
2. **正则化训练**：在训练数据 $\mathcal{D}_t$ 上优化 $\mathcal{L}_t'(A,B)$，其中正则项使用累积 Fisher $F_{t-1}^{\mathrm{cum}}$ 约束 $\mathrm{vec}(AB)$ 偏离旧任务重要方向的程度。
3. **Fisher 估计**：训练收敛后，在最优参数 $W_t^*$ 上采样一批数据，按 Eq. 4 计算当前任务的 Fisher 矩阵 $F_t$。
4. **累积与合并**：按 Eq. (累积 Fisher 更新) 更新 $F_t^{\mathrm{cum}}$，然后将 A、B 合并进基础权重 $W_t = W_{t-1} + AB$，释放 A、B 为下一任务腾出空间。

这一流程的关键性质是：**正则化发生在全维空间 $\Delta W$ 上，但优化和存储始终在低秩空间中进行**，从而在固定内存预算下实现了稳定性与可塑性的有利权衡。Table 5 的内存分析表明，EWC-LoRA 的训练时间与 Vanilla LoRA 几乎相同，额外开销仅来自 Fisher 估计所需的约 6 GB 显存（Table 1）。

## 核心模块与公式推导

### 问题形式化

持续学习场景中，模型依次学习 $T$ 个任务 $\{\mathcal{T}_1, \mathcal{T}_2, \ldots, \mathcal{T}_T\}$。对于任务 $\mathcal{T}_t$，数据集 $\mathcal{D}_t = \{(x_k^t, y_k^t)\}_{k=1}^{|\mathcal{D}_t|}$ 包含输入-标签对，目标是最小化交叉熵损失：

$$\mathcal{L}_t(\mathbf{W}) = -\frac{1}{|\mathcal{D}_t|} \sum_{k=1}^{|\mathcal{D}_t|} \sum_{c=1}^{C} \mathbb{1}_{[y_k^t=c]} \log p_{\mathbf{W}}(y=c \mid x_k^t) \tag{Eq. 1}$$

其中 $\mathbf{W}$ 为模型参数，$p_{\mathbf{W}}(y \mid x)$ 为模型预测分布。

### 标准 EWC 正则化

弹性权重巩固（EWC）通过二次惩罚项约束新任务学习时参数远离旧任务的最优解。对于任务 $t$，正则化损失为：

$$\mathscr{L}_t'(\mathbf{W}) = \mathscr{L}_t(\mathbf{W}) + \frac{\lambda}{2} (\mathbf{W} - \mathbf{W}_{t-1}^*)^\top \mathrm{diag}(\mathbf{F}_{t-1}^{\mathrm{cum}}) (\mathbf{W} - \mathbf{W}_{t-1}^*) \tag{Eq. 2}$$

其中 $\mathbf{W}_{t-1}^*$ 为前 $t-1$ 个任务的最优参数，$\mathbf{F}_{t-1}^{\mathrm{cum}}$ 为累积 Fisher 信息矩阵的对角近似，$\lambda$ 控制正则化强度。惩罚项对每个参数按其重要性加权：Fisher 值大的参数对旧任务更关键，偏离代价更高。

### EWC-LoRA 核心模块

EWC-LoRA 由三个关键模块构成，形成“共享低秩更新 → 全维 Fisher 估计 → 累积正则化”的闭环。

#### 模块一：共享 LoRA 分支

所有任务共享同一组低秩分解矩阵 $\mathbf{A} \in \mathbb{R}^{d \times r}$ 和 $\mathbf{B} \in \mathbb{R}^{r \times k}$，参数更新为 $\Delta\mathbf{W} = \mathbf{A}\mathbf{B}$，其中秩 $r \ll \min(d, k)$。每个任务从零或均匀分布初始化 $\mathbf{A}$ 和 $\mathbf{B}$，训练结束后将学习到的更新合并到基础权重中：$\mathbf{W}_t = \mathbf{W}_{t-1} + \mathbf{A}\mathbf{B}$。与先前方法（InfLoRA、SD-LoRA 等）为每个任务添加独立 LoRA 分支不同，这一设计使存储开销与任务数无关。

#### 模块二：全维 Fisher 估计

在任务 $t$ 训练收敛到最优参数 $\mathbf{W}_t^*$ 后，对全维更新 $\Delta\mathbf{W}$ 计算对角 Fisher 信息矩阵 $\mathbf{F}_t$。第 $i$ 个对角元素定义为：

$$F_t^{i,i} = \mathbb{E}_{x \sim \mathcal{D}_t} \left[ \mathbb{E}_{y \sim p_{\mathbf{W}_t^*}} \left[ \left( \frac{\partial \log p_{\mathbf{W}}(y|x)}{\partial w_i} \Big|_{\mathbf{W}=\mathbf{W}_t^*} \right)^2 \right] \right] \tag{Eq. 4}$$

该估计在 $\mathbf{W}_t^*$ 的全维空间中进行，而非仅在低秩参数 $\mathbf{A}$、$\mathbf{B}$ 上分别计算。理论分析表明，全空间的正则化能更忠实地保持低秩更新所诱导的参数重要性几何结构，而分别对 $\mathbf{A}$ 和 $\mathbf{B}$ 正则化会导致约束失真。从信息几何角度看，可训练子空间中的 Fisher 矩阵等于全空间 Fisher 通过雅可比矩阵的投影：

$$\mathbf{F}_{\theta} = \mathbf{J}^\top \mathbf{F}_{\mathbf{W}} \mathbf{J} \tag{Eq. 7}$$

因此，在全维空间定义 Fisher 并在低秩更新上施加正则化，与在可训练子空间内一致地定义 Fisher 是等价的。

#### 模块三：累积 Fisher 正则化

将当前任务的 Fisher 矩阵按衰减因子 $\gamma$ 合并到历史累积矩阵中：

$$\mathbf{F}_t^{\mathrm{cum}} \gets \gamma_t \cdot \mathbf{F}_{t-1}^{\mathrm{cum}} + \mathbf{F}_t$$

训练任务 $t+1$ 时，正则化项施加于全维更新 $\mathrm{vec}(\mathbf{A}\mathbf{B})$ 上，得到 EWC-LoRA 的完整损失函数：

$$\mathscr{L}_t'(\mathbf{A},\mathbf{B}) = \mathscr{L}_t(\mathbf{A},\mathbf{B}) + \frac{\lambda}{2} \mathrm{vec}(\mathbf{A}\mathbf{B})^\top \mathbf{F}_{t-1}^{\mathrm{cum}} \mathrm{vec}(\mathbf{A}\mathbf{B}) \tag{Eq. 3}$$

该设计使梯度通过 $\mathbf{A}\mathbf{B}$ 的乘积反向传播，Fisher 正则化同时约束两个低秩矩阵，避免了对 $\mathbf{A}$ 和 $\mathbf{B}$ 分别施加独立惩罚所引入的欠约束问题。

### 消融验证：Fisher 估计策略

Table 1 的消融实验对比了四种 Fisher 估计策略在 CIFAR-100（10 任务）上的效果：

- **w/o F**（无正则化的 Vanilla LoRA）：基线，不施加任何遗忘缓解。
- **Precomputed $\mathbf{F}_W$**：在冻结的预训练模型上预计算 Fisher，训练中固定不变。
- **Separate $\mathbf{F}_A, \mathbf{F}_B$**：分别对 $\mathbf{A}$ 和 $\mathbf{B}$ 估计 Fisher 并独立正则化。
- **$\mathbf{F}_{\Delta W}$ (Ours)**：对全维更新 $\Delta\mathbf{W} = \mathbf{A}\mathbf{B}$ 估计 Fisher。

结果表明，$\mathbf{F}_{\Delta W}$ 在最终准确率（87.91）、平均准确率（92.27）、稳定性（94.45）和可塑性（97.99）四项指标上均取得最优。预计算 Fisher 导致最低的可塑性，而分别正则化 $\mathbf{A}$、$\mathbf{B}$ 的性能介于两者之间，验证了全维估计的必要性。额外内存开销约为 6GB。

进一步的 Fisher 类型消融（Table 15）显示，使用 Exact Fisher（从模型预测分布采样）比 Empirical Fisher（从真实标签计算）效果更好，且所需正则化强度更小（$\lambda=10^5$ vs. $\lambda=10^7$），但 Exact Fisher 需要在每个任务结束时进行额外采样。

## 实验与分析

### 核心瓶颈与实验动机

现有低秩持续学习方法（如 InfLoRA、SD-LoRA、CL-LoRA、BiLoRA 等）通过为每个任务分配独立的低秩适配模块来缓解任务间干扰，导致存储开销随任务数量线性增长，且权重正则化在低秩持续学习中未被充分利用。EWC-LoRA 通过弹性权重巩固（EWC）对共享的低秩更新进行正则化，在保持固定内存占用的同时实现更好的稳定性-可塑性权衡。

关键因果机制在于：在全维参数空间中对低秩更新 $\Delta \mathbf{W} = \mathbf{A}\mathbf{B}$ 估计 Fisher 信息矩阵，以准确捕捉参数重要性，然后将该正则化施加于低秩分解矩阵的乘积之上。这与简单地对 $\mathbf{A}$、$\mathbf{B}$ 分别正则化或使用预计算的固定 Fisher 有本质区别——理论分析表明，全空间正则化更好地保持了低秩更新所诱导的真实几何结构和参数重要性，提供了对 $\mathbf{A}$ 和 $\mathbf{B}$ 更忠实有效的约束。

### 视觉基准主实验结果

**Table 2** 展示了四个视觉基准上的完整对比结果。EWC-LoRA 在三个基准上取得最高的最终准确率：

![[assets/figures/papers/iclr26_0012_pZj2DhfaVD_Revisiting_Weight_Regularization_for_Low-Rank_Co/figures/003_Table_2.jpg]]
*Table 2: Comparison results on CIFAR-100, DomainNet, ImageNet-R, and ImageNet-A (in %). Bold and underline indicate the highest and second-highest scores, respectively*

- **CIFAR-100（10 任务）**：最终平均准确率 $\bar{A}_{10}$ 达 87.91%，相较 Vanilla LoRA（82.99%）提升 4.92 个百分点，且优于所有基于结构隔离的低秩 CL 方法（InfLoRA 86.58%、SD-LoRA 86.38%、CL-LoRA 85.16%、BiLoRA 87.43%）。
- **DomainNet（5 任务）**：平均准确率 79.58%，相较 Vanilla LoRA（77.44%）提升 2.14 个百分点，与最优的结构隔离方法 BiLoRA（79.92%）性能相当。
- **ImageNet-A（10 任务）**：最终平均准确率 59.89%，相较 Vanilla LoRA（40.01%）大幅提升 19.88 个百分点，且显著超越所有对比方法（InfLoRA 54.63%、SD-LoRA 57.49%、CL-LoRA 52.30%、BiLoRA 57.81%）。
- **ImageNet-R（10 任务）**：平均准确率 78.95%，相较 Vanilla LoRA（75.57%）提升 3.38 个百分点，与 BiLoRA（79.58%）接近。

四个基准上 EWC-LoRA 相较 Vanilla LoRA 平均提升 8.92%，验证了权重正则化在低秩持续学习中的有效性。

值得注意的是，在 DomainNet 等域迁移显著的基准上，EWC-LoRA 的性能增益较为温和（+2.14%），表明正则化方法应对分布外任务的能力仍有限。这构成一个明确的失败模式：当任务间域差异极大时，共享低秩空间的约束可能不足以完全防止干扰。

### 语言持续学习基准结果

**Table 3** 展示了标准语言持续学习基准上的对比。在 T5-large 骨干上，EWC-LoRA 取得 76.39% 的平均准确率，超越 O-LoRA（72.42%）和 TreeLoRA（75.36%）。在 LLaMA-3.2-1B-Instruct 骨干上，EWC-LoRA 取得 63.08%，与 TreeLoRA（63.23%）相当，优于 O-LoRA（57.24%）。三个不同任务顺序下的结果验证了方法对任务排列的鲁棒性。

### 稳定性-可塑性分析

**Table 4** 报告了各方法的稳定性分数（$1 - \overline{F}$）和可塑性分数（$\frac{1}{T}\sum \frac{A_{i,i}}{A_{i,i}^{\text{ref}}}$）。EWC-LoRA 在 DomainNet（91.51）和 ImageNet-R（98.30）上取得最高稳定性，在 CIFAR-100（94.45）和 ImageNet-A（93.13）上取得次高稳定性。可塑性方面，EWC-LoRA 在所有数据集上均保持较高水平（CIFAR-100 97.99、DomainNet 97.01、ImageNet-R 98.90、ImageNet-A 97.63），与 Vanilla LoRA 的可塑性（接近 100%）差距较小，表明正则化对新任务学习能力的抑制有限。

![[assets/figures/papers/iclr26_0012_pZj2DhfaVD_Revisiting_Weight_Regularization_for_Low-Rank_Co/figures/009_Table_4.jpg]]
*Table 4: Stability (↑) and plasticity (↑) scores of different low-rank CL methods, reflecting how well each model retains previous knowledge and adapts to new tasks. We report the normalized form of the two metrics, which is independent of the absolute performance on the dataset*

**Figure 3(a)** 的稳定性-可塑性曲线进一步揭示了这一权衡：EWC-LoRA 在稳定性-可塑性平面上位于右上角，表明其同时保持了较高的旧知识保留能力和新知识适应能力，而 Vanilla LoRA 虽可塑性极高但稳定性最低。

![[assets/figures/papers/iclr26_0012_pZj2DhfaVD_Revisiting_Weight_Regularization_for_Low-Rank_Co/figures/012_Figure_3.jpg]]
*Figure 3: (a) Stability-Plasticity curves illustrating the trade-off between retaining previous knowledge and learning new tasks. (b) Performance across a range of regularization strengths λ on CIFAR-100 and DomainNet, showing the effect of λ on accuracy*

### Fisher 估计策略消融实验

**Table 1** 是关键的消融实验，比较了四种 Fisher 估计策略在 CIFAR-100 上的效果：

![[assets/figures/papers/iclr26_0012_pZj2DhfaVD_Revisiting_Weight_Regularization_for_Low-Rank_Co/figures/002_Table_1.jpg]]
*Table 1: Comparison of different Fisher estimation strategies on CIFAR-100. “+ Mem.” indicates the additional memory required for Fisher estimation and regularization during training*

| 策略 | $\bar{A}_{10}$ | Avg. | Stability | Plasticity | + Mem. |
|------|---------------|------|-----------|------------|--------|
| w/o F（无正则化） | 82.99 | 88.56 | 83.28 | **99.86** | 0 GB |
| Precomputed $F_W$ | 86.08 | 91.04 | 92.20 | 97.14 | 0 GB |
| Separate $F_A, F_B$ | 86.54 | 91.21 | 92.31 | 97.55 | 3 GB |
| **$F_{\Delta W}$（本文）** | **87.91** | **92.27** | **94.45** | 97.99 | 6 GB |

核心发现：
1. **全维 Fisher（$F_{\Delta W}$）在所有指标上均优于分别估计 $F_A, F_B$**：验证了理论分析中全空间正则化保持真实几何结构的重要性。分别正则化忽略了 $\mathbf{A}$ 和 $\mathbf{B}$ 之间的耦合关系，导致次优的参数重要性估计。
2. **预计算 Fisher 效果最差**：虽然不增加额外内存（Fisher 在训练前基于冻结的预训练模型计算），但其可塑性最低（97.14），说明固定的 Fisher 估计无法适应持续学习中参数重要性的动态变化。
3. **内存开销可接受**：$F_{\Delta W}$ 策略需要 6 GB 额外内存用于 Fisher 估计和正则化，但仍远低于结构隔离方法随任务数线性增长的存储开销。

### Fisher 类型与正则化强度分析

**Table 7** 比较了 Exact Fisher（500 随机样本）和 Empirical Fisher 在 CIFAR-100 上的表现。Exact Fisher 取得更优的 $\bar{A}_{10}$（88.28 vs 87.91）和 Avg.（92.76 vs 92.27），且所需正则化强度更小（$\lambda = 10^5$ vs $10^7$），内存开销更低（约 20 GB vs 24 GB），但训练时间略长（约 14 分钟 vs 11 分钟每任务）。这表明 Exact Fisher 提供了更精确的参数重要性估计，使正则化更有效。

**Figure 3(b)** 展示了不同正则化强度 $\lambda$ 对 DomainNet 准确率的影响：准确率从 $\lambda = 10^1$ 时的约 68% 急剧上升至 $\lambda = 10^5$–$10^7$ 附近的平台期（约 73.5%），随后在 $\lambda = 10^{10}$ 时逐渐下降至约 72.8%。这一倒 U 形曲线清晰地展示了正则化不足（$\lambda$ 过小导致遗忘严重）和过度正则化（$\lambda$ 过大抑制新知识学习）之间的权衡。论文使用统一的 $\lambda = 10^7$ 在所有视觉数据集上取得良好平衡。

### 任务衰减因子 $\gamma$ 的影响

**Table 9** 展示了衰减因子 $\gamma$ 在 CIFAR-100 上的影响。在 $\gamma = 0.3$–$0.9$ 的宽范围内，$\bar{A}_{10}$ 从 87.91 到 88.22、Avg. 从 92.27 到 92.46 变化甚微，稳定性-可塑性权衡保持稳定。$\gamma = 0$（不累积历史 Fisher）导致性能显著下降，$\gamma = 1.0$（等权累积）也略逊于带衰减的设置。这一不敏感性降低了超参数调优负担，但需注意：Fisher 估计仅在每个任务结束时计算一次，当参数远离该任务最优点后可能产生陈旧估计，衰减因子 $\gamma$ 正是为缓解此问题而设计。

### 内存与训练效率

**Table 5** 对比了各方法的内存开销和训练时间。EWC-LoRA 的训练时间与 Vanilla LoRA 几乎相同，因为正则化项的计算开销相对于前向-反向传播可忽略。结构隔离方法（如 InfLoRA、SD-LoRA）因需要维护多个 LoRA 分支，存储开销随任务数线性增长，而 EWC-LoRA 在每个任务结束后将 LoRA 参数合并至骨干网络，总参数量始终与预训练模型一致。

### 不同任务数量的鲁棒性

**Table 6** 展示了在 CIFAR-100 和 ImageNet-R 上 5 任务和 20 任务设置下的最终准确率。EWC-LoRA 在所有设置下均保持最优或次优性能：CIFAR-100 5 任务 $\bar{A}_5$ 达 89.98%，20 任务 $\bar{A}_{20}$ 达 85.46%；ImageNet-R 5 任务 $\bar{A}_5$ 达 86.96%，20 任务 $\bar{A}_{20}$ 达 76.21%。随着任务数增加，所有方法的性能均下降，但 EWC-LoRA 的相对优势保持稳定，验证了固定内存策略在长任务序列下的可扩展性。

### 低秩约束的隐式局限

尽管 EWC-LoRA 取得了显著性能提升，但方法默认所有任务的低秩更新共享相同的表示空间，未考虑为不同任务分配可调节的秩或对低秩空间进行结构化调整。较低的 LoRA 秩 $r$ 可提高稳定性但降低可塑性（**Table 12–13**），EWC-LoRA 在不同秩下表现相对稳定，但这一固定的秩分配策略在任务多样性极高的场景下可能成为瓶颈。此外，在域增量或任务无关的增量学习场景下，EWC-LoRA 的表现仍需进一步验证。

### 补充图表

![[assets/figures/papers/iclr26_0012_pZj2DhfaVD_Revisiting_Weight_Regularization_for_Low-Rank_Co/figures/007_Figure_2.jpg]]
*Figure 2: Task-wise performance comparison of different methods across various datasets*

## 方法谱系与知识库定位

### 与现有低秩持续学习方法的谱系关系

EWC-LoRA 在参数高效持续学习（PECL）的方法谱系中占据一个独特位置：它放弃了当前主流基于结构隔离的范式，回归到权重正则化的路径，但通过全维 Fisher 估计解决了此前低秩空间中正则化失效的瓶颈。

**与结构隔离方法的对比。** InfLoRA、SD-LoRA、CL-LoRA、BiLoRA 等方法的核心机制是为每个新任务分配独立的低秩适配分支（Figure 1a），通过参数空间的物理隔离来防止任务间干扰。这一策略的代价是存储开销随任务数线性增长——每新增一个任务，模型需要额外存储一组 A、B 矩阵。EWC-LoRA 则使用所有任务共享的单一 LoRA 模块，通过 EWC 正则化约束参数更新方向（Figure 1b），将存储需求从 $\mathcal{O}(T \cdot r \cdot d)$ 压缩至 $\mathcal{O}(r \cdot d)$，与任务数 $T$ 无关。这一差异在长任务序列场景下尤为关键：Table 5 显示 EWC-LoRA 的内存开销与 Vanilla LoRA 几乎一致，而结构隔离方法的额外参数随任务累积。

**与正交化约束方法的对比。** O-LoRA 通过约束不同任务的低秩子空间相互正交来减少干扰，本质上仍是一种结构隔离策略。在语言持续学习基准上，EWC-LoRA 在 T5-large 上取得 76.39% 的平均准确率，超越 O-LoRA 的 72.42%（Table 3），表明正则化路径在跨模态场景下同样具有竞争力。

**与提示方法的对比。** L2P、DualPrompt、CODA-Prompt 等方法通过在输入空间插入可学习的提示向量来适应新任务，其参数增长同样与任务数相关。EWC-LoRA 在 ImageNet-A 上取得 59.89% 的最终准确率，而 Vanilla LoRA 仅为 40.01%（Table 2），说明在分布外偏移显著的场景中，对低秩更新的正则化比提示机制能更有效地保留可塑性。

**与朴素 EWC+LoRA 的对比。** 直接将标准 EWC 施加于 A、B 矩阵（Separate F_A, F_B）或使用冻结预训练模型的预计算 Fisher（Precomputed F_W）均导致次优性能。Table 1 的消融实验表明，Separate F_A/F_B 的平均准确率为 91.10，而 F_ΔW（EWC-LoRA）达到 92.27，且稳定性从 91.89 提升至 94.45。附录 A.1.1 从理论上解释了这一差异：在全空间中对 $\mathrm{vec}(\mathbf{AB})$ 施加正则化能够更忠实地保留低秩更新所诱导的真实几何结构和参数重要性，而分别正则化 A 和 B 会丢失两者乘积空间的耦合信息。

### 适用边界

**有效的场景。** EWC-LoRA 在以下条件下表现突出：(1) 任务序列较长时，其固定内存占用的优势愈发明显，CIFAR-100 上 5-task 和 20-task 设置下均保持最高最终准确率（Table 6）；(2) 预训练模型与下游任务之间存在显著分布偏移时，如 ImageNet-A 上的 +19.88% 增益，表明正则化能有效抑制灾难性遗忘而不牺牲对新分布的适应能力；(3) 跨模态迁移场景，语言持续学习基准上的结果（Table 3）验证了方法的通用性。

**增益温和的场景。** 在 DomainNet 等域迁移显著的基准上，EWC-LoRA 相比 Vanilla LoRA 的提升为 +2.14%，明显低于其他数据集。这一现象提示：当任务间的分布差异主要体现为域偏移（而非类别增量）时，仅靠 Fisher 正则化可能不足以捕捉域间参数重要性的精细变化，需要手动验证是否需要结合域自适应策略。

**对超参数的鲁棒性。** 衰减因子 $\gamma$ 在 0.3–0.9 的宽范围内对稳定性-可塑性权衡影响不敏感（Table 9, Figure 4），统一的 $\lambda=10^7$ 在多个数据集上均能取得有利平衡（Figure 3b），表明方法对超参数选择具有较好的容忍度。

### 局限与已知失效模式

**Fisher 陈旧性问题。** EWC-LoRA 仅在每个任务结束时计算一次 Fisher 信息矩阵，随后该矩阵被冻结并累加到累积矩阵中。当后续任务的参数更新远离该任务的最优点时，Fisher 估计的准确性会逐渐退化。Figure 11 和 Figure 12 的实验证实，随着任务索引增加，Fisher 矩阵与真实参数重要性的 Spearman 秩相关系数呈下降趋势。当前通过衰减因子 $\gamma$ 的指数遗忘机制仅能部分缓解这一问题，本质上是一种启发式补偿。

**低秩空间的固定假设。** 方法默认所有任务共享相同的秩 $r$ 和相同的低秩表示空间。Table 12 和 Table 13 显示，较低的秩可提高稳定性但降低可塑性，而 EWC-LoRA 在不同秩下虽表现稳定，但并未针对不同任务动态调整容量分配。在任务异质性较高的场景中，这一固定分配可能导致部分任务的表示能力不足或过度正则化。

**域增量场景的验证缺失。** 当前实验集中在类别增量学习（Class-IL）和任务增量学习（Task-IL）设置，DomainNet 的结果暗示域增量场景下的性能增益有限。方法在任务无关增量学习（Task-Agnostic IL）场景下的表现尚未被验证。

**Exact Fisher 的计算代价。** 虽然 Exact Fisher 相比 Empirical Fisher 取得更优性能（Table 15：92.77 vs. 92.27），且所需正则化强度更小（$\lambda=10^5$ vs. $\lambda=10^7$），但其计算需要从模型分布中采样，增加了训练时间。Table 7 显示 Exact Fisher（500 样本）的训练时间约为 14 分钟/任务，而 Empirical Fisher 约为 10 分钟/任务。

### 开放问题

1. **域增量与任务无关场景的拓展。** EWC-LoRA 在域增量学习或任务边界未知的在线持续学习场景下的表现如何？当前的正则化框架是否能够自然地扩展到这些设置，还是需要引入额外的任务检测或域判别机制？

2. **动态秩分配与结构化低秩空间。** 能否根据任务复杂度和参数重要性分布，为不同任务动态调整可学习的低秩维度？例如，在 Fisher 矩阵范数比 $NR$ 较大的层分配更高的秩，以平衡正则化强度与表示容量。

3. **在线 Fisher 更新机制。** 能否设计无需回放或额外前向传播的在线 Fisher 更新策略，在不增加计算开销的前提下减轻 Fisher 陈旧性？例如，利用优化轨迹的曲率信息进行增量更新。

4. **理论界的建立。** 在全维 Fisher 正则化与低秩约束之间是否存在更紧的理论界，能够指导 $\lambda$ 和秩 $r$ 的自动选择？附录 A.1.2 的 Fisher 投影恒等式 $\mathbf{F}_{\theta} = \mathbf{J}^{\top} \mathbf{F}_{\mathbf{W}} \mathbf{J}$ 提供了初步的理论框架，但尚未导出关于稳定性-可塑性权衡的定量保证。

5. **与回放方法的协同。** EWC-LoRA 的固定内存特性使其天然适合与经验回放结合——节省的参数存储空间可用于存储回放样本。这种混合策略能否在极低内存预算下实现超越纯正则化或纯回放方法的性能？

## 原文 PDF

![[paperPDFs/ICLR_2026/Revisiting_Weight_Regularization_for_Low_Rank_Continual_Learning.pdf]]
