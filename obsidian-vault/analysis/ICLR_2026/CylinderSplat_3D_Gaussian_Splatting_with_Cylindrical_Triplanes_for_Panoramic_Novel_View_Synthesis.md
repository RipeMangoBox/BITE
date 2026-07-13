---
title: "CylinderSplat: 3D Gaussian Splatting with Cylindrical Triplanes for Panoramic Novel View Synthesis"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/CylinderSplat_3D_Gaussian_Splatting_with_Cylindrical_Triplanes_for_Panoramic_Nov_778e41b31bd1.pdf
project_link: null
code_link: "https://github.com/wangqww/CylinderSplat"
aliases:
- CylinderSplat
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将三平面表示从笛卡尔坐标系转换为圆柱坐标系，天然契合全景图像的环绕几何与曼哈顿世界假设，并结合双分支完成可见区域重建与遮挡区域补全。
primary_logic: 采用圆柱三平面对全景空间进行高效编码，并通过像素分支（注意力聚合多视图特征）和体积分支（圆柱Triplane交叉注意力）协同工作，实现单张或稀疏输入下的高质量、高几何一致性新视角合成。
claims:
- 在消融研究中，圆柱Triplane在所有指标上均优于球面Triplane和笛卡尔Triplane，例如Matterport3D上WS-PSNR从20.82（笛卡尔）提升至22.17（圆柱）。
- 移除RGB检索机制后，渲染质量显著下降（WS-PSNR降低，LPIPS升高），证明其引入高频颜色信息的重要性。
- 联合训练像素分支和体积分支的课程策略优于端到端训练，避免局部最优。
- 在宽基线真实数据(20-30m)上，CylinderSplat比OmniScene领先+3.95 dB WS-PSNR，验证了圆柱三平面在极端稀疏视角下的优势。
---

# CylinderSplat: 3D Gaussian Splatting with Cylindrical Triplanes for Panoramic Novel View Synthesis

