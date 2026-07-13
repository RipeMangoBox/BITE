---
title: "LION: Latent Point Diffusion Models for 3D Shape Generation"
type: paper
paper_level: A
venue: NeurIPS
year: 2022
pdf_ref: paperPDFs/NEURIPS_2022/LION_Latent_Point_Diffusion_Models_for_3D_Shape_Generation.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/LION/
aliases:
- LLPDM
- LION
tags:
- NEURIPS_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "构建具有点结构隐变量和全局形状隐变量的分层变分自编码器（VAE），将点云压缩到平滑、正则化的隐空间，再在隐空间中训练两个分层去噪扩散模型，从而利用隐空间的平滑性简化扩散建模，同时保留点结构以发挥点云处理架构的优势。"
primary_logic: "利用VAE正则化隐空间降低扩散模型训练难度，同时保持点云结构的隐表示，兼顾了通过编码器微调的任务灵活性、高质量生成和自然的形状解耦。"
claims:
- "LION在ShapeNet基线的1-NNA指标上显著优于直接对点云建模的扩散基线PVD和DPM，且在不同归一化及数据集划分下均达到了SOTA。"
- "消融实验证实，同时使用全局形状隐变量和点结构隐变量的完全分层架构，其生成质量（1-NNA）显著优于仅使用单一隐变量的消融变体。"
- "ShapeNet (PointFlow split, global normalization) - Airplane 上 1-NNA CD↓ = 67.41"
- "ShapeNet (PointFlow split, global normalization) - Chair 上 1-NNA CD↓ = 53.70"
---

# LION: Latent Point Diffusion Models for 3D Shape Generation

> [!tip] 核心洞察
> 利用VAE正则化隐空间降低扩散模型训练难度，同时保持点云结构的隐表示，兼顾了通过编码器微调的任务灵活性、高质量生成和自然的形状解耦。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | LION：面向三维形状生成的隐点扩散模型 |
| 英文题名 | LION: Latent Point Diffusion Models for 3D Shape Generation |
| 会议/期刊 | NeurIPS 2022 |
| Links | [paper](https://arxiv.org/abs/2210.06978) · [Project](https://nv-tlabs.github.io/LION) · [Project](https://research.nvidia.com/labs/toronto-ai/LION/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | LION (Latent Point Diffusion Model) |
| Dataset | ShapeNet (PointFlow split, global normalization) - Airplane, global normalization) - Chair, global normalization) - Car, ShapeNet-vol 13 classes (unconditional) |

> [!tip] 效果简介
> - ShapeNet (PointFlow split, global normalization) - Airplane 上，1-NNA CD↓ 为 67.41，对比 73.82 (PVD)，变化 -6.41。
> - ShapeNet (PointFlow split, global normalization) - Chair 上，1-NNA CD↓ 为 53.70，对比 56.26 (PVD)，变化 -2.56。
> - ShapeNet (PointFlow split, global normalization) - Car 上，1-NNA CD↓ 为 51.14，对比 54.55 (PVD)，变化 -3.41。

## 概要

**核心问题**：直接在复杂高维的点云坐标上训练扩散模型面临根本性困难——点云的非结构化特性与高维空间使得单一扩散模型难以在生成质量、样本多样性以及灵活的任务适配之间取得平衡。

**核心方法**：LION（Latent Point Diffusion Model）提出了一种**分层隐空间扩散**范式。其核心思路是构建一个具有两层隐变量的变分自编码器（VAE）——全局形状隐变量 $\mathbf{z}_0$ 捕捉整体几何，点结构化隐变量 $\mathbf{h}_0$ 保留局部细节——将点云压缩到一个平滑、正则化的隐空间中。随后，在该隐空间内训练两个分层去噪扩散模型（DDM），分别对 $\mathbf{z}_0$ 和条件于 $\mathbf{z}_0$ 的 $\mathbf{h}_0$ 进行扩散建模。这一设计的关键在于：**利用VAE的KL正则化降低扩散模型的训练难度，同时保持点结构的隐表示，从而兼顾了扩散模型的高质量生成能力、点云处理架构（PVCNN）的表达优势，以及通过编码器微调实现的多任务灵活性**（如体素引导合成、单视图重建等）。

**方法定位**：LION处于三维生成模型中“隐空间扩散”与“点云原生处理”的交汇点。相较于直接在点云坐标上扩散的**PVD**和**DPM**，LION将扩散过程从高维坐标空间迁移至低维平滑隐空间，显著降低了建模难度；相较于**PointFlow**（Yang et al., ICCV 2019）等基于规范化流的模型，LION借助扩散模型的强生成能力取得了更优的保真度。

