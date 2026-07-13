---
title: Guiding Diffusion-based Reconstruction with Contrastive Signals for Balanced Visual Representation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Guiding_Diffusion_based_Reconstruction_with_Contrastive_Signals_for_Balanced_Visual_Representation.pdf
project_link: null
code_link: "https://github.com/boyuh/DCR"
aliases:
- DCRD
- GDBRCSBVR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 在扩散模型的噪声预测空间中构造对比三元组（锚点、正样本、负样本），用单一的DCR损失同时优化判别性与重建一致性。
primary_logic: 将对比信号从原始图像空间迁移至扩散模型的预测噪声空间，利用噪声预测的对比学习统一判别学习和重建学习，从根本上消除多目标优化中的梯度冲突。
claims:
- 直接加权组合对比损失与重建损失导致86.3%的训练步骤出现负梯度余弦相似度，造成优化冲突与收敛不稳定。
- DCR在MMVP-VLM基准上的P-Ability平均准确率比原始CLIP提升14.1%（OpenAI ViT-L@224）。
- 在CIFAR-10零样本分类上，DCR保持95.6%准确率，而GenHancer降至73.7%，证明DCR不损害判别能力。
- 理论分析（定理1和定理2）证明DCR损失可以同时满足判别性约束（类内/类间散度优化）和重建一致性约束。
---

# Guiding Diffusion-based Reconstruction with Contrastive Signals for Balanced Visual Representation

> [!tip] 核心洞察
> 将对比信号从原始图像空间迁移至扩散模型的预测噪声空间，利用噪声预测的对比学习统一判别学习和重建学习，从根本上消除多目标优化中的梯度冲突。

