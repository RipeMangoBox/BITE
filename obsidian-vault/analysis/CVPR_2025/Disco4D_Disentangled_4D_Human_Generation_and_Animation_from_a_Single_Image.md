---
title: "Disco4D: Disentangled 4D Human Generation and Animation from a Single Image"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Disco4D_Disentangled_4D_Human_Generation_and_Animation_from_a_Single_Image.pdf
project_link: https://disco-4d.github.io/
code_link: null
aliases:
- Disco4D
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过将人体基础模型 SMPL-X 转化为固定的高斯表示，并在其外部拟合可分离的衣物高斯，同时为每个衣物高斯引入可学习的身份编码（Identity Encoding），从而在训练中对身体与衣物进行结构化解耦。"
primary_logic: "固定 SMPL-X 高斯，在其上拟合分段高斯，实现身体与衣物的解耦，为后续的独立编辑和动画奠定基础。"
claims:
- "在 SynBody 和 CloSe 数据集上，Disco4D 在 CLIP 相似度、PSNR、SSIM、LPIPS 等指标上均显著优于 DreamGaussian、LGM 和 SHERF，尤其在 novel pose 任务中优势明显。"
- "在 4D-Dress 数据集上，Disco4D（重姿态+学习形变）在所有评估指标（CLIP、PSNR、SSIM、LPIPS）上全面超过 DreamGaussian4D、MonoHuman 等视频到 4D 方法。"
- "用户研究显示，Disco4D 生成的 3D 高斯在图像一致性和整体质量上均获得最高评分，显著优于 DreamGaussian 和 LGM。"
- "SynBody (3D generation) 上 CLIP Similarity (All) ↑ = 0.851"
---

# Disco4D: Disentangled 4D Human Generation and Animation from a Single Image

