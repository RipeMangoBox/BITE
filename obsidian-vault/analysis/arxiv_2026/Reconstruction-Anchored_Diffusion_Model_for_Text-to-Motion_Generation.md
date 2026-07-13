---
title: Reconstruction-Anchored Diffusion Model for Text-to-Motion Generation
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/Reconstruction-Anchored_Diffusion_Model_for_Text-to-Motion_Generation.pdf
project_link: null
code_link: null
aliases:
- RADMR
- RADMTMG
tags:
- arxiv_2026
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过运动重建分支学习运动潜在空间作为中间监督，并在推理时利用重建误差引导来放大正确方向。
primary_logic: 将文本嵌入映射到运动中心潜在空间，利用当前预测与重建过去估计的残差作为负参考，引导采样远离错误区域，从而提升运动质量和语义对齐。
claims:
- RAM achieves state-of-the-art FID of 0.032 on HumanML3D, surpassing prior diffusion methods.
- RAM achieves R-Precision Top-1 of 56.1%, significantly higher than MDM.
- Each proposed component (self-regularization, latent alignment, REG) contributes to performance improvement.
- HumanML3D 上 FID = 0.032
---

# Reconstruction-Anchored Diffusion Model for Text-to-Motion Generation

> [!tip] 核心洞察
> 将文本嵌入映射到运动中心潜在空间，利用当前预测与重建过去估计的残差作为负参考，引导采样远离错误区域，从而提升运动质量和语义对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | 用于文本到运动生成的重建锚定扩散模型 |
| 英文题名 | Reconstruction-Anchored Diffusion Model for Text-to-Motion Generation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2601.14788) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Reconstruction-Anchored Diffusion Model (RAM) |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，FID 0.032 vs 0.116 (T2M-GPT) (-0.084)；R-Precision Top1 0.561 vs 0.491 (T2M-GPT) (+0.070)；MMDist 2.716 vs 3.118 (T2M-GPT) (-0.402)。
> - KIT-ML 上，FID 0.172 vs 0.512 (T2M-GPT) (-0.340)；R-Precision Top1 0.464 vs 0.416 (T2M-GPT) (+0.048)；MMDist 2.653 vs 3.007 (T2M-GPT) (-0.354)。

## 概要

文本到运动生成的核心瓶颈在于：预训练的文本编码器缺乏运动特定的语义信息，导致文本嵌入与运动空间之间存在显著的表示差距；同时，扩散模型在迭代去噪过程中会产生误差累积，使生成的运动偏离真实数据流形。针对这一问题，本文提出**重建锚定扩散模型（Reconstruction-Anchored Diffusion Model, RAM）**，通过构建运动重建分支来学习一个运动中心潜在空间，并以此作为中间监督，将文本嵌入映射到该空间中。在推理阶段，RAM利用当前预测与上一步运动重建之间的残差作为负参考，引导采样远离错误区域，从而同时提升运动质量与语义对齐。

RAM在HumanML3D和KIT-ML两个基准数据集上取得了领先性能。在HumanML3D上，RAM的FID达到0.032，R-Precision Top-1达到56.1%，均显著优于此前最优的扩散方法MDM（Tevet et al., arXiv 2022）和VQ-VAE方法T2M-GPT（Zhang et al., CVPR 2023）。消融实验证实，运动重建分支、自正则化损失、运动中心潜在对齐以及重构误差引导（REG）四个组件各自对性能有实质性贡献，且REG与分类器自由引导（CFG）在功能上互补——CFG主要提升语义准确度，REG主要增强运动真实感。

**方法定位**：RAM属于基于扩散的文本到运动生成方法，与MDM共享扩散解码器架构，但通过双流训练范式引入了运动潜在空间学习。相较于Salad（Hong et al., CVPR 2025）等潜在扩散方法，RAM的核心差异在于以运动重建为锚点，在训练和推理两端均利用运动潜在空间进行约束与引导。



文本到运动生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的三维人体运动序列，在虚拟人、影视动画和人机交互等领域具有重要应用价值。该任务的核心挑战在于建立文本语义与人体运动之间的精确映射，这要求模型同时理解语言的抽象语义和运动的高维时空结构。

