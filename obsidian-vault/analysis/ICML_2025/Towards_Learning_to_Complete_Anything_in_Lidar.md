---
title: "Towards Learning to Complete Anything in Lidar"
type: paper
paper_level: A
venue: ICML
year: 2025
pdf_ref: paperPDFs/ICML_2025/Towards_Learning_to_Complete_Anything_in_Lidar.pdf
aliases:
- CCAL
- TLCAL
tags:
- ICML_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "利用2D基础模型从无标签RGB‑Lidar时间序列中挖掘物体形状先验与语义特征，再蒸馏到纯激光雷达实例补全网络中，实现零样本推理。"
primary_logic: "通过伪标签引擎自动提取不完整但可学习的物体占用形状和CLIP特征，训练模型揭示从单帧稀疏观测到完整形状的映射，从而摆脱对人工标注和固定词表依赖。"
claims:
- "伪标签引擎利用视频分割基础模型 SAM 和 SAM 2 定位并跟踪任意物体，将 2D 掩膜提升到激光雷达空间并累积时间观测形成伪标签。"
- "从伪标签中蒸馏 CLIP 特征并回归每个实例的语义 token, 支持测试时通过文本提示进行零样本分类。"
- "在 SemanticKITTI 上 CAL（零样本）达到 13.12 PQ† 和 13.09 mIoU，显著超过自建零样本基线 LODE+SAL (7.74) 和 LiDiff+SAL (7.35)。"
- "CRF 细化将伪标签覆盖提升 1.9‑2.5 倍，使模型性能从 12.25 PQ†（无 CRF）提升至 17.12 PQ†（有 CRF，语义先知）。"
---

# Towards Learning to Complete Anything in Lidar

