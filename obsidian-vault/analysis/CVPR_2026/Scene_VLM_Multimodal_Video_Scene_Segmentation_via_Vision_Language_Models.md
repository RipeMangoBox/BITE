---
title: "Scene-VLM: Multimodal Video Scene Segmentation via Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Scene_VLM_Multimodal_Video_Scene_Segmentation_via_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- SV
- Scene-VLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将视觉-语言模型（VLM）微调为序列预测器，联合处理多模态镜头表征（视觉帧、字幕、元数据），并引入上下文-聚焦窗口机制以提供充分时序证据。
primary_logic: 利用 VLM 的跨模态推理能力，通过顺序生成边界预测并从 token 级 logits 中提取置信度，实现了可解释、可控的场景分割，并可进一步对齐产生自然语言解释。
claims:
- Scene-VLM 在 MovieNet 上相比先前最佳方法 TranS4mer 实现了 +6 AP 和 +13.7 F1 的显著提升。
- 移除视觉输入导致 F1 从 62.1 急剧下降至 32.0，证明视觉模态对场景分割至关重要。
- 上下文-聚焦窗口设计防止了序列边缘的性能退化，消融实验证实移除聚焦窗口导致边缘预测崩溃。
- 仅需 35 个人工标注样本进行额外微调，模型即可将解释生成的解析失败和幻觉率降至零。
---

# Scene-VLM: Multimodal Video Scene Segmentation via Vision-Language Models

> [!tip] 核心洞察
> 利用 VLM 的跨模态推理能力，通过顺序生成边界预测并从 token 级 logits 中提取置信度，实现了可解释、可控的场景分割，并可进一步对齐产生自然语言解释。

| 字段 | 内容 |
|------|------|
| 中文题名 | Scene-VLM：基于视觉-语言模型的多模态视频场景分割 |
| 英文题名 | Scene-VLM: Multimodal Video Scene Segmentation via Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Berman_Scene-VLM_Multimodal_Video_Scene_Segmentation_via_Vision-Language_Models_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Scene-VLM |
| Dataset | MovieNet-318, BBC Planet Earth, VidChapters-7M |

> [!tip] 效果简介
> - MovieNet-318 上，F1 62.1 vs 48.4 (TranS4mer) (+13.7)；AP 66.8 vs 60.8 (TranS4mer) (+6.0)。
> - BBC Planet Earth 上，AP 45.8 vs 43.6 (TranS4mer) (+2.2)。
> - VidChapters-7M 上，F1 32.2 vs 28.4 (Chapter-LLaMA) (+3.8)。

## 概要

视频场景分割旨在将长视频自动划分为叙事连贯的片段，是视频理解中的基础任务。现有方法普遍存在**视觉中心偏差**——过度依赖视觉帧而忽略对话、字幕等文本叙事线索，同时采用**逐点独立分类范式**，对每个镜头单独预测边界，缺乏序列因果推理能力和可解释性。

针对上述瓶颈，本文提出 **Scene-VLM**，首个将视觉-语言模型（VLM）微调用于视频场景分割的框架。其核心洞察在于：利用 VLM 的跨模态推理能力，将场景分割重构为**因果顺序预测**任务——模型联合处理多模态镜头表征（视觉帧、字幕、元数据），顺序生成边界判定，并通过上下文-聚焦窗口机制为每个决策提供充分的时序证据。此外，Scene-VLM 可从 token 级 logits 中提取可校准的置信度分数，并能对齐生成边界决策的自然语言解释。

在 **MovieNet-318** 基准上，Scene-VLM 相较先前最佳方法 **TranS4mer**（Islam et al., CVPR 2023）实现了 **+6 AP** 和 **+13.7 F1** 的显著提升；在 BBC Planet Earth 上的零样本泛化亦取得最优结果。消融实验证实：移除视觉输入导致 F1 从 62.1 骤降至 32.0，上下文-聚焦窗口设计有效防止了序列边缘的性能崩溃，而仅需 35 个标注样本即可消除解释生成中的格式错误和幻觉。

### 问题背景：视频场景分割的核心挑战

视频场景分割（Video Scene Segmentation）旨在将长视频自动划分为叙事连贯的场景单元，是视频理解中的一项基础任务。与镜头边界检测不同，场景边界通常跨越多个镜头，需要捕捉更高层次的语义转变，如地点切换、时间流逝或情节推进。这一任务在电影、纪录片、用户生成内容等长视频分析中具有广泛的应用价值，包括视频摘要、章节导航和内容索引。

