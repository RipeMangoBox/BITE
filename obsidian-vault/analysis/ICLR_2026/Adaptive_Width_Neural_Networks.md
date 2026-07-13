---
title: "Adaptive Width Neural Networks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Adaptive_Width_Neural_Networks.pdf
project_link: null
code_link: null
aliases:
- AWNNA
- AWNN
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "AWN learns layer widths by optimizing a variational latent width parameter that defines a monotone importance distribution over neurons."
primary_logic: "It jointly trains weights and width parameters under an ELBO, soft-sorts neurons by importance, and enables post-training truncation of low-importance units."
claims:
- "AWN removes the need to preselect fixed layer widths or run expensive width grid search."
- "A monotone decreasing importance distribution makes later neurons less influential and easy to prune."
- "The note reports comparable or better performance than fixed-width baselines across tabular, image, text, sequence, and graph tasks."
---

# Adaptive Width Neural Networks

> [!tip] 核心洞察
> 通过变分推断（ELBO）联合优化网络权重和宽度参数，利用单调递减的分布对神经元施加软排序（soft ordering），使得新加入的神经元具有较低的重要性，从而在不预设上限的情况下实现宽度的自适应学习，并允许在训练后通过简单地删除最后几行/列权重矩阵来实现零成本压缩。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 自适应宽度神经网络 |
| 英文题名 | Adaptive Width Neural Networks |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=p6Ek7Qg577) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Adaptive Width Neural Networks (AWN) |
| Dataset | DoubleMoon, Spiral, SpiralHard, pol |

> [!tip] 效果简介
> - DoubleMoon 上，Accuracy 为 100.0 (0.0)，对比 100.0 (0.0)，变化 0.0。
> - Spiral 上，Accuracy 为 99.8 (0.1)，对比 100.0 (0.0)，变化 -0.2。
> - SpiralHard 上，Accuracy 为 100.0 (0.0)，对比 98.0 (2.0)，变化 +2.0。

## 概要

本文提出了一种名为**自适应宽度神经网络（Adaptive Width Neural Networks, AWN）** 的新方法，旨在解决传统神经网络中每层宽度（神经元数量）需要作为固定超参数进行手动或网格搜索调优的问题。AWN通过引入一个可学习的潜在变量，利用变分推断（ELBO）在标准反向传播过程中动态调整每层的神经元数量，无需预设上限。该方法在多个领域（表格、图像、文本、序列、图）的实验中，性能与固定宽度基线相当，且宽度能自适应任务难度。此外，AWN通过对神经元施加软排序（soft ordering），允许在训练后通过简单地删除最后几行/列权重矩阵来实现零成本压缩。

传统神经网络将每层宽度（神经元数量）视为需要手动或通过网格搜索等超参数调优方法选择的固定超参数，这导致搜索空间随层数指数增长，且在大规模模型（如拥有数十亿参数的基础模型）上因训练成本过高而几乎不可行。现有方法如构造性算法（Cascade Correlation, Firefly Network Descent）和剪枝方法虽然可以动态调整网络规模，但通常依赖人工定义的启发式规则，而非端到端的梯度学习。本文受Nazaret & Blei (2022) 的无界深度网络启发，将注意力转向神经元数量，提出了一种通过梯度下降自动学习网络宽度的概率框架。

## 核心方法与创新机理

AWN的核心创新在于引入一个可学习的潜在变量 λℓ，该变量参数化一个定义在自然数上、具有无限支撑的单调递减分布 fℓ（具体实现为离散化指数分布），并通过该分布的 k 分位数函数确定每层的截断宽度 Dℓ。通过变分推断（ELBO）联合优化网络权重和宽度参数，利用单调递减的分布对神经元施加软排序（soft ordering），使得新加入的神经元具有较低的重要性，从而在不预设上限的情况下实现宽度的自适应学习，并允许在训练后通过简单地删除最后几行/列权重矩阵来实现零成本压缩。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_p6Ek7Qg577_Adaptiv/figures/001_Figure_1.jpg]]
*Figure 1: (Left) The graphical model of AWN, with dark observable random variables and white latent ones. (Middle) The distribution $f _ { \ell }$ over hidden units’ importance at layer ℓ is parametrized by $\lambda _ { \ell }$ . . The width of layer ℓ is chosen as the quantile function of the distribution $f _ { \ell }$ evaluated at k and denoted by $D _ { \ell } . \mathrm { \ }$ ( R i g h t ) The hidden units’ activations at layer ℓ are rescaled by their importance.

AWN的整体框架基于一个概率图模型，其中观测变量为输入X和标签Y，潜在变量包括宽度参数λ和网络权重θ。训练过程通过最大化证据下界（ELBO）来联合学习λ和θ。具体而言，AWN为每一层ℓ引入一个潜在变量λℓ，该变量控制一个离散化指数分布fℓ，该分布定义了神经元的重要性。每层的实际宽度Dℓ由fℓ的k分位数函数确定。在训练过程中，AWN通过反向传播更新λℓ和θ，从而动态调整网络宽度。训练完成后，由于神经元被软排序，可以通过删除最后几个神经元（即权重矩阵的最后几行/列）来实现零成本压缩。

**变分推断框架**：AWN定义了一个概率图模型，引入潜在变量λ和θ，通过最大化ELBO来联合学习宽度和权重。ELBO的一阶近似形式为：

