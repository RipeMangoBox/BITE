---
title: Unsupervised Multi-Scale Segmentation of 3D Subcellular World with Stable Diffusion Foundation Model
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Unsupervised_Multi_Scale_Segmentation_of_3D_Subcellular_World_with_Stable_Diffusion_Foundation_Model.pdf
project_link: null
code_link: null
aliases:
- UMSCESSD
- UMSS3SWSDFM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 引入基于Stable Diffusion基础模型全部注意力层的特征提取与启发式特征聚合策略，通过谱聚类优化特征向量、多样性分数自适应阈值，将无监督特征转化为高质量分割掩码。
primary_logic: 利用Stable Diffusion UNet所有注意力层的query-key亲和矩阵，通过联合优化多个亲和矩阵的谱聚类目标获得正交特征向量，再以多样性分数迭代合并、相邻切片一致性校正等启发式规则构建聚集特征图，最终用高斯自适应阈值生成多尺度伪标签，驱动有监督模型训练，实现无需人工标注的跨尺度、跨域分割。
claims:
- 无监督膜分割Dice系数仅比有监督方法低约4.6%，且远超其他无监督方法（SAM, FreeSOLO, CutLer）。
- 无监督大分子定位F1分数超过使用100个真实坐标训练的有监督DeepETPicker（0.43 vs 0.35），并远超CrYOLO所有设置。
- 无监督方法能够自动分割肌动蛋白丝，而基于人工标注训练的有监督方法无法识别此类结构，展示出生物发现潜力。
- VPP S. Pombe cellular cryo-ET dataset (10 tomograms) 上 Dice coefficient (膜分割) = 0.309 (Our Method)
---

# Unsupervised Multi-Scale Segmentation of 3D Subcellular World with Stable Diffusion Foundation Model

> [!tip] 核心洞察
> 利用Stable Diffusion UNet所有注意力层的query-key亲和矩阵，通过联合优化多个亲和矩阵的谱聚类目标获得正交特征向量，再以多样性分数迭代合并、相邻切片一致性校正等启发式规则构建聚集特征图，最终用高斯自适应阈值生成多尺度伪标签，驱动有监督模型训练，实现无需人工标注的跨尺度、跨域分割。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于Stable Diffusion基础模型的无监督多尺度三维亚细胞分割 |
| 英文题名 | Unsupervised Multi-Scale Segmentation of 3D Subcellular World with Stable Diffusion Foundation Model |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Uddin_Unsupervised_Multi-Scale_Segmentation_of_3D_Subcellular_World_with_Stable_Diffusion_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | Unsupervised Multi-Scale Cryo-ET Segmentation via Stable Diffusion (无监督多尺度分割流程) |
| Dataset | VPP S. Pombe cellular cryo-ET dataset |

