---
title: "A-ViT: Adaptive Tokens for Efficient Vision Transformer"
type: paper
paper_level: A
venue: CVPR
year: 2022
pdf_ref: paperPDFs/CVPR_2022/A_ViT_Adaptive_Tokens_for_Efficient_Vision_Transformer.pdf
project_link: https://a-vit.github.io/
code_link: null
aliases:
- A-ViT
tags:
- CVPR_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过每个token自适应地累积停止概率，在不同深度提前中止对非信息性token的处理，实现细粒度空间自适应推理。"
primary_logic: "复用原始Transformer模块中嵌入向量的单一维度计算token停止概率，无需引入额外参数或子网络；引入分布先验正则化引导停止分布朝向目标深度，稳定训练并提升精度。"
claims:
- "通过复用现有参数中的单一神经元计算halting概率，不增加额外参数或计算量。"
- "在几乎不损失准确率的前提下显著提升吞吐量：DeiT-Tiny提升62%，DeiT-Small提升38%，准确率仅下降0.3%。"
- "Token级别的细粒度ponder损失相比传统ACT减少约3层平均深度，额外降低25% FLOPs。"
- "分布先验正则化使训练快速收敛到目标深度，并带来6.4%的精度增益。"
---

# A-ViT: Adaptive Tokens for Efficient Vision Transformer

