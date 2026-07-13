---
title: "SpatialVID: A Large-Scale Video Dataset with Spatial Annotations"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SpatialVID_A_Large_Scale_Video_Dataset_with_Spatial_Annotations.pdf
project_link: null
code_link: null
aliases:
- SpatialVID
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 为互联网视频添加逐帧相机姿态、深度图等密集 3D 标注，并集成利用相机姿态先验的结构化空间感知标题，使模型能够学习显式的 3D 归纳偏置。
primary_logic: 通过‘手动筛选运动丰富的视频 → 层次化质量过滤 → 改进 MegaSaM 深度估计 → VLM/LLM 结合相机姿态生成空间准确标题’的流程，可将互联网视频转化为大规模、多样化、具备几何与语义双重注释的空间智能数据集，从而显著提升下游任务性能。
claims:
- SpatialVID-HQ 在相机控制视频生成任务的所有三个基准上均取得最低 TransErr，相机可控性最优。
- 相比 Panda-70M，SpatialVID 在美学、亮度、运动等指标上分布更集中，且相机运动轨迹更具多样性，超过 80% 的 Panda-70M 视频因运动不足无法重建。
- 使用 SpatialVID 训练的 GS-LRM 在新视角合成任务上优于 RealEstate10K（DL3DV 上 PSNR 27.80 vs 27.01）。
- RE10K 上 TransErr = 7.42
---

# SpatialVID: A Large-Scale Video Dataset with Spatial Annotations

> [!tip] 核心洞察
> 通过‘手动筛选运动丰富的视频 → 层次化质量过滤 → 改进 MegaSaM 深度估计 → VLM/LLM 结合相机姿态生成空间准确标题’的流程，可将互联网视频转化为大规模、多样化、具备几何与语义双重注释的空间智能数据集，从而显著提升下游任务性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | SpatialVID：大规模空间标注视频数据集 |
| 英文题名 | SpatialVID: A Large-Scale Video Dataset with Spatial Annotations |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.09676) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | SpatialVID |
| Dataset | RE10K, Sekai, SpatialVID, DL3DV |

> [!tip] 效果简介
> - RE10K 上，TransErr 7.42 vs 7.46 (RE10K) (-0.04)。
> - Sekai 上，TransErr 6.04 vs 6.49 (Sekai-Real) (-0.45)。
> - SpatialVID 上，TransErr 4.33 vs 5.16 (RE10K) (-0.83)。

## 概要

**瓶颈与动机** 现有视频数据集普遍缺乏大规模、高质量且显式带有几何（相机姿态、深度）与语义标注的动态场景数据，导致空间智能模型难以从像素中隐式习得可靠的空间关系。SpatialVID 正是针对这一缺口构建的百万级开放场景视频数据集。

**核心思路** 通过“手动筛选运动丰富的互联网视频 → 层次化质量过滤 → 改进 MegaSaM 深度估计 → VLM/LLM 结合相机姿态生成空间准确标题”的流程，将 21,000+ 小时的原始 YouTube 视频转化为 2.7 百万个片段、总计 7,089 小时的动态内容。每个片段携带逐帧相机姿态、深度图、动态掩码以及结构化空间感知标题，使模型能够学习显式的 3D 归纳偏置。

**方法谱系与知识库定位** 与仅提供相机姿态或简短标签的 **RealEstate10K**、**Sekai-Real** 等数据集不同，SpatialVID 在几何注释和语义标题两个维度上同时升级：几何层面引入逐帧深度与动态掩码，语义层面引入由 Gemini-2.0-Flash 与 Qwen3-30B-A3B 联合生成、经相机姿态先验修正的结构化标题。深度估计器由 MegaSaM 原始模块替换为 UniDepth v2 + Depth Anything v2。

