---
title: "HandX: Scaling Bimanual Motion and Interaction Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HandX_Scaling_Bimanual_Motion_and_Interaction_Generation.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_HandX_Scaling_Bimanual_Motion_and_Interaction_Generation_CVPR_2026_paper.html
project_link: https://handx-project.github.io
code_link: null
aliases:
- HandX
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过构建统一、大规模且带有多层级细粒度文本标注的 HandX 数据集，并建立标准化的评估基准（包括接触精度指标），从而为双手运动生成模型的训练和评价提供关键支撑。
primary_logic: 将结构化运动特征提取与大型语言模型推理解耦，可实现双手运动序列的可扩展细粒度自动标注；在此基础上，扩散模型和自回归模型在数据量和模型容量同时增加时，能持续提升文本对齐和接触精度，且 R-Precision 与计算量存在对数-线性缩放关系。
claims:
- Top‑3 R‑Precision 与 FLOPs 呈现严格的对数‑线性关系 (Rprec = 0.4391·log10(FLOPs) − 3.8707)，相关系数 0.96，表明文本‑运动对齐随计算量可预测地提升。
- 扩散模型中，同时增加训练数据量和 Transformer 解码器层数使 R‑Precision 和双手接触 F1 持续改善，12 层模型在 100% 数据上获得最佳接触性能 (C_F1 = 0.641)，但过度增大容量 (超大模型) 反而导致性能下降。
- 自回归模型中，单独增大 FSQ 码书尺寸不能可靠提升性能；只有联合增加模型容量和码书尺寸才能获得最佳 FID 和接触质量，证实二者需协同缩放。
- HandX text-to-motion 上 R-Precision vs FLOPs (scaling law) = Rprec = 0.4391 × log10(FLOPs) − 3.8707
---

# HandX: Scaling Bimanual Motion and Interaction Generation

> [!tip] 核心洞察
> 将结构化运动特征提取与大型语言模型推理解耦，可实现双手运动序列的可扩展细粒度自动标注；在此基础上，扩散模型和自回归模型在数据量和模型容量同时增加时，能持续提升文本对齐和接触精度，且 R-Precision 与计算量存在对数-线性缩放关系。

