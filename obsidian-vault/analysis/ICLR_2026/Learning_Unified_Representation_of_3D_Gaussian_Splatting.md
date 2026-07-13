---
title: Learning Unified Representation of 3D Gaussian Splatting
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Learning_Unified_Representation_of_3D_Gaussian_Splatting_bb3f48b32ad5.pdf
project_link: "https://instruct-gs2gs.github.io/"
code_link: "https://github.com/cilix-ai/gs-embedding"
aliases:
- SVSFVAE
- LUR3GS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 将每个高斯原语替换为其等概率表面上的子流形场（连续颜色场），该表示被证明是单射且唯一，从而消除嵌入冲突和数值不匹配。
primary_logic: 在保留底层颜色和几何结构的前提下，通过子流形场实现唯一映射和通道同质性，再用 PointNet 变分自编码器在离散点云上学习低维嵌入，并引入基于最优传输的流形距离作为重建目标。
claims:
- 参数表示的非唯一性源于四元数符号歧义、几何对称性和旋转‑球谐相互作用，破坏学习稳定性。
- 子流形场表示提供唯一映射（命题 2），确保一对一的域对应。
- 在 ShapeSplat 和 Mip‑NeRF 360 上，SF‑VAE 的重建质量远超参数量匹配的参数基线。
- 跨域泛化（ShapeSplat→Mip‑NeRF 360）时 SF 嵌入始终优于参数基线。
---

# Learning Unified Representation of 3D Gaussian Splatting

> [!tip] 核心洞察
> 在保留底层颜色和几何结构的前提下，通过子流形场实现唯一映射和通道同质性，再用 PointNet 变分自编码器在离散点云上学习低维嵌入，并引入基于最优传输的流形距离作为重建目标。

