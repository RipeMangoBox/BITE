---
title: "ReLi3D: Relightable Multi-view 3D Reconstruction with Disentangled Illumination"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ReLi3D_Relightable_Multi_view_3D_Reconstruction_with_Disentangled_Illumination_5eeafb1d146e.pdf
project_link: "https://reli3d.jdihlmann.com/"
code_link: null
aliases:
- ReLi3D
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 用多视角交叉视图融合（cross-view fusion）为材质-光照解耦提供几何一致性约束，并通过可微分蒙特卡洛渲染器（MC+MIS）强制物理可解释性，从而将不适定的单视角问题转化为可约束的多视角问题。
primary_logic: 多视角观测对同一表面点在不同视角下的一致性约束，能够显著缩小材质与光照的可行解空间，是实现材质-光照解耦的关键缺失信息；结合双路径预测与基于物理的渲染，可首次在单次前馈推理中联合重建网格、空间变化PBR材质和HDR环境光。
claims:
- 多视角约束可以显著改善材质与光照的解耦，而这一问题对单视角方法来说仍然是根本上不适定的。
- 在Polyhaven+HDRI数据集上，ReLi3D的重光照PSNR达到20.88 dB，而SPAR3D仅为17.10 dB，同时推理速度（0.34s）远快于DiffusionLight（21.46s）。
- 在Polyhaven+Blender Shiny数据集上，ReLi3D预测的空间变化基色PSNR达到25.00 dB，而SF3D的全局基色PSNR仅为18.42 dB。
- 移除可微分MC渲染器后，图像重建PSNR从19.92 dB降至17.54 dB，表明物理渲染是材质-光照解耦的关键组件，而非优化细节。
---

# ReLi3D: Relightable Multi-view 3D Reconstruction with Disentangled Illumination

