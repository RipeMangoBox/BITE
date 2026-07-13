---
title: "GET3D: A Generative Model of High Quality 3D Textured Shapes Learned from Images"
type: paper
paper_level: A
venue: NeurIPS
year: 2022
pdf_ref: paperPDFs/NEURIPS_2022/GET3D_A_Generative_Model_of_High_Quality_3D_Textured_Shapes_Learned_from_Images.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/GET3D/
aliases:
- GET3D
tags:
- NEURIPS_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "结合可微显式表面提取（DMTet）与可微光栅化渲染，使2D对抗训练能够直接优化3D网格的几何与纹理，从而绕过了对3D监督的依赖。"
primary_logic: "通过将DMTet和tri-plane纹理场集成到StyleGAN框架中，并利用高效可微渲染器生成高分辨率2D观察，可以从图像集合中学习复杂3D资产的生成。"
claims:
- "GET3D可以直接生成具有复杂拓扑、丰富几何细节和高保真纹理的显式3D网格。"
- "在ShapeNet的汽车、椅子、摩托车和Turbosquid的动物等多个类别上，GET3D在几何和纹理指标上均大幅超越现有方法。"
- "GET3D生成的几何细节显著优于基线方法。"
- "GET3D生成的纹理清晰度领先于对比方法。"
---

# GET3D: A Generative Model of High Quality 3D Textured Shapes Learned from Images