### 现有方法的视觉中心偏差

当前主流的视频场景分割方法普遍存在一个根本性瓶颈：**视觉中心偏差**。以 **TranS4mer**（Islam et al., CVPR 2023）为代表的状态空间方法、以 **MEGA**（Sadoughi et al., ICCV 2023）为代表的多模态融合方法，以及 **BaSSL**（Mun et al., arXiv 2022）等自监督学习方法，其核心建模均围绕视觉帧展开。尽管部分方法引入了音频或文本模态，但这些辅助信号通常被视为视觉特征的补充，而非独立的叙事线索。

这种视觉中心范式在电影等叙事性视频中暴露出明显缺陷：场景转换往往由对话内容、角色出场或情节转折驱动，而这些信息主要蕴含在字幕和元数据中，仅凭视觉帧难以捕捉。例如，一段室内对话场景切换到另一段室内对话场景时，视觉特征可能高度相似，但对话主题和参与角色的变化才是场景边界的关键信号。

### 独立点预测范式的因果推理缺失

现有方法的第二个关键缺陷在于**预测范式的根本局限**。主流方法——包括 **ShotCoL**（Chen et al., CVPR 2021）、**LGSS**（Rao et al., CVPR 2020）以及前述的 TranS4mer 和 BaSSL——均采用逐点独立分类策略：对每个镜头单独预测其是否为场景边界，各预测之间不存在因果依赖。这种范式忽略了场景分割的序列本质——一个镜头被判定为边界，意味着后续镜头属于新场景，这一决策应当因果性地影响对相邻镜头的判断。

独立预测还导致模型缺乏可解释性。当模型输出一个边界决策时，用户无法追溯该决策的依据：是基于视觉变化、对话转折，还是角色更替？这种黑箱特性限制了模型在实际应用中的可信度和可调试性。

### 大语言模型时代的新机遇与缺口

大语言模型（LLM）的兴起为视频理解带来了新的可能。**Chapter-LLaMA**（Ventura et al., CVPR 2025）率先将 LLM 应用于视频章节划分，证明了语言模型在时序视频任务中的潜力。然而，Chapter-LLaMA 仅处理文本模态（字幕/转录文本），完全忽略了视觉信息，本质上仍是一种文本摘要方法，无法利用丰富的视觉叙事线索。

视觉-语言模型（VLM）的成熟——尤其是 Qwen2.5-VL 等开源多模态模型的出现——为弥合这一缺口提供了技术基础。VLM 天然具备跨模态对齐能力，能够同时理解视觉帧和文本内容，并具有强大的序列推理能力。但截至本文工作，尚无方法将 VLM 系统性地应用于视频场景分割任务。

### 本文动机

针对上述三个层面的缺口，本文提出 **Scene-VLM**，核心动机包括：

1. **突破视觉中心偏差**：构建结构化的多模态镜头表征，将视觉帧、对话字幕和角色元数据作为同等重要的叙事线索，使模型能够综合利用场景转换的多模态信号。

2. **建立因果序列推理**：将预测范式从独立点分类转变为因果顺序预测，使每个边界决策依赖于先前预测结果，更贴近人类对叙事结构的理解方式。

3. **赋予可解释性**：利用 VLM 的生成能力，不仅输出边界决策，还能从 token 级 logits 中提取置信度，并可进一步对齐生成自然语言解释，使场景分割从黑箱预测走向透明推理。

## 核心方法与创新机理

Scene-VLM 的核心创新在于将视频场景分割从传统的**逐点独立分类范式**重构为**因果顺序预测任务**，并首次引入视觉-语言模型（VLM）作为序列预测器，实现多模态联合推理与可解释输出。

### 范式转变：从独立点预测到因果序列预测

现有方法（如 **TranS4mer** (Islam et al., CVPR 2023)、**MEGA** (Sadoughi et al., ICCV 2023)）普遍采用逐点独立分类范式——每个镜头是否构成场景边界被独立判定，预测之间不存在因果依赖。这忽略了场景分割的本质：**场景边界是一个序列决策问题，当前决策应依赖于先前的预测结果**。

Scene-VLM 将预测范式彻底改变为因果顺序预测：VLM 按镜头顺序逐一生成“Yes/No”边界判定，每个决策都建立在之前所有预测之上。这一转变使得模型能够建模场景的叙事连贯性，而非孤立地判断单镜头特征。消融实验证实，将焦点窗口缩减至单镜头（即退化为近似独立预测）会导致性能持续下降，证明因果链式预测对性能提升至关重要。

