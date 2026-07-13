---
title: "FlashIn: Fast and Accurate Image Inversion for Real-time Image Editing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FlashIn_Fast_and_Accurate_Image_Inversion_for_Real_time_Image_Editing.pdf
project_link: null
code_link: null
aliases:
- FlashIn
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 为反演网络提供明确的噪声-图像对作为训练目标（循环一致性损失），并结合对抗训练对齐合成与真实分布，显著提升反演精度和细节保留。
primary_logic: 利用生成模型产生已知噪声种子的合成图像，训练一个直接映射图像到噪声的神经网络，并用循环一致性和对抗学习保证重建质量，实现1-4步的高质量反演。
claims:
- FlashIn 在 PIE-Bench 上达到最佳背景保留（PSNR 31.91）和编辑保真度（CLIP 评分 23.94），远超现有方法。
- 循环一致性训练使背景保留和编辑保真度显著提升（PSNR 从 26.19 到 28.40），对抗训练进一步提升（到 31.91）。
- 对抗训练显著恢复重建图像中的细节（如草地质感）。
- PIE-Bench 上 PSNR (背景保留) = 31.91 (cycle+adversarial)
---

# FlashIn: Fast and Accurate Image Inversion for Real-time Image Editing

> [!tip] 核心洞察
> 利用生成模型产生已知噪声种子的合成图像，训练一个直接映射图像到噪声的神经网络，并用循环一致性和对抗学习保证重建质量，实现1-4步的高质量反演。

| 字段 | 内容 |
|------|------|
| 中文题名 | FlashIn：面向实时图像编辑的快速精确图像反演 |
| 英文题名 | FlashIn: Fast and Accurate Image Inversion for Real-time Image Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_FlashIn_Fast_and_Accurate_Image_Inversion_for_Real-time_Image_Editing_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FlashIn |
| Dataset | PIE-Bench |

> [!tip] 效果简介
> - PIE-Bench 上，PSNR (背景保留) 31.91 (cycle+adversarial) vs 26.19 (无 cycle 和 adversarial 的基线) (+5.72)；SSIM (×10²) 88.76 vs 81.47 (+7.29)；CLIP 相似度 (Whole) 25.67 vs 24.88 (+0.79)。
> - PIE-Bench (作为插件与 Flux-Kontext 配合) 上，LPIPS (×10³) 降低 31.44 (with FlashIn noise) vs 38.44 (with random noise) (-7.00)。
> - 推理速度 上，总编辑时间 (秒) ~1.04 (单步反演+生成) vs >10 (多步 DDIM 等方法) (快一个数量级)。

## 概要

### 问题瓶颈

图像反演（inversion）是扩散模型图像编辑的核心步骤，旨在从给定图像恢复其对应的初始噪声，以支持后续的编辑生成。现有方法普遍依赖 DDIM 反演等近似逆向过程，需要数十步迭代，导致三个关键瓶颈：（1）**误差累积**——每步近似引入偏差，最终重建出现伪影与背景失真；（2）**速度慢**——多步迭代使编辑过程耗时超过 10 秒，无法满足实时交互需求；（3）**目标缺失**——训练式反演方法缺乏明确的噪声-图像监督信号，仅依赖重建损失与 KL 正则化，难以精确还原细节。

### 核心思路

FlashIn 提出了一种根本性的范式转换：**将反演从多步近似过程重新定义为单步神经网络直接映射**。其核心洞察是：利用生成模型自身产生已知噪声种子的合成图像，训练一个反演网络学习图像到噪声的直接映射，并通过循环一致性和对抗训练保证重建质量。

具体而言，方法包含三个关键设计：
- **直接映射**：训练神经网络 $F$，将图像潜在表示直接映射回初始噪声，实现 1–4 步内完成反演。
- **循环一致性训练**：引入 $\mathcal{L}_{cycle}$ 损失，包含噪声匹配项与潜在空间重建项，为反演网络提供明确的优化目标。
- **对抗训练**：引入判别器 $D$ 区分重构潜在与真实潜在，促使重构图像分布向真实图像对齐，恢复纹理细节（如草地质感、岩石纹理）。

### 方法谱系与知识库定位

FlashIn 位于**基于学习的快速反演**这一新兴技术路线。与之对比：

