---
title: "FantasyWorld: Geometry-Consistent World Modeling via Unified Video and 3D Prediction"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/FantasyWorld_Geometry_Consistent_World_Modeling_via_Unified_Video_and_3D_Prediction.pdf
openreview_forum_id: 3q9vHEqsNx
aliases:
- FantasyWorld
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "在冻结的视频基础模型（Wan2.1）内部嵌入可训练的几何分支，通过预备条件模块（PCB）和集成重建生成模块（IRG）实现视频潜变量与隐式3D场的联合前向推理，并利用双向交叉注意力机制让几何线索约束视频生成、视频先验反哺几何预测，从而将想象与感知统一在单个骨干中。"
primary_logic: "复用冻结视频扩散模型并从中提取去噪后期语义丰富、结构可靠的特征，结合“反向”DPT解码策略（从深到浅上采样），能够在不损害视频创造力的情况下，高效端到端地产生几何一致且可泛化的3D感知表示，充当世界模型的核心桥梁。"
claims:
- "移除几何分支（Ours w/o 3D）导致WorldScore三维一致性在Small设置下从83.31下降至79.77，在Large设置下从74.83暴跌至60.61，表明几何分支是保证多视角一致性的关键组件。"
- "在3DGS重建实验中，完整模型的PSNR/SSIM/LPIPS分别为28.24/0.86/0.14，显著优于移除几何分支变体的26.89/0.84/0.17，证明几何分支直接提升了三维结构质量。"
- "与近期基线（WonderWorld, AETHER, Uni3C, Voyager）相比，FANTASYWORLD在WorldScore的多视角一致性（3D Consist.）、照片一致性（Photo Consist.）和风格一致性（Style Consist.）上均取得最高分，且标准差更低，显示出更强的稳定性和泛化能力。"
- "定性结果（图4、图5）直观显示，基线方法在大视角变化下出现撕裂、空洞、风格漂移和结构错乱，而FANTASYWORLD能保持结构连贯和风格一致，且重建的点云布局更干净、纹理更清晰。"
---

# FantasyWorld: Geometry-Consistent World Modeling via Unified Video and 3D Prediction