**主要结果概览** 
- **相机控制视频生成**：在 RE10K、Sekai、SpatialVID 三个基准上，SpatialVID-HQ 训练的模型均取得最低 TransErr（Table 2），相机可控性最优。
- **新视角合成**：使用 SpatialVID 训练的 GS-LRM 在 DL3DV 上 PSNR 达 27.80，优于 RealEstate10K 的 27.01（Table 4）。
- **相机姿态估计微调**：在 TUM-dynamics 上，VGGT 的 ATE 从 0.015 降至 0.013，CUT3R 从 0.049 降至 0.040（Table 3）。
- **数据质量**：相比 Panda-70M，SpatialVID-HQ 在美学、亮度、运动等指标上分布更紧凑，且相机运动轨迹更具多样性（Figure 5）。

**局限与开放问题** 几何注释依赖 MegaSaM，在主要移动物体主导或共线运动等极端条件下精度受限；场景分布受限于手动筛选的关键词与偏好，存在地理和内容偏差。未来可探索向 LiDAR 等传感器模态扩展，以及更强的 3D 推理能力以提升自动化标题质量。

### 空间智能的数据瓶颈

空间智能（Spatial Intelligence）旨在赋予机器理解、推理并与三维世界交互的能力，其核心在于对场景几何结构、相机运动与语义关系的联合建模。近年来，视频生成模型和三维重建方法取得了显著进展，但一个根本性瓶颈始终存在：**现有视频数据集普遍缺乏大规模、高质量且显式带有几何与语义标注的动态场景数据**。

具体而言，当前可用的空间信息数据集呈现出明显的结构性缺陷：

- **规模与多样性不足**：如 RealEstate10K 等数据集虽提供相机姿态，但场景局限于房地产等静态室内环境，且规模远不足以支撑现代生成模型的训练需求。
- **标注维度单一**：多数数据集仅提供相机姿态或稀疏点云，缺少逐帧深度图、动态掩码等密集三维标注，迫使模型仅能从像素中隐式学习空间关系。
- **语义信息缺失**：现有视频标题通常为简短标签或无空间参考的通用描述，无法为模型提供关于相机运动方向、场景深度结构等空间先验的显式监督信号。

### 现有数据集的局限性

Table 1 系统性地对比了 SpatialVID 与已有空间信息数据集的关键属性。从对比中可以看出，现有数据集在以下维度上存在显著缺口：

1. **场景动态性**：多数高质量三维数据集（如 RealEstate10K、DL3DV）聚焦于静态场景，而真实世界的空间智能应用需要理解动态环境中的物体运动与相机运动之间的复杂交互。
2. **开放场景覆盖**：合成数据集（如 Hypersim）虽可提供完美标注，但难以覆盖真实世界中多样化的拍摄场景、光照条件和运动模式。
3. **几何与语义的割裂**：即便部分数据集同时提供相机姿态和文本描述，两者之间缺乏结构化关联——文本描述不包含对相机运动的空间参考，几何信息也未参与语义理解过程。

### SpatialVID 的动机与核心思路

针对上述缺口，SpatialVID 的核心动机在于：**构建一个大规模、多样化、同时具备显式几何标注与空间感知语义标注的视频数据集，使模型能够学习显式的三维归纳偏置**。

其核心洞察可概括为：通过“手动筛选运动丰富的视频 → 层次化质量过滤 → 改进 MegaSaM 深度估计 → VLM/LLM 结合相机姿态生成空间准确标题”的流程，可将互联网视频转化为大规模、多样化、具备几何与语义双重注释的空间智能数据集。

具体而言，SpatialVID 从超过 21,000 小时的互联网视频出发，经过层次化过滤与多维度标注，最终产出 270 万片段、总计 7,089 小时的动态内容。每个片段均包含：

- **逐帧相机姿态**与**深度图**（基于改进版 MegaSaM 估计）
- **动态掩码**（区分场景中的运动物体与静态背景）
- **结构化空间感知标题**（由 VLM 解析视觉内容，LLM 结合相机姿态先验精炼生成）
- **序列化运动指令**（将相机轨迹映射为标准电影摄影术语）

这种“几何+语义”双重注释的设计，使得 SpatialVID 能够同时服务于相机控制视频生成、新视角合成、相机姿态估计等多种下游任务，为空间智能模型的训练提供了前所未有的数据基础。

## 核心方法与创新机理