**主要结果**：
- 在ShapeNet的多个基准（PointFlow划分、全局/单独归一化）上，LION在**1-NNA**指标上显著优于PVD和DPM等直接点云扩散基线。例如，在全局归一化的飞机类别上，LION的1-NNA CD↓达到67.41，而PVD为73.82（Table 1）；在ShapeNet-vol 13类无条件生成任务上，LION的1-NNA CD↓为51.85，PVD为58.65（Table 4）。
- 消融实验证实，同时使用全局形状隐变量和点结构隐变量的完全分层架构，其生成质量显著优于仅使用单一隐变量的变体（Table 11），验证了分层设计的必要性。
- LION展示了丰富的应用能力，包括体素引导合成、隐空间形状插值、单视图重建，以及通过SAP（Shape As Points）模块从生成点云中提取高质量网格。

**局限与待验证点**：LION的标准DDPM采样速度较慢（约27秒/形状），虽可通过DDIM加速至1秒以内，但步数过少（如5步）会导致生成质量急剧下降（Table 25）。此外，模型目前仅处理无纹理几何，且未扩展到完整场景合成。在大规模跨类别真实数据集上的泛化能力尚待验证。



三维形状生成是计算机视觉与图形学领域的核心问题之一，其目标是从无到有地合成结构合理、细节丰富且多样化的三维形体。近年来，以点云为表示媒介的生成方法因其直接性和灵活性而受到广泛关注。点云无需预设拓扑结构，能够自然表达任意复杂度的几何表面，且与主流三维传感器获取的数据形式高度一致。

然而，直接在原始点云坐标空间进行生成式建模面临根本性困难。点云数据本身具有高维度、无序性和不规则采样的特点，其分布高度复杂且非平滑。早期基于似然的方法，如 **PointFlow**（Yang et al., ICCV 2019），采用连续规范化流（continuous normalizing flows）对点云分布进行建模，但受限于流模型本身的容量与训练难度，生成质量与多样性难以兼顾。

扩散模型（Diffusion Probabilistic Models, DDMs）的出现为高维数据生成带来了新的范式。DDM通过定义马尔可夫前向加噪过程，将数据逐步破坏为高斯噪声，再学习一个参数化的逆向去噪过程来重建原始数据。其训练目标本质上等价于去噪得分匹配（denoising score matching），具有稳定的训练动态和良好的模式覆盖能力。在三维点云生成领域，**PVD**（Point-Voxel Diffusion）和 **DPM**（Diffusion Probabilistic Models for 3D Point Cloud Generation）率先将扩散模型直接应用于点云坐标空间，取得了当时最优的生成性能。

尽管如此，直接在点云坐标空间运行扩散模型仍然是一个次优选择。问题的瓶颈在于：**点云空间的高维复杂结构使得扩散模型需要在极为崎岖的数据流形上学习去噪映射，这显著增加了训练难度，并限制了模型在生成质量、多样性以及灵活任务适配（如条件生成、形状编辑）之间的权衡空间。** 具体而言，单一扩散模型难以同时满足以下三个要求：（1）生成高保真度的精细几何；（2）覆盖数据分布的完整多样性；（3）通过编码器微调等方式灵活融入外部条件信号。

这一瓶颈的因果调控旋钮在于**建模空间的选择**。如果将扩散过程从原始点云坐标空间迁移到一个经过正则化、更为平滑的隐空间（latent space），则有望大幅降低扩散建模的难度。然而，简单的隐空间压缩（如将点云编码为单一全局向量）会丢失点云固有的结构信息，从而牺牲利用点云处理架构（如PointNet++、PVCNN）进行局部几何建模的优势。

LION正是在这一背景下被提出。其核心洞察是：**构建一个分层变分自编码器（Hierarchical VAE），将点云同时压缩为全局形状隐变量和保持点结构的隐点（latent points）表示，从而在平滑的隐空间中训练两个分层去噪扩散模型。** 这种设计同时利用VAE隐空间的正则化效果来简化扩散建模，又保留了点结构表示以发挥点云处理架构的优势，进而在高质量生成、自然形状解耦与任务灵活性之间取得更好的平衡。



## 核心方法与创新机理

LION 的核心创新在于将**分层变分自编码器（VAE）与隐空间去噪扩散模型（DDM）**相结合，从而将3D形状生成的难度从复杂高维的点云坐标空间转移到一个平滑、正则化的隐空间中。这一设计直接回应了核心瓶颈：在原始点云上直接训练扩散模型（如 **PVD** 和 **DPM**）难以在单一模型中同时保证生成质量、多样性与灵活的任务适配。

### 关键设计变更（Changed Slots）

相对直接在点云坐标空间进行加噪与去噪的基线（如 PVD），LION 在两个关键维度上做出了根本性改变：

