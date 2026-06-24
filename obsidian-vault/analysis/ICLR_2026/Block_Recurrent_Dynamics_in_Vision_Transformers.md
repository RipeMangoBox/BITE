---
title: "Block Recurrent Dynamics in Vision Transformers"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Block_Recurrent_Dynamics_in_Vision_Transformers.pdf
aliases:
- RRAPST
- BRDVT
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/interpretability_and_visualization
core_operator: "通过层间权重绑定（参数共享）和基于最大化层间相似度的阶段划分（max-cut算法），显式地引入块递归结构，并用自回归轨迹匹配训练来诱导功能上的相位对齐。"
primary_logic: "训练后的ViT深度轴隐含一个紧凑的递归程序：少量参数绑定的块被重复应用，即可等价（或近似）地重现原始多层的内部表示轨迹，且该结构受随机深度等正则化增强，揭示了ViT的低算法复杂度本质和收敛到低维吸引子的动力学特性。"
claims:
- "在DINOv2 ViT‑B上，仅2个循环块（Raptor k=2）能在ImageNet‑1k线性探针上恢复96%的准确率，k=3恢复98%，且块内层互换保持精度而块间互换导致崩溃，证明了功能上的块循环复用。"
- "随机深度（Stochastic Depth）训练增强层间表示相似度和Raptor重构保真度，且过拟合时块结构和重构质量同步退化，表明该递归结构是训练中涌现的规范化属性。"
- "最大割算法划分的阶段优于随机分区，且与动力学分析中的相位边界吻合；动力学测度（方向收敛、令牌特异的角速度、低秩更新）进一步验证了深度上的功能阶段化。"
- "ImageNet‑1k 上 Top‑1 Accuracy (%) = Raptor k=3: 83.0±0.1"
---

# Block Recurrent Dynamics in Vision Transformers

