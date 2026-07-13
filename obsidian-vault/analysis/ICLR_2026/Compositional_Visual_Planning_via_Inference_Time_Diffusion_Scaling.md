---
title: "Compositional Visual Planning via Inference-Time Diffusion Scaling"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Compositional_Visual_Planning_via_Inference_Time_Diffusion_Scaling.pdf
project_link: https://comp-visual-planning.github.io/
code_link: null
openreview_forum_id: EEONns7ae4
aliases:
- CVPITDS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "在扩散模型的Tweedie（去噪）估计上强制边界一致性，而非在噪声中间状态上操作。"
primary_logic: "将长序列规划建模为链式因子图上的推理，利用预训练短片段扩散模型作为局部先验，在推理时通过同步与异步消息传递在Tweedie估计上强制边界一致，配合扩散球体引导实现无需额外训练的长序列视觉规划。"
claims:
- "Bethe近似在扩散噪声状态下不成立，存在Noisy-Bethe间隙，导致分数平均组合不稳定。"
- "在Tweedie估计上进行边界一致性能有效解决组合不稳定性。"
- "同步与异步消息传递结合扩散球体引导，相比单独使用任何一方均能提升规划成功率。"
- "方法在分布外（OOD）起止组合上显著优于DiffCollage等基线。"
---

# Compositional Visual Planning via Inference-Time Diffusion Scaling

