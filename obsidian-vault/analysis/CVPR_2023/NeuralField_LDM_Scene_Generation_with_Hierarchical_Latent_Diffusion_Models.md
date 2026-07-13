---
title: "NeuralField-LDM: Scene Generation with Hierarchical Latent Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2023
pdf_ref: paperPDFs/CVPR_2023/NeuralField_LDM_Scene_Generation_with_Hierarchical_Latent_Diffusion_Models.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/NFLDM/
aliases:
- NLNL
- NeuralField-LDM
tags:
- CVPR_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "显式体素网格表示与分层潜在空间（全局g、粗c、细f）结合，通过从全局到局部的条件扩散生成，实现多尺度场景分布建模。"
primary_logic: "将场景编码为密度和特征体素网格，进一步压缩分解为三个潜在变量（1D全局、3D粗、2D细），然后使用分层潜在扩散模型依次生成g、c、f，使模型能够分别捕捉全局属性、粗略3D结构和精细2D细节，从而显著提升复杂场景生成质量。"
claims:
- "NF-LDM通过编码图像到显式体素网格，并分解为三层潜在（g, c, f）来克服单向量瓶颈。"
- "在复杂户外数据集Carla上，NF-LDM的FID为35.69，远低于EG3D的76.89和GSN的75.45。"
- "分层消融实验显示，添加全局和精细潜在可显著提升FID（从46.43到35.69）。"
- "VizDoom 上 FID = 19.54*"
---

# NeuralField-LDM: Scene Generation with Hierarchical Latent Diffusion Models

