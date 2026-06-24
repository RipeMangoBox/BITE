---
title: "PGA: Prior-free Generative Attack for Practical No-box Scenario"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PGA_Prior_free_Generative_Attack_for_Practical_No_box_Scenario.pdf
project_link: null
code_link: null
aliases:
- PPFGA
- PGA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过课程式微鲁棒优化 (Curriculum-Guided Micro-Robust Optimization, CMRO) 逐步训练替代模型，使模型在稳定收敛后逐渐适应鲁棒目标，学习到更丰富和鲁棒的特征表示。同时，采用区域感知一致性扰动学习 (Region-Aware Consistent Perturbation Learning, RCPL)，在生成...
primary_logic: 在自监督学习中，通过课程式引入微鲁棒分支，可以缓解有限数据下的特征退化，使替代模型学习到与标准预训练模型相似的激活分布；而将图像划分为多个区域并施加区域级特征相似度损失和跨区域Gram矩阵一致性，能够鼓励对抗扰动从依赖局部特征的模式转向模型无关的全局结构，从而显著提升跨模型、跨域和跨任务的可迁移性。
claims:
- 同时应用CMRO和RCPL后，ImageNet上对CNN的平均攻击成功率(AVGc)从54.18%提升至71.39%，对ViT/MLP的平均成功率(AVGv)从32.95%提升至47.50%，两者贡献互补。
- 替代模型的特征分布与标准预训练模型更接近，Wasserstein距离更小，说明CMRO有效缓解了特征坍缩。
- 生成器输出的对抗样本在中间层具有更低的余弦相似度和更大的扰动幅度，联合分布分析表明其攻击效果更优。
- ImageNet cross-model (CNNs) 上 AVGc (%) = 71.39
---

# PGA: Prior-free Generative Attack for Practical No-box Scenario

> [!tip] 核心洞察
> 在自监督学习中，通过课程式引入微鲁棒分支，可以缓解有限数据下的特征退化，使替代模型学习到与标准预训练模型相似的激活分布；而将图像划分为多个区域并施加区域级特征相似度损失和跨区域Gram矩阵一致性，能够鼓励对抗扰动从依赖局部特征的模式转向模型无关的全局结构，从而显著提升跨模型、跨域和跨任务的可迁移性。

| 字段 | 内容 |
|------|------|
| 中文题名 | PGA：面向实际无盒场景的先验无关生成式攻击 |
| 英文题名 | PGA: Prior-free Generative Attack for Practical No-box Scenario |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Peng_PGA_Prior-free_Generative_Attack_for_Practical_No-box_Scenario_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PGA (Prior-free Generative Attack) |
| Dataset | ImageNet cross-model, Cross-domain coarse-grained, Cross-domain fine-grained, Cross-task object detection |

> [!tip] 效果简介
> - ImageNet cross-model (CNNs) 上，AVGc (%) 71.39 vs 56.41 (GAPF) (+14.98)。
> - ImageNet cross-model (ViTs/MLPs) 上，AVGv (%) 47.50 vs 33.08 (FACL) (+14.42)。
> - Cross-domain coarse-grained (CIFAR-10) 上，ASR (%) 33.10 vs 15.91 (CDA) (+17.19)。

## 概述

**核心问题：** 在Practical No-box Scenario (PNS)下，攻击者仅能获取少量无标签图像（如4,000张），缺乏大规模标注数据和预训练替代模型。现有生成式攻击严重依赖这些先验信息，导致替代模型训练困难、生成器产生的扰动碎片化且空间覆盖率低，对抗样本的可迁移性和生成速度均受到严重制约。

**核心洞察：** 本文提出**PGA (Prior-free Generative Attack)**，是首个面向PNS的生成式攻击框架。其核心思路包含两个互补的创新：
- **课程式微鲁棒优化 (CMRO)**：通过逐步引入微鲁棒分支，在有限数据下缓解自监督学习的特征坍缩，使替代模型学习到与标准预训练模型接近的特征分布。
- **区域感知一致性扰动学习 (RCPL)**：通过区域级特征分离与跨区域Gram矩阵一致性正则化，引导生成器产生细粒度、空间连贯的扰动，从而提升跨模型、跨域和跨任务的可迁移性。

**主要结果：** 在仅使用4,000张无标签图像的PNS设定下，PGA在ImageNet跨模型攻击中，对CNN的平均攻击成功率(AVGc)达到**71.39%**，较最佳基线GAPF提升14.98个百分点；对ViT/MLP的平均攻击成功率(AVGv)达到**47.50%**，较FACL提升14.42个百分点。在跨域（CIFAR-10、CUB等7个数据集）、跨任务（目标检测与实例分割）以及多种防御机制下，PGA均以显著优势超越现有方法，同时保持最高的推理速度。

## 背景与动机

深度神经网络在图像分类、目标检测等任务中取得了显著成功，但其固有的脆弱性——极易受到对抗样本攻击——已成为实际部署中的重大安全隐患。在攻击者视角下，对抗攻击通常被建模为三种场景：白盒攻击（完全知晓模型结构与参数）、黑盒攻击（可查询模型输出）以及无盒攻击（No-box Scenario）。其中，无盒场景最贴近现实，攻击者无法访问目标模型，只能依靠本地训练的替代模型生成对抗样本，并将其迁移至未知的目标模型。

然而，现有无盒攻击方法普遍依赖两个强先验假设：**大规模标注数据集**和**预训练替代模型**。在实际应用中，攻击者往往仅能获取极少量无标签图像（例如4,000张），既缺乏类别标注，也无法获得与目标域匹配的预训练模型。这一更严苛的设定被称为**Practical No-box Scenario (PNS)**。

