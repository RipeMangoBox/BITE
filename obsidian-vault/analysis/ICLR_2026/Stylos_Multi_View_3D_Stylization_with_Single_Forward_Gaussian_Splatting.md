---
title: "Stylos: Multi-View 3D Stylization with Single-Forward Gaussian Splatting"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Stylos_Multi_View_3D_Stylization_with_Single_Forward_Gaussian_Splatting_449d413115ca.pdf
project_link: "https://www.wikiart.org/"
code_link: "https://github.com/HanzhouLiu/Stylos"
aliases:
- Stylos
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过共享Transformer骨干将几何推理（自注意力）与风格注入（交叉注意力）分离；利用3D体素风格损失在融合后的体积空间强制视图一致性。
primary_logic: 在预训练的几何骨干（VGGT）之上，用交叉注意力沿内容特征注入风格信息，同时保留自注意力进行几何推理；并在3D体素空间中匹配特征统计量，从而在单次前向传播中实现几何保真、视图一致的风格化3D高斯场景。
claims:
- Global CrossBlock在重建质量和视觉保真度上显著优于Frame和Hybrid变体。
- 3D体素风格损失在艺术质量（ArtScore 9.15）和视图一致性（短距LPIPS 0.047）上均优于图像级和场景级损失。
- Stylos在Tanks & Temples四个场景上所有短距和长距一致性指标（LPIPS、RMSE）均排名第一。
- Stylos在保持最佳或次佳艺术质量的同时，推理速度（~0.05 s / scene）远超所有逐场景优化方法。
---

# Stylos: Multi-View 3D Stylization with Single-Forward Gaussian Splatting

> [!tip] 核心洞察
> 在预训练的几何骨干（VGGT）之上，用交叉注意力沿内容特征注入风格信息，同时保留自注意力进行几何推理；并在3D体素空间中匹配特征统计量，从而在单次前向传播中实现几何保真、视图一致的风格化3D高斯场景。

