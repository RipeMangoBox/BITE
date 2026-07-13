---
title: "Flash-DMD: Towards High-Fidelity Few-Step Image Generation with Efficient Distillation and Joint Reinforcement Learning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Flash_DMD_Towards_High_Fidelity_Few_Step_Image_Generation_with_Efficient_Distillation_and_Joint_Reinforcement_Learning.pdf
project_link: null
code_link: null
aliases:
- FD
- Flash-DMD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 时间步感知的解耦蒸馏策略：在高噪声时间步仅使用DM损失学习全局结构，在低噪声时间步使用Pixel-GAN增强真实感；并通过稳定得分估计器（减少TTUR、仅用扩散损失训练、EMA更新）消除冲突。
primary_logic: 通过将蒸馏目标按时间步解耦，并联合强化学习同时进行，蒸馏过程的稳定梯度可以作为RL的正则化器，有效防止奖励黑客行为，在极低训练成本下实现少步生成的最优质量。
claims:
- Flash-DMD仅用DMD2 2.1%的训练成本（1000步，TTUR=1）即获得更高的人类偏好评分。
- 时间步感知解耦策略解决了DM损失和对抗损失的冲突，在TTUR=2时以8.3%的成本超越DMD2。
- 联合强化学习将蒸馏与RL同时训练，蒸馏损失稳定了RL过程，避免了HyperSD等方法的过度曝光和油画伪影。
- COCO-10k (SDXL 4-step) 上 ImageReward = 0.9740 (TTUR2-8k)
---

# Flash-DMD: Towards High-Fidelity Few-Step Image Generation with Efficient Distillation and Joint Reinforcement Learning

> [!tip] 核心洞察
> 通过将蒸馏目标按时间步解耦，并联合强化学习同时进行，蒸馏过程的稳定梯度可以作为RL的正则化器，有效防止奖励黑客行为，在极低训练成本下实现少步生成的最优质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | Flash-DMD：面向高保真度少步图像生成的高效蒸馏与联合强化学习 |
| 英文题名 | Flash-DMD: Towards High-Fidelity Few-Step Image Generation with Efficient Distillation and Joint Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.20549) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Flash-DMD |
| Dataset | COCO-10k |

> [!tip] 效果简介
> - COCO-10k (SDXL 4-step) 上，ImageReward 0.9740 (TTUR2-8k) vs 0.8748 (DMD2) (+0.0992)；MPS 12.71 (TTUR2-8k) vs 12.41 (DMD2) (+0.30)。
> - COCO-10k (SD3-Medium 4-step) 上，ImageReward 1.0214 (TTUR2-7k) vs 1.0173 (SD3-Medium 28-step teacher) (+0.0041)。
> - COCO-10k (SDXL 4-step, Phase2 RL) 上，PickScore 0.2346 (Flash-DMD Stage2) vs 0.2310 (Hyper-SDXL) (+0.0036)。

## 概要

扩散模型的少步生成面临一个核心矛盾：蒸馏过程需要在分布匹配与感知真实感之间取得平衡，但现有方法将两者简单叠加，导致梯度冲突与训练开销激增。以 **DMD2** 为代表的分布匹配蒸馏框架，其得分估计器被赋予双重任务——既要跟踪生成分布，又要充当真假鉴别器，迫使生成器与得分估计器以 1:5 的频率交替更新（TTUR=5），训练成本极高。同时，对抗损失在所有时间步上无差别施加，进一步加剧了优化次优。

**Flash-DMD** 的核心洞察在于：将蒸馏目标按时间步解耦，并让强化学习与蒸馏过程联合进行。具体而言，在高噪声时间步仅使用分布匹配损失以快速对齐教师模型的全局结构，在低噪声时间步引入基于 SAM 编码器的像素级 GAN（Pixel-GAN）以增强纹理真实感；同时，得分估计器被简化为仅用扩散损失训练、通过 EMA 跟踪生成分布，TTUR 可降至 1 或 2。这一解耦策略消除了损失冲突，使蒸馏过程的稳定梯度能够作为强化学习的正则化器，有效防止奖励黑客行为（如过度曝光、油画伪影）。

在方法谱系中，Flash-DMD 属于**分布匹配蒸馏 + 对抗训练 + 偏好优化**的混合范式。相较于 **LCM-SDXL**（一致性蒸馏）、**SDXL-Turbo**（对抗蒸馏）、**Hyper-SDXL**（分离式 RL 精炼）和 **PSO-DMD2**（偏好优化），Flash-DMD 的独特之处在于将三者有机融合为单一联合训练框架，而非分阶段叠加。

