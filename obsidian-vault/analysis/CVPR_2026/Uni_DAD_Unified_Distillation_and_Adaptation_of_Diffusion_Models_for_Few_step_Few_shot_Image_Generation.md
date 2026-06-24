---
title: "Uni-DAD: Unified Distillation and Adaptation of Diffusion Models for Few-step Few-shot Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Uni_DAD_Unified_Distillation_and_Adaptation_of_Diffusion_Models_for_Few_step_Few_shot_Image_Generation.pdf
project_link: null
code_link: null
aliases:
- UD
- Uni-DAD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 双域分布匹配蒸馏（Dual-domain DMD）损失联合多尺度生成对抗网络（Multi-head GAN）损失进行协同优化：源域教师提供稳定的多样性保持信号，目标域教师（可选）促进结构适应，多级特征判别器则抑制过拟合、增强局部细节真实性，权重因子 a 平衡源域与目标域的引导强度。
primary_logic: 将蒸馏与适应统一在单阶段训练框架中，通过双域 DMD 引导生成器同时逼近源分布与目标分布，并利用多尺度对抗训练强化目标域真实感，可在保持源域多样性的前提下，仅用 ≤4 步采样和 ≤10 张目标图像实现高质量、高多样性的个性化生成。
claims:
- Uni-DAD 在 FSIG 基准上以 3 步采样获得了优于非蒸馏方法（≥25 步）的 FID，同时 Intra-LPIPS 保持可比水平。
- 在 SDP 基准上，Uni-DAD 以 1 步采样取得了与 DreamBooth 微调（100 步）相当的身份保持和文本对齐能力，且显著优于其他蒸馏方法。
- 双域 DMD 与多头 GAN 的组合是实现少样本下高质量适应的关键，消融实验中去除任何组件均导致 FID 上升。
- "目标域教师（ϵ^{trg}）的加入显著提升了与源域结构差异较大领域的适应效果，而合理的权重因子 a 可平衡保留与适应。"
---

# Uni-DAD: Unified Distillation and Adaptation of Diffusion Models for Few-step Few-shot Image Generation

> [!tip] 核心洞察
> 将蒸馏与适应统一在单阶段训练框架中，通过双域 DMD 引导生成器同时逼近源分布与目标分布，并利用多尺度对抗训练强化目标域真实感，可在保持源域多样性的前提下，仅用 ≤4 步采样和 ≤10 张目标图像实现高质量、高多样性的个性化生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | Uni-DAD：扩散模型的统一蒸馏与适应用于少步少样本图像生成 |
| 英文题名 | Uni-DAD: Unified Distillation and Adaptation of Diffusion Models for Few-step Few-shot Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.18281) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Uni-DAD |
| Dataset | FSIG, SDP |

> [!tip] 效果简介
> - FSIG (Babies 10-shot) 上，FID 45.09 vs CRDI (48.52) (-3.43)。
> - FSIG (Sunglasses 10-shot) 上，FID 24.45 vs CRDI (24.62) (-0.17)。
> - FSIG (MetFaces 10-shot) 上，FID 58.13 vs FT-DMD2 (63.25) (-5.12)。

## 概述

**问题瓶颈**：在仅给定 ≤10 张目标域图像且要求 ≤4 步采样的约束下，现有方法多采用两阶段流水线——先蒸馏后适应（Distill-then-Adapt）或先适应后蒸馏（Adapt-then-Distill）。然而，蒸馏后的学生模型容易饱和，后续微调难以注入目标域结构；先微调再蒸馏则易导致过拟合，使生成结果过度平滑、纹理缺失，且多样性显著下降。核心矛盾在于：如何在保留源域丰富先验的同时，高效注入目标域的真实结构。

**核心方法**：Uni-DAD 提出**单阶段统一蒸馏与适应框架**，将两阶段流水线压缩为一个协同优化过程。其关键设计包括：
- **双域分布匹配蒸馏（Dual-domain DMD）**：通过加权因子 $a$ 线性组合源域教师 $\epsilon^{\mathrm{src}}$ 和目标域教师 $\epsilon^{\mathrm{trg}}$ 的评分梯度，引导生成器同时逼近源分布与目标分布，在保持多样性的同时实现结构适应。
- **多头生成对抗网络（Multi-head GAN）**：复用假教师编码器的多层特征构建多尺度判别器，在多个特征层级上区分真实样本与生成样本，抑制过拟合并增强局部细节真实性。

**核心洞察**：蒸馏与适应并非必须分阶段执行。通过双域 DMD 提供分布对齐信号、多头 GAN 提供真实感监督，二者协同优化，可在单阶段训练中同时实现快速采样（≤4 步）、高质量生成和高多样性保持。

