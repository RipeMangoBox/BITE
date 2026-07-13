---
title: "A Lesson in Splats: Teacher-Guided Diffusion for 3D Gaussian Splats Generation with 2D Supervision"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/A_Lesson_in_Splats_Teacher_Guided_Diffusion_for_3D_Gaussian_Splats_Generation_with_2D_Supervision.pdf
project_link: https://lesson-in-splats.github.io/
code_link: null
aliases:
- LSTGD3GSG2S
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将去噪的噪声样本（3D）与监督信号（2D）解耦，利用确定性模型作为“噪声教师”生成噪声样本，并引入多步去噪训练策略以传播图像监督梯度到低噪声时间步。"
primary_logic: "在高噪声时间步（t > t*）下，噪声教师的噪声样本分布与真实分布对齐，可以作为有效的扩散训练输入；通过多步去噪（而非单步）使模型能够在所有噪声水平上接收图像渲染损失，从而恢复精细细节并超越教师模型。"
claims:
- "在ShapeNet-SRN Cars上，SplatDiffusion (Medium) PSNR达到24.84，比Splatter Image (Large) 提高0.84 dB。"
- "在RealEstate10K多设置下，SplatDiffusion平均PSNR比Flash3D提高约0.5 dB。"
- "Stage II纯渲染损失微调显著优于保留扩散损失或继续使用教师监督，PSNR提升约1.3 dB。"
- "循环一致性正则化在Stage I和Stage II均带来稳定提升。"
---

# A Lesson in Splats: Teacher-Guided Diffusion for 3D Gaussian Splats Generation with 2D Supervision

