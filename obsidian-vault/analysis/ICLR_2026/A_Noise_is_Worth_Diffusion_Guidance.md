---
title: A Noise is Worth Diffusion Guidance
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Noise_is_Worth_Diffusion_Guidance.pdf
aliases:
- NIWDG
acceptance: accepted
tags:
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 初始噪声的空间结构（特别是低频成分）
primary_logic: 通过学习将高斯噪声映射到富含结构化低频信息的“提炼噪声”，可以无需采样引导就生成高质量图像，同时保持扩散管线的完整性和广泛兼容性。
claims:
- 初始噪声与反转噪声的差异集中在低频部分，表明存在可学习的结构化映射
- 图像空间损失在所有评估指标上大幅优于噪声空间损失
- NoiseRefine 在 SiT-XL/2、SD2.1、SDXL 上均显著改善 FID 和 IS，超过无引导高斯噪声
- 用户研究中，提炼噪声无引导采样与有引导高斯噪声采样在图像质量和提示遵循度上偏好率相当
paradigm: 通过学习将高斯噪声映射到富含结构化低频信息的“提炼噪声”，可以无需采样引导就生成高质量图像，同时保持扩散管线的完整性和广泛兼容性。
---

# A Noise is Worth Diffusion Guidance

> [!tip] 核心洞察
> 通过学习将高斯噪声映射到富含结构化低频信息的“提炼噪声”，可以无需采样引导就生成高质量图像，同时保持扩散管线的完整性和广泛兼容性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 噪声也值得扩散引导 |
| 英文题名 | A Noise is Worth Diffusion Guidance |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=xEWooSOgaz) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | NoiseRefine |
| Dataset | MS-COCO 2014 validation (30K prompts), MS-COCO 2014 validation, ImageNet (class-conditional, SiT-XL/2), MS-COCO validation (SDXL) |

> [!tip] 效果简介
> - MS-COCO 2014 validation (30K prompts) 上，FID 为 14.62 (Refined, unguided)，对比 42.71 (Gaussian, unguided)，变化 -28.09 (↓65.8%)。
> - MS-COCO 2014 validation 上，IS 为 34.90 (Refined, unguided)，对比 20.86 (Gaussian, unguided)，变化 +14.04。
> - ImageNet (class-conditional, SiT-XL/2) 上，FID 为 10.80 (Refined, unguided)，对比 18.43 (Gaussian, unguided)，变化 -7.63。

## 概述

扩散模型在缺少采样引导（如无分类器引导 CFG）时，生成质量严重退化，常出现结构崩解和语义失配。现有引导蒸馏方案虽能提升无引导采样的质量，但需要修改去噪网络，容易导致灾难性遗忘、与 LoRA 等微调模块不兼容，且训练计算开销较大。因此，亟需一种既保持扩散管线完整、又能在无引导条件下获得接近引导采样质量的方案。

本文提出 **NoiseRefine**，将解决问题的主体从去噪网络转移到初始噪声上。其核心洞察是：初始高斯噪声与由引导图像反演得到的噪声之间的差异主要集中在低频分量（Fig. 3），表明噪声的空间低频结构是控制生成质量的关键因果旋钮。NoiseRefine 通过一个基于 LoRA 的轻量级噪声提炼网络 $g_\phi$，将普通高斯噪声映射为富含结构化低频信息的“提炼噪声”。该方法不在图像生成阶段引入任何引导，也不修改原有扩散模型，因此天然保持与 LoRA、微调模型及时间步蒸馏模型的兼容性。训练时，采用图像空间损失替代直接预测噪声的损失（Table 1），并结合多步分数蒸馏（MSD）损失实现稳定、高效的梯度回传，避免全梯度反传带来的梯度爆炸和收敛困难（Fig. 6）。

实验结果表明，提炼噪声在多个扩散骨干上均带来显著的质量跃升：在 MS‑COCO 30K 提示下，SD2.1 的 FID 从无引导高斯噪声的 42.71 降至 14.62，IS 从 20.86 升至 34.90；SDXL 的 FID 从 63.28 降至 26.22（Table 2）。用户研究中，无引导的提炼噪声在图像质量上的偏好率（53.96%）已略微超过有引导的高斯噪声（46.04%）（Table 3）。此外，提炼网络可直接泛化到未曾见过的微调模型（Table 4），并与 SD‑Turbo 等时间步蒸馏模型无缝协同，单步推理性能即超过两步高斯噪声（Table 5）。推理耗时与无引导高斯噪声相当，远低于有引导采样。当前方法的局限主要在于训练阶段仍需引导采样作为监督信号，且极端低步数下增益有限，但所开启的“噪声蒸馏”范式为扩散生成提供了一条不侵入模型、高兼容且低成本的高效路径。

## 背景与动机

