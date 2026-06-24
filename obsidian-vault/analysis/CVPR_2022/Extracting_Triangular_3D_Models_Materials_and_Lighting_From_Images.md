---
title: "Extracting Triangular 3D Models, Materials, and Lighting From Images"
type: paper
paper_level: A
venue: CVPR
year: 2022
pdf_ref: paperPDFs/CVPR_2022/Extracting_Triangular_3D_Models_Materials_and_Lighting_From_Images.pdf
aliases:
- DBJODSSL
- ET3MMLFI
tags:
- CVPR_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将DMTet扩展至2D监督实现端到端可微的显式网格重建，并提出可微分split sum近似实现全频率环境光照联合优化，使拓扑、材质与光照可同时学习。"
primary_logic: "在可变拓扑网格上利用MLP体积纹理缓变保证材质连续性，结合可微分split sum预过滤快速估算高频镜面反射，从而生成与游戏引擎兼容的PBR三角网格资产。"
claims:
- "在NeRFactor合成数据集上重光照PSNR优于NeRFactor（24.53 vs 23.78），且albedo纹理SSIM更高（0.924 vs 0.917）。"
- "在NeRF合成数据集上视角插值PSNR为29.05，与NeRF相当，但能输出可编辑的因子化网格。"
- "网格提取质量（53k三角形）在Chamfer L1仅为4.65×10⁻⁴，远优于NeRF（33.4×10⁻⁴）和NeuS（9.19×10⁻⁴），甚至逼近高三角数NeuS。"
- "可微分split sum与128个球面高斯相比训练速度快5倍，且更准确捕捉高频环境光照。"
---

# Extracting Triangular 3D Models, Materials, and Lighting From Images