> [!tip] 核心洞察
> 将场景编码为密度和特征体素网格，进一步压缩分解为三个潜在变量（1D全局、3D粗、2D细），然后使用分层潜在扩散模型依次生成g、c、f，使模型能够分别捕捉全局属性、粗略3D结构和精细2D细节，从而显著提升复杂场景生成质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | NeuralField-LDM：基于分层潜在扩散模型的场景生成 |
| 英文题名 | NeuralField-LDM: Scene Generation with Hierarchical Latent Diffusion Models |
| 会议/期刊 | CVPR 2023 |
| Links | [paper](https://arxiv.org/abs/2304.09787) · [Project](https://research.nvidia.com/labs/toronto-ai/NFLDM/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | NeuralField-LDM (NF-LDM) |
| Dataset | VizDoom, Replica, Carla, AVD |

> [!tip] 效果简介
> - VizDoom 上，FID 为 19.54*，对比 33.70 (GAUDI)，变化 -14.16。
> - Replica 上，FID 为 14.59，对比 18.75 (GAUDI)，变化 -4.16。
> - Carla 上，FID 为 35.69，对比 75.45 (GSN)，变化 -39.76。

## 概要

**核心问题**：现有三维场景生成方法（如GAUDI）通常将整个场景压缩为单个全局潜在向量，导致模型难以同时捕捉场景的全局属性与局部细节，在复杂场景分布建模上形成瓶颈。

**方法定位**：NeuralField-LDM (NF-LDM) 提出了一种显式体素网格表示与分层潜在扩散模型相结合的生成框架。该方法首先将多视图图像编码为密度和特征体素网格，再通过潜在自编码器将其分解为三个层次的潜在变量——1D全局潜在 $g$、3D粗糙潜在 $c$ 和2D精细潜在 $f$——随后以分层条件扩散的方式依次生成 $g \rightarrow c \rightarrow f$，实现从全局到局部的多尺度场景分布建模。

**知识谱系**：NF-LDM 位于神经场生成与扩散模型的交叉地带。相较于基于GAN的隐式表示方法（如GRAF、π-GAN、EG3D）和单向量自解码器方案（如GAUDI），其核心差异在于用显式体素网格替代隐式表示，并用分层潜在空间替代单一全局编码，从而在复杂户外场景生成上获得显著优势。

**主要结果**：
- 在复杂户外数据集Carla上，NF-LDM的FID达到35.69，远低于EG3D的76.89和GSN的75.45；在AVD数据集上FID为54.26，对比GSN的166.07降幅超过111。
- 在视频生成质量指标FVD上，Carla数据集达到91.80（EG3D为134.94），AVD数据集达到242.50（EG3D为1232.38）。
- 分层消融实验证实，完整的三层潜在结构（$g, c, f$）相比仅使用粗糙潜在 $c$，FID从46.43降至35.69，验证了多尺度分层建模的必要性。

**局限性**：三阶段流水线和层次结构带来较高的训练与采样计算开销；密集体素网格在大规模场景下的体渲染和扩散模型训练成本较高；需要多视图图像作为输入，在场景数有限的数据集（如AVD）上可能限制生成多样性。



三维场景生成是计算机视觉与图形学中的核心挑战，其目标是从有限观测中学习复杂三维环境的分布，并能够合成新的、逼真的场景。近年来，神经辐射场（NeRF）的兴起使得高质量三维表示成为可能，但将NeRF纳入生成式建模框架仍面临根本性困难：**场景的全局属性（如光照、整体布局）与局部细节（如物体纹理、几何结构）分布在截然不同的尺度上，单一表示难以同时捕捉。**

现有方法大多采用“单向量瓶颈”策略。以**GAUDI**（Bautista et al., 2022）为代表的工作，将整个场景压缩为一个全局潜在向量，再通过扩散模型或自解码器对该向量进行生成。这种设计的核心缺陷在于：一个固定维度的向量承载了场景的全部信息，导致模型在复杂场景（尤其是户外开放环境）上难以建模丰富的局部变化和细节结构。类似地，**GSN**（DeVries et al., 2021）和**EG3D**（Chan et al., 2022）等方法虽然在二维特征图或三平面表示上有所改进，但仍未从根本上解决多尺度特征分离的问题。在Carla和AVD等复杂户外数据集上，这些方法的FID指标高达75–166，生成质量严重受限。

另一个关键瓶颈在于**表示形式的选择**。隐式NeRF表示虽然连续且紧凑，但其黑箱性质使得对场景进行显式控制、编辑和分层生成极为困难。相比之下，显式体素网格天然支持空间定位和多尺度操作，但直接在高分辨率体素上训练扩散模型面临维度灾难——实验表明，直接在128×128×32的体素网格上拟合扩散模型几乎无法生成有意义的结构。

本文的动机由此明确：**设计一种能够将场景分解为多尺度潜在变量的生成框架，使得全局属性、粗略三维结构和精细二维细节可以分别建模、分层生成。** 具体而言，NeuralField-LDM通过将场景编码为显式的密度与特征体素网格，再经由潜在自编码器压缩分解为三个层次的潜在变量——1D全局潜在 $g$、3D粗糙潜在 $c$ 和2D精细潜在 $f$——从而让分层潜在扩散模型能够依次捕捉场景的宏观布局、中观结构和微观纹理。这一设计从根本上突破了单向量瓶颈，为复杂三维场景的高质量生成开辟了新路径。



## 核心方法与创新机理

### 从全局潜在向量到分层体素潜在表示

现有三维场景生成方法普遍采用单一全局潜在向量编码整个场景，例如 **GAUDI** 将场景压缩为单个全局码，再通过扩散模型学习其分布。这种设计构成了关键瓶颈：一个固定维度的向量难以同时承载场景的全局属性（如光照、整体风格）、粗略三维结构（如建筑布局、道路走向）和精细局部细节（如纹理、小物体），导致复杂场景分布的建模能力受限。

NeuralField-LDM 的核心创新在于**将场景表示从单一全局潜在向量替换为显式体素网格与三层分层潜在空间**。具体而言，方法首先将多视图 RGB 图像编码为显式的密度体素网格和特征体素网格，然后通过潜在自编码器将其压缩分解为三个不同尺度的潜在变量：

- **1D 全局潜在 $g$**：采用 KL 正则化，捕捉场景级全局属性；
- **3D 粗糙潜在 $c$**：采用向量量化，编码粗略的三维空间结构；
- **2D 精细潜在 $f$**：采用向量量化，保留精细的二维细节信息。

这一 changed slot 的因果机制在于：分层分解使生成模型可以**从全局到局部依次建模场景分布**。生成过程定义为 $p(V, g, c, f) = p(V|g, c, f) \, p(f|g, c) \, p(c|g) \, p(g)$，三个扩散模型 $\psi_g$、$\psi_c$、$\psi_f$ 分别学习 $p(g)$、$p(c|g)$、$p(f|g, c)$。这种条件化生成策略迫使模型在生成局部细节时显式地利用已生成的全局和结构信息，从而克服单向量瓶颈。

### 显式体素网格与神经场表示的融合

与基于隐式 NeRF 的方法（如 **GRAF**、**π-GAN**）不同，NF-LDM 选择**显式的密度和特征体素网格**作为场景表示。这一设计带来了两个优势：其一，显式体素网格天然适合作为分层潜在分解的输入，因为其规则的三维结构可以直接进行 3D/2D 的下采样和编码；其二，密度体素网格使得几何结构可以通过 marching cubes 直接提取和可视化，增强了可解释性。

消融实验证实了显式密度建模的重要性：去除显式密度体素后，渲染质量显著下降（见 Figure 15）。体素尺寸的消融进一步表明，$128 \times 128 \times 32$ 的体素分辨率在感知损失上达到 0.2237，优于更小尺寸的配置（见 Table 12）。

### 分层扩散生成的条件化设计

分层潜在扩散模型的训练采用三个独立的去噪损失（公式 4-6），其中粗糙潜在扩散模型 $\psi_c$ 以全局潜在 $g_0$ 为条件，精细潜在扩散模型 $\psi_f$ 同时以 $g_0$ 和 $c_0$ 为条件。这种设计使得每一层扩散模型都能充分利用已生成的高层信息，形成从全局到局部的信息流动。

分层消融实验直接验证了这一设计的有效性：在 Carla 数据集上，仅使用粗糙潜在 $c$ 时 FID 为 46.43；加入精细潜在 $f$ 后 FID 降至 43.52；完整的三层模型（$g + c + f$）进一步将 FID 降至 35.69（见 Table 4）。这一结果表明，全局潜在和精细潜在各自贡献了独立的生成质量增益，分层设计是性能提升的关键因素。

### 后优化机制：2D 先验注入 3D 生成

NF-LDM 还引入了基于 Score Distillation Sampling 的后优化步骤，利用预训练的 2D 扩散先验进一步优化生成的体素质量或修改场景风格。SDS 损失的梯度通过可微体渲染反向传播至体素，等效于在每一步去噪中从 $\frac{p(x|y)^\alpha}{p(x|y')}$ 采样。这一机制使得生成结果可以在不重新训练整个流水线的情况下实现质量增强和风格迁移（如将白天场景转为傍晚场景，见 Figure 10）。

### 与基线方法的关键差异总结

| 设计维度 | 基线方法 | NF-LDM 创新 |
|---------|---------|------------|
| 场景表示 | 单一全局潜在向量（GAUDI）或隐式 NeRF（GSN） | 显式密度与特征体素网格 + 三层潜在（$g, c, f$） |
| 生成策略 | 单层扩散模型或 GAN 生成器 | 分层条件扩散：$p(g) \to p(c|g) \to p(f|g,c)$ |
| 信息利用 | 部分方法未使用深度信息（GRAF、π-GAN） | 显式利用深度监督进行体素构建 |
| 后处理 | 无 | SDS 后优化支持质量增强与风格编辑 |

需要注意的是，NF-LDM 利用了深度监督信息，而部分基线方法（如 GRAF、π-GAN）未使用深度，这可能在一定程度上影响比较的公平性。此外，GAUDI 采用自动解码器在训练时为每个场景优化潜在码，而 NF-LDM 使用自编码器直接推断潜在码，两者的训练策略存在本质差异。



NeuralField-LDM (NF-LDM) 采用**三阶段分层生成流水线**，将复杂三维场景的生成问题分解为场景编码、潜在压缩与分层扩散生成三个阶段。其核心设计动机在于克服现有方法（如GAUDI）将整个场景压缩为单一全局潜在向量所导致的分布建模瓶颈——单一向量难以同时捕捉场景的全局属性、粗略三维结构与精细局部细节。

### 流水线总览

整个框架由四个核心模块串联构成（见 Figure 2）：

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2304_09787/figures/002_Figure_2.jpg]]
*Figure 2: Overview of NeuralField-LDM. We first encode RGB images with camera poses into a neural field represented by density and feature voxel grids. We compress the neural field into smaller latent spaces and fit a hierarchical latent diffusion model on the latent space. Sampled latents can then be decoded into a neural field that can be rendered into a given viewpoint*

1. **场景自编码器 (Scene Auto-Encoder)**：接收多视图RGB图像及其相机位姿，将其编码为显式的**密度体素网格**与**特征体素网格**。该模块通过2D CNN逐图提取特征，再经Lift-Splat-Shoot机制将2D特征提升至3D空间并融合为共享体素表示，最后通过体渲染与CNN解码器重建输入图像以监督训练。

2. **潜在体素自编码器 (Latent Voxel Auto-Encoder, LAE)**：将场景自编码器输出的体素网格进一步压缩分解为三个层次化的潜在变量：
   - **全局潜在 $g$**：1D向量，经KL正则化，捕捉场景级全局属性
   - **粗糙潜在 $c$**：3D体素潜在，经向量量化，编码粗略三维结构
   - **精细潜在 $f$**：2D特征图潜在，经向量量化，补充高频局部细节

3. **分层潜在扩散模型 (Hierarchical LDMs)**：依次训练三个去噪扩散模型 $\psi_g$、$\psi_c$、$\psi_f$，按照从全局到局部的条件生成链 $p(g) \rightarrow p(c|g) \rightarrow p(f|g,c)$ 进行采样。这一设计使模型能够分别建模不同尺度的场景分布，从而显著提升复杂场景的生成质量。

4. **后优化 (Post-Optimization)**：可选模块，利用Score Distillation Sampling (SDS) 对已生成的体素网格进行进一步优化，以提升渲染质量或实现风格迁移。

### 数据流与依赖关系

```
多视图RGB + 相机位姿
        │
        ▼
[场景自编码器] ─── 密度体素网格 + 特征体素网格
        │
        ▼
[潜在体素自编码器] ─── g (1D全局) ──┬── c (3D粗糙) ──┬── f (2D精细)
        │                           │                │
        ▼                           ▼                ▼
[分层LDMs]  ψ_g ──────────► ψ_c (条件于g) ──► ψ_f (条件于g,c)
        │
        ▼
[解码器] ─── 体素网格 ─── [可选: SDS后优化] ─── 新视角渲染
```

生成过程严格遵循条件概率分解 $p(V, g, c, f) = p(V|g, c, f) \, p(f|g, c) \, p(c|g) \, p(g)$，先由扩散模型采样潜在变量，再通过解码器恢复体素网格并渲染。训练时，三个扩散模型分别优化对应的去噪损失（Eq. 4-6），均采用 $x_0$-prediction 形式的DDM损失函数。

### 关键设计取舍

- **显式体素网格 vs 隐式NeRF**：NF-LDM选择显式密度与特征体素网格作为中间表示，而非直接操作隐式神经辐射场。消融实验（Figure 15）表明，显式密度建模能产生更高质量的渲染结果。
- **分层潜在 vs 单一潜在**：分层消融（Table 4）证实，仅使用粗糙潜在 $c$ 时FID为46.43，加入精细潜在 $f$ 后降至43.52，再加入全局潜在 $g$ 后进一步降至35.69，验证了三层结构的必要性。
- **潜在压缩的必要性**：直接在高维体素网格（$128 \times 128 \times 32$）上训练扩散模型效果不佳（Figure 14），LAE的压缩有效降低了扩散模型的建模难度。



### 3.1 场景自编码器（Scene Auto-Encoder）

场景自编码器将多视图RGB图像编码为显式的密度体素网格和特征体素网格，这是整个方法的基础表示层。其核心流程如下：

**图像编码与3D提升**：每张输入图像首先经过2D CNN处理，生成一个 $H \times W \times (D+C)$ 维的2D张量，其中 $D$ 为深度维度，$C$ 为特征维度。随后，采用类似Lift-Splat-Shoot（LSS）的方式将2D特征提升至3D空间，并将多视图的贡献合并到共享的体素网格中。

**体渲染与遮挡建模**：为将体素网格渲染为2D图像进行监督，方法沿相机射线构建锥体（frustum），并通过以下遮挡权重公式计算每个锥体单元的贡献：

$$O(h,w,d) = \exp(-\sum_{j=0}^{d-1} \sigma_{(h,w,j)} \delta_j) (1 - \exp(-\sigma_{(h,w,d)} \delta_d))$$

其中 $\sigma_{(h,w,d)}$ 为位置 $(h,w,d)$ 处的密度值，$\delta_j$ 为深度区间长度。该公式本质上是一个离散化的体渲染透射率-吸收率乘积：前一项 $\exp(-\sum_{j=0}^{d-1} \sigma \delta_j)$ 表示光线到达第 $d$ 层前的累积透射率，后一项 $(1 - \exp(-\sigma \delta_d))$ 表示当前层的吸收率。

**锥体构建**：将遮挡权重与特征向量结合，构建完整的锥体表示：

$$F(h,w,d) = [O(h,w,d) \phi(h,w), \sigma(h,w,d)]$$

即用遮挡权重缩放特征向量 $\phi(h,w)$，并与密度值拼接。该锥体随后通过CNN解码器重建RGB图像，以重建损失进行监督训练。

### 3.2 潜在体素自编码器（Latent Voxel Auto-Encoder, LAE）

LAE将场景自编码器输出的体素网格进一步压缩为三层潜在表示，以降低扩散模型的学习难度：

- **全局潜在 $g$**：1D向量，采用KL正则化，捕捉场景的全局属性（如光照、整体风格）。
- **粗糙潜在 $c$**：3D体素，采用向量量化（VQ），编码粗略的3D空间结构。
- **精细潜在 $f$**：2D特征图，同样采用向量量化，补充高频细节信息。

这种分解的因果机制在于：将场景分布解耦为全局-结构-细节三个层次，使扩散模型可以分别建模不同尺度的变化，从而突破单一全局向量（如GAUDI）的表达瓶颈。

### 3.3 分层潜在扩散模型（Hierarchical LDMs）

分层扩散模型按照条件依赖链 $p(g) \rightarrow p(c|g) \rightarrow p(f|g,c) \rightarrow p(V|g,c,f)$ 依次生成三层潜在变量。

**通用DDM去噪损失**：所有扩散模型均基于预测干净样本 $x_0$ 的范式训练：

$$\mathbb{E}_{t,\epsilon,x_0} [w(\lambda_t) ||x_0 - \hat{x}_\theta(x_t,t)||_2^2]$$

**全局LDM损失**：训练 $\psi_g$ 无条件生成全局潜在：

$$\mathbb{E}_{t,\epsilon,g_0} [w(\lambda_t) ||g_0 - \psi_g(g_t,t)||_2^2]$$

**粗糙LDM损失**：训练 $\psi_c$ 以全局潜在 $g_0$ 为条件生成粗糙潜在：

$$\mathbb{E}_{t,\epsilon,g_0,c_0} [w(\lambda_t) ||c_0 - \psi_c(c_t,g_0,t)||_2^2]$$

**精细LDM损失**：训练 $\psi_f$ 以 $g_0$ 和 $c_0$ 为条件生成精细潜在：

$$\mathbb{E}_{t,\epsilon,g_0,c_0,f_0} [w(\lambda_t) ||f_0 - \psi_f(f_t,g_0,c_0,t)||_2^2]$$

其中 $w(\lambda_t)$ 为信噪比相关的加权函数，$x_t$ 为加噪后的潜在变量。三个扩散模型均采用1D/3D/2D U-Net架构的对应变体。

### 3.4 后优化：分数蒸馏采样（SDS）

生成体素网格后，可选用Score Distillation Sampling（SDS）进行后优化，利用预训练2D扩散模型的先验知识进一步提升渲染质量或修改风格。SDS损失定义为：

$$\nabla_V L_{SDS} = \mathbb{E}_{\epsilon,t,\kappa} [w(\lambda_t) (\epsilon - \hat{\epsilon}_\theta(r(V,\kappa),t)) \frac{\partial r(V,\kappa)}{\partial V}]$$

其中 $V$ 为待优化的体素，$r(V,\kappa)$ 为在相机姿态 $\kappa$ 下的渲染图像，$\hat{\epsilon}_\theta$ 为预训练2D扩散模型的噪声预测。该损失通过2D扩散先验的梯度反向传播至3D体素，实现无需3D监督的质量提升。论文还引入负向导引策略，等效于在每一步去噪中采样 $\frac{p(x|y)^\alpha}{p(x|y')}$，以在风格修改中抑制不希望的属性。



## 实验与关键发现

### 主实验结果

NF-LDM在四个数据集上进行了评估：VizDoom和Replica（室内/受限环境），以及Carla和AVD（复杂户外场景）。评估指标采用图像质量FID和视频质量FVD。

**室内与受限场景（Table 1）**：在VizDoom上，NF-LDM取得FID 19.54*，显著优于GAUDI的33.70（降幅14.16）。在Replica上，NF-LDM取得FID 14.59，优于GAUDI的18.75（降幅4.16）。需注意VizDoom结果带星号，可能涉及特定实验设置。

**复杂户外场景（Table 2 & Table 3）**：这是NF-LDM的核心优势场景。在Carla上，NF-LDM的FID为35.69，而GSN为75.45，EG3D为76.89——NF-LDM将FID降低约40点。在更具挑战性的AVD数据集上，差距进一步拉大：NF-LDM的FID为54.26，GSN高达166.07（降幅111.81），EG3D为94.32。FVD指标呈现一致趋势：Carla上NF-LDM为91.80（EG3D为134.94），AVD上NF-LDM为242.50（EG3D高达1232.38，降幅近990点）。

**关键解读**：基线方法（GSN、EG3D、GAUDI）在复杂户外数据集上普遍失效，尤其是AVD。NF-LDM通过分层潜在表示（全局g + 粗c + 细f）有效捕捉了多尺度场景分布，这是性能跃升的核心机制。

**公平性说明**：部分基线（GRAF、π-GAN）未使用深度信息，而NF-LDM利用了深度监督，可能影响比较公平性。GAUDI使用自动解码器逐场景优化潜在码，与NF-LDM的自编码器推断策略不同。

### 消融实验

**分层潜在空间消融（Table 4，Carla数据集）**：仅使用粗潜在c时FID为46.43；加入细潜在f后降至43.52；再加入全局潜在g（完整模型）进一步降至35.69。每增加一层潜在表示均带来一致的FID改善，验证了分层设计的必要性。

**显式密度体素消融（Figure 15）**：移除显式密度体素网格后，渲染质量明显下降。显式密度与特征体素的联合表示是高质量场景重建的基础。

**体素维度选择（Table 12）**：体素尺寸128×128×32在感知损失上达到0.2237，优于更小尺寸的配置。该配置在表示能力与计算开销之间取得平衡。

**潜在下采样因子（Table 13）**：下采样因子ds=4时体素重建损失最低（0.4915），表明适度的压缩率对潜在自编码器的重建保真度至关重要。

**直接扩散模型拟合消融（Figure 14）**：直接在128×128×32体素网格上训练扩散模型（不经过潜在自编码器压缩）的生成结果质量较差，验证了LAE压缩步骤的必要性。

**后优化方法消融（Figure 27）**：对比了无后优化、classifier-free guidance后优化和负向导引后优化的效果。负向导引在质量提升和风格控制方面表现更优。

### 应用验证

**BEV条件生成与编辑（Figure 9）**：通过编辑BEV分割图可实现可控场景生成，如添加树木（绿色区域）或移动车辆位置（蓝色区域）。这验证了全局潜在g对场景布局的编码能力。

**3D场景编辑（Figure 11）**：通过对3D粗潜在c的局部区域重采样，结合重建引导，可实现场景的局部编辑，展示了分层潜在空间的解耦特性。

**后优化质量与风格迁移（Figure 10）**：使用SDS后优化可提升生成样本质量，或通过条件于“傍晚场景”实现风格修改。文本引导风格迁移（Figure 31）进一步展示了该机制的灵活性。

### 失败模式与局限性

1. **训练与采样效率**：三阶段流水线（场景自编码器→潜在自编码器→分层扩散模型）加上后优化步骤，导致训练和采样速度较慢。
2. **体素密度限制**：密集体素网格表示随场景规模增大，体渲染和扩散模型训练成本显著增长，限制了向更大场景的扩展。
3. **数据依赖性**：需要多视图RGB图像和相机位姿作为输入，限制可使用的数据规模。在场景数量有限的数据集（如AVD）上，生成多样性可能不足。
4. **风格编辑的内容保持**：风格化编辑过程中，部分内容（如车辆）可能出现不希望的变化，内容与风格的解耦控制仍需改进。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2304_09787/figures/006_Table_1.jpg]]
*Table 1: FID [22] scores on VizDoom and Replica. NF-LDM outperforms all baseline models. Baseline numbers are from [3]*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2304_09787/figures/008_Table_2.jpg]]
*Table 2: FID [22] scores on Carla and AVD datasets. Baseline models have trouble learning the distribution of complex outdoor datasets, in particular AVD, while NF-LDM models them well*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2304_09787/figures/011_Table_3.jpg]]
*Table 3: FVD [77] scores on Carla and AVD Datasets. As for FID, baseline models have trouble learning to model complex datasets*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2304_09787/figures/013_Figure_9.jpg]]
*Figure 9: BEV-Conditioned Synthesis: NF-LDM allows controllable generation by editing the BEV segmentation map. From the initial sample, we add trees (green) and then edit the location of the car (blue). Note the ego car is at the center and thus not rendered. Table 4. FID [22] on ablating the choice of hierarchy on the Carla dataset. The first column is for training both LAE and LDM only with the coarse latent. The last column is our full model*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2304_09787/figures/017_Table_6.jpg]]
*Table 6: Encoder for the coarse latent c*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2304_09787/figures/018_Table_5.jpg]]
*Table 5: Encoder for the global latent g*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2304_09787/figures/019_Table_7.jpg]]
*Table 7: Encoder for the fine latent f*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2304_09787/figures/020_Table_8.jpg]]
*Table 8: Decoder of the latent auto-encoder*