| 字段 | 内容 |
|------|------|
| 中文题名 | 学习三维高斯泼溅的统一表示 |
| 英文题名 | Learning Unified Representation of 3D Gaussian Splatting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=NvpVtGG6hk) · [Code](https://github.com/cilix-ai/gs-embedding) · [Project](https://instruct-gs2gs.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | SF‑VAE (Submanifold Field Variational Auto‑encoder) |
| Dataset | ShapeSplat |

> [!tip] 效果简介
> - ShapeSplat (Gaussian Neural Field) 上，PSNR / SSIM / LPIPS 58.619 / 0.980 / 0.043 vs 51.660 / 0.957 / 0.110 (Raw GS Parameter) (+6.959 / +0.023 / −0.067)。

## 概要

### 问题与瓶颈

三维高斯泼溅（3D Gaussian Splatting, 3DGS）以一组显式的高斯基元表示场景，每个基元由位置、四元数旋转、尺度、球谐系数和不透明度等参数 $\pmb \theta = \{ \mu , \mathbf q , \mathbf s , \mathbf c , o \}$ 描述。这种原生参数表示存在两个深层缺陷，使其不适合作为神经网络的学习目标：

1. **非唯一性**：不同的参数组合可以产生完全相同的辐射场——四元数的符号歧义、几何对称性以及旋转与球谐系数的耦合效应，导致多对一的映射关系，破坏学习稳定性。
2. **数值异质性**：各参数分量的量纲、值域和统计分布差异巨大，且整体空间非欧几里得，迫使编码器隐式地拟合互不兼容的数据流形。

这两个问题共同构成了该工作的核心瓶颈：**参数空间的非唯一性与异质性使神经网络难以从中学习稳定、可泛化的表示**。

### 核心思路与因果调控点

本文的因果调控点是**将每个高斯原语从其原生参数空间映射到一个连续的子流形场空间**。具体而言，对每个高斯基元 $\mathcal{G}_i$，在其等概率椭球面 $\mathcal{M}_i$ 上定义一个颜色场 $F_i$，构成表示对 $\mathcal{E}_i = (\mathcal{M}_i, F_i)$。该表示被证明是**单射且唯一**的（命题 2），从根本上消除了参数空间的歧义性，同时将异构的参数统一为通道同质的几何-颜色场。

在此基础上，作者设计了一个**子流形场变分自编码器（SF-VAE）**：以 PointNet 编码器处理从子流形场离散采样得到的彩色点云，解码器通过两个隐式函数（坐标变形网络 $g_c$ 和颜色场网络 $g_f$）重建点云，再经由 PCA 和球谐拟合恢复可渲染的高斯参数。重建目标采用基于最优传输的**流形距离（M-Dist，Wasserstein-2）**，比参数空间的 L1/L2 损失更贴合感知质量。

### 方法定位

SF-VAE 的方法定位可以从以下维度理解：

- **表示层面**：将 3DGS 的显式参数表示替换为几何-颜色耦合的子流形场，属于表示空间的重构，而非对编码器架构的修补。
- **学习范式**：采用变分自编码器框架，在无监督或自监督设定下学习紧凑的隐式嵌入，嵌入维度为 32。
- **知识库定位**：该方法处于 3D 表示学习、神经场与点云处理的交叉点。与直接对参数向量建模的基线（Parametric VAE with MLP/Transformer encoder）相比，SF-VAE 的核心差异在于**输入表示的改变**，而非模型容量的提升——所有比较模型参数量均控制在 0.62M–0.66M 以隔离表示选择的影响。

### 主要结果

在对象级数据集 ShapeSplat 和场景级数据集 Mip-NeRF 360 上，SF-VAE 的重建质量显著优于参数量匹配的参数基线：

- **ShapeSplat**：PSNR 从 51.660 提升至 58.619（+6.959），SSIM 从 0.957 提升至 0.980，LPIPS 从 0.110 降至 0.043（Table 3）。
- **跨域泛化**：在 ShapeSplat → Mip-NeRF 360 的零样本迁移中，SF 嵌入始终优于参数基线（Table 2）。
- **鲁棒性**：SF 嵌入空间对加性噪声更鲁棒，M-Dist 随噪声水平的上升显著平缓于参数空间（Figure 4）。
- **下游应用**：在无监督图聚类任务中，SF 嵌入更好地保留了细粒度语义（Figure 5）；作为高斯神经场的预测目标时，SF 嵌入同样优于原始参数（Table 3）。

消融实验进一步表明，嵌入维度 D=32 达到质量与压缩的最优平衡，仅使用 2% 的训练样本即可接近全量性能，子流形场点云采样数 $P=12^2$（144 点）提供最佳效率-质量权衡。



### 3D 高斯泼溅的参数化困境

三维高斯泼溅（3D Gaussian Splatting, 3DGS）已成为新视角合成与场景重建的主流表示。其核心思想是将场景分解为一组各向异性的三维高斯原语，每个原语由一组参数 $\pmb \theta = \{ \mu , \mathbf q , \mathbf s , \mathbf c , o \}$ 描述，分别对应位置、旋转四元数、尺度、球谐系数和不透明度。这些参数通过

$$\Sigma _ { i } = R ( \mathbf { q } _ { i } ) \operatorname { d i a g } ( \mathbf { s } _ { i } ) ^ { 2 } R ( \mathbf { q } _ { i } ) ^ { \top }$$

构建协方差矩阵以定义局部几何，并通过

$$\mathrm { C o l o r } _ { i } ( \mathbf { d } ) = \left[ \mathrm { S H } _ { i } ^ { r } ( \mathbf { d } ) , \mathrm { S H } _ { i } ^ { g } ( \mathbf { d } ) , \mathrm { S H } _ { i } ^ { b } ( \mathbf { d } ) \right] ^ { \top }$$

计算视角相关的颜色。然而，当尝试将神经网络直接应用于这些参数进行表示学习、压缩或生成时，会遭遇一个根本性障碍：**参数空间的非唯一性与数值异质性**。

### 核心瓶颈：非唯一性与异质性

参数表示 $\pmb \theta$ 存在三重非唯一性来源：

1. **四元数符号歧义**：四元数 $\mathbf q$ 与 $-\mathbf q$ 表示相同的旋转，导致同一几何体对应多个参数组合。
2. **几何对称性**：高斯原语的椭球体具有旋转和反射对称性，不同参数组合可产生相同的体积密度分布。
3. **旋转-球谐相互作用**：旋转矩阵与球谐系数之间的耦合会生成等价的参数组合（见原文 App. A 的证明）。

这些非唯一性意味着参数空间到辐射场的映射是**多对一**的，神经网络在拟合时被迫学习一个模糊的映射关系，严重破坏学习稳定性和泛化能力。

与此同时，参数空间还面临**数值异质性**问题：位置 $\mu$ 的尺度在米级，四元数 $\mathbf q$ 约束在单位球面上，尺度 $\mathbf s$ 可跨越多个数量级，球谐系数 $\mathbf c$ 的分布则依赖于场景光照。这些组件位于完全不同的流形上（如 Figure 1 粉色部分所示），数值范围和分布差异巨大，迫使编码器隐式地去拟合这些异构的数据流形，极大增加了学习难度。

### 现有方法缺口

针对 3DGS 的表示学习，现有工作多直接以原始参数 $\pmb \theta$ 作为神经网络的输入或输出目标，例如使用 MLP 或 Transformer 编码器对拼接的参数向量进行编码。然而，这些方法并未从根本上解决参数空间的非唯一性和异质性问题——它们只是试图让网络“记住”这些模糊映射，而非提供一个良好定义的、唯一的学习空间。因此，模型在重建质量、跨域泛化和噪声鲁棒性方面均表现出明显局限。

### 本文动机

本文的核心洞察是：**在保留底层颜色和几何结构的前提下，通过构造一个唯一且数值同质的中间表示空间，可以从根源上消除参数空间的嵌入冲突**。具体而言，本文提出将每个高斯原语替换为其等概率椭球面上的**子流形场**（Submanifold Field）——一个定义在二维子流形上的连续颜色场。该表示被证明是**单射且唯一**的（Proposition 2），从而确保了一对一的域对应关系，同时将异构的参数组件统一为同质的彩色点云，为后续的神经网络学习提供了数值稳定、语义一致的输入空间（如 Figure 1 紫色部分所示）。



## 核心方法与创新机理

### 瓶颈识别：参数空间的非唯一性与异质性

原始 3DGS 的参数表示 $\pmb \theta = \{ \mu , \mathbf q , \mathbf s , \mathbf c , o \}$ 存在两个根本性缺陷，使其不适用于神经网络学习：

1.  **非唯一性（Many-to-one mapping）**：同一辐射场可对应多组等效参数。来源包括：四元数符号歧义（$\mathbf q$ 与 $-\mathbf q$ 表示相同旋转）、几何对称性（例如旋转对称的高斯体），以及旋转与球谐系数之间的相互作用（见原文 App. A 证明）。这种“一对多”映射破坏了学习目标的一致性。

2.  **数值异质性（Numerical heterogeneity）**：不同参数分量（位置、四元数、尺度、颜色、不透明度）在数值尺度、分布和几何空间上差异巨大。编码器被迫隐式地拟合多个异构的数据流形，导致训练不稳定且泛化能力差。

### 核心因果开关：子流形场表示

为解决上述瓶颈，方法将每个高斯原语 $\mathcal{G}_i$ 从其原始参数空间 **转换** 为一个全新的几何表示——**子流形场（Submanifold Field）** $\mathcal{E}_i = (\mathcal{M}_i, F_i)$。该表示由两个部分构成：

-   **等概率表面 $\mathcal{M}_i$**：在 3D 欧氏空间中选取高斯椭球的一条等概率轮廓面：
    $$\mathcal { M } _ { i } = \left\{ \mathbf { x } \in \mathbb { R } ^ { 3 } \mid ( \mathbf { x } - \pmb { \mu } _ { i } ) ^ { \top } \Sigma _ { i } ^ { - 1 } ( \mathbf { x } - \pmb { \mu } _ { i } ) = r ^ { 2 } \right\}$$

-   **颜色场 $F_i$**：在该表面上定义连续的颜色场，其值为不透明度缩放后的视角相关颜色：
    $$F _ { i } ( \mathbf { x } ) = \sigma ( o _ { i } ) \cdot \mathbf { C o l o r } _ { i } ( \mathbf { d _ { x } } )$$

这一转换带来了两个决定性优势：

-   **可证明的唯一性**：命题 2 证明了子流形场表示是单射的——每个 SGRF $\phi_{\mathcal{G}}$ 对应唯一的 $\mathcal{E}$，从根本上消除了参数空间的映射歧义。
-   **数值同质性**：所有高斯原语被映射到同一类数学对象（定义在 2D 流形上的颜色场），各通道数值处于统一的量纲和分布范围内，使神经网络无需再处理异构数据流形。

### 围绕新表示的系统性方法重构

基于子流形场这一核心表示，整个学习框架进行了四个关键组件的替换：

1.  **编码器架构：MLP/Transformer → PointNet**
    参数基线使用 MLP 或 Transformer 直接编码拼接的参数向量。SF-VAE 将子流形场离散化为彩色点云（默认 $P=12^2=144$ 个采样点），然后采用 **PointNet** 作为编码器 $f$，天然适配点云数据的置换不变性，输出 32 维隐向量 $\mathbf{z}$。

2.  **重建目标：参数空间 L1/L2 → 流形距离 M-Dist**
    参数基线在参数空间使用逐元素损失，与最终渲染质量的感知指标（PSNR, LPIPS）相关性弱。SF-VAE 引入基于最优传输的 **流形距离（M-Dist）**——即输入与重建点云之间的 Wasserstein-2 距离——作为重建损失：
    $$W _ { 2 } ^ { 2 } ( \mathcal { E } , \hat { \mathcal { E } } ) = \operatorname* { i n f } _ { \gamma \in \Gamma ( \hat { \sigma } , \hat { \sigma } ^ { \prime } ) } \int _ { \mathcal { M } \times \hat { \mathcal { M } } } d ^ { 2 } \big ( ( \mathbf { x } , c _ { x } ) , ( \mathbf { y } , c _ { y } ) \big ) d \gamma ( \mathbf { x } , \mathbf { y } )$$
    其中地面距离同时考虑空间坐标与颜色的差异。消融实验证实，M-Dist 与 PSNR、LPIPS 等感知指标的一致性远高于参数空间的 L1/L2 距离。

3.  **解码器与参数恢复：直接输出参数 → 隐式函数 + 后拟合**
    参数基线由 MLP 直接输出参数向量。SF-VAE 的解码器由两个隐式网络组成：坐标变换网络 $g_c$ 和颜色场网络 $g_f$，从隐向量 $\mathbf{z}$ 和单位球采样点重建彩色点云。随后通过 **PCA 估计协方差矩阵 $\Sigma_i$**，并通过 **球谐拟合恢复 SH 系数**，最终得到可渲染的高斯参数。GPU 上的参数拟合模块实现了约 85 倍加速，且质量损失可忽略。

4.  **训练数据策略：领域数据 → 随机生成**
    由于嵌入模型仅在单个高斯原语层级运行，不依赖场景全局语义，因此可以在 **随机生成的高斯原语数据集** 上训练，使模型本身领域无关。这一策略与子流形场的唯一性共同作用，赋予了模型极强的跨域泛化能力。

### 创新总结

| 组件 | 参数基线 | SF-VAE（本文） | 创新本质 |
|------|----------|---------------|----------|
| 表示空间 | 原始参数 $\theta$（非唯一、异构） | 子流形场 $(M,F)$（唯一、同质） | 从源头消除学习歧义 |
| 编码器 | MLP/Transformer | PointNet | 适配点云结构，置换不变 |
| 重建损失 | L1/L2 参数距离 | Wasserstein-2 流形距离 | 与感知质量对齐 |
| 解码恢复 | 直接输出参数 | 隐式函数 + PCA/SH 拟合 | 保持几何一致性 |
| 训练数据 | 领域数据集 | 随机生成 | 实现领域无关的泛化 |



SF‑VAE 的核心设计动机源于一个关键瓶颈：**原始高斯参数表示 θ = {μ, q, s, c, o} 存在非唯一性（四元数符号歧义、几何对称性、旋转‑球谐相互作用）和数值异质性（各组件尺度与分布差异巨大），导致神经网络学习不稳定、泛化差**。为从根本上消除这一瓶颈，SF‑VAE 将表示空间从“参数域”迁移到“子流形场域”，并围绕该新表示构建完整的编码‑解码管线。

### Pipeline 总览

整个框架由五个核心模块串联而成，形成“高斯原语 → 子流形场 → 点云 → 隐向量 → 点云 → 高斯参数”的闭环：

1. **子流形场构建**：对每个高斯原语 G_i，在其等概率椭球面 M_i 上定义连续颜色场 F_i，并均匀采样为彩色点云 P_i，得到统一、唯一且数值同质的表示 E_i。
2. **PointNet 编码器 f**：将点云 P_i 编码为 32 维隐向量 z ∈ R^D。
3. **坐标变换网络 g_c**：以单位球面上的查询点 e_n 和隐向量 z 为输入，输出变形后的新坐标。
4. **颜色场网络 g_f**：以变形坐标和隐向量为输入，预测对应颜色值，二者共同输出重建点云 \hat{P}。
5. **参数拟合模块**：从重建点云通过 PCA 估计协方差矩阵 Σ，并通过球谐拟合恢复 SH 系数，最终得到可渲染的 Gaussian 参数。

### 输入输出流

| 阶段 | 输入 | 输出 | 关键操作 |
|------|------|------|----------|
| 表示转换 | 原始高斯参数 θ_i | 子流形场点云 P_i ⊂ M_i × R^3 | 等概率面采样 + 颜色场求值 |
| 编码 | 点云 P_i | 隐向量 z | PointNet 编码 |
| 解码 | z + 单位球采样点 e_n | 重建点云 \hat{P} | g_c 变形 + g_f 着色 |
| 参数恢复 | \hat{P} | 可渲染参数 \hat{θ}_i | PCA 估计 Σ + SH 拟合 c |

### 训练目标

SF‑VAE 的损失函数结合了两项：

$$
\mathcal{L}_{\mathrm{VAE}} = \mathbb{E}_{\hat{\mathcal{P}} \sim \mathrm{VAE}(\mathcal{P})} \left( \hat{W}_2^2(\mathcal{P}, \hat{\mathcal{P}}) + \beta \cdot d_{\mathrm{KL}}\left( f(\mathbf{z} \mid \mathcal{P}) \lVert \mathcal{N}(0, \mathbf{I}) \right) \right)
$$

其中 **流形距离（M‑Dist）** \hat{W}_2^2 是输入点云与重建点云之间的 Wasserstein‑2 距离，其地面距离同时考虑空间坐标与颜色差异：

$$
d^2\big((\mathbf{x}, c_x), (\mathbf{y}, c_y)\big) = \|\mathbf{x} - \mathbf{y}\|_2^2 + \lambda \|c_x - c_y\|_2^2
$$

这一设计的因果逻辑是：**M‑Dist 在子流形场空间中度量几何与颜色的联合差异，比参数空间的 L1/L2 距离更符合感知质量指标（PSNR、LPIPS）**（消融实验已验证）。

### 关键设计决策

- **单原语层级训练**：编码器仅处理单个高斯原语，训练数据采用随机生成的高斯原语数据集，使模型本身领域无关，从而天然支持跨域泛化（ShapeSplat ↔ Mip‑NeRF 360）。
- **公平性控制**：所有比较模型具有相近的参数量（约 0.62M–0.66M），采用相同的自实现编码器‑解码器框架，仅输入表示不同，以隔离表示选择的影响。
- **效率优化**：子流形场点云采样数 P = 12²（144 点）提供最佳效率‑质量权衡；GPU 上的参数拟合模块实现约 85 倍加速，质量损失可忽略。

### 补充图表

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_NvpVtGG6hk/figures/001_Figure_1.jpg]]
*Figure 1: A scene of N Gaussian primitives can be represented by N sets of parameters θ (shown in pink). Data in this parametric space resides on different manifolds and is heterogeneous and non-Euclidean, introducing challenges for encoders to fit disparate data manifolds implicitly. Shown in purple is the proposed representation, instead of relying on Gaussian parameterization, we introduce a canonical submanifold field space (M, F ) that uniquely represents a Gaussian primitive with an iso-probability surface*

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_NvpVtGG6hk/figures/002_Figure_2.jpg]]
*Figure 2: To embed the proposed submanifold field representation into a vector form suitable for neural networks, we devise a Submanifold Field Variational Auto-encoder (SF-VAE) that embeds any input submanifold field as a 32-D vector, then reconstructs the original parameter set*