> [!tip] 核心洞察
> 通过伪标签引擎自动提取不完整但可学习的物体占用形状和CLIP特征，训练模型揭示从单帧稀疏观测到完整形状的映射，从而摆脱对人工标注和固定词表依赖。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 学习在激光雷达中补全任何物体 |
| 英文题名 | Towards Learning to Complete Anything in Lidar |
| 会议/期刊 | ICML 2025 |
| Links | [paper](https://arxiv.org/abs/2504.12264); [Project](https://research.nvidia.com/labs/dvl/projects/complete-anything-lidar) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | CAL (Complete Anything in Lidar) |
| Dataset | SemanticKITTI (val), SSCBench‑KITTI360 (test) |

> [!tip] 效果简介
> - SemanticKITTI (val) 上，PQ† (Zero‑Shot) 为 13.12，对比 PaSCo (M=1) 26.49，变化 -13.37 (约 50% of PaSCo)。
> - SemanticKITTI (val) 上，mIoU (Zero‑Shot) 为 13.09，对比 PaSCo (M=1) 28.22，变化 -15.13 (约 46% of PaSCo)。
> - SemanticKITTI (val) 上，PQ† (Zero‑Shot vs zero‑shot baselines) 为 13.12，对比 LODE+SAL 7.74 ; LiDiff+SAL 7.35，变化 +5.38 / +5.77。

## 概述

激光雷达场景补全旨在从稀疏的单帧点云中恢复完整的场景几何与语义，现有方法依赖封闭集人工标注，无法处理开放词汇下的物体补全与识别。本文提出 **CAL（Complete Anything in Lidar）**，通过从无标签 RGB-Lidar 时间序列中自动挖掘 3D 形状先验与语义特征，实现了零样本、类别无关的实例级场景补全。核心思路是：利用 2D 视觉基础模型（SAM、SAM 2）在多模态序列中定位、跟踪并聚合物体占用，蒸馏 CLIP 特征作为语义锚点，从而训练一个纯激光雷达网络，使其学会从单帧稀疏观测到完整形状与语义 token 的映射。在 SemanticKITTI 和 SSCBench-KITTI360 上，CAL 在零样本设置下分别达到 13.12 PQ† 和 8.57 PQ†，显著超越自建零样本基线（LODE+SAL 7.74 PQ†，LiDiff+SAL 7.35 PQ†），达到全监督方法 PaSCo 的约 44%–50% 性能，同时支持测试时通过自由文本词表进行零样本语义/全景场景补全与 amodal 3D 检测。

**方法定位**：CAL 属于“从无标签多模态数据中蒸馏基础模型知识以驱动零样本激光雷达感知”的范式。其技术路线可拆解为两个协同模块——**伪标签引擎**负责从视频序列中挖掘不完整但可学习的物体占用与 CLIP 特征，**稀疏生成式 3D U-Net + Transformer 实例解码器**则从这些带噪伪标签中学习形状补全与语义回归。与现有工作相比，CAL 在三个关键维度上实现了突破：（i）监督来源从封闭集人工标注转向无标签多模态序列自动挖掘；（ii）类别词表从固定约 20 类扩展为测试时自由形式文本提示；（iii）识别范式从直接预测类别概率转向回归 CLIP 特征并通过余弦相似度完成零样本分类。

**主要结论**：
- 伪标签引擎利用 SAM/SAM 2 的视频目标分割与跨帧掩膜传播，配合 CRF 引导的二值占用细化，可将伪标签覆盖提升 1.9–2.5 倍，是模型有效训练的前提。
- 引入伪语义头 S 对 CLIP 特征进行 K-means 聚类形成伪类别原型，使模型性能从 4.81 PQ† 跃升至 16.08 PQ†（语义先知），证明语义原型分组对学习形状先验至关重要。
- 零样本识别性能受限于底层 CLIP 的表示能力，长尾类别（行人、骑行者）与全监督方法差距显著；伪标签覆盖受限于相机视锥范围（约 28%），实例标签无法到达完全遮挡或相机未观测区域。
- 模型性能与伪标签质量高度耦合，CRF 细化、时域聚合窗口（T_fw=32, T_bw=8）和原型数目（C ∈ {6, 18, 50, 100}）均存在收益递减的饱和点，需根据数据集特性权衡计算开销。

## 背景与动机

激光雷达场景补全（Scene Completion）旨在从稀疏的单帧点云中重建完整的 3D 场景几何与语义，是自动驾驶感知的核心任务之一。现有方法在语义场景补全（SSC）和全景场景补全（PSC）上取得了显著进展，例如 **LMSCNet**（Roldao et al., 2020）、**JS3CNet**（Yan et al., 2021）、**SCPNet**（Xia et al., 2023）以及当前最先进的 **PaSCo**（Cao et al., 2024）。然而，这些方法共享一个根本性瓶颈：**它们依赖封闭集的人工标注进行全监督训练**。

具体而言，这一瓶颈体现在三个层面：

1. **标注依赖**：全监督方法需要逐体素的语义标签或 3D 实例边界框，获取成本极高且难以扩展。
2. **封闭词表**：模型只能识别训练集中预定义的固定类别（通常约 20 类），无法泛化到未标注类别或开放词汇场景。
3. **零样本能力缺失**：当面对训练时未见过的物体类别时，现有方法完全失效，无法完成补全或识别。

近期一些工作尝试突破标注依赖，例如基于隐式神经表示的 **LODE**（Li et al., 2023b）和基于扩散模型的 **LiDiff**（Nunes et al., 2024）实现了无语义标签的场景补全，但它们的补全输出缺乏实例级语义信息。若将其与零样本全景分割方法 **SAL**（Osep et al., 2024）级联，虽可构建零样本基线（LODE+SAL、LiDiff+SAL），但如 Table 2 所示，这些组合在 SemanticKITTI 上的 PQ† 仅分别为 7.74 和 7.35，远未达到实用水平。其核心问题在于：**补全模型与识别模型各自独立训练，缺乏端到端的形状-语义联合学习**。

本文的核心动机正是打破上述双重依赖——既摆脱对人工语义标注的依赖，又突破固定类别词表的限制。关键洞察在于：**无标签的多模态传感器序列（RGB-Lidar）中蕴含丰富的物体形状先验与语义信息**，若能有效挖掘并蒸馏至纯激光雷达补全网络，即可实现零样本的“补全任何物体”。

为此，本文提出 **CAL（Complete Anything in Lidar）**，其核心因果调控变量（causal knob）是：利用 2D 基础模型从无标签 RGB-Lidar 时间序列中自动挖掘物体形状先验与语义特征，再蒸馏到纯激光雷达实例补全网络中。具体而言，CAL 通过以下路径实现零样本推理：

- **伪标签引擎**：利用视频分割基础模型 **SAM**（Kirillov et al., 2023）和 **SAM 2**（Ravi et al., 2024）在 RGB 视频中定位并跟踪任意物体，将 2D 掩膜提升到激光雷达空间并累积时间观测，自动生成带 CLIP 特征的 3D 伪标签（Fig. 2）。
- **形状-语义联合蒸馏**：训练一个稀疏生成式 3D U-Net 结合 Transformer 实例解码器，从单帧稀疏观测中预测完整实例掩码并回归 CLIP 特征（Fig. 3）。
- **测试时零样本分类**：通过计算预测 CLIP 特征与用户指定文本提示的余弦相似度，实现对任意语义类别词表的零样本识别。

这一框架使 CAL 在 SemanticKITTI 上以零样本设置达到 13.12 PQ† 和 13.09 mIoU，显著超越自建零样本基线 LODE+SAL（7.74）和 LiDiff+SAL（7.35），并达到全监督 PaSCo 约 50% 的性能水平（Table 1）。更重要的是，CAL 首次展示了从无标签数据中学习通用物体补全能力的可行性，为开放世界激光雷达感知开辟了新路径。

## 核心创新

CAL 的核心突破在于**完全摆脱对封闭集人工标注的依赖**，通过三个关键维度重构了激光雷达场景补全的范式。

### 1. 从无标签多模态序列中挖掘 3D 形状先验

传统方法（如 **LMSCNet** + MaskPLS、**PaSCo** 等）的训练监督信号完全依赖人工标注的 3D 语义或实例标签，这从根本上限制了可补全物体的类别范围。CAL 的伪标签引擎利用 2D 视觉基础模型——**SAM**（Kirillov et al., 2023）和 **SAM 2**（Ravi et al., 2024）——在无标签的 RGB‑Lidar 时间序列中自动定位、跟踪并聚合物体实例，将 2D 掩膜提升到激光雷达空间，形成不完整但可学习的 3D 占用伪标签（Fig. 2, Sec. 3.1）。这一改变使训练信号来源从“人工定义”转向“数据驱动”，为开放词汇补全奠定了基础。

### 2. 从固定类别分类到零样本语义识别

全监督方法的识别范式是直接预测封闭词表（约 20 类）上的类别概率。CAL 转而回归每个实例的 **CLIP 特征**（Radford et al., 2021），在测试时通过计算预测特征与任意文本提示的余弦相似度实现零样本分类（Sec. 3.2）。这意味着模型不再被训练时的类别集合所束缚——用户只需提供目标类别的文本描述（如 “car”、“cyclist”、“vegetation”），即可灵活切换语义场景补全、全景场景补全或非模态 3D 检测等下游任务（Fig. 1）。

### 3. 伪语义原型引导的形状先验学习

由于伪标签缺乏语义标注，模型如何在没有类别信号的情况下学会有意义的物体形状是一个核心难题。CAL 引入了一个**伪语义头 S**：在训练时对 CLIP 特征进行聚类，形成伪类别原型，并以此作为辅助监督信号（Sec. 3.2, Appx. B.2）。消融实验表明，这一设计是模型性能的关键驱动因素——引入 S 后，语义先知设定下的 PQ† 从 4.81 跃升至 16.08（Tab. 6），证明语义原型分组对于从噪声伪标签中提取形状先验至关重要。

### 4. CRF 引导的标签细化：弥合稀疏观测与稠密补全的鸿沟

伪标签引擎生成的原始标签受限于相机视锥范围（覆盖约 28% 的二值占用区域），且存在边界噪声。CAL 利用 360° 激光雷达聚合获得的稠密二值占用作为引导，通过 **CRF 细化**将实例掩膜传播到未被相机直接观测的区域（Sec. 3.1）。这一步骤将伪标签质量从 12.78 PQ† 提升至 25.90（语义先知设定，Tab. 3），并使最终模型性能从 12.25 PQ† 提升至 17.12 PQ†（Tab. 12），有效弥合了稀疏多模态观测与稠密场景补全之间的信息鸿沟。

### 创新总结

| 维度 | 基线方法 | CAL 方法 | 关键证据 |
|------|----------|----------|----------|
| 训练监督 | 封闭集人工标注 | 无标签多模态序列自动生成 | Sec. 3.1, Fig. 2 |
| 类别词表 | 固定约 20 类 | 测试时自由文本提示 | Fig. 1, Sec. 3.2 |
| 识别范式 | 固定分类头预测概率 | CLIP 特征回归 + 余弦相似度 | Sec. 3.2 |
| 形状先验 | 依赖语义标注隐式学习 | 伪语义原型聚类显式引导 | Tab. 6, Appx. B.2 |

这些创新共同使 CAL 在零样本设定下达到全监督方法 **PaSCo** 约 44‑50% 的性能（SemanticKITTI: 13.12 PQ† vs 26.49; SSCBench‑KITTI360: 8.57 PQ† vs 19.53, Tab. 1），同时显著超越自建零样本基线 **LODE+SAL**（7.74 PQ†）和 **LiDiff+SAL**（7.35 PQ†）（Tab. 2）。

## 整体框架

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2504_12264/figures/003_Figure_3.jpg]]
*Figure 3: CAL model architecture and training pipeline. The backbone consists of a sparse encoder and a dense 3D convolutional block. We estimate scene-level occupancy using a multiscale sparse generative decoder that consists of decoder blocks D , two occupancy heads B _ { o } and B _ { s } , , and a pseudo-semantic head (S) at each scale L. The Transformer decoder then predicts segmentation masks over the completed scene and regresses CLIP features*