> [!tip] 核心洞察
> 在可变拓扑网格上利用MLP体积纹理缓变保证材质连续性，结合可微分split sum预过滤快速估算高频镜面反射，从而生成与游戏引擎兼容的PBR三角网格资产。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 从图像中提取三角三维模型、材质与光照 |
| 英文题名 | Extracting Triangular 3D Models, Materials, and Lighting From Images |
| 会议/期刊 | CVPR 2022 |
| Links | [paper](https://arxiv.org/abs/2111.12503); [Project](https://nvlabs.github.io/nvdiffrec/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DMTet-based joint optimization with differentiable split sum lighting |
| Dataset | NeRFactor synthetic dataset, NeRF realistic synthetic dataset, NeRFactor variant of NeRF synthetic, DTU MVS dataset (scan65/106/118) |

> [!tip] 效果简介
> - NeRFactor synthetic dataset 上，PSNR↑/SSIM↑/LPIPS↓ (relighting avg) 为 24.53 / 0.914 / 0.085，对比 23.78 / 0.907 / 0.112 (NeRFactor)，变化 +0.75 / +0.007 / -0.027。
> - NeRF realistic synthetic dataset 上，PSNR↑ (view interpolation avg) 为 29.05，对比 31.00 (NeRF)，变化 -1.95。
> - NeRFactor variant of NeRF synthetic 上，PSNR↑ (view interpolation avg) 为 31.65，对比 26.87 (NeRFactor)，变化 +4.78。

## 概述

从多视角图像中重建三维物体是计算机视觉与图形学的长期目标。传统摄影测量流程依赖多阶段分离优化（相机标定、多视图立体、网格提取、材质烘焙），各阶段误差累积导致最终资产质量下降。近年来，以 **NeRF** 为代表的神经辐射场方法在视角合成上取得了突破性进展，但其输出的体积表示无法直接编辑，提取出的显式网格几何质量显著退化（Chamfer距离高达33.4×10⁻⁴），且材质与光照的分解不充分。神经隐式表面方法（如 **NeuS**）虽改善了网格提取质量，但仍需后处理Marching Cubes，且同样缺乏对PBR材质和全频率光照的联合建模。

本文的核心贡献在于提出了一套端到端可微的框架，首次将可变拓扑的显式三角网格生成、空间变化PBR材质与全频率HDR环境光照纳入统一的2D图像监督优化中。方法的关键洞察是：**将Deep Marching Tetrahedra（DMTet）扩展至2D监督，并结合可微分split sum近似，使拓扑结构、材质参数与光照可同时学习**。具体而言，利用可变形四面体网格的可微Marching Tetrahedra层直接生成三角网格，避免了隐式表示的后处理提取；通过在世界空间索引的体积纹理MLP保证拓扑变化时的材质连续性，并在拓扑收敛后重参数化至2D纹理以消除接缝；提出可微分split sum光照模型，利用预过滤环境贴图和预积分BSDF查找表高效估算全频率镜面反射，训练速度较128个球面高斯快5倍。

实验表明，该方法在NeRFactor合成数据集上的重光照PSNR达到24.53 dB，优于NeRFactor的23.78 dB，且反照率纹理SSIM更高（0.924 vs 0.917）。在NeRF合成数据集上，视角插值PSNR为29.05 dB，与NeRF相当，但额外输出可直接编辑的因子化网格。网格提取质量方面，仅53k三角形的Chamfer L1距离为4.65×10⁻⁴，远优于NeRF（33.4×10⁻⁴）和NeuS（9.19×10⁻⁴），甚至逼近90万三角形的NeuS（5.84×10⁻⁴）。重建模型可直接导入Blender等标准图形工具进行重打光、场景编辑和软体仿真，展示了与传统图形管线的无缝兼容。训练约需1小时（单V100 GPU），推理时间达毫秒级，显著快于需要数天的NeRD和NeRFactor等方法。

该方法的主要局限在于假设物体不透明，无法处理半透明或折射材质；训练时仅使用直接光照，在强阴影区域的材质分解质量下降；需要预先提供前景分割掩模；在光照不一致或视角稀疏的数据集上几何重建性能不如专用神经隐式方法。尽管如此，该工作为从图像到游戏引擎兼容PBR资产的端到端重建提供了重要的技术路径。

## 背景与动机

三维内容创作是计算机图形学与视觉的核心任务，广泛应用于影视、游戏和虚拟现实等领域。传统资产制作依赖专业艺术家手工建模、绘制纹理和设置光照，成本高昂且周期漫长。从多视角图像自动重建高质量三维模型因此成为长期追求的目标。

### 现有方法的瓶颈

当前主流的图像到三维重建方法大致分为两类，各自存在根本性缺陷。

**传统摄影测量流程**采用多阶段分离优化：先通过运动恢复结构估计相机位姿，再通过多视角立体匹配生成密集点云，随后进行表面重建、网格化、纹理映射和材质估计。这种级联式流水线中，各阶段的误差会逐步累积放大，且缺乏端到端的反馈机制，难以在全局层面协调几何、材质与光照的一致性。

**神经隐式表示方法**（如 NeRF、NeuS）将场景编码为连续函数，通过体积渲染实现高质量视角合成。然而，这些方法输出的是隐式场而非可编辑的显式网格。要从隐式场中提取三角网格，通常需要后处理步骤（如 Marching Cubes），提取出的网格几何质量显著下降——Chamfer L1 距离往往比本方法高出数倍至一个数量级（Figure 3）。更重要的是，现有神经方法对材质和光照的分解不充分：NeRFactor 等因子化方法虽然支持重光照，但其材质分离质量有限，且输出仍为神经网络而非标准 PBR 资产，无法直接导入游戏引擎或建模软件进行编辑。

**光照建模的局限**进一步加剧了这一问题。现有逆渲染方法（如 NeRD、PhySG）多采用球面高斯等低频表示来近似环境光照，无法准确捕捉高频光照细节（如锐利阴影、镜面高光）。而 NeRFactor 虽使用低分辨率环境贴图，同样受限于光照表达能力的不足。

### 核心动机

本文的核心动机在于弥合神经渲染的质量优势与传统图形管线的实用性需求之间的鸿沟。具体而言，我们希望实现一个端到端的可微框架，能够从多视角图像直接输出**可直接编辑的 PBR 三角网格资产**——包含显式拓扑、空间变化材质（基础色、粗糙度、金属度）以及全频率 HDR 环境光照，且该资产与 Blender、游戏引擎等标准工具完全兼容（Figure 1、Figure 8）。

这一目标面临三个关键技术挑战：

1. **可变拓扑几何的可微优化**：如何在仅给定 2D 图像监督的条件下，端到端地学习未知拓扑的三角网格，而非依赖后处理提取。
2. **材质连续性与拓扑变化的协调**：当网格拓扑在训练中动态变化时，如何保证材质参数的空间连续性，避免纹理断裂。
3. **全频率光照的高效可微建模**：如何以可接受的计算代价，实现对高频环境光照的准确建模和梯度反向传播。

本文正是围绕这三个挑战展开，通过扩展 DMTet 至 2D 监督、引入体积纹理 MLP 以及提出可微分 split sum 光照近似，构建了一个统一的逆渲染框架，使得拓扑、材质与光照能够从图像中联合学习。

## 核心创新

本文的核心贡献在于将可变形四面体网格（DMTet）从3D监督拓展至**端到端2D图像监督**，并引入**可微分split sum光照近似**，从而首次实现了拓扑、材质、光照在统一框架下的联合优化，直接输出与游戏引擎无缝兼容的PBR三角网格资产。相较于现有方法，其关键创新体现在四个维度的机制性改变：

### 1. 几何表示：从隐式后处理提取到可微显式网格生成

传统方法（NeRF、NeuS）依赖神经隐式场（密度场或SDF），网格需通过Marching Cubes后处理提取，导致几何质量显著下降（Figure 3）。本文直接采用**DMTet**作为几何表示：在可变形的四面体网格上定义离散SDF值和顶点偏移，通过可微Marching Tetrahedra层在训练过程中动态生成三角网格。这一设计使拓扑变化（如孔洞合并、表面分裂）直接受2D渲染损失驱动，无需3D真值监督。

关键机制在于**SDF符号翻转正则化**（公式2）：惩罚四面体边上的SDF符号不一致，有效抑制内部浮空几何。消融实验（Figure 28）表明，该正则化比传统平滑正则化更彻底地清除杂乱面片，产生更干净的表面。

### 2. 光照模型：从低频球面高斯到全频率可微split sum

现有因子化方法（NeRFactor、PhySG、NeRD）普遍采用球面高斯或低分辨率环境贴图近似光照，仅能捕获低频反射，无法准确再现镜面高光细节。本文提出**可微分split sum近似**，将渲染方程（公式3）的入射辐射度积分分解为两项可预计算的独立积分（公式5）：
- **BSDF预积分项**：离线构建2D查找表，索引为粗糙度和入射角
- **预过滤环境贴图项**：对HDR立方体贴图进行多级mipmap预过滤，查询时根据粗糙度选择合适mip

这一分解使得全频率环境光照的高效估算成为可能，且整个计算图保持可微。**Figure 11**显示，split sum在捕捉高频光照细节上显著优于128个球面高斯，且训练速度提升**5倍**。

### 3. 纹理策略：从拓扑依赖的2D参数化到体积纹理MLP

固定拓扑后生成UV参数化的传统策略在拓扑剧烈变化时会产生纹理不连续。本文采用**体积纹理MLP**：使用hash grid与位置编码将世界坐标映射为PBR材质参数（基础色、粗糙度、金属度、法线扰动），在拓扑演变过程中保持材质连续性。拓扑收敛后，通过xatlas生成UV坐标，将MLP采样到2D纹理并继续微调，自动消除UV接缝（Figure 6）。

### 4. 训练范式：从分离优化到端到端联合学习

传统摄影测量流程将几何重建、材质估计、光照估计分离为多阶段优化，误差逐级累积。本文将所有可学习参数（SDF值、顶点偏移、材质MLP权重、环境贴图像素）统一纳入**经验风险最小化框架**（公式1），通过可微光栅化与延迟着色反向传播梯度。损失函数由色调映射后的L1图像损失、掩模L2损失和正则化项组成，实现从2D图像到3D PBR资产的端到端学习。

### 创新点的协同效应

上述四个创新并非孤立改进，而是形成**因果闭环**：DMTet提供可变拓扑的显式网格，使可微渲染器能计算精确的表面法线和遮挡关系；体积纹理MLP保证拓扑变化时材质连续，避免拓扑更新后纹理断裂；可微split sum以较低计算成本提供全频率光照梯度，驱动材质与几何的精细优化。三者协同使得最终输出可直接导入Blender等建模工具进行重打光、软体仿真和场景编辑（Figure 8），这是神经隐式方法无法实现的。

> **注意**：本文未提供与同期工作Neural-PIL的定量对比，split sum相较于路径追踪的精度损失也缺乏系统评估，该部分需结合具体应用场景手动验证。

## 整体框架

本文提出一个端到端可微的逆向渲染管线，从一组已知相机位姿和前景掩模的多视图图像出发，联合优化三角网格的**拓扑**、**空间变化材质**和**HDR环境光照**，最终输出可直接导入游戏引擎的PBR三角网格资产。图2展示了完整流程。

**输入与输出**。输入为多视图RGB图像、对应前景掩模及标定相机。输出包含：(1) 可变拓扑的三角网格；(2) 2D PBR纹理贴图（基础色、粗糙度、金属度、法线扰动）；(3) HDR立方体贴图形式的环境光照。

**核心优化目标**。整个管线以图像空间损失最小化为统一目标：

$$ \underset{\phi}{\mathrm{argmin}}\ \mathbb{E}_{c}\big[L\big(I_{\phi}(c), I_{\mathrm{ref}}(c)\big)\big] \tag{1} $$

其中 $\phi$ 囊括所有可优化参数——SDF值、顶点偏移、材质MLP权重、环境光照强度，$c$ 为相机位姿。总损失函数由色调映射后的L1图像损失、平方L2掩模损失和正则化项加权组成。

**五大模块协同**。管线由五个核心模块串联构成，梯度通过可微渲染自图像损失反向传播至所有参数：

1. **DMTet几何生成**（Section 3.1）：在可变形的四面体网格上定义离散SDF值和顶点偏移，通过可微Marching Tetrahedra层实时提取三角网格。网格拓扑随SDF符号变化而动态演化，无需预设拓扑。同时施加SDF符号翻转正则化（式2）以抑制内部浮空面片。

2. **体积纹理MLP**（Section 3.2）：在世界空间通过哈希网格和位置编码的MLP将任意表面点映射为PBR材质参数（基础色 $k_d$、粗糙度 $r$、金属度 $m$、法线扰动）。拓扑剧烈变化时，体积表示保证材质连续性，避免拓扑变化导致的纹理断裂。

3. **可微光栅化与延迟着色**（Section 3, Figure 2）：使用可微光栅化器渲染网格图像，在延迟着色阶段计算每个像素的PBR着色，输出色调映射后的图像，并与参考图像计算损失，梯度反向传播至几何、材质和光照参数。

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2111_12503/figures/003_Figure_2.jpg]]
*Figure 2: Overview of our approach. We learn topology, materials, and environment map lighting jointly from 2D supervision. We leverage differentiable marching tetrahedrons to directly optimize topology of a triangle mesh. While the topology is drastically changing, we learn materials through volumetric texturing, efficiently encoded using an MLP with positional encoding. Finally, we introduce a differentiable version of the split sum approximation for environment lighting. Our output representation is a triangle mesh with spatially varying 2D textures and a high dynamic range environment map, which can be used unmodified in standard game engines. The system is trained end-to-end, supervised by loss...*