> [!tip] 核心洞察
> 固定 SMPL-X 高斯，在其上拟合分段高斯，实现身体与衣物的解耦，为后续的独立编辑和动画奠定基础。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Disco4D: 从单张图像解耦4D人体生成与动画 |
| 英文题名 | Disco4D: Disentangled 4D Human Generation and Animation from a Single Image |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2409.17280) · [Project](https://disco-4d.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Disco4D |
| Dataset | SynBody (3D generation), CloSe (3D generation, Novel Pose), 4D-Dress (4D animation) |

> [!tip] 效果简介
> - SynBody (3D generation) 上，CLIP Similarity (All) ↑ 为 0.851，对比 0.751 (DreamGaussian)，变化 +0.100。
> - SynBody (3D generation) 上，PSNR (Novel View) ↑ 为 15.691，对比 13.118 (DreamGaussian)，变化 +2.573。
> - CloSe (3D generation, Novel Pose) 上，PSNR ↑ 为 17.96，对比 15.54 (SHERF)，变化 +2.42。

## 概要

从单张二维图像重建可动画的三维数字人，是虚拟试穿、数字人定制与影视游戏等应用的核心需求。然而，现有方法普遍将人体与衣物融合为单一表面或隐式场，导致重建结果无法独立编辑衣物、更换服饰或进行物理准确的动画驱动。这一瓶颈源于表示层面的根本性耦合——身体与衣物的几何、外观被绑定在同一个不可分割的表示中。

Disco4D 针对这一瓶颈提出了结构化解耦方案。其核心思路是：**将 SMPL-X 参数化人体模型转化为固定的三维高斯表示，并在其外部独立拟合可分离的衣物高斯**。通过为每个衣物高斯引入可学习的身份编码（Identity Encoding），Disco4D 在训练过程中实现了身体与衣物的显式分离，为后续的独立编辑与动画控制奠定了基础。具体而言，身体高斯由 SMPL-X 姿态直接驱动，衣物高斯则结合重姿态变换与学习到的形变网络分开控制，既跟随身体运动，又保留衣料自身的动态特征。

在定量评估中，Disco4D 展现了显著优势。在 SynBody 与 CloSe 数据集上，其 CLIP 相似度、PSNR、SSIM、LPIPS 等指标均显著优于 DreamGaussian、LGM 与 SHERF 等基线方法，尤其在新视角与新姿态任务中优势突出（Table 3）。在 4D-Dress 数据集的动态动画评估中，Disco4D 在所有指标上全面超过 DreamGaussian4D、MonoHuman 等视频到 4D 方法（Table 5）。用户研究进一步表明，Disco4D 生成的 3D 高斯在图像一致性与整体质量上均获得最高评分（Table 4）。

该方法也存在若干已知局限：SMPL-X 估计在挑战性姿态下不够鲁棒；视觉外壳初始化依赖多视图扩散模型，侧面与背面视角存在不准确风险；服装类别解耦受限于二维分割模型精度，可能发生误分类；当前仅支持单层服装，无法处理多层叠加与遮挡场景。



### 问题背景

从单张图像生成可动画的 3D 人体是虚拟试穿、数字人定制、影视特效等应用的核心需求。理想的人体生成模型不仅需要在新视角下保持高保真度的外观重建，还应支持对衣物资产进行独立的编辑、换装和物理准确的动画驱动。然而，现有方法在这一目标上存在根本性瓶颈。

### 现有方法的瓶颈

当前主流的单图像人体重建方法——无论是基于网格、NeRF 还是 3D Gaussian Splatting——普遍将衣物与身体融合为单一表面或隐式场。这种耦合表示带来了三个关键缺陷：

1. **编辑不可分离**：由于衣物与身体在几何和外观上未被区分，无法对上衣、裤子等衣物资产进行独立的删除、重新上色或换装操作。
2. **动画物理不准确**：在驱动人体姿态变化时，衣物缺乏独立的运动模型，无法展现符合其材质特性的动态行为（如裙摆的摆动、宽松衣物的褶皱变化）。
3. **遮挡区域重建困难**：输入图像中被遮挡的身体部位和衣物背面缺乏有效的先验引导，导致不可见区域的重建质量低下。

从方法谱系来看（Table 1、Table 2），现有 3D 生成方法（如 **DreamGaussian**、**LGM**）仅输出单一的静态高斯场，缺乏分层结构和动画能力；以人体为中心的 NeRF 方法（如 **SHERF**）虽能处理姿态变化，但同样未实现身体与衣物的解耦。在 4D 动画领域，**DreamGaussian4D**、**MonoHuman**、**GART**、**GaussianAvatar** 等方法使用单一形变场驱动所有高斯点，无法对衣物进行独立的动态建模。这些缺口共同指向一个核心问题：**缺乏一种结构化解耦的表示，使得身体与衣物能够被分别建模、独立编辑和差异化动画**。

### 本文动机

Disco4D 的动机正是填补上述空白：**构建一个从单张图像出发，能够解耦身体与衣物、支持 4D 动画和编辑的人体生成框架**。其核心思路是将人体基础模型 SMPL-X 转化为固定的高斯表示，并在其外部拟合可分离的衣物高斯，同时为每个衣物高斯引入可学习的身份编码（Identity Encoding），从而在训练中对身体与衣物进行结构化解耦。这一设计使得身体由 SMPL-X 姿态直接驱动，衣物则结合重姿态变换与学习到的形变网络分开控制，为后续的独立编辑和物理合理动画奠定基础。



## 核心方法与创新机理

Disco4D 的核心创新在于将人体与衣物从表示层面进行**结构化解耦**，从而在单张图像输入下同时实现高质量的 3D/4D 生成、独立编辑与可动画化。这一解耦设计围绕以下关键机制展开：

### 身体与衣物的分层高斯表示

现有单图像人体重建方法（如 DreamGaussian、LGM、SHERF）将身体与衣物融合为单一表面或隐式场，导致无法独立编辑、换装或进行物理准确的动画。Disco4D 的解决方案是：将 SMPL-X 网格转化为固定的高斯表示作为身体层，在其外部拟合可分离的衣物高斯层，两者在几何上严格分层。

具体而言，身体高斯通过预定义的重心坐标绑定到 SMPL-X 网格三角面，形成不可变的基底表示；衣物高斯则嵌入到规范网格的三角面上，以局部坐标系的偏移向量定义位置。训练期间，**身体高斯的参数完全固定**，仅优化衣物高斯，从根本上避免了身体与衣物相互干扰的问题。

### 身份编码与类别感知的衣物分离

为实现衣物的按类别分离和管理，Disco4D 为每个衣物高斯引入一个可学习的 **15 维身份编码（Identity Encoding）** $e$，将高斯点与其所属的衣物类别关联。该编码通过 alpha 混合渲染为 2D 特征图，由 2D 分割掩码提供监督。基于身份编码，系统在优化过程中对衣物高斯进行**类别选择性稠密化**，确保不同衣物资产在 3D 空间中保持独立。

### 视觉外壳引导的衣物初始化

衣物高斯的初始化质量直接影响后续优化的收敛效果。Disco4D 利用视频扩散模型与高斯重建模型（GRM）生成初步的衣物高斯及视觉外壳（visual hull），再将其对齐并绑定到 SMPL-X 网格。消融实验（Figure 10）表明，相比随机初始化或直接使用 SMPL-X 表面初始化，视觉外壳初始化显著提升了重建精度和几何真实感。

### SDF 损失与剪枝确保分层边界

为强制衣物高斯始终位于身体网格外部，Disco4D 引入**有符号距离函数（SDF）损失**，对侵入 SMPL-X 网格内部的高斯点施加惩罚，并结合定期剪枝操作强化这一空间约束。消融实验（Figure 7）证实，若取消此约束并共同优化所有高斯，身体内部会出现衣物点，分层效果被破坏。

### 解耦驱动的 4D 动画策略

在动画阶段，身体高斯直接由 SMPL-X 姿态参数驱动，衣物高斯则结合**重姿态变换**与**可学习的形变网络** $\phi$ 分开控制。形变网络根据时间戳预测衣物高斯的位置、旋转和缩放变化，以模拟衣物材质的动态特性。这种“重姿态 + 学习形变”的组合策略在 4D-Dress 数据集上取得了最优指标（Table 5：CLIP 相似度 0.900，PSNR 25.46，LPIPS 0.035），验证了分层动画机制的有效性。

### 相对基线的关键变化总结

| 设计维度 | 基线方法 | Disco4D 创新 |
|---------|---------|-------------|
| 身体-衣物表示 | 融合为单一网格/NeRF/高斯层 | SMPL-X 高斯（固定身体）与衣物高斯彻底解耦 |
| 衣物分离机制 | 缺少显式类别分离 | 15 维身份编码 + 类别选择性稠密化 |
| 优化策略 | 身体与衣物同时优化 | 固定身体高斯，仅优化衣物高斯 |
| 衣物初始化 | 随机或 SMPL-X 表面初始化 | 视频扩散模型 + GRM 生成视觉外壳初始化 |
| 4D 动画 | 单一形变场驱动所有高斯 | 身体姿态直驱 + 衣物重姿态 + 学习形变网络 |



![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2409_17280/figures/001_Figure_1.jpg]]
*Figure 1: Disco4D is a novel Gaussian Splatting framework for 4D disentangled human generation, animation and editing from a single image*

