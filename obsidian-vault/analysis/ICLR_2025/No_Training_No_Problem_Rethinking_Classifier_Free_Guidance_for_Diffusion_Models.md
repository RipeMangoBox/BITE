---
title: "No Training, No Problem: Rethinking Classifier-Free Guidance for Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/No_Training_No_Problem_Rethinking_Classifier_Free_Guidance_for_Diffusion_Models.pdf
aliases:
- ICGITSGT
- NTNPRCFGDM
tags:
- ICLR_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 对于ICG，是条件向量与输入数据的独立性；对于TSG，是时间步骤嵌入的扰动。
primary_logic: 利用独立于输入数据的条件向量，可以使条件模型等效地预测无条件得分，从而在推断时实现CFG而无需额外训练。同时，对时间步骤嵌入进行高斯扰动，可以产生类似CFG的引导信号，提升无条件模型的生成质量。
claims:
- ICG在多个条件扩散模型上取得与CFG相似或更好的FID。
- 使用纯条件模型训练并配合ICG，比标准CFG训练（标签丢弃）具有更快的收敛和更低的FID。
- TSG显著改善了无条件生成和条件生成的FID，且优于SAG和PAG。
- ICG和TSG可以结合，进一步提升生成质量。
---

# No Training, No Problem: Rethinking Classifier-Free Guidance for Diffusion Models

> [!tip] 核心洞察
> 利用独立于输入数据的条件向量，可以使条件模型等效地预测无条件得分，从而在推断时实现CFG而无需额外训练。同时，对时间步骤嵌入进行高斯扰动，可以产生类似CFG的引导信号，提升无条件模型的生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 无需训练：重新思考扩散模型的无分类器引导 |
| 英文题名 | No Training, No Problem: Rethinking Classifier-Free Guidance for Diffusion Models |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://openreview.net/forum?id=b3CzCCCILJ) · [Project](http://probml.github.io/book2) · [arXiv](https://arxiv.org/abs/2112.03111) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Independent Condition Guidance (ICG) 和 Time-step Guidance (TSG) |
| Dataset | Stable Diffusion, DiT-XL/2, EDM2-XS, DiT-XL/2 unconditional |

> [!tip] 效果简介
> - Stable Diffusion (MS COCO 2017) 上，FID 20.05 vs 20.13 (-0.08)。
> - DiT-XL/2 (ImageNet class-conditional) 上，FID 5.50 vs 5.56 (-0.06)。
> - EDM2-XS (ImageNet) 上，FID 3.35 vs 3.36 (-0.01)。

## 概述

扩散模型的无分类器引导（Classifier-Free Guidance, CFG）已成为提升生成质量的关键技术，但其标准实现存在一个根本性瓶颈：需要训练一个单独的无条件模型，或在训练过程中随机丢弃条件信息。这不仅降低了训练效率，还使得CFG天然无法应用于无条件生成模型。

本文提出两种无需额外训练即可实现CFG式引导的推断方法，核心洞察在于：

- **独立条件引导（ICG）**：利用独立于输入数据的条件向量，使条件模型能够等效地预测无条件得分，从而在推断时复现CFG的行为，完全规避了对无条件模型训练的需求。
- **时间步引导（TSG）**：通过对扩散模型的时间步骤嵌入施加高斯扰动，产生类似CFG的引导信号，首次将引导机制扩展到无条件生成模型。

实验表明，ICG在Stable Diffusion和DiT-XL/2等条件模型上取得了与标准CFG相当甚至更优的FID（例如，Stable Diffusion上FID从20.13降至20.05），且使用纯条件模型训练配合ICG在所有检查点均优于标签丢弃的CFG训练。TSG则显著改善了无条件生成的质量——在DiT-XL/2上将FID从48.67大幅降至29.03，并优于SAG和PAG等现有方法。两种方法可进一步结合，获得额外的质量提升。

在方法谱系上，ICG和TSG处于推断时引导技术的交汇点：ICG延续了CFG的条件-无条件混合范式，但将无条件分支的获取方式从“训练时准备”转变为“推断时构造”；TSG则开辟了全新的引导信号来源——时间嵌入扰动，使引导机制不再依赖任何条件信息，从而扩展了CFG类技术的适用范围。

## 背景与动机

扩散模型通过逐步去噪从高斯噪声中生成高质量样本，其核心是学习数据分布的得分函数 $\nabla_{z_t} \log p_t(z_t)$。条件扩散模型进一步引入条件信息 $y$（如类别标签、文本描述），学习条件得分 $\nabla_{z_t} \log p_t(z_t | y)$，以实现可控生成。然而，条件模型直接生成的样本往往在保真度与多样性之间存在权衡，引导（guidance）技术应运而生。