### VLM 作为多模态序列预测器

不同于以往方法仅使用视觉帧或有限模态融合，Scene-VLM 构建了**结构化的多模态镜头表征**，将视觉帧、字幕（对话）和元数据（角色信息）统一编码为 VLM 的输入序列。这使得模型能够：

- **联合利用视觉与文本叙事线索**：场景边界往往由对话主题转换或角色出场变化驱动，纯视觉方法无法捕捉这些信号。
- **通过 token 级 logits 提取置信度**：利用 VLM 输出中“Yes”和“No” token 的 softmax 概率，计算归一化置信度分数

$$ \mathrm{conf}_i = \frac{p_i(\mathrm{Yes})}{p_i(\mathrm{Yes}) + p_i(\mathrm{No})} $$

这一机制无需额外训练，直接从模型内部状态中提取预测的可靠程度，为下游应用提供可控性。

### 上下文-聚焦窗口机制

传统滑动窗口方法在序列边缘存在上下文不足的问题。Scene-VLM 设计了**上下文-聚焦窗口**（context–focus window）：一个较大的上下文窗口（如 20 个镜头）提供充分的时序证据，而预测仅在中部的聚焦窗口（如 10 个镜头）内输出。这一设计的关键效果是：

- **防止序列边缘性能崩溃**：无聚焦机制时，序列边界处的 F1 急剧下降；引入聚焦窗口后，各位置性能保持稳定。
- **平衡上下文充分性与计算效率**：上下文窗口提供跨场景的全局视野，聚焦窗口确保每个决策都有前后双向证据支撑。

### 可解释性对齐

Scene-VLM 的 VLM 架构天然支持**生成场景边界决策的自然语言解释**。通过少量人工标注样本（仅 35 个）进行额外微调，模型即可输出连贯的判定理据，解释为何某个镜头被判定为场景边界——涉及视觉变化、对话主题转换或角色出现/消失等具体线索。这一能力在以往方法中完全缺失。

### 方法能力全景对比

Table 1 将 Scene-VLM 与代表性方法进行了能力维度的系统对比，凸显其全面性：同时支持顺序预测、置信度评分、可解释性、电影级场景分割和视频章节划分五项关键能力，而所有 baseline 方法均存在至少两项缺失。

Scene-VLM 将视频场景分割重新定义为**视觉-语言模型（VLM）的顺序预测任务**。其核心 pipeline 由四个紧密耦合的模块构成：多模态镜头表征构建、上下文-聚焦窗口划分、VLM 序列预测、以及置信度提取。此外，模型可通过额外对齐微调，为每个边界决策生成自然语言解释。

### 多模态镜头表征构建

每个镜头被转换成一个统一的结构化表示，包含三类信息：

- **视觉帧**：从镜头中采样关键帧（默认 3 帧），提供场景构图、光照变化、人物位置等视觉线索。
- **字幕/对话**：镜头对应的语音转录文本，承载叙事推进和对话语义。
- **元数据**：可选的角色身份（Actor-ID）和镜头序号（Shot-ID），提供角色出场信息及序列位置信号。

消融实验证实，**视觉模态是场景分割的支柱**——移除视觉输入后 F1 从 62.1 骤降至 32.0（Table 4），而 Shot-ID 标记的移除也会导致 1.3 点 F1 下降，说明序列位置信息对模型推理有辅助作用。

### 上下文-聚焦窗口划分

为处理长视频，Scene-VLM 采用**上下文-聚焦窗口（context–focus window）**机制。从视频中提取连续 $N$ 个镜头构成上下文窗口（默认 20 个镜头），其中**仅对中心聚焦窗口内的镜头（默认 10 个）输出边界预测**。上下文窗口为聚焦窗口提供前后时序 padding，使每个预测都能获得充分的因果证据。

这一设计的关键作用体现在序列边缘位置：**移除聚焦窗口后，序列首尾的预测性能急剧崩溃**（Figure 5），而保留聚焦机制则使各位置性能保持稳定。同时，将聚焦窗口缩减至单镜头会持续损害性能，证明模型受益于跨多个镜头的因果关联预测。

### VLM 序列预测

Scene-VLM 基于 **Qwen2.5-VL-7B** 微调，将多模态镜头表征序列 $C$ 与任务指令 $P$ 输入 VLM $\mathcal{M}$，得到输出 logits：

