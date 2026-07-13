---
title: "Approximately Piecewise E(3) Equivariant Point Networks"
type: paper
paper_level: A
venue: ICLR
year: 2024
pdf_ref: paperPDFs/ICLR_2024/Approximately_Piecewise_E_3_Equivariant_Point_Networks.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/apen/
aliases:
- APE3EPN
tags:
- ICLR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/segmentation
core_operator: "分区预测的不确定性δ(Q)和抽取非适当子分区的概率λ(Q)共同决定了等变近似误差的上界。"
primary_logic: "保持对较细（子）分区的等变性可保证对真实分区的等变性；通过组合从细到粗的分区预测层，并利用δ和λ来控制和绑定等变近似误差。"
claims:
- "APEN框架提供了对分片E(3)等变近似误差的可控边界，该边界仅依赖于分区预测的不确定性量和抽取不良分区的概率。"
- "定理1证明了采用硬指派（argmax）的层形式φ属于(G,Q)等变函数类，其误差被(λ(Q_simple)+δ(Q))M所限制。"
- "分区预测模型通过最小化高斯混合模型负对数似然和KL散度正则化能量来学习，且当σ→0时δ(Q)→0且λ(Q)≤λ(Q_simple)。"
- "在人体部位分割和一次性泛化场景的实例分割任务中，APEN的mIoU显著优于全局等变网络（EPN）和非等变基线（PointNet, DGCNN, VN）。"
---

# Approximately Piecewise E(3) Equivariant Point Networks