实验结果表明，Flash-DMD 在极低训练成本下实现了最优的少步生成质量。在 SDXL 4 步生成设定下，仅用 DMD2 约 2.1% 的训练成本（1000 步，TTUR=1），ImageReward 评分即达到 0.9740，超越 DMD2 的 0.8748；在 TTUR=2、8000 步时，MPS 评分达 12.71。跨架构验证中，基于 SD3-Medium 的 4 步 Flash-DMD 在 ImageReward 上以 1.0214 超越 28 步教师模型（1.0173）。在第二阶段联合强化学习后，PickScore 达到 0.2346，优于 Hyper-SDXL 的 0.2310。消融实验进一步证实：EMA 更新得分估计器在训练后期显著提升人类偏好评分，Pixel-GAN 对防止 RL 阶段模式坍塌至关重要，而 RL 损失与蒸馏损失的最佳更新频率比为 5:1。

### 少步生成：扩散模型加速的核心路径

扩散模型（Diffusion Models）凭借其在图像生成质量上的卓越表现，已成为当前生成式建模的主流范式。然而，其迭代采样机制导致推理速度极慢——生成单张图像通常需要数十甚至上百次神经网络前向传播，这严重制约了其在实时交互场景中的应用。少步生成（Few-Step Generation）因此成为该领域的核心研究问题，目标是将推理步数压缩至4–8步，同时尽可能保持生成质量。

现有少步生成方法大致可分为三条技术路线：**一致性蒸馏**（如**LCM-SDXL**）、**对抗蒸馏**（如**SDXL-Turbo**）以及**分布匹配蒸馏**（如**DMD2**）。其中，DMD2通过最小化生成分布与教师分布之间的KL散度，在理论上具有更直接的优化目标，因而在少步设置下展现出较强的竞争力。

### DMD2的效率瓶颈：梯度冲突与双重任务困境

尽管DMD2在分布匹配蒸馏框架上取得了显著进展，但其训练过程存在两个根本性的效率瓶颈：

**瓶颈一：损失函数的全局冲突。** DMD2在所有扩散时间步上同时叠加分布匹配损失（DMD loss）与对抗损失（adversarial loss），导致梯度方向相互矛盾。在高噪声时间步（如 $t=999$），生成器的主要任务是学习图像的全局结构布局，此时对抗损失的纹理增强信号不仅无益，反而干扰结构对齐；而在低噪声时间步（如 $t=499$），分布匹配损失的全局约束又限制了局部纹理细节的自由生成。这种“一刀切”的损失叠加策略造成了优化次优，迫使模型需要更长的训练时间来消解冲突。

**瓶颈二：得分估计器的双重任务困境。** 在DMD2框架中，生成器的得分估计器（Score Estimator）被同时赋予两项任务：其一，准确跟踪生成分布以估计 $p_{\text{gen}}$ 的得分函数；其二，充当隐式鉴别器以区分真假样本。这种双重角色迫使得分估计器需要以极高频率更新——DMD2采用TTUR=5（即得分估计器每更新5次，生成器才更新1次），极大增加了训练计算开销。

### 强化学习精炼的“奖励黑客”风险

在蒸馏获得少步模型后，现有工作常引入强化学习（RL）进行偏好精炼以进一步提升视觉质量，如**Hyper-SDXL**采用RL微调、**PSO-DMD2**采用偏好优化。然而，这些方法将RL作为一个独立的后期阶段，缺乏对生成过程的约束。当仅以奖励模型（如ImageReward、PickScore）为优化目标时，生成器容易产生“奖励黑客”（Reward Hacking）行为——即通过过度曝光、油画化纹理等伪影来欺骗奖励模型，而非真正提升图像的感知真实感。

### 本文动机：解耦蒸馏与联合强化学习

针对上述瓶颈，本文提出**Flash-DMD**，核心动机在于两点：

1. **时间步感知的解耦蒸馏**：将蒸馏目标按扩散时间步进行解耦——在高噪声步仅使用分布匹配损失学习全局结构，在低噪声步引入像素级对抗损失（Pixel-GAN）增强纹理真实感。同时，通过稳定得分估计器（降低TTUR、仅用扩散损失训练、引入EMA更新）消除双重任务冲突，从而以极低的训练成本实现高效蒸馏。

2. **联合强化学习**：将偏好优化与蒸馏过程同时进行，而非分离为独立阶段。蒸馏损失提供的分布匹配约束天然充当RL的正则化器，有效抑制奖励黑客行为，使得RL精炼能够稳定地提升视觉保真度而非产生伪影。

