---
title: "VP-VAE: Rethinking Vector Quantization via Adaptive Vector Perturbation"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/VP-VAE_Rethinking_Vector_Quantization_via_Adaptive_Vector_Perturbation.pdf
project_link: null
code_link: null
aliases:
- VVVPVFFSP
- VP-VAE
tags:
- arxiv_2026
- topic/vision_multimodal_applications
core_operator: 将训练阶段的离散量化替换为自适应向量扰动，解耦表示学习与码本学习；仅在推理时通过K-Means生成码本，从根本上消除码本崩溃。
primary_logic: 从神经网络视角看，量化操作本质上是向潜在空间注入一个有界的、局部的结构化扰动（即量化误差）。因此，训练时无需显式码本，只需让解码器对符合量化误差分布的扰动具有鲁棒性，即可在推理时无缝切换到离散量化。
claims:
- VP-VAE和FSP在所有码本大小下均保持稳定的高码本利用率（CVU），而VQ-VAE和FSQ在训练后期出现利用率下降。
- VP-VAE和FSP在图像和音频重建质量上均优于或持平于最强基线，且未出现训练失败。
- 去除Metropolis–Hastings（始终接受扰动）导致CVU从0.81降至0.75，重建质量下降，验证了分布一致性扰动的必要性。
- 去除潜在归一化正则项同样损害感知质量和码本平衡，证明其对于尺度估计的重要性。
---

# VP-VAE: Rethinking Vector Quantization via Adaptive Vector Perturbation

> [!tip] 核心洞察
> 从神经网络视角看，量化操作本质上是向潜在空间注入一个有界的、局部的结构化扰动（即量化误差）。因此，训练时无需显式码本，只需让解码器对符合量化误差分布的扰动具有鲁棒性，即可在推理时无缝切换到离散量化。

| 字段 | 内容 |
|------|------|
| 中文题名 | VP-VAE：通过自适应向量扰动重新思考向量量化 |
| 英文题名 | VP-VAE: Rethinking Vector Quantization via Adaptive Vector Perturbation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2602.17133) |
| Topic | #topic/vision_multimodal_applications |
| Method | VP-VAE (Vector Perturbation VAE) 及其轻量变体 FSP (Finite Scalar Perturbation) |
| Dataset | COCO, LibriSpeech, ImageNet, Common Voice |

> [!tip] 效果简介
> - COCO (图像重建) 上，LPIPS↓ VP-VAE (K=1024): 0.1717 vs VQ-VAE (K=1024): 0.1821 (-0.0104)；PSNR↑ FSP (K=1024): 24.1910 vs FSQ (K=1024): 23.6006 (+0.5904)。
> - LibriSpeech (音频重建) 上，PESQ↑ VP-VAE (K=1024): 2.3826 vs SimVQ (K=1024): 1.3213 (+1.0613)；STOI↑ FSP (K=1024): 0.9191 vs FSQ (K=1024): 0.9001 (+0.0190)。
> - ImageNet (分布外泛化-图像) 上，PSNR↑ VP-VAE (K=16384): 23.3166 vs SimVQ (K=16384): 23.0381 (+0.2785)。

## 概要

**核心问题：码本崩溃与耦合优化困境。** 向量量化变分自编码器（VQ-VAE）及其后续变体在训练中面临一个根本性瓶颈：表示学习与码本学习紧密耦合，导致大量码本向量失活（codebook collapse），有效比特率持续下降，形成自反馈的恶性循环。这一问题在跨模态任务中普遍存在——从图像到音频，耦合量化方法均表现出训练后期码本利用率骤降，甚至直接训练失败。

**核心洞察：量化即扰动。** 从神经网络视角审视，离散量化操作本质上是在潜在空间中注入一个有界的、局部的结构化扰动——即量化误差。基于这一洞察，VP-VAE提出将训练阶段的显式码本查找替换为自适应向量扰动，仅在推理时通过K-Means离线生成码本，从根本上解耦表示学习与码本学习，从而消除码本崩溃的结构性根源。

**方法定位：解耦训练范式。** VP-VAE及其轻量变体FSP属于训练策略层面的创新，不改变编解码器架构本身。其核心操作可概括为：在低维瓶颈空间（$d \leq 16$）中，利用FIFO记忆队列与kNN密度估计自适应地确定扰动半径，再通过Metropolis–Hastings采样生成分布一致性的扰动向量，使解码器在训练中学会对符合量化误差分布的扰动保持鲁棒。推理时，对训练集潜在向量运行K-Means++聚类生成码本，无缝切换到标准最近邻量化。FSP则在假设潜在变量近似均匀分布的前提下，用有界均匀扰动替代复杂的MH采样，并用Lloyd-Max最优区间中心量化替代边界舍入。

