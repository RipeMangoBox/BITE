---
title: "RE-VLM: Event-Augmented Vision-Language Model for Scene Understanding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RE_VLM_Event_Augmented_Vision_Language_Model_for_Scene_Understanding.pdf
project_link: null
code_link: null
aliases:
- RV
- RE-VLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过双流架构同时利用RGB静态外观与事件流高动态范围的运动线索，利用时空对齐模块（STAM）在训练时对齐两种模态，并采用退化感知的图驱动数据生成管道提供可靠监督，使得模型在挑战条件下仍能保持稳健的场景理解。
primary_logic: 事件相机与标准RGB相机在信息上天然互补：前者记录高时间分辨率、宽动态范围的亮度变化，但对静态纹理和颜色不敏感；后者提供丰富的纹理和颜色，但在极端光照或运动下失效。通过将两种模态在特征空间对齐，并在数据生成阶段显式建模退化并仲裁模态置信度，可以大幅提升在不利条件下的视觉-语言理解能力。
claims:
- 在光照挑战数据集PEOD-Chat上，RE-VLM的Caption CI/DO/CU和VQA Acc全面超越纯RGB和纯事件基线，例如Caption CI较RGB-only提升+0.63，VQA Acc提升+0.06。
- 在通用场景数据集RGBE-Chat上，双流融合同样优于单模态，且加入STAM带来一致提升。
- 图驱动数据生成管道相比纯RGB生成基线，在人工审核中校正率仅18.1%（基线54.2%），证明生成的监督更可靠。
- 两个不同LLM裁判（GPT-3.5-Turbo和Qwen3-Omni-30B）评估的趋势一致，验证了结果的信度。
---

# RE-VLM: Event-Augmented Vision-Language Model for Scene Understanding

> [!tip] 核心洞察
> 事件相机与标准RGB相机在信息上天然互补：前者记录高时间分辨率、宽动态范围的亮度变化，但对静态纹理和颜色不敏感；后者提供丰富的纹理和颜色，但在极端光照或运动下失效。通过将两种模态在特征空间对齐，并在数据生成阶段显式建模退化并仲裁模态置信度，可以大幅提升在不利条件下的视觉-语言理解能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | RE-VLM：事件增强的视觉-语言模型用于场景理解 |
| 英文题名 | RE-VLM: Event-Augmented Vision-Language Model for Scene Understanding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.19329) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | RE-VLM |
| Dataset | PEOD-Chat, RGBE-Chat |

> [!tip] 效果简介
> - PEOD-Chat 上，Caption CI 3.68 vs 3.05 (RGB-only) (+0.63)；Caption DO 3.12 vs 2.51 (RGB-only) (+0.61)；Caption CU 3.95 vs 3.32 (RGB-only) (+0.63)。
> - RGBE-Chat 上，Caption CI 4.03 vs 3.97 (RGB-only) (+0.06)；Caption DO 3.50 vs 3.46 (RGB-only) (+0.04)；Caption CU 4.34 vs 4.32 (RGB-only) (+0.02)。

## 概要

### 问题背景

标准视觉-语言模型（VLM）依赖RGB图像进行场景理解，但RGB传感器在低光照、过曝、高动态范围或快速运动等不利条件下会发生严重退化，导致纹理、颜色和动态信息的丢失。这一问题在自动驾驶、夜间监控等安全攸关场景中尤为突出——纯RGB VLM可能完全忽略行人、斑马线或交通灯状态等关键信息。事件相机能够以微秒级时间分辨率、高动态范围记录亮度变化，天然适合捕捉运动和结构轮廓，但其对静态纹理和颜色不敏感。因此，**瓶颈在于单一模态无法在挑战性条件下提供完整的场景表征**。

### 核心方法

RE-VLM 提出了一种**双流视觉-语言模型**，首次将RGB静态外观与事件流动态运动线索在VLM框架内联合建模。其核心设计包含三个关键组件：

1. **退化感知的图驱动数据生成管道**：将同步的RGB帧和事件流转化为结构化场景图，显式标注光照退化类型，并根据退化程度在字段级别仲裁RGB与事件模态的可信度，从而自动合成更可靠的描述文本和视觉问答对。人工审核表明，该管道的标注修正率仅为18.1%，远低于纯RGB生成基线的54.2%（Table 1）。

2. **双流编码器与时序增强**：RGB分支采用标准ViT编码器提取外观特征；事件分支则对多时间切片的事件帧进行ViT编码，并通过多尺度时序深度可分离卷积和SE-style通道加权突出运动显著的帧。

3. **时空对齐模块（STAM）**：在训练阶段，STAM通过并行计算RGB和事件特征的自注意力矩阵，生成统一的时空重要性图，并施加跨模态加权距离损失$L_{CA-WTD}$，强制两种模态在特征空间中对齐。推理时STAM被移除，不增加额外计算开销。

模型采用三阶段渐进训练策略：先进行事件-语言对齐，再加入STAM进行事件-RGB对齐，最后进行端到端指令调优（仅更新LoRA参数）。

### 主要结果

