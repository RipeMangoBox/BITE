---
title: "OpenFly: A COMPREHENSIVE PLATFORM FOR AERIAL VISION-LANGUAGE NAVIGATION"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/OpenFly_A_COMPREHENSIVE_PLATFORM_FOR_AERIAL_VISION_LANGUAGE_NAVIGATION.pdf
openreview_forum_id: OKm3w71ymP
aliases:
- OA
- OpenFly
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "平台集成的多渲染引擎（UE、GTA V、Google Earth、3D GS）与高度自动化的工具链，消除了对手动数据收集与标注的依赖，可在短时间内生成大规模、多样化的轨迹与指令。"
primary_logic: "通过统一不同渲染引擎的接口并构建自动数据生成流水线，能够同时解决空中VLN的数据多样性与规模瓶颈；在此基础上，一个关键帧感知的语言-动作模型可进一步提升导航效率与精度。"
claims:
- "OpenFly整合了四种渲染引擎，大幅增强了空中VLN的场景多样性。"
- "开发的高度自动化工具链消除了对人工标注的依赖，可自动生成轨迹和指令。"
- "基于该工具链构建了包含100K条轨迹的大规模数据集，是现有最大空中VLN数据集。"
- "OpenFly-Agent在已见和未见场景上的成功率分别比次优方法高14.0%和7.9%。"
---

# OpenFly: A COMPREHENSIVE PLATFORM FOR AERIAL VISION-LANGUAGE NAVIGATION

> [!tip] 核心洞察
> 通过统一不同渲染引擎的接口并构建自动数据生成流水线，能够同时解决空中VLN的数据多样性与规模瓶颈；在此基础上，一个关键帧感知的语言-动作模型可进一步提升导航效率与精度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | OpenFly：面向空中视觉语言导航的综合平台 |
| 英文题名 | OpenFly: A COMPREHENSIVE PLATFORM FOR AERIAL VISION-LANGUAGE NAVIGATION |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=OKm3w71ymP) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | OpenFly-Agent |
| Dataset | OpenFly test-seen, OpenFly test-unseen, Real-world (真实场景) |

> [!tip] 效果简介
> - OpenFly test-seen 上，Success Rate (SR) 为 34.3%，对比 14.7% (NaVila)，变化 +19.6%。
> - OpenFly test-unseen 上，Success Rate (SR) 为 22.6%，对比 14.7% (NaVila)，变化 +7.9%。
> - OpenFly test-seen 上，Oracle Success Rate (OSR) 为 64.3%，对比 37.4% (NaVila)，变化 +26.9%。

## 概述

空中视觉语言导航（Aerial VLN）要求无人机根据自然语言指令在三维空间中飞行至指定目标。现有空中VLN数据集规模小、场景多样性有限，且依赖人工操控与标注，收集成本高、不易扩展，严重制约了大模型在该领域的发展。

针对上述瓶颈，OpenFly平台通过集成四种渲染引擎（Unreal Engine、GTA V、Google Earth、3D Gaussian Splatting）并构建高度自动化的数据生成工具链，消除了对手动数据收集与标注的依赖，可在短时间内生成大规模、多样化的轨迹与指令。基于该平台，作者构建了包含100K条轨迹的大规模空中VLN数据集，覆盖18个高质量场景，是当前规模最大的空中VLN基准。

在此基础上，本文提出OpenFly-Agent——一种关键帧感知的视觉语言导航模型。该模型通过动作转换检测和地标锚定模块选取包含关键观测的历史帧，并利用视觉token合并策略缓解文本与图像token的数量失衡问题，从而在提升导航精度的同时降低计算开销。实验表明，OpenFly-Agent在已见和未见场景上的成功率分别达到34.3%和22.6%，比次优方法分别高出14.0个百分点和7.9个百分点；在真实世界校园场景中也取得了26.09%的成功率，验证了其从仿真到现实的迁移能力。

## 背景与动机

