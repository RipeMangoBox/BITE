---
title: 3D Gaussian Splatting for Real-time Radiance Field Rendering
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/3D_Gaussian_Splatting_for_Real_time_Radiance_Field_Rendering.pdf
project_link: "http://fungraph.inria.fr"
code_link: "https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/"
aliases:
- 3GS
- 3GSRTRFR
tags:
- SIGGRAPH_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 用显式3D高斯表示代替隐式MLP或体素网格，通过基于tile的快速各向异性泼溅光栅化和自适应密度控制，同时实现高质量和实时渲染。
primary_logic: 3D高斯是一种可微体积表示，既能像点云一样快速投影和混合，又能像NeRF一样优化连续辐射场；通过参数化各向异性协方差和球谐函数，可以紧凑地表示复杂几何和视角相关外观；基于tile的GPU排序和光栅化使得训练与渲染极高效。
claims:
- 使用3D高斯表示，从SfM稀疏点云初始化，实现可微的连续体积表示。
- 通过优化各向异性协方差、不透明度、球谐系数，并结合自适应密度控制，生成高质量紧凑表示。
- 基于tile的可微光栅化渲染器实现各向异性泼溅和可见性排序，达到实时渲染。
- 训练35-45分钟即可达到或超过Mip-NeRF360训练48小时的质量，同时渲染帧率超过30fps。
---

# 3D Gaussian Splatting for Real-time Radiance Field Rendering

