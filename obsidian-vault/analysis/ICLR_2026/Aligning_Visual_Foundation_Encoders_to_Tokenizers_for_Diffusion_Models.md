---
title: "Aligning Visual Foundation Encoders to Tokenizers for Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Aligning_Visual_Foundation_Encoders_to_Tokenizers_for_Diffusion_Models.pdf
project_link: https://aligntok.github.io
code_link: null
aliases:
- AVFETDM
- AlignTok
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "将预训练视觉基础编码器通过适配器和三阶段训练对齐为扩散模型分词器，构建兼具语义结构和扩散友好性的潜在空间。"
primary_logic: |
  AlignTok 先冻结 DINOv2 等预训练编码器，只训练适配器和解码器完成潜在对齐。
  随后联合微调编码器、适配器和解码器，并用语义保持损失约束当前潜在码贴近前一阶段潜在码，避免语义灾难性遗忘。
  最后仅精炼解码器以提升重建质量，再将所得潜在空间用于 ImageNet 类别条件生成和 LAION 文本到图像扩散训练。
claims:
- "预训练视觉编码器的语义结构可通过渐进式对齐转化为扩散友好的图像潜在空间。"
- "语义保持损失能防止联合微调阶段的语义结构崩塌，并保持线性探测能力。"
- "AlignTok 在 ImageNet 和文本到图像生成设置中比 Vanilla VAE、VA-VAE 或 FLUX VAE 取得更好的生成指标和更快收敛。"
---

# Aligning Visual Foundation Encoders to Tokenizers for Diffusion Models

