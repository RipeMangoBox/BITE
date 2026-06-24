---
title: Frequency-aware Dynamic Gaussian Splatting
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Frequency_aware_Dynamic_Gaussian_Splatting_a82166feb7da.pdf
project_link: "https://arxiv.org/abs/2503.14501"
code_link: null
aliases:
- FADGSF
- FADGS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过频率区分的自适应高斯核显式解耦高/低频表现力，并利用频率感知的变形网络分别捕捉高频局部变形和低频全局运动。
primary_logic: 将每个高斯核的学习调制函数参数化为可自适应调整的锐利高频核或平滑低频核，减少重叠依赖；同时，通过傅里叶特征注入每点的高频时间变化，并用频率感知门控调节变形强度，使网络既能精准建模高频运动又保持稳定性。
claims:
- 在D-NeRF合成数据集上，FAGS在所有七个场景中均取得最佳PSNR，平均PSNR达到42.76，较最优基线Grid4D（平均PSNR约42.27）提升0.49 dB。
- 消融实验表明，移除频率区分高斯核（FDGK）后PSNR从42.76降至42.11，验证了FDGK的关键作用。
- 时间运动功率谱可视化显示FAGS将更多高斯集中在高频带，证实其有效捕捉了高频运动。
- D-NeRF (synthetic) 上 PSNR (dB) = 42.76
---

# Frequency-aware Dynamic Gaussian Splatting

