---
title: "C-GenReg: Training-Free 3D Point Cloud Registration by Multi-View-Consistent Geometry-to-Image Generation with Probabilistic Modalities Fusion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/C_GenReg_Training_Free_3D_Point_Cloud_Registration_by_Multi_View_Consistent_Geometry_to_Image_Generation_with_Probabilistic_Modalities_Fusion.pdf
project_link: null
code_link: "https://github.com/yuvalH9/CGenReg"
aliases:
- CG
- C-GenReg
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过世界基础模型（WFM）将3D几何转换为多视图一致的RGB图像，利用任务特定的视觉基础模型（VFM）提取密集对应关系，并与原始几何特征进行概率后验融合。
primary_logic: 将点云配准转化为图像域匹配问题：利用WFM生成几何对齐且多视图外观一致的图像，结合匹配专用VFM和纯几何分支，通过“先匹配后融合”的概率建模（条件独立假设下的Noisy-AND/Noisy-OR）在无训练条件下获得高置信度对应。
claims:
- C-GenReg在3DMatch上实现最优的旋转和翻译精度，将GeoTransformer的平均RTE降低近一半。
- 在Waymo室外LiDAR基准上大幅超越基于KITTI训练的学习方法，首次验证生成式框架在真实LiDAR数据上的可行性。
- 消融表明概率融合（Noisy-AND）在匹配精度上优于简单特征级联，且Noisy-AND产生更高精度的点匹配。
- 3DMatch 上 旋转 Accuracy@5° (%) = 94.2
---

# C-GenReg: Training-Free 3D Point Cloud Registration by Multi-View-Consistent Geometry-to-Image Generation with Probabilistic Modalities Fusion

> [!tip] 核心洞察
> 将点云配准转化为图像域匹配问题：利用WFM生成几何对齐且多视图外观一致的图像，结合匹配专用VFM和纯几何分支，通过“先匹配后融合”的概率建模（条件独立假设下的Noisy-AND/Noisy-OR）在无训练条件下获得高置信度对应。