**主要结果概览。** 在COCO图像重建上，VP-VAE以K=1024码本取得LPIPS 0.1717，优于VQ-VAE的0.1821；FSP取得PSNR 24.1910，优于FSQ的23.6006。在LibriSpeech音频重建上，VP-VAE的PESQ达2.3826，显著高于SimVQ的1.3213（后者出现严重码本崩溃）。更重要的是，VP-VAE和FSP在所有码本大小下均保持稳定的高码本利用率（CVU），而VQ-VAE和FSQ的CVU曲线呈先升后降的典型崩溃模式。在ImageNet和Common Voice上的分布外泛化评估进一步验证了解耦训练范式的优越性。消融实验确认，去除Metropolis–Hastings接受机制或潜在归一化正则项均会导致重建质量下降和码本平衡性恶化。



### 向量量化的核心瓶颈：码本崩溃与训练不稳定性

向量量化变分自编码器（VQ-VAE）及其衍生方法已成为生成式建模中Token化（tokenization）的核心范式，广泛应用于图像、音频、视频等模态的离散表示学习。然而，这类方法长期受困于一个根本性问题：**码本崩溃（codebook collapse）**。在训练过程中，码本中大量向量逐渐失活，只有少数码字被实际使用，导致有效比特率急剧下降，表征能力严重受损。这一现象并非偶然的优化失败，而是源于VQ-VAE训练范式中一个深层耦合——**表示学习与码本优化共享同一量化算子**。

具体而言，编码器输出的连续潜在向量通过最近邻查找映射到离散码字，而码本本身又依赖编码器的输出来更新。这种双向依赖形成了一个自反馈的恶性循环：码本利用率下降使得解码器只能从极少数码字中重建信号，梯度信号进一步收缩，反过来又加速码本失活。**VQ-VAE**（Van Den Oord et al., NeurIPS 2017）依赖直通估计器（STE）来近似量化操作的梯度，但STE引入的梯度偏差本质上无法解决这一结构性问题。后续工作如**SimVQ**（Zhu et al., ICCV 2025）通过可学习线性层重新参数化码本、**FSQ**（Mentzer et al., ICLR 2023）通过固定标量网格绕过可学习码本，虽然在一定程度上缓解了崩溃，但并未从根本上解耦表示学习与离散化之间的关系。

### 现有方法的局限：耦合范式下的两难困境

当前主流方法可大致分为两类，各自面临不同的局限：

- **耦合方法**（如VQ-VAE、SimVQ）：训练时编码器、码本、解码器联合优化，量化操作直接参与前向传播。优势在于端到端学习，但码本崩溃风险始终存在，尤其在跨模态任务中表现脆弱——VQ-VAE在音频重建上甚至出现码本利用率趋近于零的训练失败（见Table 1中“-”标记）。
- **固定量化方法**（如FSQ、TokenBridge）：使用预定义的量化网格或分位数离散化，避免了可学习码本的不稳定性。然而，固定网格的设计高度依赖对潜在分布的先验假设。**FSQ**的rounding操作将潜在变量投影到网格边界，导致量化输出分布偏向极端值，偏离Lloyd-Max最优量化理论所要求的区间中心重建原则。**TokenBridge**（Wang et al., ICCV 2024）虽采用高斯分位数网格，但其先训练KL正则化VAE再离散化的两阶段流程割裂了表示学习与量化目标。

两类方法的共同困境在于：**训练阶段的离散化操作要么引入不稳定的耦合，要么依赖强分布假设**。这引出一个关键问题——是否必须在训练时显式执行离散量化？

### 核心动机：从“量化即离散化”到“量化即扰动”

VP-VAE的核心洞察在于对量化操作的本质重新理解：**从神经网络的视角看，量化等价于向潜在空间注入一个有界的、局部的结构化扰动（即量化误差）**。如果解码器在训练过程中已经学会对这种扰动保持鲁棒，那么在推理时无缝切换到离散量化就变得可行——无需在训练时维护任何码本。

这一视角转换带来一个根本性的解耦策略：**训练阶段用自适应向量扰动替代离散量化，推理阶段再通过K-Means生成码本进行最近邻量化**。这样，表示学习完全摆脱了码本优化的束缚，码本崩溃问题从根源上被消除。扰动机制需要满足两个关键约束：（1）扰动尺度应与目标码本大小决定的预期量化误差对齐；（2）扰动后的向量应停留在原始潜在分布的高密度区域，避免分布偏移导致解码器行为异常。

基于此，VP-VAE设计了基于Metropolis-Hastings采样的自适应扰动机制，结合kNN非参数密度估计和潜在归一化正则，确保扰动在统计意义上与量化误差分布一致。其轻量变体FSP（Finite Scalar Perturbation）则在假设潜在分布近似均匀的前提下，用有界均匀扰动和Lloyd-Max最优中心量化实现高效简化。



## 核心方法与创新机理

VP-VAE的核心创新在于**将VQ-VAE训练中表示学习与码本学习的强耦合彻底解耦**，从根本上消除了码本崩溃（codebook collapse）这一长期困扰向量量化方法的结构性缺陷。