| 方法 | 反演范式 | 代表工作 |
|------|----------|----------|
| 标准 DDIM 反演 | 多步近似逆向 ODE | **DDIM Inversion** (Song et al., ICLR 2021) |
| 基于优化的反演 | 逐样本优化空文本嵌入 | **Null-text Inversion** (Mokady et al., CVPR 2023) |
| 可逆扩散反演 | 构造可逆扩散过程 | **EDICT** (Wallace et al., CVPR 2023) |
| 定点迭代反演 | 迭代精炼噪声估计 | **ReNoise** (Garibi et al., ECCV 2024) |
| 编码器式反演 | 编码器学习反演映射 | **TurboEdit** (Wu et al., ECCV 2024) |
| 合成数据训练 | 合成数据监督训练 | **SwiftEdit** (Nguyen et al., arXiv 2024) |
| 整流流反演 | 基于整流流的逆向 | **FireFlow** (Deng et al., 2024) |
| **FlashIn（本文）** | **单步直接映射 + 循环一致 + 对抗** | 本文 |

FlashIn 的关键差异化在于：首次将循环一致性损失与对抗训练引入反演网络训练，使得合成数据训练的模型能够泛化到真实图像，同时保持 1 步推理的实时性。

### 主要结果

在 PIE-Bench 基准上，FlashIn 取得了全面的最优表现：
- **背景保留**：PSNR 达到 31.91，较无循环一致性与对抗训练的基线（26.19）提升 +5.72 dB；SSIM 从 81.47 提升至 88.76。
- **编辑保真度**：Edited CLIP 相似度达到 23.94，优于所有对比方法。
- **推理速度**：总编辑时间约 1.04 秒（单步），比多步 DDIM 方法快一个数量级。

消融实验证实了各组件的因果作用：循环一致性训练使 PSNR 从 26.19 提升至 28.40，对抗训练进一步推高至 31.91（Table 2）。定性结果（Figure 5）显示，对抗训练显著恢复了重建图像中的纹理细节。此外，FlashIn 可作为插件直接提升指令式编辑方法（如 Flux-Kontext）的背景保留，LPIPS 从 38.44 降至 31.44（Table 3）。

### 局限与展望

当前方法存在以下局限：（1）仅支持图像编辑，尚未扩展到视频或 3D 场景；（2）依赖生成模型合成数据训练，对训练域外真实图像的泛化虽经对抗训练缓解，但仍需进一步验证；（3）多步推理（4 步）虽提升质量，但计算开销增加，实时性有所折损。未来工作将聚焦于视频反演扩展、跨生成模型泛化增强，以及在更少步骤下达到多步相当的质量。



图像编辑是视觉内容创作的核心需求，而基于扩散模型的生成式编辑方法近年来取得了显著进展。这类方法通常遵循“反演-编辑-重建”范式：先将真实图像反演至扩散模型的噪声空间，在噪声或潜在空间施加编辑操作，再通过去噪过程生成编辑后的图像。反演质量直接决定了编辑结果对原始图像结构的保真度——背景是否完整保留、物体轮廓是否准确还原，均取决于反演过程能否精确捕捉图像对应的初始噪声。

**现有反演方法的瓶颈**。当前主流反演方法依赖扩散模型的近似逆向过程，最典型的代表是 **DDIM Inversion**（Song et al., ICLR 2021），它利用确定性去噪调度将图像逐步逆向映射至噪声空间。然而，这一过程存在根本性缺陷：DDIM 反演需要数十步迭代，每一步的线性近似都会引入误差，误差在长序列中不断累积，最终导致重建图像出现模糊、伪影和细节丢失。后续方法试图从不同角度缓解这一问题——**Null-text Inversion**（Mokady et al., CVPR 2023）引入空文本优化来修正反演偏差，**EDICT**（Wallace et al., CVPR 2023）通过可逆扩散过程保证数学精确性，**ReNoise**（Garibi et al., ECCV 2024）采用定点迭代策略逐步逼近真实噪声——但这些方法本质上仍是多步迭代框架，计算开销大（编辑过程通常超过10秒），且精度提升有限，难以满足实时编辑需求。

**速度与精度的双重困境**。如图 1 所示，现有方法在 PIE-Bench 基准上呈现出明显的速度-质量权衡：基于优化的方法（如 Null-text Inversion）背景保留较好但耗时极长，基于编码器的方法（如 **TurboEdit**，Wu et al., ECCV 2024）速度较快但编辑保真度不足。这一困境的根源在于，现有方法缺乏对反演目标的明确定义——它们试图通过逆向求解扩散过程来“猜测”初始噪声，而非直接学习从图像到噪声的映射关系。