CAL（Complete Anything in Lidar）的整体设计围绕一个核心洞察展开：**利用无标签多模态视频序列自动挖掘物体形状先验与语义特征，再将其蒸馏到纯激光雷达实例补全网络中，从而摆脱对人工标注和固定词表的依赖**。整个框架由两大关键组件构成：（i）一个伪标签引擎（Pseudo-labeling Engine），负责从校准后的 RGB‑Lidar 序列中自动生成带语义特征的 3D 实例补全伪标签；（ii）一个零样本、类不可知的物体补全模型，在训练时仅接收伪标签，测试时仅依赖单帧激光雷达输入即可完成实例级补全与开放词汇识别。

### 输入输出流

模型的输入为单帧激光雷达点云 $P = \{ p_n \}_{n=1}^N, p_n \in \mathbb{R}^4$，包含空间位置和强度通道。输出为一组已完成补全的物体实例，每个实例由以下信息表示：

- **体素占用掩码**：在正则体素网格上的二值占用，描述物体的完整 3D 形状；
- **实例 ID**：区分不同物体实例；
- **语义特征**：每个实例对应一个预测的 CLIP 特征向量，用于测试时通过文本提示进行零样本分类。

通过提供不同的语义类别词表，CAL 可在测试时被“提示”执行多种下游任务：语义场景补全（SSC）、全景场景补全（PSC）或非模态 3D 物体检测（Figure 1）。

### 伪标签引擎

伪标签引擎是整个框架的“知识挖掘器”，其核心目标是**从不具备任何 3D 标注的 RGB‑Lidar 时间序列中提取不完整但可学习的物体占用形状和 CLIP 特征**。该引擎包含六个步骤（Figure 2）：

