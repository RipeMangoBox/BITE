---
title: A Dynamic By-example BTF Synthesis Scheme
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2024/A_Dynamic_By_example_BTF_Synthesis_Scheme.pdf
project_link: null
code_link: null
aliases:
- CS3GSM
- DBEBSS
tags:
- SIGGRAPH_ASIA_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过将3DGS方法按功能分类为三维重建（质量增强、压缩、动态重建、挑战性输入）、三维编辑（几何、外观、物理模拟）和下游应用（SLAM、数字人、3D/4D生成），揭示了关键设计选择（如高斯属性建模、优化策略、变形场表示）对任务性能的影响。
primary_logic: 3DGS通过显式高斯椭球和光栅化渲染，在保持与NeRF相当的重建质量（PSNR约27–29 dB）的同时，将训练时间缩短至约30分钟，渲染速度提升至30 FPS以上，并且其显式表示天然支持几何编辑、物理模拟和快速生成等高级任务。
claims:
- 该综述将3DGS方法系统分类为三维重建、编辑和下游应用三大类，并通过时间线展示了代表性工作。
- 3DGS在保持高质量视角合成的同时，训练时间约30分钟，渲染速度≥30 FPS，远优于NeRF。
- 3DGS的显式表示便于进行动态重建、几何编辑和物理模拟等下游任务，推动了该领域的快速发展。
- Novel View Synthesis (general) 上 Training Time = ~30 minutes
---

# A Dynamic By-example BTF Synthesis Scheme

> [!tip] 核心洞察
> 3DGS通过显式高斯椭球和光栅化渲染，在保持与NeRF相当的重建质量（PSNR约27–29 dB）的同时，将训练时间缩短至约30分钟，渲染速度提升至30 FPS以上，并且其显式表示天然支持几何编辑、物理模拟和快速生成等高级任务。

