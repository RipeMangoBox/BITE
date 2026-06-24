---
title: "ObjectMorpher: 3D-Aware Image Editing via Deformable 3DGS"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ObjectMorpher_3D_Aware_Image_Editing_via_Deformable_3DGS.pdf
project_link: null
code_link: null
aliases:
- ObjectMorpher
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将2D编辑操作提升至3D高斯溅射（3DGS）代理，利用ARAP物理约束进行图引导的非刚性变形，并通过扩散模型合成保持光照、色彩与边界的一致性。
primary_logic: 将模糊的2D拖拽编辑转化为几何明确的3D操作：通过轻量级3DGS重建、保持局部刚度的非刚性变形以及生成式合成，在实时交互下实现对象身份保持的逼真编辑。
claims:
- ObjectMorpher在用户研究中在所有三个指标（引导跟随、风格一致性、身份保持）上均显著优于基线方法。
- 提出的ARAP约束确保编辑保持物理合理性，避免不自然失真。
- 与2D拖拽和3D感知基线相比，ObjectMorpher在KID、LPIPS、SIFID指标上均表现更优，并支持实时交互。
- 综合编辑数据集（Table 1） 上 LPIPS = 0.127
---

# ObjectMorpher: 3D-Aware Image Editing via Deformable 3DGS

> [!tip] 核心洞察
> 将模糊的2D拖拽编辑转化为几何明确的3D操作：通过轻量级3DGS重建、保持局部刚度的非刚性变形以及生成式合成，在实时交互下实现对象身份保持的逼真编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | ObjectMorpher: 基于可变形3DGS的3D感知图像编辑 |
| 英文题名 | ObjectMorpher: 3D-Aware Image Editing via Deformable 3DGS |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.28152) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ObjectMorpher |
| Dataset | 综合编辑数据集（Table 1）, 用户研究（Figure 6） |

> [!tip] 效果简介
> - 综合编辑数据集（Table 1） 上，LPIPS 0.127 vs 优于所有比较方法（详见论文表1） (实现最优保真度，同时支持实时交互)；SIFID 10.896 vs 优于所有比较方法 (领先于2D拖拽与3D感知基线)；KID -0.059 vs 优于所有比较方法 (结构相似性更优)。
> - 用户研究（Figure 6） 上，用户偏好 显著领先 vs DragGAN、DragDiffusion等 (在引导跟随、风格一致性、身份保持三项指标上均超过80%偏好)。
> - 效率评估 上，交互延迟 / 模型推理时间 <10s 实时交互，模型推理~20s vs Image Sculpting需半小时以上 (实时交互且高效)。

## 概述

### 问题瓶颈

现有2D图像编辑方法（如**DragGAN**，Pan et al., SIGGRAPH 2023；**DragDiffusion**，Shi et al., CVPR 2024）在像素或隐空间层面操作，缺乏对三维几何的理解，无法处理复杂姿态变化与非刚性变形。另一方面，3D感知编辑方法（如**Object 3DIT**，Michel et al., NeurIPS 2023；**Image Sculpting**，Yenphraphai et al., CVPR 2024）往往依赖繁琐的优化过程、不完整的单目重建或仅支持刚性控制，难以在保持对象身份的同时实现高效、物理合理的对象级编辑。

核心矛盾在于：**将模糊的2D拖拽编辑提升为几何明确的3D操作**，同时保持实时交互性与视觉真实感。

### 核心方法

ObjectMorpher提出了一条从2D像素到3D操作再回到2D合成的闭环管线，其关键调控旋钮是将用户拖拽操作转化为对**可变形3D高斯溅射（3DGS）代理**的物理约束变形，并通过生成式扩散模型完成场景协调。具体而言：

1. **对象表示升级**：利用SAM分割目标对象，通过TRELLIS重建为3DGS表示（Figure 2），替代传统2D像素或隐空间特征。
2. **物理合理的非刚性变形**：基于最远点采样构建稀疏控制图，应用ARAP（As-Rigid-As-Possible）能量约束进行图引导的非刚性变形，保持局部刚度和几何细节。
3. **生成式合成协调**：使用基于Qwen-Image-Edit的LoRA微调扩散模型，将变形后的对象无缝合成回原图，保持光照、色彩与边界一致性（Figure 4）。

### 核心结论

