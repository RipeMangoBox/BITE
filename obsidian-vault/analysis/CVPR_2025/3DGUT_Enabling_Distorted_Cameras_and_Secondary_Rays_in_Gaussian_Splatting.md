---
title: "3DGUT: Enabling Distorted Cameras and Secondary Rays in Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/3DGUT_Enabling_Distorted_Cameras_and_Secondary_Rays_in_Gaussian_Splatting.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/3DGUT/
aliases:
- 33GUT
- 3EDCSRGS
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "用Unscented Transform（UT）的sigma点投影取代EWA splatting的线性化投影，并将粒子响应评估从2D图像平面迁移到3D空间的最大响应点。"
primary_logic: "通过UT近似粒子分布而非近似投影函数，可以精确处理任意非线性相机模型和滚动快门（每个sigma点可独立变换），并统一光栅化与光线追踪的渲染表达，从而在保持高帧率的同时实现次级光线效果。"
claims:
- "将EWA splatting替换为Unscented Transform，利用sigma点进行精确投影，消除对雅可比矩阵的依赖。"
- "UT方法对鱼眼相机和滚动快门均保持低且一致的KL散度，而EWA方法的误差随畸变增大而恶化。"
- "在3D空间中沿射线最大响应点评估粒子，避免了投影函数的梯度传播，与3DGRT渲染表达对齐。"
- "采用MLAB多层级alpha融合近似逐射线深度排序，使光栅化结果与追踪方法高度一致。"
---

# 3DGUT: Enabling Distorted Cameras and Secondary Rays in Gaussian Splatting

