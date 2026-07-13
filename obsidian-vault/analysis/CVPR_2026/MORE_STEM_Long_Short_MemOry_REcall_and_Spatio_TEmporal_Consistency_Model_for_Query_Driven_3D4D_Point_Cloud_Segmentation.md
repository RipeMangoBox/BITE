---
title: "MORE-STEM: Long-Short MemOry REcall and Spatio-TEmporal Consistency Model for Query-Driven 3D/4D Point Cloud Segmentation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MORE_STEM_Long_Short_MemOry_REcall_and_Spatio_TEmporal_Consistency_Model_for_Query_Driven_3D_4D_Point_Cloud_Segmentation.pdf
project_link: null
code_link: null
aliases:
- MS
- MORE-STEM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入长短期记忆召回与时空一致性模型的联合框架，通过文本-视觉跨帧对齐、状态空间时序传播和分级记忆机制，统一解决静态与动态场景下的查询驱动分割。核心干预点在于同时建模体素级的时空一致性（STEM）和分层记忆召回（LTM+STM），使语言查询能够动态地与多帧几何特征对齐。
primary_logic: 将语言查询与多帧点云特征进行时间感知的跨模态对齐，并利用长短期记忆模块平衡长期跨场景语义召回与短期帧级连续性，同时通过状态空间模型和可控制Transformer实现体素级时空一致性，从而实现稳定且连贯的4D点云理解。
claims:
- 在Instruct3D指令分割上，MORE-STEM以mIoU 35.9、Acc 31.4大幅超越此前最优方法SegPoint的31.6和27.5，分别提升4.3和3.9个点。
- 在ScanRefer引用分割上，MORE-STEM取得mIoU 52.7、Acc@50 54.8的最佳性能，相比此前最优方法有显著提升。
- 消融实验表明，依次移除CFTVA、STEM、LTM、STM模块后，mIoU从35.9分别降至33.1、32.5、32.0、31.4，验证各模块的必要性。
- 在自行构建的InstructKITTI 4D基准上，方法在无直接前人工作对比的情况下取得Acc@50 42.19和mIoU 40.67，补充了动态场景指令分割的性能基线。
---

# MORE-STEM: Long-Short MemOry REcall and Spatio-TEmporal Consistency Model for Query-Driven 3D/4D Point Cloud Segmentation

> [!tip] 核心洞察
> 将语言查询与多帧点云特征进行时间感知的跨模态对齐，并利用长短期记忆模块平衡长期跨场景语义召回与短期帧级连续性，同时通过状态空间模型和可控制Transformer实现体素级时空一致性，从而实现稳定且连贯的4D点云理解。

| 字段 | 内容 |
|------|------|
| 中文题名 | MORE-STEM：面向查询驱动的3D/4D点云分割的长短记忆召回与时空一致性模型 |
| 英文题名 | MORE-STEM: Long-Short MemOry REcall and Spatio-TEmporal Consistency Model for Query-Driven 3D/4D Point Cloud Segmentation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_MORE-STEM_Long-Short_MemOry_REcall_and_Spatio-TEmporal_Consistency_Model_for_Query-Driven_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MORE-STEM |
| Dataset | Instruct3D, InstructKITTI, ScanRefer, SemanticKITTI |

> [!tip] 效果简介
> - Instruct3D 上，mIoU / Acc 35.9 / 31.4 vs 31.6 / 27.5 (SegPoint) (+4.3 / +3.9)。
> - InstructKITTI (3D) 上，Acc / mIoU 38.62 / 37.95 vs Not reported (SegPoint/3D-LLaVA would be lower) (N/A)。
> - ScanRefer (Referring) 上，mIoU / Acc@50 52.7 / 54.8 vs Prior best around 50/52 (estimated) (~+2-3)。

## 概要

### 问题与瓶颈

查询驱动的3D点云分割旨在根据自然语言指令或引用表达式，从场景中分割出对应的目标区域。然而，现有方法（如**SegPoint**（He et al., ECCV 2024）、**3D-LLaVA**（Deng et al., CVPR 2025）等）几乎完全局限于静态点云，面临两个根本性瓶颈：其一，无法在动态场景中保持时空一致性，导致分割结果在帧间漂移、缺乏时序连贯性；其二，缺乏有效的跨场景记忆召回机制，难以利用历史信息改善当前帧的推理质量。

### 核心思路

针对上述问题，本文提出 **MORE-STEM**（Long-Short MemOry REcall and Spatio-TEmporal Consistency Model），一个面向查询驱动3D/4D点云分割的统一框架。其核心洞察在于：将语言查询与多帧点云特征进行时间感知的跨模态对齐，并利用长短期记忆模块平衡长期跨场景语义召回与短期帧级连续性，同时通过状态空间模型和可控制Transformer实现体素级时空一致性，从而实现稳定且连贯的4D点云理解。

### 方法定位