### 现有方法的根本瓶颈

在PNS设定下，现有攻击方法面临双重困境：

**替代模型训练退化。** 传统无盒攻击依赖监督学习或迁移学习训练替代模型，但在PNS中标注数据不可得，只能诉诸自监督学习。然而，经典自监督方法（如SimSiam）在有限数据下极易产生**特征空间坍缩**——模型学习到的表示多样性不足、判别能力退化，导致替代模型与标准预训练模型的特征分布差异巨大。这直接削弱了基于该替代模型生成的对抗样本的可迁移性。

**生成器扰动碎片化。** 现有生成式攻击（如**BIA** (Zhang et al., ICLR 2022)、**CDA** (Naseer et al., NeurIPS 2019)）在训练生成器时仅依赖全局特征相似度损失，缺乏对扰动空间结构的显式约束。在替代模型表示能力本就受限的情况下，生成器倾向于产生**碎片化、空间覆盖率低**的局部扰动，这些扰动过度拟合替代模型的局部特征模式，难以泛化至结构迥异的目标模型（尤其是ViT/MLP等非CNN架构）。

上述两个问题形成恶性循环：退化的替代模型无法提供有效的学习信号，而碎片化的扰动又进一步限制了对抗样本的跨模型移动性。实验证据表明，在PNS设定下，现有最优生成式基线**GAPF** (Salzmann et al., NeurIPS 2021) 在CNN上的平均攻击成功率仅为56.41%，而针对ViT/MLP的最优基线**FACL** (Yang et al., AAAI 2024) 仅为33.08%，远未达到实用水平。

### 核心动机与研究思路

本文的核心洞察在于：**PNS下对抗攻击的瓶颈并非不可突破，关键在于如何在有限无标签数据下，同时提升替代模型的表示质量和生成扰动的空间结构性。**

具体而言，本文从两个维度切入：

1. **替代模型侧**：能否设计一种训练策略，使自监督替代模型在有限数据下学习到与大规模预训练模型相似的丰富特征表示，从而为生成器提供更高质量的攻击信号？

2. **生成器侧**：能否引入显式的空间结构约束，引导生成器产生细粒度、空间连贯的扰动，使其摆脱对替代模型局部特征的过度依赖，转而捕捉模型无关的全局结构模式？

基于上述动机，本文提出**PGA（Prior-free Generative Attack）**，通过**课程式微鲁棒优化（CMRO）** 和**区域感知一致性扰动学习（RCPL）** 分别解决替代模型退化和扰动碎片化问题，首次在PNS设定下实现了高效且高可迁移性的生成式攻击。

## 核心创新

PGA 的核心创新在于，针对 Practical No-box Scenario (PNS) 中“有限无标签数据 + 无预训练替代模型”的双重困境，将攻击问题分解为两个相互解耦但协同增强的阶段，并分别为每个阶段设计了全新的训练目标。

### 瓶颈与因果调控

在 PNS 设定下，攻击者仅能获取约 4,000 张无标签图像。这导致了两个连锁瓶颈：

1. **替代模型的特征退化**：传统自监督学习（如 SimSiam）在有限数据下容易发生特征空间坍缩，学到的表示缺乏判别性和多样性，无法为后续生成器提供有效的监督信号。
2. **生成扰动的碎片化**：由于缺乏强监督和多样数据分布，生成器产生的对抗扰动倾向于依赖局部、碎片化的模式，空间覆盖率低，限制了跨模型迁移性。

PGA 通过两个 **changed slots** 精准调控上述因果链：

| 模块 | Baseline 做法 | PGA 做法 | 调控机制 |
|------|-------------|---------|---------|
| 替代模型训练目标 | 仅使用干净多视图对比损失 $\mathcal{L}_{\mathrm{cle}}^{S}$ | 预热 $T$ 个 epoch 后引入微鲁棒分支 $\mathcal{L}_{\mathrm{rob}}^{S}$，课程调度 $\tau$ 从 0 线性增至 $\tau_{\max}$，联合损失 $\mathcal{L}_{\mathrm{tot}}^{S} = (1-\lambda_t)\mathcal{L}_{\mathrm{cle}}^{S} + \lambda_t\mathcal{L}_{\mathrm{rob}}^{S}$，$\lambda_t=0.5$ | 先稳定收敛再逐步适应鲁棒目标，缓解特征坍缩 |
| 生成器训练目标 | 仅使用全局特征相似度损失 $\mathcal{L}_{\mathrm{ori}}^{G}$ | 联合优化全局相似度 $\mathcal{L}_{\mathrm{ori}}^{G}$、区域特征相似度 $\mathcal{L}_{\mathrm{reg}}^{G}$（$K$ 个区域）和跨区域一致性损失 $\mathcal{L}_{\mathrm{cro}}^{G}$（Gram 矩阵 Frobenius 距离），总损失 $\mathcal{L}_{\mathrm{tot}}^{G} = \mathcal{L}_{\mathrm{ori}}^{G} + \alpha\mathcal{L}_{\mathrm{reg}}^{G} + \gamma\mathcal{L}_{\mathrm{cro}}^{G}$，$\alpha=\gamma=1.0$ | 引导生成器产生细粒度、空间连贯的扰动 |

### 课程式微鲁棒优化 (CMRO)

CMRO 的核心洞察是：在有限数据下，**直接引入强鲁棒目标会导致模型发散，而“先稳定、后鲁棒”的课程策略可以逐步扩展特征空间**。

具体而言，替代模型在前 $T$ 个 epoch 仅通过干净多视图对比损失 $\mathcal{L}_{\mathrm{cle}}^{S}$ 学习基础表示。预热完成后，模型同时优化干净视图对和微鲁棒扰动视图对的对齐：