ObjectMorpher在定量与定性评估中均展现出显著优势：

- **用户偏好**：在用户研究中，ObjectMorpher在引导跟随、风格一致性、身份保持三项指标上均获得超过80%的偏好，显著优于所有基线方法（Figure 6）。
- **图像保真度**：在LPIPS（0.127）、SIFID（10.896）、KID（-0.059）等指标上均达到最优，同时支持实时交互（<10秒），而Image Sculpting等3D感知方法需半小时以上（Table 1）。
- **消融验证**：ARAP约束相比拉普拉斯变形能更好地保持局部刚度（Figure 8）；3DGS表示优于网格表示（Figure 7）；生成式合成模块显著消除合成痕迹，提升视觉一致性（Figure 7）。

### 方法谱系与知识库定位

ObjectMorpher处于**3D感知图像编辑**与**交互式对象操控**的交叉地带，其方法定位可通过以下维度刻画：

| 方法维度 | 传统2D拖拽方法 | 现有3D感知方法 | **ObjectMorpher** |
|---------|--------------|--------------|-------------------|
| 对象表示 | 2D像素/隐空间特征 | 网格或NeRF | **可编辑3DGS** |
| 形变控制 | 2D拖拽 | 刚性6-DoF或文本 | **图引导ARAP非刚性变形** |
| 合成方式 | 简单叠放或修补 | 手工修复 | **生成式扩散模型协调** |
| 交互效率 | 实时 | 分钟至小时级 | **实时（<10s）** |

该方法将3DGS的灵活性与可微分性、ARAP的物理合理性以及扩散模型的生成能力相结合，为单图对象编辑提供了一种实时、身份保持且视觉协调的解决方案。

### 待验证边界

以下问题需要进一步验证或探索：
- ARAP变形对具有复杂关节的对象（如人体）的鲁棒性；
- 生成式合成模块是否会在某些情况下改变对象的固有纹理或细节；
- 2D提升至3D的过程依赖TRELLIS的重建质量，其对最终编辑效果的影响边界；
- 方法向多对象场景或视频的扩展可行性。

## 背景与动机

图像编辑是视觉内容创作的核心任务，其理想目标是让用户以直观、高效的方式操控图像中的对象，同时保持结果的真实感和身份一致性。近年来，基于拖拽的编辑范式因其直观性而受到广泛关注——用户只需在图像上定义若干控制点并拖拽至目标位置，即可驱动对象的形变。然而，现有方法在实现这一目标时面临根本性瓶颈。

**2D方法的几何盲区。** 以 **DragGAN**（Pan et al., SIGGRAPH 2023）和 **DragDiffusion**（Shi et al., CVPR 2024）为代表的2D拖拽编辑方法，直接在像素空间或隐空间特征上进行操作。这类方法缺乏对三维几何结构的理解，无法处理复杂的姿态变化与非刚性变形——当用户试图旋转对象或改变其三维朝向时，2D方法往往产生近乎原图的结果，未能真正执行3D感知的编辑（见Figure 5）。其根本原因在于：2D操作只能移动像素，无法推断和保持对象在三维空间中的几何一致性。

**3D感知方法的效率与灵活性困境。** 另一类工作尝试引入3D信息来增强编辑的几何合理性。**Object 3DIT**（Michel et al., NeurIPS 2023）通过语言引导实现3D感知编辑，但缺乏精确的空间控制能力；**Image Sculpting**（Yenphraphai et al., CVPR 2024）基于3D几何控制进行对象编辑，然而其优化过程耗时半小时以上，远未达到实时交互的要求；**BlenderFusion**等方法依赖单目网格重建，表示能力有限且仅支持刚性控制。这些方法共同面临一个困境：要么牺牲编辑精度换取效率，要么承受沉重的计算代价，难以在实时交互与物理合理变形之间取得平衡。

**核心瓶颈。** 综上，现有方法的根本缺口在于：缺乏一种既能保持3D几何意识、又能实现高效非刚性编辑的对象表示与操控机制。具体而言，需要同时解决三个子问题：（1）如何从单张2D图像中构建可编辑的3D对象代理；（2）如何在该代理上施加物理合理的非刚性变形；（3）如何将编辑结果无缝合成回原始场景，保持光照、色彩与边界的一致性。

