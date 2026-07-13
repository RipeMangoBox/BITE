---
title: Learnable Motion-Focused Tokenization for Effective and Efficient Video Unsupervised Domain Adaptation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Learnable_Motion_Focused_Tokenization_for_Effective_and_Efficient_Video_Unsupervised_Domain_Adaptation.pdf
project_link: null
code_link: null
aliases:
- LMFTL
- LMFTEEVUDA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入可学习的运动聚焦令牌化（LMFT），通过计算相邻令牌间的L1运动差异并利用强化学习动态学习丢弃低运动背景令牌的阈值，仅保留动作相关的运动令牌。
primary_logic: 只传递运动丰富的令牌不仅能缓解背景诱导的域偏移、提升域自适应效果，还能大幅减少传入ViT的令牌数，显著提高训练和推理效率；利用RL让阈值自适应学习，避免手动调参并优化动作识别与效率的平衡。
claims:
- 在三个标准VUDA基准（Daily-DA、UCF-HMDB_full、ActorShift）上，LMFT均显著超越现有最优方法，分别提升5.3%、1.8%和12%的平均Top-1准确率。
- LMFT在训练和推理效率上均优于其他令牌压缩方法（ToMe、PruMerge、DivPrune、RLT），在保持最高准确率的同时实现约1.4倍训练加速和0.82倍计算成本。
- 与直接采用Gumbel-Softmax近似离散选择相比，基于RL的阈值学习在准确率和内存/时间效率上均有优势（例如H←W场景Accuracy 74.2 vs 73.3，训练时间2784s vs 3275s）。
- Daily-DA 上 Top-1 Accuracy (%) Average = 64.5
---

# Learnable Motion-Focused Tokenization for Effective and Efficient Video Unsupervised Domain Adaptation

> [!tip] 核心洞察
> 只传递运动丰富的令牌不仅能缓解背景诱导的域偏移、提升域自适应效果，还能大幅减少传入ViT的令牌数，显著提高训练和推理效率；利用RL让阈值自适应学习，避免手动调参并优化动作识别与效率的平衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | 用于有效高效视频无监督域自适应的可学习运动聚焦令牌化 |
| 英文题名 | Learnable Motion-Focused Tokenization for Effective and Efficient Video Unsupervised Domain Adaptation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.09955) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Learnable Motion-Focused Tokenization (LMFT) |
| Dataset | Daily-DA, UCF-HMDB_full, ActorShift |

> [!tip] 效果简介
> - Daily-DA 上，Top-1 Accuracy (%) Average 64.5 vs 59.2 (UNITE) (+5.3)。
> - UCF-HMDB_full 上，Top-1 Accuracy (%) Average 96.4 vs 94.6 (UNITE) (+1.8)。
> - ActorShift 上，Top-1 Accuracy (%) Average 88.4 vs 76.4 (UNITE) (+12.0)。

## 概要

**问题瓶颈**：现有视频无监督域自适应（VUDA）方法通常对视频的所有时空令牌进行全量处理，导致两个关键瓶颈——大量静态或无关背景令牌加剧了域偏移，干扰动作语义在源域与目标域之间的迁移；同时，自注意力计算量随令牌数平方增长，使得训练和推理效率低下。

**核心思路**：本文提出可学习运动聚焦令牌化（Learnable Motion-Focused Tokenization, LMFT），通过计算相邻时空令牌间的 L1 运动差异，并利用强化学习动态学习一个丢弃低运动背景令牌的阈值，仅保留动作相关的运动令牌送入 ViT 进行域自适应。

**核心洞察**：只传递运动丰富的令牌，既能缓解背景诱导的域偏移、提升域自适应效果，又能大幅减少传入 ViT 的令牌数量，显著提高训练和推理效率。采用强化学习让阈值自适应学习，避免了手动调参，并在动作识别准确率与计算效率之间取得优化平衡。

**方法定位**：LMFT 属于“令牌选择”范式，与通用令牌压缩方法（如 Token Merging、Run-Length Tokenization）不同，它专为视频域自适应设计，以运动信号为选择依据，并与 CLIP 伪标签生成及 ViT 域自适应训练框架协同工作。

**主要结果**：在三个标准 VUDA 基准（Daily-DA、UCF-HMDB_full、ActorShift）上，LMFT 均显著超越现有最优方法，平均 Top-1 准确率分别提升 5.3%、1.8% 和 12%。同时，LMFT 在保持最高准确率的前提下，实现了约 1.4 倍训练加速和 0.82 倍计算成本，在精度-效率权衡上全面优于其他令牌压缩方法。



### 视频无监督域自适应的核心瓶颈

