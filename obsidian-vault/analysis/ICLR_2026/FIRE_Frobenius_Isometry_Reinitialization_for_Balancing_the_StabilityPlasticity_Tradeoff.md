---
title: "FIRE: Frobenius-Isometry Reinitialization for Balancing the Stability–Plasticity Tradeoff"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/FIRE_Frobenius_Isometry_Reinitialization_for_Balancing_the_StabilityPlasticity_Tradeoff.pdf
openreview_forum_id: CfZLxT3zIZ
aliases:
- FFIR
- FIRE
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过约束优化将重初始化构造为在最小化权重 Frobenius 距离（SFE）的同时强制权重矩阵正交（DfI=0），从而在保留先前表示能力的前提下恢复权重各向同性，提升对新数据的适应能力。"
primary_logic: "将稳定性-可塑性权衡显式表达为有约束的优化问题，利用 SFE 和 DfI 分别量化两个维度，并通过牛顿-舒尔茨迭代高效求解正交 Procrustes 问题，实现无需手动调参的精确平衡。"
claims:
- "FIRE 将重初始化建模为最小化 SFE 并满足 DfI=0 的约束优化问题，提供了原则性框架。"
- "该方法可通过牛顿-舒尔茨迭代高效实现，仅增加不到 1% 的训练时间。"
- "定理 1 证明 SFE 可控制输出特征协方差差异；定理 2–4 证明 DfI 可同时约束 Hessian 谱范数、特征有效秩和神经元活性，为两个度量提供了可靠的理论保证。"
- "CIFAR-10 (ResNet-18) Warm-start 上 Test Accuracy = FIRE 超越所有基线方法"
---

# FIRE: Frobenius-Isometry Reinitialization for Balancing the Stability–Plasticity Tradeoff

