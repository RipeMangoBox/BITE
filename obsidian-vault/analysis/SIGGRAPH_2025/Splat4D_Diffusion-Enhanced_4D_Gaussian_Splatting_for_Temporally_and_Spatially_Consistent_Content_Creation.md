---
title: "Splat4D: Diffusion-Enhanced 4D Gaussian Splatting for Temporally and Spatially Consistent Content Creation"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/Splat4D_Diffusion_Enhanced_4D_Gaussian_Splatting_for_Temporally_and_Spatially_Consistent_Content_Creation.pdf
project_link: "https://visual-ai.github.io/splat4d"
code_link: null
aliases:
- Splat4D
tags:
- SIGGRAPH_2025
- topic/generative_models_diffusion
core_operator: 通过多视图渲染生成不一致性掩蔽，并利用视频扩散模型对不一致区域进行不确定性引导的修复，结合微调后的非对称U-Net消除时空伪影。
primary_logic: 将多视图视频生成、图像增强、不确定性掩蔽和视频扩散迭代细化统一在4D高斯溅射框架中，同步提升空间与时间一致性，并通过微调非对称U-Net弥合域间隙。
claims:
- 移除不确定性掩蔽或U-Net训练使LPIPS、CLIP-S和FVD指标显著恶化，证明这些组件对处理时空不一致至关重要。
- 在Consistent4D数据集的液体和多物体场景中，完整模型在CLIP、LPIPS、FVD上均大幅超越SV4D等基线，且反馈回路、图像增强器和MV-Adapter均贡献显著。
- Consistent4D (液体场景) 上 CLIP↑ / LPIPS↓ / FVD↓ = 0.93 / 0.127 / 493.0
- Consistent4D (多物体场景) 上 CLIP↑ / LPIPS↓ / FVD↓ = 0.96 / 0.102 / 428.5
---

# Splat4D: Diffusion-Enhanced 4D Gaussian Splatting for Temporally and Spatially Consistent Content Creation

> [!tip] 核心洞察
> 将多视图视频生成、图像增强、不确定性掩蔽和视频扩散迭代细化统一在4D高斯溅射框架中，同步提升空间与时间一致性，并通过微调非对称U-Net弥合域间隙。

