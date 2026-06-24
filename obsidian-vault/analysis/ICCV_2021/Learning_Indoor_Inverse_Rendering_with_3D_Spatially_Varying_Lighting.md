---
title: "Learning Indoor Inverse Rendering with 3D Spatially-Varying Lighting"
type: paper
paper_level: A
venue: ICCV
year: 2021
pdf_ref: paperPDFs/ICCV_2021/Learning_Indoor_Inverse_Rendering_with_3D_Spatially_Varying_Lighting.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/inverse-rendering-3d-lighting/
aliases:
- VBIRO
- LIIR3SVL
tags:
- ICCV_2021
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将照明表示为体素化的三维球面高斯（Volumetric Spherical Gaussian），结合基于光线追踪的可微物理渲染器，实现从 LDR 图像到 HDR 体积照明的端到端联合训练。"
primary_logic: "利用照明体积的重渲染损失与可见域一致性损失，无需 HDR 监督即可迫使模型推测物理正确的光照，同时体积表达自然捕捉角度和空间高频变化。"
claims:
- "提出的 VSG 表示可以参数化场景表面任意点的出射辐射度，支持视角相关效果和高方向性光源。"
- "通过朗伯可微渲染和反向传播的重渲染损失，模型仅用 LDR 图像端到端预测出 HDR 照明。"
- "在 InteriorNet 上，本方法在反照率、法线、深度和照明预测均超过 NIR 和 Li et al. 等方法。"
- "在真实图像上的虚拟物体插入实验展示了高保真阴影与高频反射，尤其适用于高度镜面物体。"
---

# Learning Indoor Inverse Rendering with 3D Spatially-Varying Lighting