> [!tip] 核心洞察
> 通过将DMTet和tri-plane纹理场集成到StyleGAN框架中，并利用高效可微渲染器生成高分辨率2D观察，可以从图像集合中学习复杂3D资产的生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GET3D：从图像中学习高质量3D纹理形状的生成模型 |
| 英文题名 | GET3D: A Generative Model of High Quality 3D Textured Shapes Learned from Images |
| 会议/期刊 | NeurIPS 2022 |
| Links | [paper](https://arxiv.org/abs/2209.11163) · [Project](https://nv-tlabs.github.io/GET3D) · [Project](https://research.nvidia.com/labs/toronto-ai/GET3D/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | GET3D |
| Dataset | ShapeNet Car, ShapeNet Chair, ShapeNet Motorbike, Turbosquid Animal |

> [!tip] 效果简介
> - ShapeNet Car 上，COV LFD (%) 为 66.78，对比 51.91 (PointFlow)，变化 +14.87。
> - ShapeNet Chair 上，COV LFD (%) 为 69.08，对比 61.10 (OccNet)，变化 +7.98。
> - ShapeNet Motorbike 上，COV LFD (%) 为 67.12，对比 50.68 (PointFlow)，变化 +16.44。

## 概要

**核心问题**：现有3D生成模型无法直接从2D图像中生成具有复杂拓扑和高保真纹理的显式网格，导致其输出不能直接被标准图形引擎使用。

**核心方法**：GET3D结合可微显式表面提取（DMTet）与可微光栅化渲染，将tri-plane纹理场集成到StyleGAN框架中，使2D对抗训练能够直接优化3D网格的几何与纹理。

**方法定位**：与**PointFlow**（Yang et al., NeurIPS 2019）、**OccNet**（Mescheder et al., CVPR 2019）等仅输出点云或隐式场的方法不同，GET3D直接生成显式纹理网格；与**PiGAN**（Chan et al., CVPR 2021）、**GRAF**（Schwarz et al., NeurIPS 2020）、**EG3D**（Chan et al., CVPR 2022）等3D感知图像合成方法不同，GET3D输出的是可被Blender等图形软件直接使用的网格资产，而非仅支持新视角合成的神经场。

**主要结果**：在ShapeNet的汽车、椅子、摩托车和Turbosquid动物等多个类别上，GET3D在几何指标（COV LFD提升+5.61至+16.44）和纹理指标（FID-3D降低-11.64）上均大幅超越现有方法。

三维内容创作是计算机图形学、影视制作、游戏开发和虚拟现实等领域的核心需求。高质量的三维资产通常需要专业艺术家耗费大量时间进行手工建模和纹理绘制，这一过程成本高昂且难以规模化。因此，能够自动生成具有复杂拓扑结构、丰富几何细节和高保真纹理的三维形状的生成模型，一直是计算机视觉与图形学交叉领域的关键追求。

近年来，生成对抗网络和扩散模型在二维图像生成领域取得了显著进展，能够合成逼真且多样化的图像。然而，将这种生成能力扩展到三维领域面临着根本性的挑战。三维数据本身比二维图像更为稀缺——大规模、高质量的三维模型数据集无论在规模还是多样性上都远不及二维图像数据集。这一数据瓶颈严重制约了依赖三维真值监督的生成模型的发展。

在这一背景下，研究者们探索了多种三维表示和生成范式。早期的工作如 **PointFlow**（Yang et al., NeurIPS 2019）和 **OccNet**（Mescheder et al., CVPR 2019）分别采用点云和隐式占用场来表示三维形状，但这些方法无法生成纹理，且输出的表示形式不能直接被标准图形引擎消费。另一类方法，如 **PiGAN**（Chan et al., CVPR 2021）、**GRAF**（Schwarz et al., NeurIPS 2020）和 **EG3D**（Chan et al., CVPR 2022），通过神经辐射场实现三维感知的图像合成，能够生成多视角一致的二维图像，但其底层表示仍然是隐式的，难以导出可直接用于下游图形管线的显式网格和纹理贴图。

现有方法的核心瓶颈在于：它们要么依赖三维真值监督而受限于数据规模，要么输出隐式表示而无法生成具有复杂拓扑和高保真纹理的显式网格。这一缺口意味着，尽管这些方法在各自设定的指标上取得了进展，但其输出距离实际可用的三维资产仍有显著距离——标准图形引擎需要的是带纹理的显式网格，而非点云、隐式场或仅能用于新视角合成的神经表示。

GET3D 正是在这一背景下提出的。其核心动机是：能否绕过三维真值监督的依赖，直接从二维图像集合中学习生成高质量、带纹理的显式三维网格？这一问题的解决意味着可以利用海量的二维图像数据来训练三维生成模型，从而突破三维数据稀缺的瓶颈，同时输出可直接用于 Blender 等图形软件的标准三维资产。

## 核心方法与创新机理

GET3D的核心创新在于将**可微显式表面提取**与**可微光栅化渲染**深度整合到生成对抗框架中，从而首次实现了从2D图像集合直接生成具有复杂拓扑、丰富几何细节和高保真纹理的显式3D网格。这一突破通过以下三个关键“changed slots”实现：

### 1. 从隐式场到可变形四面体网格的表面表示跃迁

**Baseline状态**：此前的3D生成模型普遍采用隐式场（如**OccNet**（Mescheder et al., CVPR 2019）的占用场）或点云（如**PointFlow**（Yang et al., NeurIPS 2019））作为输出表示。这些表示虽然灵活，但无法直接产生可供图形引擎使用的显式网格，且难以表达尖锐的几何细节和薄壁结构。

**GET3D方案**：引入**DMTet**（可变形四面体网格）作为核心几何表示（Sec 3.1.1）。该模块在一个可变形四面体网格上定义符号距离场（SDF），通过可微的移动四面体算法（marching tetrahedra）直接提取任意拓扑的显式表面网格。具体而言，生成器输出每个顶点的SDF值$s_i$和变形量$\Delta\mathbf{v}_i$，网格面顶点通过SDF值线性插值得到：
$$\mathbf{m}_{i,j} = \frac{\mathbf{v}_i' s_j - \mathbf{v}_j' s_i}{s_i - s_j}$$

**因果机制**：DMTet的可微性使得2D渲染损失能够通过网格顶点直接反向传播到SDF和变形参数，绕过了对3D真值监督的依赖。同时，四面体网格的显式拓扑结构天然支持薄壁和复杂拓扑的生成，这是隐式表示难以实现的。

### 2. 从射线采样到表面点查询的纹理表示革新

**Baseline状态**：3D感知图像合成方法（如**PiGAN**（Chan et al., CVPR 2021）、**GRAF**（Schwarz et al., NeurIPS 2020）、**EG3D**（Chan et al., CVPR 2022））通常沿相机射线密集采样神经辐射场来获取颜色，计算成本高昂且无法直接输出纹理贴图。

**GET3D方案**：采用**tri-plane纹理场**并仅在表面点查询（Sec 3.1.2）。纹理场由三个正交特征平面组成，表面点$\mathbf{p}$的纹理特征通过投影到各平面并双线性插值后聚合得到：
$$\mathbf{f}^t = \sum_e \rho(\pi_e(\mathbf{p}))$$
随后通过轻量级MLP解码为RGB颜色。由于DMTet已提供精确的表面位置，纹理查询仅需在网格顶点处进行，无需沿射线密集采样。

**因果机制**：表面点查询将纹理生成的计算复杂度从体积渲染的$O(N_{\text{rays}} \times N_{\text{samples}})$降至$O(N_{\text{vertices}})$，使得高分辨率纹理生成在计算上可行。同时，tri-plane表示在三个正交方向上解耦了空间信息，提供了比单一体素网格更强的表达能力。

### 3. 从3D监督到2D对抗训练的监督范式转换

**Baseline状态**：传统3D生成模型依赖3D真值（如体素、点云）进行训练，而3D感知图像合成方法虽使用2D图像，但输出的是神经辐射场而非显式网格。

**GET3D方案**：将整个几何-纹理生成管线置于**2D对抗训练**框架下（Sec 3.2）。利用高效可微光栅化器**Nvdiffrast**将生成的网格和纹理渲染为2D RGB图像和剪影，随后通过两个独立的判别器（RGB判别器和剪影判别器）进行对抗训练。总损失函数为：
$$L = L(D_{\text{rgb}}, G) + L(D_{\text{mask}}, G) + \mu L_{\text{reg}}$$
其中$L(D_x, G)$为非饱和GAN损失（带R1梯度惩罚），$L_{\text{reg}}$为SDF符号一致性正则项（Eq 2），用于消除不可见的内面。

**因果机制**：2D对抗训练使模型能够从图像集合中学习3D资产的生成，完全绕过了对昂贵3D标注的依赖。双判别器设计（RGB + 剪影）相比单判别器显著提升了训练稳定性（Figure H消融实验证实），因为剪影判别器为几何生成提供了清晰的形状边界信号，而RGB判别器专注于纹理和外观的逼真度。

### 创新总结

GET3D的三个changed slots形成了紧密耦合的因果链：DMTet提供可微的显式几何提取，tri-plane纹理场提供高效的表面纹理生成，可微光栅化与双判别器对抗训练则将2D图像信号有效传导至3D表示。这一组合使得GET3D在ShapeNet的汽车、椅子、摩托车和Turbosquid动物等多个类别上，在几何指标（COV LFD提升+5.61至+16.44）和纹理指标（FID-3D降低-11.64）上均大幅超越现有方法（Table 2）。

GET3D 的整体生成流程将 3D 纹理网格的生成任务分解为两条并行分支：**几何分支**与**纹理分支**，二者共享输入噪声但拥有独立的潜在映射网络，最终通过可微渲染在 2D 对抗训练中联合优化。

### 输入与潜在空间

生成器从两个独立的高斯噪声向量出发：
- ${\bf z}_1 \sim \mathcal{N}(0, I)$ 用于几何生成
- ${\bf z}_2 \sim \mathcal{N}(0, I)$ 用于纹理生成

每个噪声向量分别经过一个 **Mapping Network** 映射为中间潜在代码 ${\bf w}_1 = f_{\mathrm{geo}}({\bf z}_1)$ 和 ${\bf w}_2 = f_{\mathrm{tex}}({\bf z}_2)$。这种双潜在空间设计使得几何与纹理可以独立控制，为后续的形状插值与局部编辑提供了结构化操作空间（见 Figure 6、Figure 7）。

### 几何生成分支

几何生成器接收 ${\bf w}_1$，输出一个可变形四面体网格上的符号距离场（SDF）与顶点位移。随后，通过 **DMTet**（可微移动四面体）从该 SDF 中提取显式三角网格。DMTet 的核心优势在于：它允许网格拓扑在训练过程中动态变化，从而生成具有任意拓扑的复杂形状（如摩托车的薄壁结构、椅子的镂空靠背）。

提取网格时，对于四面体边上 SDF 符号相异的顶点对，通过线性插值确定网格面顶点位置：
$$\mathbf{m}_{i,j} = \frac{\mathbf{v}_i' s_j - \mathbf{v}_j' s_i}{s_i - s_j}$$
其中 $\mathbf{v}_i'$、$\mathbf{v}_j'$ 为变形后的顶点坐标，$s_i$、$s_j$ 为对应的 SDF 值。

### 纹理生成分支

纹理生成器以 ${\bf w}_1$ 和 ${\bf w}_2$ 为条件，生成一个基于 **tri-plane 表示**的纹理场。该纹理场由三个正交特征平面组成：对于网格表面的任意一点 $\mathbf{p}$，将其投影到三个平面上进行双线性插值，再将三个特征向量求和得到该点的纹理特征 $\mathbf{f}^t$：
$$\mathbf{f}^t = \sum_e \rho(\pi_e(\mathbf{p}))$$
随后，$\mathbf{f}^t$ 经小型 MLP 解码为 RGB 颜色值。

与基于神经辐射场的方法（如 **EG3D**，Chan et al., CVPR 2022）不同，GET3D 的纹理场**仅在表面点处查询**，无需沿射线密集采样，大幅降低了计算开销。

### 可微渲染与对抗训练

几何与纹理分支的输出汇合为一个带顶点颜色的显式网格。该网格通过高效可微光栅化器 **Nvdiffrast** 渲染为 2D 图像和剪影（silhouette）。渲染过程接受相机姿态 $c$ 作为条件，从预设的相机分布（如上半球采样）中随机采样。

训练采用两个独立的判别器：
- **RGB 判别器** $D_{\mathrm{rgb}}$：判别渲染彩色图像的真伪
- **剪影判别器** $D_{\mathrm{mask}}$：判别渲染剪影的真伪

每个判别器使用非饱和 GAN 损失配合 R1 梯度惩罚：
$$L(D_x, G) = \mathbb{E}_{\mathbf{z} \sim N, c \sim C} [g(D_x(R(G(\mathbf{z}), c)))] + \mathbb{E}_{I_x \sim p_x} [g(-D_x(I_x)) + \lambda \|\nabla D_x(I_x)\|_2^2]$$
其中 $x \in \{\mathrm{rgb}, \mathrm{mask}\}$，$g(y) = -\log(1 + \exp(-y))$。

此外，为消除网格内部不可见面，引入基于四面体边 SDF 符号一致性的正则项：
$$L_{\mathrm{reg}} = \sum_{i,j \in \mathbb{S}_e} H(\sigma(s_i), \mathrm{sign}(s_j)) + H(\sigma(s_j), \mathrm{sign}(s_i))$$
其中 $H$ 为交叉熵，$\sigma$ 为 sigmoid 函数。该正则项鼓励同一条边上相邻顶点的 SDF 符号保持一致，从而抑制浮动的内面伪影。

最终生成器的总损失为：
$$L = L(D_{\mathrm{rgb}}, G) + L(D_{\mathrm{mask}}, G) + \mu L_{\mathrm{reg}}$$

### 端到端可微性

整个 pipeline 从噪声输入到 2D 渲染输出是**完全可微的**：DMTet 提供从 SDF 到网格的可微提取，Nvdiffrast 提供从网格到像素的可微光栅化，因此 2D 对抗损失的梯度可以无缝回传至几何与纹理生成器的所有参数。这一设计使得 GET3D 能够仅从 2D 图像集合中学习，无需任何 3D 真值监督。

### 架构演进说明

论文还报告了一个改进版生成器（Ours improved G），其将几何与纹理分支共享同一个骨干网络，在多个类别上取得了进一步的性能提升（见 Table 2）。详细的网络架构配置见附录 Figure B 和 Figure C。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2209_11163/figures/003_Figure_2.jpg]]
*Figure 2: Overview of GET3D: We generate a 3D SDF and a texture field via two latent codes. We utilize DMTet [60] to extract a 3D surface mesh from the SDF, and query the texture field at surface points to get colors. We train with adversarial losses defined on 2D images. In particular, we use a rasterization-based differentiable renderer [37] to obtain RGB images and silhouettes. We utilize two 2D discriminators, each on RGB image, and silhouette, respectively, to classify whether the inputs are real or fake. The whole model is end-to-end trainable. Note that we additionally provide an improved version of our Generator in Appendix A.5 and Fig. C*

