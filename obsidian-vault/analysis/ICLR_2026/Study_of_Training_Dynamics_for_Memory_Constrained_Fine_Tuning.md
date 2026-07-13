---
title: "Study of Training Dynamics for Memory-Constrained Fine-Tuning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Study_of_Training_Dynamics_for_Memory_Constrained_Fine_Tuning.pdf
project_link: null
code_link: null
aliases:
- STDMCFT
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/domain_adaptation_and_transfer_learning
core_operator: "动态随机选择待更新的输入通道子网络，使其期望梯度逼近全梯度，从而在严格内存限制下高效微调。"
primary_logic: "随机梯度具有重尾特性，梯度范数集中于少数通道；层重要性由架构决定且跨任务一致，可离线预选；通道重要性随任务变化，因此每训练轮动态随机重采样通道既可逼近全梯度又能满足内存约束。"
claims:
- "随机梯度在微调期间始终呈重尾分布（α<2），创造了天然的稀疏更新结构。"
- "层梯度范数排名跨下游任务高度一致（Spearman相关系数≥0.8），仅取决于网络架构。"
- "通道梯度范数分布在任务间显著不同（p≈0），无法离线预判。"
- "TraDy（D-TopK Random）在严格内存预算下，性能超过所有静态基线及确定性RGN方法。"
---

# Study of Training Dynamics for Memory-Constrained Fine-Tuning

> [!tip] 核心洞察
> 随机梯度具有重尾特性，梯度范数集中于少数通道；层重要性由架构决定且跨任务一致，可离线预选；通道重要性随任务变化，因此每训练轮动态随机重采样通道既可逼近全梯度又能满足内存约束。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向内存受限微调的训练动力学研究 |
| 英文题名 | Study of Training Dynamics for Memory-Constrained Fine-Tuning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=BhfIg0tuti) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/domain_adaptation_and_transfer_learning |
| Method | TraDy |
| Dataset | MobileNetV2-w0.35（跨CIFAR-10/100, CUB, Flowers, Food, Pets, VWW七个数据集）, MobileNetV2 on Food（最严格内存预算）, 所有架构与数据集（微调过程）, 不同任务下的层梯度范数分布相似性 |

> [!tip] 效果简介
> - MobileNetV2-w0.35（跨CIFAR-10/100, CUB, Flowers, Food, Pets, VWW七个数据集） 上，平均Top1准确率（%） 为 74.91 ± 0.64（TraDy, 最小预算27,946），对比 SU（静态稀疏更新），变化 TraDy显著优于SU。
> - MobileNetV2 on Food（最严格内存预算） 上，激活稀疏度 为 ~99%（TraDy及相关动态方法），对比 静态方法，变化 相似稀疏度下准确率更高。
> - 所有架构与数据集（微调过程） 上，重尾指数 α 为 始终小于2，对比 无（理论验证），变化 确认重尾梯度特性。

## 概要

在内存受限的边缘设备上微调预训练模型时，存储完整激活张量及其梯度所需的内存开销极大，使得全参数更新无法实现。本研究发现，随机梯度在微调全程始终呈现重尾分布（重尾指数 α<2），为稀疏更新提供了天然结构；同时，不同下游任务之间的层梯度范数排名高度一致（Spearman 相关系数 ≥0.8），说明层重要性主要由网络架构决定，可离线预判；而通道级别的梯度分布则严格依赖具体任务（p≈0），无法事先静态确定。基于上述动力学规律，本文提出 **TraDy**（Dynamic Top‑K Random）方法：首先利用重加权梯度范数（RGN）离线选出最关键的若干网络层，随后在每训练轮从这些层的全部输入通道中均匀随机采样，直至用尽预定义的内存预算。该策略使得被更新子网络的梯度在期望上逼近全梯度，同时严格满足内存约束。在广泛实验中，TraDy 在极小内存预算下显著优于静态稀疏更新基线（如 SU）和确定性动态选择方法（如 Velocity），例如在 MobileNetV2‑w0.35 的七个视觉数据集上平均准确率达 74.91%，并在 Food 数据集上实现约 99% 激活稀疏度、95% 权重导数稀疏度以及 97% 的权重导数计算量缩减。消融实验进一步表明，动态通道重采样与基于 RGN 的层预选是性能增益的主要来源，且动态随机性有助于逃离确定性方法可能落入的局部极小，使最终准确率甚至超越最优确定性子集选择（oracle）方法。该方法普遍适用于 CNN、Swin Transformer 和 BERT 等多种预训练架构，为边缘设备上的内存高效微调提供了一种通用范式。