$$Y = \mathcal{M}(C, P)$$

模型按镜头顺序逐一生成“Shot i: Yes/No”格式的边界判定。与现有方法采用的**逐点独立分类**不同，Scene-VLM 的序列预测范式使**当前镜头的决策因果性地依赖之前所有预测**，从而捕捉场景边界的时序逻辑。这一范式转变是方法的核心创新之一——它将场景分割从孤立判断提升为上下文感知的因果推理过程。

### 置信度提取

Scene-VLM 从 VLM 的 token 级 logits 中提取置信度，而非依赖额外的分类头。对于每个镜头 $i$ 的预测位置，计算“Yes”和“No” token 的概率：

$$p_j(t) = \frac{\exp(y_j[t])}{\sum_{u \in V} \exp(y_j[u])}$$

然后归一化得到边界置信度：

$$\mathrm{conf}_i = \frac{p_i(\mathrm{Yes})}{p_i(\mathrm{Yes}) + p_i(\mathrm{No})}$$

此方案无需修改模型架构即可提供可校准的置信度估计，使下游应用可按需过滤低置信度预测。

### 解释生成对齐（可选）

通过额外监督微调，Scene-VLM 可对齐生成边界决策的自然语言解释。仅需 **35 个人工标注样本**，模型即可将解释生成中的格式错误和幻觉率降至零（Table 9）。Figure 6 展示了典型示例：模型为《林肯》中的场景过渡提供基于视觉变化、对话和角色出场的简要理据。

### 输入输出流总结

**输入**：连续镜头的多模态表征序列（视觉帧 + 字幕 + 元数据），通过上下文-聚焦窗口组织。  
**输出**：聚焦窗口内每个镜头的边界判定（Yes/No）、对应置信度分数，以及可选的决策解释。  
**端到端流程**：视频 → 镜头切分 → 多模态表征构建 → 窗口划分 → VLM 顺序预测 → 置信度提取 → 场景边界集合（及解释）。

![[assets/figures/papers/paper_list_l2416_https_openaccess_thecvf_com_content_CVPR2026_html_Berman_Scene_VLM_Multi/figures/001_Figure_1.jpg]]
*Figure 1: Video scene segmentation with Scene-VLM. We present Scene-VLM, the first vision-language model (VLM) framework fine-tuned for video scene segmentation. Scene-VLM jointly processes visual frames, dialogue, and metadata from consecutive shots to sequentially predict scene boundaries with associated confidence scores, and can be aligned to produce coherent post-hoc explanations for its decisions*

Scene-VLM 将视频场景分割重构为**因果顺序预测**任务，其核心由五个紧密耦合的模块构成。

### 多模态镜头表征构建

每个镜头被转换为统一的结构化表示，包含三类信息：

- **视觉帧**：从镜头中等间隔采样固定数量的 RGB 帧，作为 VLM 的视觉输入 token。
- **字幕/对话**：镜头内对应的语音转录文本，提供叙事层面的语义线索。
- **元数据**：可选的角色身份（Actor-ID）和镜头序号（Shot-ID），前者帮助模型追踪人物出场连续性，后者为序列位置提供显式锚点。

消融实验表明，移除视觉输入导致 F1 从 62.1 骤降至 32.0（Table 4），证实视觉模态对场景边界感知的不可替代性；移除 Shot-ID 则使 F1 下降 1.3 点，说明位置标识对序列推理有辅助作用。

### 上下文-聚焦窗口机制

为平衡长程时序依赖与计算效率，Scene-VLM 采用**上下文-聚焦窗口**设计：

- **上下文窗口**（默认 20 个连续镜头）：提供充足的时序上下文，使模型能感知场景过渡前后的叙事变化。
- **聚焦窗口**（默认中心 10 个镜头）：模型仅对聚焦窗口内的镜头输出边界预测，上下文窗口中的其余镜头仅作为信息源参与注意力计算，不产生预测。

该设计的必要性在 Figure 5 中得到直接验证：移除聚焦机制后，序列边缘位置的预测性能急剧崩溃；而保留聚焦机制时，各位置性能保持稳定。此外，Table 5 的窗口大小消融显示，增大上下文窗口可稳定提升 F1，但聚焦窗口缩小至单镜头（l_focus=1）会持续损害性能，证明模型受益于跨多镜头的因果关联预测。

### VLM 序列预测

给定上下文窗口内的多模态镜头序列 $C$ 和任务指令 $P$，微调后的 VLM（基于 Qwen2.5-VL-7B）执行顺序推理：