> [!tip] 核心洞察
> 将稳定性-可塑性权衡显式表达为有约束的优化问题，利用 SFE 和 DfI 分别量化两个维度，并通过牛顿-舒尔茨迭代高效求解正交 Procrustes 问题，实现无需手动调参的精确平衡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | FIRE：Frobenius-Isometry 再初始化以平衡稳定性-可塑性权衡 |
| 英文题名 | FIRE: Frobenius-Isometry Reinitialization for Balancing the Stability–Plasticity Tradeoff |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=CfZLxT3zIZ); [Project](https://isaac7778.github.io/fire/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | FIRE (Frobenius-Isometry Reinitialization) |
| Dataset | CIFAR-10 (ResNet-18) Warm-start, Continual Learning (CIFAR-100 ViT-Tiny), Class-incremental (Tiny ImageNet VGG-16), Continual Pretraining of GPT-0.1B (60k checkpoint) |

> [!tip] 效果简介
> - CIFAR-10 (ResNet-18) Warm-start 上，Test Accuracy 为 FIRE 超越所有基线方法，对比 S&P, DASH, Parseval Reg., L2Init, CBP, ReDo, SNR, Muon，变化 性能显著领先。
> - Continual Learning (CIFAR-100 ViT-Tiny) 上，Test Accuracy 为 FIRE 提供一致增益，与最佳替代方案持平，对比 S&P, DASH 等，变化 增量阶段性能下降轻微。
> - Class-incremental (Tiny ImageNet VGG-16) 上，Test Accuracy 为 FIRE 表现稳健，无重置后性能骤降，对比 Full Reset, S&P 等，变化 避免急降。

## 概述

深度神经网络在非平稳数据流中持续训练时，面临**稳定性-可塑性困境**：既要保留从旧数据中学到的知识（稳定性），又要保持对新数据的适应能力（可塑性）。现有重初始化方法通常依赖启发式规则——保守策略无法恢复足够可塑性，激进策略则破坏已学知识——缺乏一个原则性框架来同时优化这两个相互冲突的目标。

**FIRE（Frobenius-Isometry Reinitialization）** 将这一权衡显式建模为约束优化问题：最小化当前权重与先前权重的平方 Frobenius 误差（SFE）以保持稳定性，同时强制权重矩阵正交（DfI=0）以恢复可塑性。该问题的闭式解为正交 Procrustes 问题的极分解，可通过牛顿-舒尔茨迭代高效逼近，仅增加不到 1% 的训练时间。

理论分析为两个度量提供了坚实保证：定理 1 证明 SFE 可控制输出特征协方差差异，定理 2–4 证明降低 DfI 与更平滑的损失景观、更少的休眠神经元和更高的特征有效秩直接相关。实验覆盖持续视觉学习（CIFAR-10/100、Tiny ImageNet）、大语言模型持续预训练（GPT-0.1B）和强化学习（Atari DQN、HumanoidBench SAC），FIRE 在所有场景下均超越或匹配 S&P、DASH、CBP、ReDo 等基线方法，同时保持极低的计算开销（0.06 秒 vs DASH 69 秒）和显存占用（55 MB vs DASH 2834 MB）。

## 背景与动机

深度神经网络在非平稳环境中持续学习时面临一个根本性困境：如何在保留已学知识（稳定性）与适应新数据（可塑性）之间取得平衡。当模型在新数据上继续训练时，权重会逐渐偏离初始分布，出现**可塑性丧失**——模型更新能力下降，难以有效拟合新任务或新数据分布。这一现象在持续学习、增量训练和强化学习等场景中尤为突出，严重制约了模型的长期适应能力。

现有应对可塑性丧失的方法大致可分为三类：**正则化方法**在训练期间持续约束权重，例如 **L2 Init** 通过 L2 惩罚使权重接近初始值，**Parseval Regularization** 约束权重矩阵保持近似正交；**神经元级重置方法**定期重新初始化低贡献或休眠单元，如 **CBP**（Continual Backpropagation）基于效用分数重置单元，**ReDo**（Recycling Dormant neurons）重置激活分数低于阈值的神经元，**SNR**（Self-Normalized Resets）通过统计检验检测活性下降的神经元；**权重级重初始化方法**直接干预整个层的权重矩阵，如 **S&P**（Shrink & Perturb）将权重向初始值收缩并添加噪声，**DASH**（Direction-Aware Shrinking）根据权重与损失梯度的方向相似度选择性收缩权重。

然而，这些方法存在一个共同的核心瓶颈：**缺乏一个原则性的框架来同时优化稳定性和可塑性这两个相互冲突的目标**。保守的重初始化（如轻度收缩）无法恢复足够的可塑性，而激进的重初始化（如完全重置）会破坏已学知识。现有方法或依赖启发式规则，或将两个目标隐式地混入单一操作中，无法精确控制稳定性与可塑性之间的权衡。此外，像 DASH 这样的方法计算开销巨大（需计算梯度方向相似度），难以在实际应用中高效部署。

FIRE 的动机正是填补这一空白：**将稳定性-可塑性权衡显式建模为有约束的优化问题**，用两个独立且可量化的度量——平方 Frobenius 误差（SFE）和等距偏离度（DfI）——分别刻画稳定性和可塑性，并通过高效的正交 Procrustes 求解器实现无需手动调参的精确平衡。这一思路将重初始化从经验性操作提升为有理论保证的优化过程，为持续学习中的权重干预提供了统一而高效的解决方案。

## 核心创新

FIRE 的核心创新在于将稳定性-可塑性权衡从一个启发式调参问题转化为一个**显式的约束优化问题**，并提供高效求解方案。其关键 changed slots 如下：

### 1. 重初始化策略：从启发式规则到约束优化框架

现有重初始化方法依赖启发式规则，缺乏对稳定性与可塑性两个冲突目标的联合建模。例如，**Shrink & Perturb (S&P)** 通过向初始值收缩并添加噪声来缓解可塑性丧失，但收缩因子和噪声强度需要手动调节；**DASH** 根据权重与损失梯度的方向相似度选择性收缩权重，同样缺少对两个维度的统一量化。**CBP**、**ReDo**、**SNR** 等神经元级方法则聚焦于检测并重置低贡献单元，本质上仍是局部启发式策略。

FIRE 将这一问题重新表述为：

$$\operatorname*{min}_{\widetilde{W}} \|W - \widetilde{W}\|_F^2 \quad \mathrm{s.t.} \quad \widetilde{W}^\top \widetilde{W} = I$$

其中目标函数为**平方 Frobenius 误差（SFE）**，量化稳定性——最小化 SFE 意味着尽可能保留先前权重中的知识；约束条件强制权重矩阵正交，即**偏离等距度（DfI）**为零，从而恢复权重的各向同性以提升可塑性。这一框架首次将稳定性-可塑性权衡显式建模为有约束的优化问题，无需手动调参即可实现精确平衡。

理论分析为两个度量提供了坚实保证（Theorem 1–4）：
- **Theorem 1**：SFE 为两个网络输出特征的归一化协方差差异提供上界，最小化 SFE 可单调收紧该上界，从而有效保持特征相似性。
- **Theorem 2–4**：降低 DfI 直接关联于更平滑的损失景观（Hessian 谱范数上界收紧）、更高的特征有效秩（下界提升）和更少的休眠神经元。

### 2. 正交化实现：从极分解到牛顿-舒尔茨迭代

约束优化问题的闭式解为正交 Procrustes 问题的极分解：

$$\widetilde{W}^\star = W (W^\top W)^{-\frac{1}{2}}$$

直接计算极分解涉及矩阵平方根逆，计算开销大。FIRE 采用**牛顿-舒尔茨迭代**进行高效逼近，迭代格式为：

$$X_{k+1} = a X_k + b X_k (X_k^\top X_k) \quad (a=1.5, b=-0.5)$$

该方法仅增加不到 1% 的训练时间（Table 1：FIRE 耗时 0.06 秒 vs DASH 69 秒），且显存占用极低（55 MB vs DASH 2834 MB）。消融实验表明，FIRE 对迭代次数高度鲁棒，仅用 5 次迭代即可获得显著性能提升（Figure 5a），单次迭代后 DfI 已大幅下降（Figure 6）。

### 3. 架构适配：Transformer 中的选择性正交化

与现有正则化方法（如 **Parseval Regularization** 在训练期间持续约束所有权重接近正交）不同，FIRE 在 Vision Transformer 中**仅对 Q、K 投影矩阵执行正交化**，V、O 和 MLP 权重保持不变。这一设计基于注意力机制的结构特性，避免对值投影和输出投影施加不必要的正交约束。

### 4. 缩放模块：维持信号方差

正交化后，FIRE 对权重施加与层维度相关的缩放因子以维持信号方差稳定：线性层使用 $\sqrt{d_{out} / d_{in}}$，卷积层使用 $\sqrt{C_{out} / C_{in}} / (k_h k_w)$。这一设计与 **Muon** 优化器的梯度正交化思路相似，但 FIRE 将其应用于权重重初始化而非梯度更新，且在 Transformer 中的正交化范围选择上有所不同。

### 创新边界与局限

FIRE 的创新集中在**重初始化时刻的约束优化框架**，而非持续训练过程中的正则化。与 **Plasticity Injection**（添加并冻结新预测头）和 **L2 Init**（L2 惩罚使权重接近初始值）等方法相比，FIRE 在重初始化点同时显式优化稳定性和可塑性两个维度，而非仅干预单一维度。

需要注意的是：当前验证限于中等规模模型（ResNet-18、ViT-Tiny、GPT-0.1B），在大规模架构上的效果有待检验；对 Transformer 仅正交化 Q/K 投影的选择尚未系统消融；重初始化时机目前依赖预设触发点，缺乏自适应触发机制。

## 整体框架

FIRE 将稳定性-可塑性权衡显式建模为一个约束优化问题，通过两个互补的度量——SFE 和 DfI——分别量化稳定性和可塑性损失，并在正交 Procrustes 问题的框架下求解最优重初始化权重。整个 pipeline 由四个核心模块串联构成：

1. **稳定性度量 SFE**：计算当前权重 $W$ 与先前权重 $\widetilde{W}$ 之间的平方 Frobenius 误差 $\operatorname{SFE}(W, \widetilde{W}) = \|W - \widetilde{W}\|_F^2$，量化重初始化对已学知识的保留程度。定理 1 证明 SFE 为两个网络输出特征协方差之间的差异提供了上界，因此最小化 SFE 能有效保持特征相似性。

2. **可塑性度量 DfI**：计算权重矩阵偏离正交的程度 $\mathrm{DfI}(W) = \|W^\top W - I\|_F^2$，反映权重的各向同性。定理 2–4 分别证明降低 DfI 与更平滑的损失景观（Hessian 谱范数上界收紧）、更高的特征有效秩以及更少的休眠神经元直接相关，为 DfI 作为可塑性代理指标提供了理论保证。

3. **约束优化求解器（牛顿-舒尔茨迭代）**：将重初始化构造为在 DfI=0 的约束下最小化 SFE 的优化问题：
   $$\min_{\widetilde{W}} \|W - \widetilde{W}\|_F^2 \quad \mathrm{s.t.} \quad \widetilde{W}^\top \widetilde{W} = I$$
   该问题的闭式解为极分解 $\widetilde{W}^\star = W (W^\top W)^{-\frac{1}{2}}$。FIRE 通过牛顿-舒尔茨迭代 $X_{k+1} = a X_k + b X_k (X_k^\top X_k)$ 高效逼近该解，避免直接计算极分解的高昂开销。

4. **缩放模块**：对正交化后的权重施加与层维度相关的缩放因子——线性层使用 $\sqrt{d_{\text{out}} / d_{\text{in}}}$，卷积层使用 $\sqrt{C_{\text{out}} / C_{\text{in}}} / (k_h k_w)$——以维持信号方差在前向传播中的稳定。

**输入输出流**：在触发重初始化的时刻，FIRE 以当前权重 $W$ 为输入，依次经过 DfI 评估、牛顿-舒尔茨正交化迭代、缩放调整，输出重初始化后的权重 $\widetilde{W}$，随后网络在新数据上继续训练。该流程对线性层和卷积层分别处理，在 Vision Transformer 中仅对 Q、K 投影矩阵执行正交化，V、O 及 MLP 权重保持不变。整个流程的计算开销极低——仅增加不到 1% 的训练时间，且显存占用远低于基于梯度的基线方法（如 DASH 需 2834 MB，FIRE 仅需 55 MB）。

## 核心模块与公式推导

FIRE 将稳定性-可塑性权衡显式构造为约束优化问题，其方法管线由三个核心模块构成：稳定性度量 SFE、可塑性度量 DfI，以及基于牛顿-舒尔茨迭代的约束优化求解器。

### 3.1 稳定性度量：平方 Frobenius 误差（SFE）

稳定性被量化为当前权重 $W$ 与先前权重 $\widetilde{W}$ 之间的平方 Frobenius 误差：

$$\operatorname{SFE}(W, \widetilde{W}) = \|W - \widetilde{W}\|_F^2$$

该度量计算所有权重元素上的平方偏差之和。定理 1 证明 SFE 为两个不同网络输出特征的归一化协方差差异提供了上界，且最小化 SFE 可单调收紧该上界，因此 SFE 是保持两个网络特征相似性的有效手段。这一理论保证使 SFE 成为重初始化过程中衡量知识保留程度的可靠指标。

### 3.2 可塑性度量：等距偏离度（DfI）

可塑性损失通过等距偏离度（Deviation from Isometry, DfI）来量化，该度量衡量权重矩阵偏离正交的程度：

$$\mathrm{DfI}(W) = \|W^\top W - I\|_F^2$$

DfI 与先前可塑性度量紧密关联，且具备可优化性。理论分析揭示了三个关键性质：

- **定理 2**：DfI 可约束 Hessian 谱范数。具体地，设 $\nu_k = 1 + \sqrt{\mathrm{DfI}(W_k)}$，则损失函数 Hessian 的谱范数上界由各层 DfI 值的乘积形式给出，降低 DfI 可平滑损失景观曲率。
- **定理 3**：DfI 可约束特征矩阵的有效秩下界，降低 DfI 有助于提高表征的有效秩。
- **定理 4**：降低 DfI 与减少休眠神经元数量直接相关。

这三个定理共同表明，DfI 是一个在理论上可靠的可塑性代理度量。

### 3.3 约束优化形式与闭式解

FIRE 将重初始化建模为在满足正交约束的前提下最小化 SFE 的问题：

$$\min_{\widetilde{W}} \|W - \widetilde{W}\|_F^2 \quad \mathrm{s.t.} \quad \widetilde{W}^\top \widetilde{W} = I$$

该问题等价于正交 Procrustes 问题，其闭式解通过极分解给出：

$$\widetilde{W}^\star = W (W^\top W)^{-\frac{1}{2}}$$

该解在保持与原权重最小 Frobenius 距离（即最大化稳定性）的同时，强制权重矩阵正交（即 $\mathrm{DfI}=0$，最大化可塑性），从而在重初始化时实现稳定性和可塑性的原则性平衡。

### 3.4 高效实现：牛顿-舒尔茨迭代

直接计算极分解 $(W^\top W)^{-1/2}$ 计算开销较大。FIRE 采用牛顿-舒尔茨迭代来高效逼近该解，迭代格式为：

$$X_{k+1} = a X_k + b X_k (X_k^\top X_k) + c X_k (X_k^\top X_k)^2$$

其中标准系数为 $(a, b, c) = (2, -1.5, 0.5)$，等价于：

$$X_{k+1} = 2 X_k - 1.5 X_k (X_k^\top X_k) + 0.5 X_k (X_k^\top X_k)^2$$

该迭代收敛于 $W (W^\top W)^{-1/2}$，即正交 Procrustes 问题的解。消融实验表明，FIRE 对迭代次数高度鲁棒，仅用 5 次迭代即可获得显著的性能提升，且单次迭代后 DfI 已大幅下降，后续迭代仅进行精细调整。

### 3.5 缩放模块

为在正交化后维持信号方差稳定，FIRE 对不同层类型设计了维度相关的缩放因子：

- **线性层**：$\mathrm{scale} = \sqrt{d_{\text{out}} / d_{\text{in}}}$
- **卷积层**：$\mathrm{scale} = \sqrt{C_{\text{out}} / C_{\text{in}}} / (k_h k_w)$，其中正交化沿空间维度逐核执行

### 3.6 Transformer 架构的适配

在 Vision Transformer 中，FIRE 仅对查询（Q）和键（K）投影矩阵执行正交化，值（V）、输出（O）投影及 MLP 权重保持不变。该设计选择基于 Transformer 中注意力机制对权重各向同性的敏感性差异，但论文未系统探索其他组件正交化的影响。

### 3.7 计算开销

FIRE 的计算开销极低。在对比实验中，FIRE 的墙钟时间仅约 0.06 秒，GPU 显存占用约 55 MB，而 DASH 方法需 69 秒和 2834 MB。整体上，FIRE 增加的训练时间不到 1%，在保持高效的同时实现了稳定性和可塑性的精确平衡。

## 实验与分析

### 主实验结果

FIRE 在持续视觉学习、持续语言模型预训练和强化学习三大类任务上进行了评估，均展现出相对于既有重初始化方法的显著优势。

**持续视觉学习。** 实验覆盖三种典型场景：热身启动（Warm-start，仅用 10% 数据预训练后切换全量数据）、增量数据（Continual，数据分 10 阶段逐步释放）和类增量（Class-incremental，分 20 阶段引入新类别）。

- 在 CIFAR-10 + ResNet-18 的热身启动设置中，FIRE 超越所有基线方法，包括 S&P、DASH、Parseval 正则化、L2Init、CBP、ReDo、SNR 和 Muon（Figure 2a）。这表明 FIRE 在数据分布突变时能快速恢复可塑性而不牺牲已学表示。
- 在 CIFAR-100 + ViT-Tiny 的增量数据设置中，FIRE 在每个数据扩展阶段仅产生轻微或可忽略的性能下降，而其他方法在重置后常出现大幅波动（Figure 2b）。FIRE 通过强制权重正交化（DfI=0）维持了损失景观的平滑性，使优化器在新数据上能高效收敛。
- 在 Tiny ImageNet + VGG-16 的类增量设置中，FIRE 避免了完全重置（Full Reset）或 S&P 等方法常见的重置后性能骤降问题，在整个学习过程中保持稳健（Figure 2c）。这验证了 SFE 约束在保留旧类别判别能力方面的有效性。

**持续语言模型预训练。** 在 GPT-0.1B 的持续预训练实验中，模型先在 WikiText-103 上预训练，再在 OpenWebText 与 WikiText-103 混合数据集上继续训练。当从 60k 预训练迭代的检查点初始化时，模型已出现显著的可塑性丧失。FIRE 在此条件下仍能保持较低的验证损失，优于 S&P 和完全重置（Figure 3 right）。值得注意的是，FIRE 的验证损失曲线在重置后迅速下降，表明正交化权重为优化器提供了良好的梯度传播条件。

**强化学习。** 在 Atari DQN（Asterix、BeamRider、DemonAttack）和 HumanoidBench SAC（Balance、Walk、Run）任务上，FIRE 在训练中点施加单次重初始化。在 Asterix 环境中，FIRE 显著超越 S&P 和 Plasticity Injection；在其余任务上达到竞争或更优性能（Figure 4）。这证明 FIRE 在非平稳奖励分布下的价值函数逼近中同样有效。

### 消融实验

消融实验从三个维度验证了 FIRE 的设计选择。

**牛顿-舒尔茨迭代次数的鲁棒性。** FIRE 对迭代次数高度鲁棒：仅用 5 次迭代即可获得显著的性能增益，继续增加迭代次数带来的提升趋于饱和（Figure 5a）。这与理论预期一致——单次迭代后 DfI 已大幅下降，后续迭代主要进行精细调整（Figure 6 right）。这一特性使得 FIRE 在计算开销极低的前提下即可接近最优正交解。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_CfZLxT3zIZ/figures/005_Figure_5.jpg]]
*Figure 5: Ablation study results. Final performance of FIRE with varying numbers of iterations for Netwon-Schulz algorithm (a). Comparison of FIRE and baselines in terms of loss curvature (maximum eigenvalue of the Hessian), plasticity (DfI), and stability (normalized SFE) (b)*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_CfZLxT3zIZ/figures/007_Figure_6.jpg]]
*Figure 6: Effect of number of FIRE iterations. Test accuracy of FIRE with single iteration and 10 iterations (left). Change of SFE during FIRE iterations (middle). Change of DfI during FIRE iterations (right)*