**现有方法缺口**：无分类器引导（Classifier-Free Guidance, CFG）（Ho & Salimans, 2022）是当前最广泛使用的引导方法。它通过混合条件模型和无条件模型的输出来放大条件信号：

$$D_{\text{CFG}}(z_t, t, y) = D(z_t, t, y_{\text{null}}) + w \left( D(z_t, t, y) - D(z_t, t, y_{\text{null}}) \right)$$

其中 $D(z_t, t, y_{\text{null}})$ 是无条件模型的预测。为获得无条件模型，标准CFG需要在训练时以概率 $p$ 将条件替换为空的“null”条件（标签丢弃），这带来了两个关键问题：

1. **训练效率降低**：模型必须同时学习条件生成和无条件生成两个目标，训练资源被分散，收敛速度变慢。
2. **无法适用于无条件模型**：对于从未见过条件信息的纯无条件扩散模型，CFG完全无法使用，因为不存在条件信号可供放大。

此外，一些替代方法如自注意力引导（SAG）（Hong et al., 2022）和扰动注意力引导（PAG）（Ahn et al., 2024）试图在不依赖条件信息的情况下提供引导，但它们通常绑定于特定的网络架构（如注意力层），通用性受限。

**核心瓶颈**：标准CFG需要训练一个单独的无条件模型或在训练中随机丢弃条件，这降低了训练效率且不适用于无条件模型。

**本文动机**：核心洞察在于，如果能从条件模型本身提取出等效的无条件得分，就可以在推断时实现CFG而无需额外训练。具体而言，当条件向量 $\hat{y}$ 与输入数据 $z_t$ 独立时，条件得分近似为无条件得分：

$$\nabla_{z_t} \log p_t(z_t | \hat{y}) \approx \nabla_{z_t} \log p_t(z_t)$$

基于这一原理，本文提出**独立条件引导（Independent Condition Guidance, ICG）**，用独立于 $z_t$ 的随机条件向量（如高斯噪声）替代无条件模型输出，从而在纯条件模型上直接实现CFG等效效果。进一步，本文发现对时间步骤嵌入施加高斯扰动可以产生类似CFG的引导信号，由此提出**时间步引导（Time-step Guidance, TSG）**，将引导能力扩展到无条件模型，且不依赖任何特定网络架构。

## 核心创新

本文的核心创新在于提出了两种全新的推断时引导方法——**独立条件引导 (ICG)** 与**时间步引导 (TSG)**，它们从根本上改变了扩散模型中引导信号的获取方式，完全消除了对额外训练的需求。

### 问题瓶颈：CFG 的训练依赖性

标准无分类器引导 (CFG, Ho & Salimans, 2022) 虽然能显著提升生成质量，但其实现依赖于一个关键前提：必须拥有一个无条件得分估计器。这通常通过两种方式获得：一是训练一个完全独立的无条件模型；二是在条件模型训练过程中以概率 $p$ 随机将条件置为空值，从而让模型同时学会条件与无条件去噪。这两种方式均存在明显缺陷：前者增加了模型参数量和训练成本；后者则降低了训练效率，因为部分迭代被用于学习无条件分布而非条件分布，且该方法完全不适用于无条件生成模型。

### 核心洞察：从条件模型中提取无条件信号

本文的核心洞察在于发现了一种无需训练即可从条件模型本身获取无条件得分的方法。其理论基础是贝叶斯公式对条件得分的分解：
$$\nabla_{z_t} \log p_t(z_t | y) = \nabla_{z_t} \log p_t(z_t) + \nabla_{z_t} \log p_t(y | z_t)$$
当条件向量 $y$ 与当前噪声数据 $z_t$ 统计独立时，$\nabla_{z_t} \log p_t(y | z_t) \approx 0$，此时条件得分自然退化为无条件得分。这一洞察直接催生了 ICG。

### 变更槽位一：无条件得分估计方式

**Baseline**: 训练单独的无条件模型，或在训练中随机丢弃条件标签以让条件模型同时充当无条件模型。

**Proposed (ICG)**: 在推断时，从条件模型中采样两次——一次使用真实条件 $y$，一次使用独立于 $z_t$ 的伪条件 $\hat{y}$——然后用 CFG 式的混合公式得到引导输出：
$$\hat{D}_{\mathrm{ICG}}(z_t, t, y) = D(z_t, t, \hat{y}) + w_{\mathrm{ICG}}(D(z_t, t, y) - D(z_t, t, \hat{y}))$$
其中 $\hat{y}$ 可以是高斯噪声或从条件空间中随机采样的条件向量。由于 $\hat{y}$ 与 $z_t$ 独立，$D(z_t, t, \hat{y})$ 近似于无条件得分估计，从而实现了完全基于条件模型的 CFG 行为。这一方法不仅适用于文本条件、类别条件等标准设置，还可推广至图像条件生成（如 ControlNet），且无需模型在训练时见过空条件。

