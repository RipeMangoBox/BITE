---
title: "CamI2V: Camera-Controlled Image-to-Video Diffusion Model"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/CamI2V_Camera_Controlled_Image_to_Video_Diffusion_Model.pdf
project_link: https://zgctroy.github.io/CamI2V
code_link: https://github.com/hpcaitech/Open-Sora
aliases:
- CamI2V
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过极线注意力将跨帧特征聚合限制在极线上，排除了大部分噪声的随机干扰，只保留最相关的噪声条件。
primary_logic: 将跨帧噪声特征重新解释为一类噪声条件，其价值由减少不确定性的能力而非数量决定；极线约束提供了最优的噪声条件量，使得在高噪声下仍能保持一致的跨帧关系。
claims:
- 极线注意力能够有效利用极线约束大幅缩小匹配搜索空间，减少噪声误导。
- 在RealEstate10K数据集上，CamI2V的相机可控性（RotErr/CamMC/TransErr）相比CameraCtrl提升了25%以上。
- RealEstate10K 上 RotErr (↓) = 0.4758
- RealEstate10K 上 CamMC (↓) = 1.7153
---

# CamI2V: Camera-Controlled Image-to-Video Diffusion Model

> [!tip] 核心洞察
> 将跨帧噪声特征重新解释为一类噪声条件，其价值由减少不确定性的能力而非数量决定；极线约束提供了最优的噪声条件量，使得在高噪声下仍能保持一致的跨帧关系。

