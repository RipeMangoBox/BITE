---
title: "DTO-KD: Dynamic Trade-off Optimization for Effective Knowledge Distillation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DTO_KD_Dynamic_Trade_off_Optimization_for_Effective_Knowledge_Distillation.pdf
project_link: null
code_link: null
openreview_forum_id: QMItTyQW92
aliases:
- DK
- DTO-KD
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "在每次迭代中动态优化蒸馏损失与任务损失的权重，使梯度对齐并消除主导。"
primary_logic: "将蒸馏训练建模为多目标优化，通过闭式解动态权衡梯度贡献，实现帕累托最优的平衡更新，无需手动调节损失权重。"
claims:
- "DTO-KD 实现了更低的梯度冲突和更均衡的梯度主导，优于基线方法。"
- "DTO-KD 在 ImageNet-1K 和 COCO 基准上均超越先前知识蒸馏方法，达到最优准确率。"
- "ImageNet-1K (DeiT-Ti) 上 Top-1 Accuracy (%) = 79.7"
- "ImageNet-1K (DeiT-S) 上 Top-1 Accuracy (%) = 83.1"
---

# DTO-KD: Dynamic Trade-off Optimization for Effective Knowledge Distillation

> [!tip] 核心洞察
> 将蒸馏训练建模为多目标优化，通过闭式解动态权衡梯度贡献，实现帕累托最优的平衡更新，无需手动调节损失权重。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DTO-KD：面向有效知识蒸馏的动态权衡优化 |
| 英文题名 | DTO-KD: Dynamic Trade-off Optimization for Effective Knowledge Distillation |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=QMItTyQW92) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | DTO-KD |
| Dataset | ImageNet-1K (DeiT-Ti), ImageNet-1K (DeiT-S), COCO (ViDT-nano), COCO (ViDT-tiny) |

> [!tip] 效果简介
> - ImageNet-1K (DeiT-Ti) 上，Top-1 Accuracy (%) 为 79.7，对比 74.5，变化 +5.2。
> - ImageNet-1K (DeiT-S) 上，Top-1 Accuracy (%) 为 83.1，对比 81.2，变化 +1.9。
> - COCO (ViDT-nano) 上，AP 为 43.7，对比 43.0，变化 +0.7。

## 概要

知识蒸馏（Knowledge Distillation, KD）旨在将大型教师模型的知识迁移到轻量级学生模型，但传统方法面临一个关键瓶颈：**梯度冲突（Gradient Conflict, GrC）与梯度主导（Gradient Dominance, GrD）**。当任务损失与蒸馏损失的梯度方向不一致（内积为负）或某一方梯度幅值压倒另一方时，学生模型无法有效同时优化两个目标，导致蒸馏效果受限。

本文提出 **DTO-KD（Dynamic Trade-off Optimization for Knowledge Distillation）**，将知识蒸馏训练建模为多目标优化问题。其核心思路是：在每次迭代中，通过求解 min-max 优化问题的闭式解，动态计算蒸馏损失与任务损失的最优权重，使两者的梯度对齐并消除主导，从而实现帕累托最优的平衡更新。该方法无需手动调节损失权重超参数，从根本上解决了梯度层面的冲突。

**核心结论：**
- DTO-KD 在梯度动态分析中展现出更低的冲突分数和更均衡的主导分数（Figure 1）。
- 在 ImageNet-1K 分类任务上，DeiT-Ti 学生模型达到 **79.7%** Top-1 准确率（+5.2%），DeiT-S 达到 **83.1%**（+1.9%），超越 VkD（Roy Miles & Deng, CVPR 2024）等 SOTA 方法。
- 在 COCO 目标检测任务上，ViDT-nano/tiny/small 学生模型分别取得 **43.7 / 47.4 / 49.6 AP**，一致优于 Token Matching（Song et al., ICLR 2021）和 VkD 等基线。
- 消融实验表明，轻量级投影器贡献最大（+2.1 AP），动态优化模块在此基础上进一步提升（+0.3 AP），梯度裁剪额外带来小幅增益（+0.1 AP）。

**方法定位：** DTO-KD 属于梯度层面的动态权衡蒸馏方法，区别于固定权重的传统 KD 框架（如 DeiT-KD、DearKD）。其知识库贡献在于：首次将 KD 训练中的梯度冲突与主导问题形式化为可求解的多目标优化，并提供闭式解实现高效的每迭代动态平衡。

知识蒸馏（Knowledge Distillation, KD）是模型压缩与迁移学习的核心范式，其基本思想是将大型教师模型的知识迁移到轻量级学生模型中。传统知识蒸馏的训练目标通常被形式化为任务损失与蒸馏损失的固定权重线性组合：

$$ \operatorname { L } _ { \operatorname { t o t } } ( \pmb \theta ) \triangleq \alpha _ { 1 } \mathrm { L } _ { \operatorname { d i s t i l l } } ( \pmb \theta ) + \alpha _ { 2 } \mathrm { L } _ { \operatorname { t a s k } } ( \pmb \theta ) $$

其中 $\alpha_1$ 和 $\alpha_2$ 是需要手动调节的固定超参数。这种静态加权策略在实际训练中暴露出两个根本性的梯度层面的问题：

