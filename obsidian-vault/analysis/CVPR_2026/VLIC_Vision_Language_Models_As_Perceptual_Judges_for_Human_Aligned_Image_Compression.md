---
title: "VLIC: Vision-Language Models As Perceptual Judges for Human-Aligned Image Compression"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VLIC_Vision_Language_Models_As_Perceptual_Judges_for_Human_Aligned_Image_Compression.pdf
code_link: null
aliases:
- VVLMIC
- VLIC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用VLM的零样本2AFC判断作为奖励信号，通过扩散直接偏好优化（Diffusion DPO）对扩散自编码器进行后训练，从而将压缩模型与人类视觉偏好对齐。
primary_logic: VLM能够零样本复现人类对视觉相似性的二元判断，将其与LPIPS集成后通过Diffusion DPO微调扩散压缩模型，可以显著提升重建感知质量并优于单独使用任何一种奖励。
claims:
- 在MS-COCO上，使用VLM+LPIPS后训练的VLIC在Human Elo上比仅使用LPIPS后训练提升+20 (0.07bpp) 和 +9 (0.21bpp)。
- VLM（Gemini 2.5-Flash）零样本条件下在BAPPS-Val和压缩图像2AFC基准上分别达到69.44%和83.80%的准确率，接近人类水平。
- 消融实验证实，去除自集成或LPIPS集成会损害多数指标性能，完全去除DPO后训练则所有指标恶化。
- MS-COCO 上 Human Elo @ 0.07bpp = 858
---

# VLIC: Vision-Language Models As Perceptual Judges for Human-Aligned Image Compression

> [!tip] 核心洞察
> VLM能够零样本复现人类对视觉相似性的二元判断，将其与LPIPS集成后通过Diffusion DPO微调扩散压缩模型，可以显著提升重建感知质量并优于单独使用任何一种奖励。

| 字段 | 内容 |
|------|------|
| 中文题名 | VLIC：基于视觉语言模型感知评判器的人类对齐图像压缩 |
| 英文题名 | VLIC: Vision-Language Models As Perceptual Judges for Human-Aligned Image Compression |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.15701) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VLIC (Vision-Language Models for Image Compression) |
| Dataset | MS-COCO |

> [!tip] 效果简介
> - MS-COCO 上，Human Elo @ 0.07bpp 858 vs 838 (LPIPS-only post-training) (+20)；LPIPS @ 0.07bpp 0.274 vs 0.274 (0)；Human Elo @ 0.21bpp 1112 vs 1103 (LPIPS-only post-training) (+9)。

## 概述

图像压缩的核心挑战在于：传统像素级失真度量（如 MSE）与人类视觉感知之间存在显著鸿沟，而现有学习型感知度量也难以精确捕捉人类对压缩重建的细微偏好。视觉语言模型（VLM）的涌现为这一问题提供了新的可能——VLM 能够在零样本条件下复现人类对视觉相似性的二元判断，但如何将这种离散的偏好信号转化为可微的压缩模型训练目标，仍是一个开放问题。

本文提出 **VLIC（Vision-Language Models for Image Compression）**，一种基于扩散自编码器的图像压缩系统，其核心创新在于将 VLM 的二元偏好判断直接集成为后训练奖励信号。VLIC 通过 **扩散直接偏好优化（Diffusion DPO）** 对预训练的扩散压缩模型进行在线微调，使重建结果与人类视觉偏好对齐。与将 VLM 判断蒸馏为独立感知损失网络的思路不同，VLIC 直接利用偏好对进行策略优化，避免了中间表示的损失。

方法的关键设计包括：（1）采用 **VLM 与 LPIPS 集成** 的奖励机制，要求两者对偏好对给出“一致判断”才纳入训练，从而兼顾分布感知质量与像素对齐；（2）通过 **自集成**（多随机种子 VLM 评分求和）降低 VLM 评分的随机噪声；（3）结合 **流匹配损失** 与 DPO 损失共同训练，防止偏好优化过程中的生成质量发散。

实验结果表明，VLIC 在 MS-COCO 上取得了显著的人类感知增益：在 0.07 bpp 码率下，使用 VLM+LPIPS 后训练的模型在 Human Elo 上比仅使用 LPIPS 后训练提升 +20 分；在 0.21 bpp 下提升 +9 分。VLM（Gemini 2.5 Flash）在 BAPPS-Val 和压缩图像 2AFC 基准上的零样本准确率分别达到 69.44% 和 83.80%，接近人类水平。消融实验进一步证实，去除自集成或 LPIPS 集成均会损害多数指标性能，完全去除 DPO 后训练则所有指标恶化。

