---
title: "Sat3DGen: Comprehensive Street-Level 3D Scene Generation from Single Satellite Image"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Sat3DGen_Comprehensive_Street_Level_3D_Scene_Generation_from_Single_Satellite_Im_d04b4ece93f7.pdf
project_link: null
code_link: "https://github.com/qianmingduowan/Sat3DGen"
aliases:
- Sat3DGen
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 显式的几何先验注入（重力对齐密度损失、单目相对深度先验、空间令牌扩展边界、透视训练增强视角覆盖），直接弥补了几何约束的缺失。
primary_logic: 在前馈图像到3D框架中，通过集成几何启发的正则化（重力约束、单目深度先验和空间填充）和增加有效视角覆盖，可以大幅提升卫星到街道3D场景的几何精度和真实感，而无需额外的图像质量模块。
claims:
- 几何RMSE从6.76m降至5.20m，提升23%。
- FID从~40降至19，真实感大幅提升。
- 消融表明重力损失对真实感最关键，深度损失和空间令牌对几何最关键，透视训练带来额外提升。
- VIGOR-OOD 上 FID↓ = 19.2
---

# Sat3DGen: Comprehensive Street-Level 3D Scene Generation from Single Satellite Image

> [!tip] 核心洞察
> 在前馈图像到3D框架中，通过集成几何启发的正则化（重力约束、单目深度先验和空间填充）和增加有效视角覆盖，可以大幅提升卫星到街道3D场景的几何精度和真实感，而无需额外的图像质量模块。

