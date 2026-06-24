---
title: "3DShape2VecSet: A 3D Shape Representation for Neural Fields and Generative Diffusion Models"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/3DShape2VecSet_A_3D_Shape_Representation_for_Neural_Fields_and_Generative_Diffusion_Models.pdf
project_link: "https://1zb.github.io/3DShape2VecSet/"
code_link: "https://github.com/1zb/3DShape2VecSet"
aliases:
- 33SRNFGDM
tags:
- SIGGRAPH_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 去除潜在向量的显式空间位置，采用固定大小的潜在向量集合，并通过交叉注意力实现从查询点到潜在向量的插值，使表示完全可学习且适配Transformer。
primary_logic: 将径向基函数表示中的显式中心点坐标替换为可学习的潜在向量，并将基于距离的插值替换为基于交叉注意力的相似度计算，从而将形状建模为无空间绑定的令牌集合，完全由数据驱动优化。
claims:
- 表示不再使用显式设计的位置特征，网络可自行编码空间信息
- 保留插值结构但消除显式点坐标，融入交叉注意力
- 形状自编码（从点云重建表面）达到最高水平，IoU 0.965，Chamfer 0.038，F-Score 0.970
- 无条件生成在Surface-FPD上从3DILG的1.89降至0.76，显著优于先前方法
---

# 3DShape2VecSet: A 3D Shape Representation for Neural Fields and Generative Diffusion Models

> [!tip] 核心洞察
> 将径向基函数表示中的显式中心点坐标替换为可学习的潜在向量，并将基于距离的插值替换为基于交叉注意力的相似度计算，从而将形状建模为无空间绑定的令牌集合，完全由数据驱动优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 3DShape2VecSet: 一种用于神经场和生成扩散模型的三维形状表示 |
| 英文题名 | 3DShape2VecSet: A 3D Shape Representation for Neural Fields and Generative Diffusion Models |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://1zb.github.io/3DShape2VecSet/) · [Code](https://github.com/1zb/3DShape2VecSet) · [Project](https://1zb.github.io/3DShape2VecSet/.") |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | 3DShape2VecSet |
| Dataset | ShapeNet（所有55类别）形状自编码, ShapeNet无条件生成（与网格潜在基线对比） |

> [!tip] 效果简介
> - ShapeNet（所有55类别）形状自编码 上，IoU / Chamfer-L1 (×100) / F-Score IoU=0.965, Chamfer=0.038, F-Score=0.970（Point Queries） vs 先前最优方法（OccNet、ConvOccNet、IF-Net、3DILG） (在所有类别上均取得显著提升)。
> - ShapeNet无条件生成（与网格潜在基线对比） 上，Surface-FPD 0.76 (C0=32) vs 3DILG: 1.89; Grid-8³: 5.27 (-1.13 (vs 3DILG))。
> - ShapeNet无条件生成（与点云扩散基线对比） 上，Surface-FPD 0.63 vs PVD: 2.33 (-1.70)。

## 概要

现有三维神经场表示将潜在向量显式绑定在规则网格、不规则网格或三平面等空间坐标上，导致潜在空间结构不紧凑，难以与Transformer高效结合，限制了生成质量与压缩效率。本文提出**3DShape2VecSet**，核心思路是去除潜在向量的显式空间位置，将形状表示为固定大小的无位置潜在向量集合，并通过交叉注意力机制实现从查询点到潜在向量的插值——这一设计将径向基函数表示中的显式中心点坐标替换为可学习的潜在向量，将基于距离的插值替换为基于相似度的注意力聚合，使表示完全由数据驱动优化。

在ShapeNet全部55个类别上，该方法在形状自编码任务中取得最高水平：IoU达0.965，Chamfer-L1为0.038，F-Score为0.970；无条件生成的Surface-FPD从3DILG的1.89降至0.76，降幅达1.13。消融实验表明，增加潜在向量数量（64→512）和压缩通道数（1→64）均可提升重建质量，而输入依赖的点查询策略在所有类别上均优于固定的可学习查询。该方法属于“多潜在向量、全局位置”的神经场表示范畴，为后续潜在扩散模型提供了结构化且紧凑的潜在空间。

