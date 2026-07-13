---
title: "MotionRFT: Unified Reinforcement Fine-Tuning for Text-to-Motion Generation"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: "paperPDFs/arxiv_2026/MotionRFT:_Unified_Reinforcement_Fine-Tuning_for_Text-to-Motion_Generation.pdf"
project_link: null
code_link: null
aliases:
- MotionRFT
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过逐步独立的奖励最大化（EasyTune）并结合停止梯度操作，解耦跨步递归梯度依赖，实现稠密、内存高效的更新；同时利用统一异构表示奖励模型（MotionReward）提供多维度的奖励信号。
primary_logic: 通过将异构运动表示映射到由文本锚定的共享语义空间，构建统一的多维度奖励模型（MotionReward），并利用逐步去噪奖励优化（EasyTune）克服递归梯度瓶颈，从而在多种运动表示上高效实现语义对齐、人类偏好和真实性等多目标的强化微调。
claims:
- EasyTune achieves FID 0.132 with 22.10 GB peak memory, saving up to 15.22 GB over DRaFT.
- MotionRFT improves R-Precision Top1 on HY Motion by 12.6% and FID by 23.3%.
- EasyTune reduces FID by 22.9% on joint-based ACMDM.
- HumanML3D 上 FID = 0.132
---

# MotionRFT: Unified Reinforcement Fine-Tuning for Text-to-Motion Generation

> [!tip] 核心洞察
> 通过将异构运动表示映射到由文本锚定的共享语义空间，构建统一的多维度奖励模型（MotionReward），并利用逐步去噪奖励优化（EasyTune）克服递归梯度瓶颈，从而在多种运动表示上高效实现语义对齐、人类偏好和真实性等多目标的强化微调。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionRFT：面向文本到运动生成的统一强化微调 |
| 英文题名 | MotionRFT: Unified Reinforcement Fine-Tuning for Text-to-Motion Generation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.27185) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MotionRFT |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，FID 0.132 vs 0.450 (MLD) (-70.7%)；R-Precision Top 1 0.581 vs 0.504 (MLD) (+15.3%)；FID 0.101 (MLD + MotionRFT) vs 0.450 (MLD) (-77.6%)。

## 概要

**问题瓶颈**：现有基于可微奖励的文本到运动生成微调方法（如 **DRaFT** (Clark et al., ICLR 2024)、**AlignProp** (Prabhudesai et al., 2023)）需要对整个去噪链进行递归梯度反向传播。由于每一步的梯度依赖于后续所有步的累积计算，导致三个核心瓶颈：(1) 内存消耗随去噪步数 $T$ 线性增长至 $\mathcal{O}(T)$；(2) 梯度在长链传播中逐渐消失，使早期步骤几乎无法获得有效优化信号；(3) 仅对最终生成样本的整体奖励进行粗粒度优化，无法对中间去噪步骤施加精细化控制。

**核心方案**：MotionRFT 提出了一套统一的强化微调框架，包含两个关键组件：

- **MotionReward**：统一的异构运动表示奖励模型。通过轻量线性投影将不同运动表示（如基于关节的、基于旋转的、基于运动学的）映射到以文本为锚点的共享语义空间，联合学习语义对齐、人类偏好和运动真实性三个维度的奖励信号，克服了以往奖励模型仅支持单一表示、单一评价维度的局限。

- **EasyTune**：逐步独立的可微奖励优化方法。核心洞察在于，通过停止梯度操作将递归梯度依赖解耦，使每个去噪步骤独立接收奖励信号并直接优化，将内存复杂度从 $\mathcal{O}(T)$ 降至 $\mathcal{O}(1)$，同时实现细粒度的逐步更新。配合课程时间步调度，平衡早期高噪声步骤与后期低噪声步骤的优化强度。

**主要结果**：在 HumanML3D 基准上，基于 **MLD** (Chen et al., CVPR 2023) 预训练模型，MotionRFT 将 FID 从 0.450 降至 0.101（-77.6%），R-Precision Top 1 从 0.504 提升至 0.593（+17.6%）；基于 **HY Motion** (Team, 2025) 旋转流模型，FID 从 0.073 降至 0.056（-23.3%），R-Precision Top 1 提升 12.6%。EasyTune 在峰值内存仅 22.10 GB 的条件下达到 FID 0.132，相比 DRaFT 节省 15.22 GB 显存。该框架在六种不同预训练扩散模型上均展现出一致的性能提升，验证了其对异构运动表示的通用性。

文本到运动生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的三维人体运动序列，在动画制作、游戏开发和虚拟人交互等领域具有广泛应用。近年来，扩散模型（Diffusion Models）和流匹配（Flow Matching）方法在该任务上取得了显著进展，涌现出多种基于不同运动表示（如运动学特征、关节旋转、关节坐标）的预训练生成模型，包括 **MLD**（Chen et al., CVPR 2023）、**MDM**（Tevet et al., ICLR 2023）、**ACMDM**（Meng et al., 2025）和 **HY Motion**（Team, 2025）等。

然而，这些预训练模型在生成质量上仍存在明显不足：生成的运动可能与文本描述语义不一致，缺乏物理真实性，或与人类审美偏好存在偏差。为弥合这一差距，研究者开始探索将强化微调（Reinforcement Fine-Tuning）引入运动生成领域，通过奖励模型（Reward Model）对生成结果进行评分并反向传播梯度来优化生成模型。代表性工作包括基于可微奖励的 **DRaFT**（Clark et al., ICLR 2024）、**AlignProp**（Prabhudesai et al., 2023），以及基于偏好优化的 **Motion-Critic**（Wang et al., ICLR 2025）和 **SoPo**（Tan et al., NeurIPS 2025）等。