> [!tip] 核心洞察
> 复用原始Transformer模块中嵌入向量的单一维度计算token停止概率，无需引入额外参数或子网络；引入分布先验正则化引导停止分布朝向目标深度，稳定训练并提升精度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | A-ViT：面向高效视觉Transformer的自适应令牌 |
| 英文题名 | A-ViT: Adaptive Tokens for Efficient Vision Transformer |
| 会议/期刊 | CVPR 2022 |
| Links | [paper](https://arxiv.org/abs/2112.07658) · [Project](https://a-vit.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | A-ViT |
| Dataset | ImageNet-1K |

> [!tip] 效果简介
> - ImageNet-1K 上，Throughput提升 (相比DeiT) 为 +62% (DeiT-Tiny) / +38% (DeiT-Small)，对比 1× (DeiT-Tiny / DeiT-Small)，变化 +62% / +38%。
> - ImageNet-1K 上，Top-1准确率 (相比DeiT) 为 仅下降0.3% (DeiT-Tiny & DeiT-Small) 或 71.3% / 78.9% (A-ViT-T/S finetuned)，对比 72.2% (DeiT-Tiny) / 79.8% (DeiT-Small) 估计，变化 -0.3% (最大)。
> - ImageNet-1K 上，平均Token深度 / FLOPs / Top-1 Acc. (对比其他动态方法) 为 A-ViT-T: Avg. depth 7.23, FLOPs 0.8G, Top-1 71.0，对比 DynamicViT等: 更浅或更深但精度更低/更高FLOPs，变化 更好的精度-效率权衡。

## 概要

标准Vision Transformer（ViT）对所有图像块（token）均等对待，在每一层对所有token执行密集的自注意力和前馈计算。这一固定计算范式忽略了图像内容在空间上的信息差异性——背景、纹理均匀区域等大量token对最终分类贡献甚微，却消耗了与语义关键区域相同的计算资源。A-ViT针对这一瓶颈，提出了一种**无需额外参数的自适应token计算机制**：在每个Transformer块内部，复用现有MLP层中嵌入向量的单一维度，通过sigmoid函数为每个token生成一个停止概率；当某token的累积停止分数达到阈值时，该token在后续层中被提前移除并屏蔽注意力，从而实现**细粒度的空间自适应推理**。

核心洞察有二。其一，**停止决策可完全由原始网络参数承载**——仅占用嵌入向量的第一维度并引入两个标量参数（γ, β），无需额外的子网络或计算开销。实验表明，这一设计对原始模型精度几乎无影响（DeiT-Tiny下降仅0.08%±0.04%），而额外引入停止子网络仅带来约0.06%的精度收益，却造成12.6%的推理吞吐开销。其二，**分布先验正则化**通过KL散度约束各层平均停止分数的分布趋近于目标高斯分布，有效解决了传统ACT训练不稳定、收敛缓慢的问题，带来6.4%的精度增益，并实现了对平均token深度的精细控制。

在方法定位上，A-ViT属于**动态推理**与**自适应计算时间（ACT）** 的交叉。不同于**DynamicViT**（Rao et al., NeurIPS 2021）基于Gumbel-softmax的token稀疏化——后者在固定层数后一次性丢弃token——A-ViT允许不同token在不同深度独立停止，更灵活地匹配图像局部复杂度。相较于传统**ACT**（Graves, arXiv 2016）在层级对所有token同时停止，A-ViT的token级细粒度停止使平均深度减少约3层，额外降低25%的FLOPs。与**PonderNet**（Banino et al., ICML Workshop 2021）的几何分布采样停止相比，A-ViT的确定性累积停止机制在训练稳定性上更具优势。

主要结果：在ImageNet-1K上，A-ViT使DeiT-Tiny的吞吐量提升62%，DeiT-Small提升38%，而Top-1准确率仅下降0.3%。可视化分析表明，学习到的停止深度与图像语义高度对齐——信息丰富的目标区域被处理得更深，背景区域则被提前终止，验证了自适应计算的有效性和可解释性。

### 视觉Transformer的计算冗余困境

视觉Transformer（ViT）将图像建模为等长的token序列，并通过堆叠的自注意力层进行全局信息交互，在图像分类、目标检测等任务上取得了卓越性能。然而，标准ViT架构存在一个根本性的计算瓶颈：**无论输入图像的复杂度如何，所有token均需经过全部层的密集计算**。这种“一刀切”的处理方式导致了显著的计算冗余——对于背景区域、简单纹理等非信息性token，深层的特征精炼往往是不必要的。

这一瓶颈的实质在于：ViT缺乏对**空间维度计算资源自适应分配**的能力。与人类视觉系统选择性关注显著区域的机制不同，标准ViT对图像中每个patch赋予完全相同的计算预算，从而在简单样本或非判别性区域上浪费了大量计算。

### 现有动态推理方法的局限

为缓解上述冗余，研究者提出了多种动态推理策略，主要可分为两类：

**（1）层级别的自适应计算时间（ACT）**。**ACT**（Graves, arXiv 2016）通过累积停止概率在层维度上提前终止整个token序列的处理。然而，该方法对所有token同时停止，无法区分不同token的信息量差异。在视觉场景中，前景对象token通常需要比背景token更深的处理，层级别的统一停止无法捕捉这种细粒度的空间异质性。

**（2）Token稀疏化/剪枝方法**。以**DynamicViT**（Rao et al., NeurIPS 2021）为代表的方案通过Gumbel-softmax采样在特定层一次性丢弃部分token。这类方法虽然实现了空间稀疏化，但存在两个关键缺陷：一是丢弃决策仅在少数层发生，缺乏逐层的动态调整能力；二是通常需要引入额外的预测子网络来计算token保留分数，增加了参数量和计算开销。

**（3）随机停止方法**。**PonderNet**（Banino et al., ICML Workshop 2021）采用几何分布采样实现随机停止，但训练稳定性较差，且难以精确控制平均计算预算。

综上，现有方法的核心缺口在于：**缺乏一种既不引入额外参数、又能实现逐token逐层自适应停止的细粒度动态推理机制**。

### 本文动机

基于以上分析，本文提出A-ViT（Adaptive Tokens for Efficient Vision Transformer），旨在实现以下目标：

1. **细粒度空间自适应**：允许不同token在不同深度独立停止，使计算资源精准聚焦于信息性区域。
2. **零参数开销**：复用现有Transformer模块中已有的嵌入维度来计算停止概率，避免引入额外子网络或可学习参数。
3. **稳定可控的训练**：通过分布先验正则化引导停止行为收敛到目标深度分布，解决ACT类方法训练敏感的问题。

核心假设是：**通过在每个Transformer块中借用单一嵌入维度计算token级停止概率，可以在不牺牲模型容量的前提下实现高效的自适应推理**。这一设计使得A-ViT能够直接部署于现成硬件平台，无需定制稀疏计算支持即可获得显著的吞吐量提升。

## 核心方法与创新机理

A-ViT 的核心创新在于为视觉Transformer引入**空间自适应的token级动态计算机制**，使不同图像区域能够根据其信息量在不同深度提前停止处理。这一设计直击标准ViT对所有token进行同等深度密集计算的根本瓶颈，实现了细粒度的计算资源分配。

### 关键创新点一：无额外参数的自适应停止机制

A-ViT 最精巧的设计在于**完全复用现有Transformer模块中的参数来计算token停止概率**，无需引入任何额外的可学习参数或子网络。具体而言，该方法将停止函数 $H(\cdot)$ 嵌入到每个Transformer块的MLP层中，仅分配嵌入向量的单个维度（默认 $e=0$）通过sigmoid函数计算停止概率：

$$h_k^l = H(t_k^l) = \sigma(\gamma \cdot t_{k,e}^l + \beta)$$

这一设计仅引入两个标量参数（$\gamma, \beta$），且在所有层间共享。消融实验验证了这一选择的合理性：额外引入停止子网络仅带来约0.06%的精度增益，却引入了12.6%的推理吞吐开销。同时，占用单个嵌入维度对原始模型精度几乎无影响——DeiT-Tiny和DeiT-Small的Top-1准确率仅分别下降0.08%±0.04%和0.04%±0.03%。

### 关键创新点二：Token级细粒度停止策略

区别于传统ACT在层级别对所有token同时停止的粗粒度方式，A-ViT实现了**每个token独立的累积停止判断**。当token $k$ 的累积停止分数达到阈值 $1 - \epsilon$ 时，该token被立即置零并在注意力计算中被屏蔽：

$$N_k = \underset{n \leqslant L}{\mathrm{argmin}} \sum_{l=1}^n h_k^l \geqslant 1 - \epsilon$$

这种token级别的细粒度pondering相比层级别ACT减少了约3层平均深度，并额外降低了25%的FLOPs。停止后的token在后续所有层中被完全移除，使得深层Transformer块仅需处理剩余的信息性token，从而实现显著的推理加速。

### 关键创新点三：分布先验正则化稳定训练

针对ACT类方法训练敏感的问题，A-ViT引入了**分布先验正则化项**，通过KL散度约束各层平均停止分数的分布趋近于目标高斯分布：

$$\mathcal{L}_{\mathrm{distr.}} = \mathrm{KL}(\mathcal{H} || \mathcal{H}^{\mathrm{target}})$$

该正则化项引导训练快速收敛到目标平均深度，并带来了6.4%的精度增益。与单纯增大ponder损失系数 $\alpha_p$ 导致过度惩罚网络不同，分布先验提供了更精细的精度-效率控制手段。

### 与Baseline的Changed Slots总结

| 设计维度 | Baseline（DeiT） | A-ViT |
|---------|-----------------|-------|
| Token计算策略 | 所有token固定深度处理（12层） | 每个token根据累积停止概率在不同深度自适应停止，停止后被移除并屏蔽注意力 |
| 停止机制参数 | 无此机制 | 复用现有MLP层中单个嵌入维度（$e=0$），通过sigmoid计算停止概率，仅引入两个标量参数 |
| 训练稳定机制 | 仅使用任务损失 | 增加分布先验正则化项（KL散度）引导停止分布朝向目标深度，稳定训练并提供精度增益 |

这些创新共同实现了在几乎不损失准确率的前提下显著提升推理效率：DeiT-Tiny吞吐量提升62%，DeiT-Small提升38%，准确率仅下降0.3%。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2112_07658/figures/001_Figure_1.jpg]]
*Figure 1: We introduce A-ViT, a method to enable adaptive token computation for vision transformers. We augment the vision transformer block with adaptive halting module that computes a halting probability per token. The module reuses the parameters of existing blocks and it borrows a single neuron from the last dense layer in each block to compute the halting probability, imposing no extra parameters or computations. A token is discarded once reaching the halting condition. Via adaptively halting tokens, we perform dense compute only on the active tokens deemed informative for the task. As a result, successive blocks in vision transformers gradually receive less tokens, leading to faster inference....*