视觉语言导航（VLN）要求智能体根据自然语言指令在三维环境中自主移动，是具身智能领域的核心任务之一。近年来，地面VLN取得了显著进展，但空中VLN仍处于早期阶段。与地面导航不同，空中无人机在三维空间中飞行，面临更复杂的运动自由度、更稀疏的地标分布以及更严苛的实时推理要求，这使得现有地面方法难以直接迁移。

当前空中VLN面临的核心瓶颈在于**数据**。现有数据集（如AerialVLN、CityNav）规模小、场景多样性有限，且严重依赖人工操控无人机并逐条标注指令，导致收集成本高昂、难以规模化扩展。这一数据稀缺性直接制约了大模型在空域导航中的发展——缺乏大规模、多样化的训练数据，模型难以学习鲁棒的视觉-语言-动作映射。

OpenFly平台正是针对这一瓶颈而设计。其核心动机在于：**通过统一多种渲染引擎的接口并构建高度自动化的数据生成流水线，从根本上消除对手动数据收集与标注的依赖，从而在短时间内生成大规模、多样化的空中VLN数据**。具体而言，该平台整合了四种互补的渲染引擎——Unreal Engine、GTA V、Google Earth和3D Gaussian Splatting（3D GS），覆盖从高保真室内场景到大规模城市场景的广泛环境类型，显著增强了场景资源的多样性。

在数据生成层面，OpenFly开发了一套完整的自动化工具链，涵盖三维点云采集、场景语义分割、飞行轨迹创建和指令生成四个关键环节。该工具链使得研究者无需实际操控无人机或进行人工标注，即可获得带有自然语言指令的飞行轨迹数据。基于此工具链，作者构建了包含**100K条轨迹**的大规模空中VLN基准数据集，覆盖18个高质量场景，是现有最大同类数据集的数倍规模（参见Table 1的统计对比）。

在模型层面，本文进一步提出了**OpenFly-Agent**，一个关键帧感知的空中VLN模型。其设计动机源于空中导航的两个独特挑战：一是无人机视角变化剧烈，并非所有历史帧都包含关键观测信息；二是视觉token数量与文本token严重失衡，导致多模态融合效率低下。OpenFly-Agent通过关键帧选择策略和视觉token合并机制分别应对这两个问题，在保持计算效率的同时提升导航精度。

> **注意**：本文中部分实验结果的绝对成功率（仿真场景34.3%，真实场景26.09%）仍处于较低水平，且所有方法在未见场景上性能均显著下降，说明空中VLN的模型泛化能力仍是亟待突破的瓶颈。

## 核心创新

OpenFly-Agent 的核心创新并非提出全新的架构范式，而是在现有视觉-语言-动作模型（基于 OpenVLA 基线，以 LLaMA2-7b 为主干）的基础上，针对空中视觉语言导航（VLN）的两个瓶颈性挑战，进行了两项关键性的“changed slots”改造：**关键帧感知的视觉输入处理**与**视觉 token 合并的模态平衡策略**。

### 关键帧感知：从均匀采样到动作-地标双锚定

传统 VLN 模型（如 OpenVLA 基线）通常采用单帧图像输入或均匀采样的历史帧，这在空中导航场景中会引入大量冗余观测，同时可能遗漏关键的动作转换点。OpenFly-Agent 将这一“视觉输入处理”槽位替换为基于**动作转换**与**地标锚定**的双重关键帧选择机制：

- **动作转换检测**：通过启发式方法识别无人机运动的变化点（如从“前进”切换到“左转”），将动作转换时刻的帧作为候选关键帧。
- **地标锚定模块**：设计了一个地标定位模块，预测指令中提及的地标在图像中的边界框，从而筛选出包含关键地标观测的帧。

这一改造的因果效应在消融实验中得到了直接验证：仅加入关键帧选择（KS），即可将成功率（SR）从基线 OpenVLA 的 16.6% 提升至 34.3%，增幅超过一倍。这清晰地表明，空中 VLN 的性能瓶颈很大程度上在于“何时看”而非“看什么”——关键帧选择通过压缩历史观测中的信息密度，使模型能够聚焦于决策真正依赖的少数关键观测。

### 视觉 Token 合并：解决模态失衡的结构性矛盾

