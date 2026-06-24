---
title: "Overlap-guided gaussian mixture models for point cloud registration"
type: paper
paper_level: A
venue: WACV
year: 2023
pdf_ref: paperPDFs/WACV_2023/Overlap_guided_gaussian_mixture_models_for_point_cloud_registration.pdf
aliases:
- OGGMMPCR
tags:
- WACV_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入Transformer检测的重叠分数（overlap score）作为GMM建模的软注意力，使配准只关注重叠区域而忽略非重叠离群点，从而将部分到部分配准转化为重叠区域的对齐问题。"
primary_logic: "利用聚类注意力（clustered attention）Transformer检测重叠区域，在重叠分数的指导下为源和目标点云分别构建高斯混合模型，并通过最小化两个GMM之间的统计差异（最优传输+加权SVD）恢复刚体变换，解决了部分重叠场景下的配准难题。"
claims:
- "将点云配准重新定义为对齐两个高斯混合，并最小化二者之间的统计差异。"
- "重叠分数直接用于加权GMM参数估计，使配准聚焦于重叠区域，大幅降低非重叠点的干扰。"
- "聚类自注意力将Transformer的复杂度从 O(N²) 降为 O(N·J)，同时保持了匹配精度。"
- "利用聚类注意力（clustered attention）Transformer检测重叠区域，在重叠分数的指导下为源和目标点云分别构建高斯混合模型，并通过最小化两个GMM之间的统计差异（最优传输+加权SVD）恢复刚体变换，解决了部分重叠场景下的配准难题。"
---

# Overlap-guided gaussian mixture models for point cloud registration

