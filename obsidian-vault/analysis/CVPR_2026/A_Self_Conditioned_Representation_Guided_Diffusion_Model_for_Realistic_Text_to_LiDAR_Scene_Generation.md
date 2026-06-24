---
title: A Self-Conditioned Representation Guided Diffusion Model for Realistic Text-to-LiDAR Scene Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/A_Self_Conditioned_Representation_Guided_Diffusion_Model_for_Realistic_Text_to_LiDAR_Scene_Generation.pdf
project_link: null
code_link: null
aliases:
- SCRGDMRTLSG
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/representation_self_supervised_transfer
core_operator: 自条件表示引导（SCRG）通过引导网络（GN）在训练中提供多尺度几何重建正则化，使去噪网络（DN）从数据分布中学习精细结构；方向位置编码（DPE）解决球面投影带来的方向混淆，提升街道保真度。
primary_logic: 以端到端方式联合训练引导网络与去噪网络，GN仅早期参与梯度更新并在推理时解耦，在不增加推理成本的前提下，利用特征空间对齐（余弦相似度）为DN提供几何细节的软监督，从而在稀缺数据下生成具有丰富结构的LiDAR场景。
claims:
- 在KITTI-360无条件生成中，T2LDM的FSVD为21.12，显著优于次优方法Text2LiDAR的51.55（降幅约59%），其他指标也全面领先。
- 移除SCRG和DPE后（T2LDM∅），文本引导生成FSVD从66.93大幅上升至91.15，TBK从23.44%降至15.45%，证实两个组件对质量和可控性的关键作用。
- 端到端训练模式比预训练模式取得更好结果（FSVD 64.21 vs 67.35），表明联合优化GN与DN的特征对齐更有效。
- KITTI-360 (64-beam, unconditional) 上 FSVD↓ = 21.12
---

# A Self-Conditioned Representation Guided Diffusion Model for Realistic Text-to-LiDAR Scene Generation

> [!tip] 核心洞察
> 以端到端方式联合训练引导网络与去噪网络，GN仅早期参与梯度更新并在推理时解耦，在不增加推理成本的前提下，利用特征空间对齐（余弦相似度）为DN提供几何细节的软监督，从而在稀缺数据下生成具有丰富结构的LiDAR场景。

| 字段 | 内容 |
|------|------|
| 中文题名 | 自条件表示引导的文本到LiDAR场景扩散生成模型 |
| 英文题名 | A Self-Conditioned Representation Guided Diffusion Model for Realistic Text-to-LiDAR Scene Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.19004) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/representation_self_supervised_transfer |
| Method | T2LDM |
| Dataset | KITTI-360, nuScenes |

> [!tip] 效果简介
> - KITTI-360 (64-beam, unconditional) 上，FSVD↓ 21.12 vs 51.55 (Text2LiDAR) (-30.43)。
> - nuScenes (32-beam, unconditional) 上，FSVD↓ 64.21 vs 85.98 (Text2LiDAR) (-21.77)。
> - nuScenes (text-guided, 'weather, location') 上，TBR (%)↑ 23.44 vs 17.15 (Text2LiDAR) (+6.29)。

## 概述

文本到LiDAR场景生成面临一个核心瓶颈：**文本-LiDAR配对数据极度稀缺**，导致生成模型缺乏足够的训练先验，常产生过于平滑、缺乏细节目标的场景；同时低质量的文本描述进一步削弱了生成的可控性。针对这一问题，本文提出**T2LDM**（Text-to-LiDAR Diffusion Model），通过**自条件表示引导（SCRG）**和**方向位置编码（DPE）**两个关键设计，在稀缺数据条件下实现具有丰富几何结构的LiDAR场景生成。

**核心机制**：SCRG引入一个与去噪网络（DN）结构相同的引导网络（GN），在训练中从数据分布学习几何重建细节，并与DN的多层噪声特征进行余弦相似度对齐，为DN提供适应性的几何正则化监督。GN仅在训练早期参与梯度更新，推理时完全解耦，因此不增加推理成本。DPE则针对范围图球面投影带来的0°/360°边界方向混淆问题，通过傅立叶级数编码像素的水平/垂直角度信息，为模型注入真实的方向先验，显著提升街道等结构的保真度。

**方法定位**：T2LDM属于条件扩散生成模型，在文本引导下将LiDAR场景表示为范围图（Range Map）进行去噪生成。相比现有的无条件LiDAR生成方法（如**LiDARGen**（Zyrianov et al., ECCV 2022）、**LiDM**（Ran et al., CVPR 2024）、**R2DM**（Nakashima and Kurazume, ICRA 2024））和文本引导方法**Text2LiDAR**（Wu et al., ECCV 2024），T2LDM的独特之处在于以端到端方式联合训练引导网络与去噪网络，利用特征空间对齐实现软监督，而非依赖外部预训练先验。

**主要结果**：在KITTI-360无条件生成基准上，T2LDM的FSVD达到21.12，显著优于次优方法Text2LiDAR的51.55（降幅约59%）；在nuScenes文本引导生成中，文本匹配率TBR从17.15%提升至23.44%。消融实验证实，移除SCRG和DPE后FSVD从66.93恶化至91.15，TBR从23.44%降至15.45%，验证了两个组件的关键作用。此外，T2LDM在稀疏到密集上采样任务上也展现出优于专用方法**PUDM**（Qu et al., CVPR 2024）的性能。