> [!tip] 核心洞察
> 复用冻结视频扩散模型并从中提取去噪后期语义丰富、结构可靠的特征，结合“反向”DPT解码策略（从深到浅上采样），能够在不损害视频创造力的情况下，高效端到端地产生几何一致且可泛化的3D感知表示，充当世界模型的核心桥梁。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | FantasyWorld：通过统一视频与3D预测实现几何一致性世界建模 |
| 英文题名 | FantasyWorld: Geometry-Consistent World Modeling via Unified Video and 3D Prediction |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=3q9vHEqsNx); [Project](https://fantasy-amap.github.io/fantasy-world/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FANTASYWORLD |
| Dataset | WorldScore static (Small camera motion), WorldScore static (Large camera motion) |

> [!tip] 效果简介
> - WorldScore static (Small camera motion) 上，3D Consist. 为 83.31 ± 14.24，对比 82.85 ± 19.69 (WonderWorld)，变化 +0.46。
> - WorldScore static (Small camera motion) 上，Photo Consist. 为 86.11 ± 7.97，对比 85.48 ± 20.98 (Uni3C)，变化 +0.63。
> - WorldScore static (Small camera motion) 上，Style Consist. 为 94.22 ± 9.11，对比 88.32 ± 18.47 (Uni3C)，变化 +5.90。

## 概述

当前视频基础模型虽具备强大的想象力先验，却普遍缺乏显式的三维几何监督，导致生成内容在空间一致性与结构保真度上存在明显短板——视角变化稍大即出现撕裂、空洞或风格漂移。与此同时，现有方法将视频生成与三维感知视为弱耦合的两阶段流程，不仅无法相互增强，还常依赖按场景优化的后处理（如NeRF或3DGS），计算开销大、泛化能力弱。

FANTASYWORLD针对上述瓶颈，提出一种统一前馈框架：在冻结的视频扩散模型（Wan2.1）内部嵌入可训练的几何分支，通过预备条件模块（PCB）与集成重建生成模块（IRG）实现视频潜变量与隐式三维场的联合前向推理。其核心机制是双向交叉注意力——几何线索约束视频生成、视频先验反哺几何预测，使想象与感知在单一骨干中互相增强，无需额外按场景优化即可输出几何一致的多视角视频与任务无关的三维特征。

实验表明，该设计在多视角一致性上具有决定性优势：在WorldScore基准的小视角变化设置下，完整模型的3D一致性达83.31，移除几何分支后降至79.77；在大视角变化设置下，降幅更为剧烈（74.83→60.61）。在RealEstate10K的3DGS重建实验中，完整模型PSNR/SSIM/LPIPS分别为28.24/0.86/0.14，显著优于无几何分支变体的26.89/0.84/0.17。与近期基线（WonderWorld、AETHER、Uni3C、Voyager）相比，FANTASYWORLD在三维一致性、照片一致性和风格一致性上均取得最高分，且标准差更低，显示出更强的稳定性与泛化能力。

从方法定位看，FANTASYWORLD属于**视频基础模型+几何分支**的联合建模路线，区别于纯视频扩散模型、独立几何重建后处理以及弱耦合的RGB-D联合生成范式。其关键创新在于复用冻结扩散模型深层去噪后的语义丰富特征，结合“反向”DPT解码策略（深到浅上采样），在不损害视频创造力的情况下高效产出可泛化的三维感知表示，充当世界模型的核心桥梁。

当前方法仍存在若干局限：仅支持固定长度片段生成，无法处理长范围连续视频；主要面向静态或准静态场景，对强非刚体运动与时变结构尚未验证；原生相机控制能力弱于部分基线，需通过后处理显式重建增强；训练数据规模约180K视频，域外泛化边界有待进一步探索。

## 背景与动机

### 视频基础模型的想象力先验与空间感知缺口

近期视频基础模型（如 Wan2.1）在开放域视频生成上展现出强大的“想象力先验”——能够从单张图像和文本描述出发，合成外观丰富、时序连贯的视频序列。然而，这些模型的核心瓶颈在于：它们缺乏显式的三维几何监督，导致生成内容在空间一致性和结构保真度上存在根本性缺陷。当相机发生大视角变化时，纯视频扩散模型生成的帧间内容容易出现撕裂、空洞、风格漂移和结构错乱，难以直接支撑需要多视角一致性的三维推理任务。

这一缺口本质上源于视频生成与三维感知的长期割裂。现有方法通常将两者弱耦合：要么在二维生成结果之上后处理地叠加三维重建（如 NeRF 或 3DGS），要么将视频与几何模型独立前向、仅在输入空间进行简单级联。这类方案不仅无法让视频先验与几何线索互相增强，还往往需要按场景单独优化，计算开销大、泛化能力弱。

### 现有世界建模方法的局限

近年来，若干工作尝试将几何一致性引入世界生成。**WonderWorld** 基于单图交互式场景创建，使用分层高斯面元和引导深度扩散，但在大视角变化下仍出现缺失区域和结构断裂。**AETHER** 将重建与视频生成耦合，但输出细节不足。**Uni3C** 支持多模态控制，却在大视角下出现突发的风格偏移。**Voyager** 联合预测 RGB 和深度，通过缓存和几何注入维持一致性，但面临时序不连贯和首帧保真度下降的问题。这些方法的共同困境在于：视频生成与几何推理之间缺乏深层特征层面的双向交互，导致想象与结构无法在统一骨干中相互约束和增强。

### 核心动机：将想象与感知统一在单一骨干中

本文的核心动机在于回答一个关键问题：**如何在不牺牲视频生成创造力的前提下，为其注入可靠的几何基础？** 具体而言，我们希望复用冻结的视频扩散模型，从中提取去噪后期语义丰富、结构可靠的特征，并在此基础上嵌入可训练的几何分支，实现视频潜变量与隐式三维场的联合前向推理。通过双向交叉注意力机制，让几何线索约束视频生成、视频先验反哺几何预测，从而将“想象”与“感知”统一在单个骨干网络中。这一思路的关键洞察在于：去噪后期的视频潜变量已经蕴含了丰富的场景结构信息，通过“反向”DPT 解码策略（从深到浅上采样）利用这些稳定特征，能够在保持视频创造力的同时，高效端到端地产生几何一致且可泛化的三维感知表示，充当世界模型的核心桥梁。

## 核心创新

FANTASYWORLD 的核心创新在于将视频生成与三维感知统一在一个前馈框架中，关键思路是**在冻结的视频基础模型内部嵌入可训练的几何分支**，使想象先验与几何一致性在特征层面相互增强，而非像现有方法那样将二者弱耦合或依赖按场景优化。

### 1. 从纯视频扩散到视频–几何联合建模

现有视频基础模型（如 Wan2.1）虽具备强大的视觉想象力，但缺乏显式的三维监督，导致生成内容的空间一致性和结构保真度不足。FANTASYWORLD 的关键改变在于**增加可训练的几何分支**（Geometry-Consistent Branch），该分支从视频潜变量中直接预测隐式三维场，并通过 3D DPT 头输出深度图、点地图和相机姿态（Sec. 3.1, Fig. 2）。这一设计将模型从纯视频扩散转变为**视频–几何联合前向推理**，使生成过程天然携带几何约束。

### 2. 双向交叉注意力实现想象与结构的融合

传统方法中视频生成与三维感知通常独立前向或仅在输入空间级联，无法互相增强。FANTASYWORLD 在 IRG 块内引入**双向交叉注意力机制（MM-BiCrossAttn）**，使视频令牌与几何令牌在特征层面进行双向信息交换：

$$
A = \mathrm{softmax}\bigg(\frac{Q_v K_g^\top}{\sqrt{d_k}}\bigg)
$$

$$
X_v^+ = X_v + \gamma_v A V_g, \quad X_g^+ = X_g + \gamma_g A^\top V_v
$$

其中，几何→视频方向增强多视角一致性，视频→几何方向则利用想象力先验补全遮挡区域并精炼细节（Sec. 3.3）。这种设计使想象与感知在单一骨干中相互约束、协同优化。

### 3. 两阶段训练策略：冻结骨干，轻量适配

与端到端微调视频扩散模型或独立训练几何模型不同，FANTASYWORLD 采用**两阶段训练**（Sec. 3.4, Sec. 4.1）：

- **阶段一**：冻结 Wan2.1 骨干，仅训练几何分支，通过潜空间桥接使几何分支适配视频特征空间，损失函数为 $\mathcal{L}_{\mathrm{geo}} = \alpha \mathcal{L}_{\mathrm{depth}} + \beta \mathcal{L}_{\mathrm{pmap}} + \gamma \mathcal{L}_{\mathrm{camera}}$；
- **阶段二**：冻结所有核心骨干，仅训练轻量级交叉注意力适配器，以 $\mathcal{L}_{\mathrm{total}} = \mathbb{E}_{z_0,\epsilon,t,c}\Big[\|\epsilon_\theta(z_t,t,c)-\epsilon\|_2^2\Big] + \lambda \mathcal{L}_{\mathrm{geo}}$ 统一优化视频生成与几何预测。

该策略的核心优势在于**复用冻结的视频扩散模型**，在不损害其创造力的前提下，以最小的可训练参数量实现几何一致性的注入。

### 4. “反向”DPT 解码与简化相机控制

FANTASYWORLD 在解码策略和相机控制上同样做出了针对性改变：

- **反向 DPT 解码**：传统 DPT 从浅层提取高频空间细节并上采样最强，而 FANTASYWORLD 采用反转策略——从深层去噪后语义强、噪声低的特征上采样最多，浅层特征下采样，以利用稳定特征（Sec. 3.3, A.3）。
- **简化相机适配器**：将传统 AdaLN（同时预测缩放 $\gamma_i$ 和偏移 $\beta_i$）简化为仅生成偏移 $\beta_i$ 并通过加法注入视频潜变量 $f_i = f_{i-1} + \beta_i$，在保持相机控制能力的同时降低计算开销（Sec. 3.4, A.2）。

### 5. 创新的因果效应

消融实验直接验证了上述创新组件的因果贡献（Table 1, Table 2）：

- **移除几何分支**（Ours w/o 3D）在 Small 设置下使 3D 一致性从 83.31 降至 79.77，在 Large 设置下更是从 74.83 暴跌至 60.61（降幅 14.22），表明几何分支是保证多视角一致性的关键组件；
- 在 3DGS 重建实验中，完整模型的 PSNR/SSIM/LPIPS 为 28.24/0.86/0.14，显著优于移除几何分支变体的 26.89/0.84/0.17，证明几何分支直接提升了三维结构质量。

这些结果表明，FANTASYWORLD 通过**在冻结视频骨干中嵌入可训练几何分支并辅以双向交叉注意力**，成功将想象与感知统一在单个前馈模型中，为世界模型提供了高效且可泛化的几何一致性桥梁。

## 整体框架

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_3q9vHEqsNx/figures/002_Figure_2.jpg]]
*Figure 2: Overview of FANTASYWORLD. Inputs (image, text, camera) are processed by PCBs and stacked IRG blocks, where an asymmetric dual-branch design couples video synthesis with 3D reasoning. The model outputs geometry-consistent video frames and task-agnostic 3D features*

