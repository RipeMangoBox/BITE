---
title: "DextER: Language-driven Dexterous Grasp Generation with Embodied Reasoning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DextER_Language_driven_Dexterous_Grasp_Generation_with_Embodied_Reasoning.pdf
project_link: "https://junha-l.github.io/dexter"
code_link: null
aliases:
- DextER
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 基于接触预测的具身体验推理（embodied contact reasoning）
primary_logic: 预测哪些手指链接与物体表面在何处接触，提供了一种具身感知的中间表示，将高级任务语义与机器人本体和物体的物理约束相桥接，从而显著提高抓取生成的质量和意图对齐。
claims:
- 去除接触推理导致意图对齐 P-FID 从 0.20 恶化到 0.30（增加50%），成功率从 67.14% 降至 62.37%，证明接触推理是提高意图对齐和物理质量的关键因素。
- 与先前最佳模型 DexGYSNet 相比，DextER 在 DexGYS 基准上实现了 96.4% 的意图对齐改进和 3.83 个百分点的成功率提升。
- DexGYS validation set 上 Success Rate (%) = 67.14
- DexGYS validation set 上 P-FID (intention alignment) = 0.20
---

# DextER: Language-driven Dexterous Grasp Generation with Embodied Reasoning

> [!tip] 核心洞察
> 预测哪些手指链接与物体表面在何处接触，提供了一种具身感知的中间表示，将高级任务语义与机器人本体和物体的物理约束相桥接，从而显著提高抓取生成的质量和意图对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | DextER：基于具身推理的语言驱动灵巧抓取生成 |
| 英文题名 | DextER: Language-driven Dexterous Grasp Generation with Embodied Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.16046) · [Project](https://junha-l.github.io/dexter) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DextER |
| Dataset | DexGYS validation set |

> [!tip] 效果简介
> - DexGYS validation set 上，Success Rate (%) 67.14 vs 63.31 (DexGYSNet) (+3.83 p.p.)；P-FID (intention alignment) 0.20 vs 5.60 (DexGYSNet) (-96.4% improvement)。

## 概述

语言驱动的灵巧抓取生成要求模型根据自然语言指令，为多指灵巧手生成符合任务语义且物理可行的抓取姿态。现有方法（如 **GraspCVAE**、**DexGYSNet** 等）直接将视觉和语言输入映射到抓取参数，缺乏对多指手与物体之间物理交互接触的显式推理，导致抓取与任务意图的对齐性差以及物理稳定性有限。

本文提出 **DextER**，核心洞察在于：**预测哪些手指链接与物体表面在何处接触**，作为一种具身感知的中间表示，将高级任务语义与机器人本体和物体的物理约束相桥接。方法将抓取生成分解为两步推理过程——先预测接触模式 $\mathcal{C}$，再基于接触生成完整抓取配置 $\mathbf{a}$：

$$p ( \mathbf { a } , { \mathcal { C } } | \mathbf { P } , \mathbf { T } ) = p ( { \mathcal { C } } | \mathbf { P } , \mathbf { T } ) \cdot p ( \mathbf { a } | { \mathcal { C } } , \mathbf { P } , \mathbf { T } )$$

在 DexGYS 基准上，DextER 实现了 **67.14%** 的抓取成功率，较先前最佳方法 DexGYSNet（63.31%）提升 **3.83 个百分点**；意图对齐指标 P-FID 从 5.60 降至 **0.20**（提升 96.4%）。消融实验表明，移除接触推理后 P-FID 恶化至 0.30（+50%），成功率降至 62.37%，验证了接触推理是性能提升的关键因素。该方法同时支持可操控生成，用户可通过指定部分接触约束来引导抓取合成。

## 背景与动机

### 1. 问题背景：语言驱动的灵巧抓取

语言驱动的灵巧抓取（language-driven dexterous grasp generation）要求机器人根据自然语言指令，为多指灵巧手生成抓取配置，使其既能满足任务语义（如“握住茶杯把手倒水”），又能在物理上稳定执行。随着大语言模型（LLM）与视觉模型的快速融合，该任务已成为具身智能领域的重要前沿问题。

### 2. 现有方法的瓶颈：缺乏具身接触推理

当前主流方法——包括 **GraspCVAE**、**GraspTTA**、**SceneDiffusers**、**DGTR** 以及最新的 **DexGYSNet**——普遍采用“端到端映射”范式：将视觉输入（点云）和语言指令直接映射到抓取参数空间。这一范式存在一个核心瓶颈：**模型缺乏对多指手与物体之间物理交互接触的显式推理**。

具体而言，灵巧抓取的本质是手与物体的物理接触——哪些手指的哪些链接（finger links）在物体的哪些位置发生接触，直接决定了抓取的语义合理性与力学稳定性。然而，现有方法跳过了这一关键中间环节，导致两个突出问题：

1. **意图对齐性差**：模型难以将高层任务语义（如“捏住旋钮旋转”）精确映射到手指级别的接触模式，生成的抓取与指令意图之间存在语义偏差。
2. **物理稳定性有限**：由于缺乏对接触几何的显式建模，生成的抓取配置在物理仿真中容易出现穿透、滑脱或力封闭不满足等问题。

### 3. 本文动机：以接触推理桥接语义与物理

针对上述瓶颈，DextER 提出了一种基于**具身接触推理（embodied contact reasoning）**的新范式。其核心洞察在于：**预测“哪些手指链接与物体表面在何处接触”这一中间表示，可以在高层任务语义与机器人本体/物体的物理约束之间架起一座桥梁**。

具体地，DextER 将抓取生成分解为两步自回归推理过程——先预测接触模式（contact tokens），再基于接触生成完整的抓取配置（action tokens）。这一分解的数学形式为：

$$p ( \mathbf { a } , { \mathcal { C } } | \mathbf { P } , \mathbf { T } ) = p ( { \mathcal { C } } | \mathbf { P } , \mathbf { T } ) \cdot p ( \mathbf { a } | { \mathcal { C } } , \mathbf { P } , \mathbf { T } )$$

其中 $\mathbf{a}$ 为抓取配置，$\mathcal{C}$ 为接触模式，$\mathbf{P}$ 为物体点云，$\mathbf{T}$ 为语言指令。通过这一分解，接触预测充当了具身感知的中间表征，使模型在生成最终抓取前已具备对物理交互的显式认知。

### 4. 关键证据预览

实验结果表明，这一接触推理机制是性能提升的关键因素。在 DexGYS 基准上，DextER 相较先前最佳模型 **DexGYSNet** 实现了 **96.4% 的意图对齐改进**（P-FID 从 5.60 降至 0.20）和 **3.83 个百分点的成功率提升**（从 63.31% 到 67.14%）。消融实验进一步证实：移除接触推理模块后，意图对齐指标 P-FID 从 0.20 恶化至 0.30（增加 50%），成功率从 67.14% 降至 62.37%，验证了接触推理对意图对齐和物理质量的双重贡献。

## 核心创新

DextER 的核心创新在于引入**基于接触预测的具身体验推理（Embodied Contact Reasoning）**，将语言驱动的灵巧抓取生成从“端到端映射”重构为“先推理接触、再生成动作”的两阶段生成范式。

### 推理链重构：从直接映射到接触中介

现有方法（如 **DexGYSNet**、**DGTR**、**GraspCVAE** 等）直接将视觉和语言输入映射到抓取参数，缺乏对多指手与物体之间物理交互接触的显式推理。这导致两个关键瓶颈：(1) 抓取与任务意图的对齐性差——模型难以理解“捏住杯柄”与“握住杯身”在接触层面的本质差异；(2) 物理稳定性有限——缺乏接触约束使生成的抓取配置容易穿透物体或无法形成力封闭。

DextER 将抓取生成过程分解为条件概率链（公式 1）：

$$p ( \mathbf { a } , { \mathcal { C } } | \mathbf { P } , \mathbf { T } ) = p ( { \mathcal { C } } | \mathbf { P } , \mathbf { T } ) \cdot p ( \mathbf { a } | { \mathcal { C } } , \mathbf { P } , \mathbf { T } )$$

其中 $\mathbf{P}$ 为物体点云，$\mathbf{T}$ 为语言指令，$\mathcal{C}$ 为接触模式（哪些手指链接在物体表面的何处接触），$\mathbf{a}$ 为完整抓取配置。模型**先预测接触令牌**（手指链接与 3D 接触位置），**再基于接触生成抓取配置令牌**，使接触模式成为连接高级任务语义与机器人本体物理约束的具身感知中间表示。

### 决定性证据

消融实验直接验证了接触推理的核心作用：**移除接触推理（w/o ER）导致意图对齐指标 P-FID 从 0.20 恶化至 0.30（增加 50%），成功率从 67.14% 降至 62.37%**（Table 1）。这表明接触推理不仅是辅助特征，而是实现意图对齐和物理质量的关键因果调节变量。

与先前最佳模型 **DexGYSNet** 相比，DextER 在 DexGYS 基准上实现了 **96.4% 的意图对齐改进**（P-FID: 0.20 vs 5.60）和 **3.83 个百分点的成功率提升**（67.14% vs 63.31%），验证了接触中介推理范式的显著优势。

### 架构配合：PartField 编码器的部件感知特征

接触推理的有效性高度依赖点云编码器提取的特征质量。DextER 采用 **PartField** 作为点云编码器，其部件感知的 3D 几何特征与接触推理天然匹配——预测“手指接触物体哪个部位”需要理解物体的功能部件结构。消融实验证实，PartField 显著优于通用编码器 Uni3D（P-FID: 0.20 vs 0.52，Success: 67.14% vs 59.07%），说明部件级几何理解是接触推理成功的前提。

### 模型容量并非关键

值得注意的是，将 LLM 骨干从 **Qwen2.5-0.5B** 扩展到 **Qwen2.5-1.5B** 仅带来 marginal 提升（成功率 67.14% → 67.55%），而更小的 **SmolLM2-360M** 也能达到 64.87% 的成功率。这表明性能增益主要源于接触推理架构本身，而非模型容量的简单堆叠。

## 整体框架

DextER 的整体 pipeline 围绕**基于接触预测的具身体验推理**展开，将语言驱动的灵巧抓取生成分解为两步自回归过程。其核心直觉是：在生成最终抓取配置之前，先显式地推理“多指手的哪些手指链接（finger links）与物体表面何处接触”，这一中间表示将高级任务语义与机器人本体的物理约束桥接起来，从而显著提升抓取的意图对齐性和物理稳定性。

### 输入输出流

给定物体的 3D 点云 $\mathbf{P}$ 和自然语言任务描述 $\mathbf{T}$（例如“用拇指和中指捏住把手的顶部”），模型输出完整的抓取配置 $\mathbf{a}$（包括手部关节角度和 6D 抓取姿态）。按照公式 (1) 的分解，推理过程为：

$$p ( \mathbf { a } , { \mathcal { C } } | \mathbf { P } , \mathbf { T } ) = p ( { \mathcal { C } } | \mathbf { P } , \mathbf { T } ) \cdot p ( \mathbf { a } | { \mathcal { C } } , \mathbf { P } , \mathbf { T } )$$

其中 $\mathcal{C}$ 为接触模式，由**接触令牌**（contact tokens）表示，指定了哪些手指链接接触物体表面，以及各接触点在物体表面的 3D 位置。模型先预测 $\mathcal{C}$，再以 $\mathcal{C}$ 为条件生成 $\mathbf{a}$。

### 模块架构与数据流

DextER 由三个核心模块串联构成（图 2）：

1. **点云编码器（PartField）**：提取部件感知的 3D 几何特征。PartField 编码器对物体点云进行编码，输出富含部件结构信息的视觉特征，为后续接触推理提供细粒度的几何线索。消融实验表明，PartField 显著优于通用点云编码器 Uni3D（成功率 67.14% vs 59.07%，P-FID 0.20 vs 0.52），其部件感知特征与接触推理高度匹配。

2. **多模态投影器（Multimodal Projector）**：将点云编码器输出的视觉特征投影到 LLM 的嵌入空间，使视觉 token 与文本 token 在统一的表示空间中对齐。

3. **LLM 骨干（Qwen2.5-0.5B）**：作为中央推理引擎，融合多模态 token 并自回归地生成接触令牌和动作令牌。LLM 采用 Prefix-LM 注意力掩码（图 4）：点云 token 使用双向注意力，其余 token（文本、接触、动作）使用因果注意力，均可关注所有前置的点云 token。

在 LLM 内部，推理过程序列化为：
- **接触令牌生成器（Contact Token Generator）**：自回归预测手指链接的离散 token 及其对应的 3D 接触位置 token。接触位置被离散化为 256 个 bin，并在训练中以 $p=0.5$ 的概率随机丢弃位置 token（保留链接 token），作为正则化手段，防止模型过度依赖精确位置而忽略语义层面的接触推理。
- **动作令牌生成器（Action Token Generator）**：以预测的接触令牌为条件，自回归生成完整的抓取配置 token（同样离散化为 256 个 bin），经去令牌化后得到手部关节角度和抓取姿态。

### 推理链的关键性

移除接触推理（w/o ER）直接导致意图对齐指标 P-FID 从 0.20 恶化至 0.30（相对退化 50%），成功率从 67.14% 降至 62.37%，验证了接触推理作为中间推理步骤的核心作用。值得注意的是，将 LLM 骨干从 0.5B 扩展到 1.5B 仅带来边际提升（成功率 67.14% → 67.55%），表明性能增益主要源于接触推理架构本身，而非模型容量。

### 补充图表

![[assets/figures/papers/paper_list_l2461_https_arxiv_org_abs_2601_16046/figures/002_Figure_2.jpg]]
*Figure 2: DextER model architecture. Our model processes 3D point clouds and language instructions to predict dexterous grasping actions for the multi-fingered robotic hand. (Left) The input point clouds and textual grasp descriptions are encoded into tokens using a pretrained point cloud encoder [24] and a text tokenizer [32, 44]. (Middle) The LLM backbone [32, 44] fuses point cloud embeddings with text prompts and autoregressively generates discretized contact and action tokens. (Right) The generated contact and action tokens are de-tokenized into contact positions, hand joint configurations, and grasp poses*

![[assets/figures/papers/paper_list_l2461_https_arxiv_org_abs_2601_16046/figures/001_Figure_1.jpg]]
*Figure 1: DextER introduces contact-based embodied reasoning for language-driven dexterous grasp generation. Given a 3D object and instruction, DextER autoregressively predicts which finger links contact where on the object surface before generating the final grasp. Our method achieves state-of-the-art performance with significant improvement in intention alignment and enables steerable generation where users can guide grasp synthesis by specifying partial contact constraints*

## 核心模块与公式推导

### 抓取生成的因子分解

DextER 的核心洞察是将灵巧抓取生成显式分解为两步推理过程，通过接触模式作为中间推理状态，桥接高层任务语义与底层物理约束。该分解形式化为：

$$p ( \mathbf { a } , { \mathcal { C } } | \mathbf { P } , \mathbf { T } ) = p ( { \mathcal { C } } | \mathbf { P } , \mathbf { T } ) \cdot p ( \mathbf { a } | { \mathcal { C } } , \mathbf { P } , \mathbf { T } )$$

其中：$\mathbf{P}$ 为物体点云，$\mathbf{T}$ 为语言指令，$\mathcal{C}$ 为接触模式（指定哪些手指链接与物体表面何处接触），$\mathbf{a}$ 为完整抓取配置（包含手部关节角度与抓取姿态）。该公式将传统端到端映射拆解为先预测接触模式、再基于接触生成抓取配置的两阶段推理链，使模型具备显式的物理交互推理能力。

### 模型架构模块

DextER 由五个核心模块串联构成：

**Point Cloud Encoder (PartField)**。该模块负责从输入物体点云中提取部件感知的 3D 几何特征。消融实验表明，PartField 显著优于通用点云编码器 Uni3D（P-FID 0.20 vs 0.52，成功率 67.14% vs 59.07%），其部件级特征与下游接触推理高度匹配。

**Multimodal Projector**。将 PartField 输出的视觉特征投影到 LLM 嵌入空间，实现视觉与语言模态的对齐。

**LLM Backbone (Qwen2.5-0.5B)**。作为多模态融合与自回归生成的核心，LLM 骨干接收视觉 token、文本 token，并按照 Prefix-LM 注意力模式（点云 token 使用双向注意力，其余 token 使用因果注意力）自回归生成离散化的接触与动作序列。

**Contact Token Generator**。该模块实现公式中 $p(\mathcal{C}|\mathbf{P},\mathbf{T})$ 的推理步骤，自回归预测手指链接（link）与 3D 接触位置的离散 token。接触 token 序列由链接 token $\langle l_i \rangle$ 和位置 token $\langle p_{ix} \rangle \langle p_{iy} \rangle \langle p_{iz} \rangle$ 组成，其中位置坐标被离散化为 256 个 bin。

**Action Token Generator**。基于已生成的接触 token，该模块实现 $p(\mathbf{a}|\mathcal{C},\mathbf{P},\mathbf{T})$ 的条件生成，输出完整的抓取配置 token，包括手部关节角度、抓取姿态等连续参数的离散化表示。

### 接触位置 Dropout 正则化

训练阶段引入接触位置 dropout 机制：以概率 $p_{\mathrm{drop}}$ 随机移除接触序列中的位置 token $\langle p_{ix} \rangle \langle p_{iy} \rangle \langle p_{iz} \rangle$，同时保留链接 token $\langle l_i \rangle$。消融实验确定最优 dropout 概率为 0.5（P-FID=0.20, Con.=0.34），该正则化迫使模型在部分接触信息缺失时仍能推断合理抓取，提升泛化能力。

### 关键设计决策的消融验证

**离散化粒度**。动作 token 与位置 token 均采用 256 个 bin 进行离散化，消融实验证实该配置在所有指标上达到最优性能。

**LLM 骨干规模**。将 LLM 从 Qwen2.5-0.5B 扩展到 1.5B 仅带来 marginal 提升（成功率 67.14% → 67.55%），而 SmolLM2-360M 亦可取得可比结果（成功率 64.87%），表明性能增益主要源于接触推理架构而非模型容量。

**接触推理的因果作用**。移除接触推理模块（w/o ER）导致意图对齐指标 P-FID 从 0.20 恶化至 0.30（增幅 50%），成功率从 67.14% 降至 62.37%，直接验证了接触推理是驱动性能提升的关键因果变量。

### 补充图表

![[assets/figures/papers/paper_list_l2461_https_arxiv_org_abs_2601_16046/figures/009_Figure_4.jpg]]
*Figure 4: Prefix-LM attention mask for DextER. Point cloud (PC) tokens use bidirectional attention (full blue blocks in PC rows/columns), whereas the other tokens use causal attention (lower triangular patterns), attending to all preceding point cloud tokens*

## 实验与分析

### 核心实验设置

DextER 在 **DexGYS** 和 **Dexonomy** 两个大规模灵巧抓取数据集上进行训练和评估。DexGYS 提供带有语言指令的抓取标注，Dexonomy 则用于零样本泛化与可操控生成测试。训练数据同时来自这两个数据集（Sec. 3.4）。

评估维度覆盖三个层面：
- **意图对齐（Intention Alignment）**：P-FID（越低越好）、Chamfer Distance（CD）、Contact Ratio（Con.）
- **物理质量（Physical Quality）**：仿真成功率（Success %）、穿透深度（Pen.）、Q1 质量分数
- **多样性（Diversity）**：平移、旋转、关节角度的标准差（δ_t, δ_r, δ_q）

### 主实验结果

在 DexGYS 验证集上，DextER 在所有意图对齐指标上大幅超越先前方法，同时保持了最高的物理成功率（Table 1）。

![[assets/figures/papers/paper_list_l2461_https_arxiv_org_abs_2601_16046/figures/003_Table_1.jpg]]
*Table 1: Language-conditioned grasp generation on DexGYS validation set. We evaluate intention alignment (P-FID, CD, Con.), physical quality (Success*

| 方法 | P-FID ↓ | Success ↑ | CD ↓ | Con. ↑ |
|------|---------|-----------|------|--------|
| GraspCVAE | 9.14 | 53.82 | 0.018 | 0.25 |
| GraspTTA | 9.38 | 56.58 | 0.019 | 0.24 |
| SceneDiffuser | 8.50 | 57.70 | 0.017 | 0.26 |
| DGTR | 6.22 | 60.50 | 0.016 | 0.27 |
| DexGYSNet | 5.60 | 63.31 | 0.015 | 0.28 |
| **DextER** | **0.20** | **67.14** | **0.009** | **0.34** |
| DextER (w/o ER) | 0.30 | 62.37 | 0.012 | 0.27 |

**关键发现：**
1. **意图对齐的质变**：DextER 的 P-FID 仅 0.20，相比先前最优 DexGYSNet 的 5.60 实现了 **96.4% 的改进**。这表明接触推理使模型能精确理解任务语义（如“用指尖捏住杯柄”）并生成对应的抓取姿态，而非仅输出物理可行的任意抓取。
2. **物理质量的同步提升**：成功率从 63.31% 提升至 67.14%（**+3.83 p.p.**），证明接触推理不仅改善语义对齐，也通过显式建模手-物交互接触增强了物理稳定性。
3. **接触推理的因果作用**：移除具身推理（w/o ER，即直接从视觉/语言映射到抓取参数）导致 P-FID 从 0.20 退化至 0.30（**恶化 50%**），成功率从 67.14% 降至 62.37%。这确证了接触预测作为中间推理步骤的核心因果作用，而非模型容量增加的附带效应。

### 消融实验

Table 2 系统分析了四个关键设计选择的影响：

![[assets/figures/papers/paper_list_l2461_https_arxiv_org_abs_2601_16046/figures/005_Table_2.jpg]]
*Table 2: Ablation studies on DexGYS validation set. We systematically analyze the impact of key design choices: token discretization granularity, point cloud encoder architecture, backbone model capacity, and contact position dropout probability. We report primary metrics for intention alignment (P-FID, Con.) and physical quality (Success). The default configuration achieves strong performance across all metrics*

**1. Token 离散化粒度**
动作 token 和位置 token 均离散化为 256 个 bin 时达到最优（P-FID=0.20, Success=67.14%）。更粗的离散化（64/128 bin）会损失精度，更细的离散化（512 bin）则导致 token 空间过大、训练困难。

**2. 点云编码器**
PartField 编码器显著优于 Uni3D（Success: 67.14% vs 59.07%, P-FID: 0.20 vs 0.52）。PartField 的部件感知特征与接触推理高度匹配——模型需要知道“杯柄在哪里”才能预测“手指接触杯柄”，而 Uni3D 的全局特征缺乏这种细粒度几何信息。

**3. LLM 骨干规模**
将 Qwen2.5-0.5B 扩展到 1.5B 仅带来 marginal 提升（Success: 67.14% → 67.55%），SmolLM2-360M 也能达到 64.87%。这表明 **性能增益主要源于接触推理架构本身，而非 LLM 的容量或特定架构选择**。这一发现具有重要的实践意义：DextER 的核心思想可以在轻量级 LLM 上高效实现。

**4. 接触位置 Dropout**
以概率 0.5 随机丢弃接触位置 token（保留手指链接 token）获得最佳性能（P-FID=0.20, Con.=0.34）。适度的 dropout 迫使模型在位置信息不完整时依赖链接类型进行推理，起到正则化作用，防止对精确位置的过拟合。无 dropout（p=0）或过高 dropout（p=0.7）均导致性能下降。

### 零样本泛化与可操控生成

在 Dexonomy 数据集上的零样本评估（Table 3）显示，DextER 在未见过的物体类别和抓取类型上保持了较强的泛化能力。更重要的是，DextER 支持 **可操控生成（Steerable Generation）**：用户可以通过指定部分接触约束（如“食指接触物体的顶部”）来引导抓取合成，模型会在满足约束的前提下生成完整抓取配置。这在实际人机交互场景中具有重要价值。

![[assets/figures/papers/paper_list_l2461_https_arxiv_org_abs_2601_16046/figures/006_Table_3.jpg]]
*Table 3: Evaluation on Dexonomy [6]. (Upper) Zero-shot generalization across data splits. (Lower) Steerable generation with partial contact specification*

### 接触预测质量

Table 4 单独评估了具身思维链中接触预测的准确性。模型在接触链接预测上达到较高的 IoU 和 F1 分数，且预测的接触位置经过正向运动学验证，大部分落在真实链接位置的 1 cm 范围内。这进一步验证了接触推理不是“黑箱猜测”，而是可解释、可验证的物理推理过程。

![[assets/figures/papers/paper_list_l2461_https_arxiv_org_abs_2601_16046/figures/007_Table_4.jpg]]
*Table 4: Contact prediction quality. We evaluate the accuracy of predicted contact links and positions in the embodied CoT sequence. IoU, Precision, Recall, and F1 measure the contact link prediction accuracy. Position Accuracy measures the percentage of predicted contact positions within 1cm of the actual link positions computed via forward kinematics of the predicted grasp pose*

### 失败模式分析

尽管整体性能优异，DextER 存在两类典型失败：
1. **量化伪影导致穿透**：约 14.7% 的失败案例由连续参数离散化引入的量化误差造成。虽然预测的接触语义和抓取意图正确，但离散 token 解码回连续值时产生的微小偏差足以导致手指穿透物体表面。这提示未来工作可探索混合离散-连续表示或后处理优化步骤。
2. **未见抓取类型的物理不稳定**：在部分未见过的抓取类型上，接触推理能泛化出语义合理的姿态，但物理仿真中可能不稳定。这反映出模型虽然学到了接触语义，但未能完全捕获力封闭（force closure）等底层物理稳定性线索。

### 推理效率

Table 5 的推理时间对比显示，DextER 的自回归生成过程引入了适度的计算开销，但仍在可接受范围内，且显著优于部分基于扩散模型的基线方法。

![[assets/figures/papers/paper_list_l2461_https_arxiv_org_abs_2601_16046/figures/008_Table_5.jpg]]
*Table 5: Inference time comparison on DexGYS*

### 补充图表

![[assets/figures/papers/paper_list_l2461_https_arxiv_org_abs_2601_16046/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative results on language-conditioned dexterous grasp generation. Given object point clouds and natural language instructions, DextER generates embodied contact predictions (shown as colored spheres on object surfaces) followed by grasp configurations. The model successfully captures task-specific contact patterns and produces physically plausible grasps that align with language instructions across diverse objects and manipulation intents. The 3rd and 4th columns show predictions from the same model (DextER), visualized in two separate columns to better highlight the predicted contact points in the 3rd column*

![[assets/figures/papers/paper_list_l2461_https_arxiv_org_abs_2601_16046/figures/014_Table_8.jpg]]
*Table 8: Robustness to partial and noisy observations on Dex-GYS. Zero-shot evaluation without retraining on partial inputs*

![[assets/figures/papers/paper_list_l2461_https_arxiv_org_abs_2601_16046/figures/032_Figure_10.jpg]]
*Figure 10: Steerable grasp generation example*

![[assets/figures/papers/paper_list_l2461_https_arxiv_org_abs_2601_16046/figures/010_Table_6.jpg]]
*Table 6: Training hyperparameters and configuration for DextER*

## 方法谱系与知识库定位

### 1. 基线方法谱系

DextER 所对比的基线方法覆盖了灵巧抓取生成领域的主要技术路线，可归纳为三类范式：

**直接回归范式**：早期工作将视觉输入直接映射到抓取参数，缺乏中间推理环节。
- **GraspCVAE**：基于条件变分自编码器的抓取生成方法，从点云直接回归抓取配置，无显式任务语义建模。
- **GraspTTA**：利用测试时自适应策略优化抓取质量，但生成过程仍为端到端映射，未解耦任务理解与物理约束。

**扩散生成范式**：将扩散模型引入抓取生成，通过迭代去噪提升多样性和质量。
- **SceneDiffusers**：基于场景条件扩散的抓取生成方法，以去噪过程隐式建模抓取分布，但缺乏对接触物理的显式表征。
- **DGTR**：基于 Transformer 的扩散抓取生成方法，通过注意力机制融合多模态信息，但仍将接触推理隐式地交由模型自行学习。

**语言条件范式**：引入自然语言指令作为任务条件，实现意图对齐的抓取生成。
- **DexGYSNet**：此前 DexGYS 基准上的最优方法，直接融合语言和视觉特征预测抓取参数，是 DextER 的直接对比对象。该方法在意图对齐指标 P-FID 上为 5.60，成功率 63.31%。

### 2. DextER 的关键差异与因果机制

DextER 与上述基线的本质区别在于**推理链的结构性改变**：

| 维度 | 基线方法 | DextER |
|------|----------|--------|
| 推理路径 | 视觉+语言 → 抓取参数（单步映射） | 视觉+语言 → 接触令牌 → 抓取令牌（两步推理） |
| 中间表征 | 无显式中间表征 | 具身接触令牌（手指链接×3D接触位置） |
| 物理约束 | 隐式学习 | 显式预测接触模式作为条件 |

这一差异的因果机制体现在公式 (1) 的概率分解中：

$$p ( \mathbf { a } , { \mathcal { C } } | \mathbf { P } , \mathbf { T } ) = p ( { \mathcal { C } } | \mathbf { P } , \mathbf { T } ) \cdot p ( \mathbf { a } | { \mathcal { C } } , \mathbf { P } , \mathbf { T } )$$

该分解将抓取生成重构为**接触模式预测**与**条件抓取配置生成**两个阶段。接触令牌 $\mathcal{C}$ 作为具身感知的中间表征，桥接了高级任务语义（语言指令 $\mathbf{T}$）与低级物理约束（手-物接触几何），从而显著提升意图对齐与物理稳定性。

**消融实验的因果验证**：移除接触推理模块（w/o ER）导致 P-FID 从 0.20 恶化至 0.30（增幅 50%），成功率从 67.14% 降至 62.37%，直接证明了接触推理是性能提升的核心因果杠杆，而非模型容量或架构选择的附带效应。

### 3. 适用边界

**有效边界**：
- **任务类型**：语言驱动的灵巧抓取生成，涵盖抓取、握持、操作等意图类别。
- **手部形态**：多指灵巧手（DexGYS 及 Dexonomy 数据集中的手部模型）。
- **输入模态**：完整 3D 点云 + 自然语言指令。
- **输出空间**：抓取姿态、手部关节配置、接触位置。

**泛化边界**：
- **零样本泛化**：DextER 在 Dexonomy 数据集的跨数据划分上展现出零样本泛化能力（Table 3），表明接触推理的中间表征具有一定的任务迁移性。
- **部分观测鲁棒性**：Table 8 显示模型在零样本条件下对部分和噪声观测具有一定鲁棒性，但未经过针对性训练。
- **可操控生成**：用户可通过指定部分接触约束引导抓取合成（Table 3 下部，Figure 10），这是接触令牌作为显式中间表征的独特优势。

**失效边界**：
- **未见抓取类型**：对于训练分布外的抓取类型，接触推理虽能泛化出合理姿态，但物理执行可能不稳定，模型未能完全捕获某些抓取类型的力封闭稳定性线索。
- **量化伪影**：14.7% 的失败案例由连续参数离散化导致的量化误差引起，表现为手-物穿透，尽管预测的接触/抓取语义正确。这是自回归离散 token 框架的固有局限。
- **复杂真实场景**：当前评估限于相对结构化的数据集环境，存在遮挡的非结构化场景尚未验证。

### 4. 局限性与开放问题

**已知局限**：
1. **量化误差与物理穿透**：连续参数被离散化为 256 个 bin 的 token，导致 14.7% 的失败案例出现手-物穿透。离散化粒度（Table 2 消融）虽经优化，但量化伪影是自回归框架的结构性代价。
2. **力封闭稳定性不足**：在未见过的抓取类型上，模型生成的姿态可能缺乏力封闭保证，反映出接触推理虽能捕获接触几何，但未显式建模接触力与摩擦锥约束。
3. **模型容量边际收益递减**：将 LLM 骨干从 Qwen2.5-0.5B 扩展到 1.5B 仅带来 0.41 个百分点的成功率提升（67.14% → 67.55%），表明性能瓶颈在于接触推理架构本身而非模型容量。

**开放问题**：
1. **自回归框架的复合误差**：自回归生成中的逐步误差累积可能导致接触预测偏差被后续抓取生成放大。扩散模型是否能通过并行去噪提供更稳健的替代方案，是一个值得探索的方向。
2. **真实场景部署**：当前评估基于完整点云输入，如何将方法扩展到存在遮挡、传感器噪声、动态环境的真实操作场景，是推动实际部署的关键挑战。
3. **力封闭的显式建模**：将力封闭约束或接触力分析融入接触推理过程，有望解决未见抓取类型的稳定性问题，但需重新设计 token 表征与训练目标。
4. **更丰富的手部形态泛化**：当前方法针对特定多指手设计，接触令牌的定义依赖于手部运动学链。如何将接触推理框架泛化到不同手部形态（如二指夹爪、三指手、五指手）仍需探索。

### 5. 知识库定位

DextER 在灵巧抓取领域的知识贡献可定位于以下交叉点：

- **具身推理（Embodied Reasoning）**：首次将接触预测作为显式的中间推理步骤引入抓取生成，区别于以往隐式学习接触约束的方法。这一设计与视觉-语言模型中的 Chain-of-Thought 推理理念相通，但将其具身化到机器人本体的物理交互层面。
- **语言驱动操作（Language-driven Manipulation）**：在语言条件抓取任务上建立了新的 SOTA（P-FID 改进 96.4%，成功率提升 3.83 p.p.），证明了语义理解与物理交互之间的显式桥接优于隐式融合。
- **离散 token 生成（Discrete Token Generation）**：将连续抓取参数离散化为 token 序列，使灵巧抓取生成能够纳入自回归语言模型的训练范式，但同时也引入了量化误差的结构性代价。

该方法为后续研究提供了两个可复用的技术锚点：(1) 接触令牌作为可解释、可操控的中间表征；(2) 概率分解框架 $p(\mathcal{C}|\mathbf{P},\mathbf{T}) \cdot p(\mathbf{a}|\mathcal{C},\mathbf{P},\mathbf{T})$ 可作为引入其他物理约束（如力封闭、稳定性）的通用模板。

## 原文 PDF

![[paperPDFs/CVPR_2026/DextER_Language_driven_Dexterous_Grasp_Generation_with_Embodied_Reasoning.pdf]]
