---
title: "FlashMotion: Few-Step Controllable Video Generation with Trajectory Guidance"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FlashMotion_Few_Step_Controllable_Video_Generation_with_Trajectory_Guidance.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Li_FlashMotion_Few-Step_Controllable_Video_Generation_with_Trajectory_Guidance_CVPR_2026_paper.html
project_link: null
code_link: null
aliases:
- FlashMotion
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 通过三阶段训练范式，先训练多步适配器，再蒸馏少步生成器，最后采用结合扩散损失和对抗损失（辅助扩散鉴别器和动态损失缩放）的混合训练策略来微调轨迹适配器，使适配器与少步生成器的不同去噪路径对齐。
primary_logic: 引入扩散鉴别器进行对抗训练，强制对齐真实和生成视频的分布，弥补纯扩散损失仅提供像素级监督的不足；同时使用动态扩散损失缩放调度，平衡初期占优的扩散梯度与GAN梯度，从而消除模糊并保留轨迹控制。
claims:
- 直接使用少步推理或直接将SlowAdapter用于FastGenerator均导致模糊和质量下降（图1a,b）
- 仅用扩散损失微调适配器导致明显模糊（图1c），引入扩散鉴别器后质量和轨迹准确度得到提升
- 提出混合训练和动态损失缩放，显著优于多步方法和蒸馏方法，在FlashBench上达到最佳FID/FVD/IoU，同时实现47×加速
- FlashBench 上 FID = 14.35 (ControlNet)
---

# FlashMotion: Few-Step Controllable Video Generation with Trajectory Guidance

> [!tip] 核心洞察
> 引入扩散鉴别器进行对抗训练，强制对齐真实和生成视频的分布，弥补纯扩散损失仅提供像素级监督的不足；同时使用动态扩散损失缩放调度，平衡初期占优的扩散梯度与GAN梯度，从而消除模糊并保留轨迹控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | FlashMotion：基于轨迹引导的少步可控视频生成 |
| 英文题名 | FlashMotion: Few-Step Controllable Video Generation with Trajectory Guidance |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_FlashMotion_Few-Step_Controllable_Video_Generation_with_Trajectory_Guidance_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | FlashMotion |
| Dataset | FlashBench |

> [!tip] 效果简介
> - FlashBench 上，FID 14.35 (ControlNet) vs 19.44 (SlowAdapter w/o fine-tuning, ControlNet) (-5.09)；FVD 96.08 (ControlNet) vs significantly higher (e.g., >200) (~50% reduction)；Mask IoU / Box IoU 69.15 / 75.38 (ControlNet) vs less than 60 / 65 (e.g., w/o diffusion loss) (>9 points improvement)。

## 概要

**问题瓶颈**：现有多步轨迹可控视频生成方法（如 **MagicMotion** (Li et al., ICCV 2025)、**Tora** (Zhang et al., CVPR 2025)、**LeviTor** (Wang et al., CVPR 2025) 等）依赖数十步去噪过程，导致大量推理时间冗余和计算开销。直接将多步适配器应用于少步生成器，或仅使用扩散损失微调，均导致显著的视频质量退化与轨迹精度下降（图1a–c）。

**核心方法**：**FlashMotion** 提出三阶段训练范式以解决上述瓶颈：(1) 先在多步生成器（SlowGenerator）上训练轨迹适配器（SlowAdapter）；(2) 通过分布匹配蒸馏将多步生成器压缩为4步生成器（FastGenerator）；(3) 采用混合训练策略——结合扩散损失与对抗损失，并引入**扩散鉴别器**（Diffusion Discriminator）和**动态损失缩放**——对轨迹适配器进行微调，使其与少步生成器的不同去噪路径对齐（图2、图3）。

**关键洞察**：扩散鉴别器的对抗训练强制对齐真实与生成视频的分布，弥补了纯扩散损失仅提供像素级监督的不足；动态扩散损失缩放调度（$\lambda = \frac{1}{4} \times 10^{-3} \times step + 0.1$）平衡了训练初期占优的扩散梯度与GAN梯度，从而消除模糊并保留轨迹控制。

**主要结果**：在 FlashBench 基准上，FlashMotion 以4步去噪实现 ControlNet 适配器 FID 14.35、FVD 96.08、Mask IoU 69.15 / Box IoU 75.38，去噪时间仅32.2秒（121帧），相比先前最优多步方法 **MagicMotion**（50步，1507.6秒）获得 **47× 加速**，同时质量与轨迹精度均显著优于现有少步蒸馏方法（如 **LCM** (Luo et al., arXiv 2023)、**DMD²** (Yin et al., NeurIPS 2024) 等）（表1）。

