---
title: Differentially Private 2D Human Pose Estimation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Differentially_Private_2D_Human_Pose_Estimation.pdf
project_link: "https://bhairava2898.github.io/DP2DHPE/"
code_link: null
aliases:
- FPDS
- DP2HPE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 通过引入两个互补机制——(1)利用公开数据学习梯度主成分子空间并将私有梯度投影到此k维子空间(k≪p)，将隐私误差从O(p·G²)降至O(k·C²)；(2)采用特征差分隐私(FDP)，将原始图像视为私有、高斯模糊图像作为公有特征，仅对私有梯度加噪——从而大幅提升信噪比。
primary_logic: 将梯度更新的有效信号约束在低维流形内，并仅保护真正包含敏感信息的原始像素，实现了隐私-效用权衡的乘法增益。
claims:
- 在MPII数据集上，ε=0.8时，Feature-Projective DP达到82.61% PCKh@0.5，恢复73%隐私性能差距。
- 子空间投影将DP-SGD在ε=0.2、C=0.01下的准确率从63.85%提升至78.48%，接近非隐私上限。
- 在HumanART跨数据集泛化实验中，Feature-Projective DP在ε=0.8时达到51.6 AP，远超DP-SGD的39.0 AP。
- MPII 上 PCKh@0.5 = 82.61%
---

# Differentially Private 2D Human Pose Estimation

> [!tip] 核心洞察
> 将梯度更新的有效信号约束在低维流形内，并仅保护真正包含敏感信息的原始像素，实现了隐私-效用权衡的乘法增益。

