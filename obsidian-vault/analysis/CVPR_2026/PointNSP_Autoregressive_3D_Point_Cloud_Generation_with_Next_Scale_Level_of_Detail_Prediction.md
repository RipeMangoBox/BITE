---
title: "PointNSP: Autoregressive 3D Point Cloud Generation with Next-Scale Level-of-Detail Prediction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PointNSP_Autoregressive_3D_Point_Cloud_Generation_with_Next_Scale_Level_of_Detail_Prediction.pdf
project_link: null
code_link: null
aliases:
- PointNSP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将自回归建模从逐点预测转变为逐尺度（由粗到细的细节层次）预测，消除了固定的人为顺序，保留了置换不变性，并能够同时建模全局结构和局部细节。
primary_logic: 通过在粗分辨率上捕获全局形状结构，并在更高尺度上逐步细化细节，可以实现高质量且保持置换不变性的自回归点云生成，这本质上将生成任务转化为一系列保持全局一致性的上采样过程。
claims:
- 在ShapeNet基准测试（标准2048点、LION划分）上，PointNSP-m的Chamfer Distance（CD）均值为58.04，Earth Mover's Distance（EMD）均值为52.30，均取得最低值（最优），首次在自回归范式中达到最高生成质量。
- 在随机划分的2048点设定下，PointNSP-m也取得了最佳CD（均值59.65）和最佳EMD（均值56.13），验证了方法的鲁棒性。
- 在密集生成（8192点）以及55类多类别生成场景下，PointNSP均展现出一致的最高生成质量，且在训练时间、采样速度和参数量上显著优于扩散模型基线。
- 在点云补全和上采样下游任务中，PointNSP在所有类别上均优于所有选定的基线方法，证明其不仅适合无条件生成，也具备强大的条件推理能力。
---

# PointNSP: Autoregressive 3D Point Cloud Generation with Next-Scale Level-of-Detail Prediction

> [!tip] 核心洞察
> 通过在粗分辨率上捕获全局形状结构，并在更高尺度上逐步细化细节，可以实现高质量且保持置换不变性的自回归点云生成，这本质上将生成任务转化为一系列保持全局一致性的上采样过程。

| 字段 | 内容 |
|------|------|
| 中文题名 | PointNSP：基于下一尺度细节层次预测的自回归三维点云生成 |
| 英文题名 | PointNSP: Autoregressive 3D Point Cloud Generation with Next-Scale Level-of-Detail Prediction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Meng_PointNSP_Autoregressive_3D_Point_Cloud_Generation_with_Next-Scale_Level-of-Detail_Prediction_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | PointNSP |
| Dataset | ShapeNet, ShapeNet Completion |

> [!tip] 效果简介
> - ShapeNet (LION split, 2048 pts) 上，Chamfer Distance ↓ (mean) 58.04 (PointNSP-m) vs 优于所有基线（如 LION, TIGER） (最低（最优）)。
> - ShapeNet (random split, 2048 pts) 上，Earth Mover's Distance ↓ (mean) 56.13 (PointNSP-m) vs 优于所有基线 (最低（最优）)。
> - ShapeNet (8192 pts, dense generation) 上，生成质量（Chamfer Distance ↓） 显著优于所有基线（具体数值见原文） vs — (在8192点设定下优势更加显著)。

## 概述

三维点云生成的核心挑战在于：点云本质上是无序的点集，而传统自回归生成模型必须将点云强制排列为固定顺序的序列，这种人为引入的顺序破坏了置换不变性，导致模型难以捕捉全局几何结构与长距离依赖关系。扩散模型虽然避免了这一问题，但通常面临训练成本高、采样速度慢的瓶颈。

PointNSP 提出了一种范式转换：将自回归建模从“逐点预测”转变为“逐尺度预测”。具体而言，它构建由粗到细的多个细节层次（Level-of-Detail, LoD），形成从全局骨架到局部细节的因果序列。模型在每个尺度上预测一个完整的、具有全局一致性的点云，从而在保留自回归框架高效性的同时，天然地保持了置换不变性。这一设计本质上将生成任务重构为一系列保持全局一致性的上采样过程。

在 ShapeNet 基准测试上，PointNSP 首次在自回归范式下取得了最优生成质量：在标准 2048 点设定（LION 划分）下，PointNSP-m 的 Chamfer Distance 均值达到 58.04，Earth Mover's Distance 均值达到 52.30，均优于包括 **LION**（Zeng et al., NeurIPS 2022）和 **TIGER**（Ren et al., CVPR 2024）在内的强扩散基线。在随机划分下，该方法同样取得最佳 CD（59.65）和最佳 EMD（56.13），验证了其鲁棒性。在效率方面，PointNSP-s 的训练时间仅为 125 GPU 小时，相比扩散基线减少 70% 以上，同时在推理速度和参数量上均展现出显著优势。此外，PointNSP 在点云补全和上采样等下游任务中同样超越了所有选定基线，证明了其作为条件生成骨干的潜力。