$$\mathcal{L}_{\mathrm{tot}}^{S} = (1 - \lambda_t) \mathcal{L}_{\mathrm{cle}}^{S} + \lambda_t \mathcal{L}_{\mathrm{rob}}^{S}, \quad \lambda_t = \begin{cases} 0, & t < T \\ 0.5, & t \ge T \end{cases}$$

其中微鲁棒扰动强度 $\tau$ 从 0 线性增加到 $\tau_{\max}$，确保模型在收敛后逐步适应更具挑战性的判别任务。消融实验表明，$\tau_{\max}=0.01$ 且 $T=200$ 时攻击成功率最优（Figure 6）。

**效果证据**：Figure 4 显示，经 CMRO 训练的替代模型，其中间层特征分布与标准预训练模型更接近，Wasserstein 距离更小，直接验证了 CMRO 有效缓解了有限数据下的特征退化。

### 区域感知一致性扰动学习 (RCPL)

RCPL 的核心洞察是：**将图像划分为多个区域并施加区域级特征相似度损失和跨区域 Gram 矩阵一致性，可以鼓励对抗扰动从依赖局部特征的模式转向模型无关的全局结构**。

生成器训练时，图像被划分为 $K$ 个非重叠区域，分别计算每个区域的特征相似度：

$$\mathcal{L}_{\mathrm{reg}}^{G} = \frac{1}{K} \sum_{k=1}^{K} \mathrm{sim}\big(f_s^j(\mathbf{x}_k^{\mathrm{adv}}), f_s^j(\mathbf{x}_k)\big)$$

同时，通过最小化不同区域 Gram 矩阵之间的 Frobenius 距离来保持扰动空间统计的一致性：

$$\mathcal{L}_{\mathrm{cro}}^{G} = \frac{2}{K(K-1)} \sum_{k' < k''} \|\mathbf{Gram}_{k'} - \mathbf{Gram}_{k''}\|_F^2$$

**效果证据**：Figure 5 显示，PGA 生成的对抗样本在中间层具有更低的余弦相似度和更大的扰动幅度，联合分布表明其攻击效果显著优于 BIA。消融实验中，区域数 $K=4$ 时迁移性最佳，进一步增大到 $K=9$ 反而导致性能衰减（Table 5）。

### 两阶段协同增益

Table 4 的消融实验直接量化了 CMRO 和 RCPL 的协同效应：同时应用两者后，ImageNet 上对 CNN 的平均攻击成功率 (AVGc) 从 54.18% 提升至 71.39%，对 ViT/MLP 的平均成功率 (AVGv) 从 32.95% 提升至 47.50%。两者贡献互补，单独移除任一组件的性能损失均超过 14 个百分点。

## 整体框架

PGA 的整体设计遵循两阶段流水线：**替代模型学习阶段（Surrogate Learning Stage）** 与**生成器训练阶段（Generator Training Stage）**，二者串行衔接，共同解决 Practical No-box Scenario 下先验信息匮乏的核心瓶颈。

### 阶段一：替代模型学习 —— 课程式微鲁棒优化（CMRO）

在仅拥有少量无标签图像（如 4,000 张）的条件下，替代模型需要从零开始学习具有判别力和迁移性的特征表示。传统自监督学习（如 SimSiam）在此场景下极易发生特征空间坍缩，导致替代模型与标准预训练模型的行为偏差过大，后续生成的对抗样本可迁移性差。

CMRO 的核心设计是**课程式引入微鲁棒目标**。具体而言：

1. **预热阶段**（前 $T$ 个 epoch）：替代模型仅使用干净多视图对比损失 $\mathcal{L}_{\mathrm{cle}}^{S}$ 进行训练，对齐同一图像的不同增强视图，确保基础表示稳定收敛。
2. **微鲁棒激活阶段**（$t \ge T$ 后）：引入微鲁棒对齐损失 $\mathcal{L}_{\mathrm{rob}}^{S}$，该损失要求模型在受到微小扰动（由当前生成器或简单噪声构造）的视图对上同样保持表示一致性。此时总损失切换为均衡组合：

$$\mathcal{L}_{\mathrm{tot}}^{S} = (1 - \lambda_t) \mathcal{L}_{\mathrm{cle}}^{S} + \lambda_t \mathcal{L}_{\mathrm{rob}}^{S}, \quad \lambda_t = 0.5$$

这一课程调度使模型在稳定收敛后逐步适应鲁棒目标，避免训练初期因扰动过大导致的不稳定。消融实验表明，微鲁棒强度 $\tau_{\max}=0.01$、启动 epoch $T=200$ 时攻击成功率最优（Figure 6）。

**输入**：少量无标签图像及其多视图增强对。  
**输出**：一个特征分布与标准预训练模型高度接近的替代模型（Figure 4 验证了其 Wasserstein 距离更小）。

### 阶段二：生成器训练 —— 区域感知一致性扰动学习（RCPL）

替代模型固定后，训练生成器 $G$ 以产生 $\ell_{\infty}$ 约束（$\epsilon=16$）的对抗扰动。RCPL 的关键创新在于**从全局特征相似度驱动升级为区域级细粒度监督**。

生成器总损失由三项构成：

$$\mathcal{L}_{\mathrm{tot}}^{G} = \mathcal{L}_{\mathrm{ori}}^{G} + \alpha \mathcal{L}_{\mathrm{reg}}^{G} + \gamma \mathcal{L}_{\mathrm{cro}}^{G}, \quad \alpha=\gamma=1.0$$

