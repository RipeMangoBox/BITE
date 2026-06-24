---
title: "Half-order Fine-Tuning for Diffusion Model: A Recursive Likelihood Ratio Optimizer"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Half_order_Fine_Tuning_for_Diffusion_Model_A_Recursive_Likelihood_Ratio_Optimizer.pdf
openreview_forum_id: AZ6lqcvHLX
aliases:
- RLRROHOFT
- HOFTDMRLRO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过引入基于似然比（LR）技术的半阶（HO）梯度估计器，将扩散链的计算图重组为局部一阶（FO）+ 多步半阶 + 零阶（ZO）的组合，从而在有限内存下实现无偏且低方差的梯度估计。"
primary_logic: "将扩散模型的微调形式化为计算预算约束下的最小方差无偏估计问题，利用模型内部的固有噪声构建局部反向传播链，平衡了偏差、方差与计算成本，同时捕获多尺度信息。"
claims:
- "RLR梯度估计器是无偏的，且方差低于其他方法。"
- "截断BP导致模型崩溃，奖励分数大幅下降。"
- "RLR在后期训练中持续提升奖励，而AlignProp发生模型崩溃。"
- "消融实验表明，移除HO或ZO组件会导致性能下降。"
---

# Half-order Fine-Tuning for Diffusion Model: A Recursive Likelihood Ratio Optimizer

