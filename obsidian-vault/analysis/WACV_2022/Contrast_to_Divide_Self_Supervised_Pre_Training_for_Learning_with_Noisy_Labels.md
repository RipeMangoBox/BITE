---
title: "Contrast to Divide: Self-Supervised Pre-Training for Learning with Noisy Labels"
type: paper
paper_level: A
venue: WACV
year: 2022
pdf_ref: paperPDFs/WACV_2022/Contrast_to_Divide_Self_Supervised_Pre_Training_for_Learning_with_Noisy_Labels.pdf
project_link: null
code_link: https://github.com/ContrastToDivide/C2D
aliases:
- CCD
- CDSSPTLNL
tags:
- WACV_2022
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "是否在 warm-up 前使用目标数据集上的自监督预训练（无标签）以提供高质量、噪声无关的特征初始化。"
primary_logic: "通过丢弃标签，自监督预训练可以在不受噪声干扰的情况下从训练集本身学到强健的特征表示，使后续 LNL 方法能够获得更好的特征质量和损失分离性，尤其在高噪声条件下大幅度提升准确率。"
claims:
- "在 CIFAR-100 90% 对称噪声下，C2D (DivideMix with SimCLR) 峰值准确率达到 93.57%，而原始 DivideMix 仅为 31.5%。"
- "在 mini-WebVision 上，C2D 的 top-1 准确率为 78.57%，比之前最佳方法（DivideMix, Inception-ResNet-v2）的 75.20% 高出超过 3 个百分点。"
- "在 CIFAR-100 warm-up 结束时，C2D 的 ROC-AUC 噪声检测分数和线性分类准确率远高于标准 warm-up 和 ImageNet 预训练，且几乎不随噪声水平升高而退化。"
- "使用 ImageNet 监督预训练反而破坏了损失分布的可分离性，使 ELR+ 在 CIFAR-100 80% 噪声下的准确率从 60.8% 降至 48.58%。"
---

# Contrast to Divide: Self-Supervised Pre-Training for Learning with Noisy Labels