**主要结果**：
- 在 FSIG 基准上，Uni-DAD 以 3 步采样获得优于非蒸馏方法（≥25 步）的 FID（如 Babies 上 45.09 vs. CRDI 48.52），同时 Intra-LPIPS 保持可比水平。
- 在 SDP 基准上，Uni-DAD 以 1 步采样取得与 DreamBooth 微调（100 步）相当的身份保持和文本对齐能力（DINO 0.47, CLIP-I 0.73, CLIP-T 0.29），显著优于其他蒸馏方法。
- 消融实验证实，双域 DMD 与多头 GAN 的组合是实现少样本高质量适应的关键，去除任一组件均导致 FID 上升。

**方法定位**：Uni-DAD 属于扩散模型蒸馏与少样本领域适应的交叉方向，与 **DMD2** 等分布匹配蒸馏方法、**DreamBooth**（Ruiz et al., CVPR 2023）等主题驱动微调方法、以及 **CRDI**、**DDPM-PA** 等少样本适应方法形成对比。其单阶段统一训练的范式区别于现有的两阶段流水线，为极低步数、极少样本条件下的图像生成提供了新的技术路径。

## 背景与动机

扩散模型在图像生成领域取得了显著进展，但其推理过程通常需要数十甚至上百步去噪采样，计算开销巨大。分布匹配蒸馏（Distribution Matching Distillation, DMD）技术通过将多步教师模型压缩为少步学生模型，有效缓解了这一问题。然而，当面对特定目标域（如特定物体、稀有类别或艺术风格）且仅有极少量样本（≤10 张）可用时，现有方法陷入了两难困境。

**两阶段流水线的结构性缺陷。** 当前的主流方案是将领域适应（Adaptation）与模型蒸馏（Distillation）拆分为两个独立阶段：要么先蒸馏后适应（Distill-then-Adapt），要么先适应后蒸馏（Adapt-then-Distill）。先蒸馏后适应（如 DMD2-FT）首先将源域教师压缩为少步学生，再在目标域上微调该学生，但蒸馏后的学生模型容量有限，微调时容易饱和，难以充分吸收目标域的新结构。先适应后蒸馏（如 FT-DMD2）则先在目标域上微调教师模型，再将其蒸馏为少步学生，但微调后的教师容易过拟合到少量样本，导致蒸馏出的学生继承了这一过拟合倾向，生成结果多样性急剧下降。两种路径均无法在保持源域丰富先验的同时，有效捕获目标域的真实结构。

**核心瓶颈。** 在极少量目标样本（≤10）和极低采样步数（≤4）的双重约束下，现有方法生成的图像往往出现过度平滑、纹理缺失、多样性崩塌等问题。根本原因在于：两阶段流水线将分布匹配与领域适应解耦，使得蒸馏学生要么缺乏目标域结构信息（先蒸馏后适应时适应不足），要么丧失了源域的多样性支撑（先适应后蒸馏时过拟合偏差被蒸馏放大）。此外，现有蒸馏框架（如 DMD2）仅使用源域教师提供分布匹配信号，缺乏来自目标域的直接结构引导，对抗训练也仅采用单头判别器，难以在多尺度特征层面抑制过拟合和增强局部细节真实性。

**本文动机。** 针对上述困境，Uni-DAD 提出将蒸馏与适应统一在单阶段训练框架中，核心思路是：通过双域分布匹配蒸馏（Dual-domain DMD）损失同时引导生成器逼近源域分布与目标域分布，并联合多尺度生成对抗网络（Multi-head GAN）损失进行协同优化。源域教师提供稳定的多样性保持信号，目标域教师促进结构适应，多级特征判别器则抑制过拟合、增强局部细节真实性。这一设计使得模型能够在仅用 ≤4 步采样和 ≤10 张目标图像的条件下，实现高质量、高多样性的个性化生成。

## 核心创新

Uni-DAD 的核心创新在于**将扩散模型的蒸馏与领域适应统一为单阶段训练框架**，并引入**双域分布匹配蒸馏（Dual-domain DMD）**与**多头生成对抗网络（Multi-head GAN）**的协同优化机制，从而在极低采样步数（NFE ≤ 4）和极少目标样本（≤ 10 张）的双重约束下，同时实现高质量与高多样性的目标域生成。

### 1. 从两阶段到单阶段：蒸馏与适应的统一

现有方法普遍采用两阶段流水线：先蒸馏后适应（Distill-then-Adapt，如 **DMD2-FT**）或先适应后蒸馏（Adapt-then-Distill，如 **FT-DMD2**）。这两种策略存在根本性缺陷——蒸馏阶段产生的学生模型在后续微调中容易饱和，而过拟合则导致生成结果过度平滑、纹理缺失、多样性下降，无法同时保留源域丰富先验和目标域真实结构。

Uni-DAD 将蒸馏与适应合并为**单阶段统一训练**（Figure 1），在同一个训练循环中交替更新学生生成器 G、假教师与判别器、目标教师。这一设计消除了阶段间的信息断层，使模型在逼近目标分布的同时持续接收源域教师的多样性保持信号。

### 2. 双域 DMD：源域与目标域的联合分布引导

