---
title: "Learning Flexible Forward Trajectories for Masked Molecular Diffusion"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Learning_Flexible_Forward_Trajectories_for_Masked_Molecular_Diffusion.pdf
openreview_forum_id: raVuVPbnQL
aliases:
- MMEWLD
- LFFTMMD
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/chemistry_and_drug_discovery
core_operator: "为每个图元素（原子和键）学习独立的噪声调度（MELD），使不同分子的正向轨迹分离开，最小化状态冲突。"
primary_logic: "通过元素级可学习的噪声调度网络，自适应地为每个原子和键分配不同的掩码速率，减少不同分子塌缩到相同中间状态的概率，缓解状态冲突，从而使单模态去噪器更准确地学习目标分布，在保持完美有效性的同时大幅提升分布对齐度。"
claims:
- "MELD 在 QM9 和 ZINC250K 上实现 100% 化学有效性，且 FCD 大幅降低（QM9: 0.09, ZINC250K: 1.51），远超标准 MDM（FCD 3.62/26.09）。"
- "在对称分子（如邻/间苯二胺）上，元素不可知调度的去噪器预测熵高，MELD 显著降低不确定性。"
- "MELD 在正向扩散后期保留更多唯一图状态（ZINC250K T-1: 17.3 vs 标准 MDM 1.7–13.3），直接缓解了状态冲突。"
- "MELD 在 Polymer 条件生成中将平均 MAE 降低 13.4%（0.798 vs GraphDiT 0.921），同时提升分布质量（Frag 0.974, FCD 5.93）。"
---

# Learning Flexible Forward Trajectories for Masked Molecular Diffusion