> [!tip] 核心洞察
> 通过丢弃标签，自监督预训练可以在不受噪声干扰的情况下从训练集本身学到强健的特征表示，使后续 LNL 方法能够获得更好的特征质量和损失分离性，尤其在高噪声条件下大幅度提升准确率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 对比分割：用于带噪标签学习的自监督预训练 |
| 英文题名 | Contrast to Divide: Self-Supervised Pre-Training for Learning with Noisy Labels |
| 会议/期刊 | WACV 2022 |
| Links | [paper](https://arxiv.org/abs/2103.13646) · [GitHub](https://github.com/ContrastToDivide/C2D) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | C2D (Contrast to Divide) |
| Dataset | CIFAR-100 (90% symmetric noise), CIFAR-10 (90% symmetric noise), mini-WebVision, Clothing1M |

> [!tip] 效果简介
> - CIFAR-100 (90% symmetric noise) 上，Peak accuracy 为 93.57% (C2D‑DivideMix with SimCLR)，对比 31.5% (DivideMix)，变化 +62.07。
> - CIFAR-10 (90% symmetric noise) 上，Final accuracy 为 89.30% (C2D‑ELR+ with SimCLR)，对比 78.7% (ELR+)，变化 +10.60。
> - mini-WebVision 上，Top‑1 accuracy 为 78.57% (C2D‑DivideMix with SimCLR, ResNet‑50)，对比 74.42% (DivideMix* ResNet‑50)，变化 +4.15。

## 概要

在带噪标签学习（Learning with Noisy Labels, LNL）中，现有方法普遍依赖一个 **warm‑up 阶段**来获得初始的损失分离性与特征表示，然而这一阶段本身存在严重瓶颈：当噪声比例升高时，在全量含噪数据上训练的特征提取器质量急剧下降，且不可避免地记忆噪声标签，导致干净样本与噪声样本的损失分布难以分离，从而限制了后续 LNL 算法的性能上限。

本文提出 **C2D（Contrast to Divide）**，一种简单而通用的两阶段框架，核心思想是**在 warm‑up 之前引入目标数据集上的自监督预训练**，以“丢弃标签”的方式从根本上规避噪声对特征学习的干扰。具体而言，C2D 首先在无标签训练集上执行对比学习（如 SimCLR 或 Barlow Twins），获得噪声无关的高质量特征提取器；随后加载预训练权重，运行任意标准 LNL 方法（如 DivideMix 或 ELR+）进行微调。这一设计将 warm‑up 的瓶颈从“含噪监督学习”转移为“无监督表示学习”，使特征质量和损失分离性几乎不受噪声水平影响。

实验结果表明，C2D 在高噪声条件下带来显著且一致的性能提升：

- **CIFAR‑100，90% 对称噪声**：C2D‑DivideMix（SimCLR）峰值准确率达到 93.57%，而原始 DivideMix 仅为 31.5%（Table 2）。
- **CIFAR‑10，90% 对称噪声**：C2D‑ELR+（SimCLR）最终准确率达到 89.30%，较 ELR+ 的 78.7% 提升超过 10 个百分点（Table 1）。
- **mini‑WebVision**：C2D‑DivideMix（SimCLR, ResNet‑50）top‑1 准确率为 78.57%，比此前最佳结果（DivideMix 的 75.20%）高出超过 3 个百分点（Table 4）。
- **Clothing1M**：C2D‑ELR+（SimCLR）达到 74.58%，与使用 ImageNet 预训练的 SOTA 方法持平，且仅用 SimCLR 预训练 + 标准交叉熵即可达到 72.05%，验证了自监督预训练本身对 warm‑up 的改善（Table 3）。

值得注意的是，**监督预训练（如 ImageNet）在某些条件下反而会损害 LNL 性能**：在 CIFAR‑100 80% 噪声下，ImageNet 预训练使 ELR+ 准确率从 60.8% 降至 48.58%，并破坏了损失分布的可分离性（Section 6.2, Figure 3）。这一反直觉发现进一步凸显了自监督预训练在带噪标签场景中的独特优势。

C2D 的方法定位清晰：它不改变现有 LNL 算法的内部机制，而是通过**替换特征初始化的来源**来解决 warm‑up 瓶颈，因此可无缝集成到任何 LNL 方法中。其局限性主要包括自监督预训练的高计算成本（CIFAR 上需 1000 epochs，4–8 GPU），以及在真实噪声场景下预训练优势未能被 LNL 方法完全转化为最终性能提升的问题。

### 带噪标签学习的核心挑战

深度神经网络在高质量人工标注数据集上取得了显著成功，但获取大规模精确标注的成本极高。现实世界中的数据常通过众包、网络爬取或自动化标注管道收集，不可避免地包含大量错误标签。带噪标签学习（Learning with Noisy Labels, LNL）旨在从这类含噪数据中训练出鲁棒的分类器，其核心挑战在于：深度网络具有强大的记忆能力，会不可避免地拟合噪声标签，导致泛化性能严重退化。

### 现有 LNL 方法的“预热”瓶颈

当前主流的 LNL 方法大多采用两阶段策略：首先进行一个“预热”（warm-up）阶段，在全量含噪数据上使用标准交叉熵训练若干 epoch；随后利用预热阶段产生的损失值分布，通过高斯混合模型（GMM）等方法将样本划分为干净样本和噪声样本，再进入半监督学习或样本重加权等后续处理。代表性方法包括 **DivideMix**（Li et al., ICLR 2020）、**ELR+** 和 **Meta-learning**（Li et al., CVPR 2019）。

然而，预热阶段本身存在一个根本性困境。预热阶段需要同时完成两个目标：

1. **特征提取**：为后续的噪声检测和半监督学习提供有判别力的特征表示。
2. **损失分离**：使干净样本和噪声样本的损失值分布能够被有效区分，这是 GMM 正确划分样本的前提。

问题在于，这两个目标在含噪数据上相互冲突。随着噪声水平升高，特征提取器的质量急剧下降——网络在错误标签的引导下学到扭曲的特征表示，同时不可避免地开始记忆噪声样本，导致干净样本和噪声样本的损失分布高度重叠，分离性变差。这一现象在 Figure 2 中有清晰的量化证据：在 CIFAR-100 上，标准预热（随机初始化）的 ROC-AUC 噪声检测分数和线性分类准确率随噪声水平升高而迅速退化。

### 为什么监督预训练不是答案

一个直观的补救思路是使用外部大规模干净数据集（如 ImageNet）进行监督预训练，为预热阶段提供更好的特征初始化。但本文的实验揭示了一个反直觉的发现：**ImageNet 监督预训练反而会损害 LNL 性能**。在 CIFAR-100 80% 对称噪声下，使用 ImageNet 预训练使 ELR+ 的准确率从 60.8% 显著下降至 48.58%，并且严重破坏了损失分布的分离性（Figure 3）。这表明，来自不同领域的监督预训练特征可能引入领域偏差，在含噪标签的微调过程中反而加剧了噪声记忆。

### 核心洞察与本文动机

本文的关键洞察是：**通过完全丢弃标签，在目标训练集上进行自监督预训练，可以在不受噪声干扰的情况下学到强健的特征表示**。自监督学习（如对比学习）不依赖任何标签信号，因此天然免疫于标签噪声的影响。由此得到的特征提取器能为后续 LNL 方法提供高质量、噪声无关的初始化，从根本上打破预热阶段的特征-分离困境。

基于这一洞察，本文提出 **C2D（Contrast to Divide）** 框架：先通过自监督对比学习在无标签训练集上预训练特征提取器（Contrast 阶段），再加载预训练权重运行任意标准 LNL 方法（Divide 阶段）。这一简单而有效的策略使 LNL 方法在极高噪声条件下获得了前所未有的性能提升——例如在 CIFAR-100 90% 对称噪声下，C2D 将 DivideMix 的准确率从 31.5% 提升至 93.57%。

## 核心方法与创新机理

C2D 的核心创新在于**将带噪标签学习（LNL）的范式从“从含噪标签中学习”转变为“先无标签预训练，再含噪标签微调”**。这一转变直击 LNL 方法在 warm-up 阶段的瓶颈：特征提取器质量随噪声水平升高而急剧下降，且无法避免记忆噪声标签，导致损失分离性差。C2D 通过丢弃标签，在 warm-up 之前引入目标数据集上的自监督预训练，从根本上绕过了噪声对特征学习的干扰。

### 关键 changed slots

C2D 并非提出全新的 LNL 算法，而是对现有 LNL 流程的三个关键 slot 进行了系统性替换：

**1. 特征提取器初始化方式（核心 slot）**

- **Baseline 值**：随机初始化（或 ImageNet 监督预训练）
- **C2D 值**：在目标训练集上进行自监督预训练（SimCLR，CIFAR 上 1000 epochs）
- **因果机制**：自监督预训练不依赖任何标签，因此完全不受噪声干扰。它从训练集本身学到强健的、聚类良好的特征表示，为后续 LNL 阶段提供了高质量的初始化。Figure 1 的 UMAP 可视化显示，C2D 在 warm-up 结束时的特征聚类质量显著优于标准 DivideMix，即使在 90% 噪声下，类别间边界依然清晰。Figure 2 进一步量化了这一优势：在 CIFAR-100 上，C2D 的 ROC-AUC 噪声检测分数和线性分类准确率几乎不随噪声水平升高而退化，而标准 warm-up 和 ImageNet 预训练均出现严重衰减。
- **反直觉发现**：ImageNet 监督预训练反而破坏了损失分布的可分离性。在 CIFAR-100 80% 噪声下，ImageNet 预训练使 ELR+ 的准确率从 60.8% 降至 48.58%（Section 6.2，Figure 3）。这表明监督预训练引入的领域偏置或类别语义可能与噪声检测任务冲突，而自监督预训练不存在此问题。

**2. Warm-up 训练时长（适配 slot）**

- **Baseline 值**：CIFAR-10 10 epochs，CIFAR-100 30 epochs（DivideMix 默认）
- **C2D 值**：5 epochs
- **因果机制**：自监督预训练已经提供了高质量的特征提取器，warm-up 阶段不再需要从零开始学习特征。缩短 warm-up 可以防止模型在含噪标签上过拟合，同时保持足够的损失分离性来支持 GMM 噪声检测。实验发现 5 个 epoch 在所有 CIFAR 噪声水平下均足够（Section 5.1）。

**3. GMM 阈值 τ（适配 slot）**

- **Baseline 值**：0.5
- **C2D 值**：0.03
- **因果机制**：自监督预训练使得干净样本和噪声样本的损失分布分离性显著增强（Figure 3），干净样本的损失更低且分布更集中。因此，GMM 可以以更严格的阈值（更低的不确定性容忍度）来划分干净/噪声样本，从而更精确地筛选出干净样本用于后续半监督学习。τ=0.03 远低于 DivideMix 的 0.5，反映了预训练特征带来的损失分布质量提升。

### 方法框架

C2D 是一个两阶段框架，可无缝嵌入任何 LNL 方法：

1. **Contrast phase（对比阶段）**：在无标签训练集上使用 SimCLR（或 Barlow Twins）进行自监督对比学习，获得噪声无关的高质量特征提取器。
2. **Divide phase（分割阶段）**：加载预训练权重，运行标准 LNL 方法（如 DivideMix 或 ELR+），利用强特征实现更准确的噪声检测与损失分离。

这一框架的通用性在实验中得到了验证：C2D 分别与 DivideMix（基于半监督学习）和 ELR+（基于正则化）结合，均取得了显著提升，表明自监督预训练的优势独立于具体 LNL 算法的设计。

C2D（Contrast to Divide）是一个两阶段框架，其核心思想简单而直接：**先丢弃标签进行自监督对比预训练以获取高质量特征，再加载该特征进行标准的有噪标签学习（LNL）**。这一设计直击 LNL 方法中 warm-up 阶段的核心瓶颈——在全量含噪数据上随机初始化训练时，特征提取器质量随噪声水平升高而急剧下降，导致损失分离性差，严重限制了后续 LNL 算法的性能。

### 两阶段 Pipeline

**第一阶段：对比预训练（Contrast phase）**

在完全不使用任何标签的条件下，直接在目标训练集上执行自监督对比学习。本文默认采用 **SimCLR** 作为预训练方法，同时验证了 **Barlow Twins** 等替代方案同样有效。该阶段的目标是学到一个**噪声无关的高质量特征提取器**——由于训练过程完全绕过了含噪标签，特征学习不受标签噪声的任何干扰。

**第二阶段：LNL 微调（Divide phase）**

加载第一阶段预训练得到的特征提取器权重，将其作为初始化，然后运行标准的 LNL 方法（如 **DivideMix**（Li et al., ICLR 2020）或 **ELR+**）。得益于高质量的初始特征，LNL 方法在 warm-up 阶段能够获得更好的损失分离性，从而更准确地检测噪声样本，并在后续的半监督训练中取得显著更好的性能。

### 关键设计调整

为适配预训练特征，C2D 对下游 LNL 方法的超参数做了针对性调整：

- **Warm-up 时长大幅缩短**：在 CIFAR 数据集上，C2D 将 DivideMix 默认的 warm-up 训练轮数从 CIFAR-10 的 10 epochs / CIFAR-100 的 30 epochs 统一缩减至 **5 epochs**。预训练特征已具备良好的判别能力，仅需少量训练即可完成损失分离。
- **GMM 阈值显著降低**：将噪声检测中高斯混合模型的后验概率阈值从默认的 0.5 降至 **0.03**。预训练特征下干净样本的损失值更低且分布更集中，更低的阈值有助于更精确地筛选干净样本。

### 输入输出流

整个框架的输入为**含噪训练集**（图像及其对应的含噪标签），输出为**训练好的分类模型**。具体流程如下：

1. 输入含噪训练集中的所有图像（忽略标签），送入 SimCLR 等自监督框架进行对比预训练，得到预训练特征提取器。
2. 加载预训练权重初始化分类网络，在含噪训练集（图像 + 含噪标签）上执行短时 warm-up，利用 GMM 对样本损失进行噪声/干净分离。
3. 基于分离结果，LNL 方法进入半监督训练阶段，对干净样本使用真实标签监督，对噪声样本使用预测标签进行一致性正则化，最终输出鲁棒分类模型。

### 方法兼容性

C2D 框架的显著优势在于其**即插即用**的特性——自监督预训练阶段与下游 LNL 方法完全解耦，理论上可以无缝结合任何 LNL 算法。本文在 **DivideMix** 和 **ELR+** 两种不同机制的 LNL 方法上均验证了 C2D 的有效性，表明该框架具有良好的通用性。

### C2D 框架总览

C2D（Contrast to Divide）是一个简洁的两阶段框架，旨在解决带噪标签学习（Learning with Noisy Labels, LNL）中 warm-up 阶段的特征退化瓶颈。其核心思想是：**在 LNL 训练之前，先通过自监督对比学习在目标数据集（无标签）上获得高质量、噪声无关的特征提取器，再将其作为初始化馈入任意 LNL 方法**。

框架由两个序贯模块组成：

1. **Contrast 阶段（自监督预训练）**：在训练集上丢弃所有标签，使用 SimCLR 或 Barlow Twins 等对比学习方法训练特征提取器。该阶段不接触任何噪声标签，因此学到的特征表示天然具有噪声无关性。
2. **Divide 阶段（LNL 微调）**：加载预训练权重，运行标准 LNL 方法（如 DivideMix 或 ELR+），利用强特征初始化实现更准确的噪声检测与损失分离。

### 模块一：自监督预训练（Contrast 阶段）

**目标**：在无标签条件下，从含噪训练集中学得高质量特征提取器 $f_\theta$。

**方法**：采用 SimCLR 对比学习框架。对于每个样本 $x_i$，通过随机数据增强生成两个视图 $x_i^{(1)}$ 和 $x_i^{(2)}$，经编码器 $f_\theta$ 和投影头 $g_\phi$ 映射到表示空间后，使用 NT-Xent 损失最大化同一源样本两个视图之间的一致性，同时推开不同样本的表示。

**关键配置**（Section 5.1）：
- CIFAR-10/100 上使用 ResNet-18，训练 1000 epochs，4 张 NVIDIA 2080 Ti GPU
- mini-WebVision 上使用 ResNet-50
- Clothing1M 上同时验证了 SimCLR 和 Barlow Twins 两种预训练方案

**核心作用**：自监督预训练解决了 warm-up 阶段的两个根本问题——特征提取器质量随噪声水平升高而急剧下降，以及无法避免记忆噪声标签。由于完全不接触标签，该阶段不会受到噪声干扰，最终产出的特征表示在 UMAP 可视化中呈现出清晰的类别聚类结构（Figure 1 上排），即使在 90% 极端噪声条件下依然保持良好分离性。

### 模块二：LNL 微调（Divide 阶段）

**目标**：利用预训练特征初始化，执行标准 LNL 流程完成噪声检测与半监督学习。

**流程**：
1. 加载 Contrast 阶段获得的编码器权重 $f_\theta$
2. 替换分类头为随机初始化的新线性层
3. 运行 LNL 方法的标准流程：warm-up → 噪声检测（基于 GMM 对损失分布建模）→ 样本划分 → 半监督训练

**关键超参数调整**（Section 5.1）：
- **Warm-up 时长**：CIFAR 数据集上从 DivideMix 默认的 10/30 epochs 缩短至 5 epochs，因预训练特征已足够强健
- **GMM 阈值 $\tau$**：从 0.5 降至 0.03，因预训练特征下损失分离性显著增强，可更激进地筛选干净样本

**兼容性**：该模块对底层 LNL 方法无侵入性修改，仅通过特征初始化质量提升和少量超参数适配即可获得增益。论文验证了与 DivideMix 和 ELR+ 两种代表性方法的无缝结合。

### 核心公式

本文未提出新的理论公式，而是复用已有方法的损失函数。C2D 框架的创新在于**训练范式的重新编排**，而非公式层面的推导。以下为涉及的关键损失函数及其变量含义：

**SimCLR 对比损失（NT-Xent）**：在 Contrast 阶段使用，用于自监督预训练。对于大小为 $N$ 的 mini-batch，每个样本的两个增强视图形成 $2N$ 个数据点，正样本对 $(i, j)$ 的损失为：

$$\ell_{i,j} = -\log \frac{\exp(\text{sim}(z_i, z_j) / \tau)}{\sum_{k=1}^{2N} \mathbb{1}_{[k \neq i]} \exp(\text{sim}(z_i, z_k) / \tau)}$$

其中 $z_i = g_\phi(f_\theta(\tilde{x}_i))$ 为增强视图 $\tilde{x}_i$ 的投影表示，$\text{sim}(\cdot, \cdot)$ 为余弦相似度，$\tau$ 为温度参数。

**LNL 阶段的交叉熵损失**：在 Divide 阶段的 warm-up 和后续半监督训练中，对已标注（或伪标注）样本使用标准交叉熵：

$$\mathcal{L}_{\text{CE}} = -\frac{1}{|\mathcal{D}|} \sum_{(x, y) \in \mathcal{D}} y \log p(x)$$

其中 $p(x)$ 为分类器对样本 $x$ 的 softmax 输出，$\mathcal{D}$ 为当前阶段的训练子集（可能是干净样本集或混合集）。

**GMM 噪声检测**：在 warm-up 结束后，对每个样本的交叉熵损失值拟合两分量高斯混合模型，后验概率较低的成分对应噪声样本。此过程不涉及显式公式推导，而是标准统计推断步骤。

> **注意**：本文未提供 Barlow Twins 预训练损失的具体公式，也未对 ELR+ 的正则化项进行公式展开。如需完整推导，请参阅 SimCLR（Chen et al., ICML 2020）、DivideMix（Li et al., ICLR 2020）和 ELR+ 的原论文。

### 方法谱系与知识库定位

C2D 属于 **自监督预训练 + LNL 微调** 的混合范式，其核心贡献在于识别并解决了 LNL 方法中 warm-up 阶段的结构性瓶颈。

**与基线方法的关系**：
- **DivideMix**（Li et al., ICLR 2020）：C2D 直接复用其两阶段半监督 LNL 流程，但将随机初始化的 warm-up 替换为自监督预训练初始化，在高噪声条件下将 CIFAR-100 准确率从 31.5% 提升至 93.57%
- **ELR+**：C2D 复用其早期学习正则化机制，通过自监督预训练使 CIFAR-10 90% 噪声下准确率从 78.7% 提升至 89.30%
- **Meta-learning 方法**（Li et al., CVPR 2019）：C2D 在 CIFAR-100 90% 噪声下以 93.57% 远超其 47.1% 的准确率

**与 ImageNet 监督预训练的本质区别**：监督预训练在域差异和噪声干扰下反而会破坏损失分布的可分离性（Figure 3），使 ELR+ 在 CIFAR-100 80% 噪声下准确率从 60.8% 降至 48.58%。C2D 通过在目标数据集上自监督预训练，避免了域偏移和标签噪声的双重干扰。

**框架的通用性**：C2D 不依赖特定 LNL 算法，理论上可与任何需要 warm-up 的 LNL 方法结合。在 Clothing1M 上，即使不使用专门的 LNL 算法，仅 SimCLR 预训练 + 标准交叉熵即可达到 72.05%，超过 ImageNet 预训练的 69.21%，验证了自监督预训练作为通用 warm-up 替代方案的潜力。

## 实验与关键发现

### 1. 核心瓶颈：Warm‑up 阶段特征质量与损失分离的双重失效

C2D 的实验设计建立在一个明确的问题诊断之上：现有 LNL 方法（如 **DivideMix** (Li et al., ICLR 2020)、**ELR+**）的 warm‑up 阶段在全量含噪数据上训练时，特征提取器质量随噪声水平升高而急剧下降，且无法避免记忆噪声标签，导致干净样本与噪声样本的损失分布严重重叠，限制了后续噪声检测与半监督学习的性能。

Figure 2 定量地揭示了这一瓶颈：在 CIFAR‑100 上，标准 warm‑up 的噪声检测 ROC‑AUC 和线性分类准确率均随噪声比例上升而显著退化；而 C2D 在使用自监督预训练（SimCLR）初始化后，这两项指标几乎不随噪声水平升高而下降，始终保持高位。这直接验证了因果操纵变量——是否在 warm‑up 前使用目标数据集上的自监督预训练——对瓶颈的解除作用。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2103_13646/figures/007_Figure.jpg]]