## 背景与动机

三维点云作为一种灵活且紧凑的3D几何表示，在自动驾驶、机器人感知和计算机图形学等领域有着广泛的应用。近年来，深度生成模型在图像和文本领域取得了显著进展，然而三维点云的生成建模仍面临独特的挑战。点云由无序的点集构成，其概率分布天然地要求**置换不变性**——即点的排列不应改变形状本身。这一属性使得许多在有序数据上成功的生成范式难以直接迁移。

当前主流的点云生成方法主要分为两类：**扩散模型**和**自回归模型**。扩散模型（如 **DPM** (Luo and Hu, CVPR 2021)、**PVD** (Zhou et al., ICCV 2021)、**LION** (Zeng et al., NeurIPS 2022)、**TIGER** (Ren et al., CVPR 2024)）通过迭代去噪从高斯噪声中逐步恢复形状，天然保持了置换不变性，并取得了令人瞩目的生成质量。然而，这类方法通常需要数百甚至上千步的迭代采样，导致**推理速度慢、训练成本高**，在实时应用场景中受到限制。

相比之下，自回归模型（如 **PointGrow** (Sun et al., WACV 2020)、**PointGPT**、**ShapeFormer**）通过逐点预测的方式生成点云，具有采样速度快、可扩展性强的优势。但其核心瓶颈在于：**传统自回归模型将无序点集强制序列化为固定顺序**，这种人为的顺序假设引入了局部预测偏差，使得模型难以捕捉全局的几何结构和长距离依赖关系，从而破坏了全局形状的置换不变性和一致性。正如公式 $p(\mathbf{x}_1,\mathbf{x}_2,\ldots,\mathbf{x}_N)=\prod_{i=1}^N p(\mathbf{x}_i|\mathbf{x}_{i-1},\ldots,\mathbf{x}_1)$ 所示，逐点因子分解将点的生成顺序固化，而对于任意排列 $\pi\in S_N$，理想分布应满足 $p(\pi(\mathbf{x}_1,\ldots,\mathbf{x}_N))=p(\mathbf{x}_1,\ldots,\mathbf{x}_N)$。这种结构性矛盾导致自回归方法在点云生成质量上长期落后于扩散模型。

本文的核心动机在于回答一个根本性问题：**能否在自回归范式下实现保持置换不变性的高质量点云生成？** 换言之，能否既保留自回归模型的高效采样优势，又克服其因序列化导致的全局结构破坏？为此，我们提出 **PointNSP**，将自回归建模从逐点预测转变为**逐尺度细节层次（Level-of-Detail, LoD）预测**：在粗分辨率上捕获全局形状结构，并在更高尺度上逐步细化细节。这本质上将生成任务转化为一系列保持全局一致性的上采样过程，从而在自回归框架内首次实现了与扩散模型相媲美甚至更优的生成质量，同时显著降低了训练和推理成本。

## 核心创新

PointNSP 的核心创新在于将点云自回归生成的建模粒度从“逐点”提升到“逐尺度”，从根本上解决了传统自回归模型在无序点集上面临的置换不变性缺失与全局结构捕获困难两大瓶颈。

### 瓶颈与因果机制

传统自回归模型（如 **PointGrow** (Sun et al., WACV 2020)、**PointGPT**）将点云强制序列化为固定顺序，按式 $p(\mathbf{x}_1,\ldots,\mathbf{x}_N)=\prod_{i=1}^N p(\mathbf{x}_i|\mathbf{x}_{i-1},\ldots,\mathbf{x}_1)$ 进行逐点预测。这一范式引入了人为的顺序依赖，导致两个根本性问题：

1. **置换不变性被破坏**：概率分布对点的排列不再满足 $p(\pi(\mathbf{x}_1,\ldots,\mathbf{x}_N))=p(\mathbf{x}_1,\ldots,\mathbf{x}_N), \forall\pi\in S_N$，模型必须学习所有可能的排列，造成容量浪费和预测偏差。
2. **全局结构难以捕获**：逐点预测关注局部邻域关系，长距离依赖被序列位置所割裂，难以在生成早期建立完整的形状骨架。

PointNSP 通过因果旋钮的调整——将预测目标从“下一个点”改为“下一尺度细节层次”——消除了上述瓶颈。其因子分解为 $p(\mathbf{X}_1,\mathbf{X}_2,\ldots,\mathbf{X}_K)=\prod_{k=1}^K p(\mathbf{X}_k|\mathbf{X}_{k-1},\ldots,\mathbf{X}_1)$，其中每个 $\mathbf{X}_k$ 是一个完整形状在不同分辨率下的点云。这一转变将生成任务重塑为一系列保持全局一致性的上采样过程，粗尺度捕获整体拓扑，细尺度逐步注入几何细节。

### 三个关键 Changed Slot

#### Slot 1：生成范式——从逐点预测到逐尺度 LoD 预测