**稳定性-可塑性权衡的实际平衡。** 在损失曲率（Hessian 最大特征值）、可塑性（DfI）和稳定性（归一化 SFE）三个指标上，FIRE 同时实现了最低的 DfI 和最低的 SFE（Figure 5b）。相比之下，S&P 虽然保持了较低的 SFE，但 DfI 较高，导致可塑性恢复不足；完全重置虽然 DfI 较低，但 SFE 极高，破坏了已学知识。FIRE 是唯一在帕累托前沿上同时优化两个目标的方法。

**计算效率。** 在 CIFAR-10 + ResNet-18 的设置下，FIRE 的挂钟时间为 0.06 秒，显存占用仅 55 MB；而 DASH 需要 69 秒和 2834 MB（Table 1）。FIRE 的计算开销不到总训练时间的 1%，这得益于牛顿-舒尔茨迭代仅涉及矩阵乘法，无需计算梯度或存储中间激活。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_CfZLxT3zIZ/figures/006_Table_1.jpg]]
*Table 1: Wall-Clock Time and GPU memory footprint of FIRE and baseline methods*

### 失败模式与局限性

尽管 FIRE 在多个基准上表现优异，但存在以下已知局限：

1. **历史数据依赖。** 当前实验假设在新数据到达时可访问所有历史数据以计算 SFE 参考权重。在严格的无重放（rehearsal-free）或隐私受限的持续学习场景中，如何选择参考权重仍需进一步研究。
2. **模型规模验证不足。** 目前仅在中等规模模型（ResNet-18、ViT-Tiny、GPT-0.1B）上验证，尚未在数十亿参数级别的大语言模型或其他大规模架构上测试。FIRE 的正交化操作在超大矩阵上的数值稳定性有待检验。
3. **Transformer 正交化范围有限。** 对 ViT 仅正交化 Q、K 投影矩阵，V、O 和 MLP 权重保持不变。未系统探索对其他组件正交化的影响，也未在更多样化的 Transformer 变体（如 Swin、DeiT）上实验。
4. **重初始化时机固定。** 强化学习实验中仅在训练中点应用单次重初始化，未研究多次干预或基于在线指标的自适应触发策略。

