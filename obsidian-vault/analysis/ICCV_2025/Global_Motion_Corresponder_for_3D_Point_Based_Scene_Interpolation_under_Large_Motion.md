---
title: "Global Motion Corresponder for 3D Point-Based Scene Interpolation under Large Motion"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Global_Motion_Corresponder_for_3D_Point_Based_Scene_Interpolation_under_Large_Motion.pdf
aliases:
- GMCG
- GMC3PBSIULM
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过引入可学习的共享规范空间和基于能量的损失，利用一元势场预测每个高斯的 SE(3) 变换，取代直接的点对点匹配，从而建立平滑的全局对应。"
primary_logic: "利用 MLP 将 DINO 语义特征和高斯空间坐标映射为 SE(3) 变换，将两个时间步的高斯点对齐到共享规范空间；通过双向能量损失和局部等距损失优化变换，确保语义相似和空间邻近的点具有一致的运动，在无需真实运动轨迹的情况下实现鲁棒的大运动插值与外推。"
claims:
- "GMC 学习一元势场预测 SE(3) 映射到共享规范空间，平衡对应、空间语义平滑和局部刚性。"
- "在合成全局运动场景上，GMC 在平均 SI-FID (224.42) 和 SI-MPED (16.47) 上显著优于 Dynamic Gaussian (283.53 / 824.50) 等基线。"
- "移除 DINO 特征输入会导致不合理的插值和错误的全局运动插值，验证了语义特征的关键作用。"
- "Synthetic Global-Motion Scenes (8 scenes) 上 SI-FID ↓ = 224.42"
---

# Global Motion Corresponder for 3D Point-Based Scene Interpolation under Large Motion