1.  **扩散建模空间**：从在**原始点云坐标空间**直接进行扩散，转变为在一个**层次化 VAE 的隐空间**中进行扩散建模。该隐空间包含两个层次：
    *   **全局形状隐变量 $z_0$**：捕捉物体的整体形状信息。
    *   **点结构化隐变量 $h_0$**：保留了点云的结构特性，可视为输入点云的平滑版本，从而能发挥点云处理架构（如 PVCNN）的优势。
    这一改变的证据锚定于 **Section 3** 及 **Figure 1** 的模型架构总览。

2.  **生成过程**：从通过**单个扩散模型**在点云空间逐步去噪，转变为**层级式条件采样**：
    1.  首先，从形状隐变量的扩散模型 $p_\theta(z_0)$ 中采样全局形状 $z_0$。
    2.  然后，以 $z_0$ 为条件，从隐点扩散模型 $p_\psi(h_0|z_0)$ 中采样点结构化隐变量 $h_0$。
    3.  最后，通过解码器 $p_\xi(x|h_0, z_0)$ 将两者解码为最终的点云。
    这一生成过程由公式 $p_{\xi,\psi,\theta}(x, h_0, z_0) = p_{\xi}(x|h_0, z_0) p_{\psi}(h_0|z_0) p_{\theta}(z_0)$ 所定义（锚定于 **Section 3** 的 Generation 段落及 **Eq. 8**）。

### 核心洞察与机制优势

这一分层设计背后的核心洞察是：利用 VAE 的正则化隐空间来降低扩散模型的训练难度，同时通过保持点结构的隐表示 $h_0$，兼顾了生成质量、任务灵活性以及自然的形状解耦。

*   **高质量生成**：隐空间的平滑性使得扩散模型更易学习，从而生成更高质量的样本。决定性证据来自 **Table 1**，在 ShapeNet 的飞机、椅子、汽车类别上，LION 的 1-NNA 指标显著优于直接对点云建模的扩散基线 PVD 和 DPM。
*   **架构有效性**：消融实验（**Table 11**）证实，同时使用 $z_0$ 和 $h_0$ 的完整分层架构，其生成质量（1-NNA）显著优于仅使用单一隐变量的消融变体，证明了两个层次隐空间的互补性。
*   **任务灵活性**：得益于 VAE 架构，LION 可以通过微调解码器来实现对多种条件信号（如体素引导）的适配，而无需重新训练扩散模型，展现了良好的任务泛化能力。
*   **自然的形状解耦**：全局形状 $z_0$ 和局部细节 $h_0$ 的分离，使得模型天然支持形状插值（**Figure 7**）和细节编辑（**Figure 2**）等应用。



LION 构建了一个**两阶段、三层级的生成式框架**，其核心设计思想是将点云的生成任务从高维、复杂的原始坐标空间迁移到一个平滑、正则化的隐空间中进行。该框架由第一阶段的层次化变分自编码器（VAE）和第二阶段的隐空间去噪扩散模型（DDM）共同构成。

### 框架的层级结构

整个生成模型定义了一个层级化的联合分布，其生成过程严格遵循“从全局到局部”的因果链条：

$$p_{\xi,\psi,\theta}(\mathbf{x},\mathbf{h}_0,\mathbf{z}_0) = p_{\xi}(\mathbf{x}|\mathbf{h}_0,\mathbf{z}_0) \, p_{\psi}(\mathbf{h}_0|\mathbf{z}_0) \, p_{\theta}(\mathbf{z}_0)$$

该公式定义了三个核心模块及其依赖关系：
1.  **形状先验** $p_{\theta}(\mathbf{z}_0)$：对全局形状隐变量 $\mathbf{z}_0$ 的分布建模。
2.  **隐点条件先验** $p_{\psi}(\mathbf{h}_0|\mathbf{z}_0)$：在给定全局形状 $\mathbf{z}_0$ 的条件下，对点结构隐变量 $\mathbf{h}_0$ 的分布建模。
3.  **解码器** $p_{\xi}(\mathbf{x}|\mathbf{h}_0,\mathbf{z}_0)$：从全局形状和点结构隐变量中重建出原始点云 $\mathbf{x}$。

### 两阶段训练与数据流

LION 的训练被明确划分为两个阶段，以确保隐空间的正则化与扩散模型的高效训练：