> [!tip] 核心洞察
> 3D高斯是一种可微体积表示，既能像点云一样快速投影和混合，又能像NeRF一样优化连续辐射场；通过参数化各向异性协方差和球谐函数，可以紧凑地表示复杂几何和视角相关外观；基于tile的GPU排序和光栅化使得训练与渲染极高效。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向实时辐射场渲染的3D高斯泼溅 |
| 英文题名 | 3D Gaussian Splatting for Real-time Radiance Field Rendering |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/) · [Project](http://fungraph.inria.fr) · [Code](https://gitlab.inria.fr/sibr/sibr_core) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 3D Gaussian Splatting |
| Dataset | Mip-NeRF360 |

> [!tip] 效果简介
> - Mip-NeRF360 (average) 上，LPIPS 0.214 (Ours-30k) vs 0.240 (Mip-NeRF360) (-0.026)。
> - Mip-NeRF360 上，Training time ~41 min (Ours-30k) vs ~48 hours (Mip-NeRF360) (~70x speedup)；Rendering FPS (1080p) 160 (Ours-7k) vs not real-time (>30 fps (real-time))。

## 概要

现有神经辐射场（NeRF）方法依赖昂贵的体积光线行进与随机采样，无法在保持高视觉质量的同时实现实时渲染。本文提出 **3D Gaussian Splatting**，以显式三维高斯基元替代隐式 MLP 或体素网格作为场景表示，从根本上改变了渲染与优化的效率瓶颈。

核心思路是：从运动恢复结构（SfM）稀疏点云初始化一组各向异性三维高斯，每个高斯携带位置、协方差矩阵、不透明度以及球谐系数以表达视角相关外观；通过可微的基于 tile 的排序光栅化器进行快速投影与 alpha 混合，实现高帧率新视角合成；训练过程中交替执行参数优化与自适应密度控制（克隆/分裂），使高斯集合紧凑覆盖场景几何。

主要结果：在 Mip-NeRF360、Tanks&Temples、Deep Blending 三个数据集上，本方法以约 35–45 分钟的训练时间，达到或超越 Mip-NeRF360 训练约 48 小时的质量（LPIPS 0.214 vs. 0.240），同时首次实现 1080p 分辨率下超过 30 fps 的实时渲染（最高 160 fps）。方法定位上，本工作将点渲染的效率与 NeRF 的可微连续辐射场优化相融合，在场景表示、渲染方式和优化策略三个关键槽位上对先前工作进行了根本性替换。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

现有神经辐射场（NeRF）方法面临一个根本性矛盾：基于MLP的隐式表示（如Mip-NeRF360）虽能达到高质量，但依赖昂贵的体积光线行进和沿射线随机采样，无法实时渲染高分辨率图像；而基于显式网格的快速方法（如InstantNGP、Plenoxels）虽加速了训练，却在视觉质量上有所妥协。**核心瓶颈在于：隐式表示与体积光线行进的耦合导致了不可逾越的计算开销。**

本文的核心洞察是：**3D高斯是一种可微的体积表示基元**——它既能像点云一样在GPU上快速投影和混合，又能像NeRF一样通过梯度下降优化连续辐射场。通过参数化各向异性协方差矩阵和球谐函数（SH），一组显式的3D高斯可以紧凑地表示复杂几何和视角相关外观；而基于tile的GPU排序与光栅化管线，则使得训练与渲染同时获得数量级的加速。

### 三个关键Changed Slots

与基线方法相比，3D Gaussian Splatting在三个核心维度上做出了根本性改变：

| 维度 | 基线方法（Mip-NeRF360/InstantNGP） | 本文方法 |
|------|-----------------------------------|----------|
| **场景表示** | 隐式MLP或离散网格（体素/哈希） | 显式3D高斯（位置、各向异性协方差、不透明度、SH系数） |
| **渲染方式** | 基于光线行进的体积渲染（随机采样） | 基于tile的排序光栅化（各向异性泼溅、alpha混合） |
| **优化策略** | 直接梯度下降，无密度控制 | 自适应密度控制（克隆/分裂）+周期性不透明度重置 |

这三个改变相互耦合、互为因果：显式高斯表示使得快速光栅化成为可能；快速光栅化又使得优化过程中可以高效计算梯度；而自适应密度控制则补偿了显式表示的离散性，在训练中动态调整基元分布以逼近连续辐射场。

### 方法框架与模块顺序

整体流程（Fig. 2）包含四个顺序模块，形成训练-渲染的闭环：

![[assets/figures/papers/paper_list_l3_https_repo_sam_inria_fr_fungraph_3d_gaussian_splatting/figures/002_Figure_2.jpg]]
*Figure 2: Optimization starts with the sparse SfM point cloud and creates a set of 3D Gaussians. We then optimize and adaptively control the density of this set of Gaussians. During optimization we use our fast tile-based renderer, allowing competitive training times compared to SOTA fast radiance field methods. Once trained, our renderer allows real-time navigation for a wide variety of scenes*

**模块1：稀疏点云初始化（SfM）**
输入为Structure-from-Motion（SfM）标定的相机参数和稀疏3D点云。从这些点创建初始3D高斯集合，每个高斯由位置（均值 $\mu$）、协方差矩阵 $\Sigma$ 和不透明度 $\alpha$ 定义。初始协方差设为各向同性，其尺度由最近邻点距离估计。这一初始化策略利用了SfM的“免费”先验，为后续优化提供了合理的几何起点。

**模块2：3D高斯参数优化**
使用随机梯度下降（Adam优化器）联合优化所有高斯参数，包括：3D位置、各向异性协方差（分解为缩放向量 $s$ 和四元数 $q$ 表示旋转）、不透明度 $\alpha$（经sigmoid激活），以及球谐系数（编码视角相关颜色）。损失函数结合L1损失和结构相似度损失D-SSIM：

$$\mathcal{L} = (1 - \lambda) \mathcal{L}_{1} + \lambda \mathcal{L}_{\mathrm{D-SSIM}}$$

其中 $\lambda = 0.2$。可微渲染器（模块4）计算损失对每个高斯参数的梯度，反向传播更新所有参数。整个优化过程完全在GPU上以CUDA kernel执行。

**模块3：自适应密度控制**
在优化过程中周期性执行密度调整，基于视图空间位置梯度的平均幅值。当梯度超过阈值 $\tau_{\text{pos}}$ 时触发：
- **欠重建区域**（小尺度几何覆盖不足）：**克隆**该高斯，沿梯度方向复制一份；
- **过重建区域**（一个大高斯覆盖了小尺度几何）：**分裂**该高斯为两个，缩放因子除以1.6。

同时，周期性将所有高斯的 $\alpha$ 重置为接近零的值，以消除优化过程中产生的“漂浮物”伪影；并删除 $\alpha$ 低于阈值或世界空间过大的高斯。这一策略使高斯集合的分布自适应地匹配场景几何复杂度（Fig. 4）。

![[assets/figures/papers/paper_list_l3_https_repo_sam_inria_fr_fungraph_3d_gaussian_splatting/figures/004_Figure_4.jpg]]
*Figure 4: Our adaptive Gaussian densification scheme. Top row (underreconstruction): When small-scale geometry (black outline) is insufficiently covered, we clone the respective Gaussian. Bottom row (over-reconstruction): If small-scale geometry is represented by one large splat, we split it in two*

**模块4：2D投影与tile-based光栅化**
这是实现实时渲染和高效训练的核心引擎。流程如下：
1. **投影**：将每个3D高斯的均值投影到屏幕空间，通过仿射近似的Jacobian矩阵 $J$ 和观察变换 $W$ 计算2D协方差矩阵：
   $$\Sigma' = J W \Sigma W^T J^T$$
2. **tile分块**：将屏幕划分为16×16像素的tile，每个高斯根据其2D协方差覆盖的tile范围进行分配，剔除视锥体和tile外的所有高斯。
3. **排序**：对每个tile内的高斯按深度使用GPU基数排序（Radix Sort），建立从前到后的顺序。
4. **前向混合**：按排序顺序累积颜色和 $\alpha$ 值，执行alpha混合：
   $$C = \sum_{i \in N} c_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j)$$
   当累积 $\alpha$ 达到饱和时提前终止。
