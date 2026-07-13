---
title: "MicroFM: Physics-guided Flow Matching for Isotropic Microscopy Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MicroFM_Physics_guided_Flow_Matching_for_Isotropic_Microscopy_Reconstruction.pdf
project_link: null
code_link: null
aliases:
- MicroFM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: MicroFM 引入三个关键干预变量：1) 使用 SFE-Net 从轴向图像盲估计仪器匹配、空间变化的物理 PSF，并用于合成逼真的训练配对，大幅缩小仿真与真实退化差距；2) 预训练连续隐式神经表示 (INR) 编码体积几何先验，为每个切片提供跨平面加权聚合的形态学引导；3) 采用一致性流匹配 (Consistency Flow Matching) 框架，...
primary_logic: 物理引导的退化合成与体积隐式几何上下文协同作用，使流匹配网络能够准确学习各向异性到各向同性的逆映射；同时，从观测锚定流动起点有效减少了生成式模型常见的幻觉，在保真度和感知质量上均取得突破。
claims:
- MicroFM 在四个荧光显微镜系统的四个数据集上均达到最先进性能，在 Dense neuron cluster 数据集上 PSNR 达 40.186 dB，SSIM 达 0.964，显著优于所有代表基线方法。
- 消融研究证明，将物理 PSF 替换为高斯核导致 PSNR 下降约 22%，SSIM 下降 13%，直接验证了物理退化匹配的必要性。
- 从低质量观测（而非纯噪声）开始流匹配过程，将 PSNR 从 32.614 提升至 40.186，SSIM 从 0.889 提升至 0.964，表明观测锚定有效减少幻觉。
- Dense neuron cluster (CS-fMOST) 上 PSNR↑ (dB) / SSIM↑ / LPIPS↓ = 40.186 / 0.964 / 0.075
---

# MicroFM: Physics-guided Flow Matching for Isotropic Microscopy Reconstruction

> [!tip] 核心洞察
> 物理引导的退化合成与体积隐式几何上下文协同作用，使流匹配网络能够准确学习各向异性到各向同性的逆映射；同时，从观测锚定流动起点有效减少了生成式模型常见的幻觉，在保真度和感知质量上均取得突破。

| 字段 | 内容 |
|------|------|
| 中文题名 | MicroFM：物理引导的流匹配显微各向同性重建 |
| 英文题名 | MicroFM: Physics-guided Flow Matching for Isotropic Microscopy Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhan_MicroFM_Physics-guided_Flow_Matching_for_Isotropic_Microscopy_Reconstruction_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MicroFM |
| Dataset | Dense neuron cluster, Mouse Kidney |

> [!tip] 效果简介
> - Dense neuron cluster (CS-fMOST) 上，PSNR↑ (dB) / SSIM↑ / LPIPS↓ 40.186 / 0.964 / 0.075 vs 所有对比方法中最佳 (具体值见表2，本文摘要未完整列出) (显著提升 (SOTA))。
> - Mouse Kidney (Two-photon) 上，PSNR↑ / SSIM↑ 33.005 / 0.946 vs 未明确提供 (见表2) (达到或超过所有基线)。

## 概要

三维荧光显微镜是生命科学研究的核心工具，但高保真各向同性成像通常需要缓慢、昂贵的逐层扫描，在活体样本上还会引起光毒性。低成本、快速的替代方案是采集稀疏轴向切片后通过计算重建恢复各向同性分辨率。然而，现有深度学习方法面临两个根本性瓶颈：**合成训练数据依赖固定高斯核模拟轴向模糊**，忽略了真实光学系统中空间变化的点扩散函数（PSF）、像差和样本引入的退化差异，导致合成-真实域严重失配；**二维切片独立处理缺乏显式三维几何约束**，常引起跨切片结构形态失真。

针对上述问题，本文提出 **MicroFM**——一种物理引导的流匹配显微各向同性重建框架。其核心思路是将仪器匹配的物理 PSF 估计与体积隐式几何先验协同引入一致性流匹配生成过程，实现从各向异性观测到各向同性体积的高保真逆映射。具体而言，MicroFM 引入三个关键干预变量：

1. **物理 PSF 预测**：利用 SFE-Net 从轴向图像盲估计空间变化的仪器特定 PSF，并以此合成逼真的训练配对，大幅缩小仿真退化与真实光学退化之间的差距。
2. **体积几何先验**：预训练连续隐式神经表示（INR）编码各向同性体积场，通过跨切片高斯加权聚合为每个轴向切片提供形态学引导，弥补二维独立处理的几何缺失。
3. **观测锚定的流匹配**：将概率流起点从纯噪声改为低质量观测与体积先验的凸组合，使生成过程从观测出发，有效抑制幻觉，同时保证快速、稳定的采样重建。

