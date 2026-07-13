---
title: "UrbanGS: Efficient and Scalable Architecture for Geometrically Accurate Large-Scene Reconstruction"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/UrbanGS_Efficient_and_Scalable_Architecture_for_Geometrically_Accurate_Large_Sce_dbeb8df34f9e.pdf
project_link: null
code_link: null
aliases:
- UrbanGS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过“深度一致性 D-Normal 正则化”实现对高斯参数（位置、旋转）的完整更新，同时利用“空间自适应高斯修剪 (SAGP)”根据局部几何复杂度动态控制高斯密度，从根本上调和几何精度、内存效率与扩展性。
primary_logic: 从渲染深度图导出的 D-Normal 约束天然与位置梯度关联，使优化可同时校正法向与位置；配合基于梯度一致性和逆深度偏差的自适应置信度加权，该范式在不牺牲质量的前提下大幅压缩冗余高斯，从而在城市场景中同时获得高保真渲染与精确几何。
claims:
- D-Normal 正则化使得高斯位置参数能够沿法向更新，而传统渲染法向监督无法有效移动位置。
- 自适应置信度项结合梯度方向一致性和逆深度偏差，显著提升多视图深度对齐鲁棒性。
- SAGP 在减少高斯数量、训练时间和显存的同时保持了更高的几何质量 (F1 分数)。
- Mill19 (Building) 上 PSNR ↑ = 22.82 (Ours)
---

# UrbanGS: Efficient and Scalable Architecture for Geometrically Accurate Large-Scene Reconstruction

> [!tip] 核心洞察
> 从渲染深度图导出的 D-Normal 约束天然与位置梯度关联，使优化可同时校正法向与位置；配合基于梯度一致性和逆深度偏差的自适应置信度加权，该范式在不牺牲质量的前提下大幅压缩冗余高斯，从而在城市场景中同时获得高保真渲染与精确几何。

| 字段 | 内容 |
|------|------|
| 中文题名 | UrbanGS：面向几何精确大场景重建的高效可扩展架构 |
| 英文题名 | UrbanGS: Efficient and Scalable Architecture for Geometrically Accurate Large-Scene Reconstruction |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=L3utaw6SD9) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | UrbanGS |
| Dataset | Mill19, UrbanScene3D, GauU-Scene |

> [!tip] 效果简介
> - Mill19 (Building) 上，PSNR ↑ 22.82 (Ours) vs 21.55 (CityGaussian) (+1.27)。
> - Mill19 (Rubble) 上，PSNR ↑ 26.25 (Ours) vs 23.75 (CityGaussianV2) (+2.50)。
> - UrbanScene3D (Residence) 上，SSIM ↑ 0.823 (Ours) vs 0.769 (CityGaussianV2) (+0.054)。

## 概要

将 3D Gaussian Splatting (3DGS) 从物体/房间级场景推向城市级大场景重建时，面临三重瓶颈：**几何一致性差**（表面浮空、深度对齐失效）、**内存膨胀**（高斯点数量随场景规模爆炸）以及**计算可扩展性不足**（训练成本剧增）。UrbanGS 针对这些瓶颈提出了一套统一框架，其核心因果机制在于两点：

1. **深度一致性 D‑Normal 正则化**：传统法向监督仅能更新高斯旋转参数，而 UrbanGS 从渲染深度图的空间梯度导出 D‑Normal，并利用伪法向先验进行监督，使得优化过程能够**同时校正高斯的位置与旋转**。配合基于梯度方向一致性和逆深度偏差的自适应置信度加权，该正则化在多视图间实现了鲁棒的几何对齐。

2. **空间自适应高斯修剪 (SAGP)**：在局部体素内联合光线相交频率、不透明度和次线性体积权重，计算每个高斯的重要性分数并动态移除冗余点。SAGP 根据局部几何复杂度自适应控制密度，在**压缩约 24% 高斯数量**的同时，保持了更高的几何 F1 分数。

在方法谱系中，UrbanGS 属于**分块式大规模 3DGS 方法**，与 **VastGaussian** (Lin et al., 2024)、**CityGaussian** (Liu et al., 2024a)、**CityGaussianV2** (Liu et al., 2024b) 等共享“分块–并行优化–合并”范式，但其关键差异在于：(a) 分块前先通过 SAGP 进行全局预剪枝以降低各子块的计算与内存压力；(b) 子块优化中引入了统一的深度‑法向正则化，使几何质量显著超越仅依赖渲染法向监督或简单单目深度约束的方法（如 **VCR-Gaus** (Chen et al., 2024b)、**2DGS** (Huang et al., 2024a) 等）。

主要实验结果验证了上述设计的有效性：

- **新视角合成**：在 Mill19 和 UrbanScene3D 数据集上，UrbanGS 的 PSNR 较 CityGaussianV2 在 Rubble 场景提升 +2.50 dB，在 Building 场景较 CityGaussian 提升 +1.27 dB（Table 1）。
- **几何精度**：在 GauU-Scene 数据集上，F1 分数较 CityGaussianV2 在 Residence 场景提升 +0.026，在 Russian Building 场景提升 +0.009（Table 2–3）。
- **效率**：在 Rubble 场景上，训练时间仅约 2 小时 10 分钟，而对比方法普遍超过 4 小时（Figure 5），且 UrbanGS 可在 8 块 RTX A5000 GPU 上完成训练，而 VCR-Gaus 在同配置下因显存不足失败。