### 问题根源：耦合导致的恶性循环

传统VQ-VAE及其变体（如**SimVQ**，Zhu et al., ICCV 2025）在训练时同时优化编码器、解码器和码本向量。表示学习与码本学习相互依赖：编码器输出的潜在表示决定了码本向量的更新方向，而码本向量的分布又通过最近邻量化和STE梯度反向约束编码器。当部分码本向量因初始化或梯度不平衡而被“冷落”时，它们接收的更新信号减弱，进一步降低被选中的概率，形成**自反馈的恶性循环**——码本利用率持续下降，有效比特率衰减，最终导致训练失败。Table 1中VQ-VAE在音频任务上CVU接近0即为这一失效模式的典型表现。

### 核心洞察：量化即结构化扰动

VP-VAE的方法论出发点是一个简洁的神经网络视角：**量化操作本质上是在潜在空间中注入一个有界的、局部的结构化扰动**——即量化误差。如果解码器在训练时能够对符合量化误差分布的扰动保持鲁棒性，那么推理时切换到离散量化就不会引入意外的分布偏移。这一洞察使得训练阶段可以完全抛弃显式码本。

### 关键变更点（Changed Slots）

基于上述洞察，VP-VAE在四个关键设计点上与基线方法形成差异：

**1. 训练阶段量化算子：从最近邻查找+STE到自适应向量扰动**

这是最根本的变更。VQ-VAE使用 $q(z) = \arg\min_{c\in\mathcal{Q}} \|z - c\|_2$ 进行硬量化，并通过STE将量化器梯度近似为恒等映射。VP-VAE则将其替换为扰动算子 $\tilde{z} = \mathcal{T}(z; \mathcal{S})$，其中 $\mathcal{S}$ 是一个FIFO记忆队列，存储近期潜在向量。扰动通过Metropolis–Hastings采样生成，确保扰动后的向量停留在潜在分布的高密度区域，且扰动尺度与预期的量化误差对齐。训练时无码本参与，从根本上切断了码本崩溃的因果链。

**2. 潜在空间维度：从高维嵌入到低维瓶颈**

传统方法直接在高维嵌入空间（$C \approx 128$）进行量化，这使得非参数密度估计在高维空间中不可靠（维度灾难）。VP-VAE引入可学习的下投影 $P_{\downarrow}$ 和上投影 $P_{\uparrow}$，将扰动和量化操作限制在低维瓶颈空间（$d \leq 16$）：

$$z = P_{\downarrow}(h_t) \in \mathbb{R}^d, \quad \tilde{h}_t = P_{\uparrow}(\tilde{z}) \in \mathbb{R}^C$$

低维空间使得kNN密度估计具有统计可靠性，且自适应扰动半径 $R(z) = \eta D_M(z|\mathcal{S})$ 能够准确反映局部量化误差的预期尺度。

**3. 扰动分布设计：从无扰动/各向同性噪声到分布一致性采样**

VQ-VAE训练时无扰动注入，FSQ虽有噪声注入但采用各向同性高斯噪声，可能导致扰动后的向量偏离潜在分布的支持集。VP-VAE的扰动机制由三个组件协同保证分布一致性：