随着预训练模型在视觉、语言等领域的泛化能力不断提升，将其迁移至下游任务的需求已从云端延伸至资源极度受限的边缘设备（如微控制器、移动终端）。然而，全参数微调要求存储所有激活张量及其对应的梯度，其内存开销往往超过典型边缘硬件（通常仅有几十至几百KB SRAM）的承载能力。这一“内存墙”构成了**在设备端进行模型个性化适配的核心瓶颈**。

现有的参数高效微调（PEFT）方案（如Adapter、LoRA）虽能降低可训练参数量，在梯度计算和中间激活上仍会产生不可忽视的临时内存。另一类面向极端内存约束的策略则直接对可更新参数进行**稀疏化**，例如静态选择固定的一组权重或通道并在整个微调期间保持不变（如 Sparse Update，SU）。这种做法**忽略了训练动力学在任务间的变异性**：其选择依据通常来自一次性的离线分析或全参数微调的“预热”阶段，当目标任务改变或内存预算进一步收紧时，固定不变的更新子图往往无法维持竞争性精度。

针对上述缺口，本文聚焦于**微调过程中的训练动力学**，从梯度分布的结构特性中寻找可操作的稀疏化依据。观察到以下三个关键事实：

- **重尾梯度天性**：在迁移学习的整个微调周期中，随机梯度始终呈现重尾分布（尾部指数 $\alpha<2$），表明大部分梯度范数集中在少数通道上（图2）。这为高稀疏度更新提供了天然的“聚焦”结构，但也意味着离线锁定更新子集将错失梯度峰值在训练过程中的动态漂移。
- **层重要性的一致性**：不同下游任务间，各层的梯度范数分布高度相关（Spearman 相关系数 $\geq 0.8$，图3a），说明层的相对重要性主要由网络架构决定，而与任务类别近乎无关。因此，**可离线预选重要的层**，而无需担心任务依赖性。
- **通道重要性的任务依赖性**：与层特性相反，通道级梯度范数分布在任务间存在统计显著差异（$p\approx 0$，图3b）。换言之，某一个通道在当前任务中是否关键，无法通过离线分析可靠预判，而必须依赖于在目标任务上动态获取的信号。

这三个发现揭示了一条清晰的路径：**层选择应由架构主导并离线完成，通道选择则需按训练轮在线重采样**。现有工作（SU 的静态通道选择、Velocity 的动态神经元选择等）均未同时利用这些结构性特征，导致在极严格的内存预算下要么无法逼近全梯度方向，要么陷入局部极小。

为此，本文提出 **TraDy**（一种基于训练动力学的动态通道选择方法），其核心动机是利用上述洞见构建一个**期望梯度无偏逼近全梯度**的稀疏更新框架：在离线阶段通过重加权梯度范数（RGN）锁定 top-K 层；在每轮训练中，从这些层的输入通道集内均匀随机采样，直至累积内存（权值内存 + 激活内存）达到预算上限。这种“层确定、通道随机刷新”的设计，既维持了架构赋予的上层结构，又通过随机重采样继承了梯度的重尾动力性质，在仅占用极少内存的条件下（可达到 99% 激活稀疏度、95% 权重导数稀疏度及 97% 的权重导数 FLOPs 缩减，图5）实现了优于静态基线和确定性 RGN 方法的微调性能（图4，表1）。



## 核心方法与创新机理

TraDy 的核心创新在于**将内存受限微调从静态、固定的子网络选择转变为动态、随机、内存感知的通道级重采样**，从而在严格内存预算下逼近全梯度更新的学习能力。相较现有静态基线（如 Sparse Update, SU）和确定性动态方法（如 Velocity），TraDy 通过两个关键设计变更实现了这一跃迁：**层重要性离线预选**与**通道在线随机重采样**。

### 1. 输入通道冻结：同时实现权重稀疏与激活稀疏
边缘设备微调的根本瓶颈在于必须同时存储权重梯度（权重导数）与激活张量，而传统参数冻结方法（如仅冻结输出通道）无法同时压缩两者。TraDy 选择在 **输入通道维度**上进行冻结，原因是输入通道的冻结不仅免除对应权重梯度的计算与存储，还会消除下游激活图中该通道相关的计算，从而**同时实现权重稀疏与激活稀疏**——这一点在方法论层面是唯一能达成双重稀疏性的路线（见 Sec.3.1, Eq.(3)）。这为后续在内存预算内最大化有效更新量提供了结构基础。

### 2. 架构决定的层重要性离线预选
静态方法通常依赖离线的精度贡献分析或默认更新所有层，不仅开销大，且与任务无关的先验往往不可靠。TraDy 所依据的发现是：**层的梯度范数分布主要由网络架构决定，跨下游任务高度一致**。实验显示不同数据集上的层梯度范数拓扑的 Spearman 相关系数不低于 0.8 (Fig.3a)，证明层重要性可以在离线阶段用任意可用任务校准一次，随后固定 “top-K” 重要层集合，无需在设备上重新评估（Prop.3.1, 附录 D.5）。这一设计将任务相关的搜索空间压缩到层内通道粒度，大幅降低实时决策的复杂性。

