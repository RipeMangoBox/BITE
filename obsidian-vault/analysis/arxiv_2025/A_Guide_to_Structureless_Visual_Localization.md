---
title: A Guide to Structureless Visual Localization
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/A_Guide_to_Structureless_Visual_Localization.pdf
project_link: null
code_link: null
aliases:
- SVLCEF
- GSVL
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 几何推理的程度与类型（位姿三角化 / 半广义相对位姿估计 / 动态局部SfM+绝对位姿估计 / 相对位姿回归）、特征匹配类型（稀疏特征SuperPoint/ALIKED vs 稠密匹配器RoMa/MASt3R）、深度预测器选择（Metric3D v2 vs MASt3R stereo）以及三角化策略（全体数据库图像 vs 图像对）。
primary_logic: 更充分的显式几何推理通常带来更好的定位精度——动态构建局部SfM模型（Local triangulation - all）达到最优精度，在Aachen日间场景与结构基方法MeshLoc持平；半广义相对位姿估计（E5+1）提供最佳的精度-速度权衡。无结构方法在日间场景中可与结构基方法媲美，同时天然支持场景更新。没有一种特征类型在所有场景中表现最优——RoMa在室外数据集占优，MASt3R在室内数据集占优。
claims:
- 局部三角化（Local triangulation - all）在Aachen日间达到86.7/93.8/98.3，与结构基方法MeshLoc（85.9/93.6/98.8）持平
- E5+1在Aachen日间/夜间分别达到78.4/65.4（0.25m,2°），远优于Ess. mat. (5Pt)和E3+1
- 相对位姿回归方法（Reloc3r）在Aachen日间仅达到5.2/14.2/63.0，远低于基于几何的方法
- 更充分的几何推理带来更好的性能，构建局部SfM模型的方法达到最优结果
---

# A Guide to Structureless Visual Localization

> [!tip] 核心洞察
> 更充分的显式几何推理通常带来更好的定位精度——动态构建局部SfM模型（Local triangulation - all）达到最优精度，在Aachen日间场景与结构基方法MeshLoc持平；半广义相对位姿估计（E5+1）提供最佳的精度-速度权衡。无结构方法在日间场景中可与结构基方法媲美，同时天然支持场景更新。没有一种特征类型在所有场景中表现最优——RoMa在室外数据集占优，MASt3R在室内数据集占优。

| 字段 | 内容 |
|------|------|
| 中文题名 | 无结构视觉定位指南 |
| 英文题名 | A Guide to Structureless Visual Localization |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2504.17636) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | Structureless Visual Localization Comprehensive Evaluation Framework |
| Dataset | Aachen Day-Night v1.1, Extended CMU Seasons, NAVER HDS 1F |

> [!tip] 效果简介
> - Aachen Day-Night v1.1 (day) 上，localization recall at (0.25m,2°)/(0.5m,5°)/(5m,10°) Local triang. - all: 86.7/93.8/98.3 vs Hloc (structure-based): 88.1/95.4/99.0 (-1.4/-1.6/-0.7 pp)；localization recall at (0.25m,2°)/(0.5m,5°)/(5m,10°) E5+1: 78.4 (0.25m,2°) vs E3+1: 54.2 (0.25m,2°) (+24.2 pp)；localization recall at (0.25m,2°)/(0.5m,5°)/(5m,10°) Ess. mat. (MASt3R poses): 23.2/49.0/91.0 vs Reloc3r: 5.2/14.2/63.0 (+18.0/+34.8/+28.0 pp)。
> - Extended CMU Seasons (urban) 上，localization recall at (0.25m,2°)/(0.5m,5°)/(5m,10°) Local triang. - all: 95.5 (0.25m,2°) vs E5+1 (second best structureless)。
> - Aachen Day-Night v1.1 上，average runtime per query (ms) LazyLoc: 101.33 ms (fastest) vs Local triang. - all: 2908.96 ms (slowest) (28.7× faster)。

## 概要

视觉定位旨在从单张查询图像估计其在已知场景中的6自由度相机位姿。传统结构基方法依赖预构建的3D场景模型（如SfM点云或Mesh），通过建立2D-3D匹配来求解位姿，精度较高但场景更新成本大——任何场景变动都需要重建3D模型。**无结构视觉定位**（structureless visual localization）采用根本不同的范式：场景仅由一组带有相机位姿和内参的数据库图像表示，定位时先通过图像检索召回相关数据库图像，再从查询图像与检索图像的2D-2D匹配中直接估计查询位姿，完全绕过了全局3D模型的构建与维护。

这一范式转变带来了灵活性与精度之间的**根本性权衡**：增删数据库图像即可实现场景更新，但缺少预构建的全局3D模型意味着所有几何推理必须从局部的、可能充满噪声的2D-2D匹配中完成。在视觉模糊、重复纹理或低重叠度的场景中，匹配噪声会直接传导到位姿估计，构成核心瓶颈。

本文对无结构视觉定位方法进行了系统性的评估与剖析，核心发现可概括为三条主线：

