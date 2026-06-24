---
title: Implicit 4D Gaussian Splatting for Fast Motion with Large Inter-Frame Displacements
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Implicit_4D_Gaussian_Splatting_for_Fast_Motion_with_Large_Inter_Frame_Displaceme_a038d3b5b498.pdf
project_link: null
code_link: null
aliases:
- S4
- I4GSFMLIFD
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将Gaussian属性学习从时空共享参数中解耦，改用显式时空位置（x, y, z, t）作为输入，通过前馈隐式网络直接预测每帧的属性，消除跨帧属性耦合。
primary_logic: 通过将Gaussian属性视为时空位置的隐式函数，用轻量级网络从逐帧显式位置中解码属性，实现了属性学习的去耦合，使快速运动物体即使在大位移下也能保持稳定且高质量的渲染，同时避免内存爆炸。
claims:
- SPIN-4DGS在CMU Panoptic Sports数据集上平均PSNR 30.11 dB，比最强基线D3DGS（28.70 dB）高+1.41 dB，且在Basketball场景上比D3DGS高+1.83 dB。
- 消融实验证实时空切片策略（即按(x,y,z,t)显式分离Gaussian，每帧仅使用对应时间步的点）是避免交叉帧干扰的关键，去除切片后PSNR明显下降。
- 输入位置归一化（Mip-NeRF contraction）使PSNR提升超过10 dB，证明了坐标变换对稳定训练的重要性。
- CMU Panoptic Sports 上 PSNR (平均) = 30.11
---

# Implicit 4D Gaussian Splatting for Fast Motion with Large Inter-Frame Displacements