传统分布匹配蒸馏（DMD）仅将学生分布向源域分布对齐，在少样本适应中缺乏对目标域结构的直接引导。Uni-DAD 提出**双域 DMD**，通过加权因子 $a$ 线性组合源域与目标域的 DMD 梯度：

$$\nabla_{\theta} \mathcal{L}_{\mathrm{DMD}}^{\mathrm{trg+src}} = (1 - a) \nabla_{\theta} \mathcal{L}_{\mathrm{DMD}^{\mathrm{src}}} + a \nabla_{\theta} \mathcal{L}_{\mathrm{DMD}^{\mathrm{trg}}}$$

其中，**冻结的源域教师** $\epsilon^{\mathrm{src}}$ 提供稳定的多样性保持信号，**可选的目标域教师** $\epsilon^{\mathrm{trg}}$（在线训练）促进结构适应。权重因子 $a$ 是关键的因果旋钮：对于与源域相近的目标域（如 Sunglasses），较小 $a$（如 0.25）即可；对于结构差异大的领域（如 MetFaces、Cats），较大 $a$（如 0.75）能显著提升适应效果（Table 1, Figure 4, Figure 9）。

### 3. 多头 GAN：多尺度真实感约束

DMD2 等基线方法使用单头 GAN 或无 GAN，难以在少样本条件下抑制过拟合和增强局部细节。Uni-DAD 引入**多头判别器**，复用假教师 $\epsilon^{\mathrm{fk}}$ 编码器的各层特征，在多个尺度上区分真实样本与生成样本。生成器的对抗损失为：

$$\mathcal{L}_{\mathrm{GAN}}^{G}(\theta) = - \mathbb{E}_{t,z} \sum_{b \in \mathcal{B}} \log \bigl( D_{\theta}^{b}(x_t) \bigr)$$

消融实验（Table 5）表明，多头 GAN 与双域 DMD 的组合是关键：仅使用 GAN 时 FID 为 56.90（Babies），加入源域 DMD 后降至 47.38，再加入目标域 DMD 进一步降至 45.09。单独移除任一组件均导致 FID 显著上升。

### 4. 灵活的初始化与教师配置

Uni-DAD 支持**预蒸馏源模型作为学生初始化**（检查点无关），并可选用**预适应的目标教师**来替代在线训练的 $\epsilon^{\mathrm{trg}}$，从而在无需额外在线训练的情况下进一步提升性能（Table 6：预蒸馏 G + 预适应目标教师在 Babies 上 FID 42.04，MetFaces 上 54.01）。这种灵活性使 Uni-DAD 能够兼容现有的蒸馏或适应成果作为起点。

### 5. 关键创新总结

| 创新维度 | 基线做法 | Uni-DAD 做法 | 证据锚点 |
|---------|---------|-------------|---------|
| 训练阶段 | 两阶段（蒸馏→适应 或 适应→蒸馏） | 单阶段统一训练 | Abstract, Section 1 |
| 分布匹配目标 | 仅源域 DMD | 双域 DMD（源域 + 目标域），权重 $a$ 可调 | Section 3.3, Eq.(5) |
| 对抗训练 | 单头 GAN 或无 GAN | 多头 GAN，多尺度特征判别 | Section 3.5 |
| 目标域教师 | 无或仅用于微调 | 在线目标教师（可选，可替换为预适应模型） | Section 3.4, Table 6 |
| 学生初始化 | 随机或源教师蒸馏 | 支持预蒸馏源模型初始化 | Section 1, Table 6 |

这些创新协同作用，使 Uni-DAD 在 FSIG 基准上以 **3 步采样**获得了优于非蒸馏方法（≥ 25 步）的 FID（Table 1），在 SDP 基准上以 **1 步采样**取得了与 DreamBooth 微调（100 步）相当的身份保持和文本对齐能力（Table 3, Figure 6），同时将 5K 样本的推理时间从 35 分钟降至 **4.2 分钟**，TFLOPs/img 从 55.7 降至 **2.2**（Table 2）。

## 整体框架

Uni-DAD 将扩散模型的蒸馏与领域适应统一在一个单阶段训练框架中，核心目标是仅用 ≤4 步采样和 ≤10 张目标域图像，实现高质量、高多样性的个性化生成。其整体 pipeline 围绕三个关键模块的交替更新展开，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l950_https_arxiv_org_abs_2511_18281/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Uni-DAD for few-step and few-shot image generation. A (frozen) source teacher ϵsrc is adapted and distilled into a student G for fast sampling*

### 模块构成与角色

框架包含以下核心模块：