**本文动机**。FlashIn 的核心洞察在于：既然生成模型本身可以从已知噪声种子产生合成图像，那么这些噪声-图像对就构成了天然的训练数据。通过训练一个神经网络直接学习图像到噪声的映射，可以绕过迭代近似的误差累积问题，将反演过程压缩至1-4步。然而，仅依靠像素级重建损失训练的反演网络难以保证重建图像与真实图像的分布一致性，容易丢失纹理细节。为此，FlashIn 引入两个关键机制：**循环一致性训练**——通过噪声匹配和潜在空间重建的双重回环约束，为反演网络提供明确的优化目标；**对抗训练**——利用判别器对齐重构图像与真实图像的分布，恢复反演过程中丢失的细粒度细节（如草地质感、岩石纹理）。这一设计使得 FlashIn 在 PIE-Bench 上实现了最佳背景保留（PSNR 31.91）和编辑保真度（CLIP 评分 23.94），同时将编辑时间压缩至约1秒，较传统方法快一个数量级。



## 核心方法与创新机理

FlashIn 的核心突破在于**将图像反演从多步近似逆向过程重新定义为单步神经网络直接映射问题**，并通过显式训练目标与分布对齐机制解决了精度与速度的长期矛盾。

### 从多步近似到单步直接映射

传统图像编辑依赖 DDIM inversion（**DDIM Inversion**，Song et al., ICLR 2021）等近似逆向过程，需要在扩散模型上执行数十步去噪操作，每一步都会引入近似误差，最终导致误差累积、重建伪影和背景失真。**Null-text Inversion**（Mokady et al., CVPR 2023）等基于优化的方法虽然提高了精度，但进一步增加了时间开销。**EDICT**（Wallace et al., CVPR 2023）和 **ReNoise**（Garibi et al., ECCV 2024）分别从可逆扩散和定点迭代的角度改进，但本质上仍受困于多步推理的效率瓶颈。

FlashIn 做出了根本性的架构转变：训练一个神经网络 $F$，将干净潜在表示直接映射回其种子噪声 $\hat{\epsilon} = F(\mathbf{z}_0, \mathbf{c}, T)$。这一参数化方式将反演从“模拟逆向过程”变为“学习映射函数”，使得反演仅需 1–4 步即可完成，总编辑时间约 1.04 秒，比多步方法快一个数量级。

### 循环一致性：为反演网络提供显式训练目标

此前的反演方法缺乏明确的训练目标——它们或依赖扩散模型自身的近似逆向过程，或仅在合成数据上使用简单的重建损失。FlashIn 的关键创新在于**利用生成模型自身产生已知噪声种子的合成图像，构建噪声-图像对作为监督信号**，并引入循环一致性损失 $\mathcal{L}_{cycle} = \mathcal{L}_{cycle}^1 + \mathcal{L}_{cycle}^2$：

- $\mathcal{L}_{cycle}^1$：约束预测噪声 $\hat{\epsilon}$ 与真实种子噪声 $\epsilon$ 的匹配；
- $\mathcal{L}_{cycle}^2$：约束重建潜在 $\hat{\mathbf{z}}_0$ 与原始潜在 $\mathbf{z}_0$ 的保真度。

这一设计形成了“噪声→图像→噪声”的闭环约束，确保反演网络学到的是精确可逆的映射。消融实验（Table 2）证实，仅加入循环一致性训练就将背景保留 PSNR 从 26.19 提升至 28.40，编辑保真度 CLIP 评分也同步改善。

### 对抗训练：对齐合成与真实分布

仅依赖合成数据训练的反演网络面临分布偏移问题——合成图像与真实图像在细节纹理上存在差异，导致重建结果丢失高频信息。FlashIn 引入判别器 $D$ 对重建潜在与真实潜在进行对抗训练：

$$\mathcal{L}_{adv}^F = -\mathbb{E}_{\hat{\mathbf{z}}_0 \sim G(F(\cdot))}[D(G(F(\hat{\mathbf{z}}_0, \mathbf{c}, T)))]$$

对抗损失促使反演-生成管线输出的图像分布向真实图像分布靠拢。如 Figure 5 所示，加入对抗训练后，草地纹理和岩石质感等细节得到显著恢复。定量上，对抗训练将 PSNR 从 28.40 进一步提升至 31.91（Table 2），证明了分布对齐对细节保留的关键作用。

### 多步推理的灵活扩展