| 字段 | 内容 |
|------|------|
| 中文题名 | HandX: 大规模双手运动与交互生成 |
| 英文题名 | HandX: Scaling Bimanual Motion and Interaction Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_HandX_Scaling_Bimanual_Motion_and_Interaction_Generation_CVPR_2026_paper.html) · [Project](https://handx-project.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HandX |
| Dataset | HandX text-to-motion |

> [!tip] 效果简介
> - HandX text-to-motion 上，R-Precision vs FLOPs (scaling law) Rprec = 0.4391 × log10(FLOPs) − 3.8707 vs N/A (first demonstration) (r = 0.96 (log-linear correlation))。
> - HandX text-to-motion (Diffusion) 上，Intra-hand contact F1 (C_F1) 0.641 (12 layers, 100% data) vs 0.531 (4 layers, 100% data) or lower at smaller data (+0.110 over weaker model)。
> - HandX text-to-motion (Autoregressive) 上，FID 1.721 (215.31M params, codebook 4096) vs 3.050 (92.27M params, codebook 4096) (-1.329 improvement)。

## 概要

双手运动生成的核心瓶颈在于缺乏高质量、细粒度的双手交互数据与统一的评估协议，导致现有方法难以生成具有精细手指动作、接触时序和双手协调的真实运动。**HandX** 针对这一问题，构建了一个大规模、多层级细粒度文本标注的双手运动数据集（54.2 小时，5.9M 帧，485.7K 条标注），并建立了标准化评估基准。

论文的核心洞察是：将结构化运动特征提取与大型语言模型推理解耦，可实现双手运动序列的可扩展细粒度自动标注。在此数据基础上，扩散模型和自回归模型在数据量和模型容量同时增加时，能持续提升文本对齐和接触精度。实验揭示了明确的缩放规律——**Top-3 R-Precision 与 FLOPs 呈现严格的对数-线性关系**（$\text{Rprec} = 0.4391 \times \log_{10}(\text{FLOPs}) - 3.8707$，相关系数 0.96），表明文本-运动对齐随计算量可预测地提升。

在方法谱系上，HandX 立足于数据驱动的手部运动生成，通过整合多源开源数据并采集高保真光学动作捕捉数据，弥补了现有数据集在双手交互细节上的不足。其自动标注框架将运动学特征提取与 LLM 语义推理分离，为大规模运动-文本配对提供了可扩展方案。在生成模型层面，论文分别基准化了扩散模型与自回归模型两种范式：扩散模型通过独立编码左手、右手和交互文本提示并残差融合，解决了左右手动作混淆问题；自回归模型则采用局部运动表示与有限标量量化（FSQ），提高了码本利用率和重建质量。

主要实验结果包括：扩散模型在 12 层解码器与全量数据下获得最佳双手接触性能（Intra-hand $C_{F1}=0.641$）；自回归模型在模型容量与码书尺寸协同缩放时取得最优 FID（1.721）。消融实验进一步表明，单独扩大模型容量或码书尺寸而不匹配数据规模，会导致性能饱和甚至下降，揭示了缩放过程中的协同依赖关系。

本工作的局限性在于：自动标注依赖 LLM 语义理解能力，可能无法完全捕捉极细腻的手指接触语义；数据集虽扩展了双手交互覆盖，但仍限于日常室内活动，对极端姿态或专业技能的泛化性未经验证。开放问题包括如何将手部运动生成无缝扩展至全身运动、缩放规律在更大规模下是否持续有效，以及多模态条件融合的可能性。



双手灵巧运动生成是具身智能与数字人领域的核心难题。从机器人遥操作、虚拟角色动画到人机交互，系统需要理解并合成高度协调的双手动作——不仅包含腕部轨迹，更涉及每根手指的精细姿态、指尖接触的精确时序以及左右手的空间协调关系。然而，现有方法在这一目标上仍面临根本性瓶颈。

**核心瓶颈在于数据与评估的双重缺失。** 一方面，主流手部运动数据集（如 InterHand2.6M、GigaHands）要么缺乏双手交互场景，要么仅提供粗糙的动作类别标签，缺少对接触事件、手指弯曲度、左右手协调关系的细粒度语言描述。另一方面，领域缺乏统一的评估协议，尤其是针对双手接触精度的标准化指标，导致不同方法难以公平比较，生成质量的可信度量长期缺位。

从生成范式来看，现有工作大多采用简单的文本条件编码策略——将左手、右手和交互文本直接拼接输入模型。这种做法容易导致左右手动作混淆，模型难以区分“左手握杯、右手拧盖”与“右手握杯、左手拧盖”的语义差异。在运动表示层面，全局坐标表示对双手相对运动的刻画能力有限，限制了生成动作的协调性和物理合理性。

**HandX 的动机正是填补这一系统性缺口。** 该工作认识到，突破双手运动生成瓶颈需要三个关键要素的协同：大规模、高质量且带有细粒度文本标注的双手交互数据；标准化、可复现的评估基准；以及能够充分利用数据规模和模型容量的生成架构。为此，HandX 构建了统一的数据集与基准平台，整合多源开源数据并采集高保真光学动作捕捉数据，同时提出解耦的运动特征提取与大型语言模型推理相结合的自动标注策略，为双手运动生成模型的训练和评价提供了关键支撑。



## 核心方法与创新机理

HandX 的核心创新并非提出一个全新的模型架构，而是系统性地解决了双手运动生成中长期存在的**数据瓶颈**与**评估缺失**问题，并在此基础上揭示了**可预测的缩放规律**。其创新点可归纳为三个紧密耦合的“changed slots”。

### 1. 数据与标注：从粗糙动作标签到多层级细粒度语义

现有手部运动数据集（如 InterHand2.6M、GigaHands 等）的核心缺陷在于：要么仅提供粗粒度的动作类别标签，要么缺乏对双手交互细节（如手指接触时序、协调模式）的描述。这导致生成模型难以学习精细的手指动作与接触语义。

HandX 对此进行了根本性重构：
- **数据整合与采集**：清洗、对齐并过滤了 ARCTIC、H2O、HOT3D、GigaHands 等多个开源数据集，同时使用 36 相机 OptiTrack 系统采集了高保真双手交互动作，最终构建了包含 **54.2 小时、5.9M 帧** 的统一数据集（Table 1）。
- **解耦式自动标注**：提出“运动特征提取 + LLM 推理”的两阶段策略。首先从原始运动序列中计算手指弯曲度、指掌距离等运动学描述子，分割为结构化事件并存储为 JSON 格式；然后将 JSON 输入大型语言模型，生成涵盖左手、右手及双手关系的**多层级（简略 / 平衡 / 详细）细粒度文本描述**，总计 **485.7K 条标注**（Sec. 4）。这种解耦设计将结构化运动理解与语言生成分离，实现了可扩展的自动标注。

### 2. 扩散模型：解耦文本编码与残差交叉注意力融合

在文本条件编码上，基线方法通常简单拼接左手、右手和交互文本提示，容易导致左右手动作混淆。HandX 的扩散模型（Figure 2a）对此进行了针对性改进：
- **独立编码与融合**：分别编码左手、右手和交互三类文本提示，并引入可学习的 CLS 令牌。在去噪过程中，通过**残差交叉注意力**将三类文本嵌入与噪声运动特征融合：

$$
\tilde{\pmb{z}} = \pmb{z}_t' + \sum_{k \in \{L, R, I\}} \text{CrossAttention}(\pmb{z}_t', \mathfrak{T}_k)
$$

