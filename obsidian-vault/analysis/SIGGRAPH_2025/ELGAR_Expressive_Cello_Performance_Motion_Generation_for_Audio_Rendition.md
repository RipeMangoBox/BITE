---
title: "ELGAR: Expressive Cello Performance Motion Generation for Audio Rendition"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/ELGAR_Expressive_Cello_Performance_Motion_Generation_for_Audio_Rendition.pdf
project_link: "https://s2025.conference-schedule.org/presentation/?id=papers_1381&sess=sess150"
code_link: "https://github.com/Qzping/ELGAR"
aliases:
- ELGAR
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
core_operator: 基于音频信号的交互接触损失（HICL和BICL），通过领域知识约束手指按压位置与弓弦接触点的空间关系，有效保证了演奏动作的物理真实性和交互一致性。
primary_logic: 将弦乐器演奏领域的物理约束（手指按弦、弓弦接触）显式建模为扩散模型的附加损失项，同时利用预训练音频特征与交叉注意力机制的DiT架构，能够从原始音频中重建出具有丰富表现力和准确性的全身大提琴演奏动作。
claims:
- 消融实验表明，同时使用HICL和BICL时，手指接触距离（FCD）降至15.60 mm，弓弦距离（BSD）降至5.40 mm，弓法F1分数提升至0.4721，余弦相似度提升至0.7515，均优于去掉任一损失或仅使用几何损失。
- 定性比较（Figure 5）显示，加入交互接触损失后，弓和左手与弦的相对位置更加准确合理，消除了未加损失时的明显位置偏差。
- SPD-GEN 上 Finger-Contact Distance (FCD, mm, ↓) = 15.60
- SPD-GEN 上 Bow-String Distance (BSD, mm, ↓) = 5.40
---

# ELGAR: Expressive Cello Performance Motion Generation for Audio Rendition

> [!tip] 核心洞察
> 将弦乐器演奏领域的物理约束（手指按弦、弓弦接触）显式建模为扩散模型的附加损失项，同时利用预训练音频特征与交叉注意力机制的DiT架构，能够从原始音频中重建出具有丰富表现力和准确性的全身大提琴演奏动作。

