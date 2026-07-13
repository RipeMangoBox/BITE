---
title: Interspatial Attention for Efficient 4D Human Video Generation
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/Interspatial_Attention_for_Efficient_4D_Human_Video_Generation.pdf
project_link: "https://dsaurus.github.io/isa4d/"
code_link: "https://github.com/Mochi-Team/mochi"
aliases:
- IDIADT
- IAE4HVG
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 基于SMPL 3D模板的对称跨空间注意力（ISA）与相对位置编码（ISPE），通过3D-2D NDC投影建立显式几何对应，为扩散模型提供精确的空间引导。
primary_logic: 将SMPL 3D点投影至归一化设备坐标（NDC）与2D视频token对齐，并嵌入相对位置编码至对称交叉注意力中，使网络能学习3D-2D对应关系，从而高效地注入3D条件，显著改善姿态控制、身份保持以及复杂场景下的生成一致性。
claims:
- 在所有场景（静态背景、相机运动、背景蒙版）和PSNR/SSIM/LPIPS/FVD指标下，ISA-DiT均超越SOTA基线方法。
- 带有ISPE的ISA比无ISPE或2D ControlNet收敛更快、损失更低，PSNR提升显著（28.34 vs 25.21 vs 26.45）。
- 自定义视频VAE（含正则化）产生的潜分布更接近高斯分布，使扩散模型训练更快、损失更低。
- 定性比较显示，ISA在面部表情、衣物动态和手物交互等方面明显优于基线方法。
---

# Interspatial Attention for Efficient 4D Human Video Generation