## 背景与动机

### 文本到LiDAR生成的现实需求

自动驾驶系统对高质量3D场景数据的需求日益增长。LiDAR传感器能够提供精确的几何信息，是感知、定位和规划等下游任务的核心输入。然而，真实世界中采集和标注LiDAR数据成本极高——不仅需要昂贵的传感器设备和专业采集车辆，还需要大量人工进行3D边界框标注。这一瓶颈催生了LiDAR场景生成的研究方向：若能根据自然语言描述自动生成逼真的LiDAR点云场景，将极大降低数据获取成本，并为仿真、数据增强和闭环训练提供无限可能。

文本到LiDAR生成（Text-to-LiDAR Generation）正是这一方向的前沿探索。其目标是给定一段自然语言描述（如“雨天，城市街道，前方有三辆车”），生成与描述语义一致且几何逼真的LiDAR场景。相比于图像生成领域已较为成熟的文本到图像扩散模型，文本到LiDAR生成面临独特且严峻的挑战。

### 核心瓶颈：稀缺数据与低质量先验

文本-LiDAR生成的根本困难在于**训练先验的极度匮乏**。具体表现为两个相互交织的层面：

**数据稀缺层面**。文本-图像生成模型（如Stable Diffusion）得益于数十亿图文对的预训练，而文本-LiDAR配对数据几乎不存在。现有LiDAR数据集（如nuScenes的34,149帧、KITTI-360的76,165帧）不仅规模远小于图像数据集，其原始标注中也不包含自然语言描述。研究者需要借助3D边界框等先验信息人工构造文本提示，这进一步限制了文本描述的多样性和自然度。

**先验质量层面**。标准条件扩散模型仅依赖去噪损失 $L(\theta) = \mathbb{E}_{\epsilon \sim \mathcal{N}(0, I)} || v - v_{\theta}(x_t, t, c) ||^2$ 进行训练。在数据充足时，该目标足以驱动模型学习数据分布；但在文本-LiDAR稀缺场景下，模型缺乏足够的监督信号来学习精细的几何结构。其直接后果是：现有方法生成的LiDAR场景往往**过于平滑，缺乏细节目标**，难以满足下游任务对场景保真度的要求。

### 现有方法的缺口

当前LiDAR场景生成方法可大致分为两类，但均未有效解决上述瓶颈：

**无条件生成方法**——包括基于VAE的**LiDARVAE**（Caccia et al., IROS 2019）、基于GAN的**LiDARGAN**（Caccia et al., IROS 2019）和**ProjectedGAN**（Sauer et al., NeurIPS 2021）、以及基于扩散模型的**LiDARGen**（Zyrianov et al., ECCV 2022）、**LiDM**（Ran et al., CVPR 2024）和**R2DM**（Nakashima and Kurazume, ICRA 2024）——虽能生成具有一定几何结构的场景，但完全缺乏对生成内容的语义控制能力，无法根据文本描述定向生成特定场景。

**文本条件生成方法**——以**Text2LiDAR**（Wu et al., ECCV 2024）为代表——首次尝试将文本语义注入LiDAR生成过程，但受限于稀缺的训练数据，其生成质量仍不理想。在KITTI-360数据集上，Text2LiDAR的FSVD（Fréchet Scene Velocity Distance）为51.55，与理想水平存在显著差距。定性结果也表明，其生成场景中物体细节缺失严重，尤其在多物体复杂场景下表现不佳。

此外，现有方法普遍将LiDAR的范围图（Range Map）视为普通2D图像进行卷积操作，**忽略了球面投影的循环几何特性**。在范围图中，0°和360°方位角对应的像素在物理空间中是相邻的，但在图像空间中却位于左右边界两端。这种方向混淆导致模型生成的道路出现弯曲或断裂，严重损害场景的几何一致性。

### 本文动机与核心思路

针对上述缺口，本文的核心动机是：**在文本-LiDAR配对数据极度稀缺的条件下，如何为扩散模型提供额外的几何正则化，使其能够生成具有丰富细节和语义一致性的LiDAR场景？**

本文提出的T2LDM（Text-to-LiDAR Diffusion Model）通过两个关键创新回答这一问题：

1. **自条件表示引导（Self-Conditioned Representation Guidance, SCRG）**：引入一个与去噪网络（DN）结构相同的引导网络（GN），在训练过程中接收DN的多层噪声特征，并以数据分布中的真实几何表示为监督目标进行重建。通过将GN的重建特征与DN的噪声特征在特征空间中对齐（余弦相似度），SCRG为DN提供了适应性的几何细节正则化。关键设计在于：GN仅在训练早期参与梯度更新，推理时完全解耦，从而在不增加推理成本的前提下，利用数据分布中的结构先验弥补文本-LiDAR数据稀缺的不足。

2. **方向位置编码（Directional Position Encoding, DPE）**：根据范围图中每个像素在LiDAR球面坐标系中的水平和垂直角度，通过多阶傅立叶展开编码方向信息，并以可学习门控机制注入网络特征。DPE使模型能够正确感知物体的相对方位关系，从根本上解决范围图边界的方向混淆问题，从而生成几何连贯的道路和物体布局。

通过端到端联合训练DN和GN，T2LDM在KITTI-360和nuScenes两个基准上均显著超越现有方法，并在文本引导生成、稀疏到密集上采样等任务中展现出优异的泛化能力。