| 维度 | 基线范式 | PointNSP |
|------|---------|----------|
| 预测粒度 | 单个点坐标 | 完整形状的下一分辨率 |
| 序列长度 | $N$（点数，通常 2048） | $K$（尺度数，通常 3–5） |
| 置换不变性 | 需额外学习，不保证 | 天然保持（FPS 构建 + 全局形状输出） |
| 全局结构建模 | 后期逐步形成 | 第一尺度即建立骨架 |

FPS（最远点采样）迭代构建由粗到细的点云序列 $\mathbf{X}_1 \subset \mathbf{X}_2 \subset \cdots \subset \mathbf{X}_K$，保证了空间覆盖和置换不变性。生成过程由一系列上采样率 $r_1, r_2, \ldots, r_{K-1}$ 控制，本质上是一个自回归上采样过程。

#### Slot 2：点云离散表示——从单尺度 VQ-VAE 到多尺度残差 VQ-VAE

传统方法使用单尺度 VQ-VAE 将 $N$ 个点编码为一个 token 序列，丢失了多分辨率结构信息。PointNSP 的多尺度残差 VQ-VAE 分词器引入两个关键设计：

- **残差特征提取**：通过 $\mathbf{f}_k = \operatorname{query}(\mathbf{f}^{k-2}-\tilde{\mathbf{f}}_{k-1}, \mathbf{X}_k)$ 逐步减去上一尺度的贡献，使每个尺度的 token 仅编码该分辨率独有的几何信息，避免信息冗余。
- **共享码本**：所有尺度共享同一离散码本 $\mathcal{Z}$，降低参数量并强制尺度间特征对齐。

解码器采用 PU-Net 风格的复制-重塑上采样操作，将各尺度潜在表示 $\mathbf{z}_k$ 上采样到最终分辨率后求和，经 MLP 解码为 3D 点云。重建损失联合 Chamfer Distance、Earth Mover's Distance 和承诺损失：
$$\mathcal{L}_{\mathrm{recon}} = \mathcal{L}_{\mathrm{CD}}(\mathbf{X},\hat{\mathbf{X}}) + \mathcal{L}_{\mathrm{EMD}}(\mathbf{X},\hat{\mathbf{X}}) + \sum_{k=1}^K ||\mathbf{f}_k - sg(\mathbf{z}_k)||_2^2$$

#### Slot 3：注意力掩码——从标准因果掩码到块对角因果掩码 + 位置感知软掩码

标准自回归 Transformer 使用单向因果掩码，每个 token 只能关注之前的 token，限制了尺度内部的几何关系建模。PointNSP 设计了双重掩码策略：

- **块对角因果掩码**：将同一尺度内的 token 归为一个块，块内允许双向注意力，块间保持因果依赖。这使得模型在每个尺度内可以充分交互，捕获该分辨率下的完整几何结构，同时保持尺度间的自回归生成顺序。
- **位置感知软掩码**：利用解码器重建的中间形状坐标 $\mathbf{X}_k$ 生成绝对位置编码 $\mathbf{P}_k$，通过 $\mathbf{M}_k^p = \operatorname{Softmax}((\mathbf{P}_k \mathbf{W}_p)(\mathbf{P}_k \mathbf{W}_p)^T)$ 计算点间软相对位置矩阵，增强模型对 3D 几何结构的显式感知。

消融实验证实，位置感知软掩码、尺度嵌入、绝对位置编码（优于可学习位置编码）以及 FPS 路径增强（通过随机种子产生多条 FPS 序列）均对性能有显著贡献。在最佳消融配置下，模型在随机划分上达到 Mean CD 59.65, EMD 56.13。

### 创新点的协同效应

三个 changed slot 形成因果闭环：逐尺度范式（Slot 1）为多尺度表示（Slot 2）提供了建模需求，而多尺度 token 序列的层级结构又天然适配块对角因果掩码（Slot 3）的设计。三者协同使得 PointNSP 首次在自回归范式下达到与强扩散基线（如 **LION** (Zeng et al., NeurIPS 2022)、**TIGER** (Ren et al., CVPR 2024)）相当甚至更优的生成质量，同时在训练效率上降低 70% 以上（PointNSP-s 仅需 125 GPU 小时，而 LION 超过 500 GPU 小时）。

## 整体框架

### 核心洞察与范式转变

传统自回归点云生成方法（如 **PointGrow**, Sun et al., WACV 2020；**PointGPT**；**ShapeFormer**）将无序点集强制序列化为固定顺序进行逐点预测（next-point prediction），其概率分解为：

$$p(\mathbf{x}_1,\mathbf{x}_2,\ldots,\mathbf{x}_N)=\prod_{i=1}^N p(\mathbf{x}_i|\mathbf{x}_{i-1},\ldots,\mathbf{x}_1)$$

这种范式从根本上违背了点云的置换不变性要求——点云的概率分布应对任意排列保持不变：$p(\pi(\mathbf{x}_1,\ldots,\mathbf{x}_N))=p(\mathbf{x}_1,\ldots,\mathbf{x}_N), \forall \pi\in S_N$。人为引入的顺序导致模型产生局部预测偏差，难以捕捉全局几何结构和长距离依赖关系，从而破坏全局形状的一致性。

