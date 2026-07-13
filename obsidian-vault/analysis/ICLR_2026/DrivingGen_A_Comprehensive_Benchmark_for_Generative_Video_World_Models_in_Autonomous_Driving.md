---
title: "DrivingGen: A Comprehensive Benchmark for Generative Video World Models in Autonomous Driving"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DrivingGen_A_Comprehensive_Benchmark_for_Generative_Video_World_Models_in_Autono_faee0d3a7a34.pdf
project_link: "https://drivinggen-bench.github.io/"
code_link: "https://github.com/nvidia-cosmos/"
aliases:
- DrivingGen
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 通过构建一个涵盖多种天气、时段、地区的多样化评估数据集，并引入针对驾驶场景的多维度指标（视频分布、轨迹分布、视觉质量、轨迹质量、时间一致性、轨迹对齐），系统性地揭示模型在视觉与机器人学视角下的真实能力。
primary_logic: 通用视频生成模型虽然视觉质量高，但常常违反物理规律；驾驶专用模型轨迹准确、物理一致性好，但视觉保真度明显不足。当前尚无模型能够同时兼顾逼真的视觉质量与精确的物理运动，这指明了驾驶世界模型的下一个关键挑战。
claims:
- 通用闭源模型（Kling 2.1, Gen-3）视觉质量与总体排名领先，但轨迹保真度一般；驾驶专用模型（Vista, Cosmos-Predict2）轨迹对齐精准，但视觉保真度靠后。
- 没有任何模型同时在视觉真实感和轨迹保真度上达到顶尖水平，现有模型呈现明显的“视觉-物理”权衡。
- 开源通用模型中，CogVideoX和Wan在视频分布指标（低FVD）上接近闭源模型，但在轨迹质量和代理一致性上表现较差。
- SLAM Reconstruction on 20 nuPlan videos 上 Success Rate = Ours w/ failure handling (20/20)
---

# DrivingGen: A Comprehensive Benchmark for Generative Video World Models in Autonomous Driving

> [!tip] 核心洞察
> 通用视频生成模型虽然视觉质量高，但常常违反物理规律；驾驶专用模型轨迹准确、物理一致性好，但视觉保真度明显不足。当前尚无模型能够同时兼顾逼真的视觉质量与精确的物理运动，这指明了驾驶世界模型的下一个关键挑战。