这种设计迫使模型明确区分左右手与交互关系，从机制上缓解了动作混淆问题（Sec. 5.1）。

### 3. 自回归模型：局部运动表示与有限标量量化

自回归模型方面，HandX 放弃了全局坐标表示，转而采用**局部运动表示**（Figure 2b）：

$$
\pmb{x}^i = [\pmb{d}_r^i; \pmb{v}_r^i; \pmb{\theta}_r^i; \pmb{p}_l^i; \pmb{v}_l^i; \pmb{s}^i]
$$

每帧包含相对腕部向量、腕部速度、腕部朝向、局部关节位置与速度及旋转标量。配合**有限标量量化 (FSQ)** 提高码本利用率和重建质量，相比传统 VQ 方法在离散化表示上表现出更好的缩放行为（Sec. 5.2）。

### 4. 缩放规律的发现：计算量可预测地提升文本-运动对齐

HandX 最具洞察力的发现是**文本-运动对齐与计算量之间存在严格的对数-线性关系**（Figure 4）：

$$
\text{Rprec} = 0.4391 \times \log_{10}(\text{FLOPs}) - 3.8707
$$

相关系数高达 **0.96**，表明 R-Precision 随 FLOPs 可预测地提升。消融实验进一步揭示了缩放的两个关键条件：
- **数据与模型需协同缩放**：同时增大训练数据量和 Transformer 解码器层数，R-Precision 和双手接触 F1 持续改善；12 层模型在 100% 数据上获得最佳接触性能（C_F1 = 0.641），但过度增大容量（约 6.7× 参数量）反而导致性能下降（Table 2）。
- **码书与模型容量需匹配**：自回归模型中，单独扩大 FSQ 码书尺寸不能可靠提升性能；只有联合增加模型容量和码书尺寸才能获得最佳 FID（1.721）和接触质量（Table 3）。

这些发现为未来双手运动生成模型的资源分配提供了明确的指导原则。



HandX 围绕一个核心瓶颈展开：现有双手运动生成缺乏高质量、细粒度的交互数据与统一的评估协议，导致模型难以捕捉精细手指动作、接触时序和双手协调。为此，HandX 构建了一条从数据到生成再到评估的完整流水线，其因果调节点在于**大规模、多层级细粒度标注的 HandX 数据集**与**标准化的评估基准**。

### 数据与标注流水线

数据侧分为整合与采集两个阶段。首先，清洗、对齐并过滤多源开源双手运动数据（ARCTIC、H2O、HOT3D、GigaHands 等），统一到规范化的骨骼表示与坐标系下；其次，使用 36 相机 OptiTrack 光学动作捕捉系统采集高保真双手交互动作，每位演员佩戴 25 个手部反射标记点以捕捉腕、掌、指及指尖的精细运动（Figure A）。所有序列经分割后，通过基于关节角速度的强度感知滤波器去除静态或近静态片段，最终形成 54.2 小时、590 万帧的数据集。

标注侧采用**解耦的两阶段自动标注策略**，这是 HandX 实现可扩展细粒度标注的核心机制。第一阶段，从原始手部运动序列中提取结构化运动学特征——包括手指弯曲度、指掌距离、接触事件等描述子，并组织为 JSON 格式的运动事件结构（Figure C）。第二阶段，将 JSON 特征输入大型语言模型（LLM），由 LLM 进行语义推理，生成分层次（简略/平衡/详细）的文本描述，分别刻画左手、右手及双手交互关系，最终产生 485.7K 条细粒度文本标注。这种“结构化运动特征提取 + LLM 推理”的分离设计，使语义标注的扩展不再受限于人工标注成本。

### 生成流水线

HandX 在统一的数据基础上构建了两种生成范式，形成互补的基准框架（Figure 2）。

