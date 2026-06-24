---
title: ARDHOI Auto Regressive Diffusion for Generating 3D Human Object Interactions
type: paper
paper_level: A
venue: AAAI
year: 2025
pdf_ref: paperPDFs/AAAI_2025/ARDHOI_Auto_Regressive_Diffusion_for_Generating_3D_Human_Object_Interactions.pdf
aliases:
- AARDG3HOI
tags:
- AAAI_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 使用对比变分自编码器（cVAE）在连续潜在空间中学习具备物理意识的 HOI token，并通过自回归扩散模型（ARDM）在连续空间中进行 teacher-forcing 预测，从而保证长序列的一致性和物理可行性。
primary_logic: 在连续潜在空间中引入对比学习，显式扩大合理交互与不合理交互之间的边界，使自回归生成的误差不易漂移到不可行区域；同时用 Mamba 上下文编码和 MLP 降噪器高效利用历史信息，实现速度快且质量高的 HOI 合成。
claims:
- 在 OMOMO 数据集上，FID 相对最强基线 HOI-Diff 降低 23%
- 移除 cVAE 中的 triplet 对比损失使 FID 从 0.826 升至 0.948
- 用 Transformer 上下文编码器替换 Mamba 使 FID 升至 0.979，MLP 降噪器替换为 Transformer 降噪器使 FID 升至 0.902
- OMOMO 上 FID ↓ = 0.826
---

# ARDHOI Auto Regressive Diffusion for Generating 3D Human Object Interactions