MORE-STEM 在方法谱系上处于 **查询驱动分割 × 时序建模 × 记忆增强推理** 的交汇点。与仅处理静态输入的 **SegPoint**、**3D-STMN**（Wu et al., AAAI 2024）等方法不同，MORE-STEM 首次将查询驱动分割扩展到4D动态场景，并在框架层面引入了三个协同模块：跨帧文本-视觉对齐（CFTVA）、时空一致性模型（STEM）和长短期记忆召回（LTM+STM）。在时序建模维度，该方法区别于 **TASeg**（Wu et al., CVPR 2024）等仅做时序聚合的语义分割方法，也不同于 **Mamba4D**（Liu et al., CVPR 2025）等通用4D理解模型，其独特之处在于将语言查询作为跨帧对齐的锚点，并通过分级记忆实现可回溯的推理。

### 主要结果

在3D指令分割基准 Instruct3D 上，MORE-STEM 取得 mIoU 35.9、Acc 31.4，相较此前最优方法 **SegPoint**（mIoU 31.6, Acc 27.5）分别提升 4.3 和 3.9 个点（Table 1）。在 ScanRefer 引用分割任务上，方法同样取得 mIoU 52.7、Acc@50 54.8 的最佳性能（Table 3）。消融实验进一步表明，依次移除 CFTVA、STEM、LTM、STM 模块后，mIoU 从 35.9 分别降至 33.1、32.5、32.0、31.4，验证了各组件的必要性（Table 5）。此外，本文基于 SemanticKITTI 自动构建了首个户外4D指令分割基准 InstructKITTI（含超过15K对查询-掩码样本），MORE-STEM 在该基准的4D任务上取得 Acc@50 42.19、mIoU 40.67，为动态场景指令分割提供了初始性能基线。



### 3D点云理解：从静态到动态的范式迁移

点云理解是三维计算机视觉的核心任务之一，其目标是从离散、非结构化的三维点集中提取语义信息，服务于自动驾驶、机器人导航、增强现实等应用场景。近年来，随着大规模预训练模型和跨模态对齐技术的发展，**查询驱动的3D分割**（query-driven 3D segmentation）逐渐成为研究热点。该范式允许用户通过自然语言查询直接指定目标对象或区域，系统据此输出对应的分割掩码，从而摆脱了传统语义分割中固定类别体系的限制，实现了更灵活、开放的人机交互方式。

然而，现有查询驱动的3D分割方法——包括基于大语言模型的**SegPoint**（He et al., ECCV 2024）、通用3D多模态大模型**3D-LLaVA**（Deng et al., CVPR 2025）以及端到端引用分割方法**3D-STMN**（Wu et al., AAAI 2024）——均将研究焦点局限于**静态点云场景**。这些方法假设输入为单帧、冻结时刻的三维数据，忽视了真实世界中点云序列天然具备的时序属性。在自动驾驶等动态场景中，LiDAR传感器以固定频率持续采集环境点云，相邻帧之间蕴含着丰富的运动信息和时空关联，而现有方法无法有效利用这些时序信号。

### 核心瓶颈：时空一致性与长期语义关联的缺失

将查询驱动分割从静态3D扩展到动态4D场景，面临两个根本性挑战：

**其一，时空一致性的缺失。** 当语言查询作用于点云序列时，理想的分割结果应当在时序上保持稳定——同一对象在不同帧中的掩码应具有连贯的几何形态和语义归属。然而，现有方法对每一帧独立推理，缺乏帧间的特征传播与约束机制，导致分割结果在时序上出现抖动、漂移甚至对象身份切换。简单的帧聚合或循环融合策略（如**TASeg**的时序聚合，Wu et al., CVPR 2024）虽能在一定程度上缓解该问题，但无法在体素级别精细地建模运动感知的时序一致性。

**其二，长期语义关联的断裂。** 动态场景中的对象可能因遮挡、视角变化或进出视野而间歇性出现。人类在理解此类场景时，能够自然地调用记忆中的历史信息来辅助当前推理——例如，当“那辆红色轿车”暂时被卡车遮挡后重新出现时，我们仍能将其识别为同一对象。现有方法缺乏有效的跨场景记忆召回机制，无法存储和检索历史帧中的文本-视觉对应关系，导致每次推理都从零开始，丧失了利用历史信息改善当前帧分割的能力。

### 本文动机：统一框架下的长短期记忆与时空一致性建模

针对上述瓶颈，本文提出**MORE-STEM**（Long-Short MemOry REcall and Spatio-TEmporal Consistency Model），一个面向查询驱动3D/4D点云分割的统一框架。其核心设计理念在于：**将语言查询与多帧点云特征进行时间感知的跨模态对齐，并利用长短期记忆模块平衡长期跨场景语义召回与短期帧级连续性，同时通过状态空间模型和可控制Transformer实现体素级时空一致性。**

具体而言，MORE-STEM通过三个核心模块协同解决动态场景下的查询驱动分割问题：

- **跨帧文本-视觉对齐（CFTVA）**：建立文本查询与多帧3D/2D视觉特征之间的细粒度、时间感知对应关系，使语言信号能够动态地与不同时刻的几何特征对齐。
- **时空一致性模型（STEM）**：利用状态空间模型对体素特征进行帧间传播，并结合可控制3D Transformer进行帧内稀疏注意力精炼，确保分割结果在运动场景中的时空连贯性。
- **长短期记忆召回（LTM+STM）**：长期记忆存储加权的文本-视觉对以实现跨场景语义召回，短期记忆缓存近期掩码特征以维持帧间连续性，共同增强模型的时间推理能力。