### 2. CIFAR‑10/100 主实验结果：高噪声条件下的数量级提升

Table 1 和 Table 2 汇总了 CIFAR‑10 和 CIFAR‑100 上对称噪声与不对称噪声的完整对比。C2D 的核心优势集中在高噪声区域：

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2103_13646/figures/003_Table_1.jpg]]
*Table 1: Classification accuracy (%, mean ± std over five runs) on CIFAR-10. C2D achieves consistently high accuracy under different noise rates and types, with markedly improved performance under very-high noise conditions. Meta-learning results provided by Li et al. [29]*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2103_13646/figures/004_Table_2.jpg]]
*Table 2: Peak and final classification accuracies (%, mean ± std over five runs) on CIFAR-100. Unlike previous methods that suffer from rapid degradation, C2D was able to maintain good performance even under severe noise. Meta-learning results provided by Li et al. [29]. ∗ denotes results acquired by us based on published code*

**CIFAR‑10（Table 1）**：
- 在 90% 对称噪声下，C2D‑ELR+（SimCLR）最终准确率达到 89.30%，比 ELR+ 基线（78.7%）提升 10.60 个百分点。
- 在 80% 对称噪声下，C2D‑DivideMix（SimCLR）峰值准确率达到 94.40%，而原始 DivideMix 仅为 67.78%。