**扩散模型**（Section 5.1）将双手运动序列表示为 $\pmb{p} = \{ p^1, p^2, \dots, p^F \}$，每帧 $p^i \in \mathbb{R}^{2J \times 3}$ 包含双手所有关节的三维坐标。每帧运动进一步表示为 $\pmb{x}^i = [\pmb{p}^i; \pmb{s}^i] \in \mathbb{R}^{2\mathcal{J} \times 4}$，即关节坐标与紧凑旋转标量的拼接。文本提示被分解为左手、右手和交互三部分 $T = \{ T_L, T_R, T_I \}$，分别通过独立的文本交叉注意力与噪声运动嵌入交互，再经残差连接融合：

$$\tilde{\pmb{z}} = \pmb{z}_t' + \sum_{k \in \{L, R, I\}} \text{CrossAttention}(\pmb{z}_t', \mathfrak{T}_k).$$

这种分别编码、残差融合的设计明确区分了左右手动作与交互关系，避免了简单拼接导致的左右手动作混淆。训练遵循 DDPM 框架，前向加噪过程为 $\pmb{x}_t = \sqrt{\bar{\alpha}_t} \pmb{x}_0 + \sqrt{1 - \bar{\alpha}_t} \pmb{\epsilon}$，其中 $\bar{\alpha}_t = \prod_{t'=1}^{t} (1 - \beta_{t'})$。推理时，扩散模型支持局部去噪策略，可实现运动补全、关键帧引导、腕部轨迹控制等多种条件生成（Figure 3）。

**自回归模型**（Section 5.2）采用局部运动表示以避免全局坐标的累积误差，每帧表示为：

$$\pmb{x}^i = [\pmb{d}_r^i; \pmb{v}_r^i; \pmb{\theta}_r^i; \pmb{p}_l^i; \pmb{v}_l^i; \pmb{s}^i],$$

包含相对腕部向量、腕部速度、腕部朝向、局部关节位置与速度及旋转标量。运动序列经有限标量量化（FSQ）离散化为 token：

$$\hat{\pmb{y}} = \text{round}(\sigma(\pmb{y}) \cdot (L - 1)),$$

再结合文本前缀的 Transformer 进行逐 token 预测，训练目标为最小化运动 token 的负对数似然：$-\sum_{k=1}^{n} \log p(\hat{\pmb{y}}^k \mid \pmb{y}^{<k}, \mathfrak{T})$。FSQ 相比传统 VQ 提供了更好的码本利用率和重建质量，重建损失为 $\mathcal{L} = \lVert \pmb{x} - \mathcal{D}(\hat{\pmb{y}}) \rVert_2^2$。

### 输入输出流

整体框架的输入为包含左手、右手和交互关系的三部分文本提示 $T = \{ T_L, T_R, T_I \}$，输出为双手运动序列 $\pmb{p}$。扩散模型通过迭代去噪从纯噪声生成运动，自回归模型则逐 token 自回归预测。两种模型均支持额外的时空条件输入（如关键帧位姿、腕部轨迹），通过推理时的约束融合实现可控生成。

### 关键证据

该框架的有效性由以下决定性证据支撑：
- 扩散模型中，同时增加训练数据量和 Transformer 解码器层数使 R-Precision 和双手接触 F1 持续改善，12 层模型在 100% 数据上获得最佳接触性能（C_F1 = 0.641），证实数据和模型容量需协同缩放（Table 2）。
- 自回归模型中，单独扩大 FSQ 码书尺寸不能可靠提升性能；只有联合增加模型容量和码书尺寸才能获得最佳 FID（1.721）和接触质量，表明表示容量与模型容量需匹配增长（Table 3）。
- Top-3 R-Precision 与 FLOPs 呈现严格的对数-线性关系 $\text{Rprec} = 0.4391 \times \log_{10}(\text{FLOPs}) - 3.8707$，相关系数 0.96，表明文本-运动对齐随计算量可预测地提升（Figure 4）。

这些证据共同表明：HandX 通过数据、模型与表示三者的协同缩放，为双手运动生成建立了可预测的改进路径。

### 补充图表

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_HandX_Scaling_Bi/figures/001_Figure_1.jpg]]
*Figure 1: (a) We introduce HandX, a large-scale dataset of bimanual and dexterous motions paired with fine-grained textual descriptions. The examples highlight the high-fidelity captures produced by our motion capture system (Figure A), and demonstrate instantiation on a real-world humanoid with dexterous hands. (b) We benchmark two generative paradigms: diffusion-based and autoregressive (AR) models. (c) Our models support flexible conditioning and synthesize highly dynamic, expressive hand motions. (d) We observe clear scaling trends: increasing dataset size and model capacity yields substantial performance gains*



### 问题形式化