### 重要图表结论

- **Figure 5b** 是理解 FIRE 核心优势的关键：它直观展示了 FIRE 在 DfI-SFE 权衡空间中位于帕累托最优位置，而所有基线方法均在不同程度上牺牲了其中一个维度。
- **Table 1** 揭示了 FIRE 的实用价值：在保持理论优雅性的同时，其计算开销几乎可忽略，这使得 FIRE 可以无缝集成到现有训练流程中，无需调整优化器或学习率调度。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_CfZLxT3zIZ/figures/008_Figure_7.jpg]]
*Figure 7: Effect of Newton Schulz iteration coefficients on FIRE. FIRE and FIRE with Muon’s coefficients are evaluated on warm-start setting under CIFAR-10 with ResNet-18 (left), CIFAR-100 with ViT-Tiny (middle), and Tiny ImageNet with VGG-16 (right)*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_CfZLxT3zIZ/figures/010_Table_2.jpg]]
*Table 2: Detailed settings in continual visual learning*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_CfZLxT3zIZ/figures/011_Table_3.jpg]]
*Table 3: Detailed settings in continual pretraining of LLMs*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_CfZLxT3zIZ/figures/012_Table_4.jpg]]
*Table 4: Hyperparameters used in the ALE environment with DQN algorithm*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_CfZLxT3zIZ/figures/013_Table_5.jpg]]
*Table 5: Hyperparameters used in HumanoidBench environments with SimBa*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_CfZLxT3zIZ/figures/014_Table_6.jpg]]
*Table 6: Hyperparameter search space for all experiments*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_CfZLxT3zIZ/figures/015_Table_7.jpg]]
*Table 7: Hyperparameters for Warm-Start setting*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_CfZLxT3zIZ/figures/016_Table_8.jpg]]
*Table 8: Hyperparameters for Continual Setting*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_CfZLxT3zIZ/figures/017_Table_9.jpg]]
*Table 9: Hyperparameters for Class-Incremental Setting*