| 字段 | 内容 |
|------|------|
| 中文题名 | Stylos：基于单次前向高斯泼溅的多视角三维风格化 |
| 英文题名 | Stylos: Multi-View 3D Stylization with Single-Forward Gaussian Splatting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Ir0HMkRpYb) · [Code](https://github.com/HanzhouLiu/Stylos) · [Project](https://www.wikiart.org/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Stylos |
| Dataset | Tanks & Temples |

> [!tip] 效果简介
> - Tanks & Temples (Train scene) 上，Short-range LPIPS↓ 0.030 (Stylos) vs 0.033 (StyleGaussian) (↓9.1%)。
> - Tanks & Temples (Truck scene) 上，Short-range RMSE↓ 0.021 (Stylos) vs 0.034 (StyleGaussian) (↓38.2%)。
> - Tanks & Temples (all scenes avg.) 上，Long-range LPIPS↓ (relative) Stylos ranks 1st across all scenes vs Next best: StyleGaussian / G-Style (improves consistency by clear margin)。

## 概要

将任意艺术风格迁移至三维场景是视觉计算中的长期挑战。现有方法大多依赖**逐场景优化**或**预标定相机参数**，难以实现零样本泛化，且推理耗时通常在数十秒至分钟级，严重制约实时应用。Stylos 的核心主张是：**通过在预训练几何骨干之上解耦几何推理与风格注入，并引入三维体素风格损失，可以在单次前向传播中生成几何保真、多视图一致的风格化三维高斯场景**。

方法层面的关键突破在于两处设计。其一，**CrossBlock 模块**在 VGGT 的 Transformer 块中插入交叉注意力层，形成“自注意力（几何推理）→ 交叉注意力（风格注入）→ MLP”的级联结构，使风格信息沿内容特征流动而不破坏几何推理能力。其二，**三维体素风格损失**将多视图特征反投影至共享的三维网格，在体素空间对齐生成特征与风格特征的均值与标准差，强制跨视图一致性，克服了传统图像级 AdaIN 损失独立匹配各帧统计量导致的闪烁与撕裂。

实验证据从三个维度支撑上述论断。在**视图一致性**上，Stylos 在 Tanks & Temples 全部四个场景的短距和长距 LPIPS、RMSE 指标上均排名第一（如 Train 场景短距 LPIPS 0.030，较 StyleGaussian 的 0.033 降低 9.1%）。在**艺术质量**上，3D 体素风格损失使 ArtScore 从图像级损失的 4.78 跃升至 9.15，同时保持极低的短距 LPIPS（0.047），且生成纹理更干净、几何感更强。在**推理效率**上，Stylos 单场景风格化仅需约 0.05 秒，比逐场景优化方法快数个数量级，同时维持最佳或次佳的艺术质量（如 Train 场景 ArtScore 9.50，仅次于 G-Style 的 9.60）。

在方法谱系中，Stylos 处于**单次前向三维风格化**与**三维高斯泼溅（3DGS）** 的交汇点。与逐场景优化的 3DGS 风格化方法（如 **StyleGaussian** [Liu et al., 2024]、**G-Style** [Kovacs et al., 2024]、**StylizedGS** [Zhang et al., 2025]）相比，Stylos 通过前馈网络消除了场景级训练的需求；与同样采用单次前向的 **Styl3R**（Wang et al., 2025b）相比，Stylos 通过三维体素损失显式优化多视图一致性，而非仅依赖二维损失。其几何骨干继承自 **VGGT**（Wang et al., 2025a）的交替注意力设计，风格聚合器的交叉注意力机制则借鉴了图像风格化中内容-风格解耦的思想，但将其拓展至三维体素空间。

Stylos 仍存在三类典型失效模式：对高频杂乱结构（浓密叶片、线状元素）的重建和风格化质量下降；强烈全局光照变化或极端调色板下出现过饱和或外观线索丢失；输入视图数显著增加时几何骨干不稳定导致风格化效果退化。这些局限性指向若干开放问题：如何增强对复杂几何结构的鲁棒性，视图数增加导致性能退化的根本机制，以及对素描、立体主义等极简风格类型的泛化能力。



三维场景风格化旨在将参考艺术图像的视觉特征（如笔触、色彩调性、纹理模式）迁移到三维内容表示上，生成可从任意新视角渲染的风格化结果。这一任务在数字艺术创作、虚拟现实内容生成和电影预可视化等领域具有广泛应用前景。近年来，以三维高斯泼溅（3D Gaussian Splatting, 3DGS）为代表的显式辐射场表示，凭借其高保真重建和实时渲染能力，已成为三维风格化的主流载体。

然而，**现有3DGS风格化方法普遍面临一个核心瓶颈：逐场景优化的刚性依赖**。以 **StyleGaussian**（Liu et al., 2024）、**G-Style**（Kovacs et al., 2024）、**StylizedGS**（Zhang et al., 2025）和 **SGSST**（Galerne et al., 2025）为代表的代表性工作，均要求对每个内容场景和每个风格参考分别执行独立的优化过程——通常需要数分钟甚至更长的训练时间。这种"一场景一训练"的范式严重制约了风格化流程的吞吐量，使其难以满足实时交互式应用的需求。

另一条技术路线试图实现单次前向传播的风格化，如 **Styl3R**（Wang et al., 2025b），通过前馈网络直接预测风格化结果。但这类方法在设计上并未专门优化多视图一致性，导致在不同视角下渲染的风格化结果可能出现纹理漂移、颜色不一致等伪影。**几何保真与风格一致之间的张力**，构成了该领域长期存在的结构性矛盾——图像级风格损失（如AdaIN）独立匹配各帧统计量，天然缺乏跨视图的约束机制，而逐场景优化方法虽然通过迭代缓解了这一问题，却以牺牲效率为代价。

Stylos正是在这一背景下提出的。其核心动机在于**打破"效率-一致性"的折衷**：通过将几何推理与风格注入解耦到共享Transformer骨干的不同路径中，并在三维体素空间施加跨视图一致的特征统计约束，实现在单次前向传播中同时达成实时推理速度与视图一致的风格化质量。



## 核心方法与创新机理

Stylos的核心创新在于将3D风格化从“逐场景优化”的范式转变为**单次前向、零样本泛化**的生成式框架，其关键在于两个相互协同的机制：**解耦的几何-风格注入架构**和**3D体素级风格损失**。

### 1. 解耦的几何推理与风格注入：CrossBlock

现有3D风格化方法通常将风格迁移视为后处理或端到端优化问题，缺乏对几何结构与外观风格的显式解耦。Stylos在预训练的几何骨干（VGGT）之上，引入**CrossBlock**模块，将Transformer块的标准结构（自注意力→MLP）改造为**自注意力→交叉注意力→MLP**的三阶段流水线：

- **自注意力保留几何推理**：内容令牌通过帧内和全局自注意力，维持多视图几何结构的一致性推理能力。
- **交叉注意力注入风格信息**：以DINO编码的风格特征作为Key-Value，内容令牌作为Query，通过交叉注意力将风格外观条件化地注入内容表示，而不干扰几何推理路径。

这种设计实现了**几何路径与风格路径的共享骨干但功能分离**：几何头从骨干特征解码高斯的位置、尺度、旋转等几何参数，风格头从交叉注意力输出预测球谐系数作为颜色参数。消融实验（Table 1）证实，**Global CrossBlock**（拼接所有视图令牌后统一与风格交互）在重建PSNR上达到20.57，显著优于Frame变体的19.72，且视觉边界更清晰（Figure 2），验证了全局融合对多视图一致性的关键作用。

### 2. 3D体素风格损失：从图像级匹配到体积空间统计对齐

传统图像级AdaIN风格损失独立匹配各帧特征统计量，缺乏跨视图约束，容易导致纹理闪烁和几何不一致。Stylos提出**3D体素级风格损失**，将多视图特征反投影到共享的3D体素网格中，在体积空间对齐生成特征与风格特征的均值与标准差：

$$\mathcal{L}_{\mathrm{sty}}^{\mathrm{3D}} = \frac{1}{B} \sum_{b=1}^{B} \sum_{l=1}^{5} \alpha_l \Big( \| \mu(\mathcal{G}_b^l) - \mu(\mathcal{S}_b^l) \|_2^2 + \| \sigma(\mathcal{G}_b^l) - \sigma(\mathcal{S}_b^l) \|_2^2 \Big)$$

该损失在体素空间显式编码几何结构，强制风格统计量在3D空间中保持一致。消融实验（Table 2）显示，3D体素损失将ArtScore从图像级损失的4.78提升至9.15，同时保持低短距LPIPS（0.047），且生成纹理更干净、几何感更强（Figure 3）。

### 3. 两阶段训练策略

为保护几何预训练知识不被风格训练破坏，Stylos采用**两阶段训练**：
- **Stage 1 几何预训练**：冻结VGGT教师模型，通过重建损失和蒸馏损失训练几何骨干。
- **Stage 2 风格微调**：冻结几何模块，仅更新风格聚合器和颜色头，总损失为重建损失、3D体素风格损失、内容损失、CLIP损失和总变分正则项的加权组合。

这一策略确保风格化过程不损害几何重建质量，是实现零样本泛化的关键工程支撑。



Stylos 定义了一个条件映射，将多视图内容图像与一张风格参考图联合映射为风格化 3D 高斯场景与对应的相机参数：

$$f_{\theta} : (\{ I_i \}_{i=1}^N, S) \mapsto \big( G, \{ g_i \}_{i=1}^N \big)$$

其中 $\{I_i\}_{i=1}^N$ 为 $N$ 个多视图输入，$S$ 为风格参考图像，$G$ 为风格化 3D 高斯原语集合，$g_i$ 为各视图的相机内参与外参。整个流程在单次前向传播中完成，无需逐场景优化或后处理，推理时间约 0.05 秒/场景，比现有逐场景优化方法快数个数量级（Table 4）。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_Ir0HMkRpYb/figures/014_Table_5.jpg]]
*Table 5: Following StyleID (Chung et al., 2024), we additionally report sylization quality metrics, FID, LPIPS, LPIPS-gray, CFSD, color matching loss (HistoGAN loos), as supplementary to Table 4*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_Ir0HMkRpYb/figures/015_Table_6.jpg]]
*Table 6: Following StyleID (Chung et al., 2024), we additionally report sylization quality metrics, FID, LPIPS, LPIPS-gray, CFSD, color matching loss (HistoGAN loos), as supplementary to Table 4*