FlashIn 的架构天然支持多步推理：通过将前一步的重建结果作为下一步的输入，形成迭代精炼过程。Figure 6 表明，从 1 步增加到 4 步可逐步减少模糊和细节丢失，在保持实时性的前提下提供质量调节的灵活性。训练时随机采样时间步 $T \in [1.0, 0.75, 0.5, 0.25]$，使网络学会在不同噪声水平下进行反演，推理时可采用任意步数配置。

### 作为即插即用模块的通用性

FlashIn 产生的反演噪声可作为插件嵌入其他编辑框架。Table 3 显示，将 FlashIn 噪声替换随机噪声用于 **Flux-Kontext** 指令编辑方法时，LPIPS 从 38.44 降至 31.44，验证了其作为通用反演模块的潜力。



FlashIn 的核心思想是将图像反演从多步迭代过程重构为一个可训练的神经网络映射，实现从图像潜在表示到初始噪声的直接预测。整个框架围绕一条“生成 → 反演 → 重建”的闭环展开，通过合成数据驱动训练，无需依赖真实图像的噪声标签。

### 模块组成与数据流

框架由四个核心模块构成，其中仅反演网络和判别器参与训练，其余模块保持冻结：

1. **VAE 编码器 E**（预训练冻结）：将输入图像 $x$ 压缩到潜在空间，得到 $z = E(x)$。这一步将高维图像映射为扩散模型可操作的紧凑表示。

2. **反演网络 F**（可训练）：框架的核心创新。F 学习从干净潜在 $z_0$ 到其种子噪声的映射 $\hat{\epsilon} = F(z_0, c, T)$，其中 $c$ 为文本条件，$T$ 为时间步集合。与 DDIM inversion 的迭代近似不同，F 通过单次前向传播即可完成反演。

3. **生成器 G**（冻结，如 Flux.1-Schnell）：单步文本到图像模型，根据噪声和文本提示生成干净潜在 $z_0 = G(\epsilon, c, T)$。G 在训练时用于产生监督信号，在推理时用于编辑生成。

4. **判别器 D**（仅训练时使用）：区分重构潜在与真实潜在，通过对抗训练使重建图像更贴近真实分布。

数据流遵循“合成 → 反演 → 重建 → 对齐”的闭环，如 Figure 3 所示：