> [!tip] 核心洞察
> 保持对较细（子）分区的等变性可保证对真实分区的等变性；通过组合从细到粗的分区预测层，并利用δ和λ来控制和绑定等变近似误差。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 近似分片E(3)等变点网络 |
| 英文题名 | Approximately Piecewise E(3) Equivariant Point Networks |
| 会议/期刊 | ICLR 2024 |
| Links | [paper](https://arxiv.org/abs/2402.08529) · [Project](https://research.nvidia.com/labs/toronto-ai/apen/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/segmentation |
| Method | APEN |
| Dataset | Human body parts segmentation (Random split on SMPL/DFAUST), Human body parts segmentation (Unseen random seq. on DFAUST), Human body parts segmentation (Unseen seq. on DFAUST), One-shot generalization on DynLab real-world room scans |

> [!tip] 效果简介
> - Human body parts segmentation (Random split on SMPL/DFAUST) 上，mean IoU (%) 为 94.2，对比 89.6 (EPN) / 84.4 (PointNet)，变化 +4.6 over EPN。
> - Human body parts segmentation (Unseen random seq. on DFAUST) 上，mean IoU (%) 为 92.2，对比 77.8 (EPN) / 78.5 (PointNet)，变化 +14.4 over EPN。
> - Human body parts segmentation (Unseen seq. on DFAUST) 上，mean IoU (%) 为 93.5，对比 84.1 (EPN) / 80.1 (PointNet)，变化 +9.4 over EPN。

## 概要

**核心问题**：点网络在处理三维几何数据时，理想情况下应具备对刚体运动（旋转、平移、反射）的等变性。然而，真实世界的三维场景通常由多个独立运动的部件组成，全局的E(3)等变性无法刻画这种分片对称性。精确的分片E(3)等变建模要求事先知晓点云的真实分区——这一条件在实际中难以满足。分区预测的不完美会引入等变近似误差，而如何控制这一误差是此前方法未能解决的根本瓶颈。

**核心洞见**：保持对较细（子）分区的等变性，即可保证对真实分区的等变性。基于这一原理，APEN框架通过组合从细到粗的分区预测层，将等变近似误差的上界表达为两个可量化因素的函数：（i）分区预测的不确定性度量 $\delta(Q)$，以及（ii）抽取非适当子分区的概率 $\lambda(Q)$。通过显式建模并最小化这两个量，网络能够在无需真实分区标注的情况下，学习到可控误差的近似分片E(3)等变表示。

**方法定位**：APEN属于**近似分片等变点网络**。与全局等变方法（如EPN、VN）相比，APEN引入了可学习的逐层分区预测机制，实现了对局部运动对称性的自适应建模；与非等变基线（如PointNet、DGCNN）相比，APEN提供了理论可保证的等变近似误差边界。其核心架构由多层APEN层构成，每层包含三个关键模块：基于硬指派的近似分片等变变换 $\phi_{\text{III}}$、利用PCA帧平均的E(3)等变骨干 $\psi_b$、以及通过高斯混合模型能量最小化与KL散度正则化实现的分区预测模块。

**主要结果**：在人体部位分割任务上，APEN在随机划分、未见随机序列和未见序列三种设定下分别达到94.2%、92.2%和93.5%的mIoU，较全局等变基线EPN提升4.6至14.4个百分点。在DynLab真实室内场景的一次性泛化分割中，APEN仅在单个训练扫描的条件下，在8个测试场景中的7个上超越在大规模合成数据上训练的PointNet、DGCNN和VN基线。在主体分类任务上，APEN以71.4%的准确率大幅领先最佳基线（DGCNN的32.1%），提升超过39个百分点。消融实验验证了通过逐层增大高斯核参数 $\sigma$ 可实现从细到粗的分区学习，以及增加分区数量 $k$ 可有效降低不良分区概率 $\lambda(Q)$，从而控制等变近似误差。

### 点云学习的对称性先验

三维点云数据承载着丰富的几何结构，其中**欧几里得运动群 E(3)**（旋转、平移、反射）是最基本的对称性。将这一对称性编码到神经网络架构中——即构建 E(3) 等变网络——已被证明能显著提升几何深度学习在分割、分类等任务中的样本效率与泛化能力。全局 E(3) 等变网络要求对输入点云施加任意刚体变换后，网络输出以可预测的方式变换：

$$h ( g \cdot X ) = g \cdot h ( X ) \qquad \forall g \in G , X \in U$$

然而，现实场景中的几何对称性往往具有**局部性**：一个动态人体，其四肢相对于躯干各自运动；一间会议室，桌椅可被独立移动。在这些场景下，全局等变假设被打破——不同部件经历不同的欧几里得变换，而网络仍需保持对每个部件运动的等变响应。

### 分片等变性的建模困境

理想情况下，若已知点云的真实刚性部件分区（ground-truth partition），可直接对每个部件独立施加 E(3) 等变处理，再聚合结果，即可得到**分片 E(3) 等变**（piecewise E(3) equivariant）函数。这一构造在数学上是简洁的：令分区矩阵 $Z \in \{0,1\}^{n \times k}$ 将 $n$ 个点分配到 $k$ 个部件，共享等变骨干 $\psi_b$ 对每个部件独立作用：

$$\psi ( X , Z ) = \sum _ { j = 1 } ^ { k } \psi _ { b } ( X \odot Z e _ { j } \mathbf { 1 } _ { d } ^ { T } ) \odot Z e _ { j } \mathbf { 1 } ^ { T }$$

但关键瓶颈在于：**真实分区在推理时是未知的**。现有方法或依赖固定的启发式分区（如空间均匀划分），或使用软分配求期望，这些策略在分区预测不完美时会引入不可控的等变近似误差。这一“先有鸡还是先有蛋”的困境——需要分区来保证等变性，又需要等变特征来预测分区——构成了分片等变点网络设计的核心挑战。

### 核心动机与问题形式化

本文的动机源于一个关键洞察：**保持对较细（子）分区的等变性，可保证对真实分区的等变性**。换言之，若预测的分区是真实分区的一个子分区（即更细粒度的划分），则基于该预测分区的分片等变处理在真实分区下仍严格等变。这一性质将问题转化为：如何学习一个分区预测模型，使得（1）预测的分区以高概率成为真实分区的子分区；（2）分区预测的不确定性可控。

为量化这一目标，作者引入两个核心度量：

- **不良分区概率** $\lambda(Q)$：度量从分区分布 $Q$ 中采样得到的分区不是真实分区子分区的概率；
- **不确定性度量** $\delta(Q)$：量化分区预测的不确定性，仅当 $Q$ 趋向于确定性顶点分区时才趋于 $0$。

本文的核心主张是：**分片 E(3) 等变的近似误差可以被 $\lambda(Q)$ 和 $\delta(Q)$ 联合控制**，从而将架构设计的焦点从“如何完美分区”转向“如何可控地预测分区并绑定误差”。这一视角将分片等变网络从启发式设计提升为具有理论保障的框架性方法。

## 核心方法与创新机理

APEN的核心创新在于将点网络的等变对称性从**全局E(3)**扩展至**近似分片E(3)**，并通过一种可控的误差边界机制来形式化地处理分区预测的不确定性。相较于全局等变网络（如EPN）或非等变基线（PointNet、DGCNN、VN），APEN在以下三个关键维度上实现了突破性改变。

### 1. 等变性类型：从全局到近似分片，带可控误差边界

传统等变点网络要求网络函数 $h$ 满足严格的全局等变条件 $h(g \cdot X) = g \cdot h(X), \forall g \in G$。然而，当场景由多个独立运动的刚体部分组成时，全局等变性反而成为限制——它强制整个点云进行相同的刚体变换，无法刻画局部运动。APEN将等变性类型从**全局E(3)等变**改为**近似分片E(3)等变**，其核心理论贡献在于定义了$(G,Q)$等变函数类（Definition 1），并证明了等变近似误差的上界仅由两个可量化的量控制：

$$\mathbb{E}_{Q_{Z|\mathbf{X}}} \left\| \phi \left( g \cdot \left( X, Z \right) \right) - g \cdot \left( \phi ( X ), Z \right) \right\| \leq \left( \lambda(Q_{simple}) + \delta(Q) \right) M$$

其中：
- **$\lambda(Q)$**：从分区分布 $Q$ 中采样到非适当子分区（即不是真实分区的子分区）的概率（Equation 2）。该概率度量了分区模型的结构性失败风险。
- **$\delta(Q)$**：分区预测的不确定性度量，仅当 $Q$ 趋向于确定性顶点分区时才趋于零（Equation 3）。

这一形式化框架将等变近似误差分解为两个可独立分析和优化的来源，为网络设计提供了理论指导。

### 2. 分区预测：从启发式到可学习的GMM能量最小化

基线方法通常采用固定的启发式分区策略（如 $Q_{simple}$，即随机将点分配到 $k$ 个部分）或直接使用软分配的期望值。APEN将分区预测转变为一个**可学习的、逐层进行的几何聚类过程**，其关键设计包括：

- **能量最小化框架**：每层的分区 $Q_{pred}$ 通过最小化一个包含两项的能量函数来获得（Equation 9）：
  $$(\mu_j^\star, \pi_j^\star) = \underset{\alpha}{\arg\min} -\log P(Y; \alpha) - \tau \sum_{j \neq j'} \pi_j \pi_{j'} \log D_{KL}(\mathcal{N}(\cdot; \mu_j) || \mathcal{N}(\cdot; \mu_{j'}))$$
  第一项为高斯混合模型（GMM）的负对数似然，驱动部分中心 $\mu_j$ 拟合数据分布；第二项为KL散度正则化项，惩罚不同部分中心之间的重叠，鼓励学习到更紧凑、更具判别性的分区。

- **硬指派策略 $\phi_{III}$**：与使用期望软分配的 $\phi_I$ 或期望函数值的 $\phi_{II}$ 不同，APEN采用 $\phi_{III}(X) = \sum_{j=1}^{k} \psi_b(X \odot Z_* e_j \mathbf{1}_d^T) \odot Z_* e_j \mathbf{1}^T$（Equation 8），即基于 $\arg\max$ 的硬指派 $Z_*$。Theorem 1 证明了该形式属于 $(G,Q)$ 等变函数类，其误差被 $(\lambda(Q_{simple}) + \delta(Q))M$ 所限制。

- **可控的误差收敛**：当GMM中的温度参数 $\sigma \to 0$ 时，$\delta(Q_{pred}) \to 0$ 且 $\lambda(Q_{pred}) \leq \lambda(Q_{simple})$（Section 2.3），表明通过调节 $\sigma$ 可以在分区确定性和等变近似误差之间进行权衡。

### 3. 网络组合方式：从单层到自底向上的分层粗化架构

全局等变网络通常采用单次处理的方式，无法捕捉多尺度的局部结构。APEN引入了一种**自底向上的组合架构**：编码器由 $L=4$ 个APEN层堆叠而成，每层不仅输出特征，还预测一个比上一层更粗的分区 $Q_{pred}$，供下一层使用（Figure 2）。这种设计的关键机制包括：

- **逐层粗化的分区序列**：通过设置逐渐增大的 $\sigma$ 序列（$\sigma_{l+1} > \sigma_l$），网络被鼓励从细粒度分区逐步过渡到粗粒度分区（Appendix A.4）。在人体部位分割实验中，编码器各层学到的分区 $Q_{pred}$ 确实呈现出从细到粗的演化趋势（Figure 7）。

- **改进的EM算法实现中心合并**：分区预测模块采用改进的期望最大化（EM）算法，通过隐式微分实现端到端训练，并在EM迭代中引入中心合并机制，使网络能够自适应地减少下一层的部分数量 $k$。

- **共享的帧平均等变骨干**：每层使用基于PCA帧和帧平均（Frame Averaging）的共享等变骨干 $\psi_b$，内部采用稀疏PointNet网络以支持较大的 $k$ 值。这种设计保证了骨干本身对 $E(3)$ 的严格等变性，而分片近似的误差仅来源于分区预测的不完美。

### 创新总结

APEN的三项改变形成了一个完整的逻辑闭环：**可学习的逐层分区预测**提供了自适应发现局部结构的能力；**$(G,Q)$等变函数类与误差边界**为这种近似提供了理论保障；**自底向上的组合架构**则使网络能够从细到粗地逐步抽象场景结构。这一框架使得APEN在仅使用单个训练扫描的一次性泛化场景中，仍能显著优于在大规模合成数据上训练的全局等变网络和非等变基线（Table 2, Figure 3），验证了分片等变表示在数据高效学习中的关键优势。

APEN采用一种自底向上的组合式网络架构，其核心思想是：**保持对较细（子）分区的等变性，即可保证对真实分区的等变性**。整个网络由一系列分片等变层串行堆叠而成，每层不仅输出该层的特征表示，还预测一个更粗化的分区供下一层使用，从而形成从细到粗的分区层次结构。

### 编码器-解码器流水线

网络整体采用编码器-解码器设计（Figure 2）。编码器由 $L=4$ 个APEN层组成，每层接收上一层的点云特征和分区矩阵，输出更新后的特征以及一个更粗化的分区预测 $Q_{\text{pred}}$。解码器则根据具体任务（分割或分类）将编码器的最终特征映射到目标输出。

具体而言，设输入点云为 $\mathbf{X} \in U$，编码器第 $l$ 层的处理流程为：

1. **分片等变特征提取**：基于当前分区 $\mathbf{Z}_*$（初始层使用简单的均匀分区 $Q_{\text{simple}}$），通过共享的等变骨干 $\psi_b$ 对各部分独立处理，再聚合得到该层特征输出 $\phi(\mathbf{X})$（即 $\phi_{\text{III}}$ 层，Equation 8）。
2. **分区预测**：从当前层输出特征中提取逐点表示 $\mathbf{Y}$，通过最小化一个包含GMM负对数似然和KL散度正则化项的能量函数（Equation 9），求解出下一层的部分中心 $\mu_j^*$ 和混合系数 $\pi_j^*$，进而通过高斯密度归一化得到软分配矩阵 $Q_{\text{pred}}$（Equation 10）。该过程采用改进的EM算法实现中心的合并与隐式微分，确保端到端可训练。
3. **分区粗化**：通过设置逐层递增的 $\sigma$ 序列（$\sigma_{l+1} > \sigma_l$），鼓励网络学习从细到粗的分区层次。初始层使用较细的分区（较大的 $k$），后续层逐步合并部分，最终输出粗粒度的全局表示。

### 等变骨干与帧平均

每个APEN层内部的等变骨干 $\psi_b$ 采用**帧平均（Frame Averaging）** 方法实现严格的 $E(3)$ 等变性：首先通过PCA计算局部帧 $F(\mathbf{X})$，然后在该帧下应用共享的稀疏PointNet网络 $\tilde{\psi}$，最后通过帧平均对称化操作获得等变输出。稀疏线性层的使用使得网络能够高效处理较大的分区数 $k$。

### 训练监督

网络训练采用两部分监督信号：一是任务相关的最终损失（如分割的交叉熵损失或分类损失），二是对每层预测的部分中心投票 $\mathbf{Y}_l$ 与真实部分中心 $\mathbf{Y}_{\text{GT}}$ 之间的L1损失（$\text{loss}_A$），以引导分区预测学习有意义的子分区结构。

### 关键设计原则

整个框架的设计围绕两个核心量展开：
- **$\delta(Q)$**：分区预测的不确定性度量，仅当 $Q$ 趋向于确定性顶点分区时才趋于0（Equation 3）。
- **$\lambda(Q)$**：从 $Q$ 中采样得到非适当子分区的概率（Equation 2）。

定理1保证：采用硬指派（$\arg\max$）的 $\phi_{\text{III}}$ 层属于 $(G,Q)$ 等变函数类，其等变近似误差被 $(\lambda(Q_{\text{simple}}) + \delta(Q)) M$ 所限制（Equation 7）。当 $\sigma \to 0$ 时，有 $\delta(Q_{\text{pred}}) \to 0$ 且 $\lambda(Q_{\text{pred}}) \leq \lambda(Q_{\text{simple}})$，从而实现对等变近似误差的可控边界。

APEN框架的核心由三个相互耦合的模块构成：**近似分片E(3)等变层**、**分区预测模型**以及**等变骨干网络**。这三个模块通过自底向上的组合架构串联，每层在输出特征的同时预测一个更粗化的分区，供下一层使用，从而实现对局部欧几里得运动对称性的逐步建模。

### 近似分片等变层（φ_III）

当真实分区未知时，网络需要在不确定分区条件下保持近似的分片等变性。APEN采用硬指派策略，定义层函数 $`\boldsymbol{\phi}: U \to U'`$ 为：

$$`\boldsymbol{\phi}(X) = \sum_{j=1}^{k} \psi_b(X \odot Z_* e_j \mathbf{1}_d^T) \odot Z_* e_j \mathbf{1}^T`$$

其中 $`Z_*`$ 由分区预测模型给出的软分配矩阵 $`Q`$ 经 argmax 得到（即 $`(Z_*)_{i,:} = e_{\arg\max_j Q(Z|X)_{ij}}`$），$`\psi_b`$ 是共享的E(3)等变骨干网络，$`\odot`$ 表示逐元素乘法。该层的核心机制是：将输入点云 $`X`$ 按预测分区 $`Z_*`$ 拆分为 $`k`$ 个部分，每个部分独立通过等变骨干 $`\psi_b`$ 处理，再按原分区聚合输出。

**定理1** 证明了这种形式的 $`\boldsymbol{\phi}`$ 属于 $`(G, Q)`$ 等变函数类，其期望等变近似误差被严格控制：

$$`\mathbb{E}_{Q_{Z|\mathbf{X}}} \left\| \boldsymbol{\phi} \left( \boldsymbol{g} \cdot \left( \boldsymbol{X}, \boldsymbol{Z} \right) \right) - \boldsymbol{g} \cdot \left( \boldsymbol{\phi} ( \boldsymbol{X} ), \boldsymbol{Z} \right) \right\| \leq \left( \lambda(Q_{\text{simple}}) + \delta(Q) \right) M`$$

这里 $`\lambda(Q)`$ 是从分区分布 $`Q`$ 中采样得到“非真实分区子分区”（即不良分区）的概率，$`\delta(Q)`$ 是分区预测的不确定性度量（仅当 $`Q`$ 趋向于确定性顶点分区时才趋于0），$`M`$ 为常数。这一边界揭示了**误差来源的双重结构**：$`\lambda`$ 衡量分区结构本身的错误风险，$`\delta`$ 衡量预测的模糊程度。两者共同构成了等变近似误差的可控上界。

### 分区预测模型：GMM能量最小化与KL正则化

分区预测是APEN区别于固定分区或启发式方法的**核心创新**。给定当前层输出特征 $`Y`$，下一层的分区 $`Q^{\text{pred}}`$ 通过几何聚类的方式学习。具体而言，部分中心 $`\mu_j^*`$ 和混合系数 $`\pi_j^*`$ 通过最小化以下能量函数得到：

$$`(\mu_j^\star, \pi_j^\star) = \underset{\alpha}{\arg\min} -\log P(Y; \alpha) - \tau \sum_{j \neq j'} \pi_j \pi_{j'} \log D_{\mathrm{KL}} (\mathcal{N}(\cdot; \mu_j) \| \mathcal{N}(\cdot; \mu_{j'}))`$$

第一项是高斯混合模型（GMM）的负对数似然，驱动中心向数据点靠拢；第二项是KL散度正则化项，惩罚不同部分中心所对应的高斯分布之间的相似性，**促使不同部分的中心相互远离**，从而避免分区退化。$`\tau`$ 控制正则化强度。

基于优化得到的中心和混合系数，软分配矩阵由归一化的高斯密度给出：

$$`Q_{ij}^{\mathrm{pred}} = \frac{\mathcal{N}(y_i; \boldsymbol{\mu}_j^*, \sigma) \pi_j^*}{\sum_{j=1}^{k} \mathcal{N}(\boldsymbol{y}_i; \boldsymbol{\mu}_j^*, \sigma) \pi_j^*}`$$

其中 $`\sigma`$ 是控制分配锐度的温度参数。理论分析表明，当 $`\sigma \to 0`$ 时，$`\delta(Q) \to 0`$ 且 $`\lambda(Q) \leq \lambda(Q_{\text{simple}})`$，即分区预测趋于确定且不良分区概率不高于简单模型。在实践中，APEN通过设置逐层递增的 $`\sigma`$ 序列（$`\sigma_{l+1} > \sigma_l`$），使网络从细粒度分区逐步粗化，这一行为在人体部位分割实验中得到了可视化验证（Figure 7）：早期层捕获手指等细粒度结构，深层则合并为手掌、手臂等粗粒度部分。

为实现端到端训练，分区预测中的优化问题通过改进的EM算法求解，并采用隐式微分（implicit differentiation）计算梯度，更新规则为 $`\boldsymbol{\alpha} = \tilde{\boldsymbol{\alpha}} + I^{-1}(\tilde{\boldsymbol{\alpha}}) s(\boldsymbol{Y}; \tilde{\boldsymbol{\alpha}})`$，其中 $`s`$ 为得分函数，$`I`$ 为Fisher信息矩阵。

### 等变骨干：帧平均与稀疏PointNet

APEN层中的共享骨干 $`\psi_b`$ 需要严格满足E(3)等变性。论文采用**帧平均**（Frame Averaging）方法：对每个部分的点云 $`X \odot Z_* e_j \mathbf{1}_d^T`$，先通过PCA计算局部帧 $`F(\cdot)`$，再在该帧下应用非等变网络 $`\tilde{\psi}`$（稀疏PointNet），最后在所有帧上平均以保证等变性：

$$`\psi_b(X \odot Z e_j \mathbf{1}_d^T) = \tilde{\psi}(X \odot Z e_j \mathbf{1}_d^T) \big|_{F(X \odot Z e_j \mathbf{1}_d^T)}`$$

为支持较大的分区数 $`k`$，骨干内部使用稀疏线性层实现，避免计算量随 $`k`$ 线性增长带来的开销。

### 训练监督与组合架构

整个编码器由 $`L=4`$ 个APEN层串联组成（Figure 2）。除任务特定的分割/分类损失外，每层的分区预测通过**部分中心投票损失**进行监督：

$$`\mathrm{loss}_A = \sum_{l=1}^{L} |\mathbf{Y}_l - \mathbf{Y}_{\mathrm{GT}}|`$$

即要求每层预测的部分中心投票 $`\mathbf{Y}_l`$ 与真实部分中心 $`\mathbf{Y}_{\mathrm{GT}}`$ 的L1距离最小化。这种逐层监督确保了从细到粗的分区序列与真实几何结构保持一致，是APEN能够在仅使用单个训练扫描的一次性泛化任务中超越在大规模合成数据上训练的基线方法的关键机制。

## 实验与关键发现

### 主实验结果

APEN 在多个任务上均表现出对全局等变网络及非等变基线的显著优势，验证了近似分片 E(3) 等变框架的有效性。

**人体部位分割（Table 1）**。在 SMPL/DFAUST 数据集上，APEN 在随机划分测试集上达到 **94.2% mIoU**，较全局等变基线 EPN（89.6%）提升 4.6 个百分点，较 PointNet（84.4%）提升近 10 个百分点。在更具挑战性的 unseen 序列泛化设定下，APEN 的优势更为突出：在 DFAUST 的两个 unseen 序列上分别达到 92.2% 和 93.5% mIoU，分别超出 EPN 14.4 和 9.4 个百分点。这表明分片等变建模能够有效捕获人体各部位独立的刚体运动模式，而全局等变网络则无法适应这种局部运动差异。

**一次性泛化至真实室内扫描（Table 2, Figure 3）**。在 DynLab 数据集的 8 个真实房间扫描上，APEN 仅使用单个训练扫描即实现了 88.0%–98.2% 的 mIoU，在 7/8 个场景中超越了在大规模合成数据上训练的 PointNet、DGCNN 和 VN 等基线。值得注意的是，基线方法还需借助 RANSAC 地面平面去除等预处理步骤，而 APEN 无需任何预处理。这一结果直接证明了分片等变归纳偏置在跨域泛化中的关键作用：网络学到的局部欧几里得运动等变性自然地适应了不同房间的几何结构。

**主体分类（Table 3）**。在 DFAUST 数据集上，训练集与测试集包含完全不同的姿态，APEN 达到 **71.4%** 的分类准确率，远超 PointNet（18.5%）、DGCNN（32.1%）和 VN（28.2%）。这一近 40 个百分点的提升说明，分片等变表示能够将人体结构信息与姿态变化解耦，从而在未见姿态下仍能可靠地识别主体身份。

### 分区学习与组合架构的消融分析

**从细到粗的分区学习（Figure 7, Figure 8）**。APEN 编码器的多层结构通过逐渐增大的高斯核宽度 $\sigma_{l+1} > \sigma_l$，引导网络学习从细粒度到粗粒度的分区层次。Figure 7 展示了人体部位分割任务中，编码器各层预测的分区 $Q^{\mathrm{pred}}$ 逐步粗化的过程：早期层捕获局部细节，后续层合并语义相关区域。Figure 8 在一次性分割实验中进一步验证了这一行为——即使在仅有一个训练样本的条件下，学习到的分区层次结构仍能有效泛化至未见测试样本。

**不良分区概率的渐近行为（Figure 6）**。附录中的 2D 玩具实验验证了简单分区模型 $Q_{\mathrm{simple}}$ 的不良分区概率 $\lambda(Q_{\mathrm{simple}})$ 随部分数 $k \to n$ 而趋于 0。这一渐近性质为定理 1 中的误差界提供了经验支撑：通过增加分区数量，可以降低抽取非适当子分区的概率，从而收紧等变近似误差的上界 $(\lambda(Q_{\mathrm{simple}}) + \delta(Q))M$。

### 失败模式与局限性

尽管 APEN 在实验中表现出色，仍存在以下值得关注的局限：

1. **误差界的紧致性不足**。文中提供的等变近似误差界 $(\lambda(Q_{\mathrm{simple}}) + \delta(Q))M$ 仅作为初步理论洞察，其在实际网络训练中的紧致性和指导意义尚未得到充分验证。对于 $\lambda(Q_{\mathrm{simple}})$ 的精确分析被留作未来工作。

2. **任务覆盖范围有限**。当前实验仅覆盖分类和部分分割任务，尚未验证该框架在生成式建模、点云重建等更广泛 3D 任务中的有效性。

3. **数据规模与多样性**。主体分类和人体分割实验主要在 SMPL/DFAUST（10 个主体）上进行，一次性泛化实验也仅涉及 8 个室内场景。框架在大规模、高多样性数据集上的鲁棒性仍需进一步检验。

4. **超参数敏感性**。分区预测中的关键超参数（如 $\sigma$ 序列、合并阈值 $\tau$）目前需手动设定，其对不同任务和数据的自适应调整能力尚不明确。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2402_08529/figures/014_Figure_9.jpg]]
*Figure 9: Training and test set visualization for the subject classification task*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2402_08529/figures/007_Table_1.jpg]]
*Table 1: Mean IoU(%) test set score for human body parts segmentation*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2402_08529/figures/008_Figure_3.jpg]]
*Figure 3: In Tab. 2 we report the mean IoU(%) test score for each of the scenes. Fig. 3 shows qualitative results for 2 rooms. Despite only training on a single scan, our model outperforms baselines trained on a large synthetic dataset in 7 out of the 8 test scenes. These results suggest potential advantages of using piecewise E ( 3 ) equivariant architectures in a single shot setting over the use of large-scale synthetic data. Furthermore, to make baseline approaches work, we employed a RANSAC algorithm to identify the ground plane, with an inlier distance threshold of 0.02 and 1000 RANSAC iterations. In contrast, our method requires no preprocessing since the network can treat the floor as it would...*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2402_08529/figures/013_Table_3.jpg]]
*Table 3: Subject classification accuracy comparison*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2402_08529/figures/011_Figure_7.jpg]]
*Figure 7: APEN encoder’s learned partitions, $Q ^ { \mathrm { p r e d } }$ , extracted from two test-set examples in the human body segmentation experiment. In each group of 4 elements, the leftmost column shows $Q ^ { \mathrm { p r e d } }$ partitions, with subsequent layers’ partitions ordered left-to-right, culminating in the rightmost column that shows the encoder’s last layer partition