FANTASYWORLD 是一个统一的前馈模型，旨在以单次前向传播同时完成视频生成与隐式3D场景构建。其核心设计理念是：**复用冻结的视频基础模型（Wan2.1）作为想象力先验来源，并在其内部嵌入可训练的几何分支，使视频潜变量与隐式3D场在特征层面深度耦合**，从而实现外观创造力与几何一致性的统一。

### 输入编码

模型接收三类多模态输入，分别由预训练编码器处理：
- **参考图像**：通过 CLIP 编码为视觉条件信号；
- **文本描述**：通过 umT5 编码为语义条件信号；
- **相机轨迹**：采用 Wan 的 Plücker-ray 设计，由可学习的相机编码器生成相机嵌入，作为运动控制信号。

### 骨干网络拆分

FANTASYWORLD 将 Wan2.1 的 WanDiT 去噪骨干拆分为两个功能阶段（Figure 2）：

1. **预条件模块（Preconditioning Blocks, PCB）**：复用冻结的 Wan2.1 前16层去噪器，为后续模块提供部分去噪的潜变量。PCB 的作用是稳定训练初期的潜空间表示并降低梯度方差——Figure 3 的 PCA 可视化显示，PCB 输出的潜变量（红色矩形标注区域）已具备丰富的语义结构，为几何分支提供了可靠的输入基础。

