---
title: "Si-GT: Fast Interconnect Signal Integrity Analysis for Integrated Circuit Design via Graph Transformers"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Si_GT_Fast_Interconnect_Signal_Integrity_Analysis_for_Integrated_Circuit_Design_via_Graph_Transformers.pdf
openreview_forum_id: orO5727bSh
aliases:
- SG
- Si-GT
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/physics
core_operator: "通过网格模式编码显式注入局部耦合结构，虚拟NET令牌编码全局网级信号特性（切换方向/斜率），以及同网内-网间注意力机制（IIN-Attn）将电阻传播路径和耦合电容的物理偏置直接融入Transformer的自注意力计算，从而赋予图Transformer对串扰行为的长距依赖和跨网耦合的归纳偏置。"
primary_logic: "核心洞察是：将互连RC电路分解为每个节点的局部耦合网格单元并用浅层GNN结构化编码，同时通过网级令牌和专门的注意力偏置，使Transformer既能沿着同一网传播方向聚合信号退化信息，又能通过异网耦合电容偏置捕捉能量跨网转移，最终以极低推理延迟获得与SPICE高度一致的串扰延迟和毛刺预测。"
claims:
- "Si-GT在所有串扰延迟和毛刺预测任务上均超过GNN和现有图Transformer基线，同时推理速度比SPICE快多个数量级。"
- "消融实验表明，移除虚拟NET令牌、网格模式编码或IIN注意力中的任意组件均导致性能显著下降，其中<NET>令牌提升最为明显。"
- "Si-GT在不同互连长度下均保持最高精度，对长互连的泛化能力优于其他模型。"
- "Crosstalk Delay Prediction (Segment, Victim) 上 Mean Relative Accuracy (%) = 88.32 (Si-GT with MPE)"
---

# Si-GT: Fast Interconnect Signal Integrity Analysis for Integrated Circuit Design via Graph Transformers