> [!tip] 核心洞察
> 将每个高斯核的学习调制函数参数化为可自适应调整的锐利高频核或平滑低频核，减少重叠依赖；同时，通过傅里叶特征注入每点的高频时间变化，并用频率感知门控调节变形强度，使网络既能精准建模高频运动又保持稳定性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 频率感知的动态高斯溅射 |
| 英文题名 | Frequency-aware Dynamic Gaussian Splatting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=UZ00ac4eqA) · [arXiv](https://arxiv.org/abs/2108.05997) · [Project](https://arxiv.org/abs/2503.14501) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Frequency-Aware Dynamic Gaussian Splatting (FAGS) |
| Dataset | D-NeRF, Neu3D, HyperNeRF Rig subset, HyperNeRF Interpolation subset |

> [!tip] 效果简介
> - D-NeRF (synthetic) 上，PSNR (dB) 42.76 vs 42.27 (Grid4D平均) (+0.49)。
> - Neu3D (real-world) 上，PSNR (dB) 44.16。
> - HyperNeRF Rig subset 上，PSNR 25.63。

## 概述

动态场景的新视角合成（4D重建）是计算机视觉与图形学中的核心挑战，其目标是从一组稀疏的二维观测中恢复三维场景随时间的完整外观与运动。现有主流方法——尤其是基于变形驱动（deformation-driven）的动态3D高斯溅射（3DGS）——在平衡**高频渲染细节**与**高频运动建模**时面临根本性的频谱冲突。标准高斯核采用固定的不透明度衰减函数，为捕获纹理、边缘等高频外观特征，大量高斯不得不密集重叠；这迫使变形网络同时承担“再现高频外观”和“驱动高斯进行一致运动”的双重任务，最终导致网络偏向于学习平滑、低频的均匀轨迹，在新视角下产生严重的运动模糊（见Figure 1(a)）。

本文提出**频率感知的动态高斯溅射（Frequency-Aware Dynamic Gaussian Splatting, FAGS）**，核心思想是通过**频率区分的显式解耦**来打破上述频谱冲突。FAGS包含两大关键设计：

1. **频率区分高斯核（Frequency-Differentiated Gaussian Kernel, FDGK）**：为每个高斯引入可学习的自适应alpha调制函数，使其在优化过程中自动分化为锐利的高频核或平滑的低频核，从而减少对密集重叠的依赖，将高频外观表达与变形控制解耦。
2. **傅里叶变形网络（Fourier-Deformation Network, FDN）**：在低频谱哈希编码的基础上，为每个高斯注入高频傅里叶嵌入以显式捕捉周期性局部运动，并通过频率感知门控自适应调节变形强度，抑制低频区域的非必要运动。

在三个基准数据集上的实验表明，FAGS取得了具有竞争力的定量结果：在合成D-NeRF数据集上平均PSNR达到**42.76 dB**，较最优基线Grid4D（Xu et al., arXiv 2024）提升**0.49 dB**（Table 1）；在真实场景Neu3D和HyperNeRF数据集上同样表现优异（Table 2、Table 3）。消融实验证实，移除FDGK后PSNR从42.76降至42.11，验证了频率区分高斯核对性能的关键贡献（Table 4）。时间运动功率谱分析进一步表明，FAGS将更多高斯集中到高频运动带，从机制层面验证了其捕捉高频运动的能力（Figure 11）。

## 背景与动机

动态场景的新视角合成是计算机视觉与图形学中的核心挑战，其目标是从一组稀疏的多视角视频中重建出随时间变化的三维场景，并支持任意时刻、任意视角的高质量渲染。近年来，以三维高斯溅射（3D Gaussian Splatting, 3DGS）为代表的显式辐射场方法在静态场景渲染中取得了突破性进展，其通过一组可微的三维高斯原语进行高效的光栅化渲染，在速度和质量上均大幅超越基于隐式神经辐射场的方法。然而，将3DGS从静态场景拓展至动态场景时，一个根本性的瓶颈逐渐显现：**高频渲染细节与高频运动建模之间存在严重的频谱冲突**。

这一冲突的根源在于标准高斯核的固定不透明度衰减机制。在3DGS中，每个高斯的透明度 $\alpha_i$ 由其不透明度 $o_i$ 和固定的指数衰减函数共同决定（Eq. 1）。为捕捉场景中的高频外观细节（如锐利边缘、纹理变化），系统需要大量高斯在空间上密集重叠，通过精细的叠加来逼近复杂的光场变化。当场景引入时间维度后，这些密集堆叠的高斯必须由变形网络统一驱动，以产生连贯的运动轨迹。这就迫使变形网络同时承担两项相互矛盾的任务：既要维持足够的高斯密度以再现高频外观，又要协调这些高斯的集体运动以避免视觉伪影。由于网络优化天然倾向于平滑、低频的解空间，变形网络往往会偏向于产生均匀的低频运动轨迹，从而导致新视角下出现严重的运动模糊——这正是现有变形驱动的4D重建方法（如 **DeformGS**（Yang et al., CVPR 2024）、**Grid4D**（Xu et al., arXiv 2024））普遍面临的困境。

Figure 1 直观地揭示了这一问题：基线方法中，标准高斯核为了拟合高频细节而密集重叠，使得变形控制变得极为复杂，网络被迫输出平滑的低频轨迹，最终导致渲染结果出现运动模糊。这本质上是一个**表现力与可控性之间的频谱失衡**问题——高斯核的固定频率响应使得系统无法在高频细节区域和低频平滑区域之间进行差异化处理。

针对上述瓶颈，本文的核心洞察是：**通过显式解耦高斯核的高频与低频表现力，并设计频率感知的变形机制，可以从根本上缓解这一频谱冲突**。具体而言，本文提出**频率感知的动态高斯溅射（Frequency-Aware Dynamic Gaussian Splatting, FAGS）**，其动机源于两条关键设计思路：

1. **频率区分的核设计**：赋予每个高斯核自适应调整其频率响应的能力，使其可以专门化为锐利的高频核或平滑的低频核，从而减少对密集重叠的依赖，降低变形网络的协调负担。

2. **频率感知的运动建模**：在变形网络中注入高频傅里叶特征，使网络能够显式捕捉每个高斯的周期性高频运动分量，同时通过频率感知门控机制抑制低频区域的非必要运动，实现精细且稳定的动态建模。

通过将频率维度的显式解耦引入高斯溅射框架，FAGS旨在同时提升动态场景的高频细节保真度和运动建模精度，为4D重建提供一种频谱平衡的新范式。

## 核心创新

FAGS 的核心创新在于对 4D 重建中“高频外观”与“高频运动”的频谱冲突进行了显式解耦。现有变形驱动方法（如 **DeformGS** (Yang et al., CVPR 2024)、**Grid4D** (Xu et al., arXiv 2024)）依赖标准高斯核的固定不透明度衰减函数，迫使变形网络同时承担两项矛盾的任务：通过密集重叠的高斯来再现高频纹理细节，以及驱动这些高斯进行一致的运动建模。这种双重负担使网络偏向于学习平滑、低频的均匀运动轨迹，最终在新视角下产生严重的运动模糊（参见 Figure 1(a)）。

FAGS 通过三个协同的 changed slots 打破这一瓶颈：

**1. 频率区分高斯核 (FDGK)：从固定衰减到自适应频率特化**

传统 3DGS 的 alpha 值由固定不透明度 $o_i$ 与指数衰减函数直接计算（Eq. 1）。FAGS 将其替换为一个可学习的自适应分段线性调制函数 $\psi(g)$（Eq. 3），引入两个关键参数：$\lambda$ 控制高斯核对高频或低频的倾向（斜率），$\beta$ 控制频率区分区间的宽度。这使得每个高斯在优化过程中自动分化为锐利的高频核或平滑的低频核（见 Figure 2），前者负责捕捉边界与纹理细节，后者覆盖平滑区域，从而大幅减少对密集重叠的依赖，为变形网络释放了表征容量。

**2. 傅里叶变形网络 (FDN)：从纯哈希编码到高低频联合特征**

基线方法（如 Grid4D）仅使用 4D 哈希编码捕获低频时空特征。FAGS 在此基础上为每个高斯点引入高频傅里叶嵌入 $f_{\mathrm{fre}}$（Eq. 6），其幅度系数由空间特征 MLP 动态预测（Eq. 7）。该嵌入将运动轨迹建模为多个频率周期运动的叠加，使网络能够精确捕捉高频局部变形。同时，频率感知门控 $\eta$（Eq. 8）根据高斯的动态性自适应调节变形强度——对静态或低频区域抑制不必要的运动，对动态区域施加更强的变形，从而在保持稳定性的同时实现精细运动建模。

**3. 傅里叶频率损失 (FFL)：从空域约束到频域约束**

除常规的 L1 和 SSIM 损失外，FAGS 增加了傅里叶频率损失 $\mathcal{L}_{\mathrm{fre}}$（Eq. 9），直接约束渲染图像与真实图像在频域振幅谱上的一致性，强化对高频细节的优化。

消融实验（Table 4）定量验证了上述 changed slots 的关键作用：完整模型在 D-NeRF 上取得 PSNR 42.76；移除 FDGK 后降至 42.11；进一步移除高频傅里叶嵌入和频率感知门控均导致性能持续下降。时间运动功率谱可视化（Figure 11）进一步证实 FAGS 将更多高斯集中在高频带，有效捕捉了高频运动。

## 整体框架

FAGS 的整体设计遵循一个核心原则：**在 4D 重建的渲染与运动建模两个关键环节中，显式解耦高频与低频分量**。如图 3 所示，框架由两条互补的流水线构成——上方的 **频率区分高斯核（FDGK）** 负责渲染端的频域分化，下方的 **傅里叶变形网络（FDN）** 负责运动建模端的频域解耦，二者通过共享的高斯表示协同工作。

### 渲染端：高斯核的频率分化

在规范空间中，所有高斯以统一状态初始化。训练过程中，FDGK 为每个高斯引入可学习参数 **λ**（控制频率倾向）和 **β**（控制区分区域），通过自适应分段线性调制函数 **ψ(g)** 调节 alpha 衰减曲线（见 Eq. 2 和 Eq. 3）：

- 当 λ 取较大值时，ψ(g) 斜率增大，高斯核变得锐利，专精于捕捉高频细节（如边缘、纹理）；
- 当 λ 取较小值时，ψ(g) 趋于平缓，高斯核变得平滑，适合表达低频均匀区域。

这种自适应分化使高斯群体在优化过程中自动分工：**锐利核负责高频外观重建，平滑核负责低频区域填充**，从而减少了对密集重叠的依赖，缓解了传统 3DGS 中变形网络同时承担“高频渲染”与“运动建模”双重任务的频谱冲突。

### 运动端：傅里叶变形网络

FDN 接收规范空间坐标 **(x, y, z)** 和时间 **t**，通过两路编码器构建高-低频联合特征 **f_FD**：

1. **低频支路**：将 4D 坐标分解为四个 3D 哈希编码（_H_xyz_、_H_xyt_、_H_xzt_、_H_yzt_），分别提取空间特征 **f_spa** 和时间特征 **f_tem**（Eq. 5），捕获全局低频运动趋势。
2. **高频支路**：从空间特征通过 MLP 预测傅里叶嵌入的幅度系数 **[w₁, …, w_m]**（Eq. 7），构建每点的高频傅里叶嵌入 **f_fre**（Eq. 6），显式注入周期性高频时间变化。

融合后的特征 **f_FD** 送入多头解码器，同时预测变形参数和 **频率感知门控 η**（Eq. 8）。η 自适应调制每个高斯的变形强度——动态点获得高 η 值以精确追踪高频运动，静态或低频点被抑制以减少不必要的位移，从而在保持高频运动建模能力的同时维持整体稳定性。

### 优化目标

除标准的 L1 渲染损失和 SSIM 损失外，FAGS 引入 **傅里叶频率损失 L_fre**（Eq. 9），在频域对渲染图像与真实图像的振幅谱施加 L1 约束，显式强化高频细节的优化。

### 输入输出流

- **输入**：多视角视频帧（含相机位姿和时间戳）
- **规范空间**：可学习的 3D 高斯集合（位置 μ、协方差 Σ、颜色 c、不透明度 o），附加每点参数 λ、β
- **变形阶段**：FDN 接收 (x, y, z, t)，输出 η、旋转 R_x、平移 T_x、旋转增量 Δr、缩放增量 Δs，将规范高斯变换到当前时刻状态
- **渲染阶段**：FDGK 根据 λ、β 计算自适应 alpha 值，通过 alpha blending（Eq. 1）合成像素颜色
- **输出**：任意时刻、任意视角的渲染图像

### 补充图表

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_UZ00ac4eqA/figures/003_Figure_3.jpg]]
*Figure 3: Overview of Frequency-Aware Gaussian Splatting. Top: Gaussians are initialized in a canonical state and progressively differentiate into low- and high-frequency types during optimization, fitting low-frequency smooth regions and high-frequency details, respectively. Bottom: Coordinates*

