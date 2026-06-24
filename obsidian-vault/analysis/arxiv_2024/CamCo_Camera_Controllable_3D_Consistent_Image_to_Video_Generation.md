---
title: "CamCo: Camera-Controllable 3D-Consistent Image-to-Video Generation"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/CamCo_Camera_Controllable_3D_Consistent_Image_to_Video_Generation.pdf
aliases:
- CamCo
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 相机参数化方式（Plücker坐标 vs. 一维标量/外参）与跨帧注意力机制（极线约束注意力 vs. 密集自注意力）是决定相机控制精度和几何一致性的核心调节变量。
primary_logic: 将每像素的相机射线用Plücker坐标编码为密集的条件信号，并在特征空间沿极线进行交叉注意力，可以同时实现细粒度相机控制和投影几何一致的视频生成。
claims:
- Plücker坐标比一维外参更能精确控制复杂相机轨迹，配合极线注意力使COLMAP重建误差率降至3.8%，远低于此前方法。
- 极线约束注意力模块将跨帧注意力限制在几何合理的像素上，消除了“像素拷贝”伪影，使匹配点数量提升至461.07。
- 在WebVid上通过Particle‑SfM构建的高质量动态视频数据集有效改善了目标运动生成，FID从静态场景的14.66变为动态场景的22.19，仍显著优于基线。
- RealEstate10K (静态场景) 上 FID = 14.66
---

# CamCo: Camera-Controllable 3D-Consistent Image-to-Video Generation

