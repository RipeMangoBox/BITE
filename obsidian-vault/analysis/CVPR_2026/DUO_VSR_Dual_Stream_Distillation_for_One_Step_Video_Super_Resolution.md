---
title: "DUO-VSR: Dual-Stream Distillation for One-Step Video Super-Resolution"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DUO_VSR_Dual_Stream_Distillation_for_One_Step_Video_Super_Resolution.pdf
project_link: "https://cszy98.github.io/DUO-VSR/"
code_link: null
aliases:
- DV
- DUO-VSR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 双流蒸馏策略（Dual-Stream Distillation）同时优化DMD流和RFS-GAN流，RFS-GAN利用真实与假分数模型的中间层特征计算对抗损失，注入真实视频的监督信号，抑制退化监督的偏差，并稳定训练过程，从而突破仅靠教师模型的质量瓶颈。
primary_logic: 通过轨迹保持的渐进引导蒸馏提供稳定的单步初始化；然后利用双流蒸馏，将分布匹配与基于噪声样本的对抗训练相结合，引入跨模型多层判别特征作为互补监督；最后通过偏好优化（DPO）进一步对齐感知质量。该框架解决了单步VSR中训练不稳定、监督退化和质量受限的三大难题。
claims:
- 图2展示直接初始化导致训练不稳定（损失和梯度范数波动大），而渐进引导蒸馏初始化显著稳定训练。
- 图2展示真实分数模型输出存在空间偏移和伪影，证明退化监督的存在。
- 表3消融实验证实三阶段各自有效：Stage II（双流蒸馏）使CLIPIQA从0.471提升到0.487，Stage III（偏好精炼）将DOVER从78.01提升到88.15。
- 表4消融显示联合优化优于顺序优化，联合优化在CLIPIQA上达到0.489。
---

# DUO-VSR: Dual-Stream Distillation for One-Step Video Super-Resolution

> [!tip] 核心洞察
> 通过轨迹保持的渐进引导蒸馏提供稳定的单步初始化；然后利用双流蒸馏，将分布匹配与基于噪声样本的对抗训练相结合，引入跨模型多层判别特征作为互补监督；最后通过偏好优化（DPO）进一步对齐感知质量。该框架解决了单步VSR中训练不稳定、监督退化和质量受限的三大难题。