| 字段 | 内容 |
|------|------|
| 中文题名 | Sat3DGen：从单张卫星图像生成全面的街道级三维场景 |
| 英文题名 | Sat3DGen: Comprehensive Street-Level 3D Scene Generation from Single Satellite Image |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=E7JzkZCofa) · [Code](https://github.com/qianmingduowan/Sat3DGen) · [arXiv](https://arxiv.org/abs/1602.07360) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Sat3DGen |
| Dataset | VIGOR-OOD |

> [!tip] 效果简介
> - VIGOR-OOD 上，FID↓ 19.2 vs 40.8 (Sat2Density++) (-21.6)；KID↓ 0.014 vs 0.035 (Sat2Density++) (-0.021)；DINO↑ 0.525 vs 0.465 (Sat2Density++) (+0.060)。
> - VIGOR-OOD (geometric) 上，RMSE(m)↓ 5.20 vs 6.76 (Sat2Density++) (-1.56)。

## 概述

Sat3DGen 提出了一种前馈式图像到三维场景生成框架，旨在从单张卫星图像直接重建包含建筑、植被、道路等完整语义的街道级三维场景。该任务的核心瓶颈在于极端的卫星-街道视角差距与稀疏、不一致的监督信号，导致现有方法普遍存在屋顶不规则、立面伪影和边界扭曲等几何失真问题。

为解决上述问题，Sat3DGen 在标准的三平面 NeRF 基线上引入了四项关键设计：**重力对齐密度损失**（Gravity-based Density Variation Loss）惩罚密度随高度异常增长，抑制漂浮伪影；**单目相对深度先验**（Satellite-view Depth Regularization）利用 Depth Anything v2 提供尺度-平移不变的几何约束；**空间令牌填充**（Spatial Token Padding）扩展场景边界以容纳周边内容；**透视视角训练**（Perspective View Training）增加有效视角覆盖。这些组件共同构成了显式的几何先验注入机制，直接弥补了前馈框架中几何约束的不足。

在 VIGOR-OOD 跨域测试集上，Sat3DGen 相较于领先的代理式基线 **Sat2Density++**（Qian et al., 2026）取得了显著提升：几何 RMSE 从 6.76m 降至 5.20m（提升 23%），FID 从约 40 降至 19.2，真实感大幅增强。消融实验进一步揭示，重力损失对真实感最为关键，深度损失与空间令牌对几何精度贡献更大，透视训练则带来额外的综合性能增益。

从方法谱系来看，Sat3DGen 定位于前馈图像到三维生成与几何正则化的交叉点。相较于仅输出建筑外壳的几何着色方法（如 **Sat2Scene**、**Sat2City**），该方法保留了完整的语义内容；相较于缺乏几何约束的通用图像到三维框架，其通过任务特化的先验注入实现了更高的结构规整性。这一设计思路为跨视角三维场景生成中的几何精度问题提供了一种不依赖额外图像质量模块的解决方案。

## 背景与动机

### 卫星到街景3D场景生成的挑战

从单张卫星图像生成逼真的街道级3D场景，是连接宏观遥感与微观街景感知的关键桥梁。这一能力在自动驾驶仿真、城市规划、虚拟现实等领域具有重要应用价值。然而，该任务面临一个核心瓶颈：**极端的卫星-街道视角差距**。卫星图像通常以近似正交投影捕获大范围区域，而街景图像则是从地面高度以透视投影观察局部场景，两者在尺度、视角和语义粒度上存在巨大差异。

这种视角鸿沟直接导致前馈图像到3D方法的几何约束严重不足。现有方法在将卫星图像直接映射到3D场景表示时，普遍表现出三类典型失效模式：
- **屋顶不规则**：建筑顶部结构缺乏一致性，出现扭曲或断裂；
- **立面伪影**：建筑垂直面上产生漂浮的纹理碎片或密度异常；
- **边界扭曲**：场景边缘区域因缺乏足够的空间上下文而严重变形。

### 现有方法的局限性

当前卫星到街景3D生成方法可大致分为两类，但均存在明显不足：

**几何着色方法**（如 **Sat2Scene**（Li et al., 2024b）、**Sat2City**（Hua et al., 2025））仅能生成建筑和道路的几何外壳，完全缺失植被、车辆、街道设施等非建筑语义元素。这类方法本质上是对卫星图像进行高度估计后转换为点云，其表达能力受限于显式几何管线，无法捕捉丰富的场景外观。

**代理式前馈方法**（如 **Sat2Density**（Qian et al., 2023）、**Sat2Density++**（Qian et al., 2026））虽然能够保留卫星语义并生成包含多类物体的完整场景，但其3D几何质量严重退化。如Figure 1所示，Sat2Density++的结果存在明显的结构扭曲，几何RMSE高达6.76m，街景渲染的FID约为40，真实感不足。

**基于扩散的2D生成方法**（如 **ControlNet**（Zhang et al., 2023）、**ControlS2S**（Ze et al., 2025））虽然能生成高质量的街景图像，但缺乏3D一致性，无法支持自由视角渲染和3D资产提取。

### 核心洞察与本文动机

上述方法困境的根源在于：**稀疏且不一致的监督信号无法为卫星到街景的跨视角映射提供足够的几何约束**。街景全景图仅提供局部、不完整的观察，而卫星图像本身缺乏直接的3D信息。这导致模型在缺乏显式几何先验的情况下，难以推断合理的3D结构。

本文的核心洞察是：**在前馈图像到3D框架中，通过集成几何启发的正则化和增加有效视角覆盖，可以大幅提升卫星到街道3D场景的几何精度和真实感，而无需额外的图像质量模块**。具体而言，本文提出Sat3DGen，通过四个关键设计直接弥补几何约束的缺失：

1. **重力对齐密度损失**：利用物理先验惩罚密度随高度增加的现象，抑制漂浮伪影，强制建筑立面保持垂直结构；
2. **单目相对深度先验**：借助Depth Anything v2的伪深度进行尺度-平移不变约束，为卫星视图提供额外的几何监督；
3. **空间令牌扩展**：在令牌网格边界填充可学习的空间容量，有效扩展场景范围，缓解边界区域的几何扭曲；
4. **透视训练增强**：从全景图投影透视视图作为额外监督，增加有效视角覆盖，提升模型对透视变形的鲁棒性。

实验表明，这些几何启发的设计使Sat3DGen在VIGOR-OOD跨域测试集上，将几何RMSE从6.76m降至5.20m（提升23%），街景FID从约40降至19，在几何精度和真实感上均显著超越现有最强基线。

## 核心创新

Sat3DGen 的核心创新在于**对前馈图像到3D框架注入显式几何先验**，以弥合极端的卫星-街道视角差距。相较于领先的代理式基线 **Sat2Density++**（Qian et al., 2026），本方法在架构层面保持了相同的主干范式（DINO-v3 编码器 → 三平面 NeRF → 体渲染），但引入了四个关键变更槽位（changed slots），分别从物理合理性、深度感知、空间覆盖和视角多样性四个维度强化几何约束。

### 变更槽位一：重力对齐密度变化损失（Gravity-based Density Variation Loss）

**基线状态**：Sat2Density++ 仅依赖 RGB 重建损失和 GAN 损失，对体积密度的垂直分布无任何物理约束，导致屋顶不规则、立面出现漂浮伪影。

**提出方案**：引入重力对齐密度变化损失 $\mathcal{L}_{\mathrm{grav}}$，显式惩罚密度沿高度方向增加的现象：

$$\mathcal{L}_{\mathrm{grav}} = \mathbb{E}_{\mathbf{x}, \delta\mathbf{z}}[\operatorname{ReLU}(\sigma(\mathbf{x}+\delta\mathbf{z}) - \sigma(\mathbf{x}) - \epsilon)]$$

该损失允许密度在容忍阈值 $\epsilon$ 内小幅波动（如树木冠层），但严格抑制密度随高度持续增长，从而消除漂浮伪影并强化垂直结构的物理合理性。消融实验（Table 2）表明，移除该损失后 FID 从 21.6 恶化至 25.9，证明其对真实感最为关键；超参数 $\epsilon=1.0$ 取得最佳 FID/KID 平衡（Table 4）。

### 变更槽位二：卫星视图深度正则化（Satellite-view Depth Regularization）

**基线状态**：基线模型在训练中无任何深度监督信号，几何重建仅由多视图 RGB 一致性隐式驱动，导致屋顶高度估计偏差和边界扭曲。

**提出方案**：利用预训练单目深度估计器 **Depth Anything v2** 从卫星图像提取伪深度 $D^*$，并通过尺度-平移不变损失进行约束：

$$\mathcal{L}_{\mathrm{depth}} = \frac{1}{N}\sum_p |s\hat{D}(p) + t - D^*(p)| + \lambda_v \frac{1}{N}\sum_p \|\nabla(s\hat{D}(p) + t) - \nabla D^*(p)\|_1$$

该设计的关键在于：不要求绝对深度精度（卫星图像缺乏度量深度真值），而是通过可学习的尺度 $s$ 和平移 $t$ 对齐相对深度结构，同时用梯度一致性项保持边缘锐度。消融显示，移除深度损失导致几何 RMSE 从 5.23m 升至 5.75m（Table 2），证明其对几何精度的关键贡献。

### 变更槽位三：空间令牌填充（Spatial Token Padding）

**基线状态**：Sat2Density++ 的 DINO-v3 编码器仅处理卫星图像覆盖区域，输出 $16 \times 16$ 令牌网格，导致场景边界处的内容（如道路延伸、建筑边缘）无法被充分建模，产生截断伪影。

**提出方案**：在令牌网格四边各填充 $N=2$ 个零值空间令牌，将特征图扩展为 $20 \times 20$：

$$\mathbf{F}_{\mathrm{token-pad}} = \mathbf{PAD}_N(\mathbf{F}_{\mathrm{token}}) \in \mathbb{R}^{(H_t+2N) \times (W_t+2N) \times C}, N=2$$

这些填充令牌在后续三平面解码中为场景外围提供了可学习的容量，使模型能够推断卫星图像视场之外的内容。消融表明，移除空间令牌后几何 RMSE 从 5.23m 升至 5.64m（Table 2），证实其对边界几何完整性的作用。

### 变更槽位四：透视视图训练（Perspective View Training）

**基线状态**：现有方法仅在卫星视图和全景视图下进行监督，训练视角覆盖有限，导致从透视视角渲染时出现几何失真。

**提出方案**：在训练中额外从全景图像投影生成透视视图，并施加 RGB 监督。这一策略显著增加了有效视角覆盖，使模型学习到更鲁棒的 3D 表示。Table 2 显示，在启用前三个组件的基础上（Base 模型），加入透视训练使 FID 从 21.6 进一步降至 19.2，RMSE 从 5.23m 降至 5.20m，实现了最佳综合性能。

### 创新协同机制

四个变更槽位并非孤立作用，而是形成互补的几何约束体系：重力损失提供物理先验（垂直方向），深度损失提供单目几何线索（深度方向），空间令牌扩展几何容量（水平方向），透视训练增加视角多样性（观测方向）。消融实验（Table 2）的递进式设计清晰展示了这一协同效应——从移除了所有四个组件的“Canonical image-to-3D”基线开始，逐步添加各组件，性能单调提升，最终在完整模型上达到 FID 19.2、RMSE 5.20m 的最优结果。

值得注意的是，Sat3DGen 的创新集中于几何正则化层面，**未引入额外的图像质量增强模块**（如超分辨率或去噪网络），所有视觉质量提升均源自更精确的底层 3D 几何表示。这一设计哲学验证了核心洞察：在卫星到街道3D场景生成中，几何精度是真实感的上限瓶颈。

## 整体框架

Sat3DGen 是一个**前馈式图像到三维（feed-forward image-to-3D）框架**，以三平面神经辐射场（tri-plane NeRF）为骨干，从单张卫星图像直接推理出可渲染的街道级三维场景表示。框架的设计核心在于**用显式几何先验弥补卫星-街道极端视角差距造成的约束不足**，而非依赖额外的图像质量提升模块。

### 输入输出流

整个 pipeline 的输入是一张卫星图像 $I_{\mathrm{sat}}$，输出是一个支持新视角合成的隐式三维场景表示，可进一步提取为显式网格（mesh）、生成全景视频和多视角透视视频（Figure 4）。框架的推理流程可分为五个阶段：

1. **卫星编码与空间扩展**：冻结的 DINO-v3 ViT 编码器将卫星图像映射为紧凑的二维令牌网格，随后通过空间令牌填充扩展场景边界。
2. **三平面解码**：VAE 风格解码器将填充后的令牌上采样为高分辨率三平面特征场。
3. **三维采样与聚合**：对三维空间中的任意采样点，通过三正交平面的双线性插值并求和，得到该点的融合特征向量。
4. **密度-颜色预测与全局光照注入**：融合特征经 MLP 预测体积密度 $\sigma$ 和颜色 $\mathbf{c}$，同时全局光照编码控制场景的光照风格。
5. **体渲染与天空融合**：沿光线采样累积颜色，并融合球面天空特征图以提供一致的天空外观。

### 模块关系与数据流

Figure 2 展示了框架的完整数据流。以下按处理顺序描述各模块的角色与连接关系：

![[assets/figures/papers/paper_list_l60_https_openreview_net_forum_id_E7JzkZCofa/figures/003_Figure_2.jpg]]
*Figure 2: Diagram of the proposed Sat3DGen framework*

**卫星令牌化**。给定输入卫星图像 $I_{\mathrm{sat}}$，冻结的 DINO-v3 编码器 $\mathcal{E}_{\mathrm{sat}}$ 将其编码为 $H_t \times W_t \times C$ 的令牌网格（$H_t=W_t=16$，$C=1024$）：

$$\mathbf{F}_{\mathrm{token}} = \mathcal{E}_{\mathrm{sat}}(I_{\mathrm{sat}}) \in \mathbb{R}^{H_t \times W_t \times C}$$

冻结编码器的使用避免了在大规模三维训练中微调 ViT 带来的计算开销，同时保留了 DINO-v3 强大的语义提取能力。

**空间令牌填充**。由于卫星图像的覆盖范围通常小于需要生成的三维场景范围，直接在令牌网格上解码会导致边界区域缺乏几何约束，产生扭曲。为解决这一问题，在令牌网格的四周各填充 $N=2$ 个零值令牌：

$$\mathbf{F}_{\mathrm{token-pad}} = \mathbf{PAD}_N(\mathbf{F}_{\mathrm{token}}) \in \mathbb{R}^{(H_t+2N) \times (W_t+2N) \times C}$$

这些零令牌在解码过程中被赋予可学习的空间容量，使模型能够推断卫星图像覆盖范围之外的周边场景布局。消融实验证实，移除空间令牌会导致几何 RMSE 从 5.23 升至 5.64（Table 2），表明该模块对边界几何精度有显著贡献。

**三平面解码**。填充后的令牌网格被送入 VAE 风格解码器 $\mathcal{D}$，上采样为高分辨率三平面特征：

$$\mathbf{F}_{\mathrm{tri}} = \mathcal{D}(\mathbf{F}_{\mathrm{token-pad}}) \in \mathbb{R}^{\mathrm{res}_{\mathrm{tri}} \times \mathrm{res}_{\mathrm{tri}} \times 96}$$

在有填充的情况下，三平面分辨率达到 $320 \times 320 \times 96$。三个正交平面（$XY$、$XZ$、$YZ$）分别存储场景在不同投影方向上的特征表示。

**三维特征聚合**。对于三维空间中的任意采样点 $\mathbf{x}$，分别从三个正交平面进行双线性插值，并将结果求和得到融合特征：

$$\mathbf{h}(\mathbf{x}) = \phi_{XY}(\mathbf{x}) + \phi_{XZ}(\mathbf{x}) + \phi_{YZ}(\mathbf{x})$$

这种三平面聚合机制在保持高效推理的同时，提供了足够的三维表达能力。

**全局光照编码**。从输入卫星图像中提取全局光照代码 $w_{\mathrm{ill}}$，注入到颜色预测 MLP 中，使模型能够控制生成场景的光照风格（如晴天、阴天），并保证不同视角下光照的一致性。

**密度与颜色预测**。融合特征 $\mathbf{h}(\mathbf{x})$ 和光照代码 $w_{\mathrm{ill}}$ 经 MLP 预测该点的体积密度 $\sigma(\mathbf{x})$ 和颜色 $\mathbf{c}(\mathbf{x}, w_{\mathrm{ill}})$。

**天空生成模块**。为处理无几何覆盖的天空区域，框架建模了一个球面天空特征图，通过光线方向 $\mathbf{d}$ 查询天空颜色 $\mathbf{c}_{\mathrm{sky}}(\mathbf{d})$，确保全景渲染时天空外观的连续性。

**体渲染**。沿光线 $r$ 采样 $K$ 个点，通过 alpha 合成累积颜色，并融合天空背景：

$$\mathbf{C}(r) = \sum_k T_k(1 - e^{-\sigma(\mathbf{x}_k)\delta_k})\mathbf{c}(\mathbf{x}_k, w_{\mathrm{ill}}) + T_{\mathrm{out}}\mathbf{c}_{\mathrm{sky}}(\mathbf{d})$$

其中 $T_k$ 为累积透射率，$T_{\mathrm{out}}$ 为光线穿出场景后的剩余透射率，用于加权天空颜色。

**训练损失集成**。框架的总损失为多个监督项的加权组合：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{rgb}}\mathcal{L}_{\mathrm{RGB}} + \lambda_{\mathrm{grav}}\mathcal{L}_{\mathrm{grav}} + \lambda_{\mathrm{sky-op}}\mathcal{L}_{\mathrm{sky-op}} + \lambda_{\mathrm{sky-L1}}\mathcal{L}_{\mathrm{sky-L1}} + \lambda_{\mathrm{depth}}\mathcal{L}_{\mathrm{depth}}$$

