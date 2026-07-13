---
title: "Spectrum from Defocus: Fast Spectral Imaging with Chromatic Focal Stack"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Spectrum_from_Defocus_Fast_Spectral_Imaging_with_Chromatic_Focal_Stack.pdf
project_link: "https://nubivlab.github.io/spectrum_from_defocus/"
code_link: null
aliases:
- SFDS
- SFDFSICFS
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 利用两片市售透镜引入天然色差，通过移动透镜产生波长依赖的离焦编码，在保持高光子通过率的同时构建结构化感知矩阵，替换色散/滤光与复杂光学。
primary_logic: 可见光自然光谱的低秩特性使高光谱图像可投影到低维本征空间；色差引起的结构化模糊构成良态前向模型，搭配分块频域快速求逆与即插即用深度去噪，首次以极简光学和亚秒级计算实现高质量物理驱动重建。
claims:
- 在Harvard数据集30张图像上，SfD仅用4个光学元件即获得PSNR 30.81 dB、SSIM 0.92、SAM 7.35°，整体质量优于包括KRISM和MST在内的全部9种对比方法，重建时间仅0.64秒。
- 模拟低光条件下（总曝光2.9秒），SfD的优势进一步扩大，证明其光子效率带来的鲁棒性。
- 实物原型对Macbeth ColorChecker的重建平均PSNR为29.54 dB，SAM为7.42°，验证了真实色差编码的可恢复性。
- 算法利用光谱低秩投影与BCCB快速求逆将重建时间从数十分钟量级降至亚秒级；深度去噪器显著优于L1正则化。
---

# Spectrum from Defocus: Fast Spectral Imaging with Chromatic Focal Stack