> [!tip] 核心洞察
> 利用 MLP 将 DINO 语义特征和高斯空间坐标映射为 SE(3) 变换，将两个时间步的高斯点对齐到共享规范空间；通过双向能量损失和局部等距损失优化变换，确保语义相似和空间邻近的点具有一致的运动，在无需真实运动轨迹的情况下实现鲁棒的大运动插值与外推。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 大运动下基于三维点云场景插值的全局运动对应器 |
| 英文题名 | Global Motion Corresponder for 3D Point-Based Scene Interpolation under Large Motion |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2508.20136); [Project](https://junrul.github.io/gmc/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Global Motion Corresponder (GMC) |
| Dataset | Synthetic Global-Motion Scenes (8 scenes), Synthetic Local-Motion Scenes (6 scenes), Real-World Global-Motion Scenes (3 scenes) |

> [!tip] 效果简介
> - Synthetic Global-Motion Scenes (8 scenes) 上，SI-FID ↓ 为 224.42，对比 283.53 (Dynamic Gaussian)，变化 -59.11。
> - Synthetic Global-Motion Scenes (8 scenes) 上，SI-MPED ↓ (×10⁻³) 为 16.47，对比 824.50 (Dynamic Gaussian)，变化 -808.03。
> - Synthetic Local-Motion Scenes (6 scenes) 上，SI-FID ↓ 为 112.62，对比 117.94 (PAPR in Motion)，变化 -5.32。

## 概述

**核心问题**：在三维场景插值中，当相邻帧之间存在大幅度全局运动时，传统基于局部最近邻的点对应关系会严重失效，导致现有动态场景重建方法无法产生合理的中间帧渲染。

**核心方法**：本文提出 **Global Motion Corresponder (GMC)**，其关键思路是用可学习的一元势场（Unary Potential Field）取代直接的点对点匹配。具体而言，GMC 利用 MLP 将每个三维高斯的 DINO 语义特征与空间坐标映射为 SE(3) 变换（旋转与平移），将两个时间步的高斯点云对齐到一个共享的规范空间（canonical space），并通过双向能量损失和局部等距损失优化该变换，在无需真实运动轨迹的条件下实现鲁棒的大运动插值与外推。

**方法定位**：GMC 属于基于三维高斯泼溅（3D Gaussian Splatting, 3DGS）的动态场景插值方法，与 **4DGS**、**Deformable 3DGS**、**Dynamic Gaussian**、**PAPR in Motion** 等基于变形场或迭代优化的基线方法形成对比。其独特之处在于：(1) 通过共享规范空间学习全局对应，而非依赖局部空间搜索；(2) 显式引入预训练的 DINO 语义特征引导运动学习；(3) 预测每个高斯的刚性 SE(3) 变换而非直接回归位移。

**主要结果**：
- 在 8 个合成全局运动场景上，GMC 的平均 **SI-FID** 为 224.42，显著优于 Dynamic Gaussian（283.53）；**SI-MPED** 为 16.47，远低于 Dynamic Gaussian（824.50）。
- 在 3 个真实世界全局运动场景上，GMC 的 **SI-FID** 为 166.33，较 Dynamic Gaussian（308.65）降低 142.32。
- 在局部运动场景上，GMC 同样取得了有竞争力的结果（合成场景 SI-FID 112.62）。
- 消融实验证实，移除 DINO 特征输入会导致不合理的插值或错误的全局运动插值，验证了语义特征在建立可靠对应中的关键作用。

**局限性**：方法假设输入的两个时间步的三维高斯重建质量较高；训练涉及多阶段和多个超参数；目前仅支持两个已知状态间的插值与外推，尚未扩展到连续多帧序列。

## 背景与动机

### 问题背景：三维场景插值中的大运动挑战

三维场景插值（3D scene interpolation）旨在从两个已知时间步的多视角观测中，生成连续、平滑的中间状态渲染。这项任务在视觉特效、动态场景重建和自由视点视频中具有重要应用价值。近年来，基于三维高斯泼溅（3D Gaussian Splatting, 3DGS）的方法因其高效的渲染能力和显式的点云表示而受到广泛关注。然而，现有方法普遍依赖一个隐含假设：相邻时间步之间的运动幅度较小，因此可以通过**局部最近邻匹配**来建立点对应关系，进而推断运动轨迹。

Figure 1 清晰地揭示了这一假设的脆弱性：当帧间运动较小时（左图），在局部邻域内搜索对应点确实能给出正确的运动和对应关系；但当场景发生**大幅度全局运动**（中图）——例如物体整体平移、旋转或剧烈形变——局部搜索将不可避免地产生错误对应，因为正确的对应点已经远远超出了局部邻域的范围。这正是本文所要解决的核心瓶颈。

### 现有方法的缺口

当前基于变形场或迭代优化的动态场景插值方法在面对大运动时暴露出一系列结构性缺陷：

1. **基于变形场的方法**（如 **4DGS** 和 **Deformable 3DGS**）通过对预训练的静态高斯模型施加变形来建模运动。这类方法在全局运动幅度较大时往往无法产生合理的渲染结果，如 Figure 2 所示，在 Ball 和 Dolphin 场景中直接失效。

2. **基于迭代优化的方法**（如 **Dynamic Gaussian** 和 **PAPR in Motion**）通过联合优化高斯参数和运动参数来进行插值。尽管它们在小幅度局部运动场景中表现尚可，但在大运动场景下同样面临严重退化。Figure 3 的 Softball 真实场景中，Dynamic Gaussian 完全丢失了棒球棒，暴露出其对大帧间运动的脆弱性。定量结果进一步证实了这一点：在合成全局运动场景上，Dynamic Gaussian 的平均 SI-FID 为 283.53，SI-MPED 高达 824.50×10⁻³（Table 1），远不能令人满意。

3. **深层原因**：这些方法的共同症结在于**点对应关系的建立方式**——它们或显式或隐式地依赖空间邻近性来匹配点对，而大运动直接破坏了这一前提。此外，现有方法普遍**未利用语义特征**来引导对应学习，仅依赖颜色和空间坐标，使得在纹理稀疏或重复纹理区域难以区分正确对应。

### 本文动机

上述分析揭示了一个根本性的方法缺口：在大运动场景中，**需要一个不依赖局部最近邻的全局对应机制**。理想的解决方案应当能够：

- 在无需真实运动轨迹标注的情况下，学习两个时间步之间的平滑全局对应；
- 充分利用语义信息来区分外观相似但语义不同的点；
- 在建立全局对应的同时保持局部运动的一致性（局部刚性）。

本文提出 **Global Motion Corresponder (GMC)**，核心思想是：**用可学习的一元势场（unary potential field）预测每个高斯的 SE(3) 变换，将两个时间步的高斯点对齐到一个共享规范空间（shared canonical space），从而将点对应问题转化为规范空间中的最近邻匹配问题**。这一设计从根本上绕开了局部搜索的局限，使得即使在大幅度全局运动下也能建立正确的对应关系。同时，通过引入 PCA 降维的 DINO 语义特征和局部等距损失，GMC 在语义平滑性和局部刚性之间取得了平衡，实现了鲁棒的大运动插值乃至外推。

## 核心创新

GMC 的核心创新在于**将大运动下的点对应问题从“显式匹配”转化为“隐式对齐”**。传统方法（如 Dynamic Gaussian、PAPR in Motion）依赖局部最近邻搜索或变形场微调来建立跨帧对应，这在全局运动幅度较大时极易产生错误匹配（Figure 1 中段）。GMC 的关键洞察是：**不直接匹配点对，而是学习一个一元势场（Unary Potential Field），将两个时间步的高斯点分别映射到共享规范空间**，使对应点在规范空间中自然重合，从而绕过局部搜索的歧义性。

具体而言，GMC 在以下四个维度实现了方法创新：

### 1. 点对应建立方式：从局部匹配到全局规范空间对齐

基线方法（4DGS、Deformable 3DGS、Dynamic Gaussian、PAPR in Motion）均以某种形式的局部空间邻近性作为对应依据——或通过最近邻搜索，或通过变形场在局部邻域内微调。这在全局运动下存在根本性缺陷：当物体发生大幅度平移或旋转时，真实对应点可能相距甚远，局部搜索必然失败。

GMC 的解决方案是引入**可学习的共享规范空间**（Eq. 2）：

$$\underbrace{R_i^{(0)} \pmb{\mu}_i^{(0)} + \pmb{t}_i^{(0)}}_{\hat{\pmb{\mu}}_i^{(0)}} = \underbrace{R_j^{(1)} \pmb{\mu}_j^{(1)} + \pmb{t}_j^{(1)}}_{\hat{\pmb{\mu}}_j^{(1)}}$$

两个时间步的高斯均值 $\pmb{\mu}$ 各自通过 SE(3) 变换被映射到同一规范空间，对应点在规范空间中占据相同位置。这种设计将“寻找对应”转化为“学习使对应点重合的变换”，从根本上规避了局部搜索的局限性。

### 2. 语义特征利用：DINO 特征引导变换学习

基线方法通常仅依赖颜色或空间坐标进行匹配，缺乏高层语义信息。GMC 引入 **PCA 降维的 DINO 特征** $\tilde{\pmb{f}}$ 作为一元势场 MLP 的输入之一（Eq. 3）：

$$\mathcal{F}(\tilde{\pmb{f}}, \pmb{\mu}) = (\pmb{R}, \pmb{t})$$

DINO 特征提供了语义感知能力，使网络能够区分外观相似但语义不同的区域（如球棒和手臂），从而学习到语义一致的变换。消融实验证实了这一设计的决定性作用：**移除 DINO 输入会导致不合理的插值结果、错误的全局运动插值或错误的局部运动插值**。这验证了语义特征在引导全局对应学习中的关键地位。

### 3. 运动表示：从位移预测到 SE(3) 变换

基线方法通常直接预测点的位移向量或稠密变形场，这种表示难以捕捉旋转运动且缺乏结构约束。GMC 改为**预测每个高斯的完整 SE(3) 变换**（旋转 $\pmb{R}$ 以四元数表示，平移 $\pmb{t}$），由两个独立 MLP（$\Theta_{\mathcal{R}}$ 和 $\Theta_T$）分别输出。SE(3) 表示天然适合描述刚体运动，且为后续的 SLERP 插值和外推提供了数学上的便利。

### 4. 优化目标：能量损失与局部等距约束

基线方法通常仅依赖渲染损失进行优化。GMC 引入了双重几何约束：

- **双向能量损失** $\mathcal{L}_{\mathrm{E}}$（Eq. 5）：基于颜色、DINO 特征和规范空间距离的加权能量函数，在 $\mathcal{G}_0$ 和 $\mathcal{G}_1$ 之间执行双向最近邻匹配，确保所有高斯点都找到对应。
- **局部等距损失** $\mathcal{L}_{\mathrm{iso}}$（Eq. 7）：约束每个高斯的 $k$ 近邻在变换前后距离不变，促进局部刚性，抑制插值中的噪声漂浮物和模糊渲染。

总损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{E}} + \alpha \mathcal{L}_{\mathrm{iso}}$，其中 $\alpha$ 逐步增大以先建立全局对应、再强化局部平滑。消融实验表明，**移除局部等距损失会导致插值中出现噪声漂浮物或模糊渲染**，验证了该约束的必要性。

