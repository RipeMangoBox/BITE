---
title: "DeblurGS: Gaussian Splatting for Camera Motion Blur"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/DeblurGS_Gaussian_Splatting_for_Camera_Motion_Blur.pdf
project_link: null
code_link: null
aliases:
- DeblurGS
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 高斯致密化退火策略与子帧对齐参数。通过在高斯致密化过程中逐步降低阈值退火，避免在相机运动未充分优化时生成错误位置的高斯球；可学习的子帧对齐参数使离散采样子帧位姿能更准确地还原真实模糊轨迹，从而在噪声位姿条件下仍能稳定恢复精细的清晰 3D 场景。
primary_logic: 利用 3D Gaussian Splatting 的精细表达能力，通过可微的物理模糊模拟（Bézier 曲线轨迹 + 子帧对齐 + 伽马校正）将合成的模糊视图与输入模糊观测对齐，实现相机运动与清晰场景的联合优化；退火策略确保位姿收敛前避免错误高斯分裂，从而从噪声初始相机位姿中稳健地重建出高质量的清晰 3D 场景。
claims:
- DeblurGS 是唯一能在仅从模糊图像获取的噪声 COLMAP 位姿初始化（ExBlur-NP）下恢复出接近真实清晰场景的方法，其他方法均失效。
- 去除高斯致密化退火策略会产生由错误位置高斯球导致的漂浮伪影，并显著降低重建质量。
- 可学习的子帧对齐参数 ν 相比均匀采样能提高模糊合成的准确性，定量指标有所提升。
- 去除时间平滑损失 Lsmooth 会导致渲染出现抖动伪影，指标下降。
---

# DeblurGS: Gaussian Splatting for Camera Motion Blur

> [!tip] 核心洞察
> 利用 3D Gaussian Splatting 的精细表达能力，通过可微的物理模糊模拟（Bézier 曲线轨迹 + 子帧对齐 + 伽马校正）将合成的模糊视图与输入模糊观测对齐，实现相机运动与清晰场景的联合优化；退火策略确保位姿收敛前避免错误高斯分裂，从而从噪声初始相机位姿中稳健地重建出高质量的清晰 3D 场景。

| 字段 | 内容 |
|------|------|
| 中文题名 | DeblurGS：用于相机运动模糊的高斯溅射 |
| 英文题名 | DeblurGS: Gaussian Splatting for Camera Motion Blur |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2404.11358) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DeblurGS |
| Dataset | Real Motion Blur, Synthetic Extreme Blur |

> [!tip] 效果简介
> - Real Motion Blur 上，PSNR (dB) 26.28 vs 25.49 (DeblurNeRF) (+0.79)。
> - Synthetic Extreme Blur 上，PSNR (dB) 30.23 vs 23.98 (DeblurNeRF) (+6.25)。

## 概要

从运动模糊的多视图图像中恢复清晰的 3D 场景，是真实世界视觉重建中的关键瓶颈。其根本困难在于：运动模糊导致 SfM（Structure-from-Motion）估计的初始相机位姿包含显著误差，而现有基于 NeRF 的去模糊方法通常假设已知精确位姿，难以应对真实拍摄场景的高噪声位姿初始化。DeblurGS 的核心洞察是，利用 **3D Gaussian Splatting** 的精细表达能力，通过可微的物理模糊模拟——包括 Bézier 曲线轨迹、可学习子帧对齐参数与伽马校正——将合成的模糊视图与输入模糊观测对齐，实现相机运动与清晰场景的联合优化；同时引入**高斯致密化退火策略**，确保在位姿收敛前避免错误的高斯分裂，从而从噪声初始相机位姿中稳健地重建出高质量的清晰 3D 场景。

在 Real Motion Blur 和 Synthetic Extreme Blur 两个基准上，DeblurGS 分别取得 26.28 dB 和 30.23 dB 的 PSNR，相比 DeblurNeRF 提升 0.79 dB 和 6.25 dB。更具决定性的是，在仅从模糊图像获取噪声 COLMAP 位姿的 ExBlur-NP 设定下，DeblurGS 是唯一能恢复出接近真实清晰场景的方法，其他方法均失效（Fig. 6）。消融实验进一步证实，去除高斯致密化退火会产生由错误位置高斯球导致的漂浮伪影；去除可学习子帧对齐参数或时间平滑损失均导致渲染质量显著下降（Table 2）。该方法已在一段手持手机快速拍摄的 6 秒模糊视频上验证了其真实场景适用性（Fig. 7）。



### 问题背景：相机运动模糊对三维重建的挑战

在手持设备拍摄或快速场景扫描等实际应用中，相机运动模糊是普遍存在的退化现象。当曝光时间内相机发生非平凡位移时，传感器累积的光线来自不同视角的场景点，导致图像产生方向性拖影。这种模糊不仅降低了单帧图像的视觉质量，更严重的是，它破坏了多视图几何的一致性假设，使得从模糊图像中恢复清晰的三维场景成为一个极具挑战性的病态问题。