视频无监督域自适应（Video Unsupervised Domain Adaptation, VUDA）旨在将源域标注视频中学习的动作识别能力迁移到无标注的目标域，其核心挑战在于弥合域偏移（domain shift）对时空特征对齐的干扰。现有VUDA方法通常采用基于ViT的架构，将视频帧完整地划分为时空补丁令牌（spatiotemporal patch tokens），并将所有令牌送入自注意力机制进行域自适应学习。然而，这一全量处理范式存在两个根本性缺陷：

1. **背景诱导的域偏移加剧**：视频中大量令牌对应于静态或低运动背景区域（如墙壁、地面、天空），这些区域在不同域之间往往呈现显著的外观差异，但其变化与动作语义无关。当模型不加区分地对所有令牌进行域对齐时，背景令牌的跨域差异会干扰动作相关令牌的语义迁移，导致域自适应效果退化。

2. **计算效率低下**：ViT中自注意力机制的计算复杂度与令牌数量的平方成正比。对于视频输入，令牌总数 $N = N_t \times N_x \times N_y$ 通常规模庞大（例如，16帧、224×224分辨率、16×16补丁尺寸下产生约1568个令牌），全量处理带来沉重的训练和推理开销。

### 现有方法的局限

当前VUDA方法在应对上述瓶颈时存在明显不足：

- **域自适应方法层面**：以 **UNITE**（Reddy et al., CVPR 2024）为代表的最先进方法，通过掩码建模与自训练策略实现域对齐，但其仍对视频所有时空令牌进行全量处理，未考虑令牌的选择性利用。**UDAVT**（Da Costa et al., ICPR 2022）、**CoMix**（Sahoo et al., NeurIPS 2021）和 **TA³N**（Chen et al., ICCV 2019）等方法同样遵循全令牌处理范式，未能从令牌筛选角度缓解背景诱导的域偏移问题。

- **令牌压缩方法层面**：通用令牌缩减方法如 **Token Merging (ToMe)**（Bolya et al., ICLR 2023）通过合并相似令牌来降低计算量，但其合并策略不区分运动与静态区域，可能将动作相关令牌与背景令牌错误合并，损害动作识别精度。**Run-Length Tokenization (RLT)**（Choudhury et al., NeurIPS 2024）通过移除时间维度上重复的补丁来压缩视频令牌，但其设计初衷并非针对域自适应场景，无法保证保留的令牌有利于跨域动作语义对齐。

上述方法均未从根本上解决“哪些令牌对域自适应真正重要”这一核心问题。

### 本文动机：运动聚焦令牌化的核心洞察

本文的核心洞察在于：**动作识别任务的域自适应应聚焦于运动丰富的时空区域，而非静态背景区域**。具体而言：

- **因果机制**：动作的本质体现为时空维度的运动变化。相邻帧之间具有显著像素差异的补丁区域通常对应动作执行的主体部位（如挥动的手臂、移动的腿部），这些区域携带了跨域不变的动作语义信息。相反，低运动区域（如静态背景）往往在不同域之间呈现较大的外观分布差异，是域偏移的主要来源。

- **效率与效果的双重收益**：若能动态识别并仅保留高运动令牌、丢弃低运动背景令牌，不仅能减少传入ViT的令牌数量以提升计算效率，还能使模型免受背景诱导的域偏移干扰，更专注于学习跨域不变的动作表征。

基于这一洞察，本文提出**可学习运动聚焦令牌化（Learnable Motion-Focused Tokenization, LMFT）**，通过计算相邻时空补丁间的L1运动差异，并利用强化学习动态学习最优的运动阈值 $\tau$，实现自适应地丢弃低运动令牌、保留动作相关令牌，从而同时提升VUDA的域自适应效果和计算效率。



## 核心方法与创新机理

本文提出的**可学习运动聚焦令牌化（Learnable Motion-Focused Tokenization, LMFT）** 针对现有视频无监督域自适应（VUDA）方法的核心瓶颈，引入了一个关键的技术变更点：**视频令牌选择策略的根本性重构**。

### 变更点：从全量令牌处理到运动聚焦令牌选择

现有VUDA方法（如 **UNITE**（Reddy et al., CVPR 2024）、**UDAVT**（Da Costa et al., ICPR 2022））普遍采用标准视频ViT令牌化策略：将输入视频的所有时空块 $N = N_t \times N_x \times N_y$ 无差别地送入自注意力层进行处理。这一策略带来了两个严重问题：
1. **域偏移加剧**：大量静态或低运动背景令牌携带域特定但任务无关的视觉偏差，干扰了动作语义的跨域迁移；
2. **计算效率低下**：自注意力计算量随令牌数平方增长，大量冗余令牌造成不必要的算力消耗。