> [!tip] 核心洞察
> 通过将Gaussian属性视为时空位置的隐式函数，用轻量级网络从逐帧显式位置中解码属性，实现了属性学习的去耦合，使快速运动物体即使在大位移下也能保持稳定且高质量的渲染，同时避免内存爆炸。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向大帧间位移快速运动的隐式四维高斯泼溅 |
| 英文题名 | Implicit 4D Gaussian Splatting for Fast Motion with Large Inter-Frame Displacements |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=MWtXs60n38) · [arXiv](https://arxiv.org/abs/2510.03857) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SPIN-4DGS |
| Dataset | CMU Panoptic Sports, CMU Panoptic Sports - Basketball, CMU Panoptic Sports - Tennis, Neu3DV |

> [!tip] 效果简介
> - CMU Panoptic Sports 上，PSNR (平均) 30.11 vs 28.70 (D3DGS) (+1.41)。
> - CMU Panoptic Sports - Basketball 上，PSNR 30.05 vs 28.22 (D3DGS) (+1.83)。
> - CMU Panoptic Sports - Tennis 上，PSNR 30.14 vs 28.50 (Realtime-4DGS) (+1.64)。

## 概述

### 问题背景

动态场景重建在虚拟现实、增强现实和体育分析等领域具有重要应用。近年来，4D高斯泼溅（4D Gaussian Splatting, 4DGS）方法凭借其高质量的实时渲染能力成为该领域的主流范式。然而，现有4DGS方法在处理**具有大帧间位移的快速运动**时面临严重挑战：快速运动物体（如球拍、篮球）在训练过程中逐渐模糊甚至消失，而静态背景却保持清晰。

这一现象的根本原因在于**交叉帧干扰（cross-frame interference）**：现有方法中，Gaussian的属性（颜色、尺度、旋转、不透明度）在多个时间步上共享参数，导致快速运动物体的属性优化受到静态背景主导，不同帧之间的属性更新相互冲突，最终造成物体崩溃。无论是显式参数化方法（如**Realtime-4DGS**, Yang et al., 2024a; **4D-Rotor-Gaussians**, Duan et al., 2024）还是可变形方法（如**4DGaussian**, Wu et al., 2024; **Grid4D**, Xu et al., 2024; **MoDec-GS**, Kwak et al., 2025），均存在此问题（Figure 2）。

### 核心方法：SPIN-4DGS

本文提出**SPIN-4DGS**（Spatiotemporal Implicit Network for 4DGS），核心思路是将Gaussian属性学习从时空共享参数中**解耦**：不再让属性跨帧共享，而是将属性视为时空坐标 $(x, y, z, t)$ 的隐式函数，通过轻量级前馈网络逐帧预测。

方法包含两个阶段（Figure 3）：
1. **时空位置估计**：先利用显式4DGS获取初步的逐帧Gaussian位置，再通过光栅化损失精炼，稠密化显著点并剪枝冗余点。
2. **隐式网络属性预测**：将精炼后的位置经Mip-NeRF收缩归一化后，输入4D哈希编码器和多分支MLP解码器，直接输出每帧的Gaussian属性。

这种设计消除了跨帧属性耦合，使快速运动物体在大位移下也能保持稳定渲染，同时仅需存储位置和网络参数（1261 MB），避免显式存储全部属性的内存爆炸。

### 主要结果

在**CMU Panoptic Sports**数据集的六个高动态体育场景上，SPIN-4DGS平均PSNR达到**30.11 dB**，比最强基线**D3DGS**（28.70 dB, Luiten et al., 2024）高出**+1.41 dB**，其中Basketball场景领先**+1.83 dB**。值得注意的是，D3DGS依赖外部分割掩码监督，而SPIN-4DGS在无任何外部监督的情况下取得此优势。在Neu3DV和MeetRoom数据集上，SPIN-4DGS同样达到或超越现有方法。

消融实验证实了两个关键设计的作用：**时空切片**策略将Gaussian按帧分离，消除了交叉帧干扰，使PSNR从28.96提升至30.05；**输入位置归一化**（Mip-NeRF contraction）使PSNR提升超过10 dB，证明了坐标变换对稳定训练的关键性。

### 方法谱系与知识库定位

SPIN-4DGS处于**4D高斯泼溅**与**隐式神经表示**的交叉点。与现有4DGS方法相比，其独特之处在于：

| 维度 | 现有4DGS | SPIN-4DGS |
|------|----------|-----------|
| 属性学习 | 跨帧共享或从规范空间变形 | 前馈隐式网络从 $(x,y,z,t)$ 逐帧预测 |
| 位置表示 | 统一4D原语或变形场 | 显式逐帧位置 + 时空切片 |
| 内存效率 | 显式存储所有属性（如D3DGS需1994 MB） | 仅存位置和网络参数（1261 MB） |

该方法与**3DGS逐帧独立优化**（Kerbl et al., 2023）的区别在于：SPIN-4DGS使用时间共享的隐式场，能够利用帧间时序规律，比独立逐帧模型更连贯（平均PSNR高出+1.9 dB, Table 10）。其隐式解码器设计借鉴了**NeRF**系列的位置编码思想，但直接作用于Gaussian属性预测而非辐射场。

## 背景与动机

### 动态场景重建的核心挑战

三维场景的自由视点渲染是计算机视觉与图形学中的基础问题。近年来，三维高斯泼溅（3D Gaussian Splatting, 3DGS）（Kerbl et al., 2023）凭借其高保真重建与实时渲染能力，在静态场景中取得了突破性进展。然而，将其直接扩展至动态场景——即四维高斯泼溅（4DGS）——面临着根本性的困难：场景中的物体随时间运动，高斯原语（Gaussian primitives）的属性（位置、颜色、尺度、旋转、不透明度）必须随帧变化，而如何高效且稳定地建模这种时间依赖性，是当前方法的核心瓶颈。

### 现有方法的失败模式：大帧间位移下的属性崩溃

现有4DGS方法可大致分为两类：**显式参数化方法**（如Realtime-4DGS、4D-Rotor-Gaussians）与**可变形方法**（如4DGaussian、Grid4D、MoDec-GS）。尽管它们在常规运动中表现尚可，但在**具有大帧间位移的快速运动场景**中，两类方法均出现严重的渲染退化。

Figure 2 直观展示了这些失败模式。在显式参数化框架中（Figure 2a），随着训练迭代增加（15K → 30K），快速运动物体的高斯属性逐渐崩溃：球拍、球体等目标变得模糊甚至消失。这是因为显式方法中，高斯属性在多个时间步上共享参数，快速运动物体在不同帧间的位置变化剧烈，其属性梯度在共享参数空间中相互干扰——即**交叉帧干扰**（cross-frame interference）。静态背景主导了优化过程，运动物体的信号被淹没。

可变形方法（Figure 2b）同样遭遇困境。这类方法通常维护一个规范空间（canonical space）的静态表示，再通过变形场将其映射到各帧。然而，当帧间位移过大时，规范空间初始化无法为快速运动物体分配足够的高斯原语——变形场难以在规范空间中找到对应点来“搬运”到目标位置，导致快速物体在渲染中缺失或严重失真。

### 瓶颈分析：属性耦合是根本原因

两类方法的共同症结在于**属性学习的耦合性**：

- **显式方法**：所有时间步共用一组高斯属性，快速运动物体的属性被迫与静态背景及其他时间步的自身属性共享参数，优化时梯度相互干扰。
- **可变形方法**：虽然变形场提供了逐帧的位置调整，但高斯属性（颜色、尺度等）仍从规范空间继承，本质上仍存在跨帧属性共享。

这种耦合导致了一个恶性循环：快速运动需要大幅调整属性，但共享参数机制抑制了这种调整，使得优化偏向于占主导的静态背景，快速物体逐渐被“遗忘”。

### 本文动机：将属性学习解耦为时空位置的隐式函数

核心洞察在于：**高斯属性不应跨帧共享，而应视为时空位置的隐式函数**。给定一个时空坐标 $(x, y, z, t)$，其对应的高斯属性（颜色、尺度、旋转、不透明度）应当由该坐标唯一确定，而非从其他时间步继承。这样，每个时间帧的每个高斯原语都拥有独立的属性预测，彻底消除交叉帧干扰。

基于这一洞察，本文提出 **SPIN-4DGS**（Spatiotemporal Position-based Implicit Network for 4DGS），其核心思想是：

1. **显式获取逐帧时空位置**：先通过显式4DGS基线获取全场景的粗粒度时空位置，再通过逐帧光栅化损失精炼，得到高质量的位置集合 $(x, y, z, t)$。
2. **隐式网络预测属性**：使用轻量级前馈网络 $f_\theta(\mathbf{x}, \mathbf{y}, \mathbf{z}, \mathbf{t})$ 直接从时空坐标解码高斯属性，属性不跨帧共享，彻底解耦。
3. **时空切片**：按 $(x, y, z, t)$ 将高斯原语分离至各帧，每帧仅使用属于当前时间步的点，避免无关帧的干扰。

这一设计将属性学习从“跨帧共享参数”的耦合模式转变为“逐帧独立解码”的去耦合模式，使快速运动物体即使在大位移下也能保持稳定且高质量的渲染，同时避免了显式存储全部属性所导致的内存爆炸。

## 核心创新

SPIN-4DGS 的核心创新在于**将 Gaussian 属性学习从时空耦合的参数化中彻底解耦**，转而采用一种隐式前馈网络直接从显式的时空位置坐标中解码属性。这一设计直接针对现有 4DGS 方法在快速运动场景中的根本性瓶颈——**交叉帧干扰**。

### 瓶颈洞察：交叉帧干扰与属性崩溃

在具有大帧间位移的快速运动场景（如球类运动）中，现有 4DGS 方法面临严重的属性学习崩溃问题。具体而言：
- **显式参数化方法**（如 Realtime-4DGS、4D-Rotor-Gaussians）将 Gaussian 属性在多个时间步上跨帧共享，导致静态背景主导优化过程，快速运动物体的属性因同时表示多个时刻的状态而相互干扰。
- **可变形方法**（如 4DGaussian、Grid4D、MoDec-GS）从规范空间变形并共享属性，但在快速运动下，规范空间难以正确分配 Gaussian 来覆盖大位移物体，导致物体模糊或消失。

这两种范式共同的失败根源在于：**Gaussian 属性在时间维度上存在耦合**，使得快速运动物体的特征被静态背景或相邻帧的冲突信号淹没。

### 因果调控旋钮：从时空坐标直接解码属性

SPIN-4DGS 的核心调控旋钮是将属性学习转化为一个**以显式时空位置为输入的前馈预测问题**：

$$u_t = f_{\theta}(\mathbf{x}, \mathbf{y}, \mathbf{z}, \mathbf{t}), \quad \mathbf{c}_t = g_{\phi}(\mathbf{x}, \mathbf{y}, \mathbf{z}, \mathbf{t})$$

具体而言，方法构建逐帧的显式时空位置 $(x, y, z, t)$，并通过**时空切片**策略仅保留当前帧相关的 Gaussian，然后使用轻量级隐式网络 $f_\theta(\mathbf{x}, t)$ 直接从归一化的四维坐标中预测每帧的属性（RGB、尺度、旋转、不透明度）。这一设计实现了三个关键改变：

| 设计维度 | 现有方法 | SPIN-4DGS |
|---------|---------|-----------|
| **属性学习方式** | 可变形：从规范空间变形并共享属性；显式：在4D原语上时间切片，属性跨帧共享 | 使用前馈隐式网络从时空坐标直接预测每帧属性，**属性不跨帧共享** |
| **Gaussian位置表示** | 可变形：规范空间位置经变形得到帧位置；显式：所有时间步共用一组位置 | 构建逐帧显式时空位置，通过先获取后逐帧精炼得到高质量位置，**时空切片仅保留当前帧相关Gaussian** |
| **参数存储效率** | 显式存储所有Gaussian的全部属性（如D3DGS需1994 MB） | 仅存储Gaussian位置和网络参数（1261 MB），**属性由网络动态生成** |

### 隐式属性解码的技术实现

SPIN-4DGS 的隐式网络由三个关键组件构成：

1. **位置归一化**：采用 Mip-NeRF 收缩策略将无界空间坐标映射到 $[0,1]^3$，时间归一化到 $[0,1]$，形成归一化四维输入 $\tilde{\mathbf{x}} = [\bar{\mu}^\top, t_{\mathrm{norm}}]^\top \in [0,1]^4$。消融实验证实这一步骤对训练稳定性至关重要，使 PSNR 提升超过 10 dB（Table 5）。

2. **四维哈希编码器**：使用多层四维哈希网格将归一化时空坐标编码为紧凑的隐式表示 $\mathbf{z} \in \mathbb{R}^{L \times F}$，为后续解码提供丰富的多分辨率特征。

3. **多分支属性解码器**：三个三层 MLP 头分别预测尺度、旋转、SH 系数和不透明度，并通过特定的后处理与初始化（如不透明度偏置初始化为 $\mathrm{logit}(0.1) \approx -2.197$）保证训练稳定。

### 创新有效性验证

消融实验系统性地验证了核心创新的有效性：
- **时空切片**：将统一 4D 形式（无切片）与逐帧切片策略对比，PSNR 从 28.96 提升至 30.05，证实消除交叉帧干扰是性能提升的关键（Table 3）。
- **兼容性验证**：使用预训练的其他 4DGS 位置（D3DGS/Realtime-4DGS）并仅替换属性学习方案，SPIN-4DGS 仍能大幅提升 PSNR（如 D3DGS 位置在 Softball 场景上 +2.49 dB），证明隐式属性学习方案本身的有效性与通用性（Table 4）。

综上，SPIN-4DGS 通过将 Gaussian 属性重新定义为时空位置的隐式函数，从根本上消除了跨帧属性耦合，使快速运动物体即使在大位移下也能保持稳定且高质量的渲染，同时避免了显式存储全部属性带来的内存爆炸。

## 整体框架

SPIN-4DGS 的整体框架由两个核心阶段构成，其设计目标是从根本上解决现有 4DGS 方法在大帧间位移快速运动场景下的属性崩溃问题。

### 核心设计动机

现有 4DGS 方法在快速运动场景中面临严重的交叉帧干扰：显式参数化方法（如 Realtime-4DGS、4D-Rotor-Gaussians）中，同一组 Gaussian 需要在多个时间步上共享属性，导致训练后期出现剧烈退化（Figure 2a）；可变形方法（如 4DGaussian、Grid4D）的规范空间初始化则难以在大位移下为快速运动物体分配足够的 Gaussian（Figure 2b）。SPIN-4DGS 的核心洞察是：**将 Gaussian 属性学习从时空共享参数中解耦**，通过将属性视为时空位置的隐式函数，用前馈网络从逐帧显式位置中解码，从而消除跨帧属性耦合。

### 两阶段 Pipeline

SPIN-4DGS 的完整流程如 Figure 3 所示，分为以下两个阶段：

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_MWtXs60n38/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of the overall framework. SPIN-4DGS consists of two stages of (a) Spatiotemporal Position Estimation and (b) Implicit Network for 4DGS. Specifically, (a) we slice Gaussians along the temporal axis to obtain spatiotemporal position sets and refine them with rasterization loss. Then, (b) the refined positions are normalized and passed through a 4D hash encoder and multibranch decoders to predict Gaussian attributes (scale, rotation, color, and opacity)*

**阶段一：时空位置估计（Spatiotemporal Position Estimation）**

该阶段负责为每一帧获取高质量的 Gaussian 位置。具体流程为：

1. **初始位置获取**：默认使用显式 4DGS 方法 **Realtime-4DGS**（Yang et al., 2024a）进行初步训练，获取全场景的时空位置集合。
2. **时空切片**：沿时间轴对 Gaussian 进行切片，将每个 Gaussian 按 $(x, y, z, t)$ 显式分配到对应帧，仅保留当前时间步相关的点。这一步是消除交叉帧干扰的关键设计（消融实验证实，去除切片后 PSNR 从 30.05 降至 28.96）。
3. **逐帧精炼**：利用光栅化损失对每帧的位置进行细化，稠密化显著点、剪枝冗余点，提升位置质量。

**阶段二：隐式网络属性预测（Implicit Network for 4DGS）**

该阶段使用轻量级前馈网络从精炼后的时空位置中动态预测 Gaussian 属性，避免属性跨帧共享。具体流程为：

1. **位置归一化**：采用 Mip-NeRF 收缩策略将无界空间坐标映射到 $[0,1]^3$，时间归一化到 $[0,1]$，拼接为四维输入 $\tilde{\mathbf{x}} = [\bar{\mu}^\top, t_{\text{norm}}]^\top \in [0,1]^4$。
2. **四维哈希编码**：使用 16 层、每层 4 通道的 4D 哈希网格将归一化坐标编码为隐式表示 $\mathbf{z} \in \mathbb{R}^{L \times F}$。
3. **多分支属性解码**：三个三层 MLP 头分别预测尺度 $\hat{\mathbf{s}}$、旋转 $\hat{\mathbf{r}}$、SH 系数 $\hat{\mathbf{sh}}$ 和不透明度 $\hat{\mathbf{o}}$，各分支采用特定的后处理与初始化以保证训练稳定（如不透明度分支的偏置初始化为 $\text{logit}(0.1) \approx -2.197$）。
4. **光栅化与损失**：使用标准 3DGS 光栅化渲染图像，优化组合损失 $\mathcal{L} = (1 - \lambda) \mathcal{L}_1 + \lambda \mathcal{L}_{\text{D-SSIM}}$（$\lambda = 0.2$）。

### 关键设计要点

| 设计要素 | 传统 4DGS | SPIN-4DGS |
|---------|----------|-----------|
| 属性学习方式 | 跨帧共享参数（可变形或显式切片） | 前馈隐式网络 $\mathbf{f}_\theta(\mathbf{x}, \mathbf{y}, \mathbf{z}, \mathbf{t})$ 逐帧预测 |
| 位置表示 | 规范空间 + 变形 / 全时间步共用 | 逐帧显式位置 + 时空切片 |
| 参数存储 | 显式存储所有属性（如 D3DGS 需 1994 MB） | 仅存储位置和网络参数（1261 MB） |

消融实验证实了两个关键设计的必要性：输入位置归一化使 PSNR 提升超过 10 dB（LPIPS 从 0.45 降至 0.16），是稳定训练的前提；时空切片则通过将 Gaussian 按帧显式分离，从根本上消除了交叉帧干扰。兼容性实验进一步表明，即使复用其他 4DGS 方法（如 D3DGS）的预训练位置，仅替换为 SPIN-4DGS 的隐式属性学习方案，仍能大幅提升 PSNR（例如在 Softball 场景上提升 +2.49 dB），验证了隐式属性学习方案的有效性与通用性。

## 核心模块与公式推导

SPIN-4DGS 的核心设计思想是将 4D Gaussian 的属性学习从时空耦合的参数化中解耦，转而通过一个前馈隐式网络从显式的时空位置直接解码属性。整个框架由两个阶段构成：**时空位置估计** 和 **隐式网络属性预测**。

### 3D Gaussian 基础表示

在介绍核心模块之前，先回顾 3D Gaussian Splatting 的基础公式。一个三维高斯函数定义为：

$$G^{3D}(\mathbf{x}) = \exp\left(-\frac{1}{2}(\mathbf{x} - \pmb{\mu})^{\top} \pmb{\Sigma}_{3D}^{-1} (\mathbf{x} - \pmb{\mu})\right)$$

其中 $\pmb{\mu}$ 为高斯中心，$\pmb{\Sigma}_{3D}$ 为三维协方差矩阵。为保证协方差矩阵的半正定性，将其分解为旋转矩阵 $\mathbf{R}$ 和对角尺度矩阵 $\mathbf{S}$：

$$\pmb{\Sigma}_{3D} = \mathbf{R} \mathbf{S} \mathbf{S}^{\top} \mathbf{R}^{\top}$$

渲染时，三维协方差投影到二维图像平面：

$$\pmb{\Sigma}_{2D} = \mathbf{J} \mathbf{W} \pmb{\Sigma}_{3D} \mathbf{W}^{\top} \mathbf{J}^{\top}$$

其中 $\mathbf{J}$ 为投影变换的雅可比矩阵，$\mathbf{W}$ 为视角变换矩阵。最终像素颜色通过 alpha 混合计算：

$$\alpha_i' = o_i G_i^{2D}(\mathbf{x}), \quad \mathbf{C}(\mathbf{x}) = \sum_{i=1}^{N} c_i \alpha_i' \prod_{j=1}^{i-1} (1 - \alpha_j')$$

### 阶段一：时空位置估计

SPIN-4DGS 首先需要获取每帧的显式 Gaussian 位置。默认采用显式 4DGS 方法 **Realtime-4DGS**（Yang et al., 2024a）进行初步估计，得到全场景的时空位置集合。

随后，利用光栅化损失对每帧的位置进行逐帧精炼，通过稠密化显著点和剪枝冗余点来提升位置质量：

$$u _ { t } \gets \mathrm { R e f i n e } \big ( u _ { t } , \mathbf { c } _ { t } ; t \big ) , \qquad t = 0 , \ldots , T$$

该精炼步骤是保证后续属性学习质量的关键：即使仅使用 0.5K 次迭代精炼，SPIN-4DGS 仍能保持一致的物体结构而不发生崩溃；随着迭代次数增加，可逐步恢复细节（如球边缘和球拍网线）。

### 阶段二：隐式网络属性预测

这是 SPIN-4DGS 的核心创新。传统方法中，Gaussian 属性（颜色、尺度、旋转、不透明度）要么在规范空间共享后经变形得到，要么在 4D 原语上跨时间步共享。SPIN-4DGS 则将这些属性视为时空位置的隐式函数，通过一个轻量级前馈网络逐帧解码。

**位置归一化**：首先将无界空间坐标通过 Mip-NeRF 收缩策略映射到 $[0,1]^3$：

$$\operatorname { c o n t r a c t } ( \mu ) = \left\{ \begin{array} { l l } { \mu , } & { \parallel \mu \parallel \leq 1 , } \\ { \left( 2 - \frac { 1 } { \parallel \mu \parallel } \right) \frac { \mu } { \parallel \mu \parallel } , } & { \parallel \mu \parallel > 1 } \end{array} \right.$$

$$\hat { \mu } = \frac { 1 } { 4 } \operatorname { c o n t r a c t } ( \mu ) + \frac { 1 } { 2 } \in [ 0 , 1 ] ^ { 3 }$$

时间坐标同样归一化到 $[0,1]$，并与空间坐标拼接为四维输入：

$$t _ { \mathrm { n o r m } } = \frac { t - t _ { \mathrm { m i n } } } { t _ { \mathrm { m a x } } - t _ { \mathrm { m i n } } } \in [ 0 , 1 ], \quad \tilde { \bf x } = \left[ \bar { \mu } ^ { \top } , t _ { \mathrm { n o r m } } \right] ^ { \top } \in [ 0 , 1 ] ^ { 4 }$$

消融实验证实，这一归一化步骤对稳定训练至关重要：去除后 PSNR 下降超过 10 dB，LPIPS 从 0.16 恶化至 0.45。

**四维哈希编码器**：归一化的时空坐标通过一个 4D 哈希网格编码为紧凑隐式表示。编码器采用 16 层、每层 4 通道的配置：

$$z = \mathrm { f } _ { e n c } ( \tilde { \mathbf { x } } ) \in \mathbb { R } ^ { L \times F }$$

其中 $L$ 为层数，$F$ 为每层通道数。

**多分支属性解码器**：从编码器输出 $z$ 出发，三个三层 MLP 头分别预测不同的 Gaussian 属性：

$$( \hat { \mathbf { s } } , \hat { \mathbf { r } } , \hat { \mathbf { s h } } , \hat { \mathbf { o } } ) = \big ( f _ { \mathrm { s c a l e } } ( \mathbf { z } ) , ~ f _ { \mathrm { r o t } } ( \mathbf { z } ) , ~ f _ { \mathrm { s h } } ( \mathbf { z } ) , ~ f _ { \mathrm { o p a c i t y } } ( \mathbf { z } ) \big )$$

其中 $\hat{\mathbf{s}}$ 为尺度，$\hat{\mathbf{r}}$ 为旋转，$\hat{\mathbf{sh}}$ 为球谐系数（颜色），$\hat{\mathbf{o}}$ 为不透明度。各解码器采用特定的后处理与初始化策略以保证训练稳定：例如不透明度解码器的最后一层偏置初始化为 $\mathrm{logit}(0.1) \approx -2.197$（可训练），使初始 $\hat{o} \approx 0.1$，网络随后学习仅在需要的地方增大不透明度。

**训练损失**：使用标准 3DGS 的组合损失函数进行端到端训练：

$$\mathcal { L } = \left( 1 - \lambda \right) \mathcal { L } _ { 1 } + \lambda \mathcal { L } _ { \mathrm { D - S S I M } }$$

其中 $\lambda = 0.2$。

### 时空切片机制

SPIN-4DGS 的一个关键实现细节是**时空切片**：在每帧渲染时，仅保留当前时间步对应的 Gaussian 点，过滤掉其他时间步的点。这一机制显式地将 Gaussian 按 $(x, y, z, t)$ 分离，消除了跨帧属性干扰——这正是现有方法在快速运动场景中失败的根本原因。消融实验表明，去除切片后 PSNR 从 30.05 降至 28.96，且训练时间与内存显著增加。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_MWtXs60n38/figures/002_Figure_2.jpg]]
*Figure 2: Failure modes on fast motions with large inter-frame displacements. We visualize failure modes of existing frameworks; (2a) explicit parameterization and (2b) deformable methods. Figure (2a) shows drastic degradation on training iterations (i.e., 15K → 30K), and (2b) shows the canonical space of deformable initialization fails to assign Gaussians for fast motions*

## 实验与分析

### 核心性能对比

在CMU Panoptic Sports数据集上，SPIN-4DGS在所有六个体育场景中均取得最优PSNR（Table 1），平均PSNR达到**30.11 dB**，比最强基线**D3DGS**（Luiten et al., 2024）的28.70 dB高出**+1.41 dB**。其中，在Basketball场景上提升尤为显著（+1.83 dB），在Tennis场景上比**Realtime-4DGS**（Yang et al., 2024a）高出+1.64 dB。SSIM方面，SPIN-4DGS平均达到0.93，同样优于所有对比方法。值得注意的是，SPIN-4DGS在训练过程中**不使用任何外部监督**（如分割掩码），而D3DGS等基线依赖此类监督信号，这进一步凸显了方法的自监督优势。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_MWtXs60n38/figures/004_Table_1.jpg]]
*Table 1: Comparisons on dynamic sports scenes in the CMU Panoptic Sports dataset. We evaluate ours with existing 4DGS baselines on benchmarks containing fast motions with large interframe displacements. We report PSNR and SSIM for six sports scene sequences across all baselines*

