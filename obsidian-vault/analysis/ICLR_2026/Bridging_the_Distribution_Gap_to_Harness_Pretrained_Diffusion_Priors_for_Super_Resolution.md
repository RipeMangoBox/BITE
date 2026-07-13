---
title: "Bridging the Distribution Gap to Harness Pretrained Diffusion Priors for Super-Resolution"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Bridging_the_Distribution_Gap_to_Harness_Pretrained_Diffusion_Priors_for_Super_Resolution.pdf
project_link: null
code_link: null
aliases:
- DSDMSR
- BDGHPDPSR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "DM-SR训练轻量编码器把低分辨率图像映射到冻结扩散模型熟悉的噪声图像混合分布。"
primary_logic: "时间步估计器先预测退化匹配噪声水平，编码器再生成扩散兼容潜变量并由冻结SD-Turbo单步去噪。"
claims:
- "将LR输入分布对齐到预训练扩散分布可避免微调扩散模型带来的先验削弱。"
- "自适应时间步预测比固定噪声水平更能匹配不同退化强度。"
- "DM-SR在感知质量指标和推理速度上优于多步或蒸馏式超分辨率基线。"
---

# Bridging the Distribution Gap to Harness Pretrained Diffusion Priors for Super-Resolution

> [!tip] 核心洞察
> 与其修改预训练扩散模型，不如将LR图像直接变换到扩散模型训练时见过的分布（即噪声-图像混合），从而在不微调扩散模型的前提下充分利用其生成先验，实现单步高质量超分辨率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 弥合分布差距以利用预训练扩散先验进行超分辨率重建 |
| 英文题名 | Bridging the Distribution Gap to Harness Pretrained Diffusion Priors for Super-Resolution |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=66Ad0i78lW) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DM-SR (Distribution Matching Super-Resolution) |
| Dataset | ImageNet |

> [!tip] 效果简介
> - ImageNet 上，BRISQUE 为 13.427，对比 最佳基线值未明确给出，变化 最佳。
> - ImageNet 上，LIQE 为 4.699，对比 最佳基线值未明确给出，变化 最佳。
> - ImageNet 上，CLIP-IQA 为 0.785，对比 最佳基线值未明确给出，变化 最佳。

## 概要

本文提出**分布匹配超分辨率（Distribution Matching Super-Resolution, DM-SR）**，一种无需微调预训练扩散模型即可实现单步高质量超分辨率的新方法。核心思想是：与其修改扩散模型以适应低分辨率（LR）输入，不如训练一个轻量级图像编码器，将LR图像直接映射到扩散模型训练时熟悉的噪声-图像混合分布。通过自适应预测与输入退化程度匹配的噪声水平（时间步），DM-SR在多个基准数据集上的感知质量指标（如BRISQUE, CLIPIQA, MUSIQ）达到最优，且推理速度极快（92 ms，与OSEDiff和InvSR相当，远快于StableSR的10000 ms）。



预训练扩散模型（如Stable Diffusion）在噪声-自然图像混合分布上训练，展现出强大的生成先验。然而，低分辨率（LR）输入图像遵循完全不同的分布，导致直接推理时存在**分布差距**。现有方法通过条件化（如ControlNet）或微调扩散模型来缓解，但这会削弱生成先验或需要多步去噪。本文的核心洞察是：与其修改扩散模型，不如将LR图像直接变换到扩散模型训练时见过的分布（即噪声-图像混合），从而在不微调扩散模型的前提下充分利用其生成先验，实现单步高质量超分辨率。



## 核心方法与创新机理

1.  **分布匹配策略**：训练一个图像编码器，将LR输入映射到扩散模型熟悉的噪声-图像混合分布，而非将LR作为条件输入或从纯噪声开始多步去噪。
2.  **自适应时间步预测**：训练一个时间步估计器，根据输入LR的退化程度自适应预测匹配的噪声水平（时间步），确保高度退化的样本获得更多生成先验。
3.  **单步推理**：DM-SR仅需单步扩散即可生成高质量超分辨率图像，无需多步迭代或蒸馏。
4.  **保持扩散模型冻结**：预训练扩散模型（SD-Turbo）完全冻结，仅训练图像编码器和时间步估计器，保留其完整生成先验。