## 核心创新

T2LDM 针对文本到LiDAR场景生成中“配对数据稀缺导致几何细节缺失”这一瓶颈，提出了两个相互协同的关键创新：**自条件表示引导（SCRG）** 和 **方向位置编码（DPE）**。前者在不增加推理成本的前提下为去噪网络注入几何重建正则化，后者解决了范围图（Range Map）中球面投影固有的方向混淆问题。

### 自条件表示引导（SCRG）

**动机**：标准条件DDPM仅依赖速度预测损失 $L(\theta) = \mathbb{E}_{\epsilon \sim \mathcal{N}(0, I)} || v - v_{\theta}(x_t, t, c) ||^2$ 进行训练。当文本-LiDAR配对数据有限时，该损失提供的监督信号不足以让模型学习到精细的物体几何结构，生成结果往往过于平滑。

**机制**：SCRG引入一个与去噪网络（DN）结构相同的引导网络（GN，记作 $x_\phi$），在训练过程中接收DN的多层噪声特征 $F_{noise}^{v_\theta}$，并输出重建特征 $F_{recon}^{x_\phi}$。其核心由两个损失驱动：

- **重建损失**：$L(\phi) = || x_0 - x_\phi(x_0, F_{noise}^{v_\theta}) ||^2$，迫使GN从噪声特征中恢复原始坐标的几何细节。
- **对齐损失**：$L_{SCRG} = l_{recon}(F_{recon}^{x_\phi} - F_{noise}^{v_\theta})$，通过余弦相似度将GN的重建特征与DN的噪声特征在多层尺度上对齐，为DN提供适应性的几何正则化信号。

**关键设计**：GN仅在训练的前100K步参与反向传播，之后冻结；推理时完全解耦。这意味着SCRG以“软监督”的方式在训练早期帮助DN建立高频语义感知能力，而不增加任何推理开销。消融实验证实了这一设计的有效性：在KITTI-360 30k迭代时，含SCRG的T2LDM FSVD为47.29，远优于无SCRG的217.18（Table 8），表明SCRG显著加速了早期几何结构的学习。端到端联合训练模式（FSVD 64.21）优于预训练GN后再训练DN的模式（FSVD 67.35），证明特征空间的对齐需要两者协同优化（Table 9）。

### 方向位置编码（DPE）

**动机**：LiDAR点云通过球面投影转换为范围图时，水平方向在0°/360°边界处产生循环截断。现有方法将范围图视为普通2D图像进行卷积，忽略了这一循环特性，导致街道等细长结构在边界处出现弯曲或断裂（Figure 2c）。

**机制**：DPE首先为范围图中每个像素计算其真实的水平角 $\theta$ 和垂直角 $\phi$：

$$\theta = 2\pi - (2\pi - 0) * (w + 0.5) / W, \quad \phi = f_{up} - (f_{up} - f_{down}) * (h + 0.5) / H$$

然后通过K阶傅立叶展开将角度编码为多尺度方向先验：

$$\mathrm{DPE}(\theta, \phi) = Fourier^K(\theta, \phi)$$

最终通过可学习门控参数 $\alpha$ 自适应注入主干特征：

$$x' = x + \alpha * \mathrm{DPE}(\theta, \phi)$$

**效果**：DPE使模型能够正确感知范围图中物体的相对方位关系（如Figure 2b所示，car_A与car_B的真实相对位置得以保留），从而生成几何连贯的街道场景。

### 组件协同与消融验证

SCRG与DPE并非孤立工作，而是形成互补：SCRG提供几何细节的正则化，DPE提供空间方向的结构先验。在nuScenes文本引导生成任务中，同时移除两者后FSVD从66.93恶化至91.15，文本-光束召回率（TBK）从23.44%降至15.45%；仅保留DPE或仅保留SCRG均有一定改善，但两者联合效果最优（Table 7）。这表明两个组件分别在“细节感知”和“方向感知”维度上贡献了不可替代的先验信息。

**总训练目标**为三者的加权联合优化：

$$L_{total} = L(\theta) + L(\phi) + \lambda L_{SCRG}$$

其中 $L(\theta)$ 为去噪损失，$L(\phi)$ 为GN重建损失，$L_{SCRG}$ 为对齐正则化项。

## 整体框架

T2LDM 的整体架构围绕“文本条件扩散 + 自条件表示引导”两条主线构建，通过四个核心模块的协同工作，在稀缺数据下实现具有丰富几何细节的 LiDAR 场景生成。图3展示了完整的数据流与模块关系。

### 数据预处理与表示

原始 LiDAR 点云首先通过球面投影转换为二维范围图（Range Map, RM），投影公式为：

$$u = \frac{1}{2} [1 - \arctan(y, x) \pi^{-1}] W, \quad v = [1 - (\arcsin(z r^{-1}) + f_{up}) f^{-1}] H$$

其中 $(x,y,z)$ 为3D点坐标，$r$ 为深度距离，$(u,v)$ 为范围图像素坐标。这一表示将整个 LiDAR 场景压缩为规则网格，使标准卷积架构能够直接处理。实验中使用 nuScenes（32线，$32\times1024\times2$）和 KITTI-360（64线，$64\times1024\times2$）两种规格的范围图。

### 核心模块与数据流