## 核心模块与公式推导

FAGS 的核心设计围绕一个关键矛盾展开：**变形驱动的 4D 重建中，高频外观细节与高频运动轨迹对高斯核提出了相互冲突的要求**。标准 3DGS 中所有高斯共享固定的指数衰减 alpha 函数（Eq. 1），要捕捉锐利边缘和纹理细节，必须依赖大量高斯在空间上密集重叠——这反过来使变形网络难以精确控制每个高斯的独立运动，最终导致网络偏向学习平滑、低频的全局运动，在新视角下产生运动模糊（见 Figure 1(a)）。FAGS 通过三个相互配合的模块——**频率区分高斯核（FDGK）**、**傅里叶变形网络（FDN）** 和 **频率感知门控**——将“表现力”与“运动建模”在频率维度上显式解耦。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_UZ00ac4eqA/figures/001_Figure_1.jpg]]
*Figure 1: Analysis of high-frequency details and motion. (a) Baseline: Standard Gaussian kernels require dense overlapping to capture high-frequency details, which complicates deformation control and biases the network toward smooth, low-frequency trajectories, resulting in motion blur. (b) Our ?? = 1 method: Gaussians in high- and low-frequency regions are differentiated, enabling the deformation ?? = 2 Ours network to capture high-frequency motion on top of global low-frequency deformations, allowing each Gaussian to follow its own fine-grained dynamics*