5. **反向传播**：复用排序结果，按相反顺序传播梯度到每个参与混合的高斯，支持任意数量的混合高斯接收梯度。

### 关键公式与变量含义

**3D高斯函数**（Eq. 4）：
$$G(x) = e^{-\frac{1}{2}(x)^T \Sigma^{-1} (x)}$$
其中 $\Sigma$ 是3D协方差矩阵，控制高斯在空间中的形状和方向。

**协方差参数化**（Eq. 6）：
$$\Sigma = R S S^T R^T$$
将 $\Sigma$ 分解为缩放矩阵 $S$（对角矩阵，3个参数）和旋转矩阵 $R$（用四元数表示，4个参数），保证协方差矩阵在优化过程中始终半正定。

**投影协方差**（Eq. 5）：
$$\Sigma' = J W \Sigma W^T J^T$$
其中 $W$ 是世界到相机的观察变换，$J$ 是投影变换的仿射近似的Jacobian矩阵。这一公式将3D高斯映射为屏幕空间的2D高斯，是泼溅渲染的数学基础。

**体积渲染与点混合的等价性**（Eq. 2, Eq. 3）：
传统体积渲染 $C = \sum T_i \alpha_i \mathbf{c}_i$（其中 $\alpha_i = 1 - \exp(-\sigma_i \delta_i)$）与有序点alpha混合 $C = \sum c_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j)$ 在数学形式上等价。这一等价性保证了基于高斯的泼溅渲染可以保留体积渲染的连续性和可微性，同时避免了沿射线的密集采样。

### 模块间的因果链路

整个系统的性能优势源于模块间的正向因果链：

1. **显式高斯表示 → 快速投影与光栅化**：3D高斯作为显式基元，投影到屏幕空间仅需一次矩阵乘法，无需沿射线采样；tile-based光栅化将计算限制在局部区域，实现高度并行。

2. **快速光栅化 → 高效梯度计算**：反向传播复用前向的排序结果，梯度仅传播到实际参与混合的高斯，避免了对整个场景的全局计算。消融实验证实，若限制接收梯度的高斯数量（Limited-BW），PSNR下降约11dB（Table 3, Fig. 9），说明充分的梯度传播对质量至关重要。