> [!tip] 核心洞察
> 将每像素的相机射线用Plücker坐标编码为密集的条件信号，并在特征空间沿极线进行交叉注意力，可以同时实现细粒度相机控制和投影几何一致的视频生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | CamCo：相机可控的三维一致图像到视频生成 |
| 英文题名 | CamCo: Camera-Controllable 3D-Consistent Image-to-Video Generation |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2406.02509) · [Project](https://ir1d.github.io/CamCo/) · [Code](https://github.com/kakaobrain/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | CamCo |
| Dataset | RealEstate10K |

> [!tip] 效果简介
> - RealEstate10K (静态场景) 上，FID 14.66 vs N/A (优于所有对比方法) (达到文中最佳)；FVD 138.01 vs N/A (显著低于其他方法) (达到文中最佳)；COLMAP 重建误差率 3.8% vs SVD / VideoCrafter / MotionCtrl 均更高 (近于其他方法的1/10)。
> - 动态场景 (WebVid‑SfM) 上，FID 22.19 vs N/A (明显优于基线) (在动态视频上仍保持最佳视觉质量)。

## 概述

**问题瓶颈**：现有图像到视频扩散模型（如 Stable Video Diffusion、VideoCrafter、MotionCtrl）缺乏精确的 6‑DoF 相机姿态控制，且未显式建模跨帧几何一致性，导致生成视频的相机运动不可靠，三维结构常出现“像素拷贝”等伪影。

**核心思路**：CamCo 提出两个相互配合的调节变量——**相机参数化方式**与**跨帧注意力机制**。将每像素的相机射线用 Plücker 坐标编码为密集条件信号，并在特征空间沿极线执行交叉注意力，同时实现细粒度相机控制和投影几何一致的视频生成。

**方法定位**：CamCo 在预训练图像到视频扩散模型 **Stable Video Diffusion (SVD)** 之上构建，冻结大部分基础权重，仅注入轻量的相机控制适配器和极线约束注意力模块，属于参数高效的后训练可控生成方案。相比使用一维外参矩阵调制的 **MotionCtrl**（相机控制基线），CamCo 将相机表示从全局标量提升为像素级几何嵌入，并将跨帧交互从密集自注意力收紧为极线约束注意力。

**关键结果**：
- 在 RealEstate10K 静态场景上，CamCo 的 COLMAP 重建误差率仅为 **3.8%**，远低于 SVD、VideoCrafter 和 MotionCtrl（Table 1）；匹配点数达到 **461.07**，表明几何一致性显著提升。
- 平移误差（2.67）和旋转误差（7.02）均为对比方法中最低。
- 在 WebVid 动态视频上微调后，FID 为 22.19，仍明显优于基线，验证了模型在保留目标运动的同时维持相机控制的能力（Table 3）。
- 消融实验证实，Plücker 坐标和极线约束注意力各自对控制精度和几何一致性至关重要，移除任一组件均导致指标显著恶化（Table 2）。

**局限与开放问题**：当前模型假设所有帧相机内参相同，无法实现变焦效果；生成分辨率限于 256×256、长度限于 14 帧。如何扩展到更长序列、更高分辨率，以及处理内参时变的复杂轨迹，是后续研究的方向。

## 背景与动机

### 图像到视频生成的进展与瓶颈

图像到视频（Image-to-Video, I2V）生成旨在从单张静态图像出发，合成一段具有时间连续性的动态视频。近年来，基于扩散模型（Diffusion Models）的视频生成方法取得了显著进展，其核心思路是将图像扩散模型扩展至时空维度，在大量视频数据上学习从噪声到视频帧的去噪映射。典型的生成范式基于**概率流常微分方程（Probability Flow ODE）**：

$$d \mathbf{x} = - \dot{\sigma}(t) \sigma(t) \nabla_{\mathbf{x}} \log p(\mathbf{x}; \sigma(t)) dt$$

模型通过**去噪分数匹配（Denoising Score Matching）**进行训练，最小化预测去噪结果与干净数据之间的 $L_2$ 损失：

$$\mathbb{E} \left[ \| D_{\pmb{\theta}} ( \mathbf{x}_0 + \mathbf{n}; \sigma, \mathbf{c} ) - \mathbf{x}_0 \|_2^2 \right]$$

在推理阶段，**分类器无关引导（Classifier-Free Guidance）**被广泛用于调节条件信号的强度：

$$D_{\omega}(\mathbf{x}; \mathbf{c}) = \omega ( D(\mathbf{x}; \mathbf{c}) - D(\mathbf{x}; \emptyset) ) + D(\mathbf{x}; \emptyset)$$

尽管这些技术使视频生成的质量和多样性大幅提升，但现有方法在**相机控制**和**三维几何一致性**两个关键维度上存在根本性缺陷。

### 现有方法的两个核心缺口

**缺口一：缺乏精确的 6-DoF 相机姿态控制。** 主流的图像到视频生成模型（如 Stable Video Diffusion, SVD）在生成过程中未提供任何相机姿态控制接口，用户无法指定生成视频的相机运动轨迹。少数具备相机控制能力的方法（如 MotionCtrl）将相机外参压缩为一维标量值，通过时间嵌入调制的方式注入模型。这种粗糙的参数化方式丢失了相机内参（焦距、主点）和外参（旋转、平移）的完整信息，导致对复杂相机轨迹（如弧形运动、推拉镜头）的控制精度严重不足。

**缺口二：未显式建模跨帧几何一致性。** 现有视频扩散模型普遍采用**时空密集自注意力（Spatio-Temporal Dense Self-Attention）**机制，允许任意帧的任意像素关注其他帧的所有位置。这种无约束的注意力模式虽然赋予了模型较大的表达自由度，但也带来了严重的几何不一致问题——模型倾向于通过“像素拷贝”的方式生成相邻帧的对应区域，而非基于真实的三维场景结构进行投影变换。其后果是生成的视频在结构上不可靠，无法通过多视角几何验证（如 COLMAP 重建）。

### 核心动机与调节变量

上述两个缺口揭示了视频生成领域的一个深层瓶颈：**相机参数化方式**与**跨帧注意力机制**是决定相机控制精度和几何一致性的核心调节变量。具体而言：

- **相机参数化方式**：从一维标量外参到像素级密集射线编码的转变，直接决定了模型能否感知并精确执行细粒度的相机运动指令。
- **跨帧注意力机制**：从无约束密集自注意力到几何约束交叉注意力的转变，直接决定了生成帧之间是否满足投影几何一致性。

CamCo 的核心动机正是围绕这两个调节变量展开：通过将每像素的相机射线用 **Plücker 坐标**编码为与特征图空间对齐的密集条件信号，并在特征空间沿**极线（Epipolar Line）**进行约束性交叉注意力，同时实现细粒度相机控制和投影几何一致的视频生成。这一设计使得生成的视频帧之间满足真实相机成像的几何约束，从而在 COLMAP 重建等下游任务中表现出显著优势——COLMAP 重建误差率降至 3.8%，远低于此前方法（Table 1），匹配点数量提升至 461.07，验证了所生成视频的三维结构可靠性。

## 核心创新

CamCo 的核心创新在于将**精确的 6‑DoF 相机控制**与**跨帧几何一致性**同时注入预训练的图像到视频扩散模型，解决了此前方法在相机可控性与三维结构保真度之间的根本矛盾。其创新围绕两个因果调节变量展开：**相机参数化方式**与**跨帧注意力机制**。

### 从一维外参到 Plücker 坐标：相机控制的粒度跃迁

现有相机控制方法（如 **MotionCtrl**）将相机外参压缩为一维标量或低维嵌入，通过时间嵌入调制注入网络。这种粗糙的参数化丢失了像素级几何信息，无法精确描述复杂相机轨迹。CamCo 改用 **Plücker 坐标** 对每条像素射线进行密集编码：给定像素 $(u,v)$，其 Plücker 嵌入为 $(\mathbf{o} \times \mathbf{d}', \mathbf{d}')$，其中 $\mathbf{o}$ 为相机原点，$\mathbf{d}'$ 为归一化射线方向。这一表示同时编码了相机内参和外参，形成与特征图空间对齐的密集条件信号。

在每个时间注意力块中，Plücker 嵌入与网络特征沿通道拼接后通过 $1 \times 1$ 卷积投影，以零初始化部分权重保证训练初期不破坏预训练生成能力。消融实验证实，去除 Plücker 坐标（w/o Plücker）或替换为一维相机矩阵（1‑dim camera）均导致 COLMAP 重建误差率显著升高，相机控制精度大幅下降（Table 2）。

### 从密集自注意力到极线约束注意力：几何一致性的机制保障

预训练视频扩散模型（如 SVD）使用时空密集自注意力，任意像素可跨帧关注任意位置。这在相机运动场景下产生“像素拷贝”伪影——模型倾向于直接复制源帧纹理而非合成符合投影几何的新视图。CamCo 的 **极线约束注意力（ECA）** 模块从根本上改变了这一机制：对于目标帧 $i$ 的每个查询像素，ECA 仅沿其在源帧（第一帧）上的极线采样特征，并执行交叉注意力：

$$\mathrm{ECA}(z_t^i, E_t^i) = \sigma\left(\frac{q k^T}{\sqrt{d}}\right) v \in \mathbb{R}^{hw \times d}$$

其中极线由参数方程 $\mathbf{L} = \mathbf{o} + c(\mathbf{p} - \mathbf{o})$ 定义，$E_t^i$ 为沿潜在空间极线采样的特征，同时编码了图像空间中的局部区域信息。ECA 的复杂度为 $O(hwl)$（$l$ 为极线采样点数），远低于密集注意力的 $O((hw)^2)$。

消融实验表明，移除极线约束注意力（w/o epipolar attention）使 COLMAP 匹配点数从 461.07 大幅下降，几何一致性显著恶化（Table 2）。这一模块是消除“像素拷贝”伪影、实现投影几何一致视频生成的关键。

### 动态场景的相机控制：数据管线创新

此前方法多在 RealEstate10K 等静态场景数据上训练，模型倾向于忽略目标运动。CamCo 引入了一套动态视频数据管线：从 WebVid 采样视频，使用 **Particle‑SfM** 估计相机姿态，并以重建稀疏点云的点数作为姿态标注质量的指示器，过滤出 12,000 段高质量序列。在此数据上微调后，CamCo 在动态场景上仍保持最佳视觉质量（FID 22.19，Table 3），证明 Plücker 坐标与 ECA 的组合对相机和目标运动具有解耦建模能力。

### 创新总结

CamCo 的三项 changed slots——**Plücker 坐标**（相机表示）、**极线约束注意力**（跨帧注意力机制）、**动态视频数据管线**（训练数据）——形成了完整的因果链条：Plücker 坐标提供像素级精确的相机条件，ECA 确保跨帧信息聚合符合投影几何，动态数据管线则赋予模型在目标运动存在时仍保持相机控制精度的能力。这一组合使 COLMAP 重建误差率降至 3.8%，近于此前方法的 1/10，同时匹配点数达到 461.07，大幅领先所有基线（Table 1）。

## 整体框架

CamCo 的整体 pipeline 以预训练的图像到视频扩散模型 **Stable Video Diffusion (SVD)** 为生成骨架，在其时间注意力块中注入两个关键模块，构成“相机控制 + 几何一致性”的双重约束生成框架。给定一张起始帧图像和一段相机轨迹序列，系统输出一段 14 帧、分辨率为 256×256 的视频，该视频在遵循指定相机运动的同时保持跨帧的三维结构一致性。

### 输入与输出流

**输入**包含两部分：
1. **起始帧图像** $I_0$：作为视频生成的内容锚点。
2. **相机轨迹序列** $\{ \mathbf{P}_t \}_{t=1}^{T}$：每帧对应的 6‑DoF 相机外参矩阵，定义相机在世界坐标系中的位置和朝向。所有相机姿态均相对于第一帧定义，第一帧相机位于世界原点。

**输出**为一段 $T$ 帧的视频序列，其视觉内容与 $I_0$ 保持语义连贯，且相机运动严格遵循输入的轨迹。

### 核心模块与数据流

CamCo 的架构围绕三个核心模块构建（图 2），数据流自上而下贯穿 UNet 的多个时间注意力块：

**模块一：Plücker 坐标相机参数化与注入适配器**

相机轨迹中的每一帧外参矩阵首先被转换为 **Plücker 坐标**嵌入。Plücker 坐标将每条像素射线编码为一个 6 维向量 $(\mathbf{o} \times \mathbf{d}', \mathbf{d}')$，其中 $\mathbf{o}$ 为相机光心，$\mathbf{d}$ 为射线方向。这种逐像素的密集嵌入同时编码了相机内参和外参信息，形成与特征图空间严格对齐的条件信号。

在每个时间注意力块中，Plücker 嵌入与网络特征沿通道维度拼接，通过一个 $1 \times 1$ 卷积层投影回原始特征维度，再送入后续的注意力计算。该适配器采用零初始化策略，确保训练初期不干扰预训练模型的生成先验。

**模块二：极线约束注意力（ECA）**

替换原有时间注意力块中的密集自注意力机制。对于目标帧 $i$ 的每个查询像素，ECA 不再允许其关注源帧（第一帧）的所有位置，而是仅沿该像素在源帧上对应的**极线**采样特征，执行交叉注意力：

$$
\mathrm{ECA}(z_t^i, E_t^i) = \sigma\left(\frac{q k^T}{\sqrt{d}}\right) v \in \mathbb{R}^{hw \times d}
$$

其中 $z_t^i$ 为目标帧 $i$ 在去噪时间步 $t$ 的隐空间特征，$E_t^i$ 为沿极线采样的源帧特征集合。这一约束将跨帧信息聚合限制在投影几何所允许的像素对应关系内，从根本上抑制了“像素拷贝”等几何不一致伪影。

**模块三：动态视频数据管线**

为保留真实场景中的目标运动，CamCo 引入了一条从 WebVid 数据集中筛选高质量动态视频的管线。该管线使用 **Particle‑SfM** 估计每段视频的相机姿态，并以重建稀疏点云的点数作为标注质量指标，过滤出 12,000 段高置信度序列。这些序列同时包含相机运动和场景目标运动，用于微调 CamCo，使其在控制相机的同时不丧失生成目标运动的能力。

### 训练与推理流程

**训练阶段**，模型在 RealEstate10K 静态场景数据上完成基础训练，随后在筛选后的 WebVid 动态视频上微调。训练目标为标准的去噪分数匹配损失：

$$
\mathbb{E} \left[ \| D_{\pmb{\theta}} ( \mathbf{x}_0 + \mathbf{n}; \sigma, \mathbf{c} ) - \mathbf{x}_0 \|_2^2 \right]
$$

其中 $\mathbf{c}$ 包含起始帧图像和 Plücker 相机条件。

**推理阶段**，模型从随机噪声出发，通过概率流 ODE 迭代去噪：

$$
d \mathbf{x} = - \dot{\sigma}(t) \sigma(t) \nabla_{\mathbf{x}} \log p(\mathbf{x}; \sigma(t)) dt
$$

并采用分类器无关引导控制条件强度：

$$
D_{\omega}(\mathbf{x}; \mathbf{c}) = \omega ( D(\mathbf{x}; \mathbf{c}) - D(\mathbf{x}; \emptyset) ) + D(\mathbf{x}; \emptyset)
$$

### 模块间的因果关联

三个模块形成清晰的因果链：**Plücker 坐标**提供细粒度的相机控制信号（调节变量：相机参数化粒度），**ECA 模块**将这种控制约束在几何合理的像素对应中（调节变量：跨帧注意力范围），而**动态数据管线**则确保模型在获得精确几何约束的同时不退化目标运动生成能力。消融实验（Table 2）证实，移除任一模块均会导致相机控制精度或视觉质量的显著下降。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2406_02509/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our proposed CamCo framework. (a) shows the architecture, where we introduce Plücker coordinates as an effective camera parameterization and an epipolar constraint attention block to enforce geometry consistency. (b) illustrates our epipolar constraint attention block. For each queried pixel via grid sampling from the i-th frame $z _ { t } ^ { i }$ , we gather information from the corresponding epipolar line in the source frame $z _ { t } ^ { 1 }$ using a cross-attention layer. The features $E _ { t } ^ { i }$ along the latent space epipolar line encode the local regions around it in the image space*

## 核心模块与公式推导

### 3.1 预备知识：扩散模型框架

CamCo 建立在连续时间扩散模型的理论基础之上。给定干净数据 $\mathbf{x}_0$，前向扩散过程通过逐步注入高斯噪声 $\mathbf{n}$ 生成噪声样本 $\mathbf{x}$，其噪声水平由 $\sigma(t)$ 控制。逆向去噪过程等价于求解概率流常微分方程（Probability Flow ODE）：

$$d \mathbf{x} = - \dot{\sigma}(t) \sigma(t) \nabla_{\mathbf{x}} \log p(\mathbf{x}; \sigma(t)) dt \tag{1}$$

模型训练的目标是最小化去噪分数匹配损失，即让去噪网络 $D_{\pmb{\theta}}$ 从噪声样本中恢复干净数据：

$$\mathbb{E} \left[ \| D_{\pmb{\theta}} ( \mathbf{x}_0 + \mathbf{n}; \sigma, \mathbf{c} ) - \mathbf{x}_0 \|_2^2 \right] \tag{2}$$

其中 $\mathbf{c}$ 为条件信号。推理时，采用分类器无关引导（Classifier-Free Guidance）来调节条件强度：

$$D_{\omega}(\mathbf{x}; \mathbf{c}) = \omega ( D(\mathbf{x}; \mathbf{c}) - D(\mathbf{x}; \emptyset) ) + D(\mathbf{x}; \emptyset) \tag{3}$$

其中 $\omega$ 为引导系数，$\emptyset$ 表示空条件。CamCo 以预训练的图像到视频扩散模型 SVD 为基础生成器，保持其大部分权重不变，在此基础上引入相机控制与几何约束模块。

### 3.2 相机参数化：Plücker 坐标嵌入

**设计动机**：现有方法（如 MotionCtrl）将相机外参编码为一维标量向量，通过时间嵌入调制网络特征。这种方式丢失了像素级几何信息，无法精确控制复杂相机轨迹。CamCo 采用 Plücker 坐标作为相机表示，将每条像素对应的相机射线编码为密集的、与特征图空间对齐的嵌入。

**Plücker 坐标编码**：对于图像中的每个像素，其对应的相机射线由相机原点 $\mathbf{o}$ 和射线方向 $\mathbf{d}$ 定义。Plücker 坐标将该射线表示为六维向量 $(\mathbf{o} \times \mathbf{d}', \mathbf{d}')$，其中 $\mathbf{d}'$ 为归一化方向向量。这一表示同时编码了相机内参（决定射线方向分布）和外参（决定原点位置和朝向），形成像素级密集条件信号。

**条件注入方式**：在每个时间注意力块中，将 Plücker 嵌入与网络特征沿通道维度拼接，通过 $1 \times 1$ 卷积层投影回原始特征维度。该适配器层采用零初始化策略，确保训练初期不破坏预训练模型的生成先验。

### 3.3 极线约束注意力（ECA）

**问题分析**：标准视频扩散模型中的时空自注意力允许任意像素关注其他帧的任意位置。这导致模型可能通过“像素拷贝”伪造相机运动——即直接复制源帧像素到目标帧对应位置，而非基于真实几何投影生成新视图，产生三维不一致的伪影。

**ECA 机制**：极线约束注意力模块替换原有的跨帧密集自注意力。对于目标帧 $i$ 的特征图 $z_t^i$，每个查询像素仅沿源帧（第一帧）上对应的极线采样特征 $E_t^i$，并执行交叉注意力：

$$\mathrm{ECA}(z_t^i, E_t^i) = \sigma\left(\frac{q k^T}{\sqrt{d}}\right) v \in \mathbb{R}^{hw \times d} \tag{4}$$

其中 $q$ 为目标帧特征的查询投影，$k$、$v$ 为极线采样特征的键和值投影，$d$ 为特征维度。极线参数方程由相机几何给出：

$$\mathbf{L} = \mathbf{o} + c \left( \mathbf{p} - \mathbf{o} \right) \tag{6}$$

其中 $\mathbf{o}$ 为相机原点，$\mathbf{p}$ 为三维点投影到图像平面的坐标，$c$ 为实参数。ECA 的计算复杂度为 $O(hwl)$，其中 $l$ 为极线采样点数，远低于密集注意力的 $O((hw)^2)$。

**几何意义**：根据对极几何，目标帧中某像素对应的三维点必然位于源帧的极线上。ECA 将注意力搜索空间限制在这一几何合理的区域内，从机制层面强制跨帧特征聚合遵循投影几何约束，消除像素拷贝伪影，确保生成视频的三维一致性。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2406_02509/figures/001_Figure_1.jpg]]
*Figure 1: Given a single frame (the first image column) and a sequence of cameras as input, our CamCo model is able to synthesize videos that follow the camera conditions with 3D consistency. We support indoor, outdoor, object-centric, and text-to-image generated images. The prompt for the last row is “A lush garden filled with blooming roses of various colors, with a gravel path winding through it”. The camera of the first frame starts from world origin, shown in purple*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2406_02509/figures/003_Figure_3.jpg]]
*Figure 3: Static scene video generation results. The last column provides reference videos that visualize the camera trajectories. The images and trajectories are unseen during training. Regions are highlighted to reveal camera motion. Please check the video results for better visualizations on the project page: https://ir1d.github.io/CamCo/*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2406_02509/figures/004_Figure_4.jpg]]
*Figure 4: Dynamic scene video generation results where the first frame is generated by SDXL [34] from the prompt in the left. The last column provides reference videos that visualize the camera trajectories. The trajectories are unseen during training. Regions are highlighted to reveal camera motion and object motion better. Please check the video results for better visualizations on the project page: https://ir1d.github.io/CamCo/*