其中 $\mathcal{L}_{\mathrm{grav}}$（重力密度变化损失）和 $\mathcal{L}_{\mathrm{depth}}$（卫星视图深度正则化）是核心的几何先验注入项，分别抑制漂浮伪影和提供单目深度约束。透视训练策略则通过增加从全景投影的透视视图监督，进一步扩展有效视角覆盖。消融表明，移除重力损失导致 FID 恶化最严重（从 21.6 升至 25.9），而移除深度损失或空间令牌则主要损害几何精度（Table 2），验证了各模块在真实感与几何精度上的分工互补关系。

## 核心模块与公式推导

Sat3DGen 的前馈图像到3D框架由三个核心阶段构成：**卫星令牌化与空间扩展**、**三平面特征场解码**、以及**几何正则化损失函数**。以下逐一展开关键模块及其公式。

### 3.1 卫星令牌化与空间令牌填充

给定输入卫星图像 $I_{\mathrm{sat}}$，首先通过**冻结的 DINO-v3 ViT 编码器**（Simeoni et al., 2025）将其映射为紧凑的2D令牌网格：

$$\mathbf{F}_{\mathrm{token}} = \mathcal{E}_{\mathrm{sat}}(I_{\mathrm{sat}}) \in \mathbb{R}^{H_t \times W_t \times C}$$

