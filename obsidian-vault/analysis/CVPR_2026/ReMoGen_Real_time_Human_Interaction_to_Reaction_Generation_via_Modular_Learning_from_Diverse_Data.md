---
title: "ReMoGen: Real-time Human Interaction-to-Reaction Generation via Modular Learning from Diverse Data"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ReMoGen_Real_time_Human_Interaction_to_Reaction_Generation_via_Modular_Learning_from_Diverse_Data.pdf
project_link: "https://4dvlab.github.io/project_page/remogen/"
code_link: null
aliases:
- RRMG
- ReMoGen
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过冻结通用运动先验并注入独立训练的Meta-Interaction模块，将异构交互线索（他人动作和场景）转换为潜在空间的自适应调制，从而控制生成过程。
primary_logic: 将大规模单人运动先验作为通用基础，通过轻量适配器（Meta-Interaction模块）进行特定交互域的快速适应，并利用帧级细化（FWSR）在不牺牲质量的前提下实现实时响应，从而有效应对数据异质性和实时性双重挑战。
claims:
- 在HHI任务（Inter-X）上，ReMoGen的FID达到0.181，远超最佳在线基线SymBridge的2.569，且延迟仅0.042s满足实时要求。
- 在HSI任务（LINGO）上，ReMoGen在所有指标上均超过基线，FID从TRUMANS的4.731降至1.201，延迟最低（0.042s）。
- 在混合模态EgoBody上，使用通用先验初始化并微调仅2k步即可超越从头训练500k步的性能（FID 2.757 vs 2.341），快速适应新域。
- FWSR在几乎不增加延迟的情况下（0.047s）将FID从0.181改善至0.166，同时保持高语义对齐，有效解决了响应性与质量的权衡。
---

# ReMoGen: Real-time Human Interaction-to-Reaction Generation via Modular Learning from Diverse Data