1. **视频物体分割**：利用视频分割基础模型（SAM 2）在 RGB 视频中定位并跟踪任意物体实例，生成时空掩膜（masklet）；
2. **2D→3D 提升**：利用已知的传感器标定和自车位姿，将每个 masklet 从 2D 图像空间提升到激光雷达空间，在时间维度上累积稀疏观测；
3. **形状补全与特征提取**：对每个实例生成体素化的完整占用表示，并从 RGB 图像中提取逐实例的 CLIP 特征，在时序上取平均以获得多视角视觉‑语言特征；
4. **360° 占用聚合**：累积多帧 360° 激光雷达扫描，获得全场景的二值占用先验；
5. **CRF 引导的标签细化**：利用条件随机场（CRF）将聚合的伪标签与全场景二值占用进行对齐和细化，显著提升伪标签覆盖率和质量；
6. **输出伪标签对**：将单帧稀疏激光雷达扫描与对应的完整实例掩码及 CLIP 特征配对，形成训练数据。

伪标签引擎的覆盖范围受限于相机视锥（约 28% 的体素网格），但 360° 激光雷达聚合和 CRF 细化可将伪标签覆盖提升 1.9‑2.5 倍，有效缓解这一限制。

### 补全模型

CAL 的补全模型在架构上借鉴了 PaSCo（Cao et al., 2024）的设计，但训练目标完全来自伪标签引擎（Figure 3）。模型由以下模块串联而成：

- **稀疏生成式 3D U‑Net 骨干网络**：包含稀疏编码器和密集 3D 卷积块，通过多尺度生成解码器在三个分辨率层级（$L \in \{1, 2, 4\}$）上估计场景级占用；
- **Transformer 实例解码器**：在占用体素空间上交互可学习查询，输出类不可知的实例掩码和 CLIP 特征；
- **伪语义头（S）与原型分类**：训练时对 CLIP 特征进行聚类形成伪类别原型，辅助网络学习物体形状先验，测试时丢弃。

训练总损失由二值占用损失、原型分类损失、掩码损失和 CLIP 特征蒸馏损失加权求和构成：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{occ}} \mathcal{L}_{\mathrm{occ}} + \lambda_{\mathrm{prot}} \mathcal{L}_{\mathrm{prot}} + \lambda_{\mathrm{mask}} \mathcal{L}_{\mathrm{mask}} + \lambda_{\mathrm{CLIP}} \mathcal{L}_{\mathrm{CLIP}} + \mathcal{L}_{\mathrm{aux}}$$

其中 $\mathcal{L}_{\mathrm{occ}}$ 为三个分辨率尺度上二值占用损失的平均，$\mathcal{L}_{\mathrm{mask}}$ 使用加权二值交叉熵和 Dice 损失的组合监督实例掩码。

### 模块关系与信息流

整体信息流可概括为：**伪标签引擎从多模态序列中挖掘形状‑语义先验 → 伪标签对驱动补全模型训练 → 模型学习从单帧稀疏观测到完整形状的映射 → 测试时仅需单帧激光雷达即可完成零样本补全与识别**。伪标签引擎和补全模型在训练阶段是串行的（先离线生成伪标签，再训练模型），在推理阶段补全模型独立运行，无需 RGB 图像或时序信息。

## 核心模块与公式推导

### 任务形式化

CAL 接收单帧激光雷达点云作为输入：

$$P = \{ p_n \}_{n=1}^N, \quad p_n \in \mathbb{R}^4$$

其中每个点包含三维空间坐标和强度通道。模型的目标是输出一组完整的物体实例，每个实例由体素占用函数定义：

$$O_k : \mathbb{R}^4 \to \mathbb{N}^3, \quad k \leq K$$

即 $K$ 个实例在正则体素网格上的占用映射。每个实例同时附带一个预测的 CLIP 语义特征，支持测试时通过文本提示进行零样本分类。

### 核心模块一：伪标签引擎

伪标签引擎是 CAL 实现无监督训练的关键组件，其流程如 Figure 2 所示，包含六个步骤：

1. **视频物体分割与跟踪**：利用 SAM（Kirillov et al., 2023）和 SAM 2（Ravi et al., 2024）在 RGB 视频序列中定位并跟踪任意物体，生成时空物体掩膜（masklet）。
2. **2D→3D 提升**：借助标定好的多模态传感器配置和已知的车辆位姿，将每个 masklet 从图像空间提升到激光雷达空间。
3. **时序聚合与形状补全**：在时间维度上累积多帧观测，生成体素化的完整物体表示，同时为每个实例提取 CLIP（Radford et al., 2021）特征。
4. **360° 占用累积**：聚合 360° 激光雷达扫描获得全场景二值占用，作为后续细化的先验。
5. **CRF 引导的标签细化**：利用条件随机场（CRF）将聚合的伪标签与二值占用进行对齐和细化，显著提升伪标签覆盖率和质量——在 SemanticKITTI 上覆盖提升 2.5 倍，在 SSCBench-KITTI360 上提升 1.9 倍。
6. **输出**：为每帧稀疏激光雷达扫描配对补全后的物体级伪标签和时序平均的 CLIP 特征。

### 核心模块二：稀疏生成式 3D U-Net 骨干网络

模型结构如 Figure 3 所示，包含以下关键子模块：

