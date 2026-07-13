---
title: "Navigating the Latent Space Dynamics of Neural Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Navigating_the_Latent_Space_Dynamics_of_Neural_Models.pdf
project_link: null
code_link: null
openreview_forum_id: Zunww3FHPU
aliases:
- NLSDNM
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "该框架反复迭代自编码器的编码器-解码器复合映射，以提取潜在空间向量场和吸引子。"
primary_logic: "从任意AE定义f等于E组合D，追踪潜在轨迹和不动点，再用吸引子分析记忆泛化与OOD信号。"
claims:
- "任意自编码器的编码解码循环天然定义潜在向量场，无需额外训练即可分析。"
- "吸引子对齐数据分布高密度区域，并可作为网络权重中存储信息的稀疏字典。"
- "潜在轨迹得分可用于分布外检测，并在ViT-MAE实验中优于KNN特征距离基线。"
---

# Navigating the Latent Space Dynamics of Neural Models

> [!tip] 核心洞察
> Navigating

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Navigating the Latent Space Dynamics of Neural Models |
| 英文题名 | Navigating the Latent Space Dynamics of Neural Models |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=Zunww3FHPU) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method |  |
| Dataset | |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

本文揭示了一个被长期忽视的现象：**任意自编码器（AE）在其潜在空间中天然定义了一个向量场**。该向量场通过反复迭代编码器-解码器映射 $f(\mathbf{z}) = E \circ D(\mathbf{z})$ 自然涌现，无需任何额外训练。这一发现将自编码器的行为重新解释为一种**潜在空间中的动力学系统**，其不动点——即吸引子——编码了网络权重中存储的关于训练数据的信息。

**核心瓶颈**：自编码器的泛化与记忆能力缺乏统一的几何解释框架，难以从权重中直接提取模型习得的数据表征。

**因果旋钮**：编码器-解码器复合映射 $f(\mathbf{z})$ 的**局部收缩性**（local contractivity）是驱动潜在动力学行为的核心机制。训练目标（MSE重建损失）、数据增强及权重衰减等正则化手段，均隐式地降低了雅可比矩阵的谱范数 $\|J_f(\mathbf{z})\|_\sigma$，从而促进收缩行为。

**核心洞见**：当自编码映射在局部收缩且充分逼近数据分布 $p(\mathbf{x})$ 时，潜在向量场所诱导的动力学 $f(\mathbf{z}) - \mathbf{z}$ 局部正比于潜在先验的得分函数 $\nabla_\mathbf{z} \log q(\mathbf{z})$。这意味着**潜在空间中的吸引子自然对齐于数据分布的高密度区域**，且吸引子的数量与解码质量受瓶颈维度 $k$（即 $J_f$ 的秩）调控——低秩促进泛化，高秩导致记忆。

**方法定位**：本文的方法属于**无训练后验分析框架**，而非提出新的模型架构。它提供了一套统一的视角来理解各类自编码器变体（标准AE、去噪AE、掩码AE等），将它们视为最小化重建误差外加促进局部收缩性的隐式正则项（见 Table 3）。该方法可应用于任意预训练自编码器，无需访问训练数据即可从权重中提取表征信息。

**主要结果**：
- 在 MNIST/CIFAR 等数据集上，通过可视化 2D 潜在向量场（Figure 1, Figure 3），验证了吸引子从初始单点逐步分裂、最终稳定于数据流形附近的过程。
- 定义了**记忆系数**（memorization coefficient）和**轨迹得分**（trajectory score），量化了模型从记忆到泛化的相变过程（Figure 2, Figure 3b-c）。
- 在 Stable Diffusion 的 VAE 上展示了**无数据权重信息探测**：使用吸引子作为稀疏基重建图像，其 MSE 显著优于随机正交基（Figure 4），证明了吸引子确实压缩了训练数据的关键信息。
- 在 ViT-MAE 上，利用潜在轨迹得分进行**分布外检测**，AUROC 大幅超越 KNN 基线（Figure 5, Table 1）。

**证据强度**：核心理论（定理 1）给出了局部收缩条件下向量场与得分函数的关系，附录提供了完整证明；所有实验现象在多个模型和数据集上一致复现。需要手动验证的是：该框架对非收缩性自编码器（如 VQ-VAE 中的离散潜在空间）的适用边界尚未充分讨论。