> [!tip] 核心洞察
> 利用预训练编码器已有的丰富语义结构，通过渐进式对齐（冻结→联合微调→解码器精炼）构建语义丰富且扩散友好的潜在空间，避免从零学习语义的困难。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 对齐视觉基础编码器与扩散模型分词器 |
| 英文题名 | Aligning Visual Foundation Encoders to Tokenizers for Diffusion Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ajnBafpqmE) · [Project](https://aligntok.github.io) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | AlignTok |
| Dataset | ImageNet 256×256, COCO Prompt 6K (T2I) |

> [!tip] 效果简介
> - ImageNet 256×256 上，gFID (w/ CFG) 为 2.17，对比 3.13 (VA-VAE)，变化 -0.96。
> - ImageNet 256×256 上，gFID (w/ CFG, f16d64) 为 2.34，对比 3.19 (VA-VAE)，变化 -0.85。
> - ImageNet 256×256 上，gFID (800 epochs, QKNorm) 为 1.37，对比 1.52 (VA-VAE w/ QKNorm)，变化 -0.15。

## 概要

本文提出 **AlignTok**，一种通过将预训练视觉基础编码器（如 DINOv2）对齐为扩散模型分词器的方法。传统 VAE 分词器从零学习语义结构，导致潜在空间被低层细节支配、扩散友好性差。AlignTok 采用三阶段渐进对齐策略（潜在对齐 → 感知对齐 → 解码器精炼），在保留预训练编码器丰富语义的同时，构建扩散友好的潜在空间。在 ImageNet 256×256 上，AlignTok 仅用 64 个 epoch 即达到 gFID 1.90，加速扩散模型收敛约 5 倍；在 LAION 文本到图像生成中，相同训练步数下持续优于 FLUX VAE 和 VA-VAE。



**潜在扩散模型（Latent Diffusion Models, LDMs）** 通过分词器将图像压缩到潜在空间，再在该空间训练扩散模型。传统 VAE 分词器（如 LDM 中的 VAE）的编码器从零训练，重建损失主导训练过程，导致潜在空间被低层细节支配，缺乏语义结构，扩散模型需要大量训练步数才能学习语义信息。

**现有方法的局限性：**
- **Vanilla VAE**：从零训练编码器，无语义正则化，潜在空间语义贫乏。
- **VA-VAE**：使用语义正则化损失（如 DINOv2 特征对齐），但编码器仍从零训练，语义结构有限。
- **RAE**：冻结预训练编码器，但重建质量差，无法微调编码器。

**核心洞察**：利用预训练编码器（如 DINOv2）已有的丰富语义结构，通过渐进式对齐（冻结 → 联合微调 → 解码器精炼）构建语义丰富且扩散友好的潜在空间，避免从零学习语义的困难。



## 核心方法与创新机理

1. **三阶段渐进对齐策略**：第一阶段冻结预训练编码器，仅训练适配器和解码器；第二阶段联合微调所有组件，引入语义保持损失防止语义灾难性遗忘；第三阶段仅微调解码器提升重建质量。

2. **语义保持损失（Semantic Preservation Loss）**：在第二阶段约束当前潜在码与前一阶段对齐，防止联合优化中语义结构的灾难性丢失。如 Table 1 所示，无此损失时线性探测准确率从 40.55% 骤降至 9.50%。

3. **省略 KL 正则化**：发现 KL 项对语义空间施加不必要的分布约束，省略后生成质量提升。

4. **适配器设计**：两层 MLP 将 1024 维 DINOv2 特征投影到 32 维潜在空间，实现高效降维。



AlignTok 的整体框架如 Figure 2 所示，包含三个渐进阶段：

**Figure 1: Regularization vs. Alignment.** 对比了传统正则化范式（从零训练编码器 + 语义正则化损失）与本文对齐范式（利用预训练编码器 + 渐进对齐）的设计差异。

**Figure 2: Method Overview.** 展示了三阶段对齐流程：
- **Stage 1: Latent Alignment**（顶部）：冻结预训练编码器 E_p，训练适配器 A 和解码器 D，使用重建损失将编码器输出对齐到语义潜在空间。
- **Stage 2: Perceptual Alignment**（左下）：联合优化所有组件，使用重建损失 + 语义保持损失，丰富潜在空间的低层细节。
- **Stage 3: Decoder Refinement**（右下）：仅微调解码器，提升重建保真度而不扰动潜在空间。

**核心模块：**
- **预训练编码器 E_p**：DINOv2-L/14（~304M 参数），提取 1024 维语义特征。
- **适配器 A**：两层 MLP，将 1024 维投影到 32 维潜在空间。
- **解码器 D**：CNN 网络（~42M 参数），与 VA-VAE 相同架构。
- **扩散模型 v_θ**：ImageNet 实验使用 LightningDiT（~673M 参数），LAION 实验使用 FLUX 架构（2B 参数）。



### 1 重建损失

分词器训练使用组合重建损失：

$$\mathcal{L}_{\mathrm{rec}} = \mathcal{L}_{\ell_1}(x, \hat{x}) + w_p \mathcal{L}_{\mathrm{perceptual}}(x, \hat{x}) + w_g \mathcal{L}_{\mathrm{GAN}}(x, \hat{x})$$

其中 $\mathcal{L}_{\ell_1}$ 为像素级 L1 损失，$\mathcal{L}_{\mathrm{perceptual}}$ 为感知损失，$\mathcal{L}_{\mathrm{GAN}}$ 为对抗损失，权重 $w_p = 1.0$，$w_g$ 根据梯度范数比自适应调整。

### 2 流匹配公式

扩散模型使用流匹配（Flow Matching）训练：

$$z_t = (1-t)z_0 + t z_1, \quad z_1 \sim \mathcal{N}(0, I), t \in [0,1]$$

速度场定义为插值路径的导数：

$$u_t = \frac{d}{dt} z_t = z_1 - z_0$$

扩散模型 $v_\theta$ 训练损失：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{z_0, z_1, t} \left[ \| v_\theta(z_t, t) - u_t \|_2^2 \right]$$

### 3 潜在码生成

适配器将预训练编码器特征投影到紧凑潜在码：

$$z_0 = A(E_p(x))$$

### 4 语义保持损失

第二阶段引入语义保持损失，约束当前潜在码与前一阶段对齐：

$$\mathcal{L}_{\mathrm{sp}} = L_{\ell_2}(z_0^*, z_0)$$

其中 $z_0^*$ 为前一阶段（冻结编码器）的潜在码，$z_0$ 为当前阶段（微调编码器）的潜在码。

### 5 感知对齐损失

第二阶段总损失：

$$\mathcal{L}_{\mathrm{pa}} = \mathcal{L}_{\mathrm{rec}} + w_{sp} \mathcal{L}_{\mathrm{sp}}$$

默认 $w_{sp} = 1$（ImageNet）或 $w_{sp} = 3$（LAION）。



## 实验与关键发现

### 1 主要结果

**Table 3: Comparison with Other Tokenizers.** 在 ImageNet 256×256 上，AlignTok 在两种潜在配置下均显著优于基线：

| 配置 | 方法 | rFID ↓ | gFID (w/ CFG) ↓ | IS ↑ | Prec ↑ | Recall ↑ | L.P. Acc. ↑ |
|------|------|--------|-----------------|------|--------|----------|-------------|
| f16d32 | Vanilla VAE | 0.33 | 3.31 | 237.5 | 0.793 | 0.589 | 6.04% |
| f16d32 | VA-VAE | 0.24 | 3.13 | 241.7 | 0.800 | 0.592 | 22.96% |
| f16d32 | **Ours** | **0.26** | **2.17** | **249.3** | **0.811** | **0.599** | **35.09%** |
| f16d64 | Vanilla VAE | 0.14 | 4.03 | 218.1 | 0.775 | 0.573 | 5.09% |
| f16d64 | VA-VAE | 0.12 | 3.19 | 237.6 | 0.795 | 0.589 | 19.72% |
| f16d64 | **Ours** | **0.18** | **2.34** | **247.8** | **0.808** | **0.596** | **46.99%** |

**Table 4: System-Level Comparison.** 在 800 epoch 训练（含 QKNorm）下，AlignTok 达到 gFID 1.37，优于 VA-VAE 的 1.52。

**Table 5: Quantitative Comparison on Text-to-Image (T2I) Generation with FLUX VAE.** 在 COCO Prompt 6K 上，AlignTok 的 gFID 为 30.27，显著优于 FLUX VAE 的 35.78，且在 HPSv2、PickScore、ImageReward、Aesthetic、CLIP、VQA 等指标上全面领先。

### 2 消融研究

**Table 1: Ablation study.** 关键发现：

| 变体 | rFID ↓ | gFID ↓ | IS ↑ | Prec ↑ | Recall ↑ | L.P. Acc. ↑ |
|------|--------|--------|------|--------|----------|-------------|
| Stage 1 only | 1.63 | 3.00 | 237.1 | 0.792 | 0.587 | 41.53% |
| Stage 1+2 (w/o L_sp) | 0.36 | 3.05 | 237.5 | 0.793 | 0.589 | 9.50% |
| Stage 1+2 (w_sp=5) | 0.36 | 2.48 | 244.8 | 0.806 | 0.596 | 40.55% |
| Stage 1+2 (w_sp=1) | 0.36 | 2.19 | 248.6 | 0.811 | 0.591 | 35.09% |
| **Full Model (3 stages)** | **0.26** | **2.17** | **249.3** | **0.811** | **0.599** | 35.09% |

- 语义保持损失权重为 0 时，线性探测准确率从 40.55% 骤降至 9.50%，gFID 从 2.48 恶化至 3.05。
- 余弦损失变体达到 gFID 2.23，线性探测准确率 37.99%。
- 完整三阶段模型（含解码器精炼）进一步改善重建（rFID 0.26）并略微提升生成质量（gFID 2.17）。

**Table 2: Comparison of Various Pretrained Encoders.** DINOv2 在生成质量上最优（gFID 2.19），优于 MAE（gFID 3.12）和 SigLIP 2（gFID 2.85）。

### 3 收敛速度与采样效率

**Figure 4: Comparison of Sampling Steps, CFG Scales, and Convergence Speed.** 关键发现：
- **左图**：AlignTok 在 50 步采样时即超越 VA-VAE 在 250 步采样的质量。
- **中图**：在所有 CFG 尺度下，AlignTok 一致优于 VA-VAE。
- **右图**：AlignTok 收敛速度约为 VA-VAE 的 5 倍（~60K 步 vs ~300K 步达到可比质量）。

### 4 潜在空间分析

**Figure 7: PCA Visualization of Latent Space.** AlignTok 的潜在空间最接近 DINOv2 的特征分布，保留更丰富的语义结构。Vanilla VAE 产生过平滑或过锐利的潜在表示，VA-VAE 倾向于生成一致过平滑的表示。

**Table 16: Quantitative Analysis of Latent Space.** AlignTok 的 CKNNA 指标（0.282）最高，最接近 DINOv2（1.000），而 Vanilla VAE（0.023）和 VA-VAE（0.233）均较低。

### 5 训练与推理成本

**Table 6: Training Cost Comparison.** AlignTok 的累计 GPU 训练小时数（576.15）低于 Vanilla VAE 和 VA-VAE。Stage 1 和 Stage 3 因冻结编码器，内存消耗低于 VA-VAE；Stage 2 因微调 DINOv2 编码器，内存消耗最大。

**Table 7: Inference Memory Consumption Comparison.** 在高分辨率和大批量下，AlignTok 编码器内存显著低于 VA-VAE（1024 分辨率、batch size 8 时：3.015 GB vs 22.78 GB）。

**Table 8: Inference Compute Cost Comparison.** AlignTok 的编码器延迟和 GFLOPS 高于 VA-VAE，但 512 分辨率下延迟更低。

### 6 文本到图像生成扩展

**Table 11: Quantitative Comparison on T2I Generation with FLUX VAE.** 在 Parti Prompt 和 HPSv2 Prompt 上，AlignTok 在 HPSv2、PickScore、ImageReward、Aesthetic、CLIP、VQA 等指标上全面领先。

**Table 12: Quantitative Comparison on T2I Generation with FLUX VAE (Without CFG).** 无 CFG 时，AlignTok 的 gFID 为 33.46，优于 FLUX VAE 的 48.76。

**Table 13: GenEval Comparison with FLUX VAE.** 有 CFG 时，AlignTok 的 GenEval Overall 为 0.556 vs FLUX VAE 的 0.476；无 CFG 时为 0.329 vs 0.230。

**Table 14: Quantitative Comparison on T2I Generation with VA-VAE.** 在 COCO Prompt 6K 上，AlignTok 的 gFID 为 31.19 vs VA-VAE 的 34.13。

**Table 15: GenEval Comparison with VA-VAE.** 有 CFG 时，AlignTok 的 GenEval Overall 为 0.454 vs VA-VAE 的 0.411。

### 7 定性结果

**Figure 5: Qualitative Comparison on Text-to-Image Generation with FLUX VAE.** AlignTok 生成的图像具有更好的连贯性和文本对齐。

**Figure 9: Qualitative Comparison of Reconstruction Quality.** 无 Stage 2+3 的变体无法准确重建输入，而完整模型重建质量与基线相当。

**Figure 10-16: Qualitative Comparison of Convergence Speed.** 在 ImageNet 和文本到图像生成中，AlignTok 在更少训练步数下即可生成高质量图像。

**Figure 19: Qualitative Results on ImageNet Class-Conditional Generation.** 800 epoch 训练后，AlignTok 生成高质量类别条件图像。

**Figure 20-23: Qualitative Results on Text-to-Image Generation.** 在 256×256 和 512×512 分辨率下，AlignTok 生成高质量、高连贯性的图像。

### 8 失败案例

**Figure 8: Failure Case of Our Method on Text-to-Image Generation at 512×512 Resolution.** 常见问题包括：时钟数字渲染不准确（如 12）、物体计数错误、长文本生成不一致、手部等细节渲染困难。

### 9 公平性说明

- 所有实验使用相同的扩散模型架构（LightningDiT 或 FLUX）和训练超参数，仅替换分词器。
- VA-VAE 和 Vanilla VAE 的检查点来自官方 VA-VAE 仓库。
- 系统级比较（Table 4）包含多种方法（VAR, MagViT-v2, MAR, DiT 等），使用相同训练设置。
- 文本到图像实验中，所有模型训练相同步数（100K 或 50K 步），使用相同评估协议。



## 定位与知识库关联

AlignTok 属于 **视觉分词器（Visual Tokenizer）** 研究谱系，核心贡献在于将预训练视觉基础编码器对齐为扩散模型分词器。

**与相关方法的关系：**
- **VA-VAE**（Yao et al., 2025）：使用语义正则化损失对齐 DINOv2 特征，但编码器仍从零训练。AlignTok 直接使用预训练编码器，通过渐进对齐获得更优语义结构。
- **RAE**（Zheng et al., 2025b）：冻结预训练编码器作为分词器编码器，但无法微调，重建质量受限。AlignTok 通过三阶段策略实现编码器微调，显著提升重建质量。
- **REPA-E**（Leng et al., 2025）：端到端训练分词器和扩散模型。AlignTok 专注于分词器本身，可作为 REPA-E 的即插即用替换。
- **MAETok**（Chen et al., 2025a）：使用 MAE 作为编码器。AlignTok 证明 DINOv2 在生成质量上优于 MAE。

**知识库定位：**
- **领域**：生成式模型 → 潜在扩散模型 → 视觉分词器
- **核心问题**：如何构建语义丰富且扩散友好的潜在空间
- **解决方案范式**：对齐预训练编码器（Alignment）而非正则化（Regularization）
- **关键技术**：三阶段渐进对齐、语义保持损失、省略 KL 正则化
- **适用场景**：ImageNet 类别条件生成、LAION 文本到图像生成

**局限性：**
- 文本到图像生成中存在时钟数字渲染不准确、物体计数错误、长文本生成不一致、手部细节渲染困难等问题。
- 编码器推理延迟和 GFLOPS 高于 VA-VAE（除 512 分辨率外）。
- Stage 2 需要微调 DINOv2 编码器，内存消耗最大。
- 重建质量（rFID 0.26）略逊于 MAE（rFID 0.29），但生成质量显著更优。

**开放问题：**
- AlignTok 能否与 RAE 的高通道潜在空间结合，实现语义和重建的双重优势？
- 在更大规模数据集（如 LAION-5B）和更高分辨率（如 1024×1024）上的表现如何？
- 不同语义保持损失权重（如 w_sp=3）在 LAION 数据集上对生成质量的影响如何？

### 整体框架

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_ajnBafpqmE_Aligning/figures/001_Figure_1.jpg]]
*Figure 1: Regularization vs. Alignment.*