- **稀疏编码器**：对输入点云进行稀疏体素化编码。
- **密集 3D 卷积块**：将稀疏特征转换为密集特征图。
- **多尺度生成解码器**：包含三个解码块 $D^{1:L}$，在 $L \in \{1, 2, 4\}$ 三个分辨率层级上估计场景占用。每个尺度配备两个占用头 $B_o$ 和 $B_s$，以及一个伪语义头 $S$。
- **Transformer 实例解码器**：在占用体素空间上操作可学习查询，输出类不可知的实例掩码和 CLIP 特征回归值。

### 核心模块三：伪语义头与原型分类

伪语义头 $S$ 仅在训练时使用。其工作原理为：对伪标签中的 CLIP 特征进行聚类，形成 $C$ 个伪类别原型；网络通过预测每个体素所属的原型来学习物体的形状先验。消融实验（Table 6）表明，引入 $S$ 将模型性能从 4.81 PQ† 大幅提升至 16.08 PQ†（语义先知设置），证明语义原型分组对形状先验学习至关重要。CLIP 原型数目 $C$ 在 $\{6, 18, 50, 100\}$ 范围内性能鲁棒，但极端值 $C=1$ 或 $C=500$ 导致明显退化（Table 7）。

### 关键公式：训练损失函数

总训练损失由四个主要项加权求和构成：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{occ}} \mathcal{L}_{\mathrm{occ}} + \lambda_{\mathrm{prot}} \mathcal{L}_{\mathrm{prot}} + \lambda_{\mathrm{mask}} \mathcal{L}_{\mathrm{mask}} + \lambda_{\mathrm{CLIP}} \mathcal{L}_{\mathrm{CLIP}} + \mathcal{L}_{\mathrm{aux}}$$

各损失项含义如下：

- **$\mathcal{L}_{\mathrm{occ}}$**：多尺度二值占用损失，在三个分辨率层级上取平均：

$$\mathcal{L}_{\mathrm{occ}} = \frac{1}{|\{1,2,4\}|} \sum_{\mathrm{L} \in \{1,2,4\}} \mathcal{L}_{\mathrm{occ}}^{\mathrm{1:L}}$$

使用二值交叉熵监督，标签来自 360° 激光雷达聚合的二值占用。

- **$\mathcal{L}_{\mathrm{prot}}$**：原型分类损失，使用交叉熵和 Lovász 损失监督伪语义头 $S$ 的预测，标签来自 CLIP 特征聚类分配的伪类别。

- **$\mathcal{L}_{\mathrm{mask}}$**：实例掩码损失，组合加权二值交叉熵和 Dice 损失：

$$\mathcal{L}_{\mathrm{mask}} = \lambda_{\mathrm{CE}} \mathcal{L}_{\mathrm{CE}} + \lambda_{\mathrm{Dice}} \mathcal{L}_{\mathrm{Dice}}$$

- **$\mathcal{L}_{\mathrm{CLIP}}$**：CLIP 特征蒸馏损失，监督 Transformer 解码器回归的 CLIP token 与伪标签中的 CLIP 特征对齐。

### 零样本推理机制

测试时，模型对每个预测实例输出一个 CLIP 特征向量。给定任意语义类别词表，通过计算预测 CLIP 特征与文本编码之间的余弦相似度，获得每个查询在指定词表上的后验概率分布，实现零样本分类。全景质量评估采用标准公式：

$$PQ = SQ \times RQ$$

即分割质量（SQ）与识别质量（RQ）的乘积。

## 实验与分析

### 核心实验设计

CAL 在零样本（Zero‑Shot, ZS）和语义先知（Semantic Oracle, SO）两种设定下接受评估。ZS 设定完全依赖预测的 CLIP 特征与文本提示的余弦相似度进行分类；SO 设定则将每个预测掩码按体素多数投票分配真实语义标签，用于隔离补全质量与识别能力的贡献。对比基线分为两类：（1）全监督全景场景补全方法，包括 **LMSCNet+MaskPLS**（Roldao et al., 2020; Marcuzzi et al., 2023）、**JS3CNet+MaskPLS**（Yan et al., 2021; Marcuzzi et al., 2023）、**SCPNet+MaskPLS**（Xia et al., 2023; Marcuzzi et al., 2023）和 **PaSCo**（Cao et al., 2024）；（2）自建的零样本基线，将隐式补全方法 **LODE**（Li et al., 2023b）和扩散补全方法 **LiDiff**（Nunes et al., 2024）分别与零样本全景分割器 **SAL**（Osep et al., 2024）级联，构成 LODE+SAL 与 LiDiff+SAL。评估指标采用全景质量 $PQ = SQ \times RQ$（及其变体 PQ†）和 mIoU，在 SemanticKITTI 验证集和 SSCBench‑KITTI360 测试集上进行。

### 主结果分析

**Table 1** 汇总了全景场景补全的主结果。在 SemanticKITTI 上，CAL（ZS）达到 13.12 PQ† 和 13.09 mIoU，分别相当于全监督 PaSCo（M=1）的约 50% 和 46%。在 SSCBench‑KITTI360 上，CAL（ZS）为 8.57 PQ† 和 8.49 mIoU，约为 PaSCo 的 44% 和 40%。这一差距主要源于零样本识别对长尾类别（如行人、骑行者）的召回不足（见 Table 15），而非补全质量本身——当使用语义先知时，CAL（SO）在 SemanticKITTI 上达到 17.12 PQ†，显著缩小了与全监督方法的距离。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2504_12264/figures/005_Table_1.jpg]]
*Table 1: Panoptic Scene Completion. We compare CAL against LMSCNet (Roldao et al., 2020) + MaskPLS (Marcuzzi et al., 2023), JS3CNet (Yan et al., 2021) + MaskPLS, SCPNet (Xia et al., 2023) + MaskPLS, and PaSCo (Cao et al., 2024) (M=1 and Ensemble)*