**CIFAR‑100（Table 2）**：
- 在 90% 对称噪声下，C2D‑DivideMix（SimCLR）峰值准确率达到 93.57%，而原始 DivideMix 仅为 31.5%，提升幅度超过 62 个百分点。
- 在 95% 对称噪声这一极端条件下，C2D 最终准确率仍保持在 38% 以上（每次独立运行不低于 30%），而基线方法在此噪声水平下几乎完全失效。

在低噪声条件下（如 20% 对称噪声），C2D 的提升相对温和（CIFAR‑10 上 ELR+ 从 95.8% 提升至 96.83%），表明自监督预训练的核心价值在于对抗高噪声对特征学习的破坏，而非在干净数据上进一步优化。

不对称噪声场景下的提升有限：CIFAR‑100 40% 不对称噪声下，C2D 仅提升约 0.63 个百分点，说明该方法对标签翻转模式的鲁棒性仍有改进空间。

### 3. 真实世界噪声数据集：WebVision 与 Clothing1M

在 mini‑WebVision 上（Table 4），C2D‑DivideMix（SimCLR, ResNet‑50）达到 78.57% Top‑1 准确率，比原始 DivideMix（ResNet‑50 复现结果 74.42%）高出 4.15 个百分点，比之前最佳方法 DivideMix（Inception‑ResNet‑v2, 75.20%）高出超过 3 个百分点。在 ILSVRC12 验证集上的迁移表现同样领先，表明自监督预训练学到的特征具有较好的泛化能力。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2103_13646/figures/006_Table_4.jpg]]
*Table 4: Accuracy (%, mean ± std over five runs) on the WebVision validation set and the ILSVRC12 (ImageNet) validation sets, for the networks trained on (mini) WebVision dataset. ∗ denotes results acquired by us based on published code*