此外，为填补动态场景查询驱动分割的基准空白，本文基于SemanticKITTI自动构建了**InstructKITTI**基准，包含超过15K对（查询，3D掩码）的户外4D指令分割数据，为后续研究提供了评测平台。

图1对比了传统3D引用/指令分割任务与本文提出的4D指令分割任务的差异：前者仅处理单帧静态点云，后者则要求模型在多帧动态序列中保持分割的时空一致性和语义连贯性。这一范式迁移对模型的时间建模能力提出了更高要求，也是MORE-STEM设计的根本出发点。



## 核心方法与创新机理

MORE-STEM 的核心创新在于首次将查询驱动的3D点云分割从静态场景拓展到动态4D场景，通过**跨帧文本-视觉对齐（CFTVA）**、**时空一致性模型（STEM）** 和**长短期记忆召回（LTM+STM）** 三个关键模块的联合设计，系统性地解决了现有方法在时序连贯性、跨场景语义关联和体素级一致性方面的根本缺陷。

### 从单帧到多帧：跨帧文本-视觉对齐（CFTVA）

现有查询驱动分割方法（如 **SegPoint**，He et al., ECCV 2024）仅在单帧内进行文本与点云的静态对齐，缺乏跨帧交互能力。MORE-STEM 的 CFTVA 模块引入了**时间感知的跨模态对齐**机制，其核心干预体现在三个层面：