| 字段 | 内容 |
|------|------|
| 中文题名 | CamI2V：相机控制的图像到视频扩散模型 |
| 英文题名 | CamI2V: Camera-Controlled Image-to-Video Diffusion Model |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2410.15957) · [Project](https://zgctroy.github.io/CamI2V) · [Code](https://github.com/hpcaitech/Open-Sora) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | CamI2V |
| Dataset | RealEstate10K |

> [!tip] 效果简介
> - RealEstate10K 上，RotErr (↓) 0.4758 vs CameraCtrl: 0.7064 (-0.2306 (-32.96%))；CamMC (↓) 1.7153 vs CameraCtrl: 2.304 (-0.5887 (-25.64%))；TransErr (↓) 1.4955 vs CameraCtrl: 1.888 (-0.3925 (-20.77%))。

## 概要

图像到视频（I2V）生成的核心挑战在于，如何在给定单张图像和相机运动序列的条件下，生成几何一致且相机可控的视频。现有方法（如基于分离时空注意力的 **DynamiCrafter** (Xing et al., 2023) 或使用 Plücker 嵌入作为侧输入的 **CameraCtrl** (He et al., 2024a)）在噪声较大的扩散早期阶段，难以有效建模跨帧特征对应关系，导致生成的视频出现几何不一致和相机可控性下降。

CamI2V 的核心洞察在于重新审视扩散模型中“条件”的本质：条件的有用性取决于其减少不确定性的能力，而非其数量。在高噪声阶段，跨帧像素特征中的确定性信息被噪声淹没，成为不可靠的“噪声条件”。基于此，CamI2V 提出**极线注意力机制**（Epipolar Attention），利用对极几何约束将跨帧特征聚合限制在极线附近，从而大幅缩小匹配搜索空间，排除大部分噪声的随机干扰，使模型仅关注最相关的噪声条件（图 1、图 2）。

方法层面，CamI2V 以 DynamiCrafter 为基础模型，引入 Plücker 坐标作为全局 3D 光线位置编码，并在空间与时间注意力之间插入可插拔的极线注意力模块，同时辅以可学习的 register tokens 处理帧间无重叠区域。在 RealEstate10K 数据集上，CamI2V 相较此前最优方法 CameraCtrl 在相机可控性指标上取得显著提升：RotErr 降低 32.96%，CamMC 降低 25.64%，TransErr 降低 20.77%，且未牺牲生成质量和动态表现（表 1）。该方法训练仅需 24GB 显存，推理仅需约 12GB，具备在消费级 GPU 上部署的可行性。

### 扩散模型中的条件再思考

扩散模型通过沿对数概率密度函数的梯度方向逐步去噪来生成数据。在去噪初期，噪声水平较高，高密度区域呈现为大量噪声样本的重叠，导致视觉上的模糊不清。这一现象揭示了一个关键问题：**条件的有效性并不取决于其数量，而取决于它能在多大程度上减少不确定性**。

基于这一洞察，CamI2V 将扩散模型中的条件重新划分为两类（Figure 1）：

- **干净条件（clean conditions）**：在整个去噪过程中始终保持可见，例如文本描述、相机外参等。这类条件的信息始终是确定的，不受噪声水平影响。
- **噪声条件（noisy conditions）**：如当前帧和其他帧中被噪声污染的像素特征。其确定性信息 $\alpha_t x_0$ 会随着噪声 $\sigma_t \epsilon$ 的增大而逐渐被随机性淹没，使得高噪声阶段难以从中提取有效的跨帧关系。

这一分类为理解图像到视频生成中的相机控制问题提供了新的理论视角。

### 现有跨帧注意力机制的困境

在相机控制的图像到视频生成任务中，模型需要跨帧追踪由相机运动引起的像素位移，从而保持几何一致性。然而，现有注意力机制在高噪声条件下面临根本性困难（Figure 2）：

- **时间注意力（Temporal Attention）** 仅在图像的相同空间位置上进行特征交互。当相机发生显著运动时，对应像素已移动到完全不同位置，时间注意力完全失效。
- **3D 全注意力（3D Full Attention）** 拥有全局感受野，理论上可以追踪任意位移。但在高噪声水平下，噪声的随机性主导了特征表达，使得注意力难以区分真正的对应关系和噪声引起的虚假匹配，导致追踪不一致。

这两种机制都未能有效处理**噪声条件**的核心矛盾：跨帧特征中存在有用信息，但被大量噪声所掩盖。

### 核心动机：极线约束作为最优噪声条件

CamI2V 的核心动机源于一个关键发现：**对极几何约束能够将跨帧特征聚合限制在极线上，从而大幅缩小匹配搜索空间，排除大部分噪声的随机干扰**。从“条件减少不确定性”的视角看，极线约束提供了接近最优的噪声条件量——它保留了最相关的跨帧信息，同时过滤掉了绝大多数误导性的噪声特征。

具体而言，给定第 $i$ 帧上的一个像素 $(u, v)$，其在第 $j$ 帧上的对应点必然位于极线 $l_{ij}(u,v) = F_{ij} \cdot (u, v, 1)^{\mathrm{T}}$ 上，其中 $F_{ij}$ 为基础矩阵。这一几何先验使得模型无需在整幅图像中盲目搜索，而只需沿极线方向聚合特征，从根本上降低了噪声干扰的风险。

### 方法定位

基于上述动机，CamI2V 提出了一种结合 **Plücker 坐标嵌入**与**极线注意力机制**的相机控制框架。该方法以 **DynamiCrafter**（Xing et al., 2023）为基础图像到视频扩散模型，在架构层面引入显式的对极几何约束，替代 **CameraCtrl**（He et al., 2024a）中缺乏几何约束的 Plücker 侧分支注入方式。通过在空间注意力与时间注意力之间插入极线注意力模块，模型能够在高噪声条件下稳定地建模跨帧关系，从而实现更精确的相机可控性和 3D 一致性。

## 核心方法与创新机理

CamI2V 的核心创新在于重新审视了扩散模型中的条件信号，并提出了一种基于对极几何约束的跨帧注意力机制，以解决现有相机控制方法在高噪声条件下几何一致性与可控性不足的瓶颈。

### 1. 从“干净条件”到“噪声条件”的视角转换

传统扩散模型中的条件（如文本、相机外参）被视为“干净条件”——它们在去噪全过程中始终保持确定性。CamI2V 将这一概念扩展至跨帧特征：**当前帧及其他帧的含噪像素被重新解释为一类“噪声条件”**，其价值不由数量决定，而由它能在多大程度上减少不确定性来衡量（参见 Figure 1）。

这一视角转换揭示了一个关键瓶颈：在高噪声时间步，噪声条件中的确定性信息 $\alpha_t x_0$ 逐渐被随机噪声 $\sigma_t \epsilon$ 淹没。此时，不加约束的跨帧交互（如 3D 全注意力）反而会被噪声误导，导致几何不一致。

### 2. 极线注意力：用几何约束对抗噪声误导

基于上述洞察，CamI2V 提出了 **极线注意力（Epipolar Attention）** 机制，作为跨帧特征聚合的核心算子。其设计逻辑如下：

- **约束搜索空间**：对于第 $i$ 帧的像素 $(u,v)$，其在第 $j$ 帧上的对应点必然位于极线 $l_{ij}(u,v) = F_{ij} \cdot (u, v, 1)^{\mathrm{T}}$ 上。极线注意力通过离散极线掩码 $m$，将注意力计算限制在极线邻域（距离阈值 $\delta$ 内），从而将匹配搜索空间从整个帧平面缩减至一条线。
- **注意力形式**：$$\mathrm{EpipolarAttn}(q,k,v,m) = \mathrm{softmax}\left(\frac{q k^{\mathrm{T}}}{\sqrt{d}} \odot m\right) v$$ 先对注意力分数逐点乘上极线掩码再归一化，强制特征聚合严格沿极线进行。

Figure 2 对比了三种注意力机制在高噪声下的表现：时间注意力因仅关注同位置像素而无法应对大幅相机运动；3D 全注意力虽具有全局感受野，但噪声会掩盖确定性信息，导致跟踪失败；极线注意力则通过几何先验排除了大部分噪声的随机干扰，仅保留最相关的噪声条件，从而在噪声较大时仍能维持一致的跨帧关系。

### 3. 与 Baseline 的 Changed Slots 对比

CamI2V 以 **DynamiCrafter**（Xing et al., 2023）为基础 I2V 模型，并以 **CameraCtrl**（He et al., 2024a）为直接竞争基线，在以下关键模块上进行了替换：

| 变更槽位 | 基线方案 | CamI2V 方案 | 变更动机 |
|---------|---------|------------|---------|
| **跨帧注意力机制** | 分离的空间/时间注意力（间接 3D 注意力） | 在所有帧上施加极线约束的 Epipolar Attention | 3D 全注意力在高噪声下易被误导；极线约束提供了最优的噪声条件量（消融实验证实，Table 2） |
| **相机嵌入使用方式** | Plücker 坐标通过简单侧分支注入，无显式几何约束 | Plücker 嵌入与极线注意力深度耦合，利用其对极几何约束 | 单纯的 Plücker 注入缺乏显式几何引导；与极线注意力结合后，相机参数直接参与跨帧特征匹配的约束 |
| **零对极区域处理** | 无专门处理 | 引入 2 个可学习的 Register Tokens，作为极线消失时的占位符 | 处理帧间无重叠区域（如快速运动、遮挡），维持注意力计算的数值稳定性（Figure 6） |

此外，CamI2V 还引入了 **多尺度无分类器引导（Multiple CFG）** 模块，使用两个独立的引导尺度分别控制图像/文本条件和相机条件，并通过蒸馏技术将二者融合以加速推理。

### 4. 消融实验的关键证据

Table 2 的消融研究为上述创新提供了直接证据：

- **Plücker 嵌入 + 全帧极线注意力**的组合在所有变体中取得了最优的相机可控性（RotErr 0.4758, CamMC 1.7153, TransErr 1.4955）。
- **3D 全注意力**在噪声较大时性能显著劣于极线注意力，甚至不如仅在参考帧上施加极线约束的 CamCo 式设置，验证了“不加约束的全局交互反而有害”的核心论点。
- 仅使用 Plücker 嵌入而不施加极线约束（即 CameraCtrl 的基线设置）时，相机可控性大幅下降，说明**显式的几何约束是性能提升的关键因果旋钮**。

> **需人工验证**：分析材料中未提供 Register Tokens 数量的消融实验，其对性能的具体贡献大小需要查阅原文进一步确认。

CamI2V的整体管线建立在基础图像到视频扩散模型 **DynamiCrafter**（Xing et al., 2023）之上，通过两个关键模块的插入和一种条件注入策略的改进，将相机控制能力赋予原有模型。其核心设计思想是：将相机位姿转换为显式的三维几何约束，并利用该约束重塑跨帧特征的交互方式，使模型在高噪声条件下仍能保持几何一致性。

### 输入输出流

管线的输入包括三部分：一张参考图像、一段文本描述，以及一段相机轨迹。相机轨迹由一系列外参矩阵 $E_i$ 和内参矩阵 $K_i$ 定义，描述每帧的拍摄视角。输出为一段16帧、分辨率256×256的视频序列（训练时），其内容与输入图像保持语义一致，同时严格遵循给定的相机运动轨迹。

### 模块构成与数据流

**1. 位姿编码器与Plücker嵌入**

相机参数首先被转换为Plücker坐标，作为全局三维射线位置编码。对于每帧的每个像素 $(u,v)$，其对应的相机光线表示为：
$$r = \langle m, d \rangle \in \mathbb{R}^6$$
其中 $d$ 为光线方向向量，$m = p \times d$ 为力矩。这一表示将二维像素坐标与三维空间中的绝对射线一一对应，使模型能够隐式学习三维空间结构。随后，一个可学习的位姿编码器（架构与 **CameraCtrl** (He et al., 2024a) 类似）将Plücker嵌入投影为与U-Net特征兼容的表示，并通过线性投影注入扩散模型的各个层级，作为全局位置编码。

**2. 极线注意力模块**

这是CamI2V的核心创新，被插入在U-Net的空间注意力与时间注意力之间。对于任意两帧 $i$ 和 $j$，该模块利用基础矩阵 $F_{ij}$ 计算第 $i$ 帧上每个像素在第 $j$ 帧上的极线：
$$l_{ij}(u,v) = F_{ij} \cdot (u, v, 1)^{\mathrm{T}}$$
然后通过距离阈值 $\delta$ 构造离散极线掩码，只允许第 $j$ 帧上到极线距离小于 $\delta$ 的像素参与注意力计算：
$$D_{ij}(u',v') = \frac{(A,B,C) \cdot (u',v',1)}{\sqrt{A^2+B^2}}$$
最终的极线注意力计算公式为：
$$\mathrm{EpipolarAttn}(q,k,v,m) = \mathrm{softmax}\left(\frac{q k^{\mathrm{T}}}{\sqrt{d}} \odot m\right) v$$
其中 $m$ 为极线掩码，$\odot$ 表示逐元素乘法。这一机制将跨帧特征聚合严格限制在极线上，大幅缩小了匹配搜索空间，排除了大部分噪声的随机干扰。

**3. Register Tokens**

为处理帧间无重叠区域（如快速运动导致极线消失、或目标被遮挡），模块中引入2个可学习的register tokens。当某像素在目标帧的极线上找不到任何有效匹配像素时，注意力将自动转向这些register tokens，维持计算稳定性。

**4. 多尺度无分类器引导**

CamI2V采用双引导尺度设计：$s_{\mathrm{img\&txt}}$ 控制图像和文本条件的引导强度，$s_{\mathrm{camera}}$ 独立控制相机条件的引导强度。两者可分别调节，且可通过蒸馏合并为单一前向过程，避免三倍推理开销。

### 模块间关系

整个管线中，Plücker嵌入为极线注意力提供了几何计算的基础——基础矩阵 $F_{ij}$ 正是从相机参数导出。极线注意力模块位于空间注意力和时间注意力之间，先通过空间注意力处理单帧内特征，再通过极线注意力建立跨帧几何约束，最后通过时间注意力补充时序平滑。这一设计使得几何约束成为跨帧交互的主导机制，而非传统方法中时序注意力的简单替代。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_15957/figures/004_Figure_4.jpg]]
*Figure 4: Pipeline of camera-controlled image-to-video diffusion model. We follow CameraCtrl to add a learnable pose encoder and a linear projection to process plucker embeddings as a global positional embedding. Epipolar attention is added between spatial and temporal attention*