VLIC 也存在若干局限：VLM 在候选重建高度相似时可能产生幻觉（丧失自一致性）；基于编辑距离的文本可读性奖励会导致模型退化为审查所有可读文本；方法依赖强大的闭源 VLM，其可用性和推理成本可能限制广泛复现。尽管如此，VLIC 为利用 VLM 的感知能力指导压缩模型训练开辟了一条可行路径。

## 背景与动机

图像压缩是数字视觉通信的基础技术，其核心挑战在于以尽可能低的比特率重建出符合人类感知的高质量图像。传统压缩方法（如JPEG、BPG）依赖像素级失真度量（均方误差MSE、峰值信噪比PSNR）指导编解码器设计，但这些度量与人类视觉感知的对齐程度有限——两张PSNR相近的图像，在人类眼中可能呈现截然不同的感知质量。

近年来，基于深度学习的感知度量（如LPIPS、DISTS）在一定程度上弥补了这一鸿沟，它们通过预训练网络的特征空间距离来近似人类判断。然而，这些度量本质上仍是固定函数的代理，无法灵活捕捉人类感知的全部维度，例如对文本可读性、人脸细节、纹理自然度等特定视觉属性的敏感度。

与此同时，视觉语言模型（Vision-Language Models, VLM）在零样本视觉理解任务上展现出与人类高度一致的判断能力。一个自然的问题是：**能否将VLM的感知判断直接转化为可优化的压缩模型训练信号？** 这一设想的实现面临两个关键瓶颈：

1. **信号转换瓶颈**：VLM的输出通常是二元偏好判断或自然语言描述，而非可微分的连续数值，难以直接嵌入基于梯度的压缩模型训练流程。
2. **训练稳定性瓶颈**：即使将VLM判断转化为奖励信号，单独使用该信号进行偏好优化可能导致模型在像素对齐度量（如PSNR）上退化，或在高度相似的候选重建上因VLM幻觉而产生错误引导。

本文提出 **VLIC（Vision-Language Models for Image Compression）**，一个基于扩散自编码器的图像压缩框架，通过扩散直接偏好优化（Diffusion DPO）将VLM的二元偏好判断与LPIPS感知度量集成，对压缩模型进行后训练，从而在保持像素对齐能力的同时显著提升人类感知对齐质量。该方法的动机源于一个核心洞察：VLM能够零样本复现人类对视觉相似性的二元判断，将其作为奖励信号与现有感知度量协同使用，可以引导扩散压缩模型生成更符合人类偏好的重建结果。

## 核心创新

VLIC 的核心创新在于**将视觉语言模型（VLM）的零样本感知评判能力转化为扩散自编码器压缩模型的可优化训练信号**，从而突破传统像素级失真度量与人类视觉偏好对齐不足的瓶颈。相比于现有基于 GAN 或扩散模型的压缩方法，VLIC 在以下关键维度上进行了系统性改造：

### 1. 奖励函数：从单一感知损失到 VLM+LPIPS 集成评判

传统方法仅依赖 LPIPS 等感知损失作为后训练目标。VLIC 引入 VLM（Gemini 2.5-Flash）对同一潜在码解码出的两个重建图像进行二元偏好判断，并要求 **VLM 与 LPIPS 的判断必须一致**才将该偏好对纳入训练缓冲区。这一“一致过滤”机制既利用了 VLM 的高层语义理解能力，又借助 LPIPS 的低层纹理约束，避免了单一信号源的偏差。

### 2. 后训练目标：从纯流匹配损失到 Diffusion DPO + 流匹配联合优化

基线方法（如 FlowMo）仅使用流匹配损失进行预训练。VLIC 在后训练阶段引入 **Diffusion DPO（扩散直接偏好优化）** 损失，与原始流匹配损失联合训练：

$$L(\theta) = L_{\mathrm{DDPO}}(\theta) + \lambda_{\mathrm{Flow}} L_{\mathrm{Flow}}(\theta)$$

其中 Diffusion DPO 损失通过调整当前策略与参考策略在胜负样本上的噪声预测误差差异来实现偏好对齐：