**梯度冲突（Gradient Conflict, GrC）** 发生在蒸馏梯度 $\pmb{g}_{\mathrm{dist}}$ 与任务梯度 $\pmb{g}_{\mathrm{task}}$ 的内积为负时，即 $\langle \pmb{g}_{\mathrm{dist}}, \pmb{g}_{\mathrm{task}} \rangle < 0$。这意味着两个优化目标在参数空间中指向相互矛盾的方向，模型更新时一个目标的改善以牺牲另一个目标为代价。

**梯度主导（Gradient Dominance, GrD）** 则表现为两个梯度在量级上的严重失衡。当某一梯度的范数远大于另一方时，优化过程将实质上被该目标所支配，另一目标几乎无法对参数更新产生有效影响。

这两个问题共同导致知识蒸馏训练效率低下：学生模型无法同时从任务监督信号和教师知识中有效学习，蒸馏的增益被严重削弱。现有方法通常依赖人工设定固定的损失权重来缓解这一冲突，但静态权重无法适应训练过程中动态变化的梯度关系，本质上是一种次优的折中方案。

DTO-KD 的核心动机正是针对上述梯度层面的结构性问题。该方法将知识蒸馏重新建模为多目标优化（Multi-Objective Optimization, MOO）问题，在每次迭代中动态求解蒸馏损失与任务损失的最优权重，使两者梯度对齐并消除主导关系，引导优化过程走向帕累托最优的平衡更新。这一设计消除了手动调节损失权重的需求，从根本上解决了梯度冲突与梯度主导对知识迁移效果的制约。

## 核心方法与创新机理

DTO-KD 的核心创新在于将知识蒸馏的训练过程重新建模为**梯度层面的多目标优化问题**，从而动态、自适应地平衡蒸馏损失与任务损失之间的贡献，而非依赖固定的超参数权重。

### 改变的插槽：从固定权重到动态权衡

传统知识蒸馏方法的总损失定义为蒸馏损失与任务损失的线性组合：

$$ \operatorname { L } _ { \operatorname { t o t } } ( \pmb \theta ) \triangleq \alpha _ { 1 } \mathrm { L } _ { \operatorname { d i s t i l l } } ( \pmb \theta ) + \alpha _ { 2 } \mathrm { L } _ { \operatorname { t a s k } } ( \pmb \theta ) $$

其中 $\alpha_1, \alpha_2$ 是需要人工调节的固定超参数。这种静态加权策略直接导致了两个根本性问题：

1.  **梯度冲突（Gradient Conflict, GrC）**：当蒸馏梯度 $\pmb{g}_{\mathrm{dist}}$ 与任务梯度 $\pmb{g}_{\mathrm{task}}$ 的内积为负时（$\langle \pmb{g}_{\mathrm{dist}}, \pmb{g}_{\mathrm{task}} \rangle < 0$），两个目标在参数空间中朝着相互矛盾的方向更新，导致模型无法有效学习。
2.  **梯度主导（Gradient Dominance, GrD）**：当某一目标的梯度幅值远大于另一目标时，会压制另一目标的学习信号，造成优化失衡。

DTO-KD 改变了这一核心插槽：**损失权重策略**从“固定超参数 $\alpha_1, \alpha_2$”转变为“每次迭代通过求解 min-max 优化动态得出的权重 $\pi_{\mathrm{distill}}, \pi_{\mathrm{task}}$”。

### 因果机制：梯度对齐与主导消除

DTO-KD 通过以下机制实现因果干预：

**阶段一：度量改善速率。** 在每次参数更新 $\pmb{\theta}_{t+1} = \pmb{\theta}_t - \eta \pmb{g}_t$ 后，分别计算蒸馏损失和任务损失的相对改善速率：

$$ r _ { \mathrm { d i s t } } ( \pmb{g} _ t ) = \frac { \mathrm { L } _ { \mathrm { d i s t i l l } } ( \pmb { \theta } _ { t } ) - \mathrm { L } _ { \mathrm { d i s t i l l } } ( \pmb { \theta } _ { t + 1 } ) } { \mathrm { L } _ { \mathrm { d i s t i l l } } ( \pmb { \theta } _ { t } ) } , \quad r _ { \mathrm { t a s k } } ( \pmb { g } _ { t } ) = \frac { \mathrm { L } _ { \mathrm { t a s k } } ( \pmb { \theta } _ { t } ) - \mathrm { L } _ { \mathrm { t a s k } } ( \pmb { \theta } _ { t + 1 } ) } { \mathrm { L } _ { \mathrm { t a s k } } ( \pmb { \theta } _ { t } ) } $$

**阶段二：寻找帕累托最优更新方向。** 构建一个最小-最大优化目标，寻找使最差改善速率最大化的更新方向 $\pmb{g}_t$：

$$ \operatorname* { m a x } _ { \pmb { g } _ { t } \in \mathbb { R } ^ { n } } \operatorname* { m i n } _ { i \in \{ \mathrm { d i s t } , \mathrm { t a s k } \} } \frac { 1 } { \gamma } r _ { i } ( \pmb { g } _ { t } ) - \frac { 1 } { 2 } \| \pmb { g } _ { t } \| ^ { 2 } $$

通过拉格朗日对偶，该问题转化为在单纯形上最小化组合梯度的范数：