4. **可微Split Sum光照**（Section 3.3, Algorithm 1）：将渲染方程中的环境光照积分分解为可预计算的BSDF项和预过滤环境贴图项（式5），高效近似全频率环境光照。HDR立方体贴图在训练中联合优化，预过滤操作通过自定义CUDA核实现可微。

5. **2D纹理重参数化**（Section 3.2, Figure 6）：拓扑收敛后，使用xatlas生成UV坐标，将MLP采样到2D纹理上，随后固定拓扑继续微调，自动消除UV接缝，最终输出标准PBR纹理贴图。

**训练流程**。训练分为两阶段：第一阶段同时优化拓扑、体积纹理MLP和环境光照，拓扑自由演化；第二阶段拓扑固定后，将体积纹理烘焙至2D纹理并微调，消除接缝并提升细节。单张V100 GPU训练约需1小时，推理时间达毫秒级。

## 核心模块与公式推导

### 问题形式化

方法将所有可优化参数统一在经验风险最小化框架下。令 $\phi$ 表示全部可学习参数（SDF 值、顶点偏移、材质参数、环境光照），相机位姿 $c$ 采样自已知分布，渲染图像 $I_{\phi}(c)$ 与参考图像 $I_{\mathrm{ref}}(c)$ 之间的损失函数期望构成优化目标：