**现有方法缺口。** 当前主流方法可大致分为两类。基于VQ-VAE的方法（如 **T2M-GPT**，Zhang et al., CVPR 2023）将运动量化为离散编码并通过自回归模型生成，在语义对齐方面表现突出，但其离散表示不可避免地引入量化误差，限制了运动细节的保真度。基于扩散模型的方法（如 **MDM**，Tevet et al., arXiv 2022）直接在原始运动空间进行连续去噪，能够生成更流畅的运动，但存在两个关键瓶颈：

1. **表示差距（Representation Gap）。** 预训练文本编码器（如DistilBERT）提取的文本嵌入缺乏运动特定的语义信息，导致文本条件与运动生成之间的映射不够精确，难以保证语义一致性。
2. **误差传播（Error Propagation）。** 扩散模型的迭代去噪过程中，早期步骤的预测误差会逐步累积并放大，最终损害生成运动的质量和真实性。

**本文动机。** 针对上述瓶颈，本文提出核心洞察：通过引入运动重建作为中间监督，将文本嵌入映射到以运动为中心（motion-centric）的潜在空间，并利用当前预测与上一步重建估计之间的残差作为负参考，引导采样过程远离错误区域。这一思路从两个层面同时解决问题——训练阶段通过学习运动潜在空间来弥合表示差距，推理阶段通过重建误差引导（Reconstructive Error Guidance, REG）来抑制误差传播。基于此，本文设计了**重建锚定扩散模型（Reconstruction-Anchored Diffusion Model, RAM）**，以统一的框架同时提升运动生成的真实感和语义对齐精度。



## 核心方法与创新机理

RAM 的核心创新在于将**运动重建**作为中间监督锚点，系统性地解决文本到运动扩散模型中两个相互交织的瓶颈：预训练文本编码器缺乏运动特定信息导致的表示差距，以及扩散去噪过程中的误差传播。与现有方法直接依赖文本条件生成不同，RAM 通过以下四个相互协同的 **changed slots** 构建了完整的解决方案。

### 1. 运动重构分支：建立运动中心潜在空间

RAM 引入了与文本生成分支并行的**运动重构分支**（`changed_slot: 运动重构分支`），形成双流管道。该分支通过 6 层 transformer 编码器 $E_m$ 将真实运动序列 $x_0$ 编码为运动潜在 $z_m = E_m(s_m, x_0)$，再通过共享的扩散解码器 $D$ 进行重建：

$$L_{rec} = \mathbb{E}_{x_0, t} [\| D(x_t, t, z_m) - x_0 \|_2^2]$$

这一设计的因果机制在于：运动重构分支迫使模型学习一个**运动中心的潜在流形**，该流形天然包含运动特定的语义结构和物理约束。文本生成分支 $z_t = E_t(s_t, f_t)$ 则被引导向该流形对齐，从而弥补预训练文本编码器（DistilBERT）缺乏运动先验的缺陷。消融实验（Table 4）证实，仅添加运动重构分支即可使 FID 从 0.422 大幅降至 0.116，验证了运动中心潜在空间作为中间监督的核心价值。

### 2. 自正则化损失：增强潜在空间语义分辨率

在运动潜在空间上施加**自正则化损失** $L_{sr}$（`changed_slot: 自正则化损失 L_sr`），通过交叉熵形式增强运动表示的类间可分性：

$$L_{sr} = \frac{1}{B} \sum_{i=1}^B -\log \frac{\exp(\text{sim}(\tilde{z}_m^i, \tilde{z}_m^i)/\tau)}{\sum_{j=1}^B \exp(\text{sim}(\tilde{z}_m^i, \tilde{z}_m^j)/\tau)}$$

该损失的作用机制是：在 batch 内拉近同一运动样本的不同增强视图，推远不同样本的表示，从而提升运动潜在空间的**语义分辨率**。这使得相似运动在潜在空间中形成紧致聚类，不同运动类别之间边界清晰，为后续的文本-运动对齐提供了更高质量的目标空间。超参数分析（Table 7）表明，温度 $\tau=1$ 在相似度锐度上取得最佳平衡。

### 3. 运动中心潜在对齐：非对称的跨模态映射