其中 $H_t = W_t = 16$，$C = 1024$。该令牌网格直接对应卫星图像的语义布局，但其有效范围受限于编码器的感受野，导致场景边界处的几何重建出现截断和扭曲。

为解决这一问题，引入**空间令牌填充**（Spatial Token Padding）：在令牌网格四边各添加 $N=2$ 个可学习的零值令牌，扩展场景边界以容纳周边内容：

$$\mathbf{F}_{\mathrm{token-pad}} = \mathbf{PAD}_N(\mathbf{F}_{\mathrm{token}}) \in \mathbb{R}^{(H_t+2N) \times (W_t+2N) \times C}$$

消融实验证实，移除空间令牌填充会导致几何 RMSE 从 5.23 上升至 5.64，表明该模块对边界几何精度至关重要（Table 2）。

### 3.2 三平面解码与特征聚合

填充后的令牌网格通过**VAE式解码器**上采样为高分辨率三平面特征：

$$\mathbf{F}_{\mathrm{tri}} = \mathcal{D}(\mathbf{F}_{\mathrm{token-pad}}) \in \mathbb{R}^{\mathrm{res}_{\mathrm{tri}} \times \mathrm{res}_{\mathrm{tri}} \times 96}$$

有填充时分辨率达到 $320 \times 320 \times 96$。对于3D空间中的任意采样点 $\mathbf{x}$，通过在三正交平面（XY、XZ、YZ）上进行双线性插值并求和，得到融合特征：