### 补充图表

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2209_11163/figures/032_Figure.jpg]]
*Figure: EG3D Ours Ours-Tex Figure O: Additional qualitative comparison on Human Body dataset. We compare our method with EG3D on the extracted geometry*

### 3.1 整体生成流程

GET3D 的生成过程分为两个分支：几何分支和纹理分支。给定从标准高斯分布采样的噪声向量 $\mathbf{z}_1, \mathbf{z}_2 \sim \mathcal{N}(0, I)$，首先通过两个映射网络分别得到几何潜在代码 $\mathbf{w}_1 = f_{\mathrm{geo}}(\mathbf{z}_1)$ 和纹理潜在代码 $\mathbf{w}_2 = f_{\mathrm{tex}}(\mathbf{z}_2)$。几何分支以 $\mathbf{w}_1$ 为条件，通过 DMTet 可微地输出任意拓扑的表面网格；纹理分支以 $\mathbf{w}_1$ 和 $\mathbf{w}_2$ 为条件，生成可在表面点查询的纹理场。整个过程端到端可训练，仅需 2D 对抗损失作为监督信号。

### 3.2 几何生成器：DMTet 可微表面提取

几何生成器的核心是 **DMTet**（Deformable Tetrahedral Grid），一种基于可变形四面体网格的可微表面表示。它在三维空间中维护一个四面体网格，网格的每个顶点 $v_i$ 携带一个 SDF 值 $s_i$ 和一个可学习的变形向量 $\Delta v_i$。生成器以潜在代码 $\mathbf{w}_1$ 为输入，输出每个顶点的 SDF 值和变形量，得到变形后的顶点位置 $\mathbf{v}_i' = \mathbf{v}_i + \Delta \mathbf{v}_i$。