> [!tip] 核心洞察
> 通过UT近似粒子分布而非近似投影函数，可以精确处理任意非线性相机模型和滚动快门（每个sigma点可独立变换），并统一光栅化与光线追踪的渲染表达，从而在保持高帧率的同时实现次级光线效果。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 3DGUT: 在3D高斯泼溅中启用畸变相机与次级光线 |
| 英文题名 | 3DGUT: Enabling Distorted Cameras and Secondary Rays in Gaussian Splatting |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2412.12507); [GitHub](https://github.com/nv-tlabs/3dgrut); [Project](https://research.nvidia.com/labs/toronto-ai/3DGUT); [Project](https://research.nvidia.com/labs/toronto-ai/3DGUT/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 3DGUT (3D Gaussian Unscented Transform) |
| Dataset | MipNeRF360, Scannet++ (fisheye), Waymo (distorted + rolling shutter) |

> [!tip] 效果简介
> - MipNeRF360 上，LPIPS↓ 为 0.215 (Ours sorted)，对比 0.248 (3DGRT)，变化 -0.033。
> - MipNeRF360 上，FPS↑ 为 265 (Ours)，对比 52 (3DGRT)，变化 +213。
> - Scannet++ (fisheye) 上，PSNR↑ 为 29.11 (Ours sorted)，对比 28.15 (FisheyeGS)，变化 +0.96。

## 概述

3D高斯泼溅（3DGS）凭借其高保真度与实时渲染能力，已成为新视角合成的主流方法。然而，3DGS的核心光栅化管线依赖于EWA splatting对投影函数的一阶线性化近似，这使其天然受限于两个关键瓶颈：**（1）无法处理强非线性相机模型**（如鱼眼镜头、径向畸变）和**时间依赖的传感器效应**（如滚动快门），因为每种相机模型都需要单独推导雅可比矩阵；**（2）不支持次级光线**（反射、折射），因为其渲染表达与光线追踪方法在数学上不对齐。这些限制将3DGS牢牢锁定在针孔相机与直接光照的范围内，阻碍了它在自动驾驶、机器人、AR/VR等广泛使用复杂相机的场景中的应用。

本文提出**3DGUT（3D Gaussian Unscented Transform）**，以一条简洁而根本的思路同时解决上述两个问题：**用Unscented Transform（UT）近似粒子分布，而非近似投影函数**。具体而言，3DGUT用7个精心选择的sigma点来表征每个3D高斯粒子，这些sigma点可以被**精确投影**到任意非线性相机模型下，再从投影点重建2D高斯用于光栅化。这一策略彻底消除了对雅可比矩阵的依赖，使方法天然兼容鱼眼、径向畸变、滚动快门等任意相机模型——每个sigma点甚至可以独立变换不同的外参矩阵来建模滚动快门的时间依赖效应。同时，3DGUT将粒子的不透明度评估从2D图像平面迁移到3D空间中沿射线的最大响应点，使渲染表达与体积光线追踪方法（3DGRT）对齐，从而实现了**光栅化（主光线）与光线追踪（次级光线）的混合渲染**，在保持高帧率的同时解锁了反射、折射等次级光线效果。

在方法谱系中，3DGUT位于3DGS光栅化方法与3DGRT光线追踪方法的交汇点：它继承光栅化的效率优势，同时获得追踪方法的灵活性与物理正确性。实验结果表明，在标准针孔相机数据集（MipNeRF360、Tanks & Temples）上，3DGUT收敛到与3DGS相当的质量（LPIPS仅差约0.02），同时保持超过200 FPS的渲染速度；在鱼眼相机数据集Scannet++上，3DGUT以PSNR 29.11显著优于专门为该相机模型推导雅可比的FisheyeGS（28.15），且仅使用38%的高斯粒子；在Waymo自动驾驶数据集（畸变相机+滚动快门）上，3DGUT同样超越3DGRT。这些结果验证了核心洞察：**通过UT近似粒子而非近似投影，可以用统一的、无需模型定制的框架，精确处理任意非线性相机与次级光线，同时保持实时渲染能力**。

## 背景与动机

### 3D高斯泼溅的核心假设与局限

3D Gaussian Splatting（3DGS，Kerbl et al., ACM Trans. Graph. 2023）作为一种显式辐射场表示方法，凭借其高保真度与实时渲染能力，迅速成为新视角合成领域的主流方案。然而，该方法在投影渲染环节依赖椭圆加权平均泼溅（EWA Splatting），其核心操作是将3D高斯粒子投影到2D图像平面时，通过一阶泰勒展开对投影函数进行**线性化近似**：

$$\Sigma' = J_{[:2,:3]} W \Sigma W^T J_{[:2,:3]}^T$$

这一近似要求为每种相机模型**显式推导雅可比矩阵 $J$**。对于标准针孔相机，该线性化足够精确；但当面对强非线性投影函数时——例如鱼眼相机的等距投影、径向畸变模型，以及滚动快门带来的时间依赖效应——EWA的线性化误差将随非线性程度的增大而急剧恶化。

### 现有方法的缺口

上述局限造成了两个层次的方法缺口：

**第一，相机模型的通用性缺失。** 现有扩展方案（如FisheyeGS，Liao et al., arXiv 2024）试图为特定相机模型（如等距鱼眼）手动推导雅可比矩阵，但这种“逐模型适配”的策略不具备泛化能力。每当面对新型镜头或传感器时，都需要重新进行繁琐的数学推导，且无法处理滚动快门这类需要为每个像素行分配不同外参矩阵的时间依赖效应。

**第二，渲染表达的不一致性。** 3DGS的光栅化渲染与光线追踪方法（如3DGRT，Moenne-Loccoz et al., ACM Trans. Graph. 2024）在粒子响应评估上存在根本分歧：光栅化在2D投影平面上评估高斯响应，而光线追踪在3D空间中沿射线采样。这种差异使得同一场景表示无法在光栅化（主光线）与追踪（次级光线）之间无缝切换，从而限制了反射、折射等次级光线效果的实现。

### 核心动机：从近似投影到近似分布

本文的核心洞察在于**调转近似对象**：不再近似投影函数本身，而是近似3D高斯粒子的分布。具体而言，引入无迹变换（Unscented Transform, UT），用一组可被精确投影的Sigma点来表征粒子分布，再从投影后的Sigma点重建2D高斯锥形。这一策略带来三重收益：

- **相机无关性**：UT是导数无关（derivative-free）方法，无需为任何相机模型推导雅可比矩阵，天然支持任意非线性投影函数。
- **滚动快门原生支持**：每个Sigma点可独立应用不同的外参矩阵，直接将传感器运动编码进投影过程。
- **光栅化与追踪的统一**：将粒子响应评估从2D图像平面迁移到3D空间沿射线的最大响应点，使光栅化渲染表达与3DGRT对齐，为混合渲染（主光线光栅化、次级光线追踪）奠定基础。

Figure 1 直观展示了这一动机：在原始畸变鱼眼视图上训练（而非去畸变后裁剪训练）可利用全部像素提升视觉质量，同时插入的反射球与折射雕像则体现了次级光线效果的潜力。Figure 2 对比了蒙特卡洛采样、EWA线性化与UT三种投影策略的本质差异，清晰地揭示了UT“近似分布而非近似函数”的核心思想。

## 核心创新

3DGUT 的核心创新在于用一套统一的数学工具——Unscented Transform (UT)——同时解决了 3D Gaussian Splatting (3DGS) 在**非线性相机模型**、**时间依赖传感器效应**和**次级光线**三个维度上的根本性限制。其关键洞察是：**近似粒子分布，而非近似投影函数**。

### 1. 因果机制：从线性化投影到 Sigma 点近似

3DGS 依赖 EWA splatting 将 3D 高斯粒子投影到 2D 图像平面。这一投影通过一阶泰勒展开线性化投影函数实现，需要显式计算雅可比矩阵 $J$：

$$\Sigma' = J_{[:2,:3]} W \Sigma W^T J_{[:2,:3]}^T$$

这种线性化在**针孔相机**下工作良好，但面对鱼眼镜头等强非线性投影时，局部线性近似会产生显著误差，且不同相机模型需要单独推导雅可比。更重要的是，滚动快门等时间依赖效应使每个像素行对应不同的相机外参，线性化框架难以统一建模。

3DGUT 将整个范式颠倒：**用 Unscented Transform 近似 3D 高斯粒子本身，而非近似投影函数**。具体而言，每个 3D 高斯粒子被 7 个精心选择的 Sigma 点 $\pmb{x}_i$ 表征：

$$\pmb{x}_i = \begin{cases} \pmb{\mu} & i=0 \\ \pmb{\mu} + \sqrt{(3+\lambda)\pmb{\Sigma}}_{[i]} & i=1,2,3 \\ \pmb{\mu} - \sqrt{(3+\lambda)\pmb{\Sigma}}_{[i-3]} & i=4,5,6 \end{cases}$$

这些 Sigma 点可以通过**任意非线性投影函数精确投影**，然后从投影后的点集重新估计 2D 均值和协方差：

$$\pmb{v}_{\mu} = \sum_{i=0}^{6} w_i^{\mu} \pmb{v}_{x_i}, \quad \Sigma' = \sum_{i=0}^{6} w_i^{\Sigma} (\pmb{v}_{x_i} - \pmb{v}_{\mu})(\pmb{v}_{x_i} - \pmb{v}_{\mu})^{\mathrm{T}}$$

这一替换带来了三个因果性收益：
- **免导数**：无需为不同相机模型推导雅可比，UT 超参数 $\alpha=1.0, \beta=2.0, \kappa=0.0$ 在所有实验中保持固定；
- **滚动快门原生支持**：每个 Sigma 点可分配不同的外参矩阵，自然建模传感器在曝光期间的运动；
- **投影精度稳定**：在径向畸变和滚动快门条件下，UT 投影的 KL 散度中位数保持在约 $4.4\times10^{-3}$，而 EWA 的误差随畸变/运动显著增大（Figure 14, Appendix C）。

### 2. 渲染表达对齐：从 2D 评估到 3D 最大响应点

第二个关键 changed slot 是将粒子响应评估从 2D 图像平面迁移到 3D 空间。3DGS 在投影后的 2D 锥形上评估高斯响应，这要求梯度反向传播通过（近似的）投影函数，进一步加剧了非线性相机下的误差累积。

3DGUT 沿给定射线直接在 3D 空间中寻找粒子响应最大的点进行评估：

$$\tau_{\mathrm{max}} = \frac{(\pmb{\mu} - \pmb{o})^{T} \pmb{\Sigma}^{-1} \pmb{d}}{\pmb{d}^{T} \pmb{\Sigma}^{-1} \pmb{d}}$$

这一设计使渲染表达与体积粒子光线追踪方法 **3DGRT** (Moenne-Loccoz et al., SIGGRAPH Asia 2024) 完全对齐，无需投影函数的梯度传播。其直接后果是：**同一组 3D 高斯粒子可同时被光栅化和光线追踪渲染**——主光线使用光栅化保持高帧率，次级光线（反射、折射）使用 3DGRT 追踪（Figure 9）。

### 3. 深度排序：MLAB 近似逐射线排序

传统 3DGS 基于图像块的全局排序无法保证逐射线的正确深度顺序，这在混合渲染中会导致光栅化结果与追踪结果不一致。3DGUT 引入**多层级 alpha 融合 (MLAB)** 近似逐射线排序：每条射线存储 $k$ 个最近命中粒子，对剩余粒子进行增量混合。这一设计使得用光栅化训练的场景在用 3DGRT 渲染时保持高度一致（Figure 8），为混合渲染管线奠定基础。

### 4. 创新点的协同效应

上述三个 changed slots 并非孤立改进，而是形成因果闭环：
- UT 投影消除了对相机模型的依赖，使方法**通用**；
- 3D 响应评估使渲染表达与追踪方法**对齐**；
- MLAB 排序保证了光栅化与追踪的**一致性**；
- 三者共同使混合渲染成为可能，解锁了反射、折射等次级光线效果，同时保持主光线渲染的实时性能（265 FPS on MipNeRF360, Table 1）。

在鱼眼相机数据集 Scannet++ 上，这一协同效应的直接体现是：3DGUT 以仅 38% 的高斯粒子数量（0.38M vs 1.07M）显著超越专门为等距鱼眼模型推导雅可比的 **FisheyeGS** (Liao et al., arXiv 2024)，PSNR 达到 29.11 vs 28.15（Table 3）。

## 整体框架

3DGUT 在保留 3DGS 高帧率光栅化管线的前提下，通过三个核心改造将渲染表达从“近似投影函数”迁移到“近似粒子分布”，从而统一支持任意非线性相机模型、滚动快门效应以及次级光线效果。整体管线由四个关键模块串联构成，输入为经过 SFM 标定的多视角图像与对应相机参数，输出为任意目标视点的渲染图像。

### 管线总览

**模块一：Sigma 点生成与投影（ESTIMATE2DGAUSSIAN）**  
对于场景中的每一个 3D 高斯粒子，不再使用 EWA splatting 的一阶泰勒展开来线性化投影函数，而是采用 Unscented Transform 生成 7 个 Sigma 点来近似该粒子的 3D 分布。每个 Sigma 点通过任意非线性投影函数（包括鱼眼畸变模型或滚动快门对应的时变外参矩阵）进行精确投影，随后从投影点集加权重建 2D 高斯锥形（均值与协方差矩阵），作为光栅化的加速结构。该模块完全消除了对雅可比矩阵的依赖，使得同一套代码无需修改即可适配针孔、鱼眼、径向畸变以及滚动快门等多种相机模型。

**模块二：3D 粒子响应评估**  
传统 3DGS 在 2D 图像平面上利用投影后的 2D 锥形评估粒子对某一像素的贡献，这要求梯度反向传播穿越投影函数。3DGUT 将评估空间迁移到 3D：对于每条光线，计算粒子响应沿射线方向达到最大值的位置，并在该单一点处评估粒子的不透明度。这一设计使梯度传播完全绕开投影函数，同时与 3DGRT 的体积渲染表达在数学上对齐——两者的渲染方程均基于沿射线的粒子响应累积。

**模块三：MLAB 深度排序**  
标准 3DGS 采用基于图像块的全局排序来近似深度顺序，这在针孔相机下效果良好，但在复杂投影下排序误差增大。3DGUT 在需要精确排序的配置（Ours sorted）中引入多层级 alpha 融合近似，对每条射线存储 k 个最近命中粒子，并对更远的粒子进行增量混合，从而逼近正确的逐射线深度顺序。该机制使光栅化结果与光线追踪方法高度一致，为后续混合渲染奠定基础。

**模块四：混合光栅化/追踪渲染**  
由于模块二已使光栅化管线的渲染表达与 3DGRT 对齐，3DGUT 可在同一场景表示上实现混合渲染：主光线使用高效的光栅化管线，次级光线（反射、折射）则切换至 3DGRT 光线追踪管线。这一设计在保持主光线高帧率的同时，解锁了反射、折射等次级光线效果。

### 训练阶段的适配

训练过程中，稠密化策略的梯度来源也做了相应调整：原始 3DGS 使用 2D 屏幕空间梯度指导高斯粒子的分裂与克隆，3DGUT 则替换为 3D 位置梯度除以到相机距离的一半，以适配 3D 空间中的评估范式。损失函数沿用 L2 与 SSIM 的加权组合。

### 输入输出流

- **输入**：多视角 RGB 图像、对应的相机内参（支持非线性畸变模型）与外参（支持时变位姿以建模滚动快门）、SFM 稀疏点云。
- **处理**：以 SFM 点云初始化 3D 高斯粒子，通过 UT 投影→3D 响应评估→MLAB 排序→体积渲染的管线迭代优化粒子属性（位置、协方差、颜色、不透明度）。
- **输出**：优化后的 3D 高斯场景表示，可对任意相机模型（包括训练时未见过的畸变参数）和任意视点进行实时渲染，并可选择性地启用次级光线效果。

### 补充图表

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2412_12507/figures/011_Figure_8.jpg]]
*Figure 8: Scenes trained with different methods and rendered using 3DGRT [34]. Our method is the most consistent with the tracing approach, allowing for seamless hybrid rendering with splatting for primary and tracing for secondary rays*