PointNSP 的核心洞察在于将自回归建模从**逐点预测**转变为**逐尺度预测**（next-scale LoD prediction）。通过构建由粗到细的细节层次（Level-of-Detail, LoD）序列，模型在粗分辨率上捕获全局形状结构，并在更高尺度上逐步细化细节。这一范式转变消除了固定的人为顺序，保留了置换不变性，本质上将生成任务转化为一系列保持全局一致性的上采样过程：

$$p(\mathbf{X}_1,\mathbf{X}_2,\ldots,\mathbf{X}_K)=\prod_{k=1}^K p(\mathbf{X}_k|\mathbf{X}_{k-1},\ldots,\mathbf{X}_1)$$

其中 $\mathbf{X}_1, \mathbf{X}_2, \ldots, \mathbf{X}_K$ 表示从粗到细的 $K$ 个全局点云，每个分辨率对应一个完整的形状表示。生成过程受上采样率序列 $r_1, r_2, \ldots, r_{K-1}$ 控制，与自回归上采样过程高度相似。

### 整体 Pipeline

PointNSP 的整体框架分为两个训练阶段（如 Figure 3 所示），包含五个核心模块：

![[assets/figures/papers/paper_list_l2571_https_openaccess_thecvf_com_content_CVPR2026_html_Meng_PointNSP_Autoregr/figures/003_Figure_3.jpg]]
*Figure 3: (a) Illustration of training a multi-scale VQVAE in a residual manner for point cloud representation across scales s1 to s3, resulting in a multi-scale token sequence*

**阶段一：多尺度 VQ-VAE 分词器训练**

1. **LoD 序列构建（FPS）**：对原始点云使用最远点采样（Farthest Point Sampling, FPS）迭代构建由粗到细的 $K$ 个点云序列 $\mathbf{X}_1 \subset \mathbf{X}_2 \subset \cdots \subset \mathbf{X}_K$，保证置换不变性和空间覆盖。

2. **多尺度残差特征提取器**：使用置换等变网络从原始点云提取特征，并逐步减去上一尺度的贡献以得到各尺度的残差特征：
   $$\mathbf{f}_k = \operatorname{query}(\mathbf{f}^{k-2}-\tilde{\mathbf{f}}_{k-1},\mathbf{X}_k), \quad \mathbf{f}_1 = \operatorname{query}(\mathbf{f}^0,\mathbf{X}_1)$$
   这种残差设计确保每个尺度的 token 仅编码该尺度独有的几何信息。

3. **多尺度 VQ-VAE 分词器**：将各尺度的残差特征 $\mathbf{f}_k$ 通过共享码本量化为离散 token 序列 $\mathbf{z}_k$，形成多尺度 token 序列 $Q = (q_1, q_2, \ldots, q_K)$。解码时，各尺度潜在表示通过 PU-Net 风格的复制-重塑操作上采样到最终分辨率：
   $$\mathbf{z}_k (s_k \times d) \xrightarrow{\mathrm{duplicate}} \mathbf{z}_k (s_k \times r \times d) \xrightarrow{\mathrm{reshape}} \mathbf{z}_k ((s_k \cdot r) \times d)$$
   求和后通过 MLP 解码为 3D 点云。重建损失结合 Chamfer Distance、Earth Mover's Distance 和承诺损失：
   $$\mathcal{L}_{\mathrm{recon}} = \mathcal{L}_{\mathrm{CD}}(\mathbf{X},\hat{\mathbf{X}}) + \mathcal{L}_{\mathrm{EMD}}(\mathbf{X},\hat{\mathbf{X}}) + \sum_{k=1}^K ||\mathbf{f}_k - sg(\mathbf{z}_k)||_2^2$$

**阶段二：自回归 Transformer 训练**

4. **自回归 Transformer 与块对角因果掩码**：接收多尺度 token 序列，使用**块对角因果掩码**（block-wise causal mask）实现尺度间的自回归依赖和尺度内的双向交互。与标准自回归的单向因果掩码不同，该设计允许同一尺度内的 token 进行双向注意力，从而更好地建模局部几何结构。

5. **位置感知软掩码模块**：利用部分 token 序列重建的中间形状 $\mathbf{X}_k = D(\sum_{m=1}^k \phi_m(\mathrm{upsampling}(\mathbf{z}_m, s_m)))$ 生成绝对位置编码，通过 softmax 计算软掩码矩阵 $\mathbf{M}_k^p = \operatorname{Softmax}((\mathbf{P}_k \mathbf{W}_p)(\mathbf{P}_k \mathbf{W}_p)^T)$，增强模型对几何结构的空间感知能力。

### 输入输出流