实验覆盖四种荧光显微镜系统和多种组织类型。在 Dense neuron cluster 数据集上，MicroFM 达到 PSNR 40.186 dB、SSIM 0.964，显著优于 **Self-Net**（Ning et al., Light: Science & Applications 2023）、**SSAI-3D**（Han et al., Nature Communications 2025）、**CARE**（Weigert et al., Nature Methods 2018）、**OT-CycleGAN**（Park et al., Nature Communications 2022）、**UTOM**（Li et al., Light: Science & Applications 2021）和 **Volume Tells**（Li et al., CVPR 2025）等代表性基线。消融研究进一步证实：将物理 PSF 替换为高斯核导致 PSNR 下降约 22%、SSIM 下降 13%；从低质量观测（而非纯噪声）开始流匹配，PSNR 从 32.614 提升至 40.186，SSIM 从 0.889 提升至 0.964。这些结果表明，物理退化匹配与观测锚定生成是性能突破的关键。

### 各向同性显微成像的物理瓶颈

三维荧光显微镜是生命科学研究中观测细胞与组织结构的关键工具。理想的三维成像需要在横向 (XY) 和轴向 (Z) 均实现高分辨率，即各向同性分辨率。然而，传统高保真三维显微镜（如共聚焦或双光子显微镜）虽然能提供近乎各向同性的体积数据，却面临采集速度慢、成本高昂，以及对活体样本造成光毒性等根本性限制。这些限制使得此类成像手段难以适用于大规模、高通量或长时间的生物成像场景。

为克服上述瓶颈，实践中常采用快速二维扫描叠加稀疏轴向采样，再通过计算重建恢复轴向分辨率。这类策略的核心挑战在于：轴向图像受到光学系统各向异性点扩散函数 (Point Spread Function, PSF) 的严重模糊，而横向图像则保持较高分辨率。重建任务本质上是从各向异性观测中恢复各向同性体积，这是一个高度不适定的逆问题。

### 现有深度学习方法的双重缺陷

近年来，深度学习在该领域取得了显著进展，涌现出多种基于有监督、自监督或无监督学习的重建方法。然而，现有方法普遍存在两个根本性缺陷，制约了其重建保真度和泛化能力。

**缺陷一：退化模型与物理成像过程的失配。** 大多数方法依赖合成数据训练网络，其合成退化通常采用固定高斯核对横向高分辨率图像进行卷积来模拟轴向模糊。这一简化假设忽略了真实光学系统中 PSF 的空间变化性、光学像差以及样本引入的折射率不均匀性。实际显微镜的 PSF 是仪器特定的，受物镜数值孔径、波长、光路像差等因素共同决定，且在不同视场位置存在差异。高斯核退化无法捕捉这些复杂的物理特性，导致合成训练数据与真实图像形成过程之间存在严重的域差距 (domain gap)。网络在合成数据上学到的映射关系难以泛化到真实物理退化场景，重建结果常出现模糊、伪影或结构失真。

**缺陷二：缺乏显式三维体积几何约束。** 现有方法大多将三维重建问题分解为独立的二维切片处理，逐切片恢复后再堆叠为体积。这种逐切片处理方式忽略了跨切片的几何连续性和三维结构先验。在生物学样本中，细胞器、神经元纤维、血管网络等结构在三维空间中具有特定的形态学特征（如管状、球状、椭球状）。缺乏体积几何约束的重建网络容易产生形态失真，例如将原本扁长的椭球体结构错误重构为球体，或在轴向引入不连续的结构断裂。部分方法尝试使用准各向异性输入或简单的切片间插值，但这些弱约束远不足以编码完整的三维形态学先验。

### 生成式模型在显微重建中的机遇与风险

扩散模型等生成式方法在自然图像复原中展现出卓越的感知质量，其强大的分布建模能力为显微各向同性重建带来了新机遇。**Volume Tells** (Li et al., CVPR 2025) 率先将扩散模型引入该领域，展示了生成式先验的潜力。然而，标准扩散模型从纯噪声出发进行迭代去噪，在显微重建场景下存在固有风险：当退化严重或结构稀疏时，生成过程可能“幻觉”出不存在的结构细节，破坏重建结果的保真度和科学可信性。对于需要定量分析的生物医学应用，这种幻觉是不可接受的。

### MicroFM 的核心动机

综上，各向同性显微重建面临的核心矛盾在于：如何在快速、低成本的采集条件下，获得既符合物理成像规律、又保持三维几何一致性、且不引入幻觉的高保真各向同性体积。MicroFM 的提出正是为了解决这一矛盾。其核心动机可概括为三个层面：

1. **物理保真**：通过从轴向图像盲估计仪器匹配、空间变化的物理 PSF，使训练退化与真实光学过程对齐，从根本上缩小仿真与现实的差距。
2. **几何一致**：通过预训练连续隐式神经表示 (INR) 编码显式各向同性体积先验，为逐切片重建提供跨平面聚合的形态学引导，纠正孤立二维处理带来的结构失真。
3. **可信生成**：通过将流匹配的概率流起点锚定于低质量观测（而非纯噪声），使生成过程从观测出发向高质量分布演化，在保留生成模型感知优势的同时有效抑制幻觉。