RAM 提出**运动中心潜在对齐** $L_{latent}$（`changed_slot: 运动中心潜在对齐 L_latent`），将文本潜在拉向运动潜在，同时保持运动空间的主导地位：

$$L_{latent} = \mathbb{E}_{z_m, z_t} [\| z_t - (1-\beta) \operatorname{sg}(z_m) - \beta z_m \|_2^2]$$

关键设计在于：对运动潜在 $z_m$ 施加**停止梯度**（$\operatorname{sg}$），仅允许极小的梯度流（$\beta=0.01$）回传至运动编码器。这一非对称策略确保运动潜在空间保持稳定，不被文本模态"污染"，同时文本编码器被强制学习向运动流形投影。Table 6 的对比实验表明，双向对齐或跨模态对比学习虽然能获得可比的语义准确度（R-Precision），但 FID 显著劣于 RAM 的运动中心策略——这证实了**保持运动空间主导性**对于生成真实运动至关重要。

### 4. 重构误差引导：推理阶段的负参考机制

传统扩散模型在推理时仅使用分类器自由引导（CFG），而 RAM 引入了**重构误差引导（REG）**（`changed_slot: 推理策略`），利用上一步运动重建作为负参考：

$$\hat{x}_{t,s} = D(x_t, t, z_t) + w_1 (D(x_t, t, z_t) - D(x_t, t, z_{m,t+1})) + w_2 (D(x_t, t, z_t) - D(x_t, t, \mathcal{O}))$$

REG 的因果机制是：扩散去噪过程中，早期步骤的预测往往包含误差模式。RAM 将上一步预测 $x_{t+1}$ 重新编码为 $z_{m,t+1}$，通过解码器重建出带有误差的运动，然后放大当前预测与该重建的**残差** $(D(x_t, t, z_t) - D(x_t, t, z_{m,t+1}))$。这相当于将重建结果作为"反面教材"，引导采样远离错误区域，向真实数据流形靠拢。

Table 5 的消融揭示了 CFG 与 REG 的功能分工：CFG 主要提升语义准确度（R-Precision），REG 主要提升运动真实感（FID）。二者结合达到最优——CFG 确保运动与文本对齐，REG 抑制去噪过程中的误差累积。Table 3 进一步表明，仅在**早期去噪步骤**（前 5 步）应用 REG 即可获得显著 FID 改善，证实了纠正早期误差对于阻断误差传播链的关键作用。

### 创新点协同总结

四个 changed slots 形成递进式的协同体系：运动重构分支建立运动中心潜在空间（基础层），自正则化增强该空间的语义结构（优化层），运动中心对齐将文本映射到该空间（桥接层），REG 在推理时利用重建作为负参考抑制误差（推理层）。这一完整链条使得 RAM 在 HumanML3D 上取得 FID 0.032、R-Precision Top-1 56.1% 的最优性能，分别超越此前最佳的扩散方法 MDM（Tevet et al., arXiv 2022）和 VQ-VAE 方法 T2M-GPT（Zhang et al., CVPR 2023）。



RAM 采用**双流训练架构**，由运动重建分支和文本驱动生成分支构成，二者共享一个基于 MDM 的运动扩散解码器。其核心设计理念是：在训练阶段学习一个运动中心的潜在空间，使文本嵌入能够准确映射到该空间；在推理阶段，利用重建误差引导（REG）抑制扩散去噪过程中的误差传播。

### 双流训练管线

**运动重建分支**负责学习运动潜在空间。给定真实运动序列 $x_0$，运动编码器 $E_m$（6 层 transformer，结构与 TEMOS 一致）将 $x_0$ 与特殊标记 $s_m$ 一同编码为全局运动潜在向量 $z_m$：

$$z_m = E_m(s_m, x_0)$$

随后，扩散解码器 $D$ 以 $z_m$ 为条件，对加噪后的运动 $x_t$ 进行去噪，预测干净运动 $\hat{x}_t = D(x_t, t, z_m)$，并通过均方误差损失 $L_{rec}$ 进行监督。这一分支使模型学会将运动压缩为紧凑的潜在表示，该表示捕获了运动的语义和动态特征。