> [!tip] 核心洞察
> 多视角观测对同一表面点在不同视角下的一致性约束，能够显著缩小材质与光照的可行解空间，是实现材质-光照解耦的关键缺失信息；结合双路径预测与基于物理的渲染，可首次在单次前馈推理中联合重建网格、空间变化PBR材质和HDR环境光。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReLi3D：解耦光照的可重光照多视角三维重建 |
| 英文题名 | ReLi3D: Relightable Multi-view 3D Reconstruction with Disentangled Illumination |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=BlSKgQb3Vd) · [Project](https://reli3d.jdihlmann.com/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | ReLi3D |
| Dataset | Polyhaven + HDRI, Polyhaven + Blender Shiny, GSO + Stanford ORB, Speed |

> [!tip] 效果简介
> - Polyhaven + HDRI 上，Relighting PSNR (dB) 20.88 (ReLi3D) vs 17.10 (SPAR3D) (+3.78)。
> - Polyhaven + Blender Shiny 上，Basecolor PSNR (dB) 25.00 (单视图) vs 18.42 (SF3D) (+6.58)。
> - GSO + Stanford ORB 上，Image PSNR (dB) – 单视图 19.57 vs 17.64 (SF3D) (+1.93)。

## 概述

单视角图像到三维重建的核心瓶颈在于材质与光照的解耦本质上是**不适定的**：同一个二维外观可以由无数种表面反射率与入射光照的组合产生，导致材质估计不可靠、法线预测不准确，进而限制了重光照的真实感。现有的前馈重建方法（如 **SF3D**，Boss et al., 2024）仅输出全局 BRDF 参数且不估计环境光照，扩散模型方法（如 **SPAR3D**，Huang et al., 2025）虽能生成 PBR 材质但解耦质量有限，而专门的照明估计方法（如 **DiffusionLight**，Phongthawee et al., 2023）则完全独立于几何重建，无法形成统一的物理可解释管线。

**ReLi3D** 的核心洞察在于：**多视角观测对同一表面点在不同视角下的一致性约束，能够显著缩小材质与光照的可行解空间**——这是单视角方法所缺失的关键信息。基于此，ReLi3D 构建了首个统一的前馈推理框架，在单次前向传播（约 0.3 秒）中联合重建：

1. **完整三维网格**（通过 Flexicubes 提取，约 4.5k 顶点）；
2. **空间变化的 PBR 材质**（基色、粗糙度、金属度、法线凹凸贴图）；
3. **HDR 环境光照**（基于 RENI++ 潜在空间预测）。

方法的核心因果机制是**双路径架构 + 可微分物理渲染器**的协同设计：共享交叉条件变换器融合任意数量（1–16）的输入视图，构建统一的 triplane 特征表示；几何与外观路径从中预测密度场与 svBRDF 参数，光照路径则利用掩膜感知的 DINOv2 特征预测 RENI++ 潜在码与全局旋转；两条路径通过**可微分蒙特卡洛多重重要性采样（MC+MIS）渲染器**统一监督，强制材质与光照的物理可解释解耦。

实验证据表明这一设计是有效的：

- 在 Polyhaven+HDRI 数据集上，ReLi3D 的重光照 PSNR 达到 **20.88 dB**，显著优于 SPAR3D 的 17.10 dB（Table 4）；
- 空间变化基色预测 PSNR 达到 **25.00 dB**，远超 SF3D 全局基色的 18.42 dB（Table 1）；
- 消融实验证实，移除可微分 MC 渲染器后图像重建 PSNR 从 19.92 dB 降至 17.54 dB，表明物理渲染是解耦的**必要组件**而非优化细节（Table 5）；
- 训练阶段贡献分析进一步揭示：早期高斯近似阶段主要贡献几何覆盖提升（70–80%），而最终 MC 微调阶段贡献了大部分材质解耦提升——基色 53.5%、粗糙度 62.4%、金属度 51.3%（Table 6）。

在推理效率上，ReLi3D 的单张 H100 GPU 推理时间仅 **0.28 秒**，相比 Hunyuan3D 的 69.40 秒实现了约 250 倍加速，同时保持或超越了其重建质量。

方法仍存在若干局限：当环境光照超出 RENI++ 先验分布时（如多个极亮点光源），解耦易失败并出现材质图烘焙光照；强自遮挡阴影区域与极暗场景下材质估计退化；三平面分辨率（3×40×384×384）限制了纹理与几何细节的保真度。透明物体的显式网格重建与材质估计仍是一个开放挑战。

## 背景与动机

### 问题背景：三维重建中的材质-光照解耦困境

从稀疏多视角图像重建可重光照的三维资产，是计算机视觉与图形学交叉领域的核心挑战。其关键难点在于**材质与光照的解耦**：同一张二维图像的外观可以由无数种表面反射率与入射光照的组合产生，这使得从像素反推本征属性在数学上是一个严重不适定问题。对于仅依赖单视图的方法，这种歧义尤为突出——模型缺乏跨视角的几何与光度一致性约束，无法可靠地区分“白色表面在红光下”与“红色表面在白光下”两种截然不同的物理场景。

现有前馈重建方法（如 **SF3D**，Boss et al., 2024）虽能快速生成带纹理的网格，但其材质表示局限于全局粗糙度与金属度参数，既不支持空间变化的物理材质，也不具备环境光照估计能力，因而无法实现重光照。生成式方法（如 **SPAR3D**，Huang et al., 2025；**Hunyuan3D**，Zhao et al., 2025）虽在几何质量上有所提升，但材质-光照解耦仍非其设计目标，重光照真实感受到根本限制。另一方面，专门的光照估计方法（如 **DiffusionLight**，Phongthawee et al., 2023）虽能从单图预测HDR环境图，却无法同时重建三维几何与材质，且推理耗时长达数十秒。

### 核心瓶颈：单视角歧义与物理约束的缺失

上述困境的根源可归结为两个相互关联的瓶颈：

1. **单视角信息不足**：单张图像仅提供物体在特定光照条件下的二维投影，缺乏对同一表面点在不同视角下外观变化的观测。这种跨视角一致性正是缩小材质-光照可行解空间的关键缺失信息。
2. **渲染监督的物理不可解释性**：现有方法多采用不可微渲染或纯图像空间损失（如MSE、LPIPS）进行监督，这些损失函数对材质与光照的交互缺乏物理建模，无法强制模型学习有物理意义的解耦表示。

### 本文动机：多视角约束与物理渲染的联合突破

ReLi3D的核心洞察在于：**多视角观测对同一表面点在不同视角下的一致性约束，能够显著缩小材质与光照的可行解空间**。这一洞察直接回应了单视角方法的不适定本质——当系统观测到同一表面点在多个视角下的外观时，材质反射率与入射光照的组合可能性被大幅压缩，解耦变得可行。

为实现这一目标，ReLi3D设计了两个关键机制：

- **交叉视图融合**：通过共享的交叉条件变换器融合任意数量的输入视图（1–16），为几何、材质与光照的联合预测提供多视角一致性表示。
- **可微分物理渲染**：采用基于多重重要性采样（MIS）的蒙特卡洛（MC）路径追踪渲染器，在训练中强制材质-光照解耦满足物理光照传输方程，使图像重建损失能够通过可微渲染梯度反向传播至材质与光照参数。

这种“多视角约束 + 物理渲染监督”的组合，首次使得在单次前馈推理中联合重建网格、空间变化PBR材质和HDR环境光成为可能，推理时间仅约0.3秒，较生成式方法加速约250倍（对比Hunyuan3D的69.4秒）。

## 核心创新

ReLi3D的核心创新在于将单视角下根本上不适定的材质-光照解耦问题，通过**多视角交叉视图融合**与**可微分物理渲染**的联合约束，转化为一个可求解的前馈推理问题。与现有方法相比，其关键改变体现在以下五个维度。

### 从单视角到任意多视角的输入范式

现有前馈重建方法（如**SF3D** (Boss et al., 2024)）以固定单视图为输入，缺乏跨视角几何一致性信息，导致材质与光照的歧义无法消解。ReLi3D将输入扩展为1–16张任意数量的多视图图像，通过共享交叉条件变换器（Cross-conditioning Transformer）将各视图的DINOv2图像token与相机嵌入融合为统一的triplane特征表示，使不同视角对同一表面点的观测形成一致性约束。这一改变直接命中核心瓶颈：多视角观测显著缩小了材质与光照的可行解空间，将不适定问题转化为可约束问题。

### 从全局BRDF到空间变化svBRDF的材质表示

**SF3D**仅预测全局粗糙度和金属度参数，无法表达物体表面材质在空间上的变化。ReLi3D从triplane特征出发，利用五个独立MLP头联合预测密度、反照率、粗糙度、金属度和凹凸法线，并通过Flexicubes提取网格后进行快速UV展开，生成空间变化的PBR纹理贴图。在Polyhaven+Blender Shiny数据集上，ReLi3D的基色PSNR达到25.00 dB，而SF3D的全局基色PSNR仅为18.42 dB（Table 1），差距达+6.58 dB，直接验证了空间变化材质表示对重建精度的关键作用。

### 从无光照估计到HDR环境图预测

**SF3D**完全不具备环境光照估计能力，**SPAR3D** (Huang et al., 2025)虽预测RENI++潜在码但解耦质量有限。ReLi3D设计了独立的光照路径：利用掩膜感知的DINOv2-small编码多视图掩膜-图像对，通过1D环境变换器预测RENI++潜在码和6D旋转，解码为HDR环境图。在Polyhaven+HDRI数据集上，ReLi3D的重光照PSNR达到20.88 dB，显著优于SPAR3D的17.10 dB（Table 4），且推理速度（0.34s）远快于扩散方法**DiffusionLight**（21.46s），在精度与效率上实现了双重突破。

### 从不可微渲染到可微分MC+MIS物理渲染

这是ReLi3D最根本的机制创新。现有方法（如**LRM**、**SF3D**）依赖不可微渲染或纯图像空间损失，缺乏对材质-光照物理解耦的强制约束。ReLi3D引入基于VNDF采样、球帽与对抗采样的可微分蒙特卡洛多重重要性采样（MC+MIS）渲染器，将几何-外观路径与光照路径统一在物理渲染方程下进行端到端监督。消融实验（Table 5）表明，移除该渲染器后图像PSNR从19.92 dB降至17.54 dB，证明物理渲染不是优化细节，而是材质-光照解耦的必要组件。

### 从纯合成域到混合域的训练策略

**LRM**、**SF3D**等方法仅在合成数据上训练，向真实场景泛化时性能退化明显。ReLi3D采用混合域训练：42k合成PBR数据提供全监督材质真值，70k合成RGB数据与62k真实世界UCO3D捕获数据通过图像空间自监督损失（MSE+LPIPS）进行联合优化，材质监督损失（Eq. 14）根据数据可用性自适应调整权重。这一策略使ReLi3D在Stanford ORB真实数据集上同样取得领先（Table 3），弥合了合成-真实域间鸿沟。

## 整体框架

ReLi3D 是一个端到端的前馈推理管线，能够在一次前向传播中从稀疏多视角图像联合重建三维几何、空间变化的 PBR 材质以及 HDR 环境光照。管线的核心设计理念是将材质-光照解耦这一单视角下的不适定问题，通过多视角交叉视图约束转化为可约束问题，并利用可微分物理渲染强制执行物理一致性。

### 输入与输出

**输入**：任意数量（1–16 张）的已知相机位姿的 RGB 图像，以及对应的物体掩膜。相机位姿由外部系统（如 DUST3R）提供，掩膜可通过 Segment Anything 等工具获取。

**输出**：
- 带 UV 纹理的三角网格（通过 Flexicubes 从密度场提取）
- 空间变化的 PBR 材质贴图（基色、粗糙度、金属度、法线凹凸）
- HDR 环境图（通过 RENI++ 解码器从潜在码生成）

### 双路径架构

ReLi3D 的整体流程如 Figure 2 所示，由**共享交叉条件变换器**融合多视角信息后，分叉为两条并行路径：

![[assets/figures/papers/paper_list_l59_https_openreview_net_forum_id_BlSKgQb3Vd/figures/002_Figure_2.jpg]]
*Figure 2: ReLi3D Overview. Multi-view input images are fused by a shared cross-conditioning transformer into two parallel paths: a Geometry & Appearance Path (blue) using a Triplane Transformer to predict mesh geometry and PBR materials, and an Illumination Path (green) using a Multi-View Illumination Transformer to estimate HDR environments. Both paths are unified through a differentiable Monte Carlo Multiple Importance Sampling rendering to learn to wproduce complete relightable 3D assets*

1. **几何与外观路径（Geometry & Appearance Path）**：从统一的三平面（triplane）特征表示中预测密度场和空间变化的 PBR 材质参数，并通过 Flexicubes 提取显式网格，经快速 UV 展开进行纹理映射。

2. **光照路径（Illumination Path）**：利用掩膜感知的 DINOv2 特征和专用 1D 变换器，预测 RENI++ 潜在码及全局旋转，解码为 HDR 环境图。

两条路径通过**可微分蒙特卡洛多重重要性采样（MC+MIS）渲染器**统一监督，强制材质与光照的物理解耦。

### 模块间数据流

1. **多视图编码与融合**：每张输入图像通过 DINOv2 提取图像 token $\mathbf{T}_i^{\mathrm{img}}$，与相机嵌入 $\mathbf{e}_i$ 逐元素调制后拼接，形成视图条件 token $\mathbf{T}_i^{\mathrm{cond}}$。共享交叉条件变换器以“英雄视图”查询流 $\mathbf{Q}_0$ 初始化的方式，通过交叉注意力融合所有视图信息，输出统一的 triplane token $\mathbf{T}^{\mathrm{tri}}$。

2. **三平面特征构建**：triplane token 被重塑为三个正交特征平面 $\mathbf{T}_{xy}, \mathbf{T}_{yz}, \mathbf{T}_{zx}$。对于任意三维点 $\mathbf{p}$，通过投影并拼接三个平面的特征获得空间特征 $\mathbf{f}(\mathbf{p})$：
   $$\mathbf{f}(\mathbf{p}) = \operatorname{concat}(\mathbf{T}_{xy}(x,y), \mathbf{T}_{yz}(y,z), \mathbf{T}_{zx}(z,x))$$

3. **几何与材质预测**：五个独立的 MLP 头从 $\mathbf{f}(\mathbf{p})$ 联合预测密度 $\sigma$、基色 $\rho$、粗糙度 $r$、金属度 $m$ 和凹凸法线 $\mathbf{n}_{\mathrm{bump}}$。密度场通过 Flexicubes 提取网格，材质参数经 UV 展开映射为空间变化的纹理贴图。

4. **光照估计**：掩膜-图像对通过带额外输入通道的 DINOv2-small 编码为掩膜感知 token $\mathbf{T}_i^{\mathrm{mask}}$，与主变换器输出拼接形成环境上下文 $\mathbf{T}^{\mathrm{env-ctx}}$。1D 环境变换器通过交叉注意力将其映射为 RENI++ 潜在码 $\mathbf{z}_{\mathrm{env}}$ 和 6D 旋转 $\mathbf{r}_{6\mathrm{D}}$，最终解码为 HDR 环境图：
   $$L_{\mathrm{env}}(\omega) = \exp(f_{\theta}(\mathbf{z}, \gamma(\omega)))$$

5. **可微分渲染与监督**：MC+MIS 渲染器采用 VNDF 采样、球帽采样与对抗采样策略进行可微分路径追踪，将预测的网格、PBR 材质和环境图渲染为图像，与输入图像计算联合损失（MSE + LPIPS），同时施加材质监督损失和环境光监督损失。这一闭环机制是材质-光照解耦的关键——消融实验表明，移除 MC 渲染器后图像重建 PSNR 从 19.92 dB 降至 17.54 dB（Table 5），验证了物理渲染对于解耦的必要性。

### 训练策略

ReLi3D 采用**混合域训练**以弥合合成数据与真实场景之间的差距：训练数据包含 42k 合成 PBR 物体（提供完整材质真值）、70k 合成 RGB-only 物体（仅图像监督）以及 62k 真实世界 UCO3D 多视角捕获（仅图像监督）。训练分阶段进行：早期阶段使用高斯近似渲染快速扩展几何覆盖（贡献 70–80% 的覆盖提升），最终阶段切换为 MC 渲染器进行微调，贡献了大部分材质解耦增益（基色 53.5%、粗糙度 62.4%、金属度 51.3%，Table 6）。

## 核心模块与公式推导

ReLi3D 的核心架构由四条关键模块构成：共享交叉条件变换器、几何与外观路径、光照路径，以及可微分蒙特卡洛渲染器。这些模块协同工作，通过多视角一致性约束将材质-光照解耦从不适定问题转化为可约束问题。

### 共享交叉条件变换器

该模块是两条并行路径的统一基础，负责融合任意数量的输入视图并构建一致的跨视角表示。其设计遵循三个关键步骤：

**视图条件化**：每个输入视图 $i$ 首先通过预训练的 DINOv2 编码器提取图像 token $\mathbf{T}_i^{\mathrm{img}}$，并与相机嵌入 $\mathbf{e}_i$ 进行逐元素调制后拼接，形成视图条件 token：

$$\mathbf{T}_i^{\mathrm{cond}} = [ \mathbf{T}_i^{\mathrm{img}} \odot \mathbf{e}_i ; \mathbf{e}_i ]$$

其中 $\odot$ 表示逐元素乘法，$[\cdot;\cdot]$ 表示沿通道维度的拼接。相机嵌入编码了每张视图的相机位姿信息，使变换器能够感知多视角之间的空间关系。

**英雄视图查询流**：变换器采用查询流机制，其初始查询 $\mathbf{Q}_0$ 由预学习的 triplane token $\mathbf{T}^{\mathrm{tri}}$ 与选定的“英雄视图”图像 token $\mathbf{T}_h^{\mathrm{img}}$ 拼接构成：

$$\mathbf{Q}_0 = [ \mathbf{T}^{\mathrm{tri}} \Lambda; \mathbf{T}_h^{\mathrm{img}} ]$$

其中 $\Lambda$ 为可学习的缩放因子。英雄视图为几何与外观路径提供了主要的视觉参考，而其他视图则通过交叉注意力补充视差信息。

**Triplane 特征提取**：变换器输出的 triplane 表示由三个正交特征平面 $\mathbf{T}_{xy}$、$\mathbf{T}_{yz}$、$\mathbf{T}_{zx}$ 组成。对于任意三维空间点 $\mathbf{p} = (x, y, z)$，其特征通过投影到三个平面上并拼接获得：

$$\mathbf{f}(\mathbf{p}) = \operatorname{concat}(\mathbf{T}_{xy}(x,y), \mathbf{T}_{yz}(y,z), \mathbf{T}_{zx}(z,x))$$

这种显式三平面表示在保持计算效率的同时，为后续的密度场查询和材质预测提供了结构化的三维特征。

### 几何与外观路径

该路径从 triplane 特征出发，联合预测场景几何与空间变化的 PBR 材质。其核心是五个独立的 MLP 头，分别预测密度、反照率、粗糙度、金属度和凹凸法线：

$$\{\sigma, \rho, r, m, \mathbf{n}_{\mathrm{bump}}\}(\mathbf{p}) = \{\mathrm{MLP}_{\mathrm{density}}, \mathrm{MLP}_{\mathrm{albedo}}, \mathrm{MLP}_{\mathrm{rough}}, \mathrm{MLP}_{\mathrm{metal}}, \mathrm{MLP}_{\mathrm{normal}}\}(\mathbf{f}(\mathbf{p}))$$

其中 $\sigma$ 为体积密度，$\rho$ 为空间变化反照率（基色），$r$ 为粗糙度，$m$ 为金属度，$\mathbf{n}_{\mathrm{bump}}$ 为凹凸法线偏移。所有 MLP 共享 triplane 特征 $\mathbf{f}(\mathbf{p})$ 作为输入，但各自拥有独立的参数。

几何提取采用 **Flexicubes** 从密度场中提取高质量网格，随后通过快速 UV 展开将空间变化的 PBR 参数映射为纹理贴图。这一设计使得 ReLi3D 能够输出可直接用于图形管线的高质量网格资产，而非仅停留在神经场表示。

### 光照路径

光照路径负责从多视图输入中估计 HDR 环境光照，其设计充分利用了前景掩膜信息与跨视图上下文。

**掩膜感知 token 编码**：对于每个输入视图 $i$，将其前景掩膜 $\mathbf{M}_i$ 与 RGB 图像 $\mathbf{I}_i$ 沿通道拼接后，送入带有两个额外输入通道的 DINOv2-small 编码器：

$$\mathbf{T}_i^{\mathrm{mask}} = f_{\mathrm{mask}}([ \mathbf{M}_i, \mathbf{I}_i ])$$

掩膜信息使编码器能够聚焦于物体区域，同时保留背景中的光照线索（如可见光源位置）。

**环境上下文拼接**：将所有视图的掩膜 token 与主变换器的输出 token 拼接，形成光照路径的完整上下文：

$$\mathbf{T}^{\mathrm{env-ctx}} = \operatorname{concat}(\{ \mathbf{T}_i^{\mathrm{mask}} \}_{i=1}^N, \mathbf{T}^{\mathrm{out}})$$

**环境光照预测**：1D 环境变换器通过交叉注意力机制，从可学习的环境 token bank $\mathbf{T}^{\mathrm{env-bank}}$ 中查询，融合多视图上下文 $\mathbf{T}^{\mathrm{env-ctx}}$，输出 RENI++ 潜在码 $\mathbf{z}_{\mathrm{env}}$ 和 6D 旋转表示 $\mathbf{r}_{6\mathrm{D}}$：

$$[\mathbf{z}_{\mathrm{env}}, \mathbf{r}_{6\mathrm{D}}] = \mathrm{EnvTransformer}(\mathbf{T}^{\mathrm{env-bank}}, \mathbf{T}^{\mathrm{env-ctx}})$$

**RENI++ 解码**：最终 HDR 环境图 $L_{\mathrm{env}}(\omega)$ 通过预训练的 RENI++ 解码器 $f_{\theta}$ 从潜在码 $\mathbf{z}_{\mathrm{env}}$ 和方向 $\omega$ 的位置编码 $\gamma(\omega)$ 解码得到：

$$L_{\mathrm{env}}(\omega) = \exp(f_{\theta}(\mathbf{z}_{\mathrm{env}}, \gamma(\omega)))$$

指数映射确保输出的环境图值域为非负 HDR 辐射度。RENI++ 先验将环境光照约束在自然光照分布的流形上，为不适定的光照估计问题提供了有效的正则化。

### 可微分蒙特卡洛渲染器

该模块是 ReLi3D 实现材质-光照物理解耦的关键组件。它采用基于物理的路径追踪，结合 **VNDF 采样**、**球帽采样**与**对抗采样**策略，通过多重重要性采样（MIS）在材质 BRDF 采样和环境光采样之间进行最优混合。

渲染器以几何与外观路径输出的网格、svBRDF 材质以及光照路径输出的 HDR 环境图作为输入，生成物理正确的重光照图像。该过程的完全可微性使得梯度可以从图像空间损失反向传播至两条路径的所有参数，强制材质与光照在物理层面的一致性。

**训练损失**方面，ReLi3D 采用三项联合监督。图像重建损失结合像素级 MSE 与感知 LPIPS 损失：

$$\mathcal{L}_{\mathrm{img}} = 10.0\,\mathcal{L}_{\mathrm{MSE,im}} + 2.0\,\mathcal{L}_{\mathrm{LPIPS,im}}$$

材质监督损失适应混合域数据，对基色、粗糙度、金属度使用 MSE，对法线使用余弦相似度，并附加凹凸贴图的平坦正则化：

$$\mathcal{L}_{\mathrm{mat}} = 10.0\,\mathcal{L}_{\mathrm{MSE,PBR}} + 4.0\,\mathcal{L}_{\mathrm{cos,nrm}} + 0.05\,\mathcal{L}_{\mathrm{flat}}$$

环境光监督损失在有 RENI++ 真值时使用 MSE 监督，否则采用解调正则化倾向中性白光：

$$\mathcal{L}_{\mathrm{env}} = 0.1\,\mathcal{L}_{\mathrm{MSE,RENI}} + 0.02\,\mathcal{L}_{\mathrm{demod}}$$

消融实验表明，移除可微分 MC 渲染器后图像重建 PSNR 从 19.92 dB 降至 17.54 dB，证实了物理渲染对于材质-光照解耦的必要性——它不仅是渲染质量的优化细节，更是约束解空间的核心机制。

## 实验与分析

### 核心瓶颈与验证逻辑

ReLi3D的核心论断是：多视角交叉视图融合可以为材质-光照解耦提供几何一致性约束，从而将单视角方法中根本上不适定的问题转化为可约束的多视角问题。实验设计围绕三个层次展开：**（1）重建与材质解耦质量**——证明空间变化svBRDF预测的准确性及其随视图数增加的提升；**（2）光照估计与重光照真实感**——验证HDR环境图预测的精度和重光照结果对物理真实性的保持；**（3）消融与训练动态**——揭示可微分MC渲染器和分阶段训练策略各自的贡献份额。

### 重建与材质解耦质量

**主结果（Table 1, Table 2）**：在Polyhaven+Blender Shiny数据集上，ReLi3D预测的空间变化基色（basecolor）PSNR达到25.00 dB，而SF3D的全局基色PSNR仅为18.42 dB（+6.58 dB）。这一差距直接验证了多视角约束对材质-光照解耦的因果效应——SF3D的单视图全局BRDF无法区分“白色表面在暖光下”与“暖色表面在白光下”的歧义，而ReLi3D通过跨视角观测同一表面点在不同光照方向下的反射差异，显著缩小了可行解空间。

在GSO+Stanford ORB基准上，单视图图像PSNR达到19.57 dB（vs SF3D的17.64 dB），4视图进一步提升至21.43 dB。值得注意的是，单视图下Chamfer Distance（CD）为0.30，略差于SF3D的0.28（+0.02），但4视图下CD改善至0.28，说明多视图信息对几何重建的贡献主要体现在覆盖完整性而非单视图精度。Table 2注释指出TripoSG和Hunyuan3D生成的顶点数显著更高（100k+ vs 4.5k），但这不影响图像与材质指标的比较公平性。

**真实世界泛化（Table 3, Figure 7, Figure 8）**：在Stanford ORB真实数据集上，ReLi3D在所有3D重建、图像质量和基色预测指标上均优于基线，且性能随视图数增加而持续提升。Figure 8展示了UCO3D真实场景下的材质图预测——即使在强反射和运动模糊等极具挑战的条件下，方法仍能大致分离金属与非金属材质。这得益于混合域训练策略（42k合成PBR + 70k合成RGB + 62k真实UCO3D），通过图像空间自监督桥接合成-真实域间隙。

### 光照估计与重光照真实感

**定量对比（Table 4）**：在Polyhaven+HDRI数据集上，ReLi3D的重光照PSNR达到20.88 dB，显著优于SPAR3D的17.10 dB（+3.78 dB）。更关键的是推理速度：ReLi3D仅需0.34s，而扩散模型方法DiffusionLight需要21.46s（约63×加速）。这确立了前馈物理渲染路径在效率-质量权衡上的优势。

**定性对比（Figure 4, Figure 10）**：Figure 4左栏展示了单视图光照预测与真值及SPAR3D的对比——ReLi3D预测的环境图形状和颜色与真值高度吻合，而SPAR3D虽同样预测RENI++潜在码，但结果严重退化。Figure 4右栏揭示了背景信息的关键作用：当输入视图包含背景时，方法能正确定位光源位置；当仅依赖漫反射表面推断时，预测分布更为分散。Figure 10进一步显示DiffusionLight会“幻觉”出完全不同的环境图，SPAR3D基本失败，而ReLi3D忠实地复现了真值环境图的形状与色调。

**重光照指标随视图数变化（Table 1左栏）**：重光照PSNR从单视图的19.77 dB单调提升至16视图的21.21 dB，验证了多视角观测对光照估计的持续增益。值得注意的是，重光照评估中ReLi3D使用自身预测的环境图，而对比方法若支持则输入真实环境图——这使得ReLi3D的优势更具说服力。

### 消融实验

**可微分MC渲染器的必要性（Table 5）**：移除可微分MC渲染器后，图像重建PSNR从19.92 dB降至17.54 dB（-2.38 dB）。这一降幅远超一般优化细节的贡献，证实MC+MIS渲染器是材质-光照物理解耦的关键组件——它通过强制渲染方程约束，防止网络学习到仅满足图像空间损失但物理不一致的材质-光照组合。

**训练阶段贡献分析（Table 6）**：将训练过程从Phase 1（128高斯近似）到最终MC微调的总提升分解到各中间阶段，结果显示：早期高斯阶段主要贡献几何覆盖提升（70-80%），而最终MC微调阶段贡献了大部分材质解耦提升——基色53.5%、粗糙度62.4%、金属度51.3%。这一动态揭示了分阶段训练策略的功能分工：先以计算高效的高斯近似建立几何先验，再以物理精确的MC渲染精细化解耦。

**英雄视图选择敏感性（Table 7）**：随机选择英雄视图与固定正面视图相比仅有微小差异，随机选择因包含侧视视差信息而产生略优的感知质量，表明方法对视图选择策略不敏感，具有良好的鲁棒性。

### 失败模式与局限性

**Figure 11系统展示了典型失败案例**：

1. **烘焙光照残留**：强自遮挡阴影区域（如鲨鱼鳍下方）导致材质图中残留光照效果，环境光照超出RENI++先验分布时（如多个极亮局域化点光源）解耦失败。
2. **暗场景材质退化**：极暗场景（如犀牛案例）使基色预测困难，材质估计明显退化，与Hunyuan3D对比中可见纹理模糊。
3. **三平面分辨率瓶颈**：受限于3×40×384×384的三平面容量，纹理与几何细节在部分重建中表现为模糊，透明物体仅靠密度场处理，显式网格重建透明表面仍为开放挑战。
4. **相机位姿依赖**：方法假设已知相机位姿；当位姿估计严重错误时（如使用DUST3R产生大误差），会出现模糊伪影。多视图扩散生成图像可能存在视角不一致，目前会导致性能下降。

### 公平性说明

所有几何评估前均对预测网格施加刚性ICP对齐至真值网格，以补偿基线方法生成任意规范空间的偏差。部分基线（TripoSG、Hunyuan3D）生成的顶点数显著高于ReLi3D（100k+ vs 4.5k），但不影响图像与材质指标的比较。重光照评估中ReLi3D使用自身预测环境图而对比方法输入真实环境图的设计，使ReLi3D的优势更为保守可信。

### 补充图表

![[assets/figures/papers/paper_list_l59_https_openreview_net_forum_id_BlSKgQb3Vd/figures/005_Table_1.jpg]]
*Table 1: Relighting & Image & PBR Metrics Comparison. (Left) Relighting performance. (Middle) Image reconstruction performance. (Right) PBR material reconstruction performance. While most methods produce only global PBR parameters, ours produce spatially varying material maps which increase in quality with more views*

![[assets/figures/papers/paper_list_l59_https_openreview_net_forum_id_BlSKgQb3Vd/figures/006_Table_2.jpg]]
*Table 2: 3D and Image Metrics. ReLi3D clearly achieves SOTA in single and sparse multi-view reconstruction while also achieving great speeds. It is worth noting that that TripoSG and Hunyuan3D also produce signficantly higher vertex counts (100k+ vs 4.5k for ours)*

![[assets/figures/papers/paper_list_l59_https_openreview_net_forum_id_BlSKgQb3Vd/figures/007_Table_3.jpg]]
*Table 3: Real-world Evaluation on Stanford ORB. Quantitative evaluation on Stanford ORB dataset showing 3D reconstruction, image quality, and basecolor material prediction performance. Our method outperforms baselines across all metrics and improves with more input views*

![[assets/figures/papers/paper_list_l59_https_openreview_net_forum_id_BlSKgQb3Vd/figures/015_Table_4.jpg]]
*Table 4: Quantitative evaluation of illumination disentanglement. Comparison of environment map prediction and relighting quality on Polyhaven+HDRI dataset*

![[assets/figures/papers/paper_list_l59_https_openreview_net_forum_id_BlSKgQb3Vd/figures/016_Table_6.jpg]]
*Table 6: Training stage contribution analysis. Average share of the total improvement from Phase 1 (128 Gaussians) to the full Monte Carlo stage that is attributable to each intermediate stage. Columns aggregate the metrics shown in Table 1: (1) 3D coverage (CD and FS@0.05–0.5), (2) image quality (PSNR, SSIM, LPIPS), (3) basecolor (PSNR, SSIM, LSSIMSE), (4) roughness (PSNR, SSIM, RMSE), and (5) metallic (PSNR, SSIM, RMSE). Early Gaussian stages mainly expand 3D coverage, while the Monte Carlo refinement sharpens PBR material disentanglement*

![[assets/figures/papers/paper_list_l59_https_openreview_net_forum_id_BlSKgQb3Vd/figures/017_Table_7.jpg]]
*Table 7: Hero view selection sensitivity. Comparison of metrics using random hero view selection versus always selecting the most frontal view on the Polyhaven dataset*

![[assets/figures/papers/paper_list_l59_https_openreview_net_forum_id_BlSKgQb3Vd/figures/003_Figure_3.jpg]]
*Figure 3: PBR & Relighting Results. We show that our spatially varying PBR prediction is faithful to the ground truth and therefore produces highly detailed and realistic relightings*

![[assets/figures/papers/paper_list_l59_https_openreview_net_forum_id_BlSKgQb3Vd/figures/004_Figure_4.jpg]]
*Figure 4: Illumination Comparison. (Left) Single view, illumination prediction results compared to ground truth and SPAR3D, which also predicts RENI++ latents, indicating our severely improved method. (Right) Influence of increasing numbers of views and background information. Notice how well we can predict the illumination in the top rows with background information locate light sources correctly, whereas the bottom row is more spread out as it is inferred from diffuse surface reflections only*

![[assets/figures/papers/paper_list_l59_https_openreview_net_forum_id_BlSKgQb3Vd/figures/014_Figure_10.jpg]]
*Figure 10: Illumination Comparison. Comparison of illumination prediction results between DiffusionLight, SPAR3D, and our method (ReLi3D). Predicted environmens vary vastly while ours mimics the ground truth shape and color, DiffusionLight hallucinates a completely different environment, SPAR3D fails*

![[assets/figures/papers/paper_list_l59_https_openreview_net_forum_id_BlSKgQb3Vd/figures/010_Figure_7.jpg]]
*Figure 7: Reconstruction Results (Real World). Our method produces accurate reconstructions for real-world data, although challenging. Incorporating multiple views improves the performance further by clearing up uncertainties in unseen areas*

![[assets/figures/papers/paper_list_l59_https_openreview_net_forum_id_BlSKgQb3Vd/figures/011_Figure_8.jpg]]
*Figure 8: Real-world material prediction. Material maps (albedo, roughness, metallic, normal) for real-world objects from UCO3D dataset on very challenging settings, strong reflections and blur. Our method is still able to make a rough prediction and faithfully separates metallic and non-metallic materials*

## 方法谱系与知识库定位

### 1. 问题定位：从单视角不适定到多视角约束

单视角图像到三维重建中，材质与光照的解耦本质上是一个严重不适定问题——同一个二维外观可以由无数种表面反射率与入射光照的组合产生。这一根本性模糊导致现有方法在材质估计和法线预测上不可靠，进而限制了重光照的真实感。**ReLi3D** 的核心洞察在于：多视角观测对同一表面点在不同视角下的一致性约束，能够显著缩小材质与光照的可行解空间。通过将不适定的单视角问题转化为可约束的多视角问题，ReLi3D 首次在单次前馈推理中联合重建网格、空间变化 PBR 材质和 HDR 环境光。

### 2. 与基线方法的关键差异

ReLi3D 在五个关键维度上区别于现有工作：

**（1）输入模态：从单视图到任意多视图**

现有前馈重建方法大多以固定单视图为输入。**SF3D**（Boss et al., 2024）作为代表性单视图基线，仅能利用单一视角信息，缺乏跨视角几何一致性约束。ReLi3D 通过共享交叉条件变换器（Cross-conditioning Transformer）支持 1–16 个任意数量视图的融合，利用多视图间的视差与遮挡关系为材质-光照解耦提供额外约束。实验表明，从单视图到四视图，图像 PSNR 从 19.57 dB 提升至 21.43 dB（Table 2），验证了多视图信息对重建质量的正向贡献。

**（2）材质表示：从全局 BRDF 到空间变化 svBRDF**

**SF3D** 仅预测全局粗糙度和金属度参数，无法表达物体表面的材质变化。**SPAR3D**（Huang et al., 2025）虽采用生成式+回归的混合架构，但其 PBR 预测仍限于全局参数。ReLi3D 引入五个独立 MLP 头，从 triplane 特征联合预测密度、空间变化反照率、粗糙度、金属度和凹凸法线贴图（Eq. 9），并通过 Flexicubes 提取网格后以快速 UV 展开进行纹理映射。在 Polyhaven + Blender Shiny 数据集上，ReLi3D 的基色 PSNR 达到 25.00 dB，而 SF3D 的全局基色 PSNR 仅为 18.42 dB（Table 1），差距达 +6.58 dB。

**（3）光照估计：从无环境光到 HDR 环境图预测**

**SF3D** 完全不估计环境光照，无法支持重光照应用。**DiffusionLight**（Phongthawee et al., 2023）虽能从单图预测 HDR 环境图，但依赖扩散模型迭代推理，速度慢（21.46s）且易产生与输入场景不一致的幻觉光照。ReLi3D 采用基于 RENI++ 的 HDR 环境图预测（Eq. 1, 10–12），通过掩膜感知 DINOv2 token 和专用 1D 变换器，在 0.34s 内完成光照估计。在 Polyhaven + HDRI 数据集上，ReLi3D 的重光照 PSNR 达 20.88 dB，显著优于 SPAR3D 的 17.10 dB（Table 4）。

**（4）渲染监督：从不可微渲染到可微分物理渲染**

**SF3D** 和早期 LRM 系列方法依赖不可微渲染或纯图像空间损失进行监督，缺乏对材质-光照物理解耦的强制约束。ReLi3D 引入可微分蒙特卡洛多重重要性采样（MC+MIS）渲染器，采用 VNDF 采样、球帽与对抗采样的可微分路径追踪，在训练中强制物理一致性。消融实验表明，移除 MC 渲染器后图像重建 PSNR 从 19.92 dB 降至 17.54 dB（Table 5），证明物理渲染是材质-光照解耦的必要组件，而非优化细节。

**（5）训练数据域：从纯合成到混合域泛化**

**SF3D**、**LRM** 等方法仅在纯合成数据上训练，面对真实世界图像时泛化能力有限。ReLi3D 构建了包含 174k 对象的混合域训练集——42k 合成 PBR 数据提供材质真值监督，70k 合成 RGB-only 数据扩展形状多样性，62k 真实世界 UCO3D 捕获数据通过图像空间自监督弥合 sim-to-real 差距（Section 5.1）。在 Stanford ORB 真实世界数据集上，ReLi3D 在所有三维重建、图像质量和基色预测指标上均优于基线（Table 3）。

### 3. 方法谱系中的定位

ReLi3D 处于前馈三维重建与逆向渲染的交叉地带。与生成式方法（如 **Hunyuan3D**，Zhao et al., 2025；**3DTopia-XL**，Chen et al., 2024）相比，ReLi3D 不依赖扩散模型的迭代去噪，推理速度达 0.28s（Hunyuan3D 为 69.40s，约 250× 加速）。与基于优化的逆向渲染方法相比，ReLi3D 实现了单次前馈推理，无需逐场景优化。其双路径架构——几何与外观路径和光照路径——通过共享交叉条件变换器统一，代表了将物理渲染嵌入前馈网络的新范式。

训练阶段的贡献分析（Table 6）揭示了有趣的动态：早期高斯近似阶段主要贡献几何覆盖提升（70–80%），而最终 MC 微调阶段贡献了大部分材质解耦提升——基色提升 53.5%、粗糙度提升 62.4%、金属度提升 51.3%。这表明物理渲染约束在训练后期对材质-光照分离起到决定性作用。

### 4. 适用边界与局限

ReLi3D 的适用边界受以下因素制约：

- **光照先验分布限制**：当环境光照超出 RENI++ 先验分布（如多个极亮、局域化点光源）时，解耦易失败，材质图中出现烘焙光照伪影。
- **强自遮挡阴影**：强自遮挡阴影区域导致材质图残留光照效果，难以完全分离。
- **极暗场景退化**：极暗场景使基色预测困难，材质估计质量显著下降。
- **三平面分辨率瓶颈**：受限于 3×40×384×384 的三平面分辨率，纹理与几何细节存在丢失，在某些重建中表现为模糊。
- **透明物体未建模**：透明表面仅靠密度场处理，显式网格重建透明表面仍是一个开放挑战。
- **相机位姿假设**：方法假设已知相机位姿；当位姿估计严重错误时（如使用 DUST3R 产生大误差），会出现模糊伪影。
- **多视图扩散生成图像的视角不一致**：当前使用扩散模型生成的多视图图像若存在视角不一致，会导致性能下降。

### 5. 开放问题

基于上述局限，以下几个方向值得进一步探索：

1. **光照表示扩展**：如何扩展光照表示（如高清 HDR 环境图或隐式神经表示）以覆盖 RENI++ 先验外的强点光源场景？
2. **三平面容量提升**：能否通过分层三平面或自适应分辨率提升三平面容量，在几乎不增加推理时间的情况下改善细节重建？
3. **透明表面建模**：透明表面的显式网格重建与材质估计如何整合进当前前馈框架？
4. **与扩散模型协同**：能否利用生成的多视图图像与粗糙的 3D 代理模型联合训练，使 ReLi3D 在扩散模型产出的图像上也能够可靠工作？

### 6. 证据强度评估

ReLi3D 的核心主张获得了较充分的实验支撑。多视角约束改善材质-光照解耦的洞察在 Abstract 中明确陈述，并在 Table 1 和 Table 4 中获得量化验证。MC+MIS 渲染器的必要性通过消融实验（Table 5）得到证实。训练阶段贡献分析（Table 6）为物理渲染在材质解耦中的关键作用提供了因果证据。混合域训练策略的有效性通过 Stanford ORB 真实世界评估（Table 3）得到支持。需要注意的是，公平性方面，所有几何评估前均对预测网格施加刚性 ICP 对齐至真值网格，以补偿基线方法生成任意规范空间的偏差；重光照评估中，ReLi3D 使用自身预测的环境图而对比方法若支持则输入真实环境图，这使 ReLi3D 的优势更具说服力。

## 原文 PDF

![[paperPDFs/ICLR_2026/ReLi3D_Relightable_Multi_view_3D_Reconstruction_with_Disentangled_Illumination_5eeafb1d146e.pdf]]