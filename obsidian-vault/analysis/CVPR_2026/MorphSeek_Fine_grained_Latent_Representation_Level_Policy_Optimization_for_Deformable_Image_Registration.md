---
title: "MorphSeek: Fine-grained Latent Representation-Level Policy Optimization for Deformable Image Registration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MorphSeek_Fine_grained_Latent_Representation_Level_Policy_Optimization_for_Deformable_Image_Registration.pdf
project_link: null
code_link: null
aliases:
- MorphSeek
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将编码器顶部的高分辨率潜在特征参数化为可采样高斯策略，使强化学习在结构化潜在空间而非百万维变形场上进行探索和优化，并利用Latent-Dimension Variance Normalization (LDVN)稳定高维GRPO更新。
primary_logic: 通过无监督预热构建解剖保持的稳定潜在空间，再采用多轨迹、多步骤GRPO弱监督微调，将有限的标签在每个细化步中重复用于相对监督事件（每对产生T×J个监督信号），从而在极低参数开销下实现显著的标签效率和配准精度提升。
claims:
- MorphSeek在OASIS、LiTS、Abdomen MR←CT三个基准上，跨越三种骨干网络，均取得一致且显著的Dice提升和NJD降低。
- 增加轨迹数直到6条和增加细化步数直到3步带来持续增益，超过后饱和或导致变形伪影。
- MorphSeek仅需60%的标记数据即可达到98.5%的满标签性能，而基线TransMorph需要80%标签才能达到相似水平。
- 无监督预热将GRPO稳定训练的成功率从33%提升至79%，并加快收敛。
---

# MorphSeek: Fine-grained Latent Representation-Level Policy Optimization for Deformable Image Registration

> [!tip] 核心洞察
> 通过无监督预热构建解剖保持的稳定潜在空间，再采用多轨迹、多步骤GRPO弱监督微调，将有限的标签在每个细化步中重复用于相对监督事件（每对产生T×J个监督信号），从而在极低参数开销下实现显著的标签效率和配准精度提升。

| 字段 | 内容 |
|------|------|
| 中文题名 | MorphSeek：面向可变形图像配准的细粒度潜在表示级策略优化 |
| 英文题名 | MorphSeek: Fine-grained Latent Representation-Level Policy Optimization for Deformable Image Registration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.17392) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MorphSeek |
| Dataset | OASIS, LiTS, Abdomen MR←CT |

> [!tip] 效果简介
> - OASIS (Brain MRI) 上，Mean Dice (%) 88.9±1.8 (TransMorph+MorphSeek) vs 85.8±1.4 (TransMorph) (+3.1)。
> - LiTS (Liver CT) 上，Mean Dice (%) 90.5±3.7 (NICE-Trans+MorphSeek) vs 88.4±3.9 (NICE-Trans) (+2.1)。
> - Abdomen MR←CT 上，Mean Dice (%) 86.5±3.4 (TransMorph+MorphSeek) vs 82.3±4.8 (TransMorph) (+4.2)。

## 概述

可变形图像配准（Deformable Image Registration, DIR）的核心挑战在于从高维变形空间中恢复精确的局部对应关系。现有基于强化学习（RL）的DIR方法，如**SPAC**，通常将百万维变形场压缩至极低维的隐空间（如64-D向量），虽降低了动作空间复杂度，却不可避免地丢失了细粒度边界和几何细节。同时，医学图像分割标注极其稀缺，传统弱监督范式每个标记对仅提供一次监督信号，标签利用效率低下。

MorphSeek针对上述瓶颈提出了根本性的解决思路：**将编码器顶层的高分辨率潜在特征参数化为可采样的高斯策略，使RL直接在结构化潜在空间而非原始变形场上进行探索与优化**。这一设计保留了空间结构信息，同时通过多轨迹、多步细化的群组相对策略优化（Group Relative Policy Optimization, GRPO），将每对有限标签在T个细化步中对J条轨迹重复使用，产生T×J个相对监督事件，极大提升了标签效率。

方法遵循三阶段范式：（1）**RL友好重构**——解耦编码器-解码器，在编码器顶部附加均值头和对数标准差头，构建高维可采样潜在表示；（2）**无监督预热**——利用无标记数据塑造解剖保持的稳定潜在空间，为后续GRPO提供良好初始化；（3）**GRPO弱监督微调**——在少量分割标签下，以Dice增益和负雅可比惩罚作为奖励，通过潜在维度方差归一化（LDVN）稳定高维策略梯度更新。

核心实证结论如下：

- **跨基准一致提升**：在OASIS（脑MRI）、LiTS（肝脏CT）、Abdomen MR←CT三个3D配准任务上，MorphSeek在VoxelMorph-L、TransMorph、NICE-Trans三种骨干网络下均取得显著Dice提升（+2.1至+4.2个百分点）和负雅可比行列式（NJD）降低（Table 1、Figure 2）。
- **极高标签效率**：MorphSeek仅需60%的标记数据即可达到98.5%的满标签性能，而基线TransMorph需80%标签才能达到相当水平（Figure 3）。
- **训练稳定性关键依赖**：无监督预热将GRPO稳定训练成功率从33%提升至79%；LDVN缩放因子s=√N时性能最优，s=1导致梯度噪声和性能下降（Section 5.3、Figure 5）。
- **轻量级开销**：MorphSeek仅增加不到3%的模型参数，推理时间随细化步数近线性增长（Table 11）。

在方法谱系上，MorphSeek区别于**SPAC**（基于SAC的64-D压缩动作空间RL配准）、**RIIR**（固定级联逐步配准）和**WarpDDF+RegCut**（一致性正则化半监督配准），首次将高分辨率潜在空间策略优化引入DIR，在标签效率与配准精度之间实现了新的帕累托前沿。其核心洞察在于：**通过无监督预热构建稳定潜在空间，再以GRPO实现由粗到精的弱监督微调，使得有限标签在结构化探索中被反复复用**。

## 背景与动机

### 可变形图像配准：从单步预测到策略优化