2. **集成重建生成模块（Integrated Reconstruction and Generation Blocks, IRG）**：从第16层开始，在后续24个 Transformer 块后各插入一个 IRG 块。每个 IRG 块采用非对称双分支设计：
   - **想象力先验分支**：继承 Wan2.1 的视频扩散骨干，生成外观丰富的时空特征，最终通过 Wan 解码器输出几何一致的视频帧。
   - **几何一致性分支**：采用类似 VGGT 的架构作为隐式3D特征提取器，从视频潜变量中直接推理相机参数和3D信号，并通过 3D DPT 头输出深度图、点地图和相机姿态。

### 双向交叉注意力：想象与结构的融合枢纽

IRG 块的核心是双向交叉注意力机制（MM-BiCrossAttn），它充当两个分支之间的信息桥梁。给定视频令牌 $X_v$ 和几何令牌 $X_g$，首先计算注意力矩阵：

$$A = \mathrm{softmax}\bigg(\frac{Q_v K_g^\top}{\sqrt{d_k}}\bigg)$$

随后通过带可学习门控 $\gamma_v$、$\gamma_g$ 的残差更新实现双向增强：

$$X_v^+ = X_v + \gamma_v A V_g, \quad X_g^+ = X_g + \gamma_g A^\top V_v$$

这一设计实现了两个方向的互补：**几何→视频**的注意力约束多视角一致性，抑制生成内容的空间撕裂和结构漂移；**视频→几何**的注意力则利用视频先验补全被遮挡区域并精炼几何细节。这种交叉分支监督机制是 FANTASYWORLD 区别于弱耦合方案（视频生成与3D感知独立前向或仅在输入空间级联）的关键差异。

### 输出与下游衔接

模型最终输出两类结果（Figure 2）：
- **几何一致的视频帧**：由 Wan 解码器从想象力先验分支的特征解码得到；
- **任务无关的3D特征**：由 3D DPT 头对几何分支特征进行时空解码产生。3D DPT 头采用“反向”解码策略——从深层去噪后语义强、噪声低的特征进行最强的上采样，浅层特征则被下采样——以利用稳定特征产生更可靠的点地图和深度图。输出帧数通过4倍时间上采样得到：$T = 4(\bar{t} - 1) + 1$。

这些3D特征可直接作为下游任务的通用表示：例如，在 3DGS 重建实验中，模型前馈预测的点云可直接用于初始化高斯面元（Table 2），无需额外的按场景优化（如传统 NeRF 或 3DGS 的逐场景训练），显著降低了计算开销。

### 训练策略

FANTASYWORLD 采用两阶段训练以稳定地桥接视频与几何空间：

- **阶段一（潜空间桥接）**：冻结 Wan2.1 全部骨干，仅训练几何分支。从 Wan2.1 第16层提取隐藏特征，通过轻量 Transformer 适配器馈入几何分支，优化目标为加权几何损失 $\mathcal{L}_{\mathrm{geo}} = \alpha \mathcal{L}_{\mathrm{depth}} + \beta \mathcal{L}_{\mathrm{pmap}} + \gamma \mathcal{L}_{\mathrm{camera}}$。
- **阶段二（统一协同优化）**：冻结所有核心骨干，仅训练插入的双向交叉注意力适配器和相机控制适配器。总训练目标为扩散损失与几何监督损失的组合：$\mathcal{L}_{\mathrm{total}} = \mathbb{E}_{z_0,\epsilon,t,c}[\|\epsilon_\theta(z_t,t,c)-\epsilon\|_2^2] + \lambda \mathcal{L}_{\mathrm{geo}}$。

相机控制采用简化的偏移预测策略：仅生成偏移 $\beta_i$ 并以加法方式注入视频潜变量 $f_i = f_{i-1} + \beta_i$，而非完整自适应层归一化（AdaLN）同时预测缩放和偏移。这一简化设计在保持相机可控性的同时降低了适配器复杂度。

## 核心模块与公式推导

### 3.1 预备条件模块（Preconditioning Blocks, PCB）

FANTASYWORLD 将冻结的视频基础模型 Wan2.1 的前 16 层扩散去噪器复用为 PCB。其核心作用是为后续的几何分支提供**部分去噪的潜变量**：在训练初期，直接从未经去噪的噪声潜变量中提取几何特征会导致梯度方差过大、训练不稳定；PCB 通过前向扩散去噪将潜变量推向语义更丰富、结构更可靠的状态（见 Figure 3 的 PCA 可视化，红框标注的 IRG 输入潜变量已呈现清晰的语义聚类），从而稳定几何分支的早期训练。PCB 本身保持冻结，不参与梯度更新。