### 3.1 基础渲染公式

3DGS 的像素颜色通过 alpha 混合 N 个重叠高斯得到：

$$C ( \mathbf { p } ) = \sum _ { i = 1 } ^ { N } c _ { i } \alpha _ { i } \prod _ { j = 1 } ^ { i - 1 } ( 1 - \alpha _ { j } ) , \quad \alpha _ { i } = o _ { i } \exp \Big [ - \frac { 1 } { 2 } ( p - \mu ^ { 2 D } i ) ^ { T } ( \Sigma ^ { 2 D } i ) ^ { - 1 } ( p - \mu _ { i } ^ { 2 D } ) \Big ]$$

其中 $\alpha_i$ 由不透明度 $o_i$ 和高斯投影的指数衰减共同决定，衰减速率完全由协方差矩阵 $\Sigma_i^{2D}$ 固定。这一固定衰减是频谱冲突的根源——所有高斯被迫以相同方式衰减，无法根据所处区域的频率特性自适应调整。

### 3.2 频率区分高斯核（FDGK）

FDGK 的核心创新是将 alpha 衰减从“固定指数”改为“可学习的自适应调制”，使每个高斯能够根据场景需求分化为**锐利高频核**或**平滑低频核**。

首先引入广义 alpha 计算，用线性调制函数 $\psi(g)$ 替代固定指数衰减：

$$\alpha _ { i } = \operatorname* { m i n } ( o _ { i } \psi ( g ) , 0 . 9 9 ) , \quad \psi ( g ) = r g + b , \quad \mathrm { w h e r e ~ } g = \exp \Big [ - \frac { 1 } { 2 } ( { \bf p } - { \mu } _ { i } ^ { 2 D } ) ^ { T } ( \Sigma _ { i } ^ { 2 D } ) ^ { - 1 } ( { \bf p } - { \mu } _ { i } ^ { 2 D } ) \Big ]$$

其中 $r$ 控制衰减斜率，$b$ 控制偏置。$r > 1$ 时高斯更锐利（适合高频细节），$r < 1$ 时更平滑（适合低频区域）。

为使斜率 $r$ 和区分区域可自适应学习，FDGK 引入两个可学习参数 $\lambda$（控制频率倾向）和 $\beta$（控制区分区间宽度），构造分段线性激活函数 $\psi(g)$：

$$\psi ( g ) = \left\{ \begin{array} { l l } { \frac { 0 . 5 + \lambda - 0 . 5 \beta - \lambda \beta } { 0 . 5 + \lambda - \beta } g , } & { g \in [ 0 , p _ { l } ) , } \\ { ( 0 . 5 + \lambda ) g + ( 0 . 2 5 - 0 . 5 \lambda ) , } & { g \in [ p _ { l } , p _ { r } ] , } \\ { \frac { 0 . 5 + \lambda - 0 . 5 \beta - \lambda \beta } { 0 . 5 + \lambda - \beta } ( g - 1 ) + 1 , } & { g \in ( p _ { r } , 1 ] , } \end{array} \right.$$

其中 $p_l = 0.5 - \beta$，$p_r = 0.5 + \beta$。该函数的关键行为（见 Figure 2）：
- **中间区间** $[p_l, p_r]$ 的斜率由 $\lambda$ 决定：$\lambda > 0$ 使斜率大于 1，高斯趋向高频锐利核；$\lambda < 0$ 使斜率小于 1，高斯趋向低频平滑核。
- **边界参数 $\beta$** 控制中间区间的宽度，独立于 $\lambda$ 调节高斯从锐利到平滑的过渡范围，使高斯能专门化为不同类型。
- 两端区间通过连续性约束保证函数平滑，且整体 alpha 值被稳定在可控范围内。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_UZ00ac4eqA/figures/002_Figure_2.jpg]]
*Figure 2: Adaptive alpha modulation function of the frequencydifferentiated Gaussian kernel. The piecewise activation function*