## 核心方法与创新机理

### 问题瓶颈：显式空间坐标绑定的根本局限

现有神经场表示方法（如OccNet的全局潜在向量、ConvOccNet的规则网格、3DILG的不规则网格）都将潜在向量显式绑定在三维空间坐标上。这种设计导致三个根本性问题：第一，潜在空间受制于手工设计的位置特征，无法根据数据分布自适应优化空间组织；第二，基于距离的插值机制（三线性插值或RBF核回归）限制了特征聚合的灵活性；第三，显式空间结构使得潜在表示难以与Transformer架构高效结合，因为Transformer天然处理无序集合，而网格结构需要额外的位置编码和结构化处理。

**核心洞察**：将径向基函数（RBF）表示中显式的中心点坐标替换为可学习的潜在向量，并将基于距离的相似度计算替换为基于交叉注意力的自适应相似度计算。这一替换使得形状表示从“空间绑定的特征场”转变为“无空间绑定的令牌集合”，完全由数据驱动优化空间信息编码方式。

### 关键创新槽位替换

相较于基线方法，3DShape2VecSet在四个核心槽位上进行了根本性替换：

**槽位1：潜在空间结构（显式坐标绑定 → 无位置集合）**
基线方法将每个潜在向量绑定在固定的3D坐标上（规则网格点、不规则采样点或三平面交点），而本方法采用固定大小的潜在向量集合$\{\mathbf{f}_i\}_{i=1}^M$，每个向量不与任何显式空间坐标关联。网络可以自主选择以任何形式编码位置信息，不再受手工设计的位置特征限制。

**槽位2：插值机制（距离核函数 → 交叉注意力）**
传统RBF表示通过径向基函数$\phi(\mathbf{x}, \mathbf{x}_i) = \phi(\|\mathbf{x} - \mathbf{x}_i\|)$基于欧氏距离进行插值。本方法保留插值结构但消除显式点坐标，将相似度计算替换为查询点$\mathbf{x}$与潜在向量$\mathbf{f}_i$之间的交叉注意力：
$$\hat{\mathcal{F}}(\mathbf{x}) = \sum_{i=1}^{M} \frac{e^{\mathbf{q}(\mathbf{x})^{\top}\mathbf{k}(\mathbf{f}_i)/\sqrt{d}}}{Z(\mathbf{x},\{\mathbf{f}_i\})} \mathbf{v}(\mathbf{f}_i)$$
其中$\mathbf{q}(\cdot), \mathbf{k}(\cdot), \mathbf{v}(\cdot)$是可学习的线性投影，$Z$为softmax归一化因子。这一替换使相似度计算从固定的几何距离变为可学习的语义相似度。

**槽位3：解码器架构（MLP → Transformer）**
基线方法通常使用MLP直接处理潜在特征并预测占据值。本方法采用Transformer架构：潜在集合先经过多层自注意力块进行内部信息交换，再通过交叉注意力与查询点交互，最后经单层全连接输出占据概率$\hat{O}(\mathbf{x}) = \mathrm{FC}(\hat{\mathcal{F}}(\mathbf{x}))$。Transformer架构天然适配无序集合表示，且能捕获长程依赖。

**槽位4：潜在正则化（无正则化 → VAE式KL正则化）**
引入VAE风格的潜在空间正则化：将编码器输出的$M \times C$维潜在向量投影到均值$\mu$和方差$\sigma$，通过重参数化采样压缩到$M \times C_0$维（推荐$C_0=32$），并施加KL散度损失：
$$\mathcal{L}_{\mathrm{reg}} = \frac{1}{M C_0} \sum_{i=1}^{M} \sum_{j=1}^{C_0} \frac{1}{2} (\mu_{i,j}^2 + \sigma_{i,j}^2 - \log \sigma_{i,j}^2)$$
KL权重设为0.001，在重建质量和潜在空间结构化之间取得平衡，使压缩后的潜在空间适合后续扩散模型训练。

### 管线模块与因果关系