- **冻结源域教师 $ \epsilon^{\mathrm{src}} $**：基于大规模源域数据预训练的扩散模型，在训练中保持冻结，通过其评分函数 $ \nabla_x \log p^{\mathrm{src}}(x) $ 为学生生成器提供源域分布的多样性保持信号。
- **学生生成器 $ G_\theta $**：从噪声直接生成目标域图像，采样步数控制在 $ 1 \leq \mathrm{NFE} \leq 4 $，是蒸馏与适应的最终产物。
- **在线目标域教师 $ \epsilon^{\mathrm{trg}} $**（可选）：在少量目标域真实样本上持续更新，提供目标域评分以促进结构适应。当目标域与源域结构差异较大时，该模块的作用尤为关键。
- **假教师 $ \epsilon^{\mathrm{fk}} $**：初始化为源教师权重，持续跟踪学生生成分布的变化，为双域 DMD 损失提供梯度，同时其编码器各层特征被多头判别器复用。
- **多头判别器 $ D $**：附加在假教师编码器之上，在多个特征尺度上区分真实目标域样本与学生生成样本，通过对抗训练抑制过拟合、增强局部细节真实性。

### 训练循环

每次训练迭代中，Uni-DAD 交替执行三类更新（Algorithm 1）：

1. **学生更新**：优化生成器 $ G_\theta $，损失函数为双域 DMD 损失与多头 GAN 生成器损失的加权组合：
   $$ \mathcal{L}_G(\theta) = \mathcal{L}_{\mathrm{DMD}}^{\mathrm{trg+src}}(\theta) + \lambda_{\mathrm{GAN}}^G \mathcal{L}_{\mathrm{GAN}}^G(\theta) $$
   其中双域 DMD 梯度通过权重因子 $ a $ 线性组合源域与目标域的分布匹配信号：
   $$ \nabla_\theta \mathcal{L}_{\mathrm{DMD}}^{\mathrm{trg+src}} = (1 - a) \nabla_\theta \mathcal{L}_{\mathrm{DMD}^{\mathrm{src}}} + a \nabla_\theta \mathcal{L}_{\mathrm{DMD}^{\mathrm{trg}}} $$

2. **假教师与判别器更新**：更新 $ \epsilon^{\mathrm{fk}} $ 和 $ D $，损失函数为假教师的去噪 MSE 损失与判别器对抗损失的加权和。该更新在每次迭代中执行 5–10 次，以确保判别器能有效跟踪学生生成分布的变化。

3. **目标教师更新**：在目标域真实样本上最小化去噪 MSE 损失，使 $ \epsilon^{\mathrm{trg}} $ 逐步逼近目标域分布的去噪过程。

### 关键设计要点

- **单阶段统一**：与两阶段流水线（先蒸馏后适应或先适应后蒸馏）不同，Uni-DAD 在单一训练过程中同时完成蒸馏与适应，避免了蒸馏学生饱和或过拟合导致的纹理缺失与多样性下降。
- **双域 DMD 引导**：同时利用源域教师和目标域教师（可选）的评分信号，通过权重因子 $ a $ 平衡源域先验保留与目标域结构适应。对于相近领域取较小 $ a $（如 $ a=0.25 $），对于遥远领域取较大 $ a $（如 $ a=0.75 $）。
- **多头 GAN 增强**：复用假教师编码器各层特征进行多尺度判别，相比单头 GAN 或无 GAN 的设置，能更有效地抑制过拟合、提升目标域真实感。消融实验（Table 5）表明，多头 GAN 与双域 DMD 的组合是实现少样本高质量适应的关键。

### 补充图表

![[assets/figures/papers/paper_list_l950_https_arxiv_org_abs_2511_18281/figures/001_Figure_1.jpg]]
*Figure 1: Uni-DAD (Distill & Adapt) vs. two-stage pipelines, Distill-then-Adapt , and Adapt-then-Distill Adapt is performed by fine-tuning, and Distill by DMD2 [48]. The source domain is represented by 70K diverse faces, and the target domain by 10 babies. Sampling steps are reduced from 25 to 3*

## 核心模块与公式推导

Uni-DAD 的训练框架由五个核心模块与三个交替更新的损失函数构成，其设计目标是在单阶段训练中同时完成分布蒸馏与领域适应。

### 模块职责

**冻结源域教师 $\epsilon^{\mathrm{src}}$**：提供源域评分函数 $\nabla_x \log p^{\mathrm{src}}(x)$，在训练期间保持冻结，为生成器提供稳定的多样性保持信号。

**在线目标域教师 $\epsilon^{\mathrm{trg}}$**：从少量目标域样本中学习目标分布的去噪过程，为生成器提供结构适应引导。该模块为可选组件，在源域与目标域结构差异较大时作用显著。

**假教师 $\epsilon^{\mathrm{fk}}$**：跟踪学生生成器的演化分布。其参数 $\phi$ 初始化为 $\epsilon^{\mathrm{src}}$ 的权重，并在学生生成样本上通过均方误差持续更新：

$$
\mathcal{L}_{\mathrm{fk}}(\phi) = \mathbb{E}_{t,z} \Big[ \big\| \epsilon^{\mathrm{fk}}_{\phi}(x_t) - \epsilon \big\|_2^2 \Big] \tag{6}
$$

其中 $x_t$ 为对学生生成样本加噪后的结果，$\epsilon$ 为注入的标准高斯噪声。