$$\underset{\phi}{\mathrm{argmin}}\ \mathbb{E}_{c}\big[L\big(I_{\phi}(c),I_{\mathrm{ref}}(c)\big)\big] \tag{1}$$

总损失由三项加权构成：

$$L = L_{\mathrm{image}} + L_{\mathrm{mask}} + \lambda L_{\mathrm{reg}}$$

其中 $L_{\mathrm{image}}$ 为色调映射后颜色的 L1 损失，$L_{\mathrm{mask}}$ 为前景掩模的平方 L2 损失，$L_{\mathrm{reg}}$ 为正则化项。梯度通过可微光栅化反向传播至所有模块，实现端到端联合优化。

### 可微拓扑学习：DMTet 与 SDF 正则化

几何表示采用可变形四面体网格上的离散 SDF。每个四面体网格顶点 $v_i$ 携带 SDF 值 $s_i$ 和可学习的偏移量 $\Delta v_i$，变形后的顶点位置为 $v_i' = v_i + \Delta v_i$。可微 Marching Tetrahedra 层在每条边上检测 SDF 符号变化（$\operatorname{sign}(s_i) \neq \operatorname{sign}(s_j)$），线性插值生成三角面片顶点 $v_{ij}$，从而在训练过程中动态改变拓扑。

为抑制内部浮空几何与杂乱面片，引入 SDF 符号翻转正则化：

$$L_{\mathrm{reg}} = \sum_{i,j \in \mathbb{S}_e} H\big(\sigma(s_i), \operatorname{sign}(s_j)\big) + H\big(\sigma(s_j), \operatorname{sign}(s_i)\big) \tag{2}$$

其中 $\mathbb{S}_e$ 为四面体网格边集合，$H$ 为二元交叉熵，$\sigma$ 为 sigmoid 函数。该正则化惩罚边上 SDF 符号不一致的情况，鼓励表面两侧符号统一。消融实验（Figure 28）表明，该正则化比传统平滑正则化更有效地去除内部杂乱面片，产生更干净的几何。

### 体积纹理与 PBR 材质模型

材质遵循标准 PBR 模型（Figure 5），包含漫反射与 GGX 微面元镜面反射两个分量。漫反射分量由基础色 $\mathbf{k}_d$（四通道纹理）描述；镜面反射分量由粗糙度 $r$（控制 GGX 法线分布函数宽度）和金属度 $m$（控制 Fresnel 项中基础色与镜面色混合）参数化。法线通过扰动基础网格法线获得。

