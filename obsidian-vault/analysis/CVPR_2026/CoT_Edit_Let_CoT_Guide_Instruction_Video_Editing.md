---
title: "CoT-Edit: Let CoT Guide Instruction Video Editing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CoT_Edit_Let_CoT_Guide_Instruction_Video_Editing.pdf
project_link: null
code_link: "https://github.com/flying-sky999/CoT-Edit"
aliases:
- CE
- CoT-Edit
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在编辑执行前引入结构化规划（CoT MLLM规划器），将高层语义指令显式地转换为边界框序列和增强语义描述，从而解耦空间推理与外观生成。
primary_logic: 通过‘规划–引导–编辑’（Plan–Guide–Edit）范式，将语义意图到像素执行的过程分解为可解释的步骤：CoT增强的MLLM规划器解析指令并生成时域一致的边界框和丰富指令；边界框引导的掩码生成器将全局检索转化为局部细化；扩散编辑器融合掩码、增强指令和视频特征，实现空间精确、时间连贯且物理一致的编辑。
claims:
- 在Gemini评估中，CoT-Edit在空间关系（Spatial Relation）指标上达到0.841，物理规则（Physical Rule）达到0.741，显著优于所有基线方法。
- 消融实验表明，引入Qwen3-VL作为指令增强模块使指令遵循（IF）从0.575提升至0.598；同时使用Mask-Connector和Reverse-Connector使整体编辑质量（OEQ）达到0.647。
- 定性结果（Fig.4）显示，CoT-Edit在复杂多物体场景中能更精确地定位目标，保持未编辑区域，并处理物理感知指令。
- 自定义评估集（Gemini评分） 上 Spatial Relation (SR) = 0.841
---

# CoT-Edit: Let CoT Guide Instruction Video Editing