**第一阶段：层次化 VAE 训练**
此阶段旨在学习一个能够将点云压缩为紧凑、平滑隐表示的 VAE。数据流如下：
*   **编码**：输入点云 $\mathbf{x}$ 首先通过基于 PVCNN 的 **Shape Latent Encoder** 编码为全局形状隐变量 $\mathbf{z}_0$。随后，**Latent Point Encoder**（同样基于 PVCNN 并引入了自适应组归一化 AdaGN）以 $\mathbf{z}_0$ 为条件，将点云进一步编码为点结构隐变量 $\mathbf{h}_0$。
*   **解码**：**Decoder**（基于 PVCNN）接收 $\mathbf{z}_0$ 和 $\mathbf{h}_0$，重建出点云。
*   **训练目标**：通过优化修改后的证据下界（ELBO）来训练，该目标在点云重建损失和隐变量的 KL 正则化项之间进行平衡（由 $\lambda_{\mathbf{z}}$ 和 $\lambda_{\mathbf{h}}$ 控制权重）。

$$\mathcal{L}_{\mathrm{ELBO}}(\phi,\xi) = \mathbb{E}_{p(\mathbf{x}), q_\phi(\mathbf{z}_0|\mathbf{x}), q_\phi(\mathbf{h}_0|\mathbf{x},\mathbf{z}_0)} [\log p_\xi(\mathbf{x}|\mathbf{h}_0,\mathbf{z}_0) - \lambda_{\mathbf{z}} D_{\mathrm{KL}}(q_\phi(\mathbf{z}_0|\mathbf{x}) \vert p(\mathbf{z}_0)) - \lambda_{\mathbf{h}} D_{\mathrm{KL}}(q_\phi(\mathbf{h}_0|\mathbf{x},\mathbf{z}_0) \vert p(\mathbf{h}_0))]$$

**第二阶段：隐空间扩散模型训练**
在第一阶段 VAE 训练完成后，其参数被冻结。此阶段在 VAE 产生的平滑隐空间上训练两个去噪扩散模型，以学习隐变量的先验分布：
*   **全局形状扩散模型 (Shape Latent DDM)**：一个基于 ResNet 架构的混合得分模型，在 $\mathbf{z}_0$ 空间上进行加噪与去噪训练。其损失函数为标准的去噪得分匹配目标：
    $$\mathcal{L}_{\mathrm{SM}^{\mathbf{z}}}(\theta) = \mathbb{E}_{t \sim U\{1,T\}, p(\mathbf{x}), q_\phi(\mathbf{z}_0|\mathbf{x}), \epsilon \sim \mathcal{N}(\mathbf{0},I)} ||\epsilon - \epsilon_\theta(\mathbf{z}_t, t)||_2^2$$
*   **隐点扩散模型 (Latent Point DDM)**：一个基于 PVCNN 架构的混合得分模型，以 $\mathbf{z}_0$ 为条件，在 $\mathbf{h}_0$ 空间上进行加噪与去噪训练。其损失函数同样为条件去噪得分匹配目标：
    $$\mathcal{L}_{\mathrm{SM}^{\hbar}}(\psi) = \mathbb{E}_{t \sim U\{1,T\}, p(\mathbf{x}), q_\phi(\mathbf{z}_0|\mathbf{x}), q_\phi(\mathbf{h}_0|\mathbf{x},\mathbf{z}_0), \epsilon \sim \mathcal{N}(\mathbf{0},I)} ||\epsilon - \epsilon_\psi(\mathbf{h}_t, \mathbf{z}_0, t)||_2^2$$

### 生成流程

在推理生成时，LION 按照层级顺序进行采样：
1.  从标准高斯噪声出发，通过 **Shape Latent DDM** 逐步去噪，采样得到全局形状隐变量 $\mathbf{z}_0$。
2.  以采样得到的 $\mathbf{z}_0$ 为条件，再次从噪声出发，通过 **Latent Point DDM** 逐步去噪，采样得到点结构隐变量 $\mathbf{h}_0$。
3.  将 $(\mathbf{h}_0, \mathbf{z}_0)$ 输入到训练好的 **Decoder** 中，一次性解码出最终的点云。

### 可选的网格重建模块

为了生成可直接用于图形学应用的水密网格，LION 集成了一个可选的 **SAP (Shape As Points) 网格重建**模块。该模块基于可微的泊松表面重建，并在 LION 自编码器生成的训练数据上进行微调，以适应 LION 输出点云的特定噪声分布，从而从生成的点云中提取出平滑的网格。



LION 的核心架构是一个层次化变分自编码器（VAE），它将点云压缩到两个不同粒度的隐空间，并在这两个隐空间上分别训练去噪扩散模型（DDM）。整个系统通过两阶段训练完成：第一阶段训练 VAE 以获得正则化的隐表示，第二阶段在冻结的隐编码上训练两个分层 DDM。

### 关键模块

