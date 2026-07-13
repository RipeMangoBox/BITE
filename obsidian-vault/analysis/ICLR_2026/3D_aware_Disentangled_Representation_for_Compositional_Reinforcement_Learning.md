---
title: "3D-aware Disentangled Representation for Compositional Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/3D_aware_Disentangled_Representation_for_Compositional_Reinforcement_Learning.pdf
project_link: null
code_link: null
aliases:
- 3BSRBTP
- 3ADRCRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "提出3D block-slot注意力机制，将对象槽进一步分解为多个属性块（如形状、颜色、大小、位置），并利用多视图Transformer和光场解码器实现3D感知解耦。"
primary_logic: "通过将对象表示分解为可解释的属性块，并利用块级交叉注意力策略，可以稳定地匹配当前状态与目标状态之间的对象属性，从而实现高效的组合泛化和视角无关的强化学习。"
claims:
- "我们的方法在FG-ARI、解耦性(D)、完整性(C)和信息性(I)上均优于OSRT，同时PSNR相当。"
- "结合3D block-slot表示和块变换器(BT)策略，在组合泛化(CG)和分布外(OOD)设置中取得了最高的成功率。"
- "我们的策略能够泛化到未见过的视角，在OOD单视图设置下仍保持高成功率。"
- "块级解耦质量直接影响GCRL性能：高DCI模型在所有泛化设置中均显著优于低DCI模型。"
---

# 3D-aware Disentangled Representation for Compositional Reinforcement Learning

> [!tip] 核心洞察
> 通过将对象表示分解为可解释的属性块，并利用块级交叉注意力策略，可以稳定地匹配当前状态与目标状态之间的对象属性，从而实现高效的组合泛化和视角无关的强化学习。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向组合强化学习的3D感知解耦表示 |
| 英文题名 | 3D-aware Disentangled Representation for Compositional Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=GE0IFoDx8a) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | 3D block-slot representation with block transformer policy |
| Dataset | Clevr3D, IsaacGym3D (GCRL) |

> [!tip] 效果简介
> - Clevr3D 上，FG-ARI 为 0.942，对比 0.365 (OSRT)，变化 +0.577。
> - Clevr3D 上，D (Disentanglement) 为 0.867，对比 0.140 (OSRT)，变化 +0.727。
> - Clevr3D 上，PSNR 为 31.11，对比 31.57 (OSRT)，变化 -0.46。

## 概要

本文针对现有基于2D图像的对象中心表示缺乏3D感知能力，且对象属性与相机位姿之间存在纠缠的问题，提出了一种面向组合强化学习（Compositional Reinforcement Learning, GCRL）的3D感知解耦表示方法。核心瓶颈在于：当面对遮挡、视角变化和多对象操作任务时，传统表示方法（如OSRT）因无法有效解耦对象属性，导致泛化能力差。

方法的核心因果机制是：提出**3D block-slot注意力机制**，将每个对象槽（object slot）进一步分解为多个可解释的属性块（如形状、颜色、大小、位置），并使用独立的原型向量（prototypes）和GRU进行块级更新。同时，设计**混合槽注意力架构**：对前景对象槽使用块-槽注意力，而对背景和智能体槽保留标准槽注意力，避免了训练崩溃和错误分解。在策略层面，提出**块变换器（Block Transformer, BT）策略**，在匹配的当前与目标状态对象之间执行块级交叉注意力（而非对象级），实现了稳定的属性级目标条件匹配和高效的组合泛化。

主要结果验证了该方法的有效性：在Clevr3D数据集上，方法在FG-ARI（0.942 vs 0.365）、解耦性D（0.867 vs 0.140）等指标上显著优于OSRT，同时PSNR相当（31.11 vs 31.57）。在IsaacGym3D的GCRL任务中，结合BT策略的方法在分布内（ID）设置下成功率达0.967 ± 0.017，组合泛化（CG）设置下为0.895 ± 0.011，分布外（OOD）设置下为0.828 ± 0.099，均大幅超越基线。在视角泛化实验中，方法在OOD单视图设置下仍保持0.758 ± 0.021的成功率，证明了其视角无关的3D感知能力。消融实验进一步表明，块级解耦质量（DCI指标）直接正向影响GCRL性能，且方法可使用次优掩码（如DINO背景掩码+运动学智能体掩码）进行训练，性能与使用GT掩码相当，增强了实际部署的可行性。