通过这两项设计，Flash-DMD旨在以DMD2仅约2–8%的训练成本，在4步生成设置下达到甚至超越原有方法的图像质量，并实现蒸馏与RL的协同增效。

## 核心方法与创新机理

Flash-DMD 的核心创新在于对 DMD2 蒸馏框架的两个根本性效率瓶颈进行了精确的因果干预，并通过联合强化学习实现了更稳定的偏好优化。

### 瓶颈诊断：DMD2 为何低效

DMD2 的训练过程存在两个关键问题：

1.  **梯度冲突与优化次优**：DMD2 在所有时间步上同时施加分布匹配损失与对抗损失。这两种损失的目标并不完全一致——分布匹配追求整体分布对齐，而对抗损失追求局部真实感——简单叠加导致梯度方向冲突，使优化过程次优。
2.  **得分估计器的双重负担**：DMD2 的生成器得分估计器 $\mu_{\text{gen}}$ 被赋予双重任务：既要跟踪生成分布以提供分布匹配的梯度信号，又要充当鉴别器来区分真假样本。这迫使 DMD2 采用 TTUR=5 的高频更新策略，极大增加了训练开销。

### 关键创新一：时间步感知的解耦蒸馏

Flash-DMD 的核心因果旋钮是**按时间步解耦蒸馏目标**，从根本上消除了梯度冲突：

-   **高噪声时间步（全局结构学习）**：仅使用纯分布匹配损失 $\mathcal{L}_{\text{DMD}}$（Eq. 4），使生成器快速向教师模型的输出分布对齐，学习图像的全局结构和语义布局。
-   **低噪声时间步（纹理真实感增强）**：仅使用对抗损失，引入基于 SAM 编码器的**像素级 GAN（Pixel-GAN）**，在像素空间直接辨别真实与生成图像，增强纹理细节和真实感。

这一解耦策略的因果逻辑清晰：高噪声步决定了图像的宏观结构，此时对抗信号噪声过大且无益；低噪声步决定了微观纹理，此时分布匹配的梯度已趋于平缓，对抗损失恰好可以弥补模式寻求（mode-seeking）倾向。

### 关键创新二：稳定化得分估计器

为消除得分估计器的双重负担，Flash-DMD 对 $\mu_{\text{gen}}$ 的更新策略进行了三项关键修改：

| 修改项 | DMD2 | Flash-DMD |
|--------|------|-----------|
| TTUR（更新频率比） | 5 | 1 或 2 |
| 训练损失 | 分布匹配 + 对抗 | 仅扩散损失 |
| 参数更新方式 | 直接梯度更新 | EMA 更新（Eq. 11） |

通过将 TTUR 降至 1-2、移除对抗损失对得分估计器的干扰、并引入 EMA（$\psi \leftarrow \lambda_{\text{ema}} \psi + (1 - \lambda_{\text{ema}}) \theta$），得分估计器仅需稳定跟踪生成分布，无需承担鉴别器角色。这直接带来了训练成本的量级下降——Flash-DMD 仅需 DMD2 约 2.1% 的训练成本即可获得更高的人类偏好评分（Table 1）。

### 关键创新三：联合强化学习与蒸馏正则化

现有少步模型的强化学习精炼（如 Hyper-SDXL、PSO-DMD2）通常作为分离的后处理阶段，容易产生奖励黑客（reward hacking）现象——模型为追求高奖励分数而生成过度曝光、油画伪影或过度平滑的图像（Fig. 4）。

Flash-DMD 将偏好优化与蒸馏过程**联合训练**，核心机制在于：

-   蒸馏损失 $\mathcal{L}_{\text{DMD}}$ 作为强化学习的**隐式正则化器**，约束生成器在追求高奖励时不偏离教师分布太远。
-   偏好优化采用对数似然损失 $\mathcal{L}_{rl} = -\mathbb{E} [\log \sigma (\beta \mathcal{H}(w,l))]$（Eq. 12），通过隐式奖励模型（LRM）构造胜-负对，计算策略模型与参考模型的对数概率比差异 $\mathcal{H}(w,l)$（Eq. 13）。

联合训练中，RL 损失与分布匹配损失的最佳更新频率比为 5:1，可获得最高 ImageReward = 0.9808（Table 4）。Pixel-GAN 在此阶段至关重要——移除 Pixel-GAN 会导致 RL 阶段的模式坍塌和生成质量下降（Fig. 7）。

Flash-DMD 是一个面向少步扩散模型蒸馏的两阶段联合训练框架，其核心设计思想是将分布匹配与感知质量增强按时间步解耦，并在第二阶段将强化学习精炼与蒸馏过程无缝融合。

### 两阶段训练流程

