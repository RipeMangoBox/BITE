---
title: Differentiable Vector Quantization for Rate-Distortion Optimization of Generative Image Compression
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Differentiable_Vector_Quantization_for_Rate_Distortion_Optimization_of_Generative_Image_Compression.pdf
project_link: null
code_link: "https://github.com/CVL-UESTC/RDVQ"
aliases:
- DVQRDOGIC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在率估计分支引入基于距离的可微软分布代替硬分配，恢复从率损失到编码器的梯度路径，使熵模型能够直接塑造编码器诱导的潜在分布。
primary_logic: 通过训练时解耦重建/编码路径与率优化路径，利用可微软分布作为代理率目标，将标准VQ框架无缝扩展为可联合优化的RDVQ，且不改变推理时的硬量化流程。
claims:
- 去除可微松弛后，即使在更高码率下性能也急剧下降，表明可微索引分布是有效端到端RD优化的关键。
- 与启发式码本尺寸控制(K-means VQ)相比，联合RD学习提供的表示效率更高，所有感知指标均明显更优。
- RDVQ在极低码率下以轻量架构取得领先的感知质量，且模型参数量不到多数现有方法的20%。
- DIV2K-val 上 Bitrate reduction on DISTS vs. RDEIC = 0.0247 bpp (approx.)
---

# Differentiable Vector Quantization for Rate-Distortion Optimization of Generative Image Compression