### 核心设计理念

Stylos 的核心洞察在于**将几何推理与风格注入在共享 Transformer 骨干中解耦**：内容路径保留自注意力以进行多视图几何推理（深度、相机参数估计），风格路径通过交叉注意力将风格信息注入内容特征，从而在保持几何保真度的同时实现风格迁移。这一设计通过两个关键机制实现：

1. **CrossBlock 模块**：在 VGGT 的交替注意力骨干中，将标准 Transformer Block 替换为 CrossBlock——在自注意力与 MLP 之间插入交叉注意力层，使风格令牌（由 DINO 编码器提取）能够条件化内容令牌的外观表达。
2. **3D 体素风格损失**：将多视图特征反投影并融合到 3D 体素网格中，在体素空间匹配生成特征与风格特征的均值与标准差，显式编码几何结构并强制跨视图风格一致性。

### Pipeline 模块组成

系统由五个核心模块串联构成（Figure 1）：

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_Ir0HMkRpYb/figures/001_Figure_1.jpg]]
*Figure 1: Architecture overview. Given multi-view content inputs and a style reference, Stylos enables instant 3D stylization without scene-specific training or post-optimization. Its core Cross-Block module facilitates style injection by integrating a cross-attention layer between self-attention and MLP. The proposed 3D style loss matches voxelized 3D features with 2D style statistics*