可变形图像配准（Deformable Image Registration, DIR）是医学影像分析的核心任务之一，目标是为图像对建立密集的、体素级的空间对应关系，生成一个高维变形场 $\Phi$。近年来，基于深度学习的方法——如 **VoxelMorph** 和 **TransMorph**——通过单次前向传播直接预测变形场，在速度和精度上取得了显著进展。然而，这类方法本质上将配准建模为一个确定性的前馈映射，在面对大变形、复杂解剖结构或跨模态场景时，往往难以在一次推理中恢复精细的局部边界和几何细节。

强化学习（Reinforcement Learning, RL）为配准提供了另一种视角：将变形过程视为一个序贯决策问题，通过逐步优化变形场来应对复杂场景。然而，现有基于RL的配准方法面临一个根本性的维度瓶颈。以 **SPAC** 为例，该方法将高维变形场压缩到极低维的表示空间（如64维）中进行策略搜索，虽然降低了探索难度，却不可避免地丢失了大量空间细节，限制了配准精度的上限。这一困境揭示了一个核心矛盾：**百万维变形场的直接探索在计算上不可行，而过度压缩又会导致信息损失**。

### 标签效率：医学影像配准的持久挑战

医学影像配准面临的另一重约束是标注数据的极度稀缺。与自然图像不同，医学影像的解剖结构分割需要专家逐层标注，耗时且昂贵。在典型的弱监督配准设置中，通常仅有少量图像对拥有分割标签。传统的弱监督方法——无论是单步预测的 **TransMorph** 还是级联细化的 **RIIR**——每个标记对仅提供一次监督信号，标签利用效率低下。半监督方法如 **WarpDDF+RegCut** 尝试通过一致性正则化利用无标签数据，但并未从根本上改变“一对标签一对监督”的模式。

### MorphSeek 的核心动机

上述两个问题——高维探索的维度瓶颈和标签利用的低效率——在本质上相互关联。本文的核心洞察是：**如果在编码器的高分辨率潜在空间中构建一个可采样的策略分布，而非直接在变形场空间或极度压缩的表示空间中探索，就有可能在保留空间结构的同时实现高效的策略优化**。

具体而言，MorphSeek 的动机源于以下三个观察：

1. **结构化潜在空间比压缩表示更适合RL探索**。U-Net编码器顶层的高分辨率特征图天然保留了空间结构，将其参数化为高斯策略后，RL可以在一个既降维又保持空间对应关系的空间中进行探索，而非在百万维变形场上盲目搜索。

2. **多轨迹、多步骤的GRPO可以指数级复用标签**。在逐步细化框架下，每个细化步内采样多条轨迹并进行组内相对比较，使得每对标记图像产生 $T \times J$ 个相对监督事件（$T$ 为细化步数，$J$ 为轨迹数）。这从根本上改变了标签利用模式，使得有限标签下的性能显著提升成为可能。

3. **无监督预热是稳定高维GRPO的关键**。直接在随机初始化的潜在空间上运行GRPO会导致训练不稳定甚至崩溃。通过无监督预热，先让编码器学习到解剖保持的确定性表示，再将策略分布锚定在这一稳定流形上，可以大幅提升GRPO的收敛成功率和最终性能。

## 核心创新

MorphSeek的核心创新在于将可变形图像配准从“单次前向预测密集变形场”重构为“高分辨率潜在空间中的逐步策略优化”，从而在极低参数开销下同时提升配准精度与标注效率。

### 瓶颈诊断：现有RL配准方法的维度压缩困境

现有基于强化学习的配准方法（如**SPAC**）将高维变形场压缩至极低维的动作空间（如64-D），然后通过MLP解码器上采样回完整变形场。这一设计虽然降低了RL探索的难度，却从根本上丢失了空间细节——大变形场景下，单次前向传播难以恢复局部边界和精细几何结构。与此同时，医学图像标注极其稀缺，限制了监督信号的利用效率。MorphSeek的出发点正是打破这一“低维瓶颈”：**直接在编码器顶部的高分辨率特征图上构建可采样的策略空间**，让RL在保留空间结构的潜在表示上进行探索与优化。

### 关键机制：从确定性特征到可采样高斯策略

MorphSeek对标准编码器-解码器配准架构进行了三项关键重构（changed slots），形成统一的潜在空间策略优化范式：

**1. RL友好的架构解耦与策略头附加。** 传统配准网络将编码器输出的确定性特征 $\mathbf{f}_L$ 直接送入解码器预测变形场。MorphSeek在编码器顶部附加均值头 $\pmb{\mu}$ 和对数标准差头 $\log\pmb{\sigma}$，将顶层特征参数化为高斯分布 $\mathcal{N}(\pmb{\mu}, \pmb{\sigma}^2)$，并通过重参数化采样获得潜在向量：

$$\mathbf{z} = \pmb{\mu} + \tau \cdot \pmb{\sigma} \odot \pmb{\epsilon}, \quad \pmb{\epsilon} \sim \mathcal{N}(\mathbf{0},\mathbf{I})$$

其中温度 $\tau$ 调节探索强度。解码器以采样后的 $\mathbf{z}$ 替代原始 $\mathbf{f}_L$ 生成变形场，使编码器输出从“确定性特征”转变为“可采样的策略分布”。这一改动仅增加不足3%的参数量（Table 11），却将RL的动作空间从百万维变形场转移到结构化潜在空间，大幅降低了探索难度。

**2. 无监督预热构建解剖保持的稳定潜在空间。** 直接在高维潜在空间中进行RL训练极易发散。MorphSeek引入无监督预热阶段：令 $\tau=0$ 迫使所有解剖信息进入均值编码，通过图像相似度损失、变形场正则化以及KL散度项联合优化，构建一个解剖保持的稳定潜在空间结构。实验表明，去除预热（cold start）导致GRPO稳定训练成功率从79%骤降至33%，并显著延长收敛周期（Section 5.3 / Appendix 8.4）。这一预热机制为后续GRPO微调提供了良好的初始化分布，是方法成功的关键前提。

**3. 多轨迹多步骤GRPO与标签复用机制。** 在弱监督微调阶段，MorphSeek将每个标记对在 $T$ 个细化步内采样 $J$ 条轨迹，每条轨迹的奖励基于硬Dice增益和负雅可比惩罚：