> [!tip] 核心洞察
> 利用照明体积的重渲染损失与可见域一致性损失，无需 HDR 监督即可迫使模型推测物理正确的光照，同时体积表达自然捕捉角度和空间高频变化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 学习具有三维空间变化光照的室内逆向渲染 |
| 英文题名 | Learning Indoor Inverse Rendering with 3D Spatially-Varying Lighting |
| 会议/期刊 | ICCV 2021 |
| Links | [paper](https://arxiv.org/abs/2109.06061); [Project](https://research.nvidia.com/labs/toronto-ai/inverse-rendering-3d-lighting/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | VSG-based Inverse Rendering (Ours) |
| Dataset | InteriorNet (Albedo), InteriorNet (Normals), InteriorNet (Depth), InteriorNet (Lighting) |

> [!tip] 效果简介
> - InteriorNet (Albedo) 上，si-MSE 为 0.0175。
> - InteriorNet (Normals) 上，Angular Error (°) 为 18.40。
> - InteriorNet (Depth) 上，si-MSE 为 0.181。

## 概述

从单张有限动态范围（LDR）图像中恢复完整的三维场景内蕴属性——反照率、法线、深度以及高动态范围（HDR）照明——是计算机视觉与图形学中长期存在的病态问题。其核心瓶颈在于：室内场景的光传输高度复杂，包含空间变化的高频阴影、相互反射和镜面效果，而现有方法普遍将照明简化为二维全局环境贴图或逐像素参量表示，无法准确捕捉这种三维空间与角度上的高频变化，导致虚拟物体插入时缺乏真实的阴影和反射。

本文提出了一种统一的、基于学习的逆向渲染框架，其核心创新是**体素化球面高斯（Volumetric Spherical Gaussian, VSG）照明表示**。该表示将场景表面任意点的出射辐射度参数化为一个三维体素网格，每个体素携带不透明度以及一组球面高斯参数（强度、波瓣轴和锐度），从而天然具备同时表达角度高频细节（如镜面反射方向性）和空间高频变化（如局部阴影）的能力。与此配合，作者设计了一个基于光线追踪的**可微物理渲染器**，采用朗伯反射模型和能量守恒的软剪裁函数，将预测的 HDR 照明体积与内蕴属性联合重渲染为 LDR 图像。

方法的关键洞察在于：通过**重渲染损失与可见域一致性损失**的联合驱动，模型无需任何 HDR 监督信号，仅从 LDR 图像即可端到端地推测物理正确的 HDR 照明。整个框架由四个子模块构成——直接预测模块、照明联合预测模块、可微重渲染模块和联合再预测模块——它们协同工作，使得照明估计与内蕴属性分解相互促进。

在 InteriorNet 基准上，本方法在反照率（si-MSE 0.0175）、法线（角度误差 18.40°）、深度（si-MSE 0.181）和照明预测（PSNR 17.37 dB）等指标上均超越 **NIR**（Sengupta et al., ICCV 2019）和 **Li et al.**（Li et al., CVPR 2020）等方法。在真实图像上的虚拟物体插入实验中，该方法能够生成高保真的投射阴影和高频反射，尤其对高度镜面物体的渲染效果显著优于对比方法（Figure 6, Figure 7）。消融实验进一步证实，联合再预测模块和球面高斯的方向特性对最终性能至关重要。

## 背景与动机

逆向渲染旨在从单张或多张二维图像中恢复场景的内蕴属性（如几何、材质和光照），是计算机视觉与图形学交叉领域的核心问题。其应用涵盖增强现实、虚拟物体插入、场景重光照和三维内容生成。然而，室内场景的逆向渲染面临独特挑战：室内光照通常由多个光源、间接反弹和复杂遮挡构成，呈现强烈的**三维空间变化性**和**角度高频细节**。

现有方法在光照表示上存在根本性瓶颈。以 **NIR**（Sengupta et al., ICCV 2019）为代表的方法将场景光照建模为**全局环境贴图**，隐含假设场景中所有表面点接收相同的光照，无法表达室内常见的局部阴影、空间变化的反射和近场光源效应。**Li et al.**（CVPR 2020）将光照扩展为**二维逐像素球面高斯**，虽能捕捉一定空间变化，但本质上仍是图像空间的二维参数化，缺乏对三维光传输的物理建模，难以准确再现物体插入时的真实阴影和遮挡关系。**Lighthouse**（Srinivasan et al., CVPR 2020）虽然预测三维照明体积，但依赖多视角立体图像作为输入，限制了其在实际单目场景中的适用性。

上述方法的共同缺陷可归结为：**光照表示与物理渲染过程脱节**。环境贴图和逐像素参数化无法自然表达三维空间中光线沿方向传播、被遮挡和累积的物理机制，导致重渲染结果缺乏真实的阴影、反射和角度高频细节。此外，这些方法通常依赖直接监督损失进行训练，缺乏迫使模型推测物理正确光照的自监督机制。

本文的核心动机是：**通过将光照表示为三维体素化的球面高斯（Volumetric Spherical Gaussian, VSG），并耦合基于光线追踪的可微物理渲染器，实现从单张 LDR 图像到 HDR 体积照明的端到端学习**。这一设计的因果逻辑在于：体积表示天然捕捉光线的三维空间分布和方向特性，而可微渲染器使得重渲染损失能够反向传播至光照预测，无需 HDR 真值监督即可迫使模型推测物理一致的光照。最终，该框架能够从单目图像中联合恢复反照率、法线、深度和三维空间变化光照，并在虚拟物体插入任务中产生高保真的阴影和镜面反射效果。

## 核心创新

本工作针对“室内场景逆向渲染”这一任务，在照明表示、渲染器设计以及训练策略三个维度上对现有方法的通用假设做出了实质性改变。其核心创新并非增量式地改进某个组件，而是通过引入**三维体积球面高斯（Volumetric Spherical Gaussian, VSG）照明表示**，并围绕该表示构建**完全物理可微的渲染与联合推理管线**，使模型能够在仅使用单张 LDR 图像的条件下，端到端地恢复出空间变化的高动态范围（HDR）照明。

### 1. 照明表示：从二维环境贴图到三维体积球面高斯

现有室内逆向渲染方法对照明的建模存在本质性局限。**NIR**（Sengupta et al., ICCV 2019）将场景照明抽象为一张全局环境贴图，完全忽略了光源在三维空间中的位置差异，因此无法产生位置相关的阴影和反射。**Li et al.**（Li et al., CVPR 2020）虽然引入了逐像素球面高斯，在一定程度上捕捉了空间变化，但其表示仍附着于二维图像平面，对于视场外光源的建模能力有限，且难以表达光线在三维场景体积内的传输效应。

本文提出的 **VSG 表示**将照明建模为一个 $128^3$ 的三维体素网格。每个体素携带一组物理可解释的参数：不透明度 $\alpha \in [0,1]$，以及一组球面高斯参数——强度 $\mathbf{c} \in \mathbb{R}^3$、波瓣轴 $\boldsymbol{\mu} \in \mathbb{R}^3$ 和锐度控制因子 $\sigma \in \mathbb{R}_+$。给定观察方向 $\mathbf{v}$，体素的出射辐射度由球面高斯波瓣定义：

$$G(\mathbf{v}; \mathbf{c}, \boldsymbol{\mu}, \sigma) = \mathbf{c} \, e^{-(1 - \mathbf{v} \cdot \boldsymbol{\mu}) / \sigma^2}$$

这一公式赋予了每个体素表达**各向异性发光**的能力——波瓣轴 $\boldsymbol{\mu}$ 指向光源方向，$\sigma$ 控制光束的集中程度。当 $\sigma \to 0$ 时，波瓣退化为高方向性的点光源；当 $\sigma$ 较大时，则近似漫射光源。这种设计使得 VSG 能够同时表达从高度镜面反射到柔和漫射的丰富光照效果。

对于场景表面任意一点 $\mathbf{p}$，沿光线方向 $\mathbf{l}$ 入射的辐射度通过体渲染式的 alpha 合成计算：

$$\mathcal{R}(\mathbf{p}, \mathbf{l}, \mathbf{L}) = \sum_{k=1}^{N} \prod_{i=1}^{k-1}(1-\alpha_i) \, \alpha_k \, G(-\mathbf{l}; \mathbf{c}_k, \boldsymbol{\mu}_k, \sigma_k)$$

该公式沿光线路径累加各体素的球面高斯辐射，以前方体素的累积透明度作为权重。这一机制自然地捕捉了**遮挡和光传输的空间变化**——光线穿过的体素越多，后方光源的贡献就越小，从而自动产生空间一致的阴影和渐变光照。

与同样使用三维照明体积的 **Lighthouse**（Srinivasan et al., CVPR 2020）相比，本文的关键区别在于：Lighthouse 需要双目立体图像作为输入，且其体积表示仅存储简单的 RGB 颜色，缺乏方向性建模能力；而 VSG 从单目图像出发，通过球面高斯参数化赋予了体积表达**角度高频细节**的能力。

### 2. 渲染器：从神经近似到物理可微光线追踪

照明表示的升级要求渲染器也必须具备相应的物理准确性。NIR 采用一个“黑箱”神经渲染器，虽然能通过端到端学习补偿照明表示的不足，但其渲染过程缺乏物理可解释性，且容易产生伪影。Li et al. 的方法虽然使用了可微渲染，但仅考虑了预计算的直接光照，忽略了间接光照和体积遮挡效应。

本文设计了一个**基于朗伯反射模型的完全可微物理渲染器**。对于像素 $\mathbf{p}$，其重渲染的 LDR 颜色由下式给出：

$$\tilde{I}_p = \varphi\!\left(\sum_{\mathbf{l} \in \{\mathbf{l}\}_K} \frac{\tilde{A}_p}{\pi} \odot \mathcal{R}(\mathbf{p}, \mathbf{l}, \hat{L}) \, \max(\mathbf{l} \cdot \tilde{N}_p, 0) \, \Delta\Omega\right)$$

其中，$\tilde{A}_p$ 和 $\tilde{N}_p$ 分别为预测的反照率和法线，$\mathcal{R}(\mathbf{p}, \mathbf{l}, \hat{L})$ 沿光线方向查询 VSG 体积获得入射辐射度，$K$ 个采样方向按 Fibonacci 格点分布在半球上。渲染器通过光线追踪直接与 VSG 体积交互，因此**梯度可以从重渲染损失反向传播至照明体积的每一个体素参数**。

为解决 HDR 照明与 LDR 图像之间的动态范围差异，本文引入了一个**能量守恒的软剪裁函数**：

$$\varphi(x) = \begin{cases} x & x \le \tau \\ 1 - (1-\tau)e^{-\frac{x-\tau}{1-\tau}} & x > \tau \end{cases}$$

其中阈值 $\tau = 0.9$。该函数在 $[0, \tau]$ 区间保持线性以保留暗部细节，在 $[\tau, +\infty)$ 区间以指数方式饱和至 1，且在整个定义域上连续可微。这使得 HDR 辐照度可以被稳定地压缩到 LDR 空间，同时保持梯度流的畅通。

### 3. 训练策略：从直接监督到“重渲染-联合推理”闭环

传统方法（NIR、Li et al.）仅依赖对中间表示（反照率、法线等）的直接监督信号，对照明估计的质量缺乏有效的间接约束。本文构建了一个**“预测-渲染-比较-修正”的闭环训练范式**，其核心是**重渲染损失**与**联合再预测模块**的配合。

首先，模型通过 Direct Prediction Module 和 Lighting Joint Prediction Module 获得初始的内蕴属性估计和 VSG 照明体积。随后，可微渲染器根据这些预测重渲染输入图像，并计算与原始输入的差异。这个重渲染误差不仅用于监督照明体积（通过可见域一致性损失和对抗损失），更重要的是，它作为**物理一致性的反馈信号**输入 Joint Re-prediction Module。

Joint Re-prediction Module 的输入包括：原始图像、初始预测、重渲染误差图，以及由照明体积导出的**着色图 $\tilde{S}_p$ 及其对法线的雅可比矩阵**：

$$\tilde{S}_p = \sum_{\mathbf{l}} \mathcal{R}(\mathbf{p}, \mathbf{l}, \hat{L}) \, \max(\mathbf{l} \cdot \tilde{N}_p, 0) \, \Delta\Omega, \quad \frac{\partial \tilde{S}}{\partial \tilde{N}_p} = \sum_{\mathbf{l}} \mathbf{1}_{\mathbf{l}\cdot \tilde{N}_p>0} \, \mathcal{R}(\mathbf{p}, \mathbf{l}, \hat{L}) \otimes \mathbf{l} \, \Delta\Omega$$

着色图编码了当前照明条件下每个像素的明暗信息，而雅可比矩阵则显式地告知网络：法线的微小变化将如何影响着色结果。这种**照明感知的梯度线索**使得联合再预测模块能够利用光照的物理约束来修正反照率和法线——例如，若某区域的重渲染偏暗，且雅可比表明增加法线朝向光源会提亮该区域，则网络可以据此调整法线预测。

训练采用分阶段策略：首先独立训练前两个子模块，然后冻结其权重训练 Joint Re-prediction Module，最后以包含重渲染损失的多任务损失端到端微调全部模块。消融实验证实，移除 Joint Re-prediction Module 会导致反照率、法线和深度指标的全面下降（见 Table 5），而移除照明线索（着色图和雅可比）同样会削弱性能，证明了这一闭环设计的关键作用。

### 创新总结

| 创新维度 | 基线方法 | 本文方法 | 关键机制 |
|---------|---------|---------|---------|
| 照明表示 | 全局环境贴图 / 二维逐像素高斯 | 三维体积球面高斯（VSG） | 体素化各向异性高斯波瓣，角度与空间高频兼备 |
| 渲染器 | 神经黑箱 / 预计算直接光照 | 光线追踪可微朗伯渲染 | 物理正确遮挡，梯度直通照明体积 |
| 训练信号 | 直接监督损失 | 重渲染损失 + 照明雅可比反馈 | 闭环联合推理，无需 HDR 真值监督 |

这三个维度的创新并非孤立存在，而是形成了一条**因果链路**：VSG 表示提供了表达复杂光传输的能力基础，可微物理渲染器使得从 LDR 图像到 HDR 照明的梯度通路成为可能，而闭环训练策略则利用这条通路迫使模型推测出物理正确的三维空间变化光照。

## 整体框架

本文提出一个端到端的学习式逆向渲染框架，从单张 LDR 图像联合估计反照率、法线、深度以及三维空间变化的 HDR 照明体积。整个流水线由四个可微子模块级联构成，形成“初始预测—照明推理—物理重渲染—联合精炼”的闭环结构（Figure 2）：

1. **Direct Prediction Module（直接预测模块）**  
   以单张 RGB 图像 $I$ 为输入，通过编码器-解码器网络同时输出初始的反照率 $\tilde{A}$、法线 $\tilde{N}$、深度 $\tilde{D}$ 以及一个全局光照特征向量 $\tilde{\mathbf{f}}_L$（Eq. 3）。该模块提供后续照明推理和联合优化的先验起点。

2. **Lighting Joint Prediction Module（照明联合预测模块）**  
   将上一步的全局光照特征与由深度引导反投影得到的可见视场局部特征（包含像素颜色、法线、反照率）进行融合，送入 3D UNet 预测完整的 VSG 照明体积 $\hat{L}$（Eq. 5, Figure 3）。该体积以 $128^3$ 分辨率体素化，每个体素包含不透明度 $\alpha$ 及球面高斯参数（强度 $c$、波瓣轴 $\mu$、锐度 $\sigma$），可表达任意表面点的出射辐射度。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2109_06061/figures/003_Figure_3.jpg]]
