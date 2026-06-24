---
title: Confusion-Aware Spectral Regularizer for Long-Tailed Recognition
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Confusion_Aware_Spectral_Regularizer_for_Long_Tailed_Recognition.pdf
project_link: null
code_link: "https://github.com/misswayguy/CAR"
aliases:
- CASRC
- CASRLTR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 频率加权的混淆矩阵的谱范数
primary_logic: 基于PAC-Bayesian理论，推导出最差类别误差的上界由加权经验混淆矩阵的谱范数和一个模型复杂度项控制。通过最小化这个谱范数（CAR正则项），可以直接抑制类间混淆，提高尾部类别的泛化能力。
claims:
- PAC-Bayesian上界证明最差类别误差可由加权混淆矩阵的谱范数约束
- 在ImageNet-LT上，CAR+ConCutMix将整体准确率从56.20%提升至60.07%，尾部准确率从32.73%提升至38.07%
- CAR显著提升最差类别准确率，ImageNet-LT上从10%提升至22%，CIFAR100-LT上从8%提升至18%
- ImageNet-LT 上 Top-1 Accuracy Overall (%) = 60.07
---

# Confusion-Aware Spectral Regularizer for Long-Tailed Recognition

> [!tip] 核心洞察
> 基于PAC-Bayesian理论，推导出最差类别误差的上界由加权经验混淆矩阵的谱范数和一个模型复杂度项控制。通过最小化这个谱范数（CAR正则项），可以直接抑制类间混淆，提高尾部类别的泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向长尾识别的混淆感知频谱正则化器 |
| 英文题名 | Confusion-Aware Spectral Regularizer for Long-Tailed Recognition |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.16732) · [Code](https://github.com/misswayguy/CAR) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Confusion-Aware Spectral Regularizer (CAR) |
| Dataset | ImageNet-LT, CIFAR100-LT, iNaturalist |

> [!tip] 效果简介
> - ImageNet-LT 上，Top-1 Accuracy Overall (%) 60.07 vs 56.20 (LOS) (+3.87)。
> - CIFAR100-LT 上，Top-1 Accuracy Overall (%) 55.68 vs 50.85 (BBN/LOS) (+4.83)。
> - iNaturalist 上，Top-1 Accuracy Overall (%) 73.38 vs 71.01 (LOS) (+2.37)。

## 概述

长尾识别任务的核心瓶颈在于：尾部类别样本稀少，导致模型对尾部类别的特征学习不足，同时类别间混淆严重——最差类别的测试准确率远低于整体准确率，且存在明显的训练过拟合、测试泛化差的现象（Figure 1）。针对这一问题，本文提出 **Confusion-Aware Spectral Regularizer (CAR)**，一种基于混淆感知的频谱正则化方法。

CAR 的核心思想源于 PAC-Bayesian 理论推导：最差类别误差的上界可由频率加权的经验混淆矩阵的谱范数和一个模型复杂度项共同控制（Proposition 3.2）。据此，CAR 将最小化加权混淆矩阵的谱范数作为正则项引入训练目标，直接抑制类别间的混淆程度，从而提升尾部类别的泛化能力。

在方法定位上，CAR 属于**损失函数正则化**范式，可与标准交叉熵损失及现有数据增强方法（如 ConCutMix、SAFA 等）灵活结合。其关键设计包括：（1）根据类别频率定义的对角权重矩阵 $\mathbf{\Lambda}$，放大尾部类别在混淆矩阵中的贡献；（2）可微混淆矩阵替代，通过 sigmoid 软化边际门控使混淆矩阵可微；（3）EMA 混淆估计器，在 mini-batch 上稳定估计混淆矩阵。

在 ImageNet-LT、CIFAR100-LT 和 iNaturalist 三个长尾基准上，CAR 从零训练 ViT-Small 的整体准确率超越此前最优方法 LOS **2.37% ∼ 4.83%**（Table 1）。特别地，在 ImageNet-LT 上，CAR 结合 ConCutMix 将最差类别测试准确率从 10% 提升至 **22%**（Table 3），有效缩小了最差类别与整体性能之间的差距。消融实验进一步验证了频率加权矩阵和 EMA 估计器对性能的持续贡献（Table 7）。

## 背景与动机

### 长尾识别中的最差类别泛化困境

现实视觉识别任务普遍遵循长尾分布——少数头部类别占据大量样本，而大多数尾部类别仅有极少量样本。标准交叉熵损失（CE）训练的模型在此分布下会出现严重的类别偏差：头部类别准确率远高于尾部类别。现有长尾学习方法主要从损失重加权、数据增强、解耦训练等角度缓解这一不平衡，但论文通过系统性实验揭示了一个被忽视的深层问题——**最差类别（worst-class）的泛化失效**。

Figure 1 在 ImageNet-LT 上以 ViT-Small 为骨干网络，对比了多种代表性长尾方法的三个关键指标：最差类别训练准确率、最差类别测试准确率、以及整体测试准确率。图中暴露出两个关键缺口：

1. **整体-最差缺口**：最差类别测试准确率显著落后于整体测试准确率。例如，**LOS**（Wei et al., ICLR 2025）的整体准确率为 56.20%，但其最差类别测试准确率仅为 10% 左右。
2. **训练-测试缺口**：最差类别测试准确率大幅低于其训练准确率，表明模型对尾部类别存在严重的过拟合——训练时能正确分类的样本，在测试时却大量混淆。

这两个缺口共同指向一个核心瓶颈：**现有方法未能有效抑制尾部类别与其他类别之间的特征混淆**。损失重加权方法（如 **Focal Loss** (Lin et al., ICCV 2017)、**LDAM-DRW** (Cao et al., NeurIPS 2019)）虽然增大了尾部类别的优化权重，但并未直接约束类别间的决策边界混淆；数据增强方法（如 **CMO** (Park et al., CVPR 2022)、**ConCutMix** (Kang et al., TIP 2024)）通过混合样本扩充尾部类别，但混淆抑制仍是间接的副作用。

### 现有方法的理论盲区

从理论视角审视，最差类别误差的本质是**类别条件错误率的最大值**。传统长尾学习方法通常优化平均误差或其加权变体，对最大类别误差缺乏直接的泛化保证。论文指出，若能在训练过程中显式地建模并最小化类别间的混淆程度，则有望从根源上收紧最差类别的泛化上界。

然而，直接优化混淆矩阵面临两个工程障碍：
- **不可微性**：传统混淆矩阵基于硬计数（hard count），即 $\hat{c}_{ij} = \frac{1}{m_j} \sum_{q: y_q=j} \mathbf{1}(\hat{y}(x_q)=i)$，其中的指示函数不可导，无法嵌入端到端训练。
- **高方差估计**：在 mini-batch 训练中，尾部类别样本极少，单 batch 的混淆矩阵估计方差极大，难以提供稳定的优化信号。

### 本文动机与核心思路

针对上述瓶颈，论文提出 **Confusion-Aware Spectral Regularizer (CAR)**，其动机源于 PAC-Bayesian 理论的一个关键洞察：**最差类别误差的上界可由频率加权的经验混淆矩阵的谱范数（spectral norm）和一个模型复杂度项共同控制**（Proposition 3.2）。这意味着，若能在训练中直接最小化加权混淆矩阵的谱范数，就能从理论上收紧最差类别的泛化误差上界，从而系统性地提升尾部类别的测试性能。

为实现这一目标，CAR 设计了三个协同组件：
- **频率相关权重矩阵** $\mathbf{\Lambda}$：根据类别样本数 $m_j$ 定义权重 $\lambda_j = (m_j + r_0)^{-1/2}$，使正则项对尾部类别的混淆施加更强的惩罚。
- **可微混淆矩阵替代**：使用 sigmoid 软化边际门控，使混淆矩阵条目可导，从而支持梯度反传。
- **EMA 混淆估计器**：通过指数移动平均在 mini-batch 间平滑混淆矩阵，降低估计方差，提供稳定的优化目标。

最终训练目标为交叉熵损失加上谱范数正则项：

$$\mathcal{L}(f) = \frac{1}{m} \sum_{q=1}^{m} \mathbb{CE}\big(f(x_q), y_q\big) + \alpha \big\| \hat{\mathbf{C}}_t \mathbf{\Lambda} \big\|_2$$

该方法不依赖特定的数据增强策略或网络架构，可作为通用正则器与现有长尾学习方法即插即用地结合。

## 核心创新

本工作针对长尾识别中尾部类别泛化不足这一瓶颈，提出**混淆感知频谱正则化器（Confusion-Aware Spectral Regularizer, CAR）**。其核心创新在于将尾部类别泛化问题形式化为对加权混淆矩阵谱范数的约束，并通过三个关键设计使这一约束可微、稳定且高效地融入端到端训练。

### 从瓶颈到可控变量：加权混淆矩阵的谱范数

现有长尾方法普遍存在一个现象：最差类别（通常来自尾部）在训练集上的准确率远高于测试集，且与整体测试准确率之间存在显著差距（Figure 1）。这表明模型对尾部类别存在严重的**过拟合训练分布但泛化失败**的问题，本质上是类别间特征混淆在尾部被放大。

论文从 PAC-Bayesian 理论出发，推导出最差类别误差的上界由两项控制（Proposition 3.2）：

$$e _ { j } \leq \frac { \nu } { \lambda _ { j } } \left\| \mathbf { C } _ { \mathcal { S } , \gamma } ^ { f } \mathbf { A } \right\| _ { 2 } + \mathcal { E } ( f , \mathcal { S } , \gamma , \delta )$$

其中 $\mathbf{C}_{\mathcal{S},\gamma}^f$ 为经验混淆矩阵，$\mathbf{\Lambda} = \text{diag}(\lambda_j)$ 为频率相关权重矩阵，$\lambda_j = (m_j + r_0)^{-1/2}$ 使尾部类别获得更大权重。这一理论结果揭示：**最小化频率加权混淆矩阵的谱范数，可以直接收紧最差类别的泛化误差上界**。因此，谱范数成为控制尾部泛化的因果性可操作变量。

### 三个关键设计：使谱范数正则化可微、稳定、可嵌入

直接将谱范数最小化面临两个工程障碍：①硬计数混淆矩阵不可微；② mini-batch 上估计的混淆矩阵方差大。CAR 通过以下三个 changed slots 解决这些问题：

**1. 可微混淆矩阵替代（Differentiable Confusion Matrix Surrogate）**

将硬计数门控 $\mathbf{1}(\hat{y}(x_q)=i)$ 替换为 sigmoid 软边际门控：

$$\tilde { c } _ { i j } = \frac { 1 } { m _ { j } } \sum _ { q : y _ { q } = j } \sigma ( \gamma + f _ { w } ( x _ { q } ) [ i ] - f _ { w } ( x _ { q } ) [ j ] )$$

其中 $\gamma$ 控制软门控的锐度。该替代使得混淆矩阵对模型参数可微，从而可以通过反向传播直接优化谱范数。

**2. EMA 混淆估计器（EMA-based Confusion Estimator）**

为降低 mini-batch 估计的方差，引入指数移动平均来累积全局混淆信息：

$$\hat { \bf C } _ { \bf t } = \beta ( \hat { \bf C } _ { t - 1 } ) + ( 1 - \beta ) \tilde { \bf C } _ { B _ { t } , \gamma } ^ { f }$$

消融实验证实：EMA 估计器将 ImageNet-LT 上准确率从 55.77% 提升至 57.48%（Table 7），且 $\beta=0.5$ 提供最佳性能（Figure 3）。

**3. 频率感知加权矩阵 $\mathbf{\Lambda}$**

类别权重 $\lambda_j = (m_j + r_0)^{-1/2}$ 显式地根据样本频率放大尾部类别在混淆矩阵中的贡献。消融显示，加入 $\mathbf{\Lambda}$ 后 ImageNet-LT 准确率从 54.39% 提升至 57.48%（Table 7），验证了频率加权对尾部泛化的关键作用。

### 最终训练目标

将上述组件整合，CAR 的训练损失为交叉熵与谱范数正则项的加权和：

$$\mathcal { L } ( f ) = \frac { 1 } { m } \sum _ { q = 1 } ^ { m } \mathbb { C } \mathbb { E } \big ( f ( x _ { q } ) , y _ { q } \big ) + \alpha \| \big ( \hat { \mathbf { C } } _ { \mathbf { t } } \mathbf { \Lambda } \big ) \| _ { 2 }$$

其中 $\alpha \approx 0.5$ 时性能最优（Figure 3）。该公式简洁地实现了“提升尾部泛化”这一目标：交叉熵保证整体判别能力，谱范数正则项直接抑制类间混淆，权重矩阵 $\mathbf{\Lambda}$ 将优化重心导向尾部类别。

### 与现有方法的关键区别

与重加权（Focal Loss, CB）、边界调整（LDAM-DRW）、数据增强（CMO, ConCutMix）等策略不同，CAR 是**首个从混淆矩阵谱范数角度直接优化类别间混淆结构**的方法。它不改变样本分布或决策边界，而是直接作用于特征空间中类别间的重叠程度——这是尾部类别泛化失败的根源。实验表明，CAR 可以与数据增强方法（如 ConCutMix）正交叠加，在 ImageNet-LT 上进一步将整体准确率从 57.48% 提升至 60.07%，尾部准确率从 35.77% 提升至 38.07%（Table 1）。

## 整体框架

CAR 的整体框架围绕一个核心目标展开：**在标准交叉熵训练中注入一个可微分的、频率感知的混淆矩阵谱范数正则项**，从而直接抑制类别间混淆，提升尾部类别的泛化能力。整个 pipeline 由四个逻辑模块串联而成，形成“构建 → 软化 → 平滑 → 正则化”的闭环。

### 模块关系与数据流

1. **加权混淆矩阵构建**
   - 输入：模型对当前 mini-batch 的预测 logits 与真实标签。
   - 操作：根据训练集中各类别的样本频率 $m_j$ 计算对角权重矩阵 $\mathbf{\Lambda} = \text{diag}(\lambda_j)$，其中 $\lambda_j = (m_j + r_0)^{-1/2}$。该频率相关加权使尾部类别在混淆度量中获得更高的惩罚权重。
   - 输出：加权的经验混淆矩阵 $\mathbf{C}_{\mathcal{S},\gamma}^f \mathbf{\Lambda}$。

2. **可微混淆矩阵替代**
   - 瓶颈：原始的硬计数混淆矩阵（基于 argmax 的指示函数）不可微，无法用于梯度优化。
   - 解决方案：引入 sigmoid 软边际门控机制，将混淆矩阵条目替换为可微形式：
     $$\tilde{c}_{ij} = \frac{1}{m_j} \sum_{q: y_q = j} \sigma(\gamma + f_w(x_q)[i] - f_w(x_q)[j])$$
     其中 $\sigma(\cdot)$ 为 sigmoid 函数，$\gamma$ 为边际参数。该替代保持了混淆矩阵的语义，同时使梯度能够通过谱范数反向传播。
   - 输出：可微代理混淆矩阵 $\tilde{\mathbf{C}}$。

3. **EMA 混淆估计器**
   - 瓶颈：mini-batch 内样本有限，直接计算的混淆矩阵方差大、不稳定。
   - 解决方案：采用指数移动平均（EMA）跨 batch 累积混淆统计：
     $$\hat{\mathbf{C}}_t = \beta \hat{\mathbf{C}}_{t-1} + (1 - \beta) \tilde{\mathbf{C}}_{B_t, \gamma}^f$$
     其中 $\beta \in [0,1]$ 控制历史信息的衰减速率（实验表明 $\beta=0.5$ 最优）。
   - 输出：稳定估计的混淆矩阵 $\hat{\mathbf{C}}_t$。

4. **谱范数正则化**
   - 操作：计算加权混淆矩阵的谱范数（即最大奇异值）作为正则项 $\mathcal{R}(f) = \|\hat{\mathbf{C}}_t \mathbf{\Lambda}\|_2$，并将其加入标准交叉熵损失：
     $$\mathcal{L}(f) = \frac{1}{m} \sum_{q=1}^{m} \mathbb{CE}(f(x_q), y_q) + \alpha \|\hat{\mathbf{C}}_t \mathbf{\Lambda}\|_2$$
   - 理论依据：PAC-Bayesian 泛化上界（Proposition 3.2）证明，最差类别误差由 $\frac{\nu}{\lambda_j} \|\mathbf{C}_{\mathcal{S},\gamma}^f \mathbf{\Lambda}\|_2$ 主导。最小化该谱范数等价于直接压制类别间混淆，尤其对尾部类别效果显著。

### 端到端训练流程

前向传播时，模型输出 logits 同时流入两条路径：一条进入交叉熵损失计算分类误差，另一条经过可微混淆矩阵替代和 EMA 平滑后计算谱范数正则项。反向传播时，两部分损失的梯度叠加更新模型参数。正则项权重 $\alpha$ 控制混淆抑制的强度（实验建议 $\alpha \approx 0.5$）。

该框架的关键优势在于**即插即用**：CAR 仅修改损失函数，不改变模型架构，因此可以与 ViT、ResNet、Swin 等多种骨干网络及 ConCutMix、CMO 等数据增强方法无缝结合。

### 补充图表

![[assets/figures/papers/paper_list_l2115_https_arxiv_org_abs_2603_16732/figures/001_Figure_1.jpg]]
*Figure 1: Poor generalization of worst-class performance in existing long-tailed learning methods. Experiments are conducted on ImageNet-LT using ViT-Small as the backbone. The three bars for each method correspond to the worst-class accuracy on the training set (left), the worst-class accuracy on the test set (middle), and the overall test accuracy (right)*

## 核心模块与公式推导

### 动机：从最差类别误差到混淆矩阵谱范数

长尾识别中，尾部类别不仅整体准确率低，更存在严重的**训练-测试泛化鸿沟**：模型在训练集上对尾部类别过拟合，但测试时准确率大幅下降（见 Figure 1）。论文将这一现象建模为**加权最差类别误差（Weighted Worst-Class Error, WCE）**：

$$
\mathsf{WCE}(f) = \left\| \mathbf{C}_{\mathcal{D}}^{f} \boldsymbol{\Lambda} \right\|_{1}
$$

其中 $\mathbf{C}_{\mathcal{D}}^{f}$ 是总体混淆矩阵（对角线元素置零，仅保留类间混淆），$\boldsymbol{\Lambda} = \mathrm{diag}(\lambda_j)$ 是频率相关的类别权重矩阵，权重定义为 $\lambda_j = (m_j + r_0)^{-1/2}$，$m_j$ 为类别 $j$ 的样本数，$r_0$ 为平滑常数。该权重设计使得**样本稀少的尾部类别在混淆度量中获得更大的惩罚权重**。

基于 PAC-Bayesian 理论，论文推导出单个类别 $j$ 的误差上界（Proposition 3.2）：

$$
e_j \leq \frac{\nu}{\lambda_j} \left\| \mathbf{C}_{\mathcal{S},\gamma}^{f} \boldsymbol{\Lambda} \right\|_{2} + \mathcal{E}(f, \mathcal{S}, \gamma, \delta)
$$

该上界的关键项是**频率加权经验混淆矩阵的谱范数** $\|\mathbf{C}_{\mathcal{S},\gamma}^{f} \boldsymbol{\Lambda}\|_2$，其中 $\nu$ 为常数，$\mathcal{E}$ 为与模型复杂度相关的项。这一理论结果揭示：**通过最小化加权混淆矩阵的谱范数，可以直接压制最差类别误差的上界**。

### 核心模块一：可微混淆矩阵替代

标准混淆矩阵依赖硬计数 $\mathbf{1}(\hat{y}(x_q) = i)$，不可微。论文提出**可微混淆矩阵替代（Differentiable Confusion Matrix Surrogate）**，使用 sigmoid 软化边际门控：

$$
\tilde{c}_{ij} = \frac{1}{m_j} \sum_{q: y_q = j} \sigma\big(\gamma + f_{w}(x_q)[i] - f_{w}(x_q)[j]\big)
$$

其中 $f_{w}(x_q)[i]$ 为模型对样本 $x_q$ 在类别 $i$ 上的 logit 输出，$\gamma \ge 0$ 为边际参数。当 $f_{w}(x_q)[i] - f_{w}(x_q)[j] > -\gamma$ 时，sigmoid 输出接近 1，模拟“被误分类为类别 $i$”的软计数。该设计使混淆矩阵对模型参数可微，从而可以端到端优化。

### 核心模块二：EMA 混淆估计器

mini-batch 上估计的混淆矩阵方差较大，论文引入**指数移动平均（EMA）混淆估计器**进行稳定化：

$$
\hat{\mathbf{C}}_t = \beta \hat{\mathbf{C}}_{t-1} + (1 - \beta) \tilde{\mathbf{C}}_{B_t, \gamma}^{f}
$$

其中 $\tilde{\mathbf{C}}_{B_t, \gamma}^{f}$ 为当前 batch $B_t$ 上的可微混淆矩阵，$\beta \in [0, 1]$ 为 EMA 衰减因子。消融实验表明，EMA 估计器将 ImageNet-LT 上整体准确率从 55.77% 提升至 57.48%（Table 7），且 $\beta = 0.5$ 提供最佳性能（Figure 3）。

### 核心模块三：谱范数正则化

将上述模块组合，得到**混淆感知频谱正则项（Confusion-Aware Spectral Regularizer, CAR）**：

$$
\mathcal{R}(f) = \left\| \hat{\mathbf{C}}_t \boldsymbol{\Lambda} \right\|_{2}
$$

最终训练目标为交叉熵损失与该正则项的加权和：

$$
\mathcal{L}(f) = \frac{1}{m} \sum_{q=1}^{m} \mathbb{CE}\big(f(x_q), y_q\big) + \alpha \left\| \hat{\mathbf{C}}_t \boldsymbol{\Lambda} \right\|_{2}
$$

其中 $\alpha$ 控制正则化强度，消融显示 $\alpha \approx 0.5$ 为最优（Figure 3）。该正则项直接作用于混淆矩阵的谱结构，抑制类别间的系统性混淆，尤其对尾部类别效果显著。

### 模块间的因果链路

1. **频率加权 $\boldsymbol{\Lambda}$** 将尾部类别的混淆放大，使优化重心向少数类倾斜；
2. **可微代理** 使谱范数对模型参数可导，实现端到端训练；
3. **EMA 平滑** 降低 batch 级估计的方差，提供稳定的梯度信号；
4. **谱范数最小化** 直接压缩最差类别误差的理论上界，提升尾部泛化。

这一设计使 CAR 在 ImageNet-LT 上将最差类别测试准确率从 10% 提升至 22%（Table 3），同时可与数据增强方法（如 ConCutMix）叠加使用，进一步提升整体性能至 60.07%（Table 1）。

### 补充图表

![[assets/figures/papers/paper_list_l2115_https_arxiv_org_abs_2603_16732/figures/006_Figure_2.jpg]]
*Figure 2: Class-wise confusion matrices on CIFAR100-LT using ViT-Small. Left: training from scratch. Right: fine-tuning from pretrained model*

## 实验与分析

### 核心性能对比

CAR 在三个主流长尾基准上均取得最优整体准确率，且对尾部类别提升尤为显著。从零训练的 ViT-Small 下，CAR 超越此前最优方法 LOS（Wei et al., ICLR 2025）达 2.37%∼4.83%（Table 1）。具体而言，ImageNet-LT 上 CAR 整体准确率为 57.48%，尾部准确率为 35.77%；与 ConCutMix 结合后，整体准确率进一步提升至 60.07%，尾部准确率达到 38.07%，相比 LOS 的 56.20% 整体和 32.73% 尾部分别提升 3.87 和 5.34 个百分点。CIFAR100-LT 上 CAR+ConCutMix 达到 55.68% 整体准确率，iNaturalist 上达到 73.38%，均刷新记录。

![[assets/figures/papers/paper_list_l2115_https_arxiv_org_abs_2603_16732/figures/002_Table_1.jpg]]
*Table 1: Top-1 accuracy (%) comparison on ImageNet-LT, CIFAR100-LT (IF=100), and iNaturalist using ViT-Small. Results are reported for Head, Medium, Tail, and Overall. The best results are in bold, and the second-best are underlined*

在预训练微调场景下，CAR 同样保持领先（Table 2）。iNaturalist 上 CAR+ConCutMix 尾部准确率达 85.40%，整体 85.44%；CIFAR100-LT 尾部 63.33%，整体 82.12%；Tiny-ImageNet-LT 尾部 54.23%，整体 75.84%，尾部提升幅度达 2.22%∼5.19%。

![[assets/figures/papers/paper_list_l2115_https_arxiv_org_abs_2603_16732/figures/003_Table_2.jpg]]
*Table 2: Top-1 accuracy (%) comparison on Tiny-ImageNet-LT, CIFAR100-LT (IF=100), and iNaturalist using pre-trained ViT-Small. Results are reported for Head, Medium, Tail, and Overall. The best results are in bold, and the second-best are underlined*

### 最差类别泛化分析

Figure 1 揭示了现有长尾方法的两个关键差距：①最差类别测试准确率远低于整体测试准确率；②最差类别测试准确率远低于其训练准确率，表明尾部类别存在严重过拟合。Table 3 显示，CAR 直接针对此瓶颈：ImageNet-LT 上最差类别测试准确率从 SAFA/LOS 的 10% 提升至 22%（CAR+ConCutMix），CIFAR100-LT 上从 8% 提升至 18%，提升幅度达 8%∼12%。同时，最差类别比率（WR = Test/Training）显著提高，说明 CAR 有效抑制了尾部类别的过拟合。

![[assets/figures/papers/paper_list_l2115_https_arxiv_org_abs_2603_16732/figures/005_Table_3.jpg]]
*Table 3: Worst-class accuracy on training/test sets and the Worstclass Ratio (WR = Test/Training) based on ViT-Small. All results are presented as percentages. The best results are highlighted in bold, and the second-best are underlined*

### 骨干网络与不平衡因子泛化性

Table 4 验证了 CAR 在不同骨干网络上的通用性：ViT-Tiny（46.35%）、ViT-Base（63.79%）、ViT-Large（69.26%）、ResNet（50.27%）、Swin（56.38%）均取得最优。Table 5 展示在不同不平衡因子（IF）下，CAR 在 ImageNet-LT 和 CIFAR100-LT 上均持续优于基线，表明方法对不平衡程度具有鲁棒性。

![[assets/figures/papers/paper_list_l2115_https_arxiv_org_abs_2603_16732/figures/004_Table_4.jpg]]
*Table 4: Top-1 accuracy (%) on ImageNet-LT across different backbones. Results include ViT variants (Tiny/Base/Large), ResNet, and Swin. The best results are highlighted in bold*

![[assets/figures/papers/paper_list_l2115_https_arxiv_org_abs_2603_16732/figures/007_Table_5.jpg]]
*Table 5: Top-1 accuracy (%) across different imbalance factors (IF) on ImageNet-LT and CIFAR100-LT based on the ViT-Small. The best results are highlighted in bold*

### 与数据增强的协同效应

Table 6 显示 CAR 可与多种长尾数据增强方法互补叠加。在 ImageNet-LT 和 CIFAR100-LT 不同 IF 下，CAR+ConCutMix 组合始终取得最佳结果，验证了频谱正则化与混合增强策略的正交性。

![[assets/figures/papers/paper_list_l2115_https_arxiv_org_abs_2603_16732/figures/008_Table_6.jpg]]
*Table 6: Top-1 accuracy (%) of ViT-Small on ImageNet-LT and CIFAR100-LT under different imbalance factors (IF). “+” indicates the combination of our method with other long-tailed data augmentation methods*

### 消融实验

**频率加权矩阵 Λ** 是关键设计。Table 7 表明，移除 Λ 后，ImageNet-LT 整体准确率从 57.48% 降至 54.39%，CIFAR100-LT 从 55.68% 降至 51.23%，降幅约 3%∼4%。Λ 通过频率相关权重 $\lambda_j = (m_j + r_0)^{-1/2}$ 放大尾部类别在混淆矩阵中的贡献，是抑制类别间混淆的核心机制。

**EMA 混淆估计器** 对稳定训练至关重要。移除 EMA 后，ImageNet-LT 准确率降至 55.77%，CIFAR100-LT 降至 54.23%，表明 mini-batch 级别的混淆矩阵估计方差较大，EMA 平滑能有效降低噪声。

**超参数敏感性**（Figure 3）：EMA 因子 $\beta=0.5$ 和正则权重 $\alpha \approx 0.5$ 提供最佳性能，偏离此区间性能下降，说明方法对超参数有一定敏感性，实际部署需针对数据集调优。

### 混淆矩阵可视化

Figure 2 展示了 CIFAR100-LT 上不同方法的类别混淆矩阵。CAR 的混淆矩阵非对角线元素显著减弱，尤其在尾部类别区域，直观验证了谱范数正则化对抑制类间混淆的有效性。从零训练和预训练微调两种设置下，CAR 均表现出更干净的对角主导结构。

### 局限与待验证问题

方法性能对 $\alpha$、$\beta$ 等超参数敏感，不同数据集可能需要独立调优。混淆矩阵构建与谱范数计算增加了训练开销，且当前仅在图像分类任务上验证。扩展到目标检测、实例分割等任务的有效性尚未探索。在更极端的长尾分布（如无限类别流）下的表现也需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l2115_https_arxiv_org_abs_2603_16732/figures/009_Figure_3.jpg]]
*Figure 3: Ablation on four hyperparameters on CIFAR100-LT with ViT-Small (Top-1 accuracy). From left to right: EMA factor*