**文本驱动生成分支**共享同一个扩散解码器，但以文本潜在 $z_t$ 为条件。文本编码器 $E_t$（同样为 6 层 transformer）接收 DistilBERT 提取的文本嵌入和特殊标记 $s_t$，输出文本潜在 $z_t = E_t(s_t, f_t)$。生成损失 $L_{gen}$ 同样采用均方误差，监督 $D(x_t, t, z_t)$ 对 $x_0$ 的预测。

两个分支的关键区别在于条件信号的来源——$z_m$ 来自真实运动编码，$z_t$ 来自文本编码。训练时，二者并行计算，共享解码器权重，使得解码器学会在统一的潜在条件下生成运动。

### 训练目标与潜在空间约束

在基础重建和生成损失之上，RAM 引入两个关键约束来塑造运动潜在空间：

- **自正则化损失 $L_{sr}$**：在运动潜在空间上施加交叉熵损失，增强不同运动样本潜在表示之间的类间可分性，提升语义分辨率。
- **运动中心潜在对齐损失 $L_{latent}$**：将文本潜在 $z_t$ 拉向对应运动潜在 $z_m$，同时使用停止梯度 $\operatorname{sg}(z_m)$ 和小的梯度控制参数 $\beta$（最优值 0.01），确保运动空间在训练中保持主导地位，避免文本编码器反向传播破坏运动表示。

整体训练目标为加权和：

$$L_{overall} = L_{rec} + L_{gen} + w_{sr} L_{sr} + w_{latent} L_{latent}$$

### 推理时的误差引导机制

推理阶段，RAM 在每个去噪步骤中不仅使用文本条件 $z_t$ 进行预测，还额外利用**上一步预测结果的重建**作为负参考。具体而言，将上一步预测 $\hat{x}_{t+1}$ 通过运动编码器重新编码为 $z_{m,t+1}$，计算当前文本条件预测与重建预测之间的残差，并通过放大该残差来引导当前预测远离上一步的错误模式：

$$\hat{x}_{t,s} = D(x_t, t, z_t) + w_1 (D(x_t, t, z_t) - D(x_t, t, z_{m,t+1}))$$

最终采样公式同时结合 REG 和标准分类器自由引导（CFG）：

$$\hat{x}_{t,s} = D(x_t, t, z_t) + w_1 (D(x_t, t, z_t) - D(x_t, t, z_{m,t+1})) + w_2 (D(x_t, t, z_t) - D(x_t, t, \mathcal{O}))$$

其中 $w_1$ 控制 REG 强度，$w_2$ 控制 CFG 强度，$\mathcal{O}$ 表示无条件输入。消融实验表明，CFG 主要提升语义准确度（R-Precision），而 REG 主要改善运动真实感（FID），二者结合达到最优性能。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2601_14788/figures/002_Figure_2.jpg]]
*Figure 2: Overview of RAM. During training, RAM learns a motion latent space through motion reconstruction, with self-regularization to encourage better separability between motion latents, resulting in improved semantic resolution. The text latents from the text encoder are drawn closer to corresponding motion latents through motion-centric latent alignment. At each inference step, given the last step prediction*



RAM 的核心架构由双流管道、两个关键训练目标和一种推理时引导策略构成，共同解决文本到运动生成中的表示差距与误差传播问题。

### 双流管道：运动重建与文本条件生成

RAM 包含两个共享扩散解码器的分支。**运动重建分支**通过 6 层 transformer 编码器 $E_m$ 将真实运动序列 $x_0$ 映射为运动潜在表示 $z_m$：

$$z_m = E_m(s_m, x_0)$$

其中 $s_m$ 为可学习的特殊标记。**文本条件生成分支**则通过同样结构的文本编码器 $E_t$ 将 DistilBERT 提取的文本嵌入 $f_t$ 映射为文本潜在表示 $z_t$：

$$z_t = E_t(s_t, f_t)$$

两个分支共享一个基于 MDM（Tevet et al., arXiv 2022）的 8 层 transformer 扩散解码器 $D$，根据噪声输入 $x_t$、时间步 $t$ 和条件潜在（$z_m$ 或 $z_t$）预测干净运动。