## 方法谱系与知识库定位

### 稳定性-可塑性权衡的重初始化方法谱系

持续学习中应对可塑性丧失的方法可分为三条主线：**基于正则化的方法**在训练过程中持续约束权重，使其不偏离初始状态过远；**神经元级重置方法**选择性重新初始化低贡献单元；**权重级重初始化方法**则周期性地对网络参数进行干预。FIRE 属于第三条主线，但其核心创新在于首次将重初始化构造为一个**有约束的显式优化问题**，而非依赖启发式规则。

**基于正则化的方法**通过持续施加约束来维持可塑性。**Parseval Regularization** 在训练期间约束权重矩阵接近正交，**L2 Init** 则通过 L2 惩罚使权重保持在初始值附近。这些方法无需显式的重初始化步骤，但其约束强度需要手动调参，且无法在训练过程中根据可塑性丧失程度动态调整。FIRE 与这类方法的本质区别在于：它通过一次性的约束优化求解实现精确的权重调整，而非在整个训练过程中施加持续但粗糙的约束。

**神经元级重置方法**以 **Continual Backpropagation (CBP)**、**ReDo**（Recycling Dormant neurons）和 **Self-Normalized Resets (SNR)** 为代表。CBP 基于效用分数识别并重置低贡献单元，ReDo 定期重置激活分数低于阈值的休眠神经元，SNR 则通过统计检验检测活性显著下降的神经元。这类方法的粒度更细，但面临两个关键局限：一是需要维护额外的效用统计量，二是选择性重置可能破坏网络内部已建立的协同表示。FIRE 在权重级别操作，通过全局约束优化统一处理所有参数，避免了神经元选择策略的复杂性。