### 3. 通道重要性的任务依赖与动态随机重采样
与层不同，**通道梯度范数的分布随任务显著变化**，下游任务间的统计检验 p 值接近于零（Fig.3b），这意味着无法离线预判哪些通道关键。为在不增加内存开销的前提下利用这一任务相关性，TraDy 在每轮训练时于预选的重要层内 **均匀随机采样输入通道**，直至所选通道的总内存（权重内存+激活内存）达到预算上限（Algorithm 1, Eq.(3)）。其理论支撑来自随机梯度重尾分布（α 持续<2，Fig.2）——少数关键通道承载大部分梯度范数，随机采样有高概率覆盖这些高信息量通道，同时其期望梯度逼近全梯度（Eq.(9)）。这种动态重采样还引入了**良性随机性**：消融研究显示，确定性 RGN 方法（D‑Det RGN）可能因为追逐最大范数而陷入局部极小，而 TraDy 通过每轮重新混合显著通道集合，最终准确率甚至超越 oracle 方法（Sec.4.2 Discussion）。

### 4. 内存感知的梯度重加权（RGN）
为避免通道选择偏向参数规模大（内存成本高）的通道，TraDy 采用 **重加权梯度范数**（RGN）来度量通道重要性：

$$
\mathrm{RGN}_c = \frac{\|(\partial\mathcal{L}/\partial\mathcal{W}_i)_c\|_2}{\mathcal{C}_c^{\mathcal{W}_i} + \mathcal{C}_c^{\mathcal{A}_i}}
$$

并在层级别对 RGN 求和得到层重加权梯度范数（Eq.(8)），用于离线的 top‑K 层排序。实验证实，在同等内存预算下，基于 RGN 的选择相比直接使用原始梯度范数能保留更多有效信息，甚至当内存消减超过一半时仍可维持全精度（Fig.8a, 附录 D.3）。

### 5. 相对于基线的关键改进总结

| 创新点 | 基线（SU / Velocity） | TraDy | 证据强度 |
|--------|----------------------|-------|---------|
| **子网络更新策略** | 静态预选固定通道/层全程不变 | 每轮在预选层内动态随机重采样输入通道 | 高（Fig.4 消融显示动态显著优于静态） |
| **层选择先验** | 离线精度贡献分析（SU）或无先验（Velocity） | 基于 RGN 离线预选 top‑K 重要层，跨任务可复用 | 高（层梯度范数 Spearman≥0.8，Fig.3a；RGN 优于原始梯度，Fig.8a） |
| **选择粒度** | 全网络（Velocity）或固定通道（SU） | 从架构重要层中按内存预算随机抽取通道，粒度可控 | 高（Fig.11 显示 top‑K 层优于全网络随机） |

在 MobileNetV2‑w0.35 跨 7 个数据集的对比中，TraDy 在最小内存预算（27,946 单位）下取得平均 Top‑1 准确率 74.91±0.64，明显优于 SU 基线（Table 1）；同时实现高达 99% 激活稀疏度、95% 权重导数稀疏度和 97% 权重导数计算量缩减（Fig.5），验证了其在极端资源约束下的有效性。

### 6. 仍存的局限与未来方向
TraDy 优先选择靠后的深层，可能增加反向传播延迟，尽管权重导数计算量大幅降低。动态通道重采样目前仅验证了理论收益，要转化为边缘设备上的实际加速和能耗下降，仍需特殊的算子实现或编译优化（论文自述局限）。将这一范式扩展到 Transformer 架构并对自注意力头/层设计更精细的重要性评估，是论文提出的开放问题之一。



![[assets/figures/papers/iclr26_0016_BhfIg0tuti_Study_of_Training_Dynamics_for_Memory-Constraine/figures/001_Figure_1.jpg]]
*Figure 1: TRady dynamically reselects the subgraph to update within the memory budget Bmem*

### 问题形式化与内存建模
TraDy 将预训练模型视为 $n$ 个卷积层的顺序组合：
$$\mathcal{F}(\mathcal{X}) = (\mathcal{C}_{\mathcal{W}_n} \circ \mathcal{C}_{\mathcal{W}_{n-1}} \circ \cdots \circ \mathcal{C}_{\mathcal{W}_2} \circ \mathcal{C}_{\mathcal{W}_1})(\mathcal{X})$$
其中每一层的权重梯度对特定输入通道 $c$ 的依赖关系为：
$$\left[\frac{\partial \mathcal{L}}{\partial \mathcal{W}_i}\right]_{c',c,k,l} = \sum_{b=1}^{B}\sum_{h'=1}^{H'}\sum_{w'=1}^{W'} [\boldsymbol{A}_i^p]_{b,c,h,w} \left[\frac{\partial \mathcal{L}}{\partial \boldsymbol{A}_{i+1}}\right]_{b,c',h',w'}$$
基于此，输入通道 $c$ 的内存开销被精确量化为：
$$(\Theta_{\mathrm{space}})_c = \mathcal{C}_c^{\mathcal{W}_i} + \mathcal{C}_c^{\mathcal{A}_i}$$
这一定量关系是后续所有内存约束决策的数学基础（参见第3.1节）。