$$ \pmb { \pi } _ { t } ^ { * } \in \arg \operatorname* { m i n } _ { \pmb { \pi } \in \Delta } \frac { 1 } { 2 } \| \pmb { J } _ { t } \pmb { \pi } \| ^ { 2 } $$

其中 $\pmb{J}_t = [\nabla \log(\mathrm{L}_{\mathrm{distill}}(\pmb{\theta}_t)) \ |\ \nabla \log(\mathrm{L}_{\mathrm{task}}(\pmb{\theta}_t))]^\top$ 为对数损失的雅可比矩阵。当仅有两个损失时，该问题存在闭式解：

$$ \pi _ { 1 } ^ { * } = \frac { g _ { 22 } - g _ { 12 } } { g _ { 11 } + g _ { 22 } - 2 g _ { 12 } } , \quad \pi _ { 2 } ^ { * } = \frac { g _ { 11 } - g _ { 12 } } { g _ { 11 } + g _ { 22 } - 2 g _ { 12 } } $$

其中 $g_{ij}$ 为 Gram 矩阵元素。这一闭式解确保每次迭代的聚合梯度 $\pmb{g}_{\mathrm{tot}} = \pi_1^* \pmb{g}_{\mathrm{dist}} + \pi_2^* \pmb{g}_{\mathrm{task}}$ 对两个目标的贡献相等（Corollary 3.3），从而**同时消除梯度冲突和梯度主导**。

### 决定性证据

Figure 1 的梯度动力学分析直接验证了因果机制的生效：DTO-KD 相比基线方法实现了更低的梯度冲突分数（左图，冲突分数为负值且绝对值更小）和更均衡的梯度主导比例（右图，主导分数在 log-scale 下更接近 0）。在 ImageNet-1K 分类任务上，DTO-KD 将 DeiT-Ti 的 Top-1 准确率从 74.5% 提升至 79.7%（+5.2 pp），超越 **VkD**（Roy Miles & Deng, CVPR 2024）等梯度基 KD 方法（Table 1）。在 COCO 目标检测任务上，DTO-KD 同样在所有学生模型规模上取得最优 AP（Table 3）。

### 辅助创新：轻量级投影器

除动态权衡优化外，DTO-KD 还引入轻量级投影器（Projector）用于对齐教师与学生不同尺度的特征，消融实验表明该组件单独贡献 +2.1 AP 的提升（Table 4），是整体框架中增益最大的模块。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_QMItTyQW92/figures/003_Figure_2.jpg]]
*Figure 2: In DTO-KD, the teacher and student models simultaneously process the input image x. Each network consists of a Swin Transformer with a lightweight decoder. The teacher’s features (zt), and the student’s ( $z _ { s }$ ) . , are aligned using multiple lightweight projectors (P) at different scales. We formulate training as a multi-objective optimization (MOO) problem and propose a Dynamic Tradeoff Optimization module that jointly minimizes the distillation loss $\mathrm { L _ { d i s t i l l } }$ and the task-specific loss $\mathrm { L } _ { \mathrm { t a s k } }$ , guiding them toward Pareto optimality

DTO-KD 将知识蒸馏训练重新表述为**梯度层面的多目标优化**（Multi-Objective Optimization, MOO），其核心 pipeline 由两个关键模块串联构成：**轻量级投影器（Projector）** 与 **动态权衡优化模块（Dynamic Trade-off Optimization）**，整体架构见 Figure 2。

### 数据流与模块关系

1. **前向传播与特征对齐**
   教师模型与学生模型同时处理输入图像 $\pmb{x}$。两个网络均基于 Swin Transformer 并配备轻量级解码器。由于教师与学生的特征尺度可能不同，DTO-KD 在多个尺度上引入**轻量级投影器 $P$**，将教师的特征 $\pmb{z}_t$ 与学生特征 $\pmb{z}_s$ 对齐，用于计算蒸馏损失 $\mathcal{L}_{\text{distill}}$。同时，学生输出还用于计算任务特定损失 $\mathcal{L}_{\text{task}}$（如分类交叉熵或检测损失）。

2. **梯度计算与动态权衡**
   在反向传播阶段，分别计算蒸馏损失的梯度 $\pmb{g}_{\text{dist}}$ 和任务损失的梯度 $\pmb{g}_{\text{task}}$。传统 KD 方法直接以固定权重 $\alpha_1, \alpha_2$ 对两者线性求和得到总梯度 $\pmb{g}_{\text{tot}} = \alpha_1 \pmb{g}_{\text{dist}} + \alpha_2 \pmb{g}_{\text{task}}$，这容易引发**梯度冲突**（GrC：$\langle \pmb{g}_{\text{dist}}, \pmb{g}_{\text{task}} \rangle < 0$）和**梯度主导**（GrD：某一梯度量级远超另一梯度），使模型无法有效学习。