![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_66Ad0i78lW_Bridging_the_/figures/001_Figure_1.jpg]]
*Figure 1: Figure 1: ×4 super-resolution comparison on various images. The left half of each image shows the bicubic upsampled input, and the right half shows the output from our DM-SR. Compared to previous methods, DM-SR produces the most perceptually pleasing results. (Zoom-in for best view)*

DM-SR的整体架构如Figure 2所示。流程如下：

1.  **时间步估计**：时间步估计器 τ 根据输入LR图像 I_LR 预测匹配的时间步 t̂。
2.  **图像编码**：图像编码器 E_θ 将 I_LR 和 t̂ 映射到扩散兼容的潜在表示 X_SR^t̂。
3.  **分解与去噪**：预训练扩散去噪器 μ_ψ (SD-Turbo) 将 X_SR^t̂ 分解为图像分量 Z_SR 和噪声分量 ϵ_SR。
4.  **解码**：预训练VAE解码器将 Z_SR 解码为最终超分辨率图像 I_SR。

训练过程中，编码器 E_θ 通过图像损失 L_Z 和噪声损失 L_ϵ 进行优化，判别器 D_ϕ 以LR图像为条件区分 Z_SR 和真实HR潜在 X_HR^0。



### 5.1 时间步估计

时间步估计器 τ 使用VGG风格架构，预测与输入LR退化程度匹配的时间步 t̂。真值时间步 t 定义为LR图像与对应HR图像之间的归一化LPIPS分数（范围[0,500]）。预测公式为：

$$\hat{t} = sum(softmax(\mathbf{F}_{\hat{t}}) * [0,1,...,488,499])$$

其中 F_t̂ 是估计器输出的特征向量。

### 5.2 图像编码

图像编码器 E_θ 采用预训练VAE编码器，通过ControlNet风格设计将预测时间步 t̂ 的特征注入各中间层。编码器将 I_LR 映射到潜在表示 X_SR^t̂，旨在匹配对应噪声HR潜在 X_HR^t̂ 的分布。

### 5.3 分解与去噪

预训练去噪器 μ_ψ 将 X_SR^t̂ 分解为噪声分量和图像分量：

$$\epsilon_{SR} = \mu_\psi(\mathbf{X}_{SR}^{\hat{t}}, \hat{t}), \quad \mathbf{Z}_{SR} = \frac{1}{\sqrt{\bar{\alpha}_{\hat{t}}}}(\mathbf{X}_{SR}^{\hat{t}} - \sqrt{1 - \bar{\alpha}_{\hat{t}}}\epsilon_{SR})$$

其中 ᾱ_t 是噪声调度累积乘积。

### 5.4 损失函数

**图像分量损失 L_Z** 包含L1、感知、对抗和分布匹配损失：

$$\mathcal{L}_Z = \lambda_{L1}\mathcal{L}_{L1} + \lambda_{per}\mathcal{L}_{per} + \lambda_{adv}\mathcal{L}_{adv} + \lambda_{dm}\mathcal{L}_{dm}$$

**对抗损失**：判别器 D_ϕ 以LR图像为条件，区分 Z_SR 和 X_HR^0：

$$\min_{\mathcal{D}_\phi} -\mathbb{E}_{\mathbf{X}_{HR}^0 \sim p(\mathbf{X}_{HR}^0)}[\log(\mathcal{D}_\phi(\mathbf{X}_{HR}^0, \mathbf{I}_{LR}))] - \mathbb{E}_{\mathbf{Z}_{SR} \sim p(\mathbf{Z}_{SR})}[\log(1 - \mathcal{D}_\phi(\mathbf{Z}_{SR}, \mathbf{I}_{LR}))]$$

$$\mathcal{L}_{adv} = -\mathbb{E}_{\mathbf{Z}_{SR} \sim p(\mathbf{Z}_{SR})}[\log(\mathcal{D}_\phi(\mathbf{Z}_{SR}, \mathbf{I}_{LR}))]$$