网格面顶点通过 SDF 值的线性插值确定。对于一条四面体边 $(i, j)$，若两端顶点的 SDF 值异号（即 $s_i$ 与 $s_j$ 符号不同），则该边上存在一个网格面顶点，其位置由下式给出：

$$\mathbf{m}_{i,j} = \frac{\mathbf{v}_i' s_j - \mathbf{v}_j' s_i}{s_i - s_j}$$

这一插值过程完全可微，使得梯度可以从最终渲染的 2D 图像一路回传至 SDF 值和顶点变形量，从而在无 3D 监督的条件下学习几何。

### 3.3 纹理生成器：Tri-plane 纹理场

纹理以 **tri-plane 表示** 进行参数化。具体而言，维护三个互相正交的特征平面（如 $xy$、$xz$、$yz$ 平面），每个平面是一个 $N \times N \times C$ 的特征图。对于网格表面上的任意 3D 点 $\mathbf{p}$，将其投影到三个特征平面上，通过双线性插值获取各平面的特征向量，再求和得到该点的纹理特征：

$$\mathbf{f}^t = \sum_e \rho(\pi_e(\mathbf{p}))$$

其中 $\pi_e(\mathbf{p})$ 表示将点 $\mathbf{p}$ 投影到第 $e$ 个特征平面，$\rho(\cdot)$ 为双线性插值操作。聚合后的特征 $\mathbf{f}^t$ 经小型 MLP 解码为 RGB 颜色值。