通过联合优化 $\lambda$ 和 $\beta$，FDGK 使高斯在训练过程中自动分化为高频和低频类型：高频高斯用锐利衰减捕捉纹理边缘，低频高斯用平滑衰减覆盖均匀区域，**减少了对密集重叠的依赖**，从而为变形网络释放了运动建模的自由度。

### 3.3 傅里叶变形网络（FDN）与频率感知门控

FDN 的目标是在 FDGK 解耦表现力的基础上，进一步让变形网络能够同时捕捉**高频局部变形**和**低频全局运动**。

**低频特征提取**：将 4D 坐标 $(x,y,z,t)$ 分解为四个 3D 哈希编码，分别提取空间特征和时间特征：

$$f _ { \mathrm { s p a } } = \mathrm { M L P } \big ( H _ { x y z } ( x , y , z ) \big ) , \quad f _ { \mathrm { t e m } } = \mathrm { M L P } \big ( \mathrm { c o n c a t } \big [ H _ { x y t } ( x , y , t ) , H _ { x z t } ( y , z , t ) , H _ { y z t } ( x , z , t ) \big ] \big )$$

其中 $H_{xyz}$ 编码空间结构，$H_{xyt}$、$H_{xzt}$、$H_{yzt}$ 分别从三个正交时空平面捕获运动信息，经拼接和 MLP 融合得到时间特征 $f_{tem}$。

**高频傅里叶嵌入**：为每个高斯显式注入时变高频信息。从空间特征 $f_{spa}$ 通过 MLP 预测 $m$ 个傅里叶分量的幅度系数：

$$[ w _ { 1 } , \ldots , w _ { m } ] = \mathrm { M L P } ( f _ { \mathrm { s p a } } )$$

然后构造每点的高频傅里叶嵌入：

$$f _ { \mathrm { f r e } } = \left[ w _ { 1 } \sin ( \pi \gamma _ { 1 } t ) , \quad w _ { 1 } \cos ( \pi \gamma _ { 1 } t ) , \quad . . . , \quad w _ { m } \sin ( \pi \gamma _ { m } t ) , \quad w _ { m } \cos ( \pi \gamma _ { m } t ) \right] ^ { \mathrm { T } }$$

其中 $\gamma_k$ 为预设的频率基。幅度 $w_k$ 由空间特征决定，意味着**不同空间位置的高斯可以具有不同的高频运动幅度**——例如，运动剧烈的区域获得更大的高频分量，静态区域则幅度趋近于零。这种设计将运动轨迹建模为多个频率的周期运动叠加，使网络能精确捕捉快速、细微的局部变形。

高低频特征融合后输入多头部解码器，输出变形参数。

**频率感知门控**：变形网络输出的关键创新是引入门控分数 $\eta$，自适应调节变形强度：

$$\mu ^ { \prime } = \eta R _ { x } \mu + \eta T _ { x } , \quad S ^ { \prime } = S + \eta \Delta s , \quad R ^ { \prime } = R + \eta \Delta r , \quad D _ { \theta } ( f _ { \mathrm { F D } } ) = \{ \eta , R _ { x } , T _ { x } , \Delta r , \Delta s \}$$

$\eta \in [0,1]$ 由网络根据每点的高低频联合特征预测，本质上是一个“动态性判别器”：对于静态或低频区域的高斯，$\eta$ 趋近于 0，抑制不必要的位移和旋转，防止网络为拟合噪声而产生虚假运动；对于高频动态区域，$\eta$ 趋近于 1，允许充分的变形自由度。这种机制使网络能**在保持低频全局运动稳定性的同时，精准建模高频局部运动**。

### 3.4 傅里叶频率损失

为在优化层面强化高频细节重建，FAGS 引入频域监督。对渲染图像 $I'$ 和真实图像 $I$ 分别进行快速傅里叶变换（FFT），提取振幅谱 $I'_{amp}$ 和 $I_{amp}$，计算 L1 损失：

$$\mathcal{L}_{\mathrm{fre}} = \| I_{\mathrm{amp}}' - I_{\mathrm{amp}} \|_1$$

该损失直接约束频域的高频分量重建质量，与空间域的 L1 和 SSIM 损失互补。消融实验（Table 4）证实，加入 $\mathcal{L}_{fre}$ 可带来额外的 PSNR 增益。

**模块间的因果链条**：FDGK 通过自适应 alpha 调制减少高斯重叠依赖 → 为变形网络释放运动建模自由度 → FDN 用傅里叶嵌入显式注入高频时变信息 → 频率感知门控 $\eta$ 自适应调节变形强度，抑制低频区域的非必要运动 → 傅里叶频率损失在频域强化高频细节优化。四个模块协同实现了“高频外观”与“高频运动”的频率解耦，从根本上缓解了标准 3DGS 在 4D 重建中的频谱冲突。

## 实验与分析

### 核心定量结果

FAGS 在合成与真实世界动态场景数据集上均取得领先性能，验证了频率感知设计对运动建模和渲染质量的双重提升。

