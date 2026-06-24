---
title: Egocentric Scene Reconstruction From an Omnidirectional Video
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Egocentric_Scene_Reconstruction_From_an_Omnidirectional_Video.pdf
project_link: "https://vclab.kaist.ac.kr/siggraph2022p2/"
code_link: "https://github.com/KAIST-VCLAB/EgocentricReconstruction"
aliases:
- ESRSB
- ESRFOV
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入球形 binoctree 数据结构，在球坐标下采用自适应二元径向细分（防止节点过度伸长）与八叉树角度细分，使体素分辨率随距离自然变化；同时结合深度相关的截断阈值以及基于邻近、深度一致性和颜色一致性的置信加权 TSDF 融合，鲁棒地处理深度误差。
primary_logic: 将体积表示参数化为球面视锥，可根据距离动态分配细节层次，从而从短的自中心全向视频中高效重建高质量的场景级几何与纹理。
claims:
- 球形 binoctree 显著节省内存：Sponza 场景下仅需 0.08 GB，而 Cartesian octree（naïve）超过 27 GB（表 2）。
- 重建精度全面超越基线：深度 MAE 0.006（Mesh only）、颜色 PSNR 23.91，均优于 VoxelHashing、COLMAP MVS 以及 OmniSLAM（表 3）。
- Synthetic scenes (Sponza) 上 Depth MAE (Mesh only, ↓) = 0.006
- Synthetic scenes (Sponza) 上 Color PSNR (Mesh, ↑) = 23.91
---

# Egocentric Scene Reconstruction From an Omnidirectional Video

> [!tip] 核心洞察
> 将体积表示参数化为球面视锥，可根据距离动态分配细节层次，从而从短的自中心全向视频中高效重建高质量的场景级几何与纹理。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于全向视频的自我中心场景重建 |
| 英文题名 | Egocentric Scene Reconstruction From an Omnidirectional Video |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://vclab.kaist.ac.kr/siggraph2022p2/) · [Code](https://github.com/KAIST-VCLAB/EgocentricReconstruction) · [Project](https://casual-effects.com/data) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Egocentric Scene Reconstruction with Spherical Binoctree |
| Dataset | Synthetic scenes, Memory usage |

> [!tip] 效果简介
> - Synthetic scenes (Sponza) 上，Depth MAE (Mesh only, ↓) 0.006 vs 0.025 (VoxelHashing) (-0.019 (76% reduction))；Depth MAE (Mesh only, ↓) 0.006 vs 0.012 (COLMAP MVS) (-0.006 (50% reduction))；Color PSNR (Mesh, ↑) 23.91 vs 21.46 (VoxelHashing) (+2.45)。
> - Memory usage (Sponza) 上，Memory (GB, ↓) 0.08 vs >27.0 (Cartesian octree naïve) (reduction >100x)。

## 概要

针对手持全向相机拍摄的短序列自中心视频，传统体积重建方法因使用笛卡尔体素网格或八叉树，难以在球面投影下有效分配空间分辨率——固定体素大小导致远处表面细节不足、近处内存浪费，且难以从短轨迹中重建完整场景几何。本文提出一种基于**球形 binoctree** 的自适应体积重建方法：首先通过球面校正与微调的 RAFT 光流网络估计每帧深度图，随后在球坐标系中构建 binoctree 数据结构，以自适应二元径向细分与八叉树角度细分相结合的方式分配体素分辨率，并采用深度相关的截断阈值与置信加权 TSDF 融合策略，鲁棒地处理深度误差。最后通过 dual marching cubes 提取网格，并以等边三角形平铺纹理图实现高质量纹理重建。实验表明，该方法在合成场景上深度 MAE 降至 0.006（相较 VoxelHashing 降低 76%），颜色 PSNR 达 23.91，内存占用仅 0.08 GB（笛卡尔八叉树超过 27 GB），在精度与效率上均显著优于现有体积重建与多视图立体方法。

## 核心方法与创新机理

**核心瓶颈**：传统基于笛卡尔体素网格或八叉树的体积重建方法，在面向全向视频的自中心场景重建中存在根本性不适应。固定大小的体素导致远处表面分辨率不足、近处内存严重浪费，且难以从短轨迹视频中捕获完整的场景几何。此外，全向视频的球面投影特性要求表示方法能够自然地适应角度采样密度的非均匀分布。