SpatialVID 的核心创新在于将大规模互联网视频转化为首个同时具备**密集几何标注**与**空间感知语义标题**的动态场景数据集，从而为空间智能模型提供显式的 3D 归纳偏置。相较于现有数据集，其关键突破体现在以下三个维度的“changed slots”上。

### 从无/弱空间标注到密集几何注释

现有视频数据集（如 RealEstate10K、Sekai-Real）或仅提供相机姿态，或完全缺乏 3D 信息。SpatialVID 为每个片段提供**逐帧相机姿态、深度图与动态掩码**的三重几何注释（Section 3.3）。其技术瓶颈在于：互联网视频的运动模式复杂、动态物体干扰严重，传统 SLAM/深度估计方法难以稳定输出。为此，作者对 MegaSaM 管道进行了关键改造——将深度估计器替换为 **UniDepth v2 + Depth Anything v2** 的组合，并引入基于加速度的异常检测器来识别非物理运动波动，同时利用 SAM2 从自适应阈值候选区域中提取动态掩码。这一改进使得几何注释的鲁棒性显著提升，为后续任务提供了可靠的 3D 监督信号。

### 从简短标签到结构化空间感知标题

传统数据集的语义标注通常仅为简短类别标签，缺乏对空间关系和相机运动的精确描述。SpatialVID 提出了**结构化空间感知标题生成流程**（Section 3.5）：先用 Gemini-2.0-Flash 解析视觉内容并生成初始运动与场景描述，再由 Qwen3-30B-A3B 结合**相机姿态先验**进行精炼。这一“VLM → LLM + 相机先验”的级联设计是关键因果旋钮——如图 4 所示，仅靠 VLM 会将“向左移动”误判为“向右”，而注入相机姿态后 LLM 能自动纠正方向错误。最终生成的标题包含运动描述与场景描述两部分，长度较原始版本显著增加（Figure 15），为模型学习空间语义对齐提供了高质量文本监督。

### 从被动采集到主动质量筛选与运动平衡

与 Panda-70M 等大规模但运动匮乏的数据集不同，SpatialVID 从**手动筛选运动丰富的 YouTube 视频**出发（Section 3.1），经过层次化质量过滤（美学、亮度、文字遮挡、运动强度四个维度）和基于运动轨迹与场景类别的平衡采样，形成高质量子集 SpatialVID-HQ。Figure 5 的分布对比显示，Panda-70M 中超过 80% 的视频因运动不足无法重建，且其相机轨迹高度集中在静态视点；而 SpatialVID-HQ 在美学、亮度、运动等指标上分布更紧凑，同时拥有更丰富的弯曲/转向轨迹，验证了主动筛选与过滤策略的有效性。

**证据强度评估**：上述三个 changed slots 均有明确的实验锚点支撑——几何注释改进体现在 MegaSaM 轨迹对比（Figure 10）和下游任务增益（Table 3 中微调后 ATE 下降）；空间感知标题的有效性由 Figure 4 的定性纠正案例和 Table 2 中 SpatialVID-HQ 在所有基准上取得最低 TransErr 间接验证；质量筛选的优势则由 Figure 5 的分布对比直接证实。需注意，当前几何注释仍依赖 MegaSaM 框架，在极端共线运动或大动态物体主导场景下可能失效（Section 3.3），这是该创新点的已知边界。

SpatialVID 的构建流程采用“收集—过滤—注释—采样”四阶段流水线，将互联网视频转化为具备显式几何与语义标注的大规模空间智能数据集。图 2 给出了流水线总览：从手动筛选的运动丰富型网络视频出发，依次经过层次化质量过滤、几何与语义双通道注释，最后通过运动与类别均衡采样得到高质量子集 SpatialVID-HQ。

**数据收集与预处理**  
手动从 YouTube 收集超过 21,000 小时原始视频，筛选标准为场景运动显著、镜头连贯。使用改进版 PySceneDetect 将长视频分割为 3–15 秒片段，统一转码为 720P H.265 格式。