> [!tip] 核心洞察
> 将扩散模型的微调形式化为计算预算约束下的最小方差无偏估计问题，利用模型内部的固有噪声构建局部反向传播链，平衡了偏差、方差与计算成本，同时捕获多尺度信息。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 扩散模型的半阶微调：递归似然比优化器 |
| 英文题名 | Half-order Fine-Tuning for Diffusion Model: A Recursive Likelihood Ratio Optimizer |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=AZ6lqcvHLX); [GitHub](https://github.com/RTkenny/RLR-Optimizer) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Recursive Likelihood Ratio (RLR) Optimizer (Half-Order Fine-tuning) |
| Dataset | HPD v2, VBench |

> [!tip] 效果简介
> - HPD v2 上，PickScore 为 21.38 (RLR SD1.4)，对比 19.17 (Alignprop SD1.4)，变化 +2.21。
> - HPD v2 上，AES 为 6.65 (RLR SD1.4)，对比 6.02 (Alignprop SD1.4)，变化 +0.63。
> - VBench 上，Weighted Average 为 84.63 (RLR)，对比 83.45 (VADER)，变化 +1.18。

## 概述

扩散模型在生成高质量图像和视频方面取得了显著进展，然而，如何高效地对预训练扩散模型进行微调以对齐人类偏好仍然是一个核心挑战。现有微调方法主要分为两类：**截断反向传播（Truncated BP）** 方法（如AlignProp、VADER）虽然计算成本低，但会引入结构性偏差，导致模型在训练后期发生崩溃，奖励分数大幅下降（Figure 3）；**强化学习（RL）** 方法（如DDPO）虽能保证无偏梯度估计，但方差大、样本效率低，训练过程不稳定。这一问题本质上可形式化为：**在有限计算预算约束下，寻找最小方差的无偏梯度估计器**。

本文提出了 **递归似然比（Recursive Likelihood Ratio, RLR）优化器**，一种面向扩散模型的**半阶（Half-Order, HO）微调**范式。其核心思路是：将扩散链的计算图重组为**局部一阶（FO）反向传播 + 多步半阶（HO）似然比估计 + 零阶（ZO）参数扰动**的组合结构。具体而言，RLR对最后一步执行精确的一阶反向传播以利用奖励模型的结构信息；在随机选择的中间步 $j$ 上构建长度为 $h$ 的局部子链，利用模型固有噪声和似然比技巧进行半阶梯度估计，捕获特定尺度的生成信息；对剩余步则注入参数噪声构造零阶估计以保证整体无偏性。这一设计在理论上保证了梯度估计的无偏性（Theorem 6.3），同时通过子链长度 $h$ 的优化在方差和内存之间取得平衡。

实验结果表明，RLR在文本到图像和文本到视频的微调任务上均显著优于现有基线。在HPD v2基准上，RLR微调的SD1.4模型在PickScore和AES指标上分别达到21.38和6.65，相比AlignProp提升+2.21和+0.63（Table 2）；在VBench视频生成评估中，RLR以84.63的加权平均分超越所有基线（Table 3）。消融实验证实，移除HO或ZO组件均会导致性能显著下降，验证了组合方法的必要性（Table 5）。训练曲线进一步显示，RLR在后期训练中持续提升奖励分数，而截断BP方法则出现明显的模型崩溃（Figure 5）。

## 背景与动机

扩散模型（Diffusion Models, DMs）通过一个递归的去噪过程将随机噪声逐步转化为高质量样本，其生成能力已在图像、视频等多个领域得到验证。然而，将预训练扩散模型进一步微调以对齐人类偏好或特定奖励信号时，面临一个根本性的梯度估计困境。

扩散模型的生成链可形式化为 $x_0 = \phi_{1:T}(x_T, z_{1:T}; \theta)$，其中每一步 $x_{t-1} = \phi_t(x_t, z_t; \theta)$ 依赖参数 $\theta$ 和随机噪声 $z_t$。微调的目标是最大化生成样本的期望奖励：

$$\max_{\theta} \mathbb{E}[R(x_0)] = \max_{\theta} \mathbb{E}_{z_{1:T}}[R(\phi_{1:T}(x_T, z_{1:T}; \theta))]$$

计算该目标的梯度 $\nabla_{\theta} \mathbb{E}[R(x_0)]$ 时，由于生成链长达数十步（通常 $T=50$），完整反向传播（Full BP）的内存开销随步数线性增长，在实际中几乎不可行。现有方法在应对这一挑战时形成了两个极端：

- **截断反向传播（Truncated BP）**：仅对最后几步进行梯度回传，大幅降低计算成本。然而，截断操作引入了结构性偏差——被丢弃的早期步骤的梯度信息永久丢失。实证表明，这种偏差会导致严重的**模型坍塌**（Figure 3）：在美学奖励模型的微调任务中，截断BP训练的SD 1.4模型的奖励分数在训练后期急剧下降，且截断步数越少，坍塌越剧烈。

- **强化学习方法（RL-based）**：如DDPO等策略梯度方法，通过采样估计梯度，具有无偏性。但其梯度估计的方差极大，导致样本效率低下，训练过程不稳定。

因此，核心瓶颈可归结为：**在有限的计算资源（内存、时间）约束下，如何获得既无偏又低方差的梯度估计器？** 这本质上是一个约束优化问题——在无偏估计器集合中寻找方差最小者：

$$\min_{G \in \mathcal{G}} \operatorname{Var}(G) \quad \text{s.t.} \quad \nabla_{\theta} \mathbb{E}[R(x_0)] = \mathbb{E}[G], \quad \mathcal{C}(G) \leq \mathcal{B}$$

本文的动机正是弥合这一偏差-方差-成本的三元权衡缺口：既不接受截断BP的偏差风险，也不忍受RL方法的高方差低效，而是通过重组扩散链的计算图，在局部引入精确梯度信息，在其余部分采用无偏的低成本估计，从而在给定内存预算下逼近最小方差无偏估计的理论下界。

## 核心创新

### 问题瓶颈：偏差-方差-内存的三元权衡

扩散模型微调的核心困难在于梯度估计须穿越整个递归去噪链。现有方法陷入两难：**截断反向传播（Truncated BP）** 仅对最后几步精确求导，计算成本低但引入结构性偏差——图3显示截断步数越少，模型崩溃越严重，奖励分数断崖式下降；**强化学习方法（如DDPO）** 虽无偏但依赖蒙特卡洛采样，方差大、样本效率低。这一困境可形式化为预算约束下的最小方差无偏估计问题：

$$\min_{G \in \mathcal{G}} \operatorname{Var}(G) \quad \text{s.t.} \quad \nabla_{\theta} \mathbb{E}[R(x_0)] = \mathbb{E}[G], \quad \mathcal{C}(G) \leq \mathcal{B}$$

### 核心操作：递归似然比（RLR）半阶优化器

RLR的关键创新在于**将扩散链的计算图重组为三类局部估计器的组合**，而非对整条链做全有或全无的选择：

| 组件 | 覆盖范围 | 估计方式 | 作用 |
|------|---------|---------|------|
| **一阶（FO）估计器** | 最后一步 | 精确反向传播，利用奖励模型结构 | 提供低方差梯度信号 |
| **半阶（HO）估计器** | 随机起始步 $j$ 开始的 $h$ 步局部子链 | 似然比技巧，利用模型固有噪声 $z_t$ 构造 $R(x_0) \cdot D_{\theta}^{\top} \phi_{j:j+h} \cdot \nabla \ln f(z_j)$ | 捕获特定尺度信息，方差可控 |
| **零阶（ZO）估计器** | 剩余步 | 对参数注入噪声的无偏零阶估计 | 确保全局无偏性，内存消耗极低（约0.24GB/步） |

这一设计的本质是**“局部精确 + 全局无偏”**：FO提供锚点精度，HO在关键子链上保持低方差梯度流，ZO以极低成本补齐剩余步的无偏性。定理6.3严格证明了RLR估计器的无偏性：$\nabla_{\theta} \mathbb{E}[R(x_0)] = \mathbb{E}[G_{RLR}]$。

### 子链自适应优化

不同于固定截断长度的启发式做法，RLR将子链起点 $j$ 和长度 $h$ 都纳入优化。$j$ 通过梯度范数重要性采样（$j \sim \text{Softmax}(\|g\|)$）选择，使HO聚焦信息量最大的去噪阶段。$h$ 则通过求解方差-内存约束的代理优化问题得到闭式解：

$$h^{*} = \min\left\{\left\lfloor \frac{\mathcal{B} - \mathcal{B}_z (T-1)}{\mathcal{B}_h - \mathcal{B}_z} \right\rfloor, \left\lfloor \frac{T V_z}{2 (V_z - V_h)} - 1 \right\rfloor\right\}$$

其中 $\mathcal{B}$ 为内存预算，$\mathcal{B}_h$ 和 $\mathcal{B}_z$ 分别为HO和ZO的单步内存成本，$V_h$ 和 $V_z$ 为对应方差。消融实验（Table 9）证实：增大 $h$ 可提升奖励，但 $h>2$ 后增益趋于饱和，而内存和时间开销线性增长——这验证了闭式解在实践中的有效性。

### 与基线的本质差异

| 维度 | 截断BP（AlignProp/VADER） | RL方法（DDPO） | RLR（本文） |
|------|--------------------------|---------------|------------|
| **无偏性** | 有偏（结构性偏差） | 无偏 | 无偏（定理保证） |
| **方差** | 低 | 高 | 低（方差上界可控） |
| **计算图** | 最后几步截断链 | 全链采样 | FO + HO子链 + ZO补全 |
| **子链长度** | 固定超参数 | 不适用 | 自适应闭式解 |
| **多尺度能力** | 弱（仅捕获后期特征） | 间接 | 通过 $j$ 采样显式建模 |

Figure 5的奖励曲线直接印证了这一差异：RLR在训练后期持续提升奖励，而AlignProp发生模型坍塌、奖励骤降。消融实验（Table 5）进一步证实，移除HO和ZO（退化为单步BP）或仅移除ZO（退化为有偏估计）均导致性能大幅下降，验证了三组件协同的必要性。

## 整体框架

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_AZ6lqcvHLX/figures/010_Figure_6.jpg]]
*Figure 6: The framework of Diffusive Chain-of-Thought. The DM generates images in a multi-scale manner: earlier steps for low-resolution features and later steps for high-resolution features. If a specific scale has deficiencies, we utilize the HO estimator to enhance the corresponding steps*