空中 VLN 的另一个隐蔽瓶颈在于视觉与文本 token 数量的严重失衡。当模型同时处理多帧高分辨率图像和文本指令时，图像 token 数量往往远超文本 token，导致语言信息在注意力机制中被稀释。OpenFly-Agent 通过**视觉 token 合并（VTM）**策略替换了原始的图像 token 处理方式：

- **相似 token 周期性合并**：对相邻帧中相似度高的视觉 token 进行周期性的平均合并，减少跨帧冗余。
- **网格池化压缩**：在视觉编码器输出后进一步通过网格池化降低视觉 token 的总量。

消融实验显示，在关键帧选择（KS）的基础上加入 VTM（即 KS + VTM），模型性能进一步提升至 SR 34.3%、OSR 64.3%。论文明确指出，若不应用 token 合并策略，“文本与图像 token 数量之间存在严重的失衡”。这一发现揭示了多模态 VLN 模型中一个常被忽视的结构性矛盾：视觉信息的冗余不仅浪费计算资源，更会通过 token 比例失衡系统性地削弱语言理解能力。

### 创新定位与边界

上述两项改造均属于对现有 VLA 架构的“槽位替换”，而非端到端的全新设计。其有效性建立在两个前提之上：一是 OpenFly 平台提供的大规模、多样化训练数据（100K 轨迹），为关键帧选择策略提供了足够丰富的动作转换模式；二是离散的动作空间（6 个无人机动作）使得关键帧的“关键性”与动作决策之间存在可学习的映射关系。若迁移至连续动作空间或更复杂的交互式任务，这两项创新的适用性仍需进一步验证。

## 整体框架

![[assets/figures/papers/iclr26_0011_OKm3w71ymP_OpenFly_A_COMPREHENSIVE_PLATFORM_FOR_AERIAL_VISI/figures/002_Figure_2.jpg]]
*Figure 2: Framework of the automatic data generation. Multiple rendering engines are integrated to provide diverse, high-quality scenes. Built on these, several interfaces and tools are developed to enable automated generation of trajectories and instructions*

![[assets/figures/papers/iclr26_0011_OKm3w71ymP_OpenFly_A_COMPREHENSIVE_PLATFORM_FOR_AERIAL_VISI/figures/008_Figure_4.jpg]]
*Figure 4: The architecture of OpenFly-Agent. Keyframes are selected according to action transitions and the landmark grounding module to extract crucial observations as the history, with corresponding visual tokens compressed to further reduce the computational burden*

![[assets/figures/papers/iclr26_0011_OKm3w71ymP_OpenFly_A_COMPREHENSIVE_PLATFORM_FOR_AERIAL_VISI/figures/001_Figure_1.jpg]]
*Figure 1: Overview of OpenFly. This work consists of (1) the integration of 4 rendering engines, significantly enhancing the diversity of scenario resources for aerial vision-language navigation; (2) an automatic data generation toolchain, eliminating reliance on labor-intensive annotations; (3) the largest aerial VLN dataset to date, comprising 100K trajectories; and (4) a keyframe-aware VLN model, achieving superior performance in both simulated and real-world scenes*

![[assets/figures/papers/iclr26_0011_OKm3w71ymP_OpenFly_A_COMPREHENSIVE_PLATFORM_FOR_AERIAL_VISI/figures/003_Table_1.jpg]]
*Table 1: Comparisons of different VLN datasets. $N _ { t r a j }$ { : } the number of total trajectories. $N _ { v o c a b }$ { : } vocabulary size. Path Len: the average length of trajectories, measured in meters. Intr Len: the average length of instructions. $N _ { a c t } { \mathrm { : } }$ the average number of actions per trajectory*

OpenFly 平台围绕空中视觉语言导航（Aerial VLN）的**数据瓶颈**与**模型效率**两大核心问题，构建了一套从场景渲染到数据生成再到导航推理的完整流水线。其整体设计遵循“多样性场景→自动化数据→高效模型”的因果链路。

### 平台总览