Disco4D 的整体 pipeline 围绕一个核心洞察展开：**固定 SMPL-X 高斯，在其外部拟合分段衣物高斯，实现身体与衣物的结构化解耦**。基于这一解耦表示，系统可自然地扩展至 4D 动画和编辑任务。如 Figure 2 所示，框架分为两大阶段：

### 阶段一：3D 解耦生成（3D Generation）

输入为单张人物图像，输出为身体与衣物完全分离的规范姿态高斯表示。流程包含以下关键模块：

1. **SMPL-X 参数估计与精炼**：从输入图像估计 SMPL-X 模型的姿态 $\theta$、体型 $\beta$ 和表情 $\psi$ 参数，并进行像素级对齐精炼，生成与图像中人物姿态一致的身体网格 $\mathcal{M}(\beta,\theta,\psi)$。

2. **SMPL-X 高斯绑定**：将平面高斯直接绑定到 SMPL-X 网格的每个三角面上（类似 SuGaR 的方式），通过预定义的重心坐标显式计算高斯均值 $\mu_{body}$，形成固定的身体高斯表示 $S_{body}$。**训练期间，这些身体高斯的参数完全固定，不再优化**。

3. **衣物高斯初始化**：利用视频扩散模型与 Gaussian Reconstruction Models (GRM) 快速获取初步的衣物高斯及其视觉外壳（visual hull）。这些衣物高斯随后被嵌入到规范姿态的 SMPL-X 网格三角面上，采用局部坐标系描述偏移量 $\mu = O + v$，从而实现与身体网格的结构化绑定。