### 3.2 集成重建生成模块（Integrated Reconstruction and Generation Blocks, IRG）

IRG 是 FANTASYWORLD 的核心堆叠模块，从 Wan2.1 的第 16 层之后插入，共 24 个 IRG 块。每个 IRG 块采用**非对称双分支设计**：

- **想象力先验分支（Imagination Prior Branch）**：继承 Wan2.1 的视频扩散骨干，负责生成外观丰富的时空特征，保持视频创造力。
- **几何一致性分支（Geometry-Consistent Branch）**：采用与 VGGT 类似的架构作为隐式 3D 特征提取器，将视频特征投影到几何对齐的潜空间，并通过 3D DPT 头解码出深度图、点地图和相机姿态。

两个分支之间的关键耦合机制是**双向交叉注意力（MM-BiCrossAttn）**，实现视频令牌 $X_v$ 与几何令牌 $X_g$ 的特征级相互增强：

$$A = \mathrm{softmax}\bigg(\frac{Q_v K_g^\top}{\sqrt{d_k}}\bigg)$$

$$X_v^+ = X_v + \gamma_v A V_g, \quad X_g^+ = X_g + \gamma_g A^\top V_v$$

其中 $\gamma_v$、$\gamma_g$ 为可学习的门控参数。几何→视频方向（$A V_g$）将多视角一致性约束注入视频生成，抑制大视角变化下的结构撕裂与风格漂移；视频→几何方向（$A^\top V_v$）利用视频先验补全遮挡区域并精炼几何细节。消融实验（Table 1）证实：移除几何分支后，Large 设置下 3D 一致性从 74.83 暴跌至 60.61，降幅达 14.22，表明该双向耦合是宽基线场景下维持空间一致性的决定性机制。

### 3.3 3D DPT 头与“反向”解码策略

几何分支的输出特征通过 3D DPT 头进行时空解码。与传统 DPT 从浅层提取高频空间细节并上采样最强的策略不同，FANTASYWORLD 采用**反转策略**：从深层去噪后语义强、噪声低的特征进行最多上采样，而浅层特征则被下采样。其直觉在于：扩散模型后期（深层）的特征已去除大部分噪声，结构信息可靠；早期（浅层）特征仍残留噪声，直接上采样会放大伪影。该头通过时间上采样块将帧数从 $\bar{t}$ 扩展到最终输出帧数 $T = 4(\bar{t} - 1) + 1$，生成与视频帧对齐的深度图和点地图。

### 3.4 相机控制适配器

相机控制采用简化的偏移预测策略。给定相机嵌入，适配器仅生成偏移参数 $\beta_i$，以加法方式注入视频潜变量：

$$f_i = f_{i-1} + \beta_i$$

相比完整 AdaLN（同时预测缩放 $\gamma_i$ 和偏移 $\beta_i$），该设计减少了可训练参数量，同时保持了有效的相机运动控制能力。

### 3.5 训练目标

训练分两阶段进行。**阶段一**冻结 Wan2.1 全部骨干，仅训练几何分支，通过轻量 Transformer 适配器将第 16 块的隐藏特征桥接到几何分支，损失函数为加权几何监督：

$$\mathcal{L}_{\mathrm{geo}} = \alpha \mathcal{L}_{\mathrm{depth}} + \beta \mathcal{L}_{\mathrm{pmap}} + \gamma \mathcal{L}_{\mathrm{camera}}$$

其中 $\mathcal{L}_{\mathrm{depth}}$ 结合时序梯度匹配损失和逐帧尺度敏感空间损失；$\mathcal{L}_{\mathrm{pmap}}$ 根据预测不确定性加权，惩罚点位置和局部梯度误差；$\mathcal{L}_{\mathrm{camera}}$ 为对 9D 相机参数向量的鲁棒 Huber 损失。

**阶段二**冻结所有核心骨干（包括 Wan2.1 和几何分支），仅训练插入 IRG 块后的双向交叉注意力适配器，总损失为扩散损失与几何损失的联合优化：

$$\mathcal{L}_{\mathrm{total}} = \mathbb{E}_{z_0,\epsilon,t,c}\Big[\|\epsilon_\theta(z_t,t,c)-\epsilon\|_2^2\Big] + \lambda \mathcal{L}_{\mathrm{geo}}$$

相机外参通过变换到第一帧坐标系进行规范对齐 $\tilde{E}_i = E_i E_0^{-1}$，全局尺度则使用有效点的平均半径进行归一化 $s = \frac{1}{|\mathcal{V}|} \sum_{(i,p) \in \mathcal{V}} \|\tilde{X}_{i,p}^w\|_2$。

## 实验与分析

### 核心瓶颈与因果机制验证