LMFT的核心创新在于将这一**全量处理**策略替换为**选择性丢弃**策略：通过计算相邻时空块之间的像素级L1运动差异，动态学习一个阈值 $\tau$，仅保留运动能量高于该阈值的令牌，丢弃低运动、冗余的背景令牌。具体而言，LMFT首先计算运动差异张量：

$$\mathbf{D}_t^{x,y} = \left| \bar{\mathbf{P}}_{t+1}^{x,y} - \bar{\mathbf{P}}_t^{x,y} \right|$$

经归一化得到运动能量张量 $\mathbf{E}_{\text{motion}}$ 后，通过二值掩码进行令牌选择：

$$\mathbf{M}_{t,x,y} = \begin{cases} 1, & \text{if } (\mathbf{E}_{\text{motion}})_{t,x,y} > \tau \\ 0, & \text{otherwise} \end{cases}$$

这一变更的本质洞察在于：**只传递运动丰富的令牌不仅能缓解背景诱导的域偏移、提升域自适应效果，还能大幅减少传入ViT的令牌数，同时显著提高训练和推理效率**。

### 阈值学习的自适应机制

与手工设定固定阈值或采用可微近似（如Gumbel-Softmax）不同，LMFT采用**基于强化学习的阈值学习策略**，将阈值 $\tau$ 的优化建模为一个策略梯度问题。策略 $\pi_\theta$ 被训练以最大化平衡准确率与效率的奖励信号：

$$R_{\mathrm{src}} = -\lambda_{\mathcal{L}} \mathcal{L}_s - (1 - \rho_s), \quad R_{\mathrm{tgt}} = -\lambda_{\mathcal{L}} \mathcal{L}_t - (1 - \rho_t)$$

其中 $\rho_s$、$\rho_t$ 分别为源域和目标域的令牌保留比例。通过REINFORCE梯度估计器优化策略参数：