ObjectMorpher正是针对上述瓶颈提出的解决方案。其核心洞察是：将模糊的2D拖拽编辑转化为几何明确的3D操作——通过轻量级3D高斯溅射（3DGS）重建、保持局部刚度的非刚性变形以及生成式合成，在实时交互下实现对象身份保持的逼真编辑（见Figure 1与Figure 2）。

## 核心创新

ObjectMorpher 的核心创新在于将**模糊的2D拖拽编辑提升为几何明确的3D操作**，通过三个关键模块的协同设计，首次实现了实时交互、物理合理且身份保持的对象级非刚性编辑。

### 从2D像素到可编辑3D代理的表示跃迁

现有2D拖拽方法（如 **DragGAN** (Pan et al., SIGGRAPH 2023) 和 **DragDiffusion** (Shi et al., CVPR 2024)）直接在像素或隐空间特征上操作，缺乏对对象几何结构的理解，导致在复杂姿态或非刚性变形时产生失真或编辑失效（见 Figure 5）。3D感知方法（如 **Object 3DIT** (Michel et al., NeurIPS 2023) 和 **Image Sculpting** (Yenphraphai et al., CVPR 2024)）虽引入了几何信息，但依赖繁琐的优化过程或不完整的单目重建，且多局限于刚性6-DoF控制。

ObjectMorpher 的核心突破在于采用**可编辑的3D高斯溅射（3DGS）** 作为对象代理表示。每个高斯原语 $\mathcal{G}_i : (\mu_i, o_i, s_i, q_i, c_i)$ 显式编码了位置、不透明度、尺度、旋转和颜色信息，其可微性使得从单张图像快速重建3D表示成为可能（通过 TRELLIS）。这一表示跃迁带来了两个关键优势：其一，用户拖拽操作直接作用于3D几何而非2D像素，从根本上解决了跨视角一致性问题；其二，3DGS的轻量特性支持**实时交互**（<10s），而 Image Sculpting 等基于网格的方法需要半小时以上（Table 1）。

### 保持局部刚度的非刚性变形引擎

2D拖拽方法对变形缺乏物理约束，容易产生不自然的扭曲。ObjectMorpher 引入了基于图的**ARAP（As-Rigid-As-Possible）非刚性变形**机制，其能量函数为：

$$E(\mathbf{p}'_i, \mathbf{R}_i) = \sum_i \sum_{j \in \mathcal{N}_i} w_{ij} \| (\mathbf{p}'_i - \mathbf{p}'_j) - \mathbf{R}_i (\mathbf{p}_i - \mathbf{p}_j) \|^2$$

该能量通过惩罚局部非刚性失真来保持对象形状的物理合理性。优化采用交替策略：固定旋转矩阵 $\mathbf{R}_i$ 时，通过线性系统 $\mathbf{L} \mathbf{p}' = \mathbf{b}$ 更新控制点位置；固定位置后，通过 SVD 分解协方差矩阵 $\mathbf{S}_i$ 估计局部旋转。变形最终通过线性混合蒙皮传播至所有3D高斯原语：

$$\boldsymbol{\mu}'_i = \sum_{j \in \tilde{\mathcal{N}}_i} \tilde{w}_{i,j} \left( \mathbf{R}_j (\mu_i - \mathbf{p}_j) + \mathbf{p}'_j \right)$$

消融实验（Figure 8）证实，ARAP约束相比拉普拉斯变形能更好地保持局部刚度和几何细节，变形效果更自然。控制图的构建采用基于测地距离的两阶段阈值策略（Figure 3），避免了欧氏距离连接在复杂几何上的错误关联。

### 生成式合成弥合3D-2D鸿沟

3D编辑后的对象在重新渲染回2D场景时，常面临光照不一致、色彩不协调和边界生硬等问题。ObjectMorpher 设计了基于扩散模型的**生成式合成（Generative Composition）模块**：通过对 Qwen-Image-Edit 进行 LoRA 微调，模型学习将编辑后的对象无缝融入原图场景。消融实验（Figure 7）显示，加入生成式合成后，编辑结果消除了明显的合成痕迹，视觉一致性显著提升。背景修复由 PixelHacker 自动完成，处理因对象变形而暴露的背景区域。

### 创新总结