### 创新总结

GMC 的四项创新形成了一套完整的因果链条：**DINO 语义特征**提供高层判别信息 → **一元势场 MLP** 学习 SE(3) 映射 → **共享规范空间**实现隐式对齐 → **能量损失 + 局部等距损失**联合优化确保对应质量和运动平滑性。这套机制使得 GMC 在合成全局运动场景上以 SI-FID 224.42 和 SI-MPED 16.47 显著优于 Dynamic Gaussian（283.53 / 824.50），并在真实世界全局运动场景上保持了类似的优势。

## 整体框架

GMC 的整体管道围绕一个核心思想展开：**用可学习的一元势场（Unary Potential Field）取代直接的点对点匹配，将两个时间步的高斯点云映射到一个共享规范空间（Shared Canonical Space）中完成对齐**。该方法不依赖真实运动轨迹，仅需两个时刻的多视角图像即可实现大运动下的场景插值与外推。其工作流程如图 Figure 4 所示，可分为四个阶段。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2508_20136/figures/004_Figure_4.jpg]]
*Figure 4: Method Overview. (1) Left: 3DGS models at t = 0 and t = 1. (2) Middle Left: Alignment in a canonical space through SE(3) transformation. (3) Middle Right: 3D matching (colored by PCA-DINO features) is established based on the alignment. (4) Right: Continuous 3D interpolation is derived from the 3D transformation and 3D matching*