材质参数由体积纹理 MLP 在世界空间连续索引，输入为位置编码后的三维坐标，输出为 $(\mathbf{k}_d, r, m, \mathbf{n})$。此设计在拓扑剧烈变化时保持材质空间连续性，避免传统 2D UV 参数化在拓扑改变时产生的纹理不连续。当拓扑收敛后，使用 xatlas 生成 UV 坐标，将 MLP 采样到 2D 纹理并继续微调，自动消除 UV 接缝（Figure 6）。

### 可微 Split Sum 光照近似

出射辐射度由标准渲染方程给出：

$$L(\omega_o) = \int_{\Omega} L_i(\omega_i) f(\omega_i,\omega_o) (\omega_i \cdot \mathbf{n}) d\omega_i \tag{3}$$

其中 $f(\omega_i,\omega_o)$ 为 Cook-Torrance 微面元 BSDF，采用 GGX 法线分布：

$$f(\omega_i,\omega_o) = \frac{D G F}{4(\omega_o \cdot \mathbf{n})(\omega_i \cdot \mathbf{n})} \tag{4}$$

$D$ 为 GGX 分布，$G$ 为几何衰减项，$F$ 为 Schlick Fresnel 项。

为实现全频率环境光照的高效可微计算，采用 split sum 近似将积分分解为两项之积：

$$L(\omega_o) \approx \int_{\Omega} f(\omega_i,\omega_o)(\omega_i \cdot \mathbf{n})d\omega_i \cdot \int_{\Omega} L_i(\omega_i) D(\omega_i,\omega_o)(\omega_i \cdot \mathbf{n})d\omega_i \tag{5}$$

第一项仅依赖 BSDF 参数（粗糙度、$\omega_o \cdot \mathbf{n}$），可预计算为 2D 查找表；第二项为入射辐射度与 GGX 分布的卷积，通过对 HDR 立方体贴图逐粗糙度级别预过滤实现。渲染时仅需两次纹理查询，梯度可流畅通过查找表和预过滤贴图反向传播。与 128 个球面高斯拟合相比，split sum 训练速度提升约 5 倍，且更准确捕捉高频环境光照细节（Figure 11）。

### 渐进式位置编码

对于光照不一致或视角稀疏的数据（如 DTU），采用渐进式位置编码掩码以平滑表面并减少伪影：

$$\alpha_{n}(t) = \begin{cases} 1 & n \leq n_{\mathrm{base}} \\ \min(1, \frac{t}{t_f}) & n > n_{\mathrm{base}} \end{cases} \tag{6}$$

其中 $n$ 为频率带索引，$t$ 为训练迭代步数，$t_f$ 为完全开启步数。低频带始终激活，高频带在训练中逐步引入，使模型先学习平滑几何再添加细节。消融实验（Figure 26, 27）表明，MLP 参数化配合渐进式编码在稀疏视图下优于直接优化每顶点 SDF 值。

## 实验与分析

### 端到端因子化重建的核心性能

本方法在三个关键维度上同时实现了可编辑网格输出与因子化分解，而无需在视角合成质量上付出显著代价。

**重光照与材质分解质量。** 在NeRFactor合成数据集上，本方法的重光照PSNR达到24.53 dB，优于专门设计的因子化方法**NeRFactor**的23.78 dB（+0.75 dB），SSIM从0.907提升至0.914，LPIPS从0.112降至0.085（Table 2）。更重要的是，反照率纹理的SSIM达到0.924，超过NeRFactor的0.917，表明材质分解更准确。图7的定性对比显示，本方法重建的模型可直接导入Blender进行重光照，而NeRFactor的公开代码生成结果存在明显的镜面反射伪影。

**视角合成质量。** 在NeRF真实合成数据集上，本方法视角插值PSNR为29.05 dB，略低于**NeRF**的31.00 dB（-1.95 dB），但高于**PhySG**的26.79 dB和**NeRD**的23.80 dB（Table 3）。这一差距是可接受的代价——NeRF仅输出体积密度，无法直接编辑；而本方法在保持接近NeRF的视觉质量的同时，额外提供了可直接编辑的三角网格与完整的PBR材质分解。在NeRFactor版本的同一数据集上，本方法PSNR达到31.65 dB，显著优于NeRFactor的26.87 dB（+4.78 dB，Table 4）。

**网格提取质量。** 这是本方法最显著的突破。在256张渲染图像的网格提取实验中（Figure 3），本方法仅用53k三角形即达到Chamfer L1损失4.65×10⁻⁴，远优于**NeRF**的33.4×10⁻⁴（Marching Cubes提取）和**NeuS**的9.19×10⁻⁴。值得注意的是，NeuS需要900k三角形才能达到5.84×10⁻⁴的Chamfer损失，而本方法以约17倍的三角形效率实现了更优的几何精度。在DTU MVS数据集的scan65/106/118上，本方法的Chamfer距离分别为1.03/1.07/0.69，全面优于NeRF的1.44/1.44/1.13（Table 9）。

### 可微分Split Sum光照的关键作用