| 模块 | 功能 | 关键机制 |
|------|------|----------|
| **Geometric Backbone (VGGT)** | 处理多视图输入，提取几何特征并预测深度与相机参数 | 交替帧内自注意力与全局自注意力，捕获视图内结构与跨视图一致性 |
| **Style Aggregator (CrossBlocks)** | 接收 DINO 编码的风格特征，通过交叉注意力注入内容令牌 | Global CrossBlock 将所有视图令牌拼接后统一与风格令牌交互，促进多视图一致性 |
| **Geometry Head** | 从几何骨干特征解码高斯几何参数 | 输出位置 $\mu_m$、尺度 $s_m$、旋转 $r_m$、不透明度 $\alpha_m$ |
| **Style Head** | 从风格聚合输出预测球谐系数 | 定义风格相关的颜色参数 $c_m$ |
| **Gaussian Adapter + Voxelization** | 融合几何与风格输出为统一高斯基元，并通过置信度加权体素化减少冗余点 | 借鉴 AnySplat 的体素化策略 |

### 训练策略

Stylos 采用**两阶段训练策略**以保证结构感知的风格化：

- **Stage 1（几何预训练）**：冻结 VGGT 教师模型提供位姿与深度监督，仅训练几何相关模块，目标为重建损失与蒸馏损失的组合 $\mathcal{L}_{\mathrm{stage1}} = \mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{distill}} \mathcal{L}_{\mathrm{distill}}$。
- **Stage 2（风格微调）**：冻结几何模块，仅更新 Style Aggregator 和 Style Head，引入 3D 体素风格损失、内容损失、CLIP 损失与总变分正则项：

$$\mathcal{L}_{\mathrm{stage2}} = \mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{style}} \mathcal{L}_{\mathrm{style}}^{\mathrm{3D}} + \lambda_{\mathrm{cnt}} \mathcal{L}_{\mathrm{content}} + \lambda_{\mathrm{clip}} \mathcal{L}_{\mathrm{clip}} + \lambda_{\mathrm{tv}} \mathcal{L}_{\mathrm{TV}}$$

各损失权重分别为 $\lambda_{\mathrm{style}}=1.0$、$\lambda_{\mathrm{cnt}}=0.1$、$\lambda_{\mathrm{clip}}=1.0$、$\lambda_{\mathrm{tv}}=10.0$。

### 关键消融证据

消融实验（Table 1, Figure 2）表明，Global CrossBlock 在重建质量上显著优于 Frame 和 Hybrid 变体——在 Pizza 场景上 PSNR 达到 20.57（Frame 为 19.72），且纹理边界更清晰。3D 体素风格损失（Table 2, Figure 3）在 ArtScore 上达到 9.15，远超图像级损失的 4.78，同时保持低短距 LPIPS（0.047），生成的纹理更干净且几何感更强。



Stylos 的核心设计围绕一个共享的 Transformer 骨干展开，通过两条路径分别处理几何推理与风格注入，最终在单次前向传播中输出风格化的 3D 高斯场景。其关键模块包括条件映射定义、风格聚合器（CrossBlock）以及 3D 体素风格损失。

### 条件映射定义

Stylos 将任务形式化为一个条件映射：

$$f_{\theta} : (\{ I_i \}_{i=1}^N, S) \mapsto \big( G, \{ g_i \}_{i=1}^N \big)$$

其中，$\{ I_i \}_{i=1}^N$ 表示 $N$ 个内容视图，$S$ 为单张风格参考图像。函数 $f_{\theta}$ 输出一组风格化的 3D 高斯基元 $G$ 以及各视图对应的相机参数 $g_i$（包括内外参）。该映射不依赖任何逐场景优化或预计算相机参数，是实现零样本实时风格化的基础。

### 几何骨干与风格聚合器

几何骨干沿用 **VGGT**（Wang et al., 2025a）的交替注意力设计，在帧内自注意力和全局自注意力之间交替，以捕捉单帧结构并建立跨视图几何一致性。在此基础上，Stylos 引入风格聚合器，其核心是将标准 Transformer 块替换为 **CrossBlock** 模块。

CrossBlock 在自注意力与 MLP 之间插入交叉注意力操作，实现风格信息的有条件注入。具体地，对于第 $b$ 个 batch 中的第 $v$ 个视图，帧级交叉注意力定义为：

$$\widetilde{\mathcal{Q}}_{b,v} = \mathrm{CrossBlock}(\mathcal{Q}_{b,v}, \mathcal{KV}_b)$$