> [!tip] 核心洞察
> 可见光自然光谱的低秩特性使高光谱图像可投影到低维本征空间；色差引起的结构化模糊构成良态前向模型，搭配分块频域快速求逆与即插即用深度去噪，首次以极简光学和亚秒级计算实现高质量物理驱动重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | 离焦光谱：基于色差焦栈的快速光谱成像 |
| 英文题名 | Spectrum from Defocus: Fast Spectral Imaging with Chromatic Focal Stack |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2503.20184) · [Project](https://nubivlab.github.io/spectrum_from_defocus/) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | Spectrum from Defocus (SfD) |
| Dataset | Harvard dataset |

> [!tip] 效果简介
> - Harvard dataset (30 images, 5 s total exposure) 上，PSNR(dB)/SSIM/SAM(°) 30.81 / 0.92 / 7.35 vs MST 30.62 / 0.92 / 9.33 (次优综合性能) (PSNR +0.19, SAM -1.98)。

## 概要

高光谱成像在生物医学、遥感、食品检测等领域需求广泛，但传统系统长期面临**空间-光谱-时间分辨率**与**光子效率**之间的根本矛盾：扫描式系统牺牲时间，压缩式系统依赖复杂光学元件（棱镜、编码孔径、滤光片阵列）或沉重计算，而纯数据驱动方法则存在光谱幻觉风险。

**Spectrum from Defocus (SfD)** 提出了一条截然不同的技术路径：利用两片市售透镜的天然色差，通过机械平移透镜采集5帧离焦灰度图像（色差焦栈），将波长信息编码为结构化的离焦模糊。这一设计仅需**4个光学元件**（物镜+可移动透镜+灰度传感器+位移机构），在保持近乎全部入射光子通过率的同时，构建了良态的前向模型。

重建算法的核心洞察在于：可见光自然光谱具有**低秩特性**，可将高光谱图像投影到低维本征空间，大幅压缩未知量维度；色差引起的分块卷积矩阵具有**块循环（BCCB）结构**，使得大规模求逆可在频域快速完成。结合 plug-and-play ADMM 框架与预训练深度去噪器，SfD 首次以极简光学和**亚秒级计算**（0.64秒，NVIDIA RTX A6000）实现了物理驱动的高质量重建。

在 Harvard 数据集30张图像的基准测试中，SfD 以 PSNR 30.81 dB、SSIM 0.92、SAM 7.35° 的综合表现优于包括 **KRISM**（Saragadam et al., TOG 2019）和 **MST**（Cai et al., CVPR 2022）在内的全部9种对比方法。在模拟低光场景（总曝光2.9秒）下，其光子效率带来的优势进一步扩大。实物原型对 Macbeth ColorChecker 的重建（PSNR 29.54 dB, SAM 7.42°）验证了真实色差编码的可恢复性。

方法谱系上，SfD 区别于依赖色散棱镜/滤光片的传统压缩光谱成像（如 **Spectral DiffuserCam**, Monakhova et al., Optica 2020），也不同于基于消色差透镜离焦的超分辨方案（**Spectral DefocusCam**, Foley et al., ICCP 2025）——后者需要定制光学元件且光谱覆盖受限。SfD 以“离焦即编码”的物理机制，在光学复杂度与重建质量之间取得了突破性平衡。



高光谱成像在遥感、农业、文化遗产保护与生物医学等领域具有不可替代的价值，但其实际部署长期受制于一个根本矛盾：**空间分辨率、光谱分辨率与时间分辨率难以同时兼顾**。传统扫描式光谱成像（如Tunable Filter）通过逐波段采集获得高光谱保真度，但牺牲了时间效率；快照式光谱成像试图以单次曝光捕获完整光谱立方体，却不得不在光学复杂度与重建质量之间做出妥协。

### 现有方法的瓶颈

当前主流快照光谱成像系统可归纳为三类范式，各自存在显著局限：

1. **编码孔径快照光谱成像（CASSI）**：通过编码掩模与色散棱镜将三维光谱立方体压缩至二维传感器平面。代表性工作如**Choi et al.**（SIGGRAPH Asia 2017）的混合物理-数据驱动重建，以及**MST**（Cai et al., CVPR 2022）的Transformer架构。这类方法依赖9–20个光学元件，系统复杂且光子通过率低——编码掩模会阻挡约50%的入射光，在低光照条件下性能急剧退化。

2. **衍射/散射编码成像**：如**Spectral DiffuserCam**（Monakhova et al., Optica 2020）利用散射片与光谱滤光阵列实现无镜头压缩成像，**2in1 Cameras**（Shi et al., TOG 2024）则采用分裂孔径结合衍射光学元件。这些方法虽减少了光学元件数量，但散射/衍射过程的光子效率仍然受限，且重建依赖大规模迭代优化，计算耗时通常达数分钟至数十分钟。

3. **Krylov子空间光学计算**：**KRISM**（Saragadam et al., TOG 2019）通过光学实现Krylov子空间投影，在保持光子效率的同时获得结构化编码。然而该系统需要约20个光学元件，硬件实现复杂，且重建质量对光学对准精度高度敏感。

上述方法的共同症结在于：**光学编码与光子效率之间存在根本性权衡**——编码越丰富，通常意味着越多光学元件与越低光子通过率；而追求高光子效率，又往往以牺牲光谱编码多样性为代价。

### 数据驱动方法的风险

近年来，纯深度学习的光谱重建方法（如MST）在特定数据集上取得了令人瞩目的指标。然而，这类方法存在**光谱幻觉（spectral hallucination）**风险：当测试场景的光谱分布偏离训练集时，网络可能生成看似合理但物理上错误的光谱曲线。这在科学测量与工业检测等对光谱精度要求严苛的场景中尤为危险。

### 核心动机与突破口

本文的核心动机在于：**能否以极简光学系统实现光子高效的光谱编码，并通过物理驱动的快速算法完成高质量重建？**

关键洞察来自一个被长期忽视的物理现象——**天然色差（chromatic aberration）**。普通折射透镜对不同波长的光具有不同的焦距，这通常被视为成像缺陷。然而，SfD将这一“缺陷”转化为编码资源：通过移动透镜产生波长依赖的离焦模糊，不同波长的光在传感器上形成差异化的点扩散函数（PSF），构成结构化的感知矩阵。这一策略带来三重优势：

- **光子效率近100%**：无需编码掩模或滤光片，几乎所有入射光子都到达传感器；
- **光学元件仅4个**：两片市售透镜、一个灰度传感器、一个移动机构；
- **编码天然结构化**：色差PSF具有块循环矩阵（BCCB）结构，可在频域快速求逆。

配合可见光自然光谱的低秩特性——高光谱图像可投影至低维本征空间——SfD首次实现了以亚秒级计算（0.64秒）完成物理驱动的高光谱重建，在Harvard数据集30张图像上获得PSNR 30.81 dB、SSIM 0.92、SAM 7.35°的SOTA级性能（Table 1），且在模拟低光条件下（总曝光2.9秒）优势进一步扩大（Fig. 3b），验证了高光子效率带来的鲁棒性。



## 核心方法与创新机理

**Spectrum from Defocus (SfD)** 的核心创新在于将光学系统从“复杂编码”推向“极简编码”，并通过物理驱动的低维重建算法实现亚秒级高光谱成像。其关键创新点可归纳为以下三个维度。

### 1. 光学编码范式：从滤光/色散到天然色差离焦

传统高光谱成像依赖色散棱镜、编码孔径或可调滤光片将光谱维度映射到传感器空间，这不可避免地引入光子损失或增加光学复杂度。SfD 彻底改变了这一范式——**利用市售折射透镜天然存在的色差（chromatic aberration）作为编码机制**。通过沿光轴平移后方透镜，系统在不同位置采集5帧灰度图像，构成**色差焦栈（chromatic focal stack）**：每个透镜位置对应一个特定波长聚焦，其余波长则呈现不同程度的离焦模糊（Fig. 2）。这种波长依赖的结构化模糊天然构成一个良态的感知矩阵，无需任何额外的色散或滤光元件。

从光学元件数量看，SfD 仅需 **4个光学元件**（2片透镜 + 灰度传感器 + 移动机构），而对比方法中 **KRISM** (Saragadam et al., TOG 2019) 需要20个，**MST** (Cai et al., CVPR 2022) 需要9个（Table 1）。更重要的是，由于不使用滤光片或色散元件，SfD **保留了近乎全部的入射光子**，这在高光子效率至关重要的低光场景下带来显著优势——模拟低光条件下（总曝光2.9秒），SfD 的 PSNR 优势进一步扩大（Fig. 3b）。

### 2. 重建算法范式：低秩投影 + 频域快速求逆 + 即插即用去噪

SfD 的算法设计同样体现了“物理先验与数据驱动互补”的创新思路。核心洞察是：**可见光自然光谱具有低秩特性**，高光谱图像可投影到由Harvard数据集光谱主成分矩阵 $\mathbf{P}$ 张成的低维本征空间，从而将未知量维度大幅压缩。在此本征空间中，重建问题被形式化为：

$$\operatorname*{min}_{\mathbf{z}} \frac{1}{2} \| \mathbf{y} - \mathbf{C H P z} \|_{2}^{2} + \Phi_{\theta}(\mathbf{P z})$$

其中 $\mathbf{H}$ 为分块卷积矩阵（由标定的PSF构建），$\mathbf{C}$ 为裁剪矩阵，$\Phi_{\theta}$ 为预训练深度去噪器 **GSANet** 提供的正则项。

算法采用改进的 **plug-and-play ADMM** 框架，交替更新伪测量 $\mathbf{v}$、投影图像 $\mathbf{z}$ 和去噪图像 $\mathbf{u}$。其关键加速技术在于：利用传感矩阵的 **块循环（BCCB）结构**，将每次迭代中的大型矩阵求逆转化为分块频域乘法，从而将重建时间从数十分钟量级压缩至 **0.64秒**（NVIDIA RTX A6000）。消融实验表明，深度去噪器相比传统 L1 正则化显著提升重建质量，验证了数据驱动先验对物理模型的互补作用。

### 3. 系统级协同：极简光学与物理驱动算法的深度耦合

SfD 的创新并非孤立的光学或算法改进，而是二者之间的深度协同：

- **光学为算法提供良态前向模型**：色差引起的结构化模糊并非随机退化，而是可通过 PSF 标定精确建模的确定性过程，这保证了物理求逆的稳定性。
- **算法补偿光学的简约性**：低秩投影与深度去噪弥补了仅5帧测量带来的信息不足，使极简光学系统仍能输出高质量高光谱图像。
- **光子效率与重建速度的双重优势**：高光子通过率使 SfD 在低光条件下鲁棒性突出；频域快速求逆则使系统具备近实时重建能力。

这种“以计算换光学”的设计哲学——用可控的物理编码替代复杂硬件，再用高效物理驱动算法解码——代表了计算成像领域的一个重要方向。



SfD 的完整成像管线由**光学采集**与**计算重建**两大环节构成，二者通过精确标定的色差前向模型紧密耦合，形成“物理编码—快速求逆—数据驱动去噪”的闭环。

### 光学采集：色差焦栈的生成

系统仅使用 4 个光学元件——固定物镜、可移动透镜、灰度传感器及平移机构——完成光谱编码。其核心机制是：利用市售折射透镜固有的纵向色差，通过将后方透镜平移至 5 个离散位置 $z_1, z_2, \ldots, z_5$，使不同波长依次聚焦于传感器平面，而其余波长则呈现不同程度的离焦模糊（Figure 2a）。在每个位置 $z_i$ 采集一帧灰度图像 $I_i$，共 5 帧构成**色差焦栈**（chromatic focal stack）。由于没有引入色散棱镜、滤光片阵列或编码孔径，几乎全部入射光子均被传感器接收，从根本上保证了高光子效率。

采集前需进行一次 PSF 标定：借助窄带可调滤光片，测量各波长-位置对 $(\lambda_j, z_i)$ 的点扩散函数 $K(z_i, \lambda_j)$（Figure 2b）。这些 PSF 构成后续前向模型的核心参数，部署时无需再次使用滤光片。

### 计算重建：物理驱动迭代管线

重建算法接收 5 帧灰度焦栈作为输入，输出 31 通道高光谱图像，其流程可概括为四个模块：

1. **前向模型（式 1）**：将高光谱图像 $\mathbf{x}$ 的每个光谱通道与对应 PSF 的卷积矩阵 $\mathbf{H}_{i,j}$ 进行 2D 卷积，经裁剪矩阵 $\mathbf{C}$ 得到焦栈向量 $\mathbf{y}$：
   $$\mathbf{y} = \mathbf{C H} \mathbf{x}$$

2. **光谱本征投影（式 2）**：利用 Harvard 数据集预计算的光谱主成分矩阵 $\mathbf{P}$，将高维高光谱图像映射至低维本征空间 $\mathbf{z}$，大幅压缩未知量维度，同时利用自然光谱的低秩特性约束解空间：
   $$\min_{\mathbf{z}} \frac{1}{2} \| \mathbf{y} - \mathbf{C H P z} \|_2^2 + \Phi_\theta(\mathbf{P z})$$

3. **Plug-and-Play ADMM 迭代（Algorithm 1）**：将上述目标转化为含松弛变量 $\mathbf{v}, \mathbf{u}$ 的 ADMM 形式（式 3），交替执行三个子步骤：
   - **v-step**（伪测量更新）：以 Wiener 滤波形式从真实测量 $\mathbf{y}$ 和当前投影图像 $\mathbf{z}_i$ 更新 $\mathbf{v}$；
   - **z-step**（投影图像更新）：综合对偶变量与去噪先验，通过频域快速求逆更新 $\mathbf{z}$；
   - **u-step**（去噪）：调用预训练深度去噪网络 **GSANet** 对 $\mathbf{Pz}$ 去噪，提供数据驱动正则。

4. **频域快速求逆**：利用传感矩阵 $\hat{\mathbf{H}} = \mathbf{HP}$ 的块循环（BCCB）结构，将 z-step 中的大型矩阵求逆转化为分块频域逐元素乘法，将单次迭代时间压缩至极低水平，使整体重建在 NVIDIA RTX A6000 上仅需 **0.64 秒**。

重建完成后，根据灰度传感器与可见光滤光片的光谱响应曲线对结果进行最终校正，得到物理量一致的光谱辐亮度图。

### 补充图表

![[assets/figures/papers/paper_list_l2142_https_arxiv_org_abs_2503_20184/figures/001_Figure_1.jpg]]
*Figure 1: The Spectrum from Defocus (SfD) method. (a) Our hardware prototype uses a moving lens to sweep focus through chromatic aberration. (b) SfD achieves state-of-the-art hyperspectral imaging with simple optics and low computational cost. See Table 1 for details. (c) The system captures 5 defocused grayscale images and reconstructs hyperspectral images in under a second*



### 光学采集系统

SfD的光学前端仅由**4个元件**构成：一片固定物镜、一片可移动透镜、一块无内建滤波的灰度传感器，以及驱动透镜平移的移动机构（Figure 2a）。系统利用市售折射透镜的天然色差——不同波长的光在同一透镜位置下聚焦平面不同——通过将后方透镜平移至5个离散位置 $z_1, z_2, \ldots, z_5$，采集一组“色差焦栈”（chromatic focal stack）。在每个位置 $z_i$，对应波长 $\lambda_i$ 的光恰好聚焦，其余波长则呈现不同程度的离焦模糊。这一设计的核心优势在于**不引入色散棱镜、编码孔径或滤光片阵列**，几乎保留了全部入射光子，从根本上缓解了低光子条件下的信噪比瓶颈。

PSF标定阶段借助窄带可调滤光片，测量各波长-位置对 $(\lambda_j, z_i)$ 的点扩散函数 $K(z_i, \lambda_j) \in \mathbb{R}^{K \times K}$（Figure 2b）。部署时，灰度传感器直接记录场景在所有波长上的加权叠加，无需滤光片。

### 前向模型

令高光谱图像 $\mathbf{x} \in \mathbb{R}^{H W C \times 1}$ 为 $C$ 个光谱通道的向量化堆叠，焦栈测量 $\mathbf{y} \in \mathbb{R}^{H W N \times 1}$ 为 $N$ 个透镜位置的向量化堆叠。前向模型为：

$$\mathbf{y} = \mathbf{C H} \mathbf{x} = \mathbf{C} \left[ \begin{array}{ccc} \mathbf{H}_{1,1} & \ldots & \mathbf{H}_{1,C} \\ \vdots & \ddots & \vdots \\ \mathbf{H}_{N,1} & \ldots & \mathbf{H}_{N,C} \end{array} \right] \mathbf{x}$$

其中每个分块 $\mathbf{H}_{i,j} \in \mathbb{R}^{(H+K-1)(W+K-1) \times H W}$ 是由 $K(z_i, \lambda_j)$ 生成的2D卷积矩阵，$\mathbf{C}$ 为裁剪矩阵，将卷积后尺寸大于传感器的边缘部分切除。该模型的关键性质是：**$\mathbf{H}$ 具有块循环（BCCB）结构**，为后续频域快速求逆提供了数学基础。

### 光谱本征投影

可见光自然光谱具有显著的低秩特性。SfD利用Harvard数据集的光谱主成分矩阵 $\mathbf{P} \in \mathbb{R}^{C \times M}$（$M \ll C$），将高光谱图像映射至低维本征空间：$\mathbf{x} = \mathbf{P z}$，其中 $\mathbf{z} \in \mathbb{R}^{H W M \times 1}$ 为低维隐变量。这一投影将未知量维度从 $C$ 压缩至 $M$，大幅降低了逆问题的病态程度。

### Plug-and-Play ADMM迭代重建

重建问题在本征空间中形式化为：

$$\operatorname*{min}_{\mathbf{z}} \frac{1}{2} \| \mathbf{y} - \mathbf{C H P z} \|_{2}^{2} + \Phi_{\theta}(\mathbf{P z})$$

其中 $\Phi_{\theta}$ 为预训练深度去噪网络 **GSANet** 提供的隐式先验。引入松弛变量 $\mathbf{v}$（伪测量）和 $\mathbf{u}$（去噪图像）后，转化为ADMM标准形式：

$$\begin{array}{l} \operatorname*{min}_{\mathbf{z}, \mathbf{u}, \mathbf{v}} \frac{1}{2} \| \mathbf{y} - \mathbf{C v} \|_{2}^{2} + \Phi_{\theta}(\mathbf{u}) \\ \mathrm{s.t.} \quad \mathbf{v} = \hat{\mathbf{H}} \mathbf{z}, ~ \mathbf{u} = \mathbf{z} \end{array}$$

其中 $\hat{\mathbf{H}} = \mathbf{H P}$ 为投影后的等效传感矩阵。ADMM迭代交替执行以下三步更新（Algorithm 1）：

1. **伪测量更新（v-step）**：从真实测量 $\mathbf{y}$ 和当前投影图像 $\mathbf{z}_i$ 通过Wiener滤波更新 $\mathbf{v}$：

   $$\mathbf{v}_{i+1} = (\mathbf{C}^{T} \mathbf{C} + \mu_{1} \mathbf{I})^{-1} (\mathbf{C}^{T} \mathbf{y} + \mu_{1} \hat{\mathbf{H}} \mathbf{z}_{i} - \boldsymbol{\xi}_{i})$$

2. **投影图像更新（z-step）**：综合对偶变量与去噪先验，更新低维投影图像 $\mathbf{z}$：

   $$\mathbf{z}_{i+1} = (\mu_{1} \hat{\mathbf{H}}^{T} \hat{\mathbf{H}} + \mu_{2} \mathbf{I})^{-1} \left( \hat{\mathbf{H}}^{T} (\mu_{1} \mathbf{v}_{i} + \boldsymbol{\xi}_{i}) + (\boldsymbol{\eta}_{i} + \mu_{2} \mathbf{u}_{i}) \right)$$

3. **去噪更新（u-step）**：将 $\mathbf{z}_{i+1}$ 输入预训练的GSANet进行去噪，得到 $\mathbf{u}_{i+1}$。

其中 $\boldsymbol{\xi}$、$\boldsymbol{\eta}$ 为对偶变量，$\mu_1$、$\mu_2$ 为惩罚参数。

### 频域快速矩阵求逆

z-step中 $(\mu_{1} \hat{\mathbf{H}}^{T} \hat{\mathbf{H}} + \mu_{2} \mathbf{I})^{-1}$ 的直接计算代价极高。SfD利用 $\hat{\mathbf{H}}$ 的**BCCB结构**，将该大规模稀疏求逆转化为分块频域乘法：每个光谱本征通道独立地在傅里叶域完成逐元素除法，计算复杂度从 $\mathcal{O}((H W M)^3)$ 降至 $\mathcal{O}(H W M \log(H W))$。这是实现**0.64秒亚秒级重建**（NVIDIA RTX A6000）的核心计算技巧，将重建时间从传统迭代方法的数十分钟量级压缩了三个数量级。

### 光谱响应校正

重建完成后，根据灰度相机与可见光滤光片的光谱响应曲线对结果进行最终校正，确保重建光谱与实际场景的辐射度一致。

### 补充图表

![[assets/figures/papers/paper_list_l2142_https_arxiv_org_abs_2503_20184/figures/002_Figure_2.jpg]]
*Figure 2: Optical design. (a) The system consists of a lens pair in which the second lens is translated to five discrete positions*



## 实验与关键发现

### 主实验：Harvard 数据集定量对比

SfD 在 Harvard 数据集 30 张图像上与 9 种 SOTA 光谱成像系统进行对比，所有模拟均在 5 秒总曝光和各自光学组件效应下完成，计算时间统一在 NVIDIA RTX A6000 上测量。**Table 1** 汇总了核心结果：SfD 取得 PSNR 30.81 dB、SSIM 0.92、SAM 7.35°，PSNR 与 SSIM 均为最优，SAM 仅次于 KRISM（6.75°）但显著优于 MST（9.33°）。值得注意的是，SfD 仅使用 4 个光学元件（两片透镜、传感器、移动机构），而 MST 需要 9 个、KRISM 需要 20 个；重建时间仅 0.64 秒，比多数迭代方法快一个数量级以上。

![[assets/figures/papers/paper_list_l2142_https_arxiv_org_abs_2503_20184/figures/003_Table_1.jpg]]
*Table 1: Comparison of SOTA hyperspectral imaging systems in terms of reconstruction performance, and computational and optical requirements. Reconstruction quality is benchmarked on 30 images from the Harvard dataset [8] under a brightly lit condition with 5- second total exposure time and optical component effects (see supplement). Timings are reported for an NVIDIA RTX A6000. The count of optical components includes: lenses, apertures, prisms, actuators, SLMs, and sensors, but not control electronics*

在模拟低光条件下（总曝光 2.9 秒），SfD 的优势进一步扩大（**Fig. 3b**），PSNR 领先幅度显著增加，直接验证了高光子通过率带来的鲁棒性——色差编码不牺牲光通量，而基于滤光片或编码孔径的系统在低光子条件下信噪比迅速恶化。

### 定性分析与各方法失效模式

**Fig. 3a** 展示了 KAIST 和 CAVE 数据集上的重建示例。Tunable Filter 和 Zhan et al. 因光谱噪声过高而被移至补充材料展示；MST 与 Spectral DefocusCam 表现出较窄的光谱覆盖范围，这源于其训练/标定数据与前向模型的限制。相比之下，SfD 在空间细节和光谱保真度上均表现稳定，尤其在 RGB 同色异谱点（Fig. 3c 中点 5、6）上准确恢复了 RGB 相机无法区分的真实光谱差异。

实物原型对 Macbeth ColorChecker 的重建（**Fig. 4b**）进一步证实了真实色差编码的可恢复性：平均 PSNR 29.54 dB，SAM 7.42°，各色块光谱曲线与地真高度吻合。四个真实场景的逐通道重建（**Fig. 4a**）显示，即使在仅 5 帧离焦灰度测量的条件下，系统仍能忠实恢复空间纹理与光谱内容。

### 消融实验

**测量数量影响（Fig. 5a）**：增加焦栈帧数可稳定提升重建质量，但 RGB 重建在约 5 帧后趋于饱和，而光谱重建仍持续改善。这表明色差编码对光谱信息的积累更为持久——每帧离焦图像携带不同波长的互补编码，多帧叠加可逐步解混光谱维度。

**工作距离鲁棒性（Fig. 5b）**：系统在 264–298 cm 范围内重建稳定，超出此范围 PSNR 逐渐下降。可恢复工作体积约 34 cm，验证了色差编码并非仅对单一物距有效，但工作距离的扩展受限于 PSF 的标定范围与离焦模糊的可逆性。

**深度去噪器 vs. L1 正则化**：补充材料中的消融表明，使用预训练去噪网络 GSANet 替代 L1 正则化可显著提升重建质量，证明数据驱动先验对物理模型的互补作用——物理模型提供结构化前向编码，深度去噪器抑制逆问题中的噪声放大。

### 失败模式与局限性

红色与黑色区域的重建精度相对较低，根本原因在于长波段（红光）色散较弱，导致 PSF 随波长变化不够显著，编码信息不足。此外，系统需要至少 5 帧离焦图像，难以直接用于快速动态场景；深度去噪器在极端低光子条件下仍可能引入轻微光谱失真。PSF 标定依赖窄带滤光片，部署后光学布局固定，缺乏对场景变化的自适应能力。

### 补充图表

![[assets/figures/papers/paper_list_l2142_https_arxiv_org_abs_2503_20184/figures/005_Figure_4.jpg]]
*Figure 4: Results from SfD prototype. (a) We show raw grayscale measurements from the camera, samples from corresponding perchannel reconstruction results, and the aligned ground truth for four real scenes. ∆z indicates the lens displacement relative to the initial position, and sampled channels have an approximate bandwidth of 10nm centered at the displayed wavelength. The reconstructions demonstrate faithful recovery of both spatial details and spectral content. (b) Reconstructed and ground truth spectral curves for each Macbeth color patch*

![[assets/figures/papers/paper_list_l2142_https_arxiv_org_abs_2503_20184/figures/006_Figure_5.jpg]]
*Figure 5: Robust Recovery. (a) Adding measurements improves reconstruction, with performance saturating more quickly in RGB than in spectrum*



## 定位与知识库关联

### 1. 方法谱系：从扫描、编码到离焦编码的演化

SfD 处于压缩光谱成像（Compressive Spectral Imaging）向极简光学与物理驱动重建收敛的技术路径上。其核心贡献在于将“编码”从外部光学元件（色散棱镜、编码孔径、滤光片）迁移到透镜本身的天然色差中，形成波长依赖的结构化离焦模糊作为感知矩阵。

**传统扫描式光谱成像**（Tunable Filter）通过逐波段采集获得完整光谱立方体，光谱精度高但时间分辨率极低，且光子效率随波段数增加而线性衰减，无法适应低光或动态场景。

**编码孔径快照光谱成像（CASSI）** 及后续深度学习方法代表了另一主流范式。**Choi et al.**（SIGGRAPH Asia 2017）提出混合物理-数据驱动的CASSI重建，将深度学习引入压缩光谱重建流程。**MST**（Cai et al., CVPR 2022）进一步采用Transformer架构处理编码孔径测量，在Harvard数据集上取得PSNR 30.62 dB、SSIM 0.92、SAM 9.33°的强基线性能。然而，这类方法依赖9个以上光学元件（含编码孔径、色散棱镜等），且纯数据驱动方法在分布外场景存在“光谱幻觉”风险——网络可能生成看似合理但物理不一致的光谱曲线。

**无镜头与计算光学方法**进一步简化硬件。**Spectral DiffuserCam**（Monakhova et al., Optica 2020）利用散射片与光谱滤光阵列实现无镜头压缩光谱成像，但散射造成显著光子损失。**KRISM**（Saragadam et al., TOG 2019）基于Krylov子空间的光学计算范式，以20个光学元件实现高质量重建，但光学复杂度高。**2in1 Cameras**（Shi et al., TOG 2024）通过分裂孔径与衍射光学元件联合设计，在光学-计算联合优化方向上推进。

**色差离焦的早期探索**为SfD提供了直接前驱。**Zhan et al.**（Photonics 2019）受动物色盲机制启发，尝试利用色差离焦进行光谱重建，但因缺乏结构化前向模型和高效反演算法，重建噪声显著（Fig. 3c补充材料）。**Spectral DefocusCam**（Foley et al., ICCP 2025）利用消色差透镜的离焦实现超分辨光谱成像，但其训练/标定数据限制导致光谱覆盖范围较窄（Fig. 3a标注）。

SfD的关键跃迁在于：将色差离焦从“可感知但难反演”的模糊，转化为具备良态块循环矩阵（BCCB）结构的前向模型，并通过光谱低秩投影将未知量维度压缩至可高效求解的范围。这使得仅需4个光学元件即可在亚秒级时间内完成物理驱动的重建。

### 2. 技术定位与适用边界

**SfD在光谱成像技术谱系中的定位**：
- **光学复杂度**：远低于CASSI/编码孔径方法（4 vs 9–20个元件），仅高于无镜头散射方法
- **光子效率**：无色散/滤光损失，接近全光通量采集，在低光条件下优势显著
- **重建范式**：物理驱动的低秩投影 + plug-and-play深度去噪，区别于纯数据驱动的黑箱方法
- **计算效率**：BCCB频域快速求逆使重建时间降至0.64秒（NVIDIA RTX A6000），优于多数迭代优化方法

**适用边界**：
1. **静态场景为主**：需采集至少5帧离焦图像，帧间场景运动会导致重建伪影。突发摄影与光流补偿是潜在的动态扩展方向。
2. **工作距离受限**：可恢复工作距离约34 cm（264–298 cm范围），超出后PSF失配导致重建质量下降。多尺度PSF标定或自适应光学可扩展工作体积。
3. **长波段编码不足**：红色/黑色区域重建精度略低，根源在于长波段色散较弱导致PSF区分度下降。更换色散更强的玻璃材料或采用高动态范围传感器是直接改进方向。
4. **极端低光子场景**：深度去噪器GSANet虽显著优于L1正则化，但在极端低光子条件下仍可能引入轻微光谱失真。引入更精确的噪声模型（如暗噪声扩散）可进一步提升鲁棒性。

### 3. 局限与开放问题

**已验证局限**：
- 多帧采集机制限制动态场景适用性
- 长波段编码信息不足导致红色/黑色区域精度下降
- 工作距离范围约34 cm，超出后重建质量衰减
- PSF标定依赖窄带滤光片，部署后光学布局固定

**开放问题**：
1. **光学编码增强**：能否通过更换色散更强的玻璃或采用高动态范围传感器提升长波段编码能力？色差特性的主动设计（而非依赖现有透镜的天然色差）可能进一步优化感知矩阵的条件数。
2. **工作体积扩展**：如何将可恢复工作距离扩展至更大范围？多尺度PSF校准、自适应光学元件或联合优化光学-重建参数是可行路径。
3. **动态场景适应**：能否采用突发摄影（burst photography）与光流补偿缓解多帧采集造成的运动模糊？单帧编码（如结合空间变化的色差）是更根本的解决方向。
4. **噪声模型精化**：在极低光条件下引入更精确的噪声模型（如暗噪声扩散、读出噪声）是否能进一步提升重建鲁棒性？当前深度去噪器在训练分布外的噪声特性上可能退化。
5. **跨域推广**：色差离焦编码思想可否推广到近红外或其他光谱域？与三维成像（如深度估计）的联合优化是否可行？色差本身包含深度信息，光谱-深度联合重建是自然延伸。



## 原文 PDF

![[paperPDFs/CVPR_2026/Spectrum_from_Defocus_Fast_Spectral_Imaging_with_Chromatic_Focal_Stack.pdf]]