**层次化质量过滤**  
对每个片段计算四项指标：美学评分、亮度（公式 $L = 0.2126 R + 0.7152 G + 0.0722 B$）、文字遮挡（OCR）和运动强度。通过层次化评分策略逐级筛选，剔除低质量片段，最终保留约 270 万个片段、总计 7,089 小时动态内容。

**几何信息注释**  
以改进版 MegaSaM 为核心几何估计器：将原始深度模块替换为 UniDepth v2 与 Depth Anything v2，为每个片段生成逐帧相机姿态和深度图。同时利用 SAM2 从自适应阈值与轮廓检测得到的候选区域中提取动态掩码，并通过加速度检测器识别非物理运动波动，确保几何标注的可靠性。

**语义信息注释**  
采用 VLM + LLM 双阶段生成结构化空间感知标题（图 3）。首先由 Gemini-2.0-Flash 解析视觉内容并输出初步的运动与场景描述；随后 Qwen3-30B-A3B 结合相机姿态先验对描述进行精炼，修正方向错误（图 4），生成包含天气、时段、光照、场景类型等属性的结构化标题。此外，从相机姿态序列中提取、平滑并映射为标准电影摄影术语，形成序列化运动指令。

**均衡采样**  
原始数据集中某些运动方向（如纯平移）和场景类别过度集中。通过按运动轨迹类型和场景标签进行均衡采样，得到分布更均匀的高质量子集 SpatialVID-HQ（图 14），用于下游任务训练。

整个流水线的关键设计在于：几何注释与语义注释并非独立进行，而是通过相机姿态先验将两者耦合——LLM 在生成标题时显式接收相机运动信息，从而纠正纯视觉模型容易产生的空间方向误判。这一闭环机制使得 SpatialVID 的标注同时具备几何精度与语义丰富性，为下游模型学习显式 3D 归纳偏置提供了基础。

