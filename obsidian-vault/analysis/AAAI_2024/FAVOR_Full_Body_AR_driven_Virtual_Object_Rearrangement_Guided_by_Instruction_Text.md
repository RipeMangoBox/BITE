---
title: FAVOR Full Body AR driven Virtual Object Rearrangement Guided by Instruction Text
type: paper
paper_level: A
venue: AAAI
year: 2024
pdf_ref: paperPDFs/AAAI_2024/FAVOR_Full_Body_AR_driven_Virtual_Object_Rearrangement_Guided_by_Instruction_Text.pdf
aliases:
- FFBADVORGBIT
tags:
- AAAI_2024
- topic/other_unclear
- topic/other_unclear/general
core_operator: 引入AR眼镜与光学动捕系统集成的数据采集平台，并设计两阶段框架——场景‑语言接地（GPT‑4+Owl‑ViT多视角定位）与动作重排生成（CVAE关键帧抓取+内插网络），从而将文本指令与场景理解结合，生成符合物理约束的全身重排动作。
primary_logic: 利用AR眼镜提供实时视觉反馈可以高效采集高质量虚拟物体交互动作；通过结合大型语言模型、视觉‑语言检测器和多视角几何，能够直接从自然语言指令定位物体的抓取与放置位置；将动作生成分解为关键帧抓取和运动内插既降低了学习难度，又保证了序列的连贯性与准确性。
claims:
- FAVOR数据集包含3千段重排序列、717万帧交互数据，涵盖1800种物体模型，是目前最大的带文本指令的全身物体重排数据集。
- 感知研究表明，FAVOR数据集中的动作在自然度、抓取合理性和物理一致性上获得志愿者一致认可。
- KNET生成的关键帧抓取在接触率（CR=0.93）和固体交集体积（SIV=6.50）上接近真实抓取（CR=0.99, SIV=0.83），验证了其有效性。
- 消融实验表明，基于SDF的物体穿透损失（Eq.6）将穿透体积从11.81显著降至6.50，证明了物理约束的必要性。
---

# FAVOR Full Body AR driven Virtual Object Rearrangement Guided by Instruction Text

> [!tip] 核心洞察
> 利用AR眼镜提供实时视觉反馈可以高效采集高质量虚拟物体交互动作；通过结合大型语言模型、视觉‑语言检测器和多视角几何，能够直接从自然语言指令定位物体的抓取与放置位置；将动作生成分解为关键帧抓取和运动内插既降低了学习难度，又保证了序列的连贯性与准确性。

