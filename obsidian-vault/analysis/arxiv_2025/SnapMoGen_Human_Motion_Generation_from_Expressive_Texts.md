---
title: "SnapMoGen: Human Motion Generation from Expressive Texts"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/SnapMoGen_Human_Motion_Generation_from_Expressive_Texts.pdf
aliases:
- SnapMoGen
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 多尺度残差量化（共享码本）结合单一生成式掩码变换器，所有运动标记由统一模型生成，显著提升了标记容量利用率和生成可控性。
primary_logic: 通过在不同时间尺度上执行残差向量量化并共享码本，以更少的标记实现更高质量的运动重建，同时简化文本到标记的生成过程。
claims:
- 多尺度 RVQ 仅用 266 个 token 即超越传统 6 层全尺度 RVQ 的 480 token 重建质量，标记减少约 45%。
- MoMask++ 在 HumanML3D 和 SnapMoGen 基准上均取得最优性能（FID、R Precision、CLIP Score 等关键指标）。
- 共享码本和单一掩码变换器使文本到标记的生成更为统一和高效，避免了先前方法的双模型不灵活性问题。
- HumanML3D test set 上 FID↓ = 2.948 (cross-attention) / 2.912 (in-context)
---

# SnapMoGen: Human Motion Generation from Expressive Texts

> [!tip] 核心洞察
> 通过在不同时间尺度上执行残差向量量化并共享码本，以更少的标记实现更高质量的运动重建，同时简化文本到标记的生成过程。