$$\nabla_\theta \mathcal{I}(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \big[ (R(\tau) - b) \nabla_\theta \log \pi_\theta(\tau) \big]$$

这一设计使得阈值能够根据数据特性自适应调整，避免了手动调参的困难，并在动作识别精度与计算效率之间取得最优平衡。消融实验证实，基于RL的阈值学习在H←W场景下准确率较Gumbel-Softmax提升0.9%（74.2 vs 73.3），训练时间减少15%，最大GPU内存降低13%（Table 10）。

### 创新定位与差异化

与通用令牌压缩方法（如 **Token Merging (ToMe)**（Bolya et al., ICLR 2023）、**Run-Length Tokenization (RLT)**（Choudhury et al., NeurIPS 2024））相比，LMFT的独特之处在于其令牌选择策略**专为视频动作识别中的域自适应设计**——它利用运动信息作为域不变线索来区分任务相关与无关令牌，而非仅基于视觉相似性或时间冗余进行压缩。这一任务感知的设计使其在三个标准VUDA基准上均显著超越现有最优方法（Daily-DA +5.3%, UCF-HMDB_full +1.8%, ActorShift +12%），同时实现约1.4倍训练加速和0.82倍计算成本（Table 4, Table 5）。



LMFT 的整体流水线遵循**源域与目标域对称处理、运动令牌选择前置、ViT 域自适应联合优化**的设计范式，其核心思路是在令牌进入 ViT 骨干网络之前，通过可学习的运动聚焦机制剔除冗余背景令牌，从而同时缓解域偏移并降低计算开销。

### 输入与令牌化

给定源域或目标域视频 $\mathbf{V} \in \mathbb{R}^{T \times C \times H \times W}$，首先将其划分为时空块（tubelet），每个块跨越 $t_p$ 帧、空间分辨率为 $p \times p$，形成初始令牌集合 $\mathbf{P} \in \mathbb{R}^{t_p \times C \times p \times p}$。在标准设定中，每段视频采样 16 帧，tubelet 尺寸 $t_p=2$，因此时间分辨率 $N_t=8$；所有帧被缩放至 $224 \times 224$ 像素。

### 运动聚焦令牌选择模块

该模块是 LMFT 的核心创新，由三个子步骤串联构成：

1. **运动强度估计**：对时间上相邻的代表性补丁 $\bar{\mathbf{P}}_{t}^{x,y}$ 与 $\bar{\mathbf{P}}_{t+1}^{x,y}$，计算像素级 L1 运动差异 $\mathbf{D}_t^{x,y} = \left| \bar{\mathbf{P}}_{t+1}^{x,y} - \bar{\mathbf{P}}_t^{x,y} \right|$，并归一化得到运动能量张量 $\mathbf{E}_{\text{motion}}$。这一设计直接量化了每个时空位置的局部运动强度，为后续选择提供信号。

2. **基于可学习阈值的令牌选择**：引入一个可学习的运动聚焦阈值 $\tau$，生成二进制掩码：
   $$\mathbf{M}_{t,x,y} = \begin{cases} 1, & \text{if } (\mathbf{E}_{\text{motion}})_{t,x,y} > \tau \\ 0, & \text{otherwise} \end{cases}$$
   运动能量高于 $\tau$ 的令牌被保留，低于阈值的令牌（通常对应静态或冗余背景区域）被丢弃。这一操作在源域和目标域上对称执行，确保两域均只传递动作相关的运动令牌。

3. **基于强化学习的阈值优化**：由于令牌选择操作不可微，$\tau$ 无法通过标准梯度下降学习。LMFT 将阈值建模为一个逻辑正态分布策略 $\pi_\theta(\tau)$，利用 REINFORCE 策略梯度算法进行优化：
   $$\nabla_\theta \mathcal{I}(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \big[ (R(\tau) - b) \nabla_\theta \log \pi_\theta(\tau) \big]$$
   其中 $b$ 为指数移动平均基线以降低方差，对数概率通过变量变换公式计算：
   $$\log \pi_\theta(\tau) = \log \mathcal{N}(\mathrm{logit}(\tau); \mu, \sigma^2) - \log(\tau) - \log(1-\tau)$$
   奖励函数 $R(\tau)$ 同时考虑分类损失和令牌丢弃率，引导策略在准确率与效率之间取得平衡。

在测试阶段，采用确定性阈值 $\hat{\tau} = \mathbb{E}_{\tau \sim \pi_\theta}[\tau]$，通过 Monte Carlo 采样 $K$ 个标准正态噪声 $\epsilon_k$ 并计算 $\hat{\tau} = \frac{1}{K} \sum_{k=1}^{K} \mathrm{sigmoid}(\mu + \sigma \epsilon_k)$ 来近似期望值。

### ViT 域自适应与联合训练

经 LMFT 筛选后的运动令牌被送入 ViT-B/16 骨干网络 $f_\phi$ 进行动作分类。域自适应通过联合训练实现：

- **源域**：使用真实标签计算交叉熵损失 $\mathcal{L}_s$。
- **目标域**：利用预训练 CLIP（ViT-B/16）为零样本生成伪标签，并通过置信度过滤（阈值 $\gamma_c$）仅保留高置信度样本，计算伪标签交叉熵损失 $\mathcal{L}_t$。

总损失为 $\mathcal{L}_{da} = \mathcal{L}_s + \lambda_t \mathcal{L}_t$，其中 $\lambda_t$ 平衡源域和目标域损失的权重。整个框架端到端训练，运动令牌选择策略与动作识别网络在统一的优化目标下协同学习。

### 数据流总览

```
源域视频 ──→ 令牌化 ──→ 运动强度估计 ──→ 阈值选择(τ) ──→ 运动令牌 ──→ ViT ──→ 分类损失
目标域视频 ──→ 令牌化 ──→ 运动强度估计 ──→ 阈值选择(τ) ──→ 运动令牌 ──→ ViT ──→ 伪标签损失
                                                                              ↑
                                                              CLIP伪标签生成 + 置信度过滤
```

Figure 1 直观展示了上述流程：对于源域和目标域视频，LMFT 首先将帧划分为补丁令牌，计算连续时间令牌间的 L1 距离，并丢弃差异低于可学习阈值 $\tau$ 的令牌（主要对应冗余和静态背景区域），仅将运动丰富、动作相关的令牌送入 ViT 域自适应框架。

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2604_09955/figures/001_Figure_1.jpg]]
*Figure 1: Overview of LMFT. For both source and target videos, LMFT tokenizes frames into patch tokens, computes the L1 distance between consecutive temporal tokens, and discards those with differences below a learnable threshold*



LMFT 的核心由三个紧密耦合的模块构成：运动强度估计、运动聚焦令牌选择、以及基于强化学习的阈值学习策略。它们共同实现了“仅保留动作相关令牌”的目标，从而缓解背景诱导的域偏移并降低计算开销。

### 运动强度估计模块

给定输入视频 $\mathbf{V} \in \mathbb{R}^{T \times C \times H \times W}$，首先将其划分为时空块（tubelets），每个块覆盖 $t_p$ 帧和 $p \times p$ 的空间区域，得到令牌张量 $\mathbf{P}$。为量化每个时空位置的“动作显著性”，该模块计算相邻时间步代表补丁之间的像素级运动差异：