可微分split sum近似是本方法实现全频率环境光照联合优化的关键技术决策。图11的对比揭示了两项关键优势：

1. **速度优势**：split sum的训练速度是128个球面高斯近似的5倍，因为后者需要在每个着色点评估大量球面高斯基函数，而split sum利用预过滤的HDR立方体贴图和预积分BSDF查找表，将运行时着色简化为两次纹理查询。
2. **高频捕捉能力**：球面高斯近似仅能捕捉低频环境光照，在高频细节（如太阳光斑、锐利阴影边缘）处产生模糊；split sum通过mipmap预过滤在不同粗糙度级别上准确保留了高频光照信息，使镜面反射更锐利逼真。

### 消融实验的关键发现

**SDF正则化对几何质量的决定性影响。** 图28的截面图消融实验表明，不使用任何正则化时，四面体网格内部会产生大量杂乱面片（浮空几何）；使用Liao等人的平滑正则化虽能部分抑制，但表面仍残留内部碎片；本方法提出的符号翻转正则化（式2）通过惩罚四面体边上的SDF符号变化，直接消除了内部浮空几何，产生最干净的表面。这一正则化是端到端2D监督成功的关键——没有3D监督信号时，渲染损失对内部不可见面片的梯度为零，必须通过显式正则化来抑制。

**SDF参数化策略的场景依赖性。** 在密集视图、恒定光照的合成数据上，直接优化每顶点SDF值（网格参数化）比MLP参数化更能捕捉高频几何细节（Figure 27）；但在DTU等稀疏视图或光照变化的数据上，MLP参数化配合渐进式位置编码（式6）能有效平滑表面，减少伪影（Figure 26）。这一发现揭示了显式网格优化中的一个核心权衡：网格参数化提供更强的表达能力，但需要更密集的监督信号来约束。

**纹理重参数化的接缝消除。** 拓扑收敛后将体积纹理MLP采样到2D纹理时，UV参数化会在接缝处产生不连续（Figure 6左）。然而，在固定拓扑下继续优化2D纹理，接缝会迅速自动消除（Figure 6右）。这表明MLP提供的初始纹理在全局上是连续的，接缝仅由UV展开引入，可通过局部优化快速修复。

**掩模鲁棒性。** 使用自动分割产生的劣质掩模（如扩张/腐蚀操作模拟的噪声掩模）仍可获得合理重建，重建质量随掩模噪声增大而平缓下降（Figure 23、24）。系统对掩模错误的鲁棒性来源于两方面：掩模损失仅监督轮廓，而图像损失提供密集的像素级梯度；SDF正则化防止了因掩模错误导致的拓扑崩溃。

### 失败模式与边界条件

尽管本方法在多个基准上表现优异，但存在明确的失败边界：

1. **半透明与折射材质**：本方法假设物体不透明，使用单一BSDF层。对于Drums、Ship等包含玻璃或半透明材质的场景，重建完全失败。这是渲染模型的结构性限制，而非优化问题。

2. **强阴影与颜色渗漏**：训练时仅计算直接光照（忽略全局光照和阴影），在强阴影或颜色渗漏区域，优化器会将阴影错误地烘焙到反照率纹理中，导致材质分解质量下降。图8的Cornell盒实验展示了这一限制的例外——当重建模型被放入支持全局光照的渲染器时，可正确交互并投射阴影，但训练阶段本身无法处理这些效应。

3. **稀疏视图与光照不一致**：在DTU数据集上，本方法的几何重建性能不如专用神经隐式方法**NeuS**和**IDR**（Table 9中scan65的1.03 vs NeuS的0.73）。这是因为DTU场景存在光照变化和稀疏视角，DMTet的显式网格在缺乏密集监督时难以恢复精细表面细节，而神经隐式方法的连续隐式场天然具有平滑先验。

4. **计算成本**：训练约需1小时（单V100），虽然显著快于**NeRD**和**NeRFactor**（数天），但仍远慢于**NeRF**（分钟级）。推理阶段为毫秒级，适合实时应用。

### 与传统图形管线的兼容性验证

本方法输出的PBR三角网格资产可直接导入标准图形工具链，这是区别于所有神经隐式方法的核心实用价值。图8展示了两个重建模型被插入Cornell盒的场景：物体准确响应场景光照、投射阴影，并与地面产生正确的反射交互。图12进一步展示了自动LOD生成——通过标准网格简化工具即可从重建的高精度网格生成多级细节层次，无需重新训练。这种兼容性使得本方法的输出可直接用于游戏引擎、电影渲染和物理仿真等实际生产流程。