> [!tip] 核心洞察
> 将长序列规划建模为链式因子图上的推理，利用预训练短片段扩散模型作为局部先验，在推理时通过同步与异步消息传递在Tweedie估计上强制边界一致，配合扩散球体引导实现无需额外训练的长序列视觉规划。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于推理时扩散缩放的组合视觉规划 |
| 英文题名 | Compositional Visual Planning via Inference-Time Diffusion Scaling |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=EEONns7ae4) · [Project](https://comp-visual-planning.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Compositional Visual Planning via Inference-Time Diffusion Scaling |
| Dataset | Overall Scenes (IND), Overall Scenes (OOD), Overall (IND), Overall (OOD) |

> [!tip] 效果简介
> - Overall Scenes (IND) 上，Imaging Quality 为 0.70±0.03，对比 0.60±0.05 (DiffCollage)，变化 +0.10。
> - Overall Scenes (OOD) 上，Motion Smoothness 为 0.97±0.05，对比 0.87±0.06 (DiffCollage)，变化 +0.10。
> - Overall (IND) 上，Success Rate (%) 为 59±17，对比 0±1 (DiffCollage)，变化 +59。

## 概要

长序列视觉规划的核心瓶颈在于**组合泛化**：如何将预训练于短片段上的扩散模型在推理时组合成未见过的长序列计划，而无需额外训练。现有组合扩散方法（如 **DiffCollage**，Zhang et al., 2023）直接在噪声数据空间上假设因子分解的独立性，但噪声破坏了这种独立性——本文通过 **Noisy-Bethe 间隙定理**（Theorem 1）严格证明了这一点，导致分数平均组合不稳定、全局计划不一致。

本文提出 **Compositional Visual Planning via Inference-Time Diffusion Scaling**，核心洞察是：**将一致性约束从噪声中间状态迁移到 Tweedie（去噪）估计上**。具体而言，将长序列规划建模为链式因子图上的推理，利用预训练短片段视频扩散模型作为局部先验，在推理时通过同步与异步消息传递在 Tweedie 估计上强制边界一致性，并配合**扩散球体引导**实现免额外训练的采样。

主要结果：
- 在分布外（OOD）起止组合上，规划成功率从 DiffCollage 的 **0%** 提升至 **54%**（Table 2）。
- 真实机器人实验中，OOD 任务成功率达 **10/10**，而 DiffCollage 为 **0/10**（Table 3）。
- 消融实验证实，同步与异步消息传递结合扩散球体引导，显著优于单独使用任一方（Figure 4）。

方法的关键局限性在于依赖 Tweedie 估计的准确性（去噪早期阶段估计可能不准），且测试时需手动指定组合片段数量，梯度优化引导也带来更高的推理计算开销。



长序列视觉规划是机器人操作与视频生成领域的核心挑战。传统方法依赖端到端的行为克隆或扩散策略，在训练分布内表现良好，但面对未见过的起始-目标组合时泛化能力急剧下降。这是因为长序列数据的组合空间呈指数级增长，完全覆盖所有可能组合的训练数据在实际中不可行。

一种自然的解决思路是将长序列分解为多个短片段，在推理时重新组合。现有组合扩散方法——以 **DiffCollage**（Generative Skill Chaining, Zhang et al., 2023）为代表——采用 Bethe 近似在噪声扩散状态 $x_t$ 上对短片段分数进行平均，从而生成完整计划。然而，这一策略存在根本性的理论缺陷。

**核心瓶颈：Noisy-Bethe 间隙。** Bethe 近似假设因子图中的变量在给定条件下满足独立性，但这一假设在噪声数据空间上被系统性破坏。扩散过程中的加噪操作引入了变量间的伪相关，导致真实联合分布与 Bethe 估计之间产生不可忽略的偏差。该文将此偏差形式化为 **Noisy-Bethe 间隙定理**（Theorem 1），证明真分布与 Bethe 估计的差距等于缩放后的协方差项：

$$\Delta = Z \operatorname{Cov}_{u^2 \sim q} \left[ \frac{a}{c}, \frac{b}{c} \right]$$

这一间隙直接导致分数平均的组合不稳定：在圆弧组合的 toy 实验中（Figure 2），DiffCollage 生成的“花瓣”出现明显漂移，无法形成闭合环路，而本文方法成功实现了精确的边界对齐。

**动机：从噪声域转向去噪域。** 上述分析揭示了一个关键洞察：组合一致性的约束不应施加在噪声中间状态上，而应施加在扩散模型的 **Tweedie（去噪）估计** $x_{0|t}$ 上。Tweedie 估计是对干净数据的单步预测，其统计特性更接近真实数据分布，因此边界一致性约束在该空间上具有更好的理论保证。

基于这一洞察，该文将长序列规划重新建模为链式因子图上的推理问题：将重叠的视频块视为因子，首尾帧锚定为起始与目标，相邻因子通过共享的过渡边界变量交换信息。在推理时，通过同步与异步消息传递在 Tweedie 估计上强制边界一致，配合扩散球体引导，实现无需额外训练的长序列视觉规划。整个过程是即插即用的：短片段扩散模型只需训练一次并冻结，测试时可泛化至任意未见过的起始-目标组合。



## 核心方法与创新机理

本文提出**基于推理时扩散缩放的组合视觉规划**，其核心创新在于将组合扩散的约束域从**噪声中间状态**迁移至**Tweedie（去噪）估计**，并通过**同步与异步消息传递**在推理时强制边界一致性，配合**扩散球体引导**实现免额外训练的长序列规划。

### 关键创新点

**1. 组合域迁移：从噪声状态到去噪估计**

现有组合扩散方法（如 **DiffCollage** / Generative Skill Chaining, Zhang et al., 2023）基于Bethe近似在噪声数据空间 $x_t$ 上假设因子分解成立，直接对噪声分数进行平均组合。本文揭示了这一范式的根本缺陷——**Noisy-Bethe间隙定理**（Theorem 1, Eq. 8）：噪声破坏了因子间的独立性假设，导致Bethe近似与真实分布之间存在由协方差项量化的系统性偏差 $\Delta = Z \operatorname{Cov}_{u^2 \sim q} [a/c, b/c]$，使得分数平均组合不稳定，全局计划缺乏一致性（图2中DiffCollage的漂移示例）。

本文的核心洞察是：**在Tweedie估计 $x_{0|t}$ 上强制边界一致性，而非在噪声中间状态 $x_t$ 上操作**。具体而言，将因子图联合分布建模为：

$$p(z_t) = \prod_{i=1}^n p(x_t^i) \cdot \exp(-L(x_{0|t}^{1:n}))$$

其中一致性势函数 $L$ 作用于所有因子的去噪估计拼接 $x_{0|t}^{1:n}$，而非噪声状态（Eq. 9）。这一设计从根本上规避了Noisy-Bethe间隙，使组合过程在语义清晰的去噪空间中进行。

**2. 一致性约束机制：同步与异步消息传递**

区别于DiffCollage的Bethe近似乘积归一化，本文设计了两类消息传递损失来强制边界一致性：

- **同步消息传递**（Eq. 11）：将边界约束（起止锚定 $A_1 x^1 = s, B_n x^n = g$、相邻过渡 $B_i x^i = A_{i+1} x^{i+1}$）构造为高斯线性系统 $L_{sync} = \| \Sigma^{-1} x_{0|t}^{1:n} - \eta \|$，驱动全局残差至零。
- **异步消息传递**（Eq. 12）：采用自举目标和停止梯度进行前后向传递，前向从起始帧向后传播一致性，后向从目标帧向前传播，并通过折扣因子 $\gamma$ 衰减远端消息权重，提升收敛速度和稳定性。

消融实验（图4）证实：同步与异步的联合使用（Sync & Async）显著优于单独使用任一方，原因在于二者在约束强制与灵活性之间达成了更有效的平衡。

**3. 推理时引导：扩散球体引导**

DiffCollage等基线在推理时无额外引导或仅基于噪声分数的引导。本文引入**扩散球体引导**（DSG, Eq. 6），将消息传递损失梯度 $\nabla_{x_t} L(x_{0|t})$ 归一化后，与无条件DDIM采样方向进行插值：

$$d_m = d^{sample} + g_r (d^* - d^{sample}), \quad d^* = -\sqrt{s} \sigma_t \cdot \frac{\nabla_{x_t^{1:n}} L}{\|\nabla_{x_t^{1:n}} L\|}$$

该设计消除了点估计与期望之间的间隙，在保持生成多样性的同时提升边界一致性。

**4. 训练范式：完全免额外训练**

与CompDiffuser等需要测试时联合去噪的训练式方法不同，本文的短片段扩散模型仅需一次训练后冻结，推理时通过上述消息传递与DSG引导实现任意长度的组合规划，无需任何额外训练或微调。

### 证据强度

| 创新点 | 关键证据 | 置信度 |
|--------|----------|--------|
| 组合域迁移 | Theorem 1 Noisy-Bethe间隙定理；图2 DiffCollage漂移 vs 本文闭环成功 | 0.95 |
| 同步+异步消息传递 | 图4消融：Sync & Async > Async Only > Sync Only | 0.95 |
| 扩散球体引导 | OOD成功率 54±14 vs DiffCollage 0±0（表2）；真实机器人OOD 10/10 vs 0/10（表3） | 0.98 |
| 免额外训练 | 方法描述：短片段模型一次训练后冻结，测试时完全免训练 | 0.90 |



![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_EEONns7ae4/figures/002_Figure_1.jpg]]
*Figure 1: Compositional Visual Planning via Inference Time Diffuser Scaling. We train a short-horizon visual diffusion model on clips treated as a single factor. At inference, we scale visual planning horizon without retraining by chaining overlapping factors into a linear factor graph: the start and goal boundary variables are anchored at the ends, while neighboring factors exchange information through shared transition boundary variables*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_EEONns7ae4/figures/010_Figure_6.jpg]]
*Figure 6: Hardware Setup. We deploy our method on a Franka Emika Panda robot*