### Pipeline 概览
整体框架如 Figure 1 所示，TraDy 在给定的内存预算 $B_{\text{mem}}$ 约束下动态重选需更新的子图。其工作流包含三个核心组件：离线层预选、在线动态通道随机采样、内存约束控制器，三者协同完成从输入到预测的微调流程。

### 核心模块与运行机制

**层预选模块（Layer Pre-selection）**  
该模块利用重加权梯度范数（Reweighted Gradient Norm, RGN）对层进行离线排序。RGN 定义为通道梯度范数除以其内存开销：
$$\mathrm{RGN}_c = \frac{\left\|\left(\frac{\partial \mathcal{L}}{\partial \mathcal{W}_i}\right)_c\right\|_2}{\mathcal{C}_c^{\mathcal{W}_i} + \mathcal{C}_c^{\mathcal{A}_i}}$$
层的 RGN 为所有通道 RGN 之和：
$$\left\|\frac{\partial \mathcal{L}}{\partial \mathcal{W}_i}\right\|_{\mathrm{RGN}} = \sum_{c=1}^{C} \mathrm{RGN}_c$$
实证表明，层梯度范数的跨任务 Spearman 相关系数不低于 0.8（Figure 3a），意味着层重要性由架构决定且跨任务一致。因此，仅需在任意下游任务上进行少量轮次微调并记录 RGN 值，即可离线确定 top-$K$ 重要层。MobileNetV2 在 CIFAR-10 上，前 35 层已捕获 97% 的总 RGN（Figure 10）。

**动态通道随机采样模块（Dynamic Channel Random Sampling）**  
该模块在每个训练轮次开始时，从预选的 top-$K$ 层中输入通道集合内进行均匀随机采样，直至内存预算耗尽。其理论保证在于随机通道选择的梯度期望逼近全梯度期望：
$$\mathbb{E}\left[\sum_t \Delta\tilde{\mathcal{W}}\right] \simeq \mathbb{E}\left[\sum_t \Delta\mathcal{W}_{\{C^t\}}\right]$$
这一期望逼近关系使得动态重采样能有效逼近全梯度更新。与静态基线（如 S-TopK Random）不同的是，TraDy 每轮重新采样，引入有益随机性以避免确定性 RGN 方法可能陷入的局部极小（第4.2节 Discussion）。

**内存约束控制器（Memory Budget Controller）**  
控制器实时维护已选通道集，确保每一层所选通道的权重内存 $\mathcal{C}_c^{\mathcal{W}_i}$ 与激活内存 $\mathcal{C}_c^{\mathcal{A}_i}$ 之和不超过给定的总预算 $B_{\text{mem}}$。达成稀疏度的实际收益显著：在 MobileNetV2 的 Food 数据集上，激活稀疏度可达约 99%，权重导数稀疏度达 95%，权重导数计算量缩减 97%（Figure 5，第4.2节）。

### 选择粒度的关键设计决策
TraDy 选择沿输入通道维度冻结子网络，这被证明是唯一能同时实现权重稀疏和激活稀疏的粒度选择（第3.1节）。方法在层（架构先验）和通道（数据驱动动态采样）两个层级上耦合了两种异质性：层次重要性跨任务不变，通道重要性则随任务与训练轮次动态变化（Figure 3b 的 $p\approx 0$ 结果验证了通道分布的强任务依赖性）。这一分层决策使得框架在严格内存约束下仍能维持宏观梯度信息的无偏估计，同时将训练内存降至原完整微调的一半以下而不损失精度（附录 D.3）。



TraDy 利用微调过程中随机梯度的重尾特性（α<2，见图2）以及层重要性由网络架构决定、跨任务一致（Spearman 相关系数 ≥ 0.8，见图3a）而通道重要性随任务显著变化（p≈0，见图3b）的关键发现，在严格内存约束下实现高效微调。其核心思想是：**动态随机选择待更新输入通道子网络**，使每轮采样的梯度期望逼近全梯度（式9），同时严格将内存开销控制在预算内。以下分模块说明算法组成与支撑公式。

### 1. 层预选模块

该模块依据重加权梯度范数（RGN）离线确定需要更新的重要层（top-K），消除对无关层的梯度计算与存储。