### 变更槽位二：引导信号来源

**Baseline**: 引导信号依赖于外部条件信息（如类别标签、文本嵌入），无条件模型无法受益于引导。

**Proposed (TSG)**: 利用扩散模型内在的时间步嵌入作为引导信号来源。TSG 对时间步嵌入施加高斯扰动：
$$\hat{t}_{\mathrm{emb}} = t_{\mathrm{emb}} + s t^{\alpha} n, \quad n \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$
然后混合原始时间嵌入和扰动时间嵌入下的模型输出：
$$\hat{D}_{\mathrm{TSG}}(z_t, t, y) = D(z_t, \hat{t}_{\mathrm{emb}}, y) + w_{\mathrm{TSG}}(D(z_t, t_{\mathrm{emb}}, y) - D(z_t, \hat{t}_{\mathrm{emb}}, y))$$
从得分函数的角度分析，TSG 等价于在原始得分上增加了一个与去噪网络时间导数相关的修正项：
$$\nabla_{z_t} \log \hat{p}_t(z_t) = \nabla_{z_t} \log p_t(z_t) + \frac{1 - w_{\mathrm{TSG}}}{\sigma(t)^2} \frac{\partial D_{\theta}(z_t, t)}{\partial t} \Delta t$$
这一修正项在采样早期（$t$ 较大）推动生成远离低密度区域，在采样后期（$t$ 较小）则有助于收敛到高质量样本。由于时间步嵌入是扩散模型的固有组件，TSG 完全不依赖任何外部条件，可直接应用于无条件生成模型，首次将 CFG 式的引导能力扩展到无条件场景。

### 方法的互补性

ICG 和 TSG 作用于扩散模型的不同组件——前者操控条件向量，后者操控时间嵌入——因此二者天然兼容。实验表明，联合使用 ICG 和 TSG 可以进一步提升生成质量，验证了两种引导机制的互补性。

## 整体框架

本文提出两种无需额外训练的引导方法，均可在推理阶段直接应用于预训练扩散模型，无需修改训练目标或模型权重。两种方法共享一个核心思想：通过构造一个“参考输出”来模拟无引导时的预测，然后利用条件输出与参考输出之间的差异形成引导信号，从而提升生成质量。

### 方法总览

整个框架包含两个正交的引导机制，可单独使用或组合使用：

1.  **独立条件引导**：针对条件扩散模型，通过引入一个与输入数据 $z_t$ 独立的随机条件向量 $\hat{y}$，利用条件模型自身近似估计无条件得分，进而在推理时复现分类器无关引导的效果，完全省去训练无条件模型或标签丢弃的环节。
2.  **时间步引导**：针对任意扩散模型（包括无条件模型），通过对时间步嵌入 $t_{\mathrm{emb}}$ 施加高斯扰动，产生一个“扰动版”去噪输出，利用原始输出与扰动输出之差构造引导信号。该方法首次将 CFG 式的质量提升扩展到无条件生成场景。

两种方法的引导公式在结构上高度对称：

- **ICG 引导输出**：
  $$\hat{D}_{\mathrm{ICG}}(z_t, t, y) = D(z_t, t, \hat{y}) + w_{\mathrm{ICG}}(D(z_t, t, y) - D(z_t, t, \hat{y}))$$
  其中 $\hat{y}$ 为独立于 $z_t$ 的条件向量（高斯噪声或随机条件），$w_{\mathrm{ICG}}$ 为引导尺度。

- **TSG 引导输出**：
  $$\hat{D}_{\mathrm{TSG}}(z_t, t, y) = D(z_t, \hat{t}_{\mathrm{emb}}, y) + w_{\mathrm{TSG}}(D(z_t, t_{\mathrm{emb}}, y) - D(z_t, \hat{t}_{\mathrm{emb}}, y))$$
  其中 $\hat{t}_{\mathrm{emb}} = t_{\mathrm{emb}} + s t^{\alpha} n,\ n \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 为扰动后的时间嵌入，$w_{\mathrm{TSG}}$ 为引导尺度。

### 模块关系与输入输出流

下图描述了两种引导方法在采样循环中的插入位置与数据流向：