**阶段一：双时刻 3DGS 预训练。** 对输入的两个时间步 $t=0$ 和 $t=1$，分别独立训练 3D Gaussian Splatting 模型，获得两组高斯点云 $\mathcal{G}_0$ 和 $\mathcal{G}_1$。每个高斯点除常规的颜色 $\mathbf{c}$ 和不透明度等参数外，还携带从 DINO 视觉 Transformer 提取并经 PCA 降维至 4 维的语义特征 $\tilde{\mathbf{f}}$。

**阶段二：规范空间对齐。** 核心模块是一元势场 MLP $\mathcal{F}(\tilde{\mathbf{f}}, \boldsymbol{\mu}) = (\mathbf{R}, \mathbf{t})$，它以每个高斯的空间均值 $\boldsymbol{\mu}$ 和 PCA-DINO 特征 $\tilde{\mathbf{f}}$ 为输入，输出一个 SE(3) 变换（旋转 $\mathbf{R}$ 用四元数表示，平移 $\mathbf{t}$）。两个时间步各有一个独立的 MLP（$\mathcal{F}_0$ 和 $\mathcal{F}_1$），分别将 $\mathcal{G}_0$ 和 $\mathcal{G}_1$ 中的高斯点变换到共享规范空间：

$$\hat{\boldsymbol{\mu}}_i^{(0)} = \mathbf{R}_i^{(0)} \boldsymbol{\mu}_i^{(0)} + \mathbf{t}_i^{(0)}, \quad \hat{\boldsymbol{\mu}}_j^{(1)} = \mathbf{R}_j^{(1)} \boldsymbol{\mu}_j^{(1)} + \mathbf{t}_j^{(1)}$$

其目标是使语义和几何上对应的点在该空间中占据相同位置，从而隐式地建立跨时间的点对应关系。

**阶段三：基于能量的匹配与优化。** 在规范空间中，通过双向能量损失 $\mathcal{L}_{\mathrm{E}}$ 进行最近邻匹配。每对高斯 $(g_i, g_j)$ 的能量由颜色距离、特征距离和规范空间距离的加权和定义：

$$E_{i,j} = w_c \|\mathbf{c}_i - \mathbf{c}_j\|_2^2 + w_f \|\mathbf{f}_i - \mathbf{f}_j\|_2^2 + w_\mu \|\hat{\boldsymbol{\mu}}_i - \hat{\boldsymbol{\mu}}_j\|_2^2$$

损失函数对两个方向取最近邻求和，确保双向覆盖：

$$\mathcal{L}_{\mathrm{E}} = \sum_{g_i \in \mathcal{G}_0} \min_{g_j \in \mathcal{G}_1} E_{i,j} + \sum_{g_j \in \mathcal{G}_1} \min_{g_i \in \mathcal{G}_0} E_{j,i}$$

同时引入局部等距损失 $\mathcal{L}_{\mathrm{iso}}$，约束每个高斯的 $k$ 近邻在变换前后距离不变，以保持局部刚性。总训练损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{E}} + \alpha \mathcal{L}_{\mathrm{iso}}$，其中 $\alpha$ 在训练过程中逐步增大。最后，通过联合渲染损失（$\mathcal{L}_{\mathrm{render}}$，含 L1 和 LPIPS）对高斯参数和 MLP 参数进行端到端微调。

**阶段四：运动插值与外推。** 利用学到的 SE(3) 变换，计算每个高斯从 $t=0$ 到 $t=1$ 的相对变换，并对旋转部分使用 SLERP 插值、平移部分使用线性插值，生成任意中间时刻 $t \in (0,1)$ 的运动状态。外推则通过 $t < 0$ 或 $t > 1$ 实现。

**输入输出流总结：** 输入为两个时刻的多视角图像；输出为连续时间轴上任意时刻的新视角渲染图像。中间产物包括预训练的 3DGS 模型、PCA-DINO 特征、学到的 SE(3) 变换场，以及规范空间中的点对应关系。

## 核心模块与公式推导

### 问题建模：直接匹配的困境

给定两个时间步 $t=0$ 和 $t=1$ 的 3D 高斯点云 $\mathcal{G}_0$ 和 $\mathcal{G}_1$，直观的插值思路是建立点对点对应关系。然而，在大运动下，基于局部最近邻的直接匹配会失败。论文通过一个“玩具”距离函数说明这一困境（Section 3.1, Eq. 1）：

$$D_{i,j}^{\mathrm{toy}} = w_c \|\pmb{c}_i - \pmb{c}_j\|_2^2 + w_f \|\pmb{f}_i - \pmb{f}_j\|_2^2 + w_\mu \|\pmb{\mu}_i - \pmb{\mu}_j\|_2^2$$