在渲染效率与存储方面，SPIN-4DGS达到**104 FPS**的推理速度，存储占用仅为**1261 MB**，显著低于D3DGS的1994 MB。这是因为SPIN-4DGS仅需存储Gaussian位置和轻量级隐式网络参数，属性由网络动态生成，避免了显式存储全部Gaussian属性的内存开销。

跨数据集泛化能力方面，在Neu3DV数据集上（Table 8），SPIN-4DGS平均PSNR为**32.19 dB**，与Realtime-4DGS（32.01 dB）持平或略优；在MeetRoom数据集上（Table 9），SPIN-4DGS平均PSNR为**32.04 dB**，比Realtime-4DGS（30.47 dB）提升**+1.57 dB**。需要指出，在Neu3DV和MeetRoom上为公平比较，SPIN-4DGS未使用位置精炼阶段，仅使用预精炼位置训练，这在一定程度上低估了方法的完整潜力。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_MWtXs60n38/figures/013_Table_8.jpg]]
*Table 8: Comparisons on the Neu3DV scenes. We report PSNR (and SSIM when available) for SPIN-4DGS and baselines across six sequences*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_MWtXs60n38/figures/014_Table_9.jpg]]
*Table 9: Comparisons on the MeetRoom scenes. We report PSNR and SSIM for SPIN-4DGS and baselines across three sequences and their average. Note that only average PSNR scores are available for StreamRF and 3DGStream*

