---
title: Towards Detailed Text-to-Motion Synthesis via Basic-to-Advanced Hierarchical Diffusion Model
type: paper
paper_level: A
venue: AAAI
year: 2024
pdf_ref: paperPDFs/AAAI_2024/B2A_HDM_Towards_Detailed_Text_to_Motion_Synthesis_via_Basic_to_Advanced_Hierarchical_Diffusion_Model.pdf
aliases:
- BHBAHDM
- TDTMSBAHDM
tags:
- AAAI_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将去噪过程分解为低维空间的“基本扩散”（确保文本-动作对齐）和高维空间的“高级扩散”（进行细节增强），并在高级扩散中采用多个去噪器分别负责不同时间间隔，从而在不牺牲一致性的前提下提升细节。
primary_logic: 利用低维和高维潜在空间的互补优势：低维空间简化分布以学习跨模态映射，高维空间提供表达能力以保留细节；通过时间步分割和多去噪器框架，使两个模型协同工作。
claims:
- 低维潜在空间VAE重建的动作细节缺失，FID随维度降低而升高，但低维扩散模型的R-Precision明显优于高维扩散模型。
- B2A-HDM在HumanML3D数据集上同时获得最低FID（0.084）和最高Top-1 R-Precision（0.511），优于所有基线方法。
- 消融实验表明，使用2个高级去噪器且高级扩散率≥95%时，B2A-HDM的FID显著优于单一去噪器配置，验证了多去噪器框架的有效性。
- HumanML3D 上 FID↓ = 0.084
---

# Towards Detailed Text-to-Motion Synthesis via Basic-to-Advanced Hierarchical Diffusion Model