| 字段 | 内容 |
|------|------|
| 中文题名 | SnapMoGen：基于表达性文本的人体运动生成 |
| 英文题名 | SnapMoGen: Human Motion Generation from Expressive Texts |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2507.09122) · [Project](https://snap-research.github.io/SnapMoGen/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MoMask++ |
| Dataset | HumanML3D test set, SnapMoGen test set |

> [!tip] 效果简介
> - HumanML3D test set 上，FID↓ 2.948 (cross-attention) / 2.912 (in-context) vs 见原文 Table 2（多种基线） (优于所有参与比较的方法)；R Precision Top1↑ 0.528 (in-context) vs 见原文 Table 2 (最优)；MM Dist↓ 2.912 (in-context) vs 见原文 Table 2 (最优)。
> - SnapMoGen test set 上，FID↓ 15.06 (cross-attention) vs 见原文 Table 3 (显著优于其他方法)；CLIP Score↑ 0.685 (cross-attention) vs 见原文 Table 3 (显著优于其他方法)；R Precision Top1↑ 0.805 (in-context) vs 见原文 Table 3 (最优)。

## 概述

**问题瓶颈**：现有文本-运动生成模型受限于数据集中简短、通用的文本描述，缺乏表达性与细粒度控制能力。同时，传统全尺度残差向量量化（RVQ）在运动标记化中标记容量利用率低下，冗余标记过多，制约了生成质量与效率。

**核心方法**：本文提出 **MoMask++**，一种基于多尺度残差向量量化与单一生成式掩码变换器的文本-运动生成框架。其关键创新在于：在不同时间尺度上执行残差向量量化，并在所有量化层间共享单一码本，从而以更少的标记实现更高质量的运动重建；同时，使用统一的掩码变换器直接生成全部尺度的运动标记，取代以往双模型架构，简化了文本到标记的生成流程。

**主要结果**：
- 多尺度 RVQ 仅用 266 个 token 即超越传统 6 层全尺度 RVQ 的 480 token 重建质量，标记数量减少约 45%（Fig. 3）。
- 在 HumanML3D 测试集上，MoMask++ 在 FID、R Precision、MM Dist 等关键指标上均取得最优性能（Table 2）。
- 在 SnapMoGen 测试集上，该方法在 FID（15.06）、CLIP Score（0.685）和 R Precision Top1（0.805）上显著优于所有参与比较的方法（Table 3）。

**方法定位**：MoMask++ 属于基于离散标记的生成式运动合成方法，在量化策略上从传统的各层独立码本全尺度 RVQ 演进为共享码本的多尺度 RVQ，在生成架构上从双掩码变换器简化为单一统一模型。其技术路线区别于扩散模型（如 MDM、StableMoFusion）和自回归模型（如 T2M-GPT），在标记效率与生成可控性之间取得了新的平衡。

## 背景与动机

**核心瓶颈：文本-运动数据集的表达性匮乏。** 现有公开数据集（如 HumanML3D、KIT-ML）的文本标注普遍简短且泛化，平均长度仅为 8–12 个单词，描述粒度停留在“一个人向前走”或“坐下”等粗粒度动作类别。这种标注风格导致两个连锁问题：其一，训练出的生成模型难以解析包含时序细节、动作风格、情感色彩等丰富语义的复杂提示；其二，评估指标本身无法有效区分模型对细粒度语义的捕捉能力。**SnapMoGen** 数据集正是针对这一瓶颈而构建——其每条运动片段配有 6 条独立文本标注，人工标注平均长度为 48 词，并额外引入 LLM 增强标注（Table 1），使文本覆盖从动作类型、身体部位运动轨迹到节奏与情感的全方位描述。

**生成架构的效率困境。** 在方法层面，以 **MoMask**（Guo et al., 2024）为代表的残差量化（RVQ）方案虽在 HumanML3D 上取得领先性能，但其“全尺度量化 + 独立码本 + 双生成模型”的设计存在冗余：6 层 RVQ 需 480 个 token 表示一段运动，且各层码本互不共享，导致 token 容量利用率低下（Fig. 3 直观展示了大量 token 仅编码噪声级残差）；同时，主/次两个掩码变换器的分离式生成破坏了文本到运动标记的统一映射，限制了可控性的上限。

**本文动机：以更少 token 实现更强可控。** SnapMoGen 工作的核心假设是——**若能在量化阶段用更紧凑的离散表示捕获运动的多尺度结构，并在生成阶段用单一模型统一处理所有尺度标记，则生成质量与文本跟随能力可同时提升。** 这一假设的因果杠杆在于“多尺度残差量化 + 共享码本”：通过在不同时间下采样率上执行 RVQ 并共享同一码本，MoMask++ 仅用 266 个 token（较 MoMask 减少约 45%）即实现了更优的重建质量（Table 4），进而使下游的单一掩码变换器能更高效地学习从文本到运动的映射，最终在 HumanML3D 和 SnapMoGen 双基准上取得最优 FID 与 R Precision（Table 2, Table 3）。

## 核心创新

MoMask++ 的核心创新在于对运动标记化范式的根本性重构：**用单一共享码本的多尺度残差量化替代传统各层独立码本的全尺度残差量化，并将双模型生成架构统一为单一生成式掩码变换器**。这一设计直接回应了现有方法的两个结构性瓶颈——标记冗余与生成流程碎片化。

### 多尺度共享码本残差量化

传统运动 VQ-VAE 采用全尺度残差量化（RVQ），每一量化层在相同的完整时间分辨率上操作，且各层持有独立的码本。这导致两个问题：（1）深层码本被迫编码已在前层被大幅削减的残差信号，语义容量利用率低；（2）总标记数随层数线性增长（如 6 层 × 80 token/层 = 480 token），大量标记在生成阶段成为冗余负担。

MoMask++ 将量化操作分布到**逐层递增的时间分辨率**上：第 0 层在最粗粒度（$n/2^V$ 长度）量化，残差逐层向上传递并在更细粒度上被捕获，最终第 $V$ 层在全分辨率（$n/2^0$）完成量化。关键在于，**所有层共享同一个码本 $\mathcal{C}$**，这意味着不同尺度的运动模式被映射到统一的离散词汇表中，极大提升了每个码字的信息密度。

形式化地，给定编码器输出的潜特征序列 $f \in \mathbb{R}^{n \times d}$，多尺度残差量化的递推过程为：

$$q^v = \mathcal{Q}\left(\mathcal{Z}(r^v, h^v)\right), \quad r^{v+1} = r^v - \mathcal{Z}(\hat{f}^v, h^V), \quad r^0 = f$$

其中 $\mathcal{Z}(\cdot, h)$ 表示将序列下采样到时间尺度 $h$ 的算子，$\hat{f}^v = \mathsf{lookup}(\mathcal{C}, q^v)$ 为量化后的特征。最终的潜特征近似为所有尺度上采样后量化特征的求和：

$$\hat{f} = \sum_{v=0}^V \mathcal{Z}(\hat{f}^v, h^V), \quad \hat{\mathbf{m}} = \mathcal{D}(\hat{f})$$

**关键证据**：Figure 3 展示了传统 6 层全尺度 RVQ（480 token）与 10 层多尺度 RVQ（266 token）的标记容量对比。多尺度 VQ 仅用约 **45% 更少的标记**（266 vs 480）即实现了更优的运动重建质量，且各层标记展现出清晰的语义分层——粗尺度标记编码整体运动趋势，细尺度标记补充局部细节。Table 4 的消融实验进一步确认，多尺度 VQ 在重建指标（FID）和生成指标上均显著优于全尺度 VQ。

### 单一生成式掩码变换器

MoMask 及其前身方法通常采用**双模型架构**：一个主生成模型负责预测粗粒度标记，另一个次模型以粗标记为条件生成细粒度标记。这种设计引入了额外的模型复杂度，且两个模型之间的协调需要精心设计的训练策略。

MoMask++ 将所有尺度的标记序列按时间维度拼接为一个统一序列，由**单一的生成式掩码变换器**直接处理。文本条件通过 T5-base 编码器提取词级特征后，以两种可选方式注入：（1）**上下文学习**（in-context learning），将文本标记置于运动标记序列前端；（2）**交叉注意力**（cross-attention），在变换器各层中通过交叉注意力机制融合文本特征。

训练目标为标准掩码标记预测损失：

$$\mathcal{L}_{\text{mask}} = \sum_{\dot{q}_k = [\mathsf{MASK}]} -\log p_{\theta}(q_k \mid \dot{q}, c)$$

其中 $\dot{q}$ 为被部分掩码的标记序列，$c$ 为文本条件。推理时采用迭代解码策略，配合置信度调度和分类器自由引导（classifier-free guidance）逐步填充所有被掩码标记。

**关键证据**：Table 2 和 Table 3 显示，MoMask++ 在 HumanML3D 和 SnapMoGen 两个基准上均取得最优性能。在更具挑战性的 SnapMoGen 测试集上，交叉注意力变体在 FID（15.06）和 CLIP Score（0.685）上显著领先所有基线；上下文学习变体则在 R Precision Top1（0.805）上达到最优。Table 5 的消融实验确认，交叉注意力条件方式在长文本提示上比上下文学习具有更好的泛化性（见图 6 的验证损失曲线对比）。

### 创新总结

| 变更维度 | 基线方法（MoMask 等） | MoMask++ |
|---------|---------------------|----------|
| 量化方式 | 全尺度残差量化，各层独立码本 | 多尺度残差量化，共享单一码本 |
| 标记效率 | 480 token（6 层） | 266 token（10 层），减少约 45% |
| 生成架构 | 两个独立掩码变换器 | 单一掩码变换器处理全部尺度标记 |
| 标记组织 | 分层独立序列 | 按时间维度拼接为统一序列 |

这两项创新相互协同：共享码本的多尺度量化提供了紧凑且语义丰富的标记表示，单一变换器则消除了双模型架构的不灵活性和训练复杂度，使文本到运动的生成过程更为统一高效。

## 整体框架

MoMask++ 遵循“运动标记化 → 文本条件生成 → 运动重建”的两阶段范式，但在标记化与生成两个核心环节进行了结构化改造，形成了一条更紧凑、标记效率更高的流水线。

**阶段一：多尺度运动 VQ-VAE。** 给定一段长度为 $N$ 的 3D 人体姿态序列 $\mathbf{m}_{1:N} \in \mathbb{R}^{N \times D}$（$D$ 为单帧姿态维度），运动编码器 $\mathcal{E}$ 首先将其压缩为长度为 $n$ 的潜特征序列 $f \in \mathbb{R}^{n \times d}$。随后，多尺度残差量化模块（Multi-scale RVQ）对该潜特征执行 $V+1$ 层残差量化，各层的时间分辨率按 $[n/2^V, \dots, n/2^0]$ 递减，所有层共享同一个码本 $\mathcal{C}$。第 $v$ 层的量化过程可形式化为：

$$q^v = \mathcal{Q}\big(\mathcal{Z}(r^v, h^v)\big), \quad r^{v+1} = r^v - \mathcal{Z}(\hat{f}^v, h^V), \quad r^0 = f$$

其中 $\mathcal{Z}(\cdot, h)$ 表示按尺度 $h$ 进行下采样或上采样，$\hat{f}^v = \text{lookup}(\mathcal{C}, q^v)$ 为量化后的特征。最终潜特征近似为所有尺度量化特征上采样后的和：$\hat{f} = \sum_{v=0}^V \mathcal{Z}(\hat{f}^v, h^V)$，经解码器 $\mathcal{D}$ 重建出运动 $\hat{\mathbf{m}} = \mathcal{D}(\hat{f})$。相比传统各层独立码本的全尺度 RVQ（如 MoMask 所用），该设计仅用约 266 个 token 即可超越 480 token 的重建质量（token 减少约 45%），且共享码本赋予了 token 跨尺度的语义一致性。

**阶段二：统一掩码生成式变换器。** 文本编码器（T5-base）从文本描述 $c$ 中提取词级特征。所有尺度的运动 token 序列沿时间维度拼接为一个统一序列，送入单一生成式掩码变换器。与 MoMask 需双变换器（主模型与次模型）分别处理不同尺度 token 不同，MoMask++ 的单一变换器直接建模全部 token 的联合分布。训练时，按余弦调度随机掩码部分 token，以掩码预测损失优化：

$$\mathcal{L}_{\text{mask}} = \sum_{\dot{q}_k = [\mathsf{MASK}]} -\log p_{\theta}(q_k \mid \dot{q}, c)$$

推理时，迭代解码器从全掩码序列出发，结合置信度调度与分类器自由引导（CFG），逐步填充所有尺度的 token。文本条件注入支持两种模式：上下文学习（in-context）将文本 token 直接拼入序列，交叉注意力（cross-attention）则在变换器层中引入文本特征。最终，完整的 token 序列经阶段一的解码器重建为运动序列。

**流水线优势。** 三个关键改造共同构成因果杠杆——多尺度共享码本大幅压缩 token 数量并提升容量利用率，统一掩码变换器消除了双模型的不灵活性与冗余，文本条件与迭代解码则保障了从表达性文本到细粒度运动的可控映射。该框架在 HumanML3D 与 SnapMoGen 双基准上均取得最优 FID、R Precision 与 CLIP Score（详见 Table 2、Table 3），验证了设计的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2507_09122/figures/003_Figure_2.jpg]]
*Figure 2: Approach overview. (a) A multi-scale VQVAE encodes a motion sequence into V + 1 discrete token sequences*

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2507_09122/figures/013_Figure_8.jpg]]
*Figure 8: Architecture of the evaluation model [26]. Three network components are trained with two main goals: multimodal alignment and reconstruction. The cosine similarity between motion embeddings and text embeddings from positive pairs (green) is maximized, while similarity for negative pairs is minimized. Meanwhile, both embeddings are required to reconstruct the corresponding motion sequence through the motion decoder. Image adapted from TMR [26]*

