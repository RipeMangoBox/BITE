---
title: "ReGenHOI: Unifying Reconstruction and Generation for 3D Human-Object Interaction Understanding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ReGenHOI_Unifying_Reconstruction_and_Generation_for_3D_Human_Object_Interaction_Understanding.pdf
project_link: null
code_link: "https://github.com/xumiao66/ReGenHOI"
aliases:
- ReGenHOI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 通过共享的语义-几何潜在空间（shared semantic–geometric latent space）与3D接触推理（3D Contact Reasoning）形成因果调控节点：接触推理作为关键中间表示，统一支配重建准确性与生成合理性。
primary_logic: 重建与生成可以且应当在统一的接触推理空间中相互增强——生成提供语义与物理合理性先验，重建提供几何真实观测基础，二者协同提升整体交互理解性能。
claims:
- 在DAMON人体接触预测上，F1达到78.4，比现有最佳方法DECO/InteractVLM提升2.8 F1分，且测地误差更低。
- 在PICO数据集重建任务中，PA Chamfer Distance降至5.42，超越Pico等方法。
- 运动生成任务中，我们的方法在FullBodyManipulation和BEHAVE上多项指标（HandJPE、MPJPE、FID）领先SemGeoMo。
- DAMON (Human Contact) 上 F1 = 78.4
---

# ReGenHOI: Unifying Reconstruction and Generation for 3D Human-Object Interaction Understanding