> [!tip] 核心洞察
> 训练后的ViT深度轴隐含一个紧凑的递归程序：少量参数绑定的块被重复应用，即可等价（或近似）地重现原始多层的内部表示轨迹，且该结构受随机深度等正则化增强，揭示了ViT的低算法复杂度本质和收敛到低维吸引子的动力学特性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 视觉Transformer中的块递归动态 |
| 英文题名 | Block Recurrent Dynamics in Vision Transformers |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=gH3HhnfWLC); [Project](https://kempnerinstitute.github.io/raptor) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/interpretability_and_visualization |
| Method | Raptor (Recurrent Approximations to Phase‑structured TransfORmers) |
| Dataset | ImageNet‑1k, ADE20k, NYUv2 |

> [!tip] 效果简介
> - ImageNet‑1k 上，Top‑1 Accuracy (%) 为 Raptor k=3: 83.0±0.1，对比 DINOv2 ViT‑B: 84.5 / ViT‑S: 80.9，变化 相对于ViT‑B −1.5，相对于ViT‑S +2.1。
> - ADE20k 上，mIoU (%) 为 Raptor k=3: 43.0±0.3，对比 DINOv2 ViT‑B: 47.5 / ViT‑S: 44.6，变化 相对于ViT‑B −4.5。
> - NYUv2 上，RMSE (↓) 为 Raptor k=3: 0.618±0.006，对比 DINOv2 ViT‑B: 0.578 / ViT‑S: 0.600，变化 相对于ViT‑B +0.04。

## 概述

标准 Vision Transformer (ViT) 在深度方向上逐层使用独立参数，并未显式利用层间计算的可重用性。然而，实际训练好的 ViT 内部许多相邻层执行高度相似的运算，形成隐式的**块递归结构**——这一结构被标准训练方式掩盖，导致参数冗余和可解释性缺失。本文将该现象形式化为**块递归假说（Block-Recurrent Hypothesis, BRH）**：存在一组数量远少于总层数的参数绑定 Transformer 块，通过沿深度重复应用，能以极小误差逼近原模型完整的内部表示轨迹。

为将假说转化为可操作的模型，作者提出 **Raptor**（Recurrent Approximations to Phase‑structured TransfORmers）。Raptor 首先利用层间表示相似度矩阵执行最大割（max‑cut）算法，将模型深度自动划分为连续的功能阶段；随后在每个阶段内所有层共享同一组参数（权重绑定），并引入深度缩放机制以构建非自主动力学系统。训练采用两阶段自回归轨迹匹配：第一阶段以退火教师强制（teacher forcing）预训练各块，第二阶段进行全模型自回归端到端训练，同时约束所有中间层激活与教师模型对齐。

关键实证证据证实了 BRH 的有效性：
- 在 **DINOv2 ViT‑B** 上，仅 **2 个循环块**（Raptor k=2）即可通过线性探针恢复 ImageNet‑1k 上 **96%** 的教师准确率，k=3 恢复 **98%**（Table 2）。因果干预实验进一步表明，块**内部**的层互换几乎不影响精度，而**跨块**互换则导致模型崩溃（Figure 15），直接证明了功能上的阶段化循环复用。
- 随机深度（Stochastic Depth）训练强度提升会增强层间表示相似度与 Raptor 重构保真度（Figure 4），而过拟合时块结构同步退化（Figure 13），说明递归结构是训练中涌现的规范化属性。

在完整性能基准上，Raptor k=3 在 ImageNet‑1k 达到 **83.0%** 的线性探针准确率（对比教师 ViT‑B 84.5%，ViT‑S 80.9%），ADE20k 语义分割 mIoU **43.0**，NYUv2 深度估计 RMSE **0.618**（Table 2）。与教师模型存在微小但持续的差距，尤其在密集预测任务上，但模型参数总量大幅压缩，揭示了 ViT 的低算法复杂度本质。此外，作者提出的动力学可解释性程序（方向收敛、角速度、低秩更新、令牌相干性等测度）表明，ViT 深度轴对应离散时间动力学系统，其表示轨迹收敛到与类别相关的低维角度吸引子（Figure 6‑9）。这些发现为理解视觉 Transformer 的内部工作机制和设计更高效架构提供了新视角。

## 背景与动机

Vision Transformer (ViT) 已在各类视觉任务中取得卓越性能，但其标准架构将每一层视为独立参数化的变换，导致随着深度增加参数总量线性膨胀。这种设计假设各层需要不同的函数来逐步精炼表示，然而大量经验证据表明，实际训练后的 ViT 中许多层执行高度相似的计算，形成了一种隐含的**块递归结构**。例如，对多种 ViT 的层间表示余弦相似度矩阵进行可视化（Figure 1），可以清晰看到沿深度轴连续出现的高相似度块状区域，暗示存在功能上可重用的计算阶段。遗憾的是，标准的独立层训练范式掩盖了这一属性，使得网络内部存在大量计算冗余，且深度轴上的动态行为难以解释。

针对上述问题，本文的核心动机源于一个关键观察：**若将 ViT 的深度维度视为离散时间步，其表示更新可能对应一个低复杂度的动力系统，而不仅仅是逐层独立映射的堆叠**。为此，作者提出**块递归假设 (Block‑Recurrent Hypothesis, BRH)**：给定一个预训练的 L 层 ViT，存在一个小整数 k ≪ L，以及 k 个连续参数绑定块 B₁,…,Bₖ，使得对于任意输入，原网络所有中间层的激活都可以被这 k 个块按固定顺序重复执行所近似（见 Definition 1）。换言之，ViT 的内部表示轨迹可被压缩为一个紧凑的递归程序，而不需要为每一层独立存储参数。

现有方法尚未系统利用这一可重用性，导致模型在参数效率与解释性方面存在缺口：一方面，ViT 的参数量随深度线性增长，但许多参数可能执行冗余运算；另一方面，我们缺乏工具去理解深层的计算是如何逐步构建最终表示的，以及为什么深度上的相位变化会自然涌现。本文的动机正是通过**显式引入块递归结构**来填补这些缺口。具体地，作者提出 Raptor (Recurrent Approximations to Phase‑structured TransfORmers) 方法：先利用最大化层间余弦相似度的最大割算法自动划分连续块边界，再对每个块内的所有层进行参数绑定，并通过深度缩放机制使循环块变为非自主动力系统。通过自回归轨迹匹配训练（监督所有中间层而非仅最后一层），强制学生模型在深度轴上保持与教师模型一致的功能相位对齐。

进一步分析表明，这种块递归结构并非偶然，而是训练过程中**涌现的规范化属性**。例如，随机深度训练能够显著增强层间表示相似度，并同步提升 Raptor 的重构保真度和下游精度（Figure 4）；当模型发生过拟合时，块结构和重构质量会同步退化（Figure 13）。这揭示出 ViT 在训练中自然收敛至低维吸引子的动力学特性，从而为后续的动态解释性框架（将深度视为离散时间动力学，分析方向收敛、角速度、低秩更新等）提供了实验基础。

综上所述，本文的动机在于：不仅验证并利用 ViT 隐含的块递归结构以构建参数高效、性能接近原模型的循环代理（Raptor），更旨在建立一套**动态解释学**方法论，将深度轴上的计算理解为受少量块参数驱动的递归动力系统，从而深刻揭示当代视觉 Transformer 的算法复杂性本质。

## 核心创新

标准Vision Transformer (ViT) 将深度建模为独立参数层的逐次堆叠，未显式利用层间计算的可重用性，导致参数膨胀与计算冗余。本文的核心创新在于提出并验证**块递归假设 (Block‑Recurrent Hypothesis, BRH)**：深度轴上的隐式递归结构可通过少量参数绑定的块循环执行来高保真地复现原始表示轨迹，从而将ViT重新解释为**紧凑的循环程序**。围绕该假设，Raptor框架在架构与训练两个维度实现关键变更，以下基于 changed slots 展开分析。

### 架构变更：从逐层独立参数到层间参数绑定与相位发现
**基线 (DINOv2 ViT‑B)** 采用12层独立Transformer块，每层拥有独立权重，深度仅由层索引区分。  
**Raptor 方案** 将深度划分为 *k*≪*L* 个连续块（相位），块内所有层**共享同一组参数**（参数绑定），并通过**深度缩放 (depth‑scaling)** 调制每一层的残差连接（注意力、MLP），使循环块成为一个**非自主动力学系统**。相位边界由**最大割算法 (max‑cut)** 基于层间表示余弦相似度矩阵自动确定，从而最大化块内功能相似度、最小化跨块相似度。这一设计直接响应了因果发现：  
- 因果干预实验（Figure 15）显示，**块内层互换精度几乎无损，而块间互换导致模型崩溃**，证实了块内功能等价性；  
- max‑cut分区在CIFAR‑100上显著优于随机分区（Figure 3），且与后续动力学分析中的相位边界一致（Figure 6‑9）。  

因此，该变更的因果机制为：**通过消除参数冗余并注入结构化的深度先验，将原本异质的层序列压缩为功能上可复用的回路，使网络降阶为低Levin复杂度的递归系统**（Claim 2, Appendix E）。

### 训练目标变更：从终点蒸馏到全轨迹自回归匹配
**基线方法** 多依赖最终输出蒸馏或仅监督分类logits，无法保证中间层表示的保真度。  
**Raptor 训练** 引入**自回归轨迹匹配损失**（$\mathcal{L}_h^{\mathrm{AR}}$），同时监督所有中间层表示，最小化预测激活与教师激活的Frobenius范数之和（Eq. 2）。训练采用**两阶段策略**：  
1. 阶段一：**退火教师强制 (Annealed Teacher Forcing)**，逐步从教师强制（暴露偏差大、易发散）过渡到自回归生成，以平衡稳定性与自洽性；  
2. 阶段二：**全链路自回归端到端训练**，消除第一阶段块间不连续性。  

该设计直面纯Teacher Forcing的灾难性失效（Table 1：仅Teacher Forcing时ImageNet‑1k精度仅3.9%），而引入自回归训练后跃升至72.7%，完整流程达到83.0%，恢复DINOv2 ViT‑B性能的98%（k=3）。其关键机制在于：  
- 轨迹匹配**强约束隐藏状态动态**，迫使循环块学会在深度轴上复现教师的注意力模式与表示演进；  
- 退火λ使得模型逐步内化外部监督，避免自回归训练初期的误差积累。  

### 支持创新的机制性证据
- **随机深度 (Stochastic Depth) 的作用**：随机深度作为训练正则化，系统性提升层间相似度，并增强Raptor的重构保真度（R²）；过拟合时块结构退化，说明该递归结构是**训练中涌现的规范化属性**（Figure 4, Figure 13）。  
- **动力学解释性框架**：将深度轴视为离散时间系统，揭示出方向收敛至类依赖的角度吸引子、令牌特异的角速度突变（与相位边界对齐）、后期低秩更新等动力学特征，为块递归提供了**独立于表示相似度的功能验证**（Figure 6‑9）。  

综上，Raptor的核心创新并非简单的循环连接，而是通过**架构层面强制相位内参共用、训练层面全轨迹自洽约束**，将ViT从“深层串行计算”的物理视图转变为“浅层循环展开”的算法视图，从而同时获得参数效率、解释性与程序复杂度压缩。剩余精度差距（密集预测任务上‑4.5 mIoU）与训练复杂度的优化，是该创新当前的主要边界与后续工作方向。

## 整体框架

![[assets/figures/papers/iclr26_0013_gH3HhnfWLC_Block_Recurrent_Dynamics_in_Vision_Transformers/figures/027_Figure_10.jpg]]
*Figure 10: Three training paradigms for learning recurrent approximations. Each panel shows three token trajectories through depth. Gray dashed lines with filled circles represent the ground-truth teacher trajectories; black solid lines with filled circles show the student’s predictions; colored dotted lines (with ε labels) indicate the error signal between predicted and ground-truth states. Left (Distillation): The student network directly predicts the final layer from the initial state, with no supervision on intermediate representations. Error is measured only at the terminal state, providing no guidance on the representational trajectory. Middle (Teacher Forcing): At each depth step ℓ, the student...*

**核心问题与解决路径。** 标准 Vision Transformer 的逐层独立参数化造成了深度轴上的计算冗余：许多层执行高度相似的变换，形成了隐式的块状结构，却未在训练中被显式利用。Raptor 将这一观察操作化为**块递归蒸馏**管道：通过参数绑定和轨迹匹配，将预训练 ViT 的深度轴压缩成少量循环块的重复应用，同时保持中间表示的高保真度。

**管道概览**（图10、图11及附录A提供训练回路；表3给出具体的层划分）。
1. **教师表示与初始嵌入** – 复用预训练 DINOv2 ViT‑B 作为教师，其 patch embedding 和最终 LayerNorm 被冻结继承，提供输入 token 序列 $a_0(x)$ 和所有层的目标激活 $\{a_\ell(x)\}_{\ell=1}^L$。
2. **阶段发现（Max‑Cut 分区）** – 在教师模型的层‑层余弦相似度矩阵上运行最大割算法，将 $L$ 层划分成 $k$ 个连续块，最大化块内相似度并最小化块间相似度（Figure 2）。该分区与随后动力学分析中的相位边界高度吻合（Figure 6‑9），且显著优于随机分区（Figure 3）。
3. **参数绑定的循环块** – 每个块内所有层共享同一个 Transformer 块参数（包括多头注意力、MLP 及残差连接，见 Eq.1）。为使同一结构在不同层索引下表现出不同行为，引入**深度缩放（Depth‑Scaling）机制**：一个轻量 MLP 将层标量 $z$ 映射为缩放向量 $\mathbf{S}$，用于调制注意力残差、MLP 残差和块输出（附录 A.3），使循环块成为非自治动力学系统。
4. **两阶段轨迹蒸馏训练** – 目标函数组合 Teacher Forcing（TF）损失和自回归（AR）损失：
   $$\mathcal{L}_{\text{total}}(x) = \lambda \mathcal{L}_{\text{TF}}(x) + (1-\lambda) \mathcal{L}_{\text{AR},H}(x) + \Omega(\theta)$$
   其中自回归损失逐层累积教师激活与循环块预测激活的 Frobenius 范数（Eq.2），强制轨迹保真。第一阶段 $\lambda$ 从 1 退火至 0，先通过 TF 稳定训练，再过渡到完全自回归；第二阶段将所有块串联，端到端自回归微调全模型（Table 1 消融证实两阶段训练的不可或缺性）。
5. **评估协议** – 冻结训练好的 Raptor 骨干，仅在特征上训练线性探针进行分类（ImageNet‑1k）、语义分割（ADE20k）或深度估计（NYUv2），以隔离表示质量。

**关键干预证据。** 因果层交换实验（Figure 15）为功能块递归提供了强证：在同一个块内交换任意 1–3 层，分类精度几乎无损；跨块交换则导致模型崩溃。这表明块内各层计算在功能上可互换，而块间计算具有不可替代的阶段特异性。同时，训练消融（Table 1）表明，纯 Teacher Forcing 仅得 3.9% 准确率，加入自回归训练后跃升 68.8%；再叠加深度缩放、加权 cls 和第二阶段训练，最终达到 83.0% 的完整 Raptor 精度。

**架构优势与局限。** 参数绑定使 Raptor 的描述复杂度仅由 $k$ 个块的参数主导（Levin 复杂度界，附录 E），但两阶段训练仍较复杂，且微小但持续的精度差距（尤其在 ADE20k 等密集任务上）提示进一步优化的空间。

## 核心模块与公式推导

**Raptor** 的核心思想是将预训练 ViT 的层间相似结构显式化为参数绑定的循环块，并通过两阶段轨迹匹配训练来重建层激活序列。以下给出方法的关键公式及其变量含义，直接源自论文中的定义，不进行额外推导或猜测。

### 块递归假设 (BRH)
块递归假设为整个工作提供了形式化基础，声称原始 ViT 的深度计算可被极少数的循环块近似替代。

$$
\mathbb{E}_{\mathbf{x}\sim\mathbb{P}}\big( \|\mathbf{f}_\ell(\mathbf{x}) - (\mathbf{B}_k^{(n_k)}\circ\cdots\circ\mathbf{B}_1^{(n_1)})(\mathbf{x})\|_F \big) \leq \varepsilon
$$

- $\mathbf{f}_\ell$：原始 ViT 的第 $\ell$ 层变换。
- $\mathbf{B}_j$：第 $j$ 个参数绑定块的变换函数。
- $n_j$：块 $\mathbf{B}_j$ 被重复应用的次数。
- $(\mathbf{B}_k^{(n_k)}\circ\cdots\circ\mathbf{B}_1^{(n_1)})$：按序组合 $k$ 个绑定块得到的近似。
- $\varepsilon$：允许的 Frobenius 范数误差上界，要求足够小以保证轨迹保真。

### Raptor 激活近似
基于 BRH，Raptor 将输入 $\mathbf{x}$ 经过 patch embedding 后的初始激活 $\mathbf{a}_0(\mathbf{x})$ 依次通过各块得到第 $\ell$ 层的预测激活 $\tilde{\mathbf{a}}_\ell(\mathbf{x})$：

$$
\tilde{\mathbf{a}}_\ell(\mathbf{x}) \equiv (\mathbf{B}_k^{(n_k)}\circ\cdots\circ\mathbf{B}_1^{(n_1)})(\mathbf{a}_0(\mathbf{x}))
$$

- $\mathbf{a}_0(\mathbf{x})$：来自教师 ViT patch embedding 的初始表示。
- $\tilde{\mathbf{a}}_\ell$：Raptor 对原始 ViT 第 $\ell$ 层激活的近似。

### 自回归轨迹损失
为强制层间轨迹匹配，Raptor 采用自回归训练，逐层比对预测激活与教师激活：

$$
\mathcal{L}_h^{\mathrm{AR}}(\mathbf{x}) = \mathbb{E}_{\mathbf{x}}\!\Big( \sum_{\ell=1}^h \|\tilde{\mathbf{a}}_\ell(\mathbf{x}) - \mathbf{a}_\ell(\mathbf{x})\|_F \Big), \quad h \leq L
$$

- $\mathbf{a}_\ell(\mathbf{x})$：教师 ViT 在中间层 $\ell$ 的真实激活。
- $h$：当前监督的总层数，训练中退火控制。
- 损失为各层 Frobenius 误差之和，强制循环块输出与原始深度轨迹高度一致。

### 总训练损失（两阶段组合）
Raptor 的训练目标混合教师强制（TF）和自回归（AR）两种信号，并通过可退火的 $\lambda$ 平衡：

$$
\mathcal{L}_{\mathrm{total}}(\mathbf{x}) = \lambda \mathcal{L}_{\mathrm{TF}}(\mathbf{x}) + (1-\lambda) \mathcal{L}_{\mathrm{AR},H}(\mathbf{x}) + \Omega(\boldsymbol{\theta})
$$

- $\mathcal{L}_{\mathrm{TF}}$：教师强制损失，使当前块输出与目标层激活直接对齐。
- $\mathcal{L}_{\mathrm{AR},H}$：前 $H$ 层的自回归损失。
- $\lambda \in [0,1]$：第一阶段逐步退火至 $0$，使模型从依赖教师信号转向纯自回归生成。
- $\Omega(\boldsymbol{\theta})$：正则化项（如权重衰减）。

两阶段训练流程：第一阶段独立训练每个块并逐步退火 $\lambda$；第二阶段将所有块串联后以 $\lambda=0$ 做端到端自回归训练。

### 深度缩放调制
为让共享参数的循环块在不同层表现出差异，Raptor 引入一个基于层索引 $z$ 的缩放向量，调制注意力残差、MLP 残差及块输出，使系统成为非自主的动力系统。

缩放向量 $\mathbf{S}$ 由一个小型 MLP 产生：

$$
\mathbf{S} = (\mathbf{W}_2 \cdot \mathrm{SiLU}(\mathbf{W}_1 z + \mathbf{b}_1) + \mathbf{b}_2) + \mathbf{1}
$$

- $z$：目标层索引（连续值）。
- $\mathbf{W}_1, \mathbf{W}_2, \mathbf{b}_1, \mathbf{b}_2$：可学习参数。
- $\mathbf{1}$：单位偏移，确保初始化时缩放向量接近恒等，保持训练的稳定性。

该缩放向量以逐元素乘法的形式注入到块内的注意力残差和 MLP 残差中，例如：

$$
\mathbf{X}' = \mathbf{X} + \mathbf{s}_{\mathrm{attn}} \odot \mathrm{LS}_1\big( \mathrm{Attn}(\mathrm{LN}_1(\mathbf{X})) \big)
$$

其中 $\mathbf{s}_{\mathrm{attn}}$ 是 $\mathbf{S}$ 中对应注意力部分的子向量，$\mathrm{LS}$ 为 LayerScale 操作。

## 实验与分析

我们的实验围绕一个核心检验：**视觉Transformer的深度方向是否隐含一个可被递归复用的块状结构？** 为此，我们构建了Raptor（Recurrent Approximations to Phase‑structured TransfORmers），在预训练模型上进行后验蒸馏，并系统评估了其重构保真度、性能边界以及导致块递归涌现的动力学条件。所有骨干均被冻结，仅训练线性评估头（或分类器），评估复用DINOv2的patch embedding与最终LayerNorm，并报告3个种子的均值和标准差。以下先给出主结果，再深入消融训练、分割策略与因果干预的证据链，最后归纳失败模式与待解决问题。

### 主结果：块递归逼近的性能边界

ImageNet‑1k线性探针结果（Table 2）显示，仅使用2个参数绑定块的Raptor（k=2）即能恢复DINOv2 ViT‑B 96%的准确率（81.0 vs 84.5），k=3达到83.0（恢复98%），p=3的Raptor同时超越ViT‑S（80.9）。在密集预测任务上，Raptor同样保持竞争力：ADE20k语义分割mIoU达43.0（ViT‑B为47.5，ViT‑S为44.6），NYUv2深度估计RMSE为0.618（ViT‑B为0.578）。随块数k增加，重构保真度R²与下游精度同步提升（Figure 5），表明**块递归假设不仅作为一种近似有效，而且与性能之间存在正相关的保真度—精度律**。

![[assets/figures/papers/iclr26_0013_gH3HhnfWLC_Block_Recurrent_Dynamics_in_Vision_Transformers/figures/014_Table_2.jpg]]
*Table 2: Performance of Raptor compared to DINOv2 with linear probes. We report top-1 accuracy on ImageNet-1k, mean Intersection-over-Union (mIoU) on ADE20k semantic segmentation, and root mean squared error (RMSE) on NYUv2 depth estimation. Higher values are better for accuracy and mIoU, while lower values are better for RMSE. Results for Raptor are aggregated over three model runs, each trained with a different random seed, and displayed as $\mu \pm \sigma$ . For Raptor, Arch denotes the number of recurrent blocks, while for DINOv2, Arch denotes the ViT backbone

这一结果的重要性在于：Raptor以远小于ViT‑B的参数量（仅重复使用k个Transformer块）逼近了教师模型。剩余的性能差距（ImageNet‑1k约1.5%，ADE20k约4.5 mIoU）揭示块递归逼近仍存在上限，尤其在需要细密空间解析的任务中更明显，提示后期低秩动态（附录D）可能损失了部分令牌特异性。

### 训练范式消融：自回归轨迹匹配是关键

从Table 1的递进消融可清晰看出块递归的构造瓶颈：
- **纯Teacher Forcing（蒸馏）灾难性失效**：直接以DINOv2输出为目标训练Raptor，ImageNet‑1k精度仅3.9%。说明即便所有中间激活由教师提供，学生也无法收敛到可利用的解，因为误差在自回归回路中迅速累积。
- **加入自回归轨迹损失（AR）**使精度跃升至72.7：模型被强制匹配自身生成轨迹与教师中间激活的逐层Frobenius差值（式2），从而习得自一致性。
- **深度缩放模块**（+2.5%）与**加权分类令牌**（+1.5%）进一步稳定了跨层相位对齐。
- **第二阶段的端到端自回归训练**（将三个独立块串联后全模型联合训练）贡献最大（+5.7%），表明块间协同对减少长期累积误差至关重要。
- **最终分类器微调**仅带来微量提升（+0.6%），说明冻结的线性头已接近饱和。

![[assets/figures/papers/iclr26_0013_gH3HhnfWLC_Block_Recurrent_Dynamics_in_Vision_Transformers/figures/013_Table_1.jpg]]
*Table 1: Ablations to original Raptor(k=3) model, showing ImageNet-1k accuracy with DINOv2 pretrained linear classifier. Second Stage refers to putting all three blocks together and training the full model autoregressively*

该消融确立了Raptor训练的因果逻辑：**轨迹匹配而非输出蒸馏是递归重用的必要条件，且自回归自洽需在分阶段训练中逐步注入**。

### 分区策略与因果干预：阶段边界决定功能复用

Raptor依赖于最大割算法发现的块分区。在CIFAR‑100上（Figure 3），最大割分区k=2、3、4均明显优于随机连续分区及随机打乱分区（跨10个随机种子），说明**原始ViT的层间相似度结构携带着功能相关的相位信息**，随机切分会割裂共享计算单元。

![[assets/figures/papers/iclr26_0013_gH3HhnfWLC_Block_Recurrent_Dynamics_in_Vision_Transformers/figures/007_Figure_2.jpg]]
*Figure 2: Block discovery via max-cut segmentation of the layer–layer similarity matrix. Our algorithm partitions depth into contiguous segments by maximizing within-block similarity and minimizing cross-block cosine similarity. Shown are two cuts of the same ViT-B: with 3-blocks (left, green) and 2-blocks (right, magenta). These cuts reveal candidate block boundaries where the representation dynamics undergo sharp transitions, providing an operational method for detecting contiguous recurrent phases in trained ViTs. Figure 3: Evaluation of Raptor models on CIFAR-100 using our maxcut partitioning algorithm versus random partitions. Reported values are classification accuracy. Results for random parti...*

更直接的因果证据来自层互换实验（Figure 15）：在DINOv2 ViT‑B内，将属于同一最大割块内的1～3层进行替换，准确率几乎不变；而跨块替换导致性能崩溃。这证明**块内层确实执行相同或几乎相同的映射，而块间存在不同的功能阶段**——块结构不仅是表示层面的表象，更是因果上可交换的计算模块。

![[assets/figures/papers/iclr26_0013_gH3HhnfWLC_Block_Recurrent_Dynamics_in_Vision_Transformers/figures/034_Figure_15.jpg]]
*Figure 15: Causal intervention. DINOv2-Base accuracy on ImageNet-1k validation set with 1, 2, and 3 layers replaced with another layer ( k = 1 , k = 2 , k = 3 , respectively). Intra-block refers to replacing a layer with another layer from the same block. Inter-block refers to replacing a layer with a layer from a different block. Blocks are determined by the max cut algorithm. The significantly higher accuracy of intra-block replacements (blue) compared to inter-block (orange) confirms that layers within a block are functionally interchangeable in a way that any two arbitrary blocks are not, supporting the block-recurrent hypothesis*

### 随机深度正则化促进块结构涌现

我们进一步追问：**什么训练条件促进了这种递归结构的涌现？** Figure 4给出了清晰答案。在CIFAR‑100上训练ViT‑B时，随着随机深度（SD）概率p增大：
- 层间余弦相似度系统性升高（Figure 4A），块状结构更明显（Figure 4E）；
- Raptor重构R²随之提高（Figure 4B,D）；
- 教师ViT及Raptor学生的准确率同步上升（Figure 4C）。

![[assets/figures/papers/iclr26_0013_gH3HhnfWLC_Block_Recurrent_Dynamics_in_Vision_Transformers/figures/011_Figure_4.jpg]]
*Figure 4: Stochastic depth promotes representational similarity across layers block-recurrence. A) ViT layer-layer cosine similarity matrices for models trained with increasing stochastic depth (SD) dropout probability p (probabilities of 0.0-0.9, uniform over layer depth). Dashed red lines delineate blocks, as defined by the max-cut algorithm. Higher SD p values lead to a more similar representation across layers. B) Layerwise teacher-student representational alignment R ^ { 2 } (Raptor vs. ViT) of the class cls and patch tokens. Increases in SD p correspond to an increase in the ability of Raptor to match the ViT’s layerwise representations. ViT models for SD=0.7-0.9 show abberant training dynamics...*