**几何推理深度决定精度上限。** 无结构方法的位姿估计可按几何推理的充分程度分为四个层次：位姿三角化（仅利用相对平移方向）→ 半广义相对位姿估计（利用部分已知3D信息约束相对位姿）→ 动态局部SfM+绝对位姿估计（在查询时实时构建局部3D模型）→ 相对位姿回归（用学习模型直接回归相对位姿）。实验一致表明，推理越充分，精度越高——动态构建局部SfM模型的方法（Local triangulation - all）达到最优精度，在Aachen日间场景中以86.7/93.8/98.3（0.25m,2°/0.5m,5°/5m,10°阈值下的定位召回率）与结构基方法MeshLoc持平（Table 7）；而依赖学习的回归方法Reloc3r在同一场景仅达到5.2/14.2/63.0，远低于经典几何方法（Table 1），表明现有回归模型尚未有效编码场景几何约束。

**精度-速度权衡存在明确最优解。** 在运行效率方面，E5+1半广义相对位姿估计方法提供了最佳的精度-速度权衡——在Aachen日间/夜间分别达到78.4/65.4（0.25m,2°），同时保持可控的计算开销。LazyLoc以约101ms/查询的速度成为速度优先场景下的良好替代方案，而精度最优的Local triangulation - all则需要约2.9秒/查询。

**特征选择具有场景依赖性。** 没有一种特征类型在所有场景中表现最优：RoMa稠密匹配器在室外数据集（Extended CMU Seasons）中占优，MASt3R匹配器在室内数据集（NAVER）中表现更好。这一发现意味着实际部署时需根据场景类型进行特征选择，而非依赖单一通用方案。

在方法谱系中，本文工作并非提出一种新的定位算法，而是建立了一个统一的评估框架，将现有的无结构定位方法按其几何推理机制系统分类，并在统一实验条件下进行公平对比。相较于结构基SOTA方法Hloc（Sarlin et al., CVPR 2019）和MeshLoc（Panek et al., ECCV 2022），无结构方法在日间场景中已展现出可比的精度，同时天然支持场景更新。然而，在Aachen夜间场景中仍存在约10个百分点的精度差距，夜间条件下的鲁棒性不足是当前无结构方法的主要短板。



视觉定位（Visual Localization）旨在估计给定查询图像相对于已知场景的6自由度相机位姿，是自动驾驶、增强现实和机器人导航等应用的基础能力。传统方法依赖预构建的显式3D场景模型——通常通过运动恢复结构（SfM）从数据库图像中重建稀疏或稠密的3D点云，定位时将查询图像的2D特征与3D点关联，再通过PnP求解器计算位姿。这类**结构基方法**（如**Hloc**, Sarlin et al., CVPR 2019；**MeshLoc**, Panek et al., ECCV 2022）在标准基准上取得了领先的定位精度，但其核心局限在于：3D模型的构建和维护成本高昂，且对场景变化（如建筑物翻新、家具移动、季节性植被变化）高度敏感——任何场景更新都需要重新运行完整的SfM流程。

**无结构视觉定位**（Structureless Visual Localization）提供了一种根本不同的范式：场景仅由一组带有相机位姿和内参的数据库图像表示，无需显式3D模型。给定查询图像，系统首先通过图像检索识别一组相关的数据库图像，然后直接从查询图像与这些检索图像之间的2D-2D匹配中估计查询相机的位姿。这一范式天然支持场景更新——增删数据库图像即可实现，无需重建3D模型。

然而，无结构方法面临一个根本性瓶颈：**缺少预构建的全局3D模型意味着必须从局部2D-2D匹配中进行几何推理，而在存在视觉模糊、重复纹理或低重叠度的场景中，2D-2D匹配的噪声会直接传导到位姿估计**。更深层的问题在于几何推理深度的选择——推理越充分，精度潜力越大，但计算成本也越高。现有无结构方法在几何推理策略上存在显著差异，从简单的位姿三角化到动态局部SfM重建，缺乏系统性的对比和统一的评估框架。此外，特征匹配类型（稀疏关键点 vs 稠密匹配器）、深度预测器选择以及图像检索策略等因素如何影响最终定位性能，此前尚未得到系统性的实证研究。

本文的核心动机在于填补这一空白：通过构建统一的评估框架，系统性地对比无结构视觉定位中的四类几何推理方法族——**位姿三角化**、**半广义相对位姿估计**、**动态局部SfM + 绝对位姿估计**以及**相对位姿回归**——并深入分析特征匹配类型、深度预测源和三角化策略等关键设计选择对定位精度与运行效率的影响。目标是揭示无结构方法的精度上限、精度-速度权衡关系以及与结构基方法的真实差距，为该领域的后续研究提供可复现的基准和明确的方向指引。



## 核心方法与创新机理

本文并非提出单一算法，而是构建了一个系统性的**无结构视觉定位方法评估框架**，通过统一实验条件对四个方法族进行公平基准测试，揭示出无结构定位的核心创新杠杆——**几何推理深度的精细控制**。

### 关键改进槽位

#### 1. 几何推理层级：从位姿三角化到动态局部SfM

无结构方法的核心因果旋钮在于**几何推理的充分程度**。本文系统对比了四种推理范式，形成精度递增的谱系：