### 消融实验：时空切片的关键作用

时空切片（Spatiotemporal Slicing）是SPIN-4DGS避免交叉帧干扰的核心机制。如Table 3所示，移除时空切片（即采用统一4D形式，所有时间步共用Gaussian位置）后，Basketball场景的PSNR从**30.05 dB**降至**28.96 dB**，训练时间与内存亦显著增加。Figure 5的定性对比进一步揭示：无切片时，同一组Gaussian需同时表示多个时间步，导致光栅化过程中贡献重叠与冲突，快速运动物体出现模糊和畸变；而切片策略显式地将Gaussian按帧分离，实现了时间一致的高质量重建。

### 消融实验：位置归一化与网络设计

输入位置归一化（Mip-NeRF contraction）对训练稳定性至关重要。Table 5显示，移除归一化后PSNR**骤降超过10 dB**，LPIPS从0.16恶化至0.45。这一结果表明，将无界空间坐标压缩到$[0,1]^3$对于隐式网络的稳定收敛是不可或缺的。

网络设计方面的消融（Table 5）还揭示：增大哈希映射尺寸（从$2^{21}$增至$2^{23}$）以及采用GELU激活函数均可进一步提升重建质量，最佳配置达到PSNR **30.25 dB**。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_MWtXs60n38/figures/010_Table_5.jpg]]
*Table 5: Ablation on our implicit network design components. Starting from the original 4D hash encoder (Chen et al., 2025), we analyze the effects of making positions trainable, applying input position normalization, and changing activation functions. Each modification progressively enhances reconstruction quality. All experiments are performed on the Basketball scene*