本文提出了一种名为 **Compositional Visual Planning via Inference-Time Diffusion Scaling** 的组合视觉规划方法。其核心思想是将长序列规划建模为链式因子图上的推理问题，利用预训练的短片段视频扩散模型作为局部先验，在推理时通过消息传递机制在去噪估计上强制边界一致性，从而实现无需额外训练的长序列视觉规划。

### Pipeline 总览

整个系统由训练阶段和推理阶段两部分构成，其输入输出流如下：

**训练阶段**（仅需执行一次）：
1. 从长序列演示数据中随机采样短片段（chunks），每个片段包含连续三帧。
2. 在 Cosmos tokenizer 编码的紧凑潜在空间上训练一个无条件视频扩散模型，该模型学习短片段内的局部运动先验。
3. 训练一个逆动力学模型，用于将生成的连续视频帧转换为机器人末端执行器动作。

**推理阶段**（对任意起止组合免训练）：
1. **因子图构造**：给定起始帧 $s$ 和目标帧 $g$，将长序列分解为 $n$ 个重叠的因子 $x^i$，每个因子包含三帧 $[\bar{u}^{2i-1}, u^{2i}, u^{2i+1}]$，相邻因子共享一个过渡边界变量。
2. **扩散采样初始化**：对所有因子并行执行 DDIM 采样，每个因子从纯噪声开始，逐步去噪。
3. **Tweedie 估计**：在每个扩散步 $t$，计算每个因子的去噪预测 $x_{0|t}$。
4. **消息传递**：在 $x_{0|t}$ 上计算同步消息传递损失 $L_{sync}$ 和异步消息传递损失 $L_{async}$，强制边界一致性约束。
5. **扩散球体引导（DSG）**：将消息传递损失梯度与无条件采样方向插值，在球面高斯约束下更新 $x_{t-1}$。
6. **重复步骤 3-5**，直至 $t=0$，得到完整的视频帧序列。
7. **动作执行**：将生成的视频帧输入逆动力学模型，输出机器人动作序列。