*Figure 3: Architecture of Lighting Joint Prediction Module. We fuse the unprojected visible FoV information (top) and global scene information (bottom), and process them with a 3D UNet. The output is the Volumetric Spherical Gaussian lighting*

3. **Differentiable Re-rendering Module（可微重渲染模块）**  
   基于朗伯反射模型，使用预测的反照率、法线、深度和照明体积，通过光线追踪和球面高斯 alpha 合成（Eq. 2）计算每个像素的入射辐照度，再经能量守恒的软剪裁函数 $\varphi(\cdot)$（Eq. 7）将 HDR 辐照度压缩为 LDR 像素值 $\tilde{I}_p$（Eq. 6）。整个渲染过程完全可微，使得重渲染损失能够反向传播至照明体积和内蕴属性。

4. **Joint Re-prediction Module（联合再预测模块）**  
   接收原始输入图像、Direct Prediction Module 的初始预测、重渲染图像与误差，以及由照明体积导出的着色 $\tilde{S}_p$ 及其对法线的雅可比 $\partial \tilde{S} / \partial \tilde{N}_p$（Eq. 8），通过卷积网络联合精炼反照率、法线和深度。该模块利用照明线索驱动内蕴属性的优化，消除初始预测中的模糊性和伪影（Figure 4）。