$$R^{(j)} = w_{\mathrm{Dice}} \cdot [\mathrm{Dice}(S_f, S_{m\circ\Phi_t^{(j)}}) - \mathrm{Dice}(S_f, S_{m\circ\Phi_{t-1}})] + w_{\mathrm{NJD}} \cdot \mathrm{NJD}(\Phi_t^{(j)})$$

组内对 $J$ 条轨迹的奖励进行标准化得到优势函数 $A^{(j)} = \frac{R^{(j)} - \bar{R}}{\sigma_R + \epsilon}$，隐式重加权困难样本。**核心洞察在于：每对标记产生 $T \times J$ 个相对监督事件**，有限的标签在每个细化步中被重复用于组内比较，从而在极低标注比例下实现显著的标签效率提升——MorphSeek仅需60%的标记数据即可达到98.5%的满标签性能，而基线**TransMorph**需要80%标签才能达到相似水平（Figure 3）。

### 高维稳定化：LDVN缩放

GRPO的策略梯度更新依赖对数似然 $\log\pi(\mathbf{z}|\pmb{\mu},\pmb{\sigma})$。直接在高维潜在空间（$N$ 可达数千维，Table 10）求和所有维度会导致对数似然方差随 $N$ 线性增长，使组内相对比较数值不稳定。MorphSeek提出**Latent-Dimension Variance Normalization (LDVN)**，将对数似然除以缩放因子 $s \propto \sqrt{N}$：

$$\log \pi(\mathbf{z} \mid \pmb{\mu}, \pmb{\sigma}) = -\frac{1}{2s} \sum_{i=1}^N \left[\left(\frac{z_i - \mu_i}{\tau \sigma_i}\right)^2 + \log(2\pi \tau^2 \sigma_i^2)\right]$$

理论分析（Appendix 8）证明，当 $s = \sqrt{N}$ 时对数似然方差为 $\mathcal{O}(1)$，在保留策略梯度方向的同时稳定了更新幅度。消融实验（Figure 5, Table 5）验证了这一设计的有效性：$s = \sqrt{N}$ 达到最佳性能；$s = N$ 导致GRPO贡献微弱，性能接近基线；$s = 1$ 则引入梯度噪声，导致性能下降。

### 与基线方法的本质差异

| 设计维度 | 传统配准基线 | MorphSeek |
|---------|------------|-----------|
| 编码器输出 | 确定性特征 $\mathbf{f}_L$ | 可采样高斯策略 $\mathcal{N}(\pmb{\mu},\pmb{\sigma}^2)$ |
| 变形场生成 | 单次前向传播 | 多轨迹、多步骤逐步细化 |
| 对数似然处理 | 直接求和所有维度 | LDVN缩放至 $\mathcal{O}(1)$ 方差 |
| 训练范式 | 端到端无监督/弱监督 | 无监督预热 + GRPO弱监督微调 |
| 标签利用 | 每对提供一次监督 | 每对产生 $T \times J$ 个相对监督事件 |

MorphSeek的范式可泛化至任意编码器-解码器架构（已验证**VoxelMorph-L**、**TransMorph**、**NICE-Trans**三种骨干网络），在OASIS脑部MRI、LiTS肝脏CT、Abdomen MR←CT三个基准上均取得一致且显著的Dice提升（+2.1%至+4.2%）和NJD降低（Table 1），证明了该创新范式的通用性和有效性。

## 整体框架

MorphSeek 提出了一种面向可变形图像配准的**三阶段训练范式**，其核心思想是将配准任务重构为**潜在空间策略优化**问题。该范式可泛化至任意编码器-解码器架构的配准模型，通过在高分辨率潜在表示上进行强化学习探索，替代传统方法在百万维变形场空间中的直接优化。

### 阶段一：RL 友好的架构重构

传统配准网络（如 U-Net 架构）中，编码器 $\mathcal{E}$ 提取多尺度特征 $\{\mathbf{f}_1, \mathbf{f}_2, \ldots, \mathbf{f}_L\}$，解码器 $\mathcal{D}$ 直接根据这些特征预测密集变形场 $\Phi \in \mathbb{R}^{3 \times H \times W \times D}$。MorphSeek 对此进行关键重构：

- **解耦编码器与解码器**，在编码器顶层特征 $\mathbf{f}_L$ 之上附加**高斯策略头**，包含均值头 $\pmb{\mu}$ 和对数标准差头 $\pmb{\sigma}$，将原本确定性的特征映射参数化为可采样的高斯分布 $p(\mathbf{z} \mid \mathbf{f}_L)$。
- 通过重参数化采样 $\mathbf{z} = \pmb{\mu} + \tau \cdot \pmb{\sigma} \odot \pmb{\epsilon}, \; \pmb{\epsilon} \sim \mathcal{N}(\mathbf{0},\mathbf{I})$ 获得潜在向量，温度 $\tau$ 调节探索强度。
- 解码器接收采样后的潜在向量 $\mathbf{z}$ 替代原始 $\mathbf{f}_L$，生成变形场。这一设计使策略探索发生在**结构化的高分辨率潜在空间**（维度 $N$ 通常为数千至数万，如 OASIS+TransMorph 约 8,192 维），而非百万维的变形场空间，显著降低了强化学习的探索难度。

### 阶段二：无监督预热

在引入强化学习微调之前，MorphSeek 先利用大量无标记数据对重构后的网络进行**无监督预热**。此时设置温度 $\tau = 0$，迫使网络以确定性方式（$\mathbf{z} = \pmb{\mu}$）运行，通过图像相似度损失、变形场正则化项以及 KL 散度项联合优化，将解剖结构信息编码进均值表示 $\pmb{\mu}$ 中，构建一个**稳定且解剖保持的潜在空间**。实验表明，该预热阶段将后续 GRPO 稳定训练的成功率从 33% 提升至 79%，并显著加快收敛。

### 阶段三：基于 GRPO 的弱监督微调

在少量分割标签的弱监督设置下，MorphSeek 将编码器输出视为策略分布 $\pi(\mathbf{z} \mid \pmb{\mu}, \pmb{\sigma})$，采用**多轨迹、多步骤**的 Group Relative Policy Optimization (GRPO) 进行微调：