消融实验进一步证实：移除 D‑Normal 正则化导致 F1 从 0.503 降至 0.453、PSNR 从 26.44 降至 24.59（Table 5）；采用 SAGP 替代传统全局阈值修剪，在减少高斯数量的同时 F1 分数更高（0.546 vs 0.518，Table 4）。

**局限性**方面，该方法依赖预训练单目深度/法向估计器提供伪先验，在弱纹理或极端光照区域可能引入错误；框架当前面向静态场景，未显式建模动态物体；在远距离天空等缺乏明确几何结构的区域，显式几何优化可能导致渲染质量略逊于原始 3DGS。



### 城市级场景重建的范式迁移与瓶颈

大规模城市场景的逼真数字化是数字孪生、自动驾驶仿真和城市规划等领域的核心需求。近年来，**3D Gaussian Splatting (3DGS)**（Kerbl et al., 2023）以其显式点云表示和实时可微光栅化渲染，在场景重建与新颖视图合成任务中展现出巨大潜力。然而，当 3DGS 从物体级或房间级场景扩展至城市级大场景时，其原始框架暴露出三个相互纠缠的根本性瓶颈：

1. **几何一致性差**：原始 3DGS 的优化目标以光度损失为主导，缺乏显式的多视图几何约束。这导致重建结果中出现大量**表面浮空伪影**（floating artifacts），高斯椭球体未能收敛到真实表面，深度图呈现碎片化、不平滑的状态。
2. **内存膨胀**：城市级场景需要数百万乃至上千万个高斯原语来覆盖广阔的几何与纹理细节。每个高斯原语携带位置、协方差、颜色和不透明度等参数，直接导致显存占用急剧膨胀，甚至超出消费级 GPU 的容量极限。
3. **计算可扩展性不足**：全场景联合优化面临巨大的计算开销，训练时间随场景规模呈超线性增长。分块训练策略虽然缓解了单卡压力，但粗粒度的分块与视点分配方案容易引入块间不一致性和冗余计算。

### 现有方法的局限

为应对上述挑战，学术界已提出多种改进方案，但各自存在明显的功能缺口：

- **分块式大场景 3DGS 方法**（如 **VastGaussian**（Lin et al., 2024）、**CityGaussian**（Liu et al., 2024a）、**CityGaussianV2**（Liu et al., 2024b））通过空间分区实现并行训练，有效降低了单卡显存压力。然而，这些方法的**分块策略相对粗糙**：CityGS 采用简单的方形分区，未考虑局部几何复杂度差异；视点分配仅依赖空间包含关系，忽略了感知质量准则，导致部分子块被分配低贡献视图，造成计算浪费。更关键的是，分块训练前**缺乏对全局冗余高斯的预清理**，使得大量低质量高斯原语被复制到各子块中，放大了计算负担。

- **几何正则化方法**（如 **VCR-Gaus**（Chen et al., 2024b）、**2DGS**（Huang et al., 2024a））尝试引入法向或深度监督来改善几何质量。但它们存在一个**根本性的参数更新盲区**：传统方案直接使用预训练单目模型估计的渲染法向进行监督，其梯度流**仅能更新高斯的旋转参数**，无法有效驱动位置参数沿法向移动。这意味着即使法向预测正确，高斯椭球体的空间位置仍可能偏离真实表面，几何优化是不完整的。此外，简单的全局深度损失忽略了不同区域的估计置信度差异，在弱纹理或边缘区域容易引入误导性监督。

- **高斯修剪策略**普遍采用基于全局不透明度阈值或固定百分比的统一裁剪方式。这种“一刀切”的策略**无法感知局部几何复杂度**：在平面区域可能保留过多冗余高斯，而在几何细节丰富区域又可能过度修剪，导致细节丢失。修剪后的模型往往需要在压缩率和几何质量之间做出非此即彼的取舍。

### 本文动机

上述分析揭示了一个清晰的因果链条：**几何精度、内存效率和计算可扩展性之间的矛盾**，根源于现有方法在参数更新完备性、密度控制自适应性和分块策略智能性三个维度上的结构性缺陷。具体而言：

- **法向监督的梯度流不完整**，导致几何优化无法同时校正位置与朝向；
- **深度监督缺乏置信度感知**，使得多视图几何对齐的鲁棒性不足；
- **高斯修剪与分块策略未考虑局部几何先验**，造成资源分配的低效。

UrbanGS 正是针对这三个维度进行系统性重构：通过**深度一致性 D-Normal 正则化**实现位置与旋转的完备联合优化，通过**空间自适应高斯修剪 (SAGP)** 实现几何感知的密度控制，通过**预剪枝与契约分块策略**实现高效可扩展的并行训练。这三项设计的有机耦合，使得 UrbanGS 能够在消费级 GPU 上完成城市级场景的高保真渲染与精确几何重建，从根本上调和了质量、效率与扩展性的三角矛盾。



## 核心方法与创新机理

UrbanGS 针对 3DGS 在大规模城市场景中几何一致性差、内存膨胀和计算扩展性不足三大瓶颈，提出了三个相互耦合的核心创新：**深度一致性 D-Normal 正则化**、**空间自适应高斯修剪 (SAGP)** 和**预剪枝契约分块策略**。这三者形成“几何优化—密度控制—规模扩展”的闭环：D-Normal 正则化从根本上解决高斯位置参数的几何更新问题，SAGP 在保持几何精度的前提下大幅压缩冗余高斯，而预剪枝分块策略则将前两者的收益传递到城市级场景的并行训练中。

### 创新一：深度一致性 D-Normal 正则化