3. **动态权衡优化模块**
   该模块替代了固定权重策略。其核心机制是：在每次迭代中，通过求解一个 min-max 优化问题，得到使两个损失的最差改善速率最大化的更新方向。具体而言，构建由对数损失梯度组成的雅可比矩阵 $\boldsymbol{J}_t$，并在单纯形上最小化组合梯度的范数：
   $$
   \pmb{\pi}_t^{*} \in \arg\min_{\pmb{\pi} \in \Delta} \frac{1}{2} \| \boldsymbol{J}_t \pmb{\pi} \|^2
   $$
   当仅有两个目标时，该问题存在**闭式解**，可直接计算出最优权重 $\pi_1^{*}$（蒸馏）和 $\pi_2^{*}$（任务）：
   $$
   \pi_1^{*} = \frac{g_{22} - g_{12}}{g_{11} + g_{22} - 2g_{12}}, \quad \pi_2^{*} = \frac{g_{11} - g_{12}}{g_{11} + g_{22} - 2g_{12}}
   $$
   其中 $g_{ij}$ 为 Gram 矩阵元素。由此得到的聚合梯度 $\pmb{g}_t^{*} = \pi_1^{*} \pmb{g}_{\text{dist}} + \pi_2^{*} \pmb{g}_{\text{task}}$ 用于更新学生模型参数 $\pmb{\theta}_{t+1} = \pmb{\theta}_t - \eta \pmb{g}_t^{*}$。

### 关键设计动机

该 pipeline 的设计直指知识蒸馏的核心瓶颈：**梯度冲突使两个目标相互抵消，梯度主导则使优化偏向单一目标**。动态权衡优化模块通过每步自适应调整权重，使聚合梯度对两个目标贡献均等（Corollary 3.3），从而引导训练走向帕累托最优。Figure 1 的实验证据表明，相比固定权重基线，DTO-KD 实现了更低的梯度冲突分数和更均衡的梯度主导比，验证了该框架在梯度层面的有效性。

### 问题形式化

传统知识蒸馏将训练目标定义为任务损失与蒸馏损失的固定线性组合：

$$ \operatorname { L } _ { \operatorname { t o t } } ( \pmb \theta ) \triangleq \alpha _ { 1 } \mathrm { L } _ { \operatorname { d i s t i l l } } ( \pmb \theta ) + \alpha _ { 2 } \mathrm { L } _ { \operatorname { t a s k } } ( \pmb \theta ) $$

其中 $\alpha_1, \alpha_2$ 是需要手动调节的超参数。对应的总梯度为：

$$ \pmb { g } _ { \mathrm { t o t } } = \nabla \mathrm { L } _ { \mathrm { t o t } } ( \pmb { \theta } ) = \alpha _ { 1 } \pmb { g } _ { \mathrm { d i s t } } + \alpha _ { 2 } \pmb { g } _ { \mathrm { t a s k } } $$

这种固定权重策略导致两个关键瓶颈：**梯度冲突（GrC）**——当 $\langle \pmb{g}_{\mathrm{dist}}, \pmb{g}_{\mathrm{task}} \rangle < 0$ 时，两个目标在更新方向上相互抵消；**梯度主导（GrD）**——某一梯度的幅值远大于另一梯度，使得优化过程被单一目标支配。DTO-KD 将训练重新建模为多目标优化（MOO），在每次迭代中动态求解最优损失权重，使两个目标向帕累托最优方向演进。

### 两阶段动态权衡优化

DTO-KD 的核心模块采用两阶段策略，在每次迭代中自适应地确定蒸馏损失与任务损失的权重。

**第一阶段：参数试探更新与改善速率度量。** 在时刻 $t$，先用一个试探梯度 $\pmb{g}_t$ 更新学生模型参数 $\pmb{\theta}_{t+1} = \pmb{\theta}_t - \eta \pmb{g}_t$，然后分别计算蒸馏损失和任务损失的相对改善速率：

$$ r _ { \mathrm { d i s t } } ( g _ { t } ) = \frac { \mathrm { L } _ { \mathrm { d i s t i l l } } ( \pmb { \theta } _ { t } ) - \mathrm { L } _ { \mathrm { d i s t i l l } } ( \pmb { \theta } _ { t + 1 } ) } { \mathrm { L } _ { \mathrm { d i s t i l l } } ( \pmb { \theta } _ { t } ) } $$

$$ r _ { \mathrm { t a s k } } ( \pmb { g } _ { t } ) = \frac { \mathrm { L } _ { \mathrm { t a s k } } ( \pmb { \theta } _ { t } ) - \mathrm { L } _ { \mathrm { t a s k } } ( \pmb { \theta } _ { t + 1 } ) } { \mathrm { L } _ { \mathrm { t a s k } } ( \pmb { \theta } _ { t } ) } $$

**第二阶段：最小-最大优化求解最优更新方向。** 为找到使最差改善速率最大化的更新方向，构造如下优化目标：

$$ \operatorname* { m a x } _ { \pmb { g } _ { t } \in \mathbb { R } ^ { n } } \operatorname* { m i n } _ { i \in \{ \mathrm { d i s t } , \mathrm { t a s k } \} } \frac { 1 } { \gamma } r _ { i } ( \pmb { g } _ { t } ) - \frac { 1 } { 2 } \| \pmb { g } _ { t } \| ^ { 2 } $$

其中 $\gamma$ 是平衡超参数。通过构建雅可比矩阵：