与基于神经辐射场的方法不同，GET3D 只需在表面点处查询纹理场，而非沿射线密集采样，这显著提升了计算效率。

### 3.4 对抗训练目标

训练使用两个独立的判别器：RGB 判别器 $D_{\mathrm{rgb}}$ 和剪影判别器 $D_{\mathrm{mask}}$。给定生成网格 $G(\mathbf{z})$ 和相机参数 $c$，通过可微光栅化器 Nvdiffrast 渲染得到 RGB 图像和剪影，分别送入两个判别器。两个判别器均采用非饱和 GAN 损失配合 R1 梯度惩罚：

$$L(D_x, G) = \mathbb{E}_{\mathbf{z} \sim \mathcal{N}, c \sim \mathcal{C}} [g(D_x(R(G(\mathbf{z}), c)))] + \mathbb{E}_{I_x \sim p_x} [g(-D_x(I_x)) + \lambda \|\nabla D_x(I_x)\|_2^2]$$

其中 $g(y) = -\log(1 + e^{-y})$ 为 softplus 的负值，$R(\cdot)$ 表示渲染操作，$p_x$ 为真实图像分布。

### 3.5 几何正则化

为消除 DMTet 产生的不可见内面，引入基于四面体网格边的 SDF 符号一致性约束。对每条边 $(i, j)$，要求两端顶点的 SDF 符号一致（即不产生零交叉），除非该边确实穿过表面。正则项形式为交叉熵损失：