传统的去模糊方法通常在二维图像域进行操作，试图从单张模糊图像估计出清晰图像。然而，这类方法忽略了多视图之间的三维几何约束，无法为后续的新视角合成提供一致的三维表示。近年来，基于神经辐射场（NeRF）的方法尝试将去模糊与三维重建统一在一个可微框架中，但面临着一个核心瓶颈：**运动模糊导致 SfM（Structure-from-Motion）估计的初始相机位姿包含显著误差**，而现有基于 NeRF 的去模糊方法通常假设已知精确位姿，难以应对真实拍摄场景的高噪声位姿初始化。

### 现有方法的缺口

在 DeblurGS 提出之前，已有若干工作尝试在 NeRF 框架下处理运动模糊。**DeblurNeRF**（Ma et al., CVPR 2022）使用 2D 逐像素模糊核估计来建模模糊过程，但逐像素核缺乏物理基础，难以准确描述由相机刚体运动引起的全局模糊。**DP-NeRF**（Lee et al., CVPR 2023）引入了物理先验，但依然受限于 NeRF 的隐式表示效率。**BAD-NeRF**（Wang et al., CVPR 2023）尝试联合优化位姿与场景，但其优化能力在面对严重模糊时仍然不足。**ExBluRF**（Lee et al., ICCV 2023）采用 Bézier 曲线在 se(3) 空间显式建模相机运动轨迹，是当时最接近物理真实的方法，但其基于 NeRF 的隐式场景表示在表达精细几何和纹理细节方面存在固有局限，且训练和渲染速度较慢。

这些方法的共同缺口在于：**场景表示的表达能力有限，且缺乏对噪声位姿初始化的鲁棒优化机制**。当 COLMAP 从模糊图像中估计的初始位姿存在显著偏差时，NeRF 的隐式表示难以在错误几何先验下收敛到正确的清晰场景。

### 3D Gaussian Splatting 带来的新机遇

**3DGS**（Kerbl et al., TOG 2023）作为一种显式三维场景表示方法，通过各向异性三维高斯球集合对场景进行参数化，并以高效的可微光栅化实现实时渲染。与 NeRF 的隐式 MLP 表示相比，3DGS 具有两个关键优势：其一，显式的高斯基元使得场景几何的优化更加直接和精确；其二，其快速的渲染能力使得在训练过程中进行多次子帧采样的计算代价变得可接受。

然而，直接将 3DGS 应用于模糊图像训练会导致灾难性失败——模糊观测与清晰渲染之间的不一致会驱使高斯基元在错误位置分裂，产生大量漂浮伪影，无法恢复任何有意义的清晰场景。因此，**如何在 3DGS 框架中有效建模相机运动模糊，并在噪声位姿条件下稳健地联合优化场景与运动，成为一个亟待解决的关键问题**。

### 本文动机与核心思路

DeblurGS 的动机源于一个关键洞察：**利用 3D Gaussian Splatting 的精细表达能力，通过可微的物理模糊模拟将合成的模糊视图与输入模糊观测对齐，可以实现相机运动与清晰场景的联合优化**。具体而言，DeblurGS 在 se(3) 空间使用 Bézier 曲线参数化每帧曝光时间内的相机运动轨迹，通过可学习的子帧对齐参数校准离散采样子帧位姿，使累积渲染的模糊图像更准确地还原真实模糊过程。在此基础上，引入**高斯致密化退火策略**——在训练过程中逐步降低致密化阈值，确保相机运动未充分优化时不会在错误位置生成高斯基元，从而从噪声初始相机位姿中稳健地重建出高质量的清晰 3D 场景。

这一设计使得 DeblurGS 成为首个能够在仅从模糊图像获取的噪声 COLMAP 位姿初始化条件下，成功恢复接近真实清晰场景的方法，填补了现有工作在噪声位姿鲁棒性与场景表达精细度之间的双重缺口。



## 核心方法与创新机理

DeblurGS 的核心创新在于将 **3D Gaussian Splatting（3DGS）** 的精细显式表达引入相机运动去模糊问题，并通过三项关键设计使系统能够在**仅从模糊图像获取的噪声初始位姿**下稳健地联合优化相机运动与清晰场景。这与现有基于 NeRF 的去模糊方法形成根本差异——后者通常依赖较精确的初始位姿，或需要清晰-模糊配对图像来估计位姿。

### 创新一：3D Gaussian Splatting 替代 NeRF 作为场景表示

DeblurGS 将场景表示从隐式辐射场（NeRF）替换为显式的 3D 高斯基元（**3DGS** (Kerbl et al., TOG 2023)）。这一替换并非简单的“换 backbone”，而是带来了两方面的结构性优势：

1. **精细的几何与纹理表达能力**：3DGS 通过显式的高斯椭球体及其协方差矩阵直接建模场景几何，配合 alpha 混合渲染（公式 2），能够以远高于 NeRF 的细节保真度恢复清晰场景。这在运动模糊的退化条件下尤为关键——模糊观测提供的信息密度远低于清晰图像，隐式场容易陷入过度平滑，而显式基元能更有效地抓住高频细节。
2. **与物理模糊模拟的自然兼容**：3DGS 的渲染函数 $\mathcal{R}_G(\mathbf{P})$（公式 3）直接接受相机位姿 $\mathbf{P}$ 作为输入，使得在曝光时间内多次渲染子帧（公式 4-7）的计算流程更加直接高效。