> [!tip] 核心洞察
> 采用圆柱三平面对全景空间进行高效编码，并通过像素分支（注意力聚合多视图特征）和体积分支（圆柱Triplane交叉注意力）协同工作，实现单张或稀疏输入下的高质量、高几何一致性新视角合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | CylinderSplat：面向全景新视角合成的圆柱三平面3D高斯喷溅方法 |
| 英文题名 | CylinderSplat: 3D Gaussian Splatting with Cylindrical Triplanes for Panoramic Novel View Synthesis |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=lEzkct87Uy) · [Code](https://github.com/wangqww/CylinderSplat) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | CylinderSplat |
| Dataset | Matterport3D, Replica, Residential, 360Loc |

> [!tip] 效果简介
> - Matterport3D (2.0m baseline) 上，WS-PSNR / SSIM / LPIPS 23.76 / 0.835 / 0.175 vs 22.75 / 0.707 / 0.241 (OmniScene) (+1.01 / +0.128 / -0.066)。
> - Replica (1.0m baseline) 上，WS-PSNR / SSIM / LPIPS 28.89 / 0.937 / 0.081 vs 28.83 / 0.935 / 0.091 (PanSplat) (+0.06 / +0.002 / -0.010)。
> - Residential (0.3m baseline) 上，WS-PSNR / SSIM / LPIPS 28.17 / 0.866 / 0.156 vs 27.61 / 0.857 / 0.195 (OmniScene) (+0.56 / +0.009 / -0.039)。

## 概要

全景新视角合成旨在从一幅或稀疏几幅全景图像出发，生成任意新视角下的360°视图。现有前馈方法大多将针孔3D高斯喷溅（3DGS）架构直接迁移至全景域，沿用**笛卡尔三平面**或**成本体积**来表示场景几何。然而，全景图像固有的环绕结构与曼哈顿世界假设使得笛卡尔表示难以有效刻画几何扭曲与遮挡区域，导致重建中出现伪影、孔洞和几何不一致——这是当前方法的**核心瓶颈**。

针对上述问题，本文提出 **CylinderSplat**，一个面向全景新视角合成的前馈3DGS框架。其**核心洞察**在于：将三平面表示从笛卡尔坐标系切换为**圆柱坐标系**，天然契合全景图像的环绕几何特性，并辅以**双分支架构**协同工作——像素分支通过注意力机制聚合多视图特征，重建高质量可见区域；体积分支则在每台摄像机处构建圆柱Triplane，通过交叉平面注意力与三平面-图像注意力补全遮挡区域，实现几何一致的场景完成。

实验表明，CylinderSplat在多个基准上取得领先性能。在Matterport3D两视图重建中，WS-PSNR达到23.76，较此前最优方法OmniScene（Wei et al., 2025）提升+1.01 dB；在更具挑战性的单视图设定下，领先幅度扩大至+1.63 dB。消融研究进一步验证了圆柱Triplane相对于笛卡尔和球面三平面的显著优势，以及RGB检索机制、课程训练策略等设计的关键作用。在宽基线真实场景（20–30m）中，CylinderSplat比OmniScene领先+3.95 dB WS-PSNR，展现出在极端稀疏视角下的鲁棒性。

### 全景新视角合成的挑战

全景图像因其360°×180°的广阔视场，在虚拟现实、房产展示和场景理解等领域具有重要应用。然而，从稀疏甚至单张全景输入合成高质量的新视角全景图像，仍是一项极具挑战的任务。核心难点在于：全景投影固有的扭曲几何、宽基线带来的大面积遮挡，以及室内场景常见的曼哈顿世界结构，使得传统针孔相机的重建方法难以直接迁移。

### 现有方法的瓶颈

近年来，前馈式3D高斯喷溅（3D Gaussian Splatting, 3DGS）方法在针孔图像的新视角合成中取得了显著进展，代表性工作如**MVSplat**（Chen et al., 2024）利用成本体积（cost-volume）聚合多视角信息。然而，将这些方法扩展到全景场景时，面临两个根本性瓶颈：

**瓶颈一：笛卡尔三平面表示不适应全景几何。** 现有全景前馈方法，如**OmniScene**（Wei et al., 2025）采用笛卡尔三平面、**PanSplat**（Zhang et al., 2025）和**Splatter360**（Chen et al., 2025）依赖成本体积，这些表示均基于笛卡尔坐标系。但全景图像记录的是环绕视点的球面投影信息，其几何天然具有圆柱或球面对称性。笛卡尔三平面在表示此类环绕几何时，会引入严重的表示扭曲和资源浪费——其存储复杂度为$O(\Theta \cdot Z \cdot R)$，而圆柱三平面可降至$O(\Theta \cdot Z + Z \cdot R + R \cdot \Theta)$。

**瓶颈二：遮挡区域几何补全能力不足。** 成本体积方法通过多视图匹配进行一次性的几何修正，但在宽基线场景下，遮挡区域缺乏足够的视觉对应，导致重建出现伪影和几何不一致。这在全景场景中尤为突出——输入视图之间的重叠区域有限，大量空间结构仅被单侧观察到。

### 核心动机：从笛卡尔到圆柱的表示革命

本文的核心洞察在于：**将三平面表示从笛卡尔坐标系转换到圆柱坐标系，天然契合全景图像的环绕几何与曼哈顿世界假设。** 如图2所示，圆柱坐标系下的体积单元更均匀地覆盖全景场景的可见区域，而笛卡尔坐标系在远离原点处产生严重拉伸，球面坐标系则在径向方向上过度采样中心区域。

基于这一洞察，CylinderSplat提出双分支架构协同解决上述瓶颈：
- **像素分支**通过注意力机制聚合多视图特征，生成高质量的高斯点云，覆盖可见区域；
- **体积分支**引入圆柱三平面表示，通过交叉平面注意力和三平面-图像注意力，补全遮挡区域的几何与外观。

这种设计使得方法在单视图和稀疏多视图输入下，均能实现高几何一致性的全景新视角合成。

## 核心方法与创新机理

CylinderSplat 的核心创新在于**将前馈3D高斯喷溅（3DGS）的几何表示从笛卡尔坐标系迁移至圆柱坐标系**，并围绕这一表示设计了**双分支协同架构**与**RGB检索机制**，系统性地解决了全景新视角合成中几何扭曲、遮挡补全和颜色细节恢复三大瓶颈。

### 从笛卡尔到圆柱：表示空间的根本转变

现有全景前馈方法——无论是基于成本体积的 **PanSplat**（Zhang et al., 2025）和 **Splatter360**（Chen et al., 2025），还是基于笛卡尔三平面的 **OmniScene**（Wei et al., 2025）——均沿用为针孔相机设计的笛卡尔坐标系。然而，全景图像通过等距投影包裹360°空间，其几何结构天然具有环绕特性：天花板与地板在图像上下边缘被严重拉伸扭曲，而笛卡尔三平面的轴对齐平面无法有效覆盖这些区域。

CylinderSplat 将三平面表示重新定义在圆柱坐标系 $(\theta, z, r)$ 下（Figure 2），形成三个正交平面：$\theta$-$z$ 平面（方位-高度）、$z$-$r$ 平面（高度-半径）和 $r$-$\theta$ 平面（半径-方位）。这一转变带来三重优势：

1. **几何适配性**：圆柱坐标天然契合全景图像的环绕几何与室内场景的曼哈顿世界假设，使三平面的每个平面都能高效覆盖场景的主要结构面（墙面、地面、天花板）。
2. **存储效率跃升**：圆柱三平面将三维体积的存储复杂度从 $O(\Theta \cdot Z \cdot R)$ 降至 $O(\Theta \cdot Z + Z \cdot R + R \cdot \Theta)$，即从立方级降至平方级，使得在相同内存预算下能够编码更高分辨率的几何细节。
3. **遮挡区域补全**：体积分支在圆柱三平面上执行交叉平面注意力（Cross-Plane Attention），通过沿径向维度从另外两个平面聚合特征（公式1），能够基于可见区域的几何先验推理出被遮挡区域的合理结构——这是笛卡尔三平面难以实现的。

消融实验（Table 4）直接验证了这一设计的决定性作用：在仅使用体积分支的条件下，圆柱Triplane在 Matterport3D 上达到 WS-PSNR 22.17，显著优于球面Triplane的21.33和笛卡尔Triplane的20.82。Figure 7 的定性对比进一步显示，圆柱Triplane生成的深度图在遮挡边界处更加清晰连贯，几何一致性明显提升。

### 双分支架构：像素精度与体积补全的分工协同

CylinderSplat 将重建任务分解为两个互补的分支（Figure 3），改变了 baseline 方法依赖单一成本体积进行几何修正的范式：

- **像素分支（Pixel Branch）**：通过自注意力和交叉注意力在多视图特征间传递信息，直接预测每个像素的深度和特征点云，生成覆盖可见区域的高质量像素级高斯。该分支替代了 **MVSplat**（Chen et al., 2024）等方法的成本体积，以更轻量的注意力机制实现多视图信息聚合。
- **体积分支（Volume Branch）**：在每个摄像机位置构建独立的圆柱Triplane，通过交叉平面注意力（融合三平面内部信息）和三平面-图像注意力（公式2，将3D表示对齐到2D视觉证据）补全像素分支无法覆盖的遮挡区域几何，并通过高斯解码器（公式3-5）生成体积高斯。

两个分支的输出高斯通过简单串联融合，但关键在于**三阶段课程训练策略**：先独立训练像素分支，再独立训练体积分支，最后联合微调。消融显示（Table 4），跳过课程策略直接端到端训练会导致性能下降，因为两个分支在训练初期会产生相互干扰，课程学习有效避免了局部最优。

### RGB检索机制：从源视图恢复高频颜色

传统方法直接从特征解码高斯颜色，在稀疏输入下难以恢复纹理细节。CylinderSplat 引入 RGB 检索机制（公式6）：基于每个高斯的可见性权重 $w_v = \mathrm{softmax}(-s_v)$，从源视图对应像素采样颜色 $C_v$，通过 MLP 融合得到最终颜色。这一机制将颜色预测从“凭空生成”转变为“基于证据的检索与融合”，显著提升了渲染结果的纹理真实感。消融实验（Table 4）表明，移除该机制后 WS-PSNR 从 23.76 骤降至 21.89，LPIPS 显著升高，证实其对于高频颜色信息恢复的关键作用。

### 深度先验与初始化策略的配套改进

CylinderSplat 采用 **UniK3D** 作为深度先验，替代 PanSplat 和 Splatter360 使用的 UniFuse。消融实验（Table 11）显示 UniK3D 在所有指标上均优于 UniFuse 和 DepthAnywhere，且无需真实深度监督，训练更高效。此外，针对静态与动态场景，CylinderSplat 设计了自适应的三平面初始化策略：静态场景采用联合初始化以保持全局一致性，动态场景采用独立初始化以灵活应对局部变化（Table 9）。

### 创新点的协同效应

上述创新并非孤立存在，而是形成了系统性的协同：圆柱三平面为体积分支提供了高效的几何表示空间，使得遮挡补全成为可能；双分支架构将可见区域的高精度重建与遮挡区域的几何推理解耦，避免相互干扰；RGB检索机制弥补了体积分支在颜色细节上的不足；课程训练策略确保了两个分支的平稳融合。这一协同在宽基线真实场景（Kansas 数据集，20-30m基线）中得到最极致的体现：CylinderSplat 相比 OmniScene 领先 +3.95 dB WS-PSNR（Table 13），性能差距随基线增大而扩大，验证了圆柱三平面在极端稀疏视角下的结构性优势。

CylinderSplat 提出了一种**双分支前馈架构**，用于从单张或稀疏全景图像中重建3D高斯场景表示并合成新视角。整个框架围绕一个核心洞察构建：**圆柱坐标系天然契合全景图像的环绕几何特性**，能够更高效地编码曼哈顿世界中的扭曲和遮挡区域。

### 输入输出流

框架接收 $N_v$ 张稀疏的全景输入视图，经过端到端的前馈处理，输出一组3D高斯原语 $\mathcal{G}$，可直接由全景光栅化器渲染为目标视角的全景图像。处理流程分为两个互补的分支：

1. **像素分支（Pixel Branch）**：负责从输入视图中提取高质量的高斯原语，覆盖**可见的、良好观测的区域**。
2. **体积分支（Volume Branch）**：在每个摄像机位置引入**圆柱三平面（Cylindrical Triplane）**表示，补全像素分支无法覆盖的**遮挡和欠观测区域**。

两个分支的输出高斯原语被合并为最终场景表示 $\mathcal{G} = \mathcal{G}_{\text{pixel}} \cup \mathcal{G}_{\text{volume}}$，送入直接全景光栅化器（Direct Panoramic Rasterizer）进行渲染。

### 像素分支

像素分支采用**多视图注意力机制**替代传统方法中常用的成本体积（cost volume）。具体而言，它利用预训练的 UniK3D 作为深度先验，通过自注意力和交叉注意力在多个输入视图之间聚合特征，预测每个输入视图的精细化深度图 $D_{\text{pano}}$ 和特征图 $F_{\text{pano}}$，进而生成像素级高斯原语。相比成本体积方案，注意力机制在宽基线和大视角变化下具有更强的特征匹配鲁棒性。

### 体积分支

体积分支是 CylinderSplat 的核心创新所在。它在每个摄像机位置构建一个**圆柱体积**，其边界由 $R_0$（径向）、$\Theta_0$（方位角）和 $Z_0$（高度）定义。该体积被分解为三个正交的特征平面——**圆柱三平面**，将存储复杂度从 $O(N^3)$ 降至 $O(N^2)$。体积分支通过以下步骤完成遮挡区域的几何与颜色补全：

- **平面填充**：将像素分支中落入圆柱体积内的特征点聚合到三平面的对应位置。
- **交叉平面注意力（Cross-Plane Attention）**：在三个平面之间交换信息，融合出统一的3D表示。更新规则为：

$$\mathbf{f}_{\theta z}'(i,j) = \mathbf{f}_{\theta z}(i,j) + \sum_{k=0}^{N_r-1} \left( w_{zr}^{(ijk)} \mathbf{f}_{zr}(j,k) + w_{r\theta}^{(ijk)} \mathbf{f}_{r\theta}(k,i) \right)$$

- **三平面-图像注意力（Triplane-to-Image Attention）**：将三平面特征与源全景图像特征进行交叉注意力，使3D表示与2D视觉证据对齐：

$$\mathbf{f}_{\theta z}''(i,j) = \mathbf{f}_{\theta z}'(i,j) + \sum_{k=0}^{N_r'-1} w_{\mathrm{pano}}^{(ijk)} \mathbf{f}_{\mathrm{pano}}^{(ijk)}$$

