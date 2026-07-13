---
title: "gQIR: Generative Quanta Image Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/gQIR_Generative_Quanta_Image_Reconstruction.pdf
project_link: null
code_link: "https://github.com/Aryan-Garg/gQIR"
aliases:
- gQIR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入大规模文本‑图像扩散模型的语义与结构先验，并通过确定性均值编码和潜在空间对齐损失（LSA）约束编码器，避免在极端光子噪声下的灾难性遗忘，从而在稀疏量子观测下恢复可信的视觉内容。
primary_logic: 将互联网规模预训练的 Stable Diffusion 扩散先验适配到量子爆发成像的三阶段框架：阶段1 通过潜在空间对齐 VAE 实现联合去噪‑去马赛克；阶段2 对低秩适配（LoRA）U‑Net 进行对抗蒸馏，获得单步高感知质量生成器；阶段3 在潜在空间内设计伪3D FusionViT 实现运动感知的时空爆发融合，从而在极端运动与光子饥饿条件下同时获得高保真度和时序一致性。
claims:
- 在 3 位纳米爆发单帧重建中，gQIR 的感知质量（MUSIQ）显著优于微调的 Restormer 与 NAFNet，而后者因追求低失真而过度平滑。
- 在极端运动爆发重建中，gQIR 的 PSNR/SSIM/LPIPS 均大幅领先 QBP 和 QUIVER，尤其在 1000–100k fps 的高速场景下。
- 在 I2‑2k 基准上，gQIR 超过之前最佳方法 QuDI +2.17 dB PSNR，尽管存在 PPP 不匹配。
- 消融实验表明，潜在空间对齐损失（LSA）和确定性均值编码是避免 VAE 编码器崩溃、实现收敛的关键。
---

# gQIR: Generative Quanta Image Reconstruction