$$Y = \mathcal{M}(C, P)$$

其中 $\mathcal{M}$ 为 VLM 模型，$Y$ 为输出的 token 级 logits。模型按镜头顺序依次输出 “Shot i: Yes” 或 “Shot i: No”，每个边界决策因果依赖于之前所有已生成的预测 token。这一顺序范式替代了传统方法中每个镜头独立分类的点预测方式，使模型能利用已判定的场景结构信息指导后续决策。

### 置信度提取

Scene-VLM 从 VLM 的 token 级 logits 中提取可解释的置信度分数，而非依赖额外训练的标量头。对于镜头 $i$，首先计算 “Yes” 和 “No” token 在输出位置 $j$ 的 softmax 概率：

$$p_j(t) = \frac{\exp(y_j[t])}{\sum_{u \in V} \exp(y_j[u])}$$

其中 $V$ 为词表，$y_j[t]$ 为 token $t$ 在位置 $j$ 的 logit。镜头 $i$ 的边界置信度定义为：

$$\mathrm{conf}_i = \frac{p_i(\mathrm{Yes})}{p_i(\mathrm{Yes}) + p_i(\mathrm{No})}$$

该归一化分数落在 $[0,1]$ 区间，直接反映模型对边界判定的确信程度，无需额外校准步骤。

### 解释生成对齐（可选模块）

在基础分割模型之上，Scene-VLM 可通过额外监督微调对齐生成自然语言解释。仅需 35 个人工标注的边界-解释对进行微调，模型即可在输出边界判定的同时生成简洁的文本理据，且解析失败率和幻觉率均降至零（Table 9）。解释内容通常涵盖视觉变化、对话转折和角色出场等线索（Figure 6 示例）。

### 注意力分析辅助工具

为理解模型的跨模态推理行为，Scene-VLM 引入注意力分析方法。对于输出 token $i$，其对所有视觉输入 token $\mathcal{V}$ 的聚合注意力为：

$$\sum_{j \in \mathcal{V}} A_{ij}$$

经 token 数量归一化后的平均注意力为：

$$\frac{1}{|\mathcal{V}|} \sum_{j \in \mathcal{V}} A_{ij}$$

Figure 3 的注意力分布可视化揭示了两个关键发现：(a) 聚合注意力中视觉模态占主导地位，且模型高度依赖先前输出的预测 token；(b) 长度归一化后，字幕和角色 ID 的贡献与视觉 token 可比，证明文本模态在细粒度推理中同样发挥重要作用。

## 实验与关键发现

### 主实验结果

Scene-VLM 在三个核心基准上均取得最优性能，验证了其跨模态序列预测范式的有效性。

**MovieNet-318 数据集** (Table 2) 上，Scene-VLM 以 62.1 F1 和 66.8 AP 显著超越此前最佳方法 **TranS4mer**（Islam et al., CVPR 2023）的 48.4 F1 和 60.8 AP，提升幅度分别达 +13.7 F1 和 +6.0 AP。相较于多模态融合方法 **MEGA**（Sadoughi et al., ICCV 2023）的 47.2 F1，优势更为明显。值得注意的是，Scene-VLM 仅使用视觉帧和字幕即可达到 60.8 F1，已超过此前所有方法的完整模态性能，表明 VLM 的跨模态推理能力是性能跃升的核心驱动力。

**BBC Planet Earth 零样本泛化** (Table 3) 中，Scene-VLM 以 45.8 AP 超越 TranS4mer 的 43.6 AP（+2.2），证明模型在未见域上仍保持鲁棒性。该数据集为自然纪录片，与 MovieNet 的电影叙事风格存在显著域差异，零样本条件下的正向迁移表明 VLM 预训练知识有效支撑了跨域泛化。

**视频章节划分** (Table 8) 任务上，在匹配 Qwen2.5-VL-7B 骨干的条件下，Scene-VLM 以 32.2 F1 超越 **Chapter-LLaMA**（Ventura et al., CVPR 2025）的 28.4 F1（+3.8），同时在其他指标上全面领先。这验证了顺序预测范式相比独立点预测在结构化视频理解任务中的通用优势。

### 消融实验

#### 输入组件消融

Table 4 揭示了各模态对场景分割的贡献权重：

![[assets/figures/papers/paper_list_l2416_https_openaccess_thecvf_com_content_CVPR2026_html_Berman_Scene_VLM_Multi/figures/009_Table_4.jpg]]
*Table 4: Input component ablation. Top section shows removal of individual components; bottom section shows performance with only single components*