| 字段 | 内容 |
|------|------|
| 中文题名 | 差分隐私二维人体姿态估计 |
| 英文题名 | Differentially Private 2D Human Pose Estimation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2504.10190) · [Project](https://bhairava2898.github.io/DP2DHPE/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | Feature-Projective DP-SGD |
| Dataset | MPII, HumanART |

> [!tip] 效果简介
> - MPII 上，PCKh@0.5 82.61% vs 78.17% (DP-SGD, ε=0.8, C=0.01, finetuning) (+4.44%)；PCKh@0.5 78.48% (Projection DP-SGD, ε=0.2, C=0.01, finetuning) vs 63.85% (DP-SGD, same settings) (+14.63%)。
> - HumanART 上，AP 51.6 (Feature-Projective DP, ε=0.8, C=0.01, finetuning) vs 39.0 (DP-SGD, ε=0.8, C=0.01, finetuning) (+12.6)。

## 概述

**核心问题**：在二维人体姿态估计（2D HPE）中引入差分隐私保护时，标准DP-SGD（Abadi et al., 2016）因需对全量参数空间施加高斯噪声，噪声强度与参数维度 $p$ 及梯度范数 $G$ 的乘积成正比，导致关键点定位精度急剧退化——隐私与效用的冲突在高精度细粒度视觉任务中被急剧放大。

**核心方案**：本文提出 **Feature-Projective DP-SGD**，通过两个互补机制实现隐私-效用权衡的乘法增益：
1. **子空间投影**：利用公开数据学习梯度主成分子空间，将私有梯度投影至 $k$ 维子空间（$k \ll p$），将隐私误差从 $\mathcal{O}(p \cdot G^2)$ 降至 $\mathcal{O}(k \cdot C^2)$；
2. **特征差分隐私（FDP）**：将原始图像视为私有、高斯模糊图像作为公有特征，仅对私有梯度裁剪加噪，公有梯度无噪传播。

**核心洞察**：将梯度更新的有效信号约束在低维流形内，并仅保护真正包含敏感信息的原始像素，实现了信噪比的大幅提升。

**主要结果**（MPII数据集，冻结微调策略）：
- 在 $\varepsilon = 0.8$、$C = 0.01$ 设置下，Feature-Projective DP 达到 **82.61% PCKh@0.5**，恢复隐私性能差距的 **73%**；
- 在极端隐私预算 $\varepsilon = 0.2$、$C = 0.01$ 下，子空间投影将 DP-SGD 准确率从 63.85% 提升至 **78.48%**，接近非隐私上限；
- 跨数据集泛化（HumanART）中，$\varepsilon = 0.8$ 时 Feature-Projective DP 达到 **51.6 AP**，远超 DP-SGD 的 39.0 AP。

**方法定位**：该方法属于差分隐私深度学习与视觉表征学习的交叉，针对细粒度结构化输出任务提出梯度空间降维与特征级隐私解耦的双重策略，为隐私保护下的高精度人体感知提供了新的范式。

## 背景与动机

二维人体姿态估计（2D HPE）是计算机视觉的基础任务，广泛应用于人机交互、运动分析和医疗康复等领域。随着深度学习模型的成熟，高精度HPE系统通常需要在大规模人体图像数据集上进行训练，但这些数据往往包含敏感的个人身份信息（如面部、体型、纹身等），直接使用带来显著的隐私泄露风险。差分隐私（Differential Privacy, DP）作为严格的隐私保护框架，本应成为解决这一矛盾的自然选择，然而在实际部署中面临一个根本性瓶颈。

**核心瓶颈：维度灾难下的信噪比崩溃。** 标准的DP-SGD（Abadi et al., 2016）在训练过程中对整个参数空间添加高斯噪声，其噪声强度与参数维度 $p$ 及梯度范数 $G$ 的乘积成正比。在2D HPE任务中，即使是轻量级架构（如TinyViT）的参数维度也高达数百万量级，导致添加的噪声远超过梯度信号本身，关键点定位精度急剧下降。实验表明，在MPII数据集上使用DP-SGD进行微调，即使隐私预算放宽至 $\varepsilon=0.8$，PCKh@0.5也仅能达到78.17%，与非隐私基线之间存在巨大的性能鸿沟。

**现有方法的局限性。** 当前在隐私保护深度学习领域存在两类主要思路，但均未有效解决HPE场景下的效用退化问题。第一类方法通过改进DP-SGD的噪声机制或裁剪策略来减缓性能损失，但本质上仍受限于 $p \cdot G^2$ 的误差尺度，在高维视觉任务中收效甚微。第二类方法尝试利用公开数据辅助训练，如通过知识蒸馏或预训练-微调范式，但这些方法未能从梯度更新的空间结构层面降低隐私噪声的维度影响，隐私-效用权衡的改善有限。此外，特征差分隐私（Feature DP, Leemann et al., 2024）虽然提出将原始图像视为私有、模糊特征视为公有的思想，但单独使用时仍无法充分挖掘梯度空间的低维结构优势。

**本文动机。** 针对上述困境，本文提出一个核心洞察：梯度更新的有效信号天然约束在低维流形内，而隐私噪声却均匀分布在全维空间。若能精确识别并限制梯度更新于该低维子空间，同时仅对真正包含敏感信息的原始像素施加隐私保护，则可以实现隐私-效用权衡的乘法增益。基于这一洞察，本文设计Feature-Projective DP-SGD框架，通过两个互补机制——子空间投影（将隐私误差从 $\mathcal{O}(p \cdot G^2)$ 降至 $\mathcal{O}(k \cdot C^2)$，其中 $k \ll p$）和特征差分隐私（将损失分解为公有特征损失与私有图像损失，仅对后者加噪）——在严格差分隐私保证下大幅提升HPE性能，恢复隐私引入的性能差距的73%。

## 核心创新

本文提出 **Feature-Projective DP-SGD**，通过两个互补的机制革新标准差分隐私训练范式，从根本上缓解隐私噪声对高精度姿态估计的破坏。其核心创新可归纳为三个“changed slots”，即对标准 DP-SGD（Abadi et al., 2016）的三个关键环节的系统性改造。

### 创新一：梯度更新空间的维度压缩——子空间投影

标准 DP-SGD 在完整的 $p$ 维参数空间中对梯度裁剪并注入高斯噪声，噪声方差与参数维度 $p$ 及梯度范数上限 $C$ 的平方成正比，即隐私误差按 $\mathcal{O}(p \cdot C^2)$ 增长。对于姿态估计这类高精度细粒度任务，全空间加噪导致关键点定位性能急剧退化。

本文引入 **Projection DP-SGD**，将梯度更新约束至一个由公开数据学习得到的 $k$ 维主成分子空间（$k \ll p$）：
$$g_{\text{proj}} = (\hat{V}\hat{V}^T) g$$

其中 $\hat{V} \in \mathbb{R}^{p \times k}$ 的列向量来自公开数据集梯度第二矩矩阵 $M(w) = \frac{1}{m}\sum_{i=1}^{m} \nabla l(w,\tilde{z}_i) \nabla l(w,\tilde{z}_i)^T$ 的 top-$k$ 特征向量。投影操作将隐私误差从 $\mathcal{O}(p \cdot C^2)$ 降至 $\mathcal{O}(k \cdot C^2)$，实现了信噪比的**维度增益**。这一设计的因果逻辑是：梯度更新中的有效信号天然位于低维流形内，而各向同性的高斯噪声则均匀分布在全空间中——投影实质上是滤除与任务无关的噪声分量。

### 创新二：隐私加噪粒度的语义解耦——特征差分隐私

标准 DP-SGD 对整幅图像计算出的梯度统一施加隐私保护，不区分像素的敏感性。本文借鉴 **Feature DP**（FDP, Leemann et al., 2024）的思想，将训练损失分解为私有部分与公有部分：
$$l(w, x) = l_{\text{priv}}(w, x) + l_{\text{pub}}(w, \psi(x))$$

其中 $\psi(\cdot)$ 为高斯模糊映射，将原始图像 $x$ 转化为公有特征。**仅对私有梯度进行裁剪和加噪**，公有特征梯度则保持无噪状态：
$$g_{\text{priv}}^t = \frac{1}{|B_{\text{priv}}^t|} \left( \sum_{x \in B_{\text{priv}}^t} \tilde{g} + \mathcal{N}(0, \sigma^2 C^2 I) \right)$$

这一设计的核心洞察是：高斯模糊后的图像已剥离了大部分身份敏感信息，但其空间结构仍能为关键点定位提供强监督信号。通过将隐私预算精准聚焦于真正包含敏感信息的原始像素，实现了**语义粒度的隐私-效用解耦**。

### 创新三：梯度组合策略的混合融合

前两项创新分别从空间维度和语义维度降低噪声影响，本文进一步设计了混合梯度融合策略，将二者的优势乘法叠加：
$$g_t = g_{\text{pub}}^t + g_{\text{proj}}^t$$

其中 $g_{\text{pub}}^t$ 是无噪的公有特征梯度，$g_{\text{proj}}^t$ 是经子空间投影去噪后的私有梯度。最终参数更新同时受益于：
- **公有梯度**提供的稳定、无噪的定位信号；
- **投影私有梯度**在低维子空间内保留的精细调整能力。

理论收敛上界（Eq.13）揭示了这一设计的乘法增益本质：
$$\frac{1}{T}\sum_{t=1}^T\mathbb{E}\|\nabla \hat{L}_n(w_t)\|_2^2 \le \tilde{\mathcal{O}}\left(\frac{k \cdot \rho \cdot C^2}{n\varepsilon}\right) + \mathcal{O}\left(\frac{\Lambda G^4 \rho^2 \gamma_2^2 \ln p}{m}\right)$$

第一项为隐私误差，由子空间维度 $k$ 而非全参数维度 $p$ 控制；第二项为公开数据引入的重构误差，随公开样本量 $m$ 增大而衰减。两项误差可独立控制，为隐私-效用权衡提供了两个正交的调节旋钮。

### 创新间的协同机制

消融实验（Section 4.2.4, Table 6）系统验证了三个 changed slots 的协同效应：
- **单独投影**（Projection DP-SGD）在低隐私预算下提升尤为显著——$\varepsilon=0.2$、$C=0.01$ 时 PCKh@0.5 从 63.85% 跃升至 78.48%；
- **单独 FDP** 在更小的裁剪阈值 $C$ 下表现更稳定，因其公有梯度不受裁剪和加噪影响；
- **二者结合**（Feature-Projective DP）在所有隐私预算和训练策略下均取得最优性能，在 $\varepsilon=0.8$ 时达到 82.61% PCKh@0.5，恢复了 73% 的隐私性能差距。

这种乘法增益的本质在于：投影从**空间维度**压缩噪声方差，FDP 从**语义维度**减少需要加噪的梯度总量——二者作用于隐私-效用权衡的不同环节，形成互补而非冗余。

## 整体框架

本文提出 **Feature-Projective DP-SGD**，一个面向二维人体姿态估计的差分隐私训练框架。该框架将隐私保护机制深度嵌入模型训练流程，通过两个互补的模块——**子空间投影去噪**和**特征差分隐私损失分解**——协同降低差分隐私噪声对关键点定位精度的损害。

### 架构总览

整个 pipeline 以 **TinyViT** 高效分层视觉 Transformer 为骨干网络，后接 **Coordinate Classification Head** 将连续坐标量化后转为分类任务，输出精确的关键点位置（见 Figure 1）。训练过程中，数据流被分为三条路径：

![[assets/figures/papers/paper_list_l1013_https_arxiv_org_abs_2504_10190/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our private HPE pipeline coupling a TinyViT based backbone with Coordinate Classification Keypoint head. The Public feature batch*

1. **私有路径（红色箭头）**：原始图像作为隐私数据，经 TinyViT 提取特征后计算私有损失 `l_priv`，对应的梯度经过裁剪和加噪，再投影到由公开数据学习的低维子空间以滤除噪声。
2. **公有特征路径（绿色箭头）**：同一批私有图像经高斯模糊函数 `ψ` 生成公有特征，计算无噪公有损失 `l_pub` 及其梯度。
3. **投影子空间更新路径（蓝色虚线箭头）**：独立的公开图像集定期输入网络，计算梯度并估计其主成分子空间，为私有梯度提供投影基矩阵。

最终，无噪公有梯度与投影降噪后的私有梯度相加，形成混合更新方向 `g_t = g_pub^t + g_proj^t`，驱动 SGD 参数更新。

### 核心模块关系

| 模块 | 功能 | 数据依赖 |
|------|------|----------|
| TinyViT Backbone | 分层特征提取 | 私有原始图像 + 公有模糊图像 |
| Coordinate Classification Head | 坐标量化分类 | Backbone 输出特征 |
| Subspace Projection | 估计梯度主成分子空间，投影去噪 | 独立公开数据集 |
| Feature DP Loss Decomposition | 拆分损失为私有/公有部分 | 私有图像 + 公有模糊特征 |
| Hybrid Gradient Merging | 合并公有梯度与投影私有梯度 | 两条梯度路径的输出 |

### 隐私-效用权衡机制

标准 DP-SGD 的隐私误差与参数维度 `p` 及梯度范数 `G` 的平方成正比，在高精度姿态估计任务中导致性能崩溃。Feature-Projective DP-SGD 通过两个“旋钮”同时压缩这一误差：

- **子空间投影**将梯度更新约束至由公开数据学习的 `k` 维主成分子空间（`k ≪ p`），使隐私误差从 `O(p·G²)` 降至 `O(k·C²)`，其中 `C` 为梯度裁剪阈值。
- **特征差分隐私**将原始图像定义为私有、高斯模糊图像定义为公有，仅对私有梯度添加噪声，公有梯度保持无噪，从而大幅提升信噪比。

两种机制产生**乘法增益效应**：子空间投影降低噪声维度，特征 DP 减少需加噪的梯度分量，二者叠加使模型在严格隐私预算下仍能逼近非隐私性能上限。收敛分析（Eq. 13）表明，期望梯度范数上界由两项主导——隐私误差项 `O(k·ρ·C²/(nε))` 和公开数据集重构误差项 `O(ΛG⁴ρ²γ₂² ln p / m)`，前者因 `k ≪ p` 而显著降低，后者随公开数据量 `m` 增大而衰减。

## 核心模块与公式推导

Feature-Projective DP-SGD 的核心架构由三个相互耦合的模块构成：**子空间投影去噪**、**特征差分隐私损失分解**与**混合梯度合并**。这三个模块协同作用，将隐私保护下的梯度更新信号约束在低维有效流形内，实现隐私-效用权衡的乘法增益。

### 差分隐私随机梯度下降（DP-SGD）基础

标准 DP-SGD（Abadi et al., 2016）对每个训练样本的梯度进行 L2 范数裁剪（阈值为 $C$），并在聚合梯度上添加高斯噪声以保障 $(\varepsilon, \delta)$-差分隐私。其核心操作可表示为：

$$g = \frac{1}{B}\left( \sum_{i\in B} \tilde{g}_i + \mathcal{N}(0, \sigma^2 C^2 \mathbf{I}) \right)$$

其中 $\tilde{g}_i$ 为裁剪后的单样本梯度，$B$ 为批次大小，$\sigma$ 为噪声乘子，由隐私预算 $(\varepsilon, \delta)$ 决定。该机制的根本瓶颈在于：噪声方差与参数维度 $p$ 及梯度范数上界 $G$ 的乘积成正比，即隐私误差为 $\mathcal{O}(p \cdot G^2)$。在人体姿态估计这类高精度定位任务中，该误差直接导致关键点定位性能急剧下降。

### 模块一：子空间投影去噪

该模块的核心思想是：利用公开数据集学习梯度更新的主成分子空间，将全量 $p$ 维梯度投影至 $k$ 维子空间（$k \ll p$），从而将隐私误差从 $\mathcal{O}(p \cdot G^2)$ 降至 $\mathcal{O}(k \cdot C^2)$。

**梯度第二矩矩阵估计**：首先在公开数据集 $\{\tilde{z}_i\}_{i=1}^m$ 上计算梯度外积的平均，构建 $p \times p$ 矩阵：

$$M(w) = \frac{1}{m}\sum_{i=1}^{m} \nabla l(w,\tilde{z}_i) \nabla l(w,\tilde{z}_i)^T$$

对该矩阵进行特征分解，取前 $k$ 个最大特征值对应的特征向量构成投影矩阵 $\hat{V} \in \mathbb{R}^{p \times k}$。

**子空间投影操作**：将 DP-SGD 产生的含噪梯度 $g$ 投影到该子空间，滤除正交方向上的噪声分量：

$$g_{proj} = (\hat{V}\hat{V}^T) g$$

投影矩阵 $\hat{V}\hat{V}^T$ 作为低通滤波器，保留梯度中与公开数据分布一致的有效信号成分，同时抑制随机噪声。该模块在极低隐私预算（$\varepsilon=0.2$）下尤为关键——单独使用时即可将 PCKh@0.5 从标准 DP-SGD 的 63.85% 提升至 78.48%（MPII 数据集，微调策略，$C=0.01$）。

### 模块二：特征差分隐私损失分解

该模块借鉴特征差分隐私（Feature DP, Leemann et al., 2024）的思想，通过定义公有特征映射函数 $\psi$ 将训练损失拆解为私有部分与公有部分。

**公有特征映射**：对原始图像 $x$ 施加高斯模糊，得到公有特征 $\psi(x)$。模糊操作去除了细粒度纹理等身份敏感信息，同时保留了人体姿态的结构性特征。

**损失分解**：总损失函数被显式拆分为两项：

$$l(w, x) = l_{priv}(w, x) + l_{pub}(w, \psi(x))$$

其中 $l_{priv}$ 作用于原始私有图像，需进行梯度裁剪和加噪；$l_{pub}$ 作用于公有模糊特征，其梯度可无噪使用。这一分解使得模型能够从公有特征中自由学习姿态结构先验，而仅对真正包含敏感信息的原始像素梯度施加隐私保护。

### 模块三：混合梯度合并

该模块将上述两个机制整合为统一的参数更新规则。在每个训练步骤 $t$：

1. **私有梯度计算**：对私有批次 $B_{priv}^t$ 中的原始图像计算 $l_{priv}$ 的梯度，经裁剪后添加高斯噪声：

$$g_{priv}^t = \frac{1}{|B_{priv}^t|} \left( \sum_{x \in B_{priv}^t} \tilde{g} + \mathcal{N}(0, \sigma^2 C^2 \mathbf{I}) \right)$$

2. **子空间投影去噪**：将含噪私有梯度投影至由公开数据估计的子空间：

$$g_{proj}^t = (\hat{V}_t \hat{V}_t^T) g_{priv}^t$$

3. **公有梯度计算**：对公有批次 $B_{pub}^t$（由 $B_{priv}^t$ 经 $\psi$ 变换得到）计算 $l_{pub}$ 的梯度 $g_{pub}^t$，该梯度不加噪声。

4. **最终梯度合并**：

$$g_t = g_{pub}^t + g_{proj}^t$$

模型参数沿 $g_t$ 方向更新。该合并策略实现了双重增益：公有梯度提供稳定的姿态结构引导，投影去噪后的私有梯度补充细粒度定位信息，两者互补大幅提升信噪比。

### 收敛性分析

论文给出了期望梯度范数的上界，揭示了方法的理论保障：

$$\frac{1}{T}\sum_{t=1}^T\mathbb{E}\|\nabla \hat{L}_n(w_t)\|_2^2 \le \tilde{\mathcal{O}}\left(\frac{k\cdot\rho\cdot C^2}{n\varepsilon}\right) + \mathcal{O}\left(\frac{\Lambda G^4 \rho^2 \gamma_2^2 \ln p}{m}\right)$$

上界由两项构成：
- **第一项（隐私误差）**：由子空间维度 $k$、梯度范数界 $C$ 和隐私预算 $\varepsilon$ 共同决定。相比标准 DP-SGD 中与全维度 $p$ 成正比，此处仅与 $k$ 成正比（$k \ll p$），体现了子空间投影的降噪收益。
- **第二项（重构误差）**：源于公开数据集与私有数据集之间的分布差异，由公开数据量 $m$ 和分布偏移参数 $\gamma_2$ 控制。当公开数据充分且与私有数据分布相似时，该项可被有效压制。

该上界从理论上解释了 Feature-Projective DP-SGD 的乘法增益来源：子空间投影降低隐私误差的维度因子，特征差分隐私通过公有梯度减少对噪声梯度的依赖，两者共同收紧收敛界。

## 实验与分析

### 实验设置概述

实验在两个二维人体姿态估计数据集上进行：**MPII**（单人姿态基准）和 **HumanART**（合成数据集，用于跨数据集泛化验证）。模型架构统一采用 TinyViT 骨干网络配合 Coordinate Classification 头部，所有方法均使用 COCO 预训练权重初始化。实验覆盖三种训练策略：**冻结微调**（仅训练头部）、**全微调**（训练全部参数）和**从头训练**，在每个隐私预算 ε 和梯度裁剪阈值 C 的组合下进行系统对比。隐私参数 δ 固定为 4×10⁻⁵。

公平性保障措施包括：公开数据集 COCO 仅用于预训练和计算投影矩阵，私有训练集 MPII/HumanART 严格隔离；所有对比方法使用相同的模型容量和预训练起点；每个 (ε, C) 组合下独立评估。

### 非隐私基线性能

Table 1 展示了模型在 MPII 数据集上的非隐私基线结果。全微调策略下，模型在原始图像上达到 **89.36%** 的平均 PCKh@0.5，在公有特征（高斯模糊图像）上达到 **88.49%**；冻结微调策略下分别为 87.79% 和 87.64%。从头训练时性能显著下降，原始图像上为 80.68%，公有特征上仅为 17.99%。这些结果确立了隐私保护方法的性能上界，并表明公有特征在微调场景下保留了足够的姿态信息，但不足以支撑从头训练。

![[assets/figures/papers/paper_list_l1013_https_arxiv_org_abs_2504_10190/figures/004_Table_1.jpg]]
*Table 1: MPII Results: Non-Private Baselines for our HPE model on the MPII dataset*

### 主实验结果

#### MPII 数据集上的核心发现

**Table 3** 展示了标准 DP-SGD 在 MPII 上的完整结果。在冻结微调、ε=0.8、C=0.01 设置下，DP-SGD 达到 78.17% PCKh@0.5，相比非隐私上限（87.79%）存在约 9.6 个百分点的隐私性能差距。当隐私预算收紧至 ε=0.2 时，性能急剧下降至 63.85%（C=0.01），揭示出标准 DP-SGD 在高精度姿态估计任务中的根本瓶颈——全参数空间加噪导致关键点定位精度严重退化。

**Table 4** 展示了引入子空间投影后的结果（Projection DP-SGD）。在相同 ε=0.2、C=0.01 设置下，投影方法达到 **78.48%**，相比 DP-SGD 的 63.85% 提升了 **+14.63 个百分点**，几乎恢复到非隐私微调水平。这一结果直接验证了核心因果机制：将梯度更新限制在 k 维主成分子空间内，将隐私误差从 O(p·G²) 降至 O(k·C²)，其中 k≪p。

**Table 5** 展示了单独使用特征差分隐私（Feature DP）的结果。Feature DP 在所有设置下均优于标准 DP-SGD，且在更小的裁剪阈值 C 下表现更稳定，验证了仅对私有原始图像梯度加噪、公有模糊特征梯度保持无噪的策略有效性。

**Table 6** 展示了结合两种机制的 Feature-Projective DP 完整结果。在 ε=0.8、C=0.01、冻结微调设置下，该方法达到 **82.61%** PCKh@0.5，相比 DP-SGD 的 78.17% 提升 **+4.44 个百分点**，恢复约 **73%** 的隐私性能差距。在更严格的隐私预算下，增益更为显著——这证实了子空间投影与特征差分隐私之间存在乘法增益效应，而非简单的加法叠加。

#### HumanART 跨数据集泛化

**Table 7–10** 展示了在 HumanART 数据集上的跨数据集泛化结果。在 ε=0.8、C=0.01、冻结微调设置下，Feature-Projective DP 达到 **51.6 AP**，远超 DP-SGD 的 39.0 AP（**+12.6 AP**）。即使在全微调和从头训练策略下，该方法仍保持一致的性能优势。这一结果证明所提方法不依赖于私有训练集与公开数据集之间的特定分布匹配，具有较强的泛化能力。

Figure 2 和 Figure 3 分别以可视化方式汇总了 MPII 和 HumanART 上各方法在不同 (ε, C) 组合下的性能对比，直观展示了 Feature-Projective DP 在所有设置下的统治性优势。

![[assets/figures/papers/paper_list_l1013_https_arxiv_org_abs_2504_10190/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of PCKh@0.5 on MPII dataset across private and non-private methodologies under different training strategies with varied privacy budget (ε) and clipping thresholds (C).1*

![[assets/figures/papers/paper_list_l1013_https_arxiv_org_abs_2504_10190/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of AP on HumanART dataset across private and non-private methodologies under different training strategies with varied privacy budget (ε) and clipping thresholds (C).1*

### 消融实验分析

消融实验通过分别评估 Projection DP-SGD 和 Feature DP 的独立贡献，系统解耦了两种机制的效应：

1. **子空间投影的独立贡献**（Table 4 vs Table 3）：在低隐私预算（ε≤0.5）下，投影带来的提升最为显著（+10 至 +15 个百分点），验证了理论分析中隐私误差由 k 而非 p 主导的结论。在高 ε 下，提升幅度缩小但仍保持正向，表明投影子空间的表示能力在接近非隐私性能时可能成为新的瓶颈。

![[assets/figures/papers/paper_list_l1013_https_arxiv_org_abs_2504_10190/figures/007_Table_3.jpg]]
*Table 3: MPII Results: DP-SGD*

![[assets/figures/papers/paper_list_l1013_https_arxiv_org_abs_2504_10190/figures/008_Table_4.jpg]]
*Table 4: MPII Results: DP-SGD with Projection*

2. **特征差分隐私的独立贡献**（Table 5 vs Table 3）：Feature DP 的优势在于其对裁剪阈值 C 的鲁棒性——当 C 从 0.1 降至 0.01 时，标准 DP-SGD 性能急剧下降，而 Feature DP 的衰减更为平缓。这是因为公有特征梯度不受裁剪和加噪影响，为模型提供了稳定的学习信号。

![[assets/figures/papers/paper_list_l1013_https_arxiv_org_abs_2504_10190/figures/010_Table_5.jpg]]
*Table 5: MPII Results: Feature DP*

3. **乘法增益验证**（Table 6 vs Tables 4, 5）：Feature-Projective DP 在所有 (ε, C, 训练策略) 组合下均优于任一单独机制，且增益幅度大于两独立增益之和的简单叠加。这证实了两种机制作用于互补的误差来源：投影降低参数空间维度的噪声方差，特征 DP 降低需要加噪的梯度分量数量。

![[assets/figures/papers/paper_list_l1013_https_arxiv_org_abs_2504_10190/figures/009_Table_6.jpg]]
*Table 6: MPII Results: Feature Projective DP*

### 定性结果分析

Figure 4 和 Figure 5 展示了定性对比结果。在 ε=0.5、C=0.1 的冻结微调设置下：
- 标准 DP-SGD 的关键点预测存在明显的位置偏移和关节错位，尤其在四肢末端（手腕、脚踝）等细粒度位置误差显著。
- Projection DP-SGD 的预测更为稳定，关节结构保持完整，但在极端姿态下仍存在局部偏移。
- Feature-Projective DP 的预测最接近真实标注，即使在低隐私预算下也能保持关节间的几何一致性。

![[assets/figures/papers/paper_list_l1013_https_arxiv_org_abs_2504_10190/figures/005_Figure_4.jpg]]
*Figure 4: Depiction of qualitative results on DP-SGD, Projection DP-SGD and Feature Projection DP-SGD. We specifically show results on Finetuning with C = 0.1 at various privacy budgets*

![[assets/figures/papers/paper_list_l1013_https_arxiv_org_abs_2504_10190/figures/015_Figure_5.jpg]]
*Figure 5: Figures (a-e)Depiction of qualitative results on DP-SGD, Projection DP-SGD and Feature Projection DP-SGD. We specifically show results on Finetuning with C = 0.1 at various privacy budgets. (f) Representation of Raw (Private) image compared to public feature (gaussian blurred)*

Figure 5(f) 展示了原始私有图像与高斯模糊公有特征的对比，直观说明了公有特征如何在不泄露身份信息的前提下保留足够的姿态结构信息。

### 失败模式与局限性

1. **极端隐私预算下的性能退化**：当 ε≤0.2 时，即使 Feature-Projective DP 的性能也显著低于非隐私基线，表明当前方法在极高隐私要求场景下仍有较大提升空间。

2. **域差异敏感性**：方法性能依赖于公开数据集（COCO）与私有数据集之间的分布相似性。若两者域差异较大（如从自然图像迁移到医学图像），投影子空间的代表性可能减弱，需手动验证。

3. **公有特征映射的局限性**：高斯模糊作为公有特征映射函数简单直接，但在理论上可能仍泄露部分纹理信息。论文未探索其他公有特征映射函数（如边缘检测、姿态关键点热图等）的潜力。

4. **超参数敏感性**：子空间维度 k、模糊核大小等超参数需要针对具体任务调整，论文未提供自适应选择策略。k 值过小会限制表示能力，过大则削弱降噪效果，存在任务相关的隐私-效用权衡最优点。

5. **任务范围限制**：当前验证仅限于 2D 单人姿态估计，尚未扩展到多人场景、3D 姿态估计或视频上下文。在这些更复杂的设置中，梯度子空间的结构可能发生根本变化，需要进一步研究。

### 收敛性分析验证

理论收敛上界（Eq.13）表明，期望梯度范数由两项主导：第一项 $\tilde{\mathcal{O}}(k \cdot \rho \cdot C^2 / (n \varepsilon))$ 为隐私误差，由子空间维度 k 和裁剪阈值 C 控制；第二项 $\mathcal{O}(\Lambda G^4 \rho^2 \gamma_2^2 \ln p / m)$ 为公开数据集引入的重构误差。实验结果与理论预测一致：增大公开数据集规模 m 可降低重构误差，降低 k 可减小隐私误差，但过小的 k 会增加重构误差——这解释了消融实验中 k 值选择的非单调效应。

### 补充图表

![[assets/figures/papers/paper_list_l1013_https_arxiv_org_abs_2504_10190/figures/013_Table_10.jpg]]
*Table 10: HumanART Results: Feature Projection DP-SGD plus projection*

![[assets/figures/papers/paper_list_l1013_https_arxiv_org_abs_2504_10190/figures/011_Table_7.jpg]]
*Table 7: HumanART Results: DP-SGD*

## 方法谱系与知识库定位

### 差分隐私深度学习训练范式的演进

本文提出的 **Feature-Projective DP-SGD** 处于差分隐私深度学习训练方法的演进脉络中，其核心创新在于同时从梯度更新空间和隐私加噪粒度两个维度突破标准DP-SGD的瓶颈。

**标准DP-SGD**（Abadi et al., 2016）是当前隐私保护深度学习的事实标准，其机制是对每个样本的梯度进行L2范数裁剪（阈值C），然后对聚合梯度添加高斯噪声 $\mathcal{N}(0, \sigma^2 C^2 \mathbf{I})$ 以满足 $(\varepsilon, \delta)$-DP 保证。然而，在人体姿态估计这类高精度细粒度任务中，DP-SGD面临根本性困境：噪声强度与参数维度 $p$ 及梯度范数 $G$ 的乘积成正比，当 $p$ 高达数百万时，信噪比急剧恶化，导致关键点定位精度大幅下降——在MPII数据集上，$\varepsilon=0.8$ 时DP-SGD仅达78.17% PCKh@0.5，与非隐私上限（89.36%）之间存在巨大差距。

### 子空间投影DP-SGD：降维降噪

**Projection DP-SGD** 是本文引入的第一个关键消融组件，其思想源于利用公开数据学习梯度更新的低维结构。具体而言，该方法通过公开数据集 $\tilde{z}$ 估计梯度的第二矩矩阵 $M(w) = \frac{1}{m}\sum_{i=1}^{m} \nabla l(w,\tilde{z}_i) \nabla l(w,\tilde{z}_i)^T$，提取其前 $k$ 个主成分构成投影矩阵 $\hat{V}$，然后将DP-SGD产生的全量噪声梯度投影到此 $k$ 维子空间：$g_{proj} = (\hat{V}\hat{V}^T) g$。这一操作将隐私噪声的有效维度从 $p$ 降至 $k$（$k \ll p$），理论收敛上界中的隐私误差项从 $\mathcal{O}(p \cdot G^2)$ 降至 $\mathcal{O}(k \cdot C^2)$。实验验证了这一机制的有效性：在 $\varepsilon=0.2, C=0.01$ 的极端隐私设置下，Projection DP-SGD将DP-SGD的63.85% PCKh@0.5 提升至78.48%，提升幅度达14.63个百分点（Section 4.2.3, Table 4）。

### 特征差分隐私（Feature DP）：粒度解耦

**Feature DP (FDP)**（Leemann et al., 2024）是本文引入的第二个关键组件，其核心思想是将隐私保护从“整个模型参数”下沉到“敏感特征”层面。FDP利用特征映射函数 $\psi$ 将原始训练图像 $x$ 分解为私有部分（原始图像）和公有部分（高斯模糊特征 $\psi(x)$），将总损失拆解为 $l(w, x) = l_{priv}(w, x) + l_{pub}(w, \psi(x))$。在训练中，仅对私有梯度进行裁剪和加噪，而公有梯度保持无噪状态直接用于更新。这一设计使得模型可以自由利用非敏感的关节结构信息，同时仅对可能泄露身份信息的原始像素施加隐私保护。消融实验表明，单独使用Feature DP在大多数隐私预算下均优于标准DP-SGD，且在更小的裁剪阈值 $C$ 下表现更为稳定（Section 4.2.4, Table 5）。

### Feature-Projective DP：乘法增益的融合

本文的完整方案 **Feature-Projective DP-SGD** 将上述两种机制有机融合，形成双重降噪架构：

1. **梯度分解**：将每轮迭代的梯度拆分为公有梯度 $g_{pub}^t$（来自高斯模糊特征，无噪）和私有梯度 $g_{priv}^t$（来自原始图像，经裁剪加噪）。
2. **私有梯度投影**：对 $g_{priv}^t$ 施加子空间投影 $g_{proj}^t = (\hat{V}_t \hat{V}_t^T) g_{priv}^t$，进一步滤除噪声。
3. **混合合并**：最终更新方向为 $g_t = g_{pub}^t + g_{proj}^t$，结合无噪结构信号与降噪后的细节信号。

理论分析给出了该方法的收敛上界（Eq.13）：
$$\frac{1}{T}\sum_{t=1}^T\mathbb{E}\|\nabla \hat{L}_n(w_t)\|_2^2 \le \tilde{\mathcal{O}}\left(\frac{k \cdot \rho \cdot C^2}{n\varepsilon}\right) + \mathcal{O}\left(\frac{\Lambda G^4 \rho^2 \gamma_2^2 \ln p}{m}\right)$$

第一项为隐私误差，由子空间维度 $k$ 和裁剪阈值 $C$ 共同控制；第二项为公开数据集引入的子空间重构误差。这一上界揭示了方法的核心权衡：$k$ 越小则隐私误差越小，但重构误差可能增大，需要根据公开数据与私有数据的分布相似性进行调节。

实验充分验证了两种机制的乘法增益效应。在MPII数据集上，Feature-Projective DP在 $\varepsilon=0.8, C=0.01$ 的微调设置下达到82.61% PCKh@0.5，相比DP-SGD的78.17%提升4.44个百分点，恢复了73%的隐私性能差距（Abstract, Table 6）。在跨数据集泛化实验中（HumanART），该方法在 $\varepsilon=0.8$ 时达到51.6 AP，远超DP-SGD的39.0 AP（Section 4.3, Table 10），证明了其在不同数据分布下的鲁棒性。

### 适用边界与局限

尽管Feature-Projective DP-SGD展现了显著的隐私-效用权衡改进，其适用边界存在以下约束：

1. **任务范围限制**：当前验证仅限于2D单人姿态估计（MPII、HumanART数据集），尚未扩展到3D姿态估计、多人场景或视频时序上下文。在这些更复杂的设置中，梯度子空间的结构可能发生根本变化，方法的有效性需要进一步验证。

2. **公开数据依赖**：子空间投影的质量高度依赖于公开数据集与私有数据集之间的分布相似性。当两者域差异较大时（例如公开数据为自然场景、私有数据为医学影像），投影子空间的代表性可能显著减弱，导致重构误差项 $\mathcal{O}\left(\frac{\Lambda G^4 \rho^2 \gamma_2^2 \ln p}{m}\right)$ 增大，削弱降噪效果。

3. **特征映射的隐私充分性**：高斯模糊作为公有特征映射 $\psi$ 虽然简单直接，但在理论上可能仍泄露部分身份相关信息（如体型轮廓、肤色分布等）。在极端隐私需求场景（如医疗数据）下，需要更强的公有特征映射函数来确保身份信息的充分解耦。

4. **极端隐私预算下的性能瓶颈**：在 $\varepsilon \le 0.2$ 的极端隐私设置下，即使使用完整方法，性能仍然有限。此时隐私误差项 $\tilde{\mathcal{O}}(k \cdot \rho \cdot C^2 / n\varepsilon)$ 的主导作用使得进一步降低 $k$ 或 $C$ 的边际收益递减。

5. **超参数敏感性**：子空间维度 $k$、模糊核大小、投影矩阵更新频率等超参数需要针对具体任务进行调优，论文未提供自适应的选择策略。特别是 $k$ 的选择涉及隐私误差与重构误差的精细平衡，目前缺乏理论指导。

### 开放问题

1. **自适应子空间维度选择**：如何根据网络层级、训练阶段和任务特性自动确定最优的 $k$ 值？不同层的梯度可能具有不同的本征维度，逐层定制投影子空间可能进一步提升性能。

2. **更优的公有特征映射**：除高斯模糊外，哪些特征映射函数 $\psi$ 能更有效地解耦身份信息与姿态关键点？可能的候选包括边缘检测、姿态归一化、或基于学习的解耦表示。这直接关系到方法在更严格隐私定义下的合规性。

3. **复杂场景鲁棒性**：方法在严重遮挡、极端姿态、低分辨率、光照变化等真实世界挑战下的表现如何？这些因素可能同时影响私有梯度的信噪比和公有特征的质量，需要系统性评估。

4. **$\delta$ 参数的影响分析**：论文固定 $\delta = 4 \times 10^{-5}$，但未讨论该选择的理论依据或对不同 $\delta$ 值的敏感度。在差分隐私理论中，$\delta$ 通常应小于数据集大小的倒数，其取值可能影响噪声尺度和最终性能。

5. **跨任务泛化能力**：该框架能否推广到其他细粒度视觉任务（如人脸关键点检测、医学图像分割、细粒度分类）并保持类似的乘法增益？这需要验证梯度子空间假设在不同任务结构下的普适性。

6. **与差分隐私合成数据方法的对比**：近年来，基于生成模型的隐私保护方法（如DP扩散模型生成合成训练数据）在部分视觉任务上展现了竞争力。Feature-Projective DP与这类方法的相对优劣势尚待系统比较。

## 原文 PDF

![[paperPDFs/CVPR_2026/Differentially_Private_2D_Human_Pose_Estimation.pdf]]