$$ \boldsymbol { J } _ { t } = \left[ \nabla \log \left( \operatorname { L } _ { \mathrm { d i s t i l l } } ( \pmb { \theta } _ { t } ) \right) \ | \ \nabla \log \left( \operatorname { L } _ { \mathrm { t a s k } } ( \pmb { \theta } _ { t } ) \right) \right] ^ { \top } $$

可将原问题转化为对偶问题，在单纯形 $\Delta$ 上最小化组合梯度的范数：

$$ \pmb { \pi } _ { t } ^ { * } \in \arg \operatorname* { m i n } _ { \pmb { \pi } \in \Delta } \frac { 1 } { 2 } \| \pmb { J } _ { t } \pmb { \pi } \| ^ { 2 } $$

该问题在双目标情形下存在闭式解。令 Gram 矩阵元素 $g_{ij} = \langle \nabla \log \mathrm{L}_i, \nabla \log \mathrm{L}_j \rangle$，最优权重为：

$$ \pi _ { 1 } ^ { * } = \frac { g _ { 22 } - g _ { 12 } } { g _ { 11 } + g _ { 22 } - 2 g _ { 12 } } , \quad \pi _ { 2 } ^ { * } = \frac { g _ { 11 } - g _ { 12 } } { g _ { 11 } + g _ { 22 } - 2 g _ { 12 } } $$

其中 $\pi_1^*$ 对应蒸馏损失权重 $\pi_{\mathrm{distill}}$，$\pi_2^*$ 对应任务损失权重 $\pi_{\mathrm{task}}$。最终聚合梯度为 $\pmb{g}_{\mathrm{tot}} = \pi_1^* \pmb{g}_{\mathrm{dist}} + \pi_2^* \pmb{g}_{\mathrm{task}}$，用于更新学生模型。

### 理论保证

上述闭式解具有三条关键性质，从理论上保证了优化的稳定性：

- **梯度贡献均衡**（Corollary 3.3）：最优更新方向对两个损失梯度的内积贡献相等，即 $\langle \pmb{g}^*, \pmb{g}_1 \rangle = \langle \pmb{g}^*, \pmb{g}_2 \rangle$，直接消除了梯度主导问题。
- **更新幅值下界**（Corollary 3.4）：$\| \pmb{g}^* \| \ge \frac{1}{\sqrt{2}} \min(\| \pmb{g}_1 \|, \| \pmb{g}_2 \|)$，保证在梯度不平衡时更新不会坍缩。
- **更新幅值上界**（Corollary 3.5）：$\| g^* \| \leq \frac{\| g_1 \| \| g_2 \|}{|\| g_1 \| - \| g_2 \||}$，防止梯度尺度差异导致更新过大。

### 轻量级投影器

为对齐教师与学生网络不同尺度的特征，DTO-KD 引入多个轻量级投影器 $P$（Figure 2）。投影器将学生特征 $\pmb{z}_s$ 映射到教师特征 $\pmb{z}_t$ 的维度空间，用于计算蒸馏损失 $\mathrm{L}_{\mathrm{distill}}$。消融实验（Table 4）表明，投影器是贡献最显著的组件，单独引入即带来 +2.1 AP 的提升；动态优化模块在此基础上进一步贡献 +0.3 AP；梯度裁剪作为后处理步骤额外带来 +0.1 AP 的轻微增益。

## 实验与关键发现

### 核心瓶颈验证：梯度冲突与主导的消除

DTO-KD 的设计动机源于知识蒸馏训练中的两个根本性问题：**梯度冲突（Gradient Conflict, GrC）** 和**梯度主导（Gradient Dominance, GrD）**。论文通过梯度动态分析（Figure 1）系统性地验证了这一点。

在传统固定权重蒸馏（α₁、α₂ 为超参数）中，蒸馏梯度 $\pmb{g}_{\mathrm{dist}}$ 与任务梯度 $\pmb{g}_{\mathrm{task}}$ 的内积 $\langle \pmb{g}_{\mathrm{dist}}, \pmb{g}_{\mathrm{task}} \rangle$ 常呈现负值，表明两者方向不一致，互相抵消更新效果。同时，梯度范数之比 $\frac{|g_{\mathrm{dist}}|}{|g_{\mathrm{task}}|}$（对数尺度）在训练过程中剧烈波动，一种损失对参数更新的贡献压倒另一种，导致模型无法同时从两个目标中有效学习。

DTO-KD 通过每次迭代求解 min-max 优化问题，动态计算最优权重 $\pi_{\mathrm{distill}}$ 和 $\pi_{\mathrm{task}}$，使两个梯度的贡献趋于均衡。Figure 1 的实证结果表明：DTO-KD 的冲突分数（Conflict Score）显著高于基线（更接近零或正值），而主导分数（Dominance Score）更接近平衡线，验证了方法对 GrC 和 GrD 的有效抑制。

### ImageNet-1K 分类主结果

Table 1 报告了在 ImageNet-1K 数据集上，以 RegNetY-160 为教师模型的蒸馏结果。所有方法均训练 300 个 epoch，保证公平比较。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_QMItTyQW92/figures/004_Table_1.jpg]]
*Table 1: Object Classification task: DTO-KD on the ImageNet-1K dataset. Unless specified, each model is only trained for 300 epochs*