## 定位与知识库关联

### 1. APEN 与现有方法的谱系关系

APEN 框架处于**全局等变网络**与**无等变先验的点网络**之间的方法论交叉地带，其核心贡献在于引入**可控的分片等变近似**，弥补了全局对称性假设与真实场景中局部运动独立性之间的矛盾。

#### 1.1 相对于全局等变网络的推进

全局 E(3) 等变网络（如 **EPN**、**VN** (Deng et al., CVPR 2021)）要求整个点云服从单一的刚体运动变换。这一假设在人体姿态变化或动态场景中必然失效——当手臂相对于躯干独立运动时，全局等变网络无法为各部位提供正确的等变表征。APEN 通过**分片 E(3) 等变**直接回应了这一瓶颈：它允许点云的不同部分独立地进行欧几里得变换，同时保持对每部分的严格等变性。

关键的方法论跃迁在于：APEN 不假设真实分区已知，而是将分区本身建模为**可学习的隐变量**，并通过理论保证（Theorem 1）将等变近似误差绑定在分区预测的质量上。这使得 APEN 在人体部位分割任务上相对于 **EPN** 实现了 **+4.6 到 +14.4 mIoU** 的提升（Table 1），充分验证了分片等变假设的优越性。

#### 1.2 相对于非等变基线的优势