**分布匹配损失 L_dm**：通过对齐噪声化 Z_SR 和 X_HR^0 的分数函数，促进内容一致的分布对齐：

$$\mathcal{L}_{dm} = \mathbb{E}_{\mathbf{Z}_{SR}, \tilde{\mathbf{X}}_{HR}^{\hat{t}}, \hat{t}}[(\mu_\psi(\tilde{\mathbf{Z}}_{SR}^{\hat{t}}, \hat{t}) - \mu_\psi(\tilde{\mathbf{X}}_{HR}^{\hat{t}}, \hat{t}))\frac{d\mathcal{E}}{d\theta}]$$

**噪声损失 L_ϵ**：鼓励 ϵ_SR 成为重建HR潜在的最优噪声，使其具有输入感知性：

$$\mathcal{L}_\epsilon = \mathbb{E}_{\mathbf{X}_{HR}^0, \epsilon_{SR}, \hat{t}}[(\mu_\psi(\sqrt{\bar{\alpha}_t}\mathbf{X}_{HR}^0 + \sqrt{1 - \bar{\alpha}_t}\epsilon_{SR}, \hat{t}) - \epsilon_{SR})\frac{d\mathcal{E}}{d\theta}]$$

**总损失**：L_tot = L_Z + L_ϵ

### 5.5 超参数

损失权重：λ_L1=1.00, λ_per=2.00, λ_adv=0.10, λ_dm=0.50, λ_ϵ=1.00。



## 实验与关键发现


### 6.1 主要结果

Table 1展示了DM-SR在多个基准数据集上的×4 SR非参考指标比较。在ImageNet上，DM-SR在所有感知指标上达到最优：BRISQUE 13.427, LIQE 4.699, CLIP-IQA 0.785, TOPIQ (NR) 0.712, NIMA 5.492, MANIQA 0.633, MUSIQ 73.856。在RealSet80上，CLIP-IQA达到0.797。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_66Ad0i78lW_Bridging_the_/figures/003_Table_1.jpg]]
*Table 1: Table 1: × 4 SR non-reference metrics comparison on various benchmark datasets. Best numbers are denoted with bold.*

Table 2显示DM-SR在RealSR数据集上的参考指标和效率比较。推理时间仅92 ms，与OSEDiff（100 ms）和InvSR（100 ms）相当，远快于StableSR（10000 ms）。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_66Ad0i78lW_Bridging_the_/figures/011_Table_2.jpg]]
*Table 2: Table 2: (Left) × 4 SR reference metrics comparison on RealSR dataset. (Right) Efficiency Comparison of DM-SR with previous SR methods on SR task. Specifically, we upsample images of size $\mathbb { R } ^ { 1 2 8 \times 1 2 8 \times 3 }$ using a single NVIDIA A100 GPU to measure the runtime of each method. Table 3: Comparison of DM-SR on Realset80 with various timesteps. Our final model adaptively predicts $\hat { t } \in$ \ [ 0 , 5 0 0 ] from $\mathbf { I } _ { \mathrm { L R } }$ instead of relying on fixed timesteps. Table 4: Comparison of DM-SR on Realset80 with various number of steps.Despite being controllable, single-step application still produces high-quality results.

### 6.2 消融研究

**自适应时间步**（Table 3）：自适应预测时间步 t̂ ∈ [0,500] 优于所有固定时间步（t=100, 200, 300, 400, 500），在RealSet80上获得最佳感知分数：LIQE 4.652, CLIPIQA 0.797, MUSIQ 70.616。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_66Ad0i78lW_Bridging_the_/figures/012_Table_3.jpg]]

**推理步数**（Table 4）：单步（1步）推理在感知质量上最佳，更多步数（2, 3, 4, 5步）未显著提升。

**时间步真值选择**（Table 5）：LPIPS作为时间步真值优于像素距离和SSIM。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_66Ad0i78lW_Bridging_the_/figures/013_Table_5.jpg]]
*Table 5: Table 5: Comparison of DM-SR on Realset80 with various ground truth for the timesteps. Our final model utilize normalized LPIPS score ∈ [0, 500] for the ground turth for the timesteps.*