> [!tip] 核心洞察
> 利用低维和高维潜在空间的互补优势：低维空间简化分布以学习跨模态映射，高维空间提供表达能力以保留细节；通过时间步分割和多去噪器框架，使两个模型协同工作。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于基础到高级层次扩散模型的详细文本到动作合成 |
| 英文题名 | Towards Detailed Text-to-Motion Synthesis via Basic-to-Advanced Hierarchical Diffusion Model |
| 会议/期刊 | AAAI 2024 |
| Links | [Code](https://github.com/xiezhy6/B2A-HDM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | B2A-HDM (Basic-to-Advanced Hierarchical Diffusion Model) |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，FID↓ 0.084 vs 0.116 (T2M-GPT) (-0.032)；Top-1 R-Precision↑ 0.511 vs 0.491 (MotionDiffuse / T2M-GPT) (+0.020)。
> - KIT-ML 上，FID↓ 0.367 vs 0.404 (MLD) (-0.037)；Top-1 R-Precision↑ 0.436 vs 0.417 (MotionDiffuse) (+0.019)。

## 概述

文本到动作（Text-to-Motion）生成的核心瓶颈在于：低维潜在扩散模型（如 **MLD**, Chen et al., CVPR 2023）虽然易于训练且有利于跨模态对齐，但其潜在表示的容量不足导致生成的动作细节严重缺失；而直接在高维原始数据空间扩散（如 **MDM**, Tevet et al., ICCV 2023）则因数据分布复杂、训练样本有限而损害模态一致性。

**B2A-HDM**（Basic-to-Advanced Hierarchical Diffusion Model）针对上述矛盾提出了一个层次化解耦方案：将去噪过程显式分解为低维空间中的**基本扩散**（Basic Diffusion）与高维空间中的**高级扩散**（Advanced Diffusion）两个阶段。基本扩散模型在低维潜在空间（4×256）中确保文本-动作的语义对齐，提供模态一致的中间结果；高级扩散模型则在高维潜在空间（8×256）中采用多个去噪器分阶段进行细节增强，从而在不牺牲一致性的前提下显著提升动作的精细度。

实验表明，B2A-HDM在HumanML3D数据集上同时取得了最优的FID（0.084）和Top-1 R-Precision（0.511），在KIT-ML数据集上同样以FID 0.367和Top-1 R-Precision 0.436达到领先水平，验证了低维与高维空间互补协同的有效性。

## 背景与动机

**文本到动作生成**（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的3D人体动作序列，在动画制作、虚拟人交互、游戏开发等领域具有广泛应用。该任务的核心挑战在于同时满足两个相互制约的目标：**模态一致性**（生成的语义与文本描述精确对齐）和**动作细节保真度**（生成的序列包含丰富、自然的关节运动细节）。

### 现有方法的瓶颈

当前主流方法大致分为两类，但各自存在结构性缺陷：

**1. 原始数据空间扩散模型**（如 **MDM**（Tevet et al., ICCV 2023）、**MotionDiffuse**（Zhang et al., CVPR 2022））直接在关节位置或旋转的高维原始表示上执行扩散过程。这类方法虽然保留了完整的动作细节表达能力，但由于高维数据分布高度复杂且训练数据有限，扩散模型难以精确学习从文本到动作的跨模态映射，导致**模态一致性受损**。

**2. 低维潜在扩散模型**（如 **MLD**（Chen et al., CVPR 2023））将动作编码到紧凑的潜在空间后再进行扩散。低维空间显著简化了数据分布，使扩散模型更容易学习文本-动作对齐，从而获得优异的跨模态一致性。然而，这种压缩以**牺牲动作细节**为代价——低维潜在表示容量不足，VAE重建过程中会丢失微妙的关节运动、手部姿态等精细信息。

### 核心矛盾与实证证据

本文通过系统实验揭示了上述矛盾：如图2(b)(c)所示，随着VAE潜在空间维度降低，重建动作的FID持续升高（细节损失加剧），但低维扩散模型的Top-1 R-Precision却明显优于高维扩散模型。这一现象直接验证了核心瓶颈——**低维空间有利于跨模态映射学习，但容量不足以承载细节；高维空间具备细节表达能力，但分布复杂导致对齐困难**。现有方法无法同时兼顾两者。

### 本文动机与核心思路

针对上述瓶颈，B2A-HDM的动机在于**协同利用低维与高维潜在空间的互补优势**：将去噪过程分解为两个阶段——在低维空间执行“基本扩散”以确保文本-动作语义对齐，随后过渡到高维空间执行“高级扩散”以进行细节增强。通过这种分而治之的策略，模型在保持模态一致性的前提下，显著提升生成动作的细节质量。

## 核心创新

B2A-HDM 的核心创新在于**将文本到动作的扩散去噪过程显式分解为低维空间的基本扩散（BDM）与高维空间的高级扩散（ADM）两个协同层级**，从而在保持模态一致性的同时实现细节增强。该方法从根本上改变了传统单一空间扩散模型的去噪分工方式。

### 双层扩散空间的协同机制

传统潜在扩散模型（如 **MLD**，Chen et al., CVPR 2023）仅在单一低维潜在空间（如 4×256）中执行完整去噪过程。虽然低维空间通过简化数据分布降低了跨模态映射的学习难度，但潜在表示容量不足导致生成的动作细节严重缺失——这一瓶颈在 VAE 重建实验中得到了明确验证：随着潜在维度降低，重建动作的 FID 显著升高（Fig. 2(b)），而低维扩散模型的 R-Precision 却明显优于高维扩散模型（Fig. 2(c)），揭示了“一致性”与“细节”之间的根本性冲突。

B2A-HDM 的关键洞察是**利用低维与高维潜在空间的互补优势**：BDM 在低维空间（4×256）执行前 $T_l$ 步去噪，提供文本一致的中间结果；随后通过解码-重新编码操作将中间结果映射到高维空间（8×256），由 ADM 执行剩余的 $T_h$ 步去噪进行细节增强。这一分工使得两个模型各司其职——BDM 专注于跨模态对齐，ADM 专注于细节生成，而非让单一模型在表达力与一致性之间妥协。

### 多去噪器分阶段框架

ADM 的另一项关键设计是**采用多个去噪器分别负责不同时间间隔的去噪子过程**，而非使用单一去噪器处理完整的高维扩散阶段。具体而言，ADM 包含两个去噪器 $\epsilon_\theta^{h1}$ 和 $\epsilon_\theta^{h2}$，分别处理前 $T_h/2$ 步和后 $T_h/2$ 步去噪。消融实验（Table 7）表明，使用 2 个高级去噪器且高级扩散率设为 95% 时，FID 达到 0.084；而仅使用 1 个去噪器（B2A-HDM$_{t-1}$）时 FID 急剧升高至 0.315，验证了多去噪器分阶段训练对于细节增强的必要性。

### 时间步感知的加权训练损失

在 BDM 的训练中，B2A-HDM 引入了**时间步感知的加权 MSE 损失**，以增大早期去噪步骤的惩罚权重：

$$\mathcal{L}_{mse}^{t} = \lambda(t) \mathcal{L}_{mse}^{\epsilon}, \quad \lambda(t) = (1-\bar{\alpha}_t) \cdot w_1 + w_2$$

其中 $w_1=4.5$，$w_2=0.5$。由于 $\bar{\alpha}_t$ 在早期时间步较大，$(1-\bar{\alpha}_t)$ 较小，该加权策略使模型更加关注去噪早期的关键步骤，从而提升 BDM 输出结果的文本一致性，为后续 ADM 的细节增强提供更可靠的初始条件（Fig. 5）。

### 与基线方法的本质差异

相较于现有方法，B2A-HDM 的 changed slots 体现在两个维度：一是**扩散过程的空间维度与分工**，从单一低维空间的完整去噪转变为低维对齐-高维增强的分层协作；二是**BDM 的训练损失函数**，从标准等权 MSE 损失转变为时间步感知的加权损失。这两项改变共同实现了 HumanML3D 上 FID 0.084 与 Top-1 R-Precision 0.511 的最优综合性能（Table 5），在细节质量与文本一致性两个通常相互制约的指标上同时超越了所有基线方法。

## 整体框架

B2A-HDM 将文本到动作的生成过程分解为两个层次化阶段，分别对应低维和高维潜在空间中的扩散模型，以协同利用二者在跨模态对齐与细节生成上的互补优势。整体 pipeline 如图 3 所示，由以下模块串联构成：

1. **文本编码**：使用冻结的 CLIP 文本编码器 $\tau_\theta$ 提取文本嵌入 $\tau_\theta(\mathbf{w})$，作为各扩散去噪器的条件输入（Eq. 4, 5）。
2. **基本扩散模型 (BDM)**：在低维潜在空间（$4 \times 256$）中执行前 $T_l$ 步去噪。BDM 包含：
   - 低维动作 VAE 编码器 $\mathcal{E}_l$ 与解码器 $\mathcal{D}_l$
   - 去噪器 $\epsilon_\theta^l$，从纯噪声 $\mathbf{z}_{T_l}^l$ 开始，以文本嵌入为条件逐步去噪，生成文本一致的中间潜在表示 $\mathbf{z}_0^l$
3. **空间提升**：将 BDM 的输出 $\mathbf{z}_0^l$ 通过 $\mathcal{D}_l$ 解码为动作序列，再经高维动作 VAE 编码器 $\mathcal{E}_h$ 重新编码到高维潜在空间（$8 \times 256$），并加噪至高维扩散链的对应时间步 $\mathbf{z}_{T_h}^h$。
4. **高级扩散模型 (ADM)**：在高维潜在空间中执行剩余 $T_h$ 步去噪，负责细节增强。ADM 包含：
   - 高维动作 VAE 编码器 $\mathcal{E}_h$ 与解码器 $\mathcal{D}_h$
   - 两个去噪器 $\epsilon_\theta^{h1}$ 和 $\epsilon_\theta^{h2}$，分别负责前 $T_h/2$ 步和后 $T_h/2$ 步去噪（Algorithm 1）
5. **最终解码**：ADM 的输出 $\mathbf{z}_0^h$ 经 $\mathcal{D}_h$ 解码为最终的动作序列。

**关键设计决策**：

- **时间步分割与多去噪器**：BDM 与 ADM 的去噪步数比例由高级扩散率控制（最优为 95%），ADM 内部进一步将去噪过程拆分为两个子阶段，由两个去噪器分别处理。消融实验表明，使用 2 个高级去噪器时 FID 为 0.084，而单一去噪器（B2A-HDM$_{t-1}$）的 FID 升至 0.315，验证了多去噪器框架的有效性（Table 7）。
- **时间步感知损失**：BDM 训练采用加权 MSE 损失 $\mathcal{L}_{mse}^{t} = \lambda(t) \mathcal{L}_{mse}^{\epsilon}$，其中 $\lambda(t) = (1-\bar{\alpha}_t) \cdot w_1 + w_2$（$w_1=4.5, w_2=0.5$），增大早期去噪步骤的惩罚以强化文本-动作对齐（Eq. 7）。
- **VAE 训练**：两个 VAE（$\mathcal{E}_l/\mathcal{D}_l$ 与 $\mathcal{E}_h/\mathcal{D}_h$）独立训练，损失函数为 $\mathcal{L}_{vae} = \lambda_{kl}\mathcal{L}_{kl} + \lambda_{mse}^{vae}\mathcal{L}_{mse}^{vae}$，其中 $\lambda_{kl}=10^{-4}$，$\lambda_{mse}^{vae}=1.0$（Eq. 6）。

**输入输出流**：输入为自然语言描述 $\mathbf{w}$，输出为 3D 人体动作序列。推理时，BDM 从纯噪声出发，经 $T_l$ 步去噪后解码-重编码送入 ADM，ADM 经 $T_h$ 步去噪后解码得到最终动作。所有扩散去噪器均采用无分类器引导（Eq. 5），引导尺度 $g$ 用于调节文本条件与无条件预测的平衡。

### 补充图表

![[assets/figures/papers/paper_list_l1815_B2A_HDM_Towards_Detailed_Text_to_Motion_Synthesis_via_Basic_to_Advanced/figures/004_Figure_3.jpg]]
*Figure 3: Method Overview. B2A-HDM consists of a Basic Diffusion Model(BDM) and an Advanced Diffusion Model(ADM). BDM comprises a VAE*

## 核心模块与公式推导

B2A-HDM 的核心架构由两个层次化的扩散模型构成，分别运行于不同维度的潜在空间，并通过时间步分割实现协同去噪。其关键模块如下：

- **低维动作 VAE 编码器 (ℰ_l)**：将原始动作序列压缩至低维潜在空间（4×256），简化数据分布以利于跨模态对齐。
- **基本扩散去噪器 (ε_θ^l)**：在低维潜在空间中执行前 T_l 步去噪，以 CLIP 文本嵌入为条件，生成与文本描述一致的中间结果。该模块是保证模态一致性的关键。
- **低维动作 VAE 解码器 (𝒟_l)**：将低维潜在代码重建回动作空间，作为高维阶段的输入。
- **高维动作 VAE 编码器 (ℰ_h)**：将动作序列重新编码至高维潜在空间（8×256），以保留更多运动细节。
- **高级扩散去噪器 1 (ε_θ^{h1})**：在高维空间中负责前 T_h/2 步去噪，启动细节增强过程。
- **高级扩散去噪器 2 (ε_θ^{h2})**：在高维空间中负责后 T_h/2 步去噪，完成最终的细节生成。
- **高维动作 VAE 解码器 (𝒟_h)**：从高维潜在代码重建最终的动作序列。
- **冻结 CLIP 文本编码器 (τ_θ)**：提取冻结的文本嵌入，作为所有扩散去噪器的统一条件输入。

### 关键公式推导

**前向扩散过程**。给定从 VAE 编码器得到的潜在表示 z_0，前向过程通过 T 步逐步注入高斯噪声，定义为马尔可夫链：

$$q(\mathbf{z}_{1:T} \mid \mathbf{z}_0) := \prod_{t=1}^{T} q(\mathbf{z}_t \mid \mathbf{z}_{t-1})$$

其中单步条件分布为：

$$q(\mathbf{z}_t \mid \mathbf{z}_{t-1}) := \mathcal{N}(\mathbf{z}_t; \sqrt{1-\beta_t}\,\mathbf{z}_{t-1}, \beta_t \mathbf{I})$$

β_t 为噪声调度参数。利用重参数化技巧，可从 z_0 直接采样任意时间步的 z_t：

$$\mathbf{z}_t := \sqrt{\bar{\alpha}_t}\,\mathbf{z}_0 + \epsilon\sqrt{1-\bar{\alpha}_t},\quad \epsilon \sim \mathcal{N}(\mathbf{0},\mathbf{I})$$

其中 $\bar{\alpha}_t = \prod_{s=1}^{t} \alpha_s$，$\alpha_t = 1 - \beta_t$。

**去噪器训练目标**。去噪器 ε_θ 以文本条件 τ_θ(w) 和时间步 t 为输入，预测所添加的噪声，训练损失为标准 MSE：

$$\mathcal{L} := \mathbb{E}_{\epsilon\sim\mathcal{N}(\mathbf{0},\mathbf{I}),\,t\in[1,T]}\left[\|\epsilon - \epsilon_\theta(\mathbf{z}_t, \tau_\theta(\mathbf{w}), t)\|_2^2\right]$$

**无分类器引导**。推理时采用无分类器引导以增强文本条件控制：

$$\epsilon' := \epsilon_\theta(\mathbf{z}_t, \varnothing, t) + g \cdot \big(\epsilon_\theta(\mathbf{z}_t, \tau_\theta(\mathbf{w}), t) - \epsilon_\theta(\mathbf{z}_t, \varnothing, t)\big)$$

其中 g 为引导尺度，$\varnothing$ 表示空文本条件。

**VAE 训练损失**。两个 VAE（ℰ_l/𝒟_l 和 ℰ_h/𝒟_h）均采用相同的复合损失：

$$\mathcal{L}_{vae} = \lambda_{kl}\mathcal{L}_{kl} + \lambda_{mse}^{vae}\mathcal{L}_{mse}^{vae}$$

其中 KL 散度权重 $\lambda_{kl}=10^{-4}$，重建 MSE 权重 $\lambda_{mse}^{vae}=1.0$。

**时间步感知 MSE 损失**。基本扩散模型 BDM 采用时间步加权的 MSE 损失，以增大早期去噪步骤的惩罚力度：

$$\mathcal{L}_{mse}^{t} = \lambda(t)\mathcal{L}_{mse}^{\epsilon},\quad \lambda(t) = (1-\bar{\alpha}_t) \cdot w_1 + w_2$$

其中 $w_1=4.5$，$w_2=0.5$。当 t 较小时，$\bar{\alpha}_t$ 接近 1，$(1-\bar{\alpha}_t)$ 较小，权重接近 w_2；随着 t 增大，$\bar{\alpha}_t$ 减小，权重逐渐增大，从而强化对早期去噪步的监督。

### 补充图表

![[assets/figures/papers/paper_list_l1815_B2A_HDM_Towards_Detailed_Text_to_Motion_Synthesis_via_Basic_to_Advanced/figures/003_Figure_2.jpg]]
*Figure 2: (a) Visual comparisons among the reconstruction results of different VAEs. (b) Comparison of FID scores (lower is better). (c) Comparison of Top-1 R-Precision scores (higher is better)*

![[assets/figures/papers/paper_list_l1815_B2A_HDM_Towards_Detailed_Text_to_Motion_Synthesis_via_Basic_to_Advanced/figures/011_Figure_5.jpg]]
*Figure 5: Impact of the timestep-aware MSE loss for BDMs in different latent space (LS)*

## 实验与分析

### 瓶颈验证：低维潜在空间的双面性

B2A-HDM 的设计根植于一个核心观察：低维潜在扩散模型（如 **MLD** (Chen et al., CVPR 2023)）虽然易于训练且跨模态对齐能力强，但受限于潜在表示的容量，其生成的动作必然丢失大量细节。Figure 2 的定量分析清晰地揭示了这一矛盾：随着 VAE 潜在维度降低，重建动作的 FID 单调升高（质量恶化），但低维扩散模型的 Top-1 R-Precision 却显著优于高维扩散模型。这构成了一个因果瓶颈——**低维空间简化了数据分布，有利于学习文本到动作的跨模态映射（提升一致性），却以牺牲动作细节为代价；而高维空间虽能保留细节，但数据分布复杂、训练数据有限，导致扩散模型难以收敛，损害模态一致性**。B2A-HDM 的层次化设计正是为了打破这一僵局。

### 主实验结果

在 HumanML3D 和 KIT-ML 两个标准基准上，B2A-HDM 实现了细节质量与文本一致性的双重领先。

**HumanML3D 数据集**（Table 5）：B2A-HDM 取得了最低的 FID（0.084），显著优于此前最佳的 **T2M-GPT**（FID 0.116）和 **MLD**（FID 0.404）。同时，其 Top-1 R-Precision 达到 0.511，超过 **MotionDiffuse** (Zhang et al., CVPR 2022) 和 T2M-GPT 的 0.491。这意味着 B2A-HDM 在生成动作的逼真度和文本匹配度上同时达到了最优。MM-Dist 指标（3.020）同样为所有方法中最低，进一步验证了其跨模态对齐能力。

**KIT-ML 数据集**（Table 6）：B2A-HDM 的 FID 为 0.367，低于 MLD 的 0.404；Top-1 R-Precision 为 0.436，优于 MotionDiffuse 的 0.417。在两个数据集上，B2A-HDM 是唯一在 FID 和 R-Precision 两个核心指标上同时达到最佳的方法，证明了其“一致性-细节”协同优化策略的有效性。

**人类评估**（Table 3）：在 HumanML3D 上的偏好投票中，B2A-HDM 以 47.0% 的偏好率大幅领先 **MDM** (Tevet et al., ICCV 2023) 的 17.5%、MotionDiffuse 的 19.7% 和 T2M-GPT 的 15.8%，表明人类评估者一致认为其生成的动作在细节和文本一致性上更优。

**定性对比**（Figure 4）：与基线方法的可视化对比显示，B2A-HDM 在保持整体动作与文本描述一致的同时，能够生成更丰富的手部细节和更自然的肢体过渡，而低维扩散方法（如 MLD）的动作则显得平滑但缺乏细节。

### 消融实验：层次化设计的因果链路

Table 7 的系统消融揭示了 B2A-HDM 各组件的因果贡献：

![[assets/figures/papers/paper_list_l1815_B2A_HDM_Towards_Detailed_Text_to_Motion_Synthesis_via_Basic_to_Advanced/figures/017_Table_7.jpg]]
*Table 7: Quantitative results of different B2A-HDM variants with various hyperparameter configurations*

**多去噪器框架的必要性**：当仅使用 1 个高级去噪器（B2A-HDMt-1）时，FID 从 0.084 急剧恶化至 0.315，R-Precision 也出现下降。这表明将高维去噪过程分配给多个专门化去噪器，是细节增强的关键机制——单个去噪器难以同时覆盖高维空间中的不同去噪阶段。

**高级扩散率的影响**：将高级扩散（ADM 负责的步数比例）从 25% 逐步提升至 95%，FID 从 0.242 单调下降至 0.084。这验证了让 ADM 覆盖更多去噪步数有利于细节增强的假设，同时也说明 BDM 仅需在早期阶段提供粗糙的文本一致初始化即可。

**潜在空间维度的权衡**：低维潜在空间设为 4×256、高维潜在空间设为 8×256 时取得最佳 FID-R-Precision 权衡。进一步增大高维空间维度（如 12×256）反而导致性能下降，说明过高的维度会加剧数据稀疏问题，损害扩散模型的训练稳定性。

**时间步感知损失**（Figure 5）：在 BDM 训练中引入时间步加权 MSE 损失（λ(t) = (1-ᾱ_t)·4.5 + 0.5），通过增大早期去噪步骤的惩罚，使 BDM 更专注于从纯噪声中恢复全局结构，在不同潜在维度下均带来一致的 FID 和 R-Precision 提升。

### 资源效率

Table 4 显示，B2A-HDM 的生成器参数量为 35.8M，单次推理时间约 2.1 秒（在 Tesla V100 上），虽然高于单阶段潜在扩散模型 MLD（0.3 秒），但远低于在原始数据空间扩散的 MDM（28.4 秒），且生成质量显著优于两者，在质量-效率曲线上处于有利位置。

![[assets/figures/papers/paper_list_l1815_B2A_HDM_Towards_Detailed_Text_to_Motion_Synthesis_via_Basic_to_Advanced/figures/014_Table_4.jpg]]
*Table 4: Resource consumption comparisons*

### 失败模式与局限性

尽管 B2A-HDM 在主流基准上表现出色，但其层次化设计仍存在固有局限。首先，**训练数据的文本风格有限**：当输入文本过于简略或包含极端风格描述时，模型可能无法生成准确对应的动作，这源于训练数据标注风格的单一性。其次，**精细运动缺失**：与现有大多数方法类似，B2A-HDM 主要关注人体关节动作，面部表情和手部精细运动未被纳入建模范围，限制了生成动作的自然度和表现力。这些失败模式提示，未来的改进方向在于利用大语言模型扩充文本多样性，以及将面部和手部运动整合到层次化生成框架中。

### 补充图表

![[assets/figures/papers/paper_list_l1815_B2A_HDM_Towards_Detailed_Text_to_Motion_Synthesis_via_Basic_to_Advanced/figures/015_Table_5.jpg]]
*Table 5: Quantitative comparisons on HumanML3D dataset (Guo et al. 2022a). Red and Blue indicate the best and the second best result*

![[assets/figures/papers/paper_list_l1815_B2A_HDM_Towards_Detailed_Text_to_Motion_Synthesis_via_Basic_to_Advanced/figures/016_Table_6.jpg]]
*Table 6: Quantitative comparisons on KIT-ML dataset (Plappert, Mandery, and Asfour 2016). Red and Blue indicate the best and the second best result*

![[assets/figures/papers/paper_list_l1815_B2A_HDM_Towards_Detailed_Text_to_Motion_Synthesis_via_Basic_to_Advanced/figures/013_Table_3.jpg]]
*Table 3: Human Evaluation (HE) Results on HumanML3D dataset (Guo et al. 2022a)*

![[assets/figures/papers/paper_list_l1815_B2A_HDM_Towards_Detailed_Text_to_Motion_Synthesis_via_Basic_to_Advanced/figures/005_Table_1.jpg]]
*Table 1: Quantitative results on (a) HumanML3D (Guo et al. 2022a) and (b) KIT-ML (Plappert, Mandery, and Asfour 2016). Red and Blue indicate the best and the second best result*

![[assets/figures/papers/paper_list_l1815_B2A_HDM_Towards_Detailed_Text_to_Motion_Synthesis_via_Basic_to_Advanced/figures/006_Table_2.jpg]]
*Table 2: Quantitative results of the ablation study with different configurations, in which BD/AD No., LD/HD-LS Dim refer to basic/advanced denoiser number and low/highdimension latent space dimension, respectively*

![[assets/figures/papers/paper_list_l1815_B2A_HDM_Towards_Detailed_Text_to_Motion_Synthesis_via_Basic_to_Advanced/figures/012_Figure_4.jpg]]
*Figure 4: Qualitative comparisons on HumanML3D dataset (Guo et al. 2022a). The flow of time is represented by colors, with lighter shades indicating the past. Please zoom in for more details*

![[assets/figures/papers/paper_list_l1815_B2A_HDM_Towards_Detailed_Text_to_Motion_Synthesis_via_Basic_to_Advanced/figures/018_Table_9.jpg]]
*Table 9: Architecture of diffusion network ϵθ*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

B2A-HDM 的核心设计动机源于对现有文本驱动动作合成方法两大技术路线的反思与融合。

**原始数据空间扩散模型**（如 **MDM** (Tevet et al., ICCV 2023)、**MotionDiffuse** (Zhang et al., CVPR 2022)）直接在原始动作序列的高维空间执行去噪过程。该路线保留了完整的动作细节表达能力，但由于高维数据分布高度复杂，且训练数据规模有限（HumanML3D 仅约 1.5 万条动作），扩散模型难以学习到稳健的跨模态映射，导致生成结果与文本描述之间的模态一致性受损。这是 B2A-HDM 试图解决的核心矛盾之一。

**低维潜在扩散模型**（如 **MLD** (Chen et al., CVPR 2023)）将扩散过程迁移至 VAE 编码的低维潜在空间（如 $4 \times 256$），通过压缩表示来简化目标分布，使模型更易学习文本到动作的映射关系。然而，这一策略的代价是潜在空间容量不足，VAE 重建时丢失了大量动作细节（Fig. 2(a)-(b) 证实：潜在维度越低，重建 FID 越高）。B2A-HDM 的分析明确指出：“低维扩散模型虽然对细节生成无效，但对模态变换有显著益处”（Fig. 2(c)）。

**自回归生成路线**（如 **T2M-GPT** (Zhang et al., 2023)）则采用 VQ-VAE 与 GPT 的组合，在离散 token 空间中进行生成。该路线在 HumanML3D 上取得了 0.116 的 FID，是 B2A-HDM 在 FID 指标上对标的主要基线之一。

B2A-HDM 的突破在于**不将上述路线视为互斥选项，而是将其作为协同组件纳入一个分层的去噪框架**。它将去噪过程显式拆分为两个阶段：基本扩散模型（BDM）在低维潜在空间（$4 \times 256$）执行前 $T_l$ 步去噪，继承 MLD 路线在模态一致性上的优势；高级扩散模型（ADM）则将 BDM 的中间结果解码后重新编码到高维潜在空间（$8 \times 256$），在剩余 $T_h$ 步中完成细节增强。这种“低维保一致、高维补细节”的分工，使 B2A-HDM 同时超越了纯低维扩散（MLD）和纯高维扩散（MDM）的性能上限。

### 2. 关键改进槽位

相较于基线方法，B2A-HDM 在两个关键设计槽位上进行了实质性改动：

- **扩散过程的空间维度与分工**：MLD 仅在单一低维潜在空间中由单个去噪器执行完整的 $T$ 步去噪。B2A-HDM 将这一过程分解为低维空间的 BDM 去噪（$T_l$ 步）与高维空间的 ADM 去噪（$T_h$ 步），且 ADM 内部进一步由两个去噪器分阶段负责不同时间间隔（Algorithm 1, Fig. 3）。消融实验表明，使用 2 个高级去噪器且高级扩散率 $\geq 95\%$ 时，FID 从单去噪器配置的 0.315 降至 0.084（Table 7）。

- **BDM 训练损失函数**：标准扩散模型对所有时间步采用等权重的 MSE 损失。B2A-HDM 为 BDM 引入了时间步感知的加权 MSE 损失 $\mathcal{L}_{mse}^{t} = \lambda(t) \mathcal{L}_{mse}^{\epsilon}$，其中 $\lambda(t) = (1-\bar{\alpha}_t) \cdot w_1 + w_2$（$w_1=4.5$，$w_2=0.5$），通过增大早期去噪步骤的惩罚来强化 BDM 输出的文本一致性（Eq. (7)）。Fig. 5 的消融证实该损失在不同潜在维度下均能提升 BDM 的 FID 和 Top-1 R-Precision。

### 3. 适用边界与局限

B2A-HDM 的设计存在以下明确边界：

- **数据规模与标注风格的依赖性**：模型性能受限于训练数据的规模和文本标注风格。论文明确指出，B2A-HDM“可能难以泛化到风格极端或过于简略的文本描述”。这意味着在开放域、多语言或口语化文本输入场景下，模型的一致性表现可能显著下降。

- **动作表达的范畴限制**：与当前大多数文本到动作合成工作一致，B2A-HDM 主要关注人体关节动作的生成，忽视面部表情和手部的精细运动。对于需要全身细粒度表达的应用（如虚拟人交互、手语生成），该框架尚不完整。

- **计算资源需求**：B2A-HDM 包含两个 VAE（低维与高维）及三个扩散去噪器（1 个 BDM + 2 个 ADM），虽然推理速度与资源消耗在 Table 4 中有所报告，但相较于单一潜在扩散模型，其多模型协同的架构复杂度更高，可能增加部署和维护成本。

### 4. 开放问题

论文提出了两个值得后续探索的方向：

- **利用大型语言模型扩充文本风格多样性**：如何借助 ChatGPT-4 等 LLM 对现有训练数据的文本描述进行风格改写和扩充，以提升模型对不同语言风格的泛化能力，是一个具有实践价值的开放问题。

- **面部表情与手部动作的整合**：如何将准确的面部表情和手部动作合成整合到 B2A-HDM 的分层扩散框架中，使生成的动作更加自然完整，是推动该技术走向高保真虚拟人合成的关键挑战。

## 原文 PDF

![[paperPDFs/AAAI_2024/B2A_HDM_Towards_Detailed_Text_to_Motion_Synthesis_via_Basic_to_Advanced_Hierarchical_Diffusion_Model.pdf]]