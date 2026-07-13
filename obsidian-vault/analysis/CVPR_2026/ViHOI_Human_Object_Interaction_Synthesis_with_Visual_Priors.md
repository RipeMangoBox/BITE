---
title: "ViHOI: Human-Object Interaction Synthesis with Visual Priors"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ViHOI_Human_Object_Interaction_Synthesis_with_Visual_Priors.pdf
project_link: null
code_link: https://github.com/MPI-Lab/ViHOI
aliases:
- ViHOI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 从2D参考图像通过大视觉语言模型(VLM)提取解耦的视觉先验（空间几何信息）和文本先验（语义控制），并压缩为紧凑token注入扩散模型。
primary_logic: 利用VLM从多幅2D参考图像中提取丰富的交互先验，通过层次解耦策略分别从浅层捕获视觉几何信息、从深层捕获文本语义信息，并经Q-Former压缩为紧凑条件，使扩散模型能够生成逼真且物理一致的人-物交互运动。
claims:
- Q-Former适配器是必要的，直接池化VLM嵌入导致性能崩溃（FID从0.68升至26.03）
- 从VLM提取的文本先验优于CLIP文本编码（Top-1 R-precision从0.35提升至0.41）
- 视觉先验从第3层、文本先验从第12层组合（V3-T12）在所有指标上均优于其他层组合
- ViHOI在未见物体上展现强大泛化能力，性能无明显下降并显著超越基线
---

# ViHOI: Human-Object Interaction Synthesis with Visual Priors