- **视觉模态是核心支柱**：移除视觉输入（仅保留字幕和演员 ID）导致 F1 从 62.1 骤降至 32.0，降幅达 30.1 点，证实视觉帧携带的场景构图、光照变化、镜头语言等线索对边界检测具有不可替代性。
- **字幕提供互补叙事线索**：移除字幕使 F1 下降 2.4 点（62.1 → 59.7），表明对话文本蕴含的场景转换信号（如话题切换、人物互动变化）对视觉信息形成有效补充。
- **镜头 ID 标记具有结构锚定作用**：移除 Shot-ID 标记使 F1 下降 1.3 点（62.1 → 60.8），说明显式的镜头序列位置信息有助于模型建立时序参照。
- **单一模态性能对比**：仅使用视觉帧时 F1 为 52.6，仅使用字幕时 F1 为 40.0，仅使用演员 ID 时 F1 仅为 28.9，进一步印证视觉模态的主导地位与多模态融合的增益。

#### 上下文窗口设计

Table 5 展示了上下文窗口与聚焦窗口尺寸的联合消融结果：

![[assets/figures/papers/paper_list_l2416_https_openaccess_thecvf_com_content_CVPR2026_html_Berman_Scene_VLM_Multi/figures/013_Table_5.jpg]]
*Table 5: Window size ablation. Each column shows context & focus window sizes with corresponding F1 scores*

- **上下文窗口扩大带来单调增益**：在固定 10 镜头聚焦窗口下，上下文窗口从 10 增至 20 时 F1 提升至 62.1，进一步增至 30 时仍有小幅提升。更大的上下文窗口为每个边界决策提供更丰富的时序证据。
- **聚焦窗口防止边缘退化**：Figure 5 直接对比了有无聚焦机制时各序列位置的 F1 分布。无聚焦机制（红色曲线）下，序列首尾位置的性能急剧坍塌；引入聚焦机制（蓝色曲线）后，所有位置的性能保持稳定。这证实了聚焦窗口设计的核心作用——通过将预测限制在上下文充足的中央区域，避免了边缘位置因缺乏前后文信息而导致的决策失败。
- **单镜头预测退化**：将聚焦窗口缩小至 1 个镜头（l_focus=1）使性能持续下降，证明模型受益于跨多镜头的因果关联预测。

![[assets/figures/papers/paper_list_l2416_https_openaccess_thecvf_com_content_CVPR2026_html_Berman_Scene_VLM_Multi/figures/012_Figure_5.jpg]]
*Figure 5: Focus mechanism prevents edge degradation. Performance collapses at boundaries without focus mechanism (red) but remains stable with focus mechanism (blue)*

#### 每镜头帧数与模型规模

Table 6 显示每镜头采样 3 帧即可获得最佳性能（F1=62.1），继续增加帧数带来的提升有限（5 帧时 F1=62.3），表明 VLM 能从少量关键帧中高效提取视觉场景特征。

Table 7 的模型规模消融揭示了清晰的缩放规律：从 1.5B 到 7B 参数，F1 从 55.9 单调提升至 62.1（总增益 +6.2），AP 从 62.6 提升至 66.8（+4.2）。这验证了更大规模 VLM 的跨模态推理能力对场景分割任务具有直接收益。

### 注意力机制分析

通过对 VLM 内部注意力权重的分析，揭示了模型的决策依赖模式：

**模态级注意力分布** (Figure 3) 显示：(a) 聚合注意力中视觉 token 占据主导地位，同时先前输出 token 的注意力占比极高，证实了顺序预测中因果依赖的显式体现；(b) 长度归一化后的平均注意力则显示字幕和演员 ID token 的贡献与视觉 token 相当，表明文本模态在 token 级别具有密集的信息密度。

**跨镜头注意力分布** (Figure 4) 进一步展示了三个代表性镜头预测（Shot 7、Shot 11、Shot 15）对输入序列各镜头模态的注意力堆叠，直观呈现了模型在做出边界决策时如何动态分配对不同镜头和模态的关注权重。

### 可解释性评估

Table 9 评估了基础 Scene-VLM 与经解释对齐微调的 Scene-VLM + Explain 在 30 个随机采样场景过渡上的解释质量。基础模型存在严重的格式错误和幻觉问题；而仅需 35 个人工标注样本进行额外监督微调，Scene-VLM + Explain 即可将解析失败率和幻觉率均降至零。Figure 6 提供了模型生成边界判定理据的定性示例，展示其如何基于视觉变化、对话内容和人物出现等线索产生连贯的自然语言解释。