**方法定位**：FlashMotion 属于少步轨迹可控视频生成的训练框架，其技术谱系融合了扩散模型蒸馏（DMD 分布匹配）、轨迹适配器（ResNet/ControlNet 结构）与对抗训练（扩散鉴别器），在方法谱系中填补了“少步推理 + 精确轨迹控制”的空白。



### 轨迹可控视频生成的效率瓶颈

轨迹可控视频生成旨在根据用户指定的运动轨迹（如拖拽点、边界框或分割掩码）合成高质量视频，在内容创作、视觉特效和具身智能等领域具有广泛应用。近年来，以**MagicMotion** (Li et al., ICCV 2025)、**Tora** (Zhang et al., CVPR 2025)、**LeviTor** (Wang et al., CVPR 2025)、**DragAnything** (Wu et al., ECCV 2024) 和**SG-I2V** (Namekata et al., ICLR 2025) 为代表的多步去噪方法取得了显著进展。然而，这些方法的共同瓶颈在于：它们依赖数十步（通常为50步）的去噪过程来生成视频，导致推理时间冗余和计算开销巨大。例如，在单张A100 GPU上生成121帧视频，**MagicMotion**的去噪时间长达1507.6秒，严重制约了实际部署的可行性。

### 少步推理的直接适配困境

一个直观的解决思路是将多步视频生成器蒸馏为少步生成器（如4步），以大幅降低推理成本。现有少步蒸馏方法如**LCM** (Luo et al., arXiv 2023)、**DMD²** (Yin et al., NeurIPS 2024)、**APT** 和 **APT2** (Lin et al., arXiv 2025) 已在无条件或文本条件视频生成中展现出潜力。然而，当将这些蒸馏方法直接应用于轨迹可控场景时，会面临两个关键失败模式：

1. **少步推理导致模糊**：将训练好的多步轨迹适配器（SlowAdapter）直接与多步生成器（SlowGenerator）结合进行少步推理时，输出视频出现严重模糊（Figure 1a）。这是因为适配器在训练阶段习得的去噪路径与少步推理时的路径存在显著分布偏移。

2. **适配器-生成器失配**：将SlowAdapter直接应用于蒸馏后的少步生成器（FastGenerator）时，不仅视频质量下降，轨迹精度也严重退化（Figure 1b）。这表明多步适配器的特征表示与少步生成器的内部表征之间存在根本性的不兼容。

### 纯扩散损失微调的不足

为缓解上述失配问题，一个自然的尝试是使用扩散损失对适配器进行微调。然而，实验表明仅用扩散损失微调适配器仍然导致明显的模糊伪影（Figure 1c）。其深层原因在于：扩散损失本质上提供的是像素级的逐帧监督，缺乏对视频整体分布的高层语义感知。在少步生成器的去噪路径下，单纯依赖像素级损失无法有效消除由步数减少引入的分布偏差，使得生成结果在视觉质量上远逊于多步方法。

### FlashMotion的核心动机

上述分析揭示了一个核心矛盾：**如何在保持轨迹控制精度的同时，实现少步高质量视频生成？** 现有方法要么牺牲速度（多步方法），要么牺牲质量（直接蒸馏或纯扩散微调），无法同时满足效率与质量的双重需求。FlashMotion的动机正是打破这一困境——通过引入扩散鉴别器进行对抗训练，强制对齐真实视频与生成视频的分布，弥补纯扩散损失仅提供像素级监督的不足；同时设计动态扩散损失缩放策略，平衡初期占优的扩散梯度与GAN梯度，从而消除模糊并保留轨迹控制能力。最终，FlashMotion在仅需4步去噪的条件下，实现了与多步方法相当甚至更优的视觉质量与轨迹精度，同时获得了47倍的推理加速。



## 核心方法与创新机理

FlashMotion 的核心创新在于解决“少步可控视频生成”中轨迹精度与视觉质量不可兼得的瓶颈，其关键改动可归纳为以下几个维度。

### 1. 从多步到少步的生成器步数跃迁

现有轨迹可控视频方法（如 **MagicMotion** (Li et al., ICCV 2025)、**Tora** (Zhang et al., CVPR 2025)、**LeviTor** (Wang et al., CVPR 2025)）均依赖多步去噪生成器（通常 50 步），导致推理时间冗余严重。FlashMotion 将生成器步数从 **50 步压缩至 4 步**（Stage 2 蒸馏得到的 FastGenerator），使单次 121 帧视频的去噪时间从 1507.6 秒降至 32.2 秒，实现 **47× 加速**（Table 1）。这一改动直接改变了生成器的工作路径，但同时也引入了新的挑战：直接将为慢速生成器训练的轨迹适配器用于少步生成器，会导致严重的模糊和轨迹精度退化（Figure 1a,b）。