$$L_{\mathrm{reg}} = \sum_{i,j \in \mathbb{S}_e} H(\sigma(s_i), \mathrm{sign}(s_j)) + H(\sigma(s_j), \mathrm{sign}(s_i))$$

其中 $\mathbb{S}_e$ 为不应包含零交叉的边集合，$H$ 为二元交叉熵，$\sigma$ 为 sigmoid 函数。该正则项有效抑制了网格内部冗余面的生成。

### 3.6 总损失函数

生成器的完整优化目标为上述各项的加权组合：

$$L = L(D_{\mathrm{rgb}}, G) + L(D_{\mathrm{mask}}, G) + \mu L_{\mathrm{reg}}$$

其中 $\mu$ 为正则项权重。消融实验表明，使用两个独立判别器比单个联合判别器显著减少训练不稳定，而正则项对生成干净的可导出网格至关重要。

## 实验与关键发现

### 数据集与评估协议

GET3D在四个数据集上进行评估：ShapeNet的汽车（Car）、椅子（Chair）、摩托车（Motorbike）类别，以及Turbosquid的动物（Animal）数据集。各数据集的统计信息见Table A。所有方法在相同的数据集划分、相机分布和指标上进行比较，确保公平性。对于不能输出纹理网格的基线方法（如PointFlow、OccNet），统一使用marching cubes或Poisson重建提取几何，并计算FID-3D来反映3D形状质量。

评估指标覆盖几何和纹理两个维度：几何质量用Coverage（COV）和Minimum Matching Distance（MMD）衡量，基于Light Field Descriptor（LFD）和Chamfer Distance（CD）两种度量；纹理质量用FID评估，包括原始2D渲染图像的FID和从3D形状多视图渲染计算的FID-3D。

### 主实验结果

Table 2汇总了GET3D与基线方法的定量对比。在ShapeNet的汽车类别上，GET3D在COV LFD指标上达到66.78%，显著超越PointFlow（51.91%）和OccNet（55.54%）；在FID-3D上达到10.25，大幅领先EG3D的21.89。椅子类别上，GET3D的COV LFD为69.08%，优于OccNet的61.10%。摩托车类别上，GET3D的COV LFD达67.12%，比PointFlow的50.68%提升超过16个百分点。在Turbosquid动物数据集上，GET3D以79.77%的COV LFD超越EG3D的74.16%。

定性对比进一步验证了定量结果。Figure 3展示了各方法提取的3D几何形状，GET3D生成的几何细节显著优于基线方法——汽车、椅子、摩托车和动物类别均展现出更丰富的表面细节和更清晰的拓扑结构。Figure 4的2D渲染图像对比显示，GET3D生成的纹理清晰度和一致性领先于对比方法，尤其在动物毛皮纹理和汽车表面细节上表现突出。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2209_11163/figures/006_Figure.jpg]]

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2209_11163/figures/042_Figure.jpg]]

### 消融实验

**图像分辨率的影响**（Table 3）：将训练图像分辨率从128²逐步提升至1024²，FID从39.21持续下降至10.25，COV和MMD指标也同步改善。这表明高分辨率2D监督信号能有效传导至3D几何和纹理的优化，是GET3D实现高质量生成的关键因素。

**判别器架构设计**：使用两个独立的判别器（RGB判别器和剪影判别器）替代单个联合判别器，显著减少了训练不稳定性。Figure H的训练损失曲线显示，双判别器设计使损失收敛更加平稳，避免了单判别器方案中常见的震荡和模式崩溃。

**体积细分策略**：对于具有薄壁结构的类别（如摩托车），在DMTet基础上增加体积细分（Ours+Subdiv）能进一步细化几何细节。Table 2中摩托车类别的结果显示，体积细分在COV和MMD指标上均带来额外提升。

**相机条件的影响**（Table B）：移除判别器的相机姿态条件仅导致FID轻微下降（-1.38），不影响视觉质量。这说明GET3D的生成质量主要来源于几何和纹理生成器的表达能力，而非对相机条件的过拟合。

### 扩展应用与材料生成