![[assets/figures/papers/paper_list_l2416_https_openaccess_thecvf_com_content_CVPR2026_html_Berman_Scene_VLM_Multi/figures/016_Table_9.jpg]]
*Table 9: Explainability evaluation. Comparison of explanation quality between Scene-VLM and Scene-VLM + Explain on 30 randomly sampled transitions. The explanation-supervised variant eliminates all formatting errors and hallucinations*

### 失败模式与局限

尽管 Scene-VLM 在多个基准上取得显著提升，其结构化 Yes/No 输出格式在保证置信度可靠提取的同时，牺牲了生成灵活性。当前框架无法处理非二值化的场景边界判定（如渐变过渡、嵌套场景结构），这构成了向更复杂视频理解任务扩展的瓶颈。此外，模型对视觉模态的强依赖（移除视觉导致 F1 骤降 30.1 点）意味着在视觉信息严重缺失或退化的场景（如极暗画面、纯对话片段）中性能可能显著退化。

![[assets/figures/papers/paper_list_l2416_https_openaccess_thecvf_com_content_CVPR2026_html_Berman_Scene_VLM_Multi/figures/005_Figure_3.jpg]]
*Figure 3: Attention by modality. Visualization of attention distribution across input modalities (visual, subtitles, and actor IDs) as well as preceding output shot predictions. (a) Summed attention reveals strong visual dominance and high dependency on prior output tokens. (b) Averaged (length-normalized) attention highlights that subtitles and actor IDs contribute comparably to visual tokens*

## 定位与知识库关联

### 任务定位：视频场景分割的范式迁移

视频场景分割（Video Scene Segmentation）旨在将一部电影或长视频划分为叙事上连贯的场景单元。传统方法长期受困于**视觉中心偏差**——过度依赖帧间视觉相似度，而忽略了对话、字幕、角色出场等承载叙事线索的文本信号。更关键的是，几乎所有先前工作都采用**逐点独立预测范式**：对每个镜头（shot）独立判断是否为场景边界，缺乏对序列因果依赖的建模。这一设计使得模型无法利用“前一个镜头已被判定为边界”这一关键上下文来影响后续决策，同时也不具备可解释性——用户无法获知模型为何做出某个边界判断。

Scene-VLM 的核心贡献在于**将场景分割从“逐点分类”重构为“因果序列预测”**，并首次引入视觉-语言模型（VLM）作为预测器。这一范式迁移带来了连锁效应：VLM 天然支持多模态联合推理（视觉帧 + 字幕 + 角色元数据），其自回归生成机制天然满足因果依赖，而 token 级 logits 则为置信度提取提供了可操作的接口。

### 与基线方法的关系图谱

#### 编码器式方法：性能天花板与模态盲区

**TranS4mer**（Islam et al., CVPR 2023）是 Scene-VLM 之前 MovieNet 上的领先方法，其结合状态空间模型与自注意力机制进行镜头序列编码。该方法在 MovieNet-318 上达到 48.4 F1 / 60.8 AP，但其设计存在两个结构性局限：（1）逐点独立预测，缺乏序列因果推理；（2）尽管支持多模态输入，其模态融合是隐式的，无法像 VLM 那样进行跨模态语义对齐。Scene-VLM 在同一基准上实现 +13.7 F1 / +6.0 AP 的提升，幅度之大表明范式迁移而非渐进改进是性能跃升的主因。

**MEGA**（Sadoughi et al., ICCV 2023）融合视觉、音频和文本模态，代表了多模态融合路线的较高水平。然而其融合仍停留在特征拼接与注意力加权层面，不具备 VLM 的跨模态推理能力——例如理解“角色 A 离开房间”这一字幕信息与视觉场景切换之间的叙事关联。

**LGSS**（Rao et al., CVPR 2020）和 **ShotCoL**（Chen et al., CVPR 2021）分别探索了局部到全局的分层建模和对比自监督镜头表征学习，但均未突破逐点预测范式，且模态覆盖有限。

#### 自监督与 LLM 路线：互补与差异

**BaSSL**（Mun et al., arXiv 2022）通过边界感知的自监督预训练学习场景边界敏感的表征，其思路与 Scene-VLM 的监督微调互补——未来或可结合 BaSSL 的预训练策略降低 VLM 微调的数据需求。