## 实验与分析

### 评估设置

CamCo在两类场景上进行系统评估：**静态场景**（RealEstate10K数据集）和**动态场景**（从WebVid构建的高质量子集）。静态场景评估主要考察相机控制的精确性和生成视频的3D几何一致性；动态场景评估则进一步考察模型在保留目标运动的同时执行相机运动的能力。

评估指标分为两个维度：
- **视觉质量指标**：FID（Fréchet Inception Distance）和FVD（Fréchet Video Distance），衡量生成视频的视觉逼真度。
- **相机控制与几何一致性指标**：使用COLMAP对生成视频进行稀疏重建，报告**COLMAP重建误差率**（成功注册帧的比例，越低越好）、**匹配点数量**（重建稀疏点云中的点数，越高表示几何一致性越好）、**相对旋转误差** $R_{\mathrm{err}}$ 和**相对平移误差** $T_{\mathrm{err}}$。

所有对比方法均使用作者发布的模型权重和默认推理设置，输入分辨率为256×256，相机轨迹均相对第一帧定义，COLMAP配置对所有方法统一。动态场景评估使用来自SDXL生成的相同起始帧，确保比较公平。

### 静态场景主结果

Table 1报告了CamCo与基线方法在RealEstate10K上的定量对比。CamCo在所有相机控制指标上均大幅领先：