### 2. 适配器优化目标：从纯扩散损失到混合对抗训练

传统方法仅使用扩散损失（像素级 MSE）训练轨迹适配器。当适配器需要与少步生成器对齐时，纯扩散损失的监督信号不足，导致输出模糊（Figure 1c）。FlashMotion 在 Stage 3 引入**混合训练策略**，将适配器的优化目标从单一的扩散损失扩展为扩散损失与对抗损失的联合优化：

$$\mathcal{L} = \mathcal{L}_{\mathcal{G}} + \lambda \mathcal{L}_{diffusion}$$

其中生成器对抗损失 $\mathcal{L}_{\mathcal{G}}$ 迫使适配器欺骗鉴别器，扩散损失 $\mathcal{L}_{diffusion}$ 提供像素级轨迹约束。消融实验表明，移除 GAN 损失使 ControlNet 的 FID 从 14.35 升至 28.82，证实对抗训练对消除模糊至关重要；移除扩散损失则使 Mask IoU 从 69.15 降至 55.91，证明扩散损失对保持轨迹精度不可或缺（Table 2）。

### 3. 鉴别器设计：引入扩散鉴别器与多层注意力分类器

为有效区分真实视频与生成视频的分布差异，FlashMotion 设计了一个**扩散鉴别器**（Diffusion Discriminator）。该鉴别器以 SlowGenerator 的 DiT 骨干为基础，从中提取多层中间特征，送入一个注意力分类器。分类器包含三个关键注意力模块：**语义自注意力层**（SS）、**轨迹交叉注意力层**（TC）和**视频交叉注意力层**（VC）。消融实验表明，完整鉴别器架构（SS+TC+VC）在 FID 和 IoU 上均达到最佳性能（Table 3），证明多层注意力机制对捕捉视频质量与轨迹一致性至关重要。

### 4. 损失权重调度：动态扩散损失缩放

在混合训练中，扩散损失的梯度幅度在训练初期远大于 GAN 梯度，若使用固定权重 $\lambda$ 会抑制对抗训练的效果。FlashMotion 提出**动态扩散损失缩放策略**，使 $\lambda$ 随训练步数线性增长：

$$\lambda = \frac{1}{4} \times 10^{-3} \times step + 0.1$$

该调度在训练初期降低扩散损失的权重，让 GAN 梯度主导分布对齐；随着训练推进逐步增强扩散损失，强化轨迹精度。消融实验（Table 2）表明，移除动态缩放会导致 FID 和 IoU 同时下降，验证了该机制对平衡两类损失的关键作用。

### 创新点总结

| 改动维度 | 基线做法 | FlashMotion 做法 | 因果机制 |
|---------|---------|-----------------|---------|
| 生成器步数 | 50 步去噪 | 4 步去噪（FastGenerator） | 大幅减少推理时间，但引入分布不匹配 |
| 适配器优化 | 纯扩散损失 | 扩散+对抗混合损失 | 对抗损失消除模糊，扩散损失保持轨迹精度 |
| 鉴别器 | 无或简单鉴别器 | 扩散鉴别器（SS+TC+VC 注意力分类器） | 多层注意力捕捉视频分布与轨迹一致性 |
| 损失权重 | 固定 λ | 动态线性增长 λ | 平衡初期 GAN 梯度与后期扩散梯度 |

这些创新共同构成了 FlashMotion 的因果旋钮：通过三阶段训练（先训练多步适配器 → 蒸馏少步生成器 → 混合损失微调适配器），使轨迹适配器与少步生成器的不同去噪路径对齐，在保持轨迹控制精度的同时消除少步推理带来的模糊退化。



FlashMotion 的整体训练流程采用三阶段范式（图2），逐步解决将多步轨迹适配器迁移到少步生成器时面临的质量退化与轨迹精度下降问题。其核心瓶颈在于：现有多步轨迹可控视频生成方法（如 MagicMotion、Tora 等）依赖数十步去噪过程，导致大量推理时间冗余；而直接将多步适配器应用于少步生成器或仅用纯扩散损失微调，均会导致显著模糊和轨迹精度下降（图1a–c）。

### 三阶段训练流程

**阶段一：SlowAdapter 训练**  
首先在 SlowGenerator（多步视频生成模型，如 Wan2.2-TI2V-5B 的 50 步去噪版本）上训练轨迹适配器（Trajectory Adapter），采用标准扩散损失进行像素级监督。适配器支持两种架构：ResNet 和 ControlNet。训练采用由密到疏的策略——先使用分割掩码（segmentation masks）作为稠密轨迹条件训练约 4.6K 步，再使用边界框（bounding boxes）进行稀疏条件微调，以逐步增强适配器对轨迹的理解能力。轨迹图经预训练 3D VAE 编码为潜在表示 $Z_{trajectory} \in \mathbb{R}^{\frac{T}{4} \times \frac{H}{16} \times \frac{W}{16} \times 48}$，注入去噪网络。