> [!tip] 核心洞察
> 利用VLM从多幅2D参考图像中提取丰富的交互先验，通过层次解耦策略分别从浅层捕获视觉几何信息、从深层捕获文本语义信息，并经Q-Former压缩为紧凑条件，使扩散模型能够生成逼真且物理一致的人-物交互运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | ViHOI：基于视觉先验的人与物体交互合成 |
| 英文题名 | ViHOI: Human-Object Interaction Synthesis with Visual Priors |
| 会议/期刊 | CVPR 2026 |
| Links | [Code](https://github.com/MPI-Lab/ViHOI) · [paper](https://arxiv.org/abs/2603.24383) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ViHOI |
| Dataset | FullBodyManipulation, BEHAVE |

> [!tip] 效果简介
> - FullBodyManipulation 上，FID↓ 0.68 (CHOIS+ViHOI) vs 0.77 (CHOIS) (-0.09)；MPJPE↓ (cm) 14.97 (CHOIS+ViHOI) vs 15.43 (CHOIS) (-0.46)；Contact F1↑ 0.75 (CHOIS+ViHOI) vs 0.70 (CHOIS) (+0.05)。
> - FullBodyManipulation (unseen objects) 上，FID↓ 2.02 (CHOIS+ViHOI) vs 4.99 (CHOIS) (-2.97)。
> - BEHAVE 上，FID↓ 3.90 (CHOIS+ViHOI) vs 4.26 (CHOIS) (-0.36)。

## 概要

### 问题瓶颈

人与物体交互（HOI）运动生成的核心挑战在于**文本描述仅提供抽象的动作语义，缺乏物体形状、尺寸和空间接触等几何与空间先验**。这种信息缺失导致模型面临严重的一对多映射问题：同一句“拿起杯子”可以对应无数种空间轨迹和接触姿态，使得现有方法难以生成物理合理且可控的交互动作。

### 核心洞见与方法定位

ViHOI 的核心思路是**利用大视觉语言模型（VLM）从2D参考图像中提取丰富的交互先验**，并通过层次解耦策略分别获取两类互补信息：

- **视觉先验**：从 VLM 浅层（第3层）提取，保留物体的空间几何与位置信息；
- **文本先验**：从 VLM 深层（第12层）提取，捕获高层次的语义控制信号。

这两类先验经 Q-Former 适配器压缩为紧凑的条件 token，注入扩散模型以引导 HOI 运动生成。ViHOI 是一个**即插即用模块**，仅替换基线模型的文本编码部分，保持其余架构与训练设置不变。

### 方法谱系与知识库定位

ViHOI 属于**基于扩散模型的 HOI 运动生成**谱系，其核心贡献在于将条件信号从纯文本编码升级为 VLM 驱动的多模态先验。相较于同类工作：

- **MDM**（Tevet et al., ICLR 2023）是通用文本到运动扩散模型，ViHOI 为其扩展了视觉先验条件；
- **CHOIS**（Li et al., CVPR 2024）利用稀疏物体航点作为全局路径先验，ViHOI 与其互补，提供更细粒度的空间几何信息；
- **ROG**（Xue et al., CVPR 2025）通过物体表面关键点采样建模几何关系，ViHOI 则以 VLM 隐式编码替代显式几何建模；
- **SemGeoMo**（Yang et al., ECCV 2024）结合 LLM 丰富文本和可供性地图，ViHOI 直接用 VLM 统一提取视觉与文本先验，避免多源信息对齐问题。

### 主要结果速览

ViHOI 在三个基线模型（MDM、ROG、CHOIS）上均实现一致且显著的性能提升，验证了其即插即用特性。在 FullBodyManipulation 数据集上，CHOIS+ViHOI 的 FID 从 0.77 降至 0.68，接触 F1 从 0.70 提升至 0.75。在未见物体上，ViHOI 展现出强大泛化能力，FID 从 4.99 降至 2.02，性能无明显退化且显著超越基线。跨数据集迁移至 BEHAVE 同样有效（FID 从 4.26 降至 3.90）。

### 决定性证据链

消融实验揭示了 ViHOI 设计的关键有效性：

- **Q-Former 适配器是必要条件**：直接池化 VLM 嵌入替代 Q-Former 导致 FID 从 0.68 崩溃至 26.03（Table 4）；
- **VLM 文本先验优于 CLIP**：使用 CLIP 文本编码替代 VLM 文本先验，Top-1 R-precision 从 0.41 降至 0.35（Table 4）；
- **层次解耦策略有效**：视觉先验从第3层、文本先验从第12层组合（V3-T12）在所有指标上均优于其他层组合（Table 5）；
- **单查询配置最优**：Prior Adapter 采用单查询（k=1）在多数指标上优于多查询配置，过多的查询可能稀释语义信号（Supplementary Table 1）。

### 局限与开放问题

当前 ViHOI 的主要局限包括：缺乏细粒度手部标注限制了手指运动与抓取动作的精细生成；训练与推理阶段参考图像的风格差异（渲染 vs. 合成）导致 MPJPE 上升约 2 cm，性能有轻微下降但仍在可接受范围。开放问题指向：如何缩小训练-推理的图像分布差异以释放 GT 渲染时的性能潜力，以及 ViHOI 框架是否可扩展至多物体、多人协作等更复杂交互场景。

### 问题背景：文本到HOI运动生成的“一对多”困境

人与物体交互（Human-Object Interaction, HOI）运动生成旨在根据自然语言描述合成逼真的人体动作序列，同时保持与物体的物理接触。近年来，基于扩散模型的文本到运动生成取得了显著进展，如**MDM**（Tevet et al., ICLR 2023）等工作展示了扩散模型在通用运动生成中的潜力。然而，当这些方法被扩展到HOI场景时，面临一个根本性瓶颈：**文本描述仅提供抽象的动作语义（如“拉椅子”），却无法传递物体形状、尺寸、空间位置以及接触点等关键的几何与空间先验**。这导致模型陷入严重的“一对多”映射问题——同一句文本描述可以对应无数种物理上合理或不合理的交互方式，模型缺乏足够的约束来从中选择正确的那一种。

### 现有方法的缺口：几何先验的缺失与局限

为缓解上述问题，近期工作尝试从不同角度引入额外的先验信息：

- **CHOIS**（Li et al., CVPR 2024）利用稀疏的物体航点（waypoints）作为全局路径先验，引导人体运动轨迹。但航点仅提供粗略的空间约束，无法描述物体本身的几何形态和精细接触关系。
- **ROG**（Xue et al., CVPR 2025）通过物体表面关键点采样和交互距离场建模几何关系，引入了更精细的物体形状信息。然而，该方法依赖特定的几何表示，难以灵活泛化到未见物体。
- **SemGeoMo**（Yang et al., ECCV 2024）结合大语言模型（LLM）丰富文本描述和可供性地图（affordance map）作为语义与几何先验，但仍受限于显式三维几何建模的泛化能力。

这些方法的共同局限在于：**它们要么缺乏对物体视觉几何的充分理解，要么依赖于难以泛化的显式三维表示**。一个关键洞察是：人类在理解“如何与物体交互”时，仅需观察少量2D参考图像即可推断出物体的形状、大小和可供性（affordance），而无需精确的三维模型。这一能力源于强大的视觉理解与常识推理——这正是当前HOI生成模型所缺失的。

### 本文动机：从2D图像中提取可泛化的视觉先验

本文的核心动机是：**能否利用大规模视觉语言模型（VLM）从2D参考图像中提取丰富的交互先验，从而为HOI运动生成提供缺失的几何与空间约束？**

这一思路的吸引力在于：
1. **2D图像易于获取**：训练阶段可从数据集GT运动序列渲染得到，推理阶段可通过文本到图像（T2I）生成模型合成，无需依赖3D物体模型。
2. **VLM蕴含世界知识**：大规模预训练的VLM（如Qwen2.5-VL）具备从图像中理解物体形状、空间关系和交互方式的强大能力，其内部表征天然蕴含了可供性推理所需的多模态知识。
3. **即插即用**：视觉先验可作为条件信号注入现有扩散模型，无需改变其核心架构，具有高度的灵活性和通用性。

基于此，本文提出**ViHOI**——一个即插即用的框架，通过VLM从多幅2D参考图像中提取解耦的视觉与文本先验，经Q-Former压缩为紧凑条件token，注入扩散模型以引导物理一致的人-物交互运动生成。

## 核心方法与创新机理

ViHOI的核心创新在于**将大视觉语言模型（VLM）引入HOI运动生成的条件信号构建**，通过从2D参考图像中提取解耦的视觉与文本先验，替代传统CLIP文本编码器，解决了文本描述缺乏物体几何与空间接触先验的根本瓶颈。

### 创新点一：VLM驱动的多模态先验提取

传统HOI方法（如**MDM** (Tevet et al., ICLR 2023)、**CHOIS** (Li et al., CVPR 2024)、**ROG** (Xue et al., CVPR 2025)）依赖CLIP文本编码器将动作描述映射为条件向量。然而，文本描述如“拉椅子”仅提供抽象语义，无法传达椅子的形状、尺寸、把手位置等对交互至关重要的空间几何信息。这导致模型面临严重的一对多映射问题——同一文本可对应无数种物理上不可行的交互方式。

ViHOI将条件信号的来源从纯文本扩展到**参考图像+文本的联合空间**。其核心操作是：

1. **视觉先验**（$E_v$）：从Qwen2.5-VL的第3层LLM提取视觉嵌入，该浅层保留了丰富的几何与空间线索（物体边界、相对位置、接触区域等）。
2. **文本先验**（$E_t$）：从同一VLM的第12层LLM提取文本token嵌入，捕获高层的语义控制信息。

这种层次解耦策略（V3-T12）是经过严格消融验证的最优配置——Table 5显示，该组合在R-score和FID上均优于其他层组合（如V6-T12、V12-T12等）。其直觉在于：浅层视觉特征尚未被语言语义过度抽象化，仍保留细粒度空间信息；深层文本特征则已完成语义融合，适合作为控制信号。

### 创新点二：Q-Former适配器压缩高维先验

VLM输出的视觉嵌入维度高且长度可变（随图像token数变化），无法直接注入扩散模型。ViHOI设计了两个Q-Former-based Prior Adapters，通过可学习的查询向量$q_v$、$q_t$与VLM特征进行交叉注意力，将高维先验压缩为**单个紧凑条件token**（$c_v$和$c_t$）：

$$c_v = \text{CrossAttention}(q_v, Z_v, Z_v)$$

这一设计的必要性在Table 4中得到有力证实：将Q-Former替换为直接平均池化（ViHOI-Pool）导致FID从0.68骤升至26.03，性能完全崩溃。这表明简单的特征聚合会淹没关键的细粒度交互信息，而交叉注意力机制能够自适应地筛选与运动生成最相关的先验信号。

Supplementary Table 1进一步揭示，单查询（k=1）在多数指标上优于多查询配置（k=2,4,8），过多的查询可能稀释了语义信号的集中度。

### 创新点三：VLM文本先验优于CLIP

一个反直觉的发现是：从VLM深层提取的文本先验**显著优于**传统CLIP文本编码。Table 4中，将VLM文本先验替换为CLIP文本编码（ViHOI-CLIP）使Top-1 R-precision从0.41降至0.35。这表明VLM在联合处理图像与文本时，其内部的文本表征已与视觉上下文深度对齐，携带了CLIP独立文本编码所不具备的场景感知语义。

### 创新点四：即插即用的架构设计

ViHOI的changed slot极为精准——它**仅替换了基线模型的文本编码部分**（Supplementary B明确说明这是唯一的架构修改），保持扩散Transformer主干、训练超参数、损失函数等完全不变。这种非侵入式设计使其成为真正的即插即用模块：Table 1显示，在MDM、ROG、CHOIS三个架构迥异的基线上，ViHOI均实现一致且显著的性能提升（CHOIS+ViHOI的FID从0.77降至0.68，Contact F1从0.70升至0.75）。

### 创新点五：训练-推理解耦的参考图像策略

训练阶段，ViHOI利用数据集GT运动序列渲染2D图像，并依据接触标签选择关键帧（Figure 3），确保视觉条件与运动严格对齐。推理阶段则使用T2I模型（Nano Banana）根据文本提示生成参考图像。这种设计巧妙地利用了T2I模型中蕴含的丰富世界知识来增强对未见物体的泛化能力——Table 2显示，在未见物体上CHOIS+ViHOI的FID为2.02，远优于CHOIS的4.99。Supplementary Table 2显示，推理使用T2I生成图像相比GT渲染图像MPJPE从12.94升至14.97，性能下降约2 cm，但仍在可接受范围且整体仍优于现有方法。

### 方法定位

ViHOI属于**条件信号增强**范式，与**SemGeoMo** (Yang et al., ECCV 2024)利用LLM丰富文本和可供性地图的思路形成互补——前者从视觉端提取几何先验，后者从语义端注入几何知识。ViHOI的独特优势在于其先验直接来自对交互场景的视觉理解，而非对物体可供性的符号化建模，因此在未见物体泛化上表现尤为突出。

ViHOI 的整体框架围绕一个核心设计展开：将多模态视觉-语言模型（VLM）作为先验提取引擎，从一组 2D 参考图像和文本提示中获取解耦的几何与语义先验，并通过紧凑的条件 token 注入运动扩散模型，从而解决 HOI 生成中文本描述缺乏空间与几何约束的瓶颈问题。

### Pipeline 总览

ViHOI 的 pipeline 由四个关键模块串联构成，数据流清晰可追溯：

1. **VLM-based Prior Extractor（VLM 先验提取器）**：接收一组参考图像与结构化文本提示，利用大视觉语言模型 Qwen2.5-VL 进行层次化解耦提取——从浅层（第 3 层）捕获视觉几何信息 $E_v$，从深层（第 12 层）捕获文本语义信息 $E_t$。这种层解耦策略使两个模态的先验在 VLM 内部自然对齐，避免了外部跨模态对齐带来的信息损失。

2. **Q-Former-based Prior Adapters（Q-Former 先验适配器）**：两个独立的 Q-Former 模块分别接收 $E_v$ 和 $E_t$，通过可学习查询向量与 VLM 特征进行交叉注意力计算，将高维、变长的先验嵌入压缩为单个紧凑的条件 token——视觉条件 $c_v$ 和文本条件 $c_t$。投影过程为 $Z_v = \text{LayerNorm}(\text{Linear}(E_v))$，随后 $c_v = \text{CrossAttention}(q_v, Z_v, Z_v)$，文本路径同理。消融实验表明，若用直接平均池化替代 Q-Former，FID 从 0.68 骤升至 26.03（Table 4），证实了 Q-Former 编码的不可替代性。

3. **Diffusion Transformer (DiT) HOI Generator（扩散运动生成器）**：基于扩散模型的运动发生器，以 $c_v$ 和 $c_t$ 作为条件信号，在每个去噪步骤中引导 HOI 运动序列的生成。训练目标为最小化原始序列 $x_0$ 与模型重建之间的均方误差：$\mathcal{L} = \mathbb{E}_{t, x_0}[||x_0 - f_\theta(x_t, t, c)||^2]$。

4. **Reference Image Source（参考图像来源）**：训练与推理阶段采用不同的参考图像获取策略。训练阶段利用数据集 GT 运动序列渲染 2D 图像，并依据接触标签选择关键帧，确保视觉条件与运动严格对齐；推理阶段则使用 Nano Banana 文本到图像模型根据文本提示生成时序连贯的参考图像，以利用其内置的世界知识增强对未见物体的泛化能力。

### 即插即用特性

ViHOI 的架构设计遵循最小侵入原则：对基线模型的唯一修改是将原有的 CLIP 文本编码器替换为 VLM 先验提取器与 Q-Former 模块，其余架构与训练设置保持不变。这一设计使 ViHOI 能够作为即插即用模块应用于 MDM、ROG、CHOIS 三个不同基线模型，在 FullBodyManipulation 数据集上均实现一致且显著的性能提升（Table 1），验证了其架构灵活性与多模态先验的通用价值。

![[assets/figures/papers/paper_list_l1756_ViHOI_Human_Object_Interaction_Synthesis_with_Visual_Priors/figures/002_Figure_2.jpg]]
*Figure 2: Overall architecture of ViHOI. We extract visual priors from a set of reference images and textual priors from the input prompt using a VLM. This allows for natural alignment between priors of the two modalities. Subsequently, two Q-Former-based prior adapters distill these high-dimensional priors into a single compact token, respectively, providing the diffusion model with semantically consistent conditioning signals. At each denoising step, a selected HOI generator uses these compact visual and textual prior tokens to guide the synthesis of realistic, semantically coherent human-object interactions*

### 3.1 基于VLM的解耦先验提取器

ViHOI的核心创新在于利用大视觉语言模型（VLM）作为先验提取引擎，从参考图像和文本提示中获取丰富的交互先验。具体而言，该方法采用 **Qwen2.5-VL** 作为先验提取器，并设计了一种**层次解耦策略**，从VLM的不同中间层分别提取视觉与文本先验：

- **视觉先验 $E_v$**：从Qwen2.5-VL中LLM骨干网络的**第3层**提取视觉嵌入。浅层特征保留了更丰富的空间几何信息（如物体形状、尺寸、空间位置），为交互动作的物理合理性提供关键约束。

- **文本先验 $E_t$**：从LLM骨干网络的**第12层**提取文本Token嵌入。深层特征蕴含更抽象的语义信息，用于控制交互动作的语义一致性。

消融实验（Table 5）验证了这一层选择的必要性：视觉特征从第3层、文本特征从第12层组合（V3-T12）在R-score和FID上均优于其他层组合，证明浅层视觉特征与深层文本特征的互补性对于HOI生成至关重要。

### 3.2 基于Q-Former的先验适配器

从VLM提取的视觉和文本先验是高维、变长的特征序列，难以直接作为扩散模型的条件输入。为此，ViHOI设计了两个**基于Q-Former的先验适配器**，将高维先验压缩为单个紧凑条件Token。

以视觉先验适配为例，处理流程如下：

**步骤1：维度投影。** 将视觉先验嵌入 $E_v \in \mathbb{R}^{N_v \times D_v}$ 映射到运动Token维度 $D$：

$$Z_v = \text{LayerNorm}(\text{Linear}(E_v)) \tag{Eq. 3}$$

其中 $Z_v \in \mathbb{R}^{N_v \times D}$，$N_v$ 为视觉Token数量，$D_v$ 为VLM特征维度。

**步骤2：交叉注意力查询。** 通过可学习查询向量 $q_v \in \mathbb{R}^{k \times D}$ 与投影特征进行交叉注意力，得到紧凑的视觉条件Token $c_v \in \mathbb{R}^{k \times D}$：

$$c_v = \text{CrossAttention}(q_v, Z_v, Z_v) \tag{Eq. 4}$$

文本先验适配器采用相同架构，输出文本条件Token $c_t$。消融实验（Supplementary Table 1）表明，单查询配置（$k=1$）在多数指标上优于多查询配置，过多的查询可能稀释了语义信号。

### 3.3 扩散Transformer HOI生成器

HOI运动生成器基于**扩散Transformer（DiT）** 架构。给定一段HOI运动序列 $x_0$，前向扩散过程逐步添加高斯噪声：

$$q(x_t | x_0) = \mathcal{N}(x_t; \sqrt{\bar{\alpha}_t} x_0, (1 - \bar{\alpha}_t) \mathbf{I}) \tag{Eq. 1}$$

其中 $\bar{\alpha}_t$ 为噪声调度参数，$t$ 为扩散时间步。

模型 $f_\theta$ 以噪声序列 $x_t$、时间步 $t$ 和条件 $c = \{c_v, c_t\}$ 为输入，通过最小化重建损失进行训练：

$$\mathcal{L} = \mathbb{E}_{t, x_0} \left[ \left\| x_0 - f_\theta(x_t, t, c) \right\|^2 \right] \tag{Eq. 2}$$

在推理阶段，模型从随机噪声出发，以视觉和文本先验Token为条件，迭代去噪生成最终的人-物交互运动序列。

### 3.4 训练与推理的参考图像策略

ViHOI在训练和推理阶段采用不同的参考图像获取策略（Figure 3）：

- **训练阶段**：利用数据集中的GT运动序列渲染2D图像，并依据接触标签选择关键帧，确保视觉条件与运动严格对齐。

- **推理阶段**：使用文本到图像（T2I）生成模型 **Nano Banana** 根据文本提示生成时序连贯的参考图像，以利用其蕴含的世界知识增强对未见物体的泛化能力。

消融实验（Supplementary Table 2）显示，使用T2I生成图像相比GT渲染图像会导致性能轻微下降（MPJPE从12.94 cm升至14.97 cm），但仍显著优于不使用视觉先验的基线方法，验证了该策略在实际部署中的可行性。

## 实验与关键发现

### 主实验结果

ViHOI 的核心实验设计围绕一个关键主张展开：**从 VLM 提取的多模态先验可以作为一种即插即用的条件模块，一致地提升现有 HOI 运动生成基线的性能**。为验证这一点，作者将 ViHOI 应用于三种架构各异的基线模型——**MDM**（Tevet et al., ICLR 2023）、**ROG**（Xue et al., CVPR 2025）和 **CHOIS**（Li et al., CVPR 2024）——并在 FullBodyManipulation 数据集上进行评估（Table 1）。实验设置的公平性在于：ViHOI 仅替换了各基线的 CLIP 文本编码器，保持其他架构组件和训练配置完全不变（Supplementary B），因此性能增益可明确归因于多模态先验的引入。

![[assets/figures/papers/paper_list_l1756_ViHOI_Human_Object_Interaction_Synthesis_with_Visual_Priors/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparisons on the FullBodyManipulation dataset [26]. We apply ViHOI as a plug-and-play module to three stateof-the-art HOI motion generation methods, demonstrating its effectiveness and flexibility*

在 FullBodyManipulation 数据集上，CHOIS+ViHOI 取得了 **FID 0.68**（基线 CHOIS 为 0.77，降低 0.09）、**MPJPE 14.97 cm**（基线 15.43 cm，降低 0.46 cm）和 **Contact F1 0.75**（基线 0.70，提升 0.05）。当 ViHOI 与 MDM 和 ROG 结合时，同样观察到一致且显著的性能提升（Table 1），其中 ROG+ViHOI 的 MPJPE 从 17.99 cm 降至 14.99 cm，降幅达 3.0 cm。这组结果直接支撑了 verified_analysis 中的高置信度证据（confidence 0.98）：ViHOI 作为即插即用模块的有效性不依赖于特定基线的架构选择。

在跨数据集泛化方面，BEHAVE 数据集上的结果（Table 3）进一步验证了方法的鲁棒性：CHOIS+ViHOI 取得 FID 3.90（基线 4.26），MPJPE 也有相应改善。值得注意的是，ViHOI 在未使用 CLIP 文本编码器的情况下，其 R-precision 指标（文本-运动匹配度）仍能超越使用 CLIP 的基线，说明 VLM 提取的文本先验在语义对齐上具有独立优势。

![[assets/figures/papers/paper_list_l1756_ViHOI_Human_Object_Interaction_Synthesis_with_Visual_Priors/figures/007_Table_3.jpg]]
*Table 3: Quantitative comparisons on the BEHAVE dataset [3]*

### 泛化能力：未见物体上的表现

HOI 生成的一个核心挑战是对未见物体类别的泛化。Table 2 展示了在 FullBodyManipulation 数据集按物体类别划分的未见物体测试集上的结果。CHOIS+ViHOI 取得了 **FID 2.02**，相比基线 CHOIS 的 4.99 降低了 2.97，MPJPE 从 19.30 cm 降至 14.58 cm。这一显著差距（FID 降低约 60%）表明，ViHOI 从 2D 参考图像中提取的视觉先验捕获了跨物体类别的通用几何和空间关系，而非过拟合于训练物体的特定形状。定性结果（Figure 5，3D-Future 数据集）也显示，在未见物体上生成的交互动作保持了物理合理性和语义一致性。

![[assets/figures/papers/paper_list_l1756_ViHOI_Human_Object_Interaction_Synthesis_with_Visual_Priors/figures/010_Figure_5.jpg]]
*Figure 5: Qualitative comparisons on the 3D-Future dataset [11]. Our approach generates more realistic human-object interactions on unseen objects*

### 消融实验：关键设计选择

消融实验（Table 4）揭示了 ViHOI 架构中三个关键设计的因果作用：

![[assets/figures/papers/paper_list_l1756_ViHOI_Human_Object_Interaction_Synthesis_with_Visual_Priors/figures/008_Table_4.jpg]]
*Table 4: Ablation study on the FullBodyManipulation dataset [26]. We adopt CHOIS [27] as the HOI motion generator in this experiment*

**Q-Former 适配器的必要性。** 将 Q-Former 替换为直接平均池化 VLM 嵌入（ViHOI-Pool）导致 FID 从 0.68 急剧升至 26.03，模型几乎完全崩溃。这表明高维 VLM 特征中包含的细粒度空间信息无法通过简单池化保留，Q-Former 的交叉注意力压缩机制对信息蒸馏至关重要。

**VLM 文本先验优于 CLIP。** 用 CLIP 文本编码器替代 VLM 文本先验（ViHOI-CLIP）使 Top-1 R-precision 从 0.41 降至 0.35，验证了 VLM 深层文本表征在语义对齐上的优势。这一结果与直觉一致：VLM 在联合视觉-语言空间中学习到的文本表征，天然地与视觉先验保持对齐，而 CLIP 的独立文本编码缺乏这种跨模态一致性。

**层次解耦策略的最优配置。** Table 5 系统比较了从 VLM 不同层提取视觉和文本先验的组合。最优配置 **V3-T12**（视觉从第 3 层、文本从第 12 层）在 R-score 和 FID 上均优于其他组合。这验证了该方法的核心洞察：VLM 的浅层（第 3 层）保留了丰富的空间几何信息（适合作为视觉先验），而深层（第 12 层）编码了高层语义（适合作为文本先验）。若将两者颠倒（如 V12-T3），性能显著下降，说明层次选择与先验类型之间存在明确的匹配关系。

补充消融（Supplementary Table 1）还考察了 Prior Adapter 的查询数量：**单查询（k=1）在多数指标上优于多查询配置（k=2, 4, 8）**。过多的可学习查询可能稀释了语义信号，导致条件信息不够紧凑。

### 参考图像来源的影响与失败模式

ViHOI 的训练和推理使用了不同来源的参考图像：训练阶段使用 GT 运动序列渲染的 3D 图像，推理阶段使用 T2I 模型（Nano Banana）生成的合成图像。Supplementary Table 2 量化了这一差异的影响：使用 GT 渲染图像（ViHOI-GT）时 MPJPE 为 12.94 cm，而使用 T2I 合成图像时 MPJPE 升至 14.97 cm，性能下降约 2 cm。作者将此归因于训练-推理图像的**风格分布差异**，并指出这是方法的一个已知局限。

然而，即使存在此降级，ViHOI 的推理性能仍显著超越所有基线。Supplementary Figure 1 的定性分析进一步表明，即便 T2I 生成的参考图像存在瑕疵（如物体比例失真、纹理不准确），生成的 HOI 运动仍能保持物理合理性和语义对齐，说明 ViHOI 对参考图像质量具有一定鲁棒性。

![[assets/figures/papers/paper_list_l1756_ViHOI_Human_Object_Interaction_Synthesis_with_Visual_Priors/figures/013_Figure_1.jpg]]
*Figure 1: Qualitative results on the FullBodyManipulation dataset [26]. The three images on the left side are the reference inputs, while the right side shows the motion sequences generated from them. Despite imperfections in these reference images, the generated HOI motions remain plausible and well aligned with the textual semantics*

### 用户调研

补充材料中的用户调研（Supplementary Figures 2-3）在 FullBodyManipulation 和 3D-Future 数据集上进行了偏好测试。结果与定量指标一致：用户显著偏好 ViHOI 生成的交互运动，认为其在物理合理性和语义一致性上优于基线方法。这为定量指标提供了一致的感知层面验证。

### 方法谱系与知识库定位

ViHOI 在 HOI 运动生成的方法谱系中占据了一个独特位置。与 **CHOIS**（依赖稀疏物体航点作为全局路径先验）和 **ROG**（通过物体表面关键点采样和交互距离场建模几何关系）不同，ViHOI 不直接建模 3D 几何约束，而是通过 VLM 从 2D 参考图像中**隐式**提取几何与语义先验。与 **SemGeoMo**（Yang et al., ECCV 2024）相比，后者结合 LLM 丰富文本和可供性地图，ViHOI 的关键区别在于使用单一 VLM 同时提取视觉和文本先验，并通过层次解耦实现自然的跨模态对齐，避免了多模型级联带来的误差累积。

总体而言，ViHOI 提供了一种轻量、即插即用的先验增强策略，其核心贡献不在于提出新的运动生成架构，而在于证明了 **VLM 中间层表征中蕴含的丰富交互先验可以有效压缩并注入现有扩散模型**，从而显著提升生成质量和泛化能力。

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

ViHOI 面向**文本驱动的人-物交互（HOI）运动生成**任务。该领域的核心瓶颈在于：文本描述仅提供抽象的动作语义（如“拉开椅子”），但缺乏物体形状、尺寸、空间接触点等几何与空间先验。这种信息不对称导致模型面临严重的**一对多映射问题**——同一文本可对应无数种物理上不合理的交互方式——使得生成运动难以保证物理一致性和空间可控性。

### 2. 方法谱系中的位置

ViHOI 在 HOI 运动生成的方法谱系中占据 **“即插即用的多模态先验增强”** 这一独特生态位。它不提出全新的运动生成架构，而是作为条件注入模块，可适配多种现有扩散模型基线。

**基线方法及其与 ViHOI 的关系：**

- **MDM** (Tevet et al., ICLR 2023)：通用文本到运动扩散模型，后被扩展至 HOI 领域。ViHOI 将其 CLIP 文本编码器替换为 VLM 多模态先验提取器（Supplementary B 明确声明这是唯一架构修改），使原本仅依赖文本条件的模型获得视觉几何先验。

- **CHOIS** (Li et al., CVPR 2024)：利用稀疏物体航点作为全局路径先验的 HOI 扩散模型。ViHOI 与之结合时，通过 VLM 从参考图像中提取的视觉先验补充了航点所缺乏的局部几何细节和接触语义，在 FullBodyManipulation 数据集上 FID 从 0.77 降至 0.68，Contact F1 从 0.70 提升至 0.75（Table 1）。

- **ROG** (Xue et al., CVPR 2025)：通过物体表面关键点采样和交互距离场建模几何关系。ViHOI 的视觉先验提供了不同于显式几何建模的互补信息——从 2D 图像中隐式捕获的交互上下文。

- **SemGeoMo** (Yang et al., ECCV 2024)：结合 LLM 丰富文本和可供性地图作为语义与几何先验。与 ViHOI 同属“先验增强”路线，但 ViHOI 的关键差异在于：(1) 使用 VLM 而非 LLM+独立视觉模块，实现多模态先验的自然对齐；(2) 通过层次解耦策略分别从浅层和深层提取视觉几何与文本语义先验。

### 3. 核心方法机制

ViHOI 的方法贡献可分解为三个因果链路：

**链路一：层次解耦的先验提取。** 使用 Qwen2.5-VL 作为先验提取引擎，从第 3 层 LLM 提取视觉嵌入 $E_v$（保留几何与空间信息），从第 12 层提取文本嵌入 $E_t$（保留高层语义）。消融实验（Table 5）证实 V3-T12 组合在所有指标上均优于其他层组合，验证了“浅层视觉+深层文本”解耦策略的有效性。

**链路二：Q-Former 先验适配器。** 通过可学习查询向量与 VLM 特征进行交叉注意力，将高维变长特征压缩为单个紧凑条件 token $c_v$ 和 $c_t$。这是方法的关键工程创新——Table 4 显示，若用直接平均池化替代 Q-Former，FID 从 0.68 崩溃至 26.03，证明压缩编码方式对性能至关重要。Supplementary Table 1 进一步表明单查询（k=1）优于多查询配置，过多的查询可能稀释语义信号。

**链路三：训练-推理参考图像策略分离。** 训练阶段使用 GT 运动序列渲染的 2D 图像（保证条件与运动严格对齐），推理阶段使用 Nano Banana T2I 模型根据文本提示生成参考图像（利用其世界知识增强泛化）。Supplementary Table 2 显示，使用 T2I 生成图像相比 GT 渲染图像 MPJPE 从 12.94 cm 升至 14.97 cm，但性能仍显著优于基线。

### 4. 适用边界与局限

**已知适用场景：**
- 单人与单个刚体物体的交互（FullBodyManipulation、BEHAVE 数据集覆盖的场景）
- 文本描述相对明确的动作类型（拉、推、踢、放置等）
- 物体形状在训练分布内或相近的情况

**明确局限：**
1. **细粒度手部交互缺失**：缺乏手部标注数据，限制了手指运动与精细抓取动作的生成质量。
2. **训练-推理分布偏移**：训练使用干净渲染图像，推理使用 T2I 合成图像，风格差异导致约 2 cm 的 MPJPE 退化（Supplementary Table 2）。
3. **T2I 模型依赖**：对罕见或极端交互场景，T2I 模型可能生成不准确的参考图像，级联影响运动生成质量。

### 5. 开放问题

1. **分布对齐**：如何进一步缩小训练与推理阶段参考图像的分布差异，以完全释放 GT 渲染条件下的性能潜力（MPJPE 12.94 cm → 14.97 cm 的差距）？

2. **时序一致性**：当前参考图像为独立帧，能否利用视频生成模型提供时序更连贯的参考帧序列，从而提升动态交互的连贯性？

3. **场景扩展**：ViHOI 框架是否适用于多物体、多人协作的更复杂交互场景？VLM 的先验提取能力在更拥挤的场景中是否依然有效？

4. **可解释性**：VLM 中间层表征中隐藏的交互先验是否具有可解释的局部结构（如物体可供性区域、接触热区），能否被显式建模以增强可控性和编辑能力？

### 6. 证据强度评估

| 主张 | 证据强度 | 说明 |
|------|---------|------|
| ViHOI 作为即插即用模块在三个基线上一致提升 | **强** (Table 1) | 跨 MDM、ROG、CHOIS 三个架构验证，置信度 0.98 |
| Q-Former 适配器是关键设计 | **强** (Table 4) | Pool 变体 FID 崩溃至 26.03，效应量极大 |
| VLM 文本先验优于 CLIP 文本编码 | **强** (Table 4) | R-precision Top-1 从 0.35 提升至 0.41 |
| 未见物体泛化能力 | **强** (Table 2) | FID 从 4.99 降至 2.02，效应显著 |
| 层次解耦策略 (V3-T12) 最优 | **中强** (Table 5) | 多组对比一致，但层数选择范围有限 |
| 单查询优于多查询 | **中** (Supp. Table 1) | 仅在视觉查询上验证，文本查询固定为 1 |

## 原文 PDF

![[paperPDFs/CVPR_2026/ViHOI_Human_Object_Interaction_Synthesis_with_Visual_Priors.pdf]]