如图 2 所示，整个 pipeline 分为两个阶段：

**Stage 1 — 时间步感知蒸馏**：从预训练的教师扩散模型（如 SDXL、SD3-Medium）出发，对少步生成器 $G_\theta$ 进行高效蒸馏。该阶段的关键创新在于按噪声水平将蒸馏目标解耦：
- **高噪声时间步**（$t$ 接近 $T$）：仅使用分布匹配损失（DMD loss），利用教师模型的真实分数 $s_\tau$ 与生成分布分数估计器 $\mu_\text{gen}^\psi$ 之间的差异，驱动生成器快速对齐教师模型的全局输出分布。
- **低噪声时间步**（$t$ 接近 0）：仅使用像素级对抗损失（Pixel-GAN），在真实图像上增强纹理细节与真实感，对抗 DMD 损失固有的模式寻求倾向。

**Stage 2 — 联合强化学习精炼**：在 Stage 1 蒸馏得到的模型基础上，同时进行分布匹配蒸馏与偏好优化。隐式奖励模型（LRM）在任意时间步评估生成样本的隐式表示，构造胜-负对，通过偏好优化损失 $\mathcal{L}_{rl}$ 对生成器进行精炼。蒸馏损失在此过程中充当正则化器，有效抑制纯 RL 方法中常见的奖励黑客行为（如过度曝光、油画伪影）。

### 核心模块与数据流

框架由以下关键模块构成，数据流沿图 2 所示的路径传递：

1. **教师扩散模型**：固定权重，仅用于提供真实分数 $s_\tau$ 作为分布匹配的监督信号。
2. **生成器 $G_\theta$**：少步生成器，从随机噪声 $z$ 出发，经 $N$ 步（通常 $N=4$ 或 $8$）去噪生成隐式表示，再通过 VAE 解码器 $\mathcal{V}$ 重建为像素图像。
3. **得分估计器 $\mu_\text{gen}^\psi$**：跟踪生成器分布的变化，估计 $p_\text{gen}$ 的分数。与 DMD2 不同，Flash-DMD 将其从鉴别器角色中解放出来，仅用扩散损失训练，采用 TTUR=1 或 2 的更新频率，并通过 EMA 平滑参数更新（式 11）。
4. **Pixel-GAN 鉴别器 $D_\omega$**：基于冻结的 SAM 视觉编码器构建，提取层次化特征并通过多个可训练的鉴别器头在像素空间辨别真假，增强纹理真实感。
5. **隐式奖励模型（LRM）**：在任意时间步评估隐式表示的质量，用于构造偏好优化的胜-负对。
6. **偏好优化模块**：利用胜-负对计算对数似然比率差异 $\mathcal{H}(w,l)$（式 13），并通过式 12 的偏好优化损失更新生成器。

### 训练效率与稳定性设计

框架通过三个机制实现极低训练成本下的高效蒸馏：

- **时间步感知解耦**：消除了 DMD2 中分布匹配损失与对抗损失在所有时间步简单叠加导致的梯度冲突，使训练在 TTUR=2 时仅需 DMD2 约 8.3% 的成本即可超越其性能（Table 1）。
- **稳定得分估计器**：将 TTUR 从 5 降至 1-2，移除其鉴别器职责，仅用扩散损失训练并辅以 EMA 更新，显著降低训练开销并提升后期稳定性（Fig. 5, Fig. 6）。
- **联合强化学习**：蒸馏与 RL 同时训练，蒸馏损失的稳定梯度作为 RL 的正则化器，防止模式坍塌。消融实验表明，移除 Pixel-GAN 会导致 RL 阶段 ImageReward 下降（Fig. 7），而 RL 损失与 DMD 损失的最优更新频率比为 5:1（Table 4）。

整个框架在 SDXL 上仅需 DMD2 约 2.1% 的训练成本（TTUR=1, 1000 步）即可获得更高的人类偏好评分，在 SD3-Medium 上同样展现出跨架构的泛化能力（Table 2）。