| 字段 | 内容 |
|------|------|
| 中文题名 | DrivingGen：面向自动驾驶的生成式视频世界模型综合基准 |
| 英文题名 | DrivingGen: A Comprehensive Benchmark for Generative Video World Models in Autonomous Driving |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=OrgL5DsU0f) · [Project](https://drivinggen-bench.github.io/) · [paper](https://arxiv.org/abs/) · [Code](https://github.com/nvidia-cosmos/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | DrivingGen |
| Dataset | SLAM Reconstruction on 20 nuPlan videos, Open-Domain Track, Ego-Conditioned Track |

> [!tip] 效果简介
> - SLAM Reconstruction on 20 nuPlan videos 上，Success Rate Ours w/ failure handling (20/20) vs Ours w/o failure handling (17/20) (+3)；ADE Ours w/ failure handling (16.84) vs Ours w/o failure handling (15.18) (+1.66)。
> - Open-Domain Track 上，FVD (视觉分布距离) Kling 2.1 (693.4) vs VaViM (1446.6) (-753.2)。
> - Ego-Conditioned Track 上，ADE (轨迹对齐误差) Vista (29.97) vs Kling 2.1 (29.97) / Gen-3 (33.39) — note: 驾驶专模整体占优 (Vista 在 ADE 上明显优于多数通用模型)。

## 概要

**问题瓶颈**：现有驾驶世界模型的评估体系存在根本性缺陷——过度聚焦视觉保真度（以FVD等指标为主），却系统性忽视了轨迹物理合理性、时间/代理级别一致性以及运动可控性等机器人学视角的关键维度。与此同时，主流评估数据集（如nuScenes、OpenDV）中超过80%的样本采集于晴天白天场景，严重缺乏全球多样性（夜间、雨雪、雾、沙尘暴）和复杂交互场景，导致评估结论无法反映模型在真实驾驶条件下的泛化能力。

**核心发现**：通过对14个生成式世界模型（涵盖闭源通用模型、开源通用模型、物理世界模型和驾驶专用模型）的系统评估，DrivingGen揭示了一个清晰的“视觉-物理”权衡困境——通用视频生成模型（如**Kling 2.1**、**Gen-3 Alpha Turbo**）视觉质量领先，但常违反物理规律，轨迹保真度一般；驾驶专用模型（如**Vista**、**Cosmos-Predict2**）轨迹对齐精准、物理一致性好，但视觉保真度明显不足。目前尚无任何模型能同时兼顾逼真的视觉质量与精确的物理运动。

**方法定位**：DrivingGen并非提出新的生成模型，而是一个面向驾驶世界模型的**综合评估基准**。其核心贡献在于：（1）构建了400样本的多样化评估数据集，刻意平衡天气（正常<60%，含雪13.1%、雾12.6%）、时段（夜间/黄昏50%）和地理区域（覆盖六大洲）；（2）引入四维评估体系——分布（视频FVD、轨迹FTD）、质量（主观/客观图像质量、轨迹运动学质量）、时间一致性（视频一致性、代理外观一致性、代理异常消失、轨迹一致性）和轨迹对齐（ADE、DTW），首次将视觉评估与机器人学评估统一在同一框架下。

**方法谱系与知识库定位**：在驾驶世界模型评估领域，DrivingGen填补了现有基准的关键空白。与仅关注视觉分布的视频生成基准（如UCF-101、Kinetics上的FVD评估）不同，DrivingGen引入了**FTD（Fréchet Trajectory Distance）**——基于MTR编码器嵌入的轨迹分布弗雷歇距离，使轨迹层面的分布评估成为可能。与现有驾驶视频基准（如nuScenes的预测任务仅评估ADE/FDE）相比，DrivingGen新增了代理异常消失检测（VLM分类）、轨迹运动学一致性分数（速度/加速度离散系数取负指数）、PWM闪烁抑制概率（MMP，基于IEEE P2020标准）等驾驶场景特化指标。在评估对象上，DrivingGen覆盖了从通用视频生成模型（**LTX-Video**、**Wan2.2-I2V**、**Hunyuan Video-I2V**、**CogVideoX**等）到物理世界模型（**Cosmos-Predict1/2**）再到驾驶专用世界模型（**VaViM**、**UniFuture**、**GEM**、**DrivingDojo**）的完整谱系，为领域提供了首个跨类别的统一比较基准。

**主要结果概要**：在Open-Domain Track中，闭源模型**Kling 2.1**以平均排名第一的成绩在视觉质量与总体表现上领先（FVD 693.4），但轨迹保真度表现中等；开源模型中**CogVideoX**在视频分布指标上接近闭源水平（FVD 621.2），但轨迹质量（0.3856 vs Kling 0.6438）和代理一致性存在明显短板。在Ego-Conditioned Track中，驾驶专用模型**Vista**在轨迹对齐指标（ADE 29.97）上显著优于多数通用模型，验证了领域专用设计在运动可控性上的优势。SLAM轨迹提取的失败恢复策略将重建成功率从85%提升至100%（ADE仅轻微增加至16.84），保证了所有样本均能参与轨迹相关度量。人类验证实验表明，视频相关指标与人类偏好高度一致，而轨迹相关指标因单目SLAM噪声和深度恢复artifact，与人类判断的一致性稍低，这指明了未来改进方向。

### 自动驾驶世界模型的评估困境

生成式视频世界模型正迅速成为自动驾驶领域的关键技术组件。这些模型以视觉、语言或动作信号为输入，生成未来的驾驶场景视频，有望为规划、仿真和数据增强提供强大的前向预测能力。然而，一个根本性的问题制约着该领域的进展：**我们缺乏一个全面、可信的基准来评估这些模型在驾驶场景中的真实能力**。

现有评估体系存在三个层面的结构性缺陷：

**第一，评估维度严重单一化。** 当前主流基准几乎完全依赖视频分布度量——最典型的是Fréchet Video Distance（FVD）——来评判模型质量。这种“一维定胜负”的范式忽视了驾驶场景的核心需求：生成的视频不仅要“看起来像”真实驾驶画面，还必须“行为上符合”物理规律。一个生成视频可能拥有极低的FVD分数，却包含违反运动学的突然加速、代理车辆的非物理消失或轨迹的空间漂移——这些致命缺陷在纯视觉度量下完全不可见。

**第二，评估视角的割裂。** 驾驶世界模型天然横跨两个领域：视觉生成（追求逼真度与画面质量）与机器人学（追求物理合理性与轨迹精度）。然而，现有工作要么从纯视觉角度评估（如视频生成基准），要么仅关注轨迹预测精度（如运动预测基准），从未将两者统一到同一个评估框架中。这种割裂导致领域无法回答一个核心问题：一个模型是否能在保持视觉真实感的同时，生成物理上可执行的驾驶轨迹？

**第三，评估数据集的系统性偏差。** 广泛使用的驾驶数据集（如nuScenes、OpenDV）存在严重的长尾缺失：超过80%的nuScenes验证数据和超过90%的OpenDV验证数据采集于晴朗白天场景。雨雪、雾霾、沙尘暴、夜间驾驶等挑战性条件几乎被系统性排除。此外，这些数据集的地理覆盖高度集中在少数地区，缺乏全球多样性。在此类数据上评估的模型，其“高性能”可能仅反映了对常见条件的过拟合，而非真正的泛化能力。

### 通用模型 vs. 专用模型：一个悬而未决的权衡

近年来，通用视频生成模型（如Kling、Gen-3、CogVideoX等）取得了惊人的视觉质量突破，但其在驾驶场景中的物理可信度尚不明确。与此同时，驾驶专用世界模型（如Vista、UniFuture）和物理世界模型（如Cosmos-Predict系列）在轨迹精度和物理一致性上表现出色，但其视觉保真度往往明显落后于通用模型。这一“视觉-物理”权衡的存在与否、程度如何，此前缺乏系统性的量化证据。

### DrivingGen的动机与定位

DrivingGen正是为解决上述评估缺口而设计。其核心理念是：**从视觉视角和机器人学视角同时评估生成式驾驶世界模型**——前者关注生成视频的真实感与整体质量，后者关注生成轨迹的物理合理性、一致性与精确度。为此，DrivingGen构建了一个涵盖多种天气、时段和地理区域的多样化评估数据集，并引入四组互补的度量维度：分布（视频FVD + 轨迹FTD）、质量（主客观图像质量 + 轨迹运动学质量）、时间一致性（视频级 + 代理级 + 轨迹级）以及轨迹对齐（ADE/DTW）。这一多维框架旨在系统性地揭示模型在“看起来好”与“行为上对”之间的真实能力边界，为下一代驾驶世界模型的发展提供清晰的方向指引。

## 核心方法与创新机理

DrivingGen 的核心创新并非提出一个新的生成模型，而是构建了一套**面向驾驶世界模型的多维度评估框架**，系统性地改变了该领域的评估范式。其关键创新点体现在两个“changed slots”上。

### 从单一视觉指标到四维全面评估

现有驾驶视频生成工作（如 Vista、DriveGAN 等）的评估高度集中在视觉保真度上，通常仅报告 **FVD（Fréchet Video Distance）** 这一单一分布指标，部分工作辅以 **ADE（Average Displacement Error）** 衡量轨迹对齐。这种评估方式存在根本性缺陷：它无法回答“生成的视频在物理上是否合理”这一驾驶世界模型的核心问题。

DrivingGen 将评估维度从单一视觉分布拓展为**四个正交维度**（Table 2）：

1. **分布维度（Distribution）**：不仅保留传统的视频级 FVD，还创新性地引入 **FTD（Fréchet Trajectory Distance）**，基于 MTR 编码器嵌入衡量生成轨迹与参考轨迹分布的整体差异，填补了轨迹分布度量的空白。
2. **质量维度（Quality）**：从主观图像质量（CLIP-IQA+）、客观图像质量（**MMP** 抑制 PWM 闪烁）以及轨迹运动学质量（舒适度、曲率平滑度、运动学可行性）三个层面进行解耦评估。
3. **时间一致性维度（Temporal Consistency）**：引入视频级一致性、代理外观一致性、代理异常消失检测以及轨迹速度/加速度一致性，这是现有基准普遍缺失的评估层面。
4. **轨迹对齐维度（Trajectory Alignment）**：在 ADE 基础上增加 **DTW（Dynamic Time Warping）**，更鲁棒地衡量生成轨迹与给定 ego 指令的匹配程度。

这一四维框架的**因果机制**在于：视觉分布指标只能回答“生成的视频看起来像不像真实驾驶数据”，而质量、一致性和对齐指标分别回答了“画面本身好不好”“时序上是否稳定”“运动是否遵循物理与控制指令”。只有四者结合，才能完整刻画一个驾驶世界模型的真实能力。

### 从偏置数据集到全球多样化评估

现有评估数据集存在严重的分布偏差：nuScenes 验证集中超过 80% 的数据、OpenDV 验证集中超过 90% 的数据均采集于正常的晴天白天场景（Fig. 2a）。这意味着在此类数据集上表现优异的模型，可能仅仅学会了“晴天白天”这一种模式，其泛化能力无从验证。

DrivingGen 构建了一个**刻意平衡的 400 样本多样化数据集**（Section 3.1, Figure 2），其设计原则直接针对上述偏差：
- **天气多样性**：正常天气占比控制在 60% 以下，雪天占 13.1%、雾天占 12.6%，并包含沙尘暴等极端天气。
- **时段多样性**：白天场景占比控制在 60% 以下，夜间/黄昏/黎明场景占比约 50%。
- **地理多样性**：覆盖全球六大区域，避免模型过拟合于特定道路布局和交通文化。
- **交互复杂性**：包含行人横穿、密集车流等复杂交互场景。

这一数据集设计的**瓶颈突破点**在于：它迫使模型在分布外（OOD）条件下暴露真实能力上限。通用视频生成模型在常规场景下视觉质量优异，但在极端天气下可能出现物理违反；驾驶专用模型在常规场景下轨迹准确，但在未见场景下可能退化。多样化的评估数据集使得这种差异得以量化和对比。

### 创新机制的内在逻辑

两个 changed slots 之间存在因果耦合：**多样化的数据集是四维评估有效性的前提**——如果数据集中 90% 是晴天白天，那么轨迹质量、时间一致性等指标的分辨力将大幅下降，因为几乎所有模型在简单场景下都能表现尚可。反之，**四维评估是多样化数据集价值的放大器**——仅有数据多样性而没有对应指标，就无法精确诊断模型在哪些维度上因场景变化而退化。

这种“数据 × 指标”的联合设计，使得 DrivingGen 能够揭示一个此前未被系统量化的核心发现：**当前不存在任何模型能同时在视觉真实感和轨迹保真度上达到顶尖水平**，通用模型与驾驶专用模型之间存在明显的“视觉-物理”权衡（Section 4.1）。这一发现直接指明了驾驶世界模型的下一个关键挑战——如何在单一模型中统一逼真的视觉质量与精确的物理运动。

DrivingGen 构建了一个面向生成式驾驶世界模型的端到端评估流水线，其核心设计原则是从**视觉视角**（生成视频的真实感与整体质量）和**机器人学视角**（生成轨迹的物理合理性、一致性与准确性）两个维度对模型进行联合审视。图1给出了该框架的完整信息流。

### 输入模态与生成阶段

流水线的入口支持三种输入模态的组合：**视觉输入**（当前帧或历史帧序列）、**语言指令**（描述驾驶场景或动作意图的文本）以及**动作/轨迹指令**（ego 车辆的未来轨迹或控制信号）。待评估的视频生成模型接收这些输入后，产生未来时间窗口内的驾驶视频预测。基准测试统一采用 **100 帧** 的预测视界，以确保不同模型在相同的时间跨度上可比。

### 轨迹提取层

生成视频完成后，DrivingGen 并不直接依赖模型输出的轨迹，而是通过一个**独立于模型的轨迹恢复模块**从视频像素中重建 ego 轨迹。具体流程为：
1. 使用 **SIFT + RANSAC + PnP** 方案（Lowe, 2004; Fischler & Bolles, 1981; Kneip et al., 2011）进行帧间位姿估计；
2. 利用 **UniDepthV2**（Piccinelli et al., 2025）恢复度量深度，将像素级运动转换为世界坐标系下的轨迹；
3. 引入**失败恢复策略**：当 SLAM 跟踪丢失时，采用常数速度外推并叠加小扰动进行补偿，将重建成功率从 85% 提升至 100%（Table 4），代价仅为 ADE 轻微增加（15.18 → 16.84），从而保证所有样本均可参与轨迹相关度量的计算。

### 四维评估套件

恢复的轨迹与生成视频一同进入评估套件，该套件按四个维度组织指标（Table 2）：

- **分布层**：评估生成样本的整体分布与真实分布的接近程度。视频层面采用经典的 **Fréchet Video Distance (FVD)**；轨迹层面引入新指标 **Fréchet Trajectory Distance (FTD)**，基于 MTR 编码器的嵌入空间计算轨迹分布的弗雷歇距离，专门适配驾驶轨迹的结构特性。
- **质量层**：从主观与客观两个角度衡量单帧/单条轨迹的质量。视频质量包含 **CLIP-IQA+**（主观感知质量）和 **Modulation Mitigation Probability (MMP)**（基于 IEEE P2020 标准的 PWM 闪烁抑制概率）；轨迹质量则聚合舒适度、运动学平滑度和曲率合理性三个子指标，形成无需参考轨迹的复合分数。
- **时间一致性层**：捕捉生成视频的时序稳定性。视频一致性通过基于光流幅度的自适应降采样策略测量帧间连贯性；代理一致性追踪周围车辆的外观保持度与异常消失率；轨迹一致性由速度和加速度的离散系数取负指数后平均得到（$S_{\mathrm{cons}} = \frac{1}{2}(S_v + S_a)$），数值越接近 1 表示运动越平稳。
- **轨迹对齐层**：在 Ego-Conditioned Track 中专用于衡量生成轨迹与给定 ego 指令的匹配程度，采用 **ADE**（平均位移误差）和 **DTW**（动态时间规整距离）作为核心指标。

### 双轨评估设计

为覆盖不同的评估需求，DrivingGen 设置了两个互补的评估轨道：
- **Open-Domain Track**：评估模型对开放域、多样化、未见过的驾驶场景的泛化能力，不提供 ego 轨迹指令；
- **Ego-Conditioned Track**：专注于轨迹可控性评估，要求模型按照给定的 ego 轨迹指令生成视频，并通过轨迹对齐度量量化其指令遵循能力。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_OrgL5DsU0f/figures/002_Figure_1.jpg]]
*Figure 1: Overview of our DrivingGen benchmark. Video models take vision, and optional language/action as inputs to generate videos. The generated videos are then passed into our evaluation suite. Four comprehensive and novel sets of metrics for both videos and trajectories (distribution, quality, temporal consistency, and trajectory alignment) are introduced to evaluate world models*