### 训练目标

**运动重建损失** $L_{rec}$ 与**文本条件生成损失** $L_{gen}$ 均采用均方误差：

$$L_{rec} = \mathbb{E}_{x_0, t} [\| D(x_t, t, z_m) - x_0 \|_2^2]$$

$$L_{gen} = \mathbb{E}_{x_0, t, t} [\| D(x_t, t, z_t) - x_0 \|_2^2]$$

在此基础上，RAM 引入两个关键正则化项。

**自正则化损失 $L_{sr}$** 在运动潜在空间上施加交叉熵损失，增强类间可分性、提升语义分辨率：

$$L_{sr} = \frac{1}{B} \sum_{i=1}^B -\log \frac{\exp(\text{sim}(\tilde{z}_m^i, \tilde{z}_m^i)/\tau)}{\sum_{j=1}^B \exp(\text{sim}(\tilde{z}_m^i, \tilde{z}_m^j)/\tau)}$$

其中 $\tau$ 为温度系数，$\text{sim}$ 为相似度度量。

**运动中心潜在对齐损失 $L_{latent}$** 将文本潜在拉向对应的运动潜在，同时通过停止梯度 $\operatorname{sg}(\cdot)$ 和小权重 $\beta$（默认 0.01）保持运动空间的主导地位：

$$L_{latent} = \mathbb{E}_{z_m, z_t} [\| z_t - (1-\beta) \operatorname{sg}(z_m) - \beta z_m \|_2^2]$$

整体训练目标为加权组合：

$$L_{overall} = L_{rec} + L_{gen} + w_{sr} L_{sr} + w_{latent} L_{latent}$$

### 推理时的重建误差引导（REG）

标准扩散推理仅依赖分类器自由引导（CFG），而 RAM 额外引入**重建误差引导**以缓解迭代去噪中的误差传播。其核心机制是：将上一步预测 $x_{t+1}$ 编码为 $z_{m,t+1}$ 并输入解码器得到重建，计算当前文本条件预测与该重建的残差，放大该残差作为修正方向：

$$\hat{x}_{t,s} = D(x_t, t, z_t) + w_1 (D(x_t, t, z_t) - D(x_t, t, z_{m,t+1})) + w_2 (D(x_t, t, z_t) - D(x_t, t, \mathcal{O}))$$

其中 $w_1$ 控制 REG 强度，$w_2$ 控制 CFG 强度，$\mathcal{O}$ 为空条件输入。消融实验（Table 5）表明：CFG 主要提升语义准确度（R-Precision），REG 主要提升运动真实感（FID），二者结合达到最优。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2601_14788/figures/001_Figure_1.jpg]]
*Figure 1: At inference time, RAM first maps a textual description onto a motion-centric latent manifold and then predicts using a diffusion model. Meanwhile, it reconstructs previous estimates that contain error patterns. By contrasting these predictions, RAM uses the reconstruction as a negative reference to drive the output away from poor estimates and towards the real data manifold. Best viewed in color*



## 实验与关键发现

### 核心瓶颈与因果机制

文本到运动生成面临两个深层瓶颈：**预训练文本编码器（如 DistilBERT）缺乏运动特定信息**，导致文本嵌入与运动数据之间存在显著的表示差距；**扩散模型在迭代去噪过程中存在误差传播**，早期步骤的预测偏差会逐级放大，最终损害生成质量。RAM 通过一个统一的因果机制同时应对这两个问题：构建运动重建分支学习一个**运动中心潜在空间**，将文本嵌入映射到该空间作为中间监督，并在推理时利用当前预测与上一步重建估计的残差作为**负参考信号**，引导采样远离错误区域。

### 主实验结果

**HumanML3D 基准**（Table 1）上，RAM 取得了扩散方法中最优的 FID（0.032），显著优于 **MDM**（Tevet et al., arXiv 2022）和 **T2M-GPT**（Zhang et al., CVPR 2023）等基线。语义对齐指标 R-Precision Top-1 达到 56.1%，较 T2M-GPT 提升 7.0 个百分点；MMDist 降至 2.716，表明生成运动与文本描述的语义距离更小。

