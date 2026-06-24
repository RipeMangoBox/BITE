---
title: "TTL: Test-time Textual Learning for OOD Detection with Pretrained Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TTL_Test_time_Textual_Learning_for_OOD_Detection_with_Pretrained_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/figec/TTL"
aliases:
- TTTLT
- TTL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在测试时直接从无标签数据流中动态学习文本模态的 OOD 提示（learnable OOD prompts），使文本语义随测试分布演化。
primary_logic: 通过伪标签引导的 OOD 提示优化捕获 OOD 语义，同时利用 OOD 知识净化策略抑制 ID 边界样本噪声，并借助 OOD 文本知识库实现跨批次稳定的得分校准，从而在不依赖任何外部 OOD 标签的情况下显著提升检测性能。
claims:
- 在 ImageNet-1k 基准上，TTL 的平均 FPR95 降至 12.46%，AUROC 升至 97.29%，均优于所有测试时适应方法。
- 在 CIFAR-100 基准上，TTL 的平均 FPR95 仅为 2.36%，AUROC 达到 99.26%，显著超过次优方法 AdaND。
- 消融实验表明，加入 OOD 知识净化损失 L_OKP 可在两个基准上平均提升 AUROC 1.03%。
- ImageNet-1k OOD 检测基准（iNaturalist, SUN, Places, Texture 平均） 上 FPR95 ↓ = 12.46
---

# TTL: Test-time Textual Learning for OOD Detection with Pretrained Vision-Language Models