**阶段二：FastGenerator 蒸馏**  
通过分布匹配蒸馏（DMD）将 SlowGenerator 压缩为仅需 4 步去噪的 FastGenerator。DMD 的核心机制是通过最小化真实分布与生成分布之间的 KL 散度来更新学生生成器：

$$\nabla \mathcal{L}_{\mathrm{DMD}} = \mathbb{E}_{t} \big( \nabla_{\theta} \mathrm{KL}(p_{\mathrm{fake}} \| p_{\mathrm{real}}) \big) = \mathbb{E}_{\epsilon \sim \mathcal{N}(0;I)} \big[ -(s_{\mathrm{real}}(x_t,t) - s_{\mathrm{fake}}(x_t,t)) \frac{d G_{\theta}}{d\theta} \big]$$

同时，假得分模型通过标准扩散损失 $\mathcal{L}_{\mathrm{fake}} = \mathbb{E} \big[ \| \mu_{\mathrm{fake}}(x_t,t) - x_0 \|_2^2 \big]$ 跟踪生成器的输出分布。此阶段得到的 FastGenerator 具备快速生成高质量视频的能力，但尚未适配轨迹控制。

**阶段三：FastAdapter 混合训练**  
这是 FlashMotion 的核心创新。将阶段一训练好的 SlowAdapter 在 FastGenerator 上进行微调，采用结合扩散损失和对抗损失的混合训练策略（图3a）。关键设计包括：

- **扩散鉴别器**：采用从 SlowGenerator 克隆的 DiT 主干网络，并引入基于注意力的分类器。分类器接收 DiT 中间层的多级特征，通过语义自注意力（SS）、轨迹交叉注意力（TC）和视频交叉注意力（VC）三个注意力层来区分真实视频与生成视频（图3b）。
- **对抗训练**：生成器（轨迹适配器）通过 $\mathcal{L}_{\mathcal{G}} = \min_{\theta} \mathbb{E}_{t \sim [0,T]} \big[ f\big( -\mathcal{D}_{\phi}(x_t^{\mathrm{fake}}, t) \big) \big]$ 欺骗鉴别器，鉴别器通过 $\mathcal{L}_{\mathcal{D}}$ 学习区分真伪，强制对齐生成视频与真实视频的分布，弥补纯扩散损失仅提供像素级监督的不足。
- **动态损失缩放**：联合训练损失为 $\mathcal{L} = \mathcal{L}_{\mathcal{G}} + \lambda \mathcal{L}_{diffusion}$，其中 $\lambda$ 采用线性增长调度 $\lambda = \frac{1}{4} \times 10^{-3} \times step + 0.1$，以平衡训练初期占优的扩散梯度与 GAN 梯度，避免模糊并保留轨迹控制。

### 模块关系与数据流

整体架构中，输入为参考图像和轨迹条件（掩码或边界框），经轨迹适配器编码后注入 FastGenerator 的去噪过程。FastGenerator 在 4 步内完成去噪，扩散鉴别器仅在训练阶段用于提供对抗监督。三阶段训练确保了从“多步高质量控制”到“少步高质量控制”的平滑迁移，最终实现 47× 加速的同时保持领先的视觉质量和轨迹精度。

### 补充图表

![[assets/figures/papers/paper_list_l21_https_openaccess_thecvf_com_content_CVPR2026_html_Li_FlashMotion_Few_Ste/figures/003_Figure_2.jpg]]
*Figure 2: Overview of FlashMotion training pipeline. FlashMotion is trained in three stages: (1) a SlowAdapter is first trained on the SlowGenerator with a diffusion loss; (2) a FastGenerator is distilled from the SlowGenerator under the supervision of a distribution matching [65] loss; and (3) the SlowAdapter is finetuned to align with the FastGenerator using a hybrid training strategy that combines adversarial and diffusion losses*



### 整体训练范式

FlashMotion 采用三阶段训练框架（Figure 2）：

1. **阶段一**：在多步去噪生成器（SlowGenerator）上训练轨迹适配器（SlowAdapter），使用标准扩散损失。
2. **阶段二**：通过分布匹配蒸馏将 SlowGenerator 压缩为四步去噪的快速生成器（FastGenerator）。
3. **阶段三**：采用混合训练策略（扩散损失 + 对抗损失）将 SlowAdapter 微调为 FastAdapter，使其对齐 FastGenerator 的不同去噪路径。