## 定位与知识库关联

### 核心问题与突破点

现有三维场景生成方法普遍面临**单一全局潜在向量**的表示瓶颈。以**GAUDI**（Bautista et al., 2022）为代表的自解码器与扩散模型结合方法，将整个场景压缩为单个全局潜在码，导致模型难以同时捕捉场景的全局属性（如整体布局、光照）与局部细节（如物体纹理、精细几何）。这一瓶颈在复杂户外场景中尤为突出——当场景包含丰富多变的物体、遮挡关系和视点变化时，单向量表示的信息容量严重不足。

**NeuralField-LDM (NF-LDM)** 的核心突破在于将场景生成重新表述为**分层潜在空间中的条件扩散过程**。其因果机制可概括为：显式体素网格表示 → 三层潜在分解（全局 g、粗糙 c、精细 f）→ 从全局到局部的条件扩散生成。这一设计使模型能够分别建模不同尺度的场景分布：全局潜在 g 捕获场景级别的属性（如天气、整体风格），3D 粗糙潜在 c 编码空间结构，2D 精细潜在 f 补充纹理细节。

### 技术谱系定位

NF-LDM 处于**显式神经场表示**与**分层扩散生成**的交叉点，其方法谱系可从三个维度定位：

**场景表示维度**：区别于隐式 NeRF 方法（如 **GRAF** 、**π-GAN** ）和 2D 特征图条件方法（如 **GSN** ），NF-LDM 采用显式密度与特征体素网格作为中间表示。这一选择借鉴了 **Lift-Splat-Shoot**（Philion & Fidler, ECCV 2020）的多视图融合思想，但将其扩展为完整的生成框架。显式体素网格的优势在于便于后续的潜在压缩与分层建模，但也带来了随规模增长的计算成本问题。