自编码器（Autoencoder, AE）及其变体——从去噪自编码器、变分自编码器到掩码自编码器——在生成建模、表征学习和视觉基础模型中扮演着核心角色。然而，这些模型内部潜在空间的结构特性，尤其是编码器-解码器映射的动力学行为，长期以来未被系统性地揭示。

**核心发现：潜在向量场的自然涌现。** 本文揭示了一个被忽视的普遍现象：对于任意给定的自编码器架构，其编码器 $E$ 与解码器 $D$ 的组合映射 $f(\mathbf{z}) = E \circ D(\mathbf{z})$ 在潜在空间中定义了一个向量场。通过反复迭代 $\mathbf{z}_{t+1} = f(\mathbf{z}_t)$，该向量场自然涌现，无需任何额外训练。这一发现将自编码器的潜在空间从一个静态的表征容器重新定义为一个具有内在动力学结构的动态系统。

**吸引子与数据分布的对应关系。** 实验观察表明，该向量场中的吸引子（即映射 $f$ 的不动点，满足 $f(\mathbf{Z}^*) = \mathbf{Z}^*$）与训练数据的高密度区域高度对齐。在 MNIST 上的二维可视化（Figure 1）清晰展示了这一现象：不同随机初始化下的自编码器均表现出吸引子聚集于数据流形附近的行为。这意味着自编码器的训练过程在潜在空间中自发地组织起了一个以数据为中心的吸引子结构。

**现有方法的缺口。** 此前对自编码器潜在空间的研究主要关注表征的几何性质（如流形学习、解纠缠），或利用潜在空间进行生成与重建。然而，这些工作将潜在空间视为静态对象，忽略了编码器-解码器映射反复迭代所蕴含的动力学信息。具体而言，以下问题尚未得到充分探索：
- 潜在向量场的吸引子结构如何反映模型的记忆与泛化能力？
- 该动力学框架能否推广至现代视觉基础模型（如 ViT-MAE、Stable Diffusion）甚至自监督学习模型（如 DINOv2）？
- 向量场的轨迹信息能否为分布偏移检测、无数据权重探测等下游任务提供新的信号？

**本文动机。** 基于上述观察，本文旨在建立一个统一的动力学框架来理解自编码器的潜在空间行为，并探索其在现代大规模模型中的普适性与应用价值。核心假设是：训练目标（如均方误差重建损失 $\mathcal{L}_{MSE}(\mathbf{x}) = \sum_{\mathbf{x} \in X} \| \mathbf{x} - F_{\Theta}(\mathbf{x}) \|_2^2$ 及其变体）隐式地促进了映射 $f$ 的收缩性，从而在潜在空间中形成了稳定的吸引子结构。本文通过系统的理论分析与跨模型实验，验证这一框架的解释力与实用潜力。

## 核心方法与创新机理

本工作并非提出一种新的自编码器架构或训练算法，而是**发现并形式化了一个所有自编码器（AE）共有的内在结构——隐式潜变量向量场（latent vector field）**。核心创新在于视角的转换：将 AE 不再视为一个静态的“编码-解码”映射，而是视为一个在潜空间中迭代演化的动力系统。

### 关键创新点

1. **潜变量向量场的发现与形式化**
   对于任意自编码器，定义映射 $f(\mathbf{z}) = E \circ D(\mathbf{z})$，其迭代应用 $f(\cdots f(f(\mathbf{z})))$ 自然诱导出一个潜空间向量场。该向量场可通过离散 ODE 刻画：
   $$\begin{cases} \mathbf{z}_{t+1} = f(\mathbf{z}_t) \\ \mathbf{z}_0 = \mathbf{z} \end{cases}$$
   并对应连续微分方程 $\frac{\partial \mathbf{z}}{\partial t} = f(\mathbf{z}) - \mathbf{z}$。这一结构**无需任何额外训练**，仅通过迭代编码-解码映射即可揭示。

2. **吸引子作为网络知识的压缩表征**
   向量场的不动点（满足 $f(\mathbf{Z}^*) = \mathbf{Z}^*$）构成吸引子。这些吸引子天然形成对训练数据分布的稀疏字典编码——高密度数据区域对应吸引子，低密度区域则被推向邻近吸引子。这为理解 AE 的泛化与记忆提供了统一框架：瓶颈维度 $k$ 通过限制 Jacobian $J_f(\mathbf{z})$ 的秩，调控吸引子数量，从而在记忆训练样本与泛化之间权衡。

