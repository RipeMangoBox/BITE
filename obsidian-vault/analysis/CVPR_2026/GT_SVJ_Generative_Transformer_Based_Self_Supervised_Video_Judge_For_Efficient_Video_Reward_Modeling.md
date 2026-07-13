---
title: "GT-SVJ: Generative-Transformer-Based Self-Supervised Video Judge For Efficient Video Reward Modeling"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GT_SVJ_Generative_Transformer_Based_Self_Supervised_Video_Judge_For_Efficient_Video_Reward_Modeling.pdf
project_link: null
code_link: null
huggingface_link: "https://huggingface.co/sasuke-ss1/GT-SVJ"
aliases:
- GS
- GT-SVJ
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将视频生成模型重新用作能量基模型（EBM），通过自监督对比学习并注入精心设计的潜在空间扰动负样本，迫使模型学习鲁棒的时空判别特征，从而提供时间敏感的奖励信号。
primary_logic: 视频生成模型内在建模时间因果关系与运动语义；配合对比能量目标，它可以被转换为对真实视频分配低能量、对生成/扰动视频分配高能量的判别器，实现以极少的偏好数据超过VLM基准的人类偏好对齐。
claims:
- GT-SVJ 在 GenAI-Bench 上超越先前基线约 25%（含平局）与 3%（不含平局），在 MonteBench 上分别超越 4% 与 8%（含与不含平局），仅使用 30K 人类标注视频，比 VideoReward 少约 6 倍，比 VisionReward 少约 65 倍。
- 自监督对比学习采用帧洗牌、特征交换等五种在潜在空间中对真实视频的扰动，生成困难负样本，防止模型依赖表面域差异，从而学习有意义的时空特征。
- 使用判别模型初始化奖励模型可带来约 5% 的对齐准确率提升；加入扰动视频作为负样本使模型维持更稳定的梯度并取得更平滑的收敛。
- GenAI-Bench 上 人类偏好对齐准确率（含平局） = GT-SVJ 64.26
---

# GT-SVJ: Generative-Transformer-Based Self-Supervised Video Judge For Efficient Video Reward Modeling