- **训练阶段一**：输入原始点云 $\mathbf{X}$ → FPS 构建 LoD 序列 → 多尺度残差特征提取 → 共享码本量化 → 上采样与解码重建 → 输出重建点云 $\hat{\mathbf{X}}$，优化重建损失。
- **训练阶段二**：输入多尺度 token 序列 $Q$ → 块对角因果 Transformer（含位置感知软掩码）→ 预测下一尺度 token → 优化交叉熵损失。
- **推理生成**：从最粗尺度 token $q_1$ 开始，自回归预测 $q_2, \ldots, q_K$ → 通过 VQ-VAE 解码器重建最终点云。

### 方法谱系与知识库定位

PointNSP 在生成范式上区别于以下基线：
- **扩散模型**：**DPM**（Luo and Hu, CVPR 2021）、**PVD**（Zhou et al., ICCV 2021）、**LION**（Zeng et al., NeurIPS 2022）、**TIGER**（Ren et al., CVPR 2024）、**DiT-3D**（Mo et al., NeurIPS 2023）采用迭代去噪生成，PointNSP 以自回归方式实现更高效的训练和采样。
- **传统自回归模型**：**PointGrow**（Sun et al., WACV 2020）、**PointGPT**、**ShapeFormer**、**PointVQVAE** 采用逐点预测，PointNSP 通过逐尺度预测保留置换不变性。
- **基于流的模型**：**PointFlow**（Yang et al., ICCV 2019）采用连续归一化流，PointNSP 在离散 token 空间建模。

PointNSP 的上采样机制借鉴了 **PU-Net**（Yu et al., CVPR 2018）的复制-重塑操作，LoD 序列构建基于经典的 FPS 算法（Eldar et al., IEEE TIP 1997），位置编码采用三角函数绝对位置编码。

### 补充图表

![[assets/figures/papers/paper_list_l2571_https_openaccess_thecvf_com_content_CVPR2026_html_Meng_PointNSP_Autoregr/figures/002_Figure_2.jpg]]
*Figure 2: Three types of point cloud generative models: (a) diffusion-based methods that iteratively denoise shapes starting from Gaussian noise; (b) vanilla autoregressive (AR) methods that predict the next point by flattening the 3D shape into a sequence; and (c) our proposed PointNSP, which predicts next-scale level-of-detail in a coarse-to-fine manner*

## 核心模块与公式推导

### 1. 范式转换：从逐点预测到逐尺度预测

传统自回归点云生成将无序点集强制序列化为固定顺序，其概率因子分解为：

$$p(\mathbf{x}_1,\mathbf{x}_2,\ldots,\mathbf{x}_N)=\prod_{i=1}^N p(\mathbf{x}_i|\mathbf{x}_{i-1},\ldots,\mathbf{x}_1)$$

该形式破坏了置换不变性——点云的概率分布应对任意排列保持不变：

$$p(\pi(\mathbf{x}_1,\ldots,\mathbf{x}_N))=p(\mathbf{x}_1,\ldots,\mathbf{x}_N), \forall \pi\in S_N$$

PointNSP 将建模对象从“逐点”切换为“逐尺度细节层次（LoD）”。给定由粗到细的 $K$ 个全局形状序列 $\mathbf{X}_1,\mathbf{X}_2,\ldots,\mathbf{X}_K$，自回归因子分解变为：

$$p(\mathbf{X}_1,\mathbf{X}_2,\ldots,\mathbf{X}_K)=\prod_{k=1}^K p(\mathbf{X}_k|\mathbf{X}_{k-1},\ldots,\mathbf{X}_1)$$

该形式天然保持置换不变性，因为每一步预测的是完整点云而非单个点。生成过程本质上是一个受上采样率序列 $r_1,r_2,\ldots,r_{K-1}$ 控制的自回归上采样过程。

### 2. 多尺度残差 VQ-VAE 分词器

**LoD 序列构建**：采用最远点采样（FPS）迭代构建因果序列，满足 $\mathbf{X}_{k-1}=\mathrm{FPS}(\mathbf{X}_k)$，保证置换不变性和空间覆盖。

**残差特征提取**：使用置换等变网络从原始点云提取特征，并逐步减去上一尺度的贡献，以聚焦各尺度独有的信息：

$$\mathbf{f}_k = \operatorname{query}(\mathbf{f}^{k-2}-\tilde{\mathbf{f}}_{k-1},\mathbf{X}_k), \quad \mathbf{f}_1 = \operatorname{query}(\mathbf{f}^0,\mathbf{X}_1)$$

各尺度残差特征经共享码本量化后得到离散 token 序列。

**上采样与解码**：借鉴 PU-Net 的复制-重塑操作，将各尺度潜在表示上采样到最终分辨率：

$$\mathbf{z}_k (s_k \times d) \xrightarrow{\mathrm{duplicate}} \mathbf{z}_k (s_k \times r \times d) \xrightarrow{\mathrm{reshape}} \mathbf{z}_k ((s_k \cdot r) \times d)$$

上采样后的特征求和，通过 MLP 解码为最终 3D 点云。训练时，重建损失结合 Chamfer Distance、Earth Mover's Distance 和承诺损失：