4. **迭代优化与解耦**：在固定身体高斯的前提下，仅优化衣物高斯 $S_{cloth}$。通过以下机制实现彻底分层：
   - **SDF 损失与剪枝**：利用有符号距离函数损失 $\mathcal{L}_{sdf}$ 惩罚侵入 SMPL-X 网格内部的衣物高斯，并定期剪枝，确保所有衣物点位于身体表面外部。
   - **身份编码与选择性稠密化**：为每个衣物高斯引入可学习的 15 维身份编码 $e$，通过 2D 分割掩码监督，将高斯与衣物类别（如上衣、裤子等）关联。基于身份编码的类别信息，仅对特定类别的高斯进行选择性稠密化，实现衣物资产的分离管理。
   - **SDS 纹理补全**：利用扩散模型的 Score Distillation Sampling (SDS) 损失，对输入图像中不可见区域（如背面）的衣物纹理进行高分辨率补全。

端到端训练的总损失为：

$$\mathcal{L} = \mathcal{L}_{ori} + \mathcal{L}_{id} + \mathcal{L}_{ani} + \mathcal{L}_{sdf} + \mathcal{L}_{SDS}$$

其中 $\mathcal{L}_{ori}$ 为原始 3D 高斯泼溅的 RGB 重建损失，$\mathcal{L}_{id}$ 为身份编码渲染与 2D 分割掩码之间的监督损失，$\mathcal{L}_{ani}$ 约束高斯核的长宽比以防止产生过于细长的核，$\mathcal{L}_{sdf}$ 确保衣物高斯位于身体外部，$\mathcal{L}_{SDS}$ 驱动纹理补全。

### 阶段二：4D 动画与编辑（4D Animation & Editing）

基于已解耦的规范姿态高斯表示，Disco4D 支持两种动画模式：

- **直接姿态驱动**：身体高斯直接遵循 SMPL-X 模型的姿态形变，衣物高斯通过重姿态变换（reposing）跟随身体运动。这种方式无需额外训练，适用于给定姿态序列的快速动画。