![[assets/figures/papers/paper_list_l2287_https_arxiv_org_abs_2511_20549/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our proposed Flash-DMD. We decouple the distillation objective by timestep into a Diffusion Matching loss and an adversarial loss. During high-noise timesteps, the DMD loss enables rapid alignment with the teacher model, while at low-noise timesteps and on real images, Pixel-GAN loss is employed to enhance realism and texture details. This design achieves a more efficient distillation. Building upon this, we further introduce a reinforcement strategy specifically tailored for few-step distilled models, which seamlessly integrates with the distillation objective to achieve superior and more stable performance*

Flash-DMD 的训练框架由两大阶段构成：第一阶段为**时间步感知的高效蒸馏**，第二阶段为**联合强化学习精炼**。其核心创新在于将分布匹配损失与对抗损失按时间步解耦，并通过稳定得分估计器消除梯度冲突，从而以极低训练成本实现少步生成的高保真度。

### 3.1 分布匹配蒸馏基础

Flash-DMD 建立在 DMD 系列方法的分布匹配框架之上。对于教师扩散模型定义的真实分布 $p_{\tau}$ 和生成器 $G_{\theta}$ 产生的生成分布 $p_{\mathrm{gen}}$，DMD 通过 KL 散度最小化使两者对齐。其梯度形式为：

$$
\nabla_{\boldsymbol{\theta}} \mathcal{L}_{\mathrm{DMD}} = -\mathbb{E}_{z,t} \left[ s_{\tau}(\mathcal{G}_{\boldsymbol{\theta}}(\cdot)) - s_{\mathrm{gen}}(\mathcal{G}_{\boldsymbol{\theta}}(\cdot)) \right] \frac{d\mathcal{G}_{\boldsymbol{\theta}}(\cdot)}{d\boldsymbol{\theta}}
$$

其中 $s_{\tau}(x_t, t)$ 为教师分布的得分函数，$s_{\mathrm{gen}}(x_t, t)$ 为生成分布的得分函数。得分函数与扩散模型的均值估计 $\mu(x_t, t)$ 之间的关系为：

$$
s(x_t, t) = -\frac{x_t - \alpha_t \mu(x_t, t)}{\sigma_t^2}
$$

在 DMD2 中，除分布匹配损失外，还引入了对真实图像的对抗训练。然而，这种简单的叠加方式存在两个关键瓶颈：**梯度冲突**——分布匹配损失在所有时间步上与对抗损失同时作用，导致优化次优；**得分估计器过载**——生成器的得分估计器被赋予双重任务（既跟踪生成分布又充当鉴别器），迫使 TTUR=5 的高频更新，极大增加了训练开销。

### 3.2 时间步感知的解耦蒸馏策略

Flash-DMD 的核心洞察是：不同噪声水平的时间步对生成任务的贡献本质不同。**高噪声时间步**（低 SNR）主要决定图像的全局结构和语义布局，此时应专注于与教师分布对齐；**低噪声时间步**（高 SNR）则决定纹理细节和真实感，此时对抗训练最为有效。

基于此，Flash-DMD 提出**时间步感知的解耦策略**：

- **高噪声时间步**：仅使用 DMD 损失（式 4）优化生成器，快速对齐教师模型的输出分布；
- **低噪声时间步**：仅使用 Pixel-GAN 对抗损失，增强纹理真实感和细节保真度。

对抗损失的梯度形式为：

$$
\nabla_{\boldsymbol{\theta}} \mathcal{L}_{\mathrm{AdvGen}}^{\mathrm{TA}} = \left[ \mathbb{E}_{\boldsymbol{\hat{t}}, \boldsymbol{\hat{x}}} \log \mathcal{D} \left( \mathcal{V} \left( \mathcal{G}_{\boldsymbol{\theta}} ( \boldsymbol{\hat{x}}, \boldsymbol{\hat{t}} ) \right) \right) \right] \frac{d\mathcal{G}_{\boldsymbol{\theta}}(\cdot)}{d\boldsymbol{\theta}}
$$

其中 $\mathcal{V}$ 为预训练的 SAM 视觉编码器，$\mathcal{D}$ 为鉴别器，$\boldsymbol{\hat{t}}$ 为低噪声时间步。

### 3.3 Pixel-GAN：像素级对抗损失

与 DMD2 在隐空间进行对抗训练不同，Flash-DMD 引入基于 SAM 编码器的**像素级 GAN（Pixel-GAN）**。鉴别器构建于冻结的 SAM 视觉编码器之上，提取层次化特征并附加多个可训练的鉴别器头。Pixel-GAN 的鉴别器损失为：

$$
\mathcal{L}_{\mathrm{AdvDisc}}^{\mathrm{PG}} = \mathbb{E}_{x_{\mathrm{real}}} \left[ -\log \mathcal{D}_{\omega}(\cdot) \right] + \mathbb{E}_{z} \left[ \log \mathcal{D}_{\omega} \left( \mathcal{V}(\cdot) \right) \right]
$$

Pixel-GAN 在像素空间直接辨别真实图像与生成图像，能够有效对抗 DMD 损失的模式寻求倾向（纯 DMD 损失会导致高对比度、缺乏纹理的生成结果），为后续强化学习阶段的稳定性提供关键保障。

### 3.4 稳定得分估计器：EMA 更新与 TTUR 降低

为解决得分估计器的过载问题，Flash-DMD 将其角色简化为**仅跟踪生成分布**，不再承担鉴别器功能。具体措施包括：

- **降低更新频率**：将 TTUR 从 DMD2 的 5 降至 1 或 2，即生成器每更新 1-2 次，得分估计器才更新一次；
- **仅用扩散损失训练**：得分估计器仅通过扩散损失优化，避免对抗损失的干扰；
- **EMA 参数更新**：通过指数移动平均使得分估计器参数平滑跟随生成器参数：

$$
\psi \leftarrow \lambda_{\mathrm{ema}} \psi + (1 - \lambda_{\mathrm{ema}}) \theta
$$

消融实验表明，EMA 更新在训练后期（4000 步以上）显著提升 ImageReward 和 PickScore，是维持训练稳定性的关键组件。

### 3.5 联合强化学习精炼

Flash-DMD 的第二阶段将强化学习与蒸馏过程**联合训练**，而非像 Hyper-SDXL 等方法那样进行分离的 RL 微调。核心思路是：蒸馏损失为 RL 过程提供稳定的梯度正则化，防止奖励黑客行为（如过度曝光、油画伪影）。

RL 部分采用偏好优化框架，使用隐式奖励模型（LRM）在任意时间步评估隐式表示的偏好，构造胜-负对。偏好优化损失为：

$$
\mathcal{L}_{rl} = -\mathbb{E} \left[ \log \sigma \left( \beta \mathcal{H}(w, l) \right) \right]
$$

其中 $\mathcal{H}(w, l)$ 为胜者与败者的隐式奖励差异：

$$
\mathcal{H}(w, l) = \log \frac{p_{\theta}(z_{t-1}^{w}|z_t,c)}{p_{ref}(z_{t-1}^{w}|z_t,c)} - \log \frac{p_{\theta}(z_{t-1}^{l}|z_t,c)}{p_{ref}(z_{t-1}^{l}|z_t,c)}
$$

联合训练中，RL 损失与分布匹配损失的最佳更新频率比为 5:1，可获得最高的 ImageReward 评分（0.9808）。移除 Pixel-GAN 会导致 RL 阶段出现模式坍塌，进一步验证了第一阶段对抗训练对后续精炼的奠基作用。

## 实验与关键发现

### 主实验结果

Flash-DMD 在两个主流教师模型（SDXL 和 SD3-Medium）上均以极低的训练成本取得了最优或接近最优的人类偏好评分。Table 1 展示了 SDXL 4 步生成在 COCO-10k 上的 Stage 1 蒸馏对比：Flash-DMD (TTUR2-8k) 的 ImageReward 达到 **0.9740**，远超 DMD2 的 0.8748（+0.0992），而训练成本仅为 DMD2 的 2.1%（1000 步，TTUR=1）。在 MPS 指标上，Flash-DMD 同样以 12.71 领先 DMD2 的 12.41。Table 2 进一步验证了跨架构泛化能力：在 SD3-Medium 上，Flash-DMD (TTUR2-7k) 的 ImageReward 达到 **1.0214**，甚至超过了 28 步教师模型 SD3-Medium 的 1.0173。

![[assets/figures/papers/paper_list_l2287_https_arxiv_org_abs_2511_20549/figures/005_Table_1.jpg]]
*Table 1: Comparison of Flash-DMD on SDXL under stage 1 with other distillation methods on the COCO-10k dataset. ImgRwd denotes ImageReward score. Cost refers to the product of batch size and training iterations. Best performance is highlight with Bold, and the second is with underline*

![[assets/figures/papers/paper_list_l2287_https_arxiv_org_abs_2511_20549/figures/006_Table_2.jpg]]
*Table 2: Comparison of Flash-DMD on SD3 under stage 1 with other distillation method and baseline on COCO-10k dataset*

Stage 2 的联合强化学习精炼同样展现出显著优势。Table 3 显示，Flash-DMD Stage2 在 PickScore 上达到 **0.2346**，优于 Hyper-SDXL 的 0.2310 和 PSO-DMD2 的 0.2323。更重要的是，如 Fig. 4 所示，HyperSD 在 RL 精炼后出现了过度曝光和油画伪影，而 Flash-DMD 的联合训练策略通过蒸馏损失的正则化作用有效避免了此类奖励黑客行为。

![[assets/figures/papers/paper_list_l2287_https_arxiv_org_abs_2511_20549/figures/004_Table_3.jpg]]
*Table 3: Comparison of Flash-DMD under phase2 with other models with reinforcement learning on COCO-10k dataset*

![[assets/figures/papers/paper_list_l2287_https_arxiv_org_abs_2511_20549/figures/011_Figure_4.jpg]]
*Figure 4: Qualitative comparisons with other reinforcement approaches on SDXL. com*

### 消融实验

**EMA 更新策略。** Fig. 6 展示了得分估计器使用 EMA 更新的消融结果。在训练早期（4000 步以下），使用与不使用 EMA 的性能差距不大；但训练后期（4000 步以上），EMA 模型在 ImageReward 和 PickScore 上均显著优于无 EMA 版本。这验证了稳定得分估计器对于长期训练收敛的关键作用。

**Pixel-GAN 的必要性。** Fig. 7 和 Table 4 揭示了 Pixel-GAN 对 RL 阶段的关键影响。移除 Pixel-GAN 后，RL 训练出现模式坍塌，ImageReward 显著下降。这表明时间步感知解耦策略中引入的 Pixel-GAN 不仅提升了 Stage 1 的真实感，还为 Stage 2 的 RL 训练提供了必要的生成多样性基础。

**RL 与蒸馏的更新频率比。** Table 4 系统消融了 Stage 2 中强化学习损失与分布匹配损失的更新频率比。当比例为 **5:1** 时，模型获得最高 ImageReward = 0.9808，综合性能最优。过高或过低的 RL 更新频率均会导致性能下降，说明蒸馏损失的稳定梯度对 RL 过程的正则化强度需要精确控制。

**对抗训练的必要性。** 仅使用 DMD 损失（无对抗训练）的模型表现出明显的模式寻求行为——生成图像对比度过高、缺乏纹理细节。这从反面证明了时间步感知解耦策略中低噪声步引入 Pixel-GAN 对抗损失的必要性。

### 训练稳定性分析

Fig. 5 对比了 DMD2 与 Flash-DMD 在 TTUR=2 下的训练稳定性。DMD2 在训练过程中快速退化，而 Flash-DMD 持续稳定提升。这一差异的根源在于 Flash-DMD 将得分估计器的角色从“鉴别器+跟踪器”简化为“仅跟踪生成分布”，并采用 EMA 更新，消除了 DMD2 中因双重任务导致的梯度冲突和优化次优。

![[assets/figures/papers/paper_list_l2287_https_arxiv_org_abs_2511_20549/figures/012_Figure_5.jpg]]
*Figure 5: Evaluation results of DMD2(red) and Flash-DMD (blue) with TTUR at the ratio of 2 on SDXL*

### 关键图表结论

- **Table 1**：Flash-DMD 以 DMD2 2.1% 的训练成本实现了显著更高的 ImageReward（0.9740 vs 0.8748），验证了时间步感知解耦策略的效率优势。
- **Table 2**：在 SD3-Medium 上超越 28 步教师模型，证明了方法的跨架构泛化能力。
- **Table 3**：联合 RL 训练在 PickScore 上超越 Hyper-SDXL 和 PSO-DMD2，且避免了后者的视觉伪影。
- **Fig. 5**：Flash-DMD 在 TTUR=2 下持续提升，DMD2 快速退化，凸显稳定得分估计器的重要性。
- **Fig. 6**：EMA 更新在训练后期（4000+ 步）显著提升人类偏好评分。
- **Fig. 7**：移除 Pixel-GAN 导致 RL 阶段模式坍塌，验证了对抗训练对 RL 正则化的必要性。

## 定位与知识库关联

### 1. 与基线方法的关系

Flash-DMD 的核心框架建立在 **DMD2** 的分布匹配蒸馏范式之上，但针对其两个关键效率瓶颈进行了系统性重构。DMD2 在所有时间步上同时施加分布匹配损失与对抗损失，导致梯度冲突与优化次优；同时，其得分估计器被赋予双重任务——既跟踪生成分布又充当鉴别器，迫使采用 TTUR=5 的高频更新策略，极大增加了训练开销。Flash-DMD 通过时间步感知的解耦蒸馏策略和稳定得分估计器设计，从根本上解决了这两个问题。

在少步扩散蒸馏的方法谱系中，Flash-DMD 与以下代表性基线形成明确对比：

- **DMD2**：作为分布匹配蒸馏的基准框架，Flash-DMD 直接继承其教师-学生分数匹配机制，但通过解耦损失和降低 TTUR 实现了训练成本的大幅压缩（仅需 DMD2 的 2.1% 成本即获得更高人类偏好评分，见 Table 1）。
- **LCM-SDXL**：一致性蒸馏路线，通过约束相邻时间步输出一致性实现少步生成。Flash-DMD 在 ImageReward 和 MPS 上均显著超越 LCM-SDXL（Table 1），表明分布匹配范式在保真度上具有优势。
- **SDXL-Turbo**：对抗蒸馏路线，依赖隐空间 GAN 进行蒸馏。Flash-DMD 引入的 Pixel-GAN 在像素空间操作，利用 SAM 编码器的层次化特征，比隐空间鉴别器更有效地增强纹理真实感。
- **Hyper-SDXL**：采用分离的强化学习精炼阶段，但存在奖励黑客行为——使用 ImageReward 优化时产生过度曝光和油画伪影（Fig. 4）。Flash-DMD 的联合训练框架将蒸馏损失作为 RL 的正则化器，有效抑制了此类退化。
- **PSO-DMD2**：基于偏好优化的少步模型，使用 PickScore 时倾向于生成过度平滑的图像。Flash-DMD 的隐式奖励模型（LRM）在任意时间步评估偏好，配合联合训练策略，避免了单一奖励信号导致的纹理丧失。

### 2. 方法适用边界

Flash-DMD 的设计在以下条件下展现出最佳性能：

- **架构兼容性**：方法在 SDXL 和 SD3-Medium 上均得到验证（Table 1, Table 2），表明其解耦蒸馏策略对 UNet 和 DiT 架构均适用。然而，向更大规模模型（如 SD3.5 Large）的扩展尚未经验证，推理成本与训练稳定性的可迁移性需要进一步研究。
- **少步推理场景**：论文聚焦于 4 步生成，在极低推理预算下实现高质量输出。对于更少步数（1-2 步）或更多步数（8-16 步）的适用性，论文未提供系统实验。
- **文本到图像生成**：所有实验均在文本条件生成任务上进行，向视频生成、图像编辑等任务的泛化能力属于开放问题。
- **训练成本敏感场景**：Flash-DMD 的核心优势在于极低训练成本（1000-8000 步，TTUR=1 或 2），适合计算资源受限的研究环境。但消融实验表明，EMA 更新在 4000 步以上才显著提升性能（Fig. 6），暗示极低训练预算下可能无法完全释放 EMA 的增益。

### 3. 局限与开放问题

论文自身未明确列出局限性，但从实验设置和方法设计中可推断以下潜在局限：

1. **Pixel-GAN 的依赖风险**：消融实验（Fig. 7, Table 4）表明，移除 Pixel-GAN 会导致 RL 阶段 ImageReward 下降，暗示联合训练框架对 Pixel-GAN 的纹理增强作用有较强依赖。若下游任务对纹理真实性要求较低，Pixel-GAN 的计算开销可能成为冗余。
2. **隐式奖励模型的泛化性**：LRM 在任意时间步评估偏好，但其对高噪声时间步评估的可靠性尚未充分验证。论文提出的开放问题之一即是如何优化 LRM 以更好地适应少步蒸馏模型的高噪声时间步评估。
3. **联合训练的更新频率敏感度**：Table 4 显示 RL 损失与 DM 损失的最佳更新频率比为 5:1，表明联合训练对超参数配置较为敏感，实际部署时可能需要额外的调参成本。
4. **公平性评估的局限**：所有实验在 COCO-10k 测试集上进行，训练成本通过批量大小×迭代次数公平量化。但不同方法的 GPU 架构和实现优化程度可能影响实际训练时间，论文未提供端到端 GPU 小时的直接对比。

### 4. 开放问题

论文明确提出了两个阶段性开放问题：

- **Q1（早期阶段）**：如何更有效地协调分布匹配与感知真实感增强，以加速收敛？这指向时间步感知策略的进一步优化空间——当前的高噪声步纯 DM 损失与低噪声步纯 Pixel-GAN 损失之间缺乏过渡机制，可能导致中间时间步的优化盲区。
- **Q2（后期阶段）**：如何以更直接的方式精炼学生模型，以获得更好的视觉细节和感知保真度？这暗示联合 RL 框架仍有改进空间，例如引入更精细的奖励信号或多目标优化策略。

此外，论文还提出了两个架构扩展方向的开放问题：将 Flash-DMD 的联合训练框架拓展到更大模型（如 SD3.5 Large）与视频生成任务；以及优化现有 LRM 以更好地适应少步蒸馏模型的高噪声时间步评估。这些问题的解决将决定 Flash-DMD 方法范式的生态位宽度。

## 原文 PDF

![[paperPDFs/CVPR_2026/Flash_DMD_Towards_High_Fidelity_Few_Step_Image_Generation_with_Efficient_Distillation_and_Joint_Reinforcement_Learning.pdf]]