- **kNN密度估计**：$\pi(z) \propto 1/(D_k(z|\mathcal{S}))^d$，用第k近邻距离近似局部密度；
- **自适应半径**：$R(z) = \eta D_M(z|\mathcal{S})$，其中 $M = \lceil |\mathcal{S}|/K \rceil$，使扰动尺度与目标码本大小K对齐；
- **MH接受机制**：$\alpha(z, z') = \min\left(1, \left(\frac{D_k(z) \cdot D_M(z)}{D_k(z') \cdot D_M(z')}\right)^d\right)$，拒绝偏离高密度区域的候选扰动。

消融实验（Table 3）直接验证了MH机制的必要性：去除MH（始终接受扰动）导致CVU从0.81降至0.75，LPIPS从0.1717升至0.1756。

**4. FSP的量化网格与训练策略：从边界rounding到Lloyd-Max中心量化**

FSP作为VP-VAE的轻量变体，针对潜在变量近似均匀分布的场景简化了扰动机制。其关键改进在于：FSQ将潜在变量投影到固定标量网格的**边界**上（rounding操作），而FSP使用Lloyd-Max最优重建点——即等宽区间的**中心** $\mathcal{C} = \{(\ell + 1/2)/L\}_{\ell=0}^{L-1}$——进行量化。在均匀分布假设下，中心量化是理论最优的。Figure 2直观展示了这一差异：FSP产生的量化输出分布接近均匀，而FSQ及其变体偏向边界，导致输出分布失衡。训练时FSP以50%概率混合使用均匀扰动和显式STE量化，进一步平滑训练信号。

### 解耦范式的推理阶段

训练完成后，VP-VAE对训练集所有潜在向量运行K-Means++聚类，生成显式码本 $\mathcal{Q}$。推理时使用标准最近邻量化 $q(z) = \arg\min_{c\in\mathcal{Q}} \|z - c\|_2$。由于解码器在训练时已学会对符合量化误差分布的扰动保持鲁棒，这一从扰动到量化的切换不会引入性能退化。



VP-VAE 的核心设计是将 VQ-VAE 中耦合的“表示学习”与“码本学习”彻底解耦，从根本上消除码本崩溃（codebook collapse）。其训练与推理遵循两条完全不同的路径，仅在推理阶段才引入显式码本。

### 训练阶段：自适应向量扰动

训练时，模型完全不存在码本。编码器输出的 Token 特征 $h_t \in \mathbb{R}^C$ 首先经过可学习的下投影 $P_{\downarrow}$ 压缩到低维瓶颈空间（$d \leq 16$），得到潜在向量 $z \in \mathbb{R}^d$。低维投影是整个框架的关键前提——它使得后续基于 kNN 的密度估计在有限样本下变得可靠。

在此低维空间，VP-VAE 用一个显式的扰动算子 $\mathcal{T}$ 替代传统的离散量化：

$$ \tilde{z} = \mathcal{T}(z; \mathcal{S}), \quad \hat{x} = D(\{P_{\uparrow}(\tilde{z})\}_{t=1}^T) $$

扰动后的向量 $\tilde{z}$ 经上投影 $P_{\uparrow}$ 恢复至原始嵌入维度 $C$，送入解码器重建。端到端训练损失仅包含重建损失与潜在归一化正则项 $\mathcal{L}_{\text{norm}}$，无需码本相关的承诺损失或 EMA 更新。

扰动算子 $\mathcal{T}$ 的核心是 **Metropolis–Hastings（MH）采样**，其运作依赖一个 FIFO 记忆队列 $\mathcal{S}$，存储近期产生的潜在向量。具体流程如下：

1. **自适应半径估计**：对每个 $z$，在队列 $\mathcal{S}$ 中查找第 $M$ 近邻距离 $D_M(z|\mathcal{S})$，其中 $M = \lceil |\mathcal{S}| / K \rceil$，$K$ 为目标码本大小。扰动半径 $R(z) = \eta D_M(z|\mathcal{S})$ 自适应地匹配局部量化误差的预期尺度。

2. **kNN 密度估计**：以第 $k$ 近邻距离近似局部密度 $\pi(z) \propto 1 / (D_k(z|\mathcal{S}))^d$，为 MH 接受机制提供目标分布。

3. **MH 扰动采样**：在半径为 $R(z)$ 的 $d$ 维球内均匀采样候选 $z'$，计算接受概率 $\alpha(z, z') = \min\left(1, \left(\frac{D_k(z) \cdot D_M(z)}{D_k(z') \cdot D_M(z')}\right)^d\right)$，以该概率接受 $z'$ 作为 $\tilde{z}$，否则保留原值。此机制保证扰动后的向量不偏离潜在分布的高密度区域，使解码器在训练中学会对“类量化误差”的结构化扰动具有鲁棒性。

4. **潜在归一化正则**：$\mathcal{L}_{\text{norm}} = \lambda_1 \|\mu_{\text{batch}}\|_2^2 + \lambda_2 \|\sigma_{\text{batch}}^2 - \mathbf{1}\|_2^2$ 鼓励潜在变量在各维度上零均值、单位方差，确保 kNN 距离计算的尺度有效性。

### 推理阶段：离线码本生成与最近邻量化

训练完成后，VP-VAE 对训练集所有潜在向量运行 K-Means++ 聚类，生成显式码本 $\mathcal{Q}$。推理时，对每个 $z$ 执行标准最近邻量化：

$$ q(z) = \arg\min_{c \in \mathcal{Q}} \|z - c\|_2 $$

由于解码器已在训练中适应了与量化误差分布一致的扰动，此时从扰动切换到离散量化是平滑无缝的，不会产生训练-推理不匹配。

### 轻量变体 FSP

FSP（Finite Scalar Perturbation）在“潜在变量近似均匀分布”的假设下大幅简化了扰动机制。它通过单调递增的类 CDF 激活函数 $g$（如 Sigmoid、Normal CDF）将预激活值 $a$ 映射到 $[0, 1]^d$，得到 $z = g(a)$。训练时以 50% 概率使用有界均匀扰动，50% 概率使用 **Lloyd-Max 最优重建点**（区间中心而非边界）进行显式量化并配合 STE 梯度近似。推理时直接使用区间中心量化。FSP 避免了 MH 采样和 kNN 搜索的开销，同时通过中心量化策略在理论上优于 FSQ 的边界舍入。

### 输入输出流总结