$$L_{\mathrm{DDPO}}(\theta) = -\mathbb{E} \log \sigma\left(-\beta \omega(\lambda_t)(\Delta^w - \Delta^l)\right)$$

$$\Delta^w = \|\epsilon^w - \epsilon_\theta(\hat{\mathbf{x}}_t^w, \mathbf{x}, t)\|_2^2 - \|\epsilon^w - \epsilon_{\mathrm{ref}}(\hat{\mathbf{x}}_t^w, \mathbf{x}, t)\|_2^2$$

$$\Delta^l = \|\epsilon^l - \epsilon_\theta(\hat{\mathbf{x}}_t^l, \mathbf{x}, t)\|_2^2 - \|\epsilon^l - \epsilon_{\mathrm{ref}}(\hat{\mathbf{x}}_t^l, \mathbf{x}, t)\|_2^2$$

流匹配损失的保留起到正则化作用，防止 DPO 优化导致生成质量发散。

### 3. 量化方法：从 LFQ 到 FSQ

VLIC 将基线架构中的 Lookup-Free Quantization（LFQ）替换为 **Finite Scalar Quantization（FSQ）**。这是与 FlowMo 架构的唯一结构性差异，旨在简化量化过程并保持潜在表示的稳定性。

### 4. 推理策略：从固定分辨率到零样本平铺推理

基线方法通常限定在 256×256 分辨率下推理。VLIC 采用 **零样本平铺推理（tiled inference with MultiDiffusion）**，使模型能够处理任意分辨率图像，显著提升了实际部署的灵活性。

### 5. 在线偏好优化与自集成

VLIC 采用 **在线 Diffusion DPO 训练**，在训练过程中定期刷新偏好缓冲区，效果优于预先构建离线偏好数据集。同时，通过 **自集成（self-ensembling）**——对多个随机种子下的 VLM 评分求和取多数票——有效降低了 VLM 判断的噪声，提升了与人类判断的一致性（见 Figure 5）。

---

**创新本质总结**：VLIC 并未重新设计压缩架构，而是在扩散自编码器的后训练阶段引入 VLM 作为“感知评判器”，通过 Diffusion DPO 将不可微的二元偏好信号转化为可优化的梯度。这一思路将压缩模型的对齐问题从“设计更好的感知损失函数”转变为“利用强大的多模态模型直接提供人类对齐的偏好信号”，为图像压缩的感知质量提升开辟了新路径。

## 整体框架

VLIC 的整体 pipeline 围绕“压缩-采样-评判-优化”闭环构建，将视觉语言模型（VLM）的二元偏好判断转化为扩散自编码器的训练信号。系统由五个核心模块串联而成，形成端到端的可训练压缩框架，如 **Figure 3** 所示。

![[assets/figures/papers/paper_list_l808_https_arxiv_org_abs_2512_15701/figures/003_Figure_3.jpg]]
*Figure 3: Method. An original image is encoded to a one-dimensional discrete latent code via an encoder. The discrete code is entropy coded by an auto-regressive language model. The diffusion decoder samples two reconstructions conditioned on the latent code, which are ranked via a VLM. The resulting preference is used to train the full diffusion autoencoder via Diffusion DPO [47]*

**编码与量化**：原始图像首先通过一个 Transformer 编码器被压缩为一维离散潜在码。与基线方法 FlowMo 不同，VLIC 将查找无关量化（LFQ）替换为有限标量量化（FSQ），以改善码本利用和训练稳定性。这一阶段产生紧凑的离散表示，为后续的熵编码和扩散解码提供基础。

**熵编码**：离散潜在码通过一个自回归 Transformer 熵编码器进行无损算术编码，进一步压缩比特率。该熵编码器在潜在序列上执行简单的自回归建模，不引入额外的感知损失或复杂结构。

**扩散解码与采样**：熵解码后的潜在码作为条件输入扩散解码器。解码器从同一潜在码出发，随机采样两个重建图像 $x^w$ 和 $x^l$，构成偏好比较对。这一随机采样机制是生成训练偏好数据的关键——同一压缩表示可以产生视觉质量不同的多个重建，为 VLM 评判提供对比基础。

