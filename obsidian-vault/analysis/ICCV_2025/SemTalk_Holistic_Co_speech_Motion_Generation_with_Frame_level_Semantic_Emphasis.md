---
title: SemTalk Holistic Co speech Motion Generation with Frame level Semantic Emphasis
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/SemTalk_Holistic_Co_speech_Motion_Generation_with_Frame_level_Semantic_Emphasis.pdf
aliases:
- SHCSMGFLSE
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 语义门控 sem-gate 产生的帧级语义分数 ψ，能够动态调节语义动作的强调程度，使模型在保持节奏同步的同时突出语义丰富的关键帧。
primary_logic: 将协同语音运动显式分解为节奏相关的基础运动与语义感知的稀疏运动，并利用自适应融合机制，在确保自然节奏对齐的同时显著增强动作的语义丰富度。
claims:
- 语义相关动作在帧级别是稀疏的，与日常观察一致。
- SemTalk 在 BEAT2 和 SHOW 数据集上均优于最先进方法。
- 语义门控整合特征加权和损失加权有效提升语义分类准确率和 FGD。
- 节奏一致性学习、语义强调学习和 Coarse2Fine 注意力模块均对最终性能有积极贡献。
---

# SemTalk Holistic Co speech Motion Generation with Frame level Semantic Emphasis

> [!tip] 核心洞察
> 将协同语音运动显式分解为节奏相关的基础运动与语义感知的稀疏运动，并利用自适应融合机制，在确保自然节奏对齐的同时显著增强动作的语义丰富度。

