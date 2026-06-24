---
title: "When Numbers Speak: Aligning Textual Numerals and Visual Instances in Text-to-Video Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/When_Numbers_Speak_Aligning_Textual_Numerals_and_Visual_Instances_in_Text_to_Video_Diffusion_Models.pdf
project_link: "https://h-embodvis.github.io/NUMINA/"
code_link: "https://github.com/H-EmbodVis/NUMINA"
aliases:
- WNSATNVITVDM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在早期去噪阶段动态选择最具实例区分能力的自注意力头与最集中的交叉注意力头，构建可计数的语义布局；随后通过保守的实例级布局精炼（删除最小区域或增加模板实例）修正数量；最后在重新生成中通过调节交叉注意力实现布局引导，从而直接控制生成视频中的对象实例数。
primary_logic: 扩散Transformer的自注意力和交叉注意力头自然包含可提取的实例级空间结构信息，无需求助外部模型或重新训练，即可转化为显式的计数信号并作为全局引导，实现准确的数量控制，同时保持生成质量和时序一致性。
claims:
- 在Wan2.1-1.3B上，NUMINA将CountBench上的计数准确率从42.3%提升到49.7%（+7.4%）；在Wan2.2-5B上从47.8%提升到52.7%（+4.9%）；在Wan2.1-14B上从53.6%提升到59.1%（+5.5%）。
- NUMINA在提高计数准确率的同时，CLIP分数（语义对齐）和时序一致性（TC）也得到提升或维持，例如1.3B模型的CLIP分数从33.9增加到35.6。
- 基于注意力的布局构建方法优于使用外部检测器GroundingDINO的布局（CountAcc 49.7% vs 47.5%）。
- 同时使用重叠成本(C_o)、中心成本(C_c)和时序成本(C_t)的布局精炼策略实现了最优计数准确率49.7%。
---

# When Numbers Speak: Aligning Textual Numerals and Visual Instances in Text-to-Video Diffusion Models