**模块1：点云编码器（输入→潜在集合）**
给定输入点云$\mathbf{X} \in \mathbb{R}^{N \times 3}$，首先通过位置编码映射到高维嵌入$\mathrm{PosEmb}(\mathbf{X})$。编码器提供两种设计：
- **可学习查询编码器**：$\mathrm{Enc}_{\mathrm{learnable}}(\mathbf{X}) = \mathrm{CrossAttn}(\mathbf{L}, \mathrm{PosEmb}(\mathbf{X}))$，使用一组可学习查询向量$\mathbf{L}$通过交叉注意力聚合点云信息。
- **点查询编码器**：$\mathrm{Enc}_{\mathrm{point}}(\mathbf{X}) = \mathrm{SelfAttn}(\mathrm{CrossAttn}(\mathrm{Downsample}(\mathrm{PosEmb}(\mathbf{X})), \mathrm{PosEmb}(\mathbf{X})))$，直接使用下采样后的点云嵌入作为查询，再经自注意力增强。

消融实验表明，点查询编码器在所有类别上均优于可学习查询编码器，因为输入依赖的查询能更好地保留形状特定信息。

**模块2：KL正则化与压缩**
编码器输出的潜在向量经均值/方差投影后，通过重参数化采样得到压缩潜在集合$\mathbf{z} \in \mathbb{R}^{M \times C_0}$。压缩通道数$C_0$是关键超参数：$C_0=1$时IoU仅0.727，$C_0=64$时升至0.964，但$C_0=32$在重建质量与生成性能（FPD最优）之间取得最佳平衡。

**模块3：自注意力解码器**
压缩后的潜在集合$\mathbf{z}$经过多层自注意力块进行内部信息交换，使每个潜在向量融合全局上下文信息。这一步是Transformer架构的核心优势：潜在向量之间可以自由交互，不受空间距离限制。

**模块4：交叉注意力占据解码器**
对于任意查询点$\mathbf{x}$，通过交叉注意力计算其与所有潜在向量的相似度权重，加权聚合特征后经FC层输出占据概率。解码过程可高效并行处理大量查询点，支持高分辨率表面提取。

**训练路径**：第一阶段训练VAE（编码器+解码器），损失函数为二元交叉熵重建损失与KL散度损失之和。第二阶段固定VAE，在压缩潜在空间$\mathbf{z}$上训练EDM风格的扩散模型：
$$\mathbb{E}_{\mathbf{n}_i \sim \mathcal{N}(\mathbf{0}, \sigma^2 \mathbf{I})} \frac{1}{M} \sum_{i=1}^{M} \| \mathrm{Denoiser}(\{\mathbf{z}_i + \mathbf{n}_i\}, \sigma, C)_i - \mathbf{z}_i \|_2^2$$
去噪网络由多个去噪层堆叠而成，每层包含自注意力块（无条件生成）或自注意力+交叉注意力块（条件生成）。

**推理路径**：从随机噪声开始，经18步去噪采样得到潜在集合$\mathbf{z}$，再通过解码器重建任意分辨率的占据场或提取Marching Cubes网格。

### 关键公式变量含义

在核心交叉注意力解码器公式中：$M$为潜在向量数量（消融实验确定最优值512），$d$为特征维度，$\mathbf{q}(\mathbf{x})$将查询点映射到查询空间，$\mathbf{k}(\mathbf{f}_i)$和$\mathbf{v}(\mathbf{f}_i)$分别将潜在向量映射到键空间和值空间。softmax归一化确保相似度权重和为1，使输出特征具有尺度不变性。最终占据预测$\hat{O}(\mathbf{x})$通过单层全连接将聚合特征映射到$[0,1]$概率值。

## 实验与关键发现

### 形状自编码：重建精度全面超越现有神经场方法

3DShape2VecSet 在 ShapeNet 全部 55 个类别的表面重建任务上取得了当前最优结果（Table 3）。以点查询（Point Queries）配置为例，平均 IoU 达 0.965，Chamfer-L1（×100）仅 0.038，F-Score 达 0.970。相比此前最强的 3DILG（不规则网格潜在表示），IoU 提升约 0.02，Chamfer 降低约 0.01；相比 ConvOccNet（规则网格潜在表示）和 IF-Net（多尺度局部网格），优势更为显著。这一结果表明，去除潜在向量的显式空间绑定、转而采用交叉注意力进行查询-潜在交互，并未损失重建精度，反而使表示更紧凑、更具表达力。