在光照挑战数据集 **PEOD-Chat** 上，RE-VLM 相比纯RGB基线取得显著提升：Caption CI 从3.05提升至3.68（+0.63），VQA准确率从0.57提升至0.63（+0.06）。在通用场景数据集 **RGBE-Chat** 上同样保持优势（Caption CI 4.03 vs 3.97，VQA Acc 0.75 vs 0.73）。消融实验证实，双模态融合和STAM模块各自带来一致的性能增益。此外，使用开源LLM裁判Qwen3-Omni-30B进行交叉验证，结果趋势与GPT-3.5-Turbo裁判一致，排除了单一闭源裁判的偏差风险。

### 方法谱系与知识库定位

RE-VLM 处于**多模态视觉-语言理解**和**事件相机感知**的交叉点。与现有工作相比，其定位如下：

- **相对于纯RGB VLM**（如 **Qwen2.5-VL** (Bai et al., arXiv 2025)、**DeepSeek-VL** (Lu et al., arXiv 2024)、**InternVL** (Chen et al., CVPR 2024)、**LLaVA** (Liu et al., NeurIPS 2023)）：RE-VLM 通过引入事件流补充了RGB在极端光照和运动下的信息缺失，而非仅依赖单一模态的鲁棒性改进。

- **相对于事件专用VLM**（如 **EventGPT** (Liu et al., CVPR 2025)、**EventCLIP** (Wu et al., arXiv 2023)、**EventBind** (Zhou et al., ECCV 2024)）：RE-VLM 不放弃RGB的纹理和颜色优势，而是通过双流架构和STAM实现互补融合，避免了纯事件模型在静态场景理解上的不足。

- **在知识库中的增量贡献**：RE-VLM 首次将RGB-事件双流融合引入VLM范式，并通过图驱动的退化感知数据生成管道解决了高质量多模态监督数据稀缺的问题。其STAM模块提供了一种轻量级的训练时跨模态对齐方案，可推广至其他异构模态融合场景。

### 局限与展望

论文未提供推理速度和计算开销数据，实时部署的可行性需进一步验证。模型仅在PEOD-Chat和RGBE-Chat两个数据集上评估，泛化到更广泛真实场景的能力尚未明确。此外，事件相机硬件的普及程度和同步RGB-事件数据的获取难度仍是实际应用的主要障碍。未来工作可探索将双流架构扩展至深度、红外等更多模态，以及在目标级、像素级理解任务上验证RGB-事件融合的增益。



### 视觉-语言模型在不利条件下的感知瓶颈

视觉-语言模型（Vision-Language Models, VLMs）近年来在通用场景理解任务上取得了显著进展。以**Qwen2.5-VL**（Bai et al., arXiv 2025）、**DeepSeek-VL**（Lu et al., arXiv 2024）、**InternVL**（Chen et al., CVPR 2024）和**LLaVA**（Liu et al., NeurIPS 2023）为代表的RGB-only VLM，依赖标准相机捕获的RGB图像作为唯一视觉输入，在正常光照和静态场景下展现出强大的描述与问答能力。

然而，这些模型面临一个根本性瓶颈：**标准RGB图像在低光、过曝、高动态范围或快速运动等不利条件下严重退化**。当场景光照极端或物体高速移动时，RGB传感器因动态范围有限和曝光时间约束，无法同时保留亮部和暗部的纹理细节，导致图像出现饱和过曝、噪声淹没或运动模糊。此时，依赖单一RGB模态的VLM无法准确解析场景的纹理、颜色及动态信息，场景理解性能大幅下降。如图1所示，在低光场景中，RGB-only VLM因动态范围不足而完全丢失行人和斑马线等关键语义元素。

### 事件相机与RGB的天然互补性

事件相机（Event Camera）提供了一种截然不同的视觉感知范式。与以固定帧率捕获全局亮度的标准相机不同，事件相机异步记录每个像素的亮度变化，输出高时间分辨率（微秒级）、宽动态范围（>120 dB）的事件流。这一特性使其在极端光照和高速运动场景下仍能清晰捕捉物体的运动轮廓和结构边界，但对静态纹理和颜色信息不敏感。

**事件相机与标准RGB相机在信息上天然互补**：前者记录高时间分辨率、宽动态范围的亮度变化，但对静态纹理和颜色不敏感；后者提供丰富的纹理和颜色，但在极端光照或运动下失效。图1的定性对比直观展示了这一互补关系——事件-only VLM能捕捉场景结构和行人运动，却无法判断交通灯的颜色状态。

### 现有事件-语言模型的局限

尽管事件相机在计算机视觉领域已有广泛应用，将其与语言模型结合的工作仍处于早期阶段。**EventCLIP**（Wu et al., arXiv 2023）将CLIP适配到事件域，支持零样本/少样本分类；**EventBind**（Zhou et al., ECCV 2024）构建了事件-图像-文本的统一表示空间；**EventGPT**（Liu et al., CVPR 2025）作为首个事件流专用的VLM，实现了事件-to-文本的直接生成。然而，这些方法均局限于单一事件模态，**未能同时利用RGB的静态外观与事件的动态运动线索**，在需要颜色、纹理等细粒度外观信息的场景理解任务中能力不足。

### 本文动机与核心思路

上述分析揭示了一个明确的研究缺口：**缺乏一个能够联合利用RGB静态外观与事件流动态运动线索的视觉-语言模型，以在挑战性条件下实现鲁棒的场景理解**。