- **位姿三角化**（Ess. mat. 5Pt）：仅使用相对平移方向进行位置三角化，几何推理最浅，在Aachen日间场景(0.25m,2°)精度仅为51.4%（Table 3）。
- **半广义相对位姿估计**（E5+1）：利用5个数据库图像的位姿约束求解本质矩阵，几何约束显著增强，将(0.25m,2°)精度提升至78.4%，较Ess. mat. 5Pt提高27个百分点。
- **动态局部SfM + 绝对位姿估计**（Local triangulation - all）：对所有检索到的数据库图像进行3D点三角化，在RANSAC框架内进行完整的局部重建与绝对位姿估计，达到最优精度——Aachen日间86.7/93.8/98.3，与结构基方法**MeshLoc**（Panek et al., ECCV 2022）的85.9/93.6/98.8持平（Table 7）。
- **相对位姿回归**（Reloc3r）：使用神经网络直接回归相对位姿，完全绕开显式几何推理，在Aachen日间仅达到5.2/14.2/63.0，远低于所有几何方法（Table 1）。

**核心洞察**：“更充分的显式几何推理通常带来更好的定位精度”（Section 5 Conclusion），但代价是运行时间的显著增加——Local triangulation - all平均耗时2909 ms/查询，而LazyLoc仅需101 ms（Table 2）。

#### 2. 精度-速度权衡的最优解：E5+1

在精度与效率的权衡中，**E5+1半广义相对位姿估计**构成最优前沿。该方法仅需5个数据库图像即可实现78.4%的(0.25m,2°)精度，较E3+1（仅使用3个数据库图像）的54.2%提升24.2个百分点（Table 3），证明**增加广义位姿约束的数量是提升精度的有效杠杆**。当速度优先时，LazyLoc以101 ms/查询的极低延迟成为良好替代方案。

#### 3. 场景自适应的特征选择策略

消融实验揭示了一个关键发现：**没有一种特征类型在所有场景中一致最优**（Section 4.1 Discussion）。具体而言：
- **室外场景**（Aachen、Extended CMU Seasons）：稠密匹配器**RoMa**（outdoor模型）表现最优（Figure 2, Figure 5）。
- **室内场景**（NAVER）：**MASt3R匹配器**在较粗阈值下占优（Figure 2, Figure 5）。

这一发现将特征选择从固定配置提升为**场景类型相关的自适应决策**，是无结构方法部署中的关键创新点。

#### 4. 深度预测器的非关键性

对于依赖单目深度预测的方法（Ess. mat. 3Pt+depth、E3+1），消融实验表明**深度预测器的选择并不关键**——Metric3D v2与MASt3R stereo在多数场景中表现相近（Figure 3, Figure 6）。然而，MASt3R深度图的一个根本性缺陷被揭示：尽管训练目标为度量深度，其实际预测缺乏度量尺度，在样本中尺度偏差可达15.83倍（Section 4）。这解释了MASt3R depth + P3P方法在Aachen日间仅达0.1/1.1/37.7的极差表现（Table 1）——失败源于深度尺度缺失，而非P3P求解器本身。

### 方法谱系与知识库定位

本文的无结构定位框架位于以下方法谱系中：

- **结构基方法**：**Hloc**（Sarlin et al., CVPR 2019）和**MeshLoc**（Panek et al., ECCV 2022）依赖预构建的SfM点云或网格模型，提供精度上界但缺乏场景更新灵活性。本文证明Local triangulation - all在日间场景中可与MeshLoc持平，同时天然支持通过增删数据库图像实现场景更新。
- **位姿三角化方法**：**Ess. mat. 5Pt**（Zhou et al., ICRA 2019）和**LazyLoc**代表轻量级方案，本文通过统一基准揭示了LazyLoc的运动平均与重投影优化带来的精度增益。
- **学习基回归方法**：**Reloc3r**和MASt3R变体代表端到端学习范式，本文通过严格对比揭示了其与经典几何方法之间的显著精度鸿沟（Table 1），表明当前回归模型尚未有效编码场景几何约束。

### 待验证的开放性局限

以下发现需在更广泛场景中进一步验证：
- 无结构方法在Aachen夜间场景中与Hloc仍存在约10个百分点的精度差距，夜间鲁棒性不足。
- 评估仅覆盖三个数据集（Aachen、Extended CMU Seasons、NAVER），在纯室外自然环境等场景类型上的泛化性未经验证。
- MASt3R深度尺度缺失的根本原因及修复方案仍是开放问题。



无结构视觉定位方法遵循一个统一的处理流程，其核心思想是用图像数据库替代预构建的3D模型来表示场景。该流程由四个串行模块构成，查询图像依次经过图像检索、特征提取与匹配、几何位姿估计，以及可选的位姿精化/全局对齐，最终输出6自由度相机位姿。

### 流程概览

**输入**：一张查询图像，以及一个由数据库图像组成的场景表示——每张数据库图像关联已知的相机内参和6自由度相机位姿（由离线SfM或SLAM获得）。

**模块1：图像检索**。使用图像级描述符从数据库中检索与查询图像视觉相似的top-k张候选图像。所有基线方法统一使用EigenPlaces学习型描述符，确保候选图像选择的一致性。检索结果决定了后续几何推理可用的数据库图像池。

**模块2：特征提取与匹配**。在查询图像与每张候选数据库图像之间建立2D-2D特征匹配。框架支持两类匹配范式：稀疏特征（SuperPoint或ALIKED关键点 + LightGlue匹配器）和稠密匹配器（RoMa或MASt3R）。稀疏方案输出离散的关键点对应，稠密方案输出半稠密或稠密的像素级对应关系。

**模块3：几何位姿估计**。这是整个流程的核心瓶颈所在。根据几何推理的深度和类型，方法分为四个族：