> [!tip] 核心洞察
> 通过元素级可学习的噪声调度网络，自适应地为每个原子和键分配不同的掩码速率，减少不同分子塌缩到相同中间状态的概率，缓解状态冲突，从而使单模态去噪器更准确地学习目标分布，在保持完美有效性的同时大幅提升分布对齐度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向掩码分子扩散的学习灵活前向轨迹 |
| 英文题名 | Learning Flexible Forward Trajectories for Masked Molecular Diffusion |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=raVuVPbnQL); [Project](https://holymollyhao.github.io/MELD/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/chemistry_and_drug_discovery |
| Method | MELD (Masked Element-wise Learnable Diffusion) |
| Dataset | QM9, ZINC250K, Polymer (property-conditioned) |

> [!tip] 效果简介
> - QM9 上，FCD↓ 为 0.09，对比 3.62 (MDM w/ power-law)，变化 -3.53。
> - ZINC250K 上，FCD↓ 为 1.51，对比 26.09 (MDM w/ power-law)，变化 -24.58。
> - Polymer (property-conditioned) 上，MAE↓ 为 0.798，对比 0.921 (GraphDiT)，变化 -0.123 (13.4% reduction)。

## 概述

掩码扩散模型（MDM）在分子生成中面临一个根本性瓶颈：**状态冲突**（state-clashing）。标准的MDM采用固定的、与元素无关的噪声调度，所有原子和键以相同的速率被掩码。这导致语义上不同的分子在正向扩散过程中塌缩到相同的中间状态，使得逆向重建目标变为多模态分布。由于KL散度的模式覆盖特性，单模态去噪器被迫收敛到高熵分布，最终生成分布失调甚至化学无效的分子。

针对这一问题，本文提出 **MELD**（Masked Element-wise Learnable Diffusion），核心思想是**为每个图元素（原子和键）学习独立的噪声调度**。通过引入一个可学习的噪声调度网络，MELD自适应地为不同元素分配差异化的掩码速率，使不同分子的正向轨迹相互分离，从根源上缓解状态冲突。训练时，前向过程（噪声调度网络）与逆向过程（去噪器）联合优化，离散采样则通过 Straight-Through Gumbel-Softmax 估计器保持梯度流动。

实验表明，MELD在QM9和ZINC250K上均实现100%化学有效性，FCD分别降至0.09和1.51，显著优于标准MDM（FCD 3.62/26.09）。在Polymer属性条件生成中，MELD将平均MAE降低13.4%（0.798 vs GraphDiT 0.921），同时提升分布质量。消融实验直接验证了MELD在正向扩散后期保留更多唯一图状态（ZINC250K T-1: 17.3 vs 基线 1.7–13.3），证实其有效缓解了状态冲突。

## 背景与动机

分子生成是药物发现和材料设计中的核心任务，其目标是从目标分布中采样化学上有效且结构多样的分子图。近年来，扩散模型在分子生成领域展现出巨大潜力，其中**掩码扩散模型（Masked Diffusion Models, MDMs）**因其离散图生成中的高效率和完美化学有效性而备受关注。然而，标准 MDMs 在分子生成中暴露出一个关键的失效模式：**状态冲突（state‑clashing）**。

### 状态冲突：标准掩码扩散的根本瓶颈

在标准 MDMs 中，前向扩散过程对所有图元素（原子节点和化学键边）施加**固定的、与元素无关的噪声调度**。这意味着，无论分子的结构差异有多大，所有节点和边都以相同的速率被逐步掩码。随着扩散进行，不同分子在正向轨迹中会塌缩到完全相同的中间状态——即大量元素被掩码后不可区分的图。这种状态冲突导致逆向重建目标变得**多模态化**：同一个噪声状态可能对应多个不同的原始分子，而单模态去噪器无法有效学习这种一对多的映射，最终造成生成分布失调，甚至产生无效分子。

图 1 直观地展示了这一问题：元素无关的噪声调度（Figure 1a）使不同分子的正向轨迹高度重叠，而 MELD 提出的元素特定调度（Figure 1b）则通过差异化掩码速率将轨迹分离开，从而缓解状态冲突。

### 现有方法的局限

现有分子生成方法主要沿两条路径发展：一类是基于连续扩散的模型（如 GruM），另一类是基于离散扩散的模型（如 DiGress、GraphARM、GraphDiT）。尽管这些方法在特定数据集上取得了不错的效果，但它们均采用固定的前向噪声调度，未能从根本上解决状态冲突问题。具体而言：

- **固定调度**：所有元素共享相同的掩码概率 $\gamma_t$，无法区分不同原子和键在分子结构中的重要性差异。
- **单模态去噪器**：标准 MDMs 的去噪器假设每个噪声状态对应唯一的干净图，但状态冲突使这一假设失效。
- **分布失调**：在 ZINC250K 等复杂数据集上，标准 MDMs 的 FCD（Fréchet ChemNet Distance）高达 26.09，远未达到实用水平。

### 核心动机与解决思路

本文的核心洞察是：**通过为每个图元素学习独立的噪声调度，可以使不同分子的正向轨迹分离开，最小化状态冲突**。具体而言，MELD（Masked Element-wise Learnable Diffusion）引入一个可学习的噪声调度网络，为每个原子 $i$ 和键 $(i,j)$ 生成独立的掩码概率 $\gamma_{t,\phi}^i$ 和 $\gamma_{t,\phi}^{ij}$，从而在正向扩散中保留更多唯一图状态。这一设计使得单模态去噪器能够更准确地学习目标分布，在保持完美化学有效性的同时大幅提升分布对齐度。

### 关键证据预览

MELD 的有效性在多个层面得到验证：

- **分布对齐**：在 QM9 和 ZINC250K 上，MELD 将 FCD 分别降至 0.09 和 1.51，远超标准 MDM 的 3.62 和 26.09（Table 1）。
- **状态冲突缓解**：在 ZINC250K 的扩散后期（$T-1$ 步），MELD 保留了 17.3 个唯一图状态，而标准 MDM 仅保留 1.7–13.3 个（Table 6）。
- **条件生成**：在 Polymer 数据集上，MELD 将平均 MAE 降低 13.4%（0.798 vs GraphDiT 的 0.921），同时提升分布质量（Table 2）。
- **预测不确定性**：在对称分子（如邻/间苯二胺）上，元素无关调度的去噪器预测熵高，而 MELD 显著降低了不确定性（Figure 2）。

这些结果表明，通过联合优化前向（噪声调度网络）和逆向（去噪器）过程，MELD 有效解决了掩码扩散模型中固有的状态冲突问题，为分子生成提供了一种灵活且高效的框架。

## 核心创新

MELD 的核心创新在于将标准掩码扩散模型（MDM）中**固定的、与元素无关的噪声调度**，替换为**逐元素可学习的差异化调度**，从而系统性地缓解分子图生成中的**状态冲突（state-clashing）**问题。

### 问题根源：状态冲突与多模态目标

在标准 MDM 中，所有原子和键共享相同的掩码概率 $\gamma_t$，无论其化学语义如何。这一元素不可知（element-agnostic）的前向过程导致一个关键瓶颈：**语义不同的分子在正向扩散中可能塌缩到完全相同的中间状态**——例如，两个仅在某个键类型上不同的分子，当该键同时被掩码后，它们在中间时刻变得不可区分。这种现象被称为状态冲突（Section 4.1）。

状态冲突的直接后果是使逆向重建目标变为**多模态分布** $p(\mathbf{g} \mid \mathbf{g}_t)$：给定相同的中间状态 $\mathbf{g}_t$，去噪器需要同时预测多个不同的原始图。由于 KL 散度的 mode-covering 特性，用单模态去噪网络 $p_\theta$ 拟合该多模态目标会收敛到**高熵分布**——即对所有可能结果赋予相近的概率，表现为预测不确定性高、生成分布失调，甚至产生无效分子（Figure 2）。

### 关键改动：逐元素可学习的噪声调度

MELD 对上述瓶颈的解决方案体现在三个层次上对标准 MDM 的改动：

**1. 噪声调度类型：从全局固定到逐元素可学习**

标准 MDM 使用固定的全局调度（如 power-law $\gamma_t = 1 - (1 - \epsilon) \cdot t$），所有节点和边共享相同的掩码速率。MELD 引入**可学习的元素级嵌入向量** $\mathbf{h}^i$ 和 $\mathbf{h}^{ij}$，通过参数化的噪声调度网络为每个原子和键生成独立的掩码概率：

$$\gamma_{t,\phi}^i = 1 - (1 - \epsilon) \cdot t^{w_\phi^i}, \quad w_\phi^i = \sigma_{\mathrm{sf}}(f_\phi(\mathbf{h}^i))$$

其中 $f_\phi$ 是一个两层 MLP（SiLU 激活，隐藏维度 64），$\sigma_{\mathrm{sf}}$ 为 softplus 函数确保速率非负。这使得模型可以**自适应地学习哪些元素应该更早或更晚被掩码**——例如，在对称分子中，区分性键可以被赋予更低的掩码速率，从而在扩散过程中保留更长时间，减少与其他分子的状态冲突。

**2. 前向过程优化：从固定到联合学习**

标准 MDM 的前向过程完全固定，无可学习参数。MELD 将噪声调度网络 $f_\phi$ 与去噪网络 $p_\theta$ **联合优化**，使前向扩散过程本身成为学习的一部分。这一设计的关键在于：前向过程不再机械地向所有分子施加相同的破坏模式，而是通过与逆向目标的协同训练，主动学习能够**最大化区分不同分子轨迹**的差异化破坏策略。

**3. 离散采样梯度传递：Straight-Through Gumbel-Softmax**

分子图的离散采样天然阻断梯度回传。MELD 采用 Straight-Through Gumbel-Softmax（STGS）估计器解决这一问题：前向传播使用离散的 one-hot 向量进行精确采样，反向传播则通过连续的 softmax 近似传递梯度：

$$p_{\mathrm{soft},k} = \frac{\exp((z_k + g_k)/\eta)}{\sum_{l=1}^N \exp((z_l + g_l)/\eta)}$$

$$p = p_{\mathrm{hard}} - \mathrm{sg}(p_{\mathrm{soft}}) + p_{\mathrm{soft}}$$

其中 $\mathrm{sg}$ 为 stop-gradient 操作。这一设计使得整个端到端训练（从元素嵌入到噪声调度再到去噪预测）的梯度流保持完整。

### 创新效果的因果链路

上述改动的因果链路在实验中得到了直接验证：

- **状态冲突缓解**：在 ZINC250K 上，MELD 在扩散后期（T-1 步）保留了 17.3 个唯一图状态，而标准 MDM 仅保留 1.7–13.3 个（Table 6）。这直接证明了逐元素差异化调度有效减少了不同分子塌缩到相同中间状态的概率。
- **预测不确定性降低**：在对称分子（如邻/间苯二胺）上，元素不可知调度的去噪器对掩码键的预测呈现高熵分布，而 MELD 显著提升了预测置信度（Figure 2）。
- **分布质量跃升**：MELD 在 QM9 上将 FCD 从 3.62 降至 0.09，在 ZINC250K 上从 26.09 降至 1.51，同时保持 100% 化学有效性（Table 1）。

值得注意的是，MELD 的改动在计算开销上极为轻量——仅在现有 Transformer 架构基础上增加一个可学习的嵌入矩阵 $\mathbf{H}$，噪声调度网络本身仅为一个两层 MLP（Appendix C）。

## 整体框架

![[assets/figures/papers/iclr26_0012_raVuVPbnQL_Learning_Flexible_Forward_Trajectories_for_Maske/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between (a) element-agnostic noise scheduling and (b) element-specific noise scheduling. The former results in an issue denoted as state-clashing, leading to generation of invalid molecules. MELD mitigates this with element-specific noise schedule, effectively orchestrating the forward process to minimize state-clashings*

MELD 的整体 pipeline 围绕一个核心矛盾展开：标准掩码扩散模型（MDM）在分子图生成中采用固定的、与元素无关的噪声调度，导致语义不同的分子在正向扩散中塌缩到同一中间状态——即**状态冲突（state-clashing）**。这一问题使逆向过程的重建目标呈多模态分布，单模态去噪器无法有效拟合，最终产生分布失调甚至化学无效的分子。

MELD 的解决方案是将前向扩散过程本身参数化，与逆向去噪器联合优化。整个框架由三个关键模块串联构成：

### 1. 可学习的元素级嵌入

为图中每个节点 $i$ 和每条边 $(i,j)$ 分配独立的可学习嵌入向量 $\mathbf{h}^i$ 和 $\mathbf{h}^{ij}$。这些嵌入是噪声调度网络的输入，其核心作用是赋予每个图元素一个可区分的“身份标识”，使得同构结构中的不同位置也能通过随机排列嵌入来获得差异化处理。这一设计直接服务于缓解状态冲突的目标——不同分子中的原子和键即使类型相同，也能因嵌入不同而经历不同的掩码速率。

### 2. 噪声调度网络

噪声调度网络以两层 MLP（SiLU 激活，隐藏维度 64）将元素嵌入映射为每个元素的掩码速率权重 $w_\phi^i$，再通过参数化的 power-law 函数生成时间依赖的掩码概率：

$$\gamma_{t,\phi}^i = 1 - (1 - \epsilon) \cdot t^{w_\phi^i}, \quad w_\phi^i = \sigma_{\mathrm{sf}}(f_\phi(\mathbf{h}^i))$$

其中 $\sigma_{\mathrm{sf}}$ 为 softplus 函数，$\epsilon$ 为小常数。该公式使每个节点（和边）在扩散过程中以不同的速率被掩码——某些元素更早被破坏，另一些则保留更久。这直接改变了前向轨迹的几何结构：不同分子的中间状态不再轻易塌缩到同一表征，从而减少了逆向过程的多模态性。

### 3. 去噪变换器与端到端联合训练

逆向过程采用扩散变换器（DiT）作为去噪网络，独立预测原始节点类型和边类型。训练时，前向过程的噪声调度网络与逆向去噪器**联合优化**，损失函数为加权交叉熵：

$$\mathcal{L}(\theta, \phi) = \mathbb{E}_{t, g, g_t} \left[ \sum_{i} \frac{\dot{\gamma}_{t,\phi}^i}{1 - \gamma_{t,\phi}^i} \log p_\theta(x^i | g_t) + \lambda \sum_{i<j} \frac{\dot{\gamma}_{t,\phi}^{ij}}{1 - \gamma_{t,\phi}^{ij}} \log p_\theta(e^{ij} | g_t) \right]$$

这里的关键在于损失权重 $\frac{\dot{\gamma}}{1-\gamma}$ 随元素和时刻变化，使模型更关注那些刚被掩码的元素的重建。

### 4. 离散采样的梯度传递

分子图的离散性使得前向掩码采样本身不可微。MELD 采用 Straight-Through Gumbel-Softmax 估计器解决这一问题：前向传播使用 one-hot 离散向量 $p_{\mathrm{hard}}$，反向传播则使用连续的 softmax 近似 $p_{\mathrm{soft}}$ 传递梯度：

$$p = p_{\mathrm{hard}} - \mathrm{sg}(p_{\mathrm{soft}}) + p_{\mathrm{soft}}$$

其中 $p_{\mathrm{soft},k} = \frac{\exp((z_k + g_k)/\eta)}{\sum_l \exp((z_l + g_l)/\eta)}$，$g_k$ 为 Gumbel 噪声，$\eta$ 为温度参数。这一技巧保证了端到端训练的梯度完整性。

### 输入输出流

- **输入**：原始分子图 $g$（包含节点类型矩阵和边类型矩阵）。
- **前向扩散**：噪声调度网络根据元素嵌入生成每个节点/边的掩码概率 $\gamma_{t,\phi}$，通过 Gumbel-Softmax 采样得到被部分掩码的中间图 $g_t$。
- **逆向去噪**：去噪变换器接收 $g_t$ 和时间步 $t$，预测原始节点和边类型。
- **输出**：生成的分子图，经化学有效性校正后保证 100% 有效（在 QM9 和 ZINC250K 上均达到该指标）。

整个 pipeline 的计算开销极小——噪声调度网络仅额外引入嵌入矩阵 $\mathbf{H}$，其参数量相比去噪变换器主干可忽略不计。

## 核心模块与公式推导

MELD 的核心设计围绕一个问题展开：标准掩码扩散模型（MDM）中，固定的元素无关噪声调度导致语义不同的分子在正向扩散中塌缩到相同的中间状态（状态冲突），使逆向重建目标多模态化，单模态去噪器无法有效学习。MELD 通过引入逐元素可学习的噪声调度网络，为每个图元素（原子节点和键边）分配独立的掩码速率，从根源上缓解状态冲突。

### 前向过程与训练目标

MELD 的前向过程定义每个节点在时刻 $t$ 被掩码的概率为 $\gamma_{t,\phi}^i$。节点 $x_t^i$ 的边缘策略概率为：

$$
q_{\phi}(x_t^i \mid x_0^i) = \begin{cases} \gamma_{t,\phi}^i & \text{if } x_t^i = [\text{mask}] \\ 1 - \gamma_{t,\phi}^i & \text{if } x_t^i = x_0^i \end{cases}
$$

其中 $\gamma_{t,\phi}^i$ 不再是全局共享的固定值，而是由可学习的噪声调度网络根据元素嵌入动态生成的。去噪器 $p_\theta$ 的训练损失为加权交叉熵：

$$
\mathcal{L}(\theta, \phi) = \mathbb{E}_{t, g, g_t} \left[ \sum_{1 \leq i \leq N} \frac{\dot{\gamma}_{t,\phi}^i}{1 - \gamma_{t,\phi}^i} \log p_{\theta}(x^i | g_t) + \lambda \sum_{1 \leq i < j \leq N} \frac{\dot{\gamma}_{t,\phi}^{ij}}{1 - \gamma_{t,\phi}^{ij}} \log p_{\theta}(e^{ij} | g_t) \right]
$$

该损失本质上是真实后验 $p(\pmb{g} | \pmb{g}_t) \propto p(\pmb{g}_t | \pmb{g}) p(\pmb{g})$ 与参数化逆向过程 $p_\theta(\pmb{g} | \pmb{g}_t)$ 之间的 KL 散度期望。当正向过程固定且元素无关时，不同分子可能塌缩到同一 $\pmb{g}_t$，使 $p(\pmb{g} | \pmb{g}_t)$ 变成多峰分布。KL 散度的 mode-covering 特性迫使单模态去噪器收敛到高熵分布，产生模糊预测。MELD 通过使 $\gamma_{t,\phi}^i$ 依赖于元素身份，让不同分子的正向轨迹分离开，缩小 $p(\pmb{g} | \pmb{g}_t)$ 的后验支持集，从而缓解这一问题。

### 逐元素可学习的噪声调度

噪声调度网络的核心公式为：

$$
\gamma_{t,\phi}^i = 1 - (1 - \epsilon) \cdot t^{w_{\phi}^i}, \quad w_{\phi}^i = \sigma_{\mathrm{sf}}(f_{\phi}(\pmb{h}^i))
$$

其中 $\pmb{h}^i$ 是节点 $i$ 的可学习嵌入向量，$f_\phi$ 是一个两层 MLP（隐藏维度 64，SiLU 激活），$\sigma_{\mathrm{sf}}$ 是 softplus 函数，$\epsilon$ 是小常数防止数值问题。该设计通过 power-law 函数将嵌入映射为时间依赖的掩码速率：嵌入不同的节点获得不同的指数 $w_{\phi}^i$，从而以不同速率被掩码。键的调度 $\gamma_{t,\phi}^{ij}$ 采用相同机制，由边嵌入 $\pmb{h}^{ij}$ 参数化。

关键实现细节：为区分同构结构中的对称位置，元素嵌入在输入噪声调度网络前进行随机排列。这使得化学环境相同但拓扑位置不同的原子可能获得不同的掩码速率，进一步降低状态冲突。

### 离散采样的梯度传递

分子图生成涉及离散的节点类型和边类型采样。为使梯度能通过离散采样回传至噪声调度网络，MELD 采用 Straight-Through Gumbel-Softmax（STGS）估计器。首先通过 Gumbel-Softmax 获得连续松弛：

$$
p_{\mathrm{soft},k} = \frac{\exp((z_k + g_k)/\eta)}{\sum_{l=1}^N \exp((z_l + g_l)/\eta)}
$$

其中 $z_k$ 是 logits，$g_k$ 是 Gumbel 噪声，$\eta$ 是温度参数。然后通过 Straight-Through 技巧组合离散前向与连续反向：

$$
p = p_{\mathrm{hard}} - \mathrm{sg}(p_{\mathrm{soft}}) + p_{\mathrm{soft}}
$$

前向传播使用 one-hot 的 $p_{\mathrm{hard}}$，反向传播时梯度通过 $p_{\mathrm{soft}}$ 流动（$\mathrm{sg}$ 为 stop-gradient 操作）。这使得噪声调度网络和去噪器可以端到端联合优化。

### 管线模块总结

MELD 的完整管线由四个关键模块组成：

1. **可学习的元素级嵌入**：为每个节点和边分配嵌入向量，作为噪声调度网络的输入，并通过随机排列区分同构结构。
2. **噪声调度网络**：两层 MLP，将元素嵌入映射为每个元素的掩码速率 $w_{\phi}^i$，实现逐元素差异化的前向扩散。
3. **去噪变换器**：基于扩散变换器架构的去噪网络，独立预测原始节点类型和边类型。
4. **Straight-Through Gumbel-Softmax**：在离散图采样中保持梯度流动，实现前向与逆向过程的联合训练。

计算开销方面，噪声调度网络仅增加一个嵌入矩阵 $\pmb{H}$ 和一个小型 MLP，相对于已有的变换器骨干网络，额外参数量和计算量可忽略。

## 实验与分析

### 无条件分子生成主结果

MELD 在 QM9 和 ZINC250K 两个标准分子生成基准上进行了无条件生成评估，生成 10,000 个分子并与多种基线方法对比（Table 1）。核心发现如下：

![[assets/figures/papers/iclr26_0012_raVuVPbnQL_Learning_Flexible_Forward_Trajectories_for_Maske/figures/003_Table_1.jpg]]
*Table 1: Unconditional generation of 10K molecules on QM9 and ZINC250K datasets. The best and second best performances are represented by bold and underline. Table 2: Property-conditioned generation of 10K Polymers on three gas permeability properties and synthetic score. The numbers in parentheses in Valid. represent the validity without correction. The best and second best performances are represented by bold and underline*

- **QM9 数据集**：MELD 实现 100% 化学有效性，FCD 降至 0.09，相比使用 power-law 固定调度的标准 MDM（FCD = 3.62）降低了 3.53，降幅超过 97%。NSPDK 达到 0.0002，Scaffold 相似度为 0.5933，均优于或持平于 DiGress、GruM 等离散/连续扩散基线。
- **ZINC250K 数据集**：MELD 同样保持 100% 有效性，FCD 为 1.51，而标准 MDM 的 FCD 高达 26.09，降幅达 24.58。在 6 项指标中的 5 项上取得最优结果，唯一性（Uniq.）和 novelty（Novel.）也保持高位。

这些结果表明，逐元素可学习的噪声调度从根本上缓解了状态冲突问题，使得去噪器能够学习到更准确的目标分布，从而在保持完美化学有效性的同时大幅提升分布对齐度。

### 属性条件生成结果

在 Polymer 数据集上，MELD 针对三种气体渗透性（O₂、N₂、CO₂）和合成可及性分数进行属性条件生成（Table 2）：

![[assets/figures/papers/iclr26_0012_raVuVPbnQL_Learning_Flexible_Forward_Trajectories_for_Maske/figures/004_Table_2.jpg]]

- MELD 将平均 MAE 降至 0.798，相比最强基线 GraphDiT（MAE = 0.921）降低了 13.4%。
- 分布质量指标方面，MELD 在 Frag（0.974）和 FCD（5.93）上均取得最优，有效性达 99.10%。
- 所有方法均采用 classifier-free guidance，在相同测试条件下比较，确保了公平性。

### 消融实验：噪声调度策略的影响

Table 3 展示了在 ZINC250K 上对不同噪声调度策略的系统消融：

![[assets/figures/papers/iclr26_0012_raVuVPbnQL_Learning_Flexible_Forward_Trajectories_for_Maske/figures/005_Table_3.jpg]]
*Table 3: Ablation study of MELD with varying noise scheduling approaches. γ without ϕ and γϕ denote fixed and learnable schedules, respectively. V.U.N. denotes a composite score for Validity, Uniqueness, and Novelty*

- **固定调度 vs. 可学习调度**：将噪声调度从固定的 $\gamma$ 改为可学习的 $\gamma_\phi$，FCD 和 NSPDK 显著降低，Scaffold 相似度提升，验证了可学习调度的核心作用。
- **全局延迟调度 vs. 逐元素调度**：仅优化全局延迟参数（learnable global delay）的版本在分布相似度指标上已有改善，但完整的逐元素调度（MELD）进一步提升了各项指标，证明了细粒度、元素级差异化调度的额外增益。

### 状态冲突的直接验证

Table 6 量化了正向扩散过程中不同时间步的**唯一图状态数量**（ZINC250K 上平均 3 个种子）：

![[assets/figures/papers/iclr26_0012_raVuVPbnQL_Learning_Flexible_Forward_Trajectories_for_Maske/figures/009_Table_6.jpg]]
*Table 6: Number of unique graph states across varying timesteps in ZINC250K, averaged over 3 seeds*

- 在扩散后期（T-1 步），MELD 保留 17.3 个唯一图状态，而标准 MDM 仅保留 1.7–13.3 个。
- 唯一状态数量越多，意味着不同分子塌缩到相同中间状态的概率越低，状态冲突得到直接缓解。这一结果从机制层面验证了 MELD 设计的有效性。

### 预测熵可视化

Figure 2 通过对对称分子（如邻/间苯二胺）和非对称分子的预测熵可视化，揭示了元素不可知调度的根本缺陷：

![[assets/figures/papers/iclr26_0012_raVuVPbnQL_Learning_Flexible_Forward_Trajectories_for_Maske/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of prediction entropy for various molecule types. The first and second rows show prediction matrices with nitrogen bonds masked, while the third row shows generations with chlorine bond masked. From left to right: (a) 3D renderings of the input molecules, (b) predictions from MDMs using a fixed power law noise schedule, and (c) predictions from MELD. Brighter colors indicate lower uncertainty ( i . e . , higher confidence). The dark diagonal entries reflect enforced uniform predictions, as self-connections in molecules are not meaningful and are excluded from valid outputs. Note that predictions are being made for all locations, regardless of their entropy values*

- 在元素不可知调度下，去噪器在预测被掩码的键类型时表现出**高熵（高不确定性）**，尤其是在对称分子中，多个可能的键类型在中间状态下无法区分。
- MELD 的逐元素调度使去噪器的预测熵显著降低（图中更亮的颜色），表明模型对正确键类型的置信度更高。这直接印证了状态冲突导致逆向目标多模态化的理论分析。

### 逆向过程恢复速度

Figure 3 对比了固定 power-law 调度与 MELD 在逆向重建过程中的恢复速度。MELD 在更少的去噪步数内即可恢复出正确的分子结构，表明差异化的前向轨迹使得逆向过程的目标更加明确，去噪器能够更高效地收敛。

### 学习到的噪声调度分析

Figure 4 可视化了节点和边上学习到的归一化掩码概率 $\sigma$ 的变异。不同元素（原子类型、键类型）被分配了显著不同的掩码速率，说明噪声调度网络成功捕捉到了分子结构的异质性，为每个图元素定制了差异化的破坏速率。

### 扩散步数鲁棒性

Figure 5 展示了 MELD 在不同扩散步数（50、100、150、200）下的性能。所有 MELD 变体均优于使用 500 步的 GraphDiT 基线（虚线），且性能随步数增加仅轻微下降，表明 MELD 对扩散步数具有良好的鲁棒性，即使在极少的采样步数下也能保持高质量的生成。

### 大规模数据集与合成图域的泛化

- **Guacamol 数据集**（Table 5）：MELD 在有效性、唯一性、novelty 三项指标上均达到 100%，且训练轮次减少 70%，证明了方法在大规模数据集上的可扩展性。
- **合成图（SBM）**（Table 7）：MELD 在 Degree、Cluster、Orbit、Spectral 等图统计量上取得最优，V.U.N. 达 97.50，表明逐元素调度思想可泛化至非分子图生成任务。

### 计算开销分析

Table 4 和 Table 10 报告了计算成本。MELD 引入的额外开销极小——噪声调度网络仅为一个两层 MLP（隐藏维度 64），在现有 Transformer 架构上增加的参数量和计算量可忽略不计。在分子大小 $|V|=100$、batch size 32 的条件下，MELD 的前向传播时间与标准 MDM 基本持平。

### 局限性与失败模式

尽管 MELD 在分子生成上取得了显著提升，仍需注意以下局限：

1. **非分子图数据的增益有限**：在文本、蛋白质序列等领域，状态冲突的风险较低，逐元素调度的优势不如分子图明显。
2. **极大分子的状态冲突残留**：当分子规模极大时，即使使用差异化调度，唯一状态数量的保留仍可能有限，状态冲突无法完全消除。
3. **对称性问题的残留**：虽然 MELD 通过随机排列嵌入来区分同构结构，但在高度对称的分子中，去噪器的不确定性可能仍然存在（需要手动验证具体边界情况）。

## 方法谱系与知识库定位

### 与相关工作的关系

MELD 处于离散扩散模型与分子图生成两个领域的交叉点，其核心贡献——逐元素可学习的噪声调度——直接回应了标准掩码扩散模型（MDM）在分子生成中的根本性瓶颈。

**相对于标准 MDM 的改进。** 传统 MDM（如使用 power-law 或 cosine 固定调度的变体）采用与元素无关的噪声调度，所有原子和键共享相同的掩码概率 $\gamma_t$。这种设计导致不同分子在前向扩散中塌缩到相同的中间状态，即**状态冲突**（state-clashing）。从 KL 散度的模式覆盖特性来看，单模态去噪器在面对多模态重建目标时会收敛到高熵分布，表现为预测不确定性升高、生成分布失调。MELD 通过为每个图元素学习独立的掩码速率 $\gamma_{t,\phi}^i = 1 - (1 - \epsilon) \cdot t^{w_\phi^i}$，从根本上缓解了状态冲突。实验证据直接支持这一机制：在 ZINC250K 的扩散后期（T-1），MELD 保留的唯一图状态数量为 17.3，而标准 MDM 仅为 1.7–13.3（Table 6），差异显著。

**与离散扩散模型的区别。** DiGress 和 GraphDiT 同属离散扩散框架，但均使用固定的前向过程。GraphARM 采用自回归掩码策略，本质上也是一种固定的逐元素生成顺序。MELD 的独特之处在于将前向过程本身参数化并纳入联合优化，这是对离散扩散范式的一个重要扩展。在无条件生成任务中，MELD 在 QM9 和 ZINC250K 上的 FCD 分别达到 0.09 和 1.51，远超 DiGress 等基线（Table 1）；在条件生成中，MELD 的平均 MAE 为 0.798，较 GraphDiT 的 0.921 降低了 13.4%（Table 2）。

**与连续扩散模型的比较。** GruM 等连续扩散方法在分子生成中也表现出色，但其扩散过程发生在连续空间，与 MELD 处理的离散图状态有本质区别。MELD 在合成图领域（SBM）的 V.U.N. 和 Orbit 指标上同样优于 GruM（Table 7），表明逐元素调度策略的适用性不限于分子图。

**与噪声调度优化文献的关系。** 在扩散模型领域，已有工作探索了可学习的噪声调度（如优化全局延迟参数），但这些方法通常调整的是所有元素的统一调度，而非逐元素差异化。MELD 的消融实验（Table 3）表明，仅优化全局延迟调度的版本在分布相似度指标上不如完整的逐元素调度（MELD），验证了细粒度控制的重要性。

### 适用边界

MELD 的设计假设和实验覆盖范围定义了其当前已验证的适用边界：

- **分子图生成是核心场景。** MELD 在 QM9、ZINC250K、Polymer 和 Guacamol 等分子数据集上均取得了一致且显著的改进，这表明当数据具有丰富的元素类型和结构多样性时，状态冲突问题最为突出，MELD 的优势也最明显。
- **合成图领域可迁移。** 在 SBM 合成图上的实验（Table 7）初步验证了方法的通用性，但需要注意的是，合成图的元素多样性远低于分子图，因此 MELD 的增益幅度也相应收窄。
- **非分子离散数据需谨慎评估。** 如论文自身指出的局限，在文本、蛋白质序列等领域，状态冲突的风险较低，MELD 的逐元素调度可能不会带来同等程度的收益。这一判断目前缺乏实验验证，属于开放问题。

### 局限性与开放问题

**已识别的局限：**

1. **领域依赖性。** MELD 的优势与数据中元素类型的多样性和结构对称性密切相关。在元素类型单一或状态冲突不显著的场景中，额外的调度网络可能仅引入冗余参数，而不会带来实质性改进。
2. **计算开销虽小但非零。** 噪声调度网络是一个两层 MLP（SiLU 激活，隐藏维度 64），增加的参数量和计算量在分子规模上可以忽略（Table 4, Table 10），但在需要极致效率的场景中仍需权衡。
3. **极大分子的状态冲突未完全消除。** 当分子规模增大时，即使使用逐元素调度，扩散后期保留的唯一状态数量仍然有限，状态冲突无法被完全根除。这意味着 MELD 缓解了问题，但未从根本上解决离散扩散中的多模态挑战。

**待探索的开放问题：**

- **跨领域泛化。** 逐元素噪声调度能否扩展到文本 token 生成或蛋白质序列设计？这些领域的元素类型和冲突模式与分子图不同，需要独立的实验验证。
- **与等变架构的结合。** MELD 当前使用扩散变换器作为去噪骨干，未显式利用图结构的排列等变性。将逐元素调度与等变图神经网络结合，可能进一步降低对称分子带来的预测不确定性。
- **条件生成中的调度适应性。** 在更复杂的多属性条件生成场景中，元素的差异化调度是否始终带来一致的增益，还是需要根据条件动态调整调度策略，目前尚无答案。
- **理论分析。** 状态冲突的缓解在经验上得到了充分验证（Table 6, Figure 2），但缺乏严格的理论刻画——例如，逐元素调度能在多大程度上降低不同分子轨迹的碰撞概率，以及这一概率与生成质量之间的定量关系。

## 原文 PDF

![[paperPDFs/ICLR_2026/Learning_Flexible_Forward_Trajectories_for_Masked_Molecular_Diffusion.pdf]]