CamI2V 在基础 I2V 扩散模型（**DynamiCrafter**，Xing et al., 2023）之上，通过三个核心模块的协同设计，实现了对相机运动的精确控制。其关键创新在于将跨帧特征交互重新解释为一类“噪声条件”的利用问题，并通过极线约束最大化条件的信息价值。

### 3.1 Plücker 光线嵌入：从相机参数到全局 3D 位置编码

相机控制的第一个关键步骤是将每帧的相机参数转化为一种能够隐式编码 3D 空间位置的表示。CamI2V 沿用 **CameraCtrl**（He et al., 2024a）的做法，采用 Plücker 坐标作为全局位置嵌入。

给定像素坐标，从相机光心出发穿过该像素的光线 $r$ 可用 Plücker 坐标参数化：

$$r = \langle m, d \rangle \in \mathbb{R}^6$$

其中 $d$ 为光线方向向量，$m = p \times d$ 为力矩（光心位置 $p$ 与方向 $d$ 的叉积）。一帧图像的所有光线构成光线束 $\mathcal{R} = \{ r_1, \ldots, r_n \}$。

这些 6 维 Plücker 嵌入随后通过一个可学习的姿态编码器（Pose Encoder）和线性投影层，注入到基础模型的 U-Net 中，作为全局位置编码（见 Figure 4）。与简单的相机外参/内参直接注入不同，Plücker 坐标天然携带了 3D 光线在空间中的绝对位置信息，为后续的极线约束提供了几何基础。