扩散模型（如 SD、SiT）在生成高质量图像时高度依赖采样引导（例如无分类器引导 CFG）。若不使用引导，模型往往生成结构崩坏、语义混乱的图像：在 MS-COCO 验证集上，SD2.1 的无引导 FID 高达 42.71，而 CFG 可将 FID 降至 14.62（表2）。然而 CFG 会导致推理计算量翻倍（图1），限制了实用场景的效率。另一条技术路线——引导蒸馏（Meng et al.）将引导信号直接蒸馏到学生去噪网络中，试图在单次前向传播中保留引导效果。但这类方法必须修改或微调原始去噪网络，引发三个连锁瓶颈：① 灾难性遗忘，损害已学到的泛化知识；② 与后续微调模块（如 LoRA）不兼容，破坏管线灵活性（图14）；③ 蒸馏训练本身计算开销大。因此，寻找一种既不修改扩散模型、又能大幅提升无引导生成质量的方案成为关键缺口。

本文的动机源于一项观察：同一随机种子下，从高斯噪声 $x_T$ 出发的无引导生成与从引导生成结果反转得到的噪声 $x_T^{\text{Guide}}$ 之间存在系统性差异，且该差异集中在低频傅里叶分量（图3）。这表明初始高斯噪声缺乏生成所需的结构化低频信息——一种类似“布局先验”的信号，而引导采样过程能够在初始噪声中隐式地注入此类结构（图2a）。直接学习从 $x_T$ 到 $x_T^{\text{Guide}}$ 的噪声空间映射面临两个障碍：DDIM 反转本身存在重构误差（图4），且理论分析指出噪声空间差异受图像空间差异的利普希茨上界约束（命题1），强迫噪声空间对齐反而会因反转误差造成次优解。实验证实，图像空间损失在所有自动评估指标上大幅优于噪声空间损失（表1）。

基于此，我们提出 **NoiseRefine**：用一个轻量的噪声提炼网络 $g_\phi$（例如基于 LoRA 的适配器）将随机高斯噪声映射为富含低频结构的**提炼噪声** $\hat{x}_T$，在图像空间最小化无引导去噪结果与有引导目标图像之间的差异，且全程不修改预训练扩散模型。该设计使提炼噪声能够即插即用地泛化到各类微调模型（图8a, 表4）和时间步蒸馏模型（图8b, 表5），并在保持与 CoT 模块完全兼容的同时，将推理速度降至与无引导高斯噪声相当（表7）。

## 核心创新

NoiseRefine 的核心创新在于**将扩散引导信号从“修改去噪模型”转移到“精炼初始噪声”**，从而在保持原始扩散管线完整性的前提下，实现无引导的高质量生成。相较于引导蒸馏（Guidance Distillation）等基线方法，NoiseRefine 主要改变了以下关键设计槽位（changed slots），每个改变均对性能提升形成决定性贡献。

### 1. 初始噪声类型：从高斯噪声到提炼噪声
- **基线**：直接使用随机高斯噪声 $x_T$ 进行采样，无引导时生成质量低下（FID 高达 42–63），布局紊乱（Fig. 7）。  
- **本文创新**：引入一个轻量的噪声提炼网络 $g_\phi$（基于 LoRA 适配器），将高斯噪声映射为**富含结构化低频信息的“提炼噪声”** $\hat{x}_T$（Sec 3.3）。该网络捕捉了引导采样所需的先验结构，使得后续的无引导去噪过程能够避免灾难性图像崩溃。  
- **实证支撑**：  
  - 初始噪声与反转噪声的差异集中在低频区域（Fig. 3），而提炼噪声主要在该频段注入结构化信号（Fig. 9, Fig. 10）；仅有极低频替换即可重现提炼噪声的生成效果（Fig. 15）。  
  - 在 SiT‑XL/2、SD2.1、SDXL 上，使用提炼噪声的无引导采样大幅超越高斯噪声无引导采样的 FID（例如 SD2.1：FID 14.62 vs 42.71，IS 34.90 vs 20.86），部分接近甚至超越有引导采样（Table 2）。

### 2. 训练目标空间：从噪声空间到图像空间
- **基线**：直接最小化提炼噪声与反转噪声之间的差异（噪声空间损失），受反转误差影响，产生模糊、信息量低的图像（Fig. 5）。  
- **本文创新**：优化**图像空间损失**，即最小化无引导生成的图像与引导生成的图像之间的差异（Sec 3.2）。理论分析表明，在利普希茨连续假设下，图像空间差异可约束噪声空间差异（Proposition 1），从而规避反转误差，更有效地传递引导信息。  
- **实证支撑**：  
  - Table 1 显示图像空间损失在所有评估指标（PickScore, HPSv2, AES, IR, CLIPScore）上均大幅优于噪声空间损失；例如 HPSv2 为 0.258 vs 0.087，AES 为 5.296 vs 4.079。  
  - 定性比较中，图像空间损失的模型能生成清晰、结构化的图像，而噪声空间模型输出严重模糊（Fig. 5）。