- **视频驱动的动态学习**：给定驱动视频，先将规范化身重姿态对齐到视频中的各帧姿态，再优化一个形变网络 $\phi$，根据时间戳 $t$ 预测衣物高斯的额外形变 $S'' = \phi(S', t)$。该网络初始化为预测零形变以避免训练发散。身体由 SMPL-X 姿态直接驱动，衣物则结合重姿态变换与学习到的形变分开控制，从而模拟符合材质特性的动态行为。

编辑操作直接利用解耦表示：提取特定类别的高斯进行删除（如移除外套）、重新上色（通过微调颜色球谐参数并固定几何属性），或进行衣物资产的组合与替换。

### 输入输出流总结

- **输入**：单张 RGB 人物图像（3D 生成）；或单张图像 + 驱动视频/姿态序列（4D 动画）
- **中间表示**：固定的 SMPL-X 身体高斯 + 嵌入网格的衣物高斯（各高斯携带身份编码）
- **输出**：可分层的 3D 高斯化身（支持独立编辑）；或按时间序列渲染的 4D 动画帧



### 3.1 基础表示：3D高斯与SMPL-X

Disco4D 构建在两个基础表示之上。3D高斯点定义为：

$$G(x) = e^{-\frac{1}{2}(x-\mu)^{T}\Sigma^{-1}(x-\mu)}$$

其中 $\mu$ 为空间均值，$\Sigma$ 为协方差矩阵，控制高斯核的形状与方向。

SMPL-X 网格函数为：

$$\mathcal{M}(\beta,\theta,\psi): \mathbb{R}^{|\beta|\times|\theta|\times|\psi|} \to \mathbb{R}^{3N}$$

由姿态 $\theta$、体型 $\beta$ 和表情 $\psi$ 参数化，输出 $N$ 个顶点的三维坐标。

### 3.2 扩展高斯表示：身份编码

Disco4D 对标准3D高斯进行关键扩展，引入可学习的身份编码（Identity Encoding）：

$$S = G(\mu, r, s, \alpha, c, e)$$

其中除位置 $\mu$、旋转 $r$、缩放 $s$、不透明度 $\alpha$、颜色 $c$ 外，新增 $e$ 为长度15的可学习向量，用于将每个高斯点关联到特定的衣物类别。该编码通过2D分割掩码监督学习，使衣物高斯可按类别分离和管理。

### 3.3 SMPL-X高斯：固定的身体表示

身体高斯通过将平面高斯直接绑定到SMPL-X网格的三角面上生成。高斯均值 $\mu_{body}$ 使用预定义的重心坐标在对应三角形中显式计算。**在整个衣物高斯优化过程中，SMPL-X高斯的参数保持完全固定**，这是实现身体与衣物解耦的核心约束。

### 3.4 衣物高斯初始化

衣物高斯通过高斯重建模型（GRM）获取初步结果，并嵌入到SMPL-X规范网格的三角形面中。每个衣物高斯的位置由局部坐标系中的偏移向量定义：$\mu = O + v$，其中 $O$ 为三角形局部原点，$v$ 为偏移量。这种网格嵌入使衣物高斯能够继承SMPL-X的形变，同时保持独立优化。

### 3.5 优化损失函数

端到端训练的总损失为：

$$\mathcal{L} = \mathcal{L}_{ori} + \mathcal{L}_{id} + \mathcal{L}_{ani} + \mathcal{L}_{sdf} + \mathcal{L}_{SDS}$$

各分量作用如下：
- $\mathcal{L}_{ori}$：原始3D高斯的RGB重建损失
- $\mathcal{L}_{id}$：身份编码损失，通过alpha混合将身份编码渲染为2D特征图 $E_{id} = \sum_{i\in\mathcal{N}} e_i \alpha_i \prod_{j=1}^{i-1}(1-\alpha'_j)$，与2D分割掩码对齐
- $\mathcal{L}_{ani}$：各向异性损失，约束高斯核长宽比不超过阈值 $\tau$：

$$\mathcal{L}_{ani} = \frac{1}{|P|}\sum_{p\in P}\max\left(\frac{\max(s_p)}{\min(s_p)},\tau\right)-\tau$$

- $\mathcal{L}_{sdf}$：有符号距离函数损失，惩罚侵入SMPL-X网格内部的衣物高斯，配合固定间隔的剪枝操作，确保衣物始终位于身体外部
- $\mathcal{L}_{SDS}$：利用扩散模型的Score Distillation Sampling损失，对不可见区域的衣物纹理进行补全

### 3.6 4D动画：重姿态与形变网络

动画策略分两层。身体高斯直接遵循SMPL-X姿态参数驱动的形变。衣物高斯则结合两个阶段：首先通过重姿态变换将规范空间的衣物高斯变换到目标姿态；随后形变网络 $\phi$ 根据时间戳 $t$ 预测额外的位置、旋转和缩放变化：

$$S'' = \phi(S', t)$$

其中 $S'$ 为重姿态后的衣物高斯空间描述。形变网络初始化为预测零形变，避免动态与静态模型之间的发散。这种“重姿态+学习形变”的组合使衣物既能跟随身体运动，又能表现其材质特有的动态行为（如裙摆飘动）。



## 实验与关键发现

### 核心实验设置

Disco4D 的评估覆盖三个维度：**3D 生成质量**、**4D 动画能力**和**编辑灵活性**。3D 生成实验在 SynBody 和 CloSe 两个合成数据集上进行，评估指标包括 CLIP 相似度（衡量生成结果与参考图像的语义一致性）、PSNR、SSIM 和 LPIPS（衡量新视角/新姿态下的重建精度）。4D 动画实验在 4D-Dress 数据集上开展，对比视频到 4D 的方法。此外，还通过用户研究（1-5 分制）评估生成结果的主观质量。基线方法涵盖三类：通用 3D 高斯生成方法（**DreamGaussian**、**LGM**）、以人体为中心的 NeRF 基线（**SHERF**），以及 4D 生成/重建方法（**DreamGaussian4D**、**MonoHuman**、**GART**、**GaussianAvatar**）。

### 3D 生成主结果

在 SynBody 数据集上，Disco4D 在所有指标上显著超越现有 3D 生成基线（Table 3）。CLIP 相似度达到 0.851，比 DreamGaussian（0.751）高出 0.100；PSNR 为 15.691 dB，较 DreamGaussian（13.118 dB）提升 2.573 dB。这一优势在新视角渲染和新姿态生成两个子任务上均保持一致。在 CloSe 数据集的新姿态任务上，Disco4D 的 PSNR 达到 17.96 dB，比 SHERF（15.54 dB）提升 2.42 dB，LPIPS 降至 0.136（SHERF 为 0.186）。这表明解耦表示在保持人体几何一致性的同时，能更准确地重建衣物细节。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2409_17280/figures/005_Table_3.jpg]]
*Table 3: CLIP-embedding loss for generated humans and segmented assets, and performance (PSNR, SSIM, LPIPS) comparisons for novel poses and views on the Synbody and CloSe datasets across Dream-Gaussian, LGM, SHERF, and Disco4D*

用户研究（Table 4）进一步验证了 Disco4D 的感知质量优势。在图像一致性评分上，Disco4D 获得 3.037 分，DreamGaussian 和 LGM 分别仅获 2.017 和 1.852 分；整体质量评分呈现相同趋势（3.037 vs. 2.338 vs. 2.017）。定性对比（Figure 3）显示，DreamGaussian 和 LGM 生成的高斯点常混杂在身体内部或稀疏分布在表面，而 Disco4D 的衣物高斯紧密贴合在 SMPL-X 网格外部，几何分层清晰。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2409_17280/figures/007_Table_4.jpg]]
*Table 4: User study rates quality of generated 3D Gaussians from 1-5, the higher the better*