平台由四个核心组件构成（Figure 1）：
1. **多渲染引擎集成**：统一了 Unreal Engine、GTA V、Google Earth 和 3D Gaussian Splatting（3D GS）四种渲染引擎的接口，大幅提升场景资源的多样性。
2. **自动化数据生成工具链**：消除了对手动标注的依赖，实现从点云采集到指令生成的端到端自动化。
3. **大规模基准数据集**：构建了包含 100K 条轨迹、覆盖 18 个高质量场景的空中 VLN 数据集，为当前最大规模。
4. **关键帧感知的导航模型（OpenFly-Agent）**：通过关键帧选择与视觉 token 合并，在仿真和真实场景中均取得领先性能。

### 数据生成流水线

Figure 2 展示了自动化数据生成的完整框架。流水线分为两大阶段：

**渲染引擎与统一接口（左侧）**：四种渲染引擎通过统一的 Lidar、Agent Movement 和 Image Acquisition API 向上层工具链暴露能力。不同引擎提供不同风格的视觉质量与场景特性——UE 提供高保真室内外场景，GTA V 提供城市场景，Google Earth 提供真实地理数据，3D GS 则支持从真实采集数据重建场景。

**自动化工具链（右侧）**依次执行四个模块：
- **三维点云采集**：通过栅格化采样重建或基于 COLMAP 的稀疏重建获取场景占位信息，构建全局体素地图 $M_{\text{global}}$。
- **场景语义分割**：提供三种方式识别地标作为航路点候选——3D 场景理解、点云投影与轮廓提取、以及手动标注。
- **自动轨迹生成**：基于 $M_{\text{global}}$ 和定制的离散动作空间（6 个飞行动作），使用 A* 算法生成无碰撞飞行轨迹。
- **自动指令生成**：将完整轨迹按动作转换点拆分为子轨迹，每个子轨迹的最后三帧图像与动作序列提交给 VLM 生成子指令，再由 LLM 整合为完整自然语言指令。人工抽检 3K 样本显示 91% 的合格率，约 9% 存在模糊描述。

### OpenFly-Agent 模型架构

Figure 4 展示了 OpenFly-Agent 的三阶段推理流水线：

**关键帧选择（Keyframe Selection）**：不同于均匀采样历史帧，模型采用启发式方法——通过识别无人机运动的动作转换点（action transition）选取候选关键帧，并结合地标定位模块（landmark grounding module）预测边界框来锚定关键观测。消融实验表明，该策略将成功率（SR）从 16.6% 提升至 34.3%。

**视觉 Token 合并（Visual Token Merging）**：将关键帧经视觉编码器处理后，对相邻帧中相似 patch 的 token 按平均方式周期性合并，再通过网格池化进一步压缩。该设计解决了文本 token 与图像 token 数量严重失衡的问题——“KS + VTM”组合在 test-seen 上取得最高 SR 34.3% 和 OSR 64.3%。

**动作预测**：压缩后的视觉 token 与指令文本 token 一同输入基于 LLaMA2-7b 的主干网络，通过动作预测头输出离散飞行动作。

### 输入输出流总结

| 阶段 | 输入 | 输出 |
|------|------|------|
| 场景渲染 | 渲染引擎选择与场景配置 | 多视角 RGB 图像、深度/点云数据 |
| 数据生成 | 点云地图、语义分割结果 | 100K 轨迹（含动作序列与自然语言指令） |
| 模型推理 | 当前观测图像、历史关键帧、指令文本 | 离散飞行动作（6 类） |

整个流水线从多引擎渲染的原始视觉数据出发，经过全自动工具链转化为结构化训练数据，最终由关键帧感知的 VLN 模型完成从语言指令到飞行控制的端到端映射。

## 核心模块与公式推导

### 3.1 自动数据生成工具链

OpenFly 的核心贡献之一是构建了一条高度自动化的数据生成流水线，从根本上消除了空中 VLN 对人工标注的依赖。该工具链由四个紧密耦合的模块组成：

**三维点云采集**：平台提供两种重建方式——栅格化采样重建（Rasterized Sampling Reconstruction）和基于图像的稀疏重建（Image-Based Sparse Reconstruction，使用 COLMAP），用于获取场景的占位信息。

