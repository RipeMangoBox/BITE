---
title: "FlexMotion: Lightweight, Physics-Aware, and Controllable Human Motion Generation"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: "paperPDFs/arxiv_2025/FlexMotion:_Lightweight,_Physics-Aware,_and_Controllable_Human_Motion_Generation.pdf"
project_link: null
code_link: null
aliases:
- FlexMotion
tags:
- arxiv_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过预训练的多模态物理感知 Transformer 自编码器，将复杂的多模态运动数据（关节位置、旋转、速度、加速度、肌肉激活、力矩、接触力）压缩到低维潜在空间，并在训练和重建过程中显式施加欧拉-拉格朗日物理损失与肌肉协调损失，从而无需外部物理引擎即能保证生成运动的物理合理性。
primary_logic: 在潜在空间中运行扩散模型，结合物理感知自编码器的端到端物理约束，可在不牺牲计算效率的前提下生成物理真实的人体运动；附加即插即用的零卷积可控性模块，首次允许对肌肉激活、关节驱动力矩、接触力等多维物理参数进行空间/时间显式控制。
claims:
- 在潜在空间中操作扩散模型，显著降低训练和推理的计算开销，同时保持高生成质量。
- 多模态自编码器结合欧拉-拉格朗日损失和肌肉损失是保证运动物理真实性的关键，消融实验表明移除任何一项都会导致物理指标大幅劣化。
- FlexMotion 在 HumanML3D、KIT-ML、Flag3D 三个数据集上，在物理质量指标（如穿透、浮动、肌肉激活合理性、接触力准确性）方面均显著优于现有最佳方法。
- HumanML3D 上 FID↓ = 0.198 (All Conditions 20% frames)
---

# FlexMotion: Lightweight, Physics-Aware, and Controllable Human Motion Generation

> [!tip] 核心洞察
> 在潜在空间中运行扩散模型，结合物理感知自编码器的端到端物理约束，可在不牺牲计算效率的前提下生成物理真实的人体运动；附加即插即用的零卷积可控性模块，首次允许对肌肉激活、关节驱动力矩、接触力等多维物理参数进行空间/时间显式控制。