### 创新二：可学习的子帧对齐参数

现有基于 Bézier 曲线建模相机运动的方法（如 **ExBluRF** (Lee et al., ICCV 2023)）通常假设子帧在曝光区间内均匀采样。然而，如图 3 所示，即使相机轨迹估计正确，均匀采样的子帧位姿也无法准确对应真实的曝光时刻，导致合成的模糊图像与观测之间存在系统性偏差。

DeblurGS 引入**可学习的子帧对齐参数** $\nu$（公式 5-6），使离散采样子帧位姿 $\hat{\mathbf{P}}(\nu_i)$ 能够自适应地校准到真实曝光时刻 $\tau_i$。这一设计的因果逻辑是：

- **瓶颈**：均匀采样假设在真实场景中不成立，导致模糊合成的系统误差，进而污染梯度信号，使相机运动优化偏离真实轨迹。
- **机制**：通过对齐参数 $\nu$ 的可微优化，梯度可以从模糊重建损失 $\mathcal{L}_{\text{rgb}}$ 反向传播至采样区间的调整，使子帧位姿逐步逼近真实曝光位置。
- **证据**：消融实验（Table 2）表明，去除对齐参数（改用均匀采样）会降低模糊合成精度，定量指标（PSNR/SSIM/LPIPS）均出现下降。

### 创新三：高斯致密化退火策略

这是 DeblurGS 在噪声位姿条件下仍能稳定重建的关键设计。标准 3DGS 使用固定的致密化阈值来控制高斯球的分裂与克隆，但在去模糊场景中，训练初期的相机运动估计尚未收敛，基于错误位姿的梯度会诱导在错误位置生成高斯基元，产生**漂浮伪影**（floating artifacts）。

DeblurGS 提出**高斯致密化退火**策略：
- 训练初期设置较高的致密化阈值 $\theta$，抑制高斯分裂，防止在相机运动未收敛时产生错误基元。
- 随着优化的进行，逐步降低阈值，允许在已收敛的几何结构上精细化场景细节。

这一设计的因果机制是：**先锁定粗结构，再细化细节**——在相机位姿的优化信号稳定之前，避免不可逆的错误几何提交。消融实验（Table 2）证实，使用固定阈值（无退火）会产生明显漂浮伪影并显著降低重建质量。

### 创新四：时间平滑损失与退火权重

DeblurGS 引入相邻子帧渲染之间的 L2 平滑损失 $\mathcal{L}_{\text{smooth}}$（公式 9），强制相机运动轨迹上的渲染一致性。这一损失并非简单的正则化项，而是对物理模糊过程的约束：在极短的曝光时间内，相邻子帧对应的场景外观应高度相似，剧烈变化通常意味着相机运动估计错误或场景几何缺陷。

损失权重 $\lambda$ 采用退火策略，从 0.05 逐步降至 0.01（公式 10）。其逻辑与致密化退火一致：训练初期相机运动误差较大，过强的平滑约束会阻碍运动参数的探索；随着运动收敛，增强平滑约束以消除抖动伪影。消融实验（Table 2）表明，去除 $\mathcal{L}_{\text{smooth}}$ 会导致渲染出现明显抖动伪影，所有指标均下降。

### 创新之间的协同关系

上述四项创新并非孤立设计，而是形成了一条**从噪声位姿到清晰场景的因果链**：

1. **3DGS 场景表示**提供了精细表达的上限；
2. **子帧对齐参数**确保模糊合成的精度，为运动优化提供准确的梯度信号；
3. **致密化退火**保护场景几何在运动收敛前不被错误提交；
4. **时间平滑损失**在运动收敛后消除残余抖动，提升渲染一致性。

这一协同机制使 DeblurGS 成为**唯一能在仅从模糊图像获取的噪声 COLMAP 位姿初始化（ExBlur-NP）下恢复出接近真实清晰场景的方法**（Fig. 6），而其他方法（DeblurNeRF、DP-NeRF、BAD-NeRF、ExBluRF）在此设置下均失效。



DeblurGS 的目标是从一组因相机运动而模糊的多视图观测中恢复出清晰的 3D 场景。其核心思路是将物理模糊过程建模为曝光时间内多个子帧清晰图像的累积，并通过可微渲染将这一过程嵌入到 3D Gaussian Splatting（3DGS）的优化框架中，从而实现对相机运动轨迹与清晰场景的联合优化。

### 输入输出定义

- **输入**：$M$ 张因相机运动导致模糊的观测图像 $\{\mathbf{B}_i\}_{i=1}^M$，以及由 COLMAP SfM 从这些模糊图像中估计的初始（噪声）相机位姿。
- **输出**：一个经过优化的清晰 3DGS 场景表示 $G$（由一组高斯基元构成），以及每帧曝光时间内相机在 $\mathrm{se}(3)$ 空间中的运动轨迹参数。推理阶段仅保留场景 $G$，可从任意新视角渲染清晰图像。

### 训练管线模块