**核心洞察**：将体积表示参数化为球面视锥，通过球坐标下的自适应细分策略，使体素分辨率随径向距离动态变化——近处精细、远处稀疏，从而在内存效率与重建精度之间取得最优平衡。同时，引入深度相关的截断阈值与多维度置信加权融合机制，鲁棒地处理全向深度估计中的系统性误差。

---

### 1. 球形深度估计

方法首先从输入的全向视频中估计每帧的稠密深度图。核心思路是将光流估计网络适配到球面视差估计任务上。

**球面校正与视差几何**：采用 Li (2008) 的球面校正技术，将全向图像对变换为极线水平对齐的校正视图。对于基线为 $b$ 的立体对，三维点 $P$ 在参考视图和邻居视图上的投影角分别为 $\phi_{\mathrm{ref}}$ 和 $\phi_{\mathrm{neigh}}$，其球面角度视差 $\delta$ 与径向距离 $d$ 的关系为：

$$\delta = \arctan \left( \frac { b \sin \phi _ { \mathrm { ref } } } { d - b \cos \phi _ { \mathrm { ref } } } \right)$$

角度视差通过 $\Delta = \frac{w\delta}{\pi}$ 线性缩放为像素视差，其中 $w$ 为图像宽度。这一转换将球面深度估计问题规约为可被现有光流网络处理的像素视差回归问题。

**网络适配与训练**：以 RAFT（Teed and Deng, ECCV 2020）为基础网络，在其特征提取与匹配模块上进行微调。为训练该网络，作者构建了一个包含 12 个多样化场景、102 段直立全向 RGBD 视频的合成数据集，每段视频包含 500 帧。训练时将输入分辨率从 $1024\times2048$ 降至 $768\times1536$ 以适应 GPU 内存限制。

**多帧融合**：对每帧参考视图，选择 $N=11$ 个时间上最近且基线超过最小阈值的邻居帧构成立体对，独立估计 $N$ 个视差图，再通过逐像素中值滤波融合为单张更鲁棒的深度图，有效剔除异常估计值。

---

### 2. 球形 Binoctree 数据结构（核心 changed slot）

这是方法最关键的创新——将体积表示从笛卡尔坐标系迁移到球坐标系，并设计混合细分策略。

**数据结构设计**：球形 binoctree 以相机轨迹中心为原点，在球坐标 $(r, \theta, \phi)$ 下组织体素节点。每个节点是一个球形视锥（spherical frustum），其边界由径向范围 $[r_{\min}, r_{\max}]$、极角范围 $[\theta_{\min}, \theta_{\max}]$ 和方位角范围 $[\phi_{\min}, \phi_{\max}]$ 定义。

**混合细分策略**：节点的细分方式取决于其形状是否“平衡”，即是否过度伸长。平衡条件由以下公式判定：

$$1.4 \times ( \phi_{\max} - \phi_{\min} ) \left( \frac{ r_{\min} + r_{\max} }{ 2 } \right) < r_{\max} - r_{\min}$$

- **八叉树角度细分**：当节点满足平衡条件且立体角 $\Omega$ 超过阈值 $T_{\mathrm{solid}}$ 时，沿 $\theta$ 和 $\phi$ 维度各二分，产生 8 个子节点。这类似于传统八叉树的空间划分，但在球面上进行。

- **二元径向细分**：当节点不满足平衡条件（即径向跨度远大于角度跨度，视锥过度伸长）时，仅沿径向维度二分，产生 2 个子节点。这一机制防止了节点形状的极端变形，确保体素在三维空间中保持合理的宽高比。

节点体积的计算公式为：

$$V_{\mathrm{node}} = \frac{1}{3} ( r_{\max}^3 - r_{\min}^3 ) ( \cos \theta_{\min} - \cos \theta_{\max} ) ( \phi_{\max} - \phi_{\min} )$$

该自适应策略使得体素大小随径向距离自然增长：近处物体获得高分辨率体素，远处表面使用大尺寸体素，完美匹配全向视频的采样密度分布特性。