| 字段 | 内容 |
|------|------|
| 中文题名 | C-GenReg：基于多视图一致几何到图像生成与概率模态融合的无训练三维点云配准 |
| 英文题名 | C-GenReg: Training-Free 3D Point Cloud Registration by Multi-View-Consistent Geometry-to-Image Generation with Probabilistic Modalities Fusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.16680) · [Code](https://github.com/yuvalH9/CGenReg) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | C-GenReg |
| Dataset | 3DMatch, ScanNet Original, LoWaymo |

> [!tip] 效果简介
> - 3DMatch 上，旋转 Accuracy@5° (%) 94.2 vs 88.9 (+5.3)；平均 RTE (cm) 11.9 vs 24.6 (-51.6%)。
> - ScanNet Original 上，旋转 Accuracy@5° (%) 99.4 vs 94.0 (+5.4)；翻译 Accuracy@5cm (%) 87.5 vs 79.2 (+8.3)。
> - LoWaymo (低重叠) 上，平均 RRE (°) 4.95 vs 19.72 (-74.9%)。

## 概要

### 问题瓶颈

三维点云配准的核心挑战在于，现有的3D特征提取器严重依赖特定传感器模态和场景分布，缺乏跨域泛化能力和多视图一致性先验。与此同时，与图像领域蓬勃发展的视觉基础模型（VFM）相比，三维基础模型仍处于缺失状态，使得点云配准方法难以受益于大规模预训练带来的鲁棒表征。

### 核心思路

C-GenReg提出了一种**无训练、零样本**的生成式配准范式：将点云配准问题转化为图像域的匹配问题。其核心因果机制是利用**世界基础模型（WFM）**将源点云和目标点云的深度图序列分别转化为多视图一致、几何对齐的RGB图像，随后由**任务特定的视觉基础模型（MASt3R）**在生成图像上提取密集对应关系，并与原始几何分支的匹配结果进行**概率后验融合**。这一“先匹配后融合”的策略在条件独立假设下通过Noisy-AND/Noisy-OR算子联合建模两个模态的对应置信度，无需任何微调即可获得高精度对应点集。

### 方法谱系与知识库定位

C-GenReg处于**生成式点云配准**与**基础模型驱动的三维感知**的交叉点。与依赖手工特征（如FPFH）或在大规模数据上训练的纯几何方法（如GeoTransformer、FCGF、Predator、RoITr）不同，C-GenReg的所有模块均为预训练且冻结，以零样本方式运行。相较于已有的生成式配准探索（如GPCR、ZeroMatch、PointMBF），C-GenReg首次将世界基础模型引入配准流程，实现了从深度到多视图一致RGB的生成，并在真实室外LiDAR数据上验证了生成式框架的可行性。

### 主要结果

- **室内基准（3DMatch）**：C-GenReg在旋转Accuracy@5°上达到94.2%，平均翻译误差（RTE）降至11.9 cm——相比GeoTransformer的24.6 cm降低近一半。
- **室外基准（Waymo）**：在低重叠场景（LoWaymo）上，平均旋转误差从19.72°降至4.95°（降低74.9%），平均翻译误差从9.04 m降至1.66 m（降低81.6%），大幅超越基于KITTI训练的学习方法。
- **消融验证**：概率融合（Noisy-AND）相比简单特征级联在GeoTransformer特征上提升达5倍的RRE和RTE；任务特定VFM（MASt3R）相比通用VFM（DINOv2）将平均RTE降低约2倍。

### 局限与开放问题

方法的主要局限在于推理速度受WFM生成过程制约（单次注册约508秒），虽可通过蒸馏降至约7秒但仍不满足实时需求。此外，生成质量依赖深度输入和文本提示的语义合理性，极端动态场景或稀疏传感器上的泛化性尚未验证。开放问题包括：更轻量生成模型的探索、无文本提示条件下的鲁棒匹配、显式依赖建模对概率融合的改进，以及跨模态、跨季节场景的扩展。



三维点云配准旨在估计两帧点云之间的刚性变换，是三维视觉与机器人领域的核心任务。给定源点云和目标点云，配准的目标是找到最优旋转矩阵$\pmb{R}$和平移向量$\pmb{t}$，使得对齐后的对应点距离最小化：

$$
\underset{(\pmb{R},\pmb{t})\in SE(3)}{\arg\min}\sum_{(\pmb{p}^*,\pmb{q}^*)\in\mathcal{C}^*}\|\pmb{R}\pmb{p}_i^*+\pmb{t}-\pmb{q}_i^*\|_2^2
$$

该问题的关键在于获取高质量的跨点云对应关系$\mathcal{C}^*$。传统方法依赖手工设计的局部几何描述符（如**FPFH**）进行特征匹配，但在低重叠、重复纹理或大视角变化场景下表现脆弱。近年来，基于深度学习的方法通过在大规模数据上训练特征提取器（如**FCGF**、**Predator**、**GeoTransformer**、**RoITr**）显著提升了配准精度，然而这些方法面临一个根本性瓶颈：**3D点云特征提取器严重依赖传感器模态和场景，缺乏跨域泛化能力和多视图一致性先验，而真正意义上的3D基础模型至今仍处于缺失状态。**

与3D领域形成鲜明对比的是，2D视觉基础模型（VFM）已在图像匹配、密集对应等任务上展现出强大的泛化能力。部分工作尝试利用RGB-D数据中的颜色信息辅助配准（如**PointMBF**），或通过生成式方法将点云转化为图像域进行匹配（如**GPCR**、**ZeroMatch**），但这些方法要么依赖原生RGB输入，要么生成的图像缺乏跨视图的几何对齐和外观一致性，限制了其在实际纯几何传感器（如LiDAR）上的应用。

本文的核心动机在于回答一个关键问题：**能否将点云配准转化为图像域的匹配问题，从而充分利用2D视觉基础模型的强大先验，同时保持与原始几何特征的互补性？** 具体而言，C-GenReg通过世界基础模型（WFM）将3D几何转换为多视图一致的RGB图像，利用任务特定的VFM提取密集对应关系，并与原始几何特征进行概率后验融合。这一“先匹配后融合”的概率建模策略，使得整个框架在无需任何目标域训练的条件下，能够获得高置信度的跨模态对应，首次实现了生成式配准框架在真实室外LiDAR数据上的成功运行。



## 核心方法与创新机理

C-GenReg 的核心创新在于将点云配准问题转化为图像域匹配问题，并通过“先匹配后融合”的概率框架实现无训练的跨模态对应估计。相较于现有方法，其关键改变体现在三个维度。

### 1. 特征模态的扩展：从纯几何到几何-生成图像双分支

传统点云配准方法（如 **GeoTransformer**、**FCGF**、**Predator**）仅依赖原始点云的几何特征进行匹配。这类特征提取器严重依赖传感器模态和训练场景，缺乏跨域泛化能力。C-GenReg 引入了一个并行的生成RGB分支，从根本上改变了特征来源：

- **世界基础模型（WFM）**：采用 **Cosmos-Transfer** 将源点云和目标点云分别渲染为深度图序列，通过时序拼接输入WFM，生成多视图一致且外观对齐的RGB图像（Figure 5 验证了时序拼接相比水平拼接能有效保持跨视图几何一致性）。
- **任务特定视觉基础模型（VFM）**：使用 **MASt3R**——一个专为密集对应关系预训练的VFM——从生成的RGB视图中提取像素级对应感知特征，随后通过原始深度图将2D特征提升回3D点云。

这一设计将3D匹配问题转移到2D域，利用了大规模预训练VFM在图像匹配上的强大先验，绕过了3D基础模型缺失的瓶颈。消融实验（Table 4）表明，使用任务特定VFM（MASt3R）相比通用VFM（DINOv2）在平均RTE上降低约2倍，平均RRE降低约3倍，验证了VFM选择的关键性。

### 2. 对应关系获取与融合：从特征拼接/相似度匹配到概率后验融合

现有方法通常直接基于特征相似度矩阵提取对应关系，或将多模态特征简单级联后统一匹配。C-GenReg 提出了一种“先匹配后融合”（Match-then-Fuse）的概率框架，核心创新在于：

- **独立后验估计**：两个分支分别计算各自的相似度矩阵，并通过行级softmax得到单模态的对应后验概率 $p_{ij}^{\text{img}}$ 和 $p_{ij}^{\text{geo}}$（Eq. 4）。
- **条件独立假设下的概率融合**：在假设两个模态给定真实匹配状态条件独立的前提下，推导出联合后验 $p_{ij}^{\text{fuse}}$（Noisy-AND，Eq. 6）。该公式要求两个模态同时支持某一对应关系才能获得高置信度，天然倾向于保留高精度匹配。
- **对比方案 Noisy-OR**（Eq. 7）：任一模态的支持即可提升置信度，更注重召回率。

消融实验（Table 4 底部，Figure 8）表明，Noisy-AND 在GeoTransformer特征上相对特征级联提升达5倍的RRE和RTE，且在全召回范围内匹配精度始终高于Noisy-OR，验证了“联合支持”策略在配准任务中的优势。

### 3. 训练方式：从大规模监督训练到完全零样本

所有现有学习型配准方法均需在目标场景的大规模数据集（如3DMatch、KITTI）上进行训练或微调。C-GenReg 的所有模块——WFM（Cosmos-Transfer）、VFM（MASt3R）、几何特征提取器（GeoTransformer）——均使用公开预训练权重并保持冻结，无需任何微调。这使其具备天然的跨域泛化能力：在Waymo室外LiDAR基准上，C-GenReg以零样本方式大幅超越基于KITTI训练的学习方法（平均RRE降低74.9%，平均RTE降低81.6%，Table 3），首次验证了生成式配准框架在真实LiDAR数据上的可行性。

### 创新总结

C-GenReg 通过三个 changed slots 的系统性创新——引入生成RGB特征扩展模态空间、采用概率后验融合替代确定性匹配、以完全冻结的预训练模型实现零样本泛化——在无需任何任务特定训练的条件下，于室内RGB-D和室外LiDAR基准上均取得了最优或接近最优的配准精度。



C-GenReg的核心思想是将三维点云配准问题**迁移到图像域**：利用世界基础模型（WFM）从点云渲染的深度图生成多视图一致的RGB图像，借助任务特定的视觉基础模型（VFM）提取密集对应关系，再与原始几何特征进行概率后验融合，最终估计刚性变换。整个框架无需任何训练或微调，所有模块均使用预训练且冻结的权重。

### 双分支并行架构

如图2所示，C-GenReg由两个并行分支和一个融合阶段组成：

**生成式RGB分支（Generated-RGB Branch）**：该分支将源点云和目标点云分别渲染为深度图序列，通过时间维度拼接后送入冻结的世界基础模型（Cosmos-Transfer），生成几何对齐且跨视图外观一致的RGB视频帧。从生成的视图中选取K帧，送入任务特定的VFM（MASt3R）提取密集的像素级对应感知特征，再利用原始深度信息将2D特征提升回3D点云空间。

**几何分支（Geometric Branch）**：直接从原始点云提取密集几何描述符，采用预训练的几何特征提取器（GeoTransformer）编码结构线索，独立产生基于纯几何的对应关系。

### “先匹配后融合”的概率建模

两个分支各自独立计算源-目标点对的对应后验概率。几何分支通过特征相似度矩阵的softmax得到单模态后验 $p_{ij}^{\mathrm{geo}}$；图像分支取所有视图组合中最大相似度后验 $p_{ij}^{\mathrm{img}}$。随后，框架在**条件独立假设**下对两个后验进行概率融合——Noisy-AND建模“两分支同时支持”的联合后验，Noisy-OR建模“任一支支持即增加置信度”的析取后验。融合后的后验 $p_{ij}^{\mathrm{fuse}}$ 经鲁棒姿态估计器（SC2PCR）提取高置信度匹配并求解刚性变换。

### 输入输出流

1. **输入**：一对部分重叠的源/目标点云 $(\mathcal{P}, \mathcal{Q})$。
2. **深度渲染**：从两个点云各渲染 $L=50$ 帧深度图序列。
3. **WFM生成**：Cosmos-Transfer将深度序列转化为多视图一致的RGB视频（图5表明时间维度拼接是保持跨视图一致性的关键）。
4. **VFM特征提取**：选取 $K=4$ 帧输入MASt3R，提取密集2D特征并提升至3D。
5. **几何特征提取**：GeoTransformer直接处理原始点云。
6. **概率融合**：两分支后验经Noisy-AND/Noisy-OR融合为联合后验。
7. **姿态估计**：SC2PCR从融合后验中提取对应集合 $\mathcal{C}^*$，通过加权最小二乘求解刚性变换 $(\pmb{R}, \pmb{t})$。

对于室外LiDAR数据（如Waymo），框架通过虚拟相机将LiDAR点云投影为深度图（图7），其余流程保持一致，首次实现了生成式配准框架在真实LiDAR数据上的应用。

### 补充图表

![[assets/figures/papers/paper_list_l2445_https_arxiv_org_abs_2604_16680/figures/001_Figure_1.jpg]]
*Figure 1: C-GenReg: A training-free point cloud registration framework. The pipeline operates in two parallel branches: (1) Generated-RGB Branch - a World Foundation Model generates RGB views that are geometrically aligned with the input source and target point clouds and visually consistent across the two viewpoints; a task-specific Vision Foundation Model extracts dense image features and estimates RGB-based correspondences. (2) Geometric Branch - a geometric feature extractor encodes structural cues directly from the raw 3D point clouds and independently produces geometry-based correspondences. The two correspondence probability maps are then fused using our “Match-then-Fuse” probabilistic fusion...*

![[assets/figures/papers/paper_list_l2445_https_arxiv_org_abs_2604_16680/figures/002_Figure_2.jpg]]
*Figure 2: C-GenReg Overview: A training-free, zero-shot point cloud registration framework with two parallel branches. (1) Generated-RGB Branch - source and target point clouds are each represented as depth-frame sequences, temporally concatenated and processed by a frozen World Foundation Model to generate RGB views that are geometrically aligned and appearance-consistent across views. A subset of K frames per domain is fed to a frozen, task-specific Vision Foundation Model (VFM) to extract dense pixel-level features, later lifted to 3D using the original depths. (2) Geometric Branch - extracts dense geometric features directly from the raw point clouds using a pretrained geometric feature extractor...*



C-GenReg 将点云配准分解为两个并行的特征提取分支和一个概率融合阶段，其核心设计在于“先匹配后融合”：每个分支独立产生对应关系后验概率，再通过概率推理融合为统一的联合后验，从而避免了对特征空间的显式对齐学习。

### 双分支架构与特征提取

**生成RGB分支** 将三维配准问题转移到图像域。给定源点云和目标点云，首先从每个点云渲染深度图序列，然后利用冻结的世界基础模型 **Cosmos-Transfer** 将深度序列转化为多视图一致的RGB视频。该过程采用时序拼接（temporal concatenation）而非水平拼接，以保持跨视图的几何一致性和外观一致性（见 Figure 5）。从生成的视频中选取 $K$ 帧，送入任务特定的视觉基础模型 **MASt3R** 提取密集的对应感知特征。MASt3R 是专门为密集匹配和配准训练的 VFM，相比通用 VFM（如 DINOv2）能提供更强的对应判别能力。提取的像素级特征随后通过原始深度图提升回三维空间，得到3D点云的图像域描述符。

**几何分支** 直接从原始点云提取结构特征，采用预训练的 **GeoTransformer** 作为几何特征提取器，无需任何微调。该分支保留了纯几何线索，为融合提供互补的模态信息。

两个分支均使用公开的预训练权重且保持冻结，整个流程为零样本、无训练。

### 对应关系后验建模

两个分支独立计算源点云与目标点云之间的特征相似度矩阵，并通过行级 softmax 转化为对应后验概率。

**几何相似度矩阵** 由几何分支的源特征 $F_{\mathrm{src}}^{\mathrm{geo}}$ 和目标特征 $F_{\mathrm{tgt}}^{\mathrm{geo}}$ 的内积得到：

$$S^{\mathrm{geo}} = F_{\mathrm{src}}^{\mathrm{geo}}(F_{\mathrm{tgt}}^{\mathrm{geo}})^\top$$

**图像相似度矩阵** 考虑所有 $K^2$ 个视图对的组合，取最大相似度以利用多视图冗余：

$$S^{\mathrm{img}} = \max_{k\in\{1,\dots,K^2\}} F_{\mathrm{src},k}^{\mathrm{img}}(F_{\mathrm{tgt},k}^{\mathrm{img}})^\top$$

对于每个模态 $m \in \{\mathrm{img}, \mathrm{geo}\}$，将相似度矩阵通过带温度参数 $\tau_m$ 的 softmax 转化为匹配后验概率：

$$p_{ij}^{m} \triangleq \mathrm{Pr}(M_{ij}=1|S_{ij}^{m}) = \mathrm{Softmax}_{j}(S_{ij}^{m}/\tau_m)$$

其中 $M_{ij}=1$ 表示源点 $i$ 与目标点 $j$ 构成真值对应。温度参数 $\tau_m=0.1$ 用于锐化概率分布。

### 概率融合：“Match-then-Fuse”

C-GenReg 的核心创新在于对两个独立后验进行概率融合，而非在特征层面进行拼接或对齐。给定两个分支的后验 $p_{ij}^{\mathrm{img}}$ 和 $p_{ij}^{\mathrm{geo}}$，在条件独立假设下推导联合后验。

**Noisy-AND 融合** 建模为“两个模态共同支持”的合取机制。引入先验匹配概率 $\pi_{ij}$ 作为噪声模型，联合后验为：

$$p_{ij}^{\mathrm{fuse}} = \frac{p_{ij}^{\mathrm{img}}p_{ij}^{\mathrm{geo}}(1-\pi_{ij})}{p_{ij}^{\mathrm{img}}p_{ij}^{\mathrm{geo}}(1-\pi_{ij})+(1-p_{ij}^{\mathrm{img}})(1-p_{ij}^{\mathrm{geo}})\pi_{ij}}$$

该公式的直观含义是：当两个模态均给出高置信度时，融合后验趋近于1；当任一模态置信度低时，后验被抑制。$\pi_{ij}$ 控制了对冲突的容忍度。

**Noisy-OR 融合** 作为对比方案，建模为“任一模态支持即增强置信度”的析取机制：

$$p_{ij}^{\mathrm{Noisy-OR}} = 1-(1-p_{ij}^{\mathrm{img}})(1-p_{ij}^{\mathrm{geo}})$$

消融实验表明，Noisy-AND 在全召回范围内匹配精度更高，更适合保留高置信度对应（见 Figure 8），且在 GeoTransformer 特征上相对特征级联提升可达 5 倍的 RRE 和 RTE。

### 姿态估计

从融合后验 $p_{ij}^{\mathrm{fuse}}$ 中提取高置信度对应集合 $\mathcal{C}^*$，通过最小二乘优化求解刚性变换：

$$\underset{(\pmb{R},\pmb{t})\in SE(3)}{\arg\min}\sum_{(\pmb{p}^*,\pmb{q}^*)\in\mathcal{C}^*}\|\pmb{R}\pmb{p}_i^*+\pmb{t}-\pmb{q}_i^*\|_2^2$$

该步骤采用 SC2PCR 鲁棒估计器，在存在离群对应的情况下稳定求解 $SE(3)$ 变换。

### 补充图表

![[assets/figures/papers/paper_list_l2445_https_arxiv_org_abs_2604_16680/figures/009_Figure_5.jpg]]
*Figure 5: WFM Input Formatting. (a) Input depth maps of the source and target views. (b) Feeding the pretrained WFM with horizontally concatenated depth inputs causes cross-view inconsistencies, e.g., the sofa is mistakenly replaced in the generated source image. (c) Using temporal concatenation produces RGB outputs that are geometrically coherent and appearance-consistent between the two views*

![[assets/figures/papers/paper_list_l2445_https_arxiv_org_abs_2604_16680/figures/011_Figure_7.jpg]]
*Figure 7: C-GenReg LiDAR Input Pipeline: (a) A virtual camera is configured into the LiDAR scan. (b) The LiDAR points are projected into a depth image. (c) The resulting depth map is fed into the generative model to produce an aligned RGB image*



## 实验与关键发现

### 主结果：室内基准

C-GenReg 在 3DMatch 基准上实现了全面的最优性能。如表 1 所示，C-GenReg 在旋转 Accuracy@5° 上达到 94.2%，超越此前最优的 GeoTransformer（88.9%）达 5.3 个百分点；平均 RTE 从 GeoTransformer 的 24.6 cm 降至 11.9 cm，降幅达 51.6%。在 ScanNet Hard 和 SuperGlue Split 基准上（表 2），C-GenReg 同样在多数指标上取得最优。在 ScanNet Original 基准上（表 6），C-GenReg 相对 GeoTransformer 将旋转 Accuracy@5° 从 94.0% 提升至 99.4%，翻译 Accuracy@5cm 从 79.2% 提升至 87.5%。

值得注意的是，C-GenReg 以零样本方式评估，所有模块均使用公开预训练权重且未在任何目标数据集上微调；而对比的纯几何学习方法（GeoTransformer、FCGF、Predator、RoITr 等）均在 3DMatch 官方训练集上充分训练。这一公平性差异进一步凸显了生成式框架的跨域泛化优势。

### 主结果：室外 LiDAR 基准

在 Waymo 室外基准上（表 3），C-GenReg 首次验证了生成式配准框架在真实 LiDAR 数据上的可行性。在低重叠场景 LoWaymo 上（表 7），C-GenReg 将平均 RRE 从 RoITr（在 KITTI 上训练）的 19.72° 降至 4.95°（降幅 74.9%），平均 RTE 从 9.04 m 降至 1.66 m（降幅 81.6%）。这一结果揭示了基于 KITTI 训练的学习方法在跨传感器、跨场景迁移时的严重退化，而 C-GenReg 通过 WFM 生成的 RGB 图像有效弥补了纯几何特征在室外稀疏点云中的表示不足。

### 消融实验

**视觉基础模型选择**（表 4 上部分）：在仅使用生成 RGB 分支（无几何特征、无融合）的条件下，任务特定的 MASt3R 相比通用 VFM DINOv2 将平均 RTE 降低约 2 倍，平均 RRE 降低约 3 倍。这表明密集对应感知的预训练目标对配准任务至关重要，通用语义特征无法提供足够的几何判别力。

**几何特征提取器与融合策略**（表 4 下部分）：在 MASt3R 作为固定 VFM 的条件下，对比了不同几何特征提取器（GeoTransformer、FCGF）和融合方式。概率融合（Noisy-AND）相对于简单特征级联在 GeoTransformer 特征上实现高达 5 倍的 RRE 和 RTE 提升。这一结果表明，“先匹配后融合”的概率建模比直接拼接特征空间能更有效地校准两个模态的置信度，避免低质量模态污染高置信度对应。

**Noisy-AND vs. Noisy-OR**（图 8）：在全召回范围内，Noisy-AND 的匹配精度持续高于 Noisy-OR。Noisy-AND 的联合支持机制（要求两个模态同时支持才提升置信度）天然倾向于保留高置信度对应，而 Noisy-OR 的析取机制在引入额外匹配的同时也放大了假阳性，导致下游配准精度下降。

**视图数量 K 的影响**（图 6）：当 K≥4 时，配准性能趋于饱和。少量视图已能提供足够的视角多样性，更多视图仅带来边际收益，但会线性增加计算开销。

**提示鲁棒性**（图 4）：使用错误的语义描述（如将“卧室”误标为“厨房”）会导致注册精度明显下降，但粗略的场景描述即可维持接近最优的性能。这表明 WFM 的文本提示主要作为轻量语义稳定器，几何保真度和跨视图一致性更多依赖深度输入的结构约束。

### 推理效率与局限

单次注册约需 508 秒（表 5，单张 NVIDIA RTX A6000 GPU），瓶颈主要在于 WFM 的视频生成。通过模型蒸馏可将推理时间降至约 7 秒，但仍不适合实时应用。此外，室外 LiDAR 数据需通过虚拟相机投影为深度图（图 7），引入了畸变和视野限制；全景配准需要多个相机拼接，增加了工程复杂度。方法尚未在极端动态场景或稀疏传感器（如雷达）上验证，这些场景下深度图质量和生成一致性可能进一步下降。

### 补充图表

![[assets/figures/papers/paper_list_l2445_https_arxiv_org_abs_2604_16680/figures/005_Table_1.jpg]]
*Table 1: 3DMatch Benchmark. Rotation and translation accuracy (% of pairs within RRE/RTE thresholds in deg and cm respectively) and mean/median error across different methods. RGB-D baselines are included as complementary reference. Best in bold, second-best in underlined*

![[assets/figures/papers/paper_list_l2445_https_arxiv_org_abs_2604_16680/figures/008_Table_4.jpg]]
*Table 4: Ablation Study on the 3DMatch Benchmark. Top: impact of different Vision Foundation Models (no geometric features or fusion). Bottom: impact of geometric feature extractors and fusion operators (using MASt3R as the VFM). Best in bold*

![[assets/figures/papers/paper_list_l2445_https_arxiv_org_abs_2604_16680/figures/007_Table_3.jpg]]
*Table 3: Waymo Outdoor Registration Benchmark. Rotation (deg) and translation (m) accuracy/error. Best results are in bold*

![[assets/figures/papers/paper_list_l2445_https_arxiv_org_abs_2604_16680/figures/014_Table_7.jpg]]
*Table 7: Low-Overlap Results. Mean RRE (degrees) and mean RTE (cm for Lo3DMatch and m for LoWaymo)*

![[assets/figures/papers/paper_list_l2445_https_arxiv_org_abs_2604_16680/figures/004_Figure_4.jpg]]
*Figure 4: Prompt robustness on 3DMatch. Relative rotation (RRE,◦) and translation (RTE, cm) errors under different prompt types*

![[assets/figures/papers/paper_list_l2445_https_arxiv_org_abs_2604_16680/figures/010_Figure_6.jpg]]
*Figure 6: Effect of View Selection (K). Registration performance measured by Relative Rotation Error (RRE) and Relative Translation Error (RTE) as a function of the number of selected views K. Performance saturates for*

![[assets/figures/papers/paper_list_l2445_https_arxiv_org_abs_2604_16680/figures/003_Figure_3.jpg]]
*Figure 3: C-GenReg qualitative example on 3DMatch. Generated source and target images with a subset of matched points (color-coded correspondences), and the corresponding matches visualized on the input point clouds. The resulting rotation (RRE) and translation (RTE) errors are reported*

![[assets/figures/papers/paper_list_l2445_https_arxiv_org_abs_2604_16680/figures/012_Table_5.jpg]]
*Table 5: Runtime Analysis. Runtime per registration problem measured on a single NVIDIA RTX A6000 GPU*



## 定位与知识库关联

### 1. 与基线方法的关系

C-GenReg 处于点云配准方法谱系中的一个独特交叉点：它同时继承了**生成式点云配准**和**基于视觉基础模型的零样本匹配**两条技术路线，但通过“先匹配后融合”的概率框架将它们系统性地整合。

**相对于纯几何配准方法**，C-GenReg 不替代而是**增强**了几何分支。其几何分支直接使用预训练的 **GeoTransformer** 提取密集几何描述符，这与当前最强的学习型纯几何方法（如 GeoTransformer、FCGF、Predator、RoITr）共享相同的特征提取范式。区别在于，C-GenReg 并不依赖几何特征单独完成匹配，而是将其作为双分支融合中的一个互补模态。实验表明，即使单独使用 GeoTransformer 特征并加上概率融合（Noisy-AND），在 3DMatch 上的平均 RRE 和 RTE 相比特征级联可提升达 **5 倍**（Table 4 底部消融），说明融合机制本身对纯几何分支也有显著增益。

**相对于生成式点云配准方法**，C-GenReg 与 **GPCR**（生成式点云补全后配准）和 **ZeroMatch**（生成式 RGB-D 配准）形成对比。GPCR 通过生成缺失几何来辅助配准，仍停留在 3D 域；ZeroMatch 利用扩散模型生成 RGB 图像进行匹配，但缺乏多视图一致性约束。C-GenReg 的核心突破在于引入**世界基础模型（Cosmos-Transfer）** 实现多视图几何一致的 RGB 生成，从根本上解决了生成图像与原始几何的对齐问题。

**相对于 RGB-D 配准方法**，如 **PointMBF**（基于学习的 RGB-D 配准），C-GenReg 的关键区别在于**无需真实 RGB 输入**——它从深度图生成 RGB，使框架能直接应用于纯 LiDAR 数据（如 Waymo），这是此前生成式方法未曾验证的场景。

### 2. 技术谱系中的知识继承与创新

C-GenReg 的知识库定位可分解为三个层次的模型复用与创新：

| 层次 | 模型/组件 | 来源与角色 | 是否冻结 |
|------|----------|-----------|---------|
| 世界先验 | Cosmos-Transfer WFM | 大规模视频生成预训练，提供几何到RGB的跨模态映射与多视图一致先验 | 冻结 |
| 任务先验 | MASt3R VFM | 密集对应匹配预训练，提供像素级匹配感知特征 | 冻结 |
| 几何先验 | GeoTransformer | 3D点云配准预训练，提供结构几何描述符 | 冻结 |
| 融合机制 | Noisy-AND/Noisy-OR | 本文提出的概率后验融合，条件独立假设下的联合推理 | 无需训练 |
| 姿态估计 | SC2PCR | 鲁棒刚性变换估计，从融合后验中提取匹配并求解 | 无需训练 |

所有预训练模型均保持冻结，C-GenReg 本身**不引入任何可学习参数**，这是其“无训练”（training-free）属性的根本来源。创新集中在：
1. **深度序列到 RGB 视频的生成管道设计**：时间维度拼接（而非空间拼接）是保证多视图一致性的关键（Figure 5 对比验证）；
2. **“先匹配后融合”的概率框架**：两个分支独立计算对应后验，再通过 Noisy-AND（联合支持）或 Noisy-OR（析取支持）融合，避免特征级联带来的校准问题；
3. **2D→3D 特征提升**：利用原始深度图将像素级匹配特征精确映射回 3D 点云。

### 3. 适用边界与泛化能力

**已验证的适用场景**：
- 室内 RGB-D 扫描配准（3DMatch、ScanNet）：C-GenReg 在零样本条件下达到或超越需要目标域训练的学习方法；
- 室外自动驾驶 LiDAR 配准（Waymo）：首次验证生成式框架在真实 LiDAR 数据上的可行性，在低重叠场景（LoWaymo）上相对基于 KITTI 训练的方法，平均 RRE 降低 74.9%，平均 RTE 降低 81.6%。

**泛化能力的关键来源**：
- WFM 和 VFM 在大规模异构数据上预训练，提供了远超特定配准数据集的视觉先验；
- 文本提示仅作为轻量语义稳定器，粗略场景描述即可维持性能（Figure 4 验证），降低了提示工程的敏感性。

**适用边界与限制**：
1. **推理速度**：单次注册约 508 秒（Table 5），瓶颈在 WFM 视频生成。通过模型蒸馏可降至约 7 秒，但仍不满足实时需求（<1 秒）。
2. **输入质量依赖**：生成质量依赖深度序列质量和文本提示的语义合理性。语义错误的提示会导致注册精度明显下降（Figure 4）。
3. **LiDAR 场景限制**：室外 LiDAR 需通过虚拟相机投影为深度图，引入畸变和视野限制；全景配准需多相机拼接，增加了系统复杂度。
4. **未验证场景**：极端动态场景、稀疏传感器（如雷达）、跨季节/天气变化场景的配准尚未测试。

### 4. 局限性与开放问题

**已识别的局限性**（来自论文分析）：
- **推理速度瓶颈**：WFM 视频生成是主要耗时环节，当前单次注册约 508 秒（NVIDIA RTX A6000），即使蒸馏后约 7 秒，仍不适合实时 SLAM 或在线定位；
- **提示依赖性**：虽然粗略提示即可维持性能，但完全去除文本提示能否保持多视图一致性尚不明确；
- **条件独立假设**：概率融合假设图像分支和几何分支条件独立，可能未充分利用模态间的互补信息；
- **LiDAR 数据适配**：虚拟相机投影引入了额外的超参数（相机内参、位置），且视野受限。

**开放研究问题**：
1. **轻量化生成**：能否采用更轻量的生成模型（如潜在扩散模型、一致性模型）或知识蒸馏策略，使整体推理达到实时（<1 秒）？这是走向实际部署的关键瓶颈。
2. **无提示生成**：是否可能在完全不使用文本提示的条件下，仅依赖深度序列保持多视图一致性和鲁棒匹配？这需要 WFM 具备更强的无条件几何理解能力。
3. **依赖建模**：当前概率融合假设两个分支条件独立，若引入显式依赖建模（如 copula 或注意力机制），能否进一步提升融合后验的校准度？
4. **多模态扩展**：方法是否适用于多模态传感器融合（如雷达+相机）或跨季节/天气变化场景的配准？这需要验证 WFM 在非可见光模态下的生成能力。
5. **基础模型替代**：其他新兴世界基础模型（如 Sora、VideoPoet）或通用 VFM（如 Segment Anything Model、DINOv2）能否替代现有模块并获得更好泛化？Table 4 已初步验证 MASt3R 优于 DINOv2，但更广泛的模型选择空间仍待探索。
6. **跨域迁移的理论理解**：WFM 和 VFM 的预训练数据与点云配准目标域之间的分布差异如何影响性能？缺乏理论分析限制了对方法泛化边界的预测。



## 原文 PDF

![[paperPDFs/CVPR_2026/C_GenReg_Training_Free_3D_Point_Cloud_Registration_by_Multi_View_Consistent_Geometry_to_Image_Generation_with_Probabilistic_Modalities_Fusion.pdf]]