这是 UrbanGS 最根本的方法创新，直接回应了“传统渲染法向监督无法有效移动高斯位置”这一关键瓶颈。

**问题根源**：现有方法（如 VCR-Gaus）直接使用预训练模型估计的渲染法向进行监督。这种监督方式只能约束高斯的旋转参数（即协方差矩阵中的 $R$），却无法对高斯中心位置 $\boldsymbol{u}_i$ 产生有效的梯度更新。在城市级场景中，位置偏差是导致表面浮空、深度对齐失效的主要原因。

**UrbanGS 的解法**：不直接监督渲染法向，而是从渲染深度图的空间梯度推导出 **D-Normal**（深度法向），再用伪法向先验监督 D-Normal。D-Normal 的定义为：

$$\overline{N}_d(n,p) = \frac{\nabla_v d(n,p) \times \nabla_h d(n,p)}{\| \nabla_v d \times \nabla_h d \|}$$

其核心机制在于：D-Normal 天然与深度图的梯度场关联，而深度图的渲染过程直接依赖于高斯的位置参数。因此，对 D-Normal 施加损失会通过反向传播产生对位置 $\boldsymbol{u}_i$ 的梯度，使得优化过程可以**同时校正法向和位置**，实现“整体几何优化”（holistic geometric optimization）。

**自适应置信度加权**：为增强多视图深度对齐的鲁棒性，UrbanGS 引入了一个几何感知的置信度度量 $w_d$：

$$w_d = \exp\left( \frac{\cos \phi - 1}{0.01} \right) \cdot \exp\left( -\frac{\epsilon_d}{0.1} \right)$$

该置信度联合了两个几何线索：渲染深度梯度与外部伪深度梯度的余弦相似度 $\cos \phi$（衡量局部表面朝向一致性），以及归一化逆深度偏差 $\epsilon_d$（衡量深度误差敏感度）。在弱纹理或深度估计不可靠区域，$w_d$ 自动降低监督强度，避免错误先验传播。这一设计使得深度一致性框架在复杂城市场景中具有显著的鲁棒性优势。

**消融验证**：移除 D-Normal 正则化（仅保留传统渲染法向监督）导致 F1 分数从 0.503 降至 0.453，PSNR 从 26.44 降至 24.59（Table 5），证实了 D-Normal 对几何精度和渲染质量的双重贡献。

### 创新二：空间自适应高斯修剪 (SAGP)

传统高斯修剪策略（如基于全局不透明度阈值或固定阈值）采用“一刀切”的方式，容易在平坦区域保留过多高斯，而在几何复杂区域误删关键细节。SAGP 的核心思想是：**根据局部几何复杂度动态决定哪些高斯应当被保留**。

**局部体素内的自适应评估**：SAGP 在局部体素单元内操作，为每个高斯计算一个复合重要性分数：

$$S_i = \phi_i \cdot \tau_i \cdot w_{v,i}$$

其中 $\phi_i$ 是归一化光线相交频率（反映该高斯被多少视角“看到”），$\tau_i$ 是通过 sigmoid 映射的不透明度，$w_{v,i}$ 是次线性体积权重。**次线性体积权重的设计是关键**：它抑制了大体积但低贡献的高斯（如天空区域的漂浮高斯），同时保护了小体积但几何关键的高斯（如建筑边缘的细节高斯）。

**与全局修剪的本质区别**：全局阈值修剪仅依赖单一的不透明度信号，无法区分“高不透明度但几何冗余”和“低不透明度但结构关键”的高斯。SAGP 通过三维度联合评估，在移除冗余的同时保持了几何完整性。

**消融验证**：采用 SAGP 相比传统全局阈值修剪，高斯数量减少约 24%，同时 F1 分数更高（0.546 vs 0.518）（Table 4）。移除空间自适应权重中的次线性指数导致所有指标下降（Table F），验证了次线性压缩对细节保护的重要性。

### 创新三：预剪枝契约分块策略

将 3DGS 扩展至城市级场景时，分块训练是必要的，但直接分块会带来两个问题：粗模型中的冗余高斯会吸引非贡献视角，放大计算负担；块边界处的高斯断裂导致融合伪影。

**SAGP 预剪枝**：在全局粗模型上先执行 SAGP，消除冗余高斯后再进行场景分块。这防止了冗余高斯在分块训练中被各子块重复优化，显著降低了训练时间和显存。消融实验显示，移除预剪枝步骤导致高斯数增加 23%，训练时间变长且显存升高（Table G）。

**边界高斯复制**：在分块阶段，子块边界处的公共高斯被复制到相邻块中，确保块间几何连续性，消除融合接缝。

**几何感知的视点分配**：不同于 CityGS 的简单视点分配，UrbanGS 结合几何包含关系和 SSIM 感知准则为每个子块分配相关视图，减少无效计算。

### 创新间的协同关系

三个创新并非孤立存在，而是形成了紧密的因果链：

1. **D-Normal 正则化**提供精确的几何优化信号，使得高斯的位置和旋转都能被正确更新；
2. 精确的几何使得 **SAGP** 的重要性评估更加可靠——几何正确的区域不会因误判而被过度修剪；
3. **SAGP 预剪枝**大幅压缩了粗模型，使得后续的分块训练在更低的计算和内存预算下运行；
4. 分块训练中继续施加 D-Normal 正则化，确保各子块的几何质量不因独立优化而退化。