随机深度迫使网络在任意层被丢弃时仍能维持表示质量，实质上要求各个残差单元必须可被跳过或复用——这正是块递归的动力学印记。过拟合实验中，层间相似度和重构保真度的同步退化（Figure 13）进一步反证：**块递归结构并非默认属性，而是在充分正则化下训练收敛至低维吸引子的涌现结果**。

### 动态解释性验证：收敛、相位与低秩更新的协调

通过方向收敛测度γ_ℓ、令牌特异的角速度s_ℓ、稳定秩r_s等动力学指标（Figures 6‑9），我们发现：
- 表示方向沿深度单调收敛至类别相关的角度吸引子，并具备抵御扰动的自校正能力；
- 角速度在最大割划分的相位边界处出现急剧转变，为阶段划分的合理性提供了独立信号；
- 深度后期，层更新矩阵的有效秩显著降低，令牌更新方向高度相干（平均场行为），印证了后期动态仅需少数控制模式即可描述。

这些观察虽然本质上仍是现象学而非直接因果验证，但与Raptor可构造性结论高度一致：**ViT深度方向的功能阶段化是收敛至角吸引子、令牌更新从高维探索转变为低维精调的多阶段动态的直接结果**。

### 失败模式与限制

1. **训练复杂性**：两阶段训练（独立块训练→全模型自回归微调）对超参数敏感，λ退火节奏、深度缩放的嵌入维度需按教师模型调整，难以直接泛化到其他架构。
2. **密集预测的性能鸿沟**：Raptor在ADE20k上损失4.5 mIoU（相对ViT‑B），差距明显大于分类任务。这暗示块递归可能抹平了某些令牌级的高频差异，改进方向包括为密集任务保留部分逐层特殊化参数或引入时变残差门控。
3. **因果机制的缺失**：层互换、随机深度效应等提供了强相关性证据，但尚未通过受控训练实验（例如，直接删除随机深度后观察结构是否消失）确立因果方向。动态解释学目前停留在描述层间现象，未形式化为可操作的干预框架。
4. **规模局限性**：所有实验均在ViT‑B/14上完成，更大模型（ViT‑L）或多模态任务中块递归是否依然成立未知。