**Shape Latent Encoder（全局形状编码器）** 基于 PVCNN 架构，将输入点云 $\mathbf{x} \in \mathbb{R}^{N \times 3}$ 编码为全局形状隐变量 $\mathbf{z}_0 \in \mathbb{R}^{D_{\mathbf{z}}}$。该隐变量捕捉物体的整体几何语义，不保留点序结构。

**Latent Point Encoder（隐点编码器）** 同样基于 PVCNN，但引入自适应组归一化（Adaptive Group Normalization, AdaGN）以全局隐变量 $\mathbf{z}_0$ 为条件，将点云编码为点结构化的隐变量 $\mathbf{h}_0 \in \mathbb{R}^{N \times (3 + D_{\mathbf{h}})}$。其中前三维对应点的空间位置，额外 $D_{\mathbf{h}}$ 维为可选特征通道。消融实验表明 $D_{\mathbf{h}}=1$ 时在汽车类别上取得最佳性能平衡（Table 14）。

**Shape Latent DDM（全局形状扩散模型）** 使用 ResNet 骨干网络与混合得分参数化（mixed-score parameterization），在 $\mathbf{z}_0$ 空间上执行去噪扩散。该模型负责从标准高斯先验中采样全局形状。

**Latent Point DDM（隐点扩散模型）** 使用 PVCNN 骨干网络，以 $\mathbf{z}_0$ 为条件，在 $\mathbf{h}_0$ 空间上执行去噪扩散。消融实验证实 PVCNN 骨干网络在汽车类别上优于 DGCNN 和 PointTransformer（Table 13）。该模型负责在给定全局形状的条件下生成局部细节。

**Decoder（解码器）** 基于 PVCNN，从 $\mathbf{z}_0$ 和 $\mathbf{h}_0$ 联合重建输出点云 $\mathbf{x}$。

**SAP Mesh Reconstruction（可选网格重建模块）** 基于 Shape As Points（SAP）方法，利用可微泊松曲面重建从生成点云中提取平滑网格。论文对 SAP 在 LION 自编码器生成的训练数据上进行微调，以适应 LION 特有的噪声分布（Figure 20, Table 15）。

### 核心公式推导

#### 第一阶段：VAE 训练目标

LION 的 VAE 训练使用修改版证据下界（ELBO），引入 KL 散度平衡权重：

$$
\mathcal{L}_{\mathrm{ELBO}}(\phi,\xi) = \mathbb{E}_{p(\mathbf{x}), q_\phi(\mathbf{z}_0|\mathbf{x}), q_\phi(\mathbf{h}_0|\mathbf{x},\mathbf{z}_0)} [\log p_\xi(\mathbf{x}|\mathbf{h}_0,\mathbf{z}_0) - \lambda_{\mathbf{z}} D_{\mathrm{KL}}(q_\phi(\mathbf{z}_0|\mathbf{x}) \vert p(\mathbf{z}_0)) - \lambda_{\mathbf{h}} D_{\mathrm{KL}}(q_\phi(\mathbf{h}_0|\mathbf{x},\mathbf{z}_0) \vert p(\mathbf{h}_0))]
$$

其中：
- $q_\phi(\mathbf{z}_0|\mathbf{x})$ 为全局形状编码器的后验分布
- $q_\phi(\mathbf{h}_0|\mathbf{x},\mathbf{z}_0)$ 为以 $\mathbf{z}_0$ 为条件的隐点编码器后验分布
- $p_\xi(\mathbf{x}|\mathbf{h}_0,\mathbf{z}_0)$ 为解码器的重建似然
- $\lambda_{\mathbf{z}}$ 和 $\lambda_{\mathbf{h}}$ 为 KL 正则化项的平衡权重
- 先验 $p(\mathbf{z}_0)$ 和 $p(\mathbf{h}_0)$ 均设为标准高斯分布

该目标在点云重建精度和隐空间正则化之间取得平衡，为后续扩散建模提供平滑的隐空间。

#### 第二阶段：形状隐变量扩散模型损失

在冻结 VAE 编码器后，对全局形状隐变量训练去噪扩散模型，使用标准去噪得分匹配目标：

$$
\mathcal{L}_{\mathrm{SM}^{\mathbf{z}}}(\theta) = \mathbb{E}_{t \sim U\{1,T\}, p(\mathbf{x}), q_\phi(\mathbf{z}_0|\mathbf{x}), \epsilon \sim \mathcal{N}(\mathbf{0},I)} ||\epsilon - \epsilon_\theta(\mathbf{z}_t, t)||_2^2
$$

其中：
- $t$ 从 $\{1, \ldots, T\}$ 均匀采样
- $\mathbf{z}_t = \sqrt{\bar{\alpha}_t}\mathbf{z}_0 + \sqrt{1-\bar{\alpha}_t}\epsilon$ 为加噪后的隐变量
- $\epsilon_\theta(\mathbf{z}_t, t)$ 为预测所加噪声的神经网络