DrivingGen 的评估管线由五个核心模块串联构成，形成从视频生成到多维度打分的完整闭环。

**视频生成模型** 接受视觉输入（首帧图像）及可选的文本/动作条件，输出未来驾驶视频。基准统一设定预测时长为 100 帧，覆盖 Open-Domain Track（开放域泛化）与 Ego-Conditioned Track（轨迹可控性）两条评估线路。

**轨迹提取模块** 是连接视觉评估与机器人学评估的桥梁。其流程为：对生成视频逐帧提取 SIFT 特征，通过 RANSAC 框架下的 PnP 方法估计帧间相机位姿，并结合 **UniDepthV2** 恢复度量深度以获取尺度一致的轨迹。该模块内置失败恢复策略——当 PnP 求解失败时，采用常数速度外推并施加小扰动，将重建成功率从 85% 提升至 100%，代价仅为 ADE 轻微增加 1.66（Table 4）。

后续三个评估模块分别对应四维指标体系中的分布、质量与时间一致性，其核心公式如下。

### 分布度量

**Fréchet Trajectory Distance (FTD)** 是本文提出的轨迹分布距离指标，用于衡量生成轨迹与参考轨迹在嵌入空间中的整体差异。其数学形式为：

$$\mathrm{FTD}(X,Y) = \|\hat{\bm{\mu}}_{X} - \hat{\bm{\mu}}_{Y}\|_{2}^{2} + \operatorname{Tr}\Big(\hat{\Sigma}_{X} + \hat{\Sigma}_{Y} - 2\big(\hat{\Sigma}_{X}^{1/2}\hat{\Sigma}_{Y}\hat{\Sigma}_{X}^{1/2}\big)^{1/2}\Big)$$