### 3.2 极线注意力：噪声条件下的跨帧几何约束

这是 CamI2V 最核心的创新模块。其设计动机源于对扩散模型中“条件”本质的重新思考：在高噪声水平下，跨帧像素特征的确定性信息 $\alpha_t x_0$ 逐渐被噪声的随机性 $\sigma_t \epsilon$ 主导，此时无约束的全注意力机制容易被噪声误导，导致跨帧跟踪失败（见 Figure 2）。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_15957/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of existing attention mechanisms for tracking displaced noised features. Temporal attention is limited to features at the same location of picture, rendering it ineffective for significant camera movements. In contrast, 3D full attention facilitates cross-frame tracking due to its broad receptive field. However, high noise levels can obscure deterministic information, hindering consistent tracking. Our proposed epipolar attention aggregates features along the epipolar line, effectively modeling cross-frame relationships even under high noise conditions*

极线注意力通过引入显式的对极几何约束来解决这一问题，其核心操作分为三步：

**第一步：构建极线掩码。** 对于第 $i$ 帧上的像素 $(u, v)$，其在第 $j$ 帧上的极线由基础矩阵 $F_{ij}$ 导出：

$$l_{ij}(u,v) = F_{ij} \cdot (u, v, 1)^{\mathrm{T}}$$