- **高斯解码器（Gaussian Decoder）**：在圆柱体积内均匀采样稠密网格点，从三平面聚合特征后通过 MLP 解码出圆柱坐标系下的高斯参数（位置偏移、局部尺度、旋转、不透明度），并通过雅可比变换转换到笛卡尔空间：

$$(x',y',z') = (-(r+\delta_r)\sin(\theta+\delta_\theta),\; z+\delta_z,\; -(r+\delta_r)\cos(\theta+\delta_\theta))$$

$$\mathbf{S}' = |\mathbf{J}| \cdot \mathbf{S}_{\text{local}}$$

- **RGB检索机制（RGB Retrieval）**：基于可见性权重从源视图中采样像素颜色，通过 MLP 融合预测最终颜色，以保留高频纹理细节：

$$C = \mathbf{MLP}\left(\sum_{v=1}^{N_v} w_v \cdot C_v\right), \quad w_v = \mathrm{softmax}(-s_v)$$

### 三阶段课程训练

双分支架构采用**三阶段课程训练策略**以避免局部最优：

1. **阶段一**：仅使用像素分支高斯 $\mathcal{G}_{\text{pixel}}$ 训练。
2. **阶段二**：冻结像素分支，仅训练体积分支高斯 $\mathcal{G}_{\text{volume}}$。
3. **阶段三**：联合微调全部高斯 $\mathcal{G}_{\text{pixel}} \cup \mathcal{G}_{\text{volume}}$。

训练损失为复合渲染损失：

$$\mathcal{L}_{\text{render}} = \|\hat{I} - I_{\text{gt}}\|_1 + 0.05 \cdot \mathcal{L}_{\text{LPIPS}}(\hat{I}, I_{\text{gt}}) + 0.1 \cdot \|\hat{D} - D_{\text{ref}}\|_1$$

消融实验证实，端到端直接训练会导致分支间相互干扰，性能劣于课程策略（Table 4, Row 7）。

### 三平面初始化策略

对于多摄像机设置，CylinderSplat 支持两种三平面初始化策略：**联合初始化**适用于静态场景，所有摄像机共享初始三平面；**独立初始化**适用于动态或宽基线场景，每台摄像机独立初始化。框架根据场景特性动态选择，以在几何一致性和灵活性之间取得平衡。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_lEzkct87Uy/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our CylinderSplat framework. Our method uses a dual-branch architecture trained via a three-stage curriculum. The pixel branch uses a multi-view attention mechanism to generate high-quality Gaussians for well-observed regions. The volume branch is designed to fill the gaps by lifting features into our cylindrical triplane representation, thereby completing the scene geometry robustly. The outputs from both branches are then unified for a final render*

### 3.1 双分支架构总览

CylinderSplat 采用像素分支（Pixel Branch）与体积分支（Volume Branch）协同工作的前馈架构，并通过三阶段课程训练（像素→体积→联合）避免分支间干扰。像素分支负责可见区域的高质量高斯重建，体积分支则补全遮挡与扭曲区域，二者生成的高斯集合最终合并渲染。

### 3.2 像素分支：多视图注意力聚合

像素分支摒弃传统成本体积（cost-volume），改用更高效的多视图注意力机制。给定稀疏输入全景图，分支首先利用 UniK3D 提取初始深度先验 $D_{\text{pano}}$ 和特征图 $F_{\text{pano}}$，随后通过自注意力和交叉注意力在视图间传递信息，预测精细化深度与特征点云，生成针对良好观测区域的像素级高斯 $\mathcal{G}_{\text{pixel}}$。

### 3.3 体积分支：圆柱三平面补全

体积分支是 CylinderSplat 的核心创新，其关键设计在于用**圆柱三平面（Cylindrical Triplane）**替代传统笛卡尔三平面，将存储复杂度从 $O(N^3)$ 降至 $O(N^2)$。三平面由 $\theta$-$z$、$z$-$r$、$r$-$\theta$ 三个正交平面构成，覆盖以每台摄像机为中心的圆柱体积 $(R_0, \Theta_0, Z_0)$。

#### 3.3.1 交叉平面注意力（Cross-Plane Attention）

为融合三个平面的信息，对 $\theta$-$z$ 平面上的每个特征点沿径向维度采样，从 $z$-$r$ 和 $r$-$\theta$ 平面聚合加权特征：

$$\mathbf{f}_{\theta z}'(i,j) = \mathbf{f}_{\theta z}(i,j) + \sum_{k=0}^{N_r-1} \left( w_{zr}^{(ijk)} \mathbf{f}_{zr}(j,k) + w_{r\theta}^{(ijk)} \mathbf{f}_{r\theta}(k,i) \right)$$

其中 $w_{zr}^{(ijk)}$ 和 $w_{r\theta}^{(ijk)}$ 为交叉注意力权重，$N_r$ 为径向采样点数。此操作使三平面表示在三个维度上信息一致。

#### 3.3.2 三平面-图像注意力（Triplane-to-Image Attention）

为将 3D 表示与 2D 视觉证据对齐，将三平面采样点投影到源全景图像，通过交叉注意力聚合全景特征：

$$\mathbf{f}_{\theta z}''(i,j) = \mathbf{f}_{\theta z}'(i,j) + \sum_{k=0}^{N_r'-1} w_{\text{pano}}^{(ijk)} \mathbf{f}_{\text{pano}}^{(ijk)}$$

