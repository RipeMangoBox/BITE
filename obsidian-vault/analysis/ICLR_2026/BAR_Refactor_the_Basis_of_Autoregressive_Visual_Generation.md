---
title: "BAR: Refactor the Basis of Autoregressive Visual Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/BAR_Refactor_the_Basis_of_Autoregressive_Visual_Generation.pdf
project_link: null
code_link: null
aliases:
- BAB
- BAR
- "Basis Autoregressive (BAR)"
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "学习正交线性变换矩阵重构自回归视觉token基。"
primary_logic: "BAR先把潜在token序列变换为可学习基下的序列，再用AR Transformer预测并逆变换回原始空间生成图像。"
claims:
- "BAR把VAR、xAR、RAR、PAR和FAR等自回归变体统一为线性变换y等于Ax的特例。"
- "正交约束保持变换前后欧氏范数与高斯噪声分布，使训练目标与原空间一致。"
- "残差BAR目标鼓励早期token重建全局图像、后期token补充残差细节。"
- "BAR在ImageNet 256和512以及MS-COCO文本到图像任务上优于对应xAR和MAR基线。"
---

# BAR: Refactor the Basis of Autoregressive Visual Generation

> [!tip] 核心洞察
> 将token视为图像向量在子空间上的投影，通过一个端到端可学习的正交变换矩阵A，将固定token序列重构为更适合自回归预测的新序列，从而超越手工设计的归纳偏置。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | BAR：重构自回归视觉生成的基础 |
| 英文题名 | BAR: Refactor the Basis of Autoregressive Visual Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=2m9XQq4Dc3) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Basis Autoregressive (BAR) |
| Dataset | ImageNet 256×256 |

> [!tip] 效果简介
> - ImageNet 256×256 上，FID 为 1.15，对比 1.24 (xAR-H)，变化 -0.09。
> - ImageNet 256×256 上，IS 为 327.1，对比 310.6 (xAR-H)，变化 +16.5。
> - ImageNet 256×256 上，Precision 为 0.86，对比 0.85 (xAR-H)，变化 +0.01。

## 概要

本文提出 **Basis Autoregressive (BAR)**，一种全新的自回归视觉生成范式。BAR 的核心思想是将图像 token 视为图像向量在线性子空间上的投影，并通过一个端到端可学习的正交变换矩阵 **A**，将固定的 token 序列重构为更适合自回归预测的新序列。该方法在 ImageNet 256×256 条件生成任务上取得了 **FID 1.15** 的最优结果，超越了此前所有自回归和扩散模型。BAR 不仅统一了先前多种自回归变体（VAR, xAR, RAR, PAR, FAR 等）为线性变换 **y = Ax** 的特例，还通过自适应学习发现了超越手工设计的预测策略。



传统自回归（AR）视觉生成模型将图像展平为固定光栅扫描顺序的 1D token 序列，这一做法忽略了图像的 2D 结构，限制了模型能力。近年来，研究者提出了多种改进方案：VAR（Tian et al., 2024）采用粗到细的尺度预测，xAR（Ren et al., 2025）引入连续 AR 和流匹配目标，RAR（Yu et al., 2024b）使用随机排列退火，PAR（Wang et al., 2024）采用并行解码，FAR（Yu et al., 2025）在频域进行预测。然而，这些方法都依赖于手工设计的归纳偏置，缺乏统一的数学框架。

BAR 的洞察在于：将 token 序列的预测顺序和分组视为一个可学习的线性变换问题。通过将标准基向量替换为可学习的基向量，模型能够自适应地发现最优的预测策略，从而超越手工设计的局限。



## 核心方法与创新机理

BAR 的核心创新可归纳为三点：

1. **统一数学框架**：将先前所有 AR 变体形式化为线性变换 **y = Ax** 的特例，其中矩阵 **A** 的行向量构成变换后的基。VAR 对应多尺度平均池化变换，xAR 对应标准基的重排序和重分组，RAR 对应随机置换矩阵，PAR 对应选择矩阵，FAR 对应多频滤波器。

2. **端到端可学习变换**：提出参数化、可学习的变换矩阵 **A**，与 AR Transformer 联合优化，无需手工设计。矩阵 **A** 被约束为方阵和正交矩阵，以保持欧几里得范数。