**VLM 偏好排序**：两个重建图像被送入 VLM（Gemini 2.5 Flash）进行二元评判。为降低 VLM 输出的随机噪声，系统采用自集成策略：对同一对图像以多个随机种子多次请求 VLM，汇总评分得到集成奖励 $r_A = \sum_{i=1}^n r_A^i$、$r_B = \sum_{i=1}^n r_B^i$。最终奖励并非仅依赖 VLM，而是要求 VLM 与 LPIPS 感知度量做出一致判断——只有当两者对胜负达成共识时，该偏好对才被采纳。这一设计既利用了 VLM 的高层语义理解，又保留了 LPIPS 对像素级失真的敏感性，避免单一信号源的偏差。

**Diffusion DPO 训练循环**：经 VLM+LPIPS 联合评判产生的偏好对（胜者 $x^w$、败者 $x^l$）被送入在线更新的偏好缓冲区。扩散自编码器通过 Diffusion DPO 损失进行后训练，目标函数为：

$$L_{\mathrm{DDPO}}(\theta) = -\mathbb{E} \log \sigma\left(-\beta \omega(\lambda_t)(\Delta^w - \Delta^l)\right)$$

其中 $\Delta^w$ 和 $\Delta^l$ 分别衡量当前策略与参考策略在胜者和败者样本上的噪声预测误差之差。训练时编码器保持解冻，以允许整个自编码器适应偏好信号。为防止 DPO 训练导致生成质量发散，最终损失联合优化 DPO 目标和原始流匹配损失：

$$L(\theta) = L_{\mathrm{DDPO}}(\theta) + \lambda_{\mathrm{Flow}} L_{\mathrm{Flow}}(\theta)$$

**推理策略**：模型在 256×256 分辨率的 ImageNet 上训练，但通过零样本平铺推理（tiled inference with MultiDiffusion）支持任意分辨率输入。平铺时需设置合适的重叠边距（论文使用 8 像素），以在扩散过程中传递块间信息，避免边界伪影。

整个框架的核心创新在于用 VLM 的零样本二元判断替代传统的手工感知损失，并通过 Diffusion DPO 将其直接注入压缩模型的后训练过程，而非蒸馏为独立的感知网络。这种设计使得压缩模型能够捕捉到像素级度量难以表达的人类视觉偏好维度（如人脸、文本、纹理的保真度），同时保持了端到端训练的一致性和可扩展性。

## 核心模块与公式推导

### 系统流水线

VLIC 的压缩重建流水线由四个核心模块构成（Figure 3）：

1. **编码器（Transformer encoder）**：将原始图像压缩为一维离散潜在码，采用 **FSQ（Finite Scalar Quantization）** 替代 FlowMo 原有的 LFQ（Lookup-Free Quantization），这是架构层面唯一的改动。
2. **熵编码器（Autoregressive transformer entropy coder）**：对一维离散潜在序列进行自回归建模与无损算术编码，进一步降低比特率。
3. **扩散解码器（Diffusion decoder）**：以潜在码为条件，从噪声中采样生成重建图像。在训练阶段，每次对同一潜在码采样两个重建，构成偏好比较对。
4. **VLM 偏好排序模块**：使用 **Gemini 2.5 Flash** 作为零样本评判器，对重建对进行二元偏好判断，并与 LPIPS 集成——仅当两者判断一致时才将该偏好对纳入训练缓冲区。

后训练时，编码器保持解冻（unfrozen），整个扩散自编码器通过 Diffusion DPO 进行端到端优化。

### Diffusion DPO 损失函数

VLIC 的核心优化目标是将 VLM 的二元偏好信号转化为可训练梯度。为此，论文采用 Diffusion DPO 框架，其损失函数为：

$$L_{\mathrm{DDPO}}(\theta) = -\mathbb{E} \log \sigma\left(-\beta \omega(\lambda_t)(\Delta^w - \Delta^l)\right) \tag{1}$$

其中 $\sigma$ 为 sigmoid 函数，$\beta$ 控制偏好强度，$\omega(\lambda_t)$ 为时间步相关的信噪比权重。$\Delta^w$ 和 $\Delta^l$ 分别表示胜者（winner）与败者（loser）重建在当前策略 $\epsilon_\theta$ 与参考策略 $\epsilon_{\mathrm{ref}}$ 上的噪声预测误差之差：

$$\Delta^w = \|\epsilon^w - \epsilon_\theta(\hat{\mathbf{x}}_t^w, \mathbf{x}, t)\|_2^2 - \|\epsilon^w - \epsilon_{\mathrm{ref}}(\hat{\mathbf{x}}_t^w, \mathbf{x}, t)\|_2^2 \tag{2}$$