ObjectMorpher 通过三个 changed slots 的系统性创新——**3DGS表示替代2D像素操作**、**ARAP非刚性变形替代刚性控制**、**生成式合成替代简单叠放**——构建了完整的3D感知编辑管线。用户研究（Figure 6）表明，该方法在引导跟随、风格一致性和身份保持三项指标上均获得超过80%的用户偏好，显著优于所有基线方法。

## 整体框架

ObjectMorpher 的编辑管线由四个核心模块串联构成，形成一条“2D 分割 → 3D 提升 → 可变形编辑 → 生成式合成”的完整处理链（Figure 2）。该管线将用户模糊的 2D 拖拽操作转化为几何明确的 3D 操作，在实时交互下实现对象身份保持的逼真编辑。

![[assets/figures/papers/paper_list_l2555_https_arxiv_org_abs_2603_28152/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our image editing pipeline. The object is lifted from 2D pixels to high-fidelity 3DGS. Real-time editing with local rigidity is applied based on user input. The object is then repositioned, and a generative model refines the edits for harmonious results*

**模块一：2D 对象分割与 3D 提升。** 给定输入图像，用户通过点击交互选择目标对象，由 SAM 完成分割。裁剪后的对象区域送入现成的 3D 生成模型 TRELLIS，将对象重建为 3D 高斯溅射（3DGS）表示。每个高斯原语包含中心位置 $\mu_i$、不透明度 $o_i$、缩放 $s_i$、旋转四元数 $q_i$ 和颜色 $c_i$ 五类参数，为后续变形提供可微、高效的代理几何体。

**模块二：可变形图构建与 ARAP 变形。** 在 3DGS 代理上，通过最远点采样选取控制点，并以两阶段测地距离阈值化构建稀疏控制图（Figure 3）。用户拖拽控制点后，系统在硬控制点约束 $p'_{h_i} = \tilde{p}_{h_i}$ 下，交替优化 ARAP 能量函数 $E(\mathbf{p}'_i, \mathbf{R}_i) = \sum_i \sum_{j \in \mathcal{N}_i} w_{ij} \| (\mathbf{p}'_i - \mathbf{p}'_j) - \mathbf{R}_i (\mathbf{p}_i - \mathbf{p}_j) \|^2$，以保持局部刚度的非刚性变形。变形结果通过线性混合蒙皮传播至所有密集高斯原语，实现物理合理的形状与姿态编辑。

**模块三：背景修复。** 对象变形后暴露的背景区域由 PixelHacker 自动修补，为后续合成提供干净的背景基底。

**模块四：生成式合成与细化。** 编辑后的对象重新定位后，由基于 Qwen-Image-Edit 的 LoRA 微调扩散模型进行生成式合成（Figure 4），将对象无缝融入原图场景，同时协调光照、色彩、边界与背景的一致性。训练数据由 Subjects200K 和 KlingAI 生成的视频构建，通过 TRELLIS 重建 3DGS 并多视角渲染获得粗编辑对。

**关键设计选择。** 与基于 2D 像素/隐空间特征的拖拽编辑（如 DragGAN、DragDiffusion）或仅支持刚性控制的 3D 感知方法（如 Image Sculpting）不同，ObjectMorpher 以可编辑 3DGS 为代理，将模糊的 2D 拖拽提升为几何明确的 3D 操作，并通过 ARAP 物理约束和生成式合成保证编辑的物理合理性与视觉一致性。该设计使系统在保持对象身份的同时，支持实时交互（交互延迟 <10s，模型推理约 20s），显著优于需半小时以上的基线方法。

### 补充图表

![[assets/figures/papers/paper_list_l2555_https_arxiv_org_abs_2603_28152/figures/001_Figure_1.jpg]]
*Figure 1: Unlike text-based methods that fail to localize subjects or interpret geometry, ObjectMorpher uses direct 3D manipulation with real-time interaction. This ensures precise edits while preserving the object’s identity and background*

## 核心模块与公式推导

### 3D高斯溅射（3DGS）对象表示

ObjectMorpher的核心创新在于将2D编辑操作提升至3D空间。给定输入图像，用户通过点击提示交互式选择目标对象，由SAM进行分割。裁剪后的对象区域送入现成的3D生成模型TRELLIS，重建为3D高斯溅射（3DGS）表示。

每个高斯原语由以下参数定义（Sec. 3.1）：

$$\mathcal{G}_i : (\mu_i, o_i, s_i, q_i, c_i)$$

其中 $\mu_i$ 为中心位置，$o_i$ 为不透明度，$s_i$ 为缩放因子，$q_i$ 为旋转四元数，$c_i$ 为颜色属性。3DGS的灵活性与可微性使其成为可变形编辑的理想代理表示——既支持高效的实时渲染，又能通过梯度反向传播实现物理约束下的优化。

### 可变形图构建

为实现非刚性变形，ObjectMorpher在3DGS点云上构建稀疏控制图。具体流程如下（Sec. 3.2.1）：

1. **最远点采样**：从3DGS原语中心点中采样 $N$ 个控制点，确保对对象几何的均匀覆盖。
2. **辅助图构建**：基于欧氏距离连接邻近点，形成辅助图。
3. **测地距离估计**：使用Floyd算法在辅助图上计算最短路径作为测地距离近似。
4. **可变形图形成**：连接测地距离低于阈值 $0.3 D_{\text{scene}}$ 的点对（其中 $D_{\text{scene}}$ 为场景尺度），避免在空间邻近但几何分离的区域（如动物四肢间）建立错误连接。

Figure 3 展示了基于欧氏距离与测地距离构建图连接的差异：测地距离能有效区分几何上分离但空间上邻近的结构，确保变形的物理合理性。

![[assets/figures/papers/paper_list_l2555_https_arxiv_org_abs_2603_28152/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of graph connections based on Euclidean distance and geodesic distance*

### ARAP非刚性变形

ObjectMorpher采用尽可能刚性（As-Rigid-As-Possible, ARAP）约束进行图引导的非刚性变形（Sec. 3.2.2）。用户拖拽选定的控制点，系统在保持局部刚度的前提下传播变形。

**硬控制点约束**：用户指定的控制点目标位置作为优化中的硬约束：

$$p'_{h_i} = \tilde{p}_{h_i}, \quad i \in [H]$$

其中 $p'_{h_i}$ 为优化后的控制点位置，$\tilde{p}_{h_i}$ 为用户指定的目标位置。

**ARAP能量函数**：核心优化目标为最小化局部非刚性失真：

$$E(\mathbf{p}'_i, \mathbf{R}_i) = \sum_i \sum_{j \in \mathcal{N}_i} w_{ij} \| (\mathbf{p}'_i - \mathbf{p}'_j) - \mathbf{R}_i (\mathbf{p}_i - \mathbf{p}_j) \|^2$$

其中 $\mathbf{p}_i$ 和 $\mathbf{p}'_i$ 分别为变形前后的控制点位置，$\mathbf{R}_i$ 为每个控制点的局部旋转矩阵，$\mathcal{N}_i$ 为控制点 $i$ 的邻居集合，$w_{ij}$ 为边权重。该能量惩罚每个局部邻域内偏离刚性变换的程度，从而保持对象的几何细节和形状特征。

**交替优化**：ARAP能量通过两步交替优化求解：

1. **位置更新**：固定旋转矩阵 $\mathbf{R}_i$，求解线性系统更新控制点位置：
   $$\mathbf{L} \mathbf{p}' = \mathbf{b}$$
   其中 $\mathbf{L}$ 为图拉普拉斯矩阵，$\mathbf{b}$ 由当前旋转估计和约束条件决定。

2. **旋转估计**：固定位置 $\mathbf{p}'_i$，通过SVD分解估计每个控制点的局部旋转。构建协方差矩阵：
   $$\mathbf{S}_i = \sum_{j \in \mathcal{N}_i} w_{ij} (\mathbf{p}_j - \mathbf{p}_i)^T (\mathbf{p}'_j - \mathbf{p}'_i)$$
   对 $\mathbf{S}_i$ 进行SVD分解得到最优旋转 $\mathbf{R}_i = \mathbf{V}_i \mathbf{U}_i^T$。

**密集高斯变形**：稀疏控制图的变形通过线性混合蒙皮（Linear Blend Skinning）传播至所有3D高斯原语：

$$\boldsymbol{\mu}'_i = \sum_{j \in \tilde{\mathcal{N}}_i} \tilde{w}_{i,j} \left( \mathbf{R}_j (\mu_i - \mathbf{p}_j) + \mathbf{p}'_j \right)$$

其中 $\mu_i$ 和 $\boldsymbol{\mu}'_i$ 为变形前后的高斯中心，$\tilde{\mathcal{N}}_i$ 为影响高斯 $i$ 的控制点集合，$\tilde{w}_{i,j}$ 为蒙皮权重。该公式将每个控制点的刚性变换（旋转+平移）加权组合，实现了从稀疏控制到密集表示的平滑变形传播。

### 生成式合成模块

变形后的3DGS渲染结果需要无缝合成回原场景。ObjectMorpher设计了基于扩散模型的生成式合成模块（Sec. 3.3），包含以下关键组件：

1. **背景修复**：使用PixelHacker自动修复因对象变形而暴露的背景区域。
2. **LoRA微调**：基于Qwen-Image-Edit扩散模型进行LoRA微调，训练数据由Subjects200K数据集和KlingAI生成的视频构建，包含同一对象在不同姿态和变形下的配对图像。
3. **合成细化**：将编辑后的对象渲染与修复后的背景拼接，通过微调后的扩散模型进行全局协调，在保持光照、色彩和边界一致性的同时消除合成痕迹。

Figure 4 展示了训练数据准备流程和生成式合成模型的完整管线。

![[assets/figures/papers/paper_list_l2555_https_arxiv_org_abs_2603_28152/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of the training data preparation and the pipeline of our generative composition model*

### 模块间因果机制

整个管线的因果链条可概括为：**2D分割与3D提升**（Sec. 3.1）提供可编辑的几何代理 → **可变形图与ARAP约束**（Sec. 3.2）实现物理合理的非刚性编辑 → **生成式合成**（Sec. 3.3）确保编辑结果与场景的视觉一致性。消融实验（Figure 7, Figure 8）验证了各模块的必要性：3DGS表示优于网格表示，ARAP约束优于拉普拉斯变形，生成式合成显著消除合成痕迹。

## 实验与分析

### 主要定量结果

ObjectMorpher在综合编辑数据集上取得了全面的指标领先（Table 1）。在保真度方面，LPIPS降至**0.127**，SIFID为**10.896**，KID为**-0.059**，三项指标均优于DragGAN、DragDiffusion、Object 3DIT、Image Sculpting和BlenderFusion等所有对比方法。值得注意的是，DragDiffusion因其编辑修改幅度极小（论文标注为“often edits images with minimal modifications”），其数值表现需谨慎解读。

![[assets/figures/papers/paper_list_l2555_https_arxiv_org_abs_2603_28152/figures/007_Table_1.jpg]]
*Table 1: Quantitative evaluation. RI represents real-time interaction and MT represents model inference time.(∗DragDiffusion often edits images with minimal modifications.)*

在效率维度，ObjectMorpher是少数支持**实时交互**（RI √）的方法之一，用户拖拽操作的交互延迟小于10秒；完整模型推理时间约**20秒**。相比之下，同样使用3D代理的Image Sculpting需要半小时以上才能完成一次编辑。这一效率优势源于3DGS表示的轻量可微特性与ARAP变形的解析求解。

### 用户研究

用户研究（Figure 6）从三个维度评估编辑质量：**引导跟随**（Guidance Following）、**风格一致性**（Style Consistency）和**身份保持**（Identity Preservation）。ObjectMorpher在所有三个指标上均获得了超过80%的用户偏好，显著领先于DragGAN和DragDiffusion等基线。这一结果直接验证了核心主张：将2D拖拽提升至3D几何操作能更忠实地响应用户意图，同时保持对象外观一致性。

![[assets/figures/papers/paper_list_l2555_https_arxiv_org_abs_2603_28152/figures/006_Figure_6.jpg]]
*Figure 6: Visual results of our user study. Our method is consistently preferred across all three metrics (Guidance Following, Style Consistency, and Identity Preservation) over all baselines*

### 消融实验

**3D表示选择**（Figure 7）：对比3DGS与Mesh表示，在均不使用生成式合成（w/o GC）的条件下，3DGS渲染的质量明显优于Mesh。Mesh表示在变形后容易出现几何伪影和纹理拉伸，而3DGS的连续高斯原语表示能更平滑地传播变形。当加入生成式合成（w/ GC）后，3DGS渲染的编辑对象与场景的光照、色彩和边界一致性进一步提升，消除了直接叠放产生的合成痕迹。

**变形约束对比**（Figure 8）：与拉普拉斯变形相比，ARAP约束能更好地保持局部刚度和几何细节。拉普拉斯变形在固定旋转矩阵的条件下优化顶点位置，容易导致局部区域的不自然拉伸；ARAP通过交替优化位置和旋转矩阵，显式惩罚非刚性失真，使变形结果更符合物理直觉。

**图连接策略**（Figure 3）：基于测地距离构建的可变形图优于欧氏距离连接。测地距离能正确反映3D表面上的相邻关系，避免在空间上接近但表面不连通的控制点之间建立错误连接，从而防止变形时出现不合理的拉扯。

### 定性分析

Figure 5展示了8个对象在5种方法上的编辑对比。2D拖拽方法（DragGAN、DragDiffusion）无法理解3D几何，对非刚性引导的响应几乎与原始图像无异。3D感知方法中，Object 3DIT依赖语言指令，缺乏精确的空间控制能力；Image Sculpting虽支持3D操作，但在复杂非刚性变形下难以保持真实感。ObjectMorpher是唯一能忠实跟随非刚性用户引导同时保持照片级真实感的方法。

### 补充图表

![[assets/figures/papers/paper_list_l2555_https_arxiv_org_abs_2603_28152/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparisons. We show results on 8 subjects (rows) across 5 methods (columns). Our method (Ours) is the only one that faithfully follows the non-rigid user guidance while maintaining photorealism. 2D methods fail to perform the 3D-aware edit, producing results nearly identical to the origin*

![[assets/figures/papers/paper_list_l2555_https_arxiv_org_abs_2603_28152/figures/008_Figure_7.jpg]]
*Figure 7: Ablation on 3D representations (3D GS vs. Mesh) and the use of Generative Composition (w/ GC vs. w/o GC)*

![[assets/figures/papers/paper_list_l2555_https_arxiv_org_abs_2603_28152/figures/009_Figure_8.jpg]]
*Figure 8: Ablation on the deformation constraints*

## 方法谱系与知识库定位

### 问题瓶颈：从2D拖拽到3D感知编辑的鸿沟

图像编辑领域长期存在两条技术路线之间的张力。一方面，以 **DragGAN**（Pan et al., SIGGRAPH 2023）和 **DragDiffusion**（Shi et al., CVPR 2024）为代表的2D拖拽编辑方法，通过在像素空间或隐空间特征上直接操作控制点，实现了直观的用户交互。然而，这些方法本质上缺乏3D几何意识——当面对需要非刚性变形或显著姿态变化的编辑时，它们无法理解对象的三维结构，往往产生近乎于原图的保守结果（Figure 5），或在复杂视角下出现不自然的失真。

另一方面，3D感知编辑方法试图弥补这一缺陷，但各自存在明显局限。**Object 3DIT**（Michel et al., NeurIPS 2023）依赖语言引导，缺乏精确的空间定位能力；**Image Sculpting**（Yenphraphai et al., CVPR 2024）虽然引入了3D几何控制，但其基于网格的表示和优化流程导致交互延迟超过半小时，难以实用；**BlenderFusion**等基于单目网格重建的方法则面临重建不完整、仅支持刚性控制的限制。

核心瓶颈可归结为：**现有方法无法在实时交互的约束下，实现对单张图像中任意对象的物理合理、身份保持的非刚性编辑**。

### ObjectMorpher的方法定位

ObjectMorpher的关键设计在于将模糊的2D拖拽操作提升为几何明确的3D操作，其技术路线在三个维度上区别于现有工作：

**对象表示层面**：不同于2D方法依赖像素/隐空间特征，也不同于Image Sculpting使用网格表示，ObjectMorpher采用可编辑的3D高斯溅射（3DGS）作为代理表示。3DGS的可微渲染特性和显式几何结构，使其既能保持高保真度的外观重建，又支持高效的变形操作。消融实验（Figure 7）直接证实了这一点：在相同条件下，3DGS表示（w/o GC）的渲染质量明显优于网格表示（Mesh w/o GC）。

**形变控制层面**：ObjectMorpher引入基于图的ARAP（As-Rigid-As-Possible）非刚性变形框架。具体而言，通过最远点采样构建稀疏控制图，并以测地距离（而非欧氏距离）作为图连接准则，确保变形传播遵循对象的拓扑结构（Figure 3）。ARAP能量函数在交替优化中惩罚局部非刚性失真，相比拉普拉斯变形能更好地保持局部刚度和几何细节（Figure 8）。这一设计使得用户仅需拖拽少数控制点，即可实现物理合理的形状和姿态变化。

**合成协调层面**：编辑后的3DGS渲染结果需要无缝融入原图场景。ObjectMorpher通过LoRA微调的扩散模型（基于Qwen-Image-Edit）进行生成式合成，同时处理光照、色彩、边界和背景一致性。消融实验（Figure 7）表明，加入生成式合成（w/ GC）后，编辑对象与场景的视觉一致性显著提升，消除了明显的合成痕迹。背景修复则由PixelHacker自动完成。

### 与基线的定量与定性对比

定量评估（Table 1）提供了多维度的证据。在感知保真度指标上，ObjectMorpher取得了LPIPS 0.127、SIFID 10.896、KID -0.059的成绩，全面优于DragGAN、DragDiffusion、Object 3DIT和Image Sculpting等基线方法。值得注意的是，DragDiffusion的编辑往往修改幅度极小（论文标注为∗），这使得其指标数值看似不错，但实际编辑效果有限。在效率维度上，ObjectMorpher支持实时交互（<10s），模型推理时间约20s，而Image Sculpting需要半小时以上，差距显著。

定性比较（Figure 5）进一步揭示了方法的本质差异。在8个不同对象、多种编辑类型（姿态调整、形状变形、部件移动等）的测试中，2D拖拽方法几乎无法执行真正的3D感知编辑，结果与原图高度相似；Object 3DIT受限于语言引导的模糊性，难以精确定位编辑区域。ObjectMorpher是唯一能够忠实跟随非刚性用户引导、同时保持照片级真实感的方法。

用户研究（Figure 6）提供了最强有力的证据：在引导跟随、风格一致性和身份保持三项指标上，ObjectMorpher的用户偏好均超过80%，显著优于所有基线方法。这表明其编辑结果不仅在自动指标上占优，更在人类感知层面获得了压倒性认可。

### 适用边界与局限

尽管ObjectMorpher在单对象场景中表现出色，其适用边界仍需明确。首先，方法目前针对单对象编辑设计，**如何扩展至多对象场景或视频序列**是一个开放问题。多对象间的遮挡关系和交互变形将引入额外的复杂性。

其次，ARAP变形约束假设对象具有局部刚性结构，这对于刚体或半刚体对象（如雕塑、家具、水果）效果良好，但**对于具有复杂关节的对象（如人体、动物），ARAP可能不足以建模关节处的非刚性运动**。论文未在人体姿态编辑等场景上进行验证，这一局限需要关注。

第三，2D提升至3D的过程依赖TRELLIS进行3DGS重建。**TRELLIS的重建质量直接影响后续编辑的保真度**。对于严重遮挡、纹理稀疏或结构复杂的对象，重建失败可能导致编辑结果退化。论文未系统分析重建质量对编辑效果的影响边界。

最后，**生成式合成模块是否会在某些情况下改变对象的固有纹理或细节**，也是一个需要警惕的问题。扩散模型的生成特性可能在协调过程中引入微小的纹理偏差，尽管用户研究中身份保持指标表现优异，但在极端光照或复杂背景下仍需进一步验证。

### 开放问题

1. **多对象与视频扩展**：如何将基于3DGS的编辑框架推广至包含多个交互对象的场景，以及如何保持视频编辑中的时序一致性？
2. **复杂关节对象的变形鲁棒性**：对于人体等具有复杂运动学的对象，ARAP约束是否足够？是否需要引入骨骼驱动或基于物理的模拟？
3. **重建-编辑的误差传播**：TRELLIS重建的不确定性如何量化，以及如何在编辑流程中对其进行鲁棒处理？
4. **生成式合成的可控性边界**：扩散模型在协调过程中引入的纹理变化是否可预测和可控？是否存在保持原始纹理的更严格约束方式？

## 原文 PDF

![[paperPDFs/CVPR_2026/ObjectMorpher_3D_Aware_Image_Editing_via_Deformable_3DGS.pdf]]