> [!tip] 核心洞察
> 利用聚类注意力（clustered attention）Transformer检测重叠区域，在重叠分数的指导下为源和目标点云分别构建高斯混合模型，并通过最小化两个GMM之间的统计差异（最优传输+加权SVD）恢复刚体变换，解决了部分重叠场景下的配准难题。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 重叠引导的高斯混合模型点云配准 |
| 英文题名 | Overlap-guided gaussian mixture models for point cloud registration |
| 会议/期刊 | WACV 2023 |
| Links | [paper](https://arxiv.org/abs/2210.09836); [GitHub](https://github.com/gfmei/ogmm) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | OGMM |
| Dataset | ModelNet40, 7Scenes, ICL-NUIM |

> [!tip] 效果简介
> - 重叠分数直接用于加权GMM参数估计，使配准聚焦于重叠区域，大幅降低非重叠点的干扰。

## 概述

点云配准的核心挑战在于处理**部分重叠**（partial-to-partial）场景：源点云与目标点云仅共享部分区域，非重叠部分会严重干扰配准估计。现有基于高斯混合模型（GMM）的概率配准方法（如 **DeepGMR**，Yuan et al., ECCV 2020）假设两个点云共享相同的GMM参数，难以应对部分重叠问题，导致在真实部分视角点云上性能显著下降。

本文提出 **OGMM**（Overlap-guided Gaussian Mixture Models），将部分重叠下的点云配准重新定义为：**在重叠分数的引导下，对齐两个高斯混合模型，并最小化二者之间的统计差异**。核心思路是引入一个基于Transformer的重叠检测模块，预测每个点位于重叠区域的概率（重叠分数），然后用这些分数加权GMM的参数估计（权重、均值、协方差），使配准过程自动聚焦于重叠区域而忽略非重叠离群点。这本质上将部分到部分配准转化为重叠区域内的高斯混合对齐问题。

**方法定位**：OGMM属于概率配准范式，但与DeepGMR等假设共享GMM的方法不同，它通过重叠分数为源点云和目标点云分别构建独立的GMM，再通过最优传输匹配簇中心、加权SVD求解刚体变换。为降低Transformer的 $O(N^2)$ 复杂度，OGMM采用**聚类注意力**（clustered attention）机制，先用Wasserstein K-Means将点云聚类为 $J$ 个簇，仅在簇中心上计算注意力，将复杂度降至 $O(N \cdot J)$（$J \ll N$）。同时，**球面位置编码**（Spherical Positional Encoding）利用点到质心的距离和k近邻角度，为网络注入刚体变换不变的结构信息。

**主要结果**：OGMM在ModelNet40的部分到部分配准上显著优于DeepGMR、RPMNet、DCP等先前方法，且在加噪和密度变化条件下表现出较强的鲁棒性。消融实验表明，移除重叠分数预测模块后，旋转误差MAE(R)从0.5892急剧升至6.7087，验证了重叠引导是方法的核心驱动力。聚类注意力使推理时间从约0.047秒降至0.006秒，加速约8倍。在7Scenes和ICL-NUIM真实场景数据集上，OGMM同样展现出有竞争力的配准精度。

**局限性**：重叠区域检测依赖标注数据进行监督训练，难以直接应用于无标注的真实场景；在对称或重复几何结构场景中，聚类注意力可能提取歧义特征导致配准失败；重叠分数预测的距离阈值 $\eta$ 需要针对不同数据集手动调整。

## 背景与动机

点云配准（point cloud registration）是计算机视觉与机器人领域的基础任务，其目标是估计一个刚体变换 $T \in SE(3)$，使源点云与目标点云在空间上对齐。该任务在三维重建、自动驾驶、机器人导航等应用中扮演着关键角色。然而，真实场景中获取的点云往往是部分重叠的（partial-to-partial），即两个点云仅共享一部分可见区域，这为精确配准带来了根本性挑战。

现有方法大致可分为三类：基于对应关系的方法（如 **DCP**（Wang & Solomon, ICCV 2019）、**RPMNet**（Yew & Lee, CVPR 2020））、基于全局特征对齐的方法（如 **PointNetLK**（Aoki et al., CVPR 2019））以及基于概率模型的方法。其中，概率配准方法将点云建模为概率分布，通过最小化分布间的统计差异来求解变换，具有无需显式对应关系、对噪声鲁棒等优点。**DeepGMR**（Yuan et al., ECCV 2020）是这一方向的代表性工作，它利用神经网络提取特征并构建高斯混合模型（Gaussian Mixture Model, GMM），在完全重叠场景下取得了优异性能。

然而，DeepGMR 存在一个关键瓶颈：**它假设源点云与目标点云共享相同的 GMM 参数**，即要求两个点云覆盖相同的几何区域。在部分重叠场景下，非重叠区域的点会严重污染 GMM 的估计，使配准过程被离群点主导，导致性能急剧下降。这一假设从根本上限制了概率配准方法在真实部分视角点云上的适用性。

针对上述问题，OGMM 提出了一个核心洞见：**如果能够事先识别出点云间的重叠区域，就可以将部分到部分配准转化为重叠区域的对齐问题**。具体而言，OGMM 引入一个基于 Transformer 的重叠检测模块，为每个点预测一个重叠分数（overlap score），指示该点位于重叠区域的概率。这些重叠分数随后被用作软注意力，直接加权到 GMM 参数（权重 $\pi_j$、均值 $\mu_j$、协方差 $\Sigma_j$）的估计中，使 GMM 仅由重叠区域的点驱动，从而从根本上消除非重叠离群点的干扰。

此外，标准 Transformer 的自注意力机制复杂度为 $O(N^2)$，难以处理大规模点云。OGMM 采用**聚类注意力（clustered attention）**策略：先用 Wasserstein K-Means 将点云聚类为 $J$ 个簇（$J \ll N$），再在簇中心上计算注意力，将复杂度降至 $O(N \cdot J)$，在保持匹配精度的同时实现了约 8 倍的推理加速。

综上，OGMM 的动机源于一个明确的因果链条：**非重叠区域的干扰是部分配准失败的根本原因 → 通过重叠检测将配准聚焦于重叠区域 → 用重叠分数引导 GMM 建模 → 实现鲁棒的部分到部分配准**。这一设计使得 OGMM 在 ModelNet40、7Scenes 和 ICL-NUIM 等多个基准上均取得了领先的配准精度。

## 核心创新

OGMM 的核心创新在于将**部分到部分点云配准**重新定义为**两个高斯混合模型（GMM）的对齐问题**，并通过**重叠分数引导**使配准过程自动聚焦于重叠区域，从而系统性地解决了现有概率配准方法在部分重叠场景下的性能瓶颈。

### 1. 从全局GMM到重叠引导GMM的范式转变

现有基于GMM的配准方法（如 **DeepGMR**，Yuan et al., ECCV 2020）假设源点云与目标点云共享相同的GMM参数，在整片点云上进行建模。当点云仅部分重叠时，非重叠区域的点会严重污染GMM的参数估计，引入系统性偏置，导致变换估计精度急剧下降。

OGMM 的**核心因果机制**在于引入了一个**重叠分数预测模块**（Overlap Score Prediction, OSP），为源点云和目标点云的每个点预测一个 $[0,1]$ 范围内的重叠分数 $o_{p_i}$ 和 $o_{q_i}$。这些分数随后直接用于GMM参数（权重 $\pi_j^p$、均值 $\mu_j^p$、协方差 $\Sigma_j^p$）的加权计算中：

$$\pi_j^p = \sum_{i=1}^N \frac{o_{p_i} s_{ij}^p}{\epsilon + n_p},\quad \mu_j^p = \sum_{i=1}^N \frac{o_{p_i} s_{ij}^p p_i}{\epsilon + n_p \pi_j^p},\quad \Sigma_j^p = \frac{1}{\epsilon + n_p \pi_j^p} \sum_{i=1}^N o_{p_i} s_{ij}^p (p_i - \mu_j^p)(p_i - \mu_j^p)^\top$$

这一设计使得GMM的构建**仅由重叠区域的点驱动**，非重叠离群点被自动忽略，从而将部分到部分配准转化为重叠区域的对齐问题。消融实验提供了决定性证据：**移除OSP后，旋转误差 MAE(R) 从 0.5892 飙升至 6.7087**（Table 4），性能退化超过一个数量级，充分验证了重叠引导机制的核心地位。

### 2. 聚类注意力：将Transformer复杂度从 $O(N^2)$ 降至 $O(N \cdot J)$

为高效检测重叠区域，OGMM 需要交换源点云与目标点云之间的特征信息。标准Transformer的交叉注意力复杂度为 $O(N^2)$，在大规模点云上计算代价高昂。OGMM 提出**聚类自注意力**（Clustered Self-Attention）和**聚类交叉注意力**（Clustered Cross-Attention）机制：

- 先用 **Wasserstein K-Means** 将点云聚类为 $J$ 个簇（$J \ll N$）
- 仅在 $J$ 个簇中心上计算注意力，复杂度降至 $O(N \cdot J)$

这一设计在保持匹配精度的同时实现了显著加速：推理时间从约 **0.047 s 降至 0.006 s**，加速约 **8 倍**（Table 6）。消融实验进一步表明，移除聚类自注意力（CSA）会导致性能下降（Table 4），但其影响程度远小于OSP，说明聚类注意力是效率提升的关键杠杆，而重叠分数才是精度保障的核心。

### 3. 球面位置编码：注入刚性变换不变的结构信息

传统位置编码（如绝对坐标或正弦编码）对刚性变换敏感，不利于配准任务。OGMM 设计了**球面位置编码**（Spherical Positional Encoding, SPE）：

$$f_{p_i}^{pos} = \varphi\left( \| \pmb{p_i} - \pmb{p_c} \|_2 \right) + \max_{x \in \mathcal{K}_i} \{ \phi\left( \alpha_{ix} \right) \}$$

该编码利用点到质心的欧氏距离和 $k$ 近邻中的最大角度，天然具有刚性变换不变性。消融实验显示，移除SPE后配准精度下降（Table 4），验证了其对特征表达质量的贡献。

### 4. 创新点之间的协同关系

上述三个创新点并非孤立存在，而是形成了层次化的协同机制：
- **SPE** 提供变换不变的几何特征基础
- **聚类注意力** 在保持效率的前提下实现点云间特征交换，为重叠检测提供上下文
- **重叠分数** 作为核心控制信号，将GMM建模的焦点精确锁定在重叠区域

三者共同实现了“检测重叠→聚焦重叠→对齐重叠”的完整因果链路，使得OGMM在ModelNet40部分到部分配准任务上取得了最低的旋转误差（MAE(R)=0.5892）和平移误差（MAE(t)=0.0079）（Table 1），显著优于DeepGMR、RPMNet、DCP等基线方法。

> **注意**：由于论文解析限制，Table 1中所有对比方法的完整量化数值未能提取，上述OGMM自身数值来自已验证的消融实验（Table 4 Full model行），与其他方法的相对优势需结合原论文Table 1手动验证。

## 整体框架

OGMM将部分到部分的点云配准重新定义为**对齐两个高斯混合模型（GMM）**，并通过最小化二者之间的统计差异来恢复刚体变换 $T \in SE(3)$。整个框架由三个核心模块串联构成：**特征提取**、**重叠区域检测**和**重叠引导的GMM配准**，其信息流如Figure 1所示。

### 输入与输出

给定一对部分重叠的点云——源点云 $\mathcal{P} = \{\mathbf{p}_i \in \mathbb{R}^3\}_{i=1}^{N}$ 和目标点云 $\mathcal{Q} = \{\mathbf{q}_i \in \mathbb{R}^3\}_{i=1}^{M}$，OGMM输出一个刚体变换 $T = \{R \in SO(3), \mathbf{t} \in \mathbb{R}^3\}$，使得变换后的源点云与目标点云在重叠区域内精确对齐。

### 模块1：特征提取

共享权重的DGCNN编码器首先从 $\mathcal{P}$ 和 $\mathcal{Q}$ 中分别提取逐点特征 $\mathcal{F}_p$ 和 $\mathcal{F}_q$。这些初始特征随后被注入**球面位置编码**（Spherical Positional Encoding），利用点到质心的欧氏距离和k近邻中的最大角度编码刚性变换不变的结构信息。接着，**聚类自注意力**模块将点云通过Wasserstein K-Means聚类为 $J$ 个簇（$J \ll N$），仅在簇中心上计算注意力，将复杂度从 $O(N^2)$ 降至 $O(N \cdot J)$，同时保持全局上下文建模能力。更新后的逐点特征作为后续重叠检测的输入。

### 模块2：重叠区域检测

该模块通过**聚类交叉注意力**实现源点云与目标点云之间的特征交换：源点云的点特征聚合目标点云簇质心的信息，反之亦然。交换后的条件特征 $\mathcal{F}_p^t$ 和 $\mathcal{F}_q^t$ 被送入一个小型预测网络，输出每个点的**重叠分数** $o_{p_i}, o_{q_j} \in [0, 1]$，指示该点位于重叠区域的概率。Figure 2展示了从输入部分点云到重叠区域提取的可视化过程——非重叠区域以灰色显示，后续配准仅聚焦于检测到的重叠几何信息。

### 模块3：重叠引导的GMM配准

这是OGMM的核心创新所在。利用重叠分数 $o_p, o_q$ 和分类头输出的软分配概率，分别为源点云和目标点云构建 $L$ 个分量的高斯混合模型 $\mathbf{G}_{\mathcal{P}}(\mathbf{x})$ 和 $\mathbf{G}_{\mathcal{Q}}(\mathbf{x})$。关键在于，GMM的权重 $\pi_j$、均值 $\mu_j$ 和协方差 $\Sigma_j$ 均由重叠分数加权计算，使得非重叠区域的点对GMM参数的贡献被自动抑制，从而将部分到部分配准转化为**仅重叠区域的对齐问题**。

随后，通过求解最优传输问题得到簇级别的匹配矩阵 $\Gamma$，再以 $\Gamma$ 为权重执行加权SVD，一步估计出刚体变换 $T$。整个pipeline端到端可微，三个模块协同工作：特征提取提供判别性表示，重叠检测提供软注意力掩膜，GMM配准则在统计差异最小化的框架下完成鲁棒对齐。

## 核心模块与公式推导

OGMM 的完整流水线由三个核心模块串联构成：**特征提取**、**重叠区域检测**和**重叠引导的 GMM 配准**（Figure 1）。前两个模块负责为每个点生成刚性变换不变的特征以及逐点的重叠分数；第三个模块则在重叠分数的软引导下，将源点云与目标点云分别建模为高斯混合模型，并通过最小化两个 GMM 之间的统计差异恢复刚体变换 $T \in SE(3)$。

### 特征提取：聚类自注意力与球面位置编码

特征提取模块由 DGCNN、球面位置编码（Spherical Positional Encoding, SPE）和聚类自注意力（Clustered Self-Attention, CSA）组成。DGCNN 首先提取逐点局部几何特征，随后注入 SPE 以提供刚性变换不变的全局位置信息。

**球面位置编码**的计算方式为：

$$f_{p_i}^{pos} = \varphi\left( \| \pmb{p_i} - \pmb{p_c} \|_2 \right) + \max_{x \in \mathcal{K}_i} \{ \phi\left( \alpha_{ix} \right) \}$$

其中 $\pmb{p_c}$ 为点云质心，$\mathcal{K}_i$ 为点 $p_i$ 的 $k$ 近邻集合，$\alpha_{ix}$ 为近邻点 $x$ 相对于质心的角度，$\varphi$ 和 $\phi$ 为可学习的非线性映射。由于欧氏距离和角度在刚体变换下保持不变，该编码天然具备变换不变性。

为了在保持全局感受野的同时降低 Transformer 的二次复杂度，OGMM 采用**聚类自注意力**。首先用 Wasserstein K-Means 将点云聚类为 $J$ 个簇（$J \ll N$），每个簇的特征质心定义为：

$$\pmb{f}_{\bar{p}_j} = \sum_{i=1}^{N} \frac{\gamma_{ij}^p \pmb{f}_{p_i}}{\sum_k^N \gamma_{kj}^p}$$

其中 $\gamma_{ij}^p$ 为软聚类分配权重。随后，每个点的特征通过其与所有簇质心的注意力权重进行更新，而非逐点计算注意力：

$$\pmb{f_{p_i}} \gets \pmb{f_{p_i}} + \mathrm{MLP}\left( \sum_{j=1}^{J} \alpha_{ij}^p W_V^s \pmb{f_{\bar{p}_j}} \right)$$

这一设计将自注意力的复杂度从 $O(N^2)$ 降至 $O(N \cdot J)$，在保持匹配精度的同时实现了约 8 倍的推理加速（Table 6：OGMM (c) 约 0.006 s vs. OGMM (f) 约 0.047 s）。

### 重叠区域检测：聚类交叉注意力与重叠分数

在获得源点云 $\mathcal{P}$ 和目标点云 $\mathcal{Q}$ 的更新特征后，OGMM 通过**聚类交叉注意力**（Clustered Cross-Attention）实现两点云之间的信息交换：

$$f_{p_i}^t \gets f_{p_i} + \mathrm{MLP}\left( \sum \beta_{ij}^p W_V^c f_{\bar{q}_j} \right)$$

即源点云的点特征通过注意力权重 $\beta_{ij}^p$ 聚合目标点云聚类质心 $f_{\bar{q}_j}$ 的信息，得到条件化特征 $\mathcal{F}_p^t$ 和 $\mathcal{F}_q^t$。

基于条件化特征，重叠分数预测模块计算逐点重叠分数 $o_{p_i} \in [0,1]$：

$$w_{ij} = \sigma\left( {f_{p_i}^t}^\top f_{q_j}^t / \tau \right), \quad o_{p_i} = g_\beta\left( \mathrm{cat}\left[ f_{q_i}^t, w_i^\top g_\alpha\left( \mathcal{F}_q^t \right) \right] \right)$$

其中 $\sigma$ 为 softmax 函数，$\tau$ 为温度参数，$w_{ij}$ 为点对之间的软匹配相似度，$g_\alpha$ 和 $g_\beta$ 为小型可学习网络。该模块输出的重叠分数直接指示各点位于重叠区域的概率，是后续 GMM 建模的关键引导信号。

### 重叠引导的 GMM 配准：参数估计、最优传输与加权 SVD

OGMM 将点云配准重新定义为对齐两个高斯混合模型。以源点云 $\mathcal{P}$ 为例，其 GMM 参数（权重 $\pi_j^p$、均值 $\mu_j^p$、协方差 $\Sigma_j^p$）均以重叠分数加权计算：

$$\pi_j^p = \sum_{i=1}^N \frac{o_{p_i} s_{ij}^p}{\epsilon + n_p},\quad \mu_j^p = \sum_{i=1}^N \frac{o_{p_i} s_{ij}^p p_i}{\epsilon + n_p \pi_j^p},\quad \Sigma_j^p = \frac{1}{\epsilon + n_p \pi_j^p} \sum_{i=1}^N o_{p_i} s_{ij}^p (p_i - \mu_j^p)(p_i - \mu_j^p)^\top$$

其中 $s_{ij}^p$ 为分类头输出的软分配概率，$n_p = \sum_i o_{p_i}$ 为有效重叠点数，$\epsilon$ 为数值稳定项。目标点云 $\mathcal{Q}$ 的 GMM 参数以相同方式计算。这一设计的核心效果是：**非重叠区域的点因重叠分数趋近于零，对 GMM 参数的贡献被自动抑制**，使得配准过程仅聚焦于重叠区域的几何信息。

在获得两个 GMM 后，OGMM 通过求解簇级别的**最优传输问题**建立簇-簇匹配：

$$\min_{\Gamma} \sum_{i=1}^{L} \sum_{j=1}^{L} \Gamma_{ij} \| \nu_i^p - \nu_j^q \|_2^2,\quad \text{s.t. } \Gamma \mathbf{1}_M = \pi^p, \Gamma^\top \mathbf{1}_N = \pi^q$$

其中 $\nu_i^p$ 和 $\nu_j^q$ 分别为源和目标 GMM 各分量的特征质心，$\pi^p$ 和 $\pi^q$ 为分量权重向量。求解得到的匹配矩阵 $\Gamma$ 随后用于**加权 SVD**，估计最终的刚体变换 $T$。

消融实验（Table 4）提供了该模块设计的有力证据：移除重叠分数预测（Without OSP）后，旋转误差 MAE(R) 从 0.5892 急剧上升至 6.7087，平移误差 MAE(t) 从 0.0079 升至 0.0729，验证了重叠分数在 GMM 建模中的决定性作用。

## 实验与分析

### 主实验结果

OGMM 在 ModelNet40 的部分到部分配准任务上取得了最优性能。在同类别的设置下，OGMM 的旋转误差 MAE(R) 为 **0.5892**，平移误差 MAE(t) 为 **0.0079**，倒角距离 CCD 为 **0.0493**；在跨类别设置下，MAE(R) 为 **0.6309**，MAE(t) 为 **0.0080**，CCD 为 **0.0542**（Table 1）。与基于 GMM 的基线方法 **DeepGMR**（Yuan et al., ECCV 2020）相比，OGMM 在所有指标上均有显著提升。为公平对比，论文还将 DeepGMR 的编码器替换为 OGMM 的特征提取网络，改进后的 DeepGMR 性能仍不及 OGMM，表明重叠引导的 GMM 建模策略是性能提升的核心来源。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2210_09836/figures/003_Table_1.jpg]]
*Table 1: Partial-to-Partial Registration results on ModelNet40*