- **位姿三角化**（如Ess. mat. 5Pt、Ess. mat. 3Pt+depth、LazyLoc）：从2D-2D匹配中估计查询图像与各数据库图像之间的相对位姿，然后通过三角化或运动平均获得绝对位姿。
- **半广义相对位姿估计**（如E3+1、E5+1）：利用数据库图像的已知内参和位姿，将相对位姿估计问题降维，使用更少的点对应求解。
- **动态局部SfM + 绝对位姿估计**（Local triangulation - all / pairs）：在查询时刻动态地对检索到的数据库图像和查询图像进行局部三维重建，然后在该局部模型中估计查询位姿。
- **相对位姿回归**（如Reloc3r、MASt3R变体）：使用神经网络直接回归查询-数据库图像对的相对位姿，然后通过三角化获得绝对位姿。

**模块4：位姿精化/全局对齐**（可选）。部分方法包含后处理步骤：LazyLoc使用鲁棒运动平均和重投影优化精化位姿；MASt3R pose align使用Kabsch-Umeyama算法将局部重建与数据库图像位姿对齐。

**输出**：查询图像的6自由度绝对相机位姿（3自由度平移 + 3自由度旋转）。

### 核心权衡：几何推理深度 vs. 精度与效率

该框架揭示了一条清晰的因果链条：**几何推理越充分，定位精度越高，但计算成本也越大**。动态构建局部SfM模型（Local triangulation - all）达到最优精度，在Aachen日间场景（86.7/93.8/98.3 @ 0.25m,2°/0.5m,5°/5m,10°）与结构基方法MeshLoc持平（Table 7），但平均查询耗时约2.9秒，是最慢的方法。半广义相对位姿估计（E5+1）在Aachen日间达到78.4（0.25m,2°），远优于基础位姿三角化方法Ess. mat. 5Pt，同时保持了更低的计算开销，提供了最佳的精度-速度权衡。位姿三角化族中最快的LazyLoc仅需约101毫秒/查询，适合速度优先场景。

相对位姿回归方法（Reloc3r在Aachen日间仅5.2/14.2/63.0）的精度远低于经典几何方法，表明现有回归模型尚未有效编码场景几何约束，这是回归类方法面临的核心瓶颈。

### 场景依赖的特征选择

框架的另一关键发现是**没有一种特征类型在所有场景中一致最优**。RoMa稠密匹配器在室外数据集（Extended CMU Seasons、Aachen）上占优，MASt3R匹配器在室内数据集（NAVER）上表现更好。这意味着实际部署时需要根据目标场景类型进行特征选择，目前尚无通用的跨场景最优方案。



无结构视觉定位方法共享一个统一的四阶段流水线：图像检索 → 特征提取与匹配 → 几何位姿估计 → 可选的位姿优化/全局对齐。各方法族的核心差异集中在第三阶段——几何推理的深度与类型，这是决定定位精度与运行时间权衡的关键旋钮。

### 4.1 图像检索

所有基线方法均使用相同的图像级描述符 **EigenPlaces** 从数据库图像中检索 top-k 候选图像。该步骤为后续的 2D-2D 匹配和几何推理提供候选集，检索质量直接影响定位精度的上界。在 Aachen 和 Extended CMU Seasons 数据集上，默认检索 top-10 图像；在部分实验中扩展至 top-20 以探索检索数量对精度的影响（Table 7）。

### 4.2 特征提取与匹配

系统评估了四类特征匹配方案，覆盖稀疏与稠密两种范式：

- **稀疏特征 + 匹配器**：SuperPoint 或 ALIKED 提取关键点，LightGlue 进行匹配。
- **稠密匹配器**：RoMa（室外预训练模型）和 MASt3R matcher（立体匹配模型），直接输出像素级稠密对应。

关键发现：没有一种特征类型在所有场景中一致最优——RoMa 在室外数据集（Extended CMU Seasons、Aachen）通常占优，而 MASt3R matcher 在室内数据集（NAVER）表现更好（Figure 2, Figure 5）。对于基于稠密匹配器的局部三角化方法，形成特征轨迹（tracks）的距离阈值经网格搜索设为 5 px。

### 4.3 几何位姿估计：四个方法族

从 2D-2D 匹配到绝对相机位姿，存在四种几何推理范式，按推理深度递增排列：

#### 4.3.1 位姿三角化（Pose Triangulation）

**Ess. mat. (5Pt)**：对查询图像与每张检索到的数据库图像，使用 5 点算法在 RANSAC 框架内估计本质矩阵，分解得到相对位姿。随后对相对旋转进行平均，并通过多个相对平移方向三角化查询相机位置。这是推理深度最浅的基线方法。

**Ess. mat. (3Pt+depth)**：将 5 点求解器替换为 3 点求解器，利用单目深度预测为每个 2D-2D 匹配点对提供深度先验，从而在更少的匹配点条件下估计相对位姿。深度预测器可选 Metric3D v2（单目）或 MASt3R stereo（立体）。消融实验表明，深度预测器的选择对性能影响不显著，两者在多数场景中表现相近（Figure 3）。

**LazyLoc**：在位姿三角化基础上增加鲁棒的运动平均（rotation averaging 和 translation averaging，含外点剔除），随后进行查询位姿联合优化，是位姿三角化方法族中精度最高的变体，同时保持极低的运行时间（约 101 ms/查询，Table 2）。