- **RGN 定义**：对第 i 层第 c 个输入通道，记其梯度 L2 范数为 `∥(∂L/∂W_i)_c∥_2`，该通道需占用的权重与激活内存之和为 `C_c^{W_i} + C_c^{A_i}`，则其 RGN 为
  $$
  \mathrm{RGN}_c = \frac{\big\|\big(\frac{\partial \mathcal{L}}{\partial \mathcal{W}_i}\big)_c\big\|_2}{\mathcal{C}_c^{\mathcal{W}_i} + \mathcal{C}_c^{\mathcal{A}_i}} \tag{7}
  $$
  层的 RGN 定义为所有通道 RGN 之和：
  $$
  \Big\|\frac{\partial \mathcal{L}}{\partial \mathcal{W}_i}\Big\|_{\mathrm{RGN}} = \sum_{c=1}^{C} \mathrm{RGN}_c \tag{8}
  $$
  其等价于层平均梯度范数除以层总内存开销，因此能够避免单纯追求大梯度而忽略内存代价的偏倚。

- **离线预选策略**：在任意下游任务上短时间微调并记录各层 RGN，按其降序排列后截取前 K 个层作为后续动态采样的候选层（附录 D.5）。实验表明，不到 25% 的层即贡献了网络中超过 50% 的 RGN，而 50% 的层可覆盖 90% 以上的 RGN（图 10），证明了离线层预选的可行性与高效性。由于层重要性仅由网络架构决定（命题 3.1），该预选结果可跨任务复用，无需在部署端重复计算。

### 2. 动态通道随机采样模块

在每训练轮开始时，从预选的 top-K 层中均匀随机采样输入通道，直至内存预算耗尽（算法 1）。该过程保证了：

- **期望逼近全梯度**：设 t 轮采样的通道集合为 `{C^t}`，模型按此稀疏通道更新的权重变化量为 `ΔW_{{C^t}}`，全权重变化量为 `ΔW̃`。由于采样是均匀随机的，有
  $$
  \mathbb{E}\Big[\sum_t \Delta\tilde{\mathcal{W}}\Big] \simeq \mathbb{E}\Big[\sum_t \Delta\mathcal{W}_{\{C^t\}}\Big] \tag{9}
  $$
  即长期来看，稀疏梯度期望与全梯度期望一致，保证了收敛性。

- **引入有益随机性**：确定性选择（如按 RGN 降序）易陷入局部极小；动态随机重采样使得同一通道在不同轮被更新的机会均等，从而跳出局部解，最终准确率甚至超过 oracle 方法（表 1，图 4）。同时，随机性抵消了因固定的层预选可能遗漏部分重要通道的风险。

### 3. 内存约束控制器

控制器确保每轮所选通道集的总内存（权重内存 + 激活内存）不超过给定设备预算 `B_mem`。其基本依据是每个输入通道 c 的**空间复杂度**：
$$
(\Theta_{\mathrm{space}})_c = \mathcal{C}_c^{\mathcal{W}_i} + \mathcal{C}_c^{\mathcal{A}_i} \tag{3}
$$
采样过程中持续累加 `(Θ_space)_c`，一旦超过 `B_mem` 即停止。由于输入通道冻结可同时带来权重稀疏与激活稀疏（第 3.1 节），在极严格预算（如 27,946 参数）下，TraDy 仍可维持约 99% 激活稀疏度、95% 权重导数稀疏度和 97% 的权重导数计算节省（图 5）。

---

### 关键公式汇总

以下列出方法涉及的核心公式及其变量含义，其中符号约定为：`W_i` 第 i 层权重核，`A_i` 第 i 层输入激活，`L` 损失函数，`B` 批量大小，`C` 输入通道数，`C'` 输出通道数，`H',W'` 输出空间尺寸，`k,l` 核空间索引。