**训练策略** 采用分阶段训练：先单独训练前两个子模块（Direct Prediction + Lighting Joint Prediction），冻结权重后训练 Joint Re-prediction Module，最后将所有模块端到端联合微调。损失函数组合了直接监督损失、重渲染损失、可见域一致性损失和对抗损失，仅需 LDR 图像监督即可迫使模型推测物理正确的 HDR 照明。

### 补充图表

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2109_06061/figures/001_Figure_1.jpg]]
*Figure 1: (f) Specular / Diffuse / Transparent Sphere Insertion (g) Specular Object Insertion Figure 1: From a single image, our model jointly estimates albedo, normals, depth, and the HDR lighting volume. Key to our method is inferring continuous HDR 3D spatially-varying lighting, which is critical in producing high quality virtual object insertion with realistic cast shadows and angular high-frequency details*

## 核心模块与公式推导

本方法围绕**三维空间变化照明体积的预测与物理可微重渲染**构建，由四个子模块级联组成（Figure 2）。核心思想是：先预测场景内蕴属性与照明体积的初始估计，再通过可微渲染反向传播重渲染误差，驱动所有模块联合优化。

### 3.1 直接预测模块 (Direct Prediction Module)

该模块以单张 LDR 图像 $I$ 为输入，输出反照率 $\tilde{A}$、法线 $\tilde{N}$、深度 $\tilde{D}$ 以及全局光照特征向量 $\tilde{\mathbf{f}}_L$ 的初始估计：

$$\tilde{A}, \tilde{N}, \tilde{D}, \tilde{\mathbf{f}}_L = h_{\mathrm{DP}}(I; \Theta_{\mathrm{DP}})$$

此阶段仅提供粗糙的初始猜测，后续模块将利用照明体积的重渲染信号对其进行精化。

### 3.2 照明联合预测模块 (Lighting Joint Prediction Module)

该模块的核心创新在于**体素化球面高斯 (Volumetric Spherical Gaussian, VSG)** 照明表示。与全局环境贴图或二维逐像素参数化不同，VSG 将场景照明建模为 $128^3$ 分辨率的三维体积，每个体素携带一组参数：不透明度 $\alpha \in [0,1]$、强度 $c \in \mathbb{R}^3$、波瓣轴 $\mu \in \mathbb{R}^3$ 和锐度控制参数 $\sigma \in \mathbb{R}_+$。

**球面高斯波瓣**定义了体素在视角 $v$ 下的出射辐射度：

$$G(v; c, \mu, \sigma) = c \, e^{-(1 - v \cdot \mu) / \sigma^2}$$

该公式表明：当观察方向 $v$ 与波瓣轴 $\mu$ 对齐时辐射最强，偏离时呈指数衰减，$\sigma$ 越小波瓣越尖锐（方向性越强）。这一设计使 VSG 能够自然表达从漫射环境光到高度方向性光源的全谱系照明效果。