GET3D可扩展至表面材料生成（Section 4.3.1）。通过将纹理场替换为Disney BRDF参数（基色、金属度、粗糙度），并引入基于球面高斯（SG）的可微延迟渲染管线，模型能够生成具有物理材质属性的3D资产。Table E报告了材料生成的定量FID结果，验证了该扩展的有效性。

### 形状插值与编辑

Figure 6展示了在几何和纹理潜在空间中进行插值的结果：从左侧形状平滑过渡到右侧形状，中间插值结果保持几何合理性和纹理一致性。Figure 7展示了局部扰动单个潜在编码产生的形状变化，表明潜在空间具有良好的解耦性和可编辑性。

### 失败模式与局限性

尽管GET3D在整体上表现优异，仍存在以下局限性：

1. **类别特异性训练**：当前模型需要为每个物体类别单独训练，不能跨类别生成，限制了其在大规模多样化数据上的应用。
2. **相机分布假设**：训练时假设相机分布已知（如从上半球采样）且物体位于标准朝向，在真实非受控数据上应用受限。
3. **2D剪影依赖**：训练依赖于地面真实2D剪影。在真实图像中使用预训练分割模型时会引入额外噪声。Table C报告了使用预测剪影时的性能下降情况。
4. **拓扑错误**：生成的网格虽然在视觉上质量较高，但可能仍存在拓扑错误或内面，需要后处理才能用于某些图形管线。论文提出的SDF符号一致性正则项（Eq 2）部分缓解了此问题，但未能完全消除。
5. **噪声相机鲁棒性**：Table C同时报告了在噪声相机条件下的定量结果，显示性能有一定程度下降，表明方法对相机精度存在一定敏感性。

### 补充图表

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2209_11163/figures/004_Table_2.jpg]]
*Table 2: Quantitative evaluation of generation results: ↑: the higher the better, ↓: the lower the better. The best scores are highlighted in bold. MMD-CD scores are multiplied by 103. The results of Ours (improved G) were obtained after the review process by improving the design of the generator network architecture G (see Appendix A.5 for more details)*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2209_11163/figures/007_Figure_5.jpg]]
*Figure 5: Shapes generated by GET3D rendered in Blender. GET3D generates high-quality shapes with diverse texture, high-quality geometry, and complex topology. Zoom-in for details*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2209_11163/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative comparison of GET3D to the baseline methods in terms of generated 2D images. GET3D generates sharp textures with high level of detail*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2209_11163/figures/001_Table_1.jpg]]
*Table 1: Comparison with prior works. (NV: Novel view synthesis.)*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2209_11163/figures/011_Table_3.jpg]]
*Table 3: Ablating the image resolution. ↑: higher is better, ↓: lower is better*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2209_11163/figures/020_Table.jpg]]
*Table: A: Dataset statistics*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2209_11163/figures/024_Table.jpg]]
*Table: B: Ablations on using camera condition: We ablate using camera condition for discriminator. We train the model on Shapenet Car dataset*

## 定位与知识库关联

### 核心定位：从隐式表征到显式网格的生成范式转换

GET3D 的根本贡献在于将 3D 生成模型的输出从“不可直接使用的隐式场或点云”推进到“可直接导入图形引擎的显式纹理网格”。这一转换通过两个关键的技术决策实现：**可微显式表面提取（DMTet）** 和 **可微光栅化渲染**，使模型能够在仅依赖 2D 对抗损失的条件下，直接优化 3D 网格的几何与纹理。

从方法谱系看，GET3D 处于两条研究路线的交汇点：

**路线一：3D 生成模型（输出 3D 资产，但缺乏纹理或显式结构）**
- **PointFlow**（Yang et al., NeurIPS 2019）：基于归一化流的点云生成模型，输出无纹理的点集，需后处理才能转换为网格。
- **OccNet**（Mescheder et al., CVPR 2019）：学习隐式占据场的生成模型，输出为隐式表征，需通过 marching cubes 提取网格，同样无纹理。
- 这些方法依赖 3D 真值监督，且输出不能直接用于标准图形管线。