### 现有方法的瓶颈

尽管上述方法在特定场景下有效，但存在两个根本性瓶颈：

**1. 奖励模型的表示局限性。** 现有奖励模型通常针对单一运动表示（如运动学特征）设计，且仅评估单一维度（如语义对齐或人类偏好）。当面对不同表示（运动学特征、关节旋转、关节坐标）的生成模型时，需要分别训练独立的奖励模型，缺乏统一的评估框架。这种异构性阻碍了多维度奖励（语义对齐、人类偏好、运动真实性）的联合学习。

**2. 微调策略的效率瓶颈。** 现有可微奖励微调方法（如DRaFT）通过完整的去噪链反向传播梯度，即对最终生成样本 $\mathbf{x}_0^\theta$ 计算奖励 $\mathcal{R}_\phi(\mathbf{x}_0^\theta)$ 后，将梯度递归地传播至所有中间去噪步骤 $\mathbf{x}_t^\theta$。这导致三个严重问题：
- **内存消耗过大**：需要存储完整的去噪计算图，内存复杂度为 $O(T)$（$T$ 为去噪步数），在实际训练中峰值内存可达 37.32 GB；
- **优化效率低下**：跨步递归梯度依赖使得每次更新仅能获得稀疏的梯度信号，且梯度范数随去噪步数增加而急剧衰减（梯度消失），如 Figure 4 所示；
- **优化粒度粗糙**：仅对最终生成样本的整体奖励进行优化，无法对中间去噪步骤进行细粒度的独立指导。

从梯度分解的角度来看，如 Corollary 1 所揭示：

$$
\frac{\partial\mathbf{x}_{t-1}^{\theta}}{\partial\theta} = \underbrace{\frac{\partial\pi_{\theta}(\mathbf{x}_{t}^{\theta},t,c)}{\partial\theta}}_{\mathrm{direct~term}} + \underbrace{\frac{\partial\pi_{\theta}(\mathbf{x}_{t}^{\theta},t,c)}{\partial\mathbf{x}_{t}^{\theta}}\cdot\frac{\partial\mathbf{x}_{t}^{\theta}}{\partial\theta}}_{\mathrm{indirect~term}}
$$

其中间接项（indirect term）包含了跨步递归梯度依赖，是内存膨胀和梯度衰减的根源。现有方法无法有效解耦这一依赖，成为高效强化微调的核心障碍。

### 本文动机

针对上述瓶颈，本文提出 **MotionRFT**——一个统一的强化微调框架，核心动机包含两个方面：

- **构建统一的多维度奖励模型**：将异构运动表示映射到由文本锚定的共享语义空间，使单一模型能够同时学习语义对齐、人类偏好和运动真实性三个维度的奖励信号，从而为不同表示的生成模型提供一致的评估标准。

- **设计高效细粒度的微调策略**：通过逐步独立的奖励最大化（EasyTune）并结合停止梯度（stop-gradient）操作，解耦跨步递归梯度依赖，将内存复杂度从 $O(T)$ 降至 $O(1)$，同时使每个去噪步骤都能获得稠密的奖励信号，实现细粒度优化。

## 核心方法与创新机理

MotionRFT 的核心创新在于同时解决了文本到运动生成中**奖励建模的表示异构性**和**可微微调的递归梯度瓶颈**两个根本问题，形成了一套从多维度评估到高效优化的闭环框架。

### 创新一：统一异构表示的多维度奖励模型 MotionReward

现有奖励模型通常针对单一运动表示（如关节位置或旋转）设计，且仅优化单一维度（如语义对齐），无法跨骨架、跨表示泛化。MotionReward 的关键突破在于构建了一个**以文本为锚点的共享语义空间**，将异构运动表示统一映射到同一嵌入空间中进行多维度奖励学习。

具体而言，MotionReward 通过以下机制实现统一：

1. **轻量级投影适配**：为每种运动表示 $o \in \mathcal{O}$ 设计独立的线性投影层 $\boldsymbol{\phi}^o$，将异构运动 $\mathbf{x}^o$ 映射到共享特征空间 $\mathbf{h}^o \in \mathbb{R}^{T \times d}$（$d=256$），如公式所示：
   $$\mathbf{h}^o = \boldsymbol{\phi}^o(\mathbf{x}^o), \quad \forall o \in \mathcal{O}$$
   这使得模型能够处理关节位置、旋转矩阵、SMPL 参数等多种表示，无需修改核心架构。

2. **文本锚定的语义对齐**：共享运动编码器 $\mathcal{E}_{\mathrm{M}}$ 和文本编码器 $\mathcal{E}_{\mathrm{T}}$ 分别输出对角高斯后验参数，通过重构损失、KL 散度、潜在一致性损失、对比 InfoNCE 损失和跨表示对齐损失（CRA）联合优化，确保不同表示的运动在语义空间中与对应文本紧密对齐。最终语义训练目标为：
   $$\mathcal{L}_{\mathrm{sem}} = \mathcal{L}_{\mathrm{rec}} + \lambda_1 \mathcal{L}_{\mathrm{kl}} + \lambda_2 \mathcal{L}_{\mathrm{lat}} + \lambda_3 \mathcal{L}_{\mathrm{cl}} + \lambda_4 \mathcal{L}_{\mathrm{CRA}}$$