#### 第三阶段：隐点扩散模型损失

以全局形状隐变量 $\mathbf{z}_0$ 为条件，训练点结构化的隐点扩散模型：

$$
\mathcal{L}_{\mathrm{SM}^{\hbar}}(\psi) = \mathbb{E}_{t \sim U\{1,T\}, p(\mathbf{x}), q_\phi(\mathbf{z}_0|\mathbf{x}), q_\phi(\mathbf{h}_0|\mathbf{x},\mathbf{z}_0), \epsilon \sim \mathcal{N}(\mathbf{0},I)} ||\epsilon - \epsilon_\psi(\mathbf{h}_t, \mathbf{z}_0, t)||_2^2
$$

其中 $\epsilon_\psi(\mathbf{h}_t, \mathbf{z}_0, t)$ 同时以时间步 $t$ 和全局形状 $\mathbf{z}_0$ 为条件，预测隐点空间中所加的噪声。

#### 层次化生成模型的联合分布

完成两阶段训练后，LION 定义的生成模型联合分布为：

$$
p_{\xi,\psi,\theta}(\mathbf{x},\mathbf{h}_0,\mathbf{z}_0) = p_{\xi}(\mathbf{x}|\mathbf{h}_0,\mathbf{z}_0) p_{\psi}(\mathbf{h}_0|\mathbf{z}_0) p_{\theta}(\mathbf{z}_0)
$$

生成过程按层级递进：首先从形状隐变量扩散模型 $p_{\theta}(\mathbf{z}_0)$ 采样全局形状 $\mathbf{z}_0$，然后以 $\mathbf{z}_0$ 为条件从隐点扩散模型 $p_{\psi}(\mathbf{h}_0|\mathbf{z}_0)$ 采样点结构化隐变量 $\mathbf{h}_0$，最后通过解码器 $p_{\xi}(\mathbf{x}|\mathbf{h}_0,\mathbf{z}_0)$ 生成最终点云。



## 实验与关键发现

LION 在多个 ShapeNet 基准上进行了系统评估，覆盖单类、多类无条件生成、体素引导合成和网格重建等任务。核心结论如下：**(1)** 在 ShapeNet 的三个标准类别（飞机、椅子、汽车）上，LION 在 1-NNA 指标上全面超越了直接对点云建模的扩散基线 PVD 和 DPM，并在不同归一化设置下均达到 SOTA；**(2)** 消融实验证实，同时使用全局形状隐变量 $\mathbf{z}_0$ 和点结构化隐变量 $\mathbf{h}_0$ 的完全分层架构是性能的关键来源；**(3)** LION 通过隐空间的扩散-去噪（diffuse-denoise）过程，天然支持体素引导合成、形状插值和细节编辑等多种下游应用。

### 主要生成质量对比

**Table 1** 和 **Table 2** 分别报告了在全局归一化和单独归一化设置下的 1-NNA 指标。在全局归一化下（Table 1），LION 在飞机、椅子、汽车三个类别上的 1-NNA CD 分别达到 67.41、53.70、51.14，相比最强基线 PVD 分别降低了 6.41、2.56、3.41 点。在单独归一化下（Table 2），LION 同样保持领先，且与基于规范化流的 **PointFlow** (Yang et al., ICCV 2019) 和基于形状隐变量加条件扩散的 **DPM** 相比优势更为显著。在 ShapeNet-vol 数据集上（Table 3、Table 4），作者重新训练了 PVD、DPM 和 IM-GAN 以确保公平对比，LION 在 13 类无条件生成任务上取得 51.85 的 1-NNA CD，比 PVD 的 58.65 降低了 6.80 点。

上述结果的核心机制在于：直接在原始点云坐标空间训练扩散模型面临高维复杂数据分布的挑战，而 LION 通过 VAE 将点云压缩到平滑、正则化的隐空间后再进行扩散建模，显著降低了扩散模型的训练难度。同时，点结构化的隐表示保留了 PVCNN 等点云处理架构的优势，使得解码器能够高保真地重建几何细节。

### 消融实验：分层架构的必要性

**Table 11**（附录 F.1.1）给出了最关键的消融证据：在汽车类别上，完整的层级架构（同时使用 $\mathbf{z}_0$ 和 $\mathbf{h}_0$）的 1-NNA 显著优于仅使用全局形状隐变量的变体（移除 $\mathbf{h}_0$）和仅使用点结构化隐变量的变体（移除 $\mathbf{z}_0$）。这验证了论文的核心设计主张——全局形状隐变量捕获物体的整体拓扑和粗粒度结构，而点结构化隐变量编码局部几何细节，两者互补是实现高质量生成的必要条件。