### 关键图表结论汇总

- **Figure 1**：跨多种ViT的层-层相似度矩阵均呈现连续块结构，奠定BRH的实证基础。
- **Figure 2 / Figure 3**：最大割划分算法能有效识别相位边界，且其分区显著优于随机分区，证实相似度块与功能阶段对应。
- **Figure 4 / Figure 13**：随机深度是块递归涌现的关键正则化驱动力，过拟合破坏块结构。
- **Figure 5 / Table 2**：Raptor以k=3即恢复教师模型98%的线性探针性能，但密集预测任务存在系统性差距。
- **Table 1**：轨迹匹配损失替换纯蒸馏损失使准确率从3.9%跃升，自回归训练的第二阶段贡献最大的+5.7%。
- **Figure 15**：块内层替换保持精度而块间替换崩溃，为功能块递归复用提供了因果层级的证据。
- **Figures 6‑9**：动态测度从方向、角速度、低秩更新等维度交叉验证了相位边界的动力学意义。

## 方法谱系与知识库定位

Raptor 并非提出一种全新的视觉架构，而是通过 **块递归假设（Block‑Recurrent Hypothesis, BRH）** 揭示预训练 ViT 内部的低算法复杂度本质，并将其操作化为可复现的循环代理模型。因此，该方法在知识库中的位置主要由它与教师模型、训练范式和阶段发现策略的对比关系界定，其适用边界则直接受限于 BRH 成立的隐含条件与当前蒸馏训练的技术瓶颈。