图 Figure 1 从概念层面对比了传统三维显微成像、传统深度学习重建与 MicroFM 的差异，直观展示了物理引导与体积先验协同作用的设计理念。

## 核心方法与创新机理

MicroFM 的核心创新在于**物理引导的退化合成与体积隐式几何上下文协同作用**，使流匹配网络能够准确学习各向异性到各向同性的逆映射。具体而言，该方法引入三个关键干预变量，系统性解决了传统各向同性显微重建中合成退化失配与三维几何约束缺失两大瓶颈。

### 1. 物理 PSF 驱动的退化建模

传统方法普遍采用**固定高斯核**模拟轴向模糊，忽略了真实光学系统中点扩散函数 (PSF) 的空间变化、像差及样本引入的退化差异，导致合成训练数据与物理图像形成过程严重失配。MicroFM 将这一退化模型替换为 **SFE-Net 从轴向图像盲估计的仪器匹配、空间变化物理 PSF**（Section 3.2）。具体流程为：首先利用 Zernike 多项式在光瞳面合成物理一致的 PSF 并生成低分辨率图像，训练 SFE-Net 从低分辨率图像中盲推断 PSF；随后将该网络应用于目标显微镜的轴向图像，估计出匹配该仪器的 PSF 库，用于卷积横向高分辨率切片以构建逼真的训练配对。

这一改变的因果机制在于：物理 PSF 捕获了真实光路中的像差相位 $\phi(\rho,\theta)=\sum_{n=0}^{24}a_n Z_n(\rho,\theta)$ 及复光瞳函数 $P(\rho,\theta)=A(\rho)e^{i\phi(\rho,\theta)}$，经傅里叶变换得到非相干 PSF $h(x,y)=|\mathcal{F}\{P(\rho,\theta)\}|^2$，从而将合成退化与目标显微镜的光学特性对齐。**消融实验直接验证了这一干预的必要性**：将物理 PSF 替换为高斯核导致 PSNR 下降约 22%，SSIM 下降 13%（Table 3），表明物理退化匹配是保真度提升的关键杠杆。

### 2. 连续隐式神经表示编码体积几何先验

现有方法大多独立处理二维切片，缺乏显式三维体积几何约束，常导致结构形态失真（如将椭球体重构为球体）。MicroFM 通过**预训练连续隐式神经表示 (INR)** 编码显式各向同性体积先验（Section 3.3），以 MLP 网络 $f_\theta$ 结合固定位置编码 $\gamma$ 渲染连续三维体积 $\hat{V}(y,x,z)=f_\theta(\gamma(y,x,z))$。INR 训练以预测的物理 PSF 作为前向算子，在随机采样子体积上最小化模拟观测与实际堆栈的均方误差 $\mathcal{L}_{\mathrm{INR}}=\mathbb{E}_\Omega\|\mathcal{A}(\hat{V}|_\Omega)-G|_\Omega\|_2^2$。训练收敛后，对每个轴向切片通过沿深度维的高斯加权聚合邻域隐式采样，生成切片级几何先验图 $\hat{M}_s(y,x)=\sum_{k=1}^n w_k f_\theta(\gamma(y,x,z_s+\Delta_k))$。

该设计的因果机制在于：INR 将稀疏各向异性堆栈的跨切片连续性编码为连续场，为每个切片的恢复提供形态学约束，抑制了孤立 2D 处理导致的跨平面不一致。消融实验中体积先验权重 $\beta=0.50$ 获得最佳平衡（PSNR=40.186，SSIM=0.964，VIF=0.378，LPIPS=0.075），而增大 $\beta$ 会削弱观测信息导致性能下降（Table 4），验证了先验与观测协同的必要性。

### 3. 观测锚定的流匹配生成框架

标准扩散模型从**纯噪声**出发，在显微重建中易产生幻觉。MicroFM 将概率流起点替换为**低质量输入切片与体积先验的凸组合** $x_0=\alpha x_2+\beta\hat{M}$，使流匹配过程从观测出发而非从噪声出发（Section 3.3）。在此基础上，采用一致性流匹配损失 $\mathcal{L}_{\mathrm{cons}}=\|f(t,x_t)-f(r,x_r)\|_2^2+\lambda_{\mathrm{vel}}\mathbf{1}[t<b]\mathbf{1}[d_t>\tau]\|v_t-v_r\|_2^2$，强制段内端点一致性与速度一致性，拉直 ODE 轨迹，减少采样步骤和离散化误差。

这一改变的因果机制在于：从观测锚定流动起点将生成过程约束在真实数据分布附近，有效抑制了生成式模型常见的幻觉。**消融实验表明**：从低质量观测（而非噪声）开始流匹配，将 PSNR 从 32.614 提升至 40.186，SSIM 从 0.889 提升至 0.964（Table 3），在保真度和感知质量上均取得突破性提升。

### 创新协同效应