**入射辐射度合成**通过沿光线方向 $-l$ 的透明度加权累加实现。对于场景表面点 $p$ 沿方向 $l$ 的入射光，沿光线采样 $N$ 个体素，按前后顺序进行 alpha 合成：

$$\mathcal{R}(p, l, L) = \sum_{k=1}^N \prod_{i=1}^{k-1}(1-\alpha_i) \, \alpha_k \, G(-l; c_k, \mu_k, \sigma_k)$$

其中 $\prod_{i=1}^{k-1}(1-\alpha_i)$ 为前 $k-1$ 个体素的累积透过率。该公式在物理上等价于沿光线积分体积辐射，使模型能够捕捉遮挡、间接光照等三维光传输效应。

**模块架构**（Figure 3）：将可见视场 (FoV) 的反投影特征（携带局部图像纹理、法线、反照率信息）与全局光照特征 $\tilde{\mathbf{f}}_L$ 融合，通过 3D UNet 处理，输出完整的 VSG 照明体积 $\hat{L}$。

### 3.3 可微重渲染模块 (Differentiable Re-rendering Module)

该模块以预测的反照率 $\tilde{A}_p$、法线 $\tilde{N}_p$ 和照明体积 $\hat{L}$ 为输入，通过**朗伯反射模型**和光线追踪可微地重渲染 LDR 图像。对于像素 $p$，在 $K$ 个 Fibonacci 球面采样方向 $\{l\}_K$ 上积分入射光：

$$\tilde{I}_p = \varphi\!\left(\sum_{l \in \{l\}_K} \frac{\tilde{A}_p}{\pi} \odot \mathcal{R}(p, l, \hat{L}) \max(l \cdot \tilde{N}_p, 0) \Delta\Omega\right)$$

其中 $\mathcal{R}(p, l, \hat{L})$ 为沿方向 $l$ 的入射辐射度，$\max(l \cdot \tilde{N}_p, 0)$ 为朗伯余弦项，$\Delta\Omega$ 为采样方向对应的立体角。

**HDR 到 LDR 的软剪裁**函数 $\varphi$ 使整个过程可微：

$$\varphi(x) = \begin{cases} x & x \le \tau \\ 1 - (1-\tau) e^{-\frac{x-\tau}{1-\tau}} & x > \tau \end{cases}$$

阈值 $\tau = 0.9$，当辐照度超过阈值时采用指数饱和而非硬截断，保留梯度信号以支持端到端训练。

### 3.4 联合再预测模块 (Joint Re-prediction Module)

该模块利用重渲染误差信号和照明相关的解析梯度，联合精化反照率、法线和深度。关键输入包括**着色 $S_p$ 及其对法线的雅可比**：

$$\tilde{S}_p = \sum_{l} \mathcal{R}(p, l, \hat{L}) \max(l \cdot \tilde{N}_p, 0) \Delta\Omega$$

$$\frac{\partial \tilde{S}}{\partial \tilde{N}_p} = \sum_{l} \mathbf{1}_{l \cdot \tilde{N}_p > 0} \, \mathcal{R}(p, l, \hat{L}) \otimes l \, \Delta\Omega$$

着色 $\tilde{S}_p$ 编码了当前照明下该点的亮度信息，而雅可比 $\frac{\partial \tilde{S}}{\partial \tilde{N}_p}$ 刻画了着色对法线方向的敏感度。将这两者与原始输入、初始预测和重渲染误差拼接，送入精化网络，使模型能够利用照明线索修正内蕴属性的模糊性（例如区分纹理边缘与阴影边界）。

消融实验证实（Table 5, Figure 4）：移除该模块会导致反照率、法线和深度指标全面下降；若不将照明属性（着色及雅可比）输入该模块，性能同样受损，验证了照明线索对内蕴属性推理的关键作用。

## 实验与分析

### 核心定量结果

本文在多个基准数据集上进行了全面评估，涵盖内蕴属性分解和照明估计两大任务。所有对比方法均在相同的 InteriorNet 数据划分上评估，保证了实验的公平性。

**InteriorNet 数据集（合成数据）** 是本文的主要评估平台。Table 1 报告了反照率、法线和深度的定量结果。本文方法在反照率上取得 **si-MSE 0.0175**，法线角度误差 **18.40°**，深度 si-MSE **0.181**，全面超越对比方法。与基于环境贴图的 **NIR**（Sengupta et al., ICCV 2019）和基于逐像素球面高斯的 **Li et al.**（Li et al., CVPR 2020）相比，本文的体素化照明表示与可微物理渲染器在解耦场景属性方面具有明显优势。

Table 2 展示了照明预测的定量评估。本文方法在照明预测上达到 **PSNR 17.37 dB**，显著优于仅使用全局环境贴图的 NIR。值得注意的是，**Lighthouse**（Srinivasan et al., CVPR 2020）虽然也预测三维照明体积，但需要双目立体图像作为输入，而本文方法仅使用单目图像即可达到可比甚至更优的性能。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2109_06061/figures/004_Table_2.jpg]]
*Table 2: Evaluation of lighting on InteriorNet dataset. * indicates use of a stereo pair as input*

**IIW 数据集（真实图像）** 上的反照率评估（Table 3）显示，本文方法取得 **WHDR 18.2** 的成绩。由于 IIW 仅提供稀疏的相对反射率标注，这一结果验证了模型在真实场景中的泛化能力。

