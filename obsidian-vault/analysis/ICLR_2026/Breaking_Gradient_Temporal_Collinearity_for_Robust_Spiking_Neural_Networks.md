---
title: "Breaking Gradient Temporal Collinearity for Robust Spiking Neural Networks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Breaking_Gradient_Temporal_Collinearity_for_Robust_Spiking_Neural_Networks.pdf
openreview_forum_id: udTDFAshNM
aliases:
- STODS
- BGTCRSNN
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/robustness
core_operator: "梯度时间共线性（GTC），即不同时间步梯度分量之间的方向一致性程度。"
primary_logic: "通过在直接编码的输入层引入带结构化约束的参数化正交核（PFD）和全局正交正则化（GOR），有效降低 GTC，在保留直接编码高效率和特征保持能力的同时大幅提升鲁棒性。"
claims:
- "直接编码的 GTC（约 0.8–0.9）显著高于率编码（约 0.2–0.3），且该差异与鲁棒性差距密切相关。"
- "更高的 GTC 会通过 Hessian 谱半径上界（Eq. 5）放大参数 Hessian 的谱半径，从而降低鲁棒性。"
- "在 CIFAR‑10 上，STOD 将 PGD 白盒攻击下的准确率从基线 SNN+AT 的 14.07% 提升至 43.54%。"
- "消融实验表明，训练时使用正交核、推理时移除的策略，可在不引入额外推理开销的情况下获得最大的鲁棒性增益。"
---

# Breaking Gradient Temporal Collinearity for Robust Spiking Neural Networks