RLR（Recursive Likelihood Ratio）优化器的核心思想是将扩散模型的微调形式化为**计算预算约束下的最小方差无偏估计问题**，并通过重组扩散链的计算图来实现偏差、方差与计算成本三者的平衡。其整体pipeline由以下模块构成：

### 1. 问题形式化

给定预训练扩散模型的去噪过程 $x_{t-1} = \phi_t(x_t, z_t; \theta)$，微调目标为最大化生成样本的期望奖励：

$$\max_{\theta} \mathbb{E}[R(x_0)] = \max_{\theta} \mathbb{E}_{z_{1:T}}[R(\phi_{1:T}(x_T, z_{1:T}; \theta))]$$

梯度估计的核心挑战在于：**截断反向传播（Truncated BP）** 虽然计算成本低，但会引入结构性偏差，严重时导致模型崩溃（Figure 3）；**强化学习（RL）方法** 虽无偏但方差大、样本效率低。RLR将这一问题形式化为：

$$\min_{G \in \mathcal{G}} \operatorname{Var}(G) \quad \text{s.t.} \quad \nabla_{\theta} \mathbb{E}[R(x_0)] = \mathbb{E}[G], \quad \mathcal{C}(G) \leq \mathcal{B}$$

即在计算预算 $\mathcal{B}$ 下，寻找无偏且方差最小的梯度估计器 $G$。

### 2. 梯度估计器设计空间

扩散链的 $T$ 步去噪过程中，每一步的梯度估计可从三类算子中选择：
- **一阶（FO）**：精确反向传播，方差低但内存消耗大
- **半阶（HO）**：利用似然比（Likelihood Ratio）技术在局部链上估计梯度，无偏且内存可控
- **零阶（ZO）**：注入参数噪声构造无偏估计，内存消耗极小但方差较高

完整的估计器设计空间为 $\mathcal{G}_{\text{full}} := \{ G = (g_1, \dots, g_T) \mid g_t \in \{\text{FO, HO, ZO}\} \}$，共 $3^T$ 种组合。

### 3. RLR估计器结构

RLR将搜索空间缩减为一种结构化组合：**单步FO + 多步HO子链 + 其余ZO**，具体为：