## 核心模块与公式推导

### 运动 VQ-VAE 基础框架

传统运动 VQ-VAE 将运动序列 $\mathbf{m} \in \mathbb{R}^{N \times D}$ 编码为潜特征序列 $f \in \mathbb{R}^{n \times d}$，再通过向量量化映射为离散标记序列。核心操作为最近邻查找：

$$q_i = \left( \mathbf{argmin}_{k \in [K]} \| \mathsf{lookup}( \mathscr{C}, k) - f_i \|_2 \right) \in [K] \tag{1}$$

其中 $\mathscr{C}$ 为码本，$K$ 为码本大小。量化特征通过查表重建，并输入解码器恢复运动：

$$\hat{f} = \mathsf{lookup}(\mathcal{C}, q), \quad \hat{\mathbf{m}} = \mathcal{D}(\hat{f}) \tag{2}$$

传统残差量化（RVQ）逐层执行上述过程，每层拥有独立码本 $\mathcal{C}^v$，残差传递公式为：

$$q^v = \mathcal{Q}^v(r^v), \quad \hat{f}^v = \mathsf{lookup}(\mathcal{C}^v, q^v), \quad r^{v+1} = r^v - \hat{f}^v \tag{3}$$

RVQ 训练损失结合运动重建与嵌入对齐：