**1. 文本编码器（Text Encoder, TE）**  
采用冻结的 CLIP 模型将文本提示编码为 768 维语义特征向量，作为条件信号输入去噪网络。TE 在训练和推理阶段均保持冻结，不参与梯度更新。

**2. 去噪网络（Denoising Network, DN）**  
DN 基于 U-Net 架构，包含编码器、中间阶段和解码器，核心组件为 ResBlock、AttentionBlock、DownsamplingBlock 和 UpsamplingBlock。在每个去噪步骤中，DN 接收三个输入：
- 当前噪声范围图 $x_t$
- 时间步 $t$ 的嵌入
- TE 生成的文本特征 $c$

文本特征通过交叉注意力块与 DN 的多层噪声特征融合，实现语义条件控制。DN 的训练目标是预测添加的噪声速度 $v$，损失函数为：

$$L(\theta) = \mathbb{E}_{\epsilon \sim \mathcal{N}(0, I)} \| v - v_{\theta}(x_t, t, c) \|^2$$

**3. 方向位置编码（Directional Position Encoding, DPE）**  
DPE 直接嵌入 DN 的主干特征中，为范围图的每个像素注入真实方向先验。具体而言，DPE 计算每个像素中心的水平角 $\theta$ 和垂直角 $\phi$：

$$\theta = 2\pi - (2\pi - 0) \cdot (w + 0.5) / W, \quad \phi = f_{up} - (f_{up} - f_{down}) \cdot (h + 0.5) / H$$

然后通过 $K$ 阶傅立叶展开编码多尺度方向信息，并以可学习门控参数 $\alpha$ 自适应注入：

$$\text{DPE}(\theta, \phi) = \text{Fourier}^K(\theta, \phi), \quad x' = x + \alpha \cdot \text{DPE}(\theta, \phi)$$

这解决了标准卷积将范围图视为普通2D图像而忽略球面几何循环边界的问题，有效消除了生成街道的弯曲和断裂现象。

**4. 引导网络（Guidance Network, GN）**  
GN 的架构与 DN 完全相同，但功能定位不同。GN 接收两个输入：原始干净坐标 $x_0$ 和 DN 各层输出的噪声特征 $F_{noise}^{v_\theta}$。GN 的任务是从数据分布中学习几何重建细节，其重建损失为：

$$L(\phi) = \| x_0 - x_\phi(x_0, F_{noise}^{v_\theta}) \|^2$$

GN 输出的重建特征 $F_{recon}^{x_\phi}$ 与 DN 的噪声特征 $F_{noise}^{v_\theta}$ 通过余弦相似度进行对齐，形成 SCRG 正则化损失：

$$L_{SCRG} = l_{recon}(F_{recon}^{x_\phi} - F_{noise}^{v_\theta})$$

### 训练与推理机制

总训练损失为三项联合优化：

$$L_{total} = L(\theta) + L(\phi) + \lambda L_{SCRG}$$

关键设计在于：GN 仅在训练的前 100K 步参与反向传播，之后冻结。推理阶段 GN 完全解耦，不增加任何计算开销。这种“端到端联合训练、推理时解耦”的策略使 DN 能够从 GN 的几何重建能力中获益，同时保持轻量推理。

消融实验证实了这一设计的有效性：端到端训练模式（FSVD 64.21）优于预训练模式（FSVD 67.35），表明联合优化 GN 与 DN 的特征对齐比分离训练更有效。同时移除 SCRG 和 DPE 后，文本引导生成的 FSVD 从 66.93 恶化至 91.15，TBK 从 23.44% 降至 15.45%，验证了两个组件的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l2434_https_arxiv_org_abs_2511_19004/figures/004_Figure_3.jpg]]
*Figure 3: The overall framework of T2LDM. The Text Encoder (TE) encodes text prompts to generate semantically reliable features. Meanwhile, the Denoising Network (DN) models the denoising process under text guidance, DPE, and timestep. Furthermore, the Guidance Network (GN) introduces regularization with reconstruction details for DN while detached during inference*

![[assets/figures/papers/paper_list_l2434_https_arxiv_org_abs_2511_19004/figures/026_Figure_1.jpg]]
*Figure 1: The overall framework of T2LDM. DN and GN are composed of an Encoder, a Middle Stage, and a Decoder. The core modules of T2LDM include: ResBlock (RB), AttentionBlock (AB), DownsamplingBlock (DB), and UpsamplingBlock (UB). To effectively process the spherical projection of LiDAR data, T2LDM incorporates Circular Convolution [42] to adapt to the unfolded Range Map*

## 核心模块与公式推导

T2LDM 的核心架构由四个模块构成：文本编码器（TE）、去噪网络（DN）、引导网络（GN）和方向位置编码（DPE）。其设计围绕一个关键瓶颈展开——文本-LiDAR 配对数据极度稀缺，导致生成模型先验不足，常产生过于平滑、缺乏细节目标的场景。以下逐一阐述各模块的机制与关键公式。

### 球面投影与范围图表示

LiDAR 点云首先通过球面投影转换为二维范围图（Range Map, RM），这是所有后续操作的基础表示。对于 3D 点 $(x, y, z)$，其在范围图上的坐标 $(u, v)$ 定义为：

$$u = \frac{1}{2} [1 - \arctan(y, x) \pi^{-1}] W, \quad v = [1 - (\arcsin(z r^{-1}) + f_{up}) f^{-1}] H$$