Clothing1M 的结果（Table 3）则呈现出一个值得关注的对比：
- 仅使用 SimCLR 预训练 + 标准交叉熵（不进行 LNL）即可达到 72.05% 准确率，超过 ImageNet 预训练的 69.21%，验证了自监督预训练本身对 warm‑up 的改善效果。
- 然而，当叠加 LNL 方法后，C2D‑ELR+（SimCLR）最终准确率为 74.58%，与使用 ImageNet 预训练的 SOTA 方法（如 DivideMix 74.76%）基本持平甚至略低。这表明在 Clothing1M 上，自监督预训练带来的初始化优势未能被 LNL 方法完全转化为最终性能提升——这是一个需要手动验证的结论，可能与 Clothing1M 的噪声特性、类别分布或 LNL 算法对预训练特征的利用效率有关。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2103_13646/figures/005_Table_3.jpg]]
*Table 3: Comparison with state-of-the-art methods in test accuracy (%) on Clothing1M. The upper part of the table uses ImageNet pre-training, while the lower half does not*

### 4. 消融分析：自监督预训练 vs. 监督预训练

C2D 的关键消融围绕预训练方式展开，揭示了一个反直觉的发现：**监督预训练可能损害 LNL 性能**。

在 CIFAR‑100 80% 噪声下（Section 6.2, Figure 3），使用 ImageNet 监督预训练初始化的 DivideMix，其 warm‑up 后的损失分布分离性反而比随机初始化更差——干净样本与噪声样本的损失直方图重叠加剧。相应地，ELR+ 在同样条件下的准确率从 60.8%（随机初始化）降至 48.58%（ImageNet 预训练）。相比之下，C2D 的自监督预训练显著改善了损失分离性，使干净样本的损失更低且与噪声样本的重叠最小。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2103_13646/figures/008_Figure_3.jpg]]
*Figure 3: Loss distribution of clean and noisy samples after warm-up on CIFAR-100 with 80% noise for DivideMix, DivideMix with ImageNet pre-training, and C2D. As seen in the zoom-in, ImageNet pre-training damages the separability whereas self-supervised pre-training (C2D), improves it. Table 5: C2D nearly closes the gap with semi-supervised training on the same clean set size*