### 消融实验：位置估计与精炼

Table 2a考察了从Realtime-4DGS获取初始时空位置的早期训练时长（不进行后续精炼），结果表明适中的初始训练时长已能提供合理的位置先验。Table 2b则分析了逐帧精炼迭代次数的影响：即使仅使用0.5K次精炼迭代，SPIN-4DGS也能保持一致的物体结构而不崩溃（Figure 6），而逐步增加迭代次数可恢复球边缘和球拍网等精细细节。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_MWtXs60n38/figures/016_Figure_6.jpg]]
*Figure 6: Visualizations on spatiotemporal position refinement. We visualize the effect of varying refinement iterations (0.5K, 1K, 2K) corresponding to*

### 兼容性验证：隐式属性学习的通用性

Table 4的兼容性实验验证了隐式属性学习方案的通用性：使用D3DGS或Realtime-4DGS预训练的位置，仅替换属性优化为SPIN-4DGS的隐式网络训练，PSNR仍能大幅提升。例如，在Softball场景上使用D3DGS位置时，SPIN-4DGS带来**+2.49 dB**的PSNR增益。Figure 8的可视化结果也证实，重训属性后的重建比原始基线更清晰、更稳定。这证明隐式属性函数$f_\theta(\mathbf{x}, \mathbf{y}, \mathbf{z}, \mathbf{t})$的解耦设计是有效的，且可与不同的位置估计方案兼容。