### 实验与分析

### 补充图表

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_ajnBafpqmE_Aligning/figures/005_Table_1.jpg]]
*Table 1: Ablation study. Evaluated on ImageNet 256×256 at 80K training steps with 30 sampling steps, using the CFG scale that yields the lowest generation FID (gFID). Our full three-stage model achieves the best balance between reconstruction and generation quality.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_ajnBafpqmE_Aligning/figures/009_Table_2.jpg]]
*Table 2: Comparison of Various Pretrained Encoders. ImageNet 256×256 at 80K steps; 30 sampling steps; CFG tuned for best gFID. Stage 3 is not applied.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_ajnBafpqmE_Aligning/figures/010_Table_3.jpg]]
*Table 3: Comparison with Other Tokenizers. Evaluated on ImageNet 256×256 at 80K training steps with 30 sampling steps. The checkpoints for both the Vanilla VAE and VA-VAE with CNN encoders are taken from the official VA-VAE repository. VA-VAE† denotes the VA-VAE model we trained, using a ViT encoder that matches our architecture but initialized from scratch.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_ajnBafpqmE_Aligning/figures/011_Table_4.jpg]]
*Table 4: System-Level Comparison. We compare with VAR (Tian et al., 2024), MagViT-v2 (Yu et al., 2023), MAR (Li et al., 2024), l-DeTok (Yang et al., 2025), MaskDiT (Zheng et al., 2023), DiT (Peebles & Xie, 2023), SiT (Ma et al., 2024), FasterDiT (Yao et al., 2024), MDT (Gao et al., 2023a), MDTv2 (Gao et al., 2023b), REPA (Yu et al., 2025), CausalFusion (Deng et al., 2024), MAETok (Chen et al., 2025a), and VA-VAE (Yao et al., 2025). Gray and purple regions refer to LightningDiT trained for 64 epochs (80K training steps, no QKNorm) and 800 (1M training steps, with QKNorm) epochs, respectively. Bold numbers indicate the best result in each color block.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_ajnBafpqmE_Aligning/figures/012_Table_5.jpg]]
*Table 5: Quantitative Comparison on Text-to-Image (T2I) Generation with FLUX VAE. Compared on COCO Prompt 6K, which has 6K captions sampled from the COCO validation set. Each 2B-parameter T2I model is trained for 100K steps and evaluated at 256×256 resolution with CFG. rFID is computed using 200K randomly sampled images from the COYO-700M dataset (Minwoo et al., 2022).*



## 原文 PDF

![[paperPDFs/ICLR_2026/Aligning_Visual_Foundation_Encoders_to_Tokenizers_for_Diffusion_Models.pdf]]