A-ViT 的整体推理管线在标准视觉 Transformer 的基础上引入了一个自适应令牌停止机制，使模型能够根据输入图像的信息分布，在不同深度对不同令牌提前终止计算。其核心流程如下：

**1. 图像分块与嵌入（Patch Embedding E）**
输入图像 $x$ 首先被切分为 $K$ 个 patch，经编码网络 $E(\cdot)$ 映射为带位置编码的令牌序列 $t \in \mathbb{R}^{K \times E}$。该步骤与标准 ViT 完全一致，未引入任何额外开销。

**2. 逐层 Transformer 处理（Transformer Blocks $F^l$）**
令牌序列依次通过 $L$ 层 Transformer 块，每层执行自注意力和 MLP 变换：
$$t_{1:K}^l = F^l(t_{1:K}^{l-1})$$
与标准 ViT 的关键区别在于，随着层数加深，部分令牌会被提前停止并移除，后续层仅处理仍处于活跃状态的令牌子集。

**3. 自适应停止模块（Halting Module $H(\cdot)$）**
每个 Transformer 块的 MLP 层内复用嵌入向量的第一维度（$e=0$），通过 sigmoid 门控计算每个令牌的停止概率：
$$h_k^l = H(t_k^l) = \sigma(\gamma \cdot t_{k,0}^l + \beta)$$
其中 $\gamma$ 和 $\beta$ 是仅有的两个标量参数，跨所有层共享。该设计完全复用现有 MLP 的神经元，不引入额外子网络或可学习参数。