> [!tip] 核心洞察
> 通过‘规划–引导–编辑’（Plan–Guide–Edit）范式，将语义意图到像素执行的过程分解为可解释的步骤：CoT增强的MLLM规划器解析指令并生成时域一致的边界框和丰富指令；边界框引导的掩码生成器将全局检索转化为局部细化；扩散编辑器融合掩码、增强指令和视频特征，实现空间精确、时间连贯且物理一致的编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | CoT-Edit：让思维链指导指令视频编辑 |
| 英文题名 | CoT-Edit: Let CoT Guide Instruction Video Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Liang_CoT-Edit_Let_CoT_Guide_Instruction_Video_Editing_CVPR_2026_paper.html) · [Code](https://github.com/flying-sky999/CoT-Edit) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CoT-Edit |
| Dataset | 自定义评估集（Gemini评分） |

> [!tip] 效果简介
> - 自定义评估集（Gemini评分） 上，Spatial Relation (SR) 0.841 vs N/A (最佳基线未明确) (显著提升)；Physical Rule (PR) 0.741 vs N/A (最佳基线未明确) (显著提升)。

## 概要

纯文本指令驱动的视频编辑面临一个根本瓶颈：高层语义指令缺乏显式的空间定位与物理约束，导致编辑过程中出现目标歧义、定位漂移以及物理不合理性。本文提出 **CoT-Edit**，一种“规划–引导–编辑”（Plan–Guide–Edit）框架，通过将语义意图到像素执行的过程分解为可解释的步骤，系统性地解决了上述问题。其核心机制是：一个基于思维链（Chain-of-Thought, CoT）增强的多模态大语言模型（MLLM）规划器，在编辑执行前对视频和指令进行结构化推理，显式地生成时域一致的边界框序列和增强语义描述，从而将空间推理与外观生成解耦。

CoT-Edit 包含三个核心模块：**Planner**（规划器）负责语义-空间规划，接收关键帧和编辑指令，通过多步 CoT 推理输出边界框序列和增强指令；**Guide**（引导分支）基于边界框先验生成时空一致的掩码，并通过 Reverse-Connector 接收编辑器的反馈以修正掩码细节；**Editor**（编辑器）基于 Wan2.2 5B 扩散模型，融合增强指令、掩码特征和视频特征进行条件生成，通过 Mask-Connector 引入空间引导。这种双向连接器设计使得掩码生成与扩散编辑能够相互协作，共同提升编辑精度。

在方法谱系中，CoT-Edit 区别于仅依赖文本指令的端到端方法（如 **InstructVid2Vid**（Qin et al., ICME 2024）、**InsV2V**（Cheng et al., arXiv 2023）），以及基于 MLLM 引导的 **InstructX** 和大规模指令编辑方法 **InsViE-1M**（Wu et al., ICCV 2025）。其关键创新在于将空间先验的来源从隐式的文本约束升级为显式的时域边界框序列，并通过双向连接器实现掩码与编辑的协同优化。

实验结果表明，CoT-Edit 在空间关系和物理规则两个关键维度上取得了显著优势。在基于 Gemini 评估的自定义测试集上，空间关系（Spatial Relation）指标达到 0.841，物理规则（Physical Rule）达到 0.741，均显著优于现有基线方法。消融实验进一步验证了各组件的作用：引入 Qwen3-VL 指令增强模块使指令遵循（Instruction Following）从 0.575 提升至 0.598；同时使用 Mask-Connector 和 Reverse-Connector 使整体编辑质量（Overall Editing Quality）达到最高的 0.647。定性结果（Figure 4）显示，CoT-Edit 在复杂多物体场景中能够更精确地定位目标、保持未编辑区域，并忠实处理物理感知指令。

### 指令视频编辑的核心瓶颈

文本驱动的指令视频编辑旨在根据自然语言指令（如“将黄狗替换为橙色的猫”或“在天空中添加沿椭圆轨迹飞行的UFO”）修改视频内容。尽管扩散模型在图像和视频生成领域取得了显著进展，但现有编辑方法普遍面临一个根本性瓶颈：**纯文本指令缺乏显式的空间定位和物理约束**，导致编辑过程中出现目标歧义、定位漂移和物理不合理性。

具体而言，文本指令仅提供高层语义意图，无法精确指定编辑目标的空间位置、运动轨迹和物理交互规则。当指令涉及多物体空间关系（如“将桌上的苹果移到杯子左边”）或物理感知操作（如“让球弹跳并最终停在角落”）时，仅依赖文本条件的模型难以将语义意图映射为像素级的精确执行，常出现编辑目标错误、未编辑区域受损或运动不连贯等问题（参见 Figure 1）。

### 现有方法的缺口

当前指令视频编辑方法主要分为两类：

1. **端到端文本条件编辑**：如 **InstructVid2Vid**（Qin et al., ICME 2024）、**InsV2V**（Cheng et al., arXiv 2023）、Ditto 和 Lucy-1.1 等方法，直接使用文本指令通过交叉注意力机制驱动视频编辑。这类方法虽然简洁，但完全依赖文本的隐式空间推理能力，在处理需要精确空间定位的指令时表现不佳。

2. **基于 MLLM 引导的编辑**：如 InstructX 等方法尝试引入多模态大语言模型（MLLM）辅助理解编辑意图，但仍缺乏将语义推理结果转化为可执行的空间约束（如边界框、掩码等显式先验）的有效机制。

上述方法的共同缺陷在于：**语义推理与空间执行之间缺乏显式的桥梁**。文本指令的模糊性使得模型难以准确定位编辑目标、保持时空一致性，并遵守物理常识。

### 本文动机

针对上述问题，本文的核心动机是：**在编辑执行前引入结构化规划，将高层语义指令显式地转换为空间约束和增强语义描述，从而解耦空间推理与外观生成**。

具体而言，本文提出 **CoT-Edit** 方法，通过以下思路解决指令视频编辑的核心挑战：

- **思维链规划**：利用 CoT 增强的 MLLM 规划器对视频关键帧和编辑指令进行逐步推理，生成时域一致的边界框序列和增强指令，为后续编辑提供精确的空间先验。
- **规划–引导–编辑范式**：将编辑过程分解为三个协同模块——Planner 负责语义到空间的转换，Guide 负责边界框引导的掩码生成，Editor 负责融合掩码、增强指令和视频特征的条件生成。
- **双向协作机制**：通过 Mask-Connector 和 Reverse-Connector 实现 Guide 与 Editor 之间的双向信息流动，确保掩码精度与编辑质量相互促进。

通过上述设计，CoT-Edit 旨在实现空间精确、时间连贯且物理一致的指令视频编辑，弥补现有方法在空间推理与物理合理性方面的不足。

## 核心方法与创新机理

CoT-Edit 的根本创新在于将“规划–引导–编辑”（Plan–Guide–Edit）范式引入指令视频编辑，通过**显式空间先验的解耦注入**，弥补了纯文本驱动方法在目标定位、时空一致性和物理合理性上的结构性缺陷。其核心创新可归纳为三个紧密耦合的 changed slots。

### 1. 空间先验来源：从隐式文本到显式时域边界框

传统文本指令视频编辑（如 **InstructVid2Vid** (Qin et al., ICME 2024)、**InsV2V** (Cheng et al., arXiv 2023)）仅依赖文本指令驱动编辑，缺乏对“在哪里编辑”的空间约束，导致目标歧义和定位漂移。CoT-Edit 用 **CoT MLLM 规划器**替代隐式语义推理：规划器接收关键帧序列与用户指令，通过链式思维推理显式输出**关键帧对齐的边界框序列**和**增强语义指令**（Sec. 3.1, Figure 3）。这一 changed slot 将空间推理从扩散模型的隐式注意力中剥离，使编辑区域的位置信息成为可解释、可监督的显式先验。

### 2. 掩码生成方式：从隐式生成到边界框约束的双向协作

基线方法通常从文本指令隐式生成编辑掩码或依赖注意力图，缺乏对目标区域的精确控制。CoT-Edit 引入**边界框约束的掩码预测器（Guide 分支）**，将规划器输出的边界框先验转化为时空一致的掩码序列（Sec. 3.2）。更重要的是，Guide 与 Editor 之间通过两类连接器实现**双向特征交互**：
- **Mask-Connector** 将掩码特征注入 Editor 各层，提供“在哪里编辑”的空间引导（Eq. 3）；
- **Reverse-Connector** 将 Editor 的高层语义特征反向传递至 Guide，修正掩码细节（Eq. 2）。

这一设计将掩码生成从单向流水线升级为**双向协作优化**，使掩码既受显式边界框约束，又能从编辑结果中获得反馈修正。

### 3. 编辑条件注入：从单一文本到多模态特征融合

基线方法仅通过交叉注意力注入文本条件，对复杂物理感知指令的理解能力有限。CoT-Edit 的 Editor 同时注入三类互补条件：
- **增强指令特征**：通过 Qwen-VL 交叉注意力注入 MLLM 的视觉语言特征，提升指令理解深度（Eq. 4）；
- **掩码特征**：通过 Mask-Connector 注入空间引导信号；
- **视频潜在特征**：通过通道拼接保留原视频的时序结构（Eq. 1）。

这种多模态条件融合机制使 Editor 能够在理解“做什么”的同时，精确获知“在哪里做”，从而在空间关系（SR=0.841）和物理规则（PR=0.741）指标上取得显著优势（Table 1）。

### 4. 训练策略：分阶段模块化训练

与端到端大规模训练不同，CoT-Edit 采用**分阶段训练策略**：先对各模块单独训练（第一阶段 20k steps），再联合微调（第二阶段 10k steps，batch size 64）。这种策略降低了多模块耦合训练的难度，使每个组件在联合优化前已具备基本能力。

**创新本质总结**：CoT-Edit 的核心突破不在于提出新的扩散架构，而在于通过“规划–引导–编辑”范式将语义意图到像素执行的过程**分解为可解释的中间表示**（边界框、掩码、增强指令），并通过双向连接器实现模块间的信息闭环。这一设计使空间推理与外观生成解耦，从而在保持生成质量的同时，显著提升了对复杂空间关系和物理约束指令的执行精度。

CoT-Edit 提出“规划–引导–编辑”（Plan–Guide–Edit）范式，将语义意图到像素执行的映射分解为三个可解释的阶段，从而系统性地解决纯文本指令视频编辑中目标歧义、空间漂移和物理不合理等瓶颈。整个框架由三个核心模块构成：**Planner（规划器）**、**Guide（引导分支）** 和 **Editor（编辑器）**，并通过双向连接器实现模块间的协同。

### 输入–输出流

给定一段原始视频 $y_0$ 和一条高层语义编辑指令，系统首先从视频中采样时域有序的关键帧序列。Planner 接收关键帧和指令，经过链式思维（Chain-of-Thought, CoT）推理，同步输出两类结构化信息：**（1）与关键帧对齐的边界框序列**，为编辑区域提供显式空间先验；**（2）增强语义指令**，将原始简短指令扩展为包含属性、关系和物理约束的丰富描述。Guide 分支以边界框先验和视频特征为输入，生成时空一致的编辑掩码，并通过 Reverse-Connector 接收 Editor 的高层语义反馈以修正掩码细节。Editor 分支则融合增强指令（经 Qwen-VL 编码）、掩码特征和原始视频特征，在扩散生成过程中实现空间精确且时间连贯的编辑。

### 模块间协作机制

框架的关键创新在于 Guide 与 Editor 之间的**双向信息流动**。具体而言：

- **Mask-Connector** 将 Guide 生成的掩码特征 $C_l^M$ 投射为对 Editor 特征 $Q_l^E$ 的加性调制：
  $$Q_{l}^{E} = Q_{l}^{E} + \mathrm{Mask\_Connector}(C_{l}^{M})$$
  这使 Editor 在每一层都能获得“在哪里编辑”的空间引导。

- **Reverse-Connector** 则将 Editor 的高层语义特征 $Q_l^E$ 反向传递至 Guide，对掩码特征进行修正：
  $$C_{l}^{M} = C_{l}^{M} + \mathrm{Reverse\_Connector}(Q_{l}^{E})$$
  这一反向通路有助于恢复掩码中可能丢失的细节，使掩码更贴合编辑目标。

- **Qwen-VL 交叉注意力注入**进一步将多模态大语言模型的视觉语言理解能力融入 Editor：
  $$Q_{l}^{E} = Q_{l}^{E} + \mathbf{QVLcrossattn}(\mathbf{MLP}(V), C_{l}^{M})$$
  其中 $V$ 为 Qwen-VL 提取的视觉语言特征，经 MLP 投影后通过交叉注意力注入，并受掩码特征调制，实现语义理解与空间定位的深度融合。

### 训练策略

为稳定训练并充分发挥各模块能力，CoT-Edit 采用分阶段训练策略：首先对 Planner、Guide 和 Editor 进行模块化单独预训练，随后在内部构建的 10 万对编辑数据上进行联合微调。这种策略避免了端到端大规模训练中模块间梯度冲突的问题，同时保证了各组件在联合优化前已具备基本能力。

### 补充图表

![[assets/figures/papers/paper_list_l2300_https_openaccess_thecvf_com_content_CVPR2026_html_Liang_CoT_Edit_Let_CoT/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed “Plan–Guide–Edit” framework for instruction-based video editing. Given a video and an instruction, a CoT-enhanced VLM planner performs step-by-step analysis to produce an enriched instruction and a temporal sequence of bounding boxes. The Guide branch turns these spatial priors into spatio-temporally consistent masks, while the Editor fuses text, video features, and mask guidance through bidirectional connectors to render the final edited video*

CoT-Edit 的“规划–引导–编辑”（Plan–Guide–Edit）框架由三个核心模块构成：**Planner**（规划器）、**Guide**（引导分支）和 **Editor**（编辑器），并通过两个双向连接器实现模块间的信息交互。

### Planner：CoT增强的MLLM规划器

Planner 接收视频关键帧序列和用户编辑指令，通过链式思维（Chain-of-Thought）推理，输出两项结构化结果：(1) 与关键帧对齐的边界框序列；(2) 增强后的语义指令。推理过程分解为三个阶段（Figure 3）：

![[assets/figures/papers/paper_list_l2300_https_openaccess_thecvf_com_content_CVPR2026_html_Liang_CoT_Edit_Let_CoT/figures/003_Figure_3.jpg]]
*Figure 3: Chain-of-Thought (CoT) reasoning process of the MLLM planner. Given an editing instruction and keyframes, the planner follows a five-step procedure: it parses the task type and target object, performs cross-frame perception and temporal analysis, enforces physics- and cinematography-aware consistency, synthesizes an enriched instruction, and finally outputs the enriched instruction together with a temporally coherent sequence of normalized bounding boxes in a fixed format*

- **任务解析与跨帧感知**：识别任务类型和目标物体，在关键帧间建立对应关系；
- **物理与时序一致性建模**：施加物理规则和运动学约束，确保边界框序列在时间上连贯且物理合理；
- **空间与语义引导生成**：综合以上分析，输出规范化的边界框坐标和丰富化的指令文本。

### Editor：扩散编辑器的输入构建

Editor 基于 Wan2.2 5B 扩散模型。其输入构建方式为：将噪声潜在变量 $y_{\mathrm{noise}}$ 与原始视频潜在变量 $y_{0}$ 沿通道维拼接：

$$y_{\mathrm{input}} = \mathrm{ChannelConcat}(y_{\mathrm{noise}}, y_{0}) \tag{1}$$

这一设计使扩散模型在去噪过程中始终保留原始视频的结构信息，为后续的空间引导和语义注入提供稳定的条件基础。

### Guide与Editor的双向协作

Guide 分支根据 Planner 输出的边界框先验生成时空一致的掩码，Editor 分支则融合增强指令、掩码特征和视频特征进行条件生成。两者通过两个连接器实现双向信息流动：

**Reverse-Connector（反向连接器）** 将 Editor 第 $l$ 层的特征 $Q_{l}^{E}$ 反向传递至 Guide，对掩码特征 $C_{l}^{M}$ 进行残差修正，帮助恢复掩码细节：

$$C_{l}^{M} = C_{l}^{M} + \mathrm{Reverse\_Connector}(Q_{l}^{E}) \tag{2}$$

**Mask-Connector（掩码连接器）** 将 Guide 生成的掩码特征 $C_{l}^{M}$ 投射为对 Editor 特征 $Q_{l}^{E}$ 的加性调制，显式注入空间引导信号：

$$Q_{l}^{E} = Q_{l}^{E} + \mathrm{Mask\_Connector}(C_{l}^{M}) \tag{3}$$

### Qwen-VL交叉注意力注入

为进一步增强 Editor 的指令理解能力，引入 MLLM（Qwen-VL）的视觉语言特征。经过 MLP 投影的 Qwen-VL 特征 $V$ 通过交叉注意力注入 Editor，并受掩码特征 $C_{l}^{M}$ 调制：

$$Q_{l}^{E} = Q_{l}^{E} + \mathbf{QVLcrossattn}(\mathbf{MLP}(V), C_{l}^{M}) \tag{4}$$

该设计将 MLLM 的深层语义理解与 Guide 的空间先验在 Editor 内部融合，使编辑过程同时具备语义准确性和空间精确性。消融实验（Table 2）表明，引入 Qwen3-VL 指令增强模块使指令遵循（IF）从 0.575 提升至 0.598；同时使用 Mask-Connector 和 Reverse-Connector 使整体编辑质量（OEQ）达到最高的 0.647。

## 实验与关键发现

### 定量主结果

CoT-Edit在自定义评估集上通过Gemini评分与多个基线进行了对比，涵盖视觉质量与编辑质量两个维度。Table 1给出了完整数值。在空间关系（Spatial Relation, SR）指标上，CoT-Edit达到**0.841**，在物理规则（Physical Rule, PR）上达到**0.741**，两项均显著优于**InstructVid2Vid**（Qin et al., ICME 2024）、**InsV2V**（Cheng et al., arXiv 2023）、**Ditto**、**Lucy-1.1**、**InstructX**和**InsViE-1M**（Wu et al., ICCV 2025）等基线方法。这一结果直接验证了Plan–Guide–Edit框架的核心假设：将语义意图显式地分解为结构化规划（边界框序列与增强指令）能有效解决纯文本指令编辑中的空间歧义和物理不合理性问题。在视觉质量维度（FVD、背景一致性BC、时序一致性TC、运动平滑度MS、美学评分AES）上，CoT-Edit同样保持领先或竞争性表现，表明空间先验的注入并未牺牲生成质量。

### 消融实验

Table 2报告了组件消融的完整结果，分析围绕四个关键设计展开。

**MLLM指令增强的有效性。** 对比“E w/o MLLM”与“E w/ MLLM”两组配置：引入Qwen3-VL作为指令增强模块后，指令遵循（IF）从0.575提升至**0.598**。该增益虽非巨大，但结合定性观察可知，MLLM特征主要贡献于对复杂语义和隐含物理约束的理解，而非简单的文本匹配。

**Mask分支与双向连接器的协同。** 消融的核心发现集中于Mask-Connector和Reverse-Connector的贡献。仅使用Mask-Connector（E+M w/ Mc）时，整体编辑质量OEQ为0.633；同时引入Reverse-Connector（E+M w/ Mc&Rc）后，OEQ达到最高的**0.647**。这一差距揭示了双向信息流的关键作用：Mask-Connector将Guide的掩码特征注入Editor以提供空间引导（Eq. 3），而Reverse-Connector则利用Editor的高层语义特征反向修正Guide的掩码细节（Eq. 2），二者协同实现了“定位－生成－修正”的闭环。

**CoT推理范式的贡献。** 移除CoT推理而仅保留边界框输出时，空间关系SR和物理规则PR均出现明显下降。这表明结构化的链式思维过程——依次进行任务解析、跨帧感知、物理与时序一致性建模、增强指令合成——是规划器输出高质量空间先验的前提条件，而非简单的边界框预测所能替代。

### 定性分析

Figure 4展示了CoT-Edit与开源基线的定性对比。在“添加一个以椭圆轨迹飞行的UFO”这类涉及复杂运动路径的指令中，CoT-Edit能精确地将UFO定位于天空区域并保持椭圆轨迹，而基线方法常出现目标漂移或错误区域编辑。在“将黄狗变为橘猫”这类多物体场景中，CoT-Edit仅修改目标物体而完整保留未编辑区域，基线方法则普遍存在背景破坏或相邻物体误编辑。Figure 5进一步通过CoT消融的定性结果验证：移除CoT后，编辑目标出现定位偏差和属性不一致，直接佐证了结构化推理对空间精确性的因果作用。

### 失败模式与局限

尽管整体表现优异，分析中仍可识别出若干边界情形。在大规模多物体交互场景中，MLLM规划器的计算开销和边界框预测的鲁棒性可能成为瓶颈——当场景包含五个以上交互物体且指令涉及复杂空间关系时，规划器输出的边界框序列可能出现漏检或时序不一致。此外，训练数据依赖合成视频编辑对，在真实场景（如手持拍摄、剧烈光照变化）中的泛化性仍需进一步验证。这些局限在原文中未被系统量化，建议在实际部署前进行针对性评估。

### 补充图表

![[assets/figures/papers/paper_list_l2300_https_openaccess_thecvf_com_content_CVPR2026_html_Liang_CoT_Edit_Let_CoT/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of CoT-Edit and baseline models on visual and editing quality metrics*

![[assets/figures/papers/paper_list_l2300_https_openaccess_thecvf_com_content_CVPR2026_html_Liang_CoT_Edit_Let_CoT/figures/007_Table_2.jpg]]
*Table 2: Ablation study results on video editing. Higher is better. PR, SR, IF, and OEQ denote physical plausibility, spatial relations, instruction following, and overall editing quality, respectively*

![[assets/figures/papers/paper_list_l2300_https_openaccess_thecvf_com_content_CVPR2026_html_Liang_CoT_Edit_Let_CoT/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison of CoT-Edit and open-source baselines, showing more precise target localization, better preservation of non-edited regions, and more faithful handling of complex, physics-aware editing instructions*

![[assets/figures/papers/paper_list_l2300_https_openaccess_thecvf_com_content_CVPR2026_html_Liang_CoT_Edit_Let_CoT/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative results of the CoT ablation study*

## 定位与知识库关联

### 任务定位与核心差异

CoT-Edit 面向**指令驱动的视频编辑**（instruction-based video editing），其核心瓶颈在于纯文本指令缺乏显式的空间定位与物理约束，导致编辑目标歧义、定位漂移和物理不合理性。与现有方法相比，CoT-Edit 的根本差异在于将“语义意图→像素执行”的过程显式解耦为“规划–引导–编辑”（Plan–Guide–Edit）三阶段范式，从而在编辑执行前引入结构化空间推理。

在方法谱系上，现有指令视频编辑方法可大致分为两类：

- **端到端文本条件编辑**：如 **InstructVid2Vid**（Qin et al., ICME 2024）、**InsV2V**（Cheng et al., arXiv 2023）、**Ditto**、**Lucy-1.1** 等，直接从文本指令生成编辑结果，缺乏显式的空间先验，因而在复杂空间关系和物理一致性上表现受限。
- **MLLM 引导编辑**：如 **InstructX**、**InsViE-1M**（Wu et al., ICCV 2025）等，开始引入多模态大模型辅助理解指令，但通常仅用于生成增强文本，仍未将空间约束以结构化形式注入编辑过程。

CoT-Edit 的关键突破在于：不仅用 MLLM 理解指令，更通过 **CoT 增强的规划器** 将理解结果转化为**时域一致的边界框序列**和**增强语义描述**，使空间推理与外观生成彻底解耦。这一设计使模型在空间关系（Spatial Relation）和物理规则（Physical Rule）等维度上获得了显著优势（Table 1 中 SR 达 0.841，PR 达 0.741）。

### 关键设计槽位对比

下表总结了 CoT-Edit 相对于基线方法在核心设计槽位上的改变：

| 设计槽位 | 基线方法 | CoT-Edit | 证据锚点 |
|---------|---------|---------|---------|
| 空间先验来源 | 仅依赖文本指令（无显式空间约束） | CoT MLLM 规划器生成的时域边界框序列 + 增强指令 | Sec. 3.1 |
| 掩码生成方式 | 从原始文本指令隐式生成或基于注意力 | 边界框约束的掩码预测器（Guide 分支），通过 Reverse-Connector 与 Editor 双向协作 | Sec. 3.2 |
| 编辑条件注入 | 仅通过交叉注意力注入文本 | 注入增强指令（Qwen-VL 特征）和掩码特征，并引入双向连接器（Mask-Connector, Reverse-Connector） | Sec. 3.3 |
| 训练策略 | 端到端大规模数据训练 | 分阶段训练（先模块化单独训练，再联合微调） | Abstract, Sec. 4.1 |

其中，**双向连接器**（Mask-Connector 与 Reverse-Connector）的设计是掩码引导编辑的关键机制：Mask-Connector 将 Guide 生成的掩码特征以加性调制方式注入 Editor 各层（Eq. 3），提供“在哪里编辑”的空间引导；Reverse-Connector 则反向将 Editor 的高层语义特征传回 Guide（Eq. 2），修正掩码细节。消融实验（Table 2）表明，同时使用两个连接器（E+M w/ Mc&Rc）使整体编辑质量（OEQ）达到最高的 0.647，验证了这一双向协作机制的有效性。

### 适用边界与局限

CoT-Edit 的设计决定了其适用边界：

1. **依赖 MLLM 规划器的推理质量**：规划器的 CoT 推理过程（Fig. 3 所示的五步流程）是整个框架的空间先验来源。当指令涉及极度复杂的多物体交互或需要细粒度物理模拟时，MLLM 生成的边界框序列和增强指令的准确性可能成为瓶颈。论文未提供大规模多物体交互场景下的系统评估，该边界需要进一步验证。

2. **训练数据依赖**：框架采用分阶段训练策略（先模块化单独训练 20k 步，再联合微调 10k 步，基于 100k 内部数据对），对合成训练数据的质量和覆盖范围有一定依赖。如何降低这一依赖以提升真实场景泛化性，是论文指出的开放问题之一。

3. **计算效率**：引入 MLLM 规划器和双向连接器增加了推理开销。论文未详细讨论在大规模多物体交互场景下 MLLM 规划器的计算效率与鲁棒性，这在实际部署中可能构成限制。

### 开放问题

基于论文的分析和实验设置，以下问题值得后续工作关注：

- **大规模多物体交互场景下 MLLM 规划器的计算效率与鲁棒性**：当前评估集规模和场景复杂度未明确，规划器在更复杂场景下的推理质量和效率有待进一步检验。
- **降低对合成训练数据的依赖**：分阶段训练策略依赖内部数据对，如何利用自监督或弱监督信号减少对人工标注/合成数据的依赖，是提升真实场景泛化性的关键方向。
- **物理一致性的更深层建模**：虽然 CoT-Edit 在 Physical Rule 指标上显著优于基线（0.741），但该指标的绝对分数仍有提升空间。是否需要在 Guide 或 Editor 中引入显式的物理模拟模块，值得探索。

> **注意**：上述局限和开放问题中，关于“大规模多物体交互场景下的鲁棒性”和“对合成数据依赖的降低”来自论文自身指出的开放问题；关于“计算效率”和“物理一致性的更深层建模”是基于方法设计的合理推断，需结合后续实验进行手动验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/CoT_Edit_Let_CoT_Guide_Instruction_Video_Editing.pdf]]