双手运动生成任务的目标是从文本描述 $T$ 生成包含 $F$ 帧的双手运动序列 $\pmb{p} = \{ p^1, p^2, \dots, p^F \}$，其中每帧 $p^i \in \mathbb{R}^{2J \times 3}$ 表示双手所有关节的三维坐标。文本提示被分解为三部分：

$$T = \{ T_L, T_R, T_I \}$$

分别对应左手描述、右手描述和双手交互描述。这一解耦设计是后续扩散模型中独立交叉注意力融合的基础。

---

### 扩散生成模型

扩散模型采用 DDPM 框架，将运动生成建模为迭代去噪过程。每帧运动表示 $\pmb{x}^i$ 由关节坐标与紧凑旋转标量拼接而成：

$$\pmb{x}^i = [\pmb{p}^i; \pmb{s}^i] \in \mathbb{R}^{2\mathcal{J} \times 4}$$

前向扩散过程逐步向干净信号 $\pmb{x}_0$ 注入高斯噪声：

$$\pmb{x}_t = \sqrt{\bar{\alpha}_t} \pmb{x}_0 + \sqrt{1 - \bar{\alpha}_t} \pmb{\epsilon}$$

其中累积保留信号系数 $\bar{\alpha}_t = \prod_{t'=1}^{t} (1 - \beta_{t'})$，$\beta_{t'}$ 为噪声调度参数。

**文本条件融合**是该方法的关键设计。与简单拼接三类文本提示不同，HandX 分别对左手、右手和交互文本进行独立编码，并通过残差交叉注意力与运动特征融合：

$$\tilde{\pmb{z}} = \pmb{z}_t' + \sum_{k \in \{L, R, I\}} \text{CrossAttention}(\pmb{z}_t', \mathfrak{T}_k)$$

其中 $\pmb{z}_t'$ 为当前时刻的运动嵌入，$\mathfrak{T}_k$ 为对应文本嵌入。该设计使模型明确区分左右手动作和交互关系，避免了基线方法中左右手动作混淆的问题（Figure 2(a), Sec. 5.1）。

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_HandX_Scaling_Bi/figures/004_Figure_2.jpg]]
*Figure 2: Two benchmark models. (a) Diffusion model. Text embeddings for the left hand, right hand, and bimanual interaction are separately cross-attended with noisy motion embeddings, and then fused through residual connections to predict denoised motion embeddings. (b) Autoregressive model, consisting of Finite Scalar Quantization (FSQ) and a text-prefix autoregressive model. Unlike the diffusion model, it concatenates the left-hand, righthand, and bimanual text descriptions with separator tokens to form a text prefix, and formulates bimanual motion generation as a token prediction task over motion tokenized by FSQ*

---

### 自回归生成模型

自回归模型采用局部运动表示替代全局坐标，每帧表示 $\pmb{x}^i$ 包含六个分量：

$$\pmb{x}^i = [\pmb{d}_r^i; \pmb{v}_r^i; \pmb{\theta}_r^i; \pmb{p}_l^i; \pmb{v}_l^i; \pmb{s}^i]$$

分别为相对腕部向量 $\pmb{d}_r^i$、腕部速度 $\pmb{v}_r^i$、腕部朝向 $\pmb{\theta}_r^i$、局部关节位置 $\pmb{p}_l^i$、局部关节速度 $\pmb{v}_l^i$ 和旋转标量 $\pmb{s}^i$。该局部表示有助于模型学习运动不变性。

**有限标量量化 (FSQ)** 将连续潜在向量 $\pmb{y}$ 离散化为 $L$ 级整数：

$$\hat{\pmb{y}} = \text{round}(\sigma(\pmb{y}) \cdot (L - 1))$$

其中 $\sigma(\cdot)$ 为 sigmoid 函数。相比于传统 VQ，FSQ 提供更好的码书利用率和重建质量。Tokenizer 通过最小化重建损失训练：

$$\mathcal{L} = \lVert \pmb{x} - \mathcal{D}(\hat{\pmb{y}}) \rVert_2^2$$

自回归 Transformer 以文本前缀 $\mathfrak{T}$ 为条件，逐 token 预测运动序列，训练目标为负对数似然：

$$-\sum_{k=1}^{n} \log p(\hat{\pmb{y}}^k \mid \pmb{y}^{<k}, \mathfrak{T})$$

（Figure 2(b), Sec. 5.2）

---

### 缩放规律

实验揭示了文本-运动对齐的缩放规律。R-Precision 与计算量 FLOPs 呈现严格的对数-线性关系：

$$\text{Rprec} = 0.4391 \times \log_{10}(\text{FLOPs}) - 3.8707$$