**4. 令牌停止与掩码（Token Halting & Masking）**
每个令牌 $k$ 维护一个累积停止分数 $\sum_{l=1}^n h_k^l$。当该累积值达到阈值 $1-\epsilon$ 时，令牌在层 $N_k$ 被判定停止：
$$N_k = \underset{n \leqslant L}{\mathrm{argmin}} \sum_{l=1}^n h_k^l \geqslant 1 - \epsilon$$
停止后的令牌通过两种方式被移除：(i) 令牌值置零；(ii) 在注意力计算中被屏蔽。此后所有更深层不再对该令牌进行任何计算。

**5. 分类输出（Classifier $C$）**
类令牌（class token）采用均值场加权方式聚合各层状态，以停止概率作为权重：
$$t_o = \sum_{l=1}^{L} p_c^l t_c^l$$
最终分类损失基于该加权输出计算：$\mathcal{L}_{\text{task}} = C(t_o)$。

**6. 训练目标**
整体损失函数由三部分组成：
$$\mathcal{L}_{\text{overall}} = \mathcal{L}_{\text{task}} + \alpha_p \mathcal{L}_{\text{ponder}} + \alpha_d \mathcal{L}_{\text{distr.}}$$
其中 $\mathcal{L}_{\text{ponder}} = \frac{1}{K} \sum_{k=1}^{K} (N_k + r_k)$ 鼓励令牌尽早停止，$\mathcal{L}_{\text{distr.}} = \text{KL}(\mathcal{H} \| \mathcal{H}^{\text{target}})$ 通过 KL 散度将各层停止分数的分布约束到目标高斯分布，引导平均停止深度收敛至预设值。

**模块间数据流关系**：图像 → Patch Embedding → 活跃令牌序列 → [Transformer Block + Halting Module] × L 层（逐层递减令牌数）→ 类令牌均值场聚合 → 分类器输出。随着推理深度增加，被判定为信息量低的令牌逐步退出计算，形成“漏斗式”的令牌流，后续层仅对保留的语义关键区域进行密集计算。

