---
title: "Remaining-data-free Machine Unlearning by Suppressing Sample Contribution"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Remaining_data_free_Machine_Unlearning_by_Suppressing_Sample_Contribution.pdf
openreview_forum_id: 3iw5t2W41F
aliases:
- MMMUBMIS
- RDFMUBSSC
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/algorithms
core_operator: "预训练模型对遗忘样本的输入梯度敏感性，尤其是目标类logit与无关类logit之间梯度Frobenius范数之差（灵敏度差距），可以作为样本贡献的可靠代理。通过直接缩小该差距，可以在不影响保留数据性能的前提下撤回样本贡献，从而彻底消除对保留数据的依赖。"
primary_logic: "训练过程中，样本的贡献集中体现为使模型对该样本的目标类logit敏感性变得远超无关类logit。通过最小化两者的差距，可以精确模拟重新训练模型（从未见过该样本）的行为，首次实现无保留数据条件下的高性能机器遗忘。"
claims:
- "样本对训练过程的贡献近似反映在预训练模型对该样本的输出敏感性上，且自影响项远大于其他样本的残差项。"
- "训练后，目标类logit的梯度范数变得远大于无关类logit，形成显著的灵敏度差距，而重新训练模型会使遗忘数据的该差距缩小。"
- "MU-Mis通过最小化目标类与无关类输入梯度Frobenius范数的平方差，成功将忘记数据的灵敏度差距拉回初始水平，无需访问任何保留数据即可达成与重新训练模型近似的遗忘效果。"
- "MU-Mis在CIFAR-100、PinsFaceRecognition、Tiny ImageNet等6个数据集上的全类、子类和序列遗忘任务中，性能与当前最优的依赖保留数据方法持平，并显著超越所有现有无保留数据方法。"
---

# Remaining-data-free Machine Unlearning by Suppressing Sample Contribution