![[assets/figures/papers/paper_list_l2115_https_arxiv_org_abs_2603_16732/figures/010_Table_7.jpg]]
*Table 7: Ablations for Λ and EMA. Experiments are conducted on ImageNet-LT and CIFAR100-LT based on the ViT-Small*

![[assets/figures/papers/paper_list_l2115_https_arxiv_org_abs_2603_16732/figures/012_Figure_4.jpg]]
*Figure 4: Comparison of worst-class and overall accuracies across representative long-tailed learning methods on CIFAR100-LT using Pretrained ViT-Small as the backbone. The three bars for each method correspond to the worst-class accuracy on the training set (left, red-hatched), the worst-class accuracy on the test set (middle, purple-hatched), and the overall test accuracy (right, green-hatched)*

![[assets/figures/papers/paper_list_l2115_https_arxiv_org_abs_2603_16732/figures/011_Table_8.jpg]]
*Table 8: Top-1 accuracy (%) of pre-tranied ResNet on Tiny-ImageNet-LT under different imbalance factors (IF = 50, 100, and 200). The best results are highlighted in bold*

## 方法谱系与知识库定位

### 1. 与现有长尾学习方法的谱系关系

长尾识别的研究主线可大致分为三类：重加权/重采样、边界调整/解耦训练、以及数据增强。CAR 在谱系上属于**损失函数正则化**的新分支，其独特之处在于将优化的对象从“类间边界”或“样本权重”转移到了“混淆矩阵的谱结构”。