$$\Delta^l = \|\epsilon^l - \epsilon_\theta(\hat{\mathbf{x}}_t^l, \mathbf{x}, t)\|_2^2 - \|\epsilon^l - \epsilon_{\mathrm{ref}}(\hat{\mathbf{x}}_t^l, \mathbf{x}, t)\|_2^2 \tag{3}$$

**直觉解释**：优化目标希望 $\Delta^w$ 减小（当前策略在胜者样本上的预测误差比参考策略更低），同时 $\Delta^l$ 增大（当前策略在败者样本上的预测误差比参考策略更高），从而拉大胜负样本在策略空间中的差距，使扩散解码器更倾向于生成被 VLM 偏好的重建。

### 流匹配正则化与最终损失

为防止 Diffusion DPO 训练导致生成质量退化或发散，VLIC 同时保留原始流匹配损失作为正则项：

$$L_{\mathrm{Flow}}(\theta) = \mathbb{E}_{\epsilon, x, t} \big( \| \mathbf{v} - \mathbf{v}_{\theta}(\mathbf{x}, \mathbf{x}_t, t) \|_2^2 \big) \tag{4}$$

最终训练损失为两者加权组合：

$$L(\theta) = L_{\mathrm{DDPO}}(\theta) + \lambda_{\mathrm{Flow}} L_{\mathrm{Flow}}(\theta) \tag{5}$$

### VLM 自集成奖励

由于 VLM 的二元判断存在随机噪声（尤其在高度相似的候选对之间），论文采用**自集成（self-ensembling）**策略：对同一图像对，使用多个随机种子请求 VLM 进行评分，将各次评分求和得到集成奖励：

$$r_A = \sum_{i=1}^n r_A^i, \quad r_B = \sum_{i=1}^n r_B^i$$

其中 $r_A^i$、$r_B^i$ 为第 $i$ 次随机种子下 VLM 对图像 A、B 的二元评分。Figure 5 表明，随着集成种子数增加，VLM 在 BAPPS 基准上与人类判断的一致性单调提升。

### 补充图表

![[assets/figures/papers/paper_list_l808_https_arxiv_org_abs_2512_15701/figures/012_Figure_7.jpg]]
*Figure 7: Tiled inference for arbitrary resolutions. From top to bottom: Original image, tiling strategy, reconstructed image. The margin size (we use 8 pixels in this work) must be large enough to communicate information between patches during diffusion to avoid unsightly border artifacts, but not so large as to waste BPP*

## 实验与分析

### 核心实验设置

VLIC 的训练分为预训练与后训练两个阶段。预训练阶段在 ImageNet 256×256 分辨率上进行 1,000,000 步，使用 Adam 优化器（学习率 1e-4）。后训练阶段引入 Diffusion DPO 损失与流匹配损失的联合优化，编码器在此时保持解冻状态以获得更优性能。推理时采用移位时间调度，并通过 10% 的离散潜在码丢弃实现无分类器引导。为支持任意分辨率，模型使用基于 MultiDiffusion 的零样本平铺推理策略（Figure 7），边界 margin 设为 8 像素以平衡信息传递与码率效率。

模型在 0.07 bpp 和 0.21 bpp 两个码率点进行训练，总参数量为 1.01B（Table 4、Table 5）。评估数据集涵盖 MS-COCO、CLIC 2020 和 CLIC 2022，指标包括 Human Elo、LPIPS、FID、FD-DINO、PSNR 等。

![[assets/figures/papers/paper_list_l808_https_arxiv_org_abs_2512_15701/figures/010_Table_4.jpg]]
*Table 4: Model hyperparameters for low BPP configuration. Total parameter count is 1.01B*

![[assets/figures/papers/paper_list_l808_https_arxiv_org_abs_2512_15701/figures/011_Table_5.jpg]]
*Table 5: Model hyperparameters for high BPP configuration. Total parameter count is 1.01B*

### 主实验结果

VLIC 在多个基准上达到有竞争力或最先进的性能，尤其在 MS-COCO 上表现突出——该数据集包含大量文本、人脸等人类敏感特征（Figure 4）。Table 1 直接量化了 VLM 奖励的增益：在 MS-COCO 上，使用 VLM+LPIPS 联合后训练的 VLIC 相比仅使用 LPIPS 后训练，Human Elo 在 0.07 bpp 下提升 +20（838→858），在 0.21 bpp 下提升 +9（1103→1112）。值得注意的是，LPIPS 指标在两个码率点上几乎未变（0.274 vs. 0.274；0.168 vs. 0.169），表明 VLM 奖励带来的感知质量提升无法被 LPIPS 自身捕获，这恰恰印证了 VLM 作为补充评判器的价值。