| 字段      | 内容                                                                                                                                         |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| 中文题名    | FlexMotion：轻量级、物理感知且可控的人体运动生成                                                                                                              |
| 英文题名    | FlexMotion: Lightweight, Physics-Aware, and Controllable Human Motion Generation                                                           |
| 会议/期刊   | arXiv 2025                                                                                                                                 |
| Links | [paper](https://arxiv.org/abs/2501.16778) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method  | FlexMotion                                                                                                                                 |
| Dataset | HumanML3D, Computational Efficiency                                                                                                        |

> [!tip] 效果简介
> - HumanML3D 上，FID↓ 0.198 (All Conditions 20% frames) vs MDM: 0.698 (−0.500)；R-Precision↑ 0.793 (All Conditions 20% frames) vs MDM: 0.602 (+0.191)；Penetration↓ 2.311 (All Conditions 20% frames) vs MDM: 11.291 (−8.98)。
> - Computational Efficiency 上，Inference Time (s) DDIM 50 13.158 vs MDM: 225.283 (−212.125)。

## 概要

**瓶颈**：现有文本到运动生成方法面临计算效率、物理真实性与空间可控性的三重妥协。依赖外部物理模拟器的方法（如 **PhysDiff**，Yuan et al., 2023）推理速度慢；忽略生物力学约束（肌肉激活、接触力、关节力矩）的方法则产生物理上不合理的运动；同时，多数方法仅支持关节位置控制，无法细粒度操控肌肉激活、驱动力矩等关键运动参数。

**核心思路**：FlexMotion 通过预训练的**多模态物理感知 Transformer 自编码器**，将关节位置、旋转、速度、加速度、肌肉激活、力矩、接触力等多模态运动数据压缩到低维潜在空间，并在训练和重建过程中显式施加**欧拉-拉格朗日物理损失**与**肌肉协调损失**，从而无需外部物理引擎即可保证生成运动的物理合理性。在潜在空间中运行扩散模型，结合即插即用的**零卷积可控性模块**，首次实现了对肌肉激活、关节驱动力矩、接触力等多维物理参数的显式空间/时间控制。

**方法定位**：FlexMotion 由三个模块级联构成——物理感知多模态自编码器（Sec. 3.1）、潜在空间运动扩散模型（Sec. 3.2）、空间可控性模块（Sec. 3.3）。其设计在生成空间（潜在空间 vs. 原始运动空间）、物理约束（端到端可微物理损失 vs. 外部模拟器/无约束）、可控维度（多维物理参数 vs. 仅关节位置）三个关键维度上与现有基线形成系统性差异。

**主要结果**：在 HumanML3D、KIT-ML、Flag3D 三个数据集上，FlexMotion 在穿透（Penetration）、浮动（Floating）、足部滑动（Foot Skating）、肌肉激活合理性（Muscle Limit）等物理质量指标上均显著优于 **MDM**（Tevet et al., 2023）、**OmniControl**（Xie et al., 2023）、**MLD**（Chen et al., 2023）等基线。以 HumanML3D 的 All Conditions 20% frames 条件为例，FlexMotion 的 FID 降至 0.198（MDM 为 0.698），Penetration 降至 2.311（MDM 为 11.291），Muscle Limit 降至 1.089（MDM 为 16.114）。同时，推理时间从 MDM 的 225.3 秒大幅缩减至 13.2 秒（DDIM 50 步，生成 2048 个片段），实现了物理真实性与计算效率的双重突破。

**证据强度**：上述结论由多组消融实验强力支撑——移除欧拉-拉格朗日损失或肌肉损失均导致物理指标大幅劣化（Table 8）；潜在空间维度与物理约束权重存在明确的最优配置（Tables 9–10）。需注意，训练阶段依赖 OpenSim 进行数据增强，且物理约束权重需手动权衡真实感与物理准确性，这是当前方法的已知局限。

人体运动生成是计算机视觉与图形学中的核心问题，其应用涵盖动画制作、虚拟现实、机器人仿真和人机交互等领域。近年来，扩散模型在文本到运动生成任务上取得了显著进展，涌现出 **MDM**（Tevet et al., 2023）、**MotionDiffuse**（Zhang et al., 2022）、**MLD**（Chen et al., 2023）等一系列代表性工作。然而，现有方法在以下三个维度上存在系统性妥协，构成了该领域的关键瓶颈。

**计算效率与物理真实性的两难。** 当前方法大致分为两类：一类在原始运动表示空间（如 SMPL 参数或关节位置序列）上直接运行扩散过程，虽能保持一定的生成多样性，但计算开销极大——例如 MDM 生成 2048 个运动片段需耗时约 225 秒（DDIM 50 步推理）；另一类方法如 **PhysDiff**（Yuan et al., 2023）在扩散过程中引入外部物理模拟器进行运动校正，虽能改善物理合理性，但模拟器的串行调用进一步加剧了推理延迟，且将物理约束置于生成流程之外，难以实现端到端优化。

**生物力学约束的系统性缺失。** 绝大多数现有方法仅关注运动学层面的自然度（如 FID、R-Precision），而忽略了人体运动本质上是多模态物理过程的产物——关节轨迹的生成必须同时满足肌肉激活的生理限制、关节驱动力矩的动力学约束以及足-地接触力的力学平衡。忽略这些生物力学约束会导致生成的运动出现穿透、滑步、关节超限等物理不合理现象。例如，MDM 在 HumanML3D 数据集上的穿透指标高达 11.291，肌肉激活超限达 16.114，严重限制了生成运动在实际交互场景中的可用性。

**空间可控性的维度局限。** 以 **OmniControl**（Xie et al., 2023）为代表的现有可控生成方法，其控制信号通常仅限于关节位置或末端轨迹的空间约束，无法对肌肉激活水平、关节驱动力矩、接触力分布等更深层的物理参数进行显式操控。这限制了运动生成在需要精细物理交互的场景（如康复训练动作合成、体育动作分析）中的应用潜力。

FlexMotion 的提出正是为了打破上述妥协。其核心动机在于：是否可以在不依赖外部物理模拟器的前提下，将生物力学约束直接嵌入生成模型的训练目标，同时在低维潜在空间中运行扩散过程以保持计算效率，并进一步提供对多维物理参数的即插即用式空间控制？这一思路的关键洞察是：通过预训练的物理感知自编码器将复杂的多模态运动数据压缩到潜在空间，并在重建过程中显式施加欧拉-拉格朗日动力学损失与肌肉协调损失，即可使生成框架在保持轻量化的同时获得物理合理性保证，而无需在推理阶段调用任何物理引擎。

## 核心方法与创新机理

FlexMotion 的核心创新在于构建了一条**物理感知的潜在空间生成管线**，在不牺牲计算效率的前提下，首次实现了对多模态运动参数（包括肌肉激活、关节驱动力矩、接触力）的细粒度可控生成。其创新可归结为三个紧密耦合的 changed slots。

### 从原始运动空间到物理感知的潜在空间

现有扩散类运动生成方法，如 **MDM** (Tevet et al., 2023) 和 **PhysDiff** (Yuan et al., 2023)，直接在原始运动表示空间（如 SMPL 参数或关节位置序列）上执行去噪过程。这一设计导致两个后果：一是计算开销巨大，MDM 在 DDIM 50 步推理下需 225 秒；二是物理合理性要么完全缺失（MDM），要么依赖外部物理模拟器在每步去噪后进行投影校正（PhysDiff），这进一步增加了推理负担并引入了模拟器偏差。

FlexMotion 将扩散过程整体迁移至低维潜在空间。具体而言，它首先训练一个**物理感知多模态自编码器**（Physics-aware Multimodal Autoencoder），将高维运动序列 $`\mathbf{x}_t = [\mathbf{p}_t, \mathbf{r}_t, \dot{\mathbf{r}}_t, \ddot{\mathbf{r}}_t, \mathbf{a}_t, \tau_t, \lambda_t] \in \mathbb{R}^D`$ 压缩为紧凑的潜在表示 $`\mathbf{x}_t^e = \mathcal{E}(\mathbf{x}_t; \theta_{\mathcal{E}})`$。扩散模型随后仅在该潜在空间中操作，使得推理时间锐减至 13.2 秒（Table 4），较 MDM 提速约 17 倍。与同样采用潜在空间扩散的 **MLD** (Chen et al., 2023) 相比，FlexMotion 的关键差异在于其自编码器并非单纯追求重建精度，而是被显式赋予了物理感知能力。

### 从无约束生成到端到端内嵌物理约束

FlexMotion 最根本的 causal knob 在于**将可微物理损失直接嵌入自编码器的训练目标**，从而无需外部物理引擎即可保证生成运动的生物力学合理性。自编码器的总损失函数为：

$$`\mathcal{L}_{\mathrm{AE}} = \mathcal{L}_{\mathrm{recon}} + \gamma_{\mathrm{euler}} \mathcal{L}_{\mathrm{euler}} + \gamma_{\mathrm{muscle}} \mathcal{L}_{\mathrm{muscle}}`$$

其中，$`\mathcal{L}_{\mathrm{recon}}`$ 是多模态重建损失（Eqn. 4），覆盖关节位置、旋转、速度、加速度、力矩、接触力及肌肉激活的加权 L2/L1 误差。关键的物理约束来自两项：

- **欧拉-拉格朗日损失** $`\mathcal{L}_{\mathrm{euler}}`$（Eqn. 6）：强制重建运动满足人体骨骼系统的动力学方程 $`\mathbf{M}(\mathbf{r}_t)\ddot{\mathbf{r}}_t + \mathbf{C}(\mathbf{r}_t,\dot{\mathbf{r}}_t)\dot{\mathbf{r}}_t + \mathbf{G}(\mathbf{r}_t) = \tau_t + \mathbf{J}_C^\top(\mathbf{r}_t)\lambda_t`$，计算方程左右两边之差的 L2 范数。这确保了关节力矩 $`\tau_t`$ 与接触力 $`\lambda_t`$ 在物理上自洽。
- **肌肉协调损失** $`\mathcal{L}_{\mathrm{muscle}}`$（Eqn. 7）：建模肌肉激活 $`\mathbf{a}_t`$ 与关节加速度 $`\ddot{\mathbf{r}}_t`$ 之间的线性映射关系 $`\ddot{\mathbf{r}}_t \approx L \mathbf{a}_t`$，并通过 $`\beta_{\mathrm{reg}} \| \mathbf{a}_t \|_2^2`$ 正则项惩罚过度激活，维持生理合理性。

消融实验（Table 8）为这一设计提供了决定性证据：仅使用重建损失时，FID 为 0.611，Muscle Limit 高达 14.614，Penetration 为 8.820；加入全部物理损失后，FID 降至 0.298，Muscle Limit 骤降至 5.264，Penetration 降至 4.954。这表明物理约束不仅没有损害生成自然度，反而通过正则化效应提升了整体质量。

### 从关节位置控制到多维物理参数可控

现有可控运动生成方法如 **OmniControl** (Xie et al., 2023) 仅支持对关节位置或轨迹施加空间约束。FlexMotion 通过**即插即用的空间可控性模块**（Spatial Controllability Module），将控制维度扩展至肌肉激活、关节驱动力矩和接触力等深层物理参数。

该模块的技术核心是在预训练扩散模型的去噪网络旁添加零初始化卷积支路（Eqn. 12）：

$$`\epsilon_{\theta_{\mathrm{total}}}(\mathbf{X}_n^e, C^e, n, c) = \epsilon_\theta(\mathbf{X}_n^e, n, c) + \mathbf{Z}( \epsilon_{\theta_C}(\mathbf{X}_n^e + \mathbf{Z}(C^e, \theta_{z1}), n, c), \theta_{z2} )`$$

零初始化确保训练初期控制支路输出为零，完全保留预训练模型的生成能力；随后逐步学习将控制信号 $`C^e`$ 融入去噪过程，实现“即插即用”。这一设计使得 FlexMotion 能够在文本提示的基础上，进一步通过空间掩码精确指定某块肌肉的激活程度、某个关节的驱动力矩或特定接触点的受力大小（Figure 1），这是此前所有基线方法均不具备的能力。

FlexMotion 的整体架构由三个核心模块串联构成，形成一个“压缩—生成—控制”的流水线，如 Figure 2 所示。其设计目标是在不依赖外部物理模拟器的前提下，实现轻量、物理合理且可控的人体运动生成。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2501_16778/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed FlexMotion framework. It consists of first, multimodal autoencoder, which maps motion kinematic and dynamic properties to latent space (Sec. 3.1), second, latent space motion diffusion model, which generates a motion sequence in latent space conditioned on text prompt (Sec. 3.2) and third, spatial controllability module, which adds further control to the generated motion (Sec. 3.3)*

**模块关系与数据流**

1. **物理感知多模态自编码器 (Physics-aware Multimodal Autoencoder, Sec. 3.1)**  
   该模块作为整个框架的基础，负责将高维的多模态运动数据压缩到低维潜在空间，同时确保潜在表示保留了足够的生物力学信息。其输入为每个时间步拼接而成的特征向量：
   $$\mathbf{x}_t = [\mathbf{p}_t, \mathbf{r}_t, \dot{\mathbf{r}}_t, \ddot{\mathbf{r}}_t, \mathbf{a}_t, \tau_t, \lambda_t] \in \mathbb{R}^D$$
   其中 $\mathbf{p}_t$ 为关节位置，$\mathbf{r}_t$ 为旋转，$\dot{\mathbf{r}}_t$ 和 $\ddot{\mathbf{r}}_t$ 分别为角速度和角加速度，$\mathbf{a}_t$ 为肌肉激活，$\tau_t$ 为关节驱动力矩，$\lambda_t$ 为接触力。编码器 $\mathcal{E}$ 将输入序列映射为潜在表示 $\mathbf{x}_t^e = \mathcal{E}(\mathbf{x}_t; \theta_{\mathcal{E}})$，解码器 $\mathcal{D}$ 再从潜在空间重建运动序列 $\hat{\mathbf{x}}_t = \mathcal{D}(\mathbf{x}_t^e; \theta_{\mathcal{D}})$。  
   关键创新在于：**解码器重建过程中显式施加了可微的物理约束**——欧拉-拉格朗日损失 $\mathcal{L}_{\mathrm{euler}}$ 强制重建运动满足骨骼动力学方程，肌肉协调损失 $\mathcal{L}_{\mathrm{muscle}}$ 约束肌肉激活产生合理的关节加速度。这使自编码器本身成为一个“物理感知”的压缩器，为后续生成提供了物理合理的潜在空间。

2. **潜在空间运动扩散模型 (FlexMotion Diffusion Model, Sec. 3.2)**  
   在自编码器学到的低维潜在空间中执行条件扩散过程。给定文本提示 $c$，扩散模型在潜在变量 $\mathbf{X}_n^e$ 上逐步去噪，生成符合语义的潜在运动序列。由于操作空间从原始高维运动表示（如 SMPL 参数或关节位置序列）压缩为低维潜在变量，训练和推理的计算开销显著降低——这是 FlexMotion 实现“轻量级”特性的核心机制。扩散训练目标为标准去噪损失：
   $$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{X_0^e, n, \epsilon} \left[ \| \epsilon - \epsilon_\theta(\mathbf{X}_n^e, n, c) \|_2^2 \right]$$

3. **空间可控性模块 (Spatial Controllability Module, Sec. 3.3)**  
   这是一个即插即用的扩展模块，通过在预训练扩散模型上添加零初始化卷积层来实现对多种运动参数的精细时空控制。该模块接收控制信号 $C^e$（可以是空间路径、肌肉激活、关节驱动力矩或接触力等任意组合），并将其融入扩散模型的噪声预测过程：
   $$\epsilon_{\theta_{\mathrm{total}}}(\mathbf{X}_n^e, C^e, n, c) = \epsilon_\theta(\mathbf{X}_n^e, n, c) + \mathbf{Z}( \epsilon_{\theta_C}(\mathbf{X}_n^e + \mathbf{Z}(C^e, \theta_{z1}), n, c), \theta_{z2} )$$
   零初始化设计确保了训练初期控制支路不影响预训练模型的行为，实现了真正的“即插即用”。最终训练目标为：
   $$\mathcal{L}_{\mathrm{total}} = \mathbb{E}_{X_0^e, C^e, n, \epsilon} \left[ \| \epsilon - \epsilon_{\theta_{\mathrm{total}}}(\mathbf{X}_n^e, C^e, n, c) \|_2^2 \right]$$

**端到端流程**

推理时，用户提供文本提示和可选的控制信号（如指定某关节的空间轨迹或某肌群的激活模式）。文本条件通过潜在扩散模型生成潜在运动序列，控制信号通过可控性模块注入约束；生成的潜在序列经物理感知解码器重建为包含关节运动学、肌肉激活、力矩和接触力的完整多模态运动。整个过程无需调用外部物理引擎，物理合理性由自编码器端到端保证。

FlexMotion 的整体架构由三个核心模块串联构成（Figure 2）：**物理感知多模态自编码器**、**潜在空间运动扩散模型**和**空间可控性模块**。其设计逻辑是：先通过自编码器将高维多模态运动数据压缩到低维潜在空间并嵌入物理约束，再在该潜在空间中执行轻量扩散生成，最后以即插即用的零卷积支路引入对多种运动参数的精细控制。

### 3.1 物理感知多模态自编码器

该模块（Figure 3）的核心功能是将包含运动学与动力学信息的多模态数据映射到低维潜在空间，并在解码重建过程中显式施加可微物理损失，从而保证重建运动的生物力学合理性。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2501_16778/figures/003_Figure_3.jpg]]
*Figure 3: Overview of Physics-aware Multimodal Autoencoder. It maps diverse motion properties into the latent space and reconstructs them while enforcing physics-based loss terms (Sec. 3.1)*