> [!tip] 核心洞察
> 通过训练时解耦重建/编码路径与率优化路径，利用可微软分布作为代理率目标，将标准VQ框架无缝扩展为可联合优化的RDVQ，且不改变推理时的硬量化流程。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向生成式图像压缩率失真优化的可微向量量化 |
| 英文题名 | Differentiable Vector Quantization for Rate-Distortion Optimization of Generative Image Compression |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.10546) · [Code](https://github.com/CVL-UESTC/RDVQ) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | RDVQ |
| Dataset | DIV2K-val, Kodak, Kodak, DIV2K-val, CLIC2020-test |

> [!tip] 效果简介
> - DIV2K-val 上，Bitrate reduction on DISTS vs. RDEIC 0.0247 bpp (approx.) vs RDEIC (higher bpp for same DISTS) (-75.71% bitrate)。
> - Kodak 上，BD-DISTS 0.0 (reference, best) vs Other VQ-based methods (CGIC, Diffo, OneDC) (best)。
> - Kodak, DIV2K-val, CLIC2020-test 上，DISTS, CLIPIQA state-of-the-art vs multiple GIC methods (SOTA on DISTS and CLIPIQA)。

## 概要

**问题本质**：在基于向量量化（VQ）的生成式图像压缩中，最近邻硬分配操作不可微，切断了从率损失到编码器的梯度路径，导致表示学习与熵建模相互脱耦，无法实现端到端的联合率失真优化。

**核心思路**：RDVQ 在训练时解耦重建/编码路径与率优化路径——保持硬量化用于重建和熵编码，同时在率估计分支引入基于距离的可微软分布 $p_{\mathrm{soft}}$ 作为代理率目标，恢复梯度 $\partial R_{\mathrm{soft}}/\partial \mathbf{y} \neq 0$，使熵模型能够直接塑造编码器诱导的潜在分布，而推理时完全无需改变标准 VQ 的硬量化流程。

**方法定位**：RDVQ 属于 VQ-based 生成式图像压缩方法，与现有基于扩散的生成式压缩（如 PerCo、StableCodec、DDCM）和混合 SQ-VQ 方案（如 RDEIC、DLF）形成对比。其核心差异在于：通过可微松弛实现真正端到端的率失真联合学习，而非依赖启发式码本控制或后验率分配。

**主要结果**：
- 在 DIV2K-val 上，相比 RDEIC，RDVQ 在相同 DISTS 感知质量下节省码率高达 75.71%，在相同 LPIPS 下节省 37.63%。
- 在 Kodak 数据集上，RDVQ 的 BD-DISTS 显著优于所有对比的 VQ-based 方法（CGIC、Diffo、OneDC 等）。
- 模型参数量不到多数现有方法的 20%，在极低码率下取得领先的感知质量（DISTS 和 CLIPIQA 指标）。

**关键证据**：消融实验表明，移除可微松弛后即使在更高码率下性能也急剧恶化（DISTS 从 0.1005 升至 0.2147），证明可微索引分布是实现有效端到端 RD 优化的关键；而采用 K-means 簇尺寸控制码率的启发式方案虽能匹配码率，但所有感知指标均明显劣于联合 RD 学习，表明启发式控制无法有效消除索引分布的冗余。

### 图像压缩的率失真优化框架

有损图像压缩的核心是在编码比特率与重建失真之间寻求最优权衡，这一目标通常形式化为拉格朗日率失真函数 $\mathcal{L} = \lambda R + D(\mathbf{x}, \hat{\mathbf{x}})$。在基于学习的压缩范式中，编码率 $R$ 定义为量化潜变量在熵模型下的期望负对数似然 $R = \mathbb{E}_{\hat{\mathbf{y}}} [ -\log_2 q_{\psi}(\hat{\mathbf{y}}) ]$。通过梯度下降联合优化编码器、量化器和熵模型，可以实现端到端的率失真优化——这是标量量化（scalar quantization, SQ）压缩方法取得成功的核心机制。

### 向量量化的梯度瓶颈

向量量化（Vector Quantization, VQ）通过将连续特征映射到离散码本中的最近邻向量，天然产生高压缩比的离散表示，在生成式图像压缩中展现出巨大潜力。然而，VQ引入了一个根本性的优化障碍：**最近邻硬分配操作不可微**。具体而言，编码器输出 $\mathbf{y}$ 与码本 $\mathcal{C}$ 之间的硬索引分配 $\mathbf{y}_{ind}(b,l) = \arg\min_k \|\mathbf{y}_{b,l} - \mathcal{C}_k\|^2$ 使得率损失对编码器参数的梯度 $\partial R / \partial \mathbf{y}$ 恒为零。

这一梯度断裂造成了两个严重后果：
1. **表示学习与率优化脱耦**：编码器无法从率损失接收优化信号，其学习过程仅受重建损失驱动，无法感知不同特征模式对编码代价的影响。
2. **熵建模沦为后验统计**：熵模型只能被动拟合已生成的量化表示分布，而无法主动引导编码器学习更紧凑、更可压缩的潜在表示，导致索引分布中保留大量冗余。

### 现有方法的局限

面对VQ的不可微困境，现有方法采取了多种规避策略，但均未从根本上解决问题：

- **启发式码本控制**：通过K-means聚类或均匀码本尺寸约束来控制码率，但这类方法缺乏对率失真联合目标的显式优化，导致表示效率低下——即使达到相同码率，感知质量也明显劣于端到端优化的方案。
- **两阶段训练**：先训练VQ-VAE获得离散表示，再单独训练熵模型，割裂了表示学习与率优化的内在关联。
- **依赖大规模预训练模型**：多数生成式压缩方法（如基于扩散模型的**PerCO**、**StableCodec**、**DDCM**等）依赖预训练的ViT或扩散先验，虽然提升了感知质量，但引入了巨大的参数量和计算开销，且未能解决VQ本身的率优化问题。

### 本文动机

上述分析揭示了一个清晰的改进空间：**能否在保留VQ高效离散表示能力的同时，恢复从率损失到编码器的梯度路径，从而实现真正的端到端联合率失真优化？**

RDVQ的核心动机正是回答这一问题。其关键洞察在于：**训练时解耦重建/编码路径与率优化路径**——在推理侧保持标准的硬量化流程不变，而在训练侧的率估计分支引入基于距离的可微软分布作为代理率目标。这一设计使得梯度 $\partial R_{soft} / \partial \mathbf{y} \neq 0$，让熵模型能够直接塑造编码器诱导的潜在分布，从而将标准VQ框架无缝扩展为可联合优化的RDVQ，且不改变部署时的推理管线。

## 核心方法与创新机理

RDVQ 的核心创新在于**为向量量化（VQ）框架恢复了从率损失到编码器的梯度路径**，从而首次在 VQ-based 生成式压缩中实现端到端的联合率失真优化。这一突破通过以下两个关键机制实现：

### 1. 可微松弛：从硬分配到软代理率目标

传统 VQ 压缩的根本瓶颈在于最近邻硬分配（argmin）的不可微性，导致率损失 $R = \mathbb{E}[- \log_2 q_{\psi}(\hat{\mathbf{y}})]$ 无法将梯度传回编码器，表示学习与熵建模形成事实上的解耦。RDVQ 的解决方案是**在率估计分支引入基于距离的可微软分布**，构建代理率目标，而**推理时的硬量化流程完全不变**。

具体而言，VQ 模块同时输出三条通路（Figure 2）：
- **硬量化嵌入** $\mathbf{y}_q$ 用于重建；
- **离散索引** $\mathbf{y}_{ind}$ 用于熵编码；
- **软分布** $p_{\mathrm{soft}}$ 仅用于训练时的率估计。

软分布通过距离-温度机制构建：
$$p_{\mathrm{soft}}(b,l,k) = \mathrm{softmax}_k\left(-\frac{\|\mathbf{y}_{b,l} - \mathcal{C}_k\|^2}{\tau}\right)$$

基于此，训练时的代理率损失定义为软分布与熵模型预测的交叉熵：
$$R_{\mathrm{soft}} = \mathbb{E}_{b,l}\left[-\sum_{k=1}^K p_{\mathrm{soft}}(b,l,k) \log q_{\psi}(b,l,k)\right]$$

由于 $\partial R_{\mathrm{soft}} / \partial \mathbf{y} \neq 0$，率目标得以直接塑造编码器诱导的潜在分布。**消融实验提供了决定性证据**：移除可微松弛后，即使在更高码率下（0.0247→0.0464 bpp），DISTS 仍从 0.1005 严重恶化至 0.2147（Table 1），证实可微索引分布是实现有效端到端 RD 优化的关键。

### 2. 自回归熵模型：精确率估计与测试时码率控制

与通常采用均匀先验或隐式先验的 VQ 方法不同，RDVQ 提出了**基于 masked Transformer 的自回归熵模型** $q_{\psi}$，在训练和推理中扮演双重角色：
- **训练时**：为可微软分布提供精确的码率估计，使率约束能够有效压缩索引分布中的冗余；
- **推理时**：支持通过前缀传输和自回归补全实现**无需重训练的测试时码率控制**。

该熵模型采用依赖感知的多尺度令牌排序策略（Figure 3）：在每个尺度内按空间位置分组排序，细尺度分区更精细以保留局部结构，跨尺度按粗到细排列，构建因果注意力掩码 $M = (o > o^{\intercal})$ 确保每个令牌仅关注有效前驱。

### 与启发式方案的本质区别

Table 1 的对比清晰揭示了联合 RD 优化的不可替代性：采用 K-means 聚类控制码本尺寸的启发式方案虽能匹配相同码率，但所有感知指标（DISTS、LPIPS、FID）均明显差于 RDVQ。这表明**仅靠码本容量约束无法有效消除索引分布中的统计冗余**，只有通过梯度驱动的联合优化才能使编码器学习到更可预测的特征表示和更高效的码本利用模式（Figure 8 进一步可视化验证了率约束下码本使用趋于集中）。

### 方法定位

RDVQ 的“可微松弛+自回归熵模型”组合本质上是一种**训练时解耦、推理时透明的代理优化策略**：软分布纯粹作为训练代理，不改变传统 VQ 编解码器的部署流程。这使得 RDVQ 能够以极轻量的架构（参数量不到多数现有方法的 20%，Figure 6）在极低码率下取得领先的感知质量，同时保持与标准 VQ 管线完全兼容的推理效率。

RDVQ 的核心设计在于将传统 VQ 压缩中的**硬重建/编码路径**与一个新增的**软率估计路径**解耦，从而在保持推理时标准硬量化流程不变的前提下，恢复从率损失到编码器的梯度通路，实现端到端的率失真联合优化。

### 双通路架构

如图 2 所示，RDVQ 的整体 pipeline 由四个主要模块串联构成：

1. **分析变换 $g_a$**：输入原始图像 $\mathbf{x}$，提取多尺度潜在特征 $\mathbf{y}$。多尺度设计使得模型能够在不同粒度上捕捉图像结构，为后续的向量量化和熵建模提供层次化表示。

2. **向量量化（VQ）模块**：这是 RDVQ 的核心创新所在。该模块以编码器特征 $\mathbf{y}$ 和共享码本 $\mathcal{C}$ 为输入，同时产出三路输出：
   - **硬量化嵌入 $\mathbf{y}_q$**：通过最近邻分配 $\mathbf{y}_{\text{ind}}(b,l) = \arg\min_k \|\mathbf{y}_{b,l} - \mathcal{C}_k\|^2$ 获得，用于下游的图像重建和最终的熵编码。
   - **离散索引 $\mathbf{y}_{\text{ind}}$**：码本索引序列，作为熵编码的符号流。
   - **软分布 $p_{\text{soft}}$**：基于编码器输出到各码本向量的平方欧氏距离 $d_{b,l,k} = \|\mathbf{y}_{b,l} - \mathcal{C}_k\|^2$，经温度 $\tau$ 缩放的 softmax 得到 $p_{\text{soft}}(b,l,k) = \mathrm{softmax}_k(-d_{b,l,k}/\tau)$。该分布仅在训练时用于率估计分支，**不参与**重建和熵编码。

3. **Masked Transformer 熵模型 $q_\psi$**：以软分布 $p_{\text{soft}}$ 为输入，通过自回归方式预测每个位置的条件概率 $q_\psi(b,l,k)$。该模块在训练时承担双重角色——提供准确的码率估计以计算代理率损失，同时在推理时支持通过前缀传输和自回归补全实现无需重训练的测试时码率控制。

4. **合成变换 $g_s$**：以硬量化嵌入 $\mathbf{y}_q$ 为输入，重建图像 $\hat{\mathbf{x}} = g_s(\mathbf{y}_q)$。

### 梯度流设计

RDVQ 的梯度流设计是其可端到端优化的关键。在硬量化路径（$\mathbf{y} \to \mathbf{y}_q \to \hat{\mathbf{x}}$）中，梯度通过 straight-through estimator 从重建损失反向传播至编码器，这与标准 VQ 一致。关键的差异在于率优化路径：软分布 $p_{\text{soft}}$ 对编码器输出 $\mathbf{y}$ 可微（$\partial p_{\text{soft}}/\partial \mathbf{y} \neq 0$），因此代理率损失 $R_{\text{soft}} = \mathbb{E}_{b,l}[-\sum_k p_{\text{soft}}(b,l,k) \log q_\psi(b,l,k)]$ 的梯度可以顺畅地流向编码器，使熵模型能够直接塑造编码器诱导的潜在分布。

### 训练与推理的一致性

值得强调的是，可微软分布 $p_{\text{soft}}$ **仅作为训练时的代理目标**。在推理阶段，模型完全遵循标准 VQ 编解码流程：编码器输出经硬量化得到索引序列，由熵模型进行算术编码传输，解码端通过码本查找和合成变换重建图像。这种设计保证了 RDVQ 在部署时与常规 VQ 编解码器完全兼容，无需额外的推理开销。

### 率失真联合优化目标

整体训练目标为标准的率失真拉格朗日函数 $\mathcal{L} = \lambda R + D(\mathbf{x}, \hat{\mathbf{x}})$，其中率项 $\mathcal{L}_R = \mathrm{CE}(p_{\text{soft}}, q_\psi)$ 采用软分布与熵模型预测的交叉熵，失真项 $\mathcal{L}_D$ 则由码本损失、MSE、LPIPS 和 GAN 损失加权组合构成。通过调节 $\lambda$，可以在不同码率区间实现灵活的率失真权衡。

![[assets/figures/papers/paper_list_l2051_https_arxiv_org_abs_2604_10546/figures/002_Figure_2.jpg]]
*Figure 2: Overview of RDVQ. The analysis transform*

### 率失真优化框架

RDVQ的训练目标遵循经典的率失真拉格朗日形式。令原始图像为 $\mathbf{x}$，重建图像为 $\hat{\mathbf{x}}$，量化潜变量为 $\hat{\mathbf{y}}$，整体损失函数定义为：

$$\mathcal{L} = \lambda R + D(\mathbf{x}, \hat{\mathbf{x}}) \tag{1}$$

其中率项 $R$ 衡量编码量化潜变量的期望比特数，失真项 $D$ 衡量重建图像与原始图像的感知差异。在VQ压缩框架下，期望编码率由熵模型 $q_{\psi}$ 对量化潜变量的负对数似然给出：

$$R = \mathbb{E}_{\hat{\mathbf{y}}} \left[ -\log_2 q_{\psi}(\hat{\mathbf{y}}) \right] \tag{2}$$

**核心瓶颈**在于：标准VQ中 $\hat{\mathbf{y}}$ 由最近邻硬分配产生，该操作不可微，导致 $\partial R / \partial \mathbf{y} = 0$，率损失的梯度无法回传至编码器，表示学习与熵建模完全脱耦。

### 向量量化模块的双通路设计

RDVQ的VQ模块同时服务于两条通路——硬重建/编码通路和软率估计通路，其统一输出为：

$$\mathbf{y}_q, \mathbf{y}_{ind}, p_{\mathrm{soft}} = \mathrm{VQ}(\mathbf{y}, \mathcal{C}) \tag{3}$$

其中 $\mathbf{y}$ 为分析变换 $g_a$ 提取的多尺度潜在特征，$\mathcal{C} = \{\mathcal{C}_k\}_{k=1}^K$ 为可学习码本。

**硬分配通路（重建与编码）**：对于每个空间位置 $(b,l)$ 的特征向量 $\mathbf{y}_{b,l}$，通过最近邻搜索确定离散索引：

$$\mathbf{y}_{ind}(b,l) = \arg\min_k \|\mathbf{y}_{b,l} - \mathcal{C}_k\|^2 \tag{4}$$

对应的硬量化嵌入 $\mathbf{y}_q$ 直接用于合成变换 $g_s$ 重建图像，离散索引 $\mathbf{y}_{ind}$ 用于熵编码。此通路在训练和推理中保持一致，保证解码端兼容标准VQ流程。

**软松弛通路（率估计）**：为恢复从率损失到编码器的梯度路径，RDVQ在率估计分支引入基于距离的可微松弛。首先计算 $\mathbf{y}_{b,l}$ 到每个码本向量的平方欧氏距离：

$$d_{b,l,k} = \|\mathbf{y}_{b,l} - \mathcal{C}_k\|^2 \tag{5}$$

然后通过温度参数 $\tau$ 控制的softmax构建可微软分布：

$$p_{\mathrm{soft}}(b,l,k) = \mathrm{softmax}_k\left(-\frac{d_{b,l,k}}{\tau}\right) \tag{6}$$

当 $\tau \to 0$ 时，$p_{\mathrm{soft}}$ 逼近硬分配的one-hot分布；训练时使用较大的 $\tau$ 保证梯度平滑。该软分布仅作为训练代理，**不改变推理时的硬量化流程**。

### 可微代理率目标

基于软分布 $p_{\mathrm{soft}}$ 和熵模型预测的条件概率 $q_{\psi}$，训练时的代理率损失定义为二者的交叉熵：

$$R_{\mathrm{soft}} = \mathbb{E}_{b,l}\left[-\sum_{k=1}^K p_{\mathrm{soft}}(b,l,k) \log q_{\psi}(b,l,k)\right] \tag{7}$$

由于 $p_{\mathrm{soft}}$ 对编码器输出 $\mathbf{y}$ 可微（$\partial p_{\mathrm{soft}} / \partial \mathbf{y} \neq 0$），率损失的梯度可以通过软分布传播至编码器，使熵模型能够直接塑造编码器诱导的潜在分布，实现端到端联合率失真优化。

### 自回归熵模型与依赖感知排序

熵模型 $q_{\psi}$ 采用基于masked Transformer的自回归架构，对离散索引序列进行概率建模。为构建有效的自回归依赖，RDVQ提出依赖感知的多尺度令牌排序策略：在每个尺度内按空间位置分组排序，细尺度划分更精细以保留局部结构，跨尺度按粗到细排列，形成统一的顺序向量 $\mathbf{o}$。因果注意力掩码定义为：

$$M = (\mathbf{o} > \mathbf{o}^{\intercal}) \tag{8}$$

该掩码确保每个令牌只能关注其在排序中的有效前驱，避免信息泄露。

多尺度tokenizer在 $256 \times 256$ 图像上的均匀编码理论上限为：

$$\mathfrak{bpp}_{\max} = \frac{(4^2 + 8^2 + 16^2) \cdot \log_2(4096)}{256^2} \approx 0.0615 \tag{9}$$

### 联合训练损失

RDVQ的最终训练损失联合优化失真项和率项：

$$\mathcal{L} = \mathcal{L}_D + \lambda \mathcal{L}_R \tag{11}$$

其中率损失定义为软分布与熵模型预测的交叉熵：

$$\mathcal{L}_R = \mathrm{CE}(p_{\mathrm{soft}}, q_{\psi}) \tag{12}$$

失真损失由多分量加权组合构成：

$$\mathcal{L}_D = \mathcal{L}_{\mathrm{codebook}} + \mathcal{L}_{\mathrm{MSE}} + \mathcal{L}_{\mathrm{LPIPS}} + 0.1 \mathcal{L}_{\mathrm{GAN}} \tag{13}$$

$\mathcal{L}_{\mathrm{codebook}}$ 为码本学习损失（commitment loss），$\mathcal{L}_{\mathrm{MSE}}$ 保证像素级保真度，$\mathcal{L}_{\mathrm{LPIPS}}$ 和 $\mathcal{L}_{\mathrm{GAN}}$ 提升感知质量。权重 $\lambda$ 控制率失真 trade-off，训练时采用分段策略在不同码率区间设置不同的 $\lambda$ 和温度 $\tau$ 以获得最优RD性能。

### 测试时码率控制

推理阶段，熵模型 $q_{\psi}$ 扮演双重角色：既用于算术编码/解码离散索引序列，也支持通过前缀传输实现无重训练的测试时码率控制——仅传输索引序列的前缀部分，剩余索引由熵模型自回归预测补全。该机制的有效操作范围受限于训练分布内的前缀比例。

![[assets/figures/papers/paper_list_l2051_https_arxiv_org_abs_2604_10546/figures/010_Figure_9.jpg]]
*Figure 9: Test-time rate adjustment via prefix transmission. Left: Rate–distortion curves on Kodak. Right: Visual comparisons at similar bitrates (Bpp / DISTS). RDVQ-Adj maintains competitive performance with gradual degradation, while AE-Entropy and Zero-padding suffer from more noticeable artifacts*

![[assets/figures/papers/paper_list_l2051_https_arxiv_org_abs_2604_10546/figures/011_Figure_10.jpg]]
*Figure 10: PCA visualization of the largest-scale encoder features under different compression ratios. As the bitrate decreases, the features become progressively smoother, with high-frequency details suppressed*

## 实验与关键发现

### 主要结果：极低码率下的感知质量优势

RDVQ在Kodak、DIV2K-val和CLIC2020-test三个标准基准上，在极低码率设定下取得了领先的感知质量。图4的率失真曲线显示，RDVQ在DISTS和CLIPIQA两项感知指标上均达到最优水平。与同为VQ-标量混合架构的**RDEIC**相比，RDVQ在DIV2K-val上实现高达**75.71%**的DISTS比特率节省和**37.63%**的LPIPS比特率节省。在Kodak数据集上，表S1的BD-DISTS对比进一步表明，RDVQ在CGIC、Diffo、OneDC等VQ基线上一致取得最优。

值得注意的是，RDVQ仅使用GAN损失和LPIPS感知损失从头训练，未依赖任何大规模预训练模型（如扩散模型或ViT），而多数基线方法依赖此类预训练权重。尽管如此，图6的效率分析显示，RDVQ以**不到多数基线20%的参数量**取得了最佳BD-DISTS，同时保持有竞争力的推理延迟。这表明联合率失真优化带来的表示效率提升，远超单纯增加模型容量的收益。

### 消融实验：可微松弛的核心作用

表1的消融实验直接验证了本文核心设计——可微软分布——的必要性。移除可微松弛后（w/o Relaxation），模型即使在显著更高的码率下（0.0464 bpp vs. 0.0247 bpp），DISTS从0.1005急剧恶化至0.2147。这一结果确证：**可微索引分布是实现有效端到端率失真优化的关键**，单纯依靠硬分配的VQ训练无法让熵模型梯度塑造编码器表示。

另一关键消融对比了启发式码率控制方案。K-means VQ通过调整聚类中心数量来匹配RDVQ的码率，虽然达到了相同比特率，但所有感知指标（DISTS、LPIPS、FID）均明显更差。这说明联合RD学习消除的索引分布冗余，无法通过简单的码本尺寸控制来弥补——率损失通过梯度直接压缩了编码器输出的熵，而非仅限制码本容量。

### 测试时码率控制与可调性

RDVQ的自回归熵模型赋予了无需重训练的测试时码率调整能力。通过仅传输离散索引序列的前缀部分，并利用熵模型自回归预测剩余索引，RDVQ-Adj在0.02–0.32 bpp范围内保持了沿RD曲线的渐进退化（图9左）。与AE-Entropy和Zero-padding两种替代方案相比，RDVQ-Adj在相似码率下重建图像结构更清晰、伪影更少（图9右）。

但这一能力存在明确边界：超出训练分布的前缀比例会导致质量显著下降。这是自回归模型在分布外条件下的固有限制，当前方案未提供动态超出训练范围的码率扩展机制。

### 表示学习与码本利用分析

联合RD优化对编码器特征产生了可观测的结构性影响。图10展示了不同压缩率下最大尺度编码器特征的PCA可视化：随着码率降低，特征逐渐平滑，高频细节被系统性抑制。这表明率损失不仅压缩了索引分布的熵，还通过梯度路径重塑了编码器输出的空间特性，使其更易于熵模型预测。

码本利用方面（图8），更强的率约束使码本使用更集中——高概率码本条目被更频繁激活，而低概率条目逐渐被弃用。这与交叉熵率损失的内在机制一致：最小化$-\\sum p_{\\text{soft}} \\log q_\\psi$ 等价于驱使$q_\\psi$向低熵分布收敛，从而减少编码索引所需的比特数。

### 训练策略的影响

补充实验揭示了两个对性能有显著影响的训练策略。首先，分段调整温度参数$\\tau$和率权重$\\lambda$的策略在极低码率下优于固定锐利松弛（图S2），这是因为不同码率区间对软分布的锐度要求不同——过低码率时过于锐利的松弛会削弱梯度信号。其次，从ImageNet到OpenImage再到DF2K的高分辨率逐步微调策略显著提升了DIV2K重建质量（图S1），证明了跨分辨率适配对生成式压缩泛化的重要性。

![[assets/figures/papers/paper_list_l2051_https_arxiv_org_abs_2604_10546/figures/009_Table_1.jpg]]
*Table 1: Quantitative comparison of ablation variants on DIV2Kval. Lower DISTS, LPIPS, FID indicate better perceptual quality*

![[assets/figures/papers/paper_list_l2051_https_arxiv_org_abs_2604_10546/figures/006_Figure_6.jpg]]
*Figure 6: Model efficiency comparison on DIV2K [1]. RDVQ achieves the best BD-DISTS with less than 20% of the parameters of most baselines, while maintaining competitive latency*

![[assets/figures/papers/paper_list_l2051_https_arxiv_org_abs_2604_10546/figures/014_Table_S.1.jpg]]
*Table S.1: Comparison with additional VQ-based methods on the Kodak dataset in terms of BD-DISTS. Lower is better*

## 定位与知识库关联

### 1. 与现有方法的关系

RDVQ 处于**生成式图像压缩（GIC）**与**向量量化（VQ）**两条技术路线的交汇点，其核心贡献在于解决了 VQ 框架中“硬分配不可微导致率失真（R-D）无法端到端联合优化”这一根本瓶颈。理解 RDVQ 的定位需要分别考察其与标量量化（SQ）路线、VQ 路线以及传统编解码器的关系。

#### 1.1 相对于标量量化（SQ）生成式压缩

基于 SQ 的生成式压缩方法（如 **MS-ILLM**、**ResULIC**）通常在潜在空间使用均匀量化或加性噪声松弛，天然保持可微性，因此可以直接使用熵瓶颈进行端到端 R-D 优化。这类方法的优势在于训练流程简洁，但其潜在表示受限于标量量化的表达能力。RDVQ 选择 VQ 路线的动机在于：向量量化通过码本学习能够捕获更结构化的离散表示，天然适合自回归熵建模和生成式解码。然而，VQ 的硬分配不可微问题长期阻碍了其与熵模型的联合优化——这正是 RDVQ 试图填补的空白。

#### 1.2 相对于 VQ 路线生成式压缩

在 VQ-based GIC 方法中，已有工作从不同角度尝试利用 VQ 的离散表示优势：

- **解码端扩散/一步生成**：**DDCM**、**Diffo** 等方法在解码端使用扩散模型从 VQ 索引重建图像，但编码端通常依赖固定的 VQ 编码器，缺乏对编码表示的率约束优化。**OSCAR**、**OneDC** 等一步生成方法同样侧重于解码端的生成质量提升，率控制依赖于启发式的码本尺寸或索引选择策略（如 **CGIC** 的选择性传输），而非通过梯度优化编码器来塑造潜在分布。
- **SQ-VQ 混合方案**：**DLF**、**RDEIC** 等方法结合了 SQ 和 VQ 的表示，试图平衡两种量化的优势。RDVQ 与 **RDEIC** 的直接对比（DIV2K-val 上 bitrate 降低最高 75.71% on DISTS）表明，纯 VQ 框架在获得有效的 R-D 联合优化后，可以在极低码率下实现更高的表示效率。

RDVQ 与上述 VQ 方法的本质区别在于：**它将率优化从“启发式后处理”升级为“端到端梯度驱动”**。通过在训练时解耦重建路径（硬量化）与率估计路径（可微软分布），RDVQ 在不改变推理流程的前提下，使熵模型能够直接塑造编码器诱导的潜在分布。

#### 1.3 相对于传统编解码器

与 **VVC**（Bross et al., IEEE TCSVT 2021）等传统编解码器相比，RDVQ 属于生成式压缩范式，其优化目标从像素级保真度转向感知质量（DISTS、LPIPS、CLIPIQA 等指标）。在极低码率下，RDVQ 的感知质量显著优于 VVC，但这是生成式压缩的共性优势，而非 RDVQ 独有的突破。

### 2. 方法适用边界

RDVQ 的设计在以下范围内经过验证，超出这些边界时性能可能退化或缺乏保证：

1. **码率范围**：RDVQ 针对**极低码率**场景设计，多尺度 tokenizer 的均匀编码上限约为 0.0615 bpp（256×256 图像）。在该范围内，RDVQ 通过调整 λ 权重和温度 τ 实现了有效的 R-D 控制。但在更低码率下，受限于下采样因子和码本容量（4096），表示能力存在硬性下限。
2. **分辨率范围**：实验验证集中在 Kodak（768×512）、DIV2K（2K）和 CLIC2020 测试集。对于超过 2K 分辨率的图像，多尺度 tokenizer 的内存和计算效率尚未验证，可能存在实际瓶颈。
3. **训练范式**：RDVQ 采用三阶段训练流程，且码本在初始化后保持固定。这种设计限制了不同阶段对码本的自适应调整自由度，可能无法充分挖掘端到端学习的全部潜力。
4. **测试时码率控制**：前缀传输策略（RDVQ-Adj）的有效操作范围有限（约 0.02–0.32 bpp），超出训练分布的前缀比例可能导致自回归补全质量显著下降。

### 3. 局限与开放问题

#### 3.1 已验证的局限性

- **可微松弛的必要性**：消融实验（Table 1）直接证实，移除可微软分布后，即使在更高码率下性能也急剧恶化（DISTS: 0.1005→0.2147, bpp: 0.0247→0.0464），表明可微索引分布是有效端到端 R-D 优化的关键组件，而非可选的辅助技巧。
- **启发式控制的不足**：K-means VQ 通过控制码本簇尺寸匹配码率，但所有感知指标均明显差于联合 R-D 学习（Table 1），证明启发式控制无法有效消除索引分布中的统计冗余。
- **调参复杂度**：需要分段设置温度 τ 和权重 λ 才能在不同码率区间获得最优 R-D 性能（Fig. S2），增加了实际部署中的调参负担。

#### 3.2 开放研究问题

1. **可微松弛的跨领域推广**：可微软分布方案本质上是一种针对离散潜变量的代理梯度方法。该技术能否推广到文本 tokenization、语音编码等其他离散潜变量模型，实现统一的率失真优化框架？
2. **自适应温控与码本管理**：是否可以通过学习动态温度或自适应码本剪枝来取代手工分段策略，实现全程平滑的率控制？这需要解决温度与码本利用之间的耦合关系。
3. **自回归熵模型的增强**：当前的依赖感知排序（Figure 3）基于固定的粗到细尺度顺序。能否引入上下文感知或后验校正方法，提升前缀补全质量并扩大有效比特率操作范围？
4. **与预训练基础模型的协同**：RDVQ 以不到多数基线 20% 的参数量（Figure 6）取得了领先的感知质量，且仅使用 GAN 和 LPIPS 损失从零训练。在与大规模预训练模型（如 ViT、扩散模型）结合时，轻量的 VQ-熵架构能否提供互补增益，避免冗余参数？
5. **下游任务性能评估**：当前评估聚焦于感知质量指标（DISTS, LPIPS, CLIPIQA, FID），缺乏对检测、分割等下游任务性能的系统评估。生成式压缩在感知质量与任务性能之间可能存在鸿沟，需要建立更全面的评估体系。

## 原文 PDF

![[paperPDFs/CVPR_2026/Differentiable_Vector_Quantization_for_Rate_Distortion_Optimization_of_Generative_Image_Compression.pdf]]