#### 4.3.2 半广义相对位姿估计（Semi-Generalized Relative Pose）

**E5+1** 和 **E3+1**：此类方法利用数据库图像的已知绝对位姿，将查询-数据库图像对的相对位姿估计问题转化为半广义相对位姿估计——已知一个相机的绝对位姿，估计另一个相机的相对位姿。E5+1 使用 5 点求解器的广义变体，E3+1 使用 3 点求解器的广义变体（需深度先验）。与位姿三角化相比，半广义方法直接利用数据库图像的绝对位姿信息，减少了误差累积。E5+1 在 Aachen 日间场景达到 78.4% 的召回率（0.25m, 2°），显著优于 Ess. mat. (5Pt) 和 E3+1（Table 3），被论文认定为精度-速度权衡最优的方法。

#### 4.3.3 动态局部 SfM + 绝对位姿估计（SfM on the Fly）

**Local triangulation - all**：对所有检索到的数据库图像，在查询图像与数据库图像之间建立多视图特征轨迹（tracks），在 RANSAC 框架内对每个轨迹进行三维点三角化，构建局部 SfM 模型。随后使用 PnP 求解器从 2D-3D 对应中估计查询图像的绝对位姿。这是推理深度最深的方法，达到无结构方法的最优精度——在 Aachen 日间场景中与结构基方法 MeshLoc 持平（86.7 vs 85.9，0.25m, 2°，Table 7）。

**Local triangulation - pairs**：对每对数据库图像独立进行三角化和位姿估计，选择内点最多的位姿作为最终结果。精度通常低于 all 变体，且在 NAVER HDS 4F 场景中出现异常差的表现（原因待查，属于开放问题）。

#### 4.3.4 相对位姿回归（Relative Pose Regression）

**Reloc3r**：使用神经网络直接回归查询-数据库图像对之间的相对相机位姿，再通过位姿三角化获得绝对位姿。这是推理深度最浅的方法——完全依赖学习到的先验而非显式几何约束。在 Aachen 日间场景仅达到 5.2/14.2/63.0（0.25m, 2° / 0.5m, 5° / 5m, 10°），远低于所有基于几何的方法（Table 1），表明现有回归模型尚未有效编码场景几何约束。

**MASt3R depth + P3P**：利用 MASt3R 预测的深度图，结合 P3P 求解器估计位姿。该方法表现极差（Aachen 日间仅 0.1/1.1/37.7），根本原因在于 MASt3R 的深度回归器未能产生度量尺度的深度图——尽管训练目标是度量深度，实际使用时尺度偏差可达 15.83 倍（Figure 1 定性展示）。此外，MASt3R-based 方法存在结构性不公平劣势：无法利用已知的数据库图像内参和位姿进行三维重建阶段优化，而所有其他方法均利用了这些信息。

### 4.4 位姿优化与全局对齐

**LazyLoc 的优化链**：运动平均（鲁棒外点剔除）→ 重投影误差联合优化，这是位姿三角化方法族精度提升的关键。

**MASt3R pose align 的对齐**：对 MASt3R 预测的局部点云重建，使用 Kabsch-Umeyama 算法与数据库图像的三维坐标进行全局对齐，获得查询图像的绝对位姿。该方法同样受限于 MASt3R 的尺度不确定性。

### 4.5 核心权衡的形式化理解

无结构定位的精度的核心因果机制可概括为：几何推理深度与 2D-2D 匹配噪声的博弈。设 2D-2D 匹配的噪声水平为 $\sigma_m$，推理深度为 $d$（粗略地对应几何约束的利用程度），则位姿估计误差 $\epsilon$ 可概念性地表达为：

$$\epsilon \propto \frac{\sigma_m}{f(d)}$$

其中 $f(d)$ 是随推理深度单调递增的函数。位姿三角化（$d$ 最小）对匹配噪声最敏感；局部 SfM（$d$ 最大）通过多视图几何约束有效抑制噪声，但以运行时间为代价（约 2.9 秒/查询，Table 2）。半广义相对位姿估计（E5+1）在 $f(d)$ 和计算成本之间取得了最优平衡。

> **注意**：上述公式为概念性表达，论文未提供精确的误差传播模型。具体量化关系需手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l77_https_arxiv_org_abs_2504_17636/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of depth maps from different sources - on the top left is the source image. The corresponding source camera was used for the rendering of a mesh model (AC-14 model from MeshLoc [85]). The source image together with its focal length is the sole input into the Metric3D v2 [134, 51] monocular depth estimator. As MASt3R [132, 65] is a stereo model, it also uses a second image (shown in the bottom left) to predict the 3D geometry. MASt3R performs the prediction without any knowledge about the camera parameters. Both Metric3D and MASt3R depth maps were aligned (in scale and shift) to the mesh depth map for easier comparability, while they are used in their raw unscaled form in the expe...*



## 实验与关键发现

### 核心权衡：几何推理深度决定精度，场景更新灵活性是天然红利