其中 $\hat{\bm{\mu}}_{X}, \hat{\bm{\mu}}_{Y}$ 分别为生成轨迹集 $X$ 和参考轨迹集 $Y$ 经 MTR 编码器嵌入后的均值向量，$\hat{\Sigma}_{X}, \hat{\Sigma}_{Y}$ 为对应的协方差矩阵。该公式与 FVD 同构，但作用于轨迹嵌入空间而非视频特征空间，使得分布评估从像素域延伸到运动域。

### 质量度量

**Modulation Mitigation Probability (MMP)** 用于检测生成视频中的 PWM 闪烁伪影，遵循 IEEE P2020 标准。先计算主导频带功率比：

$$A = \frac{\sum_{f\in B(f^{\star})}\widehat{P}(f)}{\sum_{f}\widehat{P}(f) + \varepsilon}$$

其中 $\widehat{P}(f)$ 为视频时序亮度信号的功率谱，$B(f^{\star})$ 为以主导频率 $f^{\star}$ 为中心的频带。当 $A$ 低于阈值 $\tau$ 时，判定闪烁得到抑制：

$$\boxed{\mathrm{MMP} = \mathbf{1}[A < \tau]} \quad \{0,1\}$$

**轨迹曲率质量分数** 衡量路径平滑度，基于 RMS 曲率 $\kappa_{\mathrm{rms}}$ 构造：