现有基于2D图像的对象中心表示（如DLPv2、SNeRL）在机器人操作任务中面临两个根本瓶颈：一是缺乏3D感知能力，无法处理视角变化和遮挡；二是对象属性与相机位姿之间存在纠缠，导致在组合泛化和分布外场景中性能严重退化。尽管OSRT等3D对象中心表示方法通过光场解码器实现了新视角合成，但其每个对象仅由一个单一槽向量表示，未对属性进行显式分解，因此解耦性能极差（FG-ARI仅0.365，解耦度D仅0.140），这从根本上限制了其在目标条件强化学习中的泛化能力——当场景中出现训练时未见过的属性组合时，策略无法准确匹配当前状态与目标状态中的对象。

本文的核心动机是：**通过将对象表示分解为可解释的属性块（如形状、颜色、大小、位置），并利用块级交叉注意力机制，实现3D感知的、视角无关的、可组合的对象表示，从而突破现有方法在组合泛化和视角泛化上的性能天花板。** 具体而言，作者提出3D block-slot注意力机制，将每个对象槽进一步分解为M个属性块，每个块通过概念记忆（prototype memory）进行独立更新；同时设计混合槽注意力架构——对前景对象使用块-槽注意力，对背景和智能体槽使用标准槽注意力——以避免训练崩溃。在策略层面，块变换器（Block Transformer）策略在匹配的对象之间进行块级交叉注意力，而非传统对象级交叉注意力，从而稳定地匹配当前状态与目标状态之间的对象属性。

该方法的因果机制在于：属性块的显式分解使得模型能够独立编码和操作每个对象的形状、颜色、大小和位置信息，而块级交叉注意力则允许策略在对象匹配时直接关注具体属性的差异，而非模糊的对象整体。这一设计直接解决了现有方法中“对象属性纠缠导致组合泛化失败”的核心问题——当训练集中红色方块和蓝色球体已出现，但红色球体是未见组合时，模型可以通过独立匹配颜色块和形状块来正确识别目标对象，而非依赖整体对象表示的相似度。



## 核心方法与创新机理

本文的核心创新在于提出了一种**3D感知的对象级解耦表示**及其配套的策略架构，从根本上解决了现有2D对象中心表示在遮挡、视角变化和多对象操作任务中泛化能力差的问题。其瓶颈在于，现有基于2D图像的对象中心表示（如OSRT、DLPv2）缺乏3D感知能力，且对象属性与相机位姿之间存在纠缠，导致模型无法在视角变化和属性组合变化时稳定工作。

**因果旋钮**是**3D block-slot注意力机制**。该机制将每个对象槽（slot）进一步分解为M个属性块（block），每个块独立编码一个可解释的属性（如形状、颜色、大小、位置）。具体地，从SRT编码器提取的场景级潜在表示 $\mathbf{F} = E_\theta(\{\mathbf{I}_i\})$ 出发，对象槽 $\mathbf{z}_n$ 被分解为 $\{\mathbf{z}_{n,m} \in \mathbb{R}^{D_{block}}\}_{m=1}^M$ 的拼接。每个块通过一个独立的概念记忆（prototype memory）和GRU进行迭代更新：$\mathbf{z}_{n,m} = \mathrm{GRU}_{\phi_m}(\mathbf{z}_{n,m}, \mathbf{u}_{n,m})$，其中 $\mathbf{u}_{n,m}$ 是块级注意力输出。这种设计使得每个块能够专门化地编码特定属性，从而实现属性级别的解耦。

**关键架构变化**体现在三个“changed slots”：

1. **对象表示结构**：从OSRT的单一槽向量变为多属性块拼接。这使表示从“对象级”降维到“属性级”，为后续的精确属性匹配和操作奠定了基础。

2. **槽注意力机制**：设计了**混合槽注意力架构**——对背景和智能体槽使用标准槽注意力，仅对前景对象槽使用块-槽注意力。消融实验（Table 10）和失败案例分析（Figure 14）明确表明，若对所有槽（包括背景和智能体）统一应用块-槽注意力，会导致训练崩溃和错误的场景分解。这一设计选择是方法稳定工作的关键。