**路线二：3D 感知图像合成（输出多视角一致图像，但不生成显式 3D 资产）**
- **GRAF**（Schwarz et al., NeurIPS 2020）：基于神经辐射场的 3D 感知 GAN，从 2D 图像学习，但输出为沿射线采样的隐式场，无显式网格。
- **PiGAN**（Chan et al., CVPR 2021）：引入周期激活的隐式辐射场 GAN，同样输出隐式表征。
- **EG3D**（Chan et al., CVPR 2022）：使用 tri-plane 混合表征的高效 3D 感知 GAN，是 GET3D 纹理表征的直接前身，但仍输出隐式场，需密集射线采样。

GET3D 的关键突破在于：将 EG3D 的 tri-plane 纹理表征与 DMTet 的显式几何表征结合，并通过可微光栅化（Nvdiffrast）替代体渲染，使得纹理场只需在表面点查询，大幅降低计算成本。这一设计使 GET3D 成为首个能从 2D 图像集合中直接生成显式纹理网格的 GAN 框架。

### 技术模块的继承与创新

| 模块 | 继承来源 | GET3D 的改进 |
|------|----------|-------------|
| 几何表征（DMTet） | DMTet | 将其集成到 StyleGAN 框架中，与纹理生成器联合训练 |
| 纹理表征（tri-plane） | EG3D（Chan et al., CVPR 2022） | 从体渲染改为表面点查询，与显式网格绑定 |
| 可微渲染 | Nvdiffrast | 用于对抗训练的 2D 监督生成，替代体渲染 |
| 对抗训练框架 | StyleGAN 系列 | 引入双判别器（RGB + 剪影）提升训练稳定性 |
| 材质生成 | Disney BRDF [6, 32] + SG 渲染 | 扩展纹理场到 PBR 材质（基色、金属度、粗糙度） |

### 适用边界与局限

1. **类别特异性训练**：当前模型需为每个物体类别单独训练，无法跨类别生成。这限制了其在多样化场景中的直接应用。

2. **相机分布假设**：训练时假设相机姿态分布已知（如从上半球采样）且物体处于标准朝向。这一假设在真实非受控数据上难以满足，限制了向“in-the-wild”数据的扩展。

3. **对 2D 剪影的依赖**：训练需要地面真实 2D 剪影作为条件。在真实图像场景中，需借助预训练分割模型获取剪影，这会引入额外的噪声和误差。

4. **拓扑与内面问题**：尽管引入了基于四面体网格边的 SDF 符号一致性正则项（Eq. 2），生成的网格仍可能存在拓扑错误或不可见的内面，需要后处理才能用于某些严格的图形管线。

5. **材质生成的局限**：材质扩展目前仅支持 Disney BRDF 的基础属性（基色、金属度、粗糙度），尚未覆盖更复杂的表面属性（如各向异性、透明涂层、次表面散射）。

### 开放问题与后续方向

1. **多类别无条件生成**：如何将 GET3D 扩展到多类别联合训练，使单一模型能够表达类间多样性，同时保持各类别的几何和纹理质量？

2. **真实世界数据适配**：是否可以通过集成实例分割和相机姿态估计模块，将 GET3D 应用于真实世界图像集合？这需要解决剪影噪声和相机分布不确定性带来的训练不稳定问题。

3. **判别器策略优化**：当前双判别器设计虽提升了训练稳定性，但增加了计算开销。能否设计一个两阶段策略——训练初期使用两个判别器，后期合并为单个——以简化训练流程？

4. **材质表征的丰富化**：如何将材质生成推广到更复杂的表面属性模型（如各向异性 BRDF、透明涂层、薄膜干涉），以支持更广泛的材质类型？

5. **几何拓扑的可靠性**：能否引入更强的拓扑正则化或后处理机制，确保生成的网格在任意视角下都没有内面或非流形边，从而直接用于物理仿真等下游任务？

### 在知识库中的位置

GET3D 代表了 3D 生成模型从“隐式场时代”向“显式资产时代”过渡的关键节点。其上承 EG3D 的 tri-plane 表征和 DMTet 的可微表面提取，下启后续工作在显式网格生成、材质合成和真实世界数据适配方面的探索。在方法谱系中，GET3D 填补了“从 2D 图像直接生成可用的 3D 网格”这一空白，为 3D 生成模型的实用化奠定了基础。

## 原文 PDF

![[paperPDFs/NEURIPS_2022/GET3D_A_Generative_Model_of_High_Quality_3D_Textured_Shapes_Learned_from_Images.pdf]]