为此，本文提出**RE-VLM**，核心思路是通过双流架构同时利用RGB静态外观与事件流高动态范围的运动线索。具体而言：（1）在数据层面，设计**退化感知的图驱动数据生成管道**，将同步的RGB-事件流转化为结构化场景图，显式标注退化类型并仲裁模态可信度，合成可靠的描述与问答监督；（2）在模型层面，采用**双流编码器**分别提取RGB和事件特征，并通过**时空对齐模块（STAM）**在训练时对齐两种模态，最终由LLM解码器融合两种视觉token生成文本。这一设计使得模型在极端光照和快速运动条件下仍能保持稳健的场景理解能力。



## 核心方法与创新机理

RE-VLM 的核心创新在于系统性地解决了标准视觉-语言模型在不利成像条件下的退化瓶颈。其设计围绕一个中心洞察展开：**事件相机与标准RGB相机在信息上天然互补**——前者以微秒级时间分辨率捕获宽动态范围的亮度变化，但对静态纹理和颜色不敏感；后者提供丰富的纹理与颜色信息，却在低光、过曝、高动态范围或快速运动下严重退化。RE-VLM 通过三个相互协同的 changed slots 将这一洞察工程化为可工作的系统。

### 双流异构模态输入与编码

最根本的 changed slot 在于**输入模态的扩展**：从仅依赖RGB图像变为同时接收RGB图像与异步事件流。与之配套，视觉编码器从单一ViT扩展为**双流编码器**——一个标准RGB编码器与一个专为事件流设计的事件编码器。事件编码器在ViT主干基础上增加了两项关键时序建模机制：

- **多尺度时序深度可分离卷积**：在事件特征的时间维度上施加多尺度一维深度卷积，捕获不同时间尺度的运动模式；
- **SE-style时序加权**：通过压缩-激励式通道注意力，自动突出运动显著的帧，抑制噪声帧。

这一设计使事件编码器能够从稀疏、异步的亮度变化事件中提取结构化的时空特征，为后续与RGB外观特征的融合奠定基础。

### 时空对齐模块与跨模态正则化

双流编码带来了新的挑战：RGB特征与事件特征在语义空间上存在天然鸿沟，简单拼接无法有效融合。RE-VLM 的第二个关键 changed slot 是在训练时引入**时空对齐模块**，替代基线中的无显式对齐或简单拼接方案。

STAM 的核心机制如下：对每一帧，分别计算RGB归一化特征与事件归一化特征的通道内自注意力矩阵，度量各自模态内token之间的亲和度：

$$P _ { r } ^ { ( t ) } = \widehat { R } ^ { ( t ) \top } \widehat { R } ^ { ( t ) } , \qquad P _ { e } ^ { ( t ) } = \widehat { E } ^ { ( t ) \top } \widehat { E } ^ { ( t ) } .$$

随后，将两个自注意力度向量（图度）平均并归一化，得到统一的时空重要性图：

$$\boldsymbol { w } ^ { ( t ) } = \operatorname { n o r m } \left( \frac { 1 } { 2 } \left( \widetilde { \boldsymbol { w } } _ { r } ^ { ( t ) } + \widetilde { \boldsymbol { w } } _ { e } ^ { ( t ) } \right) \right) .$$

基于此重要性图，STAM 施加**跨模态加权时序差异损失**作为训练正则项，迫使模型在运动显著区域对齐两种模态的特征表示：

$$L _ { \mathrm { C A - W T D } } = \frac { 1 } { T _ { c } } \sum _ { t = 1 } ^ { T _ { c } } \langle w ^ { ( t ) } , D ^ { ( t ) } \rangle .$$

总训练目标将语言建模损失与该对齐损失结合：

$$L = L_{LLM} + \lambda L_{CA-WTD}.$$

STAM 仅在训练时使用，推理时不引入额外计算开销——这是一个重要的工程权衡：用训练时的显式对齐换取推理时的高效融合。

### 退化感知的图驱动数据生成管道

高质量监督数据是训练VLM的瓶颈，尤其在事件-RGB联合理解这一新兴领域。RE-VLM 的第三个关键 changed slot 是**从直接生成或人工标注转向图驱动的退化感知数据生成管道**。该管道包含四个步骤：

1. **事件图生成**：从重建的事件帧中提取结构化场景图，专注于运动与轮廓等事件可观测事实；
2. **RGB图生成**：从同步RGB帧中提取场景图，关注外观、颜色、纹理，并显式标注退化类型（如低光、过曝）；
3. **退化感知图融合**：根据退化标签进行字段级仲裁——在RGB退化的区域信任事件信息，反之亦然——融合为统一知识图；
4. **Caption与VQA合成**：从融合图中自动生成描述文本与问答对，经人工筛选后作为监督信号。

该管道的有效性由人工审核结果直接验证：在PEOD样本上，图驱动管道的修正率仅为**18.1%**，而纯RGB生成基线的修正率高达**54.2%**（Table 1）。这意味着生成的监督信号可靠性提升了约3倍，为模型在挑战性场景下的学习提供了更干净的训练目标。

### 三阶段渐进训练策略

上述 changed slots 通过**三阶段渐进训练**串联为一个整体：第一阶段进行事件-语言对齐，第二阶段引入STAM进行事件-RGB对齐，第三阶段进行端到端指令调优（仅更新LoRA参数）。这种渐进式设计确保模型先建立各模态与语言的基本关联，再学习跨模态融合，最终在指令跟随任务上微调，避免了模态间训练信号冲突。