**多模态输入表示**：在每个时间步 $t$，运动数据由关节位置、旋转、速度、加速度、肌肉激活、关节驱动力矩和接触力七种模态拼接为单个特征向量：

$$
\mathbf{x}_t = [\mathbf{p}_t, \mathbf{r}_t, \dot{\mathbf{r}}_t, \ddot{\mathbf{r}}_t, \mathbf{a}_t, \tau_t, \lambda_t] \in \mathbb{R}^D
$$

其中 $\mathbf{p}_t$ 为关节位置，$\mathbf{r}_t$ 为关节旋转，$\dot{\mathbf{r}}_t$ 和 $\ddot{\mathbf{r}}_t$ 分别为关节角速度和角加速度，$\mathbf{a}_t$ 为肌肉激活，$\tau_t$ 为关节驱动力矩，$\lambda_t$ 为接触力。

**编码器与解码器**：编码器 $\mathcal{E}$ 将输入序列映射到潜在表示，解码器 $\mathcal{D}$ 从潜在表示重建运动序列：

$$
\mathbf{x}_t^e = \mathcal{E}(\mathbf{x}_t; \theta_{\mathcal{E}}), \quad \hat{\mathbf{x}}_t = \mathcal{D}(\mathbf{x}_t^e; \theta_{\mathcal{D}})
$$