**场景语义分割**：为识别可作为航路点的地标，平台集成了三种语义分割方法：三维场景理解、点云投影与轮廓提取、以及人工标注。前两种方法实现了自动化地标提取。

**自动轨迹生成**：基于全局体素地图 $M_{global}$ 和定制的离散动作空间，使用 A* 路径规划算法生成无碰撞飞行轨迹。动作空间包含六个离散动作：前进、后退、左转、右转、上升、下降和停止。

**自动指令生成**：将完整轨迹按动作转换点拆分为多个子轨迹，对每个子轨迹提取最后三帧图像和动作序列，提交给 VLM 生成包含动作和地标的子指令。所有子指令再由 LLM 整合为完整导航指令。人工抽检 3K 样本显示合格率达 91%。

### 3.2 OpenFly-Agent 模型架构

OpenFly-Agent 基于 OpenVLA 基线构建，采用 LLaMA2-7b 作为骨干网络，并配备动作预测头和地标定位头。其核心创新体现在两个关键模块：

**关键帧选择（Keyframe Selection）**：传统方法均匀采样历史帧，导致大量冗余信息。OpenFly-Agent 采用启发式方法，通过识别无人机运动的变向点来筛选候选帧，同时利用地标定位模块预测边界框，选取包含关键观测的历史帧。消融实验表明，该策略将成功率（SR）从 16.6% 提升至 34.3%。

**视觉 Token 合并（Visual Token Merging）**：空中 VLN 面临文本 token 与图像 token 数量严重失衡的问题。OpenFly-Agent 采用周期性合并相邻帧中相似 token 的策略——通过计算相似度，将高相似度的 token 按平均方式合并，有效压缩视觉 token 数量。消融对比中，“KS + VTM” 配置显著优于仅使用 KS 的配置，验证了该策略对缓解 token 失衡的关键作用。

### 3.3 公式推导

本文未提供独立编号的数学公式。模型的核心计算逻辑可概括为：

- **关键帧选择**：基于动作转移检测和地标定位得分，从历史帧序列 $\{f_1, f_2, ..., f_t\}$ 中选取子集 $\{f_{k1}, f_{k2}, ...\}$ 作为模型输入。
- **Token 合并**：对相邻帧的视觉 token 集合，计算相似度矩阵，将超过阈值的 token 对进行平均合并，压缩后的 token 与文本 token 拼接送入 LLaMA2-7b 进行动作预测。

> **注意**：上述计算流程基于文本描述推断，具体公式细节需查阅原文确认。

## 实验与分析

### 主要结果

Table 2 给出了在 OpenFly 测试集上与 7 个基线方法的全面对比。OpenFly-Agent 在已见场景（test-seen）上取得 **34.3%** 的成功率（SR），在未见场景（test-unseen）上取得 **22.6%** 的 SR，分别比最强基线 NaVila 高出 **19.6** 和 **7.9** 个百分点。Oracle 成功率（OSR）的差距更为显著：test-seen 上 OpenFly-Agent 达到 64.3%，而 NaVila 仅为 37.4%，差距达 **26.9** 个百分点。这表明模型在正确选择候选动作时具有更强的指令跟随能力，但最终执行成功率仍受限于感知和决策的累积误差。

![[assets/figures/papers/iclr26_0011_OKm3w71ymP_OpenFly_A_COMPREHENSIVE_PLATFORM_FOR_AERIAL_VISI/figures/009_Table_2.jpg]]
*Table 2: Comparison results on the test set. ‘Random’ means randomly selecting one action to execute until the ‘stop’ action is chosen. All models are retrained using our dataset*

一个关键瓶颈是**泛化能力**：所有方法在 test-unseen 上的 SR 均大幅下降，OpenFly-Agent 从 34.3% 跌至 22.6%，NaVila 从 14.7% 跌至 14.7%（未见场景反而持平，说明其本身已接近随机水平）。这一退化趋势在 OSR 上同样存在（从 64.3% 降至 56.2%），说明即使提供了正确动作候选，模型在陌生场景中的指令理解仍存在明显困难。

