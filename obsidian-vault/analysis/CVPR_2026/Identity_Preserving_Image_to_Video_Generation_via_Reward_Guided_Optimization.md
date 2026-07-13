---
title: Identity-Preserving Image-to-Video Generation via Reward-Guided Optimization
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Identity_Preserving_Image_to_Video_Generation_via_Reward_Guided_Optimization.pdf
project_link: "https://ipro-alimama.github.io/"
code_link: null
aliases:
- IPRGOI
- IPIVGRGO
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 采用从纯噪声开始的策略化（on-policy）训练，并通过截断梯度直接优化面部身份奖励，从根本上消除训练与推理之间的分布不匹配。
primary_logic: 将ArcFace人脸识别模型作为可微分奖励函数，结合多帧人脸特征池面部评分策略和多步KL散度正则化，可以在不引入额外身份模块的情况下，通过强化学习高效提升I2V的身份一致性，同时有效抑制奖励欺骗（reward hacking）。
claims:
- 加入身份奖励优化后，in-house I2V模型的FaceSim从0.4769提升至0.6960，相对提升45.9%。
- 与MoCA†、Concat-ID†等现有方法相比，IPRO在FaceSim指标上达到0.6942，显著优于所有对比方法。
- 消融实验证明，面部特征池（FSM）和多步KL正则化共同将奖励黑客率从58%降至10%，同时保持高身份一致性。
- 从纯噪声采样的策略化训练消除了曝光偏差，使训练与推理的分布对齐。
---

# Identity-Preserving Image-to-Video Generation via Reward-Guided Optimization