其中 $r = \sqrt{x^2 + y^2 + z^2}$ 为深度距离，$W$ 和 $H$ 分别为范围图的宽和高，$f_{up}$ 和 $f_{down}$ 为 LiDAR 的垂直视场角上下界，$f = f_{up} - f_{down}$。该投影将稀疏的 3D 点云压缩为密集的 2D 表示，使扩散模型能够以标准卷积架构处理 LiDAR 场景。

### 自条件表示引导（SCRG）

SCRG 是 T2LDM 解决数据稀缺问题的核心机制。其因果逻辑在于：引导网络（GN）从数据分布中学习几何重建细节，并通过与去噪网络（DN）的多层噪声特征对齐，为 DN 提供适应性的几何正则化监督，从而在稀缺数据下仍能生成具有丰富结构的场景。

**引导网络重建损失**：GN（记为 $x_\phi$）接收原始坐标 $x_0$ 和 DN 的多层噪声特征 $F_{noise}^{v_\theta}$，学习重建几何细节：

$$L(\phi) = || x_0 - x_\phi(x_0, F_{noise}^{v_\theta}) ||^2$$

**SCRG 对齐损失**：GN 的重建特征 $F_{recon}^{x_\phi}$ 与 DN 的噪声特征 $F_{noise}^{v_\theta}$ 通过余弦相似度进行对齐，实现特征空间的正则化：

$$L_{SCRG} = l_{recon}(F_{recon}^{x_\phi} - F_{noise}^{v_\theta})$$

消融实验证实，余弦相似度优于 L1 和 MSE 损失，因为它关注方向一致性而非数值尺度（见 Supplementary Table 1）。

**关键设计**：GN 仅在训练的前 100K 步参与反向传播，之后冻结；推理时 GN 完全解耦，不增加推理成本。这种“训练时辅助、推理时剥离”的策略，使 T2LDM 在不牺牲推理效率的前提下，获得了数据分布中几何细节的学习能力。

### 方向位置编码（DPE）

范围图本质上是球面投影的结果，其水平方向具有循环特性（0° 与 360° 对应同一方向）。现有方法将范围图视为普通 2D 图像进行卷积，忽略了这一几何先验，导致 0°/360° 边界处出现方向混淆，生成弯曲或断裂的街道（见 Figure 2）。

![[assets/figures/papers/paper_list_l2434_https_arxiv_org_abs_2511_19004/figures/003_Figure_2.jpg]]
*Figure 2: (a) In LiDAR space*

DPE 通过为每个像素注入真实的方向先验来解决此问题。首先计算范围图中每个像素中心的水平角 $\theta$ 和垂直角 $\phi$：

$$\theta = 2\pi - (2\pi - 0) * (w + 0.5) / W, \quad \phi = f_{up} - (f_{up} - f_{down}) * (h + 0.5) / H$$

然后通过 $K$ 阶傅立叶展开编码角度，并通过可学习门控参数 $\alpha$ 自适应地注入主干特征：

$$\mathrm{DPE}(\theta, \phi) = Fourier^K(\theta, \phi), \quad x' = x + \alpha * \mathrm{DPE}(\theta, \phi)$$

多尺度傅立叶展开提供了从低频到高频的方向先验，可学习门控则允许网络根据层深和任务需求自适应调整方向信息的权重。

### 文本编码器与去噪网络

文本编码器（TE）使用冻结的 CLIP 模型将文本提示编码为 768 维语义特征，作为条件引导信号。去噪网络（DN）基于 U-Net 架构，包含交叉注意力块和残差块，接收文本特征、时间步和 DPE 编码后的范围图特征，执行条件去噪过程。交叉注意力机制将文本语义与噪声特征融合，其核心操作为：

$$O = mlp(W V) + F_{noise}^{v_{\theta}}, \quad F = ffn(O) + O$$

其中 $W$ 为注意力权重矩阵，$V$ 为值投影，$F_{noise}^{v_{\theta}}$ 为残差连接的噪声特征。

### 总训练损失

T2LDM 采用端到端联合优化，总损失为去噪损失、引导网络重建损失和 SCRG 对齐损失的加权和：

$$L_{total} = L(\theta) + L(\phi) + \lambda L_{SCRG}$$

其中 $L(\theta) = \mathbb{E}_{\epsilon \sim \mathcal{N}(0, I)} || v - v_{\theta}(x_t, t, c) ||^2$ 为标准的速度预测去噪损失。消融实验（Table 9）表明，端到端训练模式（FSVD 64.21）优于预训练模式（FSVD 67.35），验证了联合优化 GN 与 DN 特征对齐的有效性。

## 实验与分析

### 核心瓶颈与实验设计逻辑

文本到LiDAR场景生成面临两个根本性挑战：**配对数据稀缺**导致生成模型训练先验不足，常产生过于平滑、缺乏细节目标的场景；**低质量文本描述**进一步降低生成可控性。T2LDM通过自条件表示引导（SCRG）和方向位置编码（DPE）两个核心机制应对这些瓶颈——SCRG利用引导网络（GN）在训练中提供多尺度几何重建正则化，使去噪网络（DN）从数据分布中学习精细结构；DPE解决球面投影带来的0°/360°边界方向混淆，提升街道等场景元素的保真度。