**重建损失**：为同时优化所有运动模态的解码精度，采用加权 $L_2$ 和 $L_1$ 损失的组合：

$$
\mathcal{L}_{\mathrm{recon}} = \sum_{t=1}^{T} \left[ \alpha_{\mathrm{pos}} \| \mathbf{p}_t - \hat{\mathbf{p}}_t \|_2^2 + \alpha_{\mathrm{rot}} \| \mathbf{r}_t - \hat{\mathbf{r}}_t \|_2^2 + \alpha_{\mathrm{vel}} \| \dot{\mathbf{r}}_t - \hat{\dot{\mathbf{r}}}_t \|_2^2 + \alpha_{\mathrm{acc}} \| \ddot{\mathbf{r}}_t - \hat{\ddot{\mathbf{r}}}_t \|_2^2 + \alpha_{\mathrm{torque}} \| \tau_t - \hat{\tau}_t \|_2^2 + \alpha_{\mathrm{force}} \| \lambda_t - \hat{\lambda}_t \|_1^1 + \alpha_{\mathrm{muscle}} \| a_t - \hat{a}_t \|_2^2 \right]
$$

**物理约束：欧拉-拉格朗日损失**。人体骨骼系统的动力学由欧拉-拉格朗日方程描述：

$$
\mathbf{M}(\mathbf{r}_t) \ddot{\mathbf{r}}_t + \mathbf{C}(\mathbf{r}_t, \dot{\mathbf{r}}_t) \dot{\mathbf{r}}_t + \mathbf{G}(\mathbf{r}_t) = \tau_t + \mathbf{J}_C^\top(\mathbf{r}_t) \lambda_t
$$