$$G_{\text{RLR}} = \underbrace{D_{\theta}^{\top} \phi(x_1, z_1; \theta) \frac{d R(x_0)}{d x_0}}_{\text{单步一阶（FO）估计器}} - \underbrace{R(x_0) D_{\theta}^{\top} \phi_{j:j+h}(x_{j+h}, z_{j:j+h}; \theta) \nabla_z \ln f(z_j)}_{h\text{步半阶（HO）子链估计器}} - \underbrace{\sum_{i \in \mathcal{C}} R(x_0) \nabla_z \ln f(z_i)}_{\text{零阶（ZO）估计器}}$$

三个组件的分工如下（Figure 4）：

| 模块 | 作用 | 关键特性 |
|------|------|----------|
| **FO估计器** | 对最后一步 $t=1$ 进行精确反向传播，利用奖励模型对 $x_0$ 的梯度结构 | 低方差，仅需存储单步计算图 |
| **HO估计器** | 在随机起始步 $j$ 开始长度为 $h$ 的局部链，利用模型固有噪声 $z_j$ 和似然比技巧估计梯度 | 无偏，捕获特定尺度的多步依赖 |
| **ZO估计器** | 对剩余步 $i \in \mathcal{C}$ 注入参数噪声，构造无偏零阶估计 | 内存极低（每步约0.24GB），保证全局无偏性 |

### 4. 子链参数优化

**子链起点 $j$ 的选择**：基于梯度范数的重要性采样，$j \sim \text{Softmax}(\|g_t\|)$，使HO子链集中于梯度信息丰富的区域，从而捕获多尺度特征。

**子链长度 $h$ 的优化**：通过求解方差-内存约束的代理优化问题得到闭式解：

$$h^{*} = \min\left\{\left\lfloor \frac{\mathcal{B} - \mathcal{B}_z (T-1)}{\mathcal{B}_h - \mathcal{B}_z} \right\rfloor, \left\lfloor \frac{T V_z}{2 (V_z - V_h)} - 1 \right\rfloor\right\}$$

其中 $\mathcal{B}_h$、$\mathcal{B}_z$ 分别为HO和ZO的单步内存成本，$V_h$、$V_z$ 为对应方差。实验表明（Table 9），$h$ 增大可提升奖励分数，但 $h>2$ 后增益趋于饱和，同时内存和时间开销线性增长。

### 5. 输入输出流

1. **输入**：预训练扩散模型参数 $\theta$、噪声样本 $x_T$、奖励模型 $R(\cdot)$、内存预算 $\mathcal{B}$
2. **前向采样**：执行完整 $T$ 步去噪生成 $x_0$，记录每步噪声 $z_t$
3. **奖励计算**：$R(x_0)$ 通过奖励模型获得标量奖励
4. **梯度估计**：按RLR结构分别计算FO、HO、ZO三项，组合为无偏梯度估计 $G_{\text{RLR}}$
5. **参数更新**：使用估计梯度更新模型参数 $\theta \leftarrow \theta + \eta \cdot G_{\text{RLR}}$
6. **输出**：微调后的扩散模型

### 6. 理论保证

RLR估计器具有严格的无偏性（Theorem 6.3）：$\nabla_{\theta} \mathbb{E}[R(x_0)] = \mathbb{E}[G_{\text{RLR}}]$，且在 $L$-平滑奖励函数下具有 $\mathcal{O}(1/\sqrt{K})$ 的收敛速率（Theorem 6.4）。消融实验（Table 5）证实：移除HO和ZO组件（仅保留单步BP）导致性能大幅下降；移除ZO使估计器变为有偏，表现不及完整RLR，验证了无偏性和组合结构的必要性。

## 核心模块与公式推导

### 问题形式化

扩散模型的微调目标为最大化生成样本的期望奖励：

$$\max_{\theta} \mathbb{E}[R(x_0)] = \max_{\theta} \mathbb{E}_{z_{1:T}}[R(\phi_{1:T}(x_T, z_{1:T}; \theta))]$$

其中单步去噪过程定义为 $x_{t-1} = \phi_t(x_t, z_t; \theta)$，完整生成链为 $x_0 = \phi_{1:T}(x_T, z_{1:T}; \theta) = \phi_1 \circ \phi_2 \circ \dots \circ \phi_T(x_T, z_{1:T}; \theta)$。核心挑战在于：在计算预算 $\mathcal{B}$ 约束下，寻找一个无偏且方差最小的梯度估计器：

$$\min_{G \in \mathcal{G}} \operatorname{Var}(G) \quad \text{s.t.} \quad \nabla_{\theta} \mathbb{E}[R(x_0)] = \mathbb{E}[G], \quad \mathcal{C}(G) \leq \mathcal{B}$$

### 梯度估计器设计空间