## 核心模块与公式推导

### 4.1 无迹变换投影（ESTIMATE2DGAUSSIAN）

3DGUT的核心创新在于将3DGS中基于EWA splatting的线性化投影替换为**无迹变换（Unscented Transform, UT）**。原始3DGS通过一阶泰勒展开近似投影函数，需为每种相机模型推导雅可比矩阵 $J$，当面对鱼眼等强非线性投影时误差急剧增大。UT则采取相反策略：**近似粒子分布而非近似投影函数**。

具体而言，对每个3D高斯粒子（均值 $\pmb{\mu}$，协方差 $\pmb{\Sigma}$），生成7个精心选择的sigma点：

$$
\pmb{x}_i = \begin{cases} \pmb{\mu} & i=0 \\\\ \pmb{\mu} + \sqrt{(3+\lambda)\pmb{\Sigma}}_{[i]} & i=1,2,3 \\\\ \pmb{\mu} - \sqrt{(3+\lambda)\pmb{\Sigma}}_{[i-3]} & i=4,5,6 \end{cases}
$$

其中 $\lambda = \alpha^2(3+\kappa)-3$，$\alpha$、$\beta$、$\kappa$ 为UT超参数（所有实验中固定为 $\alpha=1.0$、$\beta=2.0$、$\kappa=0.0$）。这7个sigma点可被任意非线性投影函数 $\phi$ **精确投影**到2D图像平面，无需任何导数计算。随后从投影点重建2D高斯的均值和协方差：