- **COLMAP重建误差率**：CamCo仅3.8%，而MotionCtrl、VideoCrafter和SVD的误差率显著更高（约高一个数量级）。这表明CamCo生成的视频具有足够的跨帧几何一致性，使得SfM算法能够成功重建相机轨迹和稀疏场景结构。
- **匹配点数量**：CamCo达到461.07，远超其他方法。这意味着极线约束注意力机制有效避免了“像素拷贝”伪影，生成了真正符合投影几何的跨帧对应关系。
- **相机姿态误差**：CamCo的平移误差（2.6655）和旋转误差（7.0218）均为最低，证明Plücker坐标参数化能够精确控制6-DoF相机运动。

在视觉质量方面，CamCo的FVD（138.01）在所有方法中最佳，FID（14.66）也具有竞争力。值得注意的是，MotionCtrl虽然也支持相机控制，但其FVD和FID均劣于CamCo，且COLMAP误差率远高于CamCo，说明其一维外参矩阵参数化无法提供足够的控制精度。

Figure 3的定性对比进一步印证了定量结果：CamCo生成的视频帧间过渡平滑，场景结构保持稳定；而SVD和VideoCrafter缺乏相机控制能力，MotionCtrl虽然能产生一定的相机运动，但几何一致性差，存在明显的结构漂移和伪影。