其中 $\mathbf{M}$ 为惯性矩阵，$\mathbf{C}$ 为科里奥利/离心力矩阵，$\mathbf{G}$ 为重力项，$\mathbf{J}_C$ 为接触雅可比矩阵。方程左侧为系统动力学效应，右侧为驱动力矩和接触力的贡献。将方程两侧之差的 $L_2$ 范数定义为可微物理约束：

$$
\mathcal{L}_{\mathrm{euler}} = \sum_{t=1}^{T} \left\| \mathbf{M}(\mathbf{r}_t)\ddot{\mathbf{r}}_t + \mathbf{C}(\mathbf{r}_t,\dot{\mathbf{r}}_t)\dot{\mathbf{r}}_t + \mathbf{G}(\mathbf{r}_t) - \tau_t - \mathbf{J}_C^\top(\mathbf{r}_t)\lambda_t \right\|^2
$$

**物理约束：肌肉协调损失**。为鼓励肌肉激活以生理合理的方式产生所需关节加速度，同时惩罚过度激活，定义：

$$
\mathcal{L}_{\mathrm{muscle}} = \sum_{t=1}^{T} \left( \left\| \ddot{\mathbf{r}}_t - L \mathbf{a}_t \right\|_2^2 + \beta_{\mathrm{reg}} \| \mathbf{a}_t \|_2^2 \right)
$$

其中 $L$ 将肌肉激活线性映射为关节加速度，$\beta_{\mathrm{reg}}$ 控制正则化强度。

**自编码器总损失**：重建损失与两项物理损失的加权和，实现端到端的物理感知训练：

$$
\mathcal{L}_{\mathrm{AE}} = \mathcal{L}_{\mathrm{recon}} + \gamma_{\mathrm{euler}} \mathcal{L}_{\mathrm{euler}} + \gamma_{\mathrm{muscle}} \mathcal{L}_{\mathrm{muscle}}
$$

消融实验（Table 8）证实：仅用重建损失时 Muscle Limit 高达 14.614、Penetration 达 8.820；加入全部物理损失后，Muscle Limit 降至 5.264，Penetration 降至 4.954，同时 FID 从 0.611 改善至 0.298，说明物理约束不仅提升合理性，也间接改善了生成自然度。

### 3.2 潜在空间运动扩散模型

在自编码器学到的低维潜在空间中执行条件扩散过程，根据文本提示生成运动序列的潜在表示。前向过程逐步添加高斯噪声：

$$
q(\mathbf{X}_n^e | \mathbf{X}_{n-1}^e) = \mathcal{N}(\mathbf{X}_n^e | \sqrt{1-\beta_n} \mathbf{X}_{n-1}^e, \beta_n \mathbf{I})
$$