3. **自适应密度控制 → 紧凑表示与质量提升**：克隆和分裂策略使高斯分布自适应匹配场景几何，避免欠重建导致的空洞和过重建导致的模糊。消融表明，SfM初始化（vs 随机点云）减少背景噪点（Fig. 7），拆分大高斯（vs 不拆分）改善背景重建（Fig. 8）。

![[assets/figures/papers/paper_list_l3_https_repo_sam_inria_fr_fungraph_3d_gaussian_splatting/figures/010_Figure_7.jpg]]
*Figure 7: Initialization with SfM points helps. Above: initialization with a random point cloud. Below: initialization using SfM points*

4. **各向异性协方差 + SH → 表达能力**：各向异性高斯能紧凑表示细长结构（如树枝、边缘），相比各向同性高斯显著提升PSNR（Table 3, Fig. 10）；球谐系数编码视角相关颜色，去除SH同样导致PSNR下降（Table 3）。

### 训练与推理路径

**训练路径**：从SfM稀疏点云初始化 → 前向光栅化渲染图像 → 计算L1+D-SSIM损失 → 反向传播梯度更新高斯参数（位置、协方差、不透明度、SH系数）→ 周期性触发密度控制（克隆/分裂/删除/不透明度重置）。完整训练约35-45分钟（30K迭代），即可达到或超过Mip-NeRF360训练48小时的质量。

**推理路径**：加载优化后的高斯集合 → 对每个新视角执行tile-based光栅化（投影→分tile→排序→混合），无需任何网络推理或采样。在1080p分辨率下渲染帧率超过30fps（Ours-7K达160fps），首次实现高质量辐射场的实时渲染。

## 实验与关键发现

**实验设置。** 3D Gaussian Splatting 在三个公开数据集上进行评估：Mip-NeRF360（9个场景，包含室外无界和室内场景）、Tanks&Temples（2个场景）和Deep Blending（2个场景）。所有方法在1080p分辨率下比较，指标为PSNR、SSIM和LPIPS。训练和渲染在单块NVIDIA RTX A6000 GPU上进行。对比基线包括质量最优的**Mip-NeRF360**（Barron et al., 2022）、快速训练的**InstantNGP**（Müller et al., 2022）和**Plenoxels**（Fridovich-Keil and Yu et al., 2022）。其中带†标记的结果直接取自原论文，其余为本文在统一条件下的复现。

**主结果：质量-速度-训练时间的三角突破。** 3D Gaussian Splatting 在三个维度上同时取得突破性表现（Table 1）：

- **渲染速度：** 在Mip-NeRF360数据集上，Ours-7K版本达到**160 FPS**（1080p），Ours-30K版本达到**82 FPS**，首次实现高质量辐射场的实时渲染（>30 fps）。相比之下，Mip-NeRF360等隐式方法无法实时渲染。
- **训练效率：** Ours-7K仅需约**7分钟**训练即可获得有竞争力的质量；Ours-30K约需**35-45分钟**，相比Mip-NeRF360的**48小时**实现了约**70倍加速**，同时与InstantNGP的训练时间（约5-10分钟）在同一量级。
- **渲染质量：** Ours-30K在Mip-NeRF360数据集上取得**LPIPS 0.214**，优于Mip-NeRF360的0.240（降低0.026），在感知质量上达到甚至超越此前最优方法。PSNR和SSIM也达到与Mip-NeRF360相当或更好的水平。

**关键数值对比（Mip-NeRF360平均）：**

| 方法 | PSNR↑ | SSIM↑ | LPIPS↓ | 训练时间 | FPS |
|------|-------|-------|--------|----------|-----|
| Mip-NeRF360 | 29.23 | 0.844 | 0.240 | ~48h | 非实时 |
| InstantNGP | 25.43 | 0.671 | 0.371 | ~5-10min | ~3-5 |
| Plenoxels | 23.08 | 0.626 | 0.463 | ~11min | ~2-3 |
| Ours-7K | 27.47 | 0.813 | 0.248 | ~7min | **160** |
| Ours-30K | **29.41** | **0.847** | **0.214** | ~41min | 82 |