该残差连接将多视图全景特征注入三平面，增强几何一致性。

#### 3.3.3 高斯解码（Gaussian Decoder）

在圆柱体积内均匀采样 $N_r \times N_\theta \times N_z$ 的稠密网格点，通过 MLP 从三平面聚合特征中解码高斯参数。位置采用带学习偏移的圆柱坐标转换：

$$(x', y', z') = \left( -(r+\delta_r)\sin(\theta+\delta_\theta),\ z+\delta_z,\ -(r+\delta_r)\cos(\theta+\delta_\theta) \right)$$

其中 $\delta_r, \delta_\theta, \delta_z$ 为 MLP 预测的偏移量。尺度通过雅可比矩阵将局部圆柱尺度转换为笛卡尔各向异性缩放：

$$\mathbf{S}' = |\mathbf{J}| \cdot \mathbf{S}_{\text{local}}$$

雅可比 $\mathbf{J}$ 由圆柱到笛卡尔坐标变换的偏导数定义，此策略优于直接预测笛卡尔尺度（消融验证见原文 Table 12）。

#### 3.3.4 RGB 检索机制（RGB Retrieval）

不同于直接从特征解码颜色，CylinderSplat 基于可见性分数从源视图检索像素颜色：

$$C = \mathbf{MLP}\left( \sum_{v=1}^{N_v} w_v \cdot C_v \right), \quad w_v = \text{softmax}(-s_v)$$

其中 $s_v$ 为可见性分数，$C_v$ 为从第 $v$ 个源视图采样的像素颜色。该机制引入高频颜色信息，消融实验表明移除后 WS-PSNR 从 23.76 降至 21.89（Table 4, row 5）。

### 3.4 训练目标

复合损失函数由三部分组成：

$$\mathcal{L}_{\text{render}} = \|\hat{I} - I_{\text{gt}}\|_1 + 0.05 \cdot \mathcal{L}_{\text{LPIPS}}(\hat{I}, I_{\text{gt}}) + 0.1 \cdot \|\hat{D} - D_{\text{ref}}\|_1$$

其中 $\hat{I}$ 为渲染全景图，$I_{\text{gt}}$ 为真值，$\hat{D}$ 为渲染深度，$D_{\text{ref}}$ 为 DepthAnywhere 生成的参考深度。三阶段课程训练策略先独立优化像素分支和体积分支，最后联合微调，避免端到端训练的局部最优问题（Table 4, row 7）。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_lEzkct87Uy/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of the Triplane representation in (a) Cartesian, (b) Spherical, and (c) Cylindrical coordinate systems. (d) The corresponding unit volume elements for each system*

## 实验与关键发现

### 主要结果

CylinderSplat 在两视图重建任务上全面超越现有前馈全景重建方法。Table 1 汇总了 Matterport3D（2.0m 基线）、Replica（1.0m 基线）和 Residential（~0.3m 基线）三个合成数据集上的定量对比。在 Matterport3D 上，CylinderSplat 取得 WS-PSNR 23.76 / SSIM 0.835 / LPIPS 0.175，相较最强基线 **OmniScene**（Wei et al., 2025）提升 +1.01 dB WS-PSNR，SSIM 提升 +0.128，LPIPS 降低 -0.066。在 Residential 数据集上，CylinderSplat 同样领先 OmniScene +0.56 dB。在 Replica 数据集上，CylinderSplat 以微弱优势（+0.06 dB）超越 **PanSplat**（Zhang et al., 2025），两者均处于高性能区间。值得注意的是，CylinderSplat 在几何一致性指标 PCC 上优势尤为突出——Matterport3D 上达到 0.851，显著高于其他方法，验证了圆柱三平面对几何结构的良好表征能力。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_lEzkct87Uy/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison for the two-view reconstruction on the Matterport3D, Replica, and Residential datasets. The first , second and third best results are highlighted. Methods marked with * indicate that we reimplemented them using their official code*

单视图重建任务（Table 2）放大了各方法间的性能差距。CylinderSplat 在 Matterport3D（1.5m 基线）上取得 WS-PSNR 25.13，领先 OmniScene +1.63 dB，SSIM 从 0.749 跃升至 0.854。这一大幅领先表明，圆柱三平面与双分支架构在极端稀疏输入下具有更强的几何补全能力。在真实场景数据集 360Loc（Table 3，平均基线 1.40m）上，CylinderSplat 同样以 WS-PSNR 28.35 排名第一，领先 PanSplat +0.11 dB，SSIM 优势达 +0.023。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_lEzkct87Uy/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison for the single-view reconstruction task*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_lEzkct87Uy/figures/007_Table_3.jpg]]
*Table 3: Quantitative comparison for the twoview reconstruction task on the 360Loc dataset*