| 公式 | 表达式 | 意义 | 编号 |
|------|--------|------|------|
| 网络模型 | $\mathcal{F}(\mathcal{X}) = (\mathcal{C}_{\mathcal{W}_n} \circ \mathcal{C}_{\mathcal{W}_{n-1}} \circ \cdots \circ \mathcal{C}_{\mathcal{W}_1})(\mathcal{X})$ | n个卷积层顺序组合 | (1) |
| 权重导数 | $\big[\frac{\partial \mathcal{L}}{\partial \mathcal{W}_i}\big]_{c',c,k,l} = \sum_{b=1}^{B}\sum_{h'=1}^{H'}\sum_{w'=1}^{W'} [\boldsymbol{A}_i^p]_{b,c,h,w} \big[\frac{\partial \mathcal{L}}{\partial \boldsymbol{A}_{i+1}}\big]_{b,c',h',w'}$ | 损失对第 i 层权重核中对应特定输入通道 c 的梯度 | (2) |
| 通道空间复杂度 | $(\Theta_{\mathrm{space}})_c = \mathcal{C}_c^{\mathcal{W}_i} + \mathcal{C}_c^{\mathcal{A}_i}$ | 更新单个输入通道 c 所需的总内存（权重占用与激活占用之和） | (3) |
| 通道时间复杂度 | $(\Theta_{\mathrm{time}})_c = D^2 C' H' W'$ | 更新单个输入通道 c 的计算量（FLOPs） | (4) |
| 通道梯度范数 | $\big\|\big(\frac{\partial \mathcal{L}}{\partial \mathcal{W}_i}\big)_c\big\|_2 = \sqrt{\sum_{c',k,l}\big[\frac{\partial \mathcal{L}}{\partial \mathcal{W}_i}\big]_{c',c,k,l}^2}$ | 通道 c 的梯度 L2 范数，衡量其重要性 | (6) |
| 通道重加权梯度范数 (RGN) | $\mathrm{RGN}_c = \dfrac{\big\|\big(\frac{\partial \mathcal{L}}{\partial \mathcal{W}_i}\big)_c\big\|_2}{\mathcal{C}_c^{\mathcal{W}_i} + \mathcal{C}_c^{\mathcal{A}_i}}$ | 梯度范数除以内存开销，用于内存感知的通道重要性评分 | (7) |
| 层重加权梯度范数 | $\big\|\frac{\partial \mathcal{L}}{\partial \mathcal{W}_i}\big\|_{\mathrm{RGN}} = \sum_{c=1}^{C} \mathrm{RGN}_c$ | 层的整体 RGN，等价于层平均梯度范数与层总内存之比 | (8) |
| 期望逼近关系 | $\mathbb{E}\big[\sum_t \Delta\tilde{\mathcal{W}}\big] \simeq \mathbb{E}\big[\sum_t \Delta\mathcal{W}_{\{C^t\}}\big]$ | 动态随机采样的梯度期望逼近全梯度期望，保证收敛 | (9) |

这些公式构成了 TraDy 的内存分析、重要性评估与动态选择的基础：式(3)(4)量化每通道成本；(7)(8)实现内存感知的层与通道重要性排序；(9)从理论上保障了随机采样的有效性。



## 实验与关键发现

### 1. 梯度结构验证：重尾特性与层‑通道分离
TraDy 依赖两个核心假设：随机梯度具备天然的重尾结构，以及层与通道的重要性服从不同的分布规律。实验在 MobileNetV2‑w0.35、MCUNet‑in1、Proxyless‑w0.3 等多种架构与 CIFAR‑10/100、CUB、Flowers、Food 等七个下游任务上验证了这些假设。

- **随机梯度在整个微调期间始终保持重尾分布**（图 2）。重尾指数 α 在所有设置下稳定低于 2，意味着梯度范数高度集中于少数通道，其余通道的贡献可忽略。这为稀疏更新提供了直接的剪枝基础。
- **层梯度范数排名跨任务高度一致**（图 3a）。不同下游任务之间层梯度范数的 Spearman 相关系数始终不低于 0.8，表明层的相对重要性主要由网络架构自身决定，而非特定任务。因此可以在**离线阶段**通过少量样本标定重要层，摆脱在线全量排序推断所带来的内存与时间开销。
- **通道梯度范数分布随任务显著变化**（图 3b）。t‑检验 p 值近乎为 0，证实通道级的重要性在任务间不存在稳定排序，无法像层那样离线预判。这一发现直接排斥静态通道预选策略，要求**训练时动态重采样**。

![[assets/figures/papers/iclr26_0016_BhfIg0tuti_Study_of_Training_Dynamics_for_Memory-Constraine/figures/004_Figure_2.jpg]]
*Figure 2: Evolution of stochastic gradient heavy-tailed index $\alpha _ { t }$*

![[assets/figures/papers/iclr26_0016_BhfIg0tuti_Study_of_Training_Dynamics_for_Memory-Constraine/figures/006_Figure_3.jpg]]
*Figure 3: Validation of channel and layer proposition across seeds and datasets for MobileNetV2*

### 2. 有限内存下的微调性能
表 1 给出了不同内存预算下动态选择策略与静态基线 Sparse Update (SU) 在三个预训练 CNN 上的平均 top‑1 准确率。TraDy（D‑TopK Random）在极小预算（27 946 单位）下达到 74.91 % 的平均准确率，在所有预算层级均明显超越 SU，且整体优于确定性 RGN 方法（D‑Det RGN）及 Velocity。该优势在 Swin Transformer（表 2）以及 BERT/RoBERTa（表 3）上同样成立，证明 TraDy 不仅适用于卷积网络，也可推广至 Transformer 架构的微调。