FANTASYWORLD 的设计根植于一个明确诊断：当前视频基础模型虽具备强大的“想象力”先验，但缺乏显式 3D 监督，导致生成内容在空间一致性和结构保真度上存在根本性不足；同时，视频生成与 3D 感知通常以弱耦合方式存在，无法互相增强。FANTASYWORLD 的因果操纵变量是在冻结的视频扩散骨干（Wan2.1）中嵌入可训练的几何分支，通过双向交叉注意力实现视频潜变量与隐式 3D 场的联合前向推理，使几何线索约束视频生成、视频先验反哺几何预测。

消融实验直接验证了这一因果机制。**Table 1** 显示，移除几何分支（Ours w/o 3D）后，在 Small 相机运动设置下 3D 一致性从 83.31 降至 79.77，Photo 一致性从 86.11 降至 83.86，Style 一致性从 94.22 降至 92.54；在 Large 相机运动下，3D 一致性更是从 74.83 骤降至 60.61（降幅 14.22）。这一结果直接证明：**几何分支是保证多视角一致性的关键组件，且其重要性随视角变化幅度增大而急剧上升**。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_3q9vHEqsNx/figures/004_Table_1.jpg]]
*Table 1: WorldScore with Small vs. Large camera motion*

在几何保真度层面，**Table 2** 的 3DGS 重建实验进一步佐证：以 VGGT 点云为初始化时，完整模型的 PSNR/SSIM/LPIPS 分别为 28.24/0.86/0.14，而移除几何分支的变体仅为 26.89/0.84/0.17。几何分支带来的 PSNR 提升达 1.35 dB，表明其直接贡献于更准确的三维结构重建。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_3q9vHEqsNx/figures/006_Table_2.jpg]]
*Table 2: 3DGS reconstruction on RealEstate10K. Post-reconstruction (Post Rec) indicates the 3DGS initialization source: either from the VGGT point cloud or our own feed-forward point cloud*

### 世界生成：多视角一致性与风格保真度

在 WorldScore 静态基准的光真实子集（1000 样本）上，FANTASYWORLD 与近期基线方法进行了系统对比。**Table 1** 汇总了 Small 和 Large 相机运动两种设置下的核心指标：

- **Small 相机运动**：FANTASYWORLD 在 3D 一致性（83.31 ± 14.24）、Photo 一致性（86.11 ± 7.97）和 Style 一致性（94.22 ± 9.11）上均取得最高分。相比最强基线，Style 一致性领先 5.90 分（vs. Uni3C 的 88.32），且标准差更低（9.11 vs. 18.47），显示出更强的稳定性和泛化能力。
- **Large 相机运动**：在宽基线场景下，FANTASYWORLD 的 3D 一致性（74.83 ± 16.31）仍略优于 Uni3C（73.95 ± 17.55），而移除几何分支的变体则暴跌至 60.61，再次印证显式几何建模在宽基线场景下的不可替代性。

**Figure 4** 的定性对比直观揭示了基线的典型失败模式：WonderWorld 在大视角变化下出现空洞和缺失区域；Voyager 存在时序不连贯和首帧保真度退化；AETHER 输出细节模糊；Uni3C 出现突发的风格漂移。相比之下，FANTASYWORLD 在不同视角间保持了结构连贯和风格一致。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_3q9vHEqsNx/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison of world generation. WonderWorld shows missing regions, Voyager suffers from temporal incoherence and degraded first-frame fidelity, AETHER produces lowdetail outputs, and Uni3C exhibits abrupt stylistic shifts. In contrast, FANTASYWORLD maintains stronger 3D consistency and coherent style across views*

### 几何保真度：点云结构与重建质量

**Figure 5** 从顶视图和等轴测视图对比了各方法的点云质量。基线方法表现出典型的结构伪影：Voyager 和 AETHER 出现重复墙体、弯曲表面和模糊纹理；Uni3C 的点云布局存在错位。FANTASYWORLD 的点云布局更干净、纹理更清晰，红色标注区域的结构错误显著减少。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_3q9vHEqsNx/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative Comparison of Geometry Fidelity. Top-view and isometric-view point clouds from Voyager, AETHER, Uni3C, and our method. The red-outlined regions indicate typical structural artifacts in baselines (e.g., duplicated walls, bent surfaces, blurred text), while our method preserves cleaner layouts and sharper geometry*

**Table 2** 进一步量化了 3DGS 重建质量。当使用 FANTASYWORLD 自身前馈点云作为初始化时，PSNR/SSIM/LPIPS 为 27.85/0.85/0.15，虽略低于 VGGT 初始化的结果，但已证明其几何分支能够产生有竞争力的前馈 3D 预测（**Figure 7** 提供了与 VGGT 的直接对比）。

### 效率与后处理增强