这一现象的可能机制是：ImageNet 预训练引入了与目标数据集分布不匹配的强语义先验，在 warm‑up 阶段反而加速了对噪声标签的拟合，破坏了损失分离性。该结论的影响因素（领域差距大小、噪声水平阈值等）仍需系统分析。

自监督方法的兼容性方面（Section 6.3, Table 3），在 Clothing1M 上用 Barlow Twins 预训练 + 交叉熵达到 73.03%，仅比 SOTA 低约 1.5%，表明 C2D 框架不依赖特定的自监督算法，SimCLR 和 Barlow Twins 均可作为有效的预训练方案。

### 5. 训练动态与特征可视化

Figure 1 通过 UMAP 可视化直观对比了 C2D 与 DivideMix 在 CIFAR‑10 warm‑up 结束时的特征分布。在 20% 和 90% 噪声下，C2D 的特征按真实类别形成清晰可分的簇，而 DivideMix 的特征则呈现散乱重叠的状态。这从几何角度解释了 C2D 为何能实现更准确的噪声检测。

Figure B.1 进一步展示了训练过程中的动态指标：C2D 的噪声检测 ROC‑AUC 从训练初期即显著高于基线，且上升更快；有效噪声率下降更稳定。这与缩短 warm‑up 至 5 个 epoch 后仍能保持高性能的现象一致——预训练特征使得 GMM 在极少量有噪训练后即可实现良好的损失分离。