1. **双向跨模态注意力精炼**：对每一帧的点特征和体素特征分别与对应图像特征进行交叉注意力计算，得到精细化表示 $F_{t}^{point'}$ 和 $F_{t}^{voxel'}$（见 Eq.(1)-(2)），使几何特征融入视觉语义信息。
2. **时序视觉token聚合**：将当前帧及历史帧的视觉特征 $[F_{t}^{vis'}, F_{t-1}^{vis'}, F_{t-2}^{vis'}]$ 与文本嵌入 $F^{txt'}$ 进行时序感知的注意力对齐（见 Eq.(3)），使语言查询能够动态地与多帧几何特征建立细粒度对应。
3. **时序对比学习约束**：通过对比损失 $\mathcal{L}_{align}$（见 Eq.(4)）强化对齐后的视觉特征与文本特征之间的区分性对应，确保模型在动态场景中能稳定地追踪查询目标。

这一设计将“文本-点云对齐”从静态的单一映射转变为动态的时序关联，为后续的时空一致性建模提供了基础。

### 从帧级聚合到体素级时空一致性：STEM 模块

现有方法在处理多帧数据时通常采用简单的帧聚合或循环融合（如 **TASeg** 的时序聚合，Wu et al., CVPR 2024），无法保持体素级的时序一致性，导致分割结果在帧间出现漂移。STEM 模块通过**状态空间模型（SSM）** 与**可控制3D Transformer** 的协同设计，实现了细粒度的时空一致性建模：

- **帧间状态传播**：对每个体素 $v$，利用状态空间模型进行隐状态更新 $h_{t}(v) = A h_{t-1}(v) + B [F_{t}^{pointalign}(v) \| F_{t}^{voxelalign}(v)]$（见 Eq.(5)），实现体素级特征的时序传播，有效捕捉运动信息。
- **帧内空间精炼**：通过可控制3D Transformer对当前帧内体素进行稀疏自注意力处理 $z_{t}(v) = \mathrm{Transformer}(Q_{t}, K_{t}, V_{t})$（见 Eq.(6)），增强空间结构一致性。
- **归一化融合**：将帧间传播与帧内精炼的特征进行归一化融合 $\tilde{f}_{t}(v) = \mathrm{Norm}(h_{t}(v) + z_{t}(v))$（见 Eq.(7)），得到最终时空一致表示。

与 **Mamba4D**（Liu et al., CVPR 2025）等基于状态空间模型的4D理解方法相比，STEM 的创新在于将 SSM 的时序传播能力与 Transformer 的空间精炼能力在体素级别进行显式融合，而非仅依赖单一的状态空间序列建模。

### 从无记忆到长短期分级记忆召回：LTM+STM

现有方法缺乏有效的跨场景记忆召回机制，无法利用历史信息改善当前帧推理。MORE-STEM 提出的长短期记忆召回模块通过分级记忆设计填补了这一空白：

- **长期记忆（LTM）**：存储加权文本-视觉对 $M_{LTM} = \{ w_{i} \cdot (f_{pair}^{i} : [F_{i}^{txt}, \tilde{f}_{i}]) \}$（见 Eq.(8)），实现跨场景语义召回。其关键创新在于**偏置权重更新机制** $w_{i}^{bias} = \frac{w_{i}^{init}}{\sum_{j \in c} w_{j}^{init}}$（见 Eq.(9)），通过动态调整类别内样本权重，防止高频类别在长期记忆中过度占据主导地位。消融实验表明，移除该机制后 mIoU 下降约 1.5 个点（见 Table 5）。
- **短期记忆（STM）**：缓存近期掩码特征，维持帧间连续性，确保分割结果在相邻帧之间平滑过渡。

这一分级记忆设计使模型能够同时平衡长期跨场景语义召回与短期帧级连续性，这是此前任何查询驱动分割方法（包括 **3D-LLaVA**，Deng et al., CVPR 2025 等通用多模态大模型）都不具备的能力。

### 基准构建：InstructKITTI 4D

为填补动态场景查询驱动分割基准的空白，MORE-STEM 基于 SemanticKITTI 自动构建了含有超过 15K 对（查询，3D掩码）的户外 4D 指令分割基准 InstructKITTI。这一基准的建立使得 4D 指令分割任务首次具备了可量化的评估平台，尽管其标签质量受源数据集和 VLM（Qwen3VL-7B）的影响，可能存在一定噪声。

### 消融验证

消融实验（Table 5）系统性地验证了各模块的必要性：完整模型在 Instruct3D 上取得 mIoU 35.9；依次移除 CFTVA、STEM、LTM、STM 后，mIoU 分别降至 33.1、32.5、32.0、31.4。其中 CFTVA 的移除导致最大幅度的性能下降（-2.8 mIoU），表明跨帧文本-视觉对齐是整个框架的基础性创新；而 LTM 和 STM 的独立贡献（分别 -0.5 和 -0.6 mIoU）则验证了分级记忆设计的互补性。



MORE-STEM 的整体设计围绕一个核心洞察展开：**将语言查询与多帧点云特征进行时间感知的跨模态对齐，并利用长短期记忆模块平衡长期跨场景语义召回与短期帧级连续性，同时通过状态空间模型和可控制 Transformer 实现体素级时空一致性**。整个框架由四个关键模块串联构成，形成一条从多模态输入到时空一致分割掩码的端到端推理管线。

### 输入与特征提取

框架接收三类输入：连续多帧点云、对应的 RGB 图像序列，以及一条自然语言文本查询。在进入核心模块之前，系统通过 Point-Voxel 双分支编码器提取四种基础特征表示：

- **点级特征** $f_{point}$：由轻量 Point Transformer 从原始点云中提取，保留细粒度的局部几何结构。
- **体素级特征** $f_{voxel}$：由带窗口偏移注意力的稀疏 3D Transformer 从体素化点云中提取，捕获更大范围的空间上下文。
- **图像特征** $f_{img}$：从同步的 RGB 帧中提取 2D 视觉语义信息。
- **文本特征** $f_{txt}$：由预训练语言模型（LLaMA2-7B）编码查询语句，生成语义嵌入。

这四类特征构成了后续所有模块的通用表示基础，其提取过程在图 Figure 2 中有完整展示。

![[assets/figures/papers/paper_list_l33_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MORE_STEM_Long_Shor/figures/002_Figure_2.jpg]]
*Figure 2: A general overview of the proposed network. Given multi-frame point clouds, RGB images, and a text query, four feature types*

### 模块化管线

四个核心模块按以下顺序组织，形成从“对齐 → 一致性 → 记忆增强 → 输出”的信息流：

1. **跨帧文本-视觉对齐（CFTVA）**：这是管线的入口模块，负责将文本查询与多帧视觉特征进行时间感知的跨模态对齐。具体而言，它首先通过双向交叉注意力将图像特征分别注入点特征和体素特征，得到精细化表示 $F_t^{point'}$ 和 $F_t^{voxel'}$（公式 1-2）；随后，将文本嵌入与当前帧及历史帧的视觉 token 进行时序注意力对齐，并通过对比学习损失 $\mathcal{L}_{align}$ 强化对齐后的视觉-文本对应关系（公式 3-4）。该模块的详细架构见 Figure 3。

2. **时空一致性模型（STEM）**：承接 CFTVA 输出的对齐特征，STEM 在体素级别同时建模帧间传播和帧内精炼。帧间传播采用状态空间模型，将前一帧的隐状态 $h_{t-1}(v)$ 与当前帧的对齐特征融合，更新为 $h_t(v)$（公式 5）；帧内精炼则通过可控制 3D Transformer 对当前帧体素进行稀疏自注意力处理，得到 $z_t(v)$（公式 6）。最终通过归一化融合 $h_t(v)$ 和 $z_t(v)$，生成时空一致的体素表示 $\tilde{f}_t(v)$（公式 7）。该模块的详细架构见 Figure 4。

3. **长短期记忆召回（LTM + STM）**：在 STEM 确保单个体素的时序一致性后，记忆召回模块从两个粒度进一步增强时间推理能力。长期记忆（LTM）维护三个记忆库——文本记忆库、特征对记忆库和视觉记忆库——存储加权文本-视觉对用于跨场景语义召回；为抑制高频类别的过度表示，LTM 采用偏置权重更新机制 $w_i^{bias}$（公式 8-9）。短期记忆（STM）则缓存近期帧的掩码特征，维持帧间分割的连续性。该模块的详细架构见 Figure 5。

4. **分割头**：管线的末端，将时空一致且记忆增强的体素特征映射为逐点或逐体素的查询驱动分割掩码，输出最终的 3D/4D 分割结果。

### 设计逻辑与因果机制

这一管线设计的因果逻辑在于：**CFTVA 解决了“语言查询与动态视觉特征如何在时间维度上对齐”的问题，STEM 解决了“对齐后的特征如何在体素级保持时空一致”的问题，LTM+STM 则解决“历史信息如何被有效召回以改善当前推理”的问题**。三者形成递进关系——没有对齐，一致性建模缺乏语义锚点；没有一致性，记忆召回会在时序漂移的特征上积累误差；没有记忆召回，模型在遮挡、大位移等困难场景下缺乏历史参照。

消融实验（Table 5）从反面验证了这一因果链：在 Instruct3D 上，完整模型的 mIoU 为 35.9；依次移除 CFTVA、STEM、LTM、STM 后，mIoU 分别降至 33.1、32.5、32.0、31.4，每个模块的移除都导致性能的阶梯式下降，且定性可视化（Figure 6）显示缺少时空一致性或记忆召回会在遮挡场景下产生明显的时序漂移和错误分割。



MORE-STEM 围绕三个核心模块构建：跨帧文本-视觉对齐（CFTVA）、时空一致性模型（STEM）以及长短期记忆召回（LTM + STM）。三个模块协同工作，将语言查询与多帧点云特征进行时间感知的跨模态对齐，并通过状态空间时序传播和分级记忆机制确保分割结果的时空一致性。

### 跨帧文本-视觉对齐（CFTVA）

CFTVA 模块负责将文本查询、图像特征与点云特征统一到共享的表示空间中。其处理流程分为三步：

**点-体素双分支跨模态精炼。** 首先利用双向交叉注意力将图像特征分别与点特征和体素特征融合，获得精细化的几何表示：

$$F_{t}^{point'} = \mathrm{CrossAttn}(F_{t}^{point}, F_{t}^{img})$$

$$F_{t}^{voxel'} = \mathrm{CrossAttn}(F_{t}^{voxel}, F_{t}^{img})$$

其中 $F_{t}^{point}$、$F_{t}^{voxel}$ 分别为第 $t$ 帧的点级和体素级特征，$F_{t}^{img}$ 为对应的图像特征。交叉注意力使每个几何 token 能够从视觉模态中吸收纹理和语义线索。

**时序视觉 token 聚合。** 将精炼后的点特征与体素特征沿通道维度拼接，得到当前帧的视觉表示 $F_{t}^{vis'}$。随后将文本嵌入 $F^{txt'}$ 与当前及历史视觉 token 进行时序感知的注意力对齐：

$$F_{t}^{visalign} = \mathrm{Attn}(F^{txt'}, [F_{t}^{vis'}, F_{t-1}^{vis'}, F_{t-2}^{vis'}])$$

该操作使文本查询能够动态地关注多帧中与语义相关的视觉区域，建立跨帧的文本-视觉对应。

**时序对比学习约束。** 为强化对齐质量，引入对比损失，使正确帧的视觉-文本对得分高于其他帧：

$$\mathcal{L}_{align} = -\log \frac{\exp(\mathrm{sim}(F_{t}^{visalign}, F^{txt'})/\tau)}{\sum_{t'}\exp(\mathrm{sim}(F_{t'}^{visalign}, F^{txt'})/\tau)}$$

其中 $\mathrm{sim}(\cdot,\cdot)$ 为余弦相似度，$\tau$ 为温度系数。该损失强制模型在时间维度上区分不同帧的视觉-文本匹配关系，提升跨帧对齐的辨别力。

### 时空一致性模型（STEM）

STEM 模块在体素级别同时建模帧间时序传播和帧内空间精炼，确保分割掩码在时间维度上的连贯性。

**状态空间帧间更新。** 将每个体素 $v$ 视为一个独立的状态单元，利用状态空间模型进行时序传播：

$$h_{t}(v) = A h_{t-1}(v) + B [F_{t}^{pointalign}(v) \| F_{t}^{voxelalign}(v)]$$

其中 $h_{t}(v)$ 为体素 $v$ 在第 $t$ 帧的隐状态，$A$ 和 $B$ 为可学习的状态转移矩阵和输入映射矩阵，$[\cdot\|\cdot]$ 表示通道拼接。该公式实现了帧间特征的递推式传播，使历史信息自然融入当前帧表示。

**Transformer 帧内精炼。** 对当前帧内的体素应用自注意力，捕捉局部空间结构：

$$z_{t}(v) = \mathrm{Transformer}(Q_{t}, K_{t}, V_{t})$$

其中 $Q_t$、$K_t$、$V_t$ 由当前帧体素特征线性投影得到。Transformer 在稀疏体素空间内执行可控注意力，增强同一帧内相邻体素的特征一致性。

**时空特征融合。** 将帧间传播与帧内精炼的结果通过残差连接和归一化进行融合：

$$\tilde{f}_{t}(v) = \mathrm{Norm}(h_{t}(v) + z_{t}(v))$$

$\tilde{f}_{t}(v)$ 即为体素 $v$ 的最终时空一致特征表示，同时编码了时序连续性和空间结构信息。

### 长短期记忆召回（LTM + STM）

记忆召回模块通过分级记忆机制平衡长期跨场景语义召回与短期帧级连续性。

**长期记忆（LTM）。** LTM 维护三个相关联的记忆库：文本记忆库 $\{F_{i}^{txt}\}$、特征对记忆库 $\{f_{pair}^{i}\}$ 和视觉记忆库。每个文本-视觉对根据其训练损失被赋予置信度权重：

$$w_{i}^{init} = \frac{1}{\mathcal{L}_{i} + \epsilon}, \quad M_{LTM} = \{ w_{i} \cdot (f_{pair}^{i} : [F_{i}^{txt}, \tilde{f}_{i}]) \}$$

其中 $\mathcal{L}_{i}$ 为样本 $i$ 的损失值，$\epsilon$ 为防止除零的小常数。损失越小的样本获得越高权重，表示其文本-视觉对应更可靠。

为防止高频类别在记忆中过度占据主导地位，引入偏置权重更新机制：

$$w_{i}^{bias} = \frac{w_{i}^{init}}{\sum_{j \in c} w_{j}^{init}}$$

该机制使类别 $c$ 内所有样本的总权重保持恒定，即使新样本不断加入，各类别的表示能力仍保持平衡。推理时，LTM 通过检索与当前查询最相关的文本-视觉对来增强语义理解。

**短期记忆（STM）。** STM 缓存近期帧的掩码特征，以滑动窗口方式维持帧间连续性。当目标在连续帧中发生部分遮挡或外观变化时，STM 提供近期的稳定特征参考，防止分割结果出现时序跳变。

三个模块的协同作用在消融实验中得到验证：完整模型在 Instruct3D 上取得 mIoU 35.9；依次移除 CFTVA、STEM、LTM、STM 后，mIoU 分别降至 33.1、32.5、32.0、31.4（Table 5），表明各模块对最终性能均有不可替代的贡献。

### 补充图表

![[assets/figures/papers/paper_list_l33_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MORE_STEM_Long_Shor/figures/004_Figure_3.jpg]]
*Figure 3: Framework of the proposed Cross-Frame Text-Visual Alignment module*

![[assets/figures/papers/paper_list_l33_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MORE_STEM_Long_Shor/figures/003_Figure_4.jpg]]
*Figure 4: Framework of the proposed Spatio-Temporal Consistency Model module*

![[assets/figures/papers/paper_list_l33_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MORE_STEM_Long_Shor/figures/005_Figure_5.jpg]]
*Figure 5: Framework of the proposed Long-Short Memory Recall module*



## 实验与关键发现

### 主实验结果

MORE-STEM 在多个 3D 和 4D 理解基准上取得了最优性能，覆盖指令分割、引用分割和语义分割三类任务。

**3D 指令分割。** 在 Instruct3D 基准上，MORE-STEM 以 mIoU 35.9、Acc 31.4 显著超越此前最优方法 **SegPoint**（He et al., ECCV 2024）的 31.6 和 27.5，分别提升 4.3 和 3.9 个百分点（Table 1）。这一提升的核心驱动力来自两方面：一是跨帧文本-视觉对齐（CFTVA）建立了语言查询与多帧几何特征之间的细粒度时间感知对应；二是长短期记忆召回机制通过文本-视觉关系映射维持了鲁棒且精确的目标一致性。值得注意的是，由于该方法以多帧点云为输入，在 3D 指令分割任务中，将同一场景的三份相同点云与三条不同文本查询同时送入网络，相当于单次前向传播处理三个任务，在一定程度上增加了计算并行度，但性能增益仍主要归因于模型本身的时序建模与记忆能力。

在自建的 InstructKITTI 3D 基准上，MORE-STEM 取得 Acc 38.62、mIoU 37.95（Table 2）。定性结果（Figure 6）显示，蓝色掩码（MORE-STEM 输出）与绿色掩码（真值标注）高度重合，而 **3D-STMN**（Wu et al., AAAI 2024）和 **3D-LLaVA**（Deng et al., CVPR 2025）的预测（红色/橙色）在遮挡区域和小目标上出现明显偏差，进一步验证了时空一致性和记忆召回在提升分割精度方面的作用。

![[assets/figures/papers/paper_list_l33_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MORE_STEM_Long_Shor/figures/007_Table_2.jpg]]
*Table 2: Instruction segmentation results on proposed InstructKITTI*

![[assets/figures/papers/paper_list_l33_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MORE_STEM_Long_Shor/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative results of 3D instruction segmentation experiment on our InstructKITTI 3D benchmark. In the visualization results, the blue masks denote the segmentation outputs from the proposed MORE-STEM, the red ones and orange ones represent the predictions of the 3D-STMN [36] and 3D-LLaVA [7], and the green masks indicate the ground truth annotations*

**3D 引用分割。** 在 ScanRefer 基准上，MORE-STEM 取得 mIoU 52.7、Acc@50 54.8 的最佳综合性能（Table 3），相比此前最优方法约有 2–3 个点的提升。这表明即使在静态场景的引用分割任务中，长短期记忆召回所提供的跨场景语义关联能力依然有效——长期记忆（LTM）存储的加权文本-视觉对能够为当前查询提供额外的语义先验。

**4D 指令分割。** 在自行构建的 InstructKITTI 4D 基准上，MORE-STEM 取得 Acc@50 42.19、mIoU 40.67。由于该基准为首个动态场景指令分割基准，缺乏直接前人工作对比，但这一结果为动态点云查询驱动分割建立了性能基线。需要指出，该基准基于 SemanticKITTI 自动构建，其标签质量受源数据集和 VLM（Qwen3VL-7B）影响，可能存在噪声。

**语义分割。** 在 SemanticKITTI 验证集上，MORE-STEM 取得 mIoU 74.6（Table 4），相比此前 SOTA（约 72–73）提升 1–2 个点。这表明时空一致性建模对常规语义分割任务同样具有正向迁移能力。

### 消融实验

消融实验（Table 5）系统验证了各模块的必要性。完整模型（CFTVA + STEM + LTM + STM）在 Instruct3D 上取得 mIoU 35.9。依次移除关键模块后，性能呈阶梯式下降：

![[assets/figures/papers/paper_list_l33_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MORE_STEM_Long_Shor/figures/011_Table_5.jpg]]
*Table 5: Ablation study of different proposed modules on Instruct3D [10]*

- **移除 CFTVA**：mIoU 降至 33.1（−2.8），表明跨帧文本-视觉对齐是语言查询与多帧几何特征建立关联的基础，缺失后模型退化为近似单帧静态对齐。
- **移除 STEM**：mIoU 降至 32.5（−3.4），降幅最大，说明体素级时空一致性对分割质量至关重要。状态空间模型的帧间隐状态传播和可控制 3D Transformer 的帧内细化共同构成了时序连贯性的核心保障。
- **移除 LTM**：mIoU 降至 32.0（−3.9），验证了长期记忆跨场景语义召回的关键作用。定性消融（Figure 6 及相关文字）显示，缺少长期记忆后，模型在遮挡或大位移场景下出现时序漂移和错误分割。
- **移除 STM**：mIoU 降至 31.4（−4.5），接近基线 SegPoint 水平，说明短期记忆缓存的近期掩码特征对维持帧间连续性不可或缺。

此外，长期记忆的偏置权重更新机制（$w_i^{bias} = \frac{w_i^{init}}{\sum_{j \in c} w_j^{init}}$）有效抑制了高频类别的过表示。消融移除该机制后，mIoU 下降约 1.5 个点，验证了类别平衡策略对记忆质量的影响。

### 失败模式与局限性

尽管 MORE-STEM 在多个基准上表现优异，仍存在以下局限：

1. **模型体积与实时性**：方法依赖预训练的 LLaMA2-7B 和 Qwen3VL-7B 进行文本编码和视觉属性抽取，模型体积较大，可能不适合资源受限的实时应用场景。
2. **基准泛化性**：InstructKITTI 基准仅基于 SemanticKITTI 的户外驾驶场景构建，其泛化性到其他动态环境（如室内机器人、拥挤人群）尚未验证。
3. **长期记忆漂移**：尽管引入了偏置权重更新，长期记忆在极端长序列或类别极度不平衡时仍可能产生表示漂移，论文未讨论记忆淘汰或主动遗忘机制。
4. **时序依赖长度**：时空一致性模型主要用于两帧间传播，对于更长的时序依赖（如数十帧）的效果未深入分析。在真实世界多传感器异步输入（如 LiDAR 与相机帧率不一致）的情况下，跨帧对齐和记忆召回机制的鲁棒性也尚待验证。

### 补充图表

![[assets/figures/papers/paper_list_l33_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MORE_STEM_Long_Shor/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of the 3D referring/instruction segmentation task and proposed 4D instruction segmentation task*

![[assets/figures/papers/paper_list_l33_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MORE_STEM_Long_Shor/figures/006_Table_1.jpg]]
*Table 1: Instruction segmentation results on Instruct3D [10]*

![[assets/figures/papers/paper_list_l33_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MORE_STEM_Long_Shor/figures/009_Table_3.jpg]]
*Table 3: Referring segmentation results on ScanRefer [4]*

![[assets/figures/papers/paper_list_l33_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MORE_STEM_Long_Shor/figures/010_Table_4.jpg]]
*Table 4: Semantic segmentation results on the validation set of SemanticKITTI [3]*



## 定位与知识库关联

### 1. 任务谱系：从静态3D分割到动态4D指令理解

MORE-STEM 的工作锚定在两条相互交叉的研究线上：**查询驱动的3D点云分割**与**动态点云序列理解**。传统3D引用/指令分割方法——包括早期基于自然语言的3D目标定位工作 **ReferIt3D**（Achlioptas et al., ECCV 2020）和 **ScanRefer**（Chen et al., ECCV 2020），以及后续的端到端引用分割方法 **3D-STMN**（Wu et al., AAAI 2024）和语言引导的Transformer方法 **RefMask3D**（He & Ding, ACM MM 2024）——均将问题限定在静态场景中。这些方法在单帧点云上建立文本-视觉对应，但完全不具备跨帧推理能力，无法处理动态场景中目标的运动、遮挡和外观变化。

最近的代表性工作 **SegPoint**（He et al., ECCV 2024）将LLM引入3D指令分割，在Instruct3D基准上取得了当时最优的mIoU 31.6和Acc 27.5，但其核心设计仍基于单帧静态输入。通用3D多模态大模型 **3D-LLaVA**（Deng et al., CVPR 2025）虽然支持指令驱动的3D理解，同样缺乏时序建模机制。MORE-STEM 正是在这一瓶颈上做出关键跨越：将查询驱动分割从静态3D扩展到动态4D，同时处理空间定位与时间一致性。

在动态场景理解一侧，**TASeg**（Wu et al., CVPR 2024）通过时序聚合改进LiDAR语义分割，**Mamba4D**（Liu et al., CVPR 2025）利用状态空间模型进行4D点云理解，但它们均面向类别级语义分割，不涉及语言查询驱动的实例级分割。MORE-STEM 首次将这两条线融合，统一了静态与动态场景下的查询驱动分割。

### 2. 核心技术定位：时空一致性与记忆召回的联合框架

从方法学角度，MORE-STEM 的核心贡献在于将三个机制有机整合为一个端到端框架：

- **跨帧文本-视觉对齐（CFTVA）** 是对现有单帧跨模态对齐范式的时序泛化。与 SegPoint 等方法的静态文本-点云融合不同，CFTVA 通过跨模态交叉注意力、对比学习和时序视觉token聚合，使语言查询能够动态地与多帧几何特征对齐。这是从“空间对齐”到“时空对齐”的关键升级。

- **时空一致性模型（STEM）** 借鉴了 Mamba4D 的状态空间建模思路，但将其应用于体素级的查询驱动分割而非类别级语义分割。STEM 通过状态空间模型实现帧间隐状态传播（$h_t(v) = A h_{t-1}(v) + B [F_t^{pointalign}(v) \| F_t^{voxelalign}(v)]$），再用可控制3D Transformer进行帧内稀疏注意力细化（$z_t(v) = \mathrm{Transformer}(Q_t, K_t, V_t)$），最终通过归一化融合（$\tilde{f}_t(v) = \mathrm{Norm}(h_t(v) + z_t(v))$）得到时空一致表示。这种“帧间SSM传播+帧内Transformer细化”的双支路设计是区别于现有4D方法的关键创新。

- **长短期记忆召回（LTM+STM）** 是该框架最具特色的模块。长期记忆（LTM）存储加权文本-视觉对，通过偏置权重更新机制（$w_i^{bias} = \frac{w_i^{init}}{\sum_{j \in c} w_j^{init}}$）防止高频类别过度占据记忆；短期记忆（STM）缓存近期掩码特征维持帧间连续性。这一分级记忆设计在现有3D/4D分割方法中尚无直接对应，是平衡跨场景语义召回与帧级连续性的核心干预点。

### 3. 适用边界与局限

**计算与部署边界**：MORE-STEM 依赖预训练的 LLaMA2-7B 和 Qwen3VL-7B 进行文本编码和视觉属性抽取，模型体积较大，不适合资源受限的实时应用。这一依赖继承自 SegPoint 等基于LLM的分割方法，但在4D场景下因多帧处理而进一步放大。

**数据与泛化边界**：论文构建的 InstructKITTI 基准仅基于 SemanticKITTI 的户外驾驶场景，其标签由 Qwen3VL-7B 自动生成，存在噪声风险。该方法在室内机器人、拥挤人群等其他动态环境中的泛化性尚未验证。

**时序建模边界**：STEM 的状态空间更新主要在两帧间传播，对于数十帧以上的长时序依赖效果未深入分析。此外，长期记忆在极端长序列或类别极度不平衡时仍可能产生表示漂移，论文未讨论记忆淘汰或主动遗忘机制。

**公平性考量**：在3D指令分割任务中，为适配多帧输入设计，同一场景的三份相同点云与三条不同文本查询同时输入，相当于在一个前向传播中处理三个任务，增加了计算并行度。在4D任务上，由于缺乏现有方法，仅报告自身分数，未能直接对比。

### 4. 开放问题

1. **任务扩展**：MORE-STEM 能否从分割扩展到预测任务（如未来帧掩码预测）或行为理解？其时空一致性和记忆召回机制为这类扩展提供了潜在基础，但需要新的输出头和训练范式。

2. **多传感器异步鲁棒性**：在真实世界部署中，LiDAR与相机帧率往往不一致。跨帧对齐和记忆召回机制如何鲁棒处理异步输入，是一个未被探索的工程挑战。

3. **记忆可扩展性**：长期记忆的容量与检索效率随数据规模线性增长。如何设计高效的检索和去重策略以支持大规模场景，是走向实用的关键问题。

4. **标注依赖**：该方法是否能与自监督预训练范式结合，从而减少对细粒度文本标注的依赖？当前框架仍需要大量文本-掩码对进行监督训练。

5. **更长时序建模**：STEM 的两帧传播机制能否扩展为多帧联合优化或引入更长的时序感受野（如Mamba的远距离依赖），值得进一步探索。



## 原文 PDF

![[paperPDFs/CVPR_2026/MORE_STEM_Long_Short_MemOry_REcall_and_Spatio_TEmporal_Consistency_Model_for_Query_Driven_3D_4D_Point_Cloud_Segmentation.pdf]]