其中 $\mathcal{Q}_{b,v}$ 为该视图的内容令牌，$\mathcal{KV}_b$ 为来自 DINO 编码器的风格令牌（键值对）。该操作在保留各视图独立几何结构的前提下注入风格信息。

为强化多视图一致性，Stylos 进一步采用全局交叉注意力，将所有视图令牌拼接后统一与风格令牌交互：

$$\widetilde{\mathcal{Q}}_{b}^{\mathrm{global}} = \mathrm{CrossBlock}(\mathcal{Q}_{b}^{\mathrm{global}}, \mathcal{KV}_b)$$

消融实验（Table 1）表明，Global CrossBlock 在重建质量上显著优于 Frame 和 Hybrid 变体——在 Pizza 场景上，Global 的 PSNR 达到 20.57，而 Frame 仅为 19.72，且视觉上边界更清晰（Figure 2）。

### 3D 体素风格损失

传统图像级 AdaIN 风格损失独立匹配各帧统计量，缺乏对底层 3D 几何的感知，容易导致视图间风格不一致。Stylos 提出 **3D 体素级风格损失**，将多视图特征反投影到共享的 3D 体素网格中，在体素空间对齐生成特征与风格特征的统计量：

$$\mathcal{L}_{\mathrm{sty}}^{\mathrm{3D}} = \frac{1}{B} \sum_{b=1}^{B} \sum_{l=1}^{5} \alpha_l \Big( \| \mu(\mathcal{G}_b^l) - \mu(\mathcal{S}_b^l) \|_2^2 + \| \sigma(\mathcal{G}_b^l) - \sigma(\mathcal{S}_b^l) \|_2^2 \Big)$$

其中，$B$ 为 batch 大小，$l$ 索引 5 层特征，$\alpha_l$ 为各层权重。$\mathcal{G}_b^l$ 和 $\mathcal{S}_b^l$ 分别表示生成特征和风格特征在体素化后的第 $l$ 层表示，$\mu(\cdot)$ 和 $\sigma(\cdot)$ 为均值和标准差。通过在体素空间匹配二阶统计量，该损失显式编码了几何结构，强制跨视图和跨 3D 结构的风格一致性。

消融实验（Table 2）证实了该设计的有效性：3D 体素风格损失在艺术质量（ArtScore 9.15）和短距一致性（LPIPS 0.047）上均优于图像级损失（ArtScore 4.78, LPIPS 0.048），且生成的纹理更干净、几何感更强（Figure 3）。

### 两阶段训练策略

Stylos 采用两阶段训练以保证结构感知的风格化：

- **Stage 1 几何预训练**：冻结 VGGT 教师模型提供位姿和深度监督，目标为重建损失与蒸馏损失的组合：

  $$\mathcal{L}_{\mathrm{stage1}} = \mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{distill}} \mathcal{L}_{\mathrm{distill}}$$

- **Stage 2 风格微调**：冻结几何模块，仅更新风格聚合器和颜色头。总损失为：

  $$\mathcal{L}_{\mathrm{stage2}} = \mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{style}} \mathcal{L}_{\mathrm{style}}^{\mathrm{3D}} + \lambda_{\mathrm{cnt}} \mathcal{L}_{\mathrm{content}} + \lambda_{\mathrm{clip}} \mathcal{L}_{\mathrm{clip}} + \lambda_{\mathrm{tv}} \mathcal{L}_{\mathrm{TV}}$$

  其中权重设置为 $\lambda_{\mathrm{style}}=1.0$、$\lambda_{\mathrm{cnt}}=0.1$、$\lambda_{\mathrm{clip}}=1.0$、$\lambda_{\mathrm{tv}}=10.0$，分别对应 3D 风格损失、内容损失、CLIP 损失和总变分正则项。



## 实验与关键发现

### 消融实验：风格注入机制设计

Stylos的核心创新之一在于如何将风格信息注入几何推理骨干。论文系统消融了三种CrossBlock设计：**Frame**（逐帧独立交叉注意力）、**Global**（拼接所有视图令牌后统一交叉注意力）和**Hybrid**（两者结合）。

**表1**（Table 1）展示了在CO3D数据集上的重建指标对比。以Pizza场景为例，Global CrossBlock取得了PSNR 20.57，显著优于Frame的19.72，LPIPS也从0.3405降至0.3110。**图2**（Figure 2）的定性结果进一步印证：Global设计生成的披萨顶料和饼皮边缘更加清晰，而Frame变体则出现模糊和边界不明确的问题。

**关键结论**：全局交叉注意力机制通过让所有视图的内容令牌与风格令牌统一交互，有效促进了多视图间的一致性，同时保留了更强的几何细节。这与Stylos“自注意力保留几何推理，交叉注意力注入风格”的设计理念一致——Global CrossBlock在全局令牌拼接后执行交叉注意力，使得风格信息能够感知完整的3D场景上下文，而非局限于单帧。