$$\mathcal{L}_{rvq} = \mathtt{SmoothL1}(\mathbf{m} - \hat{\mathbf{m}}) + \beta \sum_{v=0}^V \| r^v - \mathbf{sg}[\hat{f}^v] \|_2 \tag{4}$$

### MoMask++ 的多尺度残差量化

MoMask++ 的核心创新在于将传统全尺度 RVQ 改造为**多尺度残差量化**，并**在所有量化层间共享单一码本**。具体而言，量化器在逐步增加的时间分辨率上执行残差量化操作。设 $\mathcal{Z}(x, h)$ 为将特征 $x$ 下采样至时间尺度 $h$ 的算子，则第 $v$ 层的量化过程为：

$$q^v = \mathcal{Q}(\mathcal{Z}(r^v, h^v)), \quad r^{v+1} = r^v - \mathcal{Z}(\hat{f}^v, h^V), \quad r^0 = f \tag{5}$$

其中时间尺度按 $[n/2^V, ..., n/2^0]$ 递增。最终潜特征近似为所有上插值量化序列之和：

$$\hat{f} = \sum_{v=0}^V \mathcal{Z}(\hat{f}^v, h^V), \quad \hat{\mathbf{m}} = \mathcal{D}(\hat{f})$$

多尺度 VQ 的训练目标在 $\mathcal{L}_{rvq}$ 基础上增加对必要旋转特征的加权重建项：