### 3.1 原始参数空间的非唯一性问题

3DGS 将场景表示为 $N$ 个高斯原语，每个原语的原始参数集为：

$$
\pmb \theta = \{ \mu , \mathbf q , \mathbf s , \mathbf c , o \}
$$

其中 $\mu \in \mathbb{R}^3$ 为位置，$\mathbf{q} \in \mathbb{R}^4$ 为旋转四元数，$\mathbf{s} \in \mathbb{R}^3$ 为尺度，$\mathbf{c}$ 为球谐系数，$o \in \mathbb{R}$ 为不透明度。协方差矩阵由旋转和尺度构造：

$$
\Sigma _ { i } = R ( \mathbf { q } _ { i } ) \operatorname { d i a g } ( \mathbf { s } _ { i } ) ^ { 2 } R ( \mathbf { q } _ { i } ) ^ { \top }
$$

方向相关颜色通过球谐函数计算：

$$
\mathrm { C o l o r } _ { i } ( \mathbf { d } ) = \left[ \mathrm { S H } _ { i } ^ { r } ( \mathbf { d } ) , \mathrm { S H } _ { i } ^ { g } ( \mathbf { d } ) , \mathrm { S H } _ { i } ^ { b } ( \mathbf { d } ) \right] ^ { \top }
$$