在合成 **D-NeRF** 数据集上（Table 1），FAGS 在所有七个场景中均取得最佳 PSNR，平均 PSNR 达到 **42.76 dB**，较基于 4D 哈希编码的变形基线 **Grid4D**（Xu et al., arXiv 2024）提升 0.49 dB。SSIM 和 LPIPS 同样最优，分别为 0.995 和 0.007。值得注意的是，FAGS 在存在高频运动与复杂形变的场景（如 *Standup* 47.30 dB、*Mutant* 44.16 dB）上优势尤为明显，说明频率区分高斯核与傅里叶变形网络有效缓解了标准高斯核在高频细节与高频运动间的频谱冲突。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_UZ00ac4eqA/figures/005_Table_1.jpg]]
*Table 1: Quantitative results on D-NeRF dataset. Best and second-best results are highlighted*

在真实世界 **Neu3D** 数据集上（Table 2），FAGS 取得平均 PSNR **44.16 dB**，继续领先 Grid4D 等基线。在 **HyperNeRF** 数据集上（Table 3），FAGS 在 Rig 子集（刚性运动为主）和 Interpolation 子集（复杂插值视角）上分别取得 25.63 dB 和 **32.18 dB** 的 PSNR，尤其在 Interpolation 子集上显著超越对比方法，表明频率感知变形网络对非刚性复杂运动的泛化能力更强。由于 HyperNeRF 包含较大视角变化和稀疏输入，该结果需要结合实际场景的可视化定性判断，但定量趋势与合成数据一致。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_UZ00ac4eqA/figures/006_Table_2.jpg]]
*Table 2: Quantitative results on Neu3D dataset. The color marks the best and the second best*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_UZ00ac4eqA/figures/008_Table_3.jpg]]
*Table 3: Quantitative results on real-world HyperNeRF dataset, including 4 rig subsets (Rig) and the 6 interpolation subsets (Interpolation) . The color marks the best and the second best*

### 消融实验

消融实验在 D-NeRF 数据集上进行（Table 4），逐步移除 FAGS 的关键组件以量化各模块贡献：

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_UZ00ac4eqA/figures/010_Table_4.jpg]]
*Table 4: Quantitative ablation results on the synthetic D-NeRF dataset*

- **完整模型**：PSNR 42.76 dB。
- **移除频率区分高斯核（w/o FDGK）**：PSNR 降至 42.11 dB（−0.65 dB），降幅最大。这直接验证了 FDGK 通过自适应 alpha 调制使高斯分化为高频/低频类型，从而解耦外观细节与运动建模的核心作用。
- **进一步移除高频傅里叶嵌入（w/o FDGK, w/o HFE）**：PSNR 继续下降，表明每点傅里叶特征对捕捉高频时间变化不可或缺。
- **移除频率感知门控（w/o FG）**：性能同样受损，说明门控机制通过抑制低频点的非必要运动，有效稳定了变形场。
- **移除傅里叶频率损失（w/o FFL）**：带来额外性能损失，证实频域约束对高频细节重建的增益。

消融可视化（Figure 8）进一步显示，移除 FDGK 后运动模糊明显加重，移除 HFE 后高频运动区域（如快速旋转的关节）出现拖影，与定量结果一致。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_UZ00ac4eqA/figures/011_Figure_8.jpg]]
*Figure 8: Ablation study visualization results on D-Nerf dataset*

### 关键机制验证

**高斯频率分化过程**（Figure 7）：训练过程中，可学习参数 λ 和 β 的分布逐步分化为两个峰，分别对应高频锐利核和低频平滑核；频率感知门控 η 的分布也呈现双峰，表明网络自动识别动态与静态高斯并施加差异化变形强度。这一自组织分化是 FAGS 有效性的微观基础。

**运动频谱分析**（Figure 11）：时间运动功率谱显示，FAGS 将更多高斯集中在高频带，而基线方法的高斯运动能量主要集中在低频段。这直接证明 FAGS 的傅里叶变形网络成功捕捉了高频局部运动，而非像标准变形网络那样偏向低频均匀轨迹。

**静态场景泛化**（Figure 9）：在 Mip360-NeRF 3D 静态数据集上，FAGS 的 FDGK 模块仍能通过分化高斯提升细节重建，说明频率区分核不仅适用于动态场景，对静态高频纹理同样有效。

**运动模糊鲁棒性**（Figure 10）：在与模糊感知方法 **BARD-GS**（Lu et al., CVPR 2025）的对比中，FAGS 在运动模糊场景下展现出更清晰的运动边界，表明频率感知变形网络从根源上减少了模糊产生，而非仅在渲染端进行模糊补偿。

### 失败模式与局限

论文未明确报告失败案例或局限性分析。基于方法设计，可推断以下潜在风险需手动验证：（1）FDGK 的分段线性调制函数引入额外可学习参数 λ 和 β，在稀疏视角或极短序列下可能导致分化不稳定；（2）傅里叶频率损失依赖 FFT 振幅谱的 L1 损失，对光照突变或非周期性运动可能引入频域伪影；（3）FAGS 以 Grid4D 为变形骨干，继承了 4D 哈希编码在极长序列上的内存开销问题。以上推断需在实际部署中进一步确认。