其中 $F_{ij}$ 由两帧的相机内外参计算得到。对于第 $j$ 帧上的任意像素 $(u', v')$，其到该极线的距离为：

$$D_{ij}(u',v') = \frac{(A,B,C) \cdot (u',v',1)}{\sqrt{A^2+B^2}}$$

通过设定距离阈值 $\delta$，将连续的极线离散化为二值掩码：距离小于 $\delta$ 的像素被标记为 1（允许参与注意力），其余为 0（见 Figure 5）。该掩码在不同特征分辨率下自适应调整阈值，形成多分辨率极线掩码。

**第二步：极线约束的注意力计算。** 将离散极线掩码 $m$ 逐元素乘到注意力分数矩阵上，强制特征聚合仅沿极线进行：

$$\mathrm{EpipolarAttn}(q,k,v,m) = \mathrm{softmax}\left(\frac{q k^{\mathrm{T}}}{\sqrt{d}} \odot m\right) v$$

这一操作将跨帧匹配的搜索空间从整幅图像大幅缩小至极线邻域，有效排除了大部分噪声像素的干扰。

**第三步：Register Tokens 处理零对极区域。** 当相机运动剧烈或存在遮挡时，某些像素在其他帧上可能完全没有对应的极线区域。为此，CamI2V 在键/值序列中插入 2 个可学习的 register tokens，作为极线消失时的占位符，维持注意力计算的稳定性（见 Figure 6）。

### 3.3 多尺度无分类器引导

CamI2V 采用两个独立的无分类器引导（CFG）尺度：$s_{img\&txt}$ 控制图像和文本条件的引导强度，$s_{camera}$ 控制相机条件的引导强度。最终的去噪预测为：

$$\epsilon_{\theta}(z_t, c_{camera}, c_{img\&txt}, s_{camera}, s_{img\&txt})$$

这种解耦设计允许在推理时独立调节相机可控性与画面质量之间的平衡。论文指出，若需要加速推理，可将两个引导尺度蒸馏（Xing et al., 2023）到模型中，避免三次前向传播带来的额外耗时。

### 模块间协同关系