$$ \pmb{v}_{\mu} = \sum_{i=0}^{6} w_i^{\mu} \pmb{v}_{x_i} $$

$$ \Sigma' = \sum_{i=0}^{6} w_i^{\Sigma} (\pmb{v}_{x_i} - \pmb{v}_{\mu})(\pmb{v}_{x_i} - \pmb{v}_{\mu})^{\mathrm{T}} $$

权重分别为：

$$ w_i^{\mu} = \begin{cases} \frac{\lambda}{3+\lambda} & i=0 \\\\ \frac{1}{2(3+\lambda)} & i=1,\dots,6 \end{cases} $$

$$ w_i^{\Sigma} = \begin{cases} \frac{\lambda}{3+\lambda} + (1-\alpha^2+\beta) & i=0 \\\\ \frac{1}{2(3+\lambda)} & i=1,\dots,6 \end{cases} $$

**关键优势**：UT完全消除了对投影函数雅可比矩阵的依赖，使方法天然支持任意非线性相机模型（鱼眼、全景等）。对于滚动快门这类时间依赖效应，每个sigma点可被赋予不同的外参矩阵独立变换，从而精确建模传感器运动。

### 4.2 3D空间粒子响应评估

原始3DGS在2D图像平面上评估投影后的锥形高斯响应，这要求梯度反向传播经过（近似的）投影函数。3DGUT改为**直接在3D空间中沿射线评估粒子响应**，与3DGRT的渲染表达对齐。

对给定射线 $\pmb{r}(\tau) = \pmb{o} + \tau \pmb{d}$，3D高斯粒子的响应函数为：