| 学生模型 | 方法 | Top-1 Acc. (%) | 参数量 |
|---------|------|---------------|--------|
| DeiT-Ti | 从头训练 | 74.5 | 6M |
| DeiT-Ti | DeiT-KD (Touvron et al., PMLR 2021a) | 74.5 | 6M |
| DeiT-Ti | DearKD (Chen et al., CVPR 2022) | 76.2 | 6M |
| DeiT-Ti | VkD-Ti (Miles & Deng, CVPR 2024) | 78.2 | 6M |
| DeiT-Ti | **DTO-KD (Ti)** | **79.7** | 6M |
| DeiT-S | 从头训练 | 81.2 | 22M |
| DeiT-S | **DTO-KD (S)** | **83.1** | 22M |

DTO-KD (Ti) 达到 79.7% Top-1 准确率，相比 DeiT-Ti 基线提升 **+5.2 pp**，超越此前最优的梯度基方法 VkD-Ti（78.2%）达 1.5 pp。DTO-KD (S) 达到 83.1%，较 DeiT-S 基线提升 +1.9 pp。这一结果直接支撑了核心洞察：**将蒸馏训练建模为多目标优化，通过闭式解动态权衡梯度贡献，能够实现帕累托更优的平衡更新，无需手动调节损失权重**。

### CIFAR-100 跨架构蒸馏

Table 2 展示了 CIFAR-100 上同构与异构架构的蒸馏结果。DTO-KD 在六种教师-学生配对中均取得最优准确率：

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_QMItTyQW92/figures/006_Table_2.jpg]]
*Table 2: Object Classification task: DTO-KD evaluated on both homogeneous and heterogeneous CNN architectures using the CIFAR-100 dataset. Table 3: Object Detection task: Comparison with other detectors on COCO, with student models distilled from a pre-trained ViDT-base. Note that DTO-KD consistently outpeforms all challenging knowledge distillation baseline approaches*

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_QMItTyQW92/figures/005_Table_2.jpg]]

- **同构架构**：ResNet-56（72.35%）、WRN-40-2（75.68%）、ResNet-32×4（76.40%）
- **异构架构**：ResNet-50→MobileNet-V2（70.90%）、ResNet-32×4→ShuffleNet-V1（77.95%）、ResNet-32×4→ShuffleNet-V2（78.22%）

异构蒸馏场景下，学生模型与教师模型结构差异显著，传统固定权重方法容易出现梯度主导问题。DTO-KD 的动态权衡策略在此类场景中优势尤为明显，表明其梯度对齐机制对架构差异具有鲁棒性。

### COCO 目标检测主结果

Table 3 报告了在 MS-COCO 数据集上，以预训练 ViDT-base 为教师蒸馏 ViDT 学生模型的检测结果。DTO-KD 在所有学生规模上均超越对比方法：

| 学生模型 | 方法 | AP |
|---------|------|-----|
| ViDT-nano | 无蒸馏 | 41.0 |
| ViDT-nano | Token Matching (Song et al., ICLR 2021) | 42.6 |
| ViDT-nano | VkD (Miles & Deng, CVPR 2024) | 43.0 |
| ViDT-nano | **DTO-KD** | **43.7** |
| ViDT-tiny | 无蒸馏 | 44.4 |
| ViDT-tiny | **DTO-KD** | **47.4** |
| ViDT-small | 无蒸馏 | 45.7 |
| ViDT-small | **DTO-KD** | **49.6** |

值得关注的是，DTO-KD-small（61M 参数）的 49.6 AP 已超越从头训练的 Swin-base（0.1B 参数，49.4 AP），表明动态权衡优化使得轻量学生模型能够更充分地吸收教师知识，实现参数效率的显著提升。

Figure 4 的错误分析进一步揭示：DTO-KD 同时降低了分类错误和定位错误，说明动态权衡在检测任务的两个子目标之间也实现了有效平衡。

### 消融实验：组件贡献分解

Table 4 的消融实验以 ViDT-nano 为基线（41.0 AP），逐步叠加 DTO-KD 各组件，量化每个模块的贡献：

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_QMItTyQW92/figures/007_Table_4.jpg]]

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_QMItTyQW92/figures/008_Table_4.jpg]]
*Table 4: Component’s Impact Assessment: An ablation study showing the impact of projector and optimisation. We also applied gradient clipping as a pre-processing step to both objectives to see its impact with and without DTO. Table 5: Distillation from different teachers for the Object Detection task: Comparison of ViDT on COCO2017 val set. We report AP for the student models distilled from different teacher models*

| 配置 | AP | Δ |
|------|-----|-----|
| 无蒸馏基线 | 41.0 | — |
| + 投影器 (Projector) | 43.1 | +2.1 |
| + 动态优化 (Optimization) | 43.4 | +0.3 |
| + 梯度裁剪 (Gradient Clipping) | 43.7 | +0.3 |

**投影器**是提升最显著的组件，带来 +2.1 AP 的增益。其作用是对齐教师与学生不同尺度的特征，为蒸馏损失提供有效的监督信号。**动态优化模块**在投影器基础上进一步提升 +0.3 AP，验证了梯度级动态权衡的独立价值。**梯度裁剪**作为后处理步骤，额外贡献 +0.1 AP（在无 DTO 配置下亦有轻微提升），表明控制梯度范数对训练稳定性有普遍益处。