![[assets/figures/papers/paper_list_l872_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlashIn_Fast_and/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our method. At each step, random noise*

- **合成阶段**：从标准高斯分布采样随机噪声 $\epsilon \sim \mathcal{N}(0, 1)$，通过冻结的生成器 G 生成图像潜在 $z_0 = G(\epsilon, c, T)$。此时 $(\epsilon, z_0)$ 构成天然的噪声-图像训练对。
- **反演阶段**：将生成的 $z_0$ 送入反演网络 F，预测其对应的种子噪声 $\hat{\epsilon} = F(z_0, c, T)$。
- **重建阶段**：用预测噪声 $\hat{\epsilon}$ 再次通过 G 生成重建潜在 $\hat{z}_0 = G(\hat{\epsilon}, c, T)$，形成完整的循环。
- **对齐阶段**：判别器 D 对 $\hat{z}_0$ 和 $z_0$ 进行真假判别，驱动 F 产生更逼真的重建结果。

### 训练目标

FlashIn 的训练目标由三个互补的损失函数组成：

- **循环一致性损失** $\mathcal{L}_{cycle}$：包含噪声匹配项 $\mathcal{L}_{cycle}^1 = \|\epsilon - \hat{\epsilon}\|_2^2$ 和潜在重建项 $\mathcal{L}_{cycle}^2 = \lambda \|z_0 - \hat{z}_0\|_2^2$。前者直接监督噪声预测精度，后者约束重建图像与原图一致，共同保证反演的准确性。

- **对抗损失** $\mathcal{L}_{adv}$：训练判别器 D 区分真实潜在 $z_0$ 与重建潜在 $\hat{z}_0$，同时训练 F 欺骗 D，使重建图像保留更丰富的纹理细节（如草地质感、岩石纹理，见 Figure 5）。

- **正则化项** $\mathcal{L}_{reg}$：防止过拟合，稳定训练过程。

完整优化目标为：
$$\mathcal{L}_{full} = \mathcal{L}_{cycle} + \mathcal{L}_{reg} + \mathcal{L}_{adv}^D + \mathcal{L}_{adv}^F$$

### 推理流程

推理时，给定输入图像 $x$ 和编辑指令（目标文本提示 $c'$），编辑过程可表示为：
$$\mathbf{z}_0' = G(F(z_0, c, T), c', T)$$

即：VAE 编码 → 反演网络预测噪声 → 生成器以新文本条件生成编辑结果。整个过程仅需 1-4 步推理，总耗时约 1 秒（单张 A100 GPU），相比 DDIM inversion 等需要数十步的方法快一个数量级。

### 设计优势

与现有反演方法相比，FlashIn 的框架设计有三个关键改变：
- **反演方式**：从多步近似逆向过程（DDIM inversion）变为单步神经网络直接映射，消除了误差累积问题。
- **训练目标**：从缺乏明确目标的隐式学习变为循环一致性损失提供的显式噪声-图像监督，显著提升反演精度。
- **分布对齐**：引入对抗训练，使重建结果从合成分布向真实图像分布靠拢，恢复细节信息。

消融实验证实了这一设计的有效性：循环一致性训练将背景保留 PSNR 从 26.19 提升至 28.40，对抗训练进一步推高至 31.91（Table 2），验证了各模块的贡献。



### 方法概览

FlashIn 的核心思想是将图像反演重新参数化为一个可训练的神经网络，直接学习从干净潜变量到种子噪声的映射，从而绕过传统多步 DDIM 反演带来的误差累积和速度瓶颈。整个框架包含四个关键模块（见 Figure 3）：

- **VAE 编码器 E**（冻结）：将输入图像压缩到潜空间，得到潜变量 $\mathbf{z}_0 = E(\mathbf{x})$。
- **反演网络 F**（可训练）：学习映射 $\hat{\epsilon} = F(\mathbf{z}_0, \mathbf{c}, T)$，其中 $\mathbf{c}$ 为文本条件，$T$ 为时间步集合。
- **生成器 G**（冻结）：采用少步扩散模型（如 Flux.1-Schnell），根据文本提示从噪声生成干净潜变量 $\mathbf{z}_0 = G(\epsilon, \mathbf{c}, T)$。
- **判别器 D**（仅训练时使用）：区分重构潜变量与真实潜变量，驱动对抗训练以恢复细节。

训练时，随机采样噪声 $\epsilon \sim \mathcal{N}(0, 1)$，通过冻结的生成器 G 产生合成图像-噪声对 $(\mathbf{z}_0, \epsilon)$，反演网络 F 学习从 $\mathbf{z}_0$ 预测 $\epsilon$。推理时，给定真实图像经 E 编码得到 $\mathbf{z}_0$，F 直接输出对应噪声，再通过 G 用编辑后的文本提示 $\mathbf{c}'$ 生成编辑结果，实现单步编辑：

$$\mathbf{z}_0' = G(F(\mathbf{z}_0, \mathbf{c}, T), \mathbf{c}', T)$$

### 循环一致性损失

为确保反演的精确性，FlashIn 设计了双重循环一致性损失，直接为反演网络提供明确的训练目标：

$$\mathcal{L}_{cycle} = \mathcal{L}_{cycle}^1 + \mathcal{L}_{cycle}^2$$

- **$\mathcal{L}_{cycle}^1$（噪声匹配损失）**：约束预测噪声 $\hat{\epsilon}$ 与真实种子噪声 $\epsilon$ 一致：
  $$\mathcal{L}_{cycle}^1 = \|\epsilon - \hat{\epsilon}\|_2^2$$

- **$\mathcal{L}_{cycle}^2$（潜空间重建损失）**：将预测噪声 $\hat{\epsilon}$ 重新输入生成器 G，约束重建潜变量 $\hat{\mathbf{z}}_0 = G(\hat{\epsilon}, \mathbf{c}, T)$ 与原始潜变量 $\mathbf{z}_0$ 一致：
  $$\mathcal{L}_{cycle}^2 = \lambda \|\mathbf{z}_0 - \hat{\mathbf{z}}_0\|_2^2$$
  其中 $\lambda$ 为平衡超参数。

该设计的核心因果机制在于：通过生成模型产生已知噪声种子的合成数据，为反演网络提供“噪声-图像”真值对，使训练信号直接且无歧义，从而从根本上消除了传统 DDIM 反演中近似误差累积的问题。消融实验证实，引入循环一致性训练后，背景保留 PSNR 从 26.19 提升至 28.40（Table 2）。

### 对抗训练对齐分布

尽管循环一致性损失保证了噪声预测的准确性，但合成数据训练的模型在真实图像上仍可能出现细节丢失。FlashIn 进一步引入对抗训练，对齐重构图像与真实图像的分布：