$$\mathcal{L}_{\mathrm{recon}} = \mathcal{L}_{\mathrm{CD}}(\mathbf{X},\hat{\mathbf{X}}) + \mathcal{L}_{\mathrm{EMD}}(\mathbf{X},\hat{\mathbf{X}}) + \sum_{k=1}^K ||\mathbf{f}_k - sg(\mathbf{z}_k)||_2^2$$

### 3. 自回归 Transformer 与掩码策略

**块对角因果掩码**：接收多尺度 token 序列后，Transformer 使用块对角因果掩码实现尺度间的自回归依赖和尺度内的双向交互。与标准单向因果掩码不同，该设计允许同一尺度内的 token 充分交互以建模全局几何关系。

**位置感知软掩码**：利用解码器 $D$ 从已生成的部分 token 序列重建中间形状 $\mathbf{X}_k$：

$$\mathbf{X}_k = D\left(\sum_{m=1}^k \phi_m(\mathrm{upsampling}(\mathbf{z}_m, s_m))\right)$$

从 $\mathbf{X}_k$ 的 3D 坐标出发，通过三角函数生成绝对位置编码 $\mathbf{P}_k$，再计算点间软相对位置矩阵：

$$\mathbf{M}_k^p = \operatorname{Softmax}\left((\mathbf{P}_k \mathbf{W}_p)(\mathbf{P}_k \mathbf{W}_p)^T\right), \quad \mathbf{W}_p \in \mathbb{R}^{d \times d}$$

该软掩码增强了模型对几何结构的感知能力。消融实验证实，位置感知软掩码、绝对位置编码（A-PE 优于可学习 L-PE）以及尺度嵌入均对性能有显著贡献。

## 实验与分析

### 核心生成质量：2048点标准设定

PointNSP在ShapeNet基准上的生成质量首次使自回归范式超越了扩散模型。在标准的2048点设定下，PointNSP在两个主流数据划分上均取得最优结果（Table 1）：

![[assets/figures/papers/paper_list_l2571_https_openaccess_thecvf_com_content_CVPR2026_html_Meng_PointNSP_Autoregr/figures/004_Table_1.jpg]]
*Table 1: Performance under the standard 2048-point setup on ShapeNet is reported for two dataset splits: the top corresponds to the conventional random split, and the bottom corresponds to the LION split [65]. The best results are highlighted in bold with a green bar, and the second-best results are underlined*

- **LION划分**（Zeng et al., NeurIPS 2022）：PointNSP-m的Chamfer Distance（CD）均值降至**58.04**，Earth Mover's Distance（EMD）均值降至**52.30**，均优于所有基线方法，包括强扩散基线**LION**和**TIGER**（Ren et al., CVPR 2024）。
- **随机划分**：PointNSP-m同样取得最优，CD均值**59.65**，EMD均值**56.13**，验证了方法在不同数据划分下的鲁棒性。

这一结果的关键在于逐尺度预测范式消除了传统自回归方法（如**PointGrow**, Sun et al., WACV 2020）因固定点序引入的置换偏差。通过从粗到细建模完整形状序列，模型在粗尺度上捕获全局结构，在细尺度上逐步细化局部细节，避免了逐点预测中长距离依赖断裂的问题。

### 密集生成与多类别泛化

在更高分辨率的8192点密集生成场景下，PointNSP的优势进一步扩大（Table 2左）。随着点数增加，逐点自回归方法的序列长度线性增长，导致误差累积加剧；而PointNSP的序列长度仅与尺度数K相关（通常K=3或4），与最终点数解耦，因此在密集生成中保持稳定的建模质量。

在55类多类别生成任务中（Table 2右），PointNSP-m在所有类别上均取得最优或次优结果（以Airplane类为例，CD为**75.42**），证明其框架对不同几何拓扑具有良好的泛化能力，并非仅适用于单一类别。

### 效率优势

PointNSP在效率上显著优于扩散基线（Table 3）：

![[assets/figures/papers/paper_list_l2571_https_openaccess_thecvf_com_content_CVPR2026_html_Meng_PointNSP_Autoregr/figures/008_Table_3.jpg]]
*Table 3: Training time (in GPU hours, averaged over three categories), sampling time (in seconds, averaged over samples), and model size (in millions of parameters). Ranked by generation quality on 2048 and 8192 settings*

- **训练时间**：PointNSP-s仅需**125 GPU小时**，而扩散方法**LION**超过500 GPU小时，训练时间减少约70%。
- **采样速度**：PointNSP-s的单样本采样时间为**3.21秒**，远快于需要多步去噪的扩散模型。
- **参数量**：PointNSP-s仅**22M参数**，在2048点设定下即达到有竞争力的质量。

效率优势源于自回归模型只需一次前向传播即可完成生成，而扩散模型需要数十到数百步迭代去噪。此外，多尺度token序列的长度远小于逐点序列，进一步降低了Transformer的计算开销。

### 下游任务：补全与上采样