---

### 消融实验：3D体素风格损失

风格损失的设计直接影响风格化质量和视图一致性。论文对比了三种损失：**图像级AdaIN损失**（独立匹配各帧统计量）、**场景级损失**（在场景全局特征上匹配）、以及提出的**3D体素风格损失**（将多视图特征反投影到3D网格后在体素空间对齐均值与标准差）。

**表2**（Table 2）的结果揭示了关键权衡：
- **图像级损失**：ArtScore仅4.78，短距LPIPS为0.048，表明虽然视图一致性尚可，但艺术质量极差。
- **3D体素损失**：ArtScore跃升至9.15，短距LPIPS保持0.047，在艺术质量和几何一致性之间取得了最佳平衡。

**图3**（Figure 3）的定性对比显示，在甜甜圈、滑板和披萨等未见场景上，3D损失生成的纹理更干净，且传达出更强的3D几何感——例如桌面纹理更完整地覆盖表面，同时保留了场景的接缝等结构细节。

**机制解析**：3D体素风格损失的核心优势在于其操作空间。通过将多视图特征反投影并融合到统一的体素网格中（公式5），该损失在匹配特征统计量时天然编码了3D几何信息。这迫使风格化过程不仅要在单视图上匹配风格，更要在3D空间中保持一致的风格表达，从而解决了图像级损失中“各帧独立风格化导致视图间闪烁”的根本问题。

---

### 视图数量对风格化质量的影响

**图4**（Figure 4）展示了batch中视图数量变化对风格化质量的影响。当视图数从标准设置增加到64时，Lighthouse场景的建筑边缘出现明显artifacts。论文指出这与训练设置有关——模型在训练时最多使用24个视图，超出此范围的视图数导致VGGT几何骨干的重建不稳定，进而影响风格化质量。这一发现揭示了当前方法的一个扩展性瓶颈：几何骨干对视图数量的泛化能力限制了整体系统的鲁棒性。

---

### 主结果：视图一致性对比

**表3**（Table 3）在Tanks & Temples数据集的四个场景（Train、Truck、M60、Garden）上系统评估了短距和长距一致性。Stylos在所有场景的所有一致性指标（短距/长距LPIPS和RMSE）上均排名第一：

- **Train场景**：短距LPIPS 0.030，RMSE 0.026；长距LPIPS 0.051，RMSE 0.056。
- **Truck场景**：短距LPIPS 0.028，RMSE 0.021，相比次优方法StyleGaussian（短距RMSE 0.034）降低38.2%。
- **M60场景**：短距LPIPS 0.035，RMSE 0.024。
- **Garden场景**：短距LPIPS 0.047，RMSE 0.044。

对比基线包括**StyleGaussian**（Liu et al., 2024）、**G-Style**（Kovacs et al., 2024）、**StylizedGS**（Zhang et al., 2025）和**SGSST**（Galerne et al., 2025）等逐场景优化方法。Stylos作为单次前向方法，在一致性上全面超越这些需要逐场景训练的对手，验证了3D体素风格损失在强制视图一致性上的有效性。

---

### 主结果：艺术质量与效率

**表4**（Table 4）报告了ArtScore、ArtFID和风格化时间的对比。Stylos在四个场景上取得了最佳或次佳的艺术质量：
- Train场景ArtScore 9.50（仅次于G-Style的9.60，差距在1%以内）
- Truck场景ArtScore 9.70
- M60场景ArtScore 9.37
- Garden场景ArtScore 9.34

**效率优势**是Stylos最突出的亮点：风格化时间仅约0.05秒/场景，而逐场景优化方法（StyleGaussian、G-Style等）需要数秒到数分钟。这一数量级的效率提升源于Stylos的单次前向设计——无需任何测试时优化或预计算相机参数，直接从输入视图和风格参考一步生成风格化的3D高斯场景。

**补充指标**：**表5**和**表6**（Table 5/6）按照StyleID（Chung et al., 2024）的评估协议，额外报告了FID、LPIPS-gray、CFSD和颜色匹配损失等指标，进一步验证了Stylos在风格化质量上的竞争力。

---

### 失败模式分析

论文识别了三类典型失败案例：
1. **几何重建不准确**：当输入场景包含浓密树叶、细枝或线状结构时，VGGT骨干的重建质量下降，导致风格化结果出现几何缺失或错误颜色。
2. **颜色溢出**：生成风格参考中未出现的颜色，尤其在强烈全局光照变化或极端调色板下，可能导致过饱和。
3. **过度平滑**：引入模糊或过度平滑的风格色块，丢失细微的外观线索。