3. **训练目标与收缩性的因果关联**
   论文论证了标准 AE 训练目标（MSE 重构损失及数据增强）隐含地促进映射 $f$ 的局部收缩性（降低 Jacobian 的谱范数 $\|J_f(\mathbf{x})\|_\sigma$），这是向量场形成有意义吸引子的动力学基础。该收缩性源于初始化偏差、显式正则化与隐式正则化的共同作用。

4. **无需训练的模型探针**
   基于上述理论，吸引子可作为一种**数据无关的权重信息探针**：仅从高斯噪声出发寻找不动点，即可恢复网络权重中编码的训练数据信息。这为理解大规模预训练模型（如 Stable Diffusion、ViT-MAE）的内部表征提供了新工具。

### 与 baseline 的本质差异

传统 AE 研究关注重构质量、隐空间几何或表征学习性能，本工作则**将 AE 重新解释为潜空间中的确定性动力系统**。这一视角转变带来了几个 baseline 方法不具备的能力：
- 无需训练即可从任意 AE 中提取吸引子字典
- 通过潜轨迹分析实现分布偏移检测（OOD detection），其性能显著优于基于 KNN 的基线（FPR95 降低约 5-65 个百分点）
- 为 AE 的泛化-记忆权衡提供了基于吸引子动力学的可量化解释

> **注意**：论文未提供与特定命名 baseline 方法的直接对比表格，上述性能优势基于 Figure 5 中与 KNN 基线的比较。若需与其他 OOD 检测方法（如 Mahalanobis 距离、重构误差基线）的完整对比，请参见附录 Table 1。

本文提出了一种将任意自编码器（AE）隐式表征为**潜在向量场**的分析框架，无需额外训练或修改模型权重。整个框架围绕一个核心映射展开：

$$f(\mathbf{z}) = E \circ D(\mathbf{z})$$

其中 $E$ 为编码器，$D$ 为解码器，$\mathbf{z}$ 为潜在空间中的点。该映射的迭代应用 $f(\cdots f(f(\mathbf{z})))$ 在潜在空间中定义了一个离散动力学过程，并可进一步建模为连续微分方程：

$$\frac{\partial \mathbf{z}}{\partial t} = f(\mathbf{z}) - \mathbf{z}$$

**框架的输入-输出流**如下：
1. **输入**：任意（可能已预训练的）自编码器模型 $(E, D)$。
2. **潜在向量场构建**：定义映射 $f(\mathbf{z}) = E \circ D(\mathbf{z})$，其残差 $f(\mathbf{z}) - \mathbf{z}$ 即为潜在空间中各点的向量场。
3. **动力学分析**：通过迭代 $f$ 或求解 ODE，追踪潜在空间中点的演化轨迹，并识别不动点（吸引子）$\mathbf{Z}^*$，即满足 $f(\mathbf{Z}^*) = \mathbf{Z}^*$ 的点。
4. **输出**：吸引子集合构成网络权重的信息字典，可用于重建（通过正交匹配追踪）、分布外检测（通过轨迹到训练吸引子的距离）等下游分析。

**核心模块关系**：
- **编码器-解码器对**：作为黑箱使用，不修改参数，仅通过函数复合产生向量场。
- **向量场动力学**：揭示模型的收缩性——训练目标（MSE损失、数据增强）和初始化偏置使 $f$ 具有局部收缩性，导致潜在空间中的点沿向量场流向吸引子。
- **吸引子分析**：吸引子被视为网络权重中存储信息的压缩表示。通过记忆系数 $\operatorname{mem}(\mathbf{z}^*) = \min_{\mathbf{x} \in \mathcal{X}_{train}} \cos(D(\mathbf{z}^*), \mathbf{x})$ 和轨迹评分 $\operatorname{score}(\mathbf{z}) = \frac{1}{N} \sum_{\mathbf{z}_i \in \pi(\mathbf{z})} d(\bar{\mathbf{z}}_i, \bar{\mathbf{Z}}_{train}^*)$，框架可量化模型的记忆-泛化权衡及分布偏移检测能力。