完整的设计空间 $\mathcal{G}_{\text{full}}$ 由每个时间步 $t$ 上选择一阶（FO）、半阶（HO）或零阶（ZO）估计器的所有序列构成：

$$\mathcal{G}_{\text{full}} := \{ G = (g_1, \dots, g_T) \mid g_t \in \{\text{FO, HO, ZO}\} \ \forall 1 \leq t \leq T \}$$

RLR 优化器将该空间缩减为一个结构化组合：最后一步采用精确 FO 反向传播，中间随机位置 $j$ 起始长度为 $h$ 的局部子链采用 HO 估计，其余步采用 ZO 估计：

$$\mathcal{G}_{\text{RLR}} = \{ (g_1^{\text{FO}}, \dots, g_j^{\text{HO}}, \dots, g_{j+h}^{\text{HO}}, \dots, g_T^{\text{ZO}}) \mid 1 \leq j \leq T - h \}$$

### RLR 估计器的三个核心模块

**（1）一阶（FO）估计器**：对最后一步 $x_1 \to x_0$ 执行精确反向传播，利用奖励模型的可微结构计算梯度：

$$D_{\theta}^{\top} \phi(x_1, z_1; \theta) \frac{d R(x_0)}{d x_0}$$

**（2）半阶（HO）估计器**：在随机起始步 $j$ 构建长度为 $h$ 的局部反向传播链，利用似然比（Likelihood Ratio）技巧和模型固有噪声 $z_j$ 构造无偏梯度估计：

$$- R(x_0) D_{\theta}^{\top} \phi_{j:j+h}(x_{j+h}, z_{j:j+h}; \theta) \nabla_z \ln f(z_j)$$

HO 估计器的核心机制是将 $h$ 步局部链的雅可比与得分函数 $\nabla_z \ln f(z_j)$ 相乘，以无偏方式捕获该尺度下的梯度信息。

**（3）零阶（ZO）估计器**：对剩余时间步，直接向模型参数注入噪声，构造无偏零阶估计，内存消耗极低（约 0.24 GB/步）：

$$- \sum_{i \in C} R(x_0) \nabla_z \ln f(z_i)$$

其中 $C$ 为未被 FO 或 HO 覆盖的剩余步索引集合。

完整 RLR 估计器为上述三项之和：

$$G = \underbrace{D_{\theta}^{\top} \phi(x_1, z_1; \theta) \frac{d R(x_0)}{d x_0}}_{\text{一步一阶估计器}} - \underbrace{R(x_0) D_{\theta}^{\top} \phi_{j:j+h}(x_{j+h}, z_{j:j+h}; \theta) \nabla_z \ln f(z_j)}_{h\text{-步半阶估计器}} - \underbrace{\sum_{i \in C} R(x_0) \nabla_z \ln f(z_i)}_{\text{零阶估计器}}$$

### 子链长度 $h$ 与起点 $j$ 的优化

**子链起点 $j$ 的选择**：基于梯度范数的重要性采样，从类别分布中抽取 $j \sim \text{Softmax}(\|g\|)$，使 HO 子链优先覆盖梯度范数较大的关键步。该选择不影响方差代理目标，但影响多尺度信息的捕获能力。

**子链长度 $h$ 的优化**：通过求解方差-内存约束优化问题得到闭式解。使用 RLR 估计器方差上界作为代理目标：

$$\min_{h \in \mathbb{N}_0 : G(h) \in \mathcal{G}_{\text{RLR}}} \sum_{t=1}^{T} \operatorname{Var}(g_t) + 2 \sum_{t \neq t'} \sqrt{\operatorname{Var}(g_t) \operatorname{Var}(g_{t'})}$$

在内存预算 $\mathcal{B}$ 约束下，最优 $h$ 的闭式解为：

$$h^{*} = \min\left\{\left\lfloor \frac{\mathcal{B} - \mathcal{B}_z (T-1)}{\mathcal{B}_h - \mathcal{B}_z} \right\rfloor, \left\lfloor \frac{T V_z}{2 (V_z - V_h)} - 1 \right\rfloor\right\}$$

其中 $\mathcal{B}_h$ 和 $\mathcal{B}_z$ 分别为 HO 和 ZO 的单步内存成本（实测约 8 GB 和 0.24 GB），$V_h$ 和 $V_z$ 为对应的单步方差。该公式在内存预算与方差降低之间取得平衡：第一项确保不超出内存限制，第二项限制 $h$ 以避免方差边际收益递减。

### 理论性质

RLR 估计器具有严格的无偏性：

$$\nabla_{\theta} \mathbb{E}[R(x_0)] = \mathbb{E}[G_{\text{RLR}}]$$

在 $L$-平滑奖励假设下，RLR 的收敛速率为：