**Table 2** 展示与零样本基线的对比。CAL（ZS）以 13.12 PQ† 大幅领先 LODE+SAL（7.74）和 LiDiff+SAL（7.35），优势分别达 +5.38 和 +5.77 个点。定性结果（Figure 6, Figure 8）表明，基线方法生成的补全结果结构松散、语义混乱，而 CAL 输出更连贯的物体形状，且能正确预测交叉路口等复杂几何结构（Figure 4 第 4 行），尽管输入点云仅提供稀疏的直接证据。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2504_12264/figures/007_Table_2.jpg]]
*Table 2: Panoptic scene completion results with zero-shot baselines. We compare CAL against the zero-shot baselines we construct: LODE (Li et al., 2023b) + SAL (Osep et al., 2024) and LiDiff (Nunes et al., 2024) + SAL (Osep et al., 2024). Results reported on the SemanticKITTI dataset*

### 关键消融发现

#### 伪标签引擎消融

**CRF 细化**是伪标签质量的决定性因素（Table 3）。在 SemanticKITTI SO 设定下，CRF 将伪标签自身的 PQ† 从 12.78 提升至 25.90（提升约 2 倍）；在 SSCBench‑KITTI360 上，提升幅度为 1.9 倍。这一质量跃迁直接传导至下游模型训练：使用 CRF 伪标签训练的 CAL（SO）达到 17.12 PQ†，而无 CRF 时仅为 12.25（Table 12）。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2504_12264/figures/009_Table_3.jpg]]
*Table 3: CRF refinement ablation. We evaluate pseudo-label quality with and without CRF refinement on SemanticKITTI and SSCBench-KITTI360. Results show that CRF refinement significantly improves pseudo-label quality in both datasets and settings*

**时序聚合窗口**的消融（Table 4）显示，前向传播帧数 $T_{fw}=32$、后向 $T_{bw}=8$ 时伪标签 PQ† 达到最优（12.21），继续增大帧数收益递减。值得注意的是，即使使用短窗口（$T_{fw}=8, T_{bw}=0$），配合 CRF 仍可达到 22.06 PQ† 的补全质量（Table 11），表明 CRF 能部分补偿跟踪时长不足的问题，对降低伪标签引擎的计算开销具有实际意义。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2504_12264/figures/011_Table_4.jpg]]
*Table 4: Pseudo-labeling engine ablations, semantic oracle (SO). Pseudo-labels benefit from forward and backward propagation, with notable improvements up to T _ { f w } = 3 2 and T _ { b w } = 8 frames*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2504_12264/figures/017_Table_11.jpg]]
*Table 11: Impact of the number of frames on completion quality with CRF on Semantic KITTI (Behley et al., 2019) (val). This study demonstrates that CRF significantly enhances completion quality, allowing the use of fewer frames in the pseudo-labeling pipeline which is computationally expensive due to the costly mask propagation step. The first block evaluates mask tracking over 8 frames, while the second block uses our original setting with 32 frames forward and 8 frames backward tracking*

**覆盖范围分析**（Table 5）揭示了伪标签的根本局限：相机视锥范围内的实例标签仅覆盖约 28% 的体素网格（SemanticKITTI 28.04%，SSCBench‑KITTI360 27.38%）。360° 激光雷达聚合虽提升了二值占用覆盖，但实例级标签仍受限于相机可见区域。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2504_12264/figures/010_Table_5.jpg]]
*Table 5: Coverage analysis. Coverage of mask pseudo-labels (w/o CRF, Label) and binary occupancy (w/o 360◦ aggr., Occ.)*

#### 模型组件消融

Table 6 剖析了 CAL 模型各模块的贡献。最关键的发现是**伪语义头 S 的引入**：将 S 加入训练使模型性能从 4.81 PQ† 急剧跃升至 16.08 PQ†（SO 设定）。这表明通过对 CLIP 特征进行原型聚类形成伪类别分组，能有效引导网络学习物体形状先验，是 CAL 从噪声伪标签中提取信号的核心机制。相比之下，二值占用头 $B_o$ 使用部分覆盖（$B_o^{pc}$）或全覆盖（$B_o^{fc}$）标签训练的影响相对温和。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2504_12264/figures/013_Table_6.jpg]]
*Table 6: CAL model ablations. We analyze the contribution of CAL’s key design choices and components: training B _ { o } with partial coverage ( B _ { o } ^ { p c } ) or with full coverage ( B _ { o } ^ { f c } ) , introducing S, and adding B _ { s } . Introducing S provides a significant improvement, likely due to its implicit semantic regularization. Training with full coverage ( B _ { o } ^ { f c } ) and B _ { s } further improve performance. bility with the camera frustums (Sec. 3.1). CRF improves this coverage by 1.9× on SSCBench-KITTI360 and 2.5× on SemanticKITTI. Similarly, binary occupancy coverage benefits from full Lidar scan aggregation, improving coverage from 37.36% to 99.96% on Semanti...*