性能提升的因果链路可概括为：① 层预选屏蔽了大量无梯度层，避免将内存浪费在低贡献层；② 每轮从预选层的输入通道中均匀随机采样，保证梯度期望在长时间尺度上逼近全梯度，同时每次迭代的实际内存消耗被严格限制在预算内；③ 随机重采样引入的探索性噪声使优化器能够逃离确定性 RGN 方法容易陷入的局部极小。

### 3. 消融实验：动态重采样与层预选的决定性作用
图 4 从三个维度分解 TraDy 的优势：
1. **动态 vs. 静态**：D‑TopK Random（TraDy）的最终准确率大幅优于其静态版本 S‑TopK Random，证实**按轮重选通道**是性能核心。
2. **层预选 vs. 全网络随机**：仅从 top‑K 层采样的 D‑TopK Random 胜过全网络随机选择（D‑Full Random），说明离线选层能有效滤除无意义的更新。
3. **RGN 重加权 vs. 原始梯度范数**：通过引入内存‑梯度权衡的重加权梯度范数（RGN），在同等内存下移除超过一半的参数量仍可保留全精度（图 8a）。相比之下，直接按原始梯度范数冻结通道会导致精度立即下降。

进一步的分析表明，确定性 RGN（D‑Det RGN）总是贪婪地选择范数最大的通道，使其梯度方向偏离全梯度期望，容易陷入局部极小；TraDy 通过动态随机采样实现“平均方向上跟随非零梯度，同时引入有益随机性”，最终在多个任务上甚至超越了仅保留最大范数通道的 oracle 策略（第 4.2 节讨论）。

### 4. 计算与内存效率
在 Food 数据集上对 MobileNetV2 进行内存受限微调时，TraDy 展现出极高稀疏性：激活稀疏度约 99 %，权重导数稀疏度 95 %，且权重导数的 FLOPs 减少 97 %（图 5）。该稀疏度并非以牺牲准确率为代价——在相同稀疏水平下，TraDy 的准确率仍显著高于静态稀疏更新方法。内存节省得益于同时冻结非选中通道的激活与对应权重导数，这正是输入通道维度冻结相较于输出通道或全层冻结的独特优势。

### 5. 失败模式与局限
两种失败模式值得关注：
- **深层偏置与反向传播延迟**：TraDy 倾向于选择深度更深的层更新，因为这些层的梯度范数普遍更高（第 3.3 节）。虽然权重导数计算量锐减，但更深层的反向传播可能增加端到端延迟，在当前设备上未必能立即转化为实际加速。
- **确定性贪心方法易陷入局部极小**：D‑Det RGN 等确定性方法缺乏探索，在部分任务上表现甚至弱于全随机选择，印证了动态随机性的必要性。

此外，动态通道重采样需要专项的硬件调度支持才能释放理论效率增益；当前实验仅验证了算法层面的稀疏性和 FLOPs 节省，尚未在边缘设备上测量实际延迟与能耗（附录 A）。上述局限指出了后续硬件‑算法协同优化的方向，同时也提示在极严格延迟约束下需谨慎选择 top‑K 层的深度。

### 补充图表

![[assets/figures/papers/iclr26_0016_BhfIg0tuti_Study_of_Training_Dynamics_for_Memory-Constraine/figures/025_Table_1.jpg]]
*Table 1: Comparison of final top1 test accuracies between SU and dynamic channel selection strategies over various pretrained CNN models, datasets, and budgets*

![[assets/figures/papers/iclr26_0016_BhfIg0tuti_Study_of_Training_Dynamics_for_Memory-Constraine/figures/010_Figure_5.jpg]]
*Figure 5: (a) Weight sparsity evolution dur-(b) Activation sparsity evolution (c) Computational savings in weight derivaing training. during training. tive FLOPs. Figure 5: Efficiency metrics comparison across channel selection strategies during MobileNetV2 fine-tuning on Food dataset under memory constraint. Results show evolution of sparsity levels and computational savings throughout training*

![[assets/figures/papers/iclr26_0016_BhfIg0tuti_Study_of_Training_Dynamics_for_Memory-Constraine/figures/017_Figure_8.jpg]]
*Figure 8: Channel thresholding results based on gradient norm. Each point represents a complete training run with respect to a pre-defined threshold ε. Plots show: (a) final accuracy vs. total memory usage, (b) final accuracy vs. total computational cost, and (c) total updated channel count vs. total memory usage*



## 定位与知识库关联

TraDy 通过“离线预选重要层 + 每轮随机采样通道”实现内存受限的迁移微调，其核心经验发现是：随机梯度在微调全程保持重尾分布（重尾指数 α<2，图2），天然构成稀疏更新的结构；层重要性由架构决定且跨任务一致（Spearman 相关系数 ≥0.8，图3a），而通道重要性随任务显著变化（p≈0，图3b），因此动态重采样通道并以期望逼近全梯度（公式(9)）能够在严格内存预算下收敛到高性能。