$$\frac{1}{K+1} \sum_{k=0}^{K} \mathbb{E}(\|\nabla R(\theta_k)\|^2) \leq \sqrt{\frac{8 L \Delta_0 \sigma_{\text{RLR}}^2}{K+1}} + \frac{2 L \Delta_0}{K+1}$$

其中 $\sigma_{\text{RLR}}^2$ 为 RLR 估计器的方差。该速率表明，RLR 在保证无偏性的同时，通过降低方差 $\sigma_{\text{RLR}}^2$ 加速收敛。相比之下，截断 BP 引入的结构性偏差为：

$$\nabla_{\theta} \mathbb{E}[R(x_0)] - \mathbb{E}[\nabla_{\theta} R(x_0)_{\text{truncated}}] = \mathbb{E}_{z_{1:T}} \left[ \left( \sum_{i=T'}^{T} \cdots \right) \right] \neq 0$$

该偏差项随截断步数减少而增大，是导致模型崩溃的根本原因（Figure 3）。FO 与 ZO 的方差关系为 $\operatorname{Var}(\nabla_{\theta} R(x_0)) \leq \operatorname{Var}(R(x_0) \nabla \ln f(z))$，说明 FO 天然具有更低方差，RLR 通过 FO + HO 的组合在关键步上利用了这一优势。

## 实验与分析

### 核心瓶颈与因果机制

扩散模型微调面临一个根本性的权衡：截断反向传播（Truncated BP）计算成本低，但引入的结构性偏差会导致模型崩溃——**Figure 3** 清晰地展示了这一现象，当使用截断BP在美学奖励模型上训练 SD 1.4 时，奖励分数随训练步数急剧下降，且截断步数越少，崩溃越严重。强化学习（RL）方法如 **DDPO** 虽然无偏，但方差大、样本效率低。RLR 优化器的核心洞见是将微调形式化为计算预算约束下的最小方差无偏估计问题，通过重组扩散链的计算图为“局部一阶（FO）+ 多步半阶（HO）+ 零阶（ZO）”的组合，在有限内存下实现无偏且低方差的梯度估计。

### 主实验结果

#### 文本到图像生成

**Table 2** 报告了在不同基础模型和奖励模型下的文本到图像生成评估结果。RLR 在多个奖励模型上一致优于基线方法：

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_AZ6lqcvHLX/figures/006_Table_2.jpg]]
*Table 2: Text to Image reward score. We evaluate methods under different DM under different reward models. The higher the score, the better the performance*

- 在 HPD v2 基准上，RLR（SD 1.4）的 PickScore 达到 **21.38**，相比 **Alignprop** 的 19.17 提升 +2.21；AES 分数达到 **6.65**，相比 Alignprop 的 6.02 提升 +0.63。
- 在 SD 2.1 上，RLR 的 PickScore 进一步达到 23.22，持续领先。
- 在 ImageReward 指标上，RLR 同样取得最高分（29.22），显著优于仅使用 ZO 估计的变体（23.66）和移除 HO 的变体（26.70）。

**Figure 5** 的奖励曲线进一步揭示了 RLR 的样本效率优势：在相同训练步数下，RLR 的奖励分数持续上升，而 **Alignprop** 在训练后期出现明显的模型崩溃，奖励分数大幅下降。这表明 RLR 的无偏估计特性从根本上避免了截断BP的偏差累积问题。

#### 文本到视频生成

**Table 3** 展示了在 VBench 基准上的文本到视频生成评估。RLR 的加权平均得分达到 **84.63**，超过所有基线方法，包括 **VADER**（83.45）、**T2V-Turbo**、**DOODL** 以及闭源方法 **Pika** 和 **Gen-2**。特别地，RLR 在动态程度（Dynamic Degree）和美学质量（Aesthetic Quality）指标上以较大幅度领先，证明其在视频生成的时序一致性和视觉质量方面具有显著优势。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_AZ6lqcvHLX/figures/007_Table_3.jpg]]
*Table 3: Text2Video Generation Evaluation on the Vbench. The weighted average is calculated by assigning a weight of 1 to all metrics, except for the Dynamic Degree metric, which is assigned a weight of 0.5*

**Table 10** 提供了 VBench 的完整自动评估指标，涵盖质量维度和语义维度，进一步验证了 RLR 在多个子指标上的稳健表现。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_AZ6lqcvHLX/figures/022_Table_10.jpg]]
*Table 10: Automatic evaluation on VBench. (a) Quality dimensions and total score*

### 消融实验

**Table 5** 的消融实验严格验证了 RLR 各组件的必要性：

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_AZ6lqcvHLX/figures/012_Table_5.jpg]]
*Table 5: Ablation of the RLR*