### 6. 计算成本与公平性说明

C2D 的性能优势伴随着显著增加的计算成本：自监督预训练在 CIFAR 数据集上需要 1000 个 epoch，使用 4 块 NVIDIA 2080 Ti GPU。这一成本远高于直接使用随机初始化的 LNL 基线，在资源受限场景下可能成为实际应用的障碍。

在公平性方面，WebVision 比较中 C2D 使用 ResNet‑50，而部分基线使用 Inception‑ResNet‑v2；本文补充了 DivideMix 在 ResNet‑50 上的复现结果以作公平对比。此外，C2D 对 DivideMix 和 ELR+ 的超参数做了少量调整（warm‑up 缩短至 5 epoch、GMM 阈值降至 0.03），以适配预训练特征，但这些调整并非在所有噪声水平下都进行了严格消融，其通用性需要进一步验证。

## 定位与知识库关联

### 一、方法谱系：C2D 在 LNL 研究中的位置

C2D 的核心贡献不在于提出新的 LNL 算法，而在于**重新定义了 LNL 方法的标准前置流程**——将 warm-up 阶段替换为在目标训练集上的自监督预训练。这一设计使其成为 LNL 方法谱系中的一个**正交改进层**，而非与现有 LNL 方法直接竞争。

#### 1.1 与代表性 LNL 方法的关系

C2D 在实验中与以下代表性 LNL 方法进行了组合验证：

- **DivideMix** (Li et al., ICLR 2020)：基于噪声检测和半监督学习的 LNL 方法，采用 warm-up + GMM 两阶段训练。C2D 将 DivideMix 的 warm-up 替换为 SimCLR 自监督预训练后，在 CIFAR-100 90% 对称噪声下将峰值准确率从 31.5% 提升至 93.57%（Table 2）。同时，C2D 将 DivideMix 的 warm-up 时长从 30 epochs 缩短至 5 epochs，GMM 阈值从 0.5 降低至 0.03，以适应预训练特征的高质量初始化。

- **ELR+**：基于早期学习正则化的 LNL 方法，通过梯度扰动防止噪声记忆。C2D 与 ELR+ 组合后，在 CIFAR-10 90% 对称噪声下将最终准确率从 78.7% 提升至 89.30%（Table 1），在 Clothing1M 上达到 74.58%（Table 3）。

- **Meta-learning** (Li et al., CVPR 2019)：基于元学习的 LNL 方法，通过元目标学习重加权样本。在 CIFAR-10/100 实验中作为基线对比，C2D 在所有噪声水平下均显著优于该方法。

C2D 的作者明确声明该框架可与**任意 LNL 方法**无缝结合（Section 1），这意味着 C2D 的定位是 LNL 方法链上的一个**即插即用的特征初始化模块**，而非替代品。

#### 1.2 与自监督学习方法的关系

C2D 的自监督预训练阶段主要使用 **SimCLR** 作为对比学习框架，同时验证了 **Barlow Twins** 的兼容性：

- 在 Clothing1M 上，SimCLR 预训练 + 标准交叉熵（不进行 LNL）即可达到 72.05% 准确率，超过 ImageNet 预训练的 69.21%（Table 3）。
- Barlow Twins 预训练 + 交叉熵达到 73.03%，仅比 SOTA 低约 1.5%（Section 6.3），表明 C2D 框架对自监督方法的选择具有灵活性。