实验在两个主流LiDAR数据集上展开：**nuScenes**（32线束，34,149个训练样本）和**KITTI-360**（64线束，76,165个样本）。LiDAR数据通过球面投影转换为范围图（Range Map），nuScenes对应 $R^{32 \times 1024 \times 2}$，KITTI-360对应 $R^{64 \times 1024 \times 2}$。评估涵盖无条件生成、文本引导生成、稀疏到密集上采样和语义到LiDAR生成四个任务维度。

### 无条件生成：KITTI-360与nuScenes主结果

**KITTI-360数据集**（Table 2）上，T2LDM在所有指标上显著超越现有方法。核心指标FSVD（Fréchet Scene Velocity Distance）降至 **21.12**，相比次优方法Text2LiDAR的51.55降幅约59%，相比LiDM（Ran et al., CVPR 2024）的62.59降幅约66%。这一差距在稀疏场景的**nuScenes数据集**（Table 3）上同样显著：T2LDM取得FSVD **64.21**，优于Text2LiDAR的85.98（降幅约25%）和R2DM（Nakashima and Kurazume, ICRA 2024）的81.43。

定性可视化（Figure 4, Figure 5）揭示了性能差距的结构性原因：现有方法仅在少目标场景中能生成一定的几何细节，但在复杂多目标场景中表现急剧恶化——LiDARVAE（Caccia et al., IROS 2019）和LiDARGAN（Caccia et al., IROS 2019）产生的场景物体边界模糊、形状失真；Text2LiDAR虽有所改善，仍缺乏精细结构。相比之下，T2LDM即使在多目标复杂场景中也能生成具有清晰几何边界的物体，且对同一场景可产生多样化变体（Figure 1c）。

![[assets/figures/papers/paper_list_l2434_https_arxiv_org_abs_2511_19004/figures/005_Figure_4.jpg]]
*Figure 4: The generated visualization results on KITTI-360. Due to insufficient training priors, existing methods can only generate highquality scenes with a few objects (top row). In contrast, T2LDM produces fine-grained geometric details even in complex multi-object scenes (bottom row). This is crucial for models to recognize 3D scenes in downstream tasks. For more visualizations, please refer to SM*

![[assets/figures/papers/paper_list_l2434_https_arxiv_org_abs_2511_19004/figures/008_Figure_5.jpg]]
*Figure 5: The generated visualization results on nuScenes. Similar to KITTI-360, existing methods can generate certain geometric details in scenes with few objects (top row) but struggle to handle complex multi-object scenes (bottom row), duo to the sufficient training data. This becomes more pronounced in the sparse scenes of nuScenes. In comparison, T2LDM can generate detailed objects even in multiobject scenes. Fig. 1 also shows that T2LDM can generate diverse structures for the same scene. More visualizations are provided in SM*

### 文本引导生成：可控性验证

文本引导生成实验（Table 4）直接检验模型对语义条件的响应能力。在nuScenes上，T2LDM取得文本对齐率 **TBR 23.44%**，显著优于Text2LiDAR的17.15%（提升6.29个百分点），同时FSVD从85.98降至66.93。Figure 8的定性对比进一步印证：现有方法生成结果过于平滑，难以满足文本语义要求；T2LDM则展现出与文本提示高度一致的细节生成能力。

![[assets/figures/papers/paper_list_l2434_https_arxiv_org_abs_2511_19004/figures/010_Table_4.jpg]]
*Table 4: The text-guided results on nuScenes. T2LDM exhibits outstanding performance in generation quality and controllability*

值得注意的是，论文在Table 1中系统分析了不同文本形式对生成质量的影响：场景级文本描述显著优于对象级文本提示，而显式位置提示表现最差。这一发现为文本条件设计提供了实用指导。

### 稀疏到密集上采样：任务泛化性

T2LDM的表示学习能力在稀疏到密集上采样任务中得到进一步验证（Table 5）。在nuScenes的4倍上采样设置下，T2LDM取得Chamfer Distance **$0.104 \times 10^{-5}$**，显著优于PUDM（Qu et al., CVPR 2024）的$0.198 \times 10^{-5}$和Grad-PU（He et al., CVPR 2023）的$0.147 \times 10^{-5}$。8倍上采样的优势趋势一致，表明SCRG学到的几何先验具有良好的跨任务迁移能力。

![[assets/figures/papers/paper_list_l2434_https_arxiv_org_abs_2511_19004/figures/011_Table_5.jpg]]
*Table 5: The results of the 4× rate and the 8× rate on nuScenes. T2LDM exhibits significantly upsampling results*

### 消融研究：SCRG与DPE的因果贡献

消融实验（Table 7）是验证核心机制因果作用的关键证据。以文本引导生成为测试场景：

![[assets/figures/papers/paper_list_l2434_https_arxiv_org_abs_2511_19004/figures/016_Table_7.jpg]]
*Table 7: Ablation study of component effectiveness for textguided generation on nuScenes. T2LDM∅, T2LDMD, and T2LDMS denote removing DPE and SCRG, keeping only DPE, and keeping only SCRG, respectively. DPE and SCRG can provide effective priors and regularization, enhancing scene fidelity*