### 动态平衡策略的行为分析

Figure 3 展示了训练过程中蒸馏损失权重 $\pi_{\mathrm{distill}}$ 和任务损失权重 $\pi_{\mathrm{task}}$ 的动态变化。DTO-KD 的梯度基向量优化表现出清晰的阶段性特征：**训练初期优先分配更高权重给蒸馏损失**，使学生快速对齐教师表示；**随着训练推进，权重逐渐向任务特定损失倾斜**，确保模型最终以目标任务为优化重心。这种自适应调度无需人工设定衰减策略，由优化问题的闭式解自然导出。

### 跨教师蒸馏的鲁棒性

Table 5 检验了 DTO-KD 在不同教师模型下的表现。以 ViDT-nano 和 ViDT-tiny 为学生，分别从 ViDT-small 和 ViDT-base 教师蒸馏。DTO-KD 在所有配对中均保持最优 AP，且与无蒸馏基线相比，从较弱教师（ViDT-small）蒸馏时仍能获得显著增益。这表明动态权衡策略对教师质量变化不敏感，具有较强的部署鲁棒性。

### 局限性与待验证问题

论文明确指出，DTO-KD 与多数知识蒸馏方法一样，**依赖可用数据进行蒸馏**。将其扩展到无数据蒸馏场景仍是一个开放挑战。此外，以下问题需要进一步验证：

1. **多教师蒸馏设定**：当前方法针对单教师场景设计，多教师下的动态权衡泛化能力未经实验检验。
2. **更大规模模型与不同模态**：现有实验集中在 ViT 基分类和检测模型，在 LLM 蒸馏或多模态任务上的表现有待探索。
3. **计算开销**：每次迭代需计算 Gram 矩阵并求解对偶问题，虽然论文提供了闭式解，但在极大规模模型上的实际开销需评估。

> **注意**：SRD 方法的引用元数据在分析中缺失，如需在正文中引用，请手动核实其出处。

## 定位与知识库关联

### 瓶颈诊断：梯度冲突与梯度主导

知识蒸馏的常规做法是将任务损失与蒸馏损失按固定权重线性组合：

$$ \operatorname { L } _ { \operatorname { t o t } } ( \pmb \theta ) \triangleq \alpha _ { 1 } \mathrm { L } _ { \operatorname { d i s t i l l } } ( \pmb \theta ) + \alpha _ { 2 } \mathrm { L } _ { \operatorname { t a s k } } ( \pmb \theta ) $$

DTO-KD 的诊断性发现是，这种固定加权策略在梯度层面引发两类系统性失效：

- **梯度冲突（GrC）**：蒸馏梯度与任务梯度的内积为负，即 $\langle \pmb{g}_{\mathrm{dist}}, \pmb{g}_{\mathrm{task}} \rangle < 0$，二者在参数空间中方向相悖，导致参数更新互相抵消。
- **梯度主导（GrD）**：某一目标的梯度幅值远大于另一目标，即 $\frac{|g_{\mathrm{dist}}|}{|g_{\mathrm{task}}|}$ 严重偏离 1，使得优化过程被单一目标绑架，另一目标形同虚设。

Figure 1 的梯度动力学分析给出了直接证据：基线方法在训练过程中冲突分数持续为负且主导分数严重失衡，而 DTO-KD 通过动态权重调整显著降低了冲突程度并平衡了梯度贡献。

### 核心机制：多目标优化与闭式权重求解

DTO-KD 将知识蒸馏重新表述为多目标优化（MOO）问题，核心创新在于将损失层面的权衡下沉到梯度层面。其操作流程分为两阶段：

1. **阶段一**：沿候选方向 $\pmb{g}_t$ 更新学生模型 $\pmb{\theta}_{t+1} = \pmb{\theta}_t - \eta \pmb{g}_t$，分别测量蒸馏损失与任务损失的相对改善速率 $r_{\mathrm{dist}}(\pmb{g}_t)$ 和 $r_{\mathrm{task}}(\pmb{g}_t)$。
2. **阶段二**：求解最小-最大优化问题，寻找使最差改善速率最大化的更新方向：

$$ \operatorname* { m a x } _ { \pmb { g } _ { t } \in \mathbb { R } ^ { n } } \operatorname* { m i n } _ { i \in \{ \mathrm { d i s t } , \mathrm { t a s k } \} } \frac { 1 } { \gamma } r _ { i } ( \pmb { g } _ { t } ) - \frac { 1 } { 2 } \| \pmb { g } _ { t } \| ^ { 2 } $$

通过拉格朗日对偶，该问题等价于在单纯形上最小化组合梯度的范数：

$$ \pmb { \pi } _ { t } ^ { * } \in \arg \operatorname* { m i n } _ { \pmb { \pi } \in \Delta } \frac { 1 } { 2 } \| \pmb { J } _ { t } \pmb { \pi } \| ^ { 2 } $$

当仅有两个目标时，最优权重存在闭式解：

$$ \pi _ { 1 } ^ { * } = \frac { g _ { 22 } - g _ { 12 } } { g _ { 11 } + g _ { 22 } - 2 g _ { 12 } } , \quad \pi _ { 2 } ^ { * } = \frac { g _ { 11 } - g _ { 12 } } { g _ { 11 } + g _ { 22 } - 2 g _ { 12 } } $$