- **判别器损失**：
  $$\mathcal{L}_{adv}^D = -\mathbb{E}_{\mathbf{z}_0 \sim p_{real}}[\log D(\mathbf{z}_0)] - \mathbb{E}_{\hat{\mathbf{z}}_0 \sim G(F(\cdot))}[\log(1 - D(\hat{\mathbf{z}}_0))]$$

- **生成器（反演网络）对抗损失**：
  $$\mathcal{L}_{adv}^F = -\mathbb{E}_{\hat{\mathbf{z}}_0 \sim G(F(\cdot))}[D(\hat{\mathbf{z}}_0)]$$

判别器 D 在潜空间区分真实图像潜变量与重构潜变量，驱动反演网络 F 产生更逼真的重建结果。如 Figure 5 所示，加入对抗训练后，草地纹理、岩石质感等细粒度细节得到显著恢复，背景保留 PSNR 进一步提升至 31.91（Table 2）。

![[assets/figures/papers/paper_list_l872_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlashIn_Fast_and/figures/008_Figure_5.jpg]]
*Figure 5: Comparison of reconstruction results with and without adversarial learning. With the introduction of adversarial learning, the reconstruction results preserve more textual and fine-grained details, e.g. the details of the grass and the texture of the rocks*

### 完整训练目标

综合以上组件，FlashIn 的完整优化目标为：

$$\mathcal{L}_{full} = \mathcal{L}_{cycle} + \mathcal{L}_{reg} + \mathcal{L}_{adv}^D + \mathcal{L}_{adv}^F$$

其中 $\mathcal{L}_{reg}$ 为针对反演网络的正则化项（如权重衰减），防止过拟合到合成数据分布。

### 多步推理扩展

FlashIn 原生支持多步反演以进一步提升质量。训练时，时间步集合 T 从 [1.0, 0.75, 0.5, 0.25] 中随机选取，使单一网络学会处理不同噪声水平。推理时，可串联执行多步反演，每步将上一步的重建结果作为输入，逐步细化噪声预测。Figure 6 表明，增加推理步数（1→4）可减少模糊和细节丢失，但会相应增加计算开销。论文主要结果均采用 4 步推理，总编辑时间约 1.04 秒，仍比多步 DDIM 方法快一个数量级。



## 实验与关键发现

### 主实验结果

FlashIn 在 PIE-Bench 基准上进行了全面的定量与定性评估，与 DDIM Inversion、Null-text Inversion、EDICT、ReNoise、TurboEdit、SwiftEdit、FireFlow 等方法进行了系统对比。Table 1 汇总了各方法在背景保留和编辑保真度上的表现，所有时间测量均在单张 A100 GPU 上完成。

![[assets/figures/papers/paper_list_l872_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlashIn_Fast_and/figures/005_Table_1.jpg]]
*Table 1: Comparison with image editing methods on PIE-Bench [16]. The time cost is evaluated on a single A100 GPU. Our method achieves the best overall background preservation and editing fidelity compared to all competitors. Specifically, it excels in multiple metrics, demonstrating superior performance in maintaining background integrity while ensuring high editing fidelity*

**背景保留**：FlashIn 在四个背景保留指标中的三个取得最优。PSNR 达到 31.91，SSIM（×10²）达到 88.76，LPIPS（×10³）为 31.44。相比之下，基于优化的 Null-text Inversion 和定点迭代的 ReNoise 在 PSNR 上均低于 FlashIn，且时间开销大一个数量级以上。

**编辑保真度**：FlashIn 在 Whole CLIP 相似度（25.67）和 Edited CLIP 相似度（23.94）上均领先所有对比方法。这表明反演得到的噪声能够更准确地保留源图像结构，同时充分响应目标编辑指令。

**推理速度**：FlashIn 的单步推理总编辑时间约 1.04 秒（反演 + 生成），而多步 DDIM 等方法通常超过 10 秒，速度提升约一个数量级。Figure 1 的气泡图直观展示了 FlashIn 在速度-质量权衡上的显著优势：气泡最小（时间最少），同时位于 PSNR 和 CLIP 评分的右上角区域。

**定性对比**：Figure 4 展示了与现有方法的可视化编辑对比。在对象替换（A、B）任务中，FlashIn 更好地保留了背景细节和结构；在内容修改（C、D、E）任务中，FlashIn 的编辑结果更贴合目标描述，伪影更少。