| 阶段 | 输入 | 处理流程 | 输出 |
|------|------|----------|------|
| 训练 | 原始数据 $x$ | $x \to \text{Encoder} \to \{h_t\} \to P_{\downarrow} \to z \to \mathcal{T}(z;\mathcal{S}) \to \tilde{z} \to P_{\uparrow} \to \{\tilde{h}_t\} \to \text{Decoder} \to \hat{x}$ | 重建 $\hat{x}$ |
| 推理 | 原始数据 $x$ | $x \to \text{Encoder} \to \{h_t\} \to P_{\downarrow} \to z \to q(z) \to c \to P_{\uparrow} \to \{\tilde{h}_t\} \to \text{Decoder} \to \hat{x}$ | 离散 Token 序列与重建 $\hat{x}$ |

训练与推理的唯一差异在于低维空间中的操作：训练用 $\mathcal{T}$（自适应向量扰动），推理用 $q$（最近邻量化）。码本仅在推理前通过 K-Means 一次性生成，训练全程不参与，这是 VP-VAE 避免码本崩溃的结构性保障。

### 补充图表

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2602_17133/figures/006_Figure_1.jpg]]
*Figure 1: Codebook utilization during training. CVU curves for different methods on image reconstruction (K=1024). VQ-VAE and FSQ exhibit an initial rise followed by a decline. VP-VAE and FSP maintain stable, high utilization throughout training*



VP-VAE的核心设计围绕一个中心思想展开：**训练时用自适应向量扰动替代离散量化，推理时再用离线生成的码本进行最近邻量化**，从而将表示学习与码本学习彻底解耦。整个框架由五个关键模块构成。

### 低维投影与恢复

为避免高维空间中密度估计的“维度灾难”，VP-VAE在编码器输出的每个Token特征 $h_t \in \mathbb{R}^C$ 与扰动/量化操作之间插入了一个低维瓶颈：

$$z = P_{\downarrow}(h_t) \in \mathbb{R}^d, \quad \tilde{h}_t = P_{\uparrow}(\tilde{z}) \in \mathbb{R}^C$$

其中 $d \leq 16$。$P_{\downarrow}$ 和 $P_{\uparrow}$ 是可学习的线性投影层。所有扰动（训练时）和量化（推理时）均在压缩后的 $d$ 维空间进行，扰动后的向量 $\tilde{z}$ 再通过上投影恢复到原始嵌入维度送入解码器。这一设计使得后续的kNN密度估计在低维空间中变得可靠且计算可行。

### 自适应扰动半径与记忆队列

扰动的尺度需要与预期的量化误差对齐。VP-VAE通过一个FIFO记忆队列 $\mathcal{S}$ 存储近期编码的潜在向量，并基于目标码本大小 $K$ 自适应地估计局部扰动半径：

$$M = \left\lceil \frac{|\mathcal{S}|}{K} \right\rceil, \qquad R(z) = \eta \, D_M(z \mid \mathcal{S})$$

其中 $D_M(z \mid \mathcal{S})$ 表示 $z$ 到队列 $\mathcal{S}$ 中第 $M$ 近邻的距离。直观上，$M$ 是每个码本向量平均覆盖的样本数，因此第 $M$ 近邻距离近似了该区域的量化半径。超参数 $\eta$ 控制扰动尺度的整体缩放。队列通过随机子采样缓解存储开销，同时维持对近期潜在分布的可靠近似。

### Metropolis–Hastings扰动采样

单纯的各向同性扰动可能将潜在向量推离高密度区域，导致解码器在训练与推理之间出现分布偏移。VP-VAE采用Metropolis–Hastings（MH）采样来保证扰动后的向量仍停留在经验潜在分布的支持集内。

首先，用kNN距离估计局部密度：

$$\pi(z) \propto \frac{1}{(D_k(z \mid \mathcal{S}))^d}$$

其中 $D_k$ 是第 $k$ 近邻距离。随后，在当前点 $z$ 处以半径 $R(z)$ 的 $d$ 维球内均匀采样候选扰动：

$$z' = z + u, \quad u \sim \mathrm{Unif}(\mathcal{B}(0, R(z)))$$

为保持分布一致性，以如下简化接受概率决定是否采纳 $z'$：

$$\alpha(z, z') = \min\left(1, \left(\frac{D_k(z) \cdot D_M(z)}{D_k(z') \cdot D_M(z')}\right)^d\right)$$

最终扰动输出为：

$$\tilde{z} = \begin{cases} z', & \text{以概率 } \alpha(z, z'), \\ z, & \text{否则。} \end{cases}$$

这一机制的本质是构造一个以经验潜在密度为平稳分布的马尔可夫链，确保扰动注入不会系统性地偏离训练分布。

### 潜在归一化正则项

kNN距离计算依赖于各维度尺度的可比性。若潜在变量在某个维度上方差过大，将主导距离度量，破坏密度估计的有效性。为此，VP-VAE引入一个批次级矩匹配正则项：