$$ \rho(\pmb{x}) = \exp\Bigl(-\frac{1}{2}(\pmb{x}-\pmb{\mu})^{T}\pmb{\Sigma}^{-1}(\pmb{x}-\pmb{\mu})\Bigr) $$

沿射线响应最大处对应的参数 $\tau_{\mathrm{max}}$ 具有闭式解：

$$ \tau_{\mathrm{max}} = \frac{(\pmb{\mu} - \pmb{o})^{T} \pmb{\Sigma}^{-1} \pmb{d}}{\pmb{d}^{T} \pmb{\Sigma}^{-1} \pmb{d}} = \frac{-\pmb{o}_{g}^{T} \pmb{d}_{g}}{\pmb{d}_{g}^{T} \pmb{d}_{g}} $$

其中 $\pmb{o}_g$、$\pmb{d}_g$ 为变换到规范高斯空间中的射线原点和方向。仅在该最大响应点处进行一次采样评估，避免了投影函数梯度传播，同时使光栅化结果与光线追踪方法高度一致。

### 4.3 多层级Alpha融合（MLAB）

为逼近正确的逐射线深度排序，3DGUT引入**多层级alpha融合近似（MLAB）**。具体策略为：对每条射线存储 $k$ 个最近命中粒子，对更远的命中粒子进行增量混合。这一机制仅在 **Ours (sorted)** 变体中启用，使光栅化的深度排序质量接近追踪方法，同时保持远高于纯追踪的渲染帧率。

### 4.4 体积渲染与训练

沿射线的体积渲染遵循标准方程：

$$ c(\pmb{o},\pmb{d}) = \sum_{i=1}^{N} c_i(\pmb{d}) \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j) $$

训练损失为L2损失与SSIM感知损失的加权组合：

$$ \mathcal{L} = \mathcal{L}_2 + 0.2 \mathcal{L}_{\mathrm{SSIM}} $$

稠密化阶段的梯度来源也做了适配：原始3DGS使用2D屏幕空间梯度，3DGUT遵循3DGRT的做法，替换为**3D位置梯度除以到相机距离的一半**，以适配3D空间中的粒子评估范式。

## 实验与分析

### 核心实验设置与对比基准

3DGUT在四个性质迥异的数据集上与多个代表性基线进行对比：**MipNeRF360**（针孔相机，全景场景）、**Tanks & Temples**（针孔相机，真实捕获）、**Scannet++**（等距鱼眼相机，大畸变）和**Waymo**（畸变相机+滚动快门，自动驾驶场景）。对比方法涵盖原始光栅化管线**3DGS**（Kerbl et al., ACM Trans. Graph. 2023）、引入排序的光栅化方法**StopThePop**（Radl et al., ACM Trans. Graph. 2024）、体积粒子光线追踪方法**3DGRT**（Moenne-Loccoz et al., ACM Trans. Graph. SIGGRAPH Asia 2024）、精确椭球体渲染方法**EVER**、专为鱼眼相机推导雅可比的**FisheyeGS**（Liao et al., arXiv 2024），以及神经辐射场方法**ZipNeRF**（Barron et al., ICCV 2023）。训练损失统一采用$\mathcal{L} = \mathcal{L}_2 + 0.2 \mathcal{L}_{\mathrm{SSIM}}$，UT超参数在所有实验中固定为$\alpha=1.0, \beta=2.0, \kappa=0.0$。

### 主结果：针孔相机场景保持竞争力，复杂相机场景显著领先

在MipNeRF360和Tanks & Temples等标准针孔相机数据集上，3DGUT收敛到与3DGS相当的质量水平，同时解锁了复杂相机和次级光线的支持。如表1所示，Ours (sorted)在MipNeRF360上达到PSNR 27.26、SSIM 0.812、LPIPS 0.215，渲染速度200 FPS；未排序版本Ours达到265 FPS，远超3DGRT的52 FPS，LPIPS从0.248降至0.218。在Tanks & Temples上，Ours (sorted)的LPIPS为0.172，优于3DGS的0.196，表明排序机制对视觉感知质量有稳定增益。

真正体现方法优势的是复杂相机场景。在Scannet++鱼眼数据集上，Ours (sorted)以PSNR 29.11显著超越专为该相机模型推导雅可比的FisheyeGS（PSNR 28.15），且仅使用约38%的高斯粒子（0.38M vs 1.07M）。作为对照，若将鱼眼图像去畸变后训练3DGS，会因像素丢失导致PSNR骤降至22.76。在Waymo数据集上，Ours (sorted)以PSNR 30.16优于3DGRT的29.99，而3DGS因无法直接处理畸变和滚动快门，不具备可比性。

### 渲染效率分解：UT计算开销可控

表2给出了MipNeRF360上的详细耗时分解。UT投影（ESTIMATE2DGAUSSIAN）引入的额外计算是可控的，整体光栅化管线仍保持高帧率。Ours (sorted)因MLAB排序增加了逐射线深度排序开销，FPS从265降至200，但换取了LPIPS的显著改善（0.218→0.215）。

### 消融研究：广义高斯核与投影精度