$$\mathcal{L}_{ms\_rvq} = \mathcal{L}_{rvq} + \lambda_{ess} \mathcal{L}_{ess} \tag{6}$$

### 掩码生成式变换器

MoMask++ 使用**单一生成式掩码变换器**处理所有尺度的运动标记，替代 MoMask 的双模型架构。文本条件通过 T5-base 编码器提取词级特征 $c$。训练时，按余弦调度 $\gamma(\tau) = \cos(\pi\tau/2)$ 随机掩码部分标记，损失函数为：

$$\mathcal{L}_{mask} = \sum_{\dot{q}_k = [\mathsf{MASK}]} -\log p_{\theta}(q_k \mid \dot{q}, c) \tag{7}$$

其中 $\dot{q}$ 为部分掩码的标记序列，$p_{\theta}$ 为变换器预测分布。推理阶段采用迭代解码，通过置信度调度逐步填充全部标记，并可结合分类器自由引导提升生成质量。

### 关键公式变量说明

| 符号 | 含义 |
|------|------|
| $\mathbf{m}$ | 输入运动序列，维度 $N \times D$ |
| $f$ | 编码器输出的潜特征序列 |
| $\mathscr{C}$ / $\mathcal{C}$ | 向量量化码本 |
| $q^v$ | 第 $v$ 层的离散标记索引序列 |
| $r^v$ | 第 $v$ 层量化前的残差特征 |
| $\mathcal{Z}(\cdot, h)$ | 时间尺度 $h$ 的下采样/上插值算子 |
| $\hat{\mathbf{m}}$ | 解码器重建的运动序列 |
| $c$ | T5-base 文本编码器输出的条件特征 |
| $\mathbf{sg}[\cdot]$ | 停止梯度算子 |