**与静态基线（SU）的关系**  
Sparse Update (SU, Lin et al. 2022) 采用离线精度贡献分析预选固定的通道/层，全程不变更新。TraDy 将这一“静态预选固定子网络”的策略替换为“动态随机重采样输入通道”（算法1），同时利用 RGN（Reweighted Gradient Norm）离线预选高重要性层（命题3.1，附录 D.5），从而在相同的激活与权重导数内存约束下实现更优的准确率。实验表明，在 MobileNetV2-w0.35 七个下游数据集上，TraDy 的平均 Top1 准确率（74.91%）显著优于 SU，并且在最严格预算（≈27,946 内存单位）下优势更明显（表1）。消融实验进一步确认，动态重选对性能提升的贡献远大于静态方案（D-TopK Random vs. S-TopK Random，图4）。

**与动态神经元/通道选择工作的比较**  
Velocity（Quélennec et al. 2024）采用动态神经元选择，但不具备内存感知的层预选与通道粒度的内存建模。TraDy 将选择粒度定义在“输入通道”级别，从而同时获得权重稀疏和激活稀疏（可达到 99% 激活稀疏度、95% 权重导数稀疏度，图5）。相比于确定性 RGN 选择（D-Det RGN），TraDy 的动态随机采样避免了因追逐最大梯度范数而陷入局部极小，其最终准确率超过包括确定性 oracle 在内的所有动态策略（第4.2节 Discussion）。此外，附录 B 指出，PaCA 方法对应于本文的 S-Full Random（静态全网络随机）基线，性能表现最差，侧面验证了层预选与通道动态重采样的必要性。

**适用边界与部署前提**  
TraDy 在卷积网络（MobileNetV2、ResNet-18、EfficientNet-B0 等）和部分 ViT 类架构（SwinT）以及 BERT/RoBERTa 上均展示了有效性（表2、3）。其离线层预选步骤仅需少量轮次在任一相关下游任务上记录 RGN 即可稳定建立层重要性排序（附录 D.5），不依赖特定任务。然而，该方法天然倾向于选择深层网络中的靠后层进行更新，这可能导致反向传播路径变长，增加延迟（附录 A）。动态重采样要求每个 epoch 重新选择通道，在实际边缘设备上需要专门的调度和计算图优化才能将理论的内存节省转化为可测量的加速与功耗下降——目前论文仅报告了理论 FLOPs 缩减（≥97%）和稀疏度，但缺乏实测的端到端延迟与能耗数据。对于超大模型（如 BERT-Large），固定的 top‑K 层选择策略可能需要更复杂的校准以适应不同的信息传播模式，且原始 Transformer 自注意力层的细粒度（头/序列维度）重要性尚未被显式建模。

**局限与风险**  
1. **深层更新延迟**：选择深层特征层虽然可大幅降低权重导数计算量，但反向传播需穿过更多层，可能增加整体延迟，尤其在轻量设备上可能抵消部分收益（附录 A）。  
2. **动态采样的实现复杂性**：当前分析仅基于算法层面的稀疏性，未在真实硬件（MCU/边缘 NPU）上进行部署优化与实测。将动态通道重新指派转化为高效的运行时代码生成仍需工程验证。  
3. **通道范数估计的噪声**：利用 mini‑batch 梯度范数作为重要性代理，在极端小 batch 时可能存在噪声，需验证其对极端内存预算（如仅更新 1-2 个通道）的稳定性。

**开放问题**  
- 如何将动态通道选择扩展至 Transformer 架构，并对多头自注意力中的“头”和序列维度设计内存感知的重要性评分？目前对 SwinT 的尝试仍沿用卷积视角，可能未充分捕捉注意力机制的稀疏结构。  
- 能否利用激活梯度的天然稀疏性（如大量零梯度）压缩反向传播通道，进一步降低深层更新的额外开销，甚至实现“无计算”的跳过？  
- 如何将选层的理论加速转换为真实的嵌入式指标（延迟、能耗），建立与商业部署工具链的接口？  
- 对于 BERT-like 超大模型，离线预选的 top‑K 层是否总能保证在微调后期不会失效（即后期重要层排序是否保持不变）？需要更系统的监测与自适应 K 选择策略。  
- 动态随机采样目前采用均匀随机，能否根据历史梯度统计引入重要性偏置的采样分布，在保持无偏期望的同时提高收敛速度？



## 原文 PDF

![[paperPDFs/ICLR_2026/Study_of_Training_Dynamics_for_Memory_Constrained_Fine_Tuning.pdf]]