### 补充图表

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_UZ00ac4eqA/figures/015_Figure_11.jpg]]
*Figure 11: Temporal Motion Power Spectrum of Gaussians*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_UZ00ac4eqA/figures/012_Figure_7.jpg]]
*Figure 7: Distributions of frequency-differentiated parameters*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_UZ00ac4eqA/figures/013_Figure_9.jpg]]
*Figure 9: Qualitative results on the Mip360-NeRF 3D dataset*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_UZ00ac4eqA/figures/014_Figure_10.jpg]]
*Figure 10: Qualitative comparisons on the motion-blur dataset*

## 方法谱系与知识库定位

### 核心问题与动机

动态场景重建（4D reconstruction）的主流范式之一是基于变形的动态高斯溅射（deformation-based dynamic Gaussian Splatting）。这类方法在规范空间（canonical space）中维护一组3D高斯，通过变形网络预测每一时刻的位移、旋转和缩放变化，将高斯变换到观测空间进行渲染。然而，现有方法面临一个关键的频谱冲突：**标准高斯核的固定不透明度衰减函数迫使变形网络同时承担两项矛盾的任务**——一方面需要密集的高斯重叠来再现高频外观细节，另一方面需要驱动这些高斯进行一致的运动建模。这种双重负担使网络偏向学习平滑、低频的均匀运动轨迹，在新视角下产生严重的运动模糊（motion blur），尤其在高频细节区域（如边缘、纹理）表现尤为明显。

### 方法谱系定位

FAGS的提出建立在以下几条技术脉络的交汇点上：

**1. 3D高斯溅射（3DGS）及其动态扩展**

静态场景表示方面，**3DGS**（Kerbl et al., ACM TOG 2023）以显式高斯基元替代隐式表示，通过可微光栅化和alpha混合实现实时高质量渲染。在动态场景领域，**DeformGS**（Yang et al., CVPR 2024）率先将变形场引入3DGS，在规范空间中学习每个高斯的时变位移。**Grid4D**（Xu et al., arXiv 2024）进一步引入4D哈希编码和MLP变形网络，通过时空分解编码提升变形建模能力，成为当前变形驱动方法的强基线。FAGS直接以Grid4D为变形骨干（deformation backbone），在其基础上进行频谱感知的改造。

**2. 高斯核表达能力的改进**

针对标准高斯核表达力的局限，**DRK**（Huang et al., CVPR 2025）提出可变形径向核，通过插值不同的径向基函数来增强高斯对复杂形状的拟合能力。FAGS走了一条不同的路径：不改变高斯核的径向基形式，而是通过**自适应alpha调制函数**使高斯在优化过程中分化为高频（锐利）和低频（平滑）两种类型，从而显式解耦高/低频表现力。

**3. 运动模糊与频率感知**

**BARD-GS**（Lu et al., CVPR 2025）关注运动模糊问题，从模糊核估计和去模糊的角度处理动态场景重建。FAGS则从频率域的根本原因出发，通过**傅里叶变形网络**和**频率感知门控**直接建模高频时间变化，从源头上减少运动模糊的产生。

### 关键技术贡献与因果机制

FAGS的核心贡献可归纳为四个协同工作的模块，形成一个完整的频率感知动态重建管线：

**（1）频率区分高斯核（FDGK）——解耦高/低频表现力**

FDGK是FAGS最根本的创新。标准3DGS中，alpha值由不透明度 $o_i$ 和固定的指数衰减函数计算：
$$C ( \mathbf { p } ) = \sum _ { i = 1 } ^ { N } c _ { i } \alpha _ { i } \prod _ { j = 1 } ^ { i - 1 } ( 1 - \alpha _ { j } ) , \quad \alpha _ { i } = o _ { i } \exp \Big [ - \frac { 1 } { 2 } ( p - \mu ^ { 2 D } i ) ^ { T } ( \Sigma ^ { 2 D } i ) ^ { - 1 } ( p - \mu _ { i } ^ { 2 D } ) \Big ]$$

FAGS将其推广为广义alpha计算，引入可学习的线性调制函数 $\psi(g)$：
$$\alpha _ { i } = \operatorname* { m i n } ( o _ { i } \psi ( g ) , 0 . 9 9 ) , \quad \psi ( g ) = r g + b , \quad \mathrm { w h e r e ~ } g = \exp \Big [ - \frac { 1 } { 2 } ( { \bf p } - { \mu } _ { i } ^ { 2 D } ) ^ { T } ( \Sigma _ { i } ^ { 2 D } ) ^ { - 1 } ( { \bf p } - { \mu } _ { i } ^ { 2 D } ) \Big ]$$