这些失败模式与视图数量扩展实验中的发现一致——几何骨干的稳定性是整个系统的关键瓶颈。当基础重建不准确时，后续的风格注入和3D体素损失无法完全补偿几何误差。

### 补充图表

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_Ir0HMkRpYb/figures/002_Table_1.jpg]]
*Table 1: Ablation on the style-content fusion module, comparing Frame, Global and hybrid Cross-Block designs. The first frame of each content scene is used as the pseudo style reference. Reconstruction quality is evaluated with PSNR↑, SSIM↑, and LPIPS↓ on the CO3D dataset*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_Ir0HMkRpYb/figures/003_Figure_2.jpg]]
*Figure 2: CO3D pizza scene comparing different CrossBlock designs*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_Ir0HMkRpYb/figures/004_Table_2.jpg]]
*Table 2: Comparison of consistency and artistic quality among different style loss designs on CO3D. The frame stride is set to 3, and 15 held-out scenes are randomly selected for evaluation*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_Ir0HMkRpYb/figures/006_Figure.jpg]]
*Figure: Image Loss Scene Loss 3D Style Loss*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_Ir0HMkRpYb/figures/008_Figure_4.jpg]]
*Figure 4: Effect of varying # views / batch on the Lighthouse scene from Tanks and Temples*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_Ir0HMkRpYb/figures/009_Table_3.jpg]]
*Table 3: For consistency comparisons, we report short-range and long-range LPIPS↓ and RMSE↓ on the four scenes from the Tanks & Temples dataset. We clarify experiment details in A.4. In the following tables, the best results are highlighted and the second best results are underlined. Each stylization method category is visualized with a distinct color. The proposed Stylos demonstrates improved short-range and long-range consistency scores across the four scenes*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_Ir0HMkRpYb/figures/010_Table_4.jpg]]
*Table 4: Stylization quality, as measured by ArtScore and ArtFID (abbreviated as Score and FID respectively), and stylization time comparisons with recent 3D stylization models. Stylos achieves consistently favorable metric scores across the four scenes. Additionally, we follow StyleID (Chung et al., 2024) and calculate additional metrics as reported in A.4 Table 5 and Table 6*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_Ir0HMkRpYb/figures/011_Figure_5.jpg]]
*Figure 5: Visual comparisons between Stylos and recent 3D stylization approaches. Stylos successfully transfers diverse artistic styles to the scenes while preserving fine structural details*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_Ir0HMkRpYb/figures/007_Figure_3.jpg]]
*Figure 3: Comparison of style losses on unseen donut, skateboard, and pizza scenes from the CO3D dataset. Both scene and 3D style losses yield cleaner stylized textures compared to image-level matching, while the 3D loss further conveys a stronger sense of 3D geometry. We encourage readers to Appendix Fig. 8-10 for more visual comparisons under varing scenes and styles*



## 定位与知识库关联

### 1. 在3D风格化方法谱系中的位置

Stylos 位于**零样本、单次前向3D高斯风格化**这一新兴节点，其核心突破在于将几何推理与风格注入解耦到共享Transformer骨干的两个路径中，从而在无需逐场景优化或预计算相机参数的前提下实现实时风格化。

**与逐场景优化方法的对比。** 传统3D风格化方法普遍依赖逐场景训练或后优化，代表性工作包括 **StyleGaussian**（Liu et al., 2024）、**G-Style**（Kovacs et al., 2024）、**StylizedGS**（Zhang et al., 2025）和 **SGSST**（Galerne et al., 2025）。这些方法在给定新场景时需重新训练或微调，推理时间通常在数十秒到数分钟量级。Stylos 将风格化时间压缩至约0.05秒/场景（Table 4），速度提升数个数量级，同时在艺术质量上保持最佳或次佳水平（ArtScore 9.15–9.70）。这一效率优势源于其将风格化建模为条件映射函数 $f_{\theta} : (\{ I_i \}_{i=1}^N, S) \mapsto (G, \{ g_i \}_{i=1}^N)$，而非逐场景的优化问题。

**与单次前向方法的对比。** **Styl3R**（Wang et al., 2025b）同样采用单次前向策略，但其设计未专门优化多视图一致性。Stylos 在此基础上引入两个关键改进：(1) 通过 Global CrossBlock 在全局令牌空间中统一注入风格信息，强制跨视图外观一致性；(2) 提出3D体素风格损失，在融合后的体积空间匹配特征统计量，使风格化过程显式感知3D几何结构。Table 3 显示，Stylos 在 Tanks & Temples 四个场景的所有短距和长距一致性指标（LPIPS、RMSE）上均排名第一，验证了这一设计对视图一致性的实质提升。