### 3. 梯度回传方式：从全梯度到多步分数蒸馏（MSD）
- **基线**：通过完整的去噪链进行全梯度反向传播（$\mathcal{L}_{\mathrm{Denoise}}$），计算开销巨大，训练不稳定（Fig. 6）。  
- **本文创新**：提出**多步分数蒸馏损失（MSD）**，在每一步去噪更新中对去噪网络梯度执行停止梯度（stop‑gradient），仅让梯度通过提炼网络回传（Eq. 4–5）。MSD 显著降低了训练显存和时间开销，同时保持优化稳定性，防止梯度爆炸。  
- **实证支撑**：  
  - Fig. 6 显示全梯度 MSE 优化收敛缓慢且出现巨幅震荡，而 MSD 损失收敛快速且稳定，最终质量更高。  
  - 消融实验表明 MSD 在所有指标上均优于全梯度训练（Fig. 35–36）。

### 4. 是否修改扩散模型：保持模型完整性
- **基线**：引导蒸馏（Meng et al.）直接修改去噪网络，导致**灾难性遗忘**，破坏微调模块（如 LoRA）的身份信息（Fig. 14），并与定制化模型不兼容。  
- **本文创新**：NoiseRefine **不修改原始扩散模型**，仅附加可插拔的噪声提炼网络 $g_\phi$。因此，提炼噪声可以直接泛化到微调模型（Fig. 8a, Table 4）和时间步蒸馏模型（SD‑Turbo, Fig. 8b, Table 5），且保留 LoRA 模块的个性化效果（Fig. 14）。  
- **实证支撑**：  
  - 在“动画”和“黏土”等微调域上，提炼噪声无引导的 PickScore 等指标接近或超过高斯噪声有引导，无需重新训练提炼网络（Table 4）。  
  - 在 SD‑Turbo 单步推理下，提炼噪声的 FID 比高斯噪声降低 2.24，IS 提升 3.76（Table 5），显示其对加速模型的高度兼容性。  
  - 用户研究中，无引导提炼噪声在图像质量偏好上以 53.96% 胜出有引导高斯噪声（Table 3），进一步验证了在不改动原始模型的前提下可达成的质量飞跃。

上述四个改变相互耦合，共同构成了 NoiseRefine 的核心机制：**通过图像空间损失训练，利用多步分数蒸馏学习一个不对原始模型产生任何修改的噪声提炼网络，从而将引导信息压缩至低频结构化噪声中，实现无引导高质量生成。**

## 整体框架

![[obsidian-vault/assets/figures/papers/repair_max_xEWooSOgaz_A_Noise/figures/003_Figure_2.jpg]]
*Figure 2: Motivation and training framework of NoiseRefine. (a) Starting from an initial noise x _ { T } , unguided sampling often produces low-quality images, necessitating sampling guidance such as \mathrm { C F G } . In contrast, the inversion noise x _ { T } ^ { \mathrm { G u i d e } } , obtained by inverting guidance-generated images from the same x _ { T } , can yield high-quality results even without guidance. This raises our central question: can we learn to map x _ { T } into \hat { x } _ { T } ? (b) Learning with a reconstruction loss between x _ { T } and x _ { T } ^ { \mathrm { G u i d e } } may be suboptimal due to errors during inversion. Instead, our model learns to refine x _ { T } in...*

![[obsidian-vault/assets/figures/papers/repair_max_xEWooSOgaz_A_Noise/figures/005_Figure_3.jpg]]
*Figure 3: Analysis of the relationship between x _ { T } and x _ { T } ^ { \mathbf { G u i d e } } . (a) Histogram of pixel-wise absolute differences. Blue: pairs of Gaussian noise and corresponding inversion noise; Orange: pairs of random Gaussian noise. (b) Magnitude difference of Fourier components, showing that x _ { T } and x _ { T } ^ { \mathrm { G u i d e } } mainly differ in lowfrequency regions*

NoiseRefine 的整体 pipeline 围绕一个核心思路构建：在保持扩散模型冻结的前提下，通过学习一个**噪声提炼网络** $g_\phi$，将标准高斯噪声转换为富含**低频结构信息**的“提炼噪声” $\hat{x}_T$，从而在无引导采样下直接生成高质量图像。该框架的动机源于现有引导蒸馏方法（如 Meng et al.）需要修改去噪网络而导致的**灾难性遗忘**与**微调模块不兼容**问题，以及无引导高斯噪声因缺乏结构化先验导致生成崩溃的瓶颈（Sec 1, Sec 4.3）。整体框架完全避免了对原始扩散模型的任何微调，确保了与 LoRA 适配器、微调模型和时间步蒸馏模型的原生兼容性（Fig. 14, Table 4, Table 5）。

### 模块构成与数据流

框架由三个核心模块组成，构成一条固定的信息流水线：

1. **噪声提炼网络 $g_\phi$（基于 LoRA 的 UNet 适配器）**：  
   接收一条随机高斯噪声 $x_T$（以及可选的文本提示 $c$ 作为条件），将其映射为提炼噪声 $\hat{x}_T = g_\phi(x_T, c)$。该网络本身是一个预训练 UNet 上叠加的轻量 LoRA 适配器，参数量远小于完整去噪模型（Sec 3.3, Table 14）。