$$\mathbf{h}(\mathbf{x}) = \phi_{XY}(\mathbf{x}) + \phi_{XZ}(\mathbf{x}) + \phi_{YZ}(\mathbf{x})$$

该融合特征随后输入**密度和颜色 MLP**，预测体积密度 $\sigma(\mathbf{x})$ 和颜色 $\mathbf{c}(\mathbf{x}, w_{\mathrm{ill}})$，其中 $w_{\mathrm{ill}}$ 为全局光照代码，用于控制场景光照一致性。

### 3.3 体渲染与天空融合

沿光线 $r$ 采样后，通过体渲染方程累积颜色，并融合天空背景：

$$\mathbf{C}(r) = \sum_k T_k(1 - e^{-\sigma(\mathbf{x}_k)\delta_k})\mathbf{c}(\mathbf{x}_k, w_{\mathrm{ill}}) + T_{\mathrm{out}}\mathbf{c}_{\mathrm{sky}}(\mathbf{d})$$

其中 $T_k$ 为累积透射率，$T_{\mathrm{out}}$ 为光线穿透整个场景后的剩余透射率，$\mathbf{c}_{\mathrm{sky}}(\mathbf{d})$ 由**天空生成模块**根据视线方向 $\mathbf{d}$ 从球面天空特征图中采样得到，确保全景渲染中天空外观的一致性。

### 3.4 几何正则化损失函数

几何精度的大幅提升（RMSE 从 6.76m 降至 5.20m）主要归功于两个关键损失项。

**重力密度变化损失** $L_{\mathrm{grav}}$ 惩罚密度随高度增加的行为，强制场景符合重力方向上的密度递减先验，从而抑制漂浮伪影和屋顶不规则：

$$\mathcal{L}_{\mathrm{grav}} = \mathbb{E}_{\mathbf{x}, \delta\mathbf{z}}[\operatorname{ReLU}(\sigma(\mathbf{x}+\delta\mathbf{z}) - \sigma(\mathbf{x}) - \epsilon)]$$

其中 $\epsilon=1.0$ 为容忍阈值，允许合理的空洞结构（如拱门、桥洞）。消融表明，移除该损失导致 FID 从 21.6 恶化至 25.9，是影响真实感最关键的因素（Table 2, Table 4）。

**卫星视图深度正则化** $L_{\mathrm{depth}}$ 利用 Depth Anything v2 从卫星图像提取的单目相对深度作为伪监督，通过尺度-平移不变损失约束几何结构：