其中 $\pmb{c}$ 为颜色，$\pmb{f}$ 为语义特征，$\pmb{\mu}$ 为空间坐标，$w_c, w_f, w_\mu$ 为权重。该距离函数在颜色、语义和空间维度上加权求和，但当物体发生大幅度平移或旋转时，空间邻近性 $w_\mu$ 项会主导匹配，导致错误对应（如 Figure 1 所示）。

### 核心模块一：共享规范空间对齐

GMC 的核心思想是**不直接匹配原始空间中的点**，而是将两个时间步的高斯分别通过 SE(3) 变换映射到一个可学习的共享规范空间，使得对应的点在该空间中占据相同位置（Section 3.2, Eq. 2）：

$$\underbrace{R_i^{(0)} \pmb{\mu}_i^{(0)} + \pmb{t}_i^{(0)}}_{\hat{\pmb{\mu}}_i^{(0)}} = \underbrace{R_j^{(1)} \pmb{\mu}_j^{(1)} + \pmb{t}_j^{(1)}}_{\hat{\pmb{\mu}}_j^{(1)}}$$

其中 $R_i^{(0)}, \pmb{t}_i^{(0)}$ 是 $t=0$ 时刻高斯 $g_i$ 的旋转矩阵和平移向量，$\hat{\pmb{\mu}}_i^{(0)}$ 是其规范空间坐标。这一公式是 GMC 的理论基石——**将“找对应”问题转化为“学习变换”问题**。

### 核心模块二：一元势场 MLP

为实现上述对齐，GMC 为每个时间步学习一个**一元势场**（Unary Potential Field）$\mathcal{F}$，它是一个 MLP，输入为高斯均值 $\pmb{\mu}$ 和 PCA 降维后的 DINO 特征 $\tilde{\pmb{f}}$，输出为 SE(3) 变换（Section 3.2.1, Eq. 3）：

$$\mathcal{F}(\tilde{\pmb{f}}, \pmb{\mu}) = (\pmb{R}, \pmb{t})$$

其中旋转 $\pmb{R}$ 以四元数形式输出（$\mathbb{R}^4$），平移 $\pmb{t} \in \mathbb{R}^3$。两个时间步分别使用独立的 MLP $\mathcal{F}_0$ 和 $\mathcal{F}_1$（如 Figure 5 所示，包含 $\Theta_R$ 和 $\Theta_T$ 两个子网络）。

**关键设计**：
- **DINO 特征**：提供语义感知能力，使得语义相似的点（如同一物体的不同部位）倾向于获得一致的变换。消融实验证实，移除 DINO 输入会导致不合理的插值和错误的全局运动插值（Supplementary D）。
- **位置输入**：提供空间上下文，帮助区分空间位置不同但语义相似的点。移除位置输入同样导致错误的全局匹配（Supplementary D）。

### 核心模块三：双向能量损失

在规范空间中，GMC 通过能量函数定义高斯对之间的匹配代价（Section 3.2.2, Eq. 4）：

$$E_{i,j} = w_c \|\pmb{c}_i - \pmb{c}_j\|_2^2 + w_f \|\pmb{f}_i - \pmb{f}_j\|_2^2 + w_\mu \|\hat{\pmb{\mu}}_i - \hat{\pmb{\mu}}_j\|_2^2$$

与 Eq. 1 的关键区别在于：空间距离项使用**规范空间坐标** $\hat{\pmb{\mu}}$ 而非原始空间坐标 $\pmb{\mu}$。这意味着空间邻近性是在变换后的空间中衡量的，从而解耦了运动与匹配。

基于此能量函数，**双向能量损失**（Bidirectional Energy Loss）确保两个集合中的所有高斯都能找到对应（Section 3.2.2, Eq. 5）：

$$\mathcal{L}_{\mathrm{E}} = \sum_{g_i \in \mathcal{G}_0} \min_{g_j \in \mathcal{G}_1} E_{i,j} + \sum_{g_j \in \mathcal{G}_1} \min_{g_i \in \mathcal{G}_0} E_{j,i}$$

第一项从 $\mathcal{G}_0$ 到 $\mathcal{G}_1$ 的最近邻匹配，第二项反向匹配。梯度通过 $\min$ 操作反向传播到 MLP 参数，驱动变换网络学习将对应点拉到一起。

### 核心模块四：局部等距损失

为保持局部刚性、防止变换后的点云出现撕裂或漂浮物，GMC 引入**局部等距损失**（Local Isometry Loss）（Section 3.3, Eq. 7）：

$$\mathcal{L}_{\mathrm{iso}} = \frac{1}{kN} \sum_{g_i \in \mathcal{G}} \sum_{g_j \in \mathrm{NN}_i} \big| \|\pmb{\mu}_i - \pmb{\mu}_j\|_2^2 - \|\hat{\pmb{\mu}}_i - \hat{\pmb{\mu}}_j\|_2^2 \big|$$