### 模块关系

下图（对应原文 Figure 1）展示了各模块之间的依赖关系：

```
训练阶段:
  长序列演示 → 随机采样短片段 → Cosmos 编码 → 训练扩散模型（局部先验）
                                          → 训练逆动力学模型

推理阶段:
  s, g → 因子图构造 → 并行 DDIM 初始化
                         ↓
              ┌── Tweedie 估计 x_{0|t} ──┐
              ↓                          ↓
         同步消息传递 L_sync      异步消息传递 L_async
              └──────────┬───────────────┘
                         ↓
                  扩散球体引导 (DSG)
                         ↓
                    x_{t-1} 更新
                         ↓
              (循环至 t=0) → 视频帧序列 → 逆动力学模型 → 动作
```

### 关键设计决策

1. **组合域的选择**：与 DiffCollage 等基线在噪声状态 $x_t$ 上进行分数平均不同，本方法在 Tweedie 估计 $x_{0|t}$ 上强制边界一致性。这一设计源于 **Noisy-Bethe 间隙定理**（Theorem 1）：在噪声数据空间上，Bethe 近似的因子分解假设不成立，噪声破坏了独立性，导致组合不稳定。通过在去噪估计上操作，有效规避了这一问题。

2. **双消息传递机制**：同步消息传递将边界一致性建模为高斯线性系统 $\Sigma^{-1} x_{0|t}^{1:n} = \eta$，驱动全局残差至零；异步消息传递采用自举目标和停止梯度进行前后向传递，提升稳定性和收敛速度。消融实验表明，二者结合显著优于单独使用任一方。

3. **扩散球体引导**：将消息传递损失梯度与无条件采样方向插值，在球面高斯约束下进行更新，平衡了边界一致性与生成多样性，同时消除了点估计与期望之间的间隙。

4. **潜在空间规划**：所有因子和变量均在 Cosmos tokenizer 编码的紧凑潜在空间中操作，而非像素空间，显著降低了维度并节省了计算开销。



### 问题形式化：链式因子图上的推理

本文方法将长序列视觉规划建模为链式因子图上的推理问题。规划序列 $z = [u^1, \dots, u^m]$ 由 $m$ 个边界变量组成，$n$ 个重叠的短片段因子 $x^i$ 各覆盖三个连续帧：

$$x^i = [\bar{u}^{2i-1}, u^{2i}, u^{2i+1}], \quad i = 1, \dots, n$$

其中相邻因子共享一个过渡边界变量（如 $u^3$ 同时属于 $x^1$ 和 $x^2$）。规划的可行性由两类边界一致性约束保证：

- **起止锚定**：$A_1 x^1 = s,\; B_n x^n = g$，将链的首尾帧固定到给定的起始帧 $s$ 和目标帧 $g$。
- **过渡边界**：$B_i x^i = A_{i+1} x^{i+1},\; i = 1, \dots, n-1$，强制相邻片段在共享边界帧上一致。