### 整体推理流程

A-ViT 将标准 ViT 的固定深度推理改造为输入自适应的动态计算图。给定图像 $x$，首先通过 Patch Embedding 模块 $E(\cdot)$ 将其映射为 $K$ 个 token：

$$t_{1:K}^0 = E(x)$$

随后，token 序列逐层通过 $L$ 个 Transformer Block $F^l$。与传统 ViT 不同的是，每个 token $k$ 在每层 $l$ 都会计算一个**停止概率** $h_k^l$。一旦某个 token 的累积停止概率达到阈值，该 token 即被“停止”——在后续所有层中被置零并屏蔽注意力，不再参与计算。最终，分类器 $C$ 对类 token 的均值场加权输出进行预测：

$$y = C(t_o)$$

### 核心模块：自适应停止模块 $H(\cdot)$

停止模块是 A-ViT 的核心创新，其关键设计在于**零额外参数**。作者将停止概率的计算直接嵌入到现有 Transformer Block 的 MLP 层中，复用嵌入向量的单一维度。

具体而言，对于第 $l$ 层的 token $t_k^l \in \mathbb{R}^E$，停止概率由下式给出：

$$h_k^l = H(t_k^l) = \sigma(\gamma \cdot t_{k,e}^l + \beta)$$

其中：
- $\sigma(\cdot)$ 为 sigmoid 函数，将输出压缩到 $(0,1)$ 区间
- $t_{k,e}^l$ 是 token 嵌入向量的第 $e$ 个维度，**默认取 $e=0$（第一维）**
- $\gamma$ 和 $\beta$ 是唯一的可学习标量参数（所有层共享），分别控制 sigmoid 的陡峭程度和偏置

这一设计意味着 $H(\cdot)$ 不引入任何额外的子网络或参数矩阵——仅从现有 MLP 的最后一层“借用”一个神经元的输出，通过 sigmoid 门控转化为停止概率。

### Token 停止条件与累积机制

每个 token $k$ 维护一个累积停止分数。当该分数达到 $1 - \epsilon$ 时，token 被停止：

$$N_k = \underset{n \leqslant L}{\mathrm{argmin}} \sum_{l=1}^n h_k^l \geqslant 1 - \epsilon$$

其中 $N_k$ 为 token $k$ 的停止层索引，$\epsilon$ 是一个小常数（如 $0.01$），用于允许一定的概率余量。一旦 token 被停止，在后续所有层 $l > N_k$ 中：
1. token 值被置零
2. 该 token 的注意力被屏蔽

这使得后续层只需处理逐渐减少的活跃 token，从而实现推理加速。

### 类 Token 的均值场输出

类 token（class token）需要特殊处理，因为它最终用于分类。A-ViT 采用均值场加权方式，将类 token 在各层的状态按其停止概率加权平均，作为最终的分类输入：

$$t_o = \sum_{l=1}^{L} p_c^l t_c^l$$

其中 $p_c^l$ 是类 token 在层 $l$ 的停止概率权重（由各层停止分数归一化得到）。任务损失在此基础上计算：

$$\mathcal{L}_{\mathrm{task}} = \mathcal{C}(t_o)$$

值得注意的是，与标准 ACT 需要聚合所有 token 不同，A-ViT 的均值场公式**仅应用于类 token**——其他 patch token 通过注意力机制间接贡献于类 token，无需显式聚合。

### 训练目标：Ponder 损失与分布先验正则化

为鼓励 token 尽早停止，引入 Ponder 损失，对所有 token 的平均计算深度施加惩罚：

$$\mathcal{L}_{\mathrm{ponder}} = \frac{1}{K} \sum_{k=1}^{K} (N_k + r_k)$$

其中 $r_k$ 是 token $k$ 在停止时未用完的剩余概率（即 $1 - \sum_{l=1}^{N_k} h_k^l$），用于保证损失对停止概率的梯度可微。