该框架的普适性在于：它不依赖特定架构或训练范式，仅利用AE固有的编码-解码循环即可揭示其隐式几何结构。

### 核心模块：从自编码器到隐向量场

本文方法的核心操作极其简洁——**无需额外训练，直接从任意（预训练）自编码器提取一个隐向量场**。给定自编码器的编码器 $E$ 和解码器 $D$，定义映射：

$$f(\mathbf{z}) = E \circ D(\mathbf{z})$$

该映射将隐空间中的点 $\mathbf{z}$ 先解码再编码，形成一个自反馈回路。论文的核心洞察是：**反复迭代应用 $f$ 会在隐空间中定义一个向量场**，其动力学行为揭示了网络权重中存储的信息。

### 关键公式：离散与连续动力学

迭代过程 $f(\cdots f(f(\mathbf{z})))$ 定义了一个离散常微分方程（ODE）：

$$\begin{cases}
\mathbf{z}_{t+1} = f(\mathbf{z}_t) \\
\mathbf{z}_0 = \mathbf{z}
\end{cases}$$

该离散 ODE 是以下连续微分方程的离散化：

$$\frac{\partial \mathbf{z}}{\partial t} = f(\mathbf{z}) - \mathbf{z}$$

其中 $f(\mathbf{z}) - \mathbf{z}$ 即为隐向量场的残差方向，决定了轨迹在隐空间中的演化方向。

### 吸引子：不动点作为信息字典

隐向量场的**吸引子**（attractors）定义为 $f$ 的不动点：

$$f(\mathbf{Z}^*) = \mathbf{Z}^*$$

这些吸引子被视为网络权重中存储信息的“字典原子”。论文据此定义了**记忆系数**（memorization coefficient），衡量吸引子解码后与训练样本的相似度：

$$\operatorname{mem}(\mathbf{z}^*) = \min_{\mathbf{x} \in \mathcal{X}_{\text{train}}} \cos(D(\mathbf{z}^*), \mathbf{x})$$

以及**轨迹分数**（trajectory score），用于区分分布内与分布外样本：

$$\operatorname{score}(\mathbf{z}) = \frac{1}{N} \sum_{\mathbf{z}_i \in \pi(\mathbf{z})} d(\bar{\mathbf{z}}_i, \bar{\mathbf{Z}}_{\text{train}}^*)$$

其中 $\pi(\mathbf{z})$ 是从 $\mathbf{z}$ 出发的轨迹，$d(\cdot, \cdot)$ 为欧氏距离，$\bar{\mathbf{Z}}_{\text{train}}^*$ 为训练数据吸引子集合。

### 收缩性与训练目标的关联

论文论证了自编码器的训练目标会**隐式促进映射 $f$ 的局部收缩性**。标准 MSE 重建损失：

$$\mathcal{L}_{\text{MSE}}(\mathbf{x}) = \sum_{\mathbf{x} \in X} \| \mathbf{x} - F_{\Theta}(\mathbf{x}) \|_2^2 + \lambda \mathcal{R}(\Theta)$$

加上数据增强后，损失函数进一步约束扰动输入的映射行为：

$$\mathcal{L}_{\text{MSE}}(\mathbf{x}) = \sum_{\mathbf{x} \in \mathcal{X}} \| \mathbf{x} - F(\mathbf{x}) \|_2^2 + \sum_{T \in p(T)} \| \mathbf{x} - F(T\mathbf{x}) \|_2^2$$

这些目标倾向于降低 Jacobian 矩阵的谱范数 $\|J_F(\mathbf{x})\|_\sigma$，使得 $f$ 满足 Lipschitz 连续性条件：

$$d(f(\mathbf{z}_1), f(\mathbf{z}_2))_{\mathcal{Z}} \leq C \, d(\mathbf{z}_1, \mathbf{z}_2)_{\mathcal{Z}}$$

其中 $C < 1$ 时映射为严格收缩，保证迭代收敛到吸引子。

### 重建误差的吸引子分解

论文将重建误差分解为两项，从吸引子视角解释泛化能力：