其中 $\mathrm{NN}_i$ 是高斯 $g_i$ 的 $k$ 个最近邻，$N$ 为高斯总数。该损失约束每个高斯的局部邻域在变换前后保持距离不变，促进局部刚性运动。消融实验证实，移除该损失会导致插值中出现噪声漂浮物或模糊渲染（Supplementary D）。

### 核心模块五：全局运动恢复与插值

一旦学习了 SE(3) 变换，可以将 $t=0$ 的高斯通过规范空间映射到 $t=1$ 的位置（Section 3.2.3, Eq. 6）：

$$\pmb{\mu}_i^{(0),t=1} = \left(\pmb{R}_j^{(1)}\right)^{\top} \left(\pmb{R}_i^{(0)}\pmb{\mu}_i^{(0)} + \pmb{t}_i^{(0)} - \pmb{t}_j^{(1)}\right)$$

其中 $g_j$ 是 $g_i$ 在规范空间中的最近邻。对于连续插值，GMC 计算相对 SE(3) 变换，并在恒等变换与该相对变换之间进行 SLERP（球面线性插值），生成中间帧的运动。

### 联合优化

总训练损失为能量损失与局部等距损失的加权和（Section 3.3, Eq. 8）：

$$\mathcal{L} = \mathcal{L}_{\mathrm{E}} + \alpha \mathcal{L}_{\mathrm{iso}}$$

其中 $\alpha$ 在训练过程中逐步增大，先让网络学习大致的全局对应，再逐步加强局部刚性约束。此外，GMC 还通过渲染损失（L1 + LPIPS）联合微调高斯参数和 MLP 参数（Section 3.3, Eq. 9）：

$$\mathcal{L}_{\mathrm{render}} = \beta \mathcal{L}_{\mathrm{RGB}}(\pmb{I}_0, \hat{\pmb{I}}_0) + \mathcal{L}_{\mathrm{RGB}}(\pmb{I}_1, \hat{\pmb{I}}_1)$$

其中 $\beta$ 用于平衡两个时间步的渲染贡献，$\hat{\pmb{I}}_0, \hat{\pmb{I}}_1$ 为渲染图像。

## 实验与分析

### 实验设置与评估指标

GMC 在两个主要场景类别上进行评估：**合成全局运动场景**（8 个）和**合成局部运动场景**（6 个，来自 PAPR in Motion ），以及三个**真实世界全局运动场景**。所有实验均基于预定义的平滑性指标进行定量比较，包括 **SI-FID**（渲染图像平滑度）、**SI-EMD**（几何保真度）和 **SI-MPED**（几何平滑度）。由于缺乏真实运动轨迹，这些指标衡量的是插值序列的平滑性与一致性，而非轨迹的绝对准确性。

基线方法涵盖两类范式：基于变形场的方法——**4DGS** 和 **Deformable 3DGS**；基于迭代优化的方法——**Dynamic Gaussian** 和 **PAPR in Motion**。

### 合成全局运动场景的主结果

Table 1 报告了 8 个合成全局运动场景（Ball、Boat、Butterfly、Car、Dolphin、Knight、Microwave、Seagull）的平均指标。GMC 在所有指标上均显著优于基线：

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2508_20136/figures/007_Table_1.jpg]]
*Table 1: Scene Interpolation Evaluation. This table compares methods on synthetic global-motion scenes (“-” indicates failure). Our method achieves the lowest SI-FID and SI-MPED scores, indicating smoother interpolation of rendered images and geometry. In most scenes, our method also achieves lower SI-EMD scores, demonstrating better overall geometry fidelity*

- **SI-FID**: GMC 取得 224.42，相比最优基线 Dynamic Gaussian 的 283.53 降低了 **59.11**，降幅约 20.8%。
- **SI-MPED** (×10⁻³): GMC 为 16.47，Dynamic Gaussian 高达 824.50，GMC 实现了 **808.03** 的绝对降低，降幅达 98.0%，表明 GMC 生成的几何插值极为平滑。
- **SI-EMD**: GMC 为 149.38，在多数场景中优于基线，验证了整体几何保真度的提升。

值得注意的是，4DGS 和 Deformable 3DGS 在多个场景上完全失败（表中以“-”标记），说明基于变形场微调的方法在大的帧间运动下无法产生合理渲染。Figure 2 的定性结果进一步印证了这一点——在 Ball 和 Dolphin 场景中，Dynamic Gaussian 和 PAPR in Motion 产生了明显的伪影或模糊，而 GMC 的渲染保持了清晰的几何结构和运动轨迹。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2508_20136/figures/024_Figure.jpg]]

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2508_20136/figures/025_Figure.jpg]]

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2508_20136/figures/027_Figure.jpg]]

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2508_20136/figures/029_Figure.jpg]]