仅使用 Ponder 损失训练可能不稳定，因此 A-ViT 引入**分布先验正则化**，通过 KL 散度约束各层平均停止分数的分布 $\mathcal{H}$ 趋近于目标高斯分布 $\mathcal{H}^{\mathrm{target}}$：

$$\mathcal{L}_{\mathrm{distr.}} = \mathrm{KL}(\mathcal{H} || \mathcal{H}^{\mathrm{target}})$$

目标分布的中心对应期望的平均 token 深度 $N^{\mathrm{target}}$。这一正则项引导训练快速收敛到目标深度，消融实验表明其带来 **6.4% 的精度增益**（Figure 7）。

最终的整体训练损失为：

$$\mathcal{L}_{\mathrm{overall}} = \mathcal{L}_{\mathrm{task}} + \alpha_p \mathcal{L}_{\mathrm{ponder}} + \alpha_d \mathcal{L}_{\mathrm{distr.}}$$

其中 $\alpha_p$ 和 $\alpha_d$ 分别是 Ponder 损失和分布正则项的权重超参数。

## 实验与关键发现

### 主要结果

A-ViT 在 ImageNet-1K 上以几乎可忽略的精度代价换取了显著的吞吐量提升。在标准 DeiT 架构上，A-ViT 使 DeiT-Tiny 的吞吐量提升 **62%**，DeiT-Small 提升 **38%**，而 Top-1 准确率仅下降 **0.3%**（Table 3）。经过完整微调后，A-ViT-T 和 A-ViT-S 分别达到 71.3% 和 78.9% 的 Top-1 准确率；引入蒸馏 token 后，A-ViT-S + distil. 进一步达到 80.7% 的 Top-1 准确率，同时保持 3.6G FLOPs 和 1.1K imgs/s 的吞吐量。

在与其他动态推理机制的对比中（Table 2），A-ViT-T 以平均 token 深度 7.23 层、FLOPs 0.8G 和 Top-1 准确率 71.0% 取得了更优的精度-效率权衡。相比 **DynamicViT**（Rao et al., NeurIPS 2021）等方法，A-ViT 在更低 FLOPs 下保持了有竞争力的准确率，且无需引入额外参数或子网络。

### 定性分析

**Figure 3** 展示了不同图像上动态 token 深度的分布：token 计算量的分配与视觉特征高度对齐，信息丰富的区域（如物体主体）被自适应地处理到更深层，而背景区域则提前停止。**Figure 4(a)** 进一步从空间位置角度量化了 token 平均深度分布，**Figure 4(b)** 则展示了各层停止分数的统计特征。**Figure 5** 对比了“困难”与“简单”样本：具有均匀背景的简单样本平均 token 深度显著更低，验证了 A-ViT 根据图像复杂度自适应分配计算的能力。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2112_07658/figures/006_Figure_5.jpg]]
*Figure 5: Visual comparison of hard and easy samples from the ImageNet-1K validation set determined by average token depth. Note that all images above be correctly classified – only difference is that hard samples require more depths for tokens to process their semantic information. Tokens in the left images exit approximately 5 layers later compared to the right images*

**Table 1** 分析了不同 ImageNet 类别对自适应计算的稳定性差异，揭示了某些类别对 token 提前停止更为敏感，而另一些类别则几乎不受影响。**Figure 6** 与 DynamicViT 的定性对比显示，A-ViT 更有效地聚焦于语义对象，丢弃了更多背景 token，从而节省了更多计算。

### 消融实验

**细粒度 token 停止 vs. 层级 ACT。** 对比 Table 2 的首行和末行可知，token 级别的细粒度 ponder 损失相比传统层级 ACT（Graves, arXiv 2016）将平均 token 深度减少约 **3 层**，并额外降低 **25% 的 FLOPs**。这一结果直接验证了空间自适应停止相对于统一层级停止的显著优势。