![[assets/figures/papers/paper_list_l808_https_arxiv_org_abs_2512_15701/figures/005_Table_1.jpg]]
*Table 1: Importance of VLM. At multiple BPP (prior to entropy coding), post-training with the VLM + LPIPS objective provides gains over post-training the compression model with LPIPS alone*

![[assets/figures/papers/paper_list_l808_https_arxiv_org_abs_2512_15701/figures/004_Figure_4.jpg]]
*Figure 4: Quantitative Evaluation on Image Compression Datasets. Overall, VLIC achieves competitive or state-of-the-art performance. VLIC performs particularly well on perceptual metrics and particularly well on MS-COCO, which contains a high percentage of images with human-relevant characteristics such as text and faces*

定性对比（Figure 2）显示，VLIC 在重建感知相关的精细细节、人脸和纹理方面比 HiFiC、PO-ELIC、PerCo 等基线方法更忠实。

![[assets/figures/papers/paper_list_l808_https_arxiv_org_abs_2512_15701/figures/002_Figure_2.jpg]]
*Figure 2: Qualitative results on standard image compression datasets. Top: We compare VLIC with HiFiC [33] and PO-ELIC [18] on a CLIC 2022 image [46] at various bits per pixel (bpp). Bottom: We compare our approach with HiFiC and PerCo on MS-COCO [28]. We find that our approach represents perceptually relevant fine details, faces, and textures more faithfully*

### VLM 作为人类对齐评判器的验证

Table 2 提供了 VLM 与人类判断对齐的基准证据。Gemini 2.5-Flash 在零样本条件下，于 BAPPS-Val 上达到 69.44% 的 2AFC 准确率，在压缩图像 2AFC 基准上达到 83.80%，接近人类水平。进一步地，通过自集成（self-ensembling）——即对多个随机种子下的 VLM 评分求和取多数投票——VLM 对人类判断的预测能力随测试时计算量增加而单调提升（Figure 5）。这一发现为将 VLM 二元判断作为训练信号提供了可靠依据。

![[assets/figures/papers/paper_list_l808_https_arxiv_org_abs_2512_15701/figures/006_Table_2.jpg]]
*Table 2: Human 2AFC benchmarks. Gemini 2.5-Flash can replicate human judgments on 2AFC datasets zero-shot. †Number taken from paper*

![[assets/figures/papers/paper_list_l808_https_arxiv_org_abs_2512_15701/figures/008_Figure_5.jpg]]
*Figure 5: Scaling self-ensembling. The VLM becomes more predictive of human judgment on BAPPS [23] as test-time compute (number of VLM seeds) is scaled*

### 奖励设计消融

Table 3 的消融实验揭示了奖励设计中各组件的因果贡献：

![[assets/figures/papers/paper_list_l808_https_arxiv_org_abs_2512_15701/figures/009_Table_3.jpg]]
*Table 3: Ablation study. Various components of reward design are necessary for best performance*

- **完全去除 Diffusion DPO 后训练**（仅使用预训练模型）在所有评估指标上表现最差，确认了后训练本身的必要性。
- **仅使用 VLM 奖励（不集成 LPIPS）** 会改善分布度量（FID、FD-DINO），但损害像素对齐度量（PSNR、LPIPS）；集成 LPIPS 后实现了更好的综合平衡。
- **去除自集成** 导致多数指标明显下降，表明 VLM 输出的噪声需要集成策略来抑制。
- **在线 Diffusion DPO** 定期刷新偏好缓冲区，其效果优于预先构建离线偏好数据集（Section 4）。

这些结果共同支撑了一个核心设计原则：VLM 偏好信号与 LPIPS 感知约束的联合使用，是取得人类对齐与像素保真度之间最优权衡的关键。

### 失败模式与局限

尽管 VLM 评判能力总体可靠，论文揭示了若干值得注意的失败模式：

**VLM 幻觉与自不一致性**。当候选重建高度相似时，VLM 可能产生幻觉，表现为对同一图像对在顺序反转后给出矛盾评分（Figure 6）。自集成和 LPIPS 集成在一定程度上缓解了此问题，但无法完全消除。