### 消融实验

Table 2 系统验证了各训练策略的贡献，以无循环一致性和无对抗训练的版本作为基线。

![[assets/figures/papers/paper_list_l872_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlashIn_Fast_and/figures/006_Table_2.jpg]]
*Table 2: Validation of training strategies of FlashIn on the PIE-Bench [16]*

**循环一致性训练的影响**：引入循环一致性损失后，PSNR 从 26.19 提升至 28.40（+2.21），SSIM 从 81.47 提升至 86.32，Edited CLIP 相似度从 22.43 提升至 23.32。这表明显式的噪声-图像对监督和潜在空间重建约束是反演精度的关键保障。

**对抗训练的影响**：在循环一致性基础上加入对抗训练，PSNR 进一步提升至 31.91（+3.51），SSIM 达到 88.76，Edited CLIP 相似度达到 23.94。Figure 5 的可视化对比显示，对抗训练显著恢复了重建图像中的细粒度纹理，如草地质感和岩石纹理，这些细节在仅使用循环损失时存在明显模糊或丢失。

**推理步数的影响**：Figure 6 展示了从 1 步到 4 步推理的编辑结果变化。增加推理步数逐步提高了编辑质量，减少了模糊和细节丢失。4 步推理在细节保留和编辑一致性上达到最佳平衡，但步数增加会带来额外的计算开销，实时性略有下降。

### 作为插件的泛化性

Table 3 验证了 FlashIn 作为即插即用模块的泛化能力。将 FlashIn 产生的噪声替换随机噪声用于指令编辑方法（如 Flux-Kontext）时，LPIPS（×10³）从 38.44 降至 31.44，降幅达 7.00。Figure 7 的可视化对比进一步证实，FlashIn 噪声相比随机噪声能更好地保留源图像的结构和背景，使编辑结果更忠实于原始内容。

![[assets/figures/papers/paper_list_l872_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlashIn_Fast_and/figures/009_Table_3.jpg]]
*Table 3: Plugging in our FlashIn into instruction-based editing methods leads to consistnt performance improvement*

![[assets/figures/papers/paper_list_l872_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlashIn_Fast_and/figures/007_Figure_7.jpg]]
*Figure 7: Editing results comparison between FlashIn produced noise and random noise. Our noise leads to better structure and background preservation in the editing result*

### 失败模式与局限性

尽管 FlashIn 在整体性能上表现优异，仍存在以下局限：

1. **域外泛化**：反演网络依赖生成模型产生的合成数据进行训练，对训练域外的真实图像可能泛化有限。对抗训练部分缓解了此问题，但在分布差异较大的场景下仍需手动验证。
2. **极端编辑指令**：在涉及复杂语义变换（如大幅改变物体空间关系）的编辑指令下，编辑一致性可能略有下降，表现为局部伪影或语义偏差。
3. **步数-质量权衡**：单步推理虽快，但在细节保留上不及 4 步推理；多步推理增加了计算开销，对实时性要求极高的场景需权衡。
4. **应用范围**：当前方法仅支持图像编辑，尚未扩展到视频或 3D 场景的时序一致反演。

### 补充图表

![[assets/figures/papers/paper_list_l872_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlashIn_Fast_and/figures/010_Figure_6.jpg]]
*Figure 6: Comparison of image editing with different inversion inference steps. The results are improved with more inference steps*