1. **多轨迹采样**：对每个输入对，在每个细化步 $t$ 内采样 $J$ 条轨迹 $\mathbf{z}^{(j)}$，解码得到 $J$ 个候选变形场 $\phi^{(j)}$。
2. **奖励计算**：每条轨迹的奖励 $R^{(j)}$ 由硬 Dice 增益和负雅可比行列式（NJD）惩罚组成，衡量该步变形相对于上一步的改进。
3. **组归一化优势**：对同一样本内的 $J$ 条轨迹奖励进行组内标准化，计算优势 $A^{(j)} = \frac{R^{(j)} - \bar{R}}{\sigma_R + \epsilon}$，隐式重加权困难样本。
4. **策略更新**：以最大化高奖励轨迹的采样概率为目标，结合**Latent-Dimension Variance Normalization (LDVN)** 控制高维对数似然的方差（缩放因子 $s \propto \sqrt{N}$），稳定梯度更新。
5. **逐步细化**：采用贪婪策略，选择最优轨迹更新当前变形场 $\Phi_t = \Phi_{t-1} \circ \phi^{(j^*)}$，经 $T$ 步迭代由粗到精地优化配准结果。

GRPO 微调阶段的总损失函数为：

$$\mathcal{E}_{\mathrm{grpo}}(\pmb\theta) = \mathcal{L}_{\mathrm{policy}}(\pmb\theta_E) + \lambda_{\mathrm{warm}} \mathcal{L}_{\mathrm{warm}}(\pmb\theta) + \lambda_{\mathrm{Dice}} \mathcal{L}_{\mathrm{Dice}}(\pmb\theta)$$

其中 $\mathcal{L}_{\mathrm{policy}}$ 为策略梯度损失，$\mathcal{L}_{\mathrm{warm}}$ 为预热损失正则项（防止灾难性遗忘），$\mathcal{L}_{\mathrm{Dice}}$ 为软 Dice 监督项。

### 标签效率的关键机制

该框架的一个核心优势在于**标签复用效率**：每个标记对在 $T$ 个细化步内产生 $T \times J$ 个相对监督事件（组内轨迹比较），使有限标签被反复利用。实验证实，MorphSeek 仅需 60% 的标记数据即可达到 98.5% 的满标签性能，而基线 TransMorph 需要 80% 标签才能达到相当水平。这一特性对医学图像分析中标注稀缺的现实约束具有重要价值。

### 补充图表

![[assets/figures/papers/paper_list_l2549_https_arxiv_org_abs_2511_17392/figures/001_Figure_1.jpg]]
*Figure 1: MorphSeek Registration Framework Process*

## 核心模块与公式推导

### 3.1 RL友好重构：从确定性特征到可采样潜在策略

传统配准网络的编码器-解码器结构将输入图像对 $(I_m, I_f)$ 映射为密集变形场 $\Phi$，其内部表示是确定性的。MorphSeek 的第一个核心改造是在编码器顶部构建一个**可采样的高分辨率潜在空间**，将其形式化为强化学习的策略分布。