3. **残差训练目标**：引入残差目标 $\mathcal{L}_{\mathrm{residual\ BAR}}$，强制早期 token 最大化重建图像，后期 token 恢复残差，从而自然地实现粗到细的生成特性。



![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_2m9XQq4Dc3_BAR_Refactor_/figures/001_Figure_1.jpg]]
*Figure 1: An overview of the unified framework of BAR and its strength over previous approaches. (a) By applying a linear transform associated with the matrix A, BAR offers the generalized viewpoint that encompasses prior methods as specific instances of A and facilitates further extensions. (b) BAR at its core lies that each token x _ { k } is the projection of whole image x on a sub-space, or basis with channels omitted. It transforms the standard basis e _ { k } into the row vectors a _ { k } of matrix A. (c) We illustrate each method with its corresponding a _ { k } . While vanilla AR directly employs e _ { i } as raster scan of tokens and VAR manually designs a coarse-to-fine pattern,...*

BAR 的整体流水线如 Figure 2 所示，包含以下模块：

- **VAE 编码器**：使用 LDM（Rombach et al., 2022）的连续 KL-16 VAE 将图像编码为连续潜在特征网格。
- **线性变换层（矩阵 A）**：将原始 token 序列 **x** 变换为新序列 **y = Ax**，其中 **A** 是可学习的正交矩阵。
- **AR Transformer**：在变换后的序列 **y** 上进行自回归预测。
- **逆变换层（A⁻¹）**：将预测的 **ŷ** 变换回原始空间 **x̂ = A⁻¹ ŷ**。
- **VAE 解码器**：将预测的潜在特征解码为图像。

Figure 1 展示了 BAR 的统一框架概览：(a) 通过线性变换 **A**，BAR 将先前方法作为特例统一；(b) 每个 token 是图像在子空间上的投影；(c) 不同方法对应的基向量可视化。



### 5.1 自回归分解与基线损失

标准自回归分解为：
$$p_\theta(\mathbf{x}) = \prod_{k=1}^N p_\theta(x_k \mid x_{<k})$$

MAR（Li et al., 2024b）使用扩散去噪损失：
$$\mathcal{L}_{\mathrm{MAR}}(z_k, x_k) = ||\epsilon - \epsilon_\eta(x_k^t | t, z_k)||_2^2$$

xAR（Ren et al., 2025）使用流匹配目标：
$$\mathcal{L}_{\mathrm{xAR}}(\mathbf{x}) = \sum_{k=1}^N \left\| v_\theta(\{x_1^{t_1}, x_2^{t_2}, \dots, x_k^{t_k}\}, t_k) - v_k^{t_k} \right\|_2^2$$

### 5.2 BAR 线性变换与子空间重构

BAR 的核心变换定义为：
$$\mathbf{y} := \mathbf{Ax}$$