所有因子和变量均在 Cosmos tokenizer 编码的紧凑潜空间中操作，以降低维度并节省计算开销。

### 核心瓶颈：Noisy-Bethe 间隙

现有组合扩散方法（如 DiffCollage）在噪声数据空间上假设因子分解成立，利用 Bethe 近似表示联合分布：

$$p(z_t) := \frac{\prod_{i=1}^n p(x_t^i)}{\prod_{j=1}^m p(u_t^j)^{d_j-1}}$$

其中 $d_j$ 是变量 $u^j$ 的度。但噪声破坏了变量间的独立性，导致真分布与 Bethe 估计之间存在系统性偏差。**定理 1（Noisy-Bethe 间隙定理）** 证明该偏差可表达为缩放后的协方差：

$$\Delta = Z \operatorname{Cov}_{u^2 \sim q} \left[ \frac{a}{c}, \frac{b}{c} \right]$$

这一间隙导致分数平均的组合方式不稳定，全局计划不一致（如图 2 中 DiffCollage 在圆弧组合任务上的漂移所示）。

### 关键创新：在 Tweedie 估计上强制边界一致性

为解决上述瓶颈，本文的核心操作是将一致性约束从噪声状态 $x_t$ 转移到去噪估计 $x_{0|t}$（即 Tweedie 估计）上。因子图的联合分布重新定义为：

$$p(z_t) = \prod_{i=1}^n p(x_t^i) \cdot \exp(-L(x_{0|t}^{1:n}))$$

其中 $L(x_{0|t}^{1:n})$ 是施加在拼接 Tweedie 估计上的边界一致性势函数。这一设计的直觉在于：Tweedie 估计是对干净数据的预测，噪声干扰已被消除，因此边界一致性假设在 $x_{0|t}$ 上更接近成立。

### 消息传递损失

边界一致性通过两类消息传递损失实现，均在每个扩散步的 Tweedie 估计上计算。

**同步消息传递损失**将一致性约束建模为高斯线性系统 $\Sigma^{-1} x_{0|t}^{1:n} = \eta$，损失为偏离该系统的范数：

$$L_{sync} = \| \Sigma^{-1} x_{0|t}^{1:n} - \eta \|$$

该损失同时考虑所有因子间的约束，理论上等价于联合高斯推断，但收敛可能较慢。

**异步消息传递损失**采用自举目标和停止梯度（stop-gradient），沿链进行前向与后向传递，类似时序差分更新：

$$L_{async} = \underbrace{\| s - A_1 x_{0|t}^1 \| + \sum_{i=1}^{n-1} \gamma^i \| sg(B_i \hat{x}_{0|t}^i) - A_{i+1} x_{0|t}^{i+1} \|}_{\text{forward passing}} + \underbrace{\sum_{i=1}^{n-1} \gamma^{n-i} \| B_i x_{0|t}^i - sg(A_{i+1} \hat{x}_{0|t}^{i+1}) \| + \| B_n x_{0|t}^n - g \|}_{\text{backward passing}}$$

其中 $\gamma$ 为折扣因子，使远离起点/目标的消息权重递减；$sg(\cdot)$ 阻止梯度回传，实现单向消息传播。消融实验（图 4）表明，同步与异步消息传递组合（Sync & Async）显著优于单独使用任一方。

### 扩散球体引导（DSG）

消息传递损失通过免训练引导机制集成到 DDIM 采样过程中。将条件分布建模为势函数，梯度更新简化为对 Tweedie 估计的梯度下降：

$$\nabla_{x_t} \log p(y|x_t) = -\nabla_{x_t} L(x_{0|t})$$

为平衡一致性约束与生成多样性，DSG 在无条件采样方向与归一化损失梯度之间进行插值：

$$d_m = d^{sample} + g_r (d^* - d^{sample}), \quad x_{t-1}^{1:n} = \mu_{t-1}^{1:n} + r \frac{d_m}{\|d_m\|}$$