**NYUv2 数据集（真实图像）** 上的法线和深度评估（Table 4）进一步证实了模型的泛化性：法线角度误差 **22.95°**，深度 si-MSE **0.2827**。重渲染误差方面（Table 5），本文方法在 InteriorNet 上达到 **MSE 0.89×10⁻²**，在 NYUv2 上达到 **MSE 2.33×10⁻²**。

### 消融实验分析

Table 5 的系统消融揭示了各模块的关键贡献：

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2109_06061/figures/007_Table_4.jpg]]
*Table 4: Evaluation of normals and depth on NYUv2 dataset. Table 5: Quantitative results of re-rendering error*

**联合再预测模块（Joint Re-prediction Module）的必要性。** 移除该模块后，反照率、法线和深度的所有指标均出现明显下降。Figure 4 的定性对比显示，无联合再预测时预测结果存在模糊和伪影，而完整模型可产生更清晰、更准确的内蕴属性。这证明了利用重渲染误差和照明线索进行联合推理的重要性。

**照明属性线索的作用。** 不将着色 $\tilde{S}_p$ 及其对法线的雅可比 $\partial \tilde{S} / \partial \tilde{N}_p$（Eq. 8）输入联合再预测模块会削弱性能。这表明照明相关的解析梯度为法线和反照率的优化提供了有效的物理约束。

**球面高斯表示的优势。** 将 VSG 替换为简单的 RGBα 体积（即每个体素仅存储颜色和不透明度，无方向参数）会显著降低重渲染精度。这验证了 VSG 中球面高斯波瓣的方向特性（Eq. 1）对于捕捉角度高频光照效果（如镜面反射和方向性光源）至关重要。

**真实数据微调的有效性。** 在真实 LDR 全景图上继续训练可进一步提升在 NYUv2 上的重渲染误差，表明域适应策略有助于弥合合成到真实的差距。

**损失函数消融。** Table 2 还包含对光照损失各组成部分的消融。对抗损失 $\mathcal{L}_{\mathrm{adv}}$ 的引入鼓励模型生成更真实的照明细节，而可见域一致性损失 $\mathcal{L}_{\mathrm{nv}}$ 则强制模型在不可见视角下预测物理正确的光照。

### 定性结果与虚拟物体插入

**照明估计的定性对比（Figure 6）。** 本文在场景中插入纯镜面球体，并在每个示例的左下角显示插入位置处的估计环境贴图。与 NIR、Li et al. 和 Lighthouse 相比，本文方法同时产生了角度细节（环境贴图中的高频反射）和带有 HDR 强度的真实投射阴影。NIR 的环境贴图缺乏空间变化性，Li et al. 的逐像素表示难以捕捉远距离光源的阴影一致性，而本文的 VSG 体积表示自然支持空间和角度上的高频变化。

**真实世界图像的照明估计（Figure 7）。** 左侧展示纯镜面物体插入，右侧展示漫反射物体插入。上排为放置在固体表面的物体，下排为在三维空间中自由插入的物体。本文方法在镜面和漫反射场景下均产生更真实的结果，且光照在空间上保持一致。这归因于 VSG 体积表示能够建模场景中不同位置的光照差异（如靠近窗户处更亮，角落处更暗）。

**更多虚拟物体插入效果（Figure 8）。** 从兔子、水壶、推车到扶手椅，本文方法能够为不同材质和几何复杂度的虚拟物体生成逼真的光照交互。

**与 NIR 的内蕴属性定性对比（Figure 5）。** 本文的完全基于物理的照明表示和可微渲染器能够更好地消除歧义，以更少的伪影复现复杂的光照效果。NIR 依赖神经渲染器补偿照明表示的不足，在移除神经渲染后其重渲染误差会进一步增大。

### 失败模式与局限性

尽管本文方法取得了显著进展，仍存在以下局限：

1. **朗伯反射假设。** 渲染过程基于朗伯反射模型（Eq. 6），未考虑镜面反射和更复杂的 BRDF。这可能导致高度镜面的虚拟物体与场景的交互不够真实，因为真实场景中的镜面反射依赖于完整的 BRDF 而非仅漫反射分量。

2. **合成数据训练的泛化瓶颈。** 训练完全依赖 InteriorNet 合成数据集，对真实世界中更复杂的照明条件（如混合光源、散射介质）和材质变化的泛化可能有限。虽然真实数据微调可部分缓解此问题，但域差距仍然存在。

3. **体积分辨率的限制。** 当前 VSG 分辨率为 128³，可能不足以精细捕捉极小或远距离光源（如点光源或窄光束）。对于需要精确阴影边缘的场景，分辨率不足会导致阴影模糊。

4. **深度估计误差的传播。** 由于仅使用单目图像，模型严重依赖预测的深度图进行三维反投影和光线追踪。深度估计的误差会直接传播至照明体积预测和最终的虚拟物体插入效果，尤其在深度不连续区域（如物体边界）更为明显。

5. **静态场景假设。** 当前方法假设场景光照是静态的，未考虑动态物体或可变形光照条件。这限制了其在增强现实等需要实时适应变化光照的应用中的使用。

### 开放性讨论

- 该模型在室外场景（如天空光主导的环境）中的光照估计效果尚未验证，室外场景的光照分布与室内有本质差异。
- 采样光线数量 $K$ 和每条光线的采样点数 $N$ 如何权衡渲染质量与计算开销，文中未给出详细的消融分析。
- 多视角输入能否进一步提升三维体积光照的准确性和稳定性，是一个值得探索的方向。
- 如何将框架扩展至动态场景或变动的光照条件，对于实际部署至关重要。