**Table 3** 对比了各方法的资源消耗。FANTASYWORLD 在保持联合视频-3D 生成能力的同时，GPU 内存和推理时间处于可接受范围（具体数值需查阅原表）。**Table 4** 探索了后处理显式重建的增强效果：对 FANTASYWORLD 的输出施加后处理显式重建后，3D 一致性进一步提升至 88.88，Photo 一致性提升至 86.59，表明框架的隐式 3D 表示可作为更高质量显式重建的有效初始化。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_3q9vHEqsNx/figures/011_Table_4.jpg]]
*Table 4: WorldScore metrics when augmenting FantasyWorld with a post-hoc explicit reconstruction method*

### 失败模式与边界条件

尽管 FANTASYWORLD 在静态场景下表现优异，其设计存在明确的边界条件：

1. **固定长度片段限制**：当前模型仅支持固定长度片段生成，尚未支持连续的长范围视频合成。
2. **动态场景局限**：主要关注静态或准静态场景，无法有效处理强非刚体运动和时变结构。
3. **相机控制权衡**：直接优化目标为几何一致性而非相机控制，原生相机控制能力弱于部分基线，需通过后处理显式重建增强。
4. **域外泛化**：训练数据约 180K 视频片段，域外泛化能力受限于数据覆盖范围（**Figure 8** 展示了部分域外场景的生成结果，虽保持结构稳定，但系统评估尚不充分）。

### 证据强度总结

| 核心主张 | 关键证据 | 置信度 |
|---------|---------|--------|
| 几何分支是保证多视角一致性的关键组件 | Table 1：移除几何分支后 3D 一致性在 Large 设置下从 74.83 降至 60.61 | 0.98 |
| 几何分支直接提升三维结构质量 | Table 2：完整模型 PSNR 28.24 vs. 移除几何分支 26.89 | 0.98 |
| FANTASYWORLD 在多视角一致性上优于近期基线 | Table 1：3D/Photo/Style 一致性均取得最高分，且标准差更低 | 0.95 |
| 定性结果支持定量发现 | Figure 4、Figure 5：基线出现撕裂、空洞、风格漂移，FANTASYWORLD 保持结构连贯 | 0.95 |

## 方法谱系与知识库定位

### 瓶颈与动机

当前视频基础模型（如 Wan2.1）虽具备强大的想象力先验，能生成外观丰富的视频内容，但其训练过程缺乏显式的三维几何监督。这导致生成结果在空间一致性和结构保真度上存在根本性缺陷——多视角画面之间容易出现撕裂、空洞和风格漂移，难以直接支撑需要三维理解的推理任务。与此同时，现有方法在处理视频生成与三维感知时，通常采用弱耦合策略：要么先独立生成视频再后处理重建几何，要么将两者在输入空间简单级联。这类设计使视频先验无法反哺几何预测，几何约束也无法指导视频生成，且往往需要额外的按场景优化步骤（如 NeRF 或 3DGS 的逐场景拟合），计算开销大、泛化性弱。

FANTASYWORLD 的核心动机正是弥合这一“想象”与“感知”之间的鸿沟：在冻结的视频扩散模型内部嵌入可训练的几何分支，通过双向交叉注意力实现视频潜变量与隐式三维场的联合前向推理，使想象与结构在单一骨干中相互增强。

### 方法定位与差异

FANTASYWORLD 的方法定位可以从以下几个关键维度与基线方法进行区分：

**1. 三维几何建模的显式化程度。** 纯视频扩散模型（如 Wan2.1）完全不具备显式的三维建模模块，其多视角一致性仅依赖于隐式的时序先验。FANTASYWORLD 在此基础上增加了可训练的几何分支，从视频潜变量中直接预测隐式三维场，并通过 DPT 头输出深度图、点地图和相机姿态（Sec. 3.1, Fig. 2）。这一设计使几何推理成为前馈过程的内在组成部分，而非后处理附加步骤。

**2. 视频-几何特征的耦合方式。** 现有基线方法中，视频与几何通常独立前向传播或仅在输入空间进行级联。例如，**WonderWorld** 采用分层高斯面元和引导深度扩散实现交互式场景创建，但其视频生成与几何构建之间缺乏特征层面的双向交互。**AETHER** 将重建与视频生成耦合，但耦合程度和交互机制与 FANTASYWORLD 有本质区别。FANTASYWORLD 在 IRG 块内引入双向交叉注意力（MM-BiCrossAttn），使几何令牌与视频令牌在特征层面相互增强：几何线索约束视频生成以提升多视角一致性，视频先验反哺几何预测以补全遮挡区域并精炼细节（Sec. 3.3, Eq. (2)-(3)）。

**3. 训练策略的差异。** 与端到端微调视频扩散模型或独立训练几何模型的基线策略不同，FANTASYWORLD 采用两阶段训练：阶段一冻结视频骨干，仅训练几何分支以完成潜空间桥接；阶段二冻结所有核心骨干，仅训练轻量级交叉注意力适配器（Sec. 3.4, Sec. 4.1）。这一策略在保护视频扩散模型创造力的同时，以最小的可训练参数量实现了几何一致性的注入。