### 补充图表

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2111_12503/figures/004_Figure.jpg]]
*Figure: Reference Chamfer L1 ×10−4 L _ { 1 }*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2111_12503/figures/012_Figure.jpg]]

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2111_12503/figures/027_Table_6.jpg]]
*Table 6: Image quality metrics for the NeRF realistic synthetic dataset. Each training set consists of 100 images with masks and known camera poses, and the reported image metrics are the arithmetic mean over the 200 images in the test set. Results for NeRF are based on Table 4 of the original paper [45], with new measurements for PhySG and MipNeRF using their respective publicly available source code. We additionally report FLIP mean scores [3]. Note that the Hotdog outlier LPIPS score for NeRF is consistent with the original paper, but probably a bug*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2111_12503/figures/028_Table_7.jpg]]
*Table 7: View interpolation results for the four scenes of NeR-Factor’s synthetic dataset. The NeRF column shows the baseline NeRF trained as part of NeRFactor’s setup, and is different from the NeRF in our other view interpolation results. Each training set consists of 100 images with masks and known camera poses, and the reported image metrics are the arithmetic mean over the eight images in the test set*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2111_12503/figures/031_Figure.jpg]]

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2111_12503/figures/033_Figure.jpg]]

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2111_12503/figures/035_Figure_24.jpg]]
*Figure 24: To evaluate the impact of corrupted masks, we warp perfect masks by texture-mapping them on a grid, displacing each of the 25 × 25 vertices by zero-mean Gaussian noise with increasing standard deviation, σ. From top to bottom, we show a warped texture (to give a sense of the magnitude of corruption), the corrupted masks with the reference mask shown in red, and our reconstruction. The training set consists of 200 images, and PSNR↑ scores are computed as the arithmetic mean of 50 validation images. The ‘uncorrelated‘ series, U, are generated with unique random numbers for each frame, while in the “correlated” scores, C, we corrupt all masks using the same random seed, simulating a segmentati...*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2111_12503/figures/037_Figure.jpg]]
*Figure: korm normals*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2111_12503/figures/032_Figure_22.jpg]]
*Figure 22: Examples of masking errors for the Mold Gold Cape dataset. Note the inconsistencies in classifying the plastic mount as both part of the object and background*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2111_12503/figures/034_Figure_20.jpg]]
*Figure 20: Extracted mesh quality visualization examples on the synthetic KNOB and CERBERUS datasets*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2111_12503/figures/038_Figure_26.jpg]]
*Figure 26: Comparing grid vs. MLP parametrizations of DMTet on scan 65 from the DTU MVS dataset [28]. Directly optimizing SDF values at grid vertices leads to a surface with high-frequency noise (left). In contrast, if we use an MLP to parametrize the SDF values, we can regularize the geometry, with smoothness controlled by the frequency of positional encoding. We use the positional encoding in NeRF [45] with frequency set to 4 (middle) and 6 (right) respectively. Grid*

## 方法谱系与知识库定位

### 1. 问题定位：从隐式重建到可编辑资产生成的瓶颈

传统多视图三维重建与材质获取流程存在两个核心断层。其一，经典摄影测量管线将几何重建、纹理贴图、材质估计与光照估计分离为多个串行阶段，各阶段的误差在后续不可纠正地累积，最终资产质量难以保证。其二，以 **NeRF**（Mildenhall et al., ECCV 2020）为代表的神经辐射场方法虽然在视角合成质量上取得突破，但其输出的体积密度场无法直接编辑，必须经由Marching Cubes等后处理步骤提取网格——这一离线提取过程不仅引入几何退化，更丢失了材质与光照的因子化信息。

后续工作试图弥合这一鸿沟。**NeuS**（Wang et al., NeurIPS 2021）通过将SDF引入体渲染实现了更精确的表面重建，但其输出仍为隐式SDF，网格提取后几何质量显著下降（如Figure 3所示，50k三角形级别的Chamfer L1为9.19×10⁻⁴，远高于本方法的4.65×10⁻⁴）。**NeRFactor**（Zhang et al., SIGGRAPH Asia 2021）率先实现了神经辐射场的因子化分解，可输出反照率、法线和环境光照，但其光照模型受限于低分辨率环境贴图，仅能处理低频光照，且几何表示仍为体积密度场，无法直接导出编辑友好的三角网格。**PhySG**（Zhang et al., ICCV 2021）引入球面高斯表示环境光照，但球面高斯本质上仅能捕获低频光照成分，对高频镜面反射的建模能力不足。**NeRD**（Boss et al., ICCV 2021）和**NeRFactor**的训练时间长达数天，严重制约了实用部署。

本方法在方法谱系中的定位清晰：它处于神经隐式重建与经典图形管线之间的关键接口，目标是**端到端地从2D图像直接生成与游戏引擎和DCC工具无缝兼容的PBR三角网格资产**。这一目标要求同时解决三个子问题——可变拓扑的显式几何、因子化的材质分解、全频率环境光照估计——且三者必须在统一的梯度回传框架下联合优化，这正是本方法的核心贡献。

### 2. 关键技术路线对比