---

### 阶段二：FastGenerator 蒸馏

目标是将 SlowGenerator 蒸馏为仅需少量去噪步骤的 FastGenerator。核心机制是 **分布匹配蒸馏（DMD）**，通过最小化生成分布与真实分布之间的 KL 散度来更新学生生成器 $G_\theta$：

$$
\nabla \mathcal{L}_{\mathrm{DMD}} = \mathbb{E}_{t} \big( \nabla_{\theta} \mathrm{KL}(p_{\mathrm{fake}} \| p_{\mathrm{real}}) \big) = \mathbb{E}_{\epsilon \sim \mathcal{N}(0;I)} \big[ -(s_{\mathrm{real}}(x_t,t) - s_{\mathrm{fake}}(x_t,t)) \frac{d G_{\theta}}{d\theta} \big]
$$

其中 $s_{\mathrm{real}}$ 和 $s_{\mathrm{fake}}$ 分别为真实和生成分布的得分模型。为跟踪生成器输出分布的变化，同时训练假得分模型，其损失为标准扩散损失：

$$
\mathcal{L}_{\mathrm{fake}} = \mathbb{E} \big[ \| \mu_{\mathrm{fake}}(x_t,t) - x_0 \|_2^2 \big]
$$

其中 $\mu_{\mathrm{fake}}(x_t,t)$ 为假得分模型预测的去噪结果，$x_0$ 为生成器输出的干净视频。

---

### 阶段三：FastAdapter 混合训练

#### 扩散损失

轨迹适配器的基础监督来自像素级扩散损失，约束生成视频遵循指定轨迹：

$$
\mathcal{L}_{\mathrm{diffusion}} = \| G_{\theta}(x_t, t) - x_0^{\mathrm{real}} \|_2^2
$$

其中 $G_{\theta}$ 为带轨迹适配器的 FastGenerator，$x_0^{\mathrm{real}}$ 为真实视频帧。该损失提供逐像素监督，但单独使用会导致明显模糊（Figure 1c）。

#### 扩散鉴别器与对抗损失

为弥补纯扩散损失仅提供像素级监督的不足，FlashMotion 引入**扩散鉴别器** $\mathcal{D}_{\phi}$（Figure 3b）。鉴别器采用克隆自 SlowGenerator 的 DiT 骨干网络，并将多个中间层特征输入基于注意力的分类器（包含语义自注意力 SS、轨迹交叉注意力 TC、视频交叉注意力 VC 三层），以区分真实视频与生成视频。

生成器（轨迹适配器）的对抗损失为：

$$
\mathcal{L}_{\mathcal{G}} = \min_{\theta} \mathbb{E}_{t \sim [0,T]} \big[ f\big( -\mathcal{D}_{\phi}(x_t^{\mathrm{fake}}, t) \big) \big]
$$

鉴别器的对抗损失为：

$$
\mathcal{L}_{\mathcal{D}} = \min_{\phi} \mathbb{E}_{t \sim [0,T]} \Big[ f\big( -\mathcal{D}_{\phi}(x_t^{\mathrm{real}}, t) \big) + f\big( \mathcal{D}_{\phi}(x_t^{\mathrm{fake}}, t) \big) \Big]
$$

其中 $f$ 为 softplus 函数，$x_t^{\mathrm{fake}}$ 和 $x_t^{\mathrm{real}}$ 分别为生成视频和真实视频在时间步 $t$ 的加噪版本。扩散鉴别器在噪声时间步上操作，与生成器的去噪过程形成对抗，强制对齐生成分布与真实分布，从而消除模糊。

#### 联合训练与动态损失缩放

最终联合训练损失为：

$$
\mathcal{L} = \mathcal{L}_{\mathcal{G}} + \lambda \mathcal{L}_{\mathrm{diffusion}}
$$

关键创新在于**动态扩散损失权重** $\lambda$，随训练步数线性增长：

$$
\lambda = \frac{1}{4} \times 10^{-3} \times step + 0.1
$$

该设计的核心动机：训练初期扩散损失梯度远大于 GAN 损失梯度，若使用固定权重会导致对抗训练失效。动态缩放使初期 $\lambda$ 较小（0.1），让 GAN 梯度主导优化以快速消除模糊；随着训练推进逐步增大 $\lambda$，加强轨迹精度的像素级约束，最终实现视觉质量与轨迹控制的平衡。消融实验（Table 2）证实，移除动态缩放策略会导致 FID 和 IoU 同步退化。

### 补充图表