**CLIP 原型数目 C** 的鲁棒性分析（Table 7）表明，在 $C \in \{6, 18, 50, 100\}$ 范围内性能稳定，但极端取值 $C=1$（丧失分组能力）或 $C=500$（过度碎片化）会导致明显退化。这一发现验证了伪语义分组对形状先验学习的必要性，同时说明该方法对超参数不敏感。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2504_12264/figures/012_Table_7.jpg]]
*Table 7: Number of CLIP prototypes. We evaluate SSC/PSC performance on SemanticKITTI when varying the number of CLIP prototypes C. We observe similar performance with C $\in {6, 18, 50, 100}$, indicating general robustness to C. Extreme cases ( C = 1 and C = 5 0 0 ) result in performance degradation*

#### 数据质量消融

Table 12 和 Table 13 分别展示了在 SemanticKITTI 和 SSCBench‑KITTI360 上使用不同质量伪标签训练模型的效果。一致结论是：**带 CRF 细化的伪标签在所有指标上均显著优于无 CRF 版本**。进一步按 thing/stuff 类别细分发现，CRF 对 thing 类别的分割质量和识别召回提升尤为明显，但对 stuff 类别改善有限——这与 CRF 主要优化实例边界而非语义区域扩展的机制一致。

### 失败模式与局限性

1. **零样本识别的长尾退化**：Table 15 的逐类分析显示，CAL 对行人、骑行者等低频类别的识别性能远低于全监督方法。这受限于底层 CLIP 特征空间的表示能力，而非补全质量本身——语义先知设定下这些类别的补全质量显著更高。

2. **伪标签覆盖的视锥限制**：尽管 360° 激光雷达聚合改善了二值占用覆盖，实例标签仍无法到达相机未观测或被完全遮挡的区域，导致模型在这些区域缺乏监督信号。

3. **伪标签质量依赖性**：模型性能与伪标签质量高度耦合。训练时容易过拟合于常见且完全可见的实例，对部分观测或罕见物体的泛化能力有限。

4. **计算效率瓶颈**：伪标签引擎涉及视频分割、跨帧掩膜传播、CRF 细化等密集计算步骤。虽然 CRF 可部分补偿短跟踪窗口（Table 11），但整体效率仍有优化空间，限制了在大规模数据集或实时系统中的应用。

5. **评估场景有限**：当前验证仅覆盖 SemanticKITTI 和 KITTI‑360 两个数据集，尚未在更多样化的场景或传感器配置下测试跨域泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2504_12264/figures/014_Table_8.jpg]]
*Table 8: Pseudo-labeling engine configuration with dataset-specific parameters for SemanticKITTI and KITTI360*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2504_12264/figures/015_Table_9.jpg]]
*Table 9: Pseudo-labeling engine ablations using CLIP semantics. This table presents an analysis on the key parameters of the pseudo-label aggregation process: the number of frames for tracking T _ { f w } and T _ { b w } , as well as the stride, w*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2504_12264/figures/016_Table_10.jpg]]
*Table 10: Pseudo-label evaluation restricted to the areas in the voxel grid for which we have pseudo-labels. Analysis of the accuracy of pseudo-labels on the SemanticKITTI (Behley et al., 2019) validation set. The full-grid eval setting refers to evaluating our pseudo-labels using the usual PSC evaluation with respect to the GT. The masked-voxel eval setting refers to excluding the voxels for which we don’t have any pseudo-labels during PSC evaluation*

## 方法谱系与知识库定位

### 1. 在激光雷达场景补全谱系中的位置

CAL 处于“从封闭集监督向开放词汇零样本补全”的转折点。传统激光雷达场景补全方法——无论是语义场景补全（SSC）还是全景场景补全（PSC）——均依赖密集的人工标注和固定类别词表。代表性全监督基线包括：

- **LMSCNet + MaskPLS** (Roldao et al., 2020; Marcuzzi et al., 2023)：将语义占用预测与实例分割头组合，需要逐体素语义/实例标签。
- **JS3CNet + MaskPLS** (Yan et al., 2021; Marcuzzi et al., 2023)：基于点体素联合表示的语义场景补全。
- **SCPNet + MaskPLS** (Xia et al., 2023; Marcuzzi et al., 2023)：引入扩散先验的场景补全方法。
- **PaSCo** (Cao et al., 2024)：当前全景场景补全的最先进方法，采用稀疏生成式 U-Net 和 Transformer 实例解码器，但需要完整的实例级语义标注。

这些方法共享两个根本约束：**训练需要封闭集人工标注**（3D 边界框或逐体素语义/实例标签），且**词汇表固定**（通常约 20 类）。CAL 通过伪标签引擎和 CLIP 特征蒸馏，将监督来源从“人工标注”切换为“无标签多模态视频序列自动挖掘”，将识别范式从“固定分类头”切换为“测试时文本提示的零样本分类”。

在零样本场景补全这一新设定下，论文构建了两个基线：**LODE + SAL**（Li et al., 2023b; Osep et al., 2024）和 **LiDiff + SAL**（Nunes et al., 2024; Osep et al., 2024），分别将隐式神经表示补全和扩散补全与零样本全景分割器 SAL 级联。CAL 在 SemanticKITTI 上以 13.12 PQ† 显著超过这两个基线（7.74 和 7.35），证明端到端学习从稀疏观测到完整形状的映射，优于“先补全再分割”的级联方案。