**权重级重初始化方法**中，**Shrink & Perturb (S&P)** 是最常用的基线，它将权重向初始值收缩并添加噪声。**DASH**（Direction-Aware SHrinking）进一步根据权重与损失梯度的方向相似度进行选择性收缩。然而，这些方法的收缩系数和噪声强度需要手动调节，缺乏对稳定性-可塑性权衡的显式建模。FIRE 通过 SFE 和 DfI 两个度量将这一权衡形式化为可解的优化问题，消除了手动调参的需求。

### FIRE 的核心机制定位

FIRE 的方法论贡献体现在三个层面：

**第一，问题形式化的突破。** FIRE 将重初始化建模为最小化 SFE（稳定性度量）且满足 DfI=0（可塑性度量）的约束优化问题，即：

$$\operatorname*{min}_{\widetilde{W}} \|W - \widetilde{W}\|_F^2 \quad \mathrm{s.t.} \quad \widetilde{W}^\top \widetilde{W} = I$$

该问题的闭式解为极分解 $\widetilde{W}^\star = W (W^\top W)^{-\frac{1}{2}}$，本质上是寻找与原始权重最接近的正交矩阵。这一形式化使稳定性-可塑性权衡从经验性调参提升为原则性优化。

**第二，理论保证的完备性。** 论文为两个核心度量提供了严格的理论支撑：定理 1 证明 SFE 可控制输出特征协方差差异，为稳定性度量提供了可靠上界；定理 2–4 分别证明 DfI 可约束 Hessian 谱范数（损失景观平滑度）、特征有效秩和神经元活性，为可塑性度量建立了与网络训练动力学的直接联系。这种双度量理论框架在现有重初始化方法中尚无先例。