这一闭环使得 UrbanGS 在 Mill19 Rubble 场景上仅需 2h10min 训练时间（baseline 方法超过 4 小时），同时在 PSNR 上领先 CityGaussianV2 达 +2.50 dB（Table 1），在 GauU-Scene 的 Residence 场景上 F1 达到 0.493（Table 2），实现了效率与质量的双重突破。



UrbanGS 的整体流水线遵循“全局粗建模 → 几何感知压缩 → 分块并行精化 → 融合”的四阶段范式，旨在以可扩展的方式从多视图 RGB 图像重建几何精确的大规模城市场景。其核心设计思想在于：**在分块训练之前，先通过空间自适应高斯修剪 (SAGP) 消除冗余高斯基元，再以深度一致性 D-Normal 正则化对每个子块进行联合几何优化**，从而在内存、计算效率与几何/渲染质量之间取得平衡。

### 流水线概览

Figure 2 (a) 完整呈现了 UrbanGS 的训练流水线，主要包含以下模块：

![[assets/figures/papers/paper_list_l64_https_openreview_net_forum_id_L3utaw6SD9/figures/002_Figure_2.jpg]]
*Figure 2: UrbanGS training pipeline and core components. (a) Training Pipeline: Starting from coarse global Gaussians, we apply spatially adaptive Gaussian pruning to obtain compact priors, contract and partition the scene into blocks, assign camera views using geometric and SSIM-based criteria, and refine all blocks in parallel before merging them into a unified large-scale 3D Gaussian scene. (b) Depth-Consistent D-Normal Regularization: 3D Gaussians are rendered to depth and normal maps, depth is converted to D-normals and jointly supervised with pseudo-depth and pseudonormal priors from pretrained models via the loss*

1. **全局粗高斯初始化**
   利用所有输入视图与 COLMAP 估计的相机位姿，训练一个覆盖全场景的粗粒度 3DGS 模型。该模型为后续所有操作提供初始几何与外观先验。

2. **空间自适应高斯修剪 (SAGP)**
   在粗模型上执行 SAGP（详见 Section 3.3），根据局部几何复杂度、光线相交频率和可见性感知的重要性分数，动态移除对场景表达贡献低的高斯基元。这一步在分块前大幅压缩模型规模，避免冗余高斯在后续子块训练中吸引无效视图并放大计算开销。

3. **场景收缩与分块**
   借鉴 CityGS 的分块思想并加以改进：首先对经 SAGP 修剪后的高斯场进行坐标收缩，随后将场景划分为可并行训练的子块。关键改进在于**边界高斯复制策略**——每个子块的边界处保留公共高斯基元，以消除块间几何不连续导致的融合伪影。

4. **相机视点分配**
   为每个子块分配相关视图时，联合考虑几何包含关系（高斯是否落在视锥内）与 SSIM 感知质量准则，确保每个子块只接收对其优化有实质贡献的视图，减少无效计算。

5. **并行分块优化**
   各子块独立进行高斯参数微调，优化过程中统一施加**深度一致性 D-Normal 正则化损失**（详见 Section 3.2）。该损失由三部分构成：RGB 渲染损失、D-Normal 损失（从渲染深度图推导的法向约束）以及自适应加权的逆深度损失，三者联合驱动高斯的位置、旋转、不透明度等全部几何参数的更新。

6. **块合并**
   所有子块优化完成后，将其高斯基元合并为统一的大场景高斯场，用于最终的新视角渲染与表面重建。

### 核心模块间的因果关联

流水线中两个关键模块——**SAGP 预剪枝**与**深度一致性 D-Normal 正则化**——之间存在因果协同关系：

- **SAGP 为深度正则化创造稀疏而准确的初始几何**：在分块前去除浮空和低贡献高斯，使后续 D-Normal 约束能够作用于真正承载场景结构的高斯基元，避免梯度被噪声高斯分散。
- **D-Normal 正则化为 SAGP 提供更可靠的几何信号**：通过从渲染深度图反投影计算 D-Normal 并施加伪法向先验监督，该正则化使得高斯位置能够沿法向方向更新（传统渲染法向监督仅能更新旋转参数），从而在优化过程中主动修正位置偏差。这种位置修正能力使得 SAGP 的局部几何重要性评估更加准确，形成正向反馈。

### 输入输出规范

- **输入**：多视图 RGB 图像 + COLMAP 估计的相机内/外参 + 预训练单目模型预测的伪深度图与伪法向图（作为几何先验）。
- **输出**：统一的大场景 3D 高斯场，可直接用于新视角 RGB 渲染、深度图渲染及表面 mesh 提取（通过 screened Poisson 重建）。

> **注意**：伪深度/法向先验的质量直接影响 D-Normal 正则化的有效性，在弱纹理或极端光照区域可能引入系统性偏差，这一点需在应用中加以留意。



UrbanGS 的核心架构围绕两个关键设计展开：**深度一致性 D-Normal 正则化** 和 **空间自适应高斯修剪 (SAGP)**，二者共同解决了 3DGS 在大场景中的几何退化与内存膨胀问题。

### 3D 高斯表示基础

UrbanGS 沿用 3DGS 的场景表示范式，将场景建模为一组各向异性的 3D 高斯椭球。每个高斯单元 $G_i(\boldsymbol{p})$ 的空间分布由均值 $\boldsymbol{u}_i$ 和协方差矩阵 $\Sigma_i$ 定义：

$$G_i(\boldsymbol{p}) = \exp\left\{ -\frac{1}{2} (\boldsymbol{p} - \boldsymbol{u}_i)^\top \Sigma_i^{-1} (\boldsymbol{p} - \boldsymbol{u}_i) \right\}$$