整体训练流程如 Fig. 2 所示，包含以下核心模块：

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2404_11358/figures/002_Figure_2.jpg]]
*Figure 2: Training pipeline of DeblurGS. We simulate the physical blur operation while the camera is moving. In our optimization, the blurry images {Bˆi}Mi=1 are reconstructed by accumulating rendered images along with the estimated camera trajectories. We minimize L1 loss*

1. **相机位姿初始化**  
   对所有模糊观测执行 COLMAP SfM，获取每帧的初始相机位姿。这些位姿通常包含由运动模糊引入的显著误差，构成后续联合优化的起点。

2. **相机运动估计**  
   将每帧的相机刚体运动参数化为 $\mathrm{se}(3)$ 空间中的 Bézier 曲线，并引入可学习的子帧对齐参数 $\nu$ 来校准离散采样子帧位姿与真实曝光时刻的对应关系（详见 Fig. 3）。这一设计使得即使初始轨迹不准确，优化后的子帧位姿也能更精确地还原真实模糊轨迹。

3. **模糊视图合成**  
   对每一帧，从估计的子帧位姿 $\{\hat{\mathbf{P}}_i\}_{i=1}^N$ 渲染 $N$ 张清晰子帧图像，取平均后施加伽马校正 $\gamma(\cdot)$，得到合成的模糊图像：
   $$
   \hat{\mathbf{B}}(G) = \gamma\left(\frac{1}{N} \sum_{i=1}^{N} \mathcal{R}_G(\hat{\mathbf{P}}_i)\right)
   $$
   其中 $\mathcal{R}_G(\cdot)$ 表示从 3DGS 场景 $G$ 在给定位姿下渲染清晰图像。

4. **高斯致密化退火**  
   在训练过程中逐步降低 3DGS 的致密化阈值 $\theta$。初始阶段采用较高阈值抑制高斯分裂，避免在相机运动尚未充分收敛时于错误位置生成高斯基元；随着位姿优化逐步改善，阈值降低以允许场景细节的精细表达。

5. **损失计算与联合优化**  
   总损失由两部分组成：
   $$
   \mathcal{L} = \mathcal{L}_{\mathrm{rgb}} + \lambda \mathcal{L}_{\mathrm{smooth}}
   $$
   - **重建损失** $\mathcal{L}_{\mathrm{rgb}} = \sum_i \|\mathbf{B}_i - \hat{\mathbf{B}}_i\|_1$：约束合成模糊图像与输入模糊观测的 L1 一致性。
   - **时间平滑损失** $\mathcal{L}_{\mathrm{smooth}}$：惩罚相邻子帧渲染之间的 RGB 差异，强制相机运动轨迹上渲染内容的时序平滑性，防止抖动伪影。
   - 权重 $\lambda$ 在训练过程中从 0.05 退火至 0.01。

### 数据流与优化闭环

模糊观测 $\mathbf{B}_i$ → 初始位姿 → Bézier 曲线参数化 + 对齐参数 $\nu$ → 子帧位姿 $\hat{\mathbf{P}}_i$ → 3DGS 渲染子帧 → 累积 + 伽马校正 → 合成模糊图 $\hat{\mathbf{B}}_i$ → 与 $\mathbf{B}_i$ 比较计算 $\mathcal{L}_{\mathrm{rgb}}$，同时计算 $\mathcal{L}_{\mathrm{smooth}}$ → 反向传播更新场景参数 $G$、Bézier 曲线控制点及对齐参数 $\nu$。这一闭环使得相机运动与清晰场景在统一的可微框架下协同优化。

### 关键设计动机

该框架的核心瓶颈在于：运动模糊导致 SfM 估计的初始位姿包含显著误差，而现有基于 NeRF 的去模糊方法通常假设已知精确位姿，难以应对真实拍摄场景的高噪声位姿初始化。DeblurGS 通过两个关键机制应对这一挑战：

- **高斯致密化退火**：防止位姿未收敛前在错误位置生成高斯基元，从而避免漂浮伪影。
- **可学习子帧对齐参数**：使离散采样子帧位姿能更准确地还原真实模糊轨迹，提升模糊合成的精度。

两者协同作用，使得 DeblurGS 能够在仅从模糊图像获取的噪声 COLMAP 位姿初始化（ExBlur-NP 设置）下，仍能稳定恢复出高质量的清晰 3D 场景——这是其他对比方法均无法实现的能力（见 Fig. 6）。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2404_11358/figures/001_Figure_1.jpg]]
*Figure 1: Novel View Synthesis with Blurry Views. Our DeblurGS achieves stateof-the-art performance in novel view synthesis and deblurring compared to previous approaches*



DeblurGS 的核心流程可概括为：从模糊多视图观测出发，通过可微的物理模糊模拟，将 3D Gaussian Splatting 渲染的清晰子帧累积为合成模糊图像，并与输入模糊观测对齐，从而联合优化相机运动轨迹与清晰 3D 场景（图 Fig. 2）。以下逐一剖析其关键模块与公式。

### 3D Gaussian Splatting 场景表示

DeblurGS 采用 **3DGS** (Kerbl et al., TOG 2023) 作为底层场景表示。场景由一组各向异性 3D 高斯基元 $G$ 构成，每个基元携带位置均值 $\mathbf{x}_i$、协方差 $\Sigma_i$、颜色 $c_i$ 和不透明度 $\alpha_i$。给定相机位姿 $\mathbf{P}$，3D 高斯通过投影变换映射到 2D 图像平面：