| 字段 | 内容 |
|------|------|
| 中文题名 | FAVOR：全身AR驱动的指令文本引导虚拟物体重排 |
| 英文题名 | FAVOR Full Body AR driven Virtual Object Rearrangement Guided by Instruction Text |
| 会议/期刊 | AAAI 2024 |
| Links | [Project](https://kailinli.github.io/FAVOR) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | FAVORITE |
| Dataset | Perceptual Study, Grasp Quality |

> [!tip] 效果简介
> - Perceptual Study (Likert scale) 上，Average Likert score (↑) 3.85 ± 1.04 (生成动作) vs 4.62 ± 0.54 (FAVOR数据集真值) (-0.77)。
> - Grasp Quality 上，CR↑ / SIV↓ 0.93 / 6.50 (KNET在初始物体姿态下) vs 0.99 / 0.83 (FAVOR数据集抓取GT) (CR: -0.06, SIV: +5.67)。

## 概述

**核心问题**：现有的人-物交互数据集普遍缺乏大规模、全身、场景多样化且附带自然语言指令的物体重排数据，导致从文本指令直接生成连贯、物理合理的全身重排动作面临瓶颈。同时，现有方法在复杂场景下难以准确解析指令语义并生成流畅的抓取与放置动作。

**核心洞察**：本文提出利用AR眼镜提供实时虚拟物体视觉反馈，结合光学运动捕捉系统，构建高效、高质量的数据采集平台；并设计两阶段框架FAVORITE，将场景-语言接地与动作重排生成解耦，借助大型语言模型、视觉-语言检测器与多视角几何实现从自然语言指令到物体定位，再通过CVAE关键帧生成与运动内插网络生成符合物理约束的全身动作序列。

**方法定位**：FAVORITE在数据采集方式上以AR眼镜+动捕替代传统真实物体交互或纯合成数据；在指令解析上以GPT‑4+Owl‑ViT多视角定位替代直接文本编码；在动作生成框架上以分阶段CVAE关键帧抓取+运动内插替代端到端生成。消融实验表明，基于SDF的物体穿透损失（Eq. 6）将固体交集体积从11.81降至6.50，验证了物理约束的必要性；使用**FLEX**（Tendulkar et al., CVPR 2023）替代专有的KNET生成关键帧抓取时，近半数尝试失败，说明针对桌面重排场景的专用训练至关重要。

**主要结果**：FAVOR数据集包含3千段重排序列、717万帧交互数据，涵盖1800种物体模型，是当前最大的带文本指令的全身物体重排数据集（Table 1）。感知研究表明，生成动作在自然度、抓取合理性和物理一致性上获得志愿者一致认可（平均Likert评分3.85±1.04，真实数据为4.62±0.54）。KNET生成的关键帧抓取在接触率（CR=0.93）和固体交集体积（SIV=6.50）上接近真实抓取（CR=0.99, SIV=0.83），验证了其有效性。

**局限与开放问题**：AR眼镜缺乏触觉反馈可能影响抓取自然度；数据集动作风格多样性有限；指令解析依赖预定义模板，对复杂指令泛化能力受限；实验场景主要集中在桌面堆放，尚未覆盖更开放的动态环境。未来工作可探索引入触觉反馈、扩展场景多样性，以及将场景-语言接地模块扩展到长时间连续规划任务中。

## 背景与动机

### 问题背景：从指令到全身物体重排动作的生成

物体重排（Object Rearrangement）是具身智能与虚拟人交互中的核心任务之一。其目标是根据自然语言指令，将场景中的物体从初始位置移动到指定的目标位置，并生成相应的全身抓取与放置动作序列。这一能力在增强现实（AR）、机器人学习、数字人动画以及沉浸式训练场景中具有广泛的应用前景。

然而，从文本指令直接生成自然、物理合理的全身重排动作面临双重挑战。一方面，系统需要准确理解指令中隐含的空间语义，将“把蓝色杯子放到红色盘子右边”这样的自然语言映射为场景中具体物体的三维位置；另一方面，系统需要生成符合人体运动学、物理约束且视觉上自然的抓取、搬运与放置动作序列。这两者的耦合使得该任务成为一个典型的跨模态、跨层级生成问题。

### 现有方法的缺口：数据、解析与动作生成的断层

已有工作在物体重排的三个关键环节上均存在明显缺口。

**数据缺口**：现有的人体运动数据集（如GRAB、SAMP）要么缺乏文本指令标注，要么仅覆盖手部交互而忽略全身运动，要么场景多样性有限且物体数量稀少。如Table 1所示，此前没有任何数据集同时满足“全身动作捕捉”“文本指令标注”“多样化物体模型”和“大规模交互序列”这四个条件。这直接限制了数据驱动方法的学习能力——缺乏大规模、全身、场景多样化且带文本指令的物体重排交互数据，使得从指令生成自然重排动作的能力受到根本性制约。

**指令解析缺口**：在将自然语言指令与三维场景关联方面，现有方法通常采用直接的文本编码或简单的指令模板，难以处理包含空间关系、物体属性与目标位置的复杂指令。当场景中存在多个相似物体或物体之间存在遮挡时，仅靠单视角视觉语言模型难以实现精确的三维定位。

**动作生成缺口**：现有动作生成方法多采用端到端的单阶段框架，试图直接从指令映射到完整的运动序列。这种设计在面对需要精确抓取与稳定放置的物体重排任务时，往往难以同时保证抓取姿态的准确性与运动序列的连贯性。此外，大多数方法未显式建模手部与物体之间的物理约束（如穿透、接触稳定性），导致生成的抓取动作在物理上不可行。

### 本文动机：AR驱动的数据采集与两阶段生成框架

针对上述三重缺口，本文提出了一套完整的解决方案——**FAVOR**（Full-body AR-driven Virtual Object Rearrangement）数据集与**FAVORITE**生成框架。

在数据层面，本文设计了一种创新的数据采集平台，将光学运动捕捉系统（MoCap）与AR眼镜集成。AR眼镜向受试者提供虚拟物体的实时视觉反馈，使其能够在无实物的情况下自然地执行抓取与放置动作。这一设计将单段序列的后处理时间从传统MoCap的45分钟以上压缩至约3分钟，使得大规模数据采集成为可能。最终构建的FAVOR数据集包含3千段重排序列、717万帧交互数据，涵盖1800种物体模型，是目前最大的带文本指令的全身物体重排数据集。

在方法层面，本文提出FAVORITE两阶段框架。第一阶段为**场景‑语言接地**（Scene-Language Grounding），利用GPT‑4将自然语言指令解析为结构化的定位函数，结合Owl‑ViT视觉‑语言检测器与多视角几何，精确获取物体的初始与目标三维位置。第二阶段为**运动重排生成**（Motion Rearrangement Generation），将动作生成分解为关键帧抓取（CVAE生成抓取与放置姿态）与运动内插（INET生成连贯序列）两个子任务，既降低了学习难度，又通过物理约束优化保证了序列的物理合理性。

这一“数据‑方法”协同设计，从根源上回应了现有工作的三个断层：AR数据采集填补了数据缺口，GPT‑4+多视角几何填补了解析缺口，分阶段生成+物理约束填补了动作生成缺口。

## 核心创新

FAVORITE框架的核心创新并非单一技术的突破，而是围绕“从指令文本生成全身虚拟物体重排动作”这一目标，在**数据采集范式**与**两阶段生成框架**上进行了系统性重构。以下从三个关键维度展开分析。

### 1. 数据采集范式变革：从真实/合成数据到AR驱动的全身交互采集

传统物体交互数据集或依赖真实物体操作（缺乏大规模文本标注），或采用纯合成渲染（缺乏真实人体运动学特征）。FAVOR提出的采集平台（Figure 2）首次将**光学动捕系统**与**AR眼镜**深度集成，形成了闭环反馈的采集范式：

- **因果机制**：AR眼镜将虚拟物体实时叠加到物理场景中，受试者可在看到虚拟物体的同时执行自然抓取与放置动作；动捕系统以120 fps记录全身SMPL-X参数（$\beta \in \bar{\mathbb{R}}^{10}$, $\pmb{\theta} \in \mathbb{R}^{55 \times 3}$, $t \in \mathbb{R}^3$）以及物体轨迹 $\tau_{\mathcal{O}}^{0:T}$。这一设计直接解决了“如何让人类自然地与虚拟物体交互”这一瓶颈——AR提供的实时视觉反馈使受试者能够像操作真实物体一样调整手部姿态，从而产生物理上合理的接触与抓取动作。
- **证据强度**：Table 1显示，FAVOR数据集包含3K条重排序列、7.17M帧交互数据、1800种物体模型，是目前**最大规模的带文本指令全身物体重排数据集**。与传统动捕相比，AR采集将单序列后处理时间从45分钟以上降至约3分钟（15倍加速），这为大规模数据构建提供了可行性基础。

### 2. 指令解析机制变革：从简单文本编码到LLM+VLM的多视角场景‑语言接地

现有方法通常将文本指令直接编码为条件向量，缺乏对场景中物体空间位置的精确解析能力。FAVORITE的**Scene-Language Grounding**模块（Figure 4）引入了“LLM解析+VLM检测+多视角几何定位”的级联机制：

- **因果机制**：GPT‑4首先将自然语言指令解析为结构化输出（目标物体 $\mathcal{O}$、放置介词如“on top of”、参照物等），随后生成模板化的`locate`函数调用。该函数通过多视角渲染获取场景图像，利用**Owl‑ViT**进行开放词汇物体检测，最后通过**多视图几何**恢复物体的三维初始位置 $T_{\mathcal{O}}^{\mathcal{G}}$ 和最终位置 $T_{\mathcal{O}}^{\mathcal{P}}$。这一设计将“语言理解”与“三维空间定位”解耦，使LLM专注于语义解析，而VLM与几何计算负责精确的空间推理。
- **证据强度**：该模块的定位精度直接支撑了后续关键帧生成——KNET在初始物体姿态下生成的抓取姿态接触率（CR）达到0.93，接近数据集真值（0.99），表明场景‑语言接地为动作生成提供了可靠的空间锚点。但需注意，当前`locate`模板对复杂非模板化指令的泛化能力有限，这是该模块的已知局限。

### 3. 动作生成框架变革：从端到端生成到关键帧抓取+运动内插的分阶段架构

端到端生成全身重排动作面临两大难题：抓取姿态的高精度要求与长序列运动的时间一致性难以同时满足。FAVORITE将生成过程分解为两个子任务（Figure 5）：

- **关键帧抓取网络（KNET）**：基于BPS物体编码的CVAE，专门生成抓取时刻 $\Theta^{\mathcal{G}}$ 和放置时刻 $\Theta^{\mathcal{P}}$ 的全身关键帧姿态。将问题聚焦于“静态抓取质量”而非完整序列，显著降低了学习难度。
- **运动内插网络（INET）**：以关键帧和物体信息为条件，生成从T‑pose到抓取（$\mathbf{\breve{\Theta}}^{0:\mathcal{G}}$）以及从抓取到放置（$\mathbf{\Theta}^{\mathcal{G}:\mathcal{P}}$）的连贯运动序列。这种分阶段设计使每个子网络只需专注于各自的目标分布。

**关键物理约束**：生成的关键帧抓取姿态并非直接使用，而是通过联合优化穿透损失与接触损失进行后处理优化。基于SDF的穿透损失 $L_{\mathrm{penetrate}} = \sum_{i} -\min(SDF_{\mathcal{O}}(\mathcal{V}_{h,i}), 0)$ 惩罚手部顶点进入物体内部，接触损失 $L_{\mathrm{contact}}$ 将手部锚点拉向附近物体顶点。消融实验（Table 5）提供了决定性证据：移除穿透损失后，固体交集体积（SIV）从6.50急剧上升至11.81，验证了该物理约束在保证抓取合理性上的关键作用。此外，用通用抓取方法**FLEX**（Tendulkar et al., CVPR 2023）替代KNET时近半数尝试失败，表明针对桌面重排场景的专有训练不可或缺。

**运动内插的阶段性差异**：Table 4显示，INET在T‑pose到抓取阶段（0:G）的运动平滑度（PSKL‑J）优于抓取到放置阶段（G:P），说明重排阶段因涉及物体转移和放置约束，运动生成难度更高。这一发现揭示了分阶段架构的另一个优势——可以针对不同阶段定制优化策略。

### 创新点之间的因果链路

三个维度的创新形成了完整的因果链：AR采集范式提供了高质量训练数据基础 → 场景‑语言接地模块将文本指令转化为精确的空间坐标 → 分阶段生成框架利用这些坐标生成物理合理的抓取姿态与连贯运动序列。感知研究（Table 2）表明，生成动作在Likert量表上获得3.85±1.04的平均分，虽低于数据集真值（4.62±0.54），但已获得志愿者在自然度、抓取合理性和物理一致性上的认可。这一差距主要源于AR视觉反馈缺乏触觉通道，以及数据集动作风格多样性有限，指向了该框架的未来改进方向。

## 整体框架

FAVORITE 是一个两阶段的文本驱动全身虚拟物体重排框架，其核心设计思路是将复杂的“理解指令—定位物体—生成动作”链条解耦为**场景‑语言接地**与**动作重排生成**两个串行模块（Figure 3）。这种分解使得每个阶段可以专注于各自的子问题，从而降低整体学习难度，并保证最终动作序列的连贯性与物理合理性。

![[assets/figures/papers/paper_list_l1661_FAVOR_Full_Body_AR_driven_Virtual_Object_Rearrangement_Guided_by_Instruc/figures/005_Figure_3.jpg]]
*Figure 3: FAVORITE: text-guided motion rearrangement pipeline. It sequentially grounds the object locations, generates grasp poses and flls the motions in between*

### 输入与输出

框架的输入由三部分构成：
- 一段**自然语言指令**，描述需要抓取的目标物体及其放置位置关系（例如 “将蓝色杯子放到红色盘子右侧”）；
- 初始**三维场景布局**，包含桌面、物体模型及其初始位姿；
- 一个**虚拟人物模型**（基于 SMPL‑X 参数化人体）。

框架的输出是一段**连续的全身运动序列**，包含从 T‑pose 出发、抓取目标物体、将其移动并放置到目标位置的完整动作。

### 阶段一：场景‑语言接地

该阶段负责将自然语言指令映射到具体的三维空间位置。系统首先利用大型语言模型 **GPT‑4** 解析指令，提取出目标物体类别与放置介词（如 “on the right of”）。随后，通过一个预定义的 `locate` 函数，结合多视角渲染与视觉‑语言检测器 **Owl‑ViT**，在多个虚拟相机视角下检测物体，并利用多视图几何恢复物体的初始三维位置 $T_{\mathcal{O}}^G$ 与目标放置位置 $T_{\mathcal{O}}^P$（Figure 4）。这一过程将抽象的语义指令转化为精确的空间坐标，为后续动作生成提供明确的目标约束。

### 阶段二：动作重排生成

在获得物体的初始与目标位姿后，动作生成阶段进一步分解为两个子步骤（Figure 5）：

1. **关键帧抓取生成（KNET）**：采用基于条件变分自编码器（CVAE）的网络，以物体的 Basis Point Set（BPS）编码为条件，分别生成抓取时刻与放置时刻的全身关键帧姿态 $\Theta^{\mathcal{G}}$ 与 $\Theta^{\mathcal{P}}$。随后，这些关键帧姿态通过穿透损失 $L_{\mathrm{penetrate}}$、接触损失 $L_{\mathrm{contact}}$ 和正则化损失 $L_{\mathrm{reg}}$ 进行物理约束优化，确保手部与物体之间形成稳定且无穿透的接触。

2. **运动内插生成（INET）**：以关键帧姿态和物体信息为条件，INET 负责生成从 T‑pose 到抓取关键帧（$\mathbf{\breve{\Theta}}^{0:\mathcal{G}}$）以及从抓取到放置关键帧（$\mathbf{\Theta}^{\mathcal{G}:\mathcal{P}}$）的中间运动序列。在生成过程中，系统引入基于 SDF 的障碍物避免优化，推动身体顶点远离场景中的其他物体，同时保持对预测姿态的忠实度。

### 数据闭环与物理约束

值得注意的是，FAVORITE 的训练数据来源于配套的 **FAVOR 数据集**，该数据集通过 AR 眼镜与光学动捕系统采集，包含 3 千段重排序列和 717 万帧交互数据。框架在多个环节嵌入了物理约束：抓取关键帧经过穿透与接触联合优化；放置阶段利用物理模拟器验证物体摆放的稳定性；运动内插时通过 SDF 损失避免身体与障碍物碰撞。这种“数据驱动生成 + 物理后优化”的设计，使得 FAVORITE 能够在保持动作自然度的同时，显著降低穿透和穿模现象。

### 补充图表

![[assets/figures/papers/paper_list_l1661_FAVOR_Full_Body_AR_driven_Virtual_Object_Rearrangement_Guided_by_Instruc/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of the FAVOR data collection pipeline. The researcher directs the task through textual instructions and projects the scene onto the AR glasses. Subjects then rearrange the objects via interaction within the AR space*

![[assets/figures/papers/paper_list_l1661_FAVOR_Full_Body_AR_driven_Virtual_Object_Rearrangement_Guided_by_Instruc/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of recording setup (MoCap + AR glasses)*

## 核心模块与公式推导

FAVORITE 框架的核心由两个阶段构成：**场景‑语言接地** 与 **运动重排生成**。前者负责从文本指令中解析物体的初始与目标位姿；后者则基于接地结果生成符合物理约束的全身抓取与放置动作序列。

### 场景‑语言接地

该模块的目标是将自然语言指令映射为物体的三维空间坐标。流程如下：

1. **指令解析**：利用 GPT‑4 将指令解析为待抓取物体 $O$ 及其放置介词（如 “on top of”），输出结构化的 `locate` 函数调用。
2. **多视角渲染与检测**：在场景中布置虚拟相机进行多视角渲染，将渲染图像送入 Owl‑ViT 视觉‑语言检测器，获取物体在各视角下的二维边界框。
3. **多视图几何定位**：通过多视图几何方法，将二维检测结果提升为物体的三维位置与朝向，分别得到抓取时刻物体位姿 $T_{\mathcal{O}}^{\mathcal{G}}$ 和放置时刻物体位姿 $T_{\mathcal{O}}^{\mathcal{P}}$。

该过程将非结构化的语言指令转化为可操作的几何约束，为后续动作生成提供明确的空间目标。

### 运动重排生成

运动重排生成阶段采用“关键帧生成 + 运动内插”的分治策略，由 **关键帧抓取网络（KNET）** 和 **运动内插网络（INET）** 协同完成。

#### 关键帧抓取网络（KNET）

KNET 是一个基于条件变分自编码器（CVAE）的生成模型，以物体的 Basis Point Set（BPS）编码为条件，生成抓取关键帧 $\Theta^{\mathcal{G}}$ 和放置关键帧 $\Theta^{\mathcal{P}}$ 的全身体姿态。生成的关键帧姿态随后通过物理优化进行精炼，优化目标为：

$$
\underset{\bar{\Theta}}{\operatorname{argmin}} \left( L_{\mathrm{penetrate}} + L_{\mathrm{contact}} + L_{\mathrm{reg}} \right) \tag{Eq. 4}
$$

其中各项损失的物理含义如下：

- **穿透损失** $L_{\mathrm{penetrate}}$：惩罚手部顶点 $\mathcal{V}_{h,i}$ 侵入物体网格内部的情况。其定义为：

$$
L_{\mathrm{penetrate}} = \sum_{i} -\min(SDF_{\mathcal{O}}(\mathcal{V}_{h,i}), 0) \tag{Eq. 1}
$$

当手部顶点位于物体内部时，其有符号距离函数（SDF）值为负，损失取正值；顶点在外部时损失为零。该损失是保证抓取物理合理性的核心约束。

- **接触损失** $L_{\mathrm{contact}}$：将手部锚点 $\mathcal{A}_j$ 拉向其附近（距离小于 3 cm）的物体顶点 $\mathcal{V}_{\mathcal{O},k}$，以增强接触稳定性：

$$
L_{\mathrm{contact}} = \frac{1}{\sum \mathcal{T}} \sum_{j,k} \mathcal{T}_{j,k} ||\mathcal{A}_j - \mathcal{V}_{\mathcal{O},k}||_2^2 \tag{Eq. 2}
$$

其中 $\mathcal{T}$ 为指示矩阵，标记满足距离阈值的锚点‑顶点对。

- **正则化损失** $L_{\mathrm{reg}}$：防止优化后的姿态 $\mathring{\Theta}$ 偏离网络预测姿态 $\hat{\Theta}$ 过远，保持姿态的自然度：

$$
L_{\mathrm{reg}} = || \mathring{\Theta} - \hat{\Theta} ||_1
$$

消融实验（Table 5）表明，移除基于 SDF 的穿透损失后，固体交集体积（SIV）从 6.50 上升至 11.81，验证了该物理约束对生成质量的关键作用。

#### 运动内插网络（INET）

INET 以关键帧姿态和物体信息为条件，生成两段连续的中间运动序列：从 T‑pose 到抓取关键帧的运动 $\mathbf{\breve{\Theta}}^{0:\mathcal{G}}$，以及从抓取关键帧到放置关键帧的运动 $\mathbf{\Theta}^{\mathcal{G}:\mathcal{P}}$。

在内插过程中，为保证运动序列的物理合理性，引入**障碍物避免优化**，推动身体顶点 $\hat{\mathcal{V}}_j$ 远离场景中的障碍物体 $\mathcal{Q}_i$：

$$
\underset{\hat{\mathbf{\Theta}}^{t}}{\operatorname{argmin}} \sum_{i,j} -\min(SDF_{\mathcal{Q}_i}(\hat{\mathcal{V}}_j), 0) + || \hat{\mathbf{\Theta}}^{t} - \hat{\mathbf{\Theta}}^{t} ||_1 \tag{Eq. 5}
$$

此外，在运动生成完成后，通过优化物体到手部的相对变换 $\mathcal{T}_{h\mathcal{O}}$，进一步减少已生成序列中的手部穿透：

$$
\underset{\mathcal{T}_{h\mathcal{O}}}{\mathrm{argmin}} \sum_{j} -\min(SDF_{\mathcal{O}}(\mathring{\mathcal{T}}_{h\mathcal{O}}^{-1} \cdot \mathcal{V}_{h,j}), 0) \tag{Eq. 6}
$$

该后期优化步骤将穿透体积从 11.81 显著降至 6.50，是保证最终动作质量的关键后处理环节。

### 物理约束与姿态先验

除上述公式化约束外，框架还引入两个辅助模块：

- **物理模拟器**：在物体放置阶段验证虚拟物体的稳定性，确保放置姿态不会导致物体滑落或穿透桌面。
- **姿态先验**：将全身体姿态参数投影到 VPoser 的隐空间中，利用其学到的自然人体姿态流形作为正则化先验；同时使用 HuMoR 模型提升运动序列的时间连续性。

### 补充图表

![[assets/figures/papers/paper_list_l1661_FAVOR_Full_Body_AR_driven_Virtual_Object_Rearrangement_Guided_by_Instruc/figures/004_Figure_4.jpg]]
*Figure 4: Diagram of visual-language grounding procedure. Text and images are parsed through the LLM and VLM to implement locate function, and the outcomes of both initial and anticipated object locations*

![[assets/figures/papers/paper_list_l1661_FAVOR_Full_Body_AR_driven_Virtual_Object_Rearrangement_Guided_by_Instruc/figures/006_Figure_5.jpg]]
*Figure 5: Diagram of motion rearrangement generation. keyframe grasping poses*

## 实验与分析

### 数据集规模与采集效率

FAVOR数据集共包含3千段重排序列与717万帧交互数据，涵盖1800种物体模型（Table 1），是目前已知规模最大的带文本指令的全身物体重排数据集。与现有全身交互数据集相比，FAVOR在文本意图标注、3D全身姿态与手部姿态的完整性上具有显著优势。基于AR眼镜的采集管线将单段序列的后处理时间压缩至约3分钟，相比传统光学动捕流程（通常需45分钟以上）实现了约15倍的效率提升。

![[assets/figures/papers/paper_list_l1661_FAVOR_Full_Body_AR_driven_Virtual_Object_Rearrangement_Guided_by_Instruc/figures/003_Table_1.jpg]]
*Table 1: Statistics of the current human motion datasets. †: For the multi-view datasets, we only calculate the total number of frames within a single viewpoint. ‡: We only consider the video clips in the dataset. Annotation methods range from ‘crowd’: labeled by humans; ‘auto’: annotations from visual cues like segmentation, pose estimation, etc.; or ‘mix’: collected from multiple datasets*

### 感知研究：生成动作的自然度评估

为验证FAVORITE生成动作的感知质量，论文组织了5名志愿者的Likert量表评估，对生成动作与FAVOR数据集真值动作在自然度、抓取合理性与物理一致性三个维度进行评分（Table 2）。生成动作的平均Likert得分为3.85±1.04，真值动作为4.62±0.54，差距为-0.77。这一结果表明，FAVORITE生成的动作在整体感知上已接近真实采集水平，但仍存在可辨识的差距。需要注意的是，感知评估仅由5名志愿者完成，样本量较小，可能存在主观偏差，该结论的统计稳健性需进一步验证。

### 关键帧抓取质量评估

抓取质量通过接触率（Contact Ratio, CR）与固体交集体积（Solid Intersection Volume, SIV）两个指标衡量（Table 3）。KNET在初始物体姿态下生成的抓取关键帧达到CR=0.93、SIV=6.50，与FAVOR数据集真实抓取（CR=0.99, SIV=0.83）相比，CR仅下降0.06，SIV上升5.67。这一结果表明KNET能够生成高接触率的抓取姿态，但手部与物体的穿透程度仍明显高于真实数据，反映出仅依赖视觉反馈（无触觉）的虚拟物体交互在接触稳定性上的固有局限。

![[assets/figures/papers/paper_list_l1661_FAVOR_Full_Body_AR_driven_Virtual_Object_Rearrangement_Guided_by_Instruc/figures/011_Table_3.jpg]]
*Table 3: Grasp quality evaluation for FAVOR and KNET*

### 运动内插平滑度分析

INET的运动平滑度通过PSKL-J指标评估（Table 4）。从T-pose到抓取的内插阶段（INET 0:G）在运动平滑度上优于从抓取到放置的内插阶段（INET G:P），说明放置阶段的运动约束更为复杂——放置动作不仅需要维持抓取稳定性，还需在目标位置完成精确释放，对运动规划提出了更高要求。当使用FAVOR数据集真实抓取关键帧替代KNET生成的关键帧时，两阶段内插的平滑度均有提升，进一步表明关键帧抓取质量是制约整体运动连贯性的瓶颈之一。

![[assets/figures/papers/paper_list_l1661_FAVOR_Full_Body_AR_driven_Virtual_Object_Rearrangement_Guided_by_Instruc/figures/008_Table_4.jpg]]
*Table 4: PSKL-J score of our INET with different phase and keyframe grasping pose*

### 消融实验：穿透损失的关键作用

Table 5的消融实验揭示了基于SDF的物体穿透损失（$L_{\mathrm{penetrate}}$）的核心贡献。移除该损失后，固体交集体积从6.50显著上升至11.81，增幅约82%，直接证明了物理穿透约束对于生成合理抓取姿态的必要性。该损失通过惩罚手部顶点在物体网格内部的负SDF值（Eq. 1），有效抑制了手‑物穿透，是KNET能够生成物理可信抓取的关键机制。

### 消融实验：KNET与FLEX的对比

在关键帧抓取生成的消融中，使用**FLEX**（Tendulkar et al., CVPR 2023）替代KNET时，近半数生成尝试失败（Table 5）。FLEX作为通用抓取姿态生成方法，在桌面重排这一特定场景下缺乏针对性训练，难以适应全身姿态与桌面物体交互的联合约束。这一对比验证了KNET专有训练的必要性：基于BPS物体编码的CVAE架构使其能够有效学习桌面场景下物体几何与全身抓取姿态之间的映射关系。

![[assets/figures/papers/paper_list_l1661_FAVOR_Full_Body_AR_driven_Virtual_Object_Rearrangement_Guided_by_Instruc/figures/009_Table_5.jpg]]
*Table 5: INET ablations. The SIV scores are averages from sequences grasping success*

### 后期物体穿透优化

Eq. (6)定义的物体穿透最小化优化（优化物体到手部的相对变换$\mathcal{T}_{h\mathcal{O}}$）作为后处理步骤，进一步降低了已生成运动序列中的手部穿透。该优化与抓取关键帧优化（Eq. 4）和运动内插中的障碍物避免优化（Eq. 5）共同构成了贯穿生成全流程的多层次物理约束体系。

### 定性结果与失败模式

Figure 6展示了FAVORITE生成的抓取与放置动作序列的定性结果。黄色高亮人体表示抓取阶段（$\Theta^{0:\mathcal{G}}$），品红色高亮人体表示放置阶段（$\Theta^{\mathcal{G}:\mathcal{P}}$），可见生成动作在整体上保持了合理的身体姿态与手‑物空间关系。

主要失败模式包括：（1）放置阶段的抓取稳定性显著低于初始抓取阶段，可能与放置视角受限及接触优化不足有关；（2）复杂、非模板化指令下，场景‑语言接地模块的定位精度下降；（3）AR虚拟物体缺乏触觉反馈，导致手部抓取的自然度与真实交互仍有差距。这些问题指向了未来工作的关键方向：引入多模态感知反馈、扩展指令解析的泛化能力、以及覆盖更开放动态的交互场景。

### 补充图表

![[assets/figures/papers/paper_list_l1661_FAVOR_Full_Body_AR_driven_Virtual_Object_Rearrangement_Guided_by_Instruc/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative results of motion synthesis. The man highlighted in yellow illustrates the grasping motion*

## 方法谱系与知识库定位

### 任务定位与核心差异

FAVORITE 解决的是**文本指令驱动的全身虚拟物体重排**任务。该任务要求系统根据自然语言指令，在三维场景中定位物体、生成从初始抓取到目标放置的完整全身动作序列。与现有工作的核心差异在于：

- **数据模态的扩展**：现有全身交互数据集（如 GRAB、BEHAVE、InterCap）主要关注真实物体抓取或简单交互，缺乏大规模、场景多样化且带文本指令的物体重排数据。FAVOR 数据集填补了这一空白，包含 3K 段重排序列、7.17M 帧交互数据、1800 种物体模型，是目前最大的带文本指令的全身物体重排数据集（Table 1）。
- **交互范式的革新**：传统数据采集依赖真实物体交互或纯合成数据，FAVOR 引入 AR 眼镜与光学动捕系统集成的采集平台，通过实时虚拟物体视觉反馈，将单段序列的后处理时间从传统动捕的 45 分钟以上缩短至约 3 分钟，效率提升约 15 倍。
- **生成框架的分阶段设计**：与端到端生成或单阶段方法不同，FAVORITE 将任务分解为场景‑语言接地（GPT‑4 + Owl‑ViT 多视角定位）和动作重排生成（CVAE 关键帧抓取 + 运动内插网络 INET），降低了学习难度并保证了序列的连贯性与准确性。

### 与相关工作的关系

#### 数据集层面

FAVOR 数据集在规模、标注维度和交互类型上与现有数据集形成互补（Table 1）：

- 相比 **GRAB**（Taheri et al., ECCV 2020）等真实物体抓取数据集，FAVOR 提供文本指令标注和虚拟物体交互，支持从语言到动作的端到端学习。
- 相比 **BEHAVE**（Bhatnagar et al., CVPR 2022）等多人‑物交互数据集，FAVOR 聚焦单人全身重排，动作序列更长、物体种类更丰富。
- 相比 **InterCap**（Huang et al., CVPR 2022）等基于多视角的交互数据集，FAVOR 通过 AR 反馈实现了更自然的交互采集，且包含完整的物体运动轨迹 $\tau_{\mathcal{O}}^{0:T}$。

#### 方法层面

- **场景‑语言接地**：FAVORITE 采用 GPT‑4 解析指令为 Python‑like `locate` 函数，结合 Owl‑ViT 多视角检测与多视图几何定位物体三维位置。这一设计与传统直接文本编码或简单指令模板相比，增强了对复杂空间关系的理解能力，但当前仍依赖预定义的 `locate` 模板，对非模板化指令的泛化能力有限。
- **关键帧抓取生成（KNET）**：KNET 是基于 BPS 物体编码的条件变分自编码器，专为桌面重排场景训练。消融实验表明，使用通用抓取姿态生成方法 **FLEX**（Tendulkar et al., CVPR 2023）替代 KNET 时，近半数尝试失败，验证了针对特定场景进行专有训练的必要性（Table 5）。
- **物理约束与姿态优化**：FAVORITE 引入基于 SDF 的穿透损失 $L_{\mathrm{penetrate}}$ 和接触损失 $L_{\mathrm{contact}}$，结合物理模拟器确保物体放置稳定，并利用 VPoser 与 HuMoR 提升姿态自然度和动作连续性。消融实验验证了穿透损失的关键作用——移除该损失后，固体交集体积（SIV）从 6.50 显著上升至 11.81（Table 5）。

### 适用边界与局限性

1. **视觉反馈的局限**：AR 眼镜仅提供视觉场景，缺乏触觉反馈，可能影响手部与物体的接触稳定性。这是虚拟物体交互相对于真实物体交互的固有精度损失，其对最终动作质量的影响程度尚需量化。
2. **动作风格的多样性**：数据集由少量受试者采集，动作风格多样性有限，可能影响生成模型的泛化能力。
3. **物理模拟的保真度**：虚拟物体的交互虽通过物理模拟器约束，但与真实物理动态仍可能存在差异，尤其在复杂接触和碰撞场景下。
4. **指令解析的泛化性**：场景‑语言接地模块依赖预定义的 `locate` 模板，对复杂、非模板化指令（如涉及多个物体、条件判断或时序约束的指令）的泛化能力有限。
5. **场景覆盖范围**：实验场景主要集中在桌面上进行物体堆放，尚未覆盖更开放或动态的环境（如地面、货架、移动障碍物等）。

### 开放问题

1. **精度损失的量化**：使用 AR 虚拟物体替代真实物体所带来的精度损失，对最终动作质量的影响程度如何量化？能否通过引入触觉反馈或其他感知通道来缩小虚拟与真实交互的差距？
2. **放置姿态的稳定性**：为何放置姿态的抓取稳定性显著低于初始抓取姿态？是由于视角限制（放置时物体可能被遮挡）还是接触优化不足？这需要进一步分析 KNET 在不同阶段的性能差异。
3. **SDF 穿透损失的可扩展性**：基于 SDF 的穿透损失在形状更复杂、非凸的物体上是否仍然有效？其计算开销在实时应用中是否可控？
4. **指令解析的扩展**：能否将场景‑语言接地模块扩展到动态场景或需要连续规划的长时间任务中？例如，处理“将杯子放入洗碗机，然后将盘子放在架子上”这类多步指令。
5. **触觉反馈的集成**：如何将触觉反馈或其他感知通道引入 AR 交互，以提升手部抓取的自然度和接触稳定性？这是缩小虚拟与真实交互差距的关键方向。

## 原文 PDF

![[paperPDFs/AAAI_2024/FAVOR_Full_Body_AR_driven_Virtual_Object_Rearrangement_Guided_by_Instruction_Text.pdf]]