> [!tip] 核心洞察
> 通过伪标签引导的 OOD 提示优化捕获 OOD 语义，同时利用 OOD 知识净化策略抑制 ID 边界样本噪声，并借助 OOD 文本知识库实现跨批次稳定的得分校准，从而在不依赖任何外部 OOD 标签的情况下显著提升检测性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | TTL：测试时文本学习用于分布外检测 |
| 英文题名 | TTL: Test-time Textual Learning for OOD Detection with Pretrained Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.15756) · [Code](https://github.com/figec/TTL) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Test-time Textual Learning (TTL) |
| Dataset | ImageNet-1k OOD 检测基准（iNaturalist, SUN, Places, Texture 平均）, ImageNet-1k OOD 检测基准（同上）, CIFAR-100 OOD 检测基准（6 个数据集平均）, CIFAR-100 OOD 检测基准（同上） |

> [!tip] 效果简介
> - ImageNet-1k OOD 检测基准（iNaturalist, SUN, Places, Texture 平均） 上，FPR95 ↓ 12.46 vs 19.22 (AdaNeg) (-6.76)。
> - ImageNet-1k OOD 检测基准（同上） 上，AUROC ↑ 97.29 vs 96.17 (AdaNeg) (+1.12)。
> - CIFAR-100 OOD 检测基准（6 个数据集平均） 上，FPR95 ↓ 2.36 vs 20.95 (AdaND) (-18.59)。

## 概述

**问题瓶颈**：现有基于预训练视觉‑语言模型（VLM）的分布外（OOD）检测方法，其文本语义空间由固定的手工提示或外部 OOD 标签定义，无法表示现实世界中开放且不断演化的 OOD 语义分布，导致检测器对未见分布的适应能力严重不足。

**核心思路**：本文提出 **测试时文本学习（Test‑time Textual Learning, TTL）**，在测试阶段直接从无标签数据流中动态学习文本模态的 OOD 提示（learnable OOD prompts），使文本语义随测试分布持续演化，从而在不依赖任何外部 OOD 标签的前提下显著提升 OOD 检测性能。

**关键机制**：
- 利用基础 OOD 检测器生成的**伪标签**驱动可学习 OOD 提示的在线优化，捕获数据流中涌现的 OOD 语义。
- 引入 **OOD 知识净化（OKP）策略**，通过分离高/低置信度伪 OOD 样本的得分差距，抑制 ID 边界样本带来的伪标签噪声。
- 构建 **OOD 文本知识库（OKB）**，动态存储高质量文本特征，实现跨批次稳定的得分校准，克服逐批次独立适应的不稳定性。

**主要结果**：
- 在 **ImageNet‑1k** OOD 检测基准上，TTL 的平均 FPR95 降至 **12.46%**，AUROC 升至 **97.29%**，均优于所有对比方法（包括使用外部 OOD 标签的 AdaNeg）。
- 在 **CIFAR‑100** 基准上，平均 FPR95 仅为 **2.36%**，AUROC 达到 **99.26%**，显著超过次优方法 AdaND。
- 消融实验证实，OKP 净化损失在两个基准上平均贡献 **+1.03% AUROC**，OKB 更新策略与伪标签均衡损失均对性能有实质增益。

**方法定位**：TTL 属于测试时适应（TTA）方法，但区别于现有工作在固定文本空间内适配视觉特征（如 AdaNeg、OODD），TTL 首创性地在文本侧进行在线语义学习，并与视觉侧形成互补。该方法仅需无标签测试流，资源前提比利用外部 OOD 标签或标注 ID 数据的方法更为严格且公平。

## 背景与动机

### 1. 分布外检测的现实挑战

在开放世界中部署视觉模型时，模型不可避免地会遭遇训练分布之外的样本，即分布外（Out-of-Distribution, OOD）数据。一个可靠的视觉系统不仅需要对分布内（In-Distribution, ID）样本做出准确预测，还必须能够识别并拒绝这些未知的 OOD 输入，以避免静默失败。因此，OOD 检测成为安全关键应用（如自动驾驶、医疗诊断）中的核心需求。

传统的 OOD 检测方法通常依赖固定的手工提示或预定义的 OOD 标签空间。然而，现实世界中的 OOD 语义是开放且持续演化的——固定的文本空间无法覆盖无限多样的未知分布。这一根本性瓶颈导致现有检测器在面对未见过的 OOD 分布时适应能力严重不足。

### 2. 现有方法的局限性

近期，预训练视觉-语言模型（Vision-Language Models, VLMs）如 CLIP 在 OOD 检测中展现出强大的零样本能力。基于 VLM 的方法可大致分为三类：

- **后置方法（Post-hoc methods）**：如 **MCM**，利用预训练 VLM 的文本-图像对齐直接计算 OOD 得分，无需额外训练，但其文本空间完全固定，无法适应测试分布的变化。
- **基于训练的方法（Training-based methods）**：如 **LoCoOp**、**FA**、**MoFE**，通过利用 ID 背景信息或集成多专家混合来增强检测能力，但需要标注的 ID 训练数据，且训练完成后文本空间再次固化。
- **测试时适应方法（Test-time adaptation methods）**：如 **AdaNeg** 和 **OODD**，试图在测试阶段动态调整模型。然而，AdaNeg 依赖外部 OOD 标签来构建负语义，这在真实场景中难以获取；OODD 则仅在视觉侧维护图像特征记忆库，完全忽略了对 OOD 语义的文本侧建模。

这些方法的共同缺陷在于：**它们要么将文本空间视为固定不变的，要么依赖难以获取的外部 OOD 监督信号**。如图 1 所示，现有方法在固定的文本空间中适应视觉特征，当测试样本的语义超出预定义范围时，适应能力便受到根本性限制。

### 3. 核心动机与研究问题

本文的核心洞察在于：**OOD 检测的本质瓶颈不在于视觉特征的适应，而在于文本语义空间能否随测试分布动态演化**。如果能够直接从无标签的测试数据流中学习并累积 OOD 的文本语义知识，检测器便无需依赖任何外部 OOD 标签即可持续适应不断变化的分布。

基于这一动机，本文提出一个关键研究问题：能否在测试时仅利用无标签数据流，通过文本侧的学习与知识累积，实现高效且鲁棒的 OOD 检测？这要求方法同时解决三个子问题：

1. **语义获取**：如何从无标签数据中捕获 OOD 的文本语义？
2. **噪声抑制**：如何应对伪标签中不可避免的噪声，尤其是 ID 边界样本的干扰？
3. **知识累积**：如何跨批次稳定地存储和利用已学到的 OOD 知识？

### 4. 本文贡献

针对上述问题，本文提出 **Test-time Textual Learning (TTL)** 框架，其核心思想是：在测试时通过伪标签引导优化可学习的 OOD 提示（learnable OOD prompts），使文本语义随测试分布共同演化。TTL 包含三个关键设计：

- **可学习 OOD 提示**：为每个 ID 类别引入可学习的 OOD 文本提示，利用伪标签引导的少数类均衡损失 $\mathcal{L}_{\mathrm{OMB}}$ 驱动在线优化，直接从数据流中捕获 OOD 语义。
- **OOD 知识净化策略**：通过 $\mathcal{L}_{\mathrm{OKP}}$ 最大化高置信度与低置信度伪 OOD 样本的得分差距，有效抑制 ID 边界样本引入的噪声。
- **OOD 文本知识库（OKB）**：维护一个动态更新的高质量文本特征库，用于跨批次稳定地校准 OOD 得分。

实验表明，TTL 在不依赖任何外部 OOD 标签的前提下，在 ImageNet-1k 基准上将平均 FPR95 降至 12.46%（较 AdaNeg 降低 6.76%），在 CIFAR-100 基准上更是将平均 FPR95 降至 2.36%（较 AdaND 降低 18.59%），均显著优于现有测试时适应方法。

## 核心创新

TTL 的核心创新在于将 OOD 检测的适应焦点从视觉侧转向文本侧，构建了一个**测试时文本学习（Test-time Textual Learning）**框架。与现有方法在固定文本语义空间内调整视觉特征不同，TTL 直接在测试过程中从无标签数据流中学习可演化的 OOD 文本语义，从而突破手工提示或外部标签对 OOD 语义覆盖的固有限制。这一转变通过三个紧密耦合的机制实现：

### 1. 可学习的 OOD 提示：从数据流中动态捕获 OOD 语义

传统方法依赖固定的手工提示（如 MCM）或预定义的外部 OOD 标签（如 AdaNeg 使用 Neglabel），这些静态语义无法覆盖现实世界中开放且不断演化的 OOD 分布。TTL 的核心改变是为每个 ID 类别引入一组**可学习的 OOD 提示**（learnable OOD prompts），在测试时通过伪标签引导进行在线优化，直接从数据流中捕获 OOD 语义。

具体而言，可学习 OOD 提示初始化时复用与 ID 提示相同的手工模板，以充分利用 CLIP 的预训练语义先验。随后，基础检测器（MCM）为每个测试批次生成伪标签，TTL 通过**OOD 聚焦的少数类均衡损失**（$\mathcal{L}_{\mathrm{OMB}}$）驱动提示学习：

$$\mathcal{L}_{\mathrm{OMB}} = -\frac{1}{\pi_+}\sum_{i:\hat{y}_i=1}\log(1-p(\mathbf{x}_i)) - \frac{1}{\pi_-}\sum_{j:\hat{y}_j=0}\log p(\mathbf{x}_j)$$

该损失通过加权因子 $\pi_+$、$\pi_-$ 平衡 ID 与 OOD 样本的不均，使学习过程聚焦于 OOD 语义的获取，而非被大量 ID 样本主导。

### 2. OOD 知识净化：抑制 ID 边界样本的噪声干扰

仅依赖基础检测器的伪标签存在显著噪声——ID 边界样本（即与 ID 分布接近的困难样本）容易被误标为 OOD，从而污染学习到的 OOD 语义。TTL 提出**OOD 知识净化策略**（OOD Knowledge Purification, OKP），通过最大化高置信度与低置信度伪 OOD 样本之间的得分差距来净化噪声：

$$\mathcal{L}_{\mathrm{OKP}} = -\left(\frac{1}{|S_h|}\sum_{i\in S_h}p(\mathbf{x}_i) - \frac{1}{|S_\ell|}\sum_{j\in S_\ell}p(\mathbf{x}_j)\right)$$

其中 $S_h$ 和 $S_\ell$ 分别为高置信度和低置信度的伪 OOD 样本集合。这一设计迫使模型将真正的 OOD 样本推向更高 OOD 概率，同时抑制 ID 边界样本的虚假 OOD 信号。消融实验验证了该策略的有效性：加入 $\mathcal{L}_{\mathrm{OKP}}$ 后，在 ImageNet-1k 和 CIFAR-100 两个基准上平均 AUROC 提升 **1.03%**。

### 3. OOD 文本知识库：跨批次稳定的得分校准

逐批次独立适应缺乏跨批次记忆，导致检测得分在不同批次间波动。TTL 维护一个**OOD 文本知识库**（OOD Textual Knowledge Bank, OKB），容量固定为 $K$，动态存储最具区分性的 OOD 文本特征。更新策略选择与 ID 文本特征相似度最低的 OOD 提示写入知识库，确保存储的知识具有高判别性。

在推理阶段，最终 OOD 得分由基础检测器得分与 OKB 校准得分融合得到：

$$S_{\mathrm{final}}(\mathbf{x}) = S_{\mathrm{base}}(\mathbf{x}) + \beta \cdot S_{\mathrm{cal}}(\mathbf{x})$$

其中校准得分 $S_{\mathrm{cal}}(\mathbf{x}) = -\max_{j}\cos(\mathbf{z}, \mathbf{t}_j^{ood})$ 衡量图像特征与知识库中 OOD 文本特征的最大负余弦相似度。这一机制使 TTL 能够利用跨批次积累的 OOD 知识进行稳定校准，在 ImageNet-1k 基准上将平均 FPR95 降至 **12.46%**，AUROC 提升至 **97.29%**，均优于所有测试时适应方法。

### 方法谱系与知识库定位

TTL 定位于 **VLM 后置 OOD 检测** 与 **测试时适应** 的交汇点。与现有测试时适应方法形成鲜明对比：
- **AdaNeg** 依赖外部 OOD 标签（Neglabel）提供负语义，TTL 则完全从无标签数据流中学习，资源前提更严格且更公平；
- **OODD** 仅维护视觉记忆库，适应能力受限于固定文本空间，TTL 通过文本侧适应直接扩展语义边界；
- 基于训练的方法（如 **LoCoOp** 利用 ID 背景信息、**FA** 使用 ID 提示作为参考、**MoFE** 集成多专家混合）需要额外训练阶段，而 TTL 完全在测试时运作，部署灵活性更高。

实验表明，TTL 在完全不依赖外部 OOD 标签的条件下，不仅超越了所有测试时适应方法，甚至显著优于多数基于训练的方法——在 ImageNet-1k 基准上，TTL 的 FPR95 比最佳训练方法 MoFE 低 **7.56%**。

## 整体框架

TTL 的核心设计动机源于一个关键瓶颈：现有测试时适应方法（如 **AdaNeg**、**OODD**）要么依赖固定的外部 OOD 标签，要么仅在视觉侧进行适应，其文本语义空间始终是静态的，无法表征现实世界中开放且不断演化的 OOD 分布。TTL 提出的因果调节变量是在测试时直接从无标签数据流中动态学习文本模态的 OOD 提示（learnable OOD prompts），使文本语义随测试分布演化。

### 框架总览

TTL 整体框架由两个阶段构成：**适应阶段（Adaptation）** 与 **校准阶段（Calibration）**，如 Figure 2 所示。两个阶段共用一套可学习的 OOD 文本提示和一个 OOD 文本知识库（OKB），形成闭环的知识累积与利用机制。

![[assets/figures/papers/paper_list_l794_https_arxiv_org_abs_2604_15756/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed TTL framework. (a) Adaptation with TTL: During test time adaptation, pseudo labels produced by a base OOD detector are used to optimize the learnable OOD prompts, allowing the model to gradually acquire OOD textual knowledge. To reduce noise in pseudo labels, an OOD knowledge purification strategy is introduced to distinguish reliable OOD samples from ID boundary samples. The learned OOD textual features are then updated in the OOD textual knowledge bank. (b) Calibration of Prediction: During inference, the base detector’s predictions are further calibrated using the OOD textual knowledge bank*

**适应阶段** 包含三个核心模块：

1. **基础 OOD 检测器（Base OOD Detector）**：以 **MCM** 作为基础检测器，对每个测试批次生成初始 OOD 得分和伪标签。MCM 利用 CLIP 的图像编码器与固定的 ID/OOD 文本提示计算 softmax 概率，作为后续学习的监督信号来源。

2. **OOD 知识学习（OOD Knowledge Learning）**：引入 $N$ 个可学习的 OOD 提示 $\{\mathbf{t}_i^{\text{ood}}\}_{i=1}^N$，这些提示使用与 ID 提示相同的手工模板初始化，以利用 CLIP 的预训练语义先验。对每个测试样本 $\mathbf{x}$，计算其 OOD 概率：
   $$p(\mathbf{x}) = \frac{\sum_{k=1}^N s(\mathbf{x},\mathbf{t}_k^{\mathrm{ood}})}{\sum_{j=1}^N s(\mathbf{x},\mathbf{t}_j^{\mathrm{id}}) + \sum_{j=1}^N s(\mathbf{x},\mathbf{t}_j^{\mathrm{ood}})}$$
   其中 $s(\cdot,\cdot)$ 为图像特征与文本特征的余弦相似度。驱动提示优化的目标是 **OOD 聚焦的少数类均衡损失（$\mathcal{L}_{\mathrm{OMB}}$）**：
   $$\mathcal{L}_{\mathrm{OMB}} = -\frac{1}{\pi_+}\sum_{i:\hat{y}_i=1}\log(1-p(\mathbf{x}_i)) - \frac{1}{\pi_-}\sum_{j:\hat{y}_j=0}\log p(\mathbf{x}_j)$$
   $\pi_+$ 和 $\pi_-$ 分别表示伪标签中 ID 与 OOD 样本的比例，用于平衡类别不均问题。该损失通过最大化伪 OOD 样本与可学习 OOD 提示的语义相似度，驱动文本语义向真实 OOD 分布靠拢。

3. **OOD 知识净化（OOD Knowledge Purification）**：基础检测器的伪标签不可避免地包含噪声，尤其是 ID 边界样本容易被误标为 OOD。TTL 提出 $\mathcal{L}_{\mathrm{OKP}}$ 损失来抑制这类噪声：
   $$\mathcal{L}_{\mathrm{OKP}} = -\left(\frac{1}{|S_h|}\sum_{i\in S_h}p(\mathbf{x}_i) - \frac{1}{|S_\ell|}\sum_{j\in S_\ell}p(\mathbf{x}_j)\right)$$
   其中 $S_h$ 为高置信度伪 OOD 样本集，$S_\ell$ 为低置信度伪 OOD 样本集（可能是 ID 边界样本）。该损失通过最大化两组样本的 OOD 概率差距，迫使模型区分可靠 OOD 样本与噪声样本。最终优化目标为：
   $$\mathcal{L} = \mathcal{L}_{\mathrm{OMB}} + \alpha \cdot \mathcal{L}_{\mathrm{OKP}}$$

**校准阶段** 引入 OOD 文本知识库（OKB）实现跨批次的稳定得分校准：

- **OKB 构建与更新**：OKB 是一个容量为 $K$ 的动态存储库，用于累积高质量 OOD 文本特征。在每批次适应完成后，计算每个可学习 OOD 提示的“潜在 OOD 得分”：
  $$S_{\mathrm{in}}(\mathbf{t}_i^{ood}) = \min_c \left[ - \cos( \mathbf{t}_c^{id}, \mathbf{t}_i^{ood} ) \right]$$
  该得分衡量 OOD 提示与所有 ID 文本特征的最小负余弦相似度——得分越高，表示该提示与 ID 语义的区分度越大。OKB 优先保留潜在 OOD 得分最高的文本特征，确保存储库中的知识最具判别性。

- **得分校准**：对任意测试样本 $\mathbf{x}$，计算其图像特征 $\mathbf{z}$ 与 OKB 中所有 OOD 文本特征的校准得分：
  $$S_{\mathrm{cal}}(\mathbf{x}) = -\max_{j\in\{1,\dots,K\}}\cos(\mathbf{z},\mathbf{t}_j^{ood})$$
  最终 OOD 检测得分由基础检测器得分与校准得分加权融合：
  $$S_{\mathrm{final}}(\mathbf{x}) = S_{\mathrm{base}}(\mathbf{x}) + \beta \cdot S_{\mathrm{cal}}(\mathbf{x})$$
  $\beta$ 为融合系数，用于平衡两个得分的量纲差异。

### 输入输出流

整个 pipeline 的数据流如下：

- **输入**：无标签的在线测试数据流，以批次为单位到达。
- **适应阶段输出**：优化后的可学习 OOD 提示，以及更新后的 OKB。
- **校准阶段输出**：每个测试样本的最终 OOD 得分 $S_{\mathrm{final}}(\mathbf{x})$，通过与阈值 $\lambda$ 比较得到二分类决策（ID/OOD）。阈值 $\lambda$ 通过最小化 ID 得分类内方差自适应确定。

### 与现有方法的关键差异

与现有测试时适应方法相比，TTL 在三个关键维度上进行了系统性改造：

| 维度 | 现有方法（AdaNeg、OODD） | TTL |
|------|--------------------------|-----|
| OOD 语义来源 | 固定手工提示或外部 OOD 标签 | 可学习 OOD 提示，在线优化捕获 |
| 伪标签噪声处理 | 无显式抑制 | $\mathcal{L}_{\mathrm{OKP}}$ 净化策略 |
| 知识累积与校准 | 逐批次独立（或仅图像记忆） | OKB 文本知识库，跨批次稳定校准 |

这种设计使 TTL 能够在不依赖任何外部 OOD 标签的前提下，从无标签数据流中持续提取并累积 OOD 语义知识，并通过校准机制将知识有效注入检测决策。Figure 3 的得分密度分布可视化直观展示了校准前后的效果：校准后的 ID 与 OOD 得分分布的重叠区域显著缩小，验证了文本侧知识累积对检测性能的增益。

![[assets/figures/papers/paper_list_l794_https_arxiv_org_abs_2604_15756/figures/005_Figure_3.jpg]]
*Figure 3: Score density distributions for ID (ImageNet) and OOD (SUN) samples before and after calibration with our TTL, where the MCM scoring function is used as the base detector*

## 核心模块与公式推导

TTL 在测试时通过三个协同模块从无标签数据流中动态学习文本模态的 OOD 语义：**可学习 OOD 提示的伪标签驱动优化**、**OOD 知识净化策略**以及**OOD 文本知识库的跨批次校准**。以下逐一展开其公式化设计与变量含义。

### 3.1 可学习 OOD 提示与 OOD 概率建模

TTL 为每个 ID 类别引入 $N$ 个可学习 OOD 提示 $\{\mathbf{u}_i^{\mathrm{ood}}\}_{i=1}^N$，其初始化采用与 ID 提示相同的手工模板，以充分利用 CLIP 的先验语义。对于测试样本 $\mathbf{x}$，其图像特征 $\mathbf{z}$ 与所有 ID 文本特征 $\{\mathbf{t}_j^{\mathrm{id}}\}$ 及 OOD 文本特征 $\{\mathbf{t}_k^{\mathrm{ood}}\}$ 的余弦相似度构成 OOD 概率：

$$p(\mathbf{x}) = \frac{\sum_{k=1}^N s(\mathbf{x},\mathbf{t}_k^{\mathrm{ood}})}{\sum_{j=1}^N s(\mathbf{x},\mathbf{t}_j^{\mathrm{id}}) + \sum_{k=1}^N s(\mathbf{x},\mathbf{t}_k^{\mathrm{ood}})} \tag{3}$$

其中 $s(\mathbf{x},\mathbf{t}) = \exp(\cos(\mathbf{z},\mathbf{t})/\tau)$ 为温度 $\tau$ 缩放后的指数相似度。该概率直接反映样本落入 OOD 区域的倾向，为后续伪标签生成与提示学习提供连续信号。

### 3.2 伪标签引导的少数类均衡损失

基础 OOD 检测器 **MCM** 为每个测试样本生成初始得分，经自适应阈值 $\lambda$ 二值化后得到伪标签 $\hat{y} \in \{0,1\}$。由于测试批次中 ID 与 OOD 样本比例严重失衡，TTL 提出 **OOD 聚焦的少数类均衡损失**（$\mathcal{L}_{\mathrm{OMB}}$）：

$$\mathcal{L}_{\mathrm{OMB}} = -\frac{1}{\pi_+}\sum_{i:\hat{y}_i=1}\log(1-p(\mathbf{x}_i)) - \frac{1}{\pi_-}\sum_{j:\hat{y}_j=0}\log p(\mathbf{x}_j) \tag{4}$$

其中 $\pi_+$ 和 $\pi_-$ 分别为当前批次中伪标签为 ID 和 OOD 的样本比例。该损失通过逆比例加权，使少数类（通常为 OOD）的梯度贡献不被多数类淹没，从而驱动可学习 OOD 提示向真实 OOD 语义方向收敛。消融实验证实，$\mathcal{L}_{\mathrm{OMB}}$ 相比标准交叉熵在 ImageNet-1k 基准上将 FPR95 从 14.23 降至 12.46，AUROC 从 96.98 提升至 97.29。

### 3.3 OOD 知识净化损失

伪标签不可避免地包含噪声，尤其是位于决策边界的 ID 样本容易被误标为 OOD。TTL 引入 **OOD 知识净化损失**（$\mathcal{L}_{\mathrm{OKP}}$），通过最大化高置信度与低置信度伪 OOD 样本的得分差距来抑制此类噪声：

$$\mathcal{L}_{\mathrm{OKP}} = -\left(\frac{1}{|S_h|}\sum_{i\in S_h}p(\mathbf{x}_i) - \frac{1}{|S_\ell|}\sum_{j\in S_\ell}p(\mathbf{x}_j)\right) \tag{5}$$

其中 $S_h$ 为 OOD 概率 $p(\mathbf{x})$ 最高的前 $k$ 个伪 OOD 样本（高置信度集），$S_\ell$ 为 OOD 概率最低的后 $k$ 个伪 OOD 样本（低置信度集，通常对应 ID 边界样本）。该损失驱动力度集中于拉开两组样本的得分差距，使边界 ID 样本的 OOD 概率进一步降低，从而净化 OOD 提示接收的梯度信号。总优化目标为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{OMB}} + \alpha \cdot \mathcal{L}_{\mathrm{OKP}} \tag{6}$$

其中 $\alpha$ 为平衡系数。消融实验表明，加入 $\mathcal{L}_{\mathrm{OKP}}$ 可在 ImageNet-1k 和 CIFAR-100 两个基准上平均提升 AUROC 1.03%。

### 3.4 OOD 文本知识库与得分校准

为克服逐批次独立适应导致的知识碎片化，TTL 维护一个容量为 $K$ 的 **OOD 文本知识库**（OKB），存储跨批次累积的高质量 OOD 文本特征。知识库的更新策略基于 **潜在 OOD 得分**：

$$S_{\mathrm{in}}(\mathbf{t}_i^{\mathrm{ood}}) = \min_c \left[-\cos(\mathbf{t}_c^{\mathrm{id}}, \mathbf{t}_i^{\mathrm{ood}})\right] \tag{7}$$

该得分衡量 OOD 文本特征与所有 ID 文本特征的最小负余弦相似度——得分越高，表示该提示与 ID 语义的区分度越强。每批次优化后，选取 $S_{\mathrm{in}}$ 最高的 OOD 提示特征更新知识库，确保存储的始终是最具判别力的 OOD 语义表征。

在推理阶段，OKB 为每个测试样本计算校准得分：

$$S_{\mathrm{cal}}(\mathbf{x}) = -\max_{j\in\{1,\dots,K\}}\cos(\mathbf{z}, \mathbf{t}_j^{\mathrm{ood}}) \tag{8}$$

即图像特征 $\mathbf{z}$ 与知识库中所有 OOD 文本特征的最大余弦相似度的负值。该得分与基础检测器得分融合得到最终 OOD 分数：

$$S_{\mathrm{final}}(\mathbf{x}) = S_{\mathrm{base}}(\mathbf{x}) + \beta \cdot S_{\mathrm{cal}}(\mathbf{x}) \tag{9}$$

其中 $\beta$ 为融合系数，用于平衡基础得分与校准得分的量纲。Figure 3 的密度分布可视化表明，经 OKB 校准后 ID 与 OOD 样本的得分分布分离度显著增大，验证了跨批次文本知识累积对检测稳定性的关键作用。

## 实验与分析

### 核心实验设置

TTL 在 ImageNet-1k 和 CIFAR-100 两个标准 OOD 检测基准上评估，均使用 CLIP ViT‑B/16 作为视觉编码器。基础 OOD 检测器采用 **MCM**，OOD 文本知识库（OKB）容量固定为 2048，与 **OODD** 保持一致以保证内存层面的公平对比。所有测试时适应方法均不访问任何外部 OOD 标签或标注的 ID 训练数据。

### 主实验结果

**ImageNet-1k 基准。** Table 1 报告了在 iNaturalist、SUN、Places、Texture 四个 OOD 数据集上的平均性能。TTL 取得 **FPR95 12.46%、AUROC 97.29%**，显著优于所有对比方法：
- 相比最优测试时适应方法 **AdaNeg**（FPR95 19.22%、AUROC 96.17%），FPR95 降低 6.76 个百分点，AUROC 提升 1.12 个百分点；
- 相比最优基于训练的方法 **MoFE**，FPR95 降低 7.56 个百分点；
- 在 iNaturalist 上，TTL 达到 FPR95 0.42%、AUROC 99.87%，几乎完全分离 ID 与 OOD 样本。

**CIFAR-100 基准。** Table 2 展示了在六个 OOD 数据集上的平均结果。TTL 取得 **FPR95 2.36%、AUROC 99.26%**，相比次优方法 **AdaND**（FPR95 20.95%、AUROC 92.50%）有大幅度提升，FPR95 降低 18.59 个百分点，AUROC 提升 6.76 个百分点。在 Places365 上 AUROC 提升达 19.9%。

### 消融实验

**关键组件贡献。** Table 3 的消融实验表明，三个核心组件对性能均有正向贡献：
- 仅使用伪标签引导的 $\mathcal{L}_{\mathrm{OMB}}$ 损失（无 OKP 与 OKB）已能取得可观的性能提升；
- 加入 OOD 知识净化目标 $\mathcal{L}_{\mathrm{OKP}}$ 后，在两个基准上平均 AUROC 提升 **+1.03%**，验证了抑制 ID 边界样本噪声的有效性；
- 进一步引入 OKB 进行跨批次得分校准，使 FPR95 从 14.23% 进一步降至 12.46%。

**OKB 更新策略。** Table 4 对比了多种 OKB 更新策略。结果表明，选取与 ID 文本特征相似度最低的 OOD 提示作为更新对象（即最大化 OOD 语义的区分性），在两个基准上均取得最优性能，验证了“保留最具辨别力的 OOD 知识”这一设计原则。

**损失函数设计。** Table 11 显示，伪标签引导的 $\mathcal{L}_{\mathrm{OMB}}$ 损失（FPR95 12.46%、AUROC 97.29%）一致优于标准交叉熵损失（FPR95 14.23%、AUROC 96.98%），证明了对 ID/OOD 类别不平衡进行显式建模的必要性。

**OOD 提示学习策略。** Table 5 对比了 Prefix 调优与本文的 OOD 提示学习方法，TTL 的提示优化策略在两个基准上均明显占优，表明直接从测试数据流中学习 OOD 语义比调整前缀编码更有效。

### 校准效果可视化

Figure 3 展示了在 ImageNet（ID）与 SUN（OOD）上，使用 TTL 校准前后的得分密度分布。校准前，ID 与 OOD 样本的 MCM 得分存在显著重叠；校准后，两者的分布明显分离，重叠区域大幅缩小。这直观地说明了 OKB 跨批次校准机制能够有效利用累积的文本知识扩大 ID/OOD 得分差距。

### 与不同基础检测器的兼容性

Figure 4 报告了 TTL 与多种基础 OOD 检测器（MCM、Energy、Max-Logit 等）集成后的性能。TTL 在所有基础检测器上均带来一致的性能提升，表明其作为通用校准模块的灵活性。但当基础检测器产生的伪标签信号接近随机噪声时（如 MCM‑Entropy），TTL 的性能提升几乎消失——这是方法的一个关键失败模式：**净化策略无法从极弱信号中提取有效结构信息**。

![[assets/figures/papers/paper_list_l794_https_arxiv_org_abs_2604_15756/figures/009_Figure_4.jpg]]
*Figure 4: Performance when integrated with different detectors*

### 视觉知识库与文本知识库的对比

Table 6 对比了仅视觉知识库（类似 OODD）、仅文本知识库（TTL）以及两者融合的效果。结果表明：
- 纯文本知识库（OKB）在两个基准上均优于纯视觉知识库，验证了文本模态在捕获 OOD 语义方面的优势；
- 两者融合后性能进一步提升，表明视觉与文本知识存在互补性。

![[assets/figures/papers/paper_list_l794_https_arxiv_org_abs_2604_15756/figures/013_Table_6.jpg]]
*Table 6: Comparison between visual-only, textual-only, and both knowledge banks on the ImageNet-1k benchmark*

### 校准策略消融

Table 9 对比了多种校准策略，包括基于最大相似度、平均相似度等变体。TTL 采用的负最大余弦相似度校准得分在两个基准上均取得最优结果，验证了“以最相似 OOD 提示作为校准信号”的设计合理性。

### 计算与存储开销

Table 7 报告了 TTL 与代表性方法的存储和运行时间对比。TTL 的额外内存占用主要来自 OKB（2048 个文本特征向量），训练时间与 **OODD** 相当，单张图像推理时间与基础 MCM 检测器相比仅略有增加。所有实验在单张 NVIDIA 3090 GPU 上完成。

![[assets/figures/papers/paper_list_l794_https_arxiv_org_abs_2604_15756/figures/012_Table_7.jpg]]
*Table 7: Comparison of the storage and runtime usage. “Storage” indicates the extra memory occupation, “Training” denotes the training time, and “Testing” denotes per-image inference time. Experiments are conducted with a single NVIDIA 3090 GPU*

### 超参数敏感性

Figure 5 展示了超参数 α（OKP 损失权重）和 β（校准融合系数）在 ImageNet-1k 基准上的敏感性分析。两个超参数在较宽范围内（α ∈ [0.1, 1.0]，β ∈ [0.1, 1.5]）均能保持稳定且优于 **AdaNeg** 的性能，表明方法对超参数选择不敏感。

![[assets/figures/papers/paper_list_l794_https_arxiv_org_abs_2604_15756/figures/010_Figure_5.jpg]]
*Figure 5: Hyper-parameters sensitivity studies on ImageNet-1k benchmark. Dashed lines represent the performance of AdaNeg*

### 补充图表

![[assets/figures/papers/paper_list_l794_https_arxiv_org_abs_2604_15756/figures/003_Table_1.jpg]]
*Table 1: Performance comparison on ImageNet-1k OOD detection benchmark*

![[assets/figures/papers/paper_list_l794_https_arxiv_org_abs_2604_15756/figures/004_Table_2.jpg]]
*Table 2: Performance comparison on the CIFAR-100 OOD benchmark. F and A denote FPR95 and AUROC, respectively*

![[assets/figures/papers/paper_list_l794_https_arxiv_org_abs_2604_15756/figures/007_Table_3.jpg]]
*Table 3: Ablation study on the key components*

![[assets/figures/papers/paper_list_l794_https_arxiv_org_abs_2604_15756/figures/006_Table_4.jpg]]
*Table 4: Comparison of OKB update strategies*

![[assets/figures/papers/paper_list_l794_https_arxiv_org_abs_2604_15756/figures/008_Table_5.jpg]]
*Table 5: Comparison of OOD prompt learning strategies. For Prefix*

![[assets/figures/papers/paper_list_l794_https_arxiv_org_abs_2604_15756/figures/017_Table_11.jpg]]
*Table 11: Ablation study of the LOMB*

## 方法谱系与知识库定位

### 1. 与现有 VLM‑OOD 方法的关系

TTL 处于 **测试时适应（Test‑Time Adaptation, TTA）** 与 **预训练视觉‑语言模型（VLM）OOD 检测** 的交叉点。根据其与各类基线的关系，可将其定位为 **不依赖外部 OOD 标签的纯文本侧在线适应方法**。

**与后置 VLM 方法的关系**：TTL 以 **MCM** 作为基础 OOD 检测器，继承了其基于 CLIP 文本‑图像相似度比值的得分机制。但 MCM 的文本空间由固定的 ID 类名和单一手工 OOD 提示（如“a photo of something”）构成，无法表示开放世界中不断演化的 OOD 语义。TTL 通过引入可学习的 OOD 提示并在测试时在线优化，将固定的文本空间扩展为动态适应流式数据的语义空间——这是对后置方法的根本性升级。

**与基于训练的方法的关系**：**LoCoOp**、**FA**、**MoFE** 等方法在训练阶段利用 ID 背景信息或集成多专家混合来提升 OOD 检测能力，但它们需要标注的 ID 训练数据，且训练完成后文本空间即被冻结。TTL 在测试时不访问任何 ID 训练数据，仅从无标签数据流中学习 OOD 文本语义，资源前提更严格。在 ImageNet‑1k 基准上，TTL 的 FPR95 比最优训练方法 **MoFE** 低 7.56 个百分点（12.46% vs. 20.02%），表明测试时文本适应可以超越固定训练策略的泛化瓶颈。

**与测试时适应方法的关系**：现有 TTA 方法分为两类——利用外部 OOD 标签的方法（如 **AdaNeg**）和仅用视觉记忆库的方法（如 **OODD**）。AdaNeg 依赖预定义的 OOD 词汇（如 Neglabel）来引导适应，TTL 则完全从数据流中自主学习 OOD 语义，不引入任何外部 OOD 标签。OODD 仅在视觉侧维护图像特征队列，其文本空间保持固定；TTL 在文本侧维护 OOD 文本知识库（OKB），实现了跨批次的文本语义累积与得分校准。在 CIFAR‑100 基准上，TTL 的平均 FPR95 仅为 2.36%，远低于次优方法 AdaND 的 20.95%，差距达 18.59 个百分点——这一量级差异暗示文本侧适应可能比视觉侧适应更有效地捕获 OOD 分布的语义结构。

### 2. 方法适用边界

**对基础检测器伪标签质量的依赖**：TTL 的 OOD 知识学习（L_OMB）和净化（L_OKP）均以基础检测器产生的伪标签为驱动信号。当基础检测器接近随机猜测时（如使用 MCM‑Entropy 作为基础得分函数），净化策略无法从极弱信号中提取有效结构信息，TTL 的性能提升几乎消失。这意味着 TTL 适用于基础检测器已具备一定区分能力的场景，而非从零开始构建 OOD 检测器。

**OKB 容量与流式场景的张力**：当前 OKB 容量固定为 2048（参照 OODD 的设定），在标准基准上运行良好。但在无限流式场景中，固定容量可能面临知识遗忘与代表性不足的挑战——如何在不显著增加内存开销的前提下实现增量式知识累积，仍是开放问题。

**超参数的手动设定**：TTL 引入了融合权重 α（控制 L_OKP 的相对强度）和 β（控制校准得分的贡献），虽然实验表明性能对这两个参数不敏感，但仍需根据具体基准手动设定，尚未实现完全无超参数的即插即用。

### 3. 局限与开放问题

**局限 1：对伪标签信号质量的硬依赖**。当基础检测器产生的伪标签信号接近随机噪声时，TTL 的性能增益几乎消失。这一失效模式源于 L_OKP 的设计假设——高置信度伪 OOD 样本与低置信度样本之间存在可分离的得分差距。当基础检测器无法产生有意义的得分分布时，该假设不再成立。

**局限 2：文本侧与视觉侧适应的融合缺失**。TTL 仅适应文本模态，而 OODD 仅适应视觉模态。尽管两者都使用记忆库机制，但目前尚未有工作将文本侧的知识累积与视觉侧的特征队列有效融合。多模态互补性——文本语义的强泛化能力与视觉特征的细粒度判别能力——可能带来进一步的性能提升，这是直接可操作的后续方向。

**开放问题 1：更低开销的知识累积机制**。当前 OKB 需要存储 K 个完整文本特征向量，在边缘设备或超大规模类别场景中可能构成瓶颈。能否通过参数化生成模型（如轻量级 OOD 文本编码器）或稀疏记忆机制来降低存储开销，同时保持校准性能？

**开放问题 2：TTL 与闭集/开集识别的统一**。TTL 学习到的 OOD 文本语义是否可以作为开集识别中“拒绝类”的表示？将测试时文本学习从 OOD 检测扩展到更一般的开放世界识别，可能是一个有前景的延伸方向。

**开放问题 3：跨模态适应的理论理解**。为什么文本侧适应（TTL）在 CIFAR‑100 基准上比视觉侧适应（OODD）带来更大幅度的性能提升（FPR95 差距 18.59 个百分点）？这是否源于文本空间的高维语义流形更适合捕获 OOD 分布的结构，还是仅仅因为 CLIP 文本编码器的预训练质量更高？目前缺乏理论层面的解释。

## 原文 PDF

![[paperPDFs/CVPR_2026/TTL_Test_time_Textual_Learning_for_OOD_Detection_with_Pretrained_Vision_Language_Models.pdf]]