### 补充图表

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2109_06061/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative results of predicted albedo, normals and depth. The results are GT, our model without Joint Re-prediction (JR) Module and our full model. Joint Re-prediction enables joint reasoning and obtains crisper and more accurate results. Figure 5: Qualitative comparison on predicted albedo, normals and re-rendered image. Our fully physics-based lighting representation and differentiable renderer can better disambiguate and reproduce complex lighting effects with less artifacts*

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2109_06061/figures/010_Figure.jpg]]
*Figure: Image NIR Ours NIR Li et al. *

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2109_06061/figures/005_Table_1.jpg]]
*Table 1: Evaluation of albedo, normals and depth on InteriorNet dataset*

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2109_06061/figures/006_Table_3.jpg]]
*Table 3: Evaluation of albedo on IIW dataset*

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2109_06061/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparison of lighting estimation. We compare insertion of a purely specular sphere, and on the bottom-left of each example displays the estimated environment map at the inserted location. Our method produces both angular details (env. map) and realistic cast shadows with HDR, outperforming all competing methods. (* indicates use of a stereo pair as input. Best viewed zooming in. )*

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2109_06061/figures/011_Figure_7.jpg]]
*Figure 7: Qualitative comparison of lighting estimation on real-world images. We compare purely specular object insertion on the left, and on the right is mostly diffuse object. The top row shows insertion on a solid surface while bottom row shows freely inserted objects in 3D. Our method produces more realistic results in both specular and diffuse settings and is spatially consistent. (Best viewed zooming in. ) Figure 8: Qualitative results of object insertion on real-world images. From left to right, we insert a bunny, kettle, cart and armchair*

## 方法谱系与知识库定位

### 1. 方法谱系：从二维全局照明到三维空间变化照明

本文的核心贡献在于将室内逆向渲染的照明表示从**二维全局/局部参量空间**推进到**三维体积空间**，并辅以物理驱动的可微渲染实现端到端学习。这一演进路径可沿以下三个关键维度追踪：

#### 1.1 照明表示的维度跃迁

| 方法 | 照明表示 | 空间维度 | 方向表达能力 | 输入需求 |
|------|----------|----------|--------------|----------|
| **NIR** (Sengupta et al., ICCV 2019) | 全局环境贴图 | 2D（全景） | 高（隐式） | 单目图像 |
| **Li et al.** (Li et al., CVPR 2020) | 逐像素球面高斯 | 2D（图像平面） | 中（多瓣高斯） | 单目图像 |
| **Lighthouse** (Srinivasan et al., CVPR 2020) | 三维RGBα体积 | 3D（体积） | 低（无方向建模） | 双目立体 |
| **Ours (VSG)** | 体素化球面高斯 | 3D（体积） | 高（每体素多瓣高斯） | 单目图像 |

**瓶颈分析**：NIR 的全局环境贴图假设场景照明在空间上均匀，无法表达室内场景中窗户附近与角落处的光照差异。Li et al. 的逐像素球面高斯虽能捕捉图像平面内的空间变化，但其照明参数附着在二维像素上，缺乏对三维几何的显式建模——当虚拟物体插入到与原始表面不同深度的位置时，无法准确推断该处的入射光照。Lighthouse 率先引入三维照明体积，但其简单的 RGBα 表示无法建模方向性光源（如射灯、阳光束），导致镜面反射和硬阴影的缺失。

本文的 **Volumetric Spherical Gaussian (VSG)** 表示直接填补了这一空白：每个体素不仅存储不透明度 $\alpha$，还包含一组球面高斯参数（强度 $c \in \mathbb{R}^3$、波瓣轴 $\mu \in \mathbb{R}^3$、锐度 $\sigma \in \mathbb{R}_+$），通过 alpha 合成公式沿光线方向累积辐射度：

$$\mathcal{R}(p, l, L) = \sum_{k=1}^N \prod_{i=1}^{k-1}(1-\alpha_i) \alpha_k G(-l; c_k, \mu_k, \sigma_k)$$

这一设计使 VSG 能够同时捕捉**角度高频变化**（通过波瓣锐度 $\sigma$ 控制）和**空间高频变化**（通过体素网格的透明度场），从而支持方向性光源和视角相关效果。

#### 1.2 渲染器的物理忠实度

逆向渲染的一个核心挑战是“鸡与蛋”问题：照明、几何和材质的估计相互耦合。解决这一耦合的关键在于渲染器的物理忠实度——渲染器越接近真实光传输，分解的歧义性越小。

- **NIR** 使用神经渲染器隐式补偿照明表示的不足，虽然提高了重渲染精度，但牺牲了物理可解释性，导致估计的内蕴属性（反照率、法线）可能被渲染器的“黑盒”能力所污染。
- **Li et al.** 使用预计算的直接光照，但未采用完整的光线追踪，限制了其对间接光照和遮挡效果的处理。
- 本文采用基于朗伯反射和光线追踪的**可微物理渲染器**，通过能量守恒的软剪裁函数 $\varphi(x)$ 将 HDR 辐照度可微地映射到 LDR 像素值：

$$\varphi(x) = \begin{cases} x & x \le \tau \\ 1 - (1-\tau) e^{-\frac{x-\tau}{1-\tau}} & x > \tau \end{cases}$$