PointNSP不仅适用于无条件生成，在条件推理任务上也表现出色（Table 5）：

![[assets/figures/papers/paper_list_l2571_https_openaccess_thecvf_com_content_CVPR2026_html_Meng_PointNSP_Autoregr/figures/011_Table_5.jpg]]
*Table 5: Comparison on partial shape completion (left) and point cloud upsampling task (right)*

- **点云补全**：在Airplane类别上，PointNSP取得CD **40.12**、EMD **10.08**，优于**PVD**（Zhou et al., ICCV 2021）和**PointFlow**（Yang et al., ICCV 2019）等专门设计的基线方法。这得益于逐尺度生成天然适合补全任务——粗尺度可快速恢复缺失部分的全局轮廓，细尺度再逐步补充细节。
- **点云上采样**：在所有测试类别上均优于选定基线，验证了其作为通用3D生成框架的潜力。

### 消融实验

消融实验（Table 4及相关分析）揭示了各设计选择的贡献：

1. **上采样策略**：PU-Net风格的复制-重塑上采样（Eq.6）优于基于体素的上采样方法。归因于其置换等变设计，与点云的天然属性一致，避免了体素化引入的量化误差。

2. **位置感知软掩码**：移除该模块后性能显著下降。该掩码利用重建的中间形状坐标生成绝对位置编码，通过softmax计算点间软相对位置矩阵（Eq.8），使Transformer在尺度内部双向交互时能感知几何结构，而非仅依赖token顺序。

3. **尺度嵌入**：对性能有显著影响。尺度嵌入使模型能区分不同分辨率的token序列，避免混淆粗粒度结构token与细粒度细节token。

4. **位置编码类型**：绝对位置编码（A-PE）优于可学习位置编码（L-PE）。A-PE基于3D坐标的三角函数编码，直接注入几何先验，使模型无需从数据中学习位置关系。

5. **FPS路径增强**：通过随机种子产生多条FPS序列进行数据增强，持续提升模型泛化能力。这缓解了FPS采样的确定性可能导致的过拟合。

在最佳消融配置下，模型在随机划分上达到Mean CD **59.65**、EMD **56.13**，验证了各模块的协同作用。

### 生成过程可视化

Figure 5展示了随着尺度K增加，点云从粗到细的渐进式生成过程：K=1时仅呈现粗略的全局轮廓，K=2时补充主要结构特征，K=3时完成细节填充。这一可视化直观印证了逐尺度预测的核心机制——每个尺度对应一个完整的全局形状，而非局部补丁，从而在生成全过程中保持全局一致性。

### 补充图表

![[assets/figures/papers/paper_list_l2571_https_openaccess_thecvf_com_content_CVPR2026_html_Meng_PointNSP_Autoregr/figures/005_Figure_4.jpg]]
*Figure 4: Visualization of generation results compared with baseline models. PointNSP produces high-quality and diverse 3D point clouds*

![[assets/figures/papers/paper_list_l2571_https_openaccess_thecvf_com_content_CVPR2026_html_Meng_PointNSP_Autoregr/figures/007_Figure_5.jpg]]
*Figure 5: Visualization of multi-scale point clouds during the PointNSP generation process as the scale K increases*

![[assets/figures/papers/paper_list_l2571_https_openaccess_thecvf_com_content_CVPR2026_html_Meng_PointNSP_Autoregr/figures/009_Figure_6.jpg]]
*Figure 6: (Left) Visualizations of point cloud completion results. (Right) Visualizations of point cloud upsampling results*

![[assets/figures/papers/paper_list_l2571_https_openaccess_thecvf_com_content_CVPR2026_html_Meng_PointNSP_Autoregr/figures/010_Table_4.jpg]]
*Table 4: Training time (in GPU hours, averaged over three categories), sampling time (in seconds, averaged over samples), and model size (in millions of parameters). Ranked by generation quality on 2048 and 8192 settings*

## 方法谱系与知识库定位

### 生成范式谱系：从逐点预测到逐尺度细节层次建模

PointNSP 的核心贡献在于将三维点云的自回归生成从“逐点预测”范式重新定义为“逐尺度细节层次（Next-Scale LoD）预测”范式。这一转变直接回应了传统自回归方法在点云生成中长期存在的结构性瓶颈。

传统自回归模型（如 **PointGrow** (Sun et al., WACV 2020)、**PointGPT**、**ShapeFormer**、**PointVQVAE**）将无序点集强行序列化为固定顺序的序列，通过链式法则逐点预测：

$$p(\mathbf{x}_1,\mathbf{x}_2,\ldots,\mathbf{x}_N)=\prod_{i=1}^N p(\mathbf{x}_i|\mathbf{x}_{i-1},\ldots,\mathbf{x}_1)$$

这种因子分解方式从根本上违背了点云的概率分布对排列的不变性要求：

$$p(\pi(\mathbf{x}_1,\ldots,\mathbf{x}_N))=p(\mathbf{x}_1,\ldots,\mathbf{x}_N), \forall \pi\in S_N$$