在加噪和密度变化的鲁棒性测试中（Table 2），OGMM 同样表现出较强的抗干扰能力。在真实场景数据集 7Scenes 和 ICL-NUIM 上（Table 3），OGMM 的配准精度优于 RPMNet、DCP、FGR 等主流方法，验证了该方法对真实传感器数据的泛化能力。但由于解析限制，Table 1 和 Table 3 中基线方法的详细量化数值未能完整提取，建议读者参阅原论文获取精确对比数据。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2210_09836/figures/004_Table_2.jpg]]
*Table 2: Registration results on ModelNet40 with jittering noise or density variation*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2210_09836/figures/006_Table_3.jpg]]
*Table 3: The registration results on 7Scenes and ICL-NUIM*

### 消融实验

消融实验系统性地验证了 OGMM 各模块的贡献（Table 4）。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2210_09836/figures/008_Table_4.jpg]]
*Table 4: Ablation study on ModelNet40*

**重叠分数预测（OSP）是关键组件。** 移除 OSP 后，模型退化为在整个点云上估计 GMM，非重叠区域的离群点严重污染了分布估计，导致 MAE(R) 从 0.5892 急剧上升至 6.7087，MAE(t) 从 0.0079 升至 0.0729，CCD 从 0.0493 升至 0.1155。这一结果直接证明了重叠引导机制在部分到部分配准中的决定性作用。