> [!tip] 核心洞察
> 将大规模单人运动先验作为通用基础，通过轻量适配器（Meta-Interaction模块）进行特定交互域的快速适应，并利用帧级细化（FWSR）在不牺牲质量的前提下实现实时响应，从而有效应对数据异质性和实时性双重挑战。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReMoGen：基于模块化学习的实时交互反应生成 |
| 英文题名 | ReMoGen: Real-time Human Interaction-to-Reaction Generation via Modular Learning from Diverse Data |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.01082) · [Project](https://4dvlab.github.io/project_page/remogen/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ReMoGen (Reaction Motion Generation) |
| Dataset | Inter-X, LINGO, EgoBody |

> [!tip] 效果简介
> - Inter-X (HHI) 上，FID↓ 0.181 vs FreeMotion: 3.383 (-3.202)；R-Precision (Top-3)↑ 0.464 vs FreeMotionoff: 0.417 (+0.047)；Latency (s/frame)↓ 0.042 vs SymBridge: 0.040 (+0.002 (略高，但仍在实时阈值内))。
> - LINGO (HSI) 上，FID↓ 1.201 vs TRUMANS: 4.731 (-3.530)。
> - EgoBody (Mixed) 上，FID↓ (微调65k步后) 0.292 vs 从零训练: 2.341 (500k步) (-2.049)。

## 概要

交互反应生成（Interaction-to-Reaction Generation）面临双重瓶颈：**交互数据稀缺且异构分布**——大规模单人运动数据与小规模人-人/人-场景交互数据之间存在显著域差异；同时，**实时性与高保真度难以兼得**，现有方法要么牺牲质量换取低延迟，要么因全序列扩散而无法满足在线响应需求。

ReMoGen 的核心洞察是：将大规模单人运动先验作为通用基础，通过轻量适配器进行特定交互域的快速适应，并利用帧级细化在不牺牲质量的前提下实现实时响应。具体而言，该方法冻结在大规模单人数据上预训练的文本条件潜在扩散模型，仅训练独立的 **Meta-Interaction 模块**，将异构交互线索（他人动作历史和场景占用）转换为潜在空间的自适应 FiLM 调制，从而控制生成过程。在线推理时，采用分段自回归生成配合 **逐帧段细化（FWSR）**，在不重新运行完整扩散过程的情况下，基于最新观测对潜在表示进行轻量修正。

**关键实证结果**：在人-人交互（Inter-X）上，ReMoGen 的 FID 达到 0.181，远超最佳在线基线 SymBridge 的 2.569，延迟仅 0.042 s 满足实时阈值（≤0.1 s/frame）；在人-场景交互（LINGO）上，FID 从 TRUMANS 的 4.731 降至 1.201，延迟最低；在混合模态 EgoBody 上，使用通用先验初始化并微调仅 2k 步即可超越从头训练 500k 步的性能（FID 2.757 vs 2.341）。FWSR 在几乎不增加延迟（0.047 s）的情况下将 FID 进一步改善至 0.166，有效解决了响应性与质量的权衡。

**方法定位**：ReMoGen 属于“冻结通用先验 + 轻量域适配器”的模块化范式，区别于端到端联合训练或逐域独立建模的传统路线。其可组合的多分支融合机制（加权求和 + L2 范数裁剪）支持灵活的人-人、人-场景混合设置，在方法谱系中填补了实时、多域统一的交互反应生成空白。

**局限与开放问题**：潜在扩散的压缩空间可能损害细粒度空间精度，尤其在近距离接触或高精度人-物交互中；简单加权组合策略并非最优，更有效的免训练融合方法值得探索。



### 问题背景：交互反应生成的双重困境

在虚拟现实、具身智能和数字人等应用中，实时生成与外部刺激（他人动作、场景物体）协调一致的人类反应运动是一项核心能力。然而，这一任务面临两个相互纠缠的瓶颈。

**数据异质性与稀缺性**是首要障碍。大规模单人运动捕捉数据（如AMASS）相对丰富，但包含人际交互（HHI）或人-场景交互（HSI）的高质量标注数据极为有限。更棘手的是，不同交互域的数据分布差异显著——单人运动、双人互动、场景交互各自遵循不同的统计规律，直接混合训练会导致域间冲突，而单独训练则因数据不足而严重过拟合。

**实时响应与生成质量的权衡**构成第二重困境。扩散模型在运动生成中展现出卓越的质量，但其迭代去噪过程天然具有高延迟。现有方案要么牺牲实时性进行离线全序列生成，要么采用逐帧重计算导致推理成本剧增，难以在10 FPS的实时阈值（每帧<0.1s）内保持高保真度。

### 现有方法的缺口

当前交互反应生成方法可归为两类，各有明显局限：

- **端到端联合训练方法**（如ReGenNet、FreeMotion）：将交互线索与运动生成器联合优化。由于交互数据量小，这类方法容易过拟合，且训练好的模型难以泛化到未见交互域。FreeMotion的离线变体（FreeMotionoff）在Inter-X数据集上FID为3.383，但在线版本性能进一步退化。

- **在线实时方法**（如SymBridge）：通过轻量架构实现低延迟，但生成质量显著下降。SymBridge在Inter-X上的FID高达2.569，远不能满足高保真应用需求。在人-场景交互基准LINGO上，现有方法TRUMANS的FID为4.731，同样暴露了质量瓶颈。

根本问题在于：这些方法缺乏一个可复用的运动生成基础，导致每个交互域都需要从零开始学习，既浪费了大规模单人数据中蕴含的丰富运动先验，又无法在低延迟约束下维持生成质量。

### 本文动机

针对上述困境，ReMoGen的核心思路是**模块化解耦**：将“通用运动生成能力”与“特定交互适应能力”分离。

具体而言，我们提出从大规模单人数据中预训练一个冻结的通用运动先验，使其掌握基本的人体运动结构与物理合理性。在此基础上，通过独立训练的轻量级Meta-Interaction模块注入他人动作和场景上下文，实现跨交互域的快速适应。这种设计使得模型既能利用丰富数据获得强先验，又能灵活应对异构交互线索，无需为每个新域重新训练完整模型。

同时，为打破实时性与质量的僵局，我们引入帧级段细化（FWSR）机制——在分段自回归生成框架上叠加轻量逐帧潜在空间修正，以极低的额外延迟换取显著的质量提升，从而在0.047s的延迟下将FID从0.181进一步降至0.166。



## 核心方法与创新机理

ReMoGen 的核心创新在于通过**模块化解耦**同时应对交互反应生成中的两大瓶颈：交互数据稀缺且异构分布，以及实时响应与生成质量的权衡。其关键设计可归纳为三个相互协同的 changed slots。

**1. 冻结通用运动先验 + 轻量域适配器（模块化迁移）**

与以往在有限交互数据上端到端训练、易过拟合且泛化差的方案不同，ReMoGen 在**大规模单人运动数据（HumanML3D）**上预训练一个文本条件的潜在自回归扩散先验，并在后续所有交互域训练中**完全冻结**该先验。交互域的适应仅通过独立训练的轻量 **Meta-Interaction 模块**实现，该模块将他人动作历史和场景占用体积编码为上下文，以 FiLM 风格调制注入冻结先验的去噪过程（Eq. 6）。消融实验（Table 4）直接验证了这一设计的决定性作用：冻结先验+适配器方案取得 FID 0.181，而联合微调（全模型）会侵蚀预训练知识（FID 0.298），从头训练则受限于数据量（FID 0.270），仅用先验不注入交互线索则完全失效（FID 3.735）。这种“通用基础+按域插件”的范式，使得模型能有效利用异构数据——大规模单人数据提供运动结构，小规模交互数据提供交互语义。

**2. Meta-Interaction 模块实现交互线索的自适应注入**

ReMoGen 不将所有模态联合处理，而是为每种交互线索（他人动作、场景）设计**独立的 Meta-Interaction 模块**。每个模块通过交叉注意力从交互上下文（他人运动历史、场景占用）中提取调制参数 $\gamma, \beta$，对冻结先验的中间特征进行仿射变换：$h_{\mathrm{mod}} = (1 + \tanh \gamma) \odot h' + \tanh \beta$（Eq. 6）。多分支输出通过加权求和组合：$\Delta_{\mathrm{total}} = \sum_{i} \alpha_{i} \Delta_{i}$（Eq. 7），并辅以 L2 范数裁剪防止调制过度。这一设计带来两个关键收益：一是**域间解耦**——人-人交互和人-场景交互模块可独立训练，无需联合数据；二是**混合模态的即插即用组合**——在 EgoBody 混合场景中，零样本组合两个模块即可提供互补先验，经仅 2k 步微调后 FID 达 2.757，超越从头训练 500k 步的性能（FID 2.341，Table 3）。此外，该模块独立于文本条件，即使移除文本输入，仍能生成物理合理的交互动作，说明其对动态交互线索的直接响应能力。

**3. 逐帧段细化（FWSR）打破响应性-质量权衡**

在线交互生成的核心矛盾在于：分段自回归（Seg.）延迟低但更新滞后，逐帧重扩散（Slide）响应快但延迟高且引入时序伪影。ReMoGen 的 **FWSR** 策略在两者之间取得突破：保持分段级扩散生成作为稳定基础，仅在每帧对新观测进行**轻量级潜在空间调制**（Eq. 8），无需重新运行完整扩散过程。Table 5 显示，FWSR 在几乎不增加延迟（0.047s vs. Seg. 0.042s）的情况下，将 FID 从 0.181 进一步改善至 0.166，而 Slide 方案的延迟高达 0.305s 且 FID 恶化至 4.136。这一设计实现了**实时响应与高保真度的兼得**，是 ReMoGen 满足 10 FPS 实时阈值（<0.1s/frame）的关键使能技术。

**创新协同总结**

上述三个 changed slots 形成递进式的创新链条：通用先验提供高质量运动基础，Meta-Interaction 模块以最小代价注入交互语义，FWSR 在不牺牲质量的前提下实现帧级实时响应。三者共同构成了 ReMoGen 应对“数据异质性”和“实时性”双重挑战的核心机制，使其在 Inter-X（HHI）上 FID 达 0.181（最佳在线基线 SymBridge 为 2.569），在 LINGO（HSI）上 FID 达 1.201（基线 TRUMANS 为 4.731），且延迟均满足实时要求（0.042s）。



ReMoGen 采用模块化设计，将交互反应生成分解为两个功能层次：**先验引导的模块化学习（Prior-guided Modular Learning）** 与**逐帧段细化（Frame-wise Segment Refinement, FWSR）**。其核心思想是将从大规模单人数据中习得的通用运动先验作为冻结基础，通过轻量级的 Meta-Interaction 模块注入异构交互线索，再以 FWSR 实现低延迟的在线更新。

**Pipeline 总览。** 系统以自回归方式运行：给定历史运动片段 $M_h^i$，模型预测未来运动段 $\hat{M}_f^i$，随后按式 (1) 更新历史窗口：
$$M_h^{i+1} = \mathrm{concat}(M_h^i, \hat{M}_f^i)[-H:]$$
该过程持续循环，形成实时交互反应流。

**模块关系与数据流。** 框架包含三个核心模块：
1. **通用单人运动先验（Universal Single-Person Prior）**：一个冻结的文本条件潜在扩散模型，在大规模数据集（HumanML3D）上预训练，提供基础运动结构和时序连贯性。它以历史运动 $M_h^i$ 和文本嵌入 $w$ 为输入，在潜在空间中执行去噪生成。
2. **Meta-Interaction 模块**：独立训练的轻量适配器，包含他人编码器（Others Encoder）和场景编码器（Scene Encoder）。它们分别将他人运动历史和场景占用体积编码为上下文向量 $c_{\mathrm{others}}$、$c_{\mathrm{scene}}$，通过 FiLM 风格的特征调制（式 (6)）注入到冻结先验的交叉注意力层中：
   $$h_{\mathrm{mod}} = (1 + \tanh \gamma) \odot h' + \tanh \beta$$
   多个 Meta-Interaction 模块的输出可通过加权求和组合（式 (7)），支持人-人、人-场景及混合交互设置：
   $$\Delta_{\mathrm{total}} = \sum_i \alpha_i \Delta_i$$
   融合后的调制量经 L2 范数裁剪后作用于潜在特征。
3. **逐帧段细化（FWSR）**：在分段级自回归预测之上叠加轻量级逐帧修正。它不重新运行完整扩散过程，而是基于最新观测动态上下文对初始潜在 $z_0$ 施加调制（式 (8)），生成细化后的潜在 $\hat{z}^f$，在几乎不增加延迟的前提下提升响应精度。

**输入输出流。** 输入端接受多模态信号：文本描述 $w$（可选）、他人运动序列（用于 HHI）、场景占用体积（用于 HSI）。输出端生成 ego 视角的连续运动序列，帧率 10 FPS，单帧推理延迟约 0.042s（FWSR 模式下约 0.047s），满足实时交互阈值（< 0.1s/frame）。

这种“冻结先验 + 可插拔适配器 + 轻量在线修正”的架构，使得 ReMoGen 既能继承大规模预训练的运动质量，又能灵活适应不同交互域，同时保持实时响应能力。

### 补充图表

![[assets/figures/papers/paper_list_l922_https_arxiv_org_abs_2604_01082/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the ReMoGen Framework. Our framework is designed to address the challenges of data scarcity and real-time responsiveness in interaction-to-reaction generation*



ReMoGen 的架构围绕三个核心模块构建，分别解决运动先验迁移、异构交互线索注入和实时响应性三个关键问题。

### 通用单人运动先验

该模块是一个冻结的文本条件潜在扩散模型，在大规模单人运动数据集（HumanML3D）上预训练，为所有交互域提供通用的运动结构基础。其自回归生成范式如下：给定历史运动片段 $M_h^i$（包含过去 $H$ 帧），模型预测未来 $F$ 帧的运动段 $\hat{M}_f^i$，随后通过滑动窗口更新历史：

$$M_h^{i+1} = \mathrm{concat}(M_h^i, \hat{M}_f^i)[-H:] \tag{1}$$

在潜在空间中，去噪器 $G_\psi$ 以文本嵌入 $w$ 为条件，从噪声潜在 $z_t$ 预测干净潜在 $\hat{z}_0$：

$$\hat{z}_0 = G_\psi(z_t, t, M_h^i, w) \tag{3}$$

### Meta-Interaction 模块

该模块是 ReMoGen 实现异构交互线索注入的关键设计。它由两个独立编码器和一个调制块组成：

- **他人编码器**：将他人运动历史编码为上下文表示 $c_\text{others}$
- **场景编码器**：将场景占用体积编码为上下文表示 $c_\text{scene}$

这些上下文信息被注入到冻结先验的去噪过程中，使条件化去噪变为：

$$\hat{z}_0 = G_\psi(z_t, t, M_h^i, c_\text{others}, c_\text{scene}, w) \tag{4}$$

注入机制采用 **FiLM（Feature-wise Linear Modulation）** 风格的仿射变换。在去噪器的交叉注意力层中，上下文信息通过交叉注意力生成调制参数 $\gamma$ 和 $\beta$，对特征 $h'$ 进行逐元素缩放和平移：

$$h_\text{mod} = (1 + \tanh \gamma) \odot h' + \tanh \beta \tag{6}$$

其中 $\tanh$ 函数将调制幅度限制在合理范围内，$\odot$ 表示逐元素乘法。这种设计使得交互线索能够自适应地调节运动生成过程，而不会破坏预训练先验的知识结构。

对于多交互域融合（如同时存在人-人和人-场景交互），ReMoGen 采用可组合的多分支加权组合策略：

$$\Delta_\text{total} = \sum_i \alpha_i \Delta_i \tag{7}$$

其中 $\Delta_i$ 为各 Meta-Interaction 模块的输出调制量，$\alpha_i$ 为用户定义的权重系数。融合后的调制量在施加到潜在特征之前经过 L2 范数裁剪，防止调制幅度过大导致生成崩溃。

### 逐帧段细化（FWSR）

FWSR 是解决实时响应性与生成质量权衡的关键模块。标准分段自回归推理（Seg.）仅在每段结束时更新一次，无法及时响应最新观测；而逐帧重新运行完整扩散过程（Slide）虽然响应及时，但延迟过高（0.305s）且引入时序伪影。

FWSR 的核心思想是在稳定的段级预测之上施加轻量级逐帧修正。对于第 $f$ 帧，它利用初始潜在 $z_0$ 和历史与动态上下文的拼接进行调制：

$$\hat{z}^f = \mathrm{Modulate}\big(z_0, \mathrm{concat}(M_h^{(f-1)}, X_\text{dyn}^{(f)})\big) \tag{8}$$

其中 $M_h^{(f-1)}$ 为截至前一帧的运动历史，$X_\text{dyn}^{(f)}$ 为当前帧的动态交互线索。该调制通过一个小型适配器网络实现，仅需微小的额外计算开销（延迟从 0.042s 增至 0.047s），即可将 FID 从 0.181 改善至 0.166（Table 5），实现了实时响应与高保真的有效平衡。

### 补充图表

![[assets/figures/papers/paper_list_l922_https_arxiv_org_abs_2604_01082/figures/009_Figure.jpg]]
*Figure: A. Architecture of Meta-Interaction Block*



## 实验与关键发现

### 核心瓶颈与因果验证

ReMoGen 的设计直指交互生成领域的双重瓶颈：**交互数据稀缺且异构分布**（大规模单人数据 vs. 小规模人-人/人-场景数据），以及**低延迟与高保真度之间的实时权衡**。其因果机制可概括为：通过冻结在大规模单人数据上预训练的通用运动先验，并注入独立训练的 Meta-Interaction 模块，将异构交互线索（他人动作和场景）转化为潜在空间的自适应调制，从而控制生成过程。实验部分通过多域主结果、消融研究和泛化测试，系统验证了这一因果链条的有效性。

### 人-人交互（HHI）主结果

在 Inter-X 数据集上，ReMoGen 在所有质量指标上均显著超越基线模型，同时满足实时性要求（表 1）。

**表 1 核心发现**（Human–Human Interaction on Inter-X）：
- **FID↓**：ReMoGen 达到 **0.181**，远优于最佳在线基线 SymBridge 的 2.569，降幅达 93%。离线变体 FreeMotionoff 的 FID 为 2.216，同样被大幅超越。
- **R-Precision (Top-3)↑**：**0.464**，高于 FreeMotionoff 的 0.417，表明生成动作与交互语义的对齐度更高。
- **延迟**：**0.042 s/frame**，低于 0.1 s/frame 的实时阈值（绿色标记），与 SymBridge（0.040 s）相当，但质量优势巨大。
- **FWSR 增益**：启用逐帧段细化后，FID 进一步改善至 **0.166**，延迟仅微增至 0.047 s，仍在实时范围内。

这一结果直接验证了**决定性证据 1**：冻结先验 + 轻量适配器的模块化设计，在保持实时响应的同时，实现了前所未有的运动质量。

### 人-场景交互（HSI）主结果

在 LINGO 数据集上，ReMoGen 在所有评估指标上均取得最佳性能，且延迟最低（表 2）。

**表 2 核心发现**（Human-Scene Interaction on LINGO）：
- **FID↓**：ReMoGen 达到 **1.201**，相比 TRUMANS 的 4.731 降低 3.530，降幅 74.6%。
- **延迟**：**0.042 s/frame**，为所有模型中最低，且满足实时阈值。
- **全指标优势**：在 R-Precision、MM-Dist、Diversity 等指标上均超越 TRUMANS 和 LINGO 基线。

该结果验证了**决定性证据 2**：Meta-Interaction 模块中的场景编码器（Scene Encoder）能有效将场景占用体积转换为运动生成的调制信号，且模块化设计未引入额外延迟负担。

### 混合模态泛化与快速适应

EgoBody 数据集上的实验验证了 ReMoGen 在混合交互设置（人-人 + 人-场景）下的泛化能力（表 3）。

**表 3 核心发现**（Mixed-modality on EgoBody）：
- **零样本组合**：直接组合预训练的 HHI 和 HSI 模块可提供互补先验，但存在明显的域不匹配（FID 较高）。
- **先验初始化微调**：使用通用先验初始化并微调仅 **2k 步**，FID 即达到 **2.757**，超越从头训练 500k 步的 2.341。微调至 65k 步后，FID 进一步降至 **0.292**，相比从头训练降低 2.049。
- **快速适应机制**：冻结先验保留了大规模单人数据中的运动结构知识，仅需少量目标域数据即可通过 Meta-Interaction 模块实现域适应，验证了**决定性证据 3**。

### 消融研究

#### 通用运动先验的使用方式（表 4）

该消融直接验证了模块化设计的核心假设——冻结先验优于联合训练或从头训练。

- **无交互线索（仅先验）**：FID 高达 **3.735**，证明交互线索注入是必需的。
- **从头训练（无先验）**：受限于交互数据量，FID 为 **0.270**，显著差于冻结先验方案。
- **联合微调（全模型）**：FID 为 **0.298**，表明微调会侵蚀预训练知识，导致性能退化。
- **冻结先验 + 适配器（本文方案）**：FID 最佳，为 **0.181**，证明模块化设计兼顾运动质量与交互语义。

#### 逐帧段细化（FWSR）消融（表 5）

该消融验证了 FWSR 在实时性与质量之间的权衡优势。

- **标准分段推理（Seg.）**：FID **0.181**，延迟 0.042 s，但每段仅更新一次，响应滞后。
- **滑动窗口逐帧重生成（Slide）**：FID 恶化至 **4.136**，延迟飙升到 **0.305 s**，引入严重时序伪影，证明逐帧完整扩散不可行。
- **FWSR（本文方案）**：FID 改善至 **0.166**，延迟仅 **0.047 s**，几乎不增加计算成本即实现质量提升，验证了**决定性证据 4**。

#### 编码器敏感性（附录表 C）

将他人编码器从 TCN 替换为 MLP 或 Transformer，FID 分别为 0.236 和 0.223（TCN 为 0.181），性能差异较小。这表明框架的有效性不依赖于特定编码器设计，模块化架构本身是性能增益的主要来源。

#### 文本条件鲁棒性（附录 Fig. B）

即使移除文本输入或输入冲突文本，ReMoGen 仍能生成物理合理的交互动作。这是因为 Meta-Interaction 模块独立于文本条件，直接响应动态交互线索（他人运动历史和场景占用），赋予系统对文本噪声的鲁棒性。

### 失败模式与局限性

尽管 ReMoGen 在主要指标上表现优异，分析揭示了以下局限：

1. **细粒度空间精度不足**：潜在扩散先验的压缩空间可能损害细粒度空间精度，尤其在近距离接触或高精度人-物交互场景中。附录表 A 的接触度量评估可能揭示了这一不足，但需要手动验证具体数值。
2. **简单加权融合非最优**：当前多分支组合采用用户定义系数的加权求和（Eq. 7），在混合交互设置中可能并非最优。更有效的免训练融合方法可能进一步提升性能。
3. **延迟瓶颈**：附录表 B 的延迟分解显示，VAE 解码和扩散去噪是主要计算开销。在更低延迟需求（如 >30 FPS）的场景下，需进一步优化这些模块。

### 公平性说明

所有实验遵循统一的在线交互-反应协议评估：支持自回归的基线保留其原始推理机制，否则采用“预测-拼接”方案。序列统一降采样至 10 FPS，使用与训练相同的标准化处理。延迟测试基于单张 NVIDIA RTX 3090 GPU，测量 1000 帧的平均每帧计算时间。这些措施确保了对比的公平性。

### 补充图表

![[assets/figures/papers/paper_list_l922_https_arxiv_org_abs_2604_01082/figures/004_Table_1.jpg]]
*Table 1: Human–Human Interaction results on Inter-X. Bold indicates the best and underlined indicates the second-best. Reported latency is end-to-end inference time. Green latency values meet the 0.1 s/frame real-time threshold (equivalent to 10 FPS), while red values do not*

![[assets/figures/papers/paper_list_l922_https_arxiv_org_abs_2604_01082/figures/005_Table_2.jpg]]
*Table 2: Human-Scene Interaction results on LINGO. Bold indicates best performance. Green latency values meet the 0.1 s/frame real-time threshold. Ours outperforms both baselines across all evaluation metrics*

![[assets/figures/papers/paper_list_l922_https_arxiv_org_abs_2604_01082/figures/006_Table_3.jpg]]
*Table 3: Mixed-modality results on EgoBody. Zero-shot composition provides complementary priors but reflects clear domain mismatch. Prior-initialized finetuning rapidly adapts to the target domain, outperforming scratch training within a few thousand steps*

![[assets/figures/papers/paper_list_l922_https_arxiv_org_abs_2604_01082/figures/008_Table_4.jpg]]
*Table 4: Ablation on different ways of using the universal prior*

![[assets/figures/papers/paper_list_l922_https_arxiv_org_abs_2604_01082/figures/007_Table_5.jpg]]
*Table 5: Ablation on Frame-wise Segment Refinement (FWSR). Seg. denotes standard segment-based autoregressive rollout, which updates once per segment. Slide regenerates a full segment at every frame and uses only the first predicted frame. The gray row shows the baseline segment rollout, and the highlighted row shows our FWSR, which performs per-frame refinement while keeping segment-level generation unchanged*

![[assets/figures/papers/paper_list_l922_https_arxiv_org_abs_2604_01082/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative results of ReMoGen across Human–Human, Human–Scene, and mixed Human–Human–Scene scenarios. Blue meshes denote the generated ego motion, while red meshes represent the observed motions of others. The examples cover diverse interaction behaviors, including Taichi-style movements, chasing, chatting, and scene-aware interaction, demonstrating the versatility of ReMoGen across heterogeneous interaction settings*

![[assets/figures/papers/paper_list_l922_https_arxiv_org_abs_2604_01082/figures/014_Figure.jpg]]
*Figure: C. Qualitative comparisons on Human–Human Interaction tasks. For typographical reasons, we have presented the optimal offline version of FreeMotion. Our method produces smoother and more coordinated reactions aligned with the intent, whereas baselines exhibit unnatural timing, misaligned contact, or unstable body dynamics*

![[assets/figures/papers/paper_list_l922_https_arxiv_org_abs_2604_01082/figures/015_Figure.jpg]]
*Figure: D. Qualitative comparisons on Human-Scene Interaction tasks. All methods are evaluated with goal location provided*

![[assets/figures/papers/paper_list_l922_https_arxiv_org_abs_2604_01082/figures/016_Figure.jpg]]
*Figure: HHI Only HSI Only Compose Figure E. Zero-shot Human–Human–Scene Interaction results*

![[assets/figures/papers/paper_list_l922_https_arxiv_org_abs_2604_01082/figures/020_Figure.jpg]]
*Figure: I. Ablation on Frame-wise Segment Refinement. We present ”A person runs towards someone and passes by them.” FWSR provides fine-grained updates that improve responsiveness without sacrificing stability, outperforming both segment-only and naive slidestyle inference*



## 定位与知识库关联

### 1. 与基线工作的关系

ReMoGen 定位于**实时交互-反应运动生成**这一新兴任务，其核心贡献在于通过模块化学习框架，将大规模单人运动先验与稀缺的异构交互数据解耦，从而同时应对数据稀缺和实时响应两大瓶颈。以下从三个交互域分别梳理其与现有工作的关系。

#### 1.1 人-人交互（HHI）

在 HHI 任务上，ReMoGen 与以下基线形成对比：

- **ReGenNet**：基于动作-反应映射的早期方法，受限于数据规模和建模能力，在生成质量和多样性上均落后于扩散类方法。
- **FreeMotion / FreeMotionoff**：基于扩散的 HHI 生成方法。FreeMotionoff 为离线全序列扩散，无法满足实时要求；FreeMotion 虽支持在线生成，但在 Inter-X 数据集上 FID 高达 3.383（Table 1），远差于 ReMoGen 的 0.181。其根本原因在于 FreeMotion 在有限的交互数据上端到端训练，缺乏通用运动先验的支撑。
- **SymBridge**：实时人-机器人交互（HRI）基线，延迟仅 0.040 s/frame（Table 1），是唯一在延迟上与 ReMoGen 接近的方法。但其 FID 高达 2.569，表明其在运动质量上存在显著差距。ReMoGen 以 0.042 s 的延迟实现了 0.181 的 FID，在实时性和质量之间取得了更优的平衡。

**关键区分**：ReMoGen 的模块化设计使其能够利用 HumanML3D 等大规模单人数据集预训练的通用先验，而上述基线均在交互数据上从头训练或联合训练，导致对稀缺交互数据的利用效率低下。

#### 1.2 人-场景交互（HSI）

在 LINGO 数据集上，ReMoGen 与两个专用基线对比：

- **TRUMANS**：HSI 基线，FID 为 4.731（Table 2），在所有指标上均被 ReMoGen 显著超越（FID 1.201）。
- **LINGO**：同数据集基线，同样在各项指标上落后于 ReMoGen。

ReMoGen 的优势源于其 Meta-Interaction 模块将场景占用体积编码为独立的条件分支，通过 FiLM 调制注入冻结的运动先验，而非将场景信息与运动生成联合建模。这种设计避免了场景信息对运动先验的侵蚀，同时保持了跨域迁移的灵活性。

#### 1.3 混合交互（Mixed-Modality）

在 EgoBody 数据集上，ReMoGen 展示了其模块化框架的独特优势：

- **零样本组合（Zero-shot composition）**：直接组合 HHI 和 HSI 的 Meta-Interaction 模块，无需在混合数据上训练即可生成合理的混合交互动作，这得益于多分支加权融合机制（Eq. 7）。
- **先验初始化微调**：使用通用先验初始化并微调仅 2k 步，FID 达到 2.757（Table 3），优于从头训练 500k 步的 2.341；微调 65k 步后 FID 进一步降至 0.292，远超从头训练的极限。

这一结果验证了 ReMoGen 的核心设计理念：通用先验提供了跨域共享的运动结构，而轻量适配器实现了对特定交互域的快速适应。

### 2. 适用边界与局限

尽管 ReMoGen 在多个基准上取得了领先结果，其设计仍存在明确的适用边界：

1. **细粒度空间精度受限**：ReMoGen 使用潜在扩散模型作为运动先验，压缩的潜在空间可能损害细粒度空间精度。这在近距离接触（如握手、拥抱）或高精度人-物交互场景中尤为突出。论文在 Limitations 中明确指出这一点，并建议未来工作探索更精细的空间表示。

2. **多分支融合策略非最优**：当前采用简单的加权求和（Eq. 7）组合多个 Meta-Interaction 模块的输出，并辅以 L2 范数裁剪。这种硬编码的组合策略在混合交互设置中可能并非最优，更有效的免训练融合方法可能进一步提升性能。

3. **对历史窗口的依赖**：ReMoGen 的自回归生成依赖固定长度的历史窗口（H=2 段，每段 8 帧），对于需要更长时序依赖的交互行为（如长时间协作任务），可能面临上下文不足的问题。

4. **文本条件并非必需**：消融实验（Fig. B）表明，即使移除文本输入或输入冲突文本，ReMoGen 仍能生成物理合理的交互动作。这说明 Meta-Interaction 模块对动态交互线索的响应独立于文本条件，但也暗示文本控制在某些场景下可能不够强。

### 3. 开放问题与后续方向

基于上述局限，论文提出了以下开放问题：

1. **如何进一步提高近距离接触或高精度交互中的细粒度空间精度？** 可能的路径包括：引入接触图或距离场等显式空间约束，或在潜在空间中引入更高分辨率的表示。

2. **能否设计更有效的训练无关融合方法，以便在混合交互设置中实现更好的性能？** 当前的多分支加权融合需要手动设定系数，自适应的、基于上下文或不确定性的融合策略值得探索。

3. **如何将 ReMoGen 的模块化框架扩展到更多交互模态？** 当前仅覆盖人-人和人-场景两种模态，未来可扩展到人-物交互（HOI）、多智能体交互等更复杂的场景。

4. **FWSR 的进一步优化**：虽然 FWSR 在几乎不增加延迟的情况下显著改善了质量（FID 从 0.181 降至 0.166，延迟仅从 0.042 s 增至 0.047 s），但其轻量级适配器的设计空间尚未被充分探索，可能存在更高效的逐帧细化策略。

### 4. 在知识库中的定位

ReMoGen 在交互运动生成领域的方法谱系中占据以下位置：

- **相对于端到端方法**（如 ReGenNet、FreeMotion）：ReMoGen 代表了从“在稀缺交互数据上端到端学习”到“大规模先验 + 轻量适配”的范式转变。这一思路与 NLP 中的预训练-微调范式、计算机视觉中的基础模型适配思路一脉相承。

- **相对于实时方法**（如 SymBridge）：ReMoGen 证明了实时性并不必然以牺牲质量为代价。通过 FWSR 机制，它在保持低延迟的同时实现了与离线方法相当甚至更优的生成质量。

- **相对于单域方法**（如 TRUMANS、LINGO）：ReMoGen 的模块化设计使其天然支持多域融合和零样本迁移，这在现有交互生成方法中尚属首次。

- **方法谱系定位**：ReMoGen 可被归类为 **“基于预训练运动先验的模块化交互生成框架”**，其核心贡献在于将冻结先验、FiLM 调制和逐帧细化组合为一个统一的实时推理管线。这一设计范式对后续交互生成工作具有重要的参考价值。



## 原文 PDF

![[paperPDFs/CVPR_2026/ReMoGen_Real_time_Human_Interaction_to_Reaction_Generation_via_Modular_Learning_from_Diverse_Data.pdf]]