**与快速训练方法的比较。** Ours-7K在约7分钟训练后，PSNR（27.47）显著高于InstantNGP（25.43，+2.04dB）和Plenoxels（23.08，+4.39dB），LPIPS（0.248）也远优于两者（0.371和0.463）。这表明即使在训练时间预算极有限的情况下，3D高斯表示仍能提供远优于其他快速方法的视觉质量。

**与质量最优方法的比较。** Ours-30K在PSNR（29.41 vs 29.23）、SSIM（0.847 vs 0.844）和LPIPS（0.214 vs 0.240）三个指标上全面超越Mip-NeRF360，同时训练速度快约70倍，且首次实现实时渲染。Figure 5的定性对比显示，本文方法在细节重建（如Bicycle场景的车轮辐条、Counter场景的纹理）上表现更清晰，伪影更少。

**Synthetic NeRF数据集结果（Table 2）。** 在无SfM点云可用的合成场景中，使用100K随机初始化点，本文方法取得PSNR 33.32，与Mip-NeRF（33.09）相当，优于InstantNGP（25.43）。这验证了即使没有SfM先验，3D高斯优化仍能收敛到高质量表示。

**关键消融实验（Table 3，Figures 7-10）。** 消融实验在Mip-NeRF360场景上进行，使用高分辨率输入下采样到标准渲染分辨率以减少JPEG压缩等随机伪影，确保消融结果反映方法本身的因果效应。

1. **各向异性协方差 vs 各向同性（Table 3, Fig. 10）：** 禁用各向异性后PSNR显著下降。各向异性高斯能沿表面方向拉伸、沿法线方向压缩，从而用更少的基元紧凑表示薄结构和复杂几何。Figure 10中Ficus场景限制为最多5000个高斯时，各向异性版本能清晰重建细枝，各向同性版本则丢失细节。

![[assets/figures/papers/paper_list_l3_https_repo_sam_inria_fr_fungraph_3d_gaussian_splatting/figures/009_Table_3.jpg]]
*Table 3: PSNR Score for ablation runs. For this experiment, we manually downsampled high-resolution versions of each scene’s input images to the established rendering resolution of our other experiments. Doing so reduces random artifacts (e.g., due to JPEG compression in the pre-downscaled Mip-NeRF360 inputs)*

2. **球谐函数（SH）vs 无SH（Table 3）：** 移除SH系数后PSNR下降，验证了SH对建模视角相关外观（如镜面高光、反射）的必要性。SH以紧凑的频域表示替代显式存储多视角颜色，是质量-存储效率的关键权衡。

3. **SfM初始化 vs 随机点云（Fig. 7）：** SfM初始化显著减少背景噪点和漂浮物。随机初始化导致优化初期缺乏几何先验，高斯容易在空白区域生长形成伪影。SfM稀疏点云提供了可靠的初始几何锚点，使优化更快收敛到正确表面。

4. **密度控制中拆分大高斯 vs 不拆分（Fig. 8）：** 拆分策略对背景重建至关重要。大高斯覆盖过重建区域时，拆分为两个较小高斯能更精细地贴合几何边界，改善背景区域的清晰度。

5. **限制梯度传播数量（Limited-BW, Table 3, Fig. 9）：** 将接收梯度的高斯数量限制为10个时，PSNR**骤降约11dB**。Figure 9显示限制梯度传播导致严重的重建失败——颜色错误、几何模糊。这验证了本文可微光栅化器支持任意数量高斯混合进行反向传播的必要性：深度复杂场景中，正确的梯度分配需要穿透多层高斯到达被遮挡的表面。

**失败模式与适用边界（Figures 11, 12）。**