上述三个干预变量并非孤立作用，而是形成协同闭环：物理 PSF 为 INR 提供准确的前向成像算子，使体积先验更可靠；体积先验又为流匹配提供几何约束；观测锚定的流匹配则利用物理合成的训练对和体积先验，实现快速稳定的高保真重建。三者共同构成了从退化建模、几何约束到生成重建的完整物理引导链路。

MicroFM 是一个两阶段物理引导框架，将仪器感知的退化建模与几何感知的重建解耦为顺序协作的两个阶段。

**第一阶段：物理 PSF 预测与配对数据合成。** 系统从目标显微镜的轴向低分辨率图像出发，利用 SFE-Net 盲估计该仪器特有的、空间变化的物理点扩散函数（PSF）。估计得到的 PSF 库随后用于对横向高分辨率切片执行匹配真实光学特性的退化操作，合成物理逼真的训练配对。这一过程的核心在于用泽尼克多项式参数化的波前相位建模像差，通过复光瞳函数和非相干成像公式生成与目标显微镜退化分布一致的 PSF，从而弥合合成训练数据与真实图像形成过程之间的域差距。

**第二阶段：体积几何先验引导的流匹配各向同性重建。** 首先，利用第一阶段预测的物理 PSF 作为正向成像算子，训练一个连续隐式神经表示（INR），该 INR 由一个 MLP 网络和固定位置编码构成，能够渲染各向同性三维体积，并从中提取切片级的几何先验图——通过对邻域隐式采样进行高斯加权聚合得到。随后，以低质量轴向观测切片与该体积先验的凸组合作为概率流的起点，训练一个一致性流匹配重建网络。该网络在体积先验的形态学约束下，沿概率流 ODE 轨迹将起点传输到高质量各向同性切片；最终将所有重建切片融合为完整的三维各向同性体积。

**输入输出流。** 系统的输入端为轴向低分辨率图像堆栈（各向异性观测）和对应的横向高分辨率切片；中间产物包括仪器匹配的物理 PSF 库、物理退化合成的训练配对、以及 INR 渲染的各向同性体积先验；最终输出为高保真各向同性三维重建体积。Figure 2 完整展示了三个核心模块——物理 PSF 预测、预训练 INR 和流匹配重建网络——之间的数据依赖与流程关系。