> [!tip] 核心洞察
> 重建与生成可以且应当在统一的接触推理空间中相互增强——生成提供语义与物理合理性先验，重建提供几何真实观测基础，二者协同提升整体交互理解性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReGenHOI：面向三维人-物交互理解的统一重建与生成框架 |
| 英文题名 | ReGenHOI: Unifying Reconstruction and Generation for 3D Human-Object Interaction Understanding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_ReGenHOI_Unifying_Reconstruction_and_Generation_for_3D_Human-Object_Interaction_Understanding_CVPR_2026_paper.html) · [Code](https://github.com/xumiao66/ReGenHOI) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | ReGenHOI |
| Dataset | DAMON, PICO, FullBodyManipulation, BEHAVE |

> [!tip] 效果简介
> - DAMON (Human Contact) 上，F1 78.4 vs InteractVLM / DECO (约75.6) (+2.8)。
> - PICO (Reconstruction) 上，PA Chamfer Distance (PA-CDh) 5.42 vs Pico (Cseke et al., CVPR 2025) (outperforms)。
> - FullBodyManipulation (Generation) 上，HandJPE 26.91 vs SemGeoMo (outperforms)。

## 概述

**问题瓶颈**：现有三维人体-物体交互（HOI）理解将重建与生成视为独立任务，未共享空间推理与接触建模能力，导致重建缺乏语义普适性、生成缺乏几何一致性。

**核心洞察**：重建与生成可以在统一的接触推理空间中相互增强——生成提供语义与物理合理性先验，重建提供几何真实观测基础，二者协同提升整体交互理解性能。

**方法定位**：ReGenHOI 构建了一个共享语义-几何潜在空间的统一编码器-解码器框架，以 **3D 接触推理（3D Contact Reasoning）** 和 **推理轨迹细化（Reasoning Trace Refinement）** 作为因果调控节点，统一支配重建准确性与生成合理性。在此基础上，引入基于重力场扩散桥（Gravity-Field Based Diffusion Bridge）的接触细化，消除穿透并保证物理一致性。

**主要结果**：
- 在 DAMON 人体接触预测上，F1 达到 78.4，比现有最佳方法 DECO（Tripathi et al., ICCV 2023）/ InteractVLM（Dwivedi et al., CVPR 2025）提升 2.8 分，且测地误差更低。
- 在 PICO 数据集重建任务中，PA Chamfer Distance 降至 5.42，超越 Pico（Cseke et al., CVPR 2025）。
- 运动生成任务中，在 FullBodyManipulation 和 BEHAVE 上多项指标（HandJPE、MPJPE、FID）领先 SemGeoMo（Cong et al., CVPR 2025）。

**方法谱系与知识库定位**：ReGenHOI 区别于传统 2D 投影再提升的接触推理路线（如 DECO），直接在 3D 空间进行接触推理；不同于分离训练的重建/生成框架，以共享潜在空间实现跨任务知识迁移。消融实验表明，移除扩散桥细化或推理轨迹机制均导致显著性能下降，验证了统一接触推理空间作为因果调控节点的关键作用。

**局限与开放问题**：当前方法依赖数据集特定的物体池进行检索，当目标物体不在池中时需选择相似物体，可能影响重建精度。如何将框架扩展至开放词汇物体类别或任意真实场景下的交互理解，是后续研究的重要方向。

## 背景与动机

### 问题背景：三维人-物交互理解的双重需求

理解人类与物体在三维空间中的交互（Human-Object Interaction, HOI）是计算机视觉与具身智能的核心挑战之一。一个完整的HOI理解系统需要同时具备两种能力：**重建（Reconstruction）**——从单张RGB图像中恢复人体姿态、物体位姿及二者之间的空间关系；**生成（Generation）**——基于当前状态预测未来的人体运动序列，使交互过程在物理和语义层面均保持合理。这两项任务并非孤立存在：重建为生成提供几何真实的状态锚点，生成则为重建注入关于交互意图与物理合理性的语义先验。

### 现有方法的缺口：重建与生成的割裂

当前的三维HOI理解研究在方法论上呈现明显的**任务割裂**。重建方向的方法（如基于接触优化或参数化模型拟合的方法）专注于从图像中精确恢复几何配置，但缺乏对交互语义的深层理解，难以泛化至未见过的交互类别。生成方向的方法（如**SemGeoMo**（Cong et al., CVPR 2025）、**OMG**（Li et al., TOG 2023）等运动生成模型）能够合成流畅的人体运动序列，却往往忽略与物体几何的精确一致性，导致穿透或悬空等物理不合理现象。

这种割裂的根源在于：现有方法**未能将空间推理与接触建模能力在重建与生成之间共享**。具体而言，重建系统缺乏语义普适性——它们能拟合看到的交互，却不理解交互的本质；生成系统缺乏几何一致性——它们能生成语义合理的运动，却无法保证人体与物体的精确接触。

### 接触推理：统一理解的关键瓶颈

人体与物体的**接触区域（Contact Regions）**是连接几何与语义的天然桥梁。接触既定义了空间上的物理约束（人体何处触碰物体），也编码了语义上的交互意图（触碰方式反映了交互类型）。然而，现有方法对接触的建模存在两个根本性局限：

1. **二维投影再提升（2D Projection and Subsequent Lifting）**：如**DECO**（Tripathi et al., ICCV 2023）和**InteractVLM**（Dwivedi et al., CVPR 2025）等方法，先在2D图像空间预测接触，再通过投影提升至3D。这一流程不可避免地引入投影误差，且无法充分利用3D空间的几何结构信息。
2. **缺乏结构化推理轨迹**：现有方法缺乏从粗到细、从几何到语义的显式推理过程，导致接触预测的准确性和鲁棒性不足。

### 本文动机：统一框架下的协同增强

本文的核心洞察是：**重建与生成可以且应当在统一的接触推理空间中相互增强**。生成提供语义与物理合理性先验，重建提供几何真实观测基础，二者协同可同时提升接触预测、重建精度与运动生成质量。

基于此，我们提出**ReGenHOI**——一个将三维HOI重建与生成统一于共享语义-几何潜在空间的框架。该框架的核心在于通过**3D接触推理（3D Contact Reasoning）**与**结构化推理轨迹机制（Reasoning Trace Mechanism）**，直接在三维空间中对人体-物体接触进行建模，并将其作为支配重建与生成的因果中间表示。这一设计使得接触推理成为调控重建准确性与生成合理性的关键“旋钮”，从根本上弥合了重建与生成之间的方法论鸿沟。

## 核心创新

ReGenHOI 的核心创新在于**将三维人体-物体交互（HOI）的重建与生成统一到共享的语义-几何潜在空间**中，使二者通过接触推理相互增强，而非像现有方法那样将两者视为独立任务。这一统一框架围绕以下四个关键机制展开：

### 1. 共享潜在空间的统一编码器-解码器框架

现有方法（如 **DECO**（Tripathi et al., ICCV 2023）用于接触预测、**SemGeoMo**（Cong et al., CVPR 2025）用于运动生成）将重建与生成分离训练，缺乏跨任务的空间推理共享。ReGenHOI 将两类任务纳入同一编码器-解码器架构，学习一个语义对齐且几何一致的潜在表示：

$$z = \mathrm{Encoder}(\mathcal{X}; \theta_{\mathrm{enc}}), \quad \hat{y} = \mathrm{Decoder}(z \mid \theta_{\mathrm{dec}})$$

多模态输入 $\mathcal{X}$ 经编码后形成统一潜在嵌入 $z$，再分别解码为重建的三维配置或生成的运动序列。消融实验证实，联合学习共享潜在空间同时提升重建与生成性能，分离任务则导致准确性和一致性明显下降。

### 2. 3D 接触推理（3D Contact Reasoning）

基线方法依赖 2D 投影再提升（2D projection and subsequent lifting）进行接触推理，在维度压缩过程中损失空间精度。ReGenHOI 的 **3D Contact Reasoning** 直接在三维空间推理接触概率场，将接触推理作为连接重建与生成的核心中间表示。这一设计使模型能够在统一的几何空间中同时服务于静态重建的精确接触定位和动态生成的物理合理性约束。

### 3. 推理轨迹细化（Reasoning Trace Refinement）

现有方法缺乏显式的迭代优化机制。ReGenHOI 引入结构化推理轨迹，利用边界框推理空间关系，通过几何阶段（$\Phi_{\mathrm{geo}}$）、语义阶段（$\Phi_{\mathrm{sem}}$）和接触阶段（$\Phi_{\mathrm{cont}}$）的潜在一致性约束，迭代细化接触区域预测：

$$\mathcal{L}_{\mathrm{reason}} = \| \Phi_{\mathrm{geo}} - \Phi_{\mathrm{sem}} \|_2^2 + \| \Phi_{\mathrm{sem}} - \Phi_{\mathrm{cont}} \|_2^2$$

消融实验表明，移除推理轨迹机制（RTM）会导致所有指标显著下降，进而降低重建精度，验证了结构化推理路径对接触预测质量的关键作用。

### 4. 基于重力场扩散桥的接触细化

现有方法在接触细化环节缺乏物理引导。ReGenHOI 改进并适配 **Gravity-Field Based Diffusion Bridge (GBDB)**，将接触细化建模为随机微分方程（SDE），通过势场、SMPL-X 形状先验和法向一致性引导人体点云向物体表面演化，消除穿透并确保物理一致性。消融实验显示，移除 GBDB 导致手部重建的 MPJPE 和 MPVPE 增加，交互体积（IV）和穿透距离（PD）变大，证实了扩散桥在精细接触几何引导中的不可替代性。

### 创新因果链

上述四个创新形成清晰的因果链：**共享潜在空间**提供跨任务表示基础 → **3D 接触推理**在统一空间中生成核心中间表示 → **推理轨迹机制**迭代优化接触质量 → **扩散桥细化**消除穿透、确保物理一致性。这条因果链使重建获得语义普适性、生成获得几何一致性，最终在 DAMON 接触预测（F1 78.4，超越 DECO/InteractVLM 2.8 分）、PICO 重建（PA-CDh 5.42）和 FullBodyManipulation/BEHAVE 运动生成（HandJPE、MPJPE、FID 全面领先 SemGeoMo）等多项基准上取得最优结果。

## 整体框架

ReGenHOI 的核心设计理念是将三维人-物交互（HOI）的重建与生成统一在**共享的语义-几何潜在空间**中，使两个任务共享空间推理与接触建模能力。整个框架由一条**统一编码器-解码器**主线串联，并在关键节点引入**3D 接触推理**与**扩散桥细化**，形成从图像到三维配置（重建）或运动序列（生成）的端到端通路。

### 统一潜在空间编码

框架的入口是**统一潜在空间编码器（Unified Latent Space Encoder）**。给定单张 RGB 图像，编码器并行提取三类特征：图像全局特征 $f_I$、人体特征 $f_H$ 和物体特征 $f_O$。人体姿态 $\theta$ 与体型 $\beta$ 通过 SMPL-X 回归器从 $f_I$ 中回归得到：

$$\theta, \beta = \mathcal{R}_{\mathrm{human}}(f_I)$$

这三类特征随后被融合为统一的潜在表示。对于重建任务，潜在编码由加权组合构成：

$$z_{\mathrm{rec}} = W_H f_H + W_O f_O + W_I f_I$$

对于生成任务，潜在编码 $z_{\mathrm{gen}}$ 则在此基础上进一步融入时序上下文信息。整个编码过程遵循统一的抽象形式：

$$z = \mathrm{Encoder}(\mathcal{X}; \theta_{\mathrm{enc}}), \quad \hat{y} = \mathrm{Decoder}(z \mid \theta_{\mathrm{dec}})$$

其中 $\mathcal{X}$ 为多模态输入，$z$ 为共享潜在嵌入，$\hat{y}$ 为重建的三维配置或生成的运动序列。这一设计使得语义对齐与几何一致性在潜在空间层面得到保证，而非在任务层面各自为政。

### 3D 接触推理与推理轨迹机制

潜在空间的核心调控节点是 **3D 接触推理（3D Contact Reasoning）**。与现有方法依赖 2D 投影再提升（2D projection and subsequent lifting）不同，ReGenHOI 直接在三维空间推理人体-物体的接触概率场。这一转变消除了投影带来的几何信息损失，使接触推理成为同时支配重建精度与生成合理性的关键中间表示。

为增强接触推理的结构化程度，框架引入了**推理轨迹机制（Reasoning Trace Mechanism, RTM）**。RTM 以物体边界框为空间锚点，引导模型沿着“几何阶段 → 语义阶段 → 接触阶段”的推理路径迭代细化接触区域。推理路径的一致性由正则损失显式约束：

$$\mathcal{L}_{\mathrm{reason}} = \| \Phi_{\mathrm{geo}} - \Phi_{\mathrm{sem}} \|_2^2 + \| \Phi_{\mathrm{sem}} - \Phi_{\mathrm{cont}} \|_2^2$$

该损失强制几何、语义与接触三个阶段的潜在表示保持对齐，防止推理过程中的语义漂移。

### 双解码器：重建与生成

从共享潜在空间出发，框架分叉为两条解码路径：

- **重建解码器（Reconstruction Decoder）**：以 $z_{\mathrm{rec}}$ 为条件，LLM 预测稠密接触概率场，进而恢复完整的人-物三维配置，包括人体网格、物体位姿与接触区域。
- **生成解码器（Generation Decoder）**：以 $z_{\mathrm{gen}}$ 为条件，运动-语言 LLM 自回归预测未来运动 token，再通过 vQ-VAE 解码器还原为连续运动序列 $\hat{m}_{1:M}$。

两个解码器共享同一潜在空间，使得重建提供的几何观测基础与生成提供的语义-物理先验能够相互增强。

### 扩散桥接触细化

粗粒度重建结果在接触几何层面仍可能存在穿透或分离。为此，ReGenHOI 在重建与生成输出之上附加了**基于重力场扩散桥（Gravity-Field Based Diffusion Bridge, GBDB）的接触细化模块**。该模块将细化过程建模为随机微分方程（SDE）：

$$d \mathcal{H}_t = -\alpha \nabla \varphi(\mathcal{H}_t) dt - \lambda_1 \nabla \mathcal{L}_{\mathrm{SMPL-X}} dt - \lambda_2 \nabla \mathcal{L}_{\mathrm{normal}} dt + g(\mathcal{H}_t) dW_t$$

其中 $\varphi$ 为势场函数，驱动人体点云 $\mathcal{H}_t$ 向物体表面演化；$\mathcal{L}_{\mathrm{SMPL-X}}$ 保持人体形状先验；$\mathcal{L}_{\mathrm{normal}}$ 约束接触面法向一致性；扩散项 $g(\mathcal{H}_t) dW_t$ 提供随机探索以跳出局部穿透构型。消融实验表明，移除 GBDB 会导致手部重建的 MPJPE 和 MPVPE 增加，交互体积（IV）与穿透距离（PD）显著变大，验证了扩散桥在引导接触细化中的关键作用。

### 训练策略

LLM 主体采用 AdamW 优化器训练 30 个 epoch，初始学习率 $1 \times 10^{-4}$，批次大小 16，联合优化接触二值交叉熵、语义对比对齐与推理路径正则三项损失：

$$\mathcal{L}_{\mathrm{LLM}} = \lambda_c \mathcal{L}_{\mathrm{contact}} + \lambda_s \mathcal{L}_{\mathrm{semantic}} + \lambda_r \mathcal{L}_{\mathrm{reason}}$$

扩散桥细化模块则单独训练 50k 次迭代，使用相同优化器并配合余弦退火调度。这种分阶段训练策略保证了 LLM 先学到稳定的接触推理能力，再由扩散桥进行精细几何修正。

### 输入输出流总结

整体 pipeline 的信息流可概括为：**单张 RGB 图像 → 统一潜在空间编码 → 3D 接触推理（含 RTM 迭代细化）→ 分支解码（重建三维配置 / 自回归生成运动序列）→ 扩散桥接触细化 → 最终输出**。这一设计使接触推理成为贯穿重建与生成的因果调控节点，实现了“重建提供几何真实观测基础、生成提供语义与物理合理性先验”的协同效应。

### 补充图表

![[assets/figures/papers/paper_list_l971_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_ReGenHOI_Unifying_R/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our unified framework for reconstruction and generation. It consists of Unified Latent Space Encoding, Reconstruction module and Generation module. For clarity, the arrows representing the reconstruction and generation processes are distinguished using black and yellow colors, respectively*

![[assets/figures/papers/paper_list_l971_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_ReGenHOI_Unifying_R/figures/001_Figure_1.jpg]]
*Figure 1: The understanding of human–object interaction should encompass both reconstruction and generation. (a) demonstrates the ability of our method to reconstruct interaction states from images, while (b) illustrates its capability to generate interaction sequences*

## 核心模块与公式推导

ReGenHOI 的核心在于通过**统一的语义-几何潜在空间**与**3D 接触推理**，将重建与生成任务耦合为一个共享框架。以下按流水线模块依次展开关键公式与变量含义。

### 3.1 统一潜在空间编码

多模态输入 $\mathcal{X}$（图像、人体、物体特征）首先通过编码器映射到统一潜在表示 $z$：

$$z = \mathrm{Encoder}(\mathcal{X}; \theta_{\mathrm{enc}}), \quad \hat{y} = \mathrm{Decoder}(z \mid \theta_{\mathrm{dec}})$$

其中 $\hat{y}$ 为解码输出（重建的三维配置或生成的运动序列）。这是整个框架的数学基础，保证两个任务共享同一表征空间。

人体姿态 $\theta$ 与体型 $\beta$ 通过 SMPL‑X 回归器从图像特征 $f_I$ 提取：

$$\theta, \beta = \mathcal{R}_{\mathrm{human}}(f_I)$$

重建分支的潜在编码 $z_{\mathrm{rec}}$ 由人体特征 $f_H$、物体特征 $f_O$ 和图像特征 $f_I$ 融合得到：

$$z_{\mathrm{rec}} = W_H f_H + W_O f_O + W_I f_I$$

### 3.2 3D 接触推理与推理轨迹机制

接触推理在三维空间直接进行，输出稠密接触概率场，避免传统方法中“2D 投影再提升”带来的几何不一致。推理过程由**推理轨迹机制**（Reasoning Trace Mechanism, RTM）驱动，通过边界框引导的空间关系推理，迭代细化接触区域。轨迹在几何、语义、接触三个阶段之间传递，其一致性由推理路径正则损失约束。

### 3.3 扩散桥接触细化

粗粒度接触结果通过**基于重力场的扩散桥**（Gravity‑Field Based Diffusion Bridge, GBDB）进行精细化，消除穿透并保证物理一致性。该过程建模为随机微分方程（SDE）：

$$d \mathcal{H}_t = -\alpha \nabla \varphi(\mathcal{H}_t) dt - \lambda_1 \nabla \mathcal{L}_{\mathrm{SMPL-X}} dt - \lambda_2 \nabla \mathcal{L}_{\mathrm{normal}} dt + g(\mathcal{H}_t) dW_t$$

- $\mathcal{H}_t$：演化中的人体点云。
- $\varphi(\mathcal{H}_t)$：势场项，引导点云向物体表面靠近。
- $\mathcal{L}_{\mathrm{SMPL-X}}$：SMPL‑X 形状先验损失，约束人体形态合理性。
- $\mathcal{L}_{\mathrm{normal}}$：法向一致性损失，保证接触面方向匹配。
- $g(\mathcal{H}_t) dW_t$：扩散项，提供随机探索能力。

### 3.4 训练损失

LLM 训练采用联合损失：

$$\mathcal{L}_{\mathrm{LLM}} = \lambda_c \mathcal{L}_{\mathrm{contact}} + \lambda_s \mathcal{L}_{\mathrm{semantic}} + \lambda_r \mathcal{L}_{\mathrm{reason}}$$

- $\mathcal{L}_{\mathrm{contact}}$：接触二值交叉熵损失。
- $\mathcal{L}_{\mathrm{semantic}}$：语义对比对齐损失。
- $\mathcal{L}_{\mathrm{reason}}$：推理路径正则损失，定义如下：

$$\mathcal{L}_{\mathrm{reason}} = \| \Phi_{\mathrm{geo}} - \Phi_{\mathrm{sem}} \|_2^2 + \| \Phi_{\mathrm{sem}} - \Phi_{\mathrm{cont}} \|_2^2$$

其中 $\Phi_{\mathrm{geo}}$、$\Phi_{\mathrm{sem}}$、$\Phi_{\mathrm{cont}}$ 分别为几何、语义、接触阶段的潜在表示，该损失强制三阶段在潜在空间中保持一致性。

扩散桥细化阶段额外引入桥接损失 $\mathcal{L}_{\mathrm{bridge}}$，其具体形式为：

$$\mathcal{L}_{\mathrm{bridge}} = \lambda_p \| \mathcal{H}_T - \mathcal{H}^* \|_2^2 + \lambda_m \mathcal{L}_{\mathrm{SMPL-X}} + \lambda_n \mathcal{L}_{\mathrm{normal}}$$

- $\mathcal{H}_T$：扩散终态人体点云。
- $\mathcal{H}^*$：真值人体点云。
- 三项分别对应几何对齐、形状先验约束与法向一致性，与 SDE 中的漂移项形成互补。

### 模块耦合关系

上述模块形成闭环：统一编码器输出共享潜在表示 $z$，3D 接触推理与 RTM 在潜在空间中生成接触概率场，该场同时馈入重建解码器和生成解码器；GBDB 对重建结果进行后细化，其 SDE 漂移项中的形状先验与法向约束直接继承自接触推理阶段的几何输出。训练时 $\mathcal{L}_{\mathrm{reason}}$ 保证推理轨迹的跨阶段一致性，$\mathcal{L}_{\mathrm{bridge}}$ 保证细化结果的几何精度，二者共同维护共享潜在空间的语义-几何对齐。

## 实验与分析

### 主要结果

#### 人体接触预测

在DAMON数据集上，ReGenHOI在人体接触预测任务中取得了**F1 78.4**的成绩，相比此前最优方法**DECO**（Tripathi et al., ICCV 2023）和**InteractVLM**（Dwivedi et al., CVPR 2025）提升**2.8 F1分**，同时测地误差更低（Table 1）。在语义人体接触预测的逐类别评估中，该方法在运动器材等类别上同样保持领先（Table 2）。这一结果直接验证了**3D接触推理**（3D Contact Reasoning）的有效性——直接在三维空间推理接触概率场，避免了传统方法依赖2D投影再提升所带来的信息损失。

![[assets/figures/papers/paper_list_l971_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_ReGenHOI_Unifying_R/figures/005_Table_1.jpg]]
*Table 1: Evaluation for Human Contact prediction on the DAMON [38]. We compare our method with state-of-the-art approaches*

![[assets/figures/papers/paper_list_l971_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_ReGenHOI_Unifying_R/figures/004_Table_2.jpg]]
*Table 2: Evaluation for Semantic Human Contact prediction on the DAMON [38]*

#### 三维重建

在PICO数据集上，ReGenHOI的**PA Chamfer Distance（PA-CDh）降至5.42**，优于**Pico**（Cseke et al., CVPR 2025）等现有方法（Table 3）。定性对比显示，该方法生成的重建结果穿透和分离现象明显更少（Figure 3）。这一优势源于**扩散桥细化**（Diffusion Bridge Refinement）模块通过随机微分方程引导人体点云向物体表面演化，在保持物理合理性的同时消除穿透。

![[assets/figures/papers/paper_list_l971_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_ReGenHOI_Unifying_R/figures/006_Table_3.jpg]]
*Table 3: Comparisons with state-of-the-art reconstruction method and ablation studies on the PICO dataset*

![[assets/figures/papers/paper_list_l971_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_ReGenHOI_Unifying_R/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparison experiment with human interaction reconstruction methods. Our method produces more accurate results with minimal interpenetration or separation*

#### 运动生成

在FullBodyManipulation和BEHAVE两个数据集上，ReGenHOI在多项指标上全面超越**SemGeoMo**（Cong et al., CVPR 2025）：

- **FullBodyManipulation**：HandJPE 26.91，MPJPE 16.28，FID 1.02（Table 4）
- **BEHAVE**：HandJPE 27.35，MPJPE 16.00，FID 1.38（Table 5）

![[assets/figures/papers/paper_list_l971_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_ReGenHOI_Unifying_R/figures/008_Table_4.jpg]]
*Table 4: HOI motion generation results on the FullBodyManipulation dataset [31]*

![[assets/figures/papers/paper_list_l971_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_ReGenHOI_Unifying_R/figures/009_Table_5.jpg]]
*Table 5: HOI motion generation results on the BEHAVE dataset [3]*

定性结果（Figure 4）表明，该方法生成的接触区域更加真实，这得益于生成解码器与重建解码器共享同一语义-几何潜在空间，使得生成过程能够继承来自重建分支的几何一致性约束。

![[assets/figures/papers/paper_list_l971_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_ReGenHOI_Unifying_R/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison experiment with human interaction generation methods. The contact regions generated by our method are more realistic*

### 消融实验

Table 3中的消融实验揭示了三个关键模块的因果效应：

1. **移除扩散桥细化（GBDB）**：手部重建的MPJPE和MPVPE显著增加，交互体积（IV）和穿透距离（PD）变大。这证明GBDB在引导细粒度接触几何优化中不可替代——仅靠粗粒度重建无法保证物理一致性。

2. **移除推理轨迹机制（RTM）**：所有指标出现显著下降，进而导致Table 3中的重建精度降低。RTM通过边界框锚定的结构化推理路径（几何→语义→接触），为接触推理提供了必要的空间关系先验。

3. **分离重建与生成任务**：联合学习共享潜在空间同时提升了重建和生成性能，任务分离则导致准确性和一致性明显下降。这验证了核心假设——重建与生成在统一接触推理空间中相互增强。

### 局限性

该方法依赖数据集特定的物体池进行物体检索。当目标物体不在预定义池中时，需选择相似物体替代，可能影响重建精度。此外，接触标签通过弱监督DECO生成，标注质量可能对接触精度构成上限约束。

## 方法谱系与知识库定位

### 任务耦合范式：从分离到统一

现有三维人-物交互（HOI）理解研究长期沿着两条独立路径演进：**重建路径**致力于从单目或RGB-D输入恢复静态交互几何，而**生成路径**聚焦于合成未来交互运动序列。这两个方向在方法设计、表征空间与优化目标上彼此隔离，导致重建方法缺乏语义普适性、生成方法缺乏几何一致性。

ReGenHOI 的核心突破在于将重建与生成形式化为**同一编码器-解码器框架下的两个解码分支**，共享一个语义对齐且几何一致的潜在空间。这一设计使得接触推理成为贯通静态几何重建与动态运动合成的关键中间表示——重建分支利用接触概率场约束人体与物体的空间配置，生成分支则以接触推理结果为条件自回归地预测运动令牌。这种“接触推理作为共享瓶颈”的设计与现有分离式方法形成根本差异。

### 接触推理：从2D提升到原生3D

接触推理是HOI理解的核心子问题。此前的方法多采用“2D投影再提升”策略：先在渲染视图上进行2D接触分割，再通过几何投影将结果提升至3D空间。代表性工作包括：

- **DECO** (Tripathi et al., ICCV 2023)：通过弱监督方式在2D渲染视图上预测接触区域，再映射回3D人体网格。
- **InteractVLM** (Dwivedi et al., CVPR 2025)：利用大视觉语言模型在2D图像层面进行语义接触推理，同样依赖投影提升。

ReGenHOI 的**3D接触推理（3D Contact Reasoning）** 模块直接在三维护体空间中推理接触概率场，规避了2D投影带来的信息损失与几何不一致问题。这一设计选择在DAMON数据集上产生了2.8 F1分的提升（78.4 vs. 约75.6），且测地误差更低，验证了原生3D推理相对于2D提升路径的优越性。

### 推理轨迹机制：结构化的迭代优化

传统接触推理方法通常采用单步预测，缺乏对推理过程本身的显式建模。ReGenHOI 引入**推理轨迹机制（Reasoning Trace Mechanism）**，以边界框为锚点，引导模型沿“几何阶段→语义阶段→接触阶段”的结构化路径逐步细化接触区域。对应的推理路径正则损失 $\mathcal{L}_{\mathrm{reason}} = \| \Phi_{\mathrm{geo}} - \Phi_{\mathrm{sem}} \|_2^2 + \| \Phi_{\mathrm{sem}} - \Phi_{\mathrm{cont}} \|_2^2$ 约束了各阶段潜在表示的一致性。消融实验表明，移除该机制会导致所有指标显著下降，进而降低重建精度。

### 运动生成：与语义-几何先验方法的对比

在运动生成任务上，ReGenHOI 与以下方法形成直接对比：

- **SemGeoMo** (Cong et al., CVPR 2025)：利用语义与几何先验引导运动生成，是当前领先的HOI运动生成方法。
- **Object Motion Guided (OMG)** (Li et al., TOG 2023)：以物体运动为条件引导人体运动合成。

ReGenHOI 在FullBodyManipulation和BEHAVE两个数据集上，多项指标（HandJPE、MPJPE、FID）均超越SemGeoMo。其优势源于共享潜在空间使生成分支能够直接受益于接触推理模块提供的精确空间关系信息，而非仅依赖抽象的语义或几何先验。

### 扩散桥细化：物理一致性保证

粗粒度重建结果往往存在穿透与接触不自然的问题。ReGenHOI 采用基于重力场的扩散桥（Gravity-Field Based Diffusion Bridge, GBDB）进行接触细化，将其形式化为随机微分方程：

$$d \mathcal{H}_t = -\alpha \nabla \varphi(\mathcal{H}_t) dt - \lambda_1 \nabla \mathcal{L}_{\mathrm{SMPL-X}} dt - \lambda_2 \nabla \mathcal{L}_{\mathrm{normal}} dt + g(\mathcal{H}_t) dW_t$$

该SDE通过势场梯度、SMPL-X形状先验、法向一致性约束与扩散项共同引导人体点云向物体表面平滑演化。消融实验证实，移除GBDB会导致手部重建的MPJPE和MPVPE增加，交互体积（IV）和穿透距离（PD）变大。

### 适用边界与局限

1. **物体池依赖**：该方法依赖数据集特定的物体池进行物体检索。当目标物体不在预定义池中时，需选择相似物体替代，可能影响重建精度。这限制了其向开放场景的直接泛化。

2. **接触标签质量**：训练使用DECO的弱监督接触标签，通过几何投影生成对应关系。标注质量可能影响接触推理精度的上限。

3. **开放词汇扩展**：当前框架假设物体类别在训练集中可见，尚未验证向开放词汇物体类别或任意真实场景下交互理解的扩展能力。这是该方向的重要开放问题。

### 知识库定位总结

ReGenHOI 在HOI理解的知识谱系中占据了“统一重建-生成”的关键节点。其方法论贡献——原生3D接触推理、结构化推理轨迹、共享潜在空间——为后续研究提供了可复用的技术组件。未来工作可沿两个方向推进：一是突破物体池限制，实现开放场景下的物体检索与交互理解；二是将接触推理机制扩展至多人与多物体交互场景。

## 原文 PDF

![[paperPDFs/CVPR_2026/ReGenHOI_Unifying_Reconstruction_and_Generation_for_3D_Human_Object_Interaction_Understanding.pdf]]