**4. 相机控制适配器的简化。** 基线方法（如 Wan2.1）通常采用完整的自适应层归一化（AdaLN），同时预测缩放参数 $\gamma_i$ 和偏移参数 $\beta_i$。FANTASYWORLD 将其简化为仅预测偏移 $\beta_i$ 并通过加法注入视频潜变量 $f_i = f_{i-1} + \beta_i$（Sec. 3.4, A.2），在保持控制能力的同时降低了适配器的复杂度。

**5. DPT 解码特征源的“反向”策略。** 传统 DPT 解码器从浅层提取高频空间细节并对浅层特征进行最强上采样。FANTASYWORLD 采用反转策略：从深层去噪后语义丰富、噪声低的特征进行最多上采样，浅层特征则下采样，以利用稳定特征进行几何解码（Sec. 3.3, A.3）。这一设计利用了扩散模型后期特征的可靠性优势。

### 与具体基线工作的关系

| 基线方法 | 方法特点 | FANTASYWORLD 的关键差异 |
|---------|---------|----------------------|
| **WonderWorld** | 基于单图交互式场景创建，使用分层高斯面元和引导深度扩散 | 无需逐场景优化，单次前馈即可同时生成视频和隐式三维场；视频与几何在特征层面双向增强 |
| **AETHER** | 统一 RGB-D 建模，将重建与视频生成耦合 | FANTASYWORLD 的耦合更深层（双向交叉注意力 vs. 输入空间级联），且几何分支直接预测隐式三维场而非仅深度 |
| **Uni3C** | 三维世界生成，支持多模态控制 | FANTASYWORLD 在风格一致性上显著优于 Uni3C（+5.90），且标准差更低，表明更强的稳定性和泛化能力（Table 1） |
| **Voyager** | 联合预测 RGB 和深度，使用缓存和几何注入维持一致性 | FANTASYWORLD 避免了 Voyager 在大视角变化下出现的时序不连贯和首帧保真度退化问题（Fig. 4） |

在定量对比中（Table 1），FANTASYWORLD 在 WorldScore 的 Small 和 Large 设置下均取得最高的三维一致性、照片一致性和风格一致性分数，且标准差普遍更低。尤其在 Large 设置下，移除几何分支导致三维一致性从 74.83 骤降至 60.61（降幅 14.22），凸显了显式几何建模在宽基线场景下的不可替代性。

### 适用边界

FANTASYWORLD 的当前设计存在以下适用边界：

1. **片段长度限制。** 模型当前仅适用于固定长度片段的生成，尚未支持连续的长范围视频合成。扩展至无限时长的世界生成需要开发有效的缓存或流式处理机制来维持隐式三维状态。

2. **场景动态性限制。** 主要关注静态或准静态场景，无法有效处理强非刚体运动和时变结构的动态环境。尽管架构理论上兼容动态四维场景，但未在完全动态的四维数据上进行系统性验证与评估。

3. **相机控制能力。** 直接优化目标为几何一致性而非相机或对象控制，因此原生相机控制能力弱于部分基线。通过后处理显式重建可以增强控制能力（Table 4），但这引入了额外的计算步骤。

4. **训练数据覆盖。** 训练数据规模有限（约 180K 视频片段），模型的域外泛化能力可能受限于训练数据的覆盖范围。尽管在域外场景上展示了令人鼓舞的泛化效果（Fig. 8），但系统性的域外评估仍有待开展。

### 开放问题

从 FANTASYWORLD 的设计逻辑和实验结论出发，以下开放问题值得后续工作关注：

1. **创造力与几何基础的平衡。** 如何在不牺牲视频扩散模型创造力的前提下，更高效地注入可靠的几何基础？当前的两阶段训练策略是一种折中方案，但更精细的平衡机制仍有探索空间。

2. **连续长范围生成。** 如何将框架扩展至连续、无限时长的世界生成？这需要开发有效的缓存或流式处理机制来维持和更新隐式三维状态，同时避免误差累积。

3. **动态四维场景适配。** 如何将框架适配至完全动态的四维场景（含非刚体运动、时变结构），并确保几何与外观在时序上的一致性？这涉及对时变几何表示和运动建模的根本性扩展。

4. **通用下游任务表示。** 该隐式三维特征能否作为导航、操作等通用下游任务的可复用表示，从而减少任务特定的微调？这需要在下游任务基准上进行系统性评估。

5. **几何一致性与用户控制的权衡。** 在不降低生成质量的前提下，如何更好地平衡几何一致性与用户控制能力（如精确的相机和对象操控）？后处理显式重建提供了一条路径，但端到端的可控生成仍是开放挑战。

## 原文 PDF

![[paperPDFs/ICLR_2026/FantasyWorld_Geometry_Consistent_World_Modeling_via_Unified_Video_and_3D_Prediction.pdf]]