**瓶颈分析**：该参数表示存在根本性的非唯一性——多个不同的参数组合可产生完全相同的辐射场。具体来源包括：(1) 四元数符号歧义（$\mathbf{q}$ 与 $-\mathbf{q}$ 对应相同旋转）；(2) 几何对称性（如球体对旋转不变）；(3) 旋转与球谐系数的耦合效应（见附录 A 证明）。此外，各参数分量的数值尺度与分布差异巨大（位置在厘米级、四元数在单位范数、球谐系数可正可负），形成异构、非欧几里得的表示空间。这种“多对一映射”与数值异质性直接破坏神经网络的学习稳定性。

### 3.2 子流形场构造模块

为解决上述瓶颈，方法将每个高斯原语 $\mathcal{G}_i$ 转换为其等概率椭球面上的连续颜色场。

**等概率面定义**：取马氏距离为常数 $r$ 的椭球面作为子流形 $\mathcal{M}_i$：

$$
\mathcal { M } _ { i } = \left\{ \mathbf { x } \in \mathbb { R } ^ { 3 } \mid ( \mathbf { x } - \pmb { \mu } _ { i } ) ^ { \top } \Sigma _ { i } ^ { - 1 } ( \mathbf { x } - \pmb { \mu } _ { i } ) = r ^ { 2 } \right\}
$$