### 合成局部运动场景的结果

Table 2 报告了 6 个局部运动场景的平均指标。GMC 在 SI-FID 上取得 112.62，略优于 PAPR in Motion 的 117.94（降低 5.32）。这表明 GMC 不仅在大运动场景中具有压倒性优势，在局部运动场景中也保持了竞争力。详细的逐场景指标见补充材料 Table 7。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2508_20136/figures/008_Table_2.jpg]]
*Table 2: Synthetic Local-Motion Evaluation. Comparison of average metrics on synthetic local-motions scnees [20] against baselines*

### 真实世界场景的泛化能力

Table 3 报告了三个真实世界全局运动场景（Softball、Shoe、Box）的评估结果。GMC 的平均 SI-FID 为 166.33，而 Dynamic Gaussian 为 308.65，GMC 降低了 **142.32**（降幅 46.1%）。Figure 3 的定性对比直观地展示了这一差距：在 Softball 场景中，Dynamic Gaussian 完全丢失了棒球棒，而 GMC 在所有时间步（0.00 到 1.00）均保持了物体的完整性和运动连续性。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2508_20136/figures/011_Table_3.jpg]]
*Table 3: Real-World Global-Motion Evaluation. Comparison of our method with the baselines on real-world scenes with global motion (“-” indicates failure). Overall, our method outperforms the baselines in rendering quality and geometry fidelity. Table 4. Ablation Study. Average metrics on synthetic globalmotion scenes for various model variants are reported to reveal the impact of each method component on interpolation performance*

Figure 7 展示了 Box 场景中 GMC 同时处理全局与局部运动的能力——箱子整体经历全局位移，而箱盖呈现局部开合运动。GMC 准确捕捉了两类运动，生成了逼真的插值序列。

### 消融实验

Table 4 的消融研究系统性地验证了各模块的贡献。完整模型在所有指标（SI-FID、SI-EMD、SI-MPED）上均取得最优结果。关键发现如下：

1. **移除 DINO 特征输入**：导致插值不合理（Ball 场景）、全局运动插值错误（Boat 场景）或局部运动插值错误。这验证了语义特征在建立鲁棒对应中的核心作用——纯几何和颜色信息不足以区分大运动下的正确匹配。
2. **移除位置输入**：导致错误的全局匹配或错误的局部运动插值，表明空间坐标对于约束变换的几何一致性不可或缺。
3. **移除局部等距损失**：导致插值中出现噪声漂浮物或模糊渲染。该损失通过约束近邻点在变换前后距离不变，强制局部刚性，是消除伪影的关键正则项。

### 稀疏视图下的新视角合成

GMC 的变换学习机制还带来了一个额外收益：通过联合优化渲染损失，GMC 能改善 3DGS 在稀疏视图下的重建质量。Table 5 报告了稀疏-密集视图设置（起始状态 100 视图，终止状态 10 或 5 视图）的结果，GMC 在 PSNR、SSIM 和 LPIPS 上均显著优于 vanilla 3DGS。Table 6 进一步验证了在稀疏-稀疏视图设置（双方均仅有 5-10 个训练视图）下的改进。Figure 8 的定性结果展示了这一提升的视觉效果。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2508_20136/figures/012_Table_5.jpg]]
*Table 5: Novel View Synthesis for Sparse-Dense View Setting. For the synthetic scenes, the start state has 100 dense training views, while the end state has 10 sparse training views. For real-world scenes (Shoe, tapeline, and Box), the end state has 5 sparse training views. The results are reported as the mean value of test views for each scene*

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2508_20136/figures/014_Table_6.jpg]]
*Table 6: Novel View Synthesis in Sparse + Sparse View Setting. For the scenes Car and Microwave, both states have 10 training views; for Box, both states have 5 training views. The results are reported as the mean value of test views for each scene*

### 失败模式与局限性

尽管 GMC 在大运动场景中表现出色，其性能仍受以下因素制约：

- **对初始重建质量的依赖**：GMC 假设输入的两个时间步的 3DGS 重建是高质量的。稀疏或噪声输入会降低对应质量，进而影响插值效果。
- **超参数敏感性**：训练涉及多个阶段和超参数（α 逐步增大、k 近邻数量、能量项权重 w 等），可能需要针对新场景进行一定调整。
- **两帧限制**：当前方法仅限于在两个已知状态之间进行插值和外推，未处理连续多帧或高度动态的长序列。

### 补充图表

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2508_20136/figures/017_Table.jpg]]

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2508_20136/figures/010_Table.jpg]]

## 方法谱系与知识库定位

### 核心瓶颈：大运动下的点对应失效