### 2. 技术继承与创新边界

**几何骨干的继承。** Stylos 的几何骨干直接继承自 **VGGT**（Wang et al., 2025a）的交替注意力设计——帧内自注意力捕获单视图结构，全局自注意力建模跨视图关系。这一选择使得 Stylos 能够利用预训练的强大多视图几何推理能力，为风格化提供准确的深度和相机参数估计。两阶段训练策略进一步保护了这一继承：Stage 1 冻结 VGGT 教师进行几何蒸馏，Stage 2 冻结几何模块仅更新风格相关参数，确保几何推理能力不被风格微调破坏。

**风格注入机制的创新。** 核心创新在于将 VGGT 的标准 Transformer Block 替换为 CrossBlock：在自注意力（保留几何推理）和 MLP 之间插入交叉注意力层，使内容令牌能够与 DINO 编码的风格令牌交互。这一设计实现了**几何推理与风格注入的解耦**——自注意力路径保持对场景结构的推理能力，交叉注意力路径负责风格信息的传递。Table 1 和 Figure 2 的消融实验证实，Global CrossBlock（拼接所有视图令牌后统一与风格交互）在重建质量（Pizza 场景 PSNR 20.57 vs Frame 19.72）和视觉细节保真度上显著优于逐帧（Frame）和混合（Hybrid）变体。

**3D体素风格损失的贡献。** 传统图像级 AdaIN 风格损失独立匹配各帧统计量，缺乏对3D结构的感知。Stylos 提出的3D体素风格损失（Eq. 5）将多视图特征反投影到3D网格中，在体素空间对齐生成特征与风格特征的均值和标准差：
$$\mathcal{L}_{\mathrm{sty}}^{\mathrm{3D}} = \frac{1}{B} \sum_{b=1}^{B} \sum_{l=1}^{5} \alpha_l \Big( \| \mu(\mathcal{G}_b^l) - \mu(\mathcal{S}_b^l) \|_2^2 + \| \sigma(\mathcal{G}_b^l) - \sigma(\mathcal{S}_b^l) \|_2^2 \Big)$$
Table 2 显示，该损失将 ArtScore 从图像级损失的4.78提升至9.15，同时短距 LPIPS 保持在0.047的竞争水平。Figure 3 的定性结果显示，3D损失生成的纹理更干净、几何感更强（如桌面纹理覆盖更完整、接缝保留更好）。

### 3. 适用边界与失效模式

**已知局限。** 论文明确指出的失效场景包括三类：

1. **高频/杂乱结构退化**：浓密树叶、细枝、线状元素等场景的重建和风格化质量下降，可能源于 VGGT 骨干对高频细节的几何推理能力有限。
2. **极端光照与调色板敏感**：强烈全局光照变化或极端调色板可能导致过饱和或丢失细微外观线索，这与风格损失的统计匹配机制在分布外风格的泛化能力有关。
3. **视图数增加导致性能下降**：当 batch 中视图数超过32时，边缘出现 artifacts（Figure 4，灯塔场景），这与训练设置（最多24视图）不匹配有关。Figure 7（附录）展示了推理时间和 GPU 内存随视图数的扩展规律，但未揭示性能下降的根本机制。

**公平性考量。** 在一致性比较中，StylizedGS 在多个测试风格上产生纯色、几何细节丢失的失败案例，这些案例被排除在一致性计算之外。所有方法均在相同 NVIDIA GH200 GPU 上评估，推理时间包括必要的逐场景训练和渲染时间。

### 4. 开放问题

1. **高频结构处理**：如何有效处理浓密植被、线状等高频复杂结构？可能的改进方向包括增强几何骨干对细粒度细节的感知能力，或引入专门的高频损失项。
2. **视图扩展性**：输入视图数增加导致性能下降的根本机制是什么？能否通过增强几何骨干的训练视图多样性或适配训练策略来缓解？
3. **风格泛化鲁棒性**：对完全不同的风格类型（如素描、立体主义、极简色彩）的泛化鲁棒性如何？当前评估主要基于 WikiArt 数据集的艺术风格，极端抽象风格的测试尚不充分。
4. **动态场景扩展**：是否可以将该方法扩展到动态场景或视频输入，同时保持一致性和效率？这需要在时序维度上扩展当前的3D体素风格损失和 CrossBlock 设计。



## 原文 PDF

![[paperPDFs/ICLR_2026/Stylos_Multi_View_3D_Stylization_with_Single_Forward_Gaussian_Splatting_449d413115ca.pdf]]