相关系数高达 0.96（Figure 4），表明文本-运动对齐随计算量可预测地提升。这是双手运动生成领域首次观测到的缩放定律。

---

### 推理时条件生成

扩散模型支持推理时的局部去噪策略：在每一步去噪时，将已知约束条件（如关键帧姿态、腕部轨迹）与当前采样结果混合，实现运动补全、关键帧引导生成、长序列扩展等多种条件生成任务，无需额外训练（Figure 3, Sec. 5.1）。



## 实验与关键发现

### 核心瓶颈与评估基准

双手运动生成的核心瓶颈在于缺乏高质量、细粒度的双手交互数据以及统一的评估协议。HandX 通过构建大规模数据集并建立标准化评估基准来解决这一问题。评估采用以下关键指标：

- **R-Precision**：衡量生成运动与文本描述的对齐程度，采用 Top‑3 匹配准确率。
- **Intra‑hand Contact F₁ (C_F₁)** 与 **Inter‑hand Contact F₁**：评估双手内部及双手之间的接触精度。接触标签直接从真实交互标注中提取，接触阈值设为 2 cm。
- **FID (Fréchet Inception Distance)**：衡量生成运动与真实运动分布的距离。

### 缩放规律：R‑Precision 与计算量的对数‑线性关系

HandX 揭示了文本‑运动对齐随计算量可预测提升的缩放规律。如 **Figure 4** 所示，Top‑3 R‑Precision 与 FLOPs 呈现严格的对数‑线性关系：

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_HandX_Scaling_Bi/figures/006_Figure_4.jpg]]
*Figure 4: Scaling trend of computational scale. We observe a clear log-linear relationship between R-precision and FLOPS, with a high correlation coefficient of 0.96. R-Precision is evaluated with a batch size of 16*

$$\text{Rprec} = 0.4391 \times \log_{10}(\text{FLOPs}) - 3.8707$$

该关系的相关系数高达 **0.96**，表明在 HandX 基准上，文本‑运动对齐性能可以通过增加计算量实现可预测的提升。这一发现为后续模型缩放提供了量化指导。

### 扩散模型消融：数据量与模型容量的协同缩放

**Table 2** 展示了扩散模型在数据量和模型深度两个维度上的消融结果。核心发现如下：

1. **数据量与模型深度协同增长带来一致改善**：同时增加训练数据量（5% → 20% → 100%）和 Transformer 解码器层数（4 → 8 → 12），R‑Precision 和双手接触 F₁ 持续提升。
2. **最佳接触性能**：12 层模型在全量数据上获得最优接触性能，Intra‑hand C_F₁ 达到 **0.641**，相较 4 层模型的 0.531 提升 **+0.110**。
3. **容量饱和与性能下降**：过度增大模型容量（16 层解码器，参数量约为 12 层模型的 6.7 倍）反而导致性能下降。这表明缩放存在饱和点，单纯增加模型容量而不匹配数据规模会导致过拟合或优化困难。

**定性验证**：Figure 5 和 Figure 6 分别从数据规模和模型规模两个维度提供了定性对比。全量数据训练的模型生成的运动更具表现力且文本对齐更好；更大模型生成的运动在双手接触和文本对齐方面均有明显改善。

### 自回归模型消融：模型容量与码书尺寸的匹配缩放

**Table 3** 展示了自回归模型在 FSQ 码书尺寸和模型容量两个维度上的消融结果。核心发现：

1. **单独扩码书不可靠**：仅增大 FSQ 码书尺寸（如从 1024 增至 4096）而保持模型容量不变时，性能不能可靠提升，甚至可能下降。
2. **协同缩放获得最优性能**：当模型容量（从 92.27M 增至 215.31M 参数）与码书尺寸（从 1024 增至 4096）匹配增长时，FID 从 3.050 降至 **1.721**（改善 **‑1.329**），接触指标也显著提升。
3. **缩放失配导致退化**：大码书配小模型或小码书配大模型均无法获得最佳性能，证实模型容量与表示离散化粒度需协同缩放。

### 条件生成能力

除文本到运动生成外，HandX 框架支持推理时局部去噪策略，实现多种条件生成任务（**Figure 3**）：

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_HandX_Scaling_Bi/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative results of our unified framework, showing (a) high-fidelity text-to-motion generation with fine-grained articulation and contact, and (b) bimanual motion synthesis given versatile spatiotemporal conditions. Gray hands denote the input condition, green hands denote the generation, and orange hands denote the extended long-horizon generation*