### 补充图表

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2507_09122/figures/004_Figure_3.jpg]]
*Figure 3: Illustration of token capacity in a pretrained traditional 6-layer, 480-token full-scale RVQ [9] compared to a 10-layer, 266-token multi-scale*

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2507_09122/figures/010_Figure_5.jpg]]
*Figure 5: Decoding progress over iterations for different token scales*

## 实验与分析

### 主实验结果

MoMask++ 在两个基准上均取得最优性能。在 **HumanML3D** 测试集上，in-context 变体在 R Precision Top1（0.528）、Top2（0.718）、Top3（0.811）及 MM Dist（2.912）上全面领先，cross-attention 变体则获得最优 FID（2.948），详情见 **Table 2**。在 **SnapMoGen** 测试集上，cross-attention 变体以 FID 15.06 和 CLIP Score 0.685 显著优于所有基线；in-context 变体在 R Precision Top1（0.805±.002）上取得最佳，见 **Table 3**。所有基线模型均使用统一 T5-base 文本编码器在 SnapMoGen 上重新训练，评价采用 TMR 框架，确保可比性。

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2507_09122/figures/005_Table_2.jpg]]
*Table 2: Quantitative evaluation on HumanML3D test set. ± indicates a 95% confidence interval. Bold indicates the best result, while underscore refers to the second best*

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2507_09122/figures/006_Table_3.jpg]]
*Table 3: Quantitative evaluation on SnapMoGen test set*

**Figure 4** 展示了 MoMask++ 对测试提示和用户随意提示的生成样本，定性反映出对复杂文本的良好响应能力。

### 消融分析

**VQ 配置消融**（**Table 4**）揭示以下因果链路：

- **多尺度 vs. 全尺度量化**：多尺度 RVQ 仅用 266 个 token（较传统 480 token 减少约 45%）即实现更优的重建质量，且生成指标全面超越全尺度 RVQ。这验证了共享码本与多时间尺度残差量化的标记效率优势。
- **量化层数**：增加层数持续改善重建，但生成任务以 2 层为最佳——更多层反而导致文本-运动对齐下降，表明过量的标记容量可能引入生成噪声。
- **紧凑姿态表示**：仅保留 148 维本质旋转特征略微降低文本-运动生成性能，但减小了 VQ 重建误差，说明精简表示对压缩有利，但对语义建模有一定信息损失。

**生成模型配置消融**（**Table 5**）关键发现：

- **描述增强**：使用 LLM 对文本进行语法修正和语义保留改写后，所有评估指标均有提升，证实表达性文本对生成质量的正向因果作用。
- **文本条件方式**：cross-attention 条件相比 in-context 学习在运动质量和文本对齐上更优，尤其对长文本提示。**Figure 6** 的验证损失曲线显示，in-context 模型在 SnapMoGen 长文本上出现明显过拟合，而 cross-attention 模型泛化更稳定。
- **模型架构**：增大 Transformer 参数量（潜维度、前馈尺寸、层数）可提升性能，但需与文本条件方式协同选择以避免过拟合。

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2507_09122/figures/011_Figure_6.jpg]]
*Figure 6: Validation loss curves of different model sizes on SnapMoGen*

### 失败模式与局限性

尽管 MoMask++ 在基准上表现领先，仍存在以下可辨识的失败模式：

1. **量化误差导致的运动退化**：VQ 重建并非无损，对罕见运动模式（如后空翻、攀爬）和不常见文本提示，量化误差在生成中被放大，导致动作失真或与文本不匹配。
2. **物理合理性缺失**：模型未显式建模脚部着地、平衡等物理约束，生成的快速动作可能出现滑步或漂浮现象。惯性动捕数据本身的全局位置精度不足和抖动进一步加剧了此问题。
3. **长文本泛化瓶颈**：in-context 模型在长文本提示上过拟合（**Figure 6**），cross-attention 虽更鲁棒，但增大模型尺寸后同样面临泛化与容量的权衡。
4. **数据覆盖局限**：SnapMoGen 数据集因动捕设备限制，缺少高技巧动作和户外活动，模型在这些场景下的生成能力未经验证。