2. **预训练扩散去噪网络 $\epsilon_\theta$**：  
   保持冻结，接收提炼噪声 $\hat{x}_T$，在无引导条件下进行多步去噪（如 DDIM），最终输出生成的图像 $\tilde{x}_0$。其作用等同于标准扩散推理管线，只是输入由高斯噪声替换为提炼噪声。

3. **多步分数蒸馏（Multi-step Score Distillation, MSD）损失**：  
   训练 $g_\phi$ 的目标函数，度量无引导生成的图像 $\tilde{x}_0$ 与同一随机种子下有引导采样得到的目标图像 $x_0^{\mathrm{Guide}}$ 之间的 L2 距离。MSD 的核心设计在于每一步去噪操作中对 $\epsilon_\theta$ 的输出执行**停止梯度（stop-gradient）**，仅让梯度通过当前步的 $g_\phi$ 和去噪步的中间结果，而不回传通过完整的去噪图（Sec 3.3, Eq. 4–5）。这一设计 **从根本上防止了梯度爆炸和训练崩溃**，同时避免了像全梯度损失 $\mathcal{L}_{\mathrm{Denoise}}$ 那样高昂的计算代价（Fig. 6, Fig. 35-36）。

### 训练与推理流程

**训练阶段**（Fig. 2 右侧, Fig. 38）：  
- 从相同的高斯噪声 $x_T$ 出发，先用标准引导采样（CFG 或 CFG+PAG）生成高质量目标图像 $x_0^{\mathrm{Guide}}$，作为监督信号。  
- 同一 $x_T$ 送入 $g_\phi$ 得到 $\hat{x}_T$，再通过冻结的 $\epsilon_\theta$ 进行无引导多步去噪获得 $\tilde{x}_0$。  
- 通过 MSD 损失在图像空间比较 $\tilde{x}_0$ 和 $x_0^{\mathrm{Guide}}$，梯度沿去噪步以“蒸馏”形式传递回 $g_\phi$，更新其 LoRA 参数，而 $\epsilon_\theta$ 参数不动。  
- 训练无需成对图像数据集；使用随机种子和提示即可无限生成训练样本。

**推理阶段**：  
- 给定一个文本提示，生成随机高斯噪声 $x_T$，送入训练好的 $g_\phi$ 得到 $\hat{x}_T$，然后直接通过原始扩散模型以无引导采样生成最终图像。推理过程中的去噪步数与采样器可灵活选择，提炼噪声对此具有良好鲁棒性（Fig. 28）。由于不涉及引导计算，推理耗时接近标准无引导采样，显著快于有引导方案（Table 7）。

### 有效性的因果枢纽：低频结构信息的注入

分析表明，高斯噪声与对应引导采样图像的反转噪声（inversion noise）之间的差异 **集中于低频区域**（Fig. 3），且仅替换极低频成分（如半径 $<0.03$）即可重现提炼噪声的生成效果（Fig. 15）。因此，$g_\phi$ 实际上学习的是在初始化阶段注入一种**粗粒度的结构布局**（如物体位置、轮廓），使得去噪网络在无引导条件下仍能形成有意义的注意力图和一致的生成轨迹（Fig. 10, Fig. 11, Fig. 20）。这一机制解释了为何在完全不修改去噪网络的情况下，无引导生成质量能大幅逼近甚至（在用户研究中）超越有引导高斯噪声（Table 3）。

综上，NoiseRefine 的框架将“引导信息”从传统的去噪网络修改方式转移到初始噪声空间，以**即插即用的噪声提炼器**实现了无引导高质量生成，同时继承了原扩散模型的所有下游兼容性。

## 核心模块与公式推导

NoiseRefine 的核心思想是将随机高斯噪声映射到富含结构化低频成分的“提炼噪声”，从而在不使用采样引导的情况下提升生成质量。现有引导蒸馏方法需要修改去噪网络，导致灾难性遗忘、与微调模块（如 LoRA）不兼容，且训练计算开销大。NoiseRefine 完全冻结原始扩散模型，仅在初始噪声空间附加一个可训练的提炼网络，通过图像空间的重构损失进行优化，训练稳定且保持管线完整性。

### 1. 噪声提炼网络 $g_\phi$

提炼网络 $g_\phi$ 的目标是学习从高斯噪声到结构化噪声的映射 $\hat{x}_T = g_\phi(x_T, c)$，其中 $x_T \sim \mathcal{N}(0, I)$ 为初始随机噪声，$c$ 为可选的条件（如文本提示）。网络采用基于预训练 UNet 的轻量 LoRA 适配器，参数 $\phi$ 远小于完整模型（Sec 3.3，Table 14）。训练后的提炼网络可在推理时以极低的延迟将一个高斯噪声转换为提炼噪声，随后送入冻结的扩散模型执行无引导 DDIM 采样。

**关键作用**：提炼网络捕捉了引导采样在噪声空间产生的低频结构差异（Figure 3, Figure 9），并将这种差异显式编码进初始噪声。实验表明，仅替换初始噪声最外 $[0, 0.03]$ 半径频段的频率分量，即可复现提炼噪声的主要生成效果（Figure 15, Appendix A.2），验证了低频成分的核心地位。