**多头判别器 $D$**：附加于假教师编码器之上，复用其各层特征进行多尺度真伪判别。判别器在多个特征层级上区分真实目标样本与生成样本，从而强化局部细节的真实感。

**学生生成器 $G$**：从噪声 $z$ 直接生成目标域图像，推理时仅需 $\leq 4$ 个去噪步数（NFE）。

### 核心损失函数

**双域 DMD 损失**：Uni-DAD 的核心创新在于将分布匹配蒸馏（DMD）的目标从单一源域扩展为源域与目标域的双域联合。DMD 的基本梯度形式为：

$$
\nabla_{\theta} \mathcal{L}_{\mathrm{DMD}} = \mathbb{E}_{z} \big[ (\nabla_x \log p^{\mathrm{fk}}(x) - \nabla_x \log p^{\mathrm{src}}(x)) \frac{d G_{\theta}}{d \theta} \big] \tag{2}
$$

该梯度通过最小化学生分布 $p^{\mathrm{fk}}$ 与源分布 $p^{\mathrm{src}}$ 之间的 KL 散度来更新生成器参数。Uni-DAD 将其扩展为双域加权形式：

$$
\nabla_{\theta} \mathcal{L}_{\mathrm{DMD}}^{\mathrm{trg+src}} = (1 - a) \nabla_{\theta} \mathcal{L}_{\mathrm{DMD}^{\mathrm{src}}} + a \nabla_{\theta} \mathcal{L}_{\mathrm{DMD}^{\mathrm{trg}}} \tag{5}
$$

其中 $a \in [0,1]$ 为平衡因子，控制目标域引导的强度：当源域与目标域相近时取较小值（如 $a=0.25$），以保留源域多样性；当领域差距较大时取较大值（如 $a=0.75$），以促进结构适应。

**多头 GAN 损失**：生成器的对抗损失定义为：

$$
\mathcal{L}_{\mathrm{GAN}}^{G}(\theta) = - \mathbb{E}_{t,z} \sum_{b \in \mathcal{B}} \log \big( D_{\theta}^{b}(x_t) \big) \tag{8}
$$

其中 $\mathcal{B}$ 为假教师编码器的多个特征层索引集合，$D_{\theta}^{b}$ 为第 $b$ 层的判别器输出。该设计使判别信号覆盖从浅层纹理到深层语义的多级特征，有效抑制单头 GAN 在少样本下易出现的过拟合问题。

**学生总损失**：生成器的最终训练目标为双域 DMD 损失与多头 GAN 损失的加权组合：

$$
\mathcal{L}_{G}(\theta) = \mathcal{L}_{\mathrm{DMD}}^{\mathrm{trg+src}}(\theta) + \lambda_{\mathrm{GAN}}^{G} \mathcal{L}_{\mathrm{GAN}}^{G}(\theta) \tag{10}
$$

### 训练流程

每次迭代交替执行三类更新（见 Algorithm 1）：
1. **学生更新**：最小化 $\mathcal{L}_G$，同时接收源域教师与目标域教师的评分引导及多头判别器的对抗梯度。
2. **假教师与判别器更新**：最小化 $\mathcal{L}_{\mathrm{fk}} + \lambda_{\mathrm{GAN}}^{D} \mathcal{L}_{\mathrm{GAN}}^{D}$，该更新每轮执行 5–10 次以保证判别器充分收敛。
3. **目标教师更新**：在目标域真实样本上最小化标准 DDPM 去噪损失：

$$
\mathcal{L}_{\mathrm{trg}}(\eta) = \mathbb{E}_{t,\epsilon,y} \Big[ \big\| \epsilon_{\eta}^{\mathrm{trg}}(y_t) - \epsilon \big\|_2^2 \Big] \tag{7}
$$

其中 $y$ 为目标域真实图像，$y_t$ 为其加噪版本。

### 补充图表