$$
\mathbf{x}_{\mathrm{2D},i} = \mathbf{P} \mathbf{x}_i, \quad \Sigma_{\mathrm{2D},i} = J \mathbf{P} \Sigma_i \mathbf{P}^{\mathsf{T}} J^{\mathsf{T}} \tag{1}
$$

其中 $J$ 为投影变换的雅可比矩阵。随后，对像素 $\mathbf{x}$ 覆盖的所有高斯按深度排序，通过 alpha 混合计算 RGB 值：

$$
\hat{c}(\mathbf{x}) = \sum_{i=1}^{|G|} \left( \prod_{j=1}^{i-1} (1 - \alpha_j(\mathbf{x})) \right) \alpha_i(\mathbf{x}) c_i \tag{2}
$$

整幅图像的渲染函数记为：

$$
\mathcal{R}_G(\mathbf{P}) = \{ \hat{c}(\mathbf{x}) \mid \mathbf{x} \in \mathcal{P} \} \tag{3}
$$

### 相机运动建模与子帧对齐

运动模糊图像 $\mathbf{B}$ 可近似为曝光时间内 $N$ 个离散时刻清晰图像的平均：

$$
\mathbf{B} \approx \frac{1}{N} \sum_{i=1}^{N} \mathbf{I}(\mathbf{P}_{\tau_i}) \tag{4}
$$

相机运动轨迹沿用 **ExBluRF** (Lee et al., ICCV 2023) 的 Bézier 曲线在 $\mathfrak{se}(3)$ 李代数空间中的参数化方式。关键创新在于引入**可学习子帧对齐参数** $\nu$：均匀采样无法保证离散子帧位姿恰好对应真实曝光时刻的位姿，导致合成模糊与观测模糊失配（图 Fig. 3）。因此，定义对齐后的子帧位姿：

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2404_11358/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of the Sub-frame Alignment Parameters. With the estimated camera trajectory, the resulting blurry image changes based on the sampling intervals of sub-frame images. Even if the latent camera trajectory is well-optimized, the evenly sampled blurry image*

$$
\hat{\mathbf{P}}(\nu_i) \triangleq \mathbf{P}_{\tau_i} \quad \forall i \in \{1, 2, \dots, N\} \tag{5}
$$

利用对齐参数校准后，模糊图像重建为：

$$
\mathbf{B} \approx \frac{1}{N} \sum_{i=1}^{N} \mathbf{I}(\hat{\mathbf{P}}(\nu_i)) \tag{6}
$$

### 模糊视图合成与伽马校正

将上述模糊形成过程嵌入 3DGS 渲染管线：对 $N$ 个子帧位姿分别渲染清晰图像，取平均后施加**伽马校正** $\gamma(\cdot)$，得到合成模糊视图：

$$
\hat{\mathbf{B}}(G) = \gamma\left(\frac{1}{N} \sum_{i=1}^{N} \mathcal{R}_G(\hat{\mathbf{P}}_i)\right) \tag{7}
$$

伽马校正的必要性在于：真实相机传感器在 RAW 域线性累积光子，但最终输出图像经过非线性伽马映射。若忽略此步骤，暗部区域会异常增亮，破坏光度一致性，消融实验中去除 $\gamma(\cdot)$ 导致性能大幅下降（Table 2）。

### 高斯致密化退火策略

标准 3DGS 在训练中采用固定阈值触发高斯分裂/克隆。然而，在去模糊场景下，初始相机位姿来自 COLMAP 对模糊图像的 SfM 估计，包含显著误差。若在相机运动尚未充分优化时贸然致密化，会在错误位置生成高斯基元，产生漂浮伪影并难以在后续优化中消除。

DeblurGS 提出**高斯致密化退火**：训练初期设定较高致密化阈值 $\theta$，仅允许在梯度极强的区域分裂；随着相机运动逐渐收敛，逐步降低阈值，使高斯致密化在更可靠的几何基础上进行。消融实验证实，去除退火策略（使用固定阈值）会导致错误位置高斯球，显著降低重建质量（Table 2）。

### 损失函数设计

训练损失由两部分组成。**重建损失**为所有模糊观测与合成模糊视图之间的 L1 距离：

$$
\mathcal{L}_{\mathrm{rgb}} = \sum_i \|\mathbf{B}_i - \hat{\mathbf{B}}_i\|_1 \tag{8}
$$

**时间平滑损失**惩罚同一模糊图像内相邻子帧渲染之间的 RGB 差异，强制相机运动轨迹上的时序一致性：

$$
\mathcal{L}_{\mathrm{smooth}} = \frac{1}{N} \sum_{i,j} \|\mathcal{R}_G(\hat{\mathbf{P}}_{j+1}^{(i)}) - \mathcal{R}_G(\hat{\mathbf{P}}_{j}^{(i)})\|_2 \tag{9}
$$

最终优化目标为：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{rgb}} + \lambda \mathcal{L}_{\mathrm{smooth}} \tag{10}
$$