### 感知质量与训练效率

在感知质量方面（Table 6），SPIN-4DGS在所有六个体育场景上均取得最优LPIPS，与其PSNR/SSIM优势一致。训练时间方面（Table 7），SPIN-4DGS可在更短训练预算下达到或超过D3DGS的性能，展现了良好的效率-质量权衡。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_MWtXs60n38/figures/011_Table_6.jpg]]
*Table 6: Perceptual quality comparison. We report LPIPS across six sports scenes on the CMU Panoptic Sports dataset. Lower scores indicate better perceptual quality*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_MWtXs60n38/figures/012_Table_7.jpg]]
*Table 7: Training time breakdown and PSNR on the Basketball scene. We compare PSNR, position-estimation time, refinement cost, network training time, and total training time across different SPIN-4DGS configurations and the D3DGS baseline. All time measurements are reported in minutes*

### 与逐帧3DGS的对比

Table 10将SPIN-4DGS与逐帧独立优化的**3DGS**（Kerbl et al., 2023）进行对比。SPIN-4DGS在所有六个体育场景上均优于3DGS和D3DGS，验证了时空共享表示（通过隐式网络）相比完全独立逐帧重建的优势——前者能在帧间共享结构信息，而后者缺乏跨帧一致性约束。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_MWtXs60n38/figures/007_Table_3.jpg]]
*Table 3: Ablation on spatiotemporal slicing. We compare a unified 4D formulation (i.e., w/o slicing), where Gaussian positions are optimized jointly across space–time, against our spatiotemporal slicing strategy that assigns positions per frame*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_MWtXs60n38/figures/009_Table_4.jpg]]
*Table 4: Compatibility with existing 4DGS baselines. We reuse pre-trained positions from D3DGS (Luiten et al., 2024) and Realtime-4DGS (Yang et al., 2024a), replacing their attribute optimization with our proposed implicit network training. SPIN-4DGS consistently improves PSNR/SSIM across all scenes, highlighting the compatibility and effectiveness of the proposed implicit 4DGS scheme*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_MWtXs60n38/figures/015_Table_10.jpg]]
*Table 10: Comparison with frame-wise 3DGS on the CMU Panoptic Sports benchmark. We report PSNR across six sports, showing that SPIN-4DGS consistently outperforms both 3DGS and D3DGS across all sequences*