![[assets/figures/papers/paper_list_l21_https_openaccess_thecvf_com_content_CVPR2026_html_Li_FlashMotion_Few_Ste/figures/004_Figure_3.jpg]]
*Figure 3: (a) Architecture of FlashMotion. The trajectory adapter is finetuned upon the FastGenerator with a hybrid strategy that combines both diffusion and adversarial objectives. (b) Detailed illustration of our diffusion discriminator architecture. The discriminator adopts a DiT backbone cloned from the SlowGenerator, while several intermediate features from its DiT blocks are fed into an attention-based classifier to distinguish real videos from generated ones*



## 实验与关键发现

### 核心瓶颈与实验动机

现有多步轨迹可控视频生成方法（如 **MagicMotion** (Li et al., ICCV 2025)、**Tora** (Zhang et al., CVPR 2025)）依赖 50 步左右的去噪过程，推理时间高达 1500 秒以上。直接将多步适配器（SlowAdapter）应用于少步生成器（FastGenerator）或仅用扩散损失微调，均导致严重质量退化。Figure 1 系统性地展示了这一退化链条：(a) 少步推理下 SlowAdapter+SlowGenerator 产生模糊输出；(b) SlowAdapter 直接用于 FastGenerator 使质量和轨迹精度同时下降；(c) 仅用扩散损失微调适配器仍存在模糊伪影。FlashMotion 通过引入扩散鉴别器和混合训练策略，在 4 步去噪下实现了高质量轨迹可控生成 (Figure 1e)。

![[assets/figures/papers/paper_list_l21_https_openaccess_thecvf_com_content_CVPR2026_html_Li_FlashMotion_Few_Ste/figures/002_Figure_1.jpg]]
*Figure 1: Illustration of the motivation and capabilities of FlashMotion. We define the SlowGenerator as the multi-step video model and the FastGenerator as its few-step distilled version. The SlowAdapter is trained with the SlowGenerator, while the FastAdapter is fine-tuned for the FastGenerator. (a) Using the SlowAdapter with SlowGenerator under few-step inference causes blurry outputs. (b) Applying the SlowAdapter to the FastGenerator degrades both quality and trajectory accuracy. (c) Finetuning the adapter with only diffusion loss still leads to blur artifacts. (d) Finetuning the adapter with existing distillation methods yields suboptimal quality and trajectory control. (e) FlashMotion achieves...*

### 主实验结果

Table 1 汇总了 FlashMotion 在 FlashBench、MagicBench 和 DAVIS 三个基准上的定量表现，涵盖 FID、FVD、Mask IoU 和 Box IoU 四项指标，同时比较 ResNet 和 ControlNet 两种适配器架构。

![[assets/figures/papers/paper_list_l21_https_openaccess_thecvf_com_content_CVPR2026_html_Li_FlashMotion_Few_Ste/figures/005_Table_1.jpg]]
*Table 1: Quantitative results on FlashBench, MagicBench, and DAVIS. We report FID, FVD, and mask/box IoU (%) for both ResNet and ControlNet adapters. For each metric, the best result is highlighted in bold, and the second best is underlined. Denoising time is measured for generating 121 frames on one A100 GPU*

**FlashBench 上的核心指标：**

- **FID**：FlashMotion 以 ControlNet 适配器取得 **14.35**，显著优于所有少步蒸馏基线（LCM、DMD²、APT、APT2）和此前多步 SOTA 方法。
- **FVD**：ControlNet 版本达到 **96.08**，相比移除 GAN 损失后的 >200 降低约 50%。
- **轨迹精度**：Mask IoU 达 **69.15**，Box IoU 达 **75.38**（ControlNet），较移除扩散损失后的 55.91/61.59 提升超过 9 个百分点。
- **推理加速**：生成 121 帧的去噪时间从 MagicMotion 的 1507.6 秒（50 步）降至 **32.2 秒**（4 步），实现 **47× 加速**。

在 MagicBench 和 DAVIS 上，FlashMotion 同样保持最优或次优的 FID/FVD，验证了跨基准的泛化性。定性对比（Figure 4）进一步显示 FlashMotion 在轨迹跟随精度和视觉质量上均优于多步方法和蒸馏基线。