> [!tip] 核心洞察
> 在高噪声时间步（t > t*）下，噪声教师的噪声样本分布与真实分布对齐，可以作为有效的扩散训练输入；通过多步去噪（而非单步）使模型能够在所有噪声水平上接收图像渲染损失，从而恢复精细细节并超越教师模型。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Splat一课：基于2D监督的教师引导扩散方法用于3D高斯泼溅生成 |
| 英文题名 | A Lesson in Splats: Teacher-Guided Diffusion for 3D Gaussian Splats Generation with 2D Supervision |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2412.00623) · [Project](https://lesson-in-splats.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SplatDiffusion |
| Dataset | ShapeNet-SRN Cars (single view), ShapeNet-SRN Chairs (single view), RealEstate10K (5 frames), RealEstate10K (10 frames) |

> [!tip] 效果简介
> - ShapeNet-SRN Cars (single view) 上，PSNR / SSIM / LPIPS 为 24.84 / 0.93 / 0.077，对比 Splatter Image (Large) 24.00 / 0.92 / 0.078，变化 +0.84 / +0.01 / -0.001。
> - ShapeNet-SRN Chairs (single view) 上，PSNR / SSIM / LPIPS 为 25.21 / 0.93 / 0.066，对比 Splatter Image (Large) 24.43 / 0.93 / 0.067，变化 +0.78 / 0.00 / -0.001。
> - RealEstate10K (5 frames) 上，PSNR / SSIM / LPIPS 为 29.12 / 0.932 / 0.087，对比 Flash3D 28.46 / 0.899 / 0.100，变化 +0.66 / +0.033 / -0.013。

## 概要

### 问题背景

从单张或少量图像重建3D场景是计算机视觉的核心挑战。近年来，基于3D高斯泼溅（3D Gaussian Splatting, 3DGS）的前馈确定性模型（如 **Splatter Image**，Szymanowicz et al., CVPR 2024；**Flash3D**，Szymanowicz et al., arXiv 2024）在单视图3D重建上取得了显著进展，但其本质缺陷在于：确定性映射只能产生模糊的平均预测，无法捕获多解性——即同一输入视图可能对应多种合理的3D解释。

扩散模型天然具备表达多模态分布的能力，然而将其应用于3D生成面临一个根本性瓶颈：**标准扩散训练要求去噪信号和真值监督处于同一模态（3D）**，而高质量3D数据集极为稀缺，难以获取大规模3D真值监督。这构成了一个看似无解的矛盾——没有足够的3D数据，就无法训练3D扩散模型；而无法训练3D扩散模型，就无法超越确定性方法的上限。

### 核心洞见

本文提出的 **SplatDiffusion** 方法通过一个关键观察打破了上述困境：**在高噪声时间步下（t > t*），由确定性教师模型生成的噪声样本，其分布与从真实3D分布前向加噪得到的分布已足够对齐**。这意味着，即使教师模型的预测本身不完美（含有噪声），其在高噪声水平下的噪声化版本仍可作为有效的扩散训练输入。

基于此洞见，SplatDiffusion 将扩散训练中的两个要素解耦：
- **噪声样本**保持为3D模态（由“噪声教师”生成）
- **监督信号**切换为2D模态（通过可微渲染器将去噪后的3DGS渲染为图像，与目标视图计算损失）

这一解耦使得模型能够利用大规模2D图像数据进行训练，同时保持对3D表示的生成能力。

### 方法定位

SplatDiffusion 在方法谱系上位于**3D感知生成模型**与**2D监督3D学习**的交叉点：

| 维度 | 定位 |
|------|------|
| **表示空间** | 3D高斯泼溅（3DGS） |
| **生成范式** | 条件扩散模型，以单张源图像为条件 |
| **监督来源** | 2D图像渲染损失 + 循环一致性自监督 |
| **教师依赖** | 预训练的确定性前馈3DGS预测器（可替换） |
| **训练策略** | 两阶段：引导（Bootstrapping）+ 多步去噪微调 |

与现有工作的关键区别：
- 相比 **Viewset Diffusion**（Szymanowicz et al., CVPR 2023）等从2D数据学习3D生成的方法，SplatDiffusion 直接在3D空间执行去噪，避免了视图一致性问题。
- 相比 **NeRFDiff** 等扩散式单视图NeRF重建，SplatDiffusion 采用显式3DGS表示，渲染效率更高，且模型体积更小。
- 相比其教师模型 Splatter Image / Flash3D，SplatDiffusion 以**更小的U-Net架构（Medium，约一半参数量）**实现了显著的性能超越，证明增益来自扩散框架的多模态建模能力而非容量优势。

### 主要结果

在物体级和场景级基准上的实验一致验证了方法的有效性：

- **ShapeNet-SRN Cars**（单视图重建）：SplatDiffusion (Medium) PSNR 达 **24.84 dB**，比 Splatter Image (Large) 的 24.00 dB 提升 **0.84 dB**（Table 1）。
- **ShapeNet-SRN Chairs**：PSNR 达 **25.21 dB**，提升 0.78 dB。
- **RealEstate10K**（场景级新视图合成）：在5帧、10帧和随机基线范围三种设置下，平均PSNR比 Flash3D 提升约 **0.5 dB**，SSIM和LPIPS均有显著改善（Table 2）。
- **Co3D hydrant**：PSNR 达 **22.34 dB**，比 Splatter Image 提升 0.57 dB（Table 6）。

消融实验揭示了方法设计的关键要素：
- **多步去噪微调（Stage II）**仅使用渲染损失，比保留扩散损失或继续使用教师监督提升约 **1.3 dB**（Table 4 b.4 vs b.3）。
- **循环一致性正则化**在两个训练阶段均带来稳定提升：Stage I 提升约 **1.1 dB**，Stage II 提升约 **0.2 dB**（Table 4 c组）。
- **时间步加权损失**相比均匀加权进一步改善性能（Table 9）。

### 局限与开放问题

SplatDiffusion 仍存在若干局限：训练依赖预训练教师模型的质量；多步去噪训练（Stage II）显存和计算开销较大；在严重遮挡区域可能出现高斯分布不均匀导致过平滑。开放问题包括：如何自动确定最优临界时间步 t*、多步去噪策略能否推广至NeRF等其他3D表示、以及如何在更复杂的真实场景（动态、非朗伯表面）中保持有效性。

### 3D生成的任务困境：模态耦合与数据瓶颈

从单张或少量二维图像重建完整的三维场景，是计算机视觉中长期存在的核心挑战。近年来，3D高斯泼溅（3D Gaussian Splatting, 3DGS）作为一种兼具高质量渲染和实时性能的显式三维表示，迅速成为该领域的前沿方案。然而，如何为3DGS构建具有**多解性**（即同一输入图像可对应多个合理的三维解释）的生成模型，仍是一个悬而未决的问题。

扩散模型（Diffusion Models）在图像、视频等二维生成任务中展现了强大的多模态分布建模能力，理论上同样适合处理三维重建中的歧义性。但将其直接应用于3DGS生成时，面临一个根本性的**模态耦合瓶颈**：标准扩散模型的训练要求去噪信号和真值监督处于同一模态。具体而言，扩散模型学习将噪声化的3D高斯样本去噪为干净的三维表示，其损失函数天然地需要在三维空间中进行逐参数监督。这意味着训练必须依赖大规模、高质量的**三维真值数据集**——而这类数据在现实中极为稀缺，获取成本远高于二维图像。

### 确定性前馈模型的局限：平均解而非多解

为规避三维数据瓶颈，现有工作转而采用**确定性前馈模型**（如Splatter Image、Flash3D等），直接从单张图像回归3DGS参数。这类方法仅需二维图像监督即可训练，通过在多个新视角上计算渲染损失来驱动三维重建。然而，确定性回归的本质决定了它们只能输出一个“平均”解：面对输入图像中不可见的遮挡区域或模糊纹理，模型倾向于产生模糊、过平滑的几何结构，无法捕获真实世界中三维场景的**多解性**——即从同一视角出发，合理的完整三维形状可以有多种可能。

换言之，当前方法陷入了一个两难境地：
- **3D监督的扩散模型**：能建模多解性，但受限于三维数据的匮乏；
- **2D监督的确定性模型**：数据获取容易，但丧失了生成多样性的能力。

### 核心动机：解耦噪声样本与监督信号

本文的核心洞察在于一个关键问题：**能否打破模态耦合的枷锁，让扩散模型在仅使用二维图像监督的条件下，仍然保持对三维多解性的建模能力？**

这一问题的肯定回答将带来双重收益：一方面，扩散模型的多解生成能力得以保留，使重建结果不再局限于单一的平均解；另一方面，训练仅需廉价的二维图像渲染损失，无需昂贵的三维真值标注。实现这一目标的技术关键在于将扩散训练中的两个要素**解耦**：
- **噪声样本的来源**（必须保持为三维，以驱动3DGS的去噪过程）；
- **监督信号的来源**（可以是二维渲染图像，通过可微渲染器桥接模态差异）。

基于这一动机，本文提出了**SplatDiffusion**框架，利用预训练的确定性前馈模型作为“噪声教师”（Noisy Teacher）生成噪声化的三维样本，并通过多步去噪策略将二维渲染损失有效传播到扩散模型的各个噪声水平，从而在2D监督下训练出超越教师模型的3DGS扩散生成器。

## 核心方法与创新机理

SplatDiffusion 的核心创新在于打破标准扩散模型训练中“去噪信号与监督信号必须处于同一模态”的限制，提出了一套**教师引导的跨模态扩散训练框架**。其关键设计围绕以下五个 changed slots 展开。

### 1. 训练监督模态解耦

标准 3D 扩散模型要求去噪输出的 3D 表示与监督信号同为 3D 真值，然而高质量 3D 数据集稀缺，直接获取大规模 3D 监督极为困难。SplatDiffusion 将二者解耦：**噪声样本保持为 3D 高斯泼溅（由噪声教师生成），而监督信号使用 2D 渲染图像**。这一设计使得模型可以充分利用大规模 2D 图像数据（如多视图数据集）进行训练，而无需依赖 3D ground truth（Section 3.1）。

### 2. 多步去噪训练策略

传统扩散训练采用单步去噪：输入噪声样本 $s_t$，直接预测干净样本并与真值比较。SplatDiffusion 在 Stage II 中引入**多步去噪训练**：从高噪声时间步 $t > t^*$ 开始，通过 DDIM 采样器逐步去噪至 $t=0$，对最终干净预测的渲染结果计算加权 L2 损失：

$$\mathcal{L}_{\mathrm{mlt-stp}} = \mathbb{E}_{\boldsymbol{x}_{\mathrm{src}}, \boldsymbol{v} \sim \mathcal{U}[k], t > t^*, \epsilon} \left[ \lambda_t \lVert \boldsymbol{x}_{\mathrm{tgt}}^{\boldsymbol{v}} - \mathcal{R}(\hat{s}_0, \boldsymbol{v}) \rVert_2^2 \right]$$

多步去噪使得**图像渲染损失的梯度能够通过可微渲染器反向传播至所有噪声水平**，从而恢复精细细节并超越教师模型。消融实验表明，Stage II 中仅使用渲染损失（去除扩散损失）可带来约 1.3 dB 的 PSNR 提升（Table 4 b.4 vs b.3）。

### 3. 噪声教师引导初始化

SplatDiffusion 并非从随机初始化训练扩散模型，而是采用**两阶段训练**：先用预训练的确定性 3DGS 预测器（如 **Splatter Image**, Szymanowicz et al., CVPR 2024）作为“噪声教师”，通过单步去噪与渲染损失的联合引导进行引导阶段（Bootstrapping），再进入多步微调。引导阶段的组合损失为：

$$\mathcal{L}_{\mathrm{bootstrap}} = \mathbb{E}_{x_{\mathrm{src}}, v \sim \mathcal{U}[k], t \sim \mathcal{U}[T], \epsilon} [\ell_{3\mathrm{DGS}} + \ell_{\mathrm{image}}]$$

其中 $\ell_{3\mathrm{DGS}}$ 直接监督去噪器输出与教师干净样本之间的 L2 距离，$\ell_{\mathrm{image}}$ 通过渲染去噪结果与目标视图比较。消融实验证实引导阶段是必要的：若仅使用渲染损失而无 3D 扩散损失，PSNR 从 22.61 骤降至 18.82（Table 8）。

### 4. 循环一致性正则化

SplatDiffusion 引入**循环一致性损失**作为额外正则化：将去噪后渲染的目标图像再次输入模型预测 3DGS，并渲染回源视角进行自监督：

$$\mathcal{L}_{\mathrm{cyc}} = \| x_{\mathrm{src}} - \mathcal{R}(\tilde{s}_0, v_{\mathrm{src}}) \|_2^2$$

该损失在两个阶段均带来稳定提升：Stage I 中 PSNR 从 22.61 提升至 23.73（+1.1 dB），Stage II 中从 24.69 提升至 24.91（+0.2 dB）（Table 4 c.1 vs c.2, c.3 vs c.4）。

### 5. 更小的扩散模型架构

尽管扩散模型通常需要较大容量，SplatDiffusion 采用 **Medium U-Net**（约一半参数量），却超越了使用 Large U-Net 的教师模型 **Splatter Image**（Table 1: PSNR 24.84 vs 24.00）。同等规模的确定性前馈模型（Feedforward Medium）PSNR 仅 19.99，证明性能增益来自扩散框架本身而非模型容量（Table 7）。

### 创新机制的内在逻辑

上述五个 changed slots 构成一条连贯的创新链条：**模态解耦**使 2D 监督成为可能，**噪声教师引导**提供可行的初始化，**多步去噪**让渲染损失梯度覆盖全噪声水平以恢复细节，**循环一致性**进一步约束几何一致性，而**更小架构**则证明了方法的高效性——扩散模型的生成能力被成功“蒸馏”到紧凑网络中，同时超越教师。

SplatDiffusion 的核心思想是将扩散训练中的**噪声样本来源**与**监督信号来源**解耦，从而突破标准扩散模型要求两者处于同一模态（通常为3D）的限制。该方法利用一个预训练的确定性3D重建模型作为“噪声教师”（Noisy Teacher），生成带有噪声的3D高斯泼溅（3DGS）样本，而监督信号则来自2D渲染图像，使模型能够在仅依赖2D数据的情况下进行有效的扩散训练。

整个pipeline分为两个阶段，如图2所示：

### 阶段一：噪声教师引导（Noisy Teacher Bootstrapping）

此阶段的目标是为扩散模型提供一个合理的初始化。给定一张源视图图像 $x_{\mathrm{src}}$，首先由预训练的确定性教师模型 $T_\phi$ 预测一个不完美的干净3DGS样本 $s_0^{\mathrm{teacher}}$。随后，通过前向扩散过程在该预测上注入噪声，生成噪声化样本 $s_t$：

$$s_t = \sqrt{\alpha_t} s_0^{\mathrm{teacher}} + \sqrt{1-\alpha_t} \epsilon$$

扩散去噪器 $D_\theta(s_t, t, x_{\mathrm{src}})$ 接收该噪声样本和时间步 $t$，以源图像为条件，预测去噪后的干净3DGS。训练时同时施加两种监督：

- **3DGS损失** $\ell_{3\mathrm{DGS}}$：直接约束去噪器输出与教师干净样本之间的L2距离。
- **图像渲染损失** $\ell_{\mathrm{image}}$：将去噪后的3DGS通过可微渲染器 $\mathcal{R}$ 渲染到目标视角 $v$，与真值图像 $x_{\mathrm{tgt}}^v$ 计算L2损失。

引导阶段的总损失为两者在随机时间步 $t \sim \mathcal{U}[T]$ 上的期望：

$$\mathcal{L}_{\mathrm{bootstrap}} = \mathbb{E}_{x_{\mathrm{src}}, v \sim \mathcal{U}[k], t \sim \mathcal{U}[T], \epsilon} [\ell_{3\mathrm{DGS}} + \ell_{\mathrm{image}}]$$

消融实验表明，若此阶段仅使用渲染损失而舍弃3DGS损失，PSNR会从22.61骤降至18.82，证明3D监督在初始化阶段不可或缺（Table 8）。

### 阶段二：多步去噪微调（Multi-step Denoising Fine-tuning）

阶段二实现了模态解耦的核心机制。关键观察是：在高噪声时间步（$t > t^*$）下，由噪声教师生成的噪声样本分布与真实分布对齐，因此可以作为有效的扩散训练输入。该阶段不再使用教师的干净预测作为3D监督，而是执行**多步去噪**：从 $t > t^*$ 开始，通过DDIM采样器（10步）逐步去噪至 $t=0$，在每一步对最终预测的干净3DGS进行渲染，并与目标视图计算加权L2损失：

$$\mathcal{L}_{\mathrm{mlt-stp}} = \mathbb{E}_{\boldsymbol{x}_{\mathrm{src}}, \boldsymbol{v} \sim \mathcal{U}[k], t > t^*, \epsilon} \left[ \lambda_t \lVert \boldsymbol{x}_{\mathrm{tgt}}^{\boldsymbol{v}} - \mathcal{R}(\hat{s}_0, \boldsymbol{v}) \rVert_2^2 \right]$$

多步去噪的优势在于，渲染损失的梯度可以通过可微渲染器反向传播，跨越多个去噪步骤，最终到达所有噪声水平下的去噪器参数，使模型能够恢复精细细节并超越教师模型。消融证实，阶段二仅使用渲染损失（舍弃扩散损失和教师监督）可将PSNR从23.13提升至24.49，提升约1.3 dB（Table 4 b.3 vs b.4）。

### 循环一致性正则化

为进一步提升重建质量，pipeline中引入了**循环一致性分支**（Cycle Consistency Branch）。具体而言，将阶段二渲染得到的目标视图图像 $\tilde{x}_{\mathrm{tgt}}^v$ 重新送入扩散模型，预测新的3DGS $\tilde{s}_0$，再将其渲染回源视角 $v_{\mathrm{src}}$，与原始源图像计算L2损失：

$$\mathcal{L}_{\mathrm{cyc}} = \| x_{\mathrm{src}} - \mathcal{R}(\tilde{s}_0, v_{\mathrm{src}}) \|_2^2$$

该正则化在两个阶段均带来稳定提升：阶段一PSNR从22.61提升至23.73（+1.1 dB），阶段二从24.69提升至24.91（+0.2 dB）（Table 4 c.1-c.4）。

### 模块关系与数据流

整个框架包含以下核心模块：

| 模块 | 功能 | 所在阶段 |
|------|------|----------|
| 噪声教师 $T_\phi$ | 从源图像生成不完美3DGS预测，提供噪声样本和初始监督 | 阶段一 |
| 扩散去噪器 $D_\theta$ | 基于U-Net的图像条件3D去噪网络，输入噪声3DGS和源图像，预测干净3DGS | 两阶段共用 |
| 可微渲染器 $\mathcal{R}$ | 将3DGS渲染为2D视图，桥接3D去噪与2D监督 | 两阶段共用 |
| 多步去噪循环 | 从 $t>t^*$ 迭代去噪至 $t=0$，累积各步渲染损失 | 阶段二 |
| 循环一致性分支 | 利用渲染图像二次生成3DGS并投影回源视角 | 两阶段共用 |
| 视角引导模块（可选） | 在去噪过程中融入额外视图的通用引导（Universal Guidance） | 推理时 |

数据流从单张源图像出发，经噪声教师生成初始3DGS，再经扩散去噪器迭代精炼，最终通过可微渲染器产生新视图图像。两阶段设计使模型先获得合理初始化，再通过模态解耦的多步去噪超越教师模型的上限。

SplatDiffusion 的训练流水线由五个核心模块构成，按两阶段策略组织：引导阶段（Bootstrapping）利用噪声教师进行初始监督，微调阶段（Fine-tuning）通过多步去噪和渲染损失实现模态解耦的精细化训练。

### 噪声教师（Noisy Teacher）

噪声教师是一个预训练的确定性3DGS预测器 $T_\phi$，用于从单张源图像 $x_{\mathrm{src}}$ 生成不完美的3D高斯泼溅预测 $s_0^{\mathrm{teacher}}$。在物体级实验中，教师为 **Splatter Image**（Szymanowicz et al., CVPR 2024）；在场景级实验中，教师为 **Flash3D**（Szymanowicz et al., arXiv 2024）。教师的核心作用是在缺乏真实3D真值的情况下，为扩散模型提供噪声样本生成的锚点。

噪声样本 $s_t$ 通过标准前向加噪过程从教师预测构建：

$$s_t = \sqrt{\alpha_t} s_0^{\mathrm{teacher}} + \sqrt{1-\alpha_t} \epsilon$$

其中 $\alpha_t$ 为噪声调度参数，$\epsilon \sim \mathcal{N}(0, I)$ 为标准高斯噪声。该公式的关键在于：当 $t > t^*$（临界时间步）时，由教师预测生成的噪声样本分布与从真实未知3D真值加噪得到的分布近似对齐，从而为扩散训练提供了有效的输入信号。

### 扩散去噪器（Denoiser）

扩散去噪器 $D_\theta(s_t, t, x_{\mathrm{src}})$ 采用基于U-Net的图像条件架构，输入为 $N$ 个噪声化的3D高斯泼溅 $s_t \in \mathbb{R}^{N \times d}$（每个高斯包含中心位置、协方差、不透明度和颜色参数）、当前时间步 $t$ 以及源图像 $x_{\mathrm{src}}$，输出为预测的干净3DGS $\hat{s}_0$。值得注意的是，SplatDiffusion 采用 Medium 规模的U-Net（参数量约为 Splatter Image Large 的一半），在更小的模型容量下实现了更优的重建质量。

### 可微渲染器（Renderer）

可微渲染器 $\mathcal{R}(s, v)$ 将3D高斯泼溅 $s$ 从目标视角 $v$ 渲染为2D图像，使模型能够通过图像级损失接收2D监督信号。这是实现“去噪模态（3D）与监督模态（2D）解耦”的关键桥梁。

### 多步去噪循环（Multi-step Denoising Loop）

多步去噪循环是 Stage II 的核心机制，替代了传统的单步去噪训练。其训练损失定义为：

$$\mathcal{L}_{\mathrm{mlt-stp}} = \mathbb{E}_{\boldsymbol{x}_{\mathrm{src}}, \boldsymbol{v} \sim \mathcal{U}[k], t > t^*, \epsilon} \left[ \lambda_t \lVert \boldsymbol{x}_{\mathrm{tgt}}^{\boldsymbol{v}} - \mathcal{R}(\hat{s}_0, \boldsymbol{v}) \rVert_2^2 \right]$$

其中 $\hat{s}_0$ 是从 $t > t^*$ 开始执行多步DDIM去噪后得到的最终干净预测，$\lambda_t$ 为时间步相关的加权系数。该设计的因果机制在于：单步去噪仅在低噪声水平下有效，而多步去噪使渲染损失的梯度能够通过去噪链传播到所有噪声水平，从而恢复精细细节并超越教师模型的性能上限。推理时采用10步DDIM采样器。

### 循环一致性分支（Cycle Consistency Branch）

循环一致性分支利用渲染的目标视图图像再次预测3DGS $\tilde{s}_0$，并将其渲染回源视角 $v_{\mathrm{src}}$ 以提供自监督信号：

$$\mathcal{L}_{\mathrm{cyc}} = \| x_{\mathrm{src}} - \mathcal{R}(\tilde{s}_0, v_{\mathrm{src}}) \|_2^2$$

该正则化在两个训练阶段均带来稳定提升：Stage I 中 PSNR 提升约 +1.1 dB，Stage II 中提升约 +0.2 dB（Table 4, c.1 vs c.2 和 c.3 vs c.4）。

### 引导阶段损失函数

Stage I 的引导训练结合了3D直接监督和2D渲染监督：

$$\ell_{3\mathrm{DGS}} = \Vert s_0^{\mathrm{teacher}} - D_{\theta}(s_t, t, x_{\mathrm{src}}) \Vert^2$$

$$\ell_{\mathrm{image}} = \| x_{\mathrm{tgt}}^{v} - \mathcal{R}(D_{\theta}(s_t, t, x_{\mathrm{src}}), v) \|_2^2$$

$$\mathcal{L}_{\mathrm{bootstrap}} = \mathbb{E}_{x_{\mathrm{src}}, v \sim \mathcal{U}[k], t \sim \mathcal{U}[T], \epsilon} [\ell_{3\mathrm{DGS}} + \ell_{\mathrm{image}}]$$

消融实验表明，若引导阶段仅使用渲染损失（无3D扩散损失），PSNR 从 22.61 骤降至 18.82，证明3D监督在初始化阶段的必要性。

### 视角引导模块（View Guidance）

作为可选模块，SplatDiffusion 可在去噪过程中融入额外视图的通用引导（Universal Guidance）。其机制是通过噪声估计反向修正DDIM采样步进：

$$\epsilon_t = \frac{s_t - \sqrt{\alpha_t} \hat{s}_0}{\sqrt{1 - \alpha_t}}$$

$$s_{t-1} = \sqrt{\alpha_{t-1}} \hat{s}_0 + \sqrt{1 - \alpha_{t-1}} \cdot \hat{\epsilon}_t$$

其中 $\hat{\epsilon}_t$ 为结合额外视图引导梯度修正后的噪声估计。实验表明，基于扩散的引导策略优于传统的逐样本3DGS优化方法（Table 5）。

## 实验与关键发现

### 核心实验设置

SplatDiffusion 在两个代表性基准上验证：**ShapeNet-SRN**（物体级单视图重建，Cars/Chairs 类别）和 **RealEstate10K**（场景级新视图合成）。训练分两阶段——Stage I 引导阶段使用 batch size 100/GPU，Stage II 多步去噪微调因显存限制降至 10/GPU；推理采用 DDIM 采样器 10 步。关键对比基线包括确定性教师模型 **Splatter Image**（Szymanowicz et al., CVPR 2024，物体级）和 **Flash3D**（Szymanowicz et al., arXiv 2024，场景级），以及 **PixelNeRF**（Yu et al., CVPR 2021）、**Viewset Diffusion**（Szymanowicz et al., CVPR 2023）等。

### 主结果

**物体级单视图重建。** 在 ShapeNet-SRN Cars 上，SplatDiffusion（Medium U-Net）以 PSNR 24.84 / SSIM 0.93 / LPIPS 0.077 显著超越其教师模型 Splatter Image（Large）的 24.00 / 0.92 / 0.078（Table 1），PSNR 提升 0.84 dB。Chairs 类别同样取得 PSNR 25.21，比教师提高 0.78 dB。值得注意的是，SplatDiffusion 使用参数量更小的 Medium U-Net（约 Splatter Image Large 的一半，Table 3），证明增益来自扩散框架本身而非模型容量——同规模的确定性前馈模型（Feedforward Medium）PSNR 仅 19.99（Table 7），远低于扩散变体。

**场景级新视图合成。** 在 RealEstate10K 上，SplatDiffusion 在三种基线范围设置下均优于 Flash3D：5 帧（PSNR 29.12 vs 28.46）、10 帧（26.54 vs 25.94）、U[-30,30] 帧（25.40 vs 24.93），平均 PSNR 提升约 0.5 dB（Table 2）。LPIPS 改善尤为明显，在大基线范围下从 0.160 降至 0.135（-0.025），表明扩散模型有效缓解了确定性方法的过平滑问题。

**跨数据集泛化。** 在 Co3D hydrant 上，SplatDiffusion 以 PSNR 22.34 超过 Splatter Image 的 21.77（+0.57 dB，Table 6），验证了方法对域外数据的迁移能力。

### 消融实验核心发现

Table 4 系统剖析了各组件贡献（ShapeNet-SRN Cars 验证集）：

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_00623/figures/006_Table_4.jpg]]
*Table 4: Ablations Studies on Single view Reconstruction, evaluated on the validation set of ShapeNet-SRN Cars. In (b) and (c) rows, we use Splatter Image (Large) as a teacher to train our diffusion model (Medium)*