**第三，计算效率的工程突破。** 与直接计算极分解的高昂开销不同，FIRE 采用牛顿-舒尔茨迭代进行高效逼近：

$$X_{k+1} = a X_k + b X_k (X_k^\top X_k)$$

其中标准系数为 $a=1.5$，$b=-0.5$。实验表明，FIRE 的计算时间仅为 0.06 秒（对比 DASH 的 69 秒），显存占用仅 55 MB（对比 DASH 的 2834 MB），增加不到 1% 的训练时间。这一效率优势使其在实际部署中具有显著竞争力。

**第四，架构适配的精细设计。** 在 Vision Transformer 中，FIRE 仅对 Q、K 投影矩阵执行正交化，V、O 和 MLP 权重保持不变。对线性层和卷积层分别设计了与维度相关的缩放因子，以维持信号方差稳定。这种分组件处理策略避免了盲目正交化可能引入的表示破坏。

### 与邻近方法的交叉与区别

**与 Muon 优化器的关系：** Muon 使用牛顿-舒尔茨迭代将梯度更新矩阵正交化，FIRE 在实现层面与之共享迭代算法，但两者的应用场景和优化目标截然不同。Muon 在每次优化步骤中对梯度进行正交化以改善训练动态，而 FIRE 在特定时机对权重本身进行一次性正交化以恢复可塑性。FIRE 的牛顿-舒尔茨迭代系数（$a=1.5$，$b=-0.5$）与 Muon 的系数选择不同，消融实验表明 FIRE 的系数设置在持续学习场景下更为有效。