## 方法谱系与知识库定位

### 问题定位：大帧间位移下的4DGS属性崩溃

现有4DGS方法在快速运动场景中面临根本性瓶颈：当帧间位移较大时，快速运动物体的Gaussian属性在训练过程中崩溃，导致物体模糊或消失。这一问题的根源在于**跨帧属性耦合**——无论是显式参数化方法还是可变形方法，Gaussian属性（颜色、尺度、旋转、不透明度）都在多个时间步间共享或通过变形场间接关联，使得静态背景主导优化过程，快速运动区域的属性学习受到严重干扰（Figure 2）。

具体而言：
- **显式4DGS方法**（如**Realtime-4DGS** (Yang et al., 2024a)、**4D-Rotor-Gaussians** (Duan et al., 2024)）将Gaussian属性与4D原语绑定，所有时间步共用同一组属性参数。在快速运动场景中，随着训练迭代数增加（如15K→30K），共享属性在不同帧间的优化信号相互冲突，导致质量急剧退化。
- **可变形4DGS方法**（如**4DGaussian** (Wu et al., 2024)、**Grid4D** (Xu et al., 2024)、**MoDec-GS** (Kwak et al., 2025)）从规范空间变形Gaussian并共享规范空间属性。当帧间位移过大时，规范空间无法为快速运动物体分配足够的Gaussian，初始化即失败。

### 核心创新：隐式属性解耦

SPIN-4DGS的核心洞察是**将Gaussian属性学习从时空共享参数中彻底解耦**。不同于现有方法让属性跨帧耦合，SPIN-4DGS将属性视为时空位置的隐式函数，使用轻量级前馈网络 $f_\theta(\mathbf{x}, \mathbf{y}, \mathbf{z}, \mathbf{t})$ 直接从显式时空坐标预测每帧的属性，从根本上消除跨帧干扰。