**KIT-ML 基准**（Table 2）上，该数据集规模更小、挑战性更高，RAM 在扩散方法中取得了最均衡的表现：FID 为 0.172，R-Precision Top-1 为 46.4%，MMDist 为 2.653。RAM 在 FID 上大幅优于 R-Precision 领先者 **Salad**（Hong et al., CVPR 2025），同时在 R-Precision 上显著优于 FID 领先者 ReMoDiffuse，体现了质量与语义对齐的兼顾能力。

### 消融实验

**增量组件消融**（Table 4）验证了各模块的因果贡献。从纯文本条件扩散基线（FID 0.422）出发，逐步添加运动编码器、潜在对齐损失 $L_{latent}$ 和自正则化损失 $L_{sr}$，FID 逐步降至 0.032。每个组件单独移除均导致性能显著退化，证实了运动重建分支作为中间监督、潜在空间可分性增强和文本-运动空间对齐三者缺一不可。

**REG 与 CFG 的作用分解**（Table 5）揭示了两个引导机制的功能分化：CFG（$w_2$）主要提升语义准确度（R-Precision），而 REG（$w_1$）主要增强运动真实感（FID）。两者结合达到最优，表明语义引导和质量纠偏是互补而非替代关系。

**推理效率实验**（Table 3）表明，RAM 在 20 步去噪下平均推理时间低于 MDM 的 50 步配置，即使启用 REG 仍保持效率优势。仅在前几步应用 REG 即可显著改善 FID，证实了**早期去噪步骤的误差纠偏对抑制误差传播至关重要**。

**超参数分析**（Table 7）显示，潜在对齐中的梯度控制参数 $\beta=0.01$ 表现最优——过大的 $\beta$（如 1.0）会因无限制的梯度流破坏运动空间结构，导致性能退化。自正则化温度 $\tau=1$ 在相似度锐度与可分性之间取得理想平衡。

**损失权重消融**（Table 8）表明，模型对 $w_{sr}$ 和 $w_{latent}$ 的具体取值具有一定鲁棒性，但任一项置零均导致严重性能下降，再次确认两个辅助目标的必要性。

**编码器潜在维度**（Table 9）实验显示 $d_E=256$ 取得最优 FID，但即使降至 128 仍保持竞争力，说明学习到的运动潜在空间具有高度紧凑性。

### 失败模式与局限

尽管 RAM 在高质量动捕数据集上表现优异，但存在以下局限：

1. **数据鲁棒性未验证**：所有实验基于 HumanML3D 和 KIT-ML 这两个高质量动捕数据集，未在噪声较大的伪标记数据（如基于视频的动作重建）上进行评估，对低质量输入的泛化能力未知。
2. **REG 的计算开销**：REG 在推理时需额外执行一次重建解码，增加了计算负担。虽然仅在前几步应用可缓解此问题，但需要手动选择去噪步数，限制了实时应用场景的灵活性。
3. **复杂动作的语义覆盖不足**：定性评估（Figure 3）显示，当文本描述包含多个连续动作时（如“walk, bend down, pick up, and throw”），RAM 能完成三个动作，而基线方法通常仅完成一至两个，但仍未完全覆盖所有语义指令，表明长序列多动作的语义对齐仍是开放挑战。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2601_14788/figures/012_Figure_3.jpg]]
*Figure 3: Qualitative evaluation on the HumanML3D Dataset. Actions corresponding to the text are highlighted with green dashed lines, while unnatural artifacts are indicated with red dashed lines. It can be observed that baseline methods often fail to faithfully execute the entire set of actions described in the text. For example, in the second row (“a person walks up and tosses something”), most methods only execute the walking motion. Some outputs also exhibit distortions, such as unnatural drifting (in the third row, MoMask during sitting down and Salad during standing up) and error patterns (in the first row, MoMask’s hands move erratically up and down after completing the “drink” action). The fo...*

### 用户调研