### 2. 训练目标空间：图像空间 v.s. 噪声空间

早期的直接映射思路是在噪声空间最小化提炼噪声与反转噪声的差异 $d(x_T, x_T^\text{Guide\dagger})$。然而，反转过程本身存在误差（Figure 4），且噪声空间损失训练出的模型生成图像模糊（Table 1, Figure 5）。NoiseRefine 转向图像空间优化，理论基础为 **Proposition 1**（Sec 3.2）：

$$
d\big(x_T, x_T^{\mathrm{Guide}\dagger}\big) < \kappa\; d\big(x_0, x_0^{\mathrm{Guide}}\big)
$$

假设去噪映射（从噪声到图像的完整链）满足李普希茨连续，则图像空间的重构误差为噪声空间差异提供了上界。因此，通过最小化无引导生成图像 $\hat{x}_0$ 与有引导生成图像 $x_0^\mathrm{Guide}$ 的距离，可间接约束噪声空间差异，并直接获得高质量生成结果。Table 1 中，图像空间损失在 PickScore、HPSv2、AES、IR、CLIPScore 五项指标上全面大幅优于噪声空间损失，其中 HPSv2 由 0.087 提升至 0.258。

### 3. 多步分数蒸馏损失 (MSD)

全梯度去噪损失要求通过全部 $T$ 个去噪步骤反向传播，计算图庞大且易导致梯度爆炸（Figure 6，橙色曲线）：

$$
\mathcal{L}_{\mathrm{Denoise}}\big(g_\phi(x_T),\theta\big) = d\!\left(D_1\!\left(\dots D_T(g_\phi(x_T))\right), x_0^{\mathrm{Guide}}\right)
$$

其中 $D_t(x) = a_t x_t + b_t \epsilon_\theta^{(t)}(x)$ 为单步 DDIM 更新（Eq. 2），$a_t, b_t$ 为依时间步的系数，$\epsilon_\theta^{(t)}$ 为冻结的去噪网络预测噪声。

为稳定训练并降低计算开销，NoiseRefine 提出 **多步分数蒸馏损失 (MSD)**（Eq. 4-5）：

$$
\mathcal{L}_{\mathrm{MSD}}\big(g_\phi(x_T),\theta\big) = d\!\left(F_1\!\left(\dots F_T(g_\phi(x_T))\right), x_0^{\mathrm{Guide}}\right)
$$

每一步被修改为 $F_t(x) = D_t(\,\text{sg}(x)\,)$，其中 $\text{sg}(\cdot)$ 为停止梯度操作（stop-gradient），阻断去噪网络 $\epsilon_\theta$ 的梯度回传。因此，优化过程仅更新提炼网络 $g_\phi$ 的参数 $\phi$，训练目标直接比较无引导输出 $\hat{x}_0$ 与引导目标 $x_0^\mathrm{Guide}$ 的 $L_2$ 距离。Figure 6（蓝色曲线）表明，MSD 损失收敛平稳，完全避免梯度爆炸，且最终生成质量显著优于全梯度 MSE。

训练阶段，引导目标图像 $x_0^\mathrm{Guide}$ 由冻结的扩散模型配合有引导采样（如 CFG 或 PAG）生成，仅作为监督信号而不参与梯度计算。对应的引导噪声预测形式为（仅供参考，不构成 NoiseRefine 的核心模块）：

$$
\epsilon_\theta^{\mathrm{CFG}}(x_t, c) = \epsilon_\theta(x_t, c) + w\big(\epsilon_\theta(x_t, c) - \epsilon_\theta(x_t)\big), \quad
\epsilon_\theta^{\mathrm{PAG}}(x_t) = \epsilon_\theta(x_t) + s\big(\epsilon_\theta(x_t) - \hat{\epsilon}_\theta(x_t)\big)
$$

其中 $w, s$ 为引导强度，$\hat{\epsilon}_\theta$ 为扰动自注意力后的预测（Appendix D.1）。这些引导仅在训练时产生目标图像，推理阶段完全弃置。

综上，NoiseRefine 通过冻结去噪网络、仅训练轻量噪声提炼网络、采用图像空间 MSD 损失，实现了将计算昂贵的引导信号蒸馏进初始噪声，使无引导采样质量达到甚至超越有引导高斯噪声的水平。

## 实验与分析

![[obsidian-vault/assets/figures/papers/repair_max_xEWooSOgaz_A_Noise/figures/007_Table_1.jpg]]

![[obsidian-vault/assets/figures/papers/repair_max_xEWooSOgaz_A_Noise/figures/014_Table_2.jpg]]
*Table 2: Quantitative comparison of image quality. 30K prompts from MS-COCO (Lin et al., 2014) validation dataset were used for evaluation. Guidance Distil. indicates guidance distillation (Meng et al., 2023). Table 3: User study on image quality and prompt adherence*

![[obsidian-vault/assets/figures/papers/repair_max_xEWooSOgaz_A_Noise/figures/015_Table_3.jpg]]