- **运动补全 (Motion In‑betweening)**：固定起始和结束姿态，生成中间过渡。
- **关键帧引导生成**：基于稀疏关键帧约束生成完整运动序列。
- **腕部轨迹控制**：给定腕部运动轨迹，生成相应的双手手指动作。
- **长时域扩展**：通过迭代扩展生成超长运动序列。

### 失败模式与局限性

1. **容量饱和**：扩散模型中，16 层超大模型性能下降（Table 2），表明单纯增加模型容量存在收益递减。
2. **码书单独缩放失效**：自回归模型中，仅扩大 FSQ 码书尺寸无法可靠提升性能（Table 3），需与模型容量协同缩放。
3. **自动标注的语义边界**：LLM 驱动的自动标注虽能生成多层级细粒度描述，但可能无法完全捕捉极其细腻的手指接触语义，极端情况仍需人工校验。
4. **领域覆盖局限**：数据集虽通过整合和采集扩展了双手交互覆盖，但仍限于日常室内活动，对极端姿态或专业手部技能的泛化性未经验证。

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_HandX_Scaling_Bi/figures/008_Table_2.jpg]]
*Table 2: Ablation study on model size and data size. For R-precision, we adopt a batch size of 32. We observe clear scaling trends for our primary metrics, e.g., R-Precision improves consistently as we scale both data and model sizes, while Intra-hand*

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_HandX_Scaling_Bi/figures/009_Table_3.jpg]]
*Table 3: Ablation study on the codebook size of FSQ and the model size of autoregressive models. For R-precision, we adopt a batch size of 32. Both the FSQ and autoregressive models are trained on the full training dataset. The primary metrics*

### 补充图表

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_HandX_Scaling_Bi/figures/002_Table_1.jpg]]
*Table 1: Comparison of major hand motion datasets. Left: Dataset scale. Values are reported as HQ (Raw) where*

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_HandX_Scaling_Bi/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison of diffusion models trained with different data scales. The model trained on the full dataset generates more expressive motion with better text alignment*



## 定位与知识库关联

### 1. 问题定位与核心贡献边界

HandX 聚焦于**双手运动与交互生成**，其核心瓶颈在于现有方法和数据集缺乏高质量、细粒度的双手交互数据以及统一的评估协议，导致难以生成具有精细手指动作、接触时序和双手协调的真实运动。论文的因果调节变量是通过构建统一、大规模且带有多层级细粒度文本标注的 HandX 数据集，并建立标准化的评估基准（包括接触精度指标），从而为双手运动生成模型的训练和评价提供关键支撑。

在方法谱系上，HandX 并非提出全新的生成范式，而是在现有扩散模型（DDPM）和自回归模型（Autoregressive Transformer）两条主流生成路径上，通过**数据基础设施**和**评估协议**的系统性升级来推动性能边界。其核心贡献可拆解为三个层面：

1. **数据层**：构建 HandX 数据集（54.2 小时、5.9M 帧、485.7K 条多层级文本标注），整合多个开源数据（ARCTIC、H2O、HOT3D、GigaHands 等）并采集高质量光学动作捕捉数据。
2. **标注层**：提出解耦的运动特征提取 + LLM 推理的自动标注策略，将结构化运动学描述子（手指弯曲度、指掌距离等）转换为 JSON 格式后交由 LLM 生成细粒度文本描述。
3. **模型与评估层**：在扩散和自回归两种范式上建立基准，引入接触精度指标（Intra-hand Contact F1），并首次在双手运动生成领域观察到文本-运动对齐的缩放规律。

### 2. 与现有工作的关系

#### 2.1 数据集层面的超越

Table 1 的系统对比表明，现有手部运动数据集（如 InterHand2.6M、GigaHands 等）要么缺乏双手交互细节，要么仅有粗糙的动作标签或简短描述。HandX 在数据规模（54.2h vs. 典型数据集的数小时级别）、标注粒度（多层级细粒度文本 vs. 动作类别标签）和运动质量（接触丰富度、动态性）三个维度上实现了全面超越。

值得注意的差异化设计是**强度感知过滤**：基于关节角速度去除静态或近静态片段，避免生成模型"冻结"在静止姿态上。这一设计直接回应了现有数据集中静态片段占比过高导致生成多样性不足的问题。

#### 2.2 模型架构的增量改进

在扩散模型分支，HandX 的关键改进在于**文本条件的解耦编码与残差融合**。基线做法通常将左手、右手和交互文本简单拼接，易导致左右手动作混淆。HandX 分别编码三类提示并添加可学习的 CLS 令牌，通过残差交叉注意力融合（Figure 2a），使模型明确区分左右手和交互关系。这一设计本质上是多模态条件融合策略的精细化，而非架构范式的根本改变。