**潜在空间设计维度**：与 GAUDI 的单向量潜在空间形成鲜明对比，NF-LDM 的潜在自编码器（LAE）将体素网格分解为三个层次：KL 正则化的 1D 全局潜在 g、向量量化的 3D 粗糙潜在 c 和 2D 精细潜在 f。这种设计使生成模型的条件依赖关系呈现为 $p(V,g,c,f) = p(V|g,c,f) \, p(f|g,c) \, p(c|g) \, p(g)$ 的链式结构，每个扩散模型仅需在其对应尺度上建模条件分布。

**生成范式维度**：NF-LDM 采用三阶段流水线（场景自编码器 → 潜在自编码器 → 分层扩散模型），并引入后优化阶段（Score Distillation Sampling, SDS）进一步提升质量。这与端到端 GAN 方法（如 **EG3D** ）形成对比——GAN 通常训练更快但模式覆盖有限，而扩散模型在生成多样性上更具优势，但采样速度较慢。

### 适用边界与局限

**数据依赖**：NF-LDM 需要多视图 RGB 图像及对应相机位姿作为训练输入，这限制了可使用的数据规模。在场景数量较少的数据集（如 AVD）上，生成多样性可能不足。此外，部分基线方法（GRAF、π-GAN）未使用深度信息，而 NF-LDM 利用了深度监督，这可能影响比较的公平性。