$$S_{\mathrm{curv}} = \frac{1}{1 + \kappa_{\mathrm{rms}}}$$

曲率越小，分数越接近 1，表明轨迹越平滑。

### 时间一致性度量

**轨迹运动学一致性分数** 从速度和加速度的平稳性两个维度综合评估运动合理性：

$$S_{\mathrm{cons}} = \frac{1}{2}(S_v + S_a)$$

其中速度一致性 $S_v = \exp(-R_v)$，$R_v = \frac{\mathrm{std}(v)}{\mathrm{mean}(v)}$ 为速度的离散系数；加速度一致性 $S_a = \exp(-R_a)$，$R_a = \frac{\mathrm{std}(a)}{\mathrm{mean}(|a|)}$ 为加速度绝对值的离散系数。两者取负指数后平均，数值越接近 1 表明运动越平稳，越接近真实驾驶的行为模式。

### 轨迹对齐度量

Ego-Conditioned Track 使用标准的 **ADE（平均位移误差）** 和 **DTW（动态时间规整距离）** 衡量生成轨迹与给定 ego 轨迹指令的匹配程度，直接反映模型对运动控制的精确性。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_OrgL5DsU0f/figures/004_Table_2.jpg]]
*Table 2: Overview of metrics utilized in DrivingGen. Definition and details are in Sec. 3.2*