在自回归模型分支，HandX 采用**局部运动表示**替代全局坐标表示，并结合有限标量量化（FSQ）提高码本利用率。局部表示包含相对腕部向量、腕部速度、腕部朝向、局部关节位置与速度及旋转标量，这一选择与近期全身运动生成中局部表示优于全局表示的趋势一致。

#### 2.3 评估协议的建立

HandX 的另一个重要贡献是建立了标准化的双手运动生成评估基准。除常规的 FID 和 R-Precision 外，引入基于真实交互标注的接触精度指标（Contact F1），接触阈值经验性设为 2 cm。这一指标直接衡量生成运动在物理交互层面的真实性，弥补了现有评估体系对接触质量关注不足的缺陷。

### 3. 缩放规律的发现及其边界

HandX 最关键的发现是**文本-运动对齐与计算量之间的对数-线性缩放关系**：

$$\text{Rprec} = 0.4391 \times \log_{10}(\text{FLOPs}) - 3.8707$$

相关系数 0.96（Figure 4），表明 R-Precision 随计算量可预测地提升。这一发现为双手运动生成的资源投入提供了量化指导，但其适用边界需要审慎评估：

- **数据量与模型容量的协同**：Table 2 的消融实验表明，单独增加数据量或模型深度均可提升性能，但过度增大模型容量（约 6.7× 参数量）反而导致性能下降。12 层 Transformer 解码器在 100% 数据上获得最佳接触性能（C_F1 = 0.641），而 16 层超大模型出现退化，表明缩放存在饱和点。
- **码书与模型的协同缩放**：Table 3 显示，在自回归模型中单独扩大 FSQ 码书尺寸不能可靠提升性能；只有联合增加模型容量和码书尺寸才能获得最佳 FID（1.721）和接触质量。这证实了两者需协同缩放，单一维度的扩展可能适得其反。

这些发现暗示，HandX 观察到的缩放规律在当前实验范围内成立，但外推到更大规模（如百亿参数、数千小时数据）时是否持续有效仍是开放问题。

### 4. 方法的适用边界与局限

#### 4.1 数据覆盖的局限

尽管 HandX 通过整合和采集扩展了双手交互覆盖，但数据仍限于日常室内活动。对极端姿态、专业手部技能（如乐器演奏、手术操作）或高动态体育动作的泛化性未经验证。数据集的地理和文化多样性也未见讨论。

#### 4.2 自动标注的语义天花板

自动标注框架依赖于 LLM 对结构化运动特征的语义理解能力。虽然解耦设计（运动特征提取 + LLM 推理）提升了可扩展性，但 LLM 可能无法完全捕捉极其细腻的手指接触语义（如"食指指尖轻触拇指指腹"与"食指指腹按压拇指指尖"的微妙差异）。论文未报告自动标注的人工校验率或错误率，这一点的实际可靠性需要进一步验证。

#### 4.3 单模态条件的限制

当前 HandX 仅支持文本条件生成。在真实应用中，语音指令、物体形状、环境上下文等多模态条件可能更为自然。论文将此列为开放问题，但未提供初步探索。

#### 4.4 全身扩展的挑战

论文提出了"如何将手部运动生成无缝扩展至全身运动"的开放问题。这一扩展面临的核心挑战在于：手部动作与肢体动作在时空尺度上差异显著（手指关节的精细运动 vs. 躯干的宏观运动），且两者的协调关系（如抓取物体时的手-臂协同）需要额外的物理约束建模。

### 5. 在知识库中的定位

HandX 在双手运动生成领域的知识库中占据**基础设施层**的位置。其核心价值不在于提出全新的算法范式，而在于：

1. **数据基准的建立**：为后续研究提供大规模、高质量、细粒度标注的训练和评估平台。
2. **缩放规律的揭示**：为资源分配和模型设计提供可量化的指导原则。
3. **评估协议的标准化**：特别是接触精度指标的引入，推动领域从"看起来像"向"物理上正确"的评估范式转变。

后续研究可能沿着以下方向展开：（a）在 HandX 基准上探索更高效的模型架构以突破当前缩放饱和点；（b）将 HandX 的自动标注策略迁移至全身运动或物体交互场景；（c）融合多模态条件以提升生成的可控性和真实感；（d）验证缩放规律在更大规模下的持续性和潜在的结构性转变。



## 原文 PDF

![[paperPDFs/CVPR_2026/HandX_Scaling_Bimanual_Motion_and_Interaction_Generation.pdf]]