$$\mathcal{L}_{\mathrm{depth}} = \frac{1}{N}\sum_p |s\hat{D}(p) + t - D^*(p)| + \lambda_v \frac{1}{N}\sum_p \|\nabla(s\hat{D}(p) + t) - \nabla D^*(p)\|_1$$

其中 $\hat{D}(p)$ 为渲染的卫星视图深度，$D^*(p)$ 为 Depth Anything v2 预测的伪深度，$s$ 和 $t$ 为可学习的尺度和平移参数，梯度项约束深度边缘对齐。该损失对几何 RMSE 贡献显著：移除后 RMSE 从 5.23 升至 5.75（Table 2）。

**总损失函数**为各监督项的加权组合：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{rgb}}\mathcal{L}_{\mathrm{RGB}} + \lambda_{\mathrm{grav}}\mathcal{L}_{\mathrm{grav}} + \lambda_{\mathrm{sky-op}}\mathcal{L}_{\mathrm{sky-op}} + \lambda_{\mathrm{sky-L1}}\mathcal{L}_{\mathrm{sky-L1}} + \lambda_{\mathrm{depth}}\mathcal{L}_{\mathrm{depth}}$$

其中 $\mathcal{L}_{\mathrm{RGB}}$ 为渲染图像与真实全景/透视视图的像素级损失，天空相关损失项约束天空区域的透明度和颜色一致性。完整模型在此基础上加入透视视图训练，使 FID 进一步降至 19.2，RMSE 降至 5.20，实现了最佳综合性能。

## 实验与分析

### 核心定量结果

Sat3DGen 在 VIGOR-OOD 跨域测试集（未见城市 Seattle）上全面超越所有基线方法。与最强的代理式基线 **Sat2Density++**（Qian et al., 2026）相比，真实感指标 FID 从 40.8 降至 **19.2**（↓52.9%），KID 从 0.035 降至 **0.014**（↓60.0%），语义对齐指标 DINO 从 0.465 提升至 **0.525**（Table 1）。几何精度方面，DSM 的 RMSE 从 6.76m 压缩至 **5.20m**（↓23.1%）（Table 3）。这一双重提升验证了核心洞察：注入几何启发的正则化可直接弥补卫星-街道视角差距导致的几何约束缺失。

![[assets/figures/papers/paper_list_l60_https_openreview_net_forum_id_E7JzkZCofa/figures/006_Table_1.jpg]]
*Table 1: Quantitative results of street-view comparison on the test set of VIGOR-OOD. Bold indicates the best results, while underlined text represents the second-best results*

![[assets/figures/papers/paper_list_l60_https_openreview_net_forum_id_E7JzkZCofa/figures/009_Table_3.jpg]]
*Table 3: Quantitative comparison for predicted DSM*

与基于扩散的 2D 生成方法（**ControlNet** (Zhang et al., 2023)、**ControlS2S** (Ze et al., 2025)）相比，Sat3DGen 在 FID 和 KID 上同样保持显著优势，且额外提供显式 3D 表示。几何着色方法（**Sat2Scene** (Li et al., 2024b)、**Sat2City** (Hua et al., 2025)）仅生成建筑外壳和道路，缺失非建筑语义，而 Sat3DGen 完整保留了卫星图像中的语义和外观信息（Figure 1）。

### 消融实验：各模块的因果作用

Table 2 的消融实验揭示了四个关键组件的差异化贡献：

![[assets/figures/papers/paper_list_l60_https_openreview_net_forum_id_E7JzkZCofa/figures/007_Table_2.jpg]]
*Table 2: Ablation results on the VIGOR-OOD test set. The first row removes all proposed key components*

**重力密度变化损失**（Gravity-based Density Variation Loss）对真实感影响最大。移除该损失后，FID 从 21.6 恶化至 25.9（↑19.9%），KID 从 0.016 升至 0.020。该损失通过惩罚密度随高度增加（$\mathcal{L}_{\mathrm{grav}}$，ε=1.0），有效抑制了漂浮伪影和不规则屋顶结构（Figure 5）。Table 4 进一步表明，ε 过小（如 0.01）会过度惩罚合理的空洞结构，导致 FID 回升至 24.6。

**卫星视图深度正则化**（Satellite-view Depth Regularization）和**空间令牌填充**（Spatial Token Padding）对几何精度更关键。单独移除深度损失使几何 RMSE 从 5.23m 升至 5.75m（↑9.9%）；移除空间令牌则使 RMSE 升至 5.64m（↑7.8%）。深度正则化利用 Depth Anything v2 的单目相对深度先验，为卫星视图提供了尺度-平移不变的几何监督（Eq. 10）；空间令牌在令牌网格四周各填充 N=2 个零令牌，扩展了有效场景边界，缓解了卫星图像覆盖范围与全景视场之间的足迹不匹配问题（Figure 8 深度图对比）。

**透视视图训练**（Perspective View Training）在基础模型上叠加后，使所有指标进一步提升至最优（FID 19.2, RMSE 5.20）。该策略从全景图中投影生成透视视图监督，增加了有效视角覆盖，使模型能更好地处理街道级透视视角下的几何和外观（Figure 4 多视角视频）。