## 实验与关键发现

### 评估设置

DrivingGen在两条互补轨迹上评估14个生成式世界模型：**Open-Domain Track**（开放域轨迹）与**Ego-Conditioned Track**（自车条件轨迹）。前者考察模型对多样化、未见过的驾驶场景的泛化能力；后者聚焦轨迹可控性，要求模型根据给定的自车轨迹指令生成视频。所有模型统一使用100帧预测视野，评估数据集包含400个样本，刻意压低正常天气与白天场景占比（均低于60%），并引入雪（13.1%）、雾（12.6%）、夜间/黄昏/黎明（50%）等条件，覆盖全球六大区域。

### 主实验结果

**Table 3** 展示了14个模型在两条轨迹上的综合表现，核心发现如下：

**闭源通用模型视觉质量领先，但轨迹保真度一般。** **Kling 2.1**在Open-Domain Track上取得Avg. Rank第1，FVD为693.4，主观图像质量（CLIP-IQA+）和视频一致性均名列前茅；**Gen-3 Alpha Turbo**紧随其后（Avg. Rank第2）。然而，这两者在轨迹对齐指标（ADE/DTW）上表现中等，在Ego-Conditioned Track上明显落后于驾驶专用模型。

**开源通用模型视频分布逼近闭源水平，但代理一致性与轨迹质量不足。** **CogVideoX**和**Wan2.2-I2V**在FVD上分别达到621.2和609.0（Open-Domain Track），接近甚至优于部分闭源模型。但在代理一致性（Agent Consistency）和轨迹质量（Trajectory Quality）上，CogVideoX仅得0.3856，远低于Kling 2.1的0.6438，表明其生成的周围车辆运动存在明显的物理不合理性。

**驾驶专用模型轨迹精准、物理一致，但视觉保真度明显不足。** **Vista**在Ego-Conditioned Track上ADE仅29.97，DTW表现同样突出，轨迹运动学一致性高；**Cosmos-Predict2**在轨迹分布（FTD）和轨迹质量上均位列前茅。然而，这两者在视觉质量指标（主观质量、FVD）上排名靠后，生成的画面存在明显的模糊与伪影。

**物理世界模型处于中间地带。** **Cosmos-Predict1**和**Cosmos-Predict2**在视觉质量与轨迹保真度之间取得了相对平衡，但未在任何维度上达到顶尖水平。

**核心瓶颈：视觉-物理权衡。** 论文明确指出：“没有任何单一模型同时在视觉真实感和轨迹保真度上达到顶尖水平”（Section 4.1）。闭源通用模型擅长“看起来真实”，驾驶专用模型擅长“运动得正确”，二者之间存在根本性的能力鸿沟。

### 消融实验

**SLAM失败恢复策略的有效性。** **Table 4** 对比了不同SLAM流程在20段nuPlan视频上的重建表现。不加失败处理的基线成功率为17/20（85%），ADE为15.18；加入常数速度外推加小扰动的失败恢复策略后，成功率提升至20/20（100%），ADE仅轻微增加至16.84。这一消融证明恢复策略以可接受的精度代价换取了全部视频参与轨迹相关度量的能力，对基准的完整性至关重要。

**指标与人类偏好的一致性验证。** **Figure 5** 展示了DrivingGen各指标与人类偏好的相关性。视频相关指标（FVD、主观质量、视频一致性）与人类判断高度一致；轨迹相关指标（ADE、轨迹质量）与人类判断的一致性稍低，论文归因于单目SLAM的噪声与生成视频中深度恢复的artifact。这一分析为指标的可信度提供了校准参考。

### 失败模式分析

从实验结果可归纳出以下几类典型失败模式：