![[assets/figures/papers/paper_list_l872_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlashIn_Fast_and/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison between our method and existing image editing methods on PIE-Bench [16]. Our method shows better background preservation (A, B) and editing fidelity (C, D, E). This demonstrates that our method achieves more accurate noise inversion and high-quality image editing*

![[assets/figures/papers/paper_list_l872_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlashIn_Fast_and/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of previous image editing methods and ours on PIE-Bench [16]. The size of the circles indicates the time cost of the editing process. Our method achieves superior background preservation (measured by PSNR) and editing fidelity (assessed by CLIP Score relative to the target prompt), while incurring the least time cost*

![[assets/figures/papers/paper_list_l872_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlashIn_Fast_and/figures/002_Figure_2.jpg]]
*Figure 2: Our proposed inversion algorithm, FlashIn, achieves fast and precise image inversion, enabling high-quality real-time image editing. In this figure, we illustrate various editing outcomes produced by our method, including (a) object change, (b) object addition, (c) object removal, (d) identity change, (e) content change and (f) attribute change*



## 定位与知识库关联

### 1. 方法谱系：从多步近似到单步学习

FlashIn 的核心突破在于将扩散模型反演从“数值近似”范式转变为“数据驱动学习”范式。传统方法依赖扩散模型的逆向过程（如 DDIM inversion），本质上是通过常微分方程求解器逐步估计初始噪声，需要数十步迭代，导致误差累积、重建伪影和速度瓶颈。FlashIn 则用一个可训练的神经网络 $F$ 直接学习从干净潜在表示到种子噪声的映射关系，将反演过程压缩到 1-4 步内完成。

与现有反演方法的对比关系如下：

- **DDIM Inversion** (Song et al., ICLR 2021)：依赖确定性逆向 ODE 求解，需要完整的多步去噪过程，误差随步数累积，是 FlashIn 对比的标准基线。
- **Null-text Inversion** (Mokady et al., CVPR 2023)：通过优化空文本嵌入来修正 DDIM 反演中的重建误差，属于基于优化的后处理方案，计算开销更大。
- **EDICT** (Wallace et al., CVPR 2023)：构建可逆扩散过程以实现精确反演，但需要修改生成模型的采样机制，通用性受限。
- **ReNoise** (Garibi et al., ECCV 2024)：采用定点迭代逐步精炼反演噪声，仍需多步迭代，速度优势有限。
- **TurboEdit** (Wu et al., ECCV 2024)：使用编码器网络直接预测反演噪声，与 FlashIn 同属基于网络的方法，但缺少循环一致性和对抗训练机制，细节保留能力较弱。
- **SwiftEdit** (Nguyen et al., arXiv 2024)：利用合成数据训练反演网络，与 FlashIn 共享数据驱动思路，但未引入分布对齐机制。
- **FireFlow** (Deng et al., 2024)：基于整流流（rectified flow）的反演方法，在生成模型架构层面进行改造。

FlashIn 的差异化优势体现在三个关键设计维度：

1. **反演方式**：从多步近似逆向过程变为单步神经网络直接映射，推理速度提升一个数量级。
2. **训练目标**：从仅依赖重建损失和 KL 正则化变为循环一致性损失（噪声匹配 + 潜在空间重建）+ 对抗损失，为网络提供了明确的监督信号。
3. **分布对齐**：从仅在合成数据上训练变为引入对抗训练，使重构图像分布更接近真实图像分布，显著改善细节保留。

### 2. 知识库定位与适用边界

**适用场景**：FlashIn 当前聚焦于基于文本驱动的图像编辑任务，支持对象替换、添加、删除、身份变更、内容修改和属性修改等操作。其核心假设是编辑前后的图像应共享相同的底层噪声结构，因此特别适合需要保持背景和结构一致性的编辑场景。

**技术依赖**：方法依赖一个预训练的少步扩散模型（如 Flux.1-Schnell）作为生成器 $G$，以及一个预训练的 VAE 编码器 $E$ 用于潜在空间压缩。反演网络 $F$ 的训练数据完全由该生成模型合成，这意味着反演能力与特定生成模型绑定。

**局限性**：

- **模态限制**：目前仅支持图像编辑，尚未扩展到视频或 3D 场景，无法保证时序一致性。
- **域泛化风险**：训练数据完全由生成模型合成，对训练域外的真实图像可能泛化有限。尽管对抗训练缓解了合成-真实分布差异，但在极端域偏移场景下性能可能下降。
- **步数-质量权衡**：多步推理（如 4 步）虽提高了编辑质量，但增加了计算开销，单步推理在极端复杂的编辑指令下编辑一致性可能略有降低。
- **模型耦合**：反演网络与特定的生成模型（Flux-Schnell）强绑定，跨模型（如 SDXL、DALL·E）的迁移需要重新训练。

### 3. 开放问题

1. **时序扩展**：能否将 FlashIn 的单步反演思想扩展到视频域，实现时序一致的实时视频编辑？
2. **单步质量提升**：能否通过更强的训练策略或架构设计，在单步推理中达到与多步相当的质量和细节保留水平？
3. **跨模型泛化**：如何设计模型无关的反演网络，使其能够适配不同架构的扩散模型，降低迁移成本？
4. **安全性与可控性**：对抗训练引入的判别器可能影响生成结果的可控性，如何在保持细节恢复能力的同时确保编辑结果的安全性？



## 原文 PDF

![[paperPDFs/CVPR_2026/FlashIn_Fast_and_Accurate_Image_Inversion_for_Real_time_Image_Editing.pdf]]