3. **多维度奖励解耦学习**：在冻结的共享骨干网络上附加任务特定的 LoRA 适配器 $\Delta\theta_\psi$（偏好）和 $\Delta\theta_\omega$（真实性），分别学习：
   - **语义对齐奖励**：基于统一语义空间评估文本-运动匹配度
   - **人类偏好奖励**：通过排名损失 $\mathcal{L}_{\mathrm{pref}} = -\mathbb{E}_{(\mathbf{x}^{\mathrm{w},o}, \mathbf{x}^{\mathrm{l},o})} \log \sigma(h_\psi(\mathbf{z}^{\mathrm{w}}) - h_\psi(\mathbf{z}^{\mathrm{l}}))$ 学习人类偏好排序
   - **真实性奖励**：通过鉴别器判断运动是否来自真实分布

这一设计使单一奖励模型能够同时输出多维度反馈，为后续微调提供丰富的优化信号。

### 创新二：解耦递归梯度的逐步高效微调 EasyTune

现有可微奖励微调方法（如 **DRaFT** (Clark et al., ICLR 2024)、**AlignProp** (Prabhudesai et al., 2023)）需要对整个去噪链进行反向传播，存在三个根本性缺陷：

- **内存爆炸**：需存储全部 $T$ 步的计算图，内存复杂度为 $O(T)$
- **优化稀疏**：奖励信号仅作用于最终生成样本，中间步骤缺乏直接监督
- **梯度消失**：梯度经 $T$ 步递归传播后指数衰减，早期步骤几乎无法学习

EasyTune 的核心洞察在于：**将递归梯度依赖替换为逐步独立的奖励最大化**。具体而言，传统方法的梯度需通过完整去噪链递归计算：
$$\frac{\partial \mathcal{L}(\theta)}{\partial \theta} = -\mathbb{E}\left[\frac{\partial \mathcal{R}_\phi(\mathbf{x}_0^\theta)}{\partial \mathbf{x}_0^\theta} \cdot \frac{\partial \mathbf{x}_0^\theta}{\partial \theta}\right]$$
其中 $\frac{\partial \mathbf{x}_0^\theta}{\partial \theta}$ 需要沿链式法则展开 $T$ 步。

EasyTune 通过**停止梯度**操作截断递归依赖，将优化目标重新定义为在每个去噪步骤 $t$ 上独立最大化奖励：
$$\mathcal{L}_{\mathrm{EasyTune}}(\theta) = -\mathbb{E}_{c \sim \mathbb{D}_{\mathbf{T}}, \mathbf{x}_t^\theta \sim \pi_\theta(\cdot|c), t \sim \mathcal{U}(0,T)}\left[\mathcal{R}_\phi(\mathbf{x}_t^\theta, t, c)\right]$$

这一设计带来三个关键优势：

1. **内存 $O(1)$**：每次仅需存储单步计算图，峰值内存从 DRaFT 的 37.32 GB 降至 22.10 GB，节省 15.22 GB
2. **细粒度优化**：每个去噪步骤独立接收奖励信号，实现逐步骤的稠密监督
3. **规避梯度消失**：梯度仅需传播一层去噪网络，不受递归累积影响

### 创新三：课程时间步调度与自精炼偏好学习

为进一步提升 EasyTune 的优化效果，MotionRFT 引入两个补充机制：

- **课程时间步调度**：由于早期高噪声步骤的运动与洁净运动差异大（Fig. 5），直接优化可能导致学习不充分。课程调度从高噪声步向低噪声步逐步收缩优化窗口，平衡早期结构生成与后期细节精炼。

- **自精炼偏好学习**：通过硬负样本挖掘自动构建偏好对，利用 KL 散度 $\mathcal{L}_{\mathrm{SPL}}(\phi) = D_{\mathrm{KL}}(\mathcal{Q} \parallel \mathcal{P})$ 将奖励分布 $\mathcal{P}$ 对齐到目标分布 $\mathcal{Q}$，无需额外人工标注即可增强语义奖励的判别力。

### 创新总结

MotionRFT 的三个创新形成了完整的因果链条：MotionReward 提供统一、多维度的评估信号 → EasyTune 以内存高效、细粒度的方式将这些信号反馈到生成模型 → 课程调度与自精炼学习进一步稳定和增强优化过程。这一框架首次实现了在多种运动表示（关节位置、旋转、SMPL）和多种基座模型（MLD、MDM、ACMDM、HY Motion）上的统一强化微调，为文本到运动生成的对齐提供了通用解决方案。

MotionRFT 是一个统一的强化微调框架，旨在解决文本到运动生成中跨去噪步骤递归梯度依赖导致的内存爆炸、优化稀疏和梯度消失问题。框架由两个核心模块构成：**MotionReward**（异构表示统一奖励模型）和 **EasyTune**（逐步可微奖励微调方法），二者协同实现高效、细粒度的多目标对齐。

### 框架总览

整个 pipeline 的输入是文本描述 $c$ 和一个预训练的扩散/流式运动生成模型 $\pi_\theta$，输出是经过多维度奖励信号微调后的生成模型。框架的运行逻辑分为两个阶段：

1. **奖励建模阶段**：MotionReward 接受异构运动表示（如 kinematic、joint-based、rotation-based），通过轻量级线性投影将它们映射到由文本锚定的共享语义空间，并联合学习语义对齐、人类偏好和运动真实性三个维度的奖励信号。
2. **微调阶段**：EasyTune 在去噪过程的每一步独立采样时间步 $t \sim \mathcal{U}(0,T)$，对当前步的噪声运动 $\mathbf{x}_t^\theta$ 直接计算 MotionReward 的奖励 $\mathcal{R}_\phi(\mathbf{x}_t^\theta, t, c)$，并通过停止梯度操作解耦跨步递归依赖，实现 $\mathcal{O}(1)$ 内存复杂度的细粒度参数更新。