| 维度 | NeRF / NeuS | NeRFactor / PhySG | 本方法 |
|------|-------------|-------------------|--------|
| 几何表示 | 隐式密度/SDF，需后处理提取网格 | 隐式密度场，网格提取后质量退化 | 可变形四面体网格，训练中直接生成三角网格 |
| 拓扑可变性 | 固定拓扑（Marching Cubes后处理） | 固定拓扑（后处理） | 训练中可变拓扑（可微Marching Tetrahedra） |
| 材质模型 | 无因子化 | 因子化但光照低频 | 完整PBR（基础色、粗糙度、金属度、法线） |
| 光照模型 | 无显式光照 | 球面高斯/低分辨率环境贴图 | 可微split sum，支持全频率HDR环境光照 |
| 训练监督 | 2D图像 | 2D图像 | 2D图像，端到端梯度回传至所有参数 |
| 输出格式 | 体积密度/SDF → 网格（离线） | 因子化体积 → 网格（离线） | 三角网格 + 2D PBR纹理 + HDR环境贴图 |
| 训练时间 | ~小时（NeRF分钟级） | 数天 | ~1小时（单V100） |
| 推理时间 | 秒级（体渲染） | 秒级 | 毫秒级（光栅化） |

### 3. 方法适用边界

**适用场景**：
- 静态不透明物体的多视图重建，已知相机位姿和前景掩模
- 需要输出可直接编辑、可重光照、可物理仿真的PBR网格资产的场景
- 对推理速度有实时或近实时要求的应用（如游戏资产预览、虚拟拍摄）
- 密集视图（~100-256张）且光照条件相对一致的拍摄条件

**不适用或性能受限的场景**：
- 半透明或折射材质（如玻璃、烟雾），因渲染模型仅支持不透明表面
- 强阴影或颜色渗漏区域，因训练忽略全局光照和间接光照
- 光照不一致或视角稀疏的数据集（如DTU），几何重建质量不如专用神经隐式方法（**NeuS**、**IDR**（Yariv et al., NeurIPS 2020））
- 动态场景或多物体复杂交互，当前框架假设静态单一物体
- 无前景掩模的开放场景，需额外分割步骤

### 4. 核心局限与开放问题

**已确认的局限**（来自论文明确声明与消融实验）：

1. **材质模型限制**：假设所有表面不透明，不处理透射、次表面散射和折射。在NeRF合成数据集的Drums和Ship场景中重建失败，因为这些场景包含玻璃和半透明材质。

2. **光照模型简化**：训练时仅使用直接光照，忽略间接光照和阴影。在强阴影区域（如物体底部接触面），材质分解质量下降，反照率估计可能混入阴影信息。

3. **掩模依赖**：需要预先提供前景分割掩模。消融实验（Figure 23, 24）表明，使用自动分割的劣质掩模仍可获得合理重建，质量随掩模噪声增大而平缓下降，系统对掩模错误具有一定鲁棒性，但极端错误仍会导致几何缺失或溢出。

4. **几何重建精度上限**：在DTU等稀疏视图、光照变化的数据集上，几何重建的Chamfer距离虽优于NeRF，但不如**NeuS**和**IDR**等专用神经隐式方法。这是因为DMTet的四面体网格分辨率限制了可表示的几何细节频率。

5. **训练效率**：单V100约需1小时，虽显著快于NeRD/NeRFactor（数天），但仍远慢于NeRF（分钟级），限制了快速迭代实验。

6. **相机位姿假设**：需要已知精确的相机位姿，无法处理未知位姿或运动模糊的输入。

**开放问题**（论文中明确提及或从方法局限自然延伸）：

1. **可微全局光照**：能否将可微分split sum扩展为可微分路径追踪器，以支持全局光照（间接漫反射、焦散等），从而从根本上改善强阴影和颜色渗漏区域的材质分解质量？这需要解决路径追踪的梯度估计方差和计算开销问题。

2. **无掩模重建**：如何去除对前景掩模的依赖，实现自动分割与重建的联合优化？可能的路径包括引入背景模型或利用语义先验。

3. **动态场景拓展**：如何将框架拓展到动态场景或多物体复杂交互？这涉及时变拓扑建模和物体间遮挡关系的处理。

4. **透射材质支持**：能否通过改进渲染模型（如加入BTDF/BSDF混合）来处理半透明和折射材质？这需要可微的折射光线追踪支持。

5. **自动LOD与实时应用**：在极低三角形数或移动端实时应用中，如何自动选择最佳LOD并保持视觉质量？论文展示了手动LOD生成（Figure 12），但自适应LOD选择仍为开放问题。

6. **神经特征场融合**：能否与神经特征场结合，在保持显式网格优势的同时提升几何细节？例如，用网格作为低频几何代理，用神经特征补偿高频细节。

7. **多物体场景分解**：当前框架假设单一前景物体，如何扩展到包含多个物体的完整场景，实现实例级重建与分解？

## 原文 PDF

![[paperPDFs/CVPR_2022/Extracting_Triangular_3D_Models_Materials_and_Lighting_From_Images.pdf]]