| 字段 | 内容 |
|------|------|
| 中文题名 | Splat4D：扩散增强的4D高斯溅射用于时空一致性内容生成 |
| 英文题名 | Splat4D: Diffusion-Enhanced 4D Gaussian Splatting for Temporally and Spatially Consistent Content Creation |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](http://arxiv.org/abs/2508.07557v1) · [Project](https://visual-ai.github.io/splat4d) |
| Topic | #topic/generative_models_diffusion |
| Method | Splat4D |
| Dataset | Consistent4D |

> [!tip] 效果简介
> - Consistent4D (液体场景) 上，CLIP↑ / LPIPS↓ / FVD↓ 0.93 / 0.127 / 493.0 vs 0.88 / 0.147 / 772.6 (SV4D) (CLIP +0.05, LPIPS -0.020, FVD -279.6)。
> - Consistent4D (多物体场景) 上，CLIP↑ / LPIPS↓ / FVD↓ 0.96 / 0.102 / 428.5 vs 0.90 / 0.125 / 722.3 (SV4D) (CLIP +0.06, LPIPS -0.023, FVD -293.8)。

## 概要

现有4D内容生成方法多依赖单视图视频，缺乏多视角信息，且独立处理各帧，导致时空不一致、纹理模糊与时间闪烁。Splat4D提出一种扩散增强的4D高斯溅射框架，将多视图视频生成、图像增强、不确定性掩蔽与视频扩散迭代细化统一起来，同步提升空间与时间一致性。具体而言，该方法先将单目视频经MV-Adapter扩展为多视角序列，利用图像增强器提升细节，再通过非对称U-Net预测器与Splatter Image构建粗4D高斯场；随后基于多视图渲染产生的不一致性掩蔽，由视频扩散模型对不一致区域进行不确定性引导修复，并经反馈循环迭代优化。在Consistent4D数据集的液体与多物体场景中，Splat4D在CLIP、LPIPS、FVD指标上全面超越SV4D等基线方法。

## 核心方法与创新机理

### 问题瓶颈

现有4D内容生成方法（如Consistent4D、STAG4D、SV4D）普遍依赖单视图视频输入，缺乏多视角信息支撑，且独立处理每一帧，导致生成的4D表示存在**时空不一致**问题——具体表现为纹理模糊、几何失真和时间域闪烁伪影。根本原因在于：单视图视频无法提供足够的3D空间约束，而逐帧独立处理破坏了时间连续性。

### 核心创新机制

Splat4D的核心洞察在于：将**多视图视频生成、图像增强、不确定性掩蔽引导的扩散修复、以及非对称U-Net微调**统一在4D高斯溅射（4D Gaussian Splatting）框架中，同步解决空间一致性与时间一致性问题。其关键因果链条如下：

1. **多视图覆盖**：通过MV-Adapter将单视图视频扩展为多视角序列（前、左、右、后），弥补空间信息缺失。
2. **质量提升**：图像增强器（Image Enhancer）细化各帧纹理与边缘细节，为后续重建提供高质量输入。
3. **不一致检测与修复**：渲染多视图图像后，利用**不确定性掩蔽**（uncertainty masking）自动定位时空不一致区域，再由**视频扩散模型**对这些区域进行迭代修复，确保时空平滑。
4. **域间隙弥合**：使用增强后的Objaverse数据集微调非对称U-Net，消除预训练LGM模型与增强图像之间的域间隙，提升4D高斯场的保真度。

### 关键方法变更

与基线方法相比，Splat4D在以下三个关键环节进行了根本性改进：

| 环节 | 基线做法 | Splat4D做法 | 作用 |
|------|----------|-------------|------|
| **多视图生成** | 单视图视频（SV4D等） | MV-Adapter生成前、左、右、后四视图序列 | 提供多视角空间约束，消除单视图歧义 |
| **时空一致性细化** | 无细化或简单优化 | 多视图渲染 → 不确定性掩蔽 → 视频扩散修复 | 自动检测并修复不一致区域，同步提升空间与时间一致性 |
| **U-Net训练** | 预训练LGM的U-Net，未针对增强图像微调 | 在增强后的Objaverse数据集上微调非对称U-Net | 弥合域间隙，提升重建质量 |

消融实验证实了这些变更的关键性：移除不确定性掩蔽使LPIPS从0.090升至0.114；移除U-Net微调使LPIPS升至0.107；去除反馈循环（即迭代细化）使FVD指标大幅恶化（Table 4, Table 5）。

![[assets/figures/papers/paper_list_l2_http_arxiv_org_abs_2508_07557v1/figures/011_Table_5.jpg]]
*Table 5: Additional Ablation Study. The first row illustrates the results without image enhancer. The second row shows the results using SV4D over MV-Adapter for multi-view generation*

### 核心公式与变量含义

**4D高斯场表示**：Splat4D将动态场景分解为多个3D高斯分布，在时间$t$处构建堆叠表示：

$$\mathcal{G}(S, t) = [\chi_t, s_t, r_t, \sigma_t, \zeta_t]$$

其中$\chi_t$为位置，$s_t$为尺度，$r_t$为旋转，$\sigma_t$为不透明度，$\zeta_t$为球谐系数。每个3D高斯函数为：

$$G(\mathbf{x}) = e^{-\frac{1}{2}(\mathbf{x} - \boldsymbol{\mu})^T \Sigma^{-1} (\mathbf{x} - \boldsymbol{\mu})}$$

**多视图生成**：MV-Adapter从单帧$I_t$生成三个新视点：

$$\mathsf{MV-Adapter}(I_t) \to \{I_t, I_t^{\mathrm{left}}, I_t^{\mathrm{right}}, I_t^{\mathrm{back}}\}$$

**不确定性掩蔽**：基于渲染不确定性$\sigma$生成二值掩模$M$，标记不一致区域进行后续修复：

$$M = \mathbf{1}\left(\frac{1}{2\sigma^2} > 1\right)$$

### 方法框架

整体管线（Fig. 2）分为三个阶段：**粗4D高斯生成**（多视图视频生成→图像增强→Splatter Image映射→非对称U-Net预测3D高斯参数）→ **时空一致性细化**（多视图渲染→不确定性掩蔽→视频扩散模型修复）→ **迭代优化**（反馈循环，重复细化直至收敛）。该框架支持文本/图像/单目视频三种输入模态，并可嵌入文本引导的内容编辑。

![[assets/figures/papers/paper_list_l2_http_arxiv_org_abs_2508_07557v1/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Splat4D. Our method for 4D content generation begins with processing input data (text, image, or monocular video) to produce high-quality multi-view image sequences. These sequences are used to initialize a 4D Gaussian representation via an asymmetry U-Net and image splattering. Refinement steps include leveraging uncertainty masking and video denoising diffusion to ensure high fidelity and spatial-temporal consistency, culminating in versatile 4D content creation. The pipeline supports optional text-guided content editing, enabling dynamic modifications of the 4D output for enhanced flexibility and creative control*

## 实验与关键发现

Splat4D 在视频到4D生成、图像到4D生成以及多场景子类（液体、多物体）上均取得SOTA结果，并通过系统的消融实验验证了各核心组件的因果贡献。

### 视频到4D：主对比结果

在 Consistent4D 数据集上，Splat4D 的 LPIPS 达到 **0.090**，全面超越现有方法（Table 1）。在 ObjaverseDy 测试集上同样保持领先（Table 2）。关键瓶颈在于：基线方法（如 **SV4D**、**Consistent4D**、**STAG4D**、**4Diffusion**、**Diffusion4D**）或依赖单视图视频，或缺乏有效的时空一致性机制，导致新视角下纹理模糊和几何失真。Splat4D 通过多视图生成与不确定性引导的视频扩散细化，同步解决了空间多视角一致性与时间帧间平滑性问题。

![[assets/figures/papers/paper_list_l2_http_arxiv_org_abs_2508_07557v1/figures/003_Table_1.jpg]]
*Table 1: Video-to-4D quantitative Comparison on Consistent4D Dataset [Jiang et al. 2023]*

![[assets/figures/papers/paper_list_l2_http_arxiv_org_abs_2508_07557v1/figures/004_Table_2.jpg]]
*Table 2: Video-to-4D Quantitative Comparison on ObjaverseDy Test Set [Deitke et al. 2023; Xie et al. 2024]*

### 场景子类评估：液体与多物体

针对更具挑战性的动态场景，Splat4D 在液体场景（Table 6）和多物体场景（Table 7）上均显著优于 SV4D：

![[assets/figures/papers/paper_list_l2_http_arxiv_org_abs_2508_07557v1/figures/012_Table_6.jpg]]
*Table 6: Evaluation on Liquid Case*

![[assets/figures/papers/paper_list_l2_http_arxiv_org_abs_2508_07557v1/figures/013_Table_7.jpg]]
*Table 7: Evaluation on Multi-object Case*

- **液体场景**：CLIP↑ 从 0.88 提升至 **0.93**，LPIPS↓ 从 0.147 降至 **0.127**，FVD↓ 从 772.6 降至 **493.0**。
- **多物体场景**：CLIP↑ 从 0.90 提升至 **0.96**，LPIPS↓ 从 0.125 降至 **0.102**，FVD↓ 从 722.3 降至 **428.5**。

这表明 Splat4D 的不一致性掩蔽与视频扩散修复机制对非刚性运动和复杂遮挡场景具有更强的鲁棒性。

### 图像到4D生成

在图像到4D任务上，Splat4D 的 LPIPS 达到 **0.12**，同样优于所有对比方法（Table 3）。该结果验证了从单张图像出发，通过多视图生成与4D高斯重建管线能够有效恢复动态几何与外观。

![[assets/figures/papers/paper_list_l2_http_arxiv_org_abs_2508_07557v1/figures/005_Table_3.jpg]]
*Table 3: Quantitative Comparison on Image-to-4D Generation*

### 消融实验：核心组件的因果验证

消融实验（Table 4, Table 5）揭示了各组件对性能的因果贡献：

![[assets/figures/papers/paper_list_l2_http_arxiv_org_abs_2508_07557v1/figures/006_Table_4.jpg]]
*Table 4: Ablation Study. The experiments are conducted on Consistent4D dataset [Jiang et al. 2023]*

- **不确定性掩蔽**：移除后 LPIPS 从 0.090 升至 **0.114**，CLIP-S 和 FVD 同步恶化。这证明基于不确定性阈值 $M = 1 ( \frac { 1 } { 2 \sigma ^ { 2 } } > 1 )$ 生成的掩模能准确定位时空不一致区域，为扩散修复提供精确引导。
- **U-Net 微调训练**：移除后 LPIPS 升至 **0.107**。预训练 LGM 的 U-Net 与图像增强器之间存在域间隙，在 Objaverse 数据集上微调是弥合该间隙的关键。
- **反馈循环**：去除迭代细化使 FVD-F 升至 **831.84**、FVD-V 升至 **473.91**，表明单次粗重建不足以消除时空伪影，多轮渲染-掩蔽-修复循环是收敛到高一致性的必要条件。
- **图像增强器**：去除后 CLIP-S 和视觉质量下降，验证了增强模型对纹理、边缘和细节的细化作用。
- **MV-Adapter vs SV4D**：用 SV4D 替代 MV-Adapter 导致 LPIPS 和 FVD 变差，证实多视角覆盖质量直接影响下游4D重建精度。

### 失败模式与适用边界

论文未明确报告失败案例或限制条件，该部分需要手动验证。从方法机理推断，潜在边界包括：极度稀疏输入视角下多视图生成质量不足；快速非刚性变形场景中不确定性掩模的阈值设定可能敏感；视频扩散模型的修复能力受限于其训练数据分布，对域外纹理可能产生伪影。

## 定位与知识库关联

### 问题定位：从单视图视频到多视图时空一致的4D生成

现有4D内容生成方法（如**Consistent4D** (Jiang et al., 2023)、**STAG4D** (Zeng et al., 2024)、**SV4D** (Xie et al., 2024)、**4Diffusion** (Zhang et al., 2024)、**Diffusion4D** (Liang et al., 2024b)）普遍存在一个核心瓶颈：依赖单视图视频作为输入，缺乏多视角信息，且独立处理每一帧，导致时空不一致——具体表现为纹理模糊、几何失真和时间闪烁。Splat4D的定位正是填补这一“单视图→多视图时空一致性”的空白，其本质差异在于将多视图生成、图像增强、不确定性掩蔽和视频扩散迭代细化统一在4D高斯溅射框架中，同步提升空间与时间一致性。

### 与基线方法的本质差异

| 维度 | 基线方法（SV4D等） | Splat4D |
|------|-------------------|---------|
| 多视图覆盖 | 单视图视频，视角单一 | **MV-Adapter**生成前、后、左、右多视图序列（Eq. 2） |
| 图像质量 | 无增强或简单后处理 | **图像增强器(IE)**细化纹理、边缘和细节 |
| 时空一致性 | 无专门细化机制 | **不确定性掩蔽**检测不一致区域 + **视频扩散模型**迭代修复 |
| 域间隙处理 | 预训练U-Net直接使用 | 在Objaverse上**微调非对称U-Net**，降低增强图像与预训练模型间的域间隙 |

这些差异在消融实验中得到了直接验证：移除不确定性掩蔽使LPIPS从0.090升至0.114，移除U-Net微调使LPIPS升至0.107（Table 4）；去除反馈循环使FVD-F升至831.84、FVD-V升至473.91（Table 5），证明每个组件对处理时空不一致都不可或缺。

### 知识库挂载点

1. **4D高斯溅射（4D Gaussian Splatting）**：Splat4D将动态场景分解为多个3D高斯分布 $G ( \mathbf { x } ) = e ^ { - \frac { 1 } { 2 } ( \mathbf { x } - \boldsymbol { \mu } ) ^ { T } \Sigma ^ { - 1 } ( \mathbf { x } - \boldsymbol { \mu } ) }$（Eq. 1），并通过堆叠表示 $\mathcal { G } ( S , t ) = [ \chi _ { t } , s _ { t } , r _ { t } , \sigma _ { t } , \zeta _ { t } ]$ 捕捉空间结构与时间演化。这为后续4D表示学习提供了“显式几何+隐式时间”的混合范式参考。

2. **多视图扩散先验**：MV-Adapter的引入将多视图生成与4D重建解耦，使方法可灵活替换多视图生成模块。这一设计为未来更强的多视图扩散模型（如Zero123++等）的即插即用提供了接口。

3. **不确定性引导的迭代细化**：通过不确定性掩模 $M = 1 \left( \frac { 1 } { 2 \sigma ^ { 2 } } > 1 \right)$ 定位不一致区域，再用视频扩散模型修复，形成“检测-修复”闭环。这一范式可迁移至其他需要时空一致性约束的生成任务（如NeRF-based动态场景、4D人体重建）。

4. **域间隙桥接**：在Objaverse上微调U-Net以适配增强图像分布，揭示了“预训练大模型+下游增强”管线中域偏移问题的通用解决方案——针对性微调而非直接使用预训练权重。

### 适用边界

- **输入模态**：支持单视图视频、单张图像、文本描述三种输入，覆盖了从视频到4D、图像到4D、文本到4D的生成场景，以及文本引导的4D内容编辑。
- **场景类型**：在Consistent4D数据集的液体场景（Table 6：CLIP 0.93, LPIPS 0.127, FVD 493.0）和多物体场景（Table 7：CLIP 0.96, LPIPS 0.102, FVD 428.5）上均取得最优，表明方法对流体运动和多物体交互具有鲁棒性。
- **潜在局限**：分析材料中未报告极端遮挡、快速运动模糊、长时序（>数秒）场景下的性能，这些边界情况需要手动验证。此外，方法依赖多个预训练模型（MV-Adapter、视频扩散模型、图像增强器）的级联，管线复杂度较高，可能影响推理效率。

### 后续启发

1. **多视图一致性作为通用约束**：Splat4D证明多视图渲染+不一致性掩蔽+视频扩散修复的组合可有效消除时空伪影。这一思路可推广至其他生成任务（如4D人体运动生成、动态场景补全），将“不一致性检测”作为可微分损失或强化学习奖励信号。

2. **反馈循环的价值**：消融实验显示去除反馈循环导致FVD指标大幅劣化（Table 5），表明“生成-检测-修复-再生成”的迭代范式对提升时空一致性至关重要。未来工作可探索自适应循环终止条件或学习式掩蔽策略以提升效率。

3. **非对称U-Net的域适应**：微调策略的成功暗示，在3D/4D生成中，针对增强/超分后的图像分布微调重建网络，可能是提升保真度的通用技巧，尤其适用于需要级联多个扩散模型的管线。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/Splat4D_Diffusion_Enhanced_4D_Gaussian_Splatting_for_Temporally_and_Spatially_Consistent_Content_Creation.pdf]]