- **各向异性高斯的粗粒度伪影（Fig. 11）：** 在Train场景中，Mip-NeRF360产生“漂浮物”和颗粒感伪影（前景），而本文方法在背景区域产生粗粒度的各向异性高斯，导致低细节视觉效果。这说明当场景包含极细纹理或高频细节时，当前的高斯密度控制策略可能无法充分细化，各向异性形状本身成为可见的结构化伪影。
- **视角覆盖不足（Fig. 12）：** 在DrJohnson场景中，测试视角与训练视角重叠很少时，本文方法产生明显伪影。Mip-NeRF360在此情况下同样有伪影，但表现形式不同。这揭示了显式几何表示（3D高斯）和隐式表示（MLP）在泛化到未见视角时的共同局限：缺乏足够的观测约束时，两种方法都无法可靠推断被遮挡或未观测区域的辐射场。
- **存储与内存：** 典型场景需要1-5百万个高斯，每个高斯存储位置、协方差（缩放+四元数，8个浮点数）、不透明度、以及最高4阶SH系数（48个浮点数/颜色通道×3通道），总显存占用较大，不适合移动设备部署。
- **镜面反射和复杂光照：** 对强镜面反射和复杂光照效果的建模依赖SH系数的表达能力，4阶SH可能不足以捕捉极尖锐的高光或复杂的环境光照变化。

**训练效率的深层分析。** 训练加速的关键因果链：显式3D高斯表示避免了隐式MLP的多次前向推理 → 基于tile的可微光栅化器利用GPU排序和并行混合，单次前向/反向传播极快 → 自适应密度控制仅在必要时增加高斯，避免冗余计算 → 整个优化循环的每次迭代开销远低于基于光线行进的NeRF方法。Figure 6展示了7K迭代（约5-8分钟）与30K迭代（约35分钟）的视觉差异：多数场景在7K时已捕获主要结构，30K时背景伪影显著减少；部分场景7K时已接近收敛，说明优化效率极高。

![[assets/figures/papers/paper_list_l3_https_repo_sam_inria_fr_fungraph_3d_gaussian_splatting/figures/006_Table_1.jpg]]
*Table 1: Quantitative evaluation of our method compared to previous work, computed over three datasets. Results marked with dagger † have been directly adopted from the original paper, all others were obtained in our own experiments*

![[assets/figures/papers/paper_list_l3_https_repo_sam_inria_fr_fungraph_3d_gaussian_splatting/figures/008_Table_2.jpg]]
*Table 2: PSNR scores for Synthetic NeRF, we start with 100K randomly initialized points. Competing metrics extracted from respective papers*

## 定位与知识库关联

本文的核心贡献在于同时改变了神经渲染管线中的**场景表示**与**渲染方式**两个关键槽位，并配套设计了适配新表示的**优化策略**，从而在保持高视觉质量的前提下首次实现实时渲染。

### 相对已有方法的本质差异

**场景表示槽位**：将传统的隐式MLP（NeRF, Mildenhall et al., ECCV 2020）或离散网格结构（InstantNGP, Müller et al., SIGGRAPH 2022; Plenoxels, Fridovich-Keil and Yu et al., CVPR 2022）替换为**显式3D高斯基元集合**。每个基元携带位置、各向异性协方差、不透明度及球谐系数，构成一个可微的连续体积表示。这一替换的关键洞察在于：3D高斯既保留了体积表示对复杂几何和视角相关外观的建模能力，又天然支持类似点云的快速投影和混合操作，从而绕开了隐式表示必须依赖昂贵光线行进的瓶颈。

**渲染方式槽位**：将基于光线行进的随机采样体积渲染替换为**基于tile的排序光栅化**。传统方法需要沿每条光线采样数十至数百个点进行前向和反向计算，而本文的渲染器将屏幕划分为16×16的tile，利用GPU基数排序对投影后的2D高斯按深度排序，然后前向混合累积颜色和alpha值。反向传播时复用排序结果，仅对影响当前像素的高斯子集计算梯度。这一设计使得训练和推理的计算复杂度从光线采样数转向实际可见的基元数量，是实现实时渲染的直接原因。