**文本审查退化**。当引入基于编辑距离的文本可读性奖励时，模型退化为将所有可读文本模糊化（Figure 8），说明直接优化特定任务的 VLM 奖励可能产生非预期的负面效果，需要谨慎设计安全约束。

**依赖性与泛化边界**。方法依赖闭源 VLM（Gemini 2.5 Flash），其可用性和推理成本限制了复现与部署。此外，模型仅在 256×256 分辨率上训练，高分辨率图像的平铺推理虽可行，但可能引入边界伪影或效率损失。部分基线方法（PerCo、PO-ELIC、HFD）未公开代码或完整重建，限制了绝对公平的全面比较。

### 开放问题

基于上述分析，若干方向值得进一步探索：VLM 的感知评判能力在医学影像、遥感等非自然场景图像上是否同样可靠；能否将 VLM 的细粒度视觉理解（如对象识别、文本可读性）定制为特定任务的压缩奖励并安全地避免退化；如何在保持人类对齐的前提下降低 VLM 集成的计算开销；该方法能否借助时序 VLM 判断扩展到视频压缩；以及 VLM 后训练思路能否与更先进的扩散自编码器架构结合以持续提升压缩感知质量。

### 补充图表

![[assets/figures/papers/paper_list_l808_https_arxiv_org_abs_2512_15701/figures/007_Figure_6.jpg]]
*Figure 6: Failure modes. VLMs can hallucinate an incorrect ranking when the images are highly similar, such as in this case when the VLM fails to be self-consistent when the order of reconstructed images is reversed*

![[assets/figures/papers/paper_list_l808_https_arxiv_org_abs_2512_15701/figures/013_Figure_8.jpg]]
*Figure 8: Censoring readable text. A failure case of an edit-distance based reward on readable text determined by the VLM causes the model to degenerate to censoring all readable text in the images*

## 方法谱系与知识库定位

### 生成式压缩的演进脉络

VLIC 的架构直接继承自 **FlowMo**（一种基于流匹配的扩散自编码器），唯一的架构差异是将 LFQ (Lookup-Free Quantization) 替换为 FSQ (Finite Scalar Quantization)。这一替换本身不改变方法谱系的根本定位——VLIC 的核心贡献不在架构创新，而在后训练范式的突破。

在生成式图像压缩领域，VLIC 需要与两条技术路线对话：**GAN-based 压缩**（如 **HiFiC**）和 **diffusion-based 压缩**（如 **PerCo**、**HFD**）。前者在高感知质量下常伴随模式坍塌和纹理伪影；后者虽能生成更丰富的细节，但扩散采样的随机性使得解码结果与原始图像的像素对齐度难以保证。VLIC 通过 Diffusion DPO 后训练，在保持扩散模型生成多样性的同时，将解码偏好向人类视觉判断收缩，本质上是在扩散压缩框架上叠加了一层“偏好约束”的微调机制。

### 与现有感知度量的关系

传统压缩优化中，**LPIPS** 是事实上的感知损失标准。然而 LPIPS 本身是固定网络（如 AlexNet 或 VGG）提取的特征空间距离，其与人类判断的对齐程度受限于该网络的表征能力。VLIC 的洞察在于：**VLM 的零样本 2AFC 判断可以作为比 LPIPS 更贴近人类偏好的奖励信号**，但单独使用 VLM 奖励会损害像素对齐度量（PSNR 下降、LPIPS 恶化），而单独使用 LPIPS 则无法捕捉人类对纹理、文字、人脸等语义敏感区域的偏好。因此 VLIC 采取“一致性集成”策略——仅当 LPIPS 与 VLM 对偏好对的判断一致时，才将该样本纳入 Diffusion DPO 训练（见 Table 3 消融证据）。

这种集成策略的方法论意义在于：**VLIC 并非用 VLM 替代 LPIPS，而是将 VLM 作为 LPIPS 的“语义过滤器”**，在保留像素级约束的同时引入高层视觉偏好。这一设计思路与直接训练一个 VLM-distilled 感知网络（如将 VLM 判断蒸馏为可微分损失函数）形成对比——VLIC 选择通过偏好优化间接利用 VLM 信号，避免了蒸馏过程中的信息损失和架构复杂性。

### 偏好优化方法的定位