这一设计带来三个关键改变：

1. **属性学习方式**：从“跨帧共享参数”转变为“逐帧独立解码”。可变形方法从规范空间变形并共享属性，显式方法在4D原语上时间切片后属性仍共享；SPIN-4DGS则通过4D哈希编码器和多分支MLP解码器，为每一帧的每个Gaussian独立预测属性，属性不跨帧耦合。

2. **Gaussian位置表示**：从“所有时间步共用位置”转变为“逐帧显式时空位置”。SPIN-4DGS构建 $(x, y, z, t)$ 的逐帧位置集合，通过时空切片策略仅保留当前帧相关的Gaussian，消除无关时间步的干扰。位置先由显式方法（默认Realtime-4DGS）初步估计，再通过光栅化损失逐帧精炼。

3. **参数存储与内存效率**：从“显式存储所有属性”转变为“仅存储位置和网络参数”。D3DGS显式存储所有Gaussian的所有属性（1994 MB），而SPIN-4DGS仅存储Gaussian位置和网络参数（1261 MB），属性由网络动态生成，在保持更高渲染质量的同时降低了存储开销。

### 方法谱系定位

SPIN-4DGS处于**显式位置+隐式属性**的交叉点，与现有方法的关系如下：

| 方法类别 | 代表工作 | 位置表示 | 属性学习 | 跨帧耦合程度 |
|---------|---------|---------|---------|------------|
| 逐帧3DGS | **3DGS** (Kerbl et al., 2023) | 逐帧独立 | 逐帧独立优化 | 无耦合，但无时空一致性 |
| 显式4DGS | **Realtime-4DGS** (Yang et al., 2024a) | 4D原语共享 | 跨帧共享 | 高耦合 |
| 显式4DGS | **4D-Rotor-Gaussians** (Duan et al., 2024) | 4D原语共享 | 跨帧共享 | 高耦合 |
| 可变形4DGS | **4DGaussian** (Wu et al., 2024) | 规范空间+变形 | 规范空间共享 | 高耦合 |
| 可变形4DGS | **Grid4D** (Xu et al., 2024) | 规范空间+变形 | 规范空间共享 | 高耦合 |
| 可变形4DGS | **MoDec-GS** (Kwak et al., 2025) | 规范空间+变形 | 规范空间共享 | 高耦合 |
| 外部监督 | **D3DGS** (Luiten et al., 2024) | 逐帧跟踪 | 跨帧共享 | 高耦合（依赖分割掩码） |
| 外部监督 | **TC3DGS** (Javed et al., 2024) | 逐帧跟踪 | 跨帧共享 | 高耦合（依赖外部监督） |
| **本文方法** | **SPIN-4DGS** | 逐帧显式位置 | 隐式网络逐帧解码 | **无耦合** |

值得强调的是，SPIN-4DGS在训练过程中**不使用任何外部监督**（如分割掩码），而D3DGS和TC3DGS等方法依赖外部监督来隔离动态物体。兼容性实验（Table 4）进一步表明，即使复用D3DGS或Realtime-4DGS的预训练位置并仅替换属性学习方案，SPIN-4DGS仍能大幅提升PSNR（如在Softball场景上使用D3DGS位置提升+2.49 dB），证明了隐式属性学习方案的独立有效性。

### 适用边界与局限

尽管SPIN-4DGS在大帧间位移场景中表现突出，其适用边界受以下因素制约：

1. **初始位置质量依赖**：方法依赖前期位置估计的质量。当初始时空位置稀疏时（如大规模室外或高度杂乱场景），需要更长的精炼流程来稠密化Gaussian，增加训练成本。若初始位置严重不足，整体性能可能受限。

2. **小物体覆盖不足**：对于小物体或初始点极少的区域，即使多次精炼迭代也难以生成或恢复足够的缺失点。这在远处快速移动的小目标上尤为明显。

3. **场景规模与训练成本**：在Neu3DV和MeetRoom等较小规模场景上，SPIN-4DGS的优势相对收窄（Neu3DV平均PSNR仅领先+0.18 dB），表明方法的核心优势集中于大位移快速运动场景。同时，位置精炼阶段在大规模场景中可能成为训练瓶颈。

### 开放问题

1. **稀疏初始位置的优化调度**：在稀疏初始位置的大规模场景中，如何优化精炼调度以降低训练成本，同时保证覆盖完整性？

2. **极小物体的多尺度策略**：对于远处快速移动的小目标，能否引入多尺度或焦点策略改善Gaussian覆盖，避免遗漏？

3. **几何变形的联合建模**：隐式属性函数能否进一步扩展到同时建模几何变形，以处理更复杂的场景动态（如非刚性形变与快速运动的叠加）？

4. **实时应用优化**：当前框架在实时应用（如VR/AR）中的延迟和内存开销是否可进一步优化？SPIN-4DGS虽已达到104 FPS的渲染速度，但网络推理开销在资源受限设备上仍需评估。

## 原文 PDF

![[paperPDFs/ICLR_2026/Implicit_4D_Gaussian_Splatting_for_Fast_Motion_with_Large_Inter_Frame_Displaceme_a038d3b5b498.pdf]]