扩散模型的训练目标为标准去噪损失：

$$
\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{X_0^e, n, \epsilon} \left[ \| \epsilon - \epsilon_\theta(\mathbf{X}_n^e, n, c) \|_2^2 \right]
$$

其中 $c$ 为文本条件。在潜在空间而非原始运动空间执行扩散，是 FlexMotion 计算效率大幅提升的关键：生成 2048 个运动片段时，推理时间仅需 13.158 秒（DDIM 50 步），而原始空间扩散模型 **MDM**（Tevet et al., 2023）需要 225.283 秒（Table 4），加速约 17 倍。

### 3.3 空间可控性模块

该模块以即插即用方式在预训练扩散模型上添加零初始化的卷积支路，实现对多种运动参数的精细空间/时间控制。其核心设计是：将控制信号 $C^e$ 通过零卷积层 $\mathbf{Z}$ 融入噪声预测网络，零初始化确保训练初期控制模块不干扰预训练模型的生成能力：

$$
\epsilon_{\theta_{\mathrm{total}}}(\mathbf{X}_n^e, C^e, n, c) = \epsilon_\theta(\mathbf{X}_n^e, n, c) + \mathbf{Z}( \epsilon_{\theta_C}(\mathbf{X}_n^e + \mathbf{Z}(C^e, \theta_{z1}), n, c), \theta_{z2} )
$$

最终训练目标为：

$$
\mathcal{L}_{\mathrm{total}} = \mathbb{E}_{X_0^e, C^e, n, \epsilon} \left[ \| \epsilon - \epsilon_{\theta_{\mathrm{total}}}(\mathbf{X}_n^e, C^e, n, c) \|_2^2 \right]
$$

该模块首次支持对肌肉激活、关节驱动力矩、接触力等多维物理参数进行显式控制，而此前方法（如 **OmniControl**（Xie et al., 2023））仅能控制关节位置或轨迹。

## 实验与关键发现

FlexMotion 在 HumanML3D、KIT-ML 和 Flag3D 三个数据集上与多个主流基线进行了全面对比。实验覆盖无条件生成、文本条件生成以及多种空间控制条件下的表现，所有方法均在相同数据集上使用单块 NVIDIA 4090 GPU 重新训练，确保计算资源和数据条件一致。

### 主实验结果

在 HumanML3D 数据集上（Table 1），FlexMotion 在 20% 帧控制条件下取得了 FID 0.198，相比原始运动空间扩散模型 **MDM**（Tevet et al., 2023）的 0.698 降低了 0.500；R-Precision 从 0.602 提升至 0.793。在物理质量指标上，FlexMotion 的 Penetration 为 2.311（MDM 为 11.291），Muscle Limit 为 1.089（MDM 为 16.114），Joint Actuation 为 0.470，Foot Skating 为 0.564，均显著优于所有基线方法。潜在空间扩散模型 **MLD**（Chen et al., 2023）虽在计算效率上接近 FlexMotion，但其物理指标（Penetration 6.100，Muscle Limit 16.114）远不及 FlexMotion。引入物理模拟器校正的 **PhysDiff**（Yuan et al., 2023）在物理指标上有所改善，但仍劣于 FlexMotion 且推理速度更慢。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2501_16778/figures/004_Table_1.jpg]]
*Table 1: HumanML3D test set Guo et al. (2022b): Performance comparisons of text-to-motion synthesis methods. The complete table can be found in the appendix*

在 KIT-ML（Table 2）和 Flag3D（Table 3）数据集上，FlexMotion 保持了相同的优势模式：在生成自然度（FID）和物理合理性（Penetration、Muscle Limit、Joint Actuation、Foot Skating）之间实现了更好的平衡。完整实验结果见附录 Table 5–7。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2501_16778/figures/005_Table_2.jpg]]
*Table 2: KIT-ML test set Plappert et al. (2016): Performance comparisons of text-to-motion synthesis methods. The complete table can be found in the appendix*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2501_16778/figures/006_Table_3.jpg]]
*Table 3: Flag3D test set Tang et al. (2023): Performance comparisons of text-to-motion synthesis methods. The complete table can be found in the appendix*

### 计算效率

Table 4 对比了各方法生成 2048 个运动片段的计算开销。FlexMotion 在 DDIM 50 步采样下的推理时间仅为 13.158 秒，而 MDM 需要 225.283 秒，加速约 17 倍。这得益于扩散过程在低维潜在空间（$1 \times 1024$）中运行，而非原始高维运动表示空间。

### 消融实验

**物理约束的贡献（Table 8）**：仅使用重建损失时，FID 为 0.611，Muscle Limit 高达 14.614，Penetration 为 8.820。加入欧拉-拉格朗日损失 $\mathcal{L}_{\text{euler}}$ 后，Muscle Limit 降至 6.186，Penetration 降至 5.462。进一步加入肌肉损失 $\mathcal{L}_{\text{muscle}}$ 后，FID 改善至 0.298，Muscle Limit 降至 5.264，Penetration 降至 4.954。这表明两项物理约束对运动合理性具有独立且互补的增益。