**（1）相对于重加权方法的定位**

重加权方法通过调整不同类别的损失权重来缓解头部类别的支配效应，典型工作包括 **Focal Loss** (Lin et al., ICCV 2017)、**CB Loss** (Cui et al., CVPR 2019) 和 **LDAM-DRW** (Cao et al., NeurIPS 2019)。这些方法的共同瓶颈在于：权重设计主要依赖类别频率的先验，无法直接感知模型在训练过程中实际发生的类间混淆模式。CAR 与此类方法的本质区别在于，它不直接修改损失函数中各样本的权重系数，而是在交叉熵损失之上附加一个**数据驱动的正则项**——该正则项的值取决于当前模型对训练数据的真实混淆行为，从而实现了从“静态频率补偿”到“动态混淆抑制”的范式转换。

**（2）相对于边界调整方法的定位**

**LDAM-DRW** 和 **BALMS** (Ren et al., NeurIPS 2020) 通过为尾部类别分配更大的分类边界来提升泛化能力。这类方法的理论基础是尾部类别的边界被头部类别侵蚀。CAR 的理论出发点不同：基于 PAC-Bayesian 框架，论文推导出最差类别误差的上界由**加权经验混淆矩阵的谱范数**和一个模型复杂度项共同控制（Proposition 3.2）。这意味着，与其间接地扩大边界，不如直接最小化混淆矩阵的最大奇异值——后者是类间混淆的全局度量，理论上对所有类别（尤其是尾部类别）的泛化误差具有更强的约束力。