**优化策略槽位**：配合新表示引入**自适应密度控制**机制。基于视图空间位置梯度的幅值判断场景区域是欠重建还是过重建，分别执行高斯克隆或分裂操作，同时周期性重置不透明度以消除漂浮伪影。这与传统NeRF的固定采样策略形成对比——后者无法动态调整表示容量以适应场景的几何复杂度分布。

### 知识库挂载点

本文的方法架构可挂载到以下知识库节点：

1. **可微渲染**：本文的tile-based光栅化器是一个完全可微的渲染前端，其反向传播机制可挂载到可微图形学知识库中，作为点基元快速可微渲染的参考实现。与SoftRas（Liu et al., ICCV 2019）等面向网格的可微光栅化不同，本文处理的是半透明体积基元的有序混合，更接近体积渲染的物理本质。

2. **点云表示学习**：3D高斯的优化过程可视为从多视图图像中学习结构化点云表示。每个高斯的位置、形状和外观参数通过梯度下降联合优化，这与Point-NeRF（Xu et al., CVPR 2022）等基于点的神经渲染方法形成互补——后者使用神经网络预测点属性，而本文直接优化显式参数，避免了推理时的网络前传开销。

3. **实时图形学**：tile-based排序光栅化借鉴了移动GPU的延迟渲染架构设计，但针对各向异性泼溅和alpha混合进行了定制。该渲染器可挂载到实时渲染知识库，作为基于GPU排序的可微泼溅渲染范式。

4. **球谐光照**：外观的视角依赖性通过球谐系数建模，这与预计算辐射传输（PRT, Sloan et al., SIGGRAPH 2002）使用SH表示低频光照的思想一致。本文将其融入可优化管线，每高斯独立学习SH系数，为动态场景中SH系数的在线优化提供了新思路。

### 适用边界与局限

该方法在以下条件下表现优异：输入为多视图捕获且SfM能提供合理的稀疏点云初始化；场景以漫反射为主，镜面成分可由低阶SH近似；目标平台具有支持CUDA的GPU。但在以下边界外性能下降：

- **视角覆盖不足区域**（如场景边缘或大视角变化处）会产生模糊或粗粒度伪影（Fig. 11, Fig. 12），因为高斯优化的梯度信号主要来自训练视角覆盖的区域。
- **高镜面反射和复杂光照场景**受限于SH系数的表达容量，可能无法准确重现高频高光细节。
- **存储开销**：每场景需1-5百万个高斯，每个高斯存储位置、协方差（缩放+四元数）、不透明度和SH系数，总显存占用较大，不适合移动或嵌入式设备。

### 后续启发与可迁移价值

本文的核心方法论——用显式可微基元替代隐式表示，配合专用高效渲染器——具有跨领域的迁移潜力：

1. **网格重建与图形管线集成**：优化后的各向异性高斯集合可作为表面重建的中间表示，通过提取等值面或拟合网格，桥接神经渲染与传统图形管线。这是论文提出的开放问题之一，也是后续工作（如SuGaR, Guédon and Lepetit, SIGGRAPH 2024）的直接切入点。

2. **压缩与传输**：高斯的显式结构化存储使其天然适合点云压缩技术（如G-PCC, MPEG标准），可探索量化、剪枝和熵编码策略来降低存储和传输开销。

3. **动态场景扩展**：将高斯的运动参数化（如引入每高斯的变形场或速度向量），可扩展到时变场景的实时渲染。已有后续工作（如4D Gaussian Splatting, Wu et al., ICLR 2024）沿此方向推进。

4. **与其他模态融合**：SH系数的优化框架可扩展为学习更复杂的外观函数（如小型MLP或更高阶SH），以提升对复杂光照的建模能力。同时，SfM初始化的依赖可通过引入深度估计或单目几何先验来放松，降低对输入质量的敏感度。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/3D_Gaussian_Splatting_for_Real_time_Radiance_Field_Rendering.pdf]]