与 **PointNet** (Qi et al., CVPR 2017)、**DGCNN** (Wang et al., ACM TOG 2019) 等无等变先验的方法相比，APEN 的等变归纳偏置带来了显著的样本效率和泛化能力。在一次性泛化实验中，APEN 仅使用**单个训练扫描**即超越了在**大规模合成数据集**上训练的 PointNet、DGCNN 和 VN 基线（Table 2），在 8 个测试场景中的 7 个上取得更优 mIoU。在主体分类任务中，APEN 以 **71.4%** 的准确率远超最佳基线 VN 的 28.2%（Table 3），展示了分片等变结构在捕捉局部运动模式上的根本性优势。

#### 1.3 与帧平均方法的结合

APEN 的等变骨干采用了 **Frame Averaging (FA)** 技术（Puny et al., 2022），通过 PCA 帧和群平均实现严格的 E(3) 等变性。这一选择使 APEN 继承了一个经过验证的等变构建范式，同时将其从全局作用域扩展到分片作用域。这种“组合式继承”的策略——在已有等变骨干上叠加可学习的分区机制——为后续工作提供了清晰的扩展路径：任何更强大的等变骨干（如球面卷积、张量场网络）理论上都可以嵌入 APEN 框架。

### 2. 适用边界与前提条件