### 动态场景主结果

Table 3报告了动态场景上的定量对比。由于动态视频中存在目标运动，所有方法的FID和FVD均较静态场景有所上升，但CamCo仍保持明显优势：
- CamCo的FID为22.19，显著优于SVD（27.59）、VideoCrafter（28.36）和MotionCtrl（25.01）。
- FVD方面，CamCo（246.19）同样领先于所有基线。

这一结果表明，通过Particle-SfM估计相机姿态并利用稀疏点云点数过滤高质量样本的策略是有效的——CamCo在保留目标运动的同时，仍能精确执行指定的相机轨迹。Figure 4展示了动态场景的定性结果：CamCo能够同时生成自然的相机运动（如推拉、平移）和场景中的目标运动（如人物动作、水流），而基线方法要么丢失了目标运动，要么相机运动与输入条件不一致。

### 消融实验

Table 2报告了系统的消融实验，验证了CamCo各核心组件的贡献：

- **去除Plücker坐标（w/o Plücker）**：仅保留极线约束注意力但移除Plücker坐标输入，COLMAP误差率显著上升，平移和旋转误差增大。这说明即使有几何约束的注意力机制，缺乏精确的相机条件信号仍会导致控制精度下降。
- **去除极线约束注意力（w/o epipolar attention）**：仅使用Plücker坐标但移除ECA模块，匹配点数量大幅下降，COLMAP误差率升高。这表明Plücker坐标提供了控制信号，但缺少几何约束会导致跨帧特征聚合时的空间不一致。
- **一维相机矩阵（1-dim camera）**：将Plücker坐标替换为一维外参矩阵，所有指标均变差，验证了密集像素级参数化对于细粒度相机控制的重要性。
- **时间嵌入调制（Time embedding）**：将Plücker坐标通过时间嵌入方式注入，而非在空间上与特征图拼接，控制精度同样下降，证明空间对齐的条件注入方式更有效。