$$\mathcal{L}_{\mathrm{norm}} = \lambda_1 \|\mu_{\mathrm{batch}}\|_2^2 + \lambda_2 \|\sigma_{\mathrm{batch}}^2 - \mathbf{1}\|_2^2$$

鼓励每个批次内的潜在向量在 $d$ 个维度上均保持零均值、单位方差。消融实验（Table 3）表明，去除该正则项会使LPIPS从0.1717升至0.1850，验证了其对尺度估计稳定性的关键作用。

训练总损失为重建损失与该正则项之和：

$$\mathcal{L} = \mathcal{L}_{\mathrm{rec}}(x, \hat{x}) + \mathcal{L}_{\mathrm{norm}}$$

### 离线码本生成与推理量化

训练完成后，对训练集所有潜在向量运行K-Means++聚类，得到 $K$ 个聚类中心作为码本 $\mathcal{Q}$。推理时，对每个潜在向量执行标准最近邻量化：

$$q(z) = \arg\min_{c \in \mathcal{Q}} \|z - c\|_2$$

由于训练阶段解码器已通过MH扰动学会对符合量化误差分布的扰动保持鲁棒，这一从扰动到量化的切换无需任何微调即可无缝衔接。

### FSP轻量变体

FSP（Finite Scalar Perturbation）针对潜在变量近似均匀分布的场景做了大幅简化。首先通过单调递增的类CDF函数 $g$（如Sigmoid、Normal CDF）将预激活值 $a$ 映射到单位区间：

$$z = g(a) \in [0, 1]^d$$

正则项施加在预激活 $a$ 上，以匹配激活后的目标分布：

$$\mathcal{L}_{\mathrm{norm}}^{\mathrm{FSP}} = \lambda_1 \|\mu_{\mathrm{batch}}(a)\|_2^2 + \lambda_2 \|\sigma_{\mathrm{batch}}^2(a) - \sigma_g^2 \mathbf{1}\|_2^2$$

在均匀分布假设下，Lloyd–Max最优标量量化重建点为等宽区间的中心：

$$\mathcal{C} = \left\{ \frac{\ell + 1/2}{L} \right\}_{\ell = 0}^{L-1}$$

训练时以50%概率使用有界均匀扰动，50%概率使用中心量化配合STE梯度近似。Figure 2 从原理上揭示了FSP优于FSQ的根本原因：FSP的区间中心量化产生的输出分布更接近均匀，符合Lloyd–Max最优性；而FSQ的边界rounding导致输出偏向网格边界，码本利用率天然不均衡。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2602_17133/figures/007_Figure_2.jpg]]
*Figure 2: Output distributions of fixed quantization schemes. Given a uniform latent distribution, we compare the quantized output distributions produced by FSQ, FSQ with noise, symmetric FSQ with noise, and FSP. They are all configured with L=4 quantization levels. FSP produces a more uniform output distribution, aligning with the Lloyd–Max optimality principle*



## 实验与关键发现

### 域内重建主结果

Table 1 汇总了图像（COCO）和音频（LibriSpeech）两个模态上的域内重建结果。VP-VAE 和 FSP 在所有码本大小下均保持稳定的高码本利用率（CVU），而 VQ-VAE 和 FSQ 在训练后期出现利用率下降，VQ-VAE 在音频任务上甚至因严重码本崩溃导致训练失败（表中以“-”标记）。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2602_17133/figures/001_Table_1.jpg]]
*Table 1: In-domain reconstruction results. Models are trained and evaluated on COCO (image) and LibriSpeech (audio). “-” indicates training failure due to severe codebook collapse. VP-VAE and FSP demonstrate consistent stability and high fidelity across both modalities, whereas baselines often degrade in specific task*

图像重建方面，VP-VAE 在 K=1024 时取得 LPIPS 0.1717，显著优于 VQ-VAE 的 0.1821（Δ -0.0104）；FSP 在 K=1024 下 PSNR 达到 24.1910，比 FSQ 的 23.6006 高出 0.5904。在最大码本 K=16384 下，VP-VAE 的 LPIPS 进一步降至 0.1434，PSNR 升至 25.2032，CVU 仍维持 0.7957，而 VQ-VAE 的 CVU 仅为 0.3679（K=256 时），表明耦合训练范式在码本增大时利用率恶化更为严重。

音频重建的优势更为突出：VP-VAE 在 K=1024 下 PESQ 达 2.3826，相较 SimVQ 的 1.3213 提升超过 1.0；FSP 的 STOI 为 0.9191，优于 FSQ 的 0.9001。VQ-VAE 在音频上 CVU 接近 0，完全失效，说明其梯度近似策略无法应对音频潜在空间的高动态范围。