**场函数定义**：在子流形上每点 $\mathbf{x}$ 定义不透明度缩放的视相关颜色：

$$
F _ { i } ( \mathbf { x } ) = \sigma ( o _ { i } ) \cdot \mathbf { C o l o r } _ { i } ( \mathbf { d _ { x } } )
$$

其中 $\sigma(\cdot)$ 为 sigmoid 激活，$\mathbf{d_x}$ 为从 $\mu_i$ 指向 $\mathbf{x}$ 的方向向量。整个表示空间为所有子流形-场对的集合：

$$
\boldsymbol { \mathcal { E } } = \{ \boldsymbol { \mathcal { E } } _ { i } = ( \boldsymbol { \mathcal { M } } _ { i } , \boldsymbol { F } _ { i } ) \mid \boldsymbol { \mathcal { M } } _ { i } \in \mathbb { M } , \boldsymbol { F } _ { i } : \boldsymbol { \mathcal { M } } _ { i } \rightarrow \mathbb { R } ^ { 3 } \}
$$

**核心洞察**：该表示被证明是单射且唯一的（命题 2），即每个子流形场 $\mathcal{E}_i$ 对应唯一的底层高斯原语，从根本上消除了参数空间的“多对一”映射问题。同时，子流形场将异构的参数分量统一为空间坐标与颜色值的同质数值域，为神经网络提供了稳定的学习基础。

### 3.3 SF-VAE 编码器-解码器架构

为将连续的子流形场嵌入为适合神经网络的向量形式，设计变分自编码器 SF-VAE（图 2 示意）。

**离散化与编码**：将子流形场均匀采样为 $P$ 个带颜色的空间点，形成彩色点云 $\mathcal{P}$。采用 **PointNet 编码器** $f$ 将其映射为 $D=32$ 维隐向量 $\mathbf{z}$。PointNet 的置换不变性天然适合处理无序点云。

**解码器**：由两个隐式神经网络组成，以隐向量 $\mathbf{z}$ 和单位球面上采样的查询点 $\mathbf{e}_n$ 为输入：

- **坐标变换网络** $g_c: \mathbb{R}^3 \times \mathbb{R}^D \rightarrow \mathbb{R}^3$：将单位球面点变形为重建点云的空间坐标；
- **颜色场网络** $g_f: \mathbb{R}^3 \times \mathbb{R}^D \rightarrow \mathbb{R}^3$：在变形坐标处预测 RGB 颜色。

解码器输出为重建的彩色点云：

$$
\hat { \mathcal { P } } = g ( \mathbf { z } , \mathcal { U } _ { P ^ { \prime } } ) = \{ g _ { c } ( [ \mathbf { e } _ { n } , \mathbf { z } ] ) , g _ { f } ( [ g _ { c } ( [ \mathbf { e } _ { n } , \mathbf { z } ] ) , \mathbf { z } ] ) \} _ { n = 1 } ^ { P ^ { \prime } }
$$

**参数拟合模块**：从解码点云通过 PCA 估计协方差矩阵 $\Sigma_i$，再通过球谐拟合恢复 SH 系数 $\mathbf{c}_i$，最终得到可渲染的完整高斯参数。该模块在 GPU 上实现约 85 倍加速，且质量损失可忽略。

### 3.4 流形距离损失（M-Dist）

为度量输入子流形场 $\mathcal{E}$ 与重建 $\hat{\mathcal{E}}$ 之间的差异，引入基于最优传输的 Wasserstein-2 距离：

$$
W _ { 2 } ^ { 2 } ( \mathcal { E } , \hat { \mathcal { E } } ) = \operatorname* { i n f } _ { \gamma \in \Gamma ( \hat { \sigma } , \hat { \sigma } ^ { \prime } ) } \int _ { \mathcal { M } \times \hat { \mathcal { M } } } d ^ { 2 } \big ( ( \mathbf { x } , c _ { x } ) , ( \mathbf { y } , c _ { y } ) \big ) d \gamma ( \mathbf { x } , \mathbf { y } )
$$

其中地面距离同时考虑空间与颜色误差：

$$
d ^ { 2 } \big ( ( \mathbf { x } , c _ { x } ) , ( \mathbf { y } , c _ { y } ) \big ) = \| \mathbf { x } - \mathbf { y } \| _ { 2 } ^ { 2 } + \lambda \| c _ { x } - c _ { y } \| _ { 2 } ^ { 2 }
$$