完整模型（Plücker + ECA + 数据筛选）在所有指标上均取得最佳结果，证实了两个核心设计——Plücker坐标参数化和极线约束注意力——是互补且不可或缺的。

### 失败模式与局限性分析

尽管CamCo在静态和动态场景上均取得了显著进展，但实验和分析揭示了以下局限性：

1. **固定内参假设**：模型训练时假设所有视频帧具有相同的相机内参，因此无法在生成过程中改变内参。这意味着CamCo无法实现变焦镜头（dolly zoom）等需要内参变化的电影拍摄效果。当输入图像的视角与目标相机轨迹的预期视场不匹配时，生成质量可能下降。

2. **有限的分辨率和帧长**：当前模型仅支持256×256分辨率、14帧的视频生成。对于大范围场景漫游或长时间视频，14帧覆盖的视角有限，难以展示完整的3D场景结构。分辨率限制也影响了细节纹理的重建质量。

3. **动态场景的相机标注噪声**：Particle-SfM在动态场景中的相机姿态估计存在固有歧义——目标运动可能被误解释为相机运动，反之亦然。尽管通过稀疏点云点数过滤缓解了这一问题，但标注噪声仍可能影响目标运动的精确建模，导致某些动态场景中目标运动不够自然或相机轨迹偏离预期。

