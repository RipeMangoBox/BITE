---
title: "HUMAPS-4D: A Multimodal Dataset for HUman Motion Analysis with Physiological and Semantic informations"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HUMAPS_4D_A_Multimodal_Dataset_for_HUman_Motion_Analysis_with_Physiological_and_Semantic_informations.pdf
project_link: "https://humaps4d.wp.imt.fr/"
code_link: null
aliases:
- H4
- HUMAPS-4D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过系统性采集32名受试者30种动作的多模态同步数据，并配以临床语义标注，构建了首个弥合计算机视觉与生物力学鸿沟的大规模数据集。
primary_logic: 足底压力与肌电等可穿戴信号携带丰富的生物力学约束，结合语义描述可作为替代视觉的强先验，实现隐私保护下的细粒度运动理解。
claims:
- 数据集同步整合了运动捕捉、多视角视频、IMU、足底压力、表面肌电和高层语义标注。
- 该数据集提供了低层生理信号与高层人体运动描述符的独特配对。
- HUMAPS‑4D 是首个在统一协议下融合视觉、可穿戴和生物力学数据的大规模资源。
- HUMAPS‑4D LOSO 动作识别 上 Accuracy = 90.33 ± 4.3 (Insoles+MoCap fusion)
---

# HUMAPS-4D: A Multimodal Dataset for HUman Motion Analysis with Physiological and Semantic informations

> [!tip] 核心洞察
> 足底压力与肌电等可穿戴信号携带丰富的生物力学约束，结合语义描述可作为替代视觉的强先验，实现隐私保护下的细粒度运动理解。