$$
\mathbf{D}_t^{x,y} = \left| \bar{\mathbf{P}}_{t+1}^{x,y} - \bar{\mathbf{P}}_t^{x,y} \right| \tag{1}
$$

其中 $\bar{\mathbf{P}}_t^{x,y}$ 表示在时间索引 $t$、空间位置 $(x, y)$ 处的代表补丁。差异 $\mathbf{D}_t^{x,y}$ 随后被归一化为运动能量张量 $\mathbf{E}_{\text{motion}}$，其每个元素值域为 $[0, 1]$，高值对应动作丰富的区域，低值对应静态或冗余背景。

### 运动聚焦令牌选择模块

基于运动能量 $\mathbf{E}_{\text{motion}}$，该模块通过一个可学习阈值 $\tau$ 生成二值掩码，决定每个令牌的保留或丢弃：

$$
\mathbf{M}_{t,x,y} = \begin{cases} 1, & \text{if } (\mathbf{E}_{\text{motion}})_{t,x,y} > \tau \\ 0, & \text{otherwise} \end{cases} \tag{2}
$$

只有 $\mathbf{M}_{t,x,y} = 1$ 的令牌被送入后续 ViT 骨干网络进行动作识别。这一硬选择机制直接减少了传入自注意力层的令牌数量，从而降低计算复杂度。

### 基于强化学习的阈值学习策略

阈值 $\tau$ 的选取直接影响令牌保留率与识别精度之间的权衡，手动设定难以在跨域场景下泛化。LMFT 将阈值学习建模为一个策略优化问题：策略 $\pi_\theta$ 输出一个逻辑正态分布，通过采样 $\tau \sim \pi_\theta$ 来动态决定丢弃比例。由于令牌选择操作不可微，采用 REINFORCE 策略梯度估计器优化策略参数 $\theta$：