> [!tip] 核心洞察
> 训练过程中，样本的贡献集中体现为使模型对该样本的目标类logit敏感性变得远超无关类logit。通过最小化两者的差距，可以精确模拟重新训练模型（从未见过该样本）的行为，首次实现无保留数据条件下的高性能机器遗忘。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过抑制样本贡献实现无保留数据机器遗忘 |
| 英文题名 | Remaining-data-free Machine Unlearning by Suppressing Sample Contribution |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=3iw5t2W41F); [GitHub](https://github.com/poppopbean0903/MU-Mis) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/algorithms |
| Method | MU-Mis (Machine Unlearning by Minimizing Input Sensitivity) |
| Dataset | CIFAR-100 full-class (VGG-16), Tiny ImageNet full-class (ViT), Overall (6 datasets) |

> [!tip] 效果简介
> - CIFAR-100 full-class (VGG-16) 上，FA (Forgetting Accuracy) ↓ 为 0.00±0.28，对比 JIT: 3.73，变化 -3.73。
> - CIFAR-100 full-class (VGG-16) 上，Avg. Gap ↓ 为 0.32，对比 JIT: 3.21，变化 -2.89。
> - Tiny ImageNet full-class (ViT) 上，RTE (min) ↓ 为 3，对比 SalUn: 81，变化 -78 (27倍加速)。

## 概述

现有机器遗忘方法面临一个根本性瓶颈：无法精确量化并解耦各训练样本对模型的贡献，转而采用随机标签、知识蒸馏等启发式策略，导致模型在保留数据上的效用严重退化，进而必须依赖保留数据来修复——而这些数据在实践中往往不可获取。

本文揭示了这一瓶颈的突破口：预训练模型对遗忘样本的输入梯度敏感性，尤其是目标类logit与无关类logit之间梯度Frobenius范数之差（灵敏度差距），可以作为样本贡献的可靠代理。训练过程中，样本的贡献集中体现为使模型对该样本的目标类logit敏感性变得远超无关类logit；通过直接缩小该差距，可以在不影响保留数据性能的前提下撤回样本贡献。

基于此洞察，本文提出 **MU-Mis**（Machine Unlearning by Minimizing Input Sensitivity），一种完全无需保留数据的机器遗忘方法。其核心损失函数最小化目标类与随机选取无关类的输入梯度Frobenius范数平方差，配合基于无关类敏感度恢复的自适应停止准则，首次实现无保留数据条件下的高性能机器遗忘。

在CIFAR-100、PinsFaceRecognition、Tiny ImageNet等6个数据集上的全类、子类和序列遗忘任务中，MU-Mis的性能与当前最优的依赖保留数据方法持平，并显著超越所有现有无保留数据方法。例如，在CIFAR-100全类遗忘（VGG-16）上，MU-Mis的Avg. Gap仅为0.32，而最强无保留数据基线JIT为3.21；在Tiny ImageNet（ViT）上，MU-Mis的运行时间仅为3分钟，相比SalUn的81分钟实现27倍加速。

## 背景与动机

### 问题背景：机器遗忘与保留数据依赖困境

随着数据隐私法规（如GDPR的“被遗忘权”）的强化，**机器遗忘（Machine Unlearning）** 要求模型在移除特定训练数据后，其行为应与从未见过该数据的重新训练模型一致。理想目标是在忘记集 $\mathcal{D}_f$ 上消除模型的知识，同时保持对保留集 $\mathcal{D}_r$ 的效用。

然而，现有方法面临一个根本性瓶颈：**无法精确量化并解耦各训练样本对模型的贡献**。主流方法转而采用启发式策略——随机标签（RL）、负梯度（NG）、知识蒸馏（SCRUB、DUCK）或选择性突触削弱（SSD）——这些策略在撤回样本影响时不可避免地干扰了模型在保留数据上的表征，导致效用严重退化。为修复这一退化，几乎所有高性能遗忘方法（如SalUn、MUNBa、LoTus）都必须**依赖保留数据**来校准模型或恢复性能。但在实践中，保留数据往往因隐私限制、存储成本或数据时效性而不可获取，使得这类方法的应用场景严重受限。

### 现有无保留数据方法的缺口

当前仅有的少数无保留数据遗忘方法（NG、RL、JIT、SCAR）在性能上与依赖保留数据的方法之间存在显著鸿沟。例如，在全类遗忘任务上，JIT的遗忘准确率（FA）和平均差距（Avg. Gap）远逊于SCRUB等依赖保留数据的方法。这一缺口的核心原因在于：**缺乏一个精准的、无需保留数据即可量化的样本贡献信号**，导致遗忘过程要么不彻底，要么过度损害模型效用。

### 本文动机：以输入敏感性为贡献代理

本文的核心洞察是：**训练过程中，样本的贡献集中体现为使模型对该样本的目标类logit敏感性变得远超无关类logit**。具体而言，预训练模型对遗忘样本的输入梯度——尤其是目标类logit $f_c$ 与无关类logit $f_{c'}$ 之间梯度Frobenius范数之差（灵敏度差距）——可以作为样本贡献的可靠代理。理论分析表明，在梯度下降动态中，自影响项远大于其他样本的残差项（Section 3.2），因此通过直接缩小该灵敏度差距，可以在不触及保留数据的前提下撤回样本贡献，精确模拟重新训练模型的行为。

基于这一发现，本文提出 **MU-Mis（Machine Unlearning by Minimizing Input Sensitivity）**，首次实现完全无保留数据条件下的高性能机器遗忘，其性能与当前最优的依赖保留数据方法持平，并显著超越所有现有无保留数据方法。

## 核心创新

### 问题瓶颈：现有遗忘方法为何必须依赖保留数据

现有机器遗忘方法面临一个根本性困境：它们无法精确量化并解耦各训练样本对模型的贡献，因此只能采用随机标签、知识蒸馏、负梯度等启发式策略来"破坏"模型对遗忘数据的记忆。这些粗糙的操作不可避免地会损害模型在保留数据上的效用，迫使方法必须重新访问保留数据来修复损伤。然而，在实际遗忘请求场景中（如用户数据删除、版权内容移除），保留数据往往不可获取——这正是"无保留数据机器遗忘"（remaining-data-free machine unlearning）的核心挑战。

### 关键发现：灵敏度差距作为样本贡献的可靠代理

MU-Mis的核心创新在于发现了一个可精确量化样本贡献的信号：**预训练模型对遗忘样本的输入梯度敏感性，特别是目标类logit与无关类logit之间梯度Frobenius范数的差距**。

理论分析（Section 3.2）揭示了训练过程中样本贡献的本质：从梯度下降动态推导，样本 $x_i$ 对训练过程的贡献近似反映在预训练模型对该样本的输出敏感性 $\partial f(x_i; w_p) / \partial x_i$ 上，且自影响项 $S_k(x_i, x_i)$ 远大于其他样本的残差项。实证验证（Figure 2, Figure 3）进一步表明：

- **训练前**：模型对训练数据的输入梯度范数约为 $10^{-4}$，目标类与无关类的灵敏度几乎无差异。
- **训练后**：输入梯度范数急剧增长至 $10^3$ 量级，且目标类logit的梯度范数 $\|\nabla_x f_c\|_F$ 显著超越无关类 $\|\nabla_x f_{c'}\|_F$，形成明显的**灵敏度差距**。

这一差距正是样本在训练过程中"贡献"的集中体现：样本通过梯度更新不断放大模型对其目标类的敏感性，使其远超无关类。而重新训练模型（从未见过该样本）则会使遗忘数据的这一差距缩小——这为无保留数据遗忘提供了精确的优化方向。

### 方法创新：三个关键设计突破

基于上述发现，MU-Mis通过三个相互协同的设计，首次实现了完全无保留数据的高性能机器遗忘：

**1. 遗忘损失函数（核心changed slot）**

MU-Mis摒弃了随机标签、知识蒸馏等启发式策略，直接针对灵敏度差距构建损失函数（Equation 3）：

$$\mathcal{L}(\mathcal{D}_f; w) = \frac{1}{N_f} \sum_{x_f \in \mathcal{D}_f} \left( \|\nabla_x f_c(x_f, w)\|_F^2 - \|\nabla_x f_{c'}(x_f, w)\|_F^2 \right)$$

其中 $c$ 为样本的目标类，$c'$ 为随机选取的无关类。通过最小化目标类与无关类输入梯度Frobenius范数的平方差，该方法精确地撤回样本在训练中产生的贡献，使模型对该样本的响应回归至"从未见过"的状态。消融实验（Table A12）证实，联合优化目标类（TC）和无关类（OC）项是必要的——仅用TC会导致遗忘不完全，仅用OC会严重损害模型效用。

**2. 完全消除对保留数据的依赖（核心changed slot）**

传统方法必须使用保留数据来计算知识蒸馏方向或恢复模型效用，而MU-Mis的损失函数仅需对遗忘样本本身进行梯度操作。这一设计使其成为真正意义上的"remaining-data-free"方法——在遗忘过程中无需访问任何保留数据，从根本上解决了实际场景中保留数据不可获取的困境。

**3. 自适应停止准则（核心changed slot）**

传统方法依赖固定迭代次数或保留数据上的验证指标来决定何时停止优化，这在无保留数据设定下不可行。MU-Mis创新性地提出基于无关类敏感度恢复的自适应停止准则（Algorithm 1）：

$$\frac{\|\nabla_{\mathbf{x}} f_{c'}(\mathcal{D}_f, w_t)\|_F}{\|\nabla_{\mathbf{x}} f_{c'}(\mathcal{D}_f, w_0)\|_F} > \delta$$

当无关类logit的输入梯度范数恢复至预训练初始值的 $\delta$ 倍时，优化自动终止。这一准则的理论依据在于：样本贡献撤回后，无关类的敏感度应回归至训练前的基准水平。实验表明（Figure A2），该准则对 $\delta$ 的选取稳定，固定学习率下性能几乎不随 $\delta$ 变化，大幅降低了调参负担。

### 创新效果：性能与效率的双重突破

MU-Mis的创新设计在多个维度上取得了显著突破：

- **性能持平依赖保留数据的最优方法**：在CIFAR-100、PinsFaceRecognition、Tiny ImageNet等6个数据集的全类、子类和序列遗忘任务中，MU-Mis的Avg. Gap与SCRUB、SSD等依赖保留数据的SOTA方法持平（Table 1, Table 2）。
- **显著超越所有现有无保留数据方法**：相比JIT、SCAR、NG、RL等无保留数据基线，MU-Mis在FA、Avg. Gap和MIA指标上均取得显著优势（Abstract, Table 1-3）。
- **效率大幅提升**：在Tiny ImageNet全类遗忘任务上，MU-Mis仅需3分钟完成，而依赖保留数据的SalUn需要81分钟，加速达27倍（Table 3）。

### 局限与展望

尽管MU-Mis在全类遗忘场景下表现卓越，但在最具挑战性的随机子集遗忘场景下，与理想重训模型相比效用差距仍然明显。此外，对高记忆度样本的遗忘可能引起较大的剩余数据性能下降，提示灵敏度差距不能完全均一地代理各类样本的贡献。未来工作可探索将一阶灵敏度差距与二阶loss曲率更直接地关联，以提供更强的理论保证并改进随机子集遗忘性能。

## 整体框架

![[assets/figures/papers/iclr26_0011_3iw5t2W41F_Remaining-data-free_Machine_Unlearning_by_Suppre/figures/001_Figure_1.jpg]]
*Figure 1: A brief overview of the theoretical connection between sample’s contribution and a pre-trained model’s input sensitivity. The dashed lines illustrate how the influence of a training sample propagates through gradient updates to the pre-trained model. When a sample participates in training, the gradient it contributes induces an update of the model in function space, which inherently increases the learned function’s sensitivity to that sample’s input*

MU-Mis 的 pipeline 围绕一个核心发现构建：**预训练模型对遗忘样本的输入敏感性差异（目标类 logit 与无关类 logit 的梯度 Frobenius 范数之差）是样本贡献的可靠代理信号**。整个框架通过三个串联模块，在不访问任何保留数据的前提下精确撤回目标样本在训练过程中注入的贡献。

### 模块一：输入敏感性估计

该模块接收预训练模型权重 $w_0$ 和遗忘数据集 $\mathcal{D}_f$，对每个遗忘样本 $x_f$ 计算两类输入梯度：

- **目标类梯度** $\nabla_x f_c(x_f, w)$：模型对样本真实类别 $c$ 的 logit 关于输入的梯度；
- **无关类梯度** $\nabla_x f_{c'}(x_f, w)$：随机选取的一个非目标类 $c'$ 的 logit 关于输入的梯度。

理论分析（Section 3.2）表明，训练过程中样本的贡献集中体现为 $\|\nabla_x f_c\|_F$ 远超 $\|\nabla_x f_{c'}\|_F$ 的灵敏度差距，且自影响项 $S_k(x_i, x_i)$ 在输入敏感性分解中占主导地位（Figure 1）。因此，这两组梯度范数天然构成了衡量“该样本对模型留下了多少印记”的定量指标。

### 模块二：灵敏度差距最小化损失

基于模块一的估计，MU-Mis 构造核心遗忘损失函数（Equation 3）：

$$\mathcal{L}(\mathcal{D}_f; w) = \frac{1}{N_f} \sum_{x_f \in \mathcal{D}_f} \left( \|\nabla_x f_c(x_f, w)\|_F^2 - \|\nabla_x f_{c'}(x_f, w)\|_F^2 \right)$$

该损失直接驱动优化过程缩小目标类与无关类的灵敏度差距。其设计逻辑是：**训练使目标类敏感度膨胀，遗忘则应将其压回初始水平，同时提升无关类敏感度，模拟重新训练模型“从未见过该样本”的状态**。消融实验（Table A12）证实，联合优化目标类项和无关类项是必要的——仅用目标类项会导致遗忘不完全，仅用无关类项则严重损害保留数据上的模型效用。

### 模块三：自适应停止准则

传统遗忘方法依赖保留数据上的验证指标来决定停止时机，MU-Mis 则通过监控无关类 logit 的输入梯度范数恢复程度来自适应终止：

$$\frac{\|\nabla_{\mathbf{x}} f_{c'}(\mathcal{D}_f, w_t)\|_F}{\|\nabla_{\mathbf{x}} f_{c'}(\mathcal{D}_f, w_0)\|_F} > \delta$$

当无关类敏感度恢复至预训练初始值的 $\delta$ 倍以上时，认为样本贡献已成功撤回，优化停止。Figure A1 和 Figure A2 的实验表明，该准则对学习率和 $\delta$ 的取值具有较好的稳定性，性能几乎不随 $\delta$ 变化。

### 输入输出流总结

| 阶段 | 输入 | 输出 | 依赖保留数据 |
|------|------|------|------------|
| 敏感性估计 | 预训练模型 $w_0$，遗忘集 $\mathcal{D}_f$ | 目标类/无关类梯度范数对 | 否 |
| 差距最小化 | 梯度范数对，损失函数 | 更新后的模型权重 $w_t$ | 否 |
| 自适应停止 | 无关类敏感度历史，阈值 $\delta$ | 遗忘完成信号 | 否 |

整个 pipeline 的核心优势在于**完全消除了对保留数据的依赖**——从信号提取、损失构造到停止决策，所有操作仅涉及遗忘样本本身和预训练模型的内部梯度信息。这使得 MU-Mis 在保留数据不可获取的实际场景（如用户数据删除请求）中具备天然适用性，同时在 CIFAR-100、Tiny ImageNet 等六个数据集上取得了与依赖保留数据的 SoTA 方法持平的性能（Table 1, Table 2），并显著超越所有现有无保留数据方法。

## 核心模块与公式推导

MU-Mis 的遗忘过程由三个核心模块串联构成：**输入敏感性估计**、**灵敏度差距最小化损失**、以及**基于敏感度恢复的自适应停止准则**。整个流程完全在遗忘数据 $`\mathcal{D}_f`$ 上运行，无需访问任何保留数据。

### 模块一：输入敏感性估计

该模块计算预训练模型 $`w_p`$ 对遗忘样本 $`x_f`$ 的输出梯度，作为样本贡献的代理信号。具体而言，对于每个 $`x_f`$，需要计算两类梯度：

- **目标类梯度**：$`\|\nabla_{\mathbf{x}} f_c(x_f, w)\|_F^2`$，即模型对 $`x_f`$ 的目标类 logit $`f_c`$ 关于输入 $`\mathbf{x}`$ 的 Frobenius 范数平方。
- **无关类梯度**：$`\|\nabla_{\mathbf{x}} f_{c'}(x_f, w)\|_F^2`$，其中 $`c'`$ 是从除 $`c`$ 以外的类别中随机选取的一个无关类。

这一设计的理论依据在于：训练过程中，样本的贡献集中体现为使模型对该样本的目标类 logit 敏感性远超无关类 logit（Section 3.3）。因此，这两类梯度范数的差距——**灵敏度差距**——天然地编码了该样本在训练中注入的贡献量。

### 模块二：灵敏度差距最小化损失

基于上述代理信号，MU-Mis 的核心损失函数直接最小化目标类与无关类输入梯度 Frobenius 范数的平方差：

$$`\mathcal{L}(\mathcal{D}_f; w) = \frac{1}{N_f} \sum_{x_f \in \mathcal{D}_f} \left( \|\nabla_{\mathbf{x}} f_c(x_f, w)\|_F^2 - \|\nabla_{\mathbf{x}} f_{c'}(x_f, w)\|_F^2 \right)`$$

其中 $`N_f`$ 为遗忘样本数量，$`c`$ 为 $`x_f`$ 的真实标签，$`c'`$ 为随机选取的无关类。

**公式变量含义**：
- $`f_c(x_f, w)`$：模型在参数 $`w`$ 下对输入 $`x_f`$ 的第 $`c`$ 类 logit 输出。
- $`\nabla_{\mathbf{x}} f_c`$：logit $`f_c`$ 对输入 $`\mathbf{x}`$ 的梯度，反映模型输出对该输入变化的敏感程度。
- $`\|\cdot\|_F^2`$：Frobenius 范数的平方，用于量化梯度的整体强度。

通过最小化该损失，MU-Mis 同时压低目标类的输入敏感性并抬高无关类的输入敏感性，从而将灵敏度差距拉回至模型从未见过该样本时的水平——这恰好模拟了重新训练模型的行为（Figure 4）。

消融实验（Table A12）证实，联合优化目标类项和无关类项是必要的：仅用目标类项会导致遗忘不完全，仅用无关类项则会严重损害模型效用。此外，MU-Mis 对梯度范数类型不敏感，使用 Frobenius 范数或 L2 范数均可获得相似性能（Table A13）。

### 模块三：自适应停止准则

由于 MU-Mis 无法使用保留数据来监控模型效用，论文提出了一种基于无关类敏感度恢复的自适应停止机制。具体地，当满足以下条件时停止优化：

$$`\frac{\|\nabla_{\mathbf{x}} f_{c'}(\mathcal{D}_f, w_t)\|_F}{\|\nabla_{\mathbf{x}} f_{c'}(\mathcal{D}_f, w_0)\|_F} > \delta`$$

其中 $`w_0`$ 为预训练模型的初始参数，$`w_t`$ 为第 $`t`$ 步优化后的参数，$`\delta`$ 为预设阈值。

**直觉解释**：训练前，模型对任意类别的输入敏感性都处于较低水平；训练后，目标类敏感性被显著放大。MU-Mis 的优化过程会逐步恢复无关类的敏感性至其初始水平，这标志着该样本的贡献已被成功撤回。实验表明，该停止准则对 $`\delta`$ 的取值相当稳定，固定学习率下性能几乎不随 $`\delta`$ 变化（Figure A2），从而避免了过遗忘或欠遗忘的风险。

### 损失变体：动态加权

在某些场景下，论文引入了带指示器动态加权的损失变体以加速优化（Appendix F.4）：

$$`\mathcal{L} = \frac{1}{N} \sum \left[ \alpha_c \cdot \|\nabla_{\mathbf{x}} f_c\|_F^2 - \alpha_{c'} \cdot \|\nabla_{\mathbf{x}} f_{c'}\|_F^2 \right]`$$

其中 $`\alpha_c`$ 和 $`\alpha_{c'}`$ 为根据当前敏感度状态动态调整的权重系数。该变体在保持核心机制不变的前提下，为特定遗忘任务提供了更灵活的优化路径。

## 实验与分析

### 核心瓶颈验证：输入灵敏度差距作为样本贡献代理

MU-Mis的理论基础建立在两个关键实证发现之上。第一，**训练使模型对训练数据的输入灵敏度产生数量级增长**：图2显示，随机初始化模型对训练样本的输入梯度Frobenius范数$||\nabla_x f||_F$约为$10^{-4}$量级，而训练完成后暴涨至$10^3$量级，表明模型对训练数据的变化变得高度敏感。第二，**这种灵敏度增长并非均匀分布，而是集中在目标类logit上**：图3表明，训练后目标类logit的输入梯度范数$||\nabla_x f_c||_F$远超无关类logit的$||\nabla_x f_{c'}||_F$，形成显著的“灵敏度差距”。这一差距正是样本在训练过程中贡献的集中体现——样本通过梯度下降不断放大模型对其目标类的敏感度，使其区别于无关类。

![[assets/figures/papers/iclr26_0011_3iw5t2W41F_Remaining-data-free_Machine_Unlearning_by_Suppre/figures/003_Figure_2.jpg]]
*Figure 2: Input sensitivity \| $\nabla _ { \mathbf { x } }$ f \|$_ { F }$ of training data before and after training. Left: In randomly initialized model w0. Right: In well-trained model $w _ { p }$ . After training, the model exhibits significantly increased sensitivity to the training data, reflecting their contribution during training

![[assets/figures/papers/iclr26_0011_3iw5t2W41F_Remaining-data-free_Machine_Unlearning_by_Suppre/figures/005_Figure_3.jpg]]
*Figure 3: Input sensitivity \| $\nabla _ { \mathbf { x } } f _ { c }$ \|$_ { F }$ and \| $\check { \nabla } _ { \mathbf { x } } f _ { c ^ { \prime } }$ \|$_ { F }$ before and after training. Left: randomly initialized model $w _ { 0 }$ . Right: well-trained model $w _ { p }$ . . After training, the gap between target and irrelevant class sensitivities enlarges, providing a clearer signal of the sample’s contribution

图4进一步验证了遗忘方向：对于遗忘数据，重新训练模型（从未见过这些样本）的目标类灵敏度较低、无关类灵敏度较高，即灵敏度差距缩小。这为MU-Mis的优化目标提供了直接的经验支撑：**通过缩小遗忘数据上的灵敏度差距，可以近似模拟重新训练模型的行为**。

![[assets/figures/papers/iclr26_0011_3iw5t2W41F_Remaining-data-free_Machine_Unlearning_by_Suppre/figures/006_Figure_4.jpg]]
*Figure 4: Ratio of input sensitivity difference ∆ rise and fall of the forgetting data under different unlearning settings. From left to right, ∆ is the sample-wise difference between the retrained and pre-trained model on \| $\nabla _ { \pmb { x } } f _ { c }$ \|$_ { F }$ , \| $\mathbf { \bar { V } } _ { \pmb { x } } f _ { c ^ { \prime } }$ \|$_ { F }$ and \| $\dot { \nabla } _ { \pmb { x } } f _ { c }$ \|$_ { F }$ - \| $\nabla _ { \pmb { x } } f _ { c ^ { \prime } }$ \|$_ { F }$ . Sample’s contribution to input sensitivity includes promoting \| $\nabla _ { x } f _ { c }$ \|$_ { F }$ and suppressing \| $\nabla _ { x } f _ { c ^ { \prime } }$ \|$_ { F }$ , thereby enlarging the magnitude gap \| $\mathrm { \bar { V } }$...

### 全类遗忘主结果：与依赖保留数据方法持平

表1汇总了CIFAR-100、PinsFaceRecognition和Tiny ImageNet三个数据集上的全类遗忘性能。MU-Mis在所有场景下均取得**与当前最优依赖保留数据方法（SCRUB、SSD、SalUn等）持平的遗忘效果**，同时显著超越所有现有无保留数据方法（NG、RL、JIT、SCAR）。

以CIFAR-100（ResNet-18）为例，MU-Mis取得FA=0.00、RA=76.42、TA=75.64，Avg. Gap仅为0.07，MIA=0.00——这意味着遗忘集准确率归零、保留集效用几乎无损、且无法通过成员推理攻击检测到遗忘样本的痕迹。相比之下，最强的无保留数据基线JIT在相同设置下FA=3.73、Avg. Gap=3.21（表A9，VGG-16），差距显著。

在更具挑战性的Tiny ImageNet上，MU-Mis取得FA=0.00、RA=64.95、TA=64.85，Avg. Gap=0.11，同样与依赖保留数据的SCRUB（Avg. Gap=0.09）和SSD（Avg. Gap=0.14）处于同一水平。

### 子类遗忘：应对不同难度场景

表2展示了CIFAR-20子类遗忘任务的结果，涵盖“Rocket”和“Sea”两个难度不同的子类（重新训练模型对遗忘子类的泛化能力不同）。在Sea子类（更难遗忘）上，MU-Mis取得Avg. Gap=0.18，优于SCRUB（0.22）和SalUn（0.26）；在Rocket子类上，MU-Mis的Avg. Gap=0.07，仅次于SCRUB（0.06）。这表明**灵敏度差距最小化策略对不同难度的遗忘场景均具有鲁棒性**。

值得注意的是，MU-Mis在子类遗忘中的MIA指标略高于SCRUB（Sea: 7.67 vs 0.00），说明在部分场景下隐私保护尚有提升空间，但整体仍远优于其他无保留数据方法。

### 效率优势：ViT上的27倍加速

表3报告了ViT在Tiny ImageNet全类遗忘上的结果。MU-Mis仅需**3分钟**完成遗忘，而依赖保留数据的SalUn需要81分钟——**加速27倍**。同时MU-Mis取得Avg. Gap=0.68，虽略高于SalUn（0.55），但考虑到其完全无需保留数据且速度优势巨大，这一权衡在实践中有重要意义。表A10进一步显示，在CIFAR-20 Sea子类ViT场景下，MU-Mis仅需0.5分钟即完成遗忘，Avg. Gap=0.17，为所有方法最优。

![[assets/figures/papers/iclr26_0011_3iw5t2W41F_Remaining-data-free_Machine_Unlearning_by_Suppre/figures/009_Table_3.jpg]]
*Table 3: Performance overview for full class unlearning task evaluated on Tiny ImageNet using ViT. RTE is reported in minute*

### 序列遗忘稳定性

图5和图6展示了序列遗忘过程中MU-Mis与重新训练模型之间的性能差异动态。在全类和子类序列遗忘任务中，MU-Mis的效用Avg. Gap和弹性Avg. Gap始终保持在较小水平，与依赖保留数据的SSD方法相当，且在整个序列过程中偏差不累积。图7的KL散度分析进一步证实，MU-Mis遗忘后的模型输出分布与重新训练模型高度一致，表明其不仅抹除了遗忘数据的直接影响，也较好地恢复了模型的决策边界。

### 消融实验：损失项的必要性

表A12的消融实验揭示了损失函数两项的各自作用：
- **仅优化目标类项（TC only）**：遗忘不完全，FA未能归零，说明单纯降低目标类灵敏度不足以撤回全部贡献。
- **仅优化无关类项（OC only）**：虽然能提升无关类灵敏度，但严重损害保留数据效用，RA大幅下降。
- **联合优化两项**：才能同时实现完全遗忘和效用保持，验证了公式(3)设计的必要性。

### 设计选择的鲁棒性

表A13表明，MU-Mis对梯度范数类型不敏感——使用Frobenius范数或L2范数均可获得相似性能，说明核心机制在于缩小灵敏度差距本身，而非特定的范数选择。表A14显示，通过Jacobian正则化强制模型平滑反而会降低遗忘效果，这反向证明了**输入灵敏度是比模型平滑性更精准的引导信号**。

### 自适应停止准则的稳定性

图A1和A2展示了停止阈值$\delta$的影响。基于无关类敏感度恢复的自适应停止准则表现稳定：在合理的学习率下，最终性能几乎不随$\delta$变化。这一特性降低了调参负担——用户只需设定一个宽松的$\delta$范围，算法会自动在贡献撤回完成时停止，无需依赖保留数据上的验证指标。

### 失败模式与局限性

尽管MU-Mis在全类和子类遗忘中表现卓越，但在**随机子集遗忘**场景下存在明显局限。表A7显示，在CIFAR-10和SVHN上随机遗忘10%样本时，MU-Mis虽然降低了MIA（隐私泄露风险），但Avg. Gap分别为1.64和1.12，与重新训练模型的效用差距仍然显著。这表明当遗忘样本分散在多个类别中时，灵敏度差距信号的信噪比下降，难以精准定位单个样本的贡献。

此外，对**高记忆度样本**的遗忘可能引起较大的剩余数据性能下降，提示灵敏度差距与样本记忆度之间并非简单的线性关系——某些样本的贡献可能与其他样本的表示高度纠缠，单纯抑制其灵敏度差距会波及无辜样本。

这些失败模式指向两个开放问题：(1) 如何将一阶灵敏度差距与二阶loss曲率关联以增强理论保证；(2) 如何在随机子集遗忘中实现更精细的贡献定位，以同时完美保留模型效用。

### 补充图表

![[assets/figures/papers/iclr26_0011_3iw5t2W41F_Remaining-data-free_Machine_Unlearning_by_Suppre/figures/028_Table_14.jpg]]
*Table 14: Table A12: Ablation study on each term of our loss in full class (Rocket) unlearning. TC (Target Class) refers to the first term and OC (Other Class) refers to the second term*

## 方法谱系与知识库定位

### 与现有方法的关系

MU-Mis 的提出根植于现有机器遗忘方法的一个根本性瓶颈：无法精确量化并解耦各训练样本对模型的贡献，转而采用随机标签、知识蒸馏、负梯度等启发式策略，导致模型在保留数据上的效用严重退化，进而必须依赖保留数据来修复——而这些数据在实践中往往不可获取。MU-Mis 通过理论推导和实证验证，首次建立了样本贡献与预训练模型输入敏感性之间的桥梁，从而彻底消除了对保留数据的依赖。

**与依赖保留数据方法的对比。** SCRUB、SSD、SalUn、DUCK/Distill、MUNBa、LoTus 等方法虽然在遗忘效果上表现优异，但均需访问保留数据来恢复模型效用或计算遗忘方向。MU-Mis 在 CIFAR-100、PinsFaceRecognition、Tiny ImageNet 等 6 个数据集上的全类、子类和序列遗忘任务中，性能与这些最优依赖保留数据方法持平（Table 1, Table 2），同时完全无需保留数据。在 Tiny ImageNet 的 ViT 全类遗忘任务上，MU-Mis 的运行时间仅 3 分钟，而 SalUn 需要 81 分钟，实现了 27 倍加速（Table 3）。

**与现有无保留数据方法的对比。** 现有无保留数据方法包括负梯度法（NG）、随机标签法（RL）、基于局部 Lipschitz 平滑的 JIT，以及基于知识蒸馏和 OOD 数据的 SCAR。这些方法在遗忘准确率（FA）、平均效用差距（Avg. Gap）和成员推理攻击（MIA）等指标上均显著弱于 MU-Mis。例如，在 CIFAR-100 全类遗忘任务中，MU-Mis 的 Avg. Gap 为 0.07，而 JIT 为 3.21，差距达 2.89（Table A9）。MU-Mis 的核心优势在于：它直接操作样本贡献的代理信号（目标类与无关类 logit 的输入梯度 Frobenius 范数之差），而非依赖间接的启发式目标。

**方法谱系中的定位。** MU-Mis 可被归类为“基于样本贡献撤回的无保留数据遗忘方法”，其理论根基在于从梯度下降动态推导出训练样本的贡献与模型输入敏感性之间的关系（Section 3.2, Eq.(1)）。这一视角与影响力函数（influence function）和反事实学习有理论关联，但 MU-Mis 的独特之处在于将贡献量化为可优化的灵敏度差距信号，并通过最小化该差距来模拟重新训练模型的行为。

### 适用边界与条件

**适用场景。** MU-Mis 在全类遗忘（full-class unlearning）和子类遗忘（sub-class unlearning）任务上表现卓越，尤其适用于目标类与保留类边界清晰的场景。在序列遗忘（sequential unlearning）中，MU-Mis 与 SSD 表现出与重新训练模型最小的效用差距和韧性差距（Figure 6），且 KL 散度累积缓慢（Figure 7），表明其适合连续多次遗忘请求的生产环境。

**技术前提。** 方法假设预训练模型对遗忘样本的输入敏感性（尤其是目标类与无关类 logit 的梯度范数差）可以作为样本贡献的可靠代理。这一假设在标准分类任务上得到了充分验证（Figure 2, Figure 3），但在非分类任务或具有复杂损失景观的模型上的适用性仍需进一步研究。

**调参需求。** MU-Mis 需要为每个遗忘任务单独调整学习率和停止阈值 δ（Algorithm 1），尽管消融实验表明性能对 δ 的变化相对稳定（Figure A2），但这仍带来额外的调参开销。自适应停止准则依赖于无关类 logit 敏感度恢复至预训练初始值的 δ 倍，δ 的合理范围需要根据具体任务经验确定。

### 局限与已知失效模式

**随机子集遗忘的性能退化。** 在最具挑战性的随机子集遗忘场景下，MU-Mis 虽然降低了隐私泄露风险，但与理想的重新训练模型相比效用差距仍然明显。这是当前方法的主要提升方向，也是未来工作的重点。

**高记忆度样本的副作用。** 遗忘高记忆度样本时，MU-Mis 会导致更多的剩余数据性能损失。这表明灵敏度差距并不能完全均一地代理各类样本的贡献——某些样本的贡献可能涉及更复杂的参数交互，仅靠一阶梯度信息难以精确撤回。

**联合优化的必要性。** 消融实验（Table A12）表明，联合优化目标类（TC）和无关类（OC）项是必要的：仅用 TC 会导致遗忘不完全，仅用 OC 会严重损害模型效用。这意味着方法不能简化为单边操作，必须同时监控两个方向的敏感度变化。

**与 Jacobian 正则化的对比。** 通过 Jacobian 正则化强制模型平滑反而会降低遗忘效果（Table A14），表明输入敏感性是比模型平滑性更精准的引导信号。这一发现从侧面说明，简单的平滑约束不足以捕捉样本贡献的精细结构。

### 开放问题与未来方向

1. **一阶与二阶信息的融合。** 能否通过将一阶灵敏度差距与二阶 loss 曲率更直接地关联，以提供更强的理论保证并改进随机子集遗忘？当前方法仅利用一阶梯度信息，而影响力函数等框架表明二阶信息可能提供更精确的样本贡献估计。

2. **样本贡献、记忆度与影响力的关系。** 样本贡献、记忆度与影响力之间的确切关系是什么？反记忆化（通过撤回灵敏度差距）是否足以满足所有遗忘需求，还是某些场景需要更精细的贡献定位机制？

3. **随机子集遗忘的效用保护。** 如何更精细地定位和抑制样本贡献，以在随机子集遗忘场景下同时完美保留模型效用？这可能需要对灵敏度差距信号进行样本级别的加权或分解。

4. **与其他范式的结合。** 能否结合其他新兴无保留数据遗忘范式（如 RUM）与灵敏度抑制来进一步缩小与理论重训模型的差距？混合策略可能在不同遗忘场景下发挥互补优势。

5. **非分类任务的推广。** 当前方法建立在分类任务的目标类/无关类 logit 结构之上。在生成模型、强化学习或自监督学习等任务中，如何定义和操作等价的“灵敏度差距”信号是一个开放的理论问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/Remaining_data_free_Machine_Unlearning_by_Suppressing_Sample_Contribution.pdf]]