- **移除 HO 和 ZO（仅保留单步 BP）**：性能大幅下降，PickScore 从 21.38 降至 18.43，ImageReward 从 29.22 降至 23.66，AES 从 6.65 降至 5.78。这证明仅靠最后一步的精确反向传播远不足以捕获扩散链中的多尺度梯度信息。
- **移除 ZO（仅 FO + HO）**：变为有偏估计，PickScore 降至 20.11，ImageReward 降至 27.07，AES 降至 6.23。这表明 ZO 组件的无偏性保障对最终性能至关重要——缺少 ZO 意味着剩余步骤的梯度信息完全丢失，等价于一种隐式的截断偏差。
- **子链长度 h 的影响**：**Table 9** 显示，增加 h 可在一定程度上提升奖励分数，但当 h > 2 时增益趋于饱和，同时内存和时间开销显著增长（HO 每步内存约 8GB，ZO 仅 0.24GB）。这验证了 RLR 通过优化 h 来平衡方差与内存的理论设计。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_AZ6lqcvHLX/figures/021_Table_9.jpg]]
*Table 9: Comparison of methods on HPSv2 and ImageReward with memory(GB) and time cost(minute per step)*

**Table 8** 的扩散求解器消融表明，RLR 在不同求解器（DDIM、DPM-Solver 等）下均保持一致的性能优势，证明方法对采样器选择具有鲁棒性。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_AZ6lqcvHLX/figures/020_Table_8.jpg]]
*Table 8: Ablation of different diffusion solver in Text2Image experiments on SD 1.4*

### 资源效率分析

**Table 6** 和 **Table 7** 分别报告了 Text2Image 实验的内存占用和时间复杂度。RLR 通过 ZO 组件将大部分步骤的内存开销降至极低水平（0.24GB/步），仅在局部 HO 子链上付出较高的内存成本（8GB/步），实现了在有限预算下的最优配置。相比需要全链反向传播的方法，RLR 在保持无偏性的同时显著降低了峰值内存需求。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_AZ6lqcvHLX/figures/018_Table_6.jpg]]
*Table 6: Memory cost of Text2Image experiments on SD 1.4*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_AZ6lqcvHLX/figures/019_Table_7.jpg]]
*Table 7: Time complexity of Text2Image experiments on SD 1.4*

### 失败模式与局限性

1. **子链长度 h 的确定**：最优 h 依赖于对内存预算和方差特性的估计（见公式 $h^{*}$），实践中可能需要启发式调整，尤其在硬件配置变化时。
2. **奖励模型依赖性**：微调效果受预训练奖励模型质量的制约，若奖励模型存在偏好偏差，RLR 会忠实地优化该偏差，可能导致生成结果的系统性偏向。
3. **大规模模型的扩展性**：计算时间仍随 h 线性增长，在十亿参数级扩散模型上的开销需要进一步评估。
4. **子链起点 j 的选择**：当前基于梯度范数的重要性采样策略在多数任务中有效，但对于需要精确控制多尺度生成的任务（如 DCoT），需要人工指定 j 的采样范围，自适应机制尚不完善。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_AZ6lqcvHLX/figures/005_Table_1.jpg]]
*Table 1: Comparison of gradient estimators*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_AZ6lqcvHLX/figures/011_Table_4.jpg]]
*Table 4: Experiment results for Diffusive Chainof-Thought*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_AZ6lqcvHLX/figures/016_Figure_10.jpg]]
*Figure 10: Qualitative examples for DCoT prompts*

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

扩散模型微调方法长期受困于梯度估计的偏差-方差-计算成本权衡。现有方案主要分为两条路线：**截断反向传播**（Truncated BP）和**强化学习**（RL）。截断BP（例如 **Alignprop**）通过仅展开扩散链的最后几步来降低计算开销，但这引入了结构性偏差。实验证据表明，该偏差在训练后期会导致模型崩溃——奖励分数在达到峰值后急剧下降（Figure 3），且截断步数越少，崩溃越严重。另一条路线以 **DDPO** 为代表的RL方法，虽然能保证无偏性，但梯度估计方差极大，样本效率低下。

RLR优化器将这一问题形式化为**计算预算约束下的最小方差无偏估计问题**：

$$\min_{G \in \mathcal{G}} \operatorname{Var}(G) \quad \text{s.t.} \quad \nabla_{\theta} \mathbb{E}[R(x_0)] = \mathbb{E}[G], \quad \mathcal{C}(G) \leq \mathcal{B}$$

这一形式化为理解各方法在谱系中的位置提供了统一框架。

### 方法谱系：从全阶到半阶

从梯度估计器对扩散链的计算图覆盖范围来看，现有方法可沿“阶数”维度排列：