**证据强度**：消融实验（Table 4, Table 5）系统验证了每个 changed slot 的独立贡献——双模态优于单模态，加入STAM优于不加入STAM，且这一趋势在光照挑战数据集PEOD-Chat和通用场景数据集RGBE-Chat上一致成立。两个不同LLM裁判（GPT-3.5-Turbo与Qwen3-Omni-30B）的交叉验证进一步排除了单一评估偏差。



RE-VLM 的整体框架由两条协同主线构成：**图驱动的退化感知数据生成管线**与**双流视觉-语言模型**，二者共同解决“不利条件下 RGB 退化导致 VLM 场景理解失效”这一核心瓶颈。

### 设计动机与信息互补

标准 RGB 相机在低光、过曝、高动态范围或快速运动下严重退化，纹理与颜色信息大面积丢失；事件相机则以微秒级时间分辨率记录亮度变化，拥有极高的动态范围且对运动敏感，但无法感知静态纹理和颜色。RE-VLM 的核心洞察在于：**两种模态在信息上天然互补**——RGB 提供外观与语义，事件提供运动与结构轮廓；将二者在特征空间对齐，并在数据生成阶段显式建模退化并仲裁模态置信度，可以大幅提升挑战条件下的视觉-语言理解能力（Figure 1）。

![[assets/figures/papers/paper_list_l2410_https_arxiv_org_abs_2605_19329/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of RGB-Event complementarity in a challenging low-light scene. RGB-only VLM: Struggles with low dynamic range, missing the pedestrian and crosswalk. Event-only VLM: Captures the scene structure and the pedestrian’s motion but lacks color and texture, failing to determine the traffic light’s state. Our RE-VLM: Provides a complete description, correctly identifying the green light, the pedestrian, the crosswalk, and other vehicles*

### 数据生成管线：从同步流到可靠监督

为了获得可验证的 RGB-事件-文本监督，论文提出了一种**图驱动的退化感知数据生成管道**（Figure 3）。其工作流如下：

1. **事件图生成**：以 RGB 关键帧时间戳为中心，取 N×33 ms（N=4）的事件窗口重建事件帧，然后构建结构化场景图，约束仅描述可观测的运动与轮廓事实。
2. **RGB 图生成**：基于同步 RGB 帧构建场景图，关注外观、颜色、纹理，并**显式标注退化标签**（如过曝、低光区域）。
3. **退化感知图融合**：将两个图合并为统一的 RGB-事件知识图。融合策略是**字段级仲裁**——根据退化标签决定每个属性字段更信任哪种模态（例如，在过曝区域，颜色属性采信事件侧或标记为不可靠）。
4. **描述与 VQA 合成**：将融合图及仲裁策略输入文本生成模型，自动生成描述文本和最多三个问答对，再经人工筛选。

该管线的关键优势在于“可验证性”：生成内容受限于图中显式记录的事实，大幅降低了幻觉。**Table 1** 显示，在 PEOD 样本的人工审核中，本方法的 QA 校正率仅为 **18.1%**，远低于纯 RGB VLM 生成基线的 **54.2%**，证明生成的监督信号明显更可靠。

### 模型架构：双流编码与时空对齐

RE-VLM 模型由五个模块串联而成（Figure 4）：

![[assets/figures/papers/paper_list_l2410_https_arxiv_org_abs_2605_19329/figures/005_Figure_4.jpg]]
*Figure 4: RE-VLM model architecture. Synchronized RGB and event streams are encoded. During training, a Spatio-Temporal Alignment Module (STAM) provides alignment signals and a relation loss. During inference, event features after the temporal DWConv are projected (event adapter) and, together with RGB tokens (RGB adapter), are fed to the LLM*

1. **RGB 编码器**：基于 ViT 提取 RGB 图像特征图 $F_i$。
2. **事件编码器**：将多时片事件表示通过 ViT 编码为时空特征张量 $F^e = \{F_t^e\}_{t=1}^{N_w}$，再经**多尺度时序深度可分离卷积**和 **SE 式通道加权**突出运动显著帧。
3. **时空对齐模块（STAM，仅训练时使用）**：对 RGB 和事件特征分别计算通道内自注意力，得到模态内显著性图；将二者融合为统一的时空重要性权重 $w^{(t)}$，并施加**跨模态加权时序差异损失** $L_{\mathrm{CA-WTD}}$ 惩罚特征不匹配。
4. **模态适配器**：将 RGB 特征和增强后的事件特征分别投影到 LLM 的 token 空间。
5. **LLM 解码器**：接收指令 token、RGB token 和事件 token 的拼接序列，进行因果解码生成文本答案。

### 三阶段渐进训练策略

训练采用由粗到精的三阶段策略（Figure 5）：

- **阶段一：事件-语言对齐**。仅训练事件编码器与适配器，使事件特征与语言空间初步对齐。
- **阶段二：事件-RGB 对齐**。加入 RGB 分支和 STAM，利用 $L_{\mathrm{CA-WTD}}$ 实现跨模态特征对齐。
- **阶段三：指令调优**。端到端训练，但仅更新 LoRA 参数，保持视觉编码器冻结。

总训练目标为：

$$
L = L_{\mathrm{LLM}} + \lambda L_{\mathrm{CA-WTD}}
$$

其中 $L_{\mathrm{LLM}}$ 为标准语言建模损失，$\lambda$ 控制对齐正则的强度。推理时 STAM 被移除，事件特征经时序增强后直接通过适配器与 RGB token 一同送入 LLM，不引入额外推理延迟。

### 输入输出流总结

- **输入**：同步的 RGB 图像 $X$ 与事件流 $S$。
- **处理**：双流编码 → 时序增强（事件侧）→ 适配器投影 → token 拼接。
- **输出**：LLM 生成的文本答案 $A$，支持场景描述和视觉问答两种任务。

### 补充图表

![[assets/figures/papers/paper_list_l2410_https_arxiv_org_abs_2605_19329/figures/002_Figure_2.jpg]]
*Figure 2: Construction of RE-VLM: data generation pipeline and model. Left: A graph-driven pipeline converts synchronized RGB frames and event streams into a graph, extracts verifiable scene facts, and synthesizes reliable caption and QA supervision. Center: Representative examples from the datasets yielded by the pipeline: PEOD-Chat (illumination-challenged scenes) and RGBE-Chat (general scenarios). Right: The RE-VLM model fuses static RGB appearance features with dynamic cues from events and is trained with a progressive strategy for robust captioning and VQA under low-light, high-dynamic-range, and fast-motion conditions*



RE-VLM 的核心架构由双流视觉编码器、时空对齐模块（STAM）、模态适配器和大语言模型解码器四个关键组件构成，其设计目标是融合 RGB 图像的静态外观线索与事件流的动态运动线索，在低光、过曝、高动态范围等不利条件下保持鲁棒的场景理解能力。

### 双流视觉编码器

模型接收两种异构输入：RGB 图像 $X$ 和异步事件流 $S$。两种模态分别由独立的视觉编码器处理：

$$F_i = f_{\mathrm{rgb}}(X), \qquad F_e = f_{\mathrm{event}}(S)$$

其中 $F_i$ 为 RGB 编码器（基于 ViT 主干）提取的二维特征图，$F_e$ 为事件编码器输出的时空特征张量。事件编码器同样以 ViT 为基础，但增加了时序建模能力：将事件流按时间窗口切分为 $N_w$ 个切片，每个切片独立编码后堆叠为四维张量：

$$F^e = \{F_t^e\}_{t=1}^{N_w} \in \mathbb{R}^{N_w \times H \times W \times D}$$

随后通过多尺度时序深度可分离卷积（multi-scale depthwise 1D convolutions）和 SE-style 通道加权机制，突出运动显著的帧并抑制噪声，得到增强后的事件特征 $\tilde{F}^e$。

### 时空对齐模块（STAM）

STAM 仅在训练阶段使用，目的是在特征空间中对齐 RGB 与事件两种模态。其核心操作是双自注意力计算：对第 $t$ 帧的 RGB 归一化特征 $\widehat{R}^{(t)}$ 和事件归一化特征 $\widehat{E}^{(t)}$，分别计算通道内自注意力矩阵：

$$P_r^{(t)} = \widehat{R}^{(t)\top} \widehat{R}^{(t)}, \qquad P_e^{(t)} = \widehat{E}^{(t)\top} \widehat{E}^{(t)}$$

自注意力矩阵 $P_r^{(t)}$ 和 $P_e^{(t)}$ 刻画了各自模态内部 token 之间的亲和度。通过对自注意力矩阵的行求和，得到每个 token 的重要性向量（图度），再将两种模态的图度平均并归一化，形成统一的时空重要性权重：

$$\boldsymbol{w}^{(t)} = \operatorname{norm}\left(\frac{1}{2}\left(\widetilde{\boldsymbol{w}}_r^{(t)} + \widetilde{\boldsymbol{w}}_e^{(t)}\right)\right)$$

### 跨模态对齐加权时序差异损失

基于 STAM 产生的重要性权重，定义跨模态对齐加权时序差异损失（Cross-Attention Weighted Temporal Difference Loss），对 RGB 与事件特征之间的差异进行加权惩罚：

$$L_{\mathrm{CA-WTD}} = \frac{1}{T_c} \sum_{t=1}^{T_c} \langle w^{(t)}, D^{(t)} \rangle$$

其中 $T_c$ 为参与对齐的帧数，$D^{(t)}$ 为第 $t$ 帧 RGB 与事件特征之间的差异度量，$\langle\cdot,\cdot\rangle$ 表示内积运算。该损失使模型在训练过程中主动拉近两种模态在显著区域的特征分布，同时允许非显著区域保持一定的模态特异性。

### 模态适配器与 LLM 解码

RGB 特征 $F_i$ 和增强后的事件特征 $\tilde{F}^e$ 分别通过轻量级适配器投影到 LLM 的 token 空间：

$$T_i = g_i(F_i), \qquad T_e = g_e(\tilde{F}^e)$$

最后，将指令 token $P$、RGB token $T_i$ 和事件 token $T_e$ 拼接后送入 LLM 进行因果解码：

$$A = f_{\mathrm{LLM}}([P; T_i; T_e])$$

### 总训练目标

模型的总损失由标准语言建模损失 $L_{\mathrm{LLM}}$ 和对齐正则项 $L_{\mathrm{CA-WTD}}$ 加权组合而成：

$$L = L_{\mathrm{LLM}} + \lambda L_{\mathrm{CA-WTD}}$$

其中 $\lambda$ 为平衡两种损失的超参数。训练采用三阶段渐进策略：第一阶段进行事件-语言对齐（仅训练事件编码器和适配器），第二阶段加入 STAM 实现事件-RGB 对齐，第三阶段进行端到端指令调优（仅更新 LoRA 参数）。STAM 在推理时被移除，不引入额外计算开销。

### 补充图表

![[assets/figures/papers/paper_list_l2410_https_arxiv_org_abs_2605_19329/figures/003_Figure_3.jpg]]
*Figure 3: Data generation pipeline overview. From reconstructed event frames and RGB images, two modality-specific graphs are constructed. A degradation-aware fusion then merges them into a single RGB-event graph (nodes: entities, edges: relations). Finally, captions and VQA items are synthesized from the fused graph. (S: subject, P: place, D: direction, T: target; H: hierarchical relation; A: attribute.)*

![[assets/figures/papers/paper_list_l2410_https_arxiv_org_abs_2605_19329/figures/007_Figure_5.jpg]]
*Figure 5: Training pipeline. Three compact stages: (1) Initial event– language alignment, (2) Align the event and RGB modalities with STAM, (3) End-to-end instruction tuning*



## 实验与关键发现

### 核心实验设置

RE-VLM的实验评估在两类数据集上展开：光照挑战场景数据集**PEOD-Chat**和通用场景数据集**RGBE-Chat**。评估采用零样本VQA式提示，由LLM裁判对描述（Caption）从信息完整性（CI）、细节导向（DO）和上下文理解（CU）三个维度打分，VQA则报告平均得分（Ave）和属性级准确率（Acc）。为保证评估公平性，所有依赖事件输入的基线模型统一将事件流渲染为事件图像，以便标准视觉编码器处理。此外，论文引入开源LLM裁判**Qwen3-Omni-30B**与默认的GPT-3.5-Turbo裁判进行交叉验证，以规避单一闭源裁判的潜在偏差。

对比基线覆盖RGB-only和事件-only两类主流VLM：RGB侧包括**Qwen2.5-VL**（Bai et al., arXiv 2025）、**DeepSeek-VL**（Lu et al., arXiv 2024）、**InternVL**（Chen et al., CVPR 2024）和**LLaVA**（Liu et al., NeurIPS 2023）；事件侧包括首个事件流专用VLM **EventGPT**（Liu et al., CVPR 2025）、**EventCLIP**（Wu et al., arXiv 2023）和**EventBind**（Zhou et al., ECCV 2024）。

### 主实验结果

**Table 3**汇总了RE-VLM与各基线在PEOD-Chat和RGBE-Chat上的全面对比。在光照挑战的PEOD-Chat上，RE-VLM取得最优性能，Caption CI/DO/CU分别达到3.68/3.12/3.95，VQA Ave和Acc分别为3.82和0.63，相较最强RGB-only基线**Qwen2.5-VL**（CI 3.01）和事件-only基线**EventGPT**（CI 2.32）均有显著提升。在通用场景RGBE-Chat上，RE-VLM同样保持领先，Caption CI/DO/CU为4.03/3.50/4.34，VQA Ave/Acc为4.20/0.75。值得注意的是，RE-VLM在PEOD-Chat上的增益幅度远大于RGBE-Chat，这与核心瓶颈高度吻合——当RGB图像因低光、过曝等原因严重退化时，事件流的互补信息发挥关键作用。

### 消融实验

**Table 4**和**Table 5**分别报告了PEOD-Chat和RGBE-Chat上的模态与STAM消融结果。

**模态消融**：在PEOD-Chat上，仅RGB分支的Caption CI为3.05，仅事件分支为2.40，而双模态融合（RGB+Event）达到3.68，较RGB-only提升+0.63；VQA Acc从0.57提升至0.63（+0.06）。在RGBE-Chat上，双模态融合同样优于任一单模态分支，但增益幅度收窄（Caption CI从3.97升至4.03，+0.06），说明在通用场景下RGB本身已能提供较丰富的信息，事件流的边际贡献相对有限。

**STAM消融**：在双模态融合基础上，加入时空对齐模块STAM带来一致的正向增益。PEOD-Chat上，STAM使Caption CI从3.65升至3.68，VQA Acc从0.62升至0.63；RGBE-Chat上，Caption CI从4.00升至4.03，VQA Acc从0.74升至0.75。虽然单步提升幅度不大，但两个数据集、所有指标的一致性趋势表明，STAM的跨模态对齐损失有效促进了RGB与事件特征在特征空间的融合。

**裁判一致性验证**：**Table 6**展示了使用开源LLM裁判Qwen3-Omni-30B替代GPT-3.5-Turbo的评估结果。RE-VLM的Caption CI为3.29，显著高于Qwen2.5VL的2.17；VQA Acc为0.62，高于后者的0.48。趋势与GPT-3.5-Turbo裁判完全一致，验证了评估结果的可靠性。

### 数据质量验证

**Table 1**报告了数据生成管道的人工审核结果。在PEOD样本上，论文提出的图驱动退化感知生成管道校正率仅为18.1%，而纯RGB VLM生成基线的校正率高达54.2%。这一差距直接证明了在数据生成阶段显式建模退化并仲裁模态置信度的有效性——纯RGB生成在光照退化区域容易产生幻觉性描述，而融合事件流的结构化信息后，生成的监督信号显著更可靠。不过，18.1%的残余修正率也表明，数据生成管道仍存在监督噪声，这可能在一定程度上限制模型性能的上限。

### 定性分析

**Figure 6**展示了过曝交通场景下的定性VQA对比。RGB-only基线因过曝丢失了公交车的大部分纹理信息，事件-only基线虽能捕获运动轮廓但无法分辨颜色，而RE-VLM正确识别了场景中的城市公交车及其颜色属性。这一定性结果与定量消融结论一致：在极端光照条件下，RGB与事件的互补性使模型能够综合静态外观和动态结构信息，实现鲁棒的场景理解。

### 局限与待验证问题

尽管实验结果整体积极，但论文存在以下不足：首先，未提供模型推理速度和计算开销的具体数据，对实时部署场景的参考价值受限；其次，训练和评估均基于特定数据集（PEOD-Chat、RGBE-Chat），在更广泛真实场景中的泛化能力尚未验证；第三，事件相机尚未广泛普及，获取同步RGB-事件数据对实际部署构成挑战；最后，模型在极端快速运动（毫秒级事件爆发）下的特征提取鲁棒性，以及面对更大时空失配时的处理能力，仍属开放问题，需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l2410_https_arxiv_org_abs_2605_19329/figures/008_Table_3.jpg]]
*Table 3: Results on PEOD-Chat and RGBE-Chat. We report LLM-judge scores for Caption and VQA. Our RE-VLM attains the best performance on both benchmarks, with large gains on illumination-challenged PEOD-Chat, showing that jointly leveraging event streams and RGB improves illumination-challenged scene understanding. (*) denotes variants fine-tuned on PEOD-Chat and RGBE-Chat: the RGB-only model is trained with RGB–text supervision, and the event-only model with event–text supervision*