![[assets/figures/papers/paper_list_l9_https_1zb_github_io_3DShape2VecSet/figures/010_Table_3.jpg]]
*Table 3: Shape autoencoding (surface reconstruction from point clouds) on ShapeNet. We show averaged metrics on all 55 categories and individual metrics for the 7 largest categories. We compare with existing representative methods, OccNet (global latent), ConvOccNet (local latent grid), IF-Net (multiscale local latent grid), and 3DILG (irregular latent grid). For our method, we show two different designs. The column Learned Queries shows results of using Eq. (16), while the column Point Queries means we are using a subsampled point set as queries in Eq. (17). The results of Point Queries are generally better than Learned Queries. This is expected because input-dependent queries (Point Queries) are b...*

### 无条件生成：Surface-FPD 大幅降低

在 ShapeNet 无条件生成任务上，3DShape2VecSet 的 Surface-FPD 降至 0.76（C₀=32），而 3DILG 为 1.89，Grid-8³ 为 5.27（Table 6）。相对于 3DILG，FPD 降低了约 60%。与点云扩散模型 PVD（Surface-FPD 2.33）相比，本方法进一步降至 0.63（Table 7），降幅达 73%。这一巨大差距的核心原因在于：PVD 直接在点云上扩散，生成的点云需经额外表面重建步骤，而本方法在结构化潜在空间上扩散，解码器可直接输出高质量占据场，端到端优化消除了中间表示转换的累积误差。

![[assets/figures/papers/paper_list_l9_https_1zb_github_io_3DShape2VecSet/figures/017_Table_6.jpg]]
*Table 6: Unconditional generation on full ShapeNet*

### 类别条件生成：召回率显著优于基线

在类别条件生成任务上，3DShape2VecSet 在 airplane、chair、table、sofa 四个类别上的 Surface-FID 分别为 0.62、0.76、1.19、0.77，显著优于 NeuralWavelet（Table 8）。在额外度量（Precision / Recall / MMD / COV）评估中（Table 9），本方法的召回率大幅领先 AutoSDF、ShapeFormer 和 3DILG，表明生成的形状多样性更好，能覆盖更广泛的真实分布模式。这一优势源于潜在空间经 VAE 正则化后具有连续且结构化的特性，扩散模型更容易学习其分布。

### 关键消融：潜在向量数量 M 与压缩通道 C₀

**潜在向量数量 M** 从 64 增至 512 时，重建 IoU 从 0.916 单调提升至 0.965（Table 4），表明更大的潜在集合能编码更丰富的形状细节。最终选择 M=512 作为精度-效率的平衡点。

**压缩通道 C₀** 从 1 增至 64 时，重建 IoU 从 0.727 提升至 0.964（Table 5），但生成质量并非单调递增：C₀=32 时 Surface-FPD 最优（0.76），C₀=64 时生成质量反而略有下降。这说明过度压缩损害重建，而压缩不足则使潜在空间对扩散模型不够友好。C₀=32 被确定为重建-生成的最佳权衡点。

### 编码器设计选择：点查询优于可学习查询

Table 3 直接对比了两种编码器设计：Point Queries（对输入点云下采样后作为查询）在所有 7 个大类别上均优于 Learned Queries（固定可学习查询向量）。这一结果验证了“查询应依赖于输入内容”的设计直觉——固定的可学习查询无法根据形状变化自适应调整关注区域，而点查询天然提供了与形状表面分布对齐的初始注意力锚点。

### 训练与推理效率边界

KL 正则化权重设为 0.001 时，潜在空间既能保持重建精度，又具备对扩散模型友好的结构性。扩散模型采样仅需 18 步去噪即可生成高质量形状，远少于常规 DDPM 的 1000 步，推理效率较高。但需注意：整体训练采用两阶段策略（先训练 VAE 自编码器，再训练潜在扩散模型），且扩散模型需在 4 张 A100 上训练 8000 轮，计算资源需求较大。

### 适用边界与失败模式