其中 $\tau = 0.9$。这一设计使梯度可以从重渲染损失反向传播至照明体积和几何预测，形成端到端的物理约束。

#### 1.3 训练策略的闭环设计

本文的训练策略将逆向渲染从“开环预测”升级为“闭环推理”。四个子模块形成两个反馈回路：

1. **重渲染回路**：Direct Prediction Module → Lighting Joint Prediction Module → Differentiable Re-rendering Module → 重渲染损失反向传播至照明体积
2. **联合精炼回路**：Joint Re-prediction Module 接收重渲染误差、着色 $S_p$ 及其对法线的雅可比 $\frac{\partial S}{\partial N_p}$ 作为输入，联合优化反照率、法线和深度

着色对法线的雅可比是关键的物理线索：

$$\frac{\partial \tilde{S}}{\partial \tilde{N}_p} = \sum_{l} \mathbf{1}_{l\cdot \tilde{N}_p>0} \mathcal{R}(p, l, \hat{L}) \otimes l \Delta\Omega$$

它显式地编码了“改变法线方向如何影响表面接收的光照”，使法线估计不再仅依赖图像外观，而是受到物理一致性的约束。

### 2. 知识库定位：该方法的适用边界与局限

#### 2.1 适用场景

- **室内静态场景**：方法在 InteriorNet 合成数据集上训练和验证，场景类型以室内居住和办公空间为主，包含窗户、灯具、家具等典型元素。
- **LDR 输入到 HDR 照明**：仅需单张 LDR 图像即可恢复 HDR 照明体积，适用于消费级相机拍摄的室内照片。
- **虚拟物体插入**：尤其适合高度镜面物体（如金属球、陶瓷器具）的插入，因为 VSG 的方向特性可以产生逼真的高光反射和阴影（见 Figure 6、Figure 7）。
- **空间一致性要求高的应用**：由于照明体积覆盖整个场景空间，在不同位置插入物体时可保持光照的空间一致性。

#### 2.2 明确局限

根据论文提供的证据和实验设置，以下局限需要关注：

1. **朗伯反射假设**：渲染器仅建模漫反射（朗伯模型），未考虑镜面反射和更复杂的 BRDF。这意味着：
   - 场景本身的高光反射（如地板反光、金属表面）无法被准确分解
   - 虚拟镜面物体的插入效果依赖于 VSG 的方向表达能力，但场景材质估计仍为纯漫反射
   - *需要手动验证*：论文未提供在非朗伯场景上的定量评估

2. **合成数据依赖**：训练完全依赖 InteriorNet 合成数据集。虽然在 NYUv2 真实数据上进行了评估（Table 4），但泛化能力受限于合成-真实域差异。消融实验表明，在真实 LDR 全景图上微调可进一步提升重渲染精度（Table 5），暗示合成数据训练的模型在真实场景中存在性能退化。

3. **体积分辨率限制**：VSG 分辨率为 $128^3$，对于典型室内场景（假设 $5m \times 5m \times 3m$），每个体素边长约 $4cm$。这足以捕捉窗户、灯具等大面积光源，但可能不足以精细表示：
   - 小型高亮光源（如 LED 灯珠）
   - 远距离光源的锐利阴影边界
   - *需要手动验证*：论文未提供不同体积分辨率的消融实验

4. **单目深度估计的误差传播**：方法仅使用单张图像，严重依赖 Direct Prediction Module 预测的深度图来构建可见表面体积和进行光线追踪。深度估计误差（InteriorNet 上 si-MSE 为 0.181）会直接传播至：
   - 照明体积的初始化（可见视场投影）
   - 重渲染时的光线-表面交点计算
   - 虚拟物体插入时的遮挡关系

5. **静态场景假设**：当前方法假设场景光照和几何在拍摄时刻是静态的，未考虑动态物体（如移动的人）或可变形光照（如开关灯、窗帘变化）。

### 3. 开放问题

以下问题在论文中未被充分探讨，值得后续工作关注：

1. **室外场景的泛化**：VSG 表示是否能有效建模室外场景的天空光、太阳直射等大面积远距离光源？室外场景的照明体积可能需要更大的空间范围和不同的先验约束。

2. **采样效率与质量的权衡**：论文使用 $K$ 条 Fibonacci 格点分布的照明方向进行重渲染，每条光线采样 $N$ 个体素。$K$ 和 $N$ 的选择如何影响渲染质量与计算开销？是否存在自适应采样策略？

3. **多视角输入的增益**：Lighthouse 使用双目立体输入，本文仅用单目。若将 VSG 框架扩展至多视角输入，是否能显著提升照明体积的准确性和空间稳定性？

4. **动态场景扩展**：如何将三维照明体积的预测扩展至动态场景？是否需要引入时间维度的照明体积（4D VSG）或光流引导的照明传播？

5. **非朗伯材质的联合估计**：若将渲染器升级为支持镜面反射的 microfacet 模型，是否能在不增加歧义性的前提下同时估计材质粗糙度和金属度？这需要更强的约束或额外的监督信号。

6. **真实世界 HDR 照明的定量评估**：当前照明评估依赖重渲染误差（间接指标）或合成数据的 GT 照明（Table 2）。在真实场景中，如何获取 HDR 照明体积的 ground truth 以进行直接评估？

## 原文 PDF

![[paperPDFs/ICCV_2021/Learning_Indoor_Inverse_Rendering_with_3D_Spatially_Varying_Lighting.pdf]]