**与 Plasticity Injection 的关系：** Plasticity Injection 通过添加并冻结新的预测头，利用可学习的副本恢复网络可塑性。FIRE 则直接修改骨干网络权重，不引入额外参数，在架构侵入性上更小。

### 适用边界与局限

FIRE 的适用性受以下边界条件约束：

1. **数据可访问性假设：** 实验设置假设在新数据到达时可访问所有历史数据，用于计算重初始化后的训练起点。在严格的无重放（rehearsal-free）或隐私受限的持续学习场景中，这一假设可能不成立。论文未验证 FIRE 在仅能访问当前数据批次的条件下的表现。

2. **模型规模验证不足：** 当前实验仅在中等规模模型上验证（ResNet-18、ViT-Tiny、GPT-0.1B），尚未在数十亿参数级别的大语言模型或其他大规模架构上测试。FIRE 的计算效率优势在更大规模模型上是否能保持，需要进一步验证。

3. **架构覆盖范围有限：** 对 Transformer 架构仅探索了 Q/K 投影的正交化，未系统研究 V、O 及 MLP 层正交化的效果，也未在更多样化的 Transformer 变体（如仅解码器架构的现代 LLM）上实验。

4. **干预策略单一：** 在强化学习实验中仅在训练中点应用单次重初始化，未研究多次干预或自适应触发策略。在实际部署中，可塑性丧失的程度和时机可能因任务而异，固定时机的单次干预可能不是最优选择。

### 开放问题

1. **无重放场景下的有效性：** 在限制访问过去数据的条件下，FIRE 是否仍能有效平衡稳定性和可塑性？这需要重新设计 SFE 的计算方式，或寻找可替代的稳定性度量。

2. **大规模模型的扩展性：** FIRE 能否扩展到数十亿参数的 LLM 并保持其计算开销优势？极分解的近似精度在大规模矩阵上是否会退化？

3. **与经典持续学习技术的结合：** 如何将 FIRE 与经验重放、弹性权重巩固（EWC）等经典持续学习技术结合？FIRE 的正交化操作可能与 EWC 的重要性加权产生交互效应，需要系统研究。

4. **自适应触发机制：** 能否在训练过程中在线自适应地决定重初始化的触发时机和强度？DfI 本身可作为可塑性丧失的监测指标，为自适应策略提供了自然基础。

## 原文 PDF

![[paperPDFs/ICLR_2026/FIRE_Frobenius_Isometry_Reinitialization_for_Balancing_the_StabilityPlasticity_Tradeoff.pdf]]
