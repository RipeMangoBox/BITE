---
title: "FantasyVLN: Unified Multimodal Chain-of-Thought Reasoning for Vision-and-Language Navigation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FantasyVLN_Unified_Multimodal_Chain_of_Thought_Reasoning_for_Vision_and_Language_Navigation.pdf
project_link: null
code_link: "https://github.com/Fantasy-AMAP/fantasy-vln"
aliases:
- FantasyVLN
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 采用紧凑的VAR潜空间编码替代像素级视觉CoT解码，并结合跨模态对齐约束，将多模态CoT推理能力内化为直接动作映射（训练时推理，推理时不生成CoT），从而在保证推理感知的同时消除推理延迟。
primary_logic: 通过在统一框架内联合训练文本、视觉、多模态及无CoT四种推理模式，并利用门控机制与交叉模态对齐，使模型在共享参数空间下学习到模态不变的推理表征，实现‘训练时多CoT，推理时无CoT’的隐式推理范式，从而兼顾推理能力与实时性。
claims:
- Our approach achieves reasoning-aware yet real-time navigation, reducing inference latency by an order of magnitude compared to explicit CoT methods.
- Implicit CoT operates approximately five times faster than explicit CoT (APS 1.03 vs ~0.2).
- Cross-mode alignment lifts SR from 0 to 2.44 and ISR from 2.39 to 11.01, demonstrating its indispensability.
- FantasyVLN achieves full convergence at 3,000 iterations vs WorldVLA's 13,800 iterations (4.6x faster).
---

# FantasyVLN: Unified Multimodal Chain-of-Thought Reasoning for Vision-and-Language Navigation

> [!tip] 核心洞察
> 通过在统一框架内联合训练文本、视觉、多模态及无CoT四种推理模式，并利用门控机制与交叉模态对齐，使模型在共享参数空间下学习到模态不变的推理表征，实现‘训练时多CoT，推理时无CoT’的隐式推理范式，从而兼顾推理能力与实时性。