**两阶段训练的必要性。** Stage I 若仅使用渲染损失（无 3D 扩散损失）导致 PSNR 骤降至 18.82（Table 8：R only in stage 1），证明引导阶段的 3D 监督对初始化扩散模型至关重要。Stage II 中，纯渲染损失微调（b.4）达到 PSNR 24.49，显著优于保留扩散损失（b.3，PSNR 23.13）或继续使用教师监督（b.2，PSNR 22.61），说明多步去噪框架下图像级梯度比 3D 真值或教师预测更有效。

**循环一致性正则化。** 该损失在两个阶段均带来稳定提升：Stage I 中 PSNR 从 22.61 升至 23.73（+1.12 dB），Stage II 中从 24.69 升至 24.91（+0.22 dB，Table 4 c.1→c.2 和 c.3→c.4）。其机制在于利用渲染的目标图像再次生成 3DGS 并投影回源视角，形成自监督闭环，有效约束了几何一致性。

**时间步加权策略。** 对不同去噪时间步赋予加权损失（而非均匀加权）将 Stage II PSNR 从 22.88 提升至 24.49（Table 9），表明高噪声阶段需要更强的监督信号来引导分布对齐。

**双视图引导。** 在去噪过程中融入额外视图的通用引导（Universal Guidance），SplatDiffusion 优于对教师输出进行逐样本 3DGS 优化的方式（Table 5），证明扩散先验比后处理优化能更有效地利用多视图信息。