**球面位置编码（SPE）和聚类自注意力（CSA）也贡献了可观的性能增益。** 移除 SPE 后，模型失去了刚性变换不变的几何结构信息，MAE(R) 上升至 1.7621；移除 CSA 后，模型退化为标准自注意力，特征提取能力下降，MAE(R) 升至 1.0136。两者的影响程度小于 OSP，但仍是整体性能的重要组成部分。

**损失函数分析**（Table 5）表明，仅使用全局配准损失（GR）和重叠分数损失（OS）时，MAE(R) 为 0.7828；加入聚类一致性损失（CL）后，MAE(R) 进一步降至 0.5892。CL 损失通过强制同一簇的点在几何空间和特征空间中保持一致的分配，有效强化了特征空间与几何空间的对齐，从而提升了 GMM 参数估计的准确性。

### 效率分析

聚类注意力将 Transformer 的计算复杂度从 $O(N^2)$ 降至 $O(N \cdot J)$，其中 $J \ll N$。Table 6 显示，使用聚类自注意力和聚类交叉注意力的 OGMM (c) 单次推理时间约 **0.006 s**，而使用标准全注意力的 OGMM (f) 约需 0.047 s，加速约 **8 倍**。这一加速使得 OGMM 在保持高精度的同时具备了实际部署的可行性。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2210_09836/figures/007_Table_6.jpg]]
*Table 6: Comparisons of the average inference time*