### 重要图表结论

- **Table 2 / Table 3**：MoMask++ 在两个基准上全面超越 MDM、T2M-GPT、StableMoFusion、MARDM 及 MoMask 等基线，验证多尺度共享码本量化与单一掩码变换器的有效性。
- **Figure 3**：直观展示多尺度 RVQ 的标记容量优势——以更少 token 学习更有语义意义的表示，各量化层对应不同时间粒度的运动结构。
- **Table 4**：量化层数与生成性能呈倒 U 型关系，2 层为最优，揭示标记容量与生成可控性之间的权衡。
- **Table 5**：描述增强和 cross-attention 条件各自独立且叠加地提升性能，为文本-运动生成系统的设计提供明确方向。
- **Figure 6**：验证损失曲线直接暴露 in-context 模型在长文本上的过拟合风险，为条件方式选择提供经验依据。

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2507_09122/figures/009_Table_5.jpg]]
*Table 5: Ablation analysis of T2M model configuration on SnapMoGen test set. "Architecture" refers to transformer hyperparameters including latent dimension, feedforward size, and number of layers. This experiment use 2 quantization layers for VQ, with 2048 codebook size and 296 pose features*

### 补充图表

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2507_09122/figures/008_Figure_4.jpg]]
*Figure 4: MoMask++ generated samples for SnapMoGen test prompts (#1,2) and a casual user prompt (#3)*

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2507_09122/figures/002_Table_1.jpg]]
*Table 1: Comparisons with public datasets. SnapMoGen highlights its accurate and expressive text descriptions, high-quality motion capture data, and continuous motion segmentation. † indicates values calculated only from the publicly available BABEL subset. ∗ denotes a combination of 40,859 manual text annotations and 81,706 LLM-augmented annotations, both with an average text length of 48 words*

## 方法谱系与知识库定位

### 1. 基线方法谱系

MoMask++ 的直接前身是 **MoMask**（Guo et al., 2024），两者共享生成式掩码变换器的核心范式。MoMask++ 的关键改造在于将 MoMask 的双模型架构（主模型与次模型分别处理不同层级标记）统一为**单一生成式掩码变换器**，并将各层独立码本的全尺度残差量化替换为**共享码本的多尺度残差量化**。这一变化使得标记总量从 480 个降至 266 个（减少约 45%），同时提升了标记容量的语义利用效率（Fig. 3）。

在更广泛的方法谱系中，文本驱动运动生成的主流路线包括：

- **扩散模型路线**：**MDM**（Tevet et al., arXiv 2022）直接在运动空间预测噪声；**StableMoFusion**（Han et al., 2024）采用 Conv1D U-Net 架构进行扩散生成。这类方法的优势在于生成多样性，但推理速度较慢，且对文本条件的细粒度控制不如离散标记方法直观。

- **自回归离散标记路线**：**T2M-GPT**（Zhang et al., 2023）将运动量化为离散标记后，以自回归方式逐标记生成。该方法生成质量高，但自回归解码的串行特性限制了推理效率。

- **掩码生成路线**：**MARDM**（Meng et al., 2024）采用掩码自回归变换器；**MoMask** 及本工作的 **MoMask++** 则采用双向掩码生成式变换器，通过迭代式掩码预测与置信度调度实现并行解码，在推理速度与生成质量之间取得更好的平衡。

### 2. 核心创新定位

MoMask++ 的方法论贡献集中于两个因果性调控节点：