### 4D 动画主结果

4D 动画实验在 4D-Dress 数据集上进行（Table 5）。Disco4D 采用“重姿态变换 + 学习形变”策略，在所有指标上全面领先。CLIP 相似度达到 0.900，比 DreamGaussian4D（0.784）高出 0.116；PSNR 为 25.46 dB，较 DreamGaussian4D（20.54 dB）提升 4.92 dB；LPIPS 降至 0.035（DreamGaussian4D 为 0.080）。值得注意的是，即使将 DreamGaussian4D 的初始化替换为 Disco4D 的静态模型，其性能也有显著提升（PSNR 从 19.16 dB 升至 21.02 dB），说明解耦表示本身为后续动态建模提供了更好的起点。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2409_17280/figures/008_Table_5.jpg]]
*Table 5: CLIP-embedding loss for generated humans and segmented assets, and performance (PSNR, SSIM, LPIPS) comparison on the 4D-Dress dataset across various video-to-4D methods*

定性结果（Figure 4）表明，MonoHuman 和 GaussianAvatar 在不可见视角下容易出现纹理模糊和几何塌缩，GART 的衣物动态缺乏物理真实感，而 Disco4D 通过分别控制身体刚性运动与衣物形变，在保持身份一致性的同时生成了更自然的衣物褶皱和摆动。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2409_17280/figures/009_Figure_4.jpg]]
*Figure 4: Qualitative comparison of 4D generation between DreamGaussian4D, MonoHuman, GART, GaussianAvatar, and Disco4D*

### 消融实验

消融实验揭示了 Disco4D 三个关键设计的作用：

1. **视觉外壳初始化**（Figure 10）：随机初始化导致衣物高斯分布杂乱，SMPL-X 表面初始化无法捕捉宽松衣物的偏移量。基于视频扩散模型和 GRM 生成的视觉外壳初始化，使衣物高斯从一开始就位于合理的空间位置，显著提升了重建精度和几何真实感。