- **T2LDM∅**（同时移除SCRG和DPE）：FSVD从66.93急剧恶化至91.15，TBR从23.44%降至15.45%，证实两个组件对生成质量和可控性的决定性作用。
- **T2LDM_D**（仅保留DPE）：FSVD恢复至74.24，TBR回升至19.02%，表明方向先验独立有效。
- **T2LDM_S**（仅保留SCRG）：FSVD为73.10，TBR为20.11%，表明几何正则化同样独立有效。
- **完整T2LDM**：两者联合取得最佳结果，验证了DPE和SCRG的互补性——DPE提供空间方向先验，SCRG提供几何细节正则化。

训练早期收敛速度的消融（Table 8）进一步揭示SCRG的加速效应：在KITTI-360仅30k迭代时，含SCRG的T2LDM FSVD为47.29，远优于无SCRG变体的217.18。这表明SCRG使模型在训练早期即能学习高频语义信息，对数据稀缺场景尤为关键。

![[assets/figures/papers/paper_list_l2434_https_arxiv_org_abs_2511_19004/figures/018_Table_8.jpg]]
*Table 8: The results on KITTI-360 at 30k iterations. SCRG enables T2LDM to learn high-frequency semantics early*

### 训练策略与损失函数选择

端到端训练与预训练模式的对比（Table 9）验证了联合优化的必要性：端到端模式在nuScenes上取得FSVD 64.21，优于预训练模式的67.35。这一结果支持了核心设计选择——GN与DN的特征空间对齐在联合训练中更为有效，预训练GN再固定无法充分适应DN的噪声特征分布。

![[assets/figures/papers/paper_list_l2434_https_arxiv_org_abs_2511_19004/figures/017_Table_9.jpg]]
*Table 9: Ablation study of end-to-end vs. pretrained training for SCRG on nuScenes. The end-to-end mode yields better results*

在SCRG重构损失的具体形式上，余弦相似度优于L1和MSE（Table 1 in SM），原因在于余弦相似度关注特征方向一致性而非数值尺度，更适合对齐不同网络层的表示空间。

### 已知局限与失败模式

尽管T2LDM在多个基准上取得领先结果，论文明确指出以下局限：

1. **文本标注泛化性受限**：当前依赖3D框先验生成场景描述，但许多LiDAR数据集缺乏3D框标注，限制了方法的适用范围。
2. **单条件控制**：目前仅支持单一文本条件，无法同时结合语义图、边界框等多种条件进行可控生成。
3. **训练资源消耗大**：SCRG引入与DN相同架构的GN，训练时参数翻倍。虽推理时GN解耦不增加推理成本，但训练阶段的计算和显存需求显著增加。

这些局限指向明确的研究方向：开发不依赖3D框标注的替代先验、设计多条件融合机制、以及探索GN的轻量化或剪枝策略以降低训练开销。

### 补充图表

![[assets/figures/papers/paper_list_l2434_https_arxiv_org_abs_2511_19004/figures/007_Table_2.jpg]]
*Table 2: The results on KITTI-360. T2LDM significantly outperforms existing methods on all metrics*

![[assets/figures/papers/paper_list_l2434_https_arxiv_org_abs_2511_19004/figures/006_Table_3.jpg]]
*Table 3: The results on nuScenes. T2LDM achieves superior generation results across all metrics in sparse scenes*

## 方法谱系与知识库定位

### 1. 问题域定位：文本到LiDAR生成的稀缺数据困境

T2LDM 切入的核心瓶颈是**文本-LiDAR配对数据的极度稀缺**。与图像生成领域拥有数十亿图文对（如LAION-5B）不同，LiDAR场景的文本描述依赖于3D框标注作为先验来生成，而大量LiDAR数据集缺乏此类标注。这一数据约束导致现有生成模型训练先验不足，常产生过于平滑、缺乏细节目标的场景，同时低质量文本描述进一步降低了生成的可控性。

该问题将T2LDM置于一个交叉地带：它既需要解决**无条件LiDAR生成**的几何保真度问题，又必须应对**文本条件生成**的语义对齐挑战。这使得方法设计必须在“数据效率”与“条件可控性”之间寻找平衡点。

### 2. 与无条件LiDAR生成方法的继承与超越

在无条件生成维度上，T2LDM 建立在扩散模型（DDPM）的谱系之上，直接可比的方法包括：

- **LiDARGen** (Zyrianov et al., ECCV 2022)：首个将DDPM应用于范围图（Range Map）的LiDAR生成方法，证明了扩散模型在该模态的可行性。
- **LiDM** (Ran et al., CVPR 2024)：在LiDARGen基础上改进的扩散生成方法。
- **R2DM** (Nakashima and Kurazume, ICRA 2024)：另一支基于DDPM的LiDAR生成工作。

这些方法的共同局限在于：**仅依赖标准的去噪损失 $L(\theta) = \mathbb{E} \|v - v_\theta\|^2$ 进行训练，缺乏对几何细节的显式正则化**。在数据稀缺条件下，模型倾向于学习平滑的平均场景，丢失车辆、行人等小目标的精细结构。

T2LDM 的突破在于引入**自条件表示引导（SCRG）**：通过一个与去噪网络（DN）结构相同的引导网络（GN），从数据分布中学习几何重建细节，并与DN的多层噪声特征进行余弦相似度对齐。这一设计的核心洞察是：**GN仅在训练早期（前100K步）参与梯度更新，推理时完全解耦**，因此在不增加推理成本的前提下，为DN提供了几何细节的软监督。