> [!tip] 核心洞察
> 扩散Transformer的自注意力和交叉注意力头自然包含可提取的实例级空间结构信息，无需求助外部模型或重新训练，即可转化为显式的计数信号并作为全局引导，实现准确的数量控制，同时保持生成质量和时序一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 当数字说话：文本到视频扩散模型中数字与视觉实例的对齐 |
| 英文题名 | When Numbers Speak: Aligning Textual Numerals and Visual Instances in Text-to-Video Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.08546) · [Project](https://h-embodvis.github.io/NUMINA/) · [Code](https://github.com/H-EmbodVis/NUMINA) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | NUMINA |
| Dataset | CountBench |

> [!tip] 效果简介
> - CountBench 上，CountAcc (%) 49.7 vs 42.3 (+7.4)；CountAcc (%) 52.7 vs 47.8 (+4.9)；CountAcc (%) 59.1 vs 53.6 (+5.5)。
> - CountBench (CogVideoX) 上，CountAcc (%) 44.4 vs 40.2 (+4.2)。

## 概述

文本到视频（T2V）扩散模型在近年取得显著进展，但在精确数字对齐方面仍存在根本性瓶颈：当提示中包含具体数量词（如“三只狗”）时，生成视频中实际出现的对象数量往往与文本不一致。NUMINA 论文将这一问题归因于两个关键机制——**数字标记的语义弱化**与**潜在空间实例可分离性差**。具体而言，扩散Transformer中数字对应的交叉注意力响应呈现弥散性（图2），无法像名词、动词那样形成强局部激活；同时，高度下采样的时空潜在空间难以稳定编码对象数量，导致计数错误频发。

针对上述瓶颈，NUMINA 提出了一种**无需训练（training-free）的“识别-引导”（identify-then-guide）两阶段框架**。其核心洞察在于：扩散Transformer的自注意力和交叉注意力头中天然蕴含可提取的实例级空间结构信息，无需借助外部模型或重新训练，即可转化为显式的计数信号并作为全局引导，实现准确的数量控制。方法首先在早期去噪阶段动态选择最具实例区分能力的自注意力头与最集中的交叉注意力头，构建可计数的语义布局；随后通过保守的布局精炼（删除最小区域或基于模板添加实例）修正数量错误；最终在重新生成中通过调节交叉注意力实现布局引导。

在 CountBench 基准上的实验表明，NUMINA 在不同规模的 Wan 系列模型上均稳定提升计数准确率：Wan2.1-1.3B 上从 42.3% 提升至 49.7%（+7.4%），Wan2.2-5B 上从 47.8% 提升至 52.7%（+4.9%），Wan2.1-14B 上从 53.6% 提升至 59.1%（+5.5%），同时在语义对齐（CLIP Score）和时序一致性（TC）指标上也获得提升或维持（表1）。跨架构验证（CogVideoX-5B）和用户偏好研究进一步支持了方法的有效性与实用性。

## 背景与动机

### 文本到视频生成中的数字-视觉错位

文本到视频（T2V）扩散模型在生成语义丰富、时序连贯的视频方面取得了显著进展，但在精确遵循文本中的数字约束方面仍存在根本性困难。当提示中包含明确的数量描述（如“三只狗在草地上奔跑”），模型生成的视频中对象实例数往往与文本指定的数量不一致——这一现象被称为**数字-视觉错位**。

**Figure 2** 通过可视化不同词性对应的交叉注意力图揭示了这一问题的深层根源：名词和动词通常能产生强烈且集中的注意力响应，而数字标记的交叉注意力响应则呈现弥散性分布，缺乏明确的局部激活。这意味着，数字信息在扩散模型的潜在空间中未能像语义内容那样形成可辨识的空间结构，导致模型难以将抽象的数量概念转化为具体的实例计数。

### 现有方法的局限

当前应对这一问题的策略主要分为两类：

- **实用技巧**：包括**种子搜索**（生成多个随机种子视频并选择计数准确率最高的结果）和**提示增强**（使用大语言模型丰富对象描述属性）。这些方法在特定场景下有效，但缺乏对生成过程的根本性干预，性能提升有限且不稳定。

- **基于外部模型的方法**：利用目标检测器（如GroundingDINO）或分割模型获取空间布局，再据此引导生成。然而，这类方法引入了额外的模型依赖和计算开销，且外部模型的检测误差会直接传播到生成结果中。

更重要的是，上述方法均未触及问题的本质：扩散Transformer内部的自注意力和交叉注意力机制是否天然包含可用于计数的实例级空间信息？

### 核心洞察与动机

本文的核心发现是：**扩散Transformer的自注意力和交叉注意力头中自然蕴含着可提取的实例级空间结构信息**，无需借助外部模型或重新训练。如 **Figure 4** 所示，不同自注意力头捕捉到多样化的空间模式，其中部分头部展现出显著的实例可分离性——这为从模型内部构建可计数的语义布局提供了可能。

基于这一洞察，本文提出**NUMINA**，一个无需训练的“识别-引导”框架，直接从注意力图中提取显式的实例布局，并通过布局精炼和引导生成实现精确的数量控制。该方法的动机在于：与其依赖外部信号纠正生成结果，不如从扩散模型自身的内部表征中挖掘计数线索，从而在保持生成质量和时序一致性的前提下，显著提升数字-视觉对齐精度。

## 核心创新

NUMINA的核心创新在于揭示并系统性地利用了扩散Transformer内部注意力机制中天然存在的实例级空间结构，构建了一个无需训练、无需外部模型的“识别-引导”两阶段范式，将文本到视频生成中的数字对齐问题从隐式语义约束转化为显式的可计数布局控制。

### 关键洞察：注意力头中的可计数信号

文本到视频扩散模型在精确数字对齐方面存在两个根本瓶颈：其一，数字标记的交叉注意力响应高度弥散，无法像名词、动词那样形成强局部激活（见Figure 2）；其二，扩散Transformer中高度下采样的时空潜在空间导致实例可分离性差，难以稳定编码对象数量。NUMINA的核心洞察在于——扩散Transformer的自注意力和交叉注意力头中天然包含了可提取的实例级空间结构信息。不同自注意力头捕捉到多样化的空间模式（见Figure 4），其中部分头展现出显著的前景-背景分离能力和实例区分度；而交叉注意力头则将文本语义聚焦于特定空间区域。这一发现意味着，无需借助外部检测模型或重新训练，仅通过选择合适的注意力头，即可从模型内部提取出显式的计数信号。

### 两阶段“识别-引导”范式

基于上述洞察，NUMINA将传统端到端的文本条件扩散生成改造为“识别-引导”两阶段流程（见Figure 3）：

**第一阶段——数值错位识别（Numerical Misalignment Identification）**：在早期去噪步骤（$t^\star=20$）从中间层（$\ell^\star=15$）提取自注意力和交叉注意力图。通过基于PCA的三项评分机制——前景-背景分离度（$S_1^h$）、结构丰富度（$S_2^h$）和边缘清晰度（$S_3^h$）——选择最具实例区分能力的自注意力头（见公式 $S(\mathbf{SA}^h) = S_1^h + S_2^h + \gamma S_3^h$），同时选择文本响应最集中的交叉注意力头。将自注意力产生的区域建议与交叉注意力的焦点掩码通过语义重叠分数（$S_0(\mathbf{r}_i, \mathbf{F}) = \frac{|\mathbf{r}_i \cap \mathbf{F}|}{|\mathbf{r}_i|}$）进行筛选和融合，构建出每个名词类别的实例级语义布局。这一布局是显式可计数的，使得后续的数量检测和修正成为可能。

**第二阶段——布局引导生成（Layout-Guided Generation）**：根据提示中的目标数量，对布局进行保守的精炼——通过删除最小区域去除多余实例，或基于模板和三项成本函数（重叠成本 $\mathcal{C}_o$、中心成本 $\mathcal{C}_c$、时序成本 $\mathcal{C}_t$，见公式5-6）优化放置缺失实例。在重新生成过程中，通过修改交叉注意力偏置或预softmax分数，对指定区域进行注意力抑制（删除）或增强（添加），并由随时间递减的强度函数 $\delta(t)$ 控制引导力度，从而直接控制生成视频中的对象实例数。

### 相对于基线的方法论转变

与原生文本到视频扩散模型（如**Wan2.1/2.2**，Team Wan et al., arXiv 2025）相比，NUMINA在以下几个关键维度上实现了根本性的方法论转变：

| 方法维度 | 基线方案 | NUMINA方案 |
|---------|---------|-----------|
| **生成流程** | 端到端文本条件扩散生成，无中间干预 | 两阶段“识别-引导”范式：预生成提取布局，再生成进行布局引导 |
| **计数信息利用** | 仅通过文本交叉注意力隐式编码数字约束 | 从选定的自注意力/交叉注意力头中显式构建可计数的实例布局，据此检测和修正数量错误 |
| **布局获取方式** | 无显式布局 | 基于PCA和三项评分的自注意力头选择 + 基于峰值激活的交叉注意力头选择，融合得到语义布局 |
| **实例数量修正** | 无修正机制 | 保守的布局精炼：删除最小区域 + 基于模板和成本优化的实例添加 |
| **生成引导** | 标准交叉注意力计算 | 修改交叉注意力偏置/预softmax分数，进行区域级注意力抑制或增强 |

值得注意的是，NUMINA的布局构建完全基于模型内部的注意力信号，而非依赖外部检测器。消融实验证实，基于注意力的布局构建方法优于使用**GroundingDINO**等外部检测器的方案（CountAcc 49.7% vs 47.5%，见Table 2），表明模型内部表征比外部视觉模型更适配扩散潜在空间中的实例结构。此外，整个框架是训练无关的，不需要输入视频、空间掩码或辅助重布局网络，可直接应用于现成的预训练模型。

## 整体框架

NUMINA 采用一种免训练的“识别—引导”两阶段范式（identify-then-guide），在不修改扩散模型权重的前提下，将文本中的精确数字约束转化为可执行的视觉布局信号，进而引导生成过程产生正确数量的对象实例。图3给出了完整的流水线概览。

### 两阶段范式

**第一阶段：数值错位识别（Numerical Misalignment Identification）**。给定一个包含数字的文本提示，首先执行一次预生成（pre-generation），在早期去噪步骤（参考时间步 $t^\star = 20$）从中间层（参考层 $\ell^\star = 15$）提取自注意力和交叉注意力图。随后，分别选择最具实例区分能力的自注意力头（通过前景-背景分离度 $S_1^h$、结构丰富度 $S_2^h$ 和边缘清晰度 $S_3^h$ 三项指标加权评分）和文本响应最集中的交叉注意力头，将两者的空间信息融合，构建出显式可计数的实例级语义布局。该布局以类别标签 $l_T$ 标记每个前景像素，使得系统能够直接检测生成结果中的对象数量是否与提示中的目标数字一致。

**第二阶段：布局精炼与引导生成（Layout Refinement and Layout-Guided Generation）**。若检测到数量错误，则对布局进行保守修正：对于多余实例，删除语义图中面积最小的区域；对于缺失实例，以模板（默认使用圆形先验）在优化重叠代价 $\mathcal{C}_o$、中心代价 $\mathcal{C}_c$ 和时序代价 $\mathcal{C}_t$ 的加权组合下搜索最佳插入位置。修正后的布局随后用于重新生成——通过调节交叉注意力的预 softmax 分数，对删除区域进行注意力抑制、对新增区域进行注意力增强，并由单调递减的强度函数 $\delta(t)$ 控制引导力度随时间步衰减，从而在不破坏原有场景结构和时序连贯性的前提下，引导扩散过程生成正确数量的对象。

### 关键设计原则

整个框架的核心洞察在于：扩散 Transformer 的自注意力和交叉注意力头天然包含可提取的实例级空间结构信息，无需求助外部检测器或重新训练即可转化为显式的计数信号。这一原则贯穿于流水线的两个阶段——布局构建完全依赖模型内部注意力特征，布局引导也仅通过修改注意力计算中的偏置项或预 softmax 分数来实现，保持了方法的免训练特性和跨架构可迁移性。

### 补充图表

![[assets/figures/papers/paper_list_l2362_https_arxiv_org_abs_2604_08546/figures/003_Figure_3.jpg]]
*Figure 3: The pipeline of our NUMINA follows a two-phase paradigm. Given a text prompt containing numerals, we first perform the numerical misalignment identification to extract explicitly countable layouts from attention maps. Based on the layout, we further conduct a refinement and a layout-guided generation for the numerically aligned video generation*

## 核心模块与公式推导

NUMINA 遵循“识别-引导”两阶段范式，无需训练、无需外部模型，完全基于扩散Transformer内部注意力图实现数字-视觉对齐。其核心由五个模块串联构成。

### 1. 预生成与注意力提取

在早期去噪步骤 $t^\star = 20$ 和中间层 $\ell^\star = 15$ 运行一次标准前向生成，提取该层的自注意力图 $\mathbf{SA}^h$ 和交叉注意力图 $\mathbf{C}_h$。选择此时刻和层的原因在于：中间层在去噪早期提供了最清晰的实例分离模式，而极早或极晚的步骤要么噪声过大、要么结构已固化，难以提取可计数的布局信息（见图7和图8的消融验证）。

### 2. 注意力头选择

并非所有注意力头都对实例计数有用。NUMINA 分别对自注意力和交叉注意力头进行筛选。

**自注意力头选择**：对每个头 $h$ 的自注意力图 $\mathbf{SA}^h$ 计算三项评分，加权求和得到区分度分数：

$$S(\mathbf{SA}^h) = S_1^h + S_2^h + \gamma S_3^h$$

其中：
- $S_1^h$：前景-背景分离度，衡量注意力图是否将对象与背景清晰分开；
- $S_2^h$：结构丰富度，衡量注意力图包含的空间模式多样性；
- $S_3^h$：边缘清晰度，衡量实例边界的锐利程度；
- $\gamma$：权重系数，平衡各项贡献。

选择得分最高的单个头（Top-1）作为实例区分度最优的自注意力头。消融实验（Table 4）表明，Top-1 策略优于平均多个头（Top-4/Top-8）或随机选择，因为多头的平均会模糊实例边界。

**交叉注意力头选择**：选择对目标名词文本标记响应最集中、峰值激活最强的交叉注意力头，用于构建焦点掩码 $\mathbf{F}$，定位目标类别的语义区域。

### 3. 可计数布局构建

将自注意力头产生的区域建议与交叉注意力焦点掩码融合，生成实例级语义布局。

首先，对自注意力图进行聚类得到候选区域 $\mathbf{r}_i$。然后计算每个区域与焦点掩码的语义重叠分数：

$$S_0(\mathbf{r}_i, \mathbf{F}) = \frac{|\mathbf{r}_i \cap \mathbf{F}|}{|\mathbf{r}_i|}$$

该分数衡量区域 $\mathbf{r}_i$ 与目标类别语义的吻合程度。仅当重叠分数超过阈值 $\tau$ 时，该区域才被认定为有效实例。

最终，对每个目标类别 $T$，构建语义布局图：

$$\mathbf{M}_T(p) = \{ l_T, \quad \text{if } p \in \bigcup_{i : S_0(\mathbf{r}_i, \mathbf{F}) \geq \tau} \mathbf{r}_i$$

其中 $l_T$ 为类别标签，$\mathbf{M}_T$ 是只包含前景实例的二值布局图。通过直接计数 $\mathbf{M}_T$ 中不连通区域的数量，即可获得当前生成的实例数，并与提示中的目标数字比对，识别错位。

### 4. 布局精炼

当检测到数量不匹配时，采用保守的精炼策略：

- **删除多余实例**：移除目标类别中面积最小的区域，减少实例数。
- **添加缺失实例**：基于模板（默认使用圆形先验）在布局中插入新实例。插入位置 $c^*$ 通过最小化总放置成本确定：

$$\mathcal{C}(c) = \mathcal{C}_o + \mathcal{C}_c + \lambda \mathcal{C}_t$$

其中三项成本分别为：

- $\mathcal{C}_o = |\mathbf{C}_i \cap \mathbf{M}_{T,f}|$：重叠成本，新实例模板 $\mathbf{C}_i$ 与现有布局 $\mathbf{M}_{T,f}$ 的交集面积，避免碰撞；
- $\mathcal{C}_c = (c_x - c_x^0)^2 + (c_y - c_y^0)^2$：中心成本，新实例中心 $(c_x, c_y)$ 与现有布局中心 $(c_x^0, c_y^0)$ 的欧氏距离，鼓励靠近整体布局；
- $\mathcal{C}_t = \mathbb{k}^{\angle}[f > 1] \big[ (c_x - c_x')^2 + (c_y - c_y')^2 \big]$：时序成本，当前帧插入位置与上一帧位置 $(c_x', c_y')$ 的距离，仅在多帧（$f > 1$）时激活，保证跨帧稳定性。

消融实验（Table 3）证实，同时使用三项成本达到最优计数准确率 49.7%，而仅使用重叠成本或中心成本均有明显下降。

### 5. 布局引导生成

在重新生成阶段，利用精炼后的布局调节交叉注意力，实现数量控制。具体操作：

- **删除区域**：对布局中标记为删除的像素位置，在交叉注意力计算的预 softmax 分数 $\mathbf{S}_{pre}$ 中施加抑制，降低这些区域对文本标记的响应。
- **新增区域**：对布局中标记为新增的像素位置，计算参考区域的平均预 softmax 分数 $\bar{a}_f$，并将新增区域的分数覆盖为 $\bar{a}_f \cdot \delta(t)$，其中 $\delta(t)$ 是随时间递减的强度函数，确保引导在早期去噪步骤中更强，在后期逐渐减弱以保留生成的自然性。

这种引导机制直接作用于扩散Transformer的交叉注意力计算，无需修改模型权重，也无需外部检测器或重布局网络。

### 补充图表

![[assets/figures/papers/paper_list_l2362_https_arxiv_org_abs_2604_08546/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of the cross-attention maps corresponding to different texts in the prompt. The highlighted areas represent a stronger level of attention between the pixels and the text*

![[assets/figures/papers/paper_list_l2362_https_arxiv_org_abs_2604_08546/figures/004_Figure_4.jpg]]
*Figure 4: The PCA visualization of self-attention maps for Wan2.1-1.3B. (a) Different attention heads naturally capture diverse spatial patterns. (b) We select the head with the highest instance separability for countable layout construction*

## 实验与分析

### 核心定量结果

NUMINA在CountBench基准上的计数准确率（CountAcc）实现了跨模型规模的稳定提升。在Wan2.1-1.3B上，CountAcc从42.3%提升至49.7%（+7.4个百分点）；在Wan2.2-5B上从47.8%提升至52.7%（+4.9个百分点）；在Wan2.1-14B上从53.6%提升至59.1%（+5.5个百分点）（Table 1）。值得注意的是，计数准确率提升的同时，语义对齐和时序一致性均未受损——1.3B模型的CLIP分数从33.9增至35.6，时序一致性（TC）从81.2%升至83.4%，表明NUMINA的布局引导机制在修正数量的同时维持了生成质量。

![[assets/figures/papers/paper_list_l2362_https_arxiv_org_abs_2604_08546/figures/005_Table_1.jpg]]
*Table 1: Comparison of NUMINA with other practical strategies. We report Counting Accuracy (CountAcc), Temporal Consistency (TC), and CLIP Score on Wan [59] of varying scales*

跨架构验证显示，在基于MMDiT架构的CogVideoX-5B（Yang et al., ICLR 2025）上，NUMINA同样将CountAcc从40.2%提升至44.4%（+4.2个百分点）（Table 6），证明方法的架构无关性。

![[assets/figures/papers/paper_list_l2362_https_arxiv_org_abs_2604_08546/figures/013_Table_6.jpg]]
*Table 6: Evaluation results on CogVideoX [70]*

### 消融实验：设计选择的因果链

**布局构建方式。** 基于注意力的布局构建（CountAcc 49.7%）显著优于使用外部检测器GroundingDINO的布局（47.5%）（Table 2）。这一差距揭示了关键因果机制：扩散Transformer内部注意力自然编码了与生成过程一致的实例级空间结构，而外部检测器引入的分布偏移反而损害了布局精度。

**自注意力头选择策略。** 选择单个最具实例区分度的自注意力头（Top-1，CountAcc 49.7%）优于平均多个头（Top-4: 49.0%，Top-8: 48.5%）或随机选择（48.3%）（Table 4）。这一结果验证了方法的核心洞察：不同注意力头捕获的空间模式存在显著差异，选择最佳头可最大化实例可分性，而多头平均反而稀释了判别信息。

**布局精炼成本组件。** 同时使用重叠成本（C_o）、中心成本（C_c）和时序成本（C_t）达到最优CountAcc 49.7%，而仅使用C_o+C_c降至48.9%，仅使用C_o降至48.2%（Table 3）。时序成本C_t的贡献（+0.8个百分点）表明，跨帧稳定性约束对视频生成中的数量控制具有不可忽视的作用。

**对象添加与删除的贡献分解。** 对象添加操作单独使用即可提升5.4个百分点准确率，而删除操作仅提升1.5个百分点（Table 11）。二者的组合存在协同效应（总计+7.4个百分点），说明基础模型更倾向于生成不足数量的对象，添加操作是纠正计数错误的主要驱动力。

**无参考对象添加策略。** 当需要添加对象但缺乏同类别参考实例时，使用圆形模板先验达到49.7%的CountAcc，优于矩形模板（49.5%）和不干预基线（48.8%）（Table 9），证明了方法在信息匮乏场景下的鲁棒性。

### 效率与超参数分析

NUMINA引入的额外计算开销主要体现在预生成阶段的注意力提取。在Wan2.1-1.3B上，挂钟时间从基线的约350秒增至501秒（Table 5）。但与推理加速方法EasyCache集成后，时间可降至355秒，同时CountAcc仅微降至49.4%，展示了方法的实用部署潜力。

![[assets/figures/papers/paper_list_l2362_https_arxiv_org_abs_2604_08546/figures/012_Table_5.jpg]]
*Table 5: Additional time and VRAM cost*

超参数稳定性方面，语义重叠阈值λ在{4, 8, 16}范围内CountAcc分别为49.3%、49.7%、49.5%；注意力提取时间步t⋆和层ℓ⋆的选择在合理范围内均保持稳定性能（Table 10, Figure 7），降低了实际使用中的调参负担。

![[assets/figures/papers/paper_list_l2362_https_arxiv_org_abs_2604_08546/figures/008_Figure_7.jpg]]
*Figure 7: Ablation on the reference timesteps t⋆ for head selection*

### 失败模式与边界

Figure 9揭示了一个典型失败模式：当自注意力头过度聚焦于对象的显著局部特征（如鹦鹉的头部）时，布局构建阶段会将单个对象的头部与身体分离，导致实例过度分割。这种错误在布局精炼阶段无法被纠正（因为删除最小区域会移除部分身体，而添加操作会引入虚假实例），最终导致不可恢复的生成错误。这一失败模式指向方法的根本局限——基于原始注意力的布局构建缺乏整体感知分组能力，当对象具有高度纹理化的局部特征时容易产生碎片化。

此外，论文明确指出方法尚未在极高密度实例场景（如数十或数百个对象）下验证，完全实现任意数字的精确视频生成仍是一个开放挑战。

### 补充图表

![[assets/figures/papers/paper_list_l2362_https_arxiv_org_abs_2604_08546/figures/007_Figure_6.jpg]]
*Figure 6: The per-numeral accuracies for Wan2.1-1.3B*

![[assets/figures/papers/paper_list_l2362_https_arxiv_org_abs_2604_08546/figures/009_Table_2.jpg]]
*Table 2: Ablation on the layout construction method*

![[assets/figures/papers/paper_list_l2362_https_arxiv_org_abs_2604_08546/figures/010_Table_4.jpg]]
*Table 4: Ablation on the self-attention head selection strategy*

![[assets/figures/papers/paper_list_l2362_https_arxiv_org_abs_2604_08546/figures/011_Table_3.jpg]]
*Table 3: Ablation on the components of the layout refinement cost*

![[assets/figures/papers/paper_list_l2362_https_arxiv_org_abs_2604_08546/figures/019_Table_11.jpg]]
*Table 11: Ablation on object addition or removal*

## 方法谱系与知识库定位

### 1. 问题定位：文本到视频扩散模型的计数瓶颈

NUMINA 瞄准的是文本到视频（T2V）扩散模型中一个具体且长期被忽视的问题：**精确数字与视觉实例之间的对齐失败**。现有 T2V 模型能够理解“一只猫”或“三只猫”的语义差异，但在实际生成中往往无法可靠地生成恰好指定数量的对象实例。这一问题的根源在于两个相互交织的瓶颈：

1. **数字标记的语义弱化**：如 Figure 2 所示，数字词（numerals）对应的交叉注意力图呈现弥散性分布，无法像名词、动词那样形成强局部激活。这意味着模型对“三”的理解缺乏可定位的空间约束。
2. **扩散 Transformer 的时空下采样**：高倍率的下采样潜在空间导致实例可分离性差，模型难以稳定编码对象数量。这是架构层面的固有限制，而非训练数据不足的问题。

这两个瓶颈将“计数”问题与一般的语义理解或图像质量提升问题区分开来，构成了 NUMINA 独特的问题定位。

### 2. 方法谱系中的位置

NUMINA 在现有方法谱系中占据了一个独特位置：**无需训练、无需外部模型的全局引导方法**。为理解其定位，需要梳理相关方法脉络。

#### 2.1 文本到图像（T2I）的计数方法

在图像生成领域，计数问题已获得较多关注。现有方法大致可分为三类：

- **布局引导方法**：如 **MPGD**（He et al., CVPR 2023）等方法通过引入显式布局或空间条件来控制对象数量和位置。这类方法通常需要额外的布局网络或空间输入，且需要针对特定模型进行训练。
- **注意力调控方法**：通过修改交叉注意力图来增强或抑制特定区域的语义响应。这类方法通常无需训练，但往往针对单个对象或简单场景设计，缺乏对精确计数的系统处理。
- **后处理/迭代修正方法**：生成多个候选并选择计数正确的输出，或通过迭代编辑修正数量错误。这类方法计算开销大，且无法保证修正后的生成质量。

NUMINA 与这些方法的关键区别在于：它**从扩散 Transformer 内部的自注意力和交叉注意力头中直接提取可计数的实例布局**，无需外部检测器、布局网络或空间掩码。这一设计使其成为完全训练无关（training-free）的方法，同时保持了全局引导的能力。

#### 2.2 文本到视频（T2V）的计数方法

在视频生成领域，计数问题的研究更为稀缺。NUMINA 是首个系统性地解决 T2V 精确计数的工作。其与相关工作的关系如下：

- **原生 T2V 模型**：**Wan2.1**（1.3B, 14B）和 **Wan2.2**（5B）（Team Wan et al., arXiv 2025）以及 **CogVideoX-5B**（Yang et al., ICLR 2025）是 NUMINA 的直接基础模型。这些模型采用标准的端到端扩散生成流程，仅通过文本交叉注意力隐式编码数字约束。NUMINA 在它们的预训练权重之上构建，不修改模型参数。
- **实用策略**：Seed search（生成多个随机种子视频并选择计数准确率最高的结果）和 Prompt enhancement（使用大语言模型丰富对象描述属性）是实践中常用的替代方案。NUMINA 在 Table 1 中与这些策略进行了直接对比，证明了其显著优势。
- **注意力可视化与利用**：在扩散模型中利用注意力图进行控制并非全新思路（如 Prompt-to-Prompt 等），但 NUMINA 的关键创新在于**系统地选择最具实例区分能力的注意力头**，并将其融合为可计数的语义布局，而非简单地增强或抑制注意力。

#### 2.3 关键差异化设计

NUMINA 的五个核心设计决策共同定义了其方法谱系位置：

| 设计维度 | 基线/现有方法 | NUMINA 方案 |
|---------|-------------|-----------|
| 生成流程 | 端到端单次生成 | 两阶段“识别-引导”范式 |
| 计数信号来源 | 隐式（文本嵌入中编码） | 显式（从注意力头构建可计数布局） |
| 布局获取 | 无显式布局或依赖外部检测器 | 基于 PCA 和三项评分的自注意力头选择 + 峰值激活的交叉注意力头选择 |
| 数量修正 | 无修正机制 | 保守的布局精炼（删除最小区域 + 基于成本的模板添加） |
| 生成引导 | 标准交叉注意力 | 注意力偏置调控，由递减强度函数 δ(t) 控制 |

### 3. 适用边界

#### 3.1 适用条件

NUMINA 的设计使其适用于以下场景：

- **模型架构**：基于扩散 Transformer（DiT）架构的 T2V 模型，特别是采用多头自注意力和交叉注意力的设计。已在 Wan 系列（1.3B/5B/14B）和 CogVideoX-5B 上验证。
- **对象类型**：具有可辨识视觉实例的离散对象（如动物、物体），而非连续实体（如“水”、“烟”）。
- **数量范围**：论文主要验证了低到中等数量（≤10 左右）的场景。Figure 6 的每数字准确率分解显示，NUMINA 在高计数场景下改善尤为显著，但极密集实例（数十或数百个）尚未探索。
- **提示结构**：包含明确数字词和可数名词的提示。对于隐含数量的描述（如“一群鸟”）或抽象概念，方法适用性有限。

#### 3.2 适用限制

- **注意力头过度聚焦**：当自注意力头过度聚焦于对象的显著局部（如动物的头部）而非整体时，可能导致实例过度分割（Figure 9 的失败案例）。这是基于原始注意力的布局构建方法的固有局限。
- **密集实例场景**：生成非常密集的对象实例（如人群、鱼群）的场景尚未探索。在这些场景中，实例可分离性可能根本性下降，当前的布局构建和引导策略可能需要重新设计。
- **完全精确计数**：尽管 NUMINA 显著提升了计数准确率（最高 +7.4%），但绝对准确率仍远未达到 100%。完全实现任意数字的精确视频生成仍然是一个开放挑战。

### 4. 局限与开放问题

#### 4.1 已知局限

1. **实例过度分割**：如 Figure 9 所示，当注意力头过度聚焦于对象局部时，单个对象可能被误判为多个实例。这种错误在布局构建阶段发生，且一旦进入布局引导生成阶段，可能引发不可恢复的生成错误。论文指出需要融入更整体的感知分组线索来解决这一问题。
2. **高密度实例未探索**：当前实验未涵盖数十或数百个实例的极端场景。在这些场景中，布局构建中的聚类和重叠阈值可能需要根本性调整。
3. **绝对准确率上限**：即使在最佳配置下（Wan2.1-14B），NUMINA 的计数准确率为 59.1%，仍有约 40% 的样本未能生成正确数量的对象。

#### 4.2 开放问题

1. **感知分组线索的融入**：如何超越原始注意力图，融入更整体的感知分组机制（如基于特征相似性的聚类、基于运动一致性的分组），以避免实例过度分割？这可能需要引入轻量级的视觉感知先验，但需保持训练无关的特性。
2. **任意数量的精确生成**：能否实现针对任意数量的完全精确的视频生成？这可能需要更根本的架构改进，而不仅仅是推理阶段的干预。
3. **密集场景的重新设计**：在高密度实例场景下，当前的“识别-精炼-引导”范式是否仍然有效？可能需要引入密度感知的布局表示和更灵活的实例添加/删除策略。
4. **与训练方法的结合**：NUMINA 证明了注意力头中包含可提取的计数信号。这一发现是否可以反过来用于改进预训练过程，使模型在训练阶段就获得更好的计数能力？

### 5. 知识库定位总结

NUMINA 的核心贡献在于**发现并系统利用扩散 Transformer 中注意力头的实例分离能力**，将其转化为显式的计数信号和全局引导。这一发现具有方法学意义：它表明无需外部模型或重新训练，模型内部已包含可提取的实例级空间结构信息。

在知识库中，NUMINA 应被定位为：
- **问题域**：文本到视频生成的精确控制，特别是数字-视觉对齐
- **方法类**：训练无关的注意力引导方法
- **技术贡献**：注意力头选择机制、可计数布局构建、保守布局精炼、布局引导生成
- **关键发现**：扩散 Transformer 的自注意力和交叉注意力头自然包含可提取的实例级空间结构信息

## 原文 PDF

![[paperPDFs/CVPR_2026/When_Numbers_Speak_Aligning_Textual_Numerals_and_Visual_Instances_in_Text_to_Video_Diffusion_Models.pdf]]