> [!tip] 核心洞察
> 在连续潜在空间中引入对比学习，显式扩大合理交互与不合理交互之间的边界，使自回归生成的误差不易漂移到不可行区域；同时用 Mamba 上下文编码和 MLP 降噪器高效利用历史信息，实现速度快且质量高的 HOI 合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | ARDHOI：面向三维人物交互生成的自动回归扩散模型 |
| 英文题名 | ARDHOI Auto Regressive Diffusion for Generating 3D Human Object Interactions |
| 会议/期刊 | AAAI 2025 |
| Links | [Code](https://github.com/gengzichen/ARDHOI) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ARDHOI |
| Dataset | OMOMO, BEHAVE |

> [!tip] 效果简介
> - OMOMO 上，FID ↓ 0.826 vs HOI-Diff (相对降低 23% FID 误差) (-23% FID error)；AITS (秒) 1.25 vs 显著快于 THOR 等扩散方法 (最快推理)。
> - BEHAVE 上，FID ↓ 1.872 vs 优于现有方法（如 THOR） (N/A)。

## 概述

三维人-物交互（Human-Object Interaction, HOI）生成的核心瓶颈在于：长序列生成中交互一致性难以维持，且基于离散 tokenization（如 VQ-VAE）的方法在小样本 HOI 数据集上泛化能力不足，难以建模物理接触的合理性。针对这一问题，ARDHOI 提出了一套“连续潜在空间 + 自回归扩散”的解决方案。

**核心思路**：ARDHOI 采用两阶段框架。第一阶段，通过对比变分自编码器（cVAE）在连续潜在空间中学习具备物理意识的 HOI token——利用对比学习显式扩大合理交互与不合理交互之间的边界，使生成不易漂移到不可行区域；第二阶段，使用自回归扩散模型（ARDM）在连续 token 空间中进行 teacher-forcing 预测，配合 Mamba 上下文编码器和 MLP 降噪器，高效利用历史信息，保证长序列的一致性与物理可行性。

**主要结果**：在 OMOMO 数据集上，ARDHOI 的 FID 达到 0.826，相对最强基线 HOI-Diff 实现 23% 的 FID 误差降低；在 BEHAVE 数据集上 FID 为 1.872，优于现有方法。同时，ARDHOI 的推理时间仅为 1.25 秒，显著快于其他扩散方法。消融实验表明，cVAE 中的 triplet 对比损失、Mamba 上下文编码器和 MLP 降噪器均为关键设计——移除任一组件的导致 FID 显著上升至 0.948、0.979 和 0.902。

## 背景与动机

三维人物交互（3D Human‑Object Interaction, HOI）生成旨在合成人与物体在三维空间中协调运动的序列，是计算机视觉与图形学交叉领域的关键问题，支撑着虚拟人仿真、具身智能训练和 AR/VR 体验等应用。然而，**长序列 HOI 生成面临交互一致性难以维持的根本瓶颈**：模型需要在长达数秒甚至数十秒的时间跨度内，同时保持人体运动自然性、物体运动合理性与两者之间物理接触的准确性。

现有方法在应对这一挑战时存在两个层面的结构性缺口。

**在表示层面**，当前主流范式依赖离散 tokenization（如 VQ‑VAE）将运动序列压缩为离散码本，再通过自回归 Transformer（如 T2M‑GPT）逐 token 预测。这一策略在纯人体运动生成中取得了成功，但在 HOI 场景下暴露出根本性缺陷：HOI 数据集规模远小于纯运动数据集（如 OMOMO 仅数千条序列），离散码本的有限容量在数据稀疏时泛化能力严重不足，且离散量化过程天然难以捕捉物理接触的连续性和精细度。

**在生成范式层面**，现有 HOI 生成方法可归为两类。一类是将文本到运动（Text‑to‑Motion）模型直接适配到 HOI 场景，如 **MDM**（Tevet et al., ICLR 2023），但这类方法未显式建模人物交互，导致物体运动出现强烈扰动（strong perturbations）。另一类是专门设计的 HOI 生成模型，如 **InterDiff**（Xu et al., ICCV 2023）、**HOI‑Diff**（Peng et al., arXiv 2023）和 **THOR**（Wu et al., arXiv 2024），它们虽引入了交互建模，但定性分析显示其生成结果存在“粘手”（stick‑to‑hand）运动模式，且全局朝向控制不佳导致穿透（penetration）等物理不合理现象。这些问题的根源在于：缺乏一个能够显式区分合理与不合理交互的表示空间，使得生成过程中的误差累积容易漂移到不可行区域。

本文的动机由此明确：**构建一个在连续潜在空间中学习、具备物理意识的 HOI 表示，并在该空间中执行自回归扩散生成，以同时解决离散 tokenization 的泛化瓶颈和长序列生成中的一致性漂移问题**。核心假设是，通过对比学习在连续潜在空间中显式扩大合理交互与不合理交互之间的边界，可以构成一个“安全生成区域”，使自回归扩散的每一步预测都不易偏离物理可行性。

## 核心创新

ARDHOI 的核心创新在于将**连续潜在空间中的对比学习**与**自回归扩散生成**相结合，系统性地解决了长序列人-物交互（HOI）生成中交互一致性难以维持的瓶颈。与现有方法相比，ARDHOI 在三个关键设计槽位上做出了根本性的改变：

### 1. 连续对比 Tokenization 替代离散 VQ-VAE

现有方法（如 T2M-GPT 系列）普遍采用 VQ-VAE 将运动序列离散化为有限码本中的 token，但在小样本 HOI 数据集上，离散 tokenization 泛化能力不足，且难以建模物理接触的合理性。ARDHOI 提出 **cVAE（Contrastive Variational Autoencoder）**，在连续潜在空间中学习具备物理意识的 HOI token。其关键机制是：

- **Triplet 对比损失**：通过向物体平移添加微小随机偏移构造正/负样本，显式扩大合理交互与不合理交互之间的边界。该损失使锚点样本与正样本（物理合理的交互）在潜在空间中靠近，同时将负样本推远，公式为：

  $$\mathcal{L}_{tri} = \max(||s_i - s_{i,p}||_2 - ||s_i - s_{i,n}||_2 + \alpha, 0)$$

- **物理约束损失**：在重建目标之外，额外引入前向运动学（FK）、关节速度、物体速度和接触损失，使解码结果在物理上更可行：

  $$\mathcal{L}_{phy} = \lambda_{fk}\mathcal{L}_{fk} + \lambda_{vel}\mathcal{L}_{vel} + \lambda_{ovel}\mathcal{L}_{ovel} + \lambda_{con}\mathcal{L}_{con}$$

消融实验提供了决定性证据：移除 triplet 损失后，OMOMO 数据集上的 FID 从 0.826 升至 0.948（Table 6），且 PCA 可视化（Figure 5）显示无 triplet 损失时正负样本在潜在空间中严重混杂，验证了对比学习对构建合理 token 空间的关键作用。

### 2. Mamba 上下文编码器替代 Transformer

在自回归生成范式中，历史 token 的上下文编码质量直接影响后续预测的准确性。ARDHOI 采用 **Mamba 上下文编码器**替代传统的 Transformer Encoder。Table 6 的消融表明，将 Mamba 替换为 Transformer 上下文编码器后，FID 从 0.826 恶化至 0.979，说明 Mamba 的选择性状态空间机制在捕获 HOI 序列的时序依赖上具有显著优势。

### 3. MLP 降噪器替代 Transformer 降噪器

在自回归扩散的去噪环节，ARDHOI 采用简洁的 **MLP 降噪器**而非 Transformer Decoder（交叉注意力）。Table 6 显示，使用 Transformer 降噪器会使 FID 升至 0.902，而 MLP 降噪器保持了 0.826 的 FID。这一反直觉的结果表明，在 teacher-forcing 的自回归范式下，过于复杂的交叉注意力机制可能引入过拟合或训练不稳定，而 MLP 的简单性反而带来了更好的泛化能力。同时，用单步 MSE 回归替代扩散过程（L2 Loss）导致 FID 急剧恶化至 1.288，验证了扩散去噪过程本身对生成质量的重要性。

### 创新总结

上述三个 changed slots 形成了一个协同体系：cVAE 在连续空间中构建了物理合理且边界清晰的 token 表示，Mamba 高效编码历史上下文，MLP 降噪器稳定地执行扩散去噪。这一组合使 ARDHOI 在 OMOMO 数据集上实现了 FID 0.826，相对最强基线 **HOI-Diff**（Peng et al., arXiv 2023）降低 23% 的 FID 误差，同时推理速度达到 1.25 秒/序列，显著快于 **THOR**（Wu et al., arXiv 2024）等扩散方法。

## 整体框架

ARDHOI 采用**两阶段训练范式**，将长序列人-物交互生成分解为“连续潜在空间学习”与“自回归扩散生成”两个解耦的子问题（Figure 2）。

![[assets/figures/papers/paper_list_l1662_ARDHOI_Auto_Regressive_Diffusion_for_Generating_3D_Human_Object_Interact/figures/002_Figure_2.jpg]]
*Figure 2: ARDHOI. The left model is our Contrastive VAE (cVAE) which learns continuous HOI tokens in a contrastive manner. It is trained in phase 1 and frozen in phase 2. The right part is the ARDM, which generates HOI tokens in an autoregressive style using diffusion. ARDM is trained in phase 2*

**第一阶段：对比变分自编码器（cVAE）学习物理感知的连续 HOI Token。**
原始 HOI 序列被切分为固定长度的片段（每段 16 帧），cVAE 编码器将每个片段映射为连续潜在空间中的一个 token。该阶段的核心目标是学习一个**物理可行且语义可分的连续 token 空间**——通过引入对比学习（triplet loss）显式扩大合理交互与不合理交互之间的边界，同时辅以前向运动学、关节速度、物体速度和接触约束等物理损失，确保重建结果满足基本的物理合理性。cVAE 训练完成后被冻结，不再参与后续生成阶段的参数更新。

**第二阶段：自回归扩散模型（ARDM）在连续 token 空间中进行序列生成。**
ARDM 以自回归方式逐 token 预测完整 HOI 序列：在每个时间步，**Mamba 上下文编码器**将已生成的前序 tokens（$s_{1:i-1}$）与文本条件、物体点云等条件信息融合为上下文表征；随后，**MLP 降噪器**以该上下文和扩散时间步为条件，通过去噪过程生成下一个 token $s_i$。这一“上下文编码 → 扩散去噪 → 预测下一 token”的循环不断推进，直至生成完整的 HOI 序列。训练时采用 teacher-forcing 策略，以真实历史 tokens 作为上下文；推理时则使用已生成的 tokens 逐步扩展序列。

**输入输出流总结：**
- **输入**：文本描述（经 CLIP ViT-B/32 编码）、物体点云、可选的初始人体姿态与物体位姿。
- **第一阶段输出**：冻结的 cVAE 编码器/解码器，以及物理感知的连续 token 表示。
- **第二阶段输出**：完整的 HOI 运动序列（人体关节旋转与物体 6D 位姿），可直接通过 cVAE 解码器还原为原始运动表示。

**关键设计选择背后的因果逻辑：**
连续 token 空间的选择直接回应了离散 tokenization（如 VQ-VAE）在小样本 HOI 数据集上泛化不足的瓶颈——连续表示保留了更丰富的运动信息，使自回归生成的误差不易漂移到不可行区域。Mamba 上下文编码器与 MLP 降噪器的组合则是在自回归范式下经过消融验证的高效架构选择：Mamba 对长序列上下文建模的能力优于同参数量的 Transformer 编码器（Table 6，FID 0.826 vs 0.979），而 MLP 降噪器在 teacher-forcing 训练场景下比基于交叉注意力的 Transformer 降噪器更稳定（FID 0.826 vs 0.902）。

## 核心模块与公式推导

ARDHOI 采用两阶段训练范式：第一阶段训练对比变分自编码器（cVAE）学习连续 HOI token 空间，第二阶段训练自回归扩散模型（ARDM）在该空间中进行序列生成。两个阶段的核心模块与关键公式如下。

### 第一阶段：对比变分自编码器（cVAE）

cVAE 将 16 帧 HOI 片段编码为连续潜在 token，其核心创新在于通过对比学习显式扩大合理交互与不合理交互之间的边界。正负样本的构造方式为：对物体平移添加小幅随机偏移，偏移后的交互被视为负样本，原始交互作为锚点，另一段来自同一动作类别的交互作为正样本。

**Triplet 对比损失**（Equation 1）是 cVAE 的关键设计，确保正样本在潜在空间中比负样本更靠近锚点：

$$\mathcal{L}_{tri} = \max(||s_i - s_{i,p}||_2 - ||s_i - s_{i,n}||_2 + \alpha, 0)$$

其中 $s_i$ 为锚点 token，$s_{i,p}$ 为正样本 token，$s_{i,n}$ 为负样本 token，$\alpha$ 为间隔超参数。该损失在消融实验中被证明至关重要——移除后 FID 从 0.826 升至 0.948（Table 6），PCA 可视化（Figure 5）也证实 triplet loss 使正负样本在潜在空间中明显分离。

![[assets/figures/papers/paper_list_l1662_ARDHOI_Auto_Regressive_Diffusion_for_Generating_3D_Human_Object_Interact/figures/009_Figure_5.jpg]]
*Figure 5: Comparison of PCA plots for HOI positive and negative examples. The plot right is with triplet loss and the plot left is without triplet loss*

**重建损失**（Equation 2）为标准的 L2 损失：

$$\mathcal{L}_{rec} = \frac{1}{K} \sum_{i=1}^{K} ||\mathbf{x}_i - \hat{\mathbf{x}}_i||_2$$

其中 $K$ 为 token 数量，$\mathbf{x}_i$ 为原始 HOI 片段，$\hat{\mathbf{x}}_i$ 为解码器重建结果。

**KL 散度损失**（Equation 3）强制潜在空间紧凑：

$$\mathcal{L}_{kl} = \sum_{i=1}^{K} \sum_{j=1}^{d_l} (\sigma_{i,j}^2 + \mu_{i,j}^2 - 1 - \log \sigma_{i,j}^2)$$

其中 $\mu_{i,j}$ 和 $\sigma_{i,j}$ 分别为编码器输出的第 $i$ 个 token 第 $j$ 维的均值和标准差，$d_l$ 为潜在维度。

**物理约束损失**（Equation 4）进一步增强重建结果的物理合理性：

$$\mathcal{L}_{phy} = \lambda_{fk} \mathcal{L}_{fk} + \lambda_{vel} \mathcal{L}_{vel} + \lambda_{ovel} \mathcal{L}_{ovel} + \lambda_{con} \mathcal{L}_{con}$$

四项分别对应前向运动学损失、关节速度损失、物体速度损失和接触损失，$\lambda$ 为各项权重。

**cVAE 总损失**（Equation 5）为上述各项的加权和：

$$\mathcal{L}_{cVAE} = \mathcal{L}_{rec} + \lambda_{tri} \mathcal{L}_{tri} + \lambda_{kl} \mathcal{L}_{kl} + \lambda_{phy} \mathcal{L}_{phy}$$

cVAE 在第一阶段训练完成后冻结，其编码器用于将 HOI 序列转换为 token 序列，供第二阶段使用。

### 第二阶段：自回归扩散模型（ARDM）

ARDM 在连续 token 空间中以自回归方式生成序列，其对数似然分解为（Equation 6）：

$$\log p_{\theta}(s) = \sum_{i=1}^{K} \log p_{\theta}(s_i | s_{1:i-1})$$

其中 $s = \{s_1, s_2, ..., s_K\}$ 为 token 序列，每个 token 的条件分布由扩散模型建模。

**ARDM 训练损失**为去噪预测的均方误差：

$$\mathcal{L}_{ar} = \frac{1}{K} \sum_{i=1}^{K} ||s_i^t - \hat{s}_i(t, c_i)||_2$$

其中 $s_i^t$ 为第 $i$ 个 token 在扩散时间步 $t$ 的加噪版本，$\hat{s}_i(t, c_i)$ 为降噪器基于上下文 $c_i$ 的预测。

**上下文编码器**采用 Mamba 架构对前序 tokens 和条件进行编码，消融实验（Table 6）表明替换为 Transformer 编码器后 FID 从 0.826 升至 0.979，验证了 Mamba 在长序列上下文建模中的优势。

**MLP 降噪器**（Figure 3）接收上下文编码和扩散时间步，直接预测下一个 token。消融实验显示，将 MLP 降噪器替换为 Transformer Decoder（交叉注意力）后 FID 升至 0.902，说明在自回归扩散范式下 MLP 降噪器更为高效。此外，将扩散过程替换为单步 MSE 回归后 FID 飙升至 1.288，证实了扩散过程对生成质量的必要性。

**无分类器引导**（Classifier-Free Guidance）在推理时组合文本条件和空条件预测：

$$\hat{s}_i^t = \xi \hat{s}_i(z_t, t, c_i) + (1 - \xi) \hat{s}_i(z_t, t, c_{i,\emptyset})$$

其中 $\xi$ 为引导强度，$c_i$ 为文本条件，$c_{i,\emptyset}$ 为空条件。该机制在训练时通过随机丢弃文本条件实现，推理时无需额外分类器。

### 补充图表

![[assets/figures/papers/paper_list_l1662_ARDHOI_Auto_Regressive_Diffusion_for_Generating_3D_Human_Object_Interact/figures/003_Figure_3.jpg]]
*Figure 3: MLP Denoiser and autoregressive denoising*

## 实验与分析

### 主实验结果

ARDHOI 在 OMOMO 和 BEHAVE 两个数据集上均取得了最优的生成质量与推理速度。

在 OMOMO 数据集上，ARDHOI 的 FID 达到 **0.826**，相比最强基线 **HOI-Diff**（Peng et al., arXiv 2023）实现了 **23% 的 FID 误差降低**。同时，R-precision top-1 达到 **0.628**，表明生成的动作序列与文本描述之间具有更强的语义对齐能力。定性对比（Figure 4）显示，**MDM**（Tevet et al., ICLR 2023）生成的序列存在明显的抖动扰动，**InterDiff**（Xu et al., ICCV 2023）与 HOI-Diff 则表现出“手粘物体”的不自然模式，且全局朝向控制不佳导致穿透现象；ARDHOI 在这些方面均有显著改善。

![[assets/figures/papers/paper_list_l1662_ARDHOI_Auto_Regressive_Diffusion_for_Generating_3D_Human_Object_Interact/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison with current models. MDM shows strong perturbations. InterDiff and HOI-Diff present a stick-to-hand motion pattern. And their global orientation is not well controlled which leads to penetration*

在 BEHAVE 数据集上，ARDHOI 取得 FID **1.872**，优于现有方法（如 **THOR**，Wu et al., arXiv 2024）。

在条件生成设置下（文本 + 物体点云 + 初始状态），ARDHOI 的 FID 进一步降至 **0.730**，R-precision top-1 升至 **0.668**（Table 4），验证了模型在多模态条件输入下的鲁棒性。

![[assets/figures/papers/paper_list_l1662_ARDHOI_Auto_Regressive_Diffusion_for_Generating_3D_Human_Object_Interact/figures/007_Table_4.jpg]]
*Table 4: Generation results on OMOMO dataset conditioned on text, objects, and initial states*

推理速度方面，ARDHOI 的平均推理时间（AITS）仅为 **1.25 秒**，显著快于 THOR 等扩散方法（Table 3），这得益于自回归扩散范式避免了全序列迭代去噪的高昂开销。

### 消融实验

消融实验（Table 6）系统验证了各核心组件的贡献：

![[assets/figures/papers/paper_list_l1662_ARDHOI_Auto_Regressive_Diffusion_for_Generating_3D_Human_Object_Interact/figures/010_Table_6.jpg]]
*Table 6: Ablation study. The first row w.o. triplet loss removes the triplet loss in the cVAE. The TRM Context Encoder replaces the Mamba blocks with Transformer Encoder Blocks. The TRM Denoiser replaces the MLP denoiser with a Transformer Decoder (cross-attention). The L2 Loss replaces the denoise process and explicitly predicts the next token with MSE loss in one step*

**cVAE 中 triplet 对比损失的关键性**：移除 triplet 损失后，FID 从 0.826 急剧上升至 **0.948**，表明对比学习对于构建物理合理的 HOI token 空间至关重要。PCA 可视化（Figure 5）进一步佐证：无 triplet loss 时，正负样本在潜在空间中高度混杂；加入 triplet loss 后，正负样本之间形成了清晰的决策边界。

**Mamba 上下文编码器的优势**：将 Mamba 替换为 Transformer 编码器后，FID 升至 **0.979**，性能大幅退化。这说明 Mamba 的状态空间模型在捕捉长序列 HOI 的上下文依赖关系上比 Transformer 更有效。

**MLP 降噪器的适配性**：用 Transformer Decoder（交叉注意力）替换 MLP 降噪器后，FID 升至 **0.902**。这表明在自回归扩散范式中，MLP 降噪器比 Transformer 降噪器更适配——可能因为 MLP 避免了交叉注意力引入的额外归纳偏置，在 teacher-forcing 预测下更稳定。

**扩散过程的必要性**：用单步 MSE 回归替代扩散去噪过程，FID 退化至 **1.288**，验证了扩散模型在 token 预测中逐步细化的重要性。

**Token 尺寸的影响**：Token 尺寸消融（Table 5）在 1 到 24 帧范围内进行了探索，具体最优配置需参考原文表格数据（注：原文未在提供片段中明确最优值，需手动查证）。

### 失败模式与局限

从定性对比（Figure 4）可知，MDM 存在强抖动、InterDiff 与 HOI-Diff 存在“手粘物体”和穿透问题，ARDHOI 在这些方面有显著改善，但原文未明确报告 ARDHOI 自身的典型失败案例。模型在 OMOMO 和 BEHAVE 之外的泛化能力、补充材料中的具体训练设置等问题仍为开放问题，需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l1662_ARDHOI_Auto_Regressive_Diffusion_for_Generating_3D_Human_Object_Interact/figures/006_Table_2.jpg]]
*Table 2: Text-to-HOI results on BEHAVE dataset*

![[assets/figures/papers/paper_list_l1662_ARDHOI_Auto_Regressive_Diffusion_for_Generating_3D_Human_Object_Interact/figures/008_Table_5.jpg]]
*Table 5: Ablation study for Text-to-HOI on the OMOMO dataset with token sizes from 1 to 24*

![[assets/figures/papers/paper_list_l1662_ARDHOI_Auto_Regressive_Diffusion_for_Generating_3D_Human_Object_Interact/figures/001_Figure_1.jpg]]
*Figure 1: Text guided Human-Object interaction motion sequences generated by our ARDHOI*

## 方法谱系与知识库定位

### 核心问题与现有路线

长序列人-物交互（HOI）生成面临两个瓶颈：**交互一致性**在长序列生成中难以维持；**离散 tokenization**（如 VQ-VAE）在小样本 HOI 数据集上泛化能力不足，且难以建模物理接触的合理性。现有方法可大致分为三条路线：

**扩散模型路线**以 **MDM**（Tevet et al., ICLR 2023）为代表，将文本到运动（Text-to-Motion）的扩散范式适配到 HOI 场景。该路线虽能生成多样化的运动，但在长序列中易出现强扰动和全局朝向失控，导致穿透等物理不合理现象（Figure 4）。**HOI-Diff**（Peng et al., arXiv 2023）和 **InterDiff**（Xu et al., ICCV 2023）进一步针对 HOI 场景设计，但生成的运动常呈现“手粘物体”（stick-to-hand）的模式，缺乏自然交互的多样性。

**自回归路线**以 **ActFormer**（Xu et al., ICCV 2023）为代表，将 HOI 序列建模为离散 token 的自回归预测问题。该路线受限于 VQ-VAE 在小样本数据集上的 token 泛化能力，且离散空间中的误差累积容易导致交互偏离合理区域。

**多阶段扩散路线**以 **THOR**（Wu et al., arXiv 2024）为代表，采用分阶段扩散策略生成人体运动和物体运动。该路线推理速度较慢（Table 3），且阶段间的误差传播可能影响整体一致性。

### ARDHOI 的方法定位

ARDHOI 在方法谱系中占据**连续潜在空间自回归扩散**的新位置，其关键设计选择与现有路线形成系统性对比：

| 设计维度 | 离散自回归路线 | 扩散路线 | ARDHOI |
|---------|--------------|---------|--------|
| Token 空间 | 离散（VQ-VAE） | 无需 token | 连续（cVAE + 对比学习） |
| 生成范式 | 逐 token 预测 | 一次生成全序列 | 逐 token 扩散去噪 |
| 物理约束 | 通常无显式约束 | 通常无显式约束 | 对比学习 + 物理损失 |
| 上下文编码 | Transformer | N/A | Mamba |
| 降噪器 | N/A | U-Net / Transformer | MLP |

ARDHOI 的核心洞察在于：**在连续潜在空间中引入对比学习，显式扩大合理交互与不合理交互之间的边界**，使自回归生成的误差不易漂移到不可行区域。这一设计弥补了离散 tokenization 的泛化缺陷，同时保留了自回归范式在长序列一致性上的优势。

### 关键设计选择的消融证据

各组件的重要性通过消融实验得到验证（Table 6，OMOMO 数据集，FID 越低越好）：

- **Triplet 对比损失**：移除后 FID 从 0.826 升至 0.948，表明对比学习对维持 token 空间质量至关重要。PCA 可视化（Figure 5）进一步显示，无 triplet loss 时正负样本在潜在空间中高度重叠，而有 triplet loss 时二者被清晰分离。
- **Mamba 上下文编码器**：替换为 Transformer 编码器后 FID 升至 0.979，表明 Mamba 在捕获长序列上下文细节方面更有效。
- **MLP 降噪器**：替换为 Transformer Decoder（交叉注意力）后 FID 升至 0.902，表明在自回归扩散范式中，MLP 降噪器比 Transformer 降噪器更适合逐 token 预测任务。
- **扩散过程**：用单步 MSE 回归替代扩散去噪过程，FID 升至 1.288，验证了扩散过程对生成质量的关键作用。

### 适用边界与局限

**适用边界**：ARDHOI 的设计适用于小样本 HOI 数据集（如 OMOMO、BEHAVE）上的文本驱动长序列生成，且要求物体几何信息（点云）作为条件输入。其两阶段训练范式（cVAE 预训练 + ARDM 训练）依赖于 cVAE 冻结后 token 空间的质量。

**已知局限**：
- 当前评估仅覆盖 OMOMO 和 BEHAVE 两个数据集，模型在更大规模或更多样化 HOI 数据集上的泛化能力尚未验证。
- 补充材料中提及的具体训练设置（如超参数、数据增强细节）在公开信息中未完整披露，复现时需参考代码仓库。
- 物理约束损失中的各项权重（$\lambda_{fk}$, $\lambda_{vel}$, $\lambda_{ovel}$, $\lambda_{con}$）对性能的敏感性未在消融实验中单独讨论。

### 开放问题

1. **跨数据集泛化**：ARDHOI 在 OMOMO 和 BEHAVE 之外的数据集（如 GRAB、InterCap）上表现如何？cVAE 的对比学习策略是否依赖特定数据集的交互模式？
2. **多物体交互**：当前方法处理的是人-单物体交互，扩展到多物体场景时，token 空间设计和自回归顺序是否仍然有效？
3. **实时应用**：推理时间 1.25 秒（AITS）虽已显著快于 THOR 等扩散方法，但距离实时交互应用仍有差距。Mamba 和 MLP 降噪器的进一步轻量化是否可行？
4. **物理约束的充分性**：当前物理损失（前向运动学、速度、接触）是否能充分覆盖所有物理不合理情况？是否需要引入更精细的碰撞检测或动力学约束？

## 原文 PDF

![[paperPDFs/AAAI_2025/ARDHOI_Auto_Regressive_Diffusion_for_Generating_3D_Human_Object_Interactions.pdf]]