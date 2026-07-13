---
title: "LaMD: Latent Motion Diffusion for Image-Conditional Video Generation"
type: paper
paper_level: A
venue: arXiv
year: 2023
pdf_ref: paperPDFs/arxiv_2023/LaMD_Latent_Motion_Diffusion_for_Image_Conditional_Video_Generation.pdf
project_link: null
code_link: null
aliases:
- LLMD
- LaMD
tags:
- arxiv_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 运动潜变量的压缩程度与运动-内容分离的强度（通过KL惩罚系数β和潜在运动通道数d控制），以及是否去除时间维度以使用2D扩散模型。
primary_logic: 将视频生成重构为潜在运动生成与视频重建，通过高度压缩的二维运动表示和2D扩散模型，大幅降低生成模型的复杂度，同时保持运动的表现力。
claims:
- LaMD在五个基准数据集（BAIR, Landscape, NATOPS, MUG, CATER-GEN）上均生成高质量视频，FVD等指标优于先前最优方法。
- 去除潜在运动的时间维度不会损害重建性能，并能支持2D-UNet扩散模型，显著提升采样速度，达到与图像扩散模型相当的水平。
- 通过调节KL惩罚系数和潜变量通道数，可在运动分离与重建质量之间取得平衡，较小的潜空间更有利于生成性能。
- BAIR Robot Pushing 上 FVD = 57.0
---

# LaMD: Latent Motion Diffusion for Image-Conditional Video Generation

> [!tip] 核心洞察
> 将视频生成重构为潜在运动生成与视频重建，通过高度压缩的二维运动表示和2D扩散模型，大幅降低生成模型的复杂度，同时保持运动的表现力。