消融实验（Table 8）直接验证了这一机制的有效性：在KITTI-360训练仅30k迭代时，含SCRG的T2LDM FSVD为47.29，而无SCRG的变体高达217.18，表明SCRG显著加速了高频语义的早期学习。

此外，T2LDM 还超越了基于GAN和VAE的早期方法：
- **LiDARVAE** / **LiDARGAN** (Caccia et al., IROS 2019)：VAE和GAN范式在LiDAR生成上的早期探索，生成质量受限于模式坍塌和模糊问题。
- **ProjectedGAN** (Sauer et al., NeurIPS 2021)：将投影GAN应用于LiDAR生成，但同样缺乏对球面几何特性的建模。

### 3. 与文本引导LiDAR生成方法的对比

在文本条件生成维度上，**Text2LiDAR** (Wu et al., ECCV 2024) 是最直接的可比基线。两者均使用CLIP文本编码器将提示映射到语义特征空间，但T2LDM在以下方面形成差异化：

1. **几何正则化机制**：Text2LiDAR仅依赖文本条件注入，缺乏对几何细节的显式引导。T2LDM通过SCRG的扰动-条件自适应正则化，使DN在文本条件基础上额外感知几何先验。

2. **方向先验建模**：T2LDM设计了**方向位置编码（DPE）**，通过计算范围图中每个像素的水平角 $\theta$ 和垂直角 $\phi$，经傅立叶级数展开后以可学习门控注入主干特征。这解决了范围图卷积将球面投影视为普通2D图像所导致的0°/360°边界方向混淆问题——现有方法常因此产生弯曲或断裂的街道（Figure 2c）。

定量对比验证了这些设计的累积优势：
- 在KITTI-360无条件生成中，T2LDM的FSVD为21.12，Text2LiDAR为51.55（降幅约59%）（Table 2）。
- 在nuScenes文本引导生成中，T2LDM的TBR为23.44%，Text2LiDAR为17.15%（提升6.29个百分点）（Table 4）。

### 4. 与稀疏到密集上采样方法的关联

T2LDM展示了超出文本生成的泛化能力：在稀疏到密集LiDAR上采样任务中，其性能超越了专用上采样方法：

- **PUDM** (Qu et al., CVPR 2024)：点云上采样扩散模型。
- **Grad-PU** (He et al., CVPR 2023)：基于梯度的点云上采样方法。

在nuScenes 4×上采样设置下，T2LDM的倒角距离（CD）为0.104×10⁻⁵，PUDM为0.198×10⁻⁵（降幅约47%）（Table 5）。这表明SCRG学到的几何先验具有跨任务的迁移能力——GN重建的细节特征不仅服务于生成，也能指导稀疏输入的稠密化。

### 5. 适用边界与已知局限

尽管T2LDM在多个基准上取得显著提升，其适用边界受以下因素制约：

1. **文本标注的泛化性限制**：当前文本描述依赖3D框标注作为先验生成场景级描述（如“雨天，十字路口，多辆车”）。对于缺乏3D框标注的LiDAR数据集，该方法无法直接迁移。这是一个**数据管线层面的瓶颈**，而非模型架构问题。

2. **单条件控制约束**：T2LDM目前仅支持文本单条件生成，无法同时结合语义图、边界框等多模态条件。在多条件可控生成日益重要的背景下，这限制了其在需要精确空间控制的场景（如特定布局的仿真数据生成）中的应用。

3. **训练资源开销**：SCRG引入与DN相同架构的GN，训练时参数量翻倍。虽然推理时GN被解耦，但训练阶段的计算和显存需求显著增加。对于资源受限的研究团队，这可能构成复现障碍。

4. **稀疏场景的绝对质量**：尽管T2LDM在nuScenes（32线）上优于所有基线，其FSVD绝对值（64.21）仍显著高于KITTI-360（64线）上的21.12。这表明在极稀疏的LiDAR配置下，几何细节的恢复仍具挑战性。

### 6. 开放问题与未来方向

基于上述分析，以下开放问题值得后续工作关注：

1. **替代文本先验的生成**：如何针对无3D框标注的数据集，开发基于自监督或弱监督的场景描述生成方法？可能的路径包括利用视觉-语言模型（VLM）直接从LiDAR投影图生成描述，或通过对比学习从图像-文本对中迁移语义。

2. **多条件可控生成的集成**：能否将语义图布局控制、文本语义引导、边界框空间约束统一到T2LDM框架中？这需要在交叉注意力机制中引入多源条件融合模块，同时保持SCRG的正则化效果不被稀释。

3. **引导网络的轻量化**：能否通过知识蒸馏、剪枝或设计非对称架构（如GN使用更浅的U-Net）来降低训练开销？关键挑战在于保持GN提供的几何监督质量不因轻量化而退化。

4. **跨模态迁移潜力**：SCRG的核心思想——以特征空间对齐方式提供软几何监督——是否可推广到图像、视频等其他模态的生成任务中？这需要验证“自条件表示引导”在不同数据分布下的通用性。

5. **评估指标的完备性**：当前主要依赖FSVD、FID等分布距离指标，但这些指标对几何细节的敏感度有限。是否需要开发专门针对LiDAR场景结构保真度的评估协议（如目标级重建精度、道路连续性度量）？

## 原文 PDF

![[paperPDFs/CVPR_2026/A_Self_Conditioned_Representation_Guided_Diffusion_Model_for_Realistic_Text_to_LiDAR_Scene_Generation.pdf]]