### 与基准方法的关系及知识定位

**与 DINOv2 教师模型的关系。** Raptor 的直接参照上限是 DINOv2 ViT‑B（教师模型，12 层独立参数）。两者共享相同的 patch embedding 和最终 LayerNorm，差异仅在于骨干层间是否复用参数。实验显示，仅 2 个循环块的 Raptor（k=2）即可在 ImageNet‑1k 线性探针上恢复教师模型 96% 的准确率，k=3 时达到 98%，对应的 Levin 复杂度由 $O(L)$ 降至 $O(k)$（详见 `Claim 2, Appendix E`）。这表明 **循环权重绑定本身并未根本性地牺牲表示质量**，而是将原模型深度维度上隐式的计算冗余外显化。然而，k=3 时仍存在约 1.5% 的绝对精度缺口，且在密集预测任务上更为明显（ADE20k mIoU 下降 4.5，NYUv2 RMSE 上升 0.04；`Table 2`）。这构成了该方法的核心性能边界：对于需要精细局部适配的下游任务，简单的块递归循环难以完全覆盖多层独立参数的特化功能。

**与较小基线及训练范式的对比。** Raptor 并非纯粹的模型压缩：k=3 时 ImageNet 准确率（83.0%）显著超越参数量类似的 DINOv2 ViT‑S（80.9%，`Table 2`），说明递归执行紧凑程序体可能自带正则化效益。不同训练范式的消融确立了 Raptor 有效性的关键：纯 Teacher Forcing（仅逐层蒸馏激活）导致准确率仅 3.9%，而引入自回归轨迹损失（`Eq. 2`）并退火 Teacher Forcing 权重后跃升至 72.7%，两阶段端到端自回归训练最终达到 83.0%（`Table 1`）。这揭示功能上的相位对齐并非由静态蒸馏达成，而是依赖**自回归轨迹匹配强制块间自相容性**。