Figure 4 的用户调研以运动质量和语义对齐两个维度进行综合排序，RAM 在所有对比方法中获得最佳整体评价，与定量指标的趋势一致。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2601_14788/figures/013_Figure_4.jpg]]
*Figure 4: User study results on the HumanML3D test set comparing RAM with state-of-the-art methods. We conducted a perceptual study to evaluate human preferences based on a holistic assessment of two key dimensions: motion quality and semantic alignment. Participants were instructed to rank the generated motions from different methods by jointly considering these factors. The results indicate that RAM achieves the best overall performance, demonstrating its superior capability in generating motions that are both realistic and semantically accurate*

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2601_14788/figures/006_Table_4.jpg]]
*Table 4: Incremental ablation experiments on the key components of RAM. We evaluate the impact of the motion reconstruction branch, Self-Regularization*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2601_14788/figures/007_Table_5.jpg]]
*Table 5: Effect of Reconstructive Error Guidance (REG) and classifier-free guidance (CFG). w1 and w2 respectively control the influence of REG and CFG. The results demonstrate that CFG substantially improves semantic accuracy (higher R-Precision), while REG notably enhances motion realism (lower FID). Furthermore, combining both strategies enables RAM to achieve state-of-the-art performance*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2601_14788/figures/004_Table_2.jpg]]
*Table 2: Quantitative results of text-to-motion generation on the KIT-ML test set. Methods are grouped into VQ-VAE-based and diffusion-based categories. In each group, the best results are highlighted in bold, while the second-best results are underlined. Notably, on this challenging, smaller dataset, RAM achieves the most balanced performance among diffusion models, ranking second in both FID and R-Precision. It substantially outperforms the FID leader (ReMoDiffuse) in R-Precision and the R-Precision leader (Salad) in FID*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2601_14788/figures/009_Table_7.jpg]]
*Table 7: Effect of loss parameters β and τ. We study the gradient control parameter β in latent alignment and the temperature τ in self-regularization. A small β (e.g., 0.01) yields the best performance by preserving essential motion information, while unrestricted flow*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2601_14788/figures/010_Table_8.jpg]]
*Table 8: Effect of loss weights. We evaluate the impact of varying the weights for the self-regularization*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2601_14788/figures/011_Table_9.jpg]]
*Table 9: Effect of encoder latent dimension*



## 定位与知识库关联

### 1. 在文本-运动生成谱系中的位置

当前文本-运动生成方法大致分为两类：基于VQ-VAE的离散标记方法和基于扩散模型的连续生成方法。RAM属于后者，但通过引入运动重建分支，在方法论上架起了一座连接两类路线的桥梁。

**与扩散基线的关系**：最直接的参照是 **MDM**（Tevet et al., arXiv 2022），它采用原始运动空间上的扩散去噪，依赖预训练文本编码器提供条件信号。RAM继承了MDM的扩散解码器架构（8层transformer），但关键差异在于：MDM的文本条件直接注入去噪过程，缺乏运动特定的中间表示；RAM则通过双流架构将文本嵌入映射到运动中心潜在空间，从而缓解了预训练文本编码器与运动域之间的表示差距。

**与VQ-VAE路线的对比**：**T2M-GPT**（Zhang et al., CVPR 2023）将运动量化为离散标记并采用GPT式自回归生成，在语义对齐上表现突出（HumanML3D上R-Precision Top-1达0.491）。RAM在保持扩散模型连续生成优势的同时，通过自正则化损失$L_{sr}$强化运动潜在空间的类间可分性，使其语义分辨率逼近甚至超越了离散标记方法——R-Precision Top-1达到0.561，相比T2M-GPT提升7个百分点。

**与潜在扩散方法的比较**：**Salad**（Hong et al., CVPR 2025）同样采用潜在空间扩散，但在KIT-ML上呈现出FID与R-Precision的跷跷板效应——虽在R-Precision上领先，FID却显著劣于RAM（RAM的0.172 vs Salad的更高值）。RAM通过运动中心潜在对齐$L_{latent}$（带停止梯度和小$\beta=0.01$）实现了更均衡的质量-语义权衡，在KIT-ML上成为扩散方法中综合表现最均衡的模型。

### 2. 核心机制的知识贡献

RAM的知识增量可分解为三个相互耦合的机制，每个都针对一个明确的瓶颈：