**损失组合**（Table 6）：完整损失组合（L_adv + L_dm + L_ϵ）在RealSet80上获得最高感知分数：LIQE 4.652, CLIPIQA 0.797, MUSIQ 70.616。

**文本提示**（Table 7）：输入特定文本提示（LLaVA提取）略优于固定提示：LIQE 4.668 vs 4.652, CLIPIQA 0.801 vs 0.797。

**L_ϵ 分析**（Figure 6）：L_ϵ 使预测噪声 ϵ_SR 具有输入感知性，避免不同输入产生相同噪声。无 L_ϵ 时，预测噪声在不同输入间几乎相同；有 L_ϵ 时，噪声分布根据输入变化。

**L_dm 分析**（Table 9）：L_dm 促进内容一致的分布对齐，超越仅使用 L_adv 的效果。在RealSR上，添加 L_dm 同时改善感知和失真指标：PSNR 24.984, SSIM 0.710, LPIPS 0.317, LIQE 4.485, CLIPIQA 0.732, MUSIQ 71.489。

### 6.3 公平性说明

- DM-SR在感知质量指标上表现最佳，但在失真指标（如PSNR, SSIM）上并非最优，体现了感知-失真权衡。
- DM-SR使用SD-Turbo作为基础去噪器，其性能可能受限于SD-Turbo本身的能力。
- 时间步估计器使用LPIPS分数作为真值，LPIPS本身是一种感知度量，可能引入偏差。

### 6.4 局限性

- DM-SR可能生成与输入LR在内容上存在差异的细节（例如，将灰色瞳孔生成为黑色瞳孔），优先考虑感知质量而非严格保真度（Figure 5）。
- DM-SR使用固定的文本提示，虽然输入特定提示可以改善，但需要额外的LLM（如LLaVA）提取提示，增加了复杂性。
- DM-SR的性能依赖于预训练扩散模型（SD-Turbo）的能力，可能受限于其生成先验的范围。

### 补充图表

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_66Ad0i78lW_Bridging_the_/figures/014_Table_5.jpg]]



## 定位与知识库关联

DM-SR属于**单步扩散超分辨率**方法谱系，与以下方法形成对比：

| 方法 | 核心策略 | 推理步数 | 是否微调扩散模型 |
|------|----------|----------|------------------|
| RealESRGAN | GAN-based | 1 | N/A |
| StableSR | 迭代扩散 | 多步 | 是 |
| SinSR | 单步蒸馏 | 1 | 是（蒸馏） |
| OSEDiff | 单步蒸馏 | 1 | 是（蒸馏） |
| InvSR | 假设噪声HR和LR不可区分 | 1 | 否 |
| **DM-SR (本文)** | **分布匹配** | **1** | **否** |

DM-SR的核心创新在于**分布匹配策略**：通过训练编码器将LR输入映射到扩散模型熟悉的分布，而非修改扩散模型本身。这与InvSR的假设（噪声HR和LR不可区分）不同，DM-SR明确建模分布差距并通过自适应时间步预测来弥合。与蒸馏方法（SinSR, OSEDiff）相比，DM-SR无需复杂的蒸馏过程，直接利用预训练扩散模型的生成先验。

**开放问题**：
- DM-SR能否推广到其他图像恢复任务（如去噪、去模糊、修复）？
- 时间步估计器使用LPIPS作为真值的理论基础是什么？LPIPS的归一化方式如何影响性能？
- DM-SR对不同的预训练扩散模型（如SDXL, SD3）的鲁棒性和泛化能力如何？
- DM-SR能否扩展到视频超分辨率？
- 输入特定文本提示的自动生成能否完全集成到框架中，避免依赖外部LLM？
- DM-SR在极端退化（如大噪声、严重模糊）下的表现如何？



## 原文 PDF

![[paperPDFs/ICLR_2026/Bridging_the_Distribution_Gap_to_Harness_Pretrained_Diffusion_Priors_for_Super_Resolution.pdf]]