**（3）相对于数据增强方法的定位**

**ReMix** (Chou et al., ECCV 2020)、**CMO** (Park et al., CVPR 2022)、**SAFA** (Hong et al., ECCV 2022) 和 **ConCutMix** (Kang et al., TIP 2024) 等方法通过在输入空间或特征空间进行混合增强来平衡类别分布。CAR 与这些方法是**正交且互补**的：数据增强作用于输入/特征层面，而 CAR 作用于损失函数层面。实验证据充分支持这一互补性——在 ImageNet-LT 上，CAR 单独使用时整体准确率为 57.48%，与 ConCutMix 结合后提升至 60.07%（Table 1），尾部准确率从 35.77% 提升至 38.07%。这种即插即用的兼容性是 CAR 作为通用正则化器的重要优势。

**（4）相对于最新方法的定位**

**LOS** (Wei et al., ICLR 2025) 是论文发表时的最新 state-of-the-art，通过最优搜索策略来平衡各类别的训练。CAR 在三个主 benchmarks 上全面超越 LOS：ImageNet-LT 上提升 3.87%（60.07% vs. 56.20%），CIFAR100-LT 上提升 4.83%（55.68% vs. 50.85%），iNaturalist 上提升 2.37%（73.38% vs. 71.01%）。这一性能优势的根源在于：LOS 仍然在“如何分配训练资源”的框架内优化，而 CAR 直接针对“混淆如何发生”的机制进行干预。