其中平滑权重 $\lambda$ 在训练过程中从 0.05 退火至 0.01。消融实验表明，去除 $\mathcal{L}_{\mathrm{smooth}}$ 会导致渲染出现明显抖动伪影，PSNR/SSIM/LPIPS 指标均下降（Table 2）。

### 推理阶段

训练完成后，丢弃相机运动参数与子帧对齐参数，仅保留优化后的 3DGS 场景 $G$。从任意新视角渲染清晰图像时，直接调用标准 3DGS 渲染管线 $\mathcal{R}_G(\mathbf{P})$，无需再进行模糊合成。



## 实验与关键发现

### 核心实验结论

DeblurGS 在多个运动模糊数据集上均取得了最优的新视角合成与去模糊性能。**Table 1** 报告了定量对比结果：在 Real Motion Blur 数据集上，DeblurGS 的 PSNR 达到 26.28 dB，相比次优方法 DeblurNeRF（25.49 dB）提升 0.79 dB；在 Synthetic Extreme Blur 数据集上，PSNR 达到 30.23 dB，相比 DeblurNeRF（23.98 dB）大幅领先 6.25 dB，验证了 3DGS 精细表达能力在极端模糊场景下的显著优势。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2404_11358/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of novel view synthesis*

从定性结果看，**Fig. 4** 展示了 Real Motion Blur 数据集上的去模糊对比——该数据集没有对应的清晰真值对，DeblurGS 恢复的清晰视图在纹理细节和几何结构上明显优于其他方法。**Fig. 5** 展示了 ExBlur-CP 数据集（使用清晰对初始化位姿）上的去模糊结果，DeblurGS 仍保持最优。最关键的是 **Fig. 6** 所示的 ExBlur-NP 场景：所有方法仅从模糊图像获取 COLMAP 噪声初始位姿，DeblurGS 是唯一能恢复出接近真实清晰场景的方法，其他方法（包括 DeblurNeRF、DP-NeRF、BAD-NeRF、ExBluRF）均出现严重退化或完全失效。这直接验证了核心瓶颈定位——噪声位姿初始化是现有方法的主要失效原因，而 DeblurGS 的退火致密化策略与子帧对齐机制有效应对了这一挑战。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2404_11358/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative comparison of sharp 3D rendering on ExBlur-NP [24]. The camera poses are initialized from COLMAP [37] with blurry observations only*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2404_11358/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative Comparison of Deblurring on Real Motion Blur [27]. Note that blurry views in Real Motion Blur do not have their ground-truth pairs*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2404_11358/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative Comparison of Deblurring on ExBlur-CP [24]. The camera poses are initialized from COLMAP [37] with sharp pairs corresponding to each blurry observation*

### 消融实验

**Table 2** 在 ExBlur 数据集的 "Camellia" 和 "Stone Lantern" 场景上对四个关键组件进行了消融分析，所有实验均使用噪声位姿初始化：

**时间平滑损失 L_smooth**：去除该损失后，相邻子帧渲染之间出现明显的抖动伪影，PSNR/SSIM/LPIPS 三项指标均下降。L_smooth 通过惩罚相邻子帧渲染的 L2 差异，强制相机运动轨迹的时域一致性，是保证渲染稳定性的关键正则项。

**高斯致密化退火**：使用固定致密化阈值（即无退火）时，相机运动尚未充分收敛的阶段会在错误位置生成高斯基元，导致渲染结果出现漂浮伪影，重建质量显著降低。退火策略从高初始阈值逐步降低，确保只有在相机运动收敛后才进行精细致密化，是 DeblurGS 在噪声位姿下仍能稳定工作的决定性因素。

**子帧对齐参数 ν**：将可学习的对齐参数替换为均匀采样后，模糊合成的精度下降，定量指标有所降低。如 **Fig. 3** 所示，即使相机轨迹估计正确，均匀采样子帧对应的合成模糊图像也可能与实际观测不匹配；可学习的 ν 参数通过校准采样区间，使离散子帧位姿更准确地还原真实模糊轨迹。

**伽马校正 γ(·)**：去除伽马校正后，暗部区域出现异常增亮，破坏了光度一致性，导致性能大幅下降。这是因为成像管线中的伽马编码使得直接在线性空间取平均无法正确模拟物理模糊过程，伽马校正补偿了这一非线性。

### 真实场景验证

**Fig. 7** 展示了使用智能手机快速移动拍摄的 6 秒视频进行清晰场景重建的结果。DeblurGS 成功从真实模糊视频中恢复出清晰的 3D 场景，证明了方法在野外采集场景下的实用性。

### 失败模式与局限性

尽管 DeblurGS 在噪声位姿初始化下表现突出，仍存在以下限制：

1. **动态物体未建模**：当前方法假设相机运动是全局刚体运动，同一曝光时间内所有像素对应相同的相机轨迹。场景中的动态物体（如行人、车辆）可能残留模糊或产生伪影，因为其运动未被显式建模。

2. **极端模糊下的初始化依赖**：方法依然依赖 COLMAP 提供初始位姿。在极端模糊或缺乏纹理特征时，SfM 完全失效的可能性存在，此时退火策略也无法收敛——这是所有依赖初始位姿的方法的共同瓶颈。