### 失败模式与局限性

1. **教师质量依赖。** 整个训练流程以预训练确定性模型为起点，教师预测中的系统性偏差会通过噪声样本传播至扩散模型。Table 1 中 Chairs 的 SSIM 未提升（均为 0.93）可能反映教师在该类别上已接近性能上限。
2. **遮挡区域过平滑。** 定性结果（Figure 3）显示，在严重遮挡区域高斯分布趋于不均匀，导致新视图中出现模糊伪影。这是 2D 监督的固有局限——遮挡区域缺乏直接的图像梯度。
3. **计算开销。** Stage II 多步去噪需将 batch size 从 100 降至 10（受限于显存），训练效率显著低于 Stage I。临界时间步 t* 的选择目前依赖经验调参，缺乏自动化机制。
4. **表示范围未验证。** 当前仅验证于 3D Gaussian Splatting，对其他 3D 表示（NeRF、SDF）的适用性仍是开放问题。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_00623/figures/008_Figure.jpg]]

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_00623/figures/009_Figure.jpg]]

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_00623/figures/012_Figure.jpg]]

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_00623/figures/003_Table_1.jpg]]
*Table 1: ShapeNet-SRN: Single-View Reconstruction (test split). Our method achieves better quality on all metrics on the Car split and Chair dataset, while performing reconstruction in the 3D space*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_00623/figures/017_Table_6.jpg]]
*Table 6: Comparison on Co3D hydrant dataset*