其中 $g_{ij}$ 为 Gram 矩阵 $\pmb{J}_t \pmb{J}_t^\top$ 的元素。这一闭式解保证了每次迭代只需计算梯度内积即可获得帕累托最优的权重分配，无需手动调节 $\alpha_1$、$\alpha_2$。

理论分析进一步保证了该解的优良性质：
- **等贡献性**（Corollary 3.3）：$\langle \pmb{g}^*, \pmb{g}_1 \rangle = \langle \pmb{g}^*, \pmb{g}_2 \rangle$，最优更新方向对两个目标的梯度贡献相等，从根本上消除梯度主导。
- **范数下界**（Corollary 3.4）：$\| \pmb{g}^* \| \ge \frac{1}{\sqrt{2}} \min(\| \pmb{g}_1 \|, \| \pmb{g}_2 \|)$，保证更新不会因梯度失衡而坍缩。
- **范数上界**（Corollary 3.5）：$\| g^* \| \leq \frac{\| g_1 \| \| g_2 \|}{| \| g_1 \| - \| g_2 \| |}$，防止梯度尺度差异导致更新爆炸。

### 与现有方法的定位关系

**与固定权重 KD 方法的区别**：传统知识蒸馏（如 DeiT-KD，Touvron et al., PMLR 2021a）将 $\alpha_1$、$\alpha_2$ 设为固定超参数，需要大量调参且无法适应训练动态。DTO-KD 的权重 $\pi_{\mathrm{distill}}$、$\pi_{\mathrm{task}}$ 在每次迭代自适应求解，Figure 3 显示其动态平衡策略在训练初期优先蒸馏损失，随后逐步将重心转移至任务损失，实现了从“模仿教师”到“精通任务”的自然过渡。

**与梯度操控类方法的对比**：VkD（Roy Miles & Deng, CVPR 2024）同样在梯度层面操作知识蒸馏，是当前 SOTA 的梯度基 KD 方法。在 ImageNet-1K 上，DTO-KD (Ti) 达到 79.7% Top-1，超越 VkD-Ti 的 78.2%（Table 1）；在 COCO 目标检测上，DTO-KD 在所有学生规模（nano/tiny/small）上均优于 VkD（Table 3）。DTO-KD 的优势在于其权重求解有严格的优化理论支撑，而非启发式梯度修正。

**与结构蒸馏方法的区别**：DearKD（Chen et al., CVPR 2022）通过数据高效早期蒸馏改进 ViT 训练，SRD 利用结构关系蒸馏，这些方法聚焦于“蒸馏什么”，而 DTO-KD 聚焦于“如何平衡”，二者正交。DTO-KD 框架中的轻量级投影器（Projector）用于对齐师生特征尺度（Figure 2），消融实验（Table 4）表明投影器单独贡献 +2.1 AP，动态优化在此基础上额外贡献 +0.3 AP，验证了特征对齐与梯度平衡的互补性。

### 适用边界与局限

**已验证的适用场景**：
- **图像分类**：ImageNet-1K（DeiT-Ti/S 架构，Table 1）和 CIFAR-100（同构与异构 CNN 架构，Table 2）上均达到最优。
- **目标检测**：COCO 基准上基于 ViDT 检测器的蒸馏（Table 3），在 nano/tiny/small 三种规模上一致超越 Token Matching（Song et al., ICLR 2021）等基线。
- **跨教师鲁棒性**：Table 5 显示，在 ViDT-small 和 ViDT-base 两种教师模型下，DTO-KD 均稳定提升学生性能，表明方法对教师容量不敏感。

**明确的局限**：
- **数据依赖**：DTO-KD 设计前提是蒸馏数据可用，无法直接迁移至无数据蒸馏（data-free KD）场景。论文明确将此列为开放挑战。
- **多教师扩展未验证**：当前框架仅处理单教师双目标情形，多教师设定下目标数增加时，闭式解的泛化能力尚待检验。
- **更大规模模型与跨模态**：现有实验覆盖 DeiT-Ti/S（6M/22M 参数）和 ViDT-nano/tiny/small，在更大规模模型（如 ViT-L、Swin-L）或不同模态（如 NLP、语音）上的表现需要额外验证。

### 开放问题

1. **无数据蒸馏扩展**：如何在仅保留教师模型而无原始训练数据的场景下，构建等效的梯度冲突/主导诊断机制并实施动态权衡？
2. **多教师多目标泛化**：当蒸馏源扩展至多个教师或引入额外的正则化目标时，当前二目标闭式解需要推广至 $K > 2$ 的情形，其计算效率与收敛性如何？
3. **大规模与跨模态验证**：方法在 100M+ 参数模型和 NLP/语音等序列建模任务上，梯度冲突的模式是否类似，动态权衡策略是否依然有效？
4. **与架构搜索的联合**：动态权重策略能否嵌入 NAS 流程，在架构搜索阶段同时优化蒸馏强度，实现端到端的师生协同设计？

## 原文 PDF

![[paperPDFs/ICLR_2026/DTO_KD_Dynamic_Trade_off_Optimization_for_Effective_Knowledge_Distillation.pdf]]