本研究通过系统性地控制“几何推理程度”这一因果旋钮，揭示了无结构定位方法族内部的精度谱系。**更充分的显式几何推理一致地带来更高的定位精度**——构建动态局部SfM模型的方法（Local triangulation - all）达到最优结果，在Aachen日间场景中定位召回率86.7/93.8/98.3（0.25m,2°/0.5m,5°/5m,10°），与结构基方法MeshLoc（85.9/93.6/98.8）持平（Table 7）。该结果证实了核心洞察：当几何推理从简单的位姿三角化升级为完整的局部三维重建+绝对位姿估计时，2D-2D匹配噪声被更有效地滤除，精度逼近需要预构建全局3D模型的结构基方法。然而，这一精度优势以约2.9秒/查询的运行时间为代价（Table 2），在实时场景中需退而求其次。

![[assets/figures/papers/paper_list_l77_https_arxiv_org_abs_2504_17636/figures/010_Table_2.jpg]]
*Table 2: Average runtimes of the evaluated methods, measured on Aachen Day-Night v1.1 [140, 105, 106]. The experiments were performed on an Intel Core i7-9750H (2.60 GHz) CPU, using pre-computed SuperPoint [35] features matched by LightGlue [71]*

**半广义相对位姿估计（E5+1）提供了最佳的精度-速度权衡**。在Aachen日间场景中，E5+1达到78.4（0.25m,2°），相比基础5点法（Ess. mat. 5Pt）提升超过24个百分点，同时运行时间控制在可接受范围。LazyLoc以101ms/查询的速度成为速度优先场景下的良好替代方案，但精度有所折损。

### 特征类型的场景依赖性：没有银弹

消融实验揭示了一个关键发现：**没有一种特征类型在所有场景中表现最优**（Figure 2-5）。RoMa稠密匹配器在室外数据集（Extended CMU Seasons、Aachen）中通常占优，而MASt3R匹配器在室内数据集（NAVER系列）中表现更好。这一场景依赖性贯穿所有几何推理方法族，从基础的Ess. mat. 5Pt到最复杂的Local triangulation - all均成立。实际部署时需根据目标场景类型进行特征选择，目前不存在通用的“一劳永逸”方案。

![[assets/figures/papers/paper_list_l77_https_arxiv_org_abs_2504_17636/figures/002_Figure_2.jpg]]
*Figure 2: Localization results for the Ess. mat. (5Pt) approach for different features. We report localization recalls (higher is better) on the Y-axis at multiple pose thresholds (X-axis). For the outdoor scenes, the best results are obtained with the RoMa matcher. For the indoor scenes, the MASt3R matcher performs best for the coarser thresholds*

### 回归方法的系统性失败：几何约束编码不足

相对位姿回归方法（Reloc3r）在Aachen日间场景仅达到5.2/14.2/63.0的定位召回率（Table 1），远低于任何基于经典几何的方法。这一差距并非实现细节所致——即使是最简单的Ess. mat. 5Pt（使用MASt3R位姿）也达到了23.2/49.0/91.0。**失败根源在于现有回归模型未能有效编码场景几何约束**：Reloc3r直接从图像对回归相对位姿，缺少极线几何、三角化等显式约束，导致预测位姿在存在视觉模糊或低重叠度时迅速退化。

MASt3R-based方法的失败模式更为复杂。MASt3R depth + P3P方法在Aachen日间仅达0.1/1.1/37.7（Table 1），**根本原因并非P3P求解器本身，而是MASt3R深度图缺乏度量尺度**——尽管MASt3R的训练目标包含度量深度预测，实际使用时尺度偏差可达15.83倍（Figure 1定性对比）。此外，MASt3R-based方法存在不公平劣势：无法利用已知的数据库图像内参和位姿进行三维重建阶段优化，而所有其他方法均利用了这些信息。这解释了为何MASt3R pose align虽能构建局部点云，但精度仍落后于可访问内参的Local triangulation方法。

### 深度预测器选择：非关键因素

对于依赖深度图的Ess. mat. 3Pt+depth和E3+1方法，消融实验表明**深度预测器的选择（Metric3D v2 vs MASt3R stereo）对性能影响不显著**（Figure 3）。在大多数场景中，两种预测器表现相近。这一发现简化了系统设计：深度预测模块可灵活替换，无需针对特定场景精细调优。但需注意，此结论仅适用于将深度作为辅助信息的方法——当深度图被用作主要几何线索时（如MASt3R depth + P3P），尺度缺失问题会致命。

![[assets/figures/papers/paper_list_l77_https_arxiv_org_abs_2504_17636/figures/003_Figure_3.jpg]]
*Figure 3: Localization results for the Ess. mat. (3Pt + depth) approach for different features and monocular depth predictors. We report localization recalls (higher is better) on the Y-axis at multiple pose thresholds (X-axis). For most scenes, the choice of the depth predictor is not critical. For outdoor scenes, RoMa yields the best results. For indoor scenes, MASt3R leads to the highest pose accuracy in most cases*

### 室内场景的特殊挑战：重复纹理与复杂结构

在NAVER室内数据集中，Local triangulation - all虽保持最优（HDS 1F场景85.3/89.9/93.9，Table 6），但高误差查询图像的分析揭示了室内定位的瓶颈（Figure 9定性对比）：**高误差图像通常包含重复纹理或复杂结构，这些模式使三维点三角化变得困难**。室内场景的另一个异常是Local triangulation - pairs在HDS 4F场景中表现异常差，其原因尚待进一步调查。

![[assets/figures/papers/paper_list_l77_https_arxiv_org_abs_2504_17636/figures/014_Table_6.jpg]]
*Table 6: Benchmark on NAVER indoor localization datasets [64] Hyundai Department Store (HDS) scenes. We use the top 10 images retrieved using the EigenPlaces [14] image-level descriptor. We report localization recalls (higher is better) at the pose thresholds of (0.1m, 1°) / (0.25m, 2°) / (1m, 5°)*