具体而言，编码器 $\mathcal{E}$ 提取多尺度特征 $\{\mathbf{f}_1, \mathbf{f}_2, \ldots, \mathbf{f}_L\}$，其中顶层特征 $\mathbf{f}_L \in \mathbb{R}^{C \times H' \times W' \times D'}$ 保留了较高的空间分辨率。在此之上，MorphSeek 附加两个轻量级头部：

- **均值头** $\mu(\cdot)$：输出 $\pmb{\mu} \in \mathbb{R}^N$，作为潜在高斯分布的均值
- **对数标准差头** $\log\sigma(\cdot)$：输出 $\log\pmb{\sigma} \in \mathbb{R}^N$，经 $\sigma_i = \exp(\log\sigma_i)$ 得到标准差

由此，编码器输出不再是一个确定性向量，而是一个参数化的高斯策略：

$$\pi(\mathbf{z} \mid \pmb{\mu}, \pmb{\sigma}) = \mathcal{N}(\mathbf{z}; \pmb{\mu}, \tau^2 \cdot \text{diag}(\pmb{\sigma}^2))$$

其中温度参数 $\tau$ 控制探索强度。实际采样通过重参数化技巧实现：

$$\mathbf{z} = \pmb{\mu} + \tau \cdot \pmb{\sigma} \odot \pmb{\epsilon}, \quad \pmb{\epsilon} \sim \mathcal{N}(\mathbf{0},\mathbf{I}) \tag{Eq. 5}$$

采样得到的潜在向量 $\mathbf{z}$ 替代原始 $\mathbf{f}_L$ 送入解码器 $\mathcal{D}$，生成变形场 $\phi = \mathcal{D}(\mathbf{f}_1, \ldots, \mathbf{f}_{L-1}, \mathbf{z})$。这一设计的核心洞察在于：**将强化学习的探索空间从百万维的变形场压缩到结构化的潜在空间**，使策略搜索在语义上有意义的表示层面进行，而非在像素级噪声中盲目试探。

值得注意的是，潜在维度 $N$ 由特征图的空间尺寸和通道数决定（例如 TransMorph 在 OASIS 上 $N \approx 2.7 \times 10^4$），远小于变形场的维度（通常 $>10^6$），但仍远高于现有 RL 配准方法（如 **SPAC** 使用的 64-D 压缩动作空间），从而保留了足够的空间细节表达能力。

### 3.2 无监督预热：构建解剖保持的稳定潜在空间

直接在高维潜在空间上应用 GRPO 面临严重的冷启动问题：随机初始化的策略分布无法产生有意义的变形，导致奖励信号稀疏且噪声极大。MorphSeek 的解决方案是引入**无监督预热阶段**，在不使用任何分割标签的情况下，为后续策略优化构建一个结构良好的潜在空间。

预热阶段的核心技巧是将温度设为 $\tau = 0$，此时 $\mathbf{z} = \pmb{\mu}$，网络退化为确定性配准模型。训练目标 $\mathcal{L}_{\text{warm}}$ 由三部分组成：

1. **图像相似度损失**（如局部归一化互相关 NCC）：确保变形后的移动图像与固定图像在灰度层面匹配
2. **变形场正则化**（如扩散正则化）：惩罚不光滑的变形，鼓励解剖合理性
3. **KL 散度项**：$\mathcal{L}_{\text{KL}} = \beta \cdot D_{\text{KL}}(\mathcal{N}(\pmb{\mu}, \pmb{\sigma}^2) \| \mathcal{N}(\mathbf{0}, \mathbf{I}))$，防止后验坍缩，维持潜在空间的探索能力

预热的关键作用是**将解剖对应信息编码进均值 $\pmb{\mu}$**，使后续 GRPO 微调从一个合理的基线开始探索，而非从随机噪声出发。实验证据表明，无监督预热将 GRPO 稳定训练的成功率从 33% 提升至 79%（见 Section 5.3 / Appendix 8.4），并显著加快收敛。

### 3.3 GRPO 弱监督微调：多轨迹逐步策略优化

在预热获得的稳定潜在空间基础上，MorphSeek 采用**组相对策略优化（GRPO）**进行弱监督微调。该阶段的核心机制是：对每个训练图像对，在 $T$ 个细化步中分别采样 $J$ 条轨迹，利用少量分割标签计算奖励，并通过组内相对比较驱动策略更新。

**逐步细化范式**：设第 $t-1$ 步的累积变形场为 $\Phi_{t-1}$，当前步采样 $J$ 个潜在向量 $\{\mathbf{z}^{(j)}\}_{j=1}^J$，每个 $\mathbf{z}^{(j)}$ 经解码器产生增量变形场 $\phi^{(j)}$，组合后得到候选变形场 $\Phi_t^{(j)} = \Phi_{t-1} \circ \phi^{(j)}$。

**轨迹奖励设计**：每条轨迹的奖励由 Dice 增益和负雅可比惩罚构成：

$$R^{(j)} = w_{\mathrm{Dice}} \cdot [\mathrm{Dice}(S_f, S_{m\circ\Phi_t^{(j)}}) - \mathrm{Dice}(S_f, S_{m\circ\Phi_{t-1}})] + w_{\mathrm{NJD}} \cdot \mathrm{NJD}(\Phi_t^{(j)}) \tag{Eq. 9}$$

其中 $S_f$ 和 $S_m$ 分别为固定图像和移动图像的分割标签，Dice 增益衡量当前步带来的配准改进，NJD 惩罚抑制不合理的折叠变形。注意奖励计算使用的是**硬 Dice**（基于离散标签），而非可微的软 Dice，这使得奖励信号与最终评估指标直接对齐。

**组归一化优势**：GRPO 的核心创新在于对同一图像对内 $J$ 条轨迹的奖励进行组内标准化：

$$A^{(j)} = \frac{R^{(j)} - \bar{R}}{\sigma_R + \epsilon} \tag{Eq. 10}$$

其中 $\bar{R}$ 和 $\sigma_R$ 分别为组内均值和标准差。这一设计有两个关键优势：(1) 隐式地重加权困难样本——当所有轨迹的奖励都较低时，组内方差小，标准化后的优势值仍能提供有效的梯度方向；(2) 消除奖励尺度漂移，使不同图像对的梯度贡献更加均衡。

**LDVN：潜在维度方差归一化**：高维潜在空间（$N \approx 10^4$）带来的一个技术挑战是对数似然 $\log\pi(\mathbf{z})$ 的方差随 $N$ 线性增长，导致策略梯度噪声淹没有效信号。MorphSeek 提出 LDVN 解决此问题，将对数似然除以缩放因子 $s \propto \sqrt{N}$：

$$\log \tilde{\pi}(\mathbf{z} \mid \pmb{\mu}, \pmb{\sigma}) = -\frac{1}{2s} \sum_{i=1}^N \left[\left(\frac{z_i - \mu_i}{\tau \sigma_i}\right)^2 + \log(2\pi \tau^2 \sigma_i^2)\right] \tag{Eq. 12}$$

理论分析表明（见 Appendix 8），当潜在维度间满足弱相关假设时，$s = \sqrt{N}$ 使对数似然的方差保持 $O(1)$，从而稳定高维 GRPO 更新。消融实验（Figure 5, Table 5）证实 $s = \sqrt{N}$ 达到最佳性能；$s = N$ 过度压缩导致 GRPO 贡献微弱，$s = 1$ 则引入严重梯度噪声。

![[assets/figures/papers/paper_list_l2549_https_arxiv_org_abs_2511_17392/figures/008_Figure_5.jpg]]
*Figure 5: Validation Dice on OASIS for TransMorph under different LDVN scaling factors s*

**策略损失与总目标**：基于组归一化优势和 LDVN 缩放的对数似然，策略梯度损失为：

$$\mathcal{L}_{\mathrm{policy}}(\theta_E) = -\frac{1}{J} \sum_{j=1}^J A^{(j)} \cdot \log \tilde{\pi}^{(j)} \tag{Eq. 13}$$

GRPO 微调阶段的总损失整合策略优化、预热正则和辅助监督：

$$\mathcal{E}_{\mathrm{grpo}}(\pmb\theta) = \mathcal{L}_{\mathrm{policy}}(\pmb\theta_E) + \lambda_{\mathrm{warm}} \mathcal{L}_{\mathrm{warm}}(\pmb\theta) + \lambda_{\mathrm{Dice}} \mathcal{L}_{\mathrm{Dice}}(\pmb\theta) \tag{Eq. 15}$$

其中 $\mathcal{L}_{\text{warm}}$ 保留预热阶段的相似度和正则化项，防止 GRPO 探索导致解剖结构破坏；$\mathcal{L}_{\text{Dice}}$ 为软 Dice 损失，提供额外的梯度信号。推理时采用贪心策略，每步选择奖励最高的轨迹进行组合：

$$\Phi_t = \Phi_{t-1} \circ \phi^{(j^*)} \tag{Eq. 16}$$

**标签效率机制**：MorphSeek 的标签效率提升源于其多轨迹、多步设计。每个标记图像对在 $T$ 个细化步中产生 $T \times J$ 个相对监督事件（组内比较），使有限的标签被反复复用。实验表明，MorphSeek 仅需 60% 的标记数据即可达到 98.5% 的满标签性能，而基线 TransMorph 需要 80% 标签才能达到相似水平（Figure 3）。

## 实验与分析

### 主实验结果：跨基准、跨骨干的一致提升

MorphSeek 在三个 3D 医学图像配准基准（脑 MRI OASIS、肝脏 CT LiTS、腹部 MR←CT）上，分别基于三种不同的骨干网络（VoxelMorph-L、TransMorph、NICE-Trans）进行了验证。如 Table 1 所示，MorphSeek 在所有设置下均带来了显著的 Dice 提升和负雅可比行列式百分比（NJD）的降低。

![[assets/figures/papers/paper_list_l2549_https_arxiv_org_abs_2511_17392/figures/002_Table_1.jpg]]
*Table 1: Quantitative comparison on three registration tasks. All methods except affine use weakly supervised training. ↑: higher is better; ↓: lower is better. Our results are shown in bold and marked with * if there is a statistically significant difference*

在 OASIS 任务上，TransMorph+MorphSeek 达到 **88.9±1.8** 的 Mean Dice，较 TransMorph 基线的 85.8±1.4 提升了 **+3.1 个百分点**，NJD 则从 0.3% 降至 0.1%。在更具挑战性的腹部 MR←CT 跨模态配准中，TransMorph+MorphSeek 的 Mean Dice 达到 **86.5±3.4**，相比基线的 82.3±4.8 提升了 **+4.2 个百分点**，NJD 从 1.1% 降至 0.4%，降幅超过一半。LiTS 任务上同样观察到一致增益：NICE-Trans+MorphSeek 达到 90.5±3.7（基线 88.4±3.9，+2.1 pp）。

值得注意的是，MorphSeek 带来的增量并非仅适用于某一特定架构——VoxelMorph-L、TransMorph 和 NICE-Trans 三种结构迥异的骨干网络均获得了统计显著的提升（表中以 * 标注），验证了该训练范式作为即插即用模块的通用性。

Figure 2（代表性视觉对比）进一步揭示，MorphSeek 的改进集中在边界对齐和局部几何细节的恢复上。在腹部 MR←CT 任务中，基线方法在器官边界处出现明显的误对齐和模糊，而 MorphSeek 的变形场能更精准地贴合肝脏、脾脏等器官轮廓。在 OASIS 的 35 类脑区分割中，MorphSeek 对皮层下小结构（如海马体、杏仁核）的配准精度提升尤为突出。

![[assets/figures/papers/paper_list_l2549_https_arxiv_org_abs_2511_17392/figures/003_Figure_2.jpg]]
*Figure 2: Representative visual comparisons across the three registration tasks. Labels are overlaid only for the two abdominal tasks; OASIS is left unlabeled to avoid clutter from its 35 foreground classes. Additional visual results are provided in the supplement*

### 关键消融：轨迹数与细化步数

Table 2 系统性地考察了轨迹数（J）和细化步数（T）对配准性能的影响。实验在 OASIS 数据集上使用 TransMorph+MorphSeek 进行。

![[assets/figures/papers/paper_list_l2549_https_arxiv_org_abs_2511_17392/figures/005_Table_2.jpg]]
*Table 2: Ablation study on trajectory number and refinement steps on OASIS dataset. Using TransMorph + MorphSeek. Each cell shows Dice (%) ↑ / NJD (%) ↓*

**轨迹数**：从 2 条增加到 6 条轨迹，Mean Dice 持续上升（87.97→88.89），NJD 保持稳定在 0.06% 的低水平。这一趋势表明，在组内采样更多候选变形路径能有效探索潜在空间，增加找到更优变形的概率。但 8 条轨迹直接导致显存不足（OOM），暴露了多轨迹采样在内存层面的瓶颈。

**细化步数**：从 1 步增加到 3 步，Dice 从 88.14 提升至 88.89，NJD 从 0.07% 降至 0.06%。然而，超过 3 步后收益饱和甚至反转——4 步时 Dice 回落至 88.51，NJD 升至 0.07%。这表明逐步微调在适度步数内能有效累积改进，但过度迭代会引入变形伪影，可能与策略梯度在高维空间中的噪声累积有关。

综合来看，MorphSeek 在 **T=3, J=6** 的配置下达到最佳性能平衡点，后续实验均采用此设置。

### 标签效率：有限标注下的卓越表现

Figure 3 与 Section 5.2 展示了 MorphSeek 在标签效率上的核心优势。在 OASIS 数据集上，当仅使用 **60%** 的训练标记对时，MorphSeek 已达到满标签性能的 **98.5%**；而基线 TransMorph 需要 **80%** 的标签才能达到相当水平。这一差距源于 MorphSeek 的多轨迹、多步 GRPO 机制：每对标记图像在 T 个细化步内采样 J 条轨迹，通过组内相对比较产生 **T×J 个相对监督事件**，从而将稀缺的标注信号反复复用。在极端低标签场景（如仅 20% 标记对）下，MorphSeek 的性能优势更为明显，无监督预热构建的稳定潜在空间为 GRPO 微调提供了良好的初始化，避免了冷启动时的策略崩溃。

![[assets/figures/papers/paper_list_l2549_https_arxiv_org_abs_2511_17392/figures/004_Figure_3.jpg]]
*Figure 3: Impact of Warm-up and MorphSeek on GRPO Finetuning Performance with Limited Labeled Data (OASIS dataset)*

### 无监督预热的关键作用

去除无监督预热（cold start）的实验揭示了其决定性影响：GRPO 稳定训练的成功率从 **79% 骤降至 33%**（Section 5.3 / Appendix 8.4）。无预热时，策略在随机初始化的潜在空间中探索，高维对数似然的方差失控，导致梯度噪声淹没有效信号，训练频繁发散。预热阶段通过令温度 τ=0 迫使解剖信息进入均值编码，并利用相似度损失和 KL 正则化构建结构化的潜在空间，为后续 GRPO 提供了平滑的优化景观，不仅提升了稳定性，还缩短了收敛所需的迭代次数。

### LDVN 缩放因子的敏感性

Figure 5 和 Table 5 分析了 Latent-Dimension Variance Normalization（LDVN）中缩放因子 s 的影响。当 **s=√N**（N 为潜在维度，不同骨干/数据集组合的 N 值见 Table 10）时，验证 Dice 达到峰值。若 s=N（过度缩放），对数似然的组内方差被过度压缩，GRPO 的策略梯度贡献微弱，性能退化为接近基线水平。若 s=1（无缩放），高维对数似然的方差随 N 线性增长，梯度噪声导致训练不稳定且最终性能下降。这一结果验证了 LDVN 的设计动机：将高维对数似然的方差控制在 O(1) 量级，是 GRPO 在密集预测任务中稳定运行的必要条件。

![[assets/figures/papers/paper_list_l2549_https_arxiv_org_abs_2511_17392/figures/012_Table_5.jpg]]
*Table 5: Hyperparameter sensitivity on OASIS (TransMorph)*

### 组件贡献与失败模式

Table 3 的组件消融进一步量化了各模块的贡献。完整的 MorphSeek（含预热、GRPO、LDVN）达到 88.89 Dice / 0.06 NJD。移除 LDVN 后性能降至 88.14 / 0.08，移除 GRPO 仅保留预热和 Dice 监督则降至 87.63 / 0.09，验证了策略优化和方差归一化的独立增益。

![[assets/figures/papers/paper_list_l2549_https_arxiv_org_abs_2511_17392/figures/006_Table_3.jpg]]
*Table 3: Ablation analysis of MorphSeek components on OASIS dataset*

Table 5 的超参数敏感性分析揭示了若干关键失败模式：
- **去除 σ 裁剪**或设置过大的温度 τ 会导致策略分布过度离散，训练发散；
- **移除 KL 正则化**（预热损失的 KL 项）引发后验坍缩（Table 6），潜在空间的方差趋于零，策略失去探索能力，Dice 跨多次采样的标准差骤降；
- **移除预热损失中的图像相似度项**（Figure 6）导致 GRPO 出现“奖励黑客”现象——策略通过生成不合理的变形场（如过度拉伸或折叠）来最大化 Dice 增益，产生大量负雅可比区域，变形失去物理意义。

![[assets/figures/papers/paper_list_l2549_https_arxiv_org_abs_2511_17392/figures/010_Table_6.jpg]]
*Table 6: Posterior collapse analysis on OASIS. Dice is reported as mean±std (%) over ten latent samples for the same input pair*

![[assets/figures/papers/paper_list_l2549_https_arxiv_org_abs_2511_17392/figures/011_Figure_6.jpg]]
*Figure 6: Failure case when removing the similarity term from*

### 与多阶段基线的对比

Table 7 将 MorphSeek 与多阶段配准方法 LapIRN 进行对比。在相同的 100 对标记数据弱监督设置下，TransMorph+MorphSeek（88.9 Dice）显著优于 LapIRN（86.2 Dice），表明基于潜在空间策略优化的逐步微调比固定级联的渐进配准范式更有效。Table 8 进一步报告了经典优化方法（如 SyN、NiftyReg）的性能，这些方法在 CPU 时间上劣势明显（每对数十秒 vs. MorphSeek 的亚秒级），且 Dice 指标普遍低于学习方法。

### 效率分析

Table 11 的效率分析表明，MorphSeek 引入的额外参数不足骨干网络的 **3%**（仅增加均值头和对数标准差头）。推理时间随细化步数近线性增长：3 步时约为单次前向传播的 3 倍，但仍保持在可接受的亚秒级。多轨迹采样仅在训练阶段进行，推理时采用贪婪策略选择组内最优轨迹，无需额外采样开销。

![[assets/figures/papers/paper_list_l2549_https_arxiv_org_abs_2511_17392/figures/017_Table_11.jpg]]
*Table 11: Efficiency analysis on OASIS. MorphSeek adds less than 3% parameters and near-linear runtime growth with refinement steps*

### 补充图表

![[assets/figures/papers/paper_list_l2549_https_arxiv_org_abs_2511_17392/figures/018_Figure_7.jpg]]
*Figure 7: Label-wise Dice on OASIS (SPAC: Steps = 20, TransMorph+MorphSeek: Steps/Trajs = 3/6)*

## 方法谱系与知识库定位

### 一、与现有配准范式的谱系关系

MorphSeek 处于**可变形图像配准**与**强化学习策略优化**的交叉地带，其方法谱系可以从三个维度定位。

**1. 与密集预测式配准方法的关系。** 主流可变形配准方法——包括基于 U-Net 的 **VoxelMorph-L**、基于 Transformer 的 **TransMorph**、轻量级 **NICE-Trans** 以及基于 MLP 的 **CorrMLP**——均采用单次前向传播预测密集变形场的范式。这些方法将配准建模为端到端的确定性映射：编码器提取多尺度特征，解码器直接输出百万维变形场。MorphSeek 并未改变这一骨干架构，而是将其*重构*为可采样的策略网络：在编码器顶部附加均值头和对数标准差头，将原本确定性的潜在特征 $f_L$ 参数化为高斯分布 $p(z \mid f_L)$，使配准从“预测一个变形场”转变为“在结构化潜在空间中采样并优化变形场”。这一重构的参数量增加不足 3%（参见 Table 11），却从根本上改变了优化的自由度与搜索空间的结构。

**2. 与强化学习配准方法的关系。** 现有 RL-based DIR 方法（如 **SPAC**）将高维变形场压缩到低维动作空间（如 64-D），再通过 SAC 等算法进行策略优化。这种压缩虽然降低了策略搜索的难度，却不可避免地丢失了空间细节，导致大变形场景下局部边界和精细几何结构难以恢复。MorphSeek 的核心差异在于*不压缩*：它直接在编码器顶层的高分辨率潜在特征上构建策略分布（潜在维度 $N$ 通常在数千量级，参见 Table 10），使策略搜索发生在保留空间结构的表示空间中。为应对高维策略优化的数值挑战，MorphSeek 引入了 **Latent-Dimension Variance Normalization (LDVN)**，通过对数似然除以缩放因子 $s \propto \sqrt{N}$ 控制梯度方差，使 GRPO 在数千维空间中稳定运行。

**3. 与逐步/级联配准方法的关系。** **RIIR** 采用固定级联的逐步配准策略，每次迭代独立预测一个增量变形场。MorphSeek 借鉴了逐步细化的思想，但将其嵌入策略优化框架：在 $T$ 个细化步中，每步采样 $J$ 条轨迹，通过组内相对比较（GRPO）选择最优增量变形，并以贪婪方式组合。与 RIIR 的固定级联不同，MorphSeek 的每一步都是*自适应*的——策略根据当前状态（已累积的变形场）决定下一步的探索方向。与 **SPAC** 的 20 步策略执行相比，MorphSeek 仅需 3 步即可达到更优的 Dice 和 NJD（Figure 7, Figure 8），体现了潜在空间策略优化的效率优势。

**4. 与半监督配准方法的关系。** **WarpDDF+RegCut** 通过一致性正则化利用无标签数据，属于半监督学习范式。MorphSeek 的标签利用方式有本质不同：它将有限的标注对转化为 $T \times J$ 个相对监督事件——在 $T$ 个细化步中，每条轨迹的奖励通过 Dice 增益（相对于上一步）计算，组内标准化后形成优势信号。这种“标签复用”机制使 MorphSeek 仅需 60% 的标记数据即可达到满标签性能的 98.5%，而 TransMorph 基线需要 80% 标签才能达到相当水平（Figure 3）。

### 二、适用边界与局限

**解剖保持的依赖。** MorphSeek 的性能高度依赖无监督预热阶段构建的潜在空间质量。预热阶段通过相似度损失、正则化和 KL 项迫使解剖信息进入均值编码，为后续 GRPO 提供稳定的探索基础。去除预热（cold start）会导致 GRPO 稳定训练成功率从 79% 骤降至 33%（Section 5.3 / Appendix 8.4），且训练周期显著延长。这意味着 MorphSeek 要求目标域存在充足的无标注数据用于预热——在无标注数据也稀缺的场景中，该范式的有效性尚未验证。

**大变形场景的步数瓶颈。** 当前设计中，细化步数 $T$ 是全局固定的超参数。实验表明，$T$ 从 1 增至 3 带来持续增益，但超过 3 步后 Dice 饱和且 NJD 上升（Table 2），表明过度的策略探索可能引入变形伪影。在极端大变形场景（如手术前后的器官形变）中，固定 3 步可能不足以充分恢复对应关系，而简单增加步数又会触发 NJD 退化。这一矛盾指向一个开放问题：能否实现*自适应步数调度*，根据图像对难度动态决定每个样本的优化步数？

**标签依赖的底线。** GRPO 微调阶段仍依赖少量分割标签来计算基于 Dice 增益的奖励信号。在真正零标注场景中，MorphSeek 退化为纯无监督预热模型，无法享受策略优化带来的精度提升。如何将奖励信号替换为无监督度量（如基于图像相似度的局部结构对齐指标）是一个值得探索的方向，但当前框架并未提供这一能力。

**多轨迹采样的内存墙。** 每条轨迹需要独立的前向传播和变形场计算，$J$ 条轨迹的内存占用线性增长。在当前设定中，$J=8$ 即导致显存不足（Table 2），限制了可探索轨迹的规模。这一约束在 3D 医学图像场景尤为突出——单个体素网格的变形场本身已消耗大量内存。可能的缓解方向包括共享潜在空间的重要性采样、梯度检查点技术，或跨样本的轨迹复用策略。

**潜在空间可解释性的缺失。** 尽管 MorphSeek 在潜在空间中执行策略优化，但学习到的潜在维度与具体解剖结构之间的对应关系尚未建立。例如，我们无法判断某个潜在维度是否控制肝脏右叶的局部膨胀，或某个维度是否编码了脑沟回的折叠模式。这种“黑箱”特性限制了临床场景中的可信度评估和错误分析。

### 三、开放问题与前瞻

基于上述局限，以下开放问题值得后续工作关注：

1. **自适应细化调度。** 能否训练一个轻量级“难度评估器”，根据当前变形场的局部 NJD 或 Dice 增益预测是否需要额外细化步，从而实现样本级的自适应步数分配？

2. **无监督奖励设计。** 在无标注场景中，能否利用图像相似度的局部梯度（如局部归一化互相关的空间分布）作为奖励信号，替代基于分割标签的 Dice 增益？这需要解决奖励黑客问题——纯相似度驱动的策略可能产生不合理的折叠变形（正如 Figure 6 中移除预热相似度项后所观察到的）。

3. **生物力学先验的融入。** 当前奖励函数仅包含 Dice 增益和 NJD 惩罚，缺乏对组织物理特性的建模。将体积保持、超弹性约束或组织不可压缩性等先验融入策略优化的奖励或约束中，可能进一步提升配准的生理合理性。

4. **跨任务泛化。** 潜在空间策略优化范式是否适用于其他密集对应任务？光流估计、立体匹配和点云配准同样面临高维输出空间的优化挑战，LDVN 和多轨迹 GRPO 的组合可能具有跨领域的迁移价值。

5. **更大规模探索。** 能否通过共享潜在空间（如多对图像共享同一组潜在采样）或离线策略评估（如用已训练的 Critic 网络预筛选轨迹）来支持 $J > 8$ 的大规模探索，而不显著增加内存？

6. **LDVN 的自适应扩展。** 当前 LDVN 使用固定的全局缩放因子 $s \propto \sqrt{N}$，但不同编码器层级的潜在维度差异可能达到数量级（浅层高分辨率 vs. 深层低分辨率）。按层自适应调整 $s$，或将其参数化为可学习的缩放网络，可能进一步稳定训练并提升性能。

7. **与先进 RL 技术的结合。** 模型基 RL（在潜在空间中学习变形动力学模型）、离线 RL（从历史配准轨迹中学习）或好奇心驱动探索（奖励访问新颖潜在状态的策略）能否进一步提升标签效率和配准精度？这些技术在离散动作空间或低维连续控制中已有成功应用，但在高维密集预测场景中的适配仍待探索。

---

**证据强度说明：** 上述适用边界和局限均基于论文中提供的消融实验（Table 2, Table 5, Table 6, Figure 3, Figure 5, Figure 6）和附录分析（Appendix 8.4），置信度较高。开放问题部分属于基于实验观察的合理推断，部分方向（如自适应步数调度、无监督奖励设计）在论文的 limitations 和 discussion 中已有暗示，但具体实现路径需要后续工作验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/MorphSeek_Fine_grained_Latent_Representation_Level_Policy_Optimization_for_Deformable_Image_Registration.pdf]]