3. **超参数需手动设置**：子帧数量 N 及平滑损失权重 λ 的退火调度（从 0.05 退火至 0.01）需要针对不同场景手动调整，尚未实现自适应选择。

4. **训练计算成本增加**：每次迭代需渲染 N 个子帧（相比标准 3DGS 的单次渲染），训练时间线性增加，在 N 较大时计算开销显著。

### 公平性说明

所有对比方法均基于官方实现并使用推荐训练配置，评估指标（PSNR、SSIM、LPIPS）按标准流程计算。在 ExBlur-CP 设置下，部分基线（如 ExBluRF）可使用与模糊图像配对的清晰图像来估计初始位姿，而 DeblurGS 仅使用模糊观测进行初始化；在 ExBlur-NP 设置下，所有方法均仅从模糊图像获取 COLMAP 位姿，对比更为公平。DeblurGS 在两种设置下均保持领先，尤其在 ExBlur-NP 场景下优势显著。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2404_11358/figures/008_Table_2.jpg]]
*Table 2: Ablation study. We describe the ablation studies on each element of proposed method on "Camellia" and "Stone Lantern" scenes in ExBlur dataset with noisy camera pose setup. We ablate the effectiveness of the temporal smoothness loss Lsmooth, Gaussian densification annealing strategy, sub-frame alignment parameters ν, and the gamma correction γ(·)*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2404_11358/figures/009_Figure_7.jpg]]
*Figure 7: Sharp scene reconstruction from field-captured video. We record the real-world scene as a video with smartphone, swiftly to capture the whole environment within 6 seconds. Our method successfully reconstructs sharp scene with a real-world blurry video*



## 定位与知识库关联

### 1. 方法谱系：从 NeRF 去模糊到 3DGS 去模糊

DeblurGS 处于**相机运动模糊下的新视角合成与去模糊**这一任务线上，其直接前驱是基于 NeRF 的去模糊方法。理解 DeblurGS 的贡献，需要先厘清该谱系中几个关键节点的瓶颈传递关系。

**基于 NeRF 的去模糊基线**构成了 DeblurGS 的直接对比对象：

- **DeblurNeRF**（Ma et al., CVPR 2022）：采用 2D 逐像素模糊核估计，将模糊建模为清晰图像与模糊核的卷积。该方法的核心局限在于 2D 核难以表达由相机刚体运动引起的空间变化模糊，且不显式优化相机运动。
- **DP-NeRF**（Lee et al., CVPR 2023）：引入刚体运动先验，将模糊建模为曝光时间内多帧清晰图像的积分。相比 DeblurNeRF 更物理合理，但仍依赖 NeRF 的隐式场景表示，训练和渲染效率较低。
- **BAD-NeRF**（Wang et al., CVPR 2023）：在去模糊的同时执行 Bundle Adjustment，联合优化相机位姿和场景。这是首次尝试在去模糊框架内处理位姿噪声，但其优化能力受限于 NeRF 的表示容量和计算开销。
- **ExBluRF**（Lee et al., ICCV 2023）：使用 Bézier 曲线在 se(3) 空间中显式建模相机运动轨迹，是 DeblurGS 相机运动建模的直接基础。然而，ExBluRF 仍然基于 NeRF 的隐式辐射场，且子帧采样为均匀间隔，缺乏对采样区间对齐的显式优化。

**DeblurGS 的方法定位**可以理解为：将 ExBluRF 的 Bézier 曲线运动建模范式从 NeRF 迁移到 3D Gaussian Splatting（**3DGS**, Kerbl et al., TOG 2023），并针对 3DGS 的显式高斯基元特性引入两项关键改进——**高斯致密化退火**和**可学习子帧对齐参数**——以解决“噪声初始位姿下稳健优化”这一核心瓶颈。

### 2. 关键设计差异与因果机制

DeblurGS 相对于上述基线的本质差异体现在四个关键维度，每个维度都对应一个具体的因果机制：

**场景表示：隐式辐射场 → 显式高斯基元。** NeRF 系方法使用 MLP 编码的隐式辐射场，渲染单帧图像需要沿光线密集采样。3DGS 的显式高斯基元支持高效的 α-blending 光栅化渲染，使得在训练期间对每个模糊观测进行 N 次子帧渲染（N 通常取 11）的计算开销可控。这一效率优势是实现“联合优化相机运动与清晰场景”的工程前提。

**子帧采样：均匀采样 → 可学习对齐。** ExBluRF 在 Bézier 曲线上均匀采样子帧位姿，隐含假设曝光时间内的相机运动是匀速的。DeblurGS 引入可学习参数 ν 控制离散采样区间，使得估计的子帧位姿 $\hat{\mathbf{P}}(\nu_i)$ 能更准确地对应真实曝光时刻 $\tau_i$ 的相机位姿（Eq. 5–6）。消融实验（Table 2）证实，去除该对齐参数会导致模糊合成精度下降——这一机制直接提升了物理模糊模拟的保真度。