其中 $d^* = -\sqrt{s} \sigma_t \cdot \frac{\nabla_{x_t^{1:n}} L}{\|\nabla_{x_t^{1:n}} L\|}$ 为归一化最陡下降方向，$g_r$ 为引导权重。该形式消除了点估计与期望之间的间隙，在球面高斯约束下给出闭式解。

### 执行：逆动力学模型

生成的视频帧通过预训练的逆动力学模型转换为机器人末端动作，该模型从连续帧预测动作。整个过程在短片段扩散模型一次训练后冻结，测试时完全免额外训练。



## 实验与关键发现

### 核心瓶颈与因果机制

现有组合扩散方法（如 **DiffCollage** (Zhang et al., 2023)）在噪声扩散状态 $x_t$ 上直接施加因子分解假设，但噪声破坏了变量间的独立性，导致组合不稳定、全局计划不一致。本文通过 **Noisy-Bethe 间隙定理**（Theorem 1，式(8)）严格证明了这一点：真实分布与 Bethe 估计之间的差距 $\Delta$ 正比于缩放后的协方差 $\Delta = Z \operatorname{Cov}_{u^2 \sim q} \left[ \frac{a}{c}, \frac{b}{c} \right]$，这意味着在噪声域上做分数平均天然存在结构性偏差。

本文的关键因果旋钮是将边界一致性约束从噪声中间状态转移到 **Tweedie（去噪）估计** $x_{0|t}$ 上（式(9)），在扩散模型的“干净”预测空间而非噪声空间上操作，从而绕开了 Noisy-Bethe 间隙。在此基础上，同步与异步消息传递损失（式(11)-(12)）在因子图链上强制边界一致性，配合扩散球体引导（式(6)）平衡约束与多样性，实现了无需额外训练的长序列视觉规划。

### 视频生成质量（Table 1）

在四个场景（Tool-Use, Drawer, Cube, Puzzle）上评估动态与静态生成质量，所有指标基于 5 个随机种子取均值±标准差。**Table 1** 的核心结论：

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_EEONns7ae4/figures/007_Table_1.jpg]]
*Table 1: Comparison across four scenes on Dynamic/Static Quality. Our results are averaged over 5 seeds and standard deviations are shown after the ± sign*

- **运动平滑度（Motion Smoothness）**：在分布外（OOD）设置下，本文方法达到 **0.97±0.05**，DiffCollage 为 0.87±0.06（+0.10），说明 Tweedie 域上的边界一致性能有效消除帧间跳变。
- **成像质量（Imaging Quality）**：在分布内（IND）设置下，本文方法 **0.70±0.03** vs DiffCollage 0.60±0.05（+0.10），表明消息传递机制在保持视觉保真度方面具有一致优势。
- 背景一致性与美学指标同样全面优于 DiffCollage，验证了扩散球体引导在平衡约束与多样性方面的有效性。

### 组合规划成功率（Table 2）

在 100 个测试任务（4 个场景 × 30 episodes/任务）上的规划成功率是本文最关键的实验证据：

- **分布内（IND）**：本文方法 Overall **59±17%**，DiffCollage 仅为 0±1%。在 Tool-Use 场景达到 97%，Puzzle 场景 50%，表明方法在训练分布内已能稳定组合短片段模型。
- **分布外（OOD）**：本文方法 Overall **54±14%**，DiffCollage **0±0%**。这一 54 个百分点的绝对差距是本文最有力的因果证据——在噪声域上做分数平均的 DiffCollage 完全无法泛化到未见过的起止组合，而 Tweedie 域上的消息传递机制具备真正的组合泛化能力。
- 与训练式基线 CompDiffuser 相比，本文方法在多数场景仍显著领先，且完全免训练，验证了推理时优化的实用价值。

### 真实机器人验证（Table 3, Figure 6）

在 **Franka Emika Panda** 机器人（Figure 6）上部署，评估 4 个任务（2 IND + 2 OOD），每次任务 10 次试验：