$$\| \mathbf{x} - F(\mathbf{x}) \|_2^2 \leq \underbrace{\| \mathbf{x} - D(\Pi(E(\mathbf{x}))) \|_2^2}_{\text{error to prototype}} + \underbrace{L_D^2 \cdot \|E(\mathbf{x}) - \Pi(E(\mathbf{x}))\|_2^2}_{\text{coverage error}}$$

其中 $\Pi$ 是将编码投影到最近吸引子的映射，$L_D$ 为解码器的 Lipschitz 常数。第一项为原型误差（吸引子能否表示输入），第二项为覆盖误差（隐编码能否被吸引子覆盖）。这一分解定量解释了瓶颈维度 $k$ 如何通过控制吸引子数量来调节记忆与泛化的权衡。

## 实验与关键发现

### 核心发现：吸引子字典的无数据权重信息探测

论文在视觉基础模型上验证了吸引子的表征能力。核心实验设计如下：从高斯噪声 $\mathbf{Z}_n \sim \mathcal{N}(\mathbf{0}, I)$ 出发，求解不动点方程 $f(\mathbf{Z}_n^*) = \mathbf{Z}_n^*$ 得到噪声吸引子，将其作为一组隐空间基向量。随后，使用正交匹配追踪（OMP, Mallat and Zhang 1993）以不同的稀疏度水平重构测试样本的隐编码，并与随机正交基进行对比。

**Figure 4** 展示了在 Stable Diffusion 的 AutoencoderKL 上的重构误差曲线。噪声吸引子字典在所有测试数据集上均以更低的 MSE 重构测试样本，且所需原子数更少。这一结果表明，**仅从权重中提取的吸引子，无需访问任何训练数据，即可恢复出与训练分布高度一致的信息**。Figure 7 提供了 Laion2B 上的可视化佐证：吸引子重构的图像在语义结构上明显优于正交基重构，后者仅呈现噪声模式。

**因果机制解读**：该实验证明了 §3.2 提出的理论——吸引子是网络权重中存储训练数据信息的压缩表示。噪声吸引子之所以有效，是因为训练后的自编码映射在隐空间形成了指向数据流形的向量场，随机噪声沿该场演化后自然收敛到数据分布的支撑集附近。

### OOD 检测：隐轨迹对分布偏移的表征

论文进一步利用隐向量场的轨迹特性进行分布外（OOD）检测。对于每个输入样本 $\mathbf{z}$，计算其沿向量场演化轨迹 $\pi(\mathbf{z})$ 上各点到训练吸引子集合 $\bar{\mathbf{Z}}_{train}^*$ 的平均距离作为异常分数：

$$\mathrm{score}(\mathbf{z}) = \frac{1}{N} \sum_{\mathbf{z}_i \in \pi(\mathbf{z})} d(\bar{\mathbf{z}}_i, \bar{\mathbf{Z}}_{train}^*)$$

**Figure 5 及 Table 1** 报告了 ViT-MAE 上的 OOD 检测结果。主要结论：

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Zunww3FHPU/figures/005_Figure_5.jpg]]
*Figure 5: Trajectories in the latent vector field characterize distribution shifts We measure out-ofdistribution detection performance on ViTMAE: On the left we report scores for 4 different datasets, highly outperforming the KNN baseline. On the right, histograms of scores on the INaturalist dataset, demonstrating much better separability between in-distribution and out-of-distribution when probing latent trajectories distances to in-distribution attractors (c), as opposed to measure distances to in-distribution features (b)*

- **轨迹距离方法显著优于 KNN 基线**：在多个 OOD 数据集上，FPR95 从 KNN 的 34.50–100.00 降至 29.60–29.95，AUROC 从 32.36–89.41 提升至 90.99–92.63。
- **轨迹距离也优于重构误差和特征空间的马氏距离**（Table 1 扩展结果），表明向量场动力学比静态表征包含更丰富的分布信息。
- Figure 5 右侧的分数直方图显示：分布内样本的轨迹距离集中在低值区，OOD 样本则明显右移，分离度良好。