APEN 的有效性依赖于以下前提：

- **分区结构的存在性**：场景必须天然具有可分解为独立刚体运动的部分结构（如人体关节、室内家具）。对于缺乏明确部分边界的连续变形场景，分片等变假设的适用性需要重新审视。
- **分区数量的预设**：每层的部分数量 $k$ 需要作为超参数指定。虽然网络通过 $\sigma$ 序列和合并机制可以自适应地粗化分区，但初始 $k$ 的选择仍影响模型容量和计算开销。
- **训练监督的形式**：当前框架依赖对部分中心投票的 L1 监督（$\mathrm{loss}_A$），这要求训练数据具有部件级别的标注。在缺乏此类标注的场景中，如何无监督地学习分层分区仍是一个开放问题。

### 3. 已识别的局限

APEN 论文明确指出了以下局限，这些应被视为该方向当前的知识边界：

1. **理论界限的初步性**：等变近似误差的界限分析（Equation 7）提供了有价值的洞察，但作者承认该界限“仅作为初步洞察”，尚未进行更深入的理论收紧。这意味着在实际部署中，$\lambda(Q_{\text{simple}}) + \delta(Q)$ 的上界可能过于宽松，无法直接用于严格的性能保证。

2. **任务范围的有限验证**：当前实例化仅覆盖了分类和部分分割任务。框架在生成式建模、点云重建、场景补全等其他 3D 任务中的有效性尚未得到验证。分片等变表征是否能为这些任务带来类似的增益，需要进一步实验。