| 字段 | 内容 |
|------|------|
| 中文题名 | HUMAPS‑4D：一个用于人体运动分析的多模态数据集 |
| 英文题名 | HUMAPS-4D: A Multimodal Dataset for HUman Motion Analysis with Physiological and Semantic informations |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Dabrowski_HUMAPS-4D_A_Multimodal_Dataset_for_HUman_Motion_Analysis_with_Physiological_CVPR_2026_paper.html) · [Project](https://humaps4d.wp.imt.fr/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | HUMAPS‑4D 多模态数据集及其基准任务 |
| Dataset | HUMAPS‑4D LOSO 动作识别, HUMAPS‑4D 4‑fold CV 3D姿态估计 |

> [!tip] 效果简介
> - HUMAPS‑4D LOSO 动作识别 上，Accuracy 90.33 ± 4.3 (Insoles+MoCap fusion) vs 82.71 ± 3.9 (Insoles only) (+7.62)。
> - HUMAPS‑4D 4‑fold CV 3D姿态估计 上，MPJPE (cm) 31.1 ± 0.8 (足底压力→全身姿态)。

## 概要

**问题瓶颈**：现有三维人体运动数据集长期处于“视觉驱动”与“生物力学评估”两条割裂的轨道上——前者侧重多视角视频与运动捕捉的配准，后者聚焦步态、关节力矩、肌电等精密测量，但二者从未在统一的采集协议下同步整合，更缺乏高层语义标注。这一断裂导致三个后果：第一，基于纯视觉的全身姿态估计在遮挡、隐私敏感场景（如居家康复）下鲁棒性不足；第二，可穿戴信号（足底压力、表面肌电）虽携带丰富的生物力学约束，却因缺少大规模、多动作的配对真值而难以被深度学习模型充分利用；第三，面向临床运动评估的细粒度语义（如“减痛步态”“共济失调”）与传感器数据之间缺乏可学习的映射桥梁。HUMAPS‑4D 正是针对这一“数据模态与语义的多重缺失”瓶颈而构建。

**核心思路与方法定位**：该工作并非提出新的模型架构，而是通过系统性采集 32 名健康受试者执行 30 种动作（涵盖行走、上下楼梯、单腿站立、交互等类别）的同步多模态数据，构建了首个大规模“视觉‑可穿戴‑语义”一体化数据集。其采集管线包括：11 台 Qualisys 红外/彩色相机（120 Hz）提供 42 个三维关节真值与 26 个推断关节角度；3 台 720p RGB 相机提供多视角视频；16 通道 Delsys 表面肌电（1259 Hz，内含 148 Hz IMU）；Moticon OpenGo 智能鞋垫（每足 16 个压力传感器，100 Hz，含六轴 IMU）；以及三层时间对齐的语言语义标注（临床运动评估叙述、原子动作描述、详细运动描述符）。所有模态共享统一时钟，并提供内外参标定参数与人体测量数据。在方法谱系上，HUMAPS‑4D 弥合了 **SolePoser**（Wu et al., UIST 2024）等从足底压力恢复姿态的单模态基线所依赖的小规模采集与**视觉驱动数据集**（如 Human3.6M、3DPW）之间的空白，为跨模态学习、隐私保护姿态估计和运动技能评估提供了标准化基准。

**关键发现与主要结果**：论文设置了两项基准任务以验证数据集的价值。在动作识别任务上，采用留一受试者交叉验证（LOSO），仅使用足底压力信号的 **ST‑GCN**（Yan et al., AAAI 2018）分类器达到 82.71% 准确率，而融合足底压力与运动捕捉关节数据的模型进一步提升至 90.33%，表明可穿戴信号本身已携带强判别力，且多模态融合具有显著增益。在更具挑战性的“足底压力→全身 3D 姿态”任务上，受 **SolePoser** 启发的双流 Transformer 基线在 4 折交叉验证下总 MPJPE 为 31.1 cm，其中静态姿势类误差较低，而动态交互类动作（如抛接球）误差升至 34.0 cm 以上，揭示了单模态输入的固有限制。这些结果表明，HUMAPS‑4D 为“以可穿戴信号替代视觉”这一隐私保护范式提供了真实的困难标尺，同时也暴露了当前模型在时序一致性与物理合理性上的不足。

**局限与开放问题**：数据集目前仅覆盖 18–42 岁健康成年人，尚未纳入病理步态、老年或儿童人群；所有采集在受控室内环境完成，户外自由生活场景下的泛化能力待验证。姿态估计的 31 cm 级误差也指出，如何将语义标注、肌肉协同等先验显式注入模型以大幅压缩误差，是下一步的核心挑战。此外，跨模态融合的最优策略（早融合、晚融合、对比学习）是否因任务而异，以及数据集所附基线代码与预训练模型的开源计划，将直接影响社区的后续推进速度。

人体运动分析是计算机视觉与生物力学交叉领域的核心问题，其应用涵盖临床步态评估、运动康复、人机交互和具身智能。然而，当前研究面临一个关键瓶颈：**现有数据集未能同时集成视觉、可穿戴生物力学传感器和高层语义信息**，导致模型难以在隐私敏感场景下实现细粒度的全身三维运动理解。

具体而言，现有资源可分为两个相互割裂的阵营。第一类数据集（如 Human3.6M、3DPW）以视觉驱动为主，强调多视角视频与运动捕捉（MoCap）的同步，但缺乏肌肉激活、足底压力等底层生理信号。第二类数据集（如自建步态库）聚焦生物力学评估，提供表面肌电（sEMG）、测力台等精确测量，却通常规模小、动作单一，且不具备视觉模态。**HUMAPS‑4D** 正是在这一缺口下提出的——它首次在统一采集协议下，将运动捕捉、多视角 RGB 视频、IMU、足底压力鞋垫、16 通道 sEMG 以及三层时间对齐的语义标注整合为单一资源（Table 1），涵盖 32 名受试者的 30 种日常与功能性动作，总计约 14 小时记录和超过 570 万帧同步图像（Figure 1）。

该数据集的核心动机源于一个因果洞察：**足底压力与肌电等可穿戴信号携带丰富的生物力学约束**。足底压力分布直接反映地面反作用力、重心转移和步态相位，而 sEMG 编码了肌肉协同模式。当这些信号与高层运动描述符（如“缓慢下蹲并保持平衡”）配对时，它们构成了替代视觉的强先验——在摄像头不可用或隐私受限的环境中，模型仍可从中恢复全身姿态或识别动作类别。这一思路在先前工作中已有初步探索：**SolePoser**（Wu et al., UIST 2024）使用双流 Transformer 从鞋垫压力回归 3D 姿态，**P2P-Insoles** 采用类似架构但仅依赖 MoCap 信号，缺乏上下文线索。然而，这些方法受限于小规模、单一场景的私有数据，无法系统评估跨动作、跨受试者的泛化能力。

HUMAPS‑4D 的独特价值在于它提供了**低层生理信号与高层语义描述符的显式配对**。数据集附有三层语言语料库：临床风格的运动评估叙述、原子动作描述和详细运动描述符（Figure 3）。这种设计使研究者可以探索从“压力-姿态”的纯回归，到“压力+语言→姿态”的多模态推理范式跃迁。基线实验已初步验证了该资源的潜力：在留一受试者（LOSO）协议下，仅用鞋垫压力的动作识别准确率为 82.71%，融合 MoCap 后提升至 90.33%（Table 2）；而从足底压力恢复全身 3D 姿态的总 MPJPE 约为 31.1 cm（Table 3），虽仍远未实用，但为跨模态学习设立了清晰的基准线。

综上，HUMAPS‑4D 的提出并非简单的数据堆砌，而是针对“隐私保护下细粒度运动理解”这一长期目标，系统性构建了首个弥合计算机视觉与生物力学鸿沟的大规模多模态平台。

## 核心方法与创新机理

HUMAPS‑4D 的核心创新不在于提出新的模型架构，而在于**构建了首个在统一采集协议下深度融合视觉、可穿戴生物力学传感器与高层语义的大规模多模态人体运动数据集**，从而直接回应了领域内长期存在的瓶颈：现有数据集要么侧重视觉驱动（缺乏生理信号），要么侧重生物力学分析（缺乏视觉与语义），二者从未在同一批受试者、同一批动作上同步记录。这一鸿沟的填补，使隐私保护下的细粒度运动理解成为可能——足底压力与肌电等可穿戴信号本身携带丰富的生物力学约束，结合语义描述后，可作为替代视觉的强先验。

具体而言，该工作相对于既有数据资源（参见 **Table 1** 的系统对比）实现了以下关键突破：

1. **模态整合的质变**：首次将运动捕捉（42个3D关节，120 Hz）、多视角RGB视频（3台720p@120 Hz相机，含内外参）、16通道表面肌电（1259 Hz，内含IMU）、双足足底压力（16传感器×2，100 Hz，含IMU）以及**三层时间对齐的语言语义标注**（临床运动评估叙述、原子动作描述、详细运动描述符）在32名受试者、30种动作上同步采集。此前数据集最多覆盖其中2–3种模态，且缺乏语义层。

2. **从“信号”到“语义”的桥梁**：数据集提供了低层生理信号与高层人体运动描述符的独特配对。这种配对使得模型可以学习从足底压力或肌电模式直接映射到动作语义或全身姿态，而不依赖视觉输入——这正是隐私敏感场景（如居家康复、更衣室）的核心需求。

3. **标准化预处理与基准定义**：提供了跨受试者归一化方案（关节位置骨盆居中+人体测量缩放、EMG参考收缩归一化、足底压力按最大压力或体重归一化），并定义了动作识别与3D姿态估计两个基准任务，采用严格的LOSO和4折交叉验证协议，为后续研究建立了可复现的评估框架。

值得强调的是，HUMAPS‑4D 本身是**数据集贡献**，而非算法贡献。论文中使用的动作识别模型（**ST‑GCN**，Yan et al., AAAI 2018）和姿态估计基线架构（参考 **SolePoser**，Wu et al., UIST 2024）均为现有方法，其作用仅在于验证数据集的有效性和挑战性。因此，该工作的“changed slots”不体现在模型模块的替换，而体现在**任务定义空间的扩展**：从单模态或弱配对的运动分析，拓展到多模态同步、语义对齐的全身3D运动理解。

**证据强度**：数据集规模与模态完整性的声明有明确的采集协议和 Table 1 对比支撑（置信度0.98）；语义标注的三层结构有 Figure 3 和对应描述佐证（置信度0.95）；归一化公式和基准任务定义在原文中有显式的数学表述和实验配置说明（置信度0.95–0.98）。局限性方面，受试者仅覆盖健康成年人（18–42岁），未包含疾病、老年或儿童人群，且所有采集均在受控室内环境完成，户外泛化能力尚未验证。

HUMAPS‑4D 的核心贡献在于构建了一个多模态同步采集与标注流水线，而非提出新的算法架构。该流水线围绕“弥合计算机视觉与生物力学鸿沟”这一目标，将**视觉信号、可穿戴生理信号与高层语义**在统一协议下整合，为下游任务提供标准化数据基础。

### 数据采集流水线

采集流程以受试者执行预定动作为中心，同步记录以下模态：

| 模块 | 设备与规格 | 输出信号 | 角色 |
|------|-----------|---------|------|
| **运动捕捉 (MoCap)** | Qualisys 系统，11台 Miqus M3 相机（3 RGB+IR, 8 IR），120 Hz | 42个3D标记点位置 + 26个推断关节角度 | 提供3D姿态真值 |
| **多视角 RGB 视频** | 3台 Miqus M3 相机，720p@120 Hz | 三视角同步视频 + 内外参 | 支持三维场景重建与视觉分析 |
| **表面肌电 (sEMG)** | Delsys Trigno 无线系统，16电极，1259 Hz | 肌肉激活信号 + 内置IMU（148 Hz） | 记录肌肉层面的生物力学约束 |
| **足底压力 (IPS)** | Moticon OpenGo 智能鞋垫，16传感器×2，100 Hz | 压力分布、总力、压力中心 + 内置IMU（加速度/角速度） | 捕获足‑地交互的精细动力学 |
| **语义标注** | 人工标注，三层时间对齐 | 临床运动评估叙述、原子动作描述、详细运动描述符 | 提供高层语义先验 |

Figure 2 展示了传感器在受试者身体上的佩戴布局。所有模态通过硬件同步触发，确保时间对齐精度。

![[assets/figures/papers/paper_list_l973_https_openaccess_thecvf_com_content_CVPR2026_html_Dabrowski_HUMAPS_4D_A/figures/003_Figure_2.jpg]]
*Figure 2: Overview of sensors placed during data acquisition*

### 数据规范化流水线

为消除个体差异（体型、肌肉强度、体重等），数据集提供三条规范化路径：

1. **3D关节位置归一化**：以骨盆为原点，利用受试者人体测量值构建缩放矩阵 $\mathbf{S}_{\mathrm{participant}}$，将关节坐标映射到统一空间：
   $${\bf p}_i^{\mathrm{norm}} = \mathbf{S}_{\mathrm{participant}} ({\bf p}_i - {\bf p}_{\mathrm{pelvis}}), \quad i=1,\ldots,N$$

2. **EMG 信号归一化**：将各肌肉通道的信号除以该受试者在参考收缩下的平均激活值：
   $$\mathbf{EMG}_{j,m}^{\mathrm{norm}}(t) = \frac{\mathbf{EMG}_{j,m}(t)}{\mathbf{EMG}_{j,m}^{\mathrm{ref}}}$$

3. **足底压力归一化**：提供两种方案——按单步最大压力缩放，或按受试者体重 $W_j$ 缩放：
   $$P_{j,s}^{\mathrm{norm}}(t) = \frac{P_{j,s}(t)}{\max_t P_{j,s}(t)} \quad \text{或} \quad P_{j,s}^{\mathrm{norm}}(t) = \frac{P_{j,s}(t)}{W_j}$$

### 下游基准任务映射

数据集定义了从原始信号到任务输出的标准映射关系，构成评估流水线：

- **动作识别**：从足底压力序列 $\mathbf{P}_{1:T}$ 映射到动作标签序列 $\{a_1,\dots,a_{30}\}^T$。采用3秒固定长度滑动窗口，将问题建模为监督分类任务。基线模型为 **ST-GCN**（Yan et al., AAAI 2018），支持单模态（仅鞋垫）与多模态融合（鞋垫+MoCap）两种输入配置。

- **3D姿态估计**：从足底压力 $\mathbf{P}_{1:T}$ 及辅助鞋垫数据 $\mathbf{A}_{1:T}$（加速度等）映射到全身3D关节位置序列 $\mathbf{J}_{1:T}$。基线架构参考 **SolePoser**（Wu et al., UIST 2024），采用双流Transformer设计。验证阶段**不输入任何姿态数据**，严格评估从足底动力学恢复全身运动的能力。

### 输入‑输出流总览

```
┌─────────────────────────────────────────────────┐
│  输入模态                                        │
│  ├─ 多视角RGB视频 (3×720p@120Hz)                 │
│  ├─ MoCap标记点 (42点@120Hz)                     │
│  ├─ sEMG (16通道@1259Hz) + IMU (148Hz)           │
│  ├─ 足底压力 (32传感器@100Hz) + IMU              │
│  └─ 语义标注 (三层时间对齐文本)                   │
└────────────────────┬────────────────────────────┘
                     │ 时间同步 + 规范化
                     ▼
┌─────────────────────────────────────────────────┐
│  标准化数据表示                                  │
│  ├─ 骨盆居中+人体测量缩放的3D关节                 │
│  ├─ 参考收缩归一化的EMG                          │
│  └─ 最大压力/体重归一化的足底压力                 │
└────────────────────┬────────────────────────────┘
                     │ 任务映射
                     ▼
┌─────────────────────────────────────────────────┐
│  基准任务                                        │
│  ├─ 动作识别: P_{1:T} → {a}ᵀ                    │
│  └─ 姿态估计: P_{1:T}, A_{1:T} → J_{1:T}        │
└─────────────────────────────────────────────────┘
```

该流水线的核心设计理念是：**足底压力与肌电等可穿戴信号携带丰富的生物力学约束**，结合语义描述可作为替代视觉的强先验，为隐私保护下的细粒度运动理解提供数据基础。当前流水线的固有限制在于所有采集均在受控室内环境完成，且受试者仅覆盖32名健康成年人（18‑42岁），向户外自由生活场景和特殊人群的泛化能力尚待验证。

### 补充图表

![[assets/figures/papers/paper_list_l973_https_openaccess_thecvf_com_content_CVPR2026_html_Dabrowski_HUMAPS_4D_A/figures/001_Figure_1.jpg]]
*Figure 1: HUMAPS-4D is a large-scale multimodal dataset for human motion analysis, comprising 14 hours of recordings and over 6 million time-synchronized images. Each session combines exocentric video, motion capture, IMUs, instrumented insoles, and sEMG, alongside rich semantic annotations and anthropometric data. By integrating low-level biomechanical signals with high-level semantic and visual information, HUMAPS-4D provides a comprehensive resource for studying full-body 3D motion, motor skill assessment, and cross-modal learning in naturalistic settings*

HUMAPS‑4D 的多模态信号在输入模型前需经过跨受试者归一化，以消除个体生理差异。以下三个公式构成了数据预处理的核心。

**3D 关节位置归一化** 以骨盆为原点，利用人体测量信息缩放：

$${ \bf p } _ { i } ^ { \mathrm { n o r m } } = { \bf S } _ { \mathrm { p a r t i c i p a n t } } \left( { \bf p } _ { i } - { \bf p } _ { \mathrm { p e l v i s } } \right) , \quad i = 1 , \ldots , N$$

其中 ${ \bf p } _ { i }$ 为第 $i$ 个关节的原始 3D 位置，${ \bf p } _ { \mathrm { p e l v i s } }$ 为骨盆中心坐标，${ \bf S } _ { \mathrm { p a r t i c i p a n t } }$ 为受试者特定的缩放矩阵，基于关键人体测量尺寸构建。此操作使关节坐标在跨受试者间可比。

**表面肌电 (sEMG) 归一化** 将信号除以该肌肉在参考收缩下的平均激活值：

$$\mathbf { E M G } _ { j , m } ^ { \mathrm { n o r m } } ( t ) = \frac { \mathbf { E M G } _ { j , m } ( t ) } { \mathbf { E M G } _ { j , m } ^ { \mathrm { r e f } } }$$

其中 $\mathbf { E M G } _ { j , m } ( t )$ 为受试者 $j$ 肌肉 $m$ 在时刻 $t$ 的原始肌电信号，分母 $\mathbf { E M G } _ { j , m } ^ { \mathrm { r e f } }$ 为该肌肉在参考收缩下的时间平均激活值。归一化后，信号幅值反映相对于最大自主收缩的激活比例，消除了电极位置、皮下脂肪厚度等个体差异。

**足底压力归一化** 提供两种可选方案：

$$P _ { j , s } ^ { \mathrm { n o r m } } ( t ) = \frac { P _ { j , s } ( t ) } { \operatorname* { m a x } _ { t } P _ { j , s } ( t ) } \quad \mathrm { o r } \quad P _ { j , s } ^ { \mathrm { n o r m } } ( t ) = \frac { P _ { j , s } ( t ) } { W _ { j } }$$

前者按单步内传感器 $s$ 的最大压力缩放，后者按受试者体重 $W_j$ 缩放。两种策略分别适用于步态周期内相对分布分析和跨受试者绝对负荷对比。

**基准任务的形式化定义** 明确了输入输出映射关系。动作识别任务将足底压力序列映射为动作标签序列：

$$f : \mathbf{P}_{1:T} \rightarrow \{a_1, \dots, a_{30}\}^T$$

其中 $\mathbf{P}_{1:T}$ 为长度 $T$ 的足底压力时间序列，输出为 30 类动作标签。姿态推断任务则从足底压力与辅助鞋垫数据（加速度等 $\mathbf{A}_{1:T}$）映射到 3D 关节位置序列：

$$f : \mathbf{P}_{1:T}, \mathbf{A}_{1:T} \rightarrow \mathbf{J}_{1:T}$$

为量化姿态预测的时域稳定性，引入不一致性指标 (Inconsistency Score)：

$$IS = \frac{1}{n_J} \sum_{i=0}^{n_J * 3 - 1} \sigma_{1:T}(\bar{J}_{i_{1:T}} - J_{i_{1:T}})$$

其中 $n_J$ 为关节数量，$\bar{J}_{i_{1:T}}$ 与 $J_{i_{1:T}}$ 分别为推断姿态和真值在第 $i$ 个坐标分量上的时间序列，$\sigma_{1:T}(\cdot)$ 为沿时间窗的标准差。该指标捕捉预测姿态相对于真值的时域抖动，值越低表示预测越平滑。

**基线模型架构** 方面，动作识别采用 **ST‑GCN** (Yan et al., AAAI 2018) 作为分类器，姿态估计基线参考 **SolePoser** (Wu et al., UIST 2024) 的双流 Transformer 设计，包含 PressNet 和 AccelNet 两个分支（完整架构见补充材料 Figure 4）。多模态监督采用联合损失，各模态损失等权加权。

### 补充图表

![[assets/figures/papers/paper_list_l973_https_openaccess_thecvf_com_content_CVPR2026_html_Dabrowski_HUMAPS_4D_A/figures/004_Figure_3.jpg]]
*Figure 3: HUMAPS-4D offers 3 paired language corpora*

## 实验与关键发现

HUMAPS‑4D 在论文中定义了两项核心基准任务——基于可穿戴信号的**动作识别**与**3D全身姿态估计**，并提供了初步基线结果。以下分析聚焦于这些结果揭示的能力边界、模态融合的因果效应以及当前方法的失败模式。

### 动作识别：模态融合的增益与单模态瓶颈

动作识别任务被形式化为有监督分类问题，采用固定长度3秒的滑动窗口，以足底压力（IPS）序列作为输入，映射到30类动作标签。评估采用严格的留一受试者（LOSO）协议，确保受试者间无数据泄露。

**Table 2** 给出了LOSO协议下各动作类别的识别准确率。核心发现是：多模态融合显著优于单模态基线，但单模态输入在动态和交互类动作上暴露出明显瓶颈。

- **融合模型（Insoles + MoCap）**：取得 **90.33% ± 4.3** 的总准确率，在所有模态组合中表现最优。这表明足底压力与运动学数据的联合特征能有效互补，尤其对静态姿态和简单周期性动作（如站立、行走）几乎达到完美识别。
- **纯足底压力模型（Insoles only）**：总准确率降至 **82.71% ± 3.9**。更关键的是，在动态动作（如跳跃、转身）上仅为 **74.36% ± 9.4**，而同期MoCap基线可达 **92.05% ± 7.9**。这种差距揭示了一个根本性局限：足底压力仅反映足‑地交互力，缺乏上肢和躯干的直接运动学信息。当动作涉及大幅度肢体挥动或快速方向变化时，压力信号的信息量不足以唯一确定动作类别。
- **失败模式分析**：交互类动作（如双人协作任务）的识别率同样偏低。原因在于压力鞋垫只能捕获个体自身的足底力学特征，无法感知人际间的力传递或空间关系。此外，不同受试者执行同一动作时的个体步态差异（如足弓高度、步幅习惯）进一步放大了单模态的类内方差。

### 3D姿态估计：从足底压力到全身关节的映射难度

姿态估计任务被定义为从足底压力序列 $\mathbf{P}_{1:T}$ 及辅助鞋垫数据（加速度等）$\mathbf{A}_{1:T}$ 到3D关节位置序列 $\mathbf{J}_{1:T}$ 的回归映射。模型验证阶段严格不输入任何姿态数据，以评估纯可穿戴信号恢复全身运动的能力。评估采用4折交叉验证，主要指标为MPJPE（平均每关节位置误差）。

**Table 3** 报告了各动作类别的姿态估计结果。总体MPJPE约为 **31.1 ± 0.8 cm**，这一数值需结合任务难度来解读：

- **静态与慢速动作表现尚可**：对于站立、慢走等足底压力模式与姿态高度耦合的动作，误差相对较低。这是因为此类动作中，足底压力中心（CoP）的移动与全身质心投影存在强力学关联，模型可以从压力分布推断出下肢关节链的大致构型。
- **动态与上肢主导动作误差急剧增大**：跳跃、投掷、举臂等动作的MPJPE远超平均值。根本原因在于**运动学冗余性**——同一足底压力模式可对应无限多种上肢姿态。例如，双脚站立时双手可置于身体两侧、交叉胸前或高举过头，而压力鞋垫无法区分这些构型。模型只能依赖训练数据中的统计先验（即“人们通常在此类动作中如何摆臂”）进行猜测，导致对罕见姿态的泛化能力极差。
- **不一致性指标（IS）揭示的时域抖动**：论文引入的不一致性指标 $IS = \frac{1}{n_J} \sum_{i=0}^{n_J * 3 - 1} \sigma_{1:T}(\bar{J}_{i_{1:T}} - J_{i_{1:T}})$ 量化了推断姿态与真值之差沿时间窗的标准差。动态动作的IS值显著更高，说明模型输出存在高频抖动——这源于压力信号的局部噪声被网络放大为关节位置的虚假振荡。

### 数据集对比：HUMAPS‑4D 的独特定位

**Table 1** 将 HUMAPS‑4D 与现有数据集进行了系统性对比。此前数据集分为两个孤立的阵营：

- **视觉驱动3D姿态估计数据集**（如 Human3.6M、3DPW）：强调多视角视频与MoCap的同步，但缺乏可穿戴生物力学信号。
- **生物力学运动评估数据集**（如 GaitRec、ENABL3S）：聚焦于步态、关节动力学、肌电和足底压力的精确测量，但通常缺少同步视觉数据和高层语义标注。

HUMAPS‑4D 的核心贡献在于**首次在一个统一采集协议下融合了上述所有模态**：42点MoCap、三视角RGB视频、16通道sEMG、双足足底压力（各16传感器）、IMU，以及三层时间对齐的语言语义标注（临床评估叙述、原子动作描述、详细运动描述符）。32名受试者×30种动作×超过570万帧的规模，使其成为目前唯一同时支持视觉‑可穿戴‑语义跨模态学习的大规模资源。

### 归一化策略对实验结果的影响

论文提供了三种关键归一化公式，对跨受试者比较至关重要：

- **3D关节位置归一化**：$\mathbf{p}_i^{\mathrm{norm}} = \mathbf{S}_{\mathrm{participant}} (\mathbf{p}_i - \mathbf{p}_{\mathrm{pelvis}})$，以骨盆为原点并按个体人体测量值缩放。这消除了身高、肢体比例差异对MPJPE的混淆效应，确保误差反映的是姿态估计精度而非受试者体型差异。
- **EMG信号归一化**：$\mathbf{EMG}_{j,m}^{\mathrm{norm}}(t) = \frac{\mathbf{EMG}_{j,m}(t)}{\mathbf{EMG}_{j,m}^{\mathrm{ref}}}$，除以参考收缩下的平均激活值。若不进行此归一化，皮下脂肪厚度、电极放置微小偏移等因素会导致不同受试者间相同肌肉的绝对信号幅值差异巨大，使跨受试者模型无法学习到有意义的肌肉协同模式。
- **足底压力归一化**：$P_{j,s}^{\mathrm{norm}}(t) = \frac{P_{j,s}(t)}{\max_t P_{j,s}(t)}$ 或 $P_{j,s}^{\mathrm{norm}}(t) = \frac{P_{j,s}(t)}{W_j}$，分别按单步最大压力或体重归一化。前者保留步态周期内的相对压力分布，后者消除体重对压力幅值的线性影响。两种策略的选择取决于下游任务是关注压力模式形态还是绝对载荷。

### 基线模型架构与训练策略

动作识别基线采用 **ST‑GCN**（Yan et al., AAAI 2018）作为分类器，多模态融合通过联合损失函数实现，各模态损失等权重加权。姿态估计基线模型架构受 **SolePoser**（Wu et al., UIST 2024）启发，采用双流Transformer设计（见 **Figure 4**），其中 AccelNet 和 PressNet 分别处理加速度和压力分支，最终回归42个3D关节位置。

需要指出的是，当前基线结果仅作为数据集发布时的参考下限。论文明确表示这些模型未针对各模态特性进行深度优化（如未利用sEMG的肌肉协同先验、未引入语义约束），因此实际可达到的性能上限可能远高于当前报告值。

### 补充图表

![[assets/figures/papers/paper_list_l973_https_openaccess_thecvf_com_content_CVPR2026_html_Dabrowski_HUMAPS_4D_A/figures/002_Table_1.jpg]]
*Table 1: Comparison of existing multimodal datasets for human motion analysis. The first group of datasets (top rows) corresponds to Vision-Driven 3D Pose Estimation, emphasizing video with MoCap and insole data. The second group (middle rows) corresponds to Biomechanical Motion Assessment, focusing on precise measurement of gait, joint kinematics, muscle activation, and anthropometrics using insoles, sEMG, and force plates. HUMAPS-4D (bottom row) integrates these modalities in a single dataset, providing synchronized recordings from instrumented insoles, IMUs, sEMG, motion capture, and multiple RGB cameras, along with rich semantic annotations and anthropometric data. With 32 participants performin...*

![[assets/figures/papers/paper_list_l973_https_openaccess_thecvf_com_content_CVPR2026_html_Dabrowski_HUMAPS_4D_A/figures/005_Table_2.jpg]]
*Table 2: Results per action category under the LOSO protocol. Per-class evaluation scores are provided in the Appendices*

![[assets/figures/papers/paper_list_l973_https_openaccess_thecvf_com_content_CVPR2026_html_Dabrowski_HUMAPS_4D_A/figures/006_Table_3.jpg]]
*Table 3: Results of 3D pose estimation based on plantar pressure for each action category*

## 定位与知识库关联

### 1. 本工作的定位与核心贡献

HUMAPS‑4D 本质上是一个**大规模多模态基准数据集**，而非一种新的算法模型。其核心贡献在于首次在统一的采集协议下，系统性地将视觉信号（多视角RGB视频）、可穿戴生物力学信号（足底压力、sEMG、IMU）与高层语义标注（三层语言描述）进行同步整合，弥合了计算机视觉与生物力学两大领域之间的数据鸿沟。

从知识库定位来看，该工作填补了现有数据资源的两个关键空白：
1.  **模态完整性缺口**：以往数据集要么聚焦于“视觉驱动的3D姿态估计”（以视频和MoCap为主），要么聚焦于“生物力学运动评估”（以足底压力、sEMG和测力台为主），但从未在同一批受试者上同时采集这两类数据。HUMAPS‑4D 通过32名受试者、30种动作、14小时记录和超600万帧同步图像，首次实现了这两大模态体系的系统配对。
2.  **语义-信号配对缺口**：该数据集提供了低层生理信号（如肌肉激活模式、足底压力分布）与高层运动描述符（临床运动评估叙述、原子动作描述、详细运动描述符）之间的独特配对，为隐私保护下的细粒度运动理解提供了新的学习范式。

### 2. 与现有数据集的关系

**Table 1**（见“实验与分析”部分）系统对比了HUMAPS‑4D与现有代表性数据集。从谱系上，可将相关工作分为两大阵营：

- **视觉驱动3D姿态估计数据集**：如Human3.6M、3DPW等，主要提供视频/MoCap配对，部分数据集（如SolePoser所用数据）虽引入了足底压力，但规模小、动作单一，且缺乏肌电和语义标注。
- **生物力学运动评估数据集**：如自建步态分析数据集，通常包含足底压力、sEMG和人体测量数据，但缺乏同步视觉信号和高层语义，且受试者数量和动作多样性有限。

HUMAPS‑4D 将上述两大阵营的模态整合到单一数据集中，在规模、传感器多样性和语义细节上均实现了对前人工作的超越。

### 3. 与基线方法的关系

论文为数据集配套定义了两个基准任务，并选择了代表性基线模型：

- **动作识别任务**：采用 **ST‑GCN**（Yan et al., AAAI 2018）作为分类器。该模型原本设计用于基于骨骼图的动作识别，在此被适配为处理足底压力序列和/或MoCap关节数据。实验表明，仅使用足底压力（Insole‑only）的准确率为82.71%±3.9，而融合足底压力与MoCap（Insole+MoCap fusion）可达90.33%±4.3。这说明足底压力携带了足够的生物力学约束以支持粗粒度动作分类，但视觉/运动学信息的补充能显著提升对动态和交互类动作的判别力。

- **3D姿态估计任务**：基线架构受 **SolePoser**（Wu et al., UIST 2024）启发，采用双流Transformer从足底压力和辅助鞋垫数据（加速度等）回归3D关节位置。该任务的核心挑战在于：从仅有的足底接触力信息推断全身43个关节的3D位置，这是一个高度欠约束的逆问题。基线模型在4折交叉验证下取得了总MPJPE约31.1 cm的结果，表明单模态输入的固有限制——尤其是对于上肢和头部等与足底压力耦合较弱的部位。

### 4. 适用边界与局限性

基于论文自身报告的限制和实验证据，HUMAPS‑4D的适用边界可归纳如下：

1.  **人群覆盖范围有限**：数据集仅包含32名18‑42岁的健康成年人。模型在此数据上训练后，向疾病人群（如帕金森、脑瘫）、老年人或儿童群体的迁移能力未经检验，且由于步态模式和肌肉激活特征存在显著群体差异，直接迁移可能导致性能大幅下降。
2.  **环境泛化能力未知**：所有采集均在受控室内环境完成。在户外自由生活场景下，光照变化、地面材质多样性、非结构化动作等因素对视觉和可穿戴信号的影响尚未被评估。
3.  **单模态姿态估计的精度瓶颈**：仅从足底压力推断全身3D姿态的误差仍较大（总MPJPE约31 cm），尤其是对于动态和交互类动作。论文明确指出，将语义或物理约束（如肌肉协同、动作描述）显式融入模型是降低误差的关键方向，但目前尚未实现。
4.  **数据集本身不提供新算法**：HUMAPS‑4D 是一个数据资源，其价值在于赋能后续的跨模态学习、隐私保护姿态估计和运动技能评估研究，而非提出一种即插即用的解决方案。

### 5. 开放问题与后续工作方向

论文遗留了若干关键开放问题，构成了该方向的后续研究空间：

1.  **语义/物理约束的显式融合**：如何将三层语言标注（临床叙述、原子动作、详细描述符）或生物力学先验（如肌肉协同模式）作为额外的监督信号或正则化项，融入姿态估计和动作识别模型，以显著降低推断误差？这涉及多模态对齐、知识蒸馏和物理引导学习等前沿方向。
2.  **跨模态融合策略的系统性研究**：不同任务（识别vs.估计）和不同动作类别可能受益于不同的融合策略（早融合、晚融合、对比学习、跨模态注意力等）。目前尚缺乏对“哪种模态组合对哪类动作最关键”的系统性消融分析。
3.  **社区标准化与开源生态**：论文未明确承诺基线代码和预训练模型的发布时间表。提供公开挑战赛和标准化评估协议（如LOSO和4折CV的固定划分）将是推动该数据集成为社区基准的关键步骤。
4.  **隐私保护运动分析的落地路径**：足底压力作为一种非视觉、隐私友好的模态，在家庭健康监测和远程康复中具有巨大潜力。但当前31 cm的MPJPE尚不足以支撑精确的运动学分析，如何将误差降低到临床可接受水平（通常<5 cm）是决定其实际应用价值的核心瓶颈。

**注意**：以上关于后续工作方向的推测基于论文自身提出的局限性和开放问题，部分细节（如代码开源时间）需以项目官网 [https://humaps4d.wp.imt.fr/](https://humaps4d.wp.imt.fr/) 的后续更新为准。

## 原文 PDF

![[paperPDFs/CVPR_2026/HUMAPS_4D_A_Multimodal_Dataset_for_HUman_Motion_Analysis_with_Physiological_and_Semantic_informations.pdf]]