**Chapter-LLaMA**（Ventura et al., CVPR 2025）是另一条基于大语言模型的路线，将视频章节划分建模为文本生成任务。Scene-VLM 在 VidChapters-7M 上的视频章节划分任务中，以匹配主干模型（Qwen2.5-VL-7B vs. LLaMA）的设置超越 Chapter-LLaMA（F1: 32.2 vs. 28.4）。两者的核心差异在于：Chapter-LLaMA 依赖纯文本输入（ASR 转录），而 Scene-VLM 同时处理视觉帧，这一多模态优势在需要视觉线索的场景边界（如无对白的转场）中尤为关键。

### 能力边界与适用条件

Scene-VLM 的能力谱系可通过 Table 1 的五维对比清晰定位：

| 能力维度 | TranS4mer | MEGA | BaSSL | Chapter-LLaMA | Scene-VLM |
|---------|-----------|------|-------|---------------|-----------|
| 序列因果预测 | ✗ | ✗ | ✗ | ✓ | ✓ |
| 置信度估计 | ✗ | ✗ | ✗ | ✗ | ✓ |
| 可解释性 | ✗ | ✗ | ✗ | ✓ | ✓ |
| 电影场景分割 | ✓ | ✓ | ✓ | ✗ | ✓ |
| 视频章节划分 | ✗ | ✗ | ✗ | ✓ | ✓ |

Scene-VLM 是首个同时覆盖全部五项能力的方法。但其适用边界同样清晰：

**模态依赖性**：消融实验（Table 4）表明，移除视觉输入导致 F1 从 62.1 骤降至 32.0，证明视觉模态对场景分割至关重要。这意味着 Scene-VLM 不适用于纯音频或纯文本的长视频场景，其性能依赖于视觉帧的可用性。

**结构化输出的代价**：当前设计采用固定的“Shot i: Yes/No”输出格式，这牺牲了生成灵活性以换取可靠的置信度提取。论文明确将此列为局限，指出未来可探索更灵活的输出机制。

**数据与计算门槛**：Scene-VLM 基于 Qwen2.5-VL-7B 微调，模型规模消融（Table 7）显示从 1.5B 到 7B 单调提升 +6.2 F1，表明性能与模型容量正相关。这暗示小规模部署场景下可能存在性能折损。

**跨域泛化**：在 BBC Planet Earth 纪录片上的零样本测试中，Scene-VLM 以 45.8 AP 超越 TranS4mer 的 43.6 AP，但相比 MovieNet 上的大幅领先有所收窄。纪录片与剧情片在叙事结构上的差异（如缺乏明确角色线索）可能限制了多模态推理的增益空间。

### 局限与开放问题

论文明确指出的局限是**结构化 Yes/No 输出格式**对生成灵活性的限制。这一设计选择是置信度提取可靠性的保障——通过比较“Yes”和“No”两个 token 的 logits 来归一化置信度（公式 $ \mathrm{conf}_i = \frac{p_i(\mathrm{Yes})}{p_i(\mathrm{Yes}) + p_i(\mathrm{No})} $），若输出格式不固定则无法定位对应 token 位置。这构成了一个“可解释性-灵活性”的权衡。

论文提出的开放问题指向两个方向：

1. **更灵活的输出机制**：能否设计一种输出格式，在保持置信度提取可靠性的同时允许更丰富的生成表达？例如，允许模型在输出“Yes/No”的同时生成简短的边界理由，而非将解释生成作为后处理对齐步骤。

2. **推理与预测的融合**：当前的解释生成是通过额外微调实现的“事后解释”（post-hoc explanation），而非预测过程中的“内省推理”。论文提出未来可结合强化学习，将显式推理步骤融入预测过程，使模型在做出边界决策时同时生成推理链，从而同时提升准确性和可解释性。这一方向与近期推理增强语言模型（如 o1 系列）的思路一致。

此外，从知识库定位角度看，Scene-VLM 开创了“VLM for Video Structuring”这一子方向。其核心洞察——利用 VLM 的跨模态推理能力将视频结构化任务重构为序列预测问题——具有可迁移性：视频摘要、精彩片段检测、叙事弧线分析等任务同样涉及对长视频序列的结构化理解，可能受益于类似的范式迁移。

## 原文 PDF

![[paperPDFs/CVPR_2026/Scene_VLM_Multimodal_Video_Scene_Segmentation_via_Vision_Language_Models.pdf]]