3. **临界参数的未分析**：简单分区模型 $Q_{\text{simple}}$ 的精确 $\lambda(Q)$ 分析被留作未来工作。目前仅依赖其渐近行为（$\lambda \to 0$ 当 $k \to n$，Figure 6），缺乏对有限样本下行为的定量刻画。

4. **数据规模的局限性**：实验主要在较小规模的主体数据集（SMPL/DFAUST，10 个人体）和有限的室内场景（DynLab 的 8 个房间）上进行。泛化到更大规模或更复杂动态场景的能力需要进一步验证。

### 4. 开放问题与未来方向

基于 APEN 框架的现有贡献和局限，以下开放问题构成了该研究方向的自然延伸：

- **界限的精细化**：能否通过更精细的概率分析或信息论工具，收紧等变近似误差的界限，使其成为网络设计和超参数选择的实用指导工具？
- **对称性类型的扩展**：APEN 当前处理的是 E(3) 的分片等变。能否将框架扩展到非刚性运动（如参数化变形场）或更一般的对称群（如动力系统的李群作用）？
- **超参数的自适应学习**：分区预测中的关键超参数（$\sigma$ 序列、$\tau$ 合并阈值）目前需要手动设置。能否设计端到端的学习机制，使这些参数根据数据特性自适应调整？
- **等变骨干的升级**：APEN 使用 FA + PointNet 作为骨干。若替换为表达能力更强的等变架构（如 SE(3)-Transformers、Tensor Field Networks），能否在保持理论保证的同时进一步提升性能？
- **无监督分区学习**：在缺乏部件标注的情况下，能否通过自监督或对比学习目标，使网络自主发现合理的分层分区结构？这将显著扩展 APEN 的适用范围。

## 原文 PDF

![[paperPDFs/ICLR_2024/Approximately_Piecewise_E_3_Equivariant_Point_Networks.pdf]]