## 定位与知识库关联

### 1. 方法谱系

SplatDiffusion 的核心贡献在于将扩散模型的训练监督模态从 3D 真值解耦为 2D 图像，从而突破了高质量 3D 数据集稀缺对扩散模型训练的制约。该方法处于以下几条研究脉络的交汇点：

- **确定性前馈 3D 重建**：SplatDiffusion 直接依赖预训练的确定性模型作为“噪声教师”，在物体级实验中采用 **Splatter Image**（Szymanowicz et al., CVPR 2024），在场景级实验中采用 **Flash3D**（Szymanowicz et al., arXiv 2024）。这些教师模型为扩散训练提供噪声样本和初始监督，但自身仅能产生确定性的模糊平均结果。SplatDiffusion 的增益恰来自扩散框架对多解性的建模能力——消融实验表明，使用与教师同等规模的确定性前馈模型（Feedforward Medium）PSNR 仅为 19.99，远低于 SplatDiffusion 的 24.84（Table 7），证明性能提升源自扩散范式而非模型容量。

- **2D 监督下的 3D 生成**：**Viewset Diffusion**（Szymanowicz et al., CVPR 2023）探索了从多视图图像条件生成 3D 的扩散方法，但其输入和输出均作用于图像域。SplatDiffusion 将这一思路推进到 3D 表示空间——噪声样本保持为 3D 高斯泼溅（3DGS），监督信号则来自 2D 渲染图像，实现了模态解耦。