> [!tip] 核心洞察
> 将SMPL 3D点投影至归一化设备坐标（NDC）与2D视频token对齐，并嵌入相对位置编码至对称交叉注意力中，使网络能学习3D-2D对应关系，从而高效地注入3D条件，显著改善姿态控制、身份保持以及复杂场景下的生成一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 高效4D人体视频生成的跨空间注意力机制 |
| 英文题名 | Interspatial Attention for Efficient 4D Human Video Generation |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](http://arxiv.org/abs/2505.15800v2) · [Project](https://dsaurus.github.io/isa4d/) · [paper](https://arxiv.org/abs/2412.03603) · [Code](https://github.com/Mochi-Team/mochi) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ISA-DiT (Interspatial Attention Diffusion Transformer) |
| Dataset | Human4DiT Dataset, VBench |

> [!tip] 效果简介
> - Human4DiT Dataset (Video scenario) 上，PSNR 28.34 vs various SOTA baselines (see Table 2) (outperforms all baselines)。
> - VBench 上，Quality 0.724 vs Cosmos, Hunyuan, WAN2.1 (see Table 3) (comparable to larger models with far fewer parameters)。

## 概要

现有视频VAE难以编码快速人体运动，导致重建模糊且潜空间分布不佳；视频扩散模型缺少显式的3D-2D空间对应关系，无法有效处理遮挡、多人交互等复杂场景下的多视角一致性和身份保持。针对上述瓶颈，本文提出**ISA-DiT**框架，核心创新为**跨空间注意力（Interspatial Attention, ISA）**与**跨空间位置编码（ISPE）**——将SMPL 3D模板点投影至归一化设备坐标（NDC），与2D视频token对齐后嵌入对称交叉注意力，使网络能学习精确的3D-2D几何对应关系。同时，自研视频VAE引入时空数据增强与图像解码正则化，构建更接近高斯分布的潜空间，加速扩散模型训练。

实验表明，ISA-DiT在静态背景、相机运动、背景蒙版三种场景下的PSNR/SSIM/LPIPS/FVD指标均超越AnimateAnyone、Champ、Human4DiT等SOTA基线；ISA配合ISPE的PSNR达28.34，显著优于无ISPE（25.21）和2D ControlNet（26.45）方案。在VBench上，以远少于Cosmos、Hunyuan等大模型的参数量取得可比质量。定性结果在面部表情、衣物动态和手物交互等方面明显优于基线。该方法定位于参数化人体模板与视频扩散模型的交叉点，为4D人体生成提供了高效、可扩展的3D条件注入新范式。

## 核心方法与创新机理

### 瓶颈与核心思路

现有视频扩散模型在生成4D人体视频时面临两个根本性瓶颈：**视频VAE难以编码快速人体运动**，导致重建模糊且潜空间分布不佳；**缺少显式的3D-2D空间对应关系**，使模型无法有效处理遮挡、多人交互等复杂场景下的多视角一致性和身份保持。

核心解决思路是：利用SMPL 3D模板建立精确的几何对应，将3D表面点投影至归一化设备坐标（NDC）空间与2D视频token对齐，并通过**对称跨空间注意力（ISA）**与**相对位置编码（ISPE）**将这一几何先验注入扩散模型，使网络能够学习3D-2D对应关系。

### 关键创新点（Changed Slots）

**Slot 1：3D条件注入方式** — 从2D ControlNet到对称ISA+ISPE

基线方法将SMPL法向图渲染为2D图像，通过ControlNet或通道拼接注入条件（Table 4中“2D ControlNet”对应PSNR 26.45）。ISA-DiT则直接在3D token与2D token之间建立对称交叉注意力，配合基于NDC的相对位置编码（ISPE），使网络显式感知3D-2D几何对应（PSNR提升至28.34）。消融实验（Table 4, Fig. 14）表明，ISPE是性能提升的关键——去掉ISPE后PSNR降至25.21，验证损失收敛速度和终值均劣于完整ISA。

![[assets/figures/papers/paper_list_l5_http_arxiv_org_abs_2505_15800v2/figures/017_Figure_14.jpg]]
*Figure 14: Ablation of interspatial attention. We compare validation loss curves for the same DiT architecture using three different conditioning mechanisms: a baseline that only uses the 2D SMPL normal maps for conditioning, ISA without interspatial positional encoding, and interspatial attention with positional encoding. The latter conditioning converges faster and to a lower loss value than the other options*

**Slot 2：视频VAE架构** — 从预训练图像/视频VAE到定制化训练

现有视频VAE（Mochi、CogVideoX、Cosmos）在快速人体运动场景下重建质量不足。ISA-DiT从头构建视频VAE，引入三项关键设计：**时序因果3D卷积**、**3D判别器**、**时空数据增强**（随机结构化运动与动态速度调整），并加入**图像解码正则化**以缓解“末帧偏置”问题（Fig. 2）。该正则化虽略微降低重建指标（Table 1: PSNR 36.71→35.48），但使潜分布更接近高斯（Fig. 5），从而显著加速扩散模型训练收敛（Fig. 6）。

### 核心机制：对称跨空间注意力（Symmetric ISA）

ISA的核心是将3D SMPL token与2D视频token在统一的NDC空间中对齐，并通过双向交叉注意力实现信息交换。

**3D token编码**：从SMPL网格采样表面点 $\mathbf{G}_i$，经正弦位置编码和MLP映射为3D token：
$$\mathbf{Y}_{i} = \operatorname{F}_{\operatorname{mlp}}(\operatorname{PE}(\mathbf{G}_{i}))$$

**NDC投影对齐**：使用模型-视图-投影矩阵 $\mathbf{M}$ 将3D token投影至NDC空间：
$$\mathbf{g}_{ndc} = \left[\frac{x_{clip}}{w_{clip}}, \frac{y_{clip}}{w_{clip}}, \frac{z_{clip}}{w_{clip}}\right]^{T}$$
同时将2D潜在像素坐标投影至NDC深度为0的平面：
$$\mathbf{s}_{ndc} = (2 s_x / w - 1, 2 s_y / h - 1, 0)$$

**对称注意力运算**：2D token作为查询关注3D token（3D→2D注入），3D token作为查询关注2D token（2D→3D注入），双方均加入基于NDC坐标的相对位置编码：
$$\mathbf{z}_{j}^{\prime} = \mathrm{ISATTENTION}\big(\mathrm{Q}(\mathbf{z}_{j} + \mathrm{PE}(\mathbf{s}_{ndc})), \mathrm{K}(\mathcal{Y}_{j} + \mathrm{PE}(\mathbf{g}_{ndc})), \mathrm{V}(\mathcal{Y}_{j} + \mathrm{PE}(\mathbf{g}_{ndc}))\big)$$
$$\pmb{y}_{j}^{\prime} = \mathrm{ISATTENTION}(\mathrm{Q}(\pmb{y}_{j} + \mathrm{PE}(\mathbf{g}_{ndc})), \mathrm{K}(\mathbf{z}_{j} + \mathrm{PE}(\mathbf{s}_{ndc})), \mathrm{V}(\mathbf{z}_{j} + \mathrm{PE}(\mathbf{s}_{ndc})))$$

这种对称设计使3D条件注入不再是单向的“控制信号”，而是双向的特征增强——3D token从2D特征中获取外观和纹理信息，2D token从3D token中获取精确的空间引导。

### 整体流水线（ISA-DiT Pipeline）

ISA-DiT以Flow Matching扩散范式为基础，流水线包含以下模块（Fig. 8）：

![[assets/figures/papers/paper_list_l5_http_arxiv_org_abs_2505_15800v2/figures/009_Figure_8.jpg]]
*Figure 8: ISA-DiT pipeline. Overview of our diffusion transformer architecture for 4D human generation taking the reference image, SMPL condition, camera poses, and background videos as input. Our framework starts by tokenizing 3D SMPL conditions. In parallel, 2D video tokens (i.e., “noisy latents”) are optionally composited with background elements and processed through a cascade of disentangled spatial and temporal transformer blocks, enabling efficient modeling of spatio-temporal relationships. These tokens then seamlessly interact with pose tokens via our Interspatial Transformer Block, facilitating effective 3D-aware conditioning. The generated features are further enhanced through Plücker camer...*

1. **VideoVAE编码器**：将输入视频压缩为时空潜在表示
2. **SMPL Token化**：采样SMPL表面点并编码为3D token
3. **空间Transformer**：逐帧处理2D视频token
4. **时间Transformer（2D+3D分支）**：分别建立视频特征和SMPL特征的时序关联
5. **对称ISA Block**：在3D与2D token间执行双向交叉注意力（含ISPE）
6. **身份注入模块**：将参考图像特征通过像素对齐投影传播至3D SMPL token，再经交叉注意力注入2D特征
7. **相机条件模块**：将相机位姿编码为Plücker坐标，拼接后经交叉注意力注入
8. **背景集成模块**：背景视频经VAE编码后与主视频潜在表示拼接

### 训练目标

扩散过程采用Flow Matching范式，DiT骨干预测流场 $\mathbf{v} = \mathbf{x}_0 - \boldsymbol{\epsilon}$。VAE训练采用加权多损失组合：
$$\mathcal{L} = \lambda_{L1} \mathcal{L}_{L1} + \lambda_{p} \mathcal{L}_{p} + \lambda_{KL} \mathcal{L}_{KL} + \lambda_{reg} \mathcal{L}_{reg} + \lambda_{3DGAN} \mathcal{L}_{3DGAN} + \lambda_{2DGAN} \mathcal{L}_{2DGAN}$$
其中 $\mathcal{L}_{reg}$ 为图像解码正则化项，是使潜空间分布改善、加速扩散训练的关键设计。

## 实验与关键发现

### 核心定量结果：ISA-DiT在4D人体视频生成中全面超越SOTA

ISA-DiT在Human4DiT数据集上，针对三种场景（静态背景Video、相机运动Camera、背景蒙版Mask），以PSNR、SSIM、LPIPS、FVD四项指标全面超越**AnimateAnyone**（Hu et al., 2023）、**Champ**（Zhu et al., ECCV 2024）、**MusePose**（Tong et al., 2024）、**Animate-X**（Tan et al., 2024）和**Human4DiT**（Shao et al., 2024）等基线方法（Table 2）。其中PSNR达到28.34，在所有场景和指标下均为最优。

![[assets/figures/papers/paper_list_l5_http_arxiv_org_abs_2505_15800v2/figures/010_Table_2.jpg]]
*Table 2: Quantitative comparison of generated videos. We compare our method with state-of-the-art baselines AnimateAnyone [Hu et al. 2023b], Champ [Zhu et al. 2024], MusePose [Tong et al. 2024], Animate-X [Tan et al. 2024], and Human4DiT [Shao et al. 2024] using multiple metrics (PSNR, SSIM, LPIPS, and FVD). Specifically, we evaluate three scenarios: videos with a static background (“Video”), with camera movement (“Camera”), and with background mask applied (“Mask”). Our approach achieves superior quality across all metrics and all scenarios*

在VBench基准上，ISA-DiT与大规模视频生成模型**Cosmos**（Reda et al., 2024）、**Hunyuan**（Kong et al., 2024）、**WAN2.1**（Wang et al., 2025）对比，以远少于这些模型的参数量取得了可比的Quality分数（0.724），验证了ISA机制的高效性（Table 3）。

![[assets/figures/papers/paper_list_l5_http_arxiv_org_abs_2505_15800v2/figures/012_Table_3.jpg]]
*Table 3: Quantitative comparison based on VBench. We compare our method with state-of-the-art image-to-video methods including Cosmos [Reda et al. 2024], Hunyuan [Kong et al. 2024], and WAN2.1 [Wang et al. 2025] using multiple metrics (Quality, Aesthetics, and Consistency)*

定性比较（Fig. 9）进一步显示，ISA-DiT在面部表情捕捉、衣物动态建模和手物交互渲染等方面明显优于最佳基线方法，生成结果更具自然感和真实感。

![[assets/figures/papers/paper_list_l5_http_arxiv_org_abs_2505_15800v2/figures/011_Figure_9.jpg]]
*Figure 9: Qualitative comparisons of generated videos. We compare our approach with the best-performing baselines; each of these methods is conditioned on the reference image shown on the left. Our method achieves superior visual quality, particularly in capturing facial expressions, modeling clothing dynamics, and rendering natural hand–object interactions*

### 消融实验：ISA与ISPE是性能提升的关键

消融实验（Table 4, Fig. 14）揭示了ISA及其相对位置编码ISPE的因果贡献：

- **ISA + ISPE vs. ISA w/o ISPE**：PSNR从25.21提升至28.34（+3.13），验证损失曲线收敛更快、最终值更低，表明基于NDC投影的显式3D-2D几何对应关系对扩散模型训练至关重要。
- **ISA vs. 2D ControlNet**：ISA（PSNR 28.34）显著优于使用2D SMPL法线图通过ControlNet注入条件的方式（PSNR 26.45），在复杂3D姿态下，ControlNet产生不自然的变形，而ISA生成的动作更为自然（Fig. 15）。
- **3D模板扩展性**：将SMPL替换为更精细的**FLAME 3D面部模型**后，面部生成PSNR从30.42进一步提升至31.05（Table 4, Fig. 16），表明ISA机制可无缝兼容更高精度的3D模板，实现更生动的表情生成。

### 视频VAE的贡献：潜空间质量决定扩散模型训练效率

自定义视频VAE在重建质量上超越Mochi、CogVideoX、Cosmos等现有tokenizer（Table 1, Fig. 3, Fig. 4）。关键发现是：**图像解码正则化（image-decoding regularization）**虽然略微降低了VAE的重建指标（PSNR 36.71 vs. 36.58），但显著改善了潜空间分布（Fig. 5），使其更接近高斯分布。使用该正则化VAE的潜变量训练扩散Transformer时，收敛速度更快、验证损失更低（Fig. 6），证明良好的潜空间结构对扩散模型训练效率具有决定性影响。正则化还解决了“最后一帧偏差”问题（Fig. 2），使潜变量在各帧间保持均衡的时间信息分布。

![[assets/figures/papers/paper_list_l5_http_arxiv_org_abs_2505_15800v2/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of video tokenizers. While omitting regularization terms slightly improves reconstruction quality, adding regularization makes video diffusion model training more efficient*

### 失败模式与适用边界

ISA-DiT存在以下明确限制（Fig. 17）：

1. **SMPL估计依赖**：当多人场景中出现错误的角色间遮挡估计时，生成结果产生明显伪影。方法对SMPL输入的准确性高度敏感。
2. **快速相机运动**：激进的视角变化会导致背景扭曲失真，模型难以维持背景一致性。
3. **极端视角与全景背景**：当前方法无法有效处理极端相机变化和360°全景背景的生成，这些场景仍为开放挑战。

## 定位与知识库关联

### 与现有工作的本质差异

**ISA-DiT** 的核心区分点不在于扩散 Transformer 骨干本身，而在于**如何将 3D 几何先验注入 2D 视频生成过程**。现有方法可归为两类路径，ISA-DiT 对两者均构成结构性替代：

1. **2D 条件注入路线**（AnimateAnyone, Hu et al., arXiv 2023; Champ, Zhu et al., ECCV 2024; MusePose, Tong et al., arXiv 2024; Animate-X, Tan et al., arXiv 2024）：这些方法将 SMPL 姿态渲染为 2D 法向图或骨架图，通过 ControlNet 或通道拼接注入扩散模型。瓶颈在于 **2D 渲染丢失了深度和遮挡信息**，网络缺乏显式的 3D-2D 对应关系，导致复杂姿态下产生非物理形变（Fig. 15 中 ControlNet 在复杂 3D 姿态下出现不合理的肢体扭曲）。ISA 则直接在 3D SMPL token 与 2D 视频 token 之间建立对称交叉注意力，并通过 NDC 投影提供精确的几何对应，从机制上规避了 2D 投影的信息损失。

2. **3D 感知路线**（Human4DiT, Shao et al., arXiv 2024）：Human4DiT 同样使用 SMPL 条件和扩散 Transformer，但其 3D 条件注入方式与 ISA 存在根本差异。Human4DiT 未采用跨空间注意力机制，缺少基于 NDC 的相对位置编码（ISPE），因此 3D 几何信号无法精确对齐到 2D 特征空间。消融实验（Table 4）直接验证了这一差异：ISA 无 ISPE 变体（PSNR 25.21）与 2D ControlNet 变体（PSNR 26.45）均显著低于完整 ISA（PSNR 28.34），证明 **ISPE 提供的显式 3D-2D 空间引导是性能增益的关键来源**。

3. **视频 VAE 层面**：现有视频生成方法普遍复用预训练图像 VAE（如 SD3）或通用视频 VAE（Mochi, CogVideoX, Cosmos）。这些 VAE 在处理快速人体运动时面临两个瓶颈：一是**末帧偏置**（Fig. 2），潜空间将信息过度压缩到时间窗口的最后一帧；二是**潜分布偏离高斯分布**（Fig. 5），阻碍扩散模型训练。ISA-DiT 的自研 VAE 通过时序因果 3D 卷积、时空数据增强（随机结构化运动、动态速度调整）和图像解码正则化，同时解决了这两个问题——虽轻微牺牲重建指标（Table 1: PSNR 36.71 vs 37.02），但使扩散模型训练收敛更快、损失更低（Fig. 6）。

### 知识库挂载点

ISA-DiT 可挂载到以下知识节点：

- **3D 模板驱动生成**：SMPL（Loper et al., SIGGRAPH Asia 2015）作为人体先验，FLAME（Li et al., SIGGRAPH 2017）作为面部先验。ISA 的 3D token 化策略（表面点采样 → 正弦位置编码 → MLP 编码）可兼容任意三角网格模板，Table 4 已验证 SMPL 替换为 FLAME 后面部生成 PSNR 从 30.42 提升至 31.05，表明该机制对更精细的 3D 模板具有即插即用性。
- **扩散 Transformer 架构**：ISA 块作为 DiT（Peebles & Xie, ICCV 2023）的可插拔模块，与空间 Transformer、时间 Transformer 解耦串联（Fig. 8），不影响骨干网络的缩放特性。
- **视频 VAE 设计**：架构受 MAGVIT-v2（Yu et al., CVPR 2023）和 W.A.L.T.（Gupta et al., ICCV 2023）启发，采用联合图像-视频压缩的统一架构，支持任意长度视频。
- **Flow Matching 训练范式**：采用 $v = x_0 - \epsilon$ 的流匹配目标，与 Stable Diffusion 3（Esser et al., arXiv 2024）等最新工作一致。

### 适用边界

ISA-DiT 的当前边界由以下约束定义：

1. **SMPL 估计依赖**：ISA 的 3D-2D 对应关系建立在 SMPL 模板的准确性之上。当多人遮挡导致 SMPL 估计错误时，生成结果出现明显伪影（Fig. 17 左下）。这是方法的**结构性脆弱点**——ISA 本身不修正错误的 3D 先验，而是忠实地将其映射到 2D 空间。
2. **相机运动范围**：快速相机移动时背景产生扭曲（Fig. 17 右），表明 Plücker 坐标编码和背景集成模块在极端视角变化下尚不稳定。360° 全景背景生成仍为开放问题。
3. **非人体对象泛化**：当前 ISA 的 3D token 化依赖 SMPL/FLAME 等参数化人体模板，向非人体动态场景（如动物、车辆）的推广需要对应的 3D 模板，尚未验证。

### 后续启发

ISA 的设计原则——**在 3D 模板 token 与 2D 像素 token 之间建立 NDC 投影对齐的对称交叉注意力**——为以下方向提供了可迁移的技术路径：

- **通用 3D 条件注入**：将 SMPL 替换为任意可渲染 3D 表示（如 NeRF、3D Gaussian Splatting），ISA 机制可扩展至场景级 3D 感知视频生成。
- **多模态空间对齐**：ISPE 的 NDC 投影思想可推广到其他需要 3D-2D 对齐的任务，如 3D 感知的图像编辑、多视角一致性生成。
- **轻量化 3D 条件**：当前 SMPL token 数量固定，探索自适应 token 剪枝或稀疏注意力可降低计算开销，推动实时应用。
- **鲁棒 3D 先验**：引入不确定性建模或迭代修正机制，缓解 SMPL 估计错误对生成质量的连锁影响，是提升多人遮挡场景鲁棒性的关键方向。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/Interspatial_Attention_for_Efficient_4D_Human_Video_Generation.pdf]]