现有基于点的动态场景插值方法在局部、小幅运动下表现良好，但在大的全局运动下会系统性失效。其根本瓶颈在于：当帧间运动幅度超出局部邻域范围时，基于最近邻的点对应关系变得不可靠。Figure 1 清晰地展示了这一挑战——左侧的小运动场景中，局部邻域搜索可以找到正确的对应点；中间的大运动场景中，同样的策略会导致错误的匹配。GMC 的核心洞察是**用一元势场预测每个高斯的 SE(3) 变换来取代直接的点对点匹配**，从而在无需真实运动轨迹的情况下建立平滑的全局对应。

### 与现有方法的差异

现有动态场景插值方法可大致分为两类，GMC 在多个关键维度上与它们有本质区别：

**基于变形场的方法**（如 4DGS、Deformable 3DGS）通过在 3DGS 上学习变形网络来建模运动。这些方法依赖局部最近邻的空间匹配或变形场微调来建立点对应，在大运动下同样面临对应失效的问题。GMC 则通过共享规范空间中的能量损失学习全局对应，绕开了局部匹配的局限。

**基于迭代优化的方法**（如 Dynamic Gaussian、PAPR in Motion）直接预测位移或变形，优化目标仅依赖渲染损失。GMC 在以下四个关键维度上做出了改变：

| 设计维度 | 基线方法 | GMC 的改进 |
|---------|---------|-----------|
| 点对应建立方式 | 基于局部最近邻的空间匹配或变形场微调 | 通过共享规范空间中的能量损失学习全局对应 |
| 语义特征利用 | 无额外语义特征或仅用颜色 | 使用 PCA 降维的 DINO 特征引导变换网络 |
| 运动表示 | 直接预测位移或变形 | 预测每个高斯的 SE(3) 变换（旋转和平移） |
| 优化目标 | 仅渲染损失 | 引入双向能量损失和局部等距损失，并联合优化渲染损失 |

这些改变的因果链条是清晰的：DINO 语义特征提供了超越颜色和空间位置的外观不变性，使得语义相似的区域（如物体的不同部分）在规范空间中能被正确对齐；SE(3) 变换表示赋予了运动以刚体约束的先验，避免了无约束位移预测的歧义性；双向能量损失确保了所有点都找到对应，而非仅部分点；局部等距损失则进一步约束近邻点在变换后距离不变，促进局部刚性。

### 证据强度与边界

**强证据支持**：在合成全局运动场景上，GMC 在 SI-FID（224.42 vs. 283.53）和 SI-MPED（16.47 vs. 824.50）上显著优于 Dynamic Gaussian，且在大多数场景上 SI-EMD 也更低（Table 1）。在真实世界全局运动场景上，SI-FID 从 308.65 降至 166.33（Table 3）。消融实验（Table 4）进一步验证了 DINO 特征、位置输入和局部等距损失各自的关键作用——移除 DINO 输入会导致不合理的插值和错误的全局运动插值。

**适用边界**：GMC 假设输入的两个时间步的 3D 高斯重建是高质量的，稀疏或噪声输入会降低对应质量。目前仅限于在两个已知状态之间进行插值和外推，未处理连续多帧或高度动态的序列。在局部运动场景上，GMC 的优势相对收敛（SI-FID 112.62 vs. PAPR in Motion 的 117.94），表明当运动幅度较小时，现有方法的局部匹配策略已足够有效，GMC 的全局对应机制带来的增益有限。

### 局限与开放问题

1. **多阶段训练的复杂性**：训练过程涉及 3DGS 预训练、一元势场 MLP 训练、能量损失优化、联合渲染微调等多个阶段，且包含逐步增大的 α、k、w 等超参数，针对新场景可能需要一定的调整。这限制了方法的即插即用性。

2. **多帧扩展的挑战**：当前方法仅处理两个离散状态之间的插值。能否将 GMC 拓展到多于两个时间步的连续运动插值，是一个开放问题。可能的路径包括学习时间条件的一元势场，或在规范空间中建立时序一致性约束。

3. **稀疏视角的鲁棒性**：在极度稀疏视角（如单视角动态视频）下，3DGS 重建本身的质量会显著下降，进而影响 GMC 的对应质量。该方法是否仍能有效恢复运动，尚待验证。

4. **规范空间与高斯参数的一体化**：共享规范空间的学习目前与高斯参数的优化是分离的。是否可以进一步耦合以提升紧凑性和端到端的可训练性，是一个值得探索的方向。

5. **评估指标的局限性**：所有评估基于预定义的平滑性指标（SI-FID、SI-EMD、SI-MPED），由于缺乏真实运动轨迹，无法评估轨迹的绝对准确性。这意味着 GMC 的“正确性”实际上是“视觉平滑性”的代理，而非几何真值的验证。

## 原文 PDF

![[paperPDFs/ICCV_2025/Global_Motion_Corresponder_for_3D_Point_Based_Scene_Interpolation_under_Large_Motion.pdf]]