> [!tip] 核心洞察
> 将互联网规模预训练的 Stable Diffusion 扩散先验适配到量子爆发成像的三阶段框架：阶段1 通过潜在空间对齐 VAE 实现联合去噪‑去马赛克；阶段2 对低秩适配（LoRA）U‑Net 进行对抗蒸馏，获得单步高感知质量生成器；阶段3 在潜在空间内设计伪3D FusionViT 实现运动感知的时空爆发融合，从而在极端运动与光子饥饿条件下同时获得高保真度和时序一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | gQIR：生成式量子图像重建 |
| 英文题名 | gQIR: Generative Quanta Image Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.20417) · [Code](https://github.com/Aryan-Garg/gQIR) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | gQIR |
| Dataset | 3‑bit nano‑burst single RGB frame reconstruction, Extreme motion burst reconstruction, I2‑2000fps burst test set |

> [!tip] 效果简介
> - 3‑bit nano‑burst single RGB frame reconstruction 上，MUSIQ (Color) 42.038 vs Restormer 40.xxx (exact value not extracted) (提升约 2 点)。
> - Extreme motion burst reconstruction (XD dataset) 上，PSNR / SSIM / LPIPS (Cumulative) PSNR 29.832 / SSIM 0.856 / LPIPS 0.330 vs QBP PSNR ~26.x / QUIVER PSNR ~28.x (+ 1‑3 dB over QUIVER)。
> - I2‑2000fps burst test set 上，PSNR 30.811 (3.25 PPP) vs QuDI 28.641 (approx) (+2.17 dB)。

## 概要

单光子雪崩二极管（SPAD）传感器能够在极端低光环境下以数万帧每秒的速度捕获光子事件，但其输出为极端稀疏的二值爆发帧，伴随伯努利/泊松噪声、拜耳马赛克采样以及剧烈的帧间运动。传统去噪、对齐与生成模型在此类光子饥饿条件下失效——编码器易陷入平滑捷径解，难以同时保持光度保真性与感知质量。

gQIR 提出将大规模文本‑图像扩散模型的语义与结构先验适配到量子爆发成像的三阶段框架：**阶段1** 通过潜在空间对齐的 VAE 实现联合去噪‑去马赛克；**阶段2** 对低秩适配（LoRA）U‑Net 进行对抗蒸馏，获得单步高感知质量生成器；**阶段3** 在潜在空间内设计伪3D FusionViT 实现运动感知的时空爆发融合。核心机制在于引入确定性均值编码和潜在空间对齐损失（LSA）约束编码器，避免在极端光子噪声下的灾难性遗忘。

实验表明，gQIR 在 3 位纳米爆发单帧重建中感知质量显著优于微调的 **Restormer**（Zamir et al., CVPR 2022）与 **NAFNet**（Chen et al., ECCV 2022）；在极端运动爆发重建中，PSNR/SSIM/LPIPS 均大幅领先 **QBP**（Ma et al., TOG 2020）和 QUIVER；在 I2‑2k 基准上超越之前最佳方法 QuDI +2.17 dB PSNR。消融实验证实，LSA 损失与确定性均值编码是避免编码器崩溃的关键，而三阶段协同在保真度与时间稳定性之间取得最佳平衡。

**方法定位**：gQIR 属于生成式先验驱动的计算成像方法，首次将互联网规模预训练的 Stable Diffusion 扩散先验系统性地适配到量子爆发重建任务，在方法谱系上连接了扩散模型蒸馏、多帧爆发融合与单光子成像三个领域。



### 单光子成像：速度与保真度的两难

单光子雪崩二极管（Single-Photon Avalanche Diode, SPAD）传感器具备纳秒级时间分辨率，可在 10k–100k fps 的极端帧率下捕获光子到达事件。然而，这种极速能力以严重的光子饥饿为代价：每个像素在微秒级曝光窗口内仅能记录极少的光子，输出为二值伯努利事件——要么检测到至少一个光子（1），要么完全黑暗（0）。SPAD 的成像过程可形式化为：

$$x_{spad} = Bern(1 - e^{-\lambda}) = Bern(1 - e^{-\alpha \cdot x_{lin}})$$

其中 $\lambda$ 为泊松到达率，$\alpha$ 控制每像素期望光子数（photons-per-pixel, PPP）。对于彩色 SPAD，拜耳滤色阵列进一步将入射光分割为红、绿、蓝通道，经 $N$ 帧二值爆发叠加平均后，得到 $\log_2(N+1)$ 位的马赛克低质量观测：

$$x_{lq} = \frac{1}{N} \sum_{i=1}^{N} M_{\pi} \left[ Bern(1 - e^{-\alpha \cdot x_{lin}}) \right]$$

这种成像机制引入了三重核心挑战：**极端稀疏性**（每像素仅数位信息）、**伯努利/泊松噪声**（非高斯、信号依赖的量子噪声），以及**帧间运动**（高速场景下目标位移显著）。三者交织，使得从光子爆发中恢复可信的视觉内容成为一个高度病态的逆问题。

### 现有方法的瓶颈

当前量子爆发重建方法可大致分为两类，但均在极端条件下暴露结构性缺陷。

**传统对齐-合并管线**（如 **QBP**（Ma et al., TOG 2020））依赖光流对齐后维纳滤波合并。在低运动场景下表现尚可，但在 1000–100k fps 的高速运动下，光流估计本身受噪声严重干扰，导致对齐失败并产生运动模糊。**QUIVER** 引入 11 帧前降噪与循环融合，部分缓解了噪声问题，但面对真实 SPAD 采样中运动模糊叠加的纳米爆发，其降噪-对齐串联结构仍然崩溃。

**学习型方法**（如 **NAFNet**（Chen et al., ECCV 2022）、**Restormer**（Zamir et al., CVPR 2022））在合成数据上微调后，可在单帧去噪任务中获得高 PSNR，但这一优势源于对低失真目标的过度优化——模型倾向于输出平滑的“平均解”，丢失高频纹理和人脸等语义结构（见 Table 1, Figure 3）。扩散模型方法 **QuDI** 采用时间条件 U-Net 与 DDPM 式展开，在 I2-2k 基准上取得领先，但其迭代采样范式计算代价高昂，且未充分应对极端 PPP 下的先验崩溃。

**核心瓶颈在于**：当光子数极度匮乏时，仅从数据驱动的去噪或对齐策略无法可靠地区分信号与噪声，编码器极易陷入平滑捷径解——输出恒定或模糊的潜在编码，从而丧失感知保真度（Figure 4 展示了这一崩溃现象）。

### 生成式先验的机遇与挑战

互联网规模预训练的文本-图像扩散模型（如 Stable Diffusion）在海量数据中习得了丰富的语义与结构先验，理论上可为量子爆发重建提供强约束。然而，直接应用面临两个根本性障碍：

1. **域鸿沟**：扩散模型的 VAE 编码器在干净自然图像上训练，对 SPAD 的伯努利噪声与拜耳马赛克模式完全陌生，直接输入将导致潜在空间严重失配。
2. **灾难性遗忘**：若在量子数据上端到端微调 VAE，编码器会在缺乏适当约束时迅速遗忘预训练知识，退化为无意义的恒定输出（Figure 4）。

### 本文动机

针对上述缺口，gQIR 提出一个核心洞察：**将大规模扩散先验适配到量子爆发成像，需要一个精心设计的“引导-蒸馏-融合”三阶段框架**，而非简单的端到端微调。具体而言：

- **阶段 1** 通过潜在空间对齐损失（LSA）和确定性均值编码，强制微调编码器在极端噪声下保持与干净图像潜在表示的一致性，避免崩溃的同时完成联合去噪与去马赛克。
- **阶段 2** 将扩散先验通过对抗蒸馏压缩为单步 LoRA 生成器，在保留感知质量的同时消除迭代采样负担。
- **阶段 3** 在潜在空间内设计伪 3D FusionViT，实现运动感知的时空爆发融合，抑制内容漂移并提升时序一致性。

这一设计使得 gQIR 能够在光子饥饿与极端运动并存的条件下，同时获得高保真度与感知质量，并在多个基准上显著超越现有方法（Table 2, Table 3）。



## 核心方法与创新机理

gQIR 的核心创新在于将大规模文本‑图像扩散模型的语义与结构先验系统性地适配到量子爆发成像的极端退化场景，通过**三阶段模块化架构**和四个关键设计槽位（changed slots），突破了传统方法在稀疏光子、强噪声与帧间运动下的瓶颈。

### 先验知识来源：从任务专用去噪到互联网规模扩散先验

传统单帧去噪基线（如 **NAFNet** (Chen et al., ECCV 2022)、**Restormer** (Zamir et al., CVPR 2022)）依赖从零训练的特定任务网络，在极端光子饥饿下倾向于产生过度平滑的解；爆发重建方法（如 **QBP** (Ma et al., TOG 2020) 的维纳滤波、**QuDI** 的 DDPM 式展开）虽利用了时序信息，但其先验仍局限于训练数据分布。gQIR 首次将 **Stable Diffusion** 的互联网规模预训练扩散先验引入量子成像管线，利用其蕴含的丰富纹理、结构和语义知识，在仅 3 位纳米爆发输入下恢复可信的高频细节——这一先验的引入是后续所有阶段能够避免平滑捷径解的基础（Sec. 1, Sec. 2）。

### 潜在空间对齐：确定性均值编码与 LSA 损失防止编码器崩溃

直接将预训练 VAE 编码器应用于量子噪声帧会导致灾难性遗忘和编码器崩溃——编码器学习到感知无意义的捷径，输出恒定潜在编码（Figure 4）。gQIR 的两个关键设计解决了这一问题：

1. **确定性均值编码**：放弃随机采样后验分布，改用编码器输出的确定性均值 $\mu_{\phi^*}(x_{lq})$，避免光子散粒噪声在随机采样中被放大。
2. **潜在空间对齐损失（LSA）**：$\mathcal{L}_{lsa} = \| \mu_{\phi^*}(x_{lq}) - \mu_{\phi}(x_{gt}) \|_2^2$，强制微调编码器的潜在均值逼近冻结预训练编码器对干净图像的编码，为编码器提供关键的收敛梯度。

消融实验（Table 4）表明，LSA 与确定性编码缺一不可——缺少任一组件都将导致 PSNR/SSIM/ManIQA 显著下降。这一设计使得 VAE 编码器能够在保持预训练潜在空间结构的同时，完成联合去噪与去马赛克。

### 生成器训练范式：从迭代扩散采样到单步对抗蒸馏

**QuDI** 等扩散基线采用类 DDPM 的多步迭代采样，推理成本高且难以与后续爆发融合模块高效集成。gQIR 的 Stage 2 将扩散先验蒸馏为单步生成器：对 U‑Net 进行低秩适配（LoRA），通过多级 ConvNeXt‑Large 鉴别器进行对抗训练（Eq. 7‑8），将扩散模型的迭代去噪过程压缩为端到端的前馈映射。这一范式转换不仅大幅降低推理开销，还使得生成器能够作为即插即用的感知增强模块嵌入爆发融合管线。

### 爆发时空融合：从光流对齐平均到潜在空间伪 3D 注意力融合

传统爆发重建（**QBP** 的对齐‑合并 + 维纳滤波、**QUIVER** 的光流 + 循环融合）在像素空间进行光流对齐后简单平均或循环合并，在快速运动下易产生模糊与伪影。gQIR 的 Stage 3 将融合操作提升到潜在空间：

- 引入**伪 3D FusionViT**，在潜在空间内对多帧编码应用子二次复杂度的窗口注意力（windowed attention），跨时间与空间维度自适应加权合并；
- 结合**可学习调制残差**，动态抑制运动模糊和内容漂移。

Figure 5 直观展示了这一差异：光流对齐后的简单平均在场景运动下产生模糊，而 FusionViT 根据运动幅度和与参考帧的邻近程度自适应分配权重，输出更锐利的融合潜在编码。消融实验（Table 5）进一步证实，Stage 3 在提高保真度的同时有效抵消了 Stage 2 感知增强引入的内容漂移，实现了保真度与时序稳定性的最佳权衡。

### 创新总结

四项 changed slots 构成了一条因果链：**扩散先验**提供丰富的语义与纹理知识储备；**潜在空间对齐**确保编码器在极端噪声下不崩溃并将量子帧映射到有意义的潜在空间；**对抗蒸馏**将迭代先验转化为高效的单步生成器；**潜在空间注意力融合**在保持先验优势的同时实现运动感知的时空一致性。这一设计使得 gQIR 能够在传统方法失效的极端条件下（3 位纳米爆发、100k fps 高速运动）同时获得高保真度与感知质量。



gQIR 提出一个**模块化三阶段框架**，将大规模文本‑图像生成先验（Stable Diffusion）适配到单光子雪崩二极管（SPAD）量子爆发重建的极端稀疏‑噪声‑运动场景。其核心设计逻辑是：**先对齐潜在空间以稳定编码 → 再蒸馏扩散先验以增强感知质量 → 最后在潜在空间进行运动感知时空融合以恢复时序一致性**。

### 三阶段流水线

**阶段1（S1）：量子对齐变分自编码器（Quanta‑aligned VAE）**
输入为 $N$ 帧二值化拜耳马赛克纳米爆发经平均得到的低质量观测 $x_{lq}$（位深 $\log_2(N+1)$）。编码器 $\mathcal{E}_{\phi^*}$ 执行联合去噪与去马赛克，采用**确定性均值编码**（而非随机采样后验分布），输出潜在均值 $\mu_{\phi^*}(x_{lq})$。训练时冻结预训练编码器 $\mathcal{E}_\phi$ 的副本，通过**潜在空间对齐损失（LSA）** $\mathcal{L}_{lsa} = \|\mu_{\phi^*}(x_{lq}) - \mu_\phi(x_{gt})\|_2^2$ 约束低质量潜在编码与干净图像潜在编码的一致性，避免编码器在极端光子噪声下陷入平滑捷径解（即“编码器崩溃”，Figure 4）。总损失 $\mathcal{L}_{\mathcal{E}_{qvae}}$ 由 LSA、像素空间 MSE 损失和 VGG‑19 感知损失加权组合而成。

**阶段2（S2）：对抗蒸馏 LoRA U‑Net**
以阶段1输出的潜在编码为输入，对 Stable Diffusion 的 U‑Net 进行**低秩适配（LoRA）微调**，并通过**单步对抗蒸馏**将其转化为端到端生成器 $\mathcal{G}_{lora}$。鉴别器采用多级 ConvNeXt‑Large，训练目标为对抗损失、感知损失与像素重建损失的组合。该阶段将迭代式扩散先验压缩为单步前向映射，在保持语义结构的同时大幅增强高频细节与感知真实感。

**阶段3（S3）：潜在爆发 FusionViT**
在潜在空间内对爆发序列进行时空融合。引入**伪3D FusionViT**（基于窗口注意力的 miniViT），对光流对齐后的多帧潜在编码进行自适应加权合并，并叠加可学习调制残差。相比简单平均导致的运动模糊，FusionViT 根据运动幅度与参考帧邻近度动态分配权重（Figure 5）。该阶段在恢复时序一致性的同时，有效抑制阶段2因感知增强引入的内容漂移。

### 输入输出流

1. **单帧/纳米爆发输入**：$N$ 帧二值拜耳帧 → 平均为 $x_{lq}$ → S1 编码器 → 潜在编码 $z_{lq}$ → S2 LoRA U‑Net → 解码器 → 重建 RGB 图像。
2. **爆发序列输入**：多帧纳米爆发 $X_{lq}$ → S1 编码器逐帧编码 → 多帧潜在编码 → S3 FusionViT 时空融合 → 融合潜在编码 → S2 LoRA U‑Net → 解码器 → 时序一致的 RGB 爆发序列。

三阶段可独立训练，S1 提供稳定潜在表示，S2 注入生成先验，S3 恢复跨帧一致性，形成从“光子饥饿”到“可信视觉内容”的完整映射链。

### 补充图表

![[assets/figures/papers/paper_list_l2513_https_arxiv_org_abs_2602_20417/figures/002_Figure_2.jpg]]
*Figure 2: Overview of gQIR. Three-stage framework for quanta burst reconstruction: (S1) a quanta-aligned VAE for joint denoising and demosaicing of SPAD nano-bursts, (S2) an adversarially finetuned LoRA [18] latent U-Net initialized with stable diffusion [47] weights for perceptual enhancement, and (S3) a latent burst FusionViT for motion-aware spatio-temporal fusion of burst of nano-burst inputs*

![[assets/figures/papers/paper_list_l2513_https_arxiv_org_abs_2602_20417/figures/001_Figure_1.jpg]]
*Figure 1: gQIR: Photorealistic single image and burst reconstruction from ultra–high-speed color SPADs. Our pipeline reconstructs high-quality RGB images from 3-bit color-SPAD CFA nano-bursts (left) and merges SPAD photon cubes into temporally consistent bursts (right). From photon-starved inputs captured at 10k–50k fps in extreme, out-of-domain scenes, gQIR recovers sharp textures, accurate color, and coherent structure by leveraging a generative prior. For burst sequences up to 100k fps, FusionViT aligns and dynamically merges quanta latents, outperforming traditional and learning-based methods in both fidelity and perceptualness under motion*



### 3.1 图像形成模型

SPAD 传感器在每个像素处记录光子到达的二值事件。给定线性域高动态范围真值图像 $x_{lin}$，单次曝光下 SPAD 输出遵循伯努利分布：

$$x_{spad} = Bern(1 - e^{-\lambda}) = Bern(1 - e^{-\alpha \cdot x_{lin}})$$

其中 $\lambda$ 为泊松速率，$\alpha$ 控制每像素期望光子数（PPP）。对于彩色 SPAD，传感器表面覆盖拜耳滤色阵列（CFA），对 $N$ 帧二值观测按拜耳模式 $M_{\pi}$ 求和并平均，得到 $\log_2(N+1)$ 位的马赛克低质量输入：

$$x_{lq} = \frac{1}{N} \sum_{i=1}^{N} M_{\pi} \left[ Bern(1 - e^{-\alpha \cdot x_{lin}}) \right]$$

这一形成模型揭示了核心瓶颈：极端稀疏的二值观测叠加伯努利/泊松噪声，且拜耳模式进一步丢失空间分辨率，使得传统去噪与去马赛克方法面临严峻挑战。

### 3.2 阶段一：量子对齐 VAE 编码器

阶段一的核心目标是将低质量马赛克输入映射到预训练扩散模型的潜在空间，同时完成联合去噪与去马赛克。gQIR 微调 Stable Diffusion 的 VAE 编码器 $\mathcal{E}_{\phi^*}$，但面临两个关键困难：光子散粒噪声导致随机采样方差放大；编码器可学习参数过多时易陷入平滑捷径解。

**确定性均值编码**：摒弃从后验分布随机采样，改用确定性均值 $\mu_{\phi^*}(x_{lq})$ 作为潜在表示，避免噪声方差放大。

**潜在空间对齐损失（LSA）**：引入冻结的预训练编码器副本 $\mu_{\phi}$，强制低质量输入的潜在编码逼近干净图像真值的潜在编码：

$$\mathcal{L}_{lsa} = \| \mu_{\phi^*}(x_{lq}) - \mu_{\phi}(x_{gt}) \|_2^2$$

LSA 损失是防止编码器灾难性遗忘的关键——消融实验（Table 4, Figure 4）表明，缺失 LSA 时编码器退化为输出恒定值，PSNR/SSIM/ManIQA 均显著下降。

![[assets/figures/papers/paper_list_l2513_https_arxiv_org_abs_2602_20417/figures/004_Figure_4.jpg]]
*Figure 4: Encoder collapse under predegradation removal loss [34, 70]. The encoder*

**像素空间与感知监督**：解码后的重建图像还需在像素空间和 VGG-19 特征空间与真值对齐：

$$\mathcal{L}_{MSE} = \| \mathcal{D}(\mu_{\phi^*}(x_{lq})) - \mathcal{D}(\mu_{\phi}(x_{gt})) \|_2^2$$

$$\mathcal{L}_{perc} = \| \Phi(\mathcal{D}(\mu_{\phi^*}(x_{lq}))) - \Phi(\mathcal{D}(\mu_{\phi}(x_{gt}))) \|_2^2$$

阶段一总损失为三项加权组合：

$$\mathcal{L}_{\mathcal{E}_{qvae}} = \lambda_{lsa} \mathcal{L}_{lsa} + \lambda_{MSE} \mathcal{L}_{MSE} + \lambda_{perc} \mathcal{L}_{perc}$$

训练时 $\lambda_{lsa}=0.1$，$\lambda_{MSE}=10^3$，$\lambda_{perc}=2$，在 8×A100 上训练 600k 步，批次大小 8，学习率 $10^{-5}$。

### 3.3 阶段二：对抗蒸馏 LoRA U-Net

阶段一的输出虽已恢复结构与色彩，但高频细节不足。阶段二将扩散模型的迭代采样过程蒸馏为单步前向生成器，以提升感知质量。

**LoRA 微调**：对 Stable Diffusion 的 U-Net 注入低秩适配（LoRA）权重，冻结原始参数，仅训练低秩增量。生成器 $\mathcal{G}_{lora}$ 接收阶段一的潜在编码，直接输出增强后的潜在表示。

**对抗训练**：采用 ConvNeXt-Large 作为鉴别器 $\mathcal{V}_\theta$，标准 GAN 极小极大目标为：

$$\min_{\phi} \max_{\theta} \mathbb{E}_{x\sim p_{X_{gt}}} [\log \mathcal{V}_\theta(x)] + \mathbb{E}_{x\sim p_{X_{lq}}} [\log (1-\mathcal{V}_\theta(\mathcal{G}(x)))]$$

生成器总损失结合对抗损失、感知损失与像素重建损失：

$$\mathcal{L}_{G_{lora}} = \mathcal{L}_{adv} + L_{perc} + \| \mathcal{D}( \mathcal{G}_{lora}(\mu_{\phi^*}(x_{lq})) ) - x_{gt} \|_2^2$$

阶段二在单张 RTX 4090 上训练 100k 迭代，分辨率 256×256，损失权重 $\lambda_{adv}=0.5$，$\lambda_{MSE}=500$，$\lambda_{perc}=5$。

### 3.4 阶段三：潜在爆发 FusionViT

爆发序列包含多帧互补信息，但帧间运动导致简单平均产生模糊。阶段三在潜在空间内进行运动感知的时空融合。

**伪 3D 窗口注意力**：FusionViT（$\mathcal{F}$）对爆发序列的潜在编码应用子二次复杂度的窗口注意力，沿时间轴与空间轴同时建模依赖关系，自适应加权合并各帧贡献。

**可学习调制残差**：除加权合并外，FusionViT 引入可学习的调制残差，进一步抑制运动模糊和内容漂移。

**多层级监督**：融合模块的训练损失覆盖潜在空间、像素空间和感知层面：

$$\mathcal{L}_{fusion} = \| \mathcal{F}(\mu_{\phi^*}(X_{lq})) - \mu_{\phi}(x_{gt}) \|_2^2 + \| \mathcal{D}(\mathcal{G}_{lora}(\mathcal{F}(\mu_{\phi^*}(X_{lq})))) - x_{gt} \|_2^2 + \mathcal{L}_{perc}$$

消融实验（Table 5）证实，阶段三在提高保真度的同时显著抵消了阶段二引入的内容漂移，提供了最佳的保真-稳定性权衡。

### 补充图表

![[assets/figures/papers/paper_list_l2513_https_arxiv_org_abs_2602_20417/figures/005_Figure_5.jpg]]
*Figure 5: Dynamic spatio-temporal latent burst merging. Naive averaging of flow-aligned burst latents yields blur under scene motion. FusionViT instead adaptively weights latents by motion and proximity to the reference, producing a sharper output*



## 实验与关键发现

### 核心实验设置

所有实验均基于合成 SPAD 数据开展，以确保公平对比。单帧基线（**Restormer** (Zamir et al., CVPR 2022)、**NAFNet** (Chen et al., ECCV 2022)）在相同数据量、相同训练步数下微调；爆发基线（**QBP** (Ma et al., TOG 2020)、**QUIVER**）均使用 11 帧 3 位纳米爆发作为输入。训练超参数方面，阶段 1 的 VAE 在 8×A100 上训练 600k 步，学习率 $10^{-5}$，批量大小 8，损失系数 $\lambda_{lsa}=0.1$，$\lambda_{MSE}=10^3$，$\lambda_{perc}=2$；阶段 2 的 LoRA U-Net 在单张 RTX 4090 上以 256×256 分辨率训练 100k 次迭代，损失系数 $\lambda_{adv}=0.5$，$\lambda_{MSE}=500$，$\lambda_{perc}=5$。评估指标同时涵盖全参考（PSNR、SSIM、LPIPS）与非参考（MUSIQ、ManIQA、ClipIQA），避免单一指标偏倚。

### 单帧重建：感知质量与保真度权衡

Table 1 报告了 3 位纳米爆发输入的单帧 RGB 重建结果。微调后的 Restormer 与 NAFNet 由于优化目标偏向低失真，获得了更高的 PSNR，但代价是严重的过度平滑——高频纹理和远距离深度平面中的结构几乎被抹除。gQIR 的单帧输出（仅使用阶段 1+2）在 MUSIQ 感知质量指标上达到 42.038，显著优于传统去噪基线（Restormer 约 40.x），与 Figure 3 的定性对比一致：gQIR 保留了更清晰的面部特征和纹理细节，这得益于训练集中包含 FFHQ 人脸数据的生成先验。

![[assets/figures/papers/paper_list_l2513_https_arxiv_org_abs_2602_20417/figures/007_Table_1.jpg]]
*Table 1: Fidelity and perceptual quality of 3-bit nano-burst input single RGB frame reconstruction. Fine-tuned Restormer and NAFNet attain higher PSNR due to optimization for lower distortion [2], leading to oversmoothing, while gQIR achieves higher perceptual quality, consistent with visual results in Fig. 3*

![[assets/figures/papers/paper_list_l2513_https_arxiv_org_abs_2602_20417/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparison – single 3-bit frame reconstructions. Conventional finetuned baselines over-smooth high-frequency structures, especially in distant depth planes and textured regions, whereas gQIR preserves sharper details and more faithful facial features, benefitting from the inclusion of FFHQ faces [24] in the training set*

**关键结论**：在极端光子饥饿条件下，纯失真驱动的方法会陷入平滑捷径，而生成式先验能够恢复可信的视觉结构，但需注意这并非无代价——下文将讨论内容漂移问题。

### 爆发重建：极端运动与跨基准泛化

Table 2 展示了在极端运动爆发重建任务上的定量对比。gQIR 在累积指标上达到 PSNR 29.832 / SSIM 0.856 / LPIPS 0.330，较 **QBP** 提升约 3 dB，较 **QUIVER** 提升 1–3 dB。Figure 6 的定性结果揭示了传统方法的失效模式：QBP 在快速运动下产生模糊重建，因为其对齐-平均策略无法应对小爆发输入；QUIVER 则因纳米爆发帧本身的运动模糊而崩溃，因为其前降噪步骤依赖于相对清晰的输入。gQIR 通过 FusionViT 的动态加权合并（Figure 5）在 1000–100k fps 范围内持续恢复更清晰的结构。

![[assets/figures/papers/paper_list_l2513_https_arxiv_org_abs_2602_20417/figures/009_Table_2.jpg]]
*Table 2: Burst reconstruction fidelity under extreme motion. Our method achieves superior scores due to cleaner flow procsesing and dynamic burst merging while keeping the traditional align-and-merge philosophy aided with a generative prior*

![[assets/figures/papers/paper_list_l2513_https_arxiv_org_abs_2602_20417/figures/006_Figure_6.jpg]]
*Figure 6: Qualitative comparison – burst reconstruction. We simulate 1:1 GT–SPAD bursts by averaging 77 binary frames per input, preserving the original scene frame rate. QBP yields blurred reconstructions under fast motion due to small burst input while QUIVER breaks down due to motion-blurred nano-bursts, from realistic sampling. Our burst pipeline consistently recovers sharper structure and higher fidelity across extreme motion regimes, from 1000 to 100k fps*

在 I2-2k 基准测试（Table 3）上，尽管存在每像素光子数（PPP）不匹配——gQIR 使用 3.25 PPP，而此前最佳方法 **QuDI** 使用约 3.5 PPP——gQIR 仍达到 PSNR 30.811 / SSIM 0.868，较 QuDI 的约 28.641 dB 提升 +2.17 dB。这一跨基准泛化能力表明生成式先验对传感器参数差异具有一定鲁棒性，但仍需注意 PPP 不匹配可能使绝对数值比较存在偏差。

![[assets/figures/papers/paper_list_l2513_https_arxiv_org_abs_2602_20417/figures/010_Table_3.jpg]]
*Table 3: Burst Fidelity on I2-2k benchmark. Despite the PPP mismatch, our method reaches superior fidelity on I2-2k [8]*

### 消融研究

#### 阶段 1：潜在空间对齐是收敛的关键

Table 4 和 Figure 4 揭示了阶段 1 设计的核心发现。若移除潜在空间对齐损失（LSA）或采用随机采样替代确定性均值编码，VAE 编码器将迅速崩溃为恒定输出——编码器学到感知上无意义的捷径，训练曲线快速收敛到退化最优。消融实验表明，LSA 与确定性采样的组合在仅 1 个 epoch 内即可实现有意义的收敛，避免灾难性遗忘。这一发现具有方法论意义：在极端噪声条件下微调预训练 VAE 时，仅靠像素空间监督不足以维持潜在空间的结构一致性。

![[assets/figures/papers/paper_list_l2513_https_arxiv_org_abs_2602_20417/figures/013_Table_4.jpg]]
*Table 4: Ablation - Stage 1 Design Choices and Losses. Our latent space alignment loss and deterministic sampling gives the highest fidelity in 1 epoch for joint denoising and demosaicing. Both components are critical for meaningful convergence and avoiding catastrophic forgetting shown in Fig. 4*

#### 阶段 2–3：感知增强与内容漂移的权衡

Table 5 的逐阶段消融揭示了三个阶段的贡献与代价：
- **仅阶段 1**：已可恢复基本结构和色彩，但高频细节不足。
- **阶段 1+2**：对抗蒸馏显著增强感知真实感，但引入了轻微的内容漂移——这是因为阶段 2 在训练中更强调感知质量，在帧间仅有微小运动的高速序列中会削弱运动线索。
- **阶段 1+2+3**：FusionViT 的时空融合在提高保真度的同时有效抵消了阶段 2 引入的漂移，实现了保真度与时间稳定性的最佳权衡。

![[assets/figures/papers/paper_list_l2513_https_arxiv_org_abs_2602_20417/figures/011_Table_5.jpg]]
*Table 5: Ablation: All stages – fidelity versus temporal stability. Stage 2 improves fidelity over Stage 1 but slightly increases content drift, while Stage 3 provides the best overall trade-off between reconstruction quality and temporal stability*

### 真实 SPAD 原型验证

Figure 8 展示了在 1Mpx 被动式彩色 SPAD 原型上以 6k fps 采集的二值爆发重建结果。尽管合成训练数据与真实传感器噪声特性之间存在域偏移，gQIR 仍能恢复合理的色彩和结构，初步验证了方法的实用性。但需注意，该评估仅为定性展示，缺乏大规模真实 SPAD 基准上的定量验证。

![[assets/figures/papers/paper_list_l2513_https_arxiv_org_abs_2602_20417/figures/012_Figure_8.jpg]]
*Figure 8: Real color SPAD reconstructions. Qualitative results on binary bursts captured with a 1Mpx passive color SPAD prototype at 6k fps. Insets show demosaicing via sum-and-average*

### 失败模式与局限性

1. **HDR 瓶颈**：当前 VAE 解码器受限于 8 位精度，无法处理高动态范围内容；虽可通过平铺实现高分辨率，但可能引入边界伪影。
2. **内容漂移**：阶段 2 的对抗蒸馏在高速序列中可能引入帧间不一致的虚构纹理（幻觉），对于需要绝对光度保真的科学测量任务可能不适用。
3. **PPP 泛化受限**：未将每像素光子数显式建模为条件信号，导致极端低光（PPP ≤ 1）或不同传感器增益下泛化能力受限。
4. **域偏移风险**：依赖大规模合成数据训练，在真实 SPAD 噪声特性下的鲁棒性尚未充分验证。
5. **文本重建能力**：Figure 7 的补充分析表明，采用 SD3.5 的 VAE（4 倍潜在空间）可显著改善文字可读性，暗示当前 SD2.1 版本在精细文字重建上存在不足。



## 定位与知识库关联

### 与基线方法的关系

gQIR 的核心贡献在于将互联网规模预训练的文本-图像扩散先验（Stable Diffusion）适配到单光子量子爆发成像这一极端低光、高噪声领域，其设计哲学与现有方法形成系统性对比。

**单帧去噪基线：Restormer 与 NAFNet。** 在 3 位纳米爆发单帧重建任务中，gQIR 的直接对比对象是经过同等数据微调的 **Restormer**（Zamir et al., CVPR 2022）和 **NAFNet**（Chen et al., ECCV 2022）。这两种方法均采用纯像素空间去噪范式，通过优化低失真目标（MSE）实现高 PSNR，但其代价是过度平滑高频纹理与远焦平面结构（Table 1, Figure 3）。gQIR 通过引入潜在空间对齐 VAE 和对抗蒸馏的扩散先验，在感知质量指标（MUSIQ）上显著超越二者，证明生成式先验在光子饥饿条件下恢复可信视觉内容的优势。

**爆发重建基线：QBP、QUIVER 与 QuDI。** 爆发重建领域的方法可大致分为“对齐-合并”传统范式与学习型扩散展开范式。**QBP**（Ma et al., TOG 2020）采用传统光流对齐后维纳滤波合并，在快速运动下因对齐误差累积而产生模糊。**QUIVER** 引入前降噪与循环融合，但对运动模糊的纳米爆发帧敏感，在极端运动场景下性能退化（Table 2, Figure 6）。**QuDI** 采用时间条件 U-Net 的 DDPM 式迭代采样，在 I2-2k 基准上代表此前最佳水平，但存在 PPP 不匹配问题（QuDI 使用 3.5 PPP，gQIR 使用 3.25 PPP），且迭代采样效率低于 gQIR 的单步生成范式（Table 3）。gQIR 的突破在于：将传统对齐-合并哲学与生成式先验结合，在潜在空间中通过 FusionViT 自适应加权合并，避免了像素空间对齐的误差放大和扩散模型的迭代开销。

### 知识库定位与范式转换

gQIR 的方法谱系可追溯至三个技术脉络的交汇点：

**1. 扩散先验的领域适配。** 不同于直接使用扩散模型进行图像复原（如 DDRM、DiffPIR），gQIR 采用三阶段渐进适配策略：先通过 VAE 编码器微调将 SPAD 域映射到预训练潜在空间，再通过对抗蒸馏将迭代扩散先验压缩为单步生成器，最后在潜在空间内进行时空融合。这种“对齐-蒸馏-融合”的模块化设计避免了端到端微调扩散模型时常见的灾难性遗忘问题（Figure 4, Table 4）。

**2. 潜在空间对齐的编码器设计。** gQIR 的 Stage 1 引入两项关键设计：确定性均值编码（避免光子散粒噪声的方差放大）和潜在空间对齐损失（LSA，Eq. 3）。消融实验（Table 4）表明，缺失任一组件都将导致编码器崩溃——后者会学习到感知无意义的恒定输出捷径。这一发现揭示了在极端噪声下微调 VAE 编码器的核心瓶颈：当可训练编码器同时控制监督项和预测项时，训练曲线会迅速收敛到退化最优解。

**3. 单步生成器的对抗蒸馏。** Stage 2 将 LoRA 微调的 U-Net 与 ConvNeXt-Large 鉴别器进行对抗训练（Eq. 7-8），将扩散先验蒸馏为端到端映射。这区别于渐进式蒸馏（如 LCM）和对抗扩散蒸馏（如 ADD），其独特之处在于：蒸馏目标并非加速采样，而是将扩散模型的感知质量注入到单步前馈生成器中，同时通过冻结的 VAE 解码器保持结构一致性。

### 适用边界与局限

**应用边界。** gQIR 适用于以下场景：SPAD 传感器在 3 位至约 5 位光子预算下的纳米爆发重建、1000-100k fps 的高速运动爆发融合、以及需要同时优化保真度与感知质量的视觉应用。其生成式先验在恢复高频纹理、面部细节和文字内容方面表现突出（Figure 7）。

**关键局限。**

1. **HDR 瓶颈。** 当前 VAE 解码器受限于 8 位精度，无法处理高动态范围内容。虽然可通过平铺实现高分辨率，但可能引入边界伪影。

2. **运动线索退化。** Stage 2 的对抗蒸馏在增强感知质量的同时，在高速序列中会削弱帧间运动线索，导致轻微内容漂移（Table 5）。这是感知增强与运动保真之间的内在权衡。

3. **PPP 泛化不足。** 未将每像素光子数（PPP）显式建模为条件信号，导致在极端低光（PPP ≤ 1）或不同传感器增益下泛化能力受限。在 I2-2k 基准上虽展示优势，但存在 PPP 不匹配（3.25 vs 3.5），需进一步验证公平性。

4. **生成幻觉风险。** 扩散先验在极稀疏光子下可能引入可信但虚构的纹理。对于需要绝对光度保真的科学测量任务（如荧光寿命成像），该特性可能不适用。

5. **域偏移鲁棒性。** 依赖大规模合成数据训练，在真实 SPAD 噪声特性与域偏移下的鲁棒性尚未充分评估（Figure 8 仅展示定性结果）。

### 开放问题

1. **视频级扩散先验。** 如何引入跨帧扩散先验（如视频扩散模型）以进一步提高时空一致性，是突破当前逐帧处理范式的重要方向。

2. **PPP 条件建模。** 将 PPP 显式编码为条件信号是否能增强跨光照和传感器特性的泛化能力？这需要设计光子预算感知的归一化策略。

3. **HDR 解码器设计。** 能否设计 HDR 感知的 VAE 解码器，突破当前 8 位瓶颈，同时保持与预训练扩散先验的兼容性？

4. **超快帧率效率。** 在 >100k fps 的超快帧率下，如何平衡生成质量与计算效率？FusionViT 的窗口注意力机制提供了效率基础，但三阶段流水线的整体延迟仍需优化。

5. **可信度与可解释性。** 生成式先验在量化科学测量任务中如何保证可信度？可能需要引入不确定性量化机制或物理约束的生成过程。



## 原文 PDF

![[paperPDFs/CVPR_2026/gQIR_Generative_Quanta_Image_Reconstruction.pdf]]