> [!tip] 核心洞察
> 通过在直接编码的输入层引入带结构化约束的参数化正交核（PFD）和全局正交正则化（GOR），有效降低 GTC，在保留直接编码高效率和特征保持能力的同时大幅提升鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 打破梯度时间共线性以实现鲁棒脉冲神经网络 |
| 英文题名 | Breaking Gradient Temporal Collinearity for Robust Spiking Neural Networks |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=udTDFAshNM); [GitHub](https://github.com/Apple26419/SNN_STOD) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/robustness |
| Method | Structured Temporal Orthogonal Decorrelation (STOD) |
| Dataset | CIFAR-10, CIFAR-100, ImageNet |

> [!tip] 效果简介
> - CIFAR-10 上，PGD accuracy (white box, ε=8/255) 为 43.54% (STOD + AT)，对比 14.07% (SNN + AT)，变化 +29.47。
> - CIFAR-100 上，FGSM accuracy (white box, ε=8/255) 为 41.89% (STOD + AT)，对比 16.31% (SNN + AT)，变化 +25.58。
> - ImageNet 上，FGSM accuracy (white box, ε=8/255) 为 26.77% (STOD + AT)，对比 15.74% (SNN + AT)，变化 +11.03。

## 概述

脉冲神经网络（SNN）在事件驱动和低功耗场景中具有天然优势，但其鲁棒性远落后于传统人工神经网络（ANN）。本文揭示了一个此前未被认识的根本瓶颈：**梯度时间共线性（Gradient Temporal Collinearity, GTC）**。直接编码（direct encoding）在每个时间步重复注入相同输入，导致不同时间步的梯度分量高度方向一致（GTC 约 0.8–0.9），而率编码（rate encoding）通过时间多样性机制将 GTC 降至约 0.2–0.3。理论分析表明，更高的 GTC 会通过 Hessian 谱半径上界放大参数 Hessian 的谱半径，从而严重损害网络鲁棒性。

针对这一瓶颈，本文提出 **Structured Temporal Orthogonal Decorrelation (STOD)**，通过在直接编码的输入层引入两个互补机制来降低 GTC：**Patchwise Feature Diversification (PFD)** 在每个时间步使用独立的参数化正交核对输入进行多样化变换；**Global Orthogonal Regularization (GOR)** 作为软约束惩罚不同时间步变换特征之间的余弦相似度，进一步促进方向分离。该方法在保留直接编码高效率与特征保持能力的同时，实现了鲁棒性的大幅提升。

核心实验结果：
- 在 CIFAR‑10 上，STOD 结合对抗训练将 PGD 白盒攻击下的准确率从基线 SNN+AT 的 14.07% 提升至 43.54%（+29.47 个百分点）。
- 在 CIFAR‑100 和 ImageNet 上，FGSM 白盒攻击下的准确率分别提升 25.58 和 11.03 个百分点。
- 消融实验证实，训练时使用正交核、推理时移除的策略（STOD w.o. OK）可在不引入额外推理开销的情况下获得最大的鲁棒性增益。
- STOD 通过了梯度混淆检查清单的所有项目，证实鲁棒性提升并非虚假。

方法存在轻微干净准确率下降（CIFAR‑10 上约 2%），且最优鲁棒性依赖对抗训练配合。正交核初始化策略要求时间步数 T ≤ 输入通道数×分块维度，限制了极长序列下的扩展性。

## 背景与动机

### 脉冲神经网络的鲁棒性困境

脉冲神经网络（SNN）凭借事件驱动的稀疏计算特性，在能效方面展现出显著优势，但其对抗鲁棒性长期落后于同架构的人工神经网络（ANN）。这一差距的核心瓶颈并非网络结构本身，而在于输入编码方式的选择。

直接编码（direct encoding）是 SNN 中最常用的高效编码策略：它直接将静态图像的浮点像素值在每个时间步重复注入网络，无需额外的脉冲生成过程。然而，这种恒等映射的简洁性恰恰成为鲁棒性的致命弱点——**在每个时间步重复注入完全相同的输入，导致不同时间步的梯度分量高度方向一致，即梯度时间共线性（Gradient Temporal Collinearity, GTC）极高**。实验测量显示，直接编码的 GTC 值在 0.8–0.9 之间，而率编码（rate encoding）仅为 0.2–0.3（Figure 1）。

### 梯度时间共线性如何损害鲁棒性

GTC 对鲁棒性的破坏机制可以通过参数 Hessian 矩阵的谱半径来理解。给定两个时间步 $i$ 和 $j$ 的梯度分量 $G[i]$ 和 $G[j]$，GTC 定义为它们的 Frobenius 内积与各自 Frobenius 范数之比：

$$\mathcal{C}(G[i], G[j]) = \frac{\langle G[i], G[j] \rangle_F}{\|G[i]\|_F \cdot \|G[j]\|_F}$$

该度量刻画了梯度分量在参数空间中的方向一致性。理论分析表明，参数 Hessian 的谱半径上界与 GTC 呈正相关：

$$\lambda_{\max}(\widehat{H}_\theta) \lesssim T \cdot (\max_t \|G[t]\|_F^2) \cdot [1 + (T-1) \cdot \max_{i \neq j} \mathcal{C}(G[i], G[j])]$$

**当 GTC 升高时，Hessian 谱半径被放大，损失景观变得更加尖锐，网络对输入扰动的敏感性急剧增加**。这正是直接编码 SNN 在对抗攻击下表现脆弱的结构性根源。

### 现有方法的缺口

率编码通过在每个时间步生成不同的泊松脉冲序列，天然引入了时间多样性，从而降低了 GTC。但这一机制以牺牲效率为代价——率编码需要更长的仿真时间来准确表征输入，且脉冲生成过程本身增加了计算开销。其他现有防御方法（如对抗训练、正则化技术）虽然能提供一定程度的鲁棒性提升，但并未触及直接编码中 GTC 过高这一根本问题。

**核心挑战在于：能否在不牺牲直接编码高效性的前提下，引入类似率编码的时间特征多样性机制，从而打破梯度时间共线性？** 这需要一个既能降低 GTC、又能保持直接编码简洁性的结构化方案。

## 核心创新

### 问题瓶颈：梯度时间共线性（GTC）

直接编码（direct encoding）在每个时间步重复注入相同的静态图像输入，导致不同时间步的梯度分量在方向上高度一致。这种**梯度时间共线性（Gradient Temporal Collinearity, GTC）**被定义为两个时间步梯度分量之间的归一化 Frobenius 内积：

$$\mathcal{C}(G[i], G[j]) = \frac{\langle G[i], G[j] \rangle_F}{\|G[i]\|_F \cdot \|G[j]\|_F}$$

实验表明（Figure 1），直接编码的 epoch 平均 GTC 维持在 0.8–0.9，而率编码（rate encoding）仅为 0.2–0.3。这种高共线性并非无害——论文通过理论分析（Eq. 5）证明，GTC 会放大参数 Hessian 矩阵的谱半径上界：

$$\lambda_{\max}(\widehat{H}_\theta) \lesssim T \cdot (\max_t \|G[t]\|_F^2) \cdot [1 + (T-1) \cdot \max_{i \neq j} \mathcal{C}(G[i], G[j])]$$

Hessian 谱半径越大，损失函数在扰动下的波动上界越高（Eq. 46），网络鲁棒性越差。这解释了为何直接编码 SNN 即使结合对抗训练（AT），在白盒攻击下仍表现脆弱（CIFAR-10 PGD 准确率仅 14.07%）。

### 因果操纵杆：打破 GTC 的结构化正交去相关

STOD 的核心思路是：**在直接编码的输入层引入结构化正交变换，降低梯度时间共线性，从而缩小 Hessian 谱半径，提升鲁棒性**。这一定位决定了两个关键 changed slots：

| Slot | Baseline（直接编码） | STOD |
|------|---------------------|------|
| 输入变换 | 恒等映射（每时间步重复相同输入） | **Patchwise Feature Diversification (PFD)**：将输入分块后，每时间步使用独立的参数化正交核进行变换 |
| 正则化 | 无 | **Global Orthogonal Regularization (GOR)**：惩罚不同时间步变换输入之间的余弦相似度 |

### PFD：时间步特征多样化

PFD 在每个时间步 $t$ 应用一个独立的参数化正交核 $\mathcal{O}[t]$，对输入 $X[t]$ 进行分块变换：

$$X'[t] = \operatorname{vec}\left[ \mathcal{P}^{-1}\bigl( \mathcal{P}(X[t]) \otimes \mathcal{O}[t] \bigr) \right]$$

其中 $\mathcal{P}$ 将输入划分为 $p \times p$ 的分块，$\otimes$ 表示分块级正交变换。正交核通过 Householder 反射初始化，确保不同时间步的核相互正交：

$$Q[j] = I_d - 2\frac{k_j k_j^\top}{k_j^\top k_j}$$

训练中采用 RiemannianSGD 优化器在 Stiefel 流形上保持正交性。这种设计确保每个时间步看到的是同一图像的**不同正交视角**，从而在保留特征保持能力的同时打破梯度方向一致性。

### GOR：全局方向分离的软约束

PFD 提供了结构化的特征多样化机制，但仅靠正交核的硬约束不足以保证梯度分量充分去相关。GOR 作为软正则化项加入损失函数，直接惩罚不同时间步归一化变换输入之间的余弦相似度：

$$\mathcal{L}_\mathcal{O} = \sum_{1 \le i < j \le T} \cos^2(X'[i], X'[j])$$

最终训练目标为：

$$\mathcal{L} = \mathcal{L}_{CE} + \lambda_\mathcal{O} \mathcal{L}_\mathcal{O}$$

### 推理时的关键设计选择

消融实验（Table 2）揭示了一个重要发现：**训练时引入正交核、推理时移除（STOD w.o. OK），可获得最大的鲁棒性增益，且不增加任何推理开销**。这表明正交核的作用本质上是训练正则化——通过重塑梯度景观来提升网络的内在鲁棒性，而非依赖推理时的特征多样化。这一策略使 STOD 在 CIFAR-10 上仅以约 2% 的干净准确率下降为代价，将 PGD 白盒攻击准确率从 14.07% 提升至 43.54%（Table 8）。

## 整体框架

![[assets/figures/papers/iclr26_0012_udTDFAshNM_Breaking_Gradient_Temporal_Collinearity_for_Robu/figures/003_Figure_2.jpg]]
*Figure 2: Flowchart of STOD, including PFD and GOR*

STOD 的整体设计遵循“在直接编码的输入层引入结构化时间正交去相关，以降低梯度时间共线性（GTC）”这一核心思路。其 pipeline 由两个关键模块构成：**Patchwise Feature Diversification (PFD)** 和 **Global Orthogonal Regularization (GOR)**，二者协同工作，在不牺牲直接编码高效率和特征保持能力的前提下，有效打破时间步间梯度分量的方向一致性。

### 输入输出流

1. **输入**：静态图像 $X \in \mathbb{R}^{C \times H \times W}$，与标准直接编码 SNN 相同。
2. **时间展开**：输入在每个时间步 $t \in \{1, \dots, T\}$ 被复制为 $X[t] = X$。
3. **PFD 变换**：每个时间步的输入经过独立的参数化正交核 $\mathcal{O}[t]$ 进行分块变换，得到多样化特征 $X'[t]$（详见 Eq. 6）。
4. **SNN 前向传播**：变换后的序列 $\{X'[t]\}_{t=1}^T$ 送入后续 LIF 脉冲神经网络进行时序处理。
5. **损失计算**：总损失 $\mathcal{L} = \mathcal{L}_{CE} + \lambda_{\mathcal{O}} \mathcal{L}_{\mathcal{O}}$，其中 $\mathcal{L}_{CE}$ 为标准交叉熵损失，$\mathcal{L}_{\mathcal{O}}$ 为全局正交正则化项（Eq. 8–9）。
6. **输出**：网络末层的脉冲发放率经解码后产生分类预测。

### 模块关系

- **PFD** 是硬约束模块：通过 Stiefel 流形上的 Riemannian SGD 优化器保持正交核的正交性，从结构上强制时间步间特征方向分离。
- **GOR** 是软约束模块：作为损失函数的正则化项，最小化归一化变换输入 $\hat{X}'[i]$ 与 $\hat{X}'[j]$ 之间的余弦相似度平方和，进一步引导时间步间特征方向正交化。
- 两个模块形成“结构化变换 + 全局正则化”的双重机制：PFD 提供逐时间步的局部多样化，GOR 在全局层面抑制残余的共线性。

### 推理时变体

消融实验揭示了一个关键发现：正交核的主要作用是训练阶段的**正则化**，而非推理阶段的特征提取。因此，论文提出了 **STOD w.o. OK** 变体——训练时保留 PFD 和 GOR，推理时移除正交核。该变体在不引入任何额外推理开销的情况下，仍能获得显著优于基线 SNN 的鲁棒性（Table 2），证实了 STOD 通过降低 GTC 来重塑损失景观、从而内在地提升鲁棒性的机制。

### 与基线的关键差异

| 组件 | 直接编码 SNN（基线） | STOD |
|------|---------------------|------|
| 输入变换 | 恒等（$X[t] = X$） | PFD：分块正交核变换 |
| 正则化 | 无 | GOR：跨时间步余弦相似度惩罚 |
| 正交性约束 | 无 | Riemannian SGD 在 Stiefel 流形上优化 |
| GTC 水平 | 高（约 0.8–0.9） | 显著降低 |
| 推理开销 | 无额外开销 | STOD w.o. OK 同样无额外开销 |

这一框架的核心洞察在于：直接编码的高 GTC 并非其固有属性，而是输入层缺乏时间多样性的结果。通过在输入端引入结构化正交变换来打破这种共线性，即可在保留直接编码高效率和特征保持能力的同时，大幅提升 SNN 的对抗鲁棒性。

## 核心模块与公式推导

### 核心瓶颈：梯度时间共线性（GTC）

直接编码（direct encoding）在每个时间步重复注入相同的静态输入，导致不同时间步的梯度分量方向高度一致。为量化这一现象，论文定义了**梯度时间共线性**（Gradient Temporal Collinearity, GTC）：

$$
\mathcal{C}(G[i], G[j]) = \frac{\langle G[i], G[j] \rangle_F}{\|G[i]\|_F \cdot \|G[j]\|_F}
$$

其中 $G[i]$ 表示第 $i$ 个时间步的梯度分量，$\langle\cdot,\cdot\rangle_F$ 为 Frobenius 内积。该度量取值范围为 $[0,1]$，值越大表示两个时间步的梯度方向越趋于共线。

实验表明，直接编码的 GTC 约为 0.8–0.9，而率编码（rate encoding）仅为 0.2–0.3（Figure 1），且这一差异与鲁棒性差距密切相关。

### 因果机制：GTC 如何损害鲁棒性

高 GTC 通过放大参数 Hessian 的谱半径来降低网络鲁棒性。理论分析给出如下上界：

$$
\lambda_{\max}(\widehat{H}_\theta) \lesssim T \cdot (\max_t \|G[t]\|_F^2) \cdot \left[1 + (T-1) \cdot \max_{i \neq j} \mathcal{C}(G[i], G[j])\right]
$$

该式揭示了关键因果链：时间步数 $T$ 固定时，GTC（即 $\max_{i \neq j} \mathcal{C}(G[i], G[j])$）直接控制 Hessian 谱半径的放大倍数。谱半径越大，损失曲面越尖锐，对抗扰动下的损失波动越剧烈，鲁棒性越差。

### STOD 方法：两组件协同降 GTC

STOD（Structured Temporal Orthogonal Decorrelation）在直接编码的输入层引入两个关键模块，目标是**降低 GTC 同时保留特征保持能力**。

#### 组件一：Patchwise Feature Diversification（PFD）

PFD 将输入 $X[t]$ 分块后，在每个时间步使用独立的参数化正交核 $\mathcal{O}[t]$ 进行变换：

$$
X'[t] = \operatorname{vec}\left[ \mathcal{P}^{-1}\bigl( \mathcal{P}(X[t]) \otimes \mathcal{O}[t] \bigr) \right]
$$

其中 $\mathcal{P}$ 为分块操作，$\otimes$ 表示逐块矩阵乘法。正交核 $\mathcal{O}[t]$ 满足 $\mathcal{O}[t]^\top \mathcal{O}[t] = I$，通过 Householder 反射初始化以保证不同时间步的核相互正交：

$$
Q[j] = I_d - 2\frac{k_j k_j^\top}{k_j^\top k_j}
$$

正交核在 Stiefel 流形上通过 RiemannianSGD 优化，确保训练过程中保持正交性。

#### 组件二：Global Orthogonal Regularization（GOR）

GOR 作为软约束加入损失函数，进一步惩罚不同时间步变换后特征的方向相似性：

$$
\mathcal{L}_\mathcal{O} = \sum_{1 \le i < j \le T} \cos^2(X'[i], X'[j])
$$

其中 $X'[i]$ 为归一化后的变换输入。该正则化项直接最小化时间步间特征的余弦相似度平方，从优化目标层面强制特征方向分离。

#### 最终训练目标

$$
\mathcal{L} = \mathcal{L}_{CE} + \lambda_\mathcal{O} \mathcal{L}_\mathcal{O}
$$

$\lambda_\mathcal{O}$ 控制正则化强度，实验表明最优值为 0.05（Figure 6），能在 GTC 降低和干净准确率保持之间取得良好平衡。

### 推理时策略

消融实验揭示了一个关键发现（Table 2）：正交核在训练时引入、推理时移除（变体 STOD w.o. OK），可获得最大的鲁棒性增益，且不增加任何推理开销。这表明正交核的作用本质上是**训练正则化**——通过多样化时间特征来重塑梯度结构，使网络习得内在鲁棒表征，而非依赖推理时的特征变换。

## 实验与分析

### 核心瓶颈验证：GTC 与鲁棒性的因果链

论文首先通过实验验证了其核心假设——梯度时间共线性（GTC）是损害直接编码 SNN 鲁棒性的关键因子。如 Figure 1 所示，直接编码（direct encoding）的 epoch 平均 GTC 在训练过程中始终维持在 0.8–0.9 的高位，而率编码（rate encoding）的 GTC 则稳定在 0.2–0.3 的低位。这一差距与两种编码方式在鲁棒性上的表现差异高度吻合，为 GTC 作为鲁棒性瓶颈提供了初步实证。

![[assets/figures/papers/iclr26_0012_udTDFAshNM_Breaking_Gradient_Temporal_Collinearity_for_Robu/figures/002_Figure_1.jpg]]
*Figure 1: GTC evaluation curves*

理论层面，Equation (5) 建立了 GTC 到参数 Hessian 谱半径的上界关系：

$$\lambda_{\max}(\widehat{H}_\theta) \lesssim T \cdot (\max_t \|G[t]\|_F^2) \cdot [1 + (T-1) \cdot \max_{i \neq j} \mathcal{C}(G[i], G[j])]$$

该上界表明，更高的 GTC 会直接放大 Hessian 谱半径，而更大的谱半径意味着损失景观更尖锐，模型对输入扰动的敏感度更高，鲁棒性更差。这一理论推导构成了 STOD 方法设计的核心动机。

### 主实验结果

**白盒攻击下的鲁棒性提升。** Table 1 报告了在 CIFAR-10、CIFAR-100 和 ImageNet 上的白盒鲁棒性对比。STOD w.o. OK（推理时移除正交核的变体）在 CIFAR-10 上取得了 FGSM 55.80% 和 PGD 32.97% 的最高鲁棒准确率，显著优于 vanilla SNN 的 14.07%（PGD）。在 CIFAR-100 上，STOD w.o. OK 同样以 FGSM 26.26%、PGD 13.13% 领先。ImageNet 上，STOD 的 FGSM 准确率达到 26.77%，而基线 SNN+AT 仅为 15.74%。

![[assets/figures/papers/iclr26_0012_udTDFAshNM_Breaking_Gradient_Temporal_Collinearity_for_Robu/figures/004_Table_1.jpg]]
*Table 1: White box performance comparison. The highest accuracy in each column is highlighted in bold. ’*’ indicates self-implementation results*

Table 2 的消融进一步表明，训练时引入正交核（OK）可在 STOD w.o. OK 的基础上再获得 1.85–5.89 个百分点的 FGSM 增益（CIFAR-10: +3.36, CIFAR-100: +5.89），同时仅带来 0.31–0.56% 的轻微干净准确率下降。这验证了正交核在训练阶段作为正则化手段的核心价值——通过多样化时间特征表示来降低 GTC，且推理时移除正交核可在不增加推理开销的前提下保留大部分鲁棒性增益。

![[assets/figures/papers/iclr26_0012_udTDFAshNM_Breaking_Gradient_Temporal_Collinearity_for_Robu/figures/005_Table_2.jpg]]
*Table 2: White box performance comparison with-/without orthogonal kernels*

**结合对抗训练的进一步提升。** Table 8 展示了与对抗训练（AT）结合后的效果。STOD + AT 在 CIFAR-10 上达到 PGD 43.54%，相比 SNN + AT 的 14.07% 提升了 29.47 个百分点。在 CIFAR-100 和 ImageNet 上，FGSM 准确率分别从 16.31% 提升至 41.89%（+25.58）和从 15.74% 提升至 26.77%（+11.03）。这表明 STOD 与 AT 之间存在协同效应：AT 通过对抗样本增强损失景观的平坦性，而 STOD 通过降低 GTC 从结构上抑制 Hessian 谱半径，两者互补。

![[assets/figures/papers/iclr26_0012_udTDFAshNM_Breaking_Gradient_Temporal_Collinearity_for_Robu/figures/019_Table_8.jpg]]
*Table 8: White box performance (with AT) comparison. The highest accuracy in each column is highlighted in bold. ’*’ indicates self-implementation results*

**不同攻击强度下的鲁棒性。** Figure 3 展示了在 ε/255 从 0 到 128 范围内，STOD 与基线 SNN 在白盒和黑盒攻击下的性能曲线。STOD 在所有扰动强度下均保持显著优势，且白盒与黑盒攻击之间的性能差距较小，表明其鲁棒性并非来自梯度混淆（gradient obfuscation）。Table 9 提供了 Figure 3 的详细数值结果。

![[assets/figures/papers/iclr26_0012_udTDFAshNM_Breaking_Gradient_Temporal_Collinearity_for_Robu/figures/007_Figure_3.jpg]]
*Figure 3: Performance comparison under white and black box attacks*

**梯度混淆检查。** 为排除虚假鲁棒性的可能，Table 5 报告了梯度混淆检查清单的结果。STOD 通过了所有 5 项检查（包括增加攻击迭代次数不降低攻击成功率、黑盒攻击不显著弱于白盒攻击等），证实其鲁棒性提升是真实的。

### 消融实验与超参数分析

**正交核的作用机制。** Table 2 的核心发现是：训练时使用正交核、推理时移除的策略（STOD w.o. OK）可获得最佳的"鲁棒性-效率"权衡。这揭示了正交核的本质角色——它们是训练阶段的特征多样化正则器，而非推理阶段必需的组件。正交核通过强制不同时间步的输入变换方向正交化，从源头降低了 GTC，使得网络在训练过程中学会了更鲁棒的特征表示。

**分块大小 p 的影响。** Figure 5 和 Table 10 展示了不同分块大小 p 和时间步数 T 下的鲁棒性变化。最优分块大小为 p=8，在大多数 T 设置下均达到峰值准确率。过小的 p（如 2）限制了正交变换的表达能力，而过大的 p（如 32）可能导致特征过度压缩，损害干净准确率。这一超参数需要在特征多样性和信息保留之间取得平衡。

**正则化强度 λ_O 的影响。** Figure 6 展示了 λ_O 从 0 到 0.5 变化时，鲁棒准确率和 GTC 的变化趋势。最优值出现在 λ_O = 0.05，此时 GTC 显著降低且准确率保持稳定。过大的 λ_O 会过度约束特征方向，导致干净准确率下降；过小的 λ_O 则无法有效降低 GTC。

**攻击迭代次数的影响。** Table 11 报告了不同 PGD 步数 K（7 到 100）下的鲁棒性变化。STOD 在所有 K 值下均保持优势，且性能随 K 增加而缓慢下降，在 K=50–60 后趋于稳定，进一步排除了梯度混淆的可能性。

### 可视化分析

Figure 4 展示了原始输入、经 PFD 变换后的输入以及对应梯度分量的可视化。尽管 PFD 变换后的输入在视觉上难以辨识，但其梯度分量清晰揭示了图像从不同视角的结构模式。这表明 STOD 并非简单破坏输入信息，而是通过正交变换将输入投影到多个互补的特征子空间，使网络能够从多样化视角学习鲁棒特征。

### 失败模式与局限

1. **干净准确率的轻微下降。** 在 CIFAR-10 上，STOD 的干净准确率相比 vanilla SNN 下降约 2%（Table 1）。这是鲁棒性-准确率权衡的体现，源于梯度重塑对标准训练目标的干扰。

2. **对对抗训练的依赖。** 最优鲁棒性需要 STOD 与 AT 结合使用（Table 8）。单独使用 STOD 的效果虽优于基线，但尚未在无 AT 设置下进行充分验证。

3. **序列长度的限制。** 正交核的 Householder 初始化要求时间步数 T ≤ 输入通道数 × 分块维度，这限制了极长序列场景下的可扩展性。

4. **任务泛化性未验证。** 当前实验仅覆盖图像分类任务（静态图像和神经形态数据集），STOD 在视频理解、强化学习等序列决策任务上的有效性仍需探索。

## 方法谱系与知识库定位

### 方法定位与核心差异

STOD 的出发点是直接编码（direct encoding）在脉冲神经网络（SNN）中面临的一个被长期忽视的结构性瓶颈：**梯度时间共线性（Gradient Temporal Collinearity, GTC）**。直接编码在每个时间步重复注入相同的静态输入，导致不同时间步的梯度分量在方向上高度一致（GTC 约 0.8–0.9，见 Figure 1），这会通过 Hessian 谱半径的上界（Eq. 5）放大参数 Hessian 的谱半径，从而严重损害网络的对抗鲁棒性。

与直接编码形成对照的是率编码（rate encoding），后者通过泊松采样引入时间多样性，GTC 仅约 0.2–0.3，因而天然具有更好的鲁棒性。但率编码的代价是编码效率低、特征保持能力差——这正是直接编码的优势所在。STOD 的策略是在**保留直接编码高效率和特征保持能力的前提下，通过结构化变换降低 GTC**，从而在不牺牲推理效率的前提下大幅提升鲁棒性。

在方法谱系中，STOD 与现有 SNN 鲁棒性方法的根本区别在于：它不修改脉冲神经元动力学、不引入额外的脉冲正则化、不依赖更复杂的网络架构，而是**仅在输入层引入参数化正交核（PFD）和全局正交正则化（GOR）**，从根源上打破梯度时间共线性。这与基于对抗训练（AT）的 SNN 防御方法（如 HIRE-SNN、SEW-ResNet + AT）是正交的——实际上，STOD 的最优效果正是在与对抗训练结合时取得的（Table 8）。

### 适用边界

**有效的前提条件：**

1. **编码方式为直接编码。** STOD 的设计假设输入在每个时间步是相同的静态图像（或帧），这正是直接编码的特征。对于率编码或事件驱动的神经形态数据（如 DVS），GTC 本身较低，STOD 的增益可能有限——尽管实验表明在 DVS-CIFAR10 和 DVS-Gesture 上仍有效果（Table 4）。
2. **时间步数 T 受限于输入通道数 × 分块维度。** 正交核的初始化策略要求 $T \leq C_{\text{in}} \times p^2$，这是因为需要保证 T 个正交核在 Stiefel 流形上相互正交。对于极长序列，这一约束限制了直接扩展性。
3. **最优鲁棒性依赖对抗训练。** 单独使用 STOD 而不结合对抗训练的效果尚未在论文中充分验证；主要实验结果（Table 1, Table 8）均以对抗训练为基础设置。

**已验证的任务域：**
- 静态图像分类：CIFAR-10/100, ImageNet（白盒与黑盒攻击）
- 神经形态数据分类：DVS-CIFAR10, DVS-Gesture
- 尚未验证的域：视频理解、强化学习、序列预测等长时序任务

### 关键局限

1. **干净准确率的轻微下降。** STOD 在提升鲁棒性的同时，会带来约 2% 的干净准确率损失（CIFAR-10 上从 93.04% 降至 91.09%，见 Table 1）。这是梯度重塑（gradient reshaping）方法的常见代价——正交核对输入特征的变换虽然降低了 GTC，但也部分牺牲了原始特征的保真度。

2. **推理时正交核的取舍困境。** 消融实验（Table 2）揭示了一个有趣的现象：训练时使用正交核、推理时移除（STOD w.o. OK）可获得最佳的鲁棒性-效率平衡，且不引入额外推理开销。然而，若在推理时保留正交核以维持特征多样性，则会引入额外计算。目前尚无方案能在推理阶段保留正交核而不显著增加开销。

3. **正交核初始化对序列长度的硬约束。** $T \leq C_{\text{in}} \times p^2$ 的限制意味着对于高时间步数的应用（如 $T > 100$），需要更大的输入通道数或分块尺寸，这可能不切实际。

4. **超参数敏感性。** 最优分块大小 $p=8$（Figure 5）和最优正则化强度 $\lambda_{\mathcal{O}}=0.05$（Figure 6）是在 CIFAR 规模上调节得到的。对于不同规模的数据集或网络架构，这些超参数可能需要重新搜索，增加了调参负担。

### 开放问题

1. **推理阶段保留正交核的高效变体设计。** 能否通过低秩分解、知识蒸馏或条件计算，在推理时以可忽略的代价保留正交核带来的特征多样性？这是将 STOD 从“训练时正则化”升级为“推理时增强”的关键。

2. **自适应 GTC 控制。** 当前 STOD 使用固定的正交核数量和正则化强度。能否设计一种机制，根据当前 GTC 水平动态调整变换强度，在干净准确率和鲁棒性之间实现更精细的权衡？

3. **大规模 SNN 与长序列扩展。** STOD 在 VGG-11 规模的 SNN 和 $T \leq 16$ 的设置下验证有效。对于更深（如 ResNet-101 级别的 SNN）、更宽或时间步数更多的模型，GTC 的放大效应是否会发生变化？STOD 的收益是否可扩展？这需要进一步验证。

4. **与其他鲁棒性机制的协同。** STOD 目前仅与对抗训练结合。它与 SNN 领域的其他防御技术（如脉冲正则化、膜电位平滑、时序注意力机制）是否具有叠加效应，仍有待探索。

5. **理论边界的紧致性。** Eq. (5) 给出的 Hessian 谱半径上界依赖于 GTC 的最大值，但该上界是否为紧致界（tight bound）尚不明确。更紧致的理论分析可能揭示更优的 GTC 降低策略。

> **注意：** 上述开放问题中，第 1 点和第 2 点来自论文自身的讨论（Section 6），第 3–5 点为基于方法局限性的合理推断，需进一步实验验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Breaking_Gradient_Temporal_Collinearity_for_Robust_Spiking_Neural_Networks.pdf]]