为保证协方差矩阵的半正定性，$\Sigma_i$ 被分解为旋转矩阵 $R$ 和对角缩放矩阵 $S$ 的乘积形式：

$$\Sigma_i = R S S^\top R^\top$$

这一分解使得优化过程可以直接更新旋转与缩放参数，为后续的几何正则化提供了参数基础。

### 深度一致性 D-Normal 正则化

这是 UrbanGS 最核心的创新模块，直接针对传统法向监督的关键缺陷：**监督渲染法向只能更新旋转参数，无法有效移动高斯位置**。UrbanGS 的解决方案是从渲染深度图推导 D-Normal，从而建立位置梯度与法向约束之间的桥梁。

**D-Normal 的定义**：给定渲染深度图 $d(n,p)$，首先通过反投影获得 3D 点云，然后利用有限差分计算空间梯度，其叉积给出深度法向：

$$\overline{N}_d(n,p) = \frac{\nabla_v d(n,p) \times \nabla_h d(n,p)}{\| \nabla_v d \times \nabla_h d \|}$$

由于 D-Normal 是从深度图的空间梯度计算而来，其优化信号天然与高斯的位置参数相关联，使得优化过程可以**同时更新位置和旋转参数**，而传统渲染法向监督无法做到这一点。

**逆深度损失**：为平衡远近景的优化敏感性，UrbanGS 在倒数深度域构建约束：

$$\mathcal{L}_{\mathrm{id}}(u,v) = \Big| \hat{D}^{-1}(u,v) - D_{\mathrm{ext}}^{-1}(u,v) \Big|$$

其中 $\hat{D}^{-1}$ 为渲染深度的倒数，$D_{\mathrm{ext}}^{-1}$ 为外部单目深度估计器提供的伪深度倒数。在逆深度空间中，远景区域的小绝对误差不会因距离而被过度放大，从而避免了优化偏差。

**自适应几何置信度**：单目深度估计在不同区域可靠性差异显著，UrbanGS 引入统一置信度 $w_d$ 来动态调节监督强度。该置信度融合两个几何线索：

1. **深度梯度方向一致性**：计算渲染深度梯度 $\boldsymbol{\nabla} \hat{D}$ 与外部深度梯度 $\boldsymbol{\nabla} D_{\mathrm{ext}}$ 的余弦相似度 $\cos \phi$，衡量局部表面朝向的一致性。
2. **逆深度偏差**：通过归一化逆深度偏差 $\epsilon_d$ 衡量深度估计的误差敏感度。

最终置信度以高斯函数形式组合：

$$w_d = \exp\left( \frac{\cos \phi - 1}{0.01} \right) \cdot \exp\left( -\frac{\epsilon_d}{0.1} \right)$$

当梯度方向一致且逆深度偏差小时，$w_d$ 趋近于 1，深度监督强度最大；反之则自动抑制不可靠区域的约束，增强多视图几何对齐的鲁棒性。

**联合损失函数**：UrbanGS 的总优化目标整合了 RGB 渲染损失、法向损失、D-Normal 损失和自适应加权逆深度损失：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{RGB}} + \lambda_1 \mathcal{L}_{\mathrm{n}} + \lambda_2 \mathcal{L}_{\mathrm{dn}} + \lambda_3 (w_d \cdot \mathcal{L}_{\mathrm{id}})$$

### 空间自适应高斯修剪 (SAGP)

大场景中大量高斯位于低纹理或遮挡区域，对渲染贡献极小却消耗大量内存。SAGP 在局部体素内评估每个高斯的几何重要性，实现**密度感知**的冗余去除。

SAGP 为每个高斯点计算重要性分数 $S_i$，由三个因子乘积构成：

$$S_i = \phi_i \cdot \tau_i \cdot w_{v,i}$$

- $\phi_i$：归一化的光线相交频率，反映该高斯在训练视图中的可见性。
- $\tau_i$：经 sigmoid 映射的不透明度，衡量高斯对渲染的实际贡献。
- $w_{v,i}$：**次线性体积权重**，根据局部几何复杂度对高斯的体积进行次线性压缩，避免大面积平面区域过度保留高斯。

消融实验表明，移除次线性指数会导致所有指标下降，验证了该设计的必要性。SAGP 在减少约 24% 高斯数量的同时，保持了比全局阈值修剪更高的 F1 分数。

### 分块策略中的预剪枝与边界处理

UrbanGS 的分块训练流程在 CityGS 基础上进行了两项关键改进：

1. **全局预剪枝**：在获得全局粗高斯模型后，先执行 SAGP 剪枝去除冗余高斯，再进行场景收缩与分块。这避免了冗余高斯吸引非贡献视图、放大分块训练的计算负担。消融实验显示，移除预剪枝会导致高斯数增加 23%，训练时间变长且显存升高。
2. **边界高斯复制**：在分块阶段，子块边界处的公共高斯原语被复制到相邻块中，以消除块间几何不连续导致的融合伪影。

### 补充图表

![[assets/figures/papers/paper_list_l64_https_openreview_net_forum_id_L3utaw6SD9/figures/011_Figure.jpg]]
*Figure: A: Illustration of Proof of the Proposition on Comprehensive Update of Gaussian Parameters. (a) After back-propagation through alpha-blending $\mathrm { E q . 1 } ,$ the rendered normal supervision loss ${ \mathcal { L } }$ _ { n } moves Gaussians either closer to (corresponding to P o s i t i o $n _ { 1 }$ ) or farther from (corresponding to $\it { P o s i t i o n _ { 2 } ) }$ the intersecting ray. When the normal of a Gaussian is closer to the ground truth (GT) surface normal, this supervision mechanism pushes the Gaussian (e.g.$, \left. P o s i t i o n _ { 1 } \right)$ toward the ray to increase its weight in the rendering equation; conversely, if there is a significant deviation between the two n...*