**瓶颈分析**：该方法的有效性依赖于训练吸引子对分布内数据流形的充分覆盖。若训练吸引子数量不足或未能收敛到稳定不动点，轨迹距离的判别力会下降。Figure 3c 显示，噪声吸引子的收敛速度慢于训练吸引子，这在实际部署中可能引入计算开销。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Zunww3FHPU/figures/003_Figure_3.jpg]]
*Figure 3: (d) Similarity $\mathbf { Z } _ { n o i s e } ^ { * }$ and $\mathbf { Z } _ { t r a i n } ^ { * }$ Figure 3: Latent vector field dynamics. (a) The 2D vector field (k = 2) expands from a single attractor, eventually stabilizing and over-fitting because of capacity limits. Bottom: Evolution of larger capacity $\mathrm { A E s } \left$( k = 1 2 8 $\right$) across training. (b) Throughout training, the network first memorizes the data with a high memorization coefficient (in blue) and then generalizes, achieving a low test error (red). (c): Evolution of attractor count for training (blue), test (red), and noise (yellow) samples; (d) Attractors computed from training and from gaussian noise converge dur...

### 记忆与泛化的动力学分析

论文通过控制瓶颈维度 $k$ 系统研究了正则化强度对记忆-泛化权衡的影响（Figure 2）：

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Zunww3FHPU/figures/002_Figure_2.jpg]]
*Figure 2: Memorization vs Generalization. Attractors memorize the training data as a function of the rank of $J _ { f } ( \mathbf { z }$ ) by adjusting the bottleneck dimension k (left) which is inversely proportional to the amount of generalization attained by the model (center); On the right we show example of decoded attractors transitioning from a strong memorization model (first row) to good generalization (last row)*

- **低正则化（$k$ 较大）**：网络倾向于记忆训练样本，吸引子解码结果与训练数据高度相似，记忆系数 $\mathrm{mem}(\mathbf{z}^*)$ 接近 1，但测试误差较高。
- **高正则化（$k$ 较小）**：吸引子数量减少，单个吸引子覆盖更广的数据区域，测试误差下降，模型从记忆过渡到泛化。

Figure 3 从训练动态角度补充了这一图景：
- **(a)** 2D 隐向量场从初始化的单一全局吸引子逐步扩展，形成与数据分布对齐的多吸引子结构。
- **(b)** 记忆系数与测试误差呈现清晰的权衡曲线：早期 epoch 记忆占主导，后期泛化能力提升。
- **(c)** 吸引子数量随训练稳定增长，且训练和测试数据的吸引子数量趋于一致，表明模型学习到的是数据流形的结构而非个体样本。

### 实验局限与待验证点

1. **计算开销**：噪声吸引子的求解需要迭代至不动点，对于高维隐空间（如 Stable Diffusion 的 AutoencoderKL）计算成本较高。论文未给出具体的收敛迭代次数统计。
2. **OOD 检测的泛化性**：实验仅在 ViT-MAE 上验证，未涉及其他架构（如 CNN-based AE、VQ-VAE）。Table 3 统一了多种 AE 变体的形式化，但未实验验证不同正则化机制下吸引子质量的差异。
3. **吸引子收敛的理论保证**：论文假设了局部收缩性，但未提供 Jacobian 谱范数的实证测量来量化不同模型和训练阶段的收缩程度。这导致“何时吸引子可靠”缺乏可操作的判据。
4. **Figure 7 为样本级展示**：Laion2B 重构可视化仅展示 5 个随机样本，定量统计（如 FID、LPIPS）缺失，需手动补充验证。

*Figure 1: Latent dynamics of AEs. Latent vector fields induced by autoencoders with bottleneck k = 2, trained on MNIST, with $\mathbf { z } _ { 0 } \sim \mathcal { U }$ [ - 8 , 8 ] . Models with different initializations are shown. Colors (viridis colormap) represent vector norms ranging from violet (low) to yellow (high). The shape of the latent manifold identifies with the encoder’s support. White regions indicate where the vector field vanishes, revealing attractors aligned with high-density areas of the data distribution

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Zunww3FHPU/figures/009_Figure.jpg]]
*Figure: (b) 1024 atoms (c) 2048 atoms*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Zunww3FHPU/figures/012_Figure.jpg]]
*Figure: (a) 256 atoms (b) 1024 atoms (c) 2048 atoms*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Zunww3FHPU/figures/006_Table.jpg]]
*Table: (a) FPR and AUROC scores*

## 定位与知识库关联

### 与基线方法的关系