进一步的骨干网络消融（**Table 13**）表明，在隐点扩散模型中使用 PVCNN 作为骨干网络，相比 DGCNN 和 PointTransformer，在汽车类别上具有更优的生成质量。隐点额外特征维度 $D_{\mathbf{h}}$ 的消融（**Table 14**）显示，$D_{\mathbf{h}}=1$ 在性能与计算开销之间取得了最佳平衡。

### 网格重建与下游应用

LION 生成的原始输出为点云，通过可选的 Shape As Points (SAP) 模块可提取平滑网格。**Figure 5** 展示了从生成点云到网格的重建流程。关键的工程细节是：SAP 需要在 LION 自编码器的训练数据上进行微调，以适应 LION 输出点云的特定噪声分布。**Figure 20** 和 **Table 15** 的消融表明，微调后的 SAP 能显著提升网格重建质量，使其接近原始生成点云的定量指标。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2210_06978/figures/014_Figure.jpg]]

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2210_06978/figures/017_Figure.jpg]]

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2210_06978/figures/065_Figure.jpg]]

LION 的隐空间设计天然支持多种应用范式。**Figure 4** 展示了体素引导合成：通过对隐变量执行 diffuse-denoise 过程，可在保持整体形状的前提下生成多样化的合理细节。**Figure 7** 展示了形状插值：在标准高斯先验中对不同形状的编码进行插值，可产生平滑的语义过渡。**Figure 8** 进一步揭示，在 13 类无条件模型中固定全局形状隐变量 $\mathbf{z}_0$ 时，生成的样本保持一致的粗粒度结构，而点结构化隐变量 $\mathbf{h}_0$ 的采样则驱动局部细节变化——这直观地验证了分层隐空间实现了自然的形状解耦。

### 失败模式与局限性

尽管 LION 在生成质量上表现优异，但存在以下已知局限：

1. **采样速度**：标准 DDPM 采样需要 1000 步，生成单个形状约需 27 秒。**Figure 38** 和 **Table 25** 显示，DDIM 加速采样在 5 步时完全失效，10 步以上才开始生成合理形状，25 步可将时间压缩至 1 秒以内，但步数过少仍会导致质量下降。
2. **小数据集多样性受限**：在 Mug、Bottle 等非常小的类别上，生成多样性可能不足（原文提及，但未提供定量证据，需手动验证）。
3. **纹理缺失**：LION 目前仅生成几何形状，不包含纹理信息，需额外的后处理步骤（如 Text2Mesh）来添加纹理。
4. **SAP 未端到端联合训练**：网格重建模块的微调仅针对 LION 的输出噪声，未与自编码器进行端到端优化，可能限制网格质量的进一步提升。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2210_06978/figures/060_Figure_38.jpg]]
*Figure 38: DDIM samples from LION trained on different data. The top two rows show the number of steps and the wall-clock time required for drawing one sample. In general, DDIM sampling with 5 steps fails to generate reasonable shapes and DDIM sampling with more than 10 steps can generate high-quality shapes. With DDIM sampling, we can reduce the time to generate an object from 27.09 seconds (1,000 steps) to less than 1 second (25 steps). The sampling time is computed by calling the prior model and the decoder of LION with batch size as 1, number of points as 2,048*

### 补充图表

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2210_06978/figures/008_Table_2.jpg]]
*Table 2: Generation results (1-NNA↓) on ShapeNet dataset from PointFlow [31]. All data normalized individually into [-1, 1]. Table 3: Results (1-NNA↓) on ShapeNet-vol*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2210_06978/figures/063_Figure_39.jpg]]
*Figure 39: Text2Mesh results of airplane, chair, car, animal. The original mesh is generated by LION*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2210_06978/figures/009_Table_1.jpg]]
*Table 1: Generation metrics (1-NNA↓) on airplane, chair, car categories from ShapeNet dataset from PointFlow [31]. Training and test data normalized globally into [-1, 1]*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2210_06978/figures/011_Table.jpg]]

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2210_06978/figures/023_Table_5.jpg]]
*Table 5: Shape Latent Encoder Architecture Hyperparameters*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2210_06978/figures/024_Table_6.jpg]]
*Table 6: Latent Point Encoder Architecture Hyperparameters*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2210_06978/figures/025_Table_7.jpg]]
*Table 7: Decoder Architecture Hyperparameters*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2210_06978/figures/026_Table_8.jpg]]
*Table 8: Shape Latent DDM Architecture Hyperparameters*



## 定位与知识库关联

### 1. 核心瓶颈与设计动机