| 字段 | 内容 |
|------|------|
| 中文题名 | FantasyVLN：面向视觉与语言导航的统一多模态思维链推理 |
| 英文题名 | FantasyVLN: Unified Multimodal Chain-of-Thought Reasoning for Vision-and-Language Navigation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zuo_FantasyVLN_Unified_Multimodal_Chain-of-Thought_Reasoning_for_Vision-and-Language_Navigation_CVPR_2026_paper.html) · [Code](https://github.com/Fantasy-AMAP/fantasy-vln) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FantasyVLN |
| Dataset | LH-VLN |

> [!tip] 效果简介
> - LH-VLN 上，SR (%) 2.44 vs N/A (prior SOTA) (new SOTA)；ISR (%) 11.01 vs N/A (new SOTA)；CSR (%) 9.64 vs N/A (new SOTA)。

## 概要

### 问题与瓶颈

视觉与语言导航（VLN）要求智能体在复杂环境中依据自然语言指令进行长程、多阶段推理与决策。现有方法引入思维链（CoT）以增强推理能力，但面临两个核心瓶颈：**纯文本CoT**缺乏视觉感知，易过拟合稀疏标注，难以处理细粒度空间关系；**多模态CoT**虽能同时利用语义规划与视觉感知，却因需要逐像素生成想象视觉观察而导致严重的token膨胀——每步推理超3k–5k tokens，使实时导航不可行。此外，跨模态推理对齐不足进一步限制了复杂长程任务的成功率。

### 核心思路

FantasyVLN提出**“训练时多CoT，推理时无CoT”的隐式推理范式**，从根本上解耦推理能力与推理延迟。其关键机制包括：

- **紧凑视觉CoT**：在视觉自回归模型（VAR）的潜空间而非像素空间进行视觉推理解码，将高维视觉想象压缩为紧凑潜码，大幅降低token开销。
- **统一门控多CoT学习**：在共享参数空间下联合训练无CoT、文本CoT、视觉CoT及多模态CoT四种推理模式，通过二进制门控信号实现模式间无缝切换。
- **跨模态对齐约束**：强制非CoT模式的动作预测与其他推理模式对齐，以软目标蒸馏的方式将多模态推理能力内化为直接动作映射。

### 主要结果

在长程视觉语言导航基准**LH-VLN**上，FantasyVLN取得新的最优结果：成功率（SR）**2.44%**，指令成功率（ISR）**11.01%**，条件成功率（CSR）**9.64%**，条件目标达成率（CGT）**8.99%**。在推理效率方面，隐式CoT的动作执行速度（APS **1.03**）约为显式CoT方法（~0.2）的**5倍**，推理延迟降低一个数量级。消融实验表明，跨模态对齐对性能至关重要——移除对齐后SR从2.44降至0，ISR从11.01骤降至2.39。在训练效率上，紧凑视觉CoT使收敛速度相比像素级方法**WorldVLA**（Cen et al., arXiv 2025）提升约**4.6倍**（3,000 vs 13,800次迭代）。

### 方法定位

FantasyVLN在方法谱系上处于**统一多模态推理导航**的交汇点：它继承了**Aux-Think**（Wang et al., NeurIPS 2025）的文本CoT推理思路和**Uni-NaVid**（Zhang et al., RSS 2025）的统一导航框架，但通过潜空间视觉CoT和跨模态对齐机制，首次实现了多模态CoT推理能力向实时动作映射的内化，避免了**CoT-VLA**（Zhao et al., CVPR 2025）等显式视觉CoT方法的推理延迟问题。其核心创新在于**将VLN的推理-执行范式从“生成-再决策”转变为“训练时内化-推理时直接映射”**，为实时推理密集型导航提供了新的技术路径。

视觉与语言导航（VLN）要求智能体在真实环境中根据自然语言指令进行自主移动。随着任务场景从简单室内导航向多阶段、长程真实世界导航演进，智能体不仅需要理解指令的语义意图，还需具备对环境的细粒度视觉感知能力。这一需求催生了将思维链（Chain-of-Thought, CoT）推理引入VLN的研究方向——通过显式生成中间推理步骤，模型能够更好地进行语义规划和视觉感知，从而应对复杂导航任务。

然而，现有VLN方法中的显式CoT推理面临两大核心瓶颈。其一，纯文本CoT方法（如**Aux-Think**，Wang et al., NeurIPS 2025）缺乏视觉感知能力，且容易过拟合稀疏标注的文本推理数据，导致在需要精细视觉判断的场景中表现不足。其二，多模态CoT方法在生成推理链时需要同时输出像素级未来视觉观察，导致严重的token膨胀——每步推理需生成超过3k–5k tokens，使实时导航变得不可行。例如，**CoT-VLA**（Zhao et al., CVPR 2025）和**WorldVLA**（Cen et al., arXiv 2025）等像素级视觉CoT方法虽然提升了推理能力，但推理延迟高达隐式方法的5倍以上，无法满足实际部署的实时性要求。此外，现有方法普遍缺乏跨模态推理的对齐机制，文本推理与视觉推理在表征空间中相互孤立，进一步限制了复杂长程任务的成功率。

上述困境揭示了一个根本性的张力：显式CoT推理能增强导航能力，但代价是高昂的推理延迟；隐式动作映射速度快，却丧失了推理感知能力。本文的核心动机在于打破这一“推理能力–实时性”的权衡——能否让模型在训练阶段充分学习多模态CoT推理，而在推理阶段直接进行指令到动作的隐式映射，从而同时获得推理能力与实时性能？

## 核心方法与创新机理

FantasyVLN 的核心创新并非引入单一技术模块，而是围绕“训练时多模态 CoT 推理，推理时零延迟动作映射”这一隐式推理范式，系统重构了 VLN 中思维链推理的形态。下面从因果机制、关键改槽（changed slots）和证据强度三个维度展开。

### 1. 因果机制：从显式生成到隐式内化

现有 VLN 方法在引入思维链推理时面临一个结构性矛盾：**显式 CoT 生成能提升推理能力，但其 token 膨胀导致实时导航不可行**。纯文本 CoT 方法（如 **Aux-Think**，Wang et al., NeurIPS 2025）缺乏视觉感知且易过拟合稀疏标注；多模态 CoT 方法（如 **CoT-VLA**，Zhao et al., CVPR 2025；**WorldVLA**，Cen et al., arXiv 2025）则因需要生成像素级未来视觉观察，单步推理 token 量超过 3k–5k，推理延迟达到秒级（APS ≈ 0.2，见 Table 2）。

FantasyVLN 的核心因果调节变量（causal knob）是：**将视觉 CoT 的解码空间从像素域压缩到 VAR 潜空间，并通过跨模态对齐约束将多模态推理能力蒸馏到无 CoT 的直接动作映射通路中**。这一设计实现了“训练时推理，推理时不生成 CoT”的隐式推理范式——模型在训练阶段通过门控机制联合学习四种推理模式（无 CoT、文本 CoT、紧凑视觉 CoT、多模态 CoT），在推理阶段仅激活无 CoT 通路，输出单一动作 token，从而在保留推理感知的同时消除推理延迟。

### 2. 关键改槽（Changed Slots）分析

FantasyVLN 相对基线方法的核心改槽可归纳为以下四个维度：

| 改槽维度 | 基线做法 | FantasyVLN 做法 | 证据锚点 |
|---------|---------|----------------|---------|
| **推理模式** | 显式生成思维链（textual/visual CoT） | 隐式推理（训练时多模态 CoT，推理时直接指令-动作映射） | Abstract; Table 2 |
| **视觉 CoT 解码空间** | 像素空间解码（pixel-level） | VAR 潜空间紧凑解码（compact VAR latent decoding） | Section 3.3; Figure 6 |
| **模态对齐机制** | 无跨模态对齐约束 | 交叉模态对齐约束（cross-mode alignment with soft targets） | Section 3.5; Table 4 |
| **多模态融合方式** | 独立训练或简单串联各模态 CoT | 统一门控多 CoT 学习（unified gating-based multi-CoT learning） | Section 3.4; Table 3 |

#### 2.1 推理模式：隐式推理的实时性突破

这是 FantasyVLN 最具区分度的创新。推理时模型执行的是直接指令-动作映射（“At inference, our model performs direct instruction-to-action mapping while still enjoying reasoning-aware representations”），单步仅解码一个 token，而显式 CoT 方法需生成数千 token 的中间推理步骤。定量证据来自 Table 2：隐式 CoT 的 APS 达到 1.03，约为显式 CoT（APS ≈ 0.2）的 5 倍，实现了数量级的推理延迟降低。

#### 2.2 视觉 CoT 解码空间：从像素到潜码的压缩

传统视觉 CoT 方法（如 WorldVLA）在像素空间解码未来视觉观察，计算代价高昂。FantasyVLN 采用预训练的视觉自回归模型（VAR）将想象视觉 token 编码为紧凑潜码，仅解码粗尺度结构信息。消融实验（Figure 4）表明，VAR 尺度 4 即可获得最高 ISR 7.41，证明粗尺度潜码足以保留导航所需的结构信息。这一压缩带来的训练效率提升显著：FantasyVLN 在 3,000 次迭代即完全收敛，而像素级方法 WorldVLA 需要 13,800 次迭代（4.6 倍加速，Figure 6）。

#### 2.3 跨模态对齐：隐式推理能力的关键使能器

跨模态对齐是 FantasyVLN 中最关键的约束机制。其核心设计是：将无 CoT 通路作为“主参考模式”，提取其动作预测的软目标（soft targets），强制其他三种推理模式的预测与之对齐。Table 4 的消融实验提供了决定性证据：**无对齐时 SR 为 0，加入对齐后 SR 提升至 2.44；ISR 从 2.39 跃升至 11.01**。这表明，在没有对齐约束的情况下，多模态 CoT 训练无法有效迁移到无 CoT 推理通路，对齐是隐式推理范式成立的必要条件。

#### 2.4 统一门控多 CoT 学习

FantasyVLN 通过两个二进制门控信号（$g_{\mathcal{T}}$ 和 $g_{\mathcal{V}}$）控制文本推理通路和视觉推理通路的激活，实现四种推理模式的动态切换：

$$
\widehat{\mathcal{R}}_{t+1} = \begin{cases}
\mathrm{None}, & \text{if } (g_{\mathcal{T}}, g_{\mathcal{V}}) = (0,0), \\
\widehat{\mathcal{T}}_{t+1}, & \text{if } (g_{\mathcal{T}}, g_{\mathcal{V}}) = (1,0), \\
\widehat{\mathcal{V}}_{t+1}, & \text{if } (g_{\mathcal{T}}, g_{\mathcal{V}}) = (0,1), \\
\widehat{\mathcal{M}}_{t+1}, & \text{if } (g_{\mathcal{T}}, g_{\mathcal{V}}) = (1,1).
\end{cases}
$$

Table 3 的消融实验证实，包含全部四种模式的统一框架在 SR 和 CGT 等指标上达到最优，验证了多模态联合训练对导航能力的叠加增益。

### 3. 证据强度评估

支撑上述创新的证据整体质量较高：

- **推理效率提升**：Table 2 的 APS 对比直接量化了隐式推理相对显式 CoT 的 5 倍加速，置信度高（0.95）。
- **对齐的必要性**：Table 4 的 SR 从 0 到 2.44 的跃升是对齐机制决定性的最强证据，置信度高（0.95）。
- **训练效率**：Figure 6 的收敛曲线对比提供了视觉 CoT 压缩的间接但有力的支撑，置信度高（0.95）。
- **VAR 尺度选择**：Figure 4 的消融曲线表明粗尺度潜码即可保留导航结构信息，但这一结论仅在 LH-VLN 数据集上验证，大规模数据下的泛化性尚需进一步确认（见下文局限）。

### 4. 局限与待验证假设

尽管创新点证据充分，以下方面仍需注意：

1. **基座模型限制**：FantasyVLN 使用的 VLM 基座并非原生统一生成与理解模型，限制了未来场景想象能力的上限。
2. **数据规模未验证**：紧凑视觉 CoT 在大规模数据上的扩展行为未经验证，Figure 4 和 Figure 6 的结论可能受 LH-VLN 数据量限制。
3. **训练范式单一**：当前仅采用监督微调，未探索强化学习等替代方案对多模态 CoT 推理能力的进一步增强潜力。

FantasyVLN 提出了一套**统一的多模态思维链（CoT）推理框架**，其核心设计理念是“训练时多 CoT，推理时无 CoT”——在训练阶段联合学习文本、视觉、多模态及无 CoT 四种推理模式，而在推理时仅执行直接的动作映射，从而在保留推理感知能力的同时消除显式 CoT 带来的 token 膨胀与推理延迟。

### 框架总览

如图 2 所示，整个框架构建在一个**共享的 VLM 基座模型**之上，该模型接收导航指令 $\mathcal{T}$ 和历史视觉观察 $\{\mathcal{O}_{\leq t}\}$ 作为输入。与传统 VLN 方法不同，FantasyVLN 引入了两个关键扩展模块：

1. **视觉自回归模型（VAR）**：将 VLM 输出的紧凑潜码解码为像素级未来图像，仅在训练时使用。
2. **门控机制**：通过两个二进制信号 $g_{\mathcal{T}}$ 和 $g_{\mathcal{V}}$ 显式控制文本推理通路和视觉推理通路的激活，实现四种推理模式的动态切换。

### 四种推理模式

框架在统一的参数空间内支持以下四种推理模式：

| 门控信号 $(g_{\mathcal{T}}, g_{\mathcal{V}})$ | 推理模式 | 功能 |
|---|---|---|
| $(0, 0)$ | 无 CoT 推理 | 直接指令-动作映射，用于实时推理 |
| $(1, 0)$ | 文本 CoT | 生成语义规划文本，增强高层决策 |
| $(0, 1)$ | 紧凑视觉 CoT | 在 VAR 潜空间解码未来视觉想象，增强视觉感知 |
| $(1, 1)$ | 多模态 CoT | 同时生成文本推理与视觉想象，实现跨模态联合推理 |

推理链的选择由门控信号组合决定，如公式所示：

$$
\widehat{\mathcal{R}}_{t+1} = \begin{cases}
\mathrm{None}, & \mathrm{if}\ (g_{\mathcal{T}}, g_{\mathcal{V}}) = (0, 0), \\
\widehat{\mathcal{T}}_{t+1}, & \mathrm{if}\ (g_{\mathcal{T}}, g_{\mathcal{V}}) = (1, 0), \\
\widehat{\mathcal{V}}_{t+1}, & \mathrm{if}\ (g_{\mathcal{T}}, g_{\mathcal{V}}) = (0, 1), \\
\widehat{\mathcal{M}}_{t+1}, & \mathrm{if}\ (g_{\mathcal{T}}, g_{\mathcal{V}}) = (1, 1).
\end{cases}
$$

### 核心模块与数据流

**VLM 基座模型**负责自回归地生成推理链 $\widehat{\mathcal{R}}_{t+1}$ 和未来动作 $\widehat{A}_{t+1}$：

$$
[\widehat{\mathcal{R}}_{t+1}, \widehat{A}_{t+1}] = \pi_{\theta}\big(\mathcal{T}, \{\mathcal{O}_{\leq t}\}, g_{\mathcal{T}}, g_{\mathcal{V}}\big)
$$

在视觉 CoT 模式下，VLM 输出的视觉推理 token 并非像素值，而是**紧凑的 VAR 潜空间编码**。这些潜码随后由预训练的 VAR 模型通过 next-scale prediction 解码为像素级未来图像。这种设计将视觉 CoT 的 token 开销从像素级方法（如 **CoT-VLA**（Zhao et al., CVPR 2025）和 **WorldVLA**（Cen et al., arXiv 2025）每步 3k–5k tokens）压缩至紧凑潜空间，是实现训练效率提升的关键——实验表明，FantasyVLN 的训练收敛速度相比 WorldVLA 提升了约 4.6 倍（3,000 vs 13,800 迭代，Figure 6）。

**跨模态对齐模块**则在训练阶段强制无 CoT 模式与其他推理模式在动作预测上保持一致。具体而言，该方法以无 CoT 模式作为主参考路径，提取其动作预测的软目标，并通过对齐损失约束其他模式的预测分布逼近该软目标。消融实验（Table 4）表明，这一对齐约束对性能至关重要：移除对齐后，SR 从 2.44 降至 0，ISR 从 11.01 骤降至 2.39。

### 训练与推理分离

训练时，框架通过交替优化无 CoT 目标 $\mathcal{L}_{\mathrm{non-CoT}}$ 和跨模态对齐联合目标 $\mathcal{L}_{\mathrm{joint}}^{*} = \mathcal{L}_{\mathrm{align}} + \mathcal{L}_{\mathrm{CoT}}$，使模型在共享参数空间下学习到模态不变的推理表征。推理时，门控信号固定为 $(0, 0)$，模型仅执行直接的动作预测，无需生成任何显式 CoT token，从而实现**推理感知且实时**的导航——隐式推理的 APS（每秒动作数）约为 1.03，相比显式 CoT 方法（~0.2）提速约 5 倍（Table 2）。

![[assets/figures/papers/paper_list_l2167_https_openaccess_thecvf_com_content_CVPR2026_html_Zuo_FantasyVLN_Unified/figures/002_Figure_2.jpg]]
*Figure 2: Unified multimodal Chain-of-Thought reasoning framework. Within a shared representation space, a single model supports four reasoning modes: (a) non-CoT reasoning for real-time inference, (b) textual CoT for semantic planning, (c) compact visual CoT for latent future imagination, and (d) multimodal CoT integrating both modalities. A flexible gating mechanism facilitates seamless transitions among the four modes, while an alignment constraint enforces representation consistency during training*

### 3.1 统一多模态CoT推理框架

FantasyVLN的核心架构由三个关键模块构成：**VLM基座模型**、**视觉自回归模型（VAR）**和**门控机制**，三者协同实现四种推理模式的统一。

**VLM基座模型**接收导航指令 $\mathcal{T}$ 和截至当前时刻的视觉观察序列 $\{\mathcal{O}_{\le t}\}$，同时预测潜在未来图像和动作。其核心推理步公式为：

$$[ \widehat{\mathcal{R}}_{t+1}, \widehat{A}_{t+1} ] = \pi_{\theta} \big( \mathcal{T}, \{\mathcal{O}_{\le t}\}, g_{\mathcal{T}}, g_{\mathcal{V}} \big)$$

其中 $\widehat{\mathcal{R}}_{t+1}$ 为推理链输出，$\widehat{A}_{t+1}$ 为预测动作，$g_{\mathcal{T}}$ 和 $g_{\mathcal{V}}$ 分别为文本和视觉推理通路的二进制门控信号。根据门控信号的四种组合，推理链选择遵循以下规则：

$$\widehat{\mathcal{R}}_{t+1} = \begin{cases} 
\mathrm{None}, & \mathrm{if } (g_{\mathcal{T}}, g_{\mathcal{V}}) = (0, 0) \\
\widehat{\mathcal{T}}_{t+1}, & \mathrm{if } (g_{\mathcal{T}}, g_{\mathcal{V}}) = (1, 0) \\
\widehat{\mathcal{V}}_{t+1}, & \mathrm{if } (g_{\mathcal{T}}, g_{\mathcal{V}}) = (0, 1) \\
\widehat{\mathcal{M}}_{t+1}, & \mathrm{if } (g_{\mathcal{T}}, g_{\mathcal{V}}) = (1, 1)
\end{cases}$$

这四种模式分别对应：(0,0) 无CoT推理（直接指令-动作映射，用于实时导航）；(1,0) 纯文本CoT（语义规划）；(0,1) 紧凑视觉CoT（潜空间未来想象）；(1,1) 多模态CoT（文本与视觉推理整合）。

**VAR模型**仅在训练时激活，将VLM输出的潜码通过next-scale prediction解码为像素级未来图像，使视觉推理在紧凑潜空间完成，避免像素级解码的token膨胀。

### 3.2 联合训练损失

四种推理模式通过加权交叉熵损失联合优化：

$$\mathcal{L}_{\mathrm{Joint}} = (\neg g_{\mathcal{T}} \wedge \neg g_{\mathcal{V}}) \mathcal{L}_{\mathrm{CE}}(\widehat{A}_{t+1}, A_{t+1}) + \dots$$

该损失函数按门控信号组合对无CoT、文本CoT、视觉CoT和多模态CoT四种模式分别施加动作预测的交叉熵监督，实现端到端的统一训练。

### 3.3 跨模态对齐约束

为将多模态CoT的推理能力内化至无CoT模式，FantasyVLN引入交叉模态对齐机制。首先以非CoT模式为参考基准，其目标函数为：

$$\mathcal{L}_{\mathrm{non-Co T}} = \mathcal{L}_{\mathrm{CE}}(\widehat{A}_{t+1}, A_{t+1})$$

然后提取非CoT模式的动作预测作为软目标，强制其他推理模式（文本CoT、视觉CoT、多模态CoT）对齐。完整的跨模态对齐联合目标为：

$$\mathcal{L}_{\mathrm{Joint}}^{*} = \mathcal{L}_{\mathrm{Align}} + \mathcal{L}_{\mathrm{CoT}}$$

其中 $\mathcal{L}_{\mathrm{Align}}$ 约束辅助模式的动作分布逼近非CoT模式的软目标，$\mathcal{L}_{\mathrm{CoT}}$ 为各CoT模式自身的交叉熵损失。训练采用交替优化策略：轮流最小化 $\mathcal{L}_{\mathrm{non-Co T}}$ 和 $\mathcal{L}_{\mathrm{Joint}}^{*}$ 直至收敛（见Algorithm 1）。这一设计使非CoT模式在推理时无需显式生成思维链，却继承了多模态推理的感知能力。

### 3.4 推理效率度量

为量化实时性能，定义每秒动作数（Actions Per Second）：

$$\mathrm{APS} = \frac{N_{\mathrm{act}}}{T_{\mathrm{nav}}}$$

其中 $N_{\mathrm{act}}$ 为导航过程中执行的总体动作数，$T_{\mathrm{nav}}$ 为总导航时间（秒）。隐式推理方法每步仅解码单个动作token，而显式CoT方法需输出数千token的中间推理步骤，导致APS差距约5倍（1.03 vs ~0.2，见Table 2）。

![[assets/figures/papers/paper_list_l2167_https_openaccess_thecvf_com_content_CVPR2026_html_Zuo_FantasyVLN_Unified/figures/001_Figure_1.jpg]]
*Figure 1: Aligning semantic and visual reasoning. Complex real-world navigation tasks are typically multi-stage and long-horizon. Addressing them requires both textual and visual reasoning to jointly enhance semantic planning and visual perception. A critical challenge is how to effectively align these two distinct reasoning capabilities within a unified framework*

![[assets/figures/papers/paper_list_l2167_https_openaccess_thecvf_com_content_CVPR2026_html_Zuo_FantasyVLN_Unified/figures/007_Figure_3.jpg]]
*Figure 3: Qualitative comparison of VAR reconstruction across latent scales. Coarse-to-fine reconstruction shows that early scales (1–4) capture the primary structural content of the images*

## 实验与关键发现

### 核心发现与导航精度

FantasyVLN 在长程视觉语言导航基准 LH-VLN 上全面刷新了记录。如 Table 1 所示，方法在四项核心指标上均取得最优：成功率（SR）2.44%，指令成功率（ISR）11.01%，条件成功率（CSR）9.64%，条件目标达成率（CGT）8.99%。这一结果验证了统一多模态 CoT 推理框架的有效性——通过联合训练文本、视觉和多模态推理模式，模型在共享参数空间下习得了模态不变的推理表征，从而在推理时不生成显式思维链的情况下仍能保持推理感知能力。

![[assets/figures/papers/paper_list_l2167_https_openaccess_thecvf_com_content_CVPR2026_html_Zuo_FantasyVLN_Unified/figures/004_Table_1.jpg]]
*Table 1: Comparison of navigation accuracy with several advanced VLN methods on LH-VLN. The best and second-best results are marked in bold and underlined, respectively*

### 推理效率分析

推理效率是 FantasyVLN 的核心优势之一。Table 2 给出了不同 CoT 方法的动作执行速率（APS）对比。隐式推理方法每次动作仅解码单个 token，而显式 CoT 方法每次动作需输出数千 token 的中间推理步骤。实验表明，FantasyVLN 的隐式 CoT 模式达到 1.03 APS，约为显式 CoT 方法（~0.2 APS）的 **5 倍加速**，将推理延迟降低了一个数量级。这一结果直接验证了“训练时多 CoT，推理时无 CoT”范式的实时性优势。

![[assets/figures/papers/paper_list_l2167_https_openaccess_thecvf_com_content_CVPR2026_html_Zuo_FantasyVLN_Unified/figures/006_Table_2.jpg]]
*Table 2: Comparison of inference efficiency across different CoT reasoning methods. The best results are marked in bold*

值得注意的瓶颈在于：显式视觉 CoT 方法（如 WorldVLA）因需在像素空间解码未来视觉观察，导致单步推理 token 膨胀至 3k–5k 级别，使得实时导航不可行。FantasyVLN 通过紧凑 VAR 潜空间编码将视觉推理压缩为粗粒度潜码，从根本上消除了这一开销。

### 消融实验

**推理模式组合的影响。** Table 3 展示了不同推理模式组合下的导航精度。仅使用无 CoT 模式时，SR 和 CGT 近乎为零；逐步加入文本 CoT 和视觉 CoT 后，各项指标持续提升。当四种模式（无 CoT、文本 CoT、视觉 CoT、多模态 CoT）全部联合训练时，SR 和 CGT 达到最高，表明统一框架通过多模态推理协同最大化了整体导航能力。

**跨模态对齐的关键作用。** Table 4 揭示了跨模态对齐约束的不可或缺性。移除对齐后，SR 从 2.44% 骤降至 0%，ISR 从 11.01% 锐减至 2.39%，CSR 和 CGT 同样大幅退化。这说明，单纯联合训练四种模式不足以将推理能力迁移至无 CoT 模式；跨模态对齐通过强制非 CoT 模式的预测逼近其他推理模式的软目标，是实现隐式推理的关键机制。

**VAR 潜空间尺度的影响。** Figure 4 展示了不同 VAR 尺度下的 ISR 变化。尺度 4 获得最高 ISR 7.41%，表明粗粒度潜码（仅保留图像结构信息）已足以支撑导航所需的视觉推理。过细的尺度反而引入冗余细节，干扰推理质量。Figure 3 的定性重建对比进一步佐证：早期尺度（1–4）已捕获图像的主体结构内容。

**显式与隐式视觉 CoT 解码对比。** Figure 5 显示，在纯文本推理中，显式解码的 ISR（8.26%）优于隐式解码（6.06%），说明文本推理受益于逐 token 的显式生成。然而，通过多模态整合与跨模态对齐，隐式推理总体仍实现了优越的实时性能，验证了框架在推理能力与效率之间的有效折衷。

**训练效率对比。** Figure 6 对比了视觉 CoT 方法的收敛速度。FantasyVLN 的紧凑视觉 CoT 在约 3,000 次迭代即完全收敛，而像素级方法 WorldVLA 需要约 13,800 次迭代，收敛速度提升约 **4.6 倍**。紧凑潜空间解码显著降低了优化难度，加速了训练过程。

### 失败模式与局限性

尽管 FantasyVLN 取得了显著进展，仍存在若干值得关注的局限：

1. **基座模型能力上限。** 当前 VLM 基座并非原生统一生成与理解模型，限制了框架的性能天花板，尤其体现在未来场景想象能力上。在需要精细视觉推理的长程任务中，模型偶尔会产生与真实环境不一致的想象内容。

2. **数据规模限制。** LH-VLN 数据集训练数据有限，紧凑视觉 CoT 在大规模数据上的扩展行为未经验证。在更大数据量下，粗粒度潜码是否仍能保留足够的推理信息，需要进一步探索。

3. **训练范式单一。** 当前仅采用监督微调，未引入环境反馈的强化学习等替代范式。在复杂交互场景中，模型缺乏从错误中自我修正的能力。

这些局限为后续研究指明了方向：开发自适应 VAR 尺度选择机制以解锁多级视觉推理能力，以及引入强化学习利用环境反馈增强多模态 CoT 推理质量。

![[assets/figures/papers/paper_list_l2167_https_openaccess_thecvf_com_content_CVPR2026_html_Zuo_FantasyVLN_Unified/figures/003_Table_3.jpg]]
*Table 3: Comparison of navigation accuracy with different reasoning mode combinations on LH-VLN*

## 定位与知识库关联

### 1. 方法谱系与基线关系

FantasyVLN 所处的 VLN 方法谱系可以从**推理显式化程度**和**模态融合方式**两个维度进行定位。

**显式文本 CoT 方法**：以 **Aux-Think**（Wang et al., NeurIPS 2025）为代表，在导航过程中生成纯文本思维链以辅助语义规划。这类方法的瓶颈在于：文本推理缺乏对视觉观察的直接感知，且容易过拟合稀疏标注的路径描述，在需要精细视觉判断的场景中泛化能力受限。

**纯视觉导航方法**：**NaVid**（Zhang et al., RSS 2024）和 **Uni-NaVid**（Zhang et al., RSS 2025）完全依赖视觉编码进行动作预测，不引入显式推理步骤。它们在短程导航中具有实时性优势，但缺乏对复杂长程任务所需的多步语义规划能力。**NaVILA**（Cheng et al., arXiv 2024）则将类似范式扩展到腿式机器人导航场景。

**像素级视觉 CoT 方法**：**CoT-VLA**（Zhao et al., CVPR 2025）和 **WorldVLA**（Cen et al., arXiv 2025）尝试生成像素空间的未来视觉观察作为推理中间步骤。这类方法面临严重的 token 膨胀问题——每步推理需生成 3k-5k tokens 的视觉内容，导致推理延迟远超实时导航的可接受范围。以 WorldVLA 为例，其训练收敛需要约 13,800 次迭代。

**FantasyVLN 的差异化定位**：FantasyVLN 在上述谱系中占据“统一隐式多模态 CoT”的位置。其核心创新在于三个层面的突破：

1. **推理空间压缩**：将视觉 CoT 的解码空间从像素级压缩到 VAR 潜空间（compact latent decoding），仅需粗尺度潜码（scale 4 即可获得最高 ISR 7.41，见 Figure 4）即可保留导航所需的结构信息，消除了显式方法的 token 膨胀瓶颈。

2. **推理-执行解耦**：通过门控机制（gating mechanism）在训练时联合学习无 CoT、文本 CoT、视觉 CoT 和多模态 CoT 四种模式，推理时仅激活无 CoT 模式进行直接指令-动作映射，实现“训练时多 CoT，推理时无 CoT”的隐式推理范式。

3. **跨模态对齐蒸馏**：引入跨模态对齐约束（cross-mode alignment constraint），以无 CoT 模式为软目标，强制其他推理模式的预测分布与之对齐。该机制是 FantasyVLN 成功的关键——消融实验（Table 4）表明，移除对齐后 SR 从 2.44 降为 0，ISR 从 11.01 骤降至 2.39。

### 2. 适用边界与局限

**适用场景**：
- 长程、多阶段导航任务（LH-VLN 基准），需要语义规划与视觉感知的联合推理。
- 对推理延迟敏感的实时导航系统，要求每步动作决策在毫秒级完成。
- 训练数据包含文本标注和视觉观察的监督微调场景。

**已知局限**（论文明确指出的限制）：

1. **基座模型能力上限**：FantasyVLN 的 VLM 基座并非原生统一生成与理解模型，这限制了框架的性能天花板，尤其是未来场景想象（visual imagination）的质量。若基座模型的生成能力不足，VAR 潜空间编码可能丢失关键视觉细节。

2. **数据规模未验证**：LH-VLN 数据集的训练数据有限，紧凑视觉 CoT 在大规模数据上的扩展行为尚未验证。在更大数据集上，VAR 潜空间的表示容量是否足够，以及跨模态对齐是否仍能有效蒸馏，均为开放问题。

3. **训练范式单一**：当前仅采用监督微调（SFT），未探索强化学习（RL）等替代方案。在需要环境交互反馈的场景中，SFT 的分布外泛化能力可能不足。

**需注意的隐性边界**（基于论文证据推断，需人工验证）：
- 门控机制依赖训练时四种模式的均衡采样，若实际部署中某些模式的数据分布偏移，隐式推理的泛化性可能下降。
- VAR 模型需预训练且与 VLM 解耦，引入额外的模型部署复杂度。
- LH-VLN 以外的 VLN 基准（如 R2R、RxR）上的表现未报告，跨数据集的迁移能力未知。

### 3. 开放问题与未来方向

论文明确提出的开放问题包括：

1. **大规模数据扩展规律**：紧凑视觉 CoT 在更大规模数据集上是否仍能保持训练效率优势（当前相比 WorldVLA 收敛速度提升 4.6 倍）？VAR 潜空间的表示容量是否会成为瓶颈？

2. **强化学习融合**：引入环境反馈的强化学习能否进一步增强多模态 CoT 推理能力？RL 范式下跨模态对齐约束的设计面临非平稳目标分布的挑战。

3. **自适应 VAR 尺度选择**：当前 VAR 尺度为固定值（scale 4），开发自适应尺度选择机制是否可解锁多级视觉推理能力——在简单场景使用粗尺度以加速推理，在复杂场景使用细尺度以保留细节？

**论文未提及但值得探索的方向**：
- 将 FantasyVLN 的隐式推理范式扩展到 VLN 以外的具身任务（如操作、问答），验证跨任务迁移能力。
- 探索在线学习场景下门控机制的动态调整策略，使模型能根据任务难度自适应选择推理深度。
- 研究 VAR 潜空间的可解释性——潜码是否对应可解释的导航语义单元（如“走廊尽头”“左转路口”）？

## 原文 PDF

![[paperPDFs/CVPR_2026/FantasyVLN_Unified_Multimodal_Chain_of_Thought_Reasoning_for_Vision_and_Language_Navigation.pdf]]