4. **极线退化情况**：当相机运动为纯平移时，极线可能极短或退化为点，此时ECA模块的采样范围受限，可能影响跨帧信息聚合的充分性。当前实现未包含针对退化情况的特殊处理。

### 关键图表结论

- **Table 1**：CamCo在静态场景上以3.8%的COLMAP误差率和461.07的匹配点数建立新的最优水平，证明Plücker坐标+极线约束注意力的组合能够实现精确相机控制和3D几何一致视频生成。
- **Table 2**：消融实验确认Plücker坐标和ECA模块各自独立且互补地贡献于最终性能，任何组件的移除都会导致相机控制精度或几何一致性的显著下降。
- **Table 3**：在动态场景上，CamCo通过高质量动态视频数据微调，成功保留了目标运动能力，FID（22.19）和FVD（246.19）均显著优于基线方法。
- **Figure 3 & 4**：定性结果直观展示了CamCo在静态和动态场景下均能生成相机运动精确、场景结构稳定、目标运动自然的视频，而基线方法存在几何不一致、相机漂移或目标运动丢失等问题。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2406_02509/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison against baseline methods on static videos. * denotes that the results of these metrics are averaged for sequences that are successfully processed by COLMAP*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2406_02509/figures/006_Table_2.jpg]]
*Table 2: Ablation studies on model variants. * denotes that the results of these metrics are averaged for sequences that are successfully processed by COLMAP*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2406_02509/figures/007_Table_3.jpg]]
*Table 3: Quantitative comparison on generated dynamic videos*

## 方法谱系与知识库定位

### 上游奠基：图像到视频扩散模型的相机控制演进

CamCo 直接构建于 **Stable Video Diffusion (SVD)** 之上，SVD 作为一个基于 UNet 的开源图像到视频扩散模型，提供了强大的视频生成先验，但其原始设计完全缺乏相机控制能力。在 CamCo 之前，**MotionCtrl** 是相机可控视频生成的主要基线，其核心思路是将相机外参矩阵展平为一维向量，通过时间嵌入调制的方式注入扩散模型。然而，MotionCtrl 的一维参数化方式存在本质缺陷：它将 6-DoF 相机姿态压缩为全局标量信号，丢失了像素级的几何对应关系，导致生成的视频在复杂相机轨迹下出现结构扭曲和三维不一致。

**VideoCrafter** 则代表了另一条技术路线——通过文本或条件信号引导视频生成，但同样未显式建模跨帧几何约束。这些方法在 COLMAP 重建误差率上表现不佳（远高于 CamCo 的 3.8%），匹配点数量也显著偏低，反映出其生成视频的底层三维结构不可靠。