**瓶颈1：表示差距**。预训练文本编码器（DistilBERT）缺乏运动特定信息，导致文本潜在与运动潜在之间存在语义鸿沟。RAM的解决方案是**运动中心潜在对齐**（Eq. 8）：
$$L_{latent} = \mathbb{E}_{z_m, z_t} [\| z_t - (1-\beta) \operatorname{sg}(z_m) - \beta z_m \|_2^2]$$
该设计的关键在于停止梯度$\operatorname{sg}(z_m)$和非对称的小$\beta$：文本潜在被拉向运动潜在，但运动编码器仅接收极微弱的梯度信号（$\beta=0.01$），从而保持运动空间的主导地位。消融实验（Table 7）证实，$\beta=1.0$（无限制梯度流）会导致性能退化，验证了非对称设计的必要性。

**瓶颈2：语义分辨率不足**。运动潜在空间若缺乏显式的判别性约束，会导致不同语义的运动表示高度重叠。RAM引入**自正则化损失$L_{sr}$**（Eq. 7），在运动潜在空间上施加交叉熵损失，增强类间可分性。增量消融（Table 4）显示，在已有运动重建分支的基础上添加$L_{sr}$，使FID从0.422降至0.032，贡献显著。

**瓶颈3：扩散去噪中的误差传播**。标准扩散模型在推理时逐步去噪，早期步骤的预测误差会累积并放大。RAM的**重建误差引导（REG）**（Eq. 10）利用上一步的运动重建作为负参考：
$$\hat{x}_{t,s} = D(x_t, t, z_t) + w ( D(x_t, t, z_t) - D(x_t, t, z_{m,t+1}) )$$
其直觉是：上一步的预测$\hat{x}_{t+1}$经运动编码器重新编码为$z_{m,t+1}$后，解码得到的重建包含了该步的误差模式；通过放大当前预测与该重建的残差，采样被推离错误区域。Table 5表明，REG主要提升运动真实感（FID），而CFG主要提升语义准确度（R-Precision），二者互补。

### 3. 适用边界与局限

**数据依赖性**：RAM的训练和评估完全基于高质量运动捕捉数据集（HumanML3D、KIT-ML）。这些数据由光学动捕系统采集，噪声低、动作类型规范。论文未在噪声较大的伪标记数据（如基于视频的姿势估计结果）上验证，因此对低质量输入的鲁棒性未知。

**推理效率的权衡**：REG在推理时增加了额外的重建计算——每步需要将上一步预测重新编码为$z_{m,t+1}$并再次解码。Table 3显示，即使仅在早期去噪步骤应用REG（前几步），仍能显著改善FID，但需要手动选择应用步数，限制了实时场景的灵活性。完整的REG+CFG配置下，20步推理的平均时间仍优于MDM的50步推理，但这是通过减少总步数换取的。

**运动长度与复杂度**：论文主要在单人、中等长度（HumanML3D平均约4秒）的运动上验证。Figure 3的定性结果显示，对于包含四个动作的复杂描述（第四行），RAM完成了三个，而基线方法仅完成一到两个，但仍未完全执行所有动作。该方法能否扩展到多人交互或长序列生成，尚待验证。

### 4. 开放问题

1. **噪声鲁棒性**：当输入文本对应的伪标记运动（如视频重建结果）包含显著噪声时，运动重建分支学到的潜在空间是否会退化？自正则化能否在低质量数据上维持判别性？

2. **REG的全步应用**：Table 3表明仅在早期步骤应用REG即可获得大部分收益，但能否通过优化重建编码-解码的计算效率，实现所有去噪步骤的REG而不显著增加推理时间？

3. **多模态扩展**：运动中心潜在对齐的设计假设文本和运动共享一个以运动为主导的潜在流形。对于音乐-舞蹈生成或语音-手势生成等其他跨模态运动任务，这种非对称对齐策略是否同样有效？

4. **长序列生成**：当前架构的transformer编码器-解码器受限于注意力机制的二次复杂度。对于分钟级运动序列，运动潜在空间的压缩能力（Table 9显示$d_E=128$仍保持竞争力）是否足以支持高效的长程生成？



## 原文 PDF

![[paperPDFs/arxiv_2026/Reconstruction-Anchored_Diffusion_Model_for_Text-to-Motion_Generation.pdf]]