- **单视图 3D 扩散重建**：**NeRFDiff** 和 **VisionNeRF** 等工作在 NeRF 表示上探索了扩散式单视图重建，但受限于 3D 监督需求或 NeRF 的渲染效率。SplatDiffusion 在 3DGS 表示上构建扩散模型，在计算效率上具有优势——Table 3 显示其模型体积和 GPU 显存占用显著低于 VisionNeRF 和 PixelNeRF（Yu et al., CVPR 2021）。

- **扩散模型的引导机制**：SplatDiffusion 在去噪过程中可选地融入额外视图的通用引导（Universal Guidance），与 3DGS 逐样本优化方法相比，扩散引导能更有效地利用额外视图信息（Table 5）。

### 2. 适用边界

- **表示依赖性**：当前方法完全基于 3D 高斯泼溅表示构建，尚未验证在其他 3D 表示（如 NeRF、Signed Distance Field）上的可迁移性。3DGS 的显式点云结构使噪声化操作（前向扩散）和可微渲染天然兼容，但隐式表示可能需要不同的噪声策略。

- **教师依赖性**：方法性能受限于预训练教师模型的质量。噪声教师必须能够从单视图产生“大致合理”的 3D 预测，否则高噪声时间步下的噪声样本分布无法与真实分布对齐，导致引导阶段失效。