![[obsidian-vault/assets/figures/papers/repair_max_xEWooSOgaz_A_Noise/figures/013_Figure_8.jpg]]
*Figure 8: Generalizability and compatibility of refined noise. (a) Results on fine-tuned models (animation and clay object domains) comparing Gaussian vs. refined noise. (b) Results on timestepdistilled models (SD-Turbo), showing that refined noise improves structural coherence and quality over Gaussian noise*

### 主要结果：提炼噪声在无引导下实现质量飞跃
扩散模型在无引导采样时生成质量显著下降——这是本文试图打破的瓶颈：**无引导的扩散采样缺少结构化噪声先验，导致去噪轨迹混乱，无法形成有意义的空间布局**。NoiseRefine 通过学习将高斯噪声映射到“提炼噪声”，在不更改扩散管线的前提下，使无引导生成逼近甚至超越有引导的质量。

在 SiT‑XL/2（类别条件）、SD2.1 和 SDXL（文生图）三个规模差异巨大的模型上，提炼噪声的无引导采样均带来 FID 与 IS 的巨幅改善（表 2）。其中 SD2.1 的 FID 从 42.71 降至 14.62（降幅 65.8%），IS 从 20.86 升至 34.90；SDXL 的 FID 更从 63.28 压至 26.22。在 ImageNet 的 SiT‑XL/2 上，提炼噪声的 FID=10.80 已显著优于无引导的 18.43，表明**噪声空间的结构化映射具有跨模型、跨任务的有效性**。关键对照是：有引导高斯噪声（SD2.1 的 FID=14.48）与无引导提炼噪声（14.62）极其接近，这在图 7 的定性对比中得到直观印证——高斯噪声无引导生成图像结构崩溃，而提炼噪声无引导则产出连贯、高质量的画面。

### 训练目标的因果作用：图像空间损失 × MSD 蒸馏
为何直接学习噪声空间映射（噪声→反转噪声）会失败？**Proposition 1 揭示了噪声差异受图像差异的上界约束，但反转过程存在累积误差**（图 4）。为绕过反转误差，NoiseRefine 在图像空间定义损失，要求从提炼噪声去噪出的图像匹配有引导的目标图像。表 1 的消融实验给出了决定性证据：噪声空间损失模型生成的图像模糊且指标急剧劣化（PickScore 17.97 vs 21.62，HPSv2 0.087 vs 0.258，AES 4.079 vs 5.296），而图像空间损失在所有自动评估维度上跃升。图 5 的样本对比进一步说明，直接学习噪声映射几乎无法恢复高频细节，间接证明了**噪声空间微小差异会被扩散模型放大为图像级灾难**。

训练方式的选择同样关键。全梯度去噪损失（$\mathcal{L}_{\mathrm{Denoise}}$）需要通过所有去噪步反向传播，内存消耗极大且优化不稳定；MSD 损失（多步分数蒸馏，公式 4–5）在每一步对去噪网络执行停止梯度（stop‑gradient），将梯度路径限制在噪声提炼网络，既降低计算量又消除梯度爆炸。图 6 的收敛曲线显示，MSD 损失平滑收敛，而全梯度 MSE 优化在相同步数下震荡严重。这一设计是 NoiseRefine 能以相当于原始 SD2.1 训练量 0.054% 的 NFE（约 5.65M，表 8）完成训练的前提。

### 与有引导采样的人偏好对比：用户研究
仅靠自动指标不足以反映感知质量。在 1000 对图像的用户研究中，参与者在图像质量上对**无引导提炼噪声的偏好率（53.96%）反超有引导高斯噪声（46.04%）（表 3）**，提示遵循度同样占优（51.76% vs 48.24%）。这说明提炼噪声所编码的结构化信息，在人类感知中与实时计算代价高昂的 CFG/PAG 引导相当。值得注意的是，有引导采样的推理耗时显著高于无引导（SD2.1 上单张约 0.71 s vs 0.37 s，表 7），因此**NoiseRefine 在保持质量的同时将推理成本减半**。

### 泛化、兼容与鲁棒性
提炼噪声与扩散管线完全解耦的特性带来两大优势：**微调模型零样本移植**与**时间步蒸馏模型兼容**。在粘土风格和动画风格的微调 SD2.1 模型上，直接使用在原模型上训练的噪声提炼网络，无引导生成即可在多项指标上接近或超越有引导高斯噪声（表 4，图 8a）；而在少步蒸馏模型 SD‑Turbo 上，单步推理的提炼噪声就超过两步高斯噪声的性能（FID 24.94 vs 27.18，IS 38.07 vs 34.31，表 5），且画面结构更连贯（图 8b）。此外，提炼噪声对采样器（DDIM、Euler、Heun）和去噪步数（10–50 步）表现出高度鲁棒性（图 28），且能与标准 LoRA 模块无缝协作——Guidance Distillation 方法会破坏 LoRA 身份一致性，而 NoiseRefine 完整保留（图 14）。