实际计算时使用离散点云的经验 Wasserstein 距离 $\hat{W}_2^2$。VAE 的总体训练损失为：

$$
\mathcal { L } _ { \mathrm { V A E } } = \mathbb { E } _ { \hat { \mathcal { P } } \sim \mathrm { V A E } ( \mathcal { P } ) } \left( \hat { W } _ { 2 } ^ { 2 } ( \mathcal { P } , \hat { \mathcal { P } } ) + \beta \cdot d _ { \mathrm { K L } } \left( f ( \mathbf { z } \mid \mathcal { P } ) \lVert \mathcal { N } ( 0 , \mathbf { I } ) \right) \right)
$$

**消融证据**：M-Dist 相比参数空间的 L1/L2 距离，与感知质量指标（PSNR、LPIPS）的对齐程度更高，验证了在子流形场空间而非参数空间定义重建目标的必要性。

### 3.5 关键设计选择

- **采样点数** $P=12^2=144$：消融表明超过此值提升极小，该设置在效率与质量间取得最优平衡。
- **嵌入维度** $D=32$：维度行为研究表明 32 维是重建质量与压缩率之间的最优折中点。
- **训练数据**：模型在随机生成的高斯原语数据集上训练，使其天然具有领域无关性，仅需 2% 的训练样本即可接近全量性能。



## 实验与关键发现

### 核心实验设置

为隔离表示选择的影响，所有比较模型均采用相同的自实现编码器‑解码器框架，参数量控制在 0.62M–0.66M 的狭窄区间。SF‑VAE 的嵌入模型仅编码单个高斯原语，因此训练数据采用**随机生成的高斯原语数据集**，使模型本身领域无关，避免对特定场景分布的过拟合。测试则在对象级数据集 **ShapeSplat**（高斯神经场）和场景级数据集 **Mip‑NeRF 360** 上进行，以评估表示在两类典型下游任务中的重建保真度。

### 主结果：重建质量对比

Table 1 报告了在随机生成数据上训练后，各模型在 ShapeSplat 和 Mip‑NeRF 360 上的重建质量。SF‑VAE 在两个数据集上均取得**大幅领先**：在 ShapeSplat 上，PSNR 达到 63.408，相比参数基线（MLP 编码器）的 56.449 提升约 6.96 dB；LPIPS 从 0.110 降至 0.043，感知质量提升显著。在 Mip‑NeRF 360 上，SF‑VAE 的 PSNR 为 29.833，而参数基线仅 25.834，差距约 4 dB。值得注意的是，参数空间中的 Transformer 编码器在场景级数据上表现反而不及 MLP 编码器，暗示更强的序列建模能力在异构参数空间中无法有效发挥——这与论文对参数空间非唯一性与数值异质性的诊断一致。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_NvpVtGG6hk/figures/003_Table_1.jpg]]
*Table 1: Reconstruction quality comparison for object-level (ShapeSplat) and scene-level (Mip-NeRF 360) datasets. All models trained on the randomly generated dataset. The three models have a parameter count of 0.62M, 0.66M and 0.62M respectively. The relatively extreme perceptual metrics values in ShapeSplat come from the use of background during measurement*

**Table 1** 展示了对象级和场景级数据集上的重建质量对比。所有模型均在随机生成数据集上训练，参数量分别为 0.62M、0.66M 和 0.62M。

定性结果（Figure 3）进一步印证了这一趋势：参数模型在嵌入和恢复过程中产生混淆，导致重建的高斯原语出现位置偏移、形状畸变和颜色失真；而 SF‑VAE 的重建结果在视觉上与原场景高度一致。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_NvpVtGG6hk/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative results for rasterized reconstruction. Samples selected arbitrarily from Mip-NeRF 360 and ShapeSplat. Parametric models can induce confusion in parameter space, failing to embed and restore the correct Gaussian parameters*

### 跨域泛化

Table 2 报告了跨域泛化实验：模型在 ShapeSplat 上训练后在 Mip‑NeRF 360 上测试（反之亦然）。SF 嵌入在所有跨域设置下**始终优于参数基线**，且性能下降幅度远小于参数模型。这表明子流形场表示所捕获的几何与颜色结构具有内在的领域无关性，即使不使用随机生成数据，其泛化能力也显著强于直接在原始参数上学习的表示。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_NvpVtGG6hk/figures/004_Table_2.jpg]]
*Table 2: Reconstruction quality comparison under cross-domain setting. All models trained on either ShapeSplat or Mip-NeRF 360 dataset are tested on another dataset. We show that the generalization ability of SF Embedding framework is inherently domain-agnostic even without random data*

**Table 2** 展示了跨域设置下的重建质量对比。模型在 ShapeSplat 或 Mip‑NeRF 360 上训练后在另一个数据集上测试。

### 下游应用：高斯神经场

Table 3 将 SF 嵌入作为高斯神经场（GNF）的预测目标，与直接预测原始 GS 参数进行对比。在 ShapeSplat 上，SF 嵌入训练的 GNF 达到 **PSNR 58.619 / SSIM 0.980 / LPIPS 0.043**，远超参数预测的 51.660 / 0.957 / 0.110。在 Mip‑NeRF 360 上同样保持明显优势。这验证了子流形场表示不仅适合自编码重建，也能作为条件生成任务的有效学习目标。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_NvpVtGG6hk/figures/008_Table_3.jpg]]
*Table 3: Comparison between Gaussian Neural Fields trained using submanifold field embeddings and raw Gaussian parameters. Top: ShapeSplat, bottom: Mip-NeRF 360*