### 定性分析与3D资产质量

Figure 3 的定性对比显示，Sat2Density++ 生成的三平面表示存在严重扭曲——屋顶不规则、立面出现伪影、边界区域几何塌缩。Sat3DGen 通过重力约束和深度正则化，产生了结构更规整、高度更合理的 3D 表示。Figure 6 的 3D 资产比较进一步表明，Sat3DGen 在建筑轮廓完整性、树木和车辆等非建筑元素的几何一致性方面显著优于基线。

![[assets/figures/papers/paper_list_l60_https_openreview_net_forum_id_E7JzkZCofa/figures/005_Figure_3.jpg]]
*Figure 3: The comparison of generation 3D between Sat2Density++ (Qian et al., 2026) and our model on the VIGOR-OOD test set (Zhu et al., 2021)*

![[assets/figures/papers/paper_list_l60_https_openreview_net_forum_id_E7JzkZCofa/figures/010_Figure_6.jpg]]
*Figure 6: Comparison of generation 3D assets between Sat2Density++(Qian et al., 2026) and Ours*

Figure 7 将完整模型与移除所有几何组件的“Canonical image-to-3D”基线对比，直观展示了四个组件的累积效应：基线产生大量漂浮伪影和边界扭曲，而完整模型恢复了清晰的几何结构。

### 泛化能力与扩展应用

Sat3DGen 展现出良好的泛化性。Figure 10 展示了滑动窗口推理模式，可处理大规模卫星图像并生成连续网格。Figure 11 演示了从语义地图到 3D 的流水线：先通过图像转换模型将语义地图转为卫星地图，再输入 Sat3DGen 生成 3D 资产，扩展了应用场景。值得注意的是，模型在训练时未使用任何度量深度数据，但仍能从单张卫星图像预测出合理的 DSM（Figure 9），证明几何先验的注入使模型习得了隐式的单目深度推理能力。

![[assets/figures/papers/paper_list_l60_https_openreview_net_forum_id_E7JzkZCofa/figures/013_Figure_9.jpg]]
*Figure 9: Visual results of our model generated DSM (metric depth) from the monocular satellite image, which is rendered from the satellite view, with no metric depth data for training*

![[assets/figures/papers/paper_list_l60_https_openreview_net_forum_id_E7JzkZCofa/figures/014_Figure_10.jpg]]
*Figure 10: Given a large satellite image, our model can generate mesh with sliding window inference mode*

![[assets/figures/papers/paper_list_l60_https_openreview_net_forum_id_E7JzkZCofa/figures/015_Figure_11.jpg]]
*Figure 11: Given a colored semantic map, our model can generate 3D mesh through a pipeline that first converts the semantic map to a satellite map and then transforms the satellite map into 3D assets*

### 失败模式与局限性

尽管整体性能显著提升，Sat3DGen 仍存在以下失效场景：

1. **非典型建筑**：训练数据中罕见的建筑形态（如圆形穹顶、异形结构）会导致几何重建退化，缺乏显式 3D 形状监督使模型难以泛化到分布外结构。
2. **地形假设**：模型假设局部平地面，在显著地形起伏（如丘陵、坡地）的场景中，建筑基底和道路高度可能出现系统性偏差。
3. **相机姿态近似**：卫星图像被视为理想正交投影，全景图忽略滚动角，这些简化在精确几何评估中可能引入误差。
4. **评估局限性**：VIGOR 数据集仅提供单视图全景真值，无法测量多视图一致性或时间闪烁度，实际部署中的 3D 稳定性需额外验证。

### 公平性说明

所有方法均在相同的 VIGOR-OOD 测试集上评估，测试城市 Seattle 与训练城市完全不重叠，保证了跨域外推的公平性。对于 2D 生成方法（ControlNet 等），直接采用其论文报告的最佳结果，避免重新训练引入的不公平偏差。对比时使用统一的全局光照特征输入，排除了光照变化对生成质量评估的干扰。

### 补充图表