- **计算开销**：多步去噪训练（Stage II）需要执行完整的 DDIM 采样链（10 步），显存占用显著增加，batch size 被迫从 100 降至 10。这限制了在更大规模数据集上的训练效率。

- **遮挡场景**：在严重遮挡区域，3DGS 可能出现高斯分布不均匀，导致新视图中产生过平滑伪影。当前方法未引入显式的遮挡处理机制。

### 3. 局限与开放问题

**已识别的局限**：

1. 临界时间步 $t^*$ 的选择目前依赖经验调参，不同教师模型和数据集可能需要不同的 $t^*$ 值。$t^*$ 过小会导致低噪声时间步的噪声样本分布偏差，过大会损失可利用的训练信号。
2. 循环一致性分支（Cycle Consistency）在 Stage II 仅带来约 0.2 dB 的增益（Table 4, c.3 vs c.4），其边际效益随训练推进递减，暗示当前的循环设计可能尚未充分挖掘自监督潜力。
3. 双视图引导虽然有效，但扩展到任意多视图的引导机制尚未建立——当前公式依赖于对每个引导视图独立计算损失梯度并聚合。

**开放问题**：

- 如何自动确定最优临界时间步 $t^*$？是否可能通过分析教师预测的误差分布与扩散噪声调度之间的关系来推导自适应阈值？
- 多步去噪策略能否推广到 NeRF 或 signed distance field 等其他 3D 表示？关键挑战在于隐式表示缺乏类似 3DGS 的显式参数化，噪声注入和可微渲染的耦合方式需要重新设计。
- 循环一致性分支是否可能反向改善教师模型自身？当前设计仅将循环信号用于扩散模型训练，若将循环反馈回教师模型可能形成协同增强的闭环。
- 在动态场景、非朗伯表面等更复杂的真实环境中，噪声教师的预测质量可能急剧下降，该方法是否仍能保持对教师的超越？这需要在更具挑战性的基准上进行验证。

## 原文 PDF

![[paperPDFs/ICCV_2025/A_Lesson_in_Splats_Teacher_Guided_Diffusion_for_3D_Gaussian_Splats_Generation_with_2D_Supervision.pdf]]