其中 **A** ∈ ℝ^{N×N} 是满秩矩阵。标准基子空间 $\{S_k | S_k := \mathrm{span}(e_k), 1 \le k \le N\}$ 被变换为 $\{S_k' | S_k' := \mathrm{span}(a_k), 1 \le k \le N'\}$，其中 $a_k$ 是 **A** 的行向量。

### 5.3 等价性证明

**命题 1**：在变换序列 **y** 上优化 BAR 等价于在原始序列 **x** 上优化 MAR，即：
$$\mathcal{L}_{\mathrm{BAR}}(\mathbf{y}) = \frac{\bar{\alpha}_t}{1-\bar{\alpha}_t} \|\mathbf{y} - \hat{\mathbf{y}}\|_2^2 = \frac{\bar{\alpha}_t}{1-\bar{\alpha}_t} \|\mathbf{A}(\mathbf{x} - \hat{\mathbf{x}})\|_2^2$$

当 **A** 正交时，$\|\mathbf{A}(\mathbf{x} - \hat{\mathbf{x}})\|_2^2 = \|\mathbf{x} - \hat{\mathbf{x}}\|_2^2$，因此 $\mathcal{L}_{\mathrm{BAR}}(\mathbf{y}) = \mathcal{L}_{\mathrm{MAR}}^{\mathrm{ref}}(\mathbf{x})$。

**命题 2**：优化 BAR 在变换序列 **y** 上等价于 xAR 在原始序列 **x** 上。

### 5.4 残差 BAR 目标

为显式强制基向量的有序性，引入残差目标：
$$\mathcal{L}_{\mathrm{residual\ BAR}}(\mathbf{y}) = \frac{\bar{\alpha}_t}{1-\bar{\alpha}_t} \sum_{k=1}^N \|\mathbf{x} - \mathbf{A}^\top \tilde{\mathbf{y}}_k\|_2^2$$

其中 $\tilde{\mathbf{y}}_k$ 是预测 **ŷ** 的前 k 个 token 组成的向量。该损失鼓励早期 token 最大化重建图像，后期 token 恢复残差。

### 5.5 正交正则化与投影

为保持 **A** 的正交性，使用正则化项：
$$\mathcal{L}_{\mathrm{reg}} := \|\mathbf{A}^\top \mathbf{A} - \mathbf{I}\|_2^2$$

同时采用软正交投影：通过 SVD 分解 $\mathbf{A} = \mathbf{USV}^\top$，将奇异值夹紧到 $(1-\delta, 1+\delta)$ 区间。

### 5.6 变换噪声的保持

变换后的噪声 $\epsilon'_k = \sum_{l=1}^N a_{k,l} \epsilon_l$ 保持独立同分布高斯噪声，协方差为：
$$\Sigma_{\epsilon'} = \mathbf{A} \mathbf{A}^\top = \mathbf{I}$$

这一性质确保了 BAR 在变换空间中的训练与原始空间等价。



## 实验与关键发现

### 6.1 主要结果

**Table 1** 展示了 ImageNet 256×256 条件生成上的系统级比较：

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_2m9XQq4Dc3_BAR_Refactor_/figures/004_Table_1.jpg]]
*Table 1: Benchmarking conditional image generation on ImageNet 2 5 6 $\times$ 2 5 6 . Initialization of the transform matrix A is important for its optimization. While the identity matrix I corresponds to vanilla AR, we can also use a random matrix followed by an orthogonal projection.*

| 方法 | FID ↓ | IS ↑ | Precision ↑ | Recall ↑ | #Step | #Param |
|------|-------|------|-------------|----------|-------|--------|
| BAR-H (ours) | **1.15** | **327.1** | **0.86** | **0.68** | 50 | 1.1B |
| xAR-H | 1.24 | 310.6 | 0.85 | 0.65 | 50 | 1.1B |
| MAR-H | 1.55 | 303.0 | 0.83 | 0.63 | 256 | 1.1B |
| VAR-d30 | 1.73 | 350.2 | 0.84 | 0.61 | 10 | 2.0B |
| DiT-XL/2 | 2.27 | 278.2 | 0.83 | 0.57 | 250 | 0.7B |

BAR-H 以 1.15 的 FID 达到当时最优，相比 xAR-H 降低 0.09，相比 MAR-H 降低 0.40。

**Table 2** 验证了 BAR 在不同模型上的兼容性：

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_2m9XQq4Dc3_BAR_Refactor_/figures/008_Table_2.jpg]]
*Table 2: Experiments on different models.*

| 模型 | 基线 FID | BAR FID | 改进 |
|------|---------|---------|------|
| MAR-B | 2.31 | **2.18** | -0.13 |
| MAR-L | 1.78 | **1.56** | -0.22 |
| MAR-H | 1.553 | **1.49** | -0.063 |
| xAR-B | 1.722 | **1.63** | -0.092 |
| xAR-L | 1.28 | **1.24** | -0.04 |
| xAR-H | 1.24 | **1.15** | -0.09 |

**Table 3** 展示了 ImageNet 512×512 上的结果：BAR-H 取得 FID 2.55，优于 xAR-H 的 2.68。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_2m9XQq4Dc3_BAR_Refactor_/figures/011_Table_3.jpg]]
*Table 3: Experiments on ImageNet 512.*

**Table 4** 展示了文本到图像生成结果：BAR 在 MS-COCO 上取得 FID 8.89，优于 FAR 的 9.19 和 LDM 的 12.63。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_2m9XQq4Dc3_BAR_Refactor_/figures/009_Table_4.jpg]]
*Table 4: Experiments on text-to-image.*

### 6.2 消融实验