```
┌─────────────────────────────────────────────────────────┐
│                    采样循环 (t = T → 0)                  │
│                                                         │
│  输入: z_t, t, y (条件, 可选)                            │
│       │                                                 │
│       ▼                                                 │
│  ┌──────────────────────────────┐                       │
│  │     时间步嵌入生成            │                       │
│  │  t_emb = Embed(t)            │                       │
│  └──────────┬───────────────────┘                       │
│             │                                           │
│             ▼                                           │
│  ┌──────────────────────────────┐                       │
│  │      TSG (可选)              │                       │
│  │  t̂_emb = t_emb + s·t^α·n    │                       │
│  │  输出: 原始 + 扰动嵌入        │                       │
│  └──────────┬───────────────────┘                       │
│             │                                           │
│             ▼                                           │
│  ┌──────────────────────────────┐                       │
│  │      模型前向 (×2)           │                       │
│  │                              │                       │
│  │  分支A: D(z_t, t_emb, y)     │  ← 原始条件/时间输出   │
│  │  分支B: D(z_t, t̂_emb, y)     │  ← TSG扰动输出        │
│  │    或: D(z_t, t, ŷ)          │  ← ICG独立条件输出     │
│  └──────────┬───────────────────┘                       │
│             │                                           │
│             ▼                                           │
│  ┌──────────────────────────────┐                       │
│  │      引导信号合成             │                       │
│  │  D̂ = D_ref + w·(D_cond - D_ref)│                    │
│  └──────────┬───────────────────┘                       │
│             │                                           │
│             ▼                                           │
│  输出: 引导后的去噪预测 D̂ → 更新 z_{t-1}                │
└─────────────────────────────────────────────────────────┘
```

**关键模块说明**：

- **独立条件构造**：ICG 的 $\hat{y}$ 可从两个来源获取：① 从与条件向量同尺度的高斯分布中采样；② 从条件空间中随机选取一个条件（如随机类别标签、随机文本嵌入）。两种方式性能相当（FID 5.50 vs 5.55，Table 5）。

- **时间步扰动**：TSG 对时间嵌入施加缩放高斯噪声 $s t^{\alpha} n$，其中 $s$ 控制噪声尺度，$\alpha$ 控制噪声随采样进程的衰减速率。扰动后的嵌入 $\hat{t}_{\mathrm{emb}}$ 使模型产生“过度去噪”或“欠去噪”的输出，两者的差异即构成引导信号（Figure 10）。

- **引导信号合成**：两种方法均采用 CFG 式的线性外推公式，将参考输出作为“基底”，条件输出与参考输出的残差作为“引导方向”，通过引导尺度 $w$ 控制质量-多样性的权衡（Figure 4, Figure 7）。

### 方法间的兼容性

ICG 和 TSG 作用于模型的不同输入维度——ICG 修改条件向量，TSG 修改时间嵌入——因此二者天然正交，可同时施加。实验表明，组合使用可进一步提升生成质量（Table 4），例如在 DiT-XL/2 类条件生成上，单独 ICG 为 FID 5.50，单独 TSG 为 6.39，组合后达到更优的指标。

### 与现有引导方法的定位差异

- 相较于 **CFG**（Ho & Salimans, 2022），ICG 无需训练无条件模型或使用 null 条件丢弃，可直接从纯条件模型中提取无条件得分。
- 相较于 **SAG**（Hong et al., 2022）和 **PAG**（Ahn et al., 2024），TSG 不依赖注意力层的特定结构，对模型架构无任何假设，且取得更优的 FID（Table 8）。
- 两种方法均与 **CADS** 等条件增强方法兼容，可在高引导尺度下提高多样性（Table 7, Figure 9）。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_b3CzCCCILJ/figures/015_Table_7.jpg]]
*Table 7: Effectiveness of CADS on ICG*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_b3CzCCCILJ/figures/016_Figure_9.jpg]]
*Figure 9: Similar to CFG, ICG is compatible with CADS, and CADS can be used to increase the diversity of ICG at higher guidance scales. Samples are generated from the DiT-XL/2 model*

### 计算成本与适用范围

两种方法的共同代价是每步采样需要两次模型前向传播，计算量约为标准采样的两倍，这与 CFG 一致。ICG 适用于任何条件扩散模型，TSG 适用于任何使用时间步嵌入的扩散模型（包括无条件模型）。两种方法均在 Stable Diffusion、DiT、EDM 等多种架构上验证有效。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_b3CzCCCILJ/figures/002_Figure_1.jpg]]
*Figure 1: Comparison between CFG and ICG for (a) Stable Diffusion (Rombach et al., 2022) and (b) DiT-XL/2 (Peebles & Xie, 2022). Both CFG and ICG significantly improve the image quality of the baseline. Also note the similarity between the outputs of CFG and ICG, confirming our theoretical analysis in Section 4*

## 核心模块与公式推导

### 3.1 标准无分类器引导（CFG）的瓶颈

标准CFG（Ho & Salimans, 2022）在推理时通过混合条件模型和无条件模型的输出来提升生成质量。其核心更新步骤为：

$$D_\theta(z_t, t, y_{\mathrm{null}}) + w_{\mathrm{CFG}}(D_\theta(z_t, t, y) - D_\theta(z_t, t, y_{\mathrm{null}}))$$