### 模块关系与数据流

MotionReward 和 EasyTune 之间的数据流是单向的：MotionReward 作为冻结的奖励评估器，为 EasyTune 提供多维度的标量奖励信号；EasyTune 则利用这些信号以逐步独立的方式更新生成模型参数。两个模块的设计相互解耦——MotionReward 可以独立训练和评估，EasyTune 可以适配任意预训练扩散/流式模型。

**MotionReward 内部结构**（Fig. 2）：
- **统一投影层**：针对每种运动表示 $o \in \mathcal{O}$ 配备特定的轻量级投影器 $\phi^o$，将异构运动 $\mathbf{x}^o$ 映射到共享特征空间 $\mathbf{h}^o = \phi^o(\mathbf{x}^o) \in \mathbb{R}^{T \times d}$（$d=256$）。
- **共享表示学习**：共享运动编码器 $\mathcal{E}_\mathrm{M}$ 和文本编码器 $\mathcal{E}_\mathrm{T}$ 分别输出对角高斯后验参数，通过 VAE 框架学习统一的语义潜在空间。训练目标整合了重构损失 $\mathcal{L}_\mathrm{rec}$、KL 损失 $\mathcal{L}_\mathrm{kl}$、潜在一致性损失 $\mathcal{L}_\mathrm{lat}$、对比 InfoNCE 损失 $\mathcal{L}_\mathrm{cl}$ 和跨表示对齐损失 $\mathcal{L}_\mathrm{CRA}$，整体语义损失为：
  $$\mathcal{L}_{\mathrm{sem}} = \mathcal{L}_{\mathrm{rec}} + \lambda_{1}\mathcal{L}_{\mathrm{kl}} + \lambda_{2}\mathcal{L}_{\mathrm{lat}} + \lambda_{3}\mathcal{L}_{\mathrm{cl}} + \lambda_{4}\mathcal{L}_{\mathrm{CRA}}$$
- **多偏好学习分支**：在冻结的骨干网络上附加两个任务特定的 LoRA 适配器 $\Delta\theta_\psi$（偏好建模）和 $\Delta\theta_\omega$（真实性建模）。偏好奖励通过排名损失 $\mathcal{L}_{\mathrm{pref}} = -\mathbb{E}_{(\mathbf{x}^{\mathrm{w},o},\mathbf{x}^{\mathrm{l},o})}\log\sigma\big(h_{\psi}(\mathbf{z}^{\mathrm{w}}) - h_{\psi}(\mathbf{z}^{\mathrm{l}})\big)$ 训练，真实性奖励通过鉴别器区分真实运动与 deepfake 样本训练。
- **自精炼偏好学习（SPL）**：通过硬负样本挖掘自动构建偏好对，利用 KL 散度 $\mathcal{L}_{\mathrm{SPL}}(\phi) = D_{\mathrm{KL}}(\mathcal{Q} \parallel \mathcal{P})$ 精炼语义奖励，无需额外人工标注。

**EasyTune 核心机制**（Fig. 3, Fig. 7）：
- 现有可微奖励方法（如 DRaFT、AlignProp）需要对完整去噪链进行递归梯度反向传播，内存复杂度为 $\mathcal{O}(T)$，且因梯度消失导致早期步骤优化稀疏。
- EasyTune 的训练目标为：
  $$\mathcal{L}_{\mathrm{EasyTune}}(\theta) = -\mathbb{E}_{c\sim\mathbb{D}_{\mathbf{T}},\mathbf{x}_{t}^{\theta}\sim\pi_{\theta}(\cdot|c),t\sim\mathcal{U}(0,T)}\left[\mathcal{R}_{\phi}(\mathbf{x}_{t}^{\theta},t,c)\right]$$
  其关键洞察在于用逐步梯度替代递归梯度。根据 Corollary 1，反转过程输出对参数的全导数分解为直接项和间接递归项：
  $$\frac{\partial\mathbf{x}_{t-1}^{\theta}}{\partial\theta} = \underbrace{\frac{\partial\pi_{\theta}(\mathbf{x}_{t}^{\theta},t,c)}{\partial\theta}}_{\mathrm{direct~term}} + \underbrace{\frac{\partial\pi_{\theta}(\mathbf{x}_{t}^{\theta},t,c)}{\partial\mathbf{x}_{t}^{\theta}}\cdot\frac{\partial\mathbf{x}_{t}^{\theta}}{\partial\theta}}_{\mathrm{indirect~term}}$$
  EasyTune 通过停止梯度操作截断间接项，仅保留直接项，从而将内存降至 $\mathcal{O}(1)$，并实现每个去噪步骤的稠密、独立优化。
- **课程时间步调度**：引入从高噪声到低噪声步的课程窗口调度，平衡早期（结构形成）与晚期（细节精炼）步骤的优化强度，避免早期高噪声步骤学习不充分。

### 框架的关键优势

1. **表示统一性**：MotionReward 的共享语义空间使同一奖励模型可服务于多种运动表示（kinematic、joint-based、rotation-based），无需为每种表示单独训练奖励模型。
2. **内存高效性**：EasyTune 的峰值 GPU 内存仅 22.10 GB，相比 DRaFT 的 37.32 GB 节省 15.22 GB（Fig. 9），使得在消费级 GPU 上进行强化微调成为可能。
3. **优化细粒度**：逐步独立优化使每个去噪步骤都能接收奖励信号，避免了传统方法仅对最终生成样本进行粗粒度整体奖励优化的局限。
4. **多目标协同**：语义对齐、人类偏好和真实性三维度奖励联合优化，消融实验表明多维奖励相比单方面奖励能一致提升生成质量（Tab. III, Fig. 11）。