**Table 3** 比较了使用子流形场嵌入与原始高斯参数训练的高斯神经场在 ShapeSplat（上）和 Mip‑NeRF 360（下）上的结果。

### 鲁棒性分析

Figure 4 展示了嵌入空间的噪声鲁棒性。向嵌入向量注入不同强度的高斯噪声后，SF‑VAE 从加噪嵌入重建的场景质量明显优于参数基线。定量上，SF‑VAE 的流形距离（M‑Dist）随噪声水平上升的增幅更为平缓，表明其嵌入空间具有更好的**几何连续性和抗扰动能力**。这一性质对于将嵌入用于生成模型或压缩传输等场景至关重要。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_NvpVtGG6hk/figures/006_Figure_4.jpg]]
*Figure 4: Reconstruction results using embeddings with noise. Left: Visualization of reconstructed scene from noisy embeddings of Gaussian parameters (MLP) and SF-VAE. Right: Comparison on M-Dist for different noise levels added to embedding space, tested on Mip-NeRF 360. Noise level is defined as the ratio between the noise magnitude and the embedding variance*

### 消融研究

Figure 7 系统考察了三个关键设计选择（均在 Mip‑NeRF 360 上测试）：

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_NvpVtGG6hk/figures/009_Figure_7.jpg]]
*Figure 7: Behavior studies tested on Mip-NeRF 360. From left to right: (a) embedding dimension, (b) generated training dataset size, (c) Submanifold Field discretized (i.e., point sample) grid size*

- **嵌入维度**（Figure 7a）：维度从 8 增至 128，PSNR 在 D=32 处达到拐点，之后提升趋于饱和。32 维被确定为重建质量与压缩效率的最优平衡点。
- **训练集规模**（Figure 7b）：仅使用随机训练集的 **2%** 即可达到接近全集的性能，说明子流形场表示本身具有高样本效率，模型无需海量数据即可学到有效的嵌入映射。
- **子流形场采样密度**（Figure 7c）：点云采样数 P=12²（144 点）提供最佳效率‑质量权衡；超过此密度提升极小，因此论文固定使用 12² 的网格采样。

此外，论文验证了所提出的 **M‑Dist（Wasserstein‑2 距离）** 相比参数空间的 L1/L2 距离，与感知质量指标（PSNR、LPIPS）的排序一致性更高，从而为 VAE 训练提供了更合理的重建目标。在工程实现上，GPU 上的参数拟合模块（PCA + SH 拟合）实现了约 **85 倍加速**，且质量损失可忽略。

### 无监督聚类

Figure 5 展示了基于嵌入的无监督图聚类结果。相比原始高斯参数和参数 VAE 嵌入，SF 嵌入能更好地保留细粒度语义结构，聚类结果中相同语义部件（如椅腿、椅背）被更清晰地归为一组，表明学习到的表示在下游分析任务中具有实用价值。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_NvpVtGG6hk/figures/007_Figure_5.jpg]]
*Figure 5: Unsupervised graph clustering based on raw Gaussian parameters and various embeddings. Submanifold field embeddings show better preservation of detailed semantics, showing its downstream applicability*

### 失败模式与局限

尽管 SF‑VAE 在单原语层级取得了显著优势，其设计存在两个值得关注的局限：

1. **忽略原语间结构关系**：当前方法在单个高斯原语层级独立运行，未显式建模原语间的空间或结构交互。对于具有强全局依赖性的场景（如稠密室内空间、长程反射），这一简化可能限制嵌入的表达能力。论文未提供此类场景的测试结果。
2. **扩展性待验证**：虽然展示了跨域泛化，但所有实验均在静态场景上进行。在动态场景、非刚性形变或大规模城市场景下的表现尚未被检验，子流形场表示在这些设定下的鲁棒性和计算开销仍是开放问题。

> **手动验证提示**：论文未提供与基于 NeRF 的隐式表示压缩方法（如 VQ‑VAE 系列）的直接对比。若需定位该方法在更广泛表示学习谱系中的相对优势，建议补充相关基线。



## 定位与知识库关联

### 核心问题定位：参数空间的表示非唯一性与数值异质性

本工作将三维高斯泼溅（3DGS）的嵌入学习问题重新定义为**表示空间的选择问题**，而非单纯的网络架构设计问题。其出发点是识别并形式化地刻画原始高斯参数表示 $\pmb \theta = \{ \mu , \mathbf q , \mathbf s , \mathbf c , o \}$ 在神经网络学习中的两个根本性缺陷：

1.  **表示非唯一性**：多个不同的参数组合可以对应完全相同的辐射场输出。这源于四元数符号歧义（$\mathbf q$ 和 $-\mathbf q$ 对应相同旋转）、几何对称性（尺度轴的排列等价性）以及旋转与球谐系数之间的相互作用。这种多对一映射直接违反了神经网络学习对输入-输出映射一致性的基本要求，导致优化过程中的混淆和不稳定。
2.  **数值异质性**：参数向量的不同分量（位置 $\mu$、四元数 $\mathbf q$、尺度 $\mathbf s$、球谐系数 $\mathbf c$、不透明度 $o$）在数值尺度、分布范围和底层几何结构上差异巨大，且驻留在不同的流形上（如 $\mathbf q$ 位于单位球面 $S^3$ 上）。直接将这些异构、非欧几里得的数据拼接输入编码器，迫使网络隐式地拟合多个不相干的数据流形，显著增加了学习难度。