多视图扩展实验（Table 5）显示，当输入视图从 2 增至 4 时，CylinderSplat 性能持续提升且始终保持领先，证明框架对视图数量的良好可扩展性。

### 消融研究

Table 4 在 Matterport3D（2.0m 基线）上系统性拆解了各模块的贡献，揭示了以下关键因果机制：

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_lEzkct87Uy/figures/011_Table_4.jpg]]
*Table 4: Ablation Study on Matterport3D (2.0m baseline) using a two-view input. ”Pixel Branch” and ”Volume Branch” denote using only the respective branch. Rows 2-4 compare the performance of cylindrical, spherical, and Cartesian Triplanes. Row 5 presents results without our RGB retrieval, and row 6 shows the impact of the mutil Triplane strategy. Row 7 shows the result of training without our curriculum*

**圆柱三平面的核心作用。** 在仅使用 Volume Branch 的条件下，圆柱 Triplane 取得 WS-PSNR 22.17，显著优于球面 Triplane（19.30）和笛卡尔 Triplane（20.82）。PCC 指标同样从笛卡尔的 0.688 提升至圆柱的 0.782。这一对比直接验证了核心洞察：圆柱坐标系天然契合全景图像的环绕几何与曼哈顿世界假设，其体积单元沿径向、方位角和高度均匀分布，避免了笛卡尔三平面在边缘区域的扭曲和球面三平面在垂直方向的过度拉伸（Fig. 7 可视化佐证）。