本文提出将自编码器（AE）隐式地表征为潜在向量场，通过迭代编码器-解码器映射 $f(\mathbf{z}) = E \circ D(\mathbf{z})$ 来定义离散 ODE 及其对应的连续微分方程 $\frac{\partial \mathbf{z}}{\partial t} = f(\mathbf{z}) - \mathbf{z}$。该方法的核心前提——AE 的局部收缩性——建立在三个来源的归纳偏置之上：初始化偏置、显式正则化（如权重衰减）和隐式正则化（如数据增强）。这一框架将 AE 的动力学与**得分函数**建立了理论联系：在局部收缩条件下，潜在动力学 $f(\mathbf{z}) - \mathbf{z}$ 局部正比于潜在先验的得分函数 $\nabla_{\mathbf{z}} \log q(\mathbf{z})$。这一结果的理论基础可追溯至**Miyasawa et al.（1961）**、**Robbins（1992）**以及**Alain and Bengio（2014）**关于去噪自编码器残差逼近得分函数的经典工作。

在 OOD 检测实验中，本文以 KNN 基线、重构误差基线和特征空间马氏距离作为对比方法，在 ViT-MAE 上验证了基于潜在轨迹距离的检测方法在 FPR95 和 AUROC 上的显著优势。然而，论文未与更先进的 OOD 检测方法（如基于能量模型、梯度范数或特征空间密度估计的方法）进行系统比较，因此该方法在 OOD 检测领域的相对竞争力需要进一步验证。

### 适用边界

本方法的适用性建立在以下前提之上：
1. **模型需为自编码器或其变体**：框架依赖编码器-解码器结构的可迭代性。论文在卷积 AE、ViT-MAE 和 Stable Diffusion 的 VAE 编码器-解码器对上验证了有效性，但明确指出对非可逆模型（如分类器）的推广需要将向量场定义在输出空间，即研究残差 $F(\mathbf{x}) - y$。
2. **局部收缩性是必要条件**：理论分析依赖映射 $f$ 的局部收缩性。论文在附录中验证了多个 torchvision 模型在初始化时方差保持比小于 1（Figure 6），表明收缩性在初始化时普遍存在。但对于训练后的模型，收缩性可能随容量和正则化强度变化——高容量低正则化模型可能过拟合为记忆模式，此时吸引子数量激增，收缩性减弱。
3. **吸引子计算依赖固定点求解**：吸引子 $\mathbf{Z}^*$ 需满足 $f(\mathbf{Z}^*) = \mathbf{Z}^*$，通过迭代求解获得。收敛速度与初始点到吸引子的距离相关（Figure 11），Pearson 相关系数约为 0.99，表明线性收敛特性。但对于高维潜在空间（如 Stable Diffusion 的潜在空间），吸引子求解的计算成本可能较高。

### 局限与开放问题

**已明确的局限：**
- 本文框架目前仅适用于自编码器类模型，对任意神经网络（如纯分类器、自监督模型）的推广尚未实现。
- 吸引子在训练过程中的形成机制尚未被严格刻画：论文观察到噪声吸引子随训练收敛至训练吸引子，但这一过程的动力学和收敛速度缺乏理论分析。
- 实验验证集中于图像领域（MNIST、CIFAR、ImageNet、Laion2B），在其他模态（文本、音频、图数据）上的适用性未知。

**开放问题：**
1. **跨模型潜在向量场对齐**：不同神经网络模型的潜在向量场之间是否存在结构对应关系？这一问题对模型融合和知识迁移具有潜在意义。
2. **吸引子形成动力学**：训练过程中吸引子如何从初始的单一原点吸引子（Figure 3a）分裂并稳定为多个吸引子？噪声吸引子收敛至训练吸引子的速率与哪些因素相关？
3. **向非自编码器模型的推广**：如何将潜在向量场框架推广至深度分类器或自监督模型？论文建议在输出空间研究残差 $F(\mathbf{x}) - y$，但这一方向尚未被实验验证。
4. **吸引子作为字典的稀疏编码能力**：论文展示了吸引子作为字典在无数据样本恢复中的有效性（Figure 4），但吸引子字典的理论完备性（如等距约束、相干性）及其与学习理论中泛化界的关联尚未被探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/Navigating_the_Latent_Space_Dynamics_of_Neural_Models.pdf]]