其中 $D_\theta$ 为去噪器，$z_t$ 为噪声隐变量，$t$ 为时间步，$y$ 为条件，$y_{\mathrm{null}}$ 为空条件，$w_{\mathrm{CFG}}$ 为引导尺度。

**瓶颈**：实现该公式需要训练一个能够处理空条件的模型。标准做法是在训练过程中以概率 $p$ 将条件随机替换为 $\emptyset$，但这带来了两个问题：
1. **训练效率降低**：部分训练迭代被用于无条件目标，而非条件建模本身。
2. **不适用于无条件模型**：对于未使用CFG目标训练的模型（如EDM系列），无法直接应用引导。

### 3.2 独立条件引导（ICG）

**核心洞察**：利用贝叶斯公式，条件得分可分解为无条件得分与分类器得分之和：

$$\nabla_{z_t} \log p_t(z_t | y) = \nabla_{z_t} \log p_t(z_t) + \nabla_{z_t} \log p_t(y | z_t)$$

当使用一个与 $z_t$ **独立**的条件向量 $\hat{y}$ 替代真实条件 $y$ 时，由于 $\hat{y}$ 不携带关于 $z_t$ 的信息，分类器得分项 $\nabla_{z_t} \log p_t(\hat{y} | z_t)$ 趋近于零，从而有：

$$\nabla_{z_t} \log p_t(z_t | \hat{y}) \approx \nabla_{z_t} \log p_t(z_t)$$

这意味着**条件模型对独立条件向量的输出，可以近似无条件得分**。

**ICG引导输出公式**（Algorithm 1）：

$$\hat{D}_{\mathrm{ICG}}(z_t, t, y) = D(z_t, t, \hat{y}) + w_{\mathrm{ICG}}(D(z_t, t, y) - D(z_t, t, \hat{y}))$$

**变量含义**：
- $D(z_t, t, \hat{y})$：条件模型在独立条件 $\hat{y}$ 下的输出，替代CFG中的无条件模型输出。
- $D(z_t, t, y)$：条件模型在真实条件 $y$ 下的输出。
- $w_{\mathrm{ICG}}$：ICG的引导尺度，控制引导强度。

**独立条件 $\hat{y}$ 的构造方式**（Section 4, Implementation details）：
1. **高斯噪声**：从与条件向量 $y$ 尺度匹配的高斯分布中采样。
2. **随机条件**：从条件空间中随机选取一个条件（如随机类别标签、随机文本嵌入）。

两种方式性能相当（FID 5.50 vs 5.55，Table 5），验证了只要 $\hat{y}$ 与 $z_t$ 独立，近似即成立。

### 3.3 时间步引导（TSG）

**核心洞察**：扩散模型的时间步嵌入 $t_{\mathrm{emb}}$ 控制着去噪强度。对其施加扰动，可以产生类似CFG的引导信号，从而**将引导能力扩展到无条件模型**。

**TSG时间嵌入扰动**（Section 5）：

$$\hat{t}_{\mathrm{emb}} = t_{\mathrm{emb}} + s t^{\alpha} n, \quad n \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$

**变量含义**：
- $t_{\mathrm{emb}}$：原始时间步嵌入向量。
- $\hat{t}_{\mathrm{emb}}$：扰动后的时间步嵌入。
- $s$：噪声尺度，控制扰动幅度。
- $\alpha$：指数因子，使扰动幅度随时间步变化。
- $n$：标准高斯噪声。

**TSG引导输出公式**（Algorithm 2）：

$$\hat{D}_{\mathrm{TSG}}(z_t, t, y) = D(z_t, \hat{t}_{\mathrm{emb}}, y) + w_{\mathrm{TSG}}(D(z_t, t_{\mathrm{emb}}, y) - D(z_t, \hat{t}_{\mathrm{emb}}, y))$$

**变量含义**：
- $D(z_t, \hat{t}_{\mathrm{emb}}, y)$：使用扰动时间嵌入的模型输出。
- $D(z_t, t_{\mathrm{emb}}, y)$：使用原始时间嵌入的模型输出。
- $w_{\mathrm{TSG}}$：TSG的引导尺度。

**TSG的得分函数解释**（Section 5, Eq. 9）：通过泰勒展开可推导出TSG修改后的得分函数为：

$$\nabla_{z_t} \log \hat{p}_t(z_t) = \nabla_{z_t} \log p_t(z_t) + \frac{1 - w_{\mathrm{TSG}}}{\sigma(t)^2} \frac{\partial D_{\theta}(z_t, t)}{\partial t} \Delta t$$