- **IND Task1**：本文 **9/10** vs DiffCollage 1/10；**IND Task2**：**7/10** vs 1/10。
- **OOD Task3**：本文 **10/10** vs DiffCollage **0/10**；**OOD Task4**：**8/10** vs 0/10。

OOD Task3 的 10/10 完美成功率与 DiffCollage 的 0/10 形成极端对比，强有力地证明了 Tweedie 域边界一致性机制在真实物理环境中的鲁棒性。DiffCollage 在 OOD 任务上的完全失败与其在噪声域上做 Bethe 近似的理论缺陷一致。

### 消融实验（Figure 4, Figure 5）

**消息传递机制消融（Figure 4）**：
- 单独使用同步消息传递（Sync Only）或异步消息传递（Async Only）均不如二者组合（Sync & Async）。
- 组合方案在成功率和稳定性上均最优，验证了同步损失提供全局一致性约束、异步损失通过自举目标加速收敛的互补机制。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_EEONns7ae4/figures/009_Figure_4.jpg]]
*Figure 4: Effect of synchronous and asyn- Figure 5: Effect of sampling steps on planning perforchronous message passing. mance*

**采样步数消融（Figure 5）**：
- 规划成功率随扩散采样步数增加而单调提升，表明方法能有效利用额外的推理时计算资源。
- 这一定性趋势与扩散球体引导在每个 DDIM 步上插值损失梯度的设计一致——更多步数意味着更精细的边界一致性优化。

**折扣因子消融（Appendix I, Figure 15-16）**：
- 去除折扣因子 $\gamma$ 会导致起始帧/目标帧出现细微空间错位，尽管总体运动仍连贯。
- 这表明异步消息传递中的折扣机制对于精确锚定首尾帧至关重要。

### 推理效率（Table 5）

本文方法的推理时间高于 DiffCollage（例如 Tool-Use 场景 3 个组合模型：本文 30.6s vs DiffCollage 7.8s），这是梯度优化引导的固有代价。但这一开销换来了 OOD 场景下 54% vs 0% 的成功率差距，在真实机器人任务中更是 10/10 vs 0/10，计算开销在组合泛化能力的收益面前是合理的。

### 公平性说明

所有实验使用固定超参数（Table 4），未进行超参数搜索，超参数跨不同场景保持一致。结果基于 5 个不同随机种子的均值与标准差报告，确保了比较的公平性和统计可靠性。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_EEONns7ae4/figures/016_Table_4.jpg]]
*Table 4: Relevant hyperparameters used in our experiments*

### 已知局限

1. **Tweedie 估计依赖性**：在去噪早期阶段，Tweedie 估计 $x_{0|t}$ 可能不准确，此时边界一致性约束的效果受限。
2. **手动指定片段数**：测试时需要人工指定组合片段数量 $n$，缺乏从任务结构自动推断的机制。
3. **推理计算开销**：梯度优化引导导致推理时间高于直接平均采样方法（Table 5），在实时性要求高的场景中可能需要优化。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_EEONns7ae4/figures/017_Table_5.jpg]]
*Table 5: Sampling time during deployment. This is measured as the mean wall-clock time across all samples within a single scene*

### 补充图表

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_EEONns7ae4/figures/005_Figure_2.jpg]]
*Figure 2: Motivating toy example. We train a short-horizon diffusion model on circular arc clips (left). At test time, three 1 2 $0 ^ { \circ }$ arc generators are composed to form a three-petal “flower”*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_EEONns7ae4/figures/008_Table_2.jpg]]
*Table 2: Quantitative Results on Compositional Planning Bench. We benchmark our method on the 100 test-time tasks across 4 scenes with 30 episodes per task. Our results are averaged over 5 seeds and standard deviations are shown after the ± sign*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_EEONns7ae4/figures/011_Table_3.jpg]]
*Table 3: Real-robot success rates. Our method substantially outperforms DiffCollage across both in-distribution (IND) and out-of-distribution (OOD) tasks on real hardware*



## 定位与知识库关联

### 1. 与组合扩散方法的对比定位