**潜在空间维度的影响（Table 9）**：$x \in \mathbb{R}^{1 \times 1024}$ 时取得最佳 FID（0.298）和物理指标（MuscleLimit 5.264，Penetration 4.954）。当维度增大至 $1 \times 16384$ 时，FID 恶化至 0.450，MuscleLimit 升至 15.574，Penetration 升至 9.037。这说明适度的压缩有助于去除噪声并保留关键的生物力学信息，过度扩展潜在空间反而引入冗余。

**物理约束权重的权衡（Table 10）**：$\lambda_{\text{euler}}=1.0, \lambda_{\text{muscle}}=1.0$ 时，在真实感（FID 0.298，R-Precision 0.793）与物理准确性（Penetrate 4.954，Skate 0.612）之间取得良好折中。将权重加倍至 2.0 时，Penetrate 进一步降至 3.800，但 FID 升至 0.322，R-Precision 降至 0.785，表明过强的物理约束会损害运动自然度。

### 失败模式与局限性

尽管 FlexMotion 在推理阶段无需物理模拟器，但其训练阶段依赖 OpenSim 进行数据增强，需要额外的计算资源和生物力学专业知识来预处理原始运动数据。模型训练分为自编码器、扩散模型、可控性模块三个串行阶段，流程相对复杂，可能增加工程实现难度。物理约束权重需要在真实感与物理准确性之间手动权衡，默认参数可能不适用于所有应用场景。此外，潜在空间压缩是否丢失了某些高频运动细节，以及可控性模块在极端运动条件下的精度，仍需进一步验证。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2501_16778/figures/011_Table_8.jpg]]
*Table 8: Ablation study results on HumanML3D dataset*

## 定位与知识库关联

### 1. 核心瓶颈与因果杠杆

现有文本到运动生成方法长期面临一个“不可能三角”：**计算效率、物理真实性与细粒度可控性难以兼得**。主流范式可分为两条路径：一是直接在原始运动空间（如 SMPL 关节位置）上运行扩散模型，代表性工作如 **MDM**（Tevet et al., 2023）和 **MotionDiffuse**（Zhang et al., 2022），它们生成质量尚可，但完全缺失显式物理约束，导致穿透、漂浮、肌肉激活不合理等物理伪影频发；二是在扩散过程中引入外部物理模拟器进行后校正，如 **PhysDiff**（Yuan et al., 2023），虽能改善物理指标，却因模拟器调用而显著拖慢推理速度。同时，现有可控生成方法（如 **OmniControl**，Xie et al., 2023）的控制维度几乎仅限于关节位置或轨迹，无法对肌肉激活、关节驱动力矩、接触力等深层动力学参数施加显式操控。

FlexMotion 的因果杠杆在于**将物理约束内化到生成管线的表示层**，而非依赖外部模拟器的事后补救。具体而言，它通过三个耦合设计打破上述三角：

1. **潜在空间操作**：与 **MLD**（Chen et al., 2023）类似，FlexMotion 在低维潜在空间中进行扩散，大幅压缩训练和推理的计算开销。但 FlexMotion 的潜在空间由物理感知自编码器构建，承载了运动学与动力学的联合信息，而非仅压缩关节位置。
2. **端到端物理约束**：在自编码器的解码器端，直接嵌入可微的欧拉-拉格朗日方程损失 $\mathcal{L}_{\mathrm{euler}}$ 和肌肉协调损失 $\mathcal{L}_{\mathrm{muscle}}$，强制重建运动满足骨骼动力学规律和肌肉激活的生理合理性。这使物理真实性成为生成过程的有机组成部分，而非外部模拟器的附属品。
3. **即插即用的多维控制**：在预训练扩散模型上附加零初始化卷积层（零卷积可控性模块），以不干扰原始生成能力的方式引入对空间路径、肌肉激活、关节驱动力矩、接触力等多维参数的显式控制。这是首次在文本到运动生成框架中实现对动力学层面参数的细粒度时空操控。

### 2. 与基线方法的关系定位

FlexMotion 在方法谱系中处于**潜在空间扩散 + 物理感知编码**的交叉点，与以下基线形成明确对比：

- **相对于 MDM / MotionDiffuse**：FlexMotion 保留了扩散模型对运动多样性和文本对齐能力的优势，但通过物理感知自编码器补足了 MDM 完全缺失的物理合理性约束。在 HumanML3D 数据集上，FlexMotion 的 Penetration 指标从 MDM 的 11.291 降至 2.311，Muscle Limit 从 16.114 降至 1.089，同时 FID 从 0.698 改善至 0.198（Table 1），表明物理约束的引入不仅未损害生成质量，反而因潜在空间的规整化效应提升了自然度。
- **相对于 PhysDiff**：PhysDiff 在原始空间扩散的每一步后调用物理模拟器进行投影校正，物理改善以推理速度为代价。FlexMotion 将物理约束前置到自编码器训练阶段，推理时无需任何模拟器介入，在 DDIM 50 步设置下推理时间仅 13.158 秒（vs. PhysDiff 依赖模拟器带来的额外开销，MDM 为 225.283 秒，Table 4），实现了物理合理性与计算效率的兼得。
- **相对于 OmniControl**：OmniControl 提供了灵活的空间控制信号注入机制，但控制对象限于关节位置。FlexMotion 的可控性模块在架构设计上借鉴了零卷积的即插即用思想，但将控制信号的语义维度扩展至肌肉激活、力矩和接触力，这在可控运动生成的维度上构成直接扩展。
- **相对于 MLD**：两者均在潜在空间进行扩散，共享“先压缩再生成”的效率优势。但 MLD 的自编码器仅以重建关节运动学为目标，潜在空间不承载动力学信息；FlexMotion 的多模态自编码器则联合编码七种运动模态（位置、旋转、速度、加速度、肌肉激活、力矩、接触力），并通过物理损失显式约束解码过程，使得潜在空间本身具有物理感知能力。