![[assets/figures/papers/paper_list_l2410_https_arxiv_org_abs_2605_19329/figures/009_Table_4.jpg]]
*Table 4: Ablation on input modality and STAM on PEOD-Chat. Single-branch rows drop the other stream at inference. For RGB+Event, ✗ indicates that STAM is not used*

![[assets/figures/papers/paper_list_l2410_https_arxiv_org_abs_2605_19329/figures/011_Table_5.jpg]]
*Table 5: Ablation on input modality and STAM on RGBE-Chat. Single-branch rows drop the other stream at inference. For RGB+Event, ✗ indicates that STAM is not used*

![[assets/figures/papers/paper_list_l2410_https_arxiv_org_abs_2605_19329/figures/004_Table_1.jpg]]
*Table 1: Manual QA corrections on PEOD samples. Human-audited correction rate and count comparing an RGB-only generation baseline [19] with our method; lower is better*

![[assets/figures/papers/paper_list_l2410_https_arxiv_org_abs_2605_19329/figures/012_Table_6.jpg]]
*Table 6: Evaluation using an open-source LLM judge (Qwen3- Omni-30B [30]) in place of GPT-3.5-Turbo. The trends remain consistent with the GPT-3.5-Turbo evaluation across metrics*

![[assets/figures/papers/paper_list_l2410_https_arxiv_org_abs_2605_19329/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative VQA comparison in an overexposed traffic scene. RGB-only and event-only baselines miss the city bus or fail to capture the color, while RE-VLM correctly identifies both, demonstrating robust scene understanding under challenging lighting conditions*

![[assets/figures/papers/paper_list_l2410_https_arxiv_org_abs_2605_19329/figures/006_Table_2.jpg]]
*Table 2: Composition of PEOD-Chat and RGBE-Chat datasets. Data sources and post-screening sample counts for captioning and VQA tasks. In RGBE-ImageNet, the RGB data come from ImageNet [7], and the paired event data are generated using the method of [31]*



## 定位与知识库关联

### 核心问题定位

RE-VLM 试图解决的根本瓶颈是：标准 RGB 图像在低光、过曝、高动态范围或快速运动等不利条件下严重退化，导致依赖纯 RGB 输入的视觉-语言模型（VLM）无法准确解析场景的纹理、颜色及动态信息，场景理解性能大幅下降。这一问题的本质在于，传统 VLM 的视觉编码器（如 ViT）和训练数据均以标准光照下的静态外观为核心假设，缺乏对极端成像条件的鲁棒性设计。

### 方法谱系与差异化

RE-VLM 处于 **多模态视觉-语言理解** 与 **事件相机感知** 的交叉地带。其方法谱系可从以下几个维度定位：

#### 与纯 RGB VLM 的关系

RE-VLM 的直接对比对象是当前主流的 RGB-only VLM，包括 **Qwen2.5-VL**（Bai et al., arXiv 2025）、**DeepSeek-VL**（Lu et al., arXiv 2024）、**InternVL**（Chen et al., CVPR 2024）和 **LLaVA**（Liu et al., NeurIPS 2023）。这些模型在标准场景下表现优异，但在光照挑战场景中性能急剧下降——例如在 PEOD-Chat 上，Qwen2.5-VL 的 Caption CI 仅为 2.17（Table 6），而 RE-VLM 达到 3.68。RE-VLM 的关键差异化在于**输入模态的扩展**：通过引入事件流作为第二视觉通道，弥补了 RGB 在极端光照和运动下的信息缺失，而非仅改进模型架构或训练策略。

#### 与事件 VLM 的关系

在事件感知的 VLM 领域，**EventGPT**（Liu et al., CVPR 2025）是首个专门处理事件流的 VLM，RE-VLM 与之相比的核心差异在于**双流融合而非单模态替换**。EventGPT 仅依赖事件流，虽然能捕捉运动结构和场景轮廓，但缺乏颜色和纹理信息（如无法判断交通灯颜色，见 Figure 1）。RE-VLM 通过同时保留 RGB 和事件两条通路，在互补性上实现了质的提升。在 PEOD-Chat 的消融实验中（Table 4），RGB+Event 双流配置的 Caption CI 达到 3.68，而 Event-only 分支仅为 2.62，差距显著。

#### 与事件-图像对齐方法的关系

在跨模态对齐层面，**EventCLIP**（Wu et al., arXiv 2023）将 CLIP 适配到事件域以实现零样本/少样本识别，**EventBind**（Zhou et al., ECCV 2024）构建了事件-图像-文本的统一表示。RE-VLM 的差异化在于：其一，对齐目标不同——RE-VLM 对齐的是 RGB 与事件两种视觉模态，而非视觉与文本；其二，对齐机制不同——RE-VLM 的时空对齐模块（STAM）通过双自注意力计算模态内显著性并施加跨模态加权距离损失 $L_{\mathrm{CA-WTD}}$，在训练时显式促进特征空间的融合，而非仅依赖对比学习或简单拼接。

### 方法适用的边界条件

根据论文提供的实验证据和训练设置，RE-VLM 的适用边界可归纳如下：

- **输入要求**：需要同步的 RGB 图像与事件流，且事件窗口为中心对齐于 RGB 关键帧的 $N \times 33$ ms 窗口（$N=4$）。这要求相机与事件传感器在空间上已标定、时间上精确同步。对于更大时间失配或空间未对齐的场景，模型能否保持鲁棒性尚未验证。
- **场景类型**：训练和评估覆盖了光照挑战场景（PEOD-Chat，来自 DSEC、MVSEC、PEDRo 等驾驶和监控数据集）和通用场景（RGBE-Chat，含 ImageNet 渲染事件对）。在极端快速运动（毫秒级事件爆发）或完全静态场景（事件流信息稀疏）下的表现缺乏专门分析。
- **任务范围**：当前验证限于场景级描述（Caption）和视觉问答（VQA）。在目标级或像素级任务（如目标检测、语义分割、实例计数）上的迁移能力未经验证。
- **计算开销**：论文未报告推理速度和计算开销数据，对于实时应用（如自动驾驶）的可行性需进一步评估。STAM 模块仅在训练时使用，推理时仅需双流编码和适配器投影，理论上不会引入显著的额外延迟，但缺乏定量证据。

### 局限性与开放问题

#### 已识别的局限

1. **数据生成管线的监督噪声**：尽管图驱动退化感知管道将人工审核修正率从纯 RGB 基线的 54.2% 降至 18.1%（Table 1），仍有近五分之一的样本需要人工校正。这意味着监督信号中存在残余噪声，可能限制模型性能的上限。

2. **事件相机部署的生态限制**：事件相机尚未广泛普及，获取同步的 RGB-事件数据对实际部署构成挑战。RE-VLM 的实用性依赖于事件传感器硬件生态的发展。

3. **泛化性验证不足**：模型在 PEOD-Chat 和 RGBE-Chat 两个特定数据集上评估，在更广泛或未见真实场景（如极端天气、非驾驶场景）中的泛化能力尚未验证。

4. **计算效率未量化**：缺乏推理延迟、吞吐量和显存占用的具体数据，难以评估在资源受限场景下的部署可行性。

#### 开放问题

1. **多模态扩展**：RE-VLM 的双流架构能否推广到更多互补模态（如深度图、红外热成像）并保持高效训练？这需要解决多模态间的对齐复杂度呈组合增长的问题。

2. **细粒度理解任务**：在目标检测、语义分割或实例计数等需要空间精确性的任务上，RGB-事件融合能否带来与场景级理解类似的增益？这需要验证事件流的高时间分辨率是否有助于运动边界和遮挡边界的精确感知。

3. **时序鲁棒性**：模型在极端快速运动（毫秒级事件爆发导致事件帧饱和）或相机-事件传感器时间失配增大时的特征提取是否依然鲁棒？当前的事件窗口设计（$N=4$，约 132 ms）可能无法覆盖所有运动速度范围。

4. **评估可靠性**：论文采用了两种 LLM 裁判（GPT-3.5-Turbo 和 Qwen3-Omni-30B）交叉验证，趋势一致（Table 6），增强了结果信度。但 LLM 裁判本身对光照挑战场景的理解能力是否构成评估上限，仍需人工评估作为最终基准的验证。

5. **事件表示的可迁移性**：当前将事件流渲染为事件图像以兼容标准视觉编码器，这一预处理步骤可能丢失事件数据的稀疏异步特性。是否可以通过原生的事件表示（如体素网格或图神经网络）进一步提升信息保留率，是一个值得探索的方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/RE_VLM_Event_Augmented_Vision_Language_Model_for_Scene_Understanding.pdf]]