**分区策略的效力与限制。** Max‑cut 算法基于层间余弦相似度识别连续阶段边界，其效果大幅优于随机连续分区和随机置乱分区（`Figure 3`），且与动力学分析中的相位过渡吻合（`Figures 6‑9`）。这确立了该算法作为 BRH 操作化核心的有效性，但也设下隐含前提：层间表示相似性需能以块对角形式显现。若目标模型因过拟合或弱正则化而未能形成清晰的块结构（如 `Figure 13` 所示），max‑cut 分区将不可靠，因此该方法仅在由适度随机深度（`Figure 4`）等机制诱导的涌现阶段结构中适用。

**在知识库中的定位。** 该工作将 ViT 深度轴重新解读为离散时间的动力学展开，构建了**动态可解释性**（Dynamical Interpretability）程序，提炼出方向收敛 $\gamma_\ell$、角速度 $s_\ell$、低秩更新 $r_s$ 及令牌相干性 $\kappa_\ell$ 等测度，形成一套新的表征分析工具。与已有的解释性方法相比，该分析目前仍属观察性质，尚未通过受控干预建立严格的因果链条。

### 适用边界与局限性

1. **训练正则化依赖**：块递归结构在随机深度概率 $p$ 增大时明显增强（`Figure 4A-E`），因此该方法要求教师模型在含强正则化条件下训练，或在蒸馏阶段隐式引入类似机制；训练不足会导致相似度矩阵平坦化，致使 max‑cut 分区失效。
2. **训练流程复杂性**：两阶段训练涉及独立块预训练、退火混合损失、深度缩放模块及最终全模型微调，超参数（λ 退火速度、各阶段学习率等）需针对不同教师模型手动调节，缺乏自动化原则。
3. **密集预测任务退化**：为表示轨迹保真（`Eq. 2`）设计的训练目标，未能充分保留层间局部细粒度的特化差异，使循环块在语义分割、深度估计等任务上出现显著精度下降（`Table 2`）。
4. **规模验证局限**：所有实验均限于 ViT‑B/14 规模；更大模型（如 ViT‑L）或多模态扩展下的递归结构保持性仍未经探索。

### 开放问题

1. **表示相似性是否等价于功能可重用性？** 层间余弦相似度高并非计算路径一致的充分条件，需设计干预实验以排除虚假相似。
2. **块结构涌现的条件边界**：在何种训练条件（数据规模、优化器、架构变体）下 BRH 必然出现？哪些条件下会消失？这需要受控训练动力学实验以建立因果关系。
3. **剩余性能差距的来源**：该差距是本质的相位偏差所致，还是训练技术不完美（如蒸馏损失、深度缩放容量不足）导致？前者需要改进循环约束的表达力，后者则呼唤更先进的蒸馏或时变组件。
4. **BRH 能否导向主动设计？** 能否利用 BRH 设计更高效的初始化或训练算法，直接从零开始诱导循环结构，而非仅作为事后提取工具？这关系到该范式的实用化深度。

## 原文 PDF

![[paperPDFs/ICLR_2026/Block_Recurrent_Dynamics_in_Vision_Transformers.pdf]]