### 2. 方法适用边界

**已验证的适用范围：**
- **任务类型**：图像分类（长尾分布），包括从零训练和预训练微调两种范式。
- **骨干网络**：ViT（Tiny/Base/Large）、ResNet、Swin Transformer。Table 4 显示 CAR 在五种不同骨干网络上均取得最优结果，表明其对架构选择不敏感。
- **数据集规模**：从小规模（CIFAR100-LT，100 类）到中等规模（ImageNet-LT，1000 类）再到大规模细粒度（iNaturalist，8142 类）。
- **不平衡程度**：Table 5 显示在不平衡因子 50、100、200 下均有效。

**已知的敏感性与限制：**
- **超参数敏感性**：Figure 3 的消融实验显示，EMA 因子 β 和正则化权重 α 对性能有显著影响，最优值约为 β=0.5、α≈0.5。这意味着在不同数据集上可能需要重新调参，缺乏自适应的超参数选择机制。
- **计算开销**：混淆矩阵的构建、EMA 更新和谱范数计算（涉及 SVD 或幂迭代）增加了训练时的计算负担。论文未量化这一开销相对于基线方法的增长幅度。
- **任务泛化未验证**：所有实验均限于图像分类，尚未扩展到目标检测、实例分割或语义分割等更复杂的视觉任务。