**分布先验正则化的作用。** **Figure 7** 展示了有无分布先验正则化的训练曲线对比。引入 $\mathcal{L}_{\mathrm{distr.}}$ 后，训练快速收敛到目标深度，并带来 **6.4% 的精度增益**。相比之下，仅使用 ponder 损失（无分布先验）的训练不仅收敛缓慢，且最终精度明显偏低。这表明分布先验正则化是稳定 ACT 训练和实现高精度-效率权衡的关键组件。

**嵌入维度占用的影响。** 为验证复用现有嵌入维度的可行性，实验将嵌入向量中一个随机索引位置置零，并在不微调的情况下评估精度损失。在 DeiT-T/S 变体上重复 10 次，ImageNet-1K Top-1 准确率仅下降 **0.08% ± 0.04% / 0.04% ± 0.03%**，证明占用单一嵌入维度对原始模型性能几乎无影响。

**额外停止子网络的必要性。** 若引入专用的停止子网络（而非复用现有参数），仅带来约 **0.06%** 的微小精度提升，却引入了 **12.6%** 的推理吞吐开销和约 0.2M 额外参数。这一结果有力支持了 A-ViT “零额外参数”设计选择的合理性。

### 方法与基线对比的公平性说明

所有方法均基于相同的 DeiT 代码库和训练 recipe 实现，吞吐量在相同的 NVIDIA TITAN RTX 2080 GPU 上使用相同 batch size 和预热流程测量。对于其他动态方法，作者进行了详细的超参数搜索以保证各方法的最优性能，确保比较的公平性。

### 失败模式与局限性

尽管 A-ViT 在图像分类上表现出色，但仍存在以下局限：
- **任务泛化未验证**：当前仅验证了 ImageNet-1K 分类任务，尚未在目标检测、分割等更复杂的视觉任务上进行广泛测试。
- **超参数敏感性**：训练对 $\alpha_p$、$\alpha_d$ 及目标停止深度等超参数仍有一定敏感性，尽管分布先验正则化已显著缓解了该问题。
- **硬件适配限制**：动态 token 移除带来的理论 FLOPs 降低在实际硬件上的加速效果可能受限于稀疏计算的支持程度，部分平台上实际加速比可能低于理论值。
- **停止机制刚性**：方法基于固定的停止分数阈值（$1-\epsilon$）和单一嵌入维度（$e=0$），未来可探索更灵活的停止准则或自适应维度选择。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2112_07658/figures/008_Table.jpg]]

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2112_07658/figures/009_Table.jpg]]

## 定位与知识库关联

### 核心谱系定位

A‑ViT 处于**自适应视觉推理**与**高效 Transformer** 的交叉点，其直接技术祖先为 **ACT**（Adaptive Computation Time, Graves, arXiv 2016）。ACT 最初为 RNN 设计，在层级别对所有 token 同时施加停止信号——即整层计算要么继续、要么全体终止。A‑ViT 的关键突破在于将这一机制**空间化**：将停止决策下沉到单个 token 粒度，使得不同空间位置的 token 可在不同深度提前退出，从而首次在视觉 Transformer 中实现细粒度的输入自适应计算。

与 ACT 的层级别停止相比，A‑ViT 的 token 级细粒度 ponder 损失使平均 token 深度减少约 3 层，并额外降低 25% 的 FLOPs（Table 2 首末行对比）。这一因果链路清晰：**停止粒度的细化直接转化为计算冗余的消除**。

### 与同期方法的对比边界

在自适应 token 削减这一赛道上，**DynamicViT**（Rao et al., NeurIPS 2021）是 A‑ViT 最直接的可比方法。两者核心差异体现在三个维度：

| 维度 | DynamicViT | A‑ViT |
|------|-----------|-------|
| 停止机制 | Gumbel‑softmax 采样的二元掩码，在固定层数后一次性丢弃 token | 逐层累积 sigmoid 停止概率，token 可在不同深度自然退出 |
| 参数开销 | 需额外引入预测模块（约 0.2M 参数） | 复用现有 MLP 层中单个嵌入维度，零额外参数 |
| 语义对齐 | 保留/丢弃决策基于全局重要性分数 | 停止深度与局部视觉特征高度对齐（Figure 3），更有效地聚焦语义对象并丢弃更多背景 token（Figure 6） |