**关键因果链**：VP-VAE/FSP 的稳定 CVU 源于训练阶段完全移除了显式码本与最近邻查找，从根本上切断了“码本失活 → 梯度信号减弱 → 更多向量失活”的自反馈崩溃循环。解码器仅需对符合量化误差分布的扰动保持鲁棒，推理时再通过 K-Means 生成码本，码本利用率由聚类质量而非训练动态决定。

### 分布外泛化

Table 2 展示了在 COCO/LibriSpeech 上训练的模型迁移到 ImageNet（图像）和 Common Voice（音频）的跨域性能。VP-VAE 在 K=16384 下 ImageNet PSNR 为 23.3166，高于 SimVQ 的 23.0381（Δ +0.2785）；音频上 VP-VAE 的 PESQ 为 2.4231，略优于 FSP 的 2.3828。解耦训练范式使模型学到的潜在表示不受特定码本分布的约束，因而对域偏移更鲁棒。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2602_17133/figures/002_Table_2.jpg]]
*Table 2: Out-of-distribution generalization results. Models trained on COCO/LibriSpeech are evaluated on unseen datasets: ImageNet (image) and Common Voice (audio). Our decoupled training paradigm yields superior generalization compared to baseline methods*

### 消融实验

Table 3 针对 VP-VAE 的两个核心组件进行了消融（K=1024，COCO 图像重建）：

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2602_17133/figures/003_Table_3.jpg]]
*Table 3: Ablation on VP-VAE components. We evaluate the contribution of latent normalization and Metropolis–Hastings mechanism on image reconstruction (K=1024). Both components contribute to reconstruction quality and codebook balance*

- **去除 Metropolis–Hastings 接受机制**（始终接受扰动）：CVU 从 0.8102 骤降至 0.7467，LPIPS 从 0.1717 升至 0.1756，PSNR 从 23.8878 降至 23.8053。这表明无约束的随机扰动会将潜在向量推向低密度区域，破坏分布一致性，解码器无法有效重建。
- **去除潜在归一化正则项**（$\mathcal{L}_{\text{norm}}$）：LPIPS 从 0.1717 升至 0.1850，CVU 轻微降至 0.8052。该正则项保证了 kNN 距离计算的尺度有效性——若各维度方差不一致，欧氏距离将被高方差维度主导，密度估计和扰动半径均会失准。

### FSP 激活函数敏感性

Table 4 和 Table 5 分别报告了 FSP 在图像和音频上使用三种 CDF-like 激活函数（Tanh、Normal CDF、Laplace CDF）的结果。各激活函数在 LPIPS、PSNR、PESQ、STOI 上差异微小，无单一激活在所有指标上占优。这表明 FSP 对“近似均匀”假设的具体实现形式不敏感，只要激活函数能将预激活值映射到有界区间并近似均匀分布，Lloyd-Max 中心量化即可有效工作。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2602_17133/figures/004_Table_4.jpg]]
*Table 4: FSP activation functions on images. We compare three CDF-like activations, which affect how well the “approximately uniform” assumption holds and thus the effectiveness of FSP (K=1024)*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2602_17133/figures/005_Table_5.jpg]]
*Table 5: FSP activation functions on audio. We evaluate three CDF-like activations on audio (K=1024)*

### 失败模式分析

VQ-VAE 在音频重建上的严重码本崩溃（CVU ≈ 0）是耦合训练范式最直接的失败证据。其根本原因在于：音频信号的潜在空间具有更高的动态范围和更复杂的分布结构，最近邻查找 + STE 梯度近似在此场景下极易陷入“赢者通吃”的退化状态——少数码本向量被频繁更新，其余向量因梯度稀疏而逐渐偏离数据流形，最终完全失活。FSQ 虽无显式码本，但其边界 rounding 操作导致量化输出集中在网格边界（Figure 2 所示），等效于有效码本数量远小于标称值 K，在训练后期同样出现 CVU 下降（Figure 1 中的先升后降曲线）。

VP-VAE 和 FSP 未出现任何训练失败案例，验证了解耦范式对码本崩溃的免疫性。需注意，VP-VAE 的 kNN 密度估计在记忆队列 $\mathcal{S}$ 较大时引入额外计算开销，目前通过低维瓶颈（d ≤ 16）和随机子采样缓解，但该点仍需手动验证在大规模部署中的实际影响。



## 定位与知识库关联

### 与基线方法的关系

VP-VAE的核心贡献在于将VQ-VAE训练中“表示学习”与“码本学习”的耦合关系彻底解耦。在传统耦合框架中，编码器、解码器与码本向量通过STE梯度近似联合优化，形成相互制约的三角关系：编码器需适应码本离散化，码本需追踪编码器输出的分布漂移，而解码器则依赖不稳定的量化表示。这种耦合被本文识别为码本崩溃的根本原因——一旦部分码本向量失活，有效比特率下降，重构质量恶化，进而通过梯度反馈进一步抑制失活码本的更新，形成自反馈的恶性循环。