| 字段 | 内容 |
|------|------|
| 中文题名 | ELGAR: 面向音频再现的表现性大提琴演奏动作生成 |
| 英文题名 | ELGAR: Expressive Cello Performance Motion Generation for Audio Rendition |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](http://arxiv.org/abs/2505.04203v2) · [Code](https://github.com/Qzping/ELGAR) · [Project](https://s2025.conference-schedule.org/presentation/?id=papers_1381&sess=sess150) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion |
| Method | ELGAR |
| Dataset | SPD-GEN |

> [!tip] 效果简介
> - SPD-GEN 上，Finger-Contact Distance (FCD, mm, ↓) 15.60 vs 37.33 (w/o HICL & BICL) (-21.73)；Bow-String Distance (BSD, mm, ↓) 5.40 vs 11.10 (w/o HICL & BICL) (-5.70)；Bowing F1-Score (BF1, ↑) 0.4721 vs 0.3685 (w/o HICL & BICL) (+0.1036)。

## 概要

现有乐器演奏动作生成方法仅关注局部身体运动，忽略手-弓-弦之间的精细交互，且无法从连续音频端到端地生成全身演奏动作，导致物理合理性与交互真实性存在缺陷。针对此瓶颈，本文提出 **ELGAR**——一种基于扩散模型的端到端框架，从原始音频直接生成全身大提琴演奏动作。核心创新在于引入了**手部交互接触损失（HICL）** 与**弓交互接触损失（BICL）**，将弦乐器演奏的领域物理约束显式建模为扩散模型的附加损失项，确保手指按弦位置与弓弦接触点的空间关系准确。架构上采用冻结的 Jukebox 提取音频特征，通过交叉注意力集成到 DiT 去噪块中。在自建的 SPD-GEN 数据集上，同时使用 HICL 和 BICL 使手指接触距离降至 15.60 mm，弓弦距离降至 5.40 mm，弓法 F1 分数提升至 0.4721，显著优于未加交互损失的基线。该方法为音频驱动的表现性乐器演奏动作生成提供了物理约束显式建模的新范式。

## 核心方法与创新机理

### 瓶颈与核心机制

现有乐器演奏动作生成方法（如音乐驱动的舞蹈或手势合成）仅关注局部身体运动，忽略了弦乐器演奏中**手-弓-弦之间的精细交互**，导致生成结果在物理合理性和交互真实性上存在根本缺陷。ELGAR 的核心突破在于将大提琴演奏的领域物理约束显式建模为扩散模型的附加损失项——**手部交互接触损失 (HICL)** 与 **弓交互接触损失 (BICL)**，从连续音频端到端地生成全身演奏动作。

### 关键创新点

**1. 交互接触损失 (Interactive Contact Loss, ICL)**

这是本文最核心的方法创新，包含两个互补的损失项：

- **HICL**：约束左手手指与琴弦的接触关系。对于当前音符对应的按弦手指，强制其指尖位置尽可能靠近音频指定的按弦点；对于其他非演奏手指，则要求它们与按弦点保持合理的空间关系（而非任意离散）。损失通过音频基频 $f_0$ 计算得到的指示矩阵 $I_{f_0}$ 进行加权，仅在有效音符区域激活。

- **BICL**：约束弓与琴弦的交互。一方面确保弓与当前激活的琴弦保持接触，另一方面约束弓的两端（弓根与弓尖）与琴弦保持合理的距离关系，防止弓过度偏离或穿透琴弦。

两项损失均直接利用 SPD 数据集中已有的音频标注信息（音符起止时间、基频 $f_0$），无需额外的人工标注。

**2. 基于 DiT 的音频条件扩散框架**

ELGAR 采用 **DiT (Diffusion Transformer)** 作为去噪骨干网络（8 个 DiT 块，adaLN-Zero 归一化，约 55M 参数），替代传统基于 U-Net 的扩散模型。音频条件通过**冻结的 Jukebox 模型**提取特征，经**交叉注意力机制**注入每个 DiT 块的去噪过程。这种设计使模型能够从原始音频中捕获丰富的音色、音高和表现力信息，同时保持训练效率。

**3. 运动表示与数据标准化**

模型输出 309 维运动表示 $\mathbf{x} = \{\mathbf{r}, \hat{\mathbf{v}}\} \in \mathbb{R}^{309}$，其中 $\mathbf{r}$ 为身体和手部的 6D 旋转表示（306 维），$\hat{\mathbf{v}}$ 为弓的方向向量（3 维）。数据预处理阶段通过大提琴归一化（统一到手动标注的共享乐器模型）和人体逆运动学（基于 SMPL-X 和 VPoser 的两阶段 IK）消除演奏者体型差异，使模型专注于学习演奏动作本身的模式。

### 关键公式

**扩散过程**（前向加噪）：
$$q(x_t | x_0) = \sqrt{\bar{\alpha}_t} x_0 + \epsilon \sqrt{1 - \bar{\alpha}_t}, \quad \epsilon \sim \mathcal{N}(0,1)$$

**训练损失**（简单 MSE + 几何约束 + 交互接触）：
$$\mathcal{L}_{simple} = \mathbb{E}_{t \sim [1,T], x_t \sim q} [\| f_\theta(x_t, t, c) - x_0 \|]$$

其中 $f_\theta$ 为 DiT 网络，$c$ 为音频条件。推理时采用无分类器引导 (CFG)，引导强度 $w$ 控制条件与无条件预测的混合比例。

**手部交互接触损失 (HICL)**：
$$\mathcal{L}_{hand} = \mathbb{1}_{note} \| \hat{d}_{cp} \odot I_{f_0} \|_2^2 + \mathbb{1}_{others} \| (\hat{d}_{cp} - d_{cp}) \odot I_{f_0} \|_2^2$$

其中 $\hat{d}_{cp}$ 为预测的手指到按弦点的距离，$d_{cp}$ 为真实距离，$I_{f_0}$ 为基于基频的激活掩码。第一项强制演奏手指接触按弦点，第二项维持非演奏手指的合理空间分布。

**弓交互接触损失 (BICL)**：
$$\mathcal{L}_{bow} = \| \hat{d}_{l_s, l_b} \odot I_{f_0} \|_2^2 + \| (\hat{d}_{p, l_s} - d_{p, l_s}) \odot I_{f_0} \|_2^2$$

第一项约束弓与激活弦的接触距离，第二项约束弓端点与弦的相对位置关系。两项均仅在音符激活区域生效。

### 方法边界与假设

- **静态乐器假设**：模型假设大提琴在演奏过程中保持静止，忽略实际演奏中乐器的微小晃动，这可能在某些动态场景中产生不自然的效果。
- **数据依赖**：ICL 损失依赖 SPD 数据集提供的音符级标注（$f_0$、音符起止时间），扩展到无标注数据集时需要额外的音频分析模块。
- **单乐器限定**：当前方法针对大提琴设计，扩展到其他弦乐器（如小提琴）需要重新定义弓-弦交互的几何关系。
- **无乐谱条件**：模型仅利用音频信号，未使用乐谱或 MIDI 等符号信息，可能在音乐结构精确性上存在局限。

## 实验与关键发现

### 主结果：交互接触损失的决定性作用

ELGAR 的核心实验围绕所提出的**手部交互接触损失（HICL）**和**弓交互接触损失（BICL）**展开消融研究，以验证其对生成动作物理真实性的贡献。Table 1 报告了在 SPD-GEN 数据集上的四项关键指标：

![[assets/figures/papers/paper_list_l10_http_arxiv_org_abs_2505_04203v2/figures/006_Table_1.jpg]]
*Table 1: Ablation study showing the impact of including or excluding HICL and BICL on the generated results across the metrics of Finger-Contact Distance (FCD, in mm), Bow-String Distance (BSD, in mm), Bowing F1-Score (BF1), and Bowing Cosine Similarity (BCS). Bold indicates best result*

| 配置 | FCD (mm, ↓) | BSD (mm, ↓) | BF1 (↑) | BCS (↑) |
|------|-------------|-------------|---------|---------|
| 无 HICL & BICL | 37.33 | 11.10 | 0.3685 | 0.6438 |
| 仅 HICL | 18.33 | 6.89 | — | — |
| **完整 ICL (HICL + BICL)** | **15.60** | **5.40** | **0.4721** | **0.7515** |

完整 ICL 配置下，手指接触距离（FCD）从 37.33 mm 降至 15.60 mm（降幅 58.2%），弓弦距离（BSD）从 11.10 mm 降至 5.40 mm（降幅 51.4%），弓法 F1 分数提升 0.1036，弓法余弦相似度提升 0.1077。这表明 HICL 和 BICL 的联合约束是保证手-弓-弦交互精度的关键。

### 消融分析：损失项的独立与协同效应

单独引入 HICL 已能显著改善手指定位：FCD 从 37.33 降至 18.33 mm，BSD 也从 11.10 降至 6.89 mm，说明手部接触损失对弓弦距离存在间接的正则化效应。单独引入 BICL 则主要提升弓法相关指标（BF1 和 BCS）。然而，**仅当 HICL 和 BICL 同时启用时，四项指标才全部达到最优**，证明了两类物理约束之间存在协同作用——手指按弦的准确性为弓法执行提供了稳定的空间参照，反之亦然。

定性对比（Figure 5）进一步验证了这一结论：未使用 ICL 时，弓和左手相对于琴弦存在明显且不真实的位置偏差；引入 ICL 后，弓与左手的交互更加准确合理，与预期演奏位置高度一致。

![[assets/figures/papers/paper_list_l10_http_arxiv_org_abs_2505_04203v2/figures/005_Figure_5.jpg]]
*Figure 5: In this figure, we present a comparative demonstration of the bow and left hand motions before and after the introduction of the Interactive Contact Loss (ICL), highlighting its significant impact. Prior to adopting ICL, both the bow and the left hand exhibited noticeable and unrealistic positional deviations relative to the strings. Following the integration of ICL, the bow and the left hand display more accurate and reasonable interactions with the strings, aligning closely with the intended playing positions*

### 关键设计决策的验证

除损失函数外，架构层面的两个设计选择也通过实验得到间接验证：

1. **DiT 骨干网络**：采用 8 个 DiT 块（55M 参数）配合 adaLN-Zero 归一化，替代传统 U-Net 扩散模型，为音频条件注入提供了更灵活的交叉注意力接口。
2. **冻结 Jukebox 音频特征**：通过交叉注意力机制将预训练音频特征集成到去噪过程，使模型能够从原始音频中提取与演奏动作相关的语义信息，而无需端到端训练音频编码器。

### 失败模式与适用边界

尽管 ICL 显著提升了交互精度，实验仍揭示了若干局限性：

- **弓弦接触不稳定**：即使引入 BICL，弓偶尔仍会失去与琴弦的接触。这表明基于损失函数的软约束无法完全替代硬性的物理接触保证，在长时间采样中尤为明显。
- **上下文感知不足**：长时间序列生成中，模型对远距离上下文的感知有限，导致在持续段落中出现不自然的弓转换。这是扩散模型在长序列建模中的共性瓶颈。
- **静态大提琴假设**：模型假设大提琴位置固定，忽略了实际演奏中乐器的微小运动，可能在动态演奏场景中产生不自然的身体-乐器相对关系。

此外，SPD-GEN 数据集仅包含 81 首曲目，演奏风格多样性有限，模型在未见风格上的泛化能力尚需进一步验证。评估指标主要聚焦于物理接触精度和弓法正确性，对整体动作的审美质量和音乐表现力缺乏量化衡量——这需要人工评估或新的感知指标来补充。

### 实验公平性说明

SPD-GEN 数据集通过人体归一化处理（包括大提琴对齐和基于 SMPL-X 的两阶段逆运动学求解）消除了演奏者身高和体型差异的影响，确保消融对比的公平性。所有消融实验在相同的数据划分和训练配置下进行，指标计算基于统一的接触判定阈值。

![[assets/figures/papers/paper_list_l10_http_arxiv_org_abs_2505_04203v2/figures/001_Figure_1.jpg]]
*Figure 1: ELGAR is capable of generating cello performance motion with precise details and complicated interactions solely from audio*

![[assets/figures/papers/paper_list_l10_http_arxiv_org_abs_2505_04203v2/figures/003_Figure_3.jpg]]
*Figure 3: Given performance audio, ELGAR employs DiT blocks with adaLN-Zero to denoise the performance motions from ???? to ??0, incorporating cross-attention to further integrate audio features extracted by a frozen Jukebox [Dhariwal et al. 2020]. The upper-right details the Interactive Contact Loss (ICL). The orange solid lines represent the "contact" of ICL; while the gray dashed lines show the "interactive" relationship between the non-playing fingers and the contact point, as well as between the bow endpoints and the activating string. The Red dot marks the contact position of the hand, and the blue-highlighted string denotes the activating string. For the hand, the note-playing finger should st...*

![[assets/figures/papers/paper_list_l10_http_arxiv_org_abs_2505_04203v2/figures/002_Figure_2.jpg]]
*Figure 2: Top: We position the starting point of the bow (frog) at the midpoint between the PIP and DIP joints of the middle finger, ring finger, and thumb (highlighted in red). Bottom: As shown in (b), SPD-GEN reconstructs the arched cello bridge, unlike the flat bridge in SPD, closely matching the actual instrument illustrated in (c). This enables the performer to play the two middle strings without unintended contact with adjacent ones, thereby avoiding potential penetration artifacts as seen in (a). The red dot in (a) and (b) indicates the bow-string contact point*

## 定位与知识库关联

ELGAR 在乐器演奏动作生成领域的核心定位是：**首次将弦乐器演奏中的手-弦-弓物理交互约束显式建模为扩散模型的损失函数**，实现了从原始音频端到端生成全身大提琴演奏动作。这与现有工作的本质差异体现在三个层面。

**与音频驱动人体运动生成的差异。** 现有音频驱动运动生成方法（如 Bailando、EDGE 等）主要面向舞蹈或上肢手势，关注的是动作与音乐节奏、风格的对齐，而非物理交互的精确性。ELGAR 将问题从“风格对齐”推向了“物理约束满足”——生成的左手手指必须按压到正确的弦位置，弓必须接触正确的弦。这一转变要求模型不仅理解音频的语义信息，还要将其映射到高度约束的物理空间关系中。

**与乐器演奏动作生成的差异。** 此前的方法（如 SPD 相关工作的运动重建部分）多关注局部身体运动（躯干或手部），且通常依赖运动捕捉数据的直接重建，而非从音频条件生成。ELGAR 的关键突破在于设计了 **手部交互接触损失（HICL）** 和 **弓交互接触损失（BICL）**，这两个损失项利用 SPD 数据集中已有的音频标注信息（音符、激活弦），将领域知识转化为可微分的约束：HICL 强制按弦手指接触音频指定的位置，同时约束其他手指维持合理的空间关系；BICL 强制弓与激活弦接触，并保持弓两端与弦的合理距离。消融实验（Table 1）表明，仅使用几何损失时，手指接触距离（FCD）为 37.33 mm，弓弦距离（BSD）为 11.10 mm；同时加入 HICL 和 BICL 后，FCD 降至 15.60 mm，BSD 降至 5.40 mm，弓法 F1 分数从 0.3685 提升至 0.4721。定性对比（Figure 5）进一步显示，未使用交互接触损失时，弓和左手相对于弦存在明显且不真实的位置偏差，加入后交互的准确性和合理性显著改善。

**与扩散模型架构设计的关联。** ELGAR 采用 DiT（Peebles & Xie, ICCV 2023）作为去噪骨干，通过 adaLN-Zero 归一化和交叉注意力机制集成冻结的 Jukebox（Dhariwal et al., NeurIPS 2020）音频特征，参数量为 55M。这一架构选择与 MotionDiffuse、MDM 等人体运动扩散模型共享技术路线，但 ELGAR 的独特之处在于将领域特定的物理约束作为附加损失注入扩散训练过程，而非仅依赖数据驱动的模式学习。

**知识库挂载点与适用边界。** ELGAR 的核心贡献可挂载到三个知识节点：(1) **音频条件运动生成**——证明了冻结的大规模音频预训练模型（Jukebox）特征对精细演奏动作生成的有效性；(2) **物理约束扩散模型**——提供了将领域知识作为可微损失注入扩散训练的一般范式；(3) **弦乐器演奏建模**——SPD-GEN 数据集对琴桥的拱形重建（Figure 2）和弓起始点的定位策略，为后续弦乐器研究提供了数据处理基准。

**适用边界与局限。** 模型假设大提琴为静态物体，忽略了实际演奏中乐器的微小运动；SPD-GEN 数据集仅包含 81 首曲目，风格多样性有限；长时间序列采样中存在上下文感知不足导致的弓转换不自然问题；模型仅利用音频信号，未利用乐谱等符号信息。这些边界条件意味着 ELGAR 适用于中等长度的独奏大提琴演奏生成，但在合奏场景、其他弦乐器泛化、实时应用等方面仍需进一步验证。

**后续启发。** 该工作的交互接触损失设计范式可推广至其他弦乐器（如小提琴、中提琴），甚至扩展到需要精细工具交互的领域（如手术模拟、精细操作机器人）。将乐谱或 MIDI 等多模态信息与音频融合，有望解决音乐结构层面的精确性问题。此外，探索更鲁棒的接触保证策略（如硬约束或强化学习）可能解决弓偶尔失去接触的问题。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/ELGAR_Expressive_Cello_Performance_Motion_Generation_for_Audio_Rendition.pdf]]