**粒子核函数的阶数消融**（表4、图10）揭示了质量与速度的权衡机制：高阶广义高斯粒子更“致密”，下降沿更陡峭，可在保持可接受质量的前提下提升渲染速度。阶数4相比阶数2提升26 FPS（233 vs 207），PSNR仅下降0.31。这一发现表明粒子形状是调节光栅化效率的有效控制旋钮，但需注意论文指出阶数4对应3DGRT中提出的阶数2广义高斯，命名上存在偏移。

**投影精度消融**（图14，附录C）是验证核心主张的关键证据。对无畸变针孔、鱼眼相机以及静态/滚动快门四种设置，分别计算每个高斯粒子用EWA投影和UT投影相对于蒙特卡洛参考投影的KL散度。UT方法在所有设置下保持稳定且低的中位数KL散度（约$4.4\times10^{-3}$），而EWA投影的KL散度随畸变参数增大或滚动快门横向平移量增加而显著恶化。这直接证实了“近似粒子分布而非近似投影函数”这一核心洞察的有效性。

### 混合渲染与次级光线效果

3DGUT通过将粒子响应评估从2D图像平面迁移到3D空间最大响应点，使渲染表达与3DGRT对齐。图8的交叉验证实验表明：用不同方法训练的场景，统一用3DGRT追踪渲染时，3DGUT训练结果与追踪方法的一致性最高，这为混合渲染奠定了基础。图9展示了主光线光栅化+次级光线追踪的混合效果，成功模拟了折射和反射现象——这是原始3DGS完全无法实现的能力。

### 失败模式与适用边界

尽管3DGUT在多数场景表现优异，分析揭示了若干需要注意的边界条件：

1. **极大畸变下的近似退化**：当镜头畸变极大（如超广角鱼眼）时，投影后的集合分布可能严重偏离2D椭球形，UT的7个sigma点近似精度会下降。这是固定sigma点数量的固有局限。
2. **单采样评估的近似误差**：方法仅在射线最大响应处进行一次采样评估高斯响应，当多个高斯沿射线重叠时可能产生近似误差。论文未提供多采样策略的对比数据。
3. **混合渲染的效率瓶颈**：次级光线追踪开销仍然显著，整体效率低于纯光栅化。如何动态决定主光线的渲染方式以实现最优效率，仍是开放问题。
4. **UT超参数未自适应**：$\alpha, \beta, \kappa$在所有实验中固定，未根据相机模型或场景调节，可能在特定设置下未达最优。
5. **训练梯度近似**：使用3D位置梯度除以到相机距离的一半替代2D屏幕空间梯度进行稠密化，在某些细节区域可能存在微小质量损失。
6. **未验证的场景**：动态物体、非刚性变形、多曝光相机设置的有效性尚未验证。

### 公平性说明

与FisheyeGS的比较中，后者专门为等距鱼眼模型推导了雅可比，而3DGUT无需任何针对性推导即全面超越，体现了通用方法的优势。在Scannet++上与3DGS的间接比较中，3DGS通过去畸变图像训练再渲染，存在像素丢失，天然处于不利地位。与3DGRT/EVER的比较使用相同的训练迭代数和类似的高斯数量，UT超参数未做场景特化调整。在针孔相机数据集上，3DGUT因UT计算额外消耗，FPS略低于3DGS，这是换取复杂相机和次级光线支持的合理代价。

### 补充图表

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2412_12507/figures/017_Figure_12.jpg]]
*Figure 12: KL divergence to Monte Carlo for equidistant fisheye cameras*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2412_12507/figures/018_Figure_13.jpg]]
*Figure 13: KL divergence to Monte Carlo under radial distortion and rolling shutter*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2412_12507/figures/019_Figure_14.jpg]]
*Figure 14: Gaussian Projection Quality: for both distortion-free pinhole and fisheye camera models, as well as static and rolling-shutter (RS, top-top-bottom shutter direction) poses, we evaluate the Kullback–Leibler (KL ↓) divergence of each Gaussian projected using either EWA (•) or UT-based (•) projections against Monte-Carlo-based reference projection. The distribution of KL-divergences for each rendering is shown in the histograms below*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2412_12507/figures/005_Table_1.jpg]]
*Table 1: Quantitative results of our approach and baselines on the MipNERF360 [1] and Tanks & Temples [21] datasets*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2412_12507/figures/006_Table_2.jpg]]
*Table 2: Detailed timings on the MipNeRF360 [1] dataset*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2412_12507/figures/010_Table_3.jpg]]
*Table 3: When evaluated on a dataset acquired with equidistant fisheye cameras, our general method outperforms [25] which derived the linerization for this specific camera model. Undistortion removes large parts of the original images and results in underobserved regions [18]. Results marked with † are taken from [25]*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2412_12507/figures/013_Table_4.jpg]]
*Table 4: Quality and speed tradeoffs computed on MipN-ERF360 [1] (excluding flower and treehill for fair comparison with 3DGRT) for various particle generalized Gaussian kernel functions. Note that our kernel of degree= 4 corresponds to the generalized Gaussian of degree= 2 proposed in 3DGRT [34]*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2412_12507/figures/016_Table_5.jpg]]
*Table 5: On the Waymo [46] autonomous vehicles dataset that was captured with distorted camera model and rolling-shuter sensor, our method achieves better quality compared to 3DGRT [34]. Note that 3DGS [18] requires the training and evaluation to be done on rectified images without rolling shutter effects and is hence not directly comparable*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2412_12507/figures/022_Table_6.jpg]]
*Table 6: Detailed evaluation results of our methods on the Tanks & Temples [21] dataset*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2412_12507/figures/023_Table_7.jpg]]
*Table 7: Per-scene evaluation results of our methods on the MipNeRF360 [1] dataset*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2412_12507/figures/024_Table_8.jpg]]
*Table 8: Per-scene evaluation results of our methods on the Scannet++ dataset*

