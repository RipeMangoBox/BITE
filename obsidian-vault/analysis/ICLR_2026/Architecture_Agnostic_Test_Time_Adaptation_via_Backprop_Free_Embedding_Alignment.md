---
title: "Architecture-Agnostic Test-Time Adaptation via Backprop-Free Embedding Alignment"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Architecture_Agnostic_Test_Time_Adaptation_via_Backprop_Free_Embedding_Alignment.pdf
openreview_forum_id: 7kLNGaAHaw
aliases:
- PEAP
- AATTABFEA
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/domain_adaptation_and_transfer_learning
core_operator: "中间层嵌入空间的几何对齐（平移、缩放、旋转），即通过纠正领域偏移引起的特征分布变形来恢复模型性能。"
primary_logic: "领域偏移本质上在嵌入空间中产生平移（均值偏移）、缩放（方差偏移）和旋转（协方差偏移）三种系统性几何变化；利用预存源域统计量，通过逐层协方差对齐（白化-着色变换），可以完全在不进行反向传播和参数更新的情况下，渐进式地将目标域特征拉回源域分布，从而实现高效、架构无关的测试时适应。"
claims:
- "领域偏移导致中间层特征出现平移、缩放和旋转三种结构变化。"
- "PEA仅需两次前向传播而不需要反向传播，内存与延迟极低，在ImageNet-C上（ViT-Base）精度64.5%、内存887MB、延迟0.31秒/批。"
- "提出的距离感知加权协方差对齐与EMA统计估计使PEA在小批量下（batch=1）仍保持稳定，ImageNet-C精度61.6%，CIFAR100-C精度69.5%，而多数基线方法失效。"
- "ImageNet-C (ViT-Base) 上 Average Accuracy (%) = 64.5 (PEA) / 66.5 (PEA+Aug)"
---

# Architecture-Agnostic Test-Time Adaptation via Backprop-Free Embedding Alignment