三个模块形成清晰的因果链路：Plücker 嵌入提供 3D 几何先验 → 极线注意力利用该先验将跨帧交互约束在几何一致的区域 → 多尺度 CFG 在推理时平衡几何精度与生成质量。消融实验（Table 2）证实，Plücker 嵌入与所有帧上的极线注意力组合取得了最优性能，而 3D 全注意力在高噪声下表现甚至不如仅参考帧的极线设置，验证了“约束优于全连接”的核心洞察。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_15957/figures/003_Figure_3.jpg]]
*Figure 3: Parameterizations for cameras. Left: Camera representation and trajectory visualization in the world coordinate system. Right: The transformation from camera representations to 3D ray representations as Plucker coordinates given pixel coordinates. ¨*

## 实验与关键发现

### 主实验结果

CamI2V 在 RealEstate10K 基准上以显著优势超越所有对比方法，实现了相机可控性与生成质量的双重领先。**Table 1** 报告了与 **DynamiCrafter** (Xing et al., 2023)、**CameraCtrl** (He et al., 2024a) 和 **MotionCtrl** (Wang et al., 2024d) 的定量对比。在相机位姿一致性指标上，CamI2V 相较于此前最优的 CameraCtrl 取得了系统性提升：旋转误差 RotErr 从 0.7064 降至 0.4758（相对降低 32.96%），相机运动一致性 CamMC 从 2.304 降至 1.7153（相对降低 25.64%），平移误差 TransErr 从 1.888 降至 1.4955（相对降低 20.77%）。这三项指标的一致改善表明，极线约束不仅提升了旋转估计精度，也有效约束了平移方向的几何一致性。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_15957/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison with state-of-the-art methods. * denotes the results we reproduced using DynamiCrafter as base I2V model. We achieve a 32.96%, 25.64%, 20.77% improvement over previous Sota CameraCtrl on RotErr, CamMC, TransErr on the RealEstate10K dataset without compromising dynamics, generation quality, and generalization on out-of-domain images. These results were obtained using Text and Image CFG set to 7.5, 25 steps, and camera CFG set to 1.0 (no camera cfg)*

在视频生成质量方面，CamI2V 的 FVD (StyleGAN) 为 55.701，略优于基础模型 DynamiCrafter 的 56.542，说明引入相机控制并未损害生成质量。所有方法均使用统一的 GLOMAP 重建管道与标准化指标计算，确保比较的公平性。

值得注意的是，这些结果是在相机 CFG 尺度设为 1.0（即未启用相机无分类器引导）的条件下获得的，表明极线注意力本身已能提供足够的几何约束，无需额外的引导增强。

### 消融研究

**Table 2** 的消融实验系统验证了 Plücker 嵌入与极线注意力两大核心设计的贡献。消融变体包括：使用 CameraCtrl 式的 Plücker 侧分支注入、仅在参考帧上施加极线约束（CamCo 类设置）、在所有帧上使用 3D 全注意力，以及本文提出的完整方案（Plücker 嵌入 + 所有帧上的极线注意力）。

关键发现如下：

- **Plücker 嵌入的贡献**：将 Plücker 坐标作为全局 3D 光线位置编码注入，相较于 CameraCtrl 的侧分支注入方式，在所有指标上均有提升。这验证了将相机参数显式转化为几何可解释的 3D 光线表示，有助于模型隐式学习空间结构。

- **极线注意力的帧范围选择**：在所有帧上施加极线注意力显著优于仅在参考帧上施加（CamCo 类设置）。这表明跨所有帧的极线约束能够更充分地利用多帧间的对极几何关系，而仅约束参考帧会丢失帧间的相互信息。

- **3D 全注意力的失效**：令人关注的是，3D 全注意力在噪声较大时性能不仅不如极线注意力，甚至劣于 CamCo 式的单帧极线设置。这一结果直接支持了本文的核心洞察——在高噪声条件下，无约束的全注意力会被噪声误导，导致跨帧特征匹配失准；极线约束通过将搜索空间压缩到对极线上，排除了大部分噪声的随机干扰，仅保留最相关的几何一致信息。

- **完整方案的最优性**：Plücker 嵌入与所有帧上极线注意力的组合在所有消融变体中取得最优，验证了两者的协同效应——Plücker 嵌入提供精确的 3D 光线定位，极线注意力则利用这些定位信息约束跨帧交互。