- **$\mathcal{L}_{\mathrm{ori}}^{G}$**：全局特征余弦相似度损失，最小化对抗样本与原图在替代模型中间层的特征相似度，驱动扰动产生模型层面的偏离。
- **$\mathcal{L}_{\mathrm{reg}}^{G}$**：将图像划分为 $K$ 个非重叠区域，分别在每个区域上计算特征相似度损失并取均值，促使扰动在局部区域也具备攻击性。消融表明 $K=4$ 时迁移性最佳（Table 5）。
- **$\mathcal{L}_{\mathrm{cro}}^{G}$**：跨区域一致性损失，计算所有区域对之间 Gram 矩阵的 Frobenius 距离，强制不同区域的扰动在二阶统计上保持一致，从而引导生成器产生空间连贯的全局结构扰动，而非碎片化的局部噪声。

**输入**：干净图像与原图；替代模型作为固定特征提取器。  
**输出**：生成器 $G$，可对任意输入图像实时生成 $\ell_{\infty}$ 约束的对抗样本 $\mathbf{x}^{\mathrm{adv}}$。

### 两阶段协同效应

CMRO 为生成器提供了更接近标准模型的、特征坍缩程度更低的替代模型，使 $\mathcal{L}_{\mathrm{ori}}^{G}$ 和 $\mathcal{L}_{\mathrm{reg}}^{G}$ 的梯度信号更具迁移价值；RCPL 则通过区域级监督弥补了有限数据下生成器缺乏多样分布引导的缺陷。消融实验（Table 4）证实，同时启用 CMRO 和 RCPL 时，AVGc 从 54.18% 跃升至 71.39%，AVGv 从 32.95% 提升至 47.50%，二者贡献互补且叠加效果显著。

### 补充图表