**VQ-VAE**（Van Den Oord et al., NeurIPS 2017）是该范式的奠基工作，其最近邻查找与STE直通估计构成了耦合训练的经典模板。VP-VAE的实验表明，VQ-VAE在音频重建任务上出现严重码本崩溃（CVU接近0），在图像重建上CVU也仅为0.3679（K=256），验证了耦合训练的固有脆弱性。

**SimVQ**（Zhu et al., ICCV 2025）作为先进的耦合方法，通过可学习的线性层重新参数化码本以缓解表示-码本失配，但仍未脱离联合优化的框架。在分布外泛化实验中，VP-VAE在ImageNet上以PSNR 23.3166优于SimVQ的23.0381（K=16384），表明解耦训练学到的表示具有更强的跨域鲁棒性。

**FSQ**（Mentzer et al., ICLR 2023）采用固定标量网格进行量化，消除了可学习码本，从而规避了码本崩溃问题。VP-VAE的FSP变体在FSQ基础上做了两项关键改进：一是将量化重建点从区间边界（rounding）改为Lloyd-Max最优的区间中心，使输出分布更均匀；二是训练时以50%概率混合均匀扰动与显式STE量化，而非单纯依赖噪声注入。Table 1显示FSP在COCO上PSNR 24.1910显著优于FSQ的23.6006（K=1024），Figure 2从原理上解释了这一差异——FSQ及其变体的量化输出偏向区间边界，而FSP的输出分布更接近均匀，符合Lloyd-Max最优量化理论。

**TokenBridge**（Wang et al., ICCV 2024）基于固定高斯分位数网格进行离散化，与FSP同属固定量化器家族，但其网格设计依赖于对潜在分布的先验假设。VP-VAE的自适应扰动策略则无需此类假设，通过kNN密度估计实时感知局部密度。

### 适用边界与局限

**适用场景**：VP-VAE的解耦训练范式适用于任何需要学习离散潜在表示的连续数据压缩任务。当前验证覆盖了图像（COCO）和音频（LibriSpeech）两种模态的自编码器结构Token化，在码本大小从256到16384的范围内均保持稳定的高码本利用率。分布外泛化实验（ImageNet、Common Voice）表明，解耦训练学到的表示具有更好的跨域迁移能力。

**计算开销**：VP-VAE依赖非参数kNN密度估计和Metropolis-Hastings采样，训练时引入额外计算。具体而言，FIFO记忆队列的维护和每次扰动的k近邻查询增加了前向传播成本。当前通过低维瓶颈（d ≤ 16）和随机子采样缓解，但作者明确指出，在超大规模模型上仍需近似最近邻搜索等加速方案。

**FSP的假设限制**：FSP的简化依赖于潜在变量近似均匀分布的假设。当该假设成立时，FSP以极低的计算代价获得接近VP-VAE的性能；但当分布严重偏离均匀时，VP-VAE仍保持优势，FSP可能退化。Table 4和Table 5的激活函数消融显示，不同CDF-like激活（Tanh、Normal CDF、Laplace CDF）对FSP性能影响微小，表明FSP对激活函数的具体形式不敏感，但对“近似均匀”假设本身的依赖程度仍需进一步量化。

**生成任务验证缺失**：当前实验仅覆盖自编码器结构的Token化任务，尚未验证与自回归或扩散生成器的结合效果。VP-VAE的解耦范式是否能在生成任务中保持码本稳定性和重建质量优势，是需要后续工作验证的关键问题。

### 开放问题

1. **码本大小与扰动精度的关系**：目标码本大小K直接决定了自适应扰动半径的估计（$M = \lceil |\mathcal{S}| / K \rceil$）。K的选择如何影响密度估计的偏差-方差权衡，以及最终的重建质量，缺乏系统性分析。

2. **可扩展的密度估计**：当前kNN密度估计的计算复杂度随记忆队列大小线性增长。能否设计可学习的扰动分布、近似最近邻索引或哈希采样机制，使VP-VAE在视频、高分辨率图像等大规模数据上实用化，是工程落地的关键。

3. **与生成模型的集成**：VP-VAE的解耦训练范式能否与基于Transformer或扩散模型的生成器无缝集成？训练时无码本，推理时通过K-Means生成码本，这一两阶段流程是否会影响生成模型的训练信号质量或采样多样性？

4. **多模态扩展**：在视频、3D点云、分子图等更多模态上，VP-VAE的自适应扰动策略是否同样有效？不同模态的潜在空间几何结构差异可能影响kNN密度估计的可靠性。

5. **FSP假设的鲁棒边界**：“近似均匀”假设的实际偏差在何种程度上开始损害量化效率？能否通过自适应网格划分或可学习的激活函数（如参数化CDF）弥补分布偏移，使FSP在更广泛的场景下保持竞争力？



## 原文 PDF

![[paperPDFs/arxiv_2026/VP-VAE_Rethinking_Vector_Quantization_via_Adaptive_Vector_Perturbation.pdf]]