人为引入的顺序导致模型产生局部预测偏差，难以捕捉全局几何结构和长距离依赖关系，最终破坏生成形状的全局一致性。

PointNSP 通过将建模对象从单个点转变为整个尺度层级的完整形状，从根本上消除了固定顺序的需求。其因子分解形式为：

$$p(\mathbf{X}_1,\mathbf{X}_2,\ldots,\mathbf{X}_K)=\prod_{k=1}^K p(\mathbf{X}_k|\mathbf{X}_{k-1},\ldots,\mathbf{X}_1)$$

其中 $\mathbf{X}_k$ 是第 $k$ 个尺度下的完整点云，由粗到细构成因果序列。这一范式转变实质上将生成任务重新定义为一系列保持全局一致性的上采样过程——在粗分辨率上捕获全局形状结构，在更高尺度上逐步注入细节信息。

与扩散模型范式（如 **DPM** (Luo and Hu, CVPR 2021)、**PVD** (Zhou et al., ICCV 2021)、**LION** (Zeng et al., NeurIPS 2022)、**TIGER** (Ren et al., CVPR 2024)、**DiT-3D** (Mo et al., NeurIPS 2023)）相比，PointNSP 避免了迭代去噪过程的推理开销，在采样速度和训练效率上展现出显著优势。与基于流的 **PointFlow** (Yang et al., ICCV 2019) 相比，PointNSP 的自回归框架提供了更灵活的生成控制能力。

### 技术组件定位与改进

PointNSP 的技术架构由三个关键组件的创新构成，每个组件都针对现有方法的不足进行了定向改进：

**（1）多尺度残差 VQ-VAE 分词器**：传统方法使用单尺度 VQ-VAE 将 $N$ 个点编码为一个 token 序列，丢失了跨尺度的结构信息。PointNSP 采用共享码本的多尺度残差 VQ-VAE，通过最远点采样（FPS）构建由粗到细的点云序列，并利用残差特征提取机制 $\mathbf{f}_k = \operatorname{query}(\mathbf{f}^{k-2}-\tilde{\mathbf{f}}_{k-1},\mathbf{X}_k)$ 聚焦各尺度独有的信息，避免跨尺度信息冗余。

**（2）块对角因果掩码与位置感知软掩码**：标准自回归的因果注意力掩码强制单向依赖，限制了同尺度内部点的几何关系建模。PointNSP 引入块对角因果掩码，允许尺度内部双向注意力交互，同时保持尺度间的自回归依赖。在此基础上，位置感知软掩码 $\mathbf{M}_k^p = \operatorname{Softmax}((\mathbf{P}_k \mathbf{W}_p)(\mathbf{P}_k \mathbf{W}_p)^T)$ 利用重构中间形状的绝对坐标编码，增强模型对几何结构的感知能力。

**（3）PU-Net 风格的上采样解码器**：借鉴 PU-Net 的复制-重塑操作 $\mathbf{z}_k (s_k \times d) \xrightarrow{\mathrm{duplicate}} \mathbf{z}_k (s_k \times r \times d) \xrightarrow{\mathrm{reshape}} \mathbf{z}_k ((s_k \cdot r) \times d)$，PointNSP 实现了置换等变的上采样过程，消融实验证实其性能优于基于体素的上采样方案。

### 适用边界与局限

PointNSP 在 ShapeNet 基准上展示了强大的生成能力，但其适用边界仍需审视：

- **分辨率扩展性**：当前验证覆盖 2048 点和 8192 点的生成设定，在极高分辨率（如 >50K 点）下的计算和内存效率尚未得到验证，FPS 构建的多尺度序列可能面临存储开销的线性增长。
- **类别多样性**：55 类多类别生成实验表明方法具备类别泛化能力，但所有实验均在 ShapeNet 的人造物体范畴内进行，对自然场景或开放世界点云的适用性有待探索。
- **表示形式的限制**：方法专为点云设计，能否迁移至其他三维表示（如网格、NeRF）仍为开放问题。

### 开放问题

1. 多尺度细节层次结构天然支持可控生成——能否利用中间尺度表示实现局部编辑和交互式生成，而无需重新生成完整形状？
2. 在极高分辨率场景下，如何设计更高效的尺度序列构建策略以降低计算开销？
3. 能否将“逐尺度预测”的核心思想推广到其他非欧几里德数据的自回归生成中？

### 知识库定位总结

PointNSP 首次在自回归范式内实现了与强扩散基线相媲美甚至超越的生成质量，证明了“逐尺度细节层次预测”是解决点云置换不变性建模的有效路径。该方法弥合了自回归模型在效率上的固有优势与扩散模型在质量上的领先地位之间的鸿沟，为三维生成领域提供了第三条技术路线。

## 原文 PDF

![[paperPDFs/CVPR_2026/PointNSP_Autoregressive_3D_Point_Cloud_Generation_with_Next_Scale_Level_of_Detail_Prediction.pdf]]