---

### 3. 置信加权 TSDF 融合（changed slots）

在球形 binoctree 的每个叶节点中存储截断符号距离函数（TSDF）值，并通过多帧观测进行增量融合。与传统方法相比，本方法在两个关键维度上进行了改进。

**深度相关截断阈值**：传统 TSDF 使用固定截断距离，无法适应全向深度估计中随距离增大的误差。本方法将截断阈值设为估计深度的线性函数：

$$T_{\mathrm{trunc}}(D^{\mathrm{est}}) = e_{\mathrm{m}} D^{\mathrm{est}} + e_{\mathrm{n}}$$

其中 $e_{\mathrm{m}}$ 和 $e_{\mathrm{n}}$ 为可调参数。远处表面获得更大的截断区间，容忍更大的深度不确定性；近处表面保持较窄的截断区间，保留精细几何细节。

**多维置信加权**：每次 TSDF 更新时，融合权重 $w_{\mathrm{update}}$ 由三个互补的置信度分量组合而成：

- **邻近权重**：惩罚远处相机对当前体素的贡献，因为远距离观测的深度估计更不可靠：

$$w_{\mathrm{p}}(i, p) = \exp\left(-\left(D_i^{\mathrm{est}}(p)\right)^2 / \sigma_{\mathrm{p}}\right)$$

- **深度一致性权重**：比较参考视图与邻居视图的深度估计一致性。先将深度转换为校正距离 $\widetilde{D}_i^{\mathrm{est}}(p) = D_i^{\mathrm{est}}(p) \sin \phi_{\mathrm{rect}}(p)$（即三维点到立体相机连线的垂直距离），再计算一致性：

$$w_{\mathrm{d}}(i, j, p) = \exp(-(1 - \frac{\widetilde{D}_i^{\mathrm{est}}(p)}{\widetilde{D}_j^{\mathrm{est}}(\pi_{ij}(p))})^2 / \sigma_{\mathrm{d}})$$

- **颜色一致性权重**：评估视图间的光度一致性，抑制动态物体和镜面反射区域的错误深度：

$$w_{\mathrm{c}}(i, j, p) = \exp(-\|I_i(p) - I_j(\pi_{ij}(p))\|_2^4 / \sigma_{\mathrm{c}})$$

三者共同构成鲁棒的融合权重，使 TSDF 融合能够自动抑制深度异常值、动态物体伪影和反射表面的干扰。

---

### 4. 网格提取与纹理重建

**表面提取**：在 TSDF 融合完成后，采用 dual marching cubes（Schaefer and Warren, 2005）算法从球形 binoctree 中提取三角网格。该算法直接在对偶图上进行等值面提取，天然适配八叉树结构，无需进行八叉树到规则网格的转换。

**纹理图集重建**：为生成高分辨率纹理，方法采用等边三角形平铺纹理图（equilateral triangle tiling texture map）。对每个三角形面片，从多个候选视图中基于可见性评分选择最优纹理帧。评分函数综合考虑法线方向与视线夹角、相机距离、可见性以及深度一致性：