**RGB 检索机制的关键性。** 移除 RGB 检索后，WS-PSNR 从完整模型的 23.76 骤降至 21.89，LPIPS 显著恶化。这表明基于可见性权重从源视图采样颜色的机制成功引入了高频纹理信息，弥补了纯特征解码的颜色模糊问题。

**多 Triplane 策略的必要性。** 将每摄像机独立圆柱 Triplane 替换为单一共享 Triplane 后，PCC 从 0.851 降至 0.826。宽基线场景下各摄像机视野差异大，独立 Triplane 能更好地建模局部遮挡几何。

**三阶段课程训练的有效性。** 端到端联合训练（无课程）导致性能下降，验证了先分别训练像素分支和体积分支、再联合微调的策略能有效避免分支间干扰和局部最优。仅使用像素分支时 PCC 为 0.813，仅使用体积分支时 PCC 为 0.782，两者联合后达到 0.851，证明双分支互补性显著。

**深度先验选择。** 消融实验（Table 11）表明 UniK3D 作为深度先验优于 UniFuse 和 DepthAnywhere，且无需真实深度监督，训练更高效。

**Jacobian 尺度变换。** Table 12 显示，通过雅可比矩阵将局部圆柱尺度转换为笛卡尔各向异性缩放，优于直接预测笛卡尔尺度，验证了局部圆柱几何约束的有效性。