2. **身体高斯固定与 SDF 约束**（Figure 7 左）：若共同优化所有高斯，衣物点会侵入 SMPL-X 网格内部，导致身体与衣物边界模糊。Disco4D 固定身体高斯并施加 SDF 损失惩罚入侵点，确保衣物高斯始终位于网格外部，这是实现清晰分层的关键。

3. **身份编码与选择性稠密化**（Figure 7 右）：身份编码使每个衣物高斯关联到特定类别（如上衣、裤子），基于类别进行选择性稠密化可让各衣物部件获得足够的高斯点覆盖。消融实验中，去除身份编码后无法实现按类别分离的编辑——编辑操作会错误地影响无关区域。

### 失败模式分析

Disco4D 的失败案例（Figure 9）可归纳为三类：

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2409_17280/figures/015_Figure_9.jpg]]
*Figure 9: Failure cases of Disco4D. (a) Poor SMPL-X estimation (b) Poor visual hull initialization (c) Misclassification of clothing categories*

- **SMPL-X 估计失败**：在挑战性姿态（如大幅度扭转、遮挡严重）下，SMPL-X 参数估计不准确，导致身体高斯骨架错位，进而影响衣物高斯的附着和动画质量。
- **视觉外壳初始化质量不足**：侧面和背面视角的视觉外壳依赖于多视图扩散模型的生成能力，当模型输出不准确时，初始化衣物高斯的位置和形状会偏离真实衣物，后续优化难以完全纠正。
- **衣物类别误分类**：身份编码的监督信号来自 2D 分割模型，当分割模型将手臂误判为上衣、或将裙子误判为裤子时，衣物高斯的类别标签出错，导致编辑时无法精确选取目标衣物。

### 公平性说明

需要指出，3D 生成实验主要在合成数据集（SynBody、CloSe）上进行，其评估结果可能不完全代表真实拍摄场景的性能。4D 动画对比中，DreamGaussian4D 并非专为人体设计，直接比较可能存在系统偏差。与 2D 动画方法（Animate-Anyone、Magic-Animate、CHAMP）的对比（Figure 8）仅提供了定性结果，未进行定量分析——定性上 Disco4D 在保持身体形态和细节方面表现更好，但缺乏数值支撑。

### 补充图表

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2409_17280/figures/012_Figure.jpg]]

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2409_17280/figures/013_Figure.jpg]]

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2409_17280/figures/002_Table_1.jpg]]
*Table 1: Overview of 3D/4D generation methods from a single image*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2409_17280/figures/003_Table_2.jpg]]
*Table 2: Overview of 4D generation methods from video*



## 定位与知识库关联

### 问题定位与核心瓶颈

单图像人体重建长期面临一个根本性瓶颈：现有方法将衣物与身体融合为单一表面（mesh）或隐式场（NeRF），导致无法独立编辑、换装或进行物理准确的动画。这一限制严重制约了虚拟试穿、数字人定制等应用场景。Disco4D 的核心因果调控变量在于**结构化解耦**——将人体基础模型 SMPL-X 转化为固定的高斯表示，并在其外部拟合可分离的衣物高斯，同时为每个衣物高斯引入可学习的身份编码（Identity Encoding），从而在训练中对身体与衣物实现类别级分离。

### 与现有方法的谱系关系

#### 3D 生成方法对比

Disco4D 在 3D 人体生成任务上与三类基线形成对比：

- **DreamGaussian**：通用 3D 高斯生成基线，将人体与衣物作为单一高斯层处理。在 SynBody 数据集上，其 CLIP 相似度仅为 0.751，而 Disco4D 达到 0.851（Table 3）。定性分析（Figure 7）显示，DreamGaussian 的所有高斯点被限制在身体几何内部，无法形成独立的衣物层。

- **LGM**：大规模多视角高斯模型，虽约有一半点延伸至 SMPL-X 体表之外，但缺乏结构化的衣物表示，导致衣物区域稀疏且无法按类别分离。用户研究中 LGM 的图像一致性评分仅为 1.852（Disco4D 为 3.037，Table 4）。