> [!tip] 核心洞察
> 领域偏移本质上在嵌入空间中产生平移（均值偏移）、缩放（方差偏移）和旋转（协方差偏移）三种系统性几何变化；利用预存源域统计量，通过逐层协方差对齐（白化-着色变换），可以完全在不进行反向传播和参数更新的情况下，渐进式地将目标域特征拉回源域分布，从而实现高效、架构无关的测试时适应。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 架构无关的无反向传播测试时适应：通过嵌入对齐实现 |
| 英文题名 | Architecture-Agnostic Test-Time Adaptation via Backprop-Free Embedding Alignment |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=7kLNGaAHaw); [GitHub](https://github.com/TheMaXiao/PEA_TTA) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/domain_adaptation_and_transfer_learning |
| Method | Progressive Embedding Alignment (PEA) |
| Dataset | ImageNet-C (ViT-Base), CIFAR100-C (ViT-Base), CIFAR10-C (ResNet-50), Mixed-Domain CIFAR100-C (ViT-Base) |

> [!tip] 效果简介
> - ImageNet-C (ViT-Base) 上，Average Accuracy (%) 为 64.5 (PEA) / 66.5 (PEA+Aug)，对比 55.5 (No Adapt) / 62.0 (SAR) / 62.6 (SPA)，变化 +9.0 (PEA vs No Adapt) / +11.0 (PEA+Aug vs No Adapt)。
> - CIFAR100-C (ViT-Base) 上，Average Accuracy (%) 为 77.0 (PEA+Aug)，对比 61.6 (No Adapt) / 67.3 (CMF) / 70.6 (SPA)，变化 +15.4 (PEA+Aug vs No Adapt)。
> - CIFAR10-C (ResNet-50) 上，Average Accuracy (%) 为 83.4 (PEA+Aug)，对比 76.9 (No Adapt) / 80.7 (MECTA) / 80.6 (L-TTA)，变化 +6.5 (PEA+Aug vs No Adapt)。

## 概述

测试时适应（Test-Time Adaptation, TTA）旨在使预训练模型在推理阶段动态应对领域偏移，而无需访问源域数据。然而，现有方法普遍依赖反向传播进行参数更新，导致内存占用高、计算延迟大，难以部署于资源受限的边缘设备；同时，多数高效方法仅针对特定架构（如CNN或ViT）设计，缺乏通用性。

本文提出**渐进式嵌入对齐（Progressive Embedding Alignment, PEA）**，一种架构无关、完全无需反向传播的测试时适应框架。其核心洞察在于：领域偏移在中间层嵌入空间中系统性地表现为三种几何变化——**平移**（均值偏移）、**缩放**（方差偏移）和**旋转**（协方差偏移）。PEA通过两个前向传播，利用预存的源域统计量对目标域特征进行逐层协方差对齐（白化-着色变换），逐步将偏移后的嵌入拉回源域分布，而无需修改任何模型参数。

主要结论如下：

- **精度与效率兼顾**：在ImageNet-C上，PEA（ViT-Base）达到64.5%的平均准确率，较无适应基线提升9.0个百分点，同时仅需887MB内存和0.31秒/批的延迟。相比之下，SPA和CMF等高性能方法内存消耗超过10GB，无法在边缘设备上运行。
- **架构通用性**：PEA在ViT和ResNet上使用完全相同的流程，在CIFAR100-C上（ViT-Base）达到77.0%，在CIFAR10-C上（ResNet-50）达到83.4%，分别超越无适应基线15.4和6.5个百分点。
- **小批量稳定性**：通过指数移动平均（EMA）统计估计和域偏移尖峰检测机制，PEA在批次大小为1的极端条件下仍保持稳定（ImageNet-C: 61.6%，CIFAR100-C: 69.5%），而多数基线方法在此设置下失效或严重退化。
- **超参数鲁棒性**：EMA动量和熵阈值在合理范围内对精度影响均小于1个百分点，且仅需5-10%的源数据计算离线统计即可接近饱和性能。

PEA将测试时适应重新定位为嵌入空间的几何校正问题，以极低的计算代价实现了与需反向传播方法相当甚至更优的适应效果，为资源受限场景下的鲁棒部署提供了可行方案。

## 背景与动机

### 测试时适应的核心瓶颈：反向传播的代价

深度学习模型在训练分布与测试分布发生偏移时，性能会显著下降。测试时适应（Test-Time Adaptation, TTA）旨在推理阶段动态调整模型，以应对这类领域偏移。然而，现有主流TTA方法——无论是基于熵最小化的Tent、SAR、EATA，还是基于批归一化校正的CMF——都严重依赖反向传播来更新模型参数或归一化统计量。这一设计带来了两个根本性瓶颈：

1. **高内存占用**：反向传播需要存储中间激活和梯度图，导致内存需求急剧膨胀。例如，SPA和CMF在服务器端的显存占用超过10GB（Table 1），使得它们无法部署在Jetson Orin Nano等仅3.5GB内存的边缘设备上。
2. **高计算延迟**：梯度计算和参数更新增加了每批次的推理时间，难以满足实时应用的低延迟要求。

与此同时，少数尝试摆脱反向传播的方法（如FOA）虽然避免了梯度计算，却引入了新的问题：它们通常针对特定架构设计（FOA仅适用于ViT），且需要多次前向搜索（9或27次），导致延迟依然较高。另一类高效TTA方法（如MECTA、EcoTTA、L-TTA）通过仅更新部分层或使用轻量网络来降低开销，但它们都是CNN专用的，缺乏架构通用性。

这种“反向传播依赖”与“架构特异性”的双重限制，构成了当前TTA方法从服务器向边缘设备迁移的核心障碍。

### 领域偏移的结构化本质：平移、缩放与旋转

本文通过系统分析领域偏移对中间层嵌入的影响，揭示了一个关键观察：**领域偏移在嵌入空间中并非随机扰动，而是呈现三种结构化的几何变化**（Figure 1）：

- **平移（Mean Shift）**：目标域特征的全局中心点相对于源域发生系统性偏移。
- **缩放（Variance Shift）**：目标域特征在各个方向上的离散程度发生变化。
- **旋转（Covariance Shift）**：目标域特征在不同通道之间的相关结构发生扭曲，表现为协方差矩阵的旋转。

这一发现暗示了一个核心洞察：如果能够预存源域的嵌入空间统计量（均值和协方差），那么在测试时，仅需通过几何变换将目标域特征“拉回”源域分布，即可恢复模型性能——整个过程无需修改模型参数，因而也无需反向传播。

### 本文动机：架构无关、无反向传播的嵌入对齐

基于上述观察，本文提出**Progressive Embedding Alignment（PEA）**，一种完全脱离反向传播、且对CNN和Transformer统一适用的测试时适应框架。PEA的核心思想是：通过逐层的白化-着色变换（Whitening-Coloring Transform, WCT），将目标域特征分布渐进地对齐到预存的源域分布，同时引入距离感知的加权机制和指数移动平均（EMA）统计估计，以应对不同程度的领域偏移和极小批次的挑战。

PEA的设计直接回应了现有方法的三个缺口：（1）消除反向传播以降低内存和延迟；（2）统一CNN和ViT的适应流程以实现架构无关性；（3）仅需两次前向传播以保持极低的计算开销。

## 核心创新

PEA 的核心创新在于**将测试时适应从反向传播驱动的参数更新范式，彻底转向仅依赖前向传播的嵌入空间几何对齐**。这一转变解决了现有 TTA 方法的两大瓶颈：反向传播带来的高内存与高延迟，以及方法对特定架构的强依赖。

### 从参数更新到嵌入对齐：消除反向传播

现有 TTA 方法（如 Tent、SAR、EATA、CMF）均需通过反向传播更新模型参数或归一化统计量，导致内存占用极高（SPA 和 CMF 超过 10GB，Table 1）且推理延迟显著。PEA 的核心洞察在于：**领域偏移的本质是中间层嵌入空间的几何变形，而非模型参数本身的问题**。因此，PEA 不修改任何模型参数，而是直接在特征层面进行纠正——通过逐层协方差对齐（白化-着色变换）将目标域特征拉回源域分布。这一设计使 PEA 完全消除了反向传播的需求，在 ViT-Base 上仅需 887MB 内存和 0.31 秒/批的延迟（Table 1），同时保持 64.5% 的 ImageNet-C 精度。

### 架构无关的统一框架

现有高效 TTA 方法普遍局限于特定架构：FOA 专为 ViT 设计（需 9 或 27 次前向搜索），EcoTTA、MECTA、L-TTA 仅适用于 CNN。PEA 通过**仅操作中间层特征**的设计，实现了真正的架构无关性——CNN 和 ViT 使用完全相同的对齐程序，无需任何架构特定的适配。在 CIFAR100-C 上，PEA+Aug 在 ViT 上达到 77.0%，在 ResNet-50 上达到 54.6%，均显著超越同类方法（Table 2）。

### 距离感知的加权对齐策略

PEA 并非对所有层施加均等的对齐强度。其关键设计是通过**第一个前向传播估计每层特征与源域分布的统计距离** $d_l$，并据此计算归一化对齐权重 $w_l$：

$$d_l = \| \pmb{\mu}_{s,l} - \pmb{\mu}_{b,l} \|_2 + \| \pmb{\sigma}_{s,l}^2 - \pmb{\sigma}_{b,l}^2 \|_2$$

$$w_l = \frac{d_l - \min_l d_l}{\max_l d_l - \min_l d_l}$$

在第二个前向传播中，原始特征与对齐特征按权重线性混合：$\pmb{F}_l' = (1 - w_l) \pmb{F}_l + w_l \pmb{Y}_l$。这种**渐进式插值**避免了对偏移轻微层的过度矫正，消融实验表明，加入加权后 ImageNet-C 精度从 25.2% 跃升至 52.9%（Table 6），证实了该机制的关键作用。

### 小批量鲁棒性：EMA 统计估计与尖峰检测

协方差对齐的质量高度依赖目标域统计估计的准确性。PEA 引入**指数移动平均（EMA）跨批次累积统计量**，使方法在极端小批量（batch=1）下仍保持稳定——ImageNet-C 精度 61.6%，CIFAR100-C 精度 69.5%，而 SAR、CMF、FOA 等方法均失效或严重退化（Table 10）。同时，通过**预测熵尖峰检测**（$H_t > E_{\mathrm{ema}} + \theta_{\mathrm{ent}}$）自动识别域突变并重置 EMA 统计，确保方法在混合域场景下的适应性（CIFAR100-C 混合域精度 72.0%，Table 5）。

### 固定两遍前向传播

与 FOA 需要 9 或 27 次前向搜索不同，PEA 将计算成本固定为**每批次仅 2 次前向传播**：第一遍估计对齐权重，第二遍执行对齐与预测。这一固定预算设计使 PEA 的延迟可预测且远低于搜索式方法，在边缘设备 Jetson Orin Nano 上 ViT 延迟 4.1 秒、ResNet 延迟 3.0 秒（Table 5），而 FOA（F=27）的延迟远超此值。

## 整体框架

![[assets/figures/papers/iclr26_0009_7kLNGaAHaw_Architecture-Agnostic_Test-Time_Adaptation_via_B/figures/001_Figure_1.jpg]]
*Figure 1: (a)Translation (Mean Shift) (b) Scaling (Variance Shift) (c) Rotation (Covariance Shift) Figure 1: Impact of domain shift on intermediate layer embeddings. Feature distributions of three classes from block 3 of the ViT model are visualized. Each subfigure illustrates a different type of shift: translation, scaling, and rotation. More experiments can be found in Appendix A*

PEA 的整体工作流分为**离线准备**与**在线适应**两个阶段，在线阶段通过固定的两次前向传播完成全部适应过程，全程无需反向传播或参数更新。

### 离线阶段：源域统计量提取

部署前，PEA 仅需在源域训练集上执行一次前向传播，计算并存储每个模块层 $l$ 的两项关键统计量：均值 $\boldsymbol{\mu}_{s,l}$ 和协方差矩阵 $\boldsymbol{\Sigma}_{s,l}$。这些统计量刻画了源域嵌入空间的几何结构，存储开销极小（ViT-Base 约 30MB），且一次计算后不再需要访问源数据。

### 在线阶段：两次前向传播

**Pass 1 —— 估计对齐权重。** 第一批测试数据进入模型，PEA 在各层提取当前批次的中间特征，计算其均值 $\boldsymbol{\mu}_{b,l}$ 和方差 $\boldsymbol{\sigma}_{b,l}^2$，并与预存的源域统计量比较，得到各层的统计距离 $d_l$：

$$d_l = \| \boldsymbol{\mu}_{s,l} - \boldsymbol{\mu}_{b,l} \|_2 + \| \boldsymbol{\sigma}_{s,l}^2 - \boldsymbol{\sigma}_{b,l}^2 \|_2$$

该距离量化了每层嵌入空间因领域偏移产生的变形程度。随后通过 min-max 归一化将距离映射为对齐权重 $w_l \in [0,1]$：

$$w_l = \frac{d_l - \min_l d_l}{\max_l d_l - \min_l d_l}$$

权重越大，表示该层偏移越严重，需要越强的对齐干预。

**Pass 2 —— 加权特征对齐与预测。** 第二次前向传播中，PEA 在每层执行白化-着色变换（Whitening-Coloring Transform, WCT），将目标域特征拉回源域分布：

$$\boldsymbol{Y}_l = (\boldsymbol{F}_l - \boldsymbol{\mu}_{t,l}) \boldsymbol{\Sigma}_{t,l}^{-1/2} \boldsymbol{\Sigma}_{s,l}^{1/2} + \boldsymbol{\mu}_{s,l}$$

其中 $\boldsymbol{\mu}_{t,l}$ 和 $\boldsymbol{\Sigma}_{t,l}$ 为目标域统计量（由 EMA 跨批次累积估计），$\boldsymbol{\Sigma}^{1/2}$ 和 $\boldsymbol{\Sigma}^{-1/2}$ 通过特征分解高效计算。变换后的特征 $\boldsymbol{Y}_l$ 与原始特征 $\boldsymbol{F}_l$ 按权重混合，避免过度矫正：

$$\boldsymbol{F}_l' = (1 - w_l) \boldsymbol{F}_l + w_l \boldsymbol{Y}_l$$

混合后的特征 $\boldsymbol{F}_l'$ 继续流入后续层，最终输出预测。

### 辅助模块：统计估计与数据增强

**EMA 统计更新。** 为在小批量场景下稳定估计目标域协方差，PEA 使用动量 $m$ 的指数移动平均累积历史批次统计量：

$$\boldsymbol{\mu}_{t,l}^{(i)} = (1 - m) \boldsymbol{\mu}_{t,l}^{(i-1)} + m \boldsymbol{\mu}_{b,l}, \quad \boldsymbol{\Sigma}_{t,l}^{(i)} = (1 - m) \boldsymbol{\Sigma}_{t,l}^{(i-1)} + m \boldsymbol{\Sigma}_{b,l}$$

**域偏移尖峰检测。** 当预测熵 $H_t$ 超出 EMA 熵 $E_{\mathrm{ema}}$ 一个阈值 $\theta_{\mathrm{ent}}$ 时，判定发生域突变，立即重置 EMA 统计量以快速适应新域。

**多视角数据增强与集成。** 对每张测试图像生成 $K$ 个轻量增强视图，在 Pass 2 中对各视图独立执行对齐，最终通过均匀平均 logits 得到集成预测：

$$\mathbf{pred}_{\mathrm{final}} = \frac{1}{K} \sum_{k=1}^{K} \mathbf{logits}_k$$

### 模块关系总结

整个 pipeline 的核心逻辑链为：**源域统计预存 → Pass 1 偏移量化与权重计算 → EMA 统计累积 → Pass 2 逐层 WCT 对齐与加权混合 → 多视图集成预测**。所有模块均在前向传播中完成，不涉及任何梯度计算或参数更新，因此天然适用于 CNN 和 ViT 等异构架构。

## 核心模块与公式推导

### 动机：领域偏移的三种几何变形

在嵌入空间中，领域偏移以三种系统的几何变化形式呈现：平移（均值偏移）、缩放（方差偏移）和旋转（协方差偏移）。Figure 1 的可视化表明，来自偏移域的中间层特征与源域特征之间，始终存在这三种结构性的差异——均值向量的移动、方差的缩放，以及通道间协方差结构的变化。这一观察构成了 PEA 的核心动机：如果能够逐层纠正这三种几何变形，就可以将目标域的特征分布拉回源域分布，而无需修改模型参数。

### 总体流程：两次前向传播

PEA 完全摒弃反向传播，每批次仅需两次前向传播。Pass 1 获取测试批次的中间层特征，估计各层与源域分布的距离，并据此计算对齐权重；Pass 2 利用这些权重，对每层特征执行协方差对齐，最终输出预测。整个过程不更新任何模型参数，且对 CNN 和 ViT 使用完全相同的程序。

### 离线阶段：源域统计量提取

部署前，PEA 使用源域训练数据计算并存储每层的源均值 $\pmb{\mu}_{s,l}$ 和源协方差矩阵 $\pmb{\Sigma}_{s,l}$。对于 ViT-Base，这些统计量仅需约 30MB 存储空间。测试时不再需要访问源数据。

### Pass 1：距离感知的对齐权重估计

第一个前向传播中，PEA 获取测试批次的中间层特征，计算每层 $l$ 的统计距离 $d_l$，以量化该层的领域偏移程度：

$$d_l = \| \pmb{\mu}_{s,l} - \pmb{\mu}_{b,l} \|_2 + \| \pmb{\sigma}_{s,l}^2 - \pmb{\sigma}_{b,l}^2 \|_2$$

其中 $\pmb{\mu}_{b,l}$ 和 $\pmb{\sigma}_{b,l}^2$ 分别为当前批次在第 $l$ 层的均值和方差。该距离同时捕捉了均值偏移和方差偏移两个维度的变化。

为了将原始距离映射为 $[0,1]$ 区间的对齐权重，PEA 对 $d_l$ 进行 min-max 归一化：

$$w_l = \frac{d_l - \min_l d_l}{\max_l d_l - \min_l d_l}$$

$w_l$ 越大，表示该层需要越强的对齐矫正。

### Pass 2：加权特征对齐

第二个前向传播中，PEA 对每层特征执行白化-着色变换（Whitening-Coloring Transform, WCT），将目标域特征映射到源域分布：

$$\pmb{Y}_l = (\pmb{F}_l - \pmb{\mu}_{t,l}) \pmb{\Sigma}_{t,l}^{-1/2} \pmb{\Sigma}_{s,l}^{1/2} + \pmb{\mu}_{s,l}$$

其中 $\pmb{F}_l$ 为当前批次在第 $l$ 层的原始特征，$\pmb{\mu}_{t,l}$ 和 $\pmb{\Sigma}_{t,l}$ 为目标域统计量（通过 EMA 估计，见下文）。变换的核心逻辑是：先用目标域统计量进行白化（去除域特有变化），再用源域统计量进行着色（恢复源域几何结构），从而实现特征分布的对齐。

为避免过度矫正，PEA 根据对齐权重 $w_l$ 将原始特征与对齐后的特征进行线性插值：

$$\pmb{F}_l' = (1 - w_l) \pmb{F}_l + w_l \pmb{Y}_l$$

这种渐进式插值策略确保了对齐强度的自适应调节——偏移严重的层获得更强的矫正，偏移轻微的层则保留更多原始表示。

### 协方差矩阵的平方根计算

WCT 需要计算协方差矩阵的平方根和逆平方根。PEA 采用特征分解来高效、稳定地处理对称半正定矩阵：

$$\Sigma^{1/2} = V \Lambda^{1/2} V^\top, \quad \Sigma^{-1/2} = V \Lambda^{-1/2} V^\top$$

其中 $V$ 为特征向量矩阵，$\Lambda$ 为特征值对角矩阵。

### EMA 统计估计与小批量稳定性

在小批量场景下，单批次的目标域协方差估计极不稳定。PEA 通过指数移动平均（EMA）累积历史批次的统计量来缓解这一问题：

$$\pmb{\mu}_{t,l}^{(i)} = (1 - m) \pmb{\mu}_{t,l}^{(i-1)} + m \pmb{\mu}_{b,l}$$

$$\pmb{\Sigma}_{t,l}^{(i)} = (1 - m) \pmb{\Sigma}_{t,l}^{(i-1)} + m \pmb{\Sigma}_{b,l}$$

其中 $m$ 为动量参数。这使得即使在 batch=1 的极端条件下，PEA 仍能保持稳定性能（ImageNet-C 精度 61.6%，CIFAR100-C 精度 69.5%），而 SAR、CMF、FOA 等基线方法则失效或严重退化。

### 域偏移尖峰检测与重置

当测试流中出现突然的域切换时，EMA 累积的历史统计量可能不再适用。PEA 利用预测熵的尖峰检测机制来应对这一问题：当当前批次的预测熵 $H_t$ 超出 EMA 熵 $E_{\mathrm{ema}}$ 一个阈值 $\theta_{\mathrm{ent}}$ 时，判定发生域突变，随即重置 EMA 统计量：

$$\mathrm{Spike\ if: } H_t > E_{\mathrm{ema}} + \theta_{\mathrm{ent}}$$

该机制使 PEA 能够在混合域流式场景中自适应地丢弃过时统计量，在 CIFAR100-C 混合域评估中达到 72.0% 精度（No Adapt 为 61.6%）。

### 多视角数据增强与集成

为丰富批次统计并提升预测稳定性，PEA 对每张测试图像生成 $K$ 个轻量增强视图。最终预测通过对 $K$ 个视图的 logits 进行均匀平均得到：

$$\mathbf{pred}_{\mathrm{final}} = \frac{1}{K} \sum_{k=1}^{K} \mathbf{logits}_k$$

该增强与集成策略无需额外模型参数或反向传播，在 ImageNet-C 上为 PEA 带来约 2 个百分点的增益（64.5% → 66.5%）。

## 实验与分析

### 核心发现：领域偏移的结构化几何本质

PEA的设计根植于一个关键实证发现：领域偏移在中间层嵌入空间中系统性地表现为三种几何变换——**平移（均值偏移）、缩放（方差偏移）和旋转（协方差偏移）**。Figure 1 的可视化证据显示，在ViT模型的第3层中，不同类别的特征分布在不同腐蚀类型下呈现出明显的均值位移、方差缩放以及通道间协方差结构的旋转。这一观察构成了方法的因果杠杆：如果偏移是结构化的几何变形，那么通过白化-着色变换（Whitening-Coloring Transform, WCT）将目标域特征拉回源域分布，就可以在不修改模型参数的前提下恢复性能。

### 主要实验结果

**ImageNet-C 基准（ViT-Base）**：Table 1 展示了各方法在ImageNet-C上的综合对比。PEA以64.5%的平均准确率显著优于无适应的源模型（55.5%，+9.0个百分点），同时超越了需要反向传播的主流方法SAR（62.0%）和SPA（62.6%）。配合轻量数据增强的PEA+Aug进一步将精度提升至66.5%（+11.0个百分点 vs No Adapt）。更关键的是效率优势：PEA仅消耗887MB显存，每批延迟0.31秒，而SPA和CMF的内存需求超过10GB，无法部署于边缘设备。FOA虽然也无需反向传播，但其27次前向搜索导致延迟高达1.96秒，是PEA的6倍以上。


![[assets/figures/papers/iclr26_0009_7kLNGaAHaw_Architecture-Agnostic_Test-Time_Adaptation_via_B/figures/002_Table_1.jpg]]
*Table 1: Comparison of accuracy (%) on ImageNet-C using ViT-Base and ResNet-50 with memory consumption on server. Aug and BP indicate whether the approaches utilize data augmentation and backpropagation. In FOA, F specifies how many forward passes per batch*

**CIFAR-C 基准**：Table 2 的结果验证了PEA的架构通用性。在CIFAR100-C上，ViT-Base的PEA+Aug达到77.0%，较No Adapt（61.6%）提升15.4个百分点，优于CMF（67.3%）和SPA（70.6%）。在CIFAR10-C上，ResNet-50的PEA+Aug达到83.4%，超过CNN专用方法MECTA（80.7%）和L-TTA（80.6%）。值得注意的是，PEA在ViT和ResNet上使用完全相同的程序，无需架构特定的设计调整。


![[assets/figures/papers/iclr26_0009_7kLNGaAHaw_Architecture-Agnostic_Test-Time_Adaptation_via_B/figures/003_Table_2.jpg]]
*Table 2: Adaptation accuracy (%) on CIFAR10-C and CIFAR100-C using ViT and ResNet*

**混合域场景**：Table 5 展示了更具挑战性的混合域评估（同一批次包含多种腐蚀类型）。PEA在ViT-Base上达到72.0%，较No Adapt（61.6%）提升10.4个百分点，优于CMF（69.0%）和SPA（71.4%）。这表明距离感知加权策略能有效处理不同层面对不同腐蚀类型的差异化偏移。


![[assets/figures/papers/iclr26_0009_7kLNGaAHaw_Architecture-Agnostic_Test-Time_Adaptation_via_B/figures/005_Table_5.jpg]]
*Table 5: Adaptation accuracy (%) on mixed domain on CIFAR100-C dataset*

### 消融实验：各组件的因果贡献

Table 6 的系统消融揭示了PEA各组件的因果作用链条：


![[assets/figures/papers/iclr26_0009_7kLNGaAHaw_Architecture-Agnostic_Test-Time_Adaptation_via_B/figures/007_Table_6.jpg]]
*Table 6: Ablation study of PEA using ViT-Base model on CIFAR100-C and ImageNet-C*

1. **纯协方差对齐（Cov Align Only）**：在CIFAR100-C上仅从61.6%提升至67.0%，而在ImageNet-C上严重退化至25.2%。这表明不加约束的全局对齐在复杂偏移下会破坏有用特征结构，过度矫正问题突出。

2. **+距离感知加权（+Weighting）**：引入权重$w_l$后，ImageNet-C恢复至52.9%，CIFAR100-C提升至68.3%。权重机制通过根据各层偏移程度控制对齐强度，有效缓解了过度矫正。

3. **+EMA统计估计（+Weighting, EMA）**：加入指数移动平均后，性能跃升至CIFAR100-C 75.7%、ImageNet-C 64.5%。EMA通过跨批次累积统计量，显著提升了小批量下协方差估计的稳定性，这是方法在batch=1场景下仍能工作的关键。

4. **+数据增强集成（PEA+Aug）**：最终加入多视角增强与集成，达到CIFAR100-C 77.0%、ImageNet-C 66.5%。增强带来的增益约为1.3–2.0个百分点，主要来自丰富批次统计和集成预测的稳定性提升。

### 小批量与边缘设备鲁棒性

**极端小批量**：Table 10 显示，在batch=1的流式场景下，PEA在ImageNet-C上保持61.6%的精度，CIFAR100-C上保持69.5%，而SAR、CMF、FOA等方法要么失效，要么严重退化。EMA统计积累和尖峰检测机制使得PEA即使在单样本下也能维持合理的协方差估计。


![[assets/figures/papers/iclr26_0009_7kLNGaAHaw_Architecture-Agnostic_Test-Time_Adaptation_via_B/figures/016_Table_10.jpg]]
*Table 10: Results on BS=1 and BS=2 on CIFAR100-C and ImageNet-C with ViT-Base.(“F” indicates that the method fails under BS=1.)*

**边缘设备部署**：在Jetson Orin Nano（3.5GB内存限制）上（Table 4），CMF和SPA因内存不足无法运行，而PEA以1011MB（ViT）和976MB（ResNet）的内存占用成功部署，延迟分别为4.1秒和3.0秒。这验证了PEA在资源受限场景下的实用价值。

### 超参数敏感性分析

Table 11 显示，EMA动量$m$在0.02–0.05范围内、熵阈值$\theta_{\text{ent}}$在0.8–1.0范围内，CIFAR100-C精度波动小于1%（75.0%–75.8%）。方法对超参数不敏感，降低了实际部署的调参成本。尖峰检测机制在域突变时平均触发次数合理，有效防止了统计污染。

### 源数据依赖的轻量性

Table 12 表明，仅使用5–10%的源数据计算离线统计即可接近饱和性能（CIFAR100-C: 76.8% @10% vs 77.0% @100%）。对于ViT-Base，存储所有层的均值和协方差矩阵仅需约30MB，且离线阶段一次计算后测试时不再需要源数据访问。

### 公平性说明

在解读结果时需注意以下几点：(1) PEA+Aug使用了数据增强，而SAR、Tent等基线未使用增强，直接比较时增强贡献约1.3–2.0个百分点；(2) 边缘设备实验受3.5GB内存硬约束，高内存方法无法运行反映了实际部署限制，但可能对资源密集型方法不公平；(3) 各方法的超参数按原作者设置，未进行全局统一微调，可能存在次优配置。

## 方法谱系与知识库定位

### 方法谱系：从反向传播驱动到纯前向对齐

PEA 在测试时适应（TTA）领域占据一个独特的位置——它是**完全无反向传播、架构无关**的方法，这一特征将其与现有工作清晰地划分开来。现有 TTA 方法可沿两条轴定位：

**轴一：是否依赖反向传播。** 主流 TTA 方法——包括 Tent、SAR、EATA、CMF、SPA——均通过反向传播更新模型参数或归一化统计量。这带来了固有的内存和延迟开销：CMF 和 SPA 的内存需求超过 10GB（Table 1），无法部署在 Jetson Orin Nano 等边缘设备（3.5GB 限制）上。MECTA 和 EcoTTA 通过剪枝梯度或轻量元网络降低了部分开销，但仍需反向传播，且局限于 CNN 架构。PEA 完全取消了反向传播，仅需两次前向传播，在 ViT-Base 上内存仅 887MB、延迟 0.31s/批（Table 1）。

**轴二：是否架构通用。** FOA 是少数无反向传播的方法之一，但它专为 ViT 设计，需要 9 或 27 次前向搜索（取决于配置），延迟显著高于 PEA。EcoTTA、MECTA、L-TTA 则仅适用于 CNN。PEA 在 CNN 和 ViT 上使用完全相同的程序，在 CIFAR10-C（ResNet-50）上达到 83.4%，在 CIFAR100-C（ViT-Base）上达到 77.0%（Table 2, Table 7），证明了跨架构的泛化能力。

**核心差异的本质：** PEA 将 TTA 问题从“修改模型参数以适应目标域”重新定义为“纠正嵌入空间的几何变形”。这一视角转换使得方法不再需要梯度计算，而是依赖离线预存的源域统计量（约 30MB for ViT-Base）与在线估计的目标域统计量之间的协方差对齐。消融实验（Table 6）揭示了一个关键瓶颈：纯协方差对齐在 CIFAR100-C 上仅提升至 67.0%，在 ImageNet-C 上甚至崩溃至 25.2%（远低于 No Adapt 的 55.5%）。只有引入距离感知加权、EMA 统计估计和数据增强后，性能才稳定提升至 77.0% 和 66.5%。这表明**对齐本身不是充分的——如何决定对齐强度（加权）和如何稳健估计目标统计（EMA）才是方法成功的关键因果机制**。

### 适用边界与局限

**源数据依赖。** PEA 需要在离线阶段访问源域训练数据以计算各层的均值 $\pmb{\mu}_{s,l}$ 和协方差 $\pmb{\Sigma}_{s,l}$。在完全无法获取源数据的场景下无法直接使用。但消融实验（Table 12）表明，仅使用 5–10% 的源数据即可接近饱和性能（CIFAR100-C: 76.8% @10% vs 77.0% @100%），这显著降低了实际门槛。

**统计估计的脆弱性。** 协方差对齐的质量直接取决于目标域统计估计的准确性。在极端域偏移或极小批次下，EMA 积累不足可能导致对齐失败。尖峰检测与重置机制（基于预测熵阈值 $\theta_{\mathrm{ent}}$）只能部分缓解这一问题——当域切换过于频繁或偏移过于剧烈时，EMA 统计可能在重置后仍需要多个批次才能重新稳定。Table 10 显示 PEA 在 batch=1 时仍保持 61.6%（ImageNet-C）和 69.5%（CIFAR100-C），但相比 batch=64 的 64.5% 和 75.7% 有明显下降。

**任务与偏移类型的限制。** 当前设计针对分类任务和 ImageNet-C / CIFAR-C 中定义的常见图像腐蚀（噪声、模糊、天气、数字变换）。对于目标检测、语义分割等需要保留空间结构的任务，或更复杂的域偏移（如风格迁移、跨模态偏移），PEA 尚未经过验证。逐层协方差对齐本质上是全局特征分布的校正，可能破坏对空间敏感的任务结构。

**超参数的自适应缺失。** EMA 动量 $m$ 和熵阈值 $\theta_{\mathrm{ent}}$ 在合理范围内（$m=0.02$–$0.05$, $\theta_{\mathrm{ent}}=0.8$–$1.0$）对精度影响 <1%（Table 11），表明方法对超参数不敏感。但这两个参数仍需针对新场景手动设定，缺乏根据数据流特性自适应调整的机制。

### 开放问题

1. **跨模态与序列模型的扩展。** 协方差对齐的核心操作——白化-着色变换（WCT）——在数学上不限于图像特征。能否将其应用于语言模型的中间表示层，以应对文本域的分布偏移？序列模型中的位置编码和自注意力结构是否会对协方差对齐产生额外的约束？

2. **自适应权重生成。** 当前对齐权重 $w_l$ 基于手工设计的统计距离 $d_l = \| \pmb{\mu}_{s,l} - \pmb{\mu}_{b,l} \|_2 + \| \pmb{\sigma}_{s,l}^2 - \pmb{\sigma}_{b,l}^2 \|_2$ 和 min-max 归一化。能否学习一个轻量的权重生成网络，以端到端的方式优化各层的对齐强度？这可能在更复杂的域偏移下提供更好的泛化能力。

3. **无源域统计的盲对齐。** 如果完全无法访问源数据，是否可以通过在线聚类或伪标签生成“伪源统计量”来实现盲对齐？这需要解决伪统计量的偏差累积问题，但若能实现，将极大扩展方法的适用范围。

4. **多层对齐的交互机制。** 当前 PEA 独立地对每一层进行对齐，然后通过加权插值与原始特征融合。各层对齐之间存在怎样的交互？是否存在最优的对齐顺序（如从浅层到深层逐步对齐）或稀疏对齐策略（仅对齐偏移最严重的层）？

5. **与持续学习的结合。** PEA 不修改模型参数，这使其天然适合持续变化的域流。能否将 EMA 累积的统计量作为“域记忆”，与知识蒸馏或弹性权重巩固等技术结合，在资源受限设备上实现终生测试时适应？

## 原文 PDF

![[paperPDFs/ICLR_2026/Architecture_Agnostic_Test_Time_Adaptation_via_Backprop_Free_Embedding_Alignment.pdf]]