### 重叠比例与聚类数量的敏感性

**重叠比例对配准精度影响显著**（Table 7）。当重叠比率从 70% 降至 30% 时，MAE(R) 由 0.9111 增至 5.6462，表明低重叠场景仍对 OGMM 构成挑战。这与重叠分数预测模块的性能边界有关：极低重叠下，Transformer 检测重叠区域的能力下降，导致 GMM 估计中有效信息不足。

**聚类数量 J 在 32 到 64 之间时性能稳定**（Table 8），MAE(R) 在 2.1000 到 2.1625 之间波动。当 J 过小时，聚类粒度过粗，损失了局部几何细节；当 J 过大时，聚类退化为近似逐点操作，丧失了注意力效率优势。论文默认使用 J=72，在实际应用中可根据点云规模和计算预算在此范围内调整。

### 失败模式与局限性

Figure 3 展示了 OGMM 在 ModelNet40 上的成功与失败案例。失败主要发生在以下两类场景：

1. **对称或重复几何结构**：对于具有旋转对称性的物体（如碗、圆桌），聚类注意力可能提取到歧义特征，导致多个几何上等效的配准方案使模型难以收敛到正确解。
2. **极低重叠率**：当源点云与目标点云的重叠区域过小（如 <30%），重叠分数预测模块难以可靠地区分重叠与非重叠点，GMM 估计的质量随之下降。

