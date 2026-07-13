---
title: "Asset Harvester: Extracting 3D Assets from Autonomous Driving Logs for Simulation"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/Asset_Harvester_Extracting_3D_Assets_from_Autonomous_Driving_Logs_for_Simulation.pdf
project_link: https://research.nvidia.com/labs/sil/projects/asset-harvester/
code_link: https://github.com/nvidia/asset-harvester/
aliases:
- AH
- AHE3AFADLS
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过设计面向稀疏、有限角度观测的扩散模型 SparseViewDiT，并结合前馈式三维高斯提升模块 Object TokenGS，系统性地解决了从真实驾驶日志中提取完整三维资产的核心挑战。其关键因果干预在于：利用大规模、多样化、经过精心管理的数据集（包括真实野外数据、合成域内数据和自蒸馏数据）进行多阶段训练，并引入几何感知预处理（如 Plücker 光线编...
primary_logic: 核心洞察在于，实现从自动驾驶日志生成完整三维资产并非仅靠单个生成模型，而是需要一个端到端的系统级设计。该系统将大规模对象中心化训练数据的构建、几何感知的异构传感器融合预处理、稀疏视角条件生成与三维高斯提升的联合训练，以及资产插入与场景和谐化紧密耦合。特别是，SparseViewDiT 采用灵活的序列构建（支持可变输入/输出视图）、基于 Plücker 光线的显式三维几何条件化以及线性注意力机制，克服了真实数据中视角受限、遮挡频繁和标注不精确等问题。
claims:
- Asset Harvester 通过 SparseViewDiT 从 1-4 个稀疏输入视图生成 16 个均匀分布的相机视角，并由 Object TokenGS 提升为三维高斯资产，从而在 NuRec AV Object Benchmark 上显著优于现有单视图重建基线。
- 所提出的混合数据管理策略（真实野外数据 + 合成域内数据 + 自蒸馏数据）和多阶段训练流程（通用预训练、域内后续训练、监督微调）是模型性能的关键。
- 在 Part A 的 PSNR 和 ED-R 指标上，Asset Harvester (1V, 解析相机姿态) 达到 22.23 dB 和 0.099，超过 TRELLIS (20.47 dB, 0.143) 和 HY2.1 (21.12 dB, 0.117) 等基线。
- 在 Part B 的 GPT-5.2 成对偏好评估中，Asset Harvester 对 TRELLIS 的偏好率达 73.9%，验证了其生成资产在视觉质量上的优势。
---

# Asset Harvester: Extracting 3D Assets from Autonomous Driving Logs for Simulation