真实世界实验进一步验证了这一发现。在校园场景中，OpenFly-Agent 的 SR 为 **26.09%**，OSR 为 34.78%，而 Navid 仅取得 13.04% 的 SR（Figure 5a）。真实环境中的光照变化、动态遮挡和传感器噪声使得仿真到真实的迁移成为当前空中 VLN 的核心挑战。

### 消融研究

Table 3 的消融实验揭示了两个设计选择的因果作用：

![[assets/figures/papers/iclr26_0011_OKm3w71ymP_OpenFly_A_COMPREHENSIVE_PLATFORM_FOR_AERIAL_VISI/figures/013_Table_3.jpg]]

**关键帧选择（KS）是性能提升的最大杠杆。** 仅使用均匀采样的历史帧（History）时，SR 仅为 16.6%；引入基于动作转移和地标锚定的关键帧选择后，SR 跃升至 **34.3%**，提升超过一倍。随机选择关键帧（Random KS）的 SR 为 28.0%，介于两者之间，说明启发式选择策略确实捕捉到了关键观测时刻，而非简单地增加帧数。

**视觉 Token 合并（VTM）解决了模态失衡问题。** 在不使用 VTM 的情况下，文本 token 与图像 token 数量严重失衡，导致模型难以有效融合跨模态信息。加入 VTM 后，KS+VTM 组合取得了最高的 SR（34.3%）和 OSR（64.3%）。单独看 VTM 的贡献：History 加入 VTM 后 SR 从 16.6% 提升至 24.3%，说明 token 压缩本身也带来了可观的增益。

### 失败模式分析

综合实验结果，可以归纳出三类主要失败模式：

1. **未见场景的指令泛化失败。** test-unseen 上 SR 的大幅下降（34.3% → 22.6%）表明模型对训练场景中的地标和路径模式存在过拟合。自动生成的指令中约有 9% 存在模糊描述，在陌生场景中这些模糊指令可能被进一步放大。

2. **真实环境的感知漂移。** 真实世界 SR（26.09%）显著低于仿真 test-seen（34.3%），尽管两者都使用已见场景训练。Figure 6 的快照显示，真实飞行中的视角变化和地标外观差异可能导致地标定位模块失效，进而引发动作预测错误。

3. **长轨迹的累积误差。** 平均轨迹长度达 99.1 米、包含多个动作步骤，单步预测错误会沿轨迹传播。OSR 与 SR 之间的巨大差距（test-seen 上 64.3% vs 34.3%）说明即使模型能识别正确动作，执行过程中的中间决策仍可能偏离指令意图。

### 公平性说明

所有对比方法均在相同的 OpenFly 数据集上重新训练，动作空间统一为 6 个离散的无人机动作（前进、后退、左转、右转、上升、下降、停止）。真实世界实验的指令格式和评估标准与仿真实验完全一致，确保结果的可比性。

## 方法谱系与知识库定位

### 1. 与现有方法的纵向关系

OpenFly-Agent 并非凭空设计，而是站在两条技术路线的交汇点上：一是空中视觉语言导航（Aerial VLN）的专用方法线，二是通用视觉‑语言‑动作（VLA）模型的迁移应用线。

**空中VLN专用方法线**。AerialVLN 是该方向的前沿代表，其核心思路是将地面VLN的架构适配到三维飞行场景。然而，这类方法的瓶颈不在模型架构本身，而在于训练数据的规模与多样性——现有空中VLN数据集仅覆盖极少数场景，且依赖人工操控与标注，收集成本高、不易扩展。OpenFly 平台通过集成四种渲染引擎（Unreal Engine、GTA V、Google Earth、3D GS）并构建高度自动化的数据生成工具链，直接打破了这一数据瓶颈，将轨迹规模推至 100K 条（Table 1），使专用方法的潜力得以释放。

**通用VLA迁移线**。Navid 和 NaVila 代表了基于大规模预训练VLM的导航范式。Navid 以视频帧序列作为输入，NaVila 则进一步融合视觉与语言特征进行动作预测。OpenFly-Agent 在 OpenVLA 基座上构建，继承了这类方法的视觉‑语言对齐能力，但针对空中导航的两个特有挑战做了关键改造：