![[assets/figures/papers/paper_list_l21_https_openaccess_thecvf_com_content_CVPR2026_html_Li_FlashMotion_Few_Ste/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative Comparisons results. FlashMotion demonstrates superior qualitative performance, outperforming both previous multi-step trajectory-controllable methods and few-step distillation baselines*

### 消融研究

Table 2 通过逐步移除关键组件，量化了各模块的贡献（以 FlashBench 为基准）：

![[assets/figures/papers/paper_list_l21_https_openaccess_thecvf_com_content_CVPR2026_html_Li_FlashMotion_Few_Ste/figures/008_Table_2.jpg]]
*Table 2: Ablation study of FlashMotion on FlashBench. We analyze both ResNet and ControlNet adapters by progressively removing key components, including the FastAdapter training stage, diffusion loss, GAN loss, and dynamic loss scaling strategy*

**1. FastAdapter 训练阶段（Stage 3）的移除**
移除 FastAdapter 微调阶段，即直接使用 Stage 1 训练好的 SlowAdapter 配合 FastGenerator，导致 ControlNet FID 从 14.35 升至 **19.44**，轨迹 IoU 同步下降。这证实了适配器与少步生成器去噪路径对齐的必要性。

**2. GAN 损失的移除**
仅保留扩散损失时，ControlNet FID 急剧恶化至 **28.82**，FVD 超过 200。这表明纯扩散损失提供的像素级监督无法消除少步去噪引入的模糊，对抗训练对视觉质量起决定性作用。

**3. 扩散损失的移除**
仅用 GAN 损失时，ControlNet Mask IoU 降至 **55.91**，Box IoU 降至 **61.59**。这说明对抗训练虽提升质量，但缺乏像素级约束会导致轨迹精度大幅退化。

**4. 动态损失缩放的移除**
将动态 λ 替换为固定权重，FID 和 IoU 均有明显退化，验证了动态调度（$\lambda = \frac{1}{4} \times 10^{-3} \times step + 0.1$）对平衡初期扩散梯度与 GAN 梯度的关键作用。

Figure 5 提供了上述消融的定性可视化，直观展示移除各组件后的模糊程度和轨迹偏离。

![[assets/figures/papers/paper_list_l21_https_openaccess_thecvf_com_content_CVPR2026_html_Li_FlashMotion_Few_Ste/figures/009_Figure_5.jpg]]
*Figure 5: Ablation studies on the FastAdapter training stage, diffusion loss, GAN loss, and the dynamic loss scaling strategy*

**鉴别器架构消融（Table 3）：**
扩散鉴别器由三个注意力层组成——语义自注意力（SS）、轨迹交叉注意力（TC）、视频交叉注意力（VC）。Table 3 显示完整架构（SS+TC+VC）在所有指标上达到最优，移除任一组件均导致性能下降，其中 TC 对轨迹精度贡献最大，VC 对时序一致性影响显著。

![[assets/figures/papers/paper_list_l21_https_openaccess_thecvf_com_content_CVPR2026_html_Li_FlashMotion_Few_Ste/figures/007_Table_3.jpg]]
*Table 3: Ablation study on the discriminator architecture on FlashBench. VC denotes the Video Cross-Attention layer, SS denotes the Semantic Self-Attention layer, and TC denotes the Trajectory Cross-Attention layer*

### 失败模式与局限性

尽管 FlashMotion 在 FlashBench 上取得 SOTA，论文未系统报告失败案例。根据消融实验可推断以下边界情况需人工验证：
- 移除扩散损失时轨迹精度骤降，暗示在极端复杂轨迹（如多物体交叉、快速方向变化）下，GAN 损失的分布匹配可能不足以维持精确控制。
- 动态 λ 调度基于线性增长，其对不同视频长度和内容类型的普适性未经验证。

### 可推广性问题

论文提出以下待验证方向：
1. FlashMotion 框架能否推广到 Wan2.2 之外的基础模型（如 Sora 类架构）和多类别目标轨迹控制？
2. 动态损失缩放策略在其他对抗训练蒸馏设置中是否同样有效？
3. FlashMotion 对更少步数（2 步）或更多步数（8 步）的适应性如何？

### 公平性说明

所有实验使用相同的基础模型 Wan2.2-TI2V-5B 和 DiffusionPIPE 训练框架，FlashBench 提供了统一的长序列标注，确保比较的公平性。



## 定位与知识库关联

### 多步轨迹可控视频生成基线

FlashMotion 的直接多步基线包括 **MagicMotion**（Li et al., ICCV 2025）、**Tora**（Zhang et al., CVPR 2025）、**LeviTor**（Wang et al., CVPR 2025）、**DragAnything**（Wu et al., ECCV 2024）和 **SG-I2V**（Namekata et al., ICLR 2025）。这些方法均在多步去噪生成器（SlowGenerator，通常需要 50 步）上训练轨迹适配器，以扩散损失为唯一监督信号，在轨迹精度和视觉质量上取得了显著进展。然而，其推理效率受制于大量去噪步骤，例如 MagicMotion 生成 121 帧需 1507.6 秒的去噪时间，这构成了实际部署的核心瓶颈。

### 少步蒸馏方法的适用边界

现有的少步视频蒸馏方法包括 **LCM**（Luo et al., arXiv 2023）、**DMD²**（Yin et al., NeurIPS 2024）、**APT** 和 **APT2**（Lin et al., arXiv 2025）。这些方法专注于将多步生成器蒸馏为少步生成器（FastGenerator），在无条件或文本条件视频生成中实现了显著的加速。但它们在轨迹可控场景下存在两个关键局限：

1. **适配器未对齐**：直接将为 SlowGenerator 训练的 SlowAdapter 应用于 FastGenerator，由于两者的去噪路径存在本质差异，导致轨迹精度显著下降（图 1b）。
2. **纯扩散损失不足**：即使使用扩散损失对适配器进行微调，仍会产生明显的模糊伪影（图 1c），因为扩散损失仅提供像素级监督，无法强制对齐真实和生成视频的分布。

### FlashMotion 的方法定位

FlashMotion 通过三阶段训练范式填补了少步轨迹可控视频生成的空白：

- **阶段一**：在 SlowGenerator 上训练 SlowAdapter，继承 MagicMotion 的 dense-to-sparse 训练策略，从分割掩码逐步过渡到边界框条件，确保轨迹理解能力。
- **阶段二**：采用 DMD 分布匹配框架将 SlowGenerator 蒸馏为 4 步 FastGenerator，通过最小化 KL 散度 $ \nabla \mathcal{L}_{\mathrm{DMD}} = \mathbb{E}_{t} \big( \nabla_{\theta} \mathrm{KL}(p_{\mathrm{fake}} \| p_{\mathrm{real}}) \big) $ 和假得分模型扩散损失 $ \mathcal{L}_{\mathrm{fake}} = \mathbb{E} \big[ \| \mu_{\mathrm{fake}}(x_t,t) - x_0 \|_2^2 \big] $ 实现生成器加速。
- **阶段三**：引入扩散鉴别器进行对抗训练，鉴别器采用从 SlowGenerator 克隆的 DiT 骨干网络，结合语义自注意力（SS）、轨迹交叉注意力（TC）和视频交叉注意力（VC）层构成注意力分类器。混合训练损失 $ \mathcal{L} = \mathcal{L}_{\mathcal{G}} + \lambda \mathcal{L}_{\mathrm{diffusion}} $ 联合优化对抗目标和扩散目标，其中 $ \lambda = \frac{1}{4} \times 10^{-3} \times step + 0.1 $ 为动态线性缩放，用于平衡初期占优的扩散梯度与 GAN 梯度。

### 关键证据与性能边界

在 FlashBench 基准上，FlashMotion 的 ControlNet 变体实现了 FID 14.35、FVD 96.08、Mask IoU 69.15% 和 Box IoU 75.38%，在视觉质量和轨迹精度上均超越了所有少步蒸馏方法和多步基线，同时实现了 47× 的推理加速（去噪时间从 1507.6s 降至 32.2s）。消融实验进一步揭示：

- **移除 FastAdapter 训练阶段**：FID 从 14.35 升至 19.44，IoU 显著下降（Table 2），证明适配器必须与 FastGenerator 的去噪路径对齐。
- **移除 GAN 损失**：FID 飙升至 28.82（Table 2），说明纯扩散损失无法消除模糊，对抗训练是质量保证的关键。
- **移除扩散损失**：Mask IoU 从 69.15% 降至 55.91%（Table 2），表明仅靠对抗损失无法维持轨迹精度，扩散损失的像素级监督不可或缺。
- **鉴别器架构完整性**：完整的 SS+TC+VC 注意力分类器达到最佳 FID/IoU（Table 3），验证了多层级特征对真伪判别的重要性。

### 局限与开放问题

当前分析未涉及 FlashMotion 的显式局限性声明。从方法设计可推断以下开放问题：

1. **基础模型泛化性**：FlashMotion 基于 Wan2.2-TI2V-5B 构建，框架能否推广到其他基础模型和多类别目标尚待验证。
2. **动态损失缩放的普适性**：$ \lambda $ 的线性调度是针对 FlashMotion 的经验设计，其在其他对抗训练蒸馏设置中的适用性需要进一步研究。
3. **步数鲁棒性**：当前仅验证了 4 步推理，对更少步数（2 步）或更多步数（8 步）的适应性未探索。
4. **长序列与复杂轨迹**：FlashBench 提供了长序列标注，但极端遮挡、快速运动和多目标交互场景下的鲁棒性仍需评估。



## 原文 PDF

![[paperPDFs/CVPR_2026/FlashMotion_Few_Step_Controllable_Video_Generation_with_Trajectory_Guidance.pdf]]
