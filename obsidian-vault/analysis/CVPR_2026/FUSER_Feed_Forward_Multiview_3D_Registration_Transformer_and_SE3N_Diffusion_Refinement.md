---
title: "FUSER: Feed-Forward Multiview 3D Registration Transformer and SE(3)$^N$ Diffusion Refinement"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FUSER_Feed_Forward_Multiview_3D_Registration_Transformer_and_SE_3_N_Diffusion_Refinement.pdf
project_link: null
code_link: "https://github.com/Jiang-HB/FUSER"
aliases:
- FFD
- FUSER
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 首次提出前馈式多视角配准Transformer（FUSER），将所有扫描统一编码到紧凑隐空间，通过交替注意力直接预测每个扫描的全局刚性位姿，彻底消除成对配准和位姿同步。
primary_logic: 利用绝对坐标的稀疏3D CNN编码保留平移线索，设计几何交替注意力实现高效的扫描内与跨扫描消息传递，并创新性地将2D基础模型的注意力先验迁移至3D点云推理，从而在单一前馈过程中实现高质量全局位姿回归。
claims:
- FUSER是首个无需任何成对估计、直接输出全局位姿的前馈多视角配准Transformer。
- 在ScanNet（30 scans）上，FUSER将平均平移误差从0.37m降至0.15m，平均旋转误差从17.4°降至6.7°，大幅超越端到端方法MDGD。
- 在ArkitScenes（200 scans）上，FUSER达到90.3%配准召回率，FUSER-DF进一步提升至92.0%。
- 在3DMatch（60 scans）上，FUSER仅需0.31秒完成推理，而两阶段方法耗时数分钟，同时取得优越配准精度。
---

# FUSER: Feed-Forward Multiview 3D Registration Transformer and SE(3)$^N$ Diffusion Refinement

> [!tip] 核心洞察
> 利用绝对坐标的稀疏3D CNN编码保留平移线索，设计几何交替注意力实现高效的扫描内与跨扫描消息传递，并创新性地将2D基础模型的注意力先验迁移至3D点云推理，从而在单一前馈过程中实现高质量全局位姿回归。