### CamCo 的核心调节变量：从密集相机参数化到几何约束注意力

CamCo 的方法学突破在于识别并操控了两个决定相机控制精度和几何一致性的核心调节变量：

**调节变量一：相机参数化方式。** 从 MotionCtrl 的一维外参标量跃迁至 **Plücker 坐标**（受光场网络启发），将每条像素射线编码为 $(\mathbf{o} \times \mathbf{d}', \mathbf{d}')$ 的密集嵌入。这一参数化同时编码了相机内参与外参信息，且与特征图在空间上对齐，使得模型能够学习像素级的相机条件响应。消融实验（Table 2）证实，去除 Plücker 坐标（w/o Plücker）或退化为“1-dim camera”均导致所有指标显著恶化，验证了密集参数化对于细粒度相机控制的必要性。

**调节变量二：跨帧注意力机制。** 从 SVD 的时空密集自注意力（任意像素可关注其他帧任意位置，易产生“像素拷贝”伪影）转变为 **极线约束注意力（ECA）**。ECA 将目标帧的查询限制在源帧的极线上进行交叉注意力，复杂度从 $O(h^2 w^2)$ 降至 $O(h w l)$（$l$ 为极线采样点数），同时强制特征聚合遵循投影几何。消融实验显示，移除 ECA（w/o epipolar attention）后匹配点数下降，几何一致性显著恶化。

### 数据管线创新：从静态场景到动态世界的迁移

CamCo 的第三个关键贡献在于训练数据的扩展策略。此前方法（包括 SVD 和 MotionCtrl）主要在 **RealEstate10K** 等静态场景数据集上训练，导致模型倾向于生成静止背景，难以处理包含目标运动的真实视频。CamCo 通过引入 **WebVid** 动态视频并利用 **Particle-SfM** 进行相机姿态估计，构建了包含 12,000 段高质量序列的动态训练集。其数据筛选策略以稀疏点云重建点数作为相机标注质量的指标，仅保留姿态估计准确且目标运动显著的视频。这一数据管线使 CamCo 在动态场景上仍能保持 FID 22.19（Table 3），虽高于静态场景的 14.66，但仍显著优于基线方法。

### 适用边界与已知局限

CamCo 的设计包含以下固有假设和边界：

1. **固定内参假设：** 训练数据假设所有视频帧共享相同的相机内参，导致生成结果无法改变输入图像的内参。这意味着 CamCo 无法模拟变焦镜头效果（如 dolly zoom），限制了其在电影级拍摄技术中的应用。

2. **时空分辨率上限：** 当前模型仅支持生成 $256 \times 256$ 分辨率、14 帧长度的视频，覆盖的视角范围有限。对于需要大范围场景探索或长时间生成的应用（如虚拟漫游），现有能力不足。

3. **动态场景的姿态估计歧义：** Particle-SfM 在动态场景中估计相机姿态存在固有歧义——目标运动与相机运动难以精确解耦。这一因素可能影响训练标注质量，进而限制目标运动的精确建模。当场景中同时存在大幅度的相机运动和目标运动时，生成质量可能出现退化。

4. **极线退化的鲁棒性：** 当相机运动为纯平移（极线极短）或极线在图像边界外退化时，ECA 模块的几何约束可能失效。论文未明确讨论此类退化情况的处理策略，其鲁棒性需要进一步验证。

### 开放问题与后续方向

基于 CamCo 的方法框架和已知局限，以下开放问题值得后续工作探索：

- **长时序与高分辨率扩展：** 如何将 CamCo 的相机控制框架扩展到超过 14 帧的长视频生成，以及 $512 \times 512$ 或更高的分辨率？这需要解决长序列中的误差累积和注意力复杂度问题。

- **变内参轨迹支持：** 如何处理相机内参随时间变化的复杂轨迹？这要求 Plücker 坐标的参数化能够表达时变内参，同时训练数据需要包含变焦视频。

- **几何先验的深度融合：** ECA 目前仅依赖极线约束，是否可以与深度预测等几何先验结合？在缺乏精确深度信息时，引入单目深度估计作为辅助信号可能进一步提升 3D 一致性。

- **相机与目标运动的解耦：** 在更复杂的真实动态场景中，如何更准确地区分目标运动和相机运动？这可能需要联合优化运动分割与姿态估计，以提高动态训练数据的标注可靠性。

- **极线退化处理：** 当极线极短或退化时，ECA 机制是否需要额外的退化处理策略（如退化为局部窗口注意力）以保证鲁棒性？

## 原文 PDF

![[paperPDFs/arxiv_2024/CamCo_Camera_Controllable_3D_Consistent_Image_to_Video_Generation.pdf]]