3D 形状生成的核心瓶颈在于：直接在复杂高维的点云坐标空间训练扩散模型难度极大。此前的扩散基线（如 **PVD** 和 **DPM**）直接在原始点云上执行加噪与去噪，难以在单一模型中同时保证生成质量、多样性与灵活的任务适配。LION 的因果调节旋钮是构造一个具有点结构隐变量和全局形状隐变量的分层 VAE，将点云压缩到一个平滑且正则化的隐空间，然后在该隐空间中训练两个分层去噪扩散模型。这利用了隐空间的平滑性来简化扩散建模，同时保留点结构以发挥点云处理架构（Point-Voxel CNN）的优势。

### 2. 与基线方法的差异化定位

LION 在扩散建模空间和生成过程两个关键维度上改变了基线设计。

| 设计维度 | 基线方法 | LION |
|----------|----------|------|
| 扩散建模空间 | 在原始点云坐标空间直接加噪/去噪（PVD, DPM） | 在分层 VAE 的隐空间中进行扩散建模，包含全局形状隐变量 $\mathbf{z}_0$ 和点结构化隐变量 $\mathbf{h}_0$ |
| 生成过程 | 单个扩散模型在点云空间逐步去噪 | 先层次化采样 $\mathbf{z}_0$，再条件采样 $\mathbf{h}_0$，最后通过解码器生成点云 |

**PVD (Point-Voxel Diffusion)** 是直接在点云坐标上应用扩散模型的强基线，但受限于点云空间的高维复杂性。**DPM (Diffusion Probabilistic Models for 3D Point Cloud Generation)** 使用规范化流建模形状隐变量并结合点态条件扩散，但其隐空间设计未采用点结构化表示，且缺乏分层架构。**PointFlow** (Yang et al., ICCV 2019) 基于连续规范化流，在生成多样性上表现良好，但生成质量在 1-NNA 指标上显著弱于 LION。

LION 的分层设计在消融实验中得到了直接验证：同时使用全局形状隐变量 $\mathbf{z}_0$ 和点结构隐变量 $\mathbf{h}_0$ 的完全分层架构，其生成质量（1-NNA）显著优于仅使用单一隐变量的消融变体（Table 11）。

### 3. 方法谱系中的位置

LION 处于以下三条技术路线的交叉点：

- **隐空间扩散模型**：继承 LDMs（Latent Diffusion Models）在 2D 图像生成中的核心思想，将扩散过程从数据空间迁移到 VAE 隐空间，但针对 3D 点云的非规则结构进行了专门设计。
- **点云深度生成模型**：延续 PointFlow、DPM 等工作的点云生成传统，但通过 PVCNN 骨干网络和点结构化隐表示，更好地利用了 3D 几何的先验。
- **分层 VAE**：采用两阶段训练策略——先训练具有标准高斯先验的 VAE，再在隐编码上训练扩散模型。这种解耦设计使得编码器可以独立微调以适应多种下游任务（如体素引导合成），而无需重新训练扩散模型。

### 4. 适用边界与限制

LION 的能力边界和已知局限包括：

1. **模态限制**：目前仅在 3D 点云上训练，不能直接生成带纹理的形状，需要额外的后处理（如 Text2Mesh）来添加纹理。
2. **场景范围**：模型专注于单个物体生成，尚未扩展到完整的 3D 场景合成。
3. **采样速度**：标准 DDPM 采样约需 27 秒/个形状。DDIM 可将时间压缩至 1 秒以内（25 步），但步数过少（如 5 步）会导致生成质量显著下降（Table 25, Figure 38）。
4. **网格重建耦合**：SAP 网格重建模块的微调仅针对 LION 的输出噪声，未与 VAE 进行端到端联合训练，存在进一步优化的空间。
5. **小数据集多样性**：在非常小的数据集上（如 Mug、Bottle 类），生成多样性可能受限。

### 5. 开放问题

从 LION 的设计出发，以下方向值得进一步探索：

- **多模态条件耦合**：能否将 LION 与图像/文本条件进行端到端联合训练，以提升可控生成的质量？
- **更高效的采样**：如何在进一步减少去噪步数的同时，保持甚至提升生成质量？
- **细粒度语义控制**：分层隐空间是否可以被设计以学习部件级的语义控制，从而实现更精细的形状编辑？
- **大规模泛化**：LION 在大规模、跨类别的真实 3D 数据集（如 Objaverse）上的泛化能力如何？
- **条件信号整合**：能否将体素引导等其他条件信号直接整合到扩散模型的训练中，而非仅通过编码器微调的方式实现？



## 原文 PDF

![[paperPDFs/NEURIPS_2022/LION_Latent_Point_Diffusion_Models_for_3D_Shape_Generation.pdf]]