该式表明TSG在原始得分函数上添加了一个**时间导数项**，其作用类似于沿采样轨迹施加额外驱动力。直观上（Figure 10）：使用较低时间步的嵌入会导致过度去噪（输出过软），使用较高时间步的嵌入会导致去噪不足（输出含噪），TSG同时利用两个方向的差异来改善输出质量。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_b3CzCCCILJ/figures/017_Figure_10.jpg]]
*Figure 10: Intuition behind TSG: Using lower time steps for guidance causes excessive noise removal (soft outputs), while higher time steps cause insufficient noise removal (noisy images). TSG employs both directions to improve output quality*

### 3.4 模块关系与计算代价

ICG和TSG均可独立使用，也可组合（Table 4验证了两者的兼容性）。两者共享相同的计算特征：每步采样需要**两次模型前向传播**，计算成本约为标准采样的两倍，与标准CFG一致。这是当前方法的主要局限之一。

## 实验与分析

### 主结果：ICG 与 CFG 等价性验证

ICG 的核心主张是：仅使用条件模型本身，即可在推理时复现 CFG 的行为，而无需训练额外的无条件模型。表 1 在多个模型上验证了这一主张。在 Stable Diffusion（MS COCO 2017）上，ICG 取得 FID 20.05，略优于 CFG 的 20.13；在 DiT‑XL/2（ImageNet 类别条件生成）上，ICG 的 FID 为 5.50，对比 CFG 的 5.56；在 Pose‑to‑Image 和 MDM 上，ICG 的 FID 分别从 14.61 降至 13.46、从 0.65 降至 0.47。上述结果表明，ICG 能够在不同条件生成任务中达到与标准 CFG 相当或更优的生成质量。

对于未使用 CFG 目标训练的 EDM 系列模型，表 2 进一步表明：ICG 与使用单独无条件模块进行引导的性能几乎一致（EDM2‑XS: CFG 3.36 vs ICG 3.35; EDM: 两者均为 1.87）。这证明 ICG 不依赖于训练时的标签丢弃策略，可直接应用于任意预训练条件扩散模型。

### 主结果：TSG 对无条件与条件生成的提升

TSG 将 CFG 式的引导信号扩展到无条件模型，其定量结果见表 3。在 DiT‑XL/2 无条件生成上，TSG 将 FID 从 48.67 大幅降至 29.03（Δ = −19.64）；在 Stable Diffusion 无条件生成上，FID 从 69.38 降至 56.65（Δ = −12.73）。对于条件生成，TSG 同样显著改善质量：DiT‑XL/2 类别条件生成的 FID 从 15.49 降至 6.39，Stable Diffusion 文本条件生成的 FID 从 36.63 降至 22.17。这表明 TSG 作为一种无需条件信息的通用引导方法，对多种设置均有效。

### ICG 与 TSG 的兼容性

表 4 展示了两种方法的结合效果。在 DiT‑XL/2 上，单独使用 ICG 的 FID 为 5.50，单独使用 TSG 为 6.39，而 ICG + TSG 联合使用进一步降至 5.24。这表明两者通过不同机制提供互补的引导信号，可以叠加使用以获得更优的生成质量。

### 消融实验

**ICG 独立条件的选择。** 表 5 对比了两种独立条件 $\hat{y}$ 的构造方式：从高斯分布采样噪声向量，或从条件空间中随机选取一个条件。在 DiT‑XL/2 上，高斯噪声的 FID 为 5.50，随机条件为 5.55，两者性能相当。这验证了理论分析的核心要求——只要 $\hat{y}$ 与当前 $z_t$ 独立，即可有效近似无条件得分，而与具体分布形式关系不大。

**纯条件训练 + ICG 对比标签丢弃训练。** 图 3 的训练曲线显示，在 DiT 模型 ImageNet 训练过程中，使用纯条件模型配合 ICG 在所有检查点均优于标准 CFG 训练（标签丢弃）。这表明 ICG 不仅避免了训练时的额外开销，还能带来更快的收敛和更低的最终 FID。

**TSG 超参数消融。** 表 6 系统研究了 TSG 的设计要素：噪声尺度 $s$、指数 $\alpha$ 以及扰动时间嵌入的应用层选择。结果显示，中等程度的扰动可获得最佳 FID，过强或过弱的扰动均会导致性能下降。应用层的选择同样重要，在特定层施加扰动比全层应用更有效。需要注意的是，这些超参数针对不同模型需手动调整，论文未进行穷举搜索，当前设置可能未达全局最优。

**TSG 与 SAG、PAG 的对比。** 表 8 将 TSG 与自注意力引导（**SAG**, Hong et al., 2022）和扰动注意力引导（**PAG**, Ahn et al., 2024）进行比较。TSG 在 FID 上优于这两种方法，且不依赖特定的网络架构假设（如注意力层），适用范围更广。

**TSG 与增加采样步数的对比。** 表 9 显示，TSG 在相同采样步数下显著优于无引导基线，且使用较少步数的 TSG 即可超过更多步数的无引导采样。这证明 TSG 的改善并非简单地等效于增加计算量，而是实质性地改变了采样轨迹。