### 3. 局限性与开放问题

**已识别的局限性：**

1. **理论假设的实践差距**：PAC-Bayesian 上界（Proposition 3.2）的推导依赖于特定的假设条件（如损失函数的有界性），论文未充分讨论这些假设在实际训练中是否严格满足，以及违反假设时上界的紧致性如何退化。

2. **混淆矩阵估计的统计可靠性**：EMA 估计器（Equation 8）在 mini-batch 上更新混淆矩阵，当类别数很大（如 iNaturalist 的 8142 类）且 batch size 有限时，每个 batch 仅覆盖极少类别，EMA 估计的方差可能仍然较大。论文未分析类别数对估计质量的影响。

3. **与最新架构的结合**：实验仅覆盖到 ViT 和 Swin，未涉及 Mamba、状态空间模型等更新架构。

4. **公平性维度缺失**：论文仅在类别不平衡的语境下研究，未讨论方法对不同种族、性别等敏感属性的公平性影响。频率加权矩阵 Λ 的设计是否可能引入新的偏见，需要进一步审视。

**开放问题：**

1. **扩展到复杂视觉任务**：CAR 的核心操作（构建混淆矩阵、计算谱范数）在理论上不限于分类任务。对于目标检测，是否可以将“类别混淆”扩展为“类别-边界框联合混淆”？对于实例分割，是否可以在 mask 层面定义混淆？这些扩展需要重新设计可微的混淆度量。

2. **极端长尾与开放类别场景**：在无限类别流（如在线学习）或存在开放类别（open-set）的长尾场景下，混淆矩阵的维度动态变化，EMA 估计器和谱范数优化的稳定性和有效性需要重新验证。

3. **与对比学习/自监督预训练的协同**：论文仅验证了与监督预训练模型的结合（Table 2）。当前主流的自监督预训练（如 DINO、MAE）是否能与 CAR 产生更强的协同效应，是一个有实践价值的问题。

4. **谱范数之外的结构约束**：论文仅约束了混淆矩阵的谱范数（最大奇异值）。核范数（奇异值之和）或秩约束是否能在抑制混淆的同时保留更多的类别可分性，值得探索。

5. **自适应超参数机制**：能否设计一种基于混淆矩阵谱结构自动调整 α 和 β 的机制，使得 CAR 在不同数据集上无需手动调参即可达到接近最优的性能？

## 原文 PDF

![[paperPDFs/CVPR_2026/Confusion_Aware_Spectral_Regularizer_for_Long_Tailed_Recognition.pdf]]