VLIC 采用的 Diffusion DPO 源自大语言模型对齐领域的 DPO 范式，经 **Diffusion-DPO** 适配至扩散模型。与 RLHF（如基于 PPO 的扩散模型微调）相比，DPO 无需显式训练奖励模型，直接利用偏好对优化策略，训练更稳定且计算开销更低。VLIC 进一步引入了**在线偏好缓冲区**机制——在训练过程中定期用当前模型重新生成候选重建并获取 VLM 评分，而非依赖预构建的离线偏好数据集。消融实验表明，在线更新策略优于离线固定数据集，这揭示了压缩偏好优化的一个关键特性：**偏好分布随模型能力变化而漂移，静态偏好数据集无法持续提供有效的训练信号**。

### 适用边界与局限

**分辨率约束与零样本泛化**。VLIC 模型仅在 256×256 的 ImageNet 上训练，对高分辨率图像采用平铺推理（tiled inference with MultiDiffusion）。这一策略虽支持任意分辨率，但平铺边界需要足够的重叠像素（文中使用 8 像素边距）来传递扩散过程中的跨块信息，否则会产生明显的拼接伪影。这种“训练-推理分辨率解耦”是以推理计算量和潜在的边界质量损失为代价的。

**VLM 依赖的脆弱性**。VLIC 使用闭源的 **Gemini 2.5 Flash** 作为评判器，其可用性、推理成本和版本稳定性均不受研究者控制。更关键的是，VLM 存在幻觉问题：当候选重建高度相似时，VLM 可能在图像顺序反转时给出矛盾评分（Figure 6），破坏偏好对的自一致性。VLIC 通过自集成（多次随机种子下的多数投票）和与 LPIPS 的一致性过滤来缓解这一问题，但并未从根本上消除 VLM 判断噪声对训练的影响。

**特定奖励的退化风险**。论文明确记录了基于编辑距离的文本可读性奖励会导致模型退化为审查所有可读文本（Figure 8），将文字区域模糊化。这一失败模式揭示了将 VLM 的细粒度视觉理解能力定制为特定压缩奖励时的潜在风险：**优化单一可量化目标可能诱导模型采取与人类意图相悖的捷径策略**。

**公平性与数据分布**。论文未讨论模型在不同人群或图像内容类型上的公平性表现。评估数据集（MS-COCO、CLIC 2020/2022）以自然场景为主，对医学影像、遥感图像、低光照条件或特定文化场景的泛化能力缺乏验证。VLM 本身的训练数据偏差也可能通过偏好信号传递至压缩模型。

### 开放问题与后续方向

1. **跨领域泛化**：VLM 的感知评判能力在医学影像、遥感、工业检测等专业领域是否同样可靠？这些领域的人类专家判断可能与通用 VLM 的“常识性”视觉偏好存在系统性偏差。

2. **细粒度奖励的安全设计**：如何将 VLM 的对象识别、文本可读性等细粒度能力定制为压缩奖励，同时避免类似文本审查的退化现象？可能需要引入多目标约束或对抗性奖励设计。

3. **计算效率优化**：自集成需要多次 VLM 调用（Figure 5 显示集成规模增大可提升与人类判断的一致性），在线偏好缓冲区需要持续推理，这使得后训练的计算开销显著高于传统 LPIPS 微调。如何在保持对齐质量的前提下降低 VLM 推理频次，是该方法走向实用的关键瓶颈。

4. **视频压缩的时序扩展**：VLIC 的 2AFC 偏好框架理论上可借助时序 VLM 判断扩展至视频压缩，但视频的时序一致性和运动感知偏好引入了新的维度，需要重新设计偏好收集和后训练策略。

5. **与更先进架构的结合**：VLIC 的后训练范式与底层扩散自编码器架构解耦，理论上可应用于任何支持偏好优化的生成式压缩模型。随着扩散模型和自编码器架构的持续进步，该方法的上限有望进一步提升。

---

**需要手动验证的内容**：部分基线方法（PerCo、PO-ELIC、HFD）未公开代码或完整重建结果，论文中的定量比较可能存在评估偏差；HiFiC 等方法的作者/年份/会议元数据在提供的分析中缺失，建议查阅原论文补充完整引用信息。

## 原文 PDF

![[paperPDFs/CVPR_2026/VLIC_Vision_Language_Models_As_Perceptual_Judges_for_Human_Aligned_Image_Compression.pdf]]