| 字段 | 内容 |
|------|------|
| 中文题名 | SemTalk：具有帧级语义强调的整体协同语音动作生成 |
| 英文题名 | SemTalk Holistic Co speech Motion Generation with Frame level Semantic Emphasis |
| 会议/期刊 | ICCV 2025 |
| Links | [Project](https://xiangyue-zhang.github.io/SemTalk) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SemTalk |
| Dataset | BEAT2, SHOW |

> [!tip] 效果简介
> - BEAT2 上，FGD↓ 4.278 vs best competitor (Table 1) (显著优于所有基线)；MSE↓ 6.153 vs best competitor (显著降低)；LVD↓ 6.938 vs best competitor (显著降低)。
> - SHOW 上，BC↑ 8.304 vs best competitor (最高)。

## 概述

协同语音动作生成旨在从语音输入中合成与说话内容同步的自然人体动作。现有方法普遍依赖节奏特征驱动运动生成，但**语义相关的手势动作在帧级别高度稀疏**（Figure 1 左侧分析），导致生成的动作缺乏语义深度和表现力——这是当前领域的核心瓶颈。

针对这一问题，SemTalk 提出了一种**整体协同语音运动生成框架**，其核心洞察在于：将协同语音运动显式分解为**节奏对齐的基础运动**（base motion）与**语义感知的稀疏运动**（sparse motion），并通过一个可学习的**语义门控机制**（sem-gate）在帧级别自适应融合两者。该门控产生的帧级语义分数 $\psi$ 能够动态调节语义动作的强调程度，使模型在保持节奏同步的同时，在语义丰富的关键帧突出手势、躯干等部位的动作幅度（Figure 1 右侧）。

在方法定位上，SemTalk 区别于 **LivelySpeaker**（Zhi et al., ICCV 2023）将语义与节奏分离处理的方式，也不同于 **TalkSHOW**（Yi et al., CVPR 2023）、**ProbTalk**（Liu et al., CVPR 2024）、**EMAGE**（Liu et al., CVPR 2024）和 **DiffSHEG**（Chen et al., CVPR 2024）等整体编码方案，首次在帧级别实现了语义强调与节奏对齐的统一建模（Figure 4）。

实验结果表明，SemTalk 在 **BEAT2** 和 **SHOW** 两个公开数据集上均显著优于现有最先进方法（Table 1）：在 BEAT2 上，FGD 降至 4.278，MSE 降至 6.153，LVD 降至 6.938；在 SHOW 上，BC 达到 8.304。消融研究进一步验证了语义门控、节奏一致性学习、Coarse2Fine 交叉注意力等关键组件的正向贡献（Table 2, Table 3）。用户研究也证实了生成动作在自然度和语义一致性上的优势（Figure 10）。

目前方法依赖 BEAT2 的帧级语义标注，尚未在跨语言或跨文化场景下验证，语义分数阈值 $\beta$ 为经验设置，这些构成了当前的主要局限。

## 背景与动机

协同语音动作生成（Co-Speech Motion Generation）旨在根据语音输入合成与说话内容、节奏和情感同步的自然人体动作，是虚拟人交互、数字人播报等应用的核心技术。近年来，基于深度学习的生成方法取得了显著进展，但现有工作普遍存在一个关键瓶颈：**过度依赖节奏特征，难以有效捕捉稀疏但语义关键的手势动作，导致生成的动作缺乏语义深度和表现力**。

具体而言，主流方法——无论是基于扩散的 **DiffSHEG**（Chen et al., CVPR 2024）、基于掩码建模的 **EMAGE**（Liu et al., CVPR 2024）、基于 VQ-VAE 的 **TalkSHOW**（Yi et al., CVPR 2023），还是基于 PQ-VAE 的 **ProbTalk**（Liu et al., CVPR 2024）——大多将运动视为整体进行编码与生成，未对节奏驱动的基础运动与语义驱动的稀疏手势进行显式解耦。这使得模型在追求整体运动平滑性和节奏对齐时，往往弱化甚至忽略了那些出现频率低但对表意至关重要的语义手势。**LivelySpeaker**（Zhi et al., ICCV 2023）虽然尝试结合语义与节奏信息，但其语义手势生成和节奏手势细化是分离的两个阶段，容易引入运动抖动和不连贯。

Figure 1 左侧的语义分析直观地揭示了这一问题的根源：对 BEAT2 数据集的帧级语义标签进行统计后发现，**语义相关的动作在帧级别是极其稀疏的**，这与日常交流中“大部分身体动作服务于节奏同步，仅在关键词处出现强调性手势”的观察高度一致。然而，现有方法缺乏对这类稀疏关键帧的专门建模机制，导致语义手势被淹没在大量的节奏动作中。

针对上述缺口，本文提出 **SemTalk**，核心动机在于：**将协同语音运动显式分解为节奏相关的基础运动与语义感知的稀疏运动，并利用自适应融合机制，在确保自然节奏对齐的同时显著增强动作的语义丰富度**。这一设计的关键在于引入一个可学习的“语义门控”（sem-gate），产生帧级语义分数 $\psi$，动态调节语义动作的强调程度，使模型能够在保持整体节奏同步的前提下，精准地在语义关键帧上放大手势和躯干的表现力（如 Figure 1 右侧示例中对 “watching” 和 “just” 的强调）。与 LivelySpeaker 的分离式两阶段方案不同，SemTalk 将节奏与语义统一在一个端到端框架内，通过语义分数实现平滑、连贯的运动融合（见 Figure 4 的概念对比）。

## 核心创新

SemTalk 的核心创新在于将协同语音动作生成从“整体建模”推进到“显式解耦—自适应融合”的范式。它抓住了现有方法的一个关键瓶颈：**过度依赖节奏特征，难以捕捉稀疏但语义关键的手势**。日常对话中，语义相关动作在帧级别是高度稀疏的（Figure 1 左侧分析，置信度 0.95），但现有方法如 **DiffSHEG** (Chen et al., CVPR 2024)、**EMAGE** (Liu et al., CVPR 2024) 等并未对此进行显式建模，导致生成的动作缺乏语义深度。

SemTalk 通过以下四个 **changed slots** 实现突破：

1.  **运动表示分解**：将运动编码显式分离为节奏对齐的**基础运动** $q^b$ 和语义感知的**稀疏运动** $q^s$。基线方法通常采用整体运动编码，无此分离。该分解由基础运动模块 $f_r$ 和稀疏运动模块 $f_s$ 分别完成，其映射关系为：
    $$f_r : (\gamma_b, \gamma_h, \tilde{m}, id; \theta_{f_r}) \rightarrow q^b$$
    $$f_s : (\phi_l, \phi_g, \phi_e, \tilde{m}, id; \theta_{f_s}) \rightarrow (q^s, \psi)$$
    其中 $\gamma$ 为节奏特征，$\phi$ 为语义特征，$\tilde{m}$ 为种子姿态，$id$ 为说话人 ID。

2.  **语义门控机制 (sem-gate)**：这是实现帧级强调的**因果旋钮**。sem-gate 利用多模态输入生成帧级语义分数 $\psi$，并通过特征加权 $W_f$ 和损失加权 $W_l$ 对关键帧进行双重强调。这与 **LivelySpeaker** (Zhi et al., ICCV 2023) 的全局控制或分离式融合有本质区别：LivelySpeaker 的 SAG 模块用 CLIP 嵌入生成语义手势，再用扩散模型单独优化节奏，容易导致抖动（Figure 4）；而 SemTalk 的门控机制实现了统一的、细粒度的帧级控制。

3.  **节奏一致性约束**：基线方法通常仅依赖音频特征输入，缺乏明确的多层次对齐损失。SemTalk 引入了局部帧级和全局序列级的 InfoNCE 损失 $\mathcal{L}_{\mathrm{Rhy}}^{(L)}$ 与 $\mathcal{L}_{\mathrm{Rhy}}^{(G)}$，将隐式运动特征与 HuBERT 节奏特征在隐空间中对齐，确保基础运动的节奏同步性。

4.  **身体部位交叉注意力层次 (Coarse2Fine)**：替代了平级的部位处理或独立生成。SemTalk 设计了一条逐级传递的注意力链：**面部 → 手部 → 上体 → 下体**，让精细的面部表情引导手部动作，进而驱动躯干运动，形成符合人类行为学的层次化动作生成。

最终，语义分数 $\psi$ 引导的融合函数 $\mathcal{E}$ 将基础编码与稀疏编码自适应结合：
$$q^m = \mathcal{E}(q^b, q^s; \psi)$$
并通过 RVQ-VAE 解码器生成最终运动。这一整套机制使得 SemTalk 在保持自然节奏对齐的同时，能在“watching”、“just”等关键词上显著增强手势和躯干的表现力（Figure 1 右侧示例）。

## 整体框架

SemTalk 的整体设计源于对协同语音动作中语义稀疏性的观察：语义相关的手势在帧级别上出现频率很低，与日常交流中“关键词语义手势”的直觉一致（Figure 1）。基于这一瓶颈，SemTalk 将整体协同语音运动生成显式分解为两个并行的生成流，并通过自适应融合机制在帧级别动态强调语义关键帧。

### 双流生成架构

SemTalk 的 pipeline 由两个核心生成模块构成（Figure 2, Figure 3）：

![[assets/figures/papers/paper_list_l1895_SemTalk_Holistic_Co_speech_Motion_Generation_with_Frame_level_Semantic_E/figures/002_Figure_2.jpg]]
*Figure 2: An overview of the SemTalk pipeline. SemTalk generates holistic co-speech motion by first constructing rhythm-aligned*

- **基础运动模块（Base Motion Blocks）** $f_r$：以节奏特征 $\gamma_b, \gamma_h$、种子姿态 $\tilde{m}$ 和说话人身份 $id$ 为输入，生成节奏对齐的基础运动编码 $q^b$。该模块专注于捕捉与语音节奏同步的周期性运动（如身体摆动、面部律动），确保生成动作的自然流畅性。
  
- **稀疏运动模块（Sparse Motion Blocks）** $f_s$：以语言级语义特征 $\phi_l$、全局语义特征 $\phi_g$（来自 CLIP）、情感特征 $\phi_e$（来自 emotion2vec）、种子姿态 $\tilde{m}$ 和说话人身份 $id$ 为输入，同时输出语义运动编码 $q^s$ 和帧级语义分数 $\psi$。该模块负责捕捉稀疏但语义关键的手势动作。

### 语义门控与自适应融合

两个生成流的融合由**语义门控（sem-gate）** 机制控制。sem-gate 利用多模态输入（文本、语音、情感）生成帧级语义分数 $\psi \in [0, 1]$，该分数在训练和推理中通过两种加权方式发挥作用：

- **特征加权** $W_f$：在特征层面以 $\psi$ 为权重对稀疏语义特征 $f_s$ 和基础运动特征 $f_b$ 进行 alpha 混合，生成语义强调的运动编码：
  $$q^s = MLP(\psi f_s + (1 - \psi) f_b)$$

- **损失加权** $W_l$：在训练时根据 $\psi$ 对语义相关帧施加更高的监督权重，使模型更关注关键语义帧的动作质量。

最终，融合模块 $\mathcal{E}$ 根据语义分数 $\psi$ 和阈值 $\beta$ 选择性地将稀疏语义编码替换到基础运动编码中，得到最终运动编码 $q^m$：
$$q^m = \mathcal{E}(q^b, q^s; \psi)$$

当 $\psi_i > \beta$ 时，基础运动编码 $q_i^b$ 被替换为稀疏语义编码 $q_i^s$；否则保留基础运动编码。这种自适应融合策略使 SemTalk 在保持节奏连贯性的同时，在语义关键帧上显著增强动作的表现力。

### 层次化身体部位细化

基础运动模块内部采用 **Coarse2Fine Cross-Attention** 模块，按照面部 → 手部 → 上体 → 下体的层级顺序逐级传递运动信息。面部作为最精细的节奏载体首先被生成，随后通过交叉注意力引导手部动作，手部再影响上体，上体驱动下体。这种层次化设计确保了全身动作的协调性和节奏一致性。

### 训练约束

整个 pipeline 的训练由两个核心损失驱动：

- **节奏一致性损失** $\mathcal{L}_{Rhy}$：包括局部帧级 $\mathcal{L}_{Rhy}^{(L)}$ 和全局序列级 $\mathcal{L}_{Rhy}^{(G)}$ 的 InfoNCE 损失，将隐式运动表示与 HuBERT 节奏特征对齐，确保生成动作与语音节奏的同步性。

- **语义强调损失**：在 sem-gate 的监督下，通过 GT 语义标签对语义分类进行约束，并结合 $W_f$ 和 $W_l$ 双重加权机制强化关键帧的语义动作学习。

融合后的运动编码 $q^m$ 最终通过 **RVQ-VAE 解码器** 重建为完整的全身运动序列。

## 核心模块与公式推导

SemTalk 的核心设计在于将协同语音运动显式分解为节奏对齐的基础运动与语义感知的稀疏运动，并通过帧级语义门控进行自适应融合。以下阐述关键模块及其公式。

### 1. 运动表示分解

传统方法将整体运动编码为一个单一表示，难以区分节奏驱动的基础动作与语义触发的稀疏手势。SemTalk 将这一过程解耦为两个并行的生成模块。

**基础运动生成映射**：基础运动模块 $f_r$ 从节奏特征 $\gamma_b$（身体节奏）、$\gamma_h$（手部节奏）、种子姿态 $\tilde{m}$ 和说话人身份 $id$ 出发，生成节奏对齐的运动编码 $q^b$：

$$f_r : (\gamma_b, \gamma_h, \tilde{m}, id; \theta_{f_r}) \rightarrow q^b$$

该模块的核心目标是确保生成的动作与语音节奏高度同步，形成自然流畅的基底运动。

**稀疏运动生成映射**：稀疏运动模块 $f_s$ 则从语义特征 $\phi_l$（帧级文本嵌入）、$\phi_g$（句子级 CLIP 特征）、$\phi_e$（情感特征，来自 emotion2vec）、种子姿态 $\tilde{m}$ 和说话人身份 $id$ 出发，同时生成语义运动编码 $q^s$ 和帧级语义分数 $\psi$：

$$f_s : (\phi_l, \phi_g, \phi_e, \tilde{m}, id; \theta_{f_s}) \rightarrow (q^s, \psi)$$

语义分数 $\psi$ 是 SemTalk 的关键创新——它是一个帧级的标量，用于动态衡量每一帧的语义重要性，从而决定稀疏语义运动在最终合成中的参与程度。

### 2. 语义门控与自适应融合

获得 $q^b$ 和 $q^s$ 后，SemTalk 通过语义分数 $\psi$ 引导的自适应融合机制 $\mathcal{E}$ 生成最终的运动编码 $q^m$：

$$q^m = \mathcal{E}(q^b, q^s; \psi)$$

融合的具体实现采用 alpha 混合策略。在 Sparse Motion Blocks 内部，语义分数 $\psi$ 对基础运动特征 $f_b$ 和稀疏语义运动特征 $f_s$ 进行加权混合，再通过 MLP 得到语义强调后的运动编码：

$$q^s = MLP( \psi f_s + ( 1 - \psi ) f_b )$$

这一设计的直觉在于：当 $\psi$ 较高时（如关键词出现时），语义特征 $f_s$ 占主导，手势表现力增强；当 $\psi$ 较低时（如功能词或静默段），基础运动特征 $f_b$ 占主导，维持节奏连贯性。在后续融合阶段，还引入阈值 $\beta$ 进行硬选择：若 $\psi_i > \beta$，则用稀疏语义编码替换对应帧的基础编码，实现关键帧的语义强调。

### 3. 节奏一致性约束

为确保基础运动与语音节奏的精确对齐，SemTalk 引入了局部-全局节奏一致性学习，采用 InfoNCE 损失对齐隐式运动表示与 HuBERT 节奏特征：

$$\mathcal{L}_{\mathrm{Rhy}} = -\frac{1}{N} \sum_{i=1}^{N} \log \frac{\exp(\mathrm{sim}(h(f_i), \gamma_h^i)/\tau)}{\sum_{j=1}^{N} \exp(\mathrm{sim}(h(f_i), \gamma_h^j)/\tau)}$$

其中，$h(f_i)$ 为隐式运动特征，$\gamma_h^i$ 为对应帧的 HuBERT 节奏特征，$\tau$ 为温度系数。该损失在局部帧级（$\mathcal{L}_{Rhy}^{(L)}$）和全局序列级（$\mathcal{L}_{Rhy}^{(G)}$）两个粒度上施加，确保短时节奏和长时韵律的一致性。

### 4. Coarse2Fine 交叉注意力模块

在基础运动生成阶段，SemTalk 设计了层次化的 Coarse2Fine 交叉注意力模块。信息流遵循从面部到手部、再到上体、最后到下体的逐级传递路径：面部引导手部动作，手部影响上体，上体进而驱动下体。这一设计模拟了人类交流中身体各部位的协调层级，确保节奏信息在全身运动中的一致性传播。

### 补充图表

![[assets/figures/papers/paper_list_l1895_SemTalk_Holistic_Co_speech_Motion_Generation_with_Frame_level_Semantic_E/figures/003_Figure_3.jpg]]
*Figure 3: Architecture of SemTalk. SemTalk generates holistic co-speech motion in three stages. (a) Base Motion Generation uses rhythmic consistency learning to produce rhythm-aligned codes*

![[assets/figures/papers/paper_list_l1895_SemTalk_Holistic_Co_speech_Motion_Generation_with_Frame_level_Semantic_E/figures/004_Figure_4.jpg]]
*Figure 4: Concept comparison with LivelySpeaker [52]. (Top) LivelySpeaker generates semantic gestures with CLIP embeddings in SAG and refines rhythm-related gestures separately using diffusion, causing potential jitter. (Bottom) SemTalk integrates text and speech, uses a semantic gate for fine-grained control, and unifies rhythm and semantics for smoother, more coherent motions*

## 实验与分析

### 核心瓶颈验证：语义相关动作在帧级别是稀疏的

SemTalk 的设计起点是一个经过数据验证的观察：在 BEAT2 数据集中，语义相关动作在帧级别高度稀疏（Figure 1 左侧语义分析，置信度 0.95）。这一发现与日常交流中“多数手势只是节奏性摆动，仅有少数关键帧承载语义表达”的直觉一致。然而，现有方法（如 **DiffSHEG** (Chen et al., CVPR 2024)、**EMAGE** (Liu et al., CVPR 2024)）过度依赖节奏特征，难以有效捕捉这些稀疏但语义关键的手势动作，导致生成的动作缺乏语义深度和表现力。SemTalk 正是针对这一瓶颈，通过语义门控 sem-gate 产生的帧级语义分数 $\psi$，动态调节语义动作的强调程度。

![[assets/figures/papers/paper_list_l1895_SemTalk_Holistic_Co_speech_Motion_Generation_with_Frame_level_Semantic_E/figures/001_Figure_1.jpg]]
*Figure 1: On the left, we analyze semantic labels from the BEAT2 dataset [31] and visualize frame-level motion, revealing that semantically relevant motions are rare and sparse, aligning with real-life observations. On the right, this observation drives the design of SemTalk, which establishes a rhythm-aligned base motion and dynamically emphasizes sparse semantic gestures at the frame-level. In this example, SemTalk amplifies expressiveness on words like “watching” and “just,” enhancing gesture and torso movements. The semantic scores below are automatically generated by SemTalk to modulate semantic emphasis over time*

### 主实验结果：BEAT2 与 SHOW 数据集上的全面领先

Table 1 报告了 SemTalk 与当前最先进方法的定量比较（置信度 0.98）。在 BEAT2 数据集上，SemTalk 在所有关键指标上均显著优于最强基线：

![[assets/figures/papers/paper_list_l1895_SemTalk_Holistic_Co_speech_Motion_Generation_with_Frame_level_Semantic_E/figures/011_Table_1.jpg]]
*Table 1: Quantitative comparison with SOTA. SemTalk consistently outperforms baselines across both the BEAT2 and SHOW datasets. Lower values are better for FMD, FGD, MSE, and LVD. Higher values are better for BC and DIV. We report*

- **FGD（Fréchet Gesture Distance）**：SemTalk 达到 **4.278**，显著低于所有竞争方法，表明生成动作的分布更接近真实数据。
- **MSE（Mean Squared Error）**：降至 **6.153**，体现了帧级重建精度的提升。
- **LVD（L2 Velocity Difference）**：降至 **6.938**，说明生成动作的速度动态更自然。
- **BC（Beat Consistency）** 和 **DIV（Diversity）**：分别达到 **7.770** 和 **12.91**，在节奏对齐和动作多样性之间取得了更好的平衡。

在 SHOW 数据集上，SemTalk 的 BC 达到 **8.304**，同样取得最高分。值得注意的是，与 **LivelySpeaker** (Zhi et al., ICCV 2023) 等将语义与节奏分离处理的方法相比，SemTalk 通过统一的自适应融合机制，避免了语义手势与节奏手势之间的抖动和不连贯问题（Figure 4）。

### 消融实验：语义门控机制的关键作用

**语义门控设计空间消融（Table 2）**

Table 2 系统消融了语义门控 sem-gate 的设计选择（置信度 0.98）：

![[assets/figures/papers/paper_list_l1895_SemTalk_Holistic_Co_speech_Motion_Generation_with_Frame_level_Semantic_E/figures/012_Table_2.jpg]]
*Table 2: Ablation study on Sem-gate. “Acc” denotes semantic classification performance on BEAT2. “w/o Sem-gate” means directly input*

1. **完全移除 sem-gate**：直接将文本特征 $f_t$ 和节奏特征 $\gamma_h$ 输入，不进行帧级语义强调，导致语义分类准确率（Acc）和 FGD 显著恶化。
2. **替换为 LivelySpeaker 的 SAG 模块**：性能大幅下降，证明 SemTalk 的 sem-gate 设计（多模态输入 + 双重加权）优于基于 CLIP 嵌入的全局语义注入方式。
3. **随机分配语义分数 $\psi$**：使用随机帧级分数替代学习到的 $\psi$，性能同样大幅下降，验证了学习到的语义分数包含有效信息。
4. **单一权重 vs. 双重权重**：仅使用特征加权 $W_f$ 或仅使用损失加权 $W_l$ 均不如同时使用两者（w/ $W_f$ + $W_l$）。SemTalk 的完整 sem-gate 整合了两种权重，在语义分类准确率和 FGD 上均取得最优结果。

**关键组件消融（Table 3）**

Table 3 消融了 SemTalk 的四个核心组件（置信度 0.98）：

![[assets/figures/papers/paper_list_l1895_SemTalk_Holistic_Co_speech_Motion_Generation_with_Frame_level_Semantic_E/figures/013_Table_3.jpg]]
*Table 3: Ablation study on each key component. “RC” denotes rhythmic consistency learning, “SE” denotes the semantic emphasis learning, and*

- **节奏一致性学习（RC）**：移除 RC 导致 FGD、BC 和 DIV 全面下降，证明局部帧级和全局序列级 InfoNCE 损失对维持节奏对齐至关重要。
- **语义强调学习（SE）**：移除 SE 后，动作的语义丰富度显著降低，BC 和 DIV 下降明显。
- **Coarse2Fine 交叉注意力模块（C2F）**：移除 C2F 后，BC、FGD 和 DIV 均恶化，验证了从面部到下肢的逐级细化策略对动作细节的积极贡献。
- **RVQ-VAE**：替换为标准 VAE 或移除量化层会导致重建质量和多样性下降。

每个组件单独移除都会造成性能损失，且完整模型在所有指标上取得最优，证明各组件的互补性。

### 定性分析与用户研究

**语义分数的可解释性（Figure 8）**：SemTalk 自动生成的语义分数 $\psi$ 与语音中的关键词（如“watching”“just”）对齐，并直接影响手势强度。这验证了 sem-gate 确实学到了有意义的帧级语义强调信号，而非过拟合到表面统计规律。

**情绪感知的运动多样性（Figure 9）**：即使文本脚本相同，SemTalk 也能根据语音中的不同情绪语调（emo）生成差异化的动作，避免了对文本本身的过拟合。这得益于 Sparse Motion Blocks 同时融合了帧级文本嵌入 $\phi_l$、句子级 CLIP 特征 $\phi_g$ 和 emotion2vec 情绪特征 $\phi_e$。

**用户研究（Figure 10）**：用户偏好结果进一步支持了定量指标的优势，参与者一致认为 SemTalk 生成的动作更自然、语义更丰富。

### 失败模式与局限性

尽管 SemTalk 在公开基准上取得了最优性能，但仍存在以下局限：

1. **标注依赖性**：sem-gate 的训练依赖 BEAT2 提供的帧级语义标签。对于无此类标注的数据集，需要额外的标签生成或迁移学习策略，这限制了方法的直接可迁移性。
2. **阈值敏感性**：语义分数阈值 $\beta$ 为经验设置（$\psi_i > \beta$ 时替换基础编码为稀疏语义编码），可能需针对不同说话人或数据分布进行调整，当前缺乏自适应阈值机制。
3. **文化与语言局限性**：实验仅在英文语音和单一文化背景的肢体语言上进行，尚未在跨语言或跨文化场景下验证运动分解和语义强调策略的泛化性。

### 公平性说明

所有实验在公开数据集 BEAT2 和 SHOW 上进行，训练/验证/测试划分遵循 EMAGE (Liu et al., CVPR 2024) 约定。评估指标涵盖 FGD、BC、DIV、MSE、LVD，并补充了用户研究。对比方法均使用官方实现或统一实验设置，确保比较的公平性。

### 补充图表

![[assets/figures/papers/paper_list_l1895_SemTalk_Holistic_Co_speech_Motion_Generation_with_Frame_level_Semantic_E/figures/009_Figure_8.jpg]]
*Figure 8: Qualitative study on semantic score. Semantic score aligns with keywords, influencing gesture intensity*

![[assets/figures/papers/paper_list_l1895_SemTalk_Holistic_Co_speech_Motion_Generation_with_Frame_level_Semantic_E/figures/007_Figure_9.jpg]]
*Figure 9: Same words with different speech from the internet. “emo” represents different emotional tones extracted from speech. SemTalk can generate different motions, even when the text script is the same, preventing overfitting to the text itself*

![[assets/figures/papers/paper_list_l1895_SemTalk_Holistic_Co_speech_Motion_Generation_with_Frame_level_Semantic_E/figures/010_Figure_10.jpg]]
*Figure 10: Results of the user study*

## 方法谱系与知识库定位

### 1. 与现有方法的谱系关系

**SemTalk** 处于协同语音手势生成任务中“节奏-语义解耦”这一新兴技术路线。其核心创新在于将整体运动显式分解为节奏对齐的基础运动（Base Motion）和语义感知的稀疏运动（Sparse Motion），并通过帧级语义门控（sem-gate）实现自适应融合。这一设计直接回应了现有方法过度依赖节奏特征、难以捕捉稀疏语义手势的瓶颈。

与代表性基线方法的关系如下：

- **TalkSHOW** (Yi et al., CVPR 2023)：基于 VQ-VAE 的整体运动生成方法，未显式建模语义与节奏的分离。SemTalk 在运动编码阶段即引入分解，使语义信息在隐空间中获得独立建模通道。
- **LivelySpeaker** (Zhi et al., ICCV 2023)：同样尝试结合语义与节奏，但其采用分离式的两阶段处理——先通过 SAG 模块生成语义手势，再通过扩散模型细化节奏手势。这种分离导致语义与节奏信息融合不充分，可能产生动作抖动（jitter）。SemTalk 通过 sem-gate 在帧级别统一调控语义强调程度，避免了分阶段处理带来的不一致性。Figure 4 明确展示了这一概念差异。
- **DiffSHEG** (Chen et al., CVPR 2024) 与 **EMAGE** (Liu et al., CVPR 2024)：分别为基于扩散和掩码建模的整体方法，均未引入帧级语义分数机制。SemTalk 的语义门控提供了更细粒度的控制能力。
- **ProbTalk** (Liu et al., CVPR 2024)：基于 PQ-VAE 的可变协调方法，关注运动多样性但未针对语义稀疏性进行专门设计。

从知识库定位来看，SemTalk 贡献了三个可迁移的机制槽位：**(1) 运动表示分解**（基础/稀疏运动分离）、**(2) 帧级语义门控**（sem-gate + 双重加权）、**(3) 分层节奏传递**（Coarse2Fine Cross-Attention）。这些机制可为后续的语音驱动人体动画、音乐驱动舞蹈合成等任务提供参考框架。

### 2. 适用边界与假设

SemTalk 的有效性建立在以下关键假设之上：

- **帧级语义标签可用性**：语义门控的训练依赖 BEAT2 数据集提供的帧级语义标注。对于无此类标注的数据集，需要额外的标签生成策略或迁移学习方法，这构成方法推广的主要障碍。
- **语义分数阈值 β 的经验性**：运动融合阶段使用的阈值 β 为经验设定，其最优值可能随数据集、说话人风格变化。论文未提供 β 的敏感性分析，实际部署时可能需要针对具体场景调优。
- **单一语言与文化背景**：当前验证仅覆盖英文语音和对应的肢体语言习惯。跨语言（如声调语言）或跨文化场景下的手势语义模式可能显著不同，方法的泛化性尚未得到验证。
- **语音-文本联合依赖**：语义门控同时利用语音特征（emotion2vec）和文本特征（CLIP），在仅语音或仅文本的场景下性能可能退化。

### 3. 局限性与开放问题

**已知局限**：
1. **语义边界定义的模糊性**：帧级语义标签本身存在标注噪声和边界模糊问题。sem-gate 学习到的语义分数 ψ 可能与人类感知的语义手势边界存在偏差，导致语义强调的过度或不足。
2. **对标注数据的强依赖**：语义强调学习（SE）需要帧级语义真值进行监督，限制了方法向大规模无标注语音数据扩展的能力。
3. **阈值调优的自动化缺失**：β 的手动设定方式缺乏自适应机制，难以应对不同说话风格或情绪强度下的语义表达需求。

**开放问题**：
1. **无监督/弱监督语义强调**：能否在仅利用语音-运动对齐信号的条件下，通过对比学习或互信息最大化等方式隐式学习帧级语义重要性，从而摆脱对语义标签的依赖？
2. **语义动作边界的精确定义**：如何更精确地定义和评估“语义动作”的起止帧？这涉及语言学、认知科学与人机交互的交叉研究。
3. **跨模态扩展**：SemTalk 的运动分解思想——节奏基础运动 + 语义/表现力稀疏运动——是否可迁移至音乐驱动的舞蹈合成？音乐中的节拍与旋律高潮可能对应类似的“节奏-表现力”分解结构。
4. **实时性与交互性**：当前框架为离线生成设计。在对话系统等实时场景中，语义门控的帧级预测需要因果约束（仅依赖历史信息），其性能退化程度值得研究。
5. **多说话人风格建模**：sem-gate 当前未显式建模个人手势风格差异。引入说话人相关的语义强调偏好可能进一步提升个性化表现。

## 原文 PDF

![[paperPDFs/ICCV_2025/SemTalk_Holistic_Co_speech_Motion_Generation_with_Frame_level_Semantic_Emphasis.pdf]]