| 方法类别 | 代表工作 | 计算图范围 | 无偏性 | 方差 | 内存 |
|---------|---------|-----------|--------|------|------|
| 全阶BP | 标准反向传播 | 全部T步 | 无偏 | 低 | 极高 |
| 截断BP | Alignprop, VADER | 最后k步 | 有偏 | 低 | 中 |
| 强化学习 | DDPO | 不展开链 | 无偏 | 高 | 低 |
| 半阶微调 | **RLR (本文)** | 局部h步HO + 1步FO + ZO | 无偏 | 低 | 可控 |

RLR的核心创新在于**重组计算图**：将扩散链拆解为一步精确反向传播（FO）、一段长度为h的局部似然比子链（HO），以及剩余步的参数扰动零阶估计（ZO）。这一设计使RLR既保留了局部链的低方差优势，又通过ZO组件补偿了截断带来的偏差，从而在理论上严格保证了无偏性（Theorem 6.3）：

$$\nabla_{\theta} \mathbb{E}[R(x_0)] = \mathbb{E}[G_{RLR}]$$

### 与基线方法的关键差异

**相对于截断BP方法（Alignprop, VADER）**：截断BP仅对最后几步计算精确梯度，丢弃了早期步骤的梯度信号。RLR通过HO子链的随机起始点j和ZO组件，覆盖了完整扩散链的信息，从根本上避免了结构性偏差。实验直接验证了这一优势：在相同训练步数下，RLR的奖励曲线持续上升，而Alignprop在后期发生模型崩溃（Figure 5）。

**相对于RL方法（DDPO）**：DDPO将整个生成过程视为黑箱，仅依赖最终奖励信号进行策略梯度估计，方差随扩散步数线性增长。RLR利用扩散模型内部的高斯噪声结构，在HO子链上构造似然比估计器，显著降低了方差。理论上，RLR的方差上界为：

$$\operatorname{Var}(RLR) \leq \sum_{t} \operatorname{Var}(g_t) + 2 \sum_{t \neq t'} \sqrt{\operatorname{Var}(g_t) \operatorname{Var}(g_{t'})}$$

其中$g_t$为各步的局部估计器方差，FO组件的方差显著低于ZO组件，HO组件介于两者之间。

### 组件消融与因果验证

消融实验（Table 5）明确揭示了各组件的因果贡献：

- **移除HO和ZO（仅保留单步BP）**：退化为极度截断的有偏估计，在所有奖励模型上性能最差。例如在PickScore上从21.38降至18.43，ImageReward从29.22降至23.66。这验证了覆盖多步信息对于微调效果的必要性。
- **移除ZO（仅FO+HO）**：变为有偏估计，性能明显低于完整RLR（PickScore: 20.11 vs 21.38）。这直接证明了无偏性对于避免模型崩溃的关键作用。
- **子链长度h的影响**：增加h可在一定程度上提升奖励分数，但当h>2时增益趋于饱和，同时内存和时间开销显著增长（Table 9）。这支持了RLR设计中选择适度h的合理性。

### 适用边界与局限

1. **子链长度的实践困难**：最优h的闭式解依赖内存预算估计$B_h$和$B_z$，实践中这些参数可能因硬件和模型架构而异，需要启发式调整。论文明确指出“Determining the appropriate subchain length h can be nontrivial in practice”。

2. **模型规模的可扩展性**：当前实验验证集中在SD1.4/SD2.1规模（约860M参数）和VideoCrafter等模型。RLR是否适用于十亿参数级扩散模型（如SDXL、Flux等）尚待验证。计算时间随h线性增长，在大规模模型上可能成为瓶颈。

3. **奖励模型的依赖性**：微调效果依赖于预训练奖励模型的质量。若奖励模型存在偏好偏差（如过度偏好特定美学风格），RLR会忠实地最大化该偏差，可能导致生成多样性下降。论文未对此进行系统消融。

4. **架构泛化性**：方法目前仅在扩散生成模型上验证。其核心思想——在递归计算图中用局部精确链+零阶补偿实现无偏低方差估计——在理论上面向更广泛的递归架构（如自回归模型），但推广需要进一步研究。

### 开放问题

- RLR能否与策略梯度方法（如PPO）结合，直接在文本到视频的在线RL环境中使用？
- 如何自适应地为不同任务和提示词选择子链起始点j的分布，而非依赖固定的梯度范数重要性采样？
- 在更大规模模型上，FO+HO+ZO的内存分配策略是否需要重新优化？
- 将DCoT的多尺度提示分解思想推广到其他生成任务（如3D生成、音频生成）的可行性。

## 原文 PDF

![[paperPDFs/ICLR_2026/Half_order_Fine_Tuning_for_Diffusion_Model_A_Recursive_Likelihood_Ratio_Optimizer.pdf]]