3. **策略网络结构**：从EIT（Entity Interaction Transformer）的对象级交叉注意力，变为**块变换器策略**的块级交叉注意力。如图2所示，块级交叉注意力 $\mathbf{H}_n = \mathrm{CrossAttn}(\mathbf{z}_{o_n}^s, \mathbf{z}_{o_n'}^g)$ 直接在匹配对象之间的属性块上计算注意力，而非在排列不变的整个槽上。这使得策略能够稳定地匹配当前状态与目标状态中对应对象的属性，避免了对象级匹配的排列歧义问题。策略最终输出通过自注意力、池化注意力和MLP生成：$\mathbf{P} = \mathrm{SelfAttn}([\mathbf{h}_1, \dots, \mathbf{h}_{N-2}, \mathbf{z}_{ag}^s, \mathbf{z}_{ba}^g, \mathbf{a}_t])$，$\mathrm{Output} = \mathrm{MLP}(\mathrm{AttnPool}(\mathbf{P}))$。

**核心洞察**在于：通过将对象表示分解为可解释的属性块，并利用块级交叉注意力策略，可以稳定地匹配当前状态与目标状态之间的对象属性，从而实现高效的组合泛化和视角无关的强化学习。消融实验（Table 13）直接验证了这一因果链：高DCI（解耦性、完整性、信息性）模型在所有泛化设置（ID、CG、CG同色、OOD）中的成功率均显著优于低DCI模型，证明**块级解耦质量是GCRL性能的直接瓶颈**。



![[assets/figures/papers/iclr26_0001_GE0IFoDx8a_3D-aware_Disentangled_Representation_for_Composi/figures/001_Figure_1.jpg]]
*Figure 1: Overall structure of our method: Our proposed pipeline consists of two steps: representation learning and policy training. (a) Pre-training 3D block-slot encoder: The object slots are further decomposed into blocks of attributes. Then, the slot-mixer decoder mixes the object-centric representation to generate images at a query view. (b) Policy training with block transformer policy: We utilize the 3D block-slot encoder to extract a structured representation for the current observation and the goal image. The decomposed latent embedding serves as the input and the goal tokens, respectively, for our block transformer of the policy architecture*

该方法的整体流程分为两个阶段：**表示学习**和**策略训练**，如Figure 1所示。核心瓶颈在于现有2D对象中心表示缺乏3D感知能力，且对象属性与相机位姿纠缠，导致在遮挡和视角变化下泛化能力差。因果机制是通过将对象槽进一步分解为属性块，并利用多视图Transformer和光场解码器实现3D感知解耦。

**阶段一：3D Block-Slot表示预训练**

输入为多视图观测 $\{\mathbf{I}_i\}$，首先通过基于Transformer的SRT Encoder $E_\theta$ 聚合为场景级潜在表示 $\mathbf{F} = E_\theta(\{\mathbf{I}_i\})$（公式1）。核心创新在于**3D Block-Slot注意力机制**：将前景对象槽 $\mathbf{z}_n$ 进一步分解为 $M$ 个属性块 $\{\mathbf{z}_{n,m} \in \mathbb{R}^{D_{\text{block}}}\}_{m=1}^M$，每个块通过独立的概念记忆（GRU+MLP）更新（公式6）；而背景和智能体槽仍使用标准槽注意力更新（公式7）。这种混合注意力架构（mixture slot-attention）是关键设计——若对所有槽使用块-槽注意力会导致训练崩溃和错误场景分解（Figure 14）。

解码器采用**Slot Mixer**，这是一个3D感知光场解码器。给定查询射线特征 $\mathbf{x}$，通过归一化点积相似度计算槽矩阵的加权均值 $\bar{\mathbf{z}} = \mathbf{w}^\top \mathbf{Z}$（公式2），最终合成新视角图像。总损失函数 $\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{recon}} + \lambda_{\text{bg}} \mathcal{L}_{\text{bg}} + \lambda_{\text{ag}} \mathcal{L}_{\text{ag}}$（公式5）结合了L2重建损失（公式3）和辅助掩码损失（公式4），后者将背景/智能体槽的注意力加权区域与GT掩码对齐，确保槽分配的一致性。

**阶段二：块变换器策略（Block Transformer Policy）**

预训练后的3D Block-Slot编码器提取当前观测和目标图像的解耦表示。策略网络的核心是**块级交叉注意力**（block-wise cross-attention）：在匹配的对象之间，对属性块进行交叉注意力计算 $\mathbf{H}_n = \text{CrossAttn}(\mathbf{z}_{o_n}^s, \mathbf{z}_{o_n'}^g)$，再通过池化注意力得到 $\mathbf{h}_n$（公式8）。这区别于基线方法（如EIT）的对象级交叉注意力——块级操作能稳定匹配当前与目标状态中对应的对象属性，避免因对象排列不变性导致的匹配错误（Figure 2）。最终输出通过自注意力和MLP生成动作和Q值（公式9）。策略中仅使用前景块和智能体槽，因为背景信息在机器人操作任务中通常包含噪声。

**模块关系与数据流**：SRT Encoder → 3D Block-Slot注意力（混合架构）→ Slot Mixer解码器（训练时重建损失）→ 预训练编码器冻结 → 块变换器策略（块级交叉注意力）。输入为多视图图像（表示学习阶段）或单/多视图（策略推理阶段），输出为对象级解耦表示（表示学习）或动作（策略）。



### 3D Block-Slot 表示学习

本方法的核心瓶颈在于现有2D对象中心表示缺乏3D感知能力，且对象属性与相机位姿之间存在纠缠。为此，论文提出了**3D block-slot注意力机制**，将每个对象槽进一步分解为M个属性块（如形状、颜色、大小、位置），从而实现3D感知解耦。

**场景级潜在表示**：首先使用基于Transformer的SRT编码器 $E_\theta$ 将多视图观测聚合为场景级潜在表示：

$$
\mathbf { F } = E _ { \theta } ( \{ \mathbf { I } _ { i } \} )
$$

**块-槽注意力**：从潜在向量 $\mathbf{F}$ 中，对象槽 $\mathbf{z}_n$ 被分解为M个属性块的拼接 $\{ \mathbf{z}_{n,m} \in \mathbb{R}^{D_{\text{block}}} \}_{m=1}^M$。每个块的更新规则为：

$$
\mathbf { z } _ { n , m } = \mathrm { GRU } _ { \phi _ { m } } ( \mathbf { z } _ { n , m } , \mathbf { u } _ { n , m } ) \quad \Rightarrow \quad \mathbf { z } _ { n , m } + = \mathrm { MLP } _ { \phi _ { m } } ( \mathrm { LN } ( \mathbf { z } _ { n , m } ) )
$$

其中 $\mathbf{u}_{n,m}$ 是块级注意力计算出的更新向量。这种解耦更新的因果机制在于：每个块通过独立的概念记忆（concept memory）进行更新，使得不同属性块能够学习到特定的语义特征。

**混合槽注意力架构**：论文设计了一种混合注意力方案——对前景对象槽使用块-槽注意力，而对背景槽和智能体槽使用标准槽注意力。背景和智能体槽的更新规则为：

$$
\mathbf { z } _ { n ^ { \prime } } = \mathbb { G } \mathbb { R } \mathbb { U } _ { \phi _ { n ^ { \prime } } } ( \mathbf { z } _ { n ^ { \prime } } , \mathbf { u } _ { n ^ { \prime } } ) \quad \Rightarrow \quad \mathbf { z } _ { n ^ { \prime } } + = \mathbb { M } \mathrm { L } \mathbb { P } _ { \phi _ { n ^ { \prime } } } ( \mathrm { LN } ( \mathbf { z } _ { n ^ { \prime } } ) ) , \quad \mathrm { where ~ } n ^ { \prime } \in \{ \mathrm { bg } , \mathrm { ag } \}
$$

这一设计的必要性通过消融实验得到验证：对所有槽使用块-槽注意力会导致训练崩溃和错误场景分解（Figure 14），因为背景和智能体不具备可分解的属性结构。

**3D感知解码器**：解码器采用Slot Mixer（Sajjadi et al., 2022a），这是一个3D感知光场解码器。对于查询射线特征 $\mathbf{x}$，解码器通过归一化点积相似度计算槽矩阵的加权均值：

$$
\mathbf { w } = \mathrm { softmax } ( ( W _ { k } \mathbf { Z } ^ { \top } ) ^ { \top } ( W _ { q } \mathbf { x } ) ) , \quad \bar { \mathbf { z } } = \mathbf { w } ^ { \top } \mathbf { Z }
$$

**损失函数**：总损失函数由三部分组成：

$$
\mathcal { L } _ { \mathrm { total } } = \mathcal { L } _ { \mathrm { recon } } + \lambda _ { \mathrm { bg } } \mathcal { L } _ { \mathrm { bg } } + \lambda _ { \mathrm { ag } } \mathcal { L } _ { \mathrm { ag } }
$$

其中重建损失为新视角合成的L2损失：

$$
\mathcal { L } _ { \mathrm { recon } } = \underset { \theta } { \arg \min } \ \mathbb { E } _ { \mathbf { r } \sim \mathbf { I } _ { i } ^ { \mathrm { gt } } } \left\| C ( \mathbf { r } ) - \mathbf { I } _ { i } ^ { \mathrm { gt } } ( \mathbf { r } ) \right\| _ { 2 } ^ { 2 }
$$

辅助掩码损失 $\mathcal{L}_{\mathrm{bg}}$ 和 $\mathcal{L}_{\mathrm{ag}}$ 分别将背景槽和智能体槽的注意力加权区域与GT掩码对齐，其形式为：

$$
\mathcal { L } _ { \mathrm { bg } } = \sum _ { ( u , v ) \in \Omega } \left. \mathbf { w } _ { \mathrm { bg } } ( u , v ) \hat { \mathbf { I } } ( u , v ) - \mathbf { m } _ { \mathrm { bg } } ^ { \mathrm { gt } } ( u , v ) \mathbf { I } ( u , v ) \right. _ { 2 } ^ { 2 }
$$

$$
\mathcal { L } _ { \mathrm { ag } } = \sum _ { ( u , v ) \in \Omega } \left. \mathbf { w } _ { \mathrm { ag } } ( u , v ) \hat { \mathbf { I } } ( u , v ) - \mathbf { m } _ { \mathrm { ag } } ^ { \mathrm { gt } } ( u , v ) \mathbf { I } ( u , v ) \right. _ { 2 } ^ { 2 }
$$

消融实验表明，辅助掩码损失权重过大（$\lambda=1.0$）会降低PSNR和解耦性能，但有助于FG-ARI（Table 14）。更重要的是，使用次优掩码（DINO背景掩码+运动学智能体掩码）训练的模型，其GCRL性能与使用GT掩码的模型相当（Table 15），表明该方法不依赖于精确的GT分割。

### 块变换器策略（Block Transformer Policy）

基于3D block-slot表示，论文提出了**块变换器策略**，其核心创新在于使用块级交叉注意力而非对象级交叉注意力。

**目标条件强化学习目标**：

$$
\mathbb { E } _ { \pi } [ \sum _ { t = 0 } ^ { \infty } \gamma ^ { t } r _ { t } ] , \quad \mathrm { where } \ r _ { t } = r ( s _ { t } , a _ { t } , g )
$$

**块级交叉注意力**：对于当前状态和目标状态中匹配的对象，策略网络在块级别进行交叉注意力：

$$
\mathbf { H } _ { n } = \mathrm { CrossAttn } ( \mathbf { z } _ { o _ { n } } ^ { s } , \mathbf { z } _ { o _ { n ^ { \prime } } } ^ { g } ) , \quad \mathbf { h } _ { n } = \mathrm { PoolAttn } ( \mathbf { H } _ { n } )
$$

其中 $\mathbf{z}_{o_n}^s$ 和 $\mathbf{z}_{o_{n'}}^g$ 分别是当前状态和目标状态中第n个对象的块级表示。这种块级匹配的因果机制在于：通过直接观察属性块，可以稳定地匹配当前和目标表示中的对应对象，从而实现对特定对象属性的精确目标条件控制。

**策略网络输出**：经过自注意力和交叉注意力后，策略网络输出动作和Q值：

$$
\mathbf { P } = \mathrm { SelfAttn } ( [ \mathbf { h } _ { 1 } , \dots , \mathbf { h } _ { N - 2 } , \mathbf { z } _ { \mathrm { ag } } ^ { s } , \mathbf { z } _ { \mathrm { ba } } ^ { g } , \mathbf { a } _ { t } ] ) , \quad \mathrm { Output } = \mathrm { MLP } ( \mathrm { AttnPool } ( \mathbf { P } ) )
$$

策略中仅使用前景块和智能体槽，因为背景信息在机器人操作任务中通常包含噪声。

### 解耦质量与GCRL性能的因果关系

消融实验（Table 13）直接验证了解耦质量对GCRL性能的关键作用：高DCI模型在所有泛化设置（ID, CG, CG (same color), OOD）中均显著优于低DCI模型。这一因果链条的机制是：块级解耦使得策略能够精确识别和匹配当前状态与目标状态之间的对象属性差异，从而在组合泛化和分布外场景中仍能保持高成功率。

**关键超参数影响**：
- **块数量**（Table 11）：从4增加到16可提高解耦性能（D从0.322升至0.447），但FG-ARI略有下降，表明需要平衡分解粒度与对象分割质量。
- **原型数量**（Table 12）：从8增加到32可显著提高解耦性能（D从0.023升至0.480）和PSNR（从22.43升至25.33），说明更多的概念记忆有助于更精细的属性编码。



## 实验与关键发现

### 3D感知与解耦表示质量

论文的核心实验首先验证了3D block-slot表示在对象分解和属性解耦上的优势。在Clevr3D和IsaacGym3D数据集上，该方法与强基线OSRT进行了对比。**Table 1**显示，在Clevr3D上，所提方法的FG-ARI达到0.942，而OSRT仅为0.365，提升超过0.577。解耦性(D)从0.140跃升至0.867，完整性(C)从0.083提升至0.789，信息性(I)从0.452提升至0.844。值得注意的是，在PSNR指标上，所提方法(31.11)与OSRT(31.57)几乎持平，仅下降0.46 dB。这一模式表明，3D block-slot注意力机制在不牺牲新视角合成质量的前提下，极大地改善了场景分解和属性解耦。**Figure 7**的定性结果进一步佐证了这一点：该方法对前景对象、背景和智能体组件的分离效果显著优于OSRT。


![[assets/figures/papers/iclr26_0001_GE0IFoDx8a_3D-aware_Disentangled_Representation_for_Composi/figures/003_Table_1.jpg]]
*Table 1: 3D awareness with novel-view synthesis and decomposition performance: Our method outperforms OSRT across FG-ARI, disentanglement (D), completeness (C), and informativeness (I), while achieving comparable PSNR. The results indicate that our approach improves object decomposition and effectively disentangles information into latent vectors, while maintaining 3D-aware representation*

**Figure 9**的K-means聚类分析和**Figure 10**的特征重要性矩阵提供了块级解耦的定量证据。聚类结果显示不同块明确编码了不同属性：例如块6聚类于形状，块3聚类于颜色，块2聚类于大小，块4和块5分别聚类于x和y位置。特征重要性矩阵表明，与OSRT的槽表示相比，所提方法的每个块都表现出清晰的属性特异性编码，而OSRT的表示则纠缠严重。

### 目标条件强化学习的主结果

在IsaacGym3D推任务上，论文评估了目标条件强化学习(GCRL)性能，涵盖分布内(ID)、组合泛化(CG)、同色组合泛化(CG same color)和分布外(OOD)四种设置。**Table 2**报告了关键结果：

- 所提3D block-slot表示结合块变换器(BT)策略在所有设置中均取得最高成功率。在ID设置下，成功率高达0.967 ± 0.017，显著优于OSRT w/EIT的0.700 ± 0.160和DLPv2 w/EIT的0.889 ± 0.043。
- 在最具挑战性的OOD设置下，所提方法以0.828 ± 0.099的成功率大幅领先于DLPv2 w/EIT的0.422 ± 0.170和OSRT w/EIT的0.411 ± 0.130。SNeRL w/EIT在此设置下完全失败，成功率仅为0.000 ± 0.000。
- 在CG设置中，所提方法达到0.895 ± 0.011，与ID性能差距很小，表明其强大的组合泛化能力。**Figure 12**的行为可视化展示了智能体在所有评估场景中的成功轨迹。

**Figure 13**的训练曲线进一步揭示了学习动力学：3D block-slot表示与对象中心策略的组合实现了最快的学习速度，而块级变换器在长程任务中表现出更强的泛化能力。

### 视角泛化能力

**Table 3**评估了策略在不同视角设置下的泛化能力。所提方法在OOD单视图设置下仍保持0.758 ± 0.021的成功率，仅比ID多视图的0.802 ± 0.028下降约5.5%。这一结果验证了3D block-slot表示能够以视角无关的方式捕获3D对象信息。相比之下，OSRT w/EIT在OOD单视图下仅为0.288 ± 0.122，DLPv2 w/EIT为0.133 ± 0.058。值得注意的是，所提方法在OOD单视图(0.758)上的表现甚至优于其自身在OOD多视图(0.676)上的表现，这一反直觉现象可能源于单视图评估中随机性的减少，但论文未提供详细解释，需人工核实。


![[assets/figures/papers/iclr26_0001_GE0IFoDx8a_3D-aware_Disentangled_Representation_for_Composi/figures/007_Table_3.jpg]]
*Table 3: Success rate of view-generalization: Our model, which leverages a pre-trained 3D blockslot representation and a block transformer (BT), effectively captures 3D object information in a viewpoint-agnostic manner and achieves state-of-the-art performance across diverse generalization settings. We evaluate generalization in goal-conditioned RL tasks under four viewpoints settings: ID Multi-View (in-distribution multi-view), ID Single-View (in-distribution single-view), OOD Multi-View (out-of-distribution multi-view), and OOD Single-View (out-of-distribution single-view). Results are computed over 400 randomly sampled goals per seed, with all reported metrics averaged over three random seeds*

### 消融与诊断实验

**块数量与原型数量的影响**：**Table 11**显示，增加块数量(从4到16)可提高解耦性(D从0.322升至0.447)，但FG-ARI略有下降。**Table 12**表明，增加原型数量(从8到32)能显著提升解耦性能(D从0.023升至0.480)和PSNR(从22.43升至25.33)。这表明原型数量是影响解耦质量的关键超参数。

**解耦质量与GCRL性能的因果关系**：**Table 13**提供了关键证据：高DCI模型在所有泛化设置中均显著优于低DCI模型。在OOD设置下，高DCI模型成功率为0.828，而低DCI模型仅为0.423。这一结果直接验证了块级解耦是GCRL泛化性能的因果驱动因素，而非仅仅是相关现象。

**混合槽注意力架构的必要性**：**Table 10**和**Figure 14**展示了将所有槽(包括背景和智能体)都使用块-槽注意力的失败模式。当对所有槽应用块-槽注意力时，模型无法学习稳定属性，导致训练崩溃和错误的场景分解。相比之下，混合架构(前景对象使用块-槽注意力，背景和智能体使用标准槽注意力)实现了稳定的属性学习和正确的场景分解。

**辅助掩码损失的影响**：**Table 14**显示，辅助掩码损失权重过大(λ=1.0)会降低PSNR和解耦性能，但有助于FG-ARI。这表明需要在重建质量和分解质量之间进行权衡。**Table 15**和**Figure 15**进一步验证了方法的实用性：使用次优掩码(DINO背景掩码+运动学智能体掩码)训练的模型，其GCRL性能与使用GT掩码的模型相当。这一结果增强了方法在真实世界部署中的可行性。

**非对象中心基线的对比**：**Table 9**显示，基于VAE的MLP策略在ID设置下成功率仅为0.042 ± 0.015，在OOD下为0.000 ± 0.000，远低于所提方法。这表明对象中心表示对于多对象操作任务至关重要。

### 补充图表

![[assets/figures/papers/iclr26_0001_GE0IFoDx8a_3D-aware_Disentangled_Representation_for_Composi/figures/006_Figure_4.jpg]]
*Figure 4: Evaluation scenarios for compositional and out-of-distribution generalization: Composition generalization environments consist of objects with properties during training, but novel in their combinations. Out of such unseen combinations, we separately evaluate cases with objects of the same color when the factorization of attributes is unsuccessful. Out-of-distribution environments use objects with colors that were not present in the training set. Table 2: Performance of goal-conditioned RL: Our proposed 3D block-slot representation, combined with a block transformer (BT) policy, can effectively interpret goal conditions and exhibit superior performance in various scenarios. We compare the p...*

![[assets/figures/papers/iclr26_0001_GE0IFoDx8a_3D-aware_Disentangled_Representation_for_Composi/figures/009_Table_4.jpg]]
*Table 4: Hyperparameters of OSRT and 3D block-slot attention used in our experiments*

![[assets/figures/papers/iclr26_0001_GE0IFoDx8a_3D-aware_Disentangled_Representation_for_Composi/figures/011_Table_5.jpg]]
*Table 5: Hyperparameters of DLPv2 used in our experiments*




## 定位与知识库关联

本文提出的3D block-slot表示与块变换器策略，定位在**对象中心强化学习**与**3D感知解耦表示**两个社区的交汇点。其核心瓶颈识别为：现有2D对象中心表示（如DLPv2）缺乏3D感知，且3D对象中心表示（如OSRT, SNeRL）中对象属性与相机位姿纠缠，导致在遮挡、视角变化和多对象组合操作任务中泛化能力不足。因果干预手段是：将对象槽进一步分解为多个属性块（形状、颜色、大小、位置），并设计混合槽注意力架构——对前景对象槽使用块-槽注意力，对背景和智能体槽保留标准槽注意力。

**与基线的关键差异**体现在三个设计槽位的替换上。第一，对象表示结构：OSRT每个对象由一个单一槽向量表示，无属性分解；本文将其分解为M个属性块。第二，槽注意力机制：OSRT对所有槽使用统一注意力；本文对前景对象槽使用块-槽注意力，背景和智能体槽使用标准注意力。第三，策略网络结构：EIT（Entity Interaction Transformer）在对象级进行交叉注意力；本文的块变换器策略在匹配的对象之间进行块级交叉注意力。这些设计选择直接导致了显著的性能差距：在Clevr3D上，FG-ARI从OSRT的0.365提升至0.942，解耦性D从0.140提升至0.867，而PSNR仅从31.57略降至31.11，表明分解质量的提升并未以重建质量为代价。在IsaacGym3D的GCRL任务中，ID设置成功率从0.700 ± 0.160（OSRT w/EIT）提升至0.967 ± 0.017，OOD设置从0.422 ± 0.170（DLPv2 w/EIT）提升至0.828 ± 0.099。

**适用边界**由实验设置清晰界定。方法假设对象数量固定，使用匈牙利匹配进行一对一的当前-目标状态匹配，不支持动态或一对多的匹配场景。表示学习依赖多视图输入，单视图推理时性能有所下降（ID Single-View成功率0.726 vs. ID Multi-View的0.802），但仍优于基线。策略中仅使用前景块和智能体槽，丢弃了可能含噪声的背景信息，这在机器人操作任务中是合理的简化，但可能丢失部分场景上下文。

**局限与开放问题**有三。第一，当前方法不支持动态或一对多的匹配场景，限制了在更复杂环境中的适用性。第二，3D block-slot表示编码了类似语言标记的语义，如何将其与视觉-语言-动作（VLA）框架结合，实现更高级的推理和规划，是重要的未来方向。第三，方法依赖多视图输入进行表示学习，且解耦质量受块数量和原型数量等超参数影响（Table 11和Table 12显示，增加块数量从4到16可提高D从0.322至0.447，但FG-ARI略有下降；增加原型数量从8到32可显著提高D从0.023至0.480和PSNR从22.43至25.33），需要仔细调优。次优掩码实验（Table 15）表明，使用DINO背景掩码和运动学智能体掩码训练的模型，其GCRL性能与使用GT掩码的模型相当，这为减少对仿真GT掩码的依赖提供了可行路径，但在真实世界场景中如何更鲁棒地获取次优掩码仍需进一步研究。

**证据强度评估**：主要性能比较（Table 1, 2, 3）基于3个随机种子、每种子400个随机采样目标，统计量充分。消融实验（Table 11-15）覆盖了块数量、原型数量、解耦质量、掩码损失权重、次优掩码等关键设计维度，证据链完整。但部分定性分析（如K-means聚类和特征重要性矩阵）的量化支撑较弱，需要手动验证其在不同数据集上的可重复性。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/3D_aware_Disentangled_Representation_for_Compositional_Reinforcement_Learning.pdf

![[paperPDFs/ICLR_2026/3D_aware_Disentangled_Representation_for_Compositional_Reinforcement_Learning.pdf]]