$$
\nabla_\theta \mathcal{I}(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \big[ (R(\tau) - b) \nabla_\theta \log \pi_\theta(\tau) \big] \tag{3}
$$

其中 $R(\tau)$ 为奖励信号，$b$ 是指数移动平均基线以降低梯度方差。为计算采样阈值 $\tau$ 的对数概率，利用变量变换公式将逻辑正态分布映射回概率空间：

$$
\log \pi_\theta(\tau) = \log \mathcal{N}\big(\mathrm{logit}(\tau); \mu, \sigma^2\big) - \log(\tau) - \log(1-\tau) \tag{4}
$$

奖励函数的设计平衡了分类损失与计算效率。源域和目标域的奖励分别定义为：

$$
R_{\mathrm{src}} = -\lambda_{\mathcal{L}} \mathcal{L}_s - (1 - \rho_s), \quad R_{\mathrm{tgt}} = -\lambda_{\mathcal{L}} \mathcal{L}_t - (1 - \rho_t) \tag{7}
$$

其中 $\mathcal{L}_s$、$\mathcal{L}_t$ 分别为源域和目标域的交叉熵损失，$\rho_s$、$\rho_t$ 表示保留令牌的比例。惩罚项 $(1 - \rho)$ 鼓励策略丢弃更多低运动令牌，而 $\lambda_{\mathcal{L}}$ 控制分类精度与令牌压缩之间的相对权重。消融实验表明，$\lambda_{\mathcal{L}} = 10.0$ 在准确率与效率之间取得了最佳平衡（Table 9）。

测试阶段，为消除随机性，使用策略动作分布的期望值作为确定性阈值，通过蒙特卡洛估计得到：

$$
\hat{\tau} = \frac{1}{K} \sum_{k=1}^{K} \mathrm{sigmoid}(\mu + \sigma \epsilon_k), \quad \epsilon_k \sim \mathcal{N}(0,1)
$$

### 设计决策分析

与直接采用 Gumbel-Softmax 近似离散选择的替代方案相比，基于 RL 的阈值学习在准确率和效率上均表现出优势。在 H←W 场景下，RL 方案准确率提升 0.9%（74.2 vs 73.3），训练时间减少约 15%（2784s vs 3275s），最大 GPU 内存占用降低 13%（Table 10）。这表明 RL 策略能够更灵活地在动作识别精度与令牌丢弃率之间进行自适应权衡，而 Gumbel-Softmax 的软近似可能引入额外的计算开销和优化难度。



## 实验与关键发现

### 主实验结果

LMFT 在三个标准 VUDA 基准上均取得最优性能，且提升幅度显著。

**Daily-DA 数据集**（Table 1）：该基准包含 12 个域迁移场景，覆盖不同拍摄视角、背景和光照条件。LMFT 平均 Top-1 准确率达到 64.5%，相比此前最优方法 **UNITE**（Reddy et al., CVPR 2024）的 59.2% 提升 **5.3 个百分点**。这一提升的核心驱动力在于 LMFT 主动丢弃了低运动背景令牌，有效缓解了背景域偏移对动作语义迁移的干扰。

**UCF-HMDB_full 数据集**（Table 2）：在 UCF→HMDB 和 HMDB→UCF 两个经典跨数据集场景下，LMFT 平均准确率 96.4%，超过 UNITE 的 94.6%（+1.8%）。该数据集域间隙相对较小，LMFT 仍能稳定获益，表明运动聚焦令牌化即使在域偏移较温和的场景下也不会误删关键动作信息。

**ActorShift 数据集**（Table 3）：这是最具挑战性的基准，涉及演员身份和场景同时变化的域偏移。LMFT 平均准确率 88.4%，大幅领先 UNITE 的 76.4%（**+12.0%**），甚至超过 Target Only 基线 7.3%。ActorShift 上的突破性表现直接验证了核心洞察：当背景域偏移极为严重时，仅保留运动令牌能从根本上切断背景干扰对动作分类的影响路径。

### 效率分析

LMFT 在实现最优准确率的同时，保持了出色的计算效率。

**训练效率**（Table 4）：与通用令牌压缩方法相比，LMFT 在 Daily-DA 上实现约 **1.4 倍训练加速**，同时准确率最高。具体而言，**ToMe**（Bolya et al., ICLR 2023）通过合并相似令牌减少计算量，但未考虑运动信息，导致动作令牌可能被错误合并；**RLT**（Choudhury et al., NeurIPS 2024）按时间重复性移除令牌，但无法区分静态背景与暂停的动作。LMFT 的运动感知丢弃策略在令牌选择质量上具有本质优势。

**推理效率**（Table 5）：LMFT 在推理吞吐量（clips/s）和 FLOPs 上均优于其他令牌压缩方法，计算成本约为全量令牌方案的 **0.82 倍**。与 VUDA 方法的整体效率对比（Table 6）进一步表明，LMFT 是唯一在准确率-效率帕累托前沿上同时超越其他 VUDA 方法的方案。

### 消融实验

**置信度过滤阈值 γ_c**（Table 7）：CLIP 生成伪标签的质量直接影响域自适应效果。实验表明 γ_c = 0.8 在伪标签保真度和覆盖率之间取得最佳平衡——在 M→H 场景下准确率 74.2%，H→M 场景下 60.0%。阈值过低会引入噪声伪标签，过高则导致可用目标域样本过少，两者均损害性能。

**时间分辨率 N_t**（Table 8）：在 N_t ∈ {2, 4, 6, 8} 范围内，LMFT 始终优于所有基线方法，对少帧场景具有鲁棒性。这表明运动差异计算不依赖密集的时间采样，即使仅 2 帧也能有效识别运动区域。

**奖励系数 λ_L**（Table 9）：λ_L 控制 RL 奖励中分类损失与令牌丢弃率的平衡权重。在 {0.1, 1, 10, 100} 范围内，总体准确率保持稳定，λ_L = 10.0 为最平衡设置。该稳定性表明 RL 阈值学习对超参数不敏感，避免了手动调参的脆弱性。

**RL vs. Gumbel-Softmax**（Table 10）：与直接采用 Gumbel-Softmax 近似离散令牌选择相比，基于 REINFORCE 的 RL 策略在 H←W 场景下准确率提升 0.9%（74.2 vs. 73.3），训练时间减少 15%（2784s vs. 3275s），最大 GPU 内存降低 13%。Gumbel-Softmax 需要在计算图中保留所有令牌的软掩码，而 RL 通过硬阈值直接物理丢弃令牌，从根本上减少了传入 ViT 的令牌数量，因此效率优势明显。

### 定性分析

Figure 2 展示了 LMFT 在四个视频上的可视化结果。每段视频包含三行：原始帧、运动差异热力图、LMFT 处理后保留的令牌区域。可以观察到，LMFT 精确地保留了人体动作相关区域（如摆动的四肢、移动的躯干），同时丢弃了大量静态背景（墙壁、地面、天空）。在背景本身包含运动（如移动的车辆）的场景下，LMFT 是否会将背景令牌错误保留，原文未提供针对性分析，该边界情况需要手动验证。

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2604_09955/figures/009_Figure_2.jpg]]
*Figure 2: Visualization of LMFT on four videos (two left, two right). Each video has three rows: original frames, motion differences, and LMFT processed frames. LMFT selects action-relevant patches, dropping static or low-motion background patches for effective DA*