1. **多尺度残差量化 + 共享码本**：传统 RVQ 在每一层对全尺度特征进行残差量化，各层拥有独立码本，导致标记容量冗余且语义分散。MoMask++ 在不同时间尺度上执行残差量化（尺度序列为 $[n/2^V, ..., n/2^0]$），所有层共享单一码本 $\mathcal{C}$。这一设计强制码本学习跨尺度的通用运动原语，使得有限数量的标记能够更高效地覆盖运动空间。消融实验（Table 4）证实，多尺度 VQ 在重建质量上显著优于同标记量的全尺度 VQ，且生成任务中 2 层量化为最优配置。

2. **单一掩码变换器统一生成**：MoMask 需要两个独立变换器分别处理不同层级的标记，存在模型间协调的灵活性瓶颈。MoMask++ 将所有尺度的标记按时间维度拼接为统一序列，由单个掩码变换器一次性生成全部标记。文本条件通过交叉注意力或上下文学习两种方式注入（Fig. 2b-c）。消融实验（Table 5）表明，交叉注意力条件在长文本提示上优于上下文学习方法，后者在 SnapMoGen 数据集上出现过拟合倾向（Fig. 6）。

### 3. 适用边界

- **数据依赖**：MoMask++ 的性能高度依赖训练数据的文本表达性。SnapMoGen 数据集提供了平均 48 词的高表达性文本描述，这是模型在复杂提示下表现优异的前提。在文本简短、通用的传统数据集（如 HumanML3D）上，多尺度标记的优势仍然存在，但 CLIP Score 等文本对齐指标的提升空间受限。

- **运动类型覆盖**：受限于惯性动捕设备的采集能力，SnapMoGen 数据集缺乏高技巧动作（后空翻、攀登）和户外活动。MoMask++ 在此类未见运动模式上的泛化能力未经充分验证，VQ 量化误差可能进一步放大对稀有运动模式的生成退化。

- **物理合理性**：当前方法未显式建模物理约束（如脚部着地、质心平衡），生成的运动可能存在滑步、悬浮等物理不合理现象。这是离散标记生成路线的共性问题，扩散模型路线同样面临类似挑战。

### 4. 局限与开放问题

基于论文明确指出的局限性和实验揭示的瓶颈，以下问题构成该方向的后续研究空间：

1. **量化误差的进一步压缩**：尽管多尺度 RVQ 以更少标记实现了更优重建，但 VQ 量化误差仍是生成运动质量下降的根源，尤其影响手指细节和快速动作的还原精度。如何在不增加标记量的前提下进一步减小量化误差（如引入更紧致的码本学习策略或混合连续-离散表示）是一个关键开放问题。

2. **稀有模式与长尾文本的泛化**：当前模型对训练集中频繁出现的运动-文本模式拟合良好，但对稀有组合和不常见提示的处理能力不足。增大模型容量在长文本上反而出现过拟合（Fig. 6），提示需要在模型容量与泛化之间寻找更优的平衡策略。

3. **物理约束的嵌入**：将脚部接触、动力学平衡等物理约束显式嵌入生成流程，是提升运动物理合理性的必要方向。可能的路径包括在解码器中引入物理损失项，或在掩码预测迭代中施加运动学约束。

4. **多尺度标记的最优策略**：当前尺度序列采用固定的 $[n/2^V, ..., n/2^0]$ 等比划分，但不同运动类型可能受益于不同的尺度分配策略。自适应尺度选择及其对下游生成任务的影响值得深入探索。

5. **与扩散模型的融合潜力**：MoMask++ 的离散标记空间为结合扩散模型的去噪能力提供了接口——例如在标记空间而非运动空间进行扩散，可能兼具离散标记的高效性和扩散模型的多样性优势。这一方向尚未被探索。

**注**：以上开放问题部分基于论文明确讨论的局限性，部分源于实验数据中可观察到的性能缺口（如 SnapMoGen 上 FID 与真实运动之间仍存在显著差距），需结合后续工作进行验证。

## 原文 PDF

![[paperPDFs/arxiv_2025/SnapMoGen_Human_Motion_Generation_from_Expressive_Texts.pdf]]