![[assets/figures/papers/paper_list_l60_https_openreview_net_forum_id_E7JzkZCofa/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative ablation on key modules*

![[assets/figures/papers/paper_list_l60_https_openreview_net_forum_id_E7JzkZCofa/figures/012_Figure_8.jpg]]
*Figure 8: Comparison of predicted satellite-view height map*

![[assets/figures/papers/paper_list_l60_https_openreview_net_forum_id_E7JzkZCofa/figures/002_Figure.jpg]]
*Figure: Large Area Mesh Gen. High-quality Renderable3D generation from satellite image support multiple applications…*

## 方法谱系与知识库定位

### 任务定位与基线谱系

Sat3DGen解决的是**单张卫星图像到街道级3D场景的跨视角生成**问题，其核心挑战在于极端的卫星-街道视角差距和稀疏监督信号导致的前馈几何约束不足。该任务处于卫星遥感、神经渲染与图像到3D生成的交叉地带，现有方法可沿两条技术路线进行定位：

**代理式方法（Proxy-based）** 将3D场景表示为显式的代理几何体（如建筑外壳、道路平面），然后进行纹理映射。早期工作**Sat2Density**（Qian et al., 2023）和其增强版**Sat2Density++**（Qian et al., 2026）是该路线的代表，能够保留卫星图像的语义和外观信息，但受限于代理几何的粗糙性，产生严重的几何扭曲（如屋顶不规则、立面伪影）。**几何着色方法（Geometric Shell）** 如**Sat2Scene**（Li et al., 2024b）和**Sat2City**（Hua et al., 2025）仅生成建筑外壳和道路平面，完全丢失非建筑语义（树木、车辆等），无法生成完整的3D场景。

**基于扩散的图像生成方法** 如**ControlNet**（Zhang et al., 2023）和**ControlS2S**（Ze et al., 2025）将卫星图像作为条件生成街景图像，但仅输出2D视图，不具备3D一致性，无法支持自由视角渲染或3D资产导出。

Sat3DGen选择了一条不同的技术路径：**前馈图像到3D框架**，以三平面NeRF作为基线表示（Canonical Image-to-3D），通过集成几何启发的正则化组件来弥补几何约束的缺失。这一设计使其同时具备语义完整性（保留非建筑元素）、3D一致性（可导出网格和自由视角渲染）和几何精度（RMSE 5.20m），在方法属性上填补了代理式方法和纯2D生成方法之间的空白。

### 核心技术贡献与因果机制

Sat3DGen的性能提升可归因于四个关键设计槽位的改变，每个组件针对特定的几何失效模式：

1. **重力对齐密度损失（Gravity-based Density Variation Loss）**：惩罚密度随高度增加的现象，直接抑制漂浮伪影和屋顶不规则。消融实验表明，移除该损失导致FID从21.6恶化至25.9，是**真实感最关键的组件**。超参数ε=1.0取得最佳平衡，过小的ε会错误惩罚合理的空洞结构（如拱门、天桥）。

2. **卫星视图深度正则化（Satellite-view Depth Regularization）**：利用Depth Anything v2的尺度-平移不变伪深度作为显式几何先验，约束卫星视角下的场景深度分布。消融显示移除该损失使几何RMSE从5.23升至5.75，是**几何精度最关键的组件之一**。

3. **空间令牌填充（Spatial Token Padding）**：在令牌网格四周各添加N=2个零令牌，有效扩展场景边界以容纳周边内容，解决边界扭曲和足迹不匹配问题。移除该模块使RMSE升至5.64，同样是几何精度的关键贡献者。

4. **透视视图训练（Perspective View Training）**：从全景图投影透视视图作为额外监督，增加有效视角覆盖。该设计使所有指标进一步提升（FID 19.2, RMSE 5.20），实现了最佳综合性能。

这些组件的因果机制可以概括为：**显式几何先验注入（重力约束+深度先验）弥补了稀疏监督下的几何约束缺失，空间容量扩展解决了边界不匹配，而透视训练增加了视角覆盖以提升泛化性**。

### 适用边界与局限

尽管Sat3DGen在VIGOR-OOD基准上取得了显著提升，其适用边界受限于以下因素：

- **相机模型假设**：卫星图像被视为理想正交投影，全景图忽略滚动角，缺乏精确的相机姿态数据。这限制了在需要精确多视图几何一致性的应用场景中的性能。
- **建筑多样性**：模型难以处理训练数据中罕见的非典型建筑（如异形屋顶、复杂立面结构），因为缺乏显式的3D真实形状监督。
- **地形假设**：模型假设局部平地面，不建模显著地形变化（如丘陵、坡地），难以推断复杂地形场景。
- **评估局限**：现有评估指标受限于VIGOR数据集，无法测量多视图一致性或时间闪烁度，可能高估实际应用中的视觉质量。

### 开放问题与未来方向

1. **精确相机姿态获取**：如何获取或预测全景图的精确内外参，以进一步提升几何精度并支持更精细的多视图监督？
2. **多模态数据融合**：如何融入地形图、建筑轮廓等多模态数据，以处理地形起伏和复杂城市场景？
3. **可扩展评估协议**：如何设计可扩展的评估协议，以测量生成3D的多视图几何一致性和时间稳定性？
4. **非典型结构建模**：如何引入显式3D先验或合成数据增强，以提升对罕见建筑类型的泛化能力？

### 知识库定位

Sat3DGen在知识库中的定位可概括为：**首个将几何启发的正则化系统性地集成到前馈图像到3D框架中，以解决卫星到街道跨视角3D生成问题的工作**。其核心洞察——通过重力约束、单目深度先验和空间填充来弥补几何约束缺失——为跨视角3D生成提供了可复用的设计范式。该方法不依赖额外的图像质量模块或后处理步骤，在保持端到端可训练性的同时大幅提升了几何精度和真实感，为后续研究在遥感3D重建、城市数字孪生等方向提供了新的基线。

## 原文 PDF

![[paperPDFs/ICLR_2026/Sat3DGen_Comprehensive_Street_Level_3D_Scene_Generation_from_Single_Satellite_Im_d04b4ece93f7.pdf]]