![[assets/figures/papers/paper_list_l828_https_arxiv_org_abs_2509_09676/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the curation pipeline. The pipeline comprises three stages: filtering, annotation, and sampling. We start from manually collected web videos with notable camera motion. In the filtering stage, raw videos are hierarchically preprocessed and filtered. The annotation stage adds geometric and semantic labels and derives motion instructions from camera poses. The sampling stage then balances clips by motion and category to form a high-quality subset (SpatialVID-HQ) with well-distributed classes for downstream tasks*

### 3.1 几何信息注释模块

SpatialVID 的几何注释管线以改进版 MegaSaM 为核心，为每个视频片段生成逐帧相机姿态、深度图和动态掩码。该模块包含三个关键子组件：

**深度估计增强**：原始 MegaSaM 的深度模块被替换为 UniDepth v2 与 Depth Anything v2 的组合，以提升在开放场景下的深度预测鲁棒性。

**动态掩码提取**：通过自适应阈值化和轮廓检测获取候选区域，从中采样锚点作为 SAM2 的提示，从而提取动态物体掩码，用于后续运动分析和深度正则化。

**轨迹质量检测**：引入基于加速度的异常检测器，识别并标记非物理性的突变运动波动，确保相机轨迹的物理一致性。

### 3.2 运动指令分解模块

从相机姿态序列中提取运动原语，经平滑处理后映射为标准电影摄影术语。具体而言，将相机外参变化分解为平移（前进/后退、左移/右移、上升/下降）与旋转（俯仰、偏航、翻滚）六自由度分量，并以键盘式图标编码运动方向。

### 3.3 语义信息注释模块

采用两阶段生成策略构建结构化空间感知标题：

1. **VLM 初描述**：Gemini-2.0-Flash 解析视觉内容，输出粗粒度的场景描述与相机运动描述。
2. **LLM 空间精炼**：Qwen3-30B-A3B 接收 VLM 输出，并显式注入相机姿态先验，修正方向错误、补充空间细节，最终生成结构化标题。

Figure 4 展示了空间增强的典型效果：LLM 利用姿态信息将 VLM 输出的错误方向“向右”纠正为“向左”。

### 3.4 关键公式

**亮度过滤公式**：用于筛选过暗或过亮片段的亮度计算标准：

$$L = 0.2126 R + 0.7152 G + 0.0722 B$$

其中 $R$、$G$、$B$ 为像素的 RGB 通道值，$L$ 为计算得到的亮度值。

**相机编码器**：在相机控制视频生成任务中，相机外参通过可学习的线性层映射到视觉令牌维度：

$$\text{cam\_encoder} \in \mathbb{R}^{12 \times d}$$

其中 $12$ 对应相机外参的维度，$d$ 为目标特征维度。编码后的特征与视觉令牌融合后注入每个 Transformer 块，实现逐帧相机控制。

**逐块投影器**：用于融合相机嵌入与视觉令牌的轻量级投影器，以恒等映射初始化：

$$\mathbb{R}^{d \times d}$$

**大型重建模型总损失**：GS-LRM 的训练损失函数结合像素级 MSE、感知 LPIPS 和深度平滑正则项：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{1} \mathcal{L}_{\mathrm{mse}} + \lambda_{2} \mathcal{L}_{\mathrm{lpips}} + \lambda_{3} \mathcal{L}_{\mathrm{reg}}$$

其中 $\lambda_{1}=1.0$、$\lambda_{2}=0.5$、$\lambda_{3}=0.25$ 为各损失项的权重系数，$\mathcal{L}_{\mathrm{mse}}$ 为像素级均方误差，$\mathcal{L}_{\mathrm{lpips}}$ 为感知损失，$\mathcal{L}_{\mathrm{reg}}$ 为深度平滑正则项。

### 3.5 模块间依赖关系

几何注释模块的输出（相机姿态、深度图）是运动指令分解和语义标题生成的前提条件。运动指令从姿态序列中派生，而语义标题的空间准确性依赖于姿态先验的注入。这种级联设计使得各模块的输出相互校验：例如，LLM 可依据姿态信息纠正 VLM 的方向误判，形成闭环的质量保障机制。

![[assets/figures/papers/paper_list_l828_https_arxiv_org_abs_2509_09676/figures/014_Figure_10.jpg]]
*Figure 10: Comparison of MegaSaM with other SLAM/3D reconstruction methods. We visualize the trajectories predicted by six representative methods. The color order ROYGBV corresponds to the progression from the initial to the final time step*

## 实验与关键发现

### 1. 数据集质量分析

在构建流程完成后，作者对 SpatialVID 及其高质量子集 SpatialVID-HQ 进行了系统的质量评估，并与现有大规模视频数据集 Panda-70M 进行了对比。如 Figure 5 所示，SpatialVID 和 SpatialVID-HQ 在美学评分（Aesthetics）、亮度（Luminance）、运动强度（Motion）等关键质量指标上呈现出更紧凑的分布形态，表明通过手动筛选与层次化过滤流程，数据集在视觉质量上具有更高的一致性和平均水平。相比之下，Panda-70M 的相机运动轨迹分布显示出严重的静态偏向——超过 80% 的视频因运动不足而无法被 MegaSaM 成功重建，而 SpatialVID 则展现出更为均衡且贴近真实场景的相机旋转与平移距离分布。

![[assets/figures/papers/paper_list_l828_https_arxiv_org_abs_2509_09676/figures/006_Figure_5.jpg]]
*Figure 5: Dataset quality comparison. Comparison of SpatialVID, its balanced subset (SpatialVID-HQ), and the Panda70M-test set processed with the same pipeline. Histograms and KDE curves reveal distribution patterns across quality metrics, showing that SpatialVID-HQ achieves consistently superior quality, validating our manual collection, filtering, and sampling process*

这一质量差异的因果根源在于数据构建策略的根本不同：SpatialVID 从逾 21,000 小时互联网视频中**手动筛选运动丰富的场景**作为起点，再经由美学、亮度、文字遮挡、运动强度四个维度的层次化过滤，从而在源头控制了数据质量。Panda-70M 的自动化收集策略虽然规模巨大，但缺乏对场景运动丰富度的主动约束，导致大量静态或近乎静态的片段混入，削弱了其在空间智能任务中的训练价值。

### 2. 相机控制视频生成

相机控制视频生成是验证空间标注质量的核心下游任务。实验采用统一的训练设置与评估协议，在 RealEstate10K（RE10K）、Sekai-Real 和 SpatialVID 三个基准上，对比了使用不同训练数据集（RealEstate10K、Sekai-Real、SpatialVID-HQ）训练的模型性能，以 TransErr 作为相机轨迹可控性的核心指标。

**Table 2 的定量结果**展示了 SpatialVID-HQ 的一致优势：

- 在 **RE10K 基准**上，SpatialVID-HQ 训练的模型取得 TransErr 7.42，略优于 RealEstate10K 自身训练的 7.46（Δ = -0.04），表明即使在 RealEstate10K 的优势领域，SpatialVID-HQ 仍能提供有竞争力的相机控制精度。
- 在 **Sekai-Real 基准**上，SpatialVID-HQ 的 TransErr 为 6.04，显著优于 Sekai-Real 训练的 6.49（Δ = -0.45），揭示了 Sekai-Real 数据集在相机运动多样性上的局限。
- 在 **SpatialVID 基准**上，SpatialVID-HQ 训练的模型达到 4.33 的最优 TransErr，相比 RealEstate10K 训练的 5.16 降低了 0.83（相对提升约 16%），充分证明了该数据集在相机可控性上的实质性增益。

这一性能提升的因果机制可归因于 SpatialVID-HQ 的两个关键设计：(1) 数据集包含丰富且均衡的相机运动轨迹分布，使模型在训练期间接触到更多样的运动模式；(2) 结构化空间感知标题集成了相机姿态先验，为模型提供了显式的 3D 归纳偏置，而非仅依赖从像素中隐式学习空间关系。

**Figure 6 的定性对比**进一步佐证了这一结论：在使用相同训练配置的情况下，基于 SpatialVID-HQ 训练的模型生成的视频在时序外观一致性上明显优于 RealEstate10K 训练的模型，且对指定相机轨迹的跟随精度更高，验证了数据集质量对生成可控性的直接影响。

### 3. 相机姿态估计微调

为检验 SpatialVID 作为预训练/微调数据的迁移价值，作者选取了两种代表性相机姿态估计方法——**VGGT** 和 **CUT3R**——在 Sintel、TUM-dynamics 和 Dycheck 三个基准上进行微调实验。

**Table 3 的结果**显示，在动态场景基准 TUM-dynamics 上，使用 SpatialVID 微调后两种方法均取得了明显的性能增益：
- VGGT 的 ATE 从 0.015 降至 0.013
- CUT3R 的 ATE 从 0.049 降至 0.040

这一改进的因果逻辑在于：原始的 VGGT 和 CUT3R 主要在静态或弱动态数据上训练，对动态场景中的相机姿态估计存在系统性偏差。SpatialVID 提供的逐帧相机姿态真值与动态掩码，使模型能够在微调阶段学习到动态场景下的稳健特征，从而缓解了静态偏置问题。值得注意的是，在 Sintel 和 Dycheck 上的增益相对有限，提示该数据集的优势主要体现在对真实世界动态场景的适配能力上。

### 4. 新视角合成

新视角合成任务采用 **GS-LRM** 作为基线框架，该框架结合了 Transformer 架构与 3D Gaussian 渲染。实验在 DL3DV 和 SpatialVID 两个测试集上，对比了使用 RealEstate10K 与 SpatialVID 子集训练的模型性能，以 PSNR 为主要指标。

**Table 4 的结果**表明 SpatialVID 训练的 GS-LRM 在两个测试集上均优于 RealEstate10K 训练的版本：
- DL3DV 上：PSNR 27.80 vs 27.01（Δ = +0.79）
- SpatialVID 上：PSNR 24.97 vs 24.13（Δ = +0.84）

这一性能提升可归因于 SpatialVID 提供的**逐帧深度图与相机姿态联合监督**。GS-LRM 的总损失函数为：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{1} \mathcal{L}_{\mathrm{mse}} + \lambda_{2} \mathcal{L}_{\mathrm{lpips}} + \lambda_{3} \mathcal{L}_{\mathrm{reg}}$$

其中 $\lambda_1=1.0$、$\lambda_2=0.5$、$\lambda_3=0.25$，正则项 $\mathcal{L}_{\mathrm{reg}}$ 包含深度平滑约束。SpatialVID 的高质量深度图使该正则项能够更有效地约束几何一致性，从而在新视角合成中产生更准确的重建结果。

### 5. 消融与失败模式分析

**数据过滤的消融验证**：Figure 5 中 SpatialVID 与 SpatialVID-HQ 的对比本质上是采样策略的消融实验。SpatialVID-HQ 通过按运动和类别进行均衡采样，在保持质量分布紧凑的同时，进一步优化了相机运动方向的均衡性。Figure 14 的环形分布图显示，原始 SpatialVID 已具备广泛的运动模式，而 SpatialVID-HQ 通过主动采样抑制了单一运动方向的过度代表，在下游任务中贡献了额外的性能增益。

**已知失败模式**：论文明确指出当前几何注释流程依赖 MegaSaM 算法，该算法在以下极端条件下仍面临挑战（Section 3.3）：
- 主要移动物体占据画面主导地位时，相机姿态估计可能被前景运动干扰
- 共线运动场景（相机运动方向与场景深度变化方向一致）下的深度估计精度下降

这些失败模式可能影响个别片段的注释精度，但论文未提供受此类问题影响的片段比例统计，该点需要进一步验证。此外，数据集的 YouTube 来源和手动筛选策略可能引入地理与内容偏好偏差，尽管规模达 7,089 小时，场景分布的代表性仍需在更广泛的下游任务中持续评估。

![[assets/figures/papers/paper_list_l828_https_arxiv_org_abs_2509_09676/figures/002_Table_1.jpg]]
*Table 1: Comparisons with previous datasets with spatial information. SpatialVID is a million-level, dynamic and open-scenario high-quality video dataset with rich annotated geometric and semantic information. Syn. denotes synthetic data; Sta. and Dyn. indicate static and dynamic scenes. In Geometry Info. column, C. denotes camera, D. denotes depth or point cloud*

![[assets/figures/papers/paper_list_l828_https_arxiv_org_abs_2509_09676/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison of camera-controlled video generation performance across different training datasets on Sekai-Real [31], RealEstate10K[82], and SpatialVID benchmarks*

![[assets/figures/papers/paper_list_l828_https_arxiv_org_abs_2509_09676/figures/009_Table_3.jpg]]
*Table 3: Comparison of Original and Fine-tuned Models for Camera Pose Estimation on Sintel [2], TUM-dynamics [48], and Dycheck [16]*

## 定位与知识库关联

### 1. 数据集谱系与定位

SpatialVID 在现有空间智能数据集中填补了一个明确的空白：**大规模、真实动态场景、开放环境、同时具备稠密几何注释与结构化语义标题的视频数据集**。Table 1 的系统对比揭示了这一空白的具体维度：

- **RealEstate10K** 等早期数据集提供相机姿态，但场景局限于静态室内房地产，缺乏动态对象和深度图。
- **Sekai-Real** 等数据集引入动态场景，但规模有限且注释维度不完整。
- **Panda-70M** 规模庞大，但如 Figure 5 所示，其超过 80% 的视频因运动不足而无法进行可靠的 3D 重建，相机轨迹分布严重偏向静态视点，缺乏训练空间智能模型所需的运动多样性。

SpatialVID 的关键区分度在于**注释的稠密性与结构化的语义-几何对齐**：每个片段不仅包含逐帧相机姿态和深度图，还拥有从相机轨迹中派生出的序列化运动指令（Section 3.4），以及经 VLM/LLM 结合相机姿态先验生成的空间感知结构化标题（Section 3.5）。这种“几何+语义”的双重注释体系，使得数据集不仅能支撑传统的 3D 重建任务，还能直接服务于相机控制视频生成等需要精细空间理解的下游任务。

### 2. 深度估计器升级的技术动机

SpatialVID 的几何注释管线对 MegaSaM 的深度模块进行了关键升级，将原始深度估计器替换为 **UniDepth v2** 与 **Depth Anything v2** 的组合（Section 3.3）。这一改动的动机源于 MegaSaM 原始深度模块在开放域互联网视频中的泛化局限：原始模块在动态对象主导或共线运动场景下容易出现深度估计退化，进而影响相机姿态估计的精度。UniDepth v2 提供了更强的度量深度估计能力，而 Depth Anything v2 则在开放场景的鲁棒性上表现更优，二者的组合有效提升了后续相机姿态估计的可靠性（Figure 10 展示了 MegaSaM 与其他 SLAM/重建方法的轨迹对比，验证了改进管线的有效性）。

### 3. 适用边界与局限

根据 verified_analysis 中的 limitations 和 open_questions，SpatialVID 的适用边界可从以下几个维度界定：

**几何注释精度边界**：当前几何注释完全依赖 MegaSaM 管线，该算法在极端条件下仍面临挑战——当场景中主要移动物体占据主导地位，或相机与场景对象呈现共线运动时，深度估计与相机姿态的精度可能下降（Section 3.3）。这意味着对于高度动态且相机运动复杂的片段（如追逐场景、快速旋转），注释质量可能存在波动，需要使用者根据具体任务进行质量筛选。

**场景分布偏差**：数据集从 YouTube 手动收集，尽管通过关键词和人工筛选覆盖了室内外多种场景（Figure 8 展示了预过滤视频的场景分布），但场景分布仍受限于筛选者的选择偏好和 YouTube 平台的内容偏向，可能存在地理区域、文化场景和拍摄设备类型的系统性偏差。在需要全球场景泛化能力的任务中，这种偏差可能构成隐性的性能瓶颈。

**传感器模态局限**：SpatialVID 的注释体系完全围绕单目 RGB 视频构建，未涉及 LiDAR、深度相机或多光谱传感器数据。对于需要绝对尺度精度或多模态融合的下游任务（如自动驾驶感知、机器人导航），数据集本身无法直接提供相应模态的监督信号。

**动态掩码与物理交互的覆盖范围**：当前动态掩码通过 SAM2 提示提取（Section 3.3），主要服务于运动分割和深度估计改进，但并未提供完整的对象级跟踪标注或物理属性标签。这意味着数据集更适合训练空间感知和相机控制能力，而非端到端的物理世界模拟或对象交互预测。

### 4. 开放问题与未来方向

基于 verified_analysis 中的 open_questions，以下方向值得后续工作关注：

- **跨模态扩展**：SpatialVID 的数据构建流程（层次化过滤→几何注释→语义增强）是否可迁移至 LiDAR 点云、深度相机序列或超高分辨率视频？这需要重新设计深度估计器和相机姿态估计器以适应不同传感器的数据特性。

- **从空间感知到世界模型**：数据集中的动态掩码和运动指令目前主要服务于空间理解任务，是否足以支持更复杂的物理交互模拟？未来能否基于 SpatialVID 的几何-语义注释体系训练端到端的世界模型，使其具备预测场景动态演变的能力？这需要在现有注释基础上增加物理属性标签（质量、材质、力学约束等）。

- **空间感知标题的质量上限**：当前结构化标题由 Gemini-2.0-Flash 解析视觉内容、Qwen3-30B-A3B 结合相机姿态精炼生成（Figure 3）。Figure 4 展示了空间增强对方向纠正的有效性，但标题的 3D 空间推理能力仍受限于 VLM/LLM 的固有局限。引入更强的 3D 推理能力（如 3D 场景图生成、空间关系推理模块）是否能进一步提升标题的空间准确性，是一个值得探索的方向。

- **注释管线的自动化与规模化**：当前管线中的人工筛选环节（手动筛选运动丰富的 YouTube 视频）是数据集质量的关键保障，但也构成了规模化的瓶颈。如何自动化识别“运动丰富且适合 3D 重建”的视频片段，同时保持与人工筛选相当的质量标准，是实现更大规模空间智能数据集的关键挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/SpatialVID_A_Large_Scale_Video_Dataset_with_Spatial_Annotations.pdf]]