## 方法谱系与知识库定位

### 1. 与基线方法的谱系关系

**3DGUT** 处于高斯泼溅（Gaussian Splatting）与体积粒子光线追踪（Volumetric Particle Ray Tracing）的交叉地带，其核心贡献在于用 **Unscented Transform（UT）** 统一了光栅化和光线追踪的渲染表达，从而突破了原始 3DGS 对线性相机模型和主光线的限制。

#### 1.1 对 3DGS 的继承与改造

**3DGS**（Kerbl et al., *ACM Trans. Graph.* 2023）奠定了 3D 高斯粒子作为场景表示的基础范式。3DGUT 完整继承了这一表示——包括 3D 高斯粒子的均值 $\pmb{\mu}$、协方差矩阵 $\pmb{\Sigma} = \pmb{R}\pmb{S}\pmb{S}^T\pmb{R}^T$ 的分解形式、球谐系数建模视角依赖外观、以及基于梯度的稠密化策略。然而，3DGUT 在三个关键模块上做出了根本性替换：

| 模块 | 3DGS 基线 | 3DGUT 替换 | 替换原因 |
|------|-----------|------------|----------|
| 粒子投影 | EWA splatting 通过一阶泰勒展开线性化投影函数（需雅可比矩阵 $\pmb{J}$） | Unscented Transform 使用 7 个 sigma 点进行精确投影，再从投影点重建 2D 高斯 | 消除对雅可比的依赖，支持任意非线性相机模型 |
| 响应评估 | 在 2D 图像平面利用投影的 2D 锥形评估粒子响应 | 在 3D 空间中沿射线的最大响应点 $\tau_{\max}$ 评估粒子响应 | 避免梯度流过投影函数，与光线追踪渲染表达对齐 |
| 深度排序 | 基于图像块的全局排序 | 多层级 alpha 融合（MLAB）近似逐射线的深度排序（仅在 Ours (sorted) 中启用） | 逼近正确的深度顺序，使光栅化结果与追踪方法一致 |

这三个替换的因果链条是：**UT 投影消除了雅可比依赖**，使得任意非线性相机模型（鱼眼、径向畸变）和滚动快门（每个 sigma 点可独立赋予不同外参矩阵）成为可能；**3D 响应评估**则使渲染表达与 **3DGRT**（Moenne-Loccoz et al., *ACM Trans. Graph.* SIGGRAPH Asia 2024）对齐，为混合光栅化/追踪渲染铺平道路。

#### 1.2 与 FisheyeGS 的对比

**FisheyeGS**（Liao et al., *arXiv* 2024）是专门针对等距鱼眼相机模型扩展的 3DGS 变体，其思路是为该特定相机模型推导专用的 EWA 投影雅可比矩阵。这一定制化策略的局限性在于：每遇到一种新的非线性相机模型，都需要重新推导雅可比，且推导过程复杂、容易出错。

3DGUT 采用了截然不同的哲学：**不是近似投影函数，而是近似粒子分布本身**。通过 UT 的 sigma 点机制，投影函数 $\pi(\cdot)$ 可以是任意黑盒非线性函数，sigma 点 $\pmb{x}_i$ 被精确投影为 $\pmb{v}_{x_i} = \pi(\pmb{x}_i)$，然后从这些投影点重建 2D 均值和协方差：

$$\pmb{v}_{\mu} = \sum_{i=0}^{6} w_i^{\mu} \pmb{v}_{x_i}, \quad \Sigma' = \sum_{i=0}^{6} w_i^{\Sigma} (\pmb{v}_{x_i} - \pmb{v}_{\mu})(\pmb{v}_{x_i} - \pmb{v}_{\mu})^{\mathrm{T}}$$

在 Scannet++ 鱼眼数据集上，这一通用方法在所有感知指标上**显著优于**专门为该相机模型定制雅可比的 FisheyeGS（PSNR 29.11 vs 28.15），且仅使用 38% 的高斯粒子（0.38M vs 1.07M）。这一结果强有力地证明了“近似粒子分布”策略相对于“近似投影函数”策略的优越性。

#### 1.3 与 3DGRT 的对齐与分化

**3DGRT**（Moenne-Loccoz et al., *ACM Trans. Graph.* SIGGRAPH Asia 2024）首次将 3D 高斯粒子表示为体积粒子，并通过光线追踪进行渲染，天然支持次级光线（反射、折射）和滚动快门。3DGUT 在渲染表达上与 3DGRT 对齐——两者都在 3D 空间中沿射线评估粒子响应，使用相同的体积渲染方程：

$$c(\pmb{o},\pmb{d}) = \sum_{i=1}^{N} c_i(\pmb{d}) \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j)$$

然而，3DGUT 在**主光线**上使用光栅化而非追踪，这使得其在 MipNeRF360 上达到 **265 FPS**，而 3DGRT 仅为 52 FPS（约 5 倍加速），同时保持可比的图像质量（PSNR 27.26 vs 27.40，LPIPS 0.218 vs 0.248）。这种“主光线光栅化 + 次级光线追踪”的混合策略，使得 3DGUT 在保持高帧率的同时解锁了反射、折射等次级光线效果。