| 字段 | 内容 |
|------|------|
| 中文题名 | FUSER：前馈多视角3D注册Transformer与SE(3)^N扩散细化 |
| 英文题名 | FUSER: Feed-Forward Multiview 3D Registration Transformer and SE(3)$^N$ Diffusion Refinement |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.09373) · [Code](https://github.com/Jiang-HB/FUSER) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | FUSER 与 FUSER-DF (扩散细化) |
| Dataset | ScanNet, 3DMatch, ArkitScenes |

> [!tip] 效果简介
> - ScanNet (30 scans) 上，Translation Error (Mean) / Rotation Error (Mean) 0.15 m / 6.7° vs 0.37 m / 17.4° (MDGD) (降低约59%平移误差和61%旋转误差)。
> - 3DMatch (60 scans) 上，Registration Recall (RR), Rotation Error (RE), Translation Error (TE) RR最高, RE/TE显著优于可比方法 vs 多种描述子（FPFH, FCGF, GeoTransformer等）结合SGHR位姿图 (取得全面的最优精度)。
> - ArkitScenes (200 scans) 上，Registration Recall (RR) / Rotation Error (RE) / Translation Error (TE) FUSER: 90.3% / 3.2° / 0.14m; FUSER-DF: 92.0% / 3.1° / 0.14m vs 次优方法 (未指定名) 的RR, RE, TE均低于FUSER (FUSER-DF 相对FUSER提升1.7% RR，RE 降低0.1°)。

## 概要

多视角三维点云配准是三维视觉与机器人领域的基础任务，其目标是将一组来自不同视点的局部扫描对齐到统一的全局坐标系中。传统方法遵循**两阶段范式**：首先对所有扫描对进行独立的成对配准，再通过位姿图同步恢复全局位姿。这一范式存在三个根本性瓶颈：（1）成对估计缺乏全局几何约束，导致局部歧义与误差累积；（2）冗余的成对计算开销巨大，随扫描数量平方级增长；（3）位姿同步阶段强依赖手工设计的异常值过滤与优化策略，限制了灵活性与全局最优性。

本文提出 **FUSER**——首个**前馈式多视角配准Transformer**，从根本上打破上述两阶段范式。FUSER将所有扫描统一编码到紧凑的隐空间中，通过交替注意力机制实现扫描内与跨扫描的高效消息传递，并在单一前馈过程中直接预测每个扫描的全局刚性位姿，完全消除了成对配准与位姿同步环节。在此基础上，进一步提出 **FUSER-DF**，将多视角位姿修正建模为联合 SE(3)$^N$ 流形上的先验条件扩散去噪过程，以FUSER的预测为起点进行小步精炼，实现精度进一步提升。

核心创新可概括为三点：
- **绝对几何编码**：利用稀疏3D CNN（MinkowskiEngine）提取保留绝对坐标信息的超点特征，为平移回归提供关键线索。
- **几何交替注意力**：32层交替堆叠的内部扫描自注意与交叉扫描注意，实现排列等变的多视图消息传递；并首次将2D重建基础模型（π³）的注意力权重迁移至3D点云推理，显著提升配准精度。
- **参考帧无关的位姿监督**：通过所有扫描对的相对位姿损失间接监督全局位姿，无需依赖真实世界坐标系。

实验结果表明，FUSER在多个基准上实现了精度与效率的双重突破：
- 在 **ScanNet**（30 scans）上，平均平移误差从 0.37m 降至 **0.15m**，平均旋转误差从 17.4° 降至 **6.7°**，大幅超越端到端方法MDGD。
- 在 **3DMatch**（60 scans）上，FUSER仅需 **0.31秒** 完成推理，而传统两阶段方法耗时数分钟，同时取得最优配准精度。
- 在 **ArkitScenes**（200 scans）上，FUSER达到 **90.3%** 配准召回率，FUSER-DF进一步提升至 **92.0%**。

FUSER的提出标志着多视角配准从“成对估计+后优化”迈向“全局前馈推理”的范式转变，为大规模、实时三维重建提供了新的技术路径。



三维场景理解与重建的核心前提是将多个部分重叠的点云扫描对齐到一个统一的全局坐标系中。这项任务——多视角点云配准——在自动驾驶、机器人导航、增强现实和数字孪生等应用中扮演着基础性角色。然而，尽管该领域已有数十年的研究积累，大规模、高精度的多视角配准仍然是一个开放挑战。

### 传统两阶段范式的结构性缺陷

当前主流方法遵循一个经典的两阶段范式：**成对相对位姿估计**与**全局位姿同步**。具体而言，系统首先对所有扫描对独立执行配准，估计每对之间的相对刚性变换；随后通过位姿图优化或同步算法，将这些成对估计融合为一致的全局位姿。

这一范式存在三个根本性瓶颈：

1. **缺乏全局几何约束**：成对估计阶段将每个扫描对视为独立问题，无法利用多视图间的一致性信息。当扫描重叠度低、几何纹理重复或存在对称结构时，成对匹配极易产生模糊估计，这些局部模糊在后续同步阶段难以被完全纠正。

2. **误差累积与异常值敏感**：成对估计的误差在位姿同步过程中会传播和放大。位姿图优化通常依赖手工设计的异常值过滤策略（如基于循环一致性的剪枝），这些启发式规则引入了强归纳偏置，限制了方法的灵活性和全局最优性。

3. **冗余计算开销巨大**：对 $N$ 个扫描，理论上需要 $O(N^2)$ 次成对配准。即使采用共视性剪枝，实际计算量仍然庞大。传统流程在 3DMatch（60 scans）上通常耗时数分钟，难以满足实时应用需求。

### 端到端方法的进展与局限

近年来，一些工作尝试将多视角配准纳入端到端学习框架。**LMVR**（Yew and Lee, 3DV 2021）联合优化成对与全局配准，**MDGD**（Li et al., IEEE RA-L 2024）基于图网络进行端到端多视角推理，**FeatSync**（Jin et al., CVPR 2024）通过特征同步实现多视图一致性。然而，这些方法仍保留了成对匹配的核心结构——它们或显式预测相对位姿，或依赖成对特征交互，未能从根本上突破两阶段范式的限制。

以 MDGD 为例，该方法在 ScanNet（30 scans）上的平均平移误差为 0.37m，平均旋转误差达 17.4°，表明端到端图网络在缺乏全局约束的情况下，精度仍然有限。

### 本文动机：前馈全局推理的新范式

上述分析揭示了一个核心洞察：**多视角配准的本质困难不在于成对匹配本身，而在于缺乏一个统一的全局推理机制**。如果能够将所有扫描同时编码到一个紧凑的隐空间中，并通过高效的消息传递直接回归每个扫描的全局刚性位姿，就可以彻底消除成对估计和位姿同步这两个冗余步骤。

基于这一动机，本文提出 **FUSER**——首个前馈式多视角配准 Transformer。FUSER 的核心思想是：利用绝对坐标感知的稀疏 3D CNN 保留平移线索，设计几何交替注意力实现扫描内与跨扫描的高效消息传递，并创新性地将 2D 基础模型的注意力先验迁移至 3D 点云推理，从而在单一前馈过程中实现高质量的全局位姿回归。在此基础上，FUSER-DF 进一步将多视角位姿校正建模为联合 SE(3)$^N$ 流形上的先验条件扩散去噪过程，实现精细化的位姿优化。



## 核心方法与创新机理

FUSER 的核心创新在于**彻底颠覆了传统多视角点云配准的两阶段范式**。传统方法（如 **MDGD** Li et al., IEEE RA-L 2024；**SGHR** Wang et al., CVPR 2023）依赖“成对相对位姿估计 + 全局位姿同步”的串行流程：先对所有扫描对进行独立的成对配准（常使用 **GeoTransformer** Qin et al., CVPR 2022 等描述子），再通过位姿图优化或同步算法恢复全局位姿。这一范式存在三重根本性缺陷：

1. **缺乏全局几何约束**：成对估计各自为政，无法利用多视图间的联合一致性，导致估计模糊与误差累积；
2. **计算冗余巨大**：$N$ 个扫描需要 $O(N^2)$ 次成对匹配，耗时数分钟；
3. **强依赖手工设计的异常值过滤与同步策略**，限制了灵活性与全局最优性。

FUSER 以**单阶段前馈全局位姿直接回归**取代上述范式，其关键创新可拆解为以下四个 changed slots：

---

### 注册范式：从“成对+同步”到“联合前馈回归”

FUSER 是首个无需任何成对估计、直接输出全局位姿的前馈多视角配准 Transformer。所有扫描被统一编码到紧凑隐空间，通过交替注意力机制一次性推理出每个扫描的全局刚性位姿，彻底消除了成对配准和位姿同步两个环节。这一范式转换带来了精度与效率的双重跃升：在 ScanNet（30 scans）上，FUSER 将平均平移误差从 0.37m 降至 0.15m，平均旋转误差从 17.4° 降至 6.7°，同时推理时间从数分钟压缩至 0.31 秒（3DMatch, 60 scans）。

---

### 特征编码：从“平移不变”到“绝对坐标感知”

传统成对配准方法通常采用平移不变的相对坐标归一化特征（如 KPConv），这有利于学习旋转等变表示，却丢失了对全局平移回归至关重要的绝对位置线索。FUSER 改用基于 MinkowskiEngine 的**绝对坐标感知稀疏 3D CNN**，通过 5 层步长为 2 的稀疏卷积层级（见 Figure 6）将输入点云编码为保留绝对位置信息的低分辨率超点特征。消融实验表明，去除绝对位置信息会导致平移误差显著增加——这一设计是 FUSER 能够直接回归全局平移的关键前提。

---

### 多视图交互推理：从“独立成对注意”到“几何交替注意力”

传统方法中，各扫描对的注意力或匹配是独立执行的，扫描间缺乏直接的信息交换。FUSER 设计了**几何交替注意力模块**：共 32 层 Transformer，交替执行 16 层内部扫描自注意（intra-scan self-attention）和 16 层交叉扫描注意（cross-scan attention），使所有扫描在统一隐空间中同时进行消息传递。该模块具有排列等变性（见公式 $\mathrm{AA}(P_{\pi}(\mathcal{S}'), P_{\pi}(\mathcal{F})) = P_{\pi}(\mathrm{AA}(\mathcal{S}', \mathcal{F}))$），保证输出不依赖扫描输入顺序。

更具突破性的是，FUSER 首次将 **2D 基础模型的注意力先验迁移至 3D 点云推理**：交替注意力层的权重从 $\pi^3$（一个在大规模 2D 图像重建任务上训练的 VGGT 变体）预训练权重初始化，用正弦编码替换原 2D ROPE 位置编码。消融实验（Table 4）证实，这一跨模态注意力初始化带来了显著的旋转和平移精度提升，验证了 2D→3D 注意力迁移的有效性。

---

### 位姿预测与监督：从“成对预测+全局监督”到“全局回归+相对损失间接监督”

传统方法预测成对相对位姿，并依赖真实世界坐标系进行全局监督，这引入了参考帧依赖。FUSER 直接回归每扫描的全局位姿——旋转通过 MLP 头输出 $3\times3$ 代理矩阵，经 SVD 正交化投影到 SO(3)；平移由另一 MLP 头直接预测。训练采用**参考帧无关的相对位姿损失**间接监督：综合测地旋转损失 $\mathcal{L}_{\mathbf{r}}$、鲁棒平移损失 $\mathcal{L}_{\mathbf{t}}$（Huber）和点云一致性损失 $\mathcal{L}_{\mathbf{p}}$，在所有扫描对上计算并平均：

$$\mathcal{L} = \frac{1}{N(N-1)} \sum_{i \neq j} [\mathcal{L}_{\mathbf{r}}(i,j) + \gamma_{t}\mathcal{L}_{\mathbf{t}}(i,j) + \gamma_{p}\mathcal{L}_{\mathbf{p}}(i,j)]$$

这种间接监督策略使全局位姿学习不依赖于特定世界坐标系，增强了泛化性。

---

### 细化机制：从“无细化/经典同步”到“SE(3)$^N$ 扩散先验去噪”

传统方法无细化步骤，或仅依赖经典同步优化。FUSER-DF 创新性地将多视角位姿修正建模为**联合 SE(3)$^N$ 流形上的先验条件扩散去噪过程**：以 FUSER 的位姿预测 $\hat{\mathbf{T}}_{1:N}$ 为先验，从最优位姿 $\mathbf{T}_i^0$ 向先验方向扩散加噪，构建训练数据：

$$\mathbf{T}_{i}^{t} = \mathrm{Exp}(\gamma\sqrt{1-\bar{\alpha}_{t}}\varepsilon) \mathcal{F}(\sqrt{\bar{\alpha}_{t}}; \mathbf{T}_{i}^{0}, \hat{\mathbf{T}}_{i})$$

其中 $\mathcal{F}$ 在最优位姿与先验之间按 $\sqrt{\bar{\alpha}_t}$ 插值。逆向过程学习一个 SE(3)$^N$ 去噪器，从 FUSER 的先验估计出发，逐步精炼至更优位姿。训练由先验条件变分下界监督（Eq. 9），FUSER 本身充当多视图代理注册模型。这一设计使 FUSER-DF 在 ArkitScenes 上将配准召回率从 90.3% 进一步提升至 92.0%。

---

### 创新总结

FUSER 的创新链条清晰且自洽：**绝对坐标编码**保留平移线索 → **几何交替注意力**实现高效的多扫描联合推理 → **2D 注意力先验迁移**注入跨模态归纳偏置 → **全局位姿直接回归**消除两阶段瓶颈 → **SE(3)$^N$ 扩散细化**提供可选的精度增益。这一系列 changed slots 共同构成了首个真正端到端的前馈多视角配准框架，在精度、效率与可扩展性上均显著超越传统两阶段方法。



FUSER 提出了一种全新的多视角点云配准范式：将传统“成对配准 + 位姿同步”两阶段流程彻底重构为单一的前馈式全局位姿回归。其核心 pipeline 由三个紧密耦合的模块组成，数据流从前端点云编码到多视角推理再到位姿输出，全程无需任何显式的成对匹配或位姿图优化。

### 输入与输出

**输入**：一组无序的多视角点云扫描 $\mathcal{S} = \{S_1, S_2, \dots, S_N\}$，每个扫描 $S_i \in \mathbb{R}^{M_i \times 3}$ 包含不同数量的三维点。序列长度 $N$ 在训练时随机采样于 2 至 50 之间，推理时可灵活适配不同规模（从 ScanNet 的 30 帧到 ArkitScenes 的 200 帧）。

**输出**：每个扫描的全局刚性位姿 $\mathbf{T}_i \in SE(3)$，以旋转矩阵 $\mathbf{R}_i \in SO(3)$ 和平移向量 $\mathbf{t}_i \in \mathbb{R}^3$ 的形式直接回归。FUSER-DF 变体在此基础上通过扩散去噪输出进一步细化的位姿。

### 三大核心模块

#### 模块一：绝对几何编码器 (Absolute Geometric Encoder)

该模块负责将原始点云压缩为紧凑的隐空间表示，同时保留对平移回归至关重要的绝对位置线索。具体采用基于 MinkowskiEngine 的 5 层稀疏 3D CNN（步长 2，核大小 3），通过层次化体素化与稀疏卷积，将每个扫描编码为低分辨率的超点特征（Figure 6）。与传统成对配准中常用的平移不变编码（如 KPConv 相对坐标归一化）不同，绝对几何编码直接保留点云的绝对坐标信息，为后续全局平移预测提供必要的几何锚点。

#### 模块二：几何交替注意力 (Geometric Alternating Attention)

这是 FUSER 实现多视角联合推理的核心机制。模块共包含 $L = 32$ 层 Transformer，交替堆叠 16 层扫描内自注意力（intra-scan self-attention）和 16 层扫描间交叉注意力（cross-scan attention）。所有扫描的特征被拼接为一个统一的序列，在交替注意力层中同时进行扫描内部的几何特征增强和跨扫描的上下文消息传递，从而在单一前馈过程中完成全局几何推理。

该模块的设计具备排列等变性——去除学习型参考令牌后，模块输出对输入扫描顺序保持不变：
$$\mathrm{AA}(P_{\pi}(\mathcal{S}'), P_{\pi}(\mathcal{F})) = P_{\pi}(\mathrm{AA}(\mathcal{S}', \mathcal{F}))$$

一个关键创新是**2D 注意力先验迁移**：交替注意力层的权重由大规模 2D 图像重建基础模型 π³（VGGT 变体）的预训练权重初始化，将 2D Transformer 学到的注意力模式迁移至 3D 点云推理。位置编码方面，用正弦编码替代 2D ROPE 以适应三维几何空间。消融实验证实该迁移策略带来了显著的旋转和平移精度提升（Table 4）。

#### 模块三：全局位姿预测器 (Global Pose Predictor)

在几何交替注意力完成多视角消息传递后，全局位姿预测器从超点特征中回归每个扫描的 6-DoF 位姿。具体流程为：首先通过自注意力和全局平均池化聚合扫描级特征，然后由两个轻量 MLP 头分别预测平移向量 $\hat{\mathbf{t}}_i$ 和一个 $3 \times 3$ 的旋转代理矩阵，最后通过 SVD 正交化将代理矩阵投影到 $SO(3)$ 得到 $\hat{\mathbf{R}}_i$。

**监督策略**：考虑到全局坐标系定义的模糊性，FUSER 采用参考帧无关的相对位姿损失进行间接监督。总损失综合了三项：
$$\mathcal{L} = \frac{1}{N(N-1)} \sum_{i \neq j} [\mathcal{L}_{\mathbf{r}}(i,j) + \gamma_{t}\mathcal{L}_{\mathbf{t}}(i,j) + \gamma_{p}\mathcal{L}_{\mathbf{p}}(i,j)]$$

其中 $\mathcal{L}_{\mathbf{r}}$ 为测地旋转损失，$\mathcal{L}_{\mathbf{t}}$ 为鲁棒 Huber 平移损失，$\mathcal{L}_{\mathbf{p}}$ 为点云一致性损失（权重 $\gamma_t = \gamma_p = 0.1$，Huber 阈值 $\beta = 0.06$）。该设计使模型无需依赖真实世界坐标系即可学习全局一致的位姿。

### FUSER-DF：SE(3)^N 扩散细化

FUSER-DF 在 FUSER 预测的基础上增加了一个后处理细化阶段。其核心思想是将多视角位姿修正建模为联合 $SE(3)^N$ 流形上的先验条件扩散去噪过程（Figure 3）。与标准扩散从最优位姿向纯噪声扩散不同，FUSER-DF 的**先验感知扩散**从最优位姿向 FUSER 的先验预测 $\hat{\mathbf{T}}_{1:N}$ 方向扩散：
$$\mathbf{T}_{i}^{t} = \mathrm{Exp}(\gamma\sqrt{1-\bar{\alpha}_{t}}\varepsilon) \mathcal{F}(\sqrt{\bar{\alpha}_{t}}; \mathbf{T}_{i}^{0}, \hat{\mathbf{T}}_{i})$$

其中 $\mathcal{F}$ 为位姿插值函数，在最优位姿与先验估计之间按扩散进度 $\sqrt{\bar{\alpha}_t}$ 进行插值并注入随机扰动。逆向过程学习一个 $SE(3)^N$ 去噪器 $p_\theta$，从先验位姿逐步去噪至最优位姿，训练由先验条件变分下界监督。FUSER 本身在此过程中充当代理注册模型，估计残差位姿以支持渐进式去噪。

### 推理效率

整个 FUSER 推理流程极为高效：在 3DMatch（60 帧）上仅需 0.31 秒，在 ArkitScenes（200 帧）上仅需 0.61 秒，而传统两阶段方法通常需要数十秒至数分钟。FUSER-DF 因扩散去噪步骤，推理时间分别增加至 2.91 秒和 6.50 秒，仍远快于传统流程。GPU 内存占用方面，得益于紧凑的超点表示和 FlashAttention 优化，200 帧序列仅需 2.83 GB 显存（FUSER-DF 为 5.09 GB）。

### 补充图表

![[assets/figures/papers/paper_list_l2037_https_arxiv_org_abs_2512_09373/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of paradigms. Conventional multiview registration relies on redundant pairwise estimation (time-consuming and no global constraint) and pose synchronization (outlier sensitivity and high inductive bias). By contrast, our FUSER directly predicts global poses through unified feed-forward reasoning across all scans without any pairwise matching, delivering outstanding accuracy and efficiency (minutes→seconds)*

![[assets/figures/papers/paper_list_l2037_https_arxiv_org_abs_2512_09373/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of FUSER. It encodes unordered scans into a compact latent space via Absolute Geometric Encoding, then performs 2D attention prior-enhanced Geometric Alternating Attention for multiview reasoning and final pose regression*



### 3.1 绝对几何编码器 (Absolute Geometric Encoder)

FUSER 的几何编码器承担将无序点云压缩为紧凑超点特征的关键角色，其设计直接服务于全局位姿回归对**绝对平移线索**的需求。传统多视角配准方法（如基于 KPConv 的编码器）通常将点云归一化到局部坐标系，导致平移信息丢失，仅能支持成对相对位姿估计。FUSER 采用基于 **MinkowskiEngine** 实现的 5 层稀疏 3D CNN（步长 2，核大小 3，结构见 Figure 6），在原始世界坐标系下执行层次化体素化与稀疏卷积，输出低分辨率超点特征。该编码器保留了超点的绝对空间坐标信息，为后续交替注意力模块提供可区分的平移线索——消融实验间接表明，去除绝对位置信息会导致平移误差显著增加。

![[assets/figures/papers/paper_list_l2037_https_arxiv_org_abs_2512_09373/figures/011_Figure_6.jpg]]
*Figure 6: Network architecture of absolute geometric encoder*

### 3.2 几何交替注意力模块 (Geometric Alternating Attention)

这是 FUSER 实现多视图联合推理的核心机制。模块共堆叠 **L = 32 层**，交替执行 16 层**内部扫描自注意**（intra-scan self-attention）和 16 层**交叉扫描注意**（cross-scan attention），使得所有扫描的几何特征在统一隐空间中同时进行消息传递。该设计具备排列等变性（permutation equivariance），即输出对输入扫描顺序不敏感，其形式化保证为：

$$
\mathrm{AA}(P_{\pi}(\mathcal S'), P_{\pi}(\mathcal F)) = P_{\pi}(\mathrm{AA}(\mathcal S', \mathcal F))
$$

其中 $P_{\pi}$ 为扫描序列的任意排列操作，$\mathcal S'$ 为超点坐标与特征的联合表示，$\mathcal F$ 为可学习特征。去除学习参考令牌后，该等变性成立。

**2D 注意力先验迁移**是本模块的另一关键创新。FUSER 的交替注意力层权重并非随机初始化，而是从大规模 2D 图像重建任务预训练的 **π³**（VGGT 变体）迁移而来。为适配 3D 几何推理，位置编码从 2D ROPE 替换为正弦编码。消融实验（Table 4）验证，该跨模态注意力初始化显著提升了旋转和平移精度。

### 3.3 全局位姿预测与监督

经交替注意力推理后的超点特征，通过自注意、全局平均池化及两个轻量 MLP 头分别回归平移向量和一个 $3 \times 3$ 旋转代理矩阵，再经 **SVD 正交化**投影到 SO(3)，得到每帧扫描的全局刚性位姿。

由于全局位姿依赖于任意世界坐标系的选择，FUSER 采用**参考帧无关的间接监督策略**：通过所有扫描对的相对位姿损失来约束全局位姿。总损失函数为：

$$
\mathcal{L} = \frac{1}{N(N-1)} \sum_{i \neq j} \left[\mathcal{L}_{\mathbf{r}}(i,j) + \gamma_{t}\mathcal{L}_{\mathbf{t}}(i,j) + \gamma_{p}\mathcal{L}_{\mathbf{p}}(i,j)\right]
$$

其中三个分量分别为：

- **测地旋转损失**：$\mathcal{L}_{\mathbf{r}}(i,j) = \operatorname{arccos}\frac{\mathrm{Tr}(\mathbf{R}_{ij}^{\top}\hat{\mathbf{R}}_{ij})-1}{2}$，度量预测相对旋转与真值之间的测地距离。
- **鲁棒平移损失**：采用 Huber 损失 $\mathcal{L}_{\mathbf{t}}(i,j)$，阈值 $\beta = 0.06$，权重 $\gamma_t = 0.1$。
- **点云一致性损失**：$\mathcal{L}_{\mathbf{p}}(i,j)$ 通过变换后对应点的空间一致性提供额外几何约束，权重 $\gamma_p = 0.1$。

### 3.4 SE(3)$^N$ 扩散细化 (FUSER-DF)

FUSER-DF 将多视角位姿修正形式化为**联合 SE(3)$^N$ 流形上的先验条件去噪扩散过程**。与标准扩散从数据向纯噪声扩散不同，其前向过程从最优位姿向 FUSER 预测的先验 $\hat{\mathbf{T}}_{i}$ 插值并注入随机扰动：

$$
\mathbf{T}_{i}^{t} = \mathrm{Exp}(\gamma\sqrt{1-\bar{\alpha}_{t}}\varepsilon) \; \mathcal{F}(\sqrt{\bar{\alpha}_{t}}; \mathbf{T}_{i}^{0}, \hat{\mathbf{T}}_{i})
$$

其中插值函数 $\mathcal{F}$ 定义为：

$$
\mathcal{F}(\sqrt{\bar{\alpha}_{t}}; \mathbf{T}_{i}^{0}, \hat{\mathbf{T}}_{i}) = \mathbf{Exp}\left((1 - \sqrt{\bar{\alpha}_{t}}) \cdot \mathrm{Log}(\hat{\mathbf{T}}_{i} (\mathbf{T}_{i}^{0})^{-1})\right) \mathbf{T}_{i}^{0}
$$

$\gamma$ 为噪声尺度，$\bar{\alpha}_t$ 控制插值权重。逆向过程学习一个 SE(3)$^N$ 去噪器 $p_{\theta}$，以 FUSER 先验为条件逐步精炼位姿。FUSER 本身在此充当**代理注册模型**（surrogate registration model），估计残差位姿以支持渐进去噪。训练由先验条件变分下界监督（Eq. 9），该下界包含先验匹配项与去噪匹配项，使学习过程有效利用 FUSER 提供的初始估计。Figure 3 展示了该先验感知去噪流程，Figure 4 定性展示了扩散细化前后重建表面光滑度的提升。

![[assets/figures/papers/paper_list_l2037_https_arxiv_org_abs_2512_09373/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline of prior-aware*



## 实验与关键发现

### 主实验结果

FUSER 在多个标准多视角配准基准上全面验证了其精度与效率优势。以下按数据集逐一分析关键结果。

**ScanNet（30 scans）**：如表 1 所示，FUSER 在 ScanNet 的 30 扫描多视角配准任务上取得显著领先。与端到端多视角配准方法 **MDGD**（Li et al., IEEE RA-L 2024）相比，FUSER 将平均平移误差从 0.37 m 降至 0.15 m（降幅约 59%），平均旋转误差从 17.4° 降至 6.7°（降幅约 61%）。这一提升的核心驱动力在于 FUSER 的前馈全局推理机制——所有扫描在统一的紧凑隐空间中同时进行消息传递，从根本上消除了成对估计的误差累积和全局约束缺失问题。

**3DMatch（60 scans）**：在 3DMatch 基准上（表 2），FUSER 与多种主流描述子结合位姿图优化的两阶段方法进行了对比。基线包括 **FPFH**、**FCGF**、**GeoTransformer**（Qin et al., CVPR 2022）等描述子，均与 **SGHR**（Wang et al., CVPR 2023）位姿图同步器组合。FUSER 和 FUSER-DF 在所有指标（Registration Recall、Rotation Error、Translation Error）上均取得最优精度。值得注意的是，FUSER 仅需 0.31 秒完成推理（表 5），而传统两阶段流程通常耗时数十秒至数分钟——这一效率优势源于消除了冗余的成对匹配计算。

**ArkitScenes（200 scans）**：在大规模场景测试中（表 3），FUSER 达到 90.3% 的配准召回率（RR）、3.2° 旋转误差（RE）和 0.14 m 平移误差（TE）。引入 SE(3)ᴺ 扩散细化后的 FUSER-DF 进一步将 RR 提升至 92.0%，RE 降至 3.1°。扩散细化带来的增益虽有限（RR +1.7%，RE -0.1°），但验证了在 FUSER 强先验基础上进行小步去噪精炼的有效性。

**定性分析**：图 5 展示了 FUSER 与 SOTA 方法（GeoTransformer + SGHR 位姿图）的定性配准对比，FUSER 重建的全局场景几何一致性明显更优。图 4 则直观展示了扩散细化前后表面平滑度的改善。此外，图 7 报告了在 iPhone 14 Pro Max 采集的真实世界多视角序列上的泛化结果，表明 FUSER 在未见域数据上仍保持较好的配准质量。

### 消融实验

表 4 报告了关键设计选择的消融结果，揭示了 FUSER 性能的两个核心支撑要素。

**2D 注意力先验迁移**：从 2D 重建基础模型 π³（VGGT 变体）迁移预训练权重到几何交替注意力层，显著提升了旋转和平移精度。这一结果表明，大规模 2D 图像重建任务中习得的注意力模式可以作为有效的 3D 点云推理初始化先验，缓解了 3D 数据稀缺带来的训练困难。该跨模态迁移策略是 FUSER 区别于以往纯 3D 训练方法的关键创新。

**训练数据规模**：依次添加 ArkitScenes、ScanNet++、3DMatch 数据集进行训练，配准精度持续提升。这说明 FUSER 的前馈架构能够有效利用更大规模的多源数据，模型容量（约 0.6B 参数）足以吸收多样化的几何模式。

**绝对几何编码**：分析指出，去除绝对位置信息的平移不变编码会导致平移误差显著增加。FUSER 采用的 MinkowskiEngine 稀疏 3D CNN 保留了绝对坐标线索，为全局位姿回归（尤其是平移分量）提供了必要的空间参考——这是传统相对坐标归一化方法无法胜任的。

### 效率分析

表 5 汇总了运行时对比。在 3DMatch（60 scans）上，FUSER 推理仅需 0.31 s，FUSER-DF 需 2.91 s；在 ArkitScenes（200 scans）上，FUSER 需 0.61 s，FUSER-DF 需 6.50 s。两阶段方法通常需要数十秒至数分钟。效率优势来自两方面：（1）紧凑的超点表示大幅压缩了 Transformer 的序列长度；（2）FlashAttention 等工程优化降低了注意力计算开销。GPU 内存占用同样可控，最长序列（200 scans）下 FUSER 仅占 2.83 G 显存，FUSER-DF 占 5.09 G。

### 局限与失败模式

尽管 FUSER 取得了全面的精度与效率优势，仍存在若干值得关注的局限：

1. **模型规模与训练成本**：约 0.6B 参数、需 8 块 NVIDIA L20 GPU 训练，对资源有限的学术复现构成障碍。
2. **扩散细化的效率代价**：FUSER-DF 虽提升精度，但推理时间从 0.31 s 升至 2.91 s（3DMatch），在低延迟场景下可能优先选择无细化的 FUSER。
3. **绝对编码的鲁棒性**：绝对几何编码依赖稠密坐标提供平移线索，在极度稀疏或噪声严重的真实扫描中可能鲁棒性下降。iPhone 实验虽展示了较好泛化，但缺乏系统性的退化场景测试。
4. **2D 先验迁移的泛化性**：当前仅验证了 π³ 这一特定 VGGT 变体的迁移效果，其对其他 2D 基础模型（如 DINOv2、SAM）的适用性尚未探索。
5. **场景覆盖范围**：训练和评估集中于室内场景数据集（ScanNet、ArkitScenes、3DMatch、ScanNet++），未见对大规模室外场景（如 KITTI、Waymo）的评估，室外场景的稀疏性和尺度变化可能带来新的挑战。

### 方法谱系与知识库定位

FUSER 在多视角点云配准领域实现了范式级创新，其定位可从以下维度理解：

- **相对于两阶段方法**：传统流程依赖“成对配准 + 位姿同步”（如 GeoTransformer + SGHR、FCGF + 位姿图优化），存在成对估计模糊、误差累积和计算冗余问题。FUSER 首次以单一前馈 Transformer 直接输出全局位姿，彻底消除了成对匹配和同步步骤。
- **相对于端到端方法**：此前端到端方法如 **MDGD**（Li et al., 2024）仍基于图网络进行扫描间消息传递，但未引入 2D 注意力先验和绝对坐标编码。FUSER 通过几何交替注意力、2D 先验迁移和绝对编码，在精度上大幅超越 MDGD。
- **相对于扩散配准方法**：SE(3) 扩散配准已有初步探索，但 FUSER-DF 首次将其扩展到多视角联合空间 SE(3)ᴺ，并以 FUSER 的预测作为先验条件，实现了先验感知的去噪精炼——这与无条件扩散或成对扩散有本质区别。
- **跨模态桥接**：从 2D 基础模型向 3D 任务迁移注意力先验的策略，为 3D 视觉中利用大规模 2D 预训练模型开辟了新路径。

### 补充图表

![[assets/figures/papers/paper_list_l2037_https_arxiv_org_abs_2512_09373/figures/004_Table_1.jpg]]
*Table 1: Multiview registration performance on the ScanNet (30 scans) [18]*

![[assets/figures/papers/paper_list_l2037_https_arxiv_org_abs_2512_09373/figures/006_Table_2.jpg]]
*Table 2: Comparisons on 3DMatch (60 scans) [80]*

![[assets/figures/papers/paper_list_l2037_https_arxiv_org_abs_2512_09373/figures/007_Table_3.jpg]]
*Table 3: Comparisons on ArkitScenes (200 scans) [6]*

![[assets/figures/papers/paper_list_l2037_https_arxiv_org_abs_2512_09373/figures/008_Table_4.jpg]]
*Table 4: Ablation Studies on ScanNet [18] (ScaN: ScanNet [18], ArkitS: ArkitScenes [6], ScaNP: ScanNet++ [75], 3DM: 3DMatch [80])*

![[assets/figures/papers/paper_list_l2037_https_arxiv_org_abs_2512_09373/figures/010_Table_5.jpg]]
*Table 5: Runtime (s) on 3DMatch [80] and ArKitScenes [6]*

![[assets/figures/papers/paper_list_l2037_https_arxiv_org_abs_2512_09373/figures/005_Figure_4.jpg]]

![[assets/figures/papers/paper_list_l2037_https_arxiv_org_abs_2512_09373/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative comparison: FUSER surpasses SOTA GeoTrans [57] and PARENet [74] descriptors with SGHR pose graph [67], achieving much higher accuracy and efficiency*



## 定位与知识库关联

### 1. 范式突破：从两阶段配对到前馈全局推理

传统多视角点云配准方法遵循一个固化的两阶段范式：首先对所有扫描对进行独立的成对配准（pairwise registration），再通过位姿同步（pose synchronization）将冗余的相对位姿估计融合为全局一致位姿。FUSER 首次打破这一范式，提出前馈式全局位姿直接回归，其核心差异体现在以下维度：

**注册范式**：基线方法如 **GeoTransformer**（Qin et al., CVPR 2022）与 **PARENet**（Yao et al., ECCV 2024）专注于提升单对扫描的配准精度，随后依赖 **SGHR**（Wang et al., CVPR 2023）等位姿图同步算法进行全局优化。**LMVR**（Yew and Lee, 3DV 2021）尝试联合优化成对与全局配准，但仍未摆脱成对估计的中间步骤。FUSER 则将所有扫描统一编码至紧凑隐空间，通过交替注意力直接输出每个扫描的全局刚性位姿，消除了成对匹配与位姿同步两个中间环节。

**多视图交互机制**：基线方法中各扫描对独立推理，缺乏跨扫描的全局几何约束，导致成对估计模糊与误差累积。FUSER 的几何交替注意力（Geometric Alternating Attention）通过 16 层内部扫描自注意与 16 层交叉扫描注意的交替堆叠，实现所有扫描间的同步消息传递，使全局几何约束贯穿整个推理过程。

**端到端对比**：**MDGD**（Li et al., IEEE RA-L, 2024）是基于图网络的端到端多视角配准方法，但其仍依赖图结构上的成对信息传递。在 ScanNet（30 scans）上，FUSER 将平均平移误差从 MDGD 的 0.37m 降至 0.15m，平均旋转误差从 17.4° 降至 6.7°，降幅分别约 59% 和 61%（Table 1），表明前馈全局推理范式在精度上的显著优势。

### 2. 关键技术组件的谱系定位

**绝对几何编码**：传统成对配准方法（如 KPConv 系列）通常采用平移不变的相对坐标归一化特征，以增强旋转鲁棒性。FUSER 反其道而行，采用基于 MinkowskiEngine 的稀疏 3D CNN 提取保留绝对坐标信息的超点特征。这一设计的关键洞察在于：全局位姿回归需要绝对平移线索，而平移不变编码会丢失此类信息。消融实验表明，去除绝对位置信息导致平移误差显著增加（Table 4 相关条目），验证了该设计选择的必要性。

**2D 注意力先验迁移**：FUSER 从 2D 重建基础模型 π³（VGGT 变体）迁移预训练权重至几何交替注意力层，实现跨模态注意力初始化。这是多视角 3D 配准领域首次将大规模 2D 基础模型的注意力先验迁移至 3D 点云推理。消融实验（Table 4）显示，该迁移带来显著的旋转和平移精度提升。这一技术路线的适用边界尚待验证：其效益可能受限于特定 2D 基础模型的选择，对 DINOv2、SAM 等其他 2D 模型的泛化性尚未得到广泛验证。

**SE(3)^N 扩散细化**：FUSER-DF 将多视角位姿修正建模为联合 SE(3)^N 流形上的先验条件扩散去噪过程。与传统扩散模型从纯噪声出发不同，FUSER-DF 以 FUSER 的预测位姿为先验起点，扩散过程从最优位姿向先验估计插值（Eq. 7），使去噪过程仅需小步精炼。这一设计与 **FeatSync**（Jin et al., CVPR 2024）等基于特征同步的细化方法形成互补——前者在位姿空间操作，后者在特征空间操作。

### 3. 适用边界与局限性

**计算资源门槛**：FUSER 模型参数量约 0.6B，训练需 8 块 NVIDIA L20 GPU，不利于资源有限的学术复现环境。尽管推理效率极高（3DMatch 上 0.31 秒），训练成本仍是推广的主要障碍。

**推理延迟权衡**：FUSER-DF 虽提升精度（ArkitScenes 上 RR 从 90.3% 升至 92.0%），但扩散去噪步骤使推理时间从 0.31 秒增至 2.91 秒（3DMatch，Table 5）。在低延迟场景下，基础版 FUSER 可能是更优选择。

**数据分布覆盖**：训练基于 ScanNet、ArkitScenes、3DMatch、ScanNet++ 等室内/小场景数据集，未见对大规模室外场景（如 KITTI、Waymo）的评估。绝对几何编码依赖稠密坐标提供平移线索，在极度稀疏或噪声大的真实扫描中鲁棒性可能下降，尽管 iPhone 扫描实验（Figure 7）显示了较好的泛化能力。

**序列长度限制**：当前方法处理固定长度的扫描序列，不支持任意数量扫描的在线增量式注册。训练时序列长度随机采样自 2 至 50，超出该范围的泛化能力未知。

### 4. 开放问题

1. **跨模态注意力桥接的通用性**：2D 注意力先验迁移目前仅针对特定 VGGT 变体（π³）验证，该技术能否形成通用的 3D-2D 注意力桥接框架，适用于更多类型的 2D 基础模型（如 DINOv2、SAM），是一个值得探索的方向。

2. **非刚性与动态场景扩展**：前馈架构目前假设刚性变换，能否扩展至非刚性或动态多视图配准场景，需要根本性的架构调整。

3. **多模态联合优化**：SE(3)^N 扩散细化框架能否联合优化其他传感器模态（如 RGB-D、LiDAR）的位姿，将单模态方法推广至多模态融合场景。

4. **轻量化与移动端部署**：当前 0.6B 参数量限制了边缘设备部署。探索知识蒸馏、架构剪枝等轻量化策略，使前馈全局配准能力下沉至移动端，具有实际应用价值。

5. **室外大规模场景验证**：在 KITTI、Waymo 等大规模室外自动驾驶场景上的性能与泛化能力尚待评估，这是从室内走向开放环境的关键一步。



## 原文 PDF

![[paperPDFs/CVPR_2026/FUSER_Feed_Forward_Multiview_3D_Registration_Transformer_and_SE_3_N_Diffusion_Refinement.pdf]]