此外，OGMM 需要标注的重叠区域进行监督训练，限制了其在无标注真实场景中的直接应用。重叠分数预测中的距离阈值 $\eta$（默认 0.1）可能需要针对不同数据集手动调整，增加了跨域迁移的工程成本。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2210_09836/figures/009_Table_5.jpg]]
*Table 5: Loss function analysis on ModelNet40*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2210_09836/figures/010_Table_9.jpg]]
*Table 9: Registration results on ModelNet40*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2210_09836/figures/012_Table_7.jpg]]
*Table 7: The effects of the overlap ratio on ModelNet40*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2210_09836/figures/013_Table_8.jpg]]
*Table 8: The effects of the cluster numbers on ModelNet40 with 50% overlapping ratio and Gaussian noise*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2210_09836/figures/002_Figure_2.jpg]]
*Figure 2: Given (a) input partial point clouds, OGMM detects (b) the overlap regions that are then used for the estimation of (c) the transformation that aligns the two point clouds. The non-overlap regions in (b) are shown in grey. Our approach focuses on the geometric information in the overlap regions to perform the point cloud registration*

## 方法谱系与知识库定位

**概率配准的演进与OGMM的定位**

点云配准方法可粗略划分为基于对应关系的方法和无对应关系的方法。基于对应关系的方法（如ICP系列、**FGR** (Zhou et al., ECCV 2016)、**DCP** (Wang & Solomon, ICCV 2019)、**RPMNet** (Yew & Lee, CVPR 2020)）依赖于显式的点级或特征级匹配，当重叠率低或几何结构重复时，匹配质量急剧下降。无对应关系的方法试图绕过匹配步骤，例如**PointNetLK** (Aoki et al., CVPR 2019)将配准视为全局特征的对齐，**DeepGMR** (Yuan et al., ECCV 2020)将点云建模为高斯混合模型（GMM），通过最小化源与目标GMM之间的统计差异来求解刚体变换。DeepGMR的瓶颈在于其假设源点云与目标点云共享相同的GMM参数，这在部分重叠场景下会导致非重叠区域的点严重污染GMM估计，使配准性能显著退化。OGMM正是在这一瓶颈上做出了关键改进：引入重叠分数作为软注意力，使GMM的估计仅由重叠区域的点驱动，将部分到部分配准转化为重叠区域的对齐问题。