| 字段 | 内容 |
|------|------|
| 中文题名 | LaMD：用于图像条件视频生成的潜在运动扩散 |
| 英文题名 | LaMD: Latent Motion Diffusion for Image-Conditional Video Generation |
| 会议/期刊 | arXiv 2023 |
| Links | [paper](https://arxiv.org/abs/2304.11603) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | LaMD (Latent Motion Diffusion) |
| Dataset | BAIR Robot Pushing, Landscape, CATER-GEN-v2, BAIR |

> [!tip] 效果简介
> - BAIR Robot Pushing 上，FVD 57.0 vs LFDM (先前最优) (显著降低)。
> - Landscape 上，FVD 100.7 vs cINN (先前最优) (显著降低)。
> - CATER-GEN-v2 上，FVD 5.77 vs LFDM (显著降低)。

## 概要

视频生成的核心瓶颈在于**运动连贯性与生成效率的协同优化**。现有方法要么在像素空间或潜在视频空间中进行高维扩散，导致采样缓慢；要么难以在保持内容一致性的同时生成自然、多样化的运动。LaMD（Latent Motion Diffusion）通过将视频生成重构为**潜在运动生成**与**视频重建**两个解耦阶段，从根本上降低了生成模型的复杂度。

其核心洞察在于：视频中的运动信息可以被高度压缩为一个**去除时间维度的二维潜在表示**，从而支持使用2D-UNet扩散模型进行高效生成，同时通过信息瓶颈机制强制实现运动与内容的分离。这一设计使LaMD在五个基准数据集（BAIR、Landscape、NATOPS、MUG、CATER-GEN）上均取得了领先的FVD指标，并在128帧、128×128分辨率下实现每视频约10.7秒的采样速度，相比传统视频扩散模型实现了数量级的加速。

在方法谱系上，LaMD区别于基于3D-UNet的潜在视频扩散模型（如**LFDM**，Ni et al., CVPR 2023）和基于条件可逆网络的**cINN**（Dorkenwald et al., CVPR 2021），开创性地将扩散目标从视频空间迁移至一个低维的、空间化的运动表示空间。其采样效率与图像级潜在扩散模型**LDM**（Rombach et al., CVPR 2022）相当，但专门针对视频生成任务进行了运动-内容分解设计。

视频生成的核心瓶颈在于**运动的连贯性与生成效率之间的矛盾**。现有方法在追求自然运动的同时，往往面临采样速度慢、训练开销大的困境，尤其在高维视频数据上，这一问题更为突出。像素空间扩散模型直接在视频帧上建模，计算成本极高；潜在视频扩散模型虽将生成目标压缩至低维空间，但仍需处理包含时间维度的3D表示，限制了扩散模型的架构选择与采样效率。

**现有方法的缺口**主要体现在三个方面。第一，运动与内容耦合紧密。多数方法将外观与运动联合编码或生成，缺乏显式的分离机制，导致生成的运动难以独立控制，且容易引入外观伪影。第二，潜在空间维度冗余。典型的潜在视频表示保留时间维度，迫使扩散模型使用3D-UNet或3D卷积网络，采样步骤数多、单步计算量大，难以达到与图像扩散模型相当的推理速度。第三，训练效率受限。在高维视频数据上训练3D扩散模型需要大量GPU资源，限制了模型的规模化与实用化。

**本文的动机**源于一个关键洞察：运动信息本身具有高度的可压缩性，可以被表示为低维的二维表示，而不损害其表达能力。基于此，LaMD提出将视频生成重构为**潜在运动生成与视频重建**两个阶段——通过运动-内容分解视频自编码器（MCD-VAE）将运动压缩为去除时间维度的2D潜在表示，再使用2D-UNet扩散模型在该低维空间中进行高效生成。这一范式转换有望同时解决运动质量、生成效率与训练成本三个核心挑战。

## 核心方法与创新机理

LaMD 的核心创新在于将视频生成问题重构为**潜在运动生成**与**视频重建**两个解耦的子任务，通过三个关键设计实现了运动连贯性与生成效率的同步突破。

### 1. 运动-内容分离的潜在空间

传统视频生成方法（如 **LFDM** (Ni et al., CVPR 2023)、**cINN** (Dorkenwald et al., CVPR 2021)）在像素空间或联合潜在视频空间中进行生成，运动与外观信息高度耦合。LaMD 引入**信息瓶颈**机制，通过 KL 惩罚约束（系数 β）强制运动编码器只保留运动相关信息，将内容信息交由独立的图像编码器提取。这种分离使得生成模型只需建模低维运动分布，而非完整视频分布，从根本上降低了生成难度。

### 2. 去除时间维度的二维运动表示

与现有方法使用 3D 潜在表示不同，LaMD 将运动编码器的时序下采样率设置为视频帧数（$r_t = L$），彻底消除潜在运动的时间维度，将运动压缩为二维平面表示。这一设计带来了双重收益：
- **架构简化**：扩散模型从 3D-UNet 降级为 2D-UNet，配合交叉注意力机制注入条件信息；
- **采样加速**：在 128 帧 128×128 分辨率下，单视频采样仅需 **10.7 秒**，达到与图像扩散模型 **LDM** (Rombach et al., CVPR 2022) 相当的水平，相比视频空间扩散模型实现数量级加速（Table 11, Fig. 4）。

消融实验（Table 12）证实，去除时间维度不会损害重建质量，反而因模型简化提升了生成性能。

### 3. 高度压缩的运动潜空间

LaMD 将运动信息压缩至极低维度的潜空间（通道数 $d=3$，空间下采样 $r_s=4$）。消融实验（Table 13）表明，较小的潜在空间（$d=3$, $\beta=10^{-2}$）在生成性能（Landscape FVD 100.7）上显著优于较大空间（$d=4$, $\beta=10^{-5}$ 时 FVD 127.1），尽管后者重建质量略高。$d=3$ 在运动表达能力与生成难度之间取得了最优平衡，成为最终配置。

### 范式对比

| 生成空间 | 像素/潜在视频空间 | **潜在运动空间** |
| 运动与内容 | 联合编码或生成 | **信息瓶颈分离** |
| 运动维度 | 含时间维度的 3D 表示 | **去除时间维度的 2D 表示** |
| 扩散架构 | 3D-UNet / 3D 卷积 | **2D-UNet + 交叉注意力** |

这一范式转换（Fig. 1）使 LaMD 在五个基准数据集（BAIR、Landscape、NATOPS、MUG、CATER-GEN）上均取得最优 FVD 指标，同时保持高运动平滑度（Landscape 99.47%，Table 5），验证了“先压缩运动、再生成运动”策略的有效性。

LaMD 采用**两阶段训练范式**，将视频生成重构为“潜在运动生成 + 视频重建”两个解耦的子问题。框架由两个核心模块串联构成：**运动-内容分解视频自编码器（MCD-VAE）** 与 **扩散运动生成器（DMG）**。

### 阶段一：MCD-VAE 的运动-内容分解与重建

第一阶段在纯视频数据上以自监督方式训练 MCD-VAE，目标是学习一个高度压缩的潜在运动表示 $\mathbf{z}_m$，同时保留完整的视频重建能力。MCD-VAE 包含三个子模块：

- **图像编码器 $E_I$**：从给定首帧 $x_0$ 提取多尺度内容特征 $f_{x_0}$，为后续所有帧的重建提供外观约束。
- **运动编码器 $E_M$**：基于轻量 3D-UNet 架构，以空间下采样因子 $r_s=4$ 和时间下采样因子 $r_t = L$（$L$ 为输入视频帧数）处理整个视频序列 $x_{0:L}$。关键设计在于 $r_t = L$，使得时间维度被完全消除，输出压缩为**二维平面表示**。在此之上施加信息瓶颈——通过重参数化技巧对运动编码器输出施加高斯分布约束（KL 惩罚系数 $\beta$），迫使 $\mathbf{z}_m$ 仅保留与运动相关的信息，实现运动与内容的分离。
- **融合解码器 $D_V$**：接收内容特征 $f_{x_0}$ 与潜在运动 $\mathbf{z}_m$，通过融合模块逐帧重建完整视频 $\hat{x}_{0:L}$。

MCD-VAE 的训练损失综合了像素级 L1 损失、感知相似度 LPIPS、KL 散度（约束潜在运动分布接近标准正态）以及对抗损失，在运动分离与重建质量之间取得平衡。

### 阶段二：扩散运动生成器的潜在运动生成

第二阶段固定 MCD-VAE 参数，在归一化的连续潜在运动空间上训练 DMG。DMG 采用**2D-UNet 配合交叉注意力**的架构，以内容特征 $f_{x_0}$ 和可选条件（文本/类别）$c$ 为条件，通过标准扩散过程学习运动分布 $p(\mathbf{z}_m)$。前向过程逐步向 $\mathbf{z}_m$ 添加高斯噪声，反向过程则由可学习去噪网络 $\epsilon_\theta$ 预测噪声，逐步恢复自然运动。

### 推理流程

推理时，DMG 从随机噪声出发，经 $T$ 步去噪生成潜在运动 $\mathbf{z}_m$，随后将其与给定首帧的内容特征 $f_{x_0}$ 一同送入 $D_V$，合成完整视频序列。由于扩散目标为低维二维表示且生成器为 2D-UNet，采样速度显著优于像素空间或潜在视频空间的扩散模型。

### 关键设计决策

| 设计维度 | 传统做法 | LaMD 方案 |
|---------|---------|----------|
| 生成空间 | 像素空间或潜在视频空间 | 潜在运动空间 |
| 运动与内容 | 联合编码或生成 | 通过信息瓶颈分离，独立压缩运动 |
| 潜在运动维度 | 含时间维度的 3D 表示 | 去除时间维度，压缩为 2D 表示 |
| 扩散模型架构 | 3D-UNet 或 3D 卷积 | 2D-UNet + 交叉注意力 |

这种将视频生成降维为“2D 运动生成 + 条件重建”的策略，是 LaMD 在生成效率与运动质量上取得突破的核心机制。

![[assets/figures/papers/paper_list_l1049_https_arxiv_org_abs_2304_11603/figures/002_Figure_2.jpg]]
*Figure 2: The framework of our proposed LaMD. During training process, the stage-I MCD-VAE is first trained to decompose latent motion with video reconstruction task, while DMG is trained to generate natural motion conditioned by*

![[assets/figures/papers/paper_list_l1049_https_arxiv_org_abs_2304_11603/figures/001_Figure_1.jpg]]
*Figure 1: The comparison of video generation in different latent space. The dashed line stands for operations only involved in training process, while the solid line represents operations both involved in training and sampling process*

LaMD 框架由两个阶段构成：第一阶段训练 **运动-内容分解视频自编码器（MCD-VAE）**，第二阶段在冻结的 MCD-VAE 潜在运动空间上训练 **扩散运动生成器（DMG）**。核心设计理念是将视频生成重构为“潜在运动生成 + 视频重建”，通过高度压缩的二维运动表示和信息瓶颈实现运动与内容的分离。

### 3.1 运动-内容分解视频自编码器（MCD-VAE）

MCD-VAE 由三个关键模块组成：**图像编码器** $E_I$、**运动编码器** $E_M$ 和**融合解码器** $D_V$。

**图像编码器 $E_I$** 从给定的第一帧 $x_0$ 提取多尺度内容特征 $f_{x_0}$，用于约束生成视频的外观一致性。

**运动编码器 $E_M$** 基于轻量级 3D-UNet 架构，对输入视频 $x_{0:L}$ 进行空间和时间下采样，提取潜在运动表示。空间下采样因子 $r_s = 4$，时间下采样因子 $r_t$ 设置为与输入视频帧数相等（即 $r_t = L$），从而**完全消除时间维度**，将运动信息压缩为二维平面表示。这一设计使得后续扩散模型可以使用 2D-UNet 而非 3D-UNet，大幅降低计算复杂度。

**信息瓶颈与运动-内容分离**：为实现运动与内容的有效解耦，运动编码器输出高斯分布的均值 $\mu_\theta$ 和方差 $\sigma_\theta$，通过重参数化技巧采样潜在运动 $z_m$：

$$ \mathbf{z}_m = \mu_\theta(\mathcal{E}_M(x_{0:L})) + \varepsilon \cdot \sigma_\theta(\mathcal{E}_M(x_{0:L})) \tag{1} $$

其中 $\varepsilon \sim \mathcal{N}(0, I)$。在训练中施加 KL 散度惩罚项 $\beta \cdot \text{KL}(q \| \mathcal{N}(0, I))$，通过调节超参数 $\beta$ 控制运动分支的信息容量，迫使运动编码器仅保留运动相关信息而排除外观内容。

**融合解码器 $D_V$** 接收多尺度内容特征 $f_{x_0}$ 和潜在运动 $z_m$，通过空间自适应融合机制重建完整视频帧 $\hat{x}_{0:L}$。其架构采用多级特征注入，将内容特征在不同分辨率层级与运动特征融合，确保重建视频在保持第一帧外观的同时展现自然运动。

**训练总损失**结合了像素级重建、感知相似度、KL 正则化和对抗训练：

$$ \mathcal{L}_{\text{GEN}} + \lambda \mathcal{L}_{\text{GAN}} \tag{2} $$

$$ \mathcal{L}_{\text{GAN}} = \log \mathcal{D}(x_{0:L}) + \log(1 - \mathcal{D}(\hat{x}_{0:L})) $$

$$ \mathcal{L}_{\text{GEN}} = \|x_{0:L} - \hat{x}_{0:L}\|_1 + \text{LPIPS}(x_{0:L}, \hat{x}_{0:L}) + \beta \cdot \text{KL}(q \| \mathcal{N}(0, I)) $$

其中 $\mathcal{L}_{\text{GEN}}$ 包含三项：L1 损失保证像素级重建精度，LPIPS 感知损失提升视觉质量，KL 散度项（权重 $\beta$）约束运动潜变量的分布接近标准正态分布。$\mathcal{L}_{\text{GAN}}$ 为对抗损失，通过判别器 $\mathcal{D}$ 进一步提升生成帧的真实性，$\lambda$ 为自适应权重。

### 3.2 扩散运动生成器（DMG）

在 MCD-VAE 训练完成后，其参数被冻结。DMG 在归一化的潜在运动空间上学习运动分布 $p(z_m)$，条件为内容特征 $f_{x_0}$ 和可选的类别/文本条件 $c$。

**前向扩散过程**向真实运动 $z_m^0$ 逐步添加高斯噪声，共 $T$ 步。单步转移为：

$$ q(z_m^t \mid z_m^{t-1}) = \mathcal{N}(z_m^t; \sqrt{1-\beta_t} z_m^{t-1}, \beta_t I) \tag{3} $$

其中 $\beta_t$ 为噪声调度参数。任意时刻 $t$ 的加噪样本可直接从 $z_m^0$ 采样：

$$ q(z_m^t \mid z_m^0) = \mathcal{N}(z_m^t; \sqrt{\bar{\alpha}_t} z_m^0, (1-\bar{\alpha}_t) I) \tag{4} $$

其中 $\bar{\alpha}_t = \prod_{s=1}^t (1-\beta_s)$。

**反向去噪过程**学习从纯噪声 $z_m^T \sim \mathcal{N}(0, I)$ 逐步恢复原始运动，条件为 $y = \{f_{x_0}, c\}$。反向转移由可学习的去噪函数 $\epsilon_\theta$ 参数化：

$$ p_\theta(z_m^{t-1} \mid z_m^t, y) = \mathcal{N}(z_m^{t-1}; \mu_\theta(z_m^t, t, y), \sigma_t^2 I) \tag{5} $$

$$ \mu_\theta = \frac{1}{\sqrt{\alpha_t}} \left( z_m^t - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon_\theta(z_m^t, t, y) \right) $$

其中 $\alpha_t = 1 - \beta_t$。去噪函数 $\epsilon_\theta$ 采用 **2D-UNet 配合交叉注意力机制**实现，内容特征 $f_{x_0}$ 和条件 $c$ 通过交叉注意力层注入。训练目标为简化的均方误差损失：

$$ \mathcal{L}_{\text{simple}}(\theta) = \| \epsilon - \epsilon_\theta(z_m^t, t, y) \|_2^2 \tag{6} $$

其中 $\epsilon$ 为真实添加的噪声。这一简化目标直接预测噪声而非完整的分布参数，在实践中训练更稳定且收敛更快。

**关键设计优势**：由于潜在运动 $z_m$ 已去除时间维度且空间分辨率仅为原视频的 $1/r_s$（即 $1/4$），扩散目标维度极低。配合 2D-UNet 架构，DMG 的采样速度达到与图像扩散模型 **LDM**（Rombach et al., CVPR 2022）相当的水平，相比像素空间或潜在视频空间的 3D 扩散模型实现数量级加速（Table 11, Fig. 4）。

## 实验与关键发现

### 核心实验设置

LaMD在五个封闭域基准数据集上进行评估：**BAIR Robot Pushing**（40k训练/256测试，16帧，64×64）、**Landscape**（35,392训练/2,815测试，32帧，128×128）、**NATOPS**、**MUG**和**CATER-GEN-v2**。实验分为两个阶段：第一阶段训练运动-内容分解视频自编码器（MCD-VAE），第二阶段固定MCD-VAE参数，在潜在运动空间训练扩散运动生成器（DMG）。MCD-VAE的空间下采样因子$r_s=4$，时间下采样因子$r_t$等于输入视频帧长（16或32），从而将时间维度完全压缩消除。所有模型在6块NVIDIA RTX 3090 GPU上训练，采样速度在单块RTX 3090上测量。详细超参数见**Table 1**和**Table 2**。

### 主结果：与SOTA的定量比较

LaMD在五个基准数据集上均取得最优或高度竞争力的FVD（Fréchet Video Distance）分数，验证了潜在运动扩散范式的有效性。

**BAIR Robot Pushing**（Table 6）：LaMD的FVD达到**57.0**，显著优于先前最优方法**LFDM**（Ni et al., CVPR 2023）。该数据集以随机机械臂推动物体为特点，要求模型捕捉高度不确定的运动模式。LaMD在运动质量（Motion Smoothness）和时间一致性（Temporal Consistency）上同样表现突出，表明压缩的潜在运动空间并未损害运动表现力。

**Landscape**（Table 7）：在包含复杂自然场景运动（如水流、云动）的Landscape数据集上，LaMD的FVD为**100.7**，大幅领先此前最优的**cINN**（Dorkenwald et al., CVPR 2021）。值得注意的是，cINN直接对像素空间建模，而LaMD通过运动-内容分离将生成复杂度压缩至二维潜在空间，在保持重建质量的同时获得更好的生成性能。

**MUG与NATOPS**（Table 8, 9）：在面部表情（MUG）和手势动作（NATOPS）数据集上，LaMD同样取得领先的FVD分数。MUG数据集上，LaMD在128×128和256×256两种分辨率下均优于对比方法，证明运动压缩策略对不同空间分辨率具有鲁棒性。

**CATER-GEN-v2**（Table 10）：该数据集要求根据给定图像和文本描述生成物体运动轨迹。LaMD的FVD低至**5.77**，显著优于LFDM，展示了在条件控制下的精确运动生成能力。可视化结果（Fig. 8）显示，给定“圆锥体拾起并包含金色飞贼”的描述，LaMD生成的视频中物体运动轨迹与文本条件高度一致。

### 重建质量分析

MCD-VAE的重建性能是生成质量的上限保证。**Table 3**展示了MCD-VAE在五个数据集上的重建指标（PSNR、SSIM、LPIPS），所有数据集均获得高质量重建。在BAIR数据集上与VQGAN的对比中（Table 4），MCD-VAE的FVD为**36.05**，相比VQGAN的42.80降低15.8%，证明连续潜在运动表示相比离散量化方法能更好地保留运动信息。

![[assets/figures/papers/paper_list_l1049_https_arxiv_org_abs_2304_11603/figures/008_Table_4.jpg]]
*Table 4: The comparison of reconstruction performance on BAIR dataset*

Landscape数据集上的运动质量评估（Table 5）进一步验证了分解的有效性：LaMD的Motion Smoothness达到**99.47%**，Temporal Consistency指标也优于对比方法。运动转移实验（Fig. 6）提供了定性证据——将一段视频的运动潜变量与另一段视频的内容特征结合，生成的视频保留了源视频的运动模式但外观完全匹配目标图像，证实运动与内容实现了有效分离。

### 消融研究

**时间维度消除的影响**（Table 12）：LaMD的核心设计选择之一是将潜在运动的时间维度完全压缩（$r_t = L$）。消融实验表明，去除时间维度（2D潜在运动）与保留时间维度（3D潜在运动）相比，重建性能几乎无差异，但2D表示使得扩散模型可采用2D-UNet架构，显著降低计算开销。这一发现验证了“运动信息可以高度压缩至空间维度而不损失表达能力”的关键假设。

**潜在空间大小与生成的权衡**（Table 13）：通过调节潜在运动通道数$d$和KL惩罚系数$\beta$，可以控制运动-内容分离的强度。实验对比了两种配置：
- 小潜在空间（$d=3$，$\beta=1e-2$）：FVD为**100.7**，重建质量略低但生成性能更优
- 大潜在空间（$d=4$，$\beta=1e-5$）：FVD为127.1，重建质量更高但生成性能下降

结果表明，较小的潜在空间虽然轻微牺牲重建精度，但通过更强的信息瓶颈约束，迫使运动编码器学习更紧凑、更规整的表示，从而降低了扩散模型的建模难度。通道数$d=3$在运动表达能力与生成难度之间取得了最佳平衡。

### 采样效率

LaMD的采样效率优势源于两个设计：低维扩散目标（仅$d \times H/r_s \times W/r_s$的2D张量）和2D-UNet架构。**Table 11**和**Fig. 4**的对比显示，在128帧、128×128分辨率下，LaMD每视频采样仅需**10.7秒**（200步DDIM），而像素空间扩散模型和潜在视频扩散模型需要数量级更长的时间。LaMD的采样速度与图像扩散模型**LDM**（Rombach et al., CVPR 2022）处于同一水平，因其扩散目标的空间尺寸与单帧图像潜在表示相当。

![[assets/figures/papers/paper_list_l1049_https_arxiv_org_abs_2304_11603/figures/022_Table_11.jpg]]
*Table 11: The comparison of sampling time per video. All diffusion models use 200 sampling steps and are tested on a single NVIDIA GeForce RTX 3090 GPU*

### 失败模式与局限性

1. **内容变化场景的退化**：运动分解假设视频内容（外观）主要由第一帧决定，后续帧的变化归因于运动。当视频中出现新物体或场景内容显著变化时（如物体移入画面），潜在运动可能被迫编码不属于运动的外观信息，导致运动-内容分离失效。当前仅在封闭域数据集验证，开放域复杂场景的泛化能力有待检验。

2. **长视频生成未验证**：实验仅覆盖16帧和32帧的短视频，对于更长时序的建模，高度压缩的潜在运动是否足以承载长程运动依赖尚未探索。

3. **文本到视频生成的间接性**：LaMD目前仅支持图像条件视频生成，无法直接进行文本到视频生成，需要额外集成图像生成模型作为前端，增加了系统复杂度。

4. **训练数据规模受限**：MCD-VAE仅在目标数据集上训练，未利用大规模外部视频数据。若结合预训练策略，MCD-VAE的表达能力和泛化性可能进一步提升，这一潜力尚未被挖掘。

### 关键图表结论汇总

| 图表 | 核心结论 |
|------|----------|
| Table 6, 7, 8, 9, 10 | LaMD在五个数据集上FVD均优于先前SOTA，验证潜在运动扩散范式的有效性 |
| Table 4 | MCD-VAE连续潜在表示相比VQGAN离散量化重建FVD降低15.8% |
| Table 12 | 消除时间维度不损害重建质量，但使2D-UNet扩散成为可能 |
| Table 13 | 较小潜在空间（$d=3$，$\beta=1e-2$）生成FVD更优（100.7 vs 127.1） |
| Table 11, Fig. 4 | 采样速度达10.7秒/视频，与图像扩散模型相当 |
| Fig. 6 | 运动转移实验定性验证运动-内容有效分离 |

![[assets/figures/papers/paper_list_l1049_https_arxiv_org_abs_2304_11603/figures/014_Table_6.jpg]]
*Table 6: Quantitative evaluation compared to the state-of-the-art on the BAIR dataset*

![[assets/figures/papers/paper_list_l1049_https_arxiv_org_abs_2304_11603/figures/024_Table_12.jpg]]
*Table 12: Ablation study of motion capacity in MCD-VAE on the BAIR dataset*

## 定位与知识库关联

### 1. 范式定位：从像素/视频生成到潜在运动生成

LaMD 将视频生成重新定义为**潜在运动生成**问题，其核心范式转移在于将生成目标从高维像素空间或潜在视频空间压缩至一个低维、去除时间轴的运动表示。Fig. 1 清晰地对比了三种生成范式：

- **像素空间生成**：扩散模型直接在原始视频帧上操作，计算代价极高。
- **潜在视频生成**：如 **LDM**（Rombach et al., CVPR 2022）的思路推广至视频域，在压缩的视频潜空间中进行扩散，但潜变量仍保留时间维度，需使用 3D-UNet 架构。
- **潜在运动生成（LaMD）**：通过运动-内容分解，将运动信息压缩为 2D 空间特征图（时间维度被完全消除），扩散模型退化为 2D-UNet，采样速度与图像扩散模型相当。

这一范式转移的关键技术杠杆是**信息瓶颈**：运动编码器输出的潜变量 $\mathbf{z}_m$ 通过 KL 散度约束（系数 $\beta$）强制逼近标准正态分布，从而限制运动分支的信息容量，使内容信息被"排斥"到图像编码器路径中。调节 $\beta$ 和潜变量通道数 $d$ 即可在运动分离程度与重建质量之间取得平衡（Table 13）。

### 2. 与基线方法的关系

#### 2.1 运动-内容分离谱系

LaMD 的运动-内容分解策略与以下工作形成对比：

- **cINN**（Dorkenwald et al., CVPR 2021）：基于条件可逆网络，将视频生成建模为从随机噪声到视频帧的双射变换。该方法隐式地混合了运动与内容，缺乏显式的分离机制。
- **LFDM**（Ni et al., CVPR 2023）：通过潜在光流驱动像素生成，将运动显式建模为光流场。LaMD 与之不同之处在于：运动表示不限于光流，而是从视频重建任务中自监督学习得到的任意运动模式，表达力更强。

#### 2.2 扩散模型架构谱系

LaMD 的扩散运动生成器（DMG）采用 2D-UNet 配合交叉注意力，与以下架构形成对比：

- **3D-UNet 视频扩散模型**：在潜在视频空间中进行扩散，需处理时空联合维度，采样计算量随帧数线性增长。
- **VideoGPT**（Yan et al., 2021）：基于 VQ-VAE 将视频量化为离散 token，再用自回归 Transformer 生成。LaMD 的连续潜空间避免了量化误差，且扩散模型支持并行采样。

Table 11 和 Fig. 4 给出了具体的效率对比：生成 128 帧 128×128 视频，LaMD 仅需 10.7 秒（单张 RTX 3090，200 步采样），相较像素空间扩散和潜在视频扩散实现数量级加速。

#### 2.3 开放域视频生成谱系

**DynamiCrafter**（Xing et al., ECCV 2024）代表了开放域图像到视频生成的扩散模型路线，依赖大规模预训练文本-图像模型。LaMD 目前仅在封闭域数据集上验证，未利用外部预训练数据，因此在开放域泛化性上处于不同研究阶段。文中明确指出的公平性限制包括：MCD-VAE 和 DMG 均在目标数据集训练集上独立训练，未使用外部视频数据。

### 3. 适用边界与局限

#### 3.1 内容变化假设

MCD-VAE 的运动分解依赖一个关键假设：视频序列中内容（外观）保持相对稳定，运动是帧间变化的主要来源。当视频中出现**新物体进入场景**或**显著遮挡**时，运动编码器可能被迫将部分外观信息"偷运"进运动潜变量中，破坏运动-内容分离的纯净性。文中将此列为已知局限：当前框架主要适用于内容变化较小的短视频。

#### 3.2 任务边界

LaMD 目前仅支持**图像条件视频生成**（给定第一帧，生成后续帧），无法直接进行文本到视频生成。要实现后者，需要额外集成图像生成模型（如文本到图像扩散模型）作为第一帧的生成器，这在文中被列为开放问题。

#### 3.3 数据域边界

所有实验在五个封闭域数据集上进行：BAIR Robot Pushing（机器人操作）、Landscape（自然风景）、NATOPS（手势动作）、MUG（面部表情）、CATER-GEN-v2（合成物体运动）。这些数据集的共同特点是背景相对简单、运动模式有限。在开放域、复杂背景视频上的泛化性能尚未验证。

#### 3.4 训练数据规模

MCD-VAE 仅在目标数据集上训练，未利用大规模外部视频数据（如 WebVid 等）。文中指出这限制了 VAE 的表达能力上限，若结合大规模预训练数据，重建质量和运动分解效果可能进一步提升。

### 4. 开放问题与后续方向

1. **长视频与内容变化**：如何扩展 LaMD 以处理包含新物体出现、场景切换等显著内容变化的长视频？可能需要引入动态内容更新机制或分层运动表示。

2. **文本到视频生成**：如何与先进图像生成模型（如 Stable Diffusion）结合，实现端到端的文本到视频生成？这涉及文本条件如何同时影响第一帧内容和后续运动。

3. **开放域泛化**：LaMD 的运动分解机制在开放域、复杂背景视频上的有效性如何？是否需要更大规模、更多样化的训练数据？

4. **运动表示的可迁移性**：运动-内容分解的思想是否可推广到其他视频任务？例如视频编辑（替换运动而保留内容）、运动迁移（将一种运动的潜变量应用于另一视频的内容特征，如 Fig. 6 所示）、视频异常检测等。

5. **潜空间最优配置**：消融实验（Table 13）表明通道数 $d=3$ 在运动表达力与生成难度之间取得最佳平衡，但这一结论是否跨数据集泛化？是否存在自适应调节 $\beta$ 和 $d$ 的机制？

## 原文 PDF

![[paperPDFs/arxiv_2023/LaMD_Latent_Motion_Diffusion_for_Image_Conditional_Video_Generation.pdf]]