![[assets/figures/papers/paper_list_l64_https_openreview_net_forum_id_L3utaw6SD9/figures/019_Figure.jpg]]
*Figure: E: Qualitative ablation for the Depth-Consistent D-Normal Regularizer. We visualized the centers of Gaussian ellipsoids in a 3D scene. In the left figure, the Depth-Consistent D-Normal Regularizer is disabled, while the right figure demonstrates the results with our proposed regularization. In comparison, the left figure exhibits a notable number of Gaussian ellipsoids floating off the surface. Our proposed Depth-Consistent D-Normal Regularizer effectively pushes the 3D Gaussians toward the surface, resulting in a cleaner reconstruction*



## 实验与关键发现

### 一、新视角合成主结果

UrbanGS 在 Mill19 和 UrbanScene3D 两个城市场景基准上全面评估了新视角合成质量，与 Mega-NeRF、Switch-NeRF、3DGS、VastGaussian、CityGaussian、CityGaussianV2、GOF 及 CityGS-X 等方法进行了系统对比（Table 1）。

![[assets/figures/papers/paper_list_l64_https_openreview_net_forum_id_L3utaw6SD9/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparisons on the Mill19 (Yu et al., 2022) and UrbanScene3D (Lin et al., 2022) datasets for novel view synthesis. ↑ indicates higher is better, while ↓ indicates lower is better. The top three results are highlighted with red, orange, and yellow backgrounds, respectively. † denotes results obtained without the decoupled appearance encoding*

**定量优势**：在 Mill19 的 Building 场景上，UrbanGS 取得 PSNR 22.82，较 CityGaussian 的 21.55 提升 **+1.27 dB**；在 Rubble 场景上，PSNR 达 26.25，较 CityGaussianV2 的 23.75 提升 **+2.50 dB**。在 UrbanScene3D 的 Residence 场景上，SSIM 达到 0.823，较 CityGaussianV2 的 0.769 提升 **+0.054**。LPIPS 指标同样保持领先，表明 UrbanGS 在感知质量上亦具竞争力。

**定性对比**：Figure 3 的可视化结果表明，UrbanGS 在建筑立面纹理、树木枝叶细节和远景结构上均表现出更少的模糊和伪影，而 VCR-Gaus 等几何正则化方法在复杂城市场景中因显存溢出直接失败（Figure 1 佐证）。

### 二、几何重建评估

在 GauU-Scene 数据集上，以精确率、召回率和 F1 分数评估表面重建质量（Table 2）。UrbanGS 在所有场景上均取得最高 F1 分数：

![[assets/figures/papers/paper_list_l64_https_openreview_net_forum_id_L3utaw6SD9/figures/006_Table_2.jpg]]
*Table 2: Detailed geometry evaluation on the GauU-Scene dataset (Xiong et al., 2024). “NaN” indicates that the method produced invalid numerical results, while “FAIL” denotes a failure to extract a valid mesh. For all metrics, ↑ indicates that higher values are better*

- Residence: F1 = 0.493 vs CityGaussianV2 的 0.467（**+0.026**）
- Russian Building: F1 = 0.546 vs CityGaussianV2 的 0.537（**+0.009**）

值得注意的是，2DGS 和 GOF 在部分场景上出现 “NaN” 或 “FAIL”，无法提取有效 mesh，而 UrbanGS 始终保持稳定输出。Figure 4 的 mesh 和纹理定性对比进一步显示，UrbanGS 重建的表面在窗户边缘、屋顶线条等细部结构上更加锐利，纹理映射失真更少。

![[assets/figures/papers/paper_list_l64_https_openreview_net_forum_id_L3utaw6SD9/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative mesh and texture comparison between SOTA and our method on GauU-Scene dataset (Xiong et al., 2024)*

### 三、效率与资源占用

Table 3 综合对比了各方法的高斯点数、模型大小和显存占用。UrbanGS 在保持最高 F1 分数的同时，高斯点数和模型体积显著低于 CityGaussian 系列。在 Rubble 数据集上，UrbanGS 训练时间仅 **2 小时 10 分钟**，而对比方法普遍超过 4 小时，效率提升至少 2 倍（Figure 5）。该效率优势源于 SAGP 预剪枝大幅压缩了粗模型中的冗余高斯，使分块训练的计算负载显著降低。

![[assets/figures/papers/paper_list_l64_https_openreview_net_forum_id_L3utaw6SD9/figures/007_Table_3.jpg]]
*Table 3: Under the GauU-Scene dataset (Lin et al., 2022), comparison of Large-Scale Scene Modeling Methods, the best result for specific metrics under each scene is highlighted in bold*

![[assets/figures/papers/paper_list_l64_https_openreview_net_forum_id_L3utaw6SD9/figures/008_Figure_5.jpg]]
*Figure 5: Experimental results on the Rubble dataset (Yu et al., 2022) demonstrate that the proposed method outperforms comparative approaches in terms of PSNR while achieving superior training efficiency*

**硬件公平性说明**：竞争方法在 RTX A800 GPU 上评估，UrbanGS 使用 8 块 RTX A5000 GPU 训练——在更弱硬件条件下仍取得效率与质量双赢。

### 四、消融实验

#### 4.1 D-Normal 正则化与深度一致性

Table 5 展示了深度一致性 D-Normal 正则化各组件的消融效果（Morden Building 场景）。移除 D-Normal 正则化（仅保留渲染法向监督）导致：

![[assets/figures/papers/paper_list_l64_https_openreview_net_forum_id_L3utaw6SD9/figures/010_Table_5.jpg]]
*Table 5: Ablation study on the effects of D-Normal Regularization and Depth Consistency Regularization, conducted on the Morden Building dataset (Xiong et al., 2024). Bold indicates best performance*

- F1 从 0.503 骤降至 0.453（**-0.050**）
- PSNR 从 26.44 降至 24.59（**-1.85 dB**）

这验证了 D-Normal 对位置参数更新的关键作用——传统法向监督仅能优化旋转，无法有效移动高斯位置以对齐真实表面。进一步移除自适应置信度权重 $w_d$ 同样导致所有指标下降，证明基于梯度方向一致性和逆深度偏差的动态加权对抑制不可靠深度先验至关重要。

#### 4.2 空间自适应高斯修剪 (SAGP)

Table 4 在 Russian Building 场景上对比了不同修剪策略。SAGP 相比传统全局阈值修剪：

![[assets/figures/papers/paper_list_l64_https_openreview_net_forum_id_L3utaw6SD9/figures/009_Table_4.jpg]]
*Table 4: Ablation Results on Russian dataset (Xiong et al., 2024). Bold indicates best performance. Note that OOM denotes Out Of Memory*

- 高斯数量减少约 **24%**
- F1 分数为 0.546 vs 0.518（**+0.028**）
- 训练时间和显存占用同步降低

全局固定阈值方法因忽略局部几何复杂度，容易误删细节区域的高斯，导致 F1 下降；而 SAGP 通过局部体素内的光线相交频率、不透明度和次线性体积权重综合评估重要性，在压缩模型的同时保留了关键几何结构。

#### 4.3 分块策略中的预剪枝

消融 SAGP 预剪枝步骤（即直接在粗模型上分块训练）导致高斯数增加 23%，训练时间延长且显存升高，同时渲染和几何质量略有下降（Table G）。这证实了先全局剪枝再分块的策略对后续子块训练效率和质量均有正向贡献。

#### 4.4 次线性体积权重

移除空间自适应重要性分数中的次线性指数项（Eq. 14 中的 $w_{v,i}$ 次线性映射）导致所有指标下降（Table F），验证了次线性压缩对平衡不同尺度高斯贡献的必要性——线性权重会使大体积高斯过度主导修剪决策，损害细节保留。

### 五、失败模式与局限性

尽管 UrbanGS 整体表现优异，分析揭示了以下局限：

1. **单目先验依赖**：D-Normal 正则化和深度一致性框架依赖预训练单目深度/法向估计器提供的伪真值。在弱纹理或极端光照区域，这些先验的误差会传播至重建结果，表现为局部表面平滑度下降或几何偏移。目前方法缺乏对先验质量的在线评估与修正机制。

2. **远距离天空区域退化**：在缺乏明确几何结构的天空等远距离区域，显式几何优化可能产生不合理的高斯分布，导致渲染质量略逊于原始 3DGS（详见 Figure G）。这是几何正则化与渲染保真度之间的固有张力。

3. **静态场景假设**：方法未显式建模城市场景中常见的动态物体（车辆、行人等），运动目标会被错误地“凝固”为静态几何，产生伪影。

4. **SAGP 超参数敏感性**：次线性体积权重的参数 $\lambda$ 在不同尺度场景中可能需要调整，当前缺乏自适应调节策略。

### 六、关键图表结论摘要

| 图表 | 核心结论 |
|------|---------|
| **Table 1** | UrbanGS 在 PSNR/SSIM/LPIPS 上全面领先，Rubble 场景 PSNR 领先第二名 2.50 dB |
| **Table 2** | 几何 F1 分数在所有 GauU-Scene 场景上均为最优，2DGS 和 GOF 在部分场景无法提取有效 mesh |
| **Table 3** | 以更低的高斯点数和模型大小取得最高 F1，效率与质量兼得 |
| **Figure 5** | Rubble 场景训练仅需 2h10min，效率至少为对比方法的 2 倍 |
| **Table 5** | 移除 D-Normal 导致 F1 下降 0.050、PSNR 下降 1.85 dB，验证其对位置更新的关键作用 |
| **Table 4** | SAGP 减少 24% 高斯的同时 F1 高于全局阈值修剪 0.028 |

### 补充图表

![[assets/figures/papers/paper_list_l64_https_openreview_net_forum_id_L3utaw6SD9/figures/022_Table.jpg]]
*Table: G: Ablation Results of Block Partition Strategy on Russian Scene Dataset (Xiong et al., 2024).Bold indicates best performance. Table H: Ablation Study of Geometry-Aware Confidence Hyperparameters*

![[assets/figures/papers/paper_list_l64_https_openreview_net_forum_id_L3utaw6SD9/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative results of ours and other methods in image rendering on Mill-19 (Yu et al., 2022) and Urbanscene3D (Lin et al., 2022)*



## 定位与知识库关联

### 1. 技术脉络定位

UrbanGS 处于**大规模 3D 高斯泼溅 (3DGS)** 与**几何精确表面重建**的交叉点。其设计直接回应了将 3DGS 从物体/小场景推向城市级大场景时暴露的核心矛盾：高斯数量爆炸导致的内存膨胀、训练时间剧增，以及缺乏有效几何约束导致的表面浮空与深度对齐失效。

**与显式几何监督方法的对比**：在几何正则化方面，UrbanGS 最直接的对比对象是 **VCR-Gaus** (Chen et al., 2024b) 和 **2DGS** (Huang et al., 2024a)。VCR-Gaus 采用预训练模型估计的渲染法向进行监督，但这种方式仅能更新高斯的旋转参数，无法驱动位置沿法向移动以修正表面偏移。UrbanGS 的核心突破在于提出“深度一致性 D-Normal 正则化”——从渲染深度图的空间梯度推导 D-Normal，并用伪法向先验监督，使得梯度可同时反向传播至位置和旋转参数，实现完整的几何参数更新。2DGS 将 3D 高斯坍缩为二维 surfel 以获取精确表面，但在大场景中面临内存爆炸问题；UrbanGS 保留了 3D 高斯的表达能力，同时通过 SAGP 压缩冗余，在几何精度与计算效率间取得平衡。

**与大规模 3DGS 分块方法的对比**：在大场景扩展策略上，UrbanGS 继承了 **CityGaussian** (Liu et al., 2024a) 和 **CityGaussianV2** (Liu et al., 2024b) 的分块训练范式，但引入了两个关键改进：(1) 在分块前对全局粗模型执行 SAGP 预剪枝，消除冗余高斯以避免它们吸引无关视图、放大计算开销；(2) 在子块边界复制共有高斯基元，消除分块融合时的几何不连续伪影。**CityGS-X** (Gao et al., 2025) 采用并行分层 3DGS，但 UrbanGS 的 SAGP 策略在减少高斯数量约 24% 的同时保持了更高的 F1 分数，验证了基于局部几何复杂度的自适应修剪优于统一分区策略。

**与其他 NVS 基线的对比**：**Mega-NeRF** (Turki et al., 2022) 和 **Switch-NeRF** (Mi & Xu, 2023) 代表了基于 NeRF 的大场景方案，但其体积渲染的计算成本远高于 3DGS 的光栅化。**VastGaussian** (Lin et al., 2024) 是早期将 3DGS 扩展至大场景的尝试，但在几何质量上明显弱于 UrbanGS。**GOF** (Yu et al., 2024b) 引入光线追踪，但计算开销限制了其在大场景中的可扩展性。

### 2. 适用边界与局限

UrbanGS 的有效性受以下边界条件约束：

- **对单目先验的依赖**：D-Normal 正则化和逆深度损失均依赖预训练单目深度/法向估计器提供的伪真值。在弱纹理区域（如纯色墙面）、极端光照条件或远距离天空区域，这些先验的误差会直接传播至重建结果。消融实验显示移除 D-Normal 正则化会导致 F1 从 0.503 降至 0.453，PSNR 从 26.44 降至 24.59，表明系统对几何监督质量的敏感性。在缺乏明确几何结构的远距离天空区域，显式几何优化甚至可能导致渲染质量略逊于原始 3DGS。

- **静态场景假设**：方法未显式建模城市场景中常见的动态物体（车辆、行人等），这些移动目标在 COLMAP 稀疏重建中通常被剔除或产生噪声，但在密集高斯优化中可能引入伪影。

- **SAGP 的超参数敏感性**：空间自适应重要性分数中的次线性体积权重 $w_{v,i}$ 依赖指数参数调节压缩强度。消融实验证实移除次线性指数会导致所有指标下降，但该参数在不同场景尺度下的最优值可能需要手动调整，泛化性有待验证。

- **GPU 资源需求**：尽管 UrbanGS 在 8 块 RTX A5000 GPU 上即可完成训练（而 VCR-Gaus 在同类硬件上因显存溢出失败），但多卡并行分块训练仍然对硬件配置有一定要求，单卡场景下的部署效率需要进一步验证。

### 3. 开放问题

1. **多视图几何一致性替代单目先验**：当前框架对预训练单目估计器的依赖构成了性能上限。如何通过多视图几何一致性约束（如跨视图光度一致性、极线约束）部分替代或校正单目先验，是提升弱纹理区域鲁棒性的关键方向。

2. **动态场景扩展**：将 UrbanGS 扩展至包含动态目标的城市场景，可能需要结合 4D 高斯场或运动分解机制。这涉及动态/静态区域的分割、运动轨迹建模，以及与现有 SAGP 修剪策略的兼容性问题。

3. **SAGP 的尺度自适应**：次线性体积权重的设计在不同场景尺度（从建筑单体到城市街区）中的泛化性如何？是否需要根据场景覆盖范围自适应调整参数 $\lambda$？这需要更大规模的跨场景验证。

4. **端到端可微分流水线**：当前流水线中 COLMAP 位姿估计、单目深度/法向估计、高斯初始化是分离的模块。将这些步骤纳入端到端可微分框架，可能进一步提升几何一致性和训练效率，但也对计算和内存提出了更高要求。

5. **与前沿高斯表示的融合**：近期出现的锚点高斯、多分辨率哈希编码等 3DGS 变体在表达能力上有所提升，UrbanGS 的 D-Normal 正则化和 SAGP 策略是否可以无缝迁移至这些新表示，值得探索。



## 原文 PDF

![[paperPDFs/ICLR_2026/UrbanGS_Efficient_and_Scalable_Architecture_for_Geometrically_Accurate_Large_Sce_dbeb8df34f9e.pdf]]