> [!tip] 核心洞察
> 核心洞察是：将互连RC电路分解为每个节点的局部耦合网格单元并用浅层GNN结构化编码，同时通过网级令牌和专门的注意力偏置，使Transformer既能沿着同一网传播方向聚合信号退化信息，又能通过异网耦合电容偏置捕捉能量跨网转移，最终以极低推理延迟获得与SPICE高度一致的串扰延迟和毛刺预测。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Si-GT：基于图变换器的快速集成电路互连信号完整性分析 |
| 英文题名 | Si-GT: Fast Interconnect Signal Integrity Analysis for Integrated Circuit Design via Graph Transformers |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=orO5727bSh); [GitHub](https://github.com/xlab-ub/Si-GT) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/physics |
| Method | Si-GT |
| Dataset | Crosstalk Delay Prediction (Segment, Victim), Crosstalk Glitch Prediction (Segment, t_width) |

> [!tip] 效果简介
> - Crosstalk Delay Prediction (Segment, Victim) 上，Mean Relative Accuracy (%) 为 88.32 (Si-GT with MPE)，对比 88.23 (GraphGPS with RWSE16)，变化 +0.09。
> - Crosstalk Glitch Prediction (Segment, t_width) 上，Mean Relative Accuracy (%) 为 98.36 (Si-GT with MPE)，对比 96.61 (GraphGPS with RWSE16)，变化 +1.75。

## 概述

大规模VLSI设计中，互连线间的电容串扰效应会引入信号延迟偏差和毛刺，导致时序违例甚至逻辑错误。SPICE电路仿真虽是精度金标准，但其计算成本随互连规模指数增长，无法用于全芯片验证。现有机器学习方法（如GNN和图Transformer）主要聚焦于时序预测，未显式建模信号切换模式变化和攻击网-受害网间的电容耦合机制，实用性受限。

针对上述瓶颈，本文提出Si-GT——一种面向互连信号完整性分析的图Transformer模型。其核心洞察是：将互连RC电路分解为每个节点的局部耦合网格单元，通过浅层GNN结构化编码局部耦合结构；同时引入虚拟NET令牌编码网级全局信号特性（切换方向、斜率），并通过同网内-网间注意力机制（IIN-Attn）将电阻传播路径偏置和耦合电容偏置直接融入自注意力计算，赋予模型对串扰行为的长距依赖和跨网耦合的归纳偏置。

实验表明，Si-GT在串扰延迟和毛刺预测任务上均超越GNN及现有图Transformer基线（延迟预测平均相对准确率达88.32%，毛刺宽度预测达98.36%），推理速度比SPICE快多个数量级。消融实验证实虚拟NET令牌、网格模式编码和IIN注意力偏置三个组件均对性能有显著贡献，其中NET令牌的提升最为突出。

## 背景与动机

### 互连信号完整性：VLSI设计中的计算瓶颈

随着集成电路制造工艺持续微缩，芯片内互连线间距不断减小，相邻导线间的电容耦合效应急剧增强。当攻击网（aggressor net）发生信号切换时，通过耦合电容向邻近的受害网（victim net）注入噪声，引发两类典型的信号完整性（Signal Integrity, SI）问题：

- **串扰毛刺（Crosstalk Glitch）**：受害网处于静态时，攻击网的切换脉冲通过耦合电容在受害网上产生电压尖峰，可能导致下游逻辑门误触发。
- **串扰延迟（Crosstalk Delay）**：受害网自身也在切换时，攻击网的同步或反向切换会加速或减速受害网的信号传播，导致时序违例。

精确分析这些效应需要求解大规模互连RC网络的瞬态响应。工业界标准工具SPICE虽能提供高精度仿真，但其计算成本随互连规模呈超线性增长——对于包含数百万条互连线的全芯片设计，逐网进行SPICE仿真在工程上不可行。这一仿真瓶颈迫使设计团队采用保守的时序裕量，牺牲芯片性能以换取设计收敛性。

### 现有方法的局限性

为缓解SPICE的计算开销，研究者探索了多种替代方案：

**传统加速方法**（如模型降阶、解析近似）通过简化电路方程来换取速度，但精度损失显著，且难以适应复杂耦合拓扑。

**基于机器学习的方法**近年来受到关注。图神经网络（GNN）将互连电路建模为图，节点表示电路节点，边表示电阻或电容连接，利用消息传递机制学习信号传播规律。然而，现有工作存在两个根本性缺口：

1. **仅关注时序预测，忽视串扰物理机制**：现有GNN方法将SI分析简化为单纯的时序回归问题，未显式建模攻击网切换模式变化（方向、斜率）对受害网的耦合效应。当攻击网的信号特性改变时，模型缺乏相应的归纳偏置来捕捉跨网能量转移。

2. **缺乏对网级全局信号的建模**：互连线上的信号退化是沿传播方向累积的过程，而电容串扰是跨网耦合的局部效应。单纯的消息传递难以同时捕获同网内的长距依赖和异网间的耦合关系——前者需要沿电阻路径聚合信息，后者需要在特定耦合位置建模跨网交互。

图Transformer（如Graphormer、GraphGPS）通过全局自注意力机制扩展了感受野，但其结构编码（最短路径距离、空间编码）是针对通用图设计的，缺乏对互连电路物理特性的针对性建模。具体而言：电阻路径上的信号衰减遵循倒数关系，耦合电容的串扰强度取决于介质常数和几何参数——这些物理先验未被现有图Transformer的结构编码所捕获。

### 本文动机与核心思路

针对上述缺口，本文提出**Si-GT**，一个专为互连信号完整性分析设计的图Transformer模型。核心思路是：将互连RC电路的物理结构分解为三个层次的归纳偏置，并将其直接注入Transformer的自注意力计算中：

- **局部耦合网格编码（Mesh Pattern Encoding）**：将每个电路节点周围的耦合网格单元用浅层GNN编码，使模型感知局部耦合拓扑。
- **网级虚拟令牌（Virtual NET Token）**：为每条互连线引入可学习的全局表示，编码切换方向、斜率等网级信号特性，并通过注意力掩码限制其仅关注所属网节点。
- **网内-网间注意力（Intra-Inter Net Attention, IIN-Attn）**：在注意力logit中显式加入同网路径电阻偏置和异网耦合电容偏置，使自注意力机制天然具备沿电阻路径传播信号和跨耦合电容转移能量的能力。

通过这种物理感知的架构设计，Si-GT旨在以极低的推理延迟（毫秒级）实现与SPICE高度一致的串扰延迟和毛刺预测精度，为大规模VLSI设计中的快速SI签核提供可行路径。

## 核心创新

Si-GT的核心创新在于将互连RC电路的物理结构显式注入图Transformer的注意力计算，从而赋予模型对串扰行为的长距依赖和跨网耦合的归纳偏置。与现有图Transformer基线（Graphormer、GraphGPS）仅依赖通用结构编码（最短路径、空间距离）不同，Si-GT通过三个**changed slots**实现了物理感知的信号完整性预测：

### 1. 网格模式编码（Mesh Pattern Encoding）替代纯节点特征投影

基线方法直接对节点特征进行线性投影作为Transformer输入，忽略了互连电路固有的局部耦合结构。Si-GT将互连图按节点分解为多个**耦合网格单元**（mesh unit），每个单元包含两对相邻网络段及其耦合电容，随后用2层浅层GNN聚合该局部子图的结构信息：

$$h^{(0)}(v_i^s) = \mathbf{GNN}^l(mesh(v_i^s)) + en(x(v_i^s)) \in \mathbb{R}^d$$

该设计使初始节点嵌入天然携带了局部耦合拓扑的先验，而非从零开始学习。消融实验（Table 5）表明，移除MPE导致延迟预测准确率下降，验证了结构化编码的必要性。

### 2. 虚拟NET令牌（Virtual NET Token）引入网级全局表示

现有GNN和图Transformer均缺乏显式的网级聚合表示，无法编码切换方向、斜率等全局信号特性。Si-GT为每条网引入可学习的`<NET>`令牌，并通过注意力掩码限制其仅关注所属网节点：

$$\mathbf{M}_{\mathrm{NET}}(i,j) := \begin{cases} -\infty, & \text{if } i \text{ represents } net^i \text{ and } j \notin \mathcal{V}_S^i, \\ 0, & \text{otherwise}. \end{cases}$$

这一设计使得网级信号状态（受害网是否活跃、攻击网切换方向）能够通过`<NET>`令牌在整个网内传播和聚合。消融实验（Table 5）显示，移除`<NET>`令牌是性能下降最显著的单一操作——延迟和毛刺预测准确率均大幅下滑，证实了网级全局信号编码的关键作用。

### 3. 网内-网间注意力（IIN-Attn）融入物理偏置

标准图Transformer的自注意力仅依赖节点特征的相似度计算，缺乏对互连物理机制的感知。Si-GT在注意力logit中额外叠加三类结构偏置：

- **同网路径电阻偏置**（$\phi_{\mathrm{Intra}}$）：对同一网内节点对，注入沿信号传播路径的累积电阻 $\frac{1}{d_{uv} \cdot R_{\mathrm{w}}^i}$，使注意力能够感知信号退化程度；
- **异网耦合电容偏置**（$\phi_{\mathrm{Inter}}$）：对异网耦合段，注入耦合电容值 $\hat{C}_{u+1}^{ij}$，使注意力显式捕捉跨网能量转移；
- **空间距离编码与最短路径边编码**：保留通用结构信息作为补充。

最终注意力计算为：

$$\mathrm{Attn-IIN}(X) = \mathrm{softmax}\bigg(\frac{QK^\top}{\sqrt{d_K}} + \tilde{\Phi}_{\mathrm{IIN}} + \tilde{\Phi}_{\mathrm{d}} + \tilde{\Phi}_{\mathrm{sp}}\bigg)V$$

消融实验（Table 5, Table 9）表明，移除IIN的网间偏置（$\phi_{\mathrm{Inter}}$）显著降低毛刺预测性能，而去除空间距离编码和边编码进一步削弱精度，证明物理偏置与通用结构编码是互补的。

### 创新总结

三个changed slots形成因果闭环：**网格模式编码**提供局部耦合拓扑的先验，**虚拟NET令牌**赋予网级信号状态的全局视野，**IIN注意力**将电阻传播路径和耦合电容的物理规律直接融入信息聚合。这套设计使Si-GT在仅使用基线3-6倍参数量的情况下（Table 7），在所有串扰延迟和毛刺预测任务上均超越GNN和现有图Transformer基线（Table 2, Table 3），推理速度比SPICE快多个数量级（Figure 6）。

## 整体框架

![[assets/figures/papers/iclr26_0010_orO5727bSh_Si-GT_Fast_Interconnect_Signal_Integrity_Analysi/figures/003_Figure_3.jpg]]
*Figure 3: Overview of Si-GT*

Si-GT 的整体 pipeline 围绕一个核心设计原则展开：将互连 RC 电路的物理结构显式注入 Transformer 的自注意力计算，使模型天然具备对串扰行为的长距依赖和跨网耦合的归纳偏置。整个框架由四个串联模块构成：**网格模式编码（Mesh Pattern Encoding）**、**虚拟 NET 令牌初始化**、**Si-GT 编码器（IIN-Attn）** 和**预测头**。

### 输入预处理与图构建

输入为多网耦合互连电路。首先将互连按节点分解为多个**耦合网格单元（mesh unit）**，每个单元包含两对相邻网络段及其耦合电容，形成局部结构化子图。同时，每条网被赋予一个可学习的虚拟 `<NET>` 令牌，用于编码该网的全局信号特性（切换方向、斜率等）。图节点为各网段上的电路节点，节点特征包括电压、位置等物理量；边则分为同网内的电阻传播边和异网间的耦合电容边。

### 模块关系与数据流

**第一步：网格模式编码。** 对每个节点 $v_i^s$，提取其所属的局部耦合网格子图 $mesh(v_i^s)$，输入一个浅层 GNN（2 层，隐藏维度 64）进行结构聚合，得到结构感知嵌入；同时将节点原始特征 $x(v_i^s)$ 经线性投影 $en(\cdot)$ 映射到 $d$ 维空间。两者求和形成初始节点嵌入：

$$h^{(0)}(v_i^s) = \mathbf{GNN}^l(mesh(v_i^s)) + en(x(v_i^s)) \in \mathbb{R}^d$$

这一步将每个节点周围的耦合拓扑显式编码进嵌入，为后续注意力提供局部结构先验。

**第二步：虚拟 NET 令牌初始化。** 为每条网创建可学习的 `<NET>` 嵌入，并通过注意力掩码限制其仅关注所属网的节点：

$$\mathbf{M}_{\mathrm{NET}}(i,j) := \begin{cases} -\infty, & \text{if } i \text{ represents } net^i \text{ and } j \notin \mathcal{V}_S^i, \\ 0, & \text{otherwise}. \end{cases}$$

该掩码确保网级聚合的纯净性，使 `<NET>` 令牌成为该网全局信号状态的紧凑表示。

**第三步：Si-GT 编码器。** 核心为 6 层 Transformer，每层使用**同网-异网注意力（IIN-Attn）**。IIN-Attn 在标准自注意力 logit 上叠加四类物理偏置：

$$\mathrm{Attn-IIN}(X) = \mathrm{softmax}\bigg(\frac{QK^\top}{\sqrt{d_K}} + \tilde{\Phi}_{\mathrm{IIN}} + \tilde{\Phi}_{\mathrm{d}} + \tilde{\Phi}_{\mathrm{sp}}\bigg)V$$

其中：
- **$\tilde{\Phi}_{\mathrm{IIN}}$**：融合同网路径电阻偏置和异网耦合电容偏置。同网偏置 $\phi_{\mathrm{Intra}}(v_i^u, v_i^v) := \frac{1}{d_{uv} \cdot R_{\mathrm{w}}^i}$ 沿信号传播方向聚合退化信息；异网偏置 $\phi_{\mathrm{Inter}}(v_i^u, v_j^u) := \hat{C}_{u+1}^{ij}$ 捕捉耦合电容导致的跨网能量转移。
- **$\tilde{\Phi}_{\mathrm{d}}$**：空间距离编码，补充节点间几何关系。
- **$\tilde{\Phi}_{\mathrm{sp}}$**：最短路径边编码，保留图拓扑结构信息。

每层配置 4 个注意力头，嵌入维度 64，前馈网络维度 128，dropout 0.1。

**第四步：预测头。** 从编码后的段节点嵌入直接预测目标量。串扰延迟任务输出 1 维（延迟值），毛刺任务输出 2 维（毛刺幅值与宽度）。训练使用 AdamW 优化器，多项式学习率衰减至 $10^{-9}$，线性 warmup，共 60 个 epoch，batch size 256。

### 关键设计决策

整个 pipeline 的因果机制清晰：网格模式编码提供局部耦合结构先验，虚拟 NET 令牌提供网级全局信号上下文，IIN-Attn 将电阻传播路径和耦合电容的物理偏置直接融入注意力计算。消融实验（Table 5）表明，移除任意组件均导致性能显著下降——其中 `<NET>` 令牌的贡献最为突出，移除后毛刺预测准确率从 98.12% 骤降至 94.97%；去除异网偏置 $\phi_{\mathrm{Inter}}$ 则严重损害毛刺预测性能，验证了显式建模耦合电容对捕捉跨网串扰的必要性。

## 核心模块与公式推导

Si-GT 的核心架构由三个紧密耦合的模块构成：网格模式编码（Mesh Pattern Encoding）、网内-网间注意力机制（IIN-Attn）和虚拟 NET 令牌。三个模块共同将互连 RC 电路的物理偏置注入 Transformer 的自注意力计算，使模型具备对串扰行为的长距依赖和跨网耦合的归纳偏置。

### 网格模式编码（Mesh Pattern Encoding）

互连电路被分解为以每个节点为中心的局部耦合网格单元（mesh unit），每个单元包含两对相邻网络段及其间的耦合电容。网格模式编码通过浅层 GNN 聚合这些局部子图的结构信息，生成结构感知的节点嵌入：

$$h^{(0)}(v_i^s) = \mathbf{GNN}^l(mesh(v_i^s)) + en(x(v_i^s)) \in \mathbb{R}^d$$

其中 $v_i^s$ 表示第 $i$ 条网的第 $s$ 个段节点，$mesh(v_i^s)$ 是以该节点为中心的局部耦合网格子图，$\mathbf{GNN}^l$ 为 $l$ 层图神经网络（论文中取 $l=2$，隐藏维度 64），$en(\cdot)$ 为节点原始特征的线性投影。两部分求和后得到初始节点嵌入，既保留了节点自身的物理属性（电压、位置等），又注入了局部耦合结构信息。

### 网内-网间注意力机制（IIN-Attn）

IIN-Attn 是 Si-GT 的核心创新，在标准自注意力 logit 中叠加四类结构偏置，将互连电路的物理先验直接融入注意力计算：

$$\mathrm{Attn-IIN}(X) = \mathrm{softmax}\bigg(\frac{QK^\top}{\sqrt{d_K}} + \tilde{\Phi}_{\mathrm{IIN}} + \tilde{\Phi}_{\mathrm{d}} + \tilde{\Phi}_{\mathrm{sp}}\bigg)V$$

其中 $\tilde{\Phi}_{\mathrm{IIN}}$ 为网内/网间物理偏置，$\tilde{\Phi}_{\mathrm{d}}$ 为空间距离编码，$\tilde{\Phi}_{\mathrm{sp}}$ 为最短路径边编码。

**网内编码（Intra-net Encoding）** 捕获同一网内节点间沿传播路径的电阻退化效应：

$$\phi_{\mathrm{Intra}}(v_i^u, v_i^v) := \frac{1}{d_{uv} \cdot R_{\mathrm{w}}^i}$$

其中 $d_{uv}$ 为节点 $u$ 和 $v$ 在同一网上的路径距离，$R_{\mathrm{w}}^i$ 为该网的单位段电阻。该偏置仅在两节点属于同一网时非零，使注意力能沿信号传播方向聚合退化信息。

**网间编码（Inter-net Encoding）** 捕获异网间耦合电容引起的能量跨网转移：

$$\phi_{\mathrm{Inter}}(v_i^u, v_j^u) := \hat{C}_{u+1}^{ij}$$

其中 $\hat{C}_{u+1}^{ij}$ 为网 $i$ 和网 $j$ 在第 $(u+1)$ 段处的归一化耦合电容。该偏置仅在两网在对应段存在耦合电容时非零，使模型能显式建模攻击网-受害网间的串扰强度。

### 虚拟 NET 令牌

为每条网引入一个可学习的虚拟 `<NET>` 令牌，编码网的全局信号特性（切换方向、斜率、网状态等）。通过注意力掩码限制 `<NET>` 令牌仅关注其所属网的节点：

$$\mathbf{M}_{\mathrm{NET}}(i,j) := \begin{cases} -\infty, & \text{if } i \text{ represents } net^i \text{ and } j \notin \mathcal{V}_S^i, \\ 0, & \text{otherwise}. \end{cases}$$

该掩码确保网级聚合的纯净性，消融实验表明移除 `<NET>` 令牌导致延迟和毛刺预测准确率大幅下降（Table 5），是 Si-GT 中贡献最大的单一组件。

## 实验与分析

### 主实验结果

Si-GT在串扰延迟和毛刺预测任务上均全面超越GNN和图Transformer基线。在段级延迟预测中，Si-GT GCN变体对受害网延迟（$\Delta \hat{D}_{vic}$）的平均相对准确率达**88.32%**，Si-GT SAGE在聚合延迟（$\Delta \hat{D}_{agg}$）上达**73.67%**（Table 2）。在段级毛刺预测中，Si-GT GIN在毛刺宽度（$\Delta t_{width}$）上达**98.36%**，Si-GT GCN在毛刺峰值电压（$\Delta v_{max}$）上达**97.89%**（Table 3）。汇级预测任务中，Si-GT同样保持领先，毛刺宽度准确率达**98.53%**，峰值电压达**98.63%**（Table 3）。

![[assets/figures/papers/iclr26_0010_orO5727bSh_Si-GT_Fast_Interconnect_Signal_Integrity_Analysi/figures/005_Table_2.jpg]]
*Table 2: Mean relative accuracy (%) of crosstalk delay prediction results*

![[assets/figures/papers/iclr26_0010_orO5727bSh_Si-GT_Fast_Interconnect_Signal_Integrity_Analysi/figures/006_Table_3.jpg]]
*Table 3: Mean relative accuracy (%) of crosstalk glitch prediction results*

值得注意的是，Si-GT在不同互连长度下均保持最高精度，对长互连的泛化能力显著优于其他模型（Figure 4）。短互连场景下所有模型精度均有所下降，这与数据集中短互连样本稀疏直接相关（Figure 7），属于数据分布瓶颈而非模型设计缺陷。

![[assets/figures/papers/iclr26_0010_orO5727bSh_Si-GT_Fast_Interconnect_Signal_Integrity_Analysi/figures/007_Figure_4.jpg]]
*Figure 4: Comparison of models in signal integrity analysis under various IC interconnect lengths*

与SPICE仿真相比，Si-GT的推理时间仅约**4.0 ms**，而SPICE则需超过100 ms（Figure 6），加速比超过一个数量级。在GPU上，对于小规模图，核启动开销可能导致Si-GT的延迟略高于CPU执行，实际部署时需根据图规模选择执行设备（Figure 8）。

![[assets/figures/papers/iclr26_0010_orO5727bSh_Si-GT_Fast_Interconnect_Signal_Integrity_Analysi/figures/014_Figure_6.jpg]]
*Figure 6: SPICE vs. Transformer-based models running time across varying interconnect scales*

### 消融实验

消融实验（Table 5）系统验证了Si-GT三项核心设计的贡献：

![[assets/figures/papers/iclr26_0010_orO5727bSh_Si-GT_Fast_Interconnect_Signal_Integrity_Analysi/figures/009_Table_5.jpg]]
*Table 5: Ablation study results on crosstalk prediction with different designs*

- **虚拟<NET>令牌（NET）**：移除后性能下降最为显著。以段级延迟预测为例，去除NET后受害网延迟准确率从88.28%降至88.23%，毛刺宽度从98.12%降至94.97%。这表明网级全局信号特性（切换方向、斜率等）的显式编码对串扰预测至关重要。
- **网格模式编码（MPE）**：去除MPE导致延迟预测准确率下降，验证了局部耦合网格结构信息对传播延迟建模的贡献。
- **IIN注意力偏置**：去除网间耦合电容偏置（$\Phi_{Inter}$）后，毛刺预测性能显著降低，证实跨网能量转移的物理偏置对毛刺建模不可或缺。去除同网路径电阻偏置（$\Phi_{Intra}$）同样导致精度下降。

进一步消融（Table 9）表明，去除空间距离编码和最短路径边编码会进一步降低精度，说明Si-GT中叠加的多层结构偏置对性能均有正向贡献。

### 注意力可视化分析

Si-GT与Graphomer的注意力图对比（Figure 5）揭示了两者的本质差异：Graphomer的注意力模式相对均匀分散，缺乏对物理结构的聚焦；而Si-GT的IIN注意力通过显式偏置，使注意力权重集中于同网传播路径和异网耦合节点，呈现出与RC电路物理行为高度一致的模式。这解释了Si-GT在精度上的优势来源。

### 段模型到汇模型的迁移

段级训练的Si-GT在汇级预测任务中表现出最小的性能波动（Table 4），汇级延迟误差幅度仅为+0.08%至-0.18%，优于DeepGCN、Graphomer和GraphGPS。这表明Si-GT学习到的物理表示具有良好的层次泛化能力，段级嵌入可直接用于汇级预测而不需重新训练。然而，段级到汇级的误差累积机理尚不明确，目前采用简单聚合策略，端到端的汇级训练架构仍需探索。

### 有向图与无向图对比

采用有向互连图对多数模型在延迟预测任务上有正向影响（Table 6），但对毛刺预测影响不显著。Si-GT在有向图下表现稳定，延迟预测变化幅度小于0.2%，表明其IIN偏置已有效捕获信号传播的方向性，对图方向性不敏感。

### 模型效率分析

Si-GT的可训练参数量约**282K-307K**（Table 7），约为相应GNN主干的3-6倍，小于Graphomer（约350K）和GraphGPS（约422K）。在保持最高精度的同时，参数效率优于同类图Transformer。训练收敛速度方面，Si-GT在延迟和毛刺任务上均展现出更快的收敛和更低的最终训练损失（Figure 9）。

### 失败模式与局限

1. **短互连泛化不足**：所有模型在段数较少的互连上精度均下降，根本原因是数据集中短互连样本稀疏（Figure 7），耦合变化模式有限。这是数据分布问题，需通过数据增强或课程学习策略解决。
2. **GPU小图推理开销**：对于小规模图，GPU核启动开销可能抵消并行计算优势，导致推理延迟高于CPU（Figure 8）。实际部署需动态选择执行设备。
3. **场景简化假设**：当前模型仅考虑单受害网-多攻击网的串扰场景，未覆盖多受害网同时切换等复杂情形。扩展到更一般场景的可行性尚待验证。
4. **全芯片规模未验证**：模型在由少量网（≤3）组成的互连簇上训练和评估，尚未在数百万网级别的全芯片设计中进行验证。

## 方法谱系与知识库定位

### 与现有方法的谱系关系

Si-GT 处于图神经网络（GNN）与图变换器（Graph Transformer）的交汇点，其设计直接回应了现有方法在互连信号完整性分析中的结构性不足。

**GNN 基线的能力边界。** GCN、GAT、GIN、SAGE 和 DeepGCN 等标准 GNN 模型（Table 2, Table 3）在串扰延迟和毛刺预测任务上的平均相对准确率普遍低于 Si-GT 变体。GNN 的核心瓶颈在于消息传递受限于局部邻域，难以捕获沿同一网长距离传播的电阻退化效应和跨网耦合电容的能量转移——这两者恰是串扰行为的物理本质。DeepGCN 虽加深了网络层数，但深层 GNN 的过平滑问题使其在长互连场景下精度提升有限（Figure 4）。

**图变换器基线的改进空间。** Graphomer 和 GraphGPS 引入了全局自注意力以突破 GNN 的局部性限制，但其结构编码（最短路径距离编码、空间编码、随机游走结构编码）是通用的拓扑偏置，缺乏对互连物理的专门建模。具体而言：
- Graphomer 的最短路径编码无法区分“同网路径电阻”与“异网耦合电容”这两种物理效应截然不同的边类型；
- GraphGPS 将消息传递与全局注意力分离为两个独立模块，导致物理偏置无法直接融入注意力计算（Section 5.4 消融分析）。

**Si-GT 的差异化设计。** Si-GT 在 Transformer 架构中引入了三个专用模块，将互连物理直接编码为注意力偏置（Figure 3）：
1. **网格模式编码（MPE）**：用浅层 GNN 聚合每个节点周围的局部耦合网格子图，将高阶耦合结构压缩为节点嵌入（Equation 1），取代了通用的位置编码方案；
2. **网内-网间注意力（IIN-Attn）**：在同网节点对之间注入路径电阻偏置 $\phi_{\mathrm{Intra}}$（Equation 2），在异网节点对之间注入耦合电容偏置 $\phi_{\mathrm{Inter}}$（Equation 3），使 Transformer 的全局注意力天然具备串扰物理的归纳偏置；
3. **虚拟 NET 令牌**：为每条网引入可学习的网级表示，编码切换方向、斜率等全局信号特性，并通过注意力掩码（Section 4.3）限制其仅关注所属网节点，实现网级信号状态的显式建模。

消融实验（Table 5）证实了每个模块的独立贡献：移除虚拟 NET 令牌导致延迟和毛刺准确率大幅下降；移除 IIN 网间偏置 $\phi_{\mathrm{Inter}}$ 显著降低毛刺预测性能；移除 MPE 和空间/边编码偏置进一步削弱精度（Table 9）。这表明 Si-GT 的性能优势并非来自 Transformer 的通用表达能力，而是来自物理偏置的精确注入。

### 适用边界与局限

**适用场景。** Si-GT 当前适用于由少量网（≤3 条）组成的互连簇的串扰延迟和毛刺预测，涵盖单受害网-多攻击网的简化串扰场景。模型在段级和汇级两种预测粒度上均表现良好（Table 2, Table 3），且推理速度比 SPICE 快多个数量级（Figure 6），适合作为 EDA 流程中的快速评估工具。

**已知局限。**
1. **规模未验证**：模型仅在 ≤3 条网的小规模互连簇上训练和评估，尚未在全芯片规模的数百万网场景下验证其可扩展性。虚拟 NET 令牌和 IIN 偏置的计算复杂度随网数增长，大规模部署时的效率需进一步评估。
2. **短互连泛化不足**：数据集中短互连（段数较少）样本稀疏（Figure 7），导致所有模型在短互连场景下的预测精度相对较低（Figure 4）。Si-GT 虽在长互连上表现最优，但短互连的泛化问题仍未根本解决。
3. **场景覆盖有限**：仅考虑单受害网-多攻击网的简化串扰情形，未覆盖多受害网同时切换、多攻击网协同作用等更复杂的实际场景。
4. **部署开销**：GPU 推理对于小尺寸图可能因核启动开销导致延迟偏高（Figure 8），实际部署时需根据图规模选择 CPU/GPU 执行策略。Si-GT 的参数量约为对应 GNN 主干的 3-6 倍（Table 7），虽小于 Graphomer 和 GraphGPS，但在资源受限的工业 EDA 环境中仍有压缩空间。

### 开放问题

1. **短互连泛化**：数据稀疏导致的短互连精度下降能否通过专门的数据增强（如合成短互连样本）或课程学习策略缓解？是否需要为不同互连长度设计分层的模型架构？

2. **复杂串扰场景扩展**：能否将 Si-GT 的网内-网间注意力机制扩展至多受害网-多攻击网的复杂串扰情形？这需要重新设计 NET 令牌的交互方式，并可能引入网间高阶耦合的层次化编码。

3. **模型压缩与部署**：如何在保持精度的前提下进一步压缩 Si-GT 的参数量和推理延迟？知识蒸馏、注意力剪枝或混合精度推理是否适用于物理偏置注入的 Transformer 架构？

4. **段级到汇级的误差累积**：当前的分段级预测到汇级预测存在误差累积（Table 4），其机理尚不明确。是否需要设计端到端的汇级训练架构，或在损失函数中显式建模误差传播路径？

5. **全芯片规模验证**：Si-GT 能否在工业级全芯片互连网络上保持精度和效率？这需要构建更大规模的数据集，并可能涉及图分区、层次化编码等工程优化策略。

## 原文 PDF

![[paperPDFs/ICLR_2026/Si_GT_Fast_Interconnect_Signal_Integrity_Analysis_for_Integrated_Circuit_Design_via_Graph_Transformers.pdf]]