**计算开销**：三阶段流水线和层次结构增加了训练与采样时间。密集体素网格表示随场景规模增大，体渲染和扩散模型训练成本高昂。消融实验（Figure 14）表明，直接在 $128 \times 128 \times 32$ 体素网格上训练扩散模型（不经过潜在压缩）是困难的，这验证了 LAE 的必要性，但也揭示了当前流水线的复杂性。

**表示能力边界**：体素尺寸消融（Table 12）显示 $128 \times 128 \times 32$ 在感知损失上达到 0.2237，优于较小尺寸，但更大尺寸的可行性受限于计算资源。潜在下采样因子 $ds=4$ 时体素重建损失最低（0.4915，Table 13），表明当前设计在压缩率与重建质量之间存在权衡。

### 开放问题

1. **表示效率**：如何探索更高效的稀疏体素表示（如八叉树、哈希网格）以扩展到更大场景，同时保持分层潜在分解的优势？
2. **数据效率**：能否减少对多视图数据的依赖，实现单视图或少视图的场景生成？这可能需要更强的 3D 先验或跨场景知识迁移。
3. **生成多样性**：在有限场景数量的真实世界数据上，如何进一步提高生成多样性？这可能涉及数据增强策略或更有效的潜在空间正则化。
4. **内容保持**：后优化阶段（SDS）在风格化编辑中可能导致内容漂移（如车辆形态改变），如何在风格迁移与内容保持之间取得更好的平衡？
5. **采样加速**：层次结构天然导致串行采样，能否通过一致性模型、蒸馏等方法加速推理，使方法更适用于交互式应用？



## 原文 PDF

![[paperPDFs/CVPR_2023/NeuralField_LDM_Scene_Generation_with_Hierarchical_Latent_Diffusion_Models.pdf]]