- **SHERF**：以人体为中心的 NeRF 基线，在新姿态任务上 PSNR 为 15.54，Disco4D 达到 17.96（CloSe 数据集，Table 3），差距主要源于 NeRF 对新视角泛化的固有限制。

Disco4D 与上述方法的本质差异在于三个关键设计槽位（changed slots）：（1）身体-衣物表示从融合改为彻底解耦；（2）引入 15 维身份编码实现类别级管理；（3）训练期间固定身体高斯、仅优化衣物高斯，避免相互干扰。

#### 4D 生成与动画方法对比

在 4D 动画任务上，Disco4D 与以下基线形成对比：

- **DreamGaussian4D**：动态高斯泼溅基线，使用单一形变场驱动所有高斯。在 4D-Dress 数据集上，其 PSNR 为 20.54，Disco4D（重姿态+学习形变）达到 25.46（Table 5）。值得注意的是，当 DreamGaussian4D 采用 Disco4D 的初始化时，PSNR 从 19.16（LGM 初始化）提升至 21.02，间接验证了解耦初始化的价值。

- **MonoHuman**：单目视频人体 4D 重建方法，同样缺乏分层表示，无法支持衣物编辑。

- **GART** 与 **GaussianAvatar**：前者侧重高斯动画重建与跟踪，后者基于可变形 3D 高斯构建化身，但均未实现身体与衣物的显式解耦。

Disco4D 的 4D 动画策略区别于上述方法的关键在于：身体由 SMPL-X 姿态直接驱动，衣物则结合重姿态变换与学习到的形变网络分开控制——重姿态处理姿态驱动的刚性变化，形变网络模拟衣物的动态材质行为。

#### 与 2D 动画方法的定性对比

与 Animate-Anyone、Magic-Animate、CHAMP 等 2D 动画方法相比，Disco4D 在身体形状保持和细节保真度上具有优势，但该对比仅提供定性结果（Figure 8），缺乏定量分析，需谨慎解读。

### 适用边界与局限

#### 技术依赖与级联失效

Disco4D 的性能受限于多个上游模块的精度：

1. **SMPL-X 估计**：在挑战性姿态下仍不够鲁棒，可能导致身体姿态错误（Figure 9a）。这是整个管线的基础依赖，估计误差会级联影响后续的高斯绑定和衣物拟合。

2. **视觉外壳初始化**：依赖多视图扩散模型生成初步衣物高斯，侧面和背面视角存在不准确的风险（Figure 9b），直接影响衣物几何的初始质量。

3. **2D 分割模型**：身份编码的训练依赖 2D 分割掩码作为监督信号，分割模型的误分类（如将手臂误判为上衣，Figure 9c）会导致衣物类别解耦失败。

#### 表示能力的边界

- **单层服装假设**：当前方法仅支持单层服装，无法处理多层衣物叠加和遮挡服装的重建。这是解耦表示的结构性限制，而非工程问题。
- **短序列动画**：4D 动画侧重于短序列重建，长时间范围动画的质量和时间一致性有待验证。形变网络在长序列上可能累积误差。

### 开放问题

1. **初始化鲁棒性**：如何改进姿态引导模型以获得更准确的视觉外壳，减少初始化对后续优化的依赖？视觉外壳质量是决定最终几何精度的关键上游因素。

2. **多层服装建模**：如何扩展框架以支持多层服装，并重建被遮挡的衣物？这需要突破当前“单层高斯拟合”的表示范式。

3. **长序列动画**：如何实现长序列动画的高质量生成，同时保持时间一致性和细节保真度？形变网络的设计和训练策略可能需要根本性改进。

4. **身份编码泛化**：能否利用更先进的分割基础模型或弱监督策略提升身份编码的准确性与泛化能力？当前对 2D 分割模型的强依赖限制了在开放场景中的适用性。

5. **多人场景推广**：Disco4D 的解耦表示是否可以推广至多人场景或交互式动画任务？这涉及多人空间关系的建模和遮挡处理。



## 原文 PDF

![[paperPDFs/CVPR_2025/Disco4D_Disentangled_4D_Human_Generation_and_Animation_from_a_Single_Image.pdf]]