**ICG 与 CADS 的兼容性。** 表 7 表明 ICG 可与条件退火采样（CADS）结合使用，在高引导尺度下提高生成多样性，缓解 CFG 常见的质量-多样性权衡问题。

### 失败模式与局限

ICG 和 TSG 与 CFG 共享一个根本性局限：每步采样需两次模型前向，计算成本翻倍。此外，ICG 在模型容量极小或独立条件 $\hat{y}$ 远离训练分布时，可能出现分布外误差，导致无条件得分估计失准。TSG 的超参数（$s$、$\alpha$、应用层索引）需针对不同模型手动调整，缺乏自动化选择机制。两种方法目前仅在扩散模型上验证，对其他生成模型（如基于流的模型）的适用性未知。

### 重要图表结论

图 1 定性展示了 Stable Diffusion 和 DiT‑XL/2 上 CFG 与 ICG 的生成对比，两者在视觉质量上高度相似，印证了 ICG 可有效复现 CFG 行为的理论分析。图 6 展示了 TSG 对无条件生成和条件生成的定性改善：在 DiT‑XL/2 类别条件生成和 Stable Diffusion 文本条件生成上，TSG 均显著提升了图像的清晰度和结构一致性。图 10 提供了 TSG 的直观解释——使用较低的时间步嵌入会导致过度去噪（输出模糊），使用较高的时间步嵌入则导致去噪不足（输出含噪），TSG 通过双向利用这一差异来提升输出质量。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_b3CzCCCILJ/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison between CFG and ICG. ICG is able to achieve similar metrics to standard CFG by extracting the unconditional score from the conditional model itself*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_b3CzCCCILJ/figures/005_Figure_3.jpg]]
*Figure 3: Comparison of CFG and ICG during training of a DiT model on ImageNet. Compared to standard CFG with label dropping, using ICG with a purely conditional model achieves better FID across all checkpoints. This indicates that the iterations spent on the CFG objective could be better allocated to training the conditional score, ultimately leading to a better model*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_b3CzCCCILJ/figures/006_Figure_4.jpg]]
*Figure 4: Behavior of ICG as the guidance scale increases. Similar to CFG, ICG trades diversity (lower recall) for quality (higher precision) at higher guidance scales*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_b3CzCCCILJ/figures/009_Table_3.jpg]]
*Table 3: Quantitative comparison between the baseline sampling of the diffusion models and sampling with TSG. TSG significantly boosts quality (lower FID) across various setups*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_b3CzCCCILJ/figures/010_Figure_7.jpg]]
*Figure 7: Behavior of TSG as the guidance scale increases for DiT-XL/2. Similar to CFG, TSG also significantly improves FID by trading diversity (recall) with quality (precision)*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_b3CzCCCILJ/figures/011_Table_4.jpg]]
*Table 4: Compatibility of ICG and TSG*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_b3CzCCCILJ/figures/014_Table_5.jpg]]
*Table 5: Ablation on the choice of independent condition in ICG*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_b3CzCCCILJ/figures/018_Table_8.jpg]]
*Table 8: Comparison between TSG and other guidance methods. TSG achieves better quality compared to SAG and PAG while requiring no specific assumption about the underlying architecture of the diffusion model*

## 方法谱系与知识库定位

### 与基线方法的关系

#### 1. 对CFG的继承与重构

本文提出的**独立条件引导（ICG）**直接继承自**无分类器引导（CFG）**（Ho & Salimans, 2022）的推断框架，但对其核心假设进行了根本性重构。CFG的核心机制是在每个采样步骤中混合条件模型和无条件模型的输出来获得引导信号：

$$D_\theta(z_t, t, y_{\text{null}}) + w_{\text{CFG}}(D_\theta(z_t, t, y) - D_\theta(z_t, t, y_{\text{null}}))$$

这一范式要求训练一个额外的无条件模型，或通过以概率 $p$ 随机丢弃条件标签来联合训练条件/无条件模型。ICG的关键突破在于：**它利用独立于输入数据 $z_t$ 的条件向量 $\hat{y}$，使条件模型等效地预测无条件得分**，即 $\nabla_{z_t} \log p_t(z_t | \hat{y}) \approx \nabla_{z_t} \log p_t(z_t)$。由此，ICG的引导步骤变为：

$$\hat{D}_{\mathrm{ICG}}(z_t, t, y) = D(z_t, t, \hat{y}) + w_{\mathrm{ICG}}(D(z_t, t, y) - D(z_t, t, \hat{y}))$$

这一重构消除了CFG对单独无条件模型或标签丢弃训练的依赖，使得**任何纯条件扩散模型都可以在推断时直接应用CFG式的引导**，无需修改训练目标或架构。