$$\sum_\ell^L \log \frac{p(\nu_\ell; \mu_\ell^\lambda, \sigma_\ell^\lambda)}{q(\nu_\ell; \nu_\ell)} + \sum_\ell^L \sum_{n=1}^{D_\ell} \log \frac{p(\rho_{\ell n}; \sigma_\ell^\theta)}{q(\rho_{\ell n}; \rho_{\ell n})} + \sum_{i=1}^N \log p(y_i|\lambda=\nu, \theta=\rho, x_i)$$

**离散化指数分布 fℓ**：作为神经元重要性的分布，具有单调递减和无限支撑的性质，用于计算截断宽度Dℓ。其概率质量函数为：

$$f_\ell(x; \lambda_\ell) = (1 - e^{-\lambda_\ell (x+1)}) - (1 - e^{-\lambda_\ell x})$$

**软排序机制**：通过将激活值乘以重要性函数fℓ，对神经元施加软排序，使得新加入的神经元影响较小。重缩放后的激活值为：

$$h_j^\ell = \sigma\left( \sum_{k=1}^{D_{\ell-1}} w_{jk}^\ell h_k^{\ell-1} \right) f_\ell(j; \nu_\ell)$$

**Kaiming+权重初始化**：根据当前宽度和重要性分布调整权重初始化方差，防止深层网络激活值坍塌。对于ReLU激活函数，权重方差初始化为：

$$\mathrm{Var}[w_{jk}^\ell] = \frac{2}{\sum_{j=1}^{D_{\ell-1}} f_\ell^2(j)}$$

## 实验与关键发现

**主要结果**：Table 1展示了AWN与固定宽度基线在多个任务上的性能对比。关键结果包括：

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_p6Ek7Qg577_Adaptiv/figures/002_Table_1.jpg]]
*Table 1: Performances and total width of MLP layers for the fixed and AWN versions of the various models used. The exact width chosen by model selection on the graph datasets is unknown since we report published results. “Linear" means the chosen downstream classifier is a linear model.*

- 在SpiralHard数据集上，AWN达到了100.0%的准确率，而固定宽度基线为98.0%。
- 在PMNIST数据集上，AWN达到95.7%准确率，固定基线为91.1%。
- 在REDDIT-B图分类数据集上，AWN达到90.2%准确率，固定基线为87.0%。
- 在Multi30k翻译任务上，AWN Transformer使用的参数比固定宽度Transformer少200倍，同时测试损失相当（AWN: 1.51, Fixed: 1.43）。

**宽度自适应**：Figure 2（左）展示了学习到的宽度随任务难度增加而增加（DoubleMoon: 8.1, Spiral: 65.9, SpiralHard: 227.4）。Figure 2（右）显示AWN在SpiralHard上收敛速度更快。

**训练时压缩**：Figure 4展示了通过增加宽度正则化项的幅度，可以在训练过程中将总宽度减少50%以上，同时保持准确率。

**训练后截断**：Figure 5（左）展示了在Spiral数据集上，训练后可以截断约30%的神经元而不损失准确率。Figure 5（右）显示神经元激活值的分布呈指数曲线。

**消融实验**：
- Table 2比较了不同重要性函数族（指数、幂律、Sigmoid）的影响。指数分布平均总宽度954.4，幂律分布2952.4，Sigmoid分布426.8。
- Table 9显示，不使用正则化和有界激活函数会导致宽度显著增加（例如MiniBooNE上宽度从53增加到4907）。
- Figure 12表明，更高的分位数k（更好的ELBO近似）能带来更稳定的性能。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_p6Ek7Qg577_Adaptiv/figures/011_Table_2.jpg]]
*Table 2: Analysis of the impact of different families of importance functions on SpiralHard validation performance and learned width, averaged across different hyper-parameter configurations.*

**公平性说明**：
- 实验涵盖了表格、图像、文本、序列和图等多种数据领域。
- 对于图数据集（NCI1, REDDIT-B），基线结果直接引用自文献，其确切宽度未知。
- NAS比较实验（Table 8）中，所有方法使用相同的预算（5次评估），宽度搜索范围限制在0到512之间。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_p6Ek7Qg577_Adaptiv/figures/019_Table_3.jpg]]
*Table 3: Dataset statistics and number of samples in each split are shown.*

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_p6Ek7Qg577_Adaptiv/figures/020_Table_4.jpg]]
*Table 4: Hyper-parameter configurations for standard MLP/RNN and AWN versions on tabular datasets.*

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_p6Ek7Qg577_Adaptiv/figures/021_Table_5.jpg]]
*Table 5: Hyper-parameter configurations for standard MLP and AWN versions on image classification datasets.*

## 定位与知识库关联

AWN属于**动态神经网络**和**神经架构搜索（NAS）** 的交叉领域。与传统的NAS方法（如Grid Search, Random Search, Bayesian Optimization）不同，AWN通过变分推断在训练过程中端到端地学习宽度，无需在离散的架构空间中搜索。与构造性算法（如Cascade Correlation）相比，AWN通过梯度下降自动调整网络规模，无需人工定义的启发式规则。与剪枝方法相比，AWN在训练过程中学习神经元的软排序，使得训练后的压缩更加自然和高效。AWN与Nazaret & Blei (2022) 的无界深度网络在思想上最为接近，但将关注点从层数转移到了每层的宽度，并引入了单调递减的重要性分布这一关键归纳偏置。

## 原文 PDF

![[paperPDFs/ICLR_2026/Adaptive_Width_Neural_Networks.pdf]]