本方法当前仅支持从点云进行编码，未直接端到端处理真实扫描点云（如含噪声、遮挡的 RGB-D 数据）的表面重建，泛化到真实扫描场景需额外适配。生成结果仅包含几何形状，不含纹理和材质属性，限制了在完整 3D 资产生成管线中的直接应用。此外，虽然 18 步去噪已较高效，但在交互式应用中仍有进一步加速空间。这些限制在论文中已明确承认，需在实际部署中加以考虑。

![[assets/figures/papers/paper_list_l9_https_1zb_github_io_3DShape2VecSet/figures/003_Table_2.jpg]]
*Table 2: Generative models for 3d shapes*

![[assets/figures/papers/paper_list_l9_https_1zb_github_io_3DShape2VecSet/figures/004_Table_1.jpg]]
*Table 1: Neural fields for 3D shapes. We categorize methods according to the position of the latents*

![[assets/figures/papers/paper_list_l9_https_1zb_github_io_3DShape2VecSet/figures/015_Table_4.jpg]]
*Table 4: Ablation study for different number of latents ?? for shape autoencoding*

![[assets/figures/papers/paper_list_l9_https_1zb_github_io_3DShape2VecSet/figures/016_Table_5.jpg]]
*Table 5: Ablation study for different number of channels*

## 定位与知识库关联

3DShape2VecSet 的核心贡献在于对神经场表示的**潜在空间结构**这一关键槽位进行了根本性重构。已有方法将潜在向量绑定在显式三维坐标上——**OccNet** (Mescheder et al., CVPR 2019) 使用单个全局潜在向量，**ConvOccNet** (Peng et al., ECCV 2020) 使用规则网格，**IF-Net** (Chibane et al., CVPR 2020) 使用多尺度局部网格，**3DILG** (Zhang et al., NeurIPS 2022) 使用不规则网格——这些方法的核心瓶颈在于：显式空间位置约束了潜在空间的结构紧凑性，使得潜在表示难以与 Transformer 高效结合，限制了生成质量与压缩效率。

本文做出的关键改变是**去除潜在向量的显式空间绑定**，将形状表示为一组固定大小（M=512）的无位置潜在向量集合。这一改变的因果链条清晰：从径向基函数（RBF）表示出发，保留插值结构但消除显式点坐标，将基于欧氏距离的核回归替换为基于交叉注意力的相似度计算（Eq. 13）。这使得网络不再依赖人工设计的位置特征，而是完全由数据驱动学习空间信息的编码方式。这一设计将形状建模转化为一个无空间绑定的令牌集合，天然适配 Transformer 架构的自注意力和交叉注意力机制。

在知识库中的定位，3DShape2VecSet 处于**神经场表示**与**潜在扩散模型**的交汇点。在神经场分类体系中（Table 1），该方法属于“Multiple, Global”类别——拥有多个潜在向量但全局共享，区别于单全局向量（OccNet）和局部绑定向量（ConvOccNet、IF-Net、3DILG）。在生成模型分类中（Table 2），它属于基于扩散模型的场生成方法，区别于基于点云（**PVD**, Zhou et al., ICCV 2021）、体素或网格的扩散方法。

该方法的适用边界明确：当前仅支持从点云进行编码，未直接处理真实扫描点云的重建问题；仅生成几何形状，不包含纹理和材质属性；需要两阶段训练策略（先训练 VAE 再训练扩散模型），训练资源需求较大（4 张 A100 训练 8000 轮）；采样仍需 18 步去噪，推理速度有优化空间。

后续启发方面，该工作打开了若干方向：将无位置潜在集合的思想推广至真实扫描点云的重建和补全任务；扩展表示以包含纹理和材质通道；利用预训练扩散模型的潜在空间实现文本引导的交互式形状编辑（如 Prompt-to-Prompt 范式）；进一步探索潜在向量数量 M 和压缩通道 C₀ 的联合优化，以提升压缩-质量的帕累托前沿。在知识库中，该工作可作为连接神经场表示学习与集合到集合 Transformer 架构的桥梁节点，为后续研究提供可插拔的表示模块。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/3DShape2VecSet_A_3D_Shape_Representation_for_Neural_Fields_and_Generative_Diffusion_Models.pdf]]