本文方法的核心差异在于**组合域的选择**：现有组合扩散方法（以 **DiffCollage** / Generative Skill Chaining, Zhang et al., 2023 为代表）在噪声数据空间 $x_t$ 上假设因子分解成立，通过 Bethe 近似对分数进行加权平均来组合短片段。本文通过 **Noisy-Bethe 间隙定理**（Theorem 1, 式 8）揭示了这一做法的根本缺陷——噪声破坏了变量间的独立性，导致 Bethe 近似在扩散中间态上不成立，组合结果出现漂移和不一致（图 2 的 DiffCollage 示例）。

本文的解决方案是将边界一致性约束从噪声状态 $x_t$ 转移到 **Tweedie（去噪）估计** $x_{0|t}$ 上（式 9），从而绕开 Noisy-Bethe 间隙。这一设计使得组合稳定性得到根本性改善，在分布外（OOD）起止组合上，本文方法成功率达 54±14%，而 DiffCollage 为 0±0%（表 2）；真实机器人 OOD 任务中差距更为悬殊（10/10 vs 0/10，表 3）。

与 **CompDiffuser** 等训练式联合去噪基线不同，本文的短片段扩散模型仅需一次训练后冻结，测试时完全免额外训练，属于推理时缩放（inference-time scaling）范式。

### 2. 与行为克隆和扩散策略的关系

本文与四类直接策略学习方法形成对比：

- **LCBC**（Language-Conditioned Behavioral Cloning）：使用 T5 文本编码器和 MLP 策略头，直接从语言指令映射到动作，缺乏对长序列组合结构的显式建模。
- **LCDP**（Language-Conditioned Diffusion Policy）：在 LCBC 基础上引入扩散策略和 Transformer 策略头输出动作块，但仍依赖语言条件，无法泛化到未见过的起止组合。
- **GCBC**（Goal-Conditioned Behavioral Cloning）：使用 ResNet 编码器和 MLP 策略头，以目标图像为条件，同样受限于训练分布内的起止对。
- **GCDP**（Goal-Conditioned Diffusion Policy）：结合 ResNet 和 Transformer 策略头输出动作块，是目标条件扩散策略的代表。

这四类方法在组合规划基准上均表现不佳（表 2），因为它们在训练时未见过的起止组合上缺乏组合泛化能力。本文通过将规划建模为因子图推理，利用预训练短片段模型作为局部先验，在推理时通过消息传递强制全局一致性，实现了对分布外起止组合的零样本泛化。

### 3. 方法适用边界

**适用场景**：
- 任务可分解为具有重叠边界的短片段链式结构。
- 具备短片段演示数据用于训练局部扩散先验。
- 测试时起止条件可能超出训练分布，需要组合泛化。

**不适用或需谨慎使用的场景**：
- 任务结构无法自然地分解为线性链式因子图（如复杂的分支或循环依赖）。
- 短片段扩散模型的 Tweedie 估计在去噪早期阶段不够准确时，边界一致性约束的效果会受到影响（见局限性分析）。

### 4. 局限性与开放问题

**已知局限**：

1. **Tweedie 估计依赖性**：方法依赖 Tweedie 估计的准确性，在扩散去噪的早期步骤中，$x_{0|t}$ 的估计可能不准确，影响边界一致性约束的有效性。

2. **片段数量需手动指定**：测试时需要手动指定组合片段数量 $n$，缺乏从任务结构和不确定性中自动推断最优 $n$ 的机制。

3. **推理计算开销**：梯度优化引导（扩散球体引导 + 消息传递残差）导致推理时的计算开销高于直接平均采样方法（如 DiffCollage 的简单分数平均）。

**开放问题**：

- 如何从任务结构和不确定性中自动推断最优的片段数量 $n$？
- 能否设计更轻量的优化调度以降低测试时的计算开销？
- 该方法能否扩展到全景图像生成、长文到视频合成等非机器人规划任务？
- 因子图结构能否从线性链推广到更一般的图拓扑（如树结构或循环图），以处理更复杂的任务依赖关系？



## 原文 PDF

![[paperPDFs/ICLR_2026/Compositional_Visual_Planning_via_Inference_Time_Diffusion_Scaling.pdf]]