### 失效条件与局限
尽管优势显著，NoiseRefine 存在以下可复现的弱项：
- **训练仍需引导**：噪声提炼网络依赖有引导采样生成目标图像，训练计算量（约 5.65M NFE）虽远低于预训练，但无法完全消除对引导的依赖。
- **极低步数退化**：在单步去噪（N=1）时，性能提升幅度有限（SD‑Turbo 上 FID 从 27.18 降至 24.94），表明**结构化噪声优势在较长的去噪链路上更为明显**。
- **跨架构迁移成本**：提炼网络与特定扩散模型的权重绑定，换用不同架构需重新训练；当前未在视频、3D 等模态验证。
- **指标滞后于有引导**：在 SDXL 上，即使 FID 大幅改善，仍与有引导结果存在差距（26.22 vs 22.04），提示大规模模型可能受益于更强的噪声结构化。
- **偏差继承**：提炼噪声的质量上限受到引导生成目标图像质量的制约，若引导本身带有偏差（如高频伪影），这些偏差可能被蒸馏进噪声先验。
- **控制粒度有限**：强度调节目前通过简单缩放差异信号实现（图 13），缺乏对布局、姿态等语义属性的独立控制。

### 核心图表证据链
以下图表构成从动机到机制的完整因果链，建议重点查阅：
- **图 3、9、10、15**：揭示提炼噪声与高斯噪声的差异集中于低频分量，且仅替换极低频率段（截止半径 0.03）即可复现提炼噪声的生成效果——解释了“结构化信息以低频布局形式编码”这一核心洞察。
- **图 11、20**：展示提炼噪声使去噪轨迹从首步就形成有意义的交叉注意力图，进而保持 $x_0$ 预测的时空一致性，说明噪声结构通过约束去噪动力学提升生成质量。
- **表 1 与图 5**：系统比较噪声空间和图像空间损失，确立了图像空间训练的必要性。
- **表 2、7、3**：贯穿定量质量、计算效率与人类偏好三个维度的核心指标，支撑“无引导可替代有引导”的结论。
- **图 8、表 4–5**：验证提炼噪声作为独立模块的即插即用能力，这是其相较 Guidance Distillation 类方法的关键工程优势。

## 方法谱系与知识库定位

**范式定位**  
NoiseRefine 并未遵循「将引导信号蒸馏进去噪网络」的主流路径（如 Meng et al. 的 guidance distillation），也不同于直接学习初始噪声到反转噪声映射的简单方案，而是通过一个可训练的噪声提炼网络 $g_\phi$，在高斯噪声空间与引导生成图像的隐式结构化噪声之间建立映射。该方法的核心干预点位于**生成管线的入口——初始噪声**，而非去噪过程本身。这一设计使其从根本上区别于：

1. **无引导高斯噪声采样**：最基础的生成范式，FID 极高（SD2.1 上 42.71，Table 2），因为缺乏任何结构性先验；
2. **有引导采样（CFG、PAG 等）**：当前高质量生成的标准方案，但推理时须对每个去噪步执行额外的网络前向，成本翻倍（Table 7）；
3. **引导蒸馏（如 Meng et al.）**：通过微调去噪网络吸收引导信号，虽然推理时无需引导，但会引发灾难性遗忘、丧失 LoRA 兼容性（Figure 14），且训练需完整反向传播，计算开销大；
4. **噪声空间直接回归**：尝试直接学习 $x_T$ 到反转噪声 $x_T^{\mathrm{Guide}}$ 的映射，由于反演误差（Figure 4）和损失空间不对齐，生成图像模糊且指标全面落后（Table 1, Figure 5）。

NoiseRefine 在这幅谱系图中的独特之处在于：它**冻结原始扩散模型**，仅训练一个轻量的 LoRA 适配器来「提炼」高斯噪声，并以**图像空间损失**配合**多步分数蒸馏（MSD）**实现稳定优化。这使其既能像有引导采样那样获得高质量图像，又保留了无引导推理的低计算成本与流水线完整性。

**与 Baseline 的实证对比**  
- 在 SiT-XL/2、SD2.1、SDXL 三个模型上，使用提炼噪声的无引导采样均大幅击败高斯噪声无引导基线：SD2.1 的 FID 从 42.71 降至 14.62（↓65.8%），IS 从 20.86 升至 34.90；SDXL 的 FID 从 63.28 降至 26.22（Table 2）。  
- 相比于引导蒸馏模型，提炼噪声在 SD2.1 上 FID 更低（14.62 vs. 16.43），且推理时无额外计算，而引导蒸馏破坏了原始去噪网络的权重，导致微调模型与 LoRA 模块失效（Figure 8(a), Table 4, Figure 14）。  
- 用户研究显示，无引导提炼噪声在图像质量偏好率上甚至略优于有引导高斯噪声（53.96% vs. 46.04%，Table 3），表明提炼噪声在主观感知层面达到了有引导生成的水平。  