### 公平性说明

所有 VUDA 方法比较均基于同一 ViT-B/16 骨干网络。ActorShift 上 UNITE 的准确率由作者重新运行其公开代码获得，避免实现差异导致的不公平比较。效率评估在同硬件环境下测量训练时间、推理吞吐量、FLOPs 和 GPU 内存消耗，确保计算开销对比的可靠性。

### 补充图表

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2604_09955/figures/002_Table_1.jpg]]
*Table 1: VUDA results on Daily-DA. Colored rows show our results, and the results in other rows are taken from [16] and [22]*

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2604_09955/figures/003_Table_2.jpg]]
*Table 2: VUDA results on*

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2604_09955/figures/004_Table_3.jpg]]
*Table 3: VUDA results on ActorShift. Colored rows indicate our experimental results. Uncolored baseline results are from [35], while UNITE [22] accuracy is from our run of their public code*

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2604_09955/figures/005_Table_6.jpg]]
*Table 6: Efficiency comparison of VUDA methods*

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2604_09955/figures/006_Table_4.jpg]]
*Table 4: Training efficiency of token reduction methods*

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2604_09955/figures/007_Table_7.jpg]]
*Table 7: Impact of threshold*

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2604_09955/figures/008_Table_5.jpg]]
*Table 5: Inference efficiency of token reduction methods*

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2604_09955/figures/010_Table_10.jpg]]
*Table 10: Gumbel-Softmax vs. RL in LMFT*

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2604_09955/figures/011_Table_8.jpg]]
*Table 8: Impact of different temporal resolutions on VUDA*

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2604_09955/figures/012_Table_9.jpg]]
*Table 9: Effect of varying λL in Eq. 7*



## 定位与知识库关联

### 1. 核心问题定位：视频无监督域自适应中的“全量令牌”瓶颈

本工作针对**视频无监督域自适应**（Video Unsupervised Domain Adaptation, VUDA）任务展开。现有VUDA方法普遍沿用标准视频Vision Transformer（ViT）的令牌化策略，即对视频的所有时空块（共 $N = N_t \times N_x \times N_y$ 个令牌）进行无差别的全量处理。这一策略在VUDA场景下暴露出两个关键瓶颈：

1.  **域偏移加剧**：视频中大量静态或无关的背景令牌携带强烈的域特异性外观信息（如光照、场景纹理），这些令牌参与域自适应过程会干扰动作语义的跨域迁移，导致负迁移。
2.  **计算效率低下**：ViT中自注意力机制的计算复杂度与令牌数量的平方成正比。全量处理大量冗余令牌造成训练和推理的计算开销巨大，限制了VUDA方法在实际应用中的可扩展性。

因此，本工作的核心洞察在于：**仅传递运动丰富的令牌，既能缓解背景诱导的域偏移，又能大幅减少传入ViT的令牌数，从而同时提升域自适应效果和计算效率。**

### 2. 方法谱系：与现有工作的关系定位

LMFT在VUDA和视频令牌压缩两条技术路线的交叉点上做出了贡献。以下从这两个维度定位其与现有工作的关系。

#### 2.1 相对于VUDA方法的定位

现有的VUDA方法主要从域对齐和自训练两个角度解决域偏移问题，但均未触及令牌选择这一根本效率瓶颈。

*   **对抗性域对齐**：早期工作如 **TA³N**（Chen et al., ICCV 2019）通过对抗训练对齐源域和目标域的时序关系特征。这类方法关注特征空间的对齐，但处理的对象仍是全部时空令牌，未考虑令牌本身的冗余性。
*   **时序对比学习**：**CoMix**（Sahoo et al., NeurIPS 2021）引入时序对比学习框架来学习域不变特征，同样继承了全量令牌处理的计算模式。
*   **信息瓶颈与互相关对齐**：**UDAVT**（Da Costa et al., ICPR 2022）将信息瓶颈理论应用于VUDA，并结合互相关矩阵对齐。它试图压缩特征中的域信息，但压缩发生在特征空间，而非输入令牌空间，因此计算开销并未降低。
*   **掩码建模与自训练**：当前最优的VUDA方法 **UNITE**（Reddy et al., CVPR 2024）结合了掩码自编码器和自训练策略，性能显著。然而，UNITE的掩码策略是随机的，目的是构造自监督学习任务，而非有目的地丢弃低运动背景令牌。因此，它仍然处理所有令牌，且随机掩码可能丢弃关键的运动令牌。

**LMFT的独特贡献**在于，它首次在VUDA任务中引入了基于运动显著性的令牌选择机制，将“令牌丢弃”从一个通用的效率手段，转变为一种服务于域自适应的主动策略。与上述方法相比，LMFT的改进是根本性的：它改变了输入ViT的数据流，而非仅仅设计新的损失函数或对齐模块。