**与图匹配和Transformer配准方法的关系**

**RGM**和**RegTR**等基于图匹配或Transformer的方法通过端到端学习对应关系来实现配准，它们在特征交换和上下文聚合方面与OGMM的特征提取模块有相似之处。OGMM的聚类自注意力和聚类交叉注意力借鉴了Transformer的注意力机制，但通过Wasserstein K-Means将点云聚类为J个簇，将复杂度从$O(N^2)$降至$O(N \cdot J)$（其中$J \ll N$），在保持匹配精度的同时实现了约8倍的推理加速（Table 6：0.006 s vs 0.047 s）。与**OMNet**学习重叠掩膜的做法相比，OGMM的重叠分数直接嵌入GMM参数估计的加权过程中，而非仅作为掩膜过滤，这使得重叠信息与配准目标在数学上更紧密地耦合。

**适用边界与局限**

OGMM在ModelNet40、7Scenes和ICL-NUIM数据集上展示了优异的配准精度，但其适用边界清晰可辨：

1. **监督依赖**：重叠分数预测需要标注的重叠区域进行监督训练，难以直接迁移到无标注的真实场景。这是当前学习型重叠检测方法的共性局限。

2. **对称性与重复结构**：当场景中存在大量重复几何结构（如对称形状、重复纹理）时，聚类注意力可能提取到歧义特征，导致配准失败（见Figure 3不成功案例）。这是聚类策略的固有问题——簇中心的特征聚合可能抹平关键的局部区分性信息。