| 字段 | 内容 |
|------|------|
| 中文题名 | 3D高斯溅射的最新进展 |
| 英文题名 | A Dynamic By-example BTF Synthesis Scheme |
| 会议/期刊 | SIGGRAPH ASIA 2024 |
| Links | [paper](https://sites.cs.ucsb.edu/~lingqi/#publications) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | Comprehensive Survey of 3D Gaussian Splatting Methods |
| Dataset | Novel View Synthesis, D-NeRF Dataset, MipNeRF 360 Dataset |

> [!tip] 效果简介
> - Novel View Synthesis (general) 上，Training Time ~30 minutes vs Hours (NeRF) (~10x faster)；Rendering Speed ≥30 FPS at 1080p vs Non-interactive (NeRF) (Real-time capable)。
> - D-NeRF Dataset 上，PSNR (best 3DGS-based method) 43.30 (SC-GS) vs 31.69 (D-NeRF original) (+11.61)。
> - MipNeRF 360 Dataset 上，PSNR (Scaffold-GS) 28.84 vs 27.57 (MipNeRF 360) (+1.27)。

## 概要

3D高斯溅射（3DGS）作为一种显式辐射场表示，通过一组可微的高斯椭球体来建模三维场景，并以光栅化方式实现高效渲染。相较于NeRF，3DGS在保持可比重建质量（PSNR约27–29 dB）的同时，将训练时间缩短至约30分钟，渲染速度达到实时水平（≥30 FPS @ 1080p），显著降低了三维重建与视角合成的计算门槛。

然而，3DGS的离散椭球表示在抗锯齿、动态重建、压缩效率、几何编辑和可控生成等方面仍面临诸多挑战，该领域近年来涌现出大量改进工作，但缺乏系统性的分类与总结。本文作为一篇综述，对现有3DGS方法进行了全面梳理，按功能将其划分为**三维重建**（质量增强、压缩、动态重建、挑战性输入）、**三维编辑**（几何编辑、外观编辑、物理模拟）和**下游应用**（SLAM、数字人、3D/4D生成）三大板块，并通过时间线和定量对比表展示了代表性工作的演进脉络与性能差异。

综述揭示了关键设计选择（如高斯属性建模、优化策略、变形场表示）对各任务性能的影响机制，同时指出了当前方法的局限性：稀疏视图重建鲁棒性不足、几何表面质量不及传统网格方法、三维编辑需重新优化、4D生成仍处初期阶段、跨平台支持有限等。这些开放问题为后续研究提供了明确方向。

## 核心方法与创新机理

### 问题瓶颈与综述定位

3D高斯溅射（3D Gaussian Splatting, 3DGS）自提出以来，以显式高斯椭球表示和光栅化渲染实现了实时视角合成，训练时间约30分钟、渲染速度≥30 FPS（1080p），在保持与NeRF相当的重建质量（PSNR约27–29 dB）的同时大幅提升了效率。然而，3DGS的离散椭球表示在抗锯齿、动态重建、压缩效率、几何编辑和可控生成等方面仍面临诸多挑战，且缺乏系统性的分类框架来梳理各方法的改进路径和设计选择。本综述的核心贡献在于构建了一个三级分类体系，将现有3DGS方法按功能归入**三维重建**、**三维编辑**和**下游应用**三大板块，并进一步细分为质量增强、压缩、动态重建、挑战性输入、几何编辑、外观编辑、物理模拟、SLAM、数字人和3D/4D生成等子任务，揭示了关键设计选择（如高斯属性建模、优化策略、变形场表示）对任务性能的影响机制。

### 3DGS基础表示与渲染管线

3DGS的核心机制建立在显式高斯椭球表示和可微光栅化渲染之上。与NeRF沿光线密集采样点基的方式不同，3DGS直接优化一组三维高斯椭球，每个椭球携带以下可学习属性：位置 $P \in \mathbb{R}^3$、旋转 $R$（四元数）、尺度 $S$、不透明度 $\alpha$ 和球谐系数（SH）用于视角相关的颜色建模。渲染时，3DGS将三维高斯椭球投影到二维图像平面，投影协方差矩阵由下式给出：

$$\Sigma' = J W \Sigma W^T J^T$$

其中 $\Sigma$ 为三维协方差矩阵，$W$ 为视图变换矩阵，$J$ 为投影变换的雅可比矩阵。随后通过基于光栅化的混合渲染累积像素颜色，避免了NeRF中沿光线密集采样的计算开销。这一设计构成了3DGS方法链的**基础模块**：显式几何表示→投影变换→光栅化混合渲染。所有后续改进方法均在此模块链的特定环节插入新的约束、优化策略或表示变换。

### 分类框架与关键设计维度

综述将现有工作按功能分为三大类，每类对应不同的**changed slots**——即相对于原始3DGS框架被修改或增强的模块：

**（1）三维重建类**：聚焦于提升视角合成质量和场景表示的效率。关键changed slots包括：
- **高斯属性建模**：在原始SH颜色和协方差参数基础上引入频率约束（Mip-Splatting）、法向一致性约束（GaussianPro）、向量量化编码（EAGLES、C3DGS）等，以解决抗锯齿、稀疏视图重建和存储压缩问题。
- **优化策略**：引入残差向量量化（R-VQ）压缩几何属性、敏感性感知K-Means聚类（SASCGS）编码颜色和几何特征，形成“优化→量化→码本存储”的压缩管线。
- **变形场表示**：在动态重建中，将时间维度引入高斯属性。代表性方案包括：仅将位置和旋转建模为时变变量（Luiten et al.）；通过MLP从位置编码和时间步预测位置、旋转、尺度的偏移量（Deformable3DGS）；将三维高斯扩展为四维高斯，在尺度矩阵对角线上添加时间维度缩放因子（4DGS）；以及假设场景由有限数量运动轨迹组成，学习轨迹基以获得更平滑表达（DynMF）。

**（2）三维编辑类**：利用3DGS显式表示的天然优势进行几何和外观操作。关键changed slots为：
- **几何编辑**：将高斯椭球绑定到网格面片（Gao et al.），通过编辑网格实现大规模几何变形，形成“网格变形→高斯重绑定→重渲染”的编辑管线。
- **外观编辑**：分解材质和光照分量（GS-IR），实现重光照和材质操作，其因果链为“材质-光照分解→独立编辑→重合成渲染”。
- **物理模拟**：将高斯椭球视为连续介质（PhysGaussian），直接应用物理仿真，形成“高斯表示→物理求解器→动态更新”的模拟管线。

**（3）下游应用类**：将3DGS作为基础表示嵌入更复杂的任务系统。关键changed slots为：
- **SLAM**：将3DGS作为场景地图表示，与相机位姿估计联合优化。
- **数字人**：针对全身（GPS-Gaussian）、头部（MonoGaussianAvatar）、手部（MANUS）分别设计高斯表示和变形场。
- **3D/4D生成**：从预训练二维扩散模型蒸馏生成先验，通过区间分数匹配（ISM）目标函数实现文本到三维生成（Luciddreamer），或进一步引入变形场实现文本到四维生成（AYG）。

### 方法间的因果关联与演进路径

综述揭示了一条清晰的方法演进路径：**基础表示→质量增强→压缩/动态扩展→编辑/生成应用**。质量增强方法（如Mip-Splatting的2D Mip滤波器、GaussianPro的法向一致性）首先解决了原始3DGS的抗锯齿和几何歧义问题；压缩方法（如EAGLES的向量量化、C3DGS的残差向量量化）在此基础上通过编码技术减少存储开销；动态重建方法则通过引入时间维度的变形场（MLP偏移预测、四维高斯扩展、轨迹基学习）将静态表示推广到时变场景。这些重建层面的改进为编辑和应用任务提供了更可靠的基础表示：显式高斯椭球使得几何编辑只需修改位置属性并重新绑定，物理模拟可直接将高斯视为连续介质施加力学求解，生成任务则可将高斯表示作为可微渲染器嵌入扩散蒸馏框架。

### 关键公式与变量含义

综述中涉及的两个核心公式分别对应NeRF和3DGS的渲染机制：

**NeRF体渲染公式**：
$$C = \sum_{i=1}^{N} c_i \alpha_i T_i$$
其中 $c_i$ 为采样点颜色，$\alpha_i$ 为不透明度，$T_i = \prod_{j=1}^{i-1} (1 - \alpha_j)$ 为累积透射率。该公式揭示了NeRF的计算瓶颈：需要沿每条光线密集采样 $N$ 个点并逐点评估神经网络。

**3DGS投影协方差公式**（见上文）揭示了3DGS的效率来源：通过解析投影变换将三维高斯直接映射到二维屏幕空间，避免了逐点采样和网络推理。公式中 $J$ 为投影变换的雅可比矩阵，保证了投影的局部仿射近似；$W$ 为视图变换矩阵，将世界坐标系下的高斯转换到相机坐标系。该投影的解析性使得光栅化渲染成为可能，是实现实时渲染的关键数学基础。

### 训练与推理路径

3DGS方法的通用训练路径为：从多视图图像出发，通过结构从运动（SfM）初始化点云作为高斯位置先验，然后通过可微光栅化渲染与真实图像比较，反向传播梯度优化所有高斯属性（位置、旋转、尺度、不透明度、SH系数）。训练过程中采用自适应密度控制（克隆和分裂）来调整高斯数量。推理时直接加载优化后的高斯椭球集合，通过光栅化渲染生成新视角图像，无需网络推理。

动态重建方法在此基础上增加了变形场的训练：对于每个时间步，MLP或显式参数化模型预测高斯属性的偏移量，然后通过光栅化渲染与对应时刻的真实图像比较，联合优化高斯基础属性和变形场参数。压缩方法则在训练后增加量化步骤：将优化后的高斯属性通过向量量化或聚类编码为紧凑码本，推理时通过码本索引重建高斯属性再进行渲染。

![[assets/figures/papers/paper_list_l17_https_sites_cs_ucsb_edu_lingqi_publications/figures/005_Figure_3.jpg]]
*Figure 3: Overview of GaussianPro [32]. Neighboring views’ normal direction consistency is considered to produce better reconstruction results*

![[assets/figures/papers/paper_list_l17_https_sites_cs_ucsb_edu_lingqi_publications/figures/006_Figure_4.jpg]]
*Figure 4: Pipeline from EAGLES [57]. Vector Quantization (VQ) is utilized to compress Gaussian attributes*

![[assets/figures/papers/paper_list_l17_https_sites_cs_ucsb_edu_lingqi_publications/figures/010_Figure_7.jpg]]
*Figure 7: Pipeline of Gao et al. [31]. It allows large-scale geometry editing by binding 3D Gaussians onto the mesh*

## 实验与关键发现

本综述系统汇总了3D高斯溅射（3DGS）在多个任务上的定量结果，核心发现可归纳为三个层次：**静态重建的性能基准**、**压缩方法的效率权衡**，以及**动态重建的突破性进展**。以下按任务维度展开关键实验证据。

### 静态新视角合成：质量与速度的双重优势

在MipNeRF 360数据集上，3DGS系列方法与NeRF系列方法处于同一质量水平，但渲染速度存在数量级差距。**Table 1**汇总了代表性方法的定量对比：原始3DGS取得PSNR 27.21、SSIM 0.815、LPIPS 0.214，与MipNeRF 360（PSNR 27.57、SSIM 0.793、LPIPS 0.234）互有胜负——3DGS在SSIM和LPIPS上略优，PSNR稍低。关键瓶颈在于：3DGS的离散高斯椭球在缩放或远距离观测时会产生高频伪影，导致LPIPS劣化。后续质量增强方法针对这一问题进行了改进：Scaffold-GS通过引入锚点结构将PSNR提升至28.84（较MipNeRF 360提升+1.27），Mip-Splatting通过频率约束和2D Mip滤波器抑制伪影，GaussianPro则利用相邻视图的法向一致性改善几何重建质量。

![[assets/figures/papers/paper_list_l17_https_sites_cs_ucsb_edu_lingqi_publications/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of novel view synthesis results on the MipNeRF 360 dataset [51] using PSNR, SSIM and LPIPS metrics*

更根本的优势体现在效率指标上：3DGS的训练时间约**30分钟**，渲染速度在1080p分辨率下达到**≥30 FPS**，而NeRF系列方法需要数小时训练且无法实时渲染。这一效率跃升源于3DGS抛弃了神经网络采样，采用光栅化渲染管线直接投影高斯椭球到图像平面，避免了沿光线的密集点采样。

### 压缩方法：存储与质量的帕累托前沿

3DGS的显式表示天然面临存储膨胀问题——每个高斯椭球需存储位置、旋转、缩放、不透明度和球谐系数等属性。**Table 2**对比了不同压缩方法在MipNeRF 360数据集上的存储开销与重建质量。核心观察是：矢量量化（VQ）成为主流压缩策略，但不同方法在码本设计和属性分组上存在关键差异。EAGLES采用VQ压缩高斯属性，C3DGS使用残差矢量量化（R-VQ）专门处理几何属性（缩放和旋转），SASCGS则通过敏感性感知的K-Means聚类将颜色和几何属性分别编码到两个码本中。这些方法在存储大小（MB级别）与渲染质量之间形成了明确的帕累托前沿——压缩率越高，PSNR下降越明显，但部分方法通过精细的属性分组策略减缓了这一退化。

![[assets/figures/papers/paper_list_l17_https_sites_cs_ucsb_edu_lingqi_publications/figures/003_Table_2.jpg]]
*Table 2: Comparison of different compression methods on the MipNeRF360 [51] dataset. Size is measured in MB*

### 动态重建：从逐帧优化到时空统一表示

D-NeRF数据集上的对比结果（**Table 3**）揭示了3DGS在动态场景重建中的巨大潜力。原始D-NeRF（NeRF-based）的PSNR仅为31.69，而基于3DGS的方法普遍大幅领先：Deformable3DGS（Yang et al.）达到PSNR 39.51、SSIM 0.990、LPIPS 0.012，SC-GS更是将PSNR推至**43.30**（SSIM 0.997、LPIPS 0.0078），较D-NeRF提升**+11.61**。这一显著差距的因果机制在于：3DGS的显式高斯表示使得变形建模更加直接——Deformable3DGS通过MLP从位置编码后的高斯位置和时间步输出位置、旋转、缩放的偏移量，而SC-GS通过稀疏控制点驱动变形，避免了NeRF中隐式表示对动态建模的间接性。4DGS进一步将3D高斯扩展为4D高斯，在缩放矩阵的对角线上加入时间维度的缩放因子，将时空视为整体进行统一优化。

![[assets/figures/papers/paper_list_l17_https_sites_cs_ucsb_edu_lingqi_publications/figures/007_Table_3.jpg]]
*Table 3: Quantitative comparison of novel view synthesis results on the D-NeRF [66] dataset using PSNR, SSIM and LPIPS metrics*

### SLAM应用：实时性与精度的平衡

在Replica数据集上（**Table 4**），基于3DGS的SLAM方法展示了实时跟踪与高质量视角合成的结合能力。相比传统SLAM方法，3DGS-SLAM系列在PSNR、SSIM和LPIPS上均有竞争力表现，同时保持了实时渲染的优势。关键设计在于：将3DGS的显式地图表示与SLAM的在线优化框架融合，高斯的增删操作天然适配场景扩展和回环检测。

### 失败模式与适用边界

尽管实验结果表明3DGS在效率上具有压倒性优势，但综述明确指出了若干失效场景：

1. **稀疏视图重建**：当输入视图少于4张时，3DGS的优化容易陷入局部最优，高斯椭球无法充分覆盖场景几何。GaussianObject等方法尝试通过引入先验缓解此问题，但重建质量仍显著低于密集视图场景。
2. **几何/表面重建质量**：3DGS的离散椭球表示导致提取的几何表面不平滑，不如传统网格重建方法（如SuGaR虽有改善但仍存在差距）。这是显式点基表示的结构性限制。
3. **复杂着色与大规模场景**：在光照变化剧烈或场景尺度极大的情况下，球谐系数的表达能力受限，且高斯数量的线性增长带来存储和优化压力。
4. **编辑后的重优化需求**：当前的3D编辑操作（几何变形、外观修改）通常需要重新优化场景表示，缺乏独立且高效的一次性编辑方案，限制了交互式应用。

### 证据强度说明

需要指出，本综述的实验数据均来自第三方方法的公开报告，未进行统一的公平性控制实验。不同方法在训练策略、超参数设置和评估协议上可能存在差异，因此跨方法的数值对比应视为参考性结论而非严格的消融验证。各表格中的具体数值（如Table 1中Scaffold-GS的PSNR 28.84）置信度较高（0.98），但方法间细微差异（<0.5 dB）可能需要手动验证其统计显著性。

## 定位与知识库关联

本综述的核心贡献在于**文献分类与知识组织这一“元方法”slot**，而非提出新的重建、编辑或生成算法。相较于单篇研究论文聚焦于某一具体任务的性能突破，本文改变了“方法创新”这一传统slot，转而构建了一个系统性的分类框架（Fig. 1），将3D Gaussian Splatting（3DGS）的现有工作按**三维重建、三维编辑、下游应用**三大板块进行组织，并通过时间线（Fig. 2）梳理了代表性工作的演进脉络。这一slot转换使得该综述成为知识库中的**索引节点**，而非算法改进节点。

### 相对已有综述的差异化定位

在3DGS领域，此前缺乏大规模、系统性的文献综述。已有的NeRF综述（如Tewari et al., 2022）主要覆盖基于神经网络的隐式表示方法，而3DGS作为一种显式高斯椭球表示，其方法谱系、设计选择和性能边界尚未被系统整理。本综述填补了这一空白，其差异化体现在：

1. **以3DGS表示为中心的分类体系**：不同于以“任务”或“应用”为分类维度的通用综述，本文的分类框架以3DGS的表示特性（显式、可光栅化、可编辑）为逻辑起点，将方法按“如何使用和扩展高斯椭球”进行归类，这为后续研究者提供了一种**表示驱动的思维范式**。
2. **跨任务性能基准的汇总**：本文汇总了静态重建（Table 1, MipNeRF 360数据集）、动态重建（Table 3, D-NeRF数据集）、压缩（Table 2）、SLAM（Table 4）等多个子任务的定量结果，形成了3DGS方法的**首个跨任务性能对比基准**，而非仅聚焦于单一任务。

### 知识库挂载点

本综述在知识库中的挂载位置为**3D视觉表示的文献索引层**，具体挂载点包括：

- **上游挂载**：NeRF系列方法（Mildenhall et al., ECCV 2020）作为3DGS的直接前驱，提供了体渲染的理论基础和视角合成任务的评测范式。3DGS保留了NeRF的视角合成目标，但将隐式MLP替换为显式高斯椭球，将体渲染替换为光栅化，从而在保持重建质量的同时实现了训练和渲染速度的数量级提升（训练约30分钟，渲染≥30 FPS）。
- **并行挂载**：基于网格的传统重建方法（如MVS、SfM）和基于点的渲染方法（如EWA Splatting, Zwicker et al., 2001）构成了3DGS的技术渊源。3DGS的投影协方差公式 $\Sigma' = J W \Sigma W^T J^T$ 直接继承了EWA Splatting的数学框架，但引入了可微优化和自适应密度控制。
- **下游挂载**：本综述覆盖的下游任务——SLAM、数字人、3D/4D生成——构成了3DGS的应用拓展空间。这些任务此前主要依赖NeRF或传统方法，3DGS的显式表示和实时渲染能力为它们提供了新的技术基座。

### 适用边界与局限

作为综述，本文的适用边界由其覆盖范围决定：

- **时间边界**：覆盖至2024年初的3DGS相关工作，后续新方法需通过增量更新纳入。
- **方法边界**：聚焦于基于3DGS表示的方法，未深入覆盖NeRF、网格重建、神经场等并行技术路线的最新进展。
- **评测边界**：所汇总的定量结果来自不同论文的独立报告，**未进行统一条件下的复现实验**，因此各方法间的数值对比需谨慎解读——不同方法可能使用了不同的训练策略、超参数或数据预处理，直接比较PSNR/SSIM/LPIPS可能存在公平性问题。这一点在知识库中需标注为“第三方报告结果，未经统一验证”。

### 后续研究的启发价值

本综述揭示的开放问题为知识库中的后续研究提供了明确方向：

1. **重建鲁棒性**：3DGS在稀疏视图、复杂着色、大规模场景下的性能退化，指向了**先验注入**这一改进方向——如何将几何先验、语义先验或多视图一致性约束融入高斯优化过程，是提升鲁棒性的关键。
2. **几何/表面质量**：3DGS的离散高斯表示导致表面重建质量不如传统网格方法（如Fig. 10中SuGaR的结果所示），这催生了**高斯-网格混合表示**的研究方向，如将高斯绑定到网格面片上进行约束。
3. **高效编辑**：当前的3D编辑通常需要重新优化，缺乏一次性、独立的编辑方案。这指向了**解耦表示**的需求——将几何、纹理、光照等属性分离建模，使得编辑某一属性时不影响其他属性。
4. **物理感知生成**：4D内容和物理感知运动的生成仍处于初期阶段（如Fig. 13中AYG的结果），这要求将物理模拟引擎与3DGS生成管道结合，形成**物理约束的生成范式**。
5. **跨平台部署**：3DGS主要依赖PyTorch实现，限制了移动端和Web端的应用。这指向了**轻量化推理引擎**的开发需求，如将光栅化算子移植到Metal/Vulkan/WebGPU等跨平台图形API。

综上，本综述作为3DGS领域的**知识组织节点**，其核心价值不在于提出新的技术方案，而在于为知识库提供了结构化的文献索引、跨任务性能基准和开放问题清单，为后续研究者的方法选型和方向判断提供了系统参考。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2024/A_Dynamic_By_example_BTF_Synthesis_Scheme.pdf]]