1. **通用模型的物理违反**：开源通用视频模型在复杂交互场景（行人横穿、密集车流）中频繁出现代理外观突变、车辆异常消失等时间不一致问题，代理一致性得分普遍偏低。
2. **驾驶专用模型的视觉退化**：Vista、VaViM等模型在夜间、雨雪条件下生成画面模糊，PWM闪烁抑制概率（MMP）较低，表明LED光源场景下存在明显的亮度调制伪影。
3. **轨迹可控性的局限**：即使是Ego-Conditioned Track中表现最好的Vista，其ADE仍达29.97（像素单位），表明当前模型在精确遵循给定轨迹指令方面仍有较大提升空间。

### 成本与效率

**Table 5** 给出了DrivingGen各组件在单张现代GPU上处理400段100帧视频的大致耗时，为不同资源预算下的基准部署提供了参考。论文明确公开了评估成本，保证了不同资源消耗模型之间的公平对比。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_OrgL5DsU0f/figures/005_Table_3.jpg]]
*Table 3: Evaluation results of 14 generative world models on our benchmark. Best results are in red region, second best are in orange region, and third best are in blue region. “*” indicates commercial closed-source models. Models fall into four categories: closed-source, open-source general video models, physical-world models, and driving-specific models*

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_OrgL5DsU0f/figures/009_Table_4.jpg]]
*Table 4: Comparison of different SLAM pipelines on 20 nuPlan videos generated with Vista. “Success rate” counts how many videos yield a valid reconstruction; ADE is the mean trajectory error over successfully reconstructed runs*

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_OrgL5DsU0f/figures/011_Figure_5.jpg]]
*Figure 5: Human Validation of Our benchmark. Our metrics closely match human preferences. Trajectory-related metrics are less accurate in comparison to humans, likely due to noisy monocular SLAM and metric-depth recovery from generated videos with artifacts*

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_OrgL5DsU0f/figures/001_Table_1.jpg]]
*Table 1: Comparison of existing video benchmarks, driving world models, and driving video benchmarks. “%” indicates the missing metrics, and “"” signifies that the evaluation is comprehensive. “Visual”, “Agent” and “Traj.” represent evaluation of images or videos, surrounding agents and vehicles’ trajectories, respectively*

## 定位与知识库关联

### 评估范式的独特定位

DrivingGen并非一个生成模型，而是一个面向**生成式视频世界模型**的综合评估基准。其核心贡献在于首次将评估从单一的视觉保真度视角拓展到**视觉+机器人学双重视角**，系统性地填补了现有评估体系的空白。Table 1明确展示了这一差异化：现有视频基准（如UCF-101、Kinetics）仅关心视觉分布，驾驶世界模型（如GAIA-1、DriveDreamer）仅关心驾驶相关指标，而DrivingGen同时覆盖视频分布、轨迹分布、视觉质量、轨迹质量、时间一致性（含代理级别）和轨迹对齐六大维度。

### 被评估模型谱系

DrivingGen评估了14个生成式世界模型，按类型可分为四个阵营：

1. **闭源通用视频生成模型**：**Kling 2.1**（快手，2024.06）、**Gen-3 Alpha Turbo**（Runway）——代表当前视频生成的视觉质量天花板，但轨迹保真度中等。
2. **开源通用视频生成模型**：**CogVideoX**（Yang et al., 2024）、**Wan2.2-I2V**（Wan et al., 2025）、**Hunyuan Video-I2V**（Kong et al., 2024）、**SkyReels-V2-I2V**（Chen et al., 2025）、**LTX-Video**（HaCohen et al., 2024）——在视频分布指标（FVD）上接近闭源模型，但在轨迹质量和代理一致性上表现较弱。
3. **物理世界视频生成模型**：**Cosmos-Predict2**（NVIDIA Cosmos, 2025）、**Cosmos-Predict1**（Agarwal et al., 2025）——定位为物理世界预测，轨迹对齐能力较强，但视觉质量与通用模型有差距。
4. **驾驶专用世界模型**：**Vista**（Gao et al., 2024）、**VaViM**（Bartoccioni et al., 2025）、**UniFuture**（Liang et al., 2025）、**GEM**（Hassan et al., 2024）、**DrivingDojo**（Wang et al., 2024）——轨迹对齐精准、物理一致性好，但视觉保真度明显不足。

### 核心发现：视觉-物理权衡

DrivingGen揭示了一个关键瓶颈：**当前没有任何模型能同时在视觉真实感和物理轨迹保真度上达到顶尖水平**。Table 3的数据清晰呈现了这一权衡：