### 需要人工验证的点

- 课程时间步调度的具体窗口衰减函数和超参数设置在现有分析中未明确给出，需对照原文 Sec. IV-B 的 Eq. (26) 确认。
- SPL 的硬负样本挖掘策略的具体实现细节（如负样本采样比例、阈值）在分析中未展开，对复现有关键影响。

![[assets/figures/papers/paper_list_l3315_https_arxiv_org_abs_2603_27185/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MotionReward, consisting of unified projection, representation, and multiple preference learning*

![[assets/figures/papers/paper_list_l3315_https_arxiv_org_abs_2603_27185/figures/003_Figure_3.jpg]]
*Figure 3: The framework of existing differentiable reward-based methods (left) and our proposed EasyTune (right). Existing methods backpropagate the gradients of the reward model through the overall denoising process, resulting in (1) excessive memory, (2) inefficient, and (3) coarse-grained optimization. In contrast, EasyTune optimizes the diffusion model by directly backpropagating the gradients at each denoising step, overcoming these issues*

MotionRFT 由两个互补的核心模块构成：**MotionReward**（统一异构表示的多维奖励模型）与 **EasyTune**（逐步去噪奖励微调方法）。前者为生成模型提供稠密、多维度的反馈信号，后者则解决现有可微奖励微调中因跨步递归梯度依赖而导致的内存爆炸与优化稀疏问题。

### MotionReward：统一异构运动表示的奖励模型

现有奖励模型通常仅针对单一运动表示和单一评价维度设计，难以泛化到不同的运动骨架与表示形式。MotionReward 的核心思路是：**将异构运动表示映射到由文本锚定的共享语义空间，并在该空间内联合学习语义对齐、人类偏好和运动真实性三个维度的奖励信号**。

#### 统一表示学习

对于不同表示的运动 $`\mathbf{x}^{o}`$（如关节位置、旋转、SMPL 参数等），MotionReward 首先通过轻量线性投影层将其映射到共享特征空间：

$$`\mathbf{h}^{o} = \boldsymbol{\phi}^{o}(\mathbf{x}^{o}) \in \mathbb{R}^{T \times d}, \quad \forall o \in \mathcal{O}`$$

其中 $`d = 256`$ 为共享特征维度。随后，共享运动编码器 $`\mathcal{E}_{\mathrm{M}}`$ 和文本编码器 $`\mathcal{E}_{\mathrm{T}}`$ 分别输出对角高斯后验的均值与方差：

$$`\mu_{m}^{o}, \sigma_{m}^{o} = \mathcal{E}_{\mathrm{M}}(\mathbf{h}^{o}), \quad \mu_{c}, \sigma_{c} = \mathcal{E}_{\mathrm{T}}(c), \quad \forall o \in \mathcal{O}`$$

通过重参数化采样得到潜在变量 $`\mathbf{z}_{m}^{o}`$ 和 $`\mathbf{z}_{c}`$，再由解码器重建运动特征和文本特征。语义保真度由重构损失保证：

$$`\mathcal{L}_{\mathrm{rec}} = \ell_{1}(\hat{\mathbf{x}}_{c}^{o}, \mathbf{x}^{o}) + \ell_{1}(\hat{\mathbf{x}}_{m}^{o}, \mathbf{x}^{o}) + \ell_{1}(\hat{\mathbf{x}}_{m}^{o}, \hat{\mathbf{x}}_{c}^{o})`$$

其中 $`\ell_{1}`$ 为平滑 Huber 损失，三项分别约束文本解码、运动解码与原始运动之间的一致性。

为增强文本与运动嵌入的判别对齐，引入 InfoNCE 对比损失：

$$`{\mathcal{L}}_{\mathrm{info}}(\mathbf{a},\mathbf{b}) = -\mathbb{E}\left[\log\frac{\exp(s_{ii}/\tau)}{\sum_{j}\exp(s_{ij}/\tau)} + \log\frac{\exp(\bar{s}_{ii}/\tau)}{\sum_{j}\exp(\bar{s}_{ij}/\tau)}\right]`$$

最终语义训练目标整合重构、KL 散度、潜在一致性、对比和跨表示对齐损失：

$$`{\mathcal{L}}_{\mathrm{sem}} = {\mathcal{L}}_{\mathrm{rec}} + \lambda_{1}{\mathcal{L}}_{\mathrm{kl}} + \lambda_{2}{\mathcal{L}}_{\mathrm{lat}} + \lambda_{3}{\mathcal{L}}_{\mathrm{cl}} + \lambda_{4}{\mathcal{L}}_{\mathrm{CRA}}`$$

#### 多维偏好学习

在统一语义空间的基础上，MotionReward 冻结骨干参数 $`\theta`$，附加两个轻量 LoRA 适配器 $`\Delta\theta_{\psi}`$ 和 $`\Delta\theta_{\omega}`$，分别建模人类偏好奖励和运动真实性奖励。

**偏好奖励**通过排名损失学习，使模型对高质量运动赋予更高分数：

$$`\mathcal{L}_{\mathrm{pref}} = -\mathbb{E}_{(\mathbf{x}^{\mathrm{w},o},\mathbf{x}^{\mathrm{l},o})}\log\sigma\big(h_{\psi}(\mathbf{z}^{\mathrm{w}}) - h_{\psi}(\mathbf{z}^{\mathrm{l}})\big)`$$

其中 $`h_{\psi}`$ 为偏好评分头，$`\sigma`$ 为 sigmoid 函数。

**自我精炼偏好学习（SPL）** 进一步通过硬负样本挖掘构建偏好对，无需额外人工标注即可增强语义奖励。SPL 将奖励分数经 Softmax 归一化后与目标分布 $`\mathcal{Q}`$ 对齐：

$$`\mathcal{P} = \operatorname{Softmax}\big(\mathcal{R}_{\phi}(\mathbf{x}^{\mathrm{w}}, c), \mathcal{R}_{\phi}(\mathbf{x}^{\mathrm{l}}, c)\big)`$$

$$`{\mathcal{L}}_{\mathrm{SPL}}(\phi) = D_{\mathrm{KL}}(\mathcal{Q} \parallel \mathcal{P})`$$

### EasyTune：逐步去噪奖励微调

#### 递归梯度瓶颈分析

现有可微奖励微调方法（如 **DRaFT**，Clark et al., ICLR 2024）对最终生成样本 $`\mathbf{x}_{0}^{\theta}`$ 的整体奖励 $`\mathcal{R}_{\phi}(\mathbf{x}_{0}^{\theta})`$ 进行优化，梯度需沿整个去噪链反向传播。设去噪过程为 $`\mathbf{x}_{t-1}^{\theta} = \pi_{\theta}(\mathbf{x}_{t}^{\theta}, t, c)`$，则中间状态对参数的全导数为：

$$`\frac{\partial\mathbf{x}_{t-1}^{\theta}}{\partial\theta} = \underbrace{\frac{\partial\pi_{\theta}(\mathbf{x}_{t}^{\theta},t,c)}{\partial\theta}}_{\mathrm{direct~term}} + \underbrace{\frac{\partial\pi_{\theta}(\mathbf{x}_{t}^{\theta},t,c)}{\partial\mathbf{x}_{t}^{\theta}}\cdot\frac{\partial\mathbf{x}_{t}^{\theta}}{\partial\theta}}_{\mathrm{indirect~term}}`$$

间接项 $`\frac{\partial\mathbf{x}_{t}^{\theta}}{\partial\theta}`$ 递归地依赖所有后续步骤的梯度，导致三个问题：
1. **内存 O(T)**：需存储完整去噪链的计算图；
2. **梯度稀疏**：早期步骤的梯度经多层链式传播后范数急剧衰减（Fig. 4 验证了此梯度消失现象）；
3. **优化粗粒度**：仅最终样本接收奖励信号，中间步骤缺乏直接监督。

![[assets/figures/papers/paper_list_l3315_https_arxiv_org_abs_2603_27185/figures/006_Figure_4.jpg]]
*Figure 4: Gradient norm with respect to denoising steps. Here, dim(·) denotes the gradient dimension*

#### EasyTune 的核心解耦

EasyTune 的关键洞察是：**用逐步独立的奖励最大化替代轨迹级递归优化**。具体而言，在均匀采样的时间步 $`t \sim \mathcal{U}(0, T)`$ 上，直接对中间状态 $`\mathbf{x}_{t}^{\theta}`$ 的奖励进行优化：

$$`\mathcal{L}_{\mathrm{EasyTune}}(\theta) = -\mathbb{E}_{c\sim\mathbb{D}_{\mathbf{T}},\mathbf{x}_{t}^{\theta}\sim\pi_{\theta}(\cdot|c),t\sim\mathcal{U}(0,T)}\left[\mathcal{R}_{\phi}(\mathbf{x}_{t}^{\theta},t,c)\right]`$$

通过停止梯度操作截断间接递归项，EasyTune 将内存复杂度从 $`\mathcal{O}(T)`$ 降至 $`\mathcal{O}(1)`$，同时使每个去噪步骤独立接收稠密的奖励信号，实现细粒度优化（Fig. 7 展示了这一解耦机制）。

#### 课程时间步调度

直接对所有时间步均匀采样可能导致早期高噪声步骤学习不充分——这些步骤的噪声运动与洁净运动相似度极低（Fig. 5），奖励信号信噪比差。为此引入课程时间步调度，从高噪声步逐步过渡到低噪声步，平衡早期结构形成与后期细节精炼的优化。

> **注意**：课程调度的具体公式 Eq. (26) 在给定材料中未完整呈现，此处仅根据分析记录其作用机制。如需精确形式，请查阅原文 Sec. IV-B。

![[assets/figures/papers/paper_list_l3315_https_arxiv_org_abs_2603_27185/figures/005_Figure_6.jpg]]
*Figure 6: Memory usage comparison. Here, “w/o*

## 实验与关键发现

### 主实验结果

MotionRFT在多个预训练基座和运动表示上均取得了一致的性能提升，验证了其作为通用强化微调框架的有效性。

**基于MLD的运动学扩散模型微调。** 在HumanML3D基准上，MLD经MotionRFT微调后，FID从0.450降至0.101（-77.6%），R-Precision Top1从0.504提升至0.593（+17.6%）。与DRaFT等现有可微奖励微调方法相比，MotionRFT在FID指标上达到0.132，同时将峰值GPU内存从37.32 GB降至22.10 GB，节省达15.22 GB。这一结果直接验证了EasyTune在解耦递归梯度依赖后带来的内存效率优势。

**基于HY Motion的旋转表示流模型微调。** MotionRFT在HY Motion上同样展现出显著提升：R-Precision Top1从0.563提升至0.634（+12.6%），FID从0.073降至0.056（-23.3%）。这表明MotionReward的统一语义空间能够有效对齐异构运动表示，使奖励信号跨表示迁移。

**跨模型泛化性。** Figure 1(b)展示了MotionRFT在六种预训练扩散模型上的泛化性能，包括**MLD**（Chen et al., CVPR 2023）、**MDM**（Tevet et al., ICLR 2023）、**ACMDM**（Meng et al., 2025）等。所有模型经微调后FID均有显著下降，验证了框架的基座无关性。

### 消融实验

**逐步优化 vs. 全链优化。** 在HumanML3D上，EasyTune的逐步优化策略在FID（0.132）上优于类DRaFT的全轨迹链式优化，同时内存占用仅为后者的约60%。这证实了逐步独立奖励最大化在生成质量和计算效率上的双重优势。

**多维度奖励的贡献。** MotionReward同时提供语义对齐、人类偏好和真实性三维度奖励。消融显示，仅使用单一语义奖励时，FID和R-Precision均出现退化；加入偏好和真实性奖励后，生成质量持续改善。Figure 11展示了训练过程中真实性和偏好奖励曲线的稳定上升趋势，表明多维度奖励信号能够协同优化。

**SPL vs. ReAlign。** 自精炼偏好学习（SPL）通过硬负样本挖掘构建偏好对，无需额外人工标注。在HumanML3D和KIT-ML上的文本-运动检索准确率对比显示，SPL在R-Precision Top1/2/3上均优于ReAlign，验证了合成偏好数据增强语义奖励的有效性。

**课程时间步调度。** 引入课程时间步调度后，模型在早期高噪声步骤和晚期低噪声步骤之间实现了更均衡的优化。消融表明，去除调度会导致FID上升，说明仅依赖均匀时间步采样可能使早期步骤学习不充分。

### 奖励模型评估

**文本-运动检索。** MotionReward在三种运动表示（关节位置、旋转、SMPL参数）上的文本-运动检索准确率均达到领先水平（Table I），验证了统一语义空间对异构表示的对齐能力。

**人类偏好预测。** 在人类偏好预测任务上，MotionReward与Motion-Critic（Wang et al., ICLR 2025）的直接对比（Table II）显示，MotionReward在偏好预测准确率上表现更优。值得注意的是，Motion-Critic原为24关节表示设计，在22关节设定下经复现后仍不及MotionReward。

### 计算效率分析

Figure 9展示了优化过程中的内存轨迹：EasyTune保持O(1)的内存占用，而DRaFT等全链反向传播方法的内存随去噪步数线性增长。Figure 10进一步显示，EasyTune在达到相同奖励分数时所需的每步训练时间显著更短，验证了逐步独立优化在计算开销上的优势。

### 失败模式与局限性

尽管MotionRFT在多个维度上表现优异，仍存在以下局限：

1. **物理真实性不足。** 当前框架未集成物理仿真，生成的运动会存在脚部滑动、接触不自然等动力学问题。Figure 8的运动真实性评估显示，虽然真实性奖励能部分缓解该问题，但距离物理级真实仍有差距。

2. **真实性奖励的泛化瓶颈。** MotionReward的真实性判别器训练依赖合成deepfake样本，可能未覆盖真实世界中的运动异常类型，在分布外运动上的判别能力需要手动验证。

3. **早期步骤优化不足。** 在未启用课程时间步调度时，高噪声步骤的梯度范数极小（Figure 4），导致这些步骤几乎不被优化。课程调度缓解了该问题，但最优调度策略仍有探索空间。

### 用户研究

Figure 13的用户研究结果显示，MotionRFT在运动自然度、文本一致性和整体偏好三项主观指标上均优于未微调基座和DRaFT微调模型。这进一步验证了多维度奖励（特别是人类偏好奖励）对生成质量的主观提升。

![[assets/figures/papers/paper_list_l3315_https_arxiv_org_abs_2603_27185/figures/015_Table.jpg]]
*Table: V COMPARISON OF FINE-TUNING METHODS ON HUMANML3D*

![[assets/figures/papers/paper_list_l3315_https_arxiv_org_abs_2603_27185/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of the training costs and generation performance on HumanML3D [15]. (a) Performance comparison of different fine-tuning methods [23], [39], [40]. (b) Generalization performance across six pre-trained diffusion-based models [7], [8], [14], [41], [42]*

## 定位与知识库关联

### 1. 与现有文本-运动生成基线的继承关系

MotionRFT 并非从头设计一个生成模型，而是构建在多个预训练扩散/流模型之上的统一微调框架。论文验证的基底模型覆盖了运动生成领域三种主流范式：

- **运动学潜变量扩散模型**：**MLD** (Chen et al., CVPR 2023) 和 **MDM** (Tevet et al., ICLR 2023)，两者在潜空间或原始运动空间进行去噪生成，是当前运动学运动生成的代表性基线。
- **关节级扩散模型**：**ACMDM** (Meng et al., 2025)，直接对关节坐标进行扩散建模。
- **旋转表示流模型**：**HY Motion** (Team, 2025)，基于连续归一化流在旋转空间生成运动。

MotionRFT 的关键创新在于提出**表示无关的统一奖励模型 MotionReward**，通过轻量线性投影将上述异构运动表示映射到由文本锚定的共享语义空间（维度 $d=256$），使同一套奖励模型能够为不同基底模型提供语义对齐、人类偏好和运动真实性三个维度的奖励信号。这一设计使 MotionRFT 成为“即插即用”的通用微调框架，而非与特定基底模型绑定。

### 2. 与现有可微奖励微调方法的对比定位

现有基于可微奖励的微调方法构成了 MotionRFT 最直接的对比基线，其核心瓶颈在于**跨去噪步骤的递归梯度依赖**：

- **DRaFT** (Clark et al., ICLR 2024) 和 **AlignProp** (Prabhudesai et al., 2023)：通过对完整去噪链进行端到端反向传播来优化生成模型。这要求存储整个 $T$ 步去噪过程的计算图，内存复杂度为 $O(T)$，且梯度需递归传播，导致优化稀疏、梯度消失，以及内存开销随去噪步数线性增长。
- **DeepReward** (Wu et al., ECCV 2025)：采用奖励监督方式，但同样面临轨迹级优化的效率问题。

MotionRFT 的 **EasyTune** 方法通过理论分析和算法设计解耦了这一递归依赖。从 **Corollary 1** 的梯度分解出发：

$$\frac{\partial\mathbf{x}_{t-1}^{\theta}}{\partial\theta} = \underbrace{\frac{\partial\pi_{\theta}(\mathbf{x}_{t}^{\theta},t,c)}{\partial\theta}}_{\mathrm{direct~term}} + \underbrace{\frac{\partial\pi_{\theta}(\mathbf{x}_{t}^{\theta},t,c)}{\partial\mathbf{x}_{t}^{\theta}}\cdot\frac{\partial\mathbf{x}_{t}^{\theta}}{\partial\theta}}_{\mathrm{indirect~term}}$$

其中间接项包含了跨步递归梯度。EasyTune 通过**停止梯度操作**截断间接项，将优化目标转化为在均匀采样的时间步上最大化期望奖励：

$$\mathcal{L}_{\mathrm{EasyTune}}(\theta) = -\mathbb{E}_{c\sim\mathbb{D}_{\mathbf{T}},\mathbf{x}_{t}^{\theta}\sim\pi_{\theta}(\cdot|c),t\sim\mathcal{U}(0,T)}\left[\mathcal{R}_{\phi}(\mathbf{x}_{t}^{\theta},t,c)\right]$$

这一设计实现了三个关键突破：(1) 内存复杂度从 $O(T)$ 降至 $O(1)$，峰值 GPU 内存从 DRaFT 的 37.32 GB 降至 22.10 GB，节省 15.22 GB；(2) 每个去噪步骤独立接收奖励信号，实现细粒度优化；(3) 避免了梯度消失导致的早期步骤优化不足。

### 3. 与偏好对齐方法的对比定位

在人类偏好对齐维度，MotionRFT 与以下方法形成对照：

- **Motion-Critic** (Wang et al., ICLR 2025)：采用 PPO 强化学习进行偏好对齐，但仅针对单一运动表示（24关节），且需要在线采样和奖励估计，训练效率较低。MotionRFT 通过 MotionReward 在统一语义空间内联合学习偏好奖励，支持多种运动表示，且在人类偏好预测准确率上表现更优（Table II）。
- **SoPo** (Tan et al., NeurIPS 2025)：通过语义偏好优化提升文本-运动对齐，但缺乏对运动真实性的显式建模。MotionRFT 将语义对齐、人类偏好和真实性三个维度统一到同一奖励模型中。
- **ReinDiffuse** (Han et al., WACV 2025)：采用规则化奖励（如物理约束）提升运动真实性，但规则设计依赖领域知识，泛化性有限。MotionRFT 通过数据驱动的鉴别器学习真实性奖励，避免手工规则设计。

### 4. 适用边界与局限

MotionRFT 的适用边界和已知局限包括：

**适用条件**：
- 需要预训练的文本-运动生成模型作为基底，框架本身不涉及生成模型的从头训练。
- MotionReward 的训练依赖于合成 deepfake 样本（用于真实性奖励的负样本挖掘），要求训练集包含足够的运动多样性以生成有效的负样本。
- 当前验证集中在 HumanML3D 和 KIT-ML 两个标准基准，对更大规模、更多样运动数据的泛化性有待进一步验证。

**已知局限**（论文明确讨论）：
1. **物理合理性未建模**：当前框架仅针对文本到运动的语义对齐和感知质量，尚未集成物理仿真以改善运动的动力学和接触真实性。生成的运动会存在脚部滑动、关节超限等物理不合理现象。
2. **真实性奖励的泛化风险**：MotionReward 的真实性判别器通过合成 deepfake 样本训练，可能未完全覆盖真实世界运动异常分布，在域外运动上的真实性评估可能存在偏差。
3. **早期步骤优化不足**：EasyTune 的逐步优化在缺乏课程调度时，早期高噪声步骤（$t$ 接近 $T$）可能因奖励信号弱而学习不充分。论文提出的 **Curriculum Timestep Scheduling** 通过从高噪声到低噪声步的课程窗口调度部分缓解了此问题，但未完全解决。

### 5. 开放问题

论文遗留的开放问题指向以下研究方向：

1. **物理仿真集成**：如何将 MotionRFT 的奖励框架扩展到物理仿真域，使生成运动满足动力学约束和接触物理？这需要设计可微的物理奖励函数，并可能引入物理仿真器作为额外的奖励源。
2. **多模态条件扩展**：统一奖励框架能否推广到更丰富的条件生成场景，如视频驱动的运动生成、音频到运动生成？这需要 MotionReward 学习跨模态的统一语义空间。
3. **大规模数据下的语义对齐**：在更大规模、更多样的运动数据集上，MotionReward 的统一语义空间是否仍能有效对齐不同表示的运动？投影层的容量和语义空间的表达能力可能成为瓶颈。
4. **奖励维度的可扩展性**：当前 MotionReward 仅覆盖语义、偏好和真实性三个维度，能否在不重新训练主干网络的前提下，通过新增 LoRA 适配器灵活扩展新的奖励维度（如风格、情感、运动流畅度）？

## 原文 PDF

![[paperPDFs/arxiv_2026/MotionRFT:_Unified_Reinforcement_Fine-Tuning_for_Text-to-Motion_Generation.pdf]]