这意味着 C2D 的改进可随自监督学习领域的发展而持续受益——任何更优的对比学习或非对比自监督方法均可直接嵌入 C2D 框架。

### 二、适用边界与关键约束

#### 2.1 噪声类型与水平

C2D 在**对称噪声**（symmetric noise）和**高噪声水平**下优势最为显著：

- 在 CIFAR-100 90% 对称噪声下，C2D-DivideMix 比原始 DivideMix 提升超过 62 个百分点（Table 2）。
- 在 CIFAR-100 95% 极端噪声下，C2D 最终准确率仍保持在 38% 以上（Table 2）。

但在**非对称噪声**（asymmetric noise）下提升有限：

- CIFAR-100 40% 非对称噪声下，C2D 仅提升约 0.63%（Table 2）。该场景仍有改进空间。

#### 2.2 数据集特性

- **CIFAR-10/100**：C2D 表现出色，尤其在高噪声条件下。这得益于自监督预训练在目标数据集上直接学习特征，无需外部数据。
- **Clothing1M**（真实世界噪声）：C2D 的优势未能被 LNL 方法完全转化。尽管 SimCLR 预训练 + 交叉熵（72.05%）优于 ImageNet 预训练（69.21%），但最终 LNL 性能（ELR+ 74.58%）仅与使用 ImageNet 预训练的 SOTA 方法持平或略低（Table 3）。这说明**真实噪声场景下，LNL 算法本身的设计仍存在瓶颈，未能充分利用预训练提供的优质特征**。
- **mini-WebVision**：C2D 以 ResNet-50 达到 78.57% top-1 准确率，比 DivideMix ResNet-50 高出 4.15 个百分点（Table 4）。需注意部分基线使用 Inception-ResNet-v2，本文补充了 ResNet-50 的 DivideMix 结果以作公平对比。

#### 2.3 计算资源约束

C2D 的自监督预训练阶段需要大量计算资源：

- CIFAR 数据集上需训练 1000 epochs，使用 4 块 NVIDIA 2080 Ti GPU（Section 5.1）。
- 这一成本远高于直接使用随机初始化的 LNL 基线，是 C2D 在实际部署中的主要障碍。

### 三、关键局限与开放问题

#### 3.1 已验证的局限

1. **计算开销大**：自监督预训练（SimCLR 1000 epochs）显著增加了训练成本，限制了在资源受限场景下的应用。

2. **真实噪声场景的性能转化不足**：在 Clothing1M 上，自监督预训练的优势未能被 LNL 方法完全转化为最终性能提升，最终准确率仅与 ImageNet 预训练方法持平或略低。

3. **非对称噪声下提升有限**：CIFAR-100 40% 非对称噪声仅提升约 0.63%，该场景仍是 C2D 的薄弱环节。

4. **模态与任务泛化性未验证**：本文仅在视觉分类任务上验证，对其他模态（文本、语音等）或任务（检测、分割等）的泛化性尚不明确。

#### 3.2 开放问题

1. **如何设计能更有效利用自监督预训练特征的 LNL 算法？** 尤其在真实世界噪声场景中，现有 LNL 方法似乎无法充分利用预训练提供的优质特征，这需要 LNL 算法层面的协同设计。

2. **自监督预训练赋予 LNL 鲁棒性的理论解释是什么？** 为什么丢弃标签信息反而能学到更有利于噪声检测的特征？这一机制的理论理解仍为空白。

3. **为什么监督预训练（如 ImageNet）在某些条件下会严重损害 LNL 性能？** 实验显示，在 CIFAR-100 80% 噪声下，ImageNet 监督预训练使 ELR+ 准确率从 60.8% 降至 48.58%，并破坏了损失分布的可分离性（Section 6.2, Figure 3）。其影响因素（领域差距、噪声水平、预训练数据分布等）需要系统分析。

4. **能否开发专门针对 LNL 下游任务的自监督预训练任务？** 当前 C2D 使用的是通用对比学习目标，针对 LNL 的噪声检测和样本分离需求设计专用预训练任务可能进一步释放潜力。

### 四、知识库定位总结

C2D 在 LNL 知识库中的定位可概括为：

- **层级**：LNL 方法链的前置模块（特征初始化层），而非 LNL 算法本身。
- **核心洞察**：通过丢弃标签，自监督预训练可以在不受噪声干扰的情况下从训练集本身学到强健特征，从根本上解决 warm-up 阶段的特征质量退化问题。
- **与现有工作的关系**：与任意 LNL 方法正交兼容，是对现有 LNL 方法体系的**通用增强**，而非替代。
- **适用场景**：高噪声对称噪声场景下优势最大；真实噪声和非对称噪声场景仍有待改进。
- **主要代价**：显著增加的计算开销，以及在某些场景下性能转化不足的问题。

## 原文 PDF

![[paperPDFs/WACV_2022/Contrast_to_Divide_Self_Supervised_Pre_Training_for_Learning_with_Noisy_Labels.pdf]]