从定量角度看，A‑ViT‑T 在 0.8G FLOPs 下达到 71.0% Top‑1 准确率，而 DynamicViT 在相近 FLOPs 下的精度‑效率权衡点不及 A‑ViT（Table 2）。消融实验进一步验证了零额外参数设计的合理性：额外引入停止子网络仅带来约 0.06% 的精度增益，却引入 12.6% 的推理吞吐开销。

**PonderNet**（Banino et al., ICML Workshop 2021）则代表了另一条技术路径——基于几何分布的随机停止采样。A‑ViT 未直接与其对比，但 ACT 类方法的训练不稳定性正是 PonderNet 试图解决的问题，而 A‑ViT 通过分布先验正则化从另一角度缓解了该问题。

### 基础架构依赖与可迁移性

A‑ViT 以 **DeiT**（Touvron et al., ICML 2021）为基础架构进行验证。DeiT 作为标准 ViT 的改进版，其块结构（自注意力 + MLP）的通用性意味着 A‑ViT 的停止机制理论上可嵌入任何具有类似 token 处理流程的视觉 Transformer。然而，当前验证仅限于 ImageNet‑1K 分类任务，尚未在以下维度提供证据：

- **架构变体**：如 Swin Transformer 的窗口注意力、PVT 的金字塔结构是否兼容 token 级停止
- **任务泛化**：目标检测、分割等密集预测任务中，token 提前停止是否会影响空间定位精度
- **视频扩展**：时间维度的冗余是否可被类似机制利用

### 训练稳定性与超参数敏感性

A‑ViT 引入的分布先验正则化 $\mathcal{L}_{\mathrm{distr.}} = \mathrm{KL}(\mathcal{H} \| \mathcal{H}^{\mathrm{target}})$ 是其训练稳定性的核心保障。该正则项通过 KL 散度约束各层平均停止分数的分布趋近于目标高斯分布，引导平均停止深度收敛至预设值。消融实验显示，去除该正则项后训练收敛显著减缓，最终精度下降 6.4%（Figure 7）。

尽管如此，训练仍对超参数组合 $(\alpha_p, \alpha_d, N^{\mathrm{target}})$ 存在一定敏感性。论文通过共享 sigmoid 控制门参数（$\gamma=5, \beta=-10$）和固定嵌入索引（$e=0$）降低了搜索空间，但目标深度的选择本质上是一个精度‑效率权衡的人为先验，缺乏自适应的目标深度选择机制。

### 硬件适配的现实约束

A‑ViT 报告的吞吐量提升（DeiT‑Tiny +62%，DeiT‑Small +38%）基于 NVIDIA TITAN RTX 2080 GPU 测量。然而，token 的动态移除产生的稀疏计算模式在通用 GPU 上可能无法完全转化为线性加速——实际收益依赖于硬件对稀疏矩阵运算的优化程度。这一硬件依赖性是所有动态推理方法的共性局限，论文未对此进行深入讨论。

### 开放问题

1. **停止准则的泛化**：当前固定阈值 $1-\epsilon$ 和单一嵌入维度 $e=0$ 是否为最优选择？是否存在更灵活的停止条件（如可学习的阈值或基于注意力的停止信号）？
2. **与 token 合并的协同**：A‑ViT 丢弃冗余 token，而 token 合并方法（如 ToMe）压缩相似 token——两者是否可互补以进一步降低计算量？
3. **无正则化的训练策略**：分布先验虽然有效，但引入了额外超参数。是否存在更优雅的训练策略（如课程学习、渐进式深度调度）可达到类似效果？
4. **跨模态扩展**：文本、语音等序列模态中是否存在类似的空间/时间冗余，可被 token 级自适应停止利用？

## 原文 PDF

![[paperPDFs/CVPR_2022/A_ViT_Adaptive_Tokens_for_Efficient_Vision_Transformer.pdf]]