这一诊断构成了全文方法设计的因果杠杆：通过将表示空间从异构的参数空间迁移到同质且唯一的子流形场空间，从根本上消除上述学习障碍。

### 方法谱系中的位置：表示驱动的嵌入学习

在 3DGS 的压缩与生成研究谱系中，本工作占据了一个独特的位置——**以表示空间设计为核心驱动力的嵌入学习方法**。与现有工作的关系可沿以下维度展开：

**与直接参数压缩方法的对比**：现有工作多采用“编码器-解码器”框架直接对原始高斯参数 $\theta$ 进行压缩，编码器通常为 MLP 或 Transformer，解码器直接输出参数向量。这类方法将学习困难归因于网络容量或架构选择，试图通过更强的模型来隐式克服参数空间的缺陷。本工作的核心洞察在于：**瓶颈不在网络架构，而在表示本身**。实验通过严格控制参数量（所有比较模型约 0.62M–0.66M），在相同的自实现编码器-解码器框架下，仅将输入表示从原始参数替换为子流形场，就实现了重建质量的显著跃升（ShapeSplat 上 PSNR 从 51.660 提升至 58.619），有力地证明了表示选择的主导作用。

**与 NeRF 相关嵌入方法的关联**：在神经辐射场领域，已有工作探索将场景嵌入到低维隐空间以支持生成或编辑任务。本工作将这一思路迁移到 3DGS 域，但面临 3DGS 特有的挑战——其基本单元是离散的高斯原语集合，而非连续的体积场。所提出的子流形场表示可视为一种“原语级”的连续化策略：将每个离散高斯原语展开为其等概率椭球面上的连续颜色场，从而使得原本离散、异构的参数集合获得了连续、同质的表示形式，为后续的 PointNet 编码和 VAE 学习铺平了道路。

**与点云表示学习的关系**：子流形场经过均匀采样后转化为彩色点云，这使得本工作能够借鉴点云深度学习（如 PointNet）的成熟架构。但关键区别在于，这里的“点云”并非任意采样的表面点，而是从高斯的等概率子流形上结构化采样的点，携带着精确的几何与颜色信息，且被证明具有唯一性（命题 2）。这种结构化采样使得点云表示与原始高斯参数之间存在可逆的双射关系，而非一般的近似重建。

### 适用边界与局限性

本方法的设计选择也划定了其适用边界：

**原语级独立编码的局限**：SF-VAE 在单个高斯原语层级运行，将每个原语独立地映射为 32-D 嵌入向量。这种设计保证了数据不变性（不受原语排列影响），但**显式地省略了原语间的空间/结构关系建模**。在需要捕捉原语间强全局依赖性的任务中（如稠密室内场景中的物体间遮挡关系、长程反射或光照一致性），这种独立编码可能成为性能瓶颈。论文自身也指出这一点，并将其列为开放问题。

**静态场景假设下的验证范围**：当前实验验证集中在 ShapeSplat（物体级）和 Mip-NeRF 360（场景级）两个静态数据集上。虽然跨域泛化实验（Table 2）展示了领域无关的嵌入能力，但**未涉及动态场景、非刚性形变或大规模城市场景**的测试。在这些场景下，高斯原语的数量和分布可能发生剧烈变化，单个原语嵌入的独立性和可扩展性尚待验证。

**参数拟合步骤的依赖**：SF-VAE 的解码器输出是彩色点云，需通过 PCA 估计协方差矩阵 $\Sigma$ 并通过球谐拟合恢复 SH 系数，才能得到可渲染的 Gaussian 参数。这一后处理步骤虽然在 GPU 上实现了约 85 倍加速，但仍引入了额外的计算开销和潜在的拟合误差，使得整个流程并非完全端到端可微。在需要梯度回传至原始渲染管线的应用中，这一断裂可能带来不便。

### 开放问题与未来方向

基于上述分析，本工作开启了若干值得深入探索的方向：

1.  **原语间关系建模的融合**：如何在保持 SF 嵌入唯一性优势的前提下，引入原语间的交互建模？可能的路径包括在图神经网络中聚合邻域嵌入，或在 VAE 的隐空间中引入结构先验。论文提出的无监督图聚类实验（Figure 5）已初步展示了 SF 嵌入在下游任务中的语义保持能力，暗示了进一步结构化建模的潜力。

2.  **与场景级压缩/生成框架的整合**：所学习的 32-D 嵌入是否可作为现有场景级压缩或生成框架的即插即用组件？例如，将场景表示为嵌入向量的集合而非原始参数集合，可能提升现有方法的压缩率和生成质量。这一方向需要验证嵌入空间的可插值性和平滑性是否满足生成模型的需求。

3.  **子流形场表示的可扩展性**：当前的子流形场定义依赖于高斯的等概率椭球面，这天然适用于各向异性的高斯原语。但对于非各向同性的材质模型、参与物理仿真的介质，或需要更高阶几何描述的表示，子流形场框架是否可扩展？这涉及对“子流形”定义的泛化以及相应唯一性保证的重新证明。

4.  **噪声鲁棒性的深层机理**：Figure 4 显示 SF 嵌入对加性噪声更鲁棒，嵌入空间的 M-Dist 随噪声增大的上升更平缓。这一现象的深层原因——是子流形场的几何正则性，还是 M-Dist 作为重建目标的平滑效应——值得进一步的理论分析，可能为鲁棒表示学习提供更一般的设计原则。



## 原文 PDF

![[paperPDFs/ICLR_2026/Learning_Unified_Representation_of_3D_Gaussian_Splatting_bb3f48b32ad5.pdf]]