| 字段 | 内容 |
|------|------|
| 中文题名 | DUO-VSR: 面向单步视频超分辨率的双流蒸馏 |
| 英文题名 | DUO-VSR: Dual-Stream Distillation for One-Step Video Super-Resolution |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.22271) · [Project](https://cszy98.github.io/DUO-VSR/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DUO-VSR |
| Dataset | SPMCS, UDM10, YouHQ40, VideoLQ |

> [!tip] 效果简介
> - SPMCS 上，DOVER ↑ 81.47 vs 79.94 (DOVE) (+1.53)。
> - UDM10 上，LPIPS ↓ 0.259 vs 0.267 (SeedVR2-7B) (-0.008)。
> - YouHQ40 上，DOVER ↑ 87.28 vs 84.43 (DOVE) (+2.85)。

## 概述

视频超分辨率（VSR）旨在从低质量视频中恢复高分辨率细节。当前性能最强的方法普遍依赖多步扩散模型，其高昂的推理成本严重阻碍了实际部署。将扩散模型蒸馏为单步模型是一条有前景的加速路径，其中分布匹配蒸馏（DMD）在图像领域已展现出潜力。然而，直接将DMD应用于单步视频超分辨率面临三个核心瓶颈：

1. **训练不稳定**：从预训练多步VSR模型初始化的学生模型，其单步输出分布与真实高分辨率视频差距显著，导致梯度波动剧烈（见Figure 2(a)）。
2. **退化监督**：真实分数模型未曾见过学生输出的带噪版本，可能产生空间偏移或伪影的输出，通过梯度更新污染学生模型（见Figure 2(b)）。
3. **监督不足**：教师模型的质量始终低于真实HR视频，仅靠DMD损失限制了学生模型的性能上限。

针对上述问题，DUO-VSR提出了一个**三阶段双流蒸馏框架**，其核心思路是：通过轨迹保持的渐进引导蒸馏提供稳定初始化；然后利用双流蒸馏将分布匹配与基于噪声样本的对抗训练相结合，引入跨模型多层判别特征作为互补监督；最后通过偏好优化（DPO）进一步对齐感知质量。

在多个基准数据集上的实验表明，DUO-VSR在感知质量上达到最优或次优水平（如SPMCS DOVER 81.47，YouHQ40 DOVER 87.28），同时推理速度比SeedVR-7B快约50倍（见Figure 1）。消融研究证实，三阶段各自发挥关键作用：双流蒸馏将CLIPIQA从0.471提升至0.487，偏好精炼将DOVER从78.01提升至88.15（见Table 3）；联合优化显著优于顺序优化（见Table 4）。该方法解决了单步VSR中训练不稳定、监督退化和质量受限的三大难题，在效率与质量之间取得了突破性平衡。

## 背景与动机

### 视频超分辨率的效率困境

视频超分辨率（VSR）旨在从低质量、低分辨率的视频序列中恢复出高分辨率、细节丰富的对应版本。近年来，基于扩散模型的VSR方法在生成质量上取得了显著进展，但其推理效率严重制约了实际部署。如图1所示，扩散模型方法通常需要数十甚至数百步采样才能生成单帧结果——以**MGLD**为代表的运动引导潜在扩散方法在21帧1080p视频上耗时956.7秒（约16分钟），而基于文本到视频扩散的**STAR**和**UAV**（Zhou et al., CVPR 2024）等方法同样面临高昂的计算开销。这种效率瓶颈源于扩散模型固有的迭代去噪机制：每一步都需要通过大型神经网络（如1.3B参数的DiT）进行完整前向传播，将推理时间推至不可接受的水平。

### 单步VSR的兴起与分布匹配蒸馏

为突破效率瓶颈，研究者开始探索将多步扩散模型蒸馏为单步生成器的路径。分布匹配蒸馏（Distribution Matching Distillation, DMD）成为这一方向的核心技术，其基本思想是通过匹配学生模型与教师模型在扩散轨迹上的分数函数，将多步采样压缩为单步前向传播。近期工作如**DOVE**、**SeedVR2-7B**、**UltraVSR**和**FlashVSR-Full**等均已尝试将DMD应用于VSR任务，实现了推理速度的量级提升。

然而，直接将DMD应用于单步VSR面临三个深层问题，这些问题构成了本工作的核心动机。

### 三大核心瓶颈

**瓶颈一：训练不稳定。** 当学生模型直接从预训练的多步VSR教师模型初始化时，其在单步设置下的输出分布与真实高分辨率（HR）视频之间存在显著差距。这种分布不匹配导致DMD训练过程中的损失函数和梯度范数出现剧烈波动。如图2(a)所示，直接初始化的模型在第二阶段蒸馏中表现出明显的训练震荡，而这种现象会阻碍模型收敛至高质量解。

**瓶颈二：退化监督。** DMD依赖真实分数模型（real score model）提供梯度信号。然而，真实分数模型是在真实HR视频上训练的，从未见过学生模型生成的带噪样本。如图2(b)所示，当面对学生输出的分布外样本时，真实分数模型可能产生空间偏移的输出（前两例绿色框标注）或包含明显伪影的结果（第三例蓝色框标注）。这些有偏差的梯度通过反向传播污染学生模型，形成“退化监督”——即教师模型非但不能正确引导学生，反而将自身的错误模式注入学生。

**瓶颈三：监督不足与质量上限。** DMD损失本质上要求学生模型逼近教师模型的输出分布，但教师模型本身的质量始终低于真实HR视频。这意味着仅靠DMD损失存在一个隐性的性能天花板——学生模型无论如何优化，其上限都被教师模型的质量所束缚。对于追求高感知质量的VSR任务而言，这一限制尤为致命。

### 本文动机与核心思路

上述三大瓶颈——训练不稳定、退化监督、质量受限——并非孤立存在，而是相互耦合的：不稳定的训练加剧了退化监督的负面影响，而退化监督又进一步压缩了本就受限的质量空间。因此，单一的技术改进难以同时解决这三个问题。

本文提出**DUO-VSR**，一个基于**双流蒸馏**（Dual-Stream Distillation）的三阶段框架。其核心洞察在于：通过引入一条与DMD并行的对抗学习流（RFS-GAN），利用真实与假分数模型的中间层特征作为判别信号，可以同时实现三个目标——（1）注入真实视频的监督信号以突破教师模型的质量瓶颈；（2）通过多模型特征互补抑制退化监督的偏差；（3）借助对抗训练的稳定性机制平滑整体优化过程。在此基础上，配合轨迹保持的渐进引导蒸馏初始化和偏好精炼后处理，构建从初始化到优化的完整解决方案。

## 核心创新

DUO-VSR 的核心创新在于提出了一套**三阶段蒸馏框架**，系统性地解决了将分布匹配蒸馏（DMD）直接应用于单步视频超分辨率（VSR）时面临的三大瓶颈：训练不稳定、退化监督、以及质量上限受限。该框架通过三个关键的技术改变（changed slots）实现了突破。

### 1. 训练初始化：从直接初始化到渐进引导蒸馏

直接将预训练的多步 VSR 模型作为单步学生模型的初始化，会导致学生输出分布与真实 HR 视频差距过大，进而引发梯度不稳定（见 Figure 2(a)）。DUO-VSR 改变了这一初始化方式，引入**轨迹保持的渐进引导蒸馏初始化**（Progressive Guided Distillation Initialization）。

该阶段由两步组成：
- **CFG 蒸馏（CFG Distillation）**：训练学生模型匹配条件与无条件扩散分支的合并输出，损失函数为：
  $$\mathcal{L}_{CFG}(\theta_S) = \mathbb{E}_{t, z_0^{HR}} || v_{\theta_S}(z_t^{HR}, t, z^{LR}, c) - v_{cfg} ||^2$$
- **渐进蒸馏（Progressive Distillation）**：通过匹配教师模型的两步预测结果，渐进地将学生蒸馏为单步模型，损失函数为：
  $$\mathcal{L}_{PD}(\theta_S) = \mathbb{E}_{t, z_0^{HR}} || \underbrace{z_t^{HR} - (t - t'') v_{\theta_S}(z_t^{HR})}_{\xi_{t''}} - \underbrace{\tilde{z}_{t''}^{HR}(\theta)}_{\xi_{t'}} ||^2$$

这一改变为后续的双流蒸馏提供了稳定的优化起点。

### 2. 损失函数与对抗训练方式：从单一 DMD 损失到双流蒸馏

传统 DMD 仅依赖真实分数模型（real score model）与假分数模型（fake score model）的分数差来更新学生。然而，真实分数模型未曾见过学生输出的带噪版本，可能产生空间偏移或伪影的输出，形成**退化监督**（见 Figure 2(b)）；同时，教师模型的质量始终低于真实 HR 视频，导致**监督不足**。

DUO-VSR 的核心改变是提出**双流蒸馏策略**（Dual-Stream Distillation），同时优化两个互补的监督流：

- **DMD 流（分布匹配）**：利用真实和假分数模型计算 DMD 损失，以 stop-gradient 方式优化学生：
  $$\mathcal{L}_{DMD}(\theta_S) = \mathbb{E}_{t, \hat{z}_0^S} || \hat{z}_0^S - \mathrm{sg}[\hat{z}_0^S - \mathrm{Grad}] ||^2$$
  其中假分数模型通过扩散损失持续追踪学生分布：
  $$\mathcal{L}_{Diff}(\theta_F) = \mathbb{E}_{t, \hat{\mathbf{z}}_0^S} || \mathbf{v}_{\theta_F}(\hat{\mathbf{z}}_t^S, t, \mathbf{z}^{LR}, \mathbf{c}) - \mathbf{v} ||^2$$

- **RFS-GAN 流（对抗监督）**：这是关键的对抗训练方式改变——**基于噪声扰动的样本**，利用真实和假分数模型的多层中间特征构建判别器，计算 hinge GAN 损失和特征匹配损失：
  $$\mathcal{L}_D = \mathbb{E}[\max(0, 1 - D(z_t^{HR}))] + \mathbb{E}[\max(0, 1 + D(\hat{z}_t^S))]$$
  $$\mathcal{L}_G = -\mathbb{E}[D(\hat{\mathbf{z}}_t^S)]$$

RFS-GAN 流注入真实视频的监督信号，有效抑制了退化监督的偏差，并突破了仅靠教师模型的质量瓶颈。消融实验证实，RFS-GAN 结合真实与假分数模型优于单一模型（Table 5）。

### 3. 优化策略：从仅更新学生到交替更新

DUO-VSR 改变了优化策略，采用**学生更新与辅助更新交替进行**的方式：每 $N=3$ 次辅助更新（更新假分数模型和判别器）进行一次学生更新。学生更新的总损失为三个损失的加权和：
$$\mathcal{L}_S = \lambda_{DMD}\mathcal{L}_{DMD} + \lambda_{GAN}\mathcal{L}_G + \lambda_{FM}\mathcal{L}_{FM}$$
其中权重分别为 1.0、0.1、0.05。消融实验进一步表明，**联合优化**（Joint）显著优于顺序优化（Seq.），在 CLIPIQA 上达到 0.489 vs 0.419（Table 4）。

### 4. 后处理/精炼：从无到偏好引导精炼

DUO-VSR 增加了第三阶段**偏好引导精炼**（Preference-Guided Refinement）。通过构建偏好数据集（优选样本纹理丰富自然，劣选样本存在伪影或模糊，见 Figure 8），使用直接偏好优化（DPO）损失对生成器进行微调，鼓励模型向优选样本的速度场靠近：
$$-\mathbb{E}[\log \sigma(-\frac{\beta_t}{2}(||\mathbf{v}^w - \mathbf{v}_{\theta_s}(\hat{z}_t^{S_w})||^2 - ||\mathbf{v}^w - \mathbf{v}_{\theta_{ref}}(\hat{z}_t^{S_w})||^2 - (||\mathbf{v}^l - \mathbf{v}_{\theta_S}(\hat{\mathbf{z}}_t^{S_l})||^2 - ||\mathbf{v}^l - \mathbf{v}_{\theta_{ref}}(\hat{\mathbf{z}}_t^{S_l})||^2)))]$$

消融实验证实，该阶段将 DOVER 从 88.01 进一步提升至 88.15（Table 3）。

### 创新总结

上述四个 changed slots 构成了 DUO-VSR 的完整创新链条：渐进引导蒸馏提供稳定初始化 → 双流蒸馏（DMD + RFS-GAN）联合优化突破质量瓶颈 → 偏好精炼进一步对齐感知质量。这一框架使 DUO-VSR 在多个基准上取得最优或次优的感知质量，同时推理速度比 SeedVR-7B 快约 50 倍（Figure 1, Table 1）。

## 整体框架

DUO-VSR 是一个三阶段单步视频超分辨率蒸馏框架，核心由**渐进引导蒸馏初始化**、**双流蒸馏**和**偏好引导精炼**三个阶段级联构成（图3）。框架的输入为低分辨率视频帧序列及其对应的文本嵌入，输出为单步生成的高分辨率视频。

### 阶段一：渐进引导蒸馏初始化（Progressive Guided Distillation Initialization）

该阶段的目标是为后续双流蒸馏提供一个稳定的单步学生模型初始化，而非直接从预训练多步VSR模型进行硬初始化。它包含两个子步骤：

1. **CFG蒸馏（CFG Distillation）**：训练学生模型匹配教师模型在条件与无条件扩散分支的合并输出速度场，使学生初步具备条件引导下的去噪能力。
2. **渐进蒸馏（Progressive Distillation）**：通过匹配教师模型的两步预测结果，将学生逐步压缩为单步生成模型。这一步保持了教师模型的去噪轨迹，避免了直接单步初始化导致的输出分布剧烈偏移。

图2(a)的实验证据表明，直接初始化会导致第二阶段训练中损失和梯度范数剧烈波动，而渐进引导蒸馏初始化显著稳定了训练过程。

### 阶段二：双流蒸馏（Dual-Stream Distillation）

这是DUO-VSR的核心创新，同时优化两条互补的监督流：

- **DMD流（DMD Stream）**：基于分布匹配蒸馏，利用真实分数模型（real score model）和假分数模型（fake score model）的分数差计算KL散度梯度，驱动学生模型输出分布向真实HR视频分布靠拢。
- **RFS-GAN流（RFS-GAN Stream）**：以真实和假分数模型的中间层作为判别骨干，在噪声扰动样本上计算hinge GAN损失和特征匹配损失，注入真实视频的对抗监督信号。

两条流通过**交替优化**协同工作：每进行N=3次辅助更新（更新假分数模型和判别器）后进行一次学生更新。学生总损失为DMD损失、GAN生成器损失和特征匹配损失的加权和，权重分别为1.0、0.1、0.05。RFS-GAN流的关键作用在于抑制真实分数模型产生的退化监督——图2(b)显示真实分数模型偶尔会输出空间偏移或含伪影的结果，若仅依赖DMD流，这些偏差会通过梯度更新污染学生模型。

### 阶段三：偏好引导精炼（Preference-Guided Refinement）

在前两阶段基础上，构建生成偏好数据集（包含视觉质量更优的“优选”样本和相对较差的“劣选”样本），使用直接偏好优化（DPO）损失对生成器进行微调。DPO损失鼓励学生模型的速度场向优选样本靠近、远离劣选样本，从而进一步提升感知质量。表3消融实验证实，该阶段将DOVER指标从88.01进一步提升至88.15。

### 模块关系与数据流

整体框架的数据流可概括为：低分辨率视频帧 → 视频VAE编码为潜在表示 → 基础VSR DiT（1.3B参数，默认50步采样）作为教师模型 → 阶段一输出单步学生初始化 → 阶段二双流蒸馏联合优化学生与辅助模型 → 阶段三偏好微调 → 最终单步生成器输出高分辨率潜在表示 → 视频VAE解码为高分辨率视频帧。

> **注意**：视频VAE采用8倍空间和4倍时间压缩，在推理时成为主要计算瓶颈，占总运行时的90%以上。

### 补充图表

![[assets/figures/papers/paper_list_l863_https_arxiv_org_abs_2603_22271/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our three-stage distillation framework. (a) We initialize the student model with trajectory-preserving Progressive Guided Distillation, which consists of CFG Distillation and Progressive Distillation steps. (b) The core of our method, Dual-Stream Distillation, jointly optimizes the DMD and RFS-GAN streams through alternating Student Update and Auxiliary Update, providing reliable and sufficient supervision. (c) In the final stage, we construct a generated preference dataset and apply DPO-based Preference-Guided Refinement to enhance perceptual quality*

## 核心模块与公式推导

DUO-VSR 围绕一个三阶段蒸馏框架构建，其核心是将分布匹配与对抗监督统一的双流蒸馏策略。以下按模块拆解关键组件与公式。

### 基础 VSR 扩散模型

方法建立在视频扩散 Transformer（DiT）之上，该模型以低分辨率潜变量 $z^{LR}$ 和文本嵌入 $\mathbf{c}$ 为条件，从噪声样本中预测干净的高分辨率潜变量。基础模型参数量约 10 亿，默认需 50 步采样。训练时，HR 潜变量按如下方式加噪：

$$z_t^{HR} = (1 - t) z_0^{HR} + t \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

其中 $t \in [0, 1]$ 控制噪声强度。模型通过预测目标速度 $\mathbf{v}$ 进行训练：

$$\mathcal{L}(\theta) = \mathbb{E}_{t, z_0^{HR}} \|\mathbf{v}_\theta(z_t^{HR}, t, z^{LR}, \mathbf{c}) - \mathbf{v}\|^2$$

### Stage I：渐进引导蒸馏初始化

直接将预训练多步模型作为单步学生初始化会导致训练不稳定（损失和梯度范数剧烈波动，见 Figure 2(a)）。为此，DUO-VSR 采用轨迹保持的渐进引导蒸馏，分两步提供稳定初始化。

![[assets/figures/papers/paper_list_l863_https_arxiv_org_abs_2603_22271/figures/002_Figure_2.jpg]]
*Figure 2: (a) Effect of initialization on the stability of the second-stage training. The proposed progressive guided distillation initialization leads to more stable loss and gradient norm trends during the second-stage distillation. (b) Compared with the fake score model, the real score model occasionally produces outputs that are spatially shifted relative to the inputs (highlighted in green boxes in the first two cases) or contain artifacts (blue boxes in the third case), leading to degraded supervision propagated to the student model*

**CFG 蒸馏**：训练学生模型匹配条件与无条件扩散分支的合并输出：

$$\mathcal{L}_{CFG}(\theta_S) = \mathbb{E}_{t, z_0^{HR}} \|v_{\theta_S}(z_t^{HR}, t, z^{LR}, c) - v_{cfg}\|^2$$

**渐进蒸馏**：通过匹配教师模型的两步预测结果，逐步将学生蒸馏为单步模型。令 $t'$ 和 $t''$ 为相邻时间步，损失函数为：

$$\mathcal{L}_{PD}(\theta_S) = \mathbb{E}_{t, z_0^{HR}} \|\underbrace{z_t^{HR} - (t - t'') v_{\theta_S}(z_t^{HR})}_{\xi_{t''}} - \underbrace{\tilde{z}_{t''}^{HR}(\theta)}_{\xi_{t'}}\|^2$$

这一阶段为后续双流优化提供了稳定的参数起点。

### Stage II：双流蒸馏

双流蒸馏是 DUO-VSR 的核心创新，同时优化 DMD 流和 RFS-GAN 流，解决直接 DMD 存在的退化监督与监督不足问题。

**DMD 流**：利用真实分数模型 $s_{real}$（预训练教师）和假分数模型 $s_{fake}$（在线追踪学生分布）的分数差计算 KL 散度梯度：

$$\nabla_\theta D_{KL} = \mathbb{E}_\epsilon [-(s_{real}(z_t^{HR}) - s_{fake}(z_t^{HR})) \frac{dv}{d\theta_S}]$$

假分数模型通过扩散损失持续更新以追踪学生分布：

$$\mathcal{L}_{Diff}(\theta_F) = \mathbb{E}_{t, \hat{\mathbf{z}}_0^S} \|\mathbf{v}_{\theta_F}(\hat{\mathbf{z}}_t^S, t, \mathbf{z}^{LR}, \mathbf{c}) - \mathbf{v}\|^2$$

DMD 损失以 stop-gradient 方式优化学生：

$$\mathcal{L}_{DMD}(\theta_S) = \mathbb{E}_{t, \hat{\mathbf{z}}_0^S} \|\hat{\mathbf{z}}_0^S - \mathrm{sg}[\hat{\mathbf{z}}_0^S - \mathrm{Grad}]\|^2$$

**RFS-GAN 流**：以真实和假分数模型的中间层特征作为判别骨干，采用 hinge GAN 目标。判别器损失：

$$\mathcal{L}_D = \mathbb{E}[\max(0, 1 - D(z_t^{HR}))] + \mathbb{E}[\max(0, 1 + D(\hat{z}_t^S))]$$

生成器损失：

$$\mathcal{L}_G = -\mathbb{E}[D(\hat{\mathbf{z}}_t^S)]$$

同时引入特征匹配损失 $\mathcal{L}_{FM}$，计算真假分数模型中间特征的均方误差，提供多层互补监督。

**学生总损失**为三者的加权和：

$$\mathcal{L}_S = \lambda_{DMD} \mathcal{L}_{DMD} + \lambda_{GAN} \mathcal{L}_G + \lambda_{FM} \mathcal{L}_{FM}$$

权重分别设为 1.0、0.1、0.05。优化采用交替策略：每 $N=3$ 次辅助更新（更新假分数模型和判别器）后进行一次学生更新，确保训练稳定。

### Stage III：偏好引导精炼

为进一步对齐感知质量，构建生成偏好数据集（优选样本纹理丰富自然，劣选样本存在伪影或模糊），使用 DPO 损失微调生成器：

$$-\mathbb{E}[\log \sigma(-\frac{\beta_t}{2}(\|\mathbf{v}^w - \mathbf{v}_{\theta_S}(\hat{z}_t^{S_w})\|^2 - \|\mathbf{v}^w - \mathbf{v}_{\theta_{ref}}(\hat{z}_t^{S_w})\|^2 - (\|\mathbf{v}^l - \mathbf{v}_{\theta_S}(\hat{\mathbf{z}}_t^{S_l})\|^2 - \|\mathbf{v}^l - \mathbf{v}_{\theta_{ref}}(\hat{\mathbf{z}}_t^{S_l})\|^2)))]$$

该损失鼓励生成器速度场向优选样本靠近，远离劣选样本，$\beta_t$ 控制偏好强度。

### 补充图表

![[assets/figures/papers/paper_list_l863_https_arxiv_org_abs_2603_22271/figures/014_Figure_10.jpg]]
*Figure 10: Discriminator features from the real and fake score models used for the RFS-GAN loss computation, reduced to three dimensions via t-SNE [39] for visualization*

## 实验与分析

### 主结果：感知质量与推理效率的双重突破

表1汇总了DUO-VSR在合成、真实世界和AIGC三类基准上的定量对比。在感知质量指标上，DUO-VSR在多个数据集上取得最优或次优结果：SPMCS上DOVER达到81.47，比次优方法**DOVE**高出+1.53；UDM10上LPIPS降至0.259，优于**SeedVR2-7B**的0.267；YouHQ40上DOVER达到87.28，领先**DOVE**达+2.85。在无参考质量方面，VideoLQ上NIQE降至4.08，AIGC60上CLIP-IQA达到0.4886，均优于对比方法。值得注意的是，这些感知质量的提升并未以牺牲推理效率为代价——表2显示，DUO-VSR在单GPU上处理21帧1080p视频仅需11.3秒，比扩散模型方法**MGLD**（956.7秒）快约85倍，比**SeedVR-7B**快约50倍（图1气泡图）。图4的可视化对比进一步印证：DUO-VSR在合成数据、真实降质视频和AIGC内容上均能重建更丰富的纹理细节，同时保持时序一致性（图5）。

### 三阶段蒸馏消融：各阶段不可或缺

表3的消融实验逐阶段验证了框架设计的有效性。移除Stage I（渐进引导蒸馏初始化）直接进行DMD蒸馏，导致CLIPIQA从0.487骤降至0.414，DOVER从88.01跌至76.32，印证了直接初始化带来的训练不稳定会严重损害最终质量。Stage II（双流蒸馏）相比仅使用DMD流，将CLIPIQA从0.471提升至0.487，DOVER从78.01大幅提升至88.01，证明RFS-GAN流注入的真实视频监督有效突破了教师模型的质量上限。Stage III（偏好精炼）在DOVER上进一步从88.01提升至88.15，其他指标亦有改善，显示偏好对齐能够精细调校感知质量。图6的可视化消融与定量趋势一致：缺少任一阶段均导致纹理模糊或伪影增加。

### 双流蒸馏策略：联合优化与判别器设计

表4对比了双流蒸馏中联合优化（Joint）与顺序优化（Seq.）的差异。联合优化在CLIPIQA上达到0.489，显著优于顺序优化的0.419，说明DMD流与RFS-GAN流需要相互约束、同步更新才能发挥互补作用——顺序优化中先训练某一流会破坏另一流的监督信号平衡。

表5进一步消融RFS-GAN的判别器设计。仅使用真实分数模型或仅使用假分数模型作为判别骨干，性能均不及两者结合：双模型组合在NIQE上达4.64，MUSIQ达63.36。图10的t-SNE可视化揭示了原因——真实与假分数模型的中间层特征在空间中呈互补分布，联合使用能够提供更丰富的判别信息，有效抑制单一模型带来的退化监督偏差。

### 失败模式与局限性分析

尽管DUO-VSR在感知质量上表现优异，论文明确指出了两个结构性局限。第一，整个框架基于潜在空间训练，视频VAE采用8倍空间压缩和4倍时间压缩，这种高压缩比可能阻碍极细粒度细节（如微小文字）的准确重建。第二，视频VAE成为推理时的主要计算瓶颈，占总运行时间的90%以上，限制了端到端加速的进一步空间。这些局限指向一个开放问题：如何设计更高效的视频VAE，在保留高频细节和时序连贯性的同时大幅加速解码过程。

### 公平性保障

所有推理速度测试在同一设备上使用相同分辨率（1920×1080）和帧数（21帧）进行，模型参数量仅统计生成器部分。定量评估采用统一的基准数据集和标准指标（PSNR、SSIM、LPIPS、NIQE、MUSIQ、CLIP-IQA、DOVER、E_warp）。用户研究采用盲测GSB方法，由20位计算机视觉背景研究人员进行主观评价（表7），DUO-VSR在“好/相当/差”三项上均取得最优。

### 补充图表

![[assets/figures/papers/paper_list_l863_https_arxiv_org_abs_2603_22271/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparisons on benchmarks, including synthetic (SPMCS [55], UDM10 [81], YouHQ40 [96]), real-world (VideoLQ [4]), and AIGC (AIGC60) videos. The best and second performances are marked in red and blue respectively*

![[assets/figures/papers/paper_list_l863_https_arxiv_org_abs_2603_22271/figures/011_Table_3.jpg]]
*Table 3: Ablation on Three Stage Distillation*

![[assets/figures/papers/paper_list_l863_https_arxiv_org_abs_2603_22271/figures/010_Table_4.jpg]]
*Table 4: Ablation on Dual-Stream Distillation Strategy. “Joint” and “Seq.” denote different optimization schemes*

![[assets/figures/papers/paper_list_l863_https_arxiv_org_abs_2603_22271/figures/015_Table_5.jpg]]
*Table 5: Ablation study on the discriminator design of RFS-GAN*

![[assets/figures/papers/paper_list_l863_https_arxiv_org_abs_2603_22271/figures/007_Table_2.jpg]]
*Table 2: Inference efficiency comparison. Measured on a single GPU using a 21-frame 1920 × 1080 video. The model parameters are counted only for the generator part*

![[assets/figures/papers/paper_list_l863_https_arxiv_org_abs_2603_22271/figures/017_Table_6.jpg]]
*Table 6: Quantitative comparison on the AIGC60 dataset*

![[assets/figures/papers/paper_list_l863_https_arxiv_org_abs_2603_22271/figures/001_Figure_1.jpg]]
*Figure 1: Inference Speed and Performance Comparison. The bubble chart on the left compares model parameter scale, inference time, and DOVER score across methods, with inference speed measured on a single GPU using a 21-frame, 1920 × 1080 resolution video. The right-side images show super-resolution results for different videos. Our method not only demonstrates remarkable detail generation capabilities but also achieves superior inference efficiency, accelerating inference speed by approximately 50× compared to SeedVR-7B*

![[assets/figures/papers/paper_list_l863_https_arxiv_org_abs_2603_22271/figures/006_Figure_5.jpg]]
*Figure 5: Comparison of temporal consistency. Extracted and stacked along the blue line in the width–temporal plane*

![[assets/figures/papers/paper_list_l863_https_arxiv_org_abs_2603_22271/figures/012_Figure_8.jpg]]
*Figure 8: Examples of preferred and less-preferred samples in the constructed preference dataset. Zoom in for details*

## 方法谱系与知识库定位

### 单步视频超分辨率的方法演进

DUO-VSR 处于单步视频超分辨率（One-Step VSR）这一新兴方向的前沿。该方向的核心目标是将多步扩散/生成模型的推理成本压缩至单次前向传播，同时尽可能保留甚至提升生成质量。理解 DUO-VSR 的位置，需要回顾从多步到单步的蒸馏路径以及相关对抗训练方法的演进。

#### 多步扩散VSR的教师模型基础

DUO-VSR 的教师模型是一个约 1.3B 参数的视频扩散 Transformer（Video DiT），默认需 50 步采样才能生成干净的高分辨率视频。该模型以低分辨率潜变量 $z^{LR}$ 和文本嵌入 $\mathbf{c}$ 为条件，通过预测目标速度 $\mathbf{v}$ 进行训练：

$$\mathcal{L}(\theta) = \mathbb{E}_{t, z_0^{HR}} \|\mathbf{v}_\theta(z_t^{HR}, t, z^{LR}, \mathbf{c}) - \mathbf{v}\|^2$$

这一基础架构代表了当前扩散式 VSR 的主流范式，与 **UAV (Upscale-A-Video)**（Zhou et al., CVPR 2024）、**STAR** 等基于扩散模型的时序一致性 VSR 方法共享相似的生成框架。然而，50 步采样的计算开销使得这类方法难以满足实时或低延迟应用需求，这正是单步蒸馏的驱动力所在。

#### 从 DMD 到单步 VSR 的直接尝试与困境

分布匹配蒸馏（Distribution Matching Distillation, DMD）是连接多步扩散模型与单步生成器的关键桥梁。其核心思想是通过真实分数模型 $s_{\mathrm{real}}$ 与假分数模型 $s_{\mathrm{fake}}$ 的分数差来估计 KL 散度的梯度，从而更新学生模型：

$$\nabla_\theta D_{KL} = \mathbb{E}_\epsilon [-(s_{\mathrm{real}}(z_t^{HR}) - s_{\mathrm{fake}}(z_t^{HR})) \frac{dv}{d\theta_{\mathrm{S}}}]$$

**DOVE** 和 **FlashVSR-Full** 等方法率先将 DMD 引入 VSR 领域，试图直接将预训练的多步 VSR 教师蒸馏为单步学生。然而，DUO-VSR 的分析揭示了这个直接迁移路径的三个根本性瓶颈：

1. **训练不稳定**：从预训练多步 VSR 模型直接初始化的学生模型，在单步设置下输出分布与真实 HR 视频差距巨大，导致损失和梯度范数剧烈波动（见 Figure 2(a)）。
2. **退化监督**：真实的分数模型未曾见过学生输出的带噪版本，可能产生空间偏移或伪影的输出，通过梯度更新污染学生模型（见 Figure 2(b)）。
3. **监督不足**：教师模型的质量始终低于真实 HR 视频，仅靠 DMD 损失限制了学生模型的性能上限。

这三个瓶颈构成了 DUO-VSR 方法设计的直接动因，也解释了为何此前的单步 VSR 方法（如 **UltraVSR**、**DLoRAL**）在感知质量上始终存在明显差距。

#### 对抗训练在 VSR 中的角色演变

对抗训练在图像/视频生成中历史悠久，但在单步 VSR 蒸馏中的系统引入尚属首次。**SeedVR2-7B** 采用了对抗后训练策略，在单步 VSR 中取得了较强的感知质量（如 UDM10 上 LPIPS 达 0.267），但其对抗训练基于干净输出，缺乏对噪声扰动的鲁棒性。DUO-VSR 的 RFS-GAN 流创新性地将真实和假分数模型同时作为判别骨干，利用其多层中间特征计算 hinge GAN 损失和特征匹配损失：

$$\mathcal{L}_D = \mathbb{E}[\max(0, 1 - D(z_t^{HR}))] + \mathbb{E}[\max(0, 1 + D(\hat{z}_t^S))]$$

$$\mathcal{L}_G = -\mathbb{E}[D(\hat{\mathbf{z}}_t^S)]$$

这一设计的独特之处在于：判别器不仅区分真假样本，还通过分数模型的特征空间捕捉分布层面的差异。消融实验（Table 5）证实，结合真实与假分数模型的 RFS-GAN 优于仅使用单一模型（NIQE 4.64, MUSIQ 63.36），表明两类特征具有互补性。

#### 偏好优化在生成模型中的延伸

偏好优化（DPO）最初在语言模型中用于对齐人类偏好，DUO-VSR 将其引入 VSR 蒸馏的第三阶段。通过构建包含优选（纹理丰富自然）和劣选样本的偏好数据集，使用 DPO 损失对生成器进行微调：

$$-\mathbb{E}[\log \sigma(-\frac{\beta_t}{2}(\|\mathbf{v}^w - \mathbf{v}_{\theta_s}(\hat{z}_t^{S_w})\|^2 - \|\mathbf{v}^w - \mathbf{v}_{\theta_{\mathrm{ref}}}(\hat{z}_t^{S_w})\|^2 - (\|\mathbf{v}^l - \mathbf{v}_{\theta_{\mathrm{S}}}(\hat{\mathbf{z}}_t^{S_l})\|^2 - \|\mathbf{v}^l - \mathbf{v}_{\theta_{\mathrm{ref}}}(\hat{\mathbf{z}}_t^{S_l})\|^2)))]$$

这一做法将感知质量的对齐问题形式化为速度场的偏好优化，为 VSR 的后处理精炼提供了新的范式。消融实验（Table 3）显示，Stage III 将 DOVER 从 88.01 进一步提升至 88.15，验证了偏好精炼的独立增益。

### 方法适用边界与局限

#### 适用场景

DUO-VSR 在以下场景展现出显著优势：

- **高分辨率视频的实时/低延迟超分**：在 21 帧 1080p 视频上推理仅需 11.3 秒，比 **MGLD**（956.7 秒）快约 85 倍，比 **SeedVR-7B** 快约 50 倍（Table 2）。
- **合成、真实世界与 AIGC 视频的通用超分**：在 SPMCS（DOVER 81.47）、UDM10（LPIPS 0.259）、YouHQ40（DOVER 87.28）、VideoLQ（NIQE 4.08）和 AIGC60（CLIP-IQA 0.4886）五个异构基准上均取得最优或次优感知质量（Table 1, Table 6）。
- **需要时序一致性的视频增强**：通过轨迹保持的渐进蒸馏初始化，DUO-VSR 在时序一致性指标 $E_{warp}^*$ 上表现优异（Figure 5）。

#### 已知局限

1. **极细粒度细节的重建受限**：由于视频 VAE 采用 8 倍空间压缩和 4 倍时间压缩，潜在空间训练可能阻碍微小文字等极细粒度细节的忠实重建。这是当前潜在扩散模型的共性局限，非 DUO-VSR 特有。

2. **视频 VAE 成为推理瓶颈**：VAE 解码占总运行时的 90% 以上，使得生成器部分的加速收益被部分抵消。这一瓶颈指向了未来工作的关键方向。

3. **训练流程的复杂性**：三阶段训练（渐进引导蒸馏 → 双流蒸馏 → 偏好精炼）虽然有效，但增加了训练流程的复杂度和调参成本。目前缺乏对超参数敏感性的系统分析。

### 开放问题与未来方向

1. **高效视频 VAE 的设计**：如何设计既能保留高频细节和时序连贯性，又能大幅加速解码过程的视频 VAE？这是提升 DUO-VSR 端到端推理速度的关键瓶颈。

2. **与现有单步 VSR 框架的兼容性**：DUO-VSR 的双流蒸馏策略能否与 **InfVSR**、**FlashVSR** 等基于 DMD 的单步 VSR 框架结合，进一步提升鲁棒性和视觉质量？这需要验证 RFS-GAN 流在不同基础架构上的迁移性。

3. **偏好数据集的自动化构建**：当前偏好数据集的构建依赖人工筛选或启发式规则，如何设计自动化的感知质量排序机制（如基于 CLIP-IQA + DOVER 的联合评分）以规模化偏好精炼？

4. **更激进的压缩比**：是否可能将教师模型的采样步数从 50 步进一步压缩至单步，同时保持与多步教师相当的感知质量？这需要在蒸馏损失设计和对抗监督强度上进行更深入的探索。

5. **跨模态扩展**：双流蒸馏策略中的 RFS-GAN 判别器设计（利用分数模型特征）是否适用于其他生成任务（如文本到视频生成、视频编辑）的单步蒸馏？

## 原文 PDF

![[paperPDFs/CVPR_2026/DUO_VSR_Dual_Stream_Distillation_for_One_Step_Video_Super_Resolution.pdf]]