#### 2.2 相对于通用令牌压缩方法的定位

在通用视频理解领域，研究者提出了多种令牌压缩方法来加速ViT，但这些方法并非为VUDA设计，忽略了域偏移问题。

*   **令牌合并（Token Merging, ToMe）**：**ToMe**（Bolya et al., ICLR 2023）通过计算令牌间的相似性，将冗余令牌合并。这是一种通用的、不考虑运动语义的压缩方法。在VUDA场景下，它可能错误地合并关键的运动令牌与背景令牌，或保留大量具有域特异性的背景令牌，从而损害域自适应性能。
*   **游程令牌化（Run-Length Tokenization, RLT）**：**RLT**（Choudhury et al., NeurIPS 2024）通过移除时间轴上重复出现的补丁来减少令牌数量。它基于“静态令牌重复出现”的假设，但无法区分“静态但属于动作主体”的令牌（如静止的人）和“静态背景”令牌，可能造成关键信息的丢失。

**LMFT的独特贡献**在于，它通过计算相邻帧间的L1运动差异，显式地建模了“运动显著性”，从而能够区分动作相关令牌和静态背景令牌。此外，LMFT引入了一个**基于强化学习（RL）的可学习阈值 $\tau$**，使其令牌选择策略能够动态适应不同视频和域的特点，以优化动作识别准确率与令牌丢弃率的平衡。这比ToMe和RLT的固定或启发式策略更为灵活和有效。

### 3. 适用边界与局限

尽管LMFT在多个基准上取得了显著效果，但其设计原理也决定了其存在以下适用边界和潜在局限：

1.  **对相机运动的敏感性**：LMFT的核心假设是“低运动区域对应冗余背景”。在相机运动剧烈（如平移、抖动）的场景下，静态背景也会产生高运动差异，可能被错误地识别为动作相关令牌而保留，导致令牌丢弃率下降，效率收益减弱。这是该方法的一个固有风险点，论文中尚未对此进行专门验证。
2.  **对动作类别数量的敏感性**：可学习阈值 $\tau$ 在RL奖励函数中平衡了准确率和令牌丢弃率。当动作类别数量大幅增加时，识别任务难度上升，当前学习的阈值可能不再是最优的，令牌丢弃率可能需要重新调整以适应更复杂的语义空间。
3.  **对伪标签质量的依赖**：LMFT的域自适应训练依赖于CLIP（ViT-B/16）生成的伪标签。在源域和目标域类别不完全一致、或出现新类别的开放集场景下，伪标签的噪声将显著增加，可能削弱自训练的效果。论文未评估该方法在开放集VUDA下的性能。
4.  **任务泛化能力未验证**：LMFT的设计围绕动作识别任务，其“运动聚焦”的归纳偏置是否适用于其他视频理解任务（如视频目标分割、目标跟踪）尚不清楚。在这些任务中，静态背景信息可能同样重要，简单地丢弃低运动令牌可能是有害的。

### 4. 开放问题

基于本工作的贡献与局限，后续研究可以考虑以下几个方向：

1.  **鲁棒的显著性建模**：如何设计对相机运动鲁棒的运动显著性度量？例如，结合光流或全局运动补偿技术，将相机运动与物体运动解耦，以更精确地定位动作相关区域。
2.  **自适应阈值策略的泛化**：可学习阈值 $\tau$ 是否对动作类别数量、域差异程度等因素敏感？能否设计一个元学习或条件化的策略网络，使其能根据输入视频的全局特征自适应地预测最优阈值？
3.  **开放集与类别不一致场景**：在源域和目标域标签空间不完全重叠的开放集或部分集VUDA设定下，如何改进伪标签生成机制，或设计不依赖伪标签的令牌选择策略？
4.  **任务驱动的令牌选择**：能否将LMFT推广到其他视频任务？这可能需要设计任务特定的显著性度量，例如，对于视频分割，显著性可能来源于物体的边界和运动；对于目标跟踪，显著性可能来源于目标的表观特征和运动轨迹。
5.  **超参数敏感度研究**：论文中RL策略的参数 $\mu$ 和 $\log \sigma$ 被设定为固定初始值（0.01和-1.0）。这些超参数在不同数据集和域偏移程度下的敏感度如何，是否具有普适性，尚需更系统的经验研究。



## 原文 PDF

![[paperPDFs/CVPR_2026/Learnable_Motion_Focused_Tokenization_for_Effective_and_Efficient_Video_Unsupervised_Domain_Adaptation.pdf]]