> [!tip] 效果简介
> - VPP S. Pombe cellular cryo-ET dataset (10 tomograms) 上，Dice coefficient (膜分割) 0.309 (Our Method) vs 0.048 (SAM), 0.003 (FreeSOLO), 0.003 (CutLer), 0.324 (Supervised UNet) (比无监督SAM/FreeSOLO/CutLer提升>0.26；仅比有监督UNet低0.015（~4.6%）)；F1 score (大分子定位) 0.43 (Our Method) vs 0.25 (CrYOLO n=100), 0.31 (CrYOLO n=500), 0.35 (DeepETPicker n=100), 0.57 (Deep... (比CrYOLO(n=500)高38.7%；比DeepETPicker(n=100)高22.86%；低于DeepETPicker(n=500) 24.6%)。

## 概要

**问题瓶颈**：冷冻电镜断层成像（cryo-ET）能以近原子分辨率解析细胞原位三维结构，但其亚细胞结构呈现高度多尺度异质性，且高质量人工标注极度匮乏。现有有监督分割方法依赖大量标注数据，跨实验域泛化能力差，难以应对密集、拥挤的细胞环境。

**核心方法定位**：本文提出一种全新范式——利用在自然图像上预训练的 **Stable Diffusion** 基础模型（Rombach et al., CVPR 2022）的内在视觉表征通路，结合启发式特征聚合策略，实现完全无人工标注的三维多尺度亚细胞分割。该方法无需对基础模型进行任何微调或训练，仅需用户从少量代表性断层图中选取信息丰富的二维切片，即可生成高质量伪标签，进而驱动有监督模型完成全数据集分割与定位。

**关键调控机制**：方法的核心因果杠杆在于：(1) 提取 Stable Diffusion 条件 UNet **全部16层注意力层**的 query-key 亲和矩阵，而非仅依赖末层或传统视觉特征；(2) 通过联合优化多层亲和矩阵的谱聚类目标获得正交特征向量，并以**多样性分数**迭代合并生成聚集特征图；(3) 采用高斯自适应阈值与预训练 CellPose 模型，将无监督特征分解为膜掩码与大分子坐标。

**主要结果**：
- **膜分割**：在 VPP S. pombe 细胞 cryo-ET 数据集上，无监督膜分割 Dice 系数达 **0.309**，仅比有监督 UNet（0.324）低约 4.6%，远超通用分割模型 SAM（0.048）、FreeSOLO（0.003）和 CutLer（0.003）。
- **大分子定位**：无监督定位 F1 分数达 **0.43**，超过使用 100 个真实坐标训练的弱监督 DeepETPicker（0.35）和所有 CrYOLO 设置（最高 0.31），仅低于使用 500 个真实坐标的 DeepETPicker（0.57）。
- **生物发现潜力**：在额外数据集上，无监督方法能自动分割出肌动蛋白丝等结构，而基于人工标注训练的有监督方法完全无法识别此类目标，展示了超越标注偏见的跨域泛化能力。

冷冻电镜断层成像（cryo-ET）能够以纳米级分辨率在近天然状态下解析细胞内分子结构，为原位结构生物学提供了独特窗口。然而，从三维断层图中分割和定位亚细胞结构面临根本性挑战：**标注数据严重匮乏**。cryo-ET图像信噪比极低、结构拥挤且形态高度异质，人工标注一个断层图需耗费数周专家时间，且标注结果受主观判断影响，跨实验条件、跨细胞类型的泛化能力差。这一标注瓶颈直接制约了有监督深度学习方法在该领域的应用——现有有监督方法在训练域内表现尚可，但一旦面对新的成像条件或细胞环境，性能急剧下降。

现有无监督分割方法主要面向自然图像设计，在cryo-ET数据上几乎完全失效。以**SAM**（Kirillov et al., ICCV 2023）、**FreeSOLO**（Wang et al., CVPR 2022）、**CutLer**（Wang et al., CVPR 2023）为代表的通用或自然图像无监督分割方法，在膜分割任务上的Dice系数仅为0.048、0.003和0.003（Table 1），几乎不具备实用价值。其根本原因在于：这些方法依赖的视觉特征（如ResNet/ViT的最后一层注意力或分类特征）与cryo-ET图像中微弱、多尺度的结构信号不匹配，无法捕捉从数十纳米的大分子复合物到微米级膜系统的跨尺度信息。

本文的核心动机在于：**绕过人工标注，直接利用视觉基础模型的内在表征能力实现cryo-ET图像的多尺度无监督分割**。关键洞察是，Stable Diffusion的条件UNet在自然图像预训练中习得的全部注意力层，其query-key亲和矩阵蕴含了丰富的多尺度结构信息——从低层的局部纹理到高层的语义分组。通过联合优化这些亲和矩阵的谱聚类目标，并辅以启发式特征聚合策略，可以将这些隐式知识转化为高质量的伪标签，进而驱动有监督模型完成全数据集的分割与定位。这一思路不仅避免了标注成本，更重要的是打破了有监督方法对特定实验域的依赖，为跨域、跨尺度的亚细胞结构分析开辟了新路径。

## 核心方法与创新机理

### 问题瓶颈：冷冻电镜断层图像的标注困境

冷冻电镜断层成像（cryo-ET）能够在近原生状态下以纳米级分辨率解析细胞内部三维结构，但其图像具有极低信噪比、高异质性和多尺度特性（从数纳米的大分子到数百纳米的细胞膜），使得人工标注极为困难且耗时。现有有监督分割方法（如 **UNet** (Ronneberger et al., MICCAI 2015)、**DeepETPicker** (Liu et al., Nature Communications 2024)）依赖大量精确标注，跨实验域泛化能力差——当面对标注数据中未出现的结构（如肌动蛋白丝）时，有监督模型完全失效。通用无监督分割方法（如 **SAM** (Kirillov et al., ICCV 2023)、**FreeSOLO** (Wang et al., CVPR 2022)、**CutLer** (Wang et al., CVPR 2023)）则因cryo-ET图像与自然图像的巨大域差异而表现极差，膜分割Dice系数仅0.003–0.048。这一瓶颈的本质在于：**cryo-ET领域标注数据的严重匮乏与亚细胞结构的多尺度高异质性之间的矛盾**。

### 因果杠杆：从基础模型注意力到无监督特征

本文的核心创新在于改变了对标注数据的依赖路径——不再试图从标注中学习任务相关特征，而是**从预训练视觉基础模型的内部表征中直接提取可分离的视觉线索**。具体而言，方法利用Stable Diffusion条件UNet全部16层注意力的query-key亲和矩阵，通过“谱聚类优化特征向量 + 启发式特征聚合”的策略，将无监督特征转化为高质量分割掩码。这一路径选择的关键优势在于：Stable Diffusion虽在自然图像上预训练，但其多层次注意力机制捕获的通用视觉基元（边缘、纹理、对比度变化）恰好与cryo-ET图像中膜边界和大分子颗粒的强度特征形成跨域迁移。

### 关键创新点（Changed Slots）

以下从五个关键维度剖析本方法相对于baseline的核心改变：

#### 1. 特征提取层：从末层到全层注意力

现有无监督分割方法通常仅利用ViT或ResNet的最后一层特征，或仅使用自注意力图的最后一层（如CutLer的MaskCut）。本方法**首次使用Stable Diffusion条件UNet的全部16层注意力层**提取query-key亲和矩阵（Section 3.3）。其因果机制在于：浅层注意力捕获细粒度边缘和纹理信息（对应大分子颗粒边界），深层注意力捕获全局结构信息（对应细胞膜轮廓），全层融合才能覆盖跨尺度的亚细胞结构。消融证据虽未在论文中明确报告，但Table 1中无监督SAM（仅用ViT特征）Dice仅0.048，间接支持了全层注意力的必要性。

#### 2. 特征聚合策略：从相似度裁剪到谱聚类优化

传统方法（如FreeSOLO、CutLer）通过相似度阈值裁剪亲和图来获得分割掩码，这种方式对噪声敏感且难以处理密集重叠对象。本方法引入三步启发式聚合策略：

- **谱聚类特征向量优化**：构建联合优化目标（Eqn. 4），在所有注意力层的亲和矩阵上最小化期望归一化亲和度偏差与正交正则化项的加权和，通过梯度下降直接学习正交特征向量 $X$。这避免了传统谱聚类对每个亲和矩阵单独求解特征值问题的不一致性。
- **多样性分数迭代合并**：定义 $\mathrm{DiversityScore}(I) = \mathrm{std}(\pmb{\sigma})$，其中 $\pmb{\sigma}$ 为图像局部块标准差的集合，用于量化特征图像的纹理丰富度。从最高多样性分数的特征向量开始，迭代合并低分特征向量，直至形成信息密集的聚集特征图。
- **z轴相邻切片一致性校正**：利用cryo-ET数据的三维连续性，对相邻切片的特征图进行一致性约束，减少单张切片的噪声伪影。

这一策略的核心洞察是：**通过谱聚类获得正交特征向量，本质上是将亲和矩阵的谱空间作为特征选择空间，而多样性分数则作为选择“信息量最大”特征向量的启发式代理指标**。

#### 3. 分割阈值方法：从固定阈值到高斯自适应阈值

cryo-ET图像存在严重的局部强度不均匀性，固定阈值无法适应不同区域的对比度变化。本方法对聚集特征图进行高斯平滑后，采用**高斯自适应阈值**（$b=15, C=3$），根据局部邻域的像素分布动态确定分割阈值。这一改变直接提升了膜边界和大分子颗粒的分割完整性，尤其对低对比度区域的弱信号目标。

#### 4. 多尺度掩码分解：引入CellPose预训练模型

由于无监督特征提取本身不区分对象尺度，初始分割掩码同时包含膜和大分子。本方法创新性地引入**预训练CellPose模型**进行掩码分解（Section 3.5），利用CellPose在细胞分割任务中学到的形态学先验，自动将连通域按尺度和形状分离为膜掩码和大分子掩码。这一设计将“无监督特征提取”与“有监督形态学分解”解耦，避免了在cryo-ET域上重新训练形态学分类器的需求。

#### 5. 伪标签利用方式：从自训练到专用模型训练

传统无监督分割方法通常采用自训练范式（如FreeSOLO），即用同一模型生成伪标签并迭代优化。本方法将无监督阶段生成的膜掩码和大分子坐标作为**伪真实标签**，分别训练专用的有监督模型：**UNet用于膜分割，DeepETPicker用于大分子定位**（Section 3.5）。这一改变的因果优势在于：(1) 专用模型架构针对各自任务优化，分割精度更高；(2) 训练后的模型可泛化至同一断层图的所有切片，实现全数据集分割；(3) 避免自训练中错误累积的恶性循环。

### 创新有效性证据

**Table 1** 显示，本方法膜分割Overall Dice达0.309，仅比有监督UNet（0.324）低约4.6%，但远超SAM（0.048）、FreeSOLO（0.003）和CutLer（0.003）。**Table 2** 显示，大分子定位Overall F1达0.43，超过使用100个真实坐标训练的DeepETPicker（0.35）22.86%，也超过使用500个坐标训练的CrYOLO（0.31）38.7%。更关键的是，在额外数据集上（Figure 4），无监督方法自动分割出肌动蛋白丝等有监督方法完全无法识别的结构，展示了**超越人工标注局限性的生物发现潜力**。

### 局限与待验证问题

尽管创新显著，方法仍存在以下局限：(1) 特征向量优化耗时较长（每层切片7-8分钟），尚未实现多GPU并行加速；(2) 分割主干仅基于强度变化，无法直接区分单个细胞器（如线粒体vs内质网），需结合下游形态学分析；(3) 多样性分数的块大小和步长参数为启发式设定，缺乏自适应学习机制；(4) 方法仅在部分cryo-ET数据集上验证，对其他体积成像模态（如FIB-SEM）的泛化能力需进一步评估。

本文提出一套完整的**无监督多尺度冷冻电镜断层图像（cryo-ET）分割流程**，其核心设计目标是在完全无需人工标注的条件下，从拥挤的三维细胞环境中同时分割膜结构与大分子复合物。流程的输入为用户从少量代表性断层图中选取的信息丰富切片集合，输出为全数据集的高质量膜分割掩码与大分子定位坐标。

### 设计动机与关键瓶颈

冷冻电镜断层图像面临**标注数据极度匮乏**的困境：亚细胞结构尺度跨越两个数量级（从几纳米的大分子到数百纳米的细胞器膜），形态高度异质，且信噪比极低。有监督方法（如UNet、DeepETPicker）依赖大量高质量人工标注，标注成本高昂且跨域泛化能力差——在一个数据集上训练的模型往往在另一个数据集上完全失效。因此，无监督路径成为突破标注瓶颈的关键。

### 核心因果机制

本方法的**因果旋钮**在于：利用Stable Diffusion基础模型全部注意力层提取的query-key亲和矩阵作为跨尺度视觉特征，通过谱聚类优化与启发式特征聚合策略，将这些无监督特征转化为高质量分割掩码。具体而言：

1. **特征提取层级的扩展**：不同于FreeSOLO、CutLer等方法仅使用最后一层注意力或ResNet/ViT特征，本方法提取Stable Diffusion条件UNet全部16层注意力的query-key亲和矩阵，捕获从纹理细节到语义结构的全尺度信息。
2. **特征聚合的谱聚类框架**：通过联合优化多层亲和矩阵的谱聚类目标，获得正交特征向量，再以多样性分数迭代合并、相邻切片一致性校正等启发式规则构建聚集特征图。
3. **自适应阈值与掩码分解**：采用高斯自适应阈值生成多尺度二值掩码，再利用预训练CellPose将多尺度掩码分解为膜掩码与大分子掩码。
4. **伪标签驱动有监督训练**：以无监督掩码为伪标签训练专用有监督模型（UNet用于膜分割，DeepETPicker用于大分子定位），实现全断层图的高效推理。

### 流程模块与数据流

整个pipeline由六个核心模块串联构成，数据流如图1所示：

**模块1：预处理与分块**
对用户选取的切片集合 $\mathbb{S} = \{ I^{(i)} \in \mathcal{R}^{H \times W}, i \in [K] \}$ 依次进行对比度拉伸与CLAHE增强，随后将每张预处理图像 $I^{(i)}$ 分割为四个等大无重叠的四等份 $I_{4_1}^{(i)}, I_{4_2}^{(i)}, I_{4_3}^{(i)}, I_{4_4}^{(i)}$，构成四等份图像集 $\mathbb{S}_4$。四等分操作既降低了单张图像的特征优化计算量，又保留了足够的空间上下文。

**模块2：Stable Diffusion特征提取**
将 $\mathbb{S}_4$ 中的每张四等份图像输入Stable Diffusion的条件UNet模块，提取所有注意力层的query $Q_l$ 与key $K_l$，计算层 $l$ 中数据点 $i$ 与 $j$ 之间的亲和矩阵：
$$A_l(i,j) = \exp\left(\frac{Q_l(i) K_l(j)^T}{\sqrt{d}}\right)$$
这一步骤完全无需对Stable Diffusion进行任何训练或微调，直接复用其在自然图像上预训练的视觉通路。

**模块3：特征向量优化与聚合**
在获得多层亲和矩阵集合 $\mathcal{A}$ 后，求解如下优化问题以获得正交特征向量 $X$：
$$\min_X \mathbb{E}_{A\in\mathcal{A}} \left| g(X)^\top D_A^{-1} A g(X) - 1 \right| + \| X^\top X - I \|_F$$
其中 $g(X)$ 为参数化特征映射，$D_A$ 为度矩阵，$I$ 为单位矩阵。该目标同时最大化跨层期望归一化亲和度并约束特征向量正交性。优化得到的特征向量通过**多样性分数**（Diversity Score）进行迭代筛选与合并——多样性分数定义为图像局部块标准差的标准差：
$$\mathrm{DiversityScore}(I) = \mathrm{std}(\pmb{\sigma}), \quad \pmb{\sigma} = \{ \mathrm{std}(I_{ij}) \mid I_{ij} \in \mathcal{P} \}$$
其中 $\mathcal{P}$ 为以步长 $s$ 滑动提取的 $p \times p$ 重叠图像块集合。最后通过z轴相邻切片一致性校正，生成聚集特征图。

**模块4：自适应阈值分割**
对聚集特征图进行高斯平滑后，采用高斯自适应阈值（参数 $b=15, C=3$）生成多尺度二值掩码，该掩码同时包含膜结构与大分子信号。

**模块5：CellPose掩码分解**
利用预训练的CellPose模型，将多尺度二值掩码分解为**膜掩码**（大面积连续区域）与**大分子掩码**（小面积离散区域），从大分子掩码中可直接提取颗粒中心坐标。

**模块6：伪标签有监督训练**
以分解后的膜掩码为伪标签，从头训练一个UNet模型（损失函数结合Dice Loss与交叉熵损失），用于全断层图的膜分割推理；以大分子坐标伪标签训练弱监督DeepETPicker，实现全数据集的大分子定位。这种“无监督生成伪标签→训练有监督模型”的策略，既保留了无监督方法的标注独立性，又获得了有监督模型的高效推理能力。

### 输入输出规范

- **输入**：用户从少量代表性断层图中手动选取的信息丰富切片（$K$ 张 $H \times W$ 灰度图像），无需任何人工标注。
- **输出**：全断层图的膜分割二值掩码（通过训练后的UNet推理）以及大分子三维坐标列表（通过训练后的DeepETPicker推理）。
- **中间产物**：四等份图像集 $\mathbb{S}_4$、多层亲和矩阵 $\mathcal{A}$、优化特征向量 $X$、聚集特征图、多尺度二值掩码、CellPose分解后的膜掩码与大分子掩码。

### 补充图表

![[assets/figures/papers/paper_list_l2621_https_openaccess_thecvf_com_content_CVPR2026_html_Uddin_Unsupervised_Mul/figures/001_Figure_1.jpg]]
*Figure 1: Our unsupervised segmentation pipeline with visual examples. (a) Selecting information-rich slabs from a tomogram and preprocessing the slabs. (b) Split the slabs into quarters. (c) Optimize eigenvector features of the quarter images from Stable Diffusion foundation model (d) Create feature image for the quarter images using the eigenvectors (e) Obtaining multiscale unsupervised segmentation mask from the feature image, splitting the multiscale mask to membrane and macromolecule masks (f) train a supervised UNet with predicted unsupervised membrane masks as ground truth (g) Use the trained UNet to infer membrane masks for other slabs in the tomogram. (h) Train a DeepETPicker [9] model with...*

本方法的核心在于将 Stable Diffusion 基础模型的内在视觉表征转化为高质量的无监督分割掩码。其技术路线围绕三个关键模块展开：基于全部注意力层的亲和矩阵提取、联合多层亲和矩阵的特征向量优化，以及基于启发式规则的聚集特征图构建。

### 亲和矩阵提取

与传统方法仅使用最后一层注意力或 ResNet/ViT 特征不同（如 FreeSOLO、CutLer），本方法从 Stable Diffusion 条件 UNet 的全部 16 层注意力中提取表征。对于第 $l$ 层注意力，给定 query 矩阵 $Q_l$ 和 key 矩阵 $K_l$，数据点 $i$ 与 $j$ 之间的亲和度定义为经过 softmax 缩放的 query-key 点积：

$$A_l(i,j) = \exp\left(\frac{Q_l(i) K_l(j)^T}{\sqrt{d}}\right)$$

其中 $d$ 为缩放因子。该亲和矩阵 $A_l$ 刻画了第 $l$ 层特征空间中任意两个空间位置之间的语义关联强度，是后续谱聚类分析的基础。

### 特征向量优化

为将多层亲和矩阵整合为统一的特征表示，本方法构建了一个联合优化问题。对于单层亲和矩阵 $A$ 及其度矩阵 $D$，谱聚类的广义特征值问题为：

$$(D - A) X = \lambda D X$$

其解 $X$ 的列向量即为该层的特征向量。为同时利用所有注意力层的信息，本方法将上述问题推广为在所有层亲和矩阵集合 $\mathcal{A}$ 上的期望最大化问题：

$$\max_X \mathbb{E}_{A\in\mathcal{A}} \left[ g(X)^\top D_A^{-1} A g(X) \right] \quad \mathrm{s.t.} \quad X^T X = \mathbf{I}$$

其中 $g(\cdot)$ 为参数化特征映射函数，正交约束 $X^T X = \mathbf{I}$ 确保特征向量的独立性。该约束优化问题进一步转化为可微损失函数，通过梯度下降直接优化参数化特征图 $X$：

$$\min_X \mathbb{E}_{A\in\mathcal{A}} \left| g(X)^\top D_A^{-1} A g(X) - 1 \right| + \| X^\top X - I \|_F$$

损失函数的第一项最大化归一化亲和度，第二项为 Frobenius 范数形式的正交正则化项。该优化过程产生一组正交特征向量，作为后续特征聚合的输入。

### 启发式特征聚合与自适应阈值

优化得到的正交特征向量需进一步聚合为单通道聚集特征图。本方法引入**多样性分数**作为特征选择的启发式准则。对于一幅特征图像 $I$，多样性分数定义为局部块标准差的全局标准差：

$$\mathrm{DiversityScore}(I) = \mathrm{std}(\pmb{\sigma}), \quad \pmb{\sigma} = \{ \mathrm{std}(I_{ij}) \mid I_{ij} \in \mathcal{P} \}$$

其中 $\mathcal{P}$ 为以步长 $s$ 滑动提取的 $p \times p$ 重叠图像块集合：

$$\mathcal{P} = \{ I_{ij} \in \mathbb{R}^{p\times p} \mid i = 0, s, 2s, \dots, H-p,\; j = 0, s, 2s, \dots, W-p \}$$

多样性分数衡量特征图像的纹理丰富程度。聚合过程以多样性分数最高的特征向量为基图，迭代合并其他特征向量以逐步增强聚集特征图的纹理信息，同时引入相邻切片沿 z 轴的一致性校正，最终对聚集特征图施加高斯平滑与**高斯自适应阈值**（参数 $b=15$，$C=3$），生成多尺度二值分割掩码。

> **注意**：多样性分数的块大小 $p$ 和重叠步长 $s$ 的具体取值在现有材料中未明确给出，需查阅原文补充。

## 实验与关键发现

### 1. 实验设置与基准

本工作采用 **VPP S. Pombe 细胞冷冻电镜断层图像数据集**（共10个断层图）进行主要评估。该数据集包含专家标注的膜分割掩码与大分子定位坐标，是冷冻电镜领域公认的基准。评估分为两个子任务：

- **膜分割**：以 Dice 系数衡量二值掩码质量。
- **大分子定位**：以 F1 分数衡量检测精度（IoU ≥ 0.3 视为正确检测）。

对比方法涵盖三类：
1. **有监督膜分割基线**：**Supervised UNet**（Ronneberger et al., MICCAI 2015），使用专家标注的膜掩码训练。
2. **有监督/弱监督大分子定位基线**：**CrYOLO**（Wagner & Raunser, Communications Biology 2020）与 **DeepETPicker**（Liu et al., Nature Communications 2024），分别使用不同数量的真实坐标训练（n=100 或 n=500）。
3. **无监督分割对比方法**：**SAM**（Kirillov et al., ICCV 2023）、**FreeSOLO**（Wang et al., CVPR 2022）、**CutLer**（Wang et al., CVPR 2023），均为自然图像域的无监督/通用分割方法，直接应用于冷冻电镜数据。

本方法仅在少量代表性切片上进行无监督伪标签生成，随后训练专用的有监督模型（UNet 用于膜分割，DeepETPicker 用于大分子定位），实现对全数据集的推断。

---

### 2. 膜分割结果

**Table 1** 汇总了膜分割的 Dice 系数对比。

| 方法 | 训练方式 | 整体 Dice |
|------|----------|-----------|
| SAM | 无监督 | 0.048 |
| FreeSOLO | 无监督 | 0.003 |
| CutLer | 无监督 | 0.003 |
| **Our Method** | **无监督** | **0.309** |
| Supervised UNet | 有监督 | 0.324 |

**核心发现**：
- 本方法以 **0.309 的 Dice 系数**大幅超越所有无监督对比方法（SAM 仅 0.048，FreeSOLO 和 CutLer 几乎完全失效，均仅 0.003），提升幅度超过 **0.26**。
- 与使用完整人工标注训练的有监督 UNet（0.324）相比，差距仅 **0.015**（约 4.6%），表明无监督伪标签质量已接近专家标注水平。
- SAM、FreeSOLO 和 CutLer 在冷冻电镜图像上的严重失效，揭示了自然图像域的无监督方法无法直接迁移至高噪声、低对比度的体积成像数据，而本方法通过 Stable Diffusion 基础模型的全部注意力层特征提取，成功捕获了亚细胞结构的跨尺度视觉线索。

**定性分析**（Figure 2）进一步证实：在训练断层图 TS_0008 和另一独立断层图上，本方法生成的膜掩码与专家标注高度一致，能准确勾勒膜边界，而有监督 UNet 在某些区域存在过分割或漏检。

---

### 3. 大分子定位结果

**Table 2** 汇总了大分子定位的 F1 分数对比。

| 方法 | 训练坐标数 | 整体 F1 |
|------|-----------|---------|
| CrYOLO | n=100 | 0.25 |
| CrYOLO | n=500 | 0.31 |
| DeepETPicker | n=100 | 0.35 |
| DeepETPicker | n=500 | 0.57 |
| **Our Method** | **0（无监督）** | **0.43** |

**核心发现**：
- 本方法在**零人工标注**条件下取得 **0.43 的 F1 分数**，显著优于使用 100 个真实坐标训练的 DeepETPicker（0.35，提升 **22.86%**），以及使用 500 个真实坐标训练的 CrYOLO（0.31，提升 **38.7%**）。
- 仅当 DeepETPicker 使用 500 个真实坐标时（0.57），才超越本方法（差距约 24.6%），但此时已投入大量标注成本。本方法的无监督伪标签驱动训练，以零标注代价逼近中等规模标注下的有监督性能。
- 这一结果验证了核心机制的有效性：Stable Diffusion 的 query-key 亲和矩阵能捕获大分子与背景的细微纹理差异，结合多样性分数迭代合并与自适应阈值，可生成高精度的大分子定位伪标签。

**定性分析**（Figure 3）显示：在训练断层图 TS_0008 和另一独立断层图上，本方法（黄色框）检测到的大分子位置与真实标注（绿色框）高度重合，且在某些密集区域，本方法的检测结果比有监督 DeepETPicker（青色框）更接近真实分布，漏检和误检更少。

---

### 4. 跨域泛化与生物发现

**Figure 4** 展示了本方法在额外冷冻电镜数据集上的分割结果。关键发现包括：

- **肌动蛋白丝的自动分割**：在未提供任何标注的额外数据集上，本方法成功分割出肌动蛋白丝，而有监督方法（基于原始数据集标注训练）完全无法识别此类结构。原文明确指出：“our unsupervised approach can automatically segment actin filaments ... supervised methods ... cannot detect these actin filaments”。这表明无监督方法避免了人工标注的域偏见，具备**跨域生物结构发现**的潜力。
- 膜和大分子的分割在额外数据集上同样保持合理质量，进一步验证了方法的泛化能力。

---

### 5. 失败模式与局限性分析

尽管整体性能优异，实验和设计层面仍存在以下局限：

1. **计算效率瓶颈**：特征向量优化（Eqn. 4）在单 GPU 上每层切片需 **7-8 分钟**，处理一个完整断层图的时间成本较高，尚无法满足实时或高通量处理需求。这是当前方法从研究走向实用的主要障碍。

2. **细胞器实例区分能力缺失**：当前分割主干仅依赖强度变化生成二值掩码，无法直接区分单个细胞器（如线粒体、内质网、高尔基体）。虽然 CellPose 的掩码分解步骤可分离膜与大分子，但膜掩码内部的不同细胞器仍粘连在一起，需结合下游形态学分析才能实现实例级区分。

3. **验证范围有限**：方法仅在 VPP S. Pombe 数据集和少量额外数据集上验证，更多细胞类型、成像条件（如不同 defocus、剂量）和物种下的稳定性仍需系统评估。

4. **启发式参数敏感性**：多样性分数的块大小、重叠步长，以及高斯自适应阈值的参数（b=15, C=3）均为手工设定，在不同数据分布下可能需要重新调参，缺乏自适应机制。

---

### 6. 消融与机制验证（基于方法设计推断）

论文未提供独立的消融实验表格，但从方法设计可推断以下组件的贡献：

- **全部注意力层 vs. 仅最后一层**：FreeSOLO 和 CutLer 仅使用最后一层注意力或 ResNet/ViT 特征，在冷冻电镜数据上几乎完全失效（Dice 0.003）。本方法使用 Stable Diffusion 条件 UNet 全部 16 层注意力的 query-key 亲和矩阵，是性能跃升的关键瓶颈突破。
- **谱聚类优化 + 多样性分数 vs. 简单聚类**：SAM 使用通用提示机制，在冷冻电镜图像上 Dice 仅 0.048。本方法通过联合优化多层亲和矩阵的谱聚类目标（Eqn. 4）获得正交特征向量，再以多样性分数迭代合并，显著提升了特征图的判别力。
- **高斯自适应阈值 vs. 固定阈值**：冷冻电镜图像局部对比度差异大，高斯自适应阈值（b=15, C=3）相比固定阈值能更好适应局部强度变化，是伪标签质量的重要保障。

> **注意**：以上消融推断基于方法对比和设计逻辑，论文未提供受控消融实验数据，具体贡献度需手动验证。

---

### 7. 公平性讨论

本方法的评估设计体现了以下公平性考量：

- **零标注 vs. 有监督**：无监督方法不依赖任何人工标注，避免了标注偏见和跨域标注成本，在公平性上具有天然优势。
- **伪标签驱动训练**：无监督生成的伪标签用于训练标准有监督模型（UNet、DeepETPicker），而非自训练同一模型，保证了与有监督基线在模型架构和训练流程上的可比性。
- **跨域泛化验证**：在额外数据集上的测试，揭示了有监督方法因训练域偏差导致的失效，而无监督方法保持稳定，凸显了其在真实应用场景中的鲁棒性优势。

### 补充图表

![[assets/figures/papers/paper_list_l2621_https_openaccess_thecvf_com_content_CVPR2026_html_Uddin_Unsupervised_Mul/figures/005_Table_1.jpg]]
*Table 1: Dice score comparison between two training methods for membrane segmentation on VPP S. Pombe cellular cryo-ET datasets. The higher score indicates better segmentation*

![[assets/figures/papers/paper_list_l2621_https_openaccess_thecvf_com_content_CVPR2026_html_Uddin_Unsupervised_Mul/figures/006_Table_2.jpg]]
*Table 2: F1 Scores of different methods on VPP S. Pombe cellular cryo-ET datasets. The higher score is better. The value of n in supervised models represent the number of training particle coordinates*

![[assets/figures/papers/paper_list_l2621_https_openaccess_thecvf_com_content_CVPR2026_html_Uddin_Unsupervised_Mul/figures/002_Figure_2.jpg]]
*Figure 2: Membrane segmentation results on S. Pombe Tomograms. The image shows several slabs of training tomogram (TS 0008) and another tomogram with the expert annotated membrane mask as ground truth, and the predicted mask by supervised UNet and our unsupervised approach*

![[assets/figures/papers/paper_list_l2621_https_openaccess_thecvf_com_content_CVPR2026_html_Uddin_Unsupervised_Mul/figures/003_Figure_3.jpg]]
*Figure 3: Macromolecule localization results on S. Pombe Tomograms. The image shows several slabs of training tomogram (TS 0008) and another tomogram with annotated macromolecules drawn as bounding boxes. Ground Truth: green boxes, Deep-ETPicker (supervised alternative): cyan boxes, Our unsupervised method: yellow boxes*

## 定位与知识库关联

### 1. 在无监督分割谱系中的位置

本工作处于**基于视觉基础模型的无监督密集预测**与**冷冻电镜图像分析**的交叉点，其核心范式可概括为：*以预训练Stable Diffusion的注意力特征为通用视觉先验，通过谱聚类优化与启发式聚合将无监督特征转化为高质量伪标签，再驱动有监督模型完成跨尺度分割与定位*。

**与通用无监督分割方法的关系**：

现有无监督分割方法主要分为两类：基于自监督特征聚类的方法（如**FreeSOLO** (Wang et al., CVPR 2022) 和**CutLer** (Wang et al., CVPR 2023)）与基于基础模型提示的方法（如**SAM** (Kirillov et al., ICCV 2023)）。本工作与它们的关键差异体现在三个层面：

- **特征来源**：FreeSOLO和CutLer依赖于自监督预训练的ResNet或ViT的最后一层特征，而本方法使用Stable Diffusion条件UNet全部16层注意力的query-key亲和矩阵，捕获了更丰富的多尺度视觉对应关系。
- **聚合机制**：FreeSOLO采用基于相似度裁剪的FreeMask策略，CutLer使用MaskCut进行迭代掩码发现；本方法则通过求解联合谱聚类优化问题获得正交特征向量，再以多样性分数驱动的迭代合并与z轴相邻切片一致性校正构建聚集特征图——这一启发式聚合策略是弥合“特征向量”与“分割掩码”之间鸿沟的核心因果机制。
- **伪标签利用**：FreeSOLO采用同一模型的自训练范式，本方法则将伪标签用于训练专用的有监督模型（UNet用于膜分割，**DeepETPicker** (Liu et al., Nature Communications 2024) 用于大分子定位），实现了更稳定的全数据集推理。

**与冷冻电镜领域有监督方法的关系**：

在冷冻电镜图像分析领域，主流方法依赖人工标注训练有监督模型：膜分割通常使用**UNet** (Ronneberger et al., MICCAI 2015) 或其变体，大分子定位则采用**CrYOLO** (Wagner & Raunser, Communications Biology 2020) 或DeepETPicker。本方法的独特贡献在于证明：*完全无需人工标注的无监督伪标签，即可驱动这些有监督模型达到接近甚至超越部分有监督设置的性能*——膜分割Dice仅比有监督UNet低约4.6%（0.309 vs 0.324），大分子定位F1超过使用100个真实坐标训练的DeepETPicker（0.43 vs 0.35）。

### 2. 方法适用边界

**适用条件**：

- **数据特征**：方法针对冷冻电镜断层图像（cryo-ET）设计，核心假设是亚细胞结构在断层切片中呈现可辨别的强度变化模式。预处理中的CLAHE对比度增强进一步放大了这些模式。
- **用户输入**：仅需用户从少量代表性断层图中选择信息丰富的切片（slabs），无需任何像素级或坐标级标注。
- **计算资源**：特征向量优化需要GPU支持（当前单GPU实现每层切片约7-8分钟），但后续的伪标签生成与有监督训练可在标准硬件上完成。

**不适用或需谨慎使用的场景**：

- **单细胞器实例分割**：当前方法仅能区分“膜”与“大分子”两类结构，无法直接分割线粒体、内质网等单个细胞器——这需要结合下游形态学分析或引入额外的实例级先验。
- **极低信噪比数据**：方法依赖Stable Diffusion特征对图像结构的敏感性，在信噪比极低的断层图中，亲和矩阵可能无法捕获有意义的视觉对应关系。
- **实时处理需求**：特征向量优化是计算瓶颈，尚无法满足实时或近实时处理需求。

### 3. 局限与开放问题

**已知局限**（来自论文明确陈述）：

- **计算效率**：特征向量优化是主要速度瓶颈，单GPU处理每层切片需7-8分钟，限制了大规模部署。
- **语义粒度**：分割主干仅基于强度变化，无法区分单个细胞器类型，需要后续形态学分析或分类步骤。
- **验证范围**：方法仅在部分冷冻电镜数据集（VPP S. Pombe细胞断层图及少量额外数据集）上验证，更多细胞类型与成像条件下的稳定性仍需评估。

**开放问题**（来自论文讨论与合理推演）：

- **加速策略**：能否通过多GPU并行化、特征向量优化的模型压缩或轻量级替代方案（如直接使用部分注意力层的特征向量而不经优化）将处理时间压缩至实用级别？
- **实例级扩展**：能否在聚集特征图上直接引入形态学先验（如细胞器的典型尺寸与形状），一步实现单个细胞器的实例分割，而无需后处理分裂步骤？
- **跨模态泛化**：该方法对其他体积成像模态（如FIB-SEM、软X射线断层成像）的泛化能力如何？Stable Diffusion在自然图像上预训练的特征是否仍能提供有效的结构先验？
- **自适应参数**：启发式聚合中的多样性分数参数（块大小p、重叠步长s）目前为固定值，是否可通过可微分方式或元学习自适应调整？

### 4. 知识库定位

本工作为计算机视觉基础模型在**科学成像领域的无监督迁移**提供了一个可复用的技术框架。其核心洞察——*利用扩散模型全部注意力层的亲和矩阵，通过谱聚类优化与启发式聚合生成伪标签*——不限于冷冻电镜领域，对标注数据稀缺的其他科学成像任务（如医学病理图像、材料显微图像）具有潜在的迁移价值。在方法谱系上，它桥接了三个活跃的研究方向：视觉基础模型的特征复用、基于谱聚类的无监督分割、以及科学成像中的弱/无监督学习。

## 原文 PDF

![[paperPDFs/CVPR_2026/Unsupervised_Multi_Scale_Segmentation_of_3D_Subcellular_World_with_Stable_Diffusion_Foundation_Model.pdf]]