3. **重叠率敏感性**：消融实验（Table 7）显示，当重叠比率从70%降至30%时，MAE(R)由0.9111增至5.6462，表明低重叠场景仍是该方法的薄弱环节。重叠分数预测的准确性在极度稀疏的重叠区域会显著下降。

4. **超参数敏感性**：重叠分数预测依赖于预先设定的距离阈值$\eta$，对不同数据集可能需要手动调整。聚类数量$J$在32到64之间时配准误差较低且变化不大（Table 8），但最优值仍依赖于点云规模和几何复杂度。

5. **计算资源需求**：模型训练需要双Tesla V100 GPU，对计算环境有一定要求，限制了其在资源受限场景下的应用。

**开放问题**

1. **无监督/自监督重叠检测**：能否利用点云自身的几何一致性（如循环一致性、变换不变性）开发无监督或自监督的重叠区域检测方法，减少对标注数据的依赖，是该方法走向实际应用的关键一步。

2. **多模态对称性处理**：对于具有对称性或多个正确配准方案的物体（如碗、圆桌等），当前的损失函数（基于单一刚体变换的监督）可能产生模糊的梯度信号。如何设计对对称性鲁棒的配准目标函数，是一个值得探索的方向。

3. **自适应聚类策略**：聚类注意力中的$J$值目前是固定的超参数。是否存在基于点云几何复杂度和重叠率的自适应聚类策略，使模型在不同场景下自动调整簇的数量和分布？

4. **大规模户外点云的泛化**：该方法在室内场景和小规模物体上表现良好，但在户外大规模LiDAR点云（如自动驾驶场景）中的泛化能力尚未验证。户外场景的稀疏性、大尺度变化和动态物体可能对聚类注意力和GMM建模构成新的挑战。

5. **与隐式神经表示的融合**：GMM本质上是对点云分布的一种显式参数化建模。能否将重叠引导的思想与隐式神经表示（如神经距离场）结合，在保持对部分重叠鲁棒性的同时，提升对复杂几何细节的建模能力？

## 原文 PDF

![[paperPDFs/WACV_2023/Overlap_guided_gaussian_mixture_models_for_point_cloud_registration.pdf]]