#### 1.4 与其他相关方法的定位

- **StopThePop**（Radl et al., *ACM Trans. Graph.* 2024）：引入了排序的光栅化高斯泼溅，3DGUT 的 MLAB 排序模块借鉴了其思想，但并非直接继承。
- **EVER**：精确椭球体渲染光线追踪方法，与 3DGRT 同为纯追踪路线，3DGUT 在次级光线上与其可比，但在主光线上以光栅化获得显著速度优势。
- **ZipNeRF**（Barron et al., *ICCV* 2023）：神经辐射场方法，代表另一条技术路线（基于网格的 NeRF），3DGUT 在渲染速度上具有数量级优势（265 FPS vs 典型 NeRF 方法的 <1 FPS）。

### 2. 适用边界

3DGUT 的适用边界由其核心设计选择决定：

**支持的能力：**
- 任意非线性相机模型（鱼眼、径向畸变、自定义镜头），无需针对每种模型推导雅可比
- 时间依赖的相机效应（滚动快门），通过为每个 sigma 点赋予独立的外参矩阵实现
- 次级光线效果（反射、折射），通过与 3DGRT 的混合渲染实现
- 标准针孔相机场景，收敛到与 3DGS 相当的质量（PSNR 27.26 vs 27.47 on MipNeRF360）

**边界与限制：**
- 当镜头畸变极大（如超广角鱼眼）时，投影后的 sigma 点集合分布可能严重偏离 2D 椭球形，UT 近似的精度会下降
- 仅在射线最大响应处进行一次采样评估高斯响应（$\tau_{\max}$），当多个高斯沿射线重叠时可能产生近似误差
- 混合渲染需要同时维护光栅化管线和光线追踪管线，次级光线追踪开销仍然显著，整体效率低于纯光栅化
- UT 的超参数 $\alpha, \beta, \kappa$ 在所有实验中固定为 $\alpha=1.0, \beta=2.0, \kappa=0.0$，未根据具体相机模型或场景进行自适应调节
- 尚未验证对动态物体、非刚性变形或多曝光相机设置的有效性

### 3. 局限与开放问题

#### 3.1 已识别的局限

1. **大畸变下的近似精度衰减**：当投影函数非线性极强时，7 个 sigma 点可能不足以充分捕获投影后的分布形状。图 14 的 KL 散度分析表明，UT 方法在径向畸变和滚动快门下保持低且一致的 KL 散度（中位数 $\approx 4.4 \times 10^{-3}$），但极端情况下仍存在尾部误差。

2. **单采样点评估的近似误差**：在 3D 空间中仅沿射线最大响应点 $\tau_{\max}$ 进行一次采样，当多个高斯粒子沿同一射线显著重叠时，可能产生累积近似误差。这一设计是为了计算效率的折中。

3. **混合渲染的工程复杂度**：同时维护光栅化和追踪两条管线增加了系统复杂度，且次级光线的追踪开销仍然显著。

4. **训练梯度的近似**：使用 3D 位置梯度除以到相机距离的一半来替代 2D 屏幕空间梯度，可能在某些细节区域引入微小的质量损失。

5. **UT 超参数未自适应**：$\alpha, \beta, \kappa$ 在所有实验中固定，未根据相机模型或场景内容进行调节，可能未达到最优投影近似。

#### 3.2 开放问题

1. **Sigma 点数量的自适应策略**：能否通过增加 sigma 点数量或采用自适应采样策略（如在投影分布偏离椭球形时动态增加采样点），进一步提高大畸变下的投影近似精度？

2. **更精确的重叠高斯评估**：是否可以设计更精确的多高斯重叠评估方法（如多次采样或局部体积积分），同时不显著增加计算开销？

3. **混合渲染的动态调度**：如何根据场景内容（如次级光线贡献的区域大小、材质属性）动态决定主光线采用光栅化或追踪，以实现最优效率？

4. **UT 方法的推广性**：UT 方法能否直接推广到其他需要非线性投影的高斯泼溅变体，如 Mip-Splatting、2D Gaussian Splatting？

5. **更复杂的传感器模型**：是否可以将 UT 思想用于更复杂的传感器模型，例如事件相机、ToF 相机或自定义镜头系统？

6. **梯度稳定性优化**：UT 损失函数的梯度是否可进一步优化，以避免在极端相机参数下的潜在数值不稳定？

### 4. 知识库定位总结

3DGUT 的核心知识贡献在于提出了一个**统一的投影-渲染框架**，其关键洞察是：**通过 UT 近似粒子分布而非近似投影函数**。这一框架将 3DGS 的适用边界从“针孔相机 + 主光线”扩展到“任意非线性相机 + 次级光线”，同时保持了光栅化的高帧率优势。在知识谱系中，3DGUT 是 3DGS 和 3DGRT 之间的桥梁——它继承了前者的光栅化效率，对齐了后者的渲染表达，从而实现了两者的优势互补。

## 原文 PDF

![[paperPDFs/CVPR_2025/3DGUT_Enabling_Distorted_Cameras_and_Secondary_Rays_in_Gaussian_Splatting.pdf]]