**致密化策略：固定阈值 → 退火策略。** 这是 DeblurGS 最关键的创新。标准 3DGS 在训练全程使用固定梯度阈值触发高斯分裂。在去模糊场景中，训练初期相机运动参数尚未收敛，基于错误位姿的梯度会触发在错误位置的高斯致密化，产生难以消除的“漂浮伪影”。DeblurGS 采用退火策略：从高初始阈值开始，随训练逐步降低阈值，确保只有在相机运动充分优化后才允许精细的高斯分裂。消融实验（Table 2）表明，去除退火策略会显著降低重建质量——这一机制是 DeblurGS 在噪声位姿（ExBlur-NP）条件下仍能稳定工作的核心原因。

**训练损失：纯重建 → 重建 + 时间平滑。** DeblurGS 引入相邻子帧渲染之间的 L2 平滑损失 $\mathcal{L}_{\mathrm{smooth}}$（Eq. 9），权重 λ 从 0.05 退火至 0.01。该损失强制相机运动轨迹上的渲染一致性，抑制因位姿估计不稳定导致的抖动伪影。消融实验（Table 2）证实去除该损失会导致指标下降和视觉伪影。

### 3. 适用边界与局限

DeblurGS 的适用性受以下边界条件约束：

1. **刚体运动假设。** 方法假设曝光时间内所有像素对应相同的全局相机刚体运动（Bézier 曲线在 se(3) 空间）。场景中的动态物体（行人、车辆等）会违反该假设，导致动态区域残留模糊或伪影。这是论文明确指出的局限。

2. **COLMAP 位姿初始化依赖。** 尽管退火策略增强了对噪声位姿的鲁棒性，但方法仍依赖 COLMAP SfM 提供初始位姿估计。在极端模糊、低纹理或重复纹理场景中，SfM 可能完全失效，此时退火策略也无法收敛。论文尚未探索与无位姿先验方法（如 Nope-NeRF、CF-3DGS）的结合可能性。

3. **超参数敏感性。** 子帧数量 N 和平滑损失权重 λ 的退火调度需要手动设置，尚未实现自适应选择。不同场景（模糊程度、运动速度）可能需要不同的参数配置，增加了实际部署的调参负担。

4. **训练计算开销。** 每个训练迭代需要对每张模糊观测渲染 N 张清晰子帧，计算成本相比标准 3DGS 线性增加。论文未提供与 NeRF 系方法的具体训练时间对比，但这一开销是显式物理模糊模拟的固有代价。

### 4. 开放问题与后续方向

从 DeblurGS 的局限出发，可以识别出以下开放问题：

- **自适应参数选择。** 能否根据输入图像的模糊程度自动确定子帧数量 N 和退火调度参数？这可以显著降低方法对人工调参的依赖，提升实用性。

- **摆脱 COLMAP 依赖。** 在严重低纹理或重复纹理场景中，能否将 DeblurGS 的退火策略与无位姿先验的联合优化框架（如 Nope-NeRF 的隐式位姿编码或 CF-3DGS 的渐进式位姿估计）结合，实现完全从模糊图像出发的端到端重建？

- **非刚性运动扩展。** 当前 Bézier 曲线建模仅适用于全局刚体运动。能否扩展至滚动快门效应（逐行曝光时间差）或更复杂的非刚性运动模糊模型？这需要重新设计运动参数化和子帧采样策略。

- **计算效率优化。** 能否通过共享子帧渲染的中间特征表示，或使用单应性近似减少实际渲染次数 N，来降低训练计算开销？这对于视频级应用的实时处理至关重要。

### 5. 在知识库中的定位

DeblurGS 在相机运动去模糊与新视角合成交叉领域占据以下位置：

- **相对于 NeRF 系去模糊方法**：DeblurGS 是首个将 3DGS 引入该任务的工作，在定量指标（PSNR 提升 +0.79 至 +6.25 dB）和视觉质量上均实现显著超越。其核心贡献不在于运动建模本身（继承自 ExBluRF），而在于揭示了“显式基元表示 + 退火致密化”这一组合对噪声位姿鲁棒性的关键作用。

- **相对于标准 3DGS**：DeblurGS 扩展了 3DGS 的适用范围，使其能够处理模糊输入。这为 3DGS 在非理想采集条件（手持拍摄、快速运动、低光照长曝光）下的应用打开了通道。

- **在更广泛的“模糊输入 3D 重建”领域**：DeblurGS 提供了一种物理驱动的可微模糊模拟范式，该范式原则上可与其他场景表示（如 2DGS、Scaffold-GS）或运动模型结合，具有一定的通用性。

**证据强度说明**：上述分析中的核心因果主张（退火策略对噪声位姿鲁棒性的关键作用、对齐参数对模糊合成精度的提升）均有消融实验（Table 2）和定性对比（Fig. 6, ExBlur-NP）的强证据支持（confidence ≥ 0.95）。关于“摆脱 COLMAP 依赖”和“非刚性运动扩展”的开放问题来自论文明确指出的局限和逻辑推演，属于合理推断但缺乏直接实验证据，需要后续工作验证。



## 原文 PDF

![[paperPDFs/arxiv_2024/DeblurGS_Gaussian_Splatting_for_Camera_Motion_Blur.pdf]]