| 字段 | 内容 |
|------|------|
| 中文题名 | 利用对比信号引导扩散重建实现平衡视觉表示 |
| 英文题名 | Guiding Diffusion-based Reconstruction with Contrastive Signals for Balanced Visual Representation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.04803) · [Code](https://github.com/boyuh/DCR) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | Diffusion Contrastive Reconstruction (DCR) |
| Dataset | MMVP-VLM, Zero-shot Classification |

> [!tip] 效果简介
> - MMVP-VLM (P-Ability) 上，Accuracy 33.3 vs 19.2 (Original CLIP) (+14.1)。
> - Zero-shot Classification (CIFAR-10， D-Ability) 上，Accuracy 95.6 vs 73.7 (GenHancer) (+21.9)。

## 概要

### 问题背景：视觉编码器的能力失衡

视觉语言模型（VLM）的视觉编码器需要同时具备两种关键能力：**判别能力（D-Ability）**——即区分类别差异的语义理解力，以及**细节感知能力（P-Ability）**——即捕捉图像精细纹理、空间关系的感知力。CLIP 视觉编码器通过大规模对比学习获得了强大的判别能力，但在细节感知方面存在显著不足。近期工作尝试利用扩散模型的重建反馈来增强 P-Ability，然而这一方向面临一个根本性瓶颈：**直接组合对比损失与重建损失会导致严重的梯度冲突**。实验表明，在朴素联合训练中，86.3% 的训练步骤出现负梯度余弦相似度（Fig. 2(c)），对比损失主导优化过程，重建损失被抑制而无法收敛。

### 核心方法：扩散对比重建（DCR）

本文提出 **Diffusion Contrastive Reconstruction (DCR)**，核心思路是将对比信号从原始图像空间迁移至扩散模型的**预测噪声空间**，用单一损失函数同时优化判别性与重建一致性，从根本上消除多目标优化中的梯度冲突。

具体而言，DCR 在扩散模型的噪声预测空间中构造对比三元组：以原图的条件预测噪声为锚点，以增强视图的预测噪声和真实噪声为正样本，以批次中其他图像的预测噪声为负样本，通过统一的 DCR 损失引导编码器学习。方法采用两阶段训练协议——先冻结编码器训练投影器以对齐扩散条件空间，再冻结投影器并用 LoRA 微调编码器——确保训练稳定性和收敛效率。

### 方法定位

DCR 属于**基于扩散模型的视觉表示增强**方法，与现有工作的关键区别在于：

- 不同于 **DIVA**（扩散视觉反馈）、**GenHancer**（离散潜在空间重建）、**un²CLIP**（逆向生成对齐）等方法直接使用重建损失或线性组合多目标，DCR 将对比学习与重建学习统一在预测噪声的单一损失中，避免了梯度冲突。
- 理论上，DCR 损失同时满足判别性约束（最小化类内散度、最大化类间散度）和重建一致性约束（定理 1 和定理 2），为能力平衡提供了形式化保证。

### 主要结果

在 OpenAI CLIP ViT-L@224 骨干网络上：

- **P-Ability**：在 MMVP-VLM 基准上，DCR 的细节感知准确率达到 33.3%，较原始 CLIP（19.2%）**提升 14.1 个百分点**（Tab. 1）。
- **D-Ability**：在 CIFAR-10 零样本分类上，DCR 保持 95.6% 准确率，而 GenHancer 降至 73.7%，证明 DCR **不损害判别能力**（Tab. 6）。
- **多模态下游任务**：以 DCR 增强的视觉编码器替换 LLaVA-1.5 中的 CLIP 编码器后，在多项 MLLM 基准上取得一致提升（Tab. 3）。

方法训练开销较低（OpenAI ViT-L@224 约 7.7 小时，53.5 GB 显存），可扩展至多种 CLIP 架构。



### 视觉表示学习的双重能力失衡

视觉表示学习长期面临一个核心矛盾：**判别能力（D-Ability）**与**细节感知能力（P-Ability）**难以兼得。以CLIP为代表的对比学习方法通过大规模图文配对训练，赋予了视觉编码器强大的语义判别能力，使其在零样本分类、聚类等任务上表现优异。然而，这类方法本质上优化的是全局语义对齐，编码器倾向于忽略细粒度的视觉细节——例如物体的精确朝向、数量关系、空间位置等——导致在需要精细感知的下游任务中频繁出错。

为弥补这一缺陷，近期工作开始引入**扩散重建**作为辅助训练信号。其基本思路是：将CLIP特征作为扩散模型的条件输入，通过重建原始图像来迫使编码器保留更多像素级信息。**DIVA**、**GenHancer**、**un²CLIP**等方法沿这一路线取得了部分成功，显著提升了编码器的细节感知能力。

### 朴素联合训练的梯度冲突困境

一个自然的想法是将对比损失与重建损失直接组合，以同时增强两种能力：

$$\mathcal{L}_{\text{naive}} = \mathcal{L}_{\text{con}} + \lambda \mathcal{L}_{\text{rec}}$$

其中 $\mathcal{L}_{\text{con}}$ 为InfoNCE风格的对比损失，$\mathcal{L}_{\text{rec}}$ 为扩散模型的噪声预测MSE损失。然而，实验表明这种朴素方案存在根本性缺陷。

如 **Figure 2** 所示，在训练过程中，对比损失梯度 $\mathbf{g}_{\text{con}}$ 与重建损失梯度 $\mathbf{g}_{\text{rec}}$ 的方向频繁背离。定量分析显示，**86.3%的训练步骤**出现负的梯度余弦相似度：

$$\cos(\mathbf{g}_{\text{con}}, \mathbf{g}_{\text{rec}}) = \frac{\mathbf{g}_{\text{con}}^\top \mathbf{g}_{\text{rec}}}{\|\mathbf{g}_{\text{con}}\|_2 \|\mathbf{g}_{\text{rec}}\|_2} < 0$$

这种梯度冲突意味着两个优化目标相互对抗：对比损失倾向于将不同样本的特征推开以增强类间可分性，而重建损失则要求特征保留足够的实例特异性以还原图像细节。两者在特征空间中施加方向相反的力，导致优化过程震荡、收敛不稳定，最终表现为**判别能力与细节感知能力的零和博弈**——增强一方必然损害另一方。例如，GenHancer在MMVP-VLM基准上提升了细节感知，但其CIFAR-10零样本分类准确率从原始CLIP的95.6%骤降至73.7%，充分暴露了这一困境。

### 核心洞察：将对比信号迁移至噪声空间

本文的核心洞察在于识别出梯度冲突的**根源**：对比损失与重建损失分别作用于不同的表示空间——前者在特征空间（$\mathbf{z}$）上计算相似度，后者在像素/噪声空间（$\hat{\epsilon}$）上计算MSE。两个空间中的优化方向天然不一致。

由此提出**扩散对比重建（Diffusion Contrastive Reconstruction, DCR）**方法，其关键思路是：**将对比信号从原始图像特征空间迁移至扩散模型的预测噪声空间**。具体而言，对于锚点图像，利用其CLIP特征作为条件，让扩散模型预测噪声 $\hat{\epsilon}$；同时，对正样本（增强视图）和负样本（批次中其他图像）也分别预测噪声。这些预测噪声天然构成了对比学习所需的三元组——锚点噪声应接近正样本噪声和真实噪声，远离负样本噪声。通过在这一统一的噪声空间中构造单一的对比损失 $\mathcal{L}_{\text{dcr}}$，从根本上消除了多目标优化中的梯度冲突。

理论分析（定理1和定理2）进一步证明，$\mathcal{L}_{\text{dcr}}$ 可以同时满足判别性约束（最小化类内散度、最大化类间散度）和重建一致性约束（锚点噪声逼近真实噪声），为方法的有效性提供了严格保证。



## 核心方法与创新机理

### 问题诊断：扩散重建与对比学习的梯度冲突

CLIP 视觉编码器存在判别能力（D-Ability）与细节感知能力（P-Ability）的失衡。基于扩散模型的重建方法（如 DIVA、GenHancer、un²CLIP）虽能提升 P-Ability，却损害 D-Ability。一个直观的补救思路是将对比损失 $\mathcal{L}_{\mathrm{con}}$ 与重建损失 $\mathcal{L}_{\mathrm{rec}}$ 进行线性加权组合：

$$\mathcal{L}_{\mathrm{joint}} = \lambda_{\mathrm{con}} \mathcal{L}_{\mathrm{con}} + \lambda_{\mathrm{rec}} \mathcal{L}_{\mathrm{rec}}$$

然而，实验表明这种朴素组合存在严重问题：**86.3% 的训练步骤中，两个损失的梯度余弦相似度为负值**（Fig. 2(c)），即梯度方向相互冲突。对比损失主导了优化过程，而重建损失被压制，无法有效收敛（Fig. 2(a)(b)）。这一发现揭示了多目标优化中的根本性障碍——两个损失函数在参数空间中指向不同的优化方向，简单的加权求和无法实现能力的平衡。

### 核心洞察：将对比信号迁移至预测噪声空间

DCR 的关键创新在于**改变了对比信号的来源**。传统方法在原始图像特征空间中构造对比三元组，而 DCR 将对比学习迁移至扩散模型的**预测噪声空间**。具体而言，给定输入图像 $\mathbf{x}$，扩散模型基于不同条件预测噪声：

- **锚点**：基于原始图像条件预测的噪声 $\hat{\epsilon}_{\mathrm{orig}}$
- **正样本**：基于增强视图条件预测的噪声 $\hat{\epsilon}_{\mathrm{aug}}$，以及真实噪声 $\epsilon_t^{\mathrm{gt}}$
- **负样本**：批次中其他图像条件预测的噪声

这些预测噪声在重建图像空间中形成对比三元组（Fig. 3），DCR 损失定义为：

$$\mathcal{L}_{\mathrm{dcr}} = -\frac{1}{2} \sum_{p \in P} \log \frac{d(\hat{\epsilon}, p)}{\sum_{c \in C} d(\hat{\epsilon}, c)}$$

其中 $d(u, v) = \exp(\mathrm{sim}(u, v) / \tau)$，$P$ 为正样本集，$C = P \cup N$ 包含正负样本全集。

### 关键 changed slots 分析

| 设计维度 | 基线方法 | DCR 方法 | 创新本质 |
|:---|:---|:---|:---|
| **优化目标** | 线性组合 $\mathcal{L}_{\mathrm{con}} + \mathcal{L}_{\mathrm{rec}}$ | 单一 $\mathcal{L}_{\mathrm{dcr}}$ | 从根本上消除多目标梯度冲突 |
| **对比信号来源** | 原始图像特征 $\mathbf{z}$ | 扩散模型预测噪声 $\hat{\epsilon}$ | 将判别学习与重建学习统一在同一表示空间 |
| **训练策略** | 端到端联合训练或简单加权 | 两阶段：Stage-1 冻结编码器训练投影器，Stage-2 冻结投影器用 LoRA 微调编码器 | 先对齐条件空间，再增强编码器，避免冷启动冲突 |

### 为什么预测噪声空间能统一两个目标？

理论分析（定理 1 和定理 2）为这一设计提供了严格保证。定理 1 建立了特征空间散度与噪声空间散度之间的界限关系：

$$S_{\mathrm{inner}} \leq \frac{1}{m^2} S_{\mathrm{inner}}^{(\epsilon)}(t), \quad S_{\mathrm{inter}} \geq \kappa S_{\mathrm{inter}}^{(\epsilon)}(t) - \eta S_{\mathrm{inner}}^{(\epsilon)}(t)$$

该不等式表明：最小化噪声空间中的类内距离 $S_{\mathrm{inner}}^{(\epsilon)}$ 可同时约束特征空间的类内散度，而最大化噪声空间中的类间距离 $S_{\mathrm{inter}}^{(\epsilon)}$ 则推动特征空间的类间分离。定理 2 进一步证明，DCR 损失能够同时满足重建一致性约束。因此，**在预测噪声空间上执行对比学习，等价于在单一损失函数中同时优化判别性约束和重建约束**，从根本上规避了多目标梯度冲突。

### 与基线方法的本质区别

- **DIVA** 等基于扩散反馈的方法仅利用重建信号增强感知，未引入对比机制，导致 D-Ability 退化。
- **GenHancer** 在离散潜在空间中扩展重建，使用全局条件与轻量去噪器，但同样缺乏判别性约束。
- **un²CLIP** 试图通过逆向生成过程保持与 CLIP 嵌入空间的对齐，但仍未解决判别与感知的联合优化问题。

DCR 的独特性在于：它不将对比学习和重建学习视为两个独立目标进行折中，而是**通过空间迁移将二者统一为同一优化问题**，使得模型在提升细节感知能力的同时，不牺牲甚至增强判别能力。这一设计使得 DCR 在 MMVP-VLM 基准上的 P-Ability 准确率比原始 CLIP 提升 14.1%（OpenAI ViT-L@224，Tab. 1），同时在 CIFAR-10 零样本分类上保持 95.6% 的准确率，而 GenHancer 降至 73.7%（Tab. 6）。



DCR 的整体框架围绕一个核心设计展开：**将对比信号从原始图像空间迁移至扩散模型的预测噪声空间**，从而在单一优化目标下同时增强 CLIP 视觉编码器的判别能力（D-Ability）与细节感知能力（P-Ability）。框架由三个功能模块串联构成，并通过两阶段训练协议协调各模块的优化。

### 模块组成与数据流

**CLIP 视觉编码器 $f_\phi$** 是整个框架的增强目标。输入图像 $\mathbf{x}$ 首先经过该编码器提取视觉特征 $\mathbf{z} = f_\phi(\mathbf{x})$。编码器可以是任意 CLIP 骨干（如 OpenAI ViT-L、MetaCLIP ViT-H、SigLIP ViT-SO 等），DCR 方法对其架构无侵入性修改。

**投影器 $h_\omega$** 是一个两层 MLP，负责将 CLIP 特征映射到扩散模型的条件空间。这一映射的必要性在于：CLIP 特征空间与 Stable Diffusion 的文本条件空间存在分布差异，直接使用原始特征作为扩散条件会导致生成质量下降。投影器在 Stage-1 中首先被训练，以建立视觉条件与文本条件之间的对齐。

**冻结的 Stable Diffusion 模型 $\epsilon_\theta$** 提供生成反馈，其作用不是生成最终图像，而是为对比学习构造三元组。具体而言，对于给定图像 $\mathbf{x}$，扩散模型基于不同条件预测噪声：
- **锚点（anchor）**：以原始图像特征为条件预测的噪声 $\hat{\epsilon}(\mathbf{x})$
- **正样本（positive）**：以数据增强视图的特征为条件预测的噪声 $\hat{\epsilon}(\mathbf{x}^+)$，以及真实噪声 $\epsilon_t^{\mathrm{gt}}$
- **负样本（negative）**：批次中其他图像的特征为条件预测的噪声 $\hat{\epsilon}(\mathbf{x}^-)$

这三者在预测噪声空间中构成对比三元组（见 Figure 3 左侧），直接支撑 DCR 损失的计算。

![[assets/figures/papers/paper_list_l2517_https_arxiv_org_abs_2603_04803/figures/003_Figure_3.jpg]]
*Figure 3: An overview of Diffusion Contrastive Reconstruction (DCR). An image is encoded by CLIP and projected into the diffusion condition space. Predicted noises from original, augmented, and negative samples form a contrastive triplet in the reconstruction image space. Training proceeds in two stages: projector alignment and encoder enhancement*

### 两阶段训练协议

DCR 采用分阶段训练策略，而非端到端联合优化。这一设计源于对朴素联合训练失败原因的深入分析：直接加权组合对比损失 $\mathcal{L}_{\mathrm{con}}$ 与重建损失 $\mathcal{L}_{\mathrm{rec}}$ 会导致严重的梯度冲突——86.3% 的训练步骤中，两个损失的梯度余弦相似度为负值（见 Figure 2(c)），且 $\mathcal{L}_{\mathrm{con}}$ 主导优化过程，$\mathcal{L}_{\mathrm{rec}}$ 被压制而无法收敛。

两阶段协议的具体安排如下：

**Stage-1（投影器对齐）**：冻结 CLIP 编码器 $f_\phi$ 和扩散模型 $\epsilon_\theta$，仅训练投影器 $h_\omega$。此阶段的目标是学习一个条件映射，使视觉引导与扩散模型中原有的文本引导对齐，确保冻结的去噪器能正确解读基于图像的条件信号。训练使用标准的扩散重建损失 $\mathcal{L}_{\mathrm{rec}}$。

**Stage-2（编码器增强）**：冻结投影器 $h_\omega$ 和扩散模型 $\epsilon_\theta$，使用 LoRA 微调 CLIP 编码器 $f_\phi$。此阶段引入 DCR 损失 $\mathcal{L}_{\mathrm{dcr}}$，在预测噪声空间上执行对比学习，同时优化判别性与重建一致性。由于对比信号来源于扩散模型的噪声预测而非原始图像特征，从根本上消除了多目标优化中的梯度冲突问题。

### 统一优化的关键机制

DCR 损失的核心公式为：

$$\mathcal{L}_{\mathrm{dcr}} = -\frac{1}{2} \sum_{p \in P} \log \frac{d(\hat{\epsilon}, p)}{\sum_{c \in C} d(\hat{\epsilon}, c)}$$

其中 $d(u, v) = \exp(\mathrm{sim}(u, v) / \tau)$ 为指数化余弦相似度，$P$ 为正样本集（包含增强视图的预测噪声和真实噪声），$C = P \cup N$ 为候选集（$N$ 为批次中其他图像的预测噪声构成的负样本集）。

这一设计的核心洞察在于：当编码器 $f_\phi$ 被优化以最小化 $\mathcal{L}_{\mathrm{dcr}}$ 时，锚点噪声与正样本噪声的相似度被拉近，与负样本噪声的相似度被推远。由于正样本包含真实噪声 $\epsilon_t^{\mathrm{gt}}$，这一过程天然地包含了重建约束；同时，正负样本的区分又提供了判别性监督。理论分析（定理 1 和定理 2）进一步证明，最小化 DCR 损失可以同时满足判别性约束（类内散度 $S_{\mathrm{inner}}$ 减小、类间散度 $S_{\mathrm{inter}}$ 增大）和重建一致性约束，从而在单一目标中实现两种能力的平衡增强。

### 训练开销与可扩展性

DCR 的训练开销相对可控。以 OpenAI ViT-L@224 骨干为例，完整训练约需 7.7 小时、53.5 GB 显存（见 Tab. 8）。方法可扩展至多种 CLIP 架构，包括 ViT-B、ViT-L、ViT-H 和 ViT-SO 等不同规模的模型，且所有实验均在统一的 CC3M 数据集上进行训练，未引入额外人工标注或私有数据，保证了对比的公平性。

### 补充图表

![[assets/figures/papers/paper_list_l2517_https_arxiv_org_abs_2603_04803/figures/001_Figure_1.jpg]]
*Figure 1: (a) Contrastive learning for D-Ability. (b) Reconstructive learning for P-Ability. (c) Our Diffusion Contrastive Reconstruction (DCR) for harmonizing D-Ability and P-Ability. (d) Performance overview of DCR and other methods on the OpenAI CLIP ViT-L@224 backbone*



### 问题形式化：判别能力与感知能力的双重约束

视觉表示学习的目标是学习编码器 $f_\phi: \mathcal{X} \rightarrow \mathcal{Z}$，将图像 $\mathbf{x}$ 映射为视觉表示 $\mathbf{z}$。该表示需同时满足两类约束：

- **判别能力（D-Ability）**：最小化类内散度 $S_{\mathrm{inner}}$，最大化类间散度 $S_{\mathrm{inter}}$，即 $\min S_{\mathrm{inner}}, \max S_{\mathrm{inter}}$。
- **感知能力（P-Ability）**：要求表示保留足够的细节信息以支持高质量重建。在扩散模型框架下，这体现为最小化重建损失：

$$\mathcal{L}_{\mathrm{rec}} = \mathbb{E}_t \Big[ \| \epsilon_\theta(\mathbf{x}_t, h_\omega(f_\phi(\mathbf{x})), t) - \epsilon_t^{\mathrm{gt}} \|_2^2 \Big]$$

其中 $\epsilon_\theta$ 为冻结的 Stable Diffusion 去噪器，$h_\omega$ 为将 CLIP 特征映射至扩散条件空间的两层 MLP 投影器，$\epsilon_t^{\mathrm{gt}}$ 为真实噪声。

### 朴素联合训练的梯度冲突

最直接的多目标优化方案是线性加权组合对比损失与重建损失：

$$\mathcal{L}_{\mathrm{joint}} = \lambda_{\mathrm{con}} \mathcal{L}_{\mathrm{con}} + \lambda_{\mathrm{rec}} \mathcal{L}_{\mathrm{rec}}$$

其中对比损失 $\mathcal{L}_{\mathrm{con}}$ 为标准 InfoNCE 形式：

$$\mathcal{L}_{\mathrm{con}} = \frac{1}{|\mathcal{B}|} \sum_{i \in \mathcal{B}} -\log \frac{\sum_{j \in \mathcal{P}(i)} \exp(\sin(\mathbf{z}_i, \mathbf{z}_j) / \tau)}{\sum_{k \in \mathcal{B} \setminus \{i\}} \exp(\sin(\mathbf{z}_i, \mathbf{z}_k) / \tau)}$$

然而，实验揭示该方案存在严重的梯度冲突。定义梯度余弦相似度为：

$$\cos(\mathbf{g}_{\mathrm{con}}, \mathbf{g}_{\mathrm{rec}}) = \frac{\mathbf{g}_{\mathrm{con}}^\top \mathbf{g}_{\mathrm{rec}}}{\|\mathbf{g}_{\mathrm{con}}\|_2 \|\mathbf{g}_{\mathrm{rec}}\|_2}$$

分析表明，**86.3% 的训练步骤中该余弦相似度为负值**（Fig. 2(c)），即两个优化目标在参数空间中指向相反方向。同时，对比损失在优化中占据主导地位，重建损失被压制而无法收敛（Fig. 2(a)(b)）。这一发现构成了本文的核心瓶颈：直接组合对比损失与重建损失无法实现 D-Ability 与 P-Ability 的平衡。

### DCR 损失：预测噪声空间的统一对比学习

为解决上述梯度冲突，DCR 将对比信号从原始图像特征空间**迁移至扩散模型的预测噪声空间**，构造单一优化目标。具体而言，对每张输入图像 $\mathbf{x}$，构造对比三元组：

- **锚点（Anchor）**：原始图像经编码器 $f_\phi$ 和投影器 $h_\omega$ 条件化后，扩散模型预测的噪声 $\hat{\epsilon} = \epsilon_\theta(\mathbf{x}_t, h_\omega(f_\phi(\mathbf{x})), t)$。
- **正样本集 $P$**：包含 (1) 增强视图 $\mathbf{x}^+$ 的预测噪声 $\hat{\epsilon}^+$，(2) 真实噪声 $\epsilon_t^{\mathrm{gt}}$。
- **负样本集 $N$**：批次中其他图像的预测噪声。

在预测噪声空间上定义对比损失：

$$\mathcal{L}_{\mathrm{dcr}} = -\frac{1}{2} \sum_{p \in P} \log \frac{d(\hat{\epsilon}, p)}{\sum_{c \in C} d(\hat{\epsilon}, c)}$$

其中 $C = P \cup N$，相似度函数 $d(u, v) = \exp(\mathrm{sim}(u, v) / \tau)$，$\tau$ 为温度参数。

该设计的核心洞察在于：**正样本集同时包含增强视图的预测噪声和真实噪声**。前者通过对比机制隐式地拉近同一图像不同视图的表示（增强判别能力），后者则强制预测噪声逼近真实噪声（保证重建质量）。由于两个目标被统一在同一个对比损失中，从根本上消除了多目标优化中的梯度冲突。

### 理论保证：散度界限与一致性约束

论文通过两个定理为 DCR 损失提供了理论支撑（详见 Sec. 4.3）：

**定理 1（类内/类间散度界限）**：最小化 $\mathcal{L}_{\mathrm{dcr}}$ 可同时约束特征空间的类内散度 $S_{\mathrm{inner}}$ 和类间散度 $S_{\mathrm{inter}}$，满足：

$$S_{\mathrm{inner}} \leq \frac{1}{m^2} S_{\mathrm{inner}}^{(\epsilon)}(t), \quad S_{\mathrm{inter}} \geq \kappa S_{\mathrm{inter}}^{(\epsilon)}(t) - \eta S_{\mathrm{inner}}^{(\epsilon)}(t)$$

其中 $S_{\mathrm{inner}}^{(\epsilon)}(t)$ 和 $S_{\mathrm{inter}}^{(\epsilon)}(t)$ 为预测噪声空间的对应散度。该定理表明，在噪声空间优化的对比目标能够有效传导至特征空间，同时实现类内紧凑和类间分离。

**定理 2（重建一致性保证）**：正样本集中包含真实噪声 $\epsilon_t^{\mathrm{gt}}$ 确保了优化过程不会偏离重建目标，DCR 损失隐式地满足重建一致性约束。

### 两阶段训练协议

DCR 采用两阶段训练策略以稳定优化过程（Fig. 3）：

- **Stage-1（投影器对齐）**：冻结 CLIP 视觉编码器 $f_\phi$ 和 Stable Diffusion 去噪器 $\epsilon_\theta$，仅训练投影器 $h_\omega$。目标是使视觉条件与扩散模型原有的文本条件空间对齐，确保冻结的去噪器能正确理解基于图像的条件信号。
- **Stage-2（编码器增强）**：冻结投影器 $h_\omega$，使用 LoRA 微调视觉编码器 $f_\phi$。在此阶段，DCR 损失通过预测噪声空间的对比信号同时优化判别能力和细节感知能力。

消融实验证实该协议的必要性：端到端联合训练在 MMVP-VLM 上仅取得 25.93 的准确率，而两阶段训练提升至 33.30（Tab. 4(b)）。

### 补充图表

![[assets/figures/papers/paper_list_l2517_https_arxiv_org_abs_2603_04803/figures/002_Figure.jpg]]
*Figure: (b) Reconstruction loss $\mathcal { L }$ _ ${ \mathrm { r e c } }$ (a) Contrastive loss ${ \mathcal { L } }$ _ ${ \mathrm { c o n } }$ . (c) Cosine similarity between gradient ${ \bf$ g } _ ${ \mathrm { c o n } }$ and $\mathrm { { \bf g } }$ _ ${ \mathrm { r e c } }$*



## 实验与关键发现

### 核心瓶颈的实证验证：梯度冲突

朴素地将对比损失 $\mathcal{L}_{\mathrm{con}}$ 与重建损失 $\mathcal{L}_{\mathrm{rec}}$ 线性组合为 $\mathcal{L}_{\mathrm{joint}} = \lambda_{\mathrm{con}} \mathcal{L}_{\mathrm{con}} + \lambda_{\mathrm{rec}} \mathcal{L}_{\mathrm{rec}}$ 会导致严重的优化冲突。实验观测表明（Fig. 2），在训练过程中，$\mathcal{L}_{\mathrm{con}}$ 主导了优化过程，而 $\mathcal{L}_{\mathrm{rec}}$ 被压制且无法收敛。更关键的是，**86.3% 的训练步骤**中，两个损失的梯度余弦相似度 $\cos(\mathbf{g}_{\mathrm{con}}, \mathbf{g}_{\mathrm{rec}})$ 为负值，意味着梯度方向频繁背离，且冲突程度随训练加深而加剧。这一实证发现构成了 DCR 方法设计的直接动机——必须用单一目标函数替代多目标加权组合。

### P-Ability 主结果：细节感知能力

在 MMVP-VLM 基准上，DCR 在多个 CLIP 骨干网络上一致地大幅提升了细节感知能力（Table 1）。以 OpenAI ViT-L@224 为例，DCR 将平均准确率从原始 CLIP 的 19.2% 提升至 **33.3%**（+14.1%），在所有对比方法中取得最优。DCR 在 MetaCLIP ViT-H-14（37.8%）和 SigLIP ViT-SO-14@224（43.0%）等更大规模骨干上也保持领先，且在各种视觉模式（如方向判别、数量计数、位置关系等）上表现出鲁棒性。定性结果（Fig. 4）进一步显示，改进后的 CLIP 能有效纠正原始模型在捕获细粒度视觉细节上的系统性错误。

![[assets/figures/papers/paper_list_l2517_https_arxiv_org_abs_2603_04803/figures/004_Table_1.jpg]]
*Table 1: Performance of Detail Perceptual Ability (P-Ability) on the MMVP-VLM benchmark. Results of baseline methods are taken from [43, 57, 77]. Our method outperforms across multiple CLIP backbones and exhibits robustness across various visual patterns. The visual patterns are symbolized as*

![[assets/figures/papers/paper_list_l2517_https_arxiv_org_abs_2603_04803/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative results of P-Ability on the MMVP-VLM benchmark. The predictions from the original CLIP and our improved version are indicated by red and green arrows, respectively. The improved CLIP effectively addresses the original model’s limitations in capturing fine-grained visual details*

### D-Ability 主结果：判别能力保持

与 GenHancer 等重建增强方法不同，DCR 在提升 P-Ability 的同时**未损害判别能力**。在 6 个标准零样本聚类基准上（Table 2），DCR 增强的 OpenAI ViT-L@224 在 CIFAR-10 上保持 **95.6%** 准确率，而 GenHancer 降至 73.7%（Table 6），差距达 21.9%。在 MNIST 上的 t-SNE 可视化（Fig. 5）也定性地展示了 DCR 增强后更好的类间分离性。这验证了理论分析（定理 1 和定理 2）的结论：DCR 损失在预测噪声空间上的对比学习可以同时满足判别性约束（类内/类间散度优化）和重建一致性约束。

![[assets/figures/papers/paper_list_l2517_https_arxiv_org_abs_2603_04803/figures/005_Table_2.jpg]]
*Table 2: Performance of Discriminative Ability (D-Ability) on 6 standard zero-shot clustering benchmarks. Our method achieves better class separability. O-1, M-1, and S-1 separately represent OpenAI CLIP ViT-L@224, MetaCLIP ViT-L@224, and SigLIP ViT-SO@224*

![[assets/figures/papers/paper_list_l2517_https_arxiv_org_abs_2603_04803/figures/012_Table_6.jpg]]
*Table 6: Performance on zero-shot classification and retrieval*

![[assets/figures/papers/paper_list_l2517_https_arxiv_org_abs_2603_04803/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative results of D-Ability on the MNIST benchmark by using the t-SNE method. The improved CLIP achieves better class separability*

### 多模态大模型下游迁移

将 DCR 增强的视觉编码器集成到 LLaVA-1.5 中（Table 3），在多个 MLLM 基准上取得了有竞争力的表现，证明增强后的视觉表示能有效迁移至更复杂的多模态理解任务。

![[assets/figures/papers/paper_list_l2517_https_arxiv_org_abs_2603_04803/figures/008_Table_3.jpg]]
*Table 3: Performance of MLLMs (LLaVA-1.5 [49]) on various benchmarks. The champion and the runner-up are highlighted in bold and underline. Results on NaturalBench follow the setting in [57], which differs from that used in un2CLIP [43], leading to the missing entries*

### 关键消融实验

**训练协议**：两阶段训练策略（Stage-1 冻结编码器训练投影器，Stage-2 冻结投影器用 LoRA 微调编码器）对最终性能至关重要。消融实验（Table 4(b)）显示，端到端联合训练仅能达到 25.93% 的 MMVP-VLM 准确率，而两阶段训练将其提升至 **33.30%**。Stage-1 的对齐过程确保了冻结的去噪器能正确解释基于图像的条件信号，为 Stage-2 的编码器增强提供了稳定的优化基础。

**局部 Token 比例**：在投影器输入中仅使用 [CLS] token（0% local tokens）获得了最佳性能；引入过多局部 token 反而稀释了监督信号强度，导致性能下降（Table 7）。

**扩散骨架选择**：对比 Stable Diffusion v1.4、v1.5、v2.1 和 SD-XL 等不同扩散骨架（Fig. 6），SD v2.1 在 P-Ability 和 D-Ability 的平衡上取得了最佳整体性能。

**训练效率**：DCR 的训练开销相对较低（Table 8），OpenAI ViT-L@224 约需 7.7 小时、53.5 GB 显存，具备良好的可扩展性。

### 局限性

尽管 DCR 在平衡判别能力与细节感知能力上取得了显著成效，但其增强效果仍受限于 CLIP 骨干网络固有的表示容量。当前框架仅基于扩散模型实现，尚未验证在 VAR 等非扩散生成范式上的适用性。此外，两阶段训练协议虽然有效，但增加了工程复杂性；方法对预训练 Stable Diffusion 模型的依赖也引入了额外的存储和部署成本。

### 补充图表

![[assets/figures/papers/paper_list_l2517_https_arxiv_org_abs_2603_04803/figures/009_Figure_6.jpg]]
*Figure 6: Ablation study on different diffusion model structures*

![[assets/figures/papers/paper_list_l2517_https_arxiv_org_abs_2603_04803/figures/014_Table_7.jpg]]
*Table 7: Results under different ratios of local tokens ([CLS] + n% local tokens)*

![[assets/figures/papers/paper_list_l2517_https_arxiv_org_abs_2603_04803/figures/013_Table_8.jpg]]
*Table 8: Training costs of our DCR*



## 定位与知识库关联

### 核心贡献定位

DCR 解决的是 **CLIP 视觉编码器中判别能力（D-Ability）与细节感知能力（P-Ability）的失衡问题**。在方法谱系中，它处于两条技术路线的交汇点：

1. **对比学习路线**：以 CLIP 为代表，通过 InfoNCE 损失在图像-文本对上进行对比预训练，赋予编码器强大的语义判别能力，但缺乏对细粒度视觉细节的敏感性。
2. **扩散重建路线**：以 **DIVA**、**GenHancer**、**un²CLIP** 为代表，利用扩散模型的生成反馈增强视觉编码器的细节感知。然而，这些方法在提升 P-Ability 的同时，会损害编码器原有的 D-Ability。

DCR 的关键创新在于**将对比信号从原始图像空间迁移至扩散模型的预测噪声空间**，用单一损失函数 $ \mathcal{L}_{\mathrm{dcr}} $ 同时优化判别性与重建一致性，从根本上消除了多目标优化中的梯度冲突问题。理论分析（定理 1 和定理 2）进一步证明，$ \mathcal{L}_{\mathrm{dcr}} $ 可以同时满足判别性约束（类内/类间散度优化）和重建一致性约束。

### 与基线方法的关系

| 方法 | 核心机制 | 与 DCR 的关键差异 |
|------|---------|------------------|
| **Original CLIP** | 对比学习，优化 $ \mathcal{L}_{\mathrm{con}} $ | 仅具备 D-Ability，缺乏 P-Ability；DCR 在其基础上增强细节感知而不损害判别能力 |
| **DIVA** | 基于扩散视觉反馈增强细粒度感知 | 使用生成反馈但未引入对比信号，P-Ability 提升有限 |
| **GenHancer** | 在离散潜在空间中扩展重建过程，使用全局条件与轻量去噪器 | 重建机制损害 D-Ability（CIFAR-10 零样本分类降至 73.7%，DCR 保持 95.6%） |
| **un²CLIP** | 逆向生成过程捕捉图像细节，同时保持与 CLIP 嵌入空间对齐 | 同样面临 D-Ability 与 P-Ability 的权衡问题，缺乏统一的优化框架 |

DCR 相较于上述方法的本质优势在于：它不是简单地加权组合两个损失，而是**在噪声预测空间中构造对比三元组**（锚点为原图预测噪声 $ \hat{\epsilon} $，正样本为增强视图的预测噪声和真实噪声，负样本为批次中其他图像的预测噪声），使得同一优化目标天然兼顾两类能力。

### 技术演进脉络

DCR 的设计逻辑可追溯到以下技术脉络：

- **扩散模型作为表示学习工具**：Stable Diffusion 的条件生成框架提供了丰富的视觉先验，DCR 利用其冻结的去噪器 $ \epsilon_\theta $ 作为“感知教师”，通过重建反馈指导编码器学习。
- **对比学习中的正负样本构造**：DCR 继承了 InfoNCE 损失的对比范式，但将样本空间从特征嵌入 $ \mathbf{z} $ 迁移到预测噪声 $ \hat{\epsilon} $，使得对比信号与重建信号在数学上同源。
- **两阶段训练协议**：Stage-1 冻结编码器训练投影器 $ h_\omega $，确保视觉条件与扩散模型的文本条件空间对齐；Stage-2 冻结投影器并用 LoRA 微调编码器。这种策略避免了端到端训练中的优化不稳定（消融实验显示，端到端训练的 MMVP-VLM 准确率仅为 25.93，两阶段训练提升至 33.30）。

### 适用边界与局限

1. **生成范式依赖**：DCR 当前仅基于扩散模型设计，尚未扩展至 VAR 等非扩散生成范式。其核心机制（在预测噪声空间构造对比三元组）是否适用于其他生成模型仍需验证。
2. **外部模型依赖**：训练依赖于预训练的 Stable Diffusion 模型，增加了存储和计算成本（OpenAI ViT-L@224 训练约需 7.7 小时，53.5 GB 显存）。在资源受限场景下，这一依赖可能成为部署瓶颈。
3. **编码器容量上限**：DCR 的增强效果受限于 CLIP 骨干网络固有的表示能力，无法超越其理论基础容量。对于本身容量较小的编码器，增强收益可能有限。
4. **训练协议复杂性**：两阶段训练虽然有效，但增加了工程实现复杂度，且 Stage-1 的投影器对齐质量直接影响 Stage-2 的最终性能。
5. **条件设计的敏感性**：消融实验表明，仅使用 [CLS] token（0% local tokens）获得最佳性能，引入过多局部 token 会降低监督信号强度。这意味着 DCR 对条件输入的设计较为敏感，需要在全局语义与局部细节之间精细权衡。

### 开放问题

1. **跨生成范式的泛化**：如何将扩散对比重建思想扩展到 VAR、GAN 等非扩散生成模型？关键在于找到这些生成框架中与“预测噪声”等价的中间表示空间。
2. **编码器架构的通用性**：DCR 框架能否直接应用于 ViT、ResNet 之外的视觉编码器（如 ConvNeXt、Swin Transformer），形成统一的增强策略？当前实验覆盖了 6 种 CLIP 骨干，但尚未验证非 CLIP 架构。
3. **理论基础的深化**：定理 1 和定理 2 建立了特征空间与噪声空间的散度界限，但基于重建的表示增强方法的根本理论原理仍不清晰。能否建立更严格的泛化保证，或从信息瓶颈角度解释 DCR 的有效性？
4. **对比信号构造的优化**：DCR 损失中的正负样本构造方式是否有更优设计？例如，使用更强的数据增强策略、引入难负样本挖掘、或利用扩散时间步 $ t $ 的调度来调控对比信号的强度。
5. **更大规模多模态模型中的收益**：在 LLaVA-1.5 上的实验已初步验证 DCR 增强编码器对 MLLM 的收益，但在更先进的多模态模型（如 LLaVA-NeXT、Qwen-VL）中，DCR 能带来多大程度的性能提升？这需要更大规模的系统性评估。
6. **训练效率优化**：当前两阶段训练协议增加了训练步骤，能否设计单阶段训练策略（如动态调整投影器与编码器的学习率），在保持性能的同时降低工程复杂度？



## 原文 PDF

![[paperPDFs/CVPR_2026/Guiding_Diffusion_based_Reconstruction_with_Contrastive_Signals_for_Balanced_Visual_Representation.pdf]]