> [!tip] 核心洞察
> 视频生成模型内在建模时间因果关系与运动语义；配合对比能量目标，它可以被转换为对真实视频分配低能量、对生成/扰动视频分配高能量的判别器，实现以极少的偏好数据超过VLM基准的人类偏好对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | GT-SVJ：基于生成式Transformer的自监督视频评判器 |
| 英文题名 | GT-SVJ: Generative-Transformer-Based Self-Supervised Video Judge For Efficient Video Reward Modeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.05202) · [HuggingFace](https://huggingface.co/sasuke-ss1/GT-SVJ) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | GT-SVJ |
| Dataset | GenAI-Bench, MonteBench, VideoReward-Bench |

> [!tip] 效果简介
> - GenAI-Bench 上，人类偏好对齐准确率（含平局） GT-SVJ 64.26 vs 先前最优（基于VLM的方法） (+24.63%（相对提升）)。
> - MonteBench 上，人类偏好对齐准确率（含平局） GT-SVJ 66.36 vs 先前最优 (+3.68%（相对提升）)。
> - VideoReward-Bench 上，人类偏好对齐准确率（含平局） GT-SVJ 57.01 vs VideoReward（当前最佳） (落后约 4–5%（差值）)。

## 概要

现有视频奖励模型主要构建于视觉语言模型（VLM）之上，如 **VideoReward**（Liu et al., 2025）和 **VisionReward**（Xu et al., 2025），它们虽然能利用文本语义进行质量评估，却难以捕捉细粒度的时序动态与运动一致性，并且严重依赖大量人类标注数据才能获得可靠的偏好对齐。GT-SVJ 针对这一瓶颈提出了一条根本不同的技术路线：**将视频生成模型重新用作能量基模型（EBM），通过自监督对比学习注入精心设计的潜在空间扰动负样本，迫使模型学习鲁棒的时空判别特征，从而以极少的偏好数据实现时间敏感的视频奖励建模。**

### 核心结论

- **性能突破**：GT-SVJ 在 GenAI-Bench 上以 64.26% 的对齐准确率（含平局）超越先前基线约 25%，在 MonteBench 上以 66.36% 超越约 4%；即使在未使用其训练数据的 VideoReward-Bench 上，也仅落后当前最佳模型约 4–5%。
- **数据效率跃升**：仅使用 30K 人类标注视频——比 VideoReward 少约 6 倍，比 VisionReward 少约 65 倍——即达到上述性能。
- **机制验证**：判别模型初始化带来约 5% 的对齐准确率提升；扰动负样本使模型维持更稳定的梯度并实现更平滑的收敛，验证对齐准确率额外提升 2–3%。

### 方法定位

GT-SVJ 并非在 VLM 范式内做增量改进，而是在**骨干架构**、**训练范式**和**负样本构造**三个维度上进行了系统性重设计：

1. **骨干架构**：以视频生成模型 CogVideoX 替代 VLM，利用其因果自注意力机制显式建模时间因果关系，从根本上增强对运动语义和时序一致性的感知能力。
2. **训练范式**：将视频生成模型转化为 EBM，先通过对比能量损失进行自监督判别预训练（区分真实视频与扰动/生成视频），再在判别模型基础上进行偏好微调，形成“先学会判断真假，再学会判断好坏”的两阶段管线。
3. **负样本构造**：在 VAE 潜在空间对真实视频施加帧洗牌、帧丢失、噪声段注入、补丁交换、时间片交换五种受控扰动，生成语义上困难但视觉上真实的负样本，防止模型依赖表面域差异，迫使其学习有意义的时空判别特征。

### 主要结果概览

| 基准 | GT-SVJ（含平局） | 相对提升 | 数据效率 |
|------|-----------------|---------|---------|
| GenAI-Bench | 64.26% | +24.63% | 30K 标注 |
| MonteBench | 66.36% | +3.68% | 30K 标注 |
| VideoReward-Bench | 57.01% | 落后约 4–5% | 30K 标注 |

消融实验进一步证实：移除判别模型预训练使 GenAI-Bench 准确率骤降至 47.62%（降幅约 16.64）；可变长度训练策略（p=0.25）相比固定长度（p=0）带来 1%–15% 的对齐准确率提升；LoRA 适配器仅作用于骨干网络最后 1/3 的 Transformer 层，在保持高性能的同时实现约 1.5 倍的训练加速。



视频生成模型近年来取得了显著进展，但如何自动、可靠地评估生成视频的质量仍是一个核心瓶颈。现有的视频评估方法主要依赖基于视觉-语言模型（VLM）的奖励模型，如 **VideoReward**（Liu et al., 2025）和 **VisionReward**（Xu et al., 2025）。这些方法通过在大规模人类偏好数据上进行 Bradley-Terry 或 DPO 训练来对齐人类判断。然而，它们存在两个关键局限：

**瓶颈一：时间动态捕捉不足。** VLM 通常从图像模型扩展而来，其时间建模能力有限，仅通过注意力机制间接捕捉帧间关系，难以充分捕获运动一致性、时间因果性和细粒度的时间动态。这导致模型在面对需要精细时间判断的偏好对时，对齐准确率受限。

**瓶颈二：标注数据依赖过重。** 主流的 VLM 奖励模型需要大量人类标注的偏好数据才能获得可靠的偏好对齐。例如，VideoReward 使用了约 180K 的人类标注视频，VisionReward 则使用了约 1.95M 的标注数据。如此庞大的标注需求不仅成本高昂，也限制了模型在新场景下的快速部署。

**核心动机：** 视频生成模型（如 CogVideoX）在训练过程中天然地学习了运动模式、时间因果关系和细粒度时空表示——这些恰恰是 VLM 所缺乏的。GT-SVJ 的核心动机在于，将视频生成模型重新用作奖励模型，利用其内在的时间建模能力来弥补 VLM 的不足。具体而言，生成模型可以被重新表述为能量基模型（EBM），对高质量视频分配低能量，对退化视频分配高能量。配合精心设计的自监督对比学习策略，模型能够在仅使用约 30K 人类标注视频的条件下（比 VideoReward 少约 6 倍，比 VisionReward 少约 65 倍），实现对人类偏好的高效对齐。

图 1 直观展示了 GT-SVJ 的工作方式：给定两个视频，模型通过自监督学习到的时空判别特征对其进行偏好排序，在多个基准上超越现有 VLM 基线。



## 核心方法与创新机理

GT-SVJ 的核心创新在于**将视频生成模型重新用作能量基判别器**，从根本上改变了视频奖励模型的构建范式。与现有基于 VLM 的方法（如 **VideoReward** (Liu et al., 2025)、**VisionReward** (Xu et al., 2025)）不同，GT-SVJ 在四个关键维度上实现了系统性突破。

### 1. 骨干架构：从“间接感知时间”到“显式建模时间因果”

现有 VLM 基奖励模型通过注意力机制间接捕捉时间信息，难以精细建模运动一致性与时间动态。GT-SVJ 采用视频生成模型 **CogVideoX** 作为骨干，其因果自注意力机制天然具备对时间因果关系的显式建模能力。这一选择的核心洞察在于：视频生成模型在预训练阶段已内化了运动语义与时间结构，将其转换为判别器时，这些表征可直接服务于质量评估，无需从零学习时间感知。

### 2. 训练范式：从“纯偏好对齐”到“自监督对比预训练 + 偏好微调”

传统方法直接使用 Bradley-Terry 或 DPO 损失在人类偏好对上训练奖励模型，数据需求极大（VideoReward 使用约 180K 标注，VisionReward 约 1.9M 标注）。GT-SVJ 引入两阶段训练策略：

- **第一阶段**：将视频生成模型转换为判别模型（DM），通过自监督对比能量损失训练其区分真实视频与扰动/生成视频。
- **第二阶段**：在判别模型基础上进行偏好微调，仅需约 30K 人类标注视频。

这种“先学会判别真假，再学会判别好坏”的课程式训练，使模型在极少监督下即可获得鲁棒的时空判别特征。消融实验表明，移除判别模型预训练（No DM）导致 GenAI-Bench 准确率从 64.26 骤降至 47.62，降幅约 16.64 个百分点，验证了该阶段的关键作用。

### 3. 负样本构造：从“域差异捷径”到“语义困难样本”

VLM 基方法通常仅使用模型生成的视频作为负样本，模型易学习域差异等表面线索，而非真正的质量缺陷。GT-SVJ 在 VAE 潜在空间中对真实视频施加五种受控扰动，生成语义上困难但视觉上真实的负样本：

| 扰动类型 | 机制 | 目的 |
|---------|------|------|
| 帧洗牌（Frame Shuffle） | 随机重排帧顺序 | 破坏时间连贯性 |
| 帧丢失（Frame Drop） | 复制前一帧替代当前帧 | 模拟丢帧伪影 |
| 噪声段注入（Noisy Segment Injection） | 在随机连续段添加高斯噪声 | 引入局部退化 |
| 补丁交换（Patch Swap） | 交换不同帧的空间补丁 | 破坏时空一致性 |
| 时间片交换（Temporal Slice Swap） | 交换不同时间段的潜在表示 | 破坏中长程时间流 |

这些扰动迫使模型关注时空一致性，而非简单的分布差异。实验证实，加入所有类型的扰动视频使验证对齐准确率提升 2–3%，且模型维持更稳定的梯度并实现更平滑的收敛——若仅使用真实与生成视频训练，模型会早期饱和并出现梯度消失。

### 4. 参数高效微调：仅适配最后 1/3 Transformer 层

GT-SVJ 仅对 CogVideoX 最后 1/3 的 Transformer 层应用 LoRA 适配器（rank=8, α=8），大幅降低可训练参数量。消融实验显示，中层配置获得最佳整体性能，而最后层配置训练速度约加快 1.5 倍，性能损失极小。这种轻量设计使得基于生成模型的奖励模型训练在计算上可行。

### 创新本质：能量基模型的判别式重利用

上述四个维度的创新统一于一个核心公式——对比能量损失：

$$\mathcal{L}_{\mathrm{contrast}} = \underbrace{\mathbb{E}_{x^{+}} [E_{\theta}(x^{+})] - \mathbb{E}_{x^{-}} [E_{\theta}(x^{-})]}_{\mathcal{L}_{\mathrm{EBM}}} + \beta \underbrace{\left(\mathbb{E}_{x^{+}} [E_{\theta}(x^{+})^{2}] + \mathbb{E}_{x^{-}} [E_{\theta}(x^{-})^{2}]\right)}_{\mathcal{L}_{2}}$$

该损失将视频生成模型转换为对真实视频分配低能量、对扰动/生成视频分配高能量的判别器。Figure 3 可视化了这一机制：真实视频的能量轨迹平滑稳定，而生成视频的能量值剧烈波动，反映其时空不一致性。这种能量基建模天然适合捕捉细粒度时间缺陷，是 VLM 基方法难以实现的。



GT‑SVJ 的核心思路是将视频生成模型重新用作**能量基模型（EBM）**，通过两阶段训练构建一个时间敏感的视频奖励模型：第一阶段训练判别模型，第二阶段在判别模型基础上进行偏好对齐。整个框架的输入为视频（及其潜在表示），输出为与人类偏好对齐的标量奖励分数或多维质量方面分数。

### 两阶段流水线

**第一阶段：判别模型训练（Discriminative Model, DM）**  
以预训练视频生成模型 **CogVideoX** 为骨干，仅取其最后 1/3 的 Transformer 层并接入一个轻量 MLP 头，在 VAE 潜在空间上对视频进行能量评分。训练采用对比能量目标：

$$
\mathcal{L}_{\mathrm{contrast}} = \mathcal{L}_{\mathrm{EBM}} + \beta \mathcal{L}_{2}
$$

其中 $\mathcal{L}_{\mathrm{EBM}}$ 推动真实视频获得低能量、负样本获得高能量，$\mathcal{L}_{2}$ 为正则项（$\beta=0.2$）。负样本来自两类：**模型生成的视频**和**在真实视频潜在表示上施加受控扰动构造的困难负样本**（帧洗牌、帧丢失、噪声段注入、补丁交换、时间片交换）。扰动生成器在潜在空间操作，迫使模型关注时空一致性而非表面域差异。训练时还以概率 $p=0.25$ 随机截断视频长度，防止对固定时长过拟合。

**第二阶段：奖励模型训练（Reward Model）**  
在训练好的判别模型基础上，增加两个输出分支：
- **方面分数预测器（Aspect-wise Score Predictor, AWP）**：将 Transformer 输出映射为 21 维视频质量方面分数 $q \in \mathbb{R}^{\mathcal{Q}}$，使用 MSE 损失回归人类评分。
- **相对偏好模型（Relative Preference Model）**：通过聚合头将 21 维分数映射为单一标量奖励 $r_{\phi}(x)$，并在人类偏好对上使用 Bradley‑Terry 损失（含平局变体）进行微调。

### 模块关系与数据流

1. 输入视频经 VAE 编码为潜在表示 $z$。
2. **扰动生成器** 对真实视频的 $z$ 施加随机扰动，生成困难负样本 $\widetilde{z}$。
3. **判别模型（DM）** 接收 $(z_{\text{real}}, z_{\text{gen}}, \widetilde{z})$，通过 CogVideoX 部分层 + MLP 头输出能量标量，由 $\mathcal{L}_{\mathrm{contrast}}$ 驱动训练。
4. 训练好的 DM 作为初始化，接入 **AWP** 头输出 21 维方面分数，以 $\mathcal{L}_{\mathrm{MSE}}$ 回归；同时**聚合头**将其压缩为标量奖励，以 $\mathcal{L}_{\mathrm{BT}}$ 在偏好对上微调。
5. 最终模型可同时输出多维质量评估和用于偏好排序的单一奖励值。

### 关键设计决策

- **骨干选择**：CogVideoX 的因果自注意力天然建模时间因果关系，相比 VLM 仅通过注意力间接捕捉时间信息，能更有效地提取运动语义和细粒度时间动态。
- **参数高效微调**：仅对 CogVideoX 最后 1/3 层应用 LoRA 适配器（rank=8, $\alpha=8$），中间层配置取得最优验证准确率，最后层配置训练速度约快 1.5 倍且性能损失极小。
- **负样本构造**：五种潜在空间扰动覆盖从帧级局部破坏（帧丢失、噪声段）到长程时序破坏（帧洗牌、时间片交换），迫使模型学习有意义的时空判别特征，避免仅依赖域差异等表面线索。

### 补充图表

![[assets/figures/papers/paper_list_l2288_https_arxiv_org_abs_2602_05202/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed GT-SVJ framework. The framework consists of two stages: (top) Training a discriminative model, where the video generative model (CogVideoX) is adapted using a contrastive energy-based objective with real, generated, and perturbed videos, and (middle and bottom) Training a reward model, where the discriminative model (DM) is aligned with human ratings through aspect-wise prediction (AWP) via regression (middle) followed by relative preference modeling (bottom)*



GT-SVJ 的核心设计围绕一个关键洞察展开：视频生成模型内在建模了时间因果关系与运动语义，将其重新用作能量基模型（EBM），并配合精心设计的潜在空间扰动负样本，可以迫使模型学习鲁棒的时空判别特征。整个框架包含三个关键模块。

### 视频判别模型（DM）

判别模型基于 CogVideoX 的部分 Transformer 层构建，后接一个轻量 MLP 头，将时空特征聚合为每个潜在帧的单一标量表示。训练采用对比能量目标：

$$
\mathcal{L}_{\mathrm{contrast}} = \mathcal{L}_{\mathrm{EBM}} + \beta \mathcal{L}_{2}
$$

其中 $\mathcal{L}_{\mathrm{EBM}}$ 推动真实视频（正样本）获得低能量、负样本获得高能量：

$$
\mathcal{L}_{\mathrm{EBM}} = \mathbb{E}_{x^{+} \sim p_{\mathrm{data}}} [E_{\theta}(x^{+})] - \mathbb{E}_{x^{-} \sim p_{\mathrm{neg}}} [E_{\theta}(x^{-})]
$$

$\mathcal{L}_{2}$ 为正则项，用于稳定 EBM 训练：

$$
\mathcal{L}_{2} = \mathbb{E}_{x^{+} \sim p_{\mathrm{data}}} [E_{\theta}(x^{+})^{2}] + \mathbb{E}_{x^{-} \sim p_{\mathrm{neg}}} [E_{\theta}(x^{-})^{2}]
$$

$\beta$ 为平衡超参数，实验中固定为 0.2。该模块仅对 CogVideoX 最后 1/3 的 Transformer 层应用 LoRA 适配器（rank=8, α=8），实现参数高效微调。

### 扰动生成器

为避免模型仅学习真实视频与生成视频之间的表面域差异，扰动生成器在真实视频的 VAE 潜在表示上施加五种受控扰动，构造语义困难但视觉上真实的负样本：

- **帧洗牌**（Frame Shuffle）：$\widetilde{z}_t = z_{\Pi(t)}$，打乱时间顺序但保留每帧外观；
- **帧丢失**（Frame Drop）：$\widetilde{z}_t = z_{t-1}$，模拟丢帧或重复帧；
- **噪声段注入**（Noisy Segment Injection）：在随机时间段注入噪声潜在表示；
- **补丁交换**（Patch Swap）：交换不同帧之间的空间补丁；
- **时间片交换**（Temporal Slice Swap）：交换不同时间段的潜在片段，破坏中长期时间流。

这些扰动迫使模型关注时空一致性，而非表面的统计差异。消融实验表明，加入所有类型扰动视频使验证对齐准确率提升 2–3%，并显著加快收敛（Figure 6、Figure A.2）。

### 方面分数预测器与偏好模型

奖励模型阶段，Transformer 输出被映射为 21 维视频质量方面分数 $q \in \mathbb{R}^{\mathcal{Q}}$，通过 MSE 损失回归人类评分。随后，聚合头将 21 个预测属性映射为单一标量奖励值 $r_{\phi}(x)$，并在人类偏好对上通过 Bradley-Terry 损失微调：

$$
P(x_{i}^{+} \succ x_{i}^{-}) = \frac{\exp(r_{\phi}(x_{i}^{+}))}{\exp(r_{\phi}(x_{i}^{+})) + \exp(r_{\phi}(x_{i}^{-}))}
$$

$$
\mathcal{L}_{\mathrm{BT}} = -\mathbb{E}_{(x^{+}, x^{-})} [\log P(x^{+} \succ x^{-})]
$$

对于允许平局的场景，采用带平局的 Bradley-Terry 模型，引入温度参数 $\gamma$ 控制平局概率：

$$
P(x^{+} \succ x^{-}) = \frac{\exp(r_{\phi}(x^{+})/\gamma)}{\exp(r_{\phi}(x^{+})/\gamma) + \exp(r_{\phi}(x^{-})/\gamma) + 1}
$$

这一两阶段设计——先通过自监督对比能量目标训练判别模型，再在判别模型基础上进行偏好微调——是 GT-SVJ 数据效率的关键：仅使用 30K 人类标注视频（比 VideoReward 少约 6 倍，比 VisionReward 少约 65 倍）即在 GenAI-Bench 和 MonteBench 上超越 VLM 基线。

### 补充图表

![[assets/figures/papers/paper_list_l2288_https_arxiv_org_abs_2602_05202/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of energy trajectories predicted by our energy-based model. For the real video in (a), energy trajectory across the time steps is smooth and stable, indicating consistent temporal dynamics. In contrast, for the generated videos in (b) and (c), the energy values fluctuate erratically, reflecting spatial and temporal inconsistencies such as implausible scene lighting and motions*



## 实验与关键发现

### 主实验结果

GT-SVJ 在三个视频偏好基准上的对齐准确率如 Table 1 所示。核心发现可归纳为三点：

![[assets/figures/papers/paper_list_l2288_https_arxiv_org_abs_2602_05202/figures/004_Table_1.jpg]]
*Table 1: Video evaluation results on multiple video preference benchmark datasets. We report comparable or better performance in alignment accuracy with human preferences on all benchmark datasets. We also report the human-annotated dataset sizes (in number of samples) and backbone sizes (in number of trainable model parameters). We use the evaluation scheme of Deutsch et al. [8]. Bold: best, underline: second-best. Higher values are better for all columns*

**GenAI-Bench 与 MonteBench 上的一致领先。** 在 GenAI-Bench 上，GT-SVJ 达到 64.26（含平局）/ 62.11（不含平局），相对先前最优基线分别提升约 25% 和 3%。在 MonteBench 上，GT-SVJ 达到 66.36（含平局）/ 62.18（不含平局），相对提升约 4% 和 8%。这一优势来自生成模型骨干对时间因果关系的显式建模，以及对比能量目标对真实/扰动视频的判别能力。

**VideoReward-Bench 上的竞争力。** GT-SVJ 在该基准上取得 57.01（含平局），落后当前最佳方法 **VideoReward**（Liu et al., 2025）约 4–5 个百分点。这一差距主要源于 VideoReward 使用该基准的公开训练数据进行偏好对齐，而 GT-SVJ 未接触该分布，存在分布偏移。该结果从反面验证了对比预训练在数据受限条件下的泛化边界。

**极高的数据效率。** GT-SVJ 仅使用 30K 人类标注视频完成全部训练，比 VideoReward 少约 6 倍，比 **VisionReward**（Xu et al., 2025）少约 65 倍。这一效率来自自监督对比预训练阶段——模型在无人类标注的条件下，通过扰动负样本学习时空判别特征，大幅降低了对偏好数据的依赖。

### 消融实验

**判别模型预训练的作用。** 移除判别模型初始化（No DM）导致 GenAI-Bench 准确率从 64.26 骤降至 47.62，降幅约 16.64 个百分点。Figure 5 的验证曲线进一步显示，有 DM 初始化的奖励模型在整个训练过程中保持更低的验证损失和更高的验证准确率，表明对比能量预训练为偏好微调提供了高质量的表示起点。

**扰动负样本的必要性。** 当判别模型仅使用真实视频与模型生成视频训练时，模型出现早期饱和与梯度消失（Figure 6）。加入五种潜在空间扰动视频（帧洗牌、帧丢失、噪声段注入、补丁交换、时间片交换）后，模型维持信息量丰富的梯度，收敛更平滑，验证对齐准确率提升 2–3%。这表明扰动负样本迫使模型关注时空一致性而非表面域差异。

**可变长度训练的影响。** 以概率 p=0.25 随机截断视频对进行可变长度训练，相比固定长度训练（p=0），对齐准确率提升 1–15%。该设计防止模型过拟合固定时长输入，增强了跨时长泛化能力。

**LoRA 放置位置。** Figure 4 展示了对 CogVideoX Transformer 不同层段应用 LoRA 的效果。中层配置（中间 1/3 层）获得最佳整体性能；末层配置训练速度约快 1.5 倍，性能损失极小。这一消融验证了参数高效微调策略的有效性，同时揭示了时间建模能力在不同深度层的分布差异。

### 扰动策略的自适应采样

Table A.1 给出了五种扰动类型的自适应采样概率。该概率基于各扰动类型单独训练时的梯度范数和损失曲线（Figure A.1）进行难度分析确定：难度越高的扰动（如时间片交换，迫使模型检测长程时间不一致性）分配越高采样概率。同时，固定 0.3 概率保留给真实视频与模型生成视频的对比，确保模型不遗忘对生成伪影的判别能力。

### 能量轨迹的定性分析

Figure 3 可视化了判别模型对真实视频与生成视频预测的能量轨迹。真实视频的能量轨迹平滑稳定，反映一致的时间动态；生成视频的能量值剧烈波动，对应空间和时间不一致性（如不合理的场景光照和运动）。这一观察从机制层面验证了能量基模型的设计直觉：真实视频被赋予低且稳定的能量，生成/扰动视频被赋予高且波动的能量。

### 失败模式与局限

尽管整体表现优异，GT-SVJ 在以下场景存在明显局限：

1. **分布外泛化不足。** 在 VideoReward-Bench 上落后于使用同分布训练数据的方法，说明对比预训练虽能提升数据效率，但无法完全弥补训练分布与测试分布的偏移。该问题在无法获取目标基准训练数据的实际部署中尤为突出。
2. **扰动覆盖有限。** 当前五种扰动主要针对时间维度（帧洗牌、帧丢失、时间片交换）和局部空间维度（补丁交换、噪声段注入），可能无法覆盖真实世界中更复杂的视频退化类型（如压缩伪影、运动模糊、色彩偏移等）。是否需要更丰富的负样本类型仍有待探索。
3. **多模态对齐缺失。** 当前框架仅基于视频信号进行偏好建模，未考虑文本提示与视频内容的一致性。在文生视频场景中，提示忠实度是重要的质量维度，该缺失限制了 GT-SVJ 在文本条件生成评估中的适用性。

### 补充图表

![[assets/figures/papers/paper_list_l2288_https_arxiv_org_abs_2602_05202/figures/005_Figure_4.jpg]]
*Figure 4: Effect of LoRA placement within the backbone transformer. We compare applying LoRA to the initial third, middle third, and last third of the transformer layers. The middle-layer configuration achieves the best overall performance, while the last-layer configuration provides faster training with minimal loss in accuracy*

![[assets/figures/papers/paper_list_l2288_https_arxiv_org_abs_2602_05202/figures/006_Figure_5.jpg]]
*Figure 5: Effect of the discriminative model. Initializing the reward model with the trained discriminative model leads to lower validation losses and higher validation accuracies throughout training*

![[assets/figures/papers/paper_list_l2288_https_arxiv_org_abs_2602_05202/figures/007_Figure_6.jpg]]
*Figure 6: Effect of perturbed videos as negative samples. Our discriminative model, when trained only on real and generated videos, exhibits early saturation and vanishing gradients. In contrast, when perturbed videos are augmented as negative samples in training, the model maintains informative gradients and achieves smoother convergence*

![[assets/figures/papers/paper_list_l2288_https_arxiv_org_abs_2602_05202/figures/008_Table.jpg]]
*Table: A.1. Sampling probabilities assigned to each perturbation type based on gradient-based difficulty analysis. Note that a fixed probability of 0.3 is reserved for contrasting real videos with model-generated videos, and hence the probabilities of perturbations for real videos sum to 0.7*

![[assets/figures/papers/paper_list_l2288_https_arxiv_org_abs_2602_05202/figures/009_Figure.jpg]]
*Figure: (a) Average gradient norm during training from using each perturbation type individually. (b) Training loss curves from using each perturbation type individually. Figure A.1. Effect of using each perturbation type individually to generate negative samples. We show the ease or difficulty of training the discriminative model when using each perturbation type individually*

![[assets/figures/papers/paper_list_l2288_https_arxiv_org_abs_2602_05202/figures/010_Figure.jpg]]
*Figure: A.2. Effect of using all types of perturbed videos in training the discriminative model (DM). We observe significantly faster convergence to 2-3% better validation alignment accuracies to human preferences*

![[assets/figures/papers/paper_list_l2288_https_arxiv_org_abs_2602_05202/figures/001_Figure_1.jpg]]
*Figure 1: GT-SVJ in action. Given two videos, our self-supervised model evaluates and ranks them on preferences, outperforming baselines on human preference alignment*



## 定位与知识库关联

### 与基于 VLM 的视频奖励模型的关系

GT-SVJ 的核心创新在于**用视频生成模型替代视觉-语言模型（VLM）作为奖励模型的骨干**，从根本上改变了视频质量评估的建模范式。现有主流方法，如 **VideoReward**（Liu et al., 2025）和 **VisionReward**（Xu et al., 2025），均基于 VLM 架构（如 LLaVA、VideoChatGPT），通过对视频帧的注意力机制间接捕捉时间信息。这类方法面临两个关键瓶颈：（1）VLM 的注意力机制并非为精细时间动态建模而设计，难以捕捉运动一致性和因果时序；（2）需要大量人类偏好标注数据才能实现可靠的偏好对齐——VideoReward 使用了约 180K 标注样本，VisionReward 使用了约 1.95M 标注样本。

GT-SVJ 的解决方案是**重新利用视频生成模型的内在时间建模能力**。视频生成模型（如 CogVideoX）通过因果自注意力显式建模帧间的时间因果关系，其潜在表示天然编码了运动语义和时序一致性。这一洞察构成了 GT-SVJ 与 VLM 基线之间的根本性“因果旋钮”差异：不是让模型从静态帧中推断时间关系，而是让一个已经学会生成连贯时序的模型去判别时序异常。

### 能量基判别框架的方法论定位

GT-SVJ 将生成模型重新表述为**能量基模型（EBM）**的做法，在方法论上连接了两条研究线索：

1. **生成模型的判别式复用**：与图像领域中将 GAN 或扩散模型的判别器/UNet 用于表示学习的工作类似，GT-SVJ 将视频生成 Transformer 的部分层用作时空特征提取器，配合轻量 MLP 头输出标量能量值。这种“生成-判别”转换的关键在于对比能量目标：
   $$\mathcal{L}_{\mathrm{contrast}} = \mathcal{L}_{\mathrm{EBM}} + \beta \mathcal{L}_{2}$$
   其中 $\mathcal{L}_{\mathrm{EBM}} = \mathbb{E}_{x^{+} \sim p_{\mathrm{data}}} [E_{\theta}(x^{+})] - \mathbb{E}_{x^{-} \sim p_{\mathrm{neg}}} [E_{\theta}(x^{-})]$，推动真实视频获得低能量，生成/扰动视频获得高能量。

2. **自监督对比学习的负样本设计**：与仅使用模型生成视频作为负样本的朴素方法不同，GT-SVJ 在 VAE 潜在空间中对真实视频施加五种受控扰动——帧洗牌（Frame Shuffle）、帧丢失（Frame Drop）、噪声段注入（Noisy Segment Injection）、补丁交换（Patch Swap）、时间片交换（Temporal Slice Swap）——生成语义上困难但视觉上真实的负样本。这迫使模型学习鲁棒的时空判别特征，而非依赖域差异等表面线索。消融实验表明，加入所有类型的扰动视频使验证对齐准确率提升 2–3%，且显著加速收敛（Figure 6, Figure A.2）。

### 训练范式的演进

GT-SVJ 的两阶段训练流程代表了视频奖励模型训练范式的重要演进：

| 训练阶段 | 基线方法（VLM-based） | GT-SVJ |
|---------|---------------------|--------|
| 预训练 | 依赖 VLM 的通用视觉-语言预训练 | **判别模型（DM）自监督对比预训练**，在 VAE 潜在空间上区分真实与扰动视频 |
| 对齐训练 | 直接使用偏好对进行 Bradley-Terry 训练 | 在 DM 初始化基础上，先通过**方面分数预测（AWP）**回归 21 维质量评分，再通过 Bradley-Terry 偏好微调 |

判别模型预训练的作用在消融实验中得到了明确验证：移除 DM 初始化（No DM）导致 GenAI-Bench 准确率从 64.26 骤降至 47.62（降幅约 16.64 个百分点），且验证损失曲线显著恶化（Figure 5）。这表明自监督对比预训练为后续的偏好对齐提供了关键的时空判别先验。

### 参数效率与可扩展性

GT-SVJ 采用**参数高效微调（PEFT）**策略，仅对 CogVideoX 最后 1/3 的 Transformer 层应用 LoRA 适配器（rank=8, α=8）。LoRA 放置位置的消融实验（Figure 4）揭示了有趣的权衡：中层配置获得最佳整体性能，而最后层配置训练速度约快 1.5 倍，性能损失极小。这种轻量级设计使得 GT-SVJ 的**可训练参数量远小于全参数微调的 VLM 基线**，同时仅需 30K 人类标注视频——比 VideoReward 少约 6 倍，比 VisionReward 少约 65 倍——即可达到具有竞争力的对齐性能。

### 适用边界与局限

尽管 GT-SVJ 在 GenAI-Bench 和 MonteBench 上取得了显著优势（分别超越先前基线约 25% 和 4%，含平局），其在 **VideoReward-Bench 上仍落后于 VideoReward 约 4–5%**（含平局）。论文将此归因于 VideoReward 的训练数据分布与 VideoReward-Bench 更接近，而 GT-SVJ 未使用该基准的训练数据。这揭示了该方法的一个适用边界：**当目标评估分布与自监督训练数据的视频特性存在显著偏移时，判别模型的先验可能不足以弥补分布差距**。

此外，以下开放问题值得关注：

1. **多模态扩展**：当前 GT-SVJ 仅基于视频信号进行质量评估，未考虑文本提示与视频内容的一致性。能否将文本条件注入判别模型，实现对“视频-文本对齐”的评估？

2. **负样本覆盖度**：五种潜在空间扰动是否足以覆盖真实世界视频退化的全部类型？复杂的运动伪影、压缩噪声、跨模态不一致等可能需要更丰富的负样本构造策略。

3. **生成模型依赖**：GT-SVJ 的性能依赖于底层生成模型 CogVideoX 的质量。生成模型的架构演进（如更强的时序建模能力）是否会直接转化为判别性能的提升，仍需验证。

### 知识库定位总结

GT-SVJ 在视频奖励建模的知识谱系中占据了一个独特位置：它**桥接了视频生成模型的自监督表示学习与人类偏好对齐**，证明了“生成即判别”范式在视频质量评估中的有效性。其核心贡献不在于提出全新的网络架构，而在于**重新组合已知组件（生成 Transformer + EBM 对比学习 + 潜在空间扰动 + Bradley-Terry 对齐）形成高效的数据利用范式**。对于后续工作，该框架的启示在于：视频生成模型的内在时序先验可以大幅降低对人工标注的依赖，而精心设计的负样本构造是将生成模型转化为鲁棒判别器的关键。



## 原文 PDF

![[paperPDFs/CVPR_2026/GT_SVJ_Generative_Transformer_Based_Self_Supervised_Video_Judge_For_Efficient_Video_Reward_Modeling.pdf]]