**初始化策略（Table 5）**：使用单位矩阵 **I** 初始化变换矩阵 **A** 效果最好，因为其对应原始 AR 模型。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_2m9XQq4Dc3_BAR_Refactor_/figures/010_Table_5.jpg]]
*Table 5: Ablation on initialization. Table 6: Ablation on orthogonal projection.*

**正交投影（Table 6）**：软正交投影（δ=0.5）效果最好，硬投影限制了 **A** 的更新方向，无投影则性能显著下降。

**训练目标（Table 7）**：$\mathcal{L}_{\mathrm{BAR}}$ 和 $\mathcal{L}_{\mathrm{residual\ BAR}}$ 均表现良好，残差目标略优。

**离线基 vs 在线可学习基（Table 10）**：在线可学习基（FID 1.63）显著优于离线预计算基（FID 1.80）。

### 6.3 收敛速度与效率

**Figure 7** 显示 BAR-B 的收敛速度显著快于 xAR-B，在整个 400 轮训练过程中始终保持更低的 FID-5K。

**Table 9** 显示 BAR 仅引入额外的矩阵乘法，训练时间和内存开销与原始 xAR 相同（1.00×），残差损失仅增加 0.01× 时间和 0.03× 内存。

### 6.4 可视化分析

**Figure 3** 和 **Figure 8** 展示了学习到的基向量 $a_k$ 的可视化，较暗区域表示较高值。这些基向量呈现出有意义的空间模式，而非随机噪声。

**Figure 4** 和 **Figure 9** 展示了生成过程：每 25 个 token 解码一次，第一列仅使用一个 token。BAR 自然地实现了粗到细的生成特性，早期 token 捕获整体结构，后期 token 填充细节。

**Figure 5** 和 **Figure 10-17** 展示了 ImageNet 256 上的无筛选样本和各类别生成样本，验证了 BAR 的生成质量。

**Figure 6** 和 **Figure 18** 展示了文本到图像生成样本。

### 6.5 额外指标

**Table 11** 和 **Table 12** 提供了 FDDINOv2、KID、CLIP score 和 HPSv2 等额外指标的对比，BAR 在所有指标上均优于或持平于基线方法。

### 6.6 公平性说明

- 所有实验使用与基线（xAR, MAR）完全相同的结构和超参数。
- 使用相同的 VAE 编码器（KL-16）和采样器（ADM 或 Euler-Maruyama）。
- BAR 仅引入额外的矩阵乘法，训练开销可忽略。



## 定位与知识库关联

BAR 在自回归视觉生成方法谱系中占据核心位置：

- **统一框架**：BAR 将 VAR（粗到细尺度预测）、xAR（连续 AR 流匹配）、RAR（随机排列）、PAR（并行解码）、FAR（频域预测）、TiTok（超紧凑 tokenization）和 FractalGen（递归分形 AR）统一为线性变换 **y = Ax** 的特例。

- **与扩散模型的关系**：BAR 在 ImageNet 256×256 上以 FID 1.15 超越了 DiT（2.27）、SiT（2.06）、REPA（1.42）和 LightningDiT（1.35）等扩散模型，证明了自回归范式在视觉生成中的竞争力。

- **局限性**：
  - BAR 主要关注连续 AR 模型，对离散 AR 模型的扩展需要进一步研究。
  - 变换矩阵 **A** 被限制为方阵和正交矩阵，可能不是最优的搜索空间。
  - 残差损失 $\mathcal{L}_{\mathrm{residual\ BAR}}$ 的计算开销略高于标准 BAR 损失。
  - BAR 在 FFHQ 上的学习基可视化显示出不连续模式，可能归因于训练不足。

- **开放问题**：
  - 如何将 BAR 框架扩展到离散 AR 模型（如 VQ-VAE）并实现端到端优化？
  - 非方阵或非正交的变换矩阵 **A** 是否能带来更好的性能？
  - BAR 的学习基是否具有跨数据集的可迁移性？
  - BAR 在更大规模数据集（如 LAION）上的表现如何？
  - BAR 的生成过程是否具有可解释性，能否通过分析基向量理解模型行为？



## 原文 PDF

![[paperPDFs/ICLR_2026/BAR_Refactor_the_Basis_of_Autoregressive_Visual_Generation.pdf]]