![[assets/figures/papers/paper_list_l950_https_arxiv_org_abs_2511_18281/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative ablation of the dual-domain DMD weighting factor a for FSIG on Babies and MetFaces. See Fig. 9 for SDP*

![[assets/figures/papers/paper_list_l950_https_arxiv_org_abs_2511_18281/figures/016_Figure_9.jpg]]
*Figure 9: Qualitative ablation of the dual-domain DMD weighting factor a for SDP across prompts on a live subject and an object*

## 实验与分析

### 实验设置

Uni-DAD 在两个核心基准上进行评估：**少样本图像生成（FSIG）** 和 **主题驱动个性化生成（SDP）**。FSIG 任务以在 FFHQ 上预训练的 DDPM 为源模型，在 Babies、Sunglasses、MetFaces、Cats 四个 10-shot 目标集上进行适应；SDP 任务以 Stable Diffusion v1.5 为骨干，在 DreamBooth 基准的 30 个主体上评估。所有实验均将采样步数压缩至 NFE ≤ 4，与使用 25–100 步的非蒸馏方法及两阶段蒸馏流水线进行对比。

### 主实验结果

#### FSIG：少样本图像生成

Table 1 汇总了 FSIG 任务上的定量结果。Uni-DAD 以仅 3 步采样（NFE=3）在 Babies 上取得 FID 45.09，优于非蒸馏方法 CRDI（48.52）和 DDPM-PA（49.91），同时 Intra-LPIPS 保持 0.46 的可比多样性水平。在 Sunglasses 上，FID 24.45 与 CRDI（24.62）持平。在源域与目标域结构差异较大的 MetFaces 上，Uni-DAD 的 FID 58.13 显著优于两阶段蒸馏-适应方法 FT-DMD2（63.25）和 DMD2-FT（69.41），验证了单阶段统一训练在抑制过拟合方面的优势。Cats 数据集上 FT-DMD2 的 FID（51.85）略优于 Uni-DAD（55.32），但作者指出通过加入目标域教师可进一步改善。

![[assets/figures/papers/paper_list_l950_https_arxiv_org_abs_2511_18281/figures/006_Table_1.jpg]]
*Table 1: Comparison of FID↓ and Intra-LPIPS↑ for FSIG across methods and 10-shot target sets. Bold indicates best result among distilled variants. Underline indicates best result among all models*

Table 2 的计算开销分析显示，Uni-DAD 的推理效率优势显著：生成 5K 样本仅需 4.2 分钟，而直接微调（FT）需要 35 分钟；每张图像的 TFLOPs 从 55.7 降至 2.2，加速比超过 25 倍。

![[assets/figures/papers/paper_list_l950_https_arxiv_org_abs_2511_18281/figures/007_Table_2.jpg]]
*Table 2: Training and test-time computational cost analysis for FSIG. Mem: memory. h: hour, m: minute*

#### SDP：主题驱动个性化生成

Table 3 展示了 SDP 任务的定量对比。Uni-DAD 在 NFE=1 的条件下取得 DINO 0.47、CLIP-I 0.73、CLIP-T 0.29，在身份保持和文本对齐能力上显著优于 DMD2-FT（DINO 0.20, CLIP-I 0.60, CLIP-T 0.23），并与使用 100 步采样的 DreamBooth 微调（DINO 0.50, CLIP-I 0.74, CLIP-T 0.30）表现相当。值得注意的是，PSO（Turbo-PSO）使用了 SDXL 骨干和 1024×1024 分辨率，与 Uni-DAD（SDv1.5, 512×512）存在骨干和分辨率的不公平优势，直接比较需谨慎。

![[assets/figures/papers/paper_list_l950_https_arxiv_org_abs_2511_18281/figures/009_Table_3.jpg]]
*Table 3: Comparison of quality (DINO↑, CLIP-I↑, CLIP-T↑) and diversity (Intra-LPIPS↑, Inter-LPIPS↑) for SDP across methods, evaluated on the DreamBooth benchmark (30 subjects, 25 prompts) [34]. Best and second best distilled method at NFE=1*

Figure 6 的定性对比进一步印证：Uni-DAD 在配饰添加和场景重构等提示下，生成结果保持了目标主体的身份特征，同时保留了源域丰富的纹理和背景多样性，而 DMD2-FT 和 FT-DMD2 两阶段方法则出现了明显的过平滑和身份丢失。

![[assets/figures/papers/paper_list_l950_https_arxiv_org_abs_2511_18281/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative comparison for SDP, adapting SDV1.5 [33] to the DreamBooth [34] cat2 subject, evaluated on accessorization and re-contextualization prompts. See additional results on other subjects (dog6, vase) and prompts in Fig. 12. Zoom in for details*

### 消融实验

#### NFE 与目标集大小

Table 4 的消融显示，NFE 从 1 增加到 3 持续改善 FID（Babies 上从 98.52 降至 45.09），但 NFE=4 时收益趋平。在 1-shot 和 5-shot 的极端少样本条件下，Uni-DAD 仍能保持合理的生成质量，但 FID 随样本数减少而上升，表明对极少量样本的适应仍存在挑战。

![[assets/figures/papers/paper_list_l950_https_arxiv_org_abs_2511_18281/figures/011_Table_4.jpg]]
*Table 4: Ablation on target set sizes and NFE, evaluated by FID↓. B: Babies, M: MetFaces. Bold indicates best result. Selected variant for main results is in gray*

#### 组件分析

Table 5 的组件消融揭示了各模块的贡献机制：

![[assets/figures/papers/paper_list_l950_https_arxiv_org_abs_2511_18281/figures/012_Table_5.jpg]]
*Table 5: Component analysis evaluated by FID↓. Mh: Multihead, Sh: Single-head, B: Babies, M: MetFaces. Bold indicates best result. Selected variants for main results are in gray*

- **仅使用多头 GAN**（无 DMD）：Babies 上 FID 56.90，表明对抗训练单独使用时缺乏足够的分布对齐能力。
- **加入源域 DMD**（DMD^{src} + GAN^{Mh}）：FID 降至 47.38，源教师提供的多样性保持信号是关键。
- **再加入目标域 DMD**（完整 Uni-DAD）：FID 进一步降至 45.09，目标域教师的加入促进了结构适应。
- **单头 GAN 替代多头 GAN**：FID 从 45.09 升至 46.24（Babies），验证了多尺度特征判别的有效性。

#### 权重因子 a

Figure 4 和 Figure 9 展示了双域 DMD 中权重因子 a 的定性影响。对于与源域相近的目标域（如 Babies），较小的 a=0.25 即可在保留源域多样性的同时完成适应；对于差异较大的领域（如 MetFaces），a=0.75 能更有效地促进目标结构的学习。在 SDP 任务中，a=0.75 整体表现良好。

#### 初始化策略

Table 6 探索了不同初始化检查点的效果。使用预蒸馏学生（G）和预适应目标教师（ϵ^{trg}）的组合在 Babies 上取得 FID 42.04，在 MetFaces 上取得 54.01，均优于在线训练版本，表明预训练组件可作为即插即用的性能增强手段。

![[assets/figures/papers/paper_list_l950_https_arxiv_org_abs_2511_18281/figures/013_Table_6.jpg]]
*Table 6: Available checkpoints at the start of training and FID↓. G is distilled via DMD2 [48] and*

#### GAN 损失函数

Table 7 对比了不同 GAN 损失函数在多头设置下的表现。二元交叉熵（BCE）在 Babies 上 FID 45.09，优于 Hinge（47.80）、LSGAN（46.31）和 WGAN（46.89），且训练过程更稳定。

![[assets/figures/papers/paper_list_l950_https_arxiv_org_abs_2511_18281/figures/014_Table_7.jpg]]
*Table 7: Ablation of GAN losses evaluated on FID↓. Bold indicates best result. Selected variant for main results is in gray*

### 公平性说明

需注意以下公平性限制：DDPM-PA 未提供公开代码，仅引用其原始报告结果；CRDI 在 MetFaces 上的复现 FID 为 121.36，与原文报告的 94.86 存在显著差异；PSO 使用 SDXL 骨干和更高分辨率，与 Uni-DAD 的 SDv1.5 骨干不直接可比。

### 失败模式与局限性

在结构差异极大的目标域上，Uni-DAD 可能牺牲一定多样性以换取更好的结构适应。在线目标教师训练增加了约 21% 的峰值显存占用。当目标域与源域差距较大时，权重因子 a 需仔细手动调节，缺乏自适应机制。目前仅在 DDPM 和 SDv1.5 两个骨干上验证，扩展到更大模型及视频、音频等模态尚未探索。

## 方法谱系与知识库定位

### 问题定位：蒸馏与适应的两阶段困境

在少样本图像生成（FSIG）和主题驱动个性化生成（SDP）任务中，现有方法普遍采用**两阶段流水线**：先蒸馏后适应（Distill-then-Adapt）或先适应后蒸馏（Adapt-then-Distill）。前者先用 DMD2 将扩散模型蒸馏为少步学生，再在目标域上微调；后者先在目标域上微调扩散模型，再用 DMD2 蒸馏为少步学生。这两种流水线面临一个共同瓶颈：**蒸馏后的学生模型容量有限，在后续微调中容易饱和或过拟合**，导致生成结果过度平滑、纹理缺失、多样性下降，无法同时保留源域丰富先验和目标域真实结构。尤其在目标样本极少（≤10 张）和采样步数极低（≤4 步）的约束下，这一矛盾更为突出。

### 方法谱系对比

Uni-DAD 的核心创新在于将蒸馏与适应**统一为单阶段训练框架**，通过双域分布匹配蒸馏（Dual-domain DMD）和多头生成对抗网络（Multi-head GAN）的协同优化，同时逼近源分布与目标分布。下表梳理了 Uni-DAD 与主要基线方法在关键设计维度上的差异：

| 方法 | 阶段 | 分布匹配目标 | 对抗训练 | 目标域教师 | 采样步数 |
|------|------|-------------|---------|-----------|---------|
| **DDPM-PA** | 单阶段适应 | 无蒸馏 | 无 | 无 | ≥25 |
| **CRDI** | 单阶段适应 | 无蒸馏 | 无 | 无 | ≥25 |
| **FT（直接微调）** | 单阶段适应 | 无蒸馏 | 无 | 无 | ≥25 |
| **DMD2-FT** | 先蒸馏后适应 | 仅源域（DMD） | 单头 GAN | 无 | ≤4 |
| **FT-DMD2** | 先适应后蒸馏 | 仅源域（DMD） | 单头 GAN | 无 | ≤4 |
| **DreamBooth**（Ruiz et al., CVPR 2023） | 单阶段适应 | 无蒸馏 | 无 | 无 | ≥50 |
| **PSO (Turbo-PSO)** | 蒸馏后适应 | 仅源域 | 无 | 无 | ≤4 |
| **Uni-DAD** | **单阶段统一** | **双域（源+目标）** | **多头 GAN** | **在线可选** | ≤4 |

**关键设计差异的机理分析**：

1. **蒸馏与适应的阶段统一**：两阶段方法在蒸馏后微调时，学生模型已处于低容量状态，微调容易破坏蒸馏阶段学到的源域多样性。Uni-DAD 在单阶段训练中同时进行分布匹配和对抗适应，避免了这一信息损失。

2. **双域 DMD 的对齐目标**：DMD2 等单域蒸馏方法仅将学生分布向源域对齐，缺乏对目标域结构的显式引导。Uni-DAD 通过加权因子 $a$ 线性组合源域 DMD 梯度与目标域 DMD 梯度（式 5），使生成器同时逼近两个分布的交集区域。当 $a=0.25$ 时适合源-目标相近领域，$a=0.75$ 时适合结构差异较大的领域。

3. **多头 GAN 的判别架构**：DMD2 使用单头判别器，仅在最终输出层进行真假判别。Uni-DAD 复用假教师编码器的各层特征，在多个尺度上进行判别（式 8），有效抑制过拟合、增强局部细节真实性。消融实验（Table 5）显示，多头 GAN 与 DMD 结合使用比单独使用 GAN 或 DMD 更有效：仅 GAN 在 Babies 上 FID 为 56.90，加入 DMD^src 和 GAN^Mh 后降至 47.38，再加入 DMD^trg 进一步降至 45.09。

4. **目标域教师的在线使用**：两阶段方法中目标域信息仅通过微调注入。Uni-DAD 引入可选的在线目标教师 $\epsilon^{trg}$，通过式 7 在目标域真实样本上训练，为双域 DMD 提供目标分布评分。在 MetFaces 和 Cats 等与源域结构差异较大的领域，目标教师的加入显著提升了适应效果（Table 1）。

### 适用边界与局限

**已验证的有效范围**：
- 扩散骨干：DDPM（FSIG 任务）和 SDv1.5（SDP 任务），分辨率 512×512
- 目标样本量：1-shot 至 10-shot（Table 4 显示 5-shot 以上性能趋于稳定）
- 采样步数：1–4 NFE（NFE=3 为性价比最优，NFE=4 收益趋平）
- 任务类型：少样本域适应（FSIG）和主题驱动个性化生成（SDP）

**已知局限**：
1. **结构差异与多样性的权衡**：在结构差异极大的目标域（如 FFHQ→MetFaces）上，Uni-DAD 可能牺牲一定多样性以换取更好的结构适应。Table 1 中 Cats 上 FT-DMD2 的 FID（51.85）略优于 Uni-DAD（55.32），说明在特定领域差距下两阶段方法仍有竞争力。
2. **显存开销**：在线目标教师训练增加了约 21% 的峰值显存占用，限制了在资源受限场景下的部署。
3. **权重因子 $a$ 的手动调节**：$a$ 系数对源-目标领域差距敏感，目前缺乏自适应选择机制，需要根据领域特性手动调节。
4. **骨干模型覆盖有限**：仅验证了 DDPM 和 SDv1.5 两个骨干，尚未扩展到 SDXL、SD3、Flux 等更大规模模型，也未探索视频、音频等模态。

**公平性注意事项**：
- PSO (Turbo-PSO) 使用 SDXL 骨干和 1024×1024 分辨率，与 Uni-DAD（SDv1.5，512×512）存在骨干和分辨率的不公平优势，直接比较需谨慎。
- CRDI 在 MetFaces 上的 FID 结果无法复现（本文复现值 121.36 vs 原文 94.86），该基线的对比结论需要人工核验。
- DDPM-PA 未提供公开代码，其对比结果仅直接引用原始报告。

### 开放问题与后续方向

1. **参数效率改进**：能否设计参数高效的 Uni-DAD 变体（如 LoRA 适配、部分层蒸馏）以降低显存和训练开销，使其更适用于消费级 GPU？
2. **自适应权重机制**：如何自动选择权重因子 $a$ 以适应任意领域差距？可能的思路包括基于领域差距度量（如 FID 距离）的动态调节或元学习策略。
3. **多概念与风格适应**：Uni-DAD 是否适用于更开放式的文本到图像生成任务，例如同时适应多个概念或风格？这需要扩展双域 DMD 到多域分布匹配。
4. **大规模模型验证**：在 SD3、Flux 等更大规模扩散模型上训练并评估 Uni-DAD 的性能，验证方法的可扩展性。
5. **极端少样本稳定性**：单阶段训练是否会对极端少样本（1-shot）或极低 NFE（1-step）下的生成带来不稳定性？Table 4 显示 NFE=1 时 FID 显著升高（Babies 上 98.52），需要进一步分析失效模式。

## 原文 PDF

![[paperPDFs/CVPR_2026/Uni_DAD_Unified_Distillation_and_Adaptation_of_Diffusion_Models_for_Few_step_Few_shot_Image_Generation.pdf]]