#### 2. 与注意力引导方法的对比

**时间步引导（TSG）** 将引导信号的来源从条件信息转移到时间嵌入，与两类现有方法形成对比：

- **自注意力引导（SAG）**（Hong et al., 2022）：通过掩盖自注意力图来产生引导信号，依赖特定的注意力架构。
- **扰动注意力引导（PAG）**（Ahn et al., 2024）：对注意力图添加扰动实现引导，同样与注意力机制绑定。

TSG的核心操作是对时间步嵌入添加高斯噪声 $\hat{t}_{\mathrm{emb}} = t_{\mathrm{emb}} + s t^{\alpha} n, \; n \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$，然后混合原始和扰动时间嵌入下的模型输出：

$$\hat{D}_{\mathrm{TSG}}(z_t, t, y) = D(z_t, \hat{t}_{\mathrm{emb}}, y) + w_{\mathrm{TSG}}(D(z_t, t_{\mathrm{emb}}, y) - D(z_t, \hat{t}_{\mathrm{emb}}, y))$$

实验证据表明，TSG在FID指标上优于SAG和PAG，且**不依赖特定网络架构**（Table 8），其引导效果源于对采样轨迹的改变（Table 9显示TSG比单纯增加采样步骤更能提升质量），而非对注意力机制的操作。TSG通过泰勒展开可推导出修改后的得分函数包含时间导数项：

$$\nabla_{z_t} \log \hat{p}_t(z_t) = \nabla_{z_t} \log p_t(z_t) + \frac{1 - w_{\mathrm{TSG}}}{\sigma(t)^2} \frac{\partial D_{\theta}(z_t, t)}{\partial t} \Delta t$$

这一形式揭示了TSG本质上在得分函数中引入了时间维度的梯度信息，从而改变了采样动力学。

### 适用边界

#### 有效范围

1. **ICG适用于任何具有明确条件嵌入的扩散模型**，在以下模型上已验证有效：Stable Diffusion（文本条件）、DiT-XL/2（类别条件）、EDM2-XS（类别条件）、Pose-to-Image（姿态条件）、MDM（运动条件），以及ControlNet（图像条件，无文本提示）。关键前提是条件向量与输入数据 $z_t$ 在统计上独立——当该条件满足时，条件得分近似为无条件得分。

2. **TSG适用于所有扩散模型，无论是否有条件输入**。其引导信号仅依赖时间步嵌入的扰动，因此在无条件生成、类别条件生成、文本条件生成等多种设置下均有效（Table 3）。

3. **ICG和TSG可以兼容组合使用**（Table 4），进一步提升生成质量，表明两种引导机制通过不同路径影响采样过程，效果可叠加。

#### 已知局限

1. **计算成本翻倍**：ICG和TSG与CFG一样，每步采样需要两次模型前向传播，这是引导类方法的固有开销。目前尚无内置的加速机制。

2. **超参数敏感性**：TSG的噪声尺度 $s$、指数 $\alpha$ 和应用层索引需要针对不同模型手动调整。论文未进行穷举搜索，当前配置可能未达最优（Table 6消融实验证实这些参数对FID有显著影响）。

3. **分布外风险**：ICG在模型容量很小或独立条件 $\hat{y}$ 远离训练分布时，条件得分对无条件得分的近似精度下降，可能出现分布外误差。这一点的量化边界尚不明确，需要根据具体模型手动验证。

4. **架构通用性未验证**：两种方法主要针对扩散模型设计和验证，对基于流的模型、自回归模型等其他生成范式的适用性未知。

### 开放问题

1. **推断效率**：如何避免每步两次前向？是否可以通过模型蒸馏、缓存策略或单步近似来降低计算成本？

2. **自适应条件分布**：ICG中独立条件 $\hat{y}$ 的分布 $q(\hat{y})$ 目前采用简单的高斯噪声或随机条件。能否根据输入数据 $z_t$ 或采样阶段自适应地选择最优的独立条件分布，以最小化无条件得分估计误差？

3. **跨架构推广**：TSG是否对非扩散架构（如基于流的模型、一致性模型）有效？时间嵌入扰动的引导机制是否具有更广泛的生成模型适用性？

4. **与先进采样器的协同**：结合更先进的采样算法（如DPM-Solver、高阶ODE求解器）是否能进一步提升ICG/TSG的性能或降低计算开销？

5. **最优超参数的自动化**：TSG的 $s$、$\alpha$ 和应用层选择目前依赖手动调参。是否存在理论指导或自动化搜索策略来确定这些超参数？

## 原文 PDF

![[paperPDFs/ICLR_2025/No_Training_No_Problem_Rethinking_Classifier_Free_Guidance_for_Diffusion_Models.pdf]]