### 3. 适用边界与局限

尽管 FlexMotion 在多个基准上展现了物理感知生成的潜力，其适用边界存在以下约束：

**训练阶段对 OpenSim 的依赖**。自编码器的训练需要包含肌肉激活、关节力矩和接触力的完整多模态运动数据，这些数据并非现有运动捕捉数据集的原生格式，而是通过 OpenSim 等生物力学仿真平台对原始运动数据进行增强得到。这意味着 FlexMotion 的训练管线需要额外的计算资源和生物力学专业知识来完成数据预处理，限制了其在缺乏此类基础设施的场景下的直接复现。这一依赖在推理阶段被完全解除——模型一旦训练完成，生成过程无需任何外部模拟器——但训练成本的门槛仍然存在。

**三阶段串行训练的工程复杂度**。FlexMotion 的训练分为自编码器预训练、潜在空间扩散模型训练、可控性模块训练三个串行阶段。这种解耦设计虽使各模块职责清晰，但也增加了整体训练流程的工程实现难度和调参负担。特别是，自编码器的物理损失权重（$\gamma_{\mathrm{euler}}$ 和 $\gamma_{\mathrm{muscle}}$）需要在真实感与物理准确性之间手动权衡（Table 10 显示 $\lambda_{\mathrm{euler}}=1.0, \lambda_{\mathrm{muscle}}=1.0$ 为实验最优，但该平衡点可能随数据集和运动类型变化），缺乏自动化的自适应策略。

**潜在空间压缩的信息损失风险**。FlexMotion 将多模态运动序列压缩至 $1 \times 1024$ 维潜在向量（Table 9 消融实验表明该维度取得最佳 FID 和物理指标），但这一压缩比是否会导致高频运动细节（如快速转向时的瞬时加速度变化、精细的手部动作）丢失，论文未进行专门分析。Table 9 显示继续增大潜在维度至 $1 \times 16384$ 反而导致性能下降（FID 升至 0.450，Muscle Limit 升至 15.574），暗示当前 Transformer 自编码器的表示容量或训练策略可能在高维潜在空间下出现优化困难，而非信息压缩本身已饱和。

**可控性模块的极端运动泛化性未验证**。零卷积可控性模块在常见运动类型上展示了有效的多维控制能力，但其在面对训练分布之外的非常规或极端运动（如杂技动作、快速跌倒与恢复）时，控制精度和物理合理性是否依然可靠，论文未提供实验证据。这属于开放问题，需在特定应用场景下进行额外验证。

### 4. 开放问题与后续工作方向

FlexMotion 开辟了物理感知运动生成的新范式，但以下问题有待后续工作探索：

1. **Sim-to-Real 差距的弥合**。当前模型在合成数据（经 OpenSim 增强的运动捕捉数据）上训练和评估，真实世界中采集的运动数据往往缺乏完整的动力学标注（肌肉激活、接触力等难以直接测量）。如何利用稀疏的真实传感器数据（如 IMU、压力鞋垫）来微调或适配 FlexMotion 的物理感知自编码器，是推动其走向实际应用的关键一步。

2. **复杂交互场景的扩展**。FlexMotion 的当前物理约束基于单人骨骼系统的欧拉-拉格朗日方程，未涉及人-物交互（如搬运重物、推拉门）或人-环境交互（如上下楼梯、在不平坦地形行走）的动力学建模。将这些交互力纳入物理损失框架，需要扩展动力学方程并获取相应的交互力标注数据，这是提升模型在具身智能场景中适用性的重要方向。

3. **潜在表示的改进**。Table 9 揭示的潜在维度增大导致性能退化现象，暗示当前基于 Transformer 的自编码器可能存在表示学习的瓶颈。探索 VQ-VAE、层次化潜在结构或流形学习等替代方案，有望在保持物理约束的前提下提升潜在空间的表示效率和生成质量。

4. **物理约束权重的自适应策略**。Table 10 的折中分析表明，物理约束权重对真实感-物理准确性的平衡有显著影响，且最优权重可能需要随运动类型动态调整。设计基于运动上下文的自适应权重调节机制（如根据运动剧烈程度自动缩放 $\gamma_{\mathrm{euler}}$），将减少人工调参负担并提升模型在不同场景下的鲁棒性。

## 原文 PDF

![[paperPDFs/arxiv_2025/FlexMotion:_Lightweight,_Physics-Aware,_and_Controllable_Human_Motion_Generation.pdf]]