### 宽基线真实场景验证

Table 13 在 Kansas 数据集（基线 20-30m）上进行了极端宽基线测试。CylinderSplat 取得 WS-PSNR 领先 OmniScene +3.95 dB 的巨大优势。这一结果表明，基于成本体积的方法在极端宽基线下因匹配失效而产生严重空洞和伪影，而圆柱 Triplane 的体积补全机制从根本上规避了稠密匹配的脆弱性。然而，论文也指出在此极端条件下渲染结果仍存在一定模糊，细节恢复能力有限。

### 效率分析

Table 6 对比了各方法的参数量和推理时间。CylinderSplat 参数量最小，端到端推理（高斯生成 + 全景渲染）速度最快。这得益于圆柱三平面将存储复杂度从 $O(N^3)$ 降至 $O(N^2)$，以及直接全景光栅化器避免了立方体贴图分解的额外开销。

### 几何精度验证

Table 7 在 Matterport3D 上使用真实深度进行几何精度评估。CylinderSplat 在所有深度误差指标上均优于对比方法，证实了圆柱三平面在几何重建上的优越性，与定性深度图对比（Fig. 6）一致——成本体积方法在天花板和地板等扭曲区域产生不一致深度，而 CylinderSplat 保持几何连续。

### 失败模式与局限

尽管整体性能领先，CylinderSplat 存在以下已确认的失败模式：

1. **动态物体鬼影。** 在包含摄影师、行人等瞬态物体的 360Loc 场景中，方法未显式处理动态元素，渲染结果出现鬼影伪影。
2. **极端宽基线模糊。** 在 20-30m 基线条件下，虽然大幅领先基线方法，但渲染细节仍不够锐利，高频纹理恢复能力受限。
3. **高斯冗余。** 当前简单串联像素分支和体积分支的高斯点，存在冗余高斯，论文未探索更高级的融合策略（如深度引导修剪）以减少冗余并提升无缝补全质量。

> **需人工验证：** 以上失败模式来自论文自述的局限性讨论，具体失败案例的定量统计和可视化需查阅原文 Figures 及补充材料确认。

## 定位与知识库关联

### 全景新视角合成的方法演化

全景新视角合成经历了从优化式方法到前馈式方法的范式转变。早期工作如 **PanoGRF** (Chen et al., 2023) 采用全景NeRF进行场景表示，但优化式方法需要逐场景训练，难以满足实时应用需求。随着3D Gaussian Splatting (3DGS) 的兴起，前馈式全景重建方法开始涌现，形成了两条主要技术路线：

**成本体积路线**以 **Splatter360** (Chen et al., 2025) 和 **PanSplat** (Zhang et al., 2025) 为代表，它们继承自针孔前馈方法 **MVSplat** (Chen et al., 2024) 的成本体积聚合范式，通过构建全景深度成本体积来推理场景几何。然而，成本体积在宽基线和大视角变化下容易产生空洞和伪影，尤其在全景图像的天花板、地板等扭曲区域表现不佳。