- **Kling 2.1**在Open-Domain Track上平均排名第1，FVD为693.4，视觉质量领先，但其轨迹质量（Trajectory Quality）为0.6438，在Ego-Conditioned Track上的ADE为29.97。
- **Vista**在Ego-Conditioned Track上ADE低至29.97（与Kling并列，但在驾驶专用模型中整体轨迹对齐占优），DTW表现优异，但其视觉质量指标明显落后于通用模型。
- **开源模型中**，CogVideoX的FVD为621.2（Open-Domain），甚至优于Kling的693.4，但其轨迹质量仅0.3856，代理一致性得分也显著低于闭源模型。

这一发现指明了驾驶世界模型的下一个关键挑战：**如何将强大的视觉生成先验与精确的物理运动约束统一到同一个生成框架中**。

### 评估方法的技术贡献

DrivingGen的评估管线包含几个关键创新：

- **轨迹提取模块**：采用SIFT+PnP+RANSAC方案配合UniDepthV2进行单目SLAM重建，并引入**失败恢复策略**（常数速度外推+小扰动）。Table 4的消融表明，该策略将SLAM重建成功率从85%（17/20）提升至100%（20/20），ADE仅从15.18轻微增加到16.84，保证了所有生成视频都能参与轨迹相关度量。
- **Fréchet Trajectory Distance (FTD)**：基于MTR编码器嵌入的轨迹分布弗雷歇距离，与FVD形成对称的分布度量，专门评估生成轨迹与参考轨迹分布的整体差异。
- **轨迹质量复合指标**：包含舒适度分数（基于RMS曲率）、运动学一致性分数（速度/加速度离散系数的负指数平均），无需参考轨迹即可评估物理合理性。
- **时间一致性自适应采样**：根据光流幅度自适应降采样视频帧，对低运动视频稀疏采样、高运动视频密集采样，提升视频一致性度量的计算效率和准确性。

### 适用边界与局限

1. **数据集规模有限**：400个样本虽刻意平衡了天气（正常<60%，包含雾/雪/沙尘暴等）、时段（白天<60%）和地理区域（六大洲），但可能无法覆盖驾驶中的长尾罕见场景。
2. **缺少闭环交互评估**：当前仅支持开环生成评估，无法衡量世界模型在决策与控制闭环中的表现，这是通往端到端自动驾驶仿真的关键缺口。
3. **模态覆盖不足**：仅支持单视图前向视频，缺少多视图一致性（如环视相机）以及LiDAR、HD Map等多模态数据的评估能力。
4. **可控性与反事实推理缺失**：尚未评估模型对场景内容的可控性（如控制其他智能体行为、道路布局变更），也不包含反事实推理（counterfactual）评估——即引入假设事件后模型反应的合理性。
5. **轨迹度量的噪声瓶颈**：Figure 5的人类验证表明，视频相关指标（FVD、主观质量、视频一致性）与人类偏好高度一致，但轨迹相关指标因单目SLAM噪声和深度恢复artifact，与人类判断的一致性稍低，这是当前技术栈的固有局限。

### 开放问题

- **视觉-物理统一生成**：如何在单一模型中同时实现逼真的视觉质量与精确的物理运动？这可能需要新的架构设计，将物理先验（如运动学约束、碰撞检测）显式嵌入生成过程。
- **综合单指标设计**：能否设计一个无需人工评判的综合性分数，同时涵盖视觉分布、质量和轨迹对齐？当前的多维排名体系虽然全面，但不利于快速比较。
- **闭环安全性评估**：如何在闭环交互环境中公平比较不同驾驶世界模型的决策安全性？这需要构建标准化的对抗场景和安全性度量。
- **多模态扩展**：评估范围扩展到多视图、多传感器数据时会引入哪些新的度量挑战？例如，跨视图一致性、LiDAR点云保真度等。
- **可控性与因果评估**：如何系统评估生成模型对场景状态的可控性（如“改变前车速度”、“插入一个横穿行人”）以及反事实推理能力？这需要构建可控的场景编辑基准。

### 知识库定位

DrivingGen处于**生成式世界模型评估**与**自动驾驶仿真基准**的交叉点。它继承了视频生成评估的传统（FVD、主观质量），引入了机器人学视角的轨迹度量（ADE、DTW、运动学一致性），并首次系统性地将代理级别的时间一致性纳入评估。其方法论可被后续工作直接复用——Table 5公开了各组件在400视频×100帧规模上的运行时间估计，为社区提供了成本参考。代码已在NVIDIA Cosmos仓库开源（https://github.com/nvidia-cosmos/），项目网站（https://drivinggen-bench.github.io/）提供了完整的排行榜和可视化结果。

## 原文 PDF

![[paperPDFs/ICLR_2026/DrivingGen_A_Comprehensive_Benchmark_for_Generative_Video_World_Models_in_Autono_faee0d3a7a34.pdf]]