### 夜间场景：无结构方法的阿喀琉斯之踵

尽管在日间场景中无结构方法可与结构基方法媲美，**Aachen夜间场景中仍存在约10个百分点的精度差距**（Table 3 vs Table 7中Hloc夜间结果）。夜间条件下，图像检索质量下降、2D-2D匹配内点率降低，这些因素在缺少全局3D模型作为先验时被放大。缩小这一差距是无结构方法走向全天候部署的关键开放问题。

![[assets/figures/papers/paper_list_l77_https_arxiv_org_abs_2504_17636/figures/011_Table_3.jpg]]
*Table 3: The best performing setup (matching method and depth map source) for each method evaluated on Aachen Day-Night v1.1 [140, 105, 106]. We use the top 10 images retrieved using the EigenPlaces [14] image-level descriptor. We report localization recalls (higher is better) at pose thresholds of (0.25m, 2°) / (0.5m, 5°) / (5m, 10°)*

### 运行时分析：精度与效率的帕累托前沿

Table 2揭示了方法族间的运行时跨度：LazyLoc（101ms）到Local triangulation - all（2909ms），差距达28.7倍。所有测量基于相同硬件（Intel Core i7-9750H CPU）和预计算SuperPoint特征+LightGlue匹配器，确保对比公平。E5+1在精度-速度帕累托前沿上占据优势位置，适合大多数实际部署场景。

### 补充图表

![[assets/figures/papers/paper_list_l77_https_arxiv_org_abs_2504_17636/figures/004_Figure_4.jpg]]
*Figure 4: LazyLoc localization results for different features. We report localization recalls (higher is better) on the Y-axis at multiple pose thresholds (X-axis). There is no type of feature that performs best in all scenes. However, the MASt3R matcher performs well in general*

![[assets/figures/papers/paper_list_l77_https_arxiv_org_abs_2504_17636/figures/006_Figure_5.jpg]]
*Figure 5: E5+1 localization results for different features. We report localization recalls (higher is better) on the Y-axis at multiple pose thresholds (X-axis). For the outdoor scenes, the best results are typically obtained with the RoMa matcher. For the indoor scenes, the MASt3R matcher performs best for the coarser thresholds*

![[assets/figures/papers/paper_list_l77_https_arxiv_org_abs_2504_17636/figures/007_Figure_6.jpg]]
*Figure 6: E3+1 localization results for different features and depth predictors. We report localization recalls (higher is better) on the Y-axis at multiple pose thresholds (X-axis). The choice of the depth predictor is not critical*

![[assets/figures/papers/paper_list_l77_https_arxiv_org_abs_2504_17636/figures/008_Figure_7.jpg]]
*Figure 7: Localization results for the local 3D point triangulation from all retrieved images (Local triangulation - all) for different features. We report localization recalls (higher is better) on the Y-axis at multiple pose thresholds (X-axis)*

![[assets/figures/papers/paper_list_l77_https_arxiv_org_abs_2504_17636/figures/012_Table_4.jpg]]
*Table 4: The best performing setup (matching method and depth map source) for each method. Evaluated on Extended CMU Seasons [105, 10]. We use the top 10 images retrieved using the EigenPlaces [14] image-level descriptor. We report localization recalls (higher is better) at the pose thresholds of (0.25m, 2°) / (0.5m, 5°) / (5m, 10°)*

![[assets/figures/papers/paper_list_l77_https_arxiv_org_abs_2504_17636/figures/016_Figure_9.jpg]]
*Figure 9: Comparison of the query images with high camera position error (top row) and the images with low camera position error (bottom row) in NAVER indoor localization dataset [64] COEX 1F scene. The former often contain repetitive patterns or other structures that complicate 3D point triangulation*



## 定位与知识库关联

### 问题定义与范式定位

无结构视觉定位（Structureless Visual Localization）代表场景表示方式的一个根本性范式选择：场景不通过预构建的3D模型（如SfM点云或Mesh）表示，而是仅维护一个图像数据库，每张数据库图像关联其相机位姿和内参。给定查询图像，系统首先通过图像检索识别一组相关数据库图像，然后估计查询相机相对于这些检索图像的位姿。这一范式与主流的**结构基方法**（Structure-based methods）形成直接对比，后者需要预先构建全局3D地图，并在定位时建立2D-3D匹配。

从知识库定位角度看，本文并非提出单一新方法，而是对无结构定位这一方法家族进行了首次系统性基准评估。研究覆盖了四个几何推理深度递增的方法族，构成一个完整的无结构定位方法谱系。

### 方法谱系：几何推理深度的四层递进

本文评估的四类方法按几何推理深度从浅到深排列，揭示了精度与推理充分性之间的因果链条：

#### 第一层：相对位姿回归（Relative Pose Regression）
这是几何推理最浅的层级，完全依赖学习模型直接从图像对预测相对位姿。代表方法包括：
- **Reloc3r**：使用神经网络预测查询-数据库图像对之间的相对相机位姿，然后通过位姿三角化获得绝对位姿。
- **MASt3R depth + P3P**：利用MASt3R稠密匹配器预测的深度图，结合P3P求解器估计位姿。