![[assets/figures/papers/paper_list_l2546_https_openaccess_thecvf_com_content_CVPR2026_html_Zhan_MicroFM_Physics_g/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework of the proposed method. (a) Physical PSF Prediction: SFE-Net is trained with Zernike-based synthetic degradations and noise to regress spatially varying physical PSFs from axial images; the predicted PSFs are then used to synthesize training pairs matched to the target microscope. (b) Pretrain INR: Using the predicted PSFs as the physics operator, an MLP-based implicit neural representation renders an isotropic volume and serves as a volumetric geometry prior. (c) Flow Matching Reconstruction Network: Starting at*

MicroFM 是一个两阶段物理引导框架，其核心由三个功能模块串联构成：物理 PSF 预测模块、预训练隐式神经表示模块、以及流匹配重建网络模块。

### 物理 PSF 预测模块

传统方法使用固定高斯核模拟轴向模糊，忽略了真实光学系统中像差、切趾和空间变化等物理特性。MicroFM 的第一阶段从轴向低质量图像中盲估计仪器匹配的物理 PSF，其物理建模链路如下。

**像差相位建模**：在归一化光瞳坐标 $(\rho, \theta)$ 上，波前相位由 25 阶 Zernike 多项式加权和表示：

$$\phi ( \rho , \theta ) = \sum _ { n = 0 } ^ { 2 4 } a _ { n } Z _ { n } ( \rho , \theta )$$

其中 $a_n$ 为 Zernike 系数，$Z_n$ 为第 $n$ 阶 Zernike 基函数。该参数化覆盖了离焦、像散、彗差等常见像差模式，为合成物理一致性 PSF 提供了灵活的表达空间。

**复光瞳函数**：在夫琅禾费近似下，复振幅光瞳函数为：

$$P ( \rho , \theta ) = A ( \rho ) \mathrm { e } ^ { \mathrm { i } \phi ( \rho , \theta ) }$$

其中 $A(\rho)$ 为环形切趾函数，模拟物镜孔径的振幅衰减。

**非相干 PSF**：对复光瞳做傅里叶变换并取模平方，得到成像系统的非相干点扩散函数：

$$h ( x , y ) = \big | \mathcal { F } \{ P ( \rho , \theta ) \} \big | ^ { 2 }$$

**低分辨率图像合成**：利用估计的 PSF，从高分辨率横向切片合成物理匹配的低质量训练对：

$$I _ { \mathrm { L R } } \sim \mathcal { D } ( \mathrm { P o i s s o n } ( S * h ) + \eta ), \quad \eta \sim \mathcal { N } ( 0 , \sigma ^ { 2 } )$$

其中 $S$ 为高分辨率真值，$h$ 为物理 PSF，$*$ 表示卷积，$\mathcal{D}$ 为降采样算子。泊松噪声模拟光子计数统计，加性高斯噪声 $\eta$ 模拟读出噪声。该合成管线将物理退化模型（像差→光瞳→PSF→噪声）端到端嵌入训练数据生成，从根本上缩小了合成退化与真实显微成像之间的域差距。

SFE-Net 在合成数据上训练后，从目标显微镜的轴向图像中盲估计空间变化的 PSF 库。消融实验表明，将物理 PSF 替换为高斯核导致 PSNR 下降约 22%、SSIM 下降 13%，直接验证了物理退化匹配的关键性。

### 预训练隐式神经表示模块

第二阶段引入连续隐式神经场作为体积几何先验，弥补传统二维切片独立处理缺乏跨平面约束的缺陷。

**隐式各向同性体积**：由 MLP 网络 $f_{\theta}$ 与固定位置编码 $\gamma$ 表示连续三维体积场：

$$\hat { V } ( y , x , z ) = f _ { \boldsymbol { \theta } } \big ( \gamma ( y , x , z ) \big )$$

该表示可在任意连续空间坐标查询强度值，天然支持各向同性分辨率的重采样。

**INR 训练损失**：在随机采样子体积 $\Omega$ 上，最小化模拟观测与实际堆栈的均方误差：

$$\mathcal { L } _ { \mathrm { I N R } } = \mathbb { E } _ { \Omega } \| \mathcal { A } ( \hat { V } | _ { \Omega } ) - G | _ { \Omega } \| _ { 2 } ^ { 2 }$$

其中 $\mathcal{A}$ 为使用第一阶段估计的物理 PSF 构建的模拟观测算子，$G$ 为采集的原始体积堆栈。该损失使 INR 学习到物理一致的体积场，隐式编码了样本的三维形态学先验。

**切片先验聚合**：对于轴向位置 $z_s$ 的待重建切片，通过高斯加权平均邻域隐式采样生成几何先验图：

$$\hat { M } _ { s } ( y , x ) = \sum _ { k = 1 } ^ { n } w _ { k } f _ { \theta } \bigl ( \gamma ( y , x , z _ { s } + \Delta _ { k } ) \bigr )$$

其中 $w_k$ 为沿深度维的高斯权重，$\Delta_k$ 为邻域偏移量。该聚合机制将三维体积的跨切片连续性显式注入二维重建过程。

### 流匹配重建网络模块

流匹配重建网络以观测锚定的起点和体积先验为条件，执行一致性流匹配恢复高保真各向同性切片。

**流起点定义**：区别于标准扩散模型从纯噪声出发，MicroFM 将概率流起点锚定于低质量观测与体积先验的凸组合：

$$x _ { 0 } = \alpha x _ { 2 } + \beta \widehat { M }$$

其中 $x_2$ 为原始低质量轴向切片，$\hat{M}$ 为 INR 提供的几何先验图，$\alpha$ 和 $\beta$ 为平衡系数。该设计将流动过程约束在数据流形附近，从源头抑制生成式模型常见的幻觉。消融实验证实，从低质量观测（而非纯噪声）开始流匹配，PSNR 从 32.614 提升至 40.186，SSIM 从 0.889 提升至 0.964。

**一致性流匹配损失**：为减少采样步数和离散化误差，采用段内端点一致性与速度一致性的联合约束：

$$\mathcal { L } _ { \mathrm { c o n s } } = \left\| f ( t , x _ { t } ) - f ( r , x _ { r } ) \right\| _ { 2 } ^ { 2 } + \lambda _ { \mathrm { v e l } } \mathbf { 1 } [ t < b ] \mathbf { 1 } [ d _ { t } > \tau ] \left\| v _ { t } - v _ { r } \right\| _ { 2 } ^ { 2 }$$

其中 $f(t, x_t)$ 为时刻 $t$ 的流网络输出，$r$ 为段内参考时刻，$v_t$ 为速度场。第一项强制段内端点输出一致性，拉直 ODE 轨迹；第二项速度一致性项仅在段内（$t < b$）且远离端点（$d_t > \tau$）时激活，进一步减少轨迹曲率。该损失使 MicroFM 仅需两阶采样即可实现高质量重建，在保真度和推理效率之间取得平衡。

## 实验与关键发现

### 实验设置与数据集

MicroFM 在 **四个不同荧光显微镜系统** 采集的数据集上进行评估，涵盖多种组织类型与成像模态，以验证跨系统的泛化能力（Table 1）。数据集包括：密集神经元簇（CS-fMOST 成像）、清除的 mTmG 小鼠肾脏（二次谐波 SHG 显微镜）、清除的 Thy1-GFP 小鼠脑神经元（共聚焦显微镜）以及清除的小鼠肝脏（宽场显微镜）。各数据集在横向 (XY) 与轴向 (Z) 的像素规模差异显著，覆盖了从高分辨率结构到厚组织体积的多样化场景。

![[assets/figures/papers/paper_list_l2546_https_openaccess_thecvf_com_content_CVPR2026_html_Zhan_MicroFM_Physics_g/figures/003_Table_1.jpg]]
*Table 1: Datasets summary used in MicroFM*

评估采用互补的双轨指标：在横向 (XY) 测试图像上使用 **全参考指标**（PSNR、SSIM、VIF、LPIPS），在轴向 (XZ/YZ) 测试图像上使用 **无参考指标**（NIQE、PIQE、NRQM），从保真度与感知质量两个维度综合评价重建效果。对比基线涵盖六种代表性方法：有监督的 **CARE** (Weigert et al., Nature Methods 2018)、自监督的 **Self-Net** (Ning et al., Light: Science & Applications 2023) 与 **SSAI-3D** (Han et al., Nature Communications 2025)、无监督的 **CycleGAN** (Zhu et al., 2020)、**OT-CycleGAN** (Park et al., Nature Communications 2022)、**UTOM** (Li et al., Light: Science & Applications 2021)，以及基于扩散模型的 **Volume Tells** (Li et al., CVPR 2025)。所有方法在相同数据划分与实验设置下评估，确保公平性。

### 主实验结果

Table 2 汇总了四个数据集上的定量对比。MicroFM 在所有数据集上均取得 **最优或并列最优** 的全参考指标，尤其在密集神经元簇数据集上，PSNR 达到 **40.186 dB**，SSIM 达到 **0.964**，LPIPS 低至 **0.075**，显著超越所有基线方法。在小鼠肾脏数据集上，PSNR 为 **33.005 dB**，SSIM 为 **0.946**，同样达到或超过所有对比方法。

![[assets/figures/papers/paper_list_l2546_https_openaccess_thecvf_com_content_CVPR2026_html_Zhan_MicroFM_Physics_g/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison on four datasets acquired from different fluorescence microscopy systems. Full Reference Metrics are computed on lateral (XY) test images, while No Reference Metrics are computed on axial (XZ/YZ) test images. Multiple complementary metrics are adopted to enable a fair and comprehensive evaluation. Arrows indicate the preferred direction for each metric: ↑ means higher is better and ↓ means lower is better. Bold entries denote the best performance, and underlined entries denote the second best*

在轴向无参考指标上，MicroFM 展现出 **更稳定的优势**：NIQE 和 PIQE 值在各数据集上均优于或接近最优，NRQM 指标亦保持领先。这表明 MicroFM 不仅在横向切片上恢复了高保真细节，在跨切片轴向结构上也有效抑制了伪影，实现了真正的三维各向同性重建。

定性结果（Figure 3）进一步印证了定量结论。以密集神经元簇为例，原始轴向输入呈现显著的轴向拉伸模糊，Self-Net 和 SSAI-3D 虽能部分恢复结构，但仍残留形态畸变（如椭球体被错误重构为球体）。MicroFM 的重建结果在放大视图中显示出更锐利的膜边界和更准确的树突形态，傅里叶频谱也呈现出更各向同性的功率分布。在小鼠肾脏 SHG 数据上，MicroFM 恢复了清晰的肾小管边界，而基线方法在管腔内部产生了不同程度的模糊或断裂。

Figure 4 展示了小鼠肾脏组织的三维重建前后对比：原始体积在轴向 (XZ) 视角下结构严重拉伸，MicroFM 重建后轴向与横向分辨率趋于一致，肾小管的三维形态得到准确恢复。

![[assets/figures/papers/paper_list_l2546_https_openaccess_thecvf_com_content_CVPR2026_html_Zhan_MicroFM_Physics_g/figures/006_Figure_4.jpg]]
*Figure 4: Comparison of cleared mTmG mouse kidney tissue before and after 3D reconstruction*

### 消融实验

为量化各核心组件的贡献，Table 3 在密集神经元簇数据集上进行了系统消融。基础模型（Base）移除物理 PSF、体积先验和观测锚定流起点，退化为使用高斯退化核的标准流匹配。

![[assets/figures/papers/paper_list_l2546_https_openaccess_thecvf_com_content_CVPR2026_html_Zhan_MicroFM_Physics_g/figures/008_Table_3.jpg]]
*Table 3: Ablation of MicroFM components on the Dense Neuron Cluster dataset. Best result in each column is shown in bold. The base model removes the physical PSFs, the volumetric prior, and the flow that starts from low-quality images, while MicroFM includes all three components*

**物理 PSF 配对** 是性能提升的最大单一驱动力：将物理 PSF 替换为高斯核导致 PSNR 下降约 **22%**，SSIM 下降 **13%**。这直接验证了物理退化匹配对于缩小合成训练与真实光学退化之间域差距的关键作用。

**观测锚定流起点** 的影响同样显著：从纯噪声（而非低质量观测）开始流匹配过程，PSNR 从 40.186 骤降至 **32.614**，SSIM 从 0.964 降至 **0.889**。这表明从观测出发的概率流有效抑制了生成式模型常见的幻觉，使网络学习到保真度更高的逆映射。

**体积几何先验** 的贡献体现在形态学保真度上：移除体积先验后，VIF 指标下降明显，说明跨切片聚合的隐式几何约束对于维持三维结构一致性不可或缺。

Table 4 进一步消融了体积先验权重 β 的影响。当 β = 0.50 时取得最佳平衡（PSNR=40.186，SSIM=0.964，VIF=0.378，LPIPS=0.075）。增大 β 会过度依赖先验而削弱观测信息，导致 PSNR 和 SSIM 下降；减小 β 则使体积约束不足，VIF 和 LPIPS 恶化。这揭示了观测保真度与几何正则化之间的精细权衡。

![[assets/figures/papers/paper_list_l2546_https_openaccess_thecvf_com_content_CVPR2026_html_Zhan_MicroFM_Physics_g/figures/009_Table_4.jpg]]
*Table 4: Ablation of the volume prior weight β on the Dense Neuron Cluster dataset. Best result is shown in bold*

### 物理 PSF 估计的跨系统分析

Figure 5 从信息论角度分析了 PSF 估计的质量。左图显示，训练后 PSF 库的熵值显著降低，表明估计的 PSF 在保持空间变化性的同时具有较高的集中度，残余离散度有限，与单台显微镜内有限的空间变异性预期一致。右图对比了四个荧光显微镜系统的晚期 PhaseZ 幅度，揭示了不同仪器间系统性的像差差异——这进一步佐证了针对目标显微镜定制物理 PSF 的必要性，而非依赖通用高斯退化假设。

### 失败模式与局限性

尽管 MicroFM 在多个数据集上取得了 SOTA 性能，分析过程与论文披露揭示了以下局限性：

1. **PSF 估计与重建解耦**：SFE-Net 需单独训练，未与重建网络端到端联合优化。这种解耦设计可能限制了 PSF 估计对下游重建任务的自适应调优能力，在退化特性与训练分布偏差较大的场景下，估计误差会直接传播至重建阶段。

2. **体积先验的泛化边界**：预训练的 INR 依赖模拟观测进行训练，对于训练集中未出现的样本形态（如罕见病理结构），体积先验可能提供不准确的几何引导。在高度散射或深度变化剧烈的组织中，INR 的连续场假设可能失效。

3. **采样效率的未充分探索**：当前流匹配推理采用两阶采样，尽管步数远少于扩散模型，但未系统研究采样步数与重建质量、计算效率之间的最优平衡点。对于实时或高通量成像场景，进一步减少采样步数的可行性尚待验证。

4. **模态与通道限制**：当前方法仅在单通道荧光数据上验证，未扩展到多通道（如多色荧光）或延时成像场景。多通道间的交叉干扰建模与联合重建是实际应用中亟待解决的问题。

5. **极端退化鲁棒性未知**：实验在相对均匀的组织样本上进行，对于强散射介质（如厚脑片深层）或极低信噪比条件下的表现尚未评估，这些场景下物理 PSF 估计的准确性可能显著下降。

### 开放问题

基于上述分析，以下方向值得进一步探索：

- 若将 PSF 估计网络与流匹配重建网络 **端到端联合训练**，能否通过重建损失的梯度反馈提升 PSF 估计精度，并减少对配对训练数据的依赖？
- 能否设计 **在线校准策略**，使 PSF 估计模块在无需重新训练的情况下适配不同显微镜或同一显微镜的状态漂移？
- 物理引导的流匹配框架能否推广至 **超分辨率显微术**（如 STED、PALM/STORM）的各向同性恢复，其中 PSF 工程化特性更为复杂？
- 体积先验的构建是否可替换为更高效的 **3D 卷积神经场**，以减少推理时的逐点隐式采样开销，提升处理通量？
- 多通道荧光信号间的 **光谱串扰与色差** 如何建模并整合到退化合成与联合重建流程中？

## 定位与知识库关联

### 1. 基线关系与差异化定位

MicroFM 处于各向同性显微重建这一细分领域，其方法设计直接回应了现有基线在两个维度上的根本缺陷：退化合成的物理失配与体积几何约束的缺失。

**相对于有监督/自监督基线。** **CARE**（Weigert et al., Nature Methods 2018）开创了基于配对数据的有监督显微图像复原范式，但其训练对依赖高斯核模拟轴向模糊，与真实光学系统的各向异性、空间变化点扩散函数（PSF）存在系统性偏差。**Self-Net**（Ning et al., Light: Science & Applications 2023）和 **SSAI-3D**（Han et al., Nature Communications 2025）将自监督学习引入各向同性重建，减少了对配对数据的依赖，但二者仍以二维切片为独立处理单元，缺乏跨切片的显式三维几何约束。MicroFM 通过 SFE-Net 盲估计仪器匹配的物理 PSF 并合成逼真训练对，从根本上缩小了仿真-真实退化差距；同时引入预训练连续隐式神经表示（INR）编码的体积几何先验，为每一切片提供跨平面加权聚合的形态学引导（公式 (7)–(8)），弥补了二维独立处理的形态失真风险。

**相对于无监督/生成式基线。** **CycleGAN**（Zhu et al., 2020）、**OT-CycleGAN**（Park et al., Nature Communications 2022）和 **UTOM**（Li et al., Light: Science & Applications 2021）均采用无监督域迁移策略，避免了对配对数据的依赖，但生成式模型固有的幻觉风险在显微重建中尤为突出——错误的亚细胞结构恢复可能导致生物学误读。**Volume Tells**（Li et al., CVPR 2025）将扩散模型引入各向同性重建，通过体积上下文约束提升保真度，但其扩散过程从纯噪声出发，仍存在幻觉隐患。MicroFM 采用一致性流匹配框架，将概率流起点锚定于低质量观测与体积先验的凸组合（$x_0 = \alpha x_2 + \beta \widehat{M}$，公式 (9)），使生成过程从观测出发而非从纯噪声出发。消融实验直接验证了这一设计的因果效应：将流起点从低质量观测替换为纯噪声，PSNR 从 40.186 dB 骤降至 32.614 dB，SSIM 从 0.964 降至 0.889（Table 3），表明观测锚定是抑制幻觉的关键干预变量。

**核心差异化总结。** MicroFM 在三个方法槽位上实现了根本性改变：训练退化模型从固定高斯 PSF 卷积替换为 SFE-Net 估计的物理 PSF；体积几何先验从无或弱二维上下文替换为 INR 编码的显式各向同性体积先验；生成模型起点从纯噪声替换为观测锚定的凸组合。这三个槽位的协同作用使 MicroFM 在四个荧光显微镜系统上均达到最优性能（Table 2），在 Dense neuron cluster 数据集上 PSNR 达 40.186 dB、SSIM 达 0.964，显著超越所有代表性基线。

### 2. 方法适用边界

**系统覆盖范围。** MicroFM 在四个荧光显微镜系统上进行了验证：CS-fMOST（密集神经元簇）、双光子 SHG 显微（小鼠肾脏）、共聚焦显微（Thy1-GFP 脑神经元）和宽场显微（小鼠肝脏），覆盖了主流的荧光成像模态。Table 2 的跨系统定量结果表明，方法对仪器差异具有较好的泛化性，但 Figure 5 右图的 PhaseZ 幅度分析揭示了不同系统间光学特性的系统性差异，暗示针对新仪器的 SFE-Net 微调或重新校准可能是必要的。

**样本形态约束。** 当前实验在相对均匀的组织样本上评估（密集神经元簇、清除组织等），体积先验基于预训练的 INR 构建，对未见过的样本形态可能存在泛化不足。INR 训练依赖模拟观测（公式 (6)），其域差距在高散射或复杂深度变化的样本上可能被放大。此类场景下的鲁棒性尚待系统验证。

**数据模态限制。** 方法仅演示在单通道荧光数据上，未扩展到多通道或延时成像。多通道荧光信号间的交叉干扰（如光谱串扰）未被建模到当前的退化合成与重建流程中，这构成了向多通道成像推广的直接障碍。

### 3. 局限性与开放问题

**架构层面的局限性。** SFE-Net 的 PSF 估计与重建网络分离训练，未实现端到端联合优化，可能限制了自适应能力——若 PSF 估计存在残余误差，重建网络无法通过梯度反馈进行补偿。此外，体积先验的构建依赖 INR 的隐式采样（公式 (7)），推理时需对邻域坐标进行多次 MLP 前向查询，计算开销高于直接的 3D 卷积神经场。

**采样效率的未解空间。** 流匹配推理采用两阶采样，尽管步数远少于扩散模型，但采样步数与重建质量、推理效率之间的最优平衡尚未被系统探索。一致性流匹配损失（公式 (12)）中的速度一致性项权重 $\lambda_{\mathrm{vel}}$ 和阈值 $\tau$ 的敏感性也未在消融中覆盖。

**开放问题。** 分析揭示了若干值得后续探索的方向：其一，若将 PSF 估计网络与重建网络联合训练，是否可进一步提升保真度并减少配对数据需求？其二，物理引导的流匹配框架能否推广到超分辨率显微术（如 STED、PALM）的各向同性恢复，这些模态的 PSF 模型与荧光显微镜存在本质差异。其三，在线校准策略能否在无需重新训练的情况下集成，以适应不同显微镜的即时调整？其四，多通道荧光信号间的交叉干扰如何建模并整合到当前的退化合成与重建流程中？这些问题构成了 MicroFM 向更广泛显微成像场景延伸的关键路径。

## 原文 PDF

![[paperPDFs/CVPR_2026/MicroFM_Physics_guided_Flow_Matching_for_Isotropic_Microscopy_Reconstruction.pdf]]