> [!tip] 核心洞察
> 核心洞察在于，实现从自动驾驶日志生成完整三维资产并非仅靠单个生成模型，而是需要一个端到端的系统级设计。该系统将大规模对象中心化训练数据的构建、几何感知的异构传感器融合预处理、稀疏视角条件生成与三维高斯提升的联合训练，以及资产插入与场景和谐化紧密耦合。特别是，SparseViewDiT 采用灵活的序列构建（支持可变输入/输出视图）、基于 Plücker 光线的显式三维几何条件化以及线性注意力机制，克服了真实数据中视角受限、遮挡频繁和标注不精确等问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | 资产收割机：从自动驾驶日志中提取三维资产用于仿真 |
| 英文题名 | Asset Harvester: Extracting 3D Assets from Autonomous Driving Logs for Simulation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2604.18468) · [Code](https://github.com/nvidia/asset-harvester/) · [Project](https://research.nvidia.com/labs/sil/projects/asset-harvester/) · [paper](https://arxiv.org/abs/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | Asset Harvester |
| Dataset | NuRec AV Object Benchmark Part A, NuRec AV Object Benchmark Part B |

> [!tip] 效果简介
> - NuRec AV Object Benchmark Part A (2,206 instances) 上，PSNR (dB) 22.23 (1V, parsed cam pose) vs TRELLIS: 20.47; HY2.1: 21.12 (+1.76 vs TRELLIS; +1.11 vs HY2.1)。
> - NuRec AV Object Benchmark Part A 上，ED-R 0.099 (1V, parsed cam pose) vs TRELLIS: 0.143; HY2.1: 0.117 (lower is better; -0.044 vs TRELLIS; -0.018 vs HY2.1)。
> - NuRec AV Object Benchmark Part B (1,510 instances) 上，GPT-5.2 Pairwise Preference Rate vs TRELLIS 73.9% vs 26.1% (preferred 73.9% of the time)。

## 概要

**问题瓶颈**：现有基于神经场景重建的自动驾驶仿真方法仅能重建已观测区域，无法为可操纵的交通参与者生成完整的三维对象资产。闭环仿真中改变自车轨迹或移动车辆时，不可见区域暴露导致新视角合成失效。稀疏视角、遮挡、传感器噪声、不准确跟踪标注及非刚性人体变形进一步加剧了从单次或少量观测恢复完整三维几何与外观的难度。

**核心方法**：Asset Harvester 是一个从大规模自动驾驶日志中提取完整三维资产的端到端系统，包含三个核心模块——数据摄取模块从 NCore 格式日志中提取对象中心化裁剪并进行质量筛选；**SparseViewDiT** 基于 Sana 扩散 Transformer，以 Plücker 光线编码注入显式三维几何条件，从 1–4 个稀疏输入视图生成 16 个均匀分布的新视角；**Object TokenGS** 以前馈方式将多视图图像提升为紧致的三维高斯表示，实现快速推理。系统通过大规模混合数据（真实野外数据、域内合成数据、自蒸馏数据）的多阶段训练（通用预训练→域内后续训练→监督微调）获得鲁棒性，并配备资产插入与 DiffusionHarmonizer 光照和谐化以实现逼真闭环仿真。

**关键发现**：在 NuRec AV Object Benchmark 的 Part A（2,206 个实例）上，Asset Harvester 以单视图解析相机姿态取得 PSNR 22.23 dB、ED-R 0.099，显著优于 **TRELLIS**（Xiang et al., arXiv 2024）的 20.47 dB / 0.143 和 **Hunyuan3D 2.1**（Tencent Hunyuan3D Team, 2025）的 21.12 dB / 0.117。在 Part B（1,510 个实例）的 GPT-5.2 成对偏好评估中，Asset Harvester 对 TRELLIS 的偏好率达 73.9%。消融实验证实增加输入视图数量（1→3）可将 ED-R 从 0.098 降至 0.087，自蒸馏数据对提升低质量输入下的鲁棒性至关重要。

**方法定位**：区别于依赖单视图输入、无显式相机几何条件、主要使用合成数据训练的现有图像到三维生成基线（TRELLIS、Hunyuan3D 系列、**SAM 3D** 等），Asset Harvester 通过几何感知的稀疏多视图条件扩散、前馈式三维高斯提升、面向自动驾驶的混合数据管理及系统级资产插入和谐化，形成了从驾驶日志到可操纵三维资产的完整闭环。



自动驾驶仿真对闭环验证至关重要，其核心需求是能够在重建的三维场景中自由操纵交通参与者，同时保持逼真的视觉一致性。然而，现有基于神经场景重建的仿真方法面临一个根本性瓶颈：它们仅能重建已观测区域的场景表示，无法为可操纵的交通参与者生成**完整的三维对象资产**。当进行闭环仿真时——例如改变自车轨迹或移动场景中的车辆——这些方法会暴露不可见的物体区域（如车辆背面、侧面或顶部），从而无法提供逼真的新视角合成和物体操纵能力。

这一瓶颈的根源在于真实驾驶数据的内在挑战。自动驾驶日志中的对象观测通常是**稀疏视角、有限角度**的——一个交通参与者往往只被少数几个相机捕捉到，且视角覆盖范围狭窄。此外，真实数据中普遍存在的遮挡、传感器噪声、不准确的跟踪标注以及非刚性人体变形等问题，进一步加剧了从单一或少量观测中恢复完整三维几何与外观的难度。

现有的图像到三维生成方法（如 **TRELLIS**（Xiang et al., arXiv 2024）、**Hunyuan3D 2.1**（Tencent Hunyuan3D Team, 2025）、**SAM 3D**（SAM 3D Team et al., arXiv 2025）等）主要依赖合成数据（如 Objaverse）进行训练，缺乏对自动驾驶领域的专门适配。它们通常以单视图作为输入，且未显式利用相机几何信息作为条件信号，在面对真实驾驶场景中常见的运动模糊、欠曝光和视角受限等退化条件时，重建质量显著下降。更重要的是，这些方法缺少一个**端到端的系统级设计**，无法将大规模对象中心化训练数据的构建、几何感知的异构传感器融合预处理、稀疏视角条件生成与三维重建的联合训练，以及资产插入与场景和谐化紧密耦合。

针对上述缺口，本文提出 **Asset Harvester**，一个从大规模自动驾驶日志中提取完整三维资产的系统。其核心动机在于：通过设计面向稀疏、有限角度观测的扩散模型 **SparseViewDiT**，并结合前馈式三维高斯提升模块 **Object TokenGS**，系统性地解决从真实驾驶日志中恢复完整三维几何与外观的核心挑战。关键思路是利用大规模、多样化、经过精心管理的数据集（包括真实野外数据、合成域内数据和自蒸馏数据）进行多阶段训练，并引入几何感知预处理（如 Plücker 光线编码、相机参数注入）和鲁棒的数据增强策略，使模型能够从极其稀疏的条件视图（例如单张或少量图像）中稳定地重建高质量三维资产。



## 核心方法与创新机理

Asset Harvester 的核心创新在于通过系统级设计，将**稀疏视角条件生成**与**前馈式三维高斯提升**紧密耦合，从而在真实自动驾驶日志的挑战性条件下（稀疏观测、遮挡、传感器噪声、不准确跟踪标注）稳定提取完整的三维资产。相较于现有图像到三维的生成基线，其关键创新体现在以下三个维度的因果干预上。

### 从单视图到稀疏多视图的几何条件化生成

现有图像到三维的生成方法（如 **TRELLIS** (Xiang et al., arXiv 2024)、**Hunyuan3D 2.1** (Tencent Hunyuan3D Team, 2025)）通常以单张图像作为输入，缺乏对相机几何的显式建模，导致生成结果在多视角一致性上存在固有缺陷。Asset Harvester 的 **SparseViewDiT** 模块从根本上改变了这一范式：它支持 1–4 个稀疏输入视图，并通过 **Plücker 光线编码**和**相机参数注入**提供显式的三维几何条件。

具体而言，SparseViewDiT 将每个像素的 Plücker 光线坐标 $r_{plucker}$ 与 VAE 潜在令牌 $z$ 拼接，形成几何感知的输入令牌：

$$z_{input} = \mathrm{LinearProj}(\mathrm{Concat}(z, r_{plucker}, m))$$

其中 $m$ 为视角类型掩码，用于区分输入视图与待生成的目标视图。同时，全局相机外参通过时间嵌入注入自适应层归一化模块：

$$e_{mod} = \mathrm{MLP}(e_t + e_{cam})$$

这一设计使得模型能够在极其稀疏的条件下（例如仅 1 张输入视图）稳定生成 16 个均匀分布的新视角，为后续的三维重建提供高质量的多视图素材。消融实验证实，将输入视图数量从 1 增加到 3 时，ED-R 指标从 0.098 降至 0.087（Table 5），验证了几何条件化对重建质量的关键作用。

### 混合数据管理策略与多阶段训练

现有基线主要依赖合成数据（如 Objaverse）进行训练，缺少针对自动驾驶领域的数据管理。Asset Harvester 构建了**真实野外数据 + 域内合成数据 + 自蒸馏数据**的混合数据体系，并设计了**三阶段训练流程**（通用预训练 → 域内后续训练 → 监督微调），这是模型性能的关键因果干预。

- **真实野外数据**：从大规模 NCore 格式的驾驶日志中提取 278k 多图像集合，经过遮挡过滤、质量筛选和最远点采样，确保视角多样性和数据质量。
- **域内合成数据**：针对车辆、行人等自动驾驶关键类别，渲染 80k Objaverse 资产的合成多视图数据。
- **自蒸馏数据**：利用训练中的模型对低质量真实数据进行增强重建，生成高质量伪标签用于后续训练，显著提升模型在模糊和低质量输入下的鲁棒性。

此外，训练中引入了**几何与图像增强策略**（随机遮挡、相机参数扰动、亮度增强），使模型能够应对真实驾驶场景中的传感器噪声和标注不精确问题。

### 前馈式三维高斯提升架构

传统三维重建方法依赖于逐实例优化（如基于 Score Distillation 的方法）或需要额外的深度估计步骤，推理效率低且难以处理稀疏视角。Asset Harvester 的 **Object TokenGS** 模块采用前馈式架构，通过编码器-解码器结构和可学习的查询令牌，直接从多视图图像预测一组紧致的三维高斯表示：

$$f_{\phi} : (\Pi_{out}, X_{out}) \mapsto \mathcal{G}$$

其中 $\mathcal{G} = \{g_k\}_{k=1}^K$ 为 $K$ 个高斯点的集合，每个高斯包含中心 $\mu_k$、协方差 $\boldsymbol{\Sigma}_k$、不透明度 $\alpha_k$ 和视角相关颜色 $\mathbf{c}_k$。该架构的关键优势在于：**解耦高斯数量与输入像素数量**，使得模型能够以固定计算预算处理任意数量的输入视图，支持快速推理（Table 4 报告了推理时间统计）。

在 NuRec AV Object Benchmark 的 Part A 上，Asset Harvester（单视图，解析相机姿态）的 PSNR 达到 **22.23 dB**，ED-R 为 **0.099**，显著优于 TRELLIS（20.47 dB, 0.143）和 HY2.1（21.12 dB, 0.117）（Table 2）。在 Part B 的 GPT-5.2 成对偏好评估中，Asset Harvester 对 TRELLIS 的偏好率达 **73.9%**（Table 3），进一步验证了其在视觉质量上的优势。



Asset Harvester 是一个从大规模自动驾驶日志中提取可操纵三维资产、用于闭环仿真的端到端系统。其核心设计目标并非单纯追求重建精度，而是解决一个更根本的瓶颈：现有神经场景重建方法只能渲染已观测区域，一旦在仿真中改变自车轨迹或移动交通参与者，就会暴露不可见区域，导致新视角合成失败。Asset Harvester 通过将资产提取问题分解为三个紧密耦合的模块，系统性地克服了这一限制。

### 系统流程总览

整个 pipeline 的输入是存储于 NCore 格式的大规模自动驾驶日志，输出是可插入任意三维场景并进行动画化的完整三维资产。如图 Figure 1 所示，系统由四个核心模块串联而成：

![[assets/figures/papers/paper_list_l68_https_arxiv_org_abs_2604_18468/figures/001_Figure_1.jpg]]
*Figure 1: Overview of Asset Harvester. Starting from large-scale AV logs stored in NCore, we crop and rectify object observations, generate multiview images with SparseViewDiT, lift them into 3D assets with an Object TokenGS, and reinsert the assets into scenes with harmonization for closed-loop simulation*

1. **数据摄取模块（Data Ingestion Module）**：从 NCore 日志中提取以对象为中心的图像裁剪。该模块利用 3D 跟踪标注和传感器标定，对每个目标实例进行遮挡过滤、质量筛选和视角筛选（基于最远点采样），最终为每个实例保留最多 32 张高质量、多视角的观测图像。

2. **SparseViewDiT**：一个基于 Sana 架构的扩散 Transformer，负责从稀疏输入视图（1–4 张）生成 16 个均匀分布的新视角图像。该模块的核心创新在于引入了显式的三维几何条件化机制——通过 Plücker 光线编码和相机参数注入，使模型能够理解输入视图之间的空间关系，从而在极其稀疏的观测条件下稳定生成多视角一致的图像。

3. **Object TokenGS**：一个前馈式三维重建网络，将 SparseViewDiT 生成的多视图图像提升为紧致的三维高斯表示。该模块采用编码器-解码器架构，通过可学习的查询令牌直接预测一组三维高斯点，解耦了高斯数量与输入像素数，支持快速推理且无需逐实例优化。

4. **资产插入与和谐化（Asset Insertion and Harmonization）**：将生成的三维资产插入到 NuRec 重建的场景中，并使用 DiffusionHarmonizer 进行光照和谐化，以消除残余伪影、改善阴影并增强局部光度一致性，最终生成逼真的仿真视频。

### 模块间的数据流与依赖关系

各模块之间的信息传递遵循严格的因果链：

- **数据摄取 → SparseViewDiT**：数据摄取模块输出的是一组稀疏的、带有相机参数的对象中心化图像。这些图像的质量和视角覆盖度直接影响 SparseViewDiT 的生成效果。系统通过最远点采样确保输入视角的多样性，通过遮挡过滤和分辨率筛选保证输入质量。

- **SparseViewDiT → Object TokenGS**：SparseViewDiT 输出的是 16 张均匀分布的新视角图像及其对应的相机参数。这 16 个视角为 Object TokenGS 提供了足够的多视图信息以进行可靠的三维重建。与直接从稀疏输入进行三维重建的方法相比，这种“先生成多视图、再提升为三维”的两阶段策略有效降低了对输入视角数量和质量的敏感度。

- **Object TokenGS → 场景插入**：Object TokenGS 输出的三维高斯资产是一个显式的几何与外观表示，可直接通过高斯泼溅（Gaussian Splatting）进行可微分渲染。这为后续的场景插入和和谐化提供了灵活的操作接口，支持对资产进行旋转、平移、缩放和动画化。

### 关键设计决策的因果逻辑

Asset Harvester 的系统架构体现了三个关键的因果干预：

**干预一：从“重建已观测”到“生成完整资产”的范式转变。** 传统方法直接对稀疏观测进行三维重建，必然受限于观测覆盖范围。Asset Harvester 通过 SparseViewDiT 先生成覆盖全视角的多视图图像，再将其提升为三维资产，从根本上解决了不可见区域的几何与外观恢复问题。

**干预二：几何感知的异构传感器融合预处理。** SparseViewDiT 并非简单地接收 RGB 图像，而是将 Plücker 光线坐标和相机参数显式编码为模型条件。这种几何感知设计使模型能够理解输入图像之间的三维空间关系，而非仅依赖外观相似性进行生成。公式 $z_{input} = \mathrm{LinearProj}(\mathrm{Concat}(z, r_{plucker}, m))$ 定义了输入令牌的构建方式，将 VAE 潜在令牌、Plücker 光线坐标和视角类型掩码合并后线性投影；公式 $e_{mod} = \mathrm{MLP}(e_t + e_{cam})$ 则将全局相机外参嵌入注入到自适应层归一化模块中。

**干预三：大规模混合数据与多阶段训练。** 系统并非依赖单一数据源，而是构建了包含真实野外数据（278k 多图像集）、域内合成数据（车辆、行人）和自蒸馏数据的混合训练集，并通过通用预训练、域内后续训练和监督微调三个阶段逐步适配自动驾驶领域。这一数据管理策略是模型在稀疏、遮挡、模糊等真实场景下保持鲁棒性的关键。

### 输入输出规格

- **系统输入**：NCore 格式的自动驾驶日志，包含多传感器数据、3D 跟踪标注和传感器标定信息。
- **中间表示**：对象中心化的图像裁剪（带相机参数）、16 张均匀分布的新视角图像。
- **系统输出**：紧致的三维高斯资产 $\mathcal{G} = \{g_k\}_{k=1}^K$，其中每个高斯点 $g_k = (\mu_k, \boldsymbol{\Sigma}_k, \alpha_k, \mathbf{c}_k)$ 包含中心位置、协方差矩阵、不透明度和视角相关颜色。该资产可直接插入三维场景并进行动画化。

整个流程的推理时间统计见 Table 4，系统在单视图输入下即可在 NuRec AV Object Benchmark 上显著优于现有图像到三维生成基线（Table 2, Table 3），验证了端到端系统设计的有效性。



### 2.1 数据摄取模块 (Data Ingestion Module)

该模块负责从 NCore 格式的自动驾驶日志中提取对象中心化的图像裁剪。流程包含三个关键步骤：首先，利用 3D 跟踪标注和传感器标定信息对每个目标实例进行裁剪与矫正；其次，通过低分辨率过滤、严重边界截断过滤和重度遮挡过滤剔除低质量候选；最后，对每个实例在相机朝向空间执行最远点采样，保留至多 32 张图像，确保视角覆盖的多样性。

### 2.2 SparseViewDiT：稀疏视角条件多视图生成

SparseViewDiT 是系统的核心生成模块，基于 Sana 扩散 Transformer 架构设计，专门处理稀疏、有限角度观测下的多视图生成问题。给定 1–4 张输入视图及其相机参数，模型生成 16 张均匀分布的目标视图。

**流匹配框架。** 模型采用条件流匹配作为生成范式。定义从噪声 $x_0$ 到数据 $x_1$ 的线性插值概率路径：

$$x_t = (1 - t) x_0 + t x_1, \quad t \in [0, 1]$$

样本通过积分时间相关向量场的概率流 ODE 生成：

$$\frac{d x}{d t} = v_t(x, c)$$

向量场网络 $v_\theta$ 通过条件流匹配损失训练：

$$\mathcal{L}_{FM} = \mathbb{E}_{t, x_0, x_1, c} \left[ || v_{\theta}(x_t, t, c) - (x_1 - x_0) ||^2 \right]$$

**几何感知条件化。** 与现有单视图生成方法的关键区别在于显式的三维几何条件注入。每个输入令牌由三部分拼接后经线性投影得到：

$$z_{input} = \mathrm{LinearProj}(\mathrm{Concat}(z, r_{plucker}, m))$$

其中 $z$ 为 VAE 潜在令牌，$r_{plucker}$ 为 Plücker 光线坐标（编码每个像素对应的三维射线方向与位置），$m$ 为视角类型掩码（区分输入视图与待生成的目标视图）。全局相机外参通过时间嵌入注入自适应层归一化模块：

$$e_{mod} = \mathrm{MLP}(e_t + e_{cam})$$

这种设计使模型能够显式推理三维几何关系，而非仅依赖图像外观的统计相关性。

**灵活序列构建。** 模型支持可变数量的输入与输出视图配置，训练时随机采样输入视图数量，使单一模型可适配不同的观测稀疏程度。

### 2.3 Object TokenGS：前馈式三维高斯提升

Object TokenGS 将 SparseViewDiT 生成的多视图图像提升为紧致的三维高斯表示。三维资产被定义为一组 $K$ 个高斯点：

$$\mathcal{G} = \{g_k\}_{k=1}^K, \quad g_k = (\mu_k, \boldsymbol{\Sigma}_k, \alpha_k, \mathbf{c}_k)$$

每个高斯点 $g_k$ 包含中心位置 $\mu_k$、协方差矩阵 $\boldsymbol{\Sigma}_k$、不透明度 $\alpha_k$ 和视角相关颜色 $\mathbf{c}_k$。

**前馈重建架构。** 与需要逐实例优化的方法不同，Object TokenGS 学习一个前馈映射：

$$f_{\phi} : (\Pi_{out}, X_{out}) \mapsto \mathcal{G}$$

该映射通过编码器-解码器架构实现：编码器提取多视图图像特征，一组可学习的查询令牌通过交叉注意力与图像特征交互，解码器直接预测高斯参数。关键设计在于高斯数量 $K$ 与输入像素数解耦，由查询令牌数量决定，从而实现快速推理。

**训练目标。** 网络通过多视图重建损失端到端训练：

$$\mathcal{L}_{rec} = \mathbb{E}_{(X_{out},\Pi_{out})} \left[ \frac{1}{v_{out}} \sum_{j=1}^{v_{out}} \ell(\hat{X}_j, X_j) \right]$$

其中 $\hat{X}_j$ 为从预测高斯渲染的第 $j$ 个视图，$\ell$ 为 $\ell_1$ 损失、SSIM 损失和感知损失的组合，$v_{out}$ 为输出视图数量。

### 2.4 资产插入与和谐化

生成的三维资产通过 DiffusionHarmonizer 进行光照和谐化后插入到 NuRec 重建的场景中。该模块对插入资产与场景背景的光照不一致、阴影缺失和局部光度不连续进行校正，以生成逼真的闭环仿真视频。

### 补充图表

![[assets/figures/papers/paper_list_l68_https_arxiv_org_abs_2604_18468/figures/002_Figure_2.jpg]]
*Figure 2: Architecture overview of SparseViewDiT for sparse-view-conditioned multi-view generation*



## 实验与关键发现

### 评估基准与指标设计

论文构建了 **NuRec AV Object Benchmark**，从大规模 NCore 格式驾驶日志中经过遮挡过滤、质量筛选和视角最远点采样，最终保留 3,716 个实例，覆盖轿车、卡车/公交车、拖车/房车、施工车辆、行人五类（Table 1）。基准被划分为两部分：

![[assets/figures/papers/paper_list_l68_https_arxiv_org_abs_2604_18468/figures/003_Table_1.jpg]]
*Table 1: Number of samples per class in NuRec AV Object Benchmark*

- **Part A（2,206 实例）**：保留一个验证视图作为真值，其余视图作为输入，支持 PSNR 等依赖相机参数的参考性指标。
- **Part B（1,510 实例）**：不保留真值视图，仅提供 1–4 个输入视图，用于评估无真值条件下的生成质量。

指标层面，论文针对自动驾驶对象的特殊性设计了互补的评估体系。对于刚性对象，采用 **ED-R（Embedding Distance – Rigid）**：将渲染图像与保留的真值视图通过前景掩码对齐后，提取 DINOv3 逐块特征，计算池化嵌入的余弦距离。对于行人等非刚性对象，则使用 **ED-P（Part-aware Embedding Distance）**：通过 SAM 3D Body 检测人体关键点，将掩码分割为多个身体部位，计算各部位嵌入距离的平均值，从而更精细地衡量局部几何与外观的保真度。

### 主实验结果

**Part A 定量比较。** Table 2 展示了 Asset Harvester 与主流图像到三维生成基线在 Part A 上的全面对比。基线包括 **TRELLIS**（Xiang et al., arXiv 2024）、**Hunyuan3D 2.0**（Zhao et al., arXiv 2025）、**Hunyuan3D 2.1**（Tencent Hunyuan3D Team, 2025）和 **SAM 3D**（SAM 3D Team et al., arXiv 2025）。Asset Harvester 在单视图输入、解析相机姿态的设置下取得最优综合性能：PSNR 达到 22.23 dB，较 TRELLIS（20.47 dB）提升 1.76 dB，较 HY2.1（21.12 dB）提升 1.11 dB；ED-R 降至 0.099，显著优于 TRELLIS（0.143）和 HY2.1（0.117）。这验证了 SparseViewDiT 的几何感知条件机制和 Object TokenGS 前馈重建在有限观测下的重建优势。

**Part B 成对偏好评估。** 由于 Part B 缺少真值视图，论文采用基于 GPT-5.2 的成对偏好评估，将生成结果与基线进行盲评比较。Table 3 显示，Asset Harvester（1V，解析相机姿态）对 TRELLIS 的偏好率达 73.9%，对 HY2.1 为 66.2%，表明生成资产在视觉质量、几何完整性和纹理真实感上获得显著更高的偏好。Table 7 和 Table 8 进一步报告了估计相机参数和解析相机参数两种设置下的完整偏好矩阵，Asset Harvester 在所有配对中均保持优势。

**各类别细分表现。** Table 6 给出了各类别的 PSNR 和 ED-R 均值。Asset Harvester 在轿车、卡车/公交车、施工车辆等刚性类别上全面领先；在行人这一非刚性类别上，由于人体姿态和衣物的高度可变性，所有方法的 ED-P 指标均相对较高，但 Asset Harvester 仍保持竞争力。

### 消融实验

**输入视图数量的影响。** Table 5 报告了输入视图数量消融实验的结果。将输入视图从 1 增至 3 时，ED-R 从 0.098 降至 0.087，PSNR 从 22.23 dB 提升至 23.12 dB，表明更多条件视图为 SparseViewDiT 提供了更丰富的几何线索，进而提升了 Object TokenGS 的重建质量。当输入视图增至 4 时，增益趋于饱和，说明系统在极稀疏条件下已能有效利用有限信息。

**训练数据策略的贡献。** 论文采用三阶段训练流程：通用预训练（Objaverse 渲染数据 80k 资产）→ 域内后训练（混合真实野外数据、域内合成数据、自蒸馏数据）→ 监督微调。消融分析指出，自蒸馏数据（由模型自身在高质量输入上生成并筛选的伪真值）对提升模型在模糊、低分辨率、欠曝光等低质量真实输入下的鲁棒性至关重要。移除自蒸馏数据后，模型在困难样本上的 ED-R 和视觉质量均出现明显退化。

**推理效率。** Table 4 报告了 Asset Harvester 各模块的推理时间。SparseViewDiT 生成 16 个新视图耗时约 2.1 秒，Object TokenGS 前馈重建耗时约 0.3 秒，整体流程支持近实时的资产提取，为大规模仿真场景中的批量处理提供了可行性。

### 定性分析与可视化

**跨类别泛化能力。** Figure 3 展示了 Asset Harvester 在轿车、公交车、拖车、垃圾桶、卡车、骑行者、行人等多类对象上的野外定性结果。即使输入视图存在局部遮挡、运动模糊或非正面视角，系统仍能生成几何完整、纹理清晰的三维资产，体现了 SparseViewDiT 在稀疏视角条件下的鲁棒生成能力。

**与基线的视觉对比。** Figure 4 提供了与 TRELLIS、HY2.1 等基线的定性对比。在轿车侧面和行人背面等挑战性视角下，基线方法常出现几何畸变（如车轮变形、肢体缺失）或纹理模糊，而 Asset Harvester 保持了更完整的三维结构和更细腻的外观细节。

**分布外编辑与泛化。** Figure 6 展示了系统的分布外泛化能力：使用 Nano Banana 对自动驾驶输入图像进行编辑（如改变车辆颜色、添加涂装），保持视角和背景不变，Asset Harvester 仍能重建出与编辑一致的三维资产。这表明模型并非简单记忆训练分布，而是学习了从图像条件到三维几何的鲁棒映射。

**行人动画化。** Figure 7 展示了行人资产动画化流程：从输入观测生成 A-pose 资产，使用 SOMA 和 GEM 实现简化线性混合蒙皮，再通过 Kimodo 驱动动画。尽管当前方法受限于训练数据中有限的姿态范围，复杂动作下几何质量可能下降，但该流程初步验证了从驾驶日志中提取可操纵人体资产的可行性。

**场景插入与和谐化。** Figure 8 展示了资产插入与和谐化的完整流程：将生成的三维资产插入 NuRec 重建的三维场景中，使用 DiffusionHarmonizer 进行光照和谐化。结果显示，和谐化处理有效减少了插入边界伪影，改善了阴影一致性，提升了局部光度一致性，使合成视图更接近真实传感器数据。

### 失败模式与局限性

尽管 Asset Harvester 在整体指标上表现优异，论文也识别出若干失败模式：

1. **标注依赖瓶颈**：系统依赖准确的 3D 跟踪标注和传感器标定。当跟踪漂移或标定存在误差时，对象裁剪的精度下降，导致输入条件与真值相机姿态不匹配，生成资产出现几何错位。
2. **低质量输入退化**：强运动模糊、严重欠曝光或极低分辨率的输入图像会导致 SparseViewDiT 生成的视图纹理模糊，进而使 Object TokenGS 重建的资产丢失细节。自蒸馏数据部分缓解了该问题，但未能完全解决。
3. **非刚性重建局限**：行人资产的几何质量受限于训练数据中有限的姿态和衣物形变范围。在极端姿态或宽松衣物场景下，ED-P 指标显著升高，动画化时可能出现关节扭曲。
4. **长尾类别盲区**：当前系统仅覆盖常见的几类道路对象，对于完全未见的长尾类别（如动物、异形车辆）缺乏泛化能力，需要额外的微调或提示机制。
5. **评估指标争议**：GPT-5.2 成对偏好评估的稳定性和与人类专家判断的一致性尚未经过严格校准，可能存在未知偏差。ED-R/ED-P 依赖 DINOv3 特征空间，其对几何误差与纹理误差的敏感度分离尚不明确。

### 补充图表

![[assets/figures/papers/paper_list_l68_https_arxiv_org_abs_2604_18468/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparison with image-to-3D baselines on Part A of the NuRec AV Object Benchmark. The best and second-best results for each metric are highlighted in bold. ED-P is a non-rigid metric and is computed only for pedestrian instances*

![[assets/figures/papers/paper_list_l68_https_arxiv_org_abs_2604_18468/figures/005_Table_3.jpg]]
*Table 3: GPT-5.2 pairwise preference rates on Part B of the NuRec AV Object Benchmark. Higher percentages indicate that the corresponding method is preferred more often. AH denotes Asset Harvester*

![[assets/figures/papers/paper_list_l68_https_arxiv_org_abs_2604_18468/figures/010_Table_5.jpg]]
*Table 5: Ablation on number of input views*

![[assets/figures/papers/paper_list_l68_https_arxiv_org_abs_2604_18468/figures/011_Table_4.jpg]]
*Table 4: Asset Harvester inference-time*

![[assets/figures/papers/paper_list_l68_https_arxiv_org_abs_2604_18468/figures/012_Figure_6.jpg]]
*Figure 6: OOD image editing and generalization with Asset Harvester. We edit AV inputs with Nano Banana to create out-of-distribution objects while preserving viewpoints, object poses, and scene background, then reconstruct plausible 3D assets from the edited observations*

![[assets/figures/papers/paper_list_l68_https_arxiv_org_abs_2604_18468/figures/014_Figure_8.jpg]]
*Figure 8: Insertion and harmonization results with Asset Harvester. We reinsert generated assets into NuRecreconstructed 3D scenes and apply DiffusionHarmonizer to reduce residual artifacts, improve shadows, and enhance local photometric consistency for better scene integration*

![[assets/figures/papers/paper_list_l68_https_arxiv_org_abs_2604_18468/figures/015_Table_6.jpg]]
*Table 6: Quantitative comparison with image-to-3D baselines on Part A of the NuRec AV Object Benchmark. For each class, we compute mean over samples. PSNR in dB; ED-R is mean embedding distance*

![[assets/figures/papers/paper_list_l68_https_arxiv_org_abs_2604_18468/figures/016_Table_7.jpg]]
*Table 7: GPT-5.2 pairwise preference rates on Part B of the NuRec AV Object Benchmark. Higher percentages indicate more preferred results. In this experiment, Asset Harvester (AH) estimates camera parameters from a single input view with C-Radio linear probing*

![[assets/figures/papers/paper_list_l68_https_arxiv_org_abs_2604_18468/figures/017_Table_8.jpg]]
*Table 8: GPT-5.2 pairwise preference rates on Part B of the NuRec AV Object Benchmark. Higher percentages indicate more preferred results. In this experiment, Asset Harvester (AH) parses object camera from NCore scene for the single view input*



## 定位与知识库关联

### 1. 方法沿革与基线关系

Asset Harvester 的核心任务——从稀疏、非受控的自动驾驶日志图像中提取完整三维对象资产——处于**稀疏视角三维重建**、**图像到三维生成**和**自动驾驶仿真**三个领域的交叉点。其设计选择与现有基线形成清晰的对比关系。

**与图像到三维生成基线的对比。** 论文将 Asset Harvester 与四类公开可用的图像到三维生成方法进行了系统比较：**TRELLIS** (Xiang et al., arXiv 2024)、**Hunyuan3D 2.0** (Zhao et al., arXiv 2025)、**Hunyuan3D 2.1** (Tencent Hunyuan3D Team, 2025) 和 **SAM 3D** (SAM 3D Team et al., arXiv 2025)。这些基线代表了当前图像条件三维生成的主流范式，但它们共享两个关键局限：(1) 设计上假定单视图输入，缺乏对多视图几何约束的显式建模；(2) 训练数据以合成三维资产库（如 Objaverse）为主，与真实自动驾驶场景中的光照、遮挡和传感器噪声分布存在显著域差异。

Asset Harvester 在三个关键维度上构成了对上述基线的系统性改进：

- **输入条件机制的几何感知化**（Section 2.2）：将单视图条件扩展为 1–4 个稀疏视图，并通过 Plücker 光线编码和相机外参嵌入注入显式三维几何先验。这一设计使模型能够利用多视图间的对极几何约束，而非仅依赖单视图外观线索推断三维结构。消融实验（Table 5）证实，输入视图数从 1 增至 3 时，ED-R 从 0.098 降至 0.087，验证了几何条件增强的因果效应。

- **训练数据管理的领域针对性**（Section 3）：区别于基线主要依赖合成数据，Asset Harvester 构建了三层数据金字塔——大规模 Objaverse 通用预训练（80k 资产）、域内合成数据（车辆、行人等道路对象）和真实驾驶日志自蒸馏数据（278k 多图像集）。自蒸馏数据被证明对提升模型在模糊和低质量输入下的鲁棒性至关重要（Section 3.2, 3.3）。

- **三维重建的前馈式高斯提升**（Section 2.3）：Object TokenGS 通过可学习查询令牌直接预测一组紧凑的三维高斯，解耦了高斯点数量与输入像素数，避免了基线中常见的逐实例优化（如 Score Distillation Sampling）或依赖额外深度估计的瓶颈，支持快速推理。

定量结果（Table 2）表明，在 NuRec AV Object Benchmark Part A 上，Asset Harvester（单视图、解析相机姿态）在 PSNR 上达到 **22.23 dB**，显著优于 TRELLIS（20.47 dB）和 HY2.1（21.12 dB）；在无参考嵌入距离 ED-R 上达到 **0.099**，低于 TRELLIS（0.143）和 HY2.1（0.117）。在 Part B 的 GPT-5.2 成对偏好评估中（Table 3），Asset Harvester 对 TRELLIS 的偏好率达 **73.9%**，进一步验证了生成资产在视觉质量上的优势。

**与神经场景重建方法的互补关系。** 现有基于神经辐射场（NeRF）或三维高斯泼溅（3DGS）的自动驾驶仿真方法（如 NuRec 本身）仅能重建已观测区域，无法为可操纵的交通参与者生成完整三维对象资产。Asset Harvester 并非替代这些方法，而是作为其上游资产供应模块，通过“资产插入与和谐化”模块（Section 2）将生成的三维高斯资产注入 NuRec 重建的场景中，并使用 DiffusionHarmonizer 进行光照和谐化（Figure 8），实现闭环仿真中的新视角合成和物体操纵。

### 2. 适用边界与关键局限

论文明确指出的局限（Section 6）和从实验设计中可推断的适用边界包括：

**数据依赖性边界。** 当前系统深度依赖准确的 3D 跟踪标注和传感器标定（Section 2.1）。标注噪声或传感器不同步会直接降低生成资产的质量。此外，整个流程与 NVIDIA 生态（NCore、NuRec、Sana、C-Radio 等）强耦合，在异构平台上的可复现性存疑。

**对象类别泛化边界。** 系统当前覆盖的类别限于车辆、行人、骑行者、施工机械等常见道路对象（Table 1），难以泛化到完全未见的长尾类别。Figure 6 展示了通过图像编辑（Nano Banana）创建分布外对象并重建的定性实验，但这依赖人工干预，并非自动化方案。

**非刚性重建质量边界。** 对行人等非刚性物体的重建受限于训练数据中有限的姿态和衣物形变范围。Figure 7 的行人动画结果虽然展示了将输入转换为 A-pose 资产并驱动动画的可行性，但复杂动作下的几何质量仍可能下降。ED-P 指标专门针对行人实例设计（Section 4.2），但其数值表现与刚性类别仍存在差距（Table 6）。

**输入质量敏感性。** 生成资产的细节保真度受输入图像质量影响显著。强运动模糊或严重欠曝光的输入会导致纹理模糊，这是数据驱动方法的固有局限。

### 3. 开放问题

论文在 Section 6 中提出了若干开放问题，结合方法设计中的隐含假设，可归纳为以下方向：

**弱监督与自监督学习。** 如何减轻对精确 3D 跟踪标注的依赖，使系统能够利用弱监督或自监督信号从更大规模驾驶数据中学习？当前系统对标注质量的敏感性（Section 2.1 的遮挡过滤和质量筛选）暗示，引入自监督几何一致性约束可能是一个有前景的方向。

**非刚性重建的精度与效率权衡。** 在保持实时推理速度（Table 4 报告了推理时间统计）的同时，如何进一步提升非刚性人体重建的几何准确性和动画化自然度？当前 Object TokenGS 的前馈设计牺牲了一定的逐实例优化精度以换取速度，针对非刚性类别的混合优化策略值得探索。

**闭环仿真评估指标。** 生成资产在闭环仿真中对下游感知、规划模块的影响如何量化？当前评估（Part A 的 PSNR/ED-R 和 Part B 的 GPT-5.2 偏好）仍聚焦于重建质量本身，缺乏面向仿真可信度的闭环评估指标。这是一个系统级开放问题。

**多模态传感器融合。** 能否融合 LiDAR 等互补传感器数据，在输入稀疏图像的基础上提供几何先验以提升重建完整度？当前方法仅使用图像输入，但自动驾驶日志通常包含多模态数据。

**快速类别扩展。** 面向完全开放的类别，能否通过少量示例的快速适配（例如微调或提示）扩展资产收割的范围？Figure 6 的分布外编辑实验暗示了这种可能性，但尚未形成系统性方法。

**合成-真实域差异。** 合成数据训练与真实数据分布间的域差异是否可以通过更强的物理渲染或风格迁移进一步缩小？当前混合数据策略（Section 3.2）已部分缓解此问题，但域间隙仍然存在。

**评估协议的稳定性。** 当前 GPT-5.2 成对偏好评估的稳定性和与人类专家判断的一致性如何，是否存在潜在偏差？这是一个影响所有采用 LLM-as-Judge 方法的研究的共性问题。



## 原文 PDF

![[paperPDFs/arxiv_2026/Asset_Harvester_Extracting_3D_Assets_from_Autonomous_Driving_Logs_for_Simulation.pdf]]