### 2. 关键技术路径与知识来源

CAL 的核心创新在于将三个独立发展的技术路线融合到统一框架中：

| 技术路线 | 知识来源 | 在 CAL 中的角色 |
|---------|---------|---------------|
| 视频/图像分割基础模型 | SAM (Kirillov et al., 2023), SAM 2 (Ravi et al., 2024) | 在无标签视频中定位并跟踪任意物体，生成时空掩膜（masklet） |
| 视觉-语言模型 | CLIP (Radford et al., 2021) | 为每个实例提取语义特征，支持测试时零样本分类 |
| 稀疏生成式场景补全 | PaSCo (Cao et al., 2024) | 提供骨干网络和 Transformer 实例解码器的架构基础 |

伪标签引擎（Figure 2）是连接这些路线的桥梁：它将 2D 基础模型的开放世界分割能力提升到 3D 空间，通过多帧时序聚合和 CRF 细化生成带 CLIP 特征的实例占用伪标签。这一设计使得 CAL 能够利用大规模无标签多模态序列进行训练，从而摆脱对人工标注的依赖。

### 3. 适用边界与关键局限

**（1）伪标签覆盖受限于相机视锥**

伪标签引擎依赖 RGB 相机进行实例分割和 CLIP 特征提取，因此实例标签仅覆盖相机可见区域（约 28% 的 360° 激光雷达占用区域，Table 5）。虽然 360° 激光雷达聚合提升了二值占用覆盖，但被遮挡或未进入相机视场的物体无法获得实例伪标签。这意味着模型在训练时对相机视场外的物体缺乏监督，可能在这些区域产生遗漏。

**（2）零样本识别性能受限于 CLIP 表示能力**

CAL 的识别能力完全依赖 CLIP 特征的质量。对于长尾或罕见类别（如行人、骑行者），CLIP 的视觉-语言对齐较弱，导致零样本分类性能远低于全监督方法（Table 15 逐类分析可证实这一点）。这是 CLIP 本身的表示瓶颈，而非 CAL 框架的设计缺陷。

**（3）模型性能与伪标签质量高度耦合**

消融实验表明，CRF 细化将伪标签质量从 12.78 PQ† 提升至 25.90（语义先知），并将最终模型性能从 12.25 PQ† 提升至 17.12（Table 3, Table 12）。伪语义头 S 的引入更是将模型性能从 4.81 PQ† 大幅提升至 16.08（Table 6）。这说明 CAL 对伪标签的质量和语义先验的注入方式非常敏感，训练时容易过拟合于常见且完全可见的实例。

**（4）计算开销与效率**

伪标签引擎涉及 SAM/SAM 2 的视频分割、跨帧掩膜传播、多帧 3D 提升和 CRF 细化，计算成本较高。论文提出用 CRF 可部分补偿短跟踪窗口（Table 11：T_fw=8, T_bw=0 配合 CRF 可达 PQ† 22.06），但整体效率仍有优化空间，限制了在大规模数据集或实时系统中的应用。

**（5）评估范围有限**

当前评估仅限 SemanticKITTI 和 KITTI-360 两个数据集，尚未在更多样化的场景、传感器配置或天气条件下验证。此外，零样本设定下缺乏对“模型预测出但数据集中未标注物体”的定量评估手段。

### 4. 开放问题

1. **长尾类别的形状先验学习**：如何在零样本范式下引入分布感知的聚类或形状先验，使模型对罕见类别也能生成合理的完整形状？当前伪语义头 S 的原型聚类（CLIP 原型数目 C 在 {6, 18, 50, 100} 内鲁棒，Table 7）提供了初步方向，但极端长尾情形仍需更精细的建模。

2. **完全未观测区域的补全**：能否利用自监督激光雷达预测（如掩码自编码器）填补相机视场外的区域，进一步提升伪标签覆盖范围？当前 360° 聚合仅提供二值占用，缺乏实例和语义信息。

3. **伪标签引擎的效率优化**：如何降低视频分割和 CRF 细化的计算开销？短跟踪窗口配合 CRF 的策略（Table 11）已显示出权衡空间，但更高效的替代方案（如单帧基础模型 + 轻量传播）值得探索。

4. **开放世界评估协议**：在无人工标注约束下，如何定量评估开放世界补全的质量？特别是对于数据集中未标注但被模型预测出的物体，需要新的评估指标和基准。

5. **跨传感器与纯视觉扩展**：CAL 框架依赖校准的多模态传感器设置。能否将其扩展到纯相机输入的场景补全任务，或适配不同的激光雷达-相机配置？这需要解决深度估计和跨模态对齐的额外挑战。

6. **从“补全”到“理解”的闭环**：当前 CAL 将补全和识别解耦为顺序步骤（先补全形状，再用 CLIP 特征分类）。是否存在端到端的联合优化方案，使补全过程能够感知语义信息，从而提升对语义模糊区域的补全质量？

## 原文 PDF

![[paperPDFs/ICML_2025/Towards_Learning_to_Complete_Anything_in_Lidar.pdf]]