### 计算效率分析

**Table 3** 报告了各方法在 DeepSpeed ZeRO-1 下的 GPU 显存占用与推理速度对比。尽管引入了额外的极线注意力模块，CamI2V 的训练显存需求仅为 24 GB，可在消费级 GPU（如 RTX 3090/4090）上完成全参数微调。推理阶段，生成 16 帧 256×256 分辨率的视频仅需 12 GB 显存，与基础模型 DynamiCrafter 相比开销增加有限。这一效率得益于极线掩码的离散化设计——通过距离阈值 δ 将注意力限制在极线附近少量像素上，避免了全注意力的二次计算复杂度。

### 失败模式与局限性

尽管取得了显著的性能提升，CamI2V 仍存在以下已知局限：

1. **高分辨率生成挑战**：在 512×320 及以上分辨率下，生成质量可能出现下降。这主要源于高分辨率特征图上极线约束的离散化误差放大，以及显存限制对批处理大小和帧数的约束。

2. **复杂相机轨迹**：快速旋转或剧烈平移场景下，帧间重叠区域急剧缩小，极线上有效匹配像素稀疏，导致跨帧一致性下降。虽然 register tokens 部分缓解了零对极区域的问题，但在极端运动下仍显不足。

3. **长视频生成**：当前实验主要基于 16 帧序列，更长视频（如 32 帧以上）的生成质量与几何一致性需要进一步验证。长序列中误差累积效应可能被放大。

4. **开放域泛化**：模型在 RealEstate10K 上训练，该数据集以静态室内外场景为主。在动态场景（包含运动物体）、显著光照变化或开放域图像上的鲁棒性尚未充分评估，需要手动验证。

### 关键图表结论

- **Table 1**：CamI2V 在相机可控性三项指标上全面超越 CameraCtrl（相对提升 20.77%–32.96%），同时保持与基础模型相当的生成质量。
- **Table 2**：极线注意力在所有帧上的应用是性能提升的关键，3D 全注意力在高噪声下反而不如约束方案，直接验证了“噪声条件”理论。
- **Table 3**：方法在消费级 GPU 上可训练、可推理，计算开销可控，具备实用部署潜力。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_15957/figures/008_Table_2.jpg]]
*Table 2: Ablation study on model variants*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_15957/figures/011_Table_3.jpg]]
*Table 3: Comparison on GPU memory usage and speed under DeepSpeed ZeRO-1. * denotes our reproduction on DynamiCrafter. We report full parameter fine-tuning results of DynamiCrafter. Our model can be trained on 24GB consumer-level GPUs despite the additional epipolar attention*

## 定位与知识库关联

### 基线关系与继承

CamI2V 建立在 **DynamiCrafter** (Xing et al., 2023) 的图像到视频扩散基础框架之上，沿用了其时空分离注意力的 U-Net 架构，但在跨帧交互机制和相机条件注入方式上进行了根本性重构。其最直接的竞争对手是 **CameraCtrl** (He et al., 2024a)，后者同样使用 Plücker 坐标作为相机表示，但通过简单的侧分支将其注入模型，且未引入显式的几何约束来指导跨帧特征聚合。另一对比基线 **MotionCtrl** (Wang et al., 2024d) 则采用不同的相机控制策略。

CamI2V 从 CameraCtrl 继承的关键设计包括：
- 可学习的姿态编码器（pose encoder）和线性投影层，用于将 Plücker 嵌入处理为全局位置编码；
- 将相机条件作为侧输入注入基础 I2V 模型的思路。

在此基础上，CamI2V 做出了三个关键改变，构成了其方法创新的核心：

**改变槽位一：跨帧注意力机制。** 基线方法（DynamiCrafter 及 CameraCtrl）采用分离的空间注意力和时间注意力，其中时间注意力仅在相同像素位置进行跨帧交互。这种“间接 3D 注意力”在相机大幅运动时完全失效，因为对应像素已偏移到完全不同的位置。CamI2V 将其替换为在所有帧上施加极线约束的极线注意力（epipolar attention），使跨帧特征聚合严格沿对极几何线进行。