![[assets/figures/papers/paper_list_l910_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_PGA_Prior_free_Ge/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our Prior-free Generative Attack (PGA). For Surrogate Learning, we train the micro-robust surrogate from scratch via a curriculum of increasing difficulty. The surrogate first learns by aligning clean multi-view pairs (P) via*

## 核心模块与公式推导

PGA 面向 Practical No-box Scenario (PNS) 设计，攻击者仅能获取少量无标签图像（如 4,000 张），缺乏大规模标注数据与预训练替代模型。现有生成式攻击在此设定下严重退化：自监督学习在有限数据下易发生特征空间坍缩，生成器因缺乏强监督而产生碎片化、空间覆盖率低的扰动。PGA 通过两个阶段联合解决这一瓶颈：**替代模型学习阶段**采用课程式微鲁棒优化（CMRO）训练具有丰富表示的替代模型；**生成器训练阶段**采用区域感知一致性扰动学习（RCPL）引导生成空间连贯的细粒度扰动。整体框架见 Figure 3。

### 替代模型学习阶段：课程式微鲁棒优化（CMRO）

替代模型 $f_s$ 基于 SimSiam 架构，包含编码器、投影头 $g$ 和预测器 $q$。对输入图像 $x$ 的两个增强视图 $x^{(v)}$ 和 $x^{(u)}$，分别编码得到投影表示 $z$ 和预测表示 $p$：

$$z^{(v)} = g(f_s(x^{(v)})), \quad p^{(v)} = q(z^{(v)})$$

两视图之间的余弦相似度定义为：

$$\mathrm{sim}(\mathbf{a}, \mathbf{b}) = \frac{\mathbf{a}^{\top}\mathbf{b}}{\|\mathbf{a}\|_2 \|\mathbf{b}\|_2}$$

干净多视图对的对比损失 $\mathcal{L}_{\mathrm{cle}}^{S}$ 最小化正样本对之间的负余弦相似度：

$$\mathcal{L}_{\mathrm{cle}}^{S} = \frac{1}{|\mathcal{P}|} \sum_{(v,u) \in \mathcal{P}} \ell_{\mathrm{sim}}(v, u)$$

其中 $\ell_{\mathrm{sim}}(v,u) = -\mathrm{sim}(p^{(v)}, z^{(u)})$ 为对称化的相似度损失，$\mathcal{P}$ 为干净多视图对集合。

**核心创新在于微鲁棒分支的课程式引入。** 在预热 $T$ 个 epoch 后，对每个视图施加微扰动（强度 $\tau$ 从 0 线性增加到 $\tau_{\max}$），构造扰动视图对集合 $\widetilde{\mathcal{P}}$，并引入微鲁棒对齐损失：

$$\mathcal{L}_{\mathrm{rob}}^{S} = \frac{1}{|\widetilde{\mathcal{P}}|} \sum_{(v,u) \in \widetilde{\mathcal{P}}} \ell_{\mathrm{sim}}(v, u)$$

替代模型总损失采用课程式调度：

$$\mathcal{L}_{\mathrm{tot}}^{S} = (1 - \lambda_t) \mathcal{L}_{\mathrm{cle}}^{S} + \lambda_t \mathcal{L}_{\mathrm{rob}}^{S}, \quad \lambda_t = \begin{cases} 0, & t < T \\ 0.5, & t \ge T \end{cases}$$

**设计动机**：在有限数据下，直接引入强鲁棒目标会破坏自监督学习的特征多样性，导致表示坍缩。CMRO 通过预热阶段先让模型学习稳定的干净表示，再逐步引入微鲁棒分支（$\lambda_t = 0.5$ 均衡两目标），使模型在收敛后逐渐适应鲁棒任务，学习到与标准预训练模型更接近的特征分布。Figure 4 的可视化验证了这一效果：本文替代模型的中间层特征分布更接近标准预训练模型，Wasserstein 距离更小。Figure 2 的梯度显著性图也显示，CMRO 训练的替代模型产生了更丰富、更具判别性的特征表示。

### 生成器训练阶段：区域感知一致性扰动学习（RCPL）

生成器 $G$ 以干净图像 $x$ 为输入，输出 $\ell_{\infty}$ 约束的对抗扰动，对抗样本生成为：

$$\mathbf{x}^{\mathrm{adv}} = \mathrm{Proj}_{[0,1]}\big(\mathbf{x} + \mathrm{Clip}_{[-\epsilon,\epsilon]}(G(\mathbf{x}) - \mathbf{x})\big)$$

其中 $\epsilon = 16$ 为扰动预算，$\mathrm{Clip}$ 和 $\mathrm{Proj}$ 分别约束扰动幅度和像素值范围。

**全局特征相似度损失** $\mathcal{L}_{\mathrm{ori}}^{G}$ 最小化替代模型在全图级别的特征余弦相似度，驱动生成器产生能欺骗替代模型的对抗样本：

$$\mathcal{L}_{\mathrm{ori}}^{G} = \mathrm{sim}\big(f_s^{j}(\mathbf{x}^{\mathrm{adv}}), f_s^{j}(\mathbf{x})\big)$$

其中 $f_s^{j}$ 表示替代模型第 $j$ 层的中间特征。

**区域特征相似度损失** $\mathcal{L}_{\mathrm{reg}}^{G}$ 将图像划分为 $K$ 个非重叠区域，在每个区域上独立计算特征相似度，鼓励生成器产生细粒度扰动：

$$\mathcal{L}_{\mathrm{reg}}^{G} = \frac{1}{K} \sum_{k=1}^{K} \mathrm{sim}\big(f_s^{j}(\mathbf{x}_k^{\mathrm{adv}}), f_s^{j}(\mathbf{x}_k)\big)$$

**跨区域一致性损失** $\mathcal{L}_{\mathrm{cro}}^{G}$ 通过最小化不同区域 Gram 矩阵之间的 Frobenius 距离，保持扰动在空间统计上的连贯性，防止区域间扰动模式割裂：

$$\mathcal{L}_{\mathrm{cro}}^{G} = \frac{2}{K(K-1)} \sum_{k' < k''} \|\mathbf{Gram}_{k'} - \mathbf{Gram}_{k''}\|_F^2$$

其中 $\mathbf{Gram}_k$ 为区域 $k$ 特征的 Gram 矩阵，编码了该区域内通道间的相关性结构。

**生成器总损失**联合优化三个目标：

$$\mathcal{L}_{\mathrm{tot}}^{G} = \mathcal{L}_{\mathrm{ori}}^{G} + \alpha \mathcal{L}_{\mathrm{reg}}^{G} + \gamma \mathcal{L}_{\mathrm{cro}}^{G}$$

其中 $\alpha = \gamma = 1.0$。

**设计动机**：仅使用全局相似度损失（如 BIA）训练的生成器倾向于学习依赖局部纹理的脆弱扰动模式，跨模型可迁移性差。RCPL 通过区域级监督迫使生成器关注多个局部区域的独立特征偏移，而跨区域 Gram 一致性正则化则约束这些区域偏移共享相似的统计结构，引导扰动从依赖局部特征的模式转向模型无关的全局结构。Figure 5 的联合分布分析证实，PGA 生成的对抗样本在中间层具有更低的余弦相似度和更大的扰动幅度，表明其对受害模型特征的偏离程度更大，攻击效果更优。

### 两阶段协同机制

CMRO 和 RCPL 分别作用于替代模型训练和生成器训练阶段，二者互补：CMRO 为生成器提供了更高质量的特征空间作为攻击目标，RCPL 则充分利用该特征空间产生更具迁移性的扰动。消融实验（Table 4）表明，单独使用 CMRO 或 RCPL 均能带来显著增益，二者联合使用时 AVGc 从 54.18% 提升至 71.39%，AVGv 从 32.95% 提升至 47.50%，验证了互补性。

### 补充图表

![[assets/figures/papers/paper_list_l910_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_PGA_Prior_free_Ge/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of gradient saliency maps for the surrogates trained by vanilla SimSiam [5] and our method, the latter producing more diverse and discriminative feature representations*

![[assets/figures/papers/paper_list_l910_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_PGA_Prior_free_Ge/figures/004_Figure_4.jpg]]
*Figure 4: Comparison of feature distributions at the intermediate layer between the standard pre-trained model and different surrogates. The mean activation of each channel is visualized using kernel density estimation (KDE). Our method exhibits a distribution closer to the standard model, with a smaller Wasserstein distance, indicating better representation stability and transferability*

![[assets/figures/papers/paper_list_l910_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_PGA_Prior_free_Ge/figures/005_Figure_5.jpg]]
*Figure 5: Visualization of the joint distribution of cosine similarity GAPF and perturbation magnitude at the intermediate layer of the victim model for BIA [61] and our method. Lower similarity and larger magnitude indicate greater deviation of adversarial examples from clean images, corresponding to better attack performance*

## 实验与分析

### 一、实验设置与公平性说明

所有实验均在Practical No-box Scenario (PNS)设定下进行：攻击者仅能获取4,000张无标签图像，无任何预训练模型或标注数据可用。PGA与所有对比方法共享相同的生成器架构，扰动预算统一设为 $L_\infty$ 范数约束 $\epsilon = 16$（除特别说明外），像素值归一化至 $[0,1]$ 区间。对比基线包括PNS迭代攻击方法——**PNAA** (Li et al., NeurIPS 2020)、**ETF** (Sun et al., NeurIPS 2022)、**CDTA** (Li et al., AAAI 2023)、**AGS** (Wang et al., AAAI 2024)，以及适配至PNS场景的生成式攻击方法——**CDA** (Naseer et al., NeurIPS 2019)、**GAPF** (Salzmann et al., NeurIPS 2021)、**BIA** (Zhang et al., ICLR 2022)、**FACL** (Yang et al., AAAI 2024)。所有基线均在相同条件下重新实现，确保公平比较。

### 二、跨模型攻击主结果

Table 1展示了ImageNet域上14个模型的跨模型攻击成功率（ASR），涵盖CNN（ResNet系列、VGG系列、DenseNet、Inception-v3等）、ViT（ViT-B/16、DeiT-B、Swin-B等）和MLP（Mixer-B/16）架构。PGA在CNN平均攻击成功率AVGc上达到 **71.39%**，相较于最强生成式基线GAPF的56.41%提升 **+14.98个百分点**；在ViT/MLP平均成功率AVGv上达到 **47.50%**，相较于FACL的33.08%提升 **+14.42个百分点**。值得注意的是，PGA在VGG-16上取得79.33%的单模型最高成功率，在ResNet-101上亦达到49.48%，展现了跨架构的稳定迁移能力。

Figure 1进一步揭示了PGA在攻击成功率与推理速度上的双重优势：相比于迭代式PNS方法，PGA作为生成式方法仅需单次前向传播即可生成对抗样本，推理速度提升数个数量级，同时攻击成功率大幅领先。这一结果直接回应了PNS场景的核心瓶颈——在信息极度匮乏的条件下，生成式攻击不仅能工作，而且能显著超越迭代方法。

### 三、跨域与跨任务泛化

**跨域攻击。** Table 2报告了7个不同域数据集上的跨域攻击结果，包括粗粒度数据集（CIFAR-10、CIFAR-100、SVHN等）和细粒度数据集（CUB-200-2011、Stanford Cars等）。PGA在CIFAR-10上取得33.10%的ASR，较CDA的15.91%提升 **+17.19个百分点**；在CIFAR-100上达到93.29%；在细粒度CUB上取得66.34%，较BIA+RN的54.07%提升 **+12.27个百分点**。粗粒度平均ASR为46.83%，在所有域上均一致超越基线。这表明RCPL产生的细粒度、空间连贯扰动具备域无关的迁移特性。

**跨任务攻击。** Table 3展示了目标检测与实例分割任务的跨任务攻击结果。PGA在Faster R-CNN上取得 **17.60% AP**，在所有基线上取得大幅领先（最佳基线约13-15% AP）。这一结果验证了PGA生成的对抗扰动不仅能在分类任务间迁移，还能有效攻击结构差异显著的检测与分割模型，进一步证明了扰动中全局结构信息的模型无关性。

### 四、消融实验

**方法论组件消融。** Table 4系统验证了CMRO和RCPL各自的贡献。以BIA为基准（ID i，AVGc=54.18%，AVGv=32.95%），单独引入CMRO（ID ii）使AVGc提升至64.55%（+10.37%），AVGv提升至42.30%（+9.35%）；单独引入RCPL（ID iii）使AVGc提升至65.54%（+11.36%），AVGv提升至41.57%（+8.62%）。两者联合（ID iv）达到AVGc=71.39%、AVGv=47.50%，表明CMRO与RCPL贡献互补且叠加有效。

**微鲁棒强度与时机。** Figure 6热力图展示了微鲁棒强度 $\tau_{max}$ 与启动epoch $T$ 对攻击性能的影响。最优配置为 $\tau_{max}=0.01$、$T=200$，此时AVGc和AVGv均达到峰值。过大的 $\tau_{max}$ 或过早引入鲁棒分支会导致性能下降，这印证了课程式调度对稳定特征学习的必要性——在有限数据下，过强的鲁棒约束会加剧特征坍缩。

**区域数量。** Table 5研究了区域数 $K$ 对攻击成功率的影响。$K=4$ 时取得最佳可迁移性，进一步增大至 $K=9$ 导致性能衰减。这表明适度的区域划分能够引导生成器关注局部细粒度结构，而过度的划分可能破坏扰动的空间连贯性，削弱跨模型迁移能力。

### 五、鲁棒性验证

**严格扰动约束。** Table 6报告了 $\epsilon=10$ 更严格约束下的跨模型攻击结果。PGA在所有模型上仍保持最优或次优性能，证明了方法在不同扰动预算下的鲁棒性。

**防御机制对抗。** Table 7评估了PGA面对多种防御机制的表现，包括对抗训练、随机平滑、JPEG压缩等。PGA在防御机制下的平均攻击成功率AVGd达到 **72.16%**，较BIA+DA的56.80%提升 **+15.36个百分点**，验证了CMRO训练的替代模型所学习的鲁棒特征表示能够泛化至防御场景。

**图像质量与攻击性权衡。** Table 8综合对比了PSNR、SSIM与ASR。PGA在保持较高图像质量（PSNR≈27.5dB, SSIM≈0.85）的同时取得最优攻击性能。当扰动预算略微收紧至 $\epsilon=15$ 时，PSNR进一步提升至28.1dB，而攻击成功率仅轻微下降，展现出良好的感知自然性与攻击性平衡。

### 六、特征空间分析

Figure 4通过核密度估计（KDE）可视化了标准预训练模型、普通SimSiam替代模型与PGA替代模型在中间层的特征分布。PGA替代模型的通道平均激活分布与标准预训练模型高度接近，Wasserstein距离显著更小，而普通SimSiam替代模型则出现明显的分布偏移和峰度坍缩。这直接证明了CMRO有效缓解了有限数据下自监督学习的特征退化问题，使替代模型学习到更丰富、更具判别力的特征表示。

Figure 5展示了BIA与PGA在受害者模型中间层的余弦相似度与扰动幅度的联合分布。PGA生成的对抗样本具有更低的特征余弦相似度和更大的扰动幅度，表明其对干净样本的偏离程度更大，对应更强的攻击效果。这一可视化从特征空间角度解释了RCPL的细粒度扰动如何转化为实际的攻击性能增益。

### 补充图表

![[assets/figures/papers/paper_list_l910_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_PGA_Prior_free_Ge/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of our PGA and existing PNS attacks on ImageNet in terms of average attack success rates and relative inference speeds. AVGc and AVGv denote the average attack success rates on CNNs and on ViTs/MLPs, respectively (see Tab. 1)*

![[assets/figures/papers/paper_list_l910_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_PGA_Prior_free_Ge/figures/006_Table_1.jpg]]
*Table 1: Results in ASR (%) under cross-model attacks. The evaluation includes fourteen models from CNN, ViT, and MLP architectures on the ImageNet domain. The perturbation budget is*

![[assets/figures/papers/paper_list_l910_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_PGA_Prior_free_Ge/figures/007_Table_2.jpg]]
*Table 2: Results in ASR (%) under cross-domain attacks. A total of seven different domains are considered, including both coarsegrained and fine-grained datasets. The perturbation budget is set to*

![[assets/figures/papers/paper_list_l910_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_PGA_Prior_free_Ge/figures/008_Table_4.jpg]]
*Table 4: Ablation studies on methodology. CMRO and RCPL are applied in the surrogate and generator training stages, respectively. ID (i) corresponds to BIA [61] trained using the surrogate from [5]. Both*

![[assets/figures/papers/paper_list_l910_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_PGA_Prior_free_Ge/figures/009_Table_3.jpg]]
*Table 3: Results in AP (%)*

![[assets/figures/papers/paper_list_l910_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_PGA_Prior_free_Ge/figures/010_Figure_6.jpg]]
*Figure 6: Ablation studies on the micro-robustness strength and timing. The heatmaps illustrate the performance variations under different strengths (x-axis) and training epochs (y-axis). The strength*

![[assets/figures/papers/paper_list_l910_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_PGA_Prior_free_Ge/figures/011_Table_5.jpg]]
*Table 5: Ablation studies on the number of regions K. Both*

![[assets/figures/papers/paper_list_l910_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_PGA_Prior_free_Ge/figures/013_Table_7.jpg]]
*Table 7: Results in ASR (%) under different defense mechanisms. All experiments are conducted on the ImageNet dataset with the same settings as in Tab. 1. The best results are shown in bold*

## 方法谱系与知识库定位

### 1. 问题定位：Practical No-box Scenario (PNS) 的独特约束

PGA 面向的是 **Practical No-box Scenario (PNS)**，这一场景对攻击者施加了极其严格的约束：仅能获取少量无标签图像（通常为 4,000 张），无法访问任何大规模标注数据集或预训练替代模型。这使其与传统的黑盒攻击、无盒攻击以及现有的生成式攻击设定存在本质区别。

在传统生成式攻击范式中，方法通常依赖以下先验之一：
- **大规模标注数据**：如 **CDA** (Naseer et al., NeurIPS 2019)、**GAPF** (Salzmann et al., NeurIPS 2021) 等需要足够的数据来训练替代模型和生成器。
- **预训练替代模型**：如 **BIA** (Zhang et al., ICLR 2022) 和 **FACL** (Yang et al., AAAI 2024)，它们假设攻击者已拥有一个在大规模数据上预训练好的替代模型。

当这些先验被剥夺时，现有方法面临两个核心瓶颈：(1) 自监督学习在有限数据下容易产生特征空间坍缩、表示能力退化，导致替代模型无法有效引导生成器；(2) 生成器由于缺乏强监督和多样数据分布，产生的扰动呈碎片化、空间覆盖率低，限制了跨模型可迁移性。PGA 正是针对这两个瓶颈提出了系统性的解决方案。

### 2. 与 PNS 迭代式攻击基线的关系

在 PNS 设定下，已有若干迭代式攻击方法被提出：

- **PNAA** (Li et al., NeurIPS 2020)：早期的 PNS 攻击方法，通过数据增强和邻域采样来生成对抗样本。
- **ETF** (Sun et al., NeurIPS 2022)：利用集成迁移和特征变换来提升攻击可迁移性。
- **CDTA** (Li et al., AAAI 2023)：通过跨域迁移增强来改善攻击效果。
- **AGS** (Wang et al., AAAI 2024)：引入自适应梯度缩放策略。

这些方法均为**迭代式攻击**，即针对每张图像需要多步梯度计算来优化对抗扰动。PGA 与它们的核心差异在于**生成式范式**：PGA 训练一个前馈生成器，在推理时仅需一次前向传播即可产生对抗样本，速度远快于迭代式方法（见图 1 的速度对比）。然而，生成式攻击在 PNS 下的挑战更大，因为生成器需要从极有限的数据中学习到可迁移的扰动模式。

### 3. 与生成式攻击基线的方法论对比

PGA 将现有生成式攻击方法（CDA、GAPF、BIA、FACL）适配到 PNS 设定下作为基线，并在两个关键模块上做出了实质性改进：

#### 3.1 替代模型训练：从简单自监督到课程式微鲁棒优化

基线方法（如 BIA 使用的 SimSiam）仅采用干净多视图对比损失 $\mathcal{L}_{\text{cle}}^S$ 训练替代模型。在数据极度匮乏的 PNS 下，这种训练方式容易导致特征空间坍缩——模型只学习到少数判别性特征，忽略了对生成对抗扰动至关重要的多样化特征。

PGA 提出的 **课程式微鲁棒优化 (CMRO)** 在以下方面做出改进：
- **课程调度**：前 $T$ 个 epoch 仅使用干净损失进行预热，确保模型稳定收敛；之后引入微鲁棒分支 $\mathcal{L}_{\text{rob}}^S$，以固定权重 $\lambda_t = 0.5$ 联合优化，避免早期引入鲁棒目标导致训练不稳定。
- **微鲁棒扰动**：在输入空间施加极小幅度的对抗扰动（强度由 $\tau$ 控制，最优值 $\tau_{\max} = 0.01$），使模型在“轻微挑战”下学习更鲁棒的特征表示，而非直接面对强对抗训练的退化风险。

这一设计与标准对抗训练的区别在于“微”和“课程”两个维度：扰动强度远小于典型的对抗训练（如 $\epsilon = 16$ 下的对抗训练），且通过渐进式引入避免了有限数据下的过拟合。图 4 的证据表明，CMRO 训练的替代模型在中间层特征分布上更接近标准预训练模型（Wasserstein 距离更小），验证了其缓解特征坍缩的有效性。

#### 3.2 生成器训练：从全局特征对齐到区域感知一致性扰动学习

基线生成式攻击（如 BIA）仅优化全局特征相似度损失 $\mathcal{L}_{\text{ori}}^G$，即最小化替代模型在全图级别对干净样本和对抗样本的特征余弦相似度。这种方式产生的扰动往往集中在局部判别性区域，缺乏空间连贯性。

PGA 提出的 **区域感知一致性扰动学习 (RCPL)** 引入了两个额外约束：
- **区域特征相似度损失** $\mathcal{L}_{\text{reg}}^G$：将图像划分为 $K$ 个非重叠区域（最优 $K = 4$），在每个区域上分别计算特征相似度损失，迫使生成器在每个局部区域都产生有效扰动，从而提升扰动的细粒度和空间覆盖率。
- **跨区域一致性损失** $\mathcal{L}_{\text{cro}}^G$：计算不同区域特征 Gram 矩阵之间的 Frobenius 距离，并最小化这些距离。Gram 矩阵编码了特征通道之间的相关性结构，通过强制不同区域的 Gram 矩阵一致，RCPL 鼓励生成器学习空间统计上连贯的扰动模式，而非碎片化的局部噪声。

这一设计的深层动机在于：模型无关的对抗扰动往往表现为全局结构性的模式，而非对特定局部特征的过拟合。通过区域级别的特征分离与跨区域一致性正则化，RCPL 引导生成器从依赖局部特征的模式转向学习更通用的扰动结构，从而提升跨模型、跨域和跨任务的可迁移性。

### 4. 方法适用边界与局限

尽管 PGA 在 PNS 设定下取得了显著提升，其适用边界和潜在局限值得关注：

- **数据量下限**：PGA 在 4,000 张无标签图像上进行了充分验证，但在更极端的数据匮乏场景（如仅几百张图像）下的表现尚不明确。CMRO 的课程调度依赖于足够的预热 epoch 来建立稳定的特征表示，数据量过少可能导致预热阶段本身就无法收敛。
- **扰动预算敏感性**：PGA 在 $\epsilon = 16$ 和 $\epsilon = 10$ 下均有验证（见表 6），但在更小的扰动预算下，RCPL 的区域划分策略可能面临挑战——过小的扰动幅度可能不足以在区域级别产生可感知的特征偏移。
- **生成器架构依赖性**：PGA 的生成器架构与基线方法保持一致以确保公平比较，但未探索不同生成器架构（如扩散模型、StyleGAN 等）对 RCPL 损失的兼容性。更强大的生成器可能进一步提升攻击效果，但也可能引入额外的训练复杂度。
- **防御适应性**：PGA 在多种防御机制下展现了较强的鲁棒性（见表 7，AVGd 达 72.16%），但这些防御主要为静态防御。面对自适应防御（如基于对抗训练的在线防御），PGA 的性能可能下降，因为 CMRO 的微鲁棒训练强度远低于标准对抗训练。
- **语义合理性未验证**：PGA 的目标是最大化攻击成功率，未对生成扰动的语义合理性施加约束。在需要对抗样本保持自然语义的场景（如物理世界攻击），PGA 的扰动可能引入不自然的视觉伪影。

### 5. 开放问题

1. **信息极限探索**：在信息极度匮乏的实际无盒场景下，生成式攻击的潜力究竟能有多大？PGA 在 4,000 张图像上取得了 71.39% 的 CNN 平均攻击成功率，但这一性能是否接近 PNS 设定下的理论上限，仍是一个开放问题。

2. **更少样本的扩展性**：方法是否能进一步扩展至更少的样本量（如几百张）？这可能需要更激进的自监督学习策略或元学习框架来弥补数据不足。

3. **生成扰动的语义合理性**：如何在不牺牲攻击成功率的前提下，保证生成扰动的语义合理性？这可能需要引入感知损失或语义约束，与 RCPL 的优化目标进行平衡。

4. **跨架构泛化的理论理解**：PGA 在 CNN 和 ViT/MLP 之间的可迁移性提升显著（AVGv 从 32.95% 提升至 47.50%），但其背后的理论机制尚需更深入的分析——RCPL 的跨区域 Gram 一致性是否与 ViT 的自注意力机制存在某种结构上的契合？

5. **动态场景下的适应性**：PGA 假设攻击者在训练阶段已拥有目标域的无标签图像。在完全动态的场景下（目标域数据在攻击时才能获取），PGA 的生成器能否快速微调以适应新域，仍需进一步研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/PGA_Prior_free_Generative_Attack_for_Practical_No_box_Scenario.pdf]]