消融实验进一步揭示了关键设计选择：**图像空间损失**在所有自动评估指标（PickScore, HPSv2, AES 等）上均远超噪声空间损失（Table 1）；**MSD 损失**比全梯度反向传播更稳定、收敛更快，并有效避免了梯度爆炸（Figure 6）。噪声提炼网络需具备一定的参数容量（基于预训练 UNet + LoRA），单纯的 MLP 参数化无法生成有意义的提炼噪声（Table 10, Figure 27）。

**适用边界与兼容性**  
- **适用模型**：NoiseRefine 在基于 Transformer 的 SiT-XL/2、基于 UNet 的 SD2.1 和 SDXL 上均有效，说明其对架构不敏感。  
- **零样本域泛化**：在未经重新训练的动画、粘土等微调模型上，提炼噪声可直接迁移使用，无引导质量显著优于高斯噪声（Table 4）。  
- **与蒸馏模型的协同**：提炼噪声可与时间步蒸馏模型（SD-Turbo）结合，单步推理的 FID 即优于两步高斯噪声（FID 24.94 vs. 27.18，Table 5），且结构一致性更好（Figure 8(b)）。  
- **流水线兼容**：提炼网络独立于去噪网络，因此与各种采样器（DDIM、Euler、Heun）、不同去噪步数以及 LoRA 模块完全兼容（Figure 14, Figure 28），避免了引导蒸馏的灾难性遗忘问题。  

**局限性与改进空间**  
尽管 NoiseRefine 在多个维度展现了显著优势，仍存在若干边界与限制：  
1. **训练代价**：提炼网络训练需要引导采样生成目标图像，训练 NFE 约 5.65M，虽仅相当于原始 SD2.1 训练量的 0.054%（Table 8），但依然构成一定计算预算。  
2. **模型特异性**：提炼网络仅针对特定预训练模型训练，跨架构（如从 UNet 转到 Transformer）迁移可能需要重新训练，未验证零样本跨架构泛化能力。  
3. **极低步数受限**：当去噪步数 N=1 时，性能提升有限（尽管仍优于高斯噪声），表明提炼噪声的优势部分依赖于多步去噪中早期低频布局的形成（Table 5 中 SD-Turbo 1-step 的 FID 降幅仅 2.24）。  
4. **未探索模态**：当前验证限于文本到图像及类别条件生成，尚未在视频、3D 生成等任务上测试。  
5. **与有引导采样的差距**：大幅缩小但未完全消除与有引导采样的指标差距（如 SDXL 有引导 FID 为 16.65，提炼噪声为 26.22），仍存在进一步优化空间。  
6. **控制粒度粗**：噪声提炼强度的调整目前仅依赖对差异信号的线性缩放（Figure 13），缺乏对布局、姿态等语义属性的精细解耦控制。  
7. **引导偏差继承**：提炼噪声的质量上限受制于训练时所采用的引导方式（CFG+PAG），若引导本身存在虚假关联或偏差，提炼噪声可能将其编码进提炼网络的参数中。  

**开放问题**  
- **低频结构的形成机理**：实验表明提炼噪声与高斯噪声的主要差异集中在低频分量（Figure 3, Figure 9），且仅替换极低频（0~0.03 频带）即可重现提炼噪声的生成效果（Figure 15）。但**扩散模型为何在没有引导时难以自主形成这些低频结构成分**？这一现象的根本原因（模型容量、优化动力学或数据分布特性）仍待揭示。  
- **训练阶段消除引导**：当前 NoiseRefine 仍依赖引导样本作为监督信号。能否通过对抗训练、自监督信号或利用去噪网络自身的隐式知识，**在训练阶段完全摆脱引导依赖**？  
- **结构化噪声的显式解耦**：提炼噪声中似乎编码了物体的粗略布局与姿态信息。能否将这些信息解耦为可控的潜变量，从而**无需引导即可独立操控布局、物体姿态与场景构成**？  
- **跨模态与多任务拓展**：将 NoiseRefine 的思想推广到**文本到视频、音频生成、分子生成**等其他扩散任务，需要验证是否存在类似的“结构化噪声先验”及其普适性。  
- **高效多样化控制**：提炼噪声空间本身是否具备多样性调节潜力？例如通过噪声插值或噪声增强实现可控的概念组合，目前仅有线性强度缩放，**更灵活且解耦的多样性控制机制**是值得探索的方向。  

整体而言，NoiseRefine 在扩散生成方法谱系中开辟了一条「入口优化」的新路径，其核心洞察（将引导信息蒸馏到噪声空间而非模型权重）不仅解耦了质量与推理成本，也保留了预训练模型生态的全部兼容性。上述局限和开放问题指明了进一步降低训练依赖、增强可控性以及向多模态扩展的后续研究方向。

## 原文 PDF

## 相关样本

- [[obsidian-vault/analysis/ICLR_2026/Adaptive_Moments_are_Surprisingly_Effective_for_Plug-and-Play_Diffusion_Sampling.md|Adaptive Moments]]：同属 diffusion guidance 样本，可对照噪声先验细化与显式引导梯度稳定化。

![[obsidian-vault/paperPDFs/ICLR_2026/A_Noise_is_Worth_Diffusion_Guidance.pdf]]