| 改造维度 | 基线方法（OpenVLA / NaVila） | OpenFly-Agent |
|---------|---------------------------|---------------|
| 视觉输入处理 | 单帧图像或均匀采样的视频帧 | 基于动作转移和地标锚定的关键帧序列 |
| 模态Token平衡 | 原始图像token数量与文本token严重失衡 | 周期性相似token合并 + 网格池化压缩 |

这两个改造并非孤立的设计选择，而是对空中导航本质特征的回应：无人机飞行路径长、视角变化剧烈，均匀采帧会引入大量冗余信息；同时，长指令与多帧图像叠加导致视觉token数量远超文本token，破坏了VLM内部的模态平衡。消融实验（Table 3）直接验证了这一因果链条：仅加入关键帧选择（KS）就将 SR 从 16.6% 提升至 34.3%，而在此基础上叠加视觉token合并（KS + VTM）进一步缓解了文本‑图像token失衡问题，取得了最高的 64.3% OSR。

### 2. 方法适用边界

OpenFly-Agent 的能力边界由三个因素共同界定：

**场景泛化边界**。所有方法在 test‑unseen 上的成功率均显著低于 test‑seen（OpenFly-Agent 从 34.3% 降至 22.6%，NaVila 从 14.7% 降至 14.7% 无改善），这表明当前模型学到的导航策略高度依赖训练场景的视觉与结构特征，尚未形成可迁移的空间推理能力。真实世界实验中 26.09% 的 SR（Figure 5a）进一步佐证了这一局限——即便在校园这类相对规整的环境中，sim‑to‑real 差距仍然显著。

**动作空间边界**。当前平台采用离散的 6 个无人机动作（前进、转向、上升、下降、悬停、停止），这在简化学习目标的同时也限制了飞行的精细度。连续动作空间能否更好地适应现实无人机的飞行控制，仍是开放问题。

**指令质量边界**。自动生成的指令中约 9% 存在模糊描述（91% 合格率），虽然整体可接受，但在需要精确空间推理的极端情况下可能成为导航失败的诱因。

### 3. 局限与开放问题

**泛化能力不足是当前最突出的瓶颈**。test‑unseen 上所有方法的大幅退化（Table 2）说明，单纯扩大数据规模不足以解决空中VLN的泛化问题。可能的突破方向包括：引入更强的空间推理预训练任务、构建跨场景的对比学习目标，或利用 3D GS 等新渲染引擎生成更丰富的训练分布。

**平台的任务覆盖范围有待拓展**。当前 OpenFly 聚焦于单步指令执行式的导航，尚未涉及基于对话的交互式导航、多无人机协同、或动态障碍物规避等更复杂的任务形态。平台的多引擎架构为这些扩展提供了基础设施，但相应的任务定义、评估指标和基线方法仍需构建。

**真实世界验证的生态效度有限**。现有真实世界实验仅在校园场景中进行（Figure 6），城市峡谷、山区、森林等更复杂环境的验证尚未开展。这些场景中的光照变化、纹理稀疏、GPS 信号衰减等因素可能进一步暴露当前方法的脆弱性，需手动验证。

### 4. 知识库定位

OpenFly 在 VLN 研究生态中的定位可概括为**基础设施型贡献**：它不提出全新的导航范式，而是通过统一多引擎接口和自动化数据生成流水线，将空中VLN从“小数据、手工标注”的作坊模式推入“大数据、自动生成”的工业化阶段。在此基础上，OpenFly-Agent 验证了一个关键假设——针对空中场景设计的关键帧感知与token压缩策略，能显著提升通用VLA模型在该领域的表现。这一发现为后续研究提供了明确的改进方向：在 OpenFly 的数据基座上，模型的泛化能力和动作空间粒度是下一阶段的核心攻坚目标。

## 原文 PDF

![[paperPDFs/ICLR_2026/OpenFly_A_COMPREHENSIVE_PLATFORM_FOR_AERIAL_VISION_LANGUAGE_NAVIGATION.pdf]]