> [!tip] 核心洞察
> 将ArcFace人脸识别模型作为可微分奖励函数，结合多帧人脸特征池面部评分策略和多步KL散度正则化，可以在不引入额外身份模块的情况下，通过强化学习高效提升I2V的身份一致性，同时有效抑制奖励欺骗（reward hacking）。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于奖励引导优化的身份保持图像到视频生成 |
| 英文题名 | Identity-Preserving Image-to-Video Generation via Reward-Guided Optimization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.14255) · [Project](https://ipro-alimama.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Identity-Preserving Reward-guided Optimization (IPRO) |
| Dataset | Small-face evaluation set, VBench-I2V metrics |

> [!tip] 效果简介
> - Small-face evaluation set (600 scenes) 上，FaceSim↑ 0.6960 vs 0.4769 (+45.9%)；FaceSim↑ 0.5460 vs 0.3788 (+44.1%)；FaceSim↑ 0.6942 vs 0.5780 (+20.1%)。
> - VBench-I2V metrics 上，Subject Consistency↑ 0.9811 (in-house) vs 0.9768 (+0.4%)。

## 概要

**问题瓶颈**：现有图像到视频（I2V）生成模型在处理低分辨率人脸与大运动场景时，因训练中的曝光偏差（exposure bias）导致身份特征随时间逐渐漂移，产生“平均脸”效应。单纯增加身份模块无法解决这一根本性分布不匹配问题。

**核心方法**：本文提出 **IPRO**（Identity-Preserving Reward-guided Optimization），将 ArcFace 人脸识别模型作为可微分奖励函数，通过从纯噪声开始的策略化强化学习直接优化面部身份一致性。该方法无需引入额外身份模块，即可高效提升 I2V 的身份保持能力。

**方法定位**：IPRO 属于基于奖励反馈的扩散模型微调范式，区别于监督微调（SFT）、直接偏好优化（DPO）和组相对优势优化（GRPO）等现有训练框架。其关键创新在于：将身份保持问题形式化为可微分奖励最大化，并通过截断梯度反向传播实现高效优化。

**主要结果**：
- 在内部 I2V 模型（15B）上，FaceSim 从 0.4769 提升至 0.6960，相对提升 **45.9%**（Table 1）。
- 在开源 Wan 2.2 5B 和 27B-A14B 模型上，FaceSim 分别提升 44.1% 和 20.1%，验证了方法的模型无关性。
- 与 MoCA†、Concat-ID† 等现有身份保留方法相比，IPRO 以 FaceSim = 0.6942 达到最优（Table 2）。
- 消融实验证实，面部特征池（FSM）和多步 KL 散度正则化共同将奖励黑客率从 58% 降至 10%，同时保持高身份一致性（Table 6, Table 7）。

**局限性**：当前方法仅关注面部身份一致性，对配饰、服装等非面部身份元素的保持尚未探索；奖励黑客现象虽被大幅抑制，仍无法完全消除（黑客率约 10%）。



### 图像到视频生成的身份保持困境

图像到视频（Image-to-Video, I2V）生成旨在将单张静态图像转化为一段动态视频，其核心挑战之一是在运动生成过程中保持人物身份的一致性。近年来，大规模扩散模型（Diffusion Models）在视频生成质量上取得了显著进展，但在身份保持这一维度上仍存在系统性缺陷。

现有I2V模型在处理包含人脸的场景时，面临一个关键瓶颈：**训练-推理分布不匹配导致的曝光偏差（exposure bias）**。具体而言，模型在训练阶段采用教师强制（teacher forcing）策略，每一步去噪都基于真实数据的分布；但在推理阶段，模型必须从纯噪声开始自回归地去噪，误差会沿采样链逐步累积。当输入图像中的人脸分辨率较低或视频包含大幅度运动时，这种分布偏移会使生成的人脸身份特征随时间逐渐漂移，最终产生“平均脸”效应——即生成的人脸看似合理，但已丧失原始人物的身份特征。

### 现有方法的局限

当前解决身份保持问题的技术路线主要分为两类：

**身份模块注入方法**（如MoCA†, Xie et al., arXiv 2025; Concat-ID†, Zhong et al., arXiv 2025）试图在扩散模型中嵌入额外的身份编码器或适配器，将参考人脸的特征显式注入生成过程。这类方法存在两个固有问题：其一，身份模块与基础模型的耦合增加了架构复杂度和训练成本；其二，身份模块本身在训练中也面临同样的曝光偏差问题，无法从根本上解决分布不匹配。

**监督微调（SFT）方法**通过构造身份保持的配对数据进行微调，但其训练范式仍然是教师强制的，训练与推理的分布鸿沟并未弥合。此外，SFT的损失函数（如均方误差）与身份保持这一高层语义目标之间存在天然的不对齐——像素级重建精度高并不意味着人脸身份特征被准确保留。

### 强化学习与奖励驱动的生成优化

扩散模型的奖励驱动优化（reward-guided optimization）为上述困境提供了新的解决思路。其核心思想是将扩散模型的采样过程视为一个可微分的策略，通过定义任务相关的奖励函数（如美学分数、文本-图像对齐分数），直接对采样链进行梯度优化。DRaFT（Clark et al., NeurIPS 2023）等工作证明了通过截断梯度反向传播（truncated backpropagation）可以有效且高效地将奖励信号注入扩散模型。

然而，将这一范式迁移到I2V的身份保持任务面临三个核心挑战：

1. **奖励函数设计**：如何定义一个可微分、鲁棒且与人类感知一致的面部身份奖励？简单的CLIP相似度对细粒度身份特征不敏感，无法区分“相似的人”和“同一个人”。

2. **奖励欺骗（reward hacking）**：强化学习中的经典问题——模型可能通过“作弊”方式获得高奖励，例如生成僵硬、缺乏运动的人脸以保持高相似度，而非真正学习身份保持的运动生成。

3. **训练稳定性**：直接优化奖励函数可能导致模型偏离原始分布，产生视觉伪影或丧失运动多样性。

### 本文动机

针对上述挑战，本文提出**身份保持奖励引导优化（Identity-Preserving Reward-guided Optimization, IPRO）**，这是首个将面部奖励反馈框架引入I2V身份保持的工作。IPRO的核心动机在于：

- **消除曝光偏差**：通过从纯噪声开始的策略化（on-policy）训练，使训练和推理的初始分布完全对齐，从根本上解决身份漂移问题。
- **精准的身份奖励**：利用ArcFace人脸识别模型作为可微分的身份奖励函数，其嵌入空间对身份特征高度敏感，能够提供细粒度的身份保持信号。
- **系统性的奖励黑客防御**：通过面部特征池评分机制（Facial Scoring Mechanism, FSM）和多步KL散度正则化，在提升身份一致性的同时有效抑制奖励欺骗，保持生成视频的自然运动表现力。

IPRO无需引入额外的身份编码模块，可直接应用于现有的I2V扩散模型，通过强化学习范式高效提升身份保持能力。



## 核心方法与创新机理

IPRO 的核心创新在于将身份保持问题从“架构修改”范式转向“奖励驱动优化”范式。与传统方法在扩散模型中注入额外的身份编码模块不同，IPRO 直接利用可微分的人脸识别模型作为奖励信号，通过强化学习微调预训练 I2V 模型的去噪网络参数，从根本上改变了模型学习身份一致性的方式。

### 1. 从纯噪声开始的策略化训练：消除曝光偏差

现有 I2V 模型在训练时普遍采用教师强制（teacher forcing），即每一步去噪都依赖真实的前一步潜变量。这种训练范式导致训练与推理之间存在严重的**曝光偏差**（exposure bias）：推理时模型必须从纯高斯噪声开始自回归采样，而训练时从未接触过这种分布。当处理低分辨率人脸与大运动场景时，这一偏差使得身份特征随时间逐渐漂移，最终产生“平均脸”效应。

IPRO 的核心突破在于**将训练过程完全策略化（on-policy）**：每次训练迭代直接从纯高斯噪声 $x_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 开始执行完整的反向采样链，然后计算身份奖励并反向传播梯度。这一设计使得训练分布与推理分布严格对齐，从根源上消除了曝光偏差。优化目标形式化为：

$$J(\theta) = \mathbb{E}_{x_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} [R_{face}(sample(\theta, x_T))]$$

其中 $sample(\theta, x_T)$ 表示从噪声 $x_T$ 出发、使用参数 $\theta$ 的模型执行完整采样链生成的视频，$R_{face}$ 为面部身份奖励函数。该公式直接最大化生成视频的身份一致性期望，而非最小化像素级重建误差。

### 2. ArcFace 可微分奖励函数：将身份感知注入梯度

IPRO 将 **ArcFace 人脸识别模型**作为可微分的奖励函数，这是实现端到端梯度优化的关键。具体而言，对于生成的视频帧和地面真值视频帧，分别提取 ArcFace 嵌入向量，计算两者之间的余弦相似度作为身份保持的度量。由于 ArcFace 网络完全可微，该相似度信号可以通过采样链反向传播至去噪网络的参数。

为降低计算开销，IPRO 采用 **DRaFT 截断策略**，仅通过采样链的最后 $K=4$ 步反向传播奖励梯度：

$$\nabla_{\theta} R_{face}^{K} = \sum_{t=0}^{K} \frac{\partial R_{face}}{\partial x_t} \cdot \frac{\partial x_t}{\partial \theta}$$

这一设计在身份一致性（FaceSim 0.6942）与计算效率之间取得了最优平衡。消融实验表明，增加截断步数虽能提供更丰富的梯度反馈，但计算成本急剧上升，而 $K=4$ 已能有效传递身份约束信号。

### 3. 面部特征池评分机制：提升泛化能力

传统方法通常仅将生成帧与参考图像或时间对齐的地面真值帧进行相似度比较，这导致模型在未见过的姿态和表情下泛化能力不足。IPRO 提出**面部评分机制（Facial Scoring Mechanism, FSM）**，将地面真值视频中所有人脸帧构建为一个**特征池**，计算每生成帧与所有地面真值帧的平均相似度：

$$s_i = \frac{1}{F} \sum_{j=1}^{F} \cos(\phi(\hat{x}_i), \phi(x_j))$$

$$R_{face} = \frac{1}{F'} \sum_{i=1}^{F'} s_i$$

其中 $\phi(\cdot)$ 为 ArcFace 嵌入提取器，$F$ 为地面真值人脸帧数，$F'$ 为生成帧数。这种多角度、多姿态的评分策略使模型学习到视角不变的身份表征，显著提升了在未见姿态下的泛化能力。

### 4. 多步 KL 散度正则化：抑制奖励黑客

直接最大化身份奖励容易引发**奖励黑客**（reward hacking）现象——模型可能通过生成僵硬、缺乏表情变化的面部来“欺骗”奖励函数，导致生成视频丧失自然动态。IPRO 引入**多步 KL 散度正则化**，约束优化后模型与原始预训练模型在反向采样路径上的差异：

$$D_{KL}\big(p_{\theta}(x_{0:T}) \big| \big| p_{\theta_{ref}}(x_{0:T})\big) = \sum_{t=1}^{K} \omega_t' \big|\big| v_{\theta}(x_t, t) - v_{\theta_{ref}}(x_t, t) \big|\big|^2$$

其中 $v_{\theta}$ 和 $v_{\theta_{ref}}$ 分别为当前模型和参考模型预测的速度场。总损失函数为：

$$\mathcal{L} = \lambda_1 \mathcal{L}_{Reward} + \lambda_2 \mathcal{L}_{KL}$$

在损失权重 $\lambda_2/\lambda_1=10$（即 $\lambda_1=0.1, \lambda_2=1$）时，FaceSim 达到 0.6942 且黑客率降至最低。消融实验表明，FSM 和多步 KL 正则化共同将奖励黑客率从 58% 降至 10%，同时保持了高身份一致性。

### 5. 与现有范式的根本差异

IPRO 与现有身份保持方法的关键差异在于**不需要任何额外的身份编码模块**。以 **MoCA†**（Xie et al., arXiv 2025）和 **Concat-ID†**（Zhong et al., arXiv 2025）为代表的 T2V 身份保留方法，通常需要将人脸嵌入注入扩散模型的交叉注意力层，这引入了额外的推理开销和架构耦合。IPRO 则完全通过奖励信号“引导”已有模型的行为，训练完成后模型架构保持不变，推理时无需额外计算。

与 **DPO**（Wallace et al., CVPR 2024）和 **GRPO**（Shao et al., arXiv 2024）等偏好优化方法相比，IPRO 使用身份奖励模型直接提供密集、校准的梯度信号，而非依赖成对偏好比较，在 FaceSim 指标上显著优于两者（0.6942 vs 更低分数）。与 SFT 和 CLIP reward 等训练框架相比，IPRO 的 ArcFace 奖励优化在身份一致性上同样展现出压倒性优势。



IPRO 的整体流程围绕一个核心闭环展开：**从纯噪声出发生成视频 → 解码到像素空间 → 用可微分面部奖励模型评分 → 将奖励梯度反向传播更新去噪网络**。这一闭环直接对齐了训练与推理的分布，从根本上消除了传统 I2V 模型中因教师强制训练带来的曝光偏差。

### 管线总览

如 Figure 2(A) 所示，IPRO 的推理与训练共享同一条采样链：

![[assets/figures/papers/paper_list_l2685_https_arxiv_org_abs_2510_14255/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method. (A) IPRO predicts x¯0 from the noise input xT , and the prediction is visualized through a frozen VAE decoder and scored by a face reward model with our facial scoring mechanism (C). This reward signal is used to update the trainable parts of the model, thereby steering the generation process to produce videos with consistent identity. (B) We further incorporate a KL-divergence regularization to alleviate reward hacking*

1. **噪声初始化**：从纯高斯噪声 $x_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 开始，而非从部分加噪的潜变量出发。这一设计使模型始终处于策略化采样状态，训练与推理的初始分布完全一致。
2. **去噪预测**：可训练的 DiT 去噪器 $ \epsilon_\theta $ 沿反向扩散链逐步去噪，最终预测干净潜变量 $\hat{x}_0$。
3. **解码可视化**：冻结的 VAE 解码器将 $\hat{x}_0$ 解码到像素空间，生成可观看的视频帧。
4. **面部奖励评分**：生成的视频帧与地面真值视频帧一同送入面部奖励模型（ArcFace 嵌入 + 面部评分机制 FSM），计算身份相似度奖励 $R_{face}$。
5. **梯度回传**：$R_{face}$ 的梯度仅通过采样链的最后 $K=4$ 步反向传播（截断梯度策略），更新去噪网络的可训练参数。

这一闭环的精妙之处在于：**奖励信号直接作用于生成过程本身**，而非像 SFT 那样依赖预先对齐的帧对，也非像 CLIP reward 那样使用粗粒度的语义相似度。面部奖励模型提供的是密集、校准的身份信号，能够精确引导模型在去噪过程中保留人脸身份特征。

### 核心模块与职责

IPRO 管线由六个关键模块构成，各自承担明确的职责：

| 模块 | 角色 | 可训练性 |
|------|------|----------|
| IPRO Predictor (DiT denoiser) | 从噪声 $x_T$ 预测干净视频帧 $\hat{x}_0$ | 可训练 |
| VAE Decoder | 将潜空间预测解码到像素空间 | 冻结 |
| Face Reward Model (ArcFace) | 提取面部嵌入，计算身份相似度 | 冻结 |
| Facial Scoring Mechanism (FSM) | 利用 GT 视频所有人脸帧构建特征池，计算多角度平均相似度 | 无参数 |
| KL-divergence Regularization | 约束当前模型与参考模型在采样路径上的差异 | 损失项 |
| Gradient Truncation ($K=4$) | 仅通过最后 $K$ 步反向传播奖励梯度 | 策略选择 |

**FSM 的设计动机**：若仅将生成帧与单一 GT 帧比较，模型可能学到“记住某一特定角度”而非“保留身份本质”。FSM 将 GT 视频中所有人脸帧作为参考池，对每个生成帧计算其与所有 GT 帧的 ArcFace 余弦相似度平均值 $s_i = \frac{1}{F}\sum_{j=1}^{F} \cos(\phi(\hat{x}_i), \phi(x_j))$，再对所有生成帧取平均得到 $R_{face} = \frac{1}{F'}\sum_{i=1}^{F'} s_i$。这一机制鼓励模型学习视角不变的身份特征。

**KL 正则化的必要性**：如 Figure 3 所示，不加 KL 正则化时，模型在训练过程中 KL 散度迅速飙升且剧烈波动（红色曲线），意味着优化后的采样分布严重偏离原始扩散先验，导致生成质量崩溃。加入多步 KL 正则化（蓝色曲线）后，散度保持低位稳定，模型在提升身份一致性的同时维持了视频生成质量。正则化形式为：

$$D_{KL}\big(p_{\theta}(x_{0:T}) || p_{\theta_{ref}}(x_{0:T})\big) = \sum_{t=1}^{K} \omega_t' || v_{\theta}(x_t, t) - v_{\theta_{ref}}(x_t, t) ||^2$$

即在反向采样轨迹的最后 $K$ 步上约束速度预测 $v_\theta$ 与参考模型 $v_{\theta_{ref}}$ 的差异。

### 训练目标

整体训练损失由面部奖励损失和 KL 正则化损失加权求和：

$$\mathcal{L} = \lambda_1 \mathcal{L}_{Reward} + \lambda_2 \mathcal{L}_{KL}$$

其中 $\lambda_1=0.1$，$\lambda_2=1$（即 $\lambda_2/\lambda_1=10$），该比例在消融实验中被证明能同时获得高 FaceSim 和低奖励黑客率。训练仅需 100 步、batch size 64、学习率 $2\times10^{-5}$（Adam 优化器），计算开销极低。

### 与基线方法的本质差异

传统 I2V 训练使用教师强制：模型在训练时看到的是 GT 前帧，推理时却只能依赖自己生成的前帧，这种曝光偏差导致身份特征随时间漂移，最终产生“平均脸”效应。IPRO 的策略化训练从纯噪声开始，使模型始终面对自己生成的上下文，训练与推理分布严格对齐。此外，IPRO 不需要额外插入身份模块（如 Concat-ID 的身份嵌入层或 MoCA 的特征注入分支），而是通过奖励信号直接塑造去噪网络的内部表示，方法更加简洁且通用。



### 3.1 问题形式化：从扩散模型到身份奖励优化

IPRO 建立在视频扩散模型的去噪框架之上。标准扩散模型通过前向马尔可夫链逐步向数据添加高斯噪声：

$$
q ( x _ { t } | x _ { t - 1 } ) = \mathcal { N } ( x _ { t } ; \sqrt { 1 - \beta _ { t } } x _ { t - 1 } , \beta _ { t } \mathbf { I } ) , \quad t = 1 , . . . , T .
$$

其中 $\beta_t$ 为固定方差调度参数，$T$ 为总扩散步数。去噪网络 $\epsilon_\theta$ 通过最小化以下损失学习逆向过程：

$$
\mathcal { L } _ { \theta } = \mathbb { E } _ { t , x _ { 0 } , \epsilon } \left[ \| \epsilon - \epsilon _ { \theta } ( x _ { t } , t ) \| ^ { 2 } \right].
$$

在此基础上，IPRO 将身份保持问题转化为**最大化面部奖励期望**的优化目标。令 $R_{face}(\cdot)$ 为可微分的面部身份奖励函数，$\text{sample}(\theta, x_T)$ 表示以纯高斯噪声 $x_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 为起点、由参数 $\theta$ 控制的完整采样链生成的视频，则优化目标为：

$$
J ( \theta ) = \mathbb { E } _ { x _ { T } \sim \mathcal { N } ( \mathbf { 0 } , \mathbf { I } ) } \left[ R _ { f a c e } \left( \text{sample} ( \theta , x _ { T } ) \right) \right].
$$

这一形式化的关键意义在于：**训练从纯噪声开始（on-policy），消除了标准监督微调中教师强制（teacher forcing）带来的曝光偏差**，使训练分布与推理分布严格对齐。

---

### 3.2 核心模块一：截断梯度身份奖励优化

直接通过完整采样链反向传播奖励梯度在计算上不可行。IPRO 采用 **DRaFT 截断策略**，仅通过采样链的最后 $K$ 步传播梯度：

$$
\nabla _ { \theta } R _ { f a c e } ^ { K } = \sum _ { t = 0 } ^ { K } { \frac { \partial R _ { f a c e } } { \partial x _ { t } } } \cdot { \frac { \partial x _ { t } } { \partial \theta } }.
$$

其中 $x_t$ 表示逆向采样链中第 $t$ 步的潜变量。实验确定 $K=4$ 在身份一致性与计算开销之间取得最佳平衡（Table 5, Supplemental D）。该模块使奖励信号能够**密集地、可校准地**反馈到模型参数更新中，这是 IPRO 区别于 DPO、GRPO 等间接偏好优化方法的核心机制。

![[assets/figures/papers/paper_list_l2685_https_arxiv_org_abs_2510_14255/figures/013_Table_5.jpg]]
*Table 5: Ablation study on different initial gradient steps*

---

### 3.3 核心模块二：面部评分机制（FSM）

为避免模型仅学习与单一参考帧对齐而导致泛化能力不足，IPRO 设计了**面部特征池评分机制**。具体而言，将地面真值视频中所有人脸帧作为参考池，计算每生成帧与所有地面真值帧的平均相似度：

$$
s _ { i } = \frac { 1 } { F } \sum _ { j = 1 } ^ { F } \cos \left( \phi ( \hat { x } _ { i } ) , \phi ( x _ { j } ) \right).
$$

其中 $\phi(\cdot)$ 为 ArcFace 人脸识别模型提取的嵌入向量，$\hat{x}_i$ 为第 $i$ 生成帧，$x_j$ 为第 $j$ 地面真值帧，$F$ 为地面真值人脸帧总数。整个生成视频的身份奖励分数为所有生成帧相似度的均值：

$$
R _ { f a c e } = \frac { 1 } { F ^ { \prime } } \sum _ { i = 1 } ^ { F ^ { \prime } } s _ { i }.
$$

FSM 的因果作用在于：**多角度、多帧的特征池比较迫使模型学习身份的不变表征，而非过拟合到单一姿态或表情**。消融实验表明，移除 FSM 后奖励黑客率从 10% 飙升至 58%（Table 6）。

---

### 3.4 核心模块三：多步 KL 散度正则化

直接最大化面部奖励可能导致**奖励黑客（reward hacking）**——模型生成僵硬、缺乏动态变化的视频以获取高分。IPRO 通过约束当前模型 $\theta$ 与参考模型 $\theta_{ref}$ 在逆向采样路径上的分布差异来抑制这一现象：

$$
D _ { K L } \big ( p _ { \theta } ( x _ { 0 : T } ) \big \| p _ { \theta _ { r e f } } ( x _ { 0 : T } ) \big ) = \sum _ { t = 1 } ^ { K } \omega _ { t } ^ { \prime } \big \| v _ { \theta } ( x _ { t } , t ) - v _ { \theta _ { r e f } } ( x _ { t } , t ) \big \| ^ { 2 }.
$$

其中 $v_\theta(x_t, t)$ 为速度预测（velocity prediction），$\omega_t'$ 为各步权重。该正则化在**最后 $K$ 步**上施加约束，与截断梯度范围一致，形成协同效应。

整体训练损失为奖励损失与 KL 正则化的加权和：

$$
\mathcal { L } = \lambda _ { 1 } \mathcal { L } _ { R e w a r d } + \lambda _ { 2 } \mathcal { L } _ { K L }.
$$

实验确定 $\lambda_1=0.1, \lambda_2=1$（即 $\lambda_2/\lambda_1=10$）时 FaceSim 达到 0.6942 且黑客率最低（Table 7）。Figure 3 的训练动态曲线进一步验证：**含 KL 正则化的模型（蓝色）KL 散度保持低且稳定，而不含正则化的模型（红色）散度快速发散**，直观展示了该模块对训练稳定性的因果贡献。

![[assets/figures/papers/paper_list_l2685_https_arxiv_org_abs_2510_14255/figures/003_Figure_3.jpg]]
*Figure 3: The effect of KL regularization on KL divergence across training steps. The model trained with KL regularization (blue) maintains a low and stable divergence, whereas the model without regularization (red) exhibits a rapid and volatile increase*

---

### 3.5 管线模块总览

IPRO 的完整推理与训练管线（Figure 2）包含以下可训练与冻结模块：

| 模块 | 角色 | 状态 |
|------|------|------|
| **IPRO Predictor (DiT denoiser)** | 从噪声 $x_T$ 预测干净视频帧 $\bar{x}_0$ | 可训练 |
| **VAE Decoder** | 将潜空间预测解码到像素空间进行可视化与评分 | 冻结 |
| **Face Reward Model (ArcFace)** | 计算生成视频与地面真值视频的面部身份相似度 | 冻结 |
| **Facial Scoring Mechanism (FSM)** | 利用地面真值所有人脸帧构建特征池，计算多角度平均相似度 | 冻结（评分逻辑） |
| **KL-divergence Regularization** | 约束当前模型与参考模型的采样路径差异 | 损失项 |
| **Gradient Truncation (K=4)** | 仅通过最后 4 步反向传播奖励梯度 | 训练策略 |

各模块的因果链路为：**截断梯度使奖励信号可高效反向传播 → FSM 提供多角度身份监督 → KL 正则化抑制奖励黑客 → 三者协同实现身份一致性的大幅提升**。消融实验（Table 6, Table 7）系统验证了这一链路中每个环节的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l2685_https_arxiv_org_abs_2510_14255/figures/012_Figure_8.jpg]]
*Figure 8: Ablation study on reward hacking. Without KL-divergence regularization or the FSM module, the generated video overly adheres to the input image, resulting in facial rigidity and reward hacking phenomenon. However, our method enables accurate, expressive prompt-following behavior, such as opening eyes*



## 实验与关键发现

### 实验设置

实验基于两个基础模型进行验证：内部 15B 参数 I2V 模型，以及开源 **Wan 2.2** 系列模型（5B 与 27B-A14B，Team Wan et al., arXiv 2025）。训练采用 Adam 优化器，学习率 $2\times10^{-5}$，共训练 100 步，批次大小为 64。核心超参数设置为：截断梯度步数 $K=4$，面部奖励权重 $\lambda_1=0.1$，KL 散度正则化权重 $\lambda_2=1$。评估在自建的 600 场景小脸评测集上进行，以 FaceSim（ArcFace 嵌入余弦相似度）作为身份一致性核心指标，同时辅以 VBench-I2V 多维度指标。

### 主实验结果

**Table 1** 展示了 IPRO 框架在三个基础模型上的定量提升。在内部 I2V 模型上，FaceSim 从基线 0.4769 提升至 0.6960，相对提升 **45.9%**；在 Wan 2.2 5B 上从 0.3788 提升至 0.5460（+44.1%）；在 Wan 2.2 27B-A14B 上从 0.5780 提升至 0.6942（+20.1%）。值得注意的是，身份一致性的大幅提升并未牺牲其他维度表现：内部模型的 Subject Consistency 从 0.9768 微升至 0.9811，其余 VBench-I2V 指标保持稳定，说明优化过程具有较好的维度解耦性。

**Table 2** 将 IPRO 与适配到 I2V 场景的身份保留方法 **MoCA†**（Xie et al., arXiv 2025）和 **Concat-ID†**（Zhong et al., arXiv 2025）进行对比。IPRO 以 FaceSim 0.6942 达到所有方法中的最高值，且无需引入额外的身份注入模块。**Table 3** 进一步对比了基于偏好优化的 **DPO**（Wallace et al., CVPR 2024）和 **GRPO**（Shao et al., arXiv 2024），IPRO 在 FaceSim 上同样显著领先，验证了基于可微分奖励的直接策略梯度优化相较于偏好排序方法的优势。

### 训练框架消融

**Table 4** 对比了三种训练框架：监督微调（SFT）、CLIP 相似度奖励训练、以及 IPRO 的 ArcFace 奖励训练。SFT 受限于教师强制（teacher forcing）与推理时的分布不匹配，FaceSim 提升有限；CLIP 奖励由于缺乏面部细粒度判别能力，无法提供有效的身份保持信号。IPRO 凭借 ArcFace 的高判别性嵌入空间和策略化训练，在 FaceSim 上大幅领先，证实了“从纯噪声开始采样→可微分面部奖励反馈”这一因果路径的有效性。

### 关键组件消融

**面部特征池（FSM）与多步 KL 正则化**是抑制奖励欺骗（reward hacking）的两大支柱。**Table 6** 显示：移除两者后，奖励黑客率高达 58%，生成视频出现面部僵硬、过度贴合输入图像的现象；单独加入 FSM 或 KL 正则化可将黑客率分别降至 25% 和 30%；两者共同作用时黑客率降至 10%，同时 FaceSim 保持在 0.6942。这验证了 FSM 通过多帧地面真值特征池提供多角度参考信号，以及 KL 正则化通过约束采样路径偏离来防止模型“投机取巧”的互补机制。

**Figure 3** 从训练动态角度佐证了 KL 正则化的稳定作用：无正则化时，KL 散度随训练步数急剧上升且剧烈波动；加入正则化后，KL 散度始终维持在低位且平稳，表明模型在优化身份奖励的同时未偏离原始模型的生成分布。

**截断梯度步数 $K$** 的消融（Table 5）表明，$K=4$ 在身份一致性（FaceSim 0.6942）与计算开销之间取得最佳平衡。过小的 $K$ 导致奖励信号传递不充分，过大的 $K$ 则增加显存消耗且收益递减。这一设计源于 DRaFT 截断策略，仅通过采样链的最后 4 步反向传播奖励梯度。

**损失权重比 $\lambda_2/\lambda_1$** 的消融（Table 7）显示，当 $\lambda_1=0.1$、$\lambda_2=1$（即比值 10）时，FaceSim 达到 0.6942 且黑客率最低。过大的 KL 权重会过度约束模型更新，削弱身份优化效果；过小的 KL 权重则无法有效抑制奖励欺骗。

### 定性分析

**Figure 4** 展示了 IPRO 集成前后的视觉对比：基线模型在低分辨率人脸和大运动场景下出现明显的身份漂移，面部特征逐渐模糊为“平均脸”；IPRO 生成的视频在跨帧间保持稳定的面部结构、五官比例和肤色一致性。**Figure 5** 与 MoCA†、Concat-ID† 的对比显示，后者在侧脸、遮挡等困难角度下身份信息丢失严重，而 IPRO 保持了更忠实的身份还原。**Figure 6** 与 DPO、GRPO 的对比进一步表明，基于偏好的方法在视频生成中难以提供逐帧密集的细粒度反馈，导致身份保持不稳定。

**Figure 8** 直观呈现了奖励欺骗现象：移除 FSM 或 KL 正则化后，生成视频中人物面部僵硬、缺乏表情变化，甚至无法执行“睁眼”等简单动作指令——模型学会了通过“冻结”面部来最大化奖励分数。完整 IPRO 则能生成准确的表情跟随行为。

### 鲁棒性分析

**Table 8** 测试了不同人脸识别模型（包括多种 ArcFace 变体及其他嵌入器）作为奖励信号源时的 FaceSim 稳定性。结果显示 IPRO 对奖励模型的选择具有一定鲁棒性，不同嵌入器下 FaceSim 均保持在较高水平，表明优化框架本身而非特定嵌入器是性能提升的主因。

### 失败模式与局限

尽管 FSM 和 KL 正则化大幅抑制了奖励欺骗，黑客率仍未被完全消除（约 10%），在极端条件下（如输入图像分辨率极低、人脸占比极小）仍可能出现面部过度平滑或微表情丢失。此外，当前方法仅关注面部身份一致性，对于人物其他身份元素（如配饰、服装、体型特征等）的保持尚未涉及。论文在补充材料中承认该方法可能被滥用于非自愿深度伪造，并表示将与法律和伦理专家合作推进安全措施。

### 补充图表

![[assets/figures/papers/paper_list_l2685_https_arxiv_org_abs_2510_14255/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparisons. Our method achieves more consistent face similarity than the baseline, without compromising its performance on other dimensions*

![[assets/figures/papers/paper_list_l2685_https_arxiv_org_abs_2510_14255/figures/009_Table_2.jpg]]
*Table 2: Comparison with other methods. Our method achieves the highest face similarity among all compared methods*

![[assets/figures/papers/paper_list_l2685_https_arxiv_org_abs_2510_14255/figures/011_Table_3.jpg]]
*Table 3: Comparison with DPO and GRPO. Our method outperforms DPO and GRPO in preserving face similarity*

![[assets/figures/papers/paper_list_l2685_https_arxiv_org_abs_2510_14255/figures/010_Table_4.jpg]]
*Table 4: Ablation study on different training frameworks. Our method outperforms SFT and CLIP reward in face similarity*

![[assets/figures/papers/paper_list_l2685_https_arxiv_org_abs_2510_14255/figures/015_Table_6.jpg]]
*Table 6: Ablation study on reward hacking. Our method enhances facial consistency without noticeable hacking*

![[assets/figures/papers/paper_list_l2685_https_arxiv_org_abs_2510_14255/figures/021_Table_7.jpg]]
*Table 7: Ablation study on loss weights*

![[assets/figures/papers/paper_list_l2685_https_arxiv_org_abs_2510_14255/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison before and after integrating our framework. Our method achieves more stable generation and superior identity preservation compared to the baseline*

![[assets/figures/papers/paper_list_l2685_https_arxiv_org_abs_2510_14255/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative comparison with DPO and GRPO. Our method achieves more stable generation and superior identity preservation compared to others*



## 定位与知识库关联

### 1. 问题定位：I2V身份漂移的本质瓶颈

现有图像到视频（I2V）生成模型在处理包含人脸的低分辨率输入图像时，面临一个核心困境：随着视频帧的推进，人物面部身份特征逐渐向“平均脸”漂移。这一现象的根源并非模型容量不足，而是训练与推理之间的**曝光偏差**（exposure bias）——标准扩散模型训练采用教师强制（teacher forcing），依赖真实中间状态；推理时则从纯噪声自回归采样，分布不匹配导致误差累积，身份信息在长序列生成中逐步丢失。

单纯在架构中嵌入身份模块（如额外的面部编码器或交叉注意力层）无法从根本上解决该问题，因为曝光偏差存在于采样动力学层面，而非表示层面。IPRO的切入点正是这一被忽视的因果机制：通过将训练过程本身策略化（on-policy），从纯高斯噪声初始化采样轨迹，消除训练-推理分布鸿沟。

### 2. 方法坐标系：奖励引导优化谱系中的定位

IPRO属于**扩散模型奖励引导优化**这一新兴方法家族。与现有工作的关系可从三个维度定位：

**（1）与监督微调（SFT）和CLIP奖励基线的对比**

SFT直接最小化预测噪声与真实噪声的均方误差，缺乏对生成结果语义质量的显式反馈。CLIP奖励方法虽然引入了可微分奖励信号，但CLIP嵌入空间对人脸身份细节的敏感性远低于专用人脸识别模型。消融实验（Table 4）表明，基于ArcFace的奖励优化在FaceSim指标上显著优于SFT和CLIP奖励训练框架，验证了奖励函数选择对身份保持任务的决定性影响。

**（2）与偏好优化方法的对比**

**DPO**（Wallace et al., CVPR 2024）和**GRPO**（Shao et al., arXiv 2024）通过成对偏好数据或组相对优势间接优化生成质量，奖励信号稀疏且依赖对比样本的构造质量。IPRO采用直接奖励梯度反向传播，通过ArcFace模型提供逐帧密集、校准的身份信号。Table 3显示IPRO的FaceSim达到0.6942，优于DPO和GRPO，表明在身份保持这一特定维度上，直接奖励优化比偏好对齐更有效。

**（3）与身份保持专用方法的对比**

**MoCA†**（Xie et al., arXiv 2025）和**Concat-ID†**（Zhong et al., arXiv 2025）原本为文本到视频（T2V）设计的身份保留方法，被适配到I2V场景。这些方法通常依赖额外的身份嵌入模块或交叉注意力注入机制。Table 2显示IPRO在FaceSim指标上达到0.6942，显著高于这些方法，且无需引入额外身份模块，体现了“奖励驱动”路径相对于“架构驱动”路径的优势。

### 3. 核心贡献的知识增量

IPRO的方法论贡献可解构为三个相互依赖的组件：

**组件一：策略化训练与截断梯度**

从纯噪声开始的on-policy训练（公式 $J(\theta) = \mathbb{E}_{x_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} [R_{face}(sample(\theta, x_T))]$ ）消除了曝光偏差的根源。同时采用DRaFT截断策略，仅通过采样链的最后 $K=4$ 步反向传播奖励梯度（公式 $\nabla_{\theta} R_{face}^{K} = \sum_{t=0}^{K} \frac{\partial R_{face}}{\partial x_t} \cdot \frac{\partial x_t}{\partial \theta}$ ），在身份一致性与计算开销之间取得平衡。

**组件二：面部特征池评分机制（FSM）**

传统做法仅将生成帧与时间对齐的单帧真值比较，FSM将真值视频中所有人脸帧构建为参考池，计算每生成帧与所有真值帧的平均ArcFace余弦相似度（公式 $s_i = \frac{1}{F} \sum_{j=1}^{F} \cos(\phi(\hat{x}_i), \phi(x_j))$ ）。这一设计允许模型学习身份的多角度不变表示，而非过拟合特定帧的瞬时表情或姿态。

**组件三：多步KL散度正则化**

直接最大化奖励函数容易诱发奖励黑客（reward hacking）——模型生成高度重复、僵硬的面部以获取高分，丧失运动自然度。IPRO引入多步KL散度正则化（公式 $D_{KL}(p_{\theta}(x_{0:T}) || p_{\theta_{ref}}(x_{0:T})) = \sum_{t=1}^{K} \omega_t' ||v_{\theta}(x_t, t) - v_{\theta_{ref}}(x_t, t)||^2$ ），约束优化模型与原始参考模型在反向采样路径上的速度预测差异，将黑客率从58%降至约10%（Table 6），同时保持FaceSim=0.6942。

### 4. 适用边界与局限

**已验证的适用范围：**
- 低分辨率人脸场景（small-face evaluation set, 600个场景）下表现优异
- 跨模型架构泛化：在in-house 15B模型（FaceSim提升45.9%）、Wan 2.2 5B（提升44.1%）和Wan 2.2 27B-A14B（提升20.1%）上均有效
- 多人场景下保持身份一致性（Figure 11）

**明确局限：**
- 身份保持仅关注面部区域，对于人物其他身份元素（配饰、服装、体型等）的保持尚未探索
- 奖励黑客现象未能完全消除（黑客率约10%），在极端优化压力下仍可能出现面部僵硬
- 依赖ArcFace等预训练人脸识别模型作为奖励函数，对人脸检测失败或极端姿态的鲁棒性受限于上游模型能力

### 5. 开放问题

论文明确指出将身份保持从面部扩展到非面部属性是未来的研究方向。更广义地，该方法框架提出了一个开放问题：**如何为视频扩散模型设计多维度、可分解的奖励函数，在身份一致性、运动自然度、文本对齐之间实现精细权衡？** 当前的总损失 $\mathcal{L} = \lambda_1 \mathcal{L}_{Reward} + \lambda_2 \mathcal{L}_{KL}$ 仅通过两个标量权重平衡，未来可能需要更结构化的多目标优化策略。



## 原文 PDF

![[paperPDFs/CVPR_2026/Identity_Preserving_Image_to_Video_Generation_via_Reward_Guided_Optimization.pdf]]