进一步，将 $\psi(g)$ 设计为分段线性激活函数，由两个可学习参数控制：
$$\psi ( g ) = \left\{ \begin{array} { l l } { \frac { 0 . 5 + \lambda - 0 . 5 \beta - \lambda \beta } { 0 . 5 + \lambda - \beta } g , } & { g \in [ 0 , p _ { l } ) , } \\ { ( 0 . 5 + \lambda ) g + ( 0 . 2 5 - 0 . 5 \lambda ) , } & { g \in [ p _ { l } , p _ { r } ] , } \\ { \frac { 0 . 5 + \lambda - 0 . 5 \beta - \lambda \beta } { 0 . 5 + \lambda - \beta } ( g - 1 ) + 1 , } & { g \in ( p _ { r } , 1 ] , } \end{array} \right.$$

其中 $\lambda$ 控制频率倾向（高频高斯获得更陡峭的衰减，低频高斯获得更平缓的衰减），$\beta$ 控制区分区域的宽度。这种设计的因果效应是：**高频高斯变得更锐利，减少了对密集重叠的依赖，使变形网络可以专注于运动建模而非外观补偿**。

**（2）傅里叶变形网络（FDN）——捕捉高频时间变化**

FDN在Grid4D的4D哈希编码基础上，为每个高斯引入高频傅里叶嵌入：
$$f _ { \mathrm { f r e } } = \left[ w _ { 1 } \sin ( \pi \gamma _ { 1 } t ) , \quad w _ { 1 } \cos ( \pi \gamma _ { 1 } t ) , \quad . . . , \quad w _ { m } \sin ( \pi \gamma _ { m } t ) , \quad w _ { m } \cos ( \pi \gamma _ { m } t ) \right] ^ { \mathrm { T } }$$

其中幅度系数由空间特征MLP预测：$[ w _ { 1 } , \ldots , w _ { m } ] = \mathrm { M L P } ( f _ { \mathrm { s p a } } )$。这种设计将运动轨迹建模为多个频率周期运动的叠加，使网络能够显式捕捉高频局部变形。

**（3）频率感知门控——自适应调制变形强度**

变形网络的输出通过频率感知门控 $\eta$ 进行调制：
$$\mu ^ { \prime } = \eta R _ { x } \mu + \eta T _ { x } , \quad S ^ { \prime } = S + \eta \Delta s , \quad R ^ { \prime } = R + \eta \Delta r , \quad D _ { \theta } ( f _ { \mathrm { F D } } ) = \{ \eta , R _ { x } , T _ { x } , \Delta r , \Delta s \}$$

门控 $\eta$ 预测每个高斯的动态性：对于静态或低频区域的高斯，$\eta$ 趋近于0，抑制非必要运动；对于高频动态区域，$\eta$ 保持较大值，允许充分的变形表达。这有效防止了低频高斯被强制学习高频运动而引入噪声。

**（4）傅里叶频率损失——频域监督**

除传统的L1和SSIM损失外，FAGS增加傅里叶频率损失：
$$\mathcal{L}_{\mathrm{fre}} = \| I_{\mathrm{amp}}' - I_{\mathrm{amp}} \|_1$$

该损失在渲染图像与真实图像的FFT振幅谱之间计算L1距离，直接强化高频细节的重建质量。

### 适用边界与局限

**适用场景**：FAGS在合成数据集（D-NeRF）、真实多相机数据集（Neu3D）和单相机数据集（HyperNeRF）上均展现出最优或次优性能，表明其对不同数据采集方式具有良好的泛化性。特别是在包含快速运动或高频细节的场景中（如D-NeRF的Bouncing Balls、Standup），FAGS的优势更为显著。

**潜在局限**（需手动验证）：
- 计算开销：FDGK为每个高斯引入额外的可学习参数（$\lambda$、$\beta$），FDN增加了傅里叶嵌入的计算，整体训练和推理开销可能高于Grid4D等基线。论文未提供详细的运行时间或显存对比。
- 静态场景适用性：FDGK的频率分化机制主要针对动态场景中的频谱冲突设计，在纯静态场景（如Mip360-NeRF）上的增益可能有限。
- 超参数敏感性：傅里叶嵌入的频率数量 $m$ 和频率损失权重 $\sigma_{\mathrm{fre}}$（默认0.3）可能需要针对不同场景进行调整。

### 开放问题

1. **频率分化的理论保证**：FDGK通过优化自动实现高斯分化，但分化过程缺乏显式约束。是否存在某些场景下分化失败（如所有高斯退化为同一类型）的风险？论文通过训练过程中的参数分布可视化（Figure 7）展示了分化的发生，但未讨论失败模式。

2. **与模糊感知方法的互补性**：FAGS从频率域预防运动模糊，BARD-GS从图像域处理模糊。两者在原理上互补，但联合使用的效果和兼容性尚未探索。

3. **扩展到更复杂的变形拓扑**：当前方法假设变形是连续且可微的，对于拓扑变化（如物体出现/消失、断裂）的场景，频率感知门控和傅里叶嵌入是否仍然有效，需要进一步研究。

## 原文 PDF

![[paperPDFs/ICLR_2026/Frequency_aware_Dynamic_Gaussian_Splatting_a82166feb7da.pdf]]