**改变槽位二：相机嵌入的使用方式。** CameraCtrl 将 Plücker 坐标通过侧分支注入后，缺乏显式的几何约束来利用这些坐标蕴含的 3D 信息。CamI2V 将 Plücker 嵌入与极线注意力深度绑定——Plücker 坐标用于推导帧间的基础矩阵 $F_{ij}$，进而生成极线掩码，使相机条件从“被动注入”变为“主动约束跨帧交互”。

**改变槽位三：零对极区域处理。** 当相机快速运动或帧间无重叠时，目标帧上可能不存在任何位于极线上的有效像素。基线方法对此无专门处理。CamI2V 引入可学习的 register tokens（设置为 2 个），作为极线消失时的占位符插入键/值序列，维持注意力计算的数值稳定性。

### 方法谱系中的定位

从更广的视角看，CamI2V 处于三个研究脉络的交汇点：

1. **图像到视频扩散模型**：以 DynamiCrafter 为代表，将文本条件扩展为图像+文本条件，通过时空注意力实现从单图到多帧的扩展。CamI2V 在此脉络中贡献了相机可控性维度。

2. **相机可控视频生成**：CameraCtrl 和 MotionCtrl 等先行工作证明了将相机参数注入扩散模型可实现显式的视角控制。CamI2V 的核心推进在于将几何先验（对极约束）从“软约束”提升为“硬约束”——不是让模型隐式学习跨帧对应，而是通过极线掩码直接限定注意力计算的有效区域。

3. **几何感知的深度学习**：Plücker 坐标作为光线表示在 NeRF 系列工作中已有广泛应用。CamI2V 将其引入视频扩散模型的跨帧注意力中，实现了 3D 几何先验与 2D 生成模型的深度融合。

### 适用边界与局限

基于论文提供的证据，CamI2V 的适用边界可归纳如下：

**已验证的有效范围：**
- 数据集：RealEstate10K（室内外房地产场景，相机运动相对平缓）
- 分辨率：256×256（训练与推理主要设置）
- 帧数：16 帧序列
- 相机运动：中等幅度的平移和旋转

**论文明确指出的局限：**
- 高分辨率生成（512×320 及以上）仍面临挑战，生成质量可能下降；
- 处理复杂相机轨迹（如快速旋转、剧烈平移）时，几何一致性可能出现退化——这与极线约束在帧间重叠不足时的固有弱点相关，register tokens 仅能部分缓解；
- 长视频（超过 16 帧）的生成质量需要进一步验证，累积误差可能随帧数增加而放大。

**需要手动验证的边界：**
- 动态场景（包含运动物体）下的鲁棒性——论文的评估集中在静态场景的相机可控性上，对动态物体与相机运动的交互尚未充分探索；
- 光照剧烈变化的场景——Plücker 嵌入仅编码几何信息，对光度变化无建模能力；
- 开放域图像（非 RealEstate10K 分布）的泛化性——论文展示了部分域外可视化结果（Figure 8），但缺乏系统的定量评估。

### 开放问题

论文遗留了若干值得追踪的研究方向：

1. **多尺度无关类引导蒸馏**：论文提到可将两个 CFG 尺度（$s_{\text{img\\&txt}}$ 和 $s_{\text{camera}}$）蒸馏到模型中以避免三次前向推理的额外耗时，但蒸馏对生成质量和速度的实际影响未量化。这是实际部署中的关键权衡。

2. **更优的相机条件注入方式**：当前设计沿用 CameraCtrl 的侧分支注入范式，将 Plücker 嵌入通过独立的姿态编码器处理后加入 U-Net。联合训练相机编码器与基础模型（而非固定基础模型仅训练新增模块）是否能进一步提升性能，仍是一个开放问题。

3. **极线约束的松弛策略**：当前的硬阈值离散化掩码（由距离阈值 $\delta$ 控制）可能过于刚性。自适应阈值或多尺度软约束是否能改善边界情况（如帧间重叠恰好处于阈值边缘），值得探索。

4. **计算效率与扩展性**：极线注意力需要为每对帧计算基础矩阵并生成掩码，在长序列或高分辨率下的计算开销尚未系统分析。register tokens 数量的最优选择（当前固定为 2）也缺乏消融研究。

## 原文 PDF

![[paperPDFs/arxiv_2024/CamI2V_Camera_Controlled_Image_to_Video_Diffusion_Model.pdf]]