**三平面路线**以 **OmniScene** (Wei et al., 2025) 为代表，采用笛卡尔三平面作为场景表示，避免了成本体积的离散化限制。但笛卡尔三平面使用轴对齐的正交平面，难以适配全景场景的环绕几何特性，导致在遮挡区域和边缘区域的几何重建不一致。

CylinderSplat 在三平面路线的基础上做出了关键突破：**将三平面坐标系从笛卡尔转换为圆柱坐标系**。这一改变并非简单的坐标变换，而是从根本上使三平面表示与全景图像的采集几何和曼哈顿世界假设对齐。圆柱坐标系的三个正交平面 $(\theta$-$z$、$z$-$r$、$r$-$\theta)$ 天然对应全景场景的环绕方向、高度方向和深度方向，使得特征编码更加紧凑且几何一致。

### 核心差异与适用边界

CylinderSplat 与现有方法的核心差异体现在三个层面：

**1. 几何表示的坐标系选择。** 消融实验（Table 4）直接对比了圆柱Triplane、球面Triplane和笛卡尔Triplane在相同架构下的性能：在Matterport3D数据集上，仅使用Volume Branch时，圆柱Triplane的WS-PSNR达到22.17，显著优于球面Triplane的21.75和笛卡尔Triplane的20.82。这一差距源于圆柱坐标系的体积单元在曼哈顿场景中具有更均匀的几何覆盖，而笛卡尔坐标系在远离原点的区域会产生严重的体积拉伸（Figure 2d），球面坐标系则在垂直方向产生不均匀采样。

**2. 遮挡区域的完成机制。** 成本体积方法（Splatter360、PanSplat）依赖多视图匹配来推理几何，在遮挡区域缺乏直接的信息来源。OmniScene使用笛卡尔三平面进行全局补全，但受限于坐标系的几何失配。CylinderSplat通过双分支架构实现了分工协作：像素分支通过多视图注意力聚合生成高质量的高斯原语用于可见区域，体积分支通过圆柱Triplane的交叉平面注意力和三平面-图像注意力专门补全遮挡区域。消融实验表明，仅使用像素分支时PCC为0.813，加入体积分支后提升至0.851，验证了体积补全的独立贡献。

**3. 颜色细节的获取策略。** CylinderSplat引入了RGB检索机制（RGB Retrieval），基于可见性权重从源视图采样像素颜色并通过MLP融合。移除该机制后，WS-PSNR从23.76降至21.89，LPIPS显著升高，证明直接从特征解码颜色会丢失高频细节信息。这一机制在单视图场景下尤为重要——单视图Matterport3D上CylinderSplat比OmniScene领先+1.63 dB WS-PSNR，差距大于两视图场景的+1.01 dB，说明RGB检索在信息匮乏时发挥了更大作用。

**适用边界方面**，CylinderSplat的设计假设场景具有曼哈顿世界结构（即主要由水平面、垂直墙面构成）。在包含大量弯曲结构（如圆顶建筑、森林场景）的环境中，圆柱Triplane的几何优势可能减弱。此外，方法未显式处理动态物体，在360Loc数据集中包含行人、摄影师的场景会产生鬼影。极宽基线（20-30m）下渲染结果仍存在一定模糊，细节恢复能力有限。

### 局限与开放问题

**已知局限：**
- **动态场景处理缺失**：当前框架假设场景完全静态，对瞬态物体（行人、车辆）缺乏显式建模，导致渲染中出现鬼影伪影。
- **高斯冗余问题**：像素分支和体积分支各自生成高斯原语，简单串联合并存在冗余，未探索深度引导修剪或高斯融合策略。
- **非曼哈顿几何适应性**：圆柱Triplane在弯曲结构场景中的优势尚未验证，可能存在表示效率下降。

**开放问题：**
- 如何设计更高级的高斯融合技术（如基于可见性权重的深度引导修剪）以减少冗余高斯并提升无缝补全质量？
- 能否将方法扩展为显式处理动态场景，例如引入运动掩码或时序建模来抑制瞬态物体的影响？
- 在非曼哈顿弯曲结构（如森林、圆顶建筑）中，是否存在比圆柱Triplane更通用的表示形式？自适应坐标系选择是否可行？
- 极宽基线场景下的细节恢复瓶颈是否可以通过引入生成式先验或超分辨率模块来缓解？

## 原文 PDF

![[paperPDFs/ICLR_2026/CylinderSplat_3D_Gaussian_Splatting_with_Cylindrical_Triplanes_for_Panoramic_Nov_778e41b31bd1.pdf]]