这一层级的方法在Aachen日间场景中表现极差——Reloc3r仅达到5.2/14.2/63.0（0.25m,2°/0.5m,5°/5m,10°），MASt3R depth + P3P更差至0.1/1.1/37.7。核心失败原因在于：MASt3R虽然训练目标是度量深度，但实际无法产生度量尺度的深度图（尺度偏差可达15.83倍），而回归模型尚未有效编码场景几何约束。

#### 第二层：位姿三角化（Pose Triangulation）
这一层级通过两视图几何估计相对位姿，再进行三角化获得查询位姿。代表方法包括：
- **Ess. mat. (5Pt)**（Zhou et al., ICRA 2019）：使用5点算法在RANSAC框架内计算本质矩阵，平均相对旋转后三角化相机位置。
- **Ess. mat. (3Pt+depth)**：使用3点求解器替代5点求解器，引入单目深度预测以降低所需匹配点数。
- **LazyLoc**：在位姿三角化基础上增加鲁棒运动平均（含外点剔除）和查询位姿联合优化，显著提升精度。

#### 第三层：半广义相对位姿估计（Semi-Generalized Relative Pose Estimation）
这一层级利用数据库图像的已知内参和位姿约束相对位姿估计。代表方法为：
- **E5+1** 和 **E3+1**：分别在5点和3点求解器中引入数据库图像的已知信息，将相对位姿估计转化为半广义问题。E5+1在Aachen日间/夜间分别达到78.4/65.4（0.25m,2°），远优于Ess. mat. (5Pt)的54.2，体现了已知约束对几何推理质量的提升。

#### 第四层：动态局部SfM + 绝对位姿估计（SfM on the Fly）
这是几何推理最充分的层级，在查询时刻动态构建局部SfM模型。代表方法为：
- **Local triangulation - all**：使用所有检索到的数据库图像进行三角化，对每个特征轨迹在RANSAC内执行三角化，构建局部3D点云后估计查询位姿。
- **Local triangulation - pairs**：考虑数据库图像对进行三角化和位姿估计，对每对候选图像独立处理。

这一层级达到最优精度——Local triangulation - all在Aachen日间达到86.7/93.8/98.3，与结构基方法**MeshLoc**（Panek et al., ECCV 2022）的85.9/93.6/98.8持平，仅比**Hloc**（Sarlin et al., CVPR 2019）的88.1/95.4/99.0低约1-2个百分点。

### 与结构基方法的关系与适用边界

无结构方法的核心优势在于场景更新灵活性——增删数据库图像即可实现场景更新，无需重新构建全局3D模型。在日间场景中，最优无结构方法（Local triangulation - all）的精度已与结构基SOTA方法可比。然而，在Aachen夜间场景中，无结构方法与Hloc仍存在约10个百分点的精度差距，夜间条件下的鲁棒性不足。

**MASt3R-based方法**（MASt3R pose align、MASt3R depth + P3P）存在结构性不公平劣势：无法利用已知的数据库图像内参和位姿进行三维重建阶段优化，而所有其他方法均利用了这些信息。这解释了为什么基于MASt3R的方法在精度上显著落后。

### 精度-速度权衡空间

各方法在运行时间上差异巨大（Table 2，均基于预计算SuperPoint特征+LightGlue匹配器，Intel Core i7-9750H CPU）：
- **LazyLoc**：101.33 ms/查询（最快），适合速度优先场景
- **E5+1**：提供最佳的精度-速度权衡
- **Local triangulation - all**：2908.96 ms/查询（最慢），仅适合离线或精度优先场景

### 特征选择的场景依赖性

消融实验揭示了特征类型选择的场景依赖性，没有一种特征类型在所有场景中表现最优：
- **RoMa稠密匹配器**在室外数据集（Extended CMU Seasons、Aachen）中通常表现最优
- **MASt3R匹配器**在室内数据集（NAVER）中通常表现更好
- 深度预测器选择（Metric3D v2 vs MASt3R stereo）对Ess. mat. (3Pt+depth)和E3+1方法的性能影响不显著

### 局限与开放问题

**已知局限**：
1. 评估仅限于三个数据集（Aachen、Extended CMU Seasons、NAVER），在其他场景类型（如纯室外自然环境）上的泛化性未经验证
2. Local triangulation - all的运行时间（约2.9秒/查询）限制了实时部署
3. 相对位姿回归方法的精度远低于经典几何方法，MASt3R深度图缺乏度量尺度是主要失败原因
4. 实际部署时需针对场景类型进行特征选择，增加了工程复杂度

**开放问题**：
1. 无结构方法能否在Aachen夜间场景中缩小与Hloc约10个百分点的差距？
2. MASt3R为何在训练目标是度量深度的情况下无法产生度量尺度的深度图？如何修复？
3. 如何利用已知相机内参和数据库位姿来改进MASt3R的重建过程？
4. 能否设计一种特征类型在室内和室外场景中均表现优异？
5. 如何自动判断何时使用单目深度图预测以提升3点求解器在低内点率场景下的性能？
6. Local triangulation - pairs在HDS 4F场景中表现异常差的原因是什么？
7. 如何提高相对位姿回归方法的精度使其达到与经典几何方法可比的水平？



## 原文 PDF

![[paperPDFs/arxiv_2025/A_Guide_to_Structureless_Visual_Localization.pdf]]