$$S({p}) = \frac{\mathbf{n} \cdot \mathbf{v}}{D^{\mathrm{tri}}({p})} \times \left\{ \begin{array}{ll} {M^{\prime}({p})} & {\mathrm{if} V(p) \leq 1.02} \\ {(M^{\prime}({p}) - 2) V(p)} & {\mathrm{if} V(p) > 1.02} \end{array} \right.$$

该策略优先选择正视角度、近距离且深度验证一致的视图，从而最大化纹理分辨率和清晰度。

---

### 模块间因果关系

整个管道的模块间存在紧密的因果依赖：**球形深度估计**为后续融合提供逐帧几何先验，其误差特性（随距离增大）直接驱动了**球形 binoctree** 的自适应细分策略和**深度相关截断阈值**的设计；binoctree 的体素分辨率分布又决定了 TSDF 融合的精度上限；**置信加权机制**通过邻近、深度一致性和颜色一致性三个维度，在融合阶段对深度估计的不可靠区域进行软抑制，弥补前端深度网络的不足；最终，高质量的 TSDF 场为**网格提取**和**纹理重建**提供了准确的几何基础，使纹理选择评分能够可靠地评估各候选视图的可见性和分辨率。

![[assets/figures/papers/paper_list_l37_https_vclab_kaist_ac_kr_siggraph2022p2/figures/001_Figure_1.jpg]]
*Figure 1: We introduce a practical reconstruction method for 3D scene geometry from short handheld omnidirectional videos. (a) Example video frame captured by a 360° camera (inset). (b) An inverse depth frame estimated by our spherical disparity estimation. (c) To reconstruct egocentric scene geometry effectively from a short omnidirectional video, we devise a scene reconstruction method using a novel spherical binoctree data structure. (d) The reconstructed 3D scene geometry. (e) 3D rendering of the reconstructed scene with our texture mapping. Please see our supplemental video for additional results and comparisons*

![[assets/figures/papers/paper_list_l37_https_vclab_kaist_ac_kr_siggraph2022p2/figures/006_Figure_6.jpg]]
*Figure 6: Our spherical binoctree and subdivision schemes: (a) Illustration of our spherical binoctree with numbers in each node representing the tree depth from the root of the octree (located at*

## 实验与关键发现

### 实验设置与评估协议

本工作从三个层次验证方法有效性：两视图球面深度估计精度、体积重建内存效率与几何质量、以及最终纹理化网格的渲染质量。深度估计网络在自建的合成球面 RGBD 数据集上微调，该数据集包含 12 个场景、102 段直立球面 RGBD 视频，每段 500 帧（图 2）。所有重建对比方法使用相同的深度图输入与相机位姿，以确保公平比较。纹理化网格评估时，从重建网格渲染图像和逆深度图，分别计算仅网格像素（“Mesh”）和全部像素（“Mesh+Skybox”）的指标；完整性（Completeness）定义为有效网格像素占总像素的比例。

### 两视图球面深度估计：精度与基线对比

表 1 报告了两视图球面深度估计的定量对比。本文方法在所有指标上显著优于经典基线：与 SGM（Hirschmüller, TPAMI 2008）相比，逆深度 MAE 大幅降低，坏像素率（>0.1 m⁻¹ 和 >0.4 m⁻¹）显著减少；相较于 OmniMVS（Won et al., ICCV 2019）和未经微调的 RAFT（Teed and Deng, ECCV 2020），本文通过球面校正与微调策略，有效消除了球面投影畸变区域的系统性误差。图 5 的定性对比进一步印证：RAFT 在球面图像边缘区域产生明显伪影，而本文适配模型在畸变区域仍保持低误差。

**关键机制**：球面校正将极线对齐为水平扫描线（图 4），使原本为透视光流设计的 RAFT 网络可直接处理球面视差估计；微调则使网络适应球面视差分布与合成数据特性。每帧深度由 11 个邻近帧的视差估计经中值融合得到，进一步抑制异常值。

### 体积重建：球形 Binoctree 的内存效率与几何精度

**内存效率**（表 2）是球形 binoctree 最突出的优势。以 Sponza 场景为例，本文方法仅需 **0.08 GB** 内存，而笛卡尔八叉树（naïve，固定细分至最终层级）超过 **27 GB**，内存节省超过两个数量级。笛卡尔八叉树（solid angle 停止策略）虽可将内存降至 0.18 GB，但本文方法仍保持约 2.25 倍优势。这一差距的根源在于：笛卡尔体素在球面投影下，远处表面体素过小（浪费分辨率）、近处体素过大（浪费内存），而球形 binoctree 在球坐标下自适应细分，使体素大小随径向距离自然增长，分辨率分配与全向视频的采样密度匹配。

**重建精度**（表 3）同样全面领先。在 Sponza 合成场景上：
- 深度 MAE（仅网格像素）：本文 **0.006**，VoxelHashing（Nießner et al., SIGGRAPH 2013）为 0.025（相对降低 76%），COLMAP MVS（Schönberger and Frahm, CVPR 2016）为 0.012（降低 50%），OmniSLAM（Won et al., ICRA 2020）为 0.010（降低 40%）。
- 颜色 PSNR（仅网格像素）：本文 **23.91**，VoxelHashing 为 21.46（提升 2.45 dB），COLMAP MVS 为 22.42（提升 1.49 dB），OmniSLAM 为 22.98（提升 0.93 dB）。
- 完整性（Comp.）：本文 0.995，VoxelHashing 为 0.995，COLMAP MVS 为 0.992，OmniSLAM 为 0.995——各方法均接近饱和，但本文在同等完整性下几何精度更高。

图 9 的定性对比显示，COLMAP MVS 在纹理稀疏区域产生孔洞，OmniSLAM 在远处表面出现噪声，而本文方法重建出更完整、更平滑的几何。图 10 在真实场景上的对比进一步验证：COLMAP 重建的网格存在大量缺失和噪声，本文方法则恢复出更完整的房间结构。

### 关键消融：自适应截断与置信加权

图 7 通过消融实验揭示了 TSDF 融合中两个核心设计的因果效应：

1. **深度相关截断阈值**（Eq. 10: $T_{\mathrm{trunc}}(D^{\mathrm{est}}) = e_{\mathrm{m}} D^{\mathrm{est}} + e_{\mathrm{n}}$）：固定阈值（图 7b）在远距离表面产生大量孔洞，因为远距离深度估计误差天然更大，固定截断区间无法有效跨越零交叉面。自适应阈值（图 7c）使截断距离随估计深度线性增长，有效填充远距离孔洞，提升重建完整性。

2. **置信加权融合**：在自适应阈值基础上，融入邻近权重（Eq. 11: $w_{\mathrm{p}}$，惩罚远处相机）、深度一致性权重（Eq. 13: $w_{\mathrm{d}}$，抑制不一致深度估计）和颜色一致性权重（Eq. 14: $w_{\mathrm{c}}$，减少动态物体与镜面反射影响），显著改善 TSDF 融合质量（图 7d vs 7e）。无置信加权时，动态物体和反射区域产生明显伪影；引入置信加权后，这些区域的噪声被有效抑制。

### 失败模式与适用边界

图 12 系统展示了三类典型失败案例，揭示了方法的能力边界：

1. **细薄结构**（图 12 左）：深度估计在锐利边缘和细薄物体（如栏杆、植物枝叶）处误差增大，导致几何细节丢失或断裂。根本原因在于球面视差网络的空间分辨率有限（输入 768×1536），且基于相关性的光流方法本身对细薄结构不敏感。

2. **镜面反射表面**（图 12 中）：窗户、镜子等反射表面产生不一致的深度估计——反射内容在不同视点间不满足朗伯假设，导致深度一致性权重降低、TSDF 融合失败，该区域网格出现孔洞或噪声。

3. **动态物体纹理**（图 12 右）：即使网格重建成功（TSDF 融合可通过置信加权抑制动态物体对几何的影响），纹理映射仍可能产生鬼影伪影。因为纹理选择基于可见性评分（Eq. 19），但动态物体在不同帧间位置变化，最优帧选择无法保证纹理一致性。

此外，方法设计针对**短自中心轨迹**优化：当相机轨迹较长时，累积的光度不一致和反射会降低深度估计可靠性，进而影响重建质量。这一约束源自全向视频自中心拍摄的典型使用场景——用户手持 360° 相机在原地或小范围移动拍摄。

### 实验证据强度评估

- **高置信度发现**：球形 binoctree 的内存效率优势（表 2，>100× 降低）和重建精度对 VoxelHashing 的显著领先（表 3，深度 MAE 降低 76%）有坚实的定量支撑，且对比条件公平（相同输入深度与位姿）。
- **中等置信度发现**：自适应截断与置信加权的消融（图 7）提供了有力的定性证据，但缺乏定量指标（如完整性提升百分比），需手动验证具体数值。
- **需注意的局限**：对比方法未包含基于 NeRF 或隐式表示的最新重建技术（如 Instant-NGP、3D Gaussian Splatting），这些方法在 2022 年后迅速发展，可能在某些场景下超越本文的显式网格重建质量。深度估计网络在合成数据上微调，对真实场景的泛化偏差未做定量分析。

![[assets/figures/papers/paper_list_l37_https_vclab_kaist_ac_kr_siggraph2022p2/figures/012_Table_2.jpg]]
*Table 2: Given the same image and depth sequence as input, our spherical binoctree is more memory-efficient thanks to adaptively sized voxels. ‘Cartesian octree (naïve)’ divides voxels always until the final level, while ‘Cartesian octree (solid angle)’ stops dividing voxels with the same rule as our spherical binoctree. The right-most column shows the volume of voxels*

![[assets/figures/papers/paper_list_l37_https_vclab_kaist_ac_kr_siggraph2022p2/figures/009_Figure_9.jpg]]
*Figure 9: Comparison of synthetic reconstruction accuracy with COLMAP [Schönberger and Frahm 2016; Schönberger et al. 2016] and OmniSLAM [Won et al. 2020] for central spherical views. Note that COLMAP’s reconstruction shows artifacts (top), and OmniSLAM’s reconstruction truncates the north/south poles and distant regions. Our reconstruction is the closest to the ground truth. Refer to Table 3 for depth and color error metrics*

![[assets/figures/papers/paper_list_l37_https_vclab_kaist_ac_kr_siggraph2022p2/figures/013_Table_3.jpg]]
*Table 3: Textured mesh reconstruction comparison. For each method, we render images and inverse depth maps using the reconstructed mesh. We evaluate the quality of just the mesh pixels (‘Mesh’) and all pixels (‘Mesh+Skybox’). Completeness (‘Comp.’) is defined as the proportion of pixels that see the mesh compared to the ground truth. Our textured mesh shows the highest geometry and texture accuracy while retaining a high completeness. The large Cartesian octree mesh crashes the texturing pipeline (out-of-memory). See Figure 9 for visual results*

![[assets/figures/papers/paper_list_l37_https_vclab_kaist_ac_kr_siggraph2022p2/figures/015_Figure_12.jpg]]
*Figure 12: Example failure cases. Left: Thin objects are hard to reconstruct due to the lack of depth accuracy. Center: Specular reflections can cause incorrect depth estimation and mesh reconstruction. Right: Texture reconstruction can fail for dynamic objects even if mesh reconstruction succeeds*

## 定位与知识库关联

本文的核心贡献在于为**自中心全向视频的体积重建**更换了三个关键设计槽位，从而解决了传统笛卡尔体积表示在球面投影场景下的根本性不适配问题。

**改变的槽位与本质差异**

第一个也是最根本的槽位变化是**体积表示的数据结构**：从笛卡尔体素网格/八叉树（固定体素大小）替换为**球形 binoctree**（球坐标下的自适应混合细分）。传统方法如 **VoxelHashing**（Nießner et al., SIGGRAPH 2013）和 **Cartesian octree**（Zeng et al., Graphical Models 2013）使用欧氏空间中的均匀或八叉树细分，其体素大小与场景位置无关。这在处理全向视频时产生结构性矛盾：等大小体素在近处浪费内存、在远处分辨率不足。球形 binoctree 将表示参数化为以相机为中心的球面视锥，通过二元径向细分（防止节点过度伸长，平衡条件见 Eq. 7）与八叉树角度细分的混合策略，使体素分辨率随径向距离自然衰减。这一改变直接带来了内存效率的数量级提升（Sponza 场景下 0.08 GB vs. Cartesian octree 的 >27 GB，Table 2），是本文区别于所有基于笛卡尔体积的基线方法（**COLMAP MVS** [Schönberger and Frahm, CVPR 2016; Schönberger et al., ECCV 2016]、**OmniSLAM** [Won et al., ICRA 2020]）的本质差异。

第二个槽位变化是 **TSDF 截断阈值**：从固定阈值替换为**深度相关的自适应阈值** $T_{\mathrm{trunc}}(D^{\mathrm{est}}) = e_{\mathrm{m}} D^{\mathrm{est}} + e_{\mathrm{n}}$（Eq. 10）。传统体积融合使用固定截断距离，隐含假设深度误差在场景各处均匀。但在全向深度估计中，误差随距离增大而显著增加——远处表面的深度不确定性远大于近处。自适应截断使融合算法在远处容忍更大的深度偏差，有效减少了远距离表面的孔洞（消融可视化见 Figure 7b vs 7c）。这一设计与球形 binoctree 的径向分辨率衰减形成协同：远处体素更大、截断更宽，共同适应了全向深度估计的误差分布特性。

第三个槽位变化是 **TSDF 融合权重**：从均匀权重或简单平均替换为**置信加权**，融合了邻近权重 $w_{\mathrm{p}}$（Eq. 11）、深度一致性权重 $w_{\mathrm{d}}$（Eq. 13）和颜色一致性权重 $w_{\mathrm{c}}$（Eq. 14）三个高斯核。这一设计直接针对自中心全向视频的独特挑战：相机始终位于场景中心，近处表面在多个视图中可见但分辨率差异大，远处表面仅被少数视图覆盖且深度不确定性高；同时，动态物体和镜面反射（全向相机常见问题）会导致局部深度估计错误。置信加权通过多视图几何和光度一致性检验抑制不可靠的深度观测，消融实验（Figure 7d vs 7e）证实其显著改善了融合质量。这一策略与 **OmniSLAM** 的 TSDF 融合形成对比：后者虽也针对全向视频，但未引入如此精细的多维度置信度建模。

此外，**纹理分配方式**从传统 UV 展开替换为**等边三角形平铺纹理图 + 基于可见性评分的最优帧选择**（Eq. 19），利用自中心轨迹中近处帧对同一表面提供更高分辨率纹理的特性，在纹理图集中优先选择最近且最正对表面的视图。该设计使纹理 PSNR 达到 23.91 dB，优于 VoxelHashing 的 21.46 dB 和 COLMAP MVS 的 22.42 dB（Table 3）。

**知识库挂载点**

本文在知识库中的定位是**体积三维重建 × 全向视觉 × 数据结构设计**的交叉节点。其上游依赖包括：(1) 球面校正理论（Li, 2008），为球面立体匹配提供极线约束；(2) 基于光流的深度估计网络 **RAFT**（Teed and Deng, ECCV 2020），本文将其改造为球面视差估计器；(3) **Dual Marching Cubes**（Schaefer and Warren, 2005），用于从自适应八叉树提取等值面。下游可挂载的方向包括：基于 NeRF 或 3D Gaussian Splatting 的全向场景表示（本文的球形 binoctree 可作为初始化或先验结构）、长轨迹全向 SLAM 的体积建图模块、以及动态场景的几何-纹理联合优化。

**适用边界**

本方法针对**短自中心轨迹**优化，核心假设是相机在场景中心附近运动且大部分表面在多个视图中可见。当相机轨迹较长、远离初始中心时，球形 binoctree 的径向分辨率衰减可能导致远处新增区域的几何精度下降；同时，光度不一致和反射累积会加剧深度估计误差。对于包含大量动态物体的场景，即使网格重建可通过置信加权保持鲁棒（Figure 12 右），纹理映射仍可能出现鬼影伪影——因为纹理选择仅基于静态几何的可见性评分，缺乏对动态区域的显式建模。反射表面（窗户、镜子）是另一个明确的失效模式（Figure 12 中）：深度估计网络在这些区域产生系统性错误，TSDF 融合即使有置信加权也难以完全补偿。细薄结构（Figure 12 左）则受限于深度估计网络的空间分辨率上限（输入 768×1536），几何细节丢失是上游模块的瓶颈而非体积融合本身的问题。

**后续启发**

本文提出的球形 binoctree 作为一种自适应体积表示，其核心思想——在球坐标系中根据信息密度动态分配表示容量——可推广至其他以自我为中心的 3D 感知任务（如 VR/AR 场景建图、机器人导航的环境表示）。将球形 binoctree 与基于学习的隐式表示（如 NeRF 的球面变体）结合，用前者提供高效的空间划分和粗几何先验，用后者补充细粒度的外观和几何细节，是一个值得探索的方向。此外，本文的置信加权融合框架可扩展为端到端可学习的 TSDF 融合模块，使深度估计网络和体积融合在训练中联合优化，有望进一步提升对反射和动态物体的鲁棒性。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Egocentric_Scene_Reconstruction_From